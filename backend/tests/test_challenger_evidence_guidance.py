"""MUJI V2 Phase 4 Slice 4.3 — Challenger evidence guidance.

Golden fixtures were captured from baseline a6e0505 (before this slice) with the
same inputs. Regenerate only deliberately, on baseline code:
REGENERATE_CHALLENGER_GUIDANCE_BASELINE=1.
"""

import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import agents.optimizer as optimizer
from services.optimizer import strategic_candidates as sc
from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY
from services.optimizer.strategic_candidates import SELECTION_VERSION, prepare_candidates

from tests.test_evidence_provenance import HOLDINGS, L2_REPLY, PROVENANCE, REGIME, WATCHLIST

GOLDEN = os.path.join(os.path.dirname(__file__), "fixtures", "challenger_evidence_guidance_baseline.json")
REGENERATE = bool(os.environ.get("REGENERATE_CHALLENGER_GUIDANCE_BASELINE"))

SCENARIOS = {
    "legacy": {},
    "sector_advisory_v1": {"sector_policy_mode": SECTOR_POLICY_ADVISORY},
    "muji_v2_challenger": {"sector_policy_mode": SECTOR_POLICY_ADVISORY,
                           "optimizer_policy_mode": OPTIMIZER_POLICY_MUJI_V2},
}
OPT_IN = {**SCENARIOS["muji_v2_challenger"], "strategy_selection_mode": SELECTION_VERSION}
# Text the baseline appended after the L2 JSON schema for opt-in runs.
OLD_L2_SUFFIX = ("\nOptional additional_plans: up to two complete portfolio plans, each with "
                 "strategy_family, observed_evidence_refs, cash_balance_target, "
                 "portfolio_assessment, and allocations in the same format as the primary plan. "
                 "Omit when evidence is insufficient. These are candidates, not selected trades.\n")
L2_OUTPUT_LINE = "Return JSON only. No markdown fences, no prose outside the JSON."
FALLBACK_OUTPUT_LINE = "Return ONLY valid JSON without markdown fences:"


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


def _preview_of(result):
    """The evidence preview a run's own frozen candidate envelope implies."""
    envelope = result["strategic_candidates"]
    preview = {"evidence_provenance_status": envelope["evidence_provenance_status"]}
    if "unobserved_evidence" in envelope:
        preview["unobserved_evidence"] = envelope["unobserved_evidence"]
    return preview


def _reviews(prompt):
    ids = re.findall(r'"candidate_id": "([^"]+)"', prompt)
    return {"risk_flags": [], "candidate_reviews": [
        {"candidate_id": cid, "supporting_refs": [], "opposing_refs": [],
         "material_conflicts": [], "assessment": "Model view"} for cid in ids]}


def _run(monkeypatch, *, fail_primary=False, l2_reply=L2_REPLY, holdings=HOLDINGS,
         watchlist=WATCHLIST, **kwargs):
    captured = {}

    def fake_ai(prompt, provider, model, *args, usage_layer, max_tokens=None, **kw):
        captured[usage_layer] = {"prompt": prompt, "max_tokens": max_tokens}
        if usage_layer == "layer1":
            payload = {"swaps": [], "top_buys": []}
        elif usage_layer == "layer2":
            payload = l2_reply
        elif usage_layer == "layer3":
            payload = _reviews(prompt)
        elif usage_layer == "committee":
            payload = {"selected_candidate_id": "hold-current", "supporting_evidence_refs": [],
                       "opposing_evidence_refs": [], "comparison_against_hold": "Waiting is preferable.",
                       "decision_rationale": "Hold the current portfolio.", "material_uncertainty": []}
        else:
            payload = {"allocations": [], "status": "NO_ACTION", "cash_balance_target": 20,
                       "risk_flags": []}
        return {"text": json.dumps(payload), "latency_ms": 1}

    monkeypatch.setattr(optimizer, "call_ai", fake_ai)
    if fail_primary:
        real = optimizer._emit_stage

        def fail_first_stage(on_stage, stage):
            if stage == "LAYER1_PROPOSAL":
                raise RuntimeError("primary pipeline failure")
            return real(on_stage, stage)

        monkeypatch.setattr(optimizer, "_emit_stage", fail_first_stage)
    result = optimizer.run_layered_optimizer(
        [dict(row) for row in holdings], [dict(row) for row in watchlist], "P",
        cash_balance=200, regime_context=REGIME, **kwargs)
    return result, captured


