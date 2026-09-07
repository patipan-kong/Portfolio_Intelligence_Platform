"""Focused tests for PFET-01 (Portfolio Funding Evidence Timeline, ADR-012).

GET /portfolios/{portfolio_id}/funding-evidence returns documentary cash-side
Investment Funding Transfer evidence naming this Portfolio. It is not a
funding ledger and not reconciliation evidence — see ADR-012.
"""
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
    CashAccountTransaction,
    Portfolio,
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


def create_portfolio(db, name="Growth Portfolio", cash_balance=0.0):
    workspace_id = main._ws_id(db)
    portfolio = Portfolio(workspace_id=workspace_id, name=name, cash_balance=cash_balance)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def investment_transfer_body(portfolio_id, **overrides):
    payload = {
        "portfolio_id": portfolio_id,
        "direction": "TO_PORTFOLIO",
        "amount": 300.0,
        "occurred_on": "2026-08-15",
        "note": "September contribution",
    }
    payload.update(overrides)
    return main.CashInvestmentTransferCreate(**payload)


def create_investment_transfer(db, account_id, portfolio_id, **overrides):
    return asyncio.run(
        main.create_cash_investment_transfer(account_id, investment_transfer_body(portfolio_id, **overrides), db)
    )


def setup_account_and_portfolio(db, account_balance=1000.0, effective_on="2026-08-01"):
    account = create_account(db, balance=account_balance)
    start_tracking(db, account["id"], effective_on=effective_on, observed_balance=account_balance)
    portfolio = create_portfolio(db)
    return account, portfolio


def funding_evidence(db, portfolio_id):
    return asyncio.run(main.list_portfolio_funding_evidence(portfolio_id, db))


def test_returns_matching_portfolio_evidence():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    create_investment_transfer(db, account["id"], portfolio.id, amount=300.0, occurred_on="2026-08-15")

    events = funding_evidence(db, portfolio.id)

    assert len(events) == 1
    assert events[0]["transaction_type"] == "INVESTMENT_TRANSFER"
    assert events[0]["counterparty_portfolio_id_snapshot"] == portfolio.id
    assert events[0]["counterparty_portfolio_name_snapshot"] == "Growth Portfolio"
    assert events[0]["account_name"] == "Everyday Cash"
    assert events[0]["account_is_archived"] is False


def test_excludes_another_portfolios_evidence():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    other_portfolio = create_portfolio(db, name="Other Portfolio")
    create_investment_transfer(db, account["id"], other_portfolio.id, amount=150.0)

    events = funding_evidence(db, portfolio.id)

    assert events == []


def test_workspace_isolation_foreign_portfolio_is_404():
    db = make_session()
    setup_account_and_portfolio(db)
    foreign_workspace = Workspace(name="Other")
    db.add(foreign_workspace)
    db.commit()
    foreign_portfolio = Portfolio(workspace_id=foreign_workspace.id, name="Not Mine", cash_balance=0.0)
    db.add(foreign_portfolio)
    db.commit()

    with pytest.raises(HTTPException) as error:
        funding_evidence(db, foreign_portfolio.id)
    assert error.value.status_code == 404


def test_deterministic_ordering_matches_occurred_on_then_id_desc():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    create_investment_transfer(db, account["id"], portfolio.id, amount=100.0, occurred_on="2026-08-10")
    create_investment_transfer(db, account["id"], portfolio.id, amount=200.0, occurred_on="2026-08-20")
    create_investment_transfer(db, account["id"], portfolio.id, amount=50.0, occurred_on="2026-08-20")

    events = funding_evidence(db, portfolio.id)

    dates = [event["occurred_on"] for event in events]
    ids = [event["id"] for event in events]
    assert dates == ["2026-08-20", "2026-08-20", "2026-08-10"]
    assert ids[0] > ids[1]


def test_legacy_row_without_snapshot_is_excluded():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    legacy_row = CashAccountTransaction(
        workspace_id=account["workspace_id"],
        cash_account_id=account["id"],
        transaction_type="INVESTMENT_TRANSFER",
        amount=-10.0,
        occurred_on="2026-08-15",
        counterparty_portfolio_id=portfolio.id,
    )
    db.add(legacy_row)
    db.commit()

    events = funding_evidence(db, portfolio.id)

    assert events == []


def test_non_investment_transfer_transactions_are_excluded():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    asyncio.run(
        main.create_cash_account_transaction(
            account["id"],
            main.CashAccountTransactionCreate(
                transaction_type="EXPENSE", amount=50.0, occurred_on="2026-08-16", category="Groceries"
            ),
            db,
        )
    )

    events = funding_evidence(db, portfolio.id)

    assert events == []


def test_archived_cash_account_evidence_remains_included():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    create_investment_transfer(db, account["id"], portfolio.id, amount=300.0)
    asyncio.run(main.update_cash_account(account["id"], main.CashAccountUpdate(is_archived=True), db))

    events = funding_evidence(db, portfolio.id)

    assert len(events) == 1
    assert events[0]["account_is_archived"] is True


def test_nonexistent_portfolio_is_404():
    db = make_session()
    setup_account_and_portfolio(db)

    with pytest.raises(HTTPException) as error:
        funding_evidence(db, 999999)
    assert error.value.status_code == 404


def test_read_causes_no_mutation():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    create_investment_transfer(db, account["id"], portfolio.id, amount=300.0)
    before_transactions = db.query(CashAccountTransaction).count()
    before_balance = db.get(CashAccount, account["id"]).balance

    funding_evidence(db, portfolio.id)
    funding_evidence(db, portfolio.id)

    assert db.query(CashAccountTransaction).count() == before_transactions
    assert db.get(CashAccount, account["id"]).balance == before_balance


def test_response_preserves_immutable_snapshot_identity_after_rename():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    create_investment_transfer(db, account["id"], portfolio.id, amount=300.0)
    portfolio.name = "Renamed Growth Portfolio"
    db.commit()

    events = funding_evidence(db, portfolio.id)

    assert len(events) == 1
    assert events[0]["counterparty_portfolio_name_snapshot"] == "Growth Portfolio"
