"""Tests for Review Workflows Slice 1 (ERR-01) — ExecutionReview.

Coverage
--------
1. Model/constraint: execution_decision_id uniqueness, invalid outcome
   CheckConstraint, cascade-delete when the parent decision is deleted.
2. Service upsert: create then update (reviewed_at fixed, updated_at advances).
3. Endpoint GET: no review -> 200 null; existing review -> 200 + payload;
   nonexistent/cross-portfolio decision -> 404 (never a special "no review"
   404 message).
4. Endpoint PUT: create -> 201, update -> 200, invalid outcome -> 422,
   cross-portfolio decision -> 404.
5. Historical-truth invariant: PUT never mutates UserExecutionDecision or
   RecommendationSnapshot.
"""
from __future__ import annotations

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import main
from models.database import (
    Base,
    ExecutionReview,
    Portfolio,
    RecommendationSnapshot,
    UserExecutionDecision,
    Workspace,
)
from services.execution_review import (
    get_execution_review,
    upsert_execution_review,
    valid_outcome,
)


def make_session():
    # StaticPool (not just check_same_thread=False): endpoint tests below
    # route requests through TestClient's anyio portal thread, distinct from
    # the fixture's own thread — SQLAlchemy's default SingletonThreadPool for
    # sqlite:///:memory: gives each thread its own separate empty database,
    # so the schema created here would be invisible to the portal thread
    # without a single shared connection.
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


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
    db.refresh(ws)

    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=100_000.0)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    decision = UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=1, portfolio_id=portfolio.id,
        decision="APPROVED", is_system_generated=False,
    )
    db.add(decision)
    db.commit()
    db.refresh(decision)

    return ws, portfolio, decision


def _mount(db):
    app = FastAPI()
    app.add_api_route(
        "/portfolios/{portfolio_id}/execution-decisions/{decision_id}/review",
        main.get_portfolio_execution_review,
        methods=["GET"],
    )
    app.add_api_route(
        "/portfolios/{portfolio_id}/execution-decisions/{decision_id}/review",
        main.put_portfolio_execution_review,
        methods=["PUT"],
    )
    app.dependency_overrides[main.get_db] = lambda: db
    return TestClient(app)


# ── Validator ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("raw,expected", [
    ("ON_TRACK", "ON_TRACK"),
    ("mixed", "MIXED"),
    (" off_track ", "OFF_TRACK"),
    ("GREAT", None),
    (None, None),
    ("", None),
])
def test_valid_outcome(raw, expected):
    assert valid_outcome(raw) == expected


# ── Model / constraint behavior ─────────────────────────────────────────────

def test_execution_decision_id_uniqueness_enforced(db, ws_portfolio_decision):
    ws, _portfolio, decision = ws_portfolio_decision
    db.add(ExecutionReview(workspace_id=ws.id, execution_decision_id=decision.id, outcome="ON_TRACK"))
    db.commit()

    db.add(ExecutionReview(workspace_id=ws.id, execution_decision_id=decision.id, outcome="MIXED"))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_invalid_outcome_violates_check_constraint(db, ws_portfolio_decision):
    ws, _portfolio, decision = ws_portfolio_decision
    db.add(ExecutionReview(workspace_id=ws.id, execution_decision_id=decision.id, outcome="GREAT"))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_review_cascade_deletes_with_parent_decision(db, ws_portfolio_decision):
    ws, _portfolio, decision = ws_portfolio_decision
    db.add(ExecutionReview(workspace_id=ws.id, execution_decision_id=decision.id, outcome="ON_TRACK"))
    db.commit()

    db.delete(decision)
    db.commit()

    assert db.query(ExecutionReview).filter_by(execution_decision_id=decision.id).first() is None


# ── Service upsert ───────────────────────────────────────────────────────────

def test_upsert_creates_then_updates(db, ws_portfolio_decision):
    ws, _portfolio, decision = ws_portfolio_decision

    payload, created = upsert_execution_review(db, decision, ws.id, "MIXED", "first pass", None)
    assert created is True
    assert payload["outcome"] == "MIXED"
    reviewed_at_original = payload["reviewed_at"]
    created_at_original = payload["created_at"]
    updated_at_original = payload["updated_at"]

    time.sleep(0.01)
    payload2, created2 = upsert_execution_review(db, decision, ws.id, "ON_TRACK", "revised", "goal date moved")
    assert created2 is False
    assert payload2["id"] == payload["id"]
    assert payload2["outcome"] == "ON_TRACK"
    assert payload2["summary"] == "revised"
    assert payload2["changed_context"] == "goal date moved"
    # id, reviewed_at, and created_at are fixed at first creation; only
    # updated_at advances on edit — proves this is an in-place update of the
    # same canonical row, not a new/append-only record.
    assert payload2["reviewed_at"] == reviewed_at_original
    assert payload2["created_at"] == created_at_original
    assert payload2["updated_at"] != updated_at_original

    assert db.query(ExecutionReview).filter_by(execution_decision_id=decision.id).count() == 1


