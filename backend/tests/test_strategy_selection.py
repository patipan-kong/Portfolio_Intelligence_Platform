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


def test_auditor_conflict_is_recorded_and_invalid_committee_does_not_select_action():
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
    assert (decision["selected_candidate_id"], decision["reason_codes"]) == (
        envelope["candidates"][1]["id"], ["COMMITTEE_SELECTED", "AUDITOR_CONFLICT_UNVERIFIED"])
    assert decision["material_uncertainty"] == ["Earnings data conflict"]
    assert decide_selection(envelope, audit, {"selected_candidate_id": "invented"})["selected_candidate_id"] == "hold-current"
    assert decide_selection(envelope, audit, {"selected_candidate_id": []})["selected_candidate_id"] == "hold-current"


# ── Slice 4.6C: non-binding Auditor material conflicts (B2) ──────────────────
# Conflict text is model-authored and never checked against observed evidence,
# so it never vetoes a selection. The selected candidate's own text is recorded
# in material_uncertainty with AUDITOR_CONFLICT_UNVERIFIED; verifiable
# contradictions stay enforced by eligibility and hard safeguards.

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


SELECTED_WITH_CONFLICT = ["COMMITTEE_SELECTED", "AUDITOR_CONFLICT_UNVERIFIED"]


def test_selected_candidate_conflict_is_recorded_without_veto():
    envelope = _three_candidate_envelope()
    audit = _conflict_audit(envelope, {"RAISE_CASH": ["Earnings data conflict"]})
    selected_id, decision = _committee_choice(envelope, audit, uncertainty=["Committee note"])
    assert (decision["state"], decision["selected_candidate_id"], decision["reason_codes"]) == (
        "SELECTED", selected_id, SELECTED_WITH_CONFLICT)
    # Committee uncertainty first, then the Auditor's own text for this candidate.
    assert decision["material_uncertainty"] == ["Committee note", "Earnings data conflict"]
    assert decision["supporting_evidence_refs"] == ["symbol:AAA:signal"]


def test_duplicate_and_padded_conflicts_are_recorded_once():
    # Model text that imitates a reason code stays model text: it is recorded
    # verbatim as uncertainty and never becomes a reason code.
    envelope = _three_candidate_envelope()
    audit = _conflict_audit(envelope, {"RAISE_CASH": ["Earnings data conflict", "  Earnings data conflict ",
                                                     "Earnings data conflict", "MATERIAL_CONFLICT_UNRESOLVED"]})
    selected_id, decision = _committee_choice(envelope, audit, uncertainty=["Earnings data conflict"])
    assert (decision["selected_candidate_id"], decision["reason_codes"]) == (selected_id, SELECTED_WITH_CONFLICT)
    assert decision["material_uncertainty"] == ["Earnings data conflict", "MATERIAL_CONFLICT_UNRESOLVED"]


def test_selected_candidate_sector_advisory_text_cannot_veto():
    # Sector concentration is advisory under MUJI V2 and cannot block an action,
    # including through Auditor wording.
    envelope = _three_candidate_envelope()
    text = "Technology sector 32.73% exceeds the advisory limit"
    audit = _conflict_audit(envelope, {"DEFENSIVE_ROTATION": [text]})
    selected_id, decision = _committee_choice(envelope, audit, family="DEFENSIVE_ROTATION")
    assert (decision["state"], decision["selected_candidate_id"], decision["reason_codes"]) == (
        "SELECTED", selected_id, SELECTED_WITH_CONFLICT)
    assert decision["material_uncertainty"] == [text]


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
    assert (decision["selected_candidate_id"], decision["reason_codes"]) == (selected_id, ["COMMITTEE_SELECTED"])
    assert decision["material_uncertainty"] == []


def test_selected_candidate_missing_analysis_text_is_recorded_without_veto():
    # Text is not classified: a statement of missing information is recorded as
    # uncertainty, exactly like any other conflict text, and never vetoes.
    envelope = _three_candidate_envelope()
    audit = _conflict_audit(envelope, {"RAISE_CASH": ["Missing timing analysis for AAA"]})
    selected_id, decision = _committee_choice(envelope, audit)
    assert (decision["selected_candidate_id"], decision["reason_codes"]) == (selected_id, SELECTED_WITH_CONFLICT)
    assert decision["material_uncertainty"] == ["Missing timing analysis for AAA"]


