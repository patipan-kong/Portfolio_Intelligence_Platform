"""max_stocks is a binding limit on active positions (Phase 4.18), enforced in two stages.

Stage 1 (_enforce_hard_policy, shared by the final plans and the selection/fallback trials):
    room = max_stocks - active holdings (shares > 0) + verified full exits (MUJI V2 only)
and the new-position allowance is min(max_new_positions, room), applied by the Phase 4.15
limiter (highest target weight first, symbol ascending on ties).
Stage 2 (MUJI V2 scheduler): only a SELL actually scheduled for the full position value frees a
slot; new buys beyond the remaining slots are left out of the schedule.

Unit tests call the helpers directly. Endpoint tests run the real /analyze/optimizer on in-memory
SQLite with call_ai mocked (harness from test_advisory_intent_integration); the snapshot writer
returns no id and main.SessionLocal raises, so no background thread can reach a configured DB.
"""
import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from agents.optimizer import (
    _enforce_hard_policy, _explicit_max_stocks, _position_count_inputs, _verified_full_exits,
)
from services.optimizer.concentration_execution import _muji_schedule, _position_slot_excess

TV = 5_000_000
FIVE = frozenset({"AAA", "CCC", "EEE", "FFF", "GGG"})


def row(symbol, action, current, target, **extra):
    change = round(target - current, 2)
    return {"symbol": symbol, "action": action, "current_weight": float(current), "target_weight": float(target),
            "allocation_change_percent": change, "estimated_amount": round(change / 100 * TV), **extra}


def holds(held=FIVE):
    return [row(s, "HOLD", 10, 10) for s in sorted(held)]


def policy(*, new=None, emergency=False, min_cash=0.0, max_pos=100.0):
    hard = {"min_cash_pct": min_cash, "max_single_position_pct": max_pos}
    if new is not None:
        hard["max_new_positions"] = new
    return {"hard_constraints": hard, "emergency_override": emergency, "deployment_bias": "SELECTIVE"}


class Observer:
    def __init__(self):
        self.events = []

    def observe(self, symbol, **kwargs):
        self.events.append((symbol, kwargs["reason_code"]))


def enforce(rows, *, max_stocks=5, held=FIVE, sell_signal=(), muji_v2=True, pol=None, regime=None,
            observer=None):
    _enforce_hard_policy(rows, total_value=TV, policy_context=policy() if pol is None else pol,
                         regime_context=regime, muji_v2=muji_v2, held_symbols=held, max_stocks=max_stocks,
                         sell_signal_symbols=frozenset(sell_signal), observer=observer)
    return {r["symbol"]: r for r in rows}


def opened(rows):
    return sorted(s for s, r in rows.items() if r["action"] in ("BUY", "ACCUMULATE") and s not in FIVE)


def suppressed(r):
    return (r["action"], r["current_weight"], r["target_weight"], r["allocation_change_percent"],
            r["estimated_amount"]) == ("HOLD", 0.0, 0.0, 0.0, 0)


# ── Unit: inputs ───────────────────────────────────────────────────────────────

def test_active_holdings_are_symbols_with_positive_shares():
    portfolio = [{"symbol": "AAA", "shares": 100, "signal": "SELL"}, {"symbol": "ZZZ", "shares": 0, "signal": "SELL"},
                 {"symbol": "NNN", "shares": None}, {"symbol": "MMM", "shares": -5}, {"symbol": "BBB", "shares": "1"},
                 {"symbol": "BAD", "shares": "x"}]
    assert _position_count_inputs(portfolio) == (frozenset({"AAA", "BBB"}), frozenset({"AAA"}))


@pytest.mark.parametrize("value, expected", [(5, 5), (0, 0), (None, None), ("5", None), (5.0, None),
                                             (True, None), (-1, None)])
def test_only_a_nonnegative_int_max_stocks_is_a_rule(value, expected):
    assert _explicit_max_stocks(value) == expected


@pytest.mark.parametrize("candidate, credited", [
    (row("AAA", "SELL", 10, 0), True),                                              # verified full exit
    (row("AAA", "SELL", 10, 0, decision_basis="INVESTMENT_THESIS"), True),
    (row("AAA", "SELL", 10, 0, decision_basis="SECTOR_ADVISORY"), False),           # advisory-only
    (row("AAA", "SELL", 10, 0, decision_basis="CONCENTRATION_ADVISORY"), False),
    (row("AAA", "SELL", 10, 3), False),                                             # partial SELL
    (row("AAA", "REDUCE", 10, 0), False),                                           # REDUCE never exits
    (row("AAA", "SELL", 0.09, 0), False),                                           # below the noise floor
    (row("AAA", "SELL", 0.1, 0), True),                                             # ฿5,000 exactly survives
])
def test_verified_full_exit_mirrors_the_scheduler_evidence(candidate, credited):
    assert _verified_full_exits([candidate], FIVE, {"AAA"}, TV) == ({"AAA"} if credited else set())


