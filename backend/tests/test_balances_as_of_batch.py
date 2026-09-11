"""Focused tests for the Cash/Liability Balances-As-Of batch endpoints
(DOGFOOD-01 — Periodic Review Net Worth request fan-out fix).

GET /cash-accounts/balances-as-of and GET /liabilities/balances-as-of exist
to replace an accounts x dates / liabilities x dates HTTP fan-out (Periodic
Review's Net Worth section previously called GET /cash-accounts/{id}/as-of
and GET /liabilities/{id}/as-of once per (account, date) / (liability, date)
pair) with exactly one request per domain. Both batch endpoints compose the
same canonical pure functions the single-lookup endpoints already use
(cash_balance_as_of / liability_balance_as_of) — no arithmetic is
duplicated, and this file's primary job is proving the batch result is
identical to what the per-pair calls already returned, for every case the
single-lookup endpoint's own test suite covers, plus proving the batch
endpoint's DB query count does not scale with the number of dates
requested (the actual fan-out this endpoint exists to eliminate).
"""
import asyncio
import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from models.database import Base, CashAccount, Liability, Workspace
import models.asset  # noqa: F401 — registers Asset tables referenced by ledger models.
import models.registry_finding  # noqa: F401 — registers registry tables referenced by Base metadata.
import main


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)(), engine


# ─── Cash helpers (mirrors test_cash_account_as_of.py) ─────────────────────


def create_cash_account(db, **overrides):
    payload = {"name": "Everyday Cash", "currency": "THB", "balance": 100.0}
    payload.update(overrides)
    return asyncio.run(main.create_cash_account(main.CashAccountCreate(**payload), db))


def start_cash_tracking(db, account_id, effective_on="2026-08-01", observed_balance=1000.0):
    return asyncio.run(
        main.create_cash_account_baseline(
            account_id,
            main.CashAccountBaselineCreate(effective_on=effective_on, observed_balance=observed_balance),
            db,
        )
    )


def add_cash_activity(db, account_id, **overrides):
    payload = {"transaction_type": "INCOME", "amount": 10.0, "occurred_on": "2026-08-05", "category": "Salary"}
    payload.update(overrides)
    return asyncio.run(main.create_cash_account_transaction(account_id, main.CashAccountTransactionCreate(**payload), db))


def update_cash_account(db, account_id, **overrides):
    return asyncio.run(main.update_cash_account(account_id, main.CashAccountUpdate(**overrides), db))


def cash_single_as_of(db, account_id, as_of_date):
    return asyncio.run(main.get_cash_account_balance_as_of(account_id, date.fromisoformat(as_of_date), db))


def cash_batch_as_of(db, dates, include_archived=False):
    return asyncio.run(
        main.list_cash_account_balances_as_of(
            dates=[date.fromisoformat(d) for d in dates], include_archived=include_archived, db=db
        )
    )


# ─── Liability helpers (mirrors test_liability_balance_observations.py) ────


def create_liability(db, **overrides):
    payload = {"name": "Home Loan", "liability_type": "MORTGAGE", "balance": 2500000.0, "currency": "THB"}
    payload.update(overrides)
    return asyncio.run(main.create_liability(main.LiabilityCreate(**payload), db))


def create_observation(db, liability_id, **overrides):
    payload = {"balance": 100.0, "observed_on": "2026-08-01"}
    payload.update(overrides)
    return asyncio.run(
        main.create_liability_balance_observation(liability_id, main.LiabilityBalanceObservationCreate(**payload), db)
    )


def update_liability(db, liability_id, **fields):
    return asyncio.run(main.update_liability(liability_id, main.LiabilityUpdate(**fields), db))


def liability_single_as_of(db, liability_id, as_of_date):
    return asyncio.run(main.get_liability_balance_as_of(liability_id, date.fromisoformat(as_of_date), db))


def liability_batch_as_of(db, dates, include_archived=False):
    return asyncio.run(
        main.list_liability_balances_as_of(
            dates=[date.fromisoformat(d) for d in dates], include_archived=include_archived, db=db
        )
    )


# ─── Cash: semantic equivalence with the single as-of endpoint ─────────────


