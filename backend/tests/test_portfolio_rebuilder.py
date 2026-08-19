"""Tests for services/portfolio_rebuilder.py — Phase 2 consumer migration.

Verifies that the replay engine operates on CanonicalTransaction objects and
that the removed duplicate parsing helpers are gone.  All tests are pure-Python
(no database or network).

Coverage
--------
Removed helpers
  1.  _REALIZED_RE not importable from portfolio_rebuilder
  2.  _QCORR_RE not importable from portfolio_rebuilder
  3.  _parse_realized_pnl not importable from portfolio_rebuilder
  4.  _parse_qty_correction_delta not importable from portfolio_rebuilder

_apply_transaction with CanonicalTransaction
  5.  DEPOSIT increases cash balance
  6.  INITIAL_CASH increases cash balance
  7.  WITHDRAW decreases cash balance
  8.  DIVIDEND increases cash balance
  9.  BUY decreases cash and adds holding (avg cost = total_amount / shares)
  10. BUY into existing holding merges with weighted-average cost
  11. BUY with zero shares is a no-op
  12. SELL increases cash and removes holding when fully sold
  13. SELL partial reduces shares; holding remains
  14. SELL accumulates realized P&L from ctx.realized_pnl
  15. SELL with None realized_pnl treated as 0.0
  16. INITIAL_POSITION adds holding without affecting cash
  17. INITIAL_POSITION into existing holding merges avg_cost
  18. INITIAL_POSITION with zero shares is a no-op
  19. QUANTITY_CORRECTION positive delta increases shares and adjusts avg_cost
  20. QUANTITY_CORRECTION negative delta decreases shares
  21. QUANTITY_CORRECTION that zeros a holding removes it
  22. QUANTITY_CORRECTION for unknown symbol is a no-op
  23. Uses canonical_symbol (not raw_symbol) as holdings key

_replay_with_date_snapshots
  24. Single date: state reflects transactions up to that date
  25. Transactions after the date are NOT applied
  26. Same date, multiple snapshots: second date builds on first
  27. Empty transaction list returns initial state for every date

_populate_return_fields
  28. DEPOSIT counted in net_ecf (deposits)
  29. WITHDRAW counted in net_ecf (withdrawals)
  30. BUY fees and taxes counted in period_fees_paid
  31. SELL P&L and fees counted in period decomposition
  32. DIVIDEND counted in period_dividend_income
  33. Transactions outside the window are excluded
"""
from __future__ import annotations

