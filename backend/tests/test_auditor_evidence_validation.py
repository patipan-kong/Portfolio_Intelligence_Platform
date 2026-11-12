"""MUJI V2 Phase 4 Slice 4.6A — Auditor sector-advisory validation and candidate-review diagnostics.

Frozen histories 245-250 (tests/fixtures/auditor_evidence_frozen_245_250.json, a
read-only export of stored optimizer results). Offline: no DB, provider or model calls.

consensus_l2_disagreements: the sector-advisory pipeline overwrites
layer2_result.disagreements with consensus.disagreement_reasons after consensus
runs and moves advisory comments to unscored_comments. The fixture rebuilds the
original consensus input as the stored reasons (basis ACTION) followed by the
unscored comments; replay then reproduces every stored consensus field.
"""

import copy
import json
import os

import pytest

import agents.optimizer as optimizer
from agents.optimizer import _consensus_engine
from services.optimizer import strategic_candidates as sc
from services.optimizer.auditor_claims import (
    SECTOR_CLAIM_VERSION, VERSION, build_claim_evidence, validate_auditor_claims,
)
from services.optimizer.risk_flags import investment_risk_flags
from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY
from services.optimizer.strategic_candidates import (
    candidate_review_diagnostics, decide_selection, validate_candidate_reviews,
)
from tests.test_auditor_review_contract import OPT_IN, _complete_reviews, _run

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "auditor_evidence_frozen_245_250.json")
RUNS = json.load(open(FIXTURE, encoding="utf-8"))["runs"]
HEALTHCARE = "CURRENT:effective_sector_limits:Healthcare"
TECHNOLOGY = "CURRENT:effective_sector_limits:Technology"


def _validate(run, flags=None):
    raw = copy.deepcopy(RUNS[run]["layer3_raw_model_output"])
    if flags is not None:
        raw["risk_flags"] = flags
    return validate_auditor_claims(raw, RUNS[run]["layer3_policy_claim_contract"])


def _review(result, symbol, ref=None):
    rows = [f for f in result["claim_reviews"] if f["symbol"] == symbol and (ref is None or f.get("evidence_ref") == ref)]
    assert len(rows) == 1
    return rows[0]


def _sector_flag(symbol, ref, **extra):
    return {"symbol": symbol, "issue": "Model wording 99% threshold", "severity": "CRITICAL",
            "category": "INVESTMENT_RISK", "claim_kind": "SECTOR_ADVISORY", "evidence_ref": ref, **extra}


# ── A. Sector Advisory validation ────────────────────────────────────────────

def test_run245_non_member_symbol_gets_no_sector_provenance():
    result = _validate("245")
    bg = _review(result, "BG.BK")  # not in the run's 89-symbol universe
    assert bg["evidence_ref"] == HEALTHCARE
    assert bg["validation_status"] == "UNSUPPORTED" and bg["scoring_eligible"] is False
    assert isinstance(bg["provenance"], str) and "not PORTFOLIO or a member" in bg["provenance"]


def test_run249_healthcare_text_comes_from_evidence():
    bh = _review(_validate("249"), "BH.BK")
    assert bh["issue"] == ("Healthcare sector 30.56% of invested equity vs 24.5% advisory limit "
                           "(REGIME_POLICY, CURRENT); members: BH.BK")
    assert "30% threshold" not in bh["issue"]
    assert (bh["validation_status"], bh["claim_kind"], bh["severity"], bh["category"], bh["scoring_eligible"]) == (
        "ADVISORY", "SECTOR_ADVISORY", "LOW", "INVESTMENT_RISK", False)
    assert bh["provenance"]["evidence_id"] == HEALTHCARE


def test_run249_technology_text_and_shared_evidence_accepted_once():
    result = _validate("249")
    nvda, micron = _review(result, "NVDA01.BK"), _review(result, "MICRON01.BK")
    assert nvda["issue"] == ("Technology sector 32.73% of invested equity vs 25% advisory limit "
                             "(EMERGENCY_OVERRIDE, CURRENT); members: MICRON01.BK, NVDA01.BK")
    assert nvda["validation_status"] == "ADVISORY"
    assert micron["validation_status"] == "UNSUPPORTED" and micron["provenance"].startswith("Duplicate")
    accepted = [f for f in result["claim_reviews"]
                if f.get("evidence_ref") == TECHNOLOGY and f["validation_status"] == "ADVISORY"]
    assert len(accepted) == 1