def test_cash_batch_matches_single_as_of_across_accounts_and_dates():
    db, _ = make_session()
    a = create_cash_account(db, name="A")
    b = create_cash_account(db, name="B")
    start_cash_tracking(db, a["id"], effective_on="2026-08-01", observed_balance=1000.0)
    start_cash_tracking(db, b["id"], effective_on="2026-08-03", observed_balance=500.0)
    add_cash_activity(db, a["id"], transaction_type="INCOME", amount=200.0, occurred_on="2026-08-05")
    add_cash_activity(db, b["id"], transaction_type="EXPENSE", amount=50.0, occurred_on="2026-08-06", category="Food")

    dates = ["2026-08-02", "2026-08-05", "2026-08-06", "2026-08-10"]
    batch = cash_batch_as_of(db, dates)

    for account in (a, b):
        for d in dates:
            expected = cash_single_as_of(db, account["id"], d)
            actual = batch[str(account["id"])][d]
            assert actual["balance"] == expected["balance"]
            assert actual["available"] == expected["available"]


def test_cash_batch_no_baseline_is_unavailable_not_zero():
    db, _ = make_session()
    account = create_cash_account(db)

    batch = cash_batch_as_of(db, ["2026-08-10"])

    entry = batch[str(account["id"])]["2026-08-10"]
    assert entry["available"] is False
    assert entry["balance"] is None


def test_cash_batch_excludes_archived_by_default_includes_when_requested():
    db, _ = make_session()
    account = create_cash_account(db)
    start_cash_tracking(db, account["id"], effective_on="2026-08-01", observed_balance=1000.0)
    update_cash_account(db, account["id"], is_archived=True)

    default_batch = cash_batch_as_of(db, ["2026-08-05"])
    assert str(account["id"]) not in default_batch

    included_batch = cash_batch_as_of(db, ["2026-08-05"], include_archived=True)
    assert included_batch[str(account["id"])]["2026-08-05"]["balance"] == 1000.0


def test_cash_batch_workspace_isolation():
    db, _ = make_session()
    main._ws_id(db)  # establish the default workspace before the foreign one
    foreign_workspace = Workspace(name="Other")
    db.add(foreign_workspace)
    db.commit()
    foreign_account = CashAccount(workspace_id=foreign_workspace.id, name="Private", currency="THB", balance=20.0)
    db.add(foreign_account)
    db.commit()

    batch = cash_batch_as_of(db, ["2026-08-10"], include_archived=True)

    assert str(foreign_account.id) not in batch


def test_cash_batch_empty_workspace_returns_empty_map():
    db, _ = make_session()
    assert cash_batch_as_of(db, ["2026-08-10"]) == {}


def test_cash_batch_dedupes_duplicate_requested_dates():
    db, _ = make_session()
    account = create_cash_account(db)
    start_cash_tracking(db, account["id"], effective_on="2026-08-01", observed_balance=1000.0)

    batch = cash_batch_as_of(db, ["2026-08-05", "2026-08-05", "2026-08-05"])

    assert list(batch[str(account["id"])].keys()) == ["2026-08-05"]


def test_cash_batch_rejects_too_many_dates():
    db, _ = make_session()
    too_many_dates = sorted(
        {f"{y}-{m:02d}-{d:02d}" for y in (2026, 2027) for m in range(1, 13) for d in range(1, 29)}
    )  # 2*12*28 = 672 > 400
    with pytest.raises(HTTPException) as error:
        asyncio.run(
            main.list_cash_account_balances_as_of(
                dates=[date.fromisoformat(d) for d in too_many_dates],
                include_archived=False,
                db=db,
            )
        )
    assert error.value.status_code == 400


# ─── Cash: bounded query count (the actual fan-out this endpoint fixes) ────


