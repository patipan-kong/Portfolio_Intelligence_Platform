"""Focused contract, integrity, and non-influence coverage for Phase 7.4
Decision Intelligence Context Admission (ADR-008)."""
import ast
import asyncio
from copy import deepcopy
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import (
    AgentCache,
    Base,
    CashAccount,
    GoalFundingAllocation,
    OptimizerHistory,
    Portfolio,
    PortfolioItem,
    RecommendationSnapshot,
    Watchlist,
    WealthGoal,
    Workspace,
)
import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
import main
from services.goal_context import (
    GoalContextIntegrityError,
    build_selected_goal_context,
    normalize_selected_goal_ids,
    selected_goal_ids_exist,
)
from services.decision_goal_context import (
    COMPLETE,
    CONTEXT_ONLY,
    CONTRACT_VERSION,
    EMPTY,
    DecisionGoalContextIntegrityError,
    build_decision_goal_context,
    load_persisted_decision_context,
)
from services.decision_memory.snapshot_writer import write_recommendation_snapshot


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


def goal(db, workspace_id, name="Goal", target_amount=500_000.0, is_archived=False, priority="HIGH", **overrides):
    item = WealthGoal(
        workspace_id=workspace_id, name=name, goal_type="HOUSE",
        target_amount=target_amount, currency="THB", priority=priority,
        is_archived=is_archived, **overrides,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def cash(db, workspace_id, name="Cash", is_archived=False, **overrides):
    item = CashAccount(workspace_id=workspace_id, name=name, currency="THB", balance=0, is_archived=is_archived, **overrides)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def portfolio_row(db, workspace_id, name="Portfolio"):
    item = Portfolio(workspace_id=workspace_id, name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def allocation(db, workspace_id, wealth_goal_id, amount, cash_account_id=None, portfolio_id=None):
    item = GoalFundingAllocation(
        workspace_id=workspace_id, wealth_goal_id=wealth_goal_id,
        cash_account_id=cash_account_id, portfolio_id=portfolio_id,
        allocated_amount=amount, currency="THB",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# ── normalize / existence ────────────────────────────────────────────────

def test_normalize_deduplicates_and_ascending_sorts():
    assert normalize_selected_goal_ids([5, 1, 3, 1, 5]) == [1, 3, 5]
    assert normalize_selected_goal_ids([]) == []


def test_selected_goal_ids_exist_true_for_owned_ids_including_archived():
    db = make_session()
    ws = workspace(db)
    active = goal(db, ws.id, "Active")
    archived = goal(db, ws.id, "Archived", is_archived=True)
    assert selected_goal_ids_exist(db, ws.id, [active.id, archived.id]) is True
    assert selected_goal_ids_exist(db, ws.id, []) is True


def test_selected_goal_ids_exist_false_and_indistinguishable_for_missing_and_foreign():
    db = make_session()
    own = workspace(db, "Own")
    foreign_ws = workspace(db, "Foreign")
    foreign_goal = goal(db, foreign_ws.id)
    assert selected_goal_ids_exist(db, own.id, [999]) is False       # missing
    assert selected_goal_ids_exist(db, own.id, [foreign_goal.id]) is False  # foreign
    own_goal = goal(db, own.id)
    assert selected_goal_ids_exist(db, own.id, [own_goal.id, 999]) is False  # partial


def test_selected_goal_ids_exist_query_reads_no_semantic_goal_fields():
    """The pre-run check must be a bare existence query — this is the
    structural evidence backing the non-influence guarantee."""
    from sqlalchemy import event
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, target_amount=999_999)
    ws_id, item_id = ws.id, item.id  # resolve before attaching the listener
    statements = []

    def track(_, __, statement, params, ___, ____):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(db.bind, "before_cursor_execute", track)
    try:
        selected_goal_ids_exist(db, ws_id, [item_id])
    finally:
        event.remove(db.bind, "before_cursor_execute", track)
    assert len(statements) == 1
    # only the id column (plus implicit alias) is projected — no target_amount,
    # priority, goal_type, or other semantic fact column name appears.
    assert "target_amount" not in statements[0]
    assert "goal_type" not in statements[0]
    assert "priority" not in statements[0]


# ── build_selected_goal_context (additive, reuses _assemble_context) ────

def test_build_selected_goal_context_empty_selection_is_complete_and_empty():
    db = make_session()
    ws = workspace(db)
    context = build_selected_goal_context(db, ws.id, [])
    assert context["completeness"] == "COMPLETE"
    assert context["goals"] == []
    assert context["scope"] == {"kind": "SELECTED", "goal_ids": []}


def test_build_selected_goal_context_includes_archived_goal_as_valid_selection():
    db = make_session()
    ws = workspace(db)
    archived = goal(db, ws.id, "Archived goal", is_archived=True)
    context = build_selected_goal_context(db, ws.id, [archived.id])
    assert context["goals"][0]["id"] == archived.id
    assert context["goals"][0]["is_archived"] is True


def test_build_selected_goal_context_multiple_goals_are_independent_facts():
    db = make_session()
    ws = workspace(db)
    house = goal(db, ws.id, "House", target_amount=1_000, priority="HIGH")
    retirement = goal(db, ws.id, "Retirement", target_amount=2_000, priority="LOW", target_date="2050-01-01")
    account = cash(db, ws.id, "Shared cash")
    allocation(db, ws.id, house.id, 400, cash_account_id=account.id)
    allocation(db, ws.id, retirement.id, 400, cash_account_id=account.id)
    context = build_selected_goal_context(db, ws.id, [house.id, retirement.id])
    by_name = {g["name"]: g for g in context["goals"]}
    assert by_name["House"]["priority"] == "HIGH"
    assert by_name["Retirement"]["priority"] == "LOW"
    assert by_name["Retirement"]["target_date"] == "2050-01-01"
    # no comparison/ranking/conflict key anywhere in the response
    assert "conflicts" not in context
    assert "ranking" not in context
    aggregates = {(row["source_kind"], row["source_id"]): row for row in context["designation_by_source"]}
    assert aggregates[("CASH_ACCOUNT", account.id)]["designated_total_in_context_scope"] == 800


def test_build_selected_goal_context_selected_goal_need_not_allocate_from_any_portfolio():
    db = make_session()
    ws = workspace(db)
    unfunded = goal(db, ws.id, "Unfunded")
    context = build_selected_goal_context(db, ws.id, [unfunded.id])
    assert context["goals"][0]["allocations"] == []
    assert context["goals"][0]["designated_total"] == 0


def test_build_selected_goal_context_raises_if_previously_valid_id_no_longer_resolves():
    """Simulates the narrow race between pre-run validation and post-run
    capture: the pre-existing GoalContextIntegrityError path is reused, not
    a bespoke error, since the caller treats this exactly like any other
    late-discovered integrity failure (see main.py's decision-memory block)."""
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    goal_id = item.id
    db.delete(item)
    db.commit()
    with pytest.raises(GoalContextIntegrityError):
        build_selected_goal_context(db, ws.id, [goal_id])


# ── build_decision_goal_context (the wealth.decision-goal-context.v1 envelope) ──

def test_decision_context_empty_selection_yields_empty_state():
    db = make_session()
    ws = workspace(db)
    payload = build_decision_goal_context(db, ws.id, [])
    assert payload["contract_version"] == CONTRACT_VERSION
    assert payload["decision_effect"] == CONTEXT_ONLY
    assert payload["context_state"] == EMPTY
    assert payload["goals"] == []
    assert payload["selected_goal_ids"] == []


def test_decision_context_populated_selection_yields_complete_state_with_admitted_fields_only():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id, "House", target_amount=1_000_000)
    account = cash(db, ws.id, "Cash")
    allocation(db, ws.id, item.id, 500_000, cash_account_id=account.id)
    payload = build_decision_goal_context(db, ws.id, [item.id])
    assert payload["context_state"] == COMPLETE
    assert payload["selected_goal_ids"] == [item.id]
    goal_payload = payload["goals"][0]
    expected_fields = {
        "id", "name", "goal_type", "priority", "target_amount", "currency",
        "target_date", "is_archived", "updated_at", "allocations",
        "designated_total", "progress_ratio", "progress_percent",
        "funding_gap", "fully_designated",
    }
    assert set(goal_payload.keys()) == expected_fields
    # no valuation, legacy, or risk field can leak through the allowlist
    for forbidden in ("current_value", "valuation", "risk_personality", "legacy_profile", "fit", "mandate"):
        assert forbidden not in goal_payload


# ── load_persisted_decision_context (fail-closed historical read) ────────

def test_load_persisted_decision_context_none_is_none():
    assert load_persisted_decision_context(None) is None


def test_load_persisted_decision_context_round_trips_a_valid_payload():
    db = make_session()
    ws = workspace(db)
    item = goal(db, ws.id)
    payload = build_decision_goal_context(db, ws.id, [item.id])
    loaded = load_persisted_decision_context(json.dumps(payload))
    assert loaded == payload


def test_load_persisted_decision_context_round_trips_valid_empty_payload():
    db = make_session()
    ws = workspace(db)
    payload = build_decision_goal_context(db, ws.id, [])
    assert load_persisted_decision_context(json.dumps(payload)) == payload


def _malformed_complete_payloads(payload):
    """Malformed but JSON-parseable variants of one real builder payload."""
    cases = {}

    def variant(name, mutate):
        candidate = deepcopy(payload)
        mutate(candidate)
        cases[name] = candidate

    variant("selected ids string", lambda item: item.__setitem__("selected_goal_ids", "1"))
    variant("selected id bool", lambda item: item.__setitem__("selected_goal_ids", [True]))
    variant(
        "duplicate selected ids",
        lambda item: item.__setitem__("selected_goal_ids", [item["selected_goal_ids"][0]] * 2),
    )
    variant(
        "non-ascending selected ids",
        lambda item: item.__setitem__("selected_goal_ids", list(reversed(item["selected_goal_ids"]))),
    )
    variant("observed_at null", lambda item: item.__setitem__("observed_at", None))
    variant("observed_at wrong type", lambda item: item.__setitem__("observed_at", 123))
    variant("source version null", lambda item: item.__setitem__("source_goal_context_version", None))
    variant(
        "source version unsupported",
        lambda item: item.__setitem__("source_goal_context_version", "wealth.goal-context.v99"),
    )
    variant("goals wrong type", lambda item: item.__setitem__("goals", {}))
    variant("malformed goal", lambda item: item["goals"][0].__setitem__("name", None))
    variant(
        "malformed allocation",
        lambda item: item["goals"][0]["allocations"][0].__setitem__("designated_amount", "500"),
    )
    variant(
        "malformed source composition",
        lambda item: item["designation_by_source"][0].__setitem__("source_id", None),
    )
    variant("unexpected outer key", lambda item: item.__setitem__("unexpected", True))
    variant("forbidden recommendation gate", lambda item: item.__setitem__("recommendation_gate", "PASS"))
    variant("forbidden conflicts", lambda item: item.__setitem__("conflicts", []))
    variant("unexpected goal key", lambda item: item["goals"][0].__setitem__("objective", "growth"))
    variant(
        "unexpected allocation key",
        lambda item: item["goals"][0]["allocations"][0].__setitem__("ranking", 1),
    )
    variant(
        "unexpected source key",
        lambda item: item["designation_by_source"][0].__setitem__("relevance", True),
    )
    variant("complete empty selection", lambda item: item.__setitem__("selected_goal_ids", []))
    variant(
        "complete mismatched goal ids",
        lambda item: item.__setitem__("selected_goal_ids", [max(item["selected_goal_ids"]) + 100]),
    )

    empty_with_content = deepcopy(payload)
    empty_with_content["context_state"] = EMPTY
    cases["empty with populated content"] = empty_with_content
    return cases


def test_load_persisted_decision_context_rejects_every_malformed_v1_shape():
    db = make_session()
    ws = workspace(db)
    first = goal(db, ws.id, "A goal")
    second = goal(db, ws.id, "B goal")
    account = cash(db, ws.id)
    allocation(db, ws.id, first.id, 500, cash_account_id=account.id)
    payload = build_decision_goal_context(db, ws.id, [first.id, second.id])
    assert load_persisted_decision_context(json.dumps(payload)) == payload

    for name, malformed in _malformed_complete_payloads(payload).items():
        with pytest.raises(DecisionGoalContextIntegrityError, match=".+") as error:
            load_persisted_decision_context(json.dumps(malformed))
        assert error.value.reason, name


@pytest.mark.parametrize("raw", [
    "not json at all {{{",
    "42",
    "null",
    json.dumps({"contract_version": "wealth.decision-goal-context.v2", "decision_effect": CONTEXT_ONLY, "context_state": EMPTY, "selected_goal_ids": [], "observed_at": "x", "goals": [], "designation_by_source": []}),
    json.dumps({"contract_version": CONTRACT_VERSION}),
    json.dumps({"contract_version": CONTRACT_VERSION, "decision_effect": "ADVISORY", "context_state": EMPTY, "selected_goal_ids": [], "observed_at": "x", "goals": [], "designation_by_source": [], "source_goal_context_version": "x"}),
    json.dumps({"contract_version": CONTRACT_VERSION, "decision_effect": CONTEXT_ONLY, "context_state": "PARTIAL", "selected_goal_ids": [], "observed_at": "x", "goals": [], "designation_by_source": [], "source_goal_context_version": "x"}),
])
def test_load_persisted_decision_context_fails_closed(raw):
    with pytest.raises(DecisionGoalContextIntegrityError):
        load_persisted_decision_context(raw)


# ── decision_goal_context.py has no optimizer/market/valuation dependency ──

def test_decision_goal_context_service_has_no_optimizer_or_market_dependency():
    source = Path(__file__).resolve().parents[1] / "services" / "decision_goal_context.py"
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
        for forbidden in ("data_fetcher", "portfolio_snapshots", "optimizer", "goal_profile", "market", "legacy_goal_profile_evidence", "wealth_review")
    )