import asyncio
import json
import sys
import os
import tempfile
from datetime import date, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.database import PortfolioSnapshot
from services.transaction_canonicalizer import CanonicalTransaction, parse_position_conversion_payload
from services.ledger_validator import LedgerFinding, LedgerValidationReport
from services.portfolio_rebuilder import (
    _apply_transaction,
    _preflight_position_conversions,
    PositionConversionReplayError,
    PositionConversionRebuildBoundaryError,
    _replay_with_date_snapshots,
    _populate_return_fields,
    _compute_confidence_score,
    _compute_confidence_report,
    _generate_execution_plan,
    _export_backup,
    _values_differ,
    _COVERAGE_THRESHOLD,
    _CONF_W_REPLAY,
    _CONF_W_LEDGER,
    _CONF_W_COVERAGE,
    _CONF_W_CONSISTENCY,
    _CONF_W_VALIDATOR,
    _CONF_LEDGER_PER_CRITICAL,
    _CONF_LEDGER_PER_ERROR,
    _CONF_LEDGER_PER_WARNING,
    _PortfolioState,
    _HoldingState,
    _SnapshotDay,
    ConfidenceReport,
    ReconstructionPlan,
    PlanOperation,
    RebuildResult,
    rebuild_all_portfolios,
    rebuild_portfolio,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _ctx(
    id: int = 1,
    transaction_type: str = "BUY",
    raw_symbol: str | None = "AOT.BK",
    canonical_symbol: str | None = "AOT.BK",
    shares: float = 100.0,
    price_per_share: float = 75.0,
    total_amount: float = 7_550.0,
    fees: float = 50.0,
    taxes: float = 3.50,
    transaction_date: date = date(2026, 1, 15),
    created_at: datetime | None = None,
    sector: str | None = "Transport",
    notes: str | None = None,
    qty_correction_delta: Decimal | None = None,
    realized_pnl: float | None = None,
    asset_id: int | None = None,
) -> CanonicalTransaction:
    return CanonicalTransaction(
        id                   = id,
        transaction_type     = transaction_type,
        raw_symbol           = raw_symbol,
        canonical_symbol     = canonical_symbol,
        shares               = Decimal(str(shares)),
        price_per_share      = Decimal(str(price_per_share)),
        total_amount         = Decimal(str(total_amount)),
        fees                 = Decimal(str(fees)),
        taxes                = Decimal(str(taxes)),
        transaction_date     = transaction_date,
        created_at           = created_at,
        sector               = sector,
        notes                = notes,
        qty_correction_delta = qty_correction_delta,
        realized_pnl         = realized_pnl,
        asset_id             = asset_id,
    )


def _state(cash: float = 0.0) -> _PortfolioState:
    return _PortfolioState(
        cash_balance            = Decimal(str(cash)),
        holdings                = {},
        cumulative_realized_pnl = Decimal("0"),
    )


def _day(holdings_json: str = "[]", total_value: float = 100_000.0) -> _SnapshotDay:
    return _SnapshotDay(
        snapshot_date = "2026-06-01",
        total_value   = total_value,
        holdings_json = holdings_json,
    )


# ══════════════════════════════════════════════════════════════════════════════
# 1-4. Removed helpers
# ══════════════════════════════════════════════════════════════════════════════

def test_realized_re_not_in_rebuilder():
    import services.portfolio_rebuilder as mod
    assert not hasattr(mod, "_REALIZED_RE")


def test_qcorr_re_not_in_rebuilder():
    import services.portfolio_rebuilder as mod
    assert not hasattr(mod, "_QCORR_RE")


def test_parse_realized_pnl_not_in_rebuilder():
    import services.portfolio_rebuilder as mod
    assert not hasattr(mod, "_parse_realized_pnl")


def test_parse_qty_correction_delta_not_in_rebuilder():
    import services.portfolio_rebuilder as mod
    assert not hasattr(mod, "_parse_qty_correction_delta")


# ══════════════════════════════════════════════════════════════════════════════
# 5-8. Cash-only transaction types
# ══════════════════════════════════════════════════════════════════════════════

def test_deposit_increases_cash():
    s = _state(0.0)
    _apply_transaction(s, _ctx(transaction_type="DEPOSIT", total_amount=50_000.0,
                                raw_symbol=None, canonical_symbol=None, shares=0.0))
    assert s.cash_balance == Decimal("50000.0")


def test_initial_cash_increases_cash():
    s = _state(0.0)
    _apply_transaction(s, _ctx(transaction_type="INITIAL_CASH", total_amount=20_000.0,
                                raw_symbol=None, canonical_symbol=None, shares=0.0))
    assert s.cash_balance == Decimal("20000.0")


def test_withdraw_decreases_cash():
    s = _state(30_000.0)
    _apply_transaction(s, _ctx(transaction_type="WITHDRAW", total_amount=10_000.0,
                                raw_symbol=None, canonical_symbol=None, shares=0.0))
    assert s.cash_balance == Decimal("20000.0")


def test_dividend_increases_cash():
    s = _state(5_000.0)
    _apply_transaction(s, _ctx(transaction_type="DIVIDEND", total_amount=500.0,
                                shares=0.0))
    assert s.cash_balance == Decimal("5500.0")


# ══════════════════════════════════════════════════════════════════════════════
# 9-11. BUY
# ══════════════════════════════════════════════════════════════════════════════

def test_buy_reduces_cash_and_adds_holding():
    s = _state(100_000.0)
    tx = _ctx(transaction_type="BUY", shares=100.0, total_amount=7_550.0,
              canonical_symbol="AOT.BK")
    _apply_transaction(s, tx)
    assert s.cash_balance == Decimal("100000.0") - Decimal("7550.0")
    assert "AOT.BK" in s.holdings
    h = s.holdings["AOT.BK"]
    assert h.shares == Decimal("100.0")
    # avg_cost = total_amount / shares = 7550 / 100 = 75.5
    assert h.avg_cost == Decimal("7550.0") / Decimal("100.0")


def test_buy_into_existing_holding_merges_weighted_avg():
    s = _state(200_000.0)
    # First buy: 100 shares @ effective 75.50 each (total_amount 7550)
    _apply_transaction(s, _ctx(id=1, transaction_type="BUY", shares=100.0,
                                total_amount=7_550.0, canonical_symbol="AOT.BK"))
    # Second buy: 100 shares @ effective 80.00 each (total_amount 8000)
    _apply_transaction(s, _ctx(id=2, transaction_type="BUY", shares=100.0,
                                total_amount=8_000.0, canonical_symbol="AOT.BK"))

    h = s.holdings["AOT.BK"]
    assert h.shares == Decimal("200.0")
    expected_avg = (Decimal("7550.0") + Decimal("8000.0")) / Decimal("200.0")
    assert h.avg_cost == expected_avg


def test_buy_zero_shares_is_no_op():
    s = _state(100_000.0)
    _apply_transaction(s, _ctx(transaction_type="BUY", shares=0.0, total_amount=0.0,
                                canonical_symbol="AOT.BK"))
    assert "AOT.BK" not in s.holdings
    assert s.cash_balance == Decimal("100000.0")


# ══════════════════════════════════════════════════════════════════════════════
# 12-15. SELL
# ══════════════════════════════════════════════════════════════════════════════

def test_sell_full_position_removes_holding():
    s = _state(0.0)
    s.holdings["AOT.BK"] = _HoldingState("AOT.BK", "AOT.BK", Decimal("100"), Decimal("75"), "Transport")
    _apply_transaction(s, _ctx(transaction_type="SELL", shares=100.0, total_amount=8_000.0,
                                canonical_symbol="AOT.BK", realized_pnl=500.0))
    assert "AOT.BK" not in s.holdings
    assert s.cash_balance == Decimal("8000.0")
    assert s.cumulative_realized_pnl == Decimal("500.0")


def test_sell_partial_reduces_shares():
    s = _state(0.0)
    s.holdings["AOT.BK"] = _HoldingState("AOT.BK", "AOT.BK", Decimal("200"), Decimal("75"), "Transport")
    _apply_transaction(s, _ctx(transaction_type="SELL", shares=50.0, total_amount=4_000.0,
                                canonical_symbol="AOT.BK", realized_pnl=250.0))
    assert "AOT.BK" in s.holdings
    assert s.holdings["AOT.BK"].shares == Decimal("150")


def test_sell_accumulates_realized_pnl_from_ctx():
    s = _state(0.0)
    s.holdings["AOT.BK"] = _HoldingState("AOT.BK", "AOT.BK", Decimal("100"), Decimal("75"), None)
    _apply_transaction(s, _ctx(transaction_type="SELL", shares=100.0, total_amount=8_000.0,
                                canonical_symbol="AOT.BK", realized_pnl=1_234.56))
    assert float(s.cumulative_realized_pnl) == pytest.approx(1_234.56)


def test_sell_with_none_realized_pnl_treated_as_zero():
    s = _state(0.0)
    s.holdings["AOT.BK"] = _HoldingState("AOT.BK", "AOT.BK", Decimal("100"), Decimal("75"), None)
    _apply_transaction(s, _ctx(transaction_type="SELL", shares=100.0, total_amount=8_000.0,
                                canonical_symbol="AOT.BK", realized_pnl=None))
    assert s.cumulative_realized_pnl == Decimal("0")


# ══════════════════════════════════════════════════════════════════════════════
# 16-18. INITIAL_POSITION
# ══════════════════════════════════════════════════════════════════════════════

def test_initial_position_adds_holding_without_affecting_cash():
    s = _state(50_000.0)
    _apply_transaction(s, _ctx(transaction_type="INITIAL_POSITION", shares=200.0,
                                price_per_share=60.0, total_amount=12_000.0,
                                raw_symbol="KBANK.BK", canonical_symbol="KBANK.BK"))
    assert s.cash_balance == Decimal("50000.0")  # unchanged
    assert "KBANK.BK" in s.holdings
    h = s.holdings["KBANK.BK"]
    assert h.shares == Decimal("200.0")
    assert h.avg_cost == Decimal("60.0")


def test_initial_position_merges_into_existing_holding():
    s = _state(0.0)
    s.holdings["KBANK.BK"] = _HoldingState("KBANK.BK", "KBANK.BK", Decimal("100"), Decimal("60"), None)
    _apply_transaction(s, _ctx(transaction_type="INITIAL_POSITION", shares=100.0,
                                price_per_share=70.0, total_amount=7_000.0,
                                raw_symbol="KBANK.BK", canonical_symbol="KBANK.BK"))
    h = s.holdings["KBANK.BK"]
    assert h.shares == Decimal("200")
    expected_avg = (Decimal("100") * Decimal("60") + Decimal("100") * Decimal("70")) / Decimal("200")
    assert h.avg_cost == expected_avg


def test_initial_position_zero_shares_is_no_op():
    s = _state(0.0)
    _apply_transaction(s, _ctx(transaction_type="INITIAL_POSITION", shares=0.0,
                                canonical_symbol="KBANK.BK"))
    assert "KBANK.BK" not in s.holdings


# ══════════════════════════════════════════════════════════════════════════════
# 19-22. QUANTITY_CORRECTION
# ══════════════════════════════════════════════════════════════════════════════

def test_qcorr_positive_delta_increases_shares_and_adjusts_avg():
    s = _state(0.0)
    s.holdings["PTT.BK"] = _HoldingState("PTT.BK", "PTT.BK", Decimal("100"), Decimal("40"), None)
    _apply_transaction(s, _ctx(
        transaction_type     = "QUANTITY_CORRECTION",
        raw_symbol           = "PTT.BK",
        canonical_symbol     = "PTT.BK",
        shares               = 10.0,
        price_per_share      = 42.0,
        qty_correction_delta = Decimal("+10.0"),
    ))
    h = s.holdings["PTT.BK"]
    assert h.shares == Decimal("110")
    expected_avg = (Decimal("100") * Decimal("40") + Decimal("10") * Decimal("42")) / Decimal("110")
    assert float(h.avg_cost) == pytest.approx(float(expected_avg), rel=1e-6)
    assert s.cash_balance == Decimal("0")  # cash unaffected


def test_qcorr_negative_delta_decreases_shares():
    s = _state(0.0)
    s.holdings["PTT.BK"] = _HoldingState("PTT.BK", "PTT.BK", Decimal("100"), Decimal("40"), None)
    _apply_transaction(s, _ctx(
        transaction_type     = "QUANTITY_CORRECTION",
        raw_symbol           = "PTT.BK",
        canonical_symbol     = "PTT.BK",
        shares               = 20.0,
        price_per_share      = 42.0,
        qty_correction_delta = Decimal("-20.0"),
    ))
    assert s.holdings["PTT.BK"].shares == Decimal("80")


def test_qcorr_zeros_holding_removes_it():
    s = _state(0.0)
    s.holdings["PTT.BK"] = _HoldingState("PTT.BK", "PTT.BK", Decimal("50"), Decimal("40"), None)
    _apply_transaction(s, _ctx(
        transaction_type     = "QUANTITY_CORRECTION",
        raw_symbol           = "PTT.BK",
        canonical_symbol     = "PTT.BK",
        shares               = 50.0,
        qty_correction_delta = Decimal("-50.0"),
    ))
    assert "PTT.BK" not in s.holdings


def test_qcorr_unknown_symbol_is_no_op():
    s = _state(10_000.0)
    _apply_transaction(s, _ctx(
        transaction_type     = "QUANTITY_CORRECTION",
        raw_symbol           = "NONEXISTENT.BK",
        canonical_symbol     = "NONEXISTENT.BK",
        shares               = 10.0,
        qty_correction_delta = Decimal("+10.0"),
    ))
    assert "NONEXISTENT.BK" not in s.holdings
    assert s.cash_balance == Decimal("10000.0")


# ══════════════════════════════════════════════════════════════════════════════
# 23. ReplayKey used as holdings key (Stage 0 / ADR-005) — DR price_symbol preserved
# ══════════════════════════════════════════════════════════════════════════════

def test_replay_key_used_as_holdings_key():
    """Holdings keys use replay_key(ctx) (canonical_symbol at Stage 0), not
    raw_symbol — the ADR-005 fix. See test_kbank_and_kbank_bk_merge_into_one_holding
    for the alias-merge case this exists to enable.
    """
    s = _state(100_000.0)
    tx = _ctx(
        transaction_type = "BUY",
        raw_symbol       = "KBANK",
        canonical_symbol = "KBANK.BK",
        shares           = 10.0,
        total_amount     = 5_000.0,
    )
    _apply_transaction(s, tx)
    assert "KBANK.BK" in s.holdings     # canonical_symbol (ReplayKey) used as key
    assert "KBANK" not in s.holdings    # raw_symbol NOT used as key


def test_kbank_and_kbank_bk_merge_into_one_holding():
    """The ADR-005 regression case: two raw spellings of the same instrument
    must merge into a single holding once replay keys by ReplayKey.
    """
    s = _state(100_000.0)
    _apply_transaction(s, _ctx(
        id=1, transaction_type="BUY", raw_symbol="KBANK", canonical_symbol="KBANK.BK",
        shares=100.0, total_amount=14_000.0,
    ))
    _apply_transaction(s, _ctx(
        id=2, transaction_type="BUY", raw_symbol="KBANK.BK", canonical_symbol="KBANK.BK",
        shares=50.0, total_amount=7_100.0,
    ))
    assert list(s.holdings.keys()) == ["KBANK.BK"]
    h = s.holdings["KBANK.BK"]
    assert h.shares == Decimal("150.0")
    assert h.avg_cost == (Decimal("14000.0") + Decimal("7100.0")) / Decimal("150.0")


def test_dr_holding_keyed_by_canonical_but_price_symbol_preserves_raw_form():
    """DR certificates (NVDA01.BK) resolve via canonical_symbol to the US
    underlying ticker (NVDA) — correct for replay identity, but yfinance must
    still be asked for the DR's own THB price, not the US ticker's USD price.
    _HoldingState.price_symbol carries the raw, DR-detectable form so
    _build_price_matrix's is_dr() branch keeps firing correctly post Stage 0.
    """
    s = _state(100_000.0)
    tx = _ctx(
        transaction_type = "BUY",
        raw_symbol       = "NVDA01.BK",
        canonical_symbol = "NVDA",
        shares           = 10.0,
        total_amount     = 5_000.0,
    )
    _apply_transaction(s, tx)
    assert "NVDA" in s.holdings              # ReplayKey (canonical_symbol) is the key
    assert "NVDA01.BK" not in s.holdings     # raw_symbol is NOT the key
    assert s.holdings["NVDA"].price_symbol == "NVDA01.BK"   # but preserved for price fetch


def test_price_symbol_falls_back_to_holdings_key_when_not_dr():
    """Non-DR holdings: price_symbol is simply the raw_symbol seen at creation,
    which for ordinary Thai equities is either identical to the ReplayKey or
    an equally valid yfinance ticker (KBANK vs KBANK.BK — both resolve fine).
    """
    s = _state(100_000.0)
    tx = _ctx(
        transaction_type = "BUY",
        raw_symbol       = "AOT.BK",
        canonical_symbol = "AOT.BK",
        shares           = 100.0,
        total_amount     = 7_500.0,
    )
    _apply_transaction(s, tx)
    assert s.holdings["AOT.BK"].price_symbol == "AOT.BK"


# ══════════════════════════════════════════════════════════════════════════════
# 24-27. _replay_with_date_snapshots
# ══════════════════════════════════════════════════════════════════════════════

def _buy(id: int, sym: str, shares: float, amount: float, dt: date) -> CanonicalTransaction:
    return _ctx(id=id, transaction_type="BUY", canonical_symbol=sym,
                shares=shares, total_amount=amount, transaction_date=dt)


def test_replay_single_date_captures_correct_state():
    txs = [
        _buy(1, "AOT.BK", 100.0, 7_000.0, date(2026, 1, 10)),
        _buy(2, "AOT.BK", 50.0,  3_500.0, date(2026, 1, 20)),
    ]
    # Snapshot date between the two buys — only first should be applied
    result = _replay_with_date_snapshots(txs, ["2026-01-15"])
    state = result["2026-01-15"]
    assert state.holdings["AOT.BK"].shares == Decimal("100.0")


def test_replay_transactions_after_date_not_applied():
    txs = [
        _buy(1, "AOT.BK", 100.0, 7_000.0, date(2026, 2, 1)),  # after snap date
    ]
    result = _replay_with_date_snapshots(txs, ["2026-01-31"])
    state = result["2026-01-31"]
    assert "AOT.BK" not in state.holdings


def test_replay_second_date_builds_on_first():
    txs = [
        _buy(1, "AOT.BK", 100.0, 7_000.0, date(2026, 1, 10)),
        _buy(2, "AOT.BK", 50.0,  3_500.0, date(2026, 1, 20)),
    ]
    result = _replay_with_date_snapshots(txs, ["2026-01-15", "2026-01-25"])
    state_15 = result["2026-01-15"]
    state_25 = result["2026-01-25"]
    assert state_15.holdings["AOT.BK"].shares == Decimal("100.0")
    assert state_25.holdings["AOT.BK"].shares == Decimal("150.0")


def test_replay_empty_txs_returns_initial_state():
    result = _replay_with_date_snapshots([], ["2026-01-01", "2026-02-01"])
    for date_str in ["2026-01-01", "2026-02-01"]:
        state = result[date_str]
        assert state.cash_balance == Decimal("0")
        assert state.holdings == {}


# ══════════════════════════════════════════════════════════════════════════════
# 28-33. _populate_return_fields
# ══════════════════════════════════════════════════════════════════════════════

def _pop(txs, prev="2026-05-31", curr="2026-06-01", prev_nav=100_000.0,
         total_value=100_000.0) -> _SnapshotDay:
    day = _day(total_value=total_value)
    _populate_return_fields(day, prev, curr, prev_nav, txs)
    return day


def _make_tx(id: int, tx_type: str, amount: float, sym: str | None = None,
             shares: float = 0.0, fees: float = 0.0, taxes: float = 0.0,
             realized_pnl: float | None = None,
             qty_delta: Decimal | None = None,
             dt: date = date(2026, 6, 1)) -> CanonicalTransaction:
    return CanonicalTransaction(
        id                   = id,
        transaction_type     = tx_type,
        raw_symbol           = sym,
        canonical_symbol     = sym,
        shares               = Decimal(str(shares)),
        price_per_share      = Decimal("0"),
        total_amount         = Decimal(str(amount)),
        fees                 = Decimal(str(fees)),
        taxes                = Decimal(str(taxes)),
        transaction_date     = dt,
        created_at           = None,
        sector               = None,
        notes                = None,
        qty_correction_delta = qty_delta,
        realized_pnl         = realized_pnl,
    )


def test_populate_deposit_counted_in_net_ecf():
    txs = [_make_tx(1, "DEPOSIT", 10_000.0)]
    day = _pop(txs, total_value=110_000.0, prev_nav=100_000.0)
    assert day.net_external_cash_flow == pytest.approx(10_000.0)


def test_populate_withdraw_counted_in_net_ecf():
    txs = [_make_tx(1, "WITHDRAW", 5_000.0)]
    day = _pop(txs, total_value=95_000.0, prev_nav=100_000.0)
    assert day.net_external_cash_flow == pytest.approx(-5_000.0)


def test_populate_buy_fees_and_taxes_in_period_fees():
    txs = [_make_tx(1, "BUY", 8_000.0, fees=50.0, taxes=3.50)]
    day = _pop(txs)
    assert day.period_fees_paid == pytest.approx(53.50)


def test_populate_sell_pnl_and_fees_in_period_decomposition():
    txs = [_make_tx(1, "SELL", 9_000.0, fees=60.0, taxes=4.20,
                    realized_pnl=750.0)]
    day = _pop(txs)
    assert day.period_realized_pnl == pytest.approx(750.0)
    assert day.period_fees_paid    == pytest.approx(64.20)


def test_populate_dividend_in_period_income():
    txs = [_make_tx(1, "DIVIDEND", 1_200.0)]
    day = _pop(txs)
    assert day.period_dividend_income == pytest.approx(1_200.0)


def test_populate_transactions_outside_window_excluded():
    txs_in  = [_make_tx(1, "DEPOSIT", 5_000.0, dt=date(2026, 6, 1))]
    txs_out = [_make_tx(2, "DEPOSIT", 99_000.0, dt=date(2026, 5, 31))]  # on prev_date = excluded
    day_in  = _pop(txs_in,  prev="2026-05-31", curr="2026-06-01", total_value=105_000.0)
    day_out = _pop(txs_out, prev="2026-05-31", curr="2026-06-01", total_value=100_000.0)
    assert day_in.net_external_cash_flow  == pytest.approx(5_000.0)
    assert day_out.net_external_cash_flow is None  # excluded → None


# ══════════════════════════════════════════════════════════════════════════════
# Phase 6 — Confidence score + backup export
# ══════════════════════════════════════════════════════════════════════════════

def _result(**kwargs) -> RebuildResult:
    """Minimal RebuildResult factory for confidence tests.

    Defaults transactions_replayed=1 so replay_confidence=100 for 'no issues' tests.
    """
    return RebuildResult(
        portfolio_id          = kwargs.pop("portfolio_id", 1),
        portfolio_name        = kwargs.pop("portfolio_name", "Test"),
        success               = kwargs.pop("success", True),
        transactions_replayed = kwargs.pop("transactions_replayed", 1),
        **kwargs,
    )


# ──────────────────────────────────────────────────────────────────────────────
# 34-40. _compute_confidence_score (delegates to _compute_confidence_report)
# These verify the scalar value returned by the backward-compat wrapper.
# ──────────────────────────────────────────────────────────────────────────────

def test_confidence_score_100_when_no_issues():
    r = _result()
    # All dimensions perfect → overall = 100.0
    assert _compute_confidence_score(r, []) == pytest.approx(100.0)


def test_confidence_score_penalises_critical_finding():
    r = _result(ledger_criticals=1)
    # ledger_integrity = 100-10 = 90; validator_confidence = 0
    # overall = 100×0.20 + 90×0.25 + 100×0.20 + 100×0.20 + 0×0.15 = 82.5
    assert _compute_confidence_score(r, []) == pytest.approx(82.5)


def test_confidence_score_penalises_error_finding():
    r = _result(ledger_errors=1)
    # ledger_integrity = 100-5 = 95; validator_confidence = 100
    # overall = 100×0.20 + 95×0.25 + 100×0.20 + 100×0.20 + 100×0.15 = 98.75 → 98.8
    assert _compute_confidence_score(r, []) == pytest.approx(98.75, abs=0.1)


def test_confidence_score_penalises_warning_finding():
    r = _result(ledger_warnings=1)
    # ledger_integrity = 100-2 = 98; validator_confidence = 100
    # overall = 100×0.20 + 98×0.25 + 100×0.20 + 100×0.20 + 100×0.15 = 99.5
    assert _compute_confidence_score(r, []) == pytest.approx(99.5)


def test_confidence_score_penalises_different_items():
    r = _result(items_different=2)
    # total_recon = 2; different_recon = 2 → snapshot_consistency = 0.0
    # overall = 100×0.20 + 100×0.25 + 100×0.20 + 0×0.20 + 100×0.15 = 80.0
    assert _compute_confidence_score(r, []) == pytest.approx(80.0)


def test_confidence_score_penalises_low_coverage_snapshots():
    low = _day()
    low.holdings_count = 1
    low.price_coverage = _COVERAGE_THRESHOLD - 0.01   # just below threshold
    r = _result()
    # 1/1 low-coverage → historical_coverage = 0.0
    # overall = 100×0.20 + 100×0.25 + 0×0.20 + 100×0.20 + 100×0.15 = 80.0
    assert _compute_confidence_score(r, [low]) == pytest.approx(80.0)


def test_full_coverage_snapshot_not_penalised():
    ok = _day()
    ok.holdings_count = 1
    ok.price_coverage = _COVERAGE_THRESHOLD   # exactly at threshold → not penalised
    r = _result()
    assert _compute_confidence_score(r, [ok]) == pytest.approx(100.0)


def test_confidence_score_many_criticals_reduces_ledger_and_validator():
    r = _result(ledger_criticals=10)
    # ledger_integrity = max(0, 100-100) = 0; validator_confidence = 0
    # replay=100, coverage=100, consistency=100 still contribute
    # overall = 100×0.20 + 0×0.25 + 100×0.20 + 100×0.20 + 0×0.15 = 60.0
    assert _compute_confidence_score(r, []) == pytest.approx(60.0)


def test_export_backup_creates_valid_json_file():
    mock_portfolio = MagicMock()
    mock_portfolio.name = "Test Portfolio"
    mock_portfolio.cash_balance = 100_000.0

    mock_db = MagicMock()
    # filter_by(...).first() → portfolio
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_portfolio
    # filter_by(...).all() → empty lists (items + snapshots)
    mock_db.query.return_value.filter_by.return_value.all.return_value = []

    with tempfile.TemporaryDirectory() as tmpdir:
        path = _export_backup(mock_db, portfolio_id=7, backup_dir=tmpdir)

        assert path.endswith(".json")
        assert os.path.isfile(path)

        with open(path) as fh:
            data = json.load(fh)

        assert data["portfolio_id"] == 7
        assert "backup_timestamp" in data
        assert data["portfolio"]["name"] == "Test Portfolio"
        assert data["portfolio"]["cash_balance"] == pytest.approx(100_000.0)
        assert data["portfolio_items"] == []
        assert data["snapshots"] == []


# ══════════════════════════════════════════════════════════════════════════════
# Phase 6.5 — ConfidenceReport, _values_differ, _generate_execution_plan
# ══════════════════════════════════════════════════════════════════════════════

# ── _compute_confidence_report (multi-dimensional) ────────────────────────────

def test_confidence_report_all_dimensions_perfect():
    r = _result()
    report = _compute_confidence_report(r, [])
    assert report.replay_confidence    == 100.0
    assert report.ledger_integrity     == 100.0
    assert report.historical_coverage  == 100.0
    assert report.snapshot_consistency == 100.0
    assert report.validator_confidence == 100.0
    assert report.overall              == 100.0


def test_confidence_report_replay_zero_transactions():
    r = _result(transactions_replayed=0)
    report = _compute_confidence_report(r, [])
    assert report.replay_confidence == 0.0
    # overall = 0×0.20 + 100×0.25 + 100×0.20 + 100×0.20 + 100×0.15 = 80.0
    assert report.overall == pytest.approx(80.0)


def test_confidence_report_ledger_integrity_deductions():
    # CRITICAL deduction: 10 per finding; ERROR: 5; WARNING: 2
    r = _result(ledger_criticals=1, ledger_errors=2, ledger_warnings=3)
    report = _compute_confidence_report(r, [])
    expected_ledger = max(0.0, 100.0 - 1 * _CONF_LEDGER_PER_CRITICAL
                                     - 2 * _CONF_LEDGER_PER_ERROR
                                     - 3 * _CONF_LEDGER_PER_WARNING)
    assert report.ledger_integrity == pytest.approx(expected_ledger, abs=0.1)


def test_confidence_report_validator_confidence_zero_on_critical():
    r = _result(ledger_criticals=1)
    report = _compute_confidence_report(r, [])
    assert report.validator_confidence == 0.0


def test_confidence_report_validator_confidence_full_when_no_critical():
    r = _result(ledger_errors=3, ledger_warnings=5)
    report = _compute_confidence_report(r, [])
    assert report.validator_confidence == 100.0


def test_confidence_report_historical_coverage_proportional():
    snap_low  = _day(); snap_low.holdings_count  = 1; snap_low.price_coverage  = 0.50
    snap_high = _day(); snap_high.holdings_count = 1; snap_high.price_coverage = 1.00
    r = _result()
    report = _compute_confidence_report(r, [snap_low, snap_high])
    # 1 out of 2 snaps below threshold → historical_coverage = 100 × (1 - 1/2) = 50.0
    assert report.historical_coverage == pytest.approx(50.0)


def test_confidence_report_snapshot_consistency_includes_items():
    # items_different counts toward snapshot_consistency dimension
    r = _result(items_matched=8, items_different=2)
    report = _compute_confidence_report(r, [])
    # total_recon=10, different=2 → consistency = 80.0
    assert report.snapshot_consistency == pytest.approx(80.0)


def test_confidence_report_overall_equals_weighted_sum():
    """Overall must exactly match the documented weighted formula."""
    r = _result(ledger_errors=1, ledger_warnings=2, snapshots_different=1, snapshots_matched=4)
    snaps = []
    report = _compute_confidence_report(r, snaps)
    expected = round(
        report.replay_confidence    * _CONF_W_REPLAY
        + report.ledger_integrity   * _CONF_W_LEDGER
        + report.historical_coverage * _CONF_W_COVERAGE
        + report.snapshot_consistency * _CONF_W_CONSISTENCY
        + report.validator_confidence * _CONF_W_VALIDATOR,
        1,
    )
    assert report.overall == pytest.approx(expected, abs=0.01)


# ── _values_differ ────────────────────────────────────────────────────────────

def test_values_differ_both_none():
    assert _values_differ(None, None) is False


def test_values_differ_one_none():
    assert _values_differ(None, 1.0) is True
    assert _values_differ(1.0, None) is True


def test_values_differ_within_tolerance():
    assert _values_differ(100.0, 100.005, tol=0.01) is False


def test_values_differ_exceeds_tolerance():
    assert _values_differ(100.0, 100.02, tol=0.01) is True


def test_values_differ_strings():
    assert _values_differ("AOT.BK", "AOT.BK") is False
    assert _values_differ("AOT.BK", "PTT.BK") is True


# ── _generate_execution_plan ──────────────────────────────────────────────────

def _mock_portfolio_obj(cash: float) -> MagicMock:
    p = MagicMock()
    p.cash_balance = cash
    p.id = 1
    return p


def _mock_item(symbol: str, shares: float, avg_cost: float) -> MagicMock:
    m = MagicMock()
    m.symbol   = symbol
    m.shares   = shares
    m.avg_cost = avg_cost
    return m


def _make_mock_db(items: list[MagicMock]) -> MagicMock:
    """Mock DB session that returns given items for PortfolioItem queries
    and empty list for PortfolioSnapshot queries."""
    db = MagicMock()

    from models.database import PortfolioItem, PortfolioSnapshot

    def _query(model):
        m = MagicMock()
        if model is PortfolioItem:
            m.filter_by.return_value.all.return_value = items
        else:
            # PortfolioSnapshot
            fby = MagicMock()
            fby.filter.return_value.all.return_value = []
            fby.all.return_value = []
            m.filter_by.return_value = fby
        return m

    db.query.side_effect = _query
    return db


def _make_final_state(holdings: dict[str, tuple[float, float]]) -> _PortfolioState:
    """Create a _PortfolioState with given {symbol: (shares, avg_cost)} holdings."""
    state = _PortfolioState(
        cash_balance            = Decimal("0"),
        holdings                = {},
        cumulative_realized_pnl = Decimal("0"),
    )
    for sym, (sh, ac) in holdings.items():
        state.holdings[sym] = _HoldingState(
            symbol        = sym,
            report_symbol = sym,
            shares        = Decimal(str(sh)),
            avg_cost      = Decimal(str(ac)),
        )
    return state


def _make_confidence() -> ConfidenceReport:
    return ConfidenceReport(
        replay_confidence=100.0, ledger_integrity=100.0,
        historical_coverage=100.0, snapshot_consistency=100.0,
        validator_confidence=100.0, overall=100.0,
    )


def test_execution_plan_no_changes_when_state_matches():
    """When DB matches replay, plan has no PortfolioItem operations."""
    items    = [_mock_item("AOT.BK", 100.0, 75.5)]
    db       = _make_mock_db(items)
    final    = _make_final_state({"AOT.BK": (100.0, 75.5)})
    portfolio = _mock_portfolio_obj(cash=0.0)
    final.cash_balance = Decimal("0.0")

    plan = _generate_execution_plan(
        db=db, portfolio_id=1, portfolio=portfolio,
        final_state=final, snapshot_days=[],
        from_date=None, confidence=_make_confidence(),
        validator=None, skip_snapshots=True,
    )

    item_ops = [o for o in plan.operations if o.table == "PortfolioItem"]
    assert item_ops == []
    assert plan.summary.item_updates == 0
    assert plan.summary.item_inserts == 0
    assert plan.summary.item_deletes == 0


def test_execution_plan_update_when_avg_cost_differs():
    """Changed avg_cost generates an UPDATE PlanOperation."""
    items    = [_mock_item("KBANK.BK", 200.0, 140.0)]   # current DB value
    db       = _make_mock_db(items)
    final    = _make_final_state({"KBANK.BK": (200.0, 142.5)})  # reconstructed
    portfolio = _mock_portfolio_obj(cash=0.0)
    final.cash_balance = Decimal("0.0")

    plan = _generate_execution_plan(
        db=db, portfolio_id=1, portfolio=portfolio,
        final_state=final, snapshot_days=[],
        from_date=None, confidence=_make_confidence(),
        validator=None, skip_snapshots=True,
    )

    update_ops = [o for o in plan.operations
                  if o.table == "PortfolioItem" and o.operation == "UPDATE"]
    assert any(o.field == "avg_cost" for o in update_ops)
    assert plan.summary.item_updates == 1


def test_execution_plan_insert_for_new_symbol():
    """Symbol in final_state but not in DB generates INSERT."""
    db       = _make_mock_db([])   # no existing items
    final    = _make_final_state({"PTT.BK": (300.0, 35.0)})
    portfolio = _mock_portfolio_obj(cash=0.0)
    final.cash_balance = Decimal("0.0")

    plan = _generate_execution_plan(
        db=db, portfolio_id=1, portfolio=portfolio,
        final_state=final, snapshot_days=[],
        from_date=None, confidence=_make_confidence(),
        validator=None, skip_snapshots=True,
    )

    insert_ops = [o for o in plan.operations
                  if o.table == "PortfolioItem" and o.operation == "INSERT"]
    assert len(insert_ops) == 1
    assert insert_ops[0].object_id == "PTT.BK"
    assert plan.summary.item_inserts == 1


def test_execution_plan_delete_for_closed_position():
    """Symbol in DB but absent from final_state generates DELETE."""
    items    = [_mock_item("CPALL.BK", 50.0, 60.0)]
    db       = _make_mock_db(items)
    final    = _make_final_state({})   # no holdings — position closed
    portfolio = _mock_portfolio_obj(cash=0.0)
    final.cash_balance = Decimal("0.0")

    plan = _generate_execution_plan(
        db=db, portfolio_id=1, portfolio=portfolio,
        final_state=final, snapshot_days=[],
        from_date=None, confidence=_make_confidence(),
        validator=None, skip_snapshots=True,
    )

    delete_ops = [o for o in plan.operations
                  if o.table == "PortfolioItem" and o.operation == "DELETE"]
    assert len(delete_ops) == 1
    assert delete_ops[0].object_id == "CPALL.BK"
    assert plan.summary.item_deletes == 1


def test_execution_plan_portfolio_cash_update():
    """Changed cash balance generates Portfolio UPDATE operation."""
    db        = _make_mock_db([])
    final     = _make_final_state({})
    portfolio = _mock_portfolio_obj(cash=50_000.0)
    final.cash_balance = Decimal("75000.0")   # different from current

    plan = _generate_execution_plan(
        db=db, portfolio_id=1, portfolio=portfolio,
        final_state=final, snapshot_days=[],
        from_date=None, confidence=_make_confidence(),
        validator=None, skip_snapshots=True,
    )

    port_ops = [o for o in plan.operations if o.table == "Portfolio"]
    assert len(port_ops) == 1
    assert port_ops[0].operation == "UPDATE"
    assert port_ops[0].field == "cash_balance"
    assert "cash_balance" in plan.summary.portfolio_updated_fields


def test_execution_plan_total_write_operations_count():
    """total_write_operations is object-level (not field-level)."""
    items    = [_mock_item("AOT.BK", 100.0, 75.5)]   # will have 2 field diffs
    db       = _make_mock_db(items)
    # Both shares and avg_cost differ → 2 UPDATE ops, but 1 object
    final    = _make_final_state({"AOT.BK": (110.0, 78.0)})
    portfolio = _mock_portfolio_obj(cash=0.0)
    final.cash_balance = Decimal("0.0")

    plan = _generate_execution_plan(
        db=db, portfolio_id=1, portfolio=portfolio,
        final_state=final, snapshot_days=[],
        from_date=None, confidence=_make_confidence(),
        validator=None, skip_snapshots=True,
    )

    assert plan.summary.item_updates == 1              # 1 object updated
    assert plan.summary.total_write_operations == 1    # object-level count
    # But two PlanOperation records generated (one per field)
    update_ops = [o for o in plan.operations
                  if o.table == "PortfolioItem" and o.operation == "UPDATE"]
    assert len(update_ops) == 2


# ══════════════════════════════════════════════════════════════════════════════
# Phase 6.7C — Effective Ledger Replay Integration
# ══════════════════════════════════════════════════════════════════════════════

# ── Integration helpers ────────────────────────────────────────────────────────

def _make_portfolio_obj(id: int = 1, name: str = "Test", cash: float = 0.0) -> MagicMock:
    p = MagicMock()
    p.id = id
    p.name = name
    p.cash_balance = cash
    return p


def _make_raw_tx_mock(tx_id: int, asset_id: int | None = None) -> MagicMock:
    t = MagicMock()
    t.id       = tx_id
    t.asset_id = asset_id
    return t


def _make_repair_ns(
    repair_id: int,
    tx_id: int | None,
    repair_type: str = "EXCLUDE",
) -> SimpleNamespace:
    return SimpleNamespace(
        id             = repair_id,
        transaction_id = tx_id,
        repair_type    = repair_type,
        reason         = "test",
        reason_code    = None,
        is_active      = True,
    )


def _clean_report(portfolio_id: int = 1) -> LedgerValidationReport:
    return LedgerValidationReport(
        portfolio_id           = portfolio_id,
        portfolio_name         = "Test",
        transactions_inspected = 0,
    )


def _make_rebuild_mock_db(
    portfolio:      MagicMock,
    raw_txs:        list,
    items:          list | None = None,
    existing_snaps: list | None = None,
) -> MagicMock:
    """Mock DB session sufficient for rebuild_portfolio(skip_snapshots=True, dry_run=True).

    existing_snaps (default []): rows returned by the Stage 2 existing_snaps
    query AND by the per-date upsert lookup's .first() (matched by
    snapshot_date so an admissible bounded rebuild upserts in place rather
    than blindly inserting — WP5-A8 needs this to prove a pre-boundary row is
    never even queried-for-update, not just never returned)."""
    from models.database import Portfolio, Transaction, PortfolioItem, PortfolioSnapshot

    items          = items or []
    existing_snaps = existing_snaps or []
    db             = MagicMock()

    def _query(model):
        m = MagicMock()
        if model is Portfolio:
            m.filter_by.return_value.first.return_value = portfolio
        elif model is Transaction:
            m.filter_by.return_value.order_by.return_value.all.return_value = raw_txs
        elif model is PortfolioItem:
            m.filter_by.return_value.all.return_value = items
            m.filter_by.return_value.delete.return_value = None
        elif model is PortfolioSnapshot:
            snap_m = MagicMock()
            snap_m.all.return_value                       = existing_snaps
            snap_m.order_by.return_value.all.return_value  = existing_snaps

            def _filter_by(**kw):
                fm = MagicMock()
                fm.all.return_value                       = existing_snaps
                fm.order_by.return_value.all.return_value = existing_snaps
                fm.filter.return_value.all.return_value   = existing_snaps
                snap_date = kw.get("snapshot_date")
                fm.first.return_value = next(
                    (s for s in existing_snaps if snap_date is not None and s.snapshot_date == snap_date),
                    None,
                )
                return fm

            m.filter_by.side_effect = _filter_by
        return m

    db.query.side_effect = _query
    return db


def _run(
    db,
    portfolio_id:   int  = 1,
    workspace_id:   int  = 1,
    apply_repairs:  bool = True,
    skip_snapshots: bool = True,
    dry_run:        bool = True,
) -> RebuildResult:
    return asyncio.run(rebuild_portfolio(
        db             = db,
        portfolio_id   = portfolio_id,
        workspace_id   = workspace_id,
        skip_snapshots = skip_snapshots,
        dry_run        = dry_run,
        apply_repairs  = apply_repairs,
    ))


# ── 34. RebuildResult new fields default to zero / empty ──────────────────────

def test_rebuild_result_new_fields_default_to_zero():
    r = RebuildResult(portfolio_id=1, portfolio_name="P", success=True)
    assert r.effective_transaction_count == 0
    assert r.excluded_transaction_count  == 0
    assert r.repairs_applied             == 0
    assert r.repair_ids                  == []
    assert r.reconstructed_realized_pnl  is None
    assert r.reconstructed_holding_basis == {}


def test_rebuild_exposes_zero_realized_pnl_without_snapshot_provider_fetch():
    """Stage 1 surfaces its zero P&L result even when later stages are skipped."""
    portfolio = _make_portfolio_obj(cash=0.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])
    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=100_000.0)]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())), \
         patch("services.portfolio_rebuilder._build_price_matrix",
               new=AsyncMock(return_value={})) as mock_fetch:
        r = _run(db, apply_repairs=True, skip_snapshots=True)

    assert r.success
    assert r.skip_snapshots is True
    assert r.reconstructed_realized_pnl == 0.0
    assert r.reconstructed_holding_basis == {}
    mock_fetch.assert_not_called()