def test_a_sell_without_frozen_signal_or_on_an_inactive_symbol_earns_nothing():
    rows = [row("AAA", "SELL", 10, 0), row("ZZZ", "SELL", 0, 0), row("QQQ", "SELL", 10, 0)]
    assert _verified_full_exits(rows, FIVE, set(), TV) == set()
    assert _verified_full_exits(rows, FIVE, {"ZZZ", "QQQ"}, TV) == set()


# ── Unit: Stage 1 inside _enforce_hard_policy ─────────────────────────────────

def test_at_the_limit_a_new_buy_becomes_hold_with_the_max_stocks_reason():
    observer = Observer()
    rows = enforce(holds() + [row("WWW", "BUY", 0, 8)], observer=observer)
    assert suppressed(rows["WWW"]) and opened(rows) == []
    assert observer.events == [("WWW", "MAX_STOCKS_LIMIT")]


@pytest.mark.parametrize("max_stocks, kept", [(5, []), (6, ["XXX"]), (7, ["VVV", "XXX"]), (8, ["VVV", "WWW", "XXX"]),
                                              (12, ["VVV", "WWW", "XXX"])])
def test_slots_go_to_the_highest_targets_then_symbol(max_stocks, kept):
    rows = enforce(holds() + [row("VVV", "BUY", 0, 6), row("WWW", "BUY", 0, 6), row("XXX", "BUY", 0, 9)],
                   max_stocks=max_stocks)
    assert opened(rows) == kept


def test_a_verified_full_exit_frees_exactly_one_slot():
    rows = enforce([*holds(FIVE - {"AAA"}), row("AAA", "SELL", 10, 0), row("WWW", "BUY", 0, 8),
                    row("VVV", "BUY", 0, 8)], sell_signal={"AAA"})
    assert opened(rows) == ["VVV"] and suppressed(rows["WWW"])     # tie at 8% → symbol ascending
    assert rows["AAA"]["action"] == "SELL"


def test_two_verified_exits_fund_two_openings():
    rows = enforce([*holds(FIVE - {"AAA", "CCC"}), row("AAA", "SELL", 10, 0), row("CCC", "SELL", 10, 0),
                    row("WWW", "BUY", 0, 8), row("VVV", "BUY", 0, 8)], sell_signal={"AAA", "CCC"})
    assert opened(rows) == ["VVV", "WWW"]


@pytest.mark.parametrize("exit_row, sell_signal", [
    (row("AAA", "SELL", 10, 0), ()),                                       # unverified SELL
    (row("AAA", "REDUCE", 10, 3), {"AAA"}),                                # partial
    (row("AAA", "SELL", 10, 0, decision_basis="SECTOR_ADVISORY"), {"AAA"}),
])
def test_an_unverified_or_partial_exit_frees_no_slot(exit_row, sell_signal):
    rows = enforce([*holds(FIVE - {"AAA"}), exit_row, row("WWW", "BUY", 0, 8)], sell_signal=sell_signal)
    assert suppressed(rows["WWW"]) and rows["AAA"]["action"] == exit_row["action"]


def test_legacy_never_credits_a_sell():
    rows = enforce([*holds(FIVE - {"AAA"}), row("AAA", "SELL", 10, 0), row("WWW", "BUY", 0, 8)],
                   sell_signal={"AAA"}, muji_v2=False)
    assert suppressed(rows["WWW"]) and rows["AAA"]["action"] == "SELL"


def test_accumulating_an_active_holding_needs_no_slot():
    rows = enforce([*holds(FIVE - {"AAA"}), row("AAA", "ACCUMULATE", 10, 13)])
    assert rows["AAA"]["action"] == "ACCUMULATE" and rows["AAA"]["target_weight"] == 13


def test_a_zero_share_row_is_not_active_and_rebuying_it_is_an_opening():
    active, _ = _position_count_inputs([{"symbol": s, "shares": 100} for s in FIVE] + [{"symbol": "ZZZ", "shares": 0}])
    rows = enforce(holds() + [row("ZZZ", "BUY", 0, 5)], held=active, max_stocks=6)
    assert rows["ZZZ"]["action"] == "BUY"                               # 5 active of 6: one slot
    rows = enforce(holds() + [row("ZZZ", "BUY", 0, 5)], held=active, max_stocks=6, pol=policy(new=0))
    assert suppressed(rows["ZZZ"])                                      # counts toward max_new_positions


def test_over_the_limit_existing_actions_stay_and_nothing_is_forced_to_sell():
    six = FIVE | {"HHH"}
    rows = [row("AAA", "HOLD", 10, 10), row("CCC", "ACCUMULATE", 10, 12), row("EEE", "REDUCE", 10, 5),
            row("FFF", "SELL", 10, 0), row("GGG", "HOLD", 10, 10), row("HHH", "HOLD", 5, 5)]
    before = copy.deepcopy(rows)
    assert enforce(rows, held=six, sell_signal={"FFF"}) == {r["symbol"]: r for r in before}


def test_over_the_limit_a_one_for_one_swap_is_blocked():
    six = FIVE | {"HHH"}
    rows = enforce([*holds(six - {"AAA"}), row("AAA", "SELL", 10, 0), row("WWW", "BUY", 0, 8)],
                   held=six, sell_signal={"AAA"})
    assert suppressed(rows["WWW"])                                      # 6 - 1 + 1 = 6 > 5


def test_over_the_limit_exits_that_reach_the_limit_allow_an_opening():
    six = FIVE | {"HHH"}
    rows = enforce([*holds(six - {"AAA", "CCC"}), row("AAA", "SELL", 10, 0), row("CCC", "SELL", 10, 0),
                    row("WWW", "BUY", 0, 8), row("VVV", "BUY", 0, 8)], held=six, sell_signal={"AAA", "CCC"})
    assert opened(rows) == ["VVV"]                                      # 6 - 2 + 1 = 5


@pytest.mark.parametrize("new, max_stocks, kept, reason", [
    (1, 12, ["XXX"], "NEW_POSITION_LIMIT"),     # max_new_positions binds
    (3, 6, ["XXX"], "MAX_STOCKS_LIMIT"),        # max_stocks binds
    (1, 6, ["XXX"], "NEW_POSITION_LIMIT"),      # equal: the per-rebalance policy reason is kept
    (0, 12, [], "NEW_POSITION_LIMIT"),
])
def test_the_smaller_limit_applies_with_a_deterministic_reason(new, max_stocks, kept, reason):
    observer = Observer()
    rows = enforce(holds() + [row("WWW", "BUY", 0, 6), row("XXX", "BUY", 0, 9)], max_stocks=max_stocks,
                   pol=policy(new=new), observer=observer)
    assert opened(rows) == kept
    assert {code for _, code in observer.events} == {reason}


def test_emergency_freeze_takes_precedence():
    observer = Observer()
    rows = enforce(holds() + [row("WWW", "BUY", 0, 8)], pol=policy(emergency=True), observer=observer)
    assert rows["WWW"]["action"] == "HOLD"
    assert observer.events == [("WWW", "EMERGENCY_BUY_FREEZE")]


def test_the_cash_floor_trims_only_the_surviving_buys():
    # Five holdings at 10%. One slot (max 6): WWW 10% survives; VVV is suppressed first, so the
    # 40% floor (50 + 10 = 60% invested) needs no trim. Had VVV 8% stayed, WWW would be cut to 2%.
    rows = enforce(holds() + [row("WWW", "BUY", 0, 10), row("VVV", "BUY", 0, 8)], max_stocks=6,
                   pol=policy(min_cash=40))
    assert (rows["WWW"]["action"], rows["WWW"]["target_weight"]) == ("BUY", 10.0) and suppressed(rows["VVV"])


def test_the_regime_only_path_enforces_max_stocks():
    rows = holds() + [row("WWW", "BUY", 0, 8)]
    _enforce_hard_policy(rows, total_value=TV, policy_context=None, regime_context={"regime": "SIDEWAYS"},
                         muji_v2=True, held_symbols=FIVE, max_stocks=5)
    assert suppressed(rows[-1])


