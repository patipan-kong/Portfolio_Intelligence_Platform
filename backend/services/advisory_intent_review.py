"""Advisory Integration V1 (Slice 1): deterministic Intent review + frozen envelope.

Two truths are kept apart for every referenced positive held position:

* the FINAL review — the quantity the final plan proposes today (after the
  noise filter and drift deferral, before scheduling), and
* RETAINED proposal reviews — non-abandoned MATERIAL proposals the run
  produced and then replaced, suppressed or deferred (for example a forced
  SELL that the legacy lock suppressed). L1 strategist legs superseded by the
  accepted allocation are intermediate reasoning: listed as non-material
  provenance, never reviewed as a conflict.

A CONFLICT is evidence of disagreement for the owner to decide. It is not a
governance violation, not a policy penalty, and it never changes, removes or
redistributes any allocation. Historical reads return the frozen envelope and
never recompute it from current Intent, thresholds or policy.
"""
from __future__ import annotations

import copy
import logging

from services.advisory_intent_context import (
    ABANDONED,
    CONTEXT_UNAVAILABLE,
    EFFECT_DEFER,
    EFFECT_SCALE,
    EFFECT_SUPPRESS,
    PRECISION_RULES,
    SHARE_QUANTUM,
    SOFT_LAYERS,
    HARD_LAYERS,
    BASIS_COMMON_NAV,
    INTERMEDIATE_REASONING,
    MIXED_BASIS_SCOPE,
    SEMANTICS_LEGACY_SYSTEM,
    STAGE_EXECUTION_SCHEDULING,
    STAGE_NOISE_FILTER,
    STAGE_STABILIZATION,
    AdvisoryIntentRun,
    HeldPosition,
    canonical_digest,
    dec_str,
    is_confirmed,
    project_direction_only,
    project_quantity,
    to_decimal,
)
from services.advisory_intent_flag import (
    ENABLED_SCOPE, FLAG_ENV, PROJECTION_VERSION, REVIEW_CONTRACT_VERSION,
)
from services.investor_intent import (
    CONFLICT,
    CONSISTENT,
    DECREASE,
    INCREASE,
    INTENT_CONTRACT_VERSION,
    NO_CHANGE,
    SOURCE_SYSTEM_RULE,
    UNRESOLVED,
    evaluate_proposal,
    quantity_direction,
)

_log = logging.getLogger(__name__)

ENVELOPE_KEY = "advisory_intent_review"
STATUS_KEY = "advisory_intent_review_status"
READ_CAPTURED = "CAPTURED"
READ_NOT_CAPTURED = "NOT_CAPTURED"
READ_EVIDENCE_INVALID = "EVIDENCE_INVALID"

TOLERANCE_AMBIGUITY = "QUANTITY_DIRECTION_TOLERANCE_AMBIGUITY"
_RESTRICTION = {INCREASE: "INCREASE_PROHIBITED_BY_OWNER", DECREASE: "DECREASE_PROHIBITED_BY_OWNER"}
_REQUIRED_SECTIONS = ("identity", "reference", "valuation", "prompt_use", "positions",
                      "coverage", "review", "integrity")


# ── Response-projection observers (enabled runs only) ─────────────────────────

def _row_basis(row: dict) -> dict:
    return {"action": (row.get("action") or "HOLD").upper(), "target_weight": row.get("target_weight"),
            "current_weight": row.get("current_weight")}


def observe_stabilization(run: AdvisoryIntentRun, result: dict) -> None:
    """Stabilization tags drift-tolerant rows; that deferral is recorded, not applied."""
    stab = result.get("stabilization") or {}
    run.run_disposition = {
        "stabilization_status": stab.get("status"),
        "original_optimizer_status": stab.get("original_optimizer_status"),
        "stabilization_reason": stab.get("reason"),
    }
    for row in result.get("target_allocations") or []:
        if row.get("within_drift_tolerance"):
            run.observe(row.get("symbol", ""), stage=STAGE_STABILIZATION, source=SOURCE_SYSTEM_RULE,
                        effect=EFFECT_DEFER, reason_code="STABILIZATION_DRIFT_TOLERANCE",
                        reason_text="Within the stabilization drift tolerance band; not traded today.",
                        before=_row_basis(row), after=_row_basis(row))