# ── snapshot_writer: NULL / EMPTY / COMPLETE persistence, serialization failure ──

def test_write_recommendation_snapshot_no_context_attempt_persists_null():
    db = make_session()
    ws = workspace(db)
    p = portfolio_row(db, ws.id)
    history = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=p.id, portfolio_name=p.name,
        analyzed_at=datetime.utcnow(), result_json="{}",
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    snap_id = write_recommendation_snapshot(
        db, workspace_id=ws.id, portfolio_id=p.id,
        optimizer_history_id=history.id, optimizer_result={},
        wealth_goal_context=None,
    )
    snap = db.query(RecommendationSnapshot).filter_by(id=snap_id).first()
    assert snap.wealth_goal_context_json is None


def test_write_recommendation_snapshot_empty_and_complete_context_persist_distinctly():
    db = make_session()
    ws = workspace(db)
    p = portfolio_row(db, ws.id)
    item = goal(db, ws.id)

    def _history():
        h = OptimizerHistory(workspace_id=ws.id, portfolio_id=p.id, portfolio_name=p.name, analyzed_at=datetime.utcnow(), result_json="{}")
        db.add(h)
        db.commit()
        db.refresh(h)
        return h

    empty_payload = build_decision_goal_context(db, ws.id, [])
    h1 = _history()
    snap_id_1 = write_recommendation_snapshot(
        db, workspace_id=ws.id, portfolio_id=p.id, optimizer_history_id=h1.id,
        optimizer_result={}, wealth_goal_context=empty_payload,
    )
    snap1 = db.query(RecommendationSnapshot).filter_by(id=snap_id_1).first()
    assert json.loads(snap1.wealth_goal_context_json)["context_state"] == EMPTY

    complete_payload = build_decision_goal_context(db, ws.id, [item.id])
    h2 = _history()
    snap_id_2 = write_recommendation_snapshot(
        db, workspace_id=ws.id, portfolio_id=p.id, optimizer_history_id=h2.id,
        optimizer_result={}, wealth_goal_context=complete_payload,
    )
    snap2 = db.query(RecommendationSnapshot).filter_by(id=snap_id_2).first()
    assert json.loads(snap2.wealth_goal_context_json)["context_state"] == COMPLETE


