"""Focused tests for the Product Intelligence Slice 3 comparison service."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401

from services.evaluation.recommendation_comparison import get_recommendation_comparison


@pytest.fixture()
def db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    from models.database import Base

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture()
def ws_portfolio(db):
    from models.database import Portfolio, Workspace

    ws = Workspace(name="Test")
    db.add(ws)
    db.commit()
    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=100_000.0)
    db.add(portfolio)
    db.commit()
    return ws, portfolio


def _seed_snapshot(db, ws, portfolio, *, created_at=None, **overrides):
    from models.database import OptimizerHistory, RecommendationSnapshot

    created_at = created_at or datetime.utcnow()
    oh = OptimizerHistory(
        workspace_id=ws.id,
        portfolio_id=portfolio.id,
        portfolio_name=portfolio.name,
        analyzed_at=created_at,
        swap_count=0,
        result_json=json.dumps({"target_allocations": []}),
    )
    db.add(oh)
    db.commit()
    snapshot_kwargs = dict(
        workspace_id=ws.id,
        optimizer_history_id=oh.id,
        portfolio_id=portfolio.id,
        created_at=created_at,
        regime_snapshot_json=json.dumps({
            "regime": "SIDEWAYS",
            "confidence_pct": 60.0,
            "transition_stability": "STABLE",
        }),
        constraint_envelope_json=json.dumps({
            "effective_single_position_pct": 20.0,
            "effective_cash_min_pct": 5.0,
            "effective_turnover_max_pct": 30.0,
            "effective_sector_limits": {"Energy": 20.0, "Financials": 25.0},
            "emergency_active": False,
        }),
        active_policy_json=json.dumps({
            "deployment_bias": "SELECTIVE",
            "strictness_level": "NORMAL",
            "risk_budget": 0.5,
            "confidence_discount": 0.1,
        }),
        consensus_json=json.dumps({
            "consensus_type": "STRONG_CONSENSUS",
            "consensus_strength_score": 70.0,
        }),
        portfolio_dna_json=json.dumps({
            "growth": 50.0,
            "value": 50.0,
            "momentum": 50.0,
            "quality": 50.0,
            "dividend": 50.0,
        }),
        style_drift_json=json.dumps({
            "drift_score": 10.0,
            "drift_severity": "LOW",
            "rebalance_urgency": "LOW",
            "factor_drift": {"growth": 0.1},
            "factor_alignment_score": 90.0,
        }),
        projected_allocations_json=json.dumps([
            {"symbol": "PTT", "target_weight": 5.0, "action": "HOLD", "allocation_change_percent": 99.0},
        ]),
        wealth_goal_context_json=json.dumps({"secret": "must not leak"}),
    )
    snapshot_kwargs.update(overrides)
    snap = RecommendationSnapshot(**snapshot_kwargs)
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def test_same_portfolio_predecessor_and_tie_break(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    at = datetime(2026, 9, 1, 3, 0, 0)
    older = _seed_snapshot(db, ws, portfolio, created_at=at - timedelta(days=1))
    first = _seed_snapshot(db, ws, portfolio, created_at=at)
    second = _seed_snapshot(db, ws, portfolio, created_at=at)

    result = get_recommendation_comparison(db, portfolio.id, second.id, ws.id)
    assert result["previous"]["snapshot_id"] == first.id
    assert result["current"]["snapshot_id"] == second.id
    assert older.id != result["previous"]["snapshot_id"]


def test_no_previous_and_isolation(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    current = _seed_snapshot(db, ws, portfolio)
    other_portfolio = type(portfolio)(workspace_id=ws.id, name="P2", cash_balance=0)
    db.add(other_portfolio)
    db.commit()
    _seed_snapshot(db, ws, other_portfolio, created_at=current.created_at - timedelta(days=1))

    result = get_recommendation_comparison(db, portfolio.id, current.id, ws.id)
    assert result["status"] == "no_previous"
    assert result["previous"] is None
    assert result["sections"] == []


def test_changed_scalars_and_unchanged_fields_are_semantic(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    before = _seed_snapshot(db, ws, portfolio, created_at=datetime(2026, 8, 1))
    after = _seed_snapshot(
        db,
        ws,
        portfolio,
        created_at=datetime(2026, 9, 1),
        regime_snapshot_json=json.dumps({"regime": "RISK_ON", "confidence_pct": 72.5, "transition_stability": "STABLE"}),
        constraint_envelope_json=json.dumps({
            "effective_single_position_pct": 20.0,
            "effective_cash_min_pct": 7.0,
            "effective_turnover_max_pct": 30.0,
            "effective_sector_limits": {"Energy": 20.0, "Financials": 25.0},
            "emergency_active": False,
        }),
        active_policy_json=json.dumps({
            "deployment_bias": "DEFENSIVE",
            "strictness_level": "NORMAL",
            "risk_budget": 0.4,
            "confidence_discount": 0.1,
        }),
        consensus_json=json.dumps({"consensus_type": "WEAK_CONSENSUS", "consensus_strength_score": 61.0}),
    )
    result = get_recommendation_comparison(db, portfolio.id, after.id, ws.id)
    sections = {section["key"]: section for section in result["sections"]}
    assert {f["key"] for f in sections["regime"]["fields"]} == {"regime", "confidence_pct"}
    assert sections["regime"]["fields"][1]["delta"] == 12.5
    assert {f["key"] for f in sections["constraint_envelope"]["fields"]} == {"effective_cash_min_pct"}
    assert {f["key"] for f in sections["policy_posture"]["fields"]} == {"deployment_bias", "risk_budget"}
    assert {f["key"] for f in sections["consensus"]["fields"]} == {"consensus_type", "consensus_strength_score"}
    assert before.wealth_goal_context_json is not None
    assert "secret" not in json.dumps(result)


def test_allocation_union_zero_sell_and_fresh_delta(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _seed_snapshot(
        db, ws, portfolio, created_at=datetime(2026, 8, 1),
        projected_allocations_json=json.dumps([
            {"symbol": "PTT", "target_weight": 5.0, "action": "HOLD", "allocation_change_percent": 500.0},
            {"symbol": "AOT", "target_weight": 6.0, "action": "HOLD"},
        ]),
    )
    current = _seed_snapshot(
        db, ws, portfolio, created_at=datetime(2026, 9, 1),
        projected_allocations_json=json.dumps([
            {"symbol": "PTT", "target_weight": 0.0, "action": "SELL", "allocation_change_percent": -999.0},
            {"symbol": "CPALL", "target_weight": 4.0, "action": "BUY"},
        ]),
    )
    result = get_recommendation_comparison(db, portfolio.id, current.id, ws.id)
    entries = {entry["symbol"]: entry for section in result["sections"] if section["key"] == "allocations" for entry in section["entries"]}
    assert entries["PTT"]["status"] == "changed"
    assert entries["PTT"]["delta"] == -5.0
    assert entries["AOT"]["status"] == "removed"
    assert entries["CPALL"]["status"] == "added"


def test_sector_diff_sorted_and_missing_sources_unavailable(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _seed_snapshot(
        db, ws, portfolio, created_at=datetime(2026, 8, 1),
        constraint_envelope_json=json.dumps({"effective_sector_limits": {"Z": 10, "A": 20}}),
        projected_allocations_json=None,
    )
    current = _seed_snapshot(
        db, ws, portfolio, created_at=datetime(2026, 9, 1),
        constraint_envelope_json=json.dumps({"effective_sector_limits": {"A": 25, "B": 30}}),
        projected_allocations_json=json.dumps([]),
    )
    result = get_recommendation_comparison(db, portfolio.id, current.id, ws.id)
    sections = {section["key"]: section for section in result["sections"]}
    sectors = sections["constraint_envelope"]["sectors"]
    assert sections["constraint_envelope"]["changed"] is True
    assert [item["sector"] for item in sectors] == ["A", "B", "Z"]
    assert sections["allocations"]["status"] == "unavailable"


def test_duplicate_allocation_symbols_are_unavailable_not_discarded(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _seed_snapshot(
        db, ws, portfolio, created_at=datetime(2026, 8, 1),
        projected_allocations_json=json.dumps([
            {"symbol": "PTT", "target_weight": 5.0, "action": "HOLD"},
        ]),
    )
    current = _seed_snapshot(
        db, ws, portfolio, created_at=datetime(2026, 9, 1),
        projected_allocations_json=json.dumps([
            {"symbol": "PTT", "target_weight": 6.0, "action": "BUY"},
            {"symbol": "PTT", "target_weight": 7.0, "action": "BUY"},
        ]),
    )

    result = get_recommendation_comparison(db, portfolio.id, current.id, ws.id)
    sections = {section["key"]: section for section in result["sections"]}
    assert sections["allocations"]["status"] == "unavailable"
    assert "entries" not in sections["allocations"]


def test_structurally_malformed_nested_sources_are_unavailable(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _seed_snapshot(
        db, ws, portfolio, created_at=datetime(2026, 8, 1),
        constraint_envelope_json=json.dumps({"effective_sector_limits": {"Energy": 20.0}}),
        projected_allocations_json=json.dumps([{"symbol": "PTT", "target_weight": 5.0, "action": "HOLD"}]),
    )
    current = _seed_snapshot(
        db, ws, portfolio, created_at=datetime(2026, 9, 1),
        constraint_envelope_json=json.dumps({"effective_sector_limits": {"Energy": "twenty"}}),
        projected_allocations_json=json.dumps([{"symbol": "PTT", "target_weight": "five", "action": "HOLD"}]),
    )

    result = get_recommendation_comparison(db, portfolio.id, current.id, ws.id)
    sections = {section["key"]: section for section in result["sections"]}
    assert sections["constraint_envelope"]["sectors_status"] == "unavailable"
    assert sections["allocations"]["status"] == "unavailable"


def test_structurally_malformed_scalar_source_is_unavailable(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _seed_snapshot(db, ws, portfolio, created_at=datetime(2026, 8, 1))
    current = _seed_snapshot(
        db,
        ws,
        portfolio,
        created_at=datetime(2026, 9, 1),
        regime_snapshot_json=json.dumps({"regime": {"name": "RISK_ON"}, "confidence_pct": 60.0}),
    )

    result = get_recommendation_comparison(db, portfolio.id, current.id, ws.id)
    sections = {section["key"]: section for section in result["sections"]}
    assert sections["regime"]["status"] == "unavailable"
    assert sections["regime"]["fields"] == []


def test_snapshots_are_not_mutated(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    previous = _seed_snapshot(db, ws, portfolio, created_at=datetime(2026, 8, 1))
    current = _seed_snapshot(db, ws, portfolio, created_at=datetime(2026, 9, 1))
    before_values = (previous.regime_snapshot_json, current.regime_snapshot_json)
    get_recommendation_comparison(db, portfolio.id, current.id, ws.id)
    db.expire_all()
    assert (db.get(type(current), previous.id).regime_snapshot_json, db.get(type(current), current.id).regime_snapshot_json) == before_values


def test_comparison_endpoint_uses_report_card_404_semantics(db, ws_portfolio):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import main

    ws, portfolio = ws_portfolio
    current = _seed_snapshot(db, ws, portfolio)
    endpoint_app = FastAPI()
    endpoint_app.add_api_route(
        "/analytics/evaluation/recommendations/{snapshot_id}/comparison",
        main.get_evaluation_recommendation_comparison,
        methods=["GET"],
    )
    endpoint_app.dependency_overrides[main.get_db] = lambda: db
    client = TestClient(endpoint_app)
    try:
        response = client.get(
            f"/analytics/evaluation/recommendations/{current.id}/comparison",
            params={"portfolio_id": portfolio.id},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "no_previous"

        wrong_portfolio = client.get(
            f"/analytics/evaluation/recommendations/{current.id}/comparison",
            params={"portfolio_id": portfolio.id + 1},
        )
        assert wrong_portfolio.status_code == 404
        assert wrong_portfolio.json()["detail"] == "Recommendation snapshot not found"
    finally:
        endpoint_app.dependency_overrides.clear()


def test_comparison_uses_one_bounded_predecessor_query(db, ws_portfolio):
    from sqlalchemy import event

    ws, portfolio = ws_portfolio
    current = _seed_snapshot(db, ws, portfolio, created_at=datetime(2026, 9, 1))
    current_id = current.id
    _seed_snapshot(db, ws, portfolio, created_at=datetime(2026, 8, 1))
    statements: list[str] = []

    def capture(_conn, _cursor, statement, _parameters, _context, _executemany):
        if "recommendation_snapshots" in statement.lower():
            statements.append(statement.lower())

    event.listen(db.bind, "before_cursor_execute", capture)
    try:
        get_recommendation_comparison(db, portfolio.id, current_id, ws.id)
    finally:
        event.remove(db.bind, "before_cursor_execute", capture)

    assert len(statements) == 2
    assert "limit" in statements[1]
    assert "order by" in statements[1]
