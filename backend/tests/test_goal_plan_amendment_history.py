"""Focused coverage for immutable WealthGoal plan-amendment evidence."""
import asyncio
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import Base, GoalFundingAllocationHistory, GoalPlanAmendmentHistory, WealthGoal, Workspace
import models.asset  # noqa: F401 — registers Asset tables referenced by ledger models.
import models.registry_finding  # noqa: F401 — registers registry tables referenced by Base metadata.
import main


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def create_goal(db, **overrides):
    payload = {
        "name": "Retire by 55",
        "goal_type": "RETIREMENT",
        "target_amount": 20_000_000.0,
        "currency": "THB",
        "target_date": "2055-01-01",
        "priority": "HIGH",
    }
    payload.update(overrides)
    return asyncio.run(main.create_wealth_goal(main.WealthGoalCreate(**payload), db))


def update_goal(db, goal_id, **fields):
    return asyncio.run(main.update_wealth_goal(goal_id, main.WealthGoalUpdate(**fields), db))


def list_history(db, goal_id):
    return asyncio.run(main.list_goal_plan_amendment_history(goal_id, db))


def history_rows(db):
    return db.query(GoalPlanAmendmentHistory).order_by(GoalPlanAmendmentHistory.id).all()


def test_each_in_scope_field_records_a_complete_before_after_snapshot():
    db = make_session()
    goal = create_goal(db)

    update_goal(db, goal["id"], target_amount=21_000_000.0)
    update_goal(db, goal["id"], target_date="2056-02-03")
    update_goal(db, goal["id"], priority="MEDIUM")

    amount, target_date, priority = history_rows(db)
    assert (amount.previous_target_amount, amount.resulting_target_amount) == (20_000_000.0, 21_000_000.0)
    assert (amount.previous_target_date, amount.resulting_target_date) == ("2055-01-01", "2055-01-01")
    assert (amount.previous_priority, amount.resulting_priority) == ("HIGH", "HIGH")
    assert (target_date.previous_target_date, target_date.resulting_target_date) == ("2055-01-01", "2056-02-03")
    assert (priority.previous_priority, priority.resulting_priority) == ("HIGH", "MEDIUM")


def test_clearing_target_date_and_multi_field_change_each_create_one_event():
    db = make_session()
    goal = create_goal(db)

    update_goal(db, goal["id"], target_date=None)
    update_goal(db, goal["id"], target_amount=25_000_000.0, target_date="2057-01-01", priority="LOW")

    cleared, multi = history_rows(db)
    assert (cleared.previous_target_date, cleared.resulting_target_date) == ("2055-01-01", None)
    assert (multi.previous_target_amount, multi.resulting_target_amount) == (20_000_000.0, 25_000_000.0)
    assert (multi.previous_target_date, multi.resulting_target_date) == (None, "2057-01-01")
    assert (multi.previous_priority, multi.resulting_priority) == ("HIGH", "LOW")


def test_omitted_or_semantically_unchanged_normalized_fields_do_not_record_history():
    db = make_session()
    goal = create_goal(db)

    update_goal(db, goal["id"], note="A note")
    update_goal(db, goal["id"], target_amount=20_000_000)
    update_goal(db, goal["id"], target_date="2055-01-01", priority="HIGH")

    assert history_rows(db) == []


def test_invalid_update_creates_no_history_and_preserves_current_goal():
    db = make_session()
    goal = create_goal(db)

    with pytest.raises(ValidationError):
        main.WealthGoalUpdate(target_amount=0)

    current = db.query(WealthGoal).filter(WealthGoal.id == goal["id"]).one()
    assert current.target_amount == 20_000_000.0
    assert history_rows(db) == []


def test_history_commit_failure_rolls_back_goal_and_history_together():
    db = make_session()
    goal = create_goal(db)

    def fail_before_commit(session):
        raise RuntimeError("history write failed")

    event.listen(db, "before_commit", fail_before_commit)
    try:
        with pytest.raises(RuntimeError, match="history write failed"):
            update_goal(db, goal["id"], target_amount=21_000_000.0)
    finally:
        event.remove(db, "before_commit", fail_before_commit)

    independent = sessionmaker(bind=db.get_bind())()
    try:
        current = independent.query(WealthGoal).filter(WealthGoal.id == goal["id"]).one()
        assert current.target_amount == 20_000_000.0
        assert independent.query(GoalPlanAmendmentHistory).count() == 0
    finally:
        independent.close()


def test_history_is_newest_first_with_id_tie_breaker_and_archived_goal_remains_readable():
    db = make_session()
    goal = create_goal(db)
    update_goal(db, goal["id"], target_amount=21_000_000.0)
    update_goal(db, goal["id"], priority="MEDIUM")
    rows = history_rows(db)
    rows[0].recorded_at = rows[1].recorded_at = datetime(2026, 9, 4, 12, 0, 0)
    db.commit()
    update_goal(db, goal["id"], is_archived=True)
    update_goal(db, goal["id"], is_archived=False)

    assert [row["id"] for row in list_history(db, goal["id"])] == [rows[1].id, rows[0].id]
    assert db.query(GoalPlanAmendmentHistory).count() == 2


def test_history_read_is_workspace_isolated():
    db = make_session()
    current_workspace_id = main._ws_id(db)
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    foreign = WealthGoal(
        workspace_id=other_workspace.id,
        name="Private",
        goal_type="OTHER",
        target_amount=100.0,
        currency="THB",
        priority="LOW",
    )
    db.add(foreign)
    db.commit()
    db.add(GoalPlanAmendmentHistory(
        workspace_id=other_workspace.id,
        wealth_goal_id=foreign.id,
        previous_target_amount=100.0,
        resulting_target_amount=200.0,
        previous_target_date=None,
        resulting_target_date=None,
        previous_priority="LOW",
        resulting_priority="LOW",
    ))
    db.commit()

    assert foreign.workspace_id != current_workspace_id
    with pytest.raises(HTTPException) as error:
        list_history(db, foreign.id)
    assert error.value.status_code == 404
    assert error.value.detail == "Wealth goal not found"


def test_current_goal_context_and_funding_history_remain_current_state_only():
    db = make_session()
    goal = create_goal(db, target_amount=1_000.0)
    # Existing funding evidence is intentionally independent of this plan
    # amendment; the plan PATCH must not alter it.
    funding_event = GoalFundingAllocationHistory(
        workspace_id=main._ws_id(db), wealth_goal_id=goal["id"], source_kind="CASH_ACCOUNT",
        source_id=1, source_name="Savings", action="CREATE", previous_designated_amount=None,
        resulting_designated_amount=100.0, currency="THB",
    )
    db.add(funding_event)
    db.commit()

    update_goal(db, goal["id"], target_amount=2_000.0)
    context = asyncio.run(main.get_goal_context(goal["id"], db))

    assert context["goals"][0]["target_amount"] == 2_000.0
    assert db.query(GoalFundingAllocationHistory).count() == 1
