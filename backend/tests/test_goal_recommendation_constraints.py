import os
import sys
from datetime import date, timedelta

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
from models.database import Base, WealthGoal, Workspace
from services.goal_recommendation_constraints import (
    CONTRACT_VERSION,
    GoalConstraintAdmission,
    build_goal_constraint_evidence,
    evaluate_goal_recommendation_constraint,
    load_goal_constraint_admission,
)
from services.optimizer.constraint_resolver import (
    apply_single_position_upper_bound,
    resolve_constraints,
)


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)(), engine


def _goal(db, workspace_id, *, target_date="2027-01-01", archived=False):
    goal = WealthGoal(
        workspace_id=workspace_id, name="Ignored", goal_type="HOUSE",
        target_amount=1.0, currency="THB", priority="HIGH",
        target_date=target_date, is_archived=archived,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def _envelope(base):
    return resolve_constraints(
        {"max_sector_pct": 40}, {},
        {"regime": "SIDEWAYS", "constraints": {
            "max_single_position_pct": base,
            "min_cash_pct": 5,
            "turnover_multiplier": 1,
        }},
        {"volatility_tolerance": 1.0, "max_cash_preference": .05, "turnover_tolerance": .4},
    )


def test_admission_query_is_workspace_scoped_and_selects_only_admitted_columns():
    db, engine = _session()
    own = Workspace(name="Own")
    foreign = Workspace(name="Foreign")
    db.add_all([own, foreign])
    db.commit()
    item = _goal(db, own.id)
    foreign_item = _goal(db, foreign.id)
    own_id, item_id, foreign_item_id = own.id, item.id, foreign_item.id
    statements = []
    event.listen(engine, "before_cursor_execute", lambda *args: statements.append(args[2]))

    admission = load_goal_constraint_admission(db, own_id, item_id)
    assert admission.goal_id == item_id
    assert load_goal_constraint_admission(db, own_id, foreign_item_id) is None
    select_sql = [s.lower() for s in statements if "select" in s.lower() and "wealth_goals" in s.lower()]
    assert select_sql
    assert all("wealth_goals.name" not in s for s in select_sql)
    assert all("goal_type" not in s and "target_amount" not in s and "priority" not in s for s in select_sql)


@pytest.mark.parametrize("days,applicable", [(0, True), (365, True), (366, False)])
def test_signed_calendar_day_boundaries(days, applicable):
    as_of = date(2030, 1, 1)
    admission = GoalConstraintAdmission(7, False, as_of + timedelta(days=days))
    evaluation = evaluate_goal_recommendation_constraint(admission, as_of)
    assert evaluation.days_remaining == days
    assert (evaluation.candidate is not None) is applicable


def test_negative_horizon_is_ineligible_and_helper_has_no_clock_dependency():
    as_of = date(2030, 1, 1)
    with pytest.raises(ValueError, match="past"):
        evaluate_goal_recommendation_constraint(
            GoalConstraintAdmission(7, False, as_of - timedelta(days=1)), as_of,
        )


@pytest.mark.parametrize(
    "base,relation,status,final",
    [
        (25, "STRICTER_THAN_BASE", "APPLIED_AND_BINDING", 20),
        (22, "STRICTER_THAN_BASE", "APPLIED_AND_BINDING", 20),
        (20, "EQUAL_TO_BASE", "APPLIED_BUT_DOMINATED", 20),
        (18, "LOOSER_THAN_BASE", "APPLIED_BUT_DOMINATED", 18),
    ],
)
def test_exact_status_mapping(base, relation, status, final):
    as_of = date(2030, 1, 1)
    evaluation = evaluate_goal_recommendation_constraint(
        GoalConstraintAdmission(9, False, as_of), as_of,
    )
    _, outcome = apply_single_position_upper_bound(_envelope(base), evaluation.candidate)
    evidence = build_goal_constraint_evidence(evaluation, outcome)
    assert evidence["contract_version"] == CONTRACT_VERSION
    assert evidence["resolution"]["relation_to_base"] == relation
    assert evidence["resolution"]["application_status"] == status
    assert evidence["resolution"]["post_goal_effective_pct"] == final
    assert evidence["resolution"]["application_status"] != "APPLIED"


def test_not_applicable_evidence_has_required_composition_nulls():
    as_of = date(2030, 1, 1)
    evaluation = evaluate_goal_recommendation_constraint(
        GoalConstraintAdmission(9, False, as_of + timedelta(days=366)), as_of,
    )
    evidence = build_goal_constraint_evidence(evaluation)
    assert evidence["matched_rule"] is None
    assert evidence["contribution"] is None
    assert evidence["resolution"] == {
        "pre_goal_effective_pct": None,
        "post_goal_effective_pct": None,
        "relation_to_base": "NOT_APPLICABLE",
        "application_status": "NOT_APPLICABLE",
        "resulting_binding_source": None,
    }
    assert "active_policy_effective_pct" not in evidence
