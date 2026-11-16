"""Phase 4.19 — Historical Shadow Cash Integrity.

The Three Portfolios "AI Portfolio" curve revalues each historical
ACTIVE_MODEL ShadowPortfolioSnapshot's holdings at canonical prices. It
previously added ShadowPortfolio.paper_cash_balance (TODAY's cash,
overwritten in place at every rebalance) to every historical date, so the
curve jumped whenever the shadow changed its cash weight. Each row must
instead be valued with its OWN cash, recovered from that row's own
persisted state:

    cash_t = total_value_t − Σ holdings_json[].market_value_t

All data is synthetic, on in-memory SQLite. No expected value here is a
real historical figure.

Coverage (brief §5 numbering)
  1  flat prices, unchanged holdings and cash
  2  flat prices, rebalance 95% → 50% → 95% invested (real regenerate writer)
  3  cash increases after a SELL
  4  cash decreases after a BUY
  5  multiple rebalance dates with moving prices
  6  changing prices, stable holdings
  7  canonical repricing of rows stored at a different (live) price
  8  missing / incomplete market values (incl. NAV-floor fallback rows)
  9  stored NAV inconsistent with holdings market value
  10 no historical snapshot data
  11 old snapshots without the enriched valuation fields
  12 stored shadow value vs reconstructed historical NAV (both real writers)
  Cross-page: Three Portfolios AI line/return/DD/vol, Gap A/B, Scorecard
  Implementation Shortfall, Ideal/You unchanged, Scorecard's stored AI
  return unchanged, remaining price-source discrepancy reported.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime, timedelta

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.decision_memory.shadow_tracker import (  # noqa: E402
    _compute_paper_value,
    _snapshot_price_history,
    regenerate_active_model_shadow,
)
from services.evaluation.ideal_series import (  # noqa: E402
    _derive_snapshot_cash,
    _revalue_ai_portfolio_with_canonical_prices,
    compute_three_portfolios,
)


# ── fixtures / helpers ────────────────────────────────────────────────────

@pytest.fixture()
def db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models.database import Base
    import models.asset  # noqa: F401 — registers Asset*/asset_relationships tables

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture()
def wp(db):
    from models.database import Workspace, Portfolio

    ws = Workspace(name="Test")
    db.add(ws)
    db.commit()
    p = Portfolio(workspace_id=ws.id, name="P1", cash_balance=0.0)
    db.add(p)
    db.commit()
    return ws, p


def _d(days_ago: int) -> str:
    return (date.today() - timedelta(days=days_ago)).isoformat()


def _price_day(db, ws, p, days_ago, prices, *, actual_return=0.0, actual_nav=1_000_000.0):
    """Canonical price archive row (PortfolioSnapshot.holdings_json), also the
    owner's own TWR input (investment_return_pct)."""
    from models.database import PortfolioSnapshot

    db.add(PortfolioSnapshot(
        workspace_id=ws.id, portfolio_id=p.id, snapshot_date=_d(days_ago),
        total_value=actual_nav, cash_balance=0.0,
        investment_return_pct=actual_return,
        holdings_json=json.dumps([{"symbol": s, "current_price": v} for s, v in prices.items()]),
    ))
    db.commit()


def _recommendation(db, ws, p, allocations, days_ago):
    from models.database import OptimizerHistory, RecommendationSnapshot

    oh = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=p.id, portfolio_name=p.name,
        analyzed_at=datetime.utcnow(), swap_count=0,
        result_json=json.dumps({"target_allocations": allocations, "cash_balance": 0.0}),
    )
    db.add(oh)
    db.commit()
    db.add(RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=p.id,
        total_portfolio_value=1_000_000.0,
        projected_allocations_json=json.dumps(allocations),
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    ))
    db.commit()


def _shadow(db, ws, p, *, inception_days_ago, paper_cash_balance):
    from models.database import ShadowPortfolio

    sh = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=p.id, shadow_type="ACTIVE_MODEL", name="AI",
        inception_date=_d(inception_days_ago), inception_value=1_000_000.0,
        inception_holdings_json="[]", paper_cash_balance=paper_cash_balance,
        is_active=True, created_at=datetime.utcnow(),
    )
    db.add(sh)
    db.commit()
    return sh


