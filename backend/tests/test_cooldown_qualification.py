"""Recommendation cooldown qualification and precedence.

Phase 4.9: a zero-trade REBALANCE run must not start the cooldown.
Phase 4.10: a top-level REVIEW is never relabelled by the cooldown or by
force_rebalance.

Unit tests cover the stored-row predicate, the reference selection and
apply_stabilization. Endpoint tests run the real /analyze/optimizer on
in-memory SQLite with call_ai mocked (harness from
test_advisory_intent_integration); no network or live data.
"""
import json
import os
import re
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


# ── Phase 4.10: REVIEW precedence in apply_stabilization ──────────────────────

REVIEW_TEXT = "Human review required; no candidate selected."


def stabilize(status, rows=(), *, days_ago=2, prev_regime="SIDEWAYS", force=False, consensus_decision="REBALANCE"):
    from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY
    from services.optimizer.stabilization import apply_stabilization

    policy = {"sector_policy_mode": SECTOR_POLICY_ADVISORY, "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2}
    result = {
        "status": status, "rebalance_opportunity_score": 90, "active_policy": policy,
        "market_regime": {"regime": "SIDEWAYS"},
        "target_allocations": [{"symbol": "AAA", "action": action, "current_weight": 20,
                                "target_weight": 30 if action == "BUY" else 20,
                                "allocation_change_percent": 10 if action == "BUY" else 0}
                               for action in rows],
        "consensus": {"consensus_decision": consensus_decision, "consensus_strength_score": 80,
                      "strategy_selection_state": "HUMAN_REVIEW_REQUIRED" if status == "REVIEW" else "SELECTED",
                      "recommended": "human_review", "recommended_action": REVIEW_TEXT},
        "no_action_reason": None, "no_action_summary": None,
        "optimization_notes": REVIEW_TEXT, "portfolio_assessment": REVIEW_TEXT,
    }
    last = None if days_ago is None else datetime.utcnow() - timedelta(days=days_ago)
    return result, apply_stabilization(result, last, prev_regime=prev_regime, force_rebalance=force)


def assert_review_untouched(before, after):
    for field in ("status", "consensus", "no_action_reason", "no_action_summary",
                  "optimization_notes", "portfolio_assessment"):
        assert after[field] == before[field], field
    assert after["stabilization"]["status"] == "REVIEW"
    assert after["stabilization"]["original_optimizer_status"] == "REVIEW"
    assert after["stabilization"]["reason"] is None


def test_review_in_active_cooldown_stays_review_with_cooldown_metadata():
    before, after = stabilize("REVIEW")
    assert_review_untouched(before, after)
    cooldown = after["stabilization"]["cooldown"]
    assert cooldown["active"] and not cooldown["overridden"]
    assert cooldown["days_elapsed"] == 2 and cooldown["days_remaining"] == 5


def test_forced_review_stays_review():
    before, after = stabilize("REVIEW", force=True)
    assert_review_untouched(before, after)
    assert after["stabilization"]["cooldown"]["override_reasons"] == ["MANUAL_OVERRIDE"]


@pytest.mark.parametrize("days_ago,prev_regime", [(None, "SIDEWAYS"), (2, "BULL")])
def test_review_without_cooldown_or_after_regime_change_is_unchanged(days_ago, prev_regime):
    before, after = stabilize("REVIEW", days_ago=days_ago, prev_regime=prev_regime)
    assert_review_untouched(before, after)
    cooldown = after["stabilization"]["cooldown"]
    assert not cooldown["active"]
    assert cooldown["override_reasons"] == ([] if days_ago is None else ["REGIME_CHANGE"])


def test_actionable_rebalance_cooldown_and_force_are_unchanged():
    _, cooled = stabilize("REBALANCE", ["BUY"])
    assert cooled["status"] == cooled["consensus"]["consensus_decision"] == "COOLDOWN_ACTIVE"
    assert cooled["no_action_reason"] == "COOLDOWN_ACTIVE"
    _, forced = stabilize("REBALANCE", ["BUY"], force=True)
    assert forced["status"] == "REBALANCE"
    assert forced["stabilization"]["cooldown"]["override_reasons"] == ["MANUAL_OVERRIDE"]
    _, regime_changed = stabilize("REBALANCE", ["BUY"], prev_regime="BULL")
    assert regime_changed["status"] == "REBALANCE"


def test_forced_no_action_still_becomes_rebalance():
    _, forced = stabilize("NO_ACTION", ["HOLD"], force=True)
    assert forced["status"] == "REBALANCE"


def test_nested_consensus_review_is_not_top_level_review():
    """Out of scope: a risk-conflict consensus_decision keeps its existing behavior."""
    _, after = stabilize("REBALANCE", ["BUY"], consensus_decision="REVIEW")
    assert after["status"] == after["consensus"]["consensus_decision"] == "COOLDOWN_ACTIVE"


# ── Phase 4.10: REVIEW precedence through the real endpoint ───────────────────

SELL_PLAN = {"allocations": [{"s": "AAA", "tw": 0, "sig": "SELL", "decision_basis": "INVESTMENT_THESIS",
                              "r": "Thesis deteriorated"}],
             "strategy_family": "RAISE_CASH", "observed_evidence_refs": ["symbol:AAA:signal"],
             "cash_balance_target": 100, "status": "REBALANCE"}


@pytest.fixture
def committee(monkeypatch):
    """Single AAA holding (500,000) with an observed SELL signal; Committee opted in."""
    from tests import test_advisory_intent_integration as harness
    from services.optimizer.strategic_candidates import SELECTION_VERSION

    def make(cash, committee_reply=None):
        ai = harness.FakeAI(SELL_PLAN)

        def on_call(layer):
            if layer != "layer3":
                return
            match = re.search(r"proposal-[0-9a-f]{12}", ai.prompts[layer][-1])
            reviews = [{"candidate_id": "hold-current", "supporting_refs": [], "opposing_refs": []}]
            if match:
                reviews.append({"candidate_id": match.group(), "supporting_refs": ["symbol:AAA:signal"],
                                "opposing_refs": []})
            ai.responses["layer3"] = {"risk_flags": [], "candidate_reviews": reviews}
            ai.responses["committee"] = committee_reply or {
                "selected_candidate_id": match.group() if match else "hold-current",
                "supporting_evidence_refs": ["symbol:AAA:signal"], "opposing_evidence_refs": [],
                "comparison_against_hold": "The frozen SELL signal supports reducing thesis risk.",
                "decision_rationale": "Sell AAA and retain proceeds as cash.", "material_uncertainty": []}

        ai.on_call = on_call
        monkeypatch.delenv(harness.FLAG, raising=False)
        harness.patch_pipeline(monkeypatch, ai)
        db = harness.session()
        portfolio = harness.seed(db, {"AAA": (10000, True)}, cash=cash, sell_signal=("AAA",))
        env = SimpleNamespace(harness=harness, db=db, portfolio=portfolio)
        env.run = lambda **body: harness.run(db, portfolio, strategy_selection_mode=SELECTION_VERSION, **body)
        return env

    return make


def latest_stored(env):
    OptimizerHistory = env.harness.OptimizerHistory
    return env.db.query(OptimizerHistory).order_by(OptimizerHistory.id.desc()).first()


@pytest.mark.parametrize("cash,reply,state,reason", [
    # 10,000 cash is 2% of NAV, below the 5% regime floor: holding is not hard-safe.
    (10000, None, "HUMAN_REVIEW_REQUIRED", "HOLD_BASIS_OR_HARD_SAFEGUARD_UNVERIFIED"),
    (500000, {"state": "ABSTAINED", "decision_rationale": "Evidence is balanced; defer to the owner.",
              "material_uncertainty": ["mixed evidence"]}, "ABSTAINED", "COMMITTEE_ABSTAINED"),
])
def test_committee_review_survives_active_cooldown(committee, cash, reply, state, reason):
    env = committee(cash, reply)
    prior_run(env, 2, regime("SIDEWAYS", "BUY"))
    response = env.run()
    assert response["status"] == "REVIEW"
    assert response["strategy_selection"]["state"] == state
    assert response["strategy_selection"]["reason_codes"] == [reason]
    assert response["consensus"]["consensus_decision"] != "COOLDOWN_ACTIVE"
    assert response["no_action_reason"] is None and response["no_action_summary"] is None
    assert response["target_allocations"] == []
    assert response["stabilization"]["cooldown"]["active"]
    assert latest_stored(env).optimizer_status == "REVIEW"


def test_forced_review_is_stored_as_review_and_starts_no_cooldown(committee):
    env = committee(10000)
    forced = env.run(force_rebalance=True)
    assert forced["status"] == "REVIEW" and forced["target_allocations"] == []
    assert latest_stored(env).optimizer_status == "REVIEW"
    # Next run: cash restored so the Committee's SELL is actionable.
    env.portfolio.cash_balance = 500000
    env.db.commit()
    following = env.run()
    assert following["status"] == "REBALANCE"
    assert following["stabilization"]["cooldown"]["last_rebalance_at"] is None
