"""Deterministic Phase 3 selection and fail-closed pipeline coverage."""

import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import agents.optimizer as optimizer
import main
from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY
from services.optimizer.strategic_candidates import (
    SELECTION_VERSION, prepare_candidates, validate_candidate_reviews, decide_selection,
)


HOLDINGS = [
    {"symbol": "AAA", "shares": 60, "current_price": 10, "weight_pct": 60,
     "signal": "SELL", "fa_score": 30},
    {"symbol": "BBB", "shares": 20, "current_price": 10, "weight_pct": 20,
     "signal": "HOLD", "fa_score": 70, "pe_ratio": 12},
]


def test_selection_mode_requires_explicit_exact_request_marker():
    assert main.OptimizerRequest(portfolio_id=1).strategy_selection_mode is None
    assert main.OptimizerRequest(portfolio_id=1, strategy_selection_mode=SELECTION_VERSION).strategy_selection_mode == SELECTION_VERSION
    with pytest.raises(Exception):
        main.OptimizerRequest(portfolio_id=1, strategy_selection_mode="wealth.strategy-selection.v2")


def _proposal(family="RAISE_CASH"):
    rows = [
        {"symbol": "AAA", "action": "SELL", "current_weight": 60,
         "target_weight": 0, "allocation_change_percent": -60,
         "decision_basis": "INVESTMENT_THESIS"},
        {"symbol": "BBB", "action": "HOLD", "current_weight": 20,
         "target_weight": 20, "allocation_change_percent": 0},
    ]
    return {"strategy_family": family, "target_allocations": rows,
            "target_cash_weight": 80, "observed_evidence_refs": ["symbol:AAA:signal"],
            "portfolio_assessment": "Frozen sell signal supports raising cash."}


def _audit(envelope):
    return validate_candidate_reviews({"candidate_reviews": [
        {"candidate_id": c["id"], "supporting_refs": list(c["observed_evidence_refs"]),
         "opposing_refs": [], "material_conflicts": [], "assessment": "Model view"}
        for c in envelope["candidates"]
    ]}, envelope)


@pytest.mark.parametrize("family", ["RAISE_CASH", "DEFENSIVE_ROTATION", "GROWTH_ROTATION"])
def test_eligible_family_can_win_with_verified_reference(family):
    plan = _proposal(family)
    if family == "DEFENSIVE_ROTATION":
        plan["target_allocations"][1].update(action="BUY", target_weight=30,
                                               allocation_change_percent=10)
        plan["target_cash_weight"] = 70
        plan["observed_evidence_refs"].append("symbol:BBB:pe_ratio")
    if family == "GROWTH_ROTATION":
        plan["target_allocations"][1].update(action="BUY", target_weight=30,
                                               allocation_change_percent=10)
        plan["target_cash_weight"] = 70
        plan["observed_evidence_refs"].append("symbol:BBB:pe_ratio")
    envelope = prepare_candidates(HOLDINGS, [], 200, plan)
    candidate = envelope["candidates"][1]
    assert candidate["eligibility_status"] == "ELIGIBLE"
    audit = _audit(envelope)
    decision = decide_selection(envelope, audit, {
        "selected_candidate_id": candidate["id"],
        "supporting_evidence_refs": ["symbol:AAA:signal"],
        "opposing_evidence_refs": [], "comparison_against_hold": "Supported exit reduces thesis risk.",
        "decision_rationale": "The independently observed SELL signal supports this exit.",
        "material_uncertainty": [],
    })
    assert decision["state"] == "SELECTED"
    assert decision["selected_candidate_id"] == candidate["id"]


def test_hold_wins_and_auditor_failure_fails_closed():
    envelope = prepare_candidates(HOLDINGS, [], 200, _proposal())
    audit = _audit(envelope)
    selected = decide_selection(envelope, audit, {
        "selected_candidate_id": "hold-current", "supporting_evidence_refs": [],
        "opposing_evidence_refs": [], "comparison_against_hold": "Current portfolio is preferred.",
        "decision_rationale": "Wait for clearer evidence.", "material_uncertainty": [],
    })
    assert selected["selected_candidate_id"] == "hold-current"
    caution = decide_selection(envelope, {"status": "UNAVAILABLE", "reason": "AUDITOR_DOWN"}, None)
    assert caution["selected_candidate_id"] == "hold-current"
    assert caution["material_uncertainty"] == ["AUDITOR_DOWN"]
    review = decide_selection(envelope, audit, None, hold_safe=False)
    assert review["state"] == "HUMAN_REVIEW_REQUIRED"
    assert review["selected_candidate_id"] is None
    missing_nav = prepare_candidates([{**HOLDINGS[0], "current_price": None}, HOLDINGS[1]],
                                     [], 200, _proposal())
    unavailable = decide_selection(missing_nav, {"status": "UNAVAILABLE"}, None)
    assert unavailable["state"] == "HUMAN_REVIEW_REQUIRED"
    assert unavailable["selected_candidate_id"] is None


