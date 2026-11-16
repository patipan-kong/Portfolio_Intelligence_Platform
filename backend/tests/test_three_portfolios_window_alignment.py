"""Phase 4.21 — Three Portfolios shared comparison window.

Ideal and AI observations are point-in-time valuations; an owner snapshot
row carries the return since the PREVIOUS row. compute_three_portfolios
must compare all three over ONE interval [start, end] whose bounds are real
observations of every participating series:

  - the owner's first in-window return (which covers the interval before
    the start valuation) is excluded;
  - a series that extends past the others (AI valued later) is trimmed;
  - nothing is forward-filled at either edge, and no gap is computed when
    no shared interval exists.

Synthetic in-memory SQLite only; no network, no configured database.
"""
from __future__ import annotations

import json
import math
import os
import sys
from datetime import date, datetime, timedelta

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.evaluation.ideal_series import compute_ideal_series, compute_three_portfolios  # noqa: E402
from services.analytics.attribution_engine import (  # noqa: E402
    _compute_daily_volatility,
    compute_portfolio_attribution,
    compute_return_index_drawdown,
)


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
    p = Portfolio(workspace_id=ws.id, name="P", cash_balance=0.0)
    db.add(p)
    db.commit()
    return ws, p


def _d(n: int) -> str:
    return (date.today() - timedelta(days=n)).isoformat()


def _recommendation(db, ws, p, days_ago=15, weight=100.0):
    from models.database import OptimizerHistory, RecommendationSnapshot

    allocs = [{"symbol": "AAA", "target_weight": weight, "action": "BUY"}]
    oh = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=p.id, portfolio_name=p.name,
        analyzed_at=datetime.utcnow(), swap_count=0,
        result_json=json.dumps({"target_allocations": allocs, "cash_balance": 0.0}),
    )
    db.add(oh)
    db.commit()
    db.add(RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=p.id,
        total_portfolio_value=1_000_000.0, projected_allocations_json=json.dumps(allocs),
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    ))
    db.commit()


def _owner_day(db, ws, p, n, price, nav, ret, flow=None, with_prices=True):
    """One owner PortfolioSnapshot: a valuation (nav) plus the return since
    the previous row (ret). Its holdings_json price is also the canonical
    price Ideal and the AI revaluation read for that date (with_prices=False
    leaves that date out of the canonical archive)."""
    from models.database import PortfolioSnapshot

    db.add(PortfolioSnapshot(
        workspace_id=ws.id, portfolio_id=p.id, snapshot_date=_d(n),
        total_value=nav, cash_balance=0.0,
        investment_return_pct=ret, daily_return_pct=ret, net_external_cash_flow=flow,
        holdings_json=json.dumps([{"symbol": "AAA", "current_price": price}]) if with_prices else None,
    ))
    db.commit()


def _price_only(db, ws, portfolio_id, n, price):
    """A canonical price observation from ANOTHER portfolio (the canonical
    archive spans every portfolio's snapshots, as in production)."""
    from models.database import PortfolioSnapshot

    db.add(PortfolioSnapshot(
        workspace_id=ws.id, portfolio_id=portfolio_id, snapshot_date=_d(n),
        total_value=1.0, cash_balance=0.0,
        holdings_json=json.dumps([{"symbol": "AAA", "current_price": price}]),
    ))
    db.commit()