def _holdings(shares: dict[str, float]) -> list[dict]:
    return [{"symbol": s, "shares": n, "inception_price": 100.0, "price_frozen": False}
            for s, n in shares.items()]


def _persist_row(db, sh, days_ago, shares, cash, live_prices, prev_total=None):
    """Write one row exactly as value_shadow_portfolio does:
    enriched holdings from _compute_paper_value, total = equity + cash."""
    from models.database import ShadowPortfolioSnapshot

    equity, enriched = _compute_paper_value(_holdings(shares), live_prices)
    total = equity + cash
    daily = round((total - prev_total) / prev_total * 100, 4) if prev_total else None
    db.add(ShadowPortfolioSnapshot(
        shadow_portfolio_id=sh.id, snapshot_date=_d(days_ago), total_value=total,
        return_pct_since_inception=None, daily_return_pct=daily,
        holdings_json=json.dumps(enriched), created_at=datetime.utcnow(),
    ))
    db.commit()
    return total


def _persist_raw_row(db, sh, days_ago, holdings_json, total):
    from models.database import ShadowPortfolioSnapshot

    db.add(ShadowPortfolioSnapshot(
        shadow_portfolio_id=sh.id, snapshot_date=_d(days_ago), total_value=total,
        holdings_json=holdings_json, created_at=datetime.utcnow(),
    ))
    db.commit()


def _revalue(db, p, window=40):
    return _revalue_ai_portfolio_with_canonical_prices(
        db, p.id, _snapshot_price_history(db), _d(window), _d(0),
    )


def _rows(db, sh):
    from models.database import ShadowPortfolioSnapshot

    return (db.query(ShadowPortfolioSnapshot)
            .filter_by(shadow_portfolio_id=sh.id)
            .order_by(ShadowPortfolioSnapshot.snapshot_date).all())


def _legacy_index(db, sh, history):
    """What the pre-fix formula produced (canonical equity + CURRENT cash),
    used only to prove each scenario actually discriminates the defect."""
    from services.decision_memory.shadow_tracker import _price_near_date

    out = []
    for r in _rows(db, sh):
        h = json.loads(r.holdings_json)
        prices = {x["symbol"]: pp for x in h if (pp := _price_near_date(history, r.snapshot_date, x["symbol"]))}
        eq, _ = _compute_paper_value(h, prices)
        out.append(eq + sh.paper_cash_balance)
    return [v / out[0] * 100 for v in out]


def _dd(v):
    return v or 0.0


# ── 1. flat prices, unchanged holdings and cash ───────────────────────────

def test_01_flat_prices_unchanged_holdings_and_cash(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=10, paper_cash_balance=50_000.0)
    for n in range(10, -1, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0})
        _persist_row(db, sh, n, {"AAA": 9_500}, 50_000.0, {"AAA": 100.0})

    r = _revalue(db, p)

    assert r["status"] == "ok"
    assert r["excluded_rows"] == []
    assert all(row["index"] == pytest.approx(100.0) for row in r["series"])
    assert r["return_pct"] == pytest.approx(0.0)
    assert _dd(r["max_drawdown_pct"]) == pytest.approx(0.0)
    assert _dd(r["annualized_volatility"]) == pytest.approx(0.0)


# ── 2. flat prices, 95% → 50% → 95% invested (production regenerate) ──────

