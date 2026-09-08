"""Focused Product Intelligence Slice 2 follow-up acknowledgment tests."""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import main
from models.database import Base, ExecutionFollowUp, ExecutionReview, Portfolio, UserExecutionDecision, Workspace
from services.execution_follow_up import (
    set_execution_follow_up,
)
from services.execution_review import upsert_execution_review


def make_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


@pytest.fixture()
def db():
    session = make_session()
    yield session
    session.close()


@pytest.fixture()
def ws_portfolio_decision(db):
    ws = Workspace(name="Test")
    db.add(ws)
    db.commit()
    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=100_000.0)
    db.add(portfolio)
    db.commit()
    decision = UserExecutionDecision(
        workspace_id=ws.id,
        recommendation_snapshot_id=1,
        portfolio_id=portfolio.id,
        decision="APPROVED",
        is_system_generated=False,
    )
    db.add(decision)
    db.commit()
    return ws, portfolio, decision


@pytest.fixture()
def system_decision(db):
    ws = Workspace(name="Test")
    db.add(ws)
    db.commit()
    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=100_000.0)
    db.add(portfolio)
    db.commit()
    decision = UserExecutionDecision(
        workspace_id=ws.id,
        recommendation_snapshot_id=1,
        portfolio_id=portfolio.id,
        decision="EXPIRED",
        is_system_generated=True,
    )
    db.add(decision)
    db.commit()
    return ws, portfolio, decision


def _mount(db):
    app = FastAPI()
    app.add_api_route(
        "/portfolios/{portfolio_id}/execution-decisions/{decision_id}/follow-up",
        main.get_portfolio_execution_follow_up,
        methods=["GET"],
    )
    app.add_api_route(
        "/portfolios/{portfolio_id}/execution-decisions/{decision_id}/follow-up",
        main.put_portfolio_execution_follow_up,
        methods=["PUT"],
    )
    app.dependency_overrides[main.get_db] = lambda: db
    return TestClient(app)


def _review(db, ws, decision, outcome="MIXED"):
    payload, _ = upsert_execution_review(db, decision, ws.id, outcome, "summary", None)
    return payload


def test_follow_up_model_is_unique_and_cascades_with_decision(db, ws_portfolio_decision):
    ws, _portfolio, decision = ws_portfolio_decision
    db.add(ExecutionFollowUp(workspace_id=ws.id, execution_decision_id=decision.id))
    db.commit()
    db.add(ExecutionFollowUp(workspace_id=ws.id, execution_decision_id=decision.id))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()

    db.delete(decision)
    db.commit()
    assert db.query(ExecutionFollowUp).filter_by(execution_decision_id=decision.id).first() is None


