"""Phase 7.7 Goal Intelligence v1, Slice 1 (ADR-014) contract and boundary tests."""

import ast
import asyncio
from datetime import date, timedelta
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import main
import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
from models.database import (
    Base,
    CashAccount,
    GoalFundingAllocation,
    Portfolio,
    PortfolioSnapshot,
    WealthGoal,
    Workspace,
)
from services.goal_context import GoalContextIntegrityError, build_goal_context
from services.wealth_review import (
    AVAILABLE,
    COMPLETE,
    OVER_ALLOCATED,
    PARTIAL,
    SUPPORTED,
    UNAVAILABLE,
    WealthReviewIntegrityError,
    build_factual_wealth_review,
)
from services.goal_intelligence import CONTRACT_VERSION, build_goal_intelligence


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def workspace(db, name="Workspace"):
    row = Workspace(name=name)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def goal(db, workspace_id, name="Goal", *, target_amount=1_000, target_date=None, archived=False):
    row = WealthGoal(
        workspace_id=workspace_id,
        name=name,
        goal_type="HOUSE",
        target_amount=target_amount,
        currency="THB",
        priority="HIGH",
        target_date=target_date,
        is_archived=archived,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def cash(db, workspace_id, name="Cash", *, balance=0, archived=False):
    row = CashAccount(
        workspace_id=workspace_id, name=name, currency="THB", balance=balance, is_archived=archived,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def portfolio(db, workspace_id, name="Portfolio"):
    row = Portfolio(workspace_id=workspace_id, name=name)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def allocation(db, workspace_id, goal_id, amount, *, cash_id=None, portfolio_id=None):
    row = GoalFundingAllocation(
        workspace_id=workspace_id,
        wealth_goal_id=goal_id,
        cash_account_id=cash_id,
        portfolio_id=portfolio_id,
        allocated_amount=amount,
        currency="THB",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def snapshot(db, workspace_id, portfolio_id, *, total=1_000, snapshot_date="2025-01-01", holdings=None):
    if holdings is None:
        holdings = [{"symbol": "AAA", "price_missing": False}]
    row = PortfolioSnapshot(
        workspace_id=workspace_id,
        portfolio_id=portfolio_id,
        snapshot_date=snapshot_date,
        total_value=total,
        cash_balance=0,
        total_invested=0,
        holdings_json=json.dumps(holdings),
        holdings_count=len(holdings),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def funding_source(intelligence, kind, source_id):
    return next(
        row for row in intelligence["funding_sources"]
        if (row["source_kind"], row["source_id"]) == (kind, source_id)
    )


TODAY = date(2026, 9, 8)


# 1. contract version and shape
def test_contract_version_and_shape():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert result["contract_version"] == CONTRACT_VERSION
    assert set(result) == {
        "contract_version", "generated_at", "goal_id", "as_of_date",
        "funding", "time", "funding_sources", "valuation_completeness",
    }
    assert result["goal_id"] == item.id
    assert result["as_of_date"] == "2026-09-08"


# 2. normal goal with cash funding
def test_normal_goal_with_cash_funding():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=1_000)
    account = cash(db, ws.id, balance=400)
    allocation(db, ws.id, item.id, 400, cash_id=account.id)

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert result["funding"] == {
        "designated_total": 400,
        "progress_ratio": 0.4,
        "funding_gap": 600,
        "fully_designated": False,
    }
    row = funding_source(result, "CASH_ACCOUNT", account.id)
    assert row["goal_designated_amount"] == 400
    assert row["valuation"]["observed_value"] == 400
    assert row["designation_coverage"] == {"status": SUPPORTED, "shortfall": 0}


# 3. normal goal with portfolio funding
def test_normal_goal_with_portfolio_funding():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=1_000)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 500, portfolio_id=investments.id)
    snapshot(db, ws.id, investments.id, total=500)

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    row = funding_source(result, "PORTFOLIO", investments.id)
    assert row["valuation"]["observed_value"] == 500
    assert row["designation_coverage"] == {"status": SUPPORTED, "shortfall": 0}


# 4. multiple funding sources
def test_multiple_funding_sources():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=1_000)
    account = cash(db, ws.id, balance=300)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 300, cash_id=account.id)
    allocation(db, ws.id, item.id, 200, portfolio_id=investments.id)
    snapshot(db, ws.id, investments.id, total=200)

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert len(result["funding_sources"]) == 2
    assert result["funding"]["designated_total"] == 500


# 5. zero designated funding
def test_zero_designated_funding():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=1_000)

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert result["funding"] == {
        "designated_total": 0,
        "progress_ratio": 0.0,
        "funding_gap": 1_000,
        "fully_designated": False,
    }
    assert result["funding_sources"] == []
    assert result["valuation_completeness"] == COMPLETE


# 6. over-designated goal / progress > 100%
def test_over_designated_goal_progress_exceeds_100_percent():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=100)
    account = cash(db, ws.id, balance=500)
    allocation(db, ws.id, item.id, 500, cash_id=account.id)

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert result["funding"]["progress_ratio"] == 5.0
    assert result["funding"]["funding_gap"] == 0
    assert result["funding"]["fully_designated"] is True


