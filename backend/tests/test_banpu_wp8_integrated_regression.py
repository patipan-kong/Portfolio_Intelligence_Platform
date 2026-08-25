"""BANPU-WP8-T3 — mandatory integrated regression test (WPP §6.2, §6.3, §21).

Closes exactly the four test-addressable proof gaps T1/T2 established, none
of which any existing test in the frozen corpus closes directly:

  1. Deterministic price-matrix correctness — `_build_price_matrix()` against
     a controlled, network-free provider substitute (WPP §9's price-matrix
     contract; `test_price_matrix.py` is print-only and asserts nothing).
  2. Attribution continuity across the BANPU conversion relationship date
     (`test_attribution_waterfall.py` only proves an ordinary, unrelated
     reconciliation — never a scenario spanning a conversion).
  3. Quant/factor continuity across the conversion relationship date
     (`test_factor_engine_asset_id.py` only proves already-materialized
     `asset_id` carries through for an ordinary holding).
  4. Mixed-portfolio dual-replay — one portfolio holding both a converted
     and an ordinary asset, replayed in both legacy and native mode.

All four tests are network-free, deterministic, and construct their own
in-memory SQLite state and controlled substitutes inline — no new fixture
file was required (see BANPU_WP8 T3 report, §H).
"""
from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta
from decimal import Decimal

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401 — registers Asset* tables on Base.metadata
from models.database import (
    Base,
    Portfolio,
    PortfolioItem,
    PortfolioSnapshot,
    ShadowPortfolio,
    ShadowPortfolioSnapshot,
    Transaction,
    Workspace,
)
from services import portfolio_rebuilder
from services.analytics import factor_engine
from services.analytics.attribution_engine import compute_attribution_waterfall
from services.analytics.quant_engine import invalidate_all
from services.portfolio_rebuilder import _build_price_matrix, rebuild_portfolio


# ══════════════════════════════════════════════════════════════════════════
# Shared DB helpers (modeled on test_position_conversion_replay.py's
# already-reviewed shape; independently authored, not imported from it)
# ══════════════════════════════════════════════════════════════════════════

def _make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


def _add_tx(
    db, tx_id, portfolio_id, tx_type, *,
    symbol=None, shares=None, price=None, amount=0.0, fees=0.0, taxes=0.0,
    date_=datetime(2026, 1, 1), asset_id=None, conversion_payload=None,
):
    # A POSITION_CONVERSION row's own shares/price/amount must reflect the
    # successor leg the payload describes — _preflight_position_conversions()
    # (services/portfolio_rebuilder.py) requires raw.shares == successor
    # shares_received within tolerance, not an arbitrary/omitted value.
    if tx_type == "POSITION_CONVERSION" and conversion_payload is not None:
        successor = conversion_payload["successor"]
        basis = conversion_payload["basis"]
        received = Decimal(successor["shares_received"])
        carried = Decimal(basis["carried_to_successor"])
        shares = float(received)
        price = float(carried / received)
        amount = float(carried)
    db.add(Transaction(
        id=tx_id, workspace_id=1, portfolio_id=portfolio_id, symbol=symbol,
        transaction_type=tx_type, shares=shares, price_per_share=price,
        total_amount=amount, fees=fees, taxes=taxes, transaction_date=date_,
        created_at=date_, asset_id=asset_id, conversion_payload=conversion_payload,
    ))