def test_unsupported_and_advisory_only_cannot_win():
    unsupported = _proposal()
    unsupported["observed_evidence_refs"] = ["position:AAA:cap"]
    envelope = prepare_candidates(HOLDINGS, [], 200, unsupported)
    bad = envelope["candidates"][1]
    assert bad["eligibility_status"] != "ELIGIBLE"
    decision = decide_selection(envelope, _audit(envelope), {
        "selected_candidate_id": bad["id"], "supporting_evidence_refs": [],
        "opposing_evidence_refs": [], "comparison_against_hold": "Cap breached",
        "decision_rationale": "Sell to repair cap", "material_uncertainty": [],
    })
    assert decision["selected_candidate_id"] == "hold-current"


def test_score_only_and_incomplete_plan_are_not_eligible():
    score_only = _proposal()
    score_only["observed_evidence_refs"] = ["symbol:AAA:fa_score"]
    assert "MODEL_SCORE_ONLY_SUPPORT" in prepare_candidates(HOLDINGS, [], 200, score_only)["candidates"][1]["eligibility_reasons"]
    incomplete = _proposal()
    incomplete["candidate_input_invalid"] = True
    assert "INCOMPLETE_MODEL_ALLOCATION" in prepare_candidates(HOLDINGS, [], 200, incomplete)["candidates"][1]["eligibility_reasons"]
    unsupported_buy = _proposal("GROWTH_ROTATION")
    unsupported_buy["target_allocations"][1].update(action="BUY", target_weight=30,
                                                       allocation_change_percent=10)
    unsupported_buy["target_cash_weight"] = 70
    assert "BUY_SUPPORT_UNVERIFIED:BBB" in prepare_candidates(
        HOLDINGS, [], 200, unsupported_buy)["candidates"][1]["eligibility_reasons"]


def test_optional_complete_plans_keep_distinct_stable_candidate_ids():
    primary = _proposal()
    defensive = _proposal("DEFENSIVE_ROTATION")
    defensive["target_allocations"][1].update(action="BUY", target_weight=30,
                                                allocation_change_percent=10)
    defensive["target_cash_weight"] = 70
    defensive["observed_evidence_refs"].append("symbol:BBB:pe_ratio")
    primary["additional_plans"] = [defensive]
    envelope = prepare_candidates(HOLDINGS, [], 200, primary)
    assert [c["family"] for c in envelope["candidates"]] == ["HOLD", "RAISE_CASH", "DEFENSIVE_ROTATION"]
    assert envelope["candidates"][1]["id"] != envelope["candidates"][2]["id"]
    assert [c["id"] for c in envelope["candidates"]] == [
        c["id"] for c in prepare_candidates(HOLDINGS, [], 200, primary)["candidates"]]


def test_auditor_conflict_and_invalid_committee_do_not_select_action():
    envelope = prepare_candidates(HOLDINGS, [], 200, _proposal())
    raw = {"candidate_reviews": [
        {"candidate_id": c["id"], "supporting_refs": list(c["observed_evidence_refs"]),
         "opposing_refs": [], "material_conflicts": ["Earnings data conflict"] if c["family"] != "HOLD" else []}
        for c in envelope["candidates"]]}
    audit = validate_candidate_reviews(raw, envelope)
    assert audit["status"] == "AVAILABLE"
    decision = decide_selection(envelope, audit, {
        "selected_candidate_id": envelope["candidates"][1]["id"],
        "supporting_evidence_refs": ["symbol:AAA:signal"], "opposing_evidence_refs": [],
        "comparison_against_hold": "Exit", "decision_rationale": "Sell",
        "material_uncertainty": []})
    assert decision["selected_candidate_id"] == "hold-current"
    assert "MATERIAL_CONFLICT_UNRESOLVED" in decision["material_uncertainty"]
    assert decide_selection(envelope, audit, {"selected_candidate_id": "invented"})["selected_candidate_id"] == "hold-current"
    assert decide_selection(envelope, audit, {"selected_candidate_id": []})["selected_candidate_id"] == "hold-current"


