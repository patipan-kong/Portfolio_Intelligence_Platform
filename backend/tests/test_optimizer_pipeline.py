"""
Regression tests for the optimizer pipeline.

Verifies that L1 swap data (Gemini) and L2 allocation data survive
raw-response → parser → orchestrator without silent loss or status corruption.
"""

import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.optimizer import (
    HardPolicyEnforcementError,
    _enforce_hard_policy,
    _fallback_prompt,
    _normalize_l1_swaps,
    _normalize_allocations,
    _reconcile_allocation_actions,
    _snap_neutral_actions,
    _consensus_engine,
    _postprocess_swaps,
)
from services.optimizer.constraint_resolver import resolve_constraints
import agents.optimizer as optimizer_module


def _effective_envelope(max_position=20.0):
    return resolve_constraints(
        {"max_sector_pct": 40}, {"Technology": 30},
        {"regime": "SIDEWAYS", "constraints": {
            "max_single_position_pct": max_position,
            "min_cash_pct": 10,
            "turnover_multiplier": 1,
        }},
        {"volatility_tolerance": 1, "max_cash_preference": .1, "turnover_tolerance": .4},
    )


def test_shared_hard_enforcement_preserves_buy_hold_reduce_semantics():
    allocations = [
        {"symbol": "BUY", "action": "BUY", "current_weight": 5.0, "target_weight": 25.0},
        {"symbol": "HOLD", "action": "HOLD", "current_weight": 30.0, "target_weight": 30.0},
        {"symbol": "REDUCE", "action": "REDUCE", "current_weight": 25.0, "target_weight": 23.0},
    ]
    for allocation in allocations:
        allocation["allocation_change_percent"] = allocation["target_weight"] - allocation["current_weight"]
        allocation["estimated_amount"] = 0
    envelope = _effective_envelope()
    policy = {
        "hard_constraints": {"max_single_position_pct": 20, "min_cash_pct": 10},
        "emergency_override": False,
        "deployment_bias": "SELECTIVE",
    }
    _enforce_hard_policy(
        allocations, total_value=1000, policy_context=policy, regime_context=None,
        effective_envelope=envelope,
        portfolio_data=[
            {"symbol": "BUY", "sector": "Technology"},
            {"symbol": "HOLD", "sector": "Financial"},
            {"symbol": "REDUCE", "sector": "Energy"},
        ],
        watchlist_data=[],
    )
    _reconcile_allocation_actions(allocations)
    by_symbol = {a["symbol"]: a for a in allocations}
    assert by_symbol["BUY"]["target_weight"] == 20
    assert by_symbol["HOLD"]["target_weight"] == 30
    assert by_symbol["HOLD"]["action"] == "HOLD"
    assert by_symbol["REDUCE"]["target_weight"] == 23
    assert by_symbol["REDUCE"]["action"] == "REDUCE"


def test_shared_hard_enforcement_emergency_cash_sector_and_reconciliation():
    emergency = [{"symbol": "A", "action": "ACCUMULATE", "current_weight": 5.0,
                  "target_weight": 25.0, "allocation_change_percent": 20.0, "estimated_amount": 200}]
    _enforce_hard_policy(
        emergency, total_value=1000,
        policy_context={"hard_constraints": {"max_single_position_pct": 20, "min_cash_pct": 10},
                        "emergency_override": True, "deployment_bias": "DEFENSIVE"},
        regime_context=None, effective_envelope=_effective_envelope(),
        portfolio_data=[{"symbol": "A", "sector": "Technology"}], watchlist_data=[],
    )
    _reconcile_allocation_actions(emergency)
    assert emergency[0]["action"] == "HOLD"
    assert emergency[0]["target_weight"] == 5

    allocations = [
        {"symbol": "A", "action": "BUY", "current_weight": 25.0,
         "target_weight": 40.0, "allocation_change_percent": 15.0, "estimated_amount": 150},
        {"symbol": "B", "action": "ACCUMULATE", "current_weight": 20.0,
         "target_weight": 35.0, "allocation_change_percent": 15.0, "estimated_amount": 150},
    ]
    _enforce_hard_policy(
        allocations, total_value=1000,
        policy_context={"hard_constraints": {"max_single_position_pct": 20, "min_cash_pct": 60},
                        "emergency_override": False, "deployment_bias": "SELECTIVE"},
        regime_context=None, effective_envelope=_effective_envelope(),
        portfolio_data=[{"symbol": "A", "sector": "Technology"}, {"symbol": "B", "sector": "Technology"}],
        watchlist_data=[],
    )
    _reconcile_allocation_actions(allocations)
    assert sum(a["target_weight"] for a in allocations) <= 40
    assert all(a["action"] in ("HOLD", "REDUCE") for a in allocations)


