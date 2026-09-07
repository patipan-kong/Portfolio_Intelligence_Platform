"""Phase 7.3B designated Portfolio legacy-profile evidence tests."""

import ast
import asyncio
from datetime import datetime
import json
import os
from pathlib import Path
import sys

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
    WealthGoal,
    Workspace,
)
from services.goal_context import GoalContextIntegrityError
from services.legacy_goal_profile_evidence import (
    ALL_FIELDS_RECORDED,
    COMPLETE,
    CONTRACT_VERSION,
    DIFFERENT_RECORDED_CODES,
    DIFFERENT_RECORDED_DATES,
    LegacyGoalProfileEvidenceIntegrityError,
    NORMALIZED,
    NOT_COMPARABLE,
    NO_FIELDS_RECORDED,
    PARTIAL_FIELDS_RECORDED,
    SAME_RECORDED_CODE,
    SAME_RECORDED_DATE,
    UNCHANGED,
    UNRECOGNIZED,
    UNSET,
    UNSPECIFIED_IN_LEGACY_CONTRACT,
    build_legacy_goal_profile_evidence,
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


def goal(
    db,
    workspace_id,
    name="Goal",
    *,
    goal_type="RETIREMENT",
    target_amount=1_000,
    target_date=None,
    archived=False,
):
    row = WealthGoal(
        workspace_id=workspace_id,
        name=name,
        goal_type=goal_type,
        target_amount=target_amount,
        currency="THB",
        target_date=target_date,
        priority="HIGH",
        is_archived=archived,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def portfolio(db, workspace_id, name="Portfolio", **legacy):
    row = Portfolio(workspace_id=workspace_id, name=name, **legacy)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def cash(db, workspace_id, name="Cash"):
    row = CashAccount(
        workspace_id=workspace_id,
        name=name,
        currency="THB",
        balance=1_000,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def allocation(db, workspace_id, goal_id, *, portfolio_id=None, cash_id=None, amount=100):
    row = GoalFundingAllocation(
        workspace_id=workspace_id,
        wealth_goal_id=goal_id,
        portfolio_id=portfolio_id,
        cash_account_id=cash_id,
        allocated_amount=amount,
        currency="THB",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def evidence_for(db, ws_id, item, investments, **kwargs):
    allocation(db, ws_id, item.id, portfolio_id=investments.id)
    response = build_legacy_goal_profile_evidence(db, ws_id, **kwargs)
    assert len(response["evidence_edges"]) == 1
    return response, response["evidence_edges"][0]


def test_contract_embeds_context_and_preserves_raw_normalized_goal_type():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_date="2035-01-01")
    investments = portfolio(
        db,
        ws.id,
        goal_type=" retirement ",
        goal_priority=" important ",
        goal_target_date="2035-01-01",
        goal_target_value=1_000,
        risk_personality="AGGRESSIVE",
    )

    response, edge = evidence_for(db, ws.id, item, investments)

    assert response["contract_version"] == CONTRACT_VERSION
    assert response["completeness"] == COMPLETE
    assert response["scope"] == response["goal_context"]["scope"]
    assert response["goal_context"]["contract_version"] == "wealth.goal-context.v1"
    assert datetime.fromisoformat(response["generated_at"])
    legacy = edge["legacy_profile"]
    assert legacy["evidence_availability"] == ALL_FIELDS_RECORDED
    assert legacy["goal_type"] == {
        "raw_value": " retirement ",
        "compatibility_projection": "RETIREMENT",
        "compatibility_label_th": "เกษียณ",
        "projection_status": NORMALIZED,
        "comparison": SAME_RECORDED_CODE,
        "provenance": "PORTFOLIO.GOAL_TYPE",
    }
    assert legacy["goal_priority"]["compatibility_projection"] == "IMPORTANT"
    assert legacy["goal_priority"]["projection_status"] == NORMALIZED
    assert "comparison" not in legacy["goal_priority"]
    assert legacy["goal_target_value"]["unit_status"] == UNSPECIFIED_IN_LEGACY_CONTRACT
    assert "comparison" not in legacy["goal_target_value"]

    # Real compatibility projection contains these fields; the evidence
    # serializer's allowlist must nevertheless keep all of them out.
    serialized = json.dumps(response)
    assert "risk_personality" not in serialized
    assert "configured" not in serialized


@pytest.mark.parametrize(
    ("raw", "canonical", "projection", "status", "comparison"),
    [
        ("RETIREMENT", "HOUSE", "RETIREMENT", UNCHANGED, DIFFERENT_RECORDED_CODES),
        ("OLD_CUSTOM_GOAL", "RETIREMENT", None, UNRECOGNIZED, NOT_COMPARABLE),
        ("   ", "RETIREMENT", None, UNRECOGNIZED, NOT_COMPARABLE),
        (None, "RETIREMENT", None, UNSET, NOT_COMPARABLE),
    ],
)
def test_goal_type_comparison_uses_only_recognized_projection(
    raw, canonical, projection, status, comparison
):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, goal_type=canonical)
    investments = portfolio(db, ws.id, goal_type=raw)

    response, edge = evidence_for(db, ws.id, item, investments)
    fact = edge["legacy_profile"]["goal_type"]
    assert fact["raw_value"] == raw
    assert fact["compatibility_projection"] == projection
    assert fact["projection_status"] == status
    assert fact["comparison"] == comparison
    assert response["completeness"] == COMPLETE  # unknown data is still evidence


@pytest.mark.parametrize(
    ("legacy", "canonical", "status", "comparison"),
    [
        ("2030-01-02", "2030-01-02", UNCHANGED, SAME_RECORDED_DATE),
        ("2030-01-02", "2030-01-03", UNCHANGED, DIFFERENT_RECORDED_DATES),
        (" 2030-01-02 ", "2030-01-02", NORMALIZED, NOT_COMPARABLE),
        ("2030-01-02T12:30:00", "2030-01-02", NORMALIZED, NOT_COMPARABLE),
        ("not-a-date", "2030-01-02", UNRECOGNIZED, NOT_COMPARABLE),
        (None, "2030-01-02", UNSET, NOT_COMPARABLE),
    ],
)
def test_target_date_comparison_requires_strict_unchanged_dates(
    legacy, canonical, status, comparison
):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_date=canonical)
    investments = portfolio(db, ws.id, goal_target_date=legacy)

    _, edge = evidence_for(db, ws.id, item, investments)
    fact = edge["legacy_profile"]["goal_target_date"]
    assert fact["raw_value"] == legacy
    assert fact["projection_status"] == status
    assert fact["comparison"] == comparison


@pytest.mark.parametrize(
    ("fields", "availability"),
    [
        ({}, NO_FIELDS_RECORDED),
        ({"goal_priority": "IMPORTANT"}, PARTIAL_FIELDS_RECORDED),
        ({"goal_target_date": "2030-01-01"}, PARTIAL_FIELDS_RECORDED),
        ({"goal_target_value": 1_000}, PARTIAL_FIELDS_RECORDED),
        ({"goal_type": "OLD", "goal_priority": "IMPORTANT", "goal_target_date": "bad", "goal_target_value": 0}, ALL_FIELDS_RECORDED),
    ],
)
def test_availability_is_field_independent_and_not_configured_gated(fields, availability):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id, **fields)

    _, edge = evidence_for(db, ws.id, item, investments)
    legacy = edge["legacy_profile"]
    assert legacy["evidence_availability"] == availability
    if "goal_priority" in fields:
        assert legacy["goal_priority"]["compatibility_projection"] == "IMPORTANT"
    if "goal_target_date" in fields:
        assert legacy["goal_target_date"]["raw_value"] == fields["goal_target_date"]
    if "goal_target_value" in fields:
        assert legacy["goal_target_value"]["raw_value"] == fields["goal_target_value"]
        assert legacy["goal_target_value"]["projection_status"] == UNCHANGED


