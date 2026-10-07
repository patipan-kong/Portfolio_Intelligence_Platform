"""Offline adapters for already-captured facts, never a fetch/cache facade.

Canonical timing/legacy pure definitions are loaded from their source AST to
avoid importing data_fetcher (provider/session construction) or optimizer AI
dependencies. No copied scoring formula and no executable top-level source code.
Source digests bind the experiment to the implementation actually reused.
"""
from __future__ import annotations

import ast
import hashlib
import io
import importlib.metadata
import json
from dataclasses import asdict
from math import isfinite
from pathlib import Path

from services.candidate_discovery import (
    DiscoveryInput, Evidence, Holding, Instrument, PortfolioOverlayInput,
    discover, portfolio_overlay,
)

BACKEND = Path(__file__).resolve().parents[1]
TIMING_SOURCE = BACKEND / "services/timing_intelligence.py"
LEGACY_SOURCE = BACKEND / "agents/optimizer.py"
FA_SOURCE = BACKEND / "agents/fundamental.py"


def source_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _definitions(path: Path, names: set[str], namespace: dict) -> dict:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    nodes = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names]
    if {node.name for node in nodes} != names:
        raise ValueError(f"canonical definitions changed: {path.name}")
    # Future annotations are needed for the TypedDict/Pydantic-style source.
    module = ast.Module(body=[ast.ImportFrom(module="__future__",
        names=[ast.alias(name="annotations")], level=0), *nodes], type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), str(path), "exec"), namespace)
    return namespace


def _timing_functions() -> dict:
    import pandas as pd
    import pandas_ta as ta
    from pydantic import BaseModel
    return _definitions(TIMING_SOURCE, {
        "StockTimingResult", "_trend_score", "_momentum_score", "_relative_strength_score",
        "_volume_score", "_classify_momentum", "_timing_category", "_execution_priority",
        "_generate_reasons", "compute_timing_score", "_extract_indicators"},
        {"pd": pd, "ta": ta, "BaseModel": BaseModel, "__name__": __name__})


def _finite(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value)


def _payload(row: dict | None, key: str) -> dict:
    value = (row or {}).get(key)
    if value is None:
        return {}
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict):
        raise ValueError(f"expected object in captured {key}")
    return value


def _cache_limits(row: dict | None, as_of: str) -> tuple[str, ...]:
    limits = ["cache_timestamp_is_not_observation_timestamp",
              "discovery_freshness_threshold_not_established"]
    if row and row.get("expires_at") and row["expires_at"] < as_of:
        limits.append("cache_expired_snapshot_diagnostic_only")
    return tuple(limits)


def _history(row: dict | None):
    import pandas as pd
    payload = _payload(row, "payload_json")
    if "json_split" not in payload:
        return None
    # Identical serialization boundary to data_fetcher._payload_to_df.
    frame = pd.read_json(io.StringIO(payload["json_split"]), orient="split")
    frame.index = pd.to_datetime(frame.index, utc=True)
    if not frame.index.is_monotonic_increasing or frame.index.has_duplicates:
        raise ValueError("history index must be unique and ascending")
    return frame


