"""Tests for the verify_snapshots audit pipeline.

All tests are read-only — no database writes.

Tests cover all five audit checks:
  1.  NAV continuity      — large / small jump, first snapshot, zero prev
  2.  Unrealized P/L      — large / small swing, missing values
  3.  Holdings integrity  — count mismatch, total_invested, total_value,
                            unrealized_pnl, duplicate symbols, invalid JSON
  4.  Price integrity     — price_missing, null price, zero price,
                            negative market_value, clean holdings
  5.  Return sanity       — impossible values flagged as CRITICAL
  6.  Status derivation   — PASS / WARNING / FAIL
  7.  Portfolio-level     — prev pointer advances correctly, all checks run
  8.  Exit-code mapping   — 0 clean, 1 warnings, 2 criticals
"""
from __future__ import annotations

import inspect
import json
import sys
import os
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import models.asset  # noqa: F401 — registers the `assets` FK target table on Base.metadata
from models.database import Base, Portfolio, PortfolioSnapshot as _DbPortfolioSnapshot, Workspace
from manage import (
    AuditAnomaly,
    AuditCheck,
    AuditSeverity,
    MechanicalContinuityState,
    PortfolioAuditResult,
    _assess_tolerance_admissibility,
    _audit_holdings_integrity,
    _audit_mechanical_continuity,
    _audit_nav_continuity,
    _audit_pnl_continuity,
    _audit_price_integrity,
    _audit_return_sanity,
    _audit_tolerance_admissibility,
    _decimal_admissibility,
    _evaluate_mechanical_continuity,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _snap(
    snapshot_id: int = 1,
    snapshot_date: str = "2026-06-01",
    total_value: float = 100_000.0,
    cash_balance: float = 10_000.0,
    total_invested: float | None = 90_000.0,
    unrealized_pnl: float | None = None,
    unrealized_pnl_pct: float | None = None,
    holdings_count: int | None = None,
    holdings_json: str | None = None,
    daily_return_pct: float | None = None,
    investment_return_pct: float | None = None,
) -> SimpleNamespace:
    """Lightweight snapshot stub — avoids SQLAlchemy session requirements."""
    return SimpleNamespace(
        id                    = snapshot_id,
        workspace_id          = 1,
        portfolio_id          = 1,
        snapshot_date         = snapshot_date,
        total_value           = total_value,
        cash_balance          = cash_balance,
        total_invested        = total_invested,
        unrealized_pnl        = unrealized_pnl,
        unrealized_pnl_pct    = unrealized_pnl_pct,
        holdings_count        = holdings_count,
        holdings_json         = holdings_json,
        daily_return_pct      = daily_return_pct,
        investment_return_pct = investment_return_pct,
    )


def _holding(
    symbol: str = "AOT.BK",
    shares: float = 100.0,
    avg_cost: float = 70.0,
    current_price: float | None = 80.0,
    market_value: float | None = 8_000.0,
    unrealized_pnl: float | None = 1_000.0,
    price_missing: bool = False,
) -> dict:
    return {
        "symbol"        : symbol,
        "shares"        : shares,
        "avg_cost"      : avg_cost,
        "current_price" : current_price,
        "market_value"  : market_value,
        "unrealized_pnl": unrealized_pnl,
        "price_missing" : price_missing,
    }


# ══════════════════════════════════════════════════════════════════════════════
# 1. NAV continuity
# ══════════════════════════════════════════════════════════════════════════════

def test_nav_continuity_large_jump_flagged():
    prev = _snap(1, "2026-05-31", total_value=100_000.0)
    curr = _snap(2, "2026-06-01", total_value=120_000.0)  # +20%, above 15%
    anomalies = _audit_nav_continuity(curr, prev, threshold_pct=15.0)
    assert len(anomalies) == 1
    a = anomalies[0]
    assert a.check    == AuditCheck.NAV_CONTINUITY
    assert a.severity == AuditSeverity.WARNING
    assert a.details["change_pct"] == pytest.approx(20.0, abs=0.01)


def test_nav_continuity_large_drop_flagged():
    prev = _snap(1, "2026-05-31", total_value=100_000.0)
    curr = _snap(2, "2026-06-01", total_value=75_000.0)   # -25%, below -15%
    anomalies = _audit_nav_continuity(curr, prev, threshold_pct=15.0)
    assert len(anomalies) == 1
    assert anomalies[0].details["change_pct"] == pytest.approx(-25.0, abs=0.01)


def test_nav_continuity_small_change_passes():
    prev = _snap(1, "2026-05-31", total_value=100_000.0)
    curr = _snap(2, "2026-06-01", total_value=105_000.0)  # +5%, under 15%
    anomalies = _audit_nav_continuity(curr, prev, threshold_pct=15.0)
    assert anomalies == []


def test_nav_continuity_first_snapshot_passes():
    curr = _snap(1, "2026-06-01", total_value=100_000.0)
    assert _audit_nav_continuity(curr, prev=None, threshold_pct=15.0) == []


def test_nav_continuity_zero_prev_nav_skipped():
    prev = _snap(1, "2026-05-31", total_value=0.0)
    curr = _snap(2, "2026-06-01", total_value=50_000.0)
    assert _audit_nav_continuity(curr, prev, threshold_pct=15.0) == []


def test_nav_continuity_custom_threshold():
    prev = _snap(1, "2026-05-31", total_value=100_000.0)
    curr = _snap(2, "2026-06-01", total_value=112_000.0)  # +12%
    # Under 15% threshold → no anomaly
    assert _audit_nav_continuity(curr, prev, threshold_pct=15.0) == []
    # Under 10% threshold → anomaly
    assert len(_audit_nav_continuity(curr, prev, threshold_pct=10.0)) == 1


# ══════════════════════════════════════════════════════════════════════════════
# 2. Unrealized P/L continuity
# ══════════════════════════════════════════════════════════════════════════════

def test_pnl_continuity_large_swing_flagged():
    # Swing of +53,000 on a 100,000 NAV = 53% > 20% threshold
    prev = _snap(1, "2026-05-31", unrealized_pnl=-35_000.0, total_value=100_000.0)
    curr = _snap(2, "2026-06-01", unrealized_pnl= 18_000.0, total_value=100_000.0)
    anomalies = _audit_pnl_continuity(curr, prev)
    assert len(anomalies) == 1
    a = anomalies[0]
    assert a.check    == AuditCheck.PNL_CONTINUITY
    assert a.severity == AuditSeverity.WARNING
    assert a.details["delta"] == pytest.approx(53_000.0, abs=1)


def test_pnl_continuity_small_swing_passes():
    prev = _snap(1, "2026-05-31", unrealized_pnl=5_000.0, total_value=100_000.0)
    curr = _snap(2, "2026-06-01", unrealized_pnl=6_000.0, total_value=100_000.0)
    assert _audit_pnl_continuity(curr, prev) == []


def test_pnl_continuity_no_prev_passes():
    curr = _snap(1, "2026-06-01", unrealized_pnl=5_000.0, total_value=100_000.0)
    assert _audit_pnl_continuity(curr, prev=None) == []


def test_pnl_continuity_missing_values_skipped():
    prev = _snap(1, "2026-05-31", unrealized_pnl=None, total_value=100_000.0)
    curr = _snap(2, "2026-06-01", unrealized_pnl=None, total_value=100_000.0)
    assert _audit_pnl_continuity(curr, prev) == []


# ══════════════════════════════════════════════════════════════════════════════
# 3. Holdings integrity
# ══════════════════════════════════════════════════════════════════════════════

def test_holdings_integrity_clean_passes():
    h = _holding(shares=100, avg_cost=70, market_value=8_000, unrealized_pnl=1_000)
    snap = _snap(
        holdings_json    = json.dumps([h]),
        holdings_count   = 1,
        total_invested   = 100 * 70,   # 7_000
        total_value      = 8_000 + 10_000,  # equity + cash
        cash_balance     = 10_000,
        unrealized_pnl   = 1_000,
    )
    assert _audit_holdings_integrity(snap) == []


def test_holdings_integrity_no_json_passes():
    snap = _snap(holdings_json=None)
    assert _audit_holdings_integrity(snap) == []


def test_holdings_integrity_invalid_json_critical():
    snap = _snap(holdings_json="not valid json {{{")
    anomalies = _audit_holdings_integrity(snap)
    assert len(anomalies) == 1
    assert anomalies[0].severity == AuditSeverity.CRITICAL
    assert "not valid JSON" in anomalies[0].description


def test_holdings_integrity_count_mismatch_warning():
    holdings = [_holding("A.BK"), _holding("B.BK")]
    snap = _snap(
        holdings_json  = json.dumps(holdings),
        holdings_count = 5,  # wrong — actual is 2
        total_invested = 0,
        total_value    = 10_000,
        cash_balance   = 10_000,
    )
    checks = {a.check for a in _audit_holdings_integrity(snap)}
    assert AuditCheck.HOLDINGS_INTEGRITY in checks
    anomaly = next(a for a in _audit_holdings_integrity(snap) if "holdings_count" in a.description.lower())
    assert anomaly.severity == AuditSeverity.WARNING


def test_holdings_integrity_total_invested_mismatch_warning():
    # 100 shares × 70 = 7,000, but snap records 9,999
    h = _holding(shares=100, avg_cost=70, market_value=8_000, unrealized_pnl=1_000)
    snap = _snap(
        holdings_json  = json.dumps([h]),
        holdings_count = 1,
        total_invested = 9_999.0,   # wrong
        total_value    = 18_000,
        cash_balance   = 10_000,
        unrealized_pnl = 1_000,
    )
    anomalies = _audit_holdings_integrity(snap)
    descs = [a.description for a in anomalies]
    assert any("total_invested" in d for d in descs)


def test_holdings_integrity_total_value_mismatch_warning():
    h = _holding(shares=100, avg_cost=70, market_value=8_000, unrealized_pnl=1_000)
    snap = _snap(
        holdings_json  = json.dumps([h]),
        holdings_count = 1,
        total_invested = 7_000,
        # total_value should be 8_000 + 10_000 = 18_000 but is 99_000
        total_value    = 99_000.0,
        cash_balance   = 10_000,
        unrealized_pnl = 1_000,
    )
    anomalies = _audit_holdings_integrity(snap)
    descs = [a.description for a in anomalies]
    assert any("total_value" in d for d in descs)


def test_holdings_integrity_unrealized_pnl_mismatch_warning():
    h = _holding(shares=100, avg_cost=70, market_value=8_000, unrealized_pnl=1_000)
    snap = _snap(
        holdings_json  = json.dumps([h]),
        holdings_count = 1,
        total_invested = 7_000,
        total_value    = 18_000,
        cash_balance   = 10_000,
        unrealized_pnl = 50_000.0,  # wrong — computed is 1,000
    )
    anomalies = _audit_holdings_integrity(snap)
    descs = [a.description for a in anomalies]
    assert any("unrealized_pnl" in d for d in descs)


def test_holdings_integrity_duplicate_symbols_critical():
    holdings = [_holding("PTT.BK"), _holding("PTT.BK")]  # same symbol twice
    snap = _snap(
        holdings_json  = json.dumps(holdings),
        total_invested = 0,
        total_value    = 10_000,
        cash_balance   = 10_000,
    )
    anomalies = _audit_holdings_integrity(snap)
    crit = [a for a in anomalies if a.severity == AuditSeverity.CRITICAL]
    assert len(crit) == 1
    assert "PTT.BK" in crit[0].description


# ══════════════════════════════════════════════════════════════════════════════
# 4. Price integrity
# ══════════════════════════════════════════════════════════════════════════════

def test_price_integrity_clean_passes():
    h = _holding(price_missing=False, current_price=80.0, market_value=8_000.0, shares=100)
    snap = _snap(holdings_json=json.dumps([h]))
    assert _audit_price_integrity(snap) == []


def test_price_integrity_no_json_passes():
    snap = _snap(holdings_json=None)
    assert _audit_price_integrity(snap) == []


def test_price_integrity_price_missing_true_flagged():
    h = _holding(price_missing=True, current_price=None, market_value=None)
    snap = _snap(holdings_json=json.dumps([h]))
    anomalies = _audit_price_integrity(snap)
    assert len(anomalies) == 1
    assert anomalies[0].severity == AuditSeverity.WARNING
    assert "price_missing=True" in anomalies[0].description


def test_price_integrity_price_missing_does_not_also_flag_null():
    # When price_missing=True the check exits early — no additional null-price anomaly
    h = _holding(price_missing=True, current_price=None, market_value=None, shares=100)
    snap = _snap(holdings_json=json.dumps([h]))
    assert len(_audit_price_integrity(snap)) == 1  # only the price_missing anomaly


def test_price_integrity_null_price_flagged():
    h = _holding(price_missing=False, current_price=None, market_value=8_000.0, shares=100)
    snap = _snap(holdings_json=json.dumps([h]))
    anomalies = _audit_price_integrity(snap)
    assert any("current_price is null" in a.description for a in anomalies)


def test_price_integrity_zero_price_flagged():
    h = _holding(price_missing=False, current_price=0.0, market_value=0.0, shares=100)
    snap = _snap(holdings_json=json.dumps([h]))
    anomalies = _audit_price_integrity(snap)
    assert any("current_price <= 0" in a.description for a in anomalies)


def test_price_integrity_negative_price_flagged():
    h = _holding(price_missing=False, current_price=-5.0, market_value=-500.0, shares=100)
    snap = _snap(holdings_json=json.dumps([h]))
    anomalies = _audit_price_integrity(snap)
    assert any("current_price <= 0" in a.description for a in anomalies)


def test_price_integrity_negative_market_value_flagged():
    # Price is positive but market_value is wrong
    h = _holding(price_missing=False, current_price=80.0, market_value=-100.0, shares=100)
    snap = _snap(holdings_json=json.dumps([h]))
    anomalies = _audit_price_integrity(snap)
    assert any("market_value" in a.description and "<= 0" in a.description for a in anomalies)


def test_price_integrity_zero_market_value_zero_shares_passes():
    # market_value=0 is OK if shares=0 (position fully sold)
    h = _holding(price_missing=False, current_price=80.0, market_value=0.0, shares=0)
    snap = _snap(holdings_json=json.dumps([h]))
    anomalies = _audit_price_integrity(snap)
    assert not any("market_value" in a.description for a in anomalies)


# ══════════════════════════════════════════════════════════════════════════════
# 5. Return sanity
# ══════════════════════════════════════════════════════════════════════════════

def test_return_sanity_normal_daily_return_passes():
    snap = _snap(daily_return_pct=1.5, investment_return_pct=1.5)
    assert _audit_return_sanity(snap) == []


def test_return_sanity_extreme_daily_return_critical():
    snap = _snap(daily_return_pct=75.0)
    anomalies = _audit_return_sanity(snap)
    assert len(anomalies) == 1
    assert anomalies[0].severity  == AuditSeverity.CRITICAL
    assert anomalies[0].check     == AuditCheck.RETURN_SANITY
    assert "daily_return_pct"     in anomalies[0].description


def test_return_sanity_extreme_negative_critical():
    snap = _snap(daily_return_pct=-80.0)
    anomalies = _audit_return_sanity(snap)
    assert len(anomalies) == 1
    assert anomalies[0].severity == AuditSeverity.CRITICAL


def test_return_sanity_investment_return_pct_also_checked():
    snap = _snap(daily_return_pct=0.5, investment_return_pct=-99.0)
    anomalies = _audit_return_sanity(snap)
    assert len(anomalies) == 1
    assert "investment_return_pct" in anomalies[0].description


def test_return_sanity_both_extreme_produces_two_anomalies():
    snap = _snap(daily_return_pct=60.0, investment_return_pct=-70.0)
    anomalies = _audit_return_sanity(snap)
    assert len(anomalies) == 2


def test_return_sanity_boundary_50_pct_passes():
    # Exactly ±50 is not strictly greater — should pass
    snap = _snap(daily_return_pct=50.0, investment_return_pct=-50.0)
    assert _audit_return_sanity(snap) == []


def test_return_sanity_none_values_skipped():
    snap = _snap(daily_return_pct=None, investment_return_pct=None)
    assert _audit_return_sanity(snap) == []


# ══════════════════════════════════════════════════════════════════════════════
# 6. PortfolioAuditResult status derivation
# ══════════════════════════════════════════════════════════════════════════════

def _make_result(*anomalies: AuditAnomaly) -> PortfolioAuditResult:
    r = PortfolioAuditResult(
        portfolio_id=1, portfolio_name="Test", snapshots_checked=10
    )
    r.anomalies = list(anomalies)
    return r


def test_status_pass_when_no_anomalies():
    assert _make_result().status == "PASS"


def test_status_warning_when_only_warnings():
    w = AuditAnomaly(1, "2026-06-01", AuditCheck.NAV_CONTINUITY, AuditSeverity.WARNING, "big jump")
    assert _make_result(w).status == "WARNING"


def test_status_fail_when_any_critical():
    c = AuditAnomaly(1, "2026-06-01", AuditCheck.RETURN_SANITY, AuditSeverity.CRITICAL, "bad return")
    assert _make_result(c).status == "FAIL"


def test_status_fail_overrides_warning():
    w = AuditAnomaly(1, "2026-06-01", AuditCheck.NAV_CONTINUITY, AuditSeverity.WARNING, "jump")
    c = AuditAnomaly(1, "2026-06-01", AuditCheck.RETURN_SANITY,  AuditSeverity.CRITICAL, "bad")
    assert _make_result(w, c).status == "FAIL"


def test_warnings_criticals_properties():
    w = AuditAnomaly(1, "2026-06-01", AuditCheck.NAV_CONTINUITY, AuditSeverity.WARNING,  "w")
    c = AuditAnomaly(1, "2026-06-01", AuditCheck.RETURN_SANITY,  AuditSeverity.CRITICAL, "c")
    r = _make_result(w, c)
    assert r.warnings  == [w]
    assert r.criticals == [c]


# ══════════════════════════════════════════════════════════════════════════════
# 7. Portfolio-level: prev pointer advances correctly
# ══════════════════════════════════════════════════════════════════════════════

def test_all_checks_run_per_snapshot():
    """Each snapshot runs through all five check functions without crashing."""
    # Snapshot with intentional anomalies across multiple checks
    h_bad = _holding(
        symbol="X.BK", shares=100, avg_cost=70,
        current_price=None,   # price_integrity
        market_value=8_000,
        unrealized_pnl=1_000,
        price_missing=False,
    )
    snap = _snap(
        snapshot_id      = 99,
        snapshot_date    = "2026-06-01",
        total_value      = 999_999.0,    # NAV continuity (vs prev 100,000)
        cash_balance     = 10_000.0,
        total_invested   = 7_000.0,
        unrealized_pnl   = 1_000.0,
        holdings_count   = 1,
        holdings_json    = json.dumps([h_bad]),
        daily_return_pct = 80.0,         # return sanity
    )
    prev = _snap(snapshot_id=98, snapshot_date="2026-05-31", total_value=100_000.0)

    # Just verify all audit functions run without raising
    nav_a  = _audit_nav_continuity(snap, prev, 15.0)
    pnl_a  = _audit_pnl_continuity(snap, prev)
    hold_a = _audit_holdings_integrity(snap)
    pri_a  = _audit_price_integrity(snap)
    ret_a  = _audit_return_sanity(snap)

    all_anomalies = nav_a + pnl_a + hold_a + pri_a + ret_a
    checks_hit = {a.check for a in all_anomalies}
    assert AuditCheck.NAV_CONTINUITY    in checks_hit
    assert AuditCheck.RETURN_SANITY     in checks_hit
    assert AuditCheck.PRICE_INTEGRITY   in checks_hit


def test_nav_continuity_uses_previous_snapshot_not_arbitrary():
    """Verify the prev passed in is the immediately preceding snapshot."""
    snap_a = _snap(1, "2026-06-01", total_value=100_000.0)
    snap_b = _snap(2, "2026-06-02", total_value=120_000.0)  # +20% vs A
    snap_c = _snap(3, "2026-06-03", total_value=122_000.0)  # +1.7% vs B

    # B vs A → flagged
    assert len(_audit_nav_continuity(snap_b, snap_a, 15.0)) == 1
    # C vs B → clean
    assert len(_audit_nav_continuity(snap_c, snap_b, 15.0)) == 0


# ══════════════════════════════════════════════════════════════════════════════
# 9. Mechanical continuity (BANPU-WP5-C7 / D7) — WP5-A12-A32
# ══════════════════════════════════════════════════════════════════════════════
#
# _evaluate_mechanical_continuity() is a pure function — tested directly with
# hand-built Decimal/str inputs, no database. _audit_mechanical_continuity()
# is tested with a lightweight SimpleNamespace conversion_ctx (mirrors the
# CanonicalTransaction.position_conversion.value.boundary_evidence shape
# _audit_mechanical_continuity() actually reads) — same pattern as this
# file's own _snap()/_holding() stubs.

def _conversion_ctx(
    id: int = 1,
    predecessor_reference_price=Decimal("100"),
    successor_reference_price=Decimal("200"),
    mechanical_nav_tolerance_pct=Decimal("1.0"),
    conversion_ratio=Decimal("0.5"),
    suspension_gap_annotation="",
) -> SimpleNamespace:
    boundary = SimpleNamespace(
        predecessor_reference_price=predecessor_reference_price,
        successor_reference_price=successor_reference_price,
        mechanical_nav_tolerance_pct=mechanical_nav_tolerance_pct,
        suspension_gap_annotation=suspension_gap_annotation,
    )
    value = SimpleNamespace(boundary_evidence=boundary, conversion_ratio=conversion_ratio)
    position_conversion = SimpleNamespace(value=value)
    return SimpleNamespace(id=id, position_conversion=position_conversion)


def _evaluate(**overrides):
    defaults = dict(
        predecessor_reference_price=Decimal("100"),
        successor_reference_price=Decimal("200"),
        mechanical_nav_tolerance_pct=Decimal("1.0"),
        conversion_ratio=Decimal("0.5"),
        suspension_gap_annotation="",
    )
    defaults.update(overrides)
    return _evaluate_mechanical_continuity(**defaults)


def _audit_status(anomalies: list[AuditAnomaly]) -> str:
    """Real PortfolioAuditResult.status — the actual exit-code-mapped
    consumer object (manage.py: FAIL->exit 2, WARNING->exit 1, PASS->exit 0),
    not a hand-rolled re-implementation of that mapping."""
    return PortfolioAuditResult(
        portfolio_id=1, portfolio_name="T", snapshots_checked=1, anomalies=anomalies,
    ).status


# ── WP5-A12-A14 — §10.3 tolerance admissibility (standalone obligation) ──────
#
# Corrected per Independent Implementation Review §12/§20 item 1: previously
# folded into D7's own NOT_EVALUABLE handling with no independently
# observable §10.3 result. _assess_tolerance_admissibility()/
# _audit_tolerance_admissibility() are now their own independently invocable
# functions (manage.py module note) — tested here directly, without going
# anywhere near D2-D6.

def test_wp5_a12_negative_tolerance_rejected():
    assert _assess_tolerance_admissibility(Decimal("-0.1")) == "NEGATIVE"

    anomalies = _audit_tolerance_admissibility(
        _snap(1, "2026-03-02"), _conversion_ctx(mechanical_nav_tolerance_pct=Decimal("-0.1")),
    )
    assert len(anomalies) == 1
    a = anomalies[0]
    assert a.check == AuditCheck.MECHANICAL_CONTINUITY
    assert a.severity == AuditSeverity.CRITICAL
    assert a.details["obligation"] == "tolerance_admissibility"
    assert a.details["reason"] == "NEGATIVE"
    assert _audit_status(anomalies) == "FAIL"   # exit-2 contribution


def test_wp5_a13_non_finite_or_non_decimal_tolerance_rejected():
    assert _assess_tolerance_admissibility(Decimal("NaN")) == "NON_FINITE"
    assert _assess_tolerance_admissibility("1.0") == "NON_DECIMAL_EXACT"
    assert _assess_tolerance_admissibility(None) == "ABSENT"

    for bad, reason in ((Decimal("NaN"), "NON_FINITE"), ("1.0", "NON_DECIMAL_EXACT"), (None, "ABSENT")):
        anomalies = _audit_tolerance_admissibility(
            _snap(1, "2026-03-02"), _conversion_ctx(mechanical_nav_tolerance_pct=bad),
        )
        assert len(anomalies) == 1, bad
        assert anomalies[0].severity == AuditSeverity.CRITICAL, bad
        assert anomalies[0].details["reason"] == reason, bad
        assert _audit_status(anomalies) == "FAIL", bad


def test_wp5_a14_admissible_tolerance_no_false_positive():
    # zero is ADMISSIBLE for a tolerance (a stricter, not invalid, requirement)
    assert _assess_tolerance_admissibility(Decimal("0")) == "ADMISSIBLE"
    assert _assess_tolerance_admissibility(Decimal("1.0")) == "ADMISSIBLE"

    anomalies = _audit_tolerance_admissibility(
        _snap(1, "2026-03-02"), _conversion_ctx(mechanical_nav_tolerance_pct=Decimal("0")),
    )
    assert anomalies == []                      # ADMISSIBLE, no finding — no false positive
    assert _audit_status(anomalies) == "PASS"


# ── WP5-A15/A16 — reconciliation, PASS ────────────────────────────────────────

def test_wp5_a15_below_tolerance_passes():
    # P_pre=100, implied=0.5*198=99, gap=1, metric=1.0% < tolerance=2.0%
    kwargs = dict(successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("2.0"))
    r = _evaluate(**kwargs)
    assert r.state == MechanicalContinuityState.PASS
    assert r.metric_pct == Decimal("1.0")

    anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**kwargs))
    assert anomalies == []                      # no consumer-level anomaly for PASS
    assert _audit_status(anomalies) == "PASS"


