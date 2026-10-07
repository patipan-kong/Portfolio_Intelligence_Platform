"""Advisory Integration V1 (Slice 1): canonical NAV basis, quantity projection, ledger.

Pure tests — no database, no AI, no network.
"""
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from services.advisory_intent_context import (
    ABANDONED, ACTIVE, REPLACED, SUPPRESSED, HeldPosition, ProposalLedger, build_valuation_basis,
    project_quantity,
)
from services.advisory_intent_review import _review
from services.investor_intent import IntentState


def held(symbol="AAA", shares="10", intent=None, status=None):
    return HeldPosition(symbol=symbol, shares=Decimal(shares), holding_started_at="2026-01-05T00:00:00",
                        legacy_allow_swap=True,
                        applicability=status or ("CONFIRMED" if intent else "NO_CONFIRMED_INTENT"),
                        intent=intent, confirmed_at="2026-02-01T00:00:00" if intent else None,
                        historical_intent=None)


def basis(positions, prices, cash="0", currency="THB", raw=None):
    quotes = raw or {p.symbol: {"current_price": prices[p.symbol]} for p in positions}
    return build_valuation_basis(positions, [], quotes, {p.symbol: currency for p in positions}, cash)


NO_DECREASE = IntentState(False, True, "NONE", 7, 1)
NO_INCREASE = IntentState(True, False, "NONE", 8, 1)


def test_equity_and_cash_use_one_nav_basis():
    a, b = held("AAA", "10"), held("BBB", "30")
    v = basis([a, b], {"AAA": 50, "BBB": 10}, cash="500")
    assert v.resolved and v.equity == Decimal("800") and v.nav == Decimal("1300")
    projection = project_quantity(a, v, "HOLD", None)
    # current weight is V0 / N with N = equity + cash, not equity-only.
    assert Decimal(projection["current_weight"]) == Decimal(100) * 500 / 1300


def test_full_sell_with_cash_is_zero_shares_and_minus_held_value():
    a = held("AAA", "10")
    v = basis([a], {"AAA": 50}, cash="1500")
    projection = project_quantity(a, v, "SELL", 0.0)
    assert projection["kind"] == "FULL_EXIT"
    assert projection["proposed_shares"] == "0" and projection["target_amount"] == "0"
    assert projection["delta_amount"] == "-500" and projection["direction"] == "DECREASE"


def test_unchanged_hold_keeps_exact_shares_regardless_of_target():
    a = held("AAA", "10.123456")
    v = basis([a], {"AAA": "33.33"}, cash="1000")
    for target in (None, 0.0, 12.5, 99.0):
        projection = project_quantity(a, v, "HOLD", target)
        assert projection["proposed_shares"] == "10.123456" and projection["delta_amount"] == "0"
        assert projection["direction"] == "NO_CHANGE"


@pytest.mark.parametrize("action,target,direction,shares", [
    ("BUY", 50, "INCREASE", "20"),          # N=2000 → 1000 / 50
    ("ACCUMULATE", 30, "INCREASE", "12"),
    ("REDUCE", 10, "DECREASE", "4"),
])
def test_target_weight_projection_direction(action, target, direction, shares):
    a = held("AAA", "10")
    v = basis([a], {"AAA": 50}, cash="1500")
    projection = project_quantity(a, v, action, target)
    assert projection["resolved"] and projection["direction"] == direction
    assert projection["proposed_shares"] == shares


def test_six_decimal_round_half_up_and_unrounded_internal_evidence():
    a = held("AAA", "1")
    v = basis([a], {"AAA": 3}, cash="2")           # N = 5
    projection = project_quantity(a, v, "BUY", 70)  # 3.5 / 3 = 1.1666666…
    assert projection["proposed_shares"] == "1.166667"
    assert projection["proposed_shares_raw"].startswith("1.1666666666")
    assert projection["target_amount"] == "3.5"


def test_action_and_quantity_disagreeing_is_unresolved_not_relabelled():
    a = held("AAA", "10")
    v = basis([a], {"AAA": 50}, cash="1500")         # current weight 25%
    projection = project_quantity(a, v, "BUY", 20)    # labelled BUY, quantity falls
    assert not projection["resolved"]
    assert projection["reasons"] == ["ACTION_QUANTITY_DIRECTION_MISMATCH"]
    assert projection["direction"] == "DECREASE"