@pytest.mark.parametrize("max_stocks", [None, "5", 5.5, True, -1])
def test_missing_or_invalid_max_stocks_preserves_existing_behaviour(max_stocks):
    rows = enforce(holds() + [row("WWW", "BUY", 0, 8)], max_stocks=max_stocks)
    assert rows["WWW"]["action"] == "BUY"
    rows = enforce(holds() + [row("WWW", "BUY", 0, 8)], max_stocks=max_stocks, pol=policy(new=0))
    assert suppressed(rows["WWW"])                                      # 4.15 still applies alone


def test_without_held_symbols_no_count_rule_runs():
    rows = holds() + [row("WWW", "BUY", 0, 8)]
    _enforce_hard_policy(rows, total_value=TV, policy_context=policy(), regime_context=None, muji_v2=True,
                         max_stocks=0)
    assert rows[-1]["action"] == "BUY"


# ── Unit: Stage 2 in the MUJI V2 scheduler ────────────────────────────────────

SALES = {"AAA": 500_000.0, "CCC": 500_000.0}


@pytest.mark.parametrize("changes, sell_rows, buys, excluded", [
    ({"AAA": -500_000.0}, {"AAA"}, {"WWW": 8}, set()),                     # scheduled FULL exit
    ({}, {"AAA"}, {"WWW": 8}, {"WWW"}),                                    # deferred SELL
    ({"AAA": -300_000.0}, {"AAA"}, {"WWW": 8}, {"WWW"}),                   # turnover-scaled (partial)
    ({"AAA": -500_000.0}, set(), {"WWW": 8}, {"WWW"}),                     # REDUCE row, not a SELL
    ({"AAA": -500_000.0}, {"AAA"}, {"WWW": 8, "VVV": 8, "XXX": 10}, {"VVV", "WWW"}),   # one slot, priority
    ({"AAA": -500_000.0, "CCC": -500_000.0}, {"AAA", "CCC"}, {"WWW": 8, "VVV": 8}, set()),
    ({}, set(), {"AAA": 13}, set()),                                       # accumulate needs no slot
])
def test_only_scheduled_full_exits_free_slots(changes, sell_rows, buys, excluded):
    limit = (5, set(FIVE), sell_rows, buys)
    assert _position_slot_excess(limit, SALES, buys, changes) == excluded


def test_over_the_limit_scheduled_exits_must_bring_the_count_back_within_it():
    six = set(FIVE | {"HHH"})
    changes = {"AAA": -500_000.0}
    assert _position_slot_excess((5, six, {"AAA"}, {"WWW": 8}), SALES, {"WWW": 1.0}, changes) == {"WWW"}
    changes["CCC"] = -500_000.0
    assert _position_slot_excess((5, six, {"AAA", "CCC"}, {"WWW": 8}), SALES, {"WWW": 1.0}, changes) == set()


def test_scheduler_skips_excluded_buys_and_reports_them():
    values = {s: 500_000.0 for s in FIVE}
    changes, scheduled, _, _, excluded = _muji_schedule(
        {"AAA": 500_000.0}, {"WWW": 100_000.0, "VVV": 100_000.0}, set(), values, 1_000_000.0, 1_000_000.0,
        2_000_000.0, False, (5, set(FIVE), {"AAA"}, {"WWW": 8.0, "VVV": 8.0}))
    assert "AAA" not in changes and scheduled == {} and excluded == {"VVV", "WWW"}   # unverified sale deferred
    changes, scheduled, _, _, excluded = _muji_schedule(
        {"AAA": 500_000.0}, {"WWW": 100_000.0, "VVV": 100_000.0}, {"AAA"}, values, 1_000_000.0, 1_000_000.0,
        2_000_000.0, False, (5, set(FIVE), {"AAA"}, {"WWW": 8.0, "VVV": 8.0}))
    assert changes["AAA"] == -500_000.0 and set(scheduled) == {"VVV"} and excluded == {"WWW"}


def test_scheduler_without_a_frozen_limit_is_unchanged():
    values = {s: 500_000.0 for s in FIVE}
    *_, excluded = _muji_schedule({}, {"WWW": 100_000.0}, set(), values, 1e6, 1e6, 2e6, False)
    assert excluded == set()


# ── Endpoint: real orchestration, call_ai mocked ──────────────────────────────

NEW = ("WWW", "VVV", "XXX")
PRICE = 50.0


def model(symbol, tw, sig, **extra):
    return {"s": symbol, "tw": tw, "sig": sig, "r": "reason", **extra}


