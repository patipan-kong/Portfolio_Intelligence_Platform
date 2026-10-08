"""Offline evidence/interpretation regressions; no DB or model/provider calls."""
import copy
import json

import pytest

from agents.optimizer import _consensus_engine, _layer3_prompt, _make_envelope_from_dict
from services.optimizer.auditor_claims import build_claim_evidence, validate_auditor_claims
from services.optimizer.policy_engine import compute_policy_alignment_score


def contract(action="HOLD", cap=15, target=16.03):
    allocations = [{"symbol": "BH.BK", "action": "HOLD", "current_weight": 15.31, "target_weight": 15.31},
                   {"symbol": "MICRON01.BK", "action": action, "current_weight": 16.03, "target_weight": target}]
    context = {"per_symbol": {"BH.BK": {"position_cap_pct": None},
                              "MICRON01.BK": {"position_cap_pct": cap}}, "dr_portfolio_cap": 40}
    return build_claim_evidence(allocations, [], context)


def flag(kind=None, symbol="MICRON01.BK", ref=None):
    return {"symbol": symbol, "severity": "HIGH", "category": "INVESTMENT_RISK",
            "issue": "Position exceeds 15% max cap for single stock", "claim_kind": kind, "evidence_ref": ref}


def interpret(flags, evidence=None):
    return validate_auditor_claims({"risk_flags": flags, "final_risk_level": "high", "safer_choice": "neither",
        "auditor_notes": "Universal 15% limit breached"}, evidence or contract())


def test_bh_has_no_execution_cap_or_universal_15_percent_limit():
    c = contract()
    assert all(e.get("symbol") != "BH.BK" for e in c["evidence"].values())
    r = interpret([flag("EXECUTION_RESTRICTION", "BH.BK", "execution:1")], c)
    assert not r["risk_flags"] and r["claim_reviews"][0]["validation_status"] == "UNSUPPORTED"


def test_micron_hold_exposure_is_not_a_liquidation_requirement():
    r = interpret([flag("EXISTING_EXPOSURE", ref="execution:1")])
    assert not r["risk_flags"] and not r["claim_reviews"][0]["scoring_eligible"]
    assert "does not require liquidation" in r["claim_reviews"][0]["issue"]
    assert interpret([flag("EXECUTION_RESTRICTION", ref="execution:1")])["risk_flags"] == []


@pytest.mark.parametrize("cap", [15, 10])
@pytest.mark.parametrize("action", ["BUY", "ACCUMULATE"])
def test_proposed_buy_exceeds_existing_applicable_cap(cap, action):
    c = contract(action, cap)
    r = interpret([flag("EXECUTION_RESTRICTION", ref="execution:1")], c)
    assert r["risk_flags"][0]["validation_status"] == "VERIFIED"
    assert r["risk_flags"][0]["provenance"]["allowed_pct"] == cap
    assert "max cap for single stock" not in r["risk_flags"][0]["issue"]


def test_actual_general_policy_breach_uses_existing_calculator():
    policy = {"hard_constraints": {"max_single_position_pct": 25, "min_cash_pct": 3,
        "max_sector_pct": 70, "max_turnover_pct": 70, "max_new_positions": 3}}
    allocations = [{"symbol": "BH.BK", "action": "HOLD", "current_weight": 26, "target_weight": 26}]
    details = compute_policy_alignment_score(allocations, _make_envelope_from_dict(policy), 100000)[4]
    c = build_claim_evidence(allocations, details, {})
    r = interpret([flag("POLICY_BREACH", "BH.BK", "policy:0")], c)
    assert r["risk_flags"][0]["provenance"]["allowed_pct"] == 25
    assert r["risk_flags"][0]["scoring_eligible"]


def test_basket_guidance_is_advisory_not_a_policy_violation():
    r = interpret([flag("ADVISORY_CONCERN"), flag("POLICY_BREACH", ref="basket_guidance")])
    assert not r["risk_flags"]
    assert [f["validation_status"] for f in r["claim_reviews"]] == ["ADVISORY", "UNSUPPORTED"]


def test_independent_evidence_retained_and_model_only_opinion_visible_unscored():
    opinion = {**flag("INVESTMENT_JUDGMENT"), "issue": "Cyclical earnings and valuation downside", "severity": "MEDIUM"}
    c = build_claim_evidence([{"symbol": "MICRON01.BK", "action": "BUY"}], [], {},
        {"MICRON01.BK": {"timing_score": 20, "execution_priority": "DEFER", "timing_data_available": True}})
    observed = flag("INVESTMENT_JUDGMENT", ref="risk:ENTRY_TIMING:MICRON01.BK")
    r = interpret([flag(), opinion, observed], c)
    assert r["risk_flags"][0]["validation_status"] == "VERIFIED"
    assert r["risk_flags"][0]["severity"] == "MEDIUM"  # Existing timing rule, not model HIGH.
    assert "timing" in r["risk_flags"][0]["issue"]
    assert r["claim_reviews"][1]["issue"] == opinion["issue"]
    assert r["claim_reviews"][1]["validation_status"] == "MODEL_OPINION"
    assert _consensus_engine({}, {}, r)["risk_alignment_score"] == 72
    assert _consensus_engine({}, {}, interpret([flag()]))["risk_alignment_score"] == 92


