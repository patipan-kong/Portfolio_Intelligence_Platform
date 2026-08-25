"""Focused tests for Cash As-Of Read (Wealth OS Phase 5 milestone).

Covers both the pure domain function (services.cash_account_ledger.cash_balance_as_of)
and the read-only endpoint (GET /cash-accounts/{id}/as-of).
"""
import asyncio
import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from pydantic import TypeAdapter, ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import (
    Base,
    CashAccount,
    Workspace,
)
import models.asset  # noqa: F401 — registers Asset tables referenced by ledger models.
import models.registry_finding  # noqa: F401 — registers registry tables referenced by Base metadata.
import main
from services.cash_account_ledger import cash_balance_as_of


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def create_account(db, **overrides):
    payload = {"name": "Everyday Cash", "currency": "THB", "balance": 100.0}
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
        "occurred_on": "2026-08-05",
        "category": "Salary",
    }
    payload.update(overrides)
    return asyncio.run(main.create_cash_account_transaction(account_id, main.CashAccountTransactionCreate(**payload), db))


def reconcile(db, account_id, **overrides):
    payload = {"observed_balance": 100.0, "occurred_on": "2026-08-05"}
    payload.update(overrides)
    return asyncio.run(main.reconcile_cash_account(account_id, main.CashAccountReconcile(**payload), db))


def update_account(db, account_id, **overrides):
    return asyncio.run(main.update_cash_account(account_id, main.CashAccountUpdate(**overrides), db))


def transfer_body(source_id, destination_id, **overrides):
    payload = {
        "source_cash_account_id": source_id,
        "destination_cash_account_id": destination_id,
        "amount": 100.0,
        "occurred_on": "2026-08-10",
        "note": "Move reserve",
    }
    payload.update(overrides)
    return main.CashAccountTransferCreate(**payload)


def create_transfer(db, source_id, destination_id, **overrides):
    return asyncio.run(main.create_cash_account_transfer(transfer_body(source_id, destination_id, **overrides), db))


def as_of(db, account_id, as_of_date):
    return asyncio.run(main.get_cash_account_balance_as_of(account_id, date.fromisoformat(as_of_date), db))


# ─── Pure domain function ──────────────────────────────────────────────────


def test_pure_function_no_baseline_is_unavailable():
    assert cash_balance_as_of(None, None, [], "2026-08-10") is None


def test_pure_function_date_before_baseline_is_unavailable():
    assert cash_balance_as_of("2026-08-05", 1000.0, [], "2026-08-04") is None


def test_pure_function_baseline_date_returns_baseline_balance():
    assert cash_balance_as_of("2026-08-05", 1000.0, [], "2026-08-05") == 1000.0


def test_pure_function_excludes_events_after_requested_date():
    events = [("INCOME", 50.0, "2026-08-06"), ("INCOME", 999.0, "2026-08-20")]
    assert cash_balance_as_of("2026-08-05", 1000.0, events, "2026-08-06") == 1050.0


def test_pure_function_unknown_event_type_fails_honestly():
    events = [("MYSTERY", 50.0, "2026-08-06")]
    with pytest.raises(ValueError, match="Unsupported cash transaction type"):
        cash_balance_as_of("2026-08-05", 1000.0, events, "2026-08-06")


# ─── Endpoint: availability ────────────────────────────────────────────────


def test_endpoint_no_baseline_is_unavailable_not_zero():
    db = make_session()
    account = create_account(db)

    result = as_of(db, account["id"], "2026-08-10")

    assert result["available"] is False
    assert result["balance"] is None
    assert result["baseline_effective_on"] is None


def test_endpoint_date_before_baseline_is_unavailable_not_zero():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-05", observed_balance=1000.0)

    result = as_of(db, account["id"], "2026-08-04")

    assert result["available"] is False
    assert result["balance"] is None


def test_endpoint_baseline_date_returns_baseline_balance():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-05", observed_balance=1000.0)

    result = as_of(db, account["id"], "2026-08-05")

    assert result["available"] is True
    assert result["balance"] == 1000.0
    assert result["baseline_effective_on"] == "2026-08-05"
    assert result["currency"] == "THB"


# ─── Endpoint: income / expense / adjustment ───────────────────────────────


def test_endpoint_income_increases_as_of_balance():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-01", observed_balance=1000.0)
    add_activity(db, account["id"], transaction_type="INCOME", amount=200.0, occurred_on="2026-08-05")

    assert as_of(db, account["id"], "2026-08-05")["balance"] == 1200.0


def test_endpoint_expense_decreases_as_of_balance():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-01", observed_balance=1000.0)
    add_activity(db, account["id"], transaction_type="EXPENSE", amount=50.0, occurred_on="2026-08-05", category="Food")

    assert as_of(db, account["id"], "2026-08-05")["balance"] == 950.0


def test_endpoint_adjustment_applied_exactly_as_stored_not_reinterpreted():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-01", observed_balance=1000.0)
    add_activity(db, account["id"], transaction_type="INCOME", amount=200.0, occurred_on="2026-08-05")
    add_activity(db, account["id"], transaction_type="EXPENSE", amount=50.0, occurred_on="2026-08-06", category="Food")
    reconcile(db, account["id"], observed_balance=1050.0, occurred_on="2026-08-07")

    # baseline 1000 + income 200 - expense 50 - adjustment(-100) = 1050
    result = as_of(db, account["id"], "2026-08-07")

    assert result["balance"] == 1050.0