def test_02_flat_prices_rebalance_95_50_95_has_no_jumps(db, wp):
    ws, p = wp
    for n in range(30, -1, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0, "BBB": 50.0})
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 95.0}], 30)
    _recommendation(db, ws, p, [{"symbol": "BBB", "target_weight": 50.0}], 20)
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 95.0}], 10)
    sh = _shadow(db, ws, p, inception_days_ago=30, paper_cash_balance=0.0)
    assert regenerate_active_model_shadow(db, p.id)["status"] == "regenerated"
    db.refresh(sh)

    # Persisted per-row cash really does vary (50k / 500k / 50k), and today's
    # paper_cash_balance is only the last regime's value.
    implied = {round(_derive_snapshot_cash(json.loads(x.holdings_json), x.total_value)[0])
               for x in _rows(db, sh)}
    assert implied == {50_000, 500_000}
    assert sh.paper_cash_balance == pytest.approx(50_000.0)
    legacy = _legacy_index(db, sh, _snapshot_price_history(db))
    assert min(legacy) < 60.0  # the pre-fix curve dropped ~45% on day -20

    r = _revalue(db, p)

    assert r["status"] == "ok"
    assert all(row["index"] == pytest.approx(100.0, abs=1e-6) for row in r["series"])
    assert r["return_pct"] == pytest.approx(0.0, abs=1e-6)
    assert _dd(r["max_drawdown_pct"]) == pytest.approx(0.0, abs=1e-6)
    assert _dd(r["annualized_volatility"]) == pytest.approx(0.0, abs=1e-6)


# ── 3. cash increases after a SELL ─────────────────────────────────────────

def test_03_cash_increase_after_sell(db, wp):
    ws, p = wp
    # AAA 100 until day 6, 110 from day 5. Day 5: SELL 4,500 of 9,500
    # shares at 110 → cash 50,000 + 495,000 = 545,000. NAV conserved.
    sh = _shadow(db, ws, p, inception_days_ago=10, paper_cash_balance=545_000.0)
    for n in range(10, 5, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0})
        _persist_row(db, sh, n, {"AAA": 9_500}, 50_000.0, {"AAA": 100.0})
    for n in range(5, -1, -1):
        _price_day(db, ws, p, n, {"AAA": 110.0})
        _persist_row(db, sh, n, {"AAA": 5_000}, 545_000.0, {"AAA": 110.0})

    r = _revalue(db, p)

    expected_end = 5_000 * 110 + 545_000   # 1,095,000
    expected_start = 9_500 * 100 + 50_000  # 1,000,000
    assert r["return_pct"] == pytest.approx((expected_end / expected_start - 1) * 100)  # +9.5%
    idx = {row["date"]: row["index"] for row in r["series"]}
    assert idx[_d(6)] == pytest.approx(100.0)
    assert idx[_d(5)] == pytest.approx(109.5)  # price move only, no cash jump
    assert idx[_d(0)] == pytest.approx(109.5)
    assert _dd(r["max_drawdown_pct"]) == pytest.approx(0.0)
    # Pre-fix: start valued with today's 545k cash → ≈ −26.8%.
    assert _legacy_index(db, sh, _snapshot_price_history(db))[-1] < 75.0


# ── 4. cash decreases after a BUY ──────────────────────────────────────────

def test_04_cash_decrease_after_buy(db, wp):
    ws, p = wp
    # Day 5: BUY 4,500 shares at 100 → cash 500,000 → 50,000. Then AAA → 120.
    sh = _shadow(db, ws, p, inception_days_ago=10, paper_cash_balance=50_000.0)
    for n in range(10, 5, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0})
        _persist_row(db, sh, n, {"AAA": 5_000}, 500_000.0, {"AAA": 100.0})
    for n in range(5, 0, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0})
        _persist_row(db, sh, n, {"AAA": 9_500}, 50_000.0, {"AAA": 100.0})
    _price_day(db, ws, p, 0, {"AAA": 120.0})
    _persist_row(db, sh, 0, {"AAA": 9_500}, 50_000.0, {"AAA": 120.0})

    r = _revalue(db, p)

    assert r["return_pct"] == pytest.approx((9_500 * 120 + 50_000) / 1_000_000 * 100 - 100)  # +19%
    idx = [row["index"] for row in r["series"]]
    assert idx[:-1] == pytest.approx([100.0] * (len(idx) - 1))  # no jump at the BUY
    # Pre-fix: start valued with today's 50k cash → ≈ +116%.
    assert _legacy_index(db, sh, _snapshot_price_history(db))[-1] > 200.0


# ── 5. multiple rebalance dates, moving prices (production regenerate) ────

