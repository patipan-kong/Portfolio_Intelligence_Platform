"""FIX 2 policy replay, using frozen values rather than the Dev database."""

import json

import pytest

from agents.optimizer import _limit_sector_buys, _make_envelope_from_dict
from services.evaluation.plan_grader import derive_full_plan
from services.optimizer.execution_optimizer import optimize_execution_for_payload
from services.optimizer.policy_engine import compute_policy, compute_policy_alignment_score
from services.optimizer.sector_policy import (
    attach_target_evaluation, current_values, evaluate_frozen_sectors, freeze_concentration,
    project_targets,
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
        turnover=100, cash_floor=0, emergency=False):
    nav = cash + sum(row["avg_cost"] for row in holdings)
    policy = {
        "hard_constraints": {"max_sector_pct": 100, "max_single_position_pct": position,
                             "max_turnover_pct": turnover, "min_cash_pct": cash_floor},
        "resolved_sector_limits": caps or {},
        "sector_limit_sources": {"Technology": "EMERGENCY_OVERRIDE", "Healthcare": "REGIME_POLICY"},
        "emergency_override": emergency,
    }
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