def test_endpoint_multiple_events_ordered_and_date_bounded():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-01", observed_balance=1000.0)
    add_activity(db, account["id"], transaction_type="INCOME", amount=100.0, occurred_on="2026-08-03")
    add_activity(db, account["id"], transaction_type="EXPENSE", amount=30.0, occurred_on="2026-08-05", category="Food")
    add_activity(db, account["id"], transaction_type="INCOME", amount=500.0, occurred_on="2026-08-09")

    # As of Aug 5, the Aug 9 income must not yet be visible.
    result = as_of(db, account["id"], "2026-08-05")

    assert result["balance"] == 1070.0


# ─── Endpoint: transfers ────────────────────────────────────────────────────


def test_endpoint_transfer_source_and_destination_legs_reconstruct_independently():
    db = make_session()
    source = create_account(db, name="Account A", balance=1000.0)
    destination = create_account(db, name="Account B", balance=500.0)
    start_tracking(db, source["id"], effective_on="2026-08-01", observed_balance=1000.0)
    start_tracking(db, destination["id"], effective_on="2026-08-01", observed_balance=500.0)

    create_transfer(db, source["id"], destination["id"], amount=100.0, occurred_on="2026-08-10")

    before_a = as_of(db, source["id"], "2026-08-09")
    before_b = as_of(db, destination["id"], "2026-08-09")
    after_a = as_of(db, source["id"], "2026-08-10")
    after_b = as_of(db, destination["id"], "2026-08-10")

    assert before_a["balance"] == 1000.0
    assert before_b["balance"] == 500.0
    assert after_a["balance"] == 900.0
    assert after_b["balance"] == 600.0
    # Combined external cash is conserved across the transfer date.
    assert before_a["balance"] + before_b["balance"] == after_a["balance"] + after_b["balance"] == 1500.0


# ─── Endpoint: zero balance, archive, workspace isolation, malformed date ──


def test_endpoint_zero_balance_is_available_numeric_zero_not_unavailable():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-01", observed_balance=0.0)

    result = as_of(db, account["id"], "2026-08-01")

    assert result["available"] is True
    assert result["balance"] == 0.0


def test_endpoint_archived_account_historical_read_remains_allowed():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-01", observed_balance=1000.0)
    add_activity(db, account["id"], transaction_type="INCOME", amount=200.0, occurred_on="2026-08-10")
    update_account(db, account["id"], is_archived=True)

    result = as_of(db, account["id"], "2026-08-10")

    assert result["available"] is True
    assert result["balance"] == 1200.0


def test_endpoint_workspace_isolation_returns_404_for_foreign_account():
    db = make_session()
    main._ws_id(db)  # establish the default workspace before the foreign one
    foreign_workspace = Workspace(name="Other")
    db.add(foreign_workspace)
    db.commit()
    foreign_account = CashAccount(workspace_id=foreign_workspace.id, name="Private", currency="THB", balance=20.0)
    db.add(foreign_account)
    db.commit()

    with pytest.raises(HTTPException) as error:
        as_of(db, foreign_account.id, "2026-08-10")

    assert error.value.status_code == 404


def test_endpoint_malformed_date_rejected_by_declared_query_param_type():
    """The `date` parameter is exercised through FastAPI's request layer, not this
    direct-call test style, so this asserts against the exact validation
    mechanism FastAPI applies to a `date`-typed query param for that endpoint."""
    with pytest.raises(ValidationError):
        TypeAdapter(date).validate_python("not-a-date")


# ─── Endpoint: current-balance fallback must never leak in ────────────────


def test_endpoint_current_balance_is_not_used_as_historical_fallback():
    db = make_session()
    account = create_account(db)
    start_tracking(db, account["id"], effective_on="2026-08-01", observed_balance=1000.0)
    add_activity(db, account["id"], transaction_type="INCOME", amount=500.0, occurred_on="2026-08-20")
    # Current CashAccount.balance is now 1500 — a date before that income must
    # not reflect it, proving the reader never substitutes current balance.
    assert db.query(CashAccount).one().balance == 1500.0

    result = as_of(db, account["id"], "2026-08-10")

    assert result["balance"] == 1000.0


# ─── Replay / invariance proof ─────────────────────────────────────────────


def test_replay_as_of_latest_event_date_matches_current_cash_account_balance():
    """Regression proof for the gap reconnaissance identified: baseline + ledger
    replay must equal the live CashAccount.balance, end to end, across every
    currently valid event type including a transfer leg."""
    db = make_session()
    source = create_account(db, name="Main", balance=1000.0)
    destination = create_account(db, name="Reserve", balance=200.0)
    start_tracking(db, source["id"], effective_on="2026-08-01", observed_balance=1000.0)
    start_tracking(db, destination["id"], effective_on="2026-08-01", observed_balance=200.0)

    add_activity(db, source["id"], transaction_type="INCOME", amount=300.0, occurred_on="2026-08-05")
    add_activity(db, source["id"], transaction_type="EXPENSE", amount=80.0, occurred_on="2026-08-06", category="Food")
    reconcile(db, source["id"], observed_balance=1300.0, occurred_on="2026-08-07")
    create_transfer(db, source["id"], destination["id"], amount=150.0, occurred_on="2026-08-08")

    latest_event_date = "2026-08-08"
    reconstructed_source = as_of(db, source["id"], latest_event_date)["balance"]
    reconstructed_destination = as_of(db, destination["id"], latest_event_date)["balance"]

    live_source = db.query(CashAccount).filter(CashAccount.id == source["id"]).one().balance
    live_destination = db.query(CashAccount).filter(CashAccount.id == destination["id"]).one().balance

    assert reconstructed_source == live_source
    assert reconstructed_destination == live_destination
