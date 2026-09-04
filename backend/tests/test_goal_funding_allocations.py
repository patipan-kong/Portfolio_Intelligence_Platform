"""Focused direct-endpoint coverage for Goal Funding Allocation Foundation
(Phase 6, Milestone 2).

Scope: "this amount from this source is designated toward this goal." No
progress, funding-gap, or capacity validation is exercised here because none
exists yet — see models.database.GoalFundingAllocation for why over-
allocation checking against a source's current value is deliberately
deferred to a future read/composition milestone.
"""
import asyncio
from datetime import datetime
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from models.database import (
    Base,
    CashAccount,
    CashAccountTransaction,
    GoalFundingAllocation,
    GoalFundingAllocationHistory,
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
        "name": "Wedding",
        "goal_type": "WEDDING",
        "target_amount": 500_000.0,
        "currency": "THB",
        "priority": "HIGH",
    }
    payload.update(overrides)
    return asyncio.run(main.create_wealth_goal(main.WealthGoalCreate(**payload), db))


def make_cash_account(db, workspace_id=None, **overrides):
    ws = workspace_id if workspace_id is not None else main._ws_id(db)
    fields = {"workspace_id": ws, "name": "Wedding Savings", "currency": "THB", "balance": 300_000.0}
    fields.update(overrides)
    account = CashAccount(**fields)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def make_portfolio(db, workspace_id=None, **overrides):
    ws = workspace_id if workspace_id is not None else main._ws_id(db)
    fields = {"workspace_id": ws, "name": "Long-term Portfolio"}
    fields.update(overrides)
    portfolio = Portfolio(**fields)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def create_allocation(db, goal_id, **fields):
    body = main.GoalFundingAllocationCreate(**fields)
    return asyncio.run(main.create_goal_funding_allocation(goal_id, body, db))


def update_allocation(db, goal_id, allocation_id, **fields):
    body = main.GoalFundingAllocationUpdate(**fields)
    return asyncio.run(main.update_goal_funding_allocation(goal_id, allocation_id, body, db))


def delete_allocation(db, goal_id, allocation_id):
    return asyncio.run(main.delete_goal_funding_allocation(goal_id, allocation_id, db))


def list_allocations(db, goal_id):
    return asyncio.run(main.list_goal_funding_allocations(goal_id, db))


def list_history(db, goal_id):
    return asyncio.run(main.list_goal_funding_allocation_history(goal_id, db))


# 1. create CashAccount allocation
def test_create_cash_account_allocation():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)

    created = create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)

    assert created["source_kind"] == "CASH_ACCOUNT"
    assert created["cash_account_id"] == cash.id
    assert created["portfolio_id"] is None
    assert created["source_name"] == "Wedding Savings"
    assert created["source_is_archived"] is False
    assert created["allocated_amount"] == 300_000.0
    assert created["currency"] == "THB"
    assert created["wealth_goal_id"] == goal["id"]


# 2. create Portfolio allocation
def test_create_portfolio_allocation():
    db = make_session()
    goal = make_goal(db, name="Retire by 55", goal_type="RETIREMENT", target_amount=20_000_000.0)
    portfolio = make_portfolio(db)

    created = create_allocation(db, goal["id"], portfolio_id=portfolio.id, allocated_amount=700_000.0)

    assert created["source_kind"] == "PORTFOLIO"
    assert created["portfolio_id"] == portfolio.id
    assert created["cash_account_id"] is None
    assert created["source_name"] == "Long-term Portfolio"
    assert created["source_is_archived"] is False


# 3. list allocations
def test_list_allocations_scoped_to_goal():
    db = make_session()
    wedding = make_goal(db)
    retirement = make_goal(db, name="Retire by 55", goal_type="RETIREMENT", target_amount=20_000_000.0)
    cash = make_cash_account(db)
    portfolio = make_portfolio(db)
    create_allocation(db, wedding["id"], cash_account_id=cash.id, allocated_amount=300_000.0)
    create_allocation(db, retirement["id"], portfolio_id=portfolio.id, allocated_amount=700_000.0)

    wedding_rows = list_allocations(db, wedding["id"])
    assert len(wedding_rows) == 1
    assert wedding_rows[0]["cash_account_id"] == cash.id