def apply_response_views(response: dict, run: AdvisoryIntentRun | None, log) -> None:
    """Noise filter, action summary and execution optimization — once, on the response view.

    Shared by the legacy path (run is None: identical behaviour to before) and
    the enabled path, where it runs on a separate copy before persistence and
    the economic allocations are left untouched.
    """
    before = {row.get("symbol"): (dict(row)) for row in response.get("target_allocations") or []} if run else {}
    try:
        from services.noise_filter import DRIFT_THRESHOLD_PCT, apply_noise_filter
        apply_noise_filter(response)
        if run is not None:
            for row in response.get("target_allocations") or []:
                prior = before.get(row.get("symbol"))
                if prior is None or not row.get("noise_suppressed") or prior.get("noise_suppressed"):
                    continue
                drift = abs(prior.get("allocation_change_percent") or 0)
                run.observe(
                    row.get("symbol", ""), stage=STAGE_NOISE_FILTER, source=SOURCE_SYSTEM_RULE,
                    effect=EFFECT_SUPPRESS,
                    reason_code=("NOISE_DRIFT_BELOW_THRESHOLD" if drift < DRIFT_THRESHOLD_PCT
                                 else "NOISE_TRADE_VALUE_BELOW_MINIMUM"),
                    reason_text=str(row.get("noise_reason") or ""),
                    before=_row_basis(prior), after=_row_basis(row),
                )
    except Exception as _nf_exc:
        log.warning("analyze_optimizer: noise filter failed — continuing: %s", _nf_exc)
        if run is not None:
            run.ledger.capture_errors.append("NOISE_FILTER_FAILED")

    try:
        from services.optimizer_action_summary import build_action_summary
        response["action_summary"] = build_action_summary(response.get("target_allocations", []))
    except Exception as _as_exc:
        log.warning("analyze_optimizer: action_summary failed — continuing: %s", _as_exc)

    try:
        from services.optimizer.execution_optimizer import optimize_execution
        _violations = (response.get("active_policy") or {}).get("violations", [])
        response["execution_optimization"] = optimize_execution(
            response.get("action_summary", {}),
            response.get("target_allocations", []),
            cash_available=float(response.get("cash_balance") or 0.0),
            violations=_violations,
        ).model_dump()
    except Exception as _eo_exc:
        log.warning("analyze_optimizer: execution_optimization failed — continuing: %s", _eo_exc)
        if run is not None:
            run.ledger.capture_errors.append("EXECUTION_OPTIMIZATION_FAILED")
        return

    if run is not None:
        for trade in (response.get("execution_optimization") or {}).get("trades") or []:
            symbol = trade.get("symbol", "")
            scheduled = {key: trade.get(key) for key in (
                "action", "execution_state", "execution_role", "necessity", "reason",
                "full_recommended_amount", "executed_amount")}
            state = trade.get("execution_state")
            if state in ("DEFERRED", "SCALED"):
                run.observe(symbol, stage=STAGE_EXECUTION_SCHEDULING, source=SOURCE_SYSTEM_RULE,
                            effect=EFFECT_DEFER if state == "DEFERRED" else EFFECT_SCALE,
                            reason_code=("EXECUTION_NOT_NEEDED_TODAY" if state == "DEFERRED"
                                         else "EXECUTION_FUNDING_SCALED"),
                            reason_text=str(trade.get("note") or ""), scheduled=scheduled)
            elif symbol in run.by_symbol:
                run.ledger.scheduled[symbol] = scheduled


# ── Review ────────────────────────────────────────────────────────────────────

