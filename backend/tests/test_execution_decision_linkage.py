"""Tests for the Transaction <-> UserExecutionDecision linkage — AI Evaluation
M2 (P5), extended for Decision -> Transaction Linkage Completion. Metadata-
only: services/portfolio_transactions.py::execute_buy / execute_sell accept
an optional execution_decision_id and store it verbatim on the created
Transaction row. Never inferred, never required.

Coverage
--------
1. execute_buy with execution_decision_id sets Transaction.execution_decision_id
2. execute_sell with execution_decision_id sets Transaction.execution_decision_id
3. Omitting it (existing call sites, existing tests) leaves it None —
   fully backward compatible
4. resolve_execution_decision_reference / _or_404 — same-workspace/
   same-portfolio match, nonexistent id, cross-portfolio id, cross-workspace id
5. Linked and unlinked trades produce identical accounting (cash, shares,
   avg_cost) — the column is metadata-only, proven by regression, not assumed
6. PARTIAL_EXECUTION and MANUAL_OVERRIDE decisions accept linkage exactly
   like APPROVED — no decision-type gating at the service layer
"""
from __future__ import annotations

import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import main
from models.database import Base, Portfolio, PortfolioItem, Transaction, UserExecutionDecision, Workspace
from services.portfolio_transactions import execute_buy, execute_sell
from services.portfolio_reference import (
    resolve_execution_decision_reference,
    resolve_execution_decision_or_404,
)


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
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


def test_execute_buy_links_execution_decision_id(db, ws_portfolio_decision):
    ws, portfolio, decision = ws_portfolio_decision

    result = execute_buy(
        db, ws.id, portfolio.id, "CENTEL", shares=100, price_per_share=30.0,
        execution_decision_id=decision.id,
    )
    tx = db.query(Transaction).filter_by(id=result["transaction_id"]).one()
    assert tx.execution_decision_id == decision.id


def test_execute_sell_links_execution_decision_id(db, ws_portfolio_decision):
    ws, portfolio, decision = ws_portfolio_decision
    buy_result = execute_buy(db, ws.id, portfolio.id, "CENTEL", shares=100, price_per_share=30.0)

    sell_result = execute_sell(
        db, ws.id, portfolio.id, "CENTEL", shares=50, price_per_share=32.0,
        execution_decision_id=decision.id,
    )
    tx = db.query(Transaction).filter_by(id=sell_result["transaction_id"]).one()
    assert tx.execution_decision_id == decision.id
    # The unrelated earlier BUY was never linked — no retroactive inference.
    buy_tx = db.query(Transaction).filter_by(id=buy_result["transaction_id"]).one()
    assert buy_tx.execution_decision_id is None


def test_omitting_execution_decision_id_leaves_it_none(db, ws_portfolio_decision):
    ws, portfolio, _decision = ws_portfolio_decision

    result = execute_buy(db, ws.id, portfolio.id, "CENTEL", shares=100, price_per_share=30.0)
    tx = db.query(Transaction).filter_by(id=result["transaction_id"]).one()
    assert tx.execution_decision_id is None


# ── Backend ownership-validation resolver ───────────────────────────────────
# Decision -> Transaction Linkage Completion: the API previously accepted any
# execution_decision_id that satisfied the DB-level FK (existence only). This
# resolver adds the missing workspace+portfolio ownership check, mirroring
# resolve_portfolio_reference/_or_404 in the same module.

def test_resolve_execution_decision_reference_matches_same_workspace_portfolio(db, ws_portfolio_decision):
    ws, portfolio, decision = ws_portfolio_decision
    found = resolve_execution_decision_reference(db, decision.id, ws.id, portfolio.id)
    assert found is not None
    assert found.id == decision.id


def test_resolve_execution_decision_reference_nonexistent_id_returns_none(db, ws_portfolio_decision):
    ws, portfolio, _decision = ws_portfolio_decision
    assert resolve_execution_decision_reference(db, 999_999, ws.id, portfolio.id) is None


def test_resolve_execution_decision_reference_cross_portfolio_returns_none(db, ws_portfolio_decision):
    ws, portfolio, decision = ws_portfolio_decision
    other_portfolio = Portfolio(workspace_id=ws.id, name="P2", cash_balance=0.0)
    db.add(other_portfolio)
    db.commit()
    db.refresh(other_portfolio)

    # decision belongs to `portfolio`, not `other_portfolio` — must not match
    assert resolve_execution_decision_reference(db, decision.id, ws.id, other_portfolio.id) is None


def test_resolve_execution_decision_reference_cross_workspace_returns_none(db, ws_portfolio_decision):
    ws, portfolio, decision = ws_portfolio_decision
    other_ws = Workspace(name="Other")
    db.add(other_ws)
    db.commit()
    db.refresh(other_ws)

    assert resolve_execution_decision_reference(db, decision.id, other_ws.id, portfolio.id) is None


def test_resolve_execution_decision_or_404_raises_on_miss(db, ws_portfolio_decision):
    ws, portfolio, _decision = ws_portfolio_decision
    with pytest.raises(HTTPException) as exc_info:
        resolve_execution_decision_or_404(db, 999_999, ws.id, portfolio.id)
    assert exc_info.value.status_code == 404