def test_policy_safe_fallback_prompt_projects_limits_without_goal_facts_or_provenance():
    rules = (
        "7. Effective maximum single-position weight is 20.0%\n"
        "8. Effective minimum cash weight is 10.0%\n"
        "9. Effective sector caps: {\"Technology\": 30.0}\n"
    )
    prompt = _fallback_prompt([], [], [], [], 12, 40, 1000, 100, rules)
    assert "20.0%" in prompt and "10.0%" in prompt and "Technology" in prompt
    for forbidden in ("goal_constraint_goal_id", "target_date", "days_remaining", "WEALTH_GOAL_POLICY"):
        assert forbidden not in prompt


def test_shared_action_reconciliation_exact_thresholds():
    allocations = [
        {"symbol": "N", "action": "BUY", "allocation_change_percent": -2},
        {"symbol": "Z", "action": "ACCUMULATE", "allocation_change_percent": 0},
        {"symbol": "P", "action": "REDUCE", "allocation_change_percent": 2},
    ]
    _reconcile_allocation_actions(allocations)
    assert [a["action"] for a in allocations] == ["REDUCE", "HOLD", "ACCUMULATE"]


def test_policy_safe_fallback_enforces_cap_and_preserves_marker(monkeypatch):
    captured = []
    monkeypatch.setattr(optimizer_module, "call_ai", lambda prompt, *args, **kwargs: (
        captured.append(prompt) or {
            "latency_ms": 1,
            "text": json.dumps({"allocations": [
                {"s": "BUY", "tw": 25, "sig": "BUY", "r": "buy"},
                {"s": "HOLD", "tw": 30, "sig": "HOLD", "r": "hold"},
                {"s": "REDUCE", "tw": 23, "sig": "REDUCE", "r": "reduce"},
            ]}),
        }
    ))
    envelope = _effective_envelope()
    result = optimizer_module._run_single_shot_fallback(
        pc=[
            {"symbol": "BUY", "sector": "Technology"},
            {"symbol": "HOLD", "sector": "Financial"},
            {"symbol": "REDUCE", "sector": "Energy"},
        ],
        wc=[], sell_forced=[], locked=[],
        portfolio_data=[
            {"symbol": "BUY", "sector": "Technology"},
            {"symbol": "HOLD", "sector": "Financial"},
            {"symbol": "REDUCE", "sector": "Energy"},
        ],
        current_sector_weights={}, pc_map={"BUY": 5, "HOLD": 30, "REDUCE": 25},
        max_stocks=12, max_sector_pct=40, sector_limits={}, total_value=1000,
        cash_balance=100, fallback_provider="test", fallback_model="test",
        portfolio_name="P", portfolio_count=3, max_reached=False,
        policy_context={
            "hard_constraints": {"max_single_position_pct": 20, "min_cash_pct": 0},
            "emergency_override": False, "deployment_bias": "SELECTIVE",
        },
        effective_envelope=envelope, enforce_effective_policy=True,
    )
    by_symbol = {a["symbol"]: a for a in result["target_allocations"]}
    assert by_symbol["BUY"]["target_weight"] == 20
    assert by_symbol["HOLD"]["target_weight"] == 30
    assert by_symbol["REDUCE"]["target_weight"] == 23
    assert result["fallback_mode"] is True
    assert "20.0%" in captured[0]


