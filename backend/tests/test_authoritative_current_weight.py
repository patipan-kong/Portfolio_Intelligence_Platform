"""Current exposure comes from the portfolio book, never from the model (Phase 4.17).

_normalize_allocations receives pc_map, the authoritative symbol -> NAV weight map for every held
symbol. A symbol absent from it is not held: its current_weight is 0 whatever the model echoes in
`current_weight` / `w`. Deltas and estimated amounts follow from that. Model-written symbols first
resolve to the canonical held/watchlist spelling (exact, else a unique case-insensitive match);
an unknown or ambiguous symbol cannot become an executable buy. Unit tests call the shared
helpers directly. Endpoint tests run the real /analyze/optimizer on in-memory SQLite with call_ai
mocked (harness from test_advisory_intent_integration). No network or live data.

Book: AAA CCC EEE FFF GGG, 10,000 sh @ 50 = 10% NAV each; cash 2.5M; NAV 5,000,000.
"""
import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from agents.optimizer import _enforce_hard_policy, _normalize_allocations, _resolve_model_symbols
from services.optimizer_action_summary import build_action_summary

PC_MAP = {"AAA": 10.0, "CCC": 10.0}
WATCH = frozenset({"WWW", "VVV"})


def model(symbol, tw, sig, **extra):
    return {"s": symbol, "tw": tw, "sig": sig, "r": "reason", **extra}


def one(raw, pc_map=PC_MAP):
    [row] = _normalize_allocations([raw], pc_map)
    return row


def weights(row):
    return row["current_weight"], row["target_weight"], row["allocation_change_percent"]


# ── Unit: _normalize_allocations ──────────────────────────────────────────────

def test_new_symbol_without_a_model_weight_starts_at_zero():
    assert weights(one(model("WWW", 8, "BUY"))) == (0.0, 8.0, 8.0)


@pytest.mark.parametrize("key", ["w", "current_weight"])
@pytest.mark.parametrize("fake, target", [(5, 8), (-10, 5), (10, 5), (50, 5)])
def test_new_symbol_ignores_any_model_reported_current_weight(key, fake, target):
    row = one(model("WWW", target, "BUY", **{key: fake}))
    assert weights(row) == (0.0, float(target), float(target))
    assert row["action"] == "BUY"   # direction is left to the existing reconciliation


@pytest.mark.parametrize("fake", [0, 50, -10])
def test_held_symbol_uses_the_book_weight(fake):
    for key in ("w", "current_weight"):
        assert weights(one(model("AAA", 13, "ACCUMULATE", **{key: fake}))) == (10.0, 13.0, 3.0)


def test_unheld_sell_has_no_current_exposure_to_sell():
    assert weights(one(model("WWW", 0, "SELL", w=10))) == (0.0, 0.0, 0.0)


def test_empty_book_is_authoritative_too():
    assert weights(one(model("WWW", 5, "BUY", w=10), pc_map={})) == (0.0, 5.0, 5.0)


def test_without_holdings_context_the_legacy_fallback_is_kept():
    # Only a caller with no book at all (pc_map=None) reads the model value; production never does.
    assert weights(one(model("WWW", 8, "BUY", w=5), pc_map=None)) == (5.0, 8.0, 3.0)


def test_book_weights_are_not_rounded_before_the_delta():
    row = one(model("AAA", 12.5, "REDUCE"), pc_map={"AAA": 15.7296})
    assert (row["current_weight"], row["allocation_change_percent"]) == (15.73, -3.23)


def test_classification_new_versus_accumulate():
    rows = _normalize_allocations([model("AAA", 13, "ACCUMULATE", w=0), model("WWW", 8, "BUY", w=5),
                                   model("VVV", 4, "ACCUMULATE", w=2)], PC_MAP)
    summary = build_action_summary(rows)
    assert [e["symbol"] for e in summary["accumulate"]] == ["AAA"]
    assert [e["symbol"] for e in summary["new_position"]] == ["WWW", "VVV"]


