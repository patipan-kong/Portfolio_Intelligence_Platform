"""Frozen optimizer concentration inputs and deterministic evaluations."""

from math import isfinite

from services.optimizer.nav_basis import item_value
from services.portfolio_sector import SECTOR_CLASSIFICATION_VERSION

EVIDENCE_VERSION = "wealth.policy-evidence.v2"
SECTOR_RULE = "effective_sector_limits"
POSITION_RULE = "hard_constraints.max_single_position_pct"
TOLERANCE = 1e-8


def normalize_policy_sector(raw: str | None) -> str:
    # Preserve the existing policy taxonomy and its treatment of unknowns.
    sector = (raw or "Other").strip()
    if sector in {"Technology", "Financial", "Energy", "Healthcare", "Consumer",
                  "Industrial", "Real Estate", "Utilities"}:
        return sector
    if "Financial" in sector or "Bank" in sector:
        return "Financial"
    return "Other"


def freeze_positions(holdings: list[dict], candidates=()) -> dict:
    positions = {}
    for row in [*candidates, *holdings]:
        price = float(row.get("current_price") or 0)
        value = row.get("value_exact", row.get("market_value"))
        if value is None:
            value = item_value(row)
        classification = row.get("sector_classification")
        positions[row["symbol"]] = {
            "sector": classification["sector"] if classification is not None else normalize_policy_sector(row.get("sector")),
            **({"sector_classification": dict(classification)} if classification is not None else {}),
            "value": max(0.0, float(value)),
            "price": price if isfinite(price) and price > 0 else None,
            "held": bool(row.get("shares") or value),
        }
    return positions


def current_values(positions: dict) -> dict:
    return {symbol: row["value"] for symbol, row in positions.items()}


def project_targets(positions: dict, allocations: list[dict], nav: float) -> dict:
    values = current_values(positions)
    for row in allocations:
        symbol = row["symbol"]
        action = row.get("action", "HOLD").upper()
        current = values.get(symbol, 0.0)
        target = nav * float(row.get("target_weight") or 0) / 100
        if action == "SELL":
            values[symbol] = 0.0
        elif action in ("BUY", "ACCUMULATE"):
            values[symbol] = max(current, target)
        elif action == "REDUCE":
            values[symbol] = max(0.0, min(current, target))
    return values


def evaluate_exposure(
    subject: str, numerator: float, denominator: float, limit: float,
    stage: str, basis: str, source: str,
) -> dict:
    observed = numerator / denominator * 100 if denominator > 0 else None
    excess = max(0.0, observed - limit) if observed is not None else 0.0
    if excess <= TOLERANCE:
        excess = 0.0
    sector = basis == "EQUITY"
    rule = SECTOR_RULE if sector else POSITION_RULE
    return {
        "evidence_version": EVIDENCE_VERSION,
        "evidence_id": f"{stage}:{rule}:{subject}",
        "type": "CONCENTRATION_BREACH" if excess else "CONCENTRATION_EVALUATION",
        "scope": "SECTOR" if sector else "SINGLE_POSITION",
        "sector" if sector else "symbol": subject,
        "rule": rule,
        "stage": stage,
        "basis": basis,
        "currency": "THB",
        "numerator": numerator,
        "denominator": denominator,
        "observed_pct": observed,
        "limit_pct": limit,
        "binding_source": source,
        "breach_pp": excess,
        "breach_amount": denominator * excess / 100,
    }