# ── Slice 4.6B: candidate-scoped material-conflict veto (B1) ─────────────────
# Candidate-scoped, NOT evidence-verified: conflict text is model-authored and
# is never checked against observed evidence.

def _three_candidate_envelope():
    primary = _proposal()
    defensive = _proposal("DEFENSIVE_ROTATION")
    defensive["target_allocations"][1].update(action="BUY", target_weight=30,
                                                allocation_change_percent=10)
    defensive["target_cash_weight"] = 70
    defensive["observed_evidence_refs"].append("symbol:BBB:pe_ratio")
    primary["additional_plans"] = [defensive]
    envelope = prepare_candidates(HOLDINGS, [], 200, primary)
    assert [(c["family"], c["eligibility_status"]) for c in envelope["candidates"]] == [
        ("HOLD", "ELIGIBLE"), ("RAISE_CASH", "ELIGIBLE"), ("DEFENSIVE_ROTATION", "ELIGIBLE")]
    return envelope


def _conflict_audit(envelope, conflicts):
    """Valid reviews for every candidate; conflicts keyed by candidate family."""
    audit = validate_candidate_reviews({"candidate_reviews": [
        {"candidate_id": c["id"], "supporting_refs": list(c["observed_evidence_refs"]),
         "opposing_refs": [], "material_conflicts": conflicts.get(c["family"], [])}
        for c in envelope["candidates"]]}, envelope)
    assert audit["status"] == "AVAILABLE"
    return audit


def _committee_choice(envelope, audit, family="RAISE_CASH", uncertainty=()):
    candidate = next(c for c in envelope["candidates"] if c["family"] == family)
    return candidate["id"], decide_selection(envelope, audit, {
        "selected_candidate_id": candidate["id"],
        "supporting_evidence_refs": [] if family == "HOLD" else ["symbol:AAA:signal"],
        "opposing_evidence_refs": [], "comparison_against_hold": "Preferred to the current portfolio.",
        "decision_rationale": "Observed evidence supports this candidate.",
        "material_uncertainty": list(uncertainty)})


def test_selected_candidate_conflict_vetoes_and_records_its_text():
    envelope = _three_candidate_envelope()
    audit = _conflict_audit(envelope, {"RAISE_CASH": ["Earnings data conflict"]})
    _, decision = _committee_choice(envelope, audit)
    assert (decision["state"], decision["selected_candidate_id"], decision["reason_codes"]) == (
        "SELECTED", "hold-current", ["CAUTIONED_HOLD"])
    assert decision["material_uncertainty"] == ["MATERIAL_CONFLICT_UNRESOLVED", "Earnings data conflict"]
    assert decision["supporting_evidence_refs"] == []


def test_duplicate_and_padded_conflicts_are_recorded_once():
    envelope = _three_candidate_envelope()
    audit = _conflict_audit(envelope, {"RAISE_CASH": ["Earnings data conflict", "  Earnings data conflict ",
                                                     "Earnings data conflict", "MATERIAL_CONFLICT_UNRESOLVED"]})
    _, decision = _committee_choice(envelope, audit)
    assert decision["material_uncertainty"] == ["MATERIAL_CONFLICT_UNRESOLVED", "Earnings data conflict"]


@pytest.mark.parametrize("family", ["HOLD", "DEFENSIVE_ROTATION"])
def test_conflict_on_hold_or_other_candidate_cannot_veto_selected_action(family):
    envelope = _three_candidate_envelope()
    text = "Technology sector 32.73% exceeds the advisory limit"
    audit = _conflict_audit(envelope, {family: [text]})
    selected_id, decision = _committee_choice(envelope, audit)
    assert (decision["state"], decision["selected_candidate_id"], decision["reason_codes"]) == (
        "SELECTED", selected_id, ["COMMITTEE_SELECTED"])
    # Another candidate's text is not attached to the selected plan...
    assert decision["material_uncertainty"] == []
    # ...and its original review record is preserved in candidate_audit.
    other_id = next(c["id"] for c in envelope["candidates"] if c["family"] == family)
    assert audit["reviews"][other_id]["material_conflicts"] == [text]


@pytest.mark.parametrize("conflicts", [[""], ["   "], ["\t\n"], ["", "  "], [None, 7, {"issue": "x"}]])
def test_blank_or_non_string_conflicts_cannot_veto(conflicts):
    envelope = _three_candidate_envelope()
    audit = validate_candidate_reviews({"candidate_reviews": [
        {"candidate_id": c["id"], "supporting_refs": list(c["observed_evidence_refs"]), "opposing_refs": [],
         "material_conflicts": conflicts if c["family"] == "RAISE_CASH" else []}
        for c in envelope["candidates"]]}, envelope)
    selected_id, decision = _committee_choice(envelope, audit)
    assert decision["selected_candidate_id"] == selected_id
    assert decision["material_uncertainty"] == []


