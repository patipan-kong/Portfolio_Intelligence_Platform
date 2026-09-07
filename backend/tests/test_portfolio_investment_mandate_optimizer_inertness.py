import ast
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
import main
from models.database import (
    AgentCache,
    Base,
    OptimizerHistory,
    Portfolio,
    PortfolioItem,
    Watchlist,
    WealthGoal,
)


def _patch_pre_ai_pipeline(monkeypatch, optimizer):
    from services.analytics import factor_engine, regime_detector
    from services import execution_instrument_facts, optimizer_timing
    from services.decision_memory import calibration
    from services.decision_memory import snapshot_writer

    monkeypatch.setattr(main, "fetch_price_info", lambda symbol: {"current_price": 50.0})
    monkeypatch.setattr(main, "run_layered_optimizer", optimizer)
    monkeypatch.setattr(factor_engine, "compute_portfolio_factor_exposure", lambda *args, **kwargs: {"factor_exposures": {}})
    monkeypatch.setattr(regime_detector, "detect_regime", lambda db: {
        "regime": "SIDEWAYS", "confidence": .7, "transition_stability": "STABLE",
        "constraints": {"min_cash_pct": 5, "max_single_position_pct": 22, "turnover_multiplier": 1},
    })
    monkeypatch.setattr(optimizer_timing, "enrich_scores_with_timing", lambda symbols: {})
    monkeypatch.setattr(execution_instrument_facts, "resolve_execution_instruments", lambda *args: {})
    monkeypatch.setattr(snapshot_writer, "write_recommendation_snapshot", lambda *args, **kwargs: None)

    class FrozenDateTime(datetime):
        @classmethod
        def utcnow(cls):
            return cls(2026, 9, 1, 0, 0, 0)

        @classmethod
        def now(cls, tz=None):
            frozen = cls(2026, 9, 1, 0, 0, 0)
            return frozen.replace(tzinfo=tz or timezone.utc)

    monkeypatch.setattr(main, "datetime", FrozenDateTime)
    monkeypatch.setattr(calibration, "compute_calibration", lambda *args, **kwargs: {})


def _session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def _seed_pipeline(db):
    workspace_id = main._ws_id(db)
    portfolio = Portfolio(workspace_id=workspace_id, name="P")
    goal = WealthGoal(
        workspace_id=workspace_id, name="G", goal_type="HOUSE",
        target_amount=1, currency="THB", priority="HIGH",
    )
    db.add_all([portfolio, goal])
    db.flush()
    db.add(PortfolioItem(
        workspace_id=workspace_id, portfolio_id=portfolio.id,
        symbol="AAA", shares=10, avg_cost=50,
    ))
    db.add(Watchlist(workspace_id=workspace_id, symbol="BBB", sector="Other"))
    now = datetime(2026, 9, 1)
    for symbol in ("AAA", "BBB"):
        db.add(AgentCache(symbol=symbol, agent="technical", result_json=json.dumps({"ta_score": 50, "trend": "sideways"}), cached_at=now))
        db.add(AgentCache(symbol=symbol, agent="fundamental", result_json=json.dumps({"fa_score": 50, "sector": "Other"}), cached_at=now))
    db.commit()
    return portfolio, goal


def test_mandate_create_remove_is_behaviorally_inert(monkeypatch):
    calls = []
    def optimizer(*args, **kwargs):
        captured_kwargs = dict(kwargs)
        callback = captured_kwargs["on_stage"]
        captured_kwargs["on_stage"] = (callback.func, callback.args, callback.keywords)
        calls.append((args, captured_kwargs))
        return {}
    _patch_pre_ai_pipeline(monkeypatch, optimizer)
    db = _session()
    portfolio, goal = _seed_pipeline(db)

    persisted_results = []
    def execute_and_capture():
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(portfolio_id=portfolio.id), db))
        row = db.query(OptimizerHistory).one()
        persisted_results.append(json.loads(row.result_json))
        db.delete(row)
        db.commit()

    execute_and_capture()
    asyncio.run(main.put_portfolio_investment_mandate(portfolio.id, goal.id, main.Response(), db))
    execute_and_capture()
    asyncio.run(main.delete_portfolio_investment_mandate(portfolio.id, goal.id, db))
    execute_and_capture()

    assert calls[0] == calls[1] == calls[2]
    assert persisted_results[0] == persisted_results[1] == persisted_results[2]


def test_current_pre_decision_modules_have_no_mandate_dependency():
    backend = Path(__file__).resolve().parents[1]
    paths = (
        backend / "agents" / "optimizer.py",
        backend / "services" / "optimizer" / "constraint_resolver.py",
        backend / "services" / "goal_recommendation_constraints.py",
    )
    forbidden = {"PortfolioInvestmentMandate", "portfolio_investment_mandates", "investment_mandates"}
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        referenced = {
            node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
        } | {
            node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
        } | {
            node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        assert forbidden.isdisjoint(referenced), path
