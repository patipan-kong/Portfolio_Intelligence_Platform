"""Focused tests for the Investment Funding Transfer (ADR-012).

Covers: persistence/validation for both directions, portfolio isolation,
Cash Flow aggregation exclusion (with a contrast EXPENSE proving the original
correctness trap is closed), historical/as-of reconstruction, reconciliation
interaction, and the existing cash↔cash TRANSFER regression boundary.
"""
import asyncio
import importlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateTable

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
from services.cash_account_ledger import cash_balance_as_of


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


def report(db, month):
    return asyncio.run(main.get_cash_flow_report(month, db))


def setup_account_and_portfolio(db, account_balance=1000.0, effective_on="2026-08-01"):
    account = create_account(db, balance=account_balance)
    start_tracking(db, account["id"], effective_on=effective_on, observed_balance=account_balance)
    portfolio = create_portfolio(db)
    return account, portfolio


# ── Persistence / validation ─────────────────────────────────────────────────


def test_to_portfolio_stores_negative_amount_with_counterparty_and_no_category_or_transfer_id():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)

    result = create_investment_transfer(db, account["id"], portfolio.id, direction="TO_PORTFOLIO", amount=300.0)

    assert result["transaction_type"] == "INVESTMENT_TRANSFER"
    assert result["amount"] == -300.0
    assert result["signed_amount"] == -300.0
    assert result["investment_direction"] == "TO_PORTFOLIO"
    assert result["counterparty_portfolio_id"] == portfolio.id
    assert result["counterparty_portfolio_name"] == "Growth Portfolio"
    assert result["category"] is None
    assert result["transfer_id"] is None
    assert db.get(CashAccount, account["id"]).balance == 700.0


def test_from_portfolio_stores_positive_amount():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)

    result = create_investment_transfer(db, account["id"], portfolio.id, direction="FROM_PORTFOLIO", amount=200.0)

    assert result["amount"] == 200.0
    assert result["signed_amount"] == 200.0
    assert result["investment_direction"] == "FROM_PORTFOLIO"
    assert db.get(CashAccount, account["id"]).balance == 1200.0


def test_foreign_workspace_cash_account_is_404():
    db = make_session()
    _, portfolio = setup_account_and_portfolio(db)
    foreign_workspace = Workspace(name="Other")
    db.add(foreign_workspace)
    db.commit()
    foreign_account = CashAccount(workspace_id=foreign_workspace.id, name="Private", currency="THB", balance=500.0)
    db.add(foreign_account)
    db.commit()
    db.add(CashAccountBaseline(cash_account_id=foreign_account.id, effective_on="2026-08-01", observed_balance=500.0))
    db.commit()

    with pytest.raises(HTTPException) as error:
        create_investment_transfer(db, foreign_account.id, portfolio.id)
    assert error.value.status_code == 404
    assert db.query(CashAccountTransaction).count() == 0


def test_foreign_workspace_portfolio_is_404():
    db = make_session()
    account, _ = setup_account_and_portfolio(db)
    foreign_workspace = Workspace(name="Other")
    db.add(foreign_workspace)
    db.commit()
    foreign_portfolio = Portfolio(workspace_id=foreign_workspace.id, name="Not Mine", cash_balance=0.0)
    db.add(foreign_portfolio)
    db.commit()

    with pytest.raises(HTTPException) as error:
        create_investment_transfer(db, account["id"], foreign_portfolio.id)
    assert error.value.status_code == 404
    assert db.query(CashAccountTransaction).count() == 0


def test_archived_cash_account_is_rejected():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    asyncio.run(main.update_cash_account(account["id"], main.CashAccountUpdate(is_archived=True), db))

    with pytest.raises(HTTPException, match="Archived"):
        create_investment_transfer(db, account["id"], portfolio.id)


def test_tracking_not_started_is_rejected():
    db = make_session()
    account = create_account(db)
    portfolio = create_portfolio(db)

    with pytest.raises(HTTPException) as error:
        create_investment_transfer(db, account["id"], portfolio.id)
    assert "tracking" in error.value.detail.lower()


def test_pre_baseline_date_is_rejected():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db, effective_on="2026-08-10")

    with pytest.raises(HTTPException) as error:
        create_investment_transfer(db, account["id"], portfolio.id, occurred_on="2026-08-01")
    assert error.value.status_code == 422