def test_micro_change_inside_kernel_tolerance_is_unresolved():
    a = held("AAA", "100", intent=NO_INCREASE)
    # N = 1000.0004 → t=100% → 100.00004 shares: a real six-decimal increase
    # that the kernel's 0.0001 non-zero tolerance would call NO_CHANGE.
    v = basis([a], {"AAA": 10}, cash="0.0004")
    projection = project_quantity(a, v, "BUY", 100)
    assert projection["proposed_shares"] == "100.00004" and projection["direction"] == "INCREASE"
    review = _review(a, projection, source="ADVISORY", reason_code="L2_ALLOCATION")
    assert review["outcome"] == "UNRESOLVED"
    assert review["reasons"] == ["QUANTITY_DIRECTION_TOLERANCE_AMBIGUITY"]


def test_positive_to_zero_is_a_decrease_conflict_under_do_not_decrease():
    a = held("AAA", "0.5", intent=NO_DECREASE)
    v = basis([a], {"AAA": 10}, cash="100")
    projection = project_quantity(a, v, "SELL", 0)
    review = _review(a, projection, source="SYSTEM_RULE", reason_code="FORCED_EXIT_SELL_SIGNAL")
    assert review["outcome"] == "CONFLICT" and review["restriction"] == "DECREASE_PROHIBITED_BY_OWNER"
    assert review["conflict_kind"] == "INTENT_SYSTEM_RULE_CONFLICT"


@pytest.mark.parametrize("raw,code", [
    ({}, "QUOTE_MISSING"),
    ({"current_price": None}, "QUOTE_MISSING"),
    ({"current_price": 0}, "QUOTE_ZERO_OR_NEGATIVE"),
    ({"current_price": 50, "_stale_data": True}, "QUOTE_STALE"),
    ({"current_price": None, "_vps_cache_miss": True}, "QUOTE_CACHE_MISS"),
    ({"current_price": None, "_quarantine_reason": "X"}, "QUOTE_QUARANTINED"),
])
def test_missing_zero_or_stale_quote_leaves_basis_unresolved(raw, code):
    a = held("AAA", "10")
    v = build_valuation_basis([a], [], {"AAA": raw}, {"AAA": "THB"}, 100)
    assert not v.resolved and code in v.reasons
    projection = project_quantity(a, v, "REDUCE", 5)
    assert projection["reasons"] == ["VALUATION_BASIS_UNRESOLVED"]


def test_no_average_cost_substitution_for_a_missing_quote():
    a = held("AAA", "10")
    v = build_valuation_basis([a], [], {"AAA": {"current_price": None, "avg_cost": 40}}, {"AAA": "THB"}, 0)
    assert not v.resolved and v.nav is None and v.values == {}


@pytest.mark.parametrize("currencies,cash,code", [
    ({"AAA": None, "BBB": "THB"}, 0, "CURRENCY_UNKNOWN"),
    ({"AAA": "USD", "BBB": "THB"}, 0, "CURRENCY_MIXED"),
    ({"AAA": "USD", "BBB": "USD"}, 100, "CURRENCY_MIXED"),   # THB cash vs USD holdings
])
def test_unknown_or_mixed_currency_is_unresolved_without_fx(currencies, cash, code):
    a, b = held("AAA"), held("BBB")
    quotes = {"AAA": {"current_price": 1}, "BBB": {"current_price": 1}}
    v = build_valuation_basis([a, b], [], quotes, currencies, cash)
    assert not v.resolved and code in v.reasons


def test_all_usd_with_no_cash_is_one_common_unit():
    a, b = held("AAA"), held("BBB")
    v = build_valuation_basis([a, b], [], {"AAA": {"current_price": 1}, "BBB": {"current_price": 2}},
                              {"AAA": "USD", "BBB": "USD"}, 0)
    assert v.resolved and v.unit == "USD"


