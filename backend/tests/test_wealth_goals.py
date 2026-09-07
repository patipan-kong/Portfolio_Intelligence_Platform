"""Focused direct-endpoint coverage for Wealth Goals Foundation v1 (Phase 6, Milestone 1)."""
import asyncio
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import (
    Base,
    CashAccount,
    CashAccountTransaction,
    Liability,
    Portfolio,
    PortfolioSnapshot,
    Transaction,
    WealthGoal,
    Workspace,
)
import models.asset  # noqa: F401 — registers Asset tables referenced by ledger models.
import models.registry_finding  # noqa: F401 — registers registry tables referenced by Base metadata.
import main


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def create(db, **overrides):
    payload = {
        "name": "Retire by 55",
        "goal_type": "RETIREMENT",
        "target_amount": 20_000_000.0,
        "currency": "THB",
        "priority": "HIGH",
    }
    payload.update(overrides)
    return asyncio.run(main.create_wealth_goal(main.WealthGoalCreate(**payload), db))


def update(db, goal_id, **fields):
    return asyncio.run(main.update_wealth_goal(goal_id, main.WealthGoalUpdate(**fields), db))


def list_goals(db, include_archived=False):
    return asyncio.run(main.list_wealth_goals(include_archived=include_archived, db=db))


# 1. create goal
def test_create_valid_goal_returns_the_frozen_v1_contract():
    db = make_session()
    created = create(db, name=" Retire by 55 ", note="  discussed with spouse  ", target_date="2055-01-01")

    assert created["name"] == "Retire by 55"
    assert created["goal_type"] == "RETIREMENT"
    assert created["target_amount"] == 20_000_000.0
    assert created["currency"] == "THB"
    assert created["target_date"] == "2055-01-01"
    assert created["priority"] == "HIGH"
    assert created["note"] == "discussed with spouse"
    assert created["is_archived"] is False
    assert created["workspace_id"] == main._ws_id(db)


# 2 & 6. active list + include_archived
def test_normal_list_is_active_only_and_include_archived_supports_management():
    db = make_session()
    active = create(db, name="Active")
    archived = create(db, name="Archived")
    update(db, archived["id"], is_archived=True)

    assert [row["id"] for row in list_goals(db)] == [active["id"]]
    assert {row["id"] for row in list_goals(db, include_archived=True)} == {active["id"], archived["id"]}


# 3. metadata update
def test_metadata_update_replaces_fields_and_leaves_others_unchanged():
    db = make_session()
    goal = create(db, name="House Down Payment", goal_type="HOUSE", priority="MEDIUM")

    changed = update(
        db,
        goal["id"],
        name="House Down Payment 2028",
        goal_type="HOUSE",
        target_amount=3_000_000.0,
        priority="HIGH",
        note="Updated target",
    )

    assert changed["name"] == "House Down Payment 2028"
    assert changed["target_amount"] == 3_000_000.0
    assert changed["priority"] == "HIGH"
    assert changed["note"] == "Updated target"
    assert db.query(WealthGoal).one().target_amount == 3_000_000.0


# 4, 5, 7. archive / archived exclusion / restore
def test_archive_is_hidden_by_default_and_restore_preserves_identity():
    db = make_session()
    goal = create(db)

    archived = update(db, goal["id"], is_archived=True)
    assert archived["is_archived"] is True
    assert list_goals(db) == []
    assert list_goals(db, include_archived=True)[0]["id"] == goal["id"]

    restored = update(db, goal["id"], is_archived=False)
    assert restored["id"] == goal["id"]
    assert restored["is_archived"] is False
    assert list_goals(db)[0]["id"] == goal["id"]


# 8. workspace isolation
def test_foreign_workspace_lookup_returns_404_without_leaking_existence():
    db = make_session()
    current_workspace_id = main._ws_id(db)
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    foreign = WealthGoal(
        workspace_id=other_workspace.id,
        name="Private Goal",
        goal_type="OTHER",
        target_amount=100.0,
        currency="THB",
        priority="LOW",
    )
    db.add(foreign)
    db.commit()

    assert foreign.workspace_id != current_workspace_id
    with pytest.raises(HTTPException) as error:
        update(db, foreign.id, target_amount=200.0)
    assert error.value.status_code == 404
    assert error.value.detail == "Wealth goal not found"