@pytest.mark.parametrize("amount", [0.0, -1.0, float("nan"), float("inf")])
def test_zero_negative_or_nonfinite_amount_is_rejected(amount):
    with pytest.raises(ValidationError):
        investment_transfer_body(1, amount=amount)


def test_invalid_direction_is_rejected():
    with pytest.raises(ValidationError):
        main.CashInvestmentTransferCreate(
            portfolio_id=1, direction="SIDEWAYS", amount=100.0, occurred_on="2026-08-15",
        )


def test_outbound_overdraft_is_rejected_without_any_row_created():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db, account_balance=100.0)

    with pytest.raises(HTTPException) as error:
        create_investment_transfer(db, account["id"], portfolio.id, direction="TO_PORTFOLIO", amount=100.01)
    assert error.value.status_code == 422
    assert db.query(CashAccountTransaction).count() == 0
    assert db.get(CashAccount, account["id"]).balance == 100.0


# ── Invalid-state prevention (DB CHECK constraints) ──────────────────────────


@pytest.mark.parametrize("transaction_type", ["EXPENSE", "INCOME", "ADJUSTMENT", "TRANSFER"])
def test_db_rejects_counterparty_on_any_non_investment_transfer_type(transaction_type):
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    amount = 10.0 if transaction_type in ("EXPENSE", "INCOME") else -10.0
    row = CashAccountTransaction(
        workspace_id=account["workspace_id"],
        cash_account_id=account["id"],
        transaction_type=transaction_type,
        amount=amount,
        occurred_on="2026-08-15",
        counterparty_portfolio_id=portfolio.id,
    )
    db.add(row)
    with pytest.raises(IntegrityError):
        db.commit()


def test_db_rejects_investment_transfer_with_transfer_id():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    other_account = create_account(db, name="Other")
    start_tracking(db, other_account["id"])
    transfer = CashAccountTransfer(
        workspace_id=account["workspace_id"],
        source_cash_account_id=account["id"],
        destination_cash_account_id=other_account["id"],
        amount=10.0,
        occurred_on="2026-08-15",
    )
    db.add(transfer)
    db.flush()
    row = CashAccountTransaction(
        workspace_id=account["workspace_id"],
        cash_account_id=account["id"],
        transaction_type="INVESTMENT_TRANSFER",
        amount=-10.0,
        occurred_on="2026-08-15",
        transfer_id=transfer.id,
        counterparty_portfolio_id=portfolio.id,
    )
    db.add(row)
    with pytest.raises(IntegrityError):
        db.commit()


def test_db_rejects_investment_transfer_with_zero_amount():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    row = CashAccountTransaction(
        workspace_id=account["workspace_id"],
        cash_account_id=account["id"],
        transaction_type="INVESTMENT_TRANSFER",
        amount=0.0,
        occurred_on="2026-08-15",
        counterparty_portfolio_id=portfolio.id,
    )
    db.add(row)
    with pytest.raises(IntegrityError):
        db.commit()


def test_portfolio_delete_nulls_counterparty_and_preserves_the_cash_fact():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    create_portfolio(db, name="Other Portfolio")  # so deleting `portfolio` isn't the workspace's last one
    create_investment_transfer(db, account["id"], portfolio.id, amount=300.0)
    portfolio_id = portfolio.id

    asyncio.run(main.delete_portfolio(portfolio_id, db))

    row = db.query(CashAccountTransaction).filter(CashAccountTransaction.transaction_type == "INVESTMENT_TRANSFER").one()
    assert row.counterparty_portfolio_id is None
    assert row.amount == -300.0
    assert db.get(CashAccount, account["id"]).balance == 700.0
    payload = main._cash_account_transaction_payload(row)
    assert payload["counterparty_portfolio_id"] is None
    assert payload["counterparty_portfolio_name"] is None


# ── Cash Flow aggregation invariant ──────────────────────────────────────────


