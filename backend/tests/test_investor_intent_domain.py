"""Investor Intent V1 pure domain contract."""
import ast
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from services.investor_intent import (
    ALLOWED, CONFLICT, CONSISTENT, DECREASE, INCREASE, NO_CHANGE, PROHIBITED, UNRESOLVED,
    SOURCE_ADVISORY, SOURCE_POLICY_RISK, SOURCE_SYSTEM_RULE,
    IntentState, evaluate_proposal, evaluate_quantity_change, quantity_direction,
)


def intent(increase=False, decrease=False, pref="NONE"):
    return IntentState(increase, decrease, pref, intent_id=7, revision=3)


@pytest.mark.parametrize("increase,decrease,direction,expected", [
    (False, False, INCREASE, ALLOWED), (False, False, DECREASE, ALLOWED),
    (True, False, INCREASE, PROHIBITED), (True, False, DECREASE, ALLOWED),
    (False, True, INCREASE, ALLOWED), (False, True, DECREASE, PROHIBITED),
    (True, True, INCREASE, PROHIBITED), (True, True, DECREASE, PROHIBITED),
])
def test_all_four_hard_permission_combinations(increase, decrease, direction, expected):
    proposed = 15 if direction == INCREASE else 5
    result = evaluate_quantity_change(intent(increase, decrease), 10, proposed)
    assert result["direction"] == direction
    assert result["permission"] == expected
    assert result["intent"]["revision"] == 3 and result["intent"]["intent_id"] == 7


def test_full_exit_is_a_decrease():
    assert evaluate_quantity_change(intent(decrease=True), 10, 0)["permission"] == PROHIBITED


@pytest.mark.parametrize("current,proposed,direction", [
    (10, 0, DECREASE),            # positive -> zero
    (0.00005, 0, DECREASE),       # tiny positive -> zero: still a real full exit
    (1e-9, 0.0, DECREASE),
    (0, 10, INCREASE),            # zero -> positive
    (0, 0.00005, INCREASE),       # zero -> tiny positive: still a real entry
    (0.0, 1e-9, INCREASE),
    (0, 0, NO_CHANGE),            # exact no-change at zero
    (10, 10, NO_CHANGE),          # exact no-change
    (0.00005, 0.00005, NO_CHANGE),
    (10, 10.00005, NO_CHANGE),    # float noise between two non-zero quantities
    (10, 9.99995, NO_CHANGE),
    (0.00005, 0.00009, NO_CHANGE),
    (10, 10.0002, INCREASE),      # beyond tolerance between non-zero quantities
    (10, 9.9998, DECREASE),
])
def test_quantity_direction_boundaries(current, proposed, direction):
    assert quantity_direction(current, proposed) == direction


def test_tiny_full_exit_is_prohibited_by_decrease_restriction():
    result = evaluate_quantity_change(intent(decrease=True), 0.00005, 0)
    assert result["direction"] == DECREASE
    assert result["permission"] == PROHIBITED
    assert result["reasons"] == ["DECREASE_PROHIBITED_BY_OWNER"]
    conflict = evaluate_proposal(intent(decrease=True), 0.00005, 0,
                                 source=SOURCE_SYSTEM_RULE, reason="Forced exit: SELL signal.")
    assert conflict["outcome"] == CONFLICT and conflict["requires_owner_decision"] is True


def test_entry_from_zero_is_prohibited_by_increase_restriction():
    result = evaluate_quantity_change(intent(increase=True), 0, 0.00005)
    assert result["direction"] == INCREASE and result["permission"] == PROHIBITED


def test_no_quantity_change_is_allowed_even_when_fully_restricted_or_without_intent():
    assert evaluate_quantity_change(intent(True, True), 10, 10)["permission"] == ALLOWED
    no_intent = evaluate_quantity_change(None, 10, 10)
    assert no_intent["permission"] == ALLOWED and no_intent["reasons"] == ["NO_QUANTITY_CHANGE"]


def test_price_only_weight_movement_is_not_a_quantity_change():
    # Same shares at a new price: the caller passes quantities, so no direction.
    assert quantity_direction(10, 10) == NO_CHANGE
    assert evaluate_quantity_change(intent(True, True), 10, 10.00005)["direction"] == NO_CHANGE


def test_absence_of_intent_is_not_permission():
    for proposed in (5, 15):
        result = evaluate_quantity_change(None, 10, proposed)
        assert result["permission"] == UNRESOLVED
        assert result["reasons"] == ["NO_CONFIRMED_INTENT"]
        assert result["intent"] is None


def test_explicit_unrestricted_intent_differs_from_absence():
    explicit = evaluate_quantity_change(intent(), 10, 15)
    absent = evaluate_quantity_change(None, 10, 15)
    assert explicit["permission"] == ALLOWED and absent["permission"] == UNRESOLVED


def test_position_absent_from_referenced_holdings_is_unresolved():
    result = evaluate_quantity_change(intent(), None, 5)
    assert result["permission"] == UNRESOLVED
    assert result["reasons"] == ["POSITION_NOT_IN_REFERENCED_HOLDINGS"]


