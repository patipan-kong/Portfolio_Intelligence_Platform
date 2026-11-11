"""MUJI V2 Phase 4 Slice 4.1 — Auditor candidate-review contract.

Opt-in OFF L3 prompts are compared byte-for-byte against a golden fixture
captured from baseline aada754 (before this slice) with the same inputs.
Regenerate only deliberately: REGENERATE_L3_BASELINE=1 on baseline code.
"""

import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import agents.optimizer as optimizer
from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY
from services.optimizer import strategic_candidates as sc
from services.optimizer.strategic_candidates import (
    SELECTION_VERSION, prepare_candidates, validate_candidate_reviews, decide_selection,
)

GOLDEN = os.path.join(os.path.dirname(__file__), "fixtures", "l3_prompt_optin_off_baseline.json")

HOLDINGS = [
    {"symbol": "AAA", "shares": 60, "current_price": 10, "weight_pct": 60,
     "signal": "SELL", "fa_score": 30, "ta_score": -1, "pe_ratio": 40},
    {"symbol": "BBB", "shares": 20, "current_price": 10, "weight_pct": 20,
     "signal": "ACCUMULATE", "fa_score": 70, "pe_ratio": 12, "roe": 0.2},
]
WATCHLIST = [
    {"symbol": "WWW", "current_price": 5, "signal": "BUY", "fa_score": 60, "pe_ratio": 9},
    {"symbol": "ZZZ", "current_price": 5, "signal": "WATCH", "fa_score": 10},
]
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


def _run(monkeypatch, layer3_reply=None, **kwargs):
    """Run the real layered pipeline offline; return (result, captured prompts and budgets)."""
    captured = {}

    def fake_ai(prompt, provider, model, *args, usage_layer, max_tokens=None, **kw):
        captured[usage_layer] = {"prompt": prompt, "max_tokens": max_tokens}
        if usage_layer == "layer1":
            payload = {"swaps": [], "top_buys": []}
        elif usage_layer == "layer2":
            payload = L2_REPLY
        elif usage_layer == "layer3":
            payload = layer3_reply(prompt) if layer3_reply else {"risk_flags": []}
        elif usage_layer == "committee":
            payload = {"selected_candidate_id": "hold-current", "supporting_evidence_refs": [],
                       "opposing_evidence_refs": [], "comparison_against_hold": "Waiting is preferable.",
                       "decision_rationale": "Hold the current portfolio.", "material_uncertainty": []}
        else:
            payload = {"allocations": [], "status": "NO_ACTION", "risk_flags": []}
        return {"text": json.dumps(payload), "latency_ms": 1}

    monkeypatch.setattr(optimizer, "call_ai", fake_ai)
    result = optimizer.run_layered_optimizer(
        HOLDINGS, WATCHLIST, "P", cash_balance=200, regime_context=REGIME, **kwargs)
    return result, captured


# ── Opt-in OFF: byte-for-byte preservation ───────────────────────────────────

