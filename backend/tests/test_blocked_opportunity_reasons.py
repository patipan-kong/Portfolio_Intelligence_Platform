"""Blocked-opportunity reason validation: portfolio_count_cap must match portfolio facts.

L2 (and the single-shot fallback) report blocked_opportunities[].reason as free text.
A portfolio_count_cap reason is kept only when the actual stock count reaches max_stocks;
otherwise it becomes emergency_buy_freeze when the backend emergency BUY freeze is active,
or it is dropped. The helper tests are pure. The endpoint tests run the real
/analyze/optimizer on in-memory SQLite with call_ai mocked (harness from
test_advisory_intent_integration). No network or live data.
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from agents.optimizer import _verify_count_cap_reasons

EMERGENCY = {"emergency_override": True, "hard_constraints": {"max_new_positions": 0}}


def cap(symbol, signal="ACCUMULATE", **extra):
    return {"symbol": symbol, "signal": signal, "reason": "portfolio_count_cap", **extra}


def freeze(item):
    return {**item, "reason": "emergency_buy_freeze"}


def verify(blocked, *, count=5, max_stocks=12, policy=None):
    return _verify_count_cap_reasons(blocked, portfolio_count=count, max_stocks=max_stocks, policy_context=policy)


# ── Helper ────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("count, max_stocks", [(12, 12), (13, 12)])
def test_reached_count_cap_keeps_the_reason(count, max_stocks):
    blocked = [cap("WWW"), cap("AAA")]
    assert verify(blocked, count=count, max_stocks=max_stocks, policy=EMERGENCY) == blocked


def test_emergency_freeze_replaces_an_unreached_count_cap():
    blocked = [cap("WWW", note="n"), cap("AAA")]
    # Held and new symbols alike; every other field is preserved and no field is added.
    assert verify(blocked, policy=EMERGENCY) == [freeze(blocked[0]), freeze(blocked[1])]


@pytest.mark.parametrize("policy", [
    None, {}, {"emergency_override": False},
    # Outside emergency max_new_positions is prompt-level only: it never justifies a reason.
    {"emergency_override": False, "hard_constraints": {"max_new_positions": 0}},
])
def test_unsupported_count_cap_is_dropped_outside_emergency(policy):
    assert verify([cap("WWW"), cap("AAA")], policy=policy) == []


@pytest.mark.parametrize("max_stocks", [0, None])
def test_missing_max_stocks_never_justifies_the_count_cap(max_stocks):
    assert verify([cap("WWW")], count=5, max_stocks=max_stocks) == []
    assert verify([cap("WWW")], count=5, max_stocks=max_stocks, policy=EMERGENCY) == [freeze(cap("WWW"))]


@pytest.mark.parametrize("policy", [None, EMERGENCY])
def test_other_reasons_and_malformed_items_pass_through_in_order(policy):
    keep = [{"symbol": "XXX", "signal": "BUY", "reason": "insufficient_cash"},
            {"symbol": "YYY", "signal": "BUY", "reason": "sector_limit_exceeded"},
            {"symbol": "ZZZ", "signal": "BUY"}, "free text"]
    blocked = [keep[0], cap("WWW"), *keep[1:]]
    corrected = [freeze(cap("WWW"))] if policy else []
    assert verify(blocked, policy=policy) == [keep[0], *corrected, *keep[1:]]


def test_reason_match_tolerates_case_and_whitespace_and_input_is_not_mutated():
    blocked = [{"symbol": "WWW", "signal": "BUY", "reason": " Portfolio_Count_Cap "}, cap("AAA")]
    before = copy.deepcopy(blocked)
    out = verify(blocked, policy=EMERGENCY)
    assert [b["reason"] for b in out] == ["emergency_buy_freeze", "emergency_buy_freeze"]
    assert blocked == before and out is not blocked
    assert verify(blocked) == [] and blocked == before


@pytest.mark.parametrize("blocked", [None, {}, "x"])
def test_non_list_input_is_returned_unchanged(blocked):
    assert verify(blocked, policy=EMERGENCY) is blocked


# ── Endpoint: L2, fallback and Phase 3 selection paths ────────────────────────

# The November 13 shape: four ACCUMULATE ideas mislabelled portfolio_count_cap while 5/12 stocks are held
# (two new symbols, two held), plus an unrelated reason that must survive untouched.
MISLABELLED = [
    {"symbol": "WWW", "signal": "ACCUMULATE", "reason": "portfolio_count_cap"},   # not held
    {"symbol": "VVV", "signal": "ACCUMULATE", "reason": "portfolio_count_cap"},   # not held
    {"symbol": "AAA", "signal": "ACCUMULATE", "reason": "portfolio_count_cap"},   # held
    {"symbol": "CCC", "signal": "ACCUMULATE", "reason": "portfolio_count_cap"},   # held
]
OTHER = {"symbol": "XXX", "signal": "BUY", "reason": "insufficient_cash"}
BLOCKED = [*MISLABELLED, OTHER]
DECISION_KEYS = ("status", "no_action_reason", "target_allocations", "target_cash_weight", "swap_suggestions",
                 "portfolio_count", "max_reached", "max_stocks", "active_policy", "consensus",
                 "strategy_selection", "strategic_candidates")
PATHS = ("layered", "fallback", "selection")


@pytest.fixture
def optimizer_run(monkeypatch):
    from tests import test_advisory_intent_integration as h
    from models.database import OptimizerHistory
    from services.analytics import regime_detector
    from services.optimizer.strategic_candidates import SELECTION_VERSION
    import agents.optimizer as optimizer_module
    import main

    def make(path, *, emergency, max_stocks=None, stale_max_reached=False, verify_reasons=True):
        proposal = h.plan()
        proposal.update(status="NO_ACTION", rebalance_opportunity_score=10,
                        blocked_opportunities=copy.deepcopy(BLOCKED))
        fallback = path == "fallback"
        monkeypatch.delenv(h.FLAG, raising=False)
        h.patch_pipeline(monkeypatch, h.FakeAI(None if fallback else proposal, fallback=proposal))
        if emergency:   # real policy engine: vol z-score ≥ 2.5 → emergency_override (backend BUY freeze)
            monkeypatch.setattr(regime_detector, "detect_regime", lambda db: {
                "regime": "SIDEWAYS", "confidence": .7, "transition_stability": "STABLE", "vol_z_score": 3.0,
                "constraints": {"min_cash_pct": 5, "max_single_position_pct": 22, "turnover_multiplier": 1},
            })
        if max_stocks is not None:
            settings = main._get_portfolio_settings
            monkeypatch.setattr(main, "_get_portfolio_settings",
                                lambda db, ws: {**settings(db, ws), "max_stocks": max_stocks})
        if stale_max_reached:   # an inconsistent max_reached=True must not justify the count cap
            layered = optimizer_module.run_layered_optimizer

            def stale(*args, **kwargs):
                args = list(args)
                args[4] = True   # portfolio_data, watchlist_data, name, portfolio_count, max_reached
                return layered(*args, **kwargs)
            monkeypatch.setattr(main, "run_layered_optimizer", stale)
        if not verify_reasons:
            monkeypatch.setattr(optimizer_module, "_verify_count_cap_reasons", lambda blocked, **_: blocked)
        db = h.session()
        p = h.seed(db, h.book(), cash=h.CASH)
        body = {"strategy_selection_mode": SELECTION_VERSION} if path == "selection" else {}
        result = h.run(db, p, **body)
        stored = db.query(OptimizerHistory).one()
        return result, json.loads(stored.blocked_opportunities_json or "[]"), json.loads(stored.result_json)
    return make


@pytest.mark.parametrize("path", PATHS)
def test_november_13_emergency_run_reports_the_freeze_not_the_count_cap(optimizer_run, path):
    result, stored_blocked, stored = optimizer_run(path, emergency=True)
    assert result["active_policy"]["emergency_override"] is True
    assert result["active_policy"]["hard_constraints"]["max_new_positions"] == 0
    assert (result["portfolio_count"], result["max_stocks"], result["max_reached"]) == (5, 12, False)
    expected = [*map(freeze, MISLABELLED), OTHER]
    assert result["blocked_opportunities"] == expected
    assert stored_blocked == expected                       # OptimizerHistory column
    assert stored["blocked_opportunities"] == expected      # persisted result_json
    assert all(set(b) == {"symbol", "signal", "reason"} for b in result["blocked_opportunities"])  # no new fields
    if path == "fallback":
        assert result["portfolio_assessment"].startswith("[FALLBACK:")
    else:   # the Challenger's raw output stays intact for debugging
        assert result["layer2_result"]["blocked_opportunities"] == BLOCKED
    if path == "selection":   # hold-current selected → NO_ACTION / INSUFFICIENT_EDGE
        assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"
        assert (result["status"], result["no_action_reason"]) == ("NO_ACTION", "INSUFFICIENT_EDGE")


@pytest.mark.parametrize("path", PATHS)
def test_reason_correction_does_not_change_the_decision(optimizer_run, path):
    corrected, _, _ = optimizer_run(path, emergency=True)
    raw, _, _ = optimizer_run(path, emergency=True, verify_reasons=False)
    assert raw["blocked_opportunities"] == BLOCKED
    assert set(corrected) == set(raw)                       # no added or removed response fields
    for key in DECISION_KEYS:
        assert corrected.get(key) == raw.get(key), key
    assert all(a["action"] == "HOLD" for a in corrected["target_allocations"])


@pytest.mark.parametrize("path", PATHS)
def test_reached_count_cap_is_kept_even_in_emergency(optimizer_run, path):
    result, _, _ = optimizer_run(path, emergency=True, max_stocks=5)
    assert (result["portfolio_count"], result["max_stocks"], result["max_reached"]) == (5, 5, True)
    assert result["blocked_opportunities"] == BLOCKED


@pytest.mark.parametrize("path", PATHS)
def test_stale_max_reached_does_not_justify_the_count_cap(optimizer_run, path):
    result, _, _ = optimizer_run(path, emergency=False, stale_max_reached=True)
    assert result["max_reached"] is True and result["portfolio_count"] < result["max_stocks"]
    assert result["blocked_opportunities"] == [OTHER]


@pytest.mark.parametrize("path", PATHS)
def test_unsupported_count_cap_is_dropped_outside_emergency(optimizer_run, path):
    result, stored_blocked, _ = optimizer_run(path, emergency=False)
    assert result["active_policy"]["emergency_override"] is False
    assert result["blocked_opportunities"] == stored_blocked == [OTHER]