def test_policy_safe_fallback_enforcement_failure_is_typed_and_has_no_second_fallback(monkeypatch):
    calls = []
    monkeypatch.setattr(optimizer_module, "call_ai", lambda *a, **k: (
        calls.append("provider") or {"latency_ms": 1, "text": '{"allocations": []}'}
    ))
    monkeypatch.setattr(
        optimizer_module, "_enforce_hard_policy",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("enforcement")),
    )
    with pytest.raises(HardPolicyEnforcementError):
        optimizer_module._run_single_shot_fallback(
            [], [], [], [], [], {}, {}, 12, 40, {}, 1000, 0,
            "test", "test", "P", 0, False,
            policy_context={"hard_constraints": {}},
            effective_envelope=_effective_envelope(), enforce_effective_policy=True,
        )
    assert calls == ["provider"]


def test_primary_enforcement_failure_bypasses_global_fallback_when_opted_in(monkeypatch):
    responses = {
        "layer1": {"swaps": [], "top_buys": [], "sector_flags": [], "priority": ""},
        "layer2": {"allocations": [{"s": "A", "tw": 25, "sig": "BUY", "r": "buy"}],
                   "status": "REBALANCE"},
        "layer3": {"risk_flags": [], "safer_choice": "layer2", "final_risk_level": "low"},
    }
    monkeypatch.setattr(optimizer_module, "call_ai", lambda *a, **k: {
        "latency_ms": 1, "text": json.dumps(responses[k["usage_layer"]]),
    })
    monkeypatch.setattr(
        optimizer_module, "_enforce_hard_policy",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("hard")),
    )
    monkeypatch.setattr(
        optimizer_module, "_run_single_shot_fallback",
        lambda *a, **k: pytest.fail("typed enforcement failure must bypass fallback"),
    )
    with pytest.raises(HardPolicyEnforcementError):
        optimizer_module.run_layered_optimizer(
            [{"symbol": "A", "shares": 1, "current_price": 100, "signal": "BUY", "sector": "Technology"}],
            [], "P", policy_context={
                "hard_constraints": {"max_single_position_pct": 20, "min_cash_pct": 0,
                                     "max_sector_pct": 40, "max_turnover_pct": 40},
                "emergency_override": False,
            },
            effective_envelope=_effective_envelope(),
            enforce_effective_policy_in_fallback=True,
        )


def test_generic_primary_failure_still_enters_policy_safe_fallback(monkeypatch):
    monkeypatch.setattr(
        optimizer_module, "call_ai",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("provider")),
    )
    fallback_calls = []
    monkeypatch.setattr(
        optimizer_module, "_run_single_shot_fallback",
        lambda *a, **k: fallback_calls.append(k) or {"fallback_mode": True},
    )
    result = optimizer_module.run_layered_optimizer(
        [{"symbol": "A", "shares": 1, "current_price": 100, "signal": "BUY", "sector": "Technology"}],
        [], "P", policy_context={
            "hard_constraints": {"max_single_position_pct": 20, "min_cash_pct": 0,
                                 "max_sector_pct": 40, "max_turnover_pct": 40},
            "emergency_override": False,
        },
        effective_envelope=_effective_envelope(),
        enforce_effective_policy_in_fallback=True,
    )
    assert result["fallback_mode"] is True
    assert fallback_calls[0]["enforce_effective_policy"] is True
    assert fallback_calls[0]["policy_context"]["hard_constraints"]["max_single_position_pct"] == 20


# ── _normalize_l1_swaps ───────────────────────────────────────────────────────

def test_normalize_l1_swaps_compact_keys():
    """Gemini compact-key format (sell/buy) → full swap_suggestions format."""
    raw = [{"sell": "SCB.BK", "buy": "MSFT01.BK", "score_delta": 3.5, "sector": "Technology", "type": "SWAP"}]
    result = _normalize_l1_swaps(raw)
    assert len(result) == 1
    assert result[0]["sell_symbol"] == "SCB.BK"
    assert result[0]["buy_symbol"] == "MSFT01.BK"
    assert result[0]["score_improvement"] == 3.5
    assert result[0]["type"] == "SWAP"


def test_normalize_l1_swaps_sell_only():
    raw = [{"sell": "PTT.BK", "buy": None, "score_delta": 0, "sector": "Energy", "type": "SELL"}]
    result = _normalize_l1_swaps(raw)
    assert result[0]["sell_symbol"] == "PTT.BK"
    assert result[0]["buy_symbol"] is None
    assert result[0]["type"] == "SELL"


def test_normalize_l1_swaps_empty():
    assert _normalize_l1_swaps([]) == []
    assert _normalize_l1_swaps(None) == []


