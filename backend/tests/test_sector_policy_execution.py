"""FIX 2 policy replay, using frozen values rather than the Dev database."""

import json

import pytest

from agents.optimizer import _limit_sector_buys, _make_envelope_from_dict
from services.evaluation.plan_grader import compute_plan_grade, derive_full_plan
from services.optimizer.execution_optimizer import optimize_execution_for_payload
from services.optimizer.policy_engine import compute_policy, compute_policy_alignment_score
from services.optimizer.sector_policy import (
    OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY, UnsupportedOptimizerPolicyEvidence,
    attach_target_evaluation, current_values, evaluate_frozen_sectors, freeze_concentration,
    optimizer_policy_mode, project_targets,
)
from services.optimizer_action_summary import build_action_summary


def holding(symbol, sector, value, quoted=True):
    return {"symbol": symbol, "sector": sector, "shares": 1,
            "current_price": value if quoted else None, "avg_cost": value}


def allocation(symbol, action, target, current, amount):
    return {"symbol": symbol, "action": action, "target_weight": target,
            "current_weight": current, "allocation_change_percent": target - current,
            "estimated_amount": amount}


def run(holdings, allocations=(), *, cash=0, caps=None, candidates=(), position=100,
        turnover=100, cash_floor=0, emergency=False, sector_advisory=False):
    nav = cash + sum(row["avg_cost"] for row in holdings)
    policy = {
        "hard_constraints": {"max_sector_pct": 100, "max_single_position_pct": position,
                             "max_turnover_pct": turnover, "min_cash_pct": cash_floor},
        "resolved_sector_limits": caps or {},
        "sector_limit_sources": {"Technology": "EMERGENCY_OVERRIDE", "Healthcare": "REGIME_POLICY"},
        "emergency_override": emergency,
    }
    if sector_advisory:
        policy["sector_policy_mode"] = SECTOR_POLICY_ADVISORY
    policy["concentration"] = freeze_concentration(holdings, candidates, policy, nav)
    result = {"active_policy": policy, "total_value": nav, "cash_balance": cash,
              "target_allocations": list(allocations)}
    attach_target_evaluation(result)
    return result


def schedule(result):
    return optimize_execution_for_payload(result, build_action_summary(result["target_allocations"]))


def sectors(evaluation):
    return {row["sector"]: row for row in evaluation["sectors"]}


@pytest.fixture
def replay_239():
    holdings = [
        holding("NVDA01.BK", "Technology", 89000), holding("MICRON01.BK", "Technology", 73000),
        holding("BH.BK", "Healthcare", 158800), holding("GULF.BK", "Utilities", 122500),
        holding("GOOGL01.BK", "Communication Services", 57000),
    ]
    allocations = [
        allocation("BH.BK", "REDUCE", 13.5, 21.50, -59086),
        allocation("GULF.BK", "REDUCE", 13.5, 16.59, -22822),
        allocation("NVDA01.BK", "REDUCE", 4.2, 12.05, -57979),
        allocation("GOOGL01.BK", "REDUCE", 4.7, 7.72, -22305),
        allocation("MICRON01.BK", "HOLD", 9.88, 9.88, 0),
    ]
    return run(holdings, allocations, cash=238280.22035, position=15, turnover=21.6,
               emergency=True, caps={"Technology": 25, "Healthcare": 24.5, "Utilities": 25, "Other": 21})