# ── Opt-in OFF: byte-for-byte preservation (fallback, all policy modes) ──────

@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_baseline_optin_off_fallback_prompt_and_allocations_unchanged(monkeypatch, name):
    extra = {} if REGENERATE else {"evidence_provenance": PROVENANCE}
    result, captured = _run(monkeypatch, fail_primary=True, **SCENARIOS[name], **extra)
    assert set(captured) == {"fallback"}
    observed = {
        "prompt": captured["fallback"],
        "target_allocations": _canonical(result.get("target_allocations")),
        "target_cash_weight": result.get("target_cash_weight"),
    }
    baseline = _golden(f"fallback_optin_off:{name}", observed)
    assert observed["prompt"]["prompt"] == baseline["prompt"]["prompt"]
    assert observed["prompt"]["max_tokens"] == baseline["prompt"]["max_tokens"]
    assert observed["target_allocations"] == baseline["target_allocations"]
    assert observed["target_cash_weight"] == baseline["target_cash_weight"]
    if not REGENERATE:
        assert "CHALLENGER EVIDENCE GUIDANCE" not in observed["prompt"]["prompt"]


# ── Opt-in ON: only the intended prompt change ───────────────────────────────

def test_baseline_optin_on_primary_only_l2_changes(monkeypatch):
    result, captured = _run(monkeypatch, evidence_provenance=PROVENANCE, **OPT_IN)
    observed = {
        "prompts": captured,
        "target_allocations": _canonical(result.get("target_allocations")),
        "strategic_candidates": _canonical(result.get("strategic_candidates")),
        "strategy_selection": _canonical(result.get("strategy_selection")),
    }
    baseline = _golden("optin_on:primary", observed)
    assert set(captured) == set(baseline["prompts"])
    for layer in captured:
        assert captured[layer]["max_tokens"] == baseline["prompts"][layer]["max_tokens"], layer
        if layer != "layer2":
            assert captured[layer]["prompt"] == baseline["prompts"][layer]["prompt"], layer
    assert observed["target_allocations"] == baseline["target_allocations"]
    assert observed["strategic_candidates"] == baseline["strategic_candidates"]
    assert observed["strategy_selection"] == baseline["strategy_selection"]
    if REGENERATE:
        return
    old = baseline["prompts"]["layer2"]["prompt"]
    new = captured["layer2"]["prompt"]
    assert old.endswith(OLD_L2_SUFFIX) and not new.endswith(OLD_L2_SUFFIX)
    head, tail = old[:-len(OLD_L2_SUFFIX)].split(L2_OUTPUT_LINE)
    block = optimizer._challenger_evidence_block(_preview_of(result), additional_plans=True)
    # The block is inserted immediately before the output instruction; nothing else changed.
    assert new == head + block + L2_OUTPUT_LINE + tail


def test_baseline_optin_on_fallback_only_guidance_added(monkeypatch):
    result, captured = _run(monkeypatch, fail_primary=True, evidence_provenance=PROVENANCE, **OPT_IN)
    observed = {
        "prompt": captured["fallback"],
        "target_allocations": _canonical(result.get("target_allocations")),
        "strategic_candidates": _canonical(result.get("strategic_candidates")),
    }
    baseline = _golden("optin_on:fallback", observed)
    assert observed["prompt"]["max_tokens"] == baseline["prompt"]["max_tokens"]
    assert observed["target_allocations"] == baseline["target_allocations"]
    assert observed["strategic_candidates"] == baseline["strategic_candidates"]
    if REGENERATE:
        return
    head, tail = baseline["prompt"]["prompt"].split(FALLBACK_OUTPUT_LINE)
    block = optimizer._challenger_evidence_block(_preview_of(result), additional_plans=False)
    assert captured["fallback"]["prompt"] == head + block + FALLBACK_OUTPUT_LINE + tail