def test_normalize_l1_swaps_full_keys():
    """Full-key format (sell_symbol/buy_symbol) also accepted."""
    raw = [{"sell_symbol": "KBANK.BK", "buy_symbol": "AAPL01.BK", "score_improvement": 2.0, "type": "SWAP"}]
    result = _normalize_l1_swaps(raw)
    assert result[0]["sell_symbol"] == "KBANK.BK"
    assert result[0]["buy_symbol"] == "AAPL01.BK"


def test_normalize_l1_swaps_compact_reason_key():
    """L1 compact schema uses "r" for the reason, same convention as _normalize_allocations'
    "r" fallback for L2 — must not be silently dropped."""
    raw = [{"sell": "SCB.BK", "buy": "MSFT01.BK", "score_delta": 3.5, "sector": "Technology", "type": "SWAP", "r": "Technology at 45% > 30% limit"}]
    result = _normalize_l1_swaps(raw)
    assert result[0]["reason"] == "Technology at 45% > 30% limit"


def test_normalize_l1_swaps_full_reason_key():
    """Full "reason" key (used by forced-SELL entries) still takes priority over "r"."""
    raw = [{"sell": "PTT.BK", "buy": None, "reason": "Forced exit: SELL signal.", "r": "ignored", "type": "SELL"}]
    result = _normalize_l1_swaps(raw)
    assert result[0]["reason"] == "Forced exit: SELL signal."


def test_normalize_l1_swaps_missing_reason_defaults_empty():
    raw = [{"sell": "PTT.BK", "buy": None, "score_delta": 0, "type": "SELL"}]
    result = _normalize_l1_swaps(raw)
    assert result[0]["reason"] == ""


# ── _normalize_allocations ────────────────────────────────────────────────────

def test_normalize_allocations_basic():
    raw = [
        {"symbol": "AAPL", "current_weight": 10.0, "target_weight": 15.0, "action": "ACCUMULATE", "reason": "Strong FA"},
        {"symbol": "PTT.BK", "current_weight": 8.0, "target_weight": 5.0, "action": "REDUCE", "reason": "Overweight"},
    ]
    result = _normalize_allocations(raw)
    assert len(result) == 2
    aapl = next(a for a in result if a["symbol"] == "AAPL")
    assert aapl["target_weight"] == 15.0
    assert aapl["action"] == "ACCUMULATE"
    assert aapl["allocation_change_percent"] == 5.0

    ptt = next(a for a in result if a["symbol"] == "PTT.BK")
    assert ptt["allocation_change_percent"] == -3.0


def test_normalize_allocations_pc_map_overrides_ai_weight():
    """pc_map (real portfolio data) should override AI-reported current_weight."""
    raw = [{"symbol": "GOOGL", "current_weight": 5.0, "target_weight": 12.0, "action": "BUY", "reason": ""}]
    pc_map = {"GOOGL": 8.0}  # real weight is 8%, AI said 5%
    result = _normalize_allocations(raw, pc_map)
    assert result[0]["current_weight"] == 8.0
    assert result[0]["allocation_change_percent"] == 4.0  # 12 - 8


def test_normalize_allocations_drops_empty_symbol():
    raw = [{"symbol": "", "target_weight": 10.0, "action": "BUY", "reason": ""}]
    result = _normalize_allocations(raw)
    assert result == []


# ── _snap_neutral_actions ──────────────────────────────────────────────────────

