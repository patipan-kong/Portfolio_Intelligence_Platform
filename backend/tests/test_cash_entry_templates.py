"""Focused direct-endpoint coverage for User-Triggered Cash-Entry Templates.

A template is workspace-owned convenience metadata that prefills the
existing Add income / Add expense form — never a financial fact. These
tests exist specifically to prove template CRUD has zero effect on
CashAccount.balance or CashAccountTransaction; only the existing
create_cash_account_transaction endpoint (exercised in
test_cash_account_ledger.py) creates ledger activity.
"""
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
    CashEntryTemplate,
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


def archive_account(db, account_id):
    return asyncio.run(main.update_cash_account(account_id, main.CashAccountUpdate(is_archived=True), db))


def create_template(db, **overrides):
    payload = {
        "name": "Monthly Salary",
        "transaction_type": "INCOME",
        "cash_account_id": overrides.pop("cash_account_id", None),
        "amount": 45000.0,
        "category": "Salary",
    }
    payload.update(overrides)
    return asyncio.run(main.create_cash_entry_template(main.CashEntryTemplateCreate(**payload), db))


def update_template(db, template_id, **fields):
    return asyncio.run(main.update_cash_entry_template(template_id, main.CashEntryTemplateUpdate(**fields), db))


def list_templates(db):
    return asyncio.run(main.list_cash_entry_templates(db))


def delete_template(db, template_id):
    return asyncio.run(main.delete_cash_entry_template(template_id, db))


# ─── CRUD ────────────────────────────────────────────────────────────────────

def test_create_valid_income_template_returns_the_frozen_contract():
    db = make_session()
    account = create_account(db)
    created = create_template(db, cash_account_id=account["id"], name="  Monthly Salary  ", note="  paycheck  ")

    assert created["name"] == "Monthly Salary"
    assert created["transaction_type"] == "INCOME"
    assert created["cash_account_id"] == account["id"]
    assert created["cash_account_name"] == "Everyday Cash"
    assert created["cash_account_is_archived"] is False
    assert created["amount"] == 45000.0
    assert created["category"] == "Salary"
    assert created["note"] == "paycheck"
    assert created["workspace_id"] == main._ws_id(db)
    assert "id" in created and "created_at" in created and "updated_at" in created


def test_create_valid_expense_template():
    db = make_session()
    account = create_account(db)
    created = create_template(
        db, cash_account_id=account["id"], name="Rent", transaction_type="EXPENSE", amount=15000.0, category="Housing"
    )

    assert created["transaction_type"] == "EXPENSE"
    assert created["amount"] == 15000.0
    assert created["category"] == "Housing"
    assert created["note"] is None


def test_list_templates_scoped_to_workspace_ordered_by_name():
    db = make_session()
    account = create_account(db)
    create_template(db, cash_account_id=account["id"], name="Zebra")
    create_template(db, cash_account_id=account["id"], name="Alpha")

    names = [row["name"] for row in list_templates(db)]
    assert names == ["Alpha", "Zebra"]


def test_update_template_metadata():
    db = make_session()
    account = create_account(db)
    other_account = create_account(db, name="Savings")
    template = create_template(db, cash_account_id=account["id"])

    updated = update_template(
        db,
        template["id"],
        name="Salary v2",
        transaction_type="EXPENSE",
        cash_account_id=other_account["id"],
        amount=100.0,
        category="Other",
        note="changed",
    )

    assert updated["name"] == "Salary v2"
    assert updated["transaction_type"] == "EXPENSE"
    assert updated["cash_account_id"] == other_account["id"]
    assert updated["amount"] == 100.0
    assert updated["category"] == "Other"
    assert updated["note"] == "changed"


def test_delete_template_removes_it_from_the_list():
    db = make_session()
    account = create_account(db)
    template = create_template(db, cash_account_id=account["id"])

    result = delete_template(db, template["id"])

    assert result == {"deleted": template["id"]}
    assert list_templates(db) == []
    assert db.query(CashEntryTemplate).count() == 0


# ─── Workspace / account isolation ──────────────────────────────────────────

def test_workspace_isolation_returns_404_without_leaking_existence():
    db = make_session()
    current_workspace_id = main._ws_id(db)
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    other_account = CashAccount(workspace_id=other_workspace.id, name="Private", currency="THB", balance=10.0)
    db.add(other_account)
    db.commit()
    foreign = CashEntryTemplate(
        workspace_id=other_workspace.id,
        name="Foreign",
        transaction_type="INCOME",
        cash_account_id=other_account.id,
        amount=1.0,
        category="X",
    )
    db.add(foreign)
    db.commit()

    assert foreign.workspace_id != current_workspace_id
    with pytest.raises(HTTPException) as error:
        update_template(db, foreign.id, amount=2.0)
    assert error.value.status_code == 404
    assert error.value.detail == "Cash entry template not found"
    with pytest.raises(HTTPException):
        delete_template(db, foreign.id)


def test_foreign_workspace_account_is_rejected_on_create():
    db = make_session()
    main._ws_id(db)  # establish the current default workspace before adding a foreign one
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    other_account = CashAccount(workspace_id=other_workspace.id, name="Private", currency="THB", balance=10.0)
    db.add(other_account)
    db.commit()

    with pytest.raises(HTTPException) as error:
        create_template(db, cash_account_id=other_account.id)
    assert error.value.status_code == 404
    assert db.query(CashEntryTemplate).count() == 0