def _ai_shadow(db, ws, p, rows, paper_cash_now=0.0):
    """rows: [(days_ago, shares, cash_t, live_price)] persisted in production
    shape: enriched holdings_json, total_value = Σ market_value + cash_t,
    daily_return_pct chained from the stored totals."""
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot
    from services.decision_memory.shadow_tracker import _compute_paper_value

    first = max(r[0] for r in rows)
    sh = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=p.id, shadow_type="ACTIVE_MODEL", name="AI",
        inception_date=_d(first), inception_value=1_000_000.0,
        inception_holdings_json=json.dumps([{"symbol": "AAA", "shares": rows[0][1], "inception_price": 100.0}]),
        paper_cash_balance=paper_cash_now, is_active=True, created_at=datetime.utcnow(),
    )
    db.add(sh)
    db.commit()
    prev = None
    for n, shares, cash_t, live in sorted(rows, key=lambda r: -r[0]):
        holdings = [{"symbol": "AAA", "shares": shares, "inception_price": 100.0, "price_frozen": False}]
        equity, enriched = _compute_paper_value(holdings, {"AAA": live})
        total = equity + cash_t
        db.add(ShadowPortfolioSnapshot(
            shadow_portfolio_id=sh.id, snapshot_date=_d(n), total_value=total,
            daily_return_pct=None if prev is None else (total - prev) / prev * 100,
            holdings_json=json.dumps(enriched), created_at=datetime.utcnow(),
        ))
        prev = total
    db.commit()
    return sh


def _twr(rets):
    out = 1.0
    for r in rets:
        out *= 1 + r / 100
    return (out - 1) * 100


def _vol_of_values(values):
    return _compute_daily_volatility([(b - a) / a * 100 for a, b in zip(values, values[1:])])


def _assert_gap_arithmetic(tp):
    i, a, y = tp["ideal"]["return_pct"], tp["ai_portfolio"]["return_pct"], tp["actual"]["return_pct"]
    if i is not None and a is not None:
        assert tp["gap_a"]["value"] == pytest.approx(round(i - a, 4), abs=1e-9)
    if a is not None and y is not None:
        assert tp["gap_b"]["value"] == pytest.approx(round(a - y, 4), abs=1e-9)


PRICES = {10: 100.0, 9: 102.0, 8: 99.0, 7: 103.0, 6: 101.0, 5: 104.0, 4: 100.0, 3: 105.0,
          2: 103.0, 1: 106.0, 0: 108.0}
OWNER_R = {10: 5.0, 9: 1.0, 8: -2.0, 7: 0.5, 6: 1.5, 5: -1.0, 4: 2.0, 3: -0.5, 2: 1.0, 1: -1.5, 0: 0.8}


def _seed_full(db, ws, p, *, owner_days=range(10, -1, -1), ai_days=range(10, -1, -1), owner_r=None,
               ai_shares=10_000, ai_cash=0.0):
    owner_r = owner_r or OWNER_R
    _recommendation(db, ws, p)
    nav = 1_000_000.0
    for n in owner_days:
        nav *= 1 + (owner_r[n] or 0) / 100
        _owner_day(db, ws, p, n, PRICES[n], nav, owner_r[n])
    return _ai_shadow(db, ws, p, [(n, ai_shares, ai_cash, PRICES[n]) for n in ai_days])


# ── 1. First in-window owner return belongs to an earlier interval ─────────

def test_first_in_window_owner_return_is_excluded_and_gap_b_changes(db, wp):
    ws, p = wp
    _seed_full(db, ws, p)

    tp = compute_three_portfolios(db, p.id, period_days=10)
    unaligned_owner = compute_portfolio_attribution(db, p.id, 10)["actual"]["return_pct"]

    win = tp["comparison_window"]
    assert (win["status"], win["start"], win["end"]) == ("aligned", _d(10), _d(0))

    expected_owner = _twr([OWNER_R[n] for n in range(9, -1, -1)])          # day-10 return excluded
    assert tp["actual"]["return_pct"] == pytest.approx(expected_owner, abs=1e-3)
    assert unaligned_owner == pytest.approx(_twr([OWNER_R[n] for n in range(10, -1, -1)]), abs=1e-3)
    assert tp["actual"]["return_pct"] != pytest.approx(unaligned_owner, abs=1.0)

    ai = (PRICES[0] / PRICES[10] - 1) * 100
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx(ai, abs=1e-3)
    assert tp["ideal"]["return_pct"] == pytest.approx(ai, abs=1e-3)
    # Gap B is the aligned difference, not AI minus the 11-interval owner chain.
    assert tp["gap_b"]["value"] == pytest.approx(ai - expected_owner, abs=1e-3)
    assert tp["gap_b"]["value"] != pytest.approx(ai - unaligned_owner, abs=1.0)
    _assert_gap_arithmetic(tp)


