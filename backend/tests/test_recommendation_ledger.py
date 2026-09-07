"""Tests for services/evaluation/recommendation_ledger.py — AI Evaluation M3.

Coverage
--------
list_recommendations_ledger
  1. Cold start (no snapshots) -> status="cold_start", empty rows
  2. Recent snapshot with no grades yet -> every horizon cell "maturing"
     with a due_date, decision=None, is_counterfactual=True (no decision
     recorded is not an accepted decision)
  3. REJECTED decision + a graded horizon -> is_counterfactual=True,
     headline_alpha reflects the most-mature graded horizon
  4. APPROVED decision -> is_counterfactual=False

get_report_card
  5. Unknown snapshot_id -> None (caller 404s)
  6. Snapshot with a PLAN grade, no decision yet -> plan section populated,
     execution section "no_decision_recorded", verdict is plan-only
  7. Snapshot with a decision but no linked transactions -> execution
     section reads "unavailable" from the analyzer, never fabricated
  8. Snapshot with a decision whose linked transaction is a .BK-variant
     spelling of the plan symbol -> execution_ledger's Registry-aware
     _linked_transactions (reused here per M6 Phase 4, replacing this
     module's former inline duplicate) links them instead of reporting
     no_linked_transaction.
"""
from __future__ import annotations

import json
import sys
import os
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import models.asset  # noqa: F401 — registers Asset* tables on Base.metadata
import models.registry_finding  # noqa: F401 — registers RegistryFinding table

from services.evaluation.recommendation_ledger import (  # noqa: E402
    get_report_card,
    list_recommendations_ledger,
)
from services import registry_lookup as lookup  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_registry_cache():
    lookup.invalidate_cache()
    yield
    lookup.invalidate_cache()


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

    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=100_000.0)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return ws, portfolio


def _seed_snapshot(db, ws, portfolio, days_ago: int = 2, allocations=None, consensus_type="STRONG_CONSENSUS"):
    from models.database import OptimizerHistory, RecommendationSnapshot

    allocations = allocations if allocations is not None else [
        {"symbol": "CENTEL", "action": "BUY", "allocation_change_percent": 3.0,
         "current_weight": 0.0, "estimated_amount": 30_000, "sector": "Consumer"},
    ]
    oh = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=portfolio.id, portfolio_name=portfolio.name,
        analyzed_at=datetime.utcnow(), swap_count=0,
        result_json=json.dumps({
            "target_allocations": allocations, "cash_balance": 50_000.0,
            "portfolio_assessment": "Balanced.",
        }),
    )
    db.add(oh)
    db.commit()
    db.refresh(oh)

    snap = RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=portfolio.id,
        total_portfolio_value=1_000_000.0,
        projected_allocations_json=json.dumps(allocations),
        active_policy_json=json.dumps({"violations": []}),
        consensus_json=json.dumps({"consensus_type": consensus_type}),
        scores_map_json=json.dumps({"CENTEL": {"current_price": 100.0}}),
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def test_cold_start_ledger(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    result = list_recommendations_ledger(db, portfolio.id)
    assert result["status"] == "cold_start"
    assert result["rows"] == []


def test_recent_snapshot_all_horizons_maturing_no_decision(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _seed_snapshot(db, ws, portfolio, days_ago=2)

    result = list_recommendations_ledger(db, portfolio.id)
    assert result["status"] == "ok"
    row = result["rows"][0]
    assert row["decision"] is None
    assert row["is_counterfactual"] is True
    assert row["trade_count"] == 1
    for kind in ("H7", "H30", "H90", "H180"):
        assert row["horizon_strip"][kind]["status"] == "maturing"
        assert "due_date" in row["horizon_strip"][kind]


def test_rejected_decision_marks_counterfactual_and_headline_alpha(db, ws_portfolio):
    from models.database import RecommendationGrade, UserExecutionDecision

    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio, days_ago=40)

    db.add(UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        decision="REJECTED", executed_at=datetime.utcnow(), created_at=datetime.utcnow(),
    ))
    db.add(RecommendationGrade(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        grade_kind="H30", graded_at=datetime.utcnow(),
        window_start="2026-01-01", window_end=datetime.utcnow().date().isoformat(),
        return_pct=-2.1, alpha=-3.9, directional_correct=False,
        created_at=datetime.utcnow(),
    ))
    db.commit()

    result = list_recommendations_ledger(db, portfolio.id)
    row = result["rows"][0]
    assert row["decision"] == "REJECTED"
    assert row["is_counterfactual"] is True
    assert row["headline_alpha"] == -3.9
    assert row["horizon_strip"]["H30"]["status"] == "graded"


