"""NAV-basis correctness hotfix (history 219 / snapshot 175).

Position weights are value / NAV (cash included) for single-position policy,
breach severity, stabilization inputs, allocation deltas and execution
amounts. Verified POLICY_ENFORCEMENT needs structured NAV-basis evidence;
stored runs keep their recorded classification, qualified, never relabeled.

AI is stubbed throughout (FakeAI / call_ai). No provider, network or paid
call can happen, and nothing touches a real database.
"""
import asyncio
import copy
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

import main
import agents.optimizer as optimizer
from agents.optimizer import _compute_portfolio_weights, _normalize_allocations
from models.database import OptimizerHistory, Portfolio
from services.optimizer import execution_optimizer as eo
from services.optimizer.nav_basis import compute_nav_basis
from services.optimizer.policy_engine import (
    HardConstraints, _detect_violations, compute_concentration_breach_severity,
    detect_concentration_evidence,
)
from services.optimizer_action_summary import build_action_summary
import tests.test_advisory_intent_integration as H
from tests.test_advisory_intent_integration import (
    FLAG, FakeAI, HELD, CASH, book, l2, alloc, patch_pipeline, plan, position, run, seed, session, set_intent,
)

with open(os.path.join(os.path.dirname(__file__), "fixtures", "history_219_nav_basis.json"), encoding="utf-8") as fh:
    FIXTURE = json.load(fh)
INPUTS = FIXTURE["inputs219"]
NAV_219 = INPUTS["nav"]
CASH_219 = INPUTS["cash"]
LIMIT = float(INPUTS["limit_pct"])


def hard(limit=LIMIT):
    return HardConstraints(min_cash_pct=5, max_single_position_pct=limit, max_sector_pct=70,
                           max_turnover_pct=60, suppress_speculative=False, beta_ceiling=None,
                           max_new_positions=3)


def items_219():
    return [{"symbol": h["symbol"], "shares": h["shares"], "current_price": h["price"], "sector": h["sector"]}
            for h in INPUTS["holdings"]]


def one_position(value, cash, others=0.0, symbol="XXX"):
    """A book where XXX is worth ``value`` and the rest of equity is ``others``."""
    items = [{"symbol": symbol, "shares": 1, "current_price": value, "sector": "Technology"}]
    if others:   # spread across ten small positions so none of them breaches by itself
        items += [{"symbol": f"O{i}", "shares": 1, "current_price": others / 10, "sector": "Financial"}
                  for i in range(10)]
    return _compute_portfolio_weights(items, cash)


def payload_for(weighted, *, limit=LIMIT, nav=None, cash=0.0, current_weight=None, symbol="XXX",
                target=10.0, evidence="auto", violations="auto"):
    """A minimal result payload carrying one REDUCE on ``symbol``."""
    item = next(i for i in weighted if i["symbol"] == symbol)
    w = item["weight_pct"]
    ev = detect_concentration_evidence(weighted, hard(limit)) if evidence == "auto" else evidence
    viol = (_detect_violations(weighted, hard(limit)) if violations == "auto" else violations)
    nav = weighted[0]["nav_value"] if nav is None else nav
    cw = round(w, 2) if current_weight is None else current_weight
    row = {"symbol": symbol, "current_weight": cw, "target_weight": target, "action": "REDUCE",
           "allocation_change_percent": round(target - cw, 2),
           "estimated_amount": round((target - cw) / 100 * nav), "sector": "Technology"}
    active = {"hard_constraints": {"max_single_position_pct": limit}, "violations": viol}
    if ev is not None:
        active["violation_evidence"] = ev
    return {"total_value": round(nav, 2), "cash_balance": cash, "target_allocations": [row],
            "active_policy": active}


def exec_trade(payload, symbol="XXX"):
    summary = build_action_summary(payload["target_allocations"])
    result = eo.optimize_execution_for_payload(payload, summary)
    return next(t for t in result.trades if t.symbol == symbol)


# ── 1. NAV weights: history 219 reproduction + negative control ───────────────