def test_wp5_a16_exact_tolerance_boundary_inclusive_passes():
    # metric=1.0%, tolerance=1.0% exactly — D4 is inclusive (<=)
    kwargs = dict(successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("1.0"))
    r = _evaluate(**kwargs)
    assert r.state == MechanicalContinuityState.PASS
    assert r.metric_pct == r.tolerance_pct == Decimal("1.0")

    anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**kwargs))
    assert anomalies == []
    assert _audit_status(anomalies) == "PASS"


# ── WP5-A17-A20 — above tolerance, D6 annotation normalization ───────────────

def test_wp5_a17_above_tolerance_no_annotation_is_failure():
    kwargs = dict(
        successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5"),
        suspension_gap_annotation=None,
    )
    r = _evaluate(**kwargs)
    assert r.state == MechanicalContinuityState.MECHANICAL_CONTINUITY_FAILURE
    assert r.metric_pct == Decimal("1.0")

    anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**kwargs))
    assert len(anomalies) == 1
    assert anomalies[0].severity == AuditSeverity.CRITICAL
    assert _audit_status(anomalies) == "FAIL"   # exit-2 contribution


def test_wp5_a18_above_tolerance_empty_string_annotation_is_failure():
    kwargs = dict(
        successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5"),
        suspension_gap_annotation="",
    )
    r = _evaluate(**kwargs)
    assert r.state == MechanicalContinuityState.MECHANICAL_CONTINUITY_FAILURE

    anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**kwargs))
    assert len(anomalies) == 1
    assert anomalies[0].severity == AuditSeverity.CRITICAL
    assert _audit_status(anomalies) == "FAIL"