def test_model_output_is_not_mutated():
    raw = [model("WWW", 8, "BUY", w=5), model("AAA", 13, "ACCUMULATE", w=50, decision_basis="INVESTMENT_THESIS")]
    before = copy.deepcopy(raw)
    pc_map = dict(PC_MAP)
    _normalize_allocations(raw, pc_map)
    assert raw == before and pc_map == PC_MAP


def test_target_action_reason_and_basis_handling_is_unchanged():
    rows = _normalize_allocations([
        {"symbol": "AAA", "target_weight": 12, "action": "accumulate", "reason": "long",
         "decision_basis": "INVESTMENT_THESIS"},
        {"s": "WWW", "tw": 4, "sig": "buy", "r": "short", "decision_basis": "MODEL_GUESS"},
        {"s": "", "tw": 9, "sig": "BUY", "w": 3},
    ], PC_MAP)
    assert [(r["symbol"], r["action"], r["target_weight"], r["reason"], r["estimated_amount"]) for r in rows] == [
        ("AAA", "ACCUMULATE", 12.0, "long", 0), ("WWW", "BUY", 4.0, "short", 0)]
    assert rows[0]["decision_basis"] == "INVESTMENT_THESIS" and "decision_basis" not in rows[1]


def test_safeguards_see_the_true_opening_size():
    # Legacy single-position cap (22%) and a binding new-position limit both still apply.
    rows = _normalize_allocations([model("AAA", 10, "HOLD"), model("WWW", 30, "BUY", w=5)], PC_MAP)
    _enforce_hard_policy(rows, total_value=1000, regime_context=None, held_symbols=PC_MAP.keys(),
                         policy_context={"hard_constraints": {"max_new_positions": 1, "min_cash_pct": 0,
                                                              "max_single_position_pct": 22}})
    www = rows[1]
    assert (www["action"], www["current_weight"], www["target_weight"]) == ("BUY", 0.0, 22.0)
    rows = _normalize_allocations([model("WWW", 8, "BUY", w=5)], PC_MAP)
    _enforce_hard_policy(rows, total_value=1000, regime_context=None, held_symbols=PC_MAP.keys(),
                         policy_context={"hard_constraints": {"max_new_positions": 0, "min_cash_pct": 0,
                                                              "max_single_position_pct": 100}})
    assert (rows[0]["action"], rows[0]["current_weight"], rows[0]["target_weight"]) == ("HOLD", 0.0, 0.0)


# ── Unit: symbol identity ─────────────────────────────────────────────────────

def resolve(raws, known=("AAA", "CCC", "WWW", "VVV")):
    return _resolve_model_symbols(raws, known)


def test_exact_symbols_resolve_to_themselves():
    assert resolve(["AAA", "WWW"]) == {"AAA": "AAA", "WWW": "WWW"}


@pytest.mark.parametrize("raw, canonical", [("aaa", "AAA"), ("Aaa", "AAA"), (" aaa ", "AAA"), ("www", "WWW")])
def test_unique_case_insensitive_match_uses_the_known_spelling(raw, canonical):
    assert resolve([raw]) == {raw: canonical}


@pytest.mark.parametrize("raw", ["QQQ", "AAA.BK", "AA", "ＡＡＡ"])
def test_unknown_symbols_stay_unresolved(raw):
    assert resolve([raw]) == {raw: None}


def test_case_collision_in_the_known_universe_is_ambiguous():
    assert resolve(["www"], known=("AAA", "WWW", "Www")) == {"www": None}
    assert resolve(["Www"], known=("AAA", "WWW", "Www")) == {"Www": "Www"}   # exact still wins


def test_a_variant_never_duplicates_another_row_for_the_same_symbol():
    assert resolve(["AAA", "aaa"]) == {"AAA": "AAA", "aaa": None}
    assert resolve(["aaa", "Aaa"]) == {"aaa": None, "Aaa": None}
    assert resolve(["aaa", "aaa"]) == {"aaa": "AAA"}   # an exact repeat is not a new collision