# ── Guidance placement and scope ─────────────────────────────────────────────

HEADER = "[CHALLENGER EVIDENCE GUIDANCE — COMMITTEE CANDIDATES]"


def _block_of(prompt, output_line):
    start = prompt.index(HEADER)
    return prompt[start:prompt.index(output_line)]


@pytest.mark.parametrize("name", sorted(SCENARIOS))
@pytest.mark.parametrize("fail_primary", [False, True])
def test_guidance_absent_when_committee_opt_in_is_off(monkeypatch, name, fail_primary):
    _, captured = _run(monkeypatch, fail_primary=fail_primary, evidence_provenance=PROVENANCE,
                       **SCENARIOS[name])
    for layer, call in captured.items():
        assert HEADER not in call["prompt"], layer
        assert "UNAVAILABLE EVIDENCE" not in call["prompt"], layer


def test_optin_l2_guidance_precedes_output_schema(monkeypatch):
    _, captured = _run(monkeypatch, evidence_provenance=PROVENANCE, **OPT_IN)
    prompt = captured["layer2"]["prompt"]
    assert prompt.count(HEADER) == 1
    assert prompt.index(HEADER) < prompt.index("UNAVAILABLE EVIDENCE") < prompt.index(L2_OUTPUT_LINE)
    # additional_plans moved inside the block, before the schema; the prompt ends with the schema.
    assert prompt.count("Optional additional_plans:") == 1
    assert prompt.index("Optional additional_plans:") < prompt.index(L2_OUTPUT_LINE)
    assert prompt.rstrip().endswith("}")
    for layer in ("layer1", "layer3", "committee"):
        assert HEADER not in captured[layer]["prompt"], layer
    assert captured["layer2"]["max_tokens"] == 8192


def test_optin_fallback_guidance_precedes_output_schema(monkeypatch):
    _, captured = _run(monkeypatch, fail_primary=True, evidence_provenance=PROVENANCE, **OPT_IN)
    prompt = captured["fallback"]["prompt"]
    assert prompt.count(HEADER) == 1
    assert prompt.index(HEADER) < prompt.index(FALLBACK_OUTPUT_LINE)
    assert "additional_plans" not in prompt  # the fallback never reads extra plans
    assert prompt.rstrip().endswith("}")


def test_normal_and_fallback_guidance_are_consistent(monkeypatch):
    _, primary = _run(monkeypatch, evidence_provenance=PROVENANCE, **OPT_IN)
    _, fallback = _run(monkeypatch, fail_primary=True, evidence_provenance=PROVENANCE, **OPT_IN)
    normal = _block_of(primary["layer2"]["prompt"], L2_OUTPUT_LINE)
    single = _block_of(fallback["fallback"]["prompt"], FALLBACK_OUTPUT_LINE)
    assert normal.startswith(optimizer._CHALLENGER_EVIDENCE_GUIDANCE)
    # Identical guidance and unavailable list; only the primary adds additional_plans.
    assert normal == single[:-1] + optimizer._ADDITIONAL_PLANS_GUIDANCE + "\n"


# ── Unavailable references ───────────────────────────────────────────────────

def _listed_refs(prompt, output_line):
    block = _block_of(prompt, output_line)
    listed = {}
    for line in block.splitlines():
        match = re.fullmatch(r"- (\w+) ([A-Z]+): (.+)", line)
        if match:
            field, status, symbols = match.groups()
            for symbol in symbols.split(", "):
                listed[f"symbol:{symbol}:{field}"] = status
    return listed


