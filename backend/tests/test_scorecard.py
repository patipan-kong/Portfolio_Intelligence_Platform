"""Tests for services/evaluation/scorecard.py — AI Evaluation M3.

Coverage
--------
1. Cold start: no RecommendationSnapshot ever -> status="cold_start",
   structured empty lenses (never zeros/errors).
2. Partial history: a PLAN grade exists (execution lens populated) but no
   horizon grade yet (belief lens cold) -> top-level status="partial".
3. Min-n gating: horizon grades exist but fewer than min_n_letter_grade ->
   belief.grade.status == "insufficient_evidence" even though hit_rate_pct
   is a real number (not hidden, just ungraded per UX D10).
4. Sufficient evidence (settings overridden to a low min_n): belief.grade
   reaches status="ok" with a letter.
5. Verdict payload always present with en/th/branch.
"""
from __future__ import annotations

import json
import sys
import os
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.evaluation.scorecard import compute_scorecard  # noqa: E402


@pytest.fixture()
def db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models.database import Base
    import models.asset  # noqa: F401 — registers Asset*/asset_relationships tables

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture()
def ws_portfolio(db):
    from models.database import Workspace, Portfolio

    ws = Workspace(name="Test")
    db.add(ws)
    db.commit()
    db.refresh(ws)

    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=100_000.0)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return ws, portfolio


def _seed_snapshot(db, ws, portfolio, days_ago: int = 40):
    from models.database import OptimizerHistory, RecommendationSnapshot

    oh = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=portfolio.id, portfolio_name=portfolio.name,
        analyzed_at=datetime.utcnow(), swap_count=0,
        result_json=json.dumps({"target_allocations": [], "cash_balance": 50_000.0}),
    )
    db.add(oh)
    db.commit()
    db.refresh(oh)

    snap = RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=portfolio.id,
        total_portfolio_value=1_000_000.0,
        projected_allocations_json="[]",
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def test_cold_start_portfolio_returns_cold_start_status(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    result = compute_scorecard(db, portfolio.id, period_days=90)

    assert result["status"] == "cold_start"
    assert result["belief"]["status"] == "cold_start"
    assert result["execution"]["status"] == "cold_start"
    assert result["verdict"]["en"]
    assert result["recent_grades"] == []


def test_partial_history_execution_graded_belief_cold(db, ws_portfolio):
    from models.database import RecommendationGrade

    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio)

    db.add(RecommendationGrade(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        grade_kind="PLAN", graded_at=datetime.utcnow(), score=88.0,
        detail_json=json.dumps({"necessity_score": 90.0, "funding_efficiency_score": 95.0}),
        created_at=datetime.utcnow(),
    ))
    db.commit()

    result = compute_scorecard(db, portfolio.id, period_days=90)

    assert result["execution"]["status"] == "ok"
    assert result["execution"]["avg_plan_score"] == 88.0
    assert result["execution"]["avg_necessity_pct"] == 90.0
    assert result["belief"]["status"] == "cold_start"
    assert result["status"] == "partial"


def test_min_n_gating_hides_letter_but_keeps_hit_rate(db, ws_portfolio):
    from models.database import RecommendationGrade

    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio)

    # Only 2 horizon grades -- default min_n_letter_grade is 8.
    for i, correct in enumerate([True, True]):
        db.add(RecommendationGrade(
            workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
            grade_kind=f"H{7 + i}", graded_at=datetime.utcnow(),
            window_start="2026-01-01", window_end=datetime.utcnow().date().isoformat(),
            return_pct=2.0, alpha=1.0, directional_correct=correct,
            created_at=datetime.utcnow(),
        ))
    db.commit()

    result = compute_scorecard(db, portfolio.id, period_days=90)

    assert result["belief"]["hit_rate_pct"] == 100.0
    assert result["belief"]["grade"]["status"] == "insufficient_evidence"
    assert result["belief"]["grade"]["letter"] is None