def test_equal_target_numbers_have_no_comparison_or_monetary_claim():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=5_000)
    investments = portfolio(db, ws.id, goal_target_value=5_000)

    _, edge = evidence_for(db, ws.id, item, investments)
    assert edge["wealth_goal"]["target_amount"] == 5_000
    target = edge["legacy_profile"]["goal_target_value"]
    assert target["raw_value"] == 5_000
    assert target["projection_status"] == UNCHANGED
    assert "comparison" not in target
    assert not ({"delta", "ratio", "coverage", "shortfall"} & set(target))


def test_shared_portfolio_keeps_one_deterministic_edge_per_allocation_and_removal_disappears():
    db = make_session()
    ws = workspace(db)
    second = goal(db, ws.id, "B Goal")
    first = goal(db, ws.id, "A Goal")
    investments = portfolio(db, ws.id, goal_type="RETIREMENT")
    second_allocation = allocation(db, ws.id, second.id, portfolio_id=investments.id, amount=20)
    first_allocation = allocation(db, ws.id, first.id, portfolio_id=investments.id, amount=10)

    response = build_legacy_goal_profile_evidence(db, ws.id)
    assert [edge["wealth_goal"]["name"] for edge in response["evidence_edges"]] == [
        "A Goal",
        "B Goal",
    ]
    assert [edge["designation"]["id"] for edge in response["evidence_edges"]] == [
        first_allocation.id,
        second_allocation.id,
    ]
    for edge in response["evidence_edges"]:
        context_goal = next(
            goal_row
            for goal_row in response["goal_context"]["goals"]
            if goal_row["id"] == edge["wealth_goal"]["id"]
        )
        assert edge["designation"] in context_goal["allocations"]
        assert edge["designation"]["source_id"] == edge["portfolio"]["id"]

    db.delete(first_allocation)
    db.commit()
    after = build_legacy_goal_profile_evidence(db, ws.id)
    assert [edge["designation"]["id"] for edge in after["evidence_edges"]] == [
        second_allocation.id
    ]
    assert "stale" not in json.dumps(after).lower()
    assert "history" not in json.dumps(after).lower()