def test_selected_candidate_missing_analysis_text_still_vetoes_known_b1_limitation():
    # B1 does not classify model text: a statement of missing information on the
    # selected candidate's own review still vetoes it (uncertainty, not proven conflict).
    envelope = _three_candidate_envelope()
    audit = _conflict_audit(envelope, {"RAISE_CASH": ["Missing timing analysis for AAA"]})
    _, decision = _committee_choice(envelope, audit)
    assert decision["selected_candidate_id"] == "hold-current"
    assert decision["material_uncertainty"] == ["MATERIAL_CONFLICT_UNRESOLVED", "Missing timing analysis for AAA"]


def test_hold_remains_selectable_despite_conflicts_and_records_only_its_own():
    envelope = _three_candidate_envelope()
    audit = _conflict_audit(envelope, {"HOLD": [" Hold leaves exposure unresolved ", "Shared note"],
                                       "RAISE_CASH": ["Earnings data conflict"],
                                       "DEFENSIVE_ROTATION": ["Valuation conflict"]})
    _, decision = _committee_choice(envelope, audit, family="HOLD", uncertainty=["Shared note"])
    assert (decision["state"], decision["selected_candidate_id"], decision["reason_codes"]) == (
        "SELECTED", "hold-current", ["COMMITTEE_SELECTED"])
    assert decision["material_uncertainty"] == ["Shared note", "Hold leaves exposure unresolved"]


def test_unknown_opposing_ref_still_fails_the_audit_closed():
    envelope = _three_candidate_envelope()
    audit = validate_candidate_reviews({"candidate_reviews": [
        {"candidate_id": c["id"], "supporting_refs": list(c["observed_evidence_refs"]),
         "opposing_refs": ["symbol:ZZZ:signal"] if c["family"] == "HOLD" else [], "material_conflicts": []}
        for c in envelope["candidates"]]}, envelope)
    assert (audit["status"], audit["reason"]) == ("UNAVAILABLE", "UNKNOWN_AUDITOR_REFERENCE")
    _, decision = _committee_choice(envelope, audit)
    assert (decision["selected_candidate_id"], decision["reason_codes"]) == ("hold-current", ["CAUTIONED_HOLD"])
    assert decision["material_uncertainty"] == ["UNKNOWN_AUDITOR_REFERENCE"]


def test_new_mode_ignores_forced_sell_when_committee_selects_hold(monkeypatch):
    replies = {
        "layer1": {"swaps": [], "top_buys": []},
        "layer2": {"allocations": [
            {"s": "AAA", "tw": 0, "sig": "SELL", "decision_basis": "INVESTMENT_THESIS"},
            {"s": "BBB", "tw": 20, "sig": "HOLD"}],
            "strategy_family": "RAISE_CASH", "observed_evidence_refs": ["symbol:AAA:signal"],
            "cash_balance_target": 80, "status": "REBALANCE"},
        "layer3": {"risk_flags": []},
        "committee": {"selected_candidate_id": "hold-current", "supporting_evidence_refs": [],
                      "opposing_evidence_refs": [], "comparison_against_hold": "Waiting is preferable.",
                      "decision_rationale": "Hold the current portfolio.", "material_uncertainty": []},
    }
    def fake_ai(prompt, *args, usage_layer, **kwargs):
        payload = replies[usage_layer]
        if usage_layer == "layer3":
            action_id = re.search(r"proposal-[0-9a-f]{12}", prompt).group()
            payload = {**payload, "candidate_reviews": [
                {"candidate_id": "hold-current", "supporting_refs": [], "opposing_refs": []},
                {"candidate_id": action_id, "supporting_refs": ["symbol:AAA:signal"], "opposing_refs": []}]}
        return {"text": json.dumps(payload), "latency_ms": 1}
    monkeypatch.setattr(optimizer, "call_ai", fake_ai)
    result = optimizer.run_layered_optimizer(
        HOLDINGS, [], "P", cash_balance=200,
        sector_policy_mode=SECTOR_POLICY_ADVISORY,
        optimizer_policy_mode=OPTIMIZER_POLICY_MUJI_V2,
        strategy_selection_mode=SELECTION_VERSION)
    assert result["strategy_selection"]["selected_candidate_id"] == "hold-current", result["strategic_candidates"].get("error_type")
    assert all(row["action"] == "HOLD" for row in result["target_allocations"])
    assert not result["swap_suggestions"]
    assert result["active_policy"]["strategy_selection_mode"] == SELECTION_VERSION


