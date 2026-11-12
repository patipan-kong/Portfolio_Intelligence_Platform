"""MUJI V2 Phase 4 Slice 4.3A — no FA/TA score-based "low-quality" violation.

The Policy Engine used to flag every non-SELL/REDUCE holding above 4% as
"low-quality … should be suppressed" whenever suppress_speculative was on,
because it compared the agents' small signed FA/TA scores against 35. The
violation is removed; regime suppression guidance and every other violation
are unchanged.

The baseline fixture was captured from the unmodified Policy Engine at
71cbf19 (``capture_policy_suppression_baseline`` below documents how). For each
scenario it stores the baseline envelope and the expected envelope: the
baseline with only the false violations removed and the prompt block
re-rendered by the baseline renderer.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import agents.optimizer as optimizer
from agents.optimizer import _compute_portfolio_weights, _make_envelope_from_dict
from services.analytics.regime_detector import build_regime_prompt_block, get_regime_constraints
from services.optimizer import policy_engine
from services.optimizer.policy_engine import HardConstraints, _detect_violations
from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY
from services.optimizer.stabilization import STATUS_NO_REBALANCE, apply_stabilization
from services.optimizer.strategy_profiles import build_persona_context, compute_style_drift

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "policy_suppression_baseline.json")
# Exact wording of the removed violation. "SUPPRESS_SPECULATIVE: YES — avoid
# low-quality or high-beta positions" is legitimate regime guidance and stays.
FALSE_FLAG = " is low-quality (FA="
FALSE_FLAG_TAIL = "should be suppressed per current policy"
SUPPRESS_GUIDANCE = "SUPPRESS_SPECULATIVE:   YES — avoid low-quality or high-beta positions"
CASH = 30_000.0


def _holding(symbol, sector, value, signal, fa, ta):
    return {"symbol": symbol, "sector": sector, "shares": 100, "current_price": value / 100,
            "signal": signal, "fa_score": fa, "ta_score": ta, "allow_swap": True}


# Real agent ranges: FA −4..+7 (fundamental.py), TA about −5..+5 (technical.py).
HOLDINGS = {
    # NAV 100,000: 30% / 20% / 5% / 15% / cash 30%.
    "mixed": [
        _holding("HEALTHY", "Technology", 30_000, "ACCUMULATE", 7, 2),
        _holding("STEADY", "Healthcare", 20_000, "WATCH", 4, 0),
        _holding("WEAKSELL", "Energy", 5_000, "SELL", -2, -3),
        _holding("DEFAULTED", "Financials", 15_000, "HOLD", 0, 0),
    ],
    # No genuine violation: 14% each, five sectors, no SELL signal.
    "clean": [
        _holding("C1", "Technology", 14_000, "ACCUMULATE", 7, 2),
        _holding("C2", "Healthcare", 14_000, "WATCH", 4, 0),
        _holding("C3", "Energy", 14_000, "HOLD", 5, -1),
        _holding("C4", "Financials", 14_000, "BUY", 6, 1),
        _holding("C5", "Industrials", 14_000, "ACCUMULATE", 3, 0),
    ],
}
REGIMES = {"SIDEWAYS": ("SIDEWAYS", 0.0), "RISK_OFF": ("RISK_OFF", 0.0),
           "EMERGENCY": ("HIGH_VOLATILITY", 3.1)}
MODES = {
    "legacy": {},
    "sector_advisory_v1": {"sector_policy_mode": SECTOR_POLICY_ADVISORY},
    "muji_v2": {"sector_policy_mode": SECTOR_POLICY_ADVISORY,
                "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2},
}
SCENARIOS = [f"{mode}/{regime}/mixed" for mode in MODES for regime in REGIMES] + ["legacy/RISK_OFF/clean"]


def regime_ctx(name):
    regime, vol_z = REGIMES[name]
    return {"regime": regime, "confidence": 0.7, "transition_stability": "STABLE",
            "vol_z_score": vol_z, "drawdown_score": 50.0, "constraints": get_regime_constraints(regime)}


def _persona():
    dna = {"growth": 55.0, "value": 45.0, "momentum": 50.0, "quality": 60.0, "dividend": 40.0}
    return build_persona_context("BALANCED", dna, compute_style_drift(dna, "BALANCED"))


def build_envelope(pe, scenario, holdings=None):
    """Serialized policy envelope, built exactly as main.py builds it."""
    mode, regime, holdings_name = scenario.split("/")
    rows = holdings if holdings is not None else HOLDINGS[holdings_name]
    envelope = pe.compute_policy(
        _persona(), regime_ctx(regime), _compute_portfolio_weights([dict(r) for r in rows], CASH),
        consensus=None, max_sector_pct=40, **MODES[mode])
    return json.loads(json.dumps(pe.envelope_to_dict(envelope), default=str))


def capture_policy_suppression_baseline(baseline_pe):
    """Fixture builder; run once against the 71cbf19 Policy Engine module."""
    data = {}
    for scenario in SCENARIOS:
        raw = build_envelope(baseline_pe, scenario)
        assert baseline_pe.build_policy_prompt_block(_make_envelope_from_dict(raw)) == raw["prompt_block"]
        kept = [v for v in raw["violations"] if FALSE_FLAG not in v]
        expected = {**raw, "violations": kept}
        expected["prompt_block"] = baseline_pe.build_policy_prompt_block(_make_envelope_from_dict(expected))
        data[scenario] = {"baseline": raw, "expected": expected}
    return data


def _fixture():
    with open(FIXTURE, encoding="utf-8") as fh:
        return json.load(fh)


def _has_false_flag(text):
    return FALSE_FLAG in text or FALSE_FLAG_TAIL in text


# ── Policy Engine output ──────────────────────────────────────────────────────

def test_real_range_scores_with_suppression_on_raise_no_violation():
    hard = HardConstraints(min_cash_pct=20.0, max_single_position_pct=15.0, max_sector_pct=25.0,
                           max_turnover_pct=15.0, suppress_speculative=True, beta_ceiling=None,
                           max_new_positions=0)
    row = {"symbol": "HEALTHY", "weight_pct": 21.0, "signal": "ACCUMULATE", "fa_score": 7, "ta_score": 2}
    assert _detect_violations([row], hard, include_sectors=False, include_positions=False) == []

    envelope = build_envelope(policy_engine, "muji_v2/EMERGENCY/mixed",
                              [_holding("HEALTHY", "Technology", 30_000, "ACCUMULATE", 7, 2)])
    assert envelope["hard_constraints"]["suppress_speculative"] is True
    assert envelope["emergency_override"] is True
    assert envelope["violations"] == []


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_envelope_equals_baseline_minus_false_flags_only(scenario):
    assert build_envelope(policy_engine, scenario) == _fixture()[scenario]["expected"]


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_baseline_fixture_documents_the_defect(scenario):
    entry = _fixture()[scenario]
    suppressed = entry["baseline"]["hard_constraints"]["suppress_speculative"]
    flagged = [v for v in entry["baseline"]["violations"] if FALSE_FLAG in v]
    if suppressed:
        # Healthy, real-range holdings were all flagged, including the best FA score.
        assert flagged and any("(FA=7, TA=2)" in v for v in flagged)
    else:
        # Non-suppression regimes never produced the flag: byte-identical output.
        assert flagged == [] and entry["baseline"] == entry["expected"]


def test_legitimate_violations_are_unchanged():
    legacy = build_envelope(policy_engine, "legacy/EMERGENCY/mixed")["violations"]
    advisory = build_envelope(policy_engine, "sector_advisory_v1/EMERGENCY/mixed")["violations"]
    muji = build_envelope(policy_engine, "muji_v2/EMERGENCY/mixed")["violations"]
    sell = "POLICY_VIOLATION: WEAKSELL has a SELL signal but remains held at 5.0%"
    assert legacy[:3] == [
        "CONCENTRATION_BREACH: HEALTHY at 30.0% exceeds 15% single-position policy limit",
        "CONCENTRATION_BREACH: STEADY at 20.0% exceeds 15% single-position policy limit",
        sell,
    ]
    assert legacy[3:] and all(v.startswith("SECTOR_BREACH:") for v in legacy[3:])
    assert advisory == legacy[:3]  # sector caps advisory, position caps enforced
    assert muji == [sell]          # concentration advisory; SELL-held still reported
    for violations in (legacy, advisory, muji):
        assert not any(_has_false_flag(v) for v in violations)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("regime", ["RISK_OFF", "EMERGENCY"])
def test_regime_suppression_guidance_remains_active(mode, regime):
    envelope = build_envelope(policy_engine, f"{mode}/{regime}/mixed")
    assert envelope["hard_constraints"]["suppress_speculative"] is True
    assert SUPPRESS_GUIDANCE in envelope["prompt_block"]
    assert not _has_false_flag(envelope["prompt_block"])
    if regime == "EMERGENCY":
        assert "speculative assets suppressed" in envelope["policy_narrative"]
        assert "ALL new aggressive allocations are FROZEN" in envelope["prompt_block"]
        assert envelope["hard_constraints"]["min_cash_pct"] >= 20.0
        assert envelope["hard_constraints"]["max_new_positions"] == 0
    regime_block = build_regime_prompt_block(regime_ctx(regime), concentration_advisory=mode == "muji_v2")
    assert "SUPPRESS speculative and high-beta positions" in regime_block


def test_emergency_prompt_no_longer_mandates_false_suppression():
    entry = _fixture()["muji_v2/EMERGENCY/mixed"]
    live = build_envelope(policy_engine, "muji_v2/EMERGENCY/mixed")["prompt_block"]
    assert _has_false_flag(entry["baseline"]["prompt_block"])
    assert not _has_false_flag(live)
    assert "Existing violations to resolve:\n  • POLICY_VIOLATION: WEAKSELL has a SELL signal" in live
    removed = [line for line in entry["baseline"]["prompt_block"].splitlines() if line not in live.splitlines()]
    assert removed and all(_has_false_flag(line) for line in removed)


# ── Prompt paths: Strategist, Challenger, Auditor, retry and fallback ─────────

WATCHLIST = [{"symbol": "CAND", "sector": "Utilities", "current_price": 10, "signal": "WATCH",
              "fa_score": 5, "ta_score": 1}]


def _capture(monkeypatch, mode, path, holdings="mixed", regime="EMERGENCY"):
    scenario = f"{mode}/{regime}/{holdings}"
    captured = {}
    rows = HOLDINGS[holdings]

    def fake_ai(prompt, provider, model, *args, usage_layer, max_tokens=None, **kw):
        captured[usage_layer] = prompt
        if usage_layer == "layer1" and path == "retry":
            return {"text": "not json", "latency_ms": 1}
        if usage_layer in ("layer1", "layer1_retry"):
            payload = {"swaps": [], "top_buys": [], "priority": "no_action"}
        elif usage_layer == "layer2":
            payload = {"allocations": [{"s": r["symbol"], "tw": r["shares"] * r["current_price"] / 1000,
                                        "sig": "HOLD"} for r in rows],
                       "status": "NO_ACTION", "cash_balance_target": 30}
        elif usage_layer == "layer3":
            payload = {"risk_flags": [], "safer_choice": "layer1", "final_risk_level": "medium"}
        else:
            payload = {"allocations": [], "status": "NO_ACTION", "cash_balance_target": 30, "risk_flags": []}
        return {"text": json.dumps(payload), "latency_ms": 1}

    monkeypatch.setattr(optimizer, "call_ai", fake_ai)
    if path == "fallback":
        real = optimizer._emit_stage

        def fail_first_stage(on_stage, stage):
            if stage == "LAYER1_PROPOSAL":
                raise RuntimeError("primary pipeline failure")
            return real(on_stage, stage)

        monkeypatch.setattr(optimizer, "_emit_stage", fail_first_stage)
    optimizer.run_layered_optimizer(
        [dict(r) for r in rows], [dict(r) for r in WATCHLIST], "P", cash_balance=CASH,
        regime_context=regime_ctx(regime), policy_context=build_envelope(policy_engine, scenario),
        **MODES[mode])
    return captured


EXPECTED_LAYERS = {"primary": {"layer1", "layer2", "layer3"},
                   "retry": {"layer1", "layer1_retry", "layer2", "layer3"},
                   "fallback": {"fallback"}}


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("path", EXPECTED_LAYERS)
def test_no_prompt_path_carries_the_false_flag(monkeypatch, mode, path):
    captured = _capture(monkeypatch, mode, path)
    assert EXPECTED_LAYERS[path] <= set(captured)
    for layer, prompt in captured.items():
        assert not _has_false_flag(prompt), layer
    # Prompts that carry the policy block still carry the genuine violation and
    # the regime suppression guidance.
    with_policy = {"layer1", "layer2"} | ({"layer1_retry", "fallback"} if mode == "muji_v2" else set())
    for layer in with_policy & set(captured):
        assert "WEAKSELL has a SELL signal but remains held" in captured[layer], layer
        assert SUPPRESS_GUIDANCE in captured[layer], layer


def test_legacy_strategist_reduce_mandate_lists_only_genuine_violations(monkeypatch):
    prompt = _capture(monkeypatch, "legacy", "primary")["layer1"]
    note = prompt.split("POLICY VIOLATIONS ACTIVE: ", 1)[1].split("\n", 1)[0]
    assert "CONCENTRATION_BREACH: HEALTHY" in note and "WEAKSELL has a SELL signal" in note
    assert not _has_false_flag(note)


def test_legacy_strategist_has_no_reduce_mandate_without_genuine_violations(monkeypatch):
    baseline = _fixture()["legacy/RISK_OFF/clean"]["baseline"]["violations"]
    assert baseline and all(FALSE_FLAG in v for v in baseline)  # previously: forced REDUCE note
    prompt = _capture(monkeypatch, "legacy", "primary", holdings="clean", regime="RISK_OFF")["layer1"]
    assert "POLICY VIOLATIONS ACTIVE" not in prompt
    assert SUPPRESS_GUIDANCE in prompt


# ── Legacy stabilization ──────────────────────────────────────────────────────

def _stabilize(active_policy):
    result = {
        "status": "REBALANCE", "consensus": {}, "active_policy": active_policy,
        "market_regime": {"regime": "RISK_OFF"}, "rebalance_opportunity_score": 50,
        "layer3_result": {"risk_flags": []},
        "target_allocations": [{"symbol": r["symbol"], "action": "HOLD", "current_weight": 14.0,
                                "target_weight": 14.0, "allocation_change_percent": 0}
                               for r in HOLDINGS["clean"]],
    }
    return apply_stabilization(result, last_rebalance_at=None)["status"]


def test_legacy_stabilization_ignores_the_removed_flag_but_not_genuine_violations():
    baseline = _fixture()["legacy/RISK_OFF/clean"]["baseline"]
    assert _stabilize(baseline) == "REBALANCE"  # false flags used to block it

    live = build_envelope(policy_engine, "legacy/RISK_OFF/clean")
    assert live["violations"] == []
    assert _stabilize(live) == STATUS_NO_REBALANCE

    with_sell = [dict(r) for r in HOLDINGS["clean"]]
    with_sell[0]["signal"] = "SELL"
    genuine = build_envelope(policy_engine, "legacy/RISK_OFF/clean", with_sell)
    assert genuine["violations"] == ["POLICY_VIOLATION: C1 has a SELL signal but remains held at 14.0%"]
    assert _stabilize(genuine) == "REBALANCE"


# ── Frozen runs #247 / #248 (offline; inputs copied from history) ─────────────

# Both runs: same holdings, scores and envelope (HIGH_VOLATILITY, emergency,
# MUJI V2 + sector advisory). Weights are current NAV weights.
FROZEN_HARD = HardConstraints(min_cash_pct=20.3, max_single_position_pct=15.0, max_sector_pct=25.0,
                              max_turnover_pct=14.7, suppress_speculative=True, beta_ceiling=None,
                              max_new_positions=0)
FROZEN_HOLDINGS = [
    {"symbol": "BH.BK", "weight_pct": 21.19, "signal": "ACCUMULATE", "fa_score": 4, "ta_score": 0},
    {"symbol": "GOOGL01.BK", "weight_pct": 7.69, "signal": "ACCUMULATE", "fa_score": 6, "ta_score": 0},
    {"symbol": "GULF.BK", "weight_pct": 16.92, "signal": "WATCH", "fa_score": 5, "ta_score": -1},
    {"symbol": "NVDA01.BK", "weight_pct": 11.64, "signal": "WATCH", "fa_score": 6, "ta_score": 1},
    {"symbol": "MICRON01.BK", "weight_pct": 10.70, "signal": "ACCUMULATE", "fa_score": 7, "ta_score": 0},
]
FROZEN_STORED_VIOLATIONS = [
    f"POLICY_VIOLATION: {h['symbol']} is low-quality (FA={h['fa_score']}, TA={h['ta_score']}) "
    "and should be suppressed per current policy" for h in FROZEN_HOLDINGS
]


def test_frozen_runs_247_248_produce_no_false_violation():
    assert all(_has_false_flag(v) for v in FROZEN_STORED_VIOLATIONS)
    # As recorded (MUJI V2 + sector advisory): every stored violation was false.
    assert _detect_violations(FROZEN_HOLDINGS, FROZEN_HARD, include_sectors=False,
                              include_positions=False) == []
    # Legacy-style position checks on the same inputs keep the genuine breaches.
    assert _detect_violations(FROZEN_HOLDINGS, FROZEN_HARD, include_sectors=False) == [
        "CONCENTRATION_BREACH: BH.BK at 21.2% exceeds 15% single-position policy limit",
        "CONCENTRATION_BREACH: GULF.BK at 16.9% exceeds 15% single-position policy limit",
    ]
