"""Shadow-only FA/Timing experiment. No trade, allocation or runtime authority.

Pure contracts and computations: no database, model, market or global state reads.
Percentiles and Pareto fronts describe this captured universe, not expected returns.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from math import isfinite

CONTRACT_VERSION = "wealth.shadow-discovery.v1"
EXPERIMENT_VERSION = "fa-timing-pareto.v1"


@dataclass(frozen=True)
class Evidence:
    value: float | None
    available: bool
    source: str
    scoring_version: str | None = None
    observed_at: str | None = None
    cached_at: str | None = None
    expires_at: str | None = None
    missing_inputs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    # An upstream validity decision, not a Discovery-invented TTL.
    invalid_reason: str | None = None
    inputs: tuple[tuple[str, float | None], ...] = ()
    provenance: tuple[tuple[str, str | None], ...] = ()


@dataclass(frozen=True)
class Instrument:
    symbol: str
    fundamental: Evidence
    timing: Evidence
    asset_id: int | None = None
    asset_type: str | None = None
    supported_stock_evidence: bool = False
    identity_source: str | None = None
    related_asset_ids: tuple[int, ...] = ()
    parent_symbol: str | None = None
    relationship_source: str | None = None
    sector: str | None = None
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class DiscoveryInput:
    universe_id: str
    as_of: str
    captured_at: str
    instruments: tuple[Instrument, ...]
    contract_version: str = CONTRACT_VERSION
    experiment_version: str = EXPERIMENT_VERSION
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class Holding:
    symbol: str
    asset_id: int | None = None
    allow_swap: bool = True
    sector: str | None = None
    # Copied canonical snapshot facts, never a new valuation calculation.
    market_value: float | None = None
    weight_pct: float | None = None


@dataclass(frozen=True)
class PortfolioOverlayInput:
    portfolio_id: str
    as_of: str
    holdings: tuple[Holding, ...]
    exposure_source: str | None = None
    policy_source: str | None = None
    sector_weights: tuple[tuple[str, float], ...] = ()
    sector_caps: tuple[tuple[str, float], ...] = ()
    position_cap: float | None = None
    max_positions: int | None = None
    nontradable_asset_ids: tuple[int, ...] = ()
    # False for historical/mixed-epoch facts: annotate but do not assert a block.
    constraints_current: bool = False
    limitations: tuple[str, ...] = ()


def _usable(evidence: Evidence) -> bool:
    return (evidence.available and evidence.invalid_reason is None
            and evidence.value is not None and not isinstance(evidence.value, bool)
            and isfinite(evidence.value))


def discover(snapshot: DiscoveryInput) -> dict:
    """Return standalone diagnostics. No portfolio or Stock Analysis label input.

    Experimental shortlist = entire first front, uncapped. Ties are never cut.
    Percentile = 100 * (strictly lower + half equal) / eligible count.
    Thus a singleton/all-equal universe has percentile 50, not 'best = 100'.
    """
    if snapshot.contract_version != CONTRACT_VERSION:
        raise ValueError("unsupported Discovery contract version")
    if snapshot.experiment_version != EXPERIMENT_VERSION:
        raise ValueError("unsupported Discovery experiment version")
    symbols = [i.symbol for i in snapshot.instruments]
    if len(symbols) != len(set(symbols)):
        raise ValueError("duplicate listing symbol")
    items = sorted(snapshot.instruments, key=lambda i: i.symbol)
    rows, eligible = [], []
    for item in items:
        research_reasons = []
        if not item.symbol.strip() or not item.identity_source:
            research_reasons.append("missing_identity")
        if not (_usable(item.fundamental) or _usable(item.timing)):
            research_reasons.append("no_supported_evidence")
        reasons = list(research_reasons)
        supported = (item.asset_type == "EQUITY" or
                     (item.asset_type is None and item.supported_stock_evidence))
        if not supported:
            reasons.append("unsupported_asset_type")
        for name, evidence in (("fundamental", item.fundamental), ("timing", item.timing)):
            if not _usable(evidence):
                reasons.append(f"missing_{name}_evidence")
            if evidence.missing_inputs:
                reasons.append(f"incomplete_{name}_inputs")
            if evidence.invalid_reason:
                reasons.append(f"invalid_{name}_evidence")
        reasons = sorted(set(reasons))
        row = {"instrument": asdict(item), "research_eligibility": {
            "eligible": not research_reasons, "reasons": sorted(research_reasons)},
            "ranking_eligibility": {"eligible": not reasons, "reasons": reasons},
            "relative": None, "shortlist": {"included": False,
                "reason": "ranking_ineligible" if reasons else "dominated"}}
        rows.append(row)
        if not reasons:
            eligible.append(item)

    def dominates(a: Instrument, b: Instrument) -> bool:
        fa, ta = a.fundamental.value, a.timing.value
        fb, tb = b.fundamental.value, b.timing.value
        return fa >= fb and ta >= tb and (fa > fb or ta > tb)

    dominators = {b.symbol: sorted(a.symbol for a in eligible if dominates(a, b))
                  for b in eligible}
    remaining = {i.symbol for i in eligible}
    fronts = []
    while remaining:
        front = sorted(s for s in remaining if not (set(dominators[s]) & remaining))
        fronts.append(front)
        remaining.difference_update(front)
    front_by_symbol = {s: index + 1 for index, front in enumerate(fronts) for s in front}
    by_symbol = {r["instrument"]["symbol"]: r for r in rows}
    for item in eligible:
        relative = {"pareto_front": front_by_symbol[item.symbol],
                    "dominated_by": dominators[item.symbol],
                    "dominates": sorted(b.symbol for b in eligible if dominates(item, b)),
                    "joint_ties": sorted(b.symbol for b in eligible
                        if b.symbol != item.symbol and b.fundamental.value == item.fundamental.value
                        and b.timing.value == item.timing.value)}
        for dimension in ("fundamental", "timing"):
            value = getattr(item, dimension).value
            values = [getattr(i, dimension).value for i in eligible]
            equal = [i.symbol for i in eligible if getattr(i, dimension).value == value]
            relative[dimension] = {"value": value,
                "rank_best_first": 1 + sum(v > value for v in values),
                "midrank_percentile": round(100 * (sum(v < value for v in values)
                                                   + len(equal) / 2) / len(values), 6),
                "ties": sorted(equal)}
        row = by_symbol[item.symbol]
        row["relative"] = relative
        row["shortlist"] = {"included": front_by_symbol[item.symbol] == 1,
                            "reason": "first_pareto_front" if front_by_symbol[item.symbol] == 1
                            else "dominated"}
    count = len(items)
    return {"contract_version": CONTRACT_VERSION, "experiment_version": EXPERIMENT_VERSION,
        "shadow_only": True, "universe_id": snapshot.universe_id,
        "as_of": snapshot.as_of, "captured_at": snapshot.captured_at,
        "limitations": list(snapshot.limitations), "candidates": rows,
        "coverage": {"universe_size": count,
            "research_eligible": sum(r["research_eligibility"]["eligible"] for r in rows),
            "ranking_eligible": len(eligible), "excluded": count - len(eligible),
            "ranking_coverage_fraction": len(eligible) / count if count else None,
            "excluded_by_reason": dict(sorted(Counter(reason for r in rows
                for reason in r["ranking_eligibility"]["reasons"]).items())),
            "missing_by_dimension": {name: sum(not _usable(getattr(i, name)) for i in items)
                                     for name in ("fundamental", "timing")},
            "incomplete_by_dimension": {name: sum(bool(getattr(i, name).missing_inputs) for i in items)
                                        for name in ("fundamental", "timing")},
            "missing_inputs_by_dimension": {name: dict(sorted(Counter(field for i in items
                for field in getattr(i, name).missing_inputs).items()))
                for name in ("fundamental", "timing")}},
        "pareto_fronts": fronts, "front_sizes": [len(f) for f in fronts],
        "experimental_shortlist": {"rule": "entire_first_front", "cap": None,
            "symbols": fronts[0] if fronts else [], "omitted_due_to_cap": []}}


def portfolio_overlay(snapshot: DiscoveryInput, context: PortfolioOverlayInput) -> dict:
    """Annotate consideration separately; never re-rank or alter standalone output.

    'unblocked' is not suitability, readiness or execution approval. Missing policy
    or mismatched epochs return unknown, not unconstrained. Existing locks apply.
    """
    standalone = discover(snapshot)
    ranking = {r["instrument"]["symbol"]: r["ranking_eligibility"] for r in standalone["candidates"]}
    weights, caps = dict(context.sector_weights), dict(context.sector_caps)
    rows = []
    for item in sorted(snapshot.instruments, key=lambda i: i.symbol):
        held = [h for h in context.holdings if h.symbol == item.symbol or
                (item.asset_id is not None and h.asset_id == item.asset_id)]
        related = [h for h in context.holdings if h.asset_id is not None
                   and h.asset_id in item.related_asset_ids]
        blocked, unknown = [], []
        if not ranking[item.symbol]["eligible"]:
            blocked.append("ranking_ineligible")
        if any(not h.allow_swap for h in held):
            blocked.append("existing_position_locked")
        if item.asset_id in context.nontradable_asset_ids:
            blocked.append("instrument_not_tradable")
        if context.constraints_current:
            if (not held and context.max_positions is not None
                    and len(context.holdings) >= context.max_positions):
                blocked.append("position_count_limit")
            if item.sector in weights and item.sector in caps:
                if weights[item.sector] >= caps[item.sector]:
                    blocked.append("sector_cap_reached")
            else:
                unknown.append("sector_constraint_unknown")
            if context.position_cap is not None:
                if any(h.weight_pct is not None and h.weight_pct >= context.position_cap for h in held):
                    blocked.append("position_cap_reached")
                if any(h.weight_pct is None for h in held):
                    unknown.append("current_exposure_unknown")
            else:
                unknown.append("position_cap_unknown")
        else:
            unknown.append("current_policy_context_unproven")
        rows.append({"symbol": item.symbol, "already_held": bool(held),
            "held_exposure": [asdict(h) for h in held],
            "related_exposure": [asdict(h) for h in related],
            "portfolio_add_consideration": {
                "status": "constrained" if blocked else "unknown" if unknown else "unblocked",
                "reasons": sorted(blocked), "limitations": sorted(unknown)}})
    return {"portfolio_id": context.portfolio_id, "as_of": context.as_of,
            "exposure_source": context.exposure_source, "policy_source": context.policy_source,
            "constraints_current": context.constraints_current,
            "captured_sector_weights": dict(context.sector_weights),
            "captured_sector_caps": dict(context.sector_caps),
            "captured_position_cap": context.position_cap,
            "limitations": list(context.limitations), "candidates": rows}