def test_resolve_execution_decision_or_404_cross_portfolio_raises_404_not_reveal(db, ws_portfolio_decision):
    """A real decision belonging to a different portfolio in the same
    workspace must 404 exactly like a nonexistent one — never a different
    status code that would reveal cross-tenant existence."""
    ws, portfolio, decision = ws_portfolio_decision
    other_portfolio = Portfolio(workspace_id=ws.id, name="P2", cash_balance=0.0)
    db.add(other_portfolio)
    db.commit()
    db.refresh(other_portfolio)

    with pytest.raises(HTTPException) as exc_info:
        resolve_execution_decision_or_404(db, decision.id, ws.id, other_portfolio.id)
    assert exc_info.value.status_code == 404


# ── Accounting equivalence (metadata-only invariant) ────────────────────────

def test_linked_and_unlinked_buys_produce_identical_accounting(db, ws_portfolio_decision):
    ws, portfolio, decision = ws_portfolio_decision
    starting_cash = portfolio.cash_balance

    # Second portfolio, same starting cash, identical trade, no linkage —
    # isolates the comparison from cross-trade cash-balance drift (captured
    # before the first trade mutates `portfolio.cash_balance`).
    other_portfolio = Portfolio(workspace_id=ws.id, name="P2", cash_balance=starting_cash)
    db.add(other_portfolio)
    db.commit()
    db.refresh(other_portfolio)

    linked = execute_buy(
        db, ws.id, portfolio.id, "CENTEL", shares=100, price_per_share=30.0,
        execution_decision_id=decision.id,
    )
    unlinked = execute_buy(db, ws.id, other_portfolio.id, "CENTEL", shares=100, price_per_share=30.0)

    for key in ("shares", "price_per_share", "total_amount", "fees", "cash_balance"):
        assert linked[key] == unlinked[key], f"{key} diverged: {linked[key]!r} vs {unlinked[key]!r}"


# ── Decision-type compatibility (no service-layer gating) ──────────────────

@pytest.mark.parametrize("decision_type", ["PARTIAL_EXECUTION", "MANUAL_OVERRIDE"])
def test_non_approved_decision_types_accept_linkage(db, ws_portfolio_decision, decision_type):
    ws, portfolio, _approved_decision = ws_portfolio_decision
    other_decision = UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=1, portfolio_id=portfolio.id,
        decision=decision_type, is_system_generated=False,
    )
    db.add(other_decision)
    db.commit()
    db.refresh(other_decision)

    result = execute_buy(
        db, ws.id, portfolio.id, "CENTEL", shares=100, price_per_share=30.0,
        execution_decision_id=other_decision.id,
    )
    tx = db.query(Transaction).filter_by(id=result["transaction_id"]).one()
    assert tx.execution_decision_id == other_decision.id


# ── Endpoint-level ownership proof ──────────────────────────────────────────
# The resolver tests above call resolve_execution_decision_reference/_or_404
# directly. That proves the resolver is correct but not that main.py's
# transaction_buy route actually calls it — deleting the two guard lines in
# main.py would leave every test above green. This test reaches the real
# route (mounted the same way test_wealth_review.py's endpoint tests do:
# a minimal FastAPI app exposing exactly one route from `main`, with
# main.get_db overridden and main._ws_id patched to the test workspace) so
# that regression is actually caught.

def test_buy_endpoint_rejects_cross_portfolio_execution_decision_id(db, ws_portfolio_decision, monkeypatch):
    ws, portfolio_a, _decision_a = ws_portfolio_decision
    portfolio_b = Portfolio(workspace_id=ws.id, name="P2", cash_balance=0.0)
    db.add(portfolio_b)
    db.commit()
    db.refresh(portfolio_b)

    decision_b = UserExecutionDecision(
        workspace_id=ws.id, recommendation_snapshot_id=1, portfolio_id=portfolio_b.id,
        decision="APPROVED", is_system_generated=False,
    )
    db.add(decision_b)
    db.commit()
    db.refresh(decision_b)

    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    endpoint_app = FastAPI()
    endpoint_app.add_api_route(
        "/portfolios/{portfolio_id}/transactions/buy",
        main.transaction_buy,
        methods=["POST"],
    )
    endpoint_app.dependency_overrides[main.get_db] = lambda: db

    tx_count_before = db.query(Transaction).count()

    # decision_b belongs to portfolio_b — posting it against portfolio_a must
    # 404 through the real route, before any accounting mutation.
    response = TestClient(endpoint_app).post(
        f"/portfolios/{portfolio_a.id}/transactions/buy",
        json={
            "symbol": "CENTEL",
            "shares": 100,
            "price_per_share": 30.0,
            "execution_decision_id": decision_b.id,
        },
    )

    assert response.status_code == 404
    # Same 404 as a nonexistent id — never reveals cross-portfolio existence.
    assert response.json()["detail"] == "Execution decision not found"
    # Failure occurred before any accounting mutation.
    assert db.query(Transaction).count() == tx_count_before