@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_optin_off_l3_prompt_matches_baseline(monkeypatch, name):
    _, captured = _run(monkeypatch, **SCENARIOS[name])
    layer3 = captured["layer3"]
    if os.environ.get("REGENERATE_L3_BASELINE"):
        data = json.load(open(GOLDEN, encoding="utf-8")) if os.path.exists(GOLDEN) else {}
        data[name] = layer3
        with open(GOLDEN, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
    baseline = json.load(open(GOLDEN, encoding="utf-8"))[name]
    assert layer3["prompt"] == baseline["prompt"]
    assert layer3["max_tokens"] == baseline["max_tokens"]
    assert "candidate_reviews" not in layer3["prompt"]
    assert "committee" not in captured


# ── Opt-in ON: schema, placement, compact evidence, budget ───────────────────

OPT_IN = {"sector_policy_mode": SECTOR_POLICY_ADVISORY,
          "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2,
          "strategy_selection_mode": SELECTION_VERSION}


def _ids(prompt):
    return re.findall(r'"candidate_id": "([^"]+)"', prompt)


def _complete_reviews(prompt):
    return {"risk_flags": [], "candidate_reviews": [
        {"candidate_id": cid, "supporting_refs": ["symbol:AAA:signal"] if cid != "hold-current" else [],
         "opposing_refs": [], "material_conflicts": [], "assessment": "Model view"}
        for cid in _ids(prompt)]}


def test_optin_l3_schema_requires_candidate_reviews_before_output_instruction(monkeypatch):
    _, captured = _run(monkeypatch, layer3_reply=_complete_reviews, **OPT_IN)
    prompt = captured["layer3"]["prompt"]
    review_at = prompt.index("[STRATEGIC CANDIDATE REVIEW — REQUIRED FOR THIS RUN]")
    output_at = prompt.index("Return JSON only. No markdown fences.")
    schema = prompt[output_at:]
    assert review_at < output_at
    assert prompt.index("CANDIDATES_FOR_REVIEW=") < output_at
    assert '"candidate_reviews": [{"candidate_id":"exact candidate_id"' in schema
    assert schema.index('"candidate_reviews"') < schema.index('"risk_flags"')
    # Nothing is appended after the JSON schema any more.
    assert prompt.endswith('"auditor_notes": "1-2 sentences."\n}')
    # Compact view, not the full envelope: unrelated catalog rows are absent.
    assert "observed_evidence_catalog" not in prompt
    assert "symbol:ZZZ:" not in prompt and "symbol:WWW:" not in prompt
    ids = _ids(prompt)
    assert len(ids) == 2 and ids[0] == "hold-current" and ids[1].startswith("proposal-")
    assert captured["layer3"]["max_tokens"] == optimizer._LAYER3_SELECTION_MAX_TOKENS == 4096
    assert captured["committee"]["max_tokens"] == 2048


def test_valid_reviews_make_audit_available_without_forcing_action(monkeypatch):
    result, captured = _run(monkeypatch, layer3_reply=_complete_reviews, **OPT_IN)
    assert result["candidate_audit"]["status"] == "AVAILABLE"
    assert set(result["candidate_audit"]["reviews"]) == set(_ids(captured["layer3"]["prompt"]))
    assert "committee" in captured
    # The Committee still decides: a valid audit does not imply a non-HOLD selection.
    assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"
    assert result["strategy_selection"]["reason_codes"] == ["COMMITTEE_SELECTED"]


def _drop_action(prompt):
    reply = _complete_reviews(prompt)
    reply["candidate_reviews"] = [r for r in reply["candidate_reviews"] if r["candidate_id"] == "hold-current"]
    return reply


def _unknown_ref(prompt):
    reply = _complete_reviews(prompt)
    reply["candidate_reviews"][0]["opposing_refs"] = ["symbol:AAA:invented"]
    return reply


def _duplicate(prompt):
    reply = _complete_reviews(prompt)
    reply["candidate_reviews"].append(dict(reply["candidate_reviews"][0]))
    return reply


TRUNCATED = '{"risk_flags": [], "candidate_reviews": [{"candidate_id": "hold-'


@pytest.mark.parametrize("reply, reason", [
    (lambda p: {"risk_flags": []}, "AUDITOR_REVIEWS_MISSING"),
    (lambda p: {"risk_flags": [], "candidate_reviews": "none"}, "AUDITOR_REVIEWS_MISSING"),
    (lambda p: TRUNCATED, "AUDITOR_REVIEWS_MISSING"),
    (_drop_action, "INCOMPLETE_AUDITOR_COVERAGE"),
    (_unknown_ref, "UNKNOWN_AUDITOR_REFERENCE"),
    (_duplicate, "DUPLICATE_AUDITOR_REVIEW"),
], ids=["absent", "not-a-list", "truncated-json", "incomplete", "unknown-ref", "duplicate"])
def test_missing_incomplete_or_invalid_reviews_fail_closed(monkeypatch, reply, reason):
    result, captured = _run(monkeypatch, layer3_reply=reply, **OPT_IN)
    audit = result["candidate_audit"]
    assert audit["status"] == "UNAVAILABLE" and audit["reason"] == reason
    assert "committee" not in captured
    selection = result["strategy_selection"]
    assert selection["selected_candidate_id"] == "hold-current"
    assert selection["reason_codes"] == ["CAUTIONED_HOLD"]
    assert selection["material_uncertainty"] == [reason]
    assert all(row["action"] == "HOLD" for row in result["target_allocations"])


# ── Concurrent failure causes ────────────────────────────────────────────────

def test_concurrent_causes_recorded_in_pipeline(monkeypatch):
    # Selling BBB contradicts its frozen ACCUMULATE signal, so no action is eligible.
    monkeypatch.setitem(L2_REPLY, "allocations", [
        {"s": "AAA", "tw": 60, "sig": "HOLD"},
        {"s": "BBB", "tw": 0, "sig": "SELL", "decision_basis": "INVESTMENT_THESIS"}])
    monkeypatch.setitem(L2_REPLY, "observed_evidence_refs", ["symbol:BBB:pe_ratio"])
    result, captured = _run(monkeypatch, layer3_reply=lambda p: {"risk_flags": []}, **OPT_IN)
    action = result["strategic_candidates"]["candidates"][1]
    assert action["eligibility_status"] != "ELIGIBLE"
    assert result["strategy_selection"]["material_uncertainty"] == ["NO_ELIGIBLE_ACTION", "AUDITOR_REVIEWS_MISSING"]
    assert result["strategy_selection"]["selected_candidate_id"] == "hold-current"
    assert "committee" not in captured


def test_concurrent_causes_are_deduplicated_deterministically():
    envelope = prepare_candidates(HOLDINGS, [], 200, {})
    both = decide_selection(envelope, {"status": "UNAVAILABLE", "reason": "AUDITOR_REVIEWS_MISSING"},
                            None, failure_reason="NO_ELIGIBLE_ACTION")
    assert both["material_uncertainty"] == ["NO_ELIGIBLE_ACTION", "AUDITOR_REVIEWS_MISSING"]
    same = decide_selection(envelope, {"status": "UNAVAILABLE", "reason": "NO_ELIGIBLE_ACTION"},
                            None, failure_reason="NO_ELIGIBLE_ACTION")
    assert same["material_uncertainty"] == ["NO_ELIGIBLE_ACTION"]
    no_audit = decide_selection(envelope, None, None, failure_reason="NO_ELIGIBLE_ACTION")
    assert no_audit["material_uncertainty"] == ["NO_ELIGIBLE_ACTION", "AUDITOR_UNAVAILABLE"]
    audit_ok = {"status": "AVAILABLE", "reason": None, "reviews": {}}
    only_failure = decide_selection(envelope, audit_ok, None, failure_reason="NO_ELIGIBLE_ACTION")
    assert only_failure["material_uncertainty"] == ["NO_ELIGIBLE_ACTION"]
    for decision in (both, same, no_audit, only_failure):
        assert decision["state"] == "SELECTED" and decision["reason_codes"] == ["CAUTIONED_HOLD"]


# ── Compact evidence view ────────────────────────────────────────────────────

GOALS = {"contract_version": "g.v1", "goals": [
    {"id": "g1", "target_date": "2030-01-01", "funding_gap": 1000, "priority": 1}]}


def _envelope():
    plan = {"strategy_family": "RAISE_CASH", "target_cash_weight": 80,
            "observed_evidence_refs": ["symbol:AAA:signal", "symbol:WWW:signal", "regime:regime"],
            "target_allocations": [
                {"symbol": "AAA", "action": "SELL", "current_weight": 60, "target_weight": 0,
                 "allocation_change_percent": -60, "decision_basis": "INVESTMENT_THESIS"},
                {"symbol": "BBB", "action": "REDUCE", "current_weight": 20, "target_weight": 0,
                 "allocation_change_percent": -20, "decision_basis": "INVESTMENT_THESIS"}]}
    return prepare_candidates(HOLDINGS, WATCHLIST, 200, plan, regime=REGIME, goals=GOALS)


def test_compact_view_keeps_identity_actions_refs_and_contradictions():
    envelope = _envelope()
    before = json.dumps(envelope, sort_keys=True, default=str)
    view = sc.candidate_review_view(envelope)
    assert json.dumps(envelope, sort_keys=True, default=str) == before  # no mutation
    by_id = {c["candidate_id"]: c for c in view["candidates"]}
    assert list(by_id) == [c["id"] for c in envelope["candidates"]]
    action = next(c for c in envelope["candidates"] if c["id"] != "hold-current")
    compact = by_id[action["id"]]
    assert compact["family"] == "RAISE_CASH"
    assert [(r["symbol"], r["action"], r["target_weight"]) for r in compact["proposed_allocations"]] == [
        ("AAA", "SELL", 0), ("BBB", "REDUCE", 0)]
    assert compact["cited_refs"] == action["observed_evidence_refs"]
    assert compact["eligibility_status"] == action["eligibility_status"]
    assert compact["missing_information"] == action["missing_information"]
    assert "UNVERIFIED_SELL:BBB" in compact["missing_information"]
    evidence = view["relevant_evidence"]
    # Contradictory frozen fact for a proposed sale travels with the support.
    assert evidence["symbol:BBB:signal"] == "ACCUMULATE"
    assert evidence["symbol:BBB:fa_score"] == 70
    assert evidence["regime:regime"] == "HIGH_VOLATILITY"
    assert evidence["goal:g1:funding_gap"] == 1000
    # A cited fact outside the allocations is kept for traceability; unrelated rows are not.
    assert evidence["symbol:WWW:signal"] == "BUY"
    assert "symbol:WWW:fa_score" not in evidence
    assert not any(key.startswith("symbol:ZZZ:") for key in evidence)
    catalog = envelope["observed_evidence_catalog"]
    assert all(catalog[key] == value for key, value in evidence.items())  # verbatim, nothing invented
    assert view["catalog_entry_count"] == len(catalog)
    assert view["omitted_unrelated_entry_count"] == len(catalog) - len(evidence)
    assert sc._symbol_of_ref("symbol:AA:signal") == "AA" and sc._symbol_of_ref("regime:regime") is None


def test_compact_view_is_deterministic_and_missing_evidence_stays_missing():
    envelope = _envelope()
    shuffled = {**envelope, "observed_evidence_catalog":
                dict(reversed(list(envelope["observed_evidence_catalog"].items())))}
    assert json.dumps(sc.candidate_review_view(envelope), sort_keys=True) == \
        json.dumps(sc.candidate_review_view(shuffled), sort_keys=True)
    # AAA has no roe in the frozen inputs; the view must not supply one.
    assert "symbol:AAA:roe" not in sc.candidate_review_view(envelope)["relevant_evidence"]
    hold = sc.candidate_review_view(envelope)["candidates"][0]
    assert hold["candidate_id"] == "hold-current" and hold["cited_refs"] == {}


def test_reviews_still_validate_against_full_frozen_catalog():
    envelope = _envelope()
    reviews = [{"candidate_id": c["id"], "supporting_refs": [], "opposing_refs": ["symbol:ZZZ:signal"]}
               for c in envelope["candidates"]]
    # An omitted-but-frozen fact remains a valid opposing reference.
    assert validate_candidate_reviews({"candidate_reviews": reviews}, envelope)["status"] == "AVAILABLE"
    reviews[0]["opposing_refs"] = ["symbol:ZZZ:invented"]
    assert validate_candidate_reviews({"candidate_reviews": reviews}, envelope)["reason"] == "UNKNOWN_AUDITOR_REFERENCE"