# 4. update amount
def test_update_amount_changes_existing_row_not_a_new_one():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)
    created = create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)

    updated = update_allocation(db, goal["id"], created["id"], allocated_amount=250_000.0)

    assert updated["id"] == created["id"]
    assert updated["allocated_amount"] == 250_000.0
    assert len(list_allocations(db, goal["id"])) == 1


# 5. removal semantics: hard delete
def test_delete_removes_the_allocation():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)
    created = create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)

    result = delete_allocation(db, goal["id"], created["id"])

    assert result == {"deleted": created["id"]}
    assert list_allocations(db, goal["id"]) == []
    with pytest.raises(HTTPException) as error:
        update_allocation(db, goal["id"], created["id"], allocated_amount=1.0)
    assert error.value.status_code == 404


# 6. exactly-one-source validation
def test_exactly_one_source_is_required():
    with pytest.raises(ValidationError):
        main.GoalFundingAllocationCreate(allocated_amount=1.0)
    with pytest.raises(ValidationError):
        main.GoalFundingAllocationCreate(cash_account_id=1, portfolio_id=1, allocated_amount=1.0)


# 7. positive finite amount validation
@pytest.mark.parametrize("amount", [0.0, -1.0, float("nan"), float("inf"), -math.inf])
def test_create_rejects_invalid_amounts(amount):
    with pytest.raises(ValidationError):
        main.GoalFundingAllocationCreate(cash_account_id=1, allocated_amount=amount)


def test_update_rejects_invalid_amounts():
    with pytest.raises(ValidationError):
        main.GoalFundingAllocationUpdate(allocated_amount=0.0)
    with pytest.raises(ValidationError):
        main.GoalFundingAllocationUpdate(allocated_amount=float("nan"))


# 8. THB-only
def test_create_rejects_non_thb_currency():
    with pytest.raises(ValidationError):
        main.GoalFundingAllocationCreate(cash_account_id=1, allocated_amount=1.0, currency="USD")


# 9. workspace isolation
def test_foreign_workspace_allocation_is_invisible():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)
    other_cash = make_cash_account(db, name="Second Account")  # distinct source so the goal x source unique constraint does not fire
    created = create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)

    # Simulates a defense-in-depth scenario: a row whose wealth_goal_id happens
    # to match a goal the current workspace owns, but whose own workspace_id
    # does not — the workspace_id filter in list/lookup must still exclude it,
    # not rely on wealth_goal_id scoping alone.
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    foreign_allocation = GoalFundingAllocation(
        workspace_id=other_workspace.id,
        wealth_goal_id=goal["id"],
        cash_account_id=other_cash.id,
        allocated_amount=1.0,
    )
    db.add(foreign_allocation)
    db.commit()

    rows = list_allocations(db, goal["id"])
    assert [row["id"] for row in rows] == [created["id"]]

    with pytest.raises(HTTPException) as error:
        update_allocation(db, goal["id"], foreign_allocation.id, allocated_amount=2.0)
    assert error.value.status_code == 404


# 10. foreign goal rejected
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
        create_allocation(db, foreign_goal.id, cash_account_id=1, allocated_amount=1.0)
    assert error.value.status_code == 404
    assert error.value.detail == "Wealth goal not found"


# 11. foreign source rejected
def test_foreign_cash_account_and_portfolio_rejected():
    db = make_session()
    goal = make_goal(db)
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    foreign_cash = make_cash_account(db, workspace_id=other_workspace.id)
    foreign_portfolio = make_portfolio(db, workspace_id=other_workspace.id)

    with pytest.raises(HTTPException) as cash_error:
        create_allocation(db, goal["id"], cash_account_id=foreign_cash.id, allocated_amount=1.0)
    assert cash_error.value.status_code == 404

    with pytest.raises(HTTPException) as portfolio_error:
        create_allocation(db, goal["id"], portfolio_id=foreign_portfolio.id, allocated_amount=1.0)
    assert portfolio_error.value.status_code == 404


