"""Tests for the snapshot return recovery engine.

Scenarios covered
-----------------
 1. Baseline snapshot  → all return fields are None (no previous NAV)
 2. Single DEPOSIT     → net_external_cash_flow stripped; investment_return_pct correct
 3. WITHDRAW           → reduces net_external_cash_flow
 4. INITIAL_CASH       → treated as inflow (same as DEPOSIT)
 5. INITIAL_POSITION   → creates imported_asset_value; return stripped accordingly
 6. QUANTITY_CORRECTION → creates manual_adjustment_value
 7. SELL transaction   → period_realized_pnl from notes; SELL fees in period_fees_paid
 8. DIVIDEND           → period_dividend_income
 9. BUY fees           → period_fees_paid
10. Bookkeeping on baseline day excluded from next window (Portfolio-2 scenario)
11. Portfolio-4 repaired baseline: first snapshot has None, second computes correctly
12. Dry run            → values computed, DB untouched
13. No-op              → already-correct fields produce unchanged=True
14. Idempotency        → running twice yields identical results
15. Rollback           → caller controls commit; partial writes safe
16. Multi-portfolio    → recover_all handles each portfolio independently
17. Unknown portfolio  → returns error result
18. Empty portfolio    → 0 snapshots scanned, no error
"""
from __future__ import annotations

import asyncio
import json
import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401 — registers the `assets` FK target table on Base.metadata
from models.database import (
    Base, Portfolio, PortfolioItem, PortfolioSnapshot, Transaction, Workspace,
)
from services import asset_registry as registry
from services.asset_domain import AssetClaim, AssetType, IdentifierRecord, IdentifierType
from services.portfolio_snapshots import generate_daily_snapshot
from services.portfolio_transactions import execute_position_conversion
from services.snapshot_return_recovery import (
    PortfolioReturnRecoveryResult,
    SnapshotReturnDiff,
    _RETURN_FIELDS,
    recover_all_snapshot_returns,
    recover_portfolio_snapshot_returns,
)


# ── DB helpers ─────────────────────────────────────────────────────────────────

def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def _seed(db, cash: float = 0.0, name: str = "Test") -> tuple:
    ws = Workspace(name="TestWS")
    db.add(ws)
    db.flush()
    p = Portfolio(workspace_id=ws.id, name=name, cash_balance=cash)
    db.add(p)
    db.commit()
    return ws, p


def _snap(
    db,
    portfolio_id: int,
    workspace_id: int,
    date: str,
    total_value: float,
    cash_balance: float = 0.0,
    *,
    investment_return_pct: float | None = None,
    daily_return_pct: float | None = None,
    investment_return_amount: float | None = None,
    net_external_cash_flow: float | None = None,
    imported_asset_value: float | None = None,
    manual_adjustment_value: float | None = None,
    period_realized_pnl: float | None = None,
    period_dividend_income: float | None = None,
    period_fees_paid: float | None = None,
) -> PortfolioSnapshot:
    s = PortfolioSnapshot(
        workspace_id           = workspace_id,
        portfolio_id           = portfolio_id,
        snapshot_date          = date,
        total_value            = total_value,
        cash_balance           = cash_balance,
        total_invested         = total_value - cash_balance,
        investment_return_pct  = investment_return_pct,
        daily_return_pct       = daily_return_pct,
        investment_return_amount = investment_return_amount,
        net_external_cash_flow = net_external_cash_flow,
        imported_asset_value   = imported_asset_value,
        manual_adjustment_value = manual_adjustment_value,
        period_realized_pnl    = period_realized_pnl,
        period_dividend_income = period_dividend_income,
        period_fees_paid       = period_fees_paid,
    )
    db.add(s)
    db.commit()
    return s


def _tx(
    db,
    portfolio_id: int,
    workspace_id: int,
    tx_type: str,
    total_amount: float,
    created_at: datetime,
    *,
    symbol: str | None = None,
    shares: float | None = None,
    price_per_share: float | None = None,
    fees: float = 0.0,
    taxes: float = 0.0,
    notes: str | None = None,
    asset_id: int | None = None,
    conversion_payload: dict | None = None,
) -> Transaction:
    t = Transaction(
        workspace_id       = workspace_id,
        portfolio_id       = portfolio_id,
        transaction_type   = tx_type,
        total_amount       = total_amount,
        symbol             = symbol,
        shares             = shares,
        price_per_share    = price_per_share,
        fees               = fees,
        taxes              = taxes,
        transaction_date   = created_at,
        created_at         = created_at,
        notes              = notes,
        asset_id           = asset_id,
        conversion_payload = conversion_payload,
    )
    db.add(t)
    db.commit()
    return t


def _d(offset: int) -> str:
    """Return a date string N days before today."""
    return (datetime.utcnow() - timedelta(days=offset)).strftime("%Y-%m-%d")


def _dt(offset: int) -> datetime:
    """Return midnight UTC N days before today."""
    base = datetime.utcnow() - timedelta(days=offset)
    return base.replace(hour=0, minute=0, second=0, microsecond=0)


# ── Test 1: Baseline snapshot has all-None return fields ──────────────────────

def test_baseline_snapshot_returns_none():
    """The first snapshot (no prev) must always produce None for every return field."""
    db = make_session()
    ws, p = _seed(db)
    _snap(db, p.id, ws.id, _d(5), 100_000.0, cash_balance=100_000.0,
          investment_return_pct=99.0)  # wrong value that should become None

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)

    assert result.snapshots_scanned == 1
    assert len(result.diffs) == 1
    diff = result.diffs[0]
    for f in _RETURN_FIELDS:
        assert diff.new_values[f] is None, f"{f} should be None for baseline"