def _review(position: HeldPosition, projection: dict, *, source: str, reason_code: str) -> dict:
    """One proposal against the frozen Intent: CONSISTENT, CONFLICT or UNRESOLVED."""
    reasons: list[str] = []
    if not is_confirmed(position):
        reasons.append(position.applicability)
    if not projection["resolved"]:
        reasons.extend(projection["reasons"] or ["PROJECTION_UNRESOLVED"])
    elif projection["proposed_shares"] is not None:
        accounting = projection["direction"]
        kernel = quantity_direction(float(position.shares), float(to_decimal(projection["proposed_shares"])))
        if kernel != accounting:
            reasons.append(TOLERANCE_AMBIGUITY)
    out = {"outcome": UNRESOLVED, "direction": projection.get("direction"), "restriction": None,
           "conflict_kind": None, "reasons": sorted(set(reasons))}
    if reasons:
        return out
    intent = position.intent
    if projection["kind"] == "DIRECTION_ONLY":
        restricted = ((projection["direction"] == INCREASE and intent.increase_prohibited)
                      or (projection["direction"] == DECREASE and intent.decrease_prohibited))
        out.update(outcome=CONFLICT if restricted else CONSISTENT,
                   restriction=_RESTRICTION[projection["direction"]] if restricted else None,
                   reasons=["DIRECTION_ONLY_PROPOSAL"])
        return out
    kernel_result = evaluate_proposal(
        intent, float(position.shares), float(to_decimal(projection["proposed_shares"])),
        source=source, reason=reason_code,
    )
    out.update(outcome=kernel_result["outcome"], direction=kernel_result["direction"],
               restriction=kernel_result["owner_restriction"], conflict_kind=kernel_result["conflict_kind"],
               reasons=list(kernel_result["reasons"]))
    return out


def _rows(result: dict) -> tuple[dict, set]:
    rows, dupes = {}, set()
    for row in result.get("target_allocations") or []:
        symbol = row.get("symbol")
        if symbol in rows:
            dupes.add(symbol)
        rows[symbol] = row
    return rows, dupes


def _unresolved_projection(position: HeldPosition, reason: str) -> dict:
    projection = project_direction_only(position, "")
    projection.update(kind=None, resolved=False, reasons=[reason], direction=None)
    return projection


def _scheduled_view(run: AdvisoryIntentRun, position: HeldPosition) -> dict | None:
    scheduled = run.ledger.scheduled.get(position.symbol)
    if scheduled is None:
        return None
    view = dict(scheduled)
    price = run.basis.quotes[position.symbol].price if position.symbol in run.basis.quotes else None
    executed = to_decimal(scheduled.get("executed_amount"))
    if run.basis.resolved and price and executed is not None:
        delta = executed / price
        sign = -1 if str(scheduled.get("action", "")).upper() in ("SELL", "REDUCE") else 1
        view["scheduled_delta_shares_raw"] = dec_str(sign * delta)
        view["scheduled_proposed_shares"] = dec_str((position.shares + sign * delta).quantize(SHARE_QUANTUM))
    view["note"] = "Scheduling only: the economic proposal above is unchanged."
    return view