def adapt_capture(capture: dict) -> tuple[DiscoveryInput, tuple[PortfolioOverlayInput, ...]]:
    """Use saved agent FA and canonical timing over saved histories only.

    Complete scoring inputs are required for ranking; producer defaults remain
    visible as raw diagnostic values but cannot masquerade as observed evidence.
    Cache expiry is a limitation, not an invented opportunity-validity threshold.
    """
    if capture.get("capture_version") != "wealth.shadow-capture.v1":
        raise ValueError("unsupported capture version")
    for package, version in capture.get("runtime_versions", {}).items():
        if importlib.metadata.version(package) != version:
            raise ValueError(f"dependency changed since capture: {package}")
    expected = capture["source_digests"]
    for name, path in (("fundamental", FA_SOURCE), ("timing", TIMING_SOURCE),
                       ("legacy", LEGACY_SOURCE)):
        if expected[name] != source_digest(path):
            raise ValueError(f"source changed since capture: {name}")
    functions = _timing_functions()
    market = {(r["symbol"], r["cache_type"]): r for r in capture["market_cache"]}
    agents = {(r["symbol"], r["agent"]): r for r in capture["agent_cache"]}
    assets = {r["id"]: r for r in capture["assets"]}
    benchmark_row = market.get(("SPY", "history:3mo:1d"))
    benchmark_return, benchmark_at = None, None
    benchmark_error = None
    try:
        benchmark = _history(benchmark_row)
        if benchmark is not None and "Close" in benchmark:
            close = benchmark["Close"].dropna()
            if len(close) >= 21 and close.iloc[-21] != 0:
                benchmark_return = float((close.iloc[-1] / close.iloc[-21] - 1) * 100)
                benchmark_at = close.index[-1].isoformat()
    except (ValueError, KeyError, TypeError) as exc:
        benchmark_error = type(exc).__name__
    instruments = []
    for watch in capture["watchlist"]:
        symbol = watch["symbol"]
        fa_row = agents.get((symbol, "fundamental"))
        fa = _payload(fa_row, "result_json")
        fa_inputs = ("pe_ratio", "revenue_growth", "roe", "debt_equity")
        missing_fa = tuple(k for k in fa_inputs if not _finite(fa.get(k)))
        fa_present = _finite(fa.get("fa_score")) and "error" not in fa and len(missing_fa) < 4
        fundamental = Evidence(value=fa.get("fa_score") if _finite(fa.get("fa_score")) else None,
            available=fa_present, source="AgentCache.fundamental", scoring_version=None,
            cached_at=(fa_row or {}).get("cached_at"),
            # Partial FA is visible and excluded by the strict experiment below.
            missing_inputs=missing_fa,
            limitations=_cache_limits(fa_row, capture["as_of"])
                + ("cached_fa_scoring_version_unrecorded",)
                + (("fa_score_has_no_observed_components",) if len(missing_fa) == 4 else ()),
            inputs=tuple((k, fa.get(k) if _finite(fa.get(k)) else None) for k in fa_inputs))
        timing_symbol = watch["timing_fetch_symbol"]
        history_row = market.get((timing_symbol, "history:1y:1d"))
        indicators, observed_at, history_error = {}, None, None
        try:
            frame = _history(history_row)
            if frame is not None:
                indicators = functions["_extract_indicators"](frame)
                if indicators and "Close" in frame:
                    observed_at = frame["Close"].dropna().index[-1].isoformat()
        except (ValueError, KeyError, TypeError, IndexError) as exc:
            history_error = type(exc).__name__
        indicators["benchmark_return_20d"] = benchmark_return
        required = ("price", "sma20", "sma50", "rsi", "current_volume", "avg_volume_20d",
                    "stock_return_20d", "benchmark_return_20d")
        missing_timing = tuple(k for k in required if not _finite(indicators.get(k)))
        # Nonfinite inputs must not enter the canonical scorer as observations.
        clean = {k: v if _finite(v) else None for k, v in indicators.items()}
        result = functions["compute_timing_score"](symbol=symbol,
            **{k: clean.get(k) for k in ("price", "sma20", "sma50", "sma200", "rsi",
                "current_volume", "avg_volume_20d", "stock_return_20d", "benchmark_return_20d")})
        limits = list(_cache_limits(history_row, capture["as_of"]))
        if benchmark_at != observed_at:
            limits.append("benchmark_and_instrument_observation_dates_differ")
        if missing_timing:
            limits.append("canonical_timing_contains_default_components")
        if history_error or benchmark_error:
            limits.append("malformed_cached_history")
        if watch.get("timing_symbol_source"):
            limits.append(watch["timing_symbol_source"])
        timing = Evidence(value=float(result.timing_score) if result.data_available else None,
            available=result.data_available and not missing_timing, source="canonical_timing_from_cached_history",
            scoring_version=expected["timing"], observed_at=observed_at,
            cached_at=(history_row or {}).get("fetched_at"), expires_at=(history_row or {}).get("expires_at"),
            missing_inputs=missing_timing, limitations=tuple(sorted(set(limits))),
            inputs=tuple((k, clean.get(k)) for k in (*required, "sma200")),
            provenance=(("history_symbol", timing_symbol), ("benchmark_symbol", "SPY"),
                ("benchmark_observed_at", benchmark_at),
                ("benchmark_cached_at", (benchmark_row or {}).get("fetched_at")),
                ("benchmark_expires_at", (benchmark_row or {}).get("expires_at"))))
        asset = assets.get(watch.get("asset_id"))
        related = sorted({r["to_asset_id"] for r in capture["relationships"]
                          if r["from_asset_id"] == watch.get("asset_id")
                          and r["relationship_type"] == "DEPOSITARY_RECEIPT_OF"
                          and (not r.get("effective_date") or r["effective_date"] <= capture["as_of"])})
        supported = bool(fa and "error" not in fa and "fa_score" in fa)
        instruments.append(Instrument(symbol=symbol, fundamental=fundamental, timing=timing,
            asset_id=asset["id"] if asset else None, asset_type=asset["asset_type"] if asset else None,
            supported_stock_evidence=supported,
            identity_source="Watchlist.asset_id" if asset else "Watchlist.symbol (listing only)",
            related_asset_ids=tuple(related), parent_symbol=fa.get("parent_symbol"),
            relationship_source="AssetRelationship.DEPOSITARY_RECEIPT_OF" if related
                else "cached FA provider parent (not canonical identity)" if fa.get("parent_symbol") else None,
            sector=fa.get("sector") or watch.get("sector"),
            limitations=() if asset else ("canonical_asset_identity_unavailable",)))
    snapshot = DiscoveryInput(capture["universe_id"], capture["as_of"], capture["captured_at"],
        tuple(instruments), limitations=(
            "cross_section_uses_latest_local_caches_with_mixed_observation_epochs",
            "complete_FA_and_timing_components_required_by_this_experiment",
            "expired_caches_retained_for_offline_diagnostics_not_current_opportunities",
            "liquidity_and_valuation_are_not_discovery_dimensions"))
    overlays = []
    for portfolio in capture["portfolios"]:
        stored = next((r for r in capture.get("portfolio_snapshots", [])
                       if r["portfolio_id"] == portfolio["id"]), None)
        saved_holdings = json.loads(stored["holdings_json"]) if stored and stored.get("holdings_json") else []
        exposures = {r["symbol"]: r for r in saved_holdings}
        policy = next((r for r in capture.get("policy_snapshots", [])
                       if r["portfolio_id"] == portfolio["id"]), None)
        envelope = _payload(policy, "constraint_envelope_json")
        holdings = []
        for row in capture["holdings"]:
            if row["portfolio_id"] != portfolio["id"]:
                continue
            saved = exposures.get(row["symbol"], {})
            # Historic exposure only when the captured quantity still matches.
            matched = saved.get("shares") == row.get("shares")
            holdings.append(Holding(row["symbol"], row.get("asset_id"), row["allow_swap"],
                row.get("sector") or saved.get("sector"),
                saved.get("market_value") if matched else None,
                saved.get("weight_pct") if matched else None))
        sectors = json.loads(stored["sector_breakdown_json"]) if stored and stored.get("sector_breakdown_json") else {}
        overlays.append(PortfolioOverlayInput(str(portfolio["id"]), capture["as_of"], tuple(holdings),
            exposure_source=f"PortfolioSnapshot:{stored['id']}:{stored['snapshot_date']}" if stored else None,
            policy_source=f"RecommendationSnapshot:{policy['id']}:{policy['created_at']}" if policy else None,
            sector_weights=tuple(sorted(sectors.items())),
            sector_caps=tuple(sorted(envelope.get("effective_sector_limits", {}).items())),
            position_cap=envelope.get("effective_single_position_pct"),
            limitations=("current_valuation_and_policy_not_reconstructed",
                         "holdings_do_not_imply_owner_preference"),
            nontradable_asset_ids=tuple(a["id"] for a in capture["assets"] if not a["tradable"])))
    return snapshot, tuple(overlays)


