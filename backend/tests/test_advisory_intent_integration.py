"""Advisory Integration V1 (Slice 1): /analyze/optimizer end to end, AI mocked.

Runs the real endpoint, the real 3-layer optimizer, stabilization, persistence
and history reads on SQLite. Only call_ai is mocked; every live-data entry
point is stubbed. No provider, network or paid call can happen.
"""
import asyncio
import copy
import json
import os
import sys
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
import main
import agents.optimizer as optimizer_module
from models.database import (
    AgentCache, AnalysisCache, Base, OptimizerHistory, Portfolio, PortfolioItem, RecommendationSnapshot,
    Watchlist,
)

FLAG = "FEATURE_ADVISORY_INTENT_REVIEW_V1"
L1_EMPTY = {"swaps": [], "top_buys": [], "sector_flags": [], "priority": "balanced", "summary": "s."}
L3_OK = {"risk_flags": [], "safer_choice": "layer2", "final_risk_level": "low", "auditor_notes": "ok"}


# ── Harness ───────────────────────────────────────────────────────────────────

class FakeAI:
    """call_ai stand-in: canned JSON per usage_layer, records every prompt."""

    def __init__(self, l2, l1=None, l3=None, fallback=None, fail=(), on_call=None):
        self.responses = {"layer1": l1 or L1_EMPTY, "layer2": l2, "layer3": l3 or L3_OK,
                          "layer1_retry": l1 or L1_EMPTY, "fallback": fallback}
        self.fail = set(fail)
        self.on_call = on_call
        self.prompts: dict[str, list[str]] = {}

    def __call__(self, prompt, *args, **kwargs):
        layer = kwargs["usage_layer"]
        self.prompts.setdefault(layer, []).append(prompt)
        if self.on_call:
            self.on_call(layer)
        if layer in self.fail:
            raise RuntimeError(f"{layer} provider down")
        return {"text": json.dumps(self.responses[layer]), "latency_ms": 1}


def patch_pipeline(monkeypatch, ai, *, quotes=None, currency="THB", snapshot_writer=None):
    from services.analytics import factor_engine, regime_detector
    from services import execution_instrument_facts, optimizer_timing
    from services.decision_memory import calibration, snapshot_writer as sw
    from services.optimizer import execution_penalty

    quotes = quotes or {}

    def no_live(*args, **kwargs):
        raise AssertionError("live analysis must not run in tests")

    monkeypatch.setattr(main, "fetch_price_info",
                        lambda symbol: dict(quotes.get(symbol, {"current_price": 50.0})))
    monkeypatch.setattr(main, "analyze_technical", no_live)
    monkeypatch.setattr(main, "analyze_fundamental", no_live)
    monkeypatch.setattr(optimizer_module, "call_ai", ai)
    monkeypatch.setattr(factor_engine, "compute_portfolio_factor_exposure",
                        lambda *a, **k: {"factor_exposures": {}})
    monkeypatch.setattr(regime_detector, "detect_regime", lambda db: {
        "regime": "SIDEWAYS", "confidence": .7, "transition_stability": "STABLE",
        "constraints": {"min_cash_pct": 5, "max_single_position_pct": 22, "turnover_multiplier": 1},
    })
    monkeypatch.setattr(optimizer_timing, "enrich_scores_with_timing", lambda symbols: {})
    monkeypatch.setattr(execution_instrument_facts, "resolve_execution_instruments",
                        lambda db, symbols: {s: SimpleNamespace(currency=currency) for s in symbols})

    def no_exec_ctx(*a, **k):
        raise RuntimeError("execution context not under test")

    monkeypatch.setattr(execution_penalty, "compute_portfolio_execution_context", no_exec_ctx)
    monkeypatch.setattr(sw, "write_recommendation_snapshot", snapshot_writer or (lambda *a, **k: None))
    monkeypatch.setattr(calibration, "compute_calibration", lambda *a, **k: {})


def session():
    # StaticPool: the optimizer runs in a worker thread; every thread must see
    # the same in-memory database.
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False},
                           poolclass=StaticPool)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def seed(db, holdings, cash, *, sell_signal=(), watch=("WWW",)):
    """holdings: {symbol: (shares, allow_swap)}; created long before any intent."""
    ws = main._ws_id(db)
    portfolio = Portfolio(workspace_id=ws, name="P", cash_balance=cash)
    db.add(portfolio)
    db.flush()
    for symbol, (shares, allow_swap) in holdings.items():
        db.add(PortfolioItem(workspace_id=ws, portfolio_id=portfolio.id, symbol=symbol, shares=shares,
                             avg_cost=40.0, allow_swap=allow_swap, created_at=datetime(2026, 1, 5)))
    for symbol in watch:
        db.add(Watchlist(workspace_id=ws, symbol=symbol, sector="Other"))
    now = datetime.utcnow()
    for symbol in list(holdings) + list(watch):
        db.add(AgentCache(symbol=symbol, agent="technical", cached_at=now,
                          result_json=json.dumps({"ta_score": 50, "trend": "sideways"})))
        db.add(AgentCache(symbol=symbol, agent="fundamental", cached_at=now,
                          result_json=json.dumps({"fa_score": 50, "sector": SECTORS.get(symbol, "Other")})))
    for symbol in sell_signal:
        db.add(AnalysisCache(workspace_id=ws, symbol=symbol, signal="SELL", confidence="HIGH",
                             reasoning="r", risks="r"))
    db.commit()
    return portfolio


def set_intent(db, portfolio, symbol, *, inc=False, dec=False, pref="NONE", expected=None):
    response = main.Response()
    asyncio.run(main.put_position_intent(
        portfolio.id, symbol,
        main.PositionIntentBody(increase_prohibited=inc, decrease_prohibited=dec,
                                soft_preference=pref, expected_revision=expected),
        response, db))


def run(db, portfolio, **body):
    return asyncio.run(main.analyze_optimizer(main.OptimizerRequest(portfolio_id=portfolio.id, **body), db))


# Standard book: five holdings of 10,000 shares at 50 (500,000 each) plus
# 2,500,000 cash → NAV N = 5,000,000. Each holding is 10% of NAV (20% of
# equity, under the 22% policy cap), so trades clear the 5,000 THB noise floor.
HELD = ("AAA", "CCC", "EEE", "FFF", "GGG")
CASH = 2_500_000
# Diversified sectors (each 20% of equity, under every sector cap) so no
# SECTOR_BREACH turns a discretionary trade into policy enforcement.
SECTORS = {"AAA": "Technology", "CCC": "Financial", "EEE": "Healthcare", "FFF": "Consumer", "GGG": "Other"}


def book(**overrides):
    holdings = {symbol: (10_000, True) for symbol in HELD}
    holdings.update(overrides)
    return holdings


def alloc(symbol, tw, sig, r="reason"):
    return {"s": symbol, "tw": tw, "sig": sig, "r": r}


def l2(*allocations, status="REBALANCE"):
    return {"status": status, "rebalance_opportunity_score": 90, "agrees_with_layer1": True,
            "allocations": list(allocations), "portfolio_assessment": "a."}


def plan(**rows):
    """L2 plan covering every held symbol: HOLD at 10% unless overridden as (tw, sig)."""
    allocations = [alloc(symbol, *rows.pop(symbol, (10, "HOLD"))) for symbol in HELD]
    allocations += [alloc(symbol, tw, sig) for symbol, (tw, sig) in rows.items()]
    return l2(*allocations)


def position(envelope, symbol):
    return next(p for p in envelope["positions"] if p["symbol"] == symbol)


@pytest.fixture
def enabled(monkeypatch):
    monkeypatch.setenv(FLAG, "true")


@pytest.fixture
def disabled(monkeypatch):
    monkeypatch.delenv(FLAG, raising=False)


# ── Disabled mode ─────────────────────────────────────────────────────────────

def test_disabled_is_legacy_prompts_response_and_persistence(monkeypatch, disabled):
    """Flag off: intent present or absent changes nothing, and nothing advisory appears."""
    outputs = []
    for with_intent in (False, True):
        ai = FakeAI(plan(AAA=(5, "REDUCE")))
        patch_pipeline(monkeypatch, ai)
        db = session()
        p = seed(db, book(), cash=CASH)
        if with_intent:
            set_intent(db, p, "AAA", dec=True, pref="PREFER_KEEP")
        response = run(db, p)
        stored = json.loads(db.query(OptimizerHistory).one().result_json)
        for volatile in ("analyzed_at", "history_id"):
            response.pop(volatile, None)
            stored.pop(volatile, None)
        outputs.append((ai.prompts, response, stored))
        assert "advisory_intent_review" not in response and "advisory_intent_review" not in stored
        assert "OWNER INVESTOR INTENT" not in json.dumps(ai.prompts)
        # Legacy weights: equity-only current weight (each holding is 20% of equity).
        assert next(a for a in stored["target_allocations"] if a["symbol"] == "AAA")["current_weight"] == 20.0
    assert outputs[0] == outputs[1]


def test_disabled_flag_values(monkeypatch):
    from services.advisory_intent_flag import advisory_intent_review_enabled
    for value, expected in ((None, False), ("false", False), ("1", False), ("TRUE", True), ("true", True)):
        if value is None:
            monkeypatch.delenv(FLAG, raising=False)
        else:
            monkeypatch.setenv(FLAG, value)
        assert advisory_intent_review_enabled() is expected


# ── Enabled: NAV basis and quantities ─────────────────────────────────────────

def test_enabled_uses_common_nav_basis_and_records_mode(monkeypatch, enabled):
    ai = FakeAI(plan(AAA=(5, "REDUCE")))
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", inc=True)
    for symbol in HELD[1:]:
        set_intent(db, p, symbol, dec=True)
    response = run(db, p)
    envelope = response["advisory_intent_review"]
    assert response["advisory_intent_review_status"] == "CAPTURED"
    assert envelope["contract_version"] == "wealth.advisory-intent-review.v1"
    assert envelope["identity"]["mode"] == "ENABLED" and envelope["identity"]["feature_flag"] == FLAG
    assert envelope["valuation"]["status"] == "RESOLVED" and envelope["valuation"]["nav"] == "5000000"
    allocation = {a["symbol"]: a for a in response["target_allocations"]}
    assert allocation["AAA"]["current_weight"] == 10.0          # 500,000 / 5,000,000, not equity-only 20%
    aaa = position(envelope, "AAA")["proposal"]["economic_candidate"]
    assert (aaa["proposed_shares"], aaa["direction"], aaa["target_amount"]) == ("5000", "DECREASE", "250000")
    assert aaa["delta_amount"] == "-250000"
    ccc = position(envelope, "CCC")["proposal"]["final_effective"]
    assert ccc["kind"] == "UNCHANGED_CONTROL" and ccc["proposed_shares"] == "10000"
    assert envelope["review"]["result"] == "CONSISTENT"
    assert envelope["coverage"]["all_resolved_and_consistent"] is True
    assert envelope["coverage"]["referenced_positive_held_count"] == 5
    stored = json.loads(db.query(OptimizerHistory).one().result_json)
    assert stored["advisory_intent_review"] == envelope


def test_stale_quote_preserves_legacy_advice_and_is_unresolved(monkeypatch, enabled):
    ai = FakeAI(plan(AAA=(5, "REDUCE")))
    patch_pipeline(monkeypatch, ai, quotes={"AAA": {"current_price": 50.0, "_stale_data": True}})
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", inc=True)
    response = run(db, p)
    envelope = response["advisory_intent_review"]
    assert envelope["valuation"]["status"] == "UNRESOLVED" and "QUOTE_STALE" in envelope["valuation"]["reasons"]
    # Legacy (equity-only) weights stand when the canonical basis is unresolved.
    rows = {a["symbol"]: a for a in response["target_allocations"]}
    assert rows["AAA"]["current_weight"] == 20.0 and rows["AAA"]["action"] == "REDUCE"
    aaa = position(envelope, "AAA")
    assert aaa["review"]["final"]["outcome"] == "UNRESOLVED"
    assert "VALUATION_BASIS_UNRESOLVED" in aaa["review"]["final"]["reasons"]
    assert envelope["coverage"]["all_resolved_and_consistent"] is False


def test_zero_quote_is_unresolved(monkeypatch, enabled):
    ai = FakeAI(plan(AAA=(5, "REDUCE")))
    patch_pipeline(monkeypatch, ai, quotes={"CCC": {"current_price": 0}})
    db = session()
    p = seed(db, book(), cash=CASH)
    envelope = run(db, p)["advisory_intent_review"]
    assert "QUOTE_ZERO_OR_NEGATIVE" in envelope["valuation"]["reasons"]
    assert "VALUATION_BASIS_UNRESOLVED" in position(envelope, "AAA")["review"]["final"]["reasons"]


def test_mixed_currency_is_unresolved(monkeypatch, enabled):
    ai = FakeAI(plan(AAA=(5, "REDUCE")))
    patch_pipeline(monkeypatch, ai, currency="USD")      # USD holdings, THB cash
    db = session()
    p = seed(db, book(), cash=CASH)
    envelope = run(db, p)["advisory_intent_review"]
    assert "CURRENCY_MIXED" in envelope["valuation"]["reasons"]


def test_missing_allocation_and_zero_share_anomaly(monkeypatch, enabled):
    ai = FakeAI(l2(*[alloc(s, 10, "HOLD") for s in HELD[1:]]))      # L2 omits held AAA
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(ZZZ=(0, True)), cash=CASH)
    envelope = run(db, p)["advisory_intent_review"]
    assert position(envelope, "AAA")["review"]["final"]["reasons"] == ["MISSING_ALLOCATION", "NO_CONFIRMED_INTENT"]
    assert {"code": "ZERO_SHARE_HOLDING", "symbol": "ZZZ"} in envelope["reference"]["anomalies"]
    assert envelope["coverage"]["referenced_positive_held_count"] == 5


def test_duplicate_allocation_rows_are_unresolved(monkeypatch, enabled):
    ai = FakeAI(l2(*[alloc(s, 10, "HOLD") for s in HELD], alloc("AAA", 5, "REDUCE")))
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", dec=True)
    response = run(db, p)
    # The optimizer keyed rows by symbol; the review checks the economic rows it was given.
    rows = [a for a in response["target_allocations"] if a["symbol"] == "AAA"]
    review = position(response["advisory_intent_review"], "AAA")["review"]["final"]
    if len(rows) > 1:
        assert review["reasons"] == ["DUPLICATE_ALLOCATION"]
    else:
        assert review["outcome"] in ("CONFLICT", "CONSISTENT")


def test_missing_and_reconfirmation_required_intent_are_unresolved(monkeypatch, enabled):
    ai = FakeAI(plan())
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "CCC", dec=True)
    # Re-entry after the intent was confirmed: the holding episode is newer.
    item = db.query(PortfolioItem).filter_by(symbol="CCC").one()
    item.created_at = datetime(2099, 1, 1)
    db.commit()
    envelope = run(db, p)["advisory_intent_review"]
    aaa, ccc = position(envelope, "AAA"), position(envelope, "CCC")
    assert aaa["intent"] is None and aaa["review"]["final"]["outcome"] == "UNRESOLVED"
    assert "NO_CONFIRMED_INTENT" in aaa["review"]["final"]["reasons"]
    assert ccc["applicability"] == "RECONFIRMATION_REQUIRED" and ccc["intent"] is None
    assert ccc["historical_intent"]["revision"] == 1           # evidence only, not applied
    assert "RECONFIRMATION_REQUIRED" in ccc["review"]["final"]["reasons"]
    assert ccc["proposal"]["final_effective"]["direction"] == "NO_CHANGE"   # still unresolved
    assert envelope["review"]["result"] == "UNRESOLVED"
    assert envelope["coverage"]["unresolved_positions"] == list(HELD)