def test_owner_drawdown_and_volatility_use_the_same_bounded_returns(db, wp):
    ws, p = wp
    _seed_full(db, ws, p)

    tp = compute_three_portfolios(db, p.id, period_days=10)

    rets = [OWNER_R[n] for n in range(9, -1, -1)]
    assert tp["actual"]["annualized_volatility"] == pytest.approx(_compute_daily_volatility(rets), abs=1e-4)
    dd = compute_return_index_drawdown([(None, r) for r in rets])["max_drawdown_pct"]
    assert tp["actual"]["max_drawdown_pct"] == pytest.approx(dd, abs=1e-4)


# ── 2. AI extends beyond Owner / Ideal ─────────────────────────────────────

def test_ai_three_days_past_owner_and_ideal_is_trimmed_no_flat_tail(db, wp):
    """Owner and the canonical price archive end at day 3; the AI shadow keeps
    being valued through day 0 (prices carried forward = flat tail). The flat
    tail must not enter AI's volatility or the comparison."""
    ws, p = wp
    _seed_full(db, ws, p, owner_days=range(10, 2, -1), ai_days=range(10, -1, -1))

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["end"] == _d(3)
    values = [PRICES[n] for n in range(10, 2, -1)]
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx((PRICES[3] / PRICES[10] - 1) * 100, abs=1e-3)
    assert tp["ai_portfolio"]["annualized_volatility"] == pytest.approx(_vol_of_values(values), abs=1e-3)
    with_flat_tail = _vol_of_values(values + [PRICES[3]] * 3)
    assert tp["ai_portfolio"]["annualized_volatility"] != pytest.approx(with_flat_tail, abs=1e-3)
    _assert_gap_arithmetic(tp)


def test_ai_and_ideal_ending_after_owner_are_bounded_by_owner_end(db, wp):
    """Real price movement after the owner's last snapshot (from another
    portfolio's canonical prices) must not enter AI/Ideal while You stops."""
    from models.database import Portfolio

    ws, p = wp
    other = Portfolio(workspace_id=ws.id, name="Other", cash_balance=0.0)
    db.add(other)
    db.commit()
    _seed_full(db, ws, p, owner_days=range(10, 2, -1), ai_days=range(10, 2, -1))
    for n in (2, 1, 0):
        _price_only(db, ws, other.id, n, 130.0)
    from models.database import ShadowPortfolio
    sh = db.query(ShadowPortfolio).filter_by(portfolio_id=p.id).one()
    db.delete(sh)
    db.commit()
    _ai_shadow(db, ws, p, [(n, 10_000, 0.0, PRICES[n]) for n in range(10, 2, -1)]
               + [(n, 10_000, 0.0, 130.0) for n in (2, 1, 0)])

    tp = compute_three_portfolios(db, p.id, period_days=10)
    full_ideal = compute_ideal_series(db, p.id, 10)["return_pct"]

    assert tp["comparison_window"]["end"] == _d(3)
    to_day3 = (PRICES[3] / PRICES[10] - 1) * 100
    assert full_ideal == pytest.approx(30.0, abs=1e-3)                    # unbounded Ideal sees the jump
    assert tp["ideal"]["return_pct"] == pytest.approx(to_day3, abs=1e-3)
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx(to_day3, abs=1e-3)
    expected_owner = _twr([OWNER_R[n] for n in range(9, 2, -1)])
    assert tp["actual"]["return_pct"] == pytest.approx(expected_owner, abs=1e-3)
    assert tp["gap_b"]["value"] == pytest.approx(to_day3 - expected_owner, abs=1e-3)
    _assert_gap_arithmetic(tp)


# ── 3. Implementation Shortfall follows aligned Gap A ──────────────────────