def test_write_recommendation_snapshot_context_serialization_failure_aborts_whole_write():
    db = make_session()
    ws = workspace(db)
    p = portfolio_row(db, ws.id)
    history = OptimizerHistory(workspace_id=ws.id, portfolio_id=p.id, portfolio_name=p.name, analyzed_at=datetime.utcnow(), result_json="{}")
    db.add(history)
    db.commit()
    db.refresh(history)

    unserializable = {}
    unserializable["self"] = unserializable  # circular reference: json.dumps always raises

    snap_id = write_recommendation_snapshot(
        db, workspace_id=ws.id, portfolio_id=p.id, optimizer_history_id=history.id,
        optimizer_result={}, wealth_goal_context=unserializable,
    )
    assert snap_id is None
    assert db.query(RecommendationSnapshot).filter_by(optimizer_history_id=history.id).first() is None
    # session remains usable after the internal rollback
    db.query(OptimizerHistory).count()


# ── analyze_optimizer orchestration: pre-run isolation, non-influence, capture ──

def _add_portfolio_with_cache(db, ws_id, symbol="AAA"):
    p = Portfolio(workspace_id=ws_id, name="P1", cash_balance=0.0)
    db.add(p)
    db.commit()
    db.refresh(p)
    db.add(PortfolioItem(workspace_id=ws_id, portfolio_id=p.id, symbol=symbol, shares=10.0, avg_cost=50.0))
    db.add(Watchlist(workspace_id=ws_id, symbol="BBB", sector="Other"))
    now = datetime.utcnow()
    for sym in (symbol, "BBB"):
        db.add(AgentCache(symbol=sym, agent="technical", result_json=json.dumps({"ta_score": 50, "trend": "sideways"}), cached_at=now))
        db.add(AgentCache(symbol=sym, agent="fundamental", result_json=json.dumps({"fa_score": 50}), cached_at=now))
    db.commit()
    return p