def test_verifiable_contradiction_blocks_through_eligibility_without_auditor_text():
    # An observed SELL signal on a BUY row makes the candidate ineligible before
    # the Committee runs; the Auditor writing no conflict cannot make it selectable.
    observed = {"status": "OBSERVED", "source": "ANALYSIS_CACHE"}
    provenance = {symbol: {field: observed for field in ("signal", "fa_score", "ta_score", "timing_score")}
                  for symbol in ("AAA", "BBB")}
    plan = {"strategy_family": "GROWTH_ROTATION", "target_cash_weight": 10,
            "observed_evidence_refs": ["symbol:AAA:signal", "symbol:BBB:pe_ratio"],
            "target_allocations": [
                {"symbol": "AAA", "action": "BUY", "current_weight": 60, "target_weight": 70,
                 "allocation_change_percent": 10},
                {"symbol": "BBB", "action": "HOLD", "current_weight": 20, "target_weight": 20,
                 "allocation_change_percent": 0}]}
    envelope = prepare_candidates(HOLDINGS, [], 200, plan, provenance=provenance)
    growth = envelope["candidates"][1]
    assert growth["eligibility_status"] == "UNVERIFIED"
    assert "BUY_CONTRADICTS_SIGNAL:AAA" in growth["eligibility_reasons"]
    audit = _conflict_audit(envelope, {})
    assert all(review["material_conflicts"] == [] for review in audit["reviews"].values())
    _, decision = _committee_choice(envelope, audit, family="GROWTH_ROTATION")
    assert (decision["selected_candidate_id"], decision["reason_codes"]) == ("hold-current", ["CAUTIONED_HOLD"])
    assert decision["material_uncertainty"] == ["COMMITTEE_CANDIDATE_INVALID"]


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
        if chosen == "action":
            assert selection["reason_codes"] == ["COMMITTEE_SELECTED"]
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
        if chosen == "invalid":
            assert selection["material_uncertainty"] == ["COMMITTEE_CANDIDATE_INVALID"]
    assert result["active_policy"]["strategy_selection_mode"] == SELECTION_VERSION


# ── Phase 4.7: offline end-to-end selection in the production evidence mode ────
# The real run_layered_optimizer runs Candidate Discovery → Eligibility (incl. the
# hard-safeguard trial) → Auditor validation → Committee → Selection → Downstream.
# Only call_ai, the model boundary, is replaced. Evidence provenance is supplied
# as the production Committee path always does, so observed-signal rules run.

E2E_HOLDINGS = [
    {"symbol": "AAA", "shares": 60, "current_price": 10, "weight_pct": 60,
     "signal": "SELL", "fa_score": 30, "pe_ratio": 40},
    {"symbol": "BBB", "shares": 20, "current_price": 10, "weight_pct": 20,
     "signal": "ACCUMULATE", "fa_score": 70, "pe_ratio": 12},
]
_OBSERVED = {"status": "OBSERVED", "source": "ANALYSIS_CACHE", "as_of": "2026-11-01T00:00:00"}
E2E_PROVENANCE = {
    symbol: {"signal": _OBSERVED, "fa_score": _OBSERVED, "ta_score": _OBSERVED,
             "timing_score": {"status": "MISSING", "source": "TIMING_INTELLIGENCE"}}
    for symbol in ("AAA", "BBB")
}
E2E_OPT_IN = {"sector_policy_mode": SECTOR_POLICY_ADVISORY,
              "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2,
              "strategy_selection_mode": SELECTION_VERSION}
RAISE_CASH_PLAN = {
    "allocations": [{"s": "AAA", "tw": 0, "sig": "SELL", "decision_basis": "INVESTMENT_THESIS"},
                    {"s": "BBB", "tw": 20, "sig": "HOLD"}],
    "strategy_family": "RAISE_CASH", "observed_evidence_refs": ["symbol:AAA:signal"],
    "cash_balance_target": 80, "status": "REBALANCE"}
