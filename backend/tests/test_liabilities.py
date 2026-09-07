"""Focused direct-endpoint coverage for Liability Foundation v1."""
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
        "name": "Home Loan",
        "liability_type": "MORTGAGE",
        "balance": 2500000.0,
        "currency": "THB",
    }
    payload.update(overrides)
    return asyncio.run(main.create_liability(main.LiabilityCreate(**payload), db))


def update(db, liability_id, **fields):
    return asyncio.run(main.update_liability(liability_id, main.LiabilityUpdate(**fields), db))


def list_liabilities(db, include_archived=False):
    return asyncio.run(main.list_liabilities(include_archived=include_archived, db=db))


def test_create_valid_liability_returns_the_frozen_v1_contract():
    db = make_session()
    created = create(db, name=" Home Loan ", lender=" SCB ", note="  observed manually  ")

    assert created["name"] == "Home Loan"
    assert created["liability_type"] == "MORTGAGE"
    assert created["lender"] == "SCB"
    assert created["balance"] == 2500000.0
    assert created["currency"] == "THB"
    assert created["note"] == "observed manually"
    assert created["is_archived"] is False
    assert created["workspace_id"] == main._ws_id(db)


def test_normal_list_is_active_only_and_include_archived_supports_management():
    db = make_session()
    active = create(db, name="Active")
    archived = create(db, name="Archived", balance=100.0)
    update(db, archived["id"], is_archived=True)

    assert [row["id"] for row in list_liabilities(db)] == [active["id"]]
    assert {row["id"] for row in list_liabilities(db, include_archived=True)} == {active["id"], archived["id"]}


def test_metadata_and_observed_balance_updates_are_replacements_only():
    db = make_session()
    liability = create(db, balance=1000.0)

    changed = update(db, liability["id"], name="Personal Loan", liability_type="PERSONAL_LOAN", lender="KBank", note="updated")
    observed = update(db, liability["id"], balance=875.5)

    assert changed["name"] == "Personal Loan"
    assert changed["liability_type"] == "PERSONAL_LOAN"
    assert changed["lender"] == "KBank"
    assert changed["note"] == "updated"
    assert observed["balance"] == 875.5
    assert db.query(Liability).one().balance == 875.5


def test_zero_balance_is_allowed_and_remains_active_as_paid_off_state():
    db = make_session()
    liability = create(db, balance=0.0)

    assert liability["balance"] == 0.0
    assert liability in list_liabilities(db)
    assert db.query(Liability).one().is_archived is False


def test_archive_is_hidden_by_default_and_restore_preserves_identity():
    db = make_session()
    liability = create(db)

    archived = update(db, liability["id"], is_archived=True)
    assert archived["is_archived"] is True
    assert list_liabilities(db) == []
    assert list_liabilities(db, include_archived=True)[0]["id"] == liability["id"]

    restored = update(db, liability["id"], is_archived=False)
    assert restored["id"] == liability["id"]
    assert restored["is_archived"] is False
    assert list_liabilities(db)[0]["id"] == liability["id"]


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "   ", "liability_type": "OTHER", "balance": 1.0, "currency": "THB"},
        {"name": "Debt", "liability_type": "UNSUPPORTED", "balance": 1.0, "currency": "THB"},
        {"name": "Debt", "liability_type": "OTHER", "balance": -1.0, "currency": "THB"},
        {"name": "Debt", "liability_type": "OTHER", "balance": float("nan"), "currency": "THB"},
        {"name": "Debt", "liability_type": "OTHER", "balance": float("inf"), "currency": "THB"},
        {"name": "Debt", "liability_type": "OTHER", "balance": -math.inf, "currency": "THB"},
        {"name": "Debt", "liability_type": "OTHER", "balance": 1.0, "currency": "USD"},
    ],
)
def test_create_validation_rejects_invalid_v1_values(payload):
    with pytest.raises(ValidationError):
        main.LiabilityCreate(**payload)


def test_update_requires_a_field_and_rejects_invalid_values():
    with pytest.raises(ValidationError):
        main.LiabilityUpdate()
    with pytest.raises(ValidationError):
        main.LiabilityUpdate(name=" ")
    with pytest.raises(ValidationError):
        main.LiabilityUpdate(liability_type="UNSUPPORTED")
    with pytest.raises(ValidationError):
        main.LiabilityUpdate(balance=-0.01)
    with pytest.raises(ValidationError):
        main.LiabilityUpdate(balance=float("nan"))
    with pytest.raises(ValidationError):
        main.LiabilityUpdate(balance=float("inf"))
    with pytest.raises(ValidationError):
        main.LiabilityUpdate(currency="USD")


def test_foreign_workspace_lookup_returns_404_without_leaking_existence():
    db = make_session()
    current_workspace_id = main._ws_id(db)
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    foreign = Liability(
        workspace_id=other_workspace.id,
        name="Private",
        liability_type="OTHER",
        balance=50.0,
        currency="THB",
    )
    db.add(foreign)
    db.commit()

    assert foreign.workspace_id != current_workspace_id
    with pytest.raises(HTTPException) as error:
        update(db, foreign.id, balance=100.0)
    assert error.value.status_code == 404
    assert error.value.detail == "Liability not found"


def test_liability_mutations_do_not_change_cash_or_investment_state():
    db = make_session()
    workspace_id = main._ws_id(db)
    cash = CashAccount(workspace_id=workspace_id, name="Savings", currency="THB", balance=1234.0)
    portfolio = Portfolio(workspace_id=workspace_id, name="Core", cash_balance=5678.0)
    db.add_all([cash, portfolio])
    db.commit()
    before_cash_transactions = db.query(CashAccountTransaction).count()
    before_investment_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()

    liability = create(db, balance=1000.0)
    update(db, liability["id"], balance=900.0, is_archived=True)
    db.refresh(cash)
    db.refresh(portfolio)

    assert cash.balance == 1234.0
    assert portfolio.cash_balance == 5678.0
    assert db.query(CashAccountTransaction).count() == before_cash_transactions
    assert db.query(Transaction).count() == before_investment_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots
