"""MUJI V2 Phase 4 Slice 4.2 — honest evidence provenance.

Golden fixtures were captured from baseline f888ebc (before this slice) with the
same inputs and no provenance argument. Regenerate only deliberately, on
baseline code: REGENERATE_PROVENANCE_BASELINE=1.
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import agents.optimizer as optimizer
from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY
from services.optimizer import strategic_candidates as sc
from services.optimizer.strategic_candidates import (
    SELECTION_VERSION, prepare_candidates, validate_candidate_reviews,
)

GOLDEN = os.path.join(os.path.dirname(__file__), "fixtures", "evidence_provenance_baseline.json")
REGENERATE = bool(os.environ.get("REGENERATE_PROVENANCE_BASELINE"))


def _golden(key, value):
    """Return the stored baseline for key; in regeneration mode store value first."""
    data = json.load(open(GOLDEN, encoding="utf-8")) if os.path.exists(GOLDEN) else {}
    if REGENERATE:
        data[key] = value
        with open(GOLDEN, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
    return data[key]


def _canonical(value):
    return json.loads(json.dumps(value, sort_keys=True, default=str))


# Rows carry the defaulted values main.py produces today: HOLD for a missing
# analysis signal, 0 for a failed/missing score, 0 timing without price data.
HOLDINGS = [
    {"symbol": "AAA", "shares": 60, "current_price": 10, "weight_pct": 60, "signal": "SELL",
     "fa_score": 30, "ta_score": 0, "pe_ratio": 40, "timing_score": 0,
     "timing_data_available": False},
    {"symbol": "BBB", "shares": 20, "current_price": 10, "weight_pct": 20, "signal": "HOLD",
     "fa_score": 0, "ta_score": 55, "pe_ratio": 12, "roe": 0.2, "timing_score": 62,
     "timing_data_available": True},
]
WATCHLIST = [
    {"symbol": "WWW", "current_price": 5, "signal": "BUY", "fa_score": 60, "ta_score": 0,
     "pe_ratio": 9, "timing_score": 0, "timing_data_available": False},
    {"symbol": "ZZZ", "current_price": 5, "signal": "HOLD", "fa_score": 0, "ta_score": 0},
]
OBS = {"status": "OBSERVED", "source": "AGENT_CACHE"}
PROVENANCE = {
    "AAA": {"signal": {"status": "OBSERVED", "source": "ANALYSIS_CACHE", "as_of": "2026-11-01T00:00:00"},
            "ta_score": OBS,  # genuine observed 0
            "fa_score": OBS,
            "timing_score": {"status": "MISSING", "source": "TIMING_INTELLIGENCE"}},
    "BBB": {"signal": {"status": "MISSING", "source": "ANALYSIS_CACHE"},
            "ta_score": OBS,
            "fa_score": {"status": "FAILED", "source": "LIVE"},
            "timing_score": {"status": "OBSERVED", "source": "TIMING_INTELLIGENCE"}},
    "WWW": {"signal": {"status": "OBSERVED", "source": "ANALYSIS_CACHE", "as_of": "2026-11-02T00:00:00"},
            "ta_score": {"status": "DISABLED"}, "fa_score": OBS,
            "timing_score": {"status": "MISSING", "source": "TIMING_INTELLIGENCE"}},
    "ZZZ": {"signal": {"status": "MISSING", "source": "ANALYSIS_CACHE"},
            "ta_score": {"status": "MISSING", "source": "AGENT_CACHE"},
            "fa_score": {"status": "MISSING", "source": "AGENT_CACHE"},
            "timing_score": {"status": "MISSING", "source": "TIMING_INTELLIGENCE"}},
}
REGIME = {"regime": "HIGH_VOLATILITY", "confidence_pct": 85}
L2_REPLY = {"allocations": [
    {"s": "AAA", "tw": 0, "sig": "SELL", "decision_basis": "INVESTMENT_THESIS"},
    {"s": "BBB", "tw": 20, "sig": "HOLD"}],
    "strategy_family": "RAISE_CASH", "observed_evidence_refs": ["symbol:AAA:signal"],
    "cash_balance_target": 80, "status": "REBALANCE"}

SCENARIOS = {
    "legacy": {},
    "sector_advisory_v1": {"sector_policy_mode": SECTOR_POLICY_ADVISORY},
    "muji_v2_challenger": {"sector_policy_mode": SECTOR_POLICY_ADVISORY,
                           "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2},
}
OPT_IN = {"sector_policy_mode": SECTOR_POLICY_ADVISORY,
          "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2,
          "strategy_selection_mode": SELECTION_VERSION}


def _run(monkeypatch, layer3_reply=None, l2_reply=L2_REPLY, **kwargs):
    captured = {}

    def fake_ai(prompt, provider, model, *args, usage_layer, max_tokens=None, **kw):
        captured[usage_layer] = {"prompt": prompt, "max_tokens": max_tokens}
        if usage_layer == "layer1":
            payload = {"swaps": [], "top_buys": []}
        elif usage_layer == "layer2":
            payload = l2_reply
        elif usage_layer == "layer3":
            payload = layer3_reply(prompt) if layer3_reply else {"risk_flags": []}
        elif usage_layer == "committee":
            payload = {"selected_candidate_id": "hold-current", "supporting_evidence_refs": [],
                       "opposing_evidence_refs": [], "comparison_against_hold": "Waiting is preferable.",
                       "decision_rationale": "Hold the current portfolio.", "material_uncertainty": []}
        else:
            payload = {"allocations": [], "status": "NO_ACTION", "cash_balance_target": 20,
                       "risk_flags": []}
        return {"text": json.dumps(payload), "latency_ms": 1}

    monkeypatch.setattr(optimizer, "call_ai", fake_ai)
    result = optimizer.run_layered_optimizer(
        [dict(row) for row in HOLDINGS], [dict(row) for row in WATCHLIST], "P",
        cash_balance=200, **kwargs)
    return result, captured


# ── Opt-in OFF: byte-for-byte preservation (pipeline) ────────────────────────

@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_baseline_optin_off_prompts_and_allocations_unchanged(monkeypatch, name):
    extra = {} if REGENERATE else {"evidence_provenance": PROVENANCE}
    result, captured = _run(monkeypatch, regime_context=REGIME, **SCENARIOS[name], **extra)
    observed = {
        "prompts": {layer: captured[layer] for layer in ("layer1", "layer2", "layer3")},
        "target_allocations": _canonical(result.get("target_allocations")),
        "target_cash_weight": result.get("target_cash_weight"),
    }
    baseline = _golden(f"pipeline:{name}", observed)
    for layer in ("layer1", "layer2", "layer3"):
        assert observed["prompts"][layer]["prompt"] == baseline["prompts"][layer]["prompt"], layer
        assert observed["prompts"][layer]["max_tokens"] == baseline["prompts"][layer]["max_tokens"], layer
    assert observed["target_allocations"] == baseline["target_allocations"]
    assert observed["target_cash_weight"] == baseline["target_cash_weight"]
    assert "committee" not in captured
    if not REGENERATE and name == "muji_v2_challenger":
        # Challenger-owned envelope ignores provenance and says so.
        envelope = result["strategic_candidates"]
        assert envelope["evidence_provenance_status"] == "NOT_SUPPLIED"
        assert "unobserved_evidence" not in envelope


# ── main.py endpoint: scores map, call arguments and snapshot input ─────────

def _endpoint_capture(monkeypatch, *, opt_in):
    import main
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import models.asset  # noqa: F401
    import models.registry_finding  # noqa: F401
    from models.database import AgentCache, AnalysisCache, Base, Portfolio, PortfolioItem, Watchlist
    from services.analytics import factor_engine, regime_detector
    from services import execution_instrument_facts, optimizer_timing
    from services.decision_memory import calibration, snapshot_writer

    calls, snapshots = [], []

    def fake_optimizer(*args, **kwargs):
        kwargs = dict(kwargs)
        kwargs.pop("on_stage")
        calls.append((args, kwargs))
        return {}

    def unexpected(*args, **kwargs):
        raise AssertionError("live analysis invoked")

    timing = {
        "AAA": SimpleNamespace(timing_score=0, timing_category="POOR", execution_priority="LOW",
                               momentum=None, timing_reason="no data", data_available=False),
        "BBB": SimpleNamespace(timing_score=62, timing_category="GOOD", execution_priority="NORMAL",
                               momentum=1.0, timing_reason="trend", data_available=True),
    }
    monkeypatch.setattr(main, "fetch_price_info", lambda symbol: {"current_price": 50.0})
    monkeypatch.setattr(main, "analyze_technical", unexpected)
    monkeypatch.setattr(main, "analyze_fundamental", unexpected)
    monkeypatch.setattr(main, "run_layered_optimizer", fake_optimizer)
    monkeypatch.setattr(factor_engine, "compute_portfolio_factor_exposure",
                        lambda *args, **kwargs: {"factor_exposures": {}})
    monkeypatch.setattr(regime_detector, "detect_regime", lambda db: {
        "regime": "SIDEWAYS", "confidence": .7, "transition_stability": "STABLE",
        "constraints": {"min_cash_pct": 5, "max_single_position_pct": 22, "turnover_multiplier": 1},
    })
    monkeypatch.setattr(optimizer_timing, "enrich_scores_with_timing",
                        lambda symbols: {s: t for s, t in timing.items() if s in symbols})
    monkeypatch.setattr(execution_instrument_facts, "resolve_execution_instruments", lambda *args: {})
    monkeypatch.setattr(snapshot_writer, "write_recommendation_snapshot",
                        lambda *args, **kwargs: snapshots.append(kwargs["scores_map"]))

    class FrozenDateTime(datetime):
        @classmethod
        def utcnow(cls):
            return cls(2026, 11, 1, 0, 0, 0)

        @classmethod
        def now(cls, tz=None):
            return cls(2026, 11, 1, 0, 0, 0).replace(tzinfo=tz or timezone.utc)

    monkeypatch.setattr(main, "datetime", FrozenDateTime)
    monkeypatch.setattr(calibration, "compute_calibration", lambda *args, **kwargs: {})

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    ws = main._ws_id(db)
    portfolio = Portfolio(workspace_id=ws, name="P", cash_balance=1000)
    db.add(portfolio)
    db.flush()
    db.add(PortfolioItem(workspace_id=ws, portfolio_id=portfolio.id, symbol="AAA", shares=10, avg_cost=50))
    db.add(Watchlist(workspace_id=ws, symbol="BBB", sector="Other"))
    cached = datetime(2026, 11, 1)
    # AAA: observed signal, genuine TA 0, failed FA.  BBB: no analysis signal,
    # TA result without a score, observed FA.
    db.add(AnalysisCache(workspace_id=ws, symbol="AAA", signal="ACCUMULATE", confidence="MEDIUM",
                         reasoning="r", risks="[]", analyzed_at=datetime(2026, 10, 30, 8, 0, 0)))
    db.add(AgentCache(symbol="AAA", agent="technical", cached_at=cached,
                      result_json=json.dumps({"ta_score": 0, "trend": "down"})))
    db.add(AgentCache(symbol="AAA", agent="fundamental", cached_at=cached,
                      result_json=json.dumps({"error": "provider failed"})))
    db.add(AgentCache(symbol="BBB", agent="technical", cached_at=cached,
                      result_json=json.dumps({"trend": "sideways"})))
    db.add(AgentCache(symbol="BBB", agent="fundamental", cached_at=cached,
                      result_json=json.dumps({"fa_score": 55, "pe_ratio": 10.5, "roe": 0.18})))
    db.commit()
    request = main.OptimizerRequest(portfolio_id=portfolio.id,
                                    **({"strategy_selection_mode": SELECTION_VERSION} if opt_in else {}))
    asyncio.run(main.analyze_optimizer(request, db))
    assert len(calls) == 1 and len(snapshots) == 1
    args, kwargs = calls[0]
    return args, kwargs, snapshots[0]


@pytest.mark.parametrize("opt_in", [False, True], ids=["optin_off", "optin_on"])
def test_baseline_endpoint_scores_map_arguments_and_snapshot_unchanged(monkeypatch, opt_in):
    args, kwargs, snapshot_scores = _endpoint_capture(monkeypatch, opt_in=opt_in)
    provenance = kwargs.pop("evidence_provenance", None)
    observed = {
        "args": _canonical(args),
        "kwargs": _canonical({k: v for k, v in kwargs.items()}),
        "snapshot_scores_map": _canonical(snapshot_scores),
    }
    baseline = _golden(f"endpoint:{'optin_on' if opt_in else 'optin_off'}", observed)
    # Same portfolio/watchlist rows (scores map), same other arguments, same snapshot input.
    assert observed["args"] == baseline["args"]
    assert observed["kwargs"] == baseline["kwargs"]
    assert observed["snapshot_scores_map"] == baseline["snapshot_scores_map"]
    if REGENERATE:
        return
    if not opt_in:
        assert provenance is None  # never passed when the Committee is off
        return
    assert provenance == {
        "AAA": {"signal": {"status": "OBSERVED", "source": "ANALYSIS_CACHE",
                           "as_of": "2026-10-30T08:00:00"},
                "ta_score": {"status": "OBSERVED", "source": "AGENT_CACHE"},
                "fa_score": {"status": "FAILED", "source": "AGENT_CACHE"},
                "timing_score": {"status": "MISSING", "source": "TIMING_INTELLIGENCE"}},
        "BBB": {"signal": {"status": "MISSING", "source": "ANALYSIS_CACHE"},
                "ta_score": {"status": "MISSING", "source": "AGENT_CACHE"},
                "fa_score": {"status": "OBSERVED", "source": "AGENT_CACHE"},
                "timing_score": {"status": "OBSERVED", "source": "TIMING_INTELLIGENCE"}},
    }
    # The defaulted row values are still there for the legacy consumers…
    portfolio_row = args[0][0]
    assert portfolio_row["fa_score"] == 0 and portfolio_row["signal"] == "ACCUMULATE"
    # …and the catalog built from them with provenance excludes them.
    envelope = prepare_candidates(list(args[0]), list(args[1]), 1000, {}, provenance=provenance)
    catalog = envelope["observed_evidence_catalog"]
    assert catalog["symbol:AAA:ta_score"] == 0  # genuine observed zero retained
    assert catalog["symbol:AAA:signal"] == "ACCUMULATE"
    for ref in ("symbol:AAA:fa_score", "symbol:AAA:timing_score", "symbol:BBB:signal",
                "symbol:BBB:ta_score"):
        assert ref not in catalog
        assert ref in envelope["unobserved_evidence"]
    assert catalog["symbol:BBB:timing_score"] == 62
    assert envelope["observed_evidence_as_of"] == {"symbol:AAA:signal": "2026-10-30T08:00:00"}


# ── Provenance helpers ───────────────────────────────────────────────────────

def test_analysis_provenance_distinguishes_observed_missing_failed_disabled():
    from services.optimizer.evidence_provenance import analysis_provenance
    assert analysis_provenance({"ta_score": 0}, "ta_score", enabled=True, source="LIVE") == \
        {"status": "OBSERVED", "source": "LIVE"}
    assert analysis_provenance({"error": "x"}, "ta_score", enabled=True, source="LIVE")["status"] == "FAILED"
    assert analysis_provenance(None, "ta_score", enabled=True, source="LIVE")["status"] == "MISSING"
    assert analysis_provenance({}, "ta_score", enabled=True, source="LIVE")["status"] == "MISSING"
    assert analysis_provenance({"trend": "up"}, "ta_score", enabled=True, source="LIVE")["status"] == "MISSING"
    assert analysis_provenance({"ta_score": None}, "ta_score", enabled=True, source="LIVE")["status"] == "MISSING"
    assert analysis_provenance({"ta_score": float("nan")}, "ta_score", enabled=True,
                               source="LIVE")["status"] == "MISSING"
    assert analysis_provenance({"ta_score": 50}, "ta_score", enabled=False, source="LIVE") == {"status": "DISABLED"}


def test_signal_and_timing_provenance():
    from services.optimizer.evidence_provenance import signal_provenance, timing_provenance
    row = SimpleNamespace(signal="WATCH", analyzed_at=datetime(2026, 1, 2, 3, 4, 5))
    assert signal_provenance(row) == {"status": "OBSERVED", "source": "ANALYSIS_CACHE",
                                      "as_of": "2026-01-02T03:04:05"}
    assert signal_provenance(None) == {"status": "MISSING", "source": "ANALYSIS_CACHE"}
    assert signal_provenance(SimpleNamespace(signal="MAYBE", analyzed_at=None))["status"] == "FAILED"
    assert timing_provenance(SimpleNamespace(data_available=True))["status"] == "OBSERVED"
    assert timing_provenance(SimpleNamespace(data_available=False))["status"] == "MISSING"
    assert timing_provenance(None)["status"] == "MISSING"


# ── Evidence catalog ─────────────────────────────────────────────────────────

def _envelope(plan=None, provenance=PROVENANCE, holdings=HOLDINGS, watchlist=WATCHLIST):
    return prepare_candidates([dict(r) for r in holdings], [dict(r) for r in watchlist], 200,
                              plan or {}, regime=REGIME, provenance=provenance)


def test_catalog_excludes_unobserved_and_records_them():
    envelope = _envelope()
    catalog = envelope["observed_evidence_catalog"]
    assert envelope["evidence_provenance_status"] == "SUPPLIED"
    # Missing analysis signal (row says HOLD by default) is not a fact.
    assert "symbol:BBB:signal" not in catalog and "symbol:ZZZ:signal" not in catalog
    # Failed FA and disabled TA are not facts.
    assert "symbol:BBB:fa_score" not in catalog and "symbol:WWW:ta_score" not in catalog
    # Timing without data is not a fact; timing with data is.
    assert "symbol:AAA:timing_score" not in catalog and "symbol:WWW:timing_score" not in catalog
    assert catalog["symbol:BBB:timing_score"] == 62
    # Genuine observed zero is retained.
    assert catalog["symbol:AAA:ta_score"] == 0
    # Observed signals and unconditional valuation facts are kept verbatim.
    assert catalog["symbol:AAA:signal"] == "SELL" and catalog["symbol:WWW:signal"] == "BUY"
    assert catalog["symbol:BBB:pe_ratio"] == 12 and catalog["symbol:BBB:roe"] == 0.2
    assert envelope["unobserved_evidence"] == {
        "symbol:AAA:timing_score": "MISSING", "symbol:BBB:fa_score": "FAILED",
        "symbol:BBB:signal": "MISSING", "symbol:WWW:ta_score": "DISABLED",
        "symbol:WWW:timing_score": "MISSING", "symbol:ZZZ:fa_score": "MISSING",
        "symbol:ZZZ:signal": "MISSING", "symbol:ZZZ:ta_score": "MISSING",
    }
    assert envelope["observed_evidence_as_of"] == {
        "symbol:AAA:signal": "2026-11-01T00:00:00", "symbol:WWW:signal": "2026-11-02T00:00:00"}
    assert not set(catalog) & set(envelope["unobserved_evidence"])


def test_symbol_without_provenance_record_is_unrecorded_not_observed():
    envelope = _envelope(provenance={"AAA": PROVENANCE["AAA"]})
    assert "symbol:BBB:ta_score" not in envelope["observed_evidence_catalog"]
    assert envelope["unobserved_evidence"]["symbol:BBB:ta_score"] == "UNRECORDED"


def test_not_supplied_keeps_legacy_catalog_and_says_so():
    legacy = prepare_candidates([dict(r) for r in HOLDINGS], [dict(r) for r in WATCHLIST], 200, {},
                                regime=REGIME)
    assert legacy["evidence_provenance_status"] == "NOT_SUPPLIED"
    assert "unobserved_evidence" not in legacy and "observed_evidence_as_of" not in legacy
    catalog = legacy["observed_evidence_catalog"]
    # Exactly today's behaviour: defaulted values remain (not provenance-verified).
    assert catalog["symbol:BBB:signal"] == "HOLD" and catalog["symbol:BBB:fa_score"] == 0
    assert catalog == sc._evidence_catalog(HOLDINGS, WATCHLIST, REGIME, None)


def test_citing_unobserved_evidence_stays_unverified():
    plan = {"strategy_family": "GROWTH_ROTATION", "target_cash_weight": 18,
            "observed_evidence_refs": ["symbol:BBB:signal", "symbol:BBB:fa_score"],
            "target_allocations": [
                {"symbol": "AAA", "action": "HOLD", "current_weight": 60, "target_weight": 60,
                 "allocation_change_percent": 0},
                {"symbol": "BBB", "action": "BUY", "current_weight": 20, "target_weight": 22,
                 "allocation_change_percent": 2}]}
    candidate = _envelope(plan)["candidates"][1]
    assert candidate["observed_evidence_refs"] == {}
    assert candidate["eligibility_status"] == "UNVERIFIED"
    assert "UNKNOWN_EVIDENCE_REF" in candidate["missing_information"]
    assert "BUY_SUPPORT_UNVERIFIED:BBB" in candidate["missing_information"]


def test_auditor_cannot_cite_unobserved_evidence():
    envelope = _envelope()
    review = [{"candidate_id": "hold-current", "supporting_refs": [],
               "opposing_refs": ["symbol:BBB:fa_score"]}]
    assert validate_candidate_reviews({"candidate_reviews": review}, envelope)["reason"] == \
        "UNKNOWN_AUDITOR_REFERENCE"


# ── BUY direction verification (D1 option B) ─────────────────────────────────

def _buy_plan(symbol, refs, *, family="GROWTH_ROTATION"):
    rows = [{"symbol": "AAA", "action": "HOLD", "current_weight": 60, "target_weight": 60,
             "allocation_change_percent": 0},
            {"symbol": "BBB", "action": "HOLD", "current_weight": 20, "target_weight": 20,
             "allocation_change_percent": 0}]
    for row in rows:
        if row["symbol"] == symbol:
            row.update(action="BUY", target_weight=row["current_weight"] + 2, allocation_change_percent=2)
    return {"strategy_family": family, "target_cash_weight": 18, "observed_evidence_refs": refs,
            "target_allocations": rows}


def _with_signal(symbol, signal):
    holdings = [dict(row, signal=signal) if row["symbol"] == symbol else dict(row) for row in HOLDINGS]
    provenance = {**PROVENANCE, symbol: {**PROVENANCE[symbol], "signal": {"status": "OBSERVED"}}}
    return holdings, provenance


def _buy_candidate(symbol, refs, signal):
    holdings, provenance = _with_signal(symbol, signal)
    return _envelope(_buy_plan(symbol, refs), provenance=provenance, holdings=holdings)["candidates"][1]


@pytest.mark.parametrize("signal", ["HOLD", "WATCH"])
def test_hold_or_watch_signal_alone_cannot_verify_buy(signal):
    candidate = _buy_candidate("BBB", ["symbol:BBB:signal", "regime:regime"], signal)
    assert candidate["observed_evidence_refs"]["symbol:BBB:signal"] == signal
    assert "BUY_SUPPORT_UNVERIFIED:BBB" in candidate["missing_information"]
    assert candidate["eligibility_status"] == "UNVERIFIED"


@pytest.mark.parametrize("signal", ["SELL", "REDUCE"])
@pytest.mark.parametrize("refs", [["symbol:BBB:pe_ratio"], ["symbol:BBB:roe"],
                                  ["symbol:BBB:pe_ratio", "symbol:BBB:roe", "symbol:BBB:signal"]])
def test_observed_sell_or_reduce_contradicts_buy_regardless_of_valuation(signal, refs):
    candidate = _buy_candidate("BBB", refs, signal)
    assert "BUY_CONTRADICTS_SIGNAL:BBB" in candidate["missing_information"]
    assert candidate["eligibility_status"] == "UNVERIFIED"


def test_contradiction_applies_even_when_signal_is_not_cited():
    candidate = _buy_candidate("BBB", ["symbol:BBB:pe_ratio"], "SELL")
    assert "symbol:BBB:signal" not in candidate["observed_evidence_refs"]
    assert "BUY_CONTRADICTS_SIGNAL:BBB" in candidate["missing_information"]


@pytest.mark.parametrize("signal", ["ACCUMULATE", "BUY"])
def test_observed_buy_direction_signal_verifies_buy(signal):
    candidate = _buy_candidate("BBB", ["symbol:BBB:signal"], signal)
    assert candidate["missing_information"] == []
    assert candidate["eligibility_status"] == "ELIGIBLE"


@pytest.mark.parametrize("refs", [["symbol:BBB:pe_ratio"], ["symbol:BBB:roe"]])
def test_valuation_support_remains_admissible_without_contradiction(refs):
    # Observed HOLD signal is not a contradiction; P/E or ROE still supports.
    candidate = _buy_candidate("BBB", refs, "HOLD")
    assert candidate["eligibility_status"] == "ELIGIBLE"
    # Missing signal (row default HOLD, provenance MISSING) is not a contradiction either.
    candidate = _envelope(_buy_plan("BBB", refs))["candidates"][1]
    assert candidate["eligibility_status"] == "ELIGIBLE"


def test_buy_with_only_model_scores_still_unverified():
    candidate = _buy_candidate("BBB", ["symbol:BBB:ta_score", "symbol:BBB:timing_score"], "ACCUMULATE")
    assert "BUY_SUPPORT_UNVERIFIED:BBB" in candidate["missing_information"]
    assert "MODEL_SCORE_ONLY_SUPPORT" in candidate["missing_information"]


def test_not_supplied_buy_rule_is_unchanged():
    plan = _buy_plan("BBB", ["symbol:BBB:signal"])
    holdings, _ = _with_signal("BBB", "SELL")
    legacy = prepare_candidates(holdings, [], 200, plan)["candidates"][1]
    # Legacy behaviour (non-score ref for the symbol suffices) is retained.
    assert legacy["eligibility_status"] == "ELIGIBLE"


# ── SELL / REDUCE rules unchanged; missing signal disclosed ──────────────────

def _sell_plan(symbol, action="SELL"):
    rows = [{"symbol": "AAA", "action": "HOLD", "current_weight": 60, "target_weight": 60,
             "allocation_change_percent": 0},
            {"symbol": "BBB", "action": "HOLD", "current_weight": 20, "target_weight": 20,
             "allocation_change_percent": 0}]
    for row in rows:
        if row["symbol"] == symbol:
            row.update(action=action, target_weight=row["current_weight"] - 10, allocation_change_percent=-10)
    return {"strategy_family": "RAISE_CASH", "target_cash_weight": 30,
            "observed_evidence_refs": [f"symbol:{symbol}:signal", "symbol:BBB:pe_ratio"],
            "target_allocations": rows}


def test_sale_on_observed_sell_signal_still_verified():
    candidate = _envelope(_sell_plan("AAA"))["candidates"][1]
    assert candidate["eligibility_status"] == "ELIGIBLE"


def test_sale_on_unobserved_signal_records_both_markers():
    candidate = _envelope(_sell_plan("BBB"))["candidates"][1]
    assert "UNVERIFIED_SELL:BBB" in candidate["missing_information"]
    assert "SIGNAL_UNOBSERVED:BBB" in candidate["missing_information"]
    assert candidate["eligibility_status"] == "UNVERIFIED"


def test_reduce_rule_unchanged_with_observed_reduce_signal():
    holdings, provenance = _with_signal("BBB", "REDUCE")
    plan = _sell_plan("BBB", action="REDUCE")
    supplied = _envelope(plan, provenance=provenance, holdings=holdings)["candidates"][1]
    legacy = prepare_candidates(holdings, WATCHLIST, 200, plan, regime=REGIME)["candidates"][1]
    # A REDUCE signal still does not verify a sale (later, separately approved slice).
    assert "UNVERIFIED_SELL:BBB" in supplied["missing_information"]
    assert "SIGNAL_UNOBSERVED:BBB" not in supplied["missing_information"]
    assert supplied["eligibility_status"] == legacy["eligibility_status"] == "UNVERIFIED"


# ── Auditor compact view ─────────────────────────────────────────────────────

def test_compact_view_discloses_relevant_unobserved_evidence():
    envelope = _envelope(_buy_plan("BBB", ["symbol:BBB:pe_ratio"]))
    view = sc.candidate_review_view(envelope)
    assert view["evidence_provenance_status"] == "SUPPLIED"
    # Touched symbols AAA, BBB: their missing analysis travels with the view.
    assert view["unobserved_evidence"] == {
        "symbol:AAA:timing_score": "MISSING", "symbol:BBB:fa_score": "FAILED",
        "symbol:BBB:signal": "MISSING"}
    # Unrelated symbols' gaps are omitted and counted.
    assert view["omitted_unrelated_unobserved_count"] == 5
    assert not set(view["unobserved_evidence"]) & set(view["relevant_evidence"])


def test_compact_view_not_supplied_status():
    view = sc.candidate_review_view(prepare_candidates(HOLDINGS, [], 200, {}))
    assert view["evidence_provenance_status"] == "NOT_SUPPLIED"
    assert "unobserved_evidence" not in view


# ── Production opt-in plumbing (primary and fallback) ────────────────────────

def _reviews(prompt):
    import re
    ids = re.findall(r'"candidate_id": "([^"]+)"', prompt)
    return {"risk_flags": [], "candidate_reviews": [
        {"candidate_id": cid, "supporting_refs": [], "opposing_refs": [],
         "material_conflicts": [], "assessment": "Model view"} for cid in ids]}


def test_optin_primary_path_uses_supplied_provenance(monkeypatch):
    result, captured = _run(monkeypatch, layer3_reply=_reviews, regime_context=REGIME,
                            evidence_provenance=PROVENANCE, **OPT_IN)
    envelope = result["strategic_candidates"]
    assert envelope["evidence_provenance_status"] == "SUPPLIED"
    assert "symbol:BBB:signal" not in envelope["observed_evidence_catalog"]
    prompt = captured["layer3"]["prompt"]
    assert '"unobserved_evidence": {' in prompt
    assert '"symbol:BBB:fa_score": "FAILED"' in prompt
    assert "unobserved_evidence" in prompt[:prompt.index("CANDIDATES_FOR_REVIEW=")]


def test_optin_without_provenance_records_not_supplied(monkeypatch):
    result, _ = _run(monkeypatch, layer3_reply=_reviews, regime_context=REGIME, **OPT_IN)
    assert result["strategic_candidates"]["evidence_provenance_status"] == "NOT_SUPPLIED"


def test_optin_fallback_path_uses_supplied_provenance(monkeypatch):
    real = optimizer.freeze_concentration
    state = {"raised": False}

    def fail_primary_once(*args, **kwargs):
        if not state["raised"]:
            state["raised"] = True
            raise RuntimeError("primary pipeline failure")
        return real(*args, **kwargs)

    monkeypatch.setattr(optimizer, "freeze_concentration", fail_primary_once)
    result, captured = _run(monkeypatch, evidence_provenance=PROVENANCE, **OPT_IN)
    assert "fallback" in captured and state["raised"]
    envelope = result["strategic_candidates"]
    assert {c["source_layer"] for c in envelope["candidates"]} <= {"FROZEN_PORTFOLIO", "SINGLE_SHOT_FALLBACK"}
    assert envelope["evidence_provenance_status"] == "SUPPLIED"
    assert "symbol:BBB:signal" not in envelope["observed_evidence_catalog"]
    assert result["candidate_audit"]["reason"] == "AUDITOR_UNAVAILABLE_IN_FALLBACK"
