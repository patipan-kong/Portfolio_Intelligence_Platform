"""Offline scoring and stabilization regressions from Advisory dogfood."""
import copy
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from agents.optimizer import _consensus_engine, _layer3_prompt
from services.optimizer.stabilization import apply_stabilization


RISK = {"symbol": "AAA", "issue": "Poor entry timing", "severity": "MEDIUM",
        "category": "INVESTMENT_RISK"}
REVIEW = {"symbol": "AAA", "issue": "Owner restriction disagrees with reduction",
          "severity": "MEDIUM", "category": "OWNER_INTENT_REVIEW"}


@pytest.mark.parametrize("flags,score", [([], 92), ([RISK], 72), ([REVIEW], 92),
                                        ([RISK, REVIEW], 72)])
def test_only_investment_flags_affect_alignment_and_evidence_is_preserved(flags, score):
    l3 = {"risk_flags": copy.deepcopy(flags), "final_risk_level": "medium"}
    before = copy.deepcopy(l3)
    consensus = _consensus_engine({}, {}, l3)
    assert consensus["risk_alignment_score"] == score
    assert consensus["risk_flag_count"] == len([f for f in flags if f["category"] == "INVESTMENT_RISK"])
    assert l3 == before  # User-visible L3 evidence is not removed/reworded.


@pytest.mark.parametrize("category", [None, "UNKNOWN"])
def test_unclassified_flags_remain_scored_without_prose_guessing(category):
    flag = {**REVIEW, "category": category}
    assert _consensus_engine({}, {}, {"risk_flags": [flag]})["risk_alignment_score"] == 72


def stabilized(drift, flags=()):
    return apply_stabilization({
        "status": "REBALANCE", "rebalance_opportunity_score": 40,
        "target_allocations": [{"symbol": "AAA", "action": "REDUCE",
                                "current_weight": 15.31, "target_weight": 15.31 - drift,
                                "allocation_change_percent": -drift}],
        "consensus": {"consensus_strength_score": 80},
        "layer3_result": {"risk_flags": list(flags)},
    }, last_rebalance_at=None)


def test_structured_drift_cause_when_all_within_tolerance():
    result = stabilized(1)
    assert result["stabilization"]["all_within_tolerance"] is True
    assert result["no_action_reason"] == "WELL_BALANCED"


def test_outside_tolerance_is_suppressed_for_minimum_benefit():
    result = stabilized(3.51)
    assert result["stabilization"]["all_within_tolerance"] is False
    assert result["status"] == "NO_REBALANCE_REQUIRED"
    assert result["no_action_reason"] == "INSUFFICIENT_EDGE"
    assert result["stabilization"]["minimum_impact"]["net_benefit_pct"] == .1974


def test_review_flag_never_becomes_a_high_risk_stabilization_breach():
    review = {**REVIEW, "severity": "HIGH"}
    assert stabilized(3.51, [review])["status"] == "NO_REBALANCE_REQUIRED"
    assert stabilized(3.51, [{**RISK, "severity": "HIGH"}])["status"] == "REBALANCE"


def test_l3_contract_explicitly_classifies_owner_disagreement():
    prompt = _layer3_prompt({}, {})
    assert '"category":"INVESTMENT_RISK|OWNER_INTENT_REVIEW"' in prompt
    assert "exclude it from final_risk_level, safer_choice" in prompt