# ── Enabled: prompt context ───────────────────────────────────────────────────

def test_hard_context_reaches_l1_l2_l3_and_soft_only_l2(monkeypatch, enabled):
    ai = FakeAI(plan())
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", dec=True, pref="PREFER_KEEP")
    envelope = run(db, p)["advisory_intent_review"]
    for layer in ("layer1", "layer2", "layer3"):
        prompt = ai.prompts[layer][0]
        assert "- AAA: do not decrease" in prompt
        assert "CCC (no confirmed intent)" in prompt
        assert "do not treat either side as automatically winning" in prompt
        assert "override" in prompt and "forced exits automatically override" not in prompt
    assert "AAA: owner prefers to keep" in ai.prompts["layer2"][0]
    assert "prefers to keep" not in ai.prompts["layer1"][0] + ai.prompts["layer3"][0]
    path = envelope["prompt_use"]["path"]
    assert [(e["layer"], e["outcome"], e["context"]) for e in path] == [
        ("L1", "SUCCESS", "HARD"), ("L2", "SUCCESS", "HARD_AND_SOFT"), ("L3", "SUCCESS", "HARD")]
    assert envelope["prompt_use"]["intended_layers"]["soft"] == ["L2", "FALLBACK"]


def test_retry_and_fallback_reuse_the_frozen_context_and_abandon_primary(monkeypatch, enabled):
    fallback = {"status": "REBALANCE", "allocations": [alloc(s, 10, "HOLD") for s in HELD]}
    ai = FakeAI(l2=None, l1={"swaps": [{"sell": "AAA", "buy": None, "type": "SELL", "r": "exit"}],
                              "top_buys": [], "sector_flags": [], "priority": "x"},
                fallback=fallback, fail={"layer2"})
    # L2 fails → L2 plan empty → global single-shot fallback.
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", dec=True, pref="PREFER_EXIT")
    response = run(db, p)
    envelope = response["advisory_intent_review"]
    assert response["fallback_mode"] is True
    assert "- AAA: do not decrease" in ai.prompts["fallback"][0]
    assert "AAA: owner prefers to exit" in ai.prompts["fallback"][0]   # fallback substitutes for L2
    path = {(e["layer"], e["attempt"]): e for e in envelope["prompt_use"]["path"]}
    assert path[("L1", "PRIMARY")]["outcome"] == "ABANDONED"
    assert path[("L2", "PRIMARY")]["outcome"] == "FAILED"
    assert path[("FALLBACK", "FALLBACK")]["outcome"] == "SUCCESS"
    hard_l1 = ai.prompts["layer1"][0].split("[OWNER INVESTOR INTENT")[1].split("\n\n")[0]
    assert hard_l1 in ai.prompts["fallback"][0]                         # same frozen hard context
    aaa = position(envelope, "AAA")
    # The abandoned L1 SELL proposal never counts as a retained conflict.
    assert aaa["review"]["retained"] == [] and aaa["review"]["final"]["outcome"] == "CONSISTENT"
    assert envelope["coverage"]["conflict_positions"] == []
    abandoned = [p_ for p_ in envelope["provenance"]["proposals"] if p_["disposition"] == "ABANDONED"]
    assert [(p_["symbol"], p_["stage"]) for p_ in abandoned] == [("AAA", "L1_STRATEGIST")]


def test_l1_retry_carries_hard_context(monkeypatch, enabled):
    class FlakyL1(FakeAI):
        def __call__(self, prompt, *args, **kwargs):
            if kwargs["usage_layer"] == "layer1":
                self.prompts.setdefault("layer1", []).append(prompt)
                return {"text": "not json", "latency_ms": 1}
            return super().__call__(prompt, *args, **kwargs)

    ai = FlakyL1(plan())
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", inc=True)
    envelope = run(db, p)["advisory_intent_review"]
    assert "- AAA: do not increase" in ai.prompts["layer1_retry"][0]
    path = [(e["layer"], e["outcome"]) for e in envelope["prompt_use"]["path"]]
    assert path[:2] == [("L1", "FAILED"), ("L1_RETRY", "SUCCESS")]
    digests = {e["context_digest"] for e in envelope["prompt_use"]["path"] if e["layer"] in ("L1", "L1_RETRY")}
    assert len(digests) == 1


def test_intent_revision_is_frozen_for_the_whole_run(monkeypatch, enabled):
    holder = {}

    def revise_mid_run(layer):
        if layer == "layer2" and not holder.get("done"):
            holder["done"] = True
            set_intent(holder["db"], holder["p"], "AAA", inc=False, dec=False, expected=1)

    ai = FakeAI(plan(AAA=(5, "REDUCE")), on_call=revise_mid_run)
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", dec=True)
    holder.update(db=db, p=p)
    envelope = run(db, p)["advisory_intent_review"]
    aaa = position(envelope, "AAA")
    assert holder["done"] is True
    assert aaa["intent"]["revision"] == 1 and aaa["hard_restrictions"]["decrease_prohibited"] is True
    assert "- AAA: do not decrease" in ai.prompts["layer3"][0]       # L3 ran after the revision
    assert aaa["review"]["final"]["outcome"] == "CONFLICT"          # judged on the frozen revision


