"""Tests for services/evaluation/execution_analyzer.py — AI Evaluation M2.

Pure-function module — no DB, no AI. Coverage:

Unavailable / null-handling
  1. Zero linked transactions -> status="unavailable", score=None, every
     planned symbol carries note="no_linked_transaction"
  2. A plan with zero planned trades and zero transactions -> completeness 100
Matching and deltas
  3. Fully matched plan, exact fill vs. plan -> status="ok", high score
  4. Timing delta sign and magnitude for a BUY filled above the recommended price
  5. Size delta when executed amount is double the planned amount
Partial completeness
  6. One of two planned trades unmatched -> status="partial",
     completeness_pct == 50, PARTIAL note present on the unmatched symbol
Funding fidelity
  7. A planned FUNDING_SOURCE trade with no linked transaction drags
     funding_fidelity_pct down
  8. No planned funding-source trades at all -> funding_fidelity_pct is None
     (not applicable), never a fabricated 100 or 0
"""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.evaluation.execution_analyzer import compute_execution_analysis  # noqa: E402


def _alloc(symbol: str, action: str, change_pct: float, estimated_amount: float,
           current_weight: float = 10.0, sector: str = "Consumer") -> dict:
    return {
        "symbol": symbol, "action": action,
        "allocation_change_percent": change_pct, "current_weight": current_weight,
        "estimated_amount": estimated_amount, "sector": sector,
    }


def _tx(
    symbol: str, shares: float, price_per_share: float, total_amount: float,
    id: int = 1, transaction_date: str = "2026-01-01T00:00:00Z",
    transaction_type: str = "BUY",
) -> dict:
    return {
        "symbol": symbol, "shares": shares, "price_per_share": price_per_share,
        "total_amount": total_amount, "id": id, "transaction_date": transaction_date,
        "transaction_type": transaction_type,
    }


# ── Unavailable / null-handling ─────────────────────────────────────────────

def test_no_linked_transactions_is_unavailable_not_fabricated():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=[],
    )
    assert result["status"] == "unavailable"
    assert result["score"] is None
    assert result["symbols"]["CENTEL"]["note"] == "no_linked_transaction"


def test_empty_plan_and_empty_transactions_completeness_is_full():
    result = compute_execution_analysis(
        [], cash_available=0.0, violations=[], recommendation_prices={}, linked_transactions=[],
    )
    assert result["completeness_pct"] == 100.0


# ── Matching and deltas ──────────────────────────────────────────────────────

def test_fully_matched_exact_fill_scores_high():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["status"] in ("ok", "partial")
    assert result["symbols"]["CENTEL"]["timing_delta_pct"] == 0.0
    assert result["symbols"]["CENTEL"]["size_delta_pct"] == 0.0
    assert result["completeness_pct"] == 100.0
    assert result["score"] > 90.0


def test_timing_delta_positive_when_buy_fills_above_recommended_price():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [_tx("CENTEL", shares=250, price_per_share=120.0, total_amount=30_000)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    # (120 - 100) / 100 * 100 = +20%
    assert result["symbols"]["CENTEL"]["timing_delta_pct"] == 20.0


def test_size_delta_when_executed_is_double_planned():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [_tx("CENTEL", shares=600, price_per_share=100.0, total_amount=60_000)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["symbols"]["CENTEL"]["size_delta_pct"] == 100.0


# ── Partial completeness ─────────────────────────────────────────────────────

def test_one_of_two_unmatched_is_partial_with_50pct_completeness():
    allocations = [
        _alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0),
        _alloc("ADVANC", "BUY", 2.0, 20_000, current_weight=0.0),
    ]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0, "ADVANC": 200.0}, linked_transactions=txs,
    )
    assert result["status"] == "partial"
    assert result["completeness_pct"] == 50.0
    assert result["symbols"]["ADVANC"]["note"] == "no_linked_transaction"
    assert result["symbols"]["ADVANC"]["executed_amount"] is None


# ── Funding fidelity ──────────────────────────────────────────────────────────