def test_05_multiple_rebalances_match_persisted_nav(db, wp):
    ws, p = wp
    prices = {n: {"AAA": 100.0 + (30 - n) * 1.5, "BBB": 50.0 - (30 - n) * 0.4} for n in range(30, -1, -1)}
    for n, px in prices.items():
        _price_day(db, ws, p, n, px)
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 95.0}], 30)
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 30.0}, {"symbol": "BBB", "target_weight": 30.0}], 24)
    _recommendation(db, ws, p, [{"symbol": "BBB", "target_weight": 90.0}], 18)
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 40.0}], 12)
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 50.0}, {"symbol": "BBB", "target_weight": 45.0}], 6)
    sh = _shadow(db, ws, p, inception_days_ago=30, paper_cash_balance=0.0)
    assert regenerate_active_model_shadow(db, p.id)["status"] == "regenerated"

    rows = _rows(db, sh)
    assert len({round(_derive_snapshot_cash(json.loads(x.holdings_json), x.total_value)[0]) for x in rows}) >= 4

    r = _revalue(db, p)

    # regenerate prices from the same canonical archive, so the canonical
    # revaluation must reproduce the persisted NAV path on every date.
    persisted_idx = [x.total_value / rows[0].total_value * 100 for x in rows]
    assert [row["date"] for row in r["series"]] == [x.snapshot_date for x in rows]
    assert [row["index"] for row in r["series"]] == pytest.approx(persisted_idx, abs=1e-3)


# ── 6. changing prices, stable holdings ────────────────────────────────────

def test_06_changing_prices_stable_holdings(db, wp):
    ws, p = wp
    path = {6: 100.0, 5: 90.0, 4: 80.0, 3: 95.0, 2: 110.0, 1: 115.0, 0: 120.0}
    sh = _shadow(db, ws, p, inception_days_ago=6, paper_cash_balance=100_000.0)
    for n, px in path.items():
        _price_day(db, ws, p, n, {"AAA": px})
        _persist_row(db, sh, n, {"AAA": 9_000}, 100_000.0, {"AAA": px})

    r = _revalue(db, p)

    expected = [(9_000 * px + 100_000) / 1_000_000 * 100 for px in path.values()]
    assert [row["index"] for row in r["series"]] == pytest.approx(expected)
    assert r["max_drawdown_pct"] == pytest.approx((1 - 820_000 / 1_000_000) * 100, abs=0.01)


# ── 7. canonical repricing of rows stored at a different live price ───────

def test_07_canonical_prices_drive_value_while_cash_is_row_own(db, wp):
    ws, p = wp
    # Live cache priced AAA at 105 on the last day; canonical archive says 100.
    sh = _shadow(db, ws, p, inception_days_ago=5, paper_cash_balance=999_999.0)
    for n in range(5, 0, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0})
        _persist_row(db, sh, n, {"AAA": 8_000}, 200_000.0, {"AAA": 100.0})
    _price_day(db, ws, p, 0, {"AAA": 100.0})
    _persist_row(db, sh, 0, {"AAA": 8_000}, 200_000.0, {"AAA": 105.0})

    last = _rows(db, sh)[-1]
    cash, reason = _derive_snapshot_cash(json.loads(last.holdings_json), last.total_value)
    assert reason is None and cash == pytest.approx(200_000.0, abs=0.01)  # price source cancels

    r = _revalue(db, p)

    assert r["return_pct"] == pytest.approx(0.0)  # canonical, not the live +4%


# ── 8. missing / incomplete market values ──────────────────────────────────

def test_08a_row_with_unpriced_holding_is_excluded_not_filled(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=4, paper_cash_balance=300_000.0)
    for n, px in {4: 100.0, 3: 100.0, 1: 100.0, 0: 110.0}.items():
        _price_day(db, ws, p, n, {"AAA": px})
        _persist_row(db, sh, n, {"AAA": 9_000}, 100_000.0, {"AAA": px})
    _price_day(db, ws, p, 2, {"AAA": 100.0})
    bad = [{"symbol": "AAA", "shares": 9_000, "inception_price": 0.0, "current_price": None,
            "market_value": None, "price_source": "missing"}]
    _persist_raw_row(db, sh, 2, json.dumps(bad), 100_000.0)

    r = _revalue(db, p)

    assert r["status"] == "ok"
    assert r["excluded_rows"] == [{"date": _d(2), "reason": "missing_market_value"}]
    assert _d(2) not in [row["date"] for row in r["series"]]
    assert r["return_pct"] == pytest.approx((9_000 * 110 + 100_000) / 1_000_000 * 100 - 100)