# ── Enabled: final vs retained proposals ──────────────────────────────────────

def test_locked_forced_sell_final_consistent_retained_conflict(monkeypatch, enabled):
    ai = FakeAI(plan())
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(AAA=(10_000, False)), cash=CASH, sell_signal=("AAA",))
    set_intent(db, p, "AAA", dec=True)
    response = run(db, p)
    envelope = response["advisory_intent_review"]
    aaa = position(envelope, "AAA")
    final = aaa["review"]["final"]
    assert aaa["proposal"]["final_effective"]["proposed_shares"] == "10000"
    assert (final["direction"], final["outcome"]) == ("NO_CHANGE", "CONSISTENT")
    [retained] = aaa["review"]["retained"]
    assert retained["source"] == "SYSTEM_RULE" and retained["stage"] == "FORCED_SELL"
    assert retained["projection"]["proposed_shares"] == "0"
    assert retained["review"]["outcome"] == "CONFLICT"
    assert retained["review"]["restriction"] == "DECREASE_PROHIBITED_BY_OWNER"
    assert (retained["disposition"], retained["suppressed_by"]) == ("SUPPRESSED", "LEGACY_ALLOW_SWAP")
    assert retained["materiality"] == "MATERIAL" and aaa["review"]["non_material_provenance"] == []
    assert aaa["review"]["requires_owner_decision"] is True
    coverage = envelope["coverage"]
    assert coverage["final_conflict_positions"] == [] and coverage["retained_conflict_positions"] == ["AAA"]
    assert coverage["conflict_positions"] == ["AAA"]
    assert envelope["review"]["requires_owner_decision"] is True
    # Provenance: L2 HOLD → forced SELL replaces → legacy lock suppresses.
    effects = [(t["stage"], t["effect"]) for t in aaa["provenance"]]
    assert effects[:3] == [("L2_ALLOCATION", "ORIGINATE"), ("FORCED_SELL", "REPLACE"),
                           ("LEGACY_ALLOW_SWAP", "SUPPRESS")]
    # The plan itself is untouched: AAA is still an unchanged HOLD.
    assert {a["symbol"]: a for a in response["target_allocations"]}["AAA"]["action"] == "HOLD"


def test_policy_trim_reversing_buy_to_reduce(monkeypatch, enabled):
    # Targets sum to 111% → the policy cash floor trims the only BUY (AAA 21%)
    # below its 10% current weight; reconciliation relabels it REDUCE.
    ai = FakeAI(plan(AAA=(21, "BUY"), CCC=(22.5, "HOLD"), EEE=(22.5, "HOLD"),
                     FFF=(22.5, "HOLD"), GGG=(22.5, "HOLD")))
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", inc=True)
    response = run(db, p)
    row = {a["symbol"]: a for a in response["target_allocations"]}["AAA"]
    assert row["action"] == "REDUCE" and row["target_weight"] < row["current_weight"] == 10.0
    aaa = position(response["advisory_intent_review"], "AAA")
    assert [(t["source"], t["stage"], t["effect"], t["reason_code"]) for t in aaa["provenance"]] == [
        ("ADVISORY", "L2_ALLOCATION", "ORIGINATE", "L2_ALLOCATION"),
        ("POLICY_RISK", "HARD_POLICY", "REPLACE", "CASH_FLOOR_TRIM"),     # reversal ⇒ new proposal
        ("SYSTEM_RULE", "ACTION_RECONCILIATION", "RELABEL", "ACTION_RECONCILE"),
        # A discretionary REDUCE with nothing to fund is scheduled later, not dropped.
        ("SYSTEM_RULE", "EXECUTION_SCHEDULING", "DEFER", "EXECUTION_NOT_NEEDED_TODAY"),
    ]
    final = aaa["proposal"]["final_effective"]
    expected_shares = Decimal(str(row["target_weight"])) * 5_000_000 / 100 / 50
    assert final["direction"] == "DECREASE" and Decimal(final["proposed_shares"]) == expected_shares
    assert aaa["review"]["final"]["outcome"] == "CONSISTENT"           # do-not-increase vs a decrease
    [retained] = aaa["review"]["retained"]
    assert (retained["source"], retained["action"], retained["disposition"]) == ("ADVISORY", "BUY", "REPLACED")
    assert retained["review"]["outcome"] == "CONFLICT"                  # the advisory saw a reason to increase
    # A deterministic policy reversal is on the material path: it still needs the owner.
    assert retained["materiality"] == "MATERIAL"
    assert aaa["review"]["requires_owner_decision"] is True
    assert response["advisory_intent_review"]["coverage"]["retained_conflict_positions"] == ["AAA"]
    # Mixed-basis evidence: the target is the legacy policy rule's output,
    # projected onto the frozen common NAV for review only.
    assert final["basis_evidence"] == {
        "projection_basis": "COMMON_NAV_FROZEN_QUOTES", "target_origin_stage": "HARD_POLICY",
        "target_origin_semantics": "LEGACY_POLICY_RULE", "row_current_weight_basis": "COMMON_NAV_FROZEN_QUOTES"}
    trim = next(t for t in aaa["provenance"] if t["stage"] == "HARD_POLICY")
    assert trim["rule_semantics"] == "LEGACY_POLICY_RULE"
    assert retained["projection"]["basis_evidence"]["target_origin_semantics"] == "ADVISORY_MODEL_OUTPUT"
    boundary = response["advisory_intent_review"]["valuation"]["basis_boundary"]
    assert boundary["name"] == "SLICE1_TEMPORARY_MIXED_BASIS"
    assert "HARD_POLICY_RULES" in boundary["legacy_basis_retained_for"]
    assert "HARD_POLICY_RULES" not in boundary["common_nav_applies_to"]