def test_missing_goal_id_returns_pre_run_404_with_zero_side_effects(monkeypatch):
    db = make_session()
    ws_id = main._ws_id(db)
    p = _add_portfolio_with_cache(db, ws_id)

    def _unexpected_work(*args, **kwargs):
        pytest.fail("provider, market, AI, and optimizer work must not run for an invalid selection")

    monkeypatch.setattr(main, "analyze_technical", _unexpected_work)
    monkeypatch.setattr(main, "analyze_fundamental", _unexpected_work)
    monkeypatch.setattr(main, "fetch_price_info", _unexpected_work)
    monkeypatch.setattr(main, "run_layered_optimizer", _unexpected_work)

    body = main.OptimizerRequest(portfolio_id=p.id, goal_ids=[999])
    with pytest.raises(HTTPException) as error:
        asyncio.run(main.analyze_optimizer(body, db))
    assert error.value.status_code == 404
    assert error.value.detail == "Wealth goal not found"
    assert db.query(OptimizerHistory).count() == 0
    assert db.query(RecommendationSnapshot).count() == 0


def test_foreign_goal_id_is_indistinguishable_from_missing(monkeypatch):
    db = make_session()
    ws_id = main._ws_id(db)
    p = _add_portfolio_with_cache(db, ws_id)
    other = workspace(db, "Other")
    foreign_goal = goal(db, other.id)

    def _unexpected_work(*args, **kwargs):
        pytest.fail("provider, market, AI, and optimizer work must not run for an invalid selection")

    monkeypatch.setattr(main, "analyze_technical", _unexpected_work)
    monkeypatch.setattr(main, "analyze_fundamental", _unexpected_work)
    monkeypatch.setattr(main, "fetch_price_info", _unexpected_work)
    monkeypatch.setattr(main, "run_layered_optimizer", _unexpected_work)

    body = main.OptimizerRequest(portfolio_id=p.id, goal_ids=[foreign_goal.id])
    with pytest.raises(HTTPException) as error:
        asyncio.run(main.analyze_optimizer(body, db))
    assert error.value.status_code == 404
    assert error.value.detail == "Wealth goal not found"
    assert db.query(OptimizerHistory).count() == 0