def test_08b_nav_floor_fallback_row_is_excluded(db, wp):
    """value_shadow_portfolio's NAV floor guard writes total_value = last
    valid NAV with every holding unpriced; that total is not cash."""
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=2, paper_cash_balance=0.0)
    _price_day(db, ws, p, 2, {"AAA": 100.0})
    _persist_row(db, sh, 2, {"AAA": 10_000}, 0.0, {"AAA": 100.0})
    _price_day(db, ws, p, 1, {"AAA": 100.0})
    floor = [{"symbol": "AAA", "shares": 10_000, "current_price": None, "market_value": None,
              "price_source": "missing"}]
    _persist_raw_row(db, sh, 1, json.dumps(floor), 1_000_000.0)
    _price_day(db, ws, p, 0, {"AAA": 100.0})
    _persist_row(db, sh, 0, {"AAA": 10_000}, 0.0, {"AAA": 100.0})

    r = _revalue(db, p)

    assert [e["date"] for e in r["excluded_rows"]] == [_d(1)]
    assert r["return_pct"] == pytest.approx(0.0)
    assert len(r["series"]) == 2


def test_08c_all_rows_incomplete_is_explicit_missing_data(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=1, paper_cash_balance=500_000.0)
    _price_day(db, ws, p, 1, {"AAA": 100.0})
    _price_day(db, ws, p, 0, {"AAA": 100.0})
    bad = json.dumps([{"symbol": "AAA", "shares": 5_000, "market_value": None}])
    _persist_raw_row(db, sh, 1, bad, 1_000_000.0)
    _persist_raw_row(db, sh, 0, bad, 1_000_000.0)

    r = _revalue(db, p)

    assert r["status"] == "incomplete_snapshot_data"
    assert r["return_pct"] is None and r["series"] == []


def test_08d_holding_without_any_canonical_price_is_excluded(db, wp):
    """Persisted row valued ZZZ from the live cache (inception_price 0), but
    the canonical archive has no ZZZ price: dropping it would fabricate a loss."""
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=1, paper_cash_balance=0.0)
    _price_day(db, ws, p, 1, {"AAA": 100.0})
    _price_day(db, ws, p, 0, {"AAA": 100.0})
    _persist_row(db, sh, 1, {"AAA": 5_000}, 500_000.0, {"AAA": 100.0})
    row = [{"symbol": "ZZZ", "shares": 5_000, "inception_price": 0.0, "price_frozen": False,
            "current_price": 100.0, "market_value": 500_000.0, "price_source": "cached"}]
    _persist_raw_row(db, sh, 0, json.dumps(row), 1_000_000.0)

    r = _revalue(db, p)

    assert r["excluded_rows"] == [{"date": _d(0), "reason": "canonical_price_unavailable"}]


# ── 9. stored NAV inconsistent with holdings market value ──────────────────

def test_09a_total_below_holdings_value_is_rejected_not_clamped(db, wp):
    holdings = [{"symbol": "AAA", "shares": 10_000, "current_price": 100.0, "market_value": 1_000_000.0}]
    cash, reason = _derive_snapshot_cash(holdings, 900_000.0)
    assert cash is None and reason == "negative_derived_cash"


def test_09b_market_value_not_shares_times_price_is_rejected(db, wp):
    holdings = [{"symbol": "AAA", "shares": 10_000, "current_price": 100.0, "market_value": 800_000.0}]
    cash, reason = _derive_snapshot_cash(holdings, 1_000_000.0)
    assert cash is None and reason == "market_value_mismatch"


def test_09c_rounding_residue_is_tolerated_without_clamping(db, wp):
    # Production stores round(mv, 2); a −0.004 residual is rounding, not cash.
    holdings = [{"symbol": "AAA", "shares": 3.333333, "current_price": 33.33,
                 "market_value": round(3.333333 * 33.33, 2)}]
    cash, reason = _derive_snapshot_cash(holdings, 3.333333 * 33.33)
    assert reason is None and abs(cash) < 0.01


