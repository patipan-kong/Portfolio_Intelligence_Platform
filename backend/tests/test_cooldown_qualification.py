"""Phase 4.9: a zero-trade REBALANCE run must not start the recommendation cooldown.

Unit tests cover the stored-row predicate and the reference selection. Endpoint
tests run the real /analyze/optimizer on in-memory SQLite with call_ai mocked
(harness from test_advisory_intent_integration); no network or live data.
"""
import json
import os
import sys
from datetime import datetime, timedelta
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from services.optimizer.stabilization import select_cooldown_reference, stored_run_has_no_trades


def stored(*actions, **extra):
    rows = [{"symbol": f"S{i}", "action": action, "target_weight": 10.0} for i, action in enumerate(actions)]
    return json.dumps({"status": "REBALANCE", "target_allocations": rows, **extra})


# ── Stored-row predicate ──────────────────────────────────────────────────────

@pytest.mark.parametrize("result_json", [
    stored("HOLD"),
    stored("HOLD", "WATCH", "HOLD"),
    stored("hold", "Watch"),
    # Neutralized Committee selection: BUY relabelled HOLD, provenance kept.
    json.dumps({"status": "REBALANCE", "strategy_selection": {"state": "SELECTED"}, "target_allocations": [
        {"symbol": "AAA", "action": "HOLD"}, {"symbol": "BBB", "action": "HOLD", "original_action": "BUY"}]}),
    # Older run with no selection fields is judged by its rows alone.
    json.dumps({"target_allocations": [{"symbol": "AAA", "action": "HOLD"}]}),
])
def test_all_neutral_final_rows_mean_no_trade(result_json):
    assert stored_run_has_no_trades(result_json) is True


@pytest.mark.parametrize("result_json", [
    stored("BUY"), stored("ACCUMULATE"), stored("SELL"), stored("REDUCE"),
    stored("HOLD", "BUY", "HOLD"),       # partially altered plan keeps a trade
    stored("HOLD", "WATCH", "REDUCE"),
])
def test_any_surviving_trade_counts(result_json):
    assert stored_run_has_no_trades(result_json) is False


@pytest.mark.parametrize("result_json", [
    None, "", "not json", "[]", "null", '"text"', "{}",
    json.dumps({"target_allocations": []}),
    json.dumps({"target_allocations": None}),
    json.dumps({"target_allocations": {"AAA": "HOLD"}}),
    json.dumps({"target_allocations": ["HOLD"]}),
    json.dumps({"target_allocations": [{"symbol": "AAA"}]}),
    json.dumps({"target_allocations": [{"symbol": "AAA", "action": None}]}),
    json.dumps({"target_allocations": [{"symbol": "AAA", "action": 1}]}),
    stored("HOLD", "TRIM"),              # unknown action value
    stored("HOLD", ""),
])
def test_missing_or_unreadable_rows_keep_legacy_counting(result_json):
    assert stored_run_has_no_trades(result_json) is False


def test_reference_skips_zero_trade_runs_and_continues_to_older():
    newest_zero = SimpleNamespace(id=3, result_json=stored("HOLD", "WATCH"))
    older_zero = SimpleNamespace(id=2, result_json=stored("HOLD"))
    actionable = SimpleNamespace(id=1, result_json=stored("HOLD", "BUY"))
    assert select_cooldown_reference([newest_zero, older_zero, actionable]) is actionable
    assert select_cooldown_reference([newest_zero, older_zero]) is None
    assert select_cooldown_reference([]) is None
    unreadable = SimpleNamespace(id=4, result_json="{")
    assert select_cooldown_reference([unreadable, actionable]) is unreadable


# ── Endpoint sequences ────────────────────────────────────────────────────────

@pytest.fixture
def endpoint(monkeypatch):
    from tests import test_advisory_intent_integration as harness

    monkeypatch.delenv(harness.FLAG, raising=False)
    harness.patch_pipeline(monkeypatch, harness.FakeAI(harness.plan(AAA=(8, "REDUCE"))))
    db = harness.session()
    portfolio = harness.seed(db, harness.book(), cash=harness.CASH)
    return SimpleNamespace(harness=harness, db=db, portfolio=portfolio)


def prior_run(env, days_ago, result_json, status="REBALANCE"):
    from models.database import OptimizerHistory

    env.db.add(OptimizerHistory(
        workspace_id=env.portfolio.workspace_id, portfolio_id=env.portfolio.id, portfolio_name="P",
        analyzed_at=datetime.utcnow() - timedelta(days=days_ago), swap_count=0,
        result_json=result_json, optimizer_status=status))
    env.db.commit()