def _seed_shortfall_case(db, ws, p):
    """Ideal 100% AAA; AI holds half cash, so Gap A is non-zero. Prices after
    the owner's last day (day 3) jump, and AI/Ideal would see that jump."""
    from models.database import Portfolio

    other = Portfolio(workspace_id=ws.id, name="Other", cash_balance=0.0)
    db.add(other)
    db.commit()
    _recommendation(db, ws, p)
    nav = 1_000_000.0
    for n in range(10, 2, -1):
        nav *= 1 + OWNER_R[n] / 100
        _owner_day(db, ws, p, n, PRICES[n], nav, OWNER_R[n])
    for n in (2, 1, 0):
        _price_only(db, ws, other.id, n, 130.0)
    live = {**PRICES, 2: 130.0, 1: 130.0, 0: 130.0}
    return _ai_shadow(db, ws, p, [(n, 5_000, 500_000.0, live[n]) for n in range(10, -1, -1)])


def test_gap_a_is_measured_over_the_shared_window(db, wp):
    ws, p = wp
    _seed_shortfall_case(db, ws, p)

    tp = compute_three_portfolios(db, p.id, period_days=10)

    move = PRICES[3] / PRICES[10] - 1
    ideal = move * 100
    ai = (5_000 * PRICES[3] + 500_000) / (5_000 * PRICES[10] + 500_000) * 100 - 100
    assert tp["ideal"]["return_pct"] == pytest.approx(ideal, abs=1e-3)
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx(ai, abs=1e-3)
    assert tp["gap_a"]["value"] == pytest.approx(ideal - ai, abs=1e-3)
    # The unbounded comparison (both through day 0's 130 price) would differ.
    unbounded_ai = (5_000 * 130 + 500_000) / (5_000 * PRICES[10] + 500_000) * 100 - 100
    assert tp["gap_a"]["value"] != pytest.approx(30.0 - unbounded_ai, abs=0.5)
    _assert_gap_arithmetic(tp)


def test_scorecard_shortfall_uses_aligned_gap_a_and_stored_methodology_unchanged(db, wp):
    import models.database as mdb

    if not str(mdb.engine.url).startswith("sqlite"):
        pytest.skip("compute_scorecard imports main; run with DATABASE_URL=sqlite:///:memory:")
    from services.evaluation.scorecard import compute_scorecard

    ws, p = wp
    sh = _seed_shortfall_case(db, ws, p)

    tp = compute_three_portfolios(db, p.id, period_days=10)
    sc = compute_scorecard(db, p.id, period_days=10)

    shortfall = sc["execution"]["implementation_shortfall"]
    assert shortfall["status"] == "ok"
    assert shortfall["value_pct"] == tp["gap_a"]["value"]

    # Scorecard's independent stored-shadow methodology is untouched: the
    # full-window TWR of persisted daily_return_pct, including the day-0 jump.
    from models.database import ShadowPortfolioSnapshot
    att = compute_portfolio_attribution(db, p.id, 10)
    assert sc["outcome"]["ai_model_return_pct"] == att["ai_model_shadow"]["return_pct"]
    rows = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=sh.id).all()
    stored = _twr([r.daily_return_pct for r in rows if r.daily_return_pct is not None])
    assert sc["outcome"]["ai_model_return_pct"] == pytest.approx(stored, abs=0.01)


# ── 4. Already-aligned scenario is unchanged ───────────────────────────────