# ── Test 2: DEPOSIT is stripped from returns ──────────────────────────────────

def test_deposit_stripped_from_investment_return():
    """A DEPOSIT in the period increases NAV but must not inflate investment_return_pct."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0, cash_balance=100_000.0)
    _snap(db, p.id, ws.id, d1, 122_000.0, cash_balance=122_000.0)  # +22k NAV

    # DEPOSIT of 22,000 happens between d0 and d1
    _tx(db, p.id, ws.id, "DEPOSIT", 22_000.0, _dt(2) + timedelta(hours=10))

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    d1_diff = result.diffs[1]

    # pure_market_gain = 122,000 − 100,000 − 22,000 = 0
    assert d1_diff.new_values["investment_return_pct"]    == pytest.approx(0.0, abs=1e-4)
    assert d1_diff.new_values["investment_return_amount"] == pytest.approx(0.0, abs=0.01)
    assert d1_diff.new_values["net_external_cash_flow"]   == pytest.approx(22_000.0, abs=0.01)
    assert d1_diff.new_values["daily_return_pct"]         == pytest.approx(0.0, abs=1e-4)


# ── Test 3: WITHDRAW reduces net_external_cash_flow ──────────────────────────

def test_withdraw_reduces_net_external_cash_flow():
    """A WITHDRAW subtracts from net_external_cash_flow."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0, cash_balance=100_000.0)
    _snap(db, p.id, ws.id, d1,  95_000.0, cash_balance=95_000.0)

    _tx(db, p.id, ws.id, "WITHDRAW", 5_000.0, _dt(2) + timedelta(hours=10))

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    d1_diff = result.diffs[1]

    # pure_market_gain = 95,000 − 100,000 − (0 − 5,000) = 0
    assert d1_diff.new_values["net_external_cash_flow"] == pytest.approx(-5_000.0, abs=0.01)
    assert d1_diff.new_values["investment_return_pct"]  == pytest.approx(0.0, abs=1e-4)


# ── Test 4: INITIAL_CASH treated as inflow ────────────────────────────────────

def test_initial_cash_treated_as_inflow():
    """INITIAL_CASH is in _CASH_INFLOW_TYPES and must be stripped the same as DEPOSIT."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 50_000.0, cash_balance=50_000.0)
    _snap(db, p.id, ws.id, d1, 60_000.0, cash_balance=60_000.0)

    _tx(db, p.id, ws.id, "INITIAL_CASH", 10_000.0, _dt(2) + timedelta(hours=6))

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    d1_diff = result.diffs[1]

    assert d1_diff.new_values["net_external_cash_flow"] == pytest.approx(10_000.0, abs=0.01)
    assert d1_diff.new_values["investment_return_pct"]  == pytest.approx(0.0, abs=1e-4)


# ── Test 5: INITIAL_POSITION creates imported_asset_value ─────────────────────

def test_initial_position_stripped_as_imported_asset_value():
    """An INITIAL_POSITION import must create imported_asset_value so the equity
    injection does not inflate investment_return_pct."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(4), _d(3)
    prev_nav  = 100_000.0
    import_mv = 200 * 50.0  # 10,000

    _snap(db, p.id, ws.id, d0, prev_nav, cash_balance=prev_nav)
    _snap(db, p.id, ws.id, d1, prev_nav + import_mv, cash_balance=prev_nav)

    _tx(
        db, p.id, ws.id, "INITIAL_POSITION", import_mv,
        _dt(3) + timedelta(hours=8),
        symbol="SCB.BK", shares=200.0, price_per_share=50.0,
    )

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    d1_diff = result.diffs[1]

    assert d1_diff.new_values["imported_asset_value"]     == pytest.approx(import_mv, abs=0.01)
    assert d1_diff.new_values["investment_return_pct"]    == pytest.approx(0.0, abs=1e-4)
    assert d1_diff.new_values["net_external_cash_flow"]   is None


# ── Test 6: QUANTITY_CORRECTION creates manual_adjustment_value ───────────────

def test_quantity_correction_creates_manual_adjustment_value():
    """A share-count correction must create manual_adjustment_value and not
    inflate investment_return_pct."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    adj_mv = 50 * 100.0  # 5,000
    _snap(db, p.id, ws.id, d0, 200_000.0)
    _snap(db, p.id, ws.id, d1, 205_000.0)

    _tx(
        db, p.id, ws.id, "QUANTITY_CORRECTION", adj_mv,
        _dt(2) + timedelta(hours=9),
        symbol="AOT.BK", shares=50.0, price_per_share=100.0,
    )

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    d1_diff = result.diffs[1]

    assert d1_diff.new_values["manual_adjustment_value"] == pytest.approx(adj_mv, abs=0.01)
    assert d1_diff.new_values["investment_return_pct"]   == pytest.approx(0.0, abs=1e-4)


# ── Test 7: SELL transaction produces period_realized_pnl and fees ────────────

def test_sell_transaction_period_realized_pnl_and_fees():
    """A SELL with notes containing 'Realized P&L: +1500' must be reflected
    in period_realized_pnl; fees+taxes in period_fees_paid."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0)
    _snap(db, p.id, ws.id, d1, 101_200.0)  # small NAV rise

    _tx(
        db, p.id, ws.id, "SELL", 15_000.0,
        _dt(2) + timedelta(hours=11),
        symbol="PTT.BK", shares=100.0, price_per_share=150.0,
        fees=100.0, taxes=7.0,
        notes="Sell 100 PTT.BK @ 150. Realized P&L: +1500.00",
    )

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    d1_diff = result.diffs[1]

    assert d1_diff.new_values["period_realized_pnl"] == pytest.approx(1500.0, abs=0.01)
    assert d1_diff.new_values["period_fees_paid"]    == pytest.approx(107.0,  abs=0.01)


