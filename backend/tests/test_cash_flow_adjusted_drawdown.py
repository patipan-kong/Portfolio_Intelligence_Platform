"""Phase 4.20 — Cash-flow-adjusted drawdown for the owner's real portfolio.

Max drawdown was measured on raw PortfolioSnapshot.total_value, which
includes deposits and withdrawals: a withdrawal read as an investment loss
and a deposit could hide a genuine one. It is now measured on the same
cash-flow-adjusted return index each module's Total Return already chains
(investment_return_pct):

    index[0] = 100;  index[t] = index[t-1] × (1 + r_t / 100)
    drawdown[t] = index[t] / max(index[0..t]) − 1

Owner-portfolio call sites covered: quant_engine.calculate_max_drawdown
(Performance page), attribution_engine._actual_portfolio_metrics (Three
Portfolios "You", Scorecard actual DD, avoided_drawdown),
human_vs_ai._portfolio_return_since (Human vs AI), timing_performance
(period DD) and human_vs_ai_timing (human DD / saved DD). AI shadow and
Ideal drawdowns are unchanged.

Synthetic data only, in-memory SQLite. Brief §6 numbering in test names.
"""
from __future__ import annotations

import os
import sys
from datetime import date, datetime, timedelta

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.analytics import quant_engine as qe  # noqa: E402
from services.analytics.attribution_engine import (  # noqa: E402
    _actual_portfolio_metrics,
    compute_max_drawdown,
    compute_owner_max_drawdown,
    compute_return_index_drawdown,
)
from services.analytics.human_vs_ai import _portfolio_return_since  # noqa: E402
from services.human_vs_ai_timing import evaluate_override  # noqa: E402
from services.timing_performance import AllocationPeriod, evaluate_period_performance  # noqa: E402


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


def _seed(db, ws, p, rows):
    """rows: [(days_ago, total_value, investment_return_pct)]. The current
    snapshot writer stores daily_return_pct = investment_return_pct."""
    from models.database import PortfolioSnapshot

    out = []
    for days_ago, nav, r in rows:
        s = PortfolioSnapshot(
            workspace_id=ws.id, portfolio_id=p.id, snapshot_date=_d(days_ago),
            total_value=nav, cash_balance=0.0, investment_return_pct=r, daily_return_pct=r,
        )
        db.add(s)
        out.append(s)
    db.commit()
    return out


def _quant(snaps):
    return qe.calculate_max_drawdown(sorted(snaps, key=lambda s: s.snapshot_date))


def _period(start_days_ago=60):
    return AllocationPeriod(
        recommendation_snapshot_id=1,
        start_date=datetime.utcnow() - timedelta(days=start_days_ago),
        end_date=None, days_active=start_days_ago, is_current=True,
    )


def _timing_dd(snaps):
    return evaluate_period_performance(_period(), snaps, {}).max_drawdown_pct


def _human_dd(snaps, shadow_snaps=()):
    return evaluate_override("REJECTED", "AAA", "BUY", 1, list(snaps), list(shadow_snaps))


def _all_owner_drawdowns(db, p, snaps):
    """Every owner-portfolio drawdown surface, positive %, None = no drawdown
    for the modules whose existing contract uses None for that."""
    q = _quant(snaps)["max_drawdown_pct"]
    _, attr_dd, _ = _actual_portfolio_metrics(snaps)
    _, hva_dd, _ = _portfolio_return_since(db, p.id, _d(400))
    return {
        "quant": None if q is None else -q,
        "attribution": attr_dd,
        "human_vs_ai": hva_dd,
        "timing_period": _timing_dd(snaps),
        "human_vs_ai_timing": _human_dd(snaps).human_drawdown_pct,
    }


def _assert_no_drawdown(dds):
    # Existing contracts: quant/timing modules report "no drawdown" as None,
    # attribution/human_vs_ai report 0.0.
    assert dds["quant"] is None
    assert dds["timing_period"] is None
    assert dds["human_vs_ai_timing"] is None
    assert dds["attribution"] == pytest.approx(0.0)
    assert dds["human_vs_ai"] == pytest.approx(0.0)


# ── 1. flat market, no flows ──────────────────────────────────────────────

