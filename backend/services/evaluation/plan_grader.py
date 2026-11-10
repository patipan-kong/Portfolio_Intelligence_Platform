"""plan_grader.py — AI Evaluation M2: Day-0 Plan Grade.

Scores the *execution plan* the moment it exists — before any human decides
anything, before any trade fills — so a bad plan can be told apart from a
bad outcome (PLAN §4.6, OPTIMIZER_PHILOSOPHY.md §12). This is a Belief-free,
deterministic composite over data the pipeline already produced:

    necessity                 (weight 30) — share of candidate SELL/REDUCE
                               trades that are either Required-tier (Reason
                               = Mandatory Risk Reduction / Policy
                               Enforcement) or actively serving as a funding
                               source today. A plan padded with discretionary
                               trades that end up deferred scores lower here
                               — every trade on the plan should be doing a
                               job, per OPTIMIZER_PHILOSOPHY.md §8.
    funding_efficiency         (weight 30) — THE BH-INCIDENT METRIC. Of the
                               total amount discretionary (Portfolio
                               Improvement) candidates proposed to release,
                               what fraction was actually needed to close the
                               funding gap? A REDUCE proposing far more than
                               the gap requires scores near the floor even
                               though services/optimizer/execution_optimizer.py
                               already defers the unneeded portion — this
                               sub-score grades the RECOMMENDATION's own
                               proportionality, not just whether the
                               execution-optimization stage caught it.
    turnover_proportionality   (weight 20) — reads the already-computed
                               TURNOVER_BREACH violation_detail (if any) from
                               policy_engine.compute_policy_alignment_score;
                               100 when absent, decaying with the recorded
                               overshoot ratio when present. No turnover
                               math is re-derived here (PLAN §4.6).
    explanation_completeness   (weight 20) — every SELL/REDUCE candidate
                               execution_optimizer produced must carry a
                               non-empty reason/necessity/execution_role/
                               execution_state/note; a no-trade plan must
                               carry a portfolio_assessment or
                               no_action_summary. This is an invariant check
                               on an already-guaranteed property, not new
                               judgment.

Legacy and Sector Advisory v1 grades re-derive the execution plan from stored
inputs. MUJI V2 grades the canonical frozen monetary schedule and marks
incomplete or contradictory evidence unavailable.

Zero AI calls, zero DB writes to anything but `recommendation_grades`
(append-only, P3), zero mutation of `RecommendationSnapshot`/
`OptimizerHistory` (PLAN §4.1). See services/evaluation/__init__.py for the
full constraint list.

Public API
----------
read_snapshot_plan_inputs(db, snap) -> dict | None
    Thin ORM-boundary reader: reconstructs (target_allocations,
    violations, violation_details, cash_available, portfolio_assessment,
    no_action_summary) from a RecommendationSnapshot + its linked
    OptimizerHistory.result_json. Single place this reconstruction is
    written (ENGINEERING_PRINCIPLES Single Source of Truth) — reused by
    grade_pending_plans below and by services/evaluation/
    recommendation_ledger.py + execution_ledger.py (M3) so the Report
    Card / execution ledger never re-derive "what does this snapshot's
    plan look like" a second way. Returns None when
    projected_allocations_json is missing/unparseable (caller decides
    how to report the skip).
derive_full_plan(target_allocations, cash_available, violations=None) -> dict
    Shared "what does the day-0 plan actually say" derivation — buy-side
    trades plus the resolved SELL/REDUCE ExecutionOptimizationResult. Reused
    by services/evaluation/execution_analyzer.py so the notion of "the plan"
    is computed in exactly one place (PLAN §4.5).
compute_plan_grade(target_allocations, cash_available, violations, ...) -> dict
    Pure function: the 0-100 composite + documented sub-scores + weights.
grade_pending_plans(db, portfolio_id=None) -> dict
    {"graded": [...], "skipped": [...]} — writes grade_kind="PLAN" rows for
    every RecommendationSnapshot lacking one.
"""
from __future__ import annotations