def test_already_aligned_series_reproduce_previous_figures(db, wp):
    """Owner's first in-window row is its inception (no return), and all
    three series share every date: the result equals each series' own
    full-window figures, exactly as before this phase."""
    from services.analytics.attribution_engine import _actual_portfolio_metrics, _get_actual_snapshots
    from services.evaluation.ideal_series import _revalue_ai_portfolio_with_canonical_prices
    from services.decision_memory.shadow_tracker import _snapshot_price_history

    ws, p = wp
    _seed_full(db, ws, p, owner_r={**OWNER_R, 10: None})

    tp = compute_three_portfolios(db, p.id, period_days=10)
    ideal = compute_ideal_series(db, p.id, 10)
    ai = _revalue_ai_portfolio_with_canonical_prices(
        db, p.id, _snapshot_price_history(db), ideal["period_start"], ideal["period_end"])
    own = _actual_portfolio_metrics(_get_actual_snapshots(db, p.id, _d(10)))

    assert tp["comparison_window"]["status"] == "aligned"
    assert tp["ideal"]["return_pct"] == pytest.approx(ideal["return_pct"], abs=1e-9)
    assert tp["ideal"]["max_drawdown_pct"] == pytest.approx(ideal["max_drawdown_pct"], abs=1e-9)
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx(ai["return_pct"], abs=1e-9)
    assert tp["ai_portfolio"]["max_drawdown_pct"] == pytest.approx(ai["max_drawdown_pct"], abs=1e-9)
    assert tp["ai_portfolio"]["annualized_volatility"] == pytest.approx(ai["annualized_volatility"], abs=1e-3)
    assert tp["actual"]["return_pct"] == pytest.approx(own[0], abs=1e-9)
    assert tp["actual"]["max_drawdown_pct"] == pytest.approx(own[1], abs=1e-9)
    assert tp["actual"]["annualized_volatility"] == pytest.approx(own[2], abs=1e-9)
    _assert_gap_arithmetic(tp)


# ── 5. Start / end edge cases ──────────────────────────────────────────────

def test_ai_starting_after_cutoff_moves_the_shared_start(db, wp):
    ws, p = wp
    _seed_full(db, ws, p, ai_days=range(5, -1, -1))

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["start"] == _d(5)
    assert tp["actual"]["return_pct"] == pytest.approx(_twr([OWNER_R[n] for n in range(4, -1, -1)]), abs=1e-3)
    assert tp["ideal"]["return_pct"] == pytest.approx((PRICES[0] / PRICES[5] - 1) * 100, abs=1e-3)
    _assert_gap_arithmetic(tp)


def test_owner_starting_after_ai_moves_the_shared_start(db, wp):
    ws, p = wp
    # Owner's first row carries a return that predates its own window.
    _seed_full(db, ws, p, owner_days=range(6, -1, -1))

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["start"] == _d(6)
    assert tp["actual"]["return_pct"] == pytest.approx(_twr([OWNER_R[n] for n in range(5, -1, -1)]), abs=1e-3)
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx((PRICES[0] / PRICES[6] - 1) * 100, abs=1e-3)
    _assert_gap_arithmetic(tp)


def test_missing_observations_at_the_beginning_use_first_common_valuation(db, wp):
    """Owner lacks day 9, AI lacks day 10: the window opens at day 8, the
    first date all three observed — never at a carried-forward valuation."""
    ws, p = wp
    owner_days = [10] + list(range(8, -1, -1))
    _seed_full(db, ws, p, owner_days=owner_days, ai_days=range(9, -1, -1))

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["start"] == _d(8)
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx((PRICES[0] / PRICES[8] - 1) * 100, abs=1e-3)
    assert tp["actual"]["return_pct"] == pytest.approx(_twr([OWNER_R[n] for n in range(7, -1, -1)]), abs=1e-3)


def test_missing_observations_near_the_end_close_at_last_common_date(db, wp):
    """AI lacks day 0; the owner's day-1 row has no return (cannot close a
    window). The window closes at day 2."""
    ws, p = wp
    _seed_full(db, ws, p, ai_days=range(10, 0, -1), owner_r={**OWNER_R, 1: None})

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["end"] == _d(2)
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx((PRICES[2] / PRICES[10] - 1) * 100, abs=1e-3)
    assert tp["actual"]["return_pct"] == pytest.approx(_twr([OWNER_R[n] for n in range(9, 1, -1)]), abs=1e-3)
    _assert_gap_arithmetic(tp)