def test_portfolio_sector_comment_is_allowed_and_model_fields_are_not_trusted():
    flag = _sector_flag("PORTFOLIO", HEALTHCARE, category="OWNER_INTENT_REVIEW")
    result = _validate("249", [flag])
    review = result["claim_reviews"][0]
    assert review["validation_status"] == "ADVISORY"
    assert (review["severity"], review["category"]) == ("LOW", "INVESTMENT_RISK")
    assert review["issue"].startswith("Healthcare sector 30.56%")
    # The model's own wording survives only in the existing raw-output storage.
    assert result["raw_model_output"]["risk_flags"] == [flag]
    assert result["sector_claim_validation_version"] == SECTOR_CLAIM_VERSION


@pytest.mark.parametrize("ref", [
    "CURRENT:effective_sector_limits:Energy",  # no such advisory in run 249
    "policy:0",                                  # a different evidence family
    None, 7,
])
def test_unknown_or_mismatched_sector_evidence_is_unsupported(ref):
    review = _validate("249", [_sector_flag("PORTFOLIO", ref)])["claim_reviews"][0]
    assert review["validation_status"] == "UNSUPPORTED" and review["scoring_eligible"] is False
    assert isinstance(review["provenance"], str)


def test_incomplete_sector_evidence_is_unsupported():
    contract = copy.deepcopy(RUNS["249"]["layer3_policy_claim_contract"])
    del contract["sector_advisories"][HEALTHCARE]["observed_pct"]
    raw = {"risk_flags": [_sector_flag("BH.BK", HEALTHCARE)]}
    review = validate_auditor_claims(raw, contract)["claim_reviews"][0]
    assert review["validation_status"] == "UNSUPPORTED" and "Incomplete" in review["provenance"]


def test_first_valid_occurrence_wins_after_an_invalid_one():
    flags = [_sector_flag("BG.BK", HEALTHCARE), _sector_flag("BH.BK", HEALTHCARE),
             _sector_flag("PORTFOLIO", HEALTHCARE)]
    statuses = [f["validation_status"] for f in _validate("249", flags)["claim_reviews"]]
    assert statuses == ["UNSUPPORTED", "ADVISORY", "UNSUPPORTED"]


def test_genuine_policy_and_execution_claims_are_unchanged_by_sector_claims():
    allocations = [{"symbol": "MICRON01.BK", "action": "BUY", "current_weight": 10.0, "target_weight": 16.03}]
    context = {"per_symbol": {"MICRON01.BK": {"position_cap_pct": 15}}, "dr_portfolio_cap": 40}
    details = [{"violation_type": "CASH_MANDATE", "symbol": "PORTFOLIO", "proposed_pct": 3, "allowed_pct": 5}]
    contract = build_claim_evidence(allocations, details, context)
    contract["sector_advisories"] = copy.deepcopy(RUNS["249"]["layer3_policy_claim_contract"]["sector_advisories"])
    genuine = [
        {"symbol": "PORTFOLIO", "issue": "x", "severity": "HIGH", "category": "INVESTMENT_RISK",
         "claim_kind": "POLICY_BREACH", "evidence_ref": "policy:0"},
        {"symbol": "MICRON01.BK", "issue": "y", "severity": "MEDIUM", "category": "INVESTMENT_RISK",
         "claim_kind": "EXECUTION_RESTRICTION", "evidence_ref": "execution:0"},
    ]
    sector = RUNS["249"]["layer3_raw_model_output"]["risk_flags"][:4]
    alone = validate_auditor_claims({"risk_flags": genuine}, contract)
    mixed = validate_auditor_claims({"risk_flags": [*genuine, *sector]}, contract)
    assert [f["issue"] for f in alone["risk_flags"]] == ["CASH_MANDATE: 3% / 5%", "EXECUTION_RESTRICTION: 16.03% / 15%"]
    assert all(f["validation_status"] == "VERIFIED" for f in alone["risk_flags"])
    for key in ("risk_flags", "final_risk_level", "safer_choice", "auditor_notes"):
        assert mixed[key] == alone[key]