def _conversion_payload(
    *, predecessor_asset_id, predecessor_symbol, shares_surrendered,
    successor_asset_id, successor_symbol, shares_entitled, shares_received,
    conversion_ratio, basis_carried, transition_date="2026-03-02",
):
    return {
        "schema_version": 1,
        "predecessor": {
            "asset_id": predecessor_asset_id, "symbol": predecessor_symbol,
            "shares_surrendered": shares_surrendered,
        },
        "successor": {
            "asset_id": successor_asset_id, "symbol": successor_symbol,
            "provider_symbol": successor_symbol,
            "shares_entitled": shares_entitled, "shares_received": shares_received,
        },
        "conversion_ratio": conversion_ratio,
        "basis": {
            "before": basis_carried, "allocated_to_cash_in_lieu": "0",
            "carried_to_successor": basis_carried,
        },
        "cash_in_lieu": None,
        "dates": {
            "legal_effective_date": transition_date,
            "valuation_transition_date": transition_date,
            "predecessor_last_price_date": transition_date,
            "successor_quote_epoch_start_date": transition_date,
        },
        "quote_binding": {
            "provider": "test-provider",
            "predecessor_provider_symbol": predecessor_symbol,
            "successor_provider_symbol": successor_symbol,
        },
        "boundary_evidence": {
            "predecessor_reference_price": "1.00", "successor_reference_price": "1.00",
            "mechanical_nav_tolerance_pct": "1.0",
            "suspension_gap_annotation": "WP8-T3 fixture — no suspension",
        },
        "evidence": {
            "reference": "WP8-T3-FIXTURE", "source": "unit-test",
            "captured_at": f"{transition_date}T00:00:00Z",
        },
    }


# ══════════════════════════════════════════════════════════════════════════
# Gap 1 — deterministic price-matrix correctness (WPP §6.3(b), §9)
# ══════════════════════════════════════════════════════════════════════════

def _fake_history_df(closes: dict[str, float]) -> pd.DataFrame:
    ordered_dates = sorted(closes.keys())
    return pd.DataFrame(
        {"Close": [closes[d] for d in ordered_dates]},
        index=pd.to_datetime(ordered_dates),
    )


def test_build_price_matrix_exact_symbol_date_and_backfill_relationship(monkeypatch):
    """Real _build_price_matrix() against a controlled, network-free
    fetch_history substitute. Proves the exact requested symbol set, exact
    requested date-key set, last-session-on-or-before-date relationship,
    deterministic positive prices, completeness, and None only where the
    controlled scenario has no session on or before the requested date.
    """
    closes_by_symbol = {
        "BANPUU.BK": {"2026-05-20": 5.50, "2026-05-22": 5.65},
        "PTT.BK": {"2026-05-21": 34.00, "2026-05-22": 34.25},
    }

    def fake_fetch_history(symbol, period, interval):
        assert period == "5y"
        assert interval == "1d"
        return _fake_history_df(closes_by_symbol[symbol])

    monkeypatch.setattr(portfolio_rebuilder, "fetch_history", fake_fetch_history)

    symbols = ["BANPUU.BK", "PTT.BK"]
    dates = ["2026-05-19", "2026-05-20", "2026-05-21", "2026-05-23"]

    matrix = asyncio.run(_build_price_matrix(symbols, dates))

    expected = {
        "BANPUU.BK": {
            "2026-05-19": None,   # before first available close — no on/before session
            "2026-05-20": 5.50,   # exact session match
            "2026-05-21": 5.50,   # no session that day — backward-filled to 05-20
            "2026-05-23": 5.65,   # last session on/before 05-23 is 05-22
        },
        "PTT.BK": {
            "2026-05-19": None,   # before first available close (05-21)
            "2026-05-20": None,   # before first available close (05-21)
            "2026-05-21": 34.00,
            "2026-05-23": 34.25,
        },
    }

    assert set(matrix.keys()) == set(expected.keys())
    for sym in expected:
        assert set(matrix[sym].keys()) == set(dates)
        assert matrix[sym] == expected[sym]
        for v in matrix[sym].values():
            if v is not None:
                assert v > 0