def test_approved_decision_is_not_counterfactual(db, ws_portfolio):
    from models.database import UserExecutionDecision

    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio, days_ago=2)
    db.add(UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        decision="APPROVED", executed_at=datetime.utcnow(), created_at=datetime.utcnow(),
    ))
    db.commit()

    result = list_recommendations_ledger(db, portfolio.id)
    assert result["rows"][0]["is_counterfactual"] is False


def test_report_card_unknown_snapshot_returns_none(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    assert get_report_card(db, portfolio.id, snapshot_id=99999) is None


def test_report_card_plan_only_when_no_decision(db, ws_portfolio):
    from models.database import RecommendationGrade

    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio, days_ago=2)
    db.add(RecommendationGrade(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        grade_kind="PLAN", graded_at=datetime.utcnow(), score=90.0,
        detail_json=json.dumps({"necessity_score": 100.0}),
        created_at=datetime.utcnow(),
    ))
    db.commit()

    card = get_report_card(db, portfolio.id, snap.id)
    assert card is not None
    assert card["plan"]["status"] == "ok"
    assert card["plan"]["grade"]["score"] == 90.0
    assert card["execution"]["status"] == "no_decision_recorded"
    assert "matured" in card["verdict"]["en"]


def test_report_card_decision_without_linked_transactions_is_unavailable(db, ws_portfolio):
    from models.database import UserExecutionDecision

    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio, days_ago=2)
    db.add(UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        decision="APPROVED", executed_at=datetime.utcnow(), created_at=datetime.utcnow(),
    ))
    db.commit()

    card = get_report_card(db, portfolio.id, snap.id)
    assert card["execution"]["status"] == "ok"
    assert card["execution"]["analysis"]["status"] == "unavailable"
    assert card["execution"]["analysis"]["score"] is None


def test_report_card_execution_section_surfaces_rationale_and_goal_context(db, ws_portfolio):
    """Slice 4 (Decision History / Audit UX) — override rationale (UX.2D) and
    frozen goal context (Phase 7.4/ADR-008, CONTEXT_ONLY) are already
    persisted on UserExecutionDecision/RecommendationSnapshot; the Report
    Card must surface them rather than continuing to drop them."""
    from models.database import UserExecutionDecision, WealthGoal
    from services.decision_goal_context import build_decision_goal_context

    ws, portfolio = ws_portfolio
    goal = WealthGoal(
        workspace_id=ws.id, name="House", goal_type="HOUSE",
        target_amount=500_000.0, currency="THB", priority="HIGH", is_archived=False,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)

    context = build_decision_goal_context(db, ws.id, [goal.id])
    assert context["context_state"] == "COMPLETE"

    snap = _seed_snapshot(db, ws, portfolio, days_ago=2)
    snap.wealth_goal_context_json = json.dumps(context)
    db.add(snap)
    db.add(UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        decision="MANUAL_OVERRIDE", executed_at=datetime.utcnow(), created_at=datetime.utcnow(),
        override_type="REPLACE_SYMBOL", original_symbol="KBANK", replacement_symbol="TOA",
        reason_category="HIGHER_CONVICTION", override_notes="Higher conviction in TOA.",
    ))
    db.commit()

    card = get_report_card(db, portfolio.id, snap.id)
    execution = card["execution"]
    assert execution["override_type"] == "REPLACE_SYMBOL"
    assert execution["original_symbol"] == "KBANK"
    assert execution["replacement_symbol"] == "TOA"
    assert execution["reason_category"] == "HIGHER_CONVICTION"
    assert execution["override_notes"] == "Higher conviction in TOA."
    assert execution["goal_context"]["context_state"] == "COMPLETE"
    assert execution["goal_context"]["decision_effect"] == "CONTEXT_ONLY"
    assert execution["goal_context"]["goals"][0]["id"] == goal.id


def test_report_card_execution_section_degrades_cleanly_without_rationale_or_goal_context(db, ws_portfolio):
    """No override fields and no captured goal context (legacy/unscoped run)
    must degrade to None, never a fabricated value or an empty label."""
    from models.database import UserExecutionDecision

    ws, portfolio = ws_portfolio
    snap = _seed_snapshot(db, ws, portfolio, days_ago=2)
    assert snap.wealth_goal_context_json is None
    db.add(UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        decision="APPROVED", executed_at=datetime.utcnow(), created_at=datetime.utcnow(),
    ))
    db.commit()

    card = get_report_card(db, portfolio.id, snap.id)
    execution = card["execution"]
    assert execution["override_type"] is None
    assert execution["original_symbol"] is None
    assert execution["replacement_symbol"] is None
    assert execution["reason_category"] is None
    assert execution["override_notes"] is None
    assert execution["goal_context"] is None


