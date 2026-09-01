import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.optimizer.constraint_resolver import (
    SinglePositionUpperBoundCandidate,
    apply_single_position_upper_bound,
    envelope_to_dict,
    resolve_constraints,
)


def _base(cap):
    return resolve_constraints(
        {"max_sector_pct": 40}, {},
        {"regime": "SIDEWAYS", "constraints": {
            "max_single_position_pct": cap, "min_cash_pct": 5, "turnover_multiplier": 1,
        }},
        {"volatility_tolerance": 1, "max_cash_preference": .05, "turnover_tolerance": .4},
    )


def _candidate(value=20):
    return SinglePositionUpperBoundCandidate(value, "REQUEST_POLICY", "request cap")


def test_strict_tightening_is_copy_on_compose_and_changes_existing_fields_only():
    original = _base(25)
    before = envelope_to_dict(original)
    composed, outcome = apply_single_position_upper_bound(original, _candidate())
    assert envelope_to_dict(original) == before
    assert composed is not original
    assert composed.effective_single_position_pct == 20
    assert composed.single_position.effective == 20
    assert composed.single_position.binding_source == "REQUEST_POLICY"
    assert outcome.relation_to_base == "STRICTER_THAN_BASE"


def test_equality_and_looser_candidate_preserve_binding_source():
    equal = _base(20)
    equal_source = equal.single_position.binding_source
    equal_composed, equal_outcome = apply_single_position_upper_bound(equal, _candidate(20))
    assert equal_composed.single_position.binding_source == equal_source
    assert equal_outcome.relation_to_base == "EQUAL_TO_BASE"

    tighter_base = _base(18)
    tighter_source = tighter_base.single_position.binding_source
    looser_composed, looser_outcome = apply_single_position_upper_bound(tighter_base, _candidate(20))
    assert looser_composed.effective_single_position_pct == 18
    assert looser_composed.single_position.binding_source == tighter_source
    assert looser_outcome.relation_to_base == "LOOSER_THAN_BASE"


def test_unactivated_serialization_shape_has_no_new_fields():
    payload = envelope_to_dict(_base(22))
    assert "additional_sources" not in payload
    assert "goal" not in repr(payload).lower()