def test_09d_inconsistent_row_in_series_is_excluded(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=2, paper_cash_balance=0.0)
    for n in (2, 1, 0):
        _price_day(db, ws, p, n, {"AAA": 100.0})
    _persist_row(db, sh, 2, {"AAA": 10_000}, 0.0, {"AAA": 100.0})
    _persist_raw_row(db, sh, 1, json.dumps(
        [{"symbol": "AAA", "shares": 10_000, "current_price": 100.0, "market_value": 1_000_000.0}]), 700_000.0)
    _persist_row(db, sh, 0, {"AAA": 10_000}, 0.0, {"AAA": 100.0})

    r = _revalue(db, p)

    assert r["excluded_rows"] == [{"date": _d(1), "reason": "negative_derived_cash"}]
    assert r["return_pct"] == pytest.approx(0.0)


# ── 10. no historical snapshot data ────────────────────────────────────────

def test_10a_no_shadow(db, wp):
    _, p = wp
    assert _revalue(db, p)["status"] == "unavailable"


def test_10b_shadow_without_snapshot_rows(db, wp):
    ws, p = wp
    _shadow(db, ws, p, inception_days_ago=5, paper_cash_balance=400_000.0)
    r = _revalue(db, p)
    assert r["status"] == "no_snapshots_in_window"
    assert r["return_pct"] is None


# ── 11. old snapshots without enriched valuation fields ────────────────────

def test_11a_legacy_rows_never_fall_back_to_current_cash(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=1, paper_cash_balance=300_000.0)
    legacy = json.dumps([{"symbol": "AAA", "shares": 7_000, "inception_price": 100.0}])
    for n in (1, 0):
        _price_day(db, ws, p, n, {"AAA": 100.0})
        _persist_raw_row(db, sh, n, legacy, 1_000_000.0)

    r = _revalue(db, p)

    assert r["status"] == "incomplete_snapshot_data"
    assert {e["reason"] for e in r["excluded_rows"]} == {"missing_market_value"}
    assert r["return_pct"] is None


def test_11b_legacy_prefix_then_enriched_rows_start_at_first_enriched(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=4, paper_cash_balance=0.0)
    legacy = json.dumps([{"symbol": "AAA", "shares": 9_000, "inception_price": 100.0}])
    for n, px in {4: 100.0, 3: 100.0, 2: 100.0, 1: 104.0, 0: 108.0}.items():
        _price_day(db, ws, p, n, {"AAA": px})
    _persist_raw_row(db, sh, 4, legacy, 1_000_000.0)
    _persist_raw_row(db, sh, 3, legacy, 1_000_000.0)
    for n, px in {2: 100.0, 1: 104.0, 0: 108.0}.items():
        _persist_row(db, sh, n, {"AAA": 9_000}, 100_000.0, {"AAA": px})

    r = _revalue(db, p)

    assert r["series"][0]["date"] == _d(2)
    assert r["return_pct"] == pytest.approx((9_000 * 108 + 100_000) / 1_000_000 * 100 - 100)


def test_11c_rows_without_holdings_json_keep_no_price_history_status(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=1, paper_cash_balance=300_000.0)
    _price_day(db, ws, p, 1, {"AAA": 100.0})
    _persist_raw_row(db, sh, 1, None, 1_000_000.0)
    assert _revalue(db, p)["status"] == "no_price_history"


