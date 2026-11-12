"""MUJI V2 Phase 4 Slice 4.3B — execution penalty no longer rewrites combined_score.

``combined_score`` is the raw ``0.4 * ta_score + 0.6 * fa_score`` (about
-5.2..+7.0). The removed ``apply_execution_score_penalties`` wrote
``max(5.0, combined - penalty)`` into it; with penalties of 4/8/14 that is
always exactly 5.0, so every penalised DR was raised to 5.0 and ranked above
every ordinary stock. The execution context (classification, caps, warnings,
slippage, informational ``combined_score_penalty``) is unchanged.

``fixtures/dr_execution_score_frozen.json`` is a read-only export of histories
247-249: the stored (distorted) scores map, the stored execution context and
the Registry facts reason needed to replay classification exactly.
"""
import asyncio
import copy
import json
import os
import re
import sys
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import agents.optimizer as optimizer
from services.execution_instrument_facts import (
    ExecutionInstrumentFacts,
    ExecutionInstrumentForm,
    ExecutionResolutionOutcome,
    ExecutionRole,
)
from services.optimizer import execution_penalty
from services.optimizer.execution_penalty import (
    build_execution_prompt_block,
    compute_portfolio_execution_context,
)
from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY
from services.optimizer.strategic_candidates import SELECTION_VERSION

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "dr_execution_score_frozen.json")
RUNS = ("247", "248", "249")
MODES = {
    "legacy": {},
    "sector_advisory_v1": {"sector_policy_mode": SECTOR_POLICY_ADVISORY},
    "muji_v2": {"sector_policy_mode": SECTOR_POLICY_ADVISORY,
                "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2},
    "muji_v2_committee": {"sector_policy_mode": SECTOR_POLICY_ADVISORY,
                          "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2,
                          "strategy_selection_mode": SELECTION_VERSION},
}
SCORE_RE = re.compile(r'"combined_score": (-?\d+(?:\.\d+)?)')


def _raw(row):
    """Canonical combined score (main.py, TA and FA both enabled)."""
    return round(0.4 * row["ta_score"] + 0.6 * row["fa_score"], 1)


def _removed_floor(scores_map, execution_ctx):
    """The removed apply_execution_score_penalties, kept only as the 'before' reference."""
    for sym, meta in execution_ctx.get("per_symbol", {}).items():
        penalty = float(meta.get("combined_score_penalty", 0.0))
        if penalty > 0 and sym in scores_map:
            original = float(scores_map[sym].get("combined_score", 0))
            scores_map[sym]["combined_score"] = round(max(5.0, original - penalty), 1)
            scores_map[sym]["execution_penalized"] = True


def _fixture():
    with open(FIXTURE, encoding="utf-8") as fh:
        return json.load(fh)


def _frozen_facts(run):
    return {
        sym: ExecutionInstrumentFacts(
            query=sym,
            resolution_status=ExecutionResolutionOutcome(meta["resolution_status"]),
            instrument_form=ExecutionInstrumentForm(meta["instrument_form"]),
            execution_role=ExecutionRole(meta["execution_role"]),
            reason=run["facts_reason"].get(sym),
        )
        for sym, meta in run["stored_execution_context"]["per_symbol"].items()
    }


def _raw_scores_map(run):
    """Frozen scores map as main.py now builds it: raw combined, no penalty marker."""
    out = {}
    for sym, row in run["stored_scores"].items():
        row = {k: v for k, v in row.items() if k != "execution_penalized"}
        out[sym] = {**row, "symbol": sym, "combined_score": _raw(row)}
    return out


def _dr_facts(sym):
    return ExecutionInstrumentFacts(
        query=sym, resolution_status=ExecutionResolutionOutcome.RESOLVED,
        instrument_form=ExecutionInstrumentForm.DEPOSITARY_RECEIPT, execution_role=ExecutionRole.TRADABLE)


def _equity_facts(sym):
    return ExecutionInstrumentFacts(
        query=sym, resolution_status=ExecutionResolutionOutcome.RESOLVED,
        instrument_form=ExecutionInstrumentForm.EQUITY, execution_role=ExecutionRole.TRADABLE)


# ── A. Score correctness at the main.py boundary ──────────────────────────────

# symbol -> (ta, fa, raw combined, is DR). Real agent ranges; values from run 249.
BOUNDARY = {
    "CATL01.BK":  (1, 7, 4.6, True),
    "GOOGL01.BK": (0, 6, 3.6, True),
    "GOLDM01.BK": (1, 0, 0.4, True),
    "TSLA01.BK":  (2, -1, 0.2, True),
    "PTTEP.BK":   (0, 6, 3.6, False),
    "BGRIM.BK":   (-1, -2, -1.6, False),
}
HELD = ("GOOGL01.BK", "PTTEP.BK")


def _endpoint_capture(monkeypatch):
    """Run main.analyze_optimizer in memory; capture every score hand-off.

    No model calls, no live analysis, no real database: an in-memory SQLite
    session, and signal-history rows are intercepted before they are added.
    """
    import main
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import models.asset  # noqa: F401
    import models.registry_finding  # noqa: F401
    from models.database import (AgentCache, AnalysisCache, Base, Portfolio, PortfolioItem,
                                 SignalHistory, Watchlist)
    from services.analytics import factor_engine, regime_detector
    from services import execution_instrument_facts, optimizer_timing
    from services.decision_memory import calibration, snapshot_writer

    calls, snapshots, signal_rows = [], [], []

    def fake_optimizer(*args, **kwargs):
        calls.append((args, kwargs))
        rows = []
        for sym in HELD:
            action = "REDUCE" if sym == "GOOGL01.BK" else "HOLD"
            rows.append({"symbol": sym, "action": action, "current_weight": 10.0,
                         "target_weight": 8.0 if action == "REDUCE" else 10.0,
                         "allocation_change_percent": -2.0 if action == "REDUCE" else 0.0,
                         "estimated_amount": 0, "reason": "test"})
        rows.append({"symbol": "CATL01.BK", "action": "ACCUMULATE", "current_weight": 0.0,
                     "target_weight": 2.0, "allocation_change_percent": 2.0,
                     "estimated_amount": 0, "reason": "test"})
        return {"target_allocations": rows}

    def unexpected(*args, **kwargs):
        raise AssertionError("live analysis invoked")

    def facts(_db, symbols):
        return {s: (_dr_facts(s) if BOUNDARY[s][3] else _equity_facts(s)) for s in symbols}

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
    monkeypatch.setattr(optimizer_timing, "enrich_scores_with_timing", lambda symbols: {})
    monkeypatch.setattr(execution_instrument_facts, "resolve_execution_instruments", facts)
    monkeypatch.setattr(snapshot_writer, "write_recommendation_snapshot",
                        lambda *args, **kwargs: snapshots.append(copy.deepcopy(kwargs["scores_map"])))
    monkeypatch.setattr(calibration, "compute_calibration", lambda *args, **kwargs: {})

    class FrozenDateTime(datetime):
        @classmethod
        def utcnow(cls):
            return cls(2026, 11, 12, 0, 0, 0)

        @classmethod
        def now(cls, tz=None):
            return cls(2026, 11, 12, 0, 0, 0).replace(tzinfo=tz or timezone.utc)

    monkeypatch.setattr(main, "datetime", FrozenDateTime)

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    real_add_all = db.add_all

    def add_all(objs):
        objs = list(objs)
        signal_rows.extend(o for o in objs if isinstance(o, SignalHistory))
        real_add_all([o for o in objs if not isinstance(o, SignalHistory)])

    db.add_all = add_all
    ws = main._ws_id(db)
    portfolio = Portfolio(workspace_id=ws, name="P", cash_balance=1000)
    db.add(portfolio)
    db.flush()
    cached = datetime(2026, 11, 12)
    for sym, (ta, fa, _, _) in BOUNDARY.items():
        if sym in HELD:
            db.add(PortfolioItem(workspace_id=ws, portfolio_id=portfolio.id, symbol=sym, shares=10, avg_cost=50))
        else:
            db.add(Watchlist(workspace_id=ws, symbol=sym, sector="Other"))
        db.add(AnalysisCache(workspace_id=ws, symbol=sym, signal="ACCUMULATE", confidence="MEDIUM",
                             reasoning="r", risks="[]", analyzed_at=cached))
        db.add(AgentCache(symbol=sym, agent="technical", cached_at=cached,
                          result_json=json.dumps({"ta_score": ta, "trend": "sideways"})))
        db.add(AgentCache(symbol=sym, agent="fundamental", cached_at=cached,
                          result_json=json.dumps({"fa_score": fa})))
    db.commit()
    asyncio.run(main.analyze_optimizer(main.OptimizerRequest(portfolio_id=portfolio.id), db))
    assert len(calls) == 1 and len(snapshots) == 1
    args, _kwargs = calls[0]
    return {"portfolio_data": args[0], "watchlist_data": args[1], "execution_ctx": args[16],
            "snapshot_scores": snapshots[0], "signal_rows": signal_rows}


@pytest.fixture
def boundary(monkeypatch):
    return _endpoint_capture(monkeypatch)


def test_dr_and_non_dr_scores_reach_the_optimizer_raw(boundary):
    rows = {r["symbol"]: r for r in boundary["portfolio_data"] + boundary["watchlist_data"]}
    assert set(rows) == set(BOUNDARY)
    for sym, (ta, fa, raw, _) in BOUNDARY.items():
        assert rows[sym]["combined_score"] == raw == round(0.4 * ta + 0.6 * fa, 1), sym
        assert "execution_penalized" not in rows[sym], sym
    # The defect: every penalised DR would have read 5.0.
    distorted = copy.deepcopy(boundary["snapshot_scores"])
    _removed_floor(distorted, boundary["execution_ctx"])
    assert {s for s, v in distorted.items() if v["combined_score"] == 5.0} == {
        s for s, v in BOUNDARY.items() if v[3]}


def test_no_score_increases_because_of_an_execution_penalty(boundary):
    per_symbol = boundary["execution_ctx"]["per_symbol"]
    penalised = {s for s, m in per_symbol.items() if m["combined_score_penalty"] > 0}
    assert penalised == {s for s, v in BOUNDARY.items() if v[3]}
    for sym, row in boundary["snapshot_scores"].items():
        assert row["combined_score"] == BOUNDARY[sym][2], sym


def test_penalty_estimate_stays_informational_in_execution_context(boundary):
    ctx = boundary["execution_ctx"]
    assert ctx["dr_symbols"] == [s for s in ctx["per_symbol"] if BOUNDARY[s][3]]
    for sym, meta in ctx["per_symbol"].items():
        if BOUNDARY[sym][3]:
            assert (meta["asset_type"], meta["execution_risk"], meta["combined_score_penalty"],
                    meta["position_cap_pct"], meta["slippage_cost_est_pct"]) == ("DR", "MEDIUM", 4.0, 15.0, 0.5)
            assert "DR - Execution Sensitive" in meta["execution_warnings"]
        else:
            assert (meta["asset_type"], meta["combined_score_penalty"], meta["position_cap_pct"]) == (
                "EQUITY", 0.0, None)
    canonical = ctx["canonical_instrument_context"]
    held_dr = next(p for p in canonical["positions"] if p["held_symbol"] == "GOOGL01.BK")
    assert held_dr["execution"]["combined_score_penalty"] == 4.0  # JSON contract kept


def test_snapshot_and_signal_history_construction_use_raw_scores(boundary):
    assert {s: v["combined_score"] for s, v in boundary["snapshot_scores"].items()} == {
        s: v[2] for s, v in BOUNDARY.items()}
    assert not any("execution_penalized" in v for v in boundary["snapshot_scores"].values())
    rows = {r.symbol: r for r in boundary["signal_rows"]}
    assert set(rows) == {"GOOGL01.BK", "CATL01.BK"}  # HOLD rows are not recorded
    assert rows["GOOGL01.BK"].score_at_signal == 3.6  # previously 5.0
    assert rows["CATL01.BK"].score_at_signal == 4.6
    assert (rows["GOOGL01.BK"].ta_score, rows["GOOGL01.BK"].fa_score) == (0, 6)


def test_execution_context_computation_never_mutates_scores():
    scores = {s: {"symbol": s, "is_dr": v[3], "combined_score": v[2], "current_price": 50.0}
              for s, v in BOUNDARY.items()}
    before = copy.deepcopy(scores)
    compute_portfolio_execution_context(scores, facts_by_symbol={
        s: (_dr_facts(s) if v[3] else _equity_facts(s)) for s, v in BOUNDARY.items()})
    assert scores == before
    assert not hasattr(execution_penalty, "apply_execution_score_penalties")


# ── B. Frozen histories 247-249 ───────────────────────────────────────────────

@pytest.mark.parametrize("run_id", RUNS)
def test_frozen_runs_previously_set_all_19_drs_to_5(run_id):
    run = _fixture()["runs"][run_id]
    stored = run["stored_scores"]
    penalised = {s for s, v in stored.items() if v.get("execution_penalized")}
    assert len(penalised) == 19
    assert {stored[s]["combined_score"] for s in penalised} == {5.0}
    assert all(_raw(stored[s]) < 5.0 for s in penalised)  # every one was raised
    assert all(stored[s]["combined_score"] == _raw(stored[s]) for s in stored if s not in penalised)
    # The removed function reproduces the stored values from the raw scores.
    replay = _raw_scores_map(run)
    _removed_floor(replay, run["stored_execution_context"])
    assert {s: v["combined_score"] for s, v in replay.items()} == {
        s: v["combined_score"] for s, v in stored.items()}


@pytest.mark.parametrize("run_id", RUNS)
def test_frozen_runs_now_keep_raw_scores_and_identical_execution_context(run_id):
    run = _fixture()["runs"][run_id]
    scores = _raw_scores_map(run)
    before = copy.deepcopy(scores)
    ctx = compute_portfolio_execution_context(scores, facts_by_symbol=_frozen_facts(run))
    assert ctx == run["stored_execution_context"]  # classification, caps, warnings, slippage
    assert build_execution_prompt_block(ctx) == build_execution_prompt_block(run["stored_execution_context"])
    assert scores == before


def test_frozen_run_249_before_and_after_scores():
    stored = _fixture()["runs"]["249"]["stored_scores"]
    expected_raw = {"CATL01.BK": 4.6, "MICRON01.BK": 4.2, "NVDA01.BK": 4.0, "GOOGL01.BK": 3.6,
                    "GOLDM01.BK": 0.4, "TSLA01.BK": 0.2, "NBIS01.BK": 0.6}
    for sym, raw in expected_raw.items():
        assert stored[sym]["combined_score"] == 5.0 and _raw(stored[sym]) == raw, sym
    ranked = sorted(stored, key=lambda s: -_raw(stored[s]))
    assert ranked[0] == "CATL01.BK"
    # Before: the 19 DRs occupied ranks 1-19. After: ordinary stocks interleave.
    assert any(not stored[s].get("execution_penalized") for s in ranked[:19])


def test_frozen_fixture_is_a_read_only_export():
    data = _fixture()
    assert set(data["runs"]) == set(RUNS)
    assert "read-only export" in data["source"]


# ── C/D. Prompts, finalization and deterministic stages ───────────────────────

def _frozen_249_inputs():
    run = _fixture()["runs"]["249"]
    scores = _raw_scores_map(run)
    nav, cash = 740_880.22, 238_280.22
    held = HELD_249
    ctx = compute_portfolio_execution_context(scores, facts_by_symbol=_frozen_facts(run))
    portfolio, watchlist = [], []
    for sym, row in scores.items():
        if sym in held:
            value = held[sym] / 100 * nav
            portfolio.append({**row, "sector": "Other", "allow_swap": True,
                              "shares": value / row["current_price"]})
        else:
            watchlist.append({**row, "sector": "Other"})
    return portfolio, watchlist, ctx, cash


def _distort(rows, ctx):
    rows = copy.deepcopy(rows)
    by_sym = {r["symbol"]: r for r in rows}
    _removed_floor(by_sym, ctx)
    return rows


HELD_249 = {"BH.BK": 20.73209619868616, "GOOGL01.BK": 7.8960132006714865, "GULF.BK": 17.006797662984745,
            "MICRON01.BK": 11.337865108656494, "NVDA01.BK": 10.865454062462474}
CANDIDATE_ID_RE = re.compile(r'"((?:proposal-[0-9a-f]{12})|hold-current)"')
GROWTH_REF = "symbol:CATL01.BK:signal"


def _run(monkeypatch, portfolio, watchlist, ctx, cash, mode, path):
    captured = {}
    committee = "strategy_selection_mode" in MODES[mode]

    def fake_ai(prompt, provider, model, *args, usage_layer, max_tokens=None, **kw):
        captured[usage_layer] = prompt
        if usage_layer in ("layer1", "layer1_retry"):
            payload = {"swaps": [], "top_buys": ["CATL01.BK"], "priority": "low"}
        elif usage_layer == "layer2" and committee:
            # Eligible actionable candidate: hold every position, add a DR.
            rows = [{"s": s, "tw": w, "sig": "HOLD"} for s, w in HELD_249.items()]
            payload = {"allocations": rows + [{"s": "CATL01.BK", "tw": 2.0, "sig": "ACCUMULATE"}],
                       "status": "REBALANCE", "cash_balance_target": 100 - sum(HELD_249.values()) - 2.0,
                       "strategy_family": "GROWTH_ROTATION", "observed_evidence_refs": [GROWTH_REF]}
        elif usage_layer == "layer2":
            payload = {"allocations": [
                {"s": "GOOGL01.BK", "tw": 6.0, "sig": "REDUCE"},
                {"s": "BH.BK", "tw": 20.73, "sig": "HOLD"},
                {"s": "GULF.BK", "tw": 17.01, "sig": "HOLD"},
                {"s": "MICRON01.BK", "tw": 11.34, "sig": "HOLD"},
                {"s": "NVDA01.BK", "tw": 10.87, "sig": "HOLD"},
                {"s": "CATL01.BK", "tw": 2.0, "sig": "ACCUMULATE"}],
                "status": "REBALANCE", "cash_balance_target": 31.0}
        elif usage_layer == "layer3":
            ids = sorted(set(CANDIDATE_ID_RE.findall(prompt)))
            payload = {"risk_flags": [], "safer_choice": "layer2", "final_risk_level": "medium",
                       "candidate_reviews": [
                           {"candidate_id": cid, "supporting_refs": [] if cid == "hold-current" else [GROWTH_REF],
                            "opposing_refs": [], "material_conflicts": [], "assessment": "reviewed"}
                           for cid in ids]}
        elif usage_layer == "committee":
            chosen = next(c for c in sorted(set(CANDIDATE_ID_RE.findall(prompt))) if c != "hold-current")
            payload = {"selected_candidate_id": chosen, "supporting_evidence_refs": [GROWTH_REF],
                       "opposing_evidence_refs": [], "comparison_against_hold": "adds observed ACCUMULATE",
                       "decision_rationale": "test", "material_uncertainty": []}
        else:
            payload = {"allocations": [{"s": "GOOGL01.BK", "tw": 6.0, "sig": "REDUCE"}],
                       "status": "REBALANCE", "cash_balance_target": 31.0, "risk_flags": []}
        return {"text": json.dumps(payload), "latency_ms": 1}

    monkeypatch.setattr(optimizer, "call_ai", fake_ai)
    if path == "fallback":
        real = optimizer._emit_stage

        def fail_first_stage(on_stage, stage):
            if stage == "LAYER1_PROPOSAL":
                raise RuntimeError("primary pipeline failure")
            return real(on_stage, stage)

        monkeypatch.setattr(optimizer, "_emit_stage", fail_first_stage)
    result = optimizer.run_layered_optimizer(
        copy.deepcopy(portfolio), copy.deepcopy(watchlist), "P", cash_balance=cash,
        execution_context=copy.deepcopy(ctx), **MODES[mode])
    return captured, result


# Challenger candidate ids hash the proposal rows, which carry combined_score;
# test_candidate_ids_differ_only_through_combined_score pins that dependency.
PROPOSAL_ID_RE = re.compile(r"proposal-[0-9a-f]{12}")


def _strip_scores(obj):
    if isinstance(obj, dict):
        return {_strip_scores(k): _strip_scores(v) for k, v in obj.items()
                if k != "combined_score" and not k.endswith("latency_ms")}
    if isinstance(obj, list):
        return [_strip_scores(v) for v in obj]
    if isinstance(obj, str):
        return PROPOSAL_ID_RE.sub("proposal-ID", obj)
    return obj


def _blank_scores(prompt):
    return PROPOSAL_ID_RE.sub("proposal-ID", SCORE_RE.sub('"combined_score": X', prompt))


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("path", ["primary", "fallback"])
def test_only_combined_scores_change_downstream(monkeypatch, mode, path):
    portfolio, watchlist, ctx, cash = _frozen_249_inputs()
    before_prompts, before = _run(monkeypatch, _distort(portfolio, ctx), _distort(watchlist, ctx),
                                  ctx, cash, mode, path)
    after_prompts, after = _run(monkeypatch, portfolio, watchlist, ctx, cash, mode, path)
    assert set(before_prompts) == set(after_prompts)
    for layer in after_prompts:
        assert _blank_scores(after_prompts[layer]) == _blank_scores(before_prompts[layer]), layer
    if path == "primary":
        assert after_prompts["layer1"] == before_prompts["layer1"]  # Strategist unchanged
    # Policy, consensus, candidates, selection, caps and scheduling: identical.
    assert _strip_scores(after) == _strip_scores(before)


def _expected_prompt_scores(portfolio, watchlist):
    return [r["combined_score"] for r in portfolio] + [r["combined_score"] for r in watchlist]


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("path,layer", [("primary", "layer2"), ("fallback", "fallback")])
def test_challenger_and_fallback_prompts_carry_raw_scores(monkeypatch, mode, path, layer):
    portfolio, watchlist, ctx, cash = _frozen_249_inputs()
    prompts, _ = _run(monkeypatch, portfolio, watchlist, ctx, cash, mode, path)
    values = [float(v) for v in SCORE_RE.findall(prompts[layer])]
    assert values == _expected_prompt_scores(portfolio, watchlist)
    assert 5.0 not in values  # no 249 instrument has a raw score of 5.0
    before, _ = _run(monkeypatch, _distort(portfolio, ctx), _distort(watchlist, ctx), ctx, cash, mode, path)
    assert sorted(float(v) for v in SCORE_RE.findall(before[layer])).count(5.0) == 19


@pytest.mark.parametrize("mode", MODES)
def test_target_allocation_and_watchlist_scores_are_raw(monkeypatch, mode):
    portfolio, watchlist, ctx, cash = _frozen_249_inputs()
    _, result = _run(monkeypatch, portfolio, watchlist, ctx, cash, mode, "primary")
    raw = {r["symbol"]: r["combined_score"] for r in portfolio + watchlist}
    rows = result["target_allocations"]
    assert rows and all(r["combined_score"] == raw[r["symbol"]] for r in rows)
    assert {r["symbol"]: r["combined_score"] for r in rows}["GOOGL01.BK"] == 3.6
    ranking = result["watchlist_ranking"]
    assert ranking and all(w["combined_score"] == raw[w["symbol"]] for w in ranking)
    assert next(w for w in ranking if w["symbol"] == "CATL01.BK")["combined_score"] == 4.6


def test_candidate_ids_differ_only_through_combined_score(monkeypatch):
    portfolio, watchlist, ctx, cash = _frozen_249_inputs()
    results = {}
    for tag, (p, w) in {"before": (_distort(portfolio, ctx), _distort(watchlist, ctx)),
                        "after": (portfolio, watchlist)}.items():
        _, result = _run(monkeypatch, p, w, ctx, cash, "muji_v2_committee", "primary")
        results[tag] = result
    proposals = {tag: next(c for c in r["strategic_candidates"]["candidates"] if c["id"] != "hold-current")
                 for tag, r in results.items()}
    assert proposals["before"]["id"] != proposals["after"]["id"]
    assert _strip_scores(proposals["before"]["proposed_allocations"]) == _strip_scores(
        proposals["after"]["proposed_allocations"])
    for tag, result in results.items():
        selection = result["strategy_selection"]
        assert selection["state"] == "SELECTED" and selection["reason_codes"] == ["COMMITTEE_SELECTED"]
        assert selection["selected_candidate_id"] == proposals[tag]["id"]
    catl = {tag: next(r for r in results[tag]["target_allocations"] if r["symbol"] == "CATL01.BK")
            for tag in results}
    assert (catl["before"]["combined_score"], catl["after"]["combined_score"]) == (5.0, 4.6)