def test_01_flat_market_no_flows(db, wp):
    ws, p = wp
    snaps = _seed(db, ws, p, [(n, 1_000_000.0, None if n == 10 else 0.0) for n in range(10, -1, -1)])
    _assert_no_drawdown(_all_owner_drawdowns(db, p, snaps))


# ── 2. flat market + 30% withdrawal ───────────────────────────────────────

def test_02_flat_market_withdrawal_is_not_a_drawdown(db, wp):
    ws, p = wp
    rows = [(n, 1_000_000.0 if n > 5 else 700_000.0, None if n == 10 else 0.0) for n in range(10, -1, -1)]
    snaps = _seed(db, ws, p, rows)

    assert compute_max_drawdown([r[1] for r in rows]) == pytest.approx(30.0)  # pre-fix raw NAV
    _assert_no_drawdown(_all_owner_drawdowns(db, p, snaps))


# ── 3. flat market + deposit ──────────────────────────────────────────────

def test_03_flat_market_deposit(db, wp):
    ws, p = wp
    rows = [(n, 1_000_000.0 if n > 5 else 1_400_000.0, None if n == 10 else 0.0) for n in range(10, -1, -1)]
    _assert_no_drawdown(_all_owner_drawdowns(db, p, _seed(db, ws, p, rows)))


# ── 4. genuine −20% return masked by a deposit ────────────────────────────

def test_04_deposit_cannot_hide_a_genuine_drawdown(db, wp):
    ws, p = wp
    # Day 5: market −20% (1.0M → 0.8M) and a same-period 250k deposit →
    # raw NAV rises to 1.05M; investment_return_pct correctly says −20%.
    rows = ([(n, 1_000_000.0, None if n == 10 else 0.0) for n in range(10, 5, -1)]
            + [(5, 1_050_000.0, -20.0)]
            + [(n, 1_050_000.0, 0.0) for n in range(4, -1, -1)])
    snaps = _seed(db, ws, p, rows)

    assert compute_max_drawdown([r[1] for r in rows]) == pytest.approx(0.0)  # pre-fix: hidden
    dds = _all_owner_drawdowns(db, p, snaps)
    assert all(v == pytest.approx(20.0) for v in dds.values()), dds

    q = _quant(snaps)
    assert q["peak_date"] == _d(6)
    assert q["trough_date"] == _d(5)
    assert q["recovery_date"] is None
    assert q["duration_days"] == 1  # peak → trough while unrecovered (unchanged rule)


# ── 5. +10%, −15%, +20%: peak, trough, recovery ───────────────────────────

def test_05_peak_trough_recovery_from_the_index(db, wp):
    ws, p = wp
    # index 100 → 110 → 93.5 → 112.2; NAVs carry unrelated flows.
    rows = [(9, 1_000_000.0, None), (6, 2_100_000.0, 10.0), (4, 500_000.0, -15.0), (1, 900_000.0, 20.0)]
    snaps = _seed(db, ws, p, rows)

    q = _quant(snaps)
    assert q["max_drawdown_pct"] == pytest.approx(-15.0)
    assert (q["peak_date"], q["trough_date"], q["recovery_date"]) == (_d(6), _d(4), _d(1))
    assert q["duration_days"] == 5  # peak (day −6) → recovery (day −1)
    assert all(v == pytest.approx(15.0) for v in _all_owner_drawdowns(db, p, snaps).values())

    res = compute_return_index_drawdown([("a", 10.0), ("b", -15.0), ("c", 20.0)], base_date="base")
    assert [round(v, 4) for _, v in res["index"]] == [100.0, 110.0, 93.5, 112.2]
    assert (res["peak_date"], res["trough_date"], res["recovery_date"]) == ("a", "b", "c")


def test_05b_drawdown_from_the_base_point(db, wp):
    ws, p = wp
    snaps = _seed(db, ws, p, [(3, 1_000_000.0, None), (2, 900_000.0, -10.0), (1, 900_000.0, 0.0)])
    q = _quant(snaps)
    assert (q["max_drawdown_pct"], q["peak_date"], q["trough_date"]) == (-10.0, _d(3), _d(2))


# ── 6. multiple deposits/withdrawals between snapshots ────────────────────