import json
import logging
from math import ceil, isfinite
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# Composite weights (documented, sum to 100). See module docstring for what
# each sub-score measures and why it is weighted this way.
_WEIGHT_NECESSITY = 30.0
_WEIGHT_FUNDING_EFFICIENCY = 30.0
_WEIGHT_TURNOVER = 20.0
_WEIGHT_EXPLANATION = 20.0
_MUJI_PLAN_GRADE_VERSION = "wealth.plan-grade-muji.v2"


def _compute_muji_plan_grade(
    target_allocations: list[dict], cash_available: float,
    portfolio_assessment: str | None, no_action_summary: str | None,
    provenance: dict[str, Any],
) -> dict[str, Any]:
    """Grade frozen advisory-plan integrity, never investment performance."""
    from services.optimizer.execution_optimizer import ExecutionOptimizationResult
    from services.optimizer.sector_policy import UnsupportedOptimizerPolicyEvidence

    try:
        raw = provenance["scheduled_execution"]
        if not isinstance(raw, dict) or any(raw.get(k) is None for k in (
            "scheduled_buys", "scheduled_changes", "estimated_trade_costs",
            "scheduled_turnover_pct", "effective_turnover_cap_pct",
        )):
            raise ValueError("Incomplete frozen monetary schedule")
        plan = ExecutionOptimizationResult.model_validate(raw)
        buys = plan.scheduled_buys or {}
        changes = plan.scheduled_changes or {}
        costs = plan.estimated_trade_costs or {}
        allocations = {a["symbol"]: a for a in target_allocations}
        if len(allocations) != len(target_allocations):
            raise ValueError("Duplicate allocation symbols")
        if not isfinite(float(cash_available)) or not all(isfinite(v) and v >= 0 for v in (
            plan.cash_available, plan.idle_cash_after, plan.total_buy_deployment, plan.funding_gap,
            plan.scheduled_turnover_pct, plan.effective_turnover_cap_pct,
            *buys.values(), *costs.values(),
        )):
            raise ValueError("Invalid monetary value")
        if plan.valuation_nav is not None and (not isfinite(plan.valuation_nav) or plan.valuation_nav < 0):
            raise ValueError("Invalid valuation NAV")
        if not all(isfinite(v) for v in changes.values()):
            raise ValueError("Invalid scheduled change")
        if abs(plan.cash_available - cash_available) > 0.011:
            raise ValueError("Frozen cash disagrees with run")
        if set(costs) != {s for s, v in changes.items() if abs(v) > 0.001}:
            raise ValueError("Trade cost evidence disagrees with schedule")
        for symbol, amount in buys.items():
            if allocations[symbol]["action"] not in ("BUY", "ACCUMULATE") or amount <= 0 or abs(changes[symbol] - amount) > 0.011:
                raise ValueError("Invalid frozen BUY direction")
        sales = {t.symbol: t for t in plan.trades}
        positions = (provenance.get("concentration") or {}).get("positions") or {}
        if len(sales) != len(plan.trades):
            raise ValueError("Duplicate frozen SELL")
        for symbol, trade in sales.items():
            if not all(isfinite(v) and v >= 0 for v in
                       (trade.full_recommended_amount, trade.executed_amount)):
                raise ValueError("Invalid frozen SELL amount")
            if trade.scheduled_cash_impact is not None and not isfinite(trade.scheduled_cash_impact):
                raise ValueError("Invalid frozen SELL cash impact")
            if allocations[symbol]["action"] not in ("SELL", "REDUCE") or trade.action != allocations[symbol]["action"]:
                raise ValueError("Invalid frozen SELL direction")
            if trade.executed_amount < 0 or abs(changes.get(symbol, 0) + trade.executed_amount) > 0.011:
                raise ValueError("Frozen sale disagrees with schedule")
            if trade.executed_amount and (trade.funding_basis != "INDEPENDENT_FROZEN_SELL_SIGNAL"
                                          or trade.evidence_status == "UNVERIFIED" or trade.execution_state == "DEFERRED"):
                raise ValueError("Unsupported scheduled SELL")
            if trade.executed_amount and (positions.get(symbol, {}).get("sell_signal") is not True
                                          or allocations[symbol].get("decision_basis") in
                                          ("SECTOR_ADVISORY", "CONCENTRATION_ADVISORY")):
                raise ValueError("Scheduled SELL lacks independent frozen signal")
        if any(symbol not in buys and symbol not in sales for symbol in changes):
            raise ValueError("Unrecognized scheduled action")
        expected_cash = plan.cash_available - sum(changes.values()) - sum(costs.values())
        if abs(expected_cash - plan.idle_cash_after) > 0.021:
            raise ValueError("Frozen cash does not reconcile")
        cash_floor_pct = (provenance.get("hard_constraints") or {}).get("min_cash_pct")
        if cash_floor_pct is not None and not isfinite(float(cash_floor_pct)):
            raise ValueError("Invalid frozen cash floor")
        if provenance.get("total_value") is not None and not isfinite(float(provenance["total_value"])):
            raise ValueError("Invalid frozen total value")
        if cash_floor_pct and provenance.get("total_value") is not None and (
            plan.idle_cash_after + 0.021 < float(provenance["total_value"]) * float(cash_floor_pct) / 100
        ):
            raise ValueError("Frozen cash violates the applicable cash floor")
        if abs(plan.total_buy_deployment - sum(buys.values())) > 0.011:
            raise ValueError("Frozen BUY total does not reconcile")
        if any(cost < 0 or abs(cost - ceil(abs(changes[symbol]) * 0.0015 * 100 - 1e-8) / 100) > 0.011
               for symbol, cost in costs.items()):
            raise ValueError("Frozen trading friction does not reconcile")
        if plan.valuation_nav and abs(plan.scheduled_turnover_pct -
                                      sum(abs(value) for value in changes.values()) / plan.valuation_nav * 100) > 0.011:
            raise ValueError("Frozen turnover does not reconcile")
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise UnsupportedOptimizerPolicyEvidence("Missing or contradictory frozen MUJI V2 schedule") from exc

    # No investment-merit inference: a frozen independent signal permits a
    # sale to count as supported, whether it funds a BUY or retains CASH.
    proposed = [a for a in target_allocations if a.get("action") in ("BUY", "ACCUMULATE", "SELL", "REDUCE")]
    supported = sum(
        (a["symbol"] in buys if a["action"] in ("BUY", "ACCUMULATE")
         else sales[a["symbol"]].executed_amount > 0 and
              sales[a["symbol"]].funding_basis == "INDEPENDENT_FROZEN_SELL_SIGNAL")
        for a in proposed if a["symbol"] in allocations and
        (a["action"] in ("BUY", "ACCUMULATE") or a["symbol"] in sales)
    )
    evidence_score = round(100 * supported / len(proposed), 2) if proposed else 100.0
    # A deferred BUY or SELL is a recommendation, never an executed action.
    feasibility_score = 100.0
    cap = plan.effective_turnover_cap_pct
    turnover_score = 100.0 if cap == 0 and plan.scheduled_turnover_pct == 0 else max(
        0.0, round(100 * (1 - max(0.0, plan.scheduled_turnover_pct - cap) / (cap or 1)), 2))
    complete = sum(bool(t.reason and t.execution_role and t.execution_state and t.note)
                   for t in plan.trades)
    explanation_score = (round(100 * complete / len(plan.trades), 2) if plan.trades else
                         100.0 if (portfolio_assessment or no_action_summary) else 60.0)
    weights = {"schedule_feasibility": 30.0, "action_evidence": 30.0,
               "turnover_proportionality": 20.0, "explanation_completeness": 20.0}
    return {
        "score": round((feasibility_score * 30 + evidence_score * 30 + turnover_score * 20
                        + explanation_score * 20) / 100, 2),
        "grade_version": _MUJI_PLAN_GRADE_VERSION,
        "grade_scope": "advisory_plan_and_execution_quality_not_investment_performance",
        "component_definitions": {
            "schedule_feasibility": "Frozen directions, friction and cash reconcile; no broker execution implied.",
            "action_evidence": "Share of proposed actions scheduled with required independent SELL evidence; funding role adds no credit.",
            "turnover_proportionality": "Scheduled turnover against the frozen applicable turnover safeguard.",
            "explanation_completeness": "Frozen sale explanations, or recorded no-action assessment, are present.",
        },
        "schedule_feasibility_score": feasibility_score,
        "action_evidence_score": evidence_score,
        "turnover_proportionality_score": turnover_score,
        "explanation_completeness_score": explanation_score,
        "weights": weights,
        "trade_count": len(plan.trades),
        "deferred_count": sum(t.execution_state == "DEFERRED" for t in plan.trades),
        "scheduled_buy_count": len(buys),
        "cash_available": plan.cash_available,
        "projected_cash": plan.idle_cash_after,
    }