def test_unmatched_funding_source_drags_fidelity_down():
    """Gap=30k, XYZ REDUCE(30k) is the funding source; if the human never
    actually sold XYZ, funding_fidelity_pct must reflect that miss."""
    allocations = [
        _alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0),
        _alloc("XYZ", "REDUCE", -3.0, 30_000),
    ]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["funding_fidelity_pct"] == 0.0
    assert result["status"] == "partial"


def test_no_funding_source_planned_fidelity_is_not_applicable():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000)]
    result = compute_execution_analysis(
        allocations, cash_available=100_000.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["funding_fidelity_pct"] is None


# ── Linked transaction provenance (Decision Continuity UX Slice 1) ──────────
# Additive only — id/transaction_date must reach the per-symbol result
# without perturbing any score/status/completeness/funding-fidelity math
# already proven above.

def test_matched_symbol_carries_transaction_provenance():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000, id=42, transaction_date="2026-03-01T00:00:00Z")]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["symbols"]["CENTEL"]["transactions"] == [{"id": 42, "transaction_date": "2026-03-01T00:00:00Z"}]
    # Existing scoring is unaffected by the new field.
    assert result["symbols"]["CENTEL"]["timing_delta_pct"] == 0.0
    assert result["symbols"]["CENTEL"]["size_delta_pct"] == 0.0
    assert result["completeness_pct"] == 100.0
    assert result["score"] > 90.0


def test_multiple_fills_for_one_symbol_all_represented():
    """Two partial fills against one symbol must both be listed — never
    arbitrarily reduced to a single reference."""
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [
        _tx("CENTEL", shares=150, price_per_share=100.0, total_amount=15_000, id=1, transaction_date="2026-03-01T00:00:00Z"),
        _tx("CENTEL", shares=150, price_per_share=100.0, total_amount=15_000, id=2, transaction_date="2026-03-02T00:00:00Z"),
    ]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    ids = {t["id"] for t in result["symbols"]["CENTEL"]["transactions"]}
    assert ids == {1, 2}
    # Aggregation math (executed_amount, deltas) is untouched by the addition.
    assert result["symbols"]["CENTEL"]["executed_amount"] == 30_000.0


def test_unmatched_symbol_has_empty_transactions_list():
    allocations = [
        _alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0),
        _alloc("ADVANC", "BUY", 2.0, 20_000, current_weight=0.0),
    ]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0, "ADVANC": 200.0}, linked_transactions=txs,
    )
    assert result["symbols"]["ADVANC"]["transactions"] == []


def test_zero_linked_transactions_gives_empty_transactions_lists():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=[],
    )
    assert result["symbols"]["CENTEL"]["transactions"] == []


# ── Canonical completion fields (Execution Completion Polish, Slice 3) ──────
# matched_count / total_planned / is_complete are additive derived facts,
# never a persisted status — see execution_analyzer.py module docstring.

def test_zero_actionable_trades_is_complete_by_definition():
    """No plan, no transactions -> nothing to record -> complete."""
    result = compute_execution_analysis(
        [], cash_available=0.0, violations=[], recommendation_prices={}, linked_transactions=[],
    )
    assert result["matched_count"] == 0
    assert result["total_planned"] == 0
    assert result["is_complete"] is True


def test_actionable_trades_with_zero_matches_is_not_complete():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=[],
    )
    assert result["matched_count"] == 0
    assert result["total_planned"] == 1
    assert result["is_complete"] is False


def test_partial_matches_is_not_complete():
    allocations = [
        _alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0),
        _alloc("ADVANC", "BUY", 2.0, 20_000, current_weight=0.0),
    ]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0, "ADVANC": 200.0}, linked_transactions=txs,
    )
    assert result["matched_count"] == 1
    assert result["total_planned"] == 2
    assert result["is_complete"] is False


def test_all_actionable_trades_matched_is_complete():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["matched_count"] == 1
    assert result["total_planned"] == 1
    assert result["is_complete"] is True


def test_fully_matched_with_no_funding_source_is_complete_regardless_of_status():
    """The defect this slice fixes: a fully-matched decision with no planned
    funding-source trade forces status="partial" (funding_fidelity_pct is
    unmeasurable) even though completion is unambiguous. is_complete must
    not inherit that ambiguity."""
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000)]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["status"] == "partial"  # grading ambiguity persists (by design)
    assert result["is_complete"] is True   # completion is unambiguous