@pytest.fixture
def optimizer_run(monkeypatch):
    from tests import test_advisory_intent_integration as h
    from models.database import AnalysisCache, OptimizerHistory, RecommendationSnapshot, Watchlist
    from services.decision_memory.snapshot_writer import write_recommendation_snapshot
    from services.optimizer.strategic_candidates import SELECTION_VERSION
    import main

    def make(rows, *, max_stocks=5, persona="MOMENTUM", book=None, sell_signal=(), family=None,
             fallback=False, legacy=False):
        book = h.book(**(book or {}))
        selection = family is not None
        mentioned = {r["s"] for r in rows}
        allocations = [model(s, 10, "HOLD") for s in h.HELD if s not in mentioned] + [dict(r) for r in rows]
        for a in allocations:
            if a["sig"] in ("SELL", "REDUCE"):
                a.setdefault("decision_basis", "INVESTMENT_THESIS")
        cash = 100 - sum(a["tw"] for a in allocations)
        proposal = {"status": "REBALANCE", "rebalance_opportunity_score": 90, "agrees_with_layer1": True,
                    "allocations": allocations, "portfolio_assessment": "a.",
                    "cash_balance_target": cash, "target_cash_weight": cash}
        ai = h.FakeAI(None if fallback else proposal, fallback=proposal)
        if selection:
            proposal["strategy_family"] = family
            proposal["observed_evidence_refs"] = sorted({f"symbol:{a['s']}:signal" for a in allocations
                                                         if a["sig"] != "HOLD"})

            def on_call(layer):
                if layer != "layer3":
                    return
                ids = list(dict.fromkeys(re.findall(r"proposal-[0-9a-f]{12}", ai.prompts[layer][-1])))
                refs = proposal["observed_evidence_refs"]
                ai.responses["layer3"] = {"risk_flags": [], "candidate_reviews": [
                    {"candidate_id": "hold-current", "supporting_refs": [], "opposing_refs": []},
                    *({"candidate_id": i, "supporting_refs": refs, "opposing_refs": []} for i in ids)]}
                pick = ids[0] if ids else "hold-current"
                ai.responses["committee"] = {
                    "selected_candidate_id": pick,
                    "supporting_evidence_refs": refs if pick != "hold-current" else [],
                    "opposing_evidence_refs": [], "comparison_against_hold": "c.",
                    "decision_rationale": "r.", "material_uncertainty": []}
            ai.on_call = on_call

        snapshots = []

        def snapshot_writer(db, **kwargs):
            # Persist the snapshot in the in-memory DB but hand main no id: a truthy id starts
            # background shadow/grading threads on main.SessionLocal (the configured database).
            snapshots.append(copy.deepcopy(kwargs["optimizer_result"]))
            write_recommendation_snapshot(db, **kwargs)
            return None

        def no_configured_db():
            raise AssertionError("tests must never open the configured database")

        monkeypatch.setattr(main, "SessionLocal", no_configured_db)
        monkeypatch.delenv(h.FLAG, raising=False)
        for s, sector in (("WWW", "Utilities"), ("VVV", "Energy"), ("XXX", "Telecom"), ("ZZZ", "Materials"),
                          ("HHH", "Industrials")):
            monkeypatch.setitem(h.SECTORS, s, sector)
        h.patch_pipeline(monkeypatch, ai, snapshot_writer=snapshot_writer)
        settings = main._get_portfolio_settings
        monkeypatch.setattr(main, "_get_portfolio_settings",
                            lambda db, ws: {**settings(db, ws), "max_stocks": max_stocks})
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
        p = h.seed(db, book, cash=h.CASH, sell_signal=sell_signal, watch=NEW)
        p.strategy_persona = persona   # SIDEWAYS: MOMENTUM -> max_new_positions 3, DIVIDEND -> 0
        for w in db.query(Watchlist).filter(Watchlist.symbol.in_(NEW)):
            w.sector = h.SECTORS[w.symbol]
        for s in NEW:
            db.add(AnalysisCache(workspace_id=p.workspace_id, symbol=s, signal="BUY", confidence="HIGH",
                                 reasoning="r", risks="r"))
        db.commit()
        result = h.run(db, p, **({"strategy_selection_mode": SELECTION_VERSION} if selection else {}))
        stored = json.loads(db.query(OptimizerHistory).one().result_json)
        snap = db.query(RecommendationSnapshot).one()
        assert_consistent(result, stored, snapshots, snap, book)
        result["_stored"] = stored
        result["_active"] = {s for s, (shares, _) in book.items() if shares > 0}
        return result
    return make