def test_claim_contract_version_is_unchanged():
    # The contract is serialized into the Auditor prompt; its version must not move.
    assert VERSION == "wealth.auditor-policy-claims.v2"
    for run in RUNS.values():
        assert run["layer3_policy_claim_contract"]["version"] == VERSION


# ── B. Candidate-review diagnostics ──────────────────────────────────────────

SELECTION_RUNS = [run for run, data in sorted(RUNS.items()) if data["candidate_audit"] is not None]


def _codes(run):
    data = RUNS[run]
    return candidate_review_diagnostics(data["layer3_raw_model_output"], data["strategic_candidates"])["findings"]


def test_run245_and_246_support_opposition_overlap_detected():
    assert {"code": "SUPPORT_OPPOSITION_OVERLAP", "candidate_id": "proposal-633bb49f9c7e",
            "refs": ["symbol:GOOGL01.BK:timing_score", "symbol:GULF.BK:ta_score"]} in _codes("245")
    assert {"code": "SUPPORT_OPPOSITION_OVERLAP", "candidate_id": "proposal-10e2e0c07ca6",
            "refs": ["symbol:GOOGL01.BK:timing_score", "symbol:GULF.BK:ta_score",
                     "symbol:MICRON01.BK:timing_score", "symbol:NVDA01.BK:timing_score"]} in _codes("246")


def test_run249_hold_support_limitation_detected():
    assert _codes("249") == [{"code": "HOLD_SUPPORT_UNREPRESENTABLE", "candidate_id": "hold-current",
                              "opposing_ref_count": 5, "reviewed": True}]


def test_opposing_ref_outside_review_view_detected():
    data = RUNS["249"]
    envelope = copy.deepcopy(data["strategic_candidates"])
    view = sc.candidate_review_view(envelope)["relevant_evidence"]
    outside = next(ref for ref in envelope["observed_evidence_catalog"] if ref not in view)
    raw = {"candidate_reviews": [{"candidate_id": "hold-current", "supporting_refs": [],
                                  "opposing_refs": [outside], "material_conflicts": []}]}
    findings = candidate_review_diagnostics(raw, envelope)["findings"]
    assert {"code": "OPPOSING_OUTSIDE_REVIEW_VIEW", "candidate_id": "hold-current", "refs": [outside]} in findings
    # Still a known catalog key, so the review itself stays AVAILABLE.
    assert validate_candidate_reviews(raw, envelope)["status"] == "AVAILABLE"


@pytest.mark.parametrize("run", SELECTION_RUNS)
def test_diagnostics_change_no_review_status_eligibility_or_selection(run):
    data = RUNS[run]
    envelope = copy.deepcopy(data["strategic_candidates"])
    raw = copy.deepcopy(data["layer3_raw_model_output"])
    before = copy.deepcopy((envelope, raw))
    candidate_review_diagnostics(raw, envelope)
    assert (envelope, raw) == before  # pure: nothing mutated, eligibility untouched
    audit = validate_candidate_reviews(raw, envelope)
    assert audit == data["candidate_audit"]


@pytest.mark.parametrize("raw", [None, "text", {"candidate_reviews": "none"}, {"candidate_reviews": [1, {}]}])
def test_malformed_reviews_never_raise(raw):
    result = candidate_review_diagnostics(raw, RUNS["249"]["strategic_candidates"])
    assert result["diagnostic_only"] is True
    assert [f["code"] for f in result["findings"]] == ["HOLD_SUPPORT_UNREPRESENTABLE"]


def _overlap_reviews(prompt):
    reply = _complete_reviews(prompt)
    for review in reply["candidate_reviews"]:
        if review["candidate_id"] != "hold-current":
            review["opposing_refs"] = ["symbol:AAA:signal"]  # also cited as support
    return reply