# 12. archived goal rejects new allocation
def test_archived_goal_rejects_new_allocation():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)
    asyncio.run(main.update_wealth_goal(goal["id"], main.WealthGoalUpdate(is_archived=True), db))

    with pytest.raises(HTTPException) as error:
        create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=1.0)
    assert error.value.status_code == 409
    assert "Archived wealth goals" in error.value.detail


# 13. archived Cash source rejects new allocation
def test_archived_cash_source_rejects_new_allocation():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db, is_archived=True)

    with pytest.raises(HTTPException) as error:
        create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=1.0)
    assert error.value.status_code == 409
    assert "Archived cash accounts" in error.value.detail


# 14. Portfolio has no archive lifecycle in this codebase (no is_archived
# column; only a real DELETE endpoint exists). "Archived Portfolio source"
# is therefore not a reachable state — see final report §STOP-condition
# review / source-model findings. Portfolio deletion is instead covered by
# test_deleting_portfolio_cascades_its_allocations below.


# 15. existing allocation remains readable after source archive
def test_allocation_remains_readable_after_cash_source_archived():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)
    created = create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)

    updated_account = asyncio.run(main.update_cash_account(cash.id, main.CashAccountUpdate(is_archived=True), db))
    assert updated_account["is_archived"] is True

    rows = list_allocations(db, goal["id"])
    assert len(rows) == 1
    assert rows[0]["id"] == created["id"]
    assert rows[0]["source_is_archived"] is True


# 16. one Goal x Source allocation only
def test_duplicate_goal_source_pair_is_rejected():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)
    create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=100_000.0)

    with pytest.raises(HTTPException) as error:
        create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=50_000.0)
    assert error.value.status_code == 409
    assert len(list_allocations(db, goal["id"])) == 1


# 17. source can fund multiple different goals
def test_one_source_can_fund_multiple_goals():
    db = make_session()
    house = make_goal(db, name="House", goal_type="HOUSE", target_amount=4_000_000.0)
    retirement = make_goal(db, name="Retire by 55", goal_type="RETIREMENT", target_amount=20_000_000.0)
    portfolio = make_portfolio(db)

    create_allocation(db, house["id"], portfolio_id=portfolio.id, allocated_amount=500_000.0)
    create_allocation(db, retirement["id"], portfolio_id=portfolio.id, allocated_amount=700_000.0)

    assert len(list_allocations(db, house["id"])) == 1
    assert len(list_allocations(db, retirement["id"])) == 1


# 18. source total allocation is deterministically summable
def test_source_total_allocation_is_summable():
    db = make_session()
    house = make_goal(db, name="House", goal_type="HOUSE", target_amount=4_000_000.0)
    retirement = make_goal(db, name="Retire by 55", goal_type="RETIREMENT", target_amount=20_000_000.0)
    portfolio = make_portfolio(db)
    create_allocation(db, house["id"], portfolio_id=portfolio.id, allocated_amount=500_000.0)
    create_allocation(db, retirement["id"], portfolio_id=portfolio.id, allocated_amount=700_000.0)

    total = (
        db.query(GoalFundingAllocation)
        .filter(GoalFundingAllocation.portfolio_id == portfolio.id)
        .with_entities(GoalFundingAllocation.allocated_amount)
        .all()
    )
    assert sum(row[0] for row in total) == 1_200_000.0


# 19. no Cash balance/ledger mutation
def test_allocation_lifecycle_does_not_mutate_cash_balance_or_ledger():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db, balance=1234.0)
    before_transactions = db.query(CashAccountTransaction).count()

    created = create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)
    update_allocation(db, goal["id"], created["id"], allocated_amount=250_000.0)
    delete_allocation(db, goal["id"], created["id"])
    db.refresh(cash)

    assert cash.balance == 1234.0
    assert db.query(CashAccountTransaction).count() == before_transactions