def l1_sell(symbol, swap_type):
    """L1 strategist output with one sell leg on a held symbol."""
    swap = ({"sell": symbol, "buy": None, "type": "SELL", "r": "exit"} if swap_type == "SELL"
            else {"sell": symbol, "buy": "WWW", "type": "SWAP", "r": "rotate"})
    return {"swaps": [swap], "top_buys": [], "sector_flags": [], "priority": "x", "summary": "s."}


@pytest.mark.parametrize("swap_type, locked", [("SELL", False), ("SWAP", False), ("SELL", True)])
def test_superseded_l1_leg_is_non_material_provenance(monkeypatch, enabled, swap_type, locked):
    """L1 reduce/sell superseded by an accepted L2 HOLD: no owner-facing conflict."""
    ai = FakeAI(plan(), l1=l1_sell("AAA", swap_type))
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(AAA=(10_000, not locked)), cash=CASH)
    set_intent(db, p, "AAA", dec=True)
    response = run(db, p)
    envelope = response["advisory_intent_review"]
    aaa = position(envelope, "AAA")
    # Not a retained conflict, not counted, no owner decision, not shown as material.
    assert aaa["review"]["retained"] == []
    assert aaa["review"]["status"] == "CONSISTENT" and aaa["review"]["final"]["outcome"] == "CONSISTENT"
    assert aaa["review"]["requires_owner_decision"] is False
    assert envelope["review"]["requires_owner_decision"] is False
    coverage = envelope["coverage"]
    assert coverage["conflict_positions"] == coverage["retained_conflict_positions"] == []
    assert aaa["display"]["material_change"] is False and aaa["display"]["show"] is False
    # The L1 leg is still in provenance, classified as intermediate reasoning.
    l1 = [t for t in aaa["provenance"] if t["stage"] == "L1_STRATEGIST"]
    assert len(l1) == 1 and l1[0]["materiality"] == "INTERMEDIATE_REASONING"
    excluded = aaa["review"]["non_material_provenance"]
    assert excluded[0]["stage"] == "L1_STRATEGIST"
    assert {e["excluded_from_review"] for e in excluded} == {"SUPERSEDED_INTERMEDIATE_REASONING"}
    assert {e["materiality"] for e in excluded} == {"INTERMEDIATE_REASONING"}
    if locked:   # the lock's placeholder for the dropped leg is intermediate too
        assert [e["stage"] for e in excluded] == ["L1_STRATEGIST", "LEGACY_ALLOW_SWAP"]
        assert excluded[0]["disposition"] == "SUPPRESSED"
    else:
        assert [e["stage"] for e in excluded] == ["L1_STRATEGIST"]
        assert excluded[0]["disposition"] == "REPLACED"
    l2_origin = next(t for t in aaa["provenance"] if t["stage"] == "L2_ALLOCATION")
    assert l2_origin["materiality"] == "MATERIAL"


def test_locked_forced_sell_still_conflicts_beside_a_superseded_l1_leg(monkeypatch, enabled):
    ai = FakeAI(plan(), l1=l1_sell("AAA", "SELL"))
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(AAA=(10_000, False)), cash=CASH, sell_signal=("AAA",))
    set_intent(db, p, "AAA", dec=True)
    envelope = run(db, p)["advisory_intent_review"]
    aaa = position(envelope, "AAA")
    [retained] = aaa["review"]["retained"]
    assert (retained["stage"], retained["disposition"], retained["materiality"]) == (
        "FORCED_SELL", "SUPPRESSED", "MATERIAL")
    assert retained["review"]["outcome"] == "CONFLICT"
    assert retained["projection"]["basis_evidence"]["target_origin_semantics"] == "LEGACY_SYSTEM_RULE"
    assert aaa["review"]["requires_owner_decision"] is True
    assert envelope["coverage"]["retained_conflict_positions"] == ["AAA"]
    assert [e["stage"] for e in aaa["review"]["non_material_provenance"]] == [
        "L1_STRATEGIST", "LEGACY_ALLOW_SWAP"]