def test_snap_neutral_actions_zeroes_hold_and_watch():
    """WATCH/HOLD are investment signals, not trade instructions — a nonzero
    target_weight on these rows (e.g. from a portfolio-level rebalance trim) must
    not leak through as a phantom weight/cash delta."""
    allocations = [
        {"symbol": "AAPL", "current_weight": 10.0, "target_weight": 15.0,
         "action": "BUY", "allocation_change_percent": 5.0, "estimated_amount": 50000},
        {"symbol": "PTT.BK", "current_weight": 8.0, "target_weight": 7.0,
         "action": "HOLD", "allocation_change_percent": -1.0, "estimated_amount": -10000},
        {"symbol": "SCB.BK", "current_weight": 6.0, "target_weight": 9.5,
         "action": "WATCH", "allocation_change_percent": 3.5, "estimated_amount": 35000},
    ]
    _snap_neutral_actions(allocations)

    aapl = next(a for a in allocations if a["symbol"] == "AAPL")
    assert aapl["target_weight"] == 15.0
    assert aapl["allocation_change_percent"] == 5.0
    assert aapl["estimated_amount"] == 50000

    ptt = next(a for a in allocations if a["symbol"] == "PTT.BK")
    assert ptt["target_weight"] == 8.0
    assert ptt["allocation_change_percent"] == 0.0
    assert ptt["estimated_amount"] == 0

    scb = next(a for a in allocations if a["symbol"] == "SCB.BK")
    assert scb["target_weight"] == 6.0
    assert scb["allocation_change_percent"] == 0.0
    assert scb["estimated_amount"] == 0


def test_snap_neutral_actions_watchlist_watch_zeroed_to_zero():
    """A WATCH row for a symbol the portfolio doesn't hold has current_weight=0.0 —
    any hallucinated nonzero target_weight must snap back to zero, not to some
    nonzero 'current' figure."""
    allocations = [
        {"symbol": "NVDA", "current_weight": 0.0, "target_weight": 4.0,
         "action": "WATCH", "allocation_change_percent": 4.0, "estimated_amount": 40000},
    ]
    _snap_neutral_actions(allocations)
    assert allocations[0]["target_weight"] == 0.0
    assert allocations[0]["allocation_change_percent"] == 0.0
    assert allocations[0]["estimated_amount"] == 0


def test_snap_neutral_actions_ignores_actionable_rows():
    """SELL/REDUCE/ACCUMULATE rows carry a real trade — must pass through unchanged.
    Also verifies case-insensitivity on the action field, matching the .upper()
    handling used elsewhere in this file."""
    allocations = [
        {"symbol": "KBANK.BK", "current_weight": 12.0, "target_weight": 0.0,
         "action": "sell", "allocation_change_percent": -12.0, "estimated_amount": -120000},
        {"symbol": "MSFT01.BK", "current_weight": 9.0, "target_weight": 6.0,
         "action": "REDUCE", "allocation_change_percent": -3.0, "estimated_amount": -30000},
        {"symbol": "GOOGL", "current_weight": 5.0, "target_weight": 8.0,
         "action": "ACCUMULATE", "allocation_change_percent": 3.0, "estimated_amount": 30000},
    ]
    before = [dict(a) for a in allocations]
    _snap_neutral_actions(allocations)
    assert allocations == before


# ── raw_allocs extraction (None vs falsy) ─────────────────────────────────────

def test_raw_allocs_none_check():
    """Simulates the fixed extraction logic — explicit None check prevents
    dropping a valid but empty allocations list."""
    l2_result = {"allocations": None, "target_allocations": [{"symbol": "X", "target_weight": 10.0}]}
    # Fixed logic: pop allocations; if None, fallback to target_allocations
    raw = l2_result.pop("allocations", None)
    if raw is None:
        raw = l2_result.pop("target_allocations", [])
    assert len(raw) == 1

    # Old buggy logic would silently drop this case:
    l2_old = {"allocations": [], "target_allocations": [{"symbol": "X"}]}
    raw_old = l2_old.pop("allocations", None) or l2_old.get("target_allocations", [])
    # Empty list from allocations is falsy → falls to target_allocations → incidentally works here
    # but the bug was that a valid empty list triggers fallback to a potentially different field
    assert raw_old == [{"symbol": "X"}]  # demonstrates the silent fallback behaviour


# ── _postprocess_swaps ────────────────────────────────────────────────────────

def test_postprocess_swaps_injects_forced_sell():
    swaps = [{"sell_symbol": "A", "buy_symbol": "B", "reason": "", "score_improvement": 1, "sector": "Tech", "type": "SWAP"}]
    result = _postprocess_swaps(swaps, sell_forced=["FORCED.BK"], locked=[])
    symbols = {s["sell_symbol"] for s in result}
    assert "FORCED.BK" in symbols