def assert_consistent(result, stored, snapshots, snap, book):
    # History and the decision snapshot freeze the same rows and schedule as the response.
    assert stored["target_allocations"] == snapshots[0]["target_allocations"]
    assert json.loads(snap.projected_allocations_json) == stored["target_allocations"]
    assert json.loads(snap.active_policy_json).get("scheduled_execution") == \
        stored["active_policy"].get("scheduled_execution")
    assert stored["active_policy"].get("scheduled_execution") == result.get("execution_optimization")
    nav = sum(shares for shares, _ in book.values()) * PRICE + 2_500_000
    for a in stored["target_allocations"]:
        shares = book.get(a["symbol"], (0, True))[0]
        assert a["current_weight"] == round(shares * PRICE / nav * 100, 2)


def final(result, symbol):
    a = next(a for a in result["_stored"]["target_allocations"] if a["symbol"] == symbol)
    return a["action"], a["target_weight"]


def scheduled(result):
    return (result.get("execution_optimization") or {}).get("scheduled_changes") or {}


def scheduled_buys(result):
    return (result.get("execution_optimization") or {}).get("scheduled_buys") or {}


def new_rows(result):
    return sorted(a["symbol"] for a in result["_stored"]["target_allocations"]
                  if a["action"] in ("BUY", "ACCUMULATE") and a["target_weight"] > 0
                  and a["symbol"] not in result["_active"])


def scheduled_count(result):
    """Active holdings after the frozen schedule: full SELLs leave, scheduled buys enter."""
    plan = result.get("execution_optimization") or {}
    held = set(result["_active"])
    held -= {t["symbol"] for t in plan.get("trades", [])
             if t["action"] == "SELL" and t["execution_state"] == "FULL" and t["executed_amount"] > 0}
    return len(held | {s for s, amount in scheduled_buys(result).items() if amount > 0})


def proposal(result):
    return next(c for c in result["strategic_candidates"]["candidates"] if c["family"] != "HOLD")


@pytest.mark.parametrize("path", ["primary", "fallback", "legacy"])
def test_r01_a_new_buy_at_the_limit_is_blocked(optimizer_run, path):
    # Before: WWW BUY 8% → ฿400,000 scheduled, 6/5.
    result = optimizer_run([model("WWW", 8, "BUY")], fallback=path == "fallback", legacy=path == "legacy")
    assert final(result, "WWW") == ("HOLD", 0.0) and new_rows(result) == []
    assert scheduled_buys(result) == {} and scheduled_count(result) == 5
    assert result["portfolio_count"] == 5 and result["max_reached"] is True


@pytest.mark.parametrize("path", ["primary", "fallback"])
def test_r02_a_verified_full_exit_funds_one_opening(optimizer_run, path):
    result = optimizer_run([model("AAA", 0, "SELL"), model("WWW", 8, "BUY")], sell_signal=("AAA",),
                           fallback=path == "fallback")
    assert final(result, "AAA") == ("SELL", 0.0) and final(result, "WWW") == ("BUY", 8.0)
    assert scheduled(result) == {"AAA": -500_000.0, "WWW": 400_000.0} and scheduled_count(result) == 5
    assert "MAX_STOCKS_LIMIT" not in result["execution_optimization"]["policy_review_reasons"]


@pytest.mark.parametrize("path", ["primary", "fallback"])
def test_r03_one_exit_cannot_fund_two_openings(optimizer_run, path):
    # Before: both buys scheduled → 6/5. Now the tie at 8% keeps VVV (symbol ascending).
    result = optimizer_run([model("AAA", 0, "SELL"), model("WWW", 8, "BUY"), model("VVV", 8, "BUY")],
                           sell_signal=("AAA",), fallback=path == "fallback")
    assert new_rows(result) == ["VVV"] and final(result, "WWW") == ("HOLD", 0.0)
    assert scheduled(result) == {"AAA": -500_000.0, "VVV": 400_000.0} and scheduled_count(result) == 5


def test_r04a_an_unverified_sell_earns_no_slot(optimizer_run):
    # Before: the SELL was deferred (no frozen SELL signal) while WWW was scheduled → 6/5.
    result = optimizer_run([model("AAA", 0, "SELL"), model("WWW", 8, "BUY")])
    assert final(result, "WWW") == ("HOLD", 0.0) and scheduled(result) == {}
    trade = result["execution_optimization"]["trades"][0]
    assert (trade["symbol"], trade["execution_state"]) == ("AAA", "DEFERRED") and scheduled_count(result) == 5


