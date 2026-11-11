"""Frozen, unselected MUJI V2 candidate preparation. No decision or scheduling authority."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from math import isfinite

VERSION = "wealth.strategic-candidates.v1"
SELECTION_VERSION = "wealth.strategy-selection.v1"
FAMILIES = frozenset({"RAISE_CASH", "DEFENSIVE_ROTATION", "GROWTH_ROTATION"})
_BUY = frozenset({"BUY", "ACCUMULATE"})
_SELL = frozenset({"SELL", "REDUCE"})


def _number(value):
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return result if isfinite(result) else None


def _evidence_catalog(holdings: list[dict], watchlist: list[dict], regime: dict | None,
                      goals: dict | None) -> dict[str, object]:
    catalog = {}
    for row in [*watchlist, *holdings]:
        symbol = row.get("symbol")
        if not symbol:
            continue
        for field in ("signal", "fa_score", "ta_score", "pe_ratio", "roe", "timing_score"):
            value = row.get(field)
            if value is not None and (not isinstance(value, (int, float)) or _number(value) is not None):
                catalog[f"symbol:{symbol}:{field}"] = value
    if isinstance(regime, dict) and regime.get("regime"):
        catalog["regime:regime"] = regime["regime"]
    for goal in (goals or {}).get("goals", []):
        for field in ("target_date", "funding_gap", "priority"):
            if goal.get(field) is not None:
                catalog[f"goal:{goal['id']}:{field}"] = goal[field]
    return catalog


def prepare_candidates(holdings: list[dict], watchlist: list[dict], cash: float,
                       challenger: dict, *, regime: dict | None = None,
                       goals: dict | None = None, source_layer: str = "CHALLENGER") -> dict:
    """Retain coherent proposals with explicit evidence status; always include current HOLD."""
    envelope = {
        "version": VERSION, "status": "PREPARED_NOT_SELECTED",
        "goal_context_version": (goals or {}).get("contract_version"), "candidates": [],
        "observed_evidence_catalog": _evidence_catalog(holdings, watchlist, regime, goals),
    }
    cash_value = _number(cash)
    hold_rows = []
    hold_errors = []
    for row in sorted(holdings, key=lambda item: str(item.get("symbol", ""))):
        symbol = row.get("symbol")
        weight = _number(row.get("weight_pct"))
        price = _number(row.get("current_price"))
        shares = _number(row.get("shares"))
        if not symbol or weight is None or price is None or price <= 0 or shares is None or shares < 0:
            hold_errors.append("CURRENT_NAV_UNAVAILABLE")
            continue
        hold_rows.append({"symbol": symbol, "action": "HOLD", "current_weight": weight,
                          "target_weight": weight, "allocation_change_percent": 0.0})
    if len({row["symbol"] for row in hold_rows}) != len(hold_rows):
        hold_errors.append("DUPLICATE_CURRENT_HOLDING")
    if cash_value is None or cash_value < 0:
        hold_errors.append("CURRENT_CASH_UNAVAILABLE")
    if not holdings and (cash_value is None or cash_value <= 0):
        hold_errors.append("CURRENT_NAV_UNAVAILABLE")
    hold_ok = not hold_errors and len(hold_rows) == len(holdings)
    envelope["candidates"].append({
        "id": "hold-current", "family": "HOLD", "source_layer": "FROZEN_PORTFOLIO",
        "proposed_allocations": hold_rows if hold_ok else [],
        "cash_intent": {"kind": "KEEP_CURRENT", "amount": cash_value},
        "observed_evidence_refs": [], "model_rationale": None,
        "risks_and_opposing_evidence": [], "missing_information": sorted(set(hold_errors)),
        "eligibility_status": "ELIGIBLE" if hold_ok else "UNVERIFIED",
        "eligibility_reasons": [] if hold_ok else sorted(set(hold_errors)),
    })

    plans = [challenger]
    for extra in (challenger.get("additional_plans") or [])[:2]:
        if isinstance(extra, dict):
            plans.append(extra)
    for plan in plans:
        _append_proposal(envelope, holdings, watchlist, hold_rows, hold_ok, regime, goals,
                         plan, source_layer)
    return envelope


def _append_proposal(envelope, holdings, watchlist, hold_rows, hold_ok, regime, goals,
                     challenger, source_layer):
    family = challenger.get("strategy_family")
    if family not in FAMILIES:
        return
    proposal = challenger.get("target_allocations")
    if not isinstance(proposal, list):
        return
    reasons = []
    missing = []
    if challenger.get("candidate_input_invalid"):
        reasons.append("INCOMPLETE_MODEL_ALLOCATION")
    held_symbols = {row.get("symbol") for row in holdings}
    symbols = [row.get("symbol") for row in proposal if isinstance(row, dict)]
    if len(symbols) != len(proposal) or len(symbols) != len(set(symbols)) or not held_symbols.issubset(symbols):
        reasons.append("INCOMPLETE_OR_DUPLICATE_ALLOCATIONS")
    known_symbols = held_symbols | {row.get("symbol") for row in watchlist}
    if any(symbol not in known_symbols for symbol in symbols):
        reasons.append("UNKNOWN_SYMBOL")
    for row in proposal:
        if not isinstance(row, dict):
            continue
        action = row.get("action")
        current = _number(row.get("current_weight"))
        target = _number(row.get("target_weight"))
        delta = _number(row.get("allocation_change_percent"))
        if action not in _BUY | _SELL | {"HOLD", "WATCH"} or any(v is None for v in (current, target, delta)):
            reasons.append("INVALID_ALLOCATION")
            continue
        if current < 0 or target < 0 or target > 100 or abs(target - current - delta) > 0.021:
            reasons.append("INVALID_WEIGHT_OR_DELTA")
        if ((action in _BUY and delta <= 0) or (action in _SELL and delta >= 0)
                or (action in {"HOLD", "WATCH"} and abs(delta) > 0.021)):
            reasons.append("ACTION_DELTA_CONFLICT")
        if action in _SELL:
            frozen = next((item for item in holdings if item.get("symbol") == row.get("symbol")), None)
            if not frozen or frozen.get("signal") != "SELL":
                missing.append(f"UNVERIFIED_SELL:{row.get('symbol')}")
            if row.get("thesis_evidence_status") == "UNVERIFIED" or row.get("decision_basis") in (
                "CONCENTRATION_ADVISORY", "SECTOR_ADVISORY"
            ):
                missing.append(f"ADVISORY_ONLY_OR_UNVERIFIED:{row.get('symbol')}")
    cash_intent = _number(challenger.get("target_cash_weight"))
    if cash_intent is None or not 0 <= cash_intent <= 100:
        reasons.append("INVALID_CASH_INTENT")
    target_weights = [_number(row.get("target_weight")) for row in proposal if isinstance(row, dict)]
    if cash_intent is not None and all(weight is not None for weight in target_weights):
        if abs(sum(target_weights) + cash_intent - 100) > 1.0:
            reasons.append("ALLOCATION_CASH_TOTAL_CONFLICT")
    actions = {row.get("action") for row in proposal if isinstance(row, dict)}
    current_weight_sum = sum(row["target_weight"] for row in hold_rows) if hold_ok else None
    current_cash_pct = 100 - current_weight_sum if current_weight_sum is not None else None
    if family == "RAISE_CASH" and (
        not actions.intersection(_SELL) or cash_intent is None or current_cash_pct is None
        or cash_intent <= current_cash_pct
    ):
        reasons.append("FAMILY_ACTION_CONFLICT")
    if family == "DEFENSIVE_ROTATION" and not (actions.intersection(_SELL) and actions.intersection(_BUY)):
        reasons.append("FAMILY_ACTION_CONFLICT")
    if family == "GROWTH_ROTATION" and not actions.intersection(_BUY):
        reasons.append("FAMILY_ACTION_CONFLICT")
    refs = challenger.get("observed_evidence_refs") or []
    if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
        reasons.append("INVALID_EVIDENCE_REFS")
        refs = []
    catalog = _evidence_catalog(holdings, watchlist, regime, goals)
    verified_refs = {ref: catalog[ref] for ref in refs if ref in catalog}
    if not verified_refs:
        missing.append("INDEPENDENT_SUPPORT_UNVERIFIED")
    if verified_refs and all(ref.endswith((":fa_score", ":ta_score", ":timing_score"))
                             for ref in verified_refs):
        missing.append("MODEL_SCORE_ONLY_SUPPORT")
    if len(verified_refs) != len(refs):
        missing.append("UNKNOWN_EVIDENCE_REF")
    # A concentration diagnostic or a bare model label never supplies independent support.
    if refs and all(ref.endswith(":signal") and verified_refs.get(ref) == "HOLD" for ref in refs):
        missing.append("INDEPENDENT_SUPPORT_UNVERIFIED")
    for row in proposal:
        if isinstance(row, dict) and row.get("action") in _BUY:
            symbol = row.get("symbol")
            if not any(ref.startswith(f"symbol:{symbol}:")
                       and not ref.endswith((":fa_score", ":ta_score", ":timing_score"))
                       for ref in verified_refs):
                missing.append(f"BUY_SUPPORT_UNVERIFIED:{symbol}")
    stable = json.dumps({"family": family, "allocations": proposal, "cash": cash_intent},
                        sort_keys=True, default=str, separators=(",", ":"))
    candidate_id = "proposal-" + sha256(stable.encode()).hexdigest()[:12]
    envelope["candidates"].append({
        "id": candidate_id, "family": family, "source_layer": source_layer,
        "proposed_allocations": deepcopy(proposal), "cash_intent": {"kind": "TARGET_WEIGHT_PCT", "value": cash_intent},
        "observed_evidence_refs": verified_refs,
        "model_rationale": challenger.get("portfolio_assessment") or challenger.get("summary"),
        "risks_and_opposing_evidence": challenger.get("disagreements") or [],
        "missing_information": sorted(set(missing)),
        "eligibility_status": "INELIGIBLE" if reasons else "UNVERIFIED" if missing else "ELIGIBLE",
        "eligibility_reasons": sorted(set(reasons + missing)),
    })


def validate_candidate_reviews(raw, envelope):
    """Bind Auditor observations to frozen candidate IDs and observed facts."""
    candidates = {c["id"]: c for c in envelope.get("candidates", [])}
    reviews = {}
    if not isinstance(raw, dict) or not isinstance(raw.get("candidate_reviews"), list):
        return {"status": "UNAVAILABLE", "reason": "AUDITOR_REVIEWS_MISSING", "reviews": {}}
    for item in raw["candidate_reviews"]:
        if (not isinstance(item, dict) or not isinstance(item.get("candidate_id"), str)
                or item.get("candidate_id") not in candidates):
            continue
        candidate_id = item["candidate_id"]
        if candidate_id in reviews:
            return {"status": "UNAVAILABLE", "reason": "DUPLICATE_AUDITOR_REVIEW", "reviews": {}}
        supporting_known = candidates[candidate_id].get("observed_evidence_refs") or {}
        opposing_known = envelope.get("observed_evidence_catalog") or {}
        supporting = item.get("supporting_refs") or []
        opposing = item.get("opposing_refs") or []
        if (not isinstance(supporting, list) or not isinstance(opposing, list)
                or any(not isinstance(ref, str) for ref in [*supporting, *opposing])
                or any(ref not in supporting_known for ref in supporting)
                or any(ref not in opposing_known for ref in opposing)):
            return {"status": "UNAVAILABLE", "reason": "UNKNOWN_AUDITOR_REFERENCE", "reviews": {}}
        reviews[candidate_id] = {
            "supporting_refs": list(dict.fromkeys(supporting)),
            "opposing_refs": list(dict.fromkeys(opposing)),
            "material_conflicts": item.get("material_conflicts") if isinstance(item.get("material_conflicts"), list) else [],
            "model_opinion": item.get("assessment") if isinstance(item.get("assessment"), str) else None,
        }
    if set(reviews) != set(candidates):
        return {"status": "UNAVAILABLE", "reason": "INCOMPLETE_AUDITOR_COVERAGE", "reviews": reviews}
    return {"status": "AVAILABLE", "reason": None, "reviews": reviews}


def decide_selection(envelope, audit, committee, *, hold_safe=True, failure_reason=None):
    """Validate qualitative Committee choice; never substitute a model score for evidence."""
    candidates = envelope.get("candidates", []) if isinstance(envelope, dict) else []
    by_id = {c.get("id"): c for c in candidates if isinstance(c, dict)}
    hold = by_id.get("hold-current")
    hold_valid = (hold is not None and hold.get("family") == "HOLD"
                  and hold.get("eligibility_status") == "ELIGIBLE" and hold_safe)
    base = {
        "version": SELECTION_VERSION, "state": "HUMAN_REVIEW_REQUIRED",
        "selected_candidate_id": None, "considered_candidate_ids": list(by_id),
        "eligible_candidate_ids": [c["id"] for c in candidates
                                   if isinstance(c, dict) and c.get("eligibility_status") == "ELIGIBLE"],
        "supporting_evidence_refs": [], "opposing_evidence_refs": [],
        "comparison_against_hold": None, "decision_rationale": None,
        "material_uncertainty": [], "reason_codes": [],
        "auditor_review_status": (audit or {}).get("status", "UNAVAILABLE"),
    }
    if len(by_id) != len(candidates) or not hold:
        base["reason_codes"] = ["INVALID_CANDIDATE_ENVELOPE"]
        return base
    if not hold_valid:
        base["reason_codes"] = ["HOLD_BASIS_OR_HARD_SAFEGUARD_UNVERIFIED"]
        return base
    if failure_reason or (audit or {}).get("status") != "AVAILABLE":
        base.update(state="SELECTED", selected_candidate_id="hold-current",
                    decision_rationale="Maintain current portfolio pending verified comparison.",
                    comparison_against_hold="No defensible action established.",
                    material_uncertainty=[failure_reason or audit.get("reason") or "AUDITOR_UNAVAILABLE"],
                    reason_codes=["CAUTIONED_HOLD"])
        return base
    if isinstance(committee, dict) and committee.get("state") == "ABSTAINED":
        base.update(state="ABSTAINED", decision_rationale=committee.get("decision_rationale"),
                    material_uncertainty=committee.get("material_uncertainty") or [],
                    reason_codes=["COMMITTEE_ABSTAINED"])
        return base
    if not isinstance(committee, dict):
        return decide_selection(envelope, audit, None, hold_safe=hold_safe,
                                failure_reason="COMMITTEE_OUTPUT_INVALID")
    selected_id = committee.get("selected_candidate_id")
    if not isinstance(selected_id, str):
        return decide_selection(envelope, audit, None, hold_safe=hold_safe,
                                failure_reason="COMMITTEE_CANDIDATE_INVALID")
    selected = by_id.get(selected_id)
    if not selected or selected.get("eligibility_status") != "ELIGIBLE":
        return decide_selection(envelope, audit, None, hold_safe=hold_safe,
                                failure_reason="COMMITTEE_CANDIDATE_INVALID")
    supporting = committee.get("supporting_evidence_refs")
    opposing = committee.get("opposing_evidence_refs")
    rationale = committee.get("decision_rationale")
    comparison = committee.get("comparison_against_hold")
    uncertainty = committee.get("material_uncertainty")
    review = audit["reviews"].get(selected_id)
    if (review is None or not isinstance(supporting, list) or not isinstance(opposing, list)
            or not isinstance(rationale, str) or not rationale.strip()
            or not isinstance(comparison, str) or not comparison.strip()
            or not isinstance(uncertainty, list)
            or any(not isinstance(ref, str) for ref in [*supporting, *opposing, *uncertainty])
            or any(ref not in review["supporting_refs"] for ref in supporting)
            or any(ref not in review["opposing_refs"] for ref in opposing)
            or not set(review["opposing_refs"]).issubset(set(opposing))
            or (selected_id != "hold-current" and not supporting)
            or (selected_id != "hold-current" and not comparison.strip())):
        return decide_selection(envelope, audit, None, hold_safe=hold_safe,
                                failure_reason="COMMITTEE_EVIDENCE_INVALID")
    unresolved = list(dict.fromkeys(
        conflict for candidate_review in audit["reviews"].values()
        for conflict in candidate_review.get("material_conflicts", [])
        if isinstance(conflict, str)
    ))
    if unresolved and selected_id != "hold-current":
        return decide_selection(envelope, audit, None, hold_safe=hold_safe,
                                failure_reason="MATERIAL_CONFLICT_UNRESOLVED")
    base.update(state="SELECTED", selected_candidate_id=selected_id,
                supporting_evidence_refs=supporting, opposing_evidence_refs=opposing,
                comparison_against_hold=comparison, decision_rationale=rationale,
                material_uncertainty=list(dict.fromkeys([*uncertainty, *unresolved])),
                reason_codes=["COMMITTEE_SELECTED"])
    return base