def test_rebuild_exposes_canonical_sell_realized_pnl():
    """The result exposes the SELL P&L supplied by canonical replay."""
    portfolio = _make_portfolio_obj(cash=0.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1), _make_raw_tx_mock(2)])
    ctxs = [
        _ctx(id=1, transaction_type="INITIAL_POSITION", shares=100.0, price_per_share=75.0,
             total_amount=0.0, canonical_symbol="AOT.BK"),
        _ctx(id=2, transaction_type="SELL", shares=100.0, total_amount=8_000.0,
             canonical_symbol="AOT.BK", realized_pnl=500.0),
    ]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=False, skip_snapshots=True)

    assert r.success
    assert r.reconstructed_realized_pnl == pytest.approx(500.0)


# ── BANPU-WP5 — exact ordinary final-holding basis result surface ─────────────

def test_reconstructed_holding_basis_initial_position_is_exact_and_skips_provider():
    """Stage 1 exposes the raw Decimal basis before any snapshot/provider work."""
    symbol = "BASISINIT.BK"
    portfolio = _make_portfolio_obj(cash=0.0)
    db = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])
    ctxs = [
        _ctx(
            id=1, transaction_type="INITIAL_POSITION", raw_symbol=symbol,
            canonical_symbol=symbol, shares=1.0000004, price_per_share=100.0000004,
            total_amount=0.0,
        ),
    ]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())), \
         patch("services.portfolio_rebuilder._build_price_matrix",
               new=AsyncMock(return_value={})) as mock_fetch:
        r = _run(db, apply_repairs=False, skip_snapshots=True)

    exact_basis = Decimal("100.00004040000016")
    projected_rounded_basis = round(
        round(1.0000004, 6) * round(100.0000004, 6), 2
    )
    assert r.success
    assert r.reconstructed_holding_basis == {symbol: exact_basis}
    assert isinstance(r.reconstructed_holding_basis[symbol], Decimal)
    assert r.reconstructed_holding_basis[symbol] != Decimal("100.00")
    assert Decimal(str(projected_rounded_basis)) == Decimal("100.0")
    mock_fetch.assert_not_called()


