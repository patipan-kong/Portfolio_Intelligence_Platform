"""Versioned, read-only projection of execution facts for model/run evidence.

No symbol taxonomy, price lookup, policy evaluation or allocation decisions.
OptimizerHistory stores this envelope in execution_context; snapshots refer
to that history. Historical readers must use the captured envelope only.
"""
from __future__ import annotations

import hashlib
import json

from services import registry_service

VERSION = "wealth.optimizer-instrument-context.v1"


def _value(value):
    return getattr(value, "value", value)


def build_instrument_context(db, held_symbols, facts_by_symbol, execution_context):
    positions = []
    per_symbol = (execution_context or {}).get("per_symbol", {})
    for symbol in dict.fromkeys(held_symbols):
        facts = facts_by_symbol.get(symbol)
        status = _value(getattr(facts, "resolution_status", None)) or "UNKNOWN"
        form = _value(getattr(facts, "instrument_form", None)) or "UNKNOWN"
        verified = status in ("RESOLVED", "NOT_TRADABLE") and form != "UNKNOWN"
        unresolved = [] if verified else [getattr(facts, "reason", None) or "Canonical classification unavailable"]
        underlying = None
        underlying_id = getattr(facts, "underlying_asset_id", None)
        if verified and form == "DEPOSITARY_RECEIPT":
            try:
                asset = registry_service.get_asset(db, underlying_id) if underlying_id is not None else None
            except Exception:
                asset = None
            if asset is None:
                unresolved.append("Canonical underlying identity unavailable")
            else:
                underlying = {"asset_id": int(asset.id), "canonical_symbol": asset.canonical_symbol,
                              "display_symbol": asset.display_symbol, "exchange": asset.exchange,
                              "currency": asset.currency, "asset_type": asset.asset_type}
        meta = per_symbol.get(symbol, {})
        provenance = [{"fact": p.fact, "source_field": p.source_field,
                       "source_value": p.source_value} for p in getattr(facts, "provenance", ())]
        positions.append({
            "held_symbol": symbol, "asset_id": getattr(facts, "asset_id", None),
            "instrument_form": form, "resolution_status": status,
            "classification_verified": verified, "classification_source": "ExecutionInstrumentFacts",
            "classification_provenance": provenance, "underlying": underlying,
            "local_quote_currency": getattr(facts, "currency", None),
            "execution": {k: meta.get(k) for k in ("asset_type", "execution_risk", "position_cap_pct",
                "classification_source", "classification_warning", "combined_score_penalty", "slippage_cost_est_pct")},
            "unresolved_evidence": unresolved,
        })
    envelope = {"version": VERSION, "positions": positions,
        "rules": {
            "execution_position_caps": {"enforcement": "DETERMINISTIC_TARGET_CLAMP",
                "enforcement_scope": "PRIMARY_LAYERED_FINALIZATION_ONLY",
                "limits": [{"symbol": symbol, "position_cap_pct": meta["position_cap_pct"],
                            "classification_source": meta.get("classification_source"),
                            "resolution_status": meta.get("resolution_status")}
                           for symbol, meta in per_symbol.items() if meta.get("position_cap_pct") is not None],
                "actions": ["BUY", "ACCUMULATE"], "scope": "Per-symbol caps supplied by execution metadata; no automatic sell of existing holdings"},
            "dr_basket_guidance": {"threshold_pct": (execution_context or {}).get("dr_portfolio_cap", 40.0),
                "enforcement": "PROMPT_ONLY_ADVISORY", "deterministic_breach_evaluated": False},
            "general_portfolio_policy": {"source": "Separate active policy context", "scope": "Existing policy limits and calculations unchanged"},
        }}
    prompt = (
        "[CANONICAL INSTRUMENT CONTEXT]\n" + json.dumps(envelope, sort_keys=True, separators=(",", ":")) + "\n"
        "Use verified canonical facts; ticker patterns and generic EQUITY asset type do not prove DR absence. "
        "Unresolved evidence is not verified classification. Underlying USD currency/prices must not replace local DR quote currency/prices.\n"
        "Instrument form alone is not a BUY/SELL signal; preserve independent investment reasoning. "
        "In primary layered finalization, execution position caps clamp BUY/ACCUMULATE targets only; "
        "the single-shot fallback has no deterministic execution-cap clamp. The 40% DR basket guidance is prompt-only advisory, "
        "not an enforced deterministic policy rule or evidence of an actual breach. "
        "Distinguish calculated policy breaches, OWNER_INTENT_REVIEW disagreements and advisory hypotheses; "
        "do not label ticker-based or basket-guidance hypotheses as verified policy breaches.\n"
    )
    return {**envelope, "prompt_block": prompt,
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()}