# ── Correct-side transaction matching ───────────────────────────────────────

def test_planned_buy_matches_linked_buy():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000, transaction_type="BUY")]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["matched_count"] == 1
    assert result["symbols"]["CENTEL"]["note"] is None


def test_planned_buy_does_not_match_linked_sell():
    allocations = [_alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000, transaction_type="SELL")]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["matched_count"] == 0
    assert result["symbols"]["CENTEL"]["note"] == "no_linked_transaction"
    assert result["symbols"]["CENTEL"]["executed_amount"] is None


def test_planned_sell_matches_linked_sell():
    allocations = [_alloc("CENTEL", "SELL", -3.0, 30_000, current_weight=3.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000, transaction_type="SELL")]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["matched_count"] == 1
    assert result["symbols"]["CENTEL"]["note"] is None


def test_planned_reduce_matches_linked_sell():
    allocations = [
        _alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0),
        _alloc("XYZ", "REDUCE", -3.0, 30_000),
    ]
    txs = [
        _tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000, transaction_type="BUY", id=1),
        _tx("XYZ", shares=300, price_per_share=100.0, total_amount=30_000, transaction_type="SELL", id=2),
    ]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0, "XYZ": 100.0}, linked_transactions=txs,
    )
    assert result["symbols"]["XYZ"]["note"] is None
    assert result["funding_fidelity_pct"] == 100.0


def test_wrong_side_transaction_does_not_inflate_completeness():
    """A BUY linked against a planned REDUCE (funding-source) trade must not
    count as a match, in either completeness_pct or funding_fidelity_pct."""
    allocations = [
        _alloc("CENTEL", "BUY", 3.0, 30_000, current_weight=0.0),
        _alloc("XYZ", "REDUCE", -3.0, 30_000),
    ]
    txs = [
        _tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000, transaction_type="BUY", id=1),
        _tx("XYZ", shares=300, price_per_share=100.0, total_amount=30_000, transaction_type="BUY", id=2),
    ]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0, "XYZ": 100.0}, linked_transactions=txs,
    )
    assert result["matched_count"] == 1
    assert result["completeness_pct"] == 50.0
    assert result["funding_fidelity_pct"] == 0.0
    assert result["symbols"]["XYZ"]["note"] == "no_linked_transaction"
    assert result["symbols"]["XYZ"]["executed_amount"] is None


# ── ACCUMULATE side matching (Correction pass — review finding 1) ──────────
# ACCUMULATE is a buy-side action (optimizer_action_summary.build_action_summary
# groups action in ("BUY", "ACCUMULATE") into the same accumulate/new_position
# buckets) — it must require a BUY fill, exactly like a plain "BUY" row, and
# must never be satisfiable by a SELL.

def test_planned_accumulate_matches_linked_buy():
    allocations = [_alloc("CENTEL", "ACCUMULATE", 3.0, 30_000, current_weight=5.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000, transaction_type="BUY")]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["matched_count"] == 1
    assert result["total_planned"] == 1
    assert result["is_complete"] is True
    assert result["symbols"]["CENTEL"]["note"] is None
    assert result["symbols"]["CENTEL"]["executed_amount"] == 30_000.0
    assert result["completeness_pct"] == 100.0


def test_planned_accumulate_does_not_match_linked_sell():
    allocations = [_alloc("CENTEL", "ACCUMULATE", 3.0, 30_000, current_weight=5.0)]
    txs = [_tx("CENTEL", shares=300, price_per_share=100.0, total_amount=30_000, transaction_type="SELL")]
    result = compute_execution_analysis(
        allocations, cash_available=0.0, violations=[],
        recommendation_prices={"CENTEL": 100.0}, linked_transactions=txs,
    )
    assert result["matched_count"] == 0
    assert result["total_planned"] == 1
    assert result["is_complete"] is False
    assert result["symbols"]["CENTEL"]["note"] == "no_linked_transaction"
    assert result["symbols"]["CENTEL"]["executed_amount"] is None
    assert result["completeness_pct"] == 0.0
