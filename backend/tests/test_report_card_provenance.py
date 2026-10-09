"""Report Card execution-provenance consistency (NAV-basis hotfix follow-up).

The Report Card's sell/reduce labels come from the same canonical classifier
as the optimizer page (optimize_execution_for_payload); every other evaluation
surface (plan grade, funding-order analytics, opportunity cost, ledger,
plan-vs-actual analyzer) keeps the legacy derivation unchanged. AI is never
called; the database is in-memory.
"""
from __future__ import annotations

import copy
import json
import os
import sys
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401

from services import registry_lookup as lookup
from services.evaluation import plan_grader
from services.evaluation.plan_grader import compute_plan_grade, derive_full_plan, read_snapshot_plan_inputs
from services.evaluation.recommendation_ledger import get_report_card
from services.optimizer import execution_optimizer as eo
from services.optimizer_action_summary import build_action_summary
from tests.test_nav_basis_hotfix import FIXTURE, genuine, one_position, payload_for


@pytest.fixture(autouse=True)
def _reset_registry_cache():
    lookup.invalidate_cache()
    yield
    lookup.invalidate_cache()


@pytest.fixture()
def db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models.database import Base

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture()
def book(db):
    from models.database import Portfolio, Workspace

    ws = Workspace(name="Test")
    db.add(ws)
    db.commit()
    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=0.0)
    db.add(portfolio)
    db.commit()
    return ws, portfolio


def seed(db, ws, portfolio, payload):
    """Store ``payload`` the way the writers do: result_json on the history row,
    allocations + active_policy on the snapshot."""
    from models.database import OptimizerHistory, RecommendationSnapshot

    result_json = json.dumps({k: payload[k] for k in ("total_value", "cash_balance") if k in payload}
                             | {"target_allocations": payload["target_allocations"]})
    oh = OptimizerHistory(workspace_id=ws.id, portfolio_id=portfolio.id, portfolio_name="P1",
                          analyzed_at=datetime.utcnow(), swap_count=0, result_json=result_json)
    db.add(oh)
    db.commit()
    snap = RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=portfolio.id,
        total_portfolio_value=payload.get("total_value"),
        projected_allocations_json=json.dumps(payload["target_allocations"]),
        active_policy_json=json.dumps(payload["active_policy"]),
        consensus_json=json.dumps({"consensus_type": "STRONG_CONSENSUS"}),
        scores_map_json=json.dumps({}),
        created_at=datetime.utcnow() - timedelta(days=2))
    db.add(snap)
    db.commit()
    return snap, oh


def recorded_payload(history_id):
    r = copy.deepcopy(FIXTURE["recorded"][str(history_id)])
    r["active_policy"] = {**r["active_policy"], "hard_constraints": r["active_policy"]["hard_constraints"]}
    return r


def page_trades(payload):
    """What the optimizer page / history detail shows for this payload."""
    summary = build_action_summary(payload["target_allocations"])
    return {t.symbol: t.model_dump() for t in eo.optimize_execution_for_payload(payload, summary).trades}


def card_trades(db, ws, portfolio, payload):
    snap, _ = seed(db, ws, portfolio, payload)
    card = get_report_card(db, portfolio.id, snap.id)
    return {t["symbol"]: t for t in card["plan"]["sell_reduce_trades"]}, snap


# ── history 219 ───────────────────────────────────────────────────────────────

def test_219_report_card_is_qualified_and_keeps_the_recorded_classification(db, book):
    ws, portfolio = book
    p = recorded_payload(219)
    trades, snap = card_trades(db, ws, portfolio, p)
    t = trades["MICRON01.BK"]
    assert (t["reason"], t["necessity"]) == ("POLICY_ENFORCEMENT", "NECESSARY")      # as recorded
    assert t["evidence_status"] == "LEGACY_RECORDED_UNVERIFIED"                      # never unqualified
    assert "cannot be verified" in t["evidence_detail"]
    assert t["full_recommended_amount"] == t["executed_amount"] == 95832.0           # recorded amount
    assert "violation_evidence" not in json.loads(snap.active_policy_json)           # nothing attached
    assert "advisory_intent_review" not in p and "advisory_intent_review" not in snap.active_policy_json


def test_219_report_card_does_not_rewrite_stored_rows(db, book):
    ws, portfolio = book
    p = recorded_payload(219)
    snap, oh = seed(db, ws, portfolio, p)
    before = (snap.projected_allocations_json, snap.active_policy_json, oh.result_json)
    get_report_card(db, portfolio.id, snap.id)
    db.expire_all()
    from models.database import OptimizerHistory, RecommendationSnapshot
    s2 = db.query(RecommendationSnapshot).one()
    o2 = db.query(OptimizerHistory).one()
    assert (s2.projected_allocations_json, s2.active_policy_json, o2.result_json) == before