def test_get_execution_review_returns_none_when_absent(db, ws_portfolio_decision):
    _ws, _portfolio, decision = ws_portfolio_decision
    assert get_execution_review(db, decision) is None


# ── Endpoint: GET ────────────────────────────────────────────────────────────

def test_get_endpoint_returns_null_when_no_review_exists(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio, decision = ws_portfolio_decision
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)

    response = client.get(f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/review")
    assert response.status_code == 200
    assert response.json() is None


def test_get_endpoint_returns_review_when_present(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio, decision = ws_portfolio_decision
    upsert_execution_review(db, decision, ws.id, "OFF_TRACK", "went wrong", None)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)

    response = client.get(f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/review")
    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == "OFF_TRACK"
    assert body["summary"] == "went wrong"


def test_get_endpoint_404_for_nonexistent_decision_not_special_no_review_message(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio, _decision = ws_portfolio_decision
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)

    response = client.get(f"/portfolios/{portfolio.id}/execution-decisions/999999/review")
    assert response.status_code == 404
    assert response.json()["detail"] == "Execution decision not found"


def test_get_endpoint_404_for_cross_portfolio_decision(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio_a, decision_a = ws_portfolio_decision
    portfolio_b = Portfolio(workspace_id=ws.id, name="P2", cash_balance=0.0)
    db.add(portfolio_b)
    db.commit()
    db.refresh(portfolio_b)

    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)

    response = client.get(f"/portfolios/{portfolio_b.id}/execution-decisions/{decision_a.id}/review")
    assert response.status_code == 404
    assert response.json()["detail"] == "Execution decision not found"


# ── Endpoint: PUT ────────────────────────────────────────────────────────────

def test_put_endpoint_creates_review_returns_201(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio, decision = ws_portfolio_decision
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)

    response = client.put(
        f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/review",
        json={"outcome": "on_track", "summary": "so far so good"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["outcome"] == "ON_TRACK"
    assert body["summary"] == "so far so good"
    assert body["changed_context"] is None


def test_put_endpoint_updates_existing_review_returns_200(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio, decision = ws_portfolio_decision
    upsert_execution_review(db, decision, ws.id, "ON_TRACK", "initial", None)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)

    response = client.put(
        f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/review",
        json={"outcome": "MIXED", "summary": "revised", "changed_context": "rates moved"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == "MIXED"
    assert body["changed_context"] == "rates moved"
    assert db.query(ExecutionReview).filter_by(execution_decision_id=decision.id).count() == 1


def test_put_endpoint_rejects_invalid_outcome(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio, decision = ws_portfolio_decision
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)

    response = client.put(
        f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/review",
        json={"outcome": "GREAT"},
    )
    assert response.status_code == 422
    assert db.query(ExecutionReview).count() == 0


def test_put_endpoint_404_for_cross_portfolio_decision(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio_a, decision_a = ws_portfolio_decision
    portfolio_b = Portfolio(workspace_id=ws.id, name="P2", cash_balance=0.0)
    db.add(portfolio_b)
    db.commit()
    db.refresh(portfolio_b)

    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)

    response = client.put(
        f"/portfolios/{portfolio_b.id}/execution-decisions/{decision_a.id}/review",
        json={"outcome": "ON_TRACK"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Execution decision not found"
    assert db.query(ExecutionReview).count() == 0


# ── Historical-truth invariant ──────────────────────────────────────────────

def test_put_never_mutates_execution_decision_or_snapshot(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio, decision = ws_portfolio_decision
    snapshot = RecommendationSnapshot(
        id=1, workspace_id=ws.id, optimizer_history_id=1, portfolio_id=portfolio.id,
        persona="BALANCED", total_portfolio_value=100_000.0,
    )
    db.add(snapshot)
    db.commit()

    decision_before = {c.name: getattr(decision, c.name) for c in decision.__table__.columns}
    snapshot_before = {c.name: getattr(snapshot, c.name) for c in snapshot.__table__.columns}

    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    client = _mount(db)
    client.put(
        f"/portfolios/{portfolio.id}/execution-decisions/{decision.id}/review",
        json={"outcome": "MIXED", "summary": "note", "changed_context": "context changed"},
    )

    db.expire_all()
    decision_after = {c.name: getattr(decision, c.name) for c in decision.__table__.columns}
    snapshot_after = {c.name: getattr(snapshot, c.name) for c in snapshot.__table__.columns}

    assert decision_after == decision_before
    assert snapshot_after == snapshot_before