def test_noise_suppressed_sell(monkeypatch, enabled):
    # DDD is 0.2% of NAV; SELL to 0 is below the 1% noise drift threshold.
    ai = FakeAI(plan(DDD=(0, "SELL")))
    patch_pipeline(monkeypatch, ai, quotes={"DDD": {"current_price": 1.0}})
    db = session()
    p = seed(db, book(DDD=(10_000, True)), cash=CASH - 10_000)       # N = 5,000,000
    set_intent(db, p, "DDD", dec=True)
    response = run(db, p)
    envelope = response["advisory_intent_review"]
    ddd = position(envelope, "DDD")
    assert ddd["review"]["final"]["outcome"] == "CONSISTENT"
    assert ddd["proposal"]["final_effective"]["proposed_shares"] == "10000"
    assert ddd["proposal"]["economic_candidate"]["proposed_shares"] == "0"
    [retained] = ddd["review"]["retained"]
    assert (retained["disposition"], retained["suppressed_by"]) == ("SUPPRESSED", "NOISE_FILTER")
    assert retained["review"]["outcome"] == "CONFLICT"
    assert ddd["display"]["final_disposition"] == "NOISE_SUPPRESSED"
    assert any(t["reason_code"] == "NOISE_DRIFT_BELOW_THRESHOLD" for t in ddd["provenance"])
    # Economic row persisted unfiltered; the response row is the noise-filtered view.
    stored = json.loads(db.query(OptimizerHistory).one().result_json)
    assert {a["symbol"]: a for a in stored["target_allocations"]}["DDD"]["action"] == "SELL"
    assert {a["symbol"]: a for a in response["target_allocations"]}["DDD"]["action"] == "HOLD"


def test_stabilization_drift_deferral_is_a_disposition(monkeypatch, enabled):
    # AAA 10% → 8% is inside the 3% drift band; CCC 10% → 2% keeps the run REBALANCE.
    ai = FakeAI(plan(AAA=(8, "REDUCE"), CCC=(2, "REDUCE")))
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", dec=True)
    response = run(db, p)
    envelope = response["advisory_intent_review"]
    aaa = position(envelope, "AAA")
    assert envelope["display"]["stabilization_status"] == "REBALANCE"
    assert aaa["display"]["final_disposition"] == "DEFERRED_WITHIN_DRIFT_TOLERANCE"
    assert aaa["proposal"]["final_effective"]["direction"] == "NO_CHANGE"
    assert aaa["review"]["final"]["outcome"] == "CONSISTENT"
    [retained] = aaa["review"]["retained"]
    assert retained["disposition"] == "DEFERRED" and retained["review"]["outcome"] == "CONFLICT"
    assert any(t["stage"] == "STABILIZATION" and t["effect"] == "DEFER" for t in aaa["provenance"])


def test_scheduling_is_separate_from_the_economic_proposal(monkeypatch, enabled):
    # A discretionary REDUCE with no buys to fund is DEFERRED by execution optimization.
    ai = FakeAI(plan(AAA=(4, "REDUCE")))
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", inc=True)
    response = run(db, p)
    envelope = response["advisory_intent_review"]
    aaa = position(envelope, "AAA")
    scheduled = aaa["proposal"]["scheduled"]
    assert scheduled["execution_state"] == "DEFERRED" and scheduled["executed_amount"] == 0.0
    assert scheduled["scheduled_proposed_shares"] == "10000"
    # The economic recommendation is unchanged by scheduling.
    assert aaa["proposal"]["final_effective"]["proposed_shares"] == "4000"
    assert aaa["proposal"]["final_effective"]["direction"] == "DECREASE"
    assert any(t["stage"] == "EXECUTION_SCHEDULING" and t["effect"] == "DEFER" for t in aaa["provenance"])
    assert aaa["review"]["final"]["outcome"] == "CONSISTENT"
    # Scheduling ran exactly once: response carries it, the economic row does not.
    stored = json.loads(db.query(OptimizerHistory).one().result_json)
    assert "execution_optimization" not in stored and "execution_optimization" in response
    assert {a["symbol"]: a for a in stored["target_allocations"]}["AAA"]["action"] == "REDUCE"


def test_conflicts_cause_no_redistribution_and_no_governance_penalty(monkeypatch, enabled):
    def once(intent_fields):
        ai = FakeAI(plan(AAA=(5, "REDUCE")))
        patch_pipeline(monkeypatch, ai)
        db = session()
        p = seed(db, book(), cash=CASH)
        set_intent(db, p, "AAA", **intent_fields)
        return run(db, p)

    unrestricted, restricted = once({}), once({"dec": True})
    assert restricted["advisory_intent_review"]["review"]["result"] == "CONFLICT"
    assert unrestricted["advisory_intent_review"]["review"]["requires_owner_decision"] is False
    for key in ("target_allocations", "consensus", "active_policy", "status", "execution_optimization",
                "action_summary", "swap_suggestions"):
        assert restricted[key] == unrestricted[key], key
    gov = restricted["consensus"].get("governance_flags") or []
    assert not any("INTENT" in flag.upper() for flag in gov)
    assert restricted["advisory_intent_review"]["review"]["not_a_governance_violation"] is True
    assert restricted["advisory_intent_review"]["review"]["allocations_changed_by_review"] is False


# ── Persistence and historical reads ──────────────────────────────────────────