def test_219_nav_weights_and_no_breach():
    weighted = _compute_portfolio_weights(items_219(), CASH_219)
    w = {i["symbol"]: i["weight_pct"] for i in weighted}
    assert weighted[0]["nav_value"] == pytest.approx(NAV_219, abs=0.01)
    assert w["MICRON01.BK"] == pytest.approx(15.7296, abs=1e-3)          # not 22.2
    assert max(w.values()) < LIMIT
    assert sum(w.values()) + CASH_219 / weighted[0]["nav_value"] * 100 == pytest.approx(100.0, abs=1e-9)
    assert _detect_violations(weighted, hard()) == []
    assert detect_concentration_evidence(weighted, hard()) == []
    assert compute_concentration_breach_severity(weighted, LIMIT, 70)[0] == "NONE"


def test_219_negative_control_equity_only_weights_reproduce_the_false_breach():
    weighted = _compute_portfolio_weights(items_219(), CASH_219)
    legacy = [{**i, "weight_pct": i["equity_weight_pct"]} for i in weighted]
    for stored in (INPUTS["stored_equity_weights"],):
        assert {i["symbol"]: i["weight_pct"] for i in legacy} == pytest.approx(stored, abs=0.05)
    assert any("CONCENTRATION_BREACH: MICRON01.BK at 22.2%" in v for v in _detect_violations(legacy, hard()))
    assert compute_concentration_breach_severity(legacy, LIMIT, 70)[0] != "NONE"
    # No NAV basis marker → no evidence can be produced from legacy weights.
    assert detect_concentration_evidence([{k: v for k, v in i.items() if k != "weight_basis"} for i in legacy],
                                         hard()) == []


def test_219_delta_and_amount_before_after():
    weighted = _compute_portfolio_weights(items_219(), CASH_219)
    target = [{"symbol": "MICRON01.BK", "target_weight": 12.5, "action": "REDUCE"}]
    nav_map = {i["symbol"]: i["weight_pct"] for i in weighted}
    [row] = _normalize_allocations(target, nav_map)
    assert (row["current_weight"], row["allocation_change_percent"]) == (15.73, -3.23)
    assert round(row["allocation_change_percent"] / 100 * NAV_219) == -31911
    # Negative control: mixed denominators reproduce the stored defect exactly.
    stored = INPUTS["stored_micron"]
    [bad] = _normalize_allocations(target, {"MICRON01.BK": stored["current_weight"]})
    assert bad["allocation_change_percent"] == stored["allocation_change_percent"]
    assert round(bad["allocation_change_percent"] / 100 * NAV_219) == stored["estimated_amount"]


# ── 2. Precision, cash-heavy, zero-cash, thresholds ───────────────────────────

def test_weights_are_unrounded_and_cash_is_in_the_denominator():
    [a, b] = _compute_portfolio_weights(
        [{"symbol": "A", "shares": 3, "current_price": 7.0}, {"symbol": "B", "shares": 1, "current_price": 11.0}], 5.0)
    assert a["weight_pct"] == pytest.approx(21 / 37 * 100, rel=1e-12) and a["weight_pct"] != round(a["weight_pct"], 1)
    assert b["weight_basis"] == "NAV" and b["nav_value"] == 37.0 and b["nav_cash"] == 5.0
    assert compute_nav_basis([{"symbol": "A", "shares": 1, "current_price": 1}], None).nav == 1.0


def test_zero_cash_nav_weights_equal_the_legacy_equity_weights():
    for i in _compute_portfolio_weights(items_219(), 0.0):
        assert i["weight_pct"] == pytest.approx(i["equity_weight_pct"], abs=0.05)
        assert i["nav_value"] == pytest.approx(sum(h["shares"] * h["price"] for h in INPUTS["holdings"]))


def test_cash_heavy_book_has_no_false_breach():
    # 22.2% of equity but only 8% of NAV (cash 63%).
    weighted = one_position(80.0, cash=630.0, others=290.0)
    assert weighted[0]["equity_weight_pct"] == pytest.approx(21.6, abs=0.1)
    assert weighted[0]["weight_pct"] == pytest.approx(8.0)
    assert _detect_violations(weighted, hard(7.9)) != [] and _detect_violations(weighted, hard(8.1)) == []
    assert _detect_violations(weighted, hard(22.0)) == []