def test_investment_transfer_does_not_affect_income_expense_or_net_cash_flow():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    db.add(CashAccountTransaction(
        workspace_id=account["workspace_id"], cash_account_id=account["id"], transaction_type="INCOME",
        amount=250.0, occurred_on="2026-08-10", category="Salary",
    ))
    db.add(CashAccountTransaction(
        workspace_id=account["workspace_id"], cash_account_id=account["id"], transaction_type="EXPENSE",
        amount=75.0, occurred_on="2026-08-11", category="Food",
    ))
    db.commit()
    baseline = report(db, "2026-08")

    create_investment_transfer(db, account["id"], portfolio.id, amount=500.0)
    after = report(db, "2026-08")

    baseline_non_funding = [e for e in baseline["events"] if e["transaction_type"] != "INVESTMENT_TRANSFER"]
    after_non_funding = [e for e in after["events"] if e["transaction_type"] != "INVESTMENT_TRANSFER"]
    assert baseline_non_funding == after_non_funding
    funding_events = [e for e in after["events"] if e["transaction_type"] == "INVESTMENT_TRANSFER"]
    assert len(funding_events) == 1
    assert len(after["events"]) == len(baseline["events"]) + 1


def test_investment_transfer_never_appears_as_income_or_expense_typed():
    """`emergencyFund.ts::computeRecordedExpenseCoverage` sums only EXPENSE-typed
    events (see frontend/lib/emergencyFund.test.ts for the full contrast proof
    against an equivalent EXPENSE row); this is the backend-side guarantee that
    makes that exclusion possible — an Investment Transfer can never be typed
    EXPENSE or INCOME, so it can never enter that sum."""
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)

    result = create_investment_transfer(db, account["id"], portfolio.id, amount=500.0)

    assert result["transaction_type"] not in ("EXPENSE", "INCOME")
    events = report(db, "2026-08")["events"]
    assert all(event["transaction_type"] != "EXPENSE" for event in events if event["id"] == result["id"])


# ── Historical truth / as-of reconstruction ──────────────────────────────────


def test_as_of_excludes_before_and_includes_on_and_after_occurred_on():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db, account_balance=1000.0)
    create_investment_transfer(db, account["id"], portfolio.id, direction="TO_PORTFOLIO", amount=300.0, occurred_on="2026-08-15")
    account_row = db.get(CashAccount, account["id"])
    events = [
        (t.transaction_type, t.amount, t.occurred_on)
        for t in db.query(CashAccountTransaction).filter(CashAccountTransaction.cash_account_id == account["id"]).all()
    ]

    before = cash_balance_as_of("2026-08-01", 1000.0, events, "2026-08-14")
    on_date = cash_balance_as_of("2026-08-01", 1000.0, events, "2026-08-15")
    later = cash_balance_as_of("2026-08-01", 1000.0, events, "2026-08-31")

    assert before == 1000.0
    assert on_date == 700.0
    assert later == 700.0
    assert account_row.balance == 700.0


def test_as_of_before_baseline_remains_unavailable_not_zero():
    events = [("INVESTMENT_TRANSFER", -300.0, "2026-08-15")]
    assert cash_balance_as_of("2026-08-01", 1000.0, events, "2026-07-31") is None


def test_archived_account_history_still_includes_investment_transfer():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    create_investment_transfer(db, account["id"], portfolio.id, amount=300.0)
    asyncio.run(main.update_cash_account(account["id"], main.CashAccountUpdate(is_archived=True), db))

    events = report(db, "2026-08")["events"]
    assert len(events) == 1
    assert events[0]["account_is_archived"] is True
    assert events[0]["transaction_type"] == "INVESTMENT_TRANSFER"


# ── Reconciliation interaction ───────────────────────────────────────────────


def test_reconciliation_after_investment_transfer_creates_no_row_when_balance_already_agrees():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db, account_balance=1000.0)
    create_investment_transfer(db, account["id"], portfolio.id, direction="TO_PORTFOLIO", amount=300.0)

    result = asyncio.run(main.reconcile_cash_account(
        account["id"], main.CashAccountReconcile(observed_balance=700.0, occurred_on="2026-08-16"), db,
    ))

    assert result["adjustment"] is None
    assert db.query(CashAccountTransaction).filter(CashAccountTransaction.transaction_type == "ADJUSTMENT").count() == 0


# ── Existing cash↔cash TRANSFER regression boundary ──────────────────────────


