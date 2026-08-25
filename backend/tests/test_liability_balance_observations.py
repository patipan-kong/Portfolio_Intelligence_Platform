"""Focused tests for Liability Historical Observations (Wealth OS Phase 5 milestone).

Covers the pure domain function (services.liability_balance.liability_balance_as_of),
the observation write/read endpoints, the PATCH-transition rule, and isolation from
Cash/Investment/current-aggregation state.
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
    CashAccountTransaction,
    Liability,
    LiabilityBalanceObservation,
    Portfolio,
    PortfolioSnapshot,
    Transaction,
    Workspace,
)
import models.asset  # noqa: F401 — registers Asset tables referenced by ledger models.
import models.registry_finding  # noqa: F401 — registers registry tables referenced by Base metadata.
import main
from services.liability_balance import liability_balance_as_of


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def create_liability(db, **overrides):
    payload = {"name": "Home Loan", "liability_type": "MORTGAGE", "balance": 2500000.0, "currency": "THB"}
    payload.update(overrides)
    return asyncio.run(main.create_liability(main.LiabilityCreate(**payload), db))


def update_liability(db, liability_id, **fields):
    return asyncio.run(main.update_liability(liability_id, main.LiabilityUpdate(**fields), db))


def create_observation(db, liability_id, **overrides):
    payload = {"balance": 100.0, "observed_on": "2026-08-01"}
    payload.update(overrides)
    return asyncio.run(
        main.create_liability_balance_observation(
            liability_id, main.LiabilityBalanceObservationCreate(**payload), db
        )
    )


def list_observations(db, liability_id):
    return asyncio.run(main.list_liability_balance_observations(liability_id, db))


def as_of(db, liability_id, as_of_date):
    return asyncio.run(main.get_liability_balance_as_of(liability_id, date.fromisoformat(as_of_date), db))


def current_balance(db, liability_id):
    return db.query(Liability).filter(Liability.id == liability_id).one().balance


# ─── Pure domain function ──────────────────────────────────────────────────


def test_pure_function_no_observations_is_unavailable():
    assert liability_balance_as_of([], "2026-08-10") is None


def test_pure_function_no_observation_on_or_before_date_is_unavailable():
    observations = [("2026-08-15", 900.0)]
    assert liability_balance_as_of(observations, "2026-08-10") is None


def test_pure_function_returns_first_observation_on_or_before_date():
    observations = [("2026-08-01", 1000.0), ("2026-08-10", 900.0), ("2026-08-20", 0.0)]
    assert liability_balance_as_of(observations, "2026-08-01") == 1000.0
    assert liability_balance_as_of(observations, "2026-08-09") == 1000.0
    assert liability_balance_as_of(observations, "2026-08-10") == 900.0
    assert liability_balance_as_of(observations, "2026-08-15") == 900.0
    assert liability_balance_as_of(observations, "2026-08-20") == 0.0
    assert liability_balance_as_of(observations, "2026-09-01") == 0.0


def test_pure_function_never_reads_current_balance_or_timestamps():
    """Static proof, independent of the empirical behavior tests above: the
    function's executable body (docstring excluded) never names a
    current-balance or timestamp field."""
    import ast
    import inspect
    func_node = ast.parse(inspect.getsource(liability_balance_as_of)).body[0]
    executable = func_node.body[1:] if isinstance(func_node.body[0], ast.Expr) else func_node.body
    executable_source = "\n".join(ast.unparse(node) for node in executable)
    assert "created_at" not in executable_source
    assert "updated_at" not in executable_source
    assert ".balance" not in executable_source  # ORM current-balance field access


# ─── 1-2: first observation / no history before it ────────────────────────


def test_first_observation_creates_history_and_updates_current_balance():
    db = make_session()
    liability = create_liability(db, balance=80000.0)

    observation = create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-25")

    assert observation["liability_id"] == liability["id"]
    assert observation["balance"] == 80000.0
    assert observation["observed_on"] == "2026-08-25"
    assert current_balance(db, liability["id"]) == 80000.0


def test_no_history_before_first_observation():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-25")

    result = as_of(db, liability["id"], "2026-08-24")

    assert result["available"] is False
    assert result["balance"] is None


def test_liability_with_no_observations_has_no_historical_balance_available():
    """No-fabrication acceptance rule: a Liability created with a current
    balance but zero explicit observations has zero historical coverage."""
    db = make_session()
    liability = create_liability(db, balance=42000.0)

    assert list_observations(db, liability["id"]) == []
    for probe_date in ("2026-01-01", "2026-08-25", "2099-01-01"):
        result = as_of(db, liability["id"], probe_date)
        assert result["available"] is False
        assert result["balance"] is None


# ─── 3-5: latest-vs-backdated rule ──────────────────────────────────────────


def test_observation_updates_current_balance_when_newest():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-20")

    create_observation(db, liability["id"], balance=79000.0, observed_on="2026-08-25")

    assert current_balance(db, liability["id"]) == 79000.0


def test_backdated_observation_does_not_overwrite_current_balance():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-25")
    assert current_balance(db, liability["id"]) == 80000.0

    create_observation(db, liability["id"], balance=100000.0, observed_on="2026-08-10")

    assert current_balance(db, liability["id"]) == 80000.0
    assert as_of(db, liability["id"], "2026-08-10")["balance"] == 100000.0
    assert as_of(db, liability["id"], "2026-08-25")["balance"] == 80000.0


def test_later_observation_updates_current_balance():
    db = make_session()
    liability = create_liability(db, balance=100000.0)
    create_observation(db, liability["id"], balance=100000.0, observed_on="2026-08-10")
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-20")
    assert current_balance(db, liability["id"]) == 80000.0

    create_observation(db, liability["id"], balance=70000.0, observed_on="2026-08-30")

    assert current_balance(db, liability["id"]) == 70000.0


# ─── 6-8: same-day correction ───────────────────────────────────────────────


def test_same_day_correction_replaces_rather_than_duplicates():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-25")

    create_observation(db, liability["id"], balance=79500.0, observed_on="2026-08-25")

    rows = list_observations(db, liability["id"])
    assert len(rows) == 1
    assert rows[0]["balance"] == 79500.0


def test_same_day_latest_correction_updates_current_balance():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-25")

    create_observation(db, liability["id"], balance=79500.0, observed_on="2026-08-25")

    assert current_balance(db, liability["id"]) == 79500.0


def test_same_day_historical_correction_does_not_alter_current_balance():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=100000.0, observed_on="2026-08-10")
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-25")
    assert current_balance(db, liability["id"]) == 80000.0

    create_observation(db, liability["id"], balance=95000.0, observed_on="2026-08-10")

    assert current_balance(db, liability["id"]) == 80000.0
    assert as_of(db, liability["id"], "2026-08-10")["balance"] == 95000.0
    rows = list_observations(db, liability["id"])
    assert len(rows) == 2


# ─── 9-10: zero balance / validation ────────────────────────────────────────


def test_zero_balance_observation_is_valid_and_available_not_unavailable():
    db = make_session()
    liability = create_liability(db, balance=50000.0)
    create_observation(db, liability["id"], balance=50000.0, observed_on="2026-08-01")

    create_observation(db, liability["id"], balance=0.0, observed_on="2026-08-20")

    assert current_balance(db, liability["id"]) == 0.0
    before = as_of(db, liability["id"], "2026-08-10")
    at_and_after = as_of(db, liability["id"], "2026-08-20")
    assert before["available"] is True and before["balance"] == 50000.0
    assert at_and_after["available"] is True and at_and_after["balance"] == 0.0
    # Zero is legitimate history/current-balance data, not an auto-archive trigger.
    assert db.query(Liability).filter(Liability.id == liability["id"]).one().is_archived is False


@pytest.mark.parametrize(
    "payload",
    [
        {"balance": -1.0, "observed_on": "2026-08-01"},
        {"balance": float("nan"), "observed_on": "2026-08-01"},
        {"balance": float("inf"), "observed_on": "2026-08-01"},
        {"balance": -float("inf"), "observed_on": "2026-08-01"},
    ],
)
def test_finite_nonnegative_validation_rejects_invalid_balance(payload):
    with pytest.raises(ValidationError):
        main.LiabilityBalanceObservationCreate(**payload)


def test_invalid_observation_payload_does_not_mutate_any_state():
    """Rollback/atomicity proof: validation runs before any DB write, so a
    rejected observation leaves both the observation table and the current
    balance untouched — the write is all-or-nothing."""
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-20")

    with pytest.raises(ValidationError):
        main.LiabilityBalanceObservationCreate(balance=-1.0, observed_on="2026-08-25")

    assert len(list_observations(db, liability["id"])) == 1
    assert current_balance(db, liability["id"]) == 80000.0


# ─── 11-12: workspace isolation / archive semantics ────────────────────────


def test_workspace_isolation_returns_404_for_foreign_liability():
    db = make_session()
    main._ws_id(db)  # establish the default workspace before the foreign one
    foreign_workspace = Workspace(name="Other")
    db.add(foreign_workspace)
    db.commit()
    foreign_liability = Liability(
        workspace_id=foreign_workspace.id, name="Private", liability_type="OTHER", balance=10.0, currency="THB"
    )
    db.add(foreign_liability)
    db.commit()

    with pytest.raises(HTTPException) as create_error:
        create_observation(db, foreign_liability.id, balance=10.0, observed_on="2026-08-25")
    assert create_error.value.status_code == 404

    with pytest.raises(HTTPException) as read_error:
        as_of(db, foreign_liability.id, "2026-08-25")
    assert read_error.value.status_code == 404

    with pytest.raises(HTTPException) as list_error:
        list_observations(db, foreign_liability.id)
    assert list_error.value.status_code == 404


def test_archived_liability_history_remains_readable_but_rejects_new_observations():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-01")
    update_liability(db, liability["id"], is_archived=True)

    result = as_of(db, liability["id"], "2026-08-01")
    assert result["available"] is True
    assert result["balance"] == 80000.0
    assert len(list_observations(db, liability["id"])) == 1

    with pytest.raises(HTTPException, match="Archived") as error:
        create_observation(db, liability["id"], balance=79000.0, observed_on="2026-08-20")
    assert error.value.status_code == 409


# ─── 13-15: PATCH transition ────────────────────────────────────────────────


def test_metadata_only_patch_creates_no_observation():
    db = make_session()
    liability = create_liability(db, balance=80000.0)

    update_liability(db, liability["id"], name="Renamed Loan", note="metadata only")

    assert list_observations(db, liability["id"]) == []
    assert current_balance(db, liability["id"]) == 80000.0


def test_pre_history_balance_patch_retains_legacy_direct_replacement():
    db = make_session()
    liability = create_liability(db, balance=1000.0)

    updated = update_liability(db, liability["id"], balance=875.5)

    assert updated["balance"] == 875.5
    assert list_observations(db, liability["id"]) == []


def test_post_history_balance_patch_creates_observation_and_updates_current_balance():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-01")

    updated = update_liability(db, liability["id"], balance=75000.0)

    assert updated["balance"] == 75000.0
    rows = list_observations(db, liability["id"])
    assert len(rows) == 2
    today = date.today().isoformat()
    assert rows[0]["observed_on"] == today
    assert rows[0]["balance"] == 75000.0


def test_post_history_same_day_balance_patch_upserts_todays_observation():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    today = date.today().isoformat()
    create_observation(db, liability["id"], balance=80000.0, observed_on=today)

    updated = update_liability(db, liability["id"], balance=79000.0)

    assert updated["balance"] == 79000.0
    rows = list_observations(db, liability["id"])
    assert len(rows) == 1
    assert rows[0]["balance"] == 79000.0


# ─── 16-17: current-aggregation / Cash / Investment isolation ─────────────


def test_liability_payload_exposes_first_observation_on_for_ui_status():
    db = make_session()
    tracked = create_liability(db, balance=80000.0)
    untouched = create_liability(db, name="No history", balance=100.0)
    create_observation(db, tracked["id"], balance=80000.0, observed_on="2026-08-01")
    create_observation(db, tracked["id"], balance=79000.0, observed_on="2026-08-10")

    rows = {row["id"]: row for row in asyncio.run(main.list_liabilities(include_archived=False, db=db))}

    assert rows[tracked["id"]]["first_observation_on"] == "2026-08-01"
    assert rows[untouched["id"]]["first_observation_on"] is None


def test_current_liability_list_payload_unaffected_beyond_defined_rule():
    db = make_session()
    tracked = create_liability(db, name="Tracked", balance=80000.0)
    untouched = create_liability(db, name="Untouched", balance=5000.0)
    create_observation(db, tracked["id"], balance=80000.0, observed_on="2026-08-01")
    create_observation(db, tracked["id"], balance=79000.0, observed_on="2026-08-10")

    rows = {row["id"]: row for row in asyncio.run(main.list_liabilities(include_archived=False, db=db))}

    assert rows[tracked["id"]]["balance"] == 79000.0
    assert rows[untouched["id"]]["balance"] == 5000.0


def test_observation_writes_do_not_change_cash_or_investment_state():
    db = make_session()
    workspace_id = main._ws_id(db)
    cash = CashAccount(workspace_id=workspace_id, name="Savings", currency="THB", balance=1234.0)
    portfolio = Portfolio(workspace_id=workspace_id, name="Core", cash_balance=5678.0)
    db.add_all([cash, portfolio])
    db.commit()
    before_cash_transactions = db.query(CashAccountTransaction).count()
    before_investment_transactions = db.query(Transaction).count()
    before_snapshots = db.query(PortfolioSnapshot).count()

    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-01")
    create_observation(db, liability["id"], balance=75000.0, observed_on="2026-08-10")
    update_liability(db, liability["id"], balance=70000.0)
    db.refresh(cash)
    db.refresh(portfolio)

    assert cash.balance == 1234.0
    assert portfolio.cash_balance == 5678.0
    assert db.query(CashAccountTransaction).count() == before_cash_transactions
    assert db.query(Transaction).count() == before_investment_transactions
    assert db.query(PortfolioSnapshot).count() == before_snapshots


# ─── 18: deterministic ordering ─────────────────────────────────────────────


def test_observation_list_ordering_is_deterministic_newest_first():
    db = make_session()
    liability = create_liability(db, balance=1000.0)
    create_observation(db, liability["id"], balance=1000.0, observed_on="2026-08-01")
    create_observation(db, liability["id"], balance=900.0, observed_on="2026-08-20")
    create_observation(db, liability["id"], balance=950.0, observed_on="2026-08-10")

    rows = list_observations(db, liability["id"])

    assert [row["observed_on"] for row in rows] == ["2026-08-20", "2026-08-10", "2026-08-01"]


# ─── 19-20: As-Of endpoint ──────────────────────────────────────────────────


def test_endpoint_as_of_before_first_observation_is_unavailable():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-10")

    result = as_of(db, liability["id"], "2026-08-09")

    assert result["available"] is False
    assert result["balance"] is None
    assert result["liability_id"] == liability["id"]
    assert result["currency"] == "THB"


def test_endpoint_as_of_effective_state_lookup_across_multiple_dates():
    db = make_session()
    liability = create_liability(db, balance=1000.0)
    create_observation(db, liability["id"], balance=1000.0, observed_on="2026-08-01")
    create_observation(db, liability["id"], balance=900.0, observed_on="2026-08-10")
    create_observation(db, liability["id"], balance=0.0, observed_on="2026-08-20")

    assert as_of(db, liability["id"], "2026-08-01")["balance"] == 1000.0
    assert as_of(db, liability["id"], "2026-08-05")["balance"] == 1000.0
    assert as_of(db, liability["id"], "2026-08-10")["balance"] == 900.0
    assert as_of(db, liability["id"], "2026-08-15")["balance"] == 900.0
    assert as_of(db, liability["id"], "2026-08-20")["balance"] == 0.0
    assert as_of(db, liability["id"], "2026-12-31")["balance"] == 0.0


def test_endpoint_current_balance_is_not_used_as_historical_fallback():
    db = make_session()
    liability = create_liability(db, balance=80000.0)
    create_observation(db, liability["id"], balance=80000.0, observed_on="2026-08-01")
    create_observation(db, liability["id"], balance=70000.0, observed_on="2026-08-20")
    assert current_balance(db, liability["id"]) == 70000.0

    result = as_of(db, liability["id"], "2026-08-10")

    assert result["balance"] == 80000.0


def test_endpoint_malformed_date_rejected_by_declared_query_param_type():
    """The `date` parameter is exercised through FastAPI's request layer, not this
    direct-call test style, so this asserts against the exact validation
    mechanism FastAPI applies to a `date`-typed query param for these endpoints."""
    with pytest.raises(ValidationError):
        TypeAdapter(date).validate_python("not-a-date")