def test_unavailable_refs_match_frozen_envelope_primary(monkeypatch):
    result, captured = _run(monkeypatch, evidence_provenance=PROVENANCE, **OPT_IN)
    envelope = result["strategic_candidates"]
    listed = _listed_refs(captured["layer2"]["prompt"], L2_OUTPUT_LINE)
    assert envelope["unobserved_evidence"]  # the fixture has excluded values
    assert listed == envelope["unobserved_evidence"]
    assert not set(listed) & set(envelope["observed_evidence_catalog"])


def test_unavailable_refs_match_frozen_envelope_fallback(monkeypatch):
    result, captured = _run(monkeypatch, fail_primary=True, evidence_provenance=PROVENANCE, **OPT_IN)
    envelope = result["strategic_candidates"]
    assert _listed_refs(captured["fallback"]["prompt"], FALLBACK_OUTPUT_LINE) == envelope["unobserved_evidence"]


def test_evidence_preview_equals_prepare_candidates():
    for provenance in (PROVENANCE, {}, None):
        preview = sc.evidence_preview(HOLDINGS, WATCHLIST, REGIME, None, provenance)
        envelope = prepare_candidates(HOLDINGS, WATCHLIST, 200, {}, regime=REGIME, provenance=provenance)
        assert preview["evidence_provenance_status"] == envelope["evidence_provenance_status"]
        assert preview.get("unobserved_evidence") == envelope.get("unobserved_evidence")


def test_no_unavailable_evidence_says_none():
    observed = {s: {f: {"status": "OBSERVED"} for f in ("signal", "fa_score", "ta_score", "timing_score")}
                for s in ("AAA", "BBB", "WWW", "ZZZ")}
    block = optimizer._challenger_evidence_block(
        sc.evidence_preview(HOLDINGS, WATCHLIST, REGIME, None, observed), additional_plans=False)
    assert "UNAVAILABLE EVIDENCE: none; every signal and score shown was observed.\n" in block


def test_not_supplied_provenance_is_disclosed(monkeypatch):
    result, captured = _run(monkeypatch, **OPT_IN)
    assert result["strategic_candidates"]["evidence_provenance_status"] == "NOT_SUPPLIED"
    prompt = captured["layer2"]["prompt"]
    assert ("UNAVAILABLE EVIDENCE: not determined for this run; signals and scores were not "
            "provenance-checked and may include defaults.") in prompt
    assert "UNAVAILABLE EVIDENCE: none" not in prompt


def test_preview_failure_degrades_wording_not_the_challenger(monkeypatch):
    def boom(*args, **kwargs):
        raise ValueError("bad row")

    monkeypatch.setattr(sc, "evidence_preview", boom)
    result, captured = _run(monkeypatch, evidence_provenance=PROVENANCE, **OPT_IN)
    assert "not provenance-checked" in captured["layer2"]["prompt"]
    assert "layer3" in captured  # the Challenger call succeeded and the pipeline continued
    assert result["strategic_candidates"]["evidence_provenance_status"] == "SUPPLIED"


def test_guidance_is_deterministic_and_order_independent():
    def block(holdings, watchlist, provenance):
        return optimizer._challenger_evidence_block(
            sc.evidence_preview(holdings, watchlist, REGIME, None, provenance), additional_plans=True)

    first = block(HOLDINGS, WATCHLIST, PROVENANCE)
    reordered = block(list(reversed(HOLDINGS)), list(reversed(WATCHLIST)),
                      dict(reversed(list(PROVENANCE.items()))))
    assert first == reordered == block(HOLDINGS, WATCHLIST, PROVENANCE)
    listing = first[first.index("UNAVAILABLE EVIDENCE ("):]
    assert listing.splitlines()[1:6] == [
        "- signal MISSING: BBB, ZZZ",
        "- fa_score FAILED: BBB",
        "- fa_score MISSING: ZZZ",
        "- ta_score DISABLED: WWW",
        "- ta_score MISSING: ZZZ",
    ]
    assert listing.splitlines()[6] == "- timing_score MISSING: AAA, WWW"