def test_report_card_execution_evidence_survives_unavailable_plan_reconstruction(db, ws_portfolio):
    """Review Correction Pass BLOCKER: a decision, its rationale, and its
    frozen goal context are independently persisted (UserExecutionDecision,
    RecommendationSnapshot.wealth_goal_context_json) and do not depend on
    projected_allocations_json. A legacy/malformed snapshot with a missing
    plan must not make the Report Card claim "no_decision_recorded" — that
    is false whenever decision_row exists — nor may it fabricate execution
    analysis it cannot compute."""
    from models.database import UserExecutionDecision, WealthGoal
    from services.decision_goal_context import build_decision_goal_context

    ws, portfolio = ws_portfolio
    goal = WealthGoal(
        workspace_id=ws.id, name="House", goal_type="HOUSE",
        target_amount=500_000.0, currency="THB", priority="HIGH", is_archived=False,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    context = build_decision_goal_context(db, ws.id, [goal.id])

    snap = _seed_snapshot(db, ws, portfolio, days_ago=2)
    snap.projected_allocations_json = None  # plan reconstruction unavailable
    snap.wealth_goal_context_json = json.dumps(context)
    db.add(snap)
    db.add(UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        decision="MANUAL_OVERRIDE", executed_at=datetime.utcnow(), created_at=datetime.utcnow(),
        override_type="REPLACE_SYMBOL", original_symbol="KBANK", replacement_symbol="TOA",
        reason_category="HIGHER_CONVICTION", override_notes="Higher conviction in TOA.",
    ))
    db.commit()

    card = get_report_card(db, portfolio.id, snap.id)
    assert card["plan"]["status"] == "unavailable"  # unrelated, confirms the fixture is real

    execution = card["execution"]
    assert execution["status"] != "no_decision_recorded"
    assert execution["status"] == "ok"
    assert execution["decision_id"] is not None
    assert execution["decision"] == "MANUAL_OVERRIDE"
    assert execution["executed_at"] is not None

    assert execution["override_type"] == "REPLACE_SYMBOL"
    assert execution["original_symbol"] == "KBANK"
    assert execution["replacement_symbol"] == "TOA"
    assert execution["reason_category"] == "HIGHER_CONVICTION"
    assert execution["override_notes"] == "Higher conviction in TOA."
    assert execution["goal_context"]["context_state"] == "COMPLETE"
    assert execution["goal_context"]["goals"][0]["id"] == goal.id

    # Execution analysis degrades truthfully — never fabricated completion.
    assert execution["analysis"]["status"] == "unavailable"
    assert execution["analysis"]["reason"] == "no_target_allocations"
    assert execution["analysis"]["score"] is None
    assert "matched_count" not in execution["analysis"]
    assert "total_planned" not in execution["analysis"]
    assert "is_complete" not in execution["analysis"]


def test_report_card_bk_variant_transaction_links_via_registry_aware_matching(db, ws_portfolio):
    """Plan says "BH"; the linked Transaction was recorded as "BH.BK". Before
    M6 Phase 4 this call site built its own linked_transactions list inline
    with no symbol normalization, so this would have read as
    no_linked_transaction. Now it reuses execution_ledger's
    _linked_transactions (registry-aware, legacy .BK fallback), matching
    execution_ledger.py's own test of the same fix."""
    from models.database import Transaction, UserExecutionDecision

    ws, portfolio = ws_portfolio
    allocations = [
        {"symbol": "BH", "action": "BUY", "allocation_change_percent": 3.0,
         "current_weight": 0.0, "estimated_amount": 30_000, "sector": "Healthcare"},
    ]
    snap = _seed_snapshot(db, ws, portfolio, days_ago=2, allocations=allocations)

    dec = UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=snap.id, portfolio_id=portfolio.id,
        decision="APPROVED", executed_at=datetime.utcnow(), created_at=datetime.utcnow(),
    )
    db.add(dec)
    db.commit()
    db.refresh(dec)

    db.add(Transaction(
        workspace_id=ws.id, portfolio_id=portfolio.id, symbol="BH.BK",
        transaction_type="BUY", shares=300, price_per_share=100.0, total_amount=30_000,
        transaction_date=datetime.utcnow(), execution_decision_id=dec.id,
    ))
    db.commit()

    card = get_report_card(db, portfolio.id, snap.id)
    assert card["execution"]["analysis"]["symbols"]["BH"]["executed_amount"] == 30_000.0
    assert card["execution"]["analysis"]["symbols"]["BH"]["note"] is None
