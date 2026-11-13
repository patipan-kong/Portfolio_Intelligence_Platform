"""Size and verify concentration repairs on the scheduled recommendation."""

from math import ceil, floor, isfinite

from services.optimizer.sector_policy import (
    EVIDENCE_VERSION, OPTIMIZER_POLICY_MUJI_V2, TOLERANCE, current_values, evaluate_exposure,
    evaluate_frozen_sectors, optimizer_policy_mode, project_targets, sector_caps_are_advisory,
)
from services.optimizer.execution_optimizer import ExecutionOptimizationResult, OptimizedTrade
from services.optimizer.stabilization import EST_TRADE_COST_BPS_PER_PCT

_ADVISORY_COST_RATE = EST_TRADE_COST_BPS_PER_PCT


def _floor_money(amount: float) -> float:
    return floor(max(0.0, amount) * 100 + TOLERANCE) / 100


def _position_slot_excess(position_limit, sales, buys, changes):
    """New buys that max_stocks leaves no slot for, given the sales actually scheduled.

    position_limit: (max_stocks, active holdings, SELL-row symbols, target weight per buy).
    Only a SELL scheduled for its full position value frees a slot: a deferred, partial,
    noise-suppressed (never summarized) or REDUCE sale does not. Slots go to the highest
    target weights, ties by symbol, as in the hard-policy new-position limiter.
    """
    if position_limit is None:
        return set()
    max_stocks, active, sell_rows, priority = position_limit
    full_exits = {symbol for symbol in sell_rows
                  if symbol in active and symbol in changes and -changes[symbol] >= sales[symbol] - TOLERANCE}
    room = max(0, max_stocks - len(active) + len(full_exits))
    new = sorted((symbol for symbol in buys if symbol not in active),
                 key=lambda symbol: (-priority.get(symbol, 0.0), symbol))
    return set(new[room:])


def _muji_schedule(sales, buys, verified_sales, values, cash, spendable_cash, budget, emergency_buy_freeze,
                   position_limit=None):
    """Schedule independently evidenced sales before sizing funded purchases.

    Returns the buys excluded by position_limit (max_stocks) as a fifth value.
    """
    changes = {}
    remaining_turnover = budget
    costs = {}
    for symbol in sorted(verified_sales):
        amount = min(sales[symbol], remaining_turnover)
        if amount > TOLERANCE:
            changes[symbol] = -amount
            costs[symbol] = ceil(amount * _ADVISORY_COST_RATE * 100 - TOLERANCE) / 100
            remaining_turnover = _floor_money(remaining_turnover - amount)
    excluded = _position_slot_excess(position_limit, sales, buys, changes)
    available = _floor_money(max(0.0, spendable_cash) + sum(-change - costs[symbol]
                                                           for symbol, change in changes.items()))
    scheduled_buys = {}
    if not emergency_buy_freeze:
        for symbol in sorted(set(buys) - excluded):
            amount = min(buys[symbol], remaining_turnover,
                         _floor_money(available / (1 + _ADVISORY_COST_RATE)))
            while amount > 0 and amount + ceil(amount * _ADVISORY_COST_RATE * 100 - TOLERANCE) / 100 > available + TOLERANCE:
                amount = _floor_money(amount - 0.01)
            if amount > TOLERANCE:
                scheduled_buys[symbol] = amount
                changes[symbol] = amount
                costs[symbol] = ceil(amount * _ADVISORY_COST_RATE * 100 - TOLERANCE) / 100
                available = _floor_money(available - amount - costs[symbol])
                remaining_turnover = _floor_money(remaining_turnover - amount)
    return (changes, scheduled_buys, costs, round(cash - sum(changes.values()) - sum(costs.values()), 2),
            excluded)


def _position_row(context, values, symbol, stage):
    return evaluate_exposure(symbol, values.get(symbol, 0.0), context["nav"],
                             context["position_cap"], stage, "NAV", context["position_source"])


def _sector_row(context, values, current, stage):
    evaluation = evaluate_frozen_sectors(context, values, stage)
    return next((row for row in evaluation["sectors"] if row["sector"] == current["sector"]),
                evaluate_exposure(current["sector"], 0, evaluation["denominator"], current["limit_pct"],
                                  stage, "EQUITY", current["binding_source"]))


def _supported_amount(row: dict) -> float:
    if row["basis"] == "NAV":
        return row["breach_amount"]
    cap = row["limit_pct"] / 100
    # Selling removes value from both the numerator and denominator.
    if cap < 1 and row["numerator"] < row["denominator"] - TOLERANCE:
        return row["breach_amount"] / (1 - cap)
    return 0.0


