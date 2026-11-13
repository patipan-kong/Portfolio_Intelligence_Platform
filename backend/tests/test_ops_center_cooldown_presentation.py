"""Phase 4.12: Ops Center presentation of a recommendation cooldown.

COOLDOWN_ACTIVE (set by stabilization) previously fell through to the
first-run / "no recommendation yet" MUJI wording. These tests pin the cooldown
wording and confirm that a verified RISK_CONFLICT stays visible through a
cooldown. Translator tests are pure; the endpoint test runs the real
/analyze/optimizer and snapshot writer on in-memory SQLite with call_ai mocked
(harness from test_advisory_intent_integration). No network or live data.
"""
import json
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from services.translations.muji_translator import (
    COOLDOWN_HEADLINE_TH, COOLDOWN_RISK_NOTE_TH, DECISION_TH, build_muji_translation, translate_decision,
)

FIRST_RUN_HEADLINE = "เริ่มต้นด้วยการอัปเดตมุมมองพอร์ตครั้งแรก"
NO_RECOMMENDATION = "ยังไม่มีคำแนะนำ — ลองอัปเดตมุมมองพอร์ตครั้งแรก"
ATTENTION_HEADLINE = "มีจุดที่ควรให้ความสนใจในพอร์ตของคุณ"
RISK_CONFLICT_TH = "มุมมองด้านความเสี่ยงยังไม่สอดคล้องกัน ควรพิจารณาด้วยความระมัดระวัง"


def translate(decision, consensus_type="STRONG_CONSENSUS", stations=None, emergency=False):
    return build_muji_translation(
        regime="SIDEWAYS", consensus_type=consensus_type, consensus_decision=decision, risk_level="medium",
        emergency_override=emergency, station_statuses=stations or {"consensus_room": "GREEN"},
        goal_progress_pct=None, days_since_rebalance=None,
    )


# ── Translator ────────────────────────────────────────────────────────────────

def test_ordinary_cooldown_has_cooldown_headline_and_action():
    m = translate("COOLDOWN_ACTIVE")
    assert m["headline"] == COOLDOWN_HEADLINE_TH
    action = m["action_required"]
    assert action["action_th"] == DECISION_TH["COOLDOWN_ACTIVE"]["action_th"]
    assert action["severity"] == "WARN"          # not INFO, which the MUJI ActionCard renders as all-clear
    assert action["link"] == "/optimizer"        # latest recommendation stays one click away
    assert action["required"] is False           # nothing to execute during the cooldown
    assert DECISION_TH["COOLDOWN_ACTIVE"]["action_th"] in m["summary"]


@pytest.mark.parametrize("decision", ["COOLDOWN_ACTIVE", "cooldown_active"])
def test_cooldown_never_uses_first_run_or_no_recommendation_wording(decision):
    m = translate(decision)
    assert m["headline"] != FIRST_RUN_HEADLINE
    assert m["action_required"]["action_th"] != NO_RECOMMENDATION
    assert NO_RECOMMENDATION not in m["summary"]
    assert translate_decision(decision)["action_th"] != NO_RECOMMENDATION


def test_cooldown_with_risk_conflict_keeps_the_risk_warning():
    m = translate("COOLDOWN_ACTIVE", "RISK_CONFLICT", stations={"consensus_room": "RED"})
    assert m["headline"] == ATTENTION_HEADLINE   # a RED station still wins the headline
    assert RISK_CONFLICT_TH in m["summary"]
    assert COOLDOWN_RISK_NOTE_TH in m["action_required"]["action_th"]
    assert m["action_required"]["severity"] == "WARN"
    # Even without a RED station the cooldown action carries the risk note.
    assert COOLDOWN_RISK_NOTE_TH in translate("COOLDOWN_ACTIVE", "RISK_CONFLICT")["action_required"]["action_th"]
    assert COOLDOWN_RISK_NOTE_TH not in translate("COOLDOWN_ACTIVE")["action_required"]["action_th"]