def test_unrounded_boundary_around_the_threshold():
    exactly = one_position(22.0, cash=0.0, others=78.0)
    assert exactly[0]["weight_pct"] == 22.0
    assert _detect_violations(exactly, hard(22.0)) == [] and detect_concentration_evidence(exactly, hard(22.0)) == []
    # 21.96% displays as "22.0" but is NOT above 22 — no breach, no evidence.
    below = one_position(21.96, cash=0.0, others=78.04)
    assert f"{below[0]['weight_pct']:.1f}" == "22.0"
    assert _detect_violations(below, hard(22.0)) == [] and detect_concentration_evidence(below, hard(22.0)) == []
    # 22.04% is above 22 although a 1 dp view would say 22.0.
    above = one_position(22.04, cash=0.0, others=77.96)
    assert f"{above[0]['weight_pct']:.1f}" == "22.0"
    assert len(_detect_violations(above, hard(22.0))) == 1 and len(detect_concentration_evidence(above, hard(22.0))) == 1
    just = one_position(22.000001, cash=0.0, others=77.999999)
    assert len(detect_concentration_evidence(just, hard(22.0))) == 1


# ── 3. Structured evidence verification ───────────────────────────────────────

def genuine():
    return one_position(240.0, cash=100.0, others=660.0)       # 24% of NAV 1000


def test_genuine_breach_is_verified_policy_enforcement():
    w = genuine()
    [ev] = detect_concentration_evidence(w, hard())
    assert ev["basis"] == "NAV" and ev["observed_pct"] == pytest.approx(24.0) and ev["nav"] == 1000.0
    trade = exec_trade(payload_for(w, cash=100.0))
    assert (trade.reason, trade.necessity, trade.evidence_status) == (
        "POLICY_ENFORCEMENT", "NECESSARY", "VERIFIED_NAV")


def test_no_breach_is_not_required():
    w = one_position(150.0, cash=100.0, others=750.0)
    trade = exec_trade(payload_for(w, cash=100.0))
    assert (trade.reason, trade.necessity, trade.evidence_status) == ("PORTFOLIO_IMPROVEMENT", "DISCRETIONARY", "NOT_APPLICABLE")


@pytest.mark.parametrize("mutate,detail", [
    (lambda ev: ev.update(basis="EQUITY"), "BASIS_NOT_NAV"),
    (lambda ev: ev.update(nav=1500.0), "VALUATION_MISMATCH"),
    (lambda ev: ev.update(cash=0.0), "VALUATION_MISMATCH"),
    (lambda ev: ev.update(observed_pct=30.0), "EVIDENCE_INCONSISTENT"),
    (lambda ev: ev.update(limit_pct=10.0), "LIMIT_MISMATCH"),
    (lambda ev: ev.update(rule="other.rule"), "RULE_MISMATCH"),
    (lambda ev: ev.update(evidence_version="v0"), "EVIDENCE_VERSION"),
    (lambda ev: ev.pop("position_value"), "EVIDENCE_MALFORMED"),
    (lambda ev: ev.update(position_value=float("nan")), "EVIDENCE_MALFORMED"),
    (lambda ev: ev.update(symbol="OTHER"), "NO_EVIDENCE"),
])
def test_tampered_or_mismatched_evidence_fails_closed(mutate, detail):
    w = genuine()
    p = payload_for(w, cash=100.0)
    mutate(p["active_policy"]["violation_evidence"][0])
    trade = exec_trade(p)
    assert (trade.reason, trade.necessity, trade.evidence_status, trade.evidence_detail) == (
        "PORTFOLIO_IMPROVEMENT", "DISCRETIONARY", "UNVERIFIED", detail)


def test_evidence_must_be_consistent_with_the_allocation_current_weight():
    w = genuine()
    trade = exec_trade(payload_for(w, cash=100.0, current_weight=15.73))   # the history-219 shape
    assert (trade.reason, trade.evidence_status, trade.evidence_detail) == (
        "PORTFOLIO_IMPROVEMENT", "UNVERIFIED", "WEIGHT_MISMATCH")


def test_non_breach_evidence_is_rejected_even_with_a_matching_string():
    w = one_position(150.0, cash=100.0, others=750.0)
    p = payload_for(w, cash=100.0, violations=["CONCENTRATION_BREACH: XXX at 15.0% exceeds 22% single-position policy limit"],
                    evidence=[{**genuine_ev(), "position_value": 150.0, "observed_pct": 15.0, "nav": 1000.0, "cash": 100.0}])
    trade = exec_trade(p)
    assert (trade.reason, trade.evidence_status, trade.evidence_detail) == ("PORTFOLIO_IMPROVEMENT", "UNVERIFIED", "NOT_A_BREACH")


