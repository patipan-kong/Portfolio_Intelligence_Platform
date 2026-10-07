"""Investor Intent isolation.

With the default-OFF Advisory Integration V1 flag off, Investor Intent is not
read by any recommendation, scoring or execution path. With it on, only the two
advisory-intent modules read it, for /analyze/optimizer held positions; the
optimizer itself only ever receives their opaque frozen run object.
"""
import ast
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main
from models.database import OptimizerHistory, PortfolioItem
from tests.test_portfolio_investment_mandate_optimizer_inertness import (
    _patch_pre_ai_pipeline, _seed_pipeline, _session,
)

BACKEND = Path(__file__).resolve().parents[1]
INTENT_NAMES = {
    "PositionIntent", "PositionIntentRevision", "position_intents", "position_intent_revisions",
    "investor_intent", "investor_intent_store", "IntentState", "evaluate_proposal",
    "evaluate_quantity_change",
}
# Modules allowed to know about Investor Intent: its own modules, the ORM,
# the API surface, the CLI portfolio-deletion cascade, migrations, and the
# Advisory Integration V1 context/review modules (flag-gated, held positions).
ALLOWED = {
    BACKEND / "services" / "investor_intent.py",
    BACKEND / "services" / "investor_intent_store.py",
    BACKEND / "services" / "advisory_intent_context.py",
    BACKEND / "services" / "advisory_intent_review.py",
    BACKEND / "models" / "database.py",
    BACKEND / "main.py",
    BACKEND / "manage.py",
}


def test_intent_create_and_revise_is_behaviorally_inert(monkeypatch):
    monkeypatch.delenv("FEATURE_ADVISORY_INTENT_REVIEW_V1", raising=False)  # default OFF
    calls = []

    def optimizer(*args, **kwargs):
        captured = dict(kwargs)
        callback = captured["on_stage"]
        captured["on_stage"] = (callback.func, callback.args, callback.keywords)
        calls.append((args, captured))
        return {}

    _patch_pre_ai_pipeline(monkeypatch, optimizer)
    db = _session()
    portfolio, _ = _seed_pipeline(db)
    results = []

    def execute_and_capture():
        asyncio.run(main.analyze_optimizer(main.OptimizerRequest(portfolio_id=portfolio.id), db))
        row = db.query(OptimizerHistory).one()
        results.append(json.loads(row.result_json))
        db.delete(row)
        db.commit()

    def put(**fields):
        asyncio.run(main.put_position_intent(
            portfolio.id, "AAA", main.PositionIntentBody(**fields), main.Response(), db))

    execute_and_capture()
    put(increase_prohibited=True, decrease_prohibited=True, soft_preference="PREFER_EXIT")
    execute_and_capture()
    put(increase_prohibited=False, decrease_prohibited=True, soft_preference="PREFER_KEEP", expected_revision=1)
    execute_and_capture()

    assert calls[0] == calls[1] == calls[2]
    assert results[0] == results[1] == results[2]
    # The legacy lock the optimizer does read is untouched by intent writes.
    assert db.query(PortfolioItem).one().allow_swap is True


def test_no_production_decision_module_references_investor_intent():
    paths = [p for d in ("agents", "services", "routers", "models", "scripts")
             for p in (BACKEND / d).rglob("*.py")]
    offenders = []
    for path in paths:
        if path in ALLOWED or "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.Attribute):
                names.add(node.attr)
            elif isinstance(node, ast.ImportFrom):
                names.update((node.module or "").split("."))
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    names.update(alias.name.split("."))
        if INTENT_NAMES & names:
            offenders.append(str(path.relative_to(BACKEND)))
    assert offenders == []


def test_main_uses_intent_only_inside_its_own_endpoints():
    tree = ast.parse((BACKEND / "main.py").read_text(encoding="utf-8"))
    users = {
        node.name for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and any(isinstance(n, ast.ImportFrom) and n.module == "services.investor_intent_store"
                for n in ast.walk(node))
    }
    assert users == {"list_position_intents", "put_position_intent", "list_position_intent_revisions"}