@pytest.mark.parametrize("consensus_type", ["STRONG_CONSENSUS", "RISK_CONFLICT"])
def test_cooldown_wording_does_not_claim_a_trade_was_executed(consensus_type):
    m = translate("COOLDOWN_ACTIVE", consensus_type)
    for text in (m["headline"], m["action_required"]["action_th"]):
        assert "แล้ว" not in text                 # no "already rebalanced / traded"
        assert "rebalanced" not in text.lower()
    assert "คำแนะนำ" in m["headline"]             # it is a recommendation cooldown


@pytest.mark.parametrize("decision, headline, action_th, severity, required, link", [
    ("REBALANCE", "มีคำแนะนำให้ปรับสัดส่วนพอร์ต",
     "แนะนำให้ปรับสัดส่วนพอร์ต — ดูแผนการลงทุนเพื่อดูรายละเอียด", "ACTION", True, "/optimizer"),
    ("REVIEW", "คำแนะนำวันนี้", "ควรเข้าไปตรวจสอบแผนการลงทุนล่าสุด", "WARN", True, "/optimizer"),
    ("NO_ACTION", "พอร์ตของคุณอยู่ในสถานะดี ไม่ต้องทำอะไรเพิ่ม",
     "ไม่ต้องทำอะไรตอนนี้ ถือพอร์ตต่อได้", "INFO", False, None),
    (None, FIRST_RUN_HEADLINE, NO_RECOMMENDATION, "INFO", False, None),
])
def test_existing_mappings_are_unchanged(decision, headline, action_th, severity, required, link):
    for consensus_type in ("STRONG_CONSENSUS", "RISK_CONFLICT"):
        m = translate(decision, consensus_type)
        assert m["headline"] == headline
        assert m["action_required"] == {"required": required, "action_th": action_th,
                                        "severity": severity, "link": link}


def test_emergency_override_still_takes_precedence_over_cooldown():
    m = translate("COOLDOWN_ACTIVE", emergency=True)
    assert m["headline"] == "กรอบการลงทุนเข้าสู่โหมดป้องกันพิเศษ — โปรดตรวจสอบ"
    assert m["action_required"]["severity"] == "ACTION" and m["action_required"]["required"] is True


@pytest.mark.parametrize("decision, consensus_type", [
    (None, None), ("", ""), ("SOMETHING_NEW", None), ("NO_REBALANCE_REQUIRED", None), ("COOLDOWN_ACTIVE", None),
])
def test_missing_or_unknown_fields_degrade_safely(decision, consensus_type):
    m = build_muji_translation(regime=None, consensus_type=consensus_type, consensus_decision=decision,
                               risk_level=None, emergency_override=False, station_statuses={},
                               goal_progress_pct=None, days_since_rebalance=None)
    assert isinstance(m["headline"], str) and m["headline"]
    assert m["summary"] and all(isinstance(s, str) and "None" not in s for s in m["summary"])
    assert set(m["action_required"]) == {"required", "action_th", "severity", "link"}
    assert m["action_required"]["severity"] in ("INFO", "WARN", "ACTION")


# ── Endpoint → snapshot → Ops Center ──────────────────────────────────────────

W = round(500_000 / 3_000_000 * 100, 2)        # five 500,000 holdings + 500,000 cash → each 16.67%