def test_run_239_current_target_and_scheduled(replay_239):
    context = replay_239["active_policy"]["concentration"]
    current = context["current"]
    target = context["projected_target"]
    assert current["denominator"] == 500300
    assert target["denominator"] == pytest.approx(338150.29910565)
    assert sectors(current)["Technology"]["observed_pct"] == pytest.approx(32.3805717)
    assert sectors(current)["Healthcare"]["limit_pct"] == 24.5
    assert sectors(current)["Utilities"]["breach_pp"] == 0
    assert sectors(current)["Other"]["numerator"] == 57000
    assert {name for name, row in sectors(target).items() if row["breach_pp"]} == {
        "Technology", "Healthcare", "Utilities",
    }
    assert sectors(target)["Technology"]["observed_pct"] == pytest.approx(30.7616, abs=0.0001)
    assert target["occupied_cap_sum_pct"] == 95.5
    plan = schedule(replay_239)
    scheduled = plan.scheduled_sector_evaluation
    assert scheduled["denominator"] == pytest.approx(391340.75)
    assert {name for name, row in sectors(scheduled).items() if row["breach_pp"]} == {
        "Technology", "Healthcare", "Utilities",
    }
    assert "INFEASIBLE_SECTOR_CAPS" in plan.policy_review_reasons
    assert "WORSENS_OTHER_SECTOR_BREACH" in plan.policy_review_reasons
    assert plan.scheduled_turnover_pct < 21.6
    trades = {trade.symbol: trade for trade in plan.trades}
    assert trades["BH.BK"].required_amount == 48012.96
    assert trades["GULF.BK"].required_amount == 11712.96
    nvda = trades["NVDA01.BK"]
    assert nvda.required_amount == 49233.33
    assert nvda.discretionary_amount == 8745.67
    [evidence] = nvda.policy_evidence
    assert evidence["current_breach"]["basis"] == "EQUITY"
    assert evidence["current_breach"]["binding_source"] == "EMERGENCY_OVERRIDE"
    assert evidence["repair"] == "PARTIAL_REPAIR"
    assert evidence["with_trade"]["breach_pp"] > 0
    assert evidence["without_trade"]["observed_pct"] > evidence["with_trade"]["observed_pct"]
    assert trades["GOOGL01.BK"].required_amount == 0


def test_cash_and_omitted_positions_do_not_change_sector_basis():
    holdings = [holding("T", "Technology", 30000), holding("U", "Utilities", 70000)]
    caps = {"Technology": 25}
    for cash in (0, 900000):
        result = run(holdings, [allocation("T", "HOLD", 0, 0, 0)], cash=cash, caps=caps)
        context = result["active_policy"]["concentration"]
        for stage in ("current", "projected_target"):
            assert sectors(context[stage])["Technology"]["observed_pct"] == 30
        assert schedule(result).scheduled_sector_evaluation["denominator"] == 100000
    positions = context["positions"]
    sold = project_targets(positions, [allocation("T", "SELL", 0, 3, -30000)], context["target_nav"])
    assert sold == {"T": 0, "U": 70000}
    added = project_targets(positions, [allocation("U", "BUY", 9, 7, 20000)], context["target_nav"])
    assert sectors(evaluate_frozen_sectors(context, added, "PROJECTED_TARGET"))["Technology"]["observed_pct"] == 25


def test_zero_equity_first_buy_and_effective_cap_are_checked():
    result = run([], [allocation("T", "BUY", 10, 0, 10000)], cash=100000,
                 candidates=[{"symbol": "T", "sector": "Technology", "current_price": 100}],
                 caps={"Technology": 24.5})
    policy = result["active_policy"]
    context = policy["concentration"]
    assert not context["current"]["applicable"]
    assert context["current"]["sectors"] == []
    target = sectors(context["projected_target"])["Technology"]
    assert target["observed_pct"] == 100 and target["limit_pct"] == 24.5
    details = compute_policy_alignment_score(
        result["target_allocations"], _make_envelope_from_dict(policy), 100000,
        frozen_positions=context["positions"],
    )[4]
    assert details[0]["policy_evidence"] == target
    plan = schedule(result)
    assert not plan.scheduled_sector_evaluation["applicable"]
    assert plan.scheduled_buys == {}
    assert sectors(plan.rejected_buy_sector_evaluation)["Technology"]["observed_pct"] == 100
    _limit_sector_buys(result["target_allocations"], 100000, policy, context["positions"])
    assert result["target_allocations"][0]["target_weight"] == 0