def test_valid_goal_ids_leave_decision_layer_arguments_unchanged(monkeypatch):
    """Non-influence proof: run_layered_optimizer is this codebase's actual
    L1/L2/L3 entry point (agents.optimizer.run_layered_optimizer, invoked at
    main.py's analyze_optimizer). Its call arguments must be identical
    whether or not goal_ids is populated."""
    calls = []

    def _spy(*args, **kwargs):
        calls.append((args, kwargs))
        return {}

    monkeypatch.setattr(main, "run_layered_optimizer", _spy)

    db = make_session()
    ws_id = main._ws_id(db)
    p = _add_portfolio_with_cache(db, ws_id)
    item = goal(db, ws_id, "Retirement")

    body_without = main.OptimizerRequest(portfolio_id=p.id)
    try:
        asyncio.run(main.analyze_optimizer(body_without, db))
    except Exception:
        pass
    args_without, kwargs_without = calls[-1]

    body_with = main.OptimizerRequest(portfolio_id=p.id, goal_ids=[item.id])
    try:
        asyncio.run(main.analyze_optimizer(body_with, db))
    except Exception:
        pass
    args_with, kwargs_with = calls[-1]

    assert args_without == args_with
    # on_stage is a fresh functools.partial per call (no __eq__), so compare
    # it structurally and compare every other kwarg by value.
    on_stage_without = kwargs_without.pop("on_stage")
    on_stage_with = kwargs_with.pop("on_stage")
    assert (on_stage_without.func, on_stage_without.args) == (on_stage_with.func, on_stage_with.args)
    assert kwargs_without == kwargs_with
    # the goal's own identity/name never appears anywhere in the call
    assert "Retirement" not in repr(args_with) + repr(kwargs_with)