def regime(name, *actions):
    """Stored run in market regime `name`; the patched current regime is SIDEWAYS."""
    return stored(*actions, market_regime={"regime": name})


def analyze(env, **body):
    response = env.harness.run(env.db, env.portfolio, **body)
    return response, response["stabilization"]["cooldown"]


def test_without_history_the_run_rebalances(endpoint):
    response, cooldown = analyze(endpoint)
    assert response["status"] == "REBALANCE"
    assert cooldown["last_rebalance_at"] is None


def test_actionable_rebalance_still_starts_the_cooldown(endpoint):
    prior_run(endpoint, 2, regime("SIDEWAYS", "HOLD", "BUY"))
    response, cooldown = analyze(endpoint)
    assert response["status"] == "COOLDOWN_ACTIVE"
    assert response["no_action_reason"] == "COOLDOWN_ACTIVE"
    assert cooldown["active"] and cooldown["days_elapsed"] == 2


def test_zero_trade_rebalance_does_not_start_the_cooldown(endpoint):
    prior_run(endpoint, 2, regime("SIDEWAYS", "HOLD", "HOLD"))
    response, cooldown = analyze(endpoint)
    assert response["status"] == "REBALANCE"
    assert response.get("no_action_reason") != "COOLDOWN_ACTIVE"
    assert not cooldown["active"] and cooldown["last_rebalance_at"] is None
    stored_status = endpoint.db.query(endpoint.harness.OptimizerHistory).order_by(
        endpoint.harness.OptimizerHistory.analyzed_at.desc()).first().optimizer_status
    assert stored_status == "REBALANCE"


def test_older_actionable_run_is_the_reference_and_supplies_the_regime(endpoint):
    # The skipped zero-trade run's BULL regime would trigger REGIME_CHANGE if used.
    prior_run(endpoint, 1, regime("BULL", "HOLD", "WATCH"))
    prior_run(endpoint, 3, regime("SIDEWAYS", "BUY", "HOLD"))
    response, cooldown = analyze(endpoint)
    assert response["status"] == "COOLDOWN_ACTIVE"
    assert cooldown["days_elapsed"] == 3 and not cooldown["overridden"]


def test_regime_change_still_bypasses_the_cooldown(endpoint):
    prior_run(endpoint, 1, regime("SIDEWAYS", "HOLD", "WATCH"))
    prior_run(endpoint, 3, regime("BULL", "BUY", "HOLD"))
    response, cooldown = analyze(endpoint)
    assert response["status"] == "REBALANCE"
    assert cooldown["overridden"] and "REGIME_CHANGE" in cooldown["override_reasons"]


def test_force_rebalance_still_bypasses_the_cooldown(endpoint):
    prior_run(endpoint, 2, regime("SIDEWAYS", "BUY"))
    response, cooldown = analyze(endpoint, force_rebalance=True)
    assert response["status"] == "REBALANCE"
    assert "MANUAL_OVERRIDE" in cooldown["override_reasons"]


@pytest.mark.parametrize("result_json", [
    "not json", json.dumps({"status": "REBALANCE"}), stored(), stored("HOLD", "TRIM"),
])
def test_unreadable_rebalance_runs_keep_legacy_cooldown(endpoint, result_json):
    prior_run(endpoint, 2, result_json)
    response, cooldown = analyze(endpoint)
    assert response["status"] == "COOLDOWN_ACTIVE"
    assert cooldown["days_elapsed"] == 2


def test_non_rebalance_runs_never_start_the_cooldown(endpoint):
    for status in ("NO_ACTION", "COOLDOWN_ACTIVE", "NO_REBALANCE_REQUIRED", "REVIEW"):
        prior_run(endpoint, 2, regime("SIDEWAYS", "BUY"), status=status)
    response, _ = analyze(endpoint)
    assert response["status"] == "REBALANCE"


def test_rebalance_outside_the_window_is_still_displayed(endpoint):
    prior_run(endpoint, 2, regime("SIDEWAYS", "HOLD"))
    prior_run(endpoint, 10, regime("SIDEWAYS", "BUY"))
    response, cooldown = analyze(endpoint)
    assert response["status"] == "REBALANCE"
    assert not cooldown["active"] and cooldown["last_rebalance_at"] is not None
    assert cooldown["days_elapsed"] == 10