def test_pipeline_keeps_diagnostics_beside_audit_and_out_of_every_gate(monkeypatch):
    result, captured = _run(monkeypatch, layer3_reply=_overlap_reviews, **OPT_IN)
    codes = [f["code"] for f in result["candidate_review_diagnostics"]["findings"]]
    assert codes == ["HOLD_SUPPORT_UNREPRESENTABLE", "SUPPORT_OPPOSITION_OVERLAP"]
    assert result["candidate_audit"]["status"] == "AVAILABLE"
    assert "candidate_review_diagnostics" not in result["candidate_audit"]
    assert "diagnostic" not in captured["committee"]["prompt"]

    def broken(*args, **kwargs):
        raise RuntimeError("diagnostics failure")

    monkeypatch.setattr(sc, "candidate_review_diagnostics", broken)
    failed, failed_captured = _run(monkeypatch, layer3_reply=_overlap_reviews, **OPT_IN)
    assert failed["candidate_review_diagnostics"]["status"] == "FAILED"
    for key in ("strategic_candidates", "candidate_audit", "strategy_selection", "consensus",
                "target_allocations", "target_cash_weight", "layer3_result"):
        assert failed[key] == result[key]
    assert failed_captured["committee"]["prompt"] == captured["committee"]["prompt"]


def test_pipeline_without_selection_has_no_diagnostics(monkeypatch):
    result, _ = _run(monkeypatch, sector_policy_mode=SECTOR_POLICY_ADVISORY,
                     optimizer_policy_mode=OPTIMIZER_POLICY_MUJI_V2)
    assert "candidate_review_diagnostics" not in result


# ── C. Deterministic decision invariance on frozen histories 245-250 ────────

@pytest.mark.parametrize("run", sorted(RUNS))
def test_frozen_decisions_unchanged(run):
    data = RUNS[run]
    stored = data["layer3_stored"]
    validated = _validate(run)
    for key in ("risk_flags", "final_risk_level", "safer_choice", "auditor_notes", "claim_validation_version"):
        assert validated[key] == stored[key]
    assert validated["final_risk_level"] == "low"
    # Stabilization reads only scored flags; none exist before or after.
    assert investment_risk_flags(validated["risk_flags"]) == investment_risk_flags(stored["risk_flags"]) == []
    # Sector-routed claims (valid or not) have no decision effect.
    kept = [f for f in data["layer3_raw_model_output"]["risk_flags"]
            if f.get("evidence_ref") not in data["layer3_policy_claim_contract"]["sector_advisories"]
            and f.get("claim_kind") != "SECTOR_ADVISORY"]
    without = _validate(run, kept)
    for key in ("risk_flags", "final_risk_level", "safer_choice", "auditor_notes"):
        assert without[key] == validated[key]

    modes = data["modes"]
    l2 = {**data["layer2_result"], "disagreements": data["consensus_l2_disagreements"]}
    consensus = _consensus_engine(data["layer1_result"], l2, validated,
                                  sector_advisory=modes["sector_policy_mode"] == SECTOR_POLICY_ADVISORY,
                                  muji_v2=modes["optimizer_policy_mode"] == OPTIMIZER_POLICY_MUJI_V2)
    assert {k: consensus.get(k) for k in data["stored_consensus"]} == data["stored_consensus"]
    assert consensus["risk_alignment_score"] == 92

    if data["candidate_audit"] is None:  # history 247: selection mode off
        assert data["strategy_selection"] is None and modes["strategy_selection_mode"] is None
        return
    envelope = data["strategic_candidates"]
    audit = validate_candidate_reviews(data["layer3_raw_model_output"], envelope)
    assert audit == data["candidate_audit"]
    selection = decide_selection(envelope, audit, None, hold_safe=True, failure_reason="NO_ELIGIBLE_ACTION")
    stored_selection = {k: v for k, v in data["strategy_selection"].items() if k != "downstream_outcome"}
    assert selection == stored_selection
    assert selection["selected_candidate_id"] == "hold-current"
    hold = next(c for c in envelope["candidates"] if c["id"] == "hold-current")
    assert [(r["symbol"], r["action"], r["target_weight"]) for r in hold["proposed_allocations"]] == [
        (r["symbol"], r["action"], r["target_weight"])
        for r in sorted(data["target_allocations"], key=lambda r: r["symbol"])]