def _trade_row(row, symbol):
    return {**row, "evidence_id": f"{row['evidence_id']}:{symbol}"}


def _uncertain_sector_membership(context, values):
    if not context.get("sector_classification_version"):
        return False
    for symbol, value in values.items():
        classification = context["positions"].get(symbol, {}).get("sector_classification") or {}
        if value > 0 and classification.get("classification_status") != "authoritative":
            return True
    return False


def _current_support(context, values, *, sector_advisory=False):
    """Use only frozen, reproducible evidence. An estimate taints the denominator."""
    if context["current"]["estimated_symbols"]:
        return {}
    sector_rows = {} if sector_advisory else {
        row["sector"]: row for row in evaluate_frozen_sectors(context, values, "CURRENT")["sectors"]
    }
    support = {}
    uncertain_membership = _uncertain_sector_membership(context, values)
    for row in context.get("current_breaches", []):
        if row.get("basis") == "NAV":
            recomputed = _position_row(context, values, row.get("symbol"), "CURRENT")
        elif uncertain_membership:
            continue
        else:
            recomputed = sector_rows.get(row.get("sector"))
        if row == recomputed and row["breach_pp"] > 0:
            subject = row.get("symbol") if row["basis"] == "NAV" else row["sector"]
            support[(row["basis"], subject)] = row
    return support


def _effects(context, base_values, scheduled, symbol, change):
    without = {**scheduled, symbol: base_values.get(symbol, 0.0)}
    before_sectors = evaluate_frozen_sectors(context, without, "WITHOUT_TRADE")
    after_sectors = evaluate_frozen_sectors(context, scheduled, "PROJECTED_SCHEDULED")
    before_map = {row["sector"]: row for row in before_sectors["sectors"]}
    after_map = {row["sector"]: row for row in after_sectors["sectors"]}
    sector = context["positions"].get(symbol, {}).get("sector", "Other")
    worsening = [
        {"without_trade": _trade_row(before_map[name], symbol), "with_trade": row}
        for name, row in after_map.items()
        if name != sector and row["breach_pp"] > before_map[name]["breach_pp"] + TOLERANCE
    ]
    comparisons = [(_position_row(context, without, symbol, "WITHOUT_TRADE"),
                    _position_row(context, scheduled, symbol, "PROJECTED_SCHEDULED"))]
    if sector in before_map or sector in after_map:
        template = before_map.get(sector) or after_map[sector]
        comparisons.append((_sector_row(context, without, template, "WITHOUT_TRADE"),
                            _sector_row(context, scheduled, template, "PROJECTED_SCHEDULED")))
    effects = []
    for before, after in comparisons:
        reduction = before["breach_pp"] - after["breach_pp"]
        repairs = (before["observed_pct"] is not None and after["observed_pct"] is not None
                   and reduction > TOLERANCE)
        effects.append({
            "without_trade": _trade_row(before, symbol),
            "with_trade": after,
            "improvement_pp": reduction if repairs else 0,
            "repair": ("PARTIAL_REPAIR" if after["breach_pp"] else "FULL_REPAIR")
                      if repairs else "NO_MEASURABLE_REPAIR",
            "scheduled_change": change,
            "worsened_other_breaches": worsening,
        })
    # Buying elsewhere can dilute a breach without increasing sales.
    for name, before in before_map.items():
        after = after_map.get(name)
        if name != sector and after and before["breach_pp"] > after["breach_pp"] + TOLERANCE:
            effects.append({
                "without_trade": _trade_row(before, symbol), "with_trade": after,
                "improvement_pp": before["breach_pp"] - after["breach_pp"],
                "repair": "PARTIAL_REPAIR" if after["breach_pp"] else "FULL_REPAIR",
                "scheduled_change": change,
                "worsened_other_breaches": worsening,
            })
    return effects


def _schedule(repairs, sales, buys, spendable_cash, budget):
    """Reserve repairs first. Keep the buy group only if funded within turnover."""
    changes = {symbol: -amount for symbol, amount in repairs.items() if amount > 0}
    if not buys:
        return changes, True
    buy_total = sum(buys.values())
    released = sum(repairs.values())
    gap = ceil(max(0, buy_total - spendable_cash - released) * 100 - TOLERANCE) / 100
    if released + buy_total + gap > budget + TOLERANCE:
        return changes, False
    funding = {}
    for symbol in sorted(sales, key=lambda symbol: (sales[symbol] - repairs.get(symbol, 0), symbol)):
        extra = min(max(0.0, sales[symbol] - repairs.get(symbol, 0)), gap)
        if extra > TOLERANCE:
            funding[symbol] = extra
            gap -= extra
    if gap > TOLERANCE:
        return changes, False
    for symbol, amount in funding.items():
        changes[symbol] = changes.get(symbol, 0) - amount
    return {**changes, **buys}, True


