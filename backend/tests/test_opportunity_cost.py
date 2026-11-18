"""Tests for services/evaluation/opportunity_cost.py — AI Evaluation M5.

Phase 4.24: matched-horizon Average Decision Return Difference. Owner return is
chained over each grade's own window; the headline is a mean over valid
comparisons (never a sum); pending/unavailable rows are never zero.
"""
from __future__ import annotations

import json
import sys
import os
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.evaluation.opportunity_cost import compute_opportunity_cost  # noqa: E402


@pytest.fixture()
def db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import models.asset  # noqa: F401  (registers the assets table for FK resolution)
    from models.database import Base

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


def _seed_snapshot(db, ws, portfolio, allocations, days_ago=10):
    from models.database import OptimizerHistory, RecommendationSnapshot

    oh = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=portfolio.id, portfolio_name=portfolio.name,
        analyzed_at=datetime.utcnow(), swap_count=0,
        result_json=json.dumps({"target_allocations": allocations, "cash_balance": 50_000.0}),
    )
    db.add(oh)
    db.commit()
    db.refresh(oh)

    snap = RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=portfolio.id,
        total_portfolio_value=1_000_000.0,
        projected_allocations_json=json.dumps(allocations),
        active_policy_json=json.dumps({"violations": []}),
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def _seed_decision(db, ws, portfolio, snap, decision_type, days_ago=10):
    from models.database import UserExecutionDecision

    dec = UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        decision=decision_type,
        executed_at=datetime.utcnow() - timedelta(days=days_ago),
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    )
    db.add(dec)
    db.commit()
    db.refresh(dec)
    return dec



_ALLOCS_BUY_ONLY = [
    {"symbol": "CENTEL", "action": "BUY", "allocation_change_percent": 3.0,
     "current_weight": 0.0, "estimated_amount": 30_000, "sector": "Consumer"},
]

# No BUY need -> funding gap is 0 -> this REDUCE has no job to do today -> deferred.
_ALLOCS_DEFERRED_REDUCE = [
    {"symbol": "BH", "action": "REDUCE", "allocation_change_percent": -3.0,
     "current_weight": 10.0, "estimated_amount": 30_000, "sector": "Consumer"},
]


def _d(days_ago: int) -> str:
    return (datetime.utcnow() - timedelta(days=days_ago)).date().isoformat()


def _seed_grade(db, ws, portfolio, snap, grade_kind="H7", return_pct=2.0,
                window_start="__default__", window_end="__default__"):
    """Grade row with explicit window; defaults to a 7-day window ending 13 days ago."""
    from models.database import RecommendationGrade

    ws_ = _d(20) if window_start == "__default__" else window_start
    we_ = _d(13) if window_end == "__default__" else window_end
    db.add(RecommendationGrade(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        grade_kind=grade_kind, graded_at=datetime.utcnow(),
        window_start=ws_, window_end=we_,
        return_pct=return_pct, alpha=1.0, created_at=datetime.utcnow(),
    ))
    db.commit()


def _seed_owner(db, ws, portfolio, series):
    """series: {days_ago: investment_return_pct (daily, cash-flow-adjusted) | None}."""
    from models.database import PortfolioSnapshot

    for days_ago, r in series.items():
        db.add(PortfolioSnapshot(
            workspace_id=ws.id, portfolio_id=portfolio.id, snapshot_date=_d(days_ago),
            total_value=1_000_000.0, cash_balance=0.0, investment_return_pct=r,
        ))
    db.commit()


def _matched_h7_owner(db, ws, portfolio, total_pct=3.0):
    """Owner series covering D(20)..D(13); the whole `total_pct` lands on D(19)."""
    _seed_owner(db, ws, portfolio, {20: 0.0, 19: total_pct, 18: 0.0, 17: 0.0, 16: 0.0, 15: 0.0, 14: 0.0, 13: 0.0})


def _divergence(db, ws, portfolio, grade_return=2.0, days_ago=20, dtype="REJECTED", **grade_kw):
    snap = _seed_snapshot(db, ws, portfolio, _ALLOCS_BUY_ONLY, days_ago=days_ago)
    dec = _seed_decision(db, ws, portfolio, snap, dtype, days_ago=days_ago)
    if grade_return is not None:
        _seed_grade(db, ws, portfolio, snap, return_pct=grade_return, **grade_kw)
    return snap, dec


def test_cold_start_no_decisions(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["status"] == "cold_start"
    assert result["rows"] == []
    assert result["net_opportunity_cost_pct"] is None
    assert result["mean_decision_delta_pp"] is None
    assert result["divergence_count"] == 0
    assert result["evaluated_count"] == 0
    assert result["system_deferrals"] == []


def test_approved_decision_is_not_a_divergence(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio, _ALLOCS_BUY_ONLY)
    _seed_decision(db, ws, portfolio, snap, "APPROVED")

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["rows"] == []
    assert result["status"] == "cold_start"
    assert result["divergence_count"] == 0


def test_exactly_matched_h7_interval(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=2.0)  # grade window D20 -> D13
    _matched_h7_owner(db, ws, portfolio, total_pct=3.0)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    row = result["rows"][0]
    assert row["status"] == "graded"
    assert row["actual_return_pct"] == pytest.approx(3.0)
    assert row["counterfactual_delta_pct"] == pytest.approx(1.0)  # positive: diverging helped
    assert (row["window_start"], row["window_end"]) == (_d(20), _d(13))
    assert result["mean_decision_delta_pp"] == pytest.approx(1.0)
    assert result["evaluated_count"] == 1
    # Legacy overlapping-window sum is retired, never silently reinterpreted.
    assert result["net_opportunity_cost_pct"] is None


def test_matched_h30_interval(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=4.0, days_ago=45,
                window_start=_d(45), window_end=_d(15))
    # 30-day window: +1% on D44, +1% on D30 (chained), zero elsewhere in window
    _seed_owner(db, ws, portfolio, {d: (1.0 if d in (44, 30) else 0.0) for d in range(45, 14, -1)})

    # H30 chosen over nothing else; period 90 allows it
    # (H30 <= 90 -> nearest graded horizon)
    from models.database import RecommendationGrade
    db.query(RecommendationGrade).update({"grade_kind": "H30"})
    db.commit()

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    row = result["rows"][0]
    assert row["grade_kind"] == "H30"
    assert row["actual_return_pct"] == pytest.approx((1.01 * 1.01 - 1) * 100, abs=1e-6)
    assert row["counterfactual_delta_pct"] == pytest.approx(2.01 - 4.0, abs=1e-6)


def test_actual_is_truncated_at_grade_end_not_today(db, ws_portfolio):
    """60-day owner history vs an H30 grade: only the grade window counts."""
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=0.0, days_ago=60,
                window_start=_d(60), window_end=_d(30))
    series = {d: 0.0 for d in range(60, 29, -1)}
    series.update({
        65: -20.0,   # before the comparison start -> excluded
        59: 2.0,     # inside the window
        25: -30.0,   # after the grade end (but before today) -> excluded
        1: -30.0,
    })
    _seed_owner(db, ws, portfolio, series)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["rows"][0]["actual_return_pct"] == pytest.approx(2.0)
    assert result["mean_decision_delta_pp"] == pytest.approx(2.0)