# 20. no Portfolio transaction/snapshot mutation
def test_allocation_lifecycle_does_not_mutate_portfolio_investment_state():
    db = make_session()
    goal = make_goal(db, name="Retire by 55", goal_type="RETIREMENT", target_amount=20_000_000.0)
    portfolio = make_portfolio(db, cash_balance=5678.0)
    before_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()

    created = create_allocation(db, goal["id"], portfolio_id=portfolio.id, allocated_amount=700_000.0)
    update_allocation(db, goal["id"], created["id"], allocated_amount=500_000.0)
    delete_allocation(db, goal["id"], created["id"])
    db.refresh(portfolio)

    assert portfolio.cash_balance == 5678.0
    assert db.query(Transaction).count() == before_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots


# 21. no Portfolio Goal Wizard mutation
def test_allocation_lifecycle_does_not_touch_portfolio_goal_wizard_fields():
    db = make_session()
    goal = make_goal(db, name="Retire by 55", goal_type="RETIREMENT", target_amount=20_000_000.0)
    portfolio = make_portfolio(
        db,
        goal_type="WEDDING",
        goal_priority="ESSENTIAL",
        goal_target_date="2027-05-01",
        goal_target_value=500_000.0,
        risk_personality="MODERATE",
    )

    created = create_allocation(db, goal["id"], portfolio_id=portfolio.id, allocated_amount=700_000.0)
    update_allocation(db, goal["id"], created["id"], allocated_amount=500_000.0)
    db.refresh(portfolio)

    assert portfolio.goal_type == "WEDDING"
    assert portfolio.goal_priority == "ESSENTIAL"
    assert portfolio.goal_target_date == "2027-05-01"
    assert portfolio.goal_target_value == 500_000.0
    assert portfolio.risk_personality == "MODERATE"


# 22. no Liability mutation (Net Worth has no backend persistence to mutate)
def test_allocation_lifecycle_does_not_mutate_liabilities():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)
    liability = Liability(workspace_id=main._ws_id(db), name="Card", liability_type="CREDIT_CARD", balance=500.0, currency="THB")
    db.add(liability)
    db.commit()

    created = create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)
    update_allocation(db, goal["id"], created["id"], allocated_amount=250_000.0)
    delete_allocation(db, goal["id"], created["id"])
    db.refresh(liability)

    assert liability.balance == 500.0


# Portfolio deletion is this codebase's only real hard-delete path among the
# two source types (CashAccount/Liability/WealthGoal are archive-only).
# GoalFundingAllocation.portfolio_id cascades at the ORM level (not just the
# FK's ondelete=CASCADE, which SQLite does not enforce without an explicit
# PRAGMA this codebase does not set) so deleting a funding-source Portfolio
# never leaves an orphaned allocation row.
def test_deleting_portfolio_cascades_its_allocations():
    db = make_session()
    goal = make_goal(db, name="Retire by 55", goal_type="RETIREMENT", target_amount=20_000_000.0)
    make_portfolio(db, name="Other Portfolio")  # so delete_portfolio's "last portfolio" guard doesn't block this
    portfolio = make_portfolio(db, name="Funding Portfolio")
    create_allocation(db, goal["id"], portfolio_id=portfolio.id, allocated_amount=700_000.0)

    asyncio.run(main.delete_portfolio(portfolio.id, db))

    assert list_allocations(db, goal["id"]) == []
    assert db.query(GoalFundingAllocation).count() == 0
    history = list_history(db, goal["id"])
    assert len(history) == 2
    assert history[0] == {
        "id": history[0]["id"],
        "workspace_id": main._ws_id(db),
        "wealth_goal_id": goal["id"],
        "source_kind": "PORTFOLIO",
        "source_id": portfolio.id,
        "source_name": "Funding Portfolio",
        "action": "REMOVE",
        "previous_designated_amount": 700_000.0,
        "resulting_designated_amount": None,
        "currency": "THB",
        "recorded_at": history[0]["recorded_at"],
    }