@pytest.mark.parametrize("chosen", ["action", "retry", "invalid", "auditor_down", "fallback", "locked", "cap"])
def test_pipeline_selection_and_degraded_paths(monkeypatch, chosen):
    action_id = None
    def fake_ai(prompt, *args, usage_layer, **kwargs):
        nonlocal action_id
        if usage_layer == "layer1":
            if chosen == "retry":
                raise RuntimeError("primary Strategist unavailable")
            payload = {"swaps": [], "top_buys": []}
        elif usage_layer == "layer1_retry":
            payload = {"swaps": [], "top_buys": []}
        elif usage_layer == "layer2":
            payload = {"allocations": [
                {"s": "AAA", "tw": 0, "sig": "SELL", "decision_basis": "INVESTMENT_THESIS"},
                {"s": "BBB", "tw": 20, "sig": "HOLD"}],
                "strategy_family": "RAISE_CASH", "observed_evidence_refs": ["symbol:AAA:signal"],
                "cash_balance_target": 80, "status": "REBALANCE"}
            if chosen == "cap":
                payload["allocations"][1].update(tw=30, sig="BUY")
                payload["strategy_family"] = "GROWTH_ROTATION"
                payload["cash_balance_target"] = 70
                payload["observed_evidence_refs"].append("symbol:BBB:pe_ratio")
            if chosen == "fallback":
                return {"text": "not-json", "latency_ms": 1}
        elif usage_layer == "layer3":
            if chosen == "auditor_down":
                raise RuntimeError("auditor unavailable")
            action_id = re.search(r"proposal-[0-9a-f]{12}", prompt).group()
            payload = {"risk_flags": [], "candidate_reviews": [
                {"candidate_id": "hold-current", "supporting_refs": [], "opposing_refs": []},
                {"candidate_id": action_id, "supporting_refs": ["symbol:AAA:signal"], "opposing_refs": []}]}
        elif usage_layer == "committee":
            payload = {"selected_candidate_id": action_id if chosen in ("action", "retry", "cap") else "unknown",
                       "supporting_evidence_refs": ["symbol:AAA:signal"],
                       "opposing_evidence_refs": [],
                       "comparison_against_hold": "Frozen SELL signal supports a risk reduction.",
                       "decision_rationale": "Raise cash on the independent SELL signal.",
                       "material_uncertainty": []}
        else:
            payload = {"allocations": [], "status": "NO_ACTION", "cash_balance_target": 20,
                       "risk_flags": []}
        return {"text": json.dumps(payload), "latency_ms": 1}
    monkeypatch.setattr(optimizer, "call_ai", fake_ai)
    holdings = [{**row, "allow_swap": False} if chosen == "locked" and row["symbol"] == "AAA" else row
                for row in HOLDINGS]
    execution = {"per_symbol": {"BBB": {"position_cap_pct": 25}}} if chosen == "cap" else None
    result = optimizer.run_layered_optimizer(
        holdings, [], "P", cash_balance=200, sector_policy_mode=SECTOR_POLICY_ADVISORY,
        optimizer_policy_mode=OPTIMIZER_POLICY_MUJI_V2,
        strategy_selection_mode=SELECTION_VERSION, execution_context=execution)
    selection = result["strategy_selection"]
    if chosen in ("action", "retry", "cap"):
        assert selection["selected_candidate_id"] == action_id
        assert result["target_allocations"][0]["action"] == "SELL"
        assert result["target_cash_weight"] == (70 if chosen == "cap" else 80)
        if chosen == "cap":
            assert selection["downstream_outcome"]["status"] == "ALTERED_BY_SAFEGUARDS"
            assert result["target_allocations"][1]["target_weight"] == 25
    else:
        assert selection["selected_candidate_id"] == "hold-current"
        assert all(row["action"] == "HOLD" for row in result["target_allocations"])
        if chosen == "locked":
            assert "MANDATORY_LOCK_CONFLICT" in result["strategic_candidates"]["candidates"][1]["eligibility_reasons"]
        else:
            assert selection["reason_codes"] == ["CAUTIONED_HOLD"]
    assert result["active_policy"]["strategy_selection_mode"] == SELECTION_VERSION