@pytest.mark.parametrize("pref", ["NONE", "PREFER_KEEP", "PREFER_EXIT"])
def test_soft_preference_never_overrides_hard_restriction(pref):
    assert evaluate_quantity_change(intent(decrease=True, pref=pref), 10, 0)["permission"] == PROHIBITED
    assert evaluate_quantity_change(intent(increase=True, pref=pref), 10, 20)["permission"] == PROHIBITED
    assert evaluate_quantity_change(intent(pref=pref), 10, 0)["permission"] == ALLOWED


def test_forced_exit_against_decrease_prohibition_is_conflict_preserving_both_facts():
    result = evaluate_proposal(intent(decrease=True, pref="PREFER_EXIT"), 10, 0,
                               source=SOURCE_SYSTEM_RULE, reason="Forced exit: SELL signal.")
    assert result["outcome"] == CONFLICT
    assert result["owner_restriction"] == "DECREASE_PROHIBITED_BY_OWNER"
    assert result["proposal"] == {"source": SOURCE_SYSTEM_RULE, "direction": DECREASE,
                                  "reason": "Forced exit: SELL signal."}
    assert result["conflict_kind"] == "INTENT_SYSTEM_RULE_CONFLICT"
    assert result["requires_owner_decision"] is True
    assert result["intent"]["decrease_prohibited"] is True
    assert result["intent"]["soft_preference"] == "PREFER_EXIT"


def test_policy_guidance_conflict_is_an_intent_policy_conflict_not_a_violation():
    result = evaluate_proposal(intent(decrease=True), 10, 6,
                               source=SOURCE_POLICY_RISK, reason="Concentration above 22% limit")
    assert result["outcome"] == CONFLICT
    assert result["conflict_kind"] == "INTENT_POLICY_CONFLICT"
    assert result["proposal"]["reason"] == "Concentration above 22% limit"
    assert "violation" not in str(result).lower()


def test_advisory_conflict_and_consistent_and_unresolved_outcomes():
    assert evaluate_proposal(intent(increase=True), 10, 12, source=SOURCE_ADVISORY,
                             reason="add")["conflict_kind"] == "INTENT_ADVISORY_CONFLICT"
    consistent = evaluate_proposal(intent(increase=True), 10, 8, source=SOURCE_ADVISORY, reason="trim")
    assert consistent["outcome"] == CONSISTENT and consistent["conflict_kind"] is None
    assert consistent["requires_owner_decision"] is False
    assert evaluate_proposal(None, 10, 8, source=SOURCE_ADVISORY, reason="trim")["outcome"] == UNRESOLVED


@pytest.mark.parametrize("bad", [-1, float("nan"), float("inf"), True, "10", None])
def test_invalid_quantities_rejected(bad):
    with pytest.raises(ValueError):
        evaluate_quantity_change(intent(), 10, bad)
    if bad is not None:
        with pytest.raises(ValueError):
            evaluate_quantity_change(intent(), bad, 10)


def test_invalid_intent_values_and_proposals_rejected():
    with pytest.raises(ValueError):
        IntentState(True, False, "PREFER_ADD")
    with pytest.raises(ValueError):
        IntentState(1, False, "NONE")
    with pytest.raises(ValueError):
        evaluate_proposal(intent(), 10, 5, source="OWNER", reason="x")
    with pytest.raises(ValueError):
        evaluate_proposal(intent(), 10, 5, source=SOURCE_ADVISORY, reason=" ")


def test_domain_module_is_pure():
    path = Path(__file__).resolve().parents[1] / "services" / "investor_intent.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported = {
        (node.module or "") if isinstance(node, ast.ImportFrom) else alias.name
        for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in (node.names if isinstance(node, ast.Import) else [None])
    }
    assert imported <= {"__future__", "dataclasses", "datetime", "math"}


def test_intent_status_for_current_holding_episode():
    from datetime import datetime

    from services.investor_intent import (
        STATUS_CONFIRMED, STATUS_NO_CONFIRMED_INTENT, STATUS_RECONFIRMATION_REQUIRED, intent_status,
    )
    episode = datetime(2026, 10, 1, 9, 0)
    before, after = datetime(2026, 9, 30), datetime(2026, 10, 2)
    assert intent_status(False, episode, None) == STATUS_NO_CONFIRMED_INTENT
    # Confirmed during the current episode.
    assert intent_status(True, episode, after) == STATUS_CONFIRMED
    # Confirmed for an earlier episode: full exit then same-symbol re-entry.
    assert intent_status(True, episode, before) == STATUS_RECONFIRMATION_REQUIRED
    # Not currently held, or a legacy row without an episode start: history applies as-is.
    assert intent_status(True, None, before) == STATUS_CONFIRMED
    # Missing confirmation record fails closed.
    assert intent_status(True, episode, None) == STATUS_RECONFIRMATION_REQUIRED