def normalize(raw, **kwargs):
    return _normalize_allocations(raw, PC_MAP, known_symbols=WATCH, **kwargs)


def test_held_case_variant_uses_the_book_weight():
    [row] = normalize([model("aaa", 13, "ACCUMULATE", w=0)])
    assert (row["symbol"], row["action"], *weights(row)) == ("AAA", "ACCUMULATE", 10.0, 13.0, 3.0)


def test_watchlist_case_variant_is_a_new_position():
    [row] = normalize([model("www", 8, "BUY", w=5)])
    assert (row["symbol"], row["action"], *weights(row)) == ("WWW", "BUY", 0.0, 8.0, 8.0)
    assert [e["symbol"] for e in build_action_summary([row])["new_position"]] == ["WWW"]


@pytest.mark.parametrize("raw", [[model("QQQ", 5, "BUY", w=3)],
                                 [model("AAA", 10, "HOLD"), model("aaa", 13, "ACCUMULATE")]])
def test_unknown_or_ambiguous_buys_are_not_executable(raw):
    rows = normalize(raw)
    suspect = rows[-1]
    assert suspect["symbol"] == raw[-1]["s"]                 # model spelling kept for eligibility checks
    assert (suspect["action"], *weights(suspect)) == ("HOLD", 0.0, 0.0, 0.0)


def test_unknown_non_buy_rows_keep_their_direction_and_no_exposure():
    rows = normalize([model("QQQ", 0, "SELL", w=10), model("QQQ2", 4, "HOLD")])
    assert [(r["symbol"], r["action"], *weights(r)) for r in rows] == [
        ("QQQ", "SELL", 0.0, 0.0, 0.0), ("QQQ2", "HOLD", 0.0, 4.0, 4.0)]


def test_without_a_known_universe_symbols_are_used_as_written():
    # Callers that pass only the book (e.g. sector alternatives) keep exact-match behaviour.
    [row] = _normalize_allocations([model("aaa", 13, "ACCUMULATE")], PC_MAP)
    assert (row["symbol"], row["action"], *weights(row)) == ("aaa", "ACCUMULATE", 0.0, 13.0, 13.0)


def test_symbol_resolution_does_not_mutate_model_output_or_inputs():
    raw = [model("aaa", 13, "ACCUMULATE", w=0), model("QQQ", 5, "BUY")]
    before, watch = copy.deepcopy(raw), set(WATCH)
    normalize(raw)
    assert raw == before and set(WATCH) == watch


def test_resolved_variant_counts_against_the_new_position_limit():
    rows = normalize([model("www", 8, "BUY"), model("aaa", 13, "ACCUMULATE")])
    _enforce_hard_policy(rows, total_value=1000, regime_context=None, held_symbols=PC_MAP.keys(),
                         policy_context={"hard_constraints": {"max_new_positions": 0, "min_cash_pct": 0,
                                                              "max_single_position_pct": 100}})
    assert [(r["symbol"], r["action"], r["target_weight"]) for r in rows] == [
        ("WWW", "HOLD", 0.0), ("AAA", "ACCUMULATE", 13.0)]


# ── Endpoint: real orchestration, call_ai mocked ──────────────────────────────

NAV = 5_000_000
NEW = ("WWW", "VVV")