def test_11d_valid_all_cash_row_is_distinct_from_missing_or_malformed_holdings(db, wp):
    """An all-cash row ("[]" or only zero-share holdings) is valid: its
    cash is its whole total_value. Missing/blank/malformed/non-list
    holdings_json is missing data and is excluded, never read as all-cash."""
    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=6, paper_cash_balance=123_456.0)
    for n in range(6, -1, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0})
    zero_shares = json.dumps([{"symbol": "AAA", "shares": 0, "inception_price": 100.0,
                               "current_price": 100.0, "market_value": 0.0, "price_source": "zero_shares"}])
    _persist_raw_row(db, sh, 6, "[]", 1_000_000.0)          # valid: 100% cash
    _persist_raw_row(db, sh, 5, None, 1_000_000.0)          # missing
    _persist_raw_row(db, sh, 4, "", 1_000_000.0)            # blank
    _persist_raw_row(db, sh, 3, "{not json", 1_000_000.0)   # malformed
    _persist_raw_row(db, sh, 2, '{"AAA": 1}', 1_000_000.0)  # not a list
    _persist_raw_row(db, sh, 1, zero_shares, 1_000_000.0)   # valid: 100% cash
    _persist_row(db, sh, 0, {"AAA": 5_000}, 500_000.0, {"AAA": 100.0})

    assert _derive_snapshot_cash([], 1_000_000.0) == (1_000_000.0, None)

    r = _revalue(db, p)

    assert r["status"] == "ok"
    assert [row["date"] for row in r["series"]] == [_d(6), _d(1), _d(0)]
    assert r["return_pct"] == pytest.approx(0.0)
    assert {e["date"]: e["reason"] for e in r["excluded_rows"]} == {
        _d(5): "missing_holdings_json",
        _d(4): "missing_holdings_json",
        _d(3): "invalid_holdings_json",
        _d(2): "invalid_holdings_json",
    }


# ── 12. stored shadow value vs reconstructed historical NAV ────────────────

def test_12a_regenerated_rows_reconstruct_exactly(db, wp):
    ws, p = wp
    for n in range(12, -1, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0 + n, "BBB": 40.0 + (12 - n)})
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 80.0}], 12)
    _recommendation(db, ws, p, [{"symbol": "BBB", "target_weight": 35.0}], 6)
    sh = _shadow(db, ws, p, inception_days_ago=12, paper_cash_balance=0.0)
    regenerate_active_model_shadow(db, p.id)

    rows = _rows(db, sh)
    r = _revalue(db, p)

    assert r["excluded_rows"] == []
    for row, stored in zip(r["series"], rows):
        assert row["index"] == pytest.approx(stored.total_value / rows[0].total_value * 100, abs=1e-4)


def test_12b_live_writer_row_reconstructs_when_prices_agree(db, wp, monkeypatch):
    """A row written by the real value_shadow_portfolio, whose live price
    equals the canonical one, must revalue to its own stored total_value."""
    from services.decision_memory import shadow_tracker

    ws, p = wp
    _price_day(db, ws, p, 1, {"AAA": 100.0})
    _price_day(db, ws, p, 0, {"AAA": 125.0})
    sh = _shadow(db, ws, p, inception_days_ago=1, paper_cash_balance=250_000.0)
    sh.inception_holdings_json = json.dumps(_holdings({"AAA": 7_500}))
    db.commit()
    _persist_row(db, sh, 1, {"AAA": 7_500}, 250_000.0, {"AAA": 100.0})

    monkeypatch.setattr(shadow_tracker, "_fetch_cached_prices", lambda _db, syms: {"AAA": 125.0})
    shadow_tracker.value_shadow_portfolio(db, sh.id)
    today = _rows(db, sh)[-1]
    assert today.snapshot_date == _d(0)

    r = _revalue(db, p)

    assert r["series"][-1]["index"] == pytest.approx(today.total_value / 1_000_000.0 * 100, abs=1e-6)
    assert r["return_pct"] == pytest.approx((7_500 * 125 + 250_000) / 1_000_000 * 100 - 100)


# ── Cross-page regression ──────────────────────────────────────────────────

def _seed_95_50_95(db, ws, p):
    for n in range(30, -1, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0, "BBB": 50.0}, actual_return=None if n == 30 else 0.0)
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 95.0}], 30)
    _recommendation(db, ws, p, [{"symbol": "BBB", "target_weight": 50.0}], 20)
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 95.0}], 10)
    sh = _shadow(db, ws, p, inception_days_ago=30, paper_cash_balance=0.0)
    regenerate_active_model_shadow(db, p.id)
    db.refresh(sh)
    return sh