def test_reconstructed_holding_basis_buy_uses_exact_weighted_average_state():
    """The result observes the Stage-1 weighted-average state, not a float report."""
    symbol = "BASISBUY.BK"
    portfolio = _make_portfolio_obj(cash=0.0)
    db = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1), _make_raw_tx_mock(2)])
    ctxs = [
        _ctx(
            id=1, transaction_type="INITIAL_POSITION", raw_symbol=symbol,
            canonical_symbol=symbol, shares=3.0, price_per_share=10.1234567,
            total_amount=0.0,
        ),
        _ctx(
            id=2, transaction_type="BUY", raw_symbol=symbol,
            canonical_symbol=symbol, shares=2.0, price_per_share=20.1234567,
            total_amount=40.2469134, fees=0.0, taxes=0.0,
        ),
    ]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=False, skip_snapshots=True)

    assert r.success
    assert r.reconstructed_holding_basis == {symbol: Decimal("70.6172835")}
    assert r.reconstructed_holding_basis[symbol] != Decimal("70.617285")


def test_reconstructed_holding_basis_partial_sell_preserves_remaining_basis():
    """SELL reduces shares while the observed basis retains Stage-1 average cost."""
    symbol = "BASISSELL.BK"
    portfolio = _make_portfolio_obj(cash=0.0)
    db = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1), _make_raw_tx_mock(2)])
    ctxs = [
        _ctx(
            id=1, transaction_type="INITIAL_POSITION", raw_symbol=symbol,
            canonical_symbol=symbol, shares=7.25, price_per_share=12.3456789,
            total_amount=0.0,
        ),
        _ctx(
            id=2, transaction_type="SELL", raw_symbol=symbol,
            canonical_symbol=symbol, shares=2.25, total_amount=30.0,
        ),
    ]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=False, skip_snapshots=True)

    assert r.success
    assert r.reconstructed_holding_basis == {symbol: Decimal("61.7283945")}