@pytest.fixture
def optimizer_run(monkeypatch):
    from tests import test_advisory_intent_integration as h
    from models.database import AnalysisCache, OptimizerHistory, RecommendationSnapshot, Watchlist
    from services.decision_memory.snapshot_writer import write_recommendation_snapshot
    from services.optimizer.strategic_candidates import SELECTION_VERSION
    import main

    def make(rows, *, persona="MOMENTUM", sell_signal=(), selection=False, fallback=False, legacy=False,
             omit=(), extra_watch=(), buy_signal=()):
        mentioned = {r["s"] for r in rows} | set(omit)
        allocations = [model(s, 10, "HOLD") for s in h.HELD if s not in mentioned] + [dict(r) for r in rows]
        for a in allocations:
            if a["sig"] in ("SELL", "REDUCE"):
                a["decision_basis"] = "INVESTMENT_THESIS"
        cash = 100 - sum(a["tw"] for a in allocations)
        proposal = {"status": "REBALANCE", "rebalance_opportunity_score": 90, "agrees_with_layer1": True,
                    "allocations": allocations, "portfolio_assessment": "a.",
                    "cash_balance_target": cash, "target_cash_weight": cash}
        if selection:
            proposal["strategy_family"] = "GROWTH_ROTATION"
            # Evidence refs cite the prompt's identifiers, which are canonical (upper-case here).
            proposal["observed_evidence_refs"] = sorted({f"symbol:{a['s'].strip().upper()}:signal"
                                                         for a in allocations if a["sig"] != "HOLD"})
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
                pick = ids[0] if ids else "hold-current"
                ai.responses["committee"] = {
                    "selected_candidate_id": pick,
                    "supporting_evidence_refs": refs if pick != "hold-current" else [],
                    "opposing_evidence_refs": [], "comparison_against_hold": "c.",
                    "decision_rationale": "r.", "material_uncertainty": []}
            ai.on_call = on_call

        snapshots = []

        def snapshot_writer(db, **kwargs):
            # Persist the real snapshot in the in-memory DB, but hand main no id: a truthy id starts
            # background shadow/grading threads that open main.SessionLocal (the configured DB).
            snapshots.append(copy.deepcopy(kwargs["optimizer_result"]))
            write_recommendation_snapshot(db, **kwargs)
            return None

        def no_configured_db():
            raise AssertionError("tests must never open the configured database")

        monkeypatch.setattr(main, "SessionLocal", no_configured_db)
        monkeypatch.delenv(h.FLAG, raising=False)
        monkeypatch.setitem(h.SECTORS, "WWW", "Utilities")
        monkeypatch.setitem(h.SECTORS, "VVV", "Energy")
        for s in extra_watch:
            monkeypatch.setitem(h.SECTORS, s, "Utilities")
        h.patch_pipeline(monkeypatch, ai, snapshot_writer=snapshot_writer)
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
        p = h.seed(db, h.book(), cash=h.CASH, sell_signal=sell_signal, watch=(*NEW, *extra_watch))
        p.strategy_persona = persona   # SIDEWAYS: MOMENTUM -> max_new_positions 3, DIVIDEND -> 0
        for w in db.query(Watchlist).filter(Watchlist.symbol.in_((*NEW, *extra_watch))):
            w.sector = h.SECTORS[w.symbol]
        for s in (*NEW, *buy_signal):
            db.add(AnalysisCache(workspace_id=p.workspace_id, symbol=s, signal="BUY", confidence="HIGH",
                                 reasoning="r", risks="r"))
        db.commit()
        result = h.run(db, p, **({"strategy_selection_mode": SELECTION_VERSION} if selection else {}))
        stored = json.loads(db.query(OptimizerHistory).one().result_json)
        snap = db.query(RecommendationSnapshot).one()
        assert_consistent(result, stored, snapshots, snap)
        return result
    return make


def assert_consistent(result, stored, snapshots, snap):
    # History and the decision snapshot freeze the same rows and schedule (the response-only
    # noise filter may still relabel a zero-delta row on the HTTP response; see noise_filter.py).
    assert stored["target_allocations"] == snapshots[0]["target_allocations"]
    assert json.loads(snap.projected_allocations_json) == stored["target_allocations"]
    assert json.loads(snap.active_policy_json).get("scheduled_execution") == \
        stored["active_policy"].get("scheduled_execution")
    assert stored["active_policy"].get("scheduled_execution") == result.get("execution_optimization")
    for a in stored["target_allocations"]:
        assert a["current_weight"] == {s: 10.0 for s in ("AAA", "CCC", "EEE", "FFF", "GGG")}.get(a["symbol"], 0.0)
        assert a["allocation_change_percent"] == round(a["target_weight"] - a["current_weight"], 2)
        assert a["estimated_amount"] == round(a["allocation_change_percent"] / 100 * NAV)