def genuine_ev():
    return detect_concentration_evidence(genuine(), hard())[0]


def test_string_only_violation_never_authorizes_enforcement():
    w = genuine()
    p = payload_for(w, cash=100.0, evidence=[])        # evidence-aware run, but no evidence for XXX
    assert p["active_policy"]["violations"], "the string claim is present"
    trade = exec_trade(p)
    assert (trade.reason, trade.necessity, trade.evidence_status, trade.evidence_detail) == (
        "PORTFOLIO_IMPROVEMENT", "DISCRETIONARY", "UNVERIFIED", "NO_EVIDENCE")


def test_model_text_and_labels_are_not_inputs():
    w = genuine()
    p = payload_for(w, cash=100.0, evidence=[])
    p["target_allocations"][0]["reason"] = "Address mandated concentration remediation"
    p["layer3_result"] = {"claim_reviews": [{"claim_kind": "POLICY_BREACH", "symbol": "XXX", "validation_status": "VALIDATED"}]}
    assert exec_trade(p).necessity == "DISCRETIONARY"


def test_sell_remains_action_derived_mandatory_risk_reduction():
    p = payload_for(one_position(100.0, cash=0.0, others=900.0), evidence=[])
    p["target_allocations"][0]["action"] = "SELL"
    trade = exec_trade(p)
    assert (trade.reason, trade.necessity) == ("MANDATORY_RISK_REDUCTION", "NECESSARY")


def test_sector_breach_behavior_is_preserved_and_qualified():
    p = payload_for(one_position(100.0, cash=0.0, others=900.0), evidence=[],
                    violations=["SECTOR_BREACH: Technology at 71.0% exceeds 70% limit"])
    trade = exec_trade(p)
    assert (trade.reason, trade.necessity, trade.evidence_status) == ("POLICY_ENFORCEMENT", "NECESSARY", "SECTOR_EQUITY_BASIS")


# ── 4. Historical compatibility ───────────────────────────────────────────────

def recorded(history_id):
    r = copy.deepcopy(FIXTURE["recorded"][str(history_id)])
    return r


def test_219_recorded_classification_is_preserved_and_qualified_not_relabeled():
    r = recorded(219)
    assert "violation_evidence" not in r["active_policy"]          # stored before evidence existed
    summary = build_action_summary(r["target_allocations"])
    trade = next(t for t in eo.optimize_execution_for_payload(r, summary).trades if t.symbol == "MICRON01.BK")
    # As recorded (what the user saw): Required / Policy enforcement ...
    assert (trade.reason, trade.necessity) == ("POLICY_ENFORCEMENT", "NECESSARY")
    # ... qualified as never NAV-verified.
    assert trade.evidence_status == "LEGACY_RECORDED_UNVERIFIED"
    assert "equity-only" in trade.evidence_detail and "cannot be verified" in trade.evidence_detail
    assert trade.full_recommended_amount == 95832.0              # original numbers untouched


@pytest.mark.parametrize("history_id", [217, 218])
def test_217_218_are_unchanged_by_the_new_logic(history_id):
    r = recorded(history_id)
    summary = build_action_summary(r["target_allocations"])
    result = eo.optimize_execution_for_payload(r, summary)
    legacy = eo.optimize_execution(summary, r["target_allocations"], float(r["cash_balance"]),
                                   violations=r["active_policy"]["violations"])      # legacy_recorded default
    assert [t.model_dump(exclude={"evidence_status", "evidence_detail"}) for t in result.trades] == \
           [t.model_dump(exclude={"evidence_status", "evidence_detail"}) for t in legacy.trades]
    assert all(t.reason != "POLICY_ENFORCEMENT" for t in result.trades)            # no violations in 217/218


