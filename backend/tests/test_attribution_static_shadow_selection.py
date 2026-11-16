"""Phase 4.22 — Attribution STATIC_FROZEN selection integrity.

compute_portfolio_attribution used to take the newest-created active
STATIC_FROZEN shadow of either family. That was usually a shadow created
today with 0–1 valuations, whose empty drawdown (0.0) turned
avoided_drawdown_pct into −(owner drawdown). These tests pin the corrected
selection (_select_static_shadow) and missing-evidence handling:

   1. Newest STATIC_FROZEN with one valuation is not selected.
   2. Newest shadow is recommendation-keyed: never selected.
   3. Eligible decision shadow existing before the window start is selected.
   4. Decision shadow starting after the window start is rejected.
   5. Enough rows but no start coverage → rejected (small calendar gap ok).
   6. Start coverage but no end coverage → rejected (small calendar gap ok).
   7. No eligible shadow → static_shadow None, avoided None.
   8. Valid zero drawdown is preserved (0.0, not None).
   9. Missing drawdown evidence (invalid NAV rows / owner < 2 rows) → None.
  10. Several eligible decision shadows → deterministic tie-breaking.
  11. Portfolios are isolated.
  12. 7D / 30D / 90D can select different shadows.
  13. ACTIVE_MODEL figures unchanged.
  14. Human-vs-AI and horizon-grader shadow selection unchanged.
  15. Response keys and nullable conventions retained.

Synthetic data on in-memory SQLite only.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime, timedelta

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.analytics.attribution_engine import (  # noqa: E402
    _get_shadow_snapshots,
    _safe_return,
    _shadow_portfolio_metrics,
    compute_portfolio_attribution,
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


def _portfolio(db, name="P1"):
    from models.database import Workspace, Portfolio

    ws = db.query(Workspace).first()
    if ws is None:
        ws = Workspace(name="Test")
        db.add(ws)
        db.commit()
    p = Portfolio(workspace_id=ws.id, name=name, cash_balance=0.0)
    db.add(p)
    db.commit()
    return ws, p


@pytest.fixture()
def wp(db):
    return _portfolio(db)


def _d(days_ago: int) -> str:
    return (date.today() - timedelta(days=days_ago)).isoformat()


def _owner(db, ws, p, days, nav=None):
    """Owner snapshots on `days` (days-ago). nav: {days_ago: value}, default flat 1e6."""
    from models.database import PortfolioSnapshot

    prev = None
    for n in sorted(days, reverse=True):
        v = (nav or {}).get(n, 1_000_000.0)
        r = None if prev is None else round((v / prev - 1) * 100, 6)
        db.add(PortfolioSnapshot(workspace_id=ws.id, portfolio_id=p.id, snapshot_date=_d(n),
                                 total_value=v, cash_balance=0.0,
                                 investment_return_pct=r, daily_return_pct=r))
        prev = v
    db.commit()


def _snapshot(db, ws, p, created_days_ago=0):
    from models.database import OptimizerHistory, RecommendationSnapshot

    oh = OptimizerHistory(workspace_id=ws.id, portfolio_id=p.id, portfolio_name=p.name,
                          analyzed_at=datetime.utcnow(), swap_count=0, result_json="{}")
    db.add(oh)
    db.commit()
    rs = RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=p.id,
        total_portfolio_value=1_000_000.0,
        projected_allocations_json=json.dumps([{"symbol": "AAA", "action": "BUY", "target_weight": 100.0}]),
        created_at=datetime.utcnow() - timedelta(days=created_days_ago))
    db.add(rs)
    db.commit()
    return rs


def _decision(db, ws, p, rs, decision="APPROVED", days_ago=0):
    from models.database import UserExecutionDecision

    dec = UserExecutionDecision(workspace_id=ws.id, recommendation_snapshot_id=rs.id, portfolio_id=p.id,
                                decision=decision,
                                executed_at=datetime.utcnow() - timedelta(days=days_ago))
    db.add(dec)
    db.commit()
    return dec


def _shadow(db, ws, p, inception, valued, nav=None, kind="decision", created_days_ago=None):
    """Shadow with inception `inception` (days ago) and valuations on `valued`
    (days ago). kind: "decision" | "recommendation" (STATIC_FROZEN) | "active"."""
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot

    rs = _snapshot(db, ws, p, created_days_ago=inception)
    dec_id = _decision(db, ws, p, rs, days_ago=inception).id if kind == "decision" else None
    created = datetime.utcnow() - timedelta(days=inception if created_days_ago is None else created_days_ago)
    sh = ShadowPortfolio(workspace_id=ws.id, portfolio_id=p.id,
                         shadow_type="ACTIVE_MODEL" if kind == "active" else "STATIC_FROZEN",
                         name=f"{kind}@{inception}", inception_date=_d(inception),
                         inception_value=1_000_000.0, recommendation_snapshot_id=rs.id,
                         execution_decision_id=dec_id, inception_holdings_json="[]",
                         paper_cash_balance=0.0, is_active=True, created_at=created)
    db.add(sh)
    db.commit()
    prev = None
    for n in sorted(valued, reverse=True):
        v = (nav or {}).get(n, 1_000_000.0)
        r = None if prev is None or prev <= 0 or v <= 0 else round((v / prev - 1) * 100, 6)
        db.add(ShadowPortfolioSnapshot(shadow_portfolio_id=sh.id, snapshot_date=_d(n), total_value=v,
                                       return_pct_since_inception=round((v / 1e6 - 1) * 100, 6),
                                       daily_return_pct=r, created_at=datetime.utcnow()))
        prev = v
    db.commit()
    return sh


def _dip(start, low_day, high=1_000_000.0, low=900_000.0):
    """NAV path: flat `high`, single dip to `low` on low_day."""
    return {n: (low if n == low_day else high) for n in range(start, -1, -1)}


# 30-day owner window with a 5% drawdown on day 10.
OWNER_30 = {n: (950_000.0 if n == 10 else 1_000_000.0) for n in range(30, -1, -1)}


# ── 1–4: family / creation-date selection ─────────────────────────────────

def test_1_newest_one_row_shadow_is_not_selected(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    old = _shadow(db, ws, p, 35, range(35, -1, -1), _dip(35, 12))
    _shadow(db, ws, p, 0, [0])  # created today, inception-only valuation

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"]["shadow_id"] == old.id
    assert att["static_shadow"]["max_drawdown_pct"] == pytest.approx(10.0)
    assert att["avoided_drawdown_pct"] == pytest.approx(10.0 - 5.0)


def test_2_recommendation_keyed_shadow_never_selected(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    dec = _shadow(db, ws, p, 40, range(40, -1, -1))
    # recommendation shadow: newer inception, full coverage — still not eligible
    _shadow(db, ws, p, 31, range(31, -1, -1), _dip(31, 5), kind="recommendation")

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"]["shadow_id"] == dec.id


def test_2b_only_recommendation_shadows_gives_unavailable(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 31, range(31, -1, -1), kind="recommendation")

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"] is None
    assert att["avoided_drawdown_pct"] is None
    assert att["static_shadow_selection"]["status"] == "no_decision_shadow"


def test_3_decision_shadow_before_window_start_is_selected(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    sh = _shadow(db, ws, p, 30, range(30, -1, -1), _dip(30, 3, low=970_000.0))

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"]["shadow_id"] == sh.id
    assert att["static_shadow_selection"] == {
        "status": "selected", "shadow_id": sh.id, "inception_date": _d(30),
        "first_valuation": _d(30), "last_valuation": _d(0)}
    assert att["avoided_drawdown_pct"] == pytest.approx(3.0 - 5.0)


def test_4_decision_shadow_starting_after_window_start_is_rejected(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 29, range(29, -1, -1))  # one day too young for 30D

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"] is None
    assert att["avoided_drawdown_pct"] is None
    assert att["static_shadow_selection"]["status"] == "no_eligible_shadow"


# ── 5–6: valuation coverage ───────────────────────────────────────────────

def test_5_rows_without_start_coverage_are_rejected(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    # existed before the window, but valuations only resume 10 days in
    _shadow(db, ws, p, 40, range(20, -1, -1))

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"] is None
    assert att["avoided_drawdown_pct"] is None


def test_5b_weekend_sized_start_gap_is_tolerated(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    sh = _shadow(db, ws, p, 40, [n for n in range(40, -1, -1) if n not in (30, 29, 28)])

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"]["shadow_id"] == sh.id
    assert att["static_shadow_selection"]["first_valuation"] == _d(27)


def test_6_start_coverage_without_end_coverage_is_rejected(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 35, range(35, 9, -1))  # valuations stop 10 days before owner end

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"] is None
    assert att["avoided_drawdown_pct"] is None


def test_6b_small_end_gap_tolerated_and_rows_after_owner_end_ignored(db, wp):
    ws, p = wp
    # owner last snapshot 3 days ago; shadow last valued 5 days ago, then a crash today
    _owner(db, ws, p, range(30, 2, -1))
    nav = {n: 1_000_000.0 for n in range(35, -1, -1)}
    nav[0] = 500_000.0
    sh = _shadow(db, ws, p, 35, [n for n in range(35, -1, -1) if n not in (4, 3, 2, 1)], nav)

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"]["shadow_id"] == sh.id
    assert att["static_shadow_selection"]["last_valuation"] == _d(5)
    # today's −50% row lies after the owner's window end and is excluded
    assert att["static_shadow"]["max_drawdown_pct"] == pytest.approx(0.0)
    assert att["static_shadow"]["return_pct"] == pytest.approx(0.0)


# ── 7–9: missing vs genuine zero ──────────────────────────────────────────

def test_7_no_shadow_at_all(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"] is None
    assert att["avoided_drawdown_pct"] is None
    assert att["static_shadow_selection"]["status"] == "no_decision_shadow"
    assert att["status"] == "no_shadows"


def test_8_valid_zero_drawdown_is_preserved(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1))  # flat owner: genuine 0 drawdown
    _shadow(db, ws, p, 30, range(30, -1, -1))  # flat shadow: genuine 0 drawdown

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"]["max_drawdown_pct"] == 0.0
    assert att["avoided_drawdown_pct"] == 0.0


def test_9_invalid_nav_rows_are_not_evidence(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    nav = {n: 0.0 for n in range(30, -1, -1)}
    nav[30] = 1_000_000.0  # only one positive-NAV valuation
    _shadow(db, ws, p, 30, range(30, -1, -1), nav)

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"] is None
    assert att["avoided_drawdown_pct"] is None


def test_9b_owner_with_one_snapshot_gives_no_avoided_drawdown(db, wp):
    ws, p = wp
    _owner(db, ws, p, [0])
    _shadow(db, ws, p, 30, range(30, -1, -1))

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["avoided_drawdown_pct"] is None


# ── 10–12: tie-breaking, isolation, windows ───────────────────────────────

def test_10_deterministic_choice_among_eligible(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 45, range(45, -1, -1))
    # same inception date: later created_at wins (then higher id)
    a = _shadow(db, ws, p, 35, range(35, -1, -1), created_days_ago=34)
    b = _shadow(db, ws, p, 35, range(35, -1, -1), created_days_ago=35)

    first = compute_portfolio_attribution(db, p.id, 30)["static_shadow"]["shadow_id"]
    second = compute_portfolio_attribution(db, p.id, 30)["static_shadow"]["shadow_id"]

    assert first == second == a.id != b.id


def test_10b_falls_back_to_older_eligible_when_newest_lacks_coverage(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    older = _shadow(db, ws, p, 45, range(45, -1, -1))
    _shadow(db, ws, p, 32, range(32, 15, -1))  # newer inception, valuations stopped

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"]["shadow_id"] == older.id


def test_11_portfolios_are_isolated(db, wp):
    ws, p = wp
    _, other = _portfolio(db, "P2")
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _owner(db, ws, other, range(30, -1, -1))
    _shadow(db, ws, other, 40, range(40, -1, -1), _dip(40, 4))

    att = compute_portfolio_attribution(db, p.id, 30)

    assert att["static_shadow"] is None
    assert att["avoided_drawdown_pct"] is None


def test_12_windows_select_different_shadows(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(90, -1, -1))
    s90 = _shadow(db, ws, p, 90, range(90, -1, -1))
    s30 = _shadow(db, ws, p, 30, range(30, -1, -1))
    s7 = _shadow(db, ws, p, 7, range(7, -1, -1))
    _shadow(db, ws, p, 0, [0])

    picked = {w: compute_portfolio_attribution(db, p.id, w)["static_shadow"]["shadow_id"]
              for w in (7, 30, 90)}

    assert picked == {7: s7.id, 30: s30.id, 90: s90.id}


# ── 13–15: unchanged consumers and contract ───────────────────────────────

def test_13_active_model_figures_unchanged(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    ai = _shadow(db, ws, p, 3, range(3, -1, -1), {3: 1e6, 2: 1.02e6, 1: 0.99e6, 0: 1.01e6}, kind="active")
    _shadow(db, ws, p, 35, range(35, -1, -1))

    att = compute_portfolio_attribution(db, p.id, 30)
    r, dd, v = _shadow_portfolio_metrics(_get_shadow_snapshots(db, ai.id, _d(30)))

    assert att["ai_model_shadow"] == {"shadow_id": ai.id, "return_pct": _safe_return(r),
                                      "max_drawdown_pct": dd, "annualized_volatility": v}
    assert att["regret_score"] == pytest.approx(round(_safe_return(r) - att["actual"]["return_pct"], 4))
    assert att["static_shadow"]["shadow_id"] != ai.id


def test_14a_human_vs_ai_still_uses_decision_linked_shadow(db, wp):
    from services.analytics.human_vs_ai import compare_human_vs_ai

    ws, p = wp
    _owner(db, ws, p, range(10, -1, -1))
    young = _shadow(db, ws, p, 2, range(2, -1, -1))  # too young for a 30D attribution window

    out = compare_human_vs_ai(db, p.id, 30)

    assert [d["shadow_id"] for d in out["decisions"]] == [young.id]
    assert compute_portfolio_attribution(db, p.id, 30)["static_shadow"] is None


def test_14b_horizon_grader_still_reads_recommendation_shadow(db, wp):
    from models.database import RecommendationGrade, Settings, ShadowPortfolio, ShadowPortfolioSnapshot
    from services.evaluation.horizon_grader import grade_due_recommendations

    ws, p = wp
    db.add(Settings(workspace_id=ws.id, key="evaluation_settings",
                    value=json.dumps({"horizons_days": [7]})))
    db.commit()
    rec = _shadow(db, ws, p, 7, range(7, -1, -1),
                  {n: 1_000_000.0 + (7 - n) * 10_000 for n in range(8)}, kind="recommendation")
    # decision shadow on the same recommendation, with a very different path
    dec = ShadowPortfolio(workspace_id=ws.id, portfolio_id=p.id, shadow_type="STATIC_FROZEN", name="d",
                          inception_date=_d(7), inception_value=1e6,
                          recommendation_snapshot_id=rec.recommendation_snapshot_id,
                          execution_decision_id=_decision(db, ws, p, rec.recommendation_snapshot).id,
                          inception_holdings_json="[]", paper_cash_balance=0.0, is_active=True,
                          created_at=datetime.utcnow())
    db.add(dec)
    db.commit()
    for n in range(7, -1, -1):
        db.add(ShadowPortfolioSnapshot(shadow_portfolio_id=dec.id, snapshot_date=_d(n), total_value=5e5,
                                       return_pct_since_inception=-50.0, created_at=datetime.utcnow()))
    db.commit()

    result = grade_due_recommendations(db, portfolio_id=p.id)

    assert [g["grade_kind"] for g in result["graded"]] == ["H7"]
    grade = db.query(RecommendationGrade).one()
    assert grade.return_pct == pytest.approx(7.0)  # recommendation shadow's +7%, not −50%
    assert result["deactivated"] == [rec.id]


def test_15_response_keys_and_nullability(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 0, [0])  # only a too-young decision shadow

    att = compute_portfolio_attribution(db, p.id, 30)

    assert {"portfolio_id", "evaluation_window_days", "period_start", "period_end", "status",
            "data_points_available", "required_days_remaining", "has_sufficient_history", "actual",
            "static_shadow", "ai_model_shadow", "avoided_drawdown_pct", "regret_score",
            "ai_outperformed", "interpretation", "computed_at"} <= set(att)
    assert att["static_shadow"] is None  # nullable object, as before
    assert att["avoided_drawdown_pct"] is None
    assert set(att["static_shadow_selection"]) == {"status", "shadow_id", "inception_date",
                                                   "first_valuation", "last_valuation"}
    # a decision shadow exists but cannot support the window yet → not "no_shadows"
    assert att["status"] == "shadows_pending_valuation"

    _shadow(db, ws, p, 31, range(31, -1, -1))
    full = compute_portfolio_attribution(db, p.id, 30)
    assert set(full["static_shadow"]) == {"shadow_id", "return_pct", "max_drawdown_pct",
                                          "annualized_volatility"}
    assert full["status"] == "ok"


# ── Window-scaled edge tolerance: min(5, window_days // 5) ────────────────
OWNER_7 = {n: (950_000.0 if n == 3 else 1_000_000.0) for n in range(7, -1, -1)}


def test_tolerance_scales_with_window():
    from services.analytics.attribution_engine import _edge_tolerance_days

    assert [_edge_tolerance_days(w) for w in (7, 30, 90)] == [1, 5, 5]


def test_w1_7d_shadow_with_only_last_two_valuations_is_rejected(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(7, -1, -1), OWNER_7)
    _shadow(db, ws, p, 20, [2, 1], _dip(20, 4))  # covers 1 of 7 days; dip on day 4 uncovered

    att = compute_portfolio_attribution(db, p.id, 7)

    assert att["static_shadow"] is None
    assert att["avoided_drawdown_pct"] is None  # null, not -owner drawdown
    assert att["static_shadow_selection"]["status"] == "no_eligible_shadow"


def test_w2_7d_shadow_missing_material_early_drawdown_is_rejected(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(7, -1, -1), OWNER_7)
    _shadow(db, ws, p, 20, [2, 1, 0], _dip(20, 4))  # first valuation 5 days late

    att = compute_portfolio_attribution(db, p.id, 7)

    assert att["static_shadow"] is None
    assert att["avoided_drawdown_pct"] is None


def test_w3_fully_covered_7d_shadow_passes(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(7, -1, -1), OWNER_7)
    sh = _shadow(db, ws, p, 20, range(7, -1, -1), _dip(20, 4))

    att = compute_portfolio_attribution(db, p.id, 7)

    assert att["static_shadow"]["shadow_id"] == sh.id
    assert att["static_shadow"]["max_drawdown_pct"] == pytest.approx(10.0)
    assert att["avoided_drawdown_pct"] == pytest.approx(5.0)


def test_w4_7d_one_day_edge_gap_passes(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(7, -1, -1), OWNER_7)
    sh = _shadow(db, ws, p, 20, range(6, 0, -1))  # starts 1 day late, ends 1 day early
    att = compute_portfolio_attribution(db, p.id, 7)
    assert att["static_shadow"]["shadow_id"] == sh.id



def test_w4b_7d_two_day_edge_gap_fails(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(7, -1, -1), OWNER_7)
    _shadow(db, ws, p, 20, range(5, -1, -1))  # starts 2 days late

    att = compute_portfolio_attribution(db, p.id, 7)

    assert att["static_shadow"] is None


def test_w5_ineligible_newer_shadow_does_not_displace_eligible_older(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(7, -1, -1), OWNER_7)
    old = _shadow(db, ws, p, 20, range(7, -1, -1), _dip(20, 4))
    _shadow(db, ws, p, 8, [1, 0])  # newer inception, still <= window start, but sparse

    att = compute_portfolio_attribution(db, p.id, 7)

    assert att["static_shadow"]["shadow_id"] == old.id
    assert att["avoided_drawdown_pct"] == pytest.approx(5.0)


def test_w6_valid_7d_zero_drawdown_is_zero_not_null(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(7, -1, -1))  # flat owner
    _shadow(db, ws, p, 20, range(7, -1, -1))  # flat shadow

    att = compute_portfolio_attribution(db, p.id, 7)

    assert att["static_shadow"]["max_drawdown_pct"] == 0.0
    assert att["avoided_drawdown_pct"] == 0.0


def test_w7_valid_90d_comparison_still_accepted(db, wp):
    ws, p = wp
    nav = {n: (950_000.0 if n == 40 else 1_000_000.0) for n in range(90, -1, -1)}
    _owner(db, ws, p, range(90, -1, -1), nav)
    # starts 5 days late and ends 5 days early: still inside the 5-day cap
    sh = _shadow(db, ws, p, 100, range(85, 4, -1), _dip(100, 50))

    att = compute_portfolio_attribution(db, p.id, 90)

    assert att["static_shadow"]["shadow_id"] == sh.id
    assert att["avoided_drawdown_pct"] is not None