def final(result, symbol):
    a = next(a for a in result["target_allocations"] if a["symbol"] == symbol)
    return a["action"], a["current_weight"], a["target_weight"], a["estimated_amount"]


def scheduled(result):
    return (result.get("execution_optimization") or {}).get("scheduled_changes") or {}


def summary(result):
    return {k: [e["symbol"] for e in v] for k, v in result["action_summary"].items() if v}


def proposal_candidate(result):
    return next(c for c in result["strategic_candidates"]["candidates"] if c["family"] != "HOLD")


@pytest.mark.parametrize("path", ["primary", "fallback", "selection"])
def test_cw_a_fake_positive_weight_cannot_shrink_a_new_buy(optimizer_run, path):
    result = optimizer_run([model("WWW", 8, "BUY", w=5)], fallback=path == "fallback", selection=path == "selection")
    assert final(result, "WWW") == ("BUY", 0.0, 8.0, 400_000)          # was cw 5 -> ฿150,000
    assert scheduled(result) == {"WWW": 400_000}
    assert summary(result) == {"new_position": ["WWW"]}               # was "accumulate"
    if path == "fallback":
        assert result["portfolio_assessment"].startswith("[FALLBACK:")
    if path == "selection":
        assert proposal_candidate(result)["eligibility_status"] == "ELIGIBLE"
        assert result["strategy_selection"]["selected_candidate_id"] == proposal_candidate(result)["id"]


def test_cw_a_legacy(optimizer_run):
    result = optimizer_run([model("WWW", 8, "BUY", w=5)], legacy=True)
    assert final(result, "WWW") == ("BUY", 0.0, 8.0, 400_000)
    assert summary(result) == {"new_position": ["WWW"]}


@pytest.mark.parametrize("legacy", [False, True])
def test_cw_a2_fake_weight_above_target_no_longer_hides_the_buy(optimizer_run, legacy):
    # Before: MUJI V2 phantom HOLD 10/10 (no trade); Legacy phantom REDUCE -฿250,000.
    result = optimizer_run([model("WWW", 5, "BUY", w=10)], legacy=legacy)
    assert final(result, "WWW") == ("BUY", 0.0, 5.0, 250_000)
    assert summary(result) == {"new_position": ["WWW"]}
    if not legacy:
        assert scheduled(result) == {"WWW": 250_000}


def test_cw_a3_unheld_sell_is_not_a_trade(optimizer_run):
    result = optimizer_run([model("WWW", 0, "SELL", w=10), model("VVV", 10, "BUY")])
    assert final(result, "WWW") == ("HOLD", 0.0, 0.0, 0)               # was SELL -฿500,000
    assert final(result, "VVV") == ("BUY", 0.0, 10.0, 500_000)
    assert scheduled(result) == {"VVV": 500_000}
    assert summary(result) == {"new_position": ["VVV"]}
    assert "INVALID_TRADE_DIRECTION_OR_AMOUNT" not in result["execution_optimization"]["policy_review_reasons"]


def test_cw_a3_selection_still_rejects_the_phantom_sell(optimizer_run):
    result = optimizer_run([model("WWW", 0, "SELL", w=10), model("VVV", 10, "BUY")], selection=True)
    candidate = proposal_candidate(result)
    assert candidate["eligibility_status"] != "ELIGIBLE"
    assert "UNVERIFIED_SELL:WWW" in candidate["eligibility_reasons"]
    assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"
    assert result["status"] == "NO_ACTION" and scheduled(result) == {}