def test_duplicate_holding_anomaly_does_not_fabricate_a_portfolio():
    a = held("AAA")
    v = build_valuation_basis([a], [{"code": "DUPLICATE_HOLDING", "symbol": "AAA", "rows": 2}],
                              {"AAA": {"current_price": 1}}, {"AAA": "THB"}, 0)
    assert not v.resolved and "DUPLICATE_HOLDING" in v.reasons


def test_absent_or_reconfirmation_required_intent_is_unresolved_even_when_unchanged():
    v_positions = [held("AAA"), held("BBB", status="RECONFIRMATION_REQUIRED")]
    v = basis(v_positions, {"AAA": 1, "BBB": 1})
    for position, reason in zip(v_positions, ("NO_CONFIRMED_INTENT", "RECONFIRMATION_REQUIRED")):
        review = _review(position, project_quantity(position, v, "HOLD", None),
                         source="ADVISORY", reason_code="L2_ALLOCATION")
        assert review["outcome"] == "UNRESOLVED" and reason in review["reasons"]


def test_ledger_scale_that_reverses_direction_becomes_a_new_proposal():
    ledger = ProposalLedger({"AAA"})
    buy = {"action": "BUY", "target_weight": 15.0, "current_weight": 10.0}
    trimmed = {"action": "BUY", "target_weight": 5.0, "current_weight": 10.0}
    ledger.observe("AAA", stage="L2_ALLOCATION", source="ADVISORY", effect="ORIGINATE",
                   reason_code="L2_ALLOCATION", after=buy)
    ledger.observe("AAA", stage="HARD_POLICY", source="POLICY_RISK", effect="SCALE",
                   reason_code="CASH_FLOOR_TRIM", before=buy, after=trimmed)
    ledger.observe("AAA", stage="ACTION_RECONCILIATION", source="SYSTEM_RULE", effect="RELABEL",
                   reason_code="ACTION_RECONCILE", before=trimmed, after={**trimmed, "action": "REDUCE"})
    first, second = ledger.proposals("AAA")
    assert (first.source, first.disposition, first.replaced_by) == ("ADVISORY", REPLACED, second.proposal_id)
    assert (second.source, second.action, second.disposition) == ("POLICY_RISK", "REDUCE", ACTIVE)
    assert [t["effect"] for t in ledger.transitions] == ["ORIGINATE", "REPLACE", "RELABEL"]


def test_ledger_policy_scale_records_the_legacy_rule_as_target_origin():
    ledger = ProposalLedger({"AAA"}, "COMMON_NAV_FROZEN_QUOTES")
    buy = {"action": "BUY", "target_weight": 30.0, "current_weight": 10.0}
    capped = {"action": "BUY", "target_weight": 22.0, "current_weight": 10.0}
    ledger.observe("AAA", stage="L2_ALLOCATION", source="ADVISORY", effect="ORIGINATE",
                   reason_code="L2_ALLOCATION", after=buy)
    ledger.observe("AAA", stage="HARD_POLICY", source="POLICY_RISK", effect="SCALE",
                   reason_code="POSITION_CAP", before=buy, after=capped)
    [proposal] = ledger.proposals("AAA")
    # Same proposal (no reversal), but its target is now the legacy policy rule's output.
    assert proposal.source == "ADVISORY" and proposal.target_stage == "HARD_POLICY"
    assert proposal.target_semantics == "LEGACY_POLICY_RULE"
    assert [t["rule_semantics"] for t in ledger.transitions] == ["ADVISORY_MODEL_OUTPUT", "LEGACY_POLICY_RULE"]
    assert {t["row_current_weight_basis"] for t in ledger.transitions} == {"COMMON_NAV_FROZEN_QUOTES"}