def test_only_one_shared_date_yields_no_gaps(db, wp):
    ws, p = wp
    _seed_full(db, ws, p, ai_days=[0])

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["status"] == "insufficient_overlap"
    assert tp["comparison_window"]["start"] is None and tp["comparison_window"]["end"] is None
    assert tp["gap_a"]["value"] is None
    assert tp["gap_b"]["value"] is None


def test_disjoint_dates_yield_empty_window_and_no_gaps(db, wp):
    ws, p = wp
    _seed_full(db, ws, p, owner_days=range(10, -1, -2), ai_days=range(9, 0, -2))

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["status"] == "insufficient_overlap"
    assert tp["gap_a"]["value"] is None
    assert tp["gap_b"]["value"] is None


def test_single_series_is_not_applicable_and_keeps_its_own_figure(db, wp):
    from models.database import PortfolioSnapshot

    ws, p = wp
    for n, r in ((2, None), (1, 1.0), (0, 0.0)):
        db.add(PortfolioSnapshot(workspace_id=ws.id, portfolio_id=p.id, snapshot_date=_d(n),
                                 total_value=1_000_000.0, cash_balance=0.0, investment_return_pct=r))
    db.commit()

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["status"] == "not_applicable"
    assert tp["actual"]["return_pct"] == pytest.approx(1.0, abs=1e-6)
    assert tp["gap_a"]["value"] is None and tp["gap_b"]["value"] is None


# ── 6. Corrections from Phases 4.19 / 4.20 are preserved ───────────────────

def test_ai_historical_cash_is_still_per_row(db, wp):
    """A mid-window AI rebalance moves half the equity to cash; today's
    paper_cash_balance (overwritten in place) must not shift history."""
    ws, p = wp
    _recommendation(db, ws, p)
    prices = {n: (100.0 if n > 5 else 110.0) for n in range(10, 0, -1)}
    prices[0] = 121.0
    nav = 1_000_000.0
    for n in range(10, -1, -1):
        r = None if n == 10 else 0.0
        _owner_day(db, ws, p, n, prices[n], nav, r)
    rows = [(n, 10_000, 0.0, prices[n]) for n in range(10, 5, -1)]
    rows += [(n, 5_000, 550_000.0, prices[n]) for n in range(5, -1, -1)]
    _ai_shadow(db, ws, p, rows, paper_cash_now=999_999.0)

    tp = compute_three_portfolios(db, p.id, period_days=10)

    expected = (5_000 * 121.0 + 550_000.0) / 1_000_000.0 * 100 - 100        # 15.5%
    assert tp["ai_portfolio"]["return_pct"] == pytest.approx(expected, abs=1e-6)


def test_owner_cash_flows_stay_out_of_aligned_return_and_drawdown(db, wp):
    ws, p = wp
    _recommendation(db, ws, p)
    rets = {10: 2.0, 9: 1.0, 8: 1.0, 7: 1.0, 6: 1.0, 5: 0.0, 4: -1.0, 3: -1.0, 2: -1.0, 1: -1.0, 0: -1.0}
    nav = 1_000_000.0
    for n in range(10, -1, -1):
        flow = 200_000.0 if n == 5 else None
        nav = nav * (1 + rets[n] / 100) + (flow or 0)
        _owner_day(db, ws, p, n, PRICES[n], nav, rets[n], flow=flow)
    _ai_shadow(db, ws, p, [(n, 10_000, 0.0, PRICES[n]) for n in range(10, -1, -1)])

    tp = compute_three_portfolios(db, p.id, period_days=10)

    inside = [rets[n] for n in range(9, -1, -1)]
    assert tp["actual"]["return_pct"] == pytest.approx(_twr(inside), abs=1e-3)
    assert tp["actual"]["max_drawdown_pct"] == pytest.approx(
        compute_return_index_drawdown([(None, r) for r in inside])["max_drawdown_pct"], abs=1e-4)
    assert tp["actual"]["return_pct"] < 10.0                                 # deposit not counted