def test_semantic_goal_context_construction_begins_after_recommendation_computation(monkeypatch):
    events = []

    def _optimizer(*args, **kwargs):
        events.append("recommendation-complete")
        return {}

    from services import decision_goal_context
    real_builder = decision_goal_context.build_decision_goal_context

    def _context_builder(*args, **kwargs):
        events.append("goal-context-begins")
        return real_builder(*args, **kwargs)

    monkeypatch.setattr(main, "run_layered_optimizer", _optimizer)
    monkeypatch.setattr(main, "fetch_price_info", lambda symbol: {"current_price": 50.0})
    monkeypatch.setattr(decision_goal_context, "build_decision_goal_context", _context_builder)

    db = make_session()
    ws_id = main._ws_id(db)
    p = _add_portfolio_with_cache(db, ws_id)
    item = goal(db, ws_id)

    asyncio.run(main.analyze_optimizer(main.OptimizerRequest(portfolio_id=p.id, goal_ids=[item.id]), db))

    assert events == ["recommendation-complete", "goal-context-begins"]


def test_populated_goal_ids_capture_complete_context_on_snapshot(monkeypatch):
    monkeypatch.setattr(main, "run_layered_optimizer", lambda *a, **k: {})

    db = make_session()
    ws_id = main._ws_id(db)
    p = _add_portfolio_with_cache(db, ws_id)
    item = goal(db, ws_id, "House")

    body = main.OptimizerRequest(portfolio_id=p.id, goal_ids=[item.id])
    try:
        asyncio.run(main.analyze_optimizer(body, db))
    except Exception:
        pass

    snap = db.query(RecommendationSnapshot).order_by(RecommendationSnapshot.id.desc()).first()
    assert snap is not None
    context = json.loads(snap.wealth_goal_context_json)
    assert context["context_state"] == COMPLETE
    assert context["goals"][0]["id"] == item.id


def test_omitted_goal_ids_leave_context_null_and_empty_list_captures_empty(monkeypatch):
    monkeypatch.setattr(main, "run_layered_optimizer", lambda *a, **k: {})

    db = make_session()
    ws_id = main._ws_id(db)
    p = _add_portfolio_with_cache(db, ws_id)

    body_none = main.OptimizerRequest(portfolio_id=p.id)
    try:
        asyncio.run(main.analyze_optimizer(body_none, db))
    except Exception:
        pass
    snap_none = db.query(RecommendationSnapshot).order_by(RecommendationSnapshot.id.desc()).first()
    assert snap_none.wealth_goal_context_json is None

    body_empty = main.OptimizerRequest(portfolio_id=p.id, goal_ids=[])
    try:
        asyncio.run(main.analyze_optimizer(body_empty, db))
    except Exception:
        pass
    snap_empty = db.query(RecommendationSnapshot).order_by(RecommendationSnapshot.id.desc()).first()
    assert json.loads(snap_empty.wealth_goal_context_json)["context_state"] == EMPTY


def test_late_capture_failure_preserves_history_and_yields_no_snapshot_with_success(monkeypatch):
    """Simulates persisted-data corruption discoverable only at full
    post-run construction time. The optimizer response must still succeed;
    OptimizerHistory must remain; no RecommendationSnapshot may be written —
    never a post-commit 404/409."""
    monkeypatch.setattr(main, "run_layered_optimizer", lambda *a, **k: {})

    def _boom(*a, **k):
        raise GoalContextIntegrityError("simulated late corruption")

    monkeypatch.setattr("services.decision_goal_context.build_decision_goal_context", _boom)

    db = make_session()
    ws_id = main._ws_id(db)
    p = _add_portfolio_with_cache(db, ws_id)
    item = goal(db, ws_id)

    body = main.OptimizerRequest(portfolio_id=p.id, goal_ids=[item.id])
    result = asyncio.run(main.analyze_optimizer(body, db))  # must not raise

    assert isinstance(result, dict)
    assert db.query(OptimizerHistory).count() == 1
    assert db.query(RecommendationSnapshot).count() == 0