def _review_position(run: AdvisoryIntentRun, position: HeldPosition, econ_rows, econ_dupes,
                     resp_rows, resp_dupes) -> dict:
    symbol = position.symbol
    ledger = run.ledger
    econ_row, resp_row = econ_rows.get(symbol), resp_rows.get(symbol)

    if symbol in econ_dupes or symbol in resp_dupes:
        economic = final = _unresolved_projection(position, "DUPLICATE_ALLOCATION")
    elif econ_row is None or resp_row is None:
        economic = final = _unresolved_projection(position, "MISSING_ALLOCATION")
    else:
        economic = project_quantity(position, run.basis, econ_row.get("action"), econ_row.get("target_weight"))
        if resp_row.get("noise_suppressed") or resp_row.get("within_drift_tolerance"):
            final = project_quantity(position, run.basis, "HOLD", resp_row.get("current_weight"))
        else:
            final = project_quantity(position, run.basis, resp_row.get("action"), resp_row.get("target_weight"))

    active = ledger.active(symbol)
    deferred = bool(resp_row and resp_row.get("within_drift_tolerance") and not resp_row.get("noise_suppressed"))
    final["basis_evidence"] = (_basis_evidence(run, STAGE_STABILIZATION, SEMANTICS_LEGACY_SYSTEM) if deferred
                               else _basis_evidence(run, active.target_stage, active.target_semantics) if active
                               else _basis_evidence(run, None, None))
    final_source = (SOURCE_SYSTEM_RULE if deferred or active is None else active.source)
    final_review = _review(position, final, source=final_source,
                           reason_code=(active.reason_code if active and not deferred else "FINAL_PLAN"))
    if ledger.capture_errors:
        final_review.update(outcome=UNRESOLVED, restriction=None, conflict_kind=None,
                            reasons=sorted(set(final_review["reasons"]) | {"PROVENANCE_CAPTURE_FAILED"}))
    elif active is None and econ_row is not None and final_review["outcome"] != UNRESOLVED:
        final_review.update(outcome=UNRESOLVED, restriction=None, conflict_kind=None,
                            reasons=["PROVENANCE_MISSING"])

    retained, non_material = [], []
    for proposal in ledger.proposals(symbol):
        if proposal.disposition == ABANDONED:
            continue
        if proposal is active and not deferred:
            continue  # this proposal IS the final plan
        if proposal.materiality == INTERMEDIATE_REASONING:
            # Superseded L1 reasoning: audit provenance only — no review, no
            # conflict count, no owner decision, not an owner-facing suppression.
            non_material.append({**proposal.as_dict(),
                                 "excluded_from_review": "SUPERSEDED_INTERMEDIATE_REASONING"})
            continue
        projection = (project_direction_only(position, proposal.action) if proposal.direction_only
                      else project_quantity(position, run.basis, proposal.action, proposal.target_weight))
        projection["basis_evidence"] = _basis_evidence(run, proposal.target_stage, proposal.target_semantics)
        if projection["resolved"] and final["resolved"] and projection["direction"] == final["direction"]:
            continue  # same direction as the final plan: same review, nothing retained to show
        review = _review(position, projection, source=proposal.source, reason_code=proposal.reason_code)
        retained.append({**proposal.as_dict(),
                         "disposition": "DEFERRED" if proposal is active and deferred else proposal.disposition,
                         "projection": projection, "review": review})

    outcomes = [final_review["outcome"]] + [r["review"]["outcome"] for r in retained]
    status = (CONFLICT if CONFLICT in outcomes
              else UNRESOLVED if UNRESOLVED in outcomes else CONSISTENT)
    material = any(r["disposition"] in ("REPLACED", "SUPPRESSED", "DEFERRED") for r in retained)
    p = position
    return {
        "symbol": symbol,
        "referenced_shares": dec_str(p.shares),
        "holding_started_at": p.holding_started_at,
        "legacy_allow_swap": p.legacy_allow_swap,
        "applicability": p.applicability,
        "intent": ({"intent_id": p.intent.intent_id, "revision": p.intent.revision,
                    "confirmed_at": p.confirmed_at} if p.intent else None),
        "historical_intent": p.historical_intent,
        "hard_restrictions": ({"increase_prohibited": p.intent.increase_prohibited,
                               "decrease_prohibited": p.intent.decrease_prohibited} if p.intent else None),
        "soft_preference": p.intent.soft_preference if p.intent else None,
        "proposal": {"economic_candidate": economic, "final_effective": final,
                     "scheduled": _scheduled_view(run, position)},
        "provenance": [t for t in ledger.transitions if t["symbol"] == symbol],
        "review": {"final": final_review, "retained": retained, "non_material_provenance": non_material,
                   "status": status,
                   "requires_owner_decision": CONFLICT in outcomes,
                   "unresolved_reasons": sorted({reason for r in [final_review] + [x["review"] for x in retained]
                                                 if r["outcome"] == UNRESOLVED for reason in r["reasons"]})},
        "display": {
            "final_disposition": _final_disposition(resp_row, final),
            "noise_reason": resp_row.get("noise_reason") if resp_row else None,
            "material_change": material,
            "show": status != CONSISTENT or material,
        },
    }


def _basis_evidence(run: AdvisoryIntentRun, target_stage: str | None, target_semantics: str | None) -> dict:
    """Where a projected target came from versus the basis it is projected on.

    A legacy policy/system-rule target is projected onto the frozen common NAV
    for review; that does not mean the rule itself computed on that basis.
    """
    return {"projection_basis": BASIS_COMMON_NAV if run.basis.resolved else None,
            "target_origin_stage": target_stage,
            "target_origin_semantics": target_semantics,
            "row_current_weight_basis": run.ledger.row_current_weight_basis}