def test_r04b_two_verified_exits_fund_two_openings(optimizer_run):
    result = optimizer_run([model("AAA", 0, "SELL"), model("CCC", 0, "SELL"), model("WWW", 8, "BUY"),
                            model("VVV", 8, "BUY")], sell_signal=("AAA", "CCC"))
    assert new_rows(result) == ["VVV", "WWW"] and set(scheduled_buys(result)) == {"VVV", "WWW"}
    assert scheduled_count(result) == 5


def test_r04c_a_noise_floor_sell_earns_no_slot(optimizer_run):
    # HHH holds ฿2,500 (< ฿5,000 noise floor): its SELL is never scheduled. Before: 7/6.
    result = optimizer_run([model("HHH", 0, "SELL"), model("WWW", 8, "BUY")], max_stocks=6,
                           book={"HHH": (50, True)}, sell_signal=("HHH",))
    assert final(result, "WWW") == ("HOLD", 0.0) and scheduled_buys(result) == {}
    assert scheduled_count(result) == 6


@pytest.mark.parametrize("family", [None, "DEFENSIVE_ROTATION"])
def test_r05_a_reduce_earns_no_slot(optimizer_run, family):
    result = optimizer_run([model("AAA", 3, "REDUCE"), model("WWW", 8, "BUY")],
                           sell_signal=("AAA",) if family else (), family=family)
    if family:   # selection: the candidate would open a sixth position, so it is rejected
        assert proposal(result)["eligibility_status"] == "INELIGIBLE"
        assert "HARD_SAFEGUARD_CONFLICT" in proposal(result)["eligibility_reasons"]
        assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"
    else:
        assert final(result, "AAA") == ("REDUCE", 3.0) and final(result, "WWW") == ("HOLD", 0.0)
    assert scheduled_buys(result) == {} and scheduled_count(result) == 5


def test_r06_over_the_limit_hold_is_unchanged(optimizer_run):
    result = optimizer_run([], max_stocks=4)
    assert all(a["action"] == "HOLD" for a in result["_stored"]["target_allocations"])
    assert scheduled(result) == {} and scheduled_count(result) == 5


@pytest.mark.parametrize("rows, sell_signal", [
    ([model("WWW", 8, "BUY")], ()),                                        # R07: another opening
    ([model("AAA", 0, "SELL"), model("WWW", 8, "BUY")], ("AAA",)),         # R07b: 1-for-1 swap stays above
])
def test_r07_over_the_limit_no_opening_that_keeps_the_excess(optimizer_run, rows, sell_signal):
    result = optimizer_run(rows, max_stocks=4, sell_signal=sell_signal)
    assert final(result, "WWW") == ("HOLD", 0.0) and scheduled_buys(result) == {}
    assert scheduled_count(result) == (4 if sell_signal else 5)   # the valid SELL still runs; nothing forced


def test_r08_a_zero_share_row_is_not_an_active_position(optimizer_run):
    result = optimizer_run([model("WWW", 8, "BUY")], max_stocks=6, book={"ZZZ": (0, True)})
    assert result["portfolio_count"] == 5 and result["max_reached"] is False   # before: 6 / True
    assert final(result, "WWW") == ("BUY", 8.0) and scheduled_count(result) == 6


def test_r08b_rebuying_a_zero_share_row_is_a_new_position(optimizer_run):
    # DIVIDEND (max_new_positions 0): before, ZZZ counted as held and ฿250,000 was scheduled.
    result = optimizer_run([model("ZZZ", 5, "BUY")], max_stocks=6, persona="DIVIDEND", book={"ZZZ": (0, True)})
    assert final(result, "ZZZ") == ("HOLD", 0.0) and scheduled_buys(result) == {}


def test_r09_accumulating_at_the_limit_is_unchanged(optimizer_run):
    result = optimizer_run([model("AAA", 13, "ACCUMULATE")])
    assert final(result, "AAA") == ("ACCUMULATE", 13.0) and scheduled(result) == {"AAA": 150_000.0}


def test_r10_selection_rejects_an_over_limit_candidate(optimizer_run):
    # Before: ELIGIBLE, selected and scheduled (6/5).
    result = optimizer_run([model("WWW", 8, "BUY")], family="GROWTH_ROTATION")
    assert proposal(result)["eligibility_status"] == "INELIGIBLE"
    assert "HARD_SAFEGUARD_CONFLICT" in proposal(result)["eligibility_reasons"]
    assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"
    assert scheduled_buys(result) == {} and scheduled_count(result) == 5