def test_no_historical_rows_are_rewritten(db, wp):
    from models.database import PortfolioSnapshot, ShadowPortfolio, ShadowPortfolioSnapshot

    ws, p = wp
    _seed_full(db, ws, p, owner_days=range(10, 2, -1))

    def dump():
        cols = lambda m: [c.name for c in m.__table__.columns]  # noqa: E731
        return {m.__name__: sorted(tuple(getattr(r, c) for c in cols(m)) for r in db.query(m).all())
                for m in (PortfolioSnapshot, ShadowPortfolio, ShadowPortfolioSnapshot)}

    before = dump()
    compute_three_portfolios(db, p.id, period_days=10)
    db.expire_all()
    assert dump() == before


# ── 7. Chart follows the shared comparison window ──────────────────────────

def _assert_chart_matches_window(tp):
    """Chart bounds equal comparison_window; Ideal / AI / You start at 100 on
    the shared start and end at 100 + their headline return_pct."""
    win, chart = tp["comparison_window"], tp["chart"]
    assert win["status"] == "aligned"
    assert chart, "aligned window must draw a chart"
    assert chart[0]["date"] == win["start"]
    assert chart[-1]["date"] == win["end"]
    assert all(win["start"] <= r["date"] <= win["end"] for r in chart)
    for line, block in (("ideal", "ideal"), ("ai", "ai_portfolio"), ("actual", "actual")):
        assert chart[0][line] == pytest.approx(100.0, abs=1e-9), line
        assert chart[-1][line] - 100.0 == pytest.approx(tp[block]["return_pct"], abs=1e-3), line


def test_chart_ai_three_days_past_you_and_ideal_ends_at_window_end(db, wp):
    ws, p = wp
    _seed_full(db, ws, p, owner_days=range(10, 2, -1), ai_days=range(10, -1, -1))

    tp = compute_three_portfolios(db, p.id, period_days=10)

    _assert_chart_matches_window(tp)
    assert tp["chart"][-1]["date"] == _d(3)
    assert not any(r["date"] > _d(3) for r in tp["chart"])            # no AI-only tail
    _assert_gap_arithmetic(tp)


def test_chart_ai_starting_later_than_you_starts_at_shared_start(db, wp):
    ws, p = wp
    _seed_full(db, ws, p, ai_days=range(5, -1, -1))

    tp = compute_three_portfolios(db, p.id, period_days=10)

    _assert_chart_matches_window(tp)
    assert tp["chart"][0]["date"] == _d(5)
    # You is re-based at the shared start, not carried from the cutoff.
    assert tp["chart"][-1]["actual"] == pytest.approx(
        100 * (1 + _twr([OWNER_R[n] for n in range(4, -1, -1)]) / 100), abs=1e-3)


def test_chart_ideal_ending_before_ai_and_you_closes_at_ideal_end(db, wp):
    """Owner days 2..0 carry no prices, so the canonical archive (and Ideal)
    ends at day 3, while You and the AI shadow continue to day 0."""
    ws, p = wp
    _recommendation(db, ws, p)
    nav = 1_000_000.0
    for n in range(10, -1, -1):
        nav *= 1 + OWNER_R[n] / 100
        _owner_day(db, ws, p, n, PRICES[n], nav, OWNER_R[n], with_prices=n > 2)
    _ai_shadow(db, ws, p, [(n, 10_000, 0.0, PRICES[min(max(n, 3), 10)] if n < 3 else PRICES[n])
                           for n in range(10, -1, -1)])

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["end"] == _d(3)
    _assert_chart_matches_window(tp)
    assert tp["actual"]["return_pct"] == pytest.approx(_twr([OWNER_R[n] for n in range(9, 2, -1)]), abs=1e-3)