def optimize_concentration_execution(payload, summary, cash):
    policy = payload.get("active_policy") or {}
    context = policy.get("concentration") or {}
    sector_advisory = sector_caps_are_advisory(policy)
    muji_v2 = optimizer_policy_mode(policy) == OPTIMIZER_POLICY_MUJI_V2
    if context.get("evidence_version") != EVIDENCE_VERSION or policy.get("hard_policy_unavailable"):
        deferred = [
            OptimizedTrade(
                symbol=row["symbol"], action=row["action"], reason="PORTFOLIO_IMPROVEMENT",
                necessity="DISCRETIONARY", execution_role="NOT_NEEDED_TODAY", execution_state="DEFERRED",
                full_recommended_amount=abs(float(row.get("estimated_amount") or 0)), executed_amount=0,
                evidence_status="UNVERIFIED" if muji_v2 else "NOT_APPLICABLE",
                note="Human Review · frozen policy evidence unavailable.",
            )
            for row in payload.get("target_allocations", [])
            if row.get("action") in ("SELL", "REDUCE")
        ]
        return ExecutionOptimizationResult(
            cash_available=cash, total_buy_deployment=0, funding_gap=0, trades=deferred,
            idle_cash_after=cash, policy_review_reasons=["MISSING_POLICY_EVIDENCE"],
            scheduled_buys={},
            scheduled_sector_evaluation=(evaluate_frozen_sectors(
                context, current_values(context["positions"]), "PROJECTED_SCHEDULED",
            ) if sector_advisory and context.get("positions") is not None else None),
        )
    positions = context["positions"]
    values = current_values(positions)
    allocs = {row["symbol"]: row for row in payload.get("target_allocations", [])}
    sales = {}
    buys = {}
    invalid_directions = set()
    for group in ("sell", "reduce", "new_position", "accumulate"):
        for entry in summary.get(group, []):
            symbol = entry["symbol"]
            row = allocs[symbol]
            if not muji_v2:
                amount = abs(float(row.get("estimated_amount") or 0))
                if group == "sell":
                    sales[symbol] = _floor_money(values.get(symbol, 0.0))
                elif group == "reduce":
                    sales[symbol] = _floor_money(min(amount, values.get(symbol, 0.0)))
                elif amount:
                    buys[symbol] = _floor_money(amount)
                continue
            try:
                signed_amount = float(row.get("estimated_amount") or 0)
            except (TypeError, ValueError):
                signed_amount = float("nan")
            if not isfinite(signed_amount):
                invalid_directions.add(symbol)
                continue
            amount = abs(signed_amount)
            if group == "sell":
                if values.get(symbol, 0.0) > 0 and signed_amount < 0:
                    sales[symbol] = _floor_money(values[symbol])
                else:
                    invalid_directions.add(symbol)
            elif group == "reduce":
                if signed_amount < 0 and values.get(symbol, 0.0) > 0:
                    sales[symbol] = _floor_money(min(amount, values[symbol]))
                else:
                    invalid_directions.add(symbol)
            elif signed_amount > 0:
                buys[symbol] = _floor_money(amount)
            else:
                invalid_directions.add(symbol)

    support = _current_support(context, values, sector_advisory=sector_advisory)
    budget = _floor_money(context["nav"] * context["turnover_cap"] / 100)
    cash_floor = (policy.get("hard_constraints") or {}).get("min_cash_pct", 0)
    spendable_cash = cash - context["nav"] * cash_floor / 100
    review = set()
    if muji_v2 and invalid_directions:
        review.add("INVALID_TRADE_DIRECTION_OR_AMOUNT")
    if context["current"]["estimated_symbols"]:
        review.add("ESTIMATED_PRICES")
    if any(symbol not in positions or positions[symbol]["price"] is None for symbol in buys):
        review.add("ESTIMATED_PRICES")
    current_breach_count = sum(row["breach_pp"] > 0 for row in context["current"]["sectors"])
    if current_breach_count and _uncertain_sector_membership(context, values):
        review.add("UNCERTAIN_SECTOR_CLASSIFICATION")
        current_breach_count = 0
    if sector_advisory:
        current_breach_count = 0
    current_breach_count += sum(_position_row(context, values, symbol, "CURRENT")["breach_pp"] > 0
                                for symbol in values)
    if current_breach_count > len(support) and "ESTIMATED_PRICES" not in review:
        review.add("MISSING_POLICY_EVIDENCE")

    # MUJI V2 can verify an upstream SELL signal from frozen holdings. A model
    # label or explanation cannot verify its own investment evidence.
    verified_sales = {
        symbol for symbol in sales
        if positions.get(symbol, {}).get("sell_signal") is True
        and allocs[symbol].get("decision_basis") not in ("SECTOR_ADVISORY", "CONCENTRATION_ADVISORY")
    } if muji_v2 else set()

    # Allocate NAV repairs first. Sector sizing starts from the isolated current
    # repair amount and is validated against the complete scheduled plan below.
    repairs = {}
    for symbol in sorted(sales) if not muji_v2 else ():
        row = support.get(("NAV", symbol))
        amount = min(sales[symbol], _floor_money(_supported_amount(row))) if row else 0
        repairs[symbol] = min(amount, max(0.0, budget - sum(repairs.values())))
    nav_repairs = dict(repairs)
    if not sector_advisory:
        sector_reserved = {}
        for symbol, amount in repairs.items():
            sector = positions.get(symbol, {}).get("sector")
            sector_reserved[sector] = sector_reserved.get(sector, 0) + amount
        for symbol in sorted(sales):
            sector = positions.get(symbol, {}).get("sector")
            row = support.get(("EQUITY", sector))
            if row:
                available = _floor_money(_supported_amount(row) - sector_reserved.get(sector, 0))
                extra = min(sales[symbol] - repairs[symbol], available, max(0.0, budget - sum(repairs.values())))
                repairs[symbol] += extra
                sector_reserved[sector] = sector_reserved.get(sector, 0) + extra

    emergency_buy_freeze = sector_advisory and bool(policy.get("emergency_override"))
    # A structured thesis proposal or independently frozen SELL signal may
    # fund buys. A sale with no supported basis remains visible as deferred.
    thesis_sales = verified_sales if muji_v2 else {
        symbol for symbol in sales
        if allocs[symbol].get("decision_basis") == "INVESTMENT_THESIS"
        or (allocs[symbol].get("decision_basis") is None and positions.get(symbol, {}).get("sell_signal") is True)
    } if sector_advisory else set()
    funding_sales = {symbol: sales[symbol] for symbol in thesis_sales} if sector_advisory else sales

    def evaluate(repair_amounts):
        eligible_buys = {} if emergency_buy_freeze else buys
        changes, funded = _schedule(repair_amounts, funding_sales, eligible_buys, spendable_cash, budget)
        if emergency_buy_freeze and buys:
            funded = False
        scheduled = {**values, **{symbol: values.get(symbol, 0) + change
                                 for symbol, change in changes.items()}}
        evaluation = evaluate_frozen_sectors(context, scheduled, "PROJECTED_SCHEDULED")
        rejected_buy_evaluation = None
        if buys and funded and not sector_advisory:
            repair_only = {**values, **{symbol: values[symbol] - amount
                                        for symbol, amount in repair_amounts.items() if amount}}
            baseline = evaluate_frozen_sectors(context, repair_only, "REPAIRS_ONLY")
            baseline_breaches = {row["sector"]: row["breach_pp"] for row in baseline["sectors"]}
            worsens = any(row["breach_pp"] > baseline_breaches.get(row["sector"], 0) + TOLERANCE
                          for row in evaluation["sectors"])
            if worsens or policy.get("emergency_override"):
                rejected_buy_evaluation = evaluation
                funded = False
                changes = {symbol: -amount for symbol, amount in repair_amounts.items() if amount}
                scheduled = repair_only
                evaluation = evaluate_frozen_sectors(context, scheduled, "PROJECTED_SCHEDULED")
        effects = {symbol: _effects(context, values, scheduled, symbol, change)
                   for symbol, change in changes.items()}
        verified = {}
        for symbol, amount in repair_amounts.items():
            if not amount:
                continue
            for effect in effects.get(symbol, []):
                before = effect["without_trade"]
                if before["basis"] == "EQUITY" and _uncertain_sector_membership(context, scheduled):
                    continue
                subject = before.get("symbol") if before["basis"] == "NAV" else before["sector"]
                row = support.get((before["basis"], subject))
                if (row and effect["repair"] != "NO_MEASURABLE_REPAIR"
                        and not evaluation["estimated_symbols"]
                        and amount <= _supported_amount(before) + TOLERANCE):
                    required_values = {**scheduled, symbol: values[symbol] - amount}
                    required_result = (_position_row(context, required_values, symbol, "REQUIRED_PORTION")
                                       if before["basis"] == "NAV" else
                                       _sector_row(context, required_values, row, "REQUIRED_PORTION"))
                    if (required_result["observed_pct"] is not None
                            and before["breach_pp"] - required_result["breach_pp"] > TOLERANCE):
                        verified.setdefault(symbol, []).append({
                            **effect, "current_breach": row, "required_amount": amount,
                            "with_required_portion": _trade_row(required_result, symbol),
                        })
        return changes, funded, scheduled, evaluation, effects, verified, rejected_buy_evaluation

    changes, funded, scheduled, evaluation, effects, verified, rejected = evaluate(repairs)
    muji_buys = None
    muji_costs = {}
    muji_cash = None
    if muji_v2:
        position_limit = None
        max_stocks = context.get("max_stocks")   # frozen only by runs that enforce it
        if isinstance(max_stocks, int) and not isinstance(max_stocks, bool) and max_stocks >= 0:
            position_limit = (max_stocks, {symbol for symbol, row in positions.items() if row.get("held")},
                              {entry["symbol"] for entry in summary.get("sell", [])},
                              {symbol: float(allocs[symbol].get("target_weight") or 0) for symbol in buys})
        changes, muji_buys, muji_costs, muji_cash, capped = _muji_schedule(
            sales, buys, verified_sales, values, cash, spendable_cash, budget, emergency_buy_freeze,
            position_limit,
        )
        admitted = {symbol: amount for symbol, amount in buys.items() if symbol not in capped}
        funded = not admitted or sum(muji_buys.values()) >= sum(admitted.values()) - TOLERANCE
        if capped and not emergency_buy_freeze:
            review.add("MAX_STOCKS_LIMIT")
        scheduled = {**values, **{symbol: values.get(symbol, 0) + change for symbol, change in changes.items()}}
        evaluation = evaluate_frozen_sectors(context, scheduled, "PROJECTED_SCHEDULED")
        effects = {symbol: _effects(context, values, scheduled, symbol, change)
                   for symbol, change in changes.items()}
        verified = {}
        rejected = None
    if any(amount > 0 and symbol not in verified for symbol, amount in repairs.items()):
        # Interacting repairs can make the isolated estimate ambiguous. Use a
        # bounded fallback and leave the unresolved size for human review.
        review.add("AMBIGUOUS_REPAIR_AMOUNT")
        repairs = nav_repairs
        changes, funded, scheduled, evaluation, effects, verified, rejected = evaluate(repairs)
        if any(amount > 0 and symbol not in verified for symbol, amount in repairs.items()):
            repairs = {}
            changes, funded, scheduled, evaluation, effects, verified, rejected = evaluate(repairs)

    if buys and not funded:
        if emergency_buy_freeze:
            review.add("EMERGENCY_BUY_FREEZE")
        else:
            review.add("BUY_POLICY" if rejected is not None else "BUY_FUNDING_OR_TURNOVER")
    target = context.get("projected_target") or {}
    if any(row["breach_pp"] for row in target.get("sectors", [])):
        target_values = project_targets(positions, list(allocs.values()), context["target_nav"])
        if _uncertain_sector_membership(context, target_values):
            review.add("UNCERTAIN_SECTOR_CLASSIFICATION")
    if any(row["breach_pp"] for row in evaluation["sectors"]) and _uncertain_sector_membership(context, scheduled):
        review.add("UNCERTAIN_SECTOR_CLASSIFICATION")
    if evaluation["infeasible_within_occupied_sectors"]:
        review.add("INFEASIBLE_SECTOR_CAPS")
    if any(row["breach_pp"] for row in evaluation["sectors"]):
        review.add("RESIDUAL_SECTOR_BREACH")
    position_breaches = [row for symbol in scheduled
                         if (row := _position_row(context, scheduled, symbol, "PROJECTED_SCHEDULED"))["breach_pp"]]
    if position_breaches:
        review.add("RESIDUAL_POSITION_BREACH")
    if any(effect["worsened_other_breaches"] for rows in effects.values() for effect in rows):
        review.add("WORSENS_OTHER_SECTOR_BREACH")
    if not evaluation["applicable"] and context["current"]["applicable"]:
        review.add("NO_INVESTED_EQUITY_AFTER_SCHEDULE")

    trades = []
    sale_rows = sales if not muji_v2 else {**{symbol: 0.0 for symbol in invalid_directions
                                              if allocs.get(symbol, {}).get("action") in ("SELL", "REDUCE")}, **sales}
    for symbol, planned in sale_rows.items():
        released = -changes.get(symbol, 0)
        required = 0 if muji_v2 else repairs.get(symbol, 0) if symbol in verified else 0
        sector = positions.get(symbol, {}).get("sector", "Other")
        trades.append(OptimizedTrade(
            symbol=symbol, action=allocs[symbol]["action"], sector=sector,
            sector_classification=positions.get(symbol, {}).get("sector_classification"),
            reason=("POLICY_ENFORCEMENT" if required else
                    "INVESTMENT_THESIS" if symbol in thesis_sales
                    else "PORTFOLIO_IMPROVEMENT"),
            necessity="NECESSARY" if required else "DISCRETIONARY",
            execution_role="STANDALONE" if (required or (muji_v2 and released and
                            sum(buys.values()) <= max(0.0, spendable_cash) + TOLERANCE)) else "FUNDING_SOURCE" if released else "NOT_NEEDED_TODAY",
            execution_state="DEFERRED" if not released else "FULL" if released >= planned else "SCALED",
            full_recommended_amount=planned, executed_amount=round(released, 2),
            required_amount=round(required, 2), discretionary_amount=round(planned - required, 2),
            policy_evidence=verified.get(symbol, []),
            evidence_status=("UNVERIFIED" if muji_v2 and symbol not in verified_sales
                             else "VERIFIED_POLICY_REPAIR" if required else "NOT_APPLICABLE"),
            funding_basis=("INDEPENDENT_FROZEN_SELL_SIGNAL" if muji_v2 and released else
                           "UNVERIFIED" if muji_v2 else None),
            original_action=allocs[symbol].get("original_action", allocs[symbol].get("action")) if muji_v2 else None,
            original_rationale=allocs[symbol].get("reason") if muji_v2 else None,
            scheduled_cash_impact=round(released - muji_costs.get(symbol, 0), 2) if muji_v2 else None,
            deferral_reason=("INVALID_TRADE_DIRECTION_OR_AMOUNT" if symbol in invalid_directions else
                             "UNVERIFIED_SELL_EVIDENCE" if symbol not in verified_sales else
                             "TURNOVER_LIMIT") if muji_v2 and not released else None,
            note=("Invalid or opposite-side trade amount. Deferred for human review."
                  if muji_v2 and symbol in invalid_directions else
                  "Investment evidence unverified. Deferred for human review."
                  if muji_v2 and symbol not in verified_sales
                  else "Policy repair amount for human review." if required
                  else "Funding supported by a frozen SELL signal." if muji_v2 and released
                  else "Discretionary funding for proposed buys." if released else "Deferred for human review."),
        ))
    scheduled_buys = muji_buys if muji_v2 else buys if funded else {}
    deployment = sum(scheduled_buys.values())
    return ExecutionOptimizationResult(
        cash_available=round(cash, 2), total_buy_deployment=round(deployment, 2),
        funding_gap=round(max(0, deployment - spendable_cash - sum(-change for change in changes.values() if change < 0)), 2) if muji_v2 else round(max(0, deployment - spendable_cash), 2) if deployment else 0,
        trades=trades, idle_cash_after=muji_cash if muji_v2 else round(cash - sum(changes.values()), 2),
        scheduled_buys=scheduled_buys, trade_effects=effects, scheduled_sector_evaluation=evaluation,
        rejected_buy_sector_evaluation=rejected,
        scheduled_position_breaches=position_breaches,
        valuation_nav=context["nav"],
        effective_turnover_cap_pct=context["turnover_cap"],
        scheduled_turnover_pct=sum(abs(change) for change in changes.values()) / context["nav"] * 100
        if context["nav"] > 0 else 0,
        policy_review_reasons=sorted(review),
        scheduled_changes={symbol: round(change, 2) for symbol, change in changes.items()} if muji_v2 else None,
        estimated_trade_costs=muji_costs if muji_v2 else None,
        funding_assumptions=(["Advisory THB monetary plan; estimated trading friction is 0.15% of gross value per side, not a broker fee quote.",
                              "Settlement and currency availability are unverified; no order has been executed."]
                             if muji_v2 else None),
    )