def compare_capture(capture: dict) -> dict:
    snapshot, contexts = adapt_capture(capture)
    standalone = discover(snapshot)
    agents = {(r["symbol"], r["agent"]): _payload(r, "result_json") for r in capture["agent_cache"]}
    analyses = {r["symbol"]: r for r in capture["analysis_cache"]}
    legacy = []
    for item in capture["watchlist"]:
        symbol = item["symbol"]
        fa, ta = agents.get((symbol, "fundamental"), {}), agents.get((symbol, "technical"), {})
        legacy.append({"symbol": symbol, "signal": analyses.get(symbol, {}).get("signal", "HOLD"),
            "fa_score": fa.get("fa_score", 0) if "error" not in fa else 0,
            "ta_score": ta.get("ta_score", 0) if "error" not in ta else 0})
    # Reuse the exact production compressor, including its stable ties/top ten.
    tree = ast.parse(LEGACY_SOURCE.read_text(encoding="utf-8"))
    gate = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "_L1_BUY_SIGNALS" for t in n.targets))
    namespace = {}
    exec(compile(ast.Module(body=[gate], type_ignores=[]), str(LEGACY_SOURCE), "exec"), namespace)
    namespace = _definitions(LEGACY_SOURCE, {"_compress_for_layer1"}, namespace)
    _, compact = namespace["_compress_for_layer1"]([], legacy)
    top = [r["s"] for r in compact]
    gated = [r for r in legacy if r["signal"] in namespace["_L1_BUY_SIGNALS"]]
    ordered = sorted(gated, key=lambda r: -(r["fa_score"] + r["ta_score"]))
    cutoff = (ordered[min(10, len(ordered)) - 1]["fa_score"]
              + ordered[min(10, len(ordered)) - 1]["ta_score"]) if ordered else None
    cutoff_ties = sorted(r["symbol"] for r in ordered if r["fa_score"] + r["ta_score"] == cutoff)
    unrestricted = sorted(legacy, key=lambda r: -(r["fa_score"] + r["ta_score"]))
    shortlist = standalone["experimental_shortlist"]["symbols"]
    by_symbol = {r["instrument"]["symbol"]: r for r in standalone["candidates"]}
    from collections import Counter
    pair_counts = Counter()
    eligible = [r for r in standalone["candidates"] if r["relative"]]
    for index, a in enumerate(eligible):
        for b in eligible[index + 1:]:
            symbol = b["instrument"]["symbol"]
            kind = ("dominance" if symbol in a["relative"]["dominates"] or
                symbol in a["relative"]["dominated_by"] else
                "exact_tie" if symbol in a["relative"]["joint_ties"] else "incomparable")
            pair_counts[kind] += 1
    return {"report_version": "wealth.shadow-comparison.v1", "standalone": standalone,
        "discovery_input": asdict(snapshot),
        "portfolio_overlays": [portfolio_overlay(snapshot, c) for c in contexts],
        "legacy": {"signal_distribution": dict(sorted(Counter(
            r["signal"] if r["symbol"] in analyses else "MISSING_ANALYSIS_CACHE" for r in legacy).items())),
            "l1_gate": sorted(namespace["_L1_BUY_SIGNALS"]), "l1_eligible_count": len(gated),
            "captured_order_top_10": top, "gated_fa_plus_ta_order": ordered,
            "top_10_cutoff_score": cutoff, "cutoff_ties": cutoff_ties,
            "cutoff_ties_omitted": sorted(set(cutoff_ties) - set(top)),
            "unrestricted_fa_plus_ta_order": unrestricted,
            "exact_current_runtime_result": "UNPROVEN",
            "limitations": ["cached_FA_TA_may_expire_and_runtime_may_refresh",
                "watchlist_captured_in_id_order_runtime_query_has_no_order_by",
                "analysis_source_settings_not_replayed",
                "legacy_tie_order_is_input_order_not_canonical_order"],
            "source_digest": capture["source_digests"]["legacy"]},
        "comparison": {"both": sorted(set(top) & set(shortlist)),
            "legacy_only": sorted(set(top) - set(shortlist)),
            "discovery_only": sorted(set(shortlist) - set(top)),
            "eligible_pair_relationships": dict(sorted(pair_counts.items())),
            "universe_sector_distribution": dict(sorted(Counter(
                r["instrument"]["sector"] or "UNKNOWN" for r in standalone["candidates"]).items())),
            "ranking_eligible_sector_distribution": dict(sorted(Counter(
                r["instrument"]["sector"] or "UNKNOWN" for r in eligible).items())),
            "shortlist_sector_distribution": dict(sorted(Counter(
                by_symbol[s]["instrument"]["sector"] or "UNKNOWN" for s in shortlist).items()))}}