# ── BANPU-WP5-A3: POSITION_CONVERSION recovery-path parity ──────────────────

def test_wp5_position_conversion_recovery_path_parity():
    """The recovery path must classify POSITION_CONVERSION identically to the
    live snapshot path: admitted cash-in-lieu realized_pnl/fees counted
    exactly once; no external/import/manual-adjustment contribution."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0)
    _snap(db, p.id, ws.id, d1, 100_050.0)

    # Same validated numbers as test_position_conversion_replay.py's
    # test_step7_cross_engine_parity_generic_cash_in_lieu fixture — satisfies
    # every parse_position_conversion_payload() invariant exactly.
    payload = {
        "schema_version": 1,
        "predecessor": {"asset_id": 101, "symbol": "PCONV.BK", "shares_surrendered": "8"},
        "successor": {
            "asset_id": 102, "symbol": "SCONV.BK", "provider_symbol": "SCONV.BK",
            "shares_entitled": "10", "shares_received": "9.5",
        },
        "conversion_ratio": "1.25",
        "basis": {"before": "240", "allocated_to_cash_in_lieu": "12", "carried_to_successor": "228"},
        "cash_in_lieu": {
            "fractional_entitlement_shares": "0.5",
            "gross_proceeds": "15",
            "fees": "1",
            "taxes": "0.5",
            "net_cash": "13.5",
            "basis_allocated": "12",
            "realized_pnl": "1.5",
        },
        "dates": {
            "legal_effective_date": "2026-06-01",
            "valuation_transition_date": "2026-06-01",
            "predecessor_last_price_date": "2026-05-29",
            "successor_quote_epoch_start_date": "2026-06-01",
        },
        "quote_binding": {
            "provider": "test-provider",
            "predecessor_provider_symbol": "PCONV.BK",
            "successor_provider_symbol": "SCONV.BK",
        },
        "boundary_evidence": {
            "predecessor_reference_price": "100",
            "successor_reference_price": "200",
            "mechanical_nav_tolerance_pct": "1.0",
            "suspension_gap_annotation": "WP5 fixture — no suspension",
        },
        "evidence": {
            "reference": "TEST", "source": "unit-test", "captured_at": "2026-06-01T00:00:00Z",
        },
    }

    _tx(
        db, p.id, ws.id, "POSITION_CONVERSION", 228.0,
        _dt(2),  # midnight — required by ck_tx_position_conversion_identity_date
        symbol="PCONV.BK", shares=9.5, price_per_share=228.0 / 9.5,
        fees=1.0, taxes=0.5,
        asset_id=101, conversion_payload=payload,
    )

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    d1_diff = result.diffs[1]

    assert d1_diff.new_values["period_realized_pnl"]      == pytest.approx(1.5, abs=0.01)
    assert d1_diff.new_values["period_fees_paid"]         == pytest.approx(1.5, abs=0.01)
    assert d1_diff.new_values["net_external_cash_flow"]   is None
    assert d1_diff.new_values["imported_asset_value"]     is None
    assert d1_diff.new_values["manual_adjustment_value"]  is None


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP5-A10/A11 — successor identity in generate_daily_snapshot() holdings
#
# Relocated here per the Independent Implementation Review correction
# (docs/implementation/BANPU_WP5_INDEPENDENT_IMPLEMENTATION_REVIEW.md §9/§20
# item 4): this file is on Authorization Record §4.2's allowlist and already
# carries the DB/PortfolioItem/asset_id fixture infrastructure (models.asset,
# _seed, _tx) WP5-A3 established; §4.2 authorizes test FILE paths, not which
# production module an authorized test file may import, so importing
# generate_daily_snapshot from services.portfolio_snapshots here is in scope.
#
# Live inspection (WP5_WORK_PACKAGE_PLAN.md §13) found the holdings-entry
# `asset_id` field already sourced directly from PortfolioItem.asset_id (the
# registry-bound column), never from a cached/display value — no source
# change was required; these are the regression tests §13 requires in that
# case. generate_daily_snapshot()'s own price_override parameter avoids any
# live market-data call.
#
# WP5-A10 correction (Fresh Independent Implementation Re-Review §9/§21):
# the prior A10 test inserted a successor-shaped PortfolioItem directly and
# so began after the very identity fact it was required to prove. The
# corrected test below exercises the real, connected provenance chain —
# registry-minted assets -> execute_position_conversion() (WP4's real
# materialization service, services/portfolio_transactions.py) -> the
# PortfolioItem row that service itself writes -> generate_daily_snapshot()
# -> holdings JSON — and asserts the exact registry-bound successor asset_id
# that chain produces, never a test-supplied one. _mint_and_prepare_registry/
# _a10_conversion_payload mirror the established pattern in the WP4-owned
# tests/test_position_conversion_live.py (not imported from — that file is
# outside the WP5 §4.2 test allowlist; the pattern is replicated here as a
# self-contained fixture using only registry/portfolio_transactions imports,
# the same "authorized file may import any authorized production module"
# principle already used for generate_daily_snapshot above).
# ══════════════════════════════════════════════════════════════════════════════

def _mint_and_prepare_registry(
    db,
    *,
    predecessor_symbol: str = "WP5A10PRED",
    successor_symbol: str = "WP5A10SUCC",
    predecessor_provider_symbol: str = "WP5A10PRED.BK",
    successor_provider_symbol: str = "WP5A10SUCC.BK",
):
    predecessor = registry.mint(
        db,
        AssetClaim(canonical_symbol=predecessor_symbol, asset_type=AssetType.EQUITY,
                   market="TH", exchange="SET", currency="THB"),
        identifiers=[IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, predecessor_provider_symbol, source="test")],
    )
    successor = registry.mint(
        db,
        AssetClaim(canonical_symbol=successor_symbol, asset_type=AssetType.EQUITY,
                   market="TH", exchange="SET", currency="THB"),
    )
    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, successor_provider_symbol, source="test",
    )
    db.commit()
    return predecessor, successor


def _a10_conversion_payload(*, predecessor_asset_id: int, successor_asset_id: int) -> dict:
    return {
        "schema_version": 1,
        "predecessor": {
            "asset_id": predecessor_asset_id, "symbol": "WP5A10PRED.BK",
            "shares_surrendered": "100",
        },
        "successor": {
            "asset_id": successor_asset_id, "symbol": "WP5A10SUCC.BK",
            "provider_symbol": "WP5A10SUCC.BK",
            "shares_entitled": "50", "shares_received": "50",
        },
        "conversion_ratio": "0.5",
        "basis": {"before": "10000", "allocated_to_cash_in_lieu": "0", "carried_to_successor": "10000"},
        "cash_in_lieu": None,
        "dates": {
            "legal_effective_date": "2026-03-02", "valuation_transition_date": "2026-03-02",
            "predecessor_last_price_date": "2026-03-01", "successor_quote_epoch_start_date": "2026-03-02",
        },
        "quote_binding": {
            "provider": "YAHOO",
            "predecessor_provider_symbol": "WP5A10PRED.BK",
            "successor_provider_symbol": "WP5A10SUCC.BK",
        },
        "boundary_evidence": {
            "predecessor_reference_price": "1.00", "successor_reference_price": "1.00",
            "mechanical_nav_tolerance_pct": "1.0",
            "suspension_gap_annotation": "WP5-A10 fixture — no suspension",
        },
        "evidence": {
            "reference": "TEST", "source": "unit-test", "captured_at": "2026-03-02T00:00:00Z",
        },
    }


def test_wp5_a10_holdings_entry_carries_successor_asset_id():
    """WP5-A10, corrected: the full connected provenance chain, not a
    pre-shaped fixture. Would this test still pass if the registry ->
    conversion -> materialized-successor identity chain were broken but a
    successor-shaped PortfolioItem were manually inserted instead? No — this
    test never constructs that PortfolioItem itself; execute_position_
    conversion() is the only writer of the successor row, and the asserted
    asset_id is read back from whatever that service actually persisted, not
    from a value the test chose."""
    # execute_position_conversion() requires an idle Session (no pending
    # transaction); expire_on_commit=False avoids the implicit autobegin a
    # post-commit attribute read (predecessor.id/successor.id below) would
    # otherwise trigger — same setting test_position_conversion_live.py's own
    # db_session fixture uses for the identical reason.
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    db = sessionmaker(bind=engine, expire_on_commit=False)()
    ws, p = _seed(db, cash=1_000.0)

    # 1. Registry-bound predecessor/successor assets — the sole identity
    #    source; asset_id values below are the registry's own, never a
    #    test-invented constant.
    predecessor, successor = _mint_and_prepare_registry(db)

    # 2. Predecessor PortfolioItem, seeded pre-conversion.
    db.add(PortfolioItem(
        workspace_id=ws.id, portfolio_id=p.id, symbol="WP5A10PRED.BK",
        shares=100.0, avg_cost=100.0, asset_id=predecessor.id,
    ))
    db.commit()

    # 3. Execute the real WP4 materialization path — this is the only thing
    #    that writes a successor PortfolioItem row in this test.
    result = execute_position_conversion(
        db, ws_id=ws.id, portfolio_id=p.id,
        conversion_payload=_a10_conversion_payload(
            predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        ),
    )
    assert result["status"] == "applied"

    # 4. Confirm materialization: the row execute_position_conversion() wrote
    #    carries the registry's own successor.id — establishing the fact A10
    #    requires, not assuming it.
    materialized = db.query(PortfolioItem).filter_by(portfolio_id=p.id, asset_id=successor.id).one()
    assert "WP5A10PRED.BK" not in {
        i.symbol for i in db.query(PortfolioItem).filter_by(portfolio_id=p.id).all()
    }

    # 5. Post-boundary snapshot generation — the actual production path,
    #    reading whatever symbol the conversion service itself assigned
    #    (never a symbol the test chose).
    snapshot_result = asyncio.run(generate_daily_snapshot(
        db, portfolio_id=p.id, workspace_id=ws.id, snapshot_date="2026-03-02",
        price_override={materialized.symbol: 210.0},
    ))

    # 6. Holdings JSON must carry the exact registry-bound successor asset_id
    #    that the connected chain produced, never the predecessor's.
    holdings = {h["symbol"]: h for h in snapshot_result["holdings"]}
    assert holdings[materialized.symbol]["asset_id"] == successor.id
    assert predecessor.id not in {h["asset_id"] for h in snapshot_result["holdings"]}


def test_wp5_a11_pre_boundary_predecessor_identity_unaffected():
    """WP5-A11 (frozen requirement, corrected per Independent Implementation
    Review §9/§14 — the prior test exercised an ordinary non-conversion
    holding, not this case): 'a pre-boundary snapshot's holdings entry
    (generated before any conversion existed) is unaffected.' Non-vacuous:
    the ledger already contains a POSITION_CONVERSION transaction dated AFTER
    the snapshot date, and PortfolioItem still reflects the predecessor (WP4's
    execute_position_conversion() has not retired it yet at this point in
    time) — proving the holdings-entry construction is driven by current
    PortfolioItem state, not by the mere existence of a future conversion
    transaction in the ledger."""
    db = make_session()
    ws, p = _seed(db, cash=1_000.0)
    db.add(PortfolioItem(
        workspace_id=ws.id, portfolio_id=p.id, symbol="WP5PRED.BK",
        shares=100.0, avg_cost=100.0, asset_id=5001,
    ))
    db.commit()

    _tx(
        db, p.id, ws.id, "INITIAL_POSITION", 0.0, _dt(20),
        symbol="WP5PRED.BK", shares=100.0, price_per_share=100.0, asset_id=5001,
    )

    payload = {
        "schema_version": 1,
        "predecessor": {"asset_id": 5001, "symbol": "WP5PRED.BK", "shares_surrendered": "100"},
        "successor": {
            "asset_id": 5002, "symbol": "WP5SUCC.BK", "provider_symbol": "WP5SUCC.BK",
            "shares_entitled": "50", "shares_received": "50",
        },
        "conversion_ratio": "0.5",
        "basis": {"before": "10000", "allocated_to_cash_in_lieu": "0", "carried_to_successor": "10000"},
        "cash_in_lieu": None,
        "dates": {
            "legal_effective_date": _d(5), "valuation_transition_date": _d(5),
            "predecessor_last_price_date": _d(6), "successor_quote_epoch_start_date": _d(5),
        },
        "quote_binding": {
            "provider": "test-provider",
            "predecessor_provider_symbol": "WP5PRED.BK",
            "successor_provider_symbol": "WP5SUCC.BK",
        },
        "boundary_evidence": {
            "predecessor_reference_price": "1.00",
            "successor_reference_price": "1.00",
            "mechanical_nav_tolerance_pct": "1.0",
            "suspension_gap_annotation": "WP5-A11 fixture — no suspension",
        },
        "evidence": {
            "reference": "TEST", "source": "unit-test", "captured_at": f"{_d(5)}T00:00:00Z",
        },
    }
    _tx(
        db, p.id, ws.id, "POSITION_CONVERSION", 10_000.0, _dt(5),   # AFTER the snapshot date below
        symbol="WP5PRED.BK", shares=50.0, price_per_share=200.0,
        fees=0.0, taxes=0.0, asset_id=5001, conversion_payload=payload,
    )

    result = asyncio.run(generate_daily_snapshot(
        db, portfolio_id=p.id, workspace_id=ws.id, snapshot_date=_d(10),   # BEFORE the conversion
        price_override={"WP5PRED.BK": 105.0},
    ))

    holdings = {h["symbol"]: h for h in result["holdings"]}
    assert "WP5PRED.BK" in holdings
    assert holdings["WP5PRED.BK"]["asset_id"] == 5001                # predecessor's own id, unchanged
    assert 5002 not in {h["asset_id"] for h in result["holdings"]}   # successor id never leaks early


# ── Test 8: DIVIDEND creates period_dividend_income ──────────────────────────

def test_dividend_creates_period_dividend_income():
    """A DIVIDEND transaction must set period_dividend_income."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0)
    _snap(db, p.id, ws.id, d1, 100_500.0)

    _tx(db, p.id, ws.id, "DIVIDEND", 500.0, _dt(2) + timedelta(hours=14))

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    d1_diff = result.diffs[1]

    assert d1_diff.new_values["period_dividend_income"] == pytest.approx(500.0, abs=0.01)
    # Dividend is market income — NOT stripped from returns
    assert d1_diff.new_values["investment_return_pct"] == pytest.approx(0.5, abs=1e-3)


