import asyncio
import os
import sys
from datetime import date, datetime, timedelta
import json

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
import main
from models.database import (
    AgentCache, Base, OptimizerHistory, Portfolio, PortfolioItem,
    RecommendationSnapshot, Watchlist, WealthGoal, Workspace,
)


def _session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def _portfolio(db, workspace_id):
    item = Portfolio(workspace_id=workspace_id, name="P")
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def _goal(db, workspace_id, *, target_date, archived=False):
    item = WealthGoal(
        workspace_id=workspace_id, name="G", goal_type="HOUSE", target_amount=1,
        currency="THB", priority="HIGH", target_date=target_date,
        is_archived=archived,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def _pipeline_portfolio(db, workspace_id):
    portfolio = _portfolio(db, workspace_id)
    db.add(PortfolioItem(
        workspace_id=workspace_id, portfolio_id=portfolio.id,
        symbol="AAA", shares=10, avg_cost=50,
    ))
    db.add(Watchlist(workspace_id=workspace_id, symbol="BBB", sector="Other"))
    now = datetime.utcnow()
    for symbol in ("AAA", "BBB"):
        db.add(AgentCache(
            symbol=symbol, agent="technical",
            result_json=json.dumps({"ta_score": 50, "trend": "sideways"}), cached_at=now,
        ))
        db.add(AgentCache(
            symbol=symbol, agent="fundamental",
            result_json=json.dumps({"fa_score": 50, "sector": "Other"}), cached_at=now,
        ))
    db.commit()
    return portfolio


def _patch_pre_ai_pipeline(monkeypatch, optimizer):
    from services.analytics import factor_engine, regime_detector
    from services import execution_instrument_facts, optimizer_timing
    from services.decision_memory import snapshot_writer

    monkeypatch.setattr(main, "fetch_price_info", lambda symbol: {"current_price": 50.0})
    monkeypatch.setattr(main, "run_layered_optimizer", optimizer)
    monkeypatch.setattr(
        factor_engine, "compute_portfolio_factor_exposure",
        lambda *args, **kwargs: {"factor_exposures": {}},
    )
    monkeypatch.setattr(regime_detector, "detect_regime", lambda db: {
        "regime": "SIDEWAYS", "confidence": .7, "transition_stability": "STABLE",
        "constraints": {"min_cash_pct": 5, "max_single_position_pct": 22, "turnover_multiplier": 1},
    })
    monkeypatch.setattr(optimizer_timing, "enrich_scores_with_timing", lambda symbols: {})
    monkeypatch.setattr(execution_instrument_facts, "resolve_execution_instruments", lambda *args: {})
    monkeypatch.setattr(snapshot_writer, "write_recommendation_snapshot", lambda *args, **kwargs: None)


@pytest.mark.parametrize("payload", [{}, {"goal_constraint_goal_id": None}, {"goal_constraint_goal_id": 1}])
def test_request_accepts_only_inactive_or_positive_integer(payload):
    request = main.OptimizerRequest(portfolio_id=1, **payload)
    assert request.goal_constraint_goal_id == payload.get("goal_constraint_goal_id")


@pytest.mark.parametrize("value", [True, False, "1", 1.0, 0, -1])
def test_request_rejects_bool_string_float_zero_and_negative(value):
    with pytest.raises(ValidationError):
        main.OptimizerRequest(portfolio_id=1, goal_constraint_goal_id=value)


def test_inactive_request_does_not_query_goal_policy(monkeypatch):
    from services import goal_recommendation_constraints as service
    monkeypatch.setattr(
        service, "load_goal_constraint_admission",
        lambda *args: pytest.fail("inactive request must not query Goal policy"),
    )
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _portfolio(db, ws_id)
    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(portfolio_id=portfolio.id), db))
    assert exc.value.status_code == 400  # no holdings; admission was never consulted


def test_missing_and_foreign_goal_ids_are_indistinguishable():
    db = _session()
    own_id = main._ws_id(db)
    portfolio = _portfolio(db, own_id)
    other = Workspace(name="Other")
    db.add(other)
    db.commit()
    db.refresh(other)
    foreign = _goal(db, other.id, target_date="2030-01-01")
    details = []
    for goal_id in (999999, foreign.id):
        with pytest.raises(HTTPException) as exc:
            asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
                portfolio_id=portfolio.id, goal_constraint_goal_id=goal_id,
            ), db))
        assert exc.value.status_code == 404
        details.append(exc.value.detail)
    assert details == ["Wealth goal not found", "Wealth goal not found"]


