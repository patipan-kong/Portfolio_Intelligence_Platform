"""Slice 3.1 candidate preparation is evidence, never strategy selection."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.optimizer.strategic_candidates import prepare_candidates


HOLDINGS = [
    {"symbol": "AAA", "shares": 60, "current_price": 10, "weight_pct": 60,
     "signal": "SELL", "fa_score": 30},
    {"symbol": "BBB", "shares": 20, "current_price": 10, "weight_pct": 20,
     "signal": "HOLD", "fa_score": 70},
]


def proposal(*, family="RAISE_CASH", refs=None, sell_basis="INVESTMENT_THESIS"):
    return {
        "strategy_family": family, "observed_evidence_refs": refs or ["symbol:AAA:signal"],
        "portfolio_assessment": "Model proposes raising cash because the AAA thesis weakened.",
        "target_cash_weight": 80,
        "target_allocations": [
            {"symbol": "AAA", "action": "SELL", "current_weight": 60,
             "target_weight": 0, "allocation_change_percent": -60,
             "decision_basis": sell_basis, "reason": "Model thesis"},
            {"symbol": "BBB", "action": "HOLD", "current_weight": 20,
             "target_weight": 20, "allocation_change_percent": 0},
        ],
    }


def test_hold_is_frozen_and_optional_family_is_not_mandatory():
    evidence = prepare_candidates(HOLDINGS, [], 200, {})
    assert evidence["status"] == "PREPARED_NOT_SELECTED"
    assert [candidate["family"] for candidate in evidence["candidates"]] == ["HOLD"]
    hold = evidence["candidates"][0]
    assert hold["eligibility_status"] == "ELIGIBLE"
    assert [row["target_weight"] for row in hold["proposed_allocations"]] == [60, 20]
    assert hold["cash_intent"] == {"kind": "KEEP_CURRENT", "amount": 200}


def test_missing_nav_never_uses_model_weights_for_hold():
    missing = [{**HOLDINGS[0], "current_price": None}, HOLDINGS[1]]
    hold = prepare_candidates(missing, [], 200, proposal())["candidates"][0]
    assert hold["eligibility_status"] == "UNVERIFIED"
    assert hold["proposed_allocations"] == []
    assert "CURRENT_NAV_UNAVAILABLE" in hold["missing_information"]


def test_supported_sell_is_eligible_but_never_selected_or_funded_by_candidates():
    evidence = prepare_candidates(HOLDINGS, [], 200, proposal())
    candidate = evidence["candidates"][1]
    assert candidate["eligibility_status"] == "ELIGIBLE"
    assert candidate["observed_evidence_refs"] == {"symbol:AAA:signal": "SELL"}
    assert "selected_candidate_id" not in evidence
    assert "scheduled_execution" not in evidence
    assert candidate["id"] == prepare_candidates(HOLDINGS, [], 200, proposal())["candidates"][1]["id"]


def test_candidate_allocations_are_frozen_from_later_challenger_mutation():
    challenger = proposal()
    candidate = prepare_candidates(HOLDINGS, [], 200, challenger)["candidates"][1]
    challenger["target_allocations"][0]["target_weight"] = 40
    assert candidate["proposed_allocations"][0]["target_weight"] == 0


def test_model_label_and_advisory_reason_do_not_verify_sale():
    holdings = [{**HOLDINGS[0], "signal": "HOLD"}, HOLDINGS[1]]
    candidate = prepare_candidates(holdings, [], 200, proposal(
        refs=["position:AAA:cap"], sell_basis="CONCENTRATION_ADVISORY",
    ))["candidates"][1]
    assert candidate["eligibility_status"] == "UNVERIFIED"
    assert "UNKNOWN_EVIDENCE_REF" in candidate["missing_information"]
    assert "UNVERIFIED_SELL:AAA" in candidate["missing_information"]
    assert candidate["model_rationale"].startswith("Model proposes")


def test_incomplete_opposite_direction_and_nonfinite_proposals_are_ineligible():
    incomplete = proposal()
    incomplete["target_allocations"] = incomplete["target_allocations"][:1]
    assert prepare_candidates(HOLDINGS, [], 200, incomplete)["candidates"][1]["eligibility_status"] == "INELIGIBLE"
    opposite = proposal()
    opposite["target_allocations"][0]["allocation_change_percent"] = 60
    assert prepare_candidates(HOLDINGS, [], 200, opposite)["candidates"][1]["eligibility_status"] == "INELIGIBLE"
    nonfinite = proposal()
    nonfinite["target_cash_weight"] = float("nan")
    assert prepare_candidates(HOLDINGS, [], 200, nonfinite)["candidates"][1]["eligibility_status"] == "INELIGIBLE"
    mislabeled = proposal(family="GROWTH_ROTATION")
    assert "FAMILY_ACTION_CONFLICT" in prepare_candidates(HOLDINGS, [], 200, mislabeled)["candidates"][1]["eligibility_reasons"]


def test_goal_facts_require_explicit_selected_context():
    goals = {"contract_version": "wealth.decision-goal-context.v2",
             "goals": [{"id": 7, "target_date": "2030-01-01", "funding_gap": 5000}]}
    item = proposal(refs=["goal:7:target_date"])
    assert prepare_candidates(HOLDINGS, [], 200, item)["candidates"][1]["eligibility_status"] == "UNVERIFIED"
    supported = prepare_candidates(HOLDINGS, [], 200, item, goals=goals)
    assert supported["goal_context_version"] == goals["contract_version"]
    assert supported["candidates"][1]["eligibility_status"] == "ELIGIBLE"