# Valuation support is cited, but AAA's observed signal is SELL.
BUY_AGAINST_SELL_PLAN = {
    "allocations": [{"s": "AAA", "tw": 70, "sig": "BUY"}, {"s": "BBB", "tw": 20, "sig": "HOLD"}],
    "strategy_family": "GROWTH_ROTATION", "observed_evidence_refs": ["symbol:AAA:pe_ratio"],
    "cash_balance_target": 10, "status": "REBALANCE"}
# Supported by BBB's observed ACCUMULATE signal; leaves 10% cash.
BUY_BBB_PLAN = {
    "allocations": [{"s": "AAA", "tw": 60, "sig": "HOLD"}, {"s": "BBB", "tw": 30, "sig": "BUY"}],
    "strategy_family": "GROWTH_ROTATION", "observed_evidence_refs": ["symbol:BBB:signal"],
    "cash_balance_target": 10, "status": "REBALANCE"}
UNKNOWN_CANDIDATE_ID = "proposal-000000000000"
ALL_HOLD = [("AAA", "HOLD", 60), ("BBB", "HOLD", 20)]


def _no_committee(ids):
    pytest.fail("the Committee must not be called")


def _run_e2e(monkeypatch, plan, *, pick=_no_committee, reviews=None, **kwargs):
    """Run the real orchestrator offline; return (result, model calls, reviewed IDs).

    The Auditor reviews every candidate in prompt order and cites the plan's refs
    for the primary proposal; ``reviews`` may rewrite that list. ``pick`` maps the
    reviewed IDs to the Committee's choice.
    """
    calls, ids = [], []

    def fake_ai(prompt, *args, usage_layer, **kw):
        calls.append(usage_layer)
        if usage_layer == "layer1":
            payload = {"swaps": [], "top_buys": []}
        elif usage_layer == "layer2":
            payload = plan
        elif usage_layer == "layer3":
            ids[:] = re.findall(r'"candidate_id": "([^"]+)"', prompt)
            items = [{"candidate_id": cid,
                      "supporting_refs": list(plan["observed_evidence_refs"]) if index == 1 else [],
                      "opposing_refs": [], "material_conflicts": [], "assessment": "Model view"}
                     for index, cid in enumerate(ids)]
            payload = {"risk_flags": [], "candidate_reviews": reviews(items) if reviews else items}
        elif usage_layer == "committee":
            chosen = pick(ids)
            payload = {"selected_candidate_id": chosen,
                       "supporting_evidence_refs": ([] if chosen == "hold-current"
                                                    else list(plan["observed_evidence_refs"])),
                       "opposing_evidence_refs": [],
                       "comparison_against_hold": "Observed evidence favours this over waiting.",
                       "decision_rationale": "Act on the observed evidence.",
                       "material_uncertainty": []}
        else:
            pytest.fail(f"unexpected model call: {usage_layer}")
        return {"text": json.dumps(payload), "latency_ms": 1}

    monkeypatch.setattr(optimizer, "call_ai", fake_ai)
    result = optimizer.run_layered_optimizer(
        [dict(row) for row in E2E_HOLDINGS], [], "P", cash_balance=200,
        evidence_provenance=E2E_PROVENANCE, **E2E_OPT_IN, **kwargs)
    assert result["strategic_candidates"]["evidence_provenance_status"] == "SUPPLIED"
    assert result["active_policy"]["strategy_selection_mode"] == SELECTION_VERSION
    return result, calls, ids


def _rows(result):
    return [(row["symbol"], row["action"], row["target_weight"]) for row in result["target_allocations"]]


def _assert_cautioned_hold(result, cause):
    selection = result["strategy_selection"]
    assert (selection["state"], selection["selected_candidate_id"]) == ("SELECTED", "hold-current")
    assert selection["reason_codes"] == ["CAUTIONED_HOLD"]
    assert selection["material_uncertainty"] == [cause]
    assert _rows(result) == ALL_HOLD


