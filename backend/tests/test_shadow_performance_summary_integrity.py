"""Phase 4.23 — /analytics/shadow-performance summary integrity (backend).

summary.static_frozen must be the LATEST FROZEN DECISION: the newest
decision-keyed STATIC_FROZEN shadow, never a recommendation-keyed one, with
its own since-inception figures, and no invented performance when only the
inception valuation exists. Synthetic in-memory SQLite; Three Portfolios is
stubbed (not under test)."""
from __future__ import annotations

import asyncio
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from test_attribution_static_shadow_selection import (  # noqa: E402,F401
    db, wp, _shadow, _owner, _dip, _portfolio, OWNER_30,
)
from services.analytics.attribution_engine import compute_portfolio_attribution  # noqa: E402


@pytest.fixture(autouse=True)
def _stub_three_portfolios(monkeypatch):
    import services.evaluation.ideal_series as ideal

    monkeypatch.setattr(
        ideal, "compute_three_portfolios",
        lambda *_a, **_k: {"gap_a": {"value": None}, "gap_b": {"value": None}},
    )


def _summary(db, pid):
    import main

    return asyncio.run(main.get_shadow_performance_summary(pid, 90, db))


def _set(db, sh, ret=None, alpha=None):
    from models.database import ShadowPortfolioSnapshot

    sh.inception_return_pct = ret
    last = (db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=sh.id)
            .order_by(ShadowPortfolioSnapshot.snapshot_date.desc()).first())
    if last is not None:
        last.alpha = alpha
    db.commit()


def test_1_newer_recommendation_shadow_does_not_replace_latest_decision(db, wp):
    ws, p = wp
    dec = _shadow(db, ws, p, 20, range(20, -1, -1))
    _set(db, dec, ret=2.5, alpha=0.4)
    rec = _shadow(db, ws, p, 0, [0], kind="recommendation")
    _set(db, rec, ret=0.0)
    s = _summary(db, p.id)["summary"]["static_frozen"]
    assert s["shadow_id"] == dec.id
    assert s["execution_decision_id"] == dec.execution_decision_id
    assert s["inception_return_pct"] == 2.5 and s["latest_alpha"] == 0.4


def test_2_latest_decision_selection_is_deterministic(db, wp):
    ws, p = wp
    older = _shadow(db, ws, p, 30, range(30, -1, -1))
    newer = _shadow(db, ws, p, 10, range(10, -1, -1))
    same_day_a = _shadow(db, ws, p, 5, range(5, -1, -1))
    same_day_b = _shadow(db, ws, p, 5, range(5, -1, -1))
    for _ in range(3):
        assert _summary(db, p.id)["summary"]["static_frozen"]["shadow_id"] == max(
            same_day_a.id, same_day_b.id)
    assert older.id != newer.id


def test_3_no_decision_shadow_gives_unavailable_static(db, wp):
    ws, p = wp
    rec = _shadow(db, ws, p, 10, range(10, -1, -1), kind="recommendation")
    _set(db, rec, ret=4.0)
    out = _summary(db, p.id)
    assert out["summary"]["static_frozen"] is None
    assert any(x["shadow_id"] == rec.id for x in out["shadows"])  # history untouched


def test_4_inception_only_decision_does_not_invent_performance(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, 0, [0])
    _set(db, sh, ret=0.0, alpha=0.0)
    s = _summary(db, p.id)["summary"]["static_frozen"]
    assert s["shadow_id"] == sh.id
    assert s["inception_return_pct"] is None and s["latest_alpha"] is None
    # the raw history row keeps the stored value untouched
    raw = next(x for x in _summary(db, p.id)["shadows"] if x["shadow_id"] == sh.id)
    assert raw["inception_return_pct"] == 0.0


def test_5_genuine_zero_return_stays_numeric_zero(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, 10, range(10, -1, -1))
    _set(db, sh, ret=0.0, alpha=0.0)
    s = _summary(db, p.id)["summary"]["static_frozen"]
    assert s["inception_return_pct"] == 0.0 and s["latest_alpha"] == 0.0


def test_6_missing_alpha_stays_null(db, wp):
    ws, p = wp
    sh = _shadow(db, ws, p, 10, range(10, -1, -1))
    _set(db, sh, ret=1.0, alpha=None)
    assert _summary(db, p.id)["summary"]["static_frozen"]["latest_alpha"] is None