@pytest.mark.parametrize(
    "target_date,archived,code",
    [
        ("2030-01-01", True, "GOAL_CONSTRAINT_GOAL_ARCHIVED"),
        (None, False, "GOAL_CONSTRAINT_TARGET_DATE_REQUIRED"),
        ("2000-01-01", False, "GOAL_CONSTRAINT_TARGET_DATE_PAST"),
    ],
)
def test_ineligible_goal_returns_stable_409(target_date, archived, code):
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _portfolio(db, ws_id)
    goal = _goal(db, ws_id, target_date=target_date, archived=archived)
    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
            portfolio_id=portfolio.id, goal_constraint_goal_id=goal.id,
        ), db))
    assert exc.value.status_code == 409
    assert exc.value.detail["code"] == code
    assert "2030" not in repr(exc.value.detail)


def test_persisted_invalid_date_returns_integrity_409():
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _portfolio(db, ws_id)
    goal = _goal(db, ws_id, target_date="not-a-date")
    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
            portfolio_id=portfolio.id, goal_constraint_goal_id=goal.id,
        ), db))
    assert exc.value.status_code == 409
    assert exc.value.detail["code"] == "GOAL_RECOMMENDATION_CONSTRAINT_DATA_INTEGRITY"


def test_goal_ids_and_behavioral_activation_are_independent_request_fields():
    request = main.OptimizerRequest(
        portfolio_id=1, goal_ids=[7, 8], goal_constraint_goal_id=9,
    )
    assert request.goal_ids == [7, 8]
    assert request.goal_constraint_goal_id == 9


def test_not_applicable_preserves_legacy_optimizer_inputs_and_persists_evidence(monkeypatch):
    calls = []
    def optimizer(*args, **kwargs):
        calls.append((args, kwargs))
        return {}
    _patch_pre_ai_pipeline(monkeypatch, optimizer)
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _pipeline_portfolio(db, ws_id)
    goal = _goal(
        db, ws_id,
        target_date=(date.today() + timedelta(days=400)).isoformat(),
    )
    result = asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
        portfolio_id=portfolio.id, goal_constraint_goal_id=goal.id,
    ), db))
    assert calls[0][1]["enforce_effective_policy_in_fallback"] is False
    assert result["goal_recommendation_constraints"]["resolution"]["application_status"] == "NOT_APPLICABLE"
    history = db.query(OptimizerHistory).one()
    persisted = json.loads(history.result_json)
    assert persisted["goal_recommendation_constraints"] == result["goal_recommendation_constraints"]


def test_candidate_propagates_goal20_and_history_survives_snapshot_failure(monkeypatch):
    calls = []
    def optimizer(*args, **kwargs):
        calls.append((args, kwargs))
        return {"fallback_mode": True}
    _patch_pre_ai_pipeline(monkeypatch, optimizer)
    from services.decision_memory import snapshot_writer
    monkeypatch.setattr(snapshot_writer, "write_recommendation_snapshot", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("snapshot")))
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _pipeline_portfolio(db, ws_id)
    goal = _goal(db, ws_id, target_date=(date.today() + timedelta(days=30)).isoformat())
    result = asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
        portfolio_id=portfolio.id, goal_constraint_goal_id=goal.id,
    ), db))
    args, kwargs = calls[0]
    effective_envelope = args[15]
    policy_context = args[14]
    assert effective_envelope.effective_single_position_pct == 20
    assert policy_context["hard_constraints"]["max_single_position_pct"] <= 20
    assert kwargs["enforce_effective_policy_in_fallback"] is True
    assert db.query(RecommendationSnapshot).count() == 0
    persisted = json.loads(db.query(OptimizerHistory).one().result_json)
    assert persisted["goal_recommendation_constraints"] == result["goal_recommendation_constraints"]
    assert persisted["fallback_mode"] is True
    frozen_evidence = persisted["goal_recommendation_constraints"]
    goal.target_date = "2099-01-01"
    goal.is_archived = True
    db.commit()
    db.delete(goal)
    db.commit()
    assert json.loads(db.query(OptimizerHistory).one().result_json)["goal_recommendation_constraints"] == frozen_evidence