def test_reconstructed_holding_basis_uses_report_symbol_in_native_and_legacy_replay():
    """The output key is stable even when the Stage-1 merge key is native."""
    symbol = "BASISIDENTITY.BK"
    legacy_ctx = _ctx(
        id=1, transaction_type="INITIAL_POSITION", raw_symbol=symbol,
        canonical_symbol=symbol, shares=4.0, price_per_share=25.0, total_amount=0.0,
    )
    native_ctx = _ctx(
        id=1, transaction_type="INITIAL_POSITION", raw_symbol=symbol,
        canonical_symbol=symbol, shares=4.0, price_per_share=25.0, total_amount=0.0,
        asset_id=4242,
    )

    results = []
    for ctx in (legacy_ctx, native_ctx):
        db = _make_rebuild_mock_db(_make_portfolio_obj(cash=0.0), [_make_raw_tx_mock(1)])
        with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=[ctx]), \
             patch("services.portfolio_rebuilder.validate_portfolio_ledger",
                   new=AsyncMock(return_value=_clean_report())):
            results.append(_run(db, apply_repairs=False, skip_snapshots=True))

    assert all(r.success for r in results)
    assert [r.reconstructed_holding_basis for r in results] == [
        {symbol: Decimal("100.0")},
        {symbol: Decimal("100.0")},
    ]
    assert 4242 not in results[1].reconstructed_holding_basis


def test_reconstructed_holding_basis_duplicate_report_symbol_fails_closed():
    """Contradictory native final holdings must not overwrite one result key."""
    symbol = "BASISDUP.BK"
    portfolio = _make_portfolio_obj(cash=0.0)
    db = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1), _make_raw_tx_mock(2)])
    ctxs = [
        _ctx(
            id=1, transaction_type="INITIAL_POSITION", raw_symbol=symbol,
            canonical_symbol=symbol, shares=1.0, price_per_share=10.0,
            total_amount=0.0, asset_id=101,
        ),
        _ctx(
            id=2, transaction_type="INITIAL_POSITION", raw_symbol=symbol,
            canonical_symbol=symbol, shares=1.0, price_per_share=20.0,
            total_amount=0.0, asset_id=202,
        ),
    ]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())), \
         patch("services.portfolio_rebuilder._build_price_matrix",
               new=AsyncMock(return_value={})) as mock_fetch:
        r = _run(db, apply_repairs=False, skip_snapshots=True)

    assert r.success is False
    assert r.reconstructed_holding_basis == {}
    assert r.error == f"Duplicate report_symbol in reconstructed holdings: {symbol}"
    mock_fetch.assert_not_called()


# ── 35. apply_repairs=True with a single EXCLUDE repair ───────────────────────

def test_rebuild_apply_repairs_excludes_buy_transaction():
    """Excluded BUY must not appear in final holdings; counts are correct."""
    portfolio = _make_portfolio_obj(cash=100_000.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1), _make_raw_tx_mock(2)])

    ctxs = [
        _ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
             shares=0.0, total_amount=100_000.0),
        _ctx(id=2, transaction_type="BUY", shares=100.0, total_amount=7_550.0,
             canonical_symbol="AOT.BK"),
    ]
    repair = _make_repair_ns(repair_id=10, tx_id=2)

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[repair]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=True)

    assert r.success
    assert r.repairs_applied             == 1
    assert r.excluded_transaction_count  == 1
    assert r.effective_transaction_count == 1   # only DEPOSIT
    assert r.transactions_replayed       == 1
    assert r.repair_ids                  == [10]
    assert r.reconstructed_holdings_count == 0
    assert r.reconstructed_cash == pytest.approx(100_000.0)


# ── 36. apply_repairs=False — overlay never called, all txs replayed ──────────

def test_rebuild_apply_repairs_false_skips_overlay():
    """apply_repairs=False must not call load_active_repairs and replays every tx."""
    portfolio = _make_portfolio_obj(cash=100_000.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1), _make_raw_tx_mock(2)])

    ctxs = [
        _ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
             shares=0.0, total_amount=100_000.0),
        _ctx(id=2, transaction_type="BUY", shares=100.0, total_amount=7_550.0,
             canonical_symbol="AOT.BK"),
    ]
    repair = _make_repair_ns(repair_id=10, tx_id=2)

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[repair]) as mock_load, \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=False)

    mock_load.assert_not_called()
    assert r.success
    assert r.repairs_applied             == 0
    assert r.excluded_transaction_count  == 0
    assert r.effective_transaction_count == 2
    assert r.transactions_replayed       == 2
    assert r.repair_ids                  == []
    assert r.reconstructed_holdings_count == 1   # BUY replayed normally


# ── 37. Empty repair list — no exclusions, counts stay zero ───────────────────

def test_rebuild_empty_repair_list_is_no_op():
    portfolio = _make_portfolio_obj(cash=50_000.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])

    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=50_000.0)]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=True)

    assert r.success
    assert r.repairs_applied             == 0
    assert r.excluded_transaction_count  == 0
    assert r.effective_transaction_count == 1
    assert r.transactions_replayed       == 1
    assert r.repair_ids                  == []


# ── 38. Multiple EXCLUDE repairs — counts correct, only survivors replayed ─────

def test_rebuild_multiple_exclusions_counts_and_effective_replay():
    portfolio = _make_portfolio_obj(cash=300_000.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(i) for i in range(1, 6)])

    ctxs = [
        _ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
             shares=0.0, total_amount=300_000.0),
        _ctx(id=2, transaction_type="BUY", shares=100.0, total_amount=7_500.0,
             canonical_symbol="AOT.BK"),
        _ctx(id=3, transaction_type="BUY", shares=200.0, total_amount=8_000.0,
             canonical_symbol="PTT.BK"),
        _ctx(id=4, transaction_type="BUY", shares=50.0,  total_amount=3_000.0,
             canonical_symbol="KBANK.BK"),
        _ctx(id=5, transaction_type="DIVIDEND", raw_symbol=None, canonical_symbol=None,
             shares=0.0, total_amount=500.0),
    ]
    repairs = [
        _make_repair_ns(repair_id=20, tx_id=2),   # exclude AOT.BK BUY
        _make_repair_ns(repair_id=21, tx_id=4),   # exclude KBANK.BK BUY
    ]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=repairs), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=True)

    assert r.success
    assert r.repairs_applied             == 2
    assert r.excluded_transaction_count  == 2
    assert r.effective_transaction_count == 3    # DEPOSIT, PTT.BK BUY, DIVIDEND
    assert r.transactions_replayed       == 3
    assert r.repair_ids                  == [20, 21]
    assert r.reconstructed_holdings_count == 1   # only PTT.BK
    assert r.reconstructed_cash == pytest.approx(300_000.0 - 8_000.0 + 500.0)


# ── 39. Execution plan transaction counts match overlay results ────────────────

def test_rebuild_execution_plan_reflects_effective_count():
    """transactions_replayed must equal effective_transaction_count."""
    portfolio = _make_portfolio_obj(cash=200_000.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(i) for i in range(1, 4)])

    ctxs = [
        _ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
             shares=0.0, total_amount=200_000.0),
        _ctx(id=2, transaction_type="BUY", shares=100.0, total_amount=7_550.0,
             canonical_symbol="AOT.BK"),
        _ctx(id=3, transaction_type="BUY", shares=200.0, total_amount=8_000.0,
             canonical_symbol="PTT.BK"),
    ]
    repair = _make_repair_ns(repair_id=30, tx_id=2)

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[repair]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=True)

    assert r.transactions_replayed == r.effective_transaction_count == 2
    assert r.excluded_transaction_count == 1


# ── 40. validate_portfolio_ledger called with mode="effective" ─────────────────

def test_rebuild_validator_called_with_effective_mode():
    portfolio = _make_portfolio_obj(cash=0.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])

    ctxs   = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                   shares=0.0, total_amount=50_000.0)]
    repair = _make_repair_ns(repair_id=40, tx_id=99)   # orphan — no match

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[repair]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())) as mock_val:
        _run(db, apply_repairs=True)

    mock_val.assert_awaited_once()
    kw = mock_val.call_args.kwargs
    assert kw.get("mode")    == "effective"
    assert kw.get("repairs") == [repair]


# ── 41. apply_repairs=False — validator NOT called with mode/repairs ───────────

def test_rebuild_validator_no_mode_when_apply_repairs_false():
    portfolio = _make_portfolio_obj(cash=0.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])

    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=50_000.0)]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[]) as mock_load, \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())) as mock_val:
        _run(db, apply_repairs=False)

    mock_load.assert_not_called()
    kw = mock_val.call_args.kwargs
    assert "mode"    not in kw
    assert "repairs" not in kw


# ── 42. Confidence uses effective validator finding counts ─────────────────────

def test_rebuild_confidence_derived_from_effective_validator_report():
    from services.ledger_validator import FindingSeverity
    portfolio = _make_portfolio_obj(cash=0.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])

    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=50_000.0)]

    err_finding = LedgerFinding(
        check_id="CASH_MISMATCH", severity=FindingSeverity.ERROR,
        portfolio_id=1, transaction_ids=[], symbol=None, normalized_symbol=None,
        title="test", explanation="", recommendation="",
    )
    report_with_error = LedgerValidationReport(
        portfolio_id=1, portfolio_name="Test",
        transactions_inspected=1, findings=[err_finding],
    )

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=report_with_error)):
        r = _run(db, apply_repairs=True)

    assert r.ledger_errors    == 1
    assert r.ledger_criticals == 0
    assert r.confidence_report is not None
    assert r.confidence_report.ledger_integrity < 100.0


# ── 43. SUPPRESS_FINDING repair — tx stays in effective list ──────────────────

def test_rebuild_suppress_finding_does_not_exclude_transaction():
    """SUPPRESS_FINDING repairs pass through apply_repair_overlay unchanged."""
    portfolio = _make_portfolio_obj(cash=100_000.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1), _make_raw_tx_mock(2)])

    ctxs = [
        _ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
             shares=0.0, total_amount=100_000.0),
        _ctx(id=2, transaction_type="BUY", shares=100.0, total_amount=7_550.0,
             canonical_symbol="AOT.BK"),
    ]
    repair = _make_repair_ns(repair_id=50, tx_id=2, repair_type="SUPPRESS_FINDING")

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[repair]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=True)

    assert r.repairs_applied             == 0    # no exclusions
    assert r.excluded_transaction_count  == 0
    assert r.effective_transaction_count == 2    # both transactions in effective list
    assert r.transactions_replayed       == 2
    assert r.repair_ids                  == [50]  # repair was loaded
    assert r.reconstructed_holdings_count == 1   # BUY was replayed


# ── 44. repair_ids lists all loaded repairs regardless of type ─────────────────

def test_rebuild_repair_ids_contains_all_loaded_repairs():
    portfolio = _make_portfolio_obj(cash=100_000.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])

    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=100_000.0)]
    repairs = [
        _make_repair_ns(repair_id=60, tx_id=99,  repair_type="EXCLUDE"),         # orphan
        _make_repair_ns(repair_id=61, tx_id=1,   repair_type="SUPPRESS_FINDING"),
    ]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=repairs), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=True)

    assert sorted(r.repair_ids)         == [60, 61]
    assert r.repairs_applied            == 0   # orphan EXCLUDE → no match; SUPPRESS → no exclude
    assert r.excluded_transaction_count == 0


# ── 45. Backward compatibility — apply_repairs=True is the safe default ────────

def test_rebuild_default_apply_repairs_true():
    """Default apply_repairs=True means load_active_repairs IS called."""
    portfolio = _make_portfolio_obj(cash=0.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])

    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=10_000.0)]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[]) as mock_load, \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        asyncio.run(rebuild_portfolio(
            db=db, portfolio_id=1, workspace_id=1,
            skip_snapshots=True, dry_run=True,
            # apply_repairs not passed → defaults to True
        ))

    mock_load.assert_called_once()


# ── 46. rebuild_all_portfolios passes apply_repairs to rebuild_portfolio ────────

def test_rebuild_all_passes_apply_repairs():
    """rebuild_all_portfolios propagates apply_repairs=False to each portfolio."""
    p = MagicMock()
    p.id   = 1
    p.name = "Test"

    db = MagicMock()
    db.query.return_value.filter_by.return_value.order_by.return_value.all.return_value = [p]

    mock_result = RebuildResult(portfolio_id=1, portfolio_name="Test", success=True)

    with patch("services.portfolio_rebuilder.rebuild_portfolio",
               new=AsyncMock(return_value=mock_result)) as mock_rebuild:
        asyncio.run(rebuild_all_portfolios(
            db=db, workspace_id=1, apply_repairs=False
        ))

    mock_rebuild.assert_awaited_once()
    kw = mock_rebuild.call_args.kwargs
    assert kw.get("apply_repairs") is False


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP2 Step 2 — POSITION_CONVERSION replay fixtures (pure _apply_transaction)
#
# Written at Step 2, when _apply_transaction() had no POSITION_CONVERSION
# branch and every fixture below correctly failed (a no-op: predecessor
# untouched, no successor created). As of Step 4's accounting-application
# branch, these now exercise real production behavior and pass.
#
# Numbers for the full-share and generic fixtures are taken verbatim from
# BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md §11, acceptance criteria 3 and 4,
# so expected values are independently defined by the frozen planning corpus,
# not derived from any WP2 production helper.
# ══════════════════════════════════════════════════════════════════════════════