# ── Test 9: BUY fees accumulate in period_fees_paid ──────────────────────────

def test_buy_fees_accumulate_in_period_fees_paid():
    """BUY transaction fees + taxes must be included in period_fees_paid."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0)
    _snap(db, p.id, ws.id, d1,  99_800.0)

    _tx(
        db, p.id, ws.id, "BUY", 10_000.0,
        _dt(2) + timedelta(hours=10),
        symbol="KBANK.BK", shares=100.0, price_per_share=100.0,
        fees=150.0, taxes=10.5,
    )

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    d1_diff = result.diffs[1]

    assert d1_diff.new_values["period_fees_paid"] == pytest.approx(160.5, abs=0.01)


# ── Test 10: Portfolio-2 scenario — bookkeeping on baseline day excluded ───────

def test_bookkeeping_transactions_on_baseline_day_excluded_from_next_window():
    """INITIAL_CASH and INITIAL_POSITION created on Day-0 (baseline day) must NOT
    appear in the return computation for Day-1 because:
      - window is  created_at >= end_of_Day-0
      - Day-0 transactions have created_at  < end_of_Day-0  → excluded

    This matches the Portfolio-2 forensic finding: setup transactions were
    created at the same time as the baseline snapshot, so they should already
    be captured in the baseline NAV and must not distort the next period's
    return.
    """
    db = make_session()
    ws, p = _seed(db)

    baseline_date = _d(3)
    next_date     = _d(2)

    # Baseline NAV includes INITIAL_CASH + INITIAL_POSITION injected on Day-0
    baseline_nav = 100_000.0 + 20_000.0  # 120,000

    _snap(db, p.id, ws.id, baseline_date, baseline_nav, cash_balance=100_000.0)

    # Pure market gain the next day: NAV rises by 1,200 (1 %).
    # Cash is unchanged (no cash transactions on next_date) → realistic cash_balance.
    _snap(db, p.id, ws.id, next_date, baseline_nav + 1_200.0, cash_balance=100_000.0)

    # Bookkeeping transactions created on Day-0 (baseline day)
    _tx(db, p.id, ws.id, "INITIAL_CASH",     100_000.0, _dt(3) + timedelta(hours=9))
    _tx(
        db, p.id, ws.id, "INITIAL_POSITION",  20_000.0, _dt(3) + timedelta(hours=9),
        symbol="AOT.BK", shares=200.0, price_per_share=100.0,
    )

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    baseline_diff = result.diffs[0]
    next_diff     = result.diffs[1]

    # Baseline: all None
    for f in _RETURN_FIELDS:
        assert baseline_diff.new_values[f] is None, f"baseline {f} should be None"

    # Next day: bookkeeping transactions are NOT in the window → not stripped
    # Return = 1,200 / 121,200 ≈ 0.9901 %
    expected_return = round(1_200.0 / baseline_nav * 100, 4)
    assert next_diff.new_values["investment_return_pct"]  == pytest.approx(expected_return, abs=1e-3)
    assert next_diff.new_values["net_external_cash_flow"] is None
    assert next_diff.new_values["imported_asset_value"]   is None


# ── Test 11: Portfolio-4 repaired baseline scenario ───────────────────────────

def test_portfolio4_repaired_baseline_two_snapshot_chain():
    """After snapshot_repair.py has fixed the NAV values, the return engine
    correctly computes performance from the repaired chain.

    Scenario:
      Snap-0 (baseline): NAV = 200,000  → all return fields = None
      Snap-1 (day+1):    NAV = 202,000  → return = +1.0%, no cash events
    """
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(5), _d(4)
    _snap(db, p.id, ws.id, d0, 200_000.0)
    _snap(db, p.id, ws.id, d1, 202_000.0)

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)

    assert result.diffs[0].new_values["investment_return_pct"] is None
    assert result.diffs[1].new_values["investment_return_pct"] == pytest.approx(1.0, abs=1e-4)
    assert result.diffs[1].new_values["net_external_cash_flow"] is None
    assert result.diffs[1].new_values["investment_return_amount"] == pytest.approx(2_000.0, abs=0.01)


# ── Test 12: Dry run does not write to DB ─────────────────────────────────────

def test_dry_run_does_not_write():
    """dry_run=True must leave every snapshot column unchanged."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0)
    s1 = _snap(db, p.id, ws.id, d1, 110_000.0, investment_return_pct=99.0)

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)
    assert result.snapshots_changed == 1

    # DB must not have been touched
    db.expire_all()
    unchanged = db.query(PortfolioSnapshot).filter_by(id=s1.id).first()
    assert unchanged.investment_return_pct == pytest.approx(99.0, abs=0.001)