@pytest.mark.parametrize("selection", [False, True])
def test_cw_a4_fake_negative_weight_cannot_oversize_a_new_buy(optimizer_run, selection):
    # Before: primary scheduled ฿750,000 (15% NAV) for a 5% target; selection rejected the whole
    # proposal (INVALID_WEIGHT_OR_DELTA) only because of the echoed weight.
    result = optimizer_run([model("WWW", 5, "BUY", w=-10)], selection=selection)
    assert final(result, "WWW") == ("BUY", 0.0, 5.0, 250_000)
    assert scheduled(result) == {"WWW": 250_000}
    if selection:
        assert proposal_candidate(result)["eligibility_status"] == "ELIGIBLE"


@pytest.mark.parametrize("fake", [0, 50])
def test_cw_b_c_held_symbol_keeps_its_book_weight(optimizer_run, fake):
    result = optimizer_run([model("AAA", 13, "ACCUMULATE", w=fake)], persona="DIVIDEND")
    assert final(result, "AAA") == ("ACCUMULATE", 10.0, 13.0, 150_000)
    assert scheduled(result) == {"AAA": 150_000}
    assert summary(result) == {"accumulate": ["AAA"]}


def test_cw_e_mixed_fake_weights_use_the_book(optimizer_run):
    result = optimizer_run([model("AAA", 5, "REDUCE", w=15), model("WWW", 5, "BUY", w=0)], sell_signal=("AAA",))
    assert final(result, "AAA") == ("SELL", 10.0, 0.0, -500_000)       # forced exit of the real 10%
    assert final(result, "WWW") == ("BUY", 0.0, 5.0, 250_000)
    assert scheduled(result) == {"AAA": -500_000, "WWW": 250_000}


def test_cw_f_large_target_is_sized_from_zero(optimizer_run):
    result = optimizer_run([model("WWW", 30, "BUY", w=5)])
    assert final(result, "WWW") == ("BUY", 0.0, 30.0, 1_500_000)       # was ฿1,250,000
    assert scheduled(result) == {"WWW": 1_500_000}
    # MUJI V2 has no single-position cap by design; the residual breach is still surfaced for review.
    assert "RESIDUAL_POSITION_BREACH" in result["execution_optimization"]["policy_review_reasons"]


def test_cw_f_legacy_caps_and_trims_from_zero(optimizer_run):
    result = optimizer_run([model("WWW", 30, "BUY", w=5)], legacy=True)
    assert final(result, "WWW") == ("BUY", 0.0, 8.27, 413_500)         # was cw 5 -> ฿163,500


# ── Endpoint: symbol identity ─────────────────────────────────────────────────

@pytest.mark.parametrize("path", ["primary", "fallback", "legacy"])
def test_lowercase_alias_of_a_holding_accumulates_from_the_book_weight(optimizer_run, path):
    # The first 4.17 cut: `aaa` for held AAA (10%) at 13% became a ฿650,000 new buy of "aaa".
    result = optimizer_run([model("aaa", 13, "ACCUMULATE", w=10)], omit=("AAA",),
                           fallback=path == "fallback", legacy=path == "legacy")
    assert final(result, "AAA") == ("ACCUMULATE", 10.0, 13.0, 150_000)
    assert not any(a["symbol"] == "aaa" for a in result["target_allocations"])
    assert summary(result) == {"accumulate": ["AAA"]}
    if path != "legacy":
        assert scheduled(result) == {"AAA": 150_000}
        assert "ESTIMATED_PRICES" not in result["execution_optimization"]["policy_review_reasons"]


def test_lowercase_alias_in_selection_is_the_canonical_holding(optimizer_run):
    result = optimizer_run([model("aaa", 13, "ACCUMULATE", w=10)], omit=("AAA",), selection=True,
                           buy_signal=("AAA",))
    candidate = proposal_candidate(result)
    assert candidate["eligibility_status"] == "ELIGIBLE"
    assert {a["symbol"] for a in candidate["proposed_allocations"]} == {"AAA", "CCC", "EEE", "FFF", "GGG"}
    assert result["strategy_selection"]["selected_candidate_id"] == candidate["id"]
    assert final(result, "AAA") == ("ACCUMULATE", 10.0, 13.0, 150_000)
    assert scheduled(result) == {"AAA": 150_000}
    assert all(a["symbol"] != "aaa" for a in result["target_allocations"])


