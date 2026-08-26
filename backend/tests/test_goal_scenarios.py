"""Focused direct-endpoint coverage for Named Scenario Foundation (Phase 6,
Milestone 3).

Scope: a GoalScenario persists only a name plus two forward What-If
assumptions (monthly_contribution, annual_return_pct) for exactly one
WealthGoal. It is never a forecast, a probability, an optimizer input, or a
saved snapshot of the goal/funding state — no target, target date, starting
value, or computed projection is ever persisted or exercised here. See
models.database.GoalScenario for the full live-context rationale.
"""
import asyncio
from pathlib import Path
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import (
    Base,
    CashAccount,
    CashAccountTransaction,
    GoalFundingAllocation,
    GoalScenario,
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


def make_goal(db, **overrides):
    payload = {
        "name": "Retire by 55",
        "goal_type": "RETIREMENT",
        "target_amount": 20_000_000.0,
        "currency": "THB",
        "priority": "HIGH",
    }
    payload.update(overrides)
    return asyncio.run(main.create_wealth_goal(main.WealthGoalCreate(**payload), db))


def archive_goal(db, goal_id):
    return asyncio.run(main.update_wealth_goal(goal_id, main.WealthGoalUpdate(is_archived=True), db))


def create_scenario(db, goal_id, **fields):
    body = main.GoalScenarioCreate(**fields)
    return asyncio.run(main.create_goal_scenario(goal_id, body, db))


def update_scenario(db, goal_id, scenario_id, **fields):
    body = main.GoalScenarioUpdate(**fields)
    return asyncio.run(main.update_goal_scenario(goal_id, scenario_id, body, db))


def list_scenarios(db, goal_id, include_archived=False):
    return asyncio.run(main.list_goal_scenarios(goal_id, include_archived=include_archived, db=db))


def default_scenario_fields(**overrides):
    fields = {"name": "Aggressive contribution", "monthly_contribution": 10_000.0, "annual_return_pct": 5.0}
    fields.update(overrides)
    return fields


def test_goal_scenario_revision_merges_the_repository_heads():
    """The scenario migration is the single post-milestone Alembic head."""
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    script = ScriptDirectory.from_config(config)

    assert script.get_heads() == ["d4f6a8c0e2b4"]


# 1. create scenario
def test_create_scenario_returns_the_frozen_contract():
    db = make_session()
    goal = make_goal(db)

    created = create_scenario(db, goal["id"], **default_scenario_fields(name="  Aggressive contribution  "))

    assert created["name"] == "Aggressive contribution"
    assert created["monthly_contribution"] == 10_000.0
    assert created["annual_return_pct"] == 5.0
    assert created["is_archived"] is False
    assert created["wealth_goal_id"] == goal["id"]
    assert created["workspace_id"] == main._ws_id(db)
    assert set(created.keys()) == {
        "id", "workspace_id", "wealth_goal_id", "name",
        "monthly_contribution", "annual_return_pct", "is_archived",
        "created_at", "updated_at",
    }


# 2. active list
def test_active_list_excludes_archived_by_default():
    db = make_session()
    goal = make_goal(db)
    active = create_scenario(db, goal["id"], **default_scenario_fields(name="Active"))
    archived = create_scenario(db, goal["id"], **default_scenario_fields(name="Archived"))
    update_scenario(db, goal["id"], archived["id"], is_archived=True)

    assert [row["id"] for row in list_scenarios(db, goal["id"])] == [active["id"]]


# 3. include_archived list
def test_include_archived_lists_both():
    db = make_session()
    goal = make_goal(db)
    active = create_scenario(db, goal["id"], **default_scenario_fields(name="Active"))
    archived = create_scenario(db, goal["id"], **default_scenario_fields(name="Archived"))
    update_scenario(db, goal["id"], archived["id"], is_archived=True)

    assert {row["id"] for row in list_scenarios(db, goal["id"], include_archived=True)} == {active["id"], archived["id"]}


# 4. update name
def test_update_name():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())

    updated = update_scenario(db, goal["id"], created["id"], name="Renamed scenario")

    assert updated["id"] == created["id"]
    assert updated["name"] == "Renamed scenario"