# ── GET /optimizer/snapshots/{id}: isolated decision_context read ───────

def _make_snapshot(db, ws_id, wealth_goal_context_json):
    p = portfolio_row(db, ws_id)
    history = OptimizerHistory(workspace_id=ws_id, portfolio_id=p.id, portfolio_name=p.name, analyzed_at=datetime.utcnow(), result_json="{}")
    db.add(history)
    db.commit()
    db.refresh(history)
    snap = RecommendationSnapshot(
        workspace_id=ws_id, optimizer_history_id=history.id, portfolio_id=p.id,
        wealth_goal_context_json=wealth_goal_context_json,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def test_snapshot_read_exposes_null_decision_context_for_legacy_or_unscoped_run():
    db = make_session()
    ws_id = main._ws_id(db)
    snap = _make_snapshot(db, ws_id, None)
    response = asyncio.run(main.get_recommendation_snapshot(snap.id, db))
    assert response["decision_context"] is None


def test_snapshot_read_exposes_self_contained_captured_decision_context():
    db = make_session()
    ws_id = main._ws_id(db)
    item = goal(db, ws_id, "House")
    payload = build_decision_goal_context(db, ws_id, [item.id])
    snap = _make_snapshot(db, ws_id, json.dumps(payload))

    # Historical read must be self-contained: mutate the live goal afterward
    # and confirm the response is unaffected (no live enrichment).
    item.name = "Renamed after capture"
    db.commit()

    response = asyncio.run(main.get_recommendation_snapshot(snap.id, db))
    assert response["decision_context"]["decision_effect"] == CONTEXT_ONLY
    assert response["decision_context"]["context_state"] == COMPLETE
    assert response["decision_context"]["goals"][0]["name"] == "House"
    # not flattened alongside policy/consensus/recommendation fields
    assert "decision_context" in response
    assert response["decision_context"] is not response.get("consensus")


def test_snapshot_read_malformed_decision_context_fails_closed_409():
    db = make_session()
    ws_id = main._ws_id(db)
    snap = _make_snapshot(db, ws_id, "{not valid json")
    with pytest.raises(HTTPException) as error:
        asyncio.run(main.get_recommendation_snapshot(snap.id, db))
    assert error.value.status_code == 409
    assert error.value.detail == {
        "code": "DECISION_GOAL_CONTEXT_DATA_INTEGRITY",
        "message": "Decision goal context evidence failed integrity validation.",
    }


def test_snapshot_read_maps_malformed_parseable_v1_shapes_to_the_same_generic_409():
    db = make_session()
    ws_id = main._ws_id(db)
    first = goal(db, ws_id, "A goal")
    second = goal(db, ws_id, "B goal")
    account = cash(db, ws_id)
    allocation(db, ws_id, first.id, 500, cash_account_id=account.id)
    valid = build_decision_goal_context(db, ws_id, [first.id, second.id])

    for name, malformed in _malformed_complete_payloads(valid).items():
        snap = _make_snapshot(db, ws_id, json.dumps(malformed))
        with pytest.raises(HTTPException) as error:
            asyncio.run(main.get_recommendation_snapshot(snap.id, db))
        assert error.value.status_code == 409, name
        assert error.value.detail == {
            "code": "DECISION_GOAL_CONTEXT_DATA_INTEGRITY",
            "message": "Decision goal context evidence failed integrity validation.",
        }, name


def test_snapshot_read_unsupported_contract_version_fails_closed_409():
    db = make_session()
    ws_id = main._ws_id(db)
    bad = json.dumps({
        "contract_version": "wealth.decision-goal-context.v99",
        "decision_effect": CONTEXT_ONLY, "context_state": EMPTY,
        "selected_goal_ids": [], "observed_at": "x", "goals": [],
        "designation_by_source": [], "source_goal_context_version": "x",
    })
    snap = _make_snapshot(db, ws_id, bad)
    with pytest.raises(HTTPException) as error:
        asyncio.run(main.get_recommendation_snapshot(snap.id, db))
    assert error.value.status_code == 409