def test_candidate_resolver_failure_fails_closed_and_finalizes_once(monkeypatch):
    _patch_pre_ai_pipeline(monkeypatch, lambda *a, **k: pytest.fail("AI must not run"))
    from services.optimizer import constraint_resolver
    from services import run_progress
    monkeypatch.setattr(constraint_resolver, "resolve_constraints", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("resolver")))
    finishes = []
    monkeypatch.setattr(run_progress, "finish_run", lambda portfolio_id, ok: finishes.append((portfolio_id, ok)))
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _pipeline_portfolio(db, ws_id)
    goal = _goal(db, ws_id, target_date=(date.today() + timedelta(days=30)).isoformat())
    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
            portfolio_id=portfolio.id, goal_constraint_goal_id=goal.id,
        ), db))
    assert exc.value.status_code == 500
    assert exc.value.detail["code"] == "GOAL_RECOMMENDATION_CONSTRAINT_INTERNAL_ERROR"
    assert finishes == [(portfolio.id, False)]
    assert db.query(OptimizerHistory).count() == 0
    assert db.query(RecommendationSnapshot).count() == 0


def test_candidate_generic_optimizer_failure_remains_generic_and_finalizes(monkeypatch):
    _patch_pre_ai_pipeline(monkeypatch, lambda *a, **k: (_ for _ in ()).throw(RuntimeError("provider")))
    from services import run_progress
    finishes = []
    monkeypatch.setattr(run_progress, "finish_run", lambda portfolio_id, ok: finishes.append((portfolio_id, ok)))
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _pipeline_portfolio(db, ws_id)
    goal = _goal(db, ws_id, target_date=(date.today() + timedelta(days=30)).isoformat())
    with pytest.raises(RuntimeError, match="provider"):
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
            portfolio_id=portfolio.id, goal_constraint_goal_id=goal.id,
        ), db))
    assert finishes == [(portfolio.id, False)]
    assert db.query(OptimizerHistory).count() == 0


def test_candidate_policy_engine_failure_fails_closed_before_optimizer(monkeypatch):
    _patch_pre_ai_pipeline(monkeypatch, lambda *a, **k: pytest.fail("optimizer must not run"))
    from services.optimizer import policy_engine
    from services import run_progress
    monkeypatch.setattr(policy_engine, "compute_policy", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("policy")))
    finishes = []
    monkeypatch.setattr(run_progress, "finish_run", lambda portfolio_id, ok: finishes.append((portfolio_id, ok)))
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _pipeline_portfolio(db, ws_id)
    goal = _goal(db, ws_id, target_date=(date.today() + timedelta(days=30)).isoformat())
    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
            portfolio_id=portfolio.id, goal_constraint_goal_id=goal.id,
        ), db))
    assert exc.value.detail["code"] == "GOAL_RECOMMENDATION_CONSTRAINT_INTERNAL_ERROR"
    assert finishes == [(portfolio.id, False)]


def test_candidate_typed_enforcement_failure_is_goal_specific(monkeypatch):
    from agents.optimizer import HardPolicyEnforcementError
    _patch_pre_ai_pipeline(monkeypatch, lambda *a, **k: (_ for _ in ()).throw(HardPolicyEnforcementError("hard")))
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _pipeline_portfolio(db, ws_id)
    goal = _goal(db, ws_id, target_date=(date.today() + timedelta(days=30)).isoformat())
    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
            portfolio_id=portfolio.id, goal_constraint_goal_id=goal.id,
        ), db))
    assert exc.value.status_code == 500
    assert exc.value.detail["code"] == "GOAL_RECOMMENDATION_CONSTRAINT_INTERNAL_ERROR"


def test_progress_finalization_failure_does_not_mask_goal_internal_error(monkeypatch):
    _patch_pre_ai_pipeline(monkeypatch, lambda *a, **k: pytest.fail("optimizer must not run"))
    from services.optimizer import constraint_resolver
    from services import run_progress
    monkeypatch.setattr(constraint_resolver, "resolve_constraints", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("resolver")))
    monkeypatch.setattr(run_progress, "finish_run", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("finish")))
    db = _session()
    ws_id = main._ws_id(db)
    portfolio = _pipeline_portfolio(db, ws_id)
    goal = _goal(db, ws_id, target_date=(date.today() + timedelta(days=30)).isoformat())
    with pytest.raises(HTTPException) as exc:
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(
            portfolio_id=portfolio.id, goal_constraint_goal_id=goal.id,
        ), db))
    assert exc.value.detail["code"] == "GOAL_RECOMMENDATION_CONSTRAINT_INTERNAL_ERROR"