# 5. update contribution
def test_update_contribution():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())

    updated = update_scenario(db, goal["id"], created["id"], monthly_contribution=15_000.0)

    assert updated["monthly_contribution"] == 15_000.0
    assert updated["annual_return_pct"] == 5.0


# 6. update return
def test_update_return():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())

    updated = update_scenario(db, goal["id"], created["id"], annual_return_pct=7.5)

    assert updated["annual_return_pct"] == 7.5
    assert updated["monthly_contribution"] == 10_000.0


# 7. archive
def test_archive():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())

    archived = update_scenario(db, goal["id"], created["id"], is_archived=True)

    assert archived["is_archived"] is True
    assert list_scenarios(db, goal["id"]) == []


# 8. restore
def test_restore():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())
    update_scenario(db, goal["id"], created["id"], is_archived=True)

    restored = update_scenario(db, goal["id"], created["id"], is_archived=False)

    assert restored["is_archived"] is False
    assert [row["id"] for row in list_scenarios(db, goal["id"])] == [created["id"]]


# 9. archived scenario immutable except restore
def test_archived_scenario_rejects_edits_but_allows_restore():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())
    update_scenario(db, goal["id"], created["id"], is_archived=True)

    with pytest.raises(HTTPException) as name_error:
        update_scenario(db, goal["id"], created["id"], name="New name")
    assert name_error.value.status_code == 409

    with pytest.raises(HTTPException) as contribution_error:
        update_scenario(db, goal["id"], created["id"], monthly_contribution=1.0)
    assert contribution_error.value.status_code == 409

    with pytest.raises(HTTPException) as combined_error:
        update_scenario(db, goal["id"], created["id"], name="New name", is_archived=False)
    assert combined_error.value.status_code == 409

    restored = update_scenario(db, goal["id"], created["id"], is_archived=False)
    assert restored["is_archived"] is False
    assert restored["name"] == "Aggressive contribution"


# 10. parent archived rejects create
def test_archived_goal_rejects_create():
    db = make_session()
    goal = make_goal(db)
    archive_goal(db, goal["id"])

    with pytest.raises(HTTPException) as error:
        create_scenario(db, goal["id"], **default_scenario_fields())
    assert error.value.status_code == 409
    assert "Archived wealth goals" in error.value.detail


# 11. parent archived rejects update
def test_archived_goal_rejects_update():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())
    archive_goal(db, goal["id"])

    with pytest.raises(HTTPException) as error:
        update_scenario(db, goal["id"], created["id"], name="New name")
    assert error.value.status_code == 409
    assert "archived" in error.value.detail.lower()


# 12. parent archived rejects archive
def test_archived_goal_rejects_archiving_its_scenario():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())
    archive_goal(db, goal["id"])

    with pytest.raises(HTTPException) as error:
        update_scenario(db, goal["id"], created["id"], is_archived=True)
    assert error.value.status_code == 409


# 13. parent archived rejects restore
def test_archived_goal_rejects_restoring_its_scenario():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())
    update_scenario(db, goal["id"], created["id"], is_archived=True)
    archive_goal(db, goal["id"])

    with pytest.raises(HTTPException) as error:
        update_scenario(db, goal["id"], created["id"], is_archived=False)
    assert error.value.status_code == 409


# 14. parent archived still allows scenario reads
def test_archived_goal_still_allows_scenario_reads():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())
    archive_goal(db, goal["id"])

    rows = list_scenarios(db, goal["id"], include_archived=True)
    assert [row["id"] for row in rows] == [created["id"]]


# 15. workspace isolation
def test_foreign_workspace_scenario_is_invisible():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())

    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    foreign_scenario = GoalScenario(
        workspace_id=other_workspace.id,
        wealth_goal_id=goal["id"],
        name="Foreign",
        monthly_contribution=1.0,
        annual_return_pct=1.0,
    )
    db.add(foreign_scenario)
    db.commit()

    rows = list_scenarios(db, goal["id"], include_archived=True)
    assert [row["id"] for row in rows] == [created["id"]]

    with pytest.raises(HTTPException) as error:
        update_scenario(db, goal["id"], foreign_scenario.id, name="Renamed")
    assert error.value.status_code == 404


