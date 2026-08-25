"""Focused tests for CashAccount Transfers v1."""
import asyncio
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
    CashAccountBaseline,
    CashAccountTransaction,
    CashAccountTransfer,
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


def transfer_body(source_id, destination_id, **overrides):
    payload = {
        "source_cash_account_id": source_id,
        "destination_cash_account_id": destination_id,
        "amount": 100.0,
        "occurred_on": "2026-08-15",
        "note": "Move reserve",
    }
    payload.update(overrides)
    return main.CashAccountTransferCreate(**payload)


def create_transfer(db, source_id, destination_id, **overrides):
    return asyncio.run(main.create_cash_account_transfer(transfer_body(source_id, destination_id, **overrides), db))


def report(db, month):
    return asyncio.run(main.get_cash_flow_report(month, db))


def setup_pair(db, source_balance=1000.0, destination_balance=500.0, source_date="2026-08-01", destination_date="2026-08-01"):
    source = create_account(db, name="Savings A", balance=source_balance)
    destination = create_account(db, name="Savings B", balance=destination_balance)
    start_tracking(db, source["id"], effective_on=source_date, observed_balance=source_balance)
    start_tracking(db, destination["id"], effective_on=destination_date, observed_balance=destination_balance)
    return source, destination


def test_success_creates_owner_two_legs_and_conserves_balances():
    db = make_session()
    source, destination = setup_pair(db)

    result = create_transfer(db, source["id"], destination["id"], amount=100.0)

    transfer = db.query(CashAccountTransfer).one()
    legs = db.query(CashAccountTransaction).filter(CashAccountTransaction.transfer_id == transfer.id).all()
    assert result["id"] == transfer.id
    assert len(legs) == 2
    assert {(leg.cash_account_id, leg.amount, leg.transaction_type) for leg in legs} == {
        (source["id"], -100.0, "TRANSFER"),
        (destination["id"], 100.0, "TRANSFER"),
    }
    db.refresh(db.get(CashAccount, source["id"]))
    db.refresh(db.get(CashAccount, destination["id"]))
    assert db.get(CashAccount, source["id"]).balance == 900.0
    assert db.get(CashAccount, destination["id"]).balance == 600.0
    assert 900.0 + 600.0 == pytest.approx(1000.0 + 500.0)


def test_transfer_response_and_account_history_expose_direction():
    db = make_session()
    source, destination = setup_pair(db)
    result = create_transfer(db, source["id"], destination["id"])

    assert result["source_account_name"] == "Savings A"
    assert result["destination_account_name"] == "Savings B"
    source_history = asyncio.run(main.list_cash_account_transactions(source["id"], db))
    destination_history = asyncio.run(main.list_cash_account_transactions(destination["id"], db))
    assert source_history[0]["transfer_direction"] == "OUT"
    assert source_history[0]["transfer_destination_account_name"] == "Savings B"
    assert destination_history[0]["transfer_direction"] == "IN"
    assert destination_history[0]["transfer_source_account_name"] == "Savings A"


def test_insufficient_funds_rejects_without_any_writes():
    db = make_session()
    source, destination = setup_pair(db, source_balance=50.0)
    with pytest.raises(HTTPException) as error:
        create_transfer(db, source["id"], destination["id"], amount=50.01)
    assert error.value.status_code == 422
    assert db.query(CashAccountTransfer).count() == 0
    assert db.query(CashAccountTransaction).count() == 0
    assert db.get(CashAccount, source["id"]).balance == 50.0
    assert db.get(CashAccount, destination["id"]).balance == 500.0


def test_same_account_and_invalid_amounts_are_rejected():
    db = make_session()
    account = create_account(db)
    with pytest.raises(ValidationError):
        transfer_body(account["id"], account["id"])
    for amount in (0.0, -1.0, float("nan"), float("inf")):
        with pytest.raises(ValidationError):
            transfer_body(account["id"], account["id"] + 1, amount=amount)
    assert db.query(CashAccountTransfer).count() == 0


def test_both_accounts_must_be_tracked_and_date_must_respect_both_baselines():
    db = make_session()
    source = create_account(db, name="Source")
    destination = create_account(db, name="Destination")
    start_tracking(db, source["id"], effective_on="2026-08-10")
    with pytest.raises(HTTPException) as untracked:
        create_transfer(db, source["id"], destination["id"])
    assert untracked.value.status_code == 409
    start_tracking(db, destination["id"], effective_on="2026-08-20")
    with pytest.raises(HTTPException) as early:
        create_transfer(db, source["id"], destination["id"], occurred_on="2026-08-19")
    assert early.value.status_code == 422
    with pytest.raises(HTTPException) as source_early:
        create_transfer(db, source["id"], destination["id"], occurred_on="2026-08-01")
    assert source_early.value.status_code == 422
    assert db.query(CashAccountTransfer).count() == 0