def test_sufficient_evidence_with_lowered_settings_yields_letter(db, ws_portfolio):
    from models.database import RecommendationGrade, Settings

    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio)

    db.add(Settings(
        workspace_id=ws.id, key="evaluation_settings",
        value=json.dumps({"min_n_letter_grade": 1, "min_n_win_rate": 1}),
    ))
    db.add(RecommendationGrade(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        grade_kind="H30", graded_at=datetime.utcnow(),
        window_start="2026-01-01", window_end=datetime.utcnow().date().isoformat(),
        return_pct=4.2, alpha=3.1, directional_correct=True,
        created_at=datetime.utcnow(),
    ))
    db.commit()

    result = compute_scorecard(db, portfolio.id, period_days=90)

    assert result["belief"]["grade"]["status"] == "ok"
    assert result["belief"]["grade"]["letter"] == "A+"
    assert result["verdict"]["branch"] in ("ai_ahead", "human_ahead", "tie", "insufficient_evidence")


# DOGFOOD-04 (2026-09-14) -- Scorecard/Three Portfolios same-concept
# reconciliation.
#
# execution.implementation_shortfall's own code comment always claimed it
# was "the exact same figure /analytics/shadow-performance's
# three_portfolios.gap_a reports" (Single Source of Truth), but until this
# fix it was independently recomputed from the RAW, full-period
# compute_ideal_series return minus attribution_engine's live-priced,
# undisplayed ai_model_shadow.return_pct -- neither of which is the
# canonical-priced, AI-shadow-window-aligned pair three_portfolios.gap_a is
# built from. Live portfolio 4, 90D: the two paths produced -3.72% vs
# -0.33% under the identical "Implementation Shortfall" label -- a
# code-comment-contradicting bug. Fixed by threading compute_three_
# portfolios's own gap_a value straight through instead of recomputing it.
#
# outcome.ai_model_return_pct/ideal_return_pct remain intentionally DISTINCT
# from Three Portfolios' AI Portfolio/Ideal (Gap A Correctness Patch,
# 2026-07-06) -- that split is deliberate, not a bug -- so this suite only
# asserts the new outcome.methodology disambiguation exists, never that the
# numbers converge.

def _d(days_ago: int) -> str:
    from datetime import date

    return (date.today() - timedelta(days=days_ago)).isoformat()


def _seed_recommendation(db, ws, portfolio, allocations, days_ago):
    from models.database import OptimizerHistory, RecommendationSnapshot

    oh = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=portfolio.id, portfolio_name=portfolio.name,
        analyzed_at=datetime.utcnow(), swap_count=0,
        result_json=json.dumps({"target_allocations": allocations, "cash_balance": 0.0}),
    )
    db.add(oh)
    db.commit()
    db.refresh(oh)

    snap = RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=portfolio.id,
        total_portfolio_value=1_000_000.0,
        projected_allocations_json=json.dumps(allocations),
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def _seed_actual_nav(db, ws, portfolio, days_ago, price, actual_total_value):
    from models.database import PortfolioSnapshot

    db.add(PortfolioSnapshot(
        workspace_id=ws.id, portfolio_id=portfolio.id,
        snapshot_date=_d(days_ago), total_value=actual_total_value, cash_balance=0.0,
        holdings_json=json.dumps([{"symbol": "AAA", "current_price": price}]),
    ))
    db.commit()


def _seed_ai_shadow(db, ws, portfolio, *, inception_days_ago, holdings, snapshot_rows):
    """Mirrors tests/test_ideal_series.py's helper of the same name.
    snapshot_rows: list of (days_ago, holdings_json_or_None, stored_total_value,
    stored_return_pct_since_inception) -- the STORED fields simulate whatever
    shadow_tracker.value_shadow_portfolio wrote from its own (live-cache)
    price source."""
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot

    shadow = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="ACTIVE_MODEL",
        name="AI", inception_date=_d(inception_days_ago), inception_value=1_000_000.0,
        inception_holdings_json=json.dumps(holdings), paper_cash_balance=0.0,
        is_active=True, created_at=datetime.utcnow(),
    )
    db.add(shadow)
    db.commit()
    db.refresh(shadow)

    for days_ago, holdings_json, stored_total_value, stored_return_pct in snapshot_rows:
        db.add(ShadowPortfolioSnapshot(
            shadow_portfolio_id=shadow.id, snapshot_date=_d(days_ago),
            total_value=stored_total_value, return_pct_since_inception=stored_return_pct,
            daily_return_pct=None,
            holdings_json=json.dumps(holdings_json) if holdings_json is not None else None,
            created_at=datetime.utcnow(),
        ))
    db.commit()
    return shadow


_SEED_100_AAA = [{"symbol": "AAA", "target_weight": 100.0, "action": "BUY"}]
_AAA_10000_SHARES = [{"symbol": "AAA", "shares": 10000, "inception_price": 100.0, "price_frozen": False}]