def test_archive_scope_empty_and_cash_only_contexts_are_valid():
    db = make_session()
    ws = workspace(db)
    empty = build_legacy_goal_profile_evidence(db, ws.id)
    assert empty["evidence_edges"] == []
    assert empty["completeness"] == COMPLETE

    archived = goal(db, ws.id, "Archived", archived=True)
    account = cash(db, ws.id)
    allocation(db, ws.id, archived.id, cash_id=account.id)
    active_only = build_legacy_goal_profile_evidence(db, ws.id)
    inclusive = build_legacy_goal_profile_evidence(db, ws.id, include_archived=True)
    assert active_only["goal_context"]["goals"] == []
    assert inclusive["scope"] == {"kind": "WORKSPACE", "include_archived": True}
    assert [row["name"] for row in inclusive["goal_context"]["goals"]] == ["Archived"]
    assert inclusive["evidence_edges"] == []


def test_additional_portfolio_query_is_skipped_without_edges_and_constant_with_cardinality():
    db = make_session()
    ws = workspace(db)
    for index in range(5):
        item = goal(db, ws.id, f"Goal {index}")
        investments = portfolio(db, ws.id, f"Portfolio {index}")
        allocation(db, ws.id, item.id, portfolio_id=investments.id)
    workspace_id = ws.id  # avoid an expired ORM access in the measured region
    selects = []

    @event.listens_for(db.bind, "before_cursor_execute")
    def record_selects(_conn, _cursor, statement, _parameters, _context, _executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            selects.append(statement)

    response = build_legacy_goal_profile_evidence(db, workspace_id)
    assert len(response["evidence_edges"]) == 5
    assert len(selects) == 4  # goals, allocations, Context Portfolios, evidence Portfolios
    assert sum("FROM portfolios" in statement for statement in selects) == 2

    db2 = make_session()
    ws2 = workspace(db2)
    empty_selects = []

    @event.listens_for(db2.bind, "before_cursor_execute")
    def record_empty(_conn, _cursor, statement, _parameters, _context, _executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            empty_selects.append(statement)

    assert build_legacy_goal_profile_evidence(db2, ws2.id)["evidence_edges"] == []
    assert len(empty_selects) == 1
    assert not any("FROM portfolios" in statement for statement in empty_selects)

    db3 = make_session()
    ws3 = workspace(db3)
    cash_goal = goal(db3, ws3.id)
    account = cash(db3, ws3.id)
    allocation(db3, ws3.id, cash_goal.id, cash_id=account.id)
    cash_selects = []

    @event.listens_for(db3.bind, "before_cursor_execute")
    def record_cash(_conn, _cursor, statement, _parameters, _context, _executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            cash_selects.append(statement)

    assert build_legacy_goal_profile_evidence(db3, ws3.id)["evidence_edges"] == []
    assert not any("FROM portfolios" in statement for statement in cash_selects)


def test_service_is_read_only():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id, goal_priority="IMPORTANT")
    allocation(db, ws.id, item.id, portfolio_id=investments.id)
    statements = []

    @event.listens_for(db.bind, "before_cursor_execute")
    def record_statements(_conn, _cursor, statement, _parameters, _context, _executemany):
        statements.append(statement.lstrip().split(None, 1)[0].upper())

    build_legacy_goal_profile_evidence(db, ws.id)
    assert set(statements) == {"SELECT"}
    assert not db.new and not db.dirty and not db.deleted

    service_path = (
        Path(__file__).resolve().parents[1]
        / "services"
        / "legacy_goal_profile_evidence.py"
    )
    tree = ast.parse(service_path.read_text(encoding="utf-8"))
    imported = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert imported <= {
        "__future__",
        "datetime",
        "sqlalchemy.orm",
        "models.database",
        "services.goal_context",
        "services.goal_profile",
    }


def test_foreign_and_missing_portfolios_fail_closed_before_legacy_data_is_returned():
    db = make_session()
    ws = workspace(db)
    other = workspace(db, "Other")
    item = goal(db, ws.id)
    investments = portfolio(db, ws.id, "Secret Portfolio", goal_type="OLD_SECRET")
    allocation(db, ws.id, item.id, portfolio_id=investments.id)

    investments.workspace_id = other.id
    db.commit()
    with pytest.raises(GoalContextIntegrityError):
        build_legacy_goal_profile_evidence(db, ws.id)

    investments.workspace_id = ws.id
    db.commit()
    db.execute(text("DELETE FROM portfolios WHERE id = :portfolio_id"), {"portfolio_id": investments.id})
    db.commit()
    with pytest.raises(GoalContextIntegrityError):
        build_legacy_goal_profile_evidence(db, ws.id)


def test_endpoint_maps_integrity_errors_to_stable_nonleaking_409(monkeypatch):
    db = make_session()
    ws = workspace(db)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    monkeypatch.setattr(
        main,
        "build_legacy_goal_profile_evidence",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            LegacyGoalProfileEvidenceIntegrityError(
                "foreign workspace Secret Portfolio OLD_SECRET"
            )
        ),
    )

    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.get_legacy_goal_profile_evidence(db=db))
    assert exc.value.status_code == 409
    assert exc.value.detail == {
        "code": "LEGACY_GOAL_PROFILE_EVIDENCE_DATA_INTEGRITY",
        "message": "Legacy goal profile evidence failed integrity validation.",
    }
    assert "Secret" not in str(exc.value.detail)

    monkeypatch.setattr(
        main,
        "build_legacy_goal_profile_evidence",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            GoalContextIntegrityError("secret goal corruption")
        ),
    )
    with pytest.raises(HTTPException) as goal_exc:
        asyncio.run(main.get_legacy_goal_profile_evidence(db=db))
    assert goal_exc.value.detail["code"] == "GOAL_CONTEXT_DATA_INTEGRITY"


def test_endpoint_contract_archive_parsing_and_static_route_order(monkeypatch):
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, "Archived", archived=True)
    investments = portfolio(db, ws.id)
    allocation(db, ws.id, item.id, portfolio_id=investments.id)
    monkeypatch.setattr(main, "_ws_id", lambda _db: ws.id)
    endpoint_app = FastAPI()
    endpoint_app.add_api_route(
        "/wealth-goals/legacy-profile-evidence",
        main.get_legacy_goal_profile_evidence,
        methods=["GET"],
    )
    endpoint_app.dependency_overrides[main.get_db] = lambda: db

    response = TestClient(endpoint_app).get(
        "/wealth-goals/legacy-profile-evidence?include_archived=true"
    )
    assert response.status_code == 200
    assert response.json()["contract_version"] == CONTRACT_VERSION
    assert len(response.json()["evidence_edges"]) == 1

    routes = [
        route.path
        for route in main.app.routes
        if getattr(route, "path", "").startswith("/wealth-goals")
    ]
    assert routes.index("/wealth-goals/legacy-profile-evidence") < routes.index(
        "/wealth-goals/{goal_id}/context"
    )