def _derive_action_summary_and_buys(
    target_allocations: list[dict],
) -> tuple[dict, list[dict], float]:
    """BUY-side trades never pass through execution_optimizer (it only ever
    classifies SELL/REDUCE candidates — PLAN §5/§7) so the buy side of the
    plan is read directly off the already-computed action_summary buckets.
    """
    from services.optimizer_action_summary import build_action_summary

    action_summary = build_action_summary(target_allocations or [])
    by_symbol = {a.get("symbol"): a for a in (target_allocations or []) if a.get("symbol")}

    buy_trades: list[dict] = []
    total_buy_deployment = 0.0
    for group in ("accumulate", "new_position"):
        for entry in action_summary.get(group, []):
            alloc = by_symbol.get(entry.get("symbol"))
            if not alloc:
                continue
            amount = abs(float(alloc.get("estimated_amount") or 0.0))
            total_buy_deployment += amount
            buy_trades.append({
                "symbol": entry["symbol"],
                "action": alloc.get("action", "BUY"),
                "planned_amount": amount,
            })

    return action_summary, buy_trades, total_buy_deployment


def read_snapshot_plan_inputs(
    db: Session, snap: Any, *, raise_on_unsupported_policy: bool = False,
) -> dict[str, Any] | None:
    """Reconstruct the stored plan inputs for one RecommendationSnapshot.

    Reads target_allocations/active_policy directly off the snapshot
    (stored verbatim by snapshot_writer.py) and cash_balance/
    portfolio_assessment/no_action_summary off the linked
    OptimizerHistory.result_json (the snapshot itself has no cash_balance
    column). result_json is committed before main.py appends the
    action_summary/execution_optimization response-time views to the
    in-memory result dict (main.py:~2409 precedes :~2599/:2610) — so this
    read is stable and reproducible (PLAN §4.1).

    Returns None (never raises) when projected_allocations_json is
    missing or unparseable.
    """
    from models.database import OptimizerHistory

    if not snap.projected_allocations_json:
        return None
    try:
        target_allocations = json.loads(snap.projected_allocations_json)
    except Exception:
        return None

    active_policy: dict = {}
    if snap.active_policy_json:
        try:
            active_policy = json.loads(snap.active_policy_json)
        except Exception:
            active_policy = {}

    oh = (
        db.query(OptimizerHistory).filter_by(id=snap.optimizer_history_id).first()
        if snap.optimizer_history_id else None
    )
    cash_available = 0.0
    portfolio_assessment = None
    no_action_summary = None
    run_total_value = None
    run_cash_balance = None
    stored = {}
    if oh and oh.result_json:
        try:
            stored = json.loads(oh.result_json)
            run_total_value = stored.get("total_value")
            run_cash_balance = stored.get("cash_balance")
            cash_available = float(stored.get("cash_balance") or 0.0)
            portfolio_assessment = stored.get("portfolio_assessment")
            no_action_summary = stored.get("no_action_summary")
        except Exception:
            pass

    if not isinstance(stored, dict):
        stored = {}
    stored_policy = stored.get("active_policy") or {}
    from services.optimizer.sector_policy import (
        OPTIMIZER_POLICY_MUJI_V2, UnsupportedOptimizerPolicyEvidence, optimizer_policy_mode,
        sector_caps_are_advisory, validate_frozen_optimizer_policy,
    )

    try:
        try:
            snapshot_envelope = json.loads(getattr(snap, "constraint_envelope_json", None) or "null")
        except (TypeError, ValueError):
            snapshot_envelope = None
        optimizer_policy_mode(stored_policy, effective_envelope=stored.get("effective_envelope"))
        optimizer_policy_mode(active_policy, effective_envelope=snapshot_envelope)
        if stored_policy and active_policy and (
            stored_policy.get("optimizer_policy_mode") != active_policy.get("optimizer_policy_mode")
        ):
            raise UnsupportedOptimizerPolicyEvidence("Snapshot and run policy modes disagree")
        if sector_caps_are_advisory(stored_policy):
            # Older snapshots can lack fields that were captured in the run.
            active_policy = {**stored_policy, **active_policy}
        policy_mode = validate_frozen_optimizer_policy(active_policy)
    except UnsupportedOptimizerPolicyEvidence:
        if raise_on_unsupported_policy:
            raise
        return None

    return {
        "target_allocations": target_allocations,
        "violations": active_policy.get("violations") or [],
        "violation_details": active_policy.get("violation_details") or [],
        "cash_available": cash_available,
        "portfolio_assessment": portfolio_assessment,
        "no_action_summary": no_action_summary,
        # The Report Card uses the frozen schedule for new runs and qualifies
        # the recorded classification for older runs.
        "policy_provenance": {
            "violation_evidence": active_policy.get("violation_evidence"),
            **{key: active_policy[key] for key in ("concentration", "scheduled_execution", "optimizer_policy_mode")
               if key in active_policy},
            **{key: active_policy[key] for key in ("sector_policy_mode", "sector_alternatives",
                                                "scheduled_action_summary", "hard_policy_unavailable", "emergency_override")
               if sector_caps_are_advisory(active_policy) and key in active_policy},
            **{key: stored[key] for key in ("execution_policy_version", "scheduled_execution")
               if key in stored and (key != "scheduled_execution" or policy_mode != OPTIMIZER_POLICY_MUJI_V2)},
            "hard_constraints": active_policy.get("hard_constraints"),
            "max_single_position_pct": (active_policy.get("hard_constraints") or {}).get("max_single_position_pct"),
            "total_value": run_total_value,
            "cash_balance": run_cash_balance,
        },
    }