def test_10_phase_422_attribution_selection_unchanged(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    old = _shadow(db, ws, p, 35, range(35, -1, -1), _dip(35, 12))
    newest = _shadow(db, ws, p, 0, [0])
    assert _summary(db, p.id)["summary"]["static_frozen"]["shadow_id"] == newest.id
    att = compute_portfolio_attribution(db, p.id, 30)
    assert att["static_shadow"]["shadow_id"] == old.id
    assert att["static_shadow_selection"]["status"] == "selected"


def test_11_active_model_summary_unchanged(db, wp):
    ws, p = wp
    ai = _shadow(db, ws, p, 20, range(20, -1, -1), kind="active")
    _set(db, ai, ret=3.0, alpha=0.2)
    out = _summary(db, p.id)["summary"]
    assert out["active_model"]["shadow_id"] == ai.id
    assert out["active_model"]["inception_return_pct"] == 3.0
    assert out["static_frozen"] is None


def test_12_response_stays_backward_compatible(db, wp):
    ws, p = wp
    _shadow(db, ws, p, 10, range(10, -1, -1))
    out = _summary(db, p.id)
    assert {"portfolio_id", "has_shadows", "shadows", "summary", "three_portfolios"} <= set(out)
    assert {"static_frozen", "active_model", "tracking_since"} <= set(out["summary"])
    item = out["shadows"][0]
    assert {"shadow_id", "shadow_type", "inception_return_pct", "latest_alpha",
            "snapshot_count", "last_valued_at"} <= set(item)


# ── Final divergence check: ACTIVE_MODEL window coverage ──────────────────

def test_ai_coverage_full_window(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 60, range(30, -1, -1), kind="active")
    att = compute_portfolio_attribution(db, p.id, 30)
    assert att["ai_model_shadow_coverage"]["window_covered"] is True


def test_ai_coverage_early_inception_but_late_valuations(db, wp):
    # inception predates the window but valuations only cover the last 10 days
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 60, range(10, -1, -1), kind="active")
    att = compute_portfolio_attribution(db, p.id, 30)
    assert att["ai_model_shadow"]["return_pct"] is not None  # figure unchanged
    assert att["ai_model_shadow_coverage"]["window_covered"] is False


def test_ai_coverage_stale_end_and_absent(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 60, range(30, 15, -1), kind="active")  # stops 15 days ago
    assert compute_portfolio_attribution(db, p.id, 30)["ai_model_shadow_coverage"]["window_covered"] is False

    ws2, p2 = _portfolio(db, "P2")
    _owner(db, ws2, p2, range(30, -1, -1), OWNER_30)
    assert compute_portfolio_attribution(db, p2.id, 30)["ai_model_shadow_coverage"] is None


# ── Final polish: AI return end-date alignment (additive coverage fields) ──

def test_ai_return_end_matches_owner_end(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 60, range(30, -1, -1), kind="active")
    cov = compute_portfolio_attribution(db, p.id, 30)["ai_model_shadow_coverage"]
    assert cov["window_covered"] is True
    assert cov["return_end_matched"] is True
    assert cov["return_start_matched"] is True
    assert cov["return_end_date"] == cov["last_valuation"]


def test_ai_return_running_past_owner_end_is_flagged(db, wp):
    # Owner's last snapshot is 2 days ago (within the 5-day edge tolerance, so
    # window_covered stays True) but the AI return chains valuations to today.
    ws, p = wp
    _owner(db, ws, p, range(30, 1, -1), OWNER_30)
    _shadow(db, ws, p, 60, range(30, -1, -1), kind="active")
    att = compute_portfolio_attribution(db, p.id, 30)
    cov = att["ai_model_shadow_coverage"]
    assert cov["window_covered"] is True
    assert cov["return_end_matched"] is False
    assert cov["return_end_date"] > cov["last_valuation"]
    assert att["ai_model_shadow"]["return_pct"] is not None  # AI figures unchanged


def test_ai_coverage_fields_without_valuations(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 60, [], kind="active")
    att = compute_portfolio_attribution(db, p.id, 30)
    cov = att["ai_model_shadow_coverage"]
    assert cov["window_covered"] is False and cov["return_end_matched"] is False
    assert cov["return_end_date"] is None
    # The backend still reports 0.0 drawdown here; the UI must gate it on coverage.
    assert att["ai_model_shadow"]["max_drawdown_pct"] == 0.0


def test_ai_return_ending_three_days_early_is_not_matched(db, wp):
    # Within window_covered's 5-day edge tolerance, but not the same end date.
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 60, range(30, 2, -1), kind="active")
    cov = compute_portfolio_attribution(db, p.id, 30)["ai_model_shadow_coverage"]
    assert cov["window_covered"] is True
    assert cov["return_end_matched"] is False
    assert cov["return_start_matched"] is True


def test_ai_return_starting_late_within_tolerance_is_not_matched(db, wp):
    ws, p = wp
    _owner(db, ws, p, range(30, -1, -1), OWNER_30)
    _shadow(db, ws, p, 60, range(28, -1, -1), kind="active")  # first in-window valuation 2 days late
    cov = compute_portfolio_attribution(db, p.id, 30)["ai_model_shadow_coverage"]
    assert cov["window_covered"] is True
    assert cov["return_start_matched"] is False
    assert cov["return_end_matched"] is True