def test_implementation_shortfall_matches_three_portfolios_gap_a(db, ws_portfolio):
    """The Execution lens's Implementation Shortfall must equal
    three_portfolios.gap_a exactly, for the identical request -- not a
    close approximation, the same number -- reproducing the DOGFOOD-04
    root-cause scenario: the AI shadow's stored valuation implies a large
    return while its canonical-priced revaluation (what Ideal is actually
    compared against) implies a small one."""
    from services.evaluation.ideal_series import compute_three_portfolios

    ws, portfolio = ws_portfolio
    _seed_recommendation(db, ws, portfolio, _SEED_100_AAA, days_ago=15)
    _seed_actual_nav(db, ws, portfolio, 10, 100.0, 1_000_000.0)
    _seed_actual_nav(db, ws, portfolio, 0, 110.0, 1_020_000.0)  # canonical AAA +10%, You +2%
    _seed_ai_shadow(
        db, ws, portfolio, inception_days_ago=10, holdings=_AAA_10000_SHARES,
        snapshot_rows=[
            (10, _AAA_10000_SHARES, 1_000_000.0, 0.0),
            # Stored valuation implies +50% -- a materially different figure
            # from the +10% canonical price move above.
            (0, _AAA_10000_SHARES, 1_500_000.0, 50.0),
        ],
    )

    sc = compute_scorecard(db, portfolio.id, period_days=10)
    tp = compute_three_portfolios(db, portfolio.id, period_days=10)

    shortfall = sc["execution"]["implementation_shortfall"]
    assert shortfall["status"] == "ok"
    assert shortfall["value_pct"] == tp["gap_a"]["value"]
    # The old, pre-DOGFOOD-04 formula (raw ideal.return_pct minus the
    # stored/live-priced ai_model_shadow.return_pct) would have landed near
    # 10 - 50 = -40%, nowhere near the canonical-priced gap_a below -- the
    # two must not be conflated.
    assert abs(shortfall["value_pct"] - (-40.0)) > 5.0


def test_outcome_methodology_disambiguates_ai_and_ideal_from_three_portfolios(db, ws_portfolio):
    """outcome.ai_model_return_pct and outcome.ideal_return_pct are
    intentionally DISTINCT concepts from Three Portfolios' AI Portfolio/
    Ideal figures (Gap A Correctness Patch) -- this is not corrected to
    converge. Instead, the response must carry an explanatory methodology
    note for each, so no user-facing surface can present either bare
    number under an unqualified label."""
    ws, portfolio = ws_portfolio
    _seed_recommendation(db, ws, portfolio, _SEED_100_AAA, days_ago=15)
    _seed_actual_nav(db, ws, portfolio, 10, 100.0, 1_000_000.0)
    _seed_actual_nav(db, ws, portfolio, 0, 105.0, 1_020_000.0)
    _seed_ai_shadow(
        db, ws, portfolio, inception_days_ago=10, holdings=_AAA_10000_SHARES,
        snapshot_rows=[
            (10, _AAA_10000_SHARES, 1_000_000.0, 0.0),
            (0, _AAA_10000_SHARES, 1_050_000.0, 5.0),
        ],
    )

    sc = compute_scorecard(db, portfolio.id, period_days=10)

    methodology = sc["outcome"]["methodology"]
    assert methodology["ai_model_return_pct"]
    assert methodology["ideal_return_pct"]
    assert "Three Portfolios" in methodology["ai_model_return_pct"]
    assert "Three Portfolios" in methodology["ideal_return_pct"]


def test_verdict_compliance_wording_does_not_say_ai_portfolio(db, ws_portfolio):
    """The Row-1 verdict sentence's compliance claim must not use the
    label "AI Portfolio" -- that label is also used, unqualified, for
    Three Portfolios' differently-computed canonical figure. It must name
    the concept it actually measures (the AI model's shadow account)."""
    from services.evaluation.verdict_composer import compose_scorecard_verdict

    result = compose_scorecard_verdict(
        period_days=90, belief_avg_alpha=1.5, belief_status="ok",
        gap_b=2.49, gap_b_n=19, min_n_win_rate=5, tie_band_pct=0.3,
    )
    assert result["branch"] == "ai_ahead"
    assert "AI Portfolio" not in result["en"]
    assert "shadow account" in result["en"]