def test_r11a_selection_permits_a_verified_rotation(optimizer_run):
    result = optimizer_run([model("AAA", 0, "SELL"), model("WWW", 8, "BUY")], sell_signal=("AAA",),
                           family="DEFENSIVE_ROTATION")
    assert proposal(result)["eligibility_status"] == "ELIGIBLE"
    assert result["strategy_selection"]["selected_candidate_id"] == proposal(result)["id"]
    assert scheduled(result) == {"AAA": -500_000.0, "WWW": 400_000.0} and scheduled_count(result) == 5


def test_r11b_selection_keeps_rejecting_an_unverified_rotation(optimizer_run):
    result = optimizer_run([model("AAA", 0, "SELL"), model("WWW", 8, "BUY")], family="DEFENSIVE_ROTATION")
    assert proposal(result)["eligibility_status"] != "ELIGIBLE"
    assert "UNVERIFIED_SELL:AAA" in proposal(result)["eligibility_reasons"]
    assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"


def test_r11c_selection_rejects_a_sell_with_excess_buys(optimizer_run):
    result = optimizer_run([model("AAA", 0, "SELL"), model("WWW", 8, "BUY"), model("VVV", 8, "BUY")],
                           sell_signal=("AAA",), family="DEFENSIVE_ROTATION")
    assert proposal(result)["eligibility_status"] == "INELIGIBLE"
    assert "HARD_SAFEGUARD_CONFLICT" in proposal(result)["eligibility_reasons"]
    assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"
    assert scheduled(result) == {}


@pytest.mark.parametrize("sell_signal", [("AAA",), ()])
def test_r12_legacy_never_credits_a_sell(optimizer_run, sell_signal):
    # Legacy may defer a SELL when cash suffices. Before: WWW ฿331,000 scheduled with AAA deferred.
    result = optimizer_run([model("AAA", 0, "SELL"), model("WWW", 8, "BUY")], sell_signal=sell_signal,
                           legacy=True)
    assert final(result, "WWW") == ("HOLD", 0.0) and scheduled_buys(result) == {}
    assert scheduled_count(result) == 5


# ── History and frozen evidence ───────────────────────────────────────────────

def _rotation(optimizer_run):
    result = optimizer_run([model("AAA", 0, "SELL"), model("WWW", 8, "BUY")], sell_signal=("AAA",))
    stored = copy.deepcopy(result["_stored"])
    assert stored["active_policy"]["concentration"]["max_stocks"] == 5
    return stored


def _recompute(payload):
    from services.optimizer.execution_optimizer import optimize_execution_for_payload
    from services.optimizer_action_summary import build_action_summary
    return optimize_execution_for_payload(payload, build_action_summary(payload["target_allocations"]))


def test_frozen_schedules_replay_unchanged(optimizer_run):
    stored = _rotation(optimizer_run)
    frozen = stored["active_policy"]["scheduled_execution"]
    stored["active_policy"]["concentration"]["max_stocks"] = 0     # a changed setting cannot rewrite history
    assert _recompute(stored).model_dump() == frozen


def test_stage2_defers_a_buy_whose_exit_is_not_scheduled(optimizer_run):
    # The proposal passed Stage 1 with a verified exit; if the frozen evidence no longer verifies the
    # sale, the scheduler defers the SELL and must not open the sixth position.
    payload = _rotation(optimizer_run)
    payload["active_policy"].pop("scheduled_execution")
    payload["active_policy"]["concentration"]["positions"]["AAA"].pop("sell_signal")
    plan = _recompute(payload)
    assert plan.scheduled_buys == {} and "MAX_STOCKS_LIMIT" in plan.policy_review_reasons
    assert "BUY_FUNDING_OR_TURNOVER" not in plan.policy_review_reasons
    assert [(t.symbol, t.execution_state) for t in plan.trades] == [("AAA", "DEFERRED")]


def test_runs_without_frozen_max_stocks_recompute_as_before(optimizer_run):
    payload = _rotation(optimizer_run)
    payload["active_policy"].pop("scheduled_execution")
    payload["active_policy"]["concentration"]["positions"]["AAA"].pop("sell_signal")
    del payload["active_policy"]["concentration"]["max_stocks"]     # a run stored before Phase 4.18
    plan = _recompute(payload)
    assert plan.scheduled_buys == {"WWW": 400_000.0} and "MAX_STOCKS_LIMIT" not in plan.policy_review_reasons