def test_investment_transfer_coexists_with_cash_to_cash_transfer_without_dedup_collision():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db, account_balance=1000.0)
    other_account = create_account(db, name="Savings B", balance=500.0)
    start_tracking(db, other_account["id"])

    asyncio.run(main.create_cash_account_transfer(
        main.CashAccountTransferCreate(
            source_cash_account_id=account["id"], destination_cash_account_id=other_account["id"],
            amount=100.0, occurred_on="2026-08-10",
        ),
        db,
    ))
    create_investment_transfer(db, account["id"], portfolio.id, amount=200.0, occurred_on="2026-08-12")

    events = report(db, "2026-08")["events"]
    types = sorted(event["transaction_type"] for event in events)
    assert types == ["INVESTMENT_TRANSFER", "TRANSFER"]


# ── Portfolio isolation ───────────────────────────────────────────────────────


def test_investment_transfer_creates_no_portfolio_transaction_and_does_not_change_portfolio_cash_balance():
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    portfolio.cash_balance = 700.0
    db.commit()
    before_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()

    create_investment_transfer(db, account["id"], portfolio.id, amount=300.0)

    assert db.query(Transaction).count() == before_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots
    assert db.get(Portfolio, portfolio.id).cash_balance == 700.0


def test_forced_commit_failure_rolls_back_row_and_balance(monkeypatch):
    db = make_session()
    account, portfolio = setup_account_and_portfolio(db)
    original_commit = db.commit

    def fail_commit():
        raise RuntimeError("forced commit failure")

    monkeypatch.setattr(db, "commit", fail_commit)
    with pytest.raises(RuntimeError, match="forced commit failure"):
        create_investment_transfer(db, account["id"], portfolio.id)
    monkeypatch.setattr(db, "commit", original_commit)
    assert db.query(CashAccountTransaction).count() == 0
    assert db.get(CashAccount, account["id"]).balance == 1000.0


# ── Schema / migration contract (IFT-001: PostgreSQL column width) ──────────
#
# 'INVESTMENT_TRANSFER' is 19 characters. The ORM column and the migration's
# PostgreSQL path both declared VARCHAR(16) before this correction, which
# SQLite silently tolerates (no length enforcement) but PostgreSQL does not —
# every INVESTMENT_TRANSFER write would have been rejected in production.
# These tests inspect the model/migration schema/intent directly, so they
# fail against the pre-correction candidate regardless of which dialect the
# test suite happens to run against.

_MIN_TRANSACTION_TYPE_WIDTH = len("INVESTMENT_TRANSFER")


def test_transaction_type_column_width_covers_investment_transfer():
    column_type = CashAccountTransaction.__table__.c.transaction_type.type
    assert column_type.length >= _MIN_TRANSACTION_TYPE_WIDTH


def test_transaction_type_postgresql_ddl_is_not_the_too_narrow_prior_width():
    create_table = CreateTable(CashAccountTransaction.__table__, include_foreign_key_constraints=[])
    postgres_ddl = str(create_table.compile(dialect=postgresql.dialect()))
    assert f"transaction_type VARCHAR({_MIN_TRANSACTION_TYPE_WIDTH})" not in postgres_ddl
    assert "transaction_type VARCHAR(16)" not in postgres_ddl


def test_migration_postgresql_path_widens_transaction_type_column():
    migration = importlib.import_module("migrations.versions.b6d8f0a2c4e6_add_cash_investment_transfers")

    class _Bind:
        dialect = postgresql.dialect()

    class _PostgresOp:
        alter_column_calls = None

        def __init__(self):
            self.alter_column_calls = []

        def get_bind(self):
            return _Bind()

        def alter_column(self, table_name, column_name, **kwargs):
            self.alter_column_calls.append((table_name, column_name, kwargs))

        def drop_constraint(self, *args, **kwargs):
            pass

        def create_check_constraint(self, *args, **kwargs):
            pass

        def add_column(self, *args, **kwargs):
            pass

        def create_index(self, *args, **kwargs):
            pass

        def create_foreign_key(self, *args, **kwargs):
            pass

    fake_op = _PostgresOp()
    original_op = migration.op
    migration.op = fake_op
    try:
        migration.upgrade()
    finally:
        migration.op = original_op

    transaction_type_calls = [
        call for call in fake_op.alter_column_calls if call[1] == "transaction_type"
    ]
    assert len(transaction_type_calls) == 1
    table_name, _, kwargs = transaction_type_calls[0]
    assert table_name == "cash_account_transactions"
    assert kwargs["existing_type"].length == 16
    assert kwargs["type_"].length >= _MIN_TRANSACTION_TYPE_WIDTH
