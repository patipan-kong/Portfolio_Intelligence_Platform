"""opportunity_cost.py — AI Evaluation M5: Counterfactual Opportunity-Cost Ledger.

Prices what every divergence from the AI's recommendation actually did (UX
S6; OPTIMIZER_PHILOSOPHY.md §12 "a philosophy that cannot measure its own
downside is dogma"). A divergence is any decision that was not full
compliance: REJECTED, PARTIAL_EXECUTION, MANUAL_OVERRIDE, or an
is_system_generated EXPIRED row (P4 — an ignored recommendation nobody
explicitly rejected).

Pricing method — reuses grade rows, never re-derives return math (PLAN
§4.6): for the divergent decision's recommendation snapshot, the nearest
matured RecommendationGrade horizon row (grade_kind H7/H30/H90/H180,
written by M1's horizon_grader) already holds
`return_pct` = the recommendation-keyed shadow's return — i.e. exactly
"what would have happened had this recommendation been followed in full."
the owner's cash-flow-adjusted TWR is then chained over that grade's OWN
[window_start, window_end] (Phase 4.24 — never decision-date→today), so both
sides cover the same interval. The difference, where a positive number means
"diverging helped you", is the row's counterfactual_delta_pct (percentage
points):

    counterfactual_delta_pct = actual_return_pct − counterfactual_recommendation_return_pct

The headline is the MEAN of valid deltas (mean_decision_delta_pp), not a sum:
decision windows overlap, so summing is not a portfolio-level figure
(DECISION_LOG Phase 4.24). Rows without a valid matched comparison are
"maturing" (no grade) or "unavailable" (explicit reason) — never zero.

This is a **decision-level approximation**, not a per-symbol figure — the
data model does not record which individual trade within a multi-trade
recommendation drove a REJECTED/PARTIAL/OVERRIDE decision, the same
documented limitation execution_ledger.py's acceptance_by_class already
carries (PLAN §4.7, surfaced via the `note` field on every row, never
hidden).

System's-own-deferrals honesty strip: execution_optimizer.py defers
SELL/REDUCE candidates whose funding need disappeared (OPTIMIZER_PHILOSOPHY
§7 STATE_DEFERRED). Per UX S6 this deserves its own accountability ledger —
"the Opportunity Cost metric pointed at the machine" — but pricing one
deferred trade in isolation would need a per-symbol counterfactual price
series this system does not yet track (no such infrastructure exists for
single trades, only for whole recommendations via the recommendation-keyed
shadow). Rather than fabricate a number, each deferral is reported
structurally (symbol, reason, snapshot) with counterfactual_pricing
explicitly "unavailable" — PLAN §4.7/§4.8: never a guessed return.

Zero AI calls. Zero writes — this module only reads RecommendationGrade,
UserExecutionDecision, RecommendationSnapshot (PLAN §4.1).

Public API
----------
compute_opportunity_cost(db, portfolio_id, period_days=90) -> dict
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# APPROVED = full compliance, never a divergence. Every other recorded
# decision type is a divergence worth pricing.
_DIVERGENT_DECISIONS = ("REJECTED", "PARTIAL_EXECUTION", "MANUAL_OVERRIDE", "EXPIRED")

# Max days a human decision may trail the grade window's start (the recommendation
# date) and still be priced over that window. EXPIRED is exempt: it records
# inaction, which holds from the recommendation date, not a dated user action.
_MAX_DECISION_DELAY_DAYS = 1


def _divergence_type(dec: Any) -> str | None:
    if dec.decision not in _DIVERGENT_DECISIONS:
        return None
    return dec.decision


def _system_deferrals(db: Session, ws: int, portfolio_id: int, cutoff: datetime) -> list[dict[str, Any]]:
    from models.database import RecommendationSnapshot
    from services.evaluation.plan_grader import (
        advisory_plan_provenance, derive_full_plan, read_snapshot_plan_inputs,
    )
    from services.optimizer.execution_optimizer import STATE_DEFERRED

    snaps = (
        db.query(RecommendationSnapshot)
        .filter(
            RecommendationSnapshot.workspace_id == ws,
            RecommendationSnapshot.portfolio_id == portfolio_id,
            RecommendationSnapshot.created_at >= cutoff,
        )
        .order_by(RecommendationSnapshot.created_at.desc())
        .all()
    )

    deferrals: list[dict[str, Any]] = []
    for snap in snaps:
        inputs = read_snapshot_plan_inputs(db, snap)
        if inputs is None:
            continue
        plan = derive_full_plan(inputs["target_allocations"], inputs["cash_available"], inputs["violations"],
                                advisory_plan_provenance(inputs))
        for t in plan["execution_optimization"].trades:
            if t.execution_state != STATE_DEFERRED:
                continue
            deferrals.append({
                "snapshot_id": snap.id,
                "date": snap.created_at.isoformat() + "Z" if snap.created_at else None,
                "symbol": t.symbol,
                "action": t.action,
                "reason": t.reason,
                "note": t.note,
                "counterfactual_pricing": "unavailable",
                "counterfactual_reason": (
                    "Pricing one deferred trade in isolation requires a per-trade "
                    "counterfactual price series that is not yet tracked; recorded "
                    "structurally (symbol + reason) only — never a fabricated return."
                ),
            })
    return deferrals


def _owner_return_between(
    db: Session, portfolio_id: int, window_start: str, window_end: str,
) -> tuple[float | None, str | None]:
    """Owner's cash-flow-adjusted TWR over exactly (window_start, window_end].

    Returns (return_pct, None) or (None, reason). Never fabricates: needs a
    usable owner observation at-or-before each boundary (within the grade
    grader's own valuation-gap tolerance), at least one daily return inside
    the window, and an investment_return_pct (cash-flow-adjusted) on every
    row chained. A genuine 0.0% is a valid return, distinct from None.
    """
    from models.database import PortfolioSnapshot
    from services.analytics.attribution_engine import _compute_twr
    from services.evaluation.horizon_grader import _MAX_VALUATION_GAP_DAYS

    try:
        start_d = datetime.strptime(window_start, "%Y-%m-%d").date()
        end_d = datetime.strptime(window_end, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None, "grade_window_unparseable"
    if end_d <= start_d:
        return None, "grade_window_empty"

    # Uncovered days tolerated at each boundary scale with the window so a 5-day
    # slack never swallows most of an H7 window (7d -> 1, 30d -> 3, 90d+ -> 5).
    tol = max(1, min(_MAX_VALUATION_GAP_DAYS, (end_d - start_d).days // 10))

    def _boundary_obs(boundary: str, d):
        row = (
            db.query(PortfolioSnapshot)
            .filter(
                PortfolioSnapshot.portfolio_id == portfolio_id,
                PortfolioSnapshot.snapshot_date <= boundary,
                PortfolioSnapshot.total_value > 0,
            )
            .order_by(PortfolioSnapshot.snapshot_date.desc())
            .first()
        )
        if row is None:
            return None
        obs_d = datetime.strptime(row.snapshot_date, "%Y-%m-%d").date()
        return obs_d if (d - obs_d).days <= tol else None

    start_obs = _boundary_obs(window_start, start_d)
    if start_obs is None:
        return None, "owner_observation_missing_at_window_start"
    if _boundary_obs(window_end, end_d) is None:
        return None, "owner_observation_missing_at_window_end"

    rows = (
        db.query(PortfolioSnapshot)
        .filter(
            PortfolioSnapshot.portfolio_id == portfolio_id,
            PortfolioSnapshot.snapshot_date > window_start,
            PortfolioSnapshot.snapshot_date <= window_end,
            PortfolioSnapshot.total_value > 0,
        )
        .order_by(PortfolioSnapshot.snapshot_date)
        .all()
    )
    if not rows:
        return None, "no_owner_observations_in_window"
    if any(r.investment_return_pct is None for r in rows):
        return None, "owner_cash_flow_adjusted_return_unavailable"
    # No silent gaps: each chained daily return must span a short interval, so a
    # missing stretch of observations is never absorbed into (or skipped by) the
    # chain. The last row must also reach the grade end within tolerance.
    prev = start_obs
    for r in rows:
        cur = datetime.strptime(r.snapshot_date, "%Y-%m-%d").date()
        if (cur - prev).days > _MAX_VALUATION_GAP_DAYS:
            return None, "owner_observation_gap_in_window"
        prev = cur
    if (end_d - prev).days > tol:
        return None, "owner_observation_missing_at_window_end"
    twr = _compute_twr([r.investment_return_pct for r in rows])
    if twr is None:
        return None, "owner_return_unavailable"
    return twr, None


def compute_opportunity_cost(db: Session, portfolio_id: int, period_days: int = 90) -> dict[str, Any]:
    """Matched-horizon Average Decision Return Difference (Phase 4.24).

    Per divergent decision: delta_pp = owner cash-flow-adjusted return over the
    recommendation grade's own [window_start, window_end] - the grade's
    return_pct. The headline is the MEAN of valid deltas (denominator =
    evaluated comparisons). Overlapping windows are never summed into a
    portfolio-level figure; the legacy `net_opportunity_cost_pct` sum is
    retired (always None) and kept only for response-shape compatibility.
    """
    from models.database import UserExecutionDecision, Workspace
    from services.analytics.human_vs_ai import _nearest_graded_horizon

    ws_row = db.query(Workspace).order_by(Workspace.id).first()
    ws = ws_row.id if ws_row else 1
    cutoff = datetime.utcnow() - timedelta(days=period_days)

    decisions = (
        db.query(UserExecutionDecision)
        .filter(
            UserExecutionDecision.workspace_id == ws,
            UserExecutionDecision.portfolio_id == portfolio_id,
            UserExecutionDecision.executed_at >= cutoff,
        )
        .order_by(UserExecutionDecision.executed_at.desc())
        .all()
    )

    rows: list[dict[str, Any]] = []
    pending_count = 0
    unavailable_count = 0
    deltas: list[float] = []
    divergence_count = 0

    for dec in decisions:
        dtype = _divergence_type(dec)
        if dtype is None:
            continue
        snap = dec.snapshot
        if snap is None:
            continue
        divergence_count += 1

        grade_row = _nearest_graded_horizon(db, snap.id, period_days)
        base = {
            "decision_id": dec.id,
            "snapshot_id": snap.id,
            "date": dec.executed_at.isoformat() + "Z" if dec.executed_at else None,
            "divergence_type": dtype,
            "override_type": dec.override_type,
            "original_symbol": dec.original_symbol,
            "replacement_symbol": dec.replacement_symbol,
        }
        empty = {
            "grade_kind": grade_row.grade_kind if grade_row else None,
            "window_start": grade_row.window_start if grade_row else None,
            "window_end": grade_row.window_end if grade_row else None,
            "counterfactual_recommendation_return_pct": None,
            "actual_return_pct": None,
            "counterfactual_delta_pct": None,
        }

        if grade_row is None or grade_row.return_pct is None:
            pending_count += 1
            rows.append({
                **base, **empty, "status": "maturing", "unavailable_reason": "no_matured_grade",
                "note": "Recommendation shadow has not matured at any horizon within this window yet.",
            })
            continue

        reason: str | None = None
        actual_ret: float | None = None
        if not grade_row.window_start or not grade_row.window_end:
            reason = "grade_window_missing"
        elif dtype != "EXPIRED" and dec.executed_at is not None and dec.executed_at.strftime("%Y-%m-%d") > grade_row.window_end:
            # The divergence happened after the grade's window closed, so that
            # window cannot price it - never substitute a different window.
            reason = "decision_after_grade_window"
        elif (
            dtype != "EXPIRED" and dec.executed_at is not None
            and (dec.executed_at.date() - datetime.strptime(grade_row.window_start, "%Y-%m-%d").date()).days
            > _MAX_DECISION_DELAY_DAYS
        ):
            # The grade window opens when the recommendation was issued. A human
            # action taken materially later would be credited with returns that
            # accrued before it existed - not evidence of that action.
            reason = "decision_delayed_after_window_start"
        else:
            actual_ret, reason = _owner_return_between(
                db, portfolio_id, grade_row.window_start, grade_row.window_end,
            )

        if reason is not None or actual_ret is None:
            unavailable_count += 1
            rows.append({
                **base, **empty, "status": "unavailable",
                "unavailable_reason": reason or "owner_return_unavailable",
                "counterfactual_recommendation_return_pct": grade_row.return_pct,
                "note": f"No valid matched comparison: {reason}.",
            })
            continue

        delta = round(actual_ret - grade_row.return_pct, 4)
        deltas.append(delta)
        rows.append({
            **base, **empty, "status": "graded", "unavailable_reason": None,
            "counterfactual_recommendation_return_pct": grade_row.return_pct,
            "actual_return_pct": actual_ret,
            "counterfactual_delta_pct": delta,
            "note": (
                "Matched-horizon decision-level comparison: your cash-flow-adjusted return "
                "over the same window as the recommendation's grade minus that grade's return, "
                "in percentage points. Prices the whole recommendation, not the symbol(s) diverged on."
            ),
        })

    rows.sort(key=lambda r: abs(r.get("counterfactual_delta_pct") or 0), reverse=True)
    evaluated = len(deltas)

    return {
        "portfolio_id": portfolio_id,
        "period_days": period_days,
        "as_of": datetime.utcnow().isoformat() + "Z",
        "status": "ok" if rows else "cold_start",
        # Phase 4.24: legacy overlapping-window sum retired; do not reuse.
        "net_opportunity_cost_pct": None,
        "mean_decision_delta_pp": round(sum(deltas) / evaluated, 4) if evaluated else None,
        "divergence_count": divergence_count,
        "evaluated_count": evaluated,
        "pending_count": pending_count,
        "unavailable_count": unavailable_count,
        "graded_count": evaluated,
        "maturing_count": pending_count,
        "rows": rows,
        "system_deferrals": _system_deferrals(db, ws, portfolio_id, cutoff),
    }