def test_history_records_create_changed_update_and_remove_but_not_unchanged_update():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)

    created = create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)
    update_allocation(db, goal["id"], created["id"], allocated_amount=250_000.0)
    update_allocation(db, goal["id"], created["id"], allocated_amount=250_000.0)
    delete_allocation(db, goal["id"], created["id"])

    history = list_history(db, goal["id"])
    assert [(event["action"], event["previous_designated_amount"], event["resulting_designated_amount"]) for event in history] == [
        ("REMOVE", 250_000.0, None),
        ("UPDATE", 300_000.0, 250_000.0),
        ("CREATE", None, 300_000.0),
    ]
    assert all(event["source_kind"] == "CASH_ACCOUNT" for event in history)
    assert all(event["source_id"] == cash.id for event in history)
    assert all(event["source_name"] == "Wedding Savings" for event in history)


def test_history_snapshots_source_name_before_later_rename():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)
    created = create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)

    asyncio.run(main.update_cash_account(cash.id, main.CashAccountUpdate(name="Renamed Savings"), db))
    update_allocation(db, goal["id"], created["id"], allocated_amount=250_000.0)

    history = list_history(db, goal["id"])
    assert [(event["action"], event["source_name"]) for event in history] == [
        ("UPDATE", "Renamed Savings"),
        ("CREATE", "Wedding Savings"),
    ]


def test_history_is_workspace_isolated_and_archived_goal_remains_readable():
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)
    create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    db.add(GoalFundingAllocationHistory(
        workspace_id=other_workspace.id,
        wealth_goal_id=goal["id"],
        source_kind="CASH_ACCOUNT",
        source_id=cash.id,
        source_name="Foreign evidence",
        action="CREATE",
        previous_designated_amount=None,
        resulting_designated_amount=1.0,
        currency="THB",
    ))
    db.commit()

    asyncio.run(main.update_wealth_goal(goal["id"], main.WealthGoalUpdate(is_archived=True), db))
    history = list_history(db, goal["id"])
    assert [event["source_name"] for event in history] == ["Wedding Savings"]
    allocation = list_allocations(db, goal["id"])[0]
    with pytest.raises(HTTPException) as error:
        update_allocation(db, goal["id"], allocation["id"], allocated_amount=250_000.0)
    assert error.value.status_code == 409


def test_history_order_is_deterministic_when_events_share_a_timestamp():
    db = make_session()
    goal = make_goal(db)
    shared_time = datetime(2026, 9, 4, 10, 0, 0)
    for name, amount in [("First", 100.0), ("Second", 200.0)]:
        db.add(GoalFundingAllocationHistory(
            workspace_id=main._ws_id(db),
            wealth_goal_id=goal["id"],
            source_kind="CASH_ACCOUNT",
            source_id=1,
            source_name=name,
            action="CREATE",
            previous_designated_amount=None,
            resulting_designated_amount=amount,
            currency="THB",
            recorded_at=shared_time,
        ))
    db.commit()

    assert [event["source_name"] for event in list_history(db, goal["id"])] == ["Second", "First"]


def test_failed_history_write_rolls_back_the_allocation_and_event(monkeypatch):
    db = make_session()
    goal = make_goal(db)
    cash = make_cash_account(db)

    def malformed_history_write(session, **kwargs):
        session.add(GoalFundingAllocationHistory(
            workspace_id=kwargs["workspace_id"],
            wealth_goal_id=kwargs["wealth_goal_id"],
            source_kind=kwargs["source_kind"],
            source_id=kwargs["source_id"],
            source_name=kwargs["source_name"],
            action="CREATE",
            previous_designated_amount=1.0,
            resulting_designated_amount=kwargs["resulting_designated_amount"],
            currency=kwargs["currency"],
        ))

    monkeypatch.setattr(main, "_append_goal_funding_allocation_history", malformed_history_write)
    with pytest.raises(IntegrityError):
        create_allocation(db, goal["id"], cash_account_id=cash.id, allocated_amount=300_000.0)

    assert db.query(GoalFundingAllocation).count() == 0
    assert db.query(GoalFundingAllocationHistory).count() == 0