def advisory_plan_provenance(inputs: dict[str, Any]) -> dict[str, Any] | None:
    """Use the frozen plan for new consumers while preserving legacy derivations."""
    from services.optimizer.sector_policy import sector_caps_are_advisory

    provenance = inputs.get("policy_provenance")
    return provenance if sector_caps_are_advisory(provenance) else None


def derive_full_plan(
    target_allocations: list[dict],
    cash_available: float,
    violations: list[str] | None = None,
    policy_provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Re-derive the complete day-0 plan: buy-side trades + the resolved
    SELL/REDUCE ExecutionOptimizationResult. Single source of truth for
    "what the plan says," shared by compute_plan_grade (below) and
    services/evaluation/execution_analyzer.py's plan-vs-actual comparison.

    Provenance-aware callers use the same classifier or frozen schedule as
    the optimizer page. Older grade and analytics callers retain their
    original derivation when provenance is absent.
    """
    from services.optimizer.execution_optimizer import optimize_execution, optimize_execution_for_payload

    action_summary, buy_trades, total_buy_deployment = _derive_action_summary_and_buys(
        target_allocations
    )
    if policy_provenance is not None:
        active_policy: dict[str, Any] = {
            "violations": violations or [],
            "hard_constraints": policy_provenance.get("hard_constraints") or {
                "max_single_position_pct": policy_provenance.get("max_single_position_pct"),
            },
            **{key: policy_provenance[key] for key in ("concentration", "scheduled_execution", "sector_policy_mode",
                                                     "optimizer_policy_mode",
                                                     "hard_policy_unavailable", "emergency_override")
               if key in policy_provenance},
        }
        if policy_provenance.get("violation_evidence") is not None:
            active_policy["violation_evidence"] = policy_provenance["violation_evidence"]
        eo = optimize_execution_for_payload(
            {
                "active_policy": active_policy,
                "target_allocations": target_allocations or [],
                "total_value": policy_provenance.get("total_value"),
                "cash_balance": policy_provenance.get("cash_balance"),
                "execution_policy_version": policy_provenance.get("execution_policy_version"),
            },
            policy_provenance.get("scheduled_action_summary", action_summary),
            cash_available=cash_available,
        )
    else:
        eo = optimize_execution(
            action_summary, target_allocations or [], cash_available, violations=violations
        )
    if eo.scheduled_buys is not None:
        by_symbol = {row["symbol"]: row for row in target_allocations}
        buy_trades = [
            {"symbol": symbol, "action": by_symbol.get(symbol, {}).get("action", "BUY"), "planned_amount": amount}
            for symbol, amount in eo.scheduled_buys.items()
        ]
        total_buy_deployment = eo.total_buy_deployment
    return {
        "buy_trades": buy_trades,
        "total_buy_deployment": total_buy_deployment,
        "execution_optimization": eo,
    }


def compute_plan_grade(
    target_allocations: list[dict],
    cash_available: float,
    violations: list[str] | None = None,
    violation_details: list[dict] | None = None,
    portfolio_assessment: str | None = None,
    no_action_summary: str | None = None,
    policy_provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Pure function: the day-0 plan composite. No DB, no AI — fully
    reproducible from the four stored arguments (asserted in tests)."""
    from services.optimizer.execution_optimizer import (
        NECESSITY_DISCRETIONARY,
        ROLE_FUNDING_SOURCE,
        STATE_DEFERRED,
    )

    if policy_provenance is not None:
        from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, optimizer_policy_mode
        if optimizer_policy_mode(policy_provenance) == OPTIMIZER_POLICY_MUJI_V2:
            return _compute_muji_plan_grade(
                target_allocations, cash_available, portfolio_assessment,
                no_action_summary, policy_provenance,
            )

    plan = derive_full_plan(target_allocations, cash_available, violations, policy_provenance)
    eo = plan["execution_optimization"]
    trades = eo.trades

    # ── Necessity: share of candidates that are Required-tier or actively funding today ──
    if trades:
        necessary_or_funding = sum(
            1 for t in trades
            if t.necessity != NECESSITY_DISCRETIONARY or t.execution_role == ROLE_FUNDING_SOURCE
        )
        necessity_score = round(100.0 * necessary_or_funding / len(trades), 2)
    else:
        necessity_score = 100.0

    # ── Funding efficiency: the BH-incident metric ──
    total_discretionary_recommended = sum(
        (trade.discretionary_amount if trade.discretionary_amount is not None else
         trade.full_recommended_amount if trade.necessity == NECESSITY_DISCRETIONARY else 0)
        for trade in trades
    )
    if total_discretionary_recommended <= 0:
        funding_efficiency_score = 100.0
    else:
        excess = max(0.0, total_discretionary_recommended - eo.funding_gap)
        funding_efficiency_score = round(
            100.0 * (1 - excess / total_discretionary_recommended), 2
        )

    # ── Turnover proportionality: reuses the already-computed TURNOVER_BREACH detail ──
    turnover_viol = next(
        (v for v in (violation_details or []) if v.get("violation_type") == "TURNOVER_BREACH"),
        None,
    )
    proposed = eo.scheduled_turnover_pct
    allowed = eo.effective_turnover_cap_pct
    if proposed is None:
        proposed = float((turnover_viol or {}).get("proposed_pct") or 0.0)
        allowed = float((turnover_viol or {}).get("allowed_pct") or 1.0)
    overshoot_ratio = max(0.0, (proposed - (allowed or 0.0)) / (allowed or 1.0))
    turnover_score = max(0.0, round(100.0 - overshoot_ratio * 100, 2))

    # ── Explanation completeness ──
    if trades:
        complete = sum(
            1 for t in trades
            if t.reason and t.necessity and t.execution_role and t.execution_state and t.note
        )
        explanation_score = round(100.0 * complete / len(trades), 2)
    else:
        explanation_score = 100.0 if (portfolio_assessment or no_action_summary) else 60.0

    composite = round(
        (
            necessity_score * _WEIGHT_NECESSITY
            + funding_efficiency_score * _WEIGHT_FUNDING_EFFICIENCY
            + turnover_score * _WEIGHT_TURNOVER
            + explanation_score * _WEIGHT_EXPLANATION
        )
        / 100.0,
        2,
    )

    deferred_count = sum(1 for t in trades if t.execution_state == STATE_DEFERRED)

    return {
        "score": composite,
        "necessity_score": necessity_score,
        "funding_efficiency_score": funding_efficiency_score,
        "turnover_proportionality_score": turnover_score,
        "explanation_completeness_score": explanation_score,
        "weights": {
            "necessity": _WEIGHT_NECESSITY,
            "funding_efficiency": _WEIGHT_FUNDING_EFFICIENCY,
            "turnover_proportionality": _WEIGHT_TURNOVER,
            "explanation_completeness": _WEIGHT_EXPLANATION,
        },
        "trade_count": len(trades),
        "deferred_count": deferred_count,
        "funding_gap": eo.funding_gap,
        "cash_available": eo.cash_available,
    }


def grade_pending_plans(db: Session, portfolio_id: int | None = None) -> dict[str, Any]:
    """Write grade_kind="PLAN" rows for every RecommendationSnapshot lacking one.

    Reads target_allocations/active_policy directly off RecommendationSnapshot
    (already stored there verbatim by snapshot_writer.py) and cash_balance /
    portfolio_assessment / no_action_summary from the linked OptimizerHistory
    .result_json (RecommendationSnapshot has no cash_balance column of its
    own). result_json is committed before main.py appends the action_summary
    /execution_optimization response-time views to the in-memory result dict
    (verified main.py:2409 precedes :2599/:2610) — so this read is stable and
    reproducible, never racing a later mutation (PLAN §4.1).

    Missing data => skip with a logged reason, same convention as
    horizon_grader.grade_due_recommendations; never raises per-snapshot.
    """
    from models.database import RecommendationGrade, RecommendationSnapshot, Workspace
    from services.optimizer.sector_policy import (
        UNSUPPORTED_OPTIMIZER_POLICY_EVIDENCE, UnsupportedOptimizerPolicyEvidence,
    )

    graded: list[dict] = []
    skipped: list[dict] = []

    for ws in db.query(Workspace).all():
        q = db.query(RecommendationSnapshot).filter(RecommendationSnapshot.workspace_id == ws.id)
        if portfolio_id is not None:
            q = q.filter(RecommendationSnapshot.portfolio_id == portfolio_id)

        for snap in q.all():
            already = (
                db.query(RecommendationGrade)
                .filter_by(recommendation_snapshot_id=snap.id, grade_kind="PLAN")
                .first()
            )
            if already:
                continue

            try:
                inputs = read_snapshot_plan_inputs(db, snap, raise_on_unsupported_policy=True)
            except UnsupportedOptimizerPolicyEvidence:
                skipped.append({"snapshot_id": snap.id, "reason": UNSUPPORTED_OPTIMIZER_POLICY_EVIDENCE})
                continue
            if inputs is None:
                reason = "no_target_allocations" if not snap.projected_allocations_json else "unparseable_allocations"
                skipped.append({"snapshot_id": snap.id, "reason": reason})
                continue

            provenance = inputs["policy_provenance"]
            versioned_plan = any(key in provenance for key in
                                 ("execution_policy_version", "concentration", "sector_policy_mode"))
            try:
                result = compute_plan_grade(
                    inputs["target_allocations"], inputs["cash_available"],
                    inputs["violations"], inputs["violation_details"],
                    portfolio_assessment=inputs["portfolio_assessment"],
                    no_action_summary=inputs["no_action_summary"],
                    policy_provenance=provenance if versioned_plan else None,
                )
            except UnsupportedOptimizerPolicyEvidence:
                skipped.append({"snapshot_id": snap.id, "reason": UNSUPPORTED_OPTIMIZER_POLICY_EVIDENCE})
                continue

            grade = RecommendationGrade(
                workspace_id=ws.id,
                recommendation_snapshot_id=snap.id,
                portfolio_id=snap.portfolio_id,
                grade_kind="PLAN",
                graded_at=datetime.utcnow(),
                window_start=None,
                window_end=None,
                score=result["score"],
                detail_json=json.dumps(result, default=str),
                created_at=datetime.utcnow(),
            )
            try:
                db.add(grade)
                db.commit()
            except Exception as exc:
                db.rollback()
                logger.warning("[EVAL] PLAN grade write failed snapshot_id=%s: %s", snap.id, exc)
                skipped.append({"snapshot_id": snap.id, "reason": "write_failed"})
                continue

            graded.append({"snapshot_id": snap.id, "score": result["score"]})
            logger.info("[EVAL] Graded PLAN snapshot_id=%s score=%s", snap.id, result["score"])

    return {"graded": graded, "skipped": skipped}