def _final_disposition(row: dict | None, final: dict) -> str:
    if row is None:
        return "NO_ALLOCATION"
    if row.get("noise_suppressed"):
        return "NOISE_SUPPRESSED"
    if row.get("within_drift_tolerance"):
        return "DEFERRED_WITHIN_DRIFT_TOLERANCE"
    if final.get("direction") == NO_CHANGE:
        return "UNCHANGED"
    return "CHANGE_PROPOSED" if final.get("direction") else "UNRESOLVED"


def _fingerprint(run: AdvisoryIntentRun) -> str:
    return canonical_digest({
        "portfolio_id": run.portfolio_id,
        "holdings": [[p.symbol, dec_str(p.shares), p.holding_started_at, p.legacy_allow_swap]
                     for p in run.positions],
        "cash": dec_str(to_decimal(run.cash_balance)),
    })


def build_review_envelope(run: AdvisoryIntentRun, economic: dict, response: dict) -> dict:
    """Construct and freeze the review envelope for one enabled run."""
    econ_rows, econ_dupes = _rows(economic)
    resp_rows, resp_dupes = _rows(response)
    positions = [_review_position(run, p, econ_rows, econ_dupes, resp_rows, resp_dupes)
                 for p in run.positions]

    final_conflicts = sorted(p["symbol"] for p in positions if p["review"]["final"]["outcome"] == CONFLICT)
    retained_conflicts = sorted(p["symbol"] for p in positions
                                if any(r["review"]["outcome"] == CONFLICT for r in p["review"]["retained"]))
    conflicts = sorted(set(final_conflicts) | set(retained_conflicts))
    unresolved = sorted(p["symbol"] for p in positions if p["review"]["final"]["outcome"] == UNRESOLVED)
    any_unresolved = any(p["review"]["status"] == UNRESOLVED for p in positions) or bool(unresolved)
    basis = run.basis
    envelope = {
        "contract_version": REVIEW_CONTRACT_VERSION,
        "projection_version": PROJECTION_VERSION,
        "intent_contract_version": INTENT_CONTRACT_VERSION,
        "identity": {"review_id": run.review_id, "created_at": run.created_at, "mode": "ENABLED",
                     "feature_flag": FLAG_ENV, "workspace_id": run.workspace_id,
                     "portfolio_id": run.portfolio_id, "enabled_scope": ENABLED_SCOPE,
                     "context_error": run.context_error},
        "reference": {"holdings_fingerprint": _fingerprint(run),
                      "holdings": [{"symbol": p.symbol, "shares": dec_str(p.shares),
                                    "holding_started_at": p.holding_started_at,
                                    "legacy_allow_swap": p.legacy_allow_swap} for p in run.positions],
                      "referenced_cash": dec_str(to_decimal(run.cash_balance)),
                      "anomalies": run.anomalies},
        "valuation": {"status": basis.status, "reasons": list(basis.reasons), "unit": basis.unit,
                      "cash": dec_str(basis.cash), "equity": dec_str(basis.equity), "nav": dec_str(basis.nav),
                      "denominator": "NAV = sum(referenced shares x frozen held quote) + referenced cash",
                      "quotes": [{"symbol": q.symbol, "price": dec_str(q.price), "status": q.status,
                                  "last_updated": q.last_updated, "currency": q.currency, "source": q.source}
                                 for q in sorted(basis.quotes.values(), key=lambda q: q.symbol)],
                      "precision": PRECISION_RULES,
                      "row_current_weight_basis": run.ledger.row_current_weight_basis,
                      "basis_boundary": copy.deepcopy(MIXED_BASIS_SCOPE)},
        "prompt_use": {"frozen_context": run.frozen_context_view(),
                       "intended_layers": {"hard": list(HARD_LAYERS), "soft": list(SOFT_LAYERS)},
                       "path": list(run.prompt_path)},
        "positions": positions,
        "provenance": {"proposals": run.ledger.proposals_view(),
                       "abandoned_transition_count": sum(
                           1 for t in run.ledger.transitions
                           if any(p.proposal_id == t["proposal_id"] and p.disposition == ABANDONED
                                  for p in run.ledger.proposals(t["symbol"]))),
                       "capture_errors": list(run.ledger.capture_errors)},
        "display": dict(run.run_disposition),
        "coverage": {"referenced_positive_held_count": len(positions),
                     "checked_count": len(positions),
                     "resolved_count": len(positions) - len(unresolved),
                     "unresolved_positions": unresolved,
                     "conflict_positions": conflicts,
                     "final_conflict_positions": final_conflicts,
                     "retained_conflict_positions": retained_conflicts,
                     "all_resolved_and_consistent": bool(positions) and not conflicts and not any_unresolved},
        "review": {"result": CONFLICT if conflicts else UNRESOLVED if any_unresolved or not positions else CONSISTENT,
                   "requires_owner_decision": bool(conflicts),
                   "unresolved_reasons": {p["symbol"]: p["review"]["unresolved_reasons"]
                                          for p in positions if p["review"]["unresolved_reasons"]},
                   "not_a_governance_violation": True,
                   "allocations_changed_by_review": False},
    }
    envelope["integrity"] = {"algorithm": "sha256", "canonicalization": "json-sorted-keys-compact",
                             "digest": canonical_digest(envelope)}
    return envelope


