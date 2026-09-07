"""Focused coverage for Net Worth Change Attribution (Level-1, ADR-013).

Follows the direct-endpoint / in-memory-sqlite pattern used by
test_wealth_goals.py. Exercises the pure arithmetic in isolation, then the
DB-backed resolvers/orchestration through services.net_worth_change_attribution
directly, plus the FastAPI endpoint's date validation.
"""
import asyncio
import os
import sys
from datetime import date, datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import (
    Base,
    CashAccount,
    CashAccountBaseline,
    CashAccountTransaction,
    Liability,
    LiabilityBalanceObservation,
    Portfolio,
    PortfolioSnapshot,
)
import models.asset  # noqa: F401 — registers Asset tables referenced by ledger models.
import models.registry_finding  # noqa: F401 — registers registry tables referenced by Base metadata.
import main
from services import net_worth_change_attribution as attribution


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def ws_id(db):
    return main._ws_id(db)


def add_portfolio(db, ws, created_at=datetime(2026, 1, 1)):
    p = Portfolio(workspace_id=ws, name="P", created_at=created_at)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def add_snapshot(db, ws, portfolio_id, snapshot_date, total_value):
    s = PortfolioSnapshot(
        workspace_id=ws, portfolio_id=portfolio_id, snapshot_date=snapshot_date,
        total_value=total_value, cash_balance=0.0, total_invested=total_value,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


def add_cash_account(db, ws, created_at=datetime(2026, 1, 1), is_archived=False):
    a = CashAccount(workspace_id=ws, name="Cash", currency="THB", balance=0.0,
                     is_archived=is_archived, created_at=created_at)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def add_baseline(db, account_id, effective_on, observed_balance):
    b = CashAccountBaseline(cash_account_id=account_id, effective_on=effective_on, observed_balance=observed_balance)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


def add_cash_tx(db, ws, account_id, transaction_type, amount, occurred_on, counterparty_portfolio_id=None):
    tx = CashAccountTransaction(
        workspace_id=ws, cash_account_id=account_id, transaction_type=transaction_type,
        amount=amount, occurred_on=occurred_on, counterparty_portfolio_id=counterparty_portfolio_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def add_liability(db, ws, created_at=datetime(2026, 1, 1), is_archived=False):
    l = Liability(workspace_id=ws, name="Loan", liability_type="OTHER", balance=0.0,
                  currency="THB", is_archived=is_archived, created_at=created_at)
    db.add(l)
    db.commit()
    db.refresh(l)
    return l


def add_observation(db, ws, liability_id, observed_on, balance):
    o = LiabilityBalanceObservation(workspace_id=ws, liability_id=liability_id, observed_on=observed_on, balance=balance)
    db.add(o)
    db.commit()
    db.refresh(o)
    return o


# ── A. Pure reconciliation ──────────────────────────────────────────────────

def test_pure_component_impacts_sum_to_net_worth_delta():
    start_values = {"investment_assets": 200_000.0, "external_cash": 100_000.0, "total_liabilities": 10_000.0}
    end_values = {"investment_assets": 260_000.0, "external_cash": 70_000.0, "total_liabilities": 5_000.0}
    result = attribution.build_available_result("2026-08-12", "2026-08-13", start_values, end_values)
    assert result is not None
    assert result["status"] == "AVAILABLE"
    assert sum(result["components"].values()) == pytest.approx(result["net_worth_change"])
    assert result["reconciliation_difference"] == pytest.approx(0.0)


# ── B. Investment-only movement ─────────────────────────────────────────────

def test_investment_only_movement():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 200_000.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 250_000.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["components"]["investment_assets_change"] == pytest.approx(50_000.0)
    assert result["components"]["external_cash_change"] == pytest.approx(0.0)
    assert result["components"]["liability_impact"] == pytest.approx(0.0)
    assert result["net_worth_change"] == pytest.approx(50_000.0)


# ── C. Cash-only movement ───────────────────────────────────────────────────

def test_cash_only_movement():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 200_000.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 200_000.0)

    a = add_cash_account(db, ws)
    add_baseline(db, a.id, "2026-08-01", 100_000.0)
    add_cash_tx(db, ws, a.id, "EXPENSE", 30_000.0, "2026-08-13")

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["components"]["investment_assets_change"] == pytest.approx(0.0)
    assert result["components"]["external_cash_change"] == pytest.approx(-30_000.0)
    assert result["net_worth_change"] == pytest.approx(-30_000.0)


# ── D. Liability decline ────────────────────────────────────────────────────

def test_liability_decline_is_a_positive_net_worth_impact():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 0.0)

    l = add_liability(db, ws)
    add_observation(db, ws, l.id, "2026-08-01", 50_000.0)
    add_observation(db, ws, l.id, "2026-08-13", 20_000.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["components"]["liability_impact"] == pytest.approx(30_000.0)
    assert result["net_worth_change"] == pytest.approx(30_000.0)


# ── E. Mixed movement ────────────────────────────────────────────────────────

def test_mixed_movement_reconciles_exactly():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 200_000.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 230_000.0)

    a = add_cash_account(db, ws)
    add_baseline(db, a.id, "2026-08-01", 100_000.0)
    add_cash_tx(db, ws, a.id, "EXPENSE", 10_000.0, "2026-08-12")

    l = add_liability(db, ws)
    add_observation(db, ws, l.id, "2026-08-01", 50_000.0)
    add_observation(db, ws, l.id, "2026-08-13", 45_000.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    total = sum(result["components"].values())
    assert total == pytest.approx(result["net_worth_change"])
    assert result["reconciliation_difference"] == pytest.approx(0.0)


# ── F. Offsetting components ────────────────────────────────────────────────

def test_offsetting_components_still_available_with_zero_delta():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 200_000.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 250_000.0)

    a = add_cash_account(db, ws)
    add_baseline(db, a.id, "2026-08-01", 100_000.0)
    add_cash_tx(db, ws, a.id, "EXPENSE", 50_000.0, "2026-08-13")

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["components"]["investment_assets_change"] == pytest.approx(50_000.0)
    assert result["components"]["external_cash_change"] == pytest.approx(-50_000.0)
    assert result["net_worth_change"] == pytest.approx(0.0)