# ── Test 13: No-op when fields are already correct ────────────────────────────

def test_noop_when_fields_already_correct():
    """A snapshot with the correct values already stored should be unchanged=True."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0)

    # Pre-seed correct values
    expected_return_pct = round(5_000.0 / 100_000.0 * 100, 4)
    _snap(
        db, p.id, ws.id, d1, 105_000.0,
        investment_return_pct    = expected_return_pct,
        daily_return_pct         = expected_return_pct,
        investment_return_amount = 5_000.0,
        # All other fields None (no transactions)
    )

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id)
    # baseline (d0) and d1 are both unchanged — 2 total
    assert result.snapshots_unchanged == 2
    assert result.snapshots_changed   == 0


# ── Test 14: Idempotency — running twice is identical ────────────────────────

def test_idempotency():
    """Running the recovery twice produces the same result as running it once."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1, d2 = _d(5), _d(4), _d(3)
    _snap(db, p.id, ws.id, d0, 100_000.0, cash_balance=100_000.0)
    _snap(db, p.id, ws.id, d1, 122_000.0, cash_balance=122_000.0)
    # d2: no cash transactions → cash unchanged from d1
    _snap(db, p.id, ws.id, d2, 124_000.0, cash_balance=122_000.0)

    _tx(db, p.id, ws.id, "DEPOSIT", 22_000.0, _dt(4) + timedelta(hours=10))

    # First run — writes values
    r1 = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=False)
    db.commit()

    # Second run — should find everything already correct
    r2 = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=False)
    db.commit()

    assert r2.snapshots_changed   == 0
    assert r2.snapshots_unchanged == r1.snapshots_scanned