def test_e2e_committee_selects_eligible_action(monkeypatch):
    result, calls, ids = _run_e2e(monkeypatch, RAISE_CASH_PLAN, pick=lambda ids: ids[1])
    action = result["strategic_candidates"]["candidates"][1]
    selection = result["strategy_selection"]
    assert calls == ["layer1", "layer2", "layer3", "committee"]
    assert (action["id"], action["family"], action["eligibility_status"]) == (ids[1], "RAISE_CASH", "ELIGIBLE")
    assert result["candidate_audit"]["status"] == "AVAILABLE"
    assert (selection["state"], selection["selected_candidate_id"]) == ("SELECTED", action["id"])
    assert selection["reason_codes"] == ["COMMITTEE_SELECTED"]
    assert selection["material_uncertainty"] == []
    assert selection["downstream_outcome"] == {"status": "UNCHANGED"}
    assert _rows(result) == [("AAA", "SELL", 0), ("BBB", "HOLD", 20)]
    assert result["target_cash_weight"] == 80


def test_e2e_selected_action_auditor_conflicts_are_recorded_not_binding(monkeypatch):
    conflicts = ["Earnings data conflict", "  Earnings data conflict ", "", "Earnings data conflict"]

    def with_conflicts(items):
        items[1]["material_conflicts"] = list(conflicts)
        return items

    result, calls, ids = _run_e2e(monkeypatch, RAISE_CASH_PLAN, reviews=with_conflicts,
                                  pick=lambda ids: ids[1])
    selection = result["strategy_selection"]
    assert "committee" in calls
    assert (selection["state"], selection["selected_candidate_id"]) == ("SELECTED", ids[1])
    assert selection["reason_codes"] == ["COMMITTEE_SELECTED", "AUDITOR_CONFLICT_UNVERIFIED"]
    assert selection["material_uncertainty"] == ["Earnings data conflict"]
    assert result["candidate_audit"]["status"] == "AVAILABLE"
    assert result["candidate_audit"]["reviews"][ids[1]]["material_conflicts"] == conflicts
    assert result["candidate_audit"]["reviews"]["hold-current"]["material_conflicts"] == []
    assert _rows(result) == [("AAA", "SELL", 0), ("BBB", "HOLD", 20)]


def test_e2e_buy_against_observed_sell_signal_is_never_selectable(monkeypatch):
    result, calls, _ = _run_e2e(monkeypatch, BUY_AGAINST_SELL_PLAN)
    action = result["strategic_candidates"]["candidates"][1]
    assert (action["family"], action["eligibility_status"]) == ("GROWTH_ROTATION", "UNVERIFIED")
    assert action["eligibility_reasons"] == ["BUY_CONTRADICTS_SIGNAL:AAA"]
    assert "committee" not in calls
    _assert_cautioned_hold(result, "NO_ELIGIBLE_ACTION")


def test_e2e_high_volatility_cash_floor_makes_candidate_ineligible(monkeypatch):
    # The same plan is ELIGIBLE without the regime (see the execution-cap test).
    result, calls, _ = _run_e2e(monkeypatch, BUY_BBB_PLAN,
                                regime_context={"regime": "HIGH_VOLATILITY", "confidence_pct": 85})
    action = result["strategic_candidates"]["candidates"][1]
    assert action["eligibility_status"] == "INELIGIBLE"
    assert action["eligibility_reasons"] == ["HARD_SAFEGUARD_CONFLICT"]
    assert "committee" not in calls
    _assert_cautioned_hold(result, "NO_ELIGIBLE_ACTION")


def test_e2e_unknown_review_substituted_for_required_review_fails_closed(monkeypatch):
    def substitute(items):
        return [items[0], {**items[1], "candidate_id": UNKNOWN_CANDIDATE_ID}]

    result, calls, ids = _run_e2e(monkeypatch, RAISE_CASH_PLAN, reviews=substitute)
    assert UNKNOWN_CANDIDATE_ID not in ids
    audit = result["candidate_audit"]
    assert (audit["status"], audit["reason"]) == ("UNAVAILABLE", "INCOMPLETE_AUDITOR_COVERAGE")
    assert "committee" not in calls
    _assert_cautioned_hold(result, "INCOMPLETE_AUDITOR_COVERAGE")