def test_lowercase_alias_with_no_new_position_allowance_still_accumulates(optimizer_run):
    result = optimizer_run([model("aaa", 13, "ACCUMULATE")], omit=("AAA",), persona="DIVIDEND")
    assert final(result, "AAA") == ("ACCUMULATE", 10.0, 13.0, 150_000)
    assert scheduled(result) == {"AAA": 150_000}


@pytest.mark.parametrize("path", ["primary", "fallback"])
def test_watchlist_symbol_with_inconsistent_casing_is_a_valid_new_buy(optimizer_run, path):
    result = optimizer_run([model("www", 8, "BUY", w=5)], fallback=path == "fallback")
    assert final(result, "WWW") == ("BUY", 0.0, 8.0, 400_000)
    assert scheduled(result) == {"WWW": 400_000}
    assert summary(result) == {"new_position": ["WWW"]}


def test_watchlist_case_variant_still_counts_as_a_new_position(optimizer_run):
    result = optimizer_run([model("www", 8, "BUY")], persona="DIVIDEND")   # max_new_positions 0
    assert final(result, "WWW") == ("HOLD", 0.0, 0.0, 0)
    assert scheduled(result) == {}


@pytest.mark.parametrize("path", ["primary", "fallback", "legacy"])
def test_unknown_symbol_buy_is_never_executable(optimizer_run, path):
    result = optimizer_run([model("QQQ", 5, "BUY", w=2), model("VVV", 5, "BUY")],
                           fallback=path == "fallback", legacy=path == "legacy")
    assert final(result, "QQQ") == ("HOLD", 0.0, 0.0, 0)
    assert final(result, "VVV") == ("BUY", 0.0, 5.0, 250_000)   # valid buys in the same plan unaffected
    assert summary(result) == {"new_position": ["VVV"]}
    if path != "legacy":
        assert scheduled(result) == {"VVV": 250_000}


def test_unknown_symbol_in_selection_keeps_the_unknown_symbol_safeguard(optimizer_run):
    result = optimizer_run([model("QQQ", 5, "BUY")], selection=True)
    candidate = proposal_candidate(result)
    assert candidate["eligibility_status"] == "INELIGIBLE"
    assert "UNKNOWN_SYMBOL" in candidate["eligibility_reasons"]
    assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"
    assert scheduled(result) == {}


def test_ambiguous_watchlist_spelling_is_not_bought(optimizer_run):
    # Watchlist holds both WWW and Www: `www` cannot be attributed to either.
    result = optimizer_run([model("www", 8, "BUY")], extra_watch=("Www",))
    assert final(result, "www") == ("HOLD", 0.0, 0.0, 0)
    assert scheduled(result) == {}


def test_variant_that_duplicates_an_existing_row_is_not_executed(optimizer_run):
    result = optimizer_run([model("AAA", 10, "HOLD"), model("aaa", 20, "ACCUMULATE")])
    assert final(result, "AAA") == ("HOLD", 10.0, 10.0, 0)
    assert final(result, "aaa") == ("HOLD", 0.0, 0.0, 0)
    assert scheduled(result) == {}


def test_lowercase_alias_sell_merges_with_the_forced_exit(optimizer_run):
    # 4.16 HM5b: `aaa` SELL plus the forced AAA exit produced a second, phantom sell row.
    result = optimizer_run([model("aaa", 0, "SELL", w=10), model("WWW", 10, "BUY")], omit=("AAA",),
                           sell_signal=("AAA",))
    assert [a["symbol"] for a in result["target_allocations"]].count("AAA") == 1
    assert final(result, "AAA") == ("SELL", 10.0, 0.0, -500_000)
    assert scheduled(result) == {"AAA": -500_000, "WWW": 500_000}