def test_foreign_workspace_account_is_rejected_on_repoint():
    db = make_session()
    account = create_account(db)
    template = create_template(db, cash_account_id=account["id"])
    other_workspace = Workspace(name="Other")
    db.add(other_workspace)
    db.commit()
    other_account = CashAccount(workspace_id=other_workspace.id, name="Private", currency="THB", balance=10.0)
    db.add(other_account)
    db.commit()

    with pytest.raises(HTTPException) as error:
        update_template(db, template["id"], cash_account_id=other_account.id)
    assert error.value.status_code == 404


# ─── Create/update validation ───────────────────────────────────────────────

@pytest.mark.parametrize(
    "overrides",
    [
        {"name": "   "},
        {"category": "   "},
        {"amount": 0.0},
        {"amount": -1.0},
        {"amount": float("nan")},
        {"amount": float("inf")},
        {"transaction_type": "ADJUSTMENT"},
        {"transaction_type": "TRANSFER"},
        {"transaction_type": "INVESTMENT_TRANSFER"},
    ],
)
def test_create_validation_rejects_invalid_values(overrides):
    payload = {
        "name": "Template",
        "transaction_type": "INCOME",
        "cash_account_id": 1,
        "amount": 100.0,
        "category": "Cat",
    }
    payload.update(overrides)
    with pytest.raises(ValidationError):
        main.CashEntryTemplateCreate(**payload)


def test_update_requires_a_field_and_rejects_invalid_values():
    with pytest.raises(ValidationError):
        main.CashEntryTemplateUpdate()
    with pytest.raises(ValidationError):
        main.CashEntryTemplateUpdate(name=" ")
    with pytest.raises(ValidationError):
        main.CashEntryTemplateUpdate(category=" ")
    with pytest.raises(ValidationError):
        main.CashEntryTemplateUpdate(amount=0.0)
    with pytest.raises(ValidationError):
        main.CashEntryTemplateUpdate(amount=-5.0)
    with pytest.raises(ValidationError):
        main.CashEntryTemplateUpdate(transaction_type="TRANSFER")


def test_create_rejects_unknown_cash_account():
    db = make_session()
    with pytest.raises(HTTPException) as error:
        create_template(db, cash_account_id=999)
    assert error.value.status_code == 404


# ─── Financial non-effect (core architectural boundary) ────────────────────

def test_template_create_update_delete_never_touch_cash_or_investment_state():
    db = make_session()
    account = create_account(db, balance=1234.0)
    portfolio = Portfolio(workspace_id=main._ws_id(db), name="Core", cash_balance=5678.0)
    db.add(portfolio)
    db.commit()
    before_cash_transactions = db.query(CashAccountTransaction).count()
    before_investment_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()

    template = create_template(db, cash_account_id=account["id"])
    account_row = db.get(CashAccount, account["id"])
    assert account_row.balance == 1234.0

    update_template(db, template["id"], amount=999.0, category="Changed")
    db.refresh(account_row)
    assert account_row.balance == 1234.0

    delete_template(db, template["id"])
    db.refresh(account_row)
    db.refresh(portfolio)

    assert account_row.balance == 1234.0
    assert portfolio.cash_balance == 5678.0
    assert db.query(CashAccountTransaction).count() == before_cash_transactions
    assert db.query(Transaction).count() == before_investment_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots


# ─── Archived-account semantics ─────────────────────────────────────────────

def test_template_survives_account_archival_and_remains_readable_and_editable():
    db = make_session()
    account = create_account(db)
    template = create_template(db, cash_account_id=account["id"])

    archive_account(db, account["id"])

    listed = list_templates(db)
    assert len(listed) == 1
    assert listed[0]["id"] == template["id"]
    assert listed[0]["cash_account_is_archived"] is True

    edited = update_template(db, template["id"], name="Still editable")
    assert edited["name"] == "Still editable"
    assert edited["cash_account_is_archived"] is True


def test_create_against_archived_account_is_rejected():
    db = make_session()
    account = create_account(db)
    archive_account(db, account["id"])

    with pytest.raises(HTTPException) as error:
        create_template(db, cash_account_id=account["id"])
    assert error.value.status_code == 409
    assert db.query(CashEntryTemplate).count() == 0


def test_repoint_to_archived_account_is_rejected():
    db = make_session()
    account = create_account(db)
    archived_account = create_account(db, name="Old Reserve")
    archive_account(db, archived_account["id"])
    template = create_template(db, cash_account_id=account["id"])

    with pytest.raises(HTTPException) as error:
        update_template(db, template["id"], cash_account_id=archived_account["id"])
    assert error.value.status_code == 409
    row = db.get(CashEntryTemplate, template["id"])
    assert row.cash_account_id == account["id"]


def test_repoint_to_a_different_active_account_is_allowed():
    db = make_session()
    account = create_account(db)
    other_account = create_account(db, name="Savings")
    template = create_template(db, cash_account_id=account["id"])

    updated = update_template(db, template["id"], cash_account_id=other_account["id"])

    assert updated["cash_account_id"] == other_account["id"]
    assert updated["cash_account_name"] == "Savings"