def test_cash_batch_query_count_does_not_scale_with_date_count():
    db, engine = make_session()
    a = create_cash_account(db, name="A")
    b = create_cash_account(db, name="B")
    start_cash_tracking(db, a["id"], effective_on="2026-08-01", observed_balance=1000.0)
    start_cash_tracking(db, b["id"], effective_on="2026-08-01", observed_balance=500.0)
    for i in range(5):
        add_cash_activity(db, a["id"], transaction_type="INCOME", amount=1.0, occurred_on=f"2026-08-{6+i:02d}")

    def count_queries(dates):
        counter = {"n": 0}

        def on_execute(*args, **kwargs):
            counter["n"] += 1

        event.listen(engine, "before_cursor_execute", on_execute)
        try:
            cash_batch_as_of(db, dates)
        finally:
            event.remove(engine, "before_cursor_execute", on_execute)
        return counter["n"]

    few_dates = [f"2026-08-{d:02d}" for d in range(1, 6)]
    many_dates = [f"2026-08-{d:02d}" for d in range(1, 26)]

    queries_for_few = count_queries(few_dates)
    queries_for_many = count_queries(many_dates)

    # Query count is driven by account count, not date count — 5x the dates
    # must not multiply the query count (it would under the old per-pair
    # HTTP fan-out; here it must stay flat).
    assert queries_for_many == queries_for_few


# ─── Liability: semantic equivalence with the single as-of endpoint ────────


def test_liability_batch_matches_single_as_of_across_liabilities_and_dates():
    db, _ = make_session()
    l1 = create_liability(db, name="Loan A")
    l2 = create_liability(db, name="Loan B")
    create_observation(db, l1["id"], balance=1000.0, observed_on="2026-08-01")
    create_observation(db, l1["id"], balance=900.0, observed_on="2026-08-10")
    create_observation(db, l2["id"], balance=500.0, observed_on="2026-08-05")

    dates = ["2026-07-31", "2026-08-01", "2026-08-05", "2026-08-10", "2026-08-15"]
    batch = liability_batch_as_of(db, dates)

    for liability in (l1, l2):
        for d in dates:
            expected = liability_single_as_of(db, liability["id"], d)
            actual = batch[str(liability["id"])][d]
            assert actual["balance"] == expected["balance"]
            assert actual["available"] == expected["available"]
            assert actual["currency"] == expected["currency"]


def test_liability_batch_no_observation_is_unavailable_not_zero():
    db, _ = make_session()
    liability = create_liability(db)

    batch = liability_batch_as_of(db, ["2026-08-10"])

    entry = batch[str(liability["id"])]["2026-08-10"]
    assert entry["available"] is False
    assert entry["balance"] is None


def test_liability_batch_excludes_archived_by_default_includes_when_requested():
    db, _ = make_session()
    liability = create_liability(db)
    create_observation(db, liability["id"], balance=2000.0, observed_on="2026-08-01")
    update_liability(db, liability["id"], is_archived=True)

    default_batch = liability_batch_as_of(db, ["2026-08-05"])
    assert str(liability["id"]) not in default_batch

    included_batch = liability_batch_as_of(db, ["2026-08-05"], include_archived=True)
    assert included_batch[str(liability["id"])]["2026-08-05"]["balance"] == 2000.0


def test_liability_batch_workspace_isolation():
    db, _ = make_session()
    main._ws_id(db)
    foreign_workspace = Workspace(name="Other")
    db.add(foreign_workspace)
    db.commit()
    foreign_liability = Liability(
        workspace_id=foreign_workspace.id, name="Private", liability_type="OTHER", balance=1.0, currency="THB"
    )
    db.add(foreign_liability)
    db.commit()

    batch = liability_batch_as_of(db, ["2026-08-10"], include_archived=True)

    assert str(foreign_liability.id) not in batch


def test_liability_batch_query_count_does_not_scale_with_date_count():
    db, engine = make_session()
    liability = create_liability(db)
    for i in range(5):
        create_observation(db, liability["id"], balance=1000.0 - i * 10, observed_on=f"2026-08-{1+i:02d}")

    def count_queries(dates):
        counter = {"n": 0}

        def on_execute(*args, **kwargs):
            counter["n"] += 1

        event.listen(engine, "before_cursor_execute", on_execute)
        try:
            liability_batch_as_of(db, dates)
        finally:
            event.remove(engine, "before_cursor_execute", on_execute)
        return counter["n"]

    few_dates = [f"2026-08-{d:02d}" for d in range(1, 6)]
    many_dates = [f"2026-08-{d:02d}" for d in range(1, 26)]

    assert count_queries(many_dates) == count_queries(few_dates)