def test_emergency_without_breach_does_not_require_a_sell():
    holdings = [holding(symbol, sector, 20) for symbol, sector in
                zip("THUFO", ("Technology", "Healthcare", "Utilities", "Financial", "Other"))]
    envelope = compute_policy(None, {"vol_z_score": 3.3}, holdings)
    assert envelope.emergency_override and envelope.hard_constraints.max_sector_pct == 25
    result = run(holdings, [allocation("T", "SELL", 0, 10, -20)], cash=100, position=15,
                 caps={row["sector"]: 25 for row in holdings}, emergency=True)
    result["active_policy"]["violations"] = ["SECTOR_BREACH: Technology"]
    trade = schedule(result).trades[0]
    assert trade.required_amount == 0 and trade.execution_state == "DEFERRED"


@pytest.mark.parametrize("price_available, evidence_available, review", [
    (False, True, "ESTIMATED_PRICES"), (True, False, "MISSING_POLICY_EVIDENCE"),
])
def test_unverified_denominator_cannot_support_required(price_available, evidence_available, review):
    result = run([holding("T", "Technology", 60), holding("U", "Utilities", 40, price_available)],
                 [allocation("T", "SELL", 0, 60, -60)], caps={"Technology": 45}, position=50)
    if not evidence_available:
        result["active_policy"]["concentration"]["current_breaches"] = []
    plan = schedule(result)
    assert plan.trades[0].required_amount == 0
    assert plan.trades[0].policy_evidence == []
    assert review in plan.policy_review_reasons


def test_turnover_limits_repair_and_defers_unfunded_buys():
    result = run([holding("T", "Technology", 60000), holding("U", "Utilities", 40000)],
                 [allocation("T", "REDUCE", 45, 60, -15000), allocation("N", "BUY", 10, 0, 10000)],
                 candidates=[{"symbol": "N", "sector": "Financial", "current_price": 100}],
                 position=50, turnover=5)
    plan = schedule(result)
    assert plan.scheduled_turnover_pct == 5
    assert plan.scheduled_buys == {}
    assert "BUY_FUNDING_OR_TURNOVER" in plan.policy_review_reasons
    [trade] = plan.trades
    assert trade.required_amount == 5000 and trade.discretionary_amount == 10000
    [evidence] = trade.policy_evidence
    assert evidence["repair"] == "PARTIAL_REPAIR"
    assert evidence["with_trade"]["breach_pp"] == pytest.approx(5)


def test_frozen_schedule_and_report_card_use_same_evidence(replay_239):
    live = schedule(replay_239).model_dump()
    saved = json.loads(json.dumps(replay_239))
    policy = saved["active_policy"]
    policy["scheduled_execution"] = live
    # Replay is independent of the current action-summary rules.
    assert optimize_execution_for_payload(saved, {}).model_dump() == live
    report = derive_full_plan(saved["target_allocations"], saved["cash_balance"], policy_provenance=policy)
    assert report["execution_optimization"].model_dump() == live
    required = next(trade for trade in live["trades"] if trade["required_amount"])
    required["policy_evidence"] = [{}]
    incomplete = optimize_execution_for_payload(saved, {})
    assert "MISSING_POLICY_EVIDENCE" in incomplete.policy_review_reasons
    assert next(trade for trade in incomplete.trades if trade.symbol == required["symbol"]).required_amount == 0


def test_only_supported_portion_of_funding_sale_is_required():
    result = run([holding("T", "Technology", 60), holding("U", "Utilities", 40)],
                 [allocation("T", "REDUCE", 10, 60, -50), allocation("N", "BUY", 30, 0, 30)],
                 candidates=[{"symbol": "N", "sector": "Financial", "current_price": 100}],
                 position=50)
    plan = schedule(result)
    assert plan.scheduled_buys == {"N": 30}
    assert plan.scheduled_turnover_pct == 60
    [trade] = plan.trades
    assert trade.executed_amount == 30
    assert trade.required_amount == 10 and trade.discretionary_amount == 40
    [evidence] = trade.policy_evidence
    assert evidence["repair"] == "FULL_REPAIR"
    assert evidence["with_required_portion"]["numerator"] == 50
    assert evidence["with_trade"]["numerator"] == 30
    assert "N" in plan.trade_effects