def evaluate_sectors(
    positions: dict, values: dict, limits: dict, default_cap: float,
    stage: str, sources: dict | None = None,
) -> dict:
    totals: dict[str, float] = {}
    for symbol, value in values.items():
        if value > 0:
            sector = positions.get(symbol, {}).get("sector", "Other")
            totals[sector] = totals.get(sector, 0.0) + value
    equity = sum(totals.values())
    rows = [
        evaluate_exposure(sector, value, equity, float(limits.get(sector, default_cap)),
                          stage, "EQUITY", (sources or {}).get(sector, (sources or {}).get("default", "POLICY_ENGINE")))
        for sector, value in sorted(totals.items())
    ]
    occupied_cap_sum = sum(row["limit_pct"] for row in rows)
    return {
        "basis": "EQUITY",
        "currency": "THB",
        "denominator": equity,
        "applicable": equity > 0,
        "sectors": rows,
        "occupied_cap_sum_pct": occupied_cap_sum if rows else None,
        "infeasible_within_occupied_sectors": bool(rows and occupied_cap_sum < 100 - TOLERANCE),
        "estimated_symbols": sorted(
            symbol for symbol, row in positions.items()
            if row["price"] is None and (row["held"] or values.get(symbol, 0) > 0)
        ),
    }


def sector_weights(evaluation: dict) -> dict:
    return {
        row["sector"]: {"value": round(row["numerator"], 2), "weight_pct": round(row["observed_pct"], 1)}
        for row in sorted(evaluation["sectors"], key=lambda row: -row["numerator"])
    }


def freeze_concentration(holdings: list[dict], candidates: list[dict], policy: dict, nav: float) -> dict:
    positions = freeze_positions(holdings, candidates)
    hard = policy.get("hard_constraints") or {}
    context = {
        "evidence_version": EVIDENCE_VERSION,
        "positions": positions,
        "nav": float(holdings[0]["nav_value"]) if holdings and "nav_value" in holdings[0] else nav,
        "target_nav": nav,
        "limits": policy.get("resolved_sector_limits") or {},
        "sources": policy.get("sector_limit_sources") or {},
        "default_cap": hard.get("max_sector_pct", 40),
        "position_cap": hard.get("max_single_position_pct", 22),
        "position_source": policy.get("position_limit_source") or "POLICY_ENGINE",
        "turnover_cap": policy.get("relaxed_turnover_cap") or hard.get("max_turnover_pct", 40),
    }
    if any("sector_classification" in row for row in positions.values()):
        context["sector_classification_version"] = SECTOR_CLASSIFICATION_VERSION
    values = current_values(positions)
    current = evaluate_frozen_sectors(context, values, "CURRENT")
    context["current"] = current
    context["current_breaches"] = [row for row in current["sectors"] if row["breach_pp"]]
    for symbol, value in values.items():
        row = evaluate_exposure(symbol, value, context["nav"], context["position_cap"], "CURRENT",
                                "NAV", context["position_source"])
        if row["breach_pp"]:
            context["current_breaches"].append(row)
    return context


def evaluate_frozen_sectors(context: dict, values: dict, stage: str) -> dict:
    return evaluate_sectors(context["positions"], values, context["limits"],
                            context["default_cap"], stage, context["sources"])


def attach_target_evaluation(result: dict) -> None:
    policy = result.get("active_policy") or {}
    context = policy.get("concentration")
    if not context:
        return
    values = project_targets(context["positions"], result["target_allocations"], context["target_nav"])
    target = evaluate_frozen_sectors(context, values, "PROJECTED_TARGET")
    context["projected_target"] = target
    current = context["current"]
    result["current_sector_weights"] = sector_weights(current)
    result["projected_sector_weights"] = sector_weights(target)
    current_by_sector = {row["sector"]: row for row in current["sectors"]}
    target_by_sector = {row["sector"]: row for row in target["sectors"]}
    warnings = []
    for sector in sorted(current_by_sector.keys() | target_by_sector.keys()):
        before = current_by_sector.get(sector, {})
        after = target_by_sector.get(sector, {})
        limit = (after or before)["limit_pct"]
        projected = after.get("observed_pct", 0)
        warnings.append({
            "sector": sector,
            "current_pct": before.get("observed_pct", 0),
            "projected_pct": projected,
            "limit_pct": limit,
            "status": "EXCEEDS" if after.get("breach_pp") else "WARNING" if projected > limit * 0.8 else "OK",
        })
    result["sector_warnings"] = warnings