def test_history_read_is_frozen_against_later_intent_and_threshold_changes(monkeypatch, enabled):
    ai = FakeAI(plan(AAA=(5, "REDUCE")))
    patch_pipeline(monkeypatch, ai)
    db = session()
    p = seed(db, book(), cash=CASH)
    set_intent(db, p, "AAA", dec=True)
    live = run(db, p)["advisory_intent_review"]
    history_id = db.query(OptimizerHistory).one().id

    set_intent(db, p, "AAA", dec=False, expected=1)                     # owner changes mind
    from services import noise_filter
    monkeypatch.setattr(noise_filter, "DRIFT_THRESHOLD_PCT", 50.0)      # thresholds change
    detail = asyncio.run(main.get_optimizer_history_detail(history_id, db))
    assert detail["advisory_intent_review_status"] == "CAPTURED"
    assert detail["advisory_intent_review"] == live
    assert position(detail["advisory_intent_review"], "AAA")["review"]["final"]["outcome"] == "CONFLICT"
    assert detail["advisory_intent_changes_since_run"] == [
        {"symbol": "AAA", "run_intent_revision": 1, "current_intent_revision": 2}]


def test_history_read_not_captured_and_evidence_invalid(monkeypatch, enabled):
    db = session()
    ws = main._ws_id(db)
    p = Portfolio(workspace_id=ws, name="P")
    db.add(p)
    db.flush()
    legacy = OptimizerHistory(workspace_id=ws, portfolio_id=p.id, portfolio_name="P",
                              analyzed_at=datetime.utcnow(), result_json=json.dumps({"status": "REBALANCE"}))
    db.add(legacy)
    db.commit()
    detail = asyncio.run(main.get_optimizer_history_detail(legacy.id, db))
    assert detail["advisory_intent_review_status"] == "NOT_CAPTURED" and detail["advisory_intent_review"] is None

    ai = FakeAI(plan())
    patch_pipeline(monkeypatch, ai)
    p2 = seed(db, book(), cash=CASH)
    run(db, p2)
    row = db.query(OptimizerHistory).filter_by(portfolio_id=p2.id).one()
    payload = json.loads(row.result_json)
    payload["advisory_intent_review"]["review"]["requires_owner_decision"] = True   # tampered
    row.result_json = json.dumps(payload)
    db.commit()
    detail = asyncio.run(main.get_optimizer_history_detail(row.id, db))
    assert detail["advisory_intent_review_status"] == "EVIDENCE_INVALID"
    assert detail["advisory_intent_review"] is None

    payload["advisory_intent_review"] = {"contract_version": "wealth.advisory-intent-review.v0"}
    row.result_json = json.dumps(payload)
    db.commit()
    detail = asyncio.run(main.get_optimizer_history_detail(row.id, db))
    assert detail["advisory_intent_review_status"] == "EVIDENCE_INVALID"


def test_snapshot_failure_leaves_history_evidence_and_snapshot_reads_through(monkeypatch, enabled):
    def failing_writer(*a, **k):
        raise RuntimeError("snapshot store down")

    ai = FakeAI(plan(AAA=(5, "REDUCE")))
    patch_pipeline(monkeypatch, ai, snapshot_writer=failing_writer)
    db = session()
    p = seed(db, book(), cash=CASH)
    response = run(db, p)
    assert "recommendation_snapshot_id" not in response
    stored = json.loads(db.query(OptimizerHistory).one().result_json)
    assert stored["advisory_intent_review"] == response["advisory_intent_review"]

    # A snapshot row reads the envelope through its OptimizerHistory link; the
    # envelope is not duplicated into RecommendationSnapshot columns.
    history = db.query(OptimizerHistory).one()
    snap = RecommendationSnapshot(workspace_id=history.workspace_id, portfolio_id=p.id,
                                  optimizer_history_id=history.id)
    db.add(snap)
    db.commit()
    detail = asyncio.run(main.get_recommendation_snapshot(snap.id, db))
    assert detail["advisory_intent_review_status"] == "CAPTURED"
    assert detail["advisory_intent_review"] == response["advisory_intent_review"]
    columns = {c.name for c in RecommendationSnapshot.__table__.columns}
    assert not any("intent" in name for name in columns)


def test_disabled_history_and_snapshot_reads_have_no_advisory_fields(monkeypatch, disabled):
    db = session()
    ws = main._ws_id(db)
    p = Portfolio(workspace_id=ws, name="P")
    db.add(p)
    db.flush()
    row = OptimizerHistory(workspace_id=ws, portfolio_id=p.id, portfolio_name="P",
                           analyzed_at=datetime.utcnow(), result_json=json.dumps({"status": "REBALANCE"}))
    db.add(row)
    db.flush()
    snap = RecommendationSnapshot(workspace_id=ws, portfolio_id=p.id, optimizer_history_id=row.id)
    db.add(snap)
    db.commit()
    assert "advisory_intent_review_status" not in asyncio.run(main.get_optimizer_history_detail(row.id, db))
    assert "advisory_intent_review_status" not in asyncio.run(main.get_recommendation_snapshot(snap.id, db))


def test_intent_api_disclosure_follows_the_flag(monkeypatch):
    db = session()
    ws = main._ws_id(db)
    p = Portfolio(workspace_id=ws, name="P")
    db.add(p)
    db.commit()
    monkeypatch.delenv(FLAG, raising=False)
    off = asyncio.run(main.list_position_intents(p.id, db))
    assert "not yet read" in off["disclosure"] and off["advisory_review_enabled"] is False
    monkeypatch.setenv(FLAG, "true")
    on = asyncio.run(main.list_position_intents(p.id, db))
    assert on["advisory_review_enabled"] is True and on["enforced_by_optimizer"] is False
    assert "do not read your intent yet" in on["disclosure"] and "not yet read or" not in on["disclosure"]