# ── Test 15: Rollback leaves DB unchanged on error ───────────────────────────

def test_rollback_on_failure():
    """When the caller rolls back after an error, no partial writes persist."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0)
    s1 = _snap(db, p.id, ws.id, d1, 108_000.0, investment_return_pct=0.0)

    # Accumulate changes without committing
    recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=False)

    # Simulate a failure — roll back instead of commit
    db.rollback()

    db.expire_all()
    unchanged = db.query(PortfolioSnapshot).filter_by(id=s1.id).first()
    # investment_return_pct should still be the original 0.0, not the newly computed 8.0
    assert unchanged.investment_return_pct == pytest.approx(0.0, abs=0.001)


# ── Test 16: recover_all handles multiple portfolios independently ─────────────

def test_recover_all_multiple_portfolios():
    """recover_all_snapshot_returns processes each portfolio separately."""
    db = make_session()
    ws = Workspace(name="WS")
    db.add(ws)
    db.flush()

    pA = Portfolio(workspace_id=ws.id, name="Alpha", cash_balance=0.0)
    pB = Portfolio(workspace_id=ws.id, name="Beta",  cash_balance=0.0)
    db.add_all([pA, pB])
    db.commit()

    d0, d1 = _d(3), _d(2)

    _snap(db, pA.id, ws.id, d0, 100_000.0)
    _snap(db, pA.id, ws.id, d1, 105_000.0)

    _snap(db, pB.id, ws.id, d0, 200_000.0)
    _snap(db, pB.id, ws.id, d1, 190_000.0)

    results = recover_all_snapshot_returns(db, ws.id, dry_run=True)

    assert len(results) == 2
    assert results[0].portfolio_id == pA.id
    assert results[1].portfolio_id == pB.id

    alpha_d1 = results[0].diffs[1]
    beta_d1  = results[1].diffs[1]

    assert alpha_d1.new_values["investment_return_pct"] == pytest.approx(5.0, abs=1e-4)
    assert beta_d1.new_values["investment_return_pct"]  == pytest.approx(-5.0, abs=1e-4)


# ── Test 17: Unknown portfolio returns error result ────────────────────────────

def test_unknown_portfolio_returns_error():
    """A non-existent portfolio_id must return a result with an error message."""
    db = make_session()
    ws, _ = _seed(db)

    result = recover_portfolio_snapshot_returns(db, portfolio_id=99999, workspace_id=ws.id)

    assert result.error is not None
    assert "99999" in result.error
    assert result.snapshots_scanned == 0


# ── Test 18: Empty portfolio scans 0 snapshots without error ─────────────────

def test_empty_portfolio_scans_zero_snapshots():
    """A portfolio with no snapshots must produce a clean result with 0 scanned."""
    db = make_session()
    ws, p = _seed(db)

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id)

    assert result.error is None
    assert result.snapshots_scanned   == 0
    assert result.snapshots_changed   == 0
    assert result.snapshots_unchanged == 0
    assert result.diffs               == []


# ── Test 19: Multi-snapshot chain — each window uses correct boundaries ────────

def test_multi_snapshot_chain_correct_windows():
    """In a 4-snapshot chain, each period's return uses only transactions in
    that specific window, not those from adjacent periods."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1, d2, d3 = _d(6), _d(5), _d(4), _d(3)
    # d0: all equity, no cash
    _snap(db, p.id, ws.id, d0, 100_000.0, cash_balance=0.0)
    # d1: DEPOSIT of 22k raised cash from 0 → 22,000; equity unchanged → total 122,000
    _snap(db, p.id, ws.id, d1, 122_000.0, cash_balance=22_000.0)
    # d2 and d3: no cash transactions → cash stays at 22,000
    _snap(db, p.id, ws.id, d2, 122_500.0, cash_balance=22_000.0)
    _snap(db, p.id, ws.id, d3, 119_500.0, cash_balance=22_000.0)

    # DEPOSIT falls between d0 and d1
    _tx(db, p.id, ws.id, "DEPOSIT", 22_000.0, _dt(5) + timedelta(hours=10))

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)

    # d0: baseline → None
    assert result.diffs[0].new_values["investment_return_pct"] is None

    # d1: DEPOSIT stripped → 0% return
    assert result.diffs[1].new_values["investment_return_pct"] == pytest.approx(0.0, abs=1e-4)
    assert result.diffs[1].new_values["net_external_cash_flow"] == pytest.approx(22_000.0, abs=0.01)

    # d2: no events → 500/122,000 ≈ 0.4098%
    assert result.diffs[2].new_values["investment_return_pct"] == pytest.approx(500.0 / 122_000.0 * 100, abs=1e-3)
    assert result.diffs[2].new_values["net_external_cash_flow"] is None

    # d3: no events → -3,000/122,500 ≈ -2.4490%
    assert result.diffs[3].new_values["investment_return_pct"] == pytest.approx(-3_000.0 / 122_500.0 * 100, abs=1e-3)