def test_ledger_l1_legs_and_their_lock_placeholder_are_intermediate():
    ledger = ProposalLedger({"AAA"})
    leg = {"action": "SELL", "target_weight": 0.0, "current_weight": None}
    ledger.observe("AAA", stage="L1_STRATEGIST", source="ADVISORY", effect="ORIGINATE",
                   reason_code="L1_PROPOSAL", after=leg)
    ledger.observe("AAA", stage="LEGACY_ALLOW_SWAP", source="SYSTEM_RULE", effect="SUPPRESS",
                   reason_code="LEGACY_ALLOW_SWAP_FALSE", before=leg,
                   after={"action": "HOLD", "target_weight": None, "current_weight": None})
    ledger.observe("AAA", stage="L2_ALLOCATION", source="ADVISORY", effect="ORIGINATE",
                   reason_code="L2_ALLOCATION", after={"action": "HOLD", "target_weight": 10.0})
    ledger.observe("AAA", stage="FORCED_SELL", source="SYSTEM_RULE", effect="REPLACE",
                   reason_code="FORCED_EXIT_SELL_SIGNAL", after={"action": "SELL", "target_weight": 0.0})
    ledger.observe("AAA", stage="LEGACY_ALLOW_SWAP", source="SYSTEM_RULE", effect="SUPPRESS",
                   reason_code="LEGACY_ALLOW_SWAP_FALSE", after={"action": "HOLD", "target_weight": 10.0})
    assert [(p.stage, p.materiality) for p in ledger.proposals("AAA")] == [
        ("L1_STRATEGIST", "INTERMEDIATE_REASONING"),
        ("LEGACY_ALLOW_SWAP", "INTERMEDIATE_REASONING"),   # placeholder for the dropped L1 leg
        ("L2_ALLOCATION", "MATERIAL"),
        ("FORCED_SELL", "MATERIAL"),
        ("LEGACY_ALLOW_SWAP", "MATERIAL"),                 # lock suppressing a material proposal
    ]


def test_ledger_abandoned_attempt_and_unheld_symbols():
    ledger = ProposalLedger({"AAA"})
    ledger.observe("AAA", stage="L2_ALLOCATION", source="ADVISORY", effect="ORIGINATE",
                   reason_code="L2_ALLOCATION", after={"action": "SELL", "target_weight": 0.0})
    ledger.observe("WATCHLIST", stage="L2_ALLOCATION", source="ADVISORY", effect="ORIGINATE",
                   reason_code="L2_ALLOCATION", after={"action": "BUY", "target_weight": 5.0})
    ledger.abandon_attempt("PRIMARY")
    ledger.begin_attempt("FALLBACK")
    ledger.observe("AAA", stage="FALLBACK_ALLOCATION", source="ADVISORY", effect="ORIGINATE",
                   reason_code="FALLBACK_ALLOCATION", after={"action": "HOLD", "target_weight": 10.0})
    first, second = ledger.proposals("AAA")
    assert first.disposition == ABANDONED and first.replaced_by is None
    assert second.attempt == "FALLBACK" and ledger.active("AAA") is second
    assert ledger.proposals("WATCHLIST") == []


def test_ledger_rejects_unbounded_vocabulary():
    ledger = ProposalLedger({"AAA"})
    with pytest.raises(ValueError):
        ledger.observe("AAA", stage="X", source="AI", effect="ORIGINATE", reason_code="X", after={})
    with pytest.raises(ValueError):
        ledger.observe("AAA", stage="X", source="ADVISORY", effect="DELETE", reason_code="X", after={})


def test_suppression_keeps_the_suppressed_proposal():
    ledger = ProposalLedger({"AAA"})
    sell = {"action": "SELL", "target_weight": 0.0, "current_weight": 10.0}
    ledger.observe("AAA", stage="FORCED_SELL", source="SYSTEM_RULE", effect="ORIGINATE",
                   reason_code="FORCED_EXIT_SELL_SIGNAL", after=sell)
    ledger.observe("AAA", stage="LEGACY_ALLOW_SWAP", source="SYSTEM_RULE", effect="SUPPRESS",
                   reason_code="LEGACY_ALLOW_SWAP_FALSE", before=sell,
                   after={"action": "HOLD", "target_weight": 10.0, "current_weight": 10.0})
    forced, hold = ledger.proposals("AAA")
    assert (forced.disposition, forced.suppressed_by) == (SUPPRESSED, "LEGACY_ALLOW_SWAP")
    assert hold.action == "HOLD" and ledger.active("AAA") is hold
