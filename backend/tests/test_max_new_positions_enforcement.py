"""max_new_positions is a binding hard constraint whenever the policy states it.

A new position is a BUY/ACCUMULATE with a positive target on a symbol not held before the run
(authoritative holdings, never the model's current_weight). Over-limit symbols become HOLD at 0%,
keeping the highest target weights (symbol ascending on ties). Unit tests call the shared
_enforce_hard_policy directly. Endpoint tests run the real /analyze/optimizer on in-memory SQLite
with call_ai mocked (harness from test_advisory_intent_integration). No network or live data.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from agents.optimizer import _enforce_hard_policy, _snap_neutral_actions

HELD = {"AAA", "CCC"}


def row(symbol, action, current, target):
    return {"symbol": symbol, "action": action, "current_weight": float(current), "target_weight": float(target),
            "allocation_change_percent": round(target - current, 2), "estimated_amount": (target - current) * 10}


def policy(limit, *, emergency=False, min_cash=0.0, max_pos=100.0):
    return {"hard_constraints": {"max_new_positions": limit, "min_cash_pct": min_cash,
                                 "max_single_position_pct": max_pos},
            "emergency_override": emergency, "deployment_bias": "SELECTIVE"}


class Observer:
    def __init__(self):
        self.events = []

    def observe(self, symbol, **kwargs):
        self.events.append((symbol, kwargs["reason_code"]))


def enforce(rows, pol, *, held=HELD, muji_v2=False, observer=None):
    _enforce_hard_policy(rows, total_value=1000, policy_context=pol, regime_context=None,
                         muji_v2=muji_v2, held_symbols=held, observer=observer)
    return {r["symbol"]: r for r in rows}


def buys(rows):
    return sorted({r["symbol"] for r in rows if r["action"] in ("BUY", "ACCUMULATE")})


def suppressed(r):
    return (r["action"], r["current_weight"], r["target_weight"], r["allocation_change_percent"],
            r["estimated_amount"]) == ("HOLD", 0.0, 0.0, 0.0, 0)


# ── Unit: the rule inside _enforce_hard_policy ─────────────────────────────────

def four_new():
    return [row("AAA", "HOLD", 30, 30), row("WWW", "BUY", 0, 8), row("VVV", "BUY", 0, 6),
            row("XXX", "BUY", 0, 4), row("YYY", "ACCUMULATE", 0, 2)]


@pytest.mark.parametrize("limit, kept", [(0, []), (1, ["WWW"]), (2, ["VVV", "WWW"]),
                                         (3, ["VVV", "WWW", "XXX"])])
def test_keeps_the_highest_target_weights_up_to_the_limit(limit, kept):
    rows = four_new()
    by = enforce(rows, policy(limit))
    assert buys(rows) == kept
    for symbol in {"WWW", "VVV", "XXX", "YYY"} - set(kept):
        assert suppressed(by[symbol])
    for symbol in kept:
        assert by[symbol]["target_weight"] == {"WWW": 8, "VVV": 6, "XXX": 4}[symbol]
    assert by["AAA"] == row("AAA", "HOLD", 30, 30)


@pytest.mark.parametrize("limit", [4, 5])
def test_at_or_under_the_limit_is_unchanged(limit):
    rows = four_new()
    enforce(rows, policy(limit))
    assert rows == four_new()


def test_accumulating_a_held_symbol_does_not_consume_a_slot():
    rows = [row("AAA", "ACCUMULATE", 10, 13), row("CCC", "BUY", 10, 12)]
    enforce(rows, policy(0))
    assert rows == [row("AAA", "ACCUMULATE", 10, 13), row("CCC", "BUY", 10, 12)]


def test_accumulating_a_non_held_symbol_counts():
    rows = [row("WWW", "ACCUMULATE", 0, 5)]
    assert suppressed(enforce(rows, policy(0))["WWW"])


def test_model_supplied_current_weight_cannot_bypass_the_rule():
    # Not held, but the model claims 4%: still new; the suppressed row lands at the true 0%.
    rows = [row("WWW", "ACCUMULATE", 4, 8), row("AAA", "HOLD", 30, 30)]
    by = enforce(rows, policy(0))
    assert suppressed(by["WWW"])
    _snap_neutral_actions(rows)   # later HOLD pinning must not resurrect the fake weight
    assert suppressed(by["WWW"])


def test_selling_a_holding_does_not_create_a_replacement_allowance():
    rows = [row("AAA", "SELL", 30, 0), row("WWW", "BUY", 0, 10)]
    by = enforce(rows, policy(0))
    assert by["AAA"] == row("AAA", "SELL", 30, 0)
    assert suppressed(by["WWW"])


def test_duplicate_rows_count_once_and_are_handled_together():
    rows = [row("WWW", "BUY", 0, 5), row("WWW", "BUY", 0, 3), row("VVV", "BUY", 0, 4)]
    enforce(rows, policy(1))
    assert [(r["symbol"], r["action"], r["target_weight"]) for r in rows] == [
        ("WWW", "BUY", 5), ("WWW", "BUY", 3), ("VVV", "HOLD", 0)]
    rows = [row("VVV", "BUY", 0, 6), row("WWW", "BUY", 0, 5), row("WWW", "ACCUMULATE", 0, 4)]
    enforce(rows, policy(1))
    assert buys(rows) == ["VVV"] and all(suppressed(r) for r in rows if r["symbol"] == "WWW")


@pytest.mark.parametrize("target", [0, -2])
def test_zero_or_negative_targets_are_not_openings(target):
    rows = [row("WWW", "BUY", 0, target), row("VVV", "BUY", 0, 5)]
    by = enforce(rows, policy(1))
    assert by["VVV"]["action"] == "BUY" and by["VVV"]["target_weight"] == 5
    assert by["WWW"] == row("WWW", "BUY", 0, target)   # left for the existing reconciliation


def test_ties_break_by_symbol_ascending():
    rows = [row("WWW", "BUY", 0, 5), row("VVV", "BUY", 0, 5), row("ZZZ", "BUY", 0, 5)]
    enforce(rows, policy(2))
    assert buys(rows) == ["VVV", "WWW"]
    rows.reverse()
    assert buys(rows) == ["VVV", "WWW"]   # independent of row order


@pytest.mark.parametrize("hard", [
    {}, {"max_new_positions": None}, {"max_new_positions": -1}, {"max_new_positions": "1"},
    {"max_new_positions": 1.5}, {"max_new_positions": 0.0}, {"max_new_positions": True},
    {"max_new_positions": False},
])
def test_missing_or_invalid_limit_is_a_no_op(hard):
    rows = four_new()
    _enforce_hard_policy(rows, total_value=1000, regime_context=None, held_symbols=HELD,
                         policy_context={"hard_constraints": {"min_cash_pct": 0, "max_single_position_pct": 100,
                                                              **hard}})
    assert rows == four_new()


@pytest.mark.parametrize("pol", [None, {}, {"emergency_override": False}])
def test_missing_policy_context_preserves_existing_behaviour(pol):
    rows = four_new()
    _enforce_hard_policy(rows, total_value=1000, policy_context=pol, regime_context=None, held_symbols=HELD)
    assert rows == four_new()


def test_without_held_symbols_the_rule_does_not_run():
    rows = four_new()
    _enforce_hard_policy(rows, total_value=1000, policy_context=policy(0), regime_context=None)
    assert rows == four_new()


def test_emergency_freeze_takes_precedence_and_keeps_its_reason():
    observer = Observer()
    rows = [row("AAA", "ACCUMULATE", 10, 13), row("WWW", "BUY", 0, 5)]
    by = enforce(rows, policy(0, emergency=True), observer=observer)
    assert observer.events == [("AAA", "EMERGENCY_BUY_FREEZE"), ("WWW", "EMERGENCY_BUY_FREEZE")]
    assert (by["AAA"]["action"], by["AAA"]["target_weight"]) == ("HOLD", 10)
    assert (by["WWW"]["action"], by["WWW"]["target_weight"]) == ("HOLD", 0)


def test_observer_records_the_new_position_limit():
    observer = Observer()
    enforce(four_new(), policy(1), observer=observer)
    assert observer.events == [("VVV", "NEW_POSITION_LIMIT"), ("XXX", "NEW_POSITION_LIMIT"),
                               ("YYY", "NEW_POSITION_LIMIT")]


def test_position_cap_and_cash_floor_still_apply_to_survivors():
    rows = [row("AAA", "HOLD", 70, 70), row("WWW", "BUY", 0, 30), row("VVV", "BUY", 0, 20)]
    by = enforce(rows, policy(1, min_cash=15, max_pos=22))
    assert suppressed(by["VVV"])
    # Cap 30→22, then the 15% floor trims 7 more (70 + 22 = 92 leaves 8% cash).
    assert (by["WWW"]["action"], by["WWW"]["target_weight"]) == ("BUY", 15)
    assert 100 - sum(r["target_weight"] for r in rows) >= 15


def test_applies_in_muji_v2_mode_too():
    rows = four_new()
    enforce(rows, policy(1), muji_v2=True)
    assert buys(rows) == ["WWW"]


# ── Endpoint: real orchestration, call_ai mocked ──────────────────────────────

NEW = ("WWW", "VVV")


@pytest.fixture
def optimizer_run(monkeypatch):
    from tests import test_advisory_intent_integration as h
    from models.database import AnalysisCache, OptimizerHistory, Watchlist
    from services.analytics import regime_detector
    from services.optimizer.strategic_candidates import SELECTION_VERSION
    import main

    def make(persona, rows, *, sell_signal=(), emergency=False, selection=False, fallback=False,
             legacy=False, pick_proposal=True):
        allocations = [h.alloc(s, *rows.get(s, (10, "HOLD"))) for s in h.HELD]
        allocations += [{**h.alloc(s, *v[:2]), **({"w": v[2]} if len(v) > 2 else {})}
                        for s, v in rows.items() if s not in h.HELD]
        for a in allocations:
            if a["sig"] in ("SELL", "REDUCE"):
                a["decision_basis"] = "INVESTMENT_THESIS"
        cash = 100 - sum(a["tw"] for a in allocations)
        proposal = {"status": "REBALANCE", "rebalance_opportunity_score": 90, "agrees_with_layer1": True,
                    "allocations": allocations, "portfolio_assessment": "a.",
                    "cash_balance_target": cash, "target_cash_weight": cash}
        if selection:
            proposal["strategy_family"] = "GROWTH_ROTATION"
            proposal["observed_evidence_refs"] = [f"symbol:{s}:signal" for s in rows if rows[s][1] != "HOLD"]
        ai = h.FakeAI(None if fallback else proposal, fallback=proposal)
        if selection:
            def on_call(layer):
                if layer != "layer3":
                    return
                ids = list(dict.fromkeys(re.findall(r"proposal-[0-9a-f]{12}", ai.prompts[layer][-1])))
                refs = proposal["observed_evidence_refs"]
                ai.responses["layer3"] = {"risk_flags": [], "candidate_reviews": [
                    {"candidate_id": "hold-current", "supporting_refs": [], "opposing_refs": []},
                    *({"candidate_id": i, "supporting_refs": refs, "opposing_refs": []} for i in ids)]}
                pick = ids[0] if ids and pick_proposal else "hold-current"
                ai.responses["committee"] = {
                    "selected_candidate_id": pick,
                    "supporting_evidence_refs": refs if pick != "hold-current" else [],
                    "opposing_evidence_refs": [], "comparison_against_hold": "c.",
                    "decision_rationale": "r.", "material_uncertainty": []}
            ai.on_call = on_call

        monkeypatch.delenv(h.FLAG, raising=False)
        # Own sectors for the new symbols so (Legacy, binding) sector limits never confound the count.
        monkeypatch.setitem(h.SECTORS, "WWW", "Utilities")
        monkeypatch.setitem(h.SECTORS, "VVV", "Energy")
        h.patch_pipeline(monkeypatch, ai)
        if emergency:   # real policy engine: vol z-score ≥ 2.5 → emergency_override
            monkeypatch.setattr(regime_detector, "detect_regime", lambda db: {
                "regime": "SIDEWAYS", "confidence": .7, "transition_stability": "STABLE", "vol_z_score": 3.0,
                "constraints": {"min_cash_pct": 5, "max_single_position_pct": 22, "turnover_multiplier": 1}})
        if legacy:   # the true Legacy optimizer modes (not reachable from the endpoint today)
            layered = main.run_layered_optimizer

            def legacy_run(*args, **kwargs):
                args = list(args)   # ..., policy_ctx(14), effective_env(15)
                args[14] = {k: v for k, v in args[14].items()
                            if k not in ("sector_policy_mode", "optimizer_policy_mode")}
                args[15] = None
                kwargs.update(sector_policy_mode=None, optimizer_policy_mode=None)
                return layered(*args, **kwargs)
            monkeypatch.setattr(main, "run_layered_optimizer", legacy_run)

        db = h.session()
        p = h.seed(db, h.book(), cash=h.CASH, sell_signal=sell_signal, watch=NEW)
        p.strategy_persona = persona   # SIDEWAYS: VALUE → limit 1, DIVIDEND → 0, BALANCED → 2
        for w in db.query(Watchlist).filter(Watchlist.symbol.in_(NEW)):
            w.sector = h.SECTORS[w.symbol]
        for s in NEW:
            db.add(AnalysisCache(workspace_id=p.workspace_id, symbol=s, signal="BUY", confidence="HIGH",
                                 reasoning="r", risks="r"))
        db.commit()
        result = h.run(db, p, **({"strategy_selection_mode": SELECTION_VERSION} if selection else {}))
        stored = json.loads(db.query(OptimizerHistory).one().result_json)
        return result, stored, ai
    return make


def final_buys(result):
    return {a["symbol"]: a["target_weight"] for a in result["target_allocations"]
            if a["action"] in ("BUY", "ACCUMULATE")}


def scheduled(result):
    return (result.get("execution_optimization") or {}).get("scheduled_changes") or {}


def assert_consistent(result, stored, *, limit, emergency=False):
    hard = result["active_policy"]["hard_constraints"]
    assert hard["max_new_positions"] == limit                       # policy values unchanged
    assert result["active_policy"]["emergency_override"] is emergency
    opened = {s for s in final_buys(result) if s not in {"AAA", "CCC", "EEE", "FFF", "GGG"}}
    assert len(opened) <= limit
    assert set(scheduled(result)) <= {*final_buys(result), *(a["symbol"] for a in result["target_allocations"]
                                                            if a["action"] in ("SELL", "REDUCE"))}
    assert all(a["target_weight"] >= 0 for a in result["target_allocations"])
    assert sum(a["target_weight"] for a in result["target_allocations"]) <= 100 + 1e-6
    # History persists the final recommendation and its frozen schedule.
    assert stored["target_allocations"] == result["target_allocations"]
    assert stored["status"] == result["status"]
    assert stored["active_policy"]["scheduled_execution"] == result["execution_optimization"]


def test_normal_regime_limit_one_keeps_only_the_largest_new_buy(optimizer_run):
    result, stored, ai = optimizer_run("VALUE", {"WWW": (6, "BUY"), "VVV": (4, "BUY")})
    assert re.search(r"MAX_NEW_POSITIONS:\s*1\b", ai.prompts["layer2"][-1])   # prompt unchanged
    assert final_buys(result) == {"WWW": 6.0}
    assert set(scheduled(result)) == {"WWW"} and scheduled(result)["WWW"] > 0
    vvv = next(a for a in result["target_allocations"] if a["symbol"] == "VVV")
    assert (vvv["action"], vvv["target_weight"], vvv["estimated_amount"]) == ("HOLD", 0.0, 0)
    assert_consistent(result, stored, limit=1)


def test_non_emergency_limit_zero_blocks_a_new_buy_even_with_a_fake_current_weight(optimizer_run):
    result, stored, _ = optimizer_run("DIVIDEND", {"WWW": (8, "BUY", 4)})
    assert final_buys(result) == {} and scheduled(result) == {}
    www = next(a for a in result["target_allocations"] if a["symbol"] == "WWW")
    assert (www["action"], www["current_weight"], www["target_weight"]) == ("HOLD", 0.0, 0.0)
    assert_consistent(result, stored, limit=0)


def test_accumulating_a_holding_with_limit_zero_still_works(optimizer_run):
    result, stored, _ = optimizer_run("DIVIDEND", {"AAA": (13, "ACCUMULATE")})
    assert final_buys(result) == {"AAA": 13.0} and scheduled(result)["AAA"] > 0
    assert_consistent(result, stored, limit=0)


def test_sell_and_replace_still_counts_the_new_symbol(optimizer_run):
    result, stored, _ = optimizer_run("DIVIDEND", {"AAA": (0, "SELL"), "WWW": (10, "BUY")}, sell_signal=("AAA",))
    assert final_buys(result) == {}
    assert set(scheduled(result)) == {"AAA"} and scheduled(result)["AAA"] < 0
    assert_consistent(result, stored, limit=0)


def test_fallback_proposal_over_the_limit_is_trimmed(optimizer_run):
    result, stored, _ = optimizer_run("VALUE", {"WWW": (4, "BUY"), "VVV": (6, "BUY")}, fallback=True)
    assert result["portfolio_assessment"].startswith("[FALLBACK:")
    assert final_buys(result) == {"VVV": 6.0} and set(scheduled(result)) == {"VVV"}
    assert_consistent(result, stored, limit=1)


def test_selection_over_limit_candidate_is_ineligible_and_hold_is_selected(optimizer_run):
    result, stored, _ = optimizer_run("VALUE", {"WWW": (5, "BUY"), "VVV": (5, "BUY")}, selection=True)
    candidates = {c["family"]: c for c in result["strategic_candidates"]["candidates"]}
    proposal = candidates["GROWTH_ROTATION"]
    assert proposal["eligibility_status"] == "INELIGIBLE"
    assert "HARD_SAFEGUARD_CONFLICT" in proposal["eligibility_reasons"]
    assert candidates["HOLD"]["eligibility_status"] == "ELIGIBLE"
    # The Committee asked for the proposal; an ineligible candidate is never selected.
    assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"
    assert (result["status"], result["no_action_reason"]) == ("NO_ACTION", "INSUFFICIENT_EDGE")
    assert final_buys(result) == {} and scheduled(result) == {}
    assert_consistent(result, stored, limit=1)


def test_selection_candidate_within_the_limit_stays_eligible(optimizer_run):
    result, stored, _ = optimizer_run("VALUE", {"WWW": (5, "BUY")}, selection=True)
    proposal = next(c for c in result["strategic_candidates"]["candidates"] if c["family"] == "GROWTH_ROTATION")
    assert proposal["eligibility_status"] == "ELIGIBLE"
    assert result["strategy_selection"]["selected_candidate_id"] == proposal["id"]
    assert result["status"] == "REBALANCE" and final_buys(result) == {"WWW": 5.0}
    assert scheduled(result)["WWW"] > 0
    assert_consistent(result, stored, limit=1)


def test_emergency_freeze_still_blocks_every_buy(optimizer_run):
    result, stored, _ = optimizer_run("BALANCED", {"WWW": (5, "BUY"), "AAA": (13, "ACCUMULATE")}, emergency=True)
    assert final_buys(result) == {} and scheduled(result) == {}
    aaa = next(a for a in result["target_allocations"] if a["symbol"] == "AAA")
    assert (aaa["action"], aaa["target_weight"]) == ("HOLD", aaa["current_weight"])
    assert_consistent(result, stored, limit=0, emergency=True)


def test_within_limit_plan_is_unchanged(optimizer_run):
    result, stored, _ = optimizer_run("BALANCED", {"WWW": (5, "BUY"), "VVV": (4, "BUY")})
    assert final_buys(result) == {"WWW": 5.0, "VVV": 4.0}
    assert set(scheduled(result)) == {"WWW", "VVV"}
    assert_consistent(result, stored, limit=2)


def test_legacy_mode_over_limit_is_trimmed(optimizer_run, monkeypatch):
    import agents.optimizer as om
    seen = []
    real = om._enforce_hard_policy
    monkeypatch.setattr(om, "_enforce_hard_policy", lambda *a, **k: (seen.append(k.get("muji_v2")), real(*a, **k)))
    result, stored, _ = optimizer_run("VALUE", {"WWW": (6, "BUY"), "VVV": (4, "BUY")}, legacy=True)
    assert seen and not any(seen)   # true Legacy enforcement ran
    assert final_buys(result) == {"WWW": 6.0}
    assert result["active_policy"]["hard_constraints"]["max_new_positions"] == 1
    assert stored["target_allocations"] == result["target_allocations"]