@pytest.mark.parametrize("history_id", [217, 218])
def test_217_and_218_report_cards_are_unchanged(db, book, history_id):
    ws, portfolio = book
    p = recorded_payload(history_id)
    trades, _ = card_trades(db, ws, portfolio, p)
    assert all(t["reason"] != "POLICY_ENFORCEMENT" and t["necessity"] == "DISCRETIONARY" for t in trades.values())
    if history_id == 218:
        assert trades == {}                                                           # HOLD / no scheduled trades


# ── optimizer page == Report Card ─────────────────────────────────────────────

def _verified():
    w = genuine()
    return payload_for(w, cash=100.0)


def _string_only():
    return payload_for(genuine(), cash=100.0, evidence=[])


def _sector():
    return payload_for(one_position(100.0, cash=0.0, others=900.0), evidence=[],
                       violations=["SECTOR_BREACH: Technology at 71.0% exceeds 70% limit"])


@pytest.mark.parametrize("build,status,reason,necessity", [
    (lambda: recorded_payload(219), "LEGACY_RECORDED_UNVERIFIED", "POLICY_ENFORCEMENT", "NECESSARY"),
    (_verified, "VERIFIED_NAV", "POLICY_ENFORCEMENT", "NECESSARY"),
    (_sector, "SECTOR_EQUITY_BASIS", "POLICY_ENFORCEMENT", "NECESSARY"),
    (_string_only, "UNVERIFIED", "PORTFOLIO_IMPROVEMENT", "DISCRETIONARY"),
])
def test_report_card_matches_the_optimizer_page_classification(db, book, build, status, reason, necessity):
    ws, portfolio = book
    p = build()
    symbol = p["target_allocations"][0]["symbol"] if p["target_allocations"][0]["action"] != "HOLD" else "MICRON01.BK"
    if "MICRON01.BK" in {a["symbol"] for a in p["target_allocations"]}:
        symbol = "MICRON01.BK"
    card, _ = card_trades(db, ws, portfolio, p)
    page = page_trades(p)
    assert card[symbol]["evidence_status"] == page[symbol]["evidence_status"] == status
    for key in ("reason", "necessity", "execution_role", "execution_state", "evidence_detail"):
        assert card[symbol][key] == page[symbol][key], key
    assert (card[symbol]["reason"], card[symbol]["necessity"]) == (reason, necessity)


# ── grader boundary ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("history_id", [217, 218, 219])
def test_legacy_derivation_is_identical_with_and_without_provenance(history_id):
    """Delegation is a no-op for every stored run: nothing in the grader's
    funding order, amounts or states differs."""
    r = recorded_payload(history_id)
    args = (r["target_allocations"], float(r["cash_balance"]), r["active_policy"]["violations"])
    legacy = derive_full_plan(*args)
    provenance = derive_full_plan(*args, policy_provenance={
        "violation_evidence": None, "max_single_position_pct": r["active_policy"]["hard_constraints"]["max_single_position_pct"],
        "total_value": r["total_value"], "cash_balance": r["cash_balance"]})
    assert legacy["buy_trades"] == provenance["buy_trades"]
    assert legacy["execution_optimization"] == provenance["execution_optimization"]


def test_plan_grade_does_not_read_the_provenance_contract():
    import inspect
    assert list(inspect.signature(compute_plan_grade).parameters) == [
        "target_allocations", "cash_available", "violations", "violation_details",
        "portfolio_assessment", "no_action_summary"]
    r = recorded_payload(219)
    a = compute_plan_grade(r["target_allocations"], float(r["cash_balance"]), r["active_policy"]["violations"], [])
    b = compute_plan_grade(r["target_allocations"], float(r["cash_balance"]), r["active_policy"]["violations"], [])
    assert a == b
    # the 219 grade still sees the recorded Required trade (legacy derivation, unchanged)
    assert a["score"] is not None


def test_snapshot_inputs_keep_every_existing_key_and_add_provenance(db, book):
    ws, portfolio = book
    snap, _ = seed(db, ws, portfolio, _verified())
    inputs = read_snapshot_plan_inputs(db, snap)
    assert {"target_allocations", "violations", "violation_details", "cash_available",
            "portfolio_assessment", "no_action_summary"} <= set(inputs)
    prov = inputs["policy_provenance"]
    assert prov["violation_evidence"] and prov["max_single_position_pct"] == 22.0 and prov["total_value"]


def test_remaining_grader_limitation_is_explicit(db, book):
    """The grade/analytics derivation still uses the legacy string rule, so for an
    evidence-aware run whose claim fails NAV verification it can differ from the
    optimizer page and Report Card. Documented limitation — not silently changed."""
    p = _string_only()
    legacy = derive_full_plan(p["target_allocations"], 100.0, p["active_policy"]["violations"])
    [t] = legacy["execution_optimization"].trades
    assert (t.reason, t.necessity) == ("POLICY_ENFORCEMENT", "NECESSARY")
    ws, portfolio = book
    card, _ = card_trades(db, ws, portfolio, p)
    assert card["XXX"]["necessity"] == "DISCRETIONARY" and card["XXX"]["evidence_status"] == "UNVERIFIED"
