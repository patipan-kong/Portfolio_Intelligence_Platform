"""Focused contract and integrity coverage for Phase 7.2 Goal Context."""
import ast
import asyncio
import json
import math
import os
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models.database import (
    Base,
    CashAccount,
    GoalFundingAllocation,
    Portfolio,
    WealthGoal,
    Workspace,
)
import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
import main
from services.goal_context import (
    COMPLETE,
    CONTRACT_VERSION,
    GoalContextIntegrityError,
    _validate_allocations,
    aggregate_designations_by_source,
    build_goal_context,
    build_workspace_goal_context,
    compute_goal_funding,
)


FIXTURE = json.loads((Path(__file__).resolve().parents[2] / "test-fixtures" / "goal-funding-golden.json").read_text())


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def workspace(db, name="Workspace"):
    item = Workspace(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def goal(db, workspace_id, name="Goal", target_amount=500_000.0, is_archived=False, **overrides):
    item = WealthGoal(
        workspace_id=workspace_id,
        name=name,
        goal_type="HOUSE",
        target_amount=target_amount,
        currency="THB",
        priority="HIGH",
        is_archived=is_archived,
        **overrides,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def cash(db, workspace_id, name="Cash", is_archived=False, **overrides):
    item = CashAccount(
        workspace_id=workspace_id,
        name=name,
        currency="THB",
        balance=0,
        is_archived=is_archived,
        **overrides,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def portfolio(db, workspace_id, name="Portfolio"):
    item = Portfolio(workspace_id=workspace_id, name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def allocation(db, workspace_id, wealth_goal_id, amount, cash_account_id=None, portfolio_id=None, **overrides):
    item = GoalFundingAllocation(
        workspace_id=workspace_id,
        wealth_goal_id=wealth_goal_id,
        cash_account_id=cash_account_id,
        portfolio_id=portfolio_id,
        allocated_amount=amount,
        currency="THB",
        **overrides,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def test_shared_fixture_metadata_and_valid_goal_funding_parity():
    assert FIXTURE["schema_version"] == 1
    assert FIXTURE["contract_version"] == CONTRACT_VERSION
    for case in FIXTURE["goal_funding_cases"]:
        if (
            not isinstance(case["target_amount"], (int, float))
            or case["target_amount"] <= 0
            or any(not isinstance(row["amount"], (int, float)) or not math.isfinite(row["amount"]) for row in case["allocations"])
        ):
            continue  # invalid persisted targets are integrity failures, not successful context facts.
        result = compute_goal_funding(
            case["target_amount"],
            [SimpleNamespace(allocated_amount=row["amount"]) for row in case["allocations"]],
        )
        assert result == case["expected"], case["id"]


def test_shared_fixture_source_aggregation_parity_and_typed_source_identity():
    for case in FIXTURE["source_aggregation_cases"]:
        evidence = [
            SimpleNamespace(
                cash_account_id=row["source_id"] if row["source_kind"] == "CASH_ACCOUNT" else None,
                portfolio_id=row["source_id"] if row["source_kind"] == "PORTFOLIO" else None,
                allocated_amount=row["amount"],
            )
            for row in case["allocations"]
        ]
        totals = aggregate_designations_by_source(evidence)
        expected = {(row["source_kind"], row["source_id"]): row["designated_total"] for row in case["expected"]}
        assert totals == expected, case["id"]


def test_workspace_context_empty_and_goal_without_allocations_are_complete():
    db = make_session()
    ws = workspace(db)
    empty = build_workspace_goal_context(db, ws.id)
    assert empty["completeness"] == COMPLETE
    assert empty["goals"] == []
    assert empty["designation_by_source"] == []

    item = goal(db, ws.id, target_amount=500_000)
    context = build_workspace_goal_context(db, ws.id)
    facts = context["goals"][0]
    assert context["contract_version"] == CONTRACT_VERSION
    assert context["scope"] == {"kind": "WORKSPACE", "include_archived": False}
    assert context["context_generated_at"].endswith("+00:00")
    assert facts["id"] == item.id
    assert facts["allocations"] == []
    assert {key: facts[key] for key in ("designated_total", "progress_ratio", "progress_percent", "funding_gap", "fully_designated")} == {
        "designated_total": 0,
        "progress_ratio": 0,
        "progress_percent": 0,
        "funding_gap": 500_000,
        "fully_designated": False,
    }


def test_context_derives_multiple_goal_facts_and_source_aggregate_without_valuation():
    db = make_session()
    ws = workspace(db)
    house = goal(db, ws.id, "House", target_amount=1_000)
    retirement = goal(db, ws.id, "Retirement", target_amount=2_000)
    account = cash(db, ws.id, "Shared cash")
    investments = portfolio(db, ws.id, "Investments")
    allocation(db, ws.id, house.id, 600, cash_account_id=account.id)
    allocation(db, ws.id, house.id, 600, portfolio_id=investments.id)
    allocation(db, ws.id, retirement.id, 500, cash_account_id=account.id)

    context = build_workspace_goal_context(db, ws.id)
    by_name = {item["name"]: item for item in context["goals"]}
    assert by_name["House"]["progress_percent"] == 120
    assert by_name["House"]["funding_gap"] == 0
    assert by_name["House"]["fully_designated"] is True
    assert by_name["Retirement"]["progress_percent"] == 25
    aggregates = {(row["source_kind"], row["source_id"]): row for row in context["designation_by_source"]}
    assert aggregates[("CASH_ACCOUNT", account.id)]["designated_total_in_context_scope"] == 1_100
    assert aggregates[("PORTFOLIO", investments.id)]["designated_total_in_context_scope"] == 600
    assert "current_value" not in str(context)


def test_archive_scope_and_exact_archived_goal_are_preserved():
    db = make_session()
    ws = workspace(db)
    active = goal(db, ws.id, "Active")
    archived = goal(db, ws.id, "Archived", is_archived=True)
    account = cash(db, ws.id, "Archived cash", is_archived=True)
    allocation(db, ws.id, active.id, 10, cash_account_id=account.id)
    allocation(db, ws.id, archived.id, 20, cash_account_id=account.id)

    active_only = build_workspace_goal_context(db, ws.id)
    assert [item["id"] for item in active_only["goals"]] == [active.id]
    assert active_only["designation_by_source"][0]["designated_total_in_context_scope"] == 10
    all_goals = build_workspace_goal_context(db, ws.id, include_archived=True)
    assert {item["id"] for item in all_goals["goals"]} == {active.id, archived.id}
    assert all_goals["designation_by_source"][0]["designated_total_in_context_scope"] == 30
    assert all_goals["designation_by_source"][0]["source_is_archived"] is True
    exact = build_goal_context(db, ws.id, archived.id)
    assert exact is not None and exact["scope"] == {"kind": "GOAL", "goal_id": archived.id}
    assert exact["goals"][0]["is_archived"] is True


def test_exact_goal_missing_or_foreign_is_none_and_api_keeps_non_leaking_404():
    db = make_session()
    own = workspace(db, "Own")
    foreign = workspace(db, "Foreign")
    foreign_goal = goal(db, foreign.id)
    assert build_goal_context(db, own.id, 999) is None
    assert build_goal_context(db, own.id, foreign_goal.id) is None
    with pytest.raises(HTTPException) as error:
        asyncio.run(main.get_goal_context(foreign_goal.id, db))
    assert error.value.status_code == 404
    assert error.value.detail == "Wealth goal not found"


@pytest.mark.parametrize(
    "allocation_evidence",
    [
        [SimpleNamespace(wealth_goal_id=1, workspace_id=1, currency="THB", allocated_amount=1, cash_account_id=1, portfolio_id=1)],
        [SimpleNamespace(wealth_goal_id=1, workspace_id=1, currency="THB", allocated_amount=1, cash_account_id=None, portfolio_id=None)],
        [SimpleNamespace(wealth_goal_id=1, workspace_id=1, currency="USD", allocated_amount=1, cash_account_id=1, portfolio_id=None)],
        [SimpleNamespace(wealth_goal_id=1, workspace_id=1, currency="THB", allocated_amount=0, cash_account_id=1, portfolio_id=None)],
        [SimpleNamespace(wealth_goal_id=1, workspace_id=1, currency="THB", allocated_amount=math.nan, cash_account_id=1, portfolio_id=None)],
        [
            SimpleNamespace(wealth_goal_id=1, workspace_id=1, currency="THB", allocated_amount=1, cash_account_id=1, portfolio_id=None),
            SimpleNamespace(wealth_goal_id=1, workspace_id=1, currency="THB", allocated_amount=2, cash_account_id=1, portfolio_id=None),
        ],
    ],
)
def test_structural_corruption_is_rejected(allocation_evidence):
    if not isinstance(allocation_evidence[0], list):
        allocation_evidence = allocation_evidence
    goals = {1: SimpleNamespace(id=1, workspace_id=1)}
    with pytest.raises(GoalContextIntegrityError):
        _validate_allocations(allocation_evidence, goals, 1)


def test_invalid_goal_source_and_workspace_evidence_fail_entire_context_and_api_is_safe_409():
    db = make_session()
    ws = workspace(db, "Own")
    other = workspace(db, "Other")
    item = goal(db, ws.id)
    foreign_cash = cash(db, other.id)
    # SQLite's default test configuration permits this orphaned cross-workspace
    # reference, which is exactly the persisted corruption the reader must find.
    allocation(db, ws.id, item.id, 1, cash_account_id=foreign_cash.id)
    with pytest.raises(GoalContextIntegrityError):
        build_workspace_goal_context(db, ws.id)
    with pytest.raises(HTTPException) as error:
        asyncio.run(main.get_workspace_goal_context(False, db))
    assert error.value.status_code == 409
    assert error.value.detail == {
        "code": "GOAL_CONTEXT_DATA_INTEGRITY",
        "message": "Goal Context evidence failed integrity validation.",
    }


def test_goal_and_allocation_workspace_disagreement_is_detected():
    db = make_session()
    ws = workspace(db, "Own")
    other = workspace(db, "Other")
    item = goal(db, ws.id)
    source = cash(db, ws.id)
    row = allocation(db, ws.id, item.id, 1, cash_account_id=source.id)
    db.execute(text("UPDATE goal_funding_allocations SET workspace_id = :workspace WHERE id = :id"), {"workspace": other.id, "id": row.id})
    db.commit()
    db.expire_all()
    with pytest.raises(GoalContextIntegrityError):
        build_workspace_goal_context(db, ws.id)


@pytest.mark.parametrize("source_kind", ["CASH_ACCOUNT", "PORTFOLIO"])
def test_missing_referenced_source_fails_the_entire_context(source_kind):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    if source_kind == "CASH_ACCOUNT":
        source = cash(db, ws.id)
        allocation(db, ws.id, item.id, 1, cash_account_id=source.id)
        db.execute(text("DELETE FROM cash_accounts WHERE id = :id"), {"id": source.id})
    else:
        source = portfolio(db, ws.id)
        allocation(db, ws.id, item.id, 1, portfolio_id=source.id)
        db.execute(text("DELETE FROM portfolios WHERE id = :id"), {"id": source.id})
    db.commit()
    db.expire_all()
    with pytest.raises(GoalContextIntegrityError):
        build_workspace_goal_context(db, ws.id)


@pytest.mark.parametrize("source_kind", ["CASH_ACCOUNT", "PORTFOLIO"])
def test_foreign_referenced_source_fails_the_entire_context(source_kind):
    db = make_session()
    ws = workspace(db, "Own")
    other = workspace(db, "Other")
    item = goal(db, ws.id)
    if source_kind == "CASH_ACCOUNT":
        source = cash(db, other.id)
        allocation(db, ws.id, item.id, 1, cash_account_id=source.id)
    else:
        source = portfolio(db, other.id)
        allocation(db, ws.id, item.id, 1, portfolio_id=source.id)
    with pytest.raises(GoalContextIntegrityError):
        build_workspace_goal_context(db, ws.id)


@pytest.mark.parametrize(
    "table,column,value",
    [
        ("wealth_goals", "target_amount", 0),
        ("wealth_goals", "currency", "USD"),
        ("goal_funding_allocations", "allocated_amount", 0),
        ("goal_funding_allocations", "currency", "USD"),
        ("cash_accounts", "currency", "USD"),
    ],
)
def test_invalid_persisted_facts_fail_integrity_validation(table, column, value):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    source = cash(db, ws.id)
    allocation_row = allocation(db, ws.id, item.id, 1, cash_account_id=source.id)
    row_id = {"wealth_goals": item.id, "goal_funding_allocations": allocation_row.id, "cash_accounts": source.id}[table]
    db.execute(text("PRAGMA ignore_check_constraints = ON"))
    db.execute(text(f"UPDATE {table} SET {column} = :value WHERE id = :id"), {"value": value, "id": row_id})
    db.commit()
    db.expire_all()
    with pytest.raises(GoalContextIntegrityError):
        build_workspace_goal_context(db, ws.id)


@pytest.mark.parametrize(
    "cash_account_id,portfolio_id",
    [(1, 1), (None, None)],
)
def test_persisted_malformed_source_shape_fails_integrity_validation(cash_account_id, portfolio_id):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    account = cash(db, ws.id)
    investments = portfolio(db, ws.id)
    row = allocation(db, ws.id, item.id, 1, cash_account_id=account.id)
    db.execute(text("PRAGMA ignore_check_constraints = ON"))
    db.execute(
        text("UPDATE goal_funding_allocations SET cash_account_id = :cash, portfolio_id = :portfolio WHERE id = :id"),
        {"cash": account.id if cash_account_id is not None else None, "portfolio": investments.id if portfolio_id is not None else None, "id": row.id},
    )
    db.commit()
    db.expire_all()
    with pytest.raises(GoalContextIntegrityError):
        build_workspace_goal_context(db, ws.id)


def test_duplicate_same_goal_source_corruption_is_rejected_before_assembly():
    goal_evidence = {1: SimpleNamespace(id=1, workspace_id=1)}
    duplicate_rows = [
        SimpleNamespace(id=1, wealth_goal_id=1, workspace_id=1, currency="THB", allocated_amount=1, cash_account_id=1, portfolio_id=None),
        SimpleNamespace(id=2, wealth_goal_id=1, workspace_id=1, currency="THB", allocated_amount=2, cash_account_id=1, portfolio_id=None),
    ]
    # The database unique constraint prevents manufacturing this state through
    # SQL in SQLite; validation still rejects it if historical/corrupt evidence
    # reaches the set-based reader.
    with pytest.raises(GoalContextIntegrityError):
        _validate_allocations(duplicate_rows, goal_evidence, 1)


def test_built_response_keeps_same_numeric_cash_and_portfolio_ids_distinct_and_has_provenance():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    account = cash(db, ws.id)
    investments = portfolio(db, ws.id)
    # Each table starts its independent primary-key sequence at 1.
    assert account.id == investments.id
    allocation(db, ws.id, item.id, 10, cash_account_id=account.id)
    allocation(db, ws.id, item.id, 20, portfolio_id=investments.id)
    context = build_workspace_goal_context(db, ws.id)
    allocations = context["goals"][0]["allocations"]
    assert {(row["source_kind"], row["source_id"]) for row in allocations} == {
        ("CASH_ACCOUNT", account.id), ("PORTFOLIO", investments.id)
    }
    assert all({"id", "wealth_goal_id", "source_name", "source_is_archived", "designated_amount", "currency", "updated_at"} <= row.keys() for row in allocations)
    assert all({"id", "name", "goal_type", "target_amount", "currency", "target_date", "priority", "is_archived", "updated_at"} <= row.keys() for row in context["goals"])


def test_route_registration_preserves_static_first_order_and_framework_integer_validation():
    routes = [route for route in main.app.routes if getattr(route, "path", "").startswith("/wealth-goals")]
    paths = [route.path for route in routes]
    assert paths.index("/wealth-goals/context") < paths.index("/wealth-goals/{goal_id}/context")
    assert any(route.path == "/wealth-goals/{goal_id}/context" for route in routes)

    # A minimal app exercises FastAPI's real path coercion without invoking
    # main.app's authentication middleware or production lifespan/database.
    validation_app = FastAPI()
    validation_app.add_api_route("/wealth-goals/{goal_id}/context", main.get_goal_context, methods=["GET"])
    client = TestClient(validation_app)
    response = client.get("/wealth-goals/not-an-integer/context")
    assert response.status_code == 422


def test_deterministic_ordering_and_bounded_set_queries():
    db = make_session()
    ws = workspace(db)
    zulu = goal(db, ws.id, "Zulu")
    alpha = goal(db, ws.id, "Alpha")
    cash_source = cash(db, ws.id, "Z cash")
    portfolio_source = portfolio(db, ws.id, "A portfolio")
    allocation(db, ws.id, zulu.id, 1, cash_account_id=cash_source.id)
    allocation(db, ws.id, alpha.id, 2, portfolio_id=portfolio_source.id)
    ws_id = ws.id
    statements = []

    def track(_, __, statement, ___, ____, _____):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(db.bind, "before_cursor_execute", track)
    try:
        context = build_workspace_goal_context(db, ws_id)
    finally:
        event.remove(db.bind, "before_cursor_execute", track)
    assert [item["name"] for item in context["goals"]] == ["Alpha", "Zulu"]
    assert [item["source_name"] for item in context["designation_by_source"]] == ["A portfolio", "Z cash"]
    assert len(statements) == 4  # goals, allocations, one CashAccount set query, one Portfolio set query


def test_goal_context_service_has_no_market_or_valuation_dependency():
    source = Path(__file__).resolve().parents[1] / "services" / "goal_context.py"
    tree = ast.parse(source.read_text())
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert not any(
        forbidden in name
        for name in imported
        for forbidden in ("data_fetcher", "portfolio_snapshots", "optimizer", "goal_profile", "market")
    )
