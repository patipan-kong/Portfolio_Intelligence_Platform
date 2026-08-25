"""Focused direct-endpoint coverage for the standalone Cash Accounts v1 API."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import Base, CashAccount, Portfolio, PortfolioSnapshot, Transaction, Workspace
import models.asset  # noqa: F401 — registers Asset tables referenced by ledger models.
import models.registry_finding  # noqa: F401 — registers registry tables referenced by Base metadata.
import main


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def create(db, **overrides):
    payload = {"name": "Emergency Fund", "currency": "THB"}
    payload.update(overrides)
    return asyncio.run(main.create_cash_account(main.CashAccountCreate(**payload), db))


def update(db, account_id, **fields):
    return asyncio.run(main.update_cash_account(account_id, main.CashAccountUpdate(**fields), db))


def list_accounts(db, include_archived=False):
    return asyncio.run(main.list_cash_accounts(include_archived=include_archived, db=db))


def test_create_default_balance_and_active_list():
    db = make_session()
    created = create(db, name=" Savings ", institution=" SCB ")

    assert created["name"] == "Savings"
    assert created["institution"] == "SCB"
    assert created["currency"] == "THB"
    assert created["balance"] == 0.0
    assert created["is_archived"] is False
    assert list_accounts(db) == [created]


def test_metadata_and_current_balance_updates_replace_the_observed_value():
    db = make_session()
    account = create(db, balance=100.0)

    metadata = update(db, account["id"], name="Travel Cash", institution=None)
    changed_balance = update(db, account["id"], balance=250.5)

    assert metadata["name"] == "Travel Cash"
    assert metadata["institution"] is None
    assert changed_balance["balance"] == 250.5
    assert db.query(CashAccount).one().balance == 250.5


def test_archive_is_hidden_by_default_and_can_be_included_and_restored():
    db = make_session()
    account = create(db)

    archived = update(db, account["id"], is_archived=True)
    assert archived["is_archived"] is True
    assert list_accounts(db) == []
    assert list_accounts(db, include_archived=True) == [archived]

    restored = update(db, account["id"], is_archived=False)
    assert restored["is_archived"] is False
    assert list_accounts(db) == [restored]


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "   ", "currency": "THB"},
        {"name": "Cash", "currency": "USD"},
        {"name": "Cash", "currency": "THB", "balance": -1.0},
        {"name": "Cash", "currency": "THB", "balance": float("inf")},
        {"name": "Cash", "currency": "THB", "balance": float("nan")},
    ],
)
def test_create_validation_rejects_blank_name_unsupported_currency_and_invalid_balance(payload):
    with pytest.raises(ValidationError):
        main.CashAccountCreate(**payload)


def test_update_requires_a_field_and_rejects_invalid_values():
    db = make_session()
    account = create(db)
    with pytest.raises(ValidationError):
        main.CashAccountUpdate()
    with pytest.raises(ValidationError):
        main.CashAccountUpdate(name=" ")
    with pytest.raises(ValidationError):
        main.CashAccountUpdate(balance=-0.01)
    with pytest.raises(ValidationError):
        main.CashAccountUpdate(balance=float("inf"))
    assert db.query(CashAccount).filter_by(id=account["id"]).one().balance == 0.0


def test_foreign_workspace_account_is_not_found_for_update():
    db = make_session()
    current_workspace_id = main._ws_id(db)
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    foreign_account = CashAccount(workspace_id=other_workspace.id, name="Private", currency="THB", balance=50.0)
    db.add(foreign_account)
    db.commit()

    assert foreign_account.workspace_id != current_workspace_id
    with pytest.raises(HTTPException) as error:
        update(db, foreign_account.id, balance=100.0)
    assert error.value.status_code == 404
    assert error.value.detail == "Cash account not found"


def test_cash_mutations_do_not_change_portfolio_brokerage_cash_or_investment_rows():
    db = make_session()
    workspace_id = main._ws_id(db)
    portfolio = Portfolio(workspace_id=workspace_id, name="Investment Core", cash_balance=1234.0)
    db.add(portfolio)
    db.commit()
    before_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()

    account = create(db, balance=400.0)
    update(db, account["id"], balance=900.0)
    update(db, account["id"], is_archived=True)
    db.refresh(portfolio)

    assert portfolio.cash_balance == 1234.0
    assert db.query(Transaction).count() == before_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots
