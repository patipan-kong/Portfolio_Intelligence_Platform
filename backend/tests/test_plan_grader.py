"""Tests for services/evaluation/plan_grader.py — AI Evaluation M2.

Coverage
--------
Pure composite (services.evaluation.plan_grader.compute_plan_grade)
  1. BH-incident fixture: funding-efficiency sub-score at/near floor
  2. Clean cash-funded plan: no discretionary excess -> funding efficiency 100
  3. Reproducibility: identical stored inputs -> identical grade dict
  4. Necessity score reflects the fraction of trades that are necessary or
     actively funding (not deferred-and-discretionary)
  5. Turnover proportionality decays with a stored TURNOVER_BREACH detail,
     is 100 when absent
  6. No-trade plan: explanation completeness depends on portfolio_assessment
     / no_action_summary presence

DB round-trip (services.evaluation.plan_grader.grade_pending_plans)
  7. Writes exactly one grade_kind="PLAN" row per snapshot
  8. Append-only: second call is a no-op
  9. Skips (with reason) a snapshot lacking target_allocations
"""
from __future__ import annotations

import itertools
import json
import sys
import os
from datetime import datetime

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.evaluation.plan_grader import compute_plan_grade, grade_pending_plans  # noqa: E402


# ── Fixture builder ─────────────────────────────────────────────────────────

def _alloc(
    symbol: str, action: str, change_pct: float, estimated_amount: float,
    current_weight: float = 10.0, sector: str = "Consumer",
) -> dict:
    return {
        "symbol": symbol,
        "action": action,
        "allocation_change_percent": change_pct,
        "current_weight": current_weight,
        "estimated_amount": estimated_amount,
        "sector": sector,
    }


# ── The BH-incident metric ──────────────────────────────────────────────────

def test_bh_incident_scores_funding_efficiency_at_floor():
    """Cash=120k, buy=30k (CENTEL), REDUCE BH proposes 95k -- the exact
    founding-example numbers from OPTIMIZER_PHILOSOPHY.md. No policy breach on
    BH's sector, so the REDUCE is discretionary Portfolio Improvement. The
    funding gap is zero (existing cash already covers CENTEL 4x over), so
    100% of BH's proposed release was unnecessary -- funding_efficiency_score
    must be at the floor (0), regardless of execution_optimizer correctly
    deferring the trade."""
    allocations = [
        _alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0, sector="Consumer"),
        _alloc("BH", "REDUCE", -9.5, 95_000, sector="Healthcare"),
    ]
    result = compute_plan_grade(allocations, cash_available=120_000, violations=[])

    assert result["funding_efficiency_score"] == 0.0
    assert result["deferred_count"] == 1
    assert result["funding_gap"] == 0.0


def test_clean_cash_funded_plan_scores_high():
    """Cash=0, buy=30k, REDUCE proposes exactly 30k -- the discretionary
    candidate is fully consumed by a real funding need; nothing is wasted."""
    allocations = [
        _alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0),
        _alloc("XYZ", "REDUCE", -3.0, 30_000),
    ]
    result = compute_plan_grade(allocations, cash_available=0.0, violations=[])

    assert result["funding_efficiency_score"] == 100.0
    assert result["necessity_score"] == 100.0  # the one trade is actively funding
    assert result["score"] > 90.0


# ── Reproducibility (Invariant 3) ───────────────────────────────────────────

def test_reproducibility_same_inputs_identical_grade():
    allocations = [
        _alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0, sector="Consumer"),
        _alloc("BH", "REDUCE", -9.5, 95_000, sector="Healthcare"),
    ]
    r1 = compute_plan_grade(allocations, cash_available=120_000, violations=[])
    r2 = compute_plan_grade(allocations, cash_available=120_000, violations=[])
    assert r1 == r2


# ── Necessity score ──────────────────────────────────────────────────────────

def test_necessity_score_reflects_deferred_fraction():
    """Two discretionary candidates, gap covers only one -- necessity_score
    is exactly 1/2 = 50."""
    allocations = [
        _alloc("BUY1", "BUY", 3.0, 30_000, current_weight=0.0),
        _alloc("A", "REDUCE", -3.0, 30_000),
        _alloc("B", "REDUCE", -3.0, 50_000),
    ]
    result = compute_plan_grade(allocations, cash_available=0.0, violations=[])
    assert result["necessity_score"] == 50.0


def test_necessary_sell_counts_toward_necessity_even_when_deferred_is_present():
    allocations = [
        _alloc("BUY1", "BUY", 3.0, 10_000, current_weight=0.0),
        _alloc("RISKY", "SELL", -10.0, 200_000),   # always NECESSARY
        _alloc("OTHER", "REDUCE", -3.0, 40_000),   # discretionary, deferred (gap already covered)
    ]
    result = compute_plan_grade(allocations, cash_available=0.0, violations=[])
    # RISKY (necessary) + OTHER (discretionary, deferred) = 1/2 = 50
    assert result["necessity_score"] == 50.0
    assert result["deferred_count"] == 1


# ── Turnover proportionality ─────────────────────────────────────────────────

def test_turnover_score_100_without_breach():
    result = compute_plan_grade([], cash_available=0.0, violations=[], violation_details=[])
    assert result["turnover_proportionality_score"] == 100.0


def test_turnover_score_decays_with_recorded_overshoot():
    violation_details = [{
        "violation_type": "TURNOVER_BREACH", "proposed_pct": 40.0, "allowed_pct": 20.0,
    }]
    result = compute_plan_grade([], cash_available=0.0, violations=[], violation_details=violation_details)
    # overshoot_ratio = (40-20)/20 = 1.0 -> score = 100 - 100 = 0
    assert result["turnover_proportionality_score"] == 0.0


# ── No-trade plan / explanation completeness ────────────────────────────────

def test_no_trade_plan_with_assessment_scores_full_explanation():
    result = compute_plan_grade(
        [], cash_available=50_000, violations=[], portfolio_assessment="Portfolio is well balanced."
    )
    assert result["explanation_completeness_score"] == 100.0
    assert result["trade_count"] == 0


def test_no_trade_plan_without_assessment_scores_partial_explanation():
    result = compute_plan_grade([], cash_available=50_000, violations=[])
    assert result["explanation_completeness_score"] == 60.0


# ── DB round-trip ────────────────────────────────────────────────────────────

_oh_id_counter = itertools.count(1)


@pytest.fixture()
def db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
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

    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=0.0)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return ws, portfolio


def _seed_snapshot(db, ws, portfolio, allocations, cash_balance=100_000.0, active_policy=None):
    from models.database import OptimizerHistory, RecommendationSnapshot

    oh = OptimizerHistory(
        workspace_id=ws.id,
        portfolio_id=portfolio.id,
        portfolio_name=portfolio.name,
        analyzed_at=datetime.utcnow(),
        swap_count=0,
        result_json=json.dumps({
            "target_allocations": allocations,
            "cash_balance": cash_balance,
            "portfolio_assessment": "Portfolio assessment text.",
            "active_policy": active_policy or {},
        }),
    )
    db.add(oh)
    db.commit()
    db.refresh(oh)

    snap = RecommendationSnapshot(
        workspace_id=ws.id,
        optimizer_history_id=oh.id,
        portfolio_id=portfolio.id,
        total_portfolio_value=1_000_000.0,
        projected_allocations_json=json.dumps(allocations),
        active_policy_json=json.dumps(active_policy or {}),
        created_at=datetime.utcnow(),
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def test_grade_pending_plans_writes_one_row(db, ws_portfolio):
    from models.database import RecommendationGrade

    ws, portfolio = ws_portfolio
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    _seed_snapshot(db, ws, portfolio, allocations, cash_balance=100_000.0)

    result = grade_pending_plans(db)

    assert len(result["graded"]) == 1
    grade = db.query(RecommendationGrade).filter_by(grade_kind="PLAN").one()
    assert grade.score is not None
    assert grade.window_start is None
    assert grade.window_end is None


def test_grade_pending_plans_is_append_only(db, ws_portfolio):
    from models.database import RecommendationGrade

    ws, portfolio = ws_portfolio
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    _seed_snapshot(db, ws, portfolio, allocations)

    first = grade_pending_plans(db)
    assert len(first["graded"]) == 1
    assert db.query(RecommendationGrade).filter_by(grade_kind="PLAN").count() == 1

    second = grade_pending_plans(db)
    assert second["graded"] == []
    assert db.query(RecommendationGrade).filter_by(grade_kind="PLAN").count() == 1


def test_grade_pending_plans_skips_missing_allocations(db, ws_portfolio):
    from models.database import OptimizerHistory, RecommendationSnapshot

    ws, portfolio = ws_portfolio
    oh = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=portfolio.id, portfolio_name=portfolio.name,
        analyzed_at=datetime.utcnow(), swap_count=0, result_json="{}",
    )
    db.add(oh)
    db.commit()
    db.refresh(oh)

    snap = RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=portfolio.id,
        total_portfolio_value=1000.0, projected_allocations_json=None,
        created_at=datetime.utcnow(),
    )
    db.add(snap)
    db.commit()

    result = grade_pending_plans(db)
    assert result["graded"] == []
    assert len(result["skipped"]) == 1
    assert result["skipped"][0]["reason"] == "no_target_allocations"


def _muji_policy(*, verified=True, buy=0.0):
    sale = 10_000.0 if verified else 0.0
    buy_cost = round(buy * 0.0015, 2)
    return {
        "optimizer_policy_mode": "wealth.optimizer-muji.v2",
        "sector_policy_mode": "wealth.optimizer-sector-advisory.v1",
        "concentration": {"positions": {"SELL1": {"sell_signal": verified}}},
        "scheduled_execution": {
            "cash_available": 1_000.0, "total_buy_deployment": buy,
            "funding_gap": max(0.0, buy - 1_000.0 - sale + sale * 0.0015),
            "idle_cash_after": round(1_000 + sale - sale * 0.0015 - buy - buy_cost, 2),
            "scheduled_buys": {"BUY1": buy} if buy else {},
            "scheduled_changes": {**({"SELL1": -sale} if sale else {}), **({"BUY1": buy} if buy else {})},
            "estimated_trade_costs": {**({"SELL1": sale * 0.0015} if sale else {}),
                                      **({"BUY1": buy_cost} if buy else {})},
            "scheduled_turnover_pct": 10.0, "effective_turnover_cap_pct": 20.0,
            "trades": [{
                "symbol": "SELL1", "action": "SELL", "reason": "INVESTMENT_THESIS",
                "necessity": "DISCRETIONARY", "execution_role": "STANDALONE" if not buy else "FUNDING_SOURCE",
                "execution_state": "FULL" if verified else "DEFERRED",
                "full_recommended_amount": 10_000.0, "executed_amount": sale,
                "evidence_status": "NOT_APPLICABLE" if verified else "UNVERIFIED",
                "funding_basis": "INDEPENDENT_FROZEN_SELL_SIGNAL" if verified else "UNVERIFIED",
                "note": "Frozen SELL signal" if verified else "Unverified sale deferred",
            }],
        },
    }


def test_muji_verified_sell_to_cash_and_funding_role_have_equal_action_credit():
    allocations = [_alloc("SELL1", "SELL", -10, -10_000)]
    standalone = compute_plan_grade(allocations, 1_000, policy_provenance=_muji_policy())
    assert standalone["grade_version"] == "wealth.plan-grade-muji.v2"
    assert standalone["score"] == 100
    assert standalone["projected_cash"] == 10_985
    funded = _muji_policy(buy=5_000)
    result = compute_plan_grade([*allocations, _alloc("BUY1", "BUY", 5, 5_000)], 1_000,
                                policy_provenance=funded)
    assert result["action_evidence_score"] == 100
    assert result["score"] == standalone["score"]


def test_muji_unverified_or_cap_only_sale_gets_no_action_credit():
    allocations = [_alloc("SELL1", "SELL", -10, -10_000)]
    policy = _muji_policy(verified=False)
    grade = compute_plan_grade(allocations, 1_000, policy_provenance=policy)
    assert grade["action_evidence_score"] == 0
    assert grade["deferred_count"] == 1
    allocations[0]["reason"] = "Position exceeds advisory cap"
    policy["concentration"] = {"position_cap": 15, "sector_cap": 40}
    assert compute_plan_grade(allocations, 1_000, policy_provenance=policy) == grade
    policy["concentration"]["position_cap"] = 25
    assert compute_plan_grade(allocations, 1_000, policy_provenance=policy) == grade


def test_muji_cash_limited_buy_remains_recommendation_without_scheduled_credit():
    policy = _muji_policy(verified=False)
    allocations = [_alloc("SELL1", "SELL", -10, -10_000),
                   _alloc("BUY1", "BUY", 5, 5_000)]
    grade = compute_plan_grade(allocations, 1_000, policy_provenance=policy)
    assert grade["scheduled_buy_count"] == 0
    assert grade["action_evidence_score"] == 0
    assert grade["projected_cash"] == 1_000


def test_muji_supported_hold_has_no_trade_penalty():
    policy = _muji_policy(verified=False)
    schedule = policy["scheduled_execution"]
    schedule["trades"] = []
    schedule["scheduled_turnover_pct"] = 0
    grade = compute_plan_grade([_alloc("HOLD1", "HOLD", 0, 0)], 1_000,
                               portfolio_assessment="No investment change is justified.",
                               policy_provenance=policy)
    assert grade["trade_count"] == 0
    assert grade["action_evidence_score"] == 100
    assert grade["score"] == 100


def test_muji_missing_or_malformed_frozen_schedule_is_unavailable(db, ws_portfolio):
    from models.database import RecommendationGrade
    from services.optimizer.sector_policy import UnsupportedOptimizerPolicyEvidence
    allocations = [_alloc("SELL1", "SELL", -10, -10_000)]
    policy = _muji_policy()
    for broken in (None, {**policy["scheduled_execution"], "scheduled_changes": None},
                   {**policy["scheduled_execution"], "idle_cash_after": 11_000}):
        candidate = {**policy, "scheduled_execution": broken}
        with pytest.raises(UnsupportedOptimizerPolicyEvidence):
            compute_plan_grade(allocations, 1_000, policy_provenance=candidate)
    ws, portfolio = ws_portfolio
    _seed_snapshot(db, ws, portfolio, allocations, cash_balance=1_000,
                   active_policy={**policy, "scheduled_execution": {**policy["scheduled_execution"], "idle_cash_after": 11_000}})
    assert grade_pending_plans(db)["skipped"][0]["reason"] == "unsupported_optimizer_policy_evidence"
    assert db.query(RecommendationGrade).count() == 0
