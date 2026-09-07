"""Focused tests for the bounded workspace/month Cash Flow reporting read path."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import (
    Base,
    CashAccount,
    CashAccountBaseline,
    CashAccountTransaction,
    Portfolio,
    PortfolioSnapshot,
    Transaction,
    Workspace,
)
import models.asset  # noqa: F401 — registers Asset tables referenced by ledger models.
import models.registry_finding  # noqa: F401 — registers registry tables referenced by Base metadata.
import main


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def create_account(db, **overrides):
    payload = {"name": "Everyday Cash", "currency": "THB", "balance": 1000.0}
    payload.update(overrides)
    return asyncio.run(main.create_cash_account(main.CashAccountCreate(**payload), db))


def start_tracking(db, account_id, effective_on="2026-08-01", observed_balance=1000.0):
    return asyncio.run(
        main.create_cash_account_baseline(
            account_id,
            main.CashAccountBaselineCreate(effective_on=effective_on, observed_balance=observed_balance),
            db,
        )
    )


def add_activity(db, account_id, **overrides):
    payload = {
        "transaction_type": "INCOME",
        "amount": 10.0,
        "occurred_on": "2026-08-15",
        "category": "Salary",
    }
    payload.update(overrides)
    return asyncio.run(main.create_cash_account_transaction(account_id, main.CashAccountTransactionCreate(**payload), db))


def update_account(db, account_id, **overrides):
    return asyncio.run(main.update_cash_account(account_id, main.CashAccountUpdate(**overrides), db))


def report(db, month):
    return asyncio.run(main.get_cash_flow_report(month, db))


def test_month_filter_is_inclusive_and_baseline_is_not_a_transaction():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-07-01")
    add_activity(db, account["id"], occurred_on="2026-07-31", amount=5.0)
    add_activity(db, account["id"], occurred_on="2026-08-01", amount=10.0)
    add_activity(db, account["id"], occurred_on="2026-08-31", amount=20.0)
    add_activity(db, account["id"], occurred_on="2026-09-01", amount=40.0)

    august = report(db, "2026-08")

    assert august["month"] == "2026-08"
    assert [(row["occurred_on"], row["amount"]) for row in august["events"]] == [
        ("2026-08-31", 20.0),
        ("2026-08-01", 10.0),
    ]
    assert db.query(CashAccountBaseline).count() == 1
    assert db.query(CashAccountTransaction).count() == 4


def test_reporting_enforces_the_explicit_baseline_boundary():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-15")
    # This row represents stale/corrupt data that the mutation route would
    # reject; the read path must still fail closed around the baseline.
    db.add(CashAccountTransaction(
        workspace_id=account["workspace_id"],
        cash_account_id=account["id"],
        transaction_type="INCOME",
        amount=999.0,
        occurred_on="2026-08-01",
        category="Pre-tracking",
    ))
    db.commit()

    assert report(db, "2026-08")["events"] == []


def test_archived_account_history_remains_visible():
    db = make_session()
    account = create_account(db, name="Old Reserve")
    start_tracking(db, account["id"])
    add_activity(db, account["id"], amount=75.0)
    update_account(db, account["id"], is_archived=True)

    events = report(db, "2026-08")["events"]

    assert len(events) == 1
    assert events[0]["account_name"] == "Old Reserve"
    assert events[0]["account_is_archived"] is True


def test_workspace_isolation_and_investment_rows_are_untouched():
    db = make_session()
    workspace_id = main._ws_id(db)
    portfolio = Portfolio(workspace_id=workspace_id, name="Investment Core", cash_balance=500.0)
    foreign_workspace = Workspace(name="Other")
    db.add_all([portfolio, foreign_workspace])
    db.commit()

    current = create_account(db, name="Current")
    start_tracking(db, current["id"])
    add_activity(db, current["id"], amount=25.0)
    foreign_account = CashAccount(
        workspace_id=foreign_workspace.id,
        name="Private",
        currency="THB",
        balance=20.0,
    )
    db.add(foreign_account)
    db.commit()
    db.add(CashAccountBaseline(cash_account_id=foreign_account.id, effective_on="2026-08-01", observed_balance=20.0))
    db.add(CashAccountTransaction(
        workspace_id=foreign_workspace.id,
        cash_account_id=foreign_account.id,
        transaction_type="INCOME",
        amount=999.0,
        occurred_on="2026-08-15",
        category="Private",
    ))
    db.commit()
    before_investment_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()
    before_cash_transactions = db.query(CashAccountTransaction).count()

    result = report(db, "2026-08")

    assert [row["account_name"] for row in result["events"]] == ["Current"]
    db.refresh(portfolio)
    assert portfolio.cash_balance == 500.0
    assert db.query(Transaction).count() == before_investment_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots
    assert db.query(CashAccountTransaction).count() == before_cash_transactions


def test_invalid_month_is_rejected_without_mutation():
    db = make_session()
    with pytest.raises(HTTPException) as error:
        report(db, "2026-13")
    assert error.value.status_code == 422
    assert db.query(CashAccountTransaction).count() == 0