def test_wp5_a19_above_tolerance_whitespace_only_annotation_is_failure():
    kwargs = dict(
        successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5"),
        suspension_gap_annotation="   ",
    )
    r = _evaluate(**kwargs)
    assert r.state == MechanicalContinuityState.MECHANICAL_CONTINUITY_FAILURE

    anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**kwargs))
    assert len(anomalies) == 1
    assert anomalies[0].severity == AuditSeverity.CRITICAL
    assert _audit_status(anomalies) == "FAIL"


def test_wp5_a20_above_tolerance_annotated_is_discontinuity_metric_preserved():
    kwargs = dict(
        successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5"),
        suspension_gap_annotation="Trading suspended — evidence attached",
    )
    r = _evaluate(**kwargs)
    assert r.state == MechanicalContinuityState.ANNOTATED_BOUNDARY_DISCONTINUITY
    assert r.metric_pct == Decimal("1.0")   # unmodified by annotation presence

    anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**kwargs))
    assert len(anomalies) == 1
    a = anomalies[0]
    assert a.severity == AuditSeverity.WARNING
    assert _audit_status(anomalies) == "WARNING"   # exit-1 contribution only, never exit-2
    # WP5-A20 correction: exact Decimal preserved end-to-end, not float()/rounded
    assert isinstance(a.details["metric_pct"], Decimal)
    assert isinstance(a.details["tolerance_pct"], Decimal)
    assert a.details["metric_pct"] == Decimal("1.0")
    # no snapshot/NAV/basis/cash-flow field referenced or mutated
    assert set(a.details) == {"conversion_transaction_id", "metric_pct", "tolerance_pct"}