@pytest.fixture
def ops_run(monkeypatch):
    """Run the real optimizer inside an active cooldown, then build the Ops Center payload."""
    from tests import test_advisory_intent_integration as h
    from models.database import OptimizerHistory, RecommendationSnapshot
    from services import operations_center
    from services.decision_memory.snapshot_writer import write_recommendation_snapshot

    def make(l3):
        # AAA REDUCE to 10% + WWW BUY 20%: the proposal leaves 3.3% cash (< 5% floor), which is
        # producer evidence policy:0. The final plan no longer breaches it, so the cooldown applies.
        plan = h.l2(*[h.alloc(s, *({"AAA": (10, "REDUCE")}.get(s, (W, "HOLD")))) for s in h.HELD],
                    h.alloc("WWW", 20, "BUY"))
        monkeypatch.delenv(h.FLAG, raising=False)
        h.patch_pipeline(monkeypatch, h.FakeAI(plan, l3=l3), snapshot_writer=write_recommendation_snapshot)
        monkeypatch.setattr(operations_center, "_regime_cache", {})
        db = h.session()
        p = h.seed(db, h.book(), cash=500_000, sell_signal=("AAA",))
        db.add(OptimizerHistory(workspace_id=p.workspace_id, portfolio_id=p.id, portfolio_name="P",
                                analyzed_at=datetime.utcnow() - timedelta(days=2), swap_count=0,
                                optimizer_status="REBALANCE",
                                result_json=json.dumps({"status": "REBALANCE", "market_regime": {"regime": "SIDEWAYS"},
                                                        "target_allocations": [{"symbol": "AAA", "action": "BUY"}]})))
        db.commit()
        response = h.run(db, p)
        snap = db.query(RecommendationSnapshot).filter_by(optimizer_history_id=response["history_id"]).one()
        return response, snap, operations_center.build_operations_status(db, p.workspace_id, p.id)
    return make


VERIFIED_CRITICAL = {"risk_flags": [{"symbol": "PORTFOLIO", "issue": "Proposal breaches the cash floor",
                                     "severity": "CRITICAL", "category": "INVESTMENT_RISK",
                                     "claim_kind": "POLICY_BREACH", "evidence_ref": "policy:0"}],
                     "safer_choice": "neither", "final_risk_level": "high", "auditor_notes": "x"}


def test_verified_risk_conflict_survives_cooldown_into_snapshot_and_ops_center(ops_run):
    response, snap, ops = ops_run(VERIFIED_CRITICAL)
    # Backend behavior is unchanged (Phase 4.11 Option D): the cooldown relabels the decision.
    assert response["status"] == response["consensus"]["consensus_decision"] == "COOLDOWN_ACTIVE"
    assert any(a["action"] != "HOLD" for a in response["target_allocations"])
    # The verified evidence survives in the frozen snapshot.
    consensus = json.loads(snap.consensus_json)
    assert consensus["consensus_type"] == "RISK_CONFLICT"
    [verified] = json.loads(snap.layer3_output_json)["risk_flags"]
    assert (verified["severity"], verified["validation_status"], verified["evidence_ref"]) == \
        ("CRITICAL", "VERIFIED", "policy:0")
    # Ops Center shows the risk and the cooldown, never "no recommendation yet".
    assert ops["optimizer"]["consensus_status"] == "RISK_CONFLICT"
    assert ops["optimizer"]["consensus_decision"] == ops["optimizer"]["optimizer_status"] == "COOLDOWN_ACTIVE"
    assert ops["agent_health"]["consensus_room"]["status"] == "RED"
    muji = ops["muji_translation"]
    assert muji["headline"] == ATTENTION_HEADLINE
    assert RISK_CONFLICT_TH in muji["summary"]
    action = muji["action_required"]
    assert COOLDOWN_RISK_NOTE_TH in action["action_th"] and NO_RECOMMENDATION not in action["action_th"]
    assert (action["severity"], action["link"]) == ("WARN", "/optimizer")


def test_ordinary_cooldown_in_ops_center(ops_run):
    response, _, ops = ops_run(None)
    assert response["status"] == "COOLDOWN_ACTIVE"
    assert ops["optimizer"]["consensus_status"] != "RISK_CONFLICT"
    assert ops["agent_health"]["consensus_room"]["status"] != "RED"
    muji = ops["muji_translation"]
    # Unrelated stations (e.g. no NAV snapshot in this fixture) may be RED and win the headline.
    red = [k for k, v in ops["agent_health"].items() if v["status"] == "RED"]
    assert muji["headline"] == (ATTENTION_HEADLINE if red else COOLDOWN_HEADLINE_TH)
    assert muji["headline"] != FIRST_RUN_HEADLINE
    assert muji["action_required"]["action_th"] == DECISION_TH["COOLDOWN_ACTIVE"]["action_th"]
    assert (muji["action_required"]["severity"], muji["action_required"]["link"]) == ("WARN", "/optimizer")