def _conversion_payload(
    *,
    predecessor_asset_id: int,
    predecessor_symbol: str,
    shares_surrendered: str,
    successor_asset_id: int,
    successor_symbol: str,
    successor_provider_symbol: str,
    shares_entitled: str,
    shares_received: str,
    conversion_ratio: str,
    basis_before: str,
    basis_allocated: str,
    basis_carried: str,
    cash_in_lieu: dict | None = None,
    transition_date: str = "2026-03-02",
) -> dict:
    return {
        "schema_version": 1,
        "predecessor": {
            "asset_id": predecessor_asset_id,
            "symbol": predecessor_symbol,
            "shares_surrendered": shares_surrendered,
        },
        "successor": {
            "asset_id": successor_asset_id,
            "symbol": successor_symbol,
            "provider_symbol": successor_provider_symbol,
            "shares_entitled": shares_entitled,
            "shares_received": shares_received,
        },
        "conversion_ratio": conversion_ratio,
        "basis": {
            "before": basis_before,
            "allocated_to_cash_in_lieu": basis_allocated,
            "carried_to_successor": basis_carried,
        },
        "cash_in_lieu": cash_in_lieu,
        "dates": {
            "legal_effective_date": transition_date,
            "valuation_transition_date": transition_date,
            "predecessor_last_price_date": transition_date,
            "successor_quote_epoch_start_date": transition_date,
        },
        "quote_binding": {
            "provider": "test-provider",
            "predecessor_provider_symbol": predecessor_symbol,
            "successor_provider_symbol": successor_provider_symbol,
        },
        "boundary_evidence": {
            "predecessor_reference_price": "1.00",
            "successor_reference_price": "1.00",
            "mechanical_nav_tolerance_pct": "1.0",
            "suspension_gap_annotation": "WP2 fixture — no suspension",
        },
        "evidence": {
            "reference": "WP2-FIXTURE",
            "source": "unit-test",
            "captured_at": "2026-03-02T00:00:00Z",
        },
    }


def _cil(fractional: str, gross: str, fees: str, taxes: str, net: str,
         basis_allocated: str, pnl: str) -> dict:
    return {
        "fractional_entitlement_shares": fractional,
        "gross_proceeds":                gross,
        "fees":                          fees,
        "taxes":                         taxes,
        "net_cash":                      net,
        "basis_allocated":               basis_allocated,
        "realized_pnl":                  pnl,
    }


def _conv_ctx(
    id: int,
    payload: dict,
    *,
    raw_symbol: str,
    canonical_symbol: str | None = None,
    asset_id: int | None = None,
    transaction_date: date = date(2026, 3, 2),
) -> CanonicalTransaction:
    parsed = parse_position_conversion_payload(payload)
    assert parsed.is_valid, parsed.errors   # fixture sanity check — not a WP2 assertion
    return CanonicalTransaction(
        id                   = id,
        transaction_type     = "POSITION_CONVERSION",
        raw_symbol           = raw_symbol,
        canonical_symbol     = canonical_symbol or raw_symbol,
        shares               = Decimal("0"),
        price_per_share      = Decimal("0"),
        total_amount         = Decimal("0"),
        fees                 = Decimal("0"),
        taxes                = Decimal("0"),
        transaction_date     = transaction_date,
        created_at           = None,
        sector               = None,
        notes                = None,
        qty_correction_delta = None,
        realized_pnl         = None,
        asset_id             = asset_id,
        position_conversion  = parsed,
    )


# ── 1. BANPU full-share conversion, no cash-in-lieu ────────────────────────────

def test_position_conversion_banpu_full_share_no_cash_in_lieu():
    """Spec §11 criterion 3: Qp=6700, R=0.38242, Qe=Qr=2562.214, B0=Bs=48709.00."""
    pred_sym = "PCONV1.BK"
    succ_sym = "SCONV1.BK"
    payload = _conversion_payload(
        predecessor_asset_id=101, predecessor_symbol=pred_sym, shares_surrendered="6700",
        successor_asset_id=102, successor_symbol=succ_sym, successor_provider_symbol=succ_sym,
        shares_entitled="2562.214", shares_received="2562.214", conversion_ratio="0.38242",
        basis_before="48709.00", basis_allocated="0", basis_carried="48709.00",
        cash_in_lieu=None,
    )

    s = _state(cash=10_000.0)
    s.cumulative_realized_pnl = Decimal("500.00")
    s.holdings[pred_sym] = _HoldingState(
        symbol=pred_sym, report_symbol=pred_sym,
        shares=Decimal("6700"), avg_cost=Decimal("48709.00") / Decimal("6700"),
        sector="Energy", price_symbol=pred_sym,
    )

    _apply_transaction(s, _conv_ctx(99, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym))

    assert pred_sym not in s.holdings
    assert succ_sym in s.holdings
    successor = s.holdings[succ_sym]
    assert successor.shares == Decimal("2562.214")
    assert successor.avg_cost == Decimal("48709.00") / Decimal("2562.214")
    assert s.cash_balance == Decimal("10000.0")             # unchanged — no cash-in-lieu
    assert s.cumulative_realized_pnl == Decimal("500.00")   # unchanged — no cash-in-lieu


# ── 2. Incident-independent generic conversion, with cash-in-lieu ──────────────

def test_position_conversion_generic_fixture_with_cash_in_lieu():
    """Spec §11 criterion 4: Qp=8, R=1.25, Qe=10, Qr=9.5, B0=240, Bf=12, Bs=228,
    Cg=15, F=1, T=0.5, Cn=13.5, RP=1.5 — arbitrary identities, no BANPU numbers."""
    pred_sym = "GPRED.BK"
    succ_sym = "GSUCC.BK"
    payload = _conversion_payload(
        predecessor_asset_id=201, predecessor_symbol=pred_sym, shares_surrendered="8",
        successor_asset_id=202, successor_symbol=succ_sym, successor_provider_symbol=succ_sym,
        shares_entitled="10", shares_received="9.5", conversion_ratio="1.25",
        basis_before="240", basis_allocated="12", basis_carried="228",
        cash_in_lieu=_cil(fractional="0.5", gross="15", fees="1", taxes="0.5",
                           net="13.5", basis_allocated="12", pnl="1.5"),
    )

    s = _state(cash=1_000.0)
    s.cumulative_realized_pnl = Decimal("0")
    s.holdings[pred_sym] = _HoldingState(
        symbol=pred_sym, report_symbol=pred_sym,
        shares=Decimal("8"), avg_cost=Decimal("240") / Decimal("8"),
        sector=None, price_symbol=pred_sym,
    )

    _apply_transaction(s, _conv_ctx(199, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym))

    assert pred_sym not in s.holdings
    assert succ_sym in s.holdings
    successor = s.holdings[succ_sym]
    assert successor.shares == Decimal("9.5")
    assert successor.avg_cost == Decimal("24")                    # 228 / 9.5
    assert s.cash_balance == Decimal("1000.0") + Decimal("13.5")           # +Cn only
    assert s.cumulative_realized_pnl == Decimal("0") + Decimal("1.5")      # +RP only


def test_rebuild_exposes_conversion_cash_in_lieu_realized_pnl():
    """The result surfaces the CIL P&L already admitted by conversion replay."""
    pred_sym = "RPRED.BK"
    succ_sym = "RSUCC.BK"
    payload = _conversion_payload(
        predecessor_asset_id=701, predecessor_symbol=pred_sym, shares_surrendered="8",
        successor_asset_id=702, successor_symbol=succ_sym, successor_provider_symbol=succ_sym,
        shares_entitled="10", shares_received="9.5", conversion_ratio="1.25",
        basis_before="240", basis_allocated="12", basis_carried="228",
        cash_in_lieu=_cil(fractional="0.5", gross="15", fees="1", taxes="0.5",
                           net="13.5", basis_allocated="12", pnl="1.5"),
    )
    raw_conversion = _make_raw_tx_mock(2, asset_id=701)
    raw_conversion.shares          = 9.5
    raw_conversion.price_per_share = 24.0
    raw_conversion.total_amount    = 228.0
    raw_conversion.fees            = 1.0
    raw_conversion.taxes           = 0.5
    portfolio = _make_portfolio_obj(cash=0.0)
    db = _make_rebuild_mock_db(
        portfolio, [_make_raw_tx_mock(1), raw_conversion],
    )
    ctxs = [
        _ctx(id=1, transaction_type="INITIAL_POSITION", raw_symbol=pred_sym,
             canonical_symbol=pred_sym, shares=8.0, price_per_share=30.0,
             total_amount=0.0),
        _conv_ctx(2, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym),
    ]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=False, skip_snapshots=True)

    assert r.success
    assert r.reconstructed_realized_pnl == pytest.approx(1.5)


def test_reconstructed_holding_basis_exposes_conversion_carried_basis():
    """The ordinary result map observes the successor state without replacing B0/Bs reconciliation."""
    pred_sym = "BASISPRED.BK"
    succ_sym = "BASISSUCC.BK"
    payload = _conversion_payload(
        predecessor_asset_id=801, predecessor_symbol=pred_sym, shares_surrendered="8",
        successor_asset_id=802, successor_symbol=succ_sym, successor_provider_symbol=succ_sym,
        shares_entitled="10", shares_received="9.5", conversion_ratio="1.25",
        basis_before="240", basis_allocated="12", basis_carried="228",
        cash_in_lieu=_cil(fractional="0.5", gross="15", fees="1", taxes="0.5",
                           net="13.5", basis_allocated="12", pnl="1.5"),
    )
    raw_conversion = _make_raw_tx_mock(2, asset_id=801)
    raw_conversion.shares          = 9.5
    raw_conversion.price_per_share = 24.0
    raw_conversion.total_amount    = 228.0
    raw_conversion.fees            = 1.0
    raw_conversion.taxes           = 0.5
    existing_successor = _mock_item(succ_sym, 9.5, 24.0)
    existing_successor.id       = 802
    existing_successor.asset_id = 802
    portfolio = _make_portfolio_obj(cash=0.0)
    db = _make_rebuild_mock_db(
        portfolio, [_make_raw_tx_mock(1), raw_conversion], items=[existing_successor],
    )
    ctxs = [
        _ctx(id=1, transaction_type="INITIAL_POSITION", raw_symbol=pred_sym,
             canonical_symbol=pred_sym, shares=8.0, price_per_share=30.0,
             total_amount=0.0),
        _conv_ctx(2, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym),
    ]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=_clean_report())):
        r = _run(db, apply_repairs=False, skip_snapshots=True)

    assert r.success
    assert r.reconstructed_holding_basis == {succ_sym: Decimal("228")}
    assert {row.field for row in r.reconciliation_report if row.identifier == succ_sym} == {
        "asset_id", "symbol", "shares", "avg_cost", "basis",
    }


# ── 3. No-cash-in-lieu must leave cash and realized P/L byte-equivalent ────────

def test_position_conversion_no_cash_in_lieu_preserves_cash_and_pnl_exactly():
    """Spec §7.3: 'No-cash-in-lieu conversions must leave cash and realized P/L
    byte-equivalent to their pre-conversion values.' Distinct nonzero starting
    values make this a non-vacuous assertion."""
    pred_sym = "IPRED.BK"
    succ_sym = "ISUCC.BK"
    payload = _conversion_payload(
        predecessor_asset_id=301, predecessor_symbol=pred_sym, shares_surrendered="6700",
        successor_asset_id=302, successor_symbol=succ_sym, successor_provider_symbol=succ_sym,
        shares_entitled="2562.214", shares_received="2562.214", conversion_ratio="0.38242",
        basis_before="48709.00", basis_allocated="0", basis_carried="48709.00",
        cash_in_lieu=None,
    )
    starting_cash = Decimal("73914.271")
    starting_pnl  = Decimal("-812.44")

    s = _state(cash=float(starting_cash))
    s.cash_balance = starting_cash          # exact Decimal, not the float round-trip
    s.cumulative_realized_pnl = starting_pnl
    s.holdings[pred_sym] = _HoldingState(
        symbol=pred_sym, report_symbol=pred_sym,
        shares=Decimal("6700"), avg_cost=Decimal("48709.00") / Decimal("6700"),
        sector=None, price_symbol=pred_sym,
    )

    _apply_transaction(s, _conv_ctx(299, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym))

    # The conversion must actually have applied (otherwise "unchanged" is vacuous)
    assert pred_sym not in s.holdings
    assert succ_sym in s.holdings
    assert s.holdings[succ_sym].shares == Decimal("2562.214")

    assert s.cash_balance == starting_cash
    assert s.cumulative_realized_pnl == starting_pnl


# ── 4. Existing-successor merge conserves combined basis exactly ──────────────