def test_xp_three_portfolios_ai_line_return_dd_vol_and_gaps(db, wp):
    ws, p = wp
    _seed_95_50_95(db, ws, p)

    tp = compute_three_portfolios(db, p.id, period_days=30)

    ai = tp["ai_portfolio"]
    assert ai["status"] == "ok"
    assert ai["return_pct"] == pytest.approx(0.0, abs=1e-6)
    assert _dd(ai["max_drawdown_pct"]) == pytest.approx(0.0, abs=1e-6)
    assert _dd(ai["annualized_volatility"]) == pytest.approx(0.0, abs=1e-6)
    ai_line = [row["ai"] for row in tp["chart"] if row["ai"] is not None]
    assert ai_line and all(v == pytest.approx(100.0, abs=1e-4) for v in ai_line)
    assert tp["gap_a"]["value"] == pytest.approx(round(tp["ideal"]["return_pct"] - ai["return_pct"], 4), abs=1e-4)
    assert tp["gap_a"]["value"] == pytest.approx(0.0, abs=1e-4)
    assert tp["gap_b"]["value"] == pytest.approx(round(ai["return_pct"] - tp["actual"]["return_pct"], 4), abs=1e-4)


def test_xp_result_independent_of_current_paper_cash_and_ideal_you_unchanged(db, wp):
    from models.database import ShadowPortfolio

    ws, p = wp
    sh = _seed_95_50_95(db, ws, p)
    before = compute_three_portfolios(db, p.id, period_days=30)

    # A later rebalance overwrites today's cash; history must not move.
    db.query(ShadowPortfolio).filter_by(id=sh.id).update({"paper_cash_balance": 987_654.0})
    db.commit()
    after = compute_three_portfolios(db, p.id, period_days=30)

    for key in ("chart", "ideal", "ai_portfolio", "actual", "gap_a", "gap_b"):
        assert before[key] == after[key], key


def test_xp_scorecard_shortfall_uses_corrected_gap_a_and_stored_ai_return_unchanged(db, wp):
    import models.database as mdb

    if not str(mdb.engine.url).startswith("sqlite"):
        pytest.skip("compute_scorecard imports main; run with DATABASE_URL=sqlite:///:memory:")
    from services.analytics.attribution_engine import compute_portfolio_attribution
    from services.evaluation.scorecard import compute_scorecard

    ws, p = wp
    sh = _seed_95_50_95(db, ws, p)

    tp = compute_three_portfolios(db, p.id, period_days=30)
    sc = compute_scorecard(db, p.id, period_days=30)

    shortfall = sc["execution"]["implementation_shortfall"]
    assert shortfall["status"] == "ok"
    assert shortfall["value_pct"] == tp["gap_a"]["value"]
    assert shortfall["value_pct"] == pytest.approx(0.0, abs=1e-4)

    # Scorecard's stored-return methodology (persisted daily_return_pct TWR)
    # is untouched: still equals the attribution engine's own figure.
    att = compute_portfolio_attribution(db, p.id, 30)
    assert sc["outcome"]["ai_model_return_pct"] == att["ai_model_shadow"]["return_pct"]
    twr = 1.0
    for r in _rows(db, sh):
        if r.daily_return_pct is not None and r.snapshot_date >= _d(30):
            twr *= 1 + r.daily_return_pct / 100
    assert sc["outcome"]["ai_model_return_pct"] == pytest.approx((twr - 1) * 100, abs=0.01)


def test_xp_price_source_discrepancy_is_reported_not_hidden(db, wp):
    from services.analytics.attribution_engine import compute_portfolio_attribution

    ws, p = wp
    sh = _shadow(db, ws, p, inception_days_ago=5, paper_cash_balance=200_000.0)
    prev = None
    for n in range(5, -1, -1):
        _price_day(db, ws, p, n, {"AAA": 100.0}, actual_return=None if n == 5 else 0.0)
        live = 100.0 if n else 105.0  # live cache diverges on the last day
        prev = _persist_row(db, sh, n, {"AAA": 8_000}, 200_000.0, {"AAA": live}, prev)
    _recommendation(db, ws, p, [{"symbol": "AAA", "target_weight": 80.0}], 5)

    tp = compute_three_portfolios(db, p.id, period_days=5)
    att = compute_portfolio_attribution(db, p.id, 5)

    # Canonical view: 0%. Stored live-priced view: +4% (8,000 × 5 / 1,000,000).
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx(0.0)
    assert att["ai_model_shadow"]["return_pct"] == pytest.approx(4.0, abs=0.01)