# 16. foreign goal
def test_foreign_goal_returns_404():
    db = make_session()
    current_workspace_id = main._ws_id(db)
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    foreign_goal = WealthGoal(
        workspace_id=other_workspace.id,
        name="Private Goal",
        goal_type="OTHER",
        target_amount=100.0,
        currency="THB",
        priority="LOW",
    )
    db.add(foreign_goal)
    db.commit()
    assert foreign_goal.workspace_id != current_workspace_id

    with pytest.raises(HTTPException) as error:
        create_scenario(db, foreign_goal.id, **default_scenario_fields())
    assert error.value.status_code == 404
    assert error.value.detail == "Wealth goal not found"


# 17. foreign scenario
def test_foreign_scenario_returns_404():
    db = make_session()
    goal_one = make_goal(db, name="Goal One")
    goal_two = make_goal(db, name="Goal Two")
    scenario = create_scenario(db, goal_one["id"], **default_scenario_fields())

    with pytest.raises(HTTPException) as error:
        update_scenario(db, goal_two["id"], scenario["id"], name="Wrong goal")
    assert error.value.status_code == 404
    assert error.value.detail == "Goal scenario not found"


# 18. blank name
def test_create_rejects_blank_name():
    with pytest.raises(ValidationError):
        main.GoalScenarioCreate(**default_scenario_fields(name="   "))
    with pytest.raises(ValidationError):
        main.GoalScenarioUpdate(name="   ")


# 19. invalid contribution
@pytest.mark.parametrize("contribution", [-1.0, -0.01])
def test_create_rejects_negative_contribution(contribution):
    with pytest.raises(ValidationError):
        main.GoalScenarioCreate(**default_scenario_fields(monthly_contribution=contribution))


def test_update_rejects_negative_contribution():
    with pytest.raises(ValidationError):
        main.GoalScenarioUpdate(monthly_contribution=-1.0)


# 20. non-finite contribution
@pytest.mark.parametrize("contribution", [float("nan"), float("inf"), -math.inf])
def test_create_rejects_non_finite_contribution(contribution):
    with pytest.raises(ValidationError):
        main.GoalScenarioCreate(**default_scenario_fields(monthly_contribution=contribution))


# 21. annual return <= -100
@pytest.mark.parametrize("rate", [-100.0, -150.0])
def test_create_rejects_return_at_or_below_negative_100(rate):
    with pytest.raises(ValidationError):
        main.GoalScenarioCreate(**default_scenario_fields(annual_return_pct=rate))


def test_update_rejects_return_at_or_below_negative_100():
    with pytest.raises(ValidationError):
        main.GoalScenarioUpdate(annual_return_pct=-100.0)


# 22. non-finite return
@pytest.mark.parametrize("rate", [float("nan"), float("inf"), -math.inf])
def test_create_rejects_non_finite_return(rate):
    with pytest.raises(ValidationError):
        main.GoalScenarioCreate(**default_scenario_fields(annual_return_pct=rate))


def test_update_requires_a_field():
    with pytest.raises(ValidationError):
        main.GoalScenarioUpdate()


# 23. duplicate assumptions allowed
def test_duplicate_assumptions_and_names_are_allowed():
    db = make_session()
    goal = make_goal(db)

    first = create_scenario(db, goal["id"], **default_scenario_fields())
    second = create_scenario(db, goal["id"], **default_scenario_fields())

    assert first["id"] != second["id"]
    assert len(list_scenarios(db, goal["id"])) == 2


# 24. multiple scenarios per goal
def test_multiple_scenarios_per_goal():
    db = make_session()
    goal = make_goal(db)
    create_scenario(db, goal["id"], **default_scenario_fields(name="Conservative", monthly_contribution=5_000.0, annual_return_pct=2.0))
    create_scenario(db, goal["id"], **default_scenario_fields(name="Aggressive", monthly_contribution=20_000.0, annual_return_pct=8.0))

    names = {row["name"] for row in list_scenarios(db, goal["id"])}
    assert names == {"Conservative", "Aggressive"}