def test_position_conversion_existing_successor_merge_combines_basis_and_shares():
    """Spec §7.3 acceptance invariants:
    combined_basis = existing_basis + converted_basis
    combined_shares = existing_shares + Qr
    combined_avg_cost = combined_basis / combined_shares
    Clean-division numbers (800 / 20 = 40 exactly) so the test does not depend
    on any particular Decimal rounding/precision behavior."""
    pred_sym = "MPRED.BK"
    succ_sym = "MSUCC.BK"
    payload = _conversion_payload(
        predecessor_asset_id=401, predecessor_symbol=pred_sym, shares_surrendered="15",
        successor_asset_id=402, successor_symbol=succ_sym, successor_provider_symbol=succ_sym,
        shares_entitled="15", shares_received="15", conversion_ratio="1",
        basis_before="300", basis_allocated="0", basis_carried="300",
        cash_in_lieu=None,
    )

    s = _state(cash=0.0)
    s.holdings[pred_sym] = _HoldingState(
        symbol=pred_sym, report_symbol=pred_sym,
        shares=Decimal("15"), avg_cost=Decimal("300") / Decimal("15"),
        sector=None, price_symbol=pred_sym,
    )
    existing_shares  = Decimal("5")
    existing_avg     = Decimal("100")
    existing_basis   = existing_shares * existing_avg   # 500
    s.holdings[succ_sym] = _HoldingState(
        symbol=succ_sym, report_symbol=succ_sym,
        shares=existing_shares, avg_cost=existing_avg,
        sector=None, price_symbol=succ_sym,
    )

    _apply_transaction(s, _conv_ctx(399, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym))

    assert pred_sym not in s.holdings
    merged = s.holdings[succ_sym]
    converted_basis  = Decimal("300")   # Bs
    combined_basis   = existing_basis + converted_basis
    combined_shares  = existing_shares + Decimal("15")   # Qr
    assert merged.shares == combined_shares == Decimal("20")
    assert merged.avg_cost == combined_basis / combined_shares == Decimal("40")
    assert merged.shares * merged.avg_cost == combined_basis == Decimal("800")


# ── 5. Dual replay-site equality: Stage 1 final state vs Stage 2 terminal date ─

def test_position_conversion_stage1_final_state_equals_stage2_terminal_state():
    """Spec §7.4 / Implementation Sequence Step 4: 'Stage 1 final state and the
    terminal Stage 2 per-date state for the same terminal date must also be
    equal.' Runs the identical canonical transaction list through both existing
    application sites (a manual sequential _apply_transaction loop for Stage 1,
    and _replay_with_date_snapshots for Stage 2) and checks both against the
    same independently-computed expected values."""
    pred_sym = "DPRED.BK"
    succ_sym = "DSUCC.BK"
    payload = _conversion_payload(
        predecessor_asset_id=501, predecessor_symbol=pred_sym, shares_surrendered="6700",
        successor_asset_id=502, successor_symbol=succ_sym, successor_provider_symbol=succ_sym,
        shares_entitled="2562.214", shares_received="2562.214", conversion_ratio="0.38242",
        basis_before="48709.00", basis_allocated="0", basis_carried="48709.00",
        cash_in_lieu=None,
        transition_date="2026-03-02",
    )
    ctxs = [
        _ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
             shares=0.0, total_amount=100_000.0, transaction_date=date(2026, 1, 1)),
        _ctx(id=2, transaction_type="INITIAL_POSITION", raw_symbol=pred_sym, canonical_symbol=pred_sym,
             shares=6700.0, price_per_share=float(Decimal("48709.00") / Decimal("6700")),
             total_amount=0.0, fees=0.0, taxes=0.0, transaction_date=date(2026, 1, 2)),
        _conv_ctx(3, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym,
                  transaction_date=date(2026, 3, 2)),
    ]
    expected_cash    = Decimal("100000.0")
    expected_shares  = Decimal("2562.214")
    expected_avg     = Decimal("48709.00") / Decimal("2562.214")

    # Stage 1 — single sequential pass over the whole run
    stage1 = _state(cash=0.0)
    for ctx in ctxs:
        _apply_transaction(stage1, ctx)

    # Stage 2 — per-date snapshot replay, terminal date == last transaction date
    stage2_by_date = _replay_with_date_snapshots(ctxs, ["2026-03-02"])
    stage2 = stage2_by_date["2026-03-02"]

    for label, state in (("stage1", stage1), ("stage2", stage2)):
        assert pred_sym not in state.holdings, label
        assert succ_sym in state.holdings, label
        assert state.holdings[succ_sym].shares == expected_shares, label
        assert state.holdings[succ_sym].avg_cost == expected_avg, label
        assert state.cash_balance == expected_cash, label

    # Explicit cross-site equality (not just both matching the same expectation)
    assert stage1.holdings.keys() == stage2.holdings.keys()
    assert stage1.holdings[succ_sym].shares   == stage2.holdings[succ_sym].shares
    assert stage1.holdings[succ_sym].avg_cost == stage2.holdings[succ_sym].avg_cost
    assert stage1.cash_balance == stage2.cash_balance


# ── 6. Successor holding accepts a subsequent ordinary trade (Observation) ────

def test_position_conversion_successor_holding_accepts_subsequent_trade():
    """Recorded observation: once a conversion creates the successor holding,
    an ordinary later BUY on the successor's raw symbol must merge into that
    same holding (weighted-average cost) like any other repeat BUY — the
    successor is not a special holding after creation."""
    pred_sym = "TPRED.BK"
    succ_sym = "TSUCC.BK"
    payload = _conversion_payload(
        predecessor_asset_id=601, predecessor_symbol=pred_sym, shares_surrendered="15",
        successor_asset_id=602, successor_symbol=succ_sym, successor_provider_symbol=succ_sym,
        shares_entitled="15", shares_received="15", conversion_ratio="1",
        basis_before="300", basis_allocated="0", basis_carried="300",
        cash_in_lieu=None,
    )

    s = _state(cash=10_000.0)
    s.holdings[pred_sym] = _HoldingState(
        symbol=pred_sym, report_symbol=pred_sym,
        shares=Decimal("15"), avg_cost=Decimal("300") / Decimal("15"),
        sector=None, price_symbol=pred_sym,
    )
    _apply_transaction(s, _conv_ctx(699, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym,
                                     transaction_date=date(2026, 3, 2)))

    # Subsequent ordinary BUY of 5 more shares @ 50/share, after the conversion
    _apply_transaction(s, _ctx(
        id=700, transaction_type="BUY", raw_symbol=succ_sym, canonical_symbol=succ_sym,
        shares=5.0, total_amount=250.0, transaction_date=date(2026, 3, 5),
    ))

    assert succ_sym in s.holdings
    merged = s.holdings[succ_sym]
    expected_shares = Decimal("15") + Decimal("5")
    expected_basis  = Decimal("300") + Decimal("250")
    assert merged.shares == expected_shares
    assert merged.avg_cost == expected_basis / expected_shares


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP2 Step 3 — preflight and identity resolution (pure, no DB)
# ══════════════════════════════════════════════════════════════════════════════

def _raw_row(id: int, asset_id: int | None):
    """Projection-valid stand-in for raw Transaction preflight."""
    return SimpleNamespace(
        id=id,
        asset_id=asset_id,
        shares=10.0,
        price_per_share=10.0,
        total_amount=100.0,
        fees=0.0,
        taxes=0.0,
    )


def test_position_conversion_duplicate_key_fails_via_preflight():
    """The WP1 partial unique index on (portfolio_id, asset_id, transaction_date)
    already prevents two persisted POSITION_CONVERSION rows from sharing a
    predecessor asset ID and date, so this condition cannot be constructed
    against a schema-compliant committed database — it is exercised directly
    against _preflight_position_conversions(), the defensive, schema-
    independent equivalent (Implementation Specification §7.1 item 5)."""
    pred_sym = "DKPRED.BK"
    payload = _conversion_payload(
        predecessor_asset_id=801, predecessor_symbol=pred_sym, shares_surrendered="10",
        successor_asset_id=802, successor_symbol="DKSUCC.BK", successor_provider_symbol="DKSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    pred  = _ctx(id=1, transaction_type="INITIAL_POSITION", raw_symbol=pred_sym, canonical_symbol=pred_sym,
                 shares=10.0, price_per_share=10.0, total_amount=0.0, transaction_date=date(2026, 1, 1))
    conv1 = _conv_ctx(2, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym, asset_id=801,
                       transaction_date=date(2026, 3, 2))
    conv2 = _conv_ctx(3, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym, asset_id=801,
                       transaction_date=date(2026, 3, 2))
    raw_txs = [_raw_row(1, None), _raw_row(2, 801), _raw_row(3, 801)]

    with pytest.raises(PositionConversionReplayError) as exc_info:
        _preflight_position_conversions(raw_txs, [pred, conv1, conv2])
    assert exc_info.value.reason == "POSITION_CONVERSION_DUPLICATE"
    assert exc_info.value.transaction_id in (2, 3)   # both occurrences of the key are invalid


def test_position_conversion_stage_replay_invocations_have_independent_duplicate_tracking():
    """Each _replay_with_date_snapshots() invocation must own a fresh
    conversion-key duplicate-tracking set, never reused across calls — the
    same requirement that keeps Stage 1's own sequential loop from treating
    Stage 2's application (or vice versa) as a duplicate. A classic Python
    mutable-default-argument bug (a set created once, at function-definition
    time, and reused across calls) would make the SECOND identical call below
    raise DUPLICATE; this test fails loudly (via an unhandled exception) if
    that ever regresses."""
    pred_sym = "SIPRED.BK"
    payload = _conversion_payload(
        predecessor_asset_id=901, predecessor_symbol=pred_sym, shares_surrendered="15",
        successor_asset_id=902, successor_symbol="SISUCC.BK", successor_provider_symbol="SISUCC.BK",
        shares_entitled="15", shares_received="15", conversion_ratio="1",
        basis_before="300", basis_allocated="0", basis_carried="300",
    )
    ctxs = [
        _ctx(id=1, transaction_type="INITIAL_POSITION", raw_symbol=pred_sym, canonical_symbol=pred_sym,
             shares=15.0, price_per_share=20.0, total_amount=0.0, transaction_date=date(2026, 1, 1)),
        _conv_ctx(2, payload, raw_symbol=pred_sym, canonical_symbol=pred_sym,
                  transaction_date=date(2026, 3, 2)),
    ]

    # "Stage 1" — one full sequential pass with its own fresh set.
    stage1 = _state(cash=0.0)
    stage1_seen: set = set()
    for ctx in ctxs:
        _apply_transaction(stage1, ctx, conversion_seen=stage1_seen)

    # "Stage 2" — two independent invocations of the same function over the
    # identical input. Neither may see the other's (or Stage 1's) tracking.
    _replay_with_date_snapshots(ctxs, ["2026-03-02"])
    _replay_with_date_snapshots(ctxs, ["2026-03-02"])


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP2 Step 5 — Stage 5 blocking policy for conversion findings
#
# services/ledger_validator.py does not implement POSITION_CONVERSION findings
# yet (Step 6) — a real end-to-end run can never produce one today. These
# tests exercise the Stage 5 gate directly by injecting a constructed
# LedgerValidationReport, the same established idiom test #42
# (test_rebuild_confidence_derived_from_effective_validator_report) already
# uses for CASH_MISMATCH. Uses skip_snapshots=True, dry_run=False against the
# MagicMock DB harness so committed can be observed (dry_run=True, this
# file's _run() default, never reaches Stage 8 at all).
# ══════════════════════════════════════════════════════════════════════════════

def _report_with_finding(check_id: str, severity, portfolio_id: int = 1) -> LedgerValidationReport:
    finding = LedgerFinding(
        check_id=check_id, severity=severity,
        portfolio_id=portfolio_id, transaction_ids=[], symbol=None, normalized_symbol=None,
        title="test", explanation="", recommendation="",
    )
    return LedgerValidationReport(
        portfolio_id=portfolio_id, portfolio_name="Test",
        transactions_inspected=1, findings=[finding],
    )


def test_rebuild_conversion_critical_finding_blocks_stage5():
    """The pre-existing generic 'any CRITICAL aborts' rule already covers
    conversion CRITICAL findings by check_id namespace alone — no new code
    needed for this half of the frozen policy, but the explicit fixture is
    required Step 5 coverage."""
    from services.ledger_validator import FindingSeverity
    portfolio = _make_portfolio_obj(cash=0.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])
    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=50_000.0)]
    report = _report_with_finding("POSITION_CONVERSION_PAYLOAD_INVALID", FindingSeverity.CRITICAL)

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=report)):
        r = _run(db, apply_repairs=True, dry_run=False)

    assert r.ledger_criticals == 1
    assert r.aborted is True
    assert r.committed is False