def test_06_multiple_flows_between_snapshots(db, wp):
    ws, p = wp
    # NAV swings from several flows; returns are what investment produced.
    rows = [(5, 1_000_000.0, None), (4, 1_520_000.0, 2.0), (3, 810_000.0, 0.0),
            (2, 1_300_000.0, -3.0), (1, 400_000.0, 1.0)]
    snaps = _seed(db, ws, p, rows)
    expected = (1 - (1.02 * 0.97) / 1.02) * 100  # 3.0%

    assert compute_max_drawdown([r[1] for r in rows]) > 70  # raw NAV nonsense
    assert all(v == pytest.approx(expected, abs=1e-3) for v in _all_owner_drawdowns(db, p, snaps).values())


# ── 7. missing snapshot dates ─────────────────────────────────────────────

def test_07_missing_dates_use_calendar_dates_of_observations(db, wp):
    ws, p = wp
    snaps = _seed(db, ws, p, [(30, 1e6, None), (21, 1e6, 5.0), (12, 1e6, -10.0), (2, 1e6, 6.0)])
    q = _quant(snaps)
    assert q["max_drawdown_pct"] == pytest.approx(-10.0)
    assert (q["peak_date"], q["trough_date"], q["recovery_date"]) == (_d(21), _d(12), None)
    assert q["duration_days"] == 9


# ── 8. zero investment return ─────────────────────────────────────────────

def test_08_zero_returns_are_observations(db, wp):
    ws, p = wp
    snaps = _seed(db, ws, p, [(4, 1e6, None), (3, 1e6, 10.0), (2, 2e6, 0.0), (1, 5e5, 0.0), (0, 1e6, -10.0)])
    q = _quant(snaps)
    assert q["max_drawdown_pct"] == pytest.approx(-10.0)
    assert q["peak_date"] == _d(1)  # equal highs: latest one (unchanged rule)
    assert all(v == pytest.approx(10.0) for v in _all_owner_drawdowns(db, p, snaps).values())


# ── 9. incomplete or invalid observations ─────────────────────────────────

def test_09a_missing_returns_match_the_twr_chain(db, wp):
    """A row without a return is not an observation in the TWR, so it is not
    one in the drawdown either: the index ends exactly at 100 + TWR."""
    ws, p = wp
    snaps = _seed(db, ws, p, [(4, 1e6, None), (3, 1e6, -10.0), (2, 1.5e6, None), (1, 1e6, 5.0)])
    twr, dd, _ = _actual_portfolio_metrics(snaps)
    res = compute_return_index_drawdown([(s.snapshot_date, s.investment_return_pct)
                                         for s in snaps if s.investment_return_pct is not None])
    assert res["index"][-1][1] == pytest.approx(100 + twr)
    assert dd == pytest.approx(10.0)


def test_09b_impossible_return_is_unknown_not_fabricated(db, wp):
    assert compute_return_index_drawdown([("a", 5.0), ("b", -150.0)]) is None
    assert compute_return_index_drawdown([("a", float("nan"))]) is None
    assert compute_return_index_drawdown([("a", "bad")]) is None
    assert compute_return_index_drawdown([]) is None
    assert compute_owner_max_drawdown([5.0, -150.0], [1e6, 1e6, 1e6]) is None

    ws, p = wp
    snaps = _seed(db, ws, p, [(3, 1e6, None), (2, 1e6, -150.0), (1, 1e6, 0.0)])
    assert _quant(snaps)["max_drawdown_pct"] is None  # shown as "—", not 0
    _, dd, _ = _actual_portfolio_metrics(snaps)
    assert dd is None


def _dict_snap(days_ago, nav, r):
    return {"snapshot_date": _d(days_ago), "total_value": nav,
            "investment_return_pct": r, "daily_return_pct": r}


def _score(snaps, bench_map=None):
    from services.timing_score import calculate_timing_score

    perf = evaluate_period_performance(_period(), snaps, bench_map or {})
    return perf, calculate_timing_score(perf)


# Raw NAV falls 30% through a withdrawal; the investment returns are flat.
_WITHDRAWAL = [(4, 1e6, 0.0), (3, 1e6, 0.0), (2, 7e5, 0.0), (1, 7e5, 0.0)]