def test_history_read_derives_but_never_rewrites_the_stored_row(monkeypatch):
    monkeypatch.delenv(FLAG, raising=False)
    db = session()
    ws = main._ws_id(db)
    p = Portfolio(workspace_id=ws, name="P", cash_balance=0)
    db.add(p)
    db.flush()
    stored = recorded(219)
    stored["history_id"] = 219
    blob = json.dumps(stored)
    row = OptimizerHistory(workspace_id=ws, portfolio_id=p.id, portfolio_name="P",
                           analyzed_at=datetime.utcnow(), result_json=blob)
    db.add(row)
    db.commit()
    detail = asyncio.run(main.get_optimizer_history_detail(row.id, db))
    trade = next(t for t in detail["execution_optimization"]["trades"] if t["symbol"] == "MICRON01.BK")
    assert (trade["reason"], trade["necessity"], trade["evidence_status"]) == (
        "POLICY_ENFORCEMENT", "NECESSARY", "LEGACY_RECORDED_UNVERIFIED")
    db.expire_all()
    assert db.query(OptimizerHistory).one().result_json == blob               # byte-identical
    assert "violation_evidence" not in detail["active_policy"]               # no current evidence attached
    assert "advisory_intent_review" not in detail                            # no retroactive Intent


# ── 5. End to end (stubbed AI): flag OFF / ON, DR cap, Intent ────────────────

def holdings_219_e2e(monkeypatch):
    # Sectors are spread out here so a (separately documented) equity-basis sector
    # breach cannot interfere with the single-position assertions.
    spread = {"AAPL01.BK": "Industrial", "BH.BK": "Healthcare", "GOOGL01.BK": "Consumer",
              "MICRON01.BK": "Technology", "NVDA01.BK": "Financial", "GULF.BK": "Other"}
    for h in INPUTS["holdings"]:
        monkeypatch.setitem(H.SECTORS, h["symbol"], spread[h["symbol"]])
    holdings = {h["symbol"]: (h["shares"], True) for h in INPUTS["holdings"]}
    quotes = {h["symbol"]: {"current_price": h["price"]} for h in INPUTS["holdings"]}
    return holdings, quotes


def micron_plan():
    nav = {h["symbol"]: h["shares"] * h["price"] / NAV_219 * 100 for h in INPUTS["holdings"]}
    rows = [alloc(s, round(w, 2), "HOLD") for s, w in nav.items() if s != "MICRON01.BK"]
    rows.append(alloc("MICRON01.BK", 12.5, "REDUCE", "Address mandated concentration remediation"))
    return l2(*rows)


def run_219(monkeypatch, *, flag, legacy_weights=False):
    if flag:
        monkeypatch.setenv(FLAG, "true")
    else:
        monkeypatch.delenv(FLAG, raising=False)
    holdings, quotes = holdings_219_e2e(monkeypatch)
    patch_pipeline(monkeypatch, FakeAI(micron_plan()), quotes=quotes)
    if legacy_weights:
        real = optimizer._compute_portfolio_weights

        def equity_only(items, cash_balance=0.0):
            return [{**{k: v for k, v in r.items() if k not in ("weight_basis", "nav_value", "nav_cash", "value_exact")},
                     "weight_pct": round(r["equity_weight_pct"], 1)} for r in real(items, cash_balance)]

        monkeypatch.setattr(optimizer, "_compute_portfolio_weights", equity_only)
    db = session()
    portfolio = seed(db, holdings, cash=CASH_219)
    return db, portfolio, run(db, portfolio)


def micron_row(response):
    return next(a for a in response["target_allocations"] if a["symbol"] == "MICRON01.BK")


def micron_trade(response):
    return next((t for t in response["execution_optimization"]["trades"] if t["symbol"] == "MICRON01.BK"), None)


def test_e2e_219_flag_off_uses_nav_basis_everywhere(monkeypatch):
    _, _, response = run_219(monkeypatch, flag=False)
    row = micron_row(response)
    assert (row["current_weight"], row["allocation_change_percent"]) == (15.73, -3.23)
    assert row["estimated_amount"] == round(-3.23 / 100 * response["total_value"]) == -31911
    policy = response["active_policy"]
    assert policy["violations"] == [] and policy["violation_evidence"] == []
    assert policy["turnover_relaxation_active"] is False
    assert "SINGLE_POSITION_BREACH" not in response["stabilization"].get("overrides_active", [])
    assert "advisory_intent_review" not in response                 # flag off: nothing captured
    trade = micron_trade(response)
    if trade is not None:
        assert (trade["reason"], trade["necessity"]) == ("PORTFOLIO_IMPROVEMENT", "DISCRETIONARY")