def test_frozen_dogfood_218_replay_does_not_rewrite_evidence():
    # Exact two flags from frozen history 218; missing typed references fail closed.
    frozen = {"risk_flags": [{k: v for k, v in flag(symbol=s).items()
        if k not in ("claim_kind", "evidence_ref")} for s in ["BH.BK", "MICRON01.BK"]],
        "final_risk_level": "medium", "safer_choice": "layer2"}
    before = copy.deepcopy(frozen)
    r = validate_auditor_claims(frozen, contract())
    assert frozen == before and r["raw_model_output"] == before
    assert [f["validation_status"] for f in r["claim_reviews"]] == ["UNSUPPORTED", "UNSUPPORTED"]
    assert _consensus_engine({}, {}, frozen)["risk_alignment_score"] == 92  # Raw model flags have no authority.
    assert _consensus_engine({}, {}, r)["risk_alignment_score"] == 92  # replay, not historical score


def test_prompt_and_api_provenance_contract():
    prompt = _layer3_prompt({}, {}, claim_contract=contract())
    assert "never a universal holding limit" in prompt and "INVESTMENT_JUDGMENT" in prompt
    r = interpret([flag("INVESTMENT_JUDGMENT")])
    assert json.loads(json.dumps(r))["claim_reviews"][0]["provenance"].startswith("No matching independently")


@pytest.mark.parametrize("label", ["DETERMINISTIC_POLICY", "INVESTMENT_JUDGMENT", "ADVISORY_GUIDANCE",
                                   "OWNER_INTENT_REVIEW", None, "UNKNOWN"])
@pytest.mark.parametrize("label_field", ["category", "claim_kind"])
def test_unsupported_cap_claims_have_no_authority_under_any_label(label, label_field):
    flags = [{**flag("INVESTMENT_JUDGMENT", symbol=s), label_field: label,
              "scoring_eligible": True, "validation_status": "VERIFIED"}
             for s in ("BH.BK", "MICRON01.BK")]
    r = interpret(flags)
    score = _consensus_engine({}, {}, r)
    assert score["risk_alignment_score"] == 92 and score["risk_flag_count"] == 0
    assert all(not f["scoring_eligible"] for f in r["risk_flags"] + r["claim_reviews"])
    assert r["raw_model_output"]["risk_flags"] == flags
    from tests.test_advisory_dogfood_correctness import stabilized
    assert stabilized(3.51, r["risk_flags"])["status"] == "NO_REBALANCE_REQUIRED"


def test_model_allocation_timing_and_invented_refs_are_not_evidence():
    c = build_claim_evidence([{"symbol": "MICRON01.BK", "action": "BUY", "timing_score": 1,
                              "execution_priority": "DEFER"}], [], {})
    assert not c["evidence"]
    assert not interpret([flag("INVESTMENT_JUDGMENT", ref="risk:ENTRY_TIMING:MICRON01.BK")], c)["risk_flags"]


@pytest.mark.parametrize("availability", [None, False])
def test_missing_upstream_timing_data_does_not_fabricate_risk(availability):
    c = build_claim_evidence([{"symbol": "MICRON01.BK", "action": "BUY"}], [], {},
        {"MICRON01.BK": {"timing_score": 0, "execution_priority": "DEFER", "timing_data_available": availability}})
    assert not c["evidence"]


def test_existing_timing_producer_availability_is_preserved(monkeypatch):
    from services import optimizer_timing
    from services.timing_intelligence import compute_timing_score
    def result(price):
        return compute_timing_score("MICRON01.BK", price, 20, 25, 30, 30, 100, 100, -5, 2)
    for price, available in [(10, True), (None, False)]:
        observed = result(price)
        monkeypatch.setattr(optimizer_timing, "score_timing_batch", lambda symbols: [observed])
        upstream = optimizer_timing.enrich_scores_with_timing(["MICRON01.BK"])["MICRON01.BK"]
        assert upstream.data_available is available
        c = build_claim_evidence([{"symbol": upstream.symbol, "action": "BUY"}], [], {},
            {upstream.symbol: {"timing_score": upstream.timing_score,
             "execution_priority": upstream.execution_priority, "timing_data_available": upstream.data_available}})
        assert bool(c["evidence"]) is available


def test_model_cannot_supply_its_own_contract_or_verification_metadata():
    invented = {"kind": "POLICY_BREACH", "symbol": "BH.BK", "allowed_pct": 15, "proposed_pct": 15.31}
    raw = {"risk_flags": [{**flag("POLICY_BREACH", "BH.BK", "policy:0"),
                            "scoring_eligible": True, "validation_status": "VERIFIED", "provenance": invented}],
           "policy_claim_contract": {"evidence": {"policy:0": invented}}}
    r = validate_auditor_claims(raw, contract())
    assert not r["risk_flags"] and r["claim_reviews"][0]["scoring_eligible"] is False
    assert r["policy_claim_contract"] == contract()


def test_malformed_and_duplicate_evidence_cannot_amplify_scoring():
    c = contract("BUY")
    r = interpret([flag("EXECUTION_RESTRICTION", ref="execution:1"),
        flag("EXECUTION_RESTRICTION", ref="execution:1"), flag("POLICY_BREACH", ref=[]), "invalid"], c)
    assert len(r["risk_flags"]) == 1 and len(r["claim_reviews"]) == 3


def test_validation_never_changes_intent_or_deferred_execution():
    frozen = {"risk_flags": [flag()], "advisory_intent_review": {"positions": [{"intent": "NO_DECREASE"}]},
        "execution_optimization": {"trades": [{"symbol": "MICRON01.BK", "status": "DEFERRED"}]}}
    r = validate_auditor_claims(frozen, contract())
    for key in ("advisory_intent_review", "execution_optimization"):
        assert r[key] == frozen[key]


def test_mocked_layered_pipeline_validates_before_scoring_and_preserves_hold(monkeypatch):
    import agents.optimizer as optimizer
    from tests.test_advisory_intent_integration import FakeAI, l2, alloc
    proposal = l2(alloc("BH.BK", 15.31, "HOLD"), alloc("MICRON01.BK", 16.03, "HOLD"), status="NO_ACTION")
    ai = FakeAI(proposal, l3={"risk_flags": [flag("POLICY_BREACH", "BH.BK", "policy:0"),
        flag("EXECUTION_RESTRICTION", ref="execution:1")], "final_risk_level": "high"})
    monkeypatch.setattr(optimizer, "call_ai", ai)
    # Supply the frozen NAV weights, as enabled Advisory does in the live run.
    monkeypatch.setattr(optimizer, "_compute_portfolio_weights", lambda rows: [
        {**r, "weight_pct": 15.31 if r["symbol"] == "BH.BK" else 16.03,
         "market_value": r["shares"] * r["current_price"]} for r in rows])
    result = optimizer.run_layered_optimizer([
        {"symbol": "BH.BK", "shares": 1531, "current_price": 1, "signal": "HOLD", "sector": "Healthcare"},
        {"symbol": "MICRON01.BK", "shares": 1603, "current_price": 1, "signal": "HOLD", "sector": "Technology"},
    ], [], "TA fixture", cash_balance=6866, max_sector_pct=70,
       policy_context={"hard_constraints": {"max_single_position_pct": 25, "min_cash_pct": 3,
           "max_sector_pct": 70, "max_turnover_pct": 70}},
       execution_context={"per_symbol": {"BH.BK": {"position_cap_pct": None},
          "MICRON01.BK": {"position_cap_pct": 15}}})
    assert list(ai.prompts) == ["layer1", "layer2", "layer3"]
    assert "AUTHORITATIVE POLICY CLAIM CONTRACT" in ai.prompts["layer3"][0]
    assert result["layer3_result"]["risk_flags"] == []
    assert result["consensus"]["risk_alignment_score"] == 92
    assert result["consensus"]["governance_flags"] == []
    assert all(a["action"] == "HOLD" for a in result["target_allocations"])
    assert result["layer3_result"]["policy_claim_contract"]["evidence"]["execution:1"]["kind"] == "EXISTING_EXPOSURE"


def test_mocked_pipeline_uses_pre_l3_timing_evidence_not_model_timing(monkeypatch):
    import agents.optimizer as optimizer
    from tests.test_advisory_intent_integration import FakeAI, l2, alloc
    ai = FakeAI(l2(alloc("ENTRY.BK", 5, "BUY")), l3={"risk_flags": [
        flag("INVESTMENT_JUDGMENT", "ENTRY.BK", "risk:ENTRY_TIMING:ENTRY.BK")]})
    monkeypatch.setattr(optimizer, "call_ai", ai)
    result = optimizer.run_layered_optimizer([], [{"symbol": "ENTRY.BK", "sector": "Technology",
        "signal": "BUY", "combined_score": 80, "timing_score": 20,
        "execution_priority": "DEFER", "timing_data_available": True}], "fixture", cash_balance=10000)
    scored = result["layer3_result"]["risk_flags"][0]
    assert scored["claim_kind"] == "INVESTMENT_OBSERVATION" and scored["severity"] == "MEDIUM"
    assert "15%" not in scored["issue"] and scored["provenance"]["data_available"] is True
    assert "risk:ENTRY_TIMING:ENTRY.BK" in ai.prompts["layer3"][0]
    assert result["consensus"]["risk_alignment_score"] == 72