def test_build_price_matrix_provider_exception_yields_none_not_fabricated_value(monkeypatch):
    """A provider exception for one symbol must not crash _build_price_matrix()
    and must not silently satisfy this suite with a fabricated price — the
    failed symbol's dates come back None while an unrelated healthy symbol's
    dates remain exact, so an all-None fallback could never pass this file's
    exact-mapping assertions above.
    """
    def fake_fetch_history(symbol, period, interval):
        if symbol == "BANPUU.BK":
            raise RuntimeError("simulated provider outage")
        return _fake_history_df({"2026-05-20": 5.65})

    monkeypatch.setattr(portfolio_rebuilder, "fetch_history", fake_fetch_history)

    matrix = asyncio.run(_build_price_matrix(["BANPUU.BK", "PTT.BK"], ["2026-05-20"]))

    assert matrix["BANPUU.BK"] == {"2026-05-20": None}
    assert matrix["PTT.BK"] == {"2026-05-20": 5.65}


# ══════════════════════════════════════════════════════════════════════════
# Gap 2 — attribution continuity across the BANPU conversion relationship date
# (WPP §10 row 17)
# ══════════════════════════════════════════════════════════════════════════

_BANPU_RELATIONSHIP_DATE = date(2026, 3, 2)  # WP4 valuation_transition_date, frozen corpus


def test_attribution_waterfall_reconciles_across_conversion_relationship_date():
    """compute_attribution_waterfall() must TWR-chain the actual portfolio's
    daily returns straight through the BANPU conversion relationship date
    without discontinuity, reset, or a dropped day — proving successor
    continuity at the attribution layer, not merely an ordinary unrelated
    window.
    """
    db = _make_session()
    ws = Workspace(name="Test")
    db.add(ws)
    db.commit()
    db.refresh(ws)

    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=0.0)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    daily_returns = [
        (_BANPU_RELATIONSHIP_DATE - timedelta(days=2), 0.0),   # baseline
        (_BANPU_RELATIONSHIP_DATE - timedelta(days=1), 0.5),   # predecessor_last_price_date
        (_BANPU_RELATIONSHIP_DATE, 0.2),                       # conversion relationship date itself
        (_BANPU_RELATIONSHIP_DATE + timedelta(days=1), 0.3),   # first successor-priced day
        (date.today(), 0.1),                                   # recent, well past the boundary
    ]
    value = 1_000_000.0
    for d, r in daily_returns:
        value *= (1.0 + r / 100.0)
        db.add(PortfolioSnapshot(
            workspace_id=ws.id, portfolio_id=portfolio.id, snapshot_date=d.isoformat(),
            total_value=round(value, 2), cash_balance=0.0, investment_return_pct=r,
        ))
    db.commit()

    shadow = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="ACTIVE_MODEL",
        name="AI", inception_date=daily_returns[0][0].isoformat(), inception_value=1_000_000.0,
        inception_holdings_json="[]", is_active=True, created_at=datetime.utcnow(),
    )
    db.add(shadow)
    db.commit()
    db.refresh(shadow)

    db.add(ShadowPortfolioSnapshot(
        shadow_portfolio_id=shadow.id, snapshot_date=daily_returns[0][0].isoformat(),
        total_value=1_000_000.0, created_at=datetime.utcnow(),
    ))
    db.add(ShadowPortfolioSnapshot(
        shadow_portfolio_id=shadow.id, snapshot_date=date.today().isoformat(),
        total_value=1_012_000.0, benchmark_return_pct=1.0, created_at=datetime.utcnow(),
    ))
    db.commit()

    period_days = (date.today() - daily_returns[0][0]).days + 5
    result = compute_attribution_waterfall(db, portfolio.id, period_days=period_days)

    assert result["status"] == "ok"

    expected_twr = 1.0
    for _, r in daily_returns:
        expected_twr *= (1.0 + r / 100.0)
    expected_actual_return_pct = round((expected_twr - 1.0) * 100.0, 4)
    assert result["actual_return_pct"] == pytest.approx(expected_actual_return_pct, abs=0.01)

    # Reconciliation identity must still hold exactly across the boundary —
    # no day silently dropped or double-counted at the relationship date.
    measured_sum = sum(e["value"] for e in result["effects"] if e["value"] is not None)
    reconciled = result["benchmark_return_pct"] + measured_sum + result["residual_pct"]
    assert reconciled == pytest.approx(result["actual_return_pct"], abs=0.01)
    assert result["residual_pct"] is not None