def test_09c1_valid_zero_returns_give_zero_drawdown_and_the_existing_bonus():
    snaps = [_dict_snap(*r) for r in _WITHDRAWAL[:1] + [(3, 1e6, 0.0), (2, 1e6, 0.0)]]
    perf, score = _score(snaps)
    assert perf.max_drawdown_pct is None          # existing "never fell" value
    assert perf.return_evidence_valid is True
    assert score.drawdown_component == 15.0       # unchanged valid behavior
    assert _human_dd(snaps).human_drawdown_pct is None


def test_09c2_flat_market_withdrawal_is_zero_drawdown_in_timing():
    snaps = [_dict_snap(*r) for r in _WITHDRAWAL]
    perf, score = _score(snaps)
    assert perf.max_drawdown_pct is None and perf.return_evidence_valid is True
    assert score.drawdown_component == 15.0
    assert _human_dd(snaps).human_drawdown_pct is None


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_09c3_invalid_current_return_never_falls_back_to_raw_nav(bad):
    """Raw NAV would show the 30% withdrawal as a drawdown; an invalid return
    must make the drawdown unavailable instead of using that raw basis."""
    rows = [(4, 1e6, 0.0), (3, 1e6, 0.0), (2, 7e5, bad), (1, 7e5, 0.0)]
    snaps = [_dict_snap(*r) for r in rows]
    from services.timing_performance import _drawdown_evidence

    assert _drawdown_evidence(snaps) == (None, False)
    hv = _human_dd(snaps, [_dict_snap(4, 1e6, 0.0), _dict_snap(2, 9e5, -10.0)])
    assert hv.human_drawdown_pct is None
    assert hv.ai_drawdown_pct == pytest.approx(10.0)
    assert hv.saved_drawdown_pct is None          # no saved-drawdown credit


def test_09c3b_non_numeric_return_is_unavailable_in_the_drawdown_helpers():
    # (Float columns cannot hold strings; the existing _twr would raise
    # first. Checked at the drawdown layer only.)
    from services.human_vs_ai_timing import _owner_max_drawdown
    from services.timing_performance import _drawdown_evidence

    snaps = [_dict_snap(3, 1e6, 0.0), _dict_snap(2, 7e5, "n/a")]
    assert _drawdown_evidence(snaps) == (None, False)
    assert _owner_max_drawdown(snaps) is None


def test_09c4_return_below_minus_100_is_rejected_as_unavailable():
    snaps = [_dict_snap(3, 1e6, 0.0), _dict_snap(2, 8e5, -150.0)]
    perf = evaluate_period_performance(_period(), snaps, {})
    assert perf.max_drawdown_pct is None
    assert perf.return_evidence_valid is False
    assert _human_dd(snaps).human_drawdown_pct is None   # was raw 20.0 before
    # Exactly −100% is a possible (total) loss, not invalid.
    perf_total = evaluate_period_performance(
        _period(), [_dict_snap(3, 1e6, 0.0), _dict_snap(2, 1.0, -100.0)], {})
    assert perf_total.max_drawdown_pct == pytest.approx(100.0)
    assert perf_total.return_evidence_valid is True


def test_09c5_unavailable_drawdown_gets_no_timing_score_bonus():
    """Two impossible returns chain to a +300% period return and None
    drawdown: before, +30 excess and +15 drawdown bonuses. Now neutral."""
    snaps = [_dict_snap(3, 1e6, -300.0), _dict_snap(2, 1e6, -300.0)]
    bench = {_d(3): 100.0, _d(1): 100.0}
    perf, score = _score(snaps, bench)
    assert perf.return_evidence_valid is False
    assert perf.max_drawdown_pct is None
    assert score.drawdown_component == 0.0
    assert score.excess_return_component == 0.0
    # Same period with valid flat returns keeps the normal bonus.
    ok_perf, ok_score = _score([_dict_snap(3, 1e6, 0.0), _dict_snap(2, 1e6, 0.0)], bench)
    assert ok_score.drawdown_component == 15.0
    assert ok_score.timing_score == score.timing_score + 15
    # The internal flag never reaches serialized output.
    assert "return_evidence_valid" not in perf.model_dump()
    assert "return_evidence_valid" not in perf.model_dump_json()


