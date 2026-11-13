"""Frozen, unselected MUJI V2 candidate preparation. No decision or scheduling authority."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from math import isfinite

VERSION = "wealth.strategic-candidates.v1"
SELECTION_VERSION = "wealth.strategy-selection.v1"
REVIEW_DIAGNOSTICS_VERSION = "wealth.candidate-review-diagnostics.v1"
FAMILIES = frozenset({"RAISE_CASH", "DEFENSIVE_ROTATION", "GROWTH_ROTATION"})
_BUY = frozenset({"BUY", "ACCUMULATE"})
_SELL = frozenset({"SELL", "REDUCE"})


def _number(value):
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return result if isfinite(result) else None


# Fields whose row value may be a default standing in for missing analysis
# (signal "HOLD", score 0); with provenance they enter the catalog only when observed.
_PROVENANCE_FIELDS = frozenset({"signal", "fa_score", "ta_score", "timing_score"})
_SCORE_SUFFIXES = (":fa_score", ":ta_score", ":timing_score")


def _admissible(value) -> bool:
    return value is not None and (not isinstance(value, (int, float)) or _number(value) is not None)


def _evidence(holdings: list[dict], watchlist: list[dict], regime: dict | None,
              goals: dict | None, provenance: dict | None = None):
    """Return (catalog, unobserved, as_of).

    provenance None keeps the legacy catalog (no provenance check). Otherwise a
    provenance-gated value enters the catalog only when its status is OBSERVED;
    an excluded value is recorded by reference in ``unobserved`` with its status
    (MISSING, FAILED, DISABLED, or UNRECORDED when no record exists).
    """
    catalog, unobserved, as_of = {}, {}, {}
    for row in [*watchlist, *holdings]:
        symbol = row.get("symbol")
        if not symbol:
            continue
        for field in ("signal", "fa_score", "ta_score", "pe_ratio", "roe", "timing_score"):
            value = row.get(field)
            if not _admissible(value):
                continue
            ref = f"symbol:{symbol}:{field}"
            if provenance is not None and field in _PROVENANCE_FIELDS:
                record = (provenance.get(symbol) or {}).get(field) or {}
                status = record.get("status") or "UNRECORDED"
                if status != "OBSERVED":
                    if ref not in catalog:
                        unobserved[ref] = status
                    continue
                if record.get("as_of"):
                    as_of[ref] = record["as_of"]
            catalog[ref] = value
            unobserved.pop(ref, None)
    if isinstance(regime, dict) and regime.get("regime"):
        catalog["regime:regime"] = regime["regime"]
    for goal in (goals or {}).get("goals", []):
        for field in ("target_date", "funding_gap", "priority"):
            if goal.get(field) is not None:
                catalog[f"goal:{goal['id']}:{field}"] = goal[field]
    return catalog, unobserved, as_of


def evidence_preview(holdings: list[dict], watchlist: list[dict], regime: dict | None = None,
                     goals: dict | None = None, provenance: dict | None = None) -> dict:
    """What the frozen catalog will exclude, known before the Challenger runs.

    Same inputs and rules as prepare_candidates, so ``unobserved_evidence`` here equals
    the envelope's. Prompt guidance only; it decides and verifies nothing.
    """
    preview = {"evidence_provenance_status": "NOT_SUPPLIED" if provenance is None else "SUPPLIED"}
    if provenance is not None:
        unobserved = _evidence(holdings, watchlist, regime, goals, provenance)[1]
        preview["unobserved_evidence"] = dict(sorted(unobserved.items()))
    return preview


def _evidence_catalog(holdings: list[dict], watchlist: list[dict], regime: dict | None,
                      goals: dict | None) -> dict[str, object]:
    """Legacy catalog without a provenance check."""
    return _evidence(holdings, watchlist, regime, goals)[0]


def prepare_candidates(holdings: list[dict], watchlist: list[dict], cash: float,
                       challenger: dict, *, regime: dict | None = None,
                       goals: dict | None = None, source_layer: str = "CHALLENGER",
                       provenance: dict | None = None) -> dict:
    """Retain coherent proposals with explicit evidence status; always include current HOLD.

    provenance: per-symbol evidence provenance (services/optimizer/evidence_provenance.py).
    The production Committee path always supplies it. Without it the legacy catalog
    is kept and the envelope records ``evidence_provenance_status: NOT_SUPPLIED``.
    """
    catalog, unobserved, as_of = _evidence(holdings, watchlist, regime, goals, provenance)
    envelope = {
        "version": VERSION, "status": "PREPARED_NOT_SELECTED",
        "goal_context_version": (goals or {}).get("contract_version"), "candidates": [],
        "observed_evidence_catalog": catalog,
        "evidence_provenance_status": "NOT_SUPPLIED" if provenance is None else "SUPPLIED",
    }
    if provenance is not None:
        envelope["unobserved_evidence"] = dict(sorted(unobserved.items()))
        envelope["observed_evidence_as_of"] = dict(sorted(as_of.items()))
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
    catalog = envelope["observed_evidence_catalog"]
    provenance_supplied = envelope.get("evidence_provenance_status") == "SUPPLIED"
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
            # Disclosure only; the sale rule above is unchanged.
            if provenance_supplied and f"symbol:{row.get('symbol')}:signal" not in catalog:
                missing.append(f"SIGNAL_UNOBSERVED:{row.get('symbol')}")
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
    verified_refs = {ref: catalog[ref] for ref in refs if ref in catalog}
    if not verified_refs:
        missing.append("INDEPENDENT_SUPPORT_UNVERIFIED")
    if verified_refs and all(ref.endswith(_SCORE_SUFFIXES) for ref in verified_refs):
        missing.append("MODEL_SCORE_ONLY_SUPPORT")
    if len(verified_refs) != len(refs):
        missing.append("UNKNOWN_EVIDENCE_REF")
    # A concentration diagnostic or a bare model label never supplies independent support.
    if refs and all(ref.endswith(":signal") and verified_refs.get(ref) == "HOLD" for ref in refs):
        missing.append("INDEPENDENT_SUPPORT_UNVERIFIED")
    for row in proposal:
        if isinstance(row, dict) and row.get("action") in _BUY:
            symbol = row.get("symbol")
            if provenance_supplied:
                # Direction check (catalog signals are observed here): an observed
                # SELL/REDUCE signal contradicts the buy whatever else is cited; a
                # cited signal supports only when it is BUY/ACCUMULATE; P/E and ROE
                # stay admissible (no invented valuation thresholds).
                if catalog.get(f"symbol:{symbol}:signal") in _SELL:
                    missing.append(f"BUY_CONTRADICTS_SIGNAL:{symbol}")
                supported = any(
                    _symbol_of_ref(ref) == symbol and not ref.endswith(_SCORE_SUFFIXES)
                    and (not ref.endswith(":signal") or value in _BUY)
                    for ref, value in verified_refs.items())
            else:
                supported = any(ref.startswith(f"symbol:{symbol}:") and not ref.endswith(_SCORE_SUFFIXES)
                                for ref in verified_refs)
            if not supported:
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


_REVIEW_ROW_FIELDS = ("symbol", "action", "current_weight", "target_weight",
                      "allocation_change_percent", "decision_basis")


def _symbol_of_ref(ref: str) -> str | None:
    if not ref.startswith("symbol:") or ref.count(":") < 2:
        return None
    return ref[len("symbol:"):ref.rindex(":")]


def candidate_review_view(envelope: dict) -> dict:
    """Compact, deterministic Auditor view of a frozen envelope. Prompt-only.

    Keeps every candidate's identity, actions, eligibility and cited refs, and
    every frozen fact for every symbol any candidate touches (so contradictory
    evidence travels with the supporting evidence), plus regime, goal and any
    other cited facts. Values are copied verbatim; nothing is inferred or filled
    in. Reviews are still validated against the full frozen catalog.
    """
    catalog = envelope.get("observed_evidence_catalog") or {}
    candidates, symbols, cited = [], set(), set()
    for candidate in envelope.get("candidates") or []:
        if not isinstance(candidate, dict):
            continue
        rows = []
        for row in candidate.get("proposed_allocations") or []:
            if not isinstance(row, dict):
                continue
            rows.append({key: row[key] for key in _REVIEW_ROW_FIELDS if row.get(key) is not None})
            if isinstance(row.get("symbol"), str):
                symbols.add(row["symbol"])
        refs = dict(candidate.get("observed_evidence_refs") or {})
        cited.update(refs)
        candidates.append({
            "candidate_id": candidate.get("id"), "family": candidate.get("family"),
            "eligibility_status": candidate.get("eligibility_status"),
            "eligibility_reasons": list(candidate.get("eligibility_reasons") or []),
            "missing_information": list(candidate.get("missing_information") or []),
            "cash_intent": candidate.get("cash_intent"),
            "proposed_allocations": rows, "cited_refs": refs,
        })
    relevant = {
        ref: value for ref, value in catalog.items()
        if ref in cited or ref.startswith(("regime:", "goal:")) or _symbol_of_ref(ref) in symbols
    }
    view = {
        "candidates": candidates,
        "relevant_evidence": dict(sorted(relevant.items())),
        "catalog_entry_count": len(catalog),
        "omitted_unrelated_entry_count": len(catalog) - len(relevant),
    }
    if envelope.get("evidence_provenance_status") is not None:
        view["evidence_provenance_status"] = envelope["evidence_provenance_status"]
    unobserved = envelope.get("unobserved_evidence")
    if isinstance(unobserved, dict):
        # Missing analysis for touched symbols travels with the view; it is not evidence.
        gaps = {ref: status for ref, status in unobserved.items() if _symbol_of_ref(ref) in symbols}
        view["unobserved_evidence"] = dict(sorted(gaps.items()))
        view["omitted_unrelated_unobserved_count"] = len(unobserved) - len(gaps)
    return view


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


def _ref_list(value):
    return [ref for ref in value if isinstance(ref, str)] if isinstance(value, list) else []


def candidate_review_diagnostics(raw, envelope):
    """Diagnostic-only evidence-quality findings for Auditor candidate reviews.

    Reports refs cited as both supporting and opposing, opposing refs outside the
    relevant_evidence view the Auditor was shown, and HOLD candidates whose
    contract has no cited refs and therefore cannot carry supporting evidence.
    Never rejects a review and is never read by validate_candidate_reviews,
    eligibility, the Committee gate or material-conflict handling.
    """
    candidates = [c for c in (envelope or {}).get("candidates") or [] if isinstance(c, dict)]
    view_refs = set(candidate_review_view(envelope)["relevant_evidence"]) if candidates else set()
    reviews = {}
    items = raw.get("candidate_reviews") if isinstance(raw, dict) else None
    for item in items if isinstance(items, list) else []:
        if isinstance(item, dict) and isinstance(item.get("candidate_id"), str):
            reviews.setdefault(item["candidate_id"], item)  # first review per candidate
    findings = []
    for candidate in candidates:
        candidate_id = candidate.get("id")
        review = reviews.get(candidate_id)
        supporting = set(_ref_list((review or {}).get("supporting_refs")))
        opposing = list(dict.fromkeys(_ref_list((review or {}).get("opposing_refs"))))
        if candidate.get("family") == "HOLD" and not candidate.get("observed_evidence_refs"):
            findings.append({"code": "HOLD_SUPPORT_UNREPRESENTABLE", "candidate_id": candidate_id,
                             "opposing_ref_count": len(opposing), "reviewed": review is not None})
        overlap = [ref for ref in opposing if ref in supporting]
        if overlap:
            findings.append({"code": "SUPPORT_OPPOSITION_OVERLAP", "candidate_id": candidate_id,
                             "refs": overlap})
        outside = [ref for ref in opposing if ref not in view_refs]
        if outside:
            findings.append({"code": "OPPOSING_OUTSIDE_REVIEW_VIEW", "candidate_id": candidate_id,
                             "refs": outside})
    return {"version": REVIEW_DIAGNOSTICS_VERSION, "diagnostic_only": True, "findings": findings}


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
    audit_unavailable = (audit or {}).get("status") != "AVAILABLE"
    if failure_reason or audit_unavailable:
        # Record every concurrent cause (e.g. NO_ELIGIBLE_ACTION and
        # AUDITOR_REVIEWS_MISSING), deterministically ordered and deduplicated.
        causes = [failure_reason] if failure_reason else []
        if audit_unavailable:
            causes.append((audit or {}).get("reason") or "AUDITOR_UNAVAILABLE")
        base.update(state="SELECTED", selected_candidate_id="hold-current",
                    decision_rationale="Maintain current portfolio pending verified comparison.",
                    comparison_against_hold="No defensible action established.",
                    material_uncertainty=list(dict.fromkeys(causes)),
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
    # Non-binding (Slice 4.6C, option B2): Auditor conflict text is model-authored
    # and unverified, so it never vetoes a selection. Every verifiable
    # contradiction is already enforced by eligibility and hard safeguards before
    # the Committee runs. Only the selected candidate's own non-blank conflicts
    # are recorded; other reviews' conflicts stay in candidate_audit only.
    own_conflicts = list(dict.fromkeys(
        conflict.strip() for conflict in review.get("material_conflicts") or []
        if isinstance(conflict, str) and conflict.strip()
    ))
    reason_codes = ["COMMITTEE_SELECTED"]
    if own_conflicts and selected_id != "hold-current":
        reason_codes.append("AUDITOR_CONFLICT_UNVERIFIED")
    base.update(state="SELECTED", selected_candidate_id=selected_id,
                supporting_evidence_refs=supporting, opposing_evidence_refs=opposing,
                comparison_against_hold=comparison, decision_rationale=rationale,
                material_uncertainty=list(dict.fromkeys([*uncertainty, *own_conflicts])),
                reason_codes=reason_codes)
    return base
