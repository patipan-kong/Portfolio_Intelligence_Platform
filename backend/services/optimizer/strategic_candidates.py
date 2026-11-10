"""Frozen, unselected MUJI V2 candidate preparation. No decision or scheduling authority."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from math import isfinite

VERSION = "wealth.strategic-candidates.v1"
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

    family = challenger.get("strategy_family")
    if family not in FAMILIES:
        return envelope
    proposal = challenger.get("target_allocations")
    if not isinstance(proposal, list):
        return envelope
    reasons = []
    missing = []
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
    if len(verified_refs) != len(refs):
        missing.append("UNKNOWN_EVIDENCE_REF")
    # A concentration diagnostic or a bare model label never supplies independent support.
    if refs and all(ref.endswith(":signal") and verified_refs.get(ref) == "HOLD" for ref in refs):
        missing.append("INDEPENDENT_SUPPORT_UNVERIFIED")
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
    return envelope