# 9, 10, 11, 12, 13, 14. create-time validation
@pytest.mark.parametrize(
    "payload",
    [
        {"name": "   ", "goal_type": "OTHER", "target_amount": 1.0, "currency": "THB", "priority": "LOW"},
        {"name": "Goal", "goal_type": "UNSUPPORTED", "target_amount": 1.0, "currency": "THB", "priority": "LOW"},
        {"name": "Goal", "goal_type": "OTHER", "target_amount": 0.0, "currency": "THB", "priority": "LOW"},
        {"name": "Goal", "goal_type": "OTHER", "target_amount": -1.0, "currency": "THB", "priority": "LOW"},
        {"name": "Goal", "goal_type": "OTHER", "target_amount": float("nan"), "currency": "THB", "priority": "LOW"},
        {"name": "Goal", "goal_type": "OTHER", "target_amount": float("inf"), "currency": "THB", "priority": "LOW"},
        {"name": "Goal", "goal_type": "OTHER", "target_amount": -math.inf, "currency": "THB", "priority": "LOW"},
        {"name": "Goal", "goal_type": "OTHER", "target_amount": 1.0, "currency": "USD", "priority": "LOW"},
        {"name": "Goal", "goal_type": "OTHER", "target_amount": 1.0, "currency": "THB", "priority": "UNSUPPORTED"},
    ],
)
def test_create_validation_rejects_invalid_v1_values(payload):
    with pytest.raises(ValidationError):
        main.WealthGoalCreate(**payload)


def test_update_requires_a_field_and_rejects_invalid_values():
    with pytest.raises(ValidationError):
        main.WealthGoalUpdate()
    with pytest.raises(ValidationError):
        main.WealthGoalUpdate(name=" ")
    with pytest.raises(ValidationError):
        main.WealthGoalUpdate(goal_type="UNSUPPORTED")
    with pytest.raises(ValidationError):
        main.WealthGoalUpdate(target_amount=0.0)
    with pytest.raises(ValidationError):
        main.WealthGoalUpdate(target_amount=-0.01)
    with pytest.raises(ValidationError):
        main.WealthGoalUpdate(target_amount=float("nan"))
    with pytest.raises(ValidationError):
        main.WealthGoalUpdate(target_amount=float("inf"))
    with pytest.raises(ValidationError):
        main.WealthGoalUpdate(priority="URGENT")


# 15. nullable/required target-date contract
def test_target_date_is_nullable_and_can_be_set_then_cleared():
    db = make_session()
    undated = create(db, name="Someday FIRE", goal_type="FIRE", target_date=None)
    assert undated["target_date"] is None
    assert undated in list_goals(db)

    dated = update(db, undated["id"], target_date="2040-06-30")
    assert dated["target_date"] == "2040-06-30"

    cleared = update(db, undated["id"], target_date=None)
    assert cleared["target_date"] is None


# 16. zero mutation of Portfolio goal fields
def test_wealth_goal_mutations_do_not_touch_portfolio_goal_fields():
    db = make_session()
    workspace_id = main._ws_id(db)
    portfolio = Portfolio(
        workspace_id=workspace_id,
        name="Core",
        goal_type="WEDDING",
        goal_priority="ESSENTIAL",
        goal_target_date="2027-05-01",
        goal_target_value=500_000.0,
        risk_personality="MODERATE",
    )
    db.add(portfolio)
    db.commit()

    goal = create(db, name="Unrelated Wealth Goal")
    update(db, goal["id"], target_amount=999.0, is_archived=True)
    db.refresh(portfolio)

    assert portfolio.goal_type == "WEDDING"
    assert portfolio.goal_priority == "ESSENTIAL"
    assert portfolio.goal_target_date == "2027-05-01"
    assert portfolio.goal_target_value == 500_000.0
    assert portfolio.risk_personality == "MODERATE"


# 17. zero mutation of CashAccount/Liability/investment state
def test_wealth_goal_mutations_do_not_change_cash_liability_or_investment_state():
    db = make_session()
    workspace_id = main._ws_id(db)
    cash = CashAccount(workspace_id=workspace_id, name="Savings", currency="THB", balance=1234.0)
    liability = Liability(workspace_id=workspace_id, name="Card", liability_type="CREDIT_CARD", balance=500.0, currency="THB")
    portfolio = Portfolio(workspace_id=workspace_id, name="Core", cash_balance=5678.0)
    db.add_all([cash, liability, portfolio])
    db.commit()
    before_cash_transactions = db.query(CashAccountTransaction).count()
    before_investment_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()

    goal = create(db, target_amount=1000.0)
    update(db, goal["id"], target_amount=900.0, is_archived=True)
    db.refresh(cash)
    db.refresh(liability)
    db.refresh(portfolio)

    assert cash.balance == 1234.0
    assert liability.balance == 500.0
    assert portfolio.cash_balance == 5678.0
    assert db.query(CashAccountTransaction).count() == before_cash_transactions
    assert db.query(Transaction).count() == before_investment_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots
