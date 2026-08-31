"""Phase 7.3A factual wealth-review contract, integrity, and I/O tests."""

import ast
import asyncio
from datetime import datetime
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, text
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
from services.goal_context import GoalContextIntegrityError
from services.wealth_review import (
    AVAILABLE,
    COMPLETE,
    CONTRACT_VERSION,
    OVER_ALLOCATED,
    PARTIAL,
    SUPPORTED,
    UNAVAILABLE,
    UNKNOWN,
    WealthReviewIntegrityError,
    build_factual_wealth_review,
)


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


def goal(db, workspace_id, name="Goal", *, archived=False):
    row = WealthGoal(
        workspace_id=workspace_id,
        name=name,
        goal_type="HOUSE",
        target_amount=1_000,
        currency="THB",
        priority="HIGH",
        is_archived=archived,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def cash(db, workspace_id, name="Cash", *, balance=0, archived=False):
    row = CashAccount(
        workspace_id=workspace_id,
        name=name,
        currency="THB",
        balance=balance,
        is_archived=archived,
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


def snapshot(
    db,
    workspace_id,
    portfolio_id,
    *,
    total=1_000,
    snapshot_date="2025-01-01",
    holdings=None,
    holdings_json=...,
    holdings_count=...,
):
    if holdings is None:
        holdings = [{"symbol": "AAA", "price_missing": False}]
    if holdings_json is ...:
        holdings_json = json.dumps(holdings)
    if holdings_count is ...:
        holdings_count = len(holdings)
    row = PortfolioSnapshot(
        workspace_id=workspace_id,
        portfolio_id=portfolio_id,
        snapshot_date=snapshot_date,
        total_value=total,
        cash_balance=0,
        total_invested=0,
        holdings_json=holdings_json,
        holdings_count=holdings_count,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def source(review, kind, source_id):
    return next(
        row
        for row in review["sources"]
        if (row["source_kind"], row["source_id"]) == (kind, source_id)
    )


def test_contract_embeds_unchanged_goal_context_and_keeps_typed_ids_distinct():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    account = cash(db, ws.id, balance=400)
    investments = portfolio(db, ws.id)
    assert account.id == investments.id == 1
    allocation(db, ws.id, item.id, 300, cash_id=account.id)
    allocation(db, ws.id, item.id, 500, portfolio_id=investments.id)
    snapshot(db, ws.id, investments.id, total=450)

    review = build_factual_wealth_review(db, ws.id)

    assert review["contract_version"] == CONTRACT_VERSION
    assert review["scope"] == review["goal_context"]["scope"]
    assert review["goal_context"]["contract_version"] == "wealth.goal-context.v1"
    assert len(review["sources"]) == 2
    assert source(review, "CASH_ACCOUNT", 1)["designation_coverage"] == {
        "status": SUPPORTED,
        "shortfall": 0,
    }
    assert source(review, "PORTFOLIO", 1)["designation_coverage"] == {
        "status": OVER_ALLOCATED,
        "shortfall": 50,
    }


def test_shared_source_aggregates_across_goals_without_reimplementing_goal_math():
    db = make_session()
    ws = workspace(db)
    first = goal(db, ws.id, "First")
    second = goal(db, ws.id, "Second")
    account = cash(db, ws.id, balance=1_000)
    allocation(db, ws.id, first.id, 200, cash_id=account.id)
    allocation(db, ws.id, second.id, 350, cash_id=account.id)

    review = build_factual_wealth_review(db, ws.id)
    row = source(review, "CASH_ACCOUNT", account.id)
    assert row["designated_total_in_context_scope"] == 550
    assert row["designation_coverage"] == {"status": SUPPORTED, "shortfall": 0}
    assert review["goal_context"]["designation_by_source"][0][
        "designated_total_in_context_scope"
    ] == 550


def test_cash_zero_is_available_complete_and_not_unavailable():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    account = cash(db, ws.id, balance=0)
    allocation(db, ws.id, item.id, 25, cash_id=account.id)

    row = source(build_factual_wealth_review(db, ws.id), "CASH_ACCOUNT", account.id)
    assert row["valuation"] == {
        "availability": AVAILABLE,
        "observed_value": 0,
        "as_of": account.updated_at.isoformat(),
        "provenance": "CASH_ACCOUNT_CURRENT_BALANCE",
        "quality": COMPLETE,
    }
    assert row["designation_coverage"] == {
        "status": OVER_ALLOCATED,
        "shortfall": 25,
    }


def test_complete_snapshot_zero_is_valid_as_of_evidence():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 25, portfolio_id=investments.id)
    snapshot(db, ws.id, investments.id, total=0, holdings=[], snapshot_date="2020-01-02")

    row = source(build_factual_wealth_review(db, ws.id), "PORTFOLIO", investments.id)
    assert row["valuation"] == {
        "availability": AVAILABLE,
        "observed_value": 0,
        "as_of": "2020-01-02",
        "provenance": "PORTFOLIO_SNAPSHOT",
        "quality": COMPLETE,
    }
    assert row["designation_coverage"]["status"] == OVER_ALLOCATED


def test_no_snapshot_is_unavailable_with_explicit_nulls():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 25, portfolio_id=investments.id)

    review = build_factual_wealth_review(db, ws.id)
    row = source(review, "PORTFOLIO", investments.id)
    assert row["valuation"] == {
        "availability": UNAVAILABLE,
        "observed_value": None,
        "as_of": None,
        "provenance": None,
        "quality": None,
    }
    assert row["designation_coverage"] == {"status": UNAVAILABLE, "shortfall": None}
    assert review["valuation_completeness"] == UNAVAILABLE


@pytest.mark.parametrize(
    ("holdings_json", "holdings_count", "quality"),
    [
        (json.dumps([{"symbol": "AAA", "price_missing": True}]), 1, PARTIAL),
        (None, None, UNKNOWN),
        (json.dumps([{"symbol": "AAA"}]), 1, UNKNOWN),
    ],
)
def test_partial_or_historical_unknown_snapshot_exposes_observation_but_not_coverage(
    holdings_json, holdings_count, quality
):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 50, portfolio_id=investments.id)
    snapshot(
        db,
        ws.id,
        investments.id,
        total=5_000,
        holdings_json=holdings_json,
        holdings_count=holdings_count,
    )

    review = build_factual_wealth_review(db, ws.id)
    row = source(review, "PORTFOLIO", investments.id)
    assert row["valuation"]["availability"] == AVAILABLE
    assert row["valuation"]["observed_value"] == 5_000
    assert row["valuation"]["quality"] == quality
    assert row["designation_coverage"] == {"status": UNAVAILABLE, "shortfall": None}
    assert review["valuation_completeness"] == PARTIAL


def test_very_old_complete_snapshot_remains_as_of_without_freshness_claim():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 1, portfolio_id=investments.id)
    snapshot(db, ws.id, investments.id, snapshot_date="1999-12-31")

    review = build_factual_wealth_review(db, ws.id)
    row = source(review, "PORTFOLIO", investments.id)
    assert row["valuation"]["as_of"] == "1999-12-31"
    assert row["valuation"]["quality"] == COMPLETE
    assert not ({"stale", "fresh", "is_stale"} & set(row["valuation"]))


def test_archived_cash_remains_visible_and_valued():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    account = cash(db, ws.id, balance=500, archived=True)
    allocation(db, ws.id, item.id, 100, cash_id=account.id)

    row = source(build_factual_wealth_review(db, ws.id), "CASH_ACCOUNT", account.id)
    assert row["source_is_archived"] is True
    assert row["valuation"]["observed_value"] == 500


def test_archived_goal_scope_changes_shared_source_designation_total():
    db = make_session()
    ws = workspace(db)
    active = goal(db, ws.id, "Active")
    archived = goal(db, ws.id, "Archived", archived=True)
    account = cash(db, ws.id, balance=1_000)
    allocation(db, ws.id, active.id, 100, cash_id=account.id)
    allocation(db, ws.id, archived.id, 250, cash_id=account.id)

    active_review = build_factual_wealth_review(db, ws.id)
    all_review = build_factual_wealth_review(db, ws.id, include_archived=True)

    assert active_review["scope"]["include_archived"] is False
    assert source(active_review, "CASH_ACCOUNT", account.id)[
        "designated_total_in_context_scope"
    ] == 100
    assert all_review["scope"]["include_archived"] is True
    assert source(all_review, "CASH_ACCOUNT", account.id)[
        "designated_total_in_context_scope"
    ] == 350
    assert [row["name"] for row in all_review["goal_context"]["goals"]] == [
        "Active",
        "Archived",
    ]