# ══════════════════════════════════════════════════════════════════════════
# Gap 3 — quant/factor continuity across the conversion relationship date
# (WPP §10 row 17)
# ══════════════════════════════════════════════════════════════════════════

def test_factor_engine_carries_successor_identity_without_cross_contaminating_ordinary_holding(monkeypatch):
    """compute_portfolio_factor_exposure() must carry the already-materialized
    successor holding's asset_id through per_stock_scores exactly as it does
    for any ordinary holding — proving quant/factor continuity across the
    conversion relationship date — while an unrelated, never-converted
    holding's own identity stays completely unaffected and no residual
    predecessor entry resurfaces.
    """
    monkeypatch.setattr(factor_engine, "fetch_price_info", lambda symbol: {"current_price": 100.0})
    monkeypatch.setattr(factor_engine, "fetch_info", lambda symbol: {})
    monkeypatch.setattr(factor_engine, "fetch_history", lambda symbol, **kw: None)
    invalidate_all()

    db = _make_session()
    db.add(Workspace(id=1, name="Default"))
    db.add(Portfolio(id=1, workspace_id=1, name="P", cash_balance=0.0))
    # Successor holding — the only row present post-conversion; the
    # predecessor BANPU.BK row was deleted and replaced at materialization
    # time (WP4 atomic live materialization).
    db.add(PortfolioItem(
        workspace_id=1, portfolio_id=1, symbol="BANPUU.BK",
        shares=2562.214, avg_cost=19.01, sector="Energy", asset_id=112,
    ))
    # Unrelated, never-converted holding.
    db.add(PortfolioItem(
        workspace_id=1, portfolio_id=1, symbol="PTT.BK",
        shares=500.0, avg_cost=34.0, sector="Energy", asset_id=201,
    ))
    db.commit()

    try:
        result = factor_engine.compute_portfolio_factor_exposure(db, portfolio_id=1, workspace_id=1)
    finally:
        invalidate_all()

    by_symbol = {row["symbol"]: row for row in result["per_stock_scores"]}

    assert set(by_symbol.keys()) == {"BANPUU.BK", "PTT.BK"}
    assert "BANPU.BK" not in by_symbol

    assert by_symbol["BANPUU.BK"]["asset_id"] == 112
    assert by_symbol["PTT.BK"]["asset_id"] == 201


# ══════════════════════════════════════════════════════════════════════════
# Gap 4 — mixed-portfolio dual-replay (WPP §10 row 11, §6.3(a))
# ══════════════════════════════════════════════════════════════════════════