# ── Historical read ───────────────────────────────────────────────────────────

def read_frozen_review(payload: dict) -> tuple[str, dict | None]:
    """(status, envelope) for a stored result. Never recomputes from current state."""
    envelope = payload.get(ENVELOPE_KEY)
    if envelope is None:
        return READ_NOT_CAPTURED, None
    try:
        if not isinstance(envelope, dict) or envelope.get("contract_version") != REVIEW_CONTRACT_VERSION:
            return READ_EVIDENCE_INVALID, None
        if any(section not in envelope for section in _REQUIRED_SECTIONS):
            return READ_EVIDENCE_INVALID, None
        body = {k: v for k, v in envelope.items() if k != "integrity"}
        if envelope["integrity"].get("digest") != canonical_digest(body):
            return READ_EVIDENCE_INVALID, None
    except Exception:
        return READ_EVIDENCE_INVALID, None
    return READ_CAPTURED, copy.deepcopy(envelope)


def frozen_review_read(db, workspace_id: int, portfolio_id: int, payload: dict) -> dict:
    """Read-side fields for a stored optimizer result (history / snapshot reads).

    The frozen envelope is returned as captured. Current intent is consulted
    only to list positions whose intent changed since the run; it never
    rewrites the frozen review.
    """
    status, envelope = read_frozen_review(payload)
    fields = {ENVELOPE_KEY: envelope, STATUS_KEY: status}
    if envelope is not None:
        from services.investor_intent_store import current_intent_revisions
        symbols = [p["symbol"] for p in envelope.get("positions", [])]
        fields["advisory_intent_changes_since_run"] = intent_changes_since_run(
            envelope, current_intent_revisions(db, workspace_id, portfolio_id, symbols))
    return fields


def intent_changes_since_run(envelope: dict, current_revisions: dict[str, int]) -> list[dict]:
    """Display-only: covered positions whose stored intent revision moved since the run."""
    changes = []
    for position in envelope.get("positions", []):
        run_revision = (position.get("intent") or {}).get("revision") \
            or (position.get("historical_intent") or {}).get("revision")
        current = current_revisions.get(position["symbol"])
        if current != run_revision:
            changes.append({"symbol": position["symbol"], "run_intent_revision": run_revision,
                            "current_intent_revision": current})
    return changes


__all__ = [
    "CONTEXT_UNAVAILABLE", "ENVELOPE_KEY", "STATUS_KEY", "READ_CAPTURED", "READ_NOT_CAPTURED",
    "READ_EVIDENCE_INVALID", "apply_response_views", "build_review_envelope",
    "intent_changes_since_run", "observe_stabilization", "read_frozen_review",
]