# ── G/H. Missing start / end evidence ───────────────────────────────────────

def test_missing_start_snapshot_is_unavailable_not_zero():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-13", 250_000.0)  # no 08-12 snapshot

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "UNAVAILABLE"
    assert "INVESTMENT_EVIDENCE_INCOMPLETE_AT_START" in result["reason_codes"]
    assert "components" not in result


def test_missing_end_snapshot_is_unavailable_not_zero():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 200_000.0)  # no 08-13 snapshot

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "UNAVAILABLE"
    assert "INVESTMENT_EVIDENCE_INCOMPLETE_AT_END" in result["reason_codes"]
    assert "components" not in result


# ── I. Reconciliation guard ─────────────────────────────────────────────────

def test_reconciliation_guard_rejects_artificially_inconsistent_evidence(monkeypatch):
    monkeypatch.setattr(attribution, "net_worth_change", lambda start, end: 999_999.0)
    start_values = {"investment_assets": 200_000.0, "external_cash": 100_000.0, "total_liabilities": 0.0}
    end_values = {"investment_assets": 250_000.0, "external_cash": 100_000.0, "total_liabilities": 0.0}
    result = attribution.build_available_result("2026-08-12", "2026-08-13", start_values, end_values)
    assert result is None


def test_reconciliation_guard_end_to_end_via_orchestration(monkeypatch):
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 200_000.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 250_000.0)

    monkeypatch.setattr(attribution, "net_worth_change", lambda start, end: 999_999.0)
    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "UNAVAILABLE"
    assert result["reason_codes"] == ["RECONCILIATION_FAILURE"]


# ── J. Archived Cash Account / Liability history remains included ──────────