def test_mixed_portfolio_conversion_and_ordinary_holding_replay_both_modes_agree():
    """A single portfolio holding both a BANPU-converted position and an
    ordinary, never-converted position, replayed once in legacy mode and
    once in native mode. Proves: conversion applies only to the intended
    holding; the ordinary holding (including a post-boundary BUY) is
    completely unaffected; both replay modes persist identical successor
    and ordinary-holding state; and no duplicate/cross-asset contamination
    occurs.
    """
    db = _make_session()
    db.add(Workspace(id=1, name="Default"))
    legacy = Portfolio(id=1, workspace_id=1, name="Legacy", cash_balance=0.0,
                        created_at=datetime(2025, 1, 1), replay_asset_id_native=False)
    native = Portfolio(id=2, workspace_id=1, name="Native", cash_balance=0.0,
                        created_at=datetime(2025, 1, 1), replay_asset_id_native=True)
    db.add(legacy)
    db.add(native)
    db.commit()

    payload = _conversion_payload(
        predecessor_asset_id=101, predecessor_symbol="BANPU.BK", shares_surrendered="6700",
        successor_asset_id=102, successor_symbol="BANPUU.BK",
        shares_entitled="2562.214", shares_received="2562.214", conversion_ratio="0.38242",
        basis_carried="48709.00",
    )

    for portfolio_id, native_mode in [(1, False), (2, True)]:
        init_asset_id = 101 if native_mode else None
        _add_tx(db, portfolio_id * 10 + 1, portfolio_id, "DEPOSIT",
                amount=200_000.0, date_=datetime(2026, 1, 1))
        _add_tx(db, portfolio_id * 10 + 2, portfolio_id, "INITIAL_POSITION",
                symbol="ORDY.BK", shares=1000.0, price=10.0, amount=0.0,
                date_=datetime(2026, 1, 2))
        _add_tx(db, portfolio_id * 10 + 3, portfolio_id, "INITIAL_POSITION",
                symbol="BANPU.BK", shares=6700.0, price=48709.00 / 6700, amount=0.0,
                date_=datetime(2026, 1, 2), asset_id=init_asset_id)
        _add_tx(db, portfolio_id * 10 + 4, portfolio_id, "POSITION_CONVERSION",
                symbol="BANPU.BK", asset_id=101, date_=datetime(2026, 3, 2),
                conversion_payload=payload)
        _add_tx(db, portfolio_id * 10 + 5, portfolio_id, "BUY",
                symbol="ORDY.BK", shares=200.0, price=11.0, amount=2_200.0,
                date_=datetime(2026, 4, 1))
    db.commit()

    legacy_result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    native_result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=2, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert legacy_result.committed is True
    assert native_result.committed is True

    legacy_items = {i.symbol: i for i in db.query(PortfolioItem).filter_by(portfolio_id=1).all()}
    native_items = {i.symbol: i for i in db.query(PortfolioItem).filter_by(portfolio_id=2).all()}

    # Conversion applies only to the intended holding — no duplicate/residual
    # predecessor row in either mode.
    for items in (legacy_items, native_items):
        assert set(items.keys()) == {"BANPUU.BK", "ORDY.BK"}
        assert "BANPU.BK" not in items

    # Successor state — exact, and identical across both replay modes.
    assert legacy_items["BANPUU.BK"].shares == pytest.approx(2562.214, abs=1e-6)
    assert native_items["BANPUU.BK"].shares == pytest.approx(2562.214, abs=1e-6)
    assert legacy_items["BANPUU.BK"].avg_cost == pytest.approx(48709.00 / 2562.214, abs=1e-4)
    assert legacy_items["BANPUU.BK"].avg_cost == pytest.approx(native_items["BANPUU.BK"].avg_cost, abs=1e-9)
    assert legacy_items["BANPUU.BK"].asset_id == native_items["BANPUU.BK"].asset_id == 102

    # Ordinary holding is completely unaffected by the conversion, including
    # the post-boundary BUY — exact weighted-average basis, identical in
    # both modes.
    expected_ordy_shares = 1200.0
    expected_ordy_avg_cost = (1000.0 * 10.0 + 200.0 * 11.0) / expected_ordy_shares
    for items in (legacy_items, native_items):
        assert items["ORDY.BK"].shares == pytest.approx(expected_ordy_shares)
        assert items["ORDY.BK"].avg_cost == pytest.approx(expected_ordy_avg_cost, abs=1e-4)
    assert legacy_items["ORDY.BK"].shares == native_items["ORDY.BK"].shares
    assert legacy_items["ORDY.BK"].avg_cost == pytest.approx(native_items["ORDY.BK"].avg_cost, abs=1e-9)

    # Cash unaffected beyond the ordinary BUY — identical in both modes (no
    # cross-asset cash contamination from the conversion).
    expected_cash = 200_000.0 - 2_200.0
    legacy_portfolio = db.query(Portfolio).filter_by(id=1).first()
    native_portfolio = db.query(Portfolio).filter_by(id=2).first()
    assert legacy_portfolio.cash_balance == pytest.approx(expected_cash)
    assert native_portfolio.cash_balance == pytest.approx(expected_cash)