def test_guidance_size_bounded_for_full_universe():
    rows = [{"symbol": f"SYM{i:02d}.BK", "signal": "HOLD", "fa_score": 0, "ta_score": 0,
             "timing_score": 0} for i in range(89)]
    missing = {"status": "MISSING"}
    provenance = {r["symbol"]: {f: missing for f in ("signal", "fa_score", "ta_score", "timing_score")}
                  for r in rows}
    preview = sc.evidence_preview(rows[:5], rows[5:], REGIME, None, provenance)
    assert len(preview["unobserved_evidence"]) == 356
    assert len(optimizer._challenger_evidence_block(preview, additional_plans=True)) < 6000
    assert len(optimizer._challenger_evidence_block(
        {"evidence_provenance_status": "SUPPLIED", "unobserved_evidence": {}},
        additional_plans=True)) < 2500


# ── Wording: direction-aware, generic, no pressure to trade ──────────────────

def test_guidance_states_required_rules_without_advertising_fields():
    text = optimizer._CHALLENGER_EVIDENCE_GUIDANCE
    for phrase in (
        "exact keys of the frozen evidence catalog",
        "defaults standing in for missing analysis, not observed facts",
        "Model scores (fa_score, ta_score, timing_score) alone never verify an action.",
        "observed evidence supporting its direction",
        "An observed SELL or REDUCE signal contradicts a BUY or ACCUMULATE.",
        "An observed SELL signal for the holding is currently required to verify a SELL or REDUCE.",
        "Policy violations, concentration figures and threshold diagnostics are context, not citable",
        "timing_data_available=false means timing is unknown, not poor timing",
        "status=NO_ACTION, strategy_family=null and an empty",
        "legitimate outcome, not a failure",
        "Never fabricate refs",
        "construct trades to satisfy these rules",
    ):
        assert phrase in text, phrase
    lowered = text.lower()
    # D1: no field is presented as a way to pass verification.
    for advertised in ("pe_ratio", "roe", "p/e", "valuation", "to pass", "sufficient"):
        assert advertised not in lowered, advertised
    for pressure in ("must propose", "should propose", "always propose", "prefer rebalanc"):
        assert pressure not in lowered, pressure


# ── Behaviour: rules unchanged, NO_ACTION stays a hold ───────────────────────

def test_null_family_challenger_yields_cautioned_hold(monkeypatch):
    reply = {"status": "NO_ACTION", "strategy_family": None, "observed_evidence_refs": [],
             "cash_balance_target": 20,
             "allocations": [{"s": "AAA", "tw": 60, "sig": "HOLD"}, {"s": "BBB", "tw": 20, "sig": "HOLD"}]}
    result, captured = _run(monkeypatch, l2_reply=reply, evidence_provenance=PROVENANCE, **OPT_IN)
    assert [c["id"] for c in result["strategic_candidates"]["candidates"]] == ["hold-current"]
    selection = result["strategy_selection"]
    assert selection["selected_candidate_id"] == "hold-current"
    assert selection["reason_codes"] == ["CAUTIONED_HOLD"]
    assert "NO_ELIGIBLE_ACTION" in selection["material_uncertainty"]
    assert "committee" not in captured


def test_citing_listed_unavailable_ref_is_still_unknown(monkeypatch):
    reply = {**L2_REPLY, "observed_evidence_refs": ["symbol:AAA:signal", "symbol:AAA:timing_score"]}
    result, captured = _run(monkeypatch, l2_reply=reply, evidence_provenance=PROVENANCE, **OPT_IN)
    assert "symbol:AAA:timing_score" in _listed_refs(captured["layer2"]["prompt"], L2_OUTPUT_LINE)
    proposal = result["strategic_candidates"]["candidates"][1]
    assert "UNKNOWN_EVIDENCE_REF" in proposal["missing_information"]
    assert proposal["eligibility_status"] == "UNVERIFIED"