def test_e2e_219_negative_control_reproduces_the_defect_and_fails_closed(monkeypatch):
    _, _, response = run_219(monkeypatch, flag=False, legacy_weights=True)
    row = micron_row(response)
    assert (row["current_weight"], row["allocation_change_percent"], row["estimated_amount"]) == (22.2, -9.7, -95832)
    assert any("CONCENTRATION_BREACH: MICRON01.BK at 22.2%" in v for v in response["active_policy"]["violations"])
    assert response["active_policy"]["violation_evidence"] == []
    trade = micron_trade(response)
    assert trade is not None
    # The string alone no longer authorizes a Required trade.
    assert (trade["reason"], trade["necessity"], trade["evidence_status"], trade["evidence_detail"]) == (
        "PORTFOLIO_IMPROVEMENT", "DISCRETIONARY", "UNVERIFIED", "NO_EVIDENCE")


def test_e2e_flag_on_and_off_agree_on_deterministic_nav_calculations(monkeypatch):
    _, _, off = run_219(monkeypatch, flag=False)
    _, _, on = run_219(monkeypatch, flag=True)
    assert on["advisory_intent_review_status"] == "CAPTURED"
    for key in ("violations", "violation_evidence", "turnover_relaxation_active"):
        assert on["active_policy"][key] == off["active_policy"][key]
    rows_off = {a["symbol"]: a for a in off["target_allocations"]}
    for a in on["target_allocations"]:
        o = rows_off[a["symbol"]]
        assert a["current_weight"] == pytest.approx(o["current_weight"], abs=0.01)
        assert a["allocation_change_percent"] == pytest.approx(o["allocation_change_percent"], abs=0.011)
        assert abs(a["estimated_amount"] - o["estimated_amount"]) <= 0.0002 * NAV_219
    assert on["stabilization"]["overrides_active"] == off["stabilization"]["overrides_active"]


def test_e2e_genuine_breach_with_intent_conflict_is_verified_but_still_advisory(monkeypatch):
    monkeypatch.setenv(FLAG, "true")
    ai = FakeAI(plan(AAA=(15, "REDUCE")))
    patch_pipeline(monkeypatch, ai)
    db = session()
    # AAA 27,000 sh x 50 = 1.35M of NAV 5.85M = 23.08% > 22% cap.
    p = seed(db, book(AAA=(27_000, True)), cash=CASH)
    set_intent(db, p, "AAA", dec=True)                     # owner: do not decrease
    response = run(db, p)
    aaa_w = next(a for a in response["target_allocations"] if a["symbol"] == "AAA")["current_weight"]
    assert aaa_w == pytest.approx(23.08, abs=0.01)
    [ev] = [e for e in response["active_policy"]["violation_evidence"] if e["symbol"] == "AAA"]
    assert ev["basis"] == "NAV" and ev["observed_pct"] > ev["limit_pct"]
    trade = next(t for t in response["execution_optimization"]["trades"] if t["symbol"] == "AAA")
    assert (trade["reason"], trade["necessity"], trade["evidence_status"]) == (
        "POLICY_ENFORCEMENT", "NECESSARY", "VERIFIED_NAV")
    review = position(response["advisory_intent_review"], "AAA")["review"]
    assert review["final"]["outcome"] == "CONFLICT" and review["requires_owner_decision"] is True
    assert response["advisory_intent_review"]["review"]["allocations_changed_by_review"] is False
    assert trade["executed_amount"] == trade["full_recommended_amount"] > 0     # advisory: not blocked


def test_e2e_no_breach_on_the_standard_book(monkeypatch):
    monkeypatch.delenv(FLAG, raising=False)
    patch_pipeline(monkeypatch, FakeAI(plan(AAA=(5, "REDUCE"))))
    db = session()
    p = seed(db, book(), cash=CASH)
    response = run(db, p)
    assert response["active_policy"]["violations"] == [] and response["active_policy"]["violation_evidence"] == []
    assert next(a for a in response["target_allocations"] if a["symbol"] == "AAA")["current_weight"] == 10.0