def test_09c6_legacy_window_without_returns_keeps_raw_nav_compatibility():
    rows = [(4, 1e6, None), (3, 1.1e6, None), (2, 9.9e5, None)]
    snaps = [_dict_snap(*r) for r in rows]
    perf, score = _score(snaps)
    assert perf.max_drawdown_pct == pytest.approx(10.0)
    assert perf.return_evidence_valid is True
    assert score.drawdown_component == 0.0        # 10% tier, as before
    assert _human_dd(snaps).human_drawdown_pct == pytest.approx(10.0)
    rising = [_dict_snap(3, 1e6, None), _dict_snap(2, 1.1e6, None)]
    assert _score(rising)[1].drawdown_component == 15.0   # existing legacy bonus


def test_09c7_valid_timing_scenario_scores_unchanged():
    """+10 / −15 / +20: 15% drawdown → −10 tier; excess and duration as before."""
    snaps = [_dict_snap(5, 1e6, None), _dict_snap(4, 1.1e6, 10.0),
             _dict_snap(3, 9.35e5, -15.0), _dict_snap(2, 1.122e6, 20.0)]
    bench = {_d(5): 100.0, _d(1): 110.0}
    perf, score = _score(snaps, bench)
    assert perf.return_evidence_valid is True
    assert perf.max_drawdown_pct == pytest.approx(15.0)
    assert perf.period_return_pct == pytest.approx(12.2)
    assert perf.excess_return_pct == pytest.approx(2.2)
    assert score.drawdown_component == -10.0
    assert score.excess_return_component == pytest.approx(8.8)
    assert score.duration_component == 10.0
    assert score.timing_score == round(50 + 8.8 - 10 + 10)


def test_09d_legacy_rows_without_returns_keep_raw_nav_fallback(db, wp):
    """No return observation at all (pre-Phase-3B.8 rows): Total Return falls
    back to raw NAV, and drawdown follows the same basis, as before."""
    ws, p = wp
    snaps = _seed(db, ws, p, [(3, 1e6, None), (2, 9e5, None), (1, 9.5e5, None)])
    _, dd, _ = _actual_portfolio_metrics(snaps)
    assert dd == pytest.approx(10.0)
    assert _quant(snaps)["max_drawdown_pct"] == pytest.approx(-10.0)


def test_09e_non_finite_quant_returns_are_dropped_like_the_twr():
    class S:
        def __init__(self, d, r):
            self.snapshot_date, self.investment_return_pct, self.daily_return_pct = d, r, r
            self.total_value, self.cash_balance, self.total_invested = 1e6, 0.0, 0.0
            self.sector_breakdown_json = self.holdings_json = None

    snaps = [S(_d(4), None), S(_d(3), 10.0), S(_d(2), float("inf")), S(_d(1), -10.0)]
    assert qe.calculate_max_drawdown(snaps)["max_drawdown_pct"] == pytest.approx(-10.0)


# ── 10. negative NAV / impossible source values ───────────────────────────

def test_10_non_positive_nav_rows_and_total_loss(db, wp):
    ws, p = wp
    # Rows with total_value <= 0 are excluded from the TWR and so from DD.
    snaps = _seed(db, ws, p, [(3, 1e6, None), (2, -5e5, -60.0), (1, 0.0, -40.0), (0, 1e6, 0.0)])
    _, dd, _ = _actual_portfolio_metrics(snaps)
    assert dd == pytest.approx(0.0)
    # A genuine −100% observation is a 100% drawdown, not filtered away.
    assert compute_return_index_drawdown([("a", -100.0)])["max_drawdown_pct"] == pytest.approx(100.0)


# ── Cross-page consistency ────────────────────────────────────────────────