# ── WP5-A21-A25 — NOT_EVALUABLE, missing/malformed/non-finite/non-positive ───
#
# Each class now also asserts the audit-consumer state: CRITICAL severity and
# exit-2 contribution, never a silent PASS or a missing anomaly.

def test_wp5_a21_missing_required_evidence_not_evaluable():
    for field in ("predecessor_reference_price", "successor_reference_price",
                  "mechanical_nav_tolerance_pct", "conversion_ratio"):
        overrides = {field: None}
        r = _evaluate(**overrides)
        assert r.state == MechanicalContinuityState.NOT_EVALUABLE, field
        assert r.invalid_field == field
        assert r.invalid_reason == "ABSENT"
        assert r.metric_pct is None

        anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**overrides))
        assert len(anomalies) == 1, field
        assert anomalies[0].severity == AuditSeverity.CRITICAL, field
        assert anomalies[0].details["invalid_field"] == field, field
        assert _audit_status(anomalies) == "FAIL", field


def test_wp5_a22_malformed_numeric_string_not_evaluable():
    overrides = dict(predecessor_reference_price="100")   # str, not Decimal
    r = _evaluate(**overrides)
    assert r.state == MechanicalContinuityState.NOT_EVALUABLE
    assert r.invalid_field == "predecessor_reference_price"
    assert r.invalid_reason == "NON_DECIMAL_EXACT"

    anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**overrides))
    assert len(anomalies) == 1
    assert anomalies[0].severity == AuditSeverity.CRITICAL
    assert _audit_status(anomalies) == "FAIL"