def test_dr_position_above_the_buy_only_cap_is_not_liquidated_or_required(monkeypatch):
    # DR XXX = 18% of NAV: above the 15% DR cap, below the 22% general limit.
    monkeypatch.setattr(optimizer, "call_ai", FakeAI(l2(alloc("XXX", 18, "HOLD"), alloc("YYY", 20, "HOLD"),
                                                       alloc("NEW", 25, "BUY"), status="NO_ACTION")))
    result = optimizer.run_layered_optimizer(
        [{"symbol": "XXX", "shares": 180, "current_price": 1, "signal": "HOLD", "sector": "Technology"},
         {"symbol": "YYY", "shares": 200, "current_price": 1, "signal": "HOLD", "sector": "Financial"}],
        [{"symbol": "NEW", "sector": "Healthcare", "signal": "BUY", "combined_score": 80}],
        "fixture", cash_balance=620, max_sector_pct=70,
        policy_context={"hard_constraints": {"max_single_position_pct": 22, "min_cash_pct": 3,
                                             "max_sector_pct": 70, "max_turnover_pct": 70}},
        execution_context={"per_symbol": {"XXX": {"position_cap_pct": 15}, "NEW": {"position_cap_pct": 15}}})
    rows = {a["symbol"]: a for a in result["target_allocations"]}
    assert rows["XXX"]["current_weight"] == 18.0 and rows["XXX"]["action"] == "HOLD"
    assert rows["XXX"]["target_weight"] == 18.0                      # cap clamps BUY/ACCUMULATE only
    if "NEW" in rows and rows["NEW"]["action"] in ("BUY", "ACCUMULATE"):
        assert rows["NEW"]["target_weight"] <= 15
    weighted = _compute_portfolio_weights(
        [{"symbol": "XXX", "shares": 180, "current_price": 1}, {"symbol": "YYY", "shares": 200, "current_price": 1}], 620)
    assert detect_concentration_evidence(weighted, hard()) == []     # a DR cap is not a general breach
    p = payload_for(weighted, symbol="XXX", cash=620.0, target=10.0)
    trade = exec_trade(p)
    assert (trade.reason, trade.necessity) == ("PORTFOLIO_IMPROVEMENT", "DISCRETIONARY")


# ── 6. Snapshot-specific decision lookup (backend) ───────────────────────────

def _seed_decisions(db, n, portfolio):
    from datetime import timedelta
    from models.database import UserExecutionDecision
    ws = main._ws_id(db)
    base = datetime(2026, 1, 1)
    for i in range(n):                                  # snapshot i, newer as i grows
        db.add(UserExecutionDecision(
            workspace_id=ws, recommendation_snapshot_id=i + 1, portfolio_id=portfolio.id, decision="APPROVED",
            executed_at=base + timedelta(hours=i), created_at=base + timedelta(hours=i)))
    db.commit()


def _list(db, **kw):
    return asyncio.run(main.list_execution_decisions(db=db, **{"limit": 50, "portfolio_id": None, "decision": None,
                                                              "recommendation_snapshot_id": None, **kw}))


def test_decision_endpoint_snapshot_filter_is_exact_and_not_truncated():
    db = session()
    p = Portfolio(workspace_id=main._ws_id(db), name="P", cash_balance=0)
    db.add(p)
    db.flush()
    _seed_decisions(db, 100, p)                         # the history-219 shape: > 50 decisions
    unfiltered = _list(db, portfolio_id=p.id)
    assert len(unfiltered) == 50 and unfiltered[0]["recommendation_snapshot_id"] == 100
    assert all(d["recommendation_snapshot_id"] > 50 for d in unfiltered)          # snapshot 3 is invisible here
    [hit] = _list(db, portfolio_id=p.id, recommendation_snapshot_id=3, limit=1)
    assert hit["recommendation_snapshot_id"] == 3 and hit["portfolio_id"] == p.id
    assert _list(db, portfolio_id=p.id, recommendation_snapshot_id=175, limit=1) == []     # confirmed empty
    assert len(_list(db, portfolio_id=p.id)) == 50                                 # unfiltered behavior unchanged
    assert _list(db, portfolio_id=p.id + 99, recommendation_snapshot_id=3) == []   # portfolio identity respected