# 7. no target date
def test_no_target_date():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_date=None)

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert result["time"] == {
        "target_date": None,
        "has_target_date": False,
        "days_remaining": None,
        "target_date_in_past": False,
    }


# 8. future target date
def test_future_target_date():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_date="2026-09-18")

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert result["time"] == {
        "target_date": "2026-09-18",
        "has_target_date": True,
        "days_remaining": 10,
        "target_date_in_past": False,
    }


# 9. target date == as-of date
def test_target_date_equals_as_of_date():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_date="2026-09-08")

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert result["time"]["days_remaining"] == 0
    assert result["time"]["target_date_in_past"] is False


# 10. past target date
def test_past_target_date_does_not_fail():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_date="2026-08-01")

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert result["time"]["days_remaining"] == -38
    assert result["time"]["target_date_in_past"] is True
    assert not ({"expired", "late", "failed"} & set(result["time"]))


# 11. archived goal remains readable
def test_archived_goal_remains_readable():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, archived=True)

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert result is not None
    assert result["goal_id"] == item.id


# 12. missing valuation evidence
def test_missing_valuation_evidence_is_unavailable_not_zero():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 100, portfolio_id=investments.id)

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    row = funding_source(result, "PORTFOLIO", investments.id)
    assert row["valuation"]["availability"] == UNAVAILABLE
    assert row["valuation"]["observed_value"] is None
    assert row["designation_coverage"] == {"status": UNAVAILABLE, "shortfall": None}
    assert result["valuation_completeness"] == UNAVAILABLE


# 13. partial/unavailable portfolio valuation evidence
def test_partial_price_coverage_surfaces_as_partial():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 100, portfolio_id=investments.id)
    snapshot(db, ws.id, investments.id, total=100, holdings=[{"symbol": "AAA", "price_missing": True}])

    result = build_goal_intelligence(db, ws.id, item.id, TODAY)

    row = funding_source(result, "PORTFOLIO", investments.id)
    assert row["valuation"]["quality"] == PARTIAL
    assert row["designation_coverage"] == {"status": UNAVAILABLE, "shortfall": None}
    assert result["valuation_completeness"] == PARTIAL


# 14. source shared across multiple goals
def test_source_shared_across_multiple_goals_exposes_scope_total():
    db = make_session()
    ws = workspace(db)
    first = goal(db, ws.id, "First")
    second = goal(db, ws.id, "Second")
    account = cash(db, ws.id, balance=1_000)
    allocation(db, ws.id, first.id, 200, cash_id=account.id)
    allocation(db, ws.id, second.id, 350, cash_id=account.id)

    result = build_goal_intelligence(db, ws.id, first.id, TODAY)

    row = funding_source(result, "CASH_ACCOUNT", account.id)
    assert row["goal_designated_amount"] == 200
    assert row["source_designated_total_in_context_scope"] == 550


# 15. source over-allocated across multiple goals
def test_source_over_allocated_across_goals_is_source_level_not_attributed_to_one_goal():
    db = make_session()
    ws = workspace(db)
    first = goal(db, ws.id, "First")
    second = goal(db, ws.id, "Second")
    account = cash(db, ws.id, balance=100)
    allocation(db, ws.id, first.id, 80, cash_id=account.id)
    allocation(db, ws.id, second.id, 90, cash_id=account.id)

    first_result = build_goal_intelligence(db, ws.id, first.id, TODAY)
    second_result = build_goal_intelligence(db, ws.id, second.id, TODAY)

    first_row = funding_source(first_result, "CASH_ACCOUNT", account.id)
    second_row = funding_source(second_result, "CASH_ACCOUNT", account.id)
    # Both goals see the identical source-level fact — neither is told it
    # alone owns the shortfall.
    assert first_row["designation_coverage"] == {"status": OVER_ALLOCATED, "shortfall": 70}
    assert second_row["designation_coverage"] == {"status": OVER_ALLOCATED, "shortfall": 70}
    assert first_row["source_designated_total_in_context_scope"] == 170
    assert second_row["source_designated_total_in_context_scope"] == 170


# 16. funding equality with canonical Goal Context
def test_funding_facts_equal_canonical_goal_context():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=1_000)
    account = cash(db, ws.id, balance=300)
    allocation(db, ws.id, item.id, 300, cash_id=account.id)

    intelligence = build_goal_intelligence(db, ws.id, item.id, TODAY)
    context = build_goal_context(db, ws.id, item.id)
    canonical_goal = context["goals"][0]

    assert intelligence["funding"] == {
        "designated_total": canonical_goal["designated_total"],
        "progress_ratio": canonical_goal["progress_ratio"],
        "funding_gap": canonical_goal["funding_gap"],
        "fully_designated": canonical_goal["fully_designated"],
    }


# 17. source coverage equality with canonical Factual Wealth Review
def test_source_coverage_equals_canonical_factual_wealth_review():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=1_000)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 500, portfolio_id=investments.id)
    snapshot(db, ws.id, investments.id, total=450)

    intelligence = build_goal_intelligence(db, ws.id, item.id, TODAY)
    review = build_factual_wealth_review(db, ws.id, include_archived=True)
    canonical_source = next(
        row for row in review["sources"]
        if (row["source_kind"], row["source_id"]) == ("PORTFOLIO", investments.id)
    )

    row = funding_source(intelligence, "PORTFOLIO", investments.id)
    assert row["valuation"] == canonical_source["valuation"]
    assert row["designation_coverage"] == canonical_source["designation_coverage"]
    assert row["source_designated_total_in_context_scope"] == canonical_source["designated_total_in_context_scope"]


# 18. missing goal -> 404
def test_missing_goal_returns_404(monkeypatch):
    db = make_session()
    ws = workspace(db)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)

    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.get_goal_intelligence(goal_id=999999, db=db))
    assert exc.value.status_code == 404
    assert exc.value.detail == "Wealth goal not found"


# 19. foreign workspace -> non-enumerating 404
def test_foreign_workspace_goal_returns_same_404_as_missing(monkeypatch):
    db = make_session()
    ws = workspace(db)
    other = workspace(db, "Other")
    foreign_goal = goal(db, other.id)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)

    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.get_goal_intelligence(goal_id=foreign_goal.id, db=db))
    assert exc.value.status_code == 404
    assert exc.value.detail == "Wealth goal not found"


# 20. canonical integrity failure -> stable 409
def test_integrity_failure_maps_to_stable_nonleaking_409(monkeypatch):
    db = make_session()
    ws = workspace(db)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)

    monkeypatch.setattr(
        main,
        "build_goal_intelligence",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            WealthReviewIntegrityError("foreign workspace Secret Name")
        ),
    )
    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.get_goal_intelligence(goal_id=1, db=db))
    assert exc.value.status_code == 409
    assert exc.value.detail == {
        "code": "WEALTH_REVIEW_DATA_INTEGRITY",
        "message": "Factual wealth review evidence failed integrity validation.",
    }
    assert "Secret" not in str(exc.value.detail)

    monkeypatch.setattr(
        main,
        "build_goal_intelligence",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            GoalContextIntegrityError("goal corruption")
        ),
    )
    with pytest.raises(HTTPException) as goal_exc:
        asyncio.run(main.get_goal_intelligence(goal_id=1, db=db))
    assert goal_exc.value.detail["code"] == "GOAL_CONTEXT_DATA_INTEGRITY"


def test_endpoint_returns_intelligence_via_http(monkeypatch):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=1_000)
    account = cash(db, ws.id, balance=250)
    allocation(db, ws.id, item.id, 250, cash_id=account.id)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)

    endpoint_app = FastAPI()
    endpoint_app.add_api_route(
        "/wealth-goals/{goal_id}/intelligence",
        main.get_goal_intelligence,
        methods=["GET"],
    )
    endpoint_app.dependency_overrides[main.get_db] = lambda: db

    response = TestClient(endpoint_app).get(f"/wealth-goals/{item.id}/intelligence")

    assert response.status_code == 200
    payload = response.json()
    assert payload["contract_version"] == CONTRACT_VERSION
    assert payload["funding"]["designated_total"] == 250


# 21. no write/persistence side effect
def test_no_persistence_side_effect():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=1_000)
    account = cash(db, ws.id, balance=250)
    allocation(db, ws.id, item.id, 250, cash_id=account.id)

    statements = []
    from sqlalchemy import event

    @event.listens_for(db.bind, "before_cursor_execute")
    def record_statements(_conn, _cursor, statement, _parameters, _context, _executemany):
        statements.append(statement.lstrip().split(None, 1)[0].upper())

    build_goal_intelligence(db, ws.id, item.id, TODAY)

    assert set(statements) == {"SELECT"}
    assert not db.new and not db.dirty and not db.deleted


# 22. no optimizer/Decision Intelligence dependency
def test_module_imports_stay_within_descriptive_composition_boundary():
    service_path = Path(__file__).resolve().parents[1] / "services" / "goal_intelligence.py"
    tree = ast.parse(service_path.read_text(encoding="utf-8"))
    imported = {
        node.module for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert imported <= {"__future__", "datetime", "sqlalchemy.orm", "services.wealth_review"}


def test_no_behavioral_module_imports_goal_intelligence():
    backend_dir = Path(__file__).resolve().parents[1]
    forbidden_dirs = [
        backend_dir / "services" / "optimizer",
        backend_dir / "services" / "decision_memory",
    ]
    forbidden_files = [
        backend_dir / "services" / "decision_goal_context.py",
        backend_dir / "services" / "goal_recommendation_constraints.py",
    ]
    candidates = list(forbidden_files)
    for directory in forbidden_dirs:
        if directory.exists():
            candidates.extend(directory.rglob("*.py"))

    for path in candidates:
        if not path.exists():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "services.goal_intelligence":
                pytest.fail(f"{path} imports services.goal_intelligence")
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "services.goal_intelligence":
                        pytest.fail(f"{path} imports services.goal_intelligence")