def test_archived_cash_account_and_liability_remain_included():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 0.0)

    a = add_cash_account(db, ws, is_archived=True)
    add_baseline(db, a.id, "2026-08-01", 40_000.0)

    l = add_liability(db, ws, is_archived=True)
    add_observation(db, ws, l.id, "2026-08-01", 10_000.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["start"]["external_cash"] == pytest.approx(40_000.0)
    assert result["start"]["total_liabilities"] == pytest.approx(10_000.0)


# ── K. New tracking scope disclosure ────────────────────────────────────────

def test_new_tracking_scope_disclosed_when_account_created_mid_period():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 0.0)

    # Not expected at start (created after start_date), expected at end.
    a = add_cash_account(db, ws, created_at=datetime(2026, 8, 13, 0, 0, 1))
    add_baseline(db, a.id, "2026-08-13", 5_000.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["new_tracking_scope"] is True


def test_no_new_tracking_scope_when_all_entities_predate_start():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 0.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["new_tracking_scope"] is False


# ── L. NWCA-01 correction: Bangkok lifecycle-date boundary ─────────────────
# 2026-08-12 18:00 UTC = 2026-08-13 01:00 Bangkok (UTC+7) — crosses the
# Bangkok calendar-date boundary. Pre-correction (raw created_at.strftime
# calendar date), an entity created at this instant was wrongly read as
# already-expected on Bangkok date 2026-08-12.

_BOUNDARY_UTC = datetime(2026, 8, 12, 18, 0, 0)
_NON_BOUNDARY_UTC = datetime(2026, 8, 12, 3, 0, 0)  # 10:00 Bangkok — same calendar day


def test_lifecycle_date_helper_crosses_bangkok_boundary():
    assert attribution.lifecycle_date(_BOUNDARY_UTC) == date(2026, 8, 13)


def test_lifecycle_date_helper_non_boundary_control_retains_same_day():
    assert attribution.lifecycle_date(_NON_BOUNDARY_UTC) == date(2026, 8, 12)


def test_portfolio_not_yet_expected_on_utc_calendar_date_before_bangkok_boundary():
    db = make_session()
    ws = ws_id(db)
    # An older Portfolio keeps the "expected" set non-empty at start, isolating
    # the boundary Portfolio's own lifecycle classification.
    old = add_portfolio(db, ws, created_at=datetime(2026, 1, 1))
    add_snapshot(db, ws, old.id, "2026-08-12", 100_000.0)
    add_snapshot(db, ws, old.id, "2026-08-13", 100_000.0)

    boundary = add_portfolio(db, ws, created_at=_BOUNDARY_UTC)
    add_snapshot(db, ws, boundary.id, "2026-08-13", 50_000.0)  # no 08-12 snapshot — not yet expected

    inv_start, ok_start = attribution._resolve_investment_assets(db, ws, "2026-08-12")
    assert ok_start is True
    assert inv_start == pytest.approx(100_000.0)  # only `old` counted — `boundary` not yet expected

    inv_end, ok_end = attribution._resolve_investment_assets(db, ws, "2026-08-13")
    assert ok_end is True
    assert inv_end == pytest.approx(150_000.0)  # both now expected


def test_cash_account_not_yet_expected_on_utc_calendar_date_before_bangkok_boundary():
    db = make_session()
    ws = ws_id(db)
    a = add_cash_account(db, ws, created_at=_BOUNDARY_UTC)
    add_baseline(db, a.id, "2026-08-13", 5_000.0)

    total_start, ok_start = attribution._resolve_external_cash(db, ws, "2026-08-12")
    assert ok_start is True
    assert total_start == pytest.approx(0.0)  # zero expected cash accounts is a legitimate zero

    total_end, ok_end = attribution._resolve_external_cash(db, ws, "2026-08-13")
    assert ok_end is True
    assert total_end == pytest.approx(5_000.0)


def test_liability_not_yet_expected_on_utc_calendar_date_before_bangkok_boundary():
    db = make_session()
    ws = ws_id(db)
    l = add_liability(db, ws, created_at=_BOUNDARY_UTC)
    add_observation(db, ws, l.id, "2026-08-13", 20_000.0)

    total_start, ok_start = attribution._resolve_total_liabilities(db, ws, "2026-08-12")
    assert ok_start is True
    assert total_start == pytest.approx(0.0)  # zero expected liabilities is a legitimate zero

    total_end, ok_end = attribution._resolve_total_liabilities(db, ws, "2026-08-13")
    assert ok_end is True
    assert total_end == pytest.approx(20_000.0)


# ── M. NWCA-01 correction: completeness parity end-to-end (orchestration) ──

def test_completeness_parity_end_to_end_across_bangkok_boundary():
    """Reproduces the independent-review counterexample: a Portfolio created
    at 2026-08-12 18:00 UTC (Bangkok lifecycle date 2026-08-13) must not be
    treated as already-expected on Bangkok date 2026-08-12. Pre-correction
    (raw UTC calendar date), this Portfolio was wrongly counted as expected
    at start with no start-date snapshot, making the whole attribution wrongly
    UNAVAILABLE (INVESTMENT_EVIDENCE_INCOMPLETE_AT_START) instead of AVAILABLE."""
    db = make_session()
    ws = ws_id(db)
    old = add_portfolio(db, ws, created_at=datetime(2026, 1, 1))
    add_snapshot(db, ws, old.id, "2026-08-12", 100_000.0)
    add_snapshot(db, ws, old.id, "2026-08-13", 100_000.0)

    new = add_portfolio(db, ws, created_at=_BOUNDARY_UTC)
    add_snapshot(db, ws, new.id, "2026-08-13", 50_000.0)  # no start snapshot — not yet expected

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["start"]["investment_assets"] == pytest.approx(100_000.0)
    assert result["end"]["investment_assets"] == pytest.approx(150_000.0)
    assert result["components"]["investment_assets_change"] == pytest.approx(50_000.0)


# ── N. NWCA-02 correction: cross-domain new_tracking_scope disclosure ──────

def test_new_tracking_scope_disclosed_when_portfolio_created_mid_period():
    db = make_session()
    ws = ws_id(db)
    old = add_portfolio(db, ws, created_at=datetime(2026, 1, 1))
    add_snapshot(db, ws, old.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, old.id, "2026-08-13", 0.0)

    new = add_portfolio(db, ws, created_at=datetime(2026, 8, 13, 0, 0, 1))
    add_snapshot(db, ws, new.id, "2026-08-13", 0.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["new_tracking_scope"] is True


def test_new_tracking_scope_disclosed_when_liability_created_mid_period():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 0.0)

    l = add_liability(db, ws, created_at=datetime(2026, 8, 13, 0, 0, 1))
    add_observation(db, ws, l.id, "2026-08-13", 5_000.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["new_tracking_scope"] is True


def test_no_new_tracking_scope_when_portfolio_created_before_start():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws, created_at=datetime(2026, 1, 1))
    add_snapshot(db, ws, p.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 0.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["new_tracking_scope"] is False


def test_no_new_tracking_scope_when_portfolio_created_after_end():
    db = make_session()
    ws = ws_id(db)
    old = add_portfolio(db, ws, created_at=datetime(2026, 1, 1))
    add_snapshot(db, ws, old.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, old.id, "2026-08-13", 0.0)

    # Created after end_date — must never affect this window's disclosure.
    add_portfolio(db, ws, created_at=datetime(2026, 9, 1))

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["new_tracking_scope"] is False


def test_new_tracking_scope_bangkok_boundary_portfolio_classified_by_bangkok_date():
    """A Portfolio whose UTC created_at falls on 2026-08-12 (the raw calendar
    date pre-correction would say 'already expected at start') but whose
    Bangkok lifecycle date is 2026-08-13 (inside the attribution period) must
    disclose new_tracking_scope=True — not the False that raw UTC calendar-
    date semantics would incorrectly produce."""
    db = make_session()
    ws = ws_id(db)
    old = add_portfolio(db, ws, created_at=datetime(2026, 1, 1))
    add_snapshot(db, ws, old.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, old.id, "2026-08-13", 0.0)

    # 2026-08-12 23:00 UTC = 2026-08-13 06:00 Bangkok.
    new = add_portfolio(db, ws, created_at=datetime(2026, 8, 12, 23, 0, 0))
    add_snapshot(db, ws, new.id, "2026-08-13", 0.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["new_tracking_scope"] is True


# ── O. Liability-increase coverage (Section 15) ─────────────────────────────

def test_liability_increase_is_a_negative_net_worth_impact():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 0.0)

    l = add_liability(db, ws)
    add_observation(db, ws, l.id, "2026-08-01", 20_000.0)
    add_observation(db, ws, l.id, "2026-08-13", 50_000.0)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["components"]["liability_impact"] == pytest.approx(-30_000.0)
    assert result["net_worth_change"] == pytest.approx(-30_000.0)


# ── Section 29: Investment Funding Transfer boundary (half-recorded) ───────

def test_half_recorded_investment_funding_reports_cash_movement_only():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 200_000.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 200_000.0)  # no Portfolio-side deposit recorded

    a = add_cash_account(db, ws)
    add_baseline(db, a.id, "2026-08-01", 100_000.0)
    add_cash_tx(db, ws, a.id, "INVESTMENT_TRANSFER", -50_000.0, "2026-08-13", counterparty_portfolio_id=p.id)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["components"]["investment_assets_change"] == pytest.approx(0.0)
    assert result["components"]["external_cash_change"] == pytest.approx(-50_000.0)
    assert result["net_worth_change"] == pytest.approx(-50_000.0)


def test_separately_recorded_portfolio_deposit_shows_independent_investment_movement():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 200_000.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 250_000.0)  # Portfolio DEPOSIT of 50k also recorded

    a = add_cash_account(db, ws)
    add_baseline(db, a.id, "2026-08-01", 100_000.0)
    add_cash_tx(db, ws, a.id, "INVESTMENT_TRANSFER", -50_000.0, "2026-08-13", counterparty_portfolio_id=p.id)

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["components"]["investment_assets_change"] == pytest.approx(50_000.0)
    assert result["components"]["external_cash_change"] == pytest.approx(-50_000.0)
    assert result["net_worth_change"] == pytest.approx(0.0)


