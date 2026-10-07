"""Slice 1B offline diagnostics. No new eligibility, score or decision authority.

The v1 captured experiment remains intact. Candidate budgets are diagnostic
parameters; no extraction method is a default or a production winner.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from itertools import accumulate
import json

from services.candidate_discovery_evidence import compare_capture

REFINEMENT_VERSION = "wealth.shadow-discovery-refinement.v1"
FA_FIELDS = {
    "pe_ratio": ("trailingPE", "forwardPE"),
    "revenue_growth": ("revenueGrowth",),
    "roe": ("returnOnEquity",),
    "debt_equity": ("debtToEquity",),
}
IMPORTANT_SYMBOLS = (
    "MICRON01.BK", "TOP.BK", "GOOGL01.BK", "META01.BK", "NVDA01.BK",
    "MSFT01.BK", "ASML01.BK", "AAPL01.BK", "CATL01.BK", "PTT.BK",
    "PTTEP.BK", "HMPRO.BK",
)


def cumulative_pareto(fronts: list[list[str]], candidate_budget: int) -> dict:
    """Include whole fronts until budget is reached, including boundary overshoot."""
    if isinstance(candidate_budget, bool) or not isinstance(candidate_budget, int) or candidate_budget < 1:
        raise ValueError("candidate budget must be a positive integer")
    flattened = [s for front in fronts for s in front]
    if len(flattened) != len(set(flattened)) or any(not front for front in fronts):
        raise ValueError("fronts must be nonempty and disjoint")
    included, symbols = [], []
    for number, front in enumerate(fronts, 1):
        if len(symbols) >= candidate_budget:
            break
        included.append(number)
        symbols.extend(sorted(front))
    overshoot = max(0, len(symbols) - candidate_budget)
    return {"method": "cumulative_pareto", "requested_budget": candidate_budget,
        "symbols": symbols, "actual_count": len(symbols), "included_fronts": included,
        "overshoot": overshoot, "overshoot_reason": "complete_boundary_front" if overshoot else None,
        "shortfall": max(0, candidate_budget - len(symbols)), "ties_split": False}


def dimension_leaders(standalone: dict, dimension: str, budget: int) -> dict:
    """Top N observed values in the jointly eligible cohort, preserving boundary ties.

    Budget is a target; a boundary tie may exceed it. Excluded values appear in
    separate research records and never influence these percentiles or boundaries.
    """
    if dimension not in ("fundamental", "timing"):
        raise ValueError("unsupported evidence dimension")
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 1:
        raise ValueError("leader budget must be a positive integer")
    eligible = [r for r in standalone["candidates"] if r["relative"] is not None]
    values = sorted((r["relative"][dimension]["value"] for r in eligible), reverse=True)
    cutoff = values[min(budget, len(values)) - 1] if values else None
    selected = [r for r in eligible if r["relative"][dimension]["value"] >= cutoff]
    selected.sort(key=lambda r: (-r["relative"][dimension]["value"], r["instrument"]["symbol"]))
    return {"dimension": dimension, "cohort": "joint_ranking_eligible", "requested_budget": budget,
        "boundary_value": cutoff, "actual_count": len(selected),
        "overshoot": max(0, len(selected) - budget), "ties_split": False,
        "leaders": [{"symbol": r["instrument"]["symbol"], "sector": r["instrument"]["sector"],
            "raw_score": r["relative"][dimension]["value"],
            "percentile": r["relative"][dimension]["midrank_percentile"],
            "ties": r["relative"][dimension]["ties"],
            "ranking_eligibility": r["ranking_eligibility"]} for r in selected]}


def candidate_sets(standalone: dict, budgets: tuple[int, ...] = (5, 10, 15)) -> dict:
    """Three inspectable methods; none is the default shortlist.

    Leader union uses the stated budget PER DIMENSION. Its nominal bound is 2N
    before duplicate removal, with explicit boundary-tie exceptions. It is not
    directly the same size target as cumulative Pareto's total budget.
    """
    front_one = standalone["pareto_fronts"][0] if standalone["pareto_fronts"] else []
    result = {"front_1": {"method": "front_1_only", "symbols": sorted(front_one),
                          "actual_count": len(front_one), "cap": None, "ties_split": False}}
    for budget in budgets:
        result[f"cumulative_{budget}"] = cumulative_pareto(standalone["pareto_fronts"], budget)
        fa = dimension_leaders(standalone, "fundamental", budget)
        timing = dimension_leaders(standalone, "timing", budget)
        symbols = sorted({r["symbol"] for r in fa["leaders"] + timing["leaders"]})
        result[f"dimension_union_{budget}"] = {
            "method": "dimension_leader_union", "per_dimension_budget": budget,
            "nominal_union_bound": 2 * budget, "symbols": symbols, "actual_count": len(symbols),
            "above_nominal_bound": max(0, len(symbols) - 2 * budget),
            "fundamental_boundary": fa["boundary_value"], "timing_boundary": timing["boundary_value"],
            "fundamental_boundary_overshoot": fa["overshoot"],
            "timing_boundary_overshoot": timing["overshoot"],
            "overshoot_reason": "dimension_boundary_ties" if len(symbols) > 2 * budget else None,
            "ties_split": False}
    return result


def _timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    # Do not invent the timezone of an unqualified timestamp.
    return parsed.astimezone(timezone.utc) if parsed.tzinfo else None


def _distribution(values: list[float]) -> dict:
    ordered = sorted(values)
    if not ordered:
        return {"count": 0, "min": None, "median": None, "max": None}
    n = len(ordered)
    median = ordered[n // 2] if n % 2 else (ordered[n // 2 - 1] + ordered[n // 2]) / 2
    return {"count": n, "min": round(ordered[0], 6), "median": round(median, 6),
            "max": round(ordered[-1], 6)}


def temporal_diagnostics(standalone: dict) -> dict:
    """Report ages/deltas, never freshness. Cache time is not observation time."""
    boundary = _timestamp(standalone["as_of"])
    rows = []
    for row in standalone["candidates"]:
        item = row["instrument"]
        fa, timing = item["fundamental"], item["timing"]
        provenance = dict(timing["provenance"])
        market = _timestamp(timing["observed_at"])
        financial = _timestamp(fa["observed_at"])
        benchmark = _timestamp(provenance.get("benchmark_observed_at"))
        delta = (benchmark - market).total_seconds() / 86400 if market and benchmark else None
        rows.append({"symbol": item["symbol"], "timing_bar_index_at": timing["observed_at"],
            "timing_cached_at": timing["cached_at"], "timing_expires_at": timing["expires_at"],
            "timing_bar_age_days": (boundary - market).total_seconds() / 86400 if boundary and market else None,
            "fa_cached_at": fa["cached_at"], "fa_observed_at": fa["observed_at"],
            "fa_cache_age_days": (boundary - _timestamp(fa["cached_at"])).total_seconds() / 86400
                if boundary and _timestamp(fa["cached_at"]) else None,
            "fa_observation_age_days": (boundary - financial).total_seconds() / 86400
                if boundary and financial else None,
            "fa_scoring_version_known": fa["scoring_version"] is not None,
            "financial_reporting_period": None,
            "benchmark_bar_index_at": provenance.get("benchmark_observed_at"),
            "benchmark_cached_at": provenance.get("benchmark_cached_at"),
            "benchmark_expires_at": provenance.get("benchmark_expires_at"),
            "benchmark_minus_instrument_days": delta,
            "same_UTC_bar_calendar_date": market.date() == benchmark.date() if market and benchmark else None,
            "calculation_at": None,
            "calculation_semantics": "offline replay execution; not historical market observation"})
    observed = [_timestamp(r["timing_bar_index_at"]) for r in rows]
    known = [t for t in observed if t]
    ages = [r["timing_bar_age_days"] for r in rows if r["timing_bar_age_days"] is not None]
    deltas = [r["benchmark_minus_instrument_days"] for r in rows
              if r["benchmark_minus_instrument_days"] is not None]
    return {"semantics": {
        "as_of": "baseline read-only transaction capture boundary",
        "timing_observation": "history index of last nonmissing Close; bar label, not verified close event time",
        "fa_cache": "agent result cached_at; not financial reporting or observation time",
        "benchmark": "saved SPY daily-bar index; not verified close event time",
        "calculation": "deterministic offline replay; historical calculation time unrecorded"},
        "timing_bar_age_days": _distribution(ages),
        "timing_date_distribution": dict(sorted(Counter(r["timing_bar_index_at"] or "UNKNOWN" for r in rows).items())),
        "timing_bar_spread_days": (max(known) - min(known)).total_seconds() / 86400 if known else None,
        "benchmark_minus_instrument_days": _distribution(deltas),
        "benchmark_after_instrument_count": sum(d > 0 for d in deltas),
        "benchmark_same_index_count": sum(d == 0 for d in deltas),
        "benchmark_same_UTC_calendar_date_count": sum(r["same_UTC_bar_calendar_date"] is True for r in rows),
        "benchmark_different_UTC_calendar_date_count": sum(r["same_UTC_bar_calendar_date"] is False for r in rows),
        "timing_observation_unknown_count": sum(t is None for t in observed),
        "fa_observation_unknown_count": sum(_timestamp(r["fa_observed_at"]) is None for r in rows),
        "fa_scoring_version_unknown_count": sum(not r["fa_scoring_version_known"] for r in rows),
        "financial_reporting_period_unknown_count": len(rows),
        "expired_timing_cache_count": sum(_timestamp(r["timing_expires_at"]) < boundary
            for r in rows if boundary and _timestamp(r["timing_expires_at"])),
        "defensible_comparison": "structural captured-score comparison only",
        "aligned_point_in_time_comparison": "UNPROVEN: FA dates/versions absent; timing windows have different endpoints",
        "current_opportunity_set": False, "candidates": rows}


def exclusion_diagnosis(standalone: dict, supplement: dict | None = None) -> list[dict]:
    """Classify missing fields without inventing applicability or historical lineage."""
    supplement = supplement or {}
    raw = {r["symbol"]: r for r in supplement.get("rows", [])}
    requests = supplement.get("requested_provider_symbols", {})
    result = []
    for row in standalone["candidates"]:
        if row["ranking_eligibility"]["eligible"]:
            continue
        item = row["instrument"]
        provider_symbol = requests.get(item["symbol"], item["parent_symbol"] or item["symbol"])
        cached = raw.get(provider_symbol)
        payload = (cached or {}).get("payload_json", {})
        if isinstance(payload, str):
            payload = json.loads(payload)
        fields = []
        for name in item["fundamental"]["missing_inputs"]:
            keys = FA_FIELDS[name]
            available = any(payload.get(k) is not None for k in keys)
            fields.append({"field": name, "producer_keys": list(keys),
                "producer_path": "YahooProvider.get_fundamentals -> data_fetcher.fetch_info -> "
                    "agents.fundamental.analyze_fundamental -> AgentCache.result_json -> Discovery adapter",
                "baseline_fact": "missing_in_captured_FA_result",
                "supplement_fact": "raw_value_present" if available else
                    "provider_missing_or_null" if cached else "raw_provider_evidence_unavailable",
                "raw_key_status": {k: "absent" if k not in payload else "null" if payload[k] is None
                                   else "present" for k in keys},
                "classification": "unresolved_baseline_epoch_or_adaptation" if available else
                    "provider_missing_in_supplement_baseline_origin_unproven" if cached else "unknown",
                "economic_applicability": "UNKNOWN: no sector-specific applicability contract in inspected FA producer",
                "scoring_semantics": "producer skips missing metric; v1 experiment requires complete inputs"})
        periods = {}
        for key in ("mostRecentQuarter", "lastFiscalYearEnd"):
            value = payload.get(key)
            periods[key] = (datetime.fromtimestamp(value, timezone.utc).isoformat()
                            if isinstance(value, (int, float)) else None)
        result.append({"symbol": item["symbol"], "baseline_sector": item["sector"],
            "listing_form": "DR reported by cached FA parent field" if item["parent_symbol"]
                else "listing; canonical security type unavailable" if item["asset_type"] is None
                else item["asset_type"],
            "canonical_asset_type": item["asset_type"], "provider_symbol": provider_symbol,
            "provider_quote_type": payload.get("quoteType"), "provider_sector": payload.get("sector"),
            "provider_industry": payload.get("industry"), "supplement_fetched_at": (cached or {}).get("fetched_at"),
            "provider_reporting_periods": periods, "fields": fields,
            "eligibility_reasons": row["ranking_eligibility"]["reasons"],
            "profile_limitation": "provider_reports_ETF; corporate_FA_profile_and_binding_require_review"
                if payload.get("quoteType") == "ETF" else "sector_applicability_unresolved",
            "lineage_limitation": "supplement is diagnosis only; not proven original baseline provider response"})
    return result


def _comparison(symbols: list[str], baseline: dict) -> dict:
    selected = set(symbols)
    legacy = baseline["legacy"]
    gate = {r["symbol"] for r in legacy["gated_fa_plus_ta_order"]}
    targets = {"legacy_gate": gate, "legacy_top_10": set(legacy["captured_order_top_10"]),
               "unrestricted_fa_plus_ta_top_10": {r["symbol"] for r in legacy["unrestricted_fa_plus_ta_order"][:10]}}
    return {name: {"overlap_count": len(selected & target),
                  "percent_of_discovery_set": 100 * len(selected & target) / len(selected) if selected else None,
                  "percent_of_legacy_set": 100 * len(selected & target) / len(target) if target else None,
                  "legacy_only": sorted(target - selected), "discovery_only": sorted(selected - target)}
            for name, target in targets.items()}


def refine_capture(capture: dict, supplement: dict | None = None,
                   budgets: tuple[int, ...] = (5, 10, 15)) -> dict:
    """All membership is computed before labels or portfolio annotations are read."""
    baseline = compare_capture(capture)
    standalone = baseline["standalone"]
    sets = candidate_sets(standalone, budgets)
    candidates = {r["instrument"]["symbol"]: r for r in standalone["candidates"]}
    labels = {r["symbol"]: r["signal"] for r in capture["analysis_cache"]}
    for experiment in sets.values():
        symbols = experiment["symbols"]
        experiment["legacy_comparison"] = _comparison(symbols, baseline)
        experiment["label_distribution_diagnostic_only"] = dict(sorted(Counter(labels.get(s, "MISSING") for s in symbols).items()))
        experiment["sector_distribution"] = dict(sorted(Counter(candidates[s]["instrument"]["sector"] or "UNKNOWN" for s in symbols).items()))
        experiment["portfolio_diagnostics"] = []
        for overlay in baseline["portfolio_overlays"]:
            selected = [r for r in overlay["candidates"] if r["symbol"] in symbols]
            restricted = [r for r in selected if r["portfolio_add_consideration"]["reasons"]]
            locked = [r["symbol"] for r in selected if "existing_position_locked" in r["portfolio_add_consideration"]["reasons"]]
            experiment["portfolio_diagnostics"].append({"portfolio_id": overlay["portfolio_id"],
                "held": sorted(r["symbol"] for r in selected if r["already_held"]),
                "new": sorted(r["symbol"] for r in selected if not r["already_held"]),
                "locked": sorted(locked), "restrictions": restricted,
                "not_blocked_by_known_hard_restrictions_count": len(selected) - len(restricted),
                "confirmed_current_feasible_count": None,
                "unknown_policy_feasibility_count": sum(bool(r["portfolio_add_consideration"]["limitations"]) for r in selected),
                "captured_sector_weights": overlay["captured_sector_weights"],
                "captured_sector_caps": overlay["captured_sector_caps"],
                "exposure_source": overlay["exposure_source"], "policy_source": overlay["policy_source"],
                "candidate_annotations": selected})
    important = []
    # Include all excluded assets as well as the specifically requested cases.
    symbols = sorted(set(IMPORTANT_SYMBOLS) | {s for s, r in candidates.items() if not r["ranking_eligibility"]["eligible"]})
    for symbol in symbols:
        row = candidates.get(symbol)
        if row is None:
            important.append({"symbol": symbol, "status": "not_in_captured_universe"})
            continue
        item, relative = row["instrument"], row["relative"]
        important.append({"symbol": symbol, "legacy_label": labels.get(symbol),
            "fa": item["fundamental"]["value"], "timing": item["timing"]["value"],
            "fa_percentile": relative["fundamental"]["midrank_percentile"] if relative else None,
            "timing_percentile": relative["timing"]["midrank_percentile"] if relative else None,
            "pareto_front": relative["pareto_front"] if relative else None,
            "legacy_top_10": symbol in baseline["legacy"]["captured_order_top_10"],
            "membership": {name: symbol in exp["symbols"] for name, exp in sets.items()},
            "ranking_eligibility": row["ranking_eligibility"],
            "limitations": list(item["fundamental"]["limitations"]) + list(item["timing"]["limitations"])})
    leaders = {dimension: dimension_leaders(standalone, dimension, 5) for dimension in ("fundamental", "timing")}
    for dimension in leaders.values():
        for row in dimension["leaders"]:
            row["held_new_by_portfolio"] = {o["portfolio_id"]: next(
                "held" if r["already_held"] else "new" for r in o["candidates"] if r["symbol"] == row["symbol"])
                for o in baseline["portfolio_overlays"]}
    eligible = [r for r in standalone["candidates"] if r["relative"]]
    coarseness = {}
    for dimension in ("fundamental", "timing"):
        counts = Counter(r["relative"][dimension]["value"] for r in eligible)
        coarseness[dimension] = {"distinct_values": len(counts), "largest_tie_group": max(counts.values(), default=0),
            "value_counts": {str(value): counts[value] for value in sorted(counts)}}
    joint_maxima = [r["instrument"]["symbol"] for r in eligible if all(
        r["relative"][dimension]["rank_best_first"] == 1 for dimension in ("fundamental", "timing"))]
    return {"refinement_version": REFINEMENT_VERSION, "shadow_only": True,
        "default_candidate_set": None, "baseline": baseline,
        "eligibility_refinement": {"implemented": False,
            "reason": "no_repository_sector_specific_FA_applicability_authority",
            "before_ranking_eligible": standalone["coverage"]["ranking_eligible"],
            "after_ranking_eligible": standalone["coverage"]["ranking_eligible"]},
        "exclusion_diagnosis": exclusion_diagnosis(standalone, supplement),
        "temporal": temporal_diagnostics(standalone), "dimension_leaders": leaders,
        "dimension_coarseness": coarseness, "joint_dimension_maxima": joint_maxima,
        "pareto_structure": {"front_sizes": standalone["front_sizes"],
            "cumulative_counts": list(accumulate(standalone["front_sizes"])),
            "pair_relationships": baseline["comparison"]["eligible_pair_relationships"],
            "sector_composition_by_front": [dict(sorted(Counter(candidates[s]["instrument"]["sector"] or "UNKNOWN"
                for s in front).items())) for front in standalone["pareto_fronts"]]},
        "candidate_sets": sets, "important_cases": important,
        "legacy_top_10_locations": [{"symbol": s, "ranking_eligibility": candidates[s]["ranking_eligibility"],
            "relative": candidates[s]["relative"]} for s in baseline["legacy"]["captured_order_top_10"]]}