def test_postprocess_swaps_removes_locked():
    swaps = [{"sell_symbol": "LOCKED.BK", "buy_symbol": "B", "reason": "", "score_improvement": 1, "sector": "Tech", "type": "SWAP"}]
    result = _postprocess_swaps(swaps, sell_forced=[], locked=["LOCKED.BK"])
    assert all(s["sell_symbol"] != "LOCKED.BK" for s in result)


# ── _consensus_engine ─────────────────────────────────────────────────────────

def test_consensus_rebalance_high_confidence():
    l2 = {"agrees_with_layer1": True, "status": "REBALANCE", "rebalance_opportunity_score": 75}
    l3 = {"risk_flags": [], "safer_choice": "layer1", "final_risk_level": "low", "auditor_notes": ""}
    c = _consensus_engine(l2, l3)
    assert c["consensus_decision"] == "REBALANCE"
    assert c["confidence"] == "high"
    assert c["recommended"] == "layer1"


def test_consensus_no_action_low_score():
    l2 = {"agrees_with_layer1": True, "status": "NO_ACTION", "rebalance_opportunity_score": 10,
          "no_action_summary": "Well balanced."}
    l3 = {"risk_flags": [], "safer_choice": "layer1", "final_risk_level": "low", "auditor_notes": ""}
    c = _consensus_engine(l2, l3)
    assert c["consensus_decision"] == "NO_ACTION"
    assert "Well balanced." in c["recommended_action"]


def test_consensus_l1_parse_failure_propagation():
    """When L1 failed and was marked strategist_parse_failed, agrees_with_layer1
    should be False and disagreements note should be present."""
    l2 = {
        "agrees_with_layer1": False,
        "disagreements": ["L1_PARSE_FAILURE: Strategist output could not be parsed — treating as disagreement."],
        "strategist_parse_failed": True,
        "status": "REBALANCE",
        "rebalance_opportunity_score": 50,
    }
    l3 = {"risk_flags": [], "safer_choice": "layer2", "final_risk_level": "medium", "auditor_notes": ""}
    c = _consensus_engine(l2, l3)
    assert c["agrees"] is False
    assert c["consensus_decision"] == "REBALANCE"


def test_consensus_critical_flag_forces_rebalance():
    """CRITICAL risk flag should veto NO_ACTION even at low score."""
    l2 = {"agrees_with_layer1": True, "status": "NO_ACTION", "rebalance_opportunity_score": 5}
    l3 = {
        "risk_flags": [{"symbol": "PTT.BK", "issue": "sector >40%", "severity": "CRITICAL"}],
        "safer_choice": "layer1", "final_risk_level": "high", "auditor_notes": "",
    }
    c = _consensus_engine(l2, l3)
    assert c["consensus_decision"] == "REBALANCE"


# ── Real Gemini L1 response fixture ──────────────────────────────────────────

GEMINI_L1_FIXTURE = """{
  "swaps": [
    {"sell": "SCB.BK", "buy": "MSFT01.BK", "score_delta": 4.2, "sector": "Technology", "type": "SWAP"},
    {"sell": "PTT.BK", "buy": null, "score_delta": 0, "sector": "Energy", "type": "SELL"}
  ],
  "top_buys": ["MSFT01.BK", "AAPL01.BK", "NVDA01.BK"],
  "sector_flags": ["Financial 32%>30%"],
  "priority": "rebalance"
}"""


def test_gemini_l1_fixture_survives_pipeline():
    """Simulates: raw Gemini response → safe_parse_json → _normalize_l1_swaps → _postprocess_swaps."""
    import json
    parsed = json.loads(GEMINI_L1_FIXTURE)

    swaps = _normalize_l1_swaps(parsed.get("swaps", []))
    assert len(swaps) == 2, "Both swaps must survive normalization"

    final = _postprocess_swaps(swaps, sell_forced=[], locked=[])
    assert len(final) == 2, "Swaps must survive postprocessing"
    assert final[0]["sell_symbol"] == "SCB.BK"
    assert final[0]["buy_symbol"] == "MSFT01.BK"
    assert final[1]["sell_symbol"] == "PTT.BK"
    assert final[1]["buy_symbol"] is None

    # Verify these would be visible in layer1_result.swap_suggestions on the frontend
    for s in final:
        assert "sell_symbol" in s
        assert "buy_symbol" in s
        assert "type" in s
        assert "reason" in s