def test_overlapping_decisions_are_averaged_not_summed(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    for grade_return in (2.0, 1.0, -3.0):   # same window, deltas +1, +2, +6
        _divergence(db, ws, portfolio, grade_return=grade_return)
    _matched_h7_owner(db, ws, portfolio, total_pct=3.0)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["evaluated_count"] == 3
    assert result["mean_decision_delta_pp"] == pytest.approx(3.0)  # (1+2+6)/3, not 9
    assert result["net_opportunity_cost_pct"] is None


def test_repeated_decisions_on_same_snapshot_each_count_once(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    snap, _ = _divergence(db, ws, portfolio, grade_return=2.0)
    _seed_decision(db, ws, portfolio, snap, "MANUAL_OVERRIDE", days_ago=20)
    _matched_h7_owner(db, ws, portfolio, total_pct=3.0)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["divergence_count"] == 2
    assert result["evaluated_count"] == 2
    assert result["mean_decision_delta_pp"] == pytest.approx(1.0)  # mean, not 2.0


def test_divergence_without_graded_horizon_is_pending(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=None, dtype="MANUAL_OVERRIDE")
    _matched_h7_owner(db, ws, portfolio)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["pending_count"] == 1 and result["maturing_count"] == 1
    assert result["evaluated_count"] == 0
    assert result["mean_decision_delta_pp"] is None
    assert result["rows"][0]["status"] == "maturing"


def test_grade_with_missing_window_is_unavailable_not_guessed(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=2.0, window_start=None, window_end=None)
    _matched_h7_owner(db, ws, portfolio)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    row = result["rows"][0]
    assert row["status"] == "unavailable"
    assert row["unavailable_reason"] == "grade_window_missing"
    assert row["counterfactual_delta_pct"] is None
    assert result["unavailable_count"] == 1
    assert result["mean_decision_delta_pp"] is None


def test_decision_after_grade_window_is_unavailable(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio, _ALLOCS_BUY_ONLY, days_ago=20)
    _seed_decision(db, ws, portfolio, snap, "REJECTED", days_ago=5)   # acted after window end (D13)
    _seed_grade(db, ws, portfolio, snap, return_pct=2.0)
    _matched_h7_owner(db, ws, portfolio)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["rows"][0]["unavailable_reason"] == "decision_after_grade_window"
    assert result["mean_decision_delta_pp"] is None


def test_valid_zero_actual_return_is_not_treated_as_missing(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=0.0)
    _matched_h7_owner(db, ws, portfolio, total_pct=0.0)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["rows"][0]["status"] == "graded"
    assert result["rows"][0]["actual_return_pct"] == 0.0
    assert result["mean_decision_delta_pp"] == 0.0
    assert result["evaluated_count"] == 1


def test_missing_owner_boundary_observation_is_unavailable(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=2.0)
    # Owner history starts well after the grade start -> no observation at start.
    _seed_owner(db, ws, portfolio, {15: 1.0, 14: 1.0, 13: 1.0})

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["rows"][0]["unavailable_reason"] == "owner_observation_missing_at_window_start"
    assert result["mean_decision_delta_pp"] is None


def test_missing_owner_end_observation_is_unavailable(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=2.0)
    _seed_owner(db, ws, portfolio, {20: 0.0, 19: 1.0})   # last obs is 6 days before D13 (> 5-day tolerance)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["rows"][0]["unavailable_reason"] == "owner_observation_missing_at_window_end"


def test_legacy_rows_without_adjusted_return_are_unavailable(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=2.0)
    _seed_owner(db, ws, portfolio, {20: None, 19: None, 13: None})

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["rows"][0]["unavailable_reason"] == "owner_cash_flow_adjusted_return_unavailable"


def test_deposit_does_not_contaminate_actual_return(db, ws_portfolio):
    from models.database import PortfolioSnapshot

    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=0.0)
    _matched_h7_owner(db, ws, portfolio, total_pct=1.0)
    # A +50% NAV jump caused by a deposit: investment (adjusted) return stays 0.
    from sqlalchemy import update
    db.execute(update(PortfolioSnapshot).where(PortfolioSnapshot.snapshot_date == _d(17)).values(
        total_value=1_500_000.0, net_external_cash_flow=500_000.0, investment_return_pct=0.0))
    db.commit()

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["rows"][0]["actual_return_pct"] == pytest.approx(1.0)  # not +50%


def test_negative_delta_means_diverging_underperformed_ai(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=5.0)
    _matched_h7_owner(db, ws, portfolio, total_pct=-2.0)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["rows"][0]["counterfactual_delta_pct"] == pytest.approx(-7.0)
    assert result["mean_decision_delta_pp"] == pytest.approx(-7.0)


def test_no_valid_comparison_returns_null_not_zero(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=2.0)   # no owner history at all

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["mean_decision_delta_pp"] is None
    assert result["evaluated_count"] == 0
    assert result["status"] == "ok"


def test_counts_separate_divergences_from_evaluated(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=2.0)                                  # evaluated
    _divergence(db, ws, portfolio, grade_return=None, dtype="MANUAL_OVERRIDE")        # pending
    _divergence(db, ws, portfolio, grade_return=1.0, window_start=None)               # unavailable
    _matched_h7_owner(db, ws, portfolio, total_pct=3.0)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["divergence_count"] == 3
    assert result["evaluated_count"] == 1
    assert result["pending_count"] == 1
    assert result["unavailable_count"] == 1
    assert result["mean_decision_delta_pp"] == pytest.approx(1.0)   # denominator 1, not 3


def test_overlapping_windows_regression_old_sum_would_exceed_portfolio_loss(db, ws_portfolio):
    """Before/after: 10 decisions over one -10% owner decline. The old
    decision-date->today sum would be near -50..-100; the mean stays ~ -10."""
    ws, portfolio = ws_portfolio
    for _ in range(10):
        _divergence(db, ws, portfolio, grade_return=0.0)
    _matched_h7_owner(db, ws, portfolio, total_pct=-10.0)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert result["mean_decision_delta_pp"] == pytest.approx(-10.0)
    assert result["mean_decision_delta_pp"] > -100.0


def test_system_deferral_reported_without_fabricated_price(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _seed_snapshot(db, ws, portfolio, _ALLOCS_DEFERRED_REDUCE, days_ago=1)

    result = compute_opportunity_cost(db, portfolio.id, period_days=90)

    assert len(result["system_deferrals"]) == 1
    deferral = result["system_deferrals"][0]
    assert deferral["symbol"] == "BH"
    assert deferral["counterfactual_pricing"] == "unavailable"
    assert "counterfactual_reason" in deferral


# ── Phase 4.24 final review: decision-date semantics & boundary coverage ──────

def _delay_case(db, ws, portfolio, delay_days, dtype="REJECTED"):
    snap = _seed_snapshot(db, ws, portfolio, _ALLOCS_BUY_ONLY, days_ago=20)
    _seed_decision(db, ws, portfolio, snap, dtype, days_ago=20 - delay_days)
    _seed_grade(db, ws, portfolio, snap, return_pct=2.0)  # window D20 -> D13
    _matched_h7_owner(db, ws, portfolio, total_pct=3.0)
    return compute_opportunity_cost(db, portfolio.id, period_days=90)


@pytest.mark.parametrize("delay", [0, 1])
def test_decision_on_or_one_day_after_window_start_is_valid(db, ws_portfolio, delay):
    ws, portfolio = ws_portfolio
    result = _delay_case(db, ws, portfolio, delay)
    assert result["rows"][0]["status"] == "graded"
    assert result["evaluated_count"] == 1


@pytest.mark.parametrize("delay", [3, 6])
def test_materially_delayed_decision_is_unavailable(db, ws_portfolio, delay):
    ws, portfolio = ws_portfolio
    result = _delay_case(db, ws, portfolio, delay)
    row = result["rows"][0]
    assert row["status"] == "unavailable"
    assert row["unavailable_reason"] == "decision_delayed_after_window_start"
    assert result["mean_decision_delta_pp"] is None
    assert result["unavailable_count"] == 1


def test_decision_after_grade_end_is_unavailable(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    result = _delay_case(db, ws, portfolio, 10)  # executed D10, window ended D13
    assert result["rows"][0]["unavailable_reason"] == "decision_after_grade_window"


def test_expired_inaction_is_priced_from_recommendation_even_if_expiry_is_late(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    result = _delay_case(db, ws, portfolio, 14, dtype="EXPIRED")  # expiry D6, after window end
    row = result["rows"][0]
    assert row["status"] == "graded"
    assert row["counterfactual_delta_pct"] == pytest.approx(1.0)


def test_h7_end_boundary_tolerance_is_one_day(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio)  # window D20 -> D13
    # Observations stop at D16: 3 days of the 7-day window uncovered.
    _seed_owner(db, ws, portfolio, {20: 0.0, 19: 3.0, 18: 0.0, 17: 0.0, 16: 0.0})
    row = compute_opportunity_cost(db, portfolio.id, period_days=90)["rows"][0]
    assert row["status"] == "unavailable"
    assert row["unavailable_reason"] == "owner_observation_missing_at_window_end"


def test_h7_start_boundary_tolerance_is_one_day(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio)
    _seed_owner(db, ws, portfolio, {24: 0.0, 19: 3.0, 18: 0.0, 17: 0.0, 16: 0.0, 15: 0.0, 14: 0.0, 13: 0.0})
    row = compute_opportunity_cost(db, portfolio.id, period_days=90)["rows"][0]
    assert row["unavailable_reason"] == "owner_observation_missing_at_window_start"


def test_missing_intermediate_observations_are_not_zero_filled(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=0.0, days_ago=60,
                window_start=_d(60), window_end=_d(30))
    # Ten-day hole inside the window.
    series = {d: 0.0 for d in list(range(60, 50, -1)) + list(range(40, 29, -1))}
    _seed_owner(db, ws, portfolio, series)
    row = compute_opportunity_cost(db, portfolio.id, period_days=90)["rows"][0]
    assert row["status"] == "unavailable"
    assert row["unavailable_reason"] == "owner_observation_gap_in_window"


def test_first_window_day_return_is_not_double_counted(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _divergence(db, ws, portfolio, grade_return=0.0)
    # The start-boundary day's own return (5%) predates the window; only later days count.
    _seed_owner(db, ws, portfolio, {20: 5.0, 19: 1.0, 18: 0.0, 17: 0.0, 16: 0.0, 15: 0.0, 14: 0.0, 13: 0.0})
    row = compute_opportunity_cost(db, portfolio.id, period_days=90)["rows"][0]
    assert row["actual_return_pct"] == pytest.approx(1.0)