def test_advisory_replay_239_keeps_only_nav_repairs(replay_239):
    historical = schedule(replay_239).model_dump()
    policy = replay_239["active_policy"]
    policy["sector_policy_mode"] = SECTOR_POLICY_ADVISORY
    plan = schedule(replay_239)
    trades = {trade.symbol: trade for trade in plan.trades}
    assert {symbol: trade.required_amount for symbol, trade in trades.items()} == {
        "BH.BK": 48012.96, "GULF.BK": 11712.96, "NVDA01.BK": 0, "GOOGL01.BK": 0,
    }
    assert trades["NVDA01.BK"].executed_amount == 0
    assert plan.scheduled_turnover_pct == pytest.approx(8.08658536)
    assert plan.scheduled_sector_evaluation["denominator"] == pytest.approx(440574.08)
    assert sectors(plan.scheduled_sector_evaluation)["Technology"]["observed_pct"] == pytest.approx(36.7702067)
    assert "RESIDUAL_SECTOR_BREACH" in plan.policy_review_reasons
    policy.pop("sector_policy_mode")
    policy["scheduled_execution"] = historical
    assert schedule(replay_239).model_dump() == historical


@pytest.mark.parametrize(
    "policy, expected",
    [
        ({}, None),
        ({"execution_policy_version": "wealth.policy-evidence.v1"}, None),
        ({"execution_policy_version": "wealth.policy-evidence.v2"}, None),
        ({"sector_policy_mode": SECTOR_POLICY_ADVISORY}, SECTOR_POLICY_ADVISORY),
        ({"sector_policy_mode": SECTOR_POLICY_ADVISORY, "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2},
         OPTIMIZER_POLICY_MUJI_V2),
    ],
)
def test_optimizer_policy_dispatch_uses_explicit_identity(policy, expected):
    assert optimizer_policy_mode(policy) == expected


@pytest.mark.parametrize(
    "markers",
    [
        {"optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2},
        {"sector_policy_mode": SECTOR_POLICY_ADVISORY, "optimizer_policy_mode": None},
        {"sector_policy_mode": SECTOR_POLICY_ADVISORY, "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2.upper()},
        {"sector_policy_mode": "unknown", "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2},
        {"sector_policy_mode": "unknown"},
    ],
)
def test_unsupported_policy_cannot_schedule_or_replay(replay_239, markers):
    policy = replay_239["active_policy"]
    policy["scheduled_execution"] = schedule(replay_239).model_dump()
    policy.update(markers)
    with pytest.raises(UnsupportedOptimizerPolicyEvidence):
        schedule(replay_239)


def test_muji_frozen_slice_one_keeps_sector_advisory_schedule_and_grade(replay_239):
    policy = replay_239["active_policy"]
    policy["sector_policy_mode"] = SECTOR_POLICY_ADVISORY
    old_schedule = schedule(replay_239).model_dump()
    policy["scheduled_execution"] = old_schedule
    grade_args = (replay_239["target_allocations"], replay_239["cash_balance"])
    old_grade = compute_plan_grade(*grade_args, policy_provenance=policy)

    policy["optimizer_policy_mode"] = OPTIMIZER_POLICY_MUJI_V2
    assert schedule(replay_239).model_dump() == old_schedule
    # Re-tagging a v1 schedule does not create V2 monetary evidence or a V2
    # grade. The old stored grade remains untouched by the new dispatch.
    from services.optimizer.sector_policy import UnsupportedOptimizerPolicyEvidence
    with pytest.raises(UnsupportedOptimizerPolicyEvidence):
        compute_plan_grade(*grade_args, policy_provenance=policy)
    legacy_policy = {key: value for key, value in policy.items() if key != "optimizer_policy_mode"}
    assert old_grade == compute_plan_grade(*grade_args, policy_provenance=legacy_policy)
    del policy["scheduled_execution"]
    assert all(trade.executed_amount == trade.required_amount == 0 for trade in schedule(replay_239).trades)


def test_run_239_v1_plan_grade_preserves_recorded_formula(replay_239):
    allocations = replay_239["target_allocations"]
    sector_by_symbol = replay_239["active_policy"]["concentration"]["positions"]
    for row in allocations:
        row["sector"] = sector_by_symbol[row["symbol"]]["sector"]
    grade = compute_plan_grade(
        allocations, replay_239["cash_balance"],
        ["CONCENTRATION_BREACH: BH.BK", "CONCENTRATION_BREACH: GULF.BK", "SECTOR_BREACH: Technology"],
        [{"violation_type": "TURNOVER_BREACH", "proposed_pct": 22.0, "allowed_pct": 21.6}],
    )
    assert grade["necessity_score"] == 75
    assert grade["score"] == 62.13


@pytest.mark.parametrize("with_holdings", [False, True])
@pytest.mark.parametrize("gate", ["eligible", "emergency", "cash", "turnover"])
def test_advisory_buy_still_obeys_hard_gates(with_holdings, gate):
    holdings = [holding("T", "Technology", 10000), holding("U", "Utilities", 30000)] if with_holdings else []
    cash = 60000 if with_holdings else 100000
    result = run(holdings, [allocation("N", "BUY", 10, 0, 10000)], cash=cash,
                 candidates=[{"symbol": "N", "sector": "Technology", "current_price": 100}],
                 caps={"Technology": 24.5}, sector_advisory=True, emergency=gate == "emergency",
                 turnover=5 if gate == "turnover" else 100,
                 cash_floor=(55 if with_holdings else 95) if gate == "cash" else 0)
    plan = schedule(result)
    assert plan.scheduled_buys == ({"N": 10000} if gate == "eligible" else {})
    assert plan.rejected_buy_sector_evaluation is None
    if gate == "eligible":
        tech = sectors(plan.scheduled_sector_evaluation)["Technology"]
        assert tech["observed_pct"] == (40 if with_holdings else 100)
        assert tech["breach_pp"] > 0
    elif gate == "emergency":
        assert "EMERGENCY_BUY_FREEZE" in plan.policy_review_reasons
    else:
        assert "BUY_FUNDING_OR_TURNOVER" in plan.policy_review_reasons


def test_sector_only_trim_cannot_fund_buy_but_thesis_trade_can():
    sell = allocation("T", "SELL", 0, 60, -60000)
    sell["reason"] = "Reduce Technology to its sector threshold"
    result = run([holding("T", "Technology", 60000), holding("U", "Utilities", 40000)],
                 [sell, allocation("N", "BUY", 10, 0, 10000)],
                 candidates=[{"symbol": "N", "sector": "Financial", "current_price": 100}],
                 caps={"Technology": 25}, sector_advisory=True)
    assert schedule(result).scheduled_buys == {}
    sell["reason"] = "Weakening business outlook"
    assert schedule(result).scheduled_buys == {}
    sell["decision_basis"] = "SECTOR_ADVISORY"
    assert schedule(result).scheduled_buys == {}
    sell["decision_basis"] = "INVESTMENT_THESIS"
    plan = schedule(result)
    assert plan.scheduled_buys == {"N": 10000}
    [trade] = plan.trades
    assert (trade.reason, trade.necessity, trade.executed_amount, trade.required_amount) == (
        "INVESTMENT_THESIS", "DISCRETIONARY", 10000, 0,
    )


def test_untagged_sale_can_fund_buy_with_frozen_sell_signal():
    holdings = [{**holding("T", "Technology", 60000), "signal": "SELL"},
                holding("U", "Utilities", 40000)]
    result = run(holdings, [allocation("T", "SELL", 0, 60, -60000), allocation("N", "BUY", 10, 0, 10000)],
                 candidates=[{"symbol": "N", "sector": "Financial", "current_price": 100}],
                 caps={"Technology": 25}, sector_advisory=True)
    plan = schedule(result)
    assert plan.scheduled_buys == {"N": 10000}
    assert plan.trades[0].reason == "INVESTMENT_THESIS"


@pytest.mark.parametrize("signal", ["HOLD", "SELL"])
def test_muji_mixed_rationale_only_funds_with_independent_frozen_sell_signal(signal):
    sell = allocation("T", "SELL", 0, 60, -60000)
    reason = "Sector exceeds threshold. Earnings are deteriorating."
    sell.update(reason=reason, decision_basis="INVESTMENT_THESIS")
    result = run(
        [{**holding("T", "Technology", 60000), "signal": signal}, holding("U", "Utilities", 40000)],
        [sell, allocation("N", "BUY", 10, 0, 10000)],
        candidates=[{"symbol": "N", "sector": "Financial", "current_price": 100}],
        caps={"Technology": 25}, sector_advisory=True,
    )
    result["active_policy"]["optimizer_policy_mode"] = OPTIMIZER_POLICY_MUJI_V2
    plan = schedule(result)
    assert plan.scheduled_buys == ({"N": 10000} if signal == "SELL" else {})
    assert plan.trades[0].executed_amount == (60000 if signal == "SELL" else 0)
    assert plan.trades[0].required_amount == 0
    assert plan.idle_cash_after == (49895 if signal == "SELL" else 0)
    assert sell["reason"] == reason


def test_muji_verified_sell_only_raises_cash_without_required_repair():
    sell = {**allocation("T", "SELL", 0, 60, -60000), "reason": "Independent frozen SELL signal"}
    result = run(
        [{**holding("T", "Technology", 60000), "signal": "SELL"}, holding("U", "Utilities", 40000)],
        [sell], caps={"Technology": 25}, position=50, sector_advisory=True,
    )
    result["active_policy"]["optimizer_policy_mode"] = OPTIMIZER_POLICY_MUJI_V2
    plan = schedule(result)
    assert plan.scheduled_buys == {}
    assert plan.scheduled_changes == {"T": -60000}
    assert plan.idle_cash_after == 59910
    assert plan.estimated_trade_costs == {"T": 90}
    assert (plan.trades[0].execution_role, plan.trades[0].required_amount) == ("STANDALONE", 0)
    assert plan.trades[0].funding_basis == "INDEPENDENT_FROZEN_SELL_SIGNAL"
    result["active_policy"]["scheduled_execution"] = plan.model_dump()
    assert schedule(result).model_dump() == plan.model_dump()
    grade = compute_plan_grade(result["target_allocations"], result["cash_balance"],
                               policy_provenance={**result["active_policy"], "total_value": result["total_value"]})
    assert grade["grade_version"] == "wealth.plan-grade-muji.v2"
    assert grade["action_evidence_score"] == 100


@pytest.mark.parametrize("action,amount", [("BUY", -10000), ("SELL", 10000), ("REDUCE", 10000),
                                             ("REDUCE", float("nan"))])
def test_muji_opposite_or_invalid_direction_never_reverses(action, amount):
    row = allocation("T", action, 50 if action != "SELL" else 0, 60, amount)
    result = run([{**holding("T", "Technology", 60000), "signal": "SELL"}], [row],
                 sector_advisory=True)
    result["active_policy"]["optimizer_policy_mode"] = OPTIMIZER_POLICY_MUJI_V2
    plan = schedule(result)
    assert plan.scheduled_changes == {}
    assert plan.scheduled_buys == {}
    assert plan.idle_cash_after == 0
    assert "INVALID_TRADE_DIRECTION_OR_AMOUNT" in plan.policy_review_reasons


@pytest.mark.parametrize("sector_advisory", [False, True])
def test_legacy_sale_amount_parsing_is_unchanged(sector_advisory):
    result = run([holding("T", "Technology", 60000)],
                 [allocation("T", "REDUCE", 50, 60, 10000)],
                 sector_advisory=sector_advisory, position=50)
    plan = schedule(result)
    assert plan.trades[0].full_recommended_amount == 10000


def test_muji_unverified_sale_cannot_fund_buy_or_raise_cash():
    result = run([holding("T", "Technology", 60000)],
                 [allocation("T", "SELL", 0, 60, -60000), allocation("N", "BUY", 10, 0, 10000)],
                 candidates=[{"symbol": "N", "sector": "Financial", "current_price": 100}],
                 sector_advisory=True)
    result["active_policy"]["optimizer_policy_mode"] = OPTIMIZER_POLICY_MUJI_V2
    plan = schedule(result)
    assert plan.scheduled_changes == {}
    assert plan.idle_cash_after == 0
    assert plan.trades[0].execution_state == "DEFERRED"
    assert plan.trades[0].evidence_status == "UNVERIFIED"


def test_muji_estimated_net_proceeds_and_buy_cost_reconcile():
    result = run([{**holding("T", "Technology", 60000), "signal": "SELL"}],
                 [allocation("T", "SELL", 0, 100, -60000), allocation("N", "BUY", 60, 0, 36000)],
                 candidates=[{"symbol": "N", "sector": "Financial", "current_price": 100}],
                 sector_advisory=True, turnover=200)
    result["active_policy"]["optimizer_policy_mode"] = OPTIMIZER_POLICY_MUJI_V2
    plan = schedule(result)
    assert plan.scheduled_changes == {"T": -60000, "N": 36000}
    assert plan.estimated_trade_costs == {"T": 90, "N": 54}
    assert plan.idle_cash_after == 23856
    assert plan.trades[0].scheduled_cash_impact == 59910
    assert "not a broker fee quote" in plan.funding_assumptions[0]


def test_muji_cash_limited_buy_scales_without_negative_cash():
    result = run([], [allocation("N", "BUY", 100, 0, 10000)], cash=10000,
                 candidates=[{"symbol": "N", "sector": "Financial", "current_price": 100}],
                 sector_advisory=True)
    result["active_policy"]["optimizer_policy_mode"] = OPTIMIZER_POLICY_MUJI_V2
    plan = schedule(result)
    assert 0 < plan.scheduled_buys["N"] < 10000
    assert plan.idle_cash_after >= 0
    assert plan.scheduled_buys["N"] + plan.estimated_trade_costs["N"] + plan.idle_cash_after == 10000


def test_run_239_sector_tag_cannot_remove_bh_nav_repair(replay_239):
    replay_239["active_policy"]["sector_policy_mode"] = SECTOR_POLICY_ADVISORY
    replay_239["target_allocations"][0]["decision_basis"] = "SECTOR_ADVISORY"
    plan = schedule(replay_239)
    bh = next(trade for trade in plan.trades if trade.symbol == "BH.BK")
    assert (bh.required_amount, bh.executed_amount, bh.discretionary_amount) == (48012.96, 48012.96, 11073.04)
    assert [evidence["current_breach"]["basis"] for evidence in bh.policy_evidence] == ["NAV"]


@pytest.mark.parametrize("reduction,turnover,nav_evidence,expected", [
    (15000, 100, True, 10000),
    (5000, 100, True, 5000),
    (15000, 5, True, 5000),
    (15000, 100, False, 0),
])
def test_sector_tagged_nav_repair_bounds_and_discretionary_funding(reduction, turnover, nav_evidence, expected):
    result = run([holding("T", "Technology", 60000), holding("U", "Utilities", 40000)],
                 [{**allocation("T", "REDUCE", 60 - reduction / 1000, 60, -reduction),
                   "decision_basis": "SECTOR_ADVISORY"}, allocation("N", "BUY", 12, 0, 12000)],
                 candidates=[{"symbol": "N", "sector": "Financial", "current_price": 100}],
                 caps={"Technology": 25}, position=50, turnover=turnover, sector_advisory=True)
    if not nav_evidence:
        result["active_policy"]["concentration"]["current_breaches"][0]["breach_amount"] += 1
    plan = schedule(result)
    [trade] = plan.trades
    assert trade.required_amount == trade.executed_amount == expected
    assert trade.discretionary_amount == reduction - expected
    assert not plan.scheduled_buys


@pytest.mark.parametrize("status", ["provisional", "unresolved"])
@pytest.mark.parametrize("quoted", [False, True])
def test_advisory_classification_is_visible_and_does_not_authorize_required(status, quoted):
    tech = holding("T", "Technology", 60000, quoted)
    tech["sector_classification"] = {
        "sector": "Technology", "classification_source": "provider_metadata",
        "classification_status": status,
    }
    result = run([tech, holding("U", "Utilities", 40000)],
                 [allocation("T", "REDUCE", 30, 60, -30000)], caps={"Technology": 25},
                 sector_advisory=True)
    plan = schedule(result)
    [trade] = plan.trades
    assert trade.required_amount == 0
    row = sectors(plan.scheduled_sector_evaluation)["Technology"]
    assert row["members"][0]["classification_status"] == status
    assert row["breach_pp"] == pytest.approx(35)
    assert ("ESTIMATED_PRICES" in plan.policy_review_reasons) == (not quoted)

def test_run_239_canonical_counterfactual_keeps_nav_repairs(replay_239):
    from services.optimizer.constraint_resolver import resolve_constraints

    resolved = resolve_constraints(
        {"max_sector_pct": 80}, {"default": 30},
        {"regime": "HIGH_VOLATILITY", "vol_z_score": 3.5}, None,
    )
    cap = resolved.sector_limits["Communication Services"]
    assert (cap.user_pref, cap.effective, cap.binding_source) == (30, 21, "REGIME_POLICY")
    assert resolved.global_sector_cap.effective == 25

    policy = replay_239["active_policy"]
    legacy = policy["concentration"]
    holdings = []
    for symbol, row in legacy["positions"].items():
        sector = "Communication Services" if symbol == "GOOGL01.BK" else row["sector"]
        holding_row = holding(symbol, sector, row["value"])
        holding_row["sector_classification"] = {
            "sector": sector, "classification_source": "provider_metadata",
            "classification_status": "provisional",
        }
        holdings.append(holding_row)

    policy["resolved_sector_limits"] = {**legacy["limits"], "Communication Services": cap.effective}
    policy["sector_limit_sources"]["Communication Services"] = cap.binding_source
    policy["concentration"] = freeze_concentration(holdings, [], policy, legacy["nav"])
    attach_target_evaluation(replay_239)
    canonical = policy["concentration"]
    assert canonical["current"]["denominator"] == legacy["current"]["denominator"] == 500300
    assert canonical["projected_target"]["denominator"] == legacy["projected_target"]["denominator"]
    assert sectors(legacy["current"])["Other"]["numerator"] == 57000
    assert sectors(canonical["current"])["Communication Services"]["numerator"] == 57000
    assert canonical["current"]["occupied_cap_sum_pct"] == 95.5

    plan = schedule(replay_239)
    assert plan.scheduled_sector_evaluation["denominator"] == pytest.approx(440574.08)
    assert "UNCERTAIN_SECTOR_CLASSIFICATION" in plan.policy_review_reasons
    assert "INFEASIBLE_SECTOR_CAPS" in plan.policy_review_reasons
    trades = {trade.symbol: trade for trade in plan.trades}
    assert trades["BH.BK"].required_amount == 48012.96
    assert trades["GULF.BK"].required_amount == 11712.96
    nvda = trades["NVDA01.BK"]
    assert nvda.required_amount == nvda.executed_amount == 0
    assert nvda.discretionary_amount == 57979
    assert nvda.execution_state == "DEFERRED"
    scheduled_sales = {trade.symbol: trade.executed_amount for trade in plan.trades if trade.executed_amount}
    assert scheduled_sales == {"BH.BK": 48012.96, "GULF.BK": 11712.96}
    assert plan.scheduled_buys == {}
    assert plan.scheduled_turnover_pct == pytest.approx(sum(scheduled_sales.values()) / legacy["nav"] * 100)
    scheduled = sectors(plan.scheduled_sector_evaluation)
    assert {key: row["breach_pp"] for key, row in scheduled.items() if row["breach_pp"]} == pytest.approx({
        "Technology": 162000 / 440574.08 * 100 - 25,
        "Healthcare": 110787.04 / 440574.08 * 100 - 24.5,
        "Utilities": 110787.04 / 440574.08 * 100 - 25,
    })
    assert trades["GOOGL01.BK"].sector_classification["sector"] == "Communication Services"
    assert {e["current_breach"]["basis"] for trade in plan.trades for e in trade.policy_evidence} == {"NAV"}

    policy["scheduled_execution"] = plan.model_dump()
    saved = json.loads(json.dumps(replay_239))
    assert schedule(saved).model_dump() == plan.model_dump()