def test_wp5_a23_non_finite_not_evaluable():
    for value in (Decimal("NaN"), Decimal("Infinity"), Decimal("-Infinity")):
        overrides = dict(successor_reference_price=value)
        r = _evaluate(**overrides)
        assert r.state == MechanicalContinuityState.NOT_EVALUABLE
        assert r.invalid_reason == "NON_FINITE"

        anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**overrides))
        assert len(anomalies) == 1, value
        assert anomalies[0].severity == AuditSeverity.CRITICAL, value
        assert _audit_status(anomalies) == "FAIL", value


def test_wp5_a24_non_positive_predecessor_price_not_evaluable():
    for value in (Decimal("0"), Decimal("-1")):
        overrides = dict(predecessor_reference_price=value)
        r = _evaluate(**overrides)
        assert r.state == MechanicalContinuityState.NOT_EVALUABLE
        assert r.invalid_field == "predecessor_reference_price"
        assert r.invalid_reason == "NON_POSITIVE"

        anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**overrides))
        assert len(anomalies) == 1, value
        assert anomalies[0].severity == AuditSeverity.CRITICAL, value
        assert _audit_status(anomalies) == "FAIL", value


def test_wp5_a25_invalid_conversion_ratio_not_evaluable():
    for value in (Decimal("0"), Decimal("-0.5"), "0.5", None):
        overrides = dict(conversion_ratio=value)
        r = _evaluate(**overrides)
        assert r.state == MechanicalContinuityState.NOT_EVALUABLE
        assert r.invalid_field == "conversion_ratio"

        anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**overrides))
        assert len(anomalies) == 1, value
        assert anomalies[0].severity == AuditSeverity.CRITICAL, value
        assert _audit_status(anomalies) == "FAIL", value