def test_chart_already_aligned_lines_match_previous_indexing(db, wp):
    """Ideal / AI rows are exactly the previous per-date indices (both already
    100 at the shared start); You ends at its unchanged headline."""
    ws, p = wp
    _seed_full(db, ws, p, owner_r={**OWNER_R, 10: None})

    tp = compute_three_portfolios(db, p.id, period_days=10)

    _assert_chart_matches_window(tp)
    assert [r["date"] for r in tp["chart"]] == [_d(n) for n in range(10, -1, -1)]
    for r, n in zip(tp["chart"], range(10, -1, -1)):
        assert r["ideal"] == pytest.approx(PRICES[n] / PRICES[10] * 100, abs=1e-3)
        assert r["ai"] == pytest.approx(PRICES[n] / PRICES[10] * 100, abs=1e-3)
    _assert_gap_arithmetic(tp)


def test_chart_and_headline_agree_after_excluding_first_owner_return(db, wp):
    ws, p = wp
    _seed_full(db, ws, p)                                   # day-10 owner return predates window

    tp = compute_three_portfolios(db, p.id, period_days=10)

    _assert_chart_matches_window(tp)
    running, expected = 100.0, {_d(10): 100.0}
    for n in range(9, -1, -1):
        running *= 1 + OWNER_R[n] / 100
        expected[_d(n)] = running
    for r in tp["chart"]:
        assert r["actual"] == pytest.approx(expected[r["date"]], abs=1e-3)


def test_chart_never_carries_a_missing_observation_forward(db, wp):
    """Owner has no row on day 5, so day 5 is also absent from the canonical
    price archive Ideal walks. Both lines are None there (not yesterday's
    value); the AI shadow, which has its own day-5 row, keeps its point."""
    ws, p = wp
    _seed_full(db, ws, p, owner_days=[n for n in range(10, -1, -1) if n != 5])

    tp = compute_three_portfolios(db, p.id, period_days=10)

    _assert_chart_matches_window(tp)
    day5 = next(r for r in tp["chart"] if r["date"] == _d(5))
    assert day5["actual"] is None
    assert day5["ideal"] is None
    assert day5["ai"] is not None


def test_chart_benchmark_is_bounded_and_not_forward_filled(db, wp):
    from models.database import BenchmarkPrice

    ws, p = wp
    _seed_full(db, ws, p, owner_days=range(10, 2, -1))
    for n in range(12, -1, -1):
        if n != 10:                                          # missing at the window start
            db.add(BenchmarkPrice(symbol="^SET.BK", price_date=_d(n), close_price=1000.0 + n))
    db.commit()

    tp = compute_three_portfolios(db, p.id, period_days=10)

    _assert_chart_matches_window(tp)
    rows = {r["date"]: r for r in tp["chart"]}
    assert rows[_d(10)]["benchmark"] is None
    assert rows[_d(9)]["benchmark"] == pytest.approx(100.0)  # rebased at its first in-window point
    assert not any(d > _d(3) for d in rows)


def test_no_shared_window_draws_no_comparison_chart(db, wp):
    ws, p = wp
    _seed_full(db, ws, p, owner_days=range(10, -1, -2), ai_days=range(9, 0, -2))

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["status"] == "insufficient_overlap"
    assert tp["chart"] == []
    assert tp["gap_a"]["value"] is None and tp["gap_b"]["value"] is None
    assert tp["status"] == "ok"                              # portfolio data exists; no comparison drawn


def test_single_series_chart_keeps_previous_display(db, wp):
    from models.database import PortfolioSnapshot

    ws, p = wp
    for n, r in ((2, None), (1, 1.0), (0, 0.0)):
        db.add(PortfolioSnapshot(workspace_id=ws.id, portfolio_id=p.id, snapshot_date=_d(n),
                                 total_value=1_000_000.0, cash_balance=0.0, investment_return_pct=r))
    db.commit()

    tp = compute_three_portfolios(db, p.id, period_days=10)

    assert tp["comparison_window"]["status"] == "not_applicable"
    assert [r["actual"] for r in tp["chart"]] == [pytest.approx(101.0), pytest.approx(101.0)]