# ── Test 20: Writes are persisted when not dry_run ────────────────────────────

def test_writes_persisted_to_db_on_commit():
    """After commit, the new return fields must be readable from the database."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0)
    s1 = _snap(db, p.id, ws.id, d1, 112_000.0)

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=False)
    db.commit()

    assert result.snapshots_changed == 1

    db.expire_all()
    updated = db.query(PortfolioSnapshot).filter_by(id=s1.id).first()
    expected_pct = round(12_000.0 / 100_000.0 * 100, 4)
    assert updated.investment_return_pct    == pytest.approx(expected_pct, abs=1e-4)
    assert updated.daily_return_pct         == pytest.approx(expected_pct, abs=1e-4)
    assert updated.investment_return_amount == pytest.approx(12_000.0, abs=0.01)


# ── Test 21: NAV fields are never modified ────────────────────────────────────

def test_nav_fields_never_modified():
    """total_value, cash_balance, total_invested, unrealized_pnl, holdings_json
    must be identical before and after recovery."""
    db = make_session()
    ws, p = _seed(db)

    d0, d1 = _d(3), _d(2)
    _snap(db, p.id, ws.id, d0, 100_000.0, cash_balance=10_000.0)

    s1 = PortfolioSnapshot(
        workspace_id      = ws.id,
        portfolio_id      = p.id,
        snapshot_date     = d1,
        total_value       = 105_000.0,
        cash_balance      = 15_000.0,
        total_invested    = 90_000.0,
        unrealized_pnl    = 5_000.0,
        unrealized_pnl_pct = 5.88,
        realized_pnl      = 1_234.5,
        holdings_json     = json.dumps([{"symbol": "AOT.BK", "shares": 100}]),
        holdings_count    = 1,
    )
    db.add(s1)
    db.commit()

    before = {
        "total_value": s1.total_value,
        "cash_balance": s1.cash_balance,
        "total_invested": s1.total_invested,
        "unrealized_pnl": s1.unrealized_pnl,
        "unrealized_pnl_pct": s1.unrealized_pnl_pct,
        "realized_pnl": s1.realized_pnl,
        "holdings_json": s1.holdings_json,
        "holdings_count": s1.holdings_count,
    }

    recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=False)
    db.commit()

    db.expire_all()
    after_snap = db.query(PortfolioSnapshot).filter_by(id=s1.id).first()
    for col, val in before.items():
        assert getattr(after_snap, col) == val, f"Column {col} was modified"


# ── Test 22: Forensic scenario — phantom DEPOSIT + INITIAL_POSITION ────────────

def test_phantom_deposit_and_initial_position_surface_as_anomalous_return():
    """Ledger-recorded-but-not-reflected-in-state entries must NOT be silently
    absorbed by the metrics engine — they must surface as an anomalous return,
    per ADR-002 ("Portfolio Metrics never compensate for ledger corruption;
    validation belongs to Ledger Validator; repair belongs to Ledger Repair").

    Mirrors the real-data forensic investigation for Snapshot 39 (portfolio 2,
    2026-05-25):
      • prev_snap: SCB.BK already held with 2300 shares, cash=23,071.69
      • curr_snap: same 2300 SCB.BK shares, cash=23,071.69 (unchanged)
      • In-window transactions:
          tx#26 — DEPOSIT 22,071.69: recorded in DB, but cash_balance unchanged
          tx#28 — INITIAL_POSITION SCB.BK 1000 shares: recorded in DB, but
                  SCB.BK was already in prev holdings with 2300 ≥ 1000 shares

    Before this engine was migrated to the shared portfolio_metrics module, it
    used a cash-balance-delta net_ecf formula plus a snapshot-level dedup
    heuristic, both of which silently absorbed these phantom ledger entries and
    recovered the "clean" pure market gain (+0.7275%). Architecture review
    (docs/PORTFOLIO_CALCULATION_RULES.md Section 4, Q1-Q3) found that masking
    is the wrong failure mode for an accounting system: a DEPOSIT recorded with
    no real cash movement, or a duplicate INITIAL_POSITION, is a ledger-quality
    defect (CASH_MISMATCH-adjacent) that ledger_validator.py / ledger_repair_plan.py
    should catch and fix BEFORE any snapshot engine runs — not something the
    return formula should paper over. The now-canonical ledger-derived formula
    (Implementation A, ADR-002) treats both ledger entries at face value, which
    correctly produces a large, obviously-wrong return — failing loud instead
    of silently laundering the discrepancy into a "clean" number.
    """
    db = make_session()
    ws, p = _seed(db)

    prev_nav  = 836_436.69
    prev_cash = 23_071.69
    prev_holdings_json = json.dumps([
        {
            "symbol": "SCB.BK", "shares": 2300.0, "avg_cost": 134.2033,
            "current_price": 135.0, "market_value": 310_500.0,
            "unrealized_pnl": 1840.0, "sector": "Finance",
        },
        {
            "symbol": "AOT.BK", "shares": 5000.0, "avg_cost": 56.09,
            "current_price": 52.75, "market_value": 263_750.0,
            "unrealized_pnl": -16_700.0, "sector": "Transport",
        },
    ])
    d_prev = _d(4)
    s0 = PortfolioSnapshot(
        workspace_id=ws.id, portfolio_id=p.id, snapshot_date=d_prev,
        total_value=prev_nav, cash_balance=prev_cash,
        holdings_json=prev_holdings_json, holdings_count=2,
    )
    db.add(s0)
    db.commit()

    # Pure market gain between periods; cash and share counts unchanged.
    market_gain = 6_085.0
    curr_nav    = prev_nav + market_gain
    curr_cash   = prev_cash  # phantom DEPOSIT did not change cash

    d_curr = _d(1)
    s1 = PortfolioSnapshot(
        workspace_id=ws.id, portfolio_id=p.id, snapshot_date=d_curr,
        total_value=curr_nav, cash_balance=curr_cash,
        holdings_count=2,
    )
    db.add(s1)
    db.commit()

    # Phantom DEPOSIT — Transaction record exists but cash_balance never updated.
    _tx(db, p.id, ws.id, "DEPOSIT", 22_071.69,
        _dt(1) + timedelta(hours=5))

    # Phantom INITIAL_POSITION — SCB.BK already held (2300 shares ≥ 1000 in tx).
    _tx(db, p.id, ws.id, "INITIAL_POSITION", 144_646.69,
        _dt(1) + timedelta(hours=5, minutes=5),
        symbol="SCB.BK", shares=1000.0, price_per_share=144.64669)

    result = recover_portfolio_snapshot_returns(db, p.id, ws.id, dry_run=True)

    assert result.snapshots_scanned == 2
    diff = result.diffs[1]  # curr snapshot

    # Ledger-derived net_ecf takes the recorded DEPOSIT at face value (22,071.69),
    # and imported_asset_value takes the recorded INITIAL_POSITION at face value
    # (1000 × 144.64669 = 144,646.69) since there is no dedup heuristic anymore.
    deposit_amount = 22_071.69
    import_value   = 1000.0 * 144.64669
    pure_gain = (curr_nav - prev_nav) - deposit_amount - import_value
    expected_return = round(pure_gain / prev_nav * 100, 4)  # ≈ -19.2045 %

    assert diff.new_values["investment_return_pct"] == pytest.approx(expected_return, abs=1e-3), (
        f"Expected {expected_return}% (ledger-derived, fails loud) but got "
        f"{diff.new_values['investment_return_pct']}%"
    )
    assert diff.new_values["net_external_cash_flow"] == pytest.approx(deposit_amount, abs=0.01), \
        "Ledger-derived net_ecf takes the recorded DEPOSIT at face value"
    assert diff.new_values["imported_asset_value"] == pytest.approx(import_value, abs=0.01), \
        "No dedup heuristic — recorded INITIAL_POSITION is taken at face value"
    assert diff.new_values["investment_return_amount"] == pytest.approx(pure_gain, abs=0.01)