def test_e2e_extra_unknown_review_is_ignored_when_coverage_is_complete(monkeypatch):
    # Pins current behaviour (Phase 4.7 D1): an extra review for an unknown candidate
    # is dropped and never reaches the Committee or the selection.
    def add_unknown(items):
        return items + [{**items[1], "candidate_id": UNKNOWN_CANDIDATE_ID}]

    result, calls, ids = _run_e2e(monkeypatch, RAISE_CASH_PLAN, reviews=add_unknown,
                                  pick=lambda ids: ids[1])
    audit = result["candidate_audit"]
    assert UNKNOWN_CANDIDATE_ID not in ids
    assert (audit["status"], audit["reason"]) == ("AVAILABLE", None)
    assert set(audit["reviews"]) == set(ids)
    assert "committee" in calls
    assert result["strategy_selection"]["selected_candidate_id"] == ids[1]
    assert result["strategy_selection"]["reason_codes"] == ["COMMITTEE_SELECTED"]


def test_e2e_committee_choosing_ineligible_candidate_falls_back_to_hold(monkeypatch):
    plan = {**RAISE_CASH_PLAN, "additional_plans": [BUY_AGAINST_SELL_PLAN]}
    result, calls, ids = _run_e2e(monkeypatch, plan, pick=lambda ids: ids[2])
    candidates = result["strategic_candidates"]["candidates"]
    assert [c["id"] for c in candidates] == ids
    assert candidates[1]["eligibility_status"] == "ELIGIBLE"
    assert (candidates[2]["family"], candidates[2]["eligibility_status"]) == ("GROWTH_ROTATION", "UNVERIFIED")
    assert candidates[2]["eligibility_reasons"] == ["BUY_CONTRADICTS_SIGNAL:AAA"]
    assert calls[-1] == "committee"
    _assert_cautioned_hold(result, "COMMITTEE_CANDIDATE_INVALID")


def test_e2e_execution_cap_alters_selected_plan_downstream(monkeypatch):
    # Real downstream path: the 15% cap leaves BBB's BUY below its 20% weight and
    # MUJI V2 relabelling turns it into HOLD. The record stays SELECTED /
    # COMMITTEE_SELECTED with ALTERED_BY_SAFEGUARDS (current behaviour; D3 deferred).
    result, calls, ids = _run_e2e(monkeypatch, BUY_BBB_PLAN, pick=lambda ids: ids[1],
                                  execution_context={"per_symbol": {"BBB": {"position_cap_pct": 15}}})
    action = result["strategic_candidates"]["candidates"][1]
    selection = result["strategy_selection"]
    assert action["eligibility_status"] == "ELIGIBLE"
    assert "committee" in calls
    assert (selection["state"], selection["selected_candidate_id"]) == ("SELECTED", ids[1])
    assert selection["reason_codes"] == ["COMMITTEE_SELECTED"]
    downstream = selection["downstream_outcome"]
    assert downstream["status"] == "ALTERED_BY_SAFEGUARDS"
    assert downstream["original"] == {"AAA": ("HOLD", 60), "BBB": ("BUY", 30)}
    assert downstream["result"] == {"AAA": ("HOLD", 60), "BBB": ("HOLD", 20)}
    assert _rows(result) == ALL_HOLD
    bbb = result["target_allocations"][1]
    assert (bbb["original_action"], bbb["execution_capped"]) == ("BUY", True)


def test_e2e_committee_selects_hold(monkeypatch):
    result, calls, _ = _run_e2e(monkeypatch, RAISE_CASH_PLAN, pick=lambda ids: "hold-current")
    selection = result["strategy_selection"]
    assert "committee" in calls
    assert (selection["state"], selection["selected_candidate_id"]) == ("SELECTED", "hold-current")
    assert selection["reason_codes"] == ["COMMITTEE_SELECTED"]
    assert selection["downstream_outcome"] == {"status": "UNCHANGED"}
    assert _rows(result) == ALL_HOLD