def test_get_returns_null_state_without_row(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio, decision = ws_portfolio_decision
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    response = _mount(db).get(f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/follow-up")
    assert response.status_code == 200
    assert response.json() == {"acknowledged_at": None}


def test_acknowledge_mixed_is_idempotent_and_requires_current_review(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio, decision = ws_portfolio_decision
    review = _review(db, ws, decision, "MIXED")
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)

    body = {"acknowledged": True, "expected_review_updated_at": review["updated_at"]}
    first = client.put(f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/follow-up", json=body)
    assert first.status_code == 200
    acknowledged_at = first.json()["acknowledged_at"]
    assert acknowledged_at is not None

    time.sleep(0.01)
    repeated = client.put(f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/follow-up", json=body)
    assert repeated.status_code == 200
    assert repeated.json()["acknowledged_at"] == acknowledged_at

    stale = client.put(
        f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/follow-up",
        json={"acknowledged": True, "expected_review_updated_at": "2026-01-01T00:00:00Z"},
    )
    assert stale.status_code == 409


def test_acknowledge_rejects_missing_or_ineligible_review_and_system_decision(
    db, ws_portfolio_decision, system_decision, monkeypatch,
):
    ws, portfolio, decision = ws_portfolio_decision
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)
    no_review = client.put(
        f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/follow-up",
        json={"acknowledged": True},
    )
    assert no_review.status_code == 409

    review = _review(db, ws, decision, "MIXED")
    client_timestamp = client.put(
        f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/follow-up",
        json={"acknowledged": False, "acknowledged_at": "2026-09-08T03:00:00Z"},
    )
    assert client_timestamp.status_code == 422

    missing = client.put(
        f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/follow-up",
        json={"acknowledged": True},
    )
    assert missing.status_code == 422

    review = _review(db, ws, decision, "ON_TRACK")
    ineligible = client.put(
        f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/follow-up",
        json={"acknowledged": True, "expected_review_updated_at": review["updated_at"]},
    )
    assert ineligible.status_code == 409

    system_ws, system_portfolio, system = system_decision
    monkeypatch.setattr(main, "_ws_id", lambda _db: system_ws.id)
    rejected = _mount(db).put(
        f"/portfolios/{system_portfolio.id}/execution-decisions/{system.id}/follow-up",
        json={"acknowledged": False},
    )
    assert rejected.status_code == 400


def test_undo_is_idempotent_and_clears_timestamp(db, ws_portfolio_decision):
    ws, _portfolio, decision = ws_portfolio_decision
    review = _review(db, ws, decision, "OFF_TRACK")
    acknowledged = set_execution_follow_up(db, decision, ws.id, True, review["updated_at"])
    assert acknowledged["acknowledged_at"] is not None
    assert set_execution_follow_up(db, decision, ws.id, False) == {"acknowledged_at": None}
    assert set_execution_follow_up(db, decision, ws.id, False) == {"acknowledged_at": None}


@pytest.mark.parametrize("old_outcome,new_outcome", [
    ("MIXED", "ON_TRACK"),
    ("MIXED", "OFF_TRACK"),
    ("OFF_TRACK", "MIXED"),
])
def test_outcome_change_clears_acknowledgment(db, ws_portfolio_decision, old_outcome, new_outcome):
    ws, _portfolio, decision = ws_portfolio_decision
    review = _review(db, ws, decision, old_outcome)
    set_execution_follow_up(db, decision, ws.id, True, review["updated_at"])
    upsert_execution_review(db, decision, ws.id, new_outcome, "changed outcome", None)
    assert db.query(ExecutionFollowUp).filter_by(execution_decision_id=decision.id).one().acknowledged_at is None
    # Returning to the original follow-up outcome does not resurrect the
    # prior acknowledgment; a new explicit acknowledgment is required.
    upsert_execution_review(db, decision, ws.id, old_outcome, "round trip", None)
    assert db.query(ExecutionFollowUp).filter_by(execution_decision_id=decision.id).one().acknowledged_at is None


@pytest.mark.parametrize("new_outcome", ["MIXED", "OFF_TRACK"])
def test_on_track_transition_clears_any_legacy_acknowledgment(db, ws_portfolio_decision, new_outcome):
    ws, _portfolio, decision = ws_portfolio_decision
    _review(db, ws, decision, "ON_TRACK")
    db.add(ExecutionFollowUp(
        workspace_id=ws.id,
        execution_decision_id=decision.id,
        acknowledged_at=datetime.utcnow(),
    ))
    db.commit()

    upsert_execution_review(db, decision, ws.id, new_outcome, "new outcome", None)
    assert db.query(ExecutionFollowUp).filter_by(execution_decision_id=decision.id).one().acknowledged_at is None


def test_text_only_and_identical_review_edits_preserve_acknowledgment(db, ws_portfolio_decision):
    ws, _portfolio, decision = ws_portfolio_decision
    review = _review(db, ws, decision, "MIXED")
    set_execution_follow_up(db, decision, ws.id, True, review["updated_at"])
    acknowledged_at = db.query(ExecutionFollowUp).filter_by(execution_decision_id=decision.id).one().acknowledged_at

    upsert_execution_review(db, decision, ws.id, "MIXED", "new summary", None)
    assert db.query(ExecutionFollowUp).filter_by(execution_decision_id=decision.id).one().acknowledged_at == acknowledged_at
    upsert_execution_review(db, decision, ws.id, "MIXED", "new summary", "new context")
    assert db.query(ExecutionFollowUp).filter_by(execution_decision_id=decision.id).one().acknowledged_at == acknowledged_at


def test_follow_up_operations_preserve_historical_decision_fields(db, ws_portfolio_decision):
    ws, _portfolio, decision = ws_portfolio_decision
    before = {column.name: getattr(decision, column.name) for column in decision.__table__.columns}
    review = _review(db, ws, decision, "MIXED")
    set_execution_follow_up(db, decision, ws.id, True, review["updated_at"])
    set_execution_follow_up(db, decision, ws.id, False)

    db.expire_all()
    after = {column.name: getattr(decision, column.name) for column in decision.__table__.columns}
    assert after == before