def test_xp_every_owner_surface_agrees_including_three_portfolios_and_scorecard(db, wp):
    import models.database as mdb
    from services.evaluation.ideal_series import compute_three_portfolios
    from services.analytics.attribution_engine import compute_portfolio_attribution

    ws, p = wp
    rows = ([(n, 1_000_000.0, None if n == 20 else 0.5) for n in range(20, 12, -1)]
            + [(12, 600_000.0, -12.0)]                       # −12% plus a withdrawal
            + [(n, 900_000.0, 1.0) for n in range(11, -1, -1)])  # recovery + deposit
    snaps = _seed(db, ws, p, rows)

    dds = _all_owner_drawdowns(db, p, snaps)
    att = compute_portfolio_attribution(db, p.id, 30)["actual"]["max_drawdown_pct"]
    you = compute_three_portfolios(db, p.id, 30)["actual"]["max_drawdown_pct"]
    expected = 12.0
    for name, v in {**dds, "attribution_api": att, "three_portfolios_you": you}.items():
        assert v == pytest.approx(expected, abs=1e-3), name

    if str(mdb.engine.url).startswith("sqlite"):  # compute_scorecard imports main
        from services.evaluation.scorecard import compute_scorecard
        from models.database import OptimizerHistory, RecommendationSnapshot

        oh = OptimizerHistory(workspace_id=ws.id, portfolio_id=p.id, portfolio_name="P1",
                              analyzed_at=datetime.utcnow(), swap_count=0, result_json="{}")
        db.add(oh)
        db.commit()
        db.add(RecommendationSnapshot(workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=p.id,
                                      total_portfolio_value=1e6, projected_allocations_json="[]",
                                      created_at=datetime.utcnow() - timedelta(days=25)))
        db.commit()
        sc = compute_scorecard(db, p.id, 30)
        assert sc["outcome"]["max_drawdown_pct"]["actual"] == pytest.approx(expected, abs=1e-3)


def test_xp_avoided_drawdown_no_longer_credits_a_withdrawal(db, wp):
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot
    from services.analytics.attribution_engine import compute_portfolio_attribution

    ws, p = wp
    _seed(db, ws, p, [(n, 1_000_000.0 if n > 5 else 700_000.0, None if n == 10 else 0.0)
                      for n in range(10, -1, -1)])
    sh = ShadowPortfolio(workspace_id=ws.id, portfolio_id=p.id, shadow_type="STATIC_FROZEN",
                         name="S", inception_date=_d(10), inception_value=1e6,
                         inception_holdings_json="[]", paper_cash_balance=0.0, is_active=True,
                         created_at=datetime.utcnow())
    db.add(sh)
    db.commit()
    for n in range(10, -1, -1):
        db.add(ShadowPortfolioSnapshot(shadow_portfolio_id=sh.id, snapshot_date=_d(n),
                                       total_value=1e6, daily_return_pct=0.0, created_at=datetime.utcnow()))
    db.commit()

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["actual"]["max_drawdown_pct"] == pytest.approx(0.0)
    assert att["avoided_drawdown_pct"] == pytest.approx(0.0)  # pre-fix: 0 − 30 = −30


def test_xp_ai_shadow_drawdowns_unchanged(db, wp):
    """AI shadows are paper portfolios without external flows: their
    drawdown stays on persisted total_value, exactly as before."""
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot
    from services.analytics.attribution_engine import compute_portfolio_attribution

    ws, p = wp
    _seed(db, ws, p, [(n, 1e6, None if n == 6 else 0.0) for n in range(6, -1, -1)])
    sh = ShadowPortfolio(workspace_id=ws.id, portfolio_id=p.id, shadow_type="ACTIVE_MODEL",
                         name="AI", inception_date=_d(6), inception_value=1e6,
                         inception_holdings_json="[]", paper_cash_balance=0.0, is_active=True,
                         created_at=datetime.utcnow())
    db.add(sh)
    db.commit()
    navs = {6: 1e6, 5: 1.1e6, 4: 0.88e6, 3: 0.95e6, 2: 1.0e6, 1: 1.05e6, 0: 1.12e6}
    shadow_rows = []
    for n, v in navs.items():
        row = ShadowPortfolioSnapshot(shadow_portfolio_id=sh.id, snapshot_date=_d(n), total_value=v,
                                      daily_return_pct=0.0, created_at=datetime.utcnow())
        db.add(row)
        shadow_rows.append(row)
    db.commit()

    raw = compute_max_drawdown(list(navs.values()))  # 20%
    att = compute_portfolio_attribution(db, p.id, 30)
    assert att["ai_model_shadow"]["max_drawdown_pct"] == pytest.approx(raw)
    shadow_dicts = [{"snapshot_date": r.snapshot_date, "total_value": r.total_value,
                     "daily_return_pct": 0.0} for r in shadow_rows]
    assert _human_dd([], shadow_dicts).ai_drawdown_pct == pytest.approx(raw)