# ── WP5-A26 — NOT_EVALUABLE distinct, never silent PASS ───────────────────────

def test_wp5_a26_not_evaluable_distinct_from_failure_and_never_silent_pass():
    not_evaluable = _evaluate(predecessor_reference_price=None)
    failure = _evaluate(successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5"))
    assert not_evaluable.state != failure.state
    assert not_evaluable.state == MechanicalContinuityState.NOT_EVALUABLE
    assert not_evaluable.state != MechanicalContinuityState.PASS

    a_not_eval = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(predecessor_reference_price=None))
    a_fail = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(
        successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5")))
    assert a_not_eval[0].severity == AuditSeverity.CRITICAL
    assert a_fail[0].severity == AuditSeverity.CRITICAL
    assert a_not_eval[0].description != a_fail[0].description
    assert "invalid_field" in a_not_eval[0].details
    assert "invalid_field" not in a_fail[0].details


# ── WP5-A27/A28 — Decimal-only, no quantization ───────────────────────────────

def test_wp5_a27_decimal_only_arithmetic_no_float_leakage():
    r = _evaluate()
    assert isinstance(r.metric_pct, Decimal)
    assert isinstance(r.tolerance_pct, Decimal)
    src = inspect.getsource(_evaluate_mechanical_continuity)
    assert "float(" not in src


def test_wp5_a28_no_intermediate_or_final_quantization():
    # P_pre=3, implied=1*2=2, gap=1 -> metric = (1/3)*100, a repeating decimal.
    # Any premature rounding/quantization would truncate this.
    r = _evaluate(
        predecessor_reference_price=Decimal("3"), successor_reference_price=Decimal("2"),
        conversion_ratio=Decimal("1"), mechanical_nav_tolerance_pct=Decimal("1000"),
    )
    expected = (abs(Decimal("3") - Decimal("1") * Decimal("2")) / Decimal("3")) * 100
    assert r.metric_pct == expected
    assert len(str(r.metric_pct).split(".")[-1]) > 10   # full ambient-context precision retained


# ── WP5-A29 — distinct AuditCheck identity ────────────────────────────────────

def test_wp5_a29_uses_distinct_mechanical_continuity_check_identity():
    anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(
        successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5")))
    assert len(anomalies) == 1
    assert anomalies[0].check == AuditCheck.MECHANICAL_CONTINUITY
    assert anomalies[0].check not in {
        AuditCheck.NAV_CONTINUITY, AuditCheck.PNL_CONTINUITY,
        AuditCheck.HOLDINGS_INTEGRITY, AuditCheck.PRICE_INTEGRITY, AuditCheck.RETURN_SANITY,
    }


# ── WP5-A30 — no mutation performed (real before/after DB-state proof) ───────
#
# Corrected per Independent Implementation Review §11/§20 item 6: an in-memory
# SimpleNamespace stub/signature check is not the required DB-state proof. A
# real (persisted, re-queried after each call) PortfolioSnapshot row now
# stands in for the stub, across all four D7 outcome states.

def test_wp5_a30_audit_consumer_performs_no_db_mutation_all_outcomes():
    sig = inspect.signature(_audit_mechanical_continuity)
    assert "db" not in sig.parameters and "session" not in sig.parameters

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    db.add(Workspace(id=1, name="Default"))
    db.add(Portfolio(id=1, workspace_id=1, name="Test", cash_balance=0.0))
    db.add(_DbPortfolioSnapshot(
        id=1, workspace_id=1, portfolio_id=1, snapshot_date="2026-03-02",
        total_value=100_000.0, cash_balance=10_000.0, total_invested=90_000.0,
    ))
    db.commit()

    cases = {
        "PASS": dict(successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("2.0")),
        "ANNOTATED_BOUNDARY_DISCONTINUITY": dict(
            successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5"),
            suspension_gap_annotation="x"),
        "MECHANICAL_CONTINUITY_FAILURE": dict(
            successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5")),
        "NOT_EVALUABLE": dict(predecessor_reference_price=None),
    }
    try:
        for label, overrides in cases.items():
            snap = db.query(_DbPortfolioSnapshot).filter_by(id=1).first()
            before = {c.name: getattr(snap, c.name) for c in _DbPortfolioSnapshot.__table__.columns}

            _audit_mechanical_continuity(snap, _conversion_ctx(**overrides))
            _audit_tolerance_admissibility(snap, _conversion_ctx(**overrides))

            db.expire_all()
            refreshed = db.query(_DbPortfolioSnapshot).filter_by(id=1).first()
            after = {c.name: getattr(refreshed, c.name) for c in _DbPortfolioSnapshot.__table__.columns}
            assert after == before, label   # zero DB writes for every outcome state
    finally:
        db.close()


# ── WP5-A31 — independence from POSITION_CONVERSION_REBUILD_BOUNDARY ─────────
#
# The rebuild-boundary-guard half of this row lives in
# test_portfolio_rebuilder.py. This half proves the D7 direction. Corrected
# per Independent Implementation Review §11/§20 item 6: co_names introspection
# alone was not accepted as the primary A31 proof — a behavioral test is now
# primary, with co_names retained only as supplementary evidence.

def test_wp5_a31_d7_independent_of_rebuild_boundary_behavioral():
    """D7 evaluation and its audit consumer never invoke rebuild-boundary
    logic — proven by patching rebuild_portfolio and asserting it is never
    touched while D7 runs to every one of its four outcome states, including
    a genuine FAILURE."""
    import services.portfolio_rebuilder as rebuilder_mod

    cases = [
        dict(successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("2.0")),  # PASS
        dict(successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5"),
             suspension_gap_annotation="x"),                                                            # ANNOTATED
        dict(successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5")),   # FAILURE
        dict(predecessor_reference_price=None),                                                        # NOT_EVALUABLE
    ]
    with patch.object(rebuilder_mod, "rebuild_portfolio") as mock_rebuild:
        for overrides in cases:
            _evaluate(**overrides)
            _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(**overrides))
            _audit_tolerance_admissibility(_snap(1, "2026-03-02"), _conversion_ctx(**overrides))
    mock_rebuild.assert_not_called()   # independent outcome: D7 never triggers reconstruction


def test_wp5_a31_supplementary_no_rebuild_boundary_reference():
    """Supplementary only — see the behavioral test above for the primary
    A31 proof. No shared predicate, no shared result identity, no call path
    between D7 mechanical continuity and portfolio_rebuilder's rebuild-
    boundary guard."""
    for fn in (_evaluate_mechanical_continuity, _audit_mechanical_continuity, _audit_tolerance_admissibility):
        names = fn.__code__.co_names
        assert not any("rebuild" in n.lower() for n in names)
        assert "PositionConversionRebuildBoundaryError" not in names

    # A FAILURE-state mechanical-continuity result carries no rebuild-boundary
    # concept anywhere in its evidence.
    anomalies = _audit_mechanical_continuity(_snap(1, "2026-03-02"), _conversion_ctx(
        successor_reference_price=Decimal("198"), mechanical_nav_tolerance_pct=Decimal("0.5")))
    assert "rebuild" not in json.dumps(anomalies[0].details, default=str).lower()


# ── WP5-A32 — canonical parser is sole input authority ───────────────────────

def test_wp5_a32_no_provider_or_network_lookup():
    sig = inspect.signature(_evaluate_mechanical_continuity)
    assert set(sig.parameters) == {
        "predecessor_reference_price", "successor_reference_price",
        "mechanical_nav_tolerance_pct", "conversion_ratio", "suspension_gap_annotation",
    }
    names = _evaluate_mechanical_continuity.__code__.co_names
    for forbidden in ("fetch_price_info", "requests", "yfinance", "get_yfinance_symbol", "urlopen"):
        assert forbidden not in names
    names2 = _audit_mechanical_continuity.__code__.co_names
    for forbidden in ("fetch_price_info", "requests", "yfinance", "get_yfinance_symbol", "urlopen"):
        assert forbidden not in names2