@pytest.mark.parametrize("archive_source", [True, False])
def test_archived_accounts_cannot_start_new_transfers(archive_source):
    db = make_session()
    source, destination = setup_pair(db)
    account_id = source["id"] if archive_source else destination["id"]
    asyncio.run(main.update_cash_account(account_id, main.CashAccountUpdate(is_archived=True), db))
    with pytest.raises(HTTPException) as error:
        create_transfer(db, source["id"], destination["id"])
    assert error.value.status_code == 409
    assert db.query(CashAccountTransfer).count() == 0


def test_foreign_workspace_account_is_not_leaked_or_mutated():
    db = make_session()
    source, destination = setup_pair(db)
    foreign_workspace = Workspace(name="Other")
    db.add(foreign_workspace)
    db.commit()
    foreign = CashAccount(workspace_id=foreign_workspace.id, name="Private", currency="THB", balance=800.0)
    db.add(foreign)
    db.commit()
    db.add(CashAccountBaseline(cash_account_id=foreign.id, effective_on="2026-08-01", observed_balance=800.0))
    db.commit()

    with pytest.raises(HTTPException) as error:
        create_transfer(db, foreign.id, destination["id"])
    assert error.value.status_code == 404
    assert db.query(CashAccountTransfer).count() == 0
    assert db.get(CashAccount, foreign.id).balance == 800.0


def test_monthly_report_projects_one_transfer_and_does_not_change_totals():
    db = make_session()
    source, destination = setup_pair(db)
    transfer = create_transfer(db, source["id"], destination["id"], amount=100.0)
    income = main.CashAccountTransaction(
        workspace_id=source["workspace_id"], cash_account_id=source["id"], transaction_type="INCOME",
        amount=250.0, occurred_on="2026-08-10", category="Salary",
    )
    expense = main.CashAccountTransaction(
        workspace_id=source["workspace_id"], cash_account_id=source["id"], transaction_type="EXPENSE",
        amount=75.0, occurred_on="2026-08-11", category="Food",
    )
    db.add_all([income, expense])
    db.commit()

    result = report(db, "2026-08")
    transfer_events = [event for event in result["events"] if event["transaction_type"] == "TRANSFER"]
    assert len(transfer_events) == 1
    assert transfer_events[0]["transfer_id"] == transfer["id"]
    assert transfer_events[0]["transfer_source_account_name"] == "Savings A"
    assert transfer_events[0]["transfer_destination_account_name"] == "Savings B"
    assert [event["transaction_type"] for event in result["events"]].count("TRANSFER") == 1
    assert {event["category"] for event in result["events"] if event["transaction_type"] != "TRANSFER"} == {"Salary", "Food"}


def test_historical_transfer_survives_later_archive():
    db = make_session()
    source, destination = setup_pair(db)
    create_transfer(db, source["id"], destination["id"])
    asyncio.run(main.update_cash_account(destination["id"], main.CashAccountUpdate(is_archived=True), db))

    events = report(db, "2026-08")["events"]
    assert len(events) == 1
    assert events[0]["transaction_type"] == "TRANSFER"
    assert events[0]["destination_account_is_archived"] is True
    assert events[0]["transfer_destination_account_name"] == "Savings B"


def test_transfer_isolated_from_investment_transactions_and_snapshots():
    db = make_session()
    workspace_id = main._ws_id(db)
    portfolio = Portfolio(workspace_id=workspace_id, name="Core", cash_balance=700.0)
    db.add(portfolio)
    db.commit()
    source, destination = setup_pair(db)
    before_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()
    create_transfer(db, source["id"], destination["id"])

    assert db.query(Transaction).count() == before_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots
    assert db.get(Portfolio, portfolio.id).cash_balance == 700.0


def test_forced_commit_failure_rolls_back_owner_legs_and_balances(monkeypatch):
    db = make_session()
    source, destination = setup_pair(db)
    original_commit = db.commit

    def fail_commit():
        raise RuntimeError("forced commit failure")

    monkeypatch.setattr(db, "commit", fail_commit)
    with pytest.raises(RuntimeError, match="forced commit failure"):
        create_transfer(db, source["id"], destination["id"])
    monkeypatch.setattr(db, "commit", original_commit)
    assert db.query(CashAccountTransfer).count() == 0
    assert db.query(CashAccountTransaction).count() == 0
    assert db.get(CashAccount, source["id"]).balance == 1000.0
    assert db.get(CashAccount, destination["id"]).balance == 500.0