def test_missing_or_foreign_source_preserves_goal_context_integrity_failure():
    db = make_session()
    ws = workspace(db)
    other = workspace(db, "Other")
    item = goal(db, ws.id)
    account = cash(db, ws.id)
    allocation(db, ws.id, item.id, 100, cash_id=account.id)

    account.workspace_id = other.id
    db.commit()
    with pytest.raises(GoalContextIntegrityError):
        build_factual_wealth_review(db, ws.id)

    account.workspace_id = ws.id
    db.commit()
    db.delete(account)
    db.commit()
    with pytest.raises(GoalContextIntegrityError):
        build_factual_wealth_review(db, ws.id)


def test_snapshot_workspace_mismatch_fails_closed_even_when_portfolio_is_owned():
    db = make_session()
    ws = workspace(db)
    other = workspace(db, "Other")
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 100, portfolio_id=investments.id)
    snapshot(db, other.id, investments.id)

    with pytest.raises(WealthReviewIntegrityError):
        build_factual_wealth_review(db, ws.id)


@pytest.mark.parametrize(
    ("holdings_json", "holdings_count"),
    [
        ("not-json", 1),
        (json.dumps({"symbol": "AAA"}), 1),
        (json.dumps(["AAA"]), 1),
        (json.dumps([{"price_missing": "false"}]), 1),
        (json.dumps([{"price_missing": False}]), 2),
        (json.dumps([]), -1),
    ],
)
def test_malformed_or_inconsistent_snapshot_metadata_fails_closed(
    holdings_json, holdings_count
):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, 100, portfolio_id=investments.id)
    db.execute(text("PRAGMA ignore_check_constraints = ON"))
    snapshot(
        db,
        ws.id,
        investments.id,
        holdings_json=holdings_json,
        holdings_count=holdings_count,
    )

    with pytest.raises(WealthReviewIntegrityError):
        build_factual_wealth_review(db, ws.id)


@pytest.mark.parametrize("kind", ["cash-negative", "cash-infinite", "snapshot-negative", "snapshot-infinite"])
def test_negative_or_nonfinite_valuation_fails_closed(kind):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    db.execute(text("PRAGMA ignore_check_constraints = ON"))
    if kind.startswith("cash"):
        account = cash(db, ws.id)
        allocation(db, ws.id, item.id, 100, cash_id=account.id)
        account.balance = -1 if kind.endswith("negative") else float("inf")
    else:
        investments = portfolio(db, ws.id)
        allocation(db, ws.id, item.id, 100, portfolio_id=investments.id)
        row = snapshot(db, ws.id, investments.id)
        row.total_value = -1 if kind.endswith("negative") else float("inf")
    db.commit()

    with pytest.raises(WealthReviewIntegrityError):
        build_factual_wealth_review(db, ws.id)


def test_empty_context_is_complete_and_skips_source_queries():
    db = make_session()
    ws = workspace(db)
    selects = []

    @event.listens_for(db.bind, "before_cursor_execute")
    def record_selects(_conn, _cursor, statement, _parameters, _context, _executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            selects.append(statement)

    review = build_factual_wealth_review(db, ws.id)
    assert review["sources"] == []
    assert review["goal_context"]["goals"] == []
    assert review["valuation_completeness"] == COMPLETE
    assert len(selects) == 1
    assert not any("cash_accounts" in statement for statement in selects)
    assert not any("portfolio_snapshots" in statement for statement in selects)


def test_select_count_is_constant_bounded_and_latest_snapshot_is_set_based():
    db = make_session()
    ws = workspace(db)
    for index in range(4):
        item = goal(db, ws.id, f"Goal {index}")
        account = cash(db, ws.id, f"Cash {index}", balance=1_000)
        investments = portfolio(db, ws.id, f"Portfolio {index}")
        allocation(db, ws.id, item.id, 100, cash_id=account.id)
        allocation(db, ws.id, item.id, 100, portfolio_id=investments.id)
        snapshot(db, ws.id, investments.id, snapshot_date="2024-01-01")
        snapshot(db, ws.id, investments.id, total=2_000, snapshot_date="2025-01-01")
    workspace_id = ws.id
    selects = []

    @event.listens_for(db.bind, "before_cursor_execute")
    def record_selects(_conn, _cursor, statement, _parameters, _context, _executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            selects.append(statement)

    review = build_factual_wealth_review(db, workspace_id)
    assert len(review["sources"]) == 8
    assert len(selects) == 6
    assert sum("portfolio_snapshots" in statement for statement in selects) == 1
    assert sum("cash_accounts" in statement for statement in selects) == 2  # context metadata + valuation


def test_review_is_read_only_and_imports_no_provider_legacy_or_advisory_services():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    account = cash(db, ws.id, balance=500)
    allocation(db, ws.id, item.id, 100, cash_id=account.id)
    statements = []

    @event.listens_for(db.bind, "before_cursor_execute")
    def record_statements(_conn, _cursor, statement, _parameters, _context, _executemany):
        statements.append(statement.lstrip().split(None, 1)[0].upper())

    build_factual_wealth_review(db, ws.id)
    assert set(statements) == {"SELECT"}
    assert not db.new and not db.dirty and not db.deleted

    service_path = Path(__file__).resolve().parents[1] / "services" / "wealth_review.py"
    tree = ast.parse(service_path.read_text(encoding="utf-8"))
    imported = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert imported <= {
        "__future__",
        "datetime",
        "sqlalchemy",
        "sqlalchemy.orm",
        "models.database",
        "services.goal_context",
    }


def test_endpoint_maps_integrity_errors_to_stable_nonleaking_409(monkeypatch):
    db = make_session()
    ws = workspace(db)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)

    monkeypatch.setattr(
        main,
        "build_factual_wealth_review",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            WealthReviewIntegrityError("foreign workspace Secret Name")
        ),
    )
    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.get_factual_wealth_review(db=db))
    assert exc.value.status_code == 409
    assert exc.value.detail == {
        "code": "WEALTH_REVIEW_DATA_INTEGRITY",
        "message": "Factual wealth review evidence failed integrity validation.",
    }
    assert "Secret" not in str(exc.value.detail)

    monkeypatch.setattr(
        main,
        "build_factual_wealth_review",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            GoalContextIntegrityError("goal corruption")
        ),
    )
    with pytest.raises(HTTPException) as goal_exc:
        asyncio.run(main.get_factual_wealth_review(db=db))
    assert goal_exc.value.detail["code"] == "GOAL_CONTEXT_DATA_INTEGRITY"


def test_endpoint_returns_versioned_review_and_parses_archive_scope(monkeypatch):
    db = make_session()
    ws = workspace(db)
    goal(db, ws.id, "Archived", archived=True)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    endpoint_app = FastAPI()
    endpoint_app.add_api_route(
        "/wealth-goals/factual-review",
        main.get_factual_wealth_review,
        methods=["GET"],
    )
    endpoint_app.dependency_overrides[main.get_db] = lambda: db

    response = TestClient(endpoint_app).get(
        "/wealth-goals/factual-review?include_archived=true"
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["contract_version"] == CONTRACT_VERSION
    assert payload["scope"] == {"kind": "WORKSPACE", "include_archived": True}
    assert [row["name"] for row in payload["goal_context"]["goals"]] == [
        "Archived"
    ]


def test_factual_review_static_route_precedes_dynamic_goal_route():
    routes = [
        route.path
        for route in main.app.routes
        if getattr(route, "path", "").startswith("/wealth-goals")
    ]
    assert routes.index("/wealth-goals/factual-review") < routes.index(
        "/wealth-goals/{goal_id}/context"
    )