# ── Section 30: cash↔cash transfer regression ───────────────────────────────

def test_internal_cash_transfer_has_no_aggregate_external_cash_effect():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 0.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 0.0)

    a = add_cash_account(db, ws)
    b = add_cash_account(db, ws)
    add_baseline(db, a.id, "2026-08-01", 60_000.0)
    add_baseline(db, b.id, "2026-08-01", 10_000.0)
    add_cash_tx(db, ws, a.id, "TRANSFER", -20_000.0, "2026-08-13")
    add_cash_tx(db, ws, b.id, "TRANSFER", 20_000.0, "2026-08-13")

    result = attribution.get_change_attribution(db, ws, "2026-08-12", "2026-08-13")
    assert result["status"] == "AVAILABLE"
    assert result["components"]["external_cash_change"] == pytest.approx(0.0)
    assert result["start"]["external_cash"] == pytest.approx(70_000.0)
    assert result["end"]["external_cash"] == pytest.approx(70_000.0)


# ── Endpoint validation ──────────────────────────────────────────────────────

def test_endpoint_rejects_start_not_before_end():
    db = make_session()
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(main.get_net_worth_change_attribution(start=date(2026, 8, 13), end=date(2026, 8, 12), db=db))
    assert exc_info.value.status_code == 400

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(main.get_net_worth_change_attribution(start=date(2026, 8, 12), end=date(2026, 8, 12), db=db))
    assert exc_info.value.status_code == 400


def test_endpoint_returns_available_result():
    db = make_session()
    ws = ws_id(db)
    p = add_portfolio(db, ws)
    add_snapshot(db, ws, p.id, "2026-08-12", 200_000.0)
    add_snapshot(db, ws, p.id, "2026-08-13", 250_000.0)

    result = asyncio.run(main.get_net_worth_change_attribution(start=date(2026, 8, 12), end=date(2026, 8, 13), db=db))
    assert result["status"] == "AVAILABLE"
    assert result["start_date"] == "2026-08-12"
    assert result["end_date"] == "2026-08-13"
