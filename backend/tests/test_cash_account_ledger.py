"""Focused direct-endpoint coverage for the prospective CashAccount ledger."""
import asyncio
import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
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
    payload = {"name": "Everyday Cash", "currency": "THB", "balance": 100.0}
    payload.update(overrides)
    return asyncio.run(main.create_cash_account(main.CashAccountCreate(**payload), db))


def start_tracking(db, account_id, effective_on="2026-08-25", observed_balance=100.0):
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
        "occurred_on": "2026-08-25",
        "category": "Salary",
    }
    payload.update(overrides)
    return asyncio.run(main.create_cash_account_transaction(account_id, main.CashAccountTransactionCreate(**payload), db))


def reconcile(db, account_id, **overrides):
    payload = {"observed_balance": 100.0, "occurred_on": "2026-08-25"}
    payload.update(overrides)
    return asyncio.run(main.reconcile_cash_account(account_id, main.CashAccountReconcile(**payload), db))


def list_activity(db, account_id):
    return asyncio.run(main.list_cash_account_transactions(account_id, db))


def update_account(db, account_id, **overrides):
    return asyncio.run(main.update_cash_account(account_id, main.CashAccountUpdate(**overrides), db))


def test_baseline_is_explicit_one_per_account_and_does_not_fabricate_history():
    db = make_session()
    account = create_account(db, balance=25.0)

    baseline = start_tracking(db, account["id"], effective_on="2026-08-20", observed_balance=125.0)

    assert baseline["effective_on"] == "2026-08-20"
    assert baseline["observed_balance"] == 125.0
    assert db.query(CashAccount).one().balance == 125.0
    assert list_activity(db, account["id"]) == []
    with pytest.raises(HTTPException, match="already started"):
        start_tracking(db, account["id"])
    assert db.query(CashAccountBaseline).count() == 1


def test_pre_tracking_balance_replacement_remains_legacy_observed_balance_behavior():
    db = make_session()
    account = create_account(db)

    updated = update_account(db, account["id"], balance=250.0)

    assert updated["balance"] == 250.0
    assert db.query(CashAccountTransaction).count() == 0


def test_income_and_expense_update_current_observed_balance_with_immutable_events():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"])

    income = add_activity(db, account["id"], amount=20.0)
    expense = add_activity(db, account["id"], transaction_type="EXPENSE", amount=30.0, category="Food")

    assert income["amount"] == 20.0 and income["signed_amount"] == 20.0
    assert expense["amount"] == 30.0 and expense["signed_amount"] == -30.0
    assert db.query(CashAccount).one().balance == 90.0
    assert [event["transaction_type"] for event in list_activity(db, account["id"])] == ["EXPENSE", "INCOME"]


def test_expense_cannot_make_observed_balance_negative():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"])

    with pytest.raises(HTTPException, match="cannot make"):
        add_activity(db, account["id"], transaction_type="EXPENSE", amount=101.0, category="Rent")

    assert db.query(CashAccount).one().balance == 100.0
    assert db.query(CashAccountTransaction).count() == 0


@pytest.mark.parametrize(
    "payload",
    [
        {"amount": 0},
        {"amount": -1},
        {"amount": float("inf")},
        {"amount": float("nan")},
        {"category": "  "},
        {"occurred_on": "not-a-date"},
    ],
)
def test_activity_requires_finite_positive_amount_category_and_calendar_date(payload):
    with pytest.raises(ValidationError):
        main.CashAccountTransactionCreate(**{
            "transaction_type": "INCOME", "amount": 10, "occurred_on": "2026-08-25", "category": "Salary", **payload,
        })


def test_activity_cannot_predate_baseline():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-25")

    with pytest.raises(HTTPException, match="predate"):
        add_activity(db, account["id"], occurred_on="2026-08-24")


def test_reconciliation_creates_signed_adjustments_or_no_meaningless_zero_event():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"])

    positive = reconcile(db, account["id"], observed_balance=140.0)
    negative = reconcile(db, account["id"], observed_balance=110.0)
    zero = reconcile(db, account["id"], observed_balance=110.0)

    assert positive["adjustment"]["transaction_type"] == "ADJUSTMENT"
    assert positive["adjustment"]["amount"] == 40.0
    assert positive["adjustment"]["signed_amount"] == 40.0
    assert negative["adjustment"]["amount"] == -30.0
    assert negative["adjustment"]["signed_amount"] == -30.0
    assert zero["adjustment"] is None
    assert db.query(CashAccount).one().balance == 110.0
    assert db.query(CashAccountTransaction).count() == 2


def test_post_tracking_direct_balance_patch_becomes_adjustment_not_silent_overwrite():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"])

    updated = update_account(db, account["id"], balance=75.0)

    event = db.query(CashAccountTransaction).one()
    assert updated["balance"] == 75.0
    assert event.transaction_type == "ADJUSTMENT"
    assert event.amount == -25.0
    assert event.category == "Reconciliation"


def test_archived_accounts_keep_history_but_reject_new_activity():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"])
    add_activity(db, account["id"])
    update_account(db, account["id"], is_archived=True)

    with pytest.raises(HTTPException, match="Archived"):
        add_activity(db, account["id"])
    assert len(list_activity(db, account["id"])) == 1


def test_workspace_isolation_and_investment_core_are_unchanged():
    db = make_session()
    workspace_id = main._ws_id(db)
    portfolio = Portfolio(workspace_id=workspace_id, name="Investment Core", cash_balance=500.0)
    foreign_workspace = Workspace(name="Other")
    db.add_all([portfolio, foreign_workspace])
    db.commit()
    foreign_account = CashAccount(workspace_id=foreign_workspace.id, name="Private", currency="THB", balance=20.0)
    db.add(foreign_account)
    db.commit()
    before_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()

    account = create_account(db)
    start_tracking(db, account["id"])
    add_activity(db, account["id"])
    with pytest.raises(HTTPException) as error:
        list_activity(db, foreign_account.id)

    db.refresh(portfolio)
    assert error.value.status_code == 404
    assert portfolio.cash_balance == 500.0
    assert db.query(Transaction).count() == before_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots


def test_failed_commit_rolls_back_both_ledger_event_and_balance_change(monkeypatch):
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"])
    original_commit = db.commit

    def fail_commit():
        raise RuntimeError("simulated commit failure")

    monkeypatch.setattr(db, "commit", fail_commit)
    with pytest.raises(RuntimeError, match="simulated"):
        add_activity(db, account["id"])
    monkeypatch.setattr(db, "commit", original_commit)

    assert db.query(CashAccountTransaction).count() == 0
    assert db.query(CashAccount).one().balance == 100.0