def test_rebuild_conversion_same_day_conflict_error_blocks_stage5():
    """POSITION_CONVERSION_SAME_DAY_CONFLICT has a fixed ERROR severity
    (Implementation Specification §9.1) but must still block commit — the one
    Stage 5-specific rule this step adds. Distinct evidence path from Step
    3's rebuilder preflight (which fires earlier, before Stage 5 ever runs,
    for the same underlying business rule via a different mechanism); this
    test proves the Stage 5 gate itself, independent of preflight."""
    from services.ledger_validator import FindingSeverity
    portfolio = _make_portfolio_obj(cash=0.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])
    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=50_000.0)]
    report = _report_with_finding("POSITION_CONVERSION_SAME_DAY_CONFLICT", FindingSeverity.ERROR)

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=report)):
        r = _run(db, apply_repairs=True, dry_run=False)

    assert r.success is True
    assert r.ledger_criticals == 0        # ERROR, not CRITICAL
    assert r.aborted is True              # still blocks
    assert r.committed is False


def test_rebuild_unrelated_error_finding_does_not_block_stage5():
    """An ordinary ERROR finding unrelated to conversions must keep its
    existing (non-blocking) policy — the special case is scoped exactly to
    POSITION_CONVERSION_SAME_DAY_CONFLICT, nothing broader."""
    from services.ledger_validator import FindingSeverity
    portfolio = _make_portfolio_obj(cash=0.0)
    db        = _make_rebuild_mock_db(portfolio, [_make_raw_tx_mock(1)])
    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=50_000.0)]
    report = _report_with_finding("CASH_MISMATCH", FindingSeverity.ERROR)

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder.load_active_repairs", return_value=[]), \
         patch("services.portfolio_rebuilder.validate_portfolio_ledger",
               new=AsyncMock(return_value=report)):
        r = _run(db, apply_repairs=True, dry_run=False)

    assert r.ledger_criticals == 0
    assert r.aborted is False
    assert r.committed is True


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP5-C3/C4 — POSITION_CONVERSION_REBUILD_BOUNDARY
#
# Relocated here per the Independent Implementation Review correction
# (docs/implementation/BANPU_WP5_INDEPENDENT_IMPLEMENTATION_REVIEW.md §6/§20
# item 3): Authorization Record §4.2 names this file, not
# test_position_conversion_replay.py, as the authorized rebuild-boundary test
# surface. WP5-A4-A8 (WP5_WORK_PACKAGE_PLAN.md §8, §9, §15) plus the
# rebuild-boundary half of WP5-A31.
#
# Uses this file's own MagicMock DB harness — _make_rebuild_mock_db (extended
# above with an existing_snaps param), _conversion_payload/_conv_ctx — not a
# real database, consistent with every other rebuild_portfolio() test here.
# _build_price_matrix is explicitly mocked and its call count asserted in
# every test: zero calls for the two refusal cases proves the guard fires
# "before any provider fetch" (review correction item 6), not merely inferred
# from exception ordering.
# ══════════════════════════════════════════════════════════════════════════════

def _wp5_conversion_ctxs(transition_date: date = date(2026, 3, 2)) -> list[CanonicalTransaction]:
    payload = _conversion_payload(
        predecessor_asset_id=5001, predecessor_symbol="WP5PRED.BK", shares_surrendered="100",
        successor_asset_id=5002, successor_symbol="WP5SUCC.BK", successor_provider_symbol="WP5SUCC.BK",
        shares_entitled="50", shares_received="50", conversion_ratio="0.5",
        basis_before="10000", basis_allocated="0", basis_carried="10000",
        cash_in_lieu=None,
        transition_date=transition_date.isoformat(),
    )
    return [
        _ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
             shares=0.0, total_amount=10_000.0, transaction_date=date(2026, 1, 1)),
        _ctx(id=2, transaction_type="INITIAL_POSITION", raw_symbol="WP5PRED.BK",
             canonical_symbol="WP5PRED.BK", shares=100.0, price_per_share=100.0,
             total_amount=0.0, transaction_date=date(2026, 1, 2)),
        _conv_ctx(3, payload, raw_symbol="WP5PRED.BK", canonical_symbol="WP5PRED.BK",
                  asset_id=5001, transaction_date=transition_date),
    ]


def _make_snap_row(snapshot_date: str, **kwargs) -> PortfolioSnapshot:
    """Real (unpersisted, no session) ORM instance — a before/after full-
    column comparison against it is a genuine structural proof (WP5-A8), not
    a hand-picked field list."""
    return PortfolioSnapshot(
        workspace_id=1, portfolio_id=1, snapshot_date=snapshot_date,
        total_value=kwargs.get("total_value", 0.0),
        cash_balance=kwargs.get("cash_balance", 0.0),
        total_invested=kwargs.get("total_invested", 0.0),
        unrealized_pnl=kwargs.get("unrealized_pnl"),
        unrealized_pnl_pct=kwargs.get("unrealized_pnl_pct"),
        holdings_json=kwargs.get("holdings_json"),
        holdings_count=kwargs.get("holdings_count"),
        daily_return_pct=kwargs.get("daily_return_pct"),
        investment_return_pct=kwargs.get("investment_return_pct"),
    )


def _make_wp5_raw_conversion_tx_mock(tx_id: int = 3) -> MagicMock:
    """Raw row satisfying _preflight_position_conversions' Pass-1 projection
    checks for _wp5_conversion_ctxs()'s fixture (shares_received=50,
    basis_carried_to_successor=10000, no cash_in_lieu)."""
    t = _make_raw_tx_mock(tx_id, asset_id=5001)
    t.shares          = 50.0
    t.price_per_share = 200.0   # 10000 / 50
    t.total_amount    = 10_000.0
    t.fees            = 0.0
    t.taxes           = 0.0
    return t


def _make_wp5_boundary_db(existing_snaps: list[PortfolioSnapshot] | None = None) -> MagicMock:
    return _make_rebuild_mock_db(
        _make_portfolio_obj(cash=0.0),
        [_make_raw_tx_mock(1), _make_raw_tx_mock(2), _make_wp5_raw_conversion_tx_mock(3)],
        existing_snaps=existing_snaps,
    )


def _run_boundary(db, *, from_date, clean_validator: bool = True):
    ctm = patch(
        "services.portfolio_rebuilder.validate_portfolio_ledger",
        new=AsyncMock(return_value=_clean_report()),
    )
    with ctm:
        return asyncio.run(rebuild_portfolio(
            db=db, portfolio_id=1, workspace_id=1, from_date=from_date,
            skip_snapshots=False, dry_run=False, apply_repairs=False,
        ))


# ── WP5-A4 — refusal, from_date=None ───────────────────────────────────────────

def test_wp5_rebuild_boundary_refuses_when_from_date_none():
    db   = _make_wp5_boundary_db()
    ctxs = _wp5_conversion_ctxs()

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder._build_price_matrix",
               new=AsyncMock(return_value={})) as mock_fetch:
        r = _run_boundary(db, from_date=None)

    assert r.success is False
    assert "POSITION_CONVERSION_REBUILD_BOUNDARY" in r.error
    mock_fetch.assert_not_called()               # zero provider fetch before refusal
    db.add.assert_not_called()                   # zero write


# ── WP5-A5 — refusal, from_date before transition ──────────────────────────────

def test_wp5_rebuild_boundary_refuses_when_from_date_before_transition():
    db   = _make_wp5_boundary_db()
    ctxs = _wp5_conversion_ctxs()

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder._build_price_matrix",
               new=AsyncMock(return_value={})) as mock_fetch:
        r = _run_boundary(db, from_date="2026-02-01")

    assert r.success is False
    assert "POSITION_CONVERSION_REBUILD_BOUNDARY" in r.error
    mock_fetch.assert_not_called()
    db.add.assert_not_called()


# ── WP5-A6 — bounded rebuild proceeds when from_date admissible ────────────────

def test_wp5_rebuild_boundary_proceeds_when_from_date_admissible():
    at_boundary = _make_snap_row("2026-03-02")
    db          = _make_wp5_boundary_db(existing_snaps=[at_boundary])
    ctxs        = _wp5_conversion_ctxs()

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder._build_price_matrix",
               new=AsyncMock(return_value={})) as mock_fetch:
        r = _run_boundary(db, from_date="2026-03-02")

    assert r.error is None or "POSITION_CONVERSION_REBUILD_BOUNDARY" not in r.error
    assert r.success is True
    mock_fetch.assert_called_once()               # normal Stage 2 behavior, unaffected


# ── WP5-A7 — no-conversion regression: guard never fires without a conversion ──

def test_wp5_rebuild_boundary_no_conversion_unaffected():
    db   = _make_wp5_boundary_db()
    ctxs = [_ctx(id=1, transaction_type="DEPOSIT", raw_symbol=None, canonical_symbol=None,
                 shares=0.0, total_amount=10_000.0)]

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder._build_price_matrix",
               new=AsyncMock(return_value={})):
        r = _run_boundary(db, from_date=None)

    assert r.error is None or "POSITION_CONVERSION_REBUILD_BOUNDARY" not in r.error
    assert r.success is True


# ── WP5-A8 — byte-exact pre-boundary preservation ──────────────────────────────

def test_wp5_rebuild_boundary_preserves_pre_boundary_snapshot_byte_exact():
    """A pre-boundary row must be neither mutated in place nor ever the
    target of a db.add() insert once a bounded (admissible from_date)
    rebuild runs. The mock DB's .first() lookup is keyed by snapshot_date
    (see _make_rebuild_mock_db), so the pre-boundary row is provably never
    even queried-for-update: Stage 8 only iterates snapshot_days, which by
    construction (Stage 2's rebuild_dates filter) never includes a
    pre-boundary date."""
    pre_boundary = _make_snap_row(
        "2026-02-01", total_value=12_345.67, cash_balance=999.0, total_invested=11_000.0,
        unrealized_pnl=345.67, unrealized_pnl_pct=3.1,
        holdings_json='[{"symbol": "WP5PRED.BK", "shares": 100, "asset_id": 5001}]',
        holdings_count=1, daily_return_pct=0.5, investment_return_pct=0.5,
    )
    at_boundary = _make_snap_row("2026-03-02")
    before = {c.name: getattr(pre_boundary, c.name) for c in PortfolioSnapshot.__table__.columns}

    db   = _make_wp5_boundary_db(existing_snaps=[pre_boundary, at_boundary])
    ctxs = _wp5_conversion_ctxs()

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder._build_price_matrix",
               new=AsyncMock(return_value={})):
        r = _run_boundary(db, from_date="2026-03-02")

    assert r.error is None or "POSITION_CONVERSION_REBUILD_BOUNDARY" not in r.error
    assert r.success is True

    after = {c.name: getattr(pre_boundary, c.name) for c in PortfolioSnapshot.__table__.columns}
    assert after == before                        # no in-place mutation, zero diffs

    for call in db.add.call_args_list:             # never (re)inserted either
        written = call.args[0] if call.args else None
        if isinstance(written, PortfolioSnapshot):
            assert written.snapshot_date != "2026-02-01"


# ── WP5-A31 (rebuild-boundary half) — independent of D7 mechanical continuity ──
#
# The D7 half of this row (manage.py) lives in test_verify_snapshots.py. This
# half proves the converse direction: an admissible from_date lets a bounded
# rebuild proceed even though the same conversion's boundary evidence would
# fail D7's D2-D6 comparison outright (P_pre=1.00, P_succ=1.00, R=0.5 in the
# payload's default boundary_evidence -> metric_pct=50% against a 1.0%
# default tolerance) — rebuild_portfolio() never evaluates that formula.

def test_wp5_a31_rebuild_boundary_proceeds_regardless_of_d7_outcome():
    at_boundary = _make_snap_row("2026-03-02")
    db          = _make_wp5_boundary_db(existing_snaps=[at_boundary])
    ctxs        = _wp5_conversion_ctxs()   # same fixture D7 would fail: 50% vs 1.0% tolerance

    with patch("services.portfolio_rebuilder.canonicalize_transactions", return_value=ctxs), \
         patch("services.portfolio_rebuilder._build_price_matrix",
               new=AsyncMock(return_value={})):
        r = _run_boundary(db, from_date="2026-03-02")

    assert r.success is True
    assert r.error is None or "POSITION_CONVERSION_REBUILD_BOUNDARY" not in r.error


def test_wp5_a31_no_manage_module_reference_in_rebuilder():
    """Supplementary only (the primary A31 proof is the behavioral test above
    plus its D7-side counterpart in test_verify_snapshots.py): portfolio_
    rebuilder.py never imports manage.py, so there is no possible call path
    from the rebuild-boundary guard into D7."""
    import services.portfolio_rebuilder as mod
    assert "manage" not in mod.__dict__