# 25. no computed outputs persisted
def test_no_computed_outputs_are_persisted():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())

    forbidden_keys = {
        "target_amount", "target_date", "starting_value", "designated_funding",
        "projected_value", "reach_date", "required_monthly_contribution",
        "funding_health", "note", "currency", "scenario_type", "probability",
    }
    assert forbidden_keys.isdisjoint(created.keys())
    row = db.query(GoalScenario).filter(GoalScenario.id == created["id"]).one()
    assert not hasattr(row, "target_amount")
    assert not hasattr(row, "projected_value")


# 26. no WealthGoal/Allocation mutation
def test_scenario_lifecycle_does_not_mutate_goal_or_allocations():
    db = make_session()
    goal = make_goal(db, target_amount=1_000_000.0)
    cash = CashAccount(workspace_id=main._ws_id(db), name="Savings", currency="THB", balance=500_000.0)
    db.add(cash)
    db.commit()
    allocation = asyncio.run(main.create_goal_funding_allocation(
        goal["id"], main.GoalFundingAllocationCreate(cash_account_id=cash.id, allocated_amount=300_000.0), db,
    ))

    created = create_scenario(db, goal["id"], **default_scenario_fields())
    update_scenario(db, goal["id"], created["id"], monthly_contribution=99_999.0)
    update_scenario(db, goal["id"], created["id"], is_archived=True)
    update_scenario(db, goal["id"], created["id"], is_archived=False)

    db.refresh(cash)
    refreshed_goal = db.query(WealthGoal).filter(WealthGoal.id == goal["id"]).one()
    refreshed_allocation = db.query(GoalFundingAllocation).filter(GoalFundingAllocation.id == allocation["id"]).one()

    assert refreshed_goal.target_amount == 1_000_000.0
    assert refreshed_allocation.allocated_amount == 300_000.0
    assert cash.balance == 500_000.0


# 27. no Cash/Portfolio/Transaction/Snapshot mutation
def test_scenario_lifecycle_does_not_mutate_cash_portfolio_or_ledger_state():
    db = make_session()
    goal = make_goal(db)
    workspace_id = main._ws_id(db)
    cash = CashAccount(workspace_id=workspace_id, name="Savings", currency="THB", balance=1234.0)
    portfolio = Portfolio(workspace_id=workspace_id, name="Core", cash_balance=5678.0)
    liability = Liability(workspace_id=workspace_id, name="Card", liability_type="CREDIT_CARD", balance=500.0, currency="THB")
    db.add_all([cash, portfolio, liability])
    db.commit()
    before_cash_transactions = db.query(CashAccountTransaction).count()
    before_investment_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()

    created = create_scenario(db, goal["id"], **default_scenario_fields())
    update_scenario(db, goal["id"], created["id"], annual_return_pct=9.0)
    update_scenario(db, goal["id"], created["id"], is_archived=True)

    db.refresh(cash)
    db.refresh(portfolio)
    db.refresh(liability)

    assert cash.balance == 1234.0
    assert portfolio.cash_balance == 5678.0
    assert liability.balance == 500.0
    assert db.query(CashAccountTransaction).count() == before_cash_transactions
    assert db.query(Transaction).count() == before_investment_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots


# 28. cascade ownership behavior: deleting the owning Workspace removes its
# GoalScenario rows (ORM-level cascade — matches WealthGoal/GoalFundingAllocation
# precedent, since SQLite does not enforce ondelete=CASCADE without an explicit
# PRAGMA this codebase does not set).
def test_deleting_workspace_cascades_its_scenarios():
    db = make_session()
    goal = make_goal(db)
    created = create_scenario(db, goal["id"], **default_scenario_fields())
    workspace = db.query(Workspace).filter(Workspace.id == main._ws_id(db)).one()

    db.delete(workspace)
    db.commit()

    assert db.query(GoalScenario).filter(GoalScenario.id == created["id"]).first() is None
