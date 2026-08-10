"""Portfolio Reconstruction Engine.

The Transaction table is the single Source of Truth.
Everything else is derived from it.

Reconstruction pipeline
-----------------------
  Stage 1 — Transaction replay
              → Portfolio.cash_balance
              → PortfolioItem (shares, avg_cost)
              → Cost basis
              → Cumulative realized P&L

  Stage 2 — Historical snapshot generation
              → Portfolio state replayed as-of each snapshot date
              → Historical closing prices fetched per symbol
              → holdings_json, equity_value, total_value, sector allocation

  Stage 3 — Return metric recalculation
              → investment_return_pct, daily_return_pct
              → net_external_cash_flow, imported_asset_value
              → period_realized_pnl, period_dividend_income, period_fees_paid

  Stage 4 — Validation / reconciliation report
              → MATCH / DIFFERENT / MISSING / EXTRA per field

  Stage 5 — Ledger validation gate
              → CRITICAL finding → abort; commit is blocked
              → Multi-dimensional confidence report computed (ConfidenceReport)

  Stage 6 — Execution plan generation (read-only)
              → Lists every intended DB change before any write occurs
              → Deterministic: same replay → same plan

  Stage 7 — Pre-commit backup (optional)
              → Existing rows exported to JSON before any writes
              → Backup failure aborts the commit

  Stage 8 — Atomic commit (single DB transaction; rollback on any failure)

  Stage 9 — Idempotency (upsert pattern; running twice = same state)

Key design decisions
---------------------
* transaction_date is used for portfolio-state ordering (what was held on a
  given day). created_at is intentionally NOT used here — it is the live
  engine's workaround for backdated imports and does not apply to a full
  rebuild from the ledger.

* Price coverage < 90% → snapshot is generated but flagged; it is written
  with price_missing=True for affected holdings and is not blocked (the
  build still proceeds; the caller may choose to skip writing it).

* allow_swap is user-configurable metadata, not derivable from transactions.
  It is preserved from the existing PortfolioItem when rebuilding.

* QUANTITY_CORRECTION stores abs(delta) in tx.shares; the signed delta is
  recovered from tx.notes ("Quantity correction: +5.0 shares").

Public API
----------
  rebuild_portfolio(db, portfolio_id, workspace_id, ...) -> RebuildResult
  rebuild_all_portfolios(db, workspace_id, ...) -> list[RebuildResult]
  ConfidenceReport         — multi-dimensional quality assessment (0-100 per dimension)
  ReconstructionPlan       — immutable execution plan with all intended DB changes
  PlanOperation            — one intended DB change (table/operation/field/values/reason)
  PlanSummary              — aggregate counts from a ReconstructionPlan
"""
from __future__ import annotations

import asyncio
import bisect
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Any, Callable, Optional

import pandas as pd
from sqlalchemy.orm import Session

from models.database import LedgerRepair, Portfolio, PortfolioItem, PortfolioSnapshot, Transaction
from services import capability_lookup_service
from services.capability_lookup_service import UnresolvedCapability
from services.capability_safety import grants_dividend_flow, permits_quantity_valuation
from services.data_fetcher import fetch_history
from services.ledger_repair import apply_repair_overlay, load_active_repairs
from services.ledger_validator import FindingSeverity, LedgerValidationReport, validate_portfolio_ledger
from services.portfolio_metrics import compute_period_metrics
from services.replay_key import replay_key
from services.runtime_consultation import (
    RuntimeConsultationLog,
    RuntimeFindingCategory,
    RuntimeValidationFinding,
)
from services.symbol_normalization import get_yfinance_symbol
from services.symbol_resolver import is_dr
from services.transaction_canonicalizer import CanonicalTransaction, canonicalize_transactions

_log = logging.getLogger(__name__)

# Shared quantization used by the live transaction engine
_QUANT = Decimal("0.000001")

# Snapshot is skipped (for write) if fewer than this fraction of holdings
# have a retrievable historical price.
_COVERAGE_THRESHOLD = 0.90

_CASH_INFLOW_TYPES  = frozenset({"DEPOSIT", "INITIAL_CASH"})
_CASH_OUTFLOW_TYPES = frozenset({"WITHDRAW"})


# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────

def _d(v: Any) -> Decimal:
    return Decimal(str(v))


def _f(v: Decimal) -> float:
    return float(v.quantize(_QUANT, rounding=ROUND_HALF_UP))


# ──────────────────────────────────────────────────────────────────────────────
# In-memory state objects (private to this module)
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class _HoldingState:
    symbol:   int | str   # ReplayKeyT — the internal merge key (asset_id → canonical_symbol → raw_symbol)
    # The display / live-DB symbol (TDD Stage 4). Set once, at holding
    # creation, as ctx.canonical_symbol or ctx.raw_symbol — exactly the same
    # two-tier string chain replay_key() itself falls back to. Under legacy
    # keying (Portfolio.replay_asset_id_native OFF), `symbol` above already
    # IS this same string, so every consumer below that reads report_symbol
    # instead of `symbol` is a byte-identical no-op. Under native keying,
    # `symbol` becomes an int (asset_id) — report_symbol is then the ONLY
    # valid string identifier for anything that touches PortfolioItem.symbol
    # (a String column; §4.1 legacy symbol columns are never removed or
    # replaced with a non-symbol value). See _reconcile_portfolio_items,
    # _generate_execution_plan, and _commit_rebuild.
    report_symbol: str
    shares:   Decimal
    avg_cost: Decimal       # fee-inclusive per share
    sector:   str | None = None
    # DR-safe symbol for yfinance price lookups (TDD Stage 0). `symbol` may be
    # the ReplayKey's asset_id/canonical_symbol tier, which fully resolves DR
    # certificates to their US underlying ticker (NVDA01.BK → NVDA per
    # get_yfinance_symbol()). That collapse is correct for replay
    # identity/merging but wrong for price fetching — a DR trades on SET at
    # ~1/10 the US price in THB, not the US ticker's own price. price_symbol
    # preserves the raw, DR-detectable form (set once, at holding creation,
    # from ctx.raw_symbol) so _build_price_matrix's existing is_dr() branch
    # keeps firing correctly. Falls back to `symbol` when unset (non-DR case:
    # canonical_symbol and raw_symbol already agree or the difference doesn't
    # matter to yfinance).
    price_symbol: str | None = None


@dataclass
class _PortfolioState:
    """Mutable portfolio state accumulated during transaction replay."""
    cash_balance:              Decimal
    holdings:                  dict[str, _HoldingState]
    cumulative_realized_pnl:   Decimal

    def copy(self) -> "_PortfolioState":
        return _PortfolioState(
            cash_balance            = self.cash_balance,
            holdings                = {
                sym: _HoldingState(
                    symbol        = h.symbol,
                    report_symbol = h.report_symbol,
                    shares        = h.shares,
                    avg_cost      = h.avg_cost,
                    sector        = h.sector,
                    price_symbol  = h.price_symbol,
                )
                for sym, h in self.holdings.items()
            },
            cumulative_realized_pnl = self.cumulative_realized_pnl,
        )


@dataclass
class _SnapshotDay:
    """All fields for one reconstructed snapshot date."""
    snapshot_date:            str
    # NAV fields (Stage 2)
    total_value:              float = 0.0
    cash_balance:             float = 0.0
    equity_value:             float = 0.0     # not stored in DB; used internally
    total_invested:           float = 0.0
    unrealized_pnl:           float = 0.0
    unrealized_pnl_pct:       float = 0.0
    realized_pnl:             float = 0.0
    holdings_json:            str   = "[]"
    holdings_count:           int   = 0
    sector_breakdown_json:    str   = "{}"
    price_coverage:           float = 1.0
    # Return fields (Stage 3)
    daily_return_pct:         float | None = None
    investment_return_pct:    float | None = None
    investment_return_amount: float | None = None
    net_external_cash_flow:   float | None = None
    imported_asset_value:     float | None = None
    manual_adjustment_value:  float | None = None
    period_realized_pnl:      float | None = None
    period_dividend_income:   float | None = None
    period_fees_paid:         float | None = None


# ──────────────────────────────────────────────────────────────────────────────
# Public result types
# ──────────────────────────────────────────────────────────────────────────────

class ReconciliationStatus(str, Enum):
    MATCH     = "MATCH"
    DIFFERENT = "DIFFERENT"
    MISSING   = "MISSING"
    EXTRA     = "EXTRA"


@dataclass
class ReconciliationRow:
    entity_type:         str                 # "portfolio_item" | "snapshot"
    identifier:          str                 # symbol  OR  "YYYY-MM-DD"
    field:               str                 # column name being compared
    current_value:       Any
    reconstructed_value: Any
    status:              ReconciliationStatus


# ── Confidence report ─────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ConfidenceReport:
    """Multi-dimensional confidence assessment for one reconstruction run.

    Dimensions (each 0–100):
      replay_confidence    Stage 1 found transactions to replay.
      ledger_integrity     Deduction per CRITICAL/ERROR/WARNING validator finding.
      historical_coverage  Proportion of snapshots with full price coverage.
      snapshot_consistency Proportion of reconciliation rows that match (items + snaps).
      validator_confidence Binary gate: 0 if any CRITICAL finding, 100 otherwise.

    overall = weighted sum using _CONF_W_* constants (must sum to 1.0).
    """
    replay_confidence:    float
    ledger_integrity:     float
    historical_coverage:  float
    snapshot_consistency: float
    validator_confidence: float
    overall:              float


# ── Execution plan ────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class PlanOperation:
    """One intended database change in the reconstruction plan."""
    table:         str        # "Portfolio" | "PortfolioItem" | "PortfolioSnapshot"
    operation:     str        # "INSERT" | "UPDATE" | "DELETE" | "UPSERT"
    object_id:     str        # primary identifier: symbol, date, or str(portfolio_id)
    field:         str | None # column name; None for whole-row operations
    current_value: Any
    new_value:     Any
    reason:        str


@dataclass(frozen=True)
class PlanSummary:
    """Aggregate counts from a ReconstructionPlan."""
    portfolio_updated_fields: tuple[str, ...]
    item_inserts:             int
    item_updates:             int    # objects with ≥1 changed field (not field count)
    item_deletes:             int
    snapshot_inserts:         int
    snapshot_updates:         int
    snapshot_deletes:         int    # always 0; engine never deletes snapshots
    total_write_operations:   int    # object-level count
    validator_critical:       int
    validator_errors:         int
    validator_warnings:       int
    confidence_score:         float


@dataclass(frozen=True)
class ReconstructionPlan:
    """Immutable, deterministic execution plan for a single portfolio rebuild.

    Describes every intended database change before any write occurs.
    Running the same replay twice on unchanged data produces an identical plan.
    Plan generation never modifies the database.
    """
    portfolio_id:      int
    confidence_score:  float
    validator_passed:  bool
    critical_findings: int
    operations:        tuple[PlanOperation, ...]
    summary:           PlanSummary
    generated_at:      str    # UTC ISO-8601 timestamp


@dataclass
class RebuildResult:
    portfolio_id:   int
    portfolio_name: str
    success:        bool
    error:          str | None = None
    dry_run:        bool = False
    from_date:      str | None = None
    skip_snapshots: bool = False
    # Stage 1
    transactions_replayed:          int   = 0
    reconstructed_holdings_count:   int   = 0
    reconstructed_cash:             float | None = None
    # Stage 1 (cont.) — effective ledger overlay (Phase 6.7C)
    effective_transaction_count: int       = 0
    excluded_transaction_count:  int       = 0
    repairs_applied:             int       = 0
    repair_ids:                  list[int] = field(default_factory=list)
    # Stage 2
    snapshots_processed:            int = 0
    snapshots_skipped_low_coverage: int = 0
    # Stage 4 tallies
    items_matched:      int = 0
    items_different:    int = 0
    items_missing:      int = 0
    items_extra:        int = 0
    snapshots_matched:  int = 0
    snapshots_different:int = 0
    snapshots_missing:  int = 0
    snapshots_extra:    int = 0
    reconciliation_report: list[ReconciliationRow] = field(default_factory=list)
    # Stage 5 — Ledger validation gate
    aborted:          bool                   = False
    ledger_criticals: int                    = 0
    ledger_errors:    int                    = 0
    ledger_warnings:  int                    = 0
    validator_report: LedgerValidationReport | None = field(default=None)
    # Stage 6 — Confidence report (multi-dimensional)
    confidence_report: ConfidenceReport | None = field(default=None)
    confidence_score:  float                   = 100.0   # = confidence_report.overall
    # Stage 7 — Execution plan
    execution_plan:   ReconstructionPlan | None = field(default=None)
    # Stage 8 — Pre-commit backup
    committed:        bool                   = False
    backup_path:      str | None             = None
    elapsed_seconds:  float                  = 0.0


# ──────────────────────────────────────────────────────────────────────────────
# BANPU-WP2 Step 3/4 — POSITION_CONVERSION preflight, identity resolution, and
# exact accounting application
#
# Scope: validate a conversion row before any replay site touches it, resolve
# which _PortfolioState.holdings key(s) its predecessor/successor identity
# match (Step 3), and — once every check passes — apply the conversion:
# remove the predecessor holding, create or merge the successor holding, and
# apply only the admitted cash/realized-P&L effects (Step 4). Successor
# asset-ID binding against pre-existing PortfolioItem rows and PortfolioItem
# preservation across a conversion-driven delete-and-reinsert commit remain
# BANPU-WP2 Step 5 — this module's replay state has no visibility into stored
# PortfolioItem rows at all, only the Transaction ledger.
# ──────────────────────────────────────────────────────────────────────────────

class PositionConversionReplayError(Exception):
    """Controlled, conversion-specific preflight/replay failure.

    Carries the offending transaction ID and a stable, machine-readable
    reason. Most reasons are POSITION_CONVERSION_* check IDs matching the
    WP2 finding catalog (Implementation Specification §9.1); a small number
    (the Step 5 materialization-identity reasons, e.g.
    POSITION_CONVERSION_SUCCESSOR_ASSET_ID_CONFLICT) describe a rebuilder-
    internal concern — comparing replay output against currently stored
    PortfolioItem rows — with no catalog counterpart, since the catalog
    describes services/ledger_validator.py's own findings, not this
    exception's reasons. Raised before any database mutation is staged; the
    existing outer rebuild_portfolio() exception handler turns this into
    RebuildResult(success=False, aborted=False, committed=False, error=...) —
    it is never converted into a success and never suppresses an unrelated
    exception's own handling.
    """

    def __init__(self, transaction_id: int, reason: str) -> None:
        self.transaction_id = transaction_id
        self.reason = reason
        super().__init__(f"POSITION_CONVERSION tx{transaction_id}: {reason}")


@dataclass(frozen=True)
class _ConversionSuccessorBinding:
    """One conversion's independently resolved successor materialization.

    The complete relation set is keyed by conversion transaction ID, never by
    successor symbol.  A later conversion may legitimately target the same
    successor across a later date; keeping one binding per conversion prevents
    that row from replacing an earlier relation before reconciliation/commit.
    """

    successor_symbol: str
    paired_item: PortfolioItem | None
    successor_asset_id: int


# Transaction types whose presence on a conversion's transition calendar date,
# targeting the predecessor or successor asset, constitutes a same-day
# conflict (Implementation Specification §4.1). Duplicate predecessor/date
# conversion keys are rejected first in Pass 2, so including conversions here
# catches distinct same-day chains without changing DUPLICATE precedence.
_SAME_DAY_CONFLICT_TYPES = frozenset({
    "BUY", "SELL", "INITIAL_POSITION", "QUANTITY_CORRECTION", "POSITION_CONVERSION",
})
_CONVERSION_PROJECTION_TOLERANCE = Decimal("0.000001")


def _preflight_position_conversions(
    raw_txs: list[Transaction],
    canonical_txs: list[CanonicalTransaction],
) -> None:
    """Validate every POSITION_CONVERSION row once, before either replay site.

    Raises PositionConversionReplayError on the first invalid conversion,
    in the deterministic (transaction_date, id) order canonical_txs is
    already sorted in. Operates on the raw, un-repaired canonical list (the
    same list every caller has before any repair overlay is applied) so a
    repair overlay can never make an invalid conversion look valid, or an
    excluded conversion disappear from validation — see
    _reinstate_excluded_conversions() for the complementary guarantee that an
    excluded conversion still reaches replay.

    Frozen canonicalization intentionally hides CanonicalTransaction.asset_id
    in legacy replay mode (prefer_asset_id=False), so the raw-row asset_id
    agreement check below reads the already-loaded raw Transaction row
    directly rather than ctx.asset_id (Implementation Specification §4).
    """
    raw_by_id = {tx.id: tx for tx in raw_txs}
    conversions = [ctx for ctx in canonical_txs if ctx.transaction_type == "POSITION_CONVERSION"]
    if not conversions:
        return

    # Pass 1 — payload validity and raw-row identity/date agreement.
    for ctx in conversions:
        parsed = ctx.position_conversion
        if parsed is None or not parsed.is_valid or parsed.value is None:
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_PAYLOAD_INVALID")
        payload = parsed.value
        raw = raw_by_id.get(ctx.id)
        if (
            raw is None
            or raw.asset_id != payload.predecessor.asset_id
            or ctx.canonical_symbol != payload.predecessor.symbol
            or ctx.transaction_date != payload.dates.valuation_transition_date
        ):
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_IDENTITY_INVALID")

        expected_avg_cost = (
            payload.basis.carried_to_successor / payload.successor.shares_received
        )
        if (
            raw.shares is None
            or abs(_d(raw.shares) - payload.successor.shares_received)
            > _CONVERSION_PROJECTION_TOLERANCE
        ):
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_SHARE_MISMATCH")
        if (
            raw.price_per_share is None
            or raw.total_amount is None
            or abs(_d(raw.price_per_share) - expected_avg_cost)
            > _CONVERSION_PROJECTION_TOLERANCE
            or abs(_d(raw.total_amount) - payload.basis.carried_to_successor)
            > _CONVERSION_PROJECTION_TOLERANCE
        ):
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_BASIS_MISMATCH")

        expected_fees = payload.cash_in_lieu.fees if payload.cash_in_lieu else Decimal("0")
        expected_taxes = payload.cash_in_lieu.taxes if payload.cash_in_lieu else Decimal("0")
        if (
            raw.fees is None
            or raw.taxes is None
            or abs(_d(raw.fees) - expected_fees) > _CONVERSION_PROJECTION_TOLERANCE
            or abs(_d(raw.taxes) - expected_taxes) > _CONVERSION_PROJECTION_TOLERANCE
        ):
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_CIL_INVALID")

    # Pass 2 — duplicate conversion key: exactly one conversion per portfolio,
    # predecessor asset ID, and valuation transition calendar date. The WP1
    # partial unique index already enforces this for persisted rows sharing
    # the same raw transaction_date; this pass is the defensive, schema-
    # independent equivalent (e.g. a legacy pre-index database, or any
    # already-loaded canonical list).
    key_counts: dict[tuple, int] = {}
    for ctx in conversions:
        payload = ctx.position_conversion.value  # validated non-None by Pass 1
        key = (payload.predecessor.asset_id, payload.dates.valuation_transition_date)
        key_counts[key] = key_counts.get(key, 0) + 1
    for ctx in conversions:
        payload = ctx.position_conversion.value
        key = (payload.predecessor.asset_id, payload.dates.valuation_transition_date)
        if key_counts[key] > 1:
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_DUPLICATE")

    # Pass 3 — same-day affected-asset conflict against ordinary equity rows.
    for ctx in conversions:
        payload = ctx.position_conversion.value
        transition_date = payload.dates.valuation_transition_date
        for other in canonical_txs:
            if other.id == ctx.id or other.transaction_type not in _SAME_DAY_CONFLICT_TYPES:
                continue
            if other.transaction_date != transition_date:
                continue
            other_symbols = {other.canonical_symbol}
            other_asset_ids = {other.asset_id}
            if other.transaction_type == "POSITION_CONVERSION":
                other_parsed = other.position_conversion
                if other_parsed is not None and other_parsed.is_valid and other_parsed.value is not None:
                    other_payload = other_parsed.value
                    other_symbols.update({
                        other_payload.predecessor.symbol,
                        other_payload.successor.symbol,
                    })
                    other_asset_ids.update({
                        other_payload.predecessor.asset_id,
                        other_payload.successor.asset_id,
                    })
            targets_predecessor = (
                payload.predecessor.symbol in other_symbols
                or payload.predecessor.asset_id in other_asset_ids
            )
            targets_successor = (
                payload.successor.symbol in other_symbols
                or payload.successor.asset_id in other_asset_ids
            )
            if targets_predecessor or targets_successor:
                raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_SAME_DAY_CONFLICT")


def _reinstate_excluded_conversions(
    all_txs: list[CanonicalTransaction],
    canonical_txs: list[CanonicalTransaction],
) -> list[CanonicalTransaction]:
    """A LedgerRepair EXCLUDE targeting POSITION_CONVERSION is ineffective: the
    conversion remains in the effective canonical sequence regardless of
    apply_repairs or any repair overlay (Implementation Specification §7.1).
    ledger_repair.py itself is not modified — this is the rebuilder consumer
    boundary the frozen plan requires instead.
    """
    effective_ids = {ctx.id for ctx in all_txs}
    missing = [
        ctx for ctx in canonical_txs
        if ctx.transaction_type == "POSITION_CONVERSION" and ctx.id not in effective_ids
    ]
    if not missing:
        return all_txs
    merged = list(all_txs) + missing
    merged.sort(key=lambda c: (c.transaction_date, c.id))
    return merged


def _resolve_conversion_predecessor_key(state: _PortfolioState, payload) -> set:
    """Local, replay_key()-compatible candidate resolution for the predecessor
    holding — legacy mode matches only the canonical-symbol tier (asset_id is
    never a dict key there); native mode also admits the payload's predecessor
    asset ID, including the canonical-symbol fallback for a historical holding
    whose creating transaction was never asset-ID backfilled. Does not call or
    modify replay_key() itself."""
    candidates: set = set()
    if payload.predecessor.symbol in state.holdings:
        candidates.add(payload.predecessor.symbol)
    if payload.predecessor.asset_id in state.holdings:
        candidates.add(payload.predecessor.asset_id)
    return candidates


def _resolve_conversion_successor_key(state: _PortfolioState, payload) -> set:
    """Local candidate resolution for an existing successor holding eligible
    for merge. Zero candidates is not an error (Step 4 creates a fresh
    holding); more than one — including asset-ID and symbol paths resolving
    to different existing holdings — is ambiguous and must fail closed."""
    candidates: set = set()
    if payload.successor.symbol in state.holdings:
        candidates.add(payload.successor.symbol)
    if payload.successor.asset_id in state.holdings:
        candidates.add(payload.successor.asset_id)
    return candidates


# ──────────────────────────────────────────────────────────────────────────────
# BANPU-WP2 Step 5 — conversion materialization identity resolution
#
# Distinct from _resolve_conversion_successor_key() above: that function
# resolves candidates against the in-memory _PortfolioState.holdings built
# purely from the Transaction ledger during replay (Step 3/4, no DB
# awareness). This function resolves the SAME conversion's successor against
# currently STORED PortfolioItem rows — the denormalized materialization
# cache replay has no visibility into — using the frozen asset-ID-precedence/
# canonical-symbol-fallback pairing rule (Implementation Specification §8).
# Runs once, after Stage 1 replay succeeds and before any reconciliation or
# persistent mutation, so both Stage 4 (reconciliation) and Stage 8 (commit)
# consume one already-validated result rather than re-deriving it.
# ──────────────────────────────────────────────────────────────────────────────

def _resolve_conversion_successors(
    db: Session,
    portfolio_id: int,
    all_txs: list[CanonicalTransaction],
) -> dict[int, _ConversionSuccessorBinding]:
    """Pair every conversion's authoritative successor identity against
    currently stored PortfolioItem rows for this portfolio.

    Returns {conversion_transaction_id: _ConversionSuccessorBinding}.  A
    `None` paired item means no pre-existing row exists — the successor will
    be newly created, not a conflict.  The transaction-keyed representation
    deliberately retains every conversion relation when several dated rows
    share one successor symbol.  Raises
    PositionConversionReplayError (fail-closed) when the asset-ID and
    canonical-symbol candidates identify two different stored rows, or when
    a uniquely paired row already carries a different non-null asset_id.  A
    shared successor symbol with conflicting payload asset IDs is likewise
    ambiguous because materialization cannot choose one authoritative identity.
    Read-only: issues one PortfolioItem query, no registry or Asset-table
    access, no general identity backfill (scope note in the WP2 governance
    corpus — asset-ID preservation is authorized only to keep a conversion-
    bearing rebuild lossless for this portfolio, nothing broader).
    """
    conversions = [ctx for ctx in all_txs if ctx.transaction_type == "POSITION_CONVERSION"]
    if not conversions:
        return {}

    current_by_symbol = {
        item.symbol: item
        for item in db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id).all()
    }

    pairings: dict[int, _ConversionSuccessorBinding] = {}
    successor_asset_ids: dict[str, int] = {}
    for ctx in conversions:
        payload = ctx.position_conversion.value  # already preflight-validated

        by_asset_id = next(
            (item for item in current_by_symbol.values()
             if item.asset_id is not None and item.asset_id == payload.successor.asset_id),
            None,
        )
        by_symbol = current_by_symbol.get(payload.successor.symbol)

        if by_asset_id is not None and by_symbol is not None and by_asset_id.id != by_symbol.id:
            raise PositionConversionReplayError(
                ctx.id, "POSITION_CONVERSION_SUCCESSOR_IDENTITY_AMBIGUOUS"
            )

        paired = by_asset_id if by_asset_id is not None else by_symbol
        if paired is not None and paired.asset_id is not None and paired.asset_id != payload.successor.asset_id:
            raise PositionConversionReplayError(
                ctx.id, "POSITION_CONVERSION_SUCCESSOR_ASSET_ID_CONFLICT"
            )

        previous_asset_id = successor_asset_ids.get(payload.successor.symbol)
        if previous_asset_id is not None and previous_asset_id != payload.successor.asset_id:
            raise PositionConversionReplayError(
                ctx.id, "POSITION_CONVERSION_SUCCESSOR_IDENTITY_AMBIGUOUS"
            )
        successor_asset_ids[payload.successor.symbol] = payload.successor.asset_id
        pairings[ctx.id] = _ConversionSuccessorBinding(
            successor_symbol=payload.successor.symbol,
            paired_item=paired,
            successor_asset_id=payload.successor.asset_id,
        )

    return pairings


def _conversion_successors_by_symbol(
    conversion_successors: dict[int, _ConversionSuccessorBinding] | None,
) -> dict[str, tuple[_ConversionSuccessorBinding, ...]]:
    """Group preserved transaction-keyed bindings for final projection.

    Grouping is intentionally a downstream view: the source mapping still
    contains one independently auditable binding per conversion transaction.
    Every binding for a shared successor must carry the same authoritative
    asset ID (enforced by _resolve_conversion_successors), so reconciliation
    and commit can consume the first deterministic binding without losing the
    other relations.
    """
    grouped: dict[str, list[_ConversionSuccessorBinding]] = {}
    for transaction_id in sorted((conversion_successors or {})):
        binding = conversion_successors[transaction_id]
        grouped.setdefault(binding.successor_symbol, []).append(binding)
    return {symbol: tuple(bindings) for symbol, bindings in grouped.items()}


# Extends Stage 5's ledger validation gate (§7.1/§9): the generic
# `if result.ledger_criticals > 0` rule already blocks on any conversion
# CRITICAL finding regardless of check_id, so no change is needed for that
# half of the frozen policy. POSITION_CONVERSION_SAME_DAY_CONFLICT is the one
# WP2-catalogued finding with a fixed ERROR severity that must still block —
# every other ERROR finding keeps its current (non-blocking) treatment.
# Rebuilder preflight is the primary detector. This Stage 5 gate independently
# corroborates the validator boundary and closes the generic CRITICAL-only
# severity hole if the validator reports the conflict there.
_CONVERSION_STAGE5_BLOCKING_ERROR_CHECK_IDS = frozenset({"POSITION_CONVERSION_SAME_DAY_CONFLICT"})


def _has_conversion_blocking_error(validation_report: LedgerValidationReport) -> bool:
    return any(
        f.check_id in _CONVERSION_STAGE5_BLOCKING_ERROR_CHECK_IDS
        for f in validation_report.errors
    )


# ──────────────────────────────────────────────────────────────────────────────
# Stage 1 — Transaction replay
# ──────────────────────────────────────────────────────────────────────────────

def _apply_transaction(
    state: _PortfolioState,
    ctx: CanonicalTransaction,
    *,
    conversion_seen: set | None = None,
) -> None:
    """Apply one canonical transaction to the mutable portfolio state in-place."""
    tx_type = ctx.transaction_type
    amount  = ctx.total_amount  # already Decimal

    if tx_type in _CASH_INFLOW_TYPES or tx_type == "DIVIDEND":
        state.cash_balance += amount

    elif tx_type == "WITHDRAW":
        state.cash_balance -= amount

    elif tx_type == "BUY":
        shares = ctx.shares
        if shares <= 0:
            return
        # total_amount = net_buy_amount (gross + all fees) — same as live engine
        eff_price = amount / shares
        state.cash_balance -= amount

        sym = replay_key(ctx)
        if sym in state.holdings:
            h = state.holdings[sym]
            new_shares = h.shares + shares
            new_avg    = (h.shares * h.avg_cost + amount) / new_shares
            h.shares   = new_shares
            h.avg_cost = new_avg
            if ctx.sector and not h.sector:
                h.sector = ctx.sector
        else:
            state.holdings[sym] = _HoldingState(
                symbol        = sym,
                report_symbol = ctx.canonical_symbol or ctx.raw_symbol,
                shares        = shares,
                avg_cost      = eff_price,
                sector        = ctx.sector,
                price_symbol  = ctx.raw_symbol,
            )

    elif tx_type == "SELL":
        shares = ctx.shares
        if shares <= 0:
            return
        # total_amount = net_sell_proceeds (cash received after fees)
        state.cash_balance += amount
        pnl = ctx.realized_pnl if ctx.realized_pnl is not None else 0.0
        state.cumulative_realized_pnl += _d(pnl)

        sym = replay_key(ctx)
        if sym in state.holdings:
            h          = state.holdings[sym]
            new_shares = h.shares - shares
            if _f(new_shares) <= 0:
                del state.holdings[sym]
            else:
                h.shares = new_shares

    elif tx_type == "INITIAL_POSITION":
        sym    = replay_key(ctx)
        shares = ctx.shares
        avg    = ctx.price_per_share
        if not sym or shares <= 0:
            return
        if sym in state.holdings:
            h          = state.holdings[sym]
            new_shares = h.shares + shares
            new_avg    = (h.shares * h.avg_cost + shares * avg) / new_shares if new_shares else avg
            h.shares   = new_shares
            h.avg_cost = new_avg
            if ctx.sector and not h.sector:
                h.sector = ctx.sector
        else:
            state.holdings[sym] = _HoldingState(
                symbol        = sym,
                report_symbol = ctx.canonical_symbol or ctx.raw_symbol,
                shares        = shares,
                avg_cost      = avg,
                sector        = ctx.sector,
                price_symbol  = ctx.raw_symbol,
            )
        # INITIAL_POSITION does NOT affect cash balance

    elif tx_type == "QUANTITY_CORRECTION":
        sym = replay_key(ctx)
        if not sym or sym not in state.holdings:
            return
        delta = ctx.qty_correction_delta  # pre-parsed Decimal with sign
        h     = state.holdings[sym]
        new_shares = h.shares + delta
        if delta > 0:
            price  = ctx.price_per_share
            if new_shares > 0:
                h.avg_cost = (h.shares * h.avg_cost + delta * price) / new_shares
        if _f(new_shares) <= 0:
            del state.holdings[sym]
        else:
            h.shares = new_shares
        # QUANTITY_CORRECTION does NOT affect cash balance

    elif tx_type == "POSITION_CONVERSION":
        # BANPU-WP2 Step 4 scope: everything through successor-candidate
        # resolution is unchanged Step 3 preflight/identity logic — every
        # raw-row/payload/duplicate/same-day fact was already verified once
        # by _preflight_position_conversions() before replay started. What
        # follows the candidate checks is new: exact-Decimal accounting
        # application (predecessor removal, successor create/merge, admitted
        # cash/realized-P&L effects). No mutation happens above this point,
        # so a raise anywhere before it leaves state untouched.
        parsed = ctx.position_conversion
        if parsed is None or not parsed.is_valid or parsed.value is None:
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_PAYLOAD_INVALID")
        payload = parsed.value

        if conversion_seen is not None:
            key = (payload.predecessor.asset_id, payload.dates.valuation_transition_date)
            if key in conversion_seen:
                raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_DUPLICATE")
            conversion_seen.add(key)

        predecessor_candidates = _resolve_conversion_predecessor_key(state, payload)
        if len(predecessor_candidates) == 0:
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_WITHOUT_HOLDING")
        if len(predecessor_candidates) > 1:
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_AMBIGUOUS_HOLDING")
        predecessor_key = next(iter(predecessor_candidates))
        predecessor = state.holdings[predecessor_key]

        successor_candidates = _resolve_conversion_successor_key(state, payload)
        if len(successor_candidates) > 1:
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_AMBIGUOUS_HOLDING")

        # Qp / B0 reconciliation — the replayed predecessor holding must
        # actually be the position the payload describes converting. Shares
        # are compared exactly (both sides are payload- or ledger-derived
        # Decimals with no independent rounding); basis is compared with the
        # spec's documented THB 0.01 tolerance to absorb float→Decimal
        # round-trip noise already present in upstream price_per_share
        # parsing (see transaction_canonicalizer), not to hide a real
        # mismatch.
        if predecessor.shares != payload.predecessor.shares_surrendered:
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_SHARE_MISMATCH")
        replayed_basis = predecessor.shares * predecessor.avg_cost
        if abs(replayed_basis - payload.basis.before) > Decimal("0.01"):
            raise PositionConversionReplayError(ctx.id, "POSITION_CONVERSION_BASIS_MISMATCH")

        # Admitted values come only from the payload — never re-derived from
        # predecessor.avg_cost/shares — so cash-in-lieu fees/taxes/rounding
        # already reconciled once by parse_position_conversion_payload()'s
        # own invariant checks are not silently redone here (Requirement 4).
        received_shares    = payload.successor.shares_received      # Qr
        carried_basis      = payload.basis.carried_to_successor     # Bs
        net_cash            = payload.cash_in_lieu.net_cash if payload.cash_in_lieu else Decimal("0")        # Cn
        realized_pnl        = payload.cash_in_lieu.realized_pnl if payload.cash_in_lieu else Decimal("0")    # RP
        predecessor_sector  = predecessor.sector

        del state.holdings[predecessor_key]

        if successor_candidates:
            successor_key = next(iter(successor_candidates))
            successor      = state.holdings[successor_key]
            existing_basis  = successor.shares * successor.avg_cost
            combined_shares = successor.shares + received_shares
            combined_basis  = existing_basis + carried_basis
            successor.shares   = combined_shares
            successor.avg_cost = combined_basis / combined_shares
            if not successor.sector:
                successor.sector = predecessor_sector
            # Step 5 (Implementation Specification §7.3.5): the successor's
            # reported symbol is always bound from the payload, on merge as
            # well as on create — never left at whatever report_symbol the
            # pre-existing holding happened to carry.
            successor.report_symbol = payload.successor.symbol
        else:
            # New holding's merge key follows the replay run's canonical mode,
            # not the tier that happened to resolve the predecessor. In native
            # mode the conversion ctx retains its top-level asset_id even when
            # the historical predecessor itself required the null-asset symbol
            # fallback. A later native successor trade therefore resolves to
            # this same asset-ID key.
            successor_key = (
                payload.successor.asset_id if ctx.asset_id is not None
                else payload.successor.symbol
            )
            state.holdings[successor_key] = _HoldingState(
                symbol        = successor_key,
                report_symbol = payload.successor.symbol,
                shares        = received_shares,
                avg_cost      = carried_basis / received_shares,
                sector        = predecessor_sector,
                price_symbol  = payload.successor.symbol,
            )

        state.cash_balance            += net_cash
        state.cumulative_realized_pnl += realized_pnl


def _replay_with_date_snapshots(
    txs:   list[CanonicalTransaction],
    dates: list[str],           # snapshot dates, sorted ascending
) -> dict[str, _PortfolioState]:
    """Single-pass replay that captures state at the end of each requested date.

    Returns {date: _PortfolioState} for every date in `dates`.
    Complexity: O(N + D) where N = transactions, D = distinct dates.

    Owns its own fresh conversion-key duplicate-tracking set (BANPU-WP2 Step 3)
    — this is Stage 2's replay invocation, entirely independent of Stage 1's
    (rebuild_portfolio()'s own sequential loop, which creates its own set).
    Neither site treats the other's application as a duplicate.
    """
    state = _PortfolioState(
        cash_balance            = Decimal("0"),
        holdings                = {},
        cumulative_realized_pnl = Decimal("0"),
    )
    result: dict[str, _PortfolioState] = {}
    tx_idx = 0
    n_txs  = len(txs)
    conversion_seen: set = set()

    for snap_date in dates:
        # Advance: apply every transaction with tx_date <= snap_date
        while tx_idx < n_txs:
            ctx     = txs[tx_idx]
            tx_date = ctx.transaction_date.strftime("%Y-%m-%d")
            if tx_date <= snap_date:
                _apply_transaction(state, ctx, conversion_seen=conversion_seen)
                tx_idx += 1
            else:
                break
        result[snap_date] = state.copy()

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Stage 2 — Historical price matrix
# ──────────────────────────────────────────────────────────────────────────────

async def _build_price_matrix(
    symbols:     list[str],
    dates:       list[str],       # "YYYY-MM-DD", sorted
    progress_cb: Callable[[str], None] | None = None,
) -> dict[str, dict[str, float | None]]:
    """Batch-fetch historical closing prices for all symbols × all dates.

    For weekend / holiday dates the last available trading-day close is used
    (backward-fill).

    Returns: {symbol: {date_str: price | None}}
    """
    if not symbols or not dates:
        return {}

    # Always use "5y" so the fetch key matches the pre-warmed cache.
    # DR certificates (e.g. AAPL01.BK) have SET listing history since ~2020;
    # requesting "10y" or "max" on a .BK ticker that lacks the full period
    # causes yfinance to silently fall back to the underlying US ticker and
    # return USD prices instead of THB DR prices.
    period = "5y"

    result: dict[str, dict[str, float | None]] = {}

    for i, sym in enumerate(symbols):
        # DR certificates trade on SET at ~1/10 the US underlying price in THB.
        # get_yfinance_symbol() resolves them to the US ticker (AAPL01.BK → AAPL),
        # which returns USD prices and inflates NAV by ~10×.  Use the .BK form
        # directly so yfinance returns the actual SET DR market price.
        # print(f"{i+1}/{len(symbols)}  {sym}")
        # print(f"\n========== START {sym} ==========")
        if is_dr(sym):
            yf_sym = sym if sym.endswith(".BK") else sym + ".BK"
        else:
            yf_sym = get_yfinance_symbol(sym)

        try:
            df: Optional[pd.DataFrame] = await asyncio.to_thread(
                fetch_history, yf_sym, period, "1d"
            )
            
            # print("=" * 80)
            # print("period :", period)
            # print("ORIGINAL SYMBOL :", sym)
            # print("YFINANCE SYMBOL :", yf_sym)
            # print("cache key :", f"history:{period}:1d")
            # print(f"========== END {sym} ==========")
            if df is not None and not df.empty:
                print(df["Close"].head())
                tail = df["Close"].tail()
        except Exception as exc:
            print(f"========== EXCEPTION {sym}: {exc}")
            _log.warning("price_matrix fetch failed symbol=%s yf=%s: %s", sym, yf_sym, exc)
            df = None        

        if df is None:
            print("DATAFRAME : None")
        else:
           x = df.head()
           print(x.shape)
           print(df.tail())
           print(df["Close"].iloc[0])
           print(df["Close"].iloc[-1])

        date_price: dict[str, float | None] = {}
        if df is not None and not df.empty:
            df_sorted   = df.sort_index()
            df_dates    = df_sorted.index.strftime("%Y-%m-%d").tolist()
            df_closes   = [
                float(v) if pd.notna(v) and float(v) > 0 else None
                for v in df_sorted["Close"]
            ]

            for snap_date in dates:
                # Binary search: last trading day on or before snap_date
                idx = bisect.bisect_right(df_dates, snap_date) - 1
                date_price[snap_date] = df_closes[idx] if idx >= 0 else None
        else:
            date_price = {d: None for d in dates}
        
        result[sym] = date_price
        
        if progress_cb:
            progress_cb(sym)

    # print("RETURNING PRICE MATRIX")
    # print(result.keys())
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Stage 2+3 — Snapshot day construction + return fields
# ──────────────────────────────────────────────────────────────────────────────

def _build_snapshot_day(
    snapshot_date: str,
    state:         _PortfolioState,
    price_row:     dict[str, float | None],   # {symbol: price} for this date
    all_txs:       list[CanonicalTransaction],
    prev_date:     str | None,
    prev_nav:      float | None,
) -> _SnapshotDay:
    """Build a _SnapshotDay from portfolio state + historical prices.

    Also computes Stage 3 return fields when prev_date / prev_nav are provided.
    """
    cash = float(state.cash_balance)

    holdings_list: list[dict] = []
    equity_value  = 0.0
    total_cost    = 0.0
    sector_agg:  dict[str, float] = {}
    n_priced      = 0
    n_holdings    = len(state.holdings)

    for sym, h in state.holdings.items():
        shares   = float(h.shares)
        avg_cost = float(h.avg_cost)
        # print("SNAPSHOT PRICE", snapshot_date, sym, price_row.get(sym))

        price    = price_row.get(sym)

        mv       = shares * price if price is not None else None
        cost     = shares * avg_cost
        upnl     = (mv - cost) if mv is not None else None
        sector   = h.sector or "Other"

        if mv is not None:
            equity_value             += mv
            sector_agg[sector]        = sector_agg.get(sector, 0.0) + mv
            n_priced                 += 1
        total_cost += cost

        # report_symbol, never the internal merge key `sym` — an int under
        # native keying, and holdings_json's "symbol" field must always be a
        # display string (TDD §4.2; the additive "asset_id" key §4.2 also
        # describes is Stage 5+ work, not introduced here).
        holdings_list.append({
            "symbol":            h.report_symbol,
            "shares":            round(shares, 6),
            "avg_cost":          round(avg_cost, 4),
            "current_price":     round(price, 4) if price is not None else None,
            "market_value":      round(mv, 4) if mv is not None else None,
            "unrealized_pnl":    round(upnl, 4) if upnl is not None else None,
            "unrealized_pnl_pct":
                round(upnl / cost * 100, 2) if (upnl is not None and cost > 0) else None,
            "sector":            sector,
            "price_missing":     price is None,
        })

    total_value        = equity_value + cash
    unrealized_pnl     = equity_value - total_cost
    unrealized_pnl_pct = (unrealized_pnl / total_cost * 100) if total_cost > 0 else 0.0
    coverage           = n_priced / n_holdings if n_holdings > 0 else 1.0

    sector_breakdown: dict[str, float] = {
        sec: round(val / total_value * 100, 2) if total_value > 0 else 0.0
        for sec, val in sector_agg.items()
    }

    day = _SnapshotDay(
        snapshot_date          = snapshot_date,
        total_value            = round(total_value, 4),
        cash_balance           = round(cash, 4),
        equity_value           = round(equity_value, 4),
        total_invested         = round(total_cost, 4),
        unrealized_pnl         = round(unrealized_pnl, 4),
        unrealized_pnl_pct     = round(unrealized_pnl_pct, 4),
        realized_pnl           = round(float(state.cumulative_realized_pnl), 4),
        holdings_json          = json.dumps(holdings_list),
        holdings_count         = n_holdings,
        sector_breakdown_json  = json.dumps(sector_breakdown),
        price_coverage         = round(coverage, 4),
    )

    # Stage 3: populate return fields when we have a previous snapshot
    if prev_date and prev_nav and prev_nav > 0:
        _populate_return_fields(day, prev_date, snapshot_date, prev_nav, all_txs)

    return day


def _populate_return_fields(
    day:       _SnapshotDay,
    prev_date: str,
    curr_date: str,
    prev_nav:  float,
    all_txs:   list[CanonicalTransaction],
) -> None:
    """Compute and set return-related fields on the SnapshotDay.

    Window: prev_date < tx.transaction_date <= curr_date.
    Uses transaction_date (not created_at) — correct for historical reconstruction.

    Delegates the actual formulas to services.portfolio_metrics.compute_period_metrics
    (ADR-004 — exactly one implementation of portfolio return calculations,
    shared across every snapshot-producing engine).
    """
    window_txs = [
        ctx for ctx in all_txs
        if prev_date < ctx.transaction_date.strftime("%Y-%m-%d") <= curr_date
    ]

    # Current prices from holdings_json for valuing asset imports/corrections
    price_map: dict[str, float] = {}
    try:
        for h in json.loads(day.holdings_json):
            sym = h.get("symbol")
            cp  = h.get("current_price")
            if sym and cp is not None:
                price_map[sym] = float(cp)
    except (ValueError, TypeError):
        pass

    metrics = compute_period_metrics(
        curr_nav=day.total_value,
        prev_nav=prev_nav,
        period_transactions=window_txs,
        price_lookup=price_map,
    )

    # ── Set return fields ─────────────────────────────────────────────────────
    day.total_invested           = round(day.total_invested, 4)
    day.net_external_cash_flow   = metrics.net_external_cash_flow
    day.imported_asset_value     = metrics.imported_asset_value
    day.manual_adjustment_value  = metrics.manual_adjustment_value
    day.period_realized_pnl      = metrics.period_realized_pnl
    day.period_dividend_income   = metrics.period_dividend_income
    day.period_fees_paid         = metrics.period_fees_paid
    day.investment_return_pct    = metrics.investment_return_pct
    day.investment_return_amount = metrics.investment_return_amount
    day.daily_return_pct         = metrics.daily_return_pct

# ──────────────────────────────────────────────────────────────────────────────
# Stage 4 — Reconciliation
# ──────────────────────────────────────────────────────────────────────────────

def _reconcile_portfolio_items(
    db:                    Session,
    portfolio_id:          int,
    final_state:           _PortfolioState,
    conversion_successors: dict[int, _ConversionSuccessorBinding] | None = None,
) -> list[ReconciliationRow]:
    """Compare existing PortfolioItem rows against the reconstructed final state.

    conversion_successors (BANPU-WP2 Step 5, from _resolve_conversion_successors,
    already fail-closed-validated before Stage 4 runs) keeps one relation per
    conversion transaction.  The symbol-grouped view below marks which final
    reconstructed symbols are conversion successors.  Only those symbols get
    the extended five-field (asset_id, symbol, shares, avg_cost, basis)
    reconciliation path — every ordinary symbol keeps the existing two-field
    shares/avg_cost behavior unchanged (Implementation Specification §8).
    """
    conversion_by_symbol = _conversion_successors_by_symbol(conversion_successors)
    current = {
        item.symbol: item
        for item in db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id).all()
    }
    # Re-keyed by report_symbol (always a str), never by the raw internal
    # merge key (`symbol`, which is an int under native/asset_id keying —
    # TDD Stage 4). Under legacy keying this is a byte-identical no-op,
    # since report_symbol IS the merge key there. See _HoldingState's own
    # docstring for why PortfolioItem.symbol must never see a non-string
    # value.
    recon = {h.report_symbol: h for h in final_state.holdings.values()}

    rows: list[ReconciliationRow] = []

    paired_current_symbols = {
        binding.paired_item.symbol
        for bindings in conversion_by_symbol.values()
        for binding in bindings
        if binding.paired_item is not None
    }
    symbols = (set(current) - paired_current_symbols) | set(recon)

    for sym in sorted(symbols):
        successor_bindings = conversion_by_symbol.get(sym, ())
        paired_item = successor_bindings[0].paired_item if successor_bindings else None
        curr_item  = paired_item if paired_item is not None else current.get(sym)
        recon_item = recon.get(sym)

        if curr_item is None:
            rows.append(ReconciliationRow(
                entity_type         = "portfolio_item",
                identifier          = sym,
                field               = "*",
                current_value       = None,
                reconstructed_value = {
                    "shares":   _f(recon_item.shares),
                    "avg_cost": _f(recon_item.avg_cost),
                },
                status = ReconciliationStatus.MISSING,
            ))
            continue

        if recon_item is None:
            rows.append(ReconciliationRow(
                entity_type         = "portfolio_item",
                identifier          = sym,
                field               = "*",
                current_value       = {"shares": curr_item.shares, "avg_cost": curr_item.avg_cost},
                reconstructed_value = None,
                status              = ReconciliationStatus.EXTRA,
            ))
            continue

        # Both exist and sym is a conversion successor with an actual
        # pre-existing comparand — five independent fields instead of the
        # ordinary two. A brand-new successor (no pre-existing row) took the
        # MISSING branch above instead; no fabricated comparand here.
        if successor_bindings:
            successor_asset_id = successor_bindings[0].successor_asset_id
            recon_shares   = _f(recon_item.shares)
            recon_avg_cost = _f(recon_item.avg_cost)
            for col, curr_val, recon_val, tol in [
                ("asset_id", curr_item.asset_id, successor_asset_id,             0),
                ("symbol",   curr_item.symbol,   recon_item.report_symbol,       0),
                ("shares",   curr_item.shares,   recon_shares,                   0.0001),
                ("avg_cost", curr_item.avg_cost, recon_avg_cost,                 0.01),
                ("basis",    (curr_item.shares or 0.0) * (curr_item.avg_cost or 0.0),
                              recon_shares * recon_avg_cost,                     0.01),
            ]:
                if isinstance(curr_val, (int, float)) and isinstance(recon_val, (int, float)):
                    matches = abs(curr_val - recon_val) <= tol
                else:
                    matches = curr_val == recon_val
                rows.append(ReconciliationRow(
                    entity_type         = "portfolio_item",
                    identifier          = sym,
                    field               = col,
                    current_value       = curr_val,
                    reconstructed_value = recon_val,
                    status              = ReconciliationStatus.MATCH if matches
                                          else ReconciliationStatus.DIFFERENT,
                ))
            continue

        # Both exist — compare field by field (ordinary items, unchanged)
        for col, tol in [("shares", 0.0001), ("avg_cost", 0.01)]:
            curr_val  = getattr(curr_item, col)
            recon_val = _f(getattr(recon_item, col))
            diff      = abs((curr_val or 0.0) - (recon_val or 0.0))
            rows.append(ReconciliationRow(
                entity_type         = "portfolio_item",
                identifier          = sym,
                field               = col,
                current_value       = round(curr_val, 6),
                reconstructed_value = round(recon_val, 6),
                status              = ReconciliationStatus.MATCH if diff <= tol
                                      else ReconciliationStatus.DIFFERENT,
            ))

    return rows


def _reconcile_snapshots(
    db:            Session,
    portfolio_id:  int,
    snapshot_days: list[_SnapshotDay],
    from_date:     str | None,
) -> list[ReconciliationRow]:
    """Compare existing PortfolioSnapshot rows against the reconstructed days."""
    recon_map = {day.snapshot_date: day for day in snapshot_days}

    # Only compare snapshots in the rebuild window
    query = db.query(PortfolioSnapshot).filter_by(portfolio_id=portfolio_id)
    if from_date:
        query = query.filter(PortfolioSnapshot.snapshot_date >= from_date)
    current_map = {s.snapshot_date: s for s in query.all()}

    rows: list[ReconciliationRow] = []
    all_dates = sorted(set(current_map) | set(recon_map))

    _NAV_FIELDS = [
        ("total_value",     1.0),
        ("cash_balance",    1.0),
        ("total_invested",  1.0),
        ("unrealized_pnl",  1.0),
        ("realized_pnl",    1.0),
    ]

    for date in all_dates:
        curr  = current_map.get(date)
        recon = recon_map.get(date)

        if curr is None:
            rows.append(ReconciliationRow(
                entity_type         = "snapshot",
                identifier          = date,
                field               = "*",
                current_value       = None,
                reconstructed_value = {"total_value": recon.total_value if recon else None},
                status              = ReconciliationStatus.MISSING,
            ))
            continue

        if recon is None:
            rows.append(ReconciliationRow(
                entity_type         = "snapshot",
                identifier          = date,
                field               = "*",
                current_value       = {"total_value": curr.total_value},
                reconstructed_value = None,
                status              = ReconciliationStatus.EXTRA,
            ))
            continue

        for col, tol in _NAV_FIELDS:
            curr_val  = getattr(curr, col, None)
            recon_val = getattr(recon, col, None)
            if curr_val is None and recon_val is None:
                continue
            diff = abs((curr_val or 0.0) - (recon_val or 0.0))
            rows.append(ReconciliationRow(
                entity_type         = "snapshot",
                identifier          = date,
                field               = col,
                current_value       = round(curr_val, 2) if curr_val is not None else None,
                reconstructed_value = round(recon_val, 2) if recon_val is not None else None,
                status              = ReconciliationStatus.MATCH if diff <= tol
                                      else ReconciliationStatus.DIFFERENT,
            ))

    return rows


# ──────────────────────────────────────────────────────────────────────────────
# Stage 5 — Ledger validation gate + confidence report
# ──────────────────────────────────────────────────────────────────────────────

# Deduction constants for the ledger_integrity dimension (applied within 0-100 scale)
_CONF_LEDGER_PER_CRITICAL = 10.0
_CONF_LEDGER_PER_ERROR    =  5.0
_CONF_LEDGER_PER_WARNING  =  2.0

# Documented weights for ConfidenceReport.overall — must sum exactly to 1.0
_CONF_W_REPLAY      = 0.20   # Stage 1 success
_CONF_W_LEDGER      = 0.25   # ledger validator integrity
_CONF_W_COVERAGE    = 0.20   # historical price coverage
_CONF_W_CONSISTENCY = 0.20   # item + snapshot field reconciliation
_CONF_W_VALIDATOR   = 0.15   # binary gate (0 if any CRITICAL)


def _compute_confidence_report(
    result:        RebuildResult,
    snapshot_days: list[_SnapshotDay],
) -> ConfidenceReport:
    """Compute the multi-dimensional ConfidenceReport for a rebuild run.

    Dimensions
    ----------
    replay_confidence     0 if no transactions were replayed; 100 otherwise.
    ledger_integrity      100 minus per-finding deductions (CRITICAL/ERROR/WARNING).
    historical_coverage   100 × (1 − low_coverage_snaps / total_snaps).
    snapshot_consistency  100 × (1 − different_recon_rows / total_recon_rows).
                          Covers both PortfolioItem and PortfolioSnapshot rows.
    validator_confidence  0 if any CRITICAL finding; 100 otherwise.

    overall = weighted sum using _CONF_W_* constants.
    """
    # Replay confidence
    replay = 100.0 if result.transactions_replayed > 0 else 0.0

    # Ledger integrity
    ledger = max(0.0, min(100.0,
        100.0
        - result.ledger_criticals * _CONF_LEDGER_PER_CRITICAL
        - result.ledger_errors    * _CONF_LEDGER_PER_ERROR
        - result.ledger_warnings  * _CONF_LEDGER_PER_WARNING
    ))

    # Historical coverage
    total_snaps = len(snapshot_days)
    low_cov = sum(
        1 for d in snapshot_days
        if d.holdings_count > 0 and d.price_coverage < _COVERAGE_THRESHOLD
    )
    coverage = max(0.0, min(100.0,
        100.0 * (1.0 - low_cov / total_snaps) if total_snaps > 0 else 100.0
    ))

    # Snapshot + item reconciliation consistency
    total_recon = (
        result.items_matched    + result.items_different
        + result.items_missing  + result.items_extra
        + result.snapshots_matched  + result.snapshots_different
        + result.snapshots_missing  + result.snapshots_extra
    )
    different_recon = result.items_different + result.snapshots_different
    consistency = max(0.0, min(100.0,
        100.0 * (1.0 - different_recon / total_recon)
        if total_recon > 0 else 100.0
    ))

    # Validator confidence (binary gate)
    validator_conf = 0.0 if result.ledger_criticals > 0 else 100.0

    # Weighted overall
    overall = round(
        replay         * _CONF_W_REPLAY
        + ledger       * _CONF_W_LEDGER
        + coverage     * _CONF_W_COVERAGE
        + consistency  * _CONF_W_CONSISTENCY
        + validator_conf * _CONF_W_VALIDATOR,
        1,
    )

    return ConfidenceReport(
        replay_confidence    = round(replay, 1),
        ledger_integrity     = round(ledger, 1),
        historical_coverage  = round(coverage, 1),
        snapshot_consistency = round(consistency, 1),
        validator_confidence = round(validator_conf, 1),
        overall              = overall,
    )


def _compute_confidence_score(
    result:        RebuildResult,
    snapshot_days: list[_SnapshotDay],
) -> float:
    """Return the overall confidence score (0–100).

    Delegates to _compute_confidence_report().overall.
    Kept for backward compatibility with callers that only need the scalar.
    """
    return _compute_confidence_report(result, snapshot_days).overall


# ──────────────────────────────────────────────────────────────────────────────
# Stage 6 — Backup export
# ──────────────────────────────────────────────────────────────────────────────

def _export_backup(
    db:           Session,
    portfolio_id: int,
    backup_dir:   str = "backups",
) -> str:
    """Dump the current PortfolioItem + PortfolioSnapshot + LedgerRepair rows to JSON.

    Called before the atomic commit so the pre-rebuild state is preserved.
    LedgerRepair rows are included so that a restore from backup can
    reconstruct the same effective canonical list that was used for the rebuild.
    Returns the absolute path of the written file.
    """
    os.makedirs(backup_dir, exist_ok=True)
    ts   = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(backup_dir, f"rebuild_{portfolio_id}_{ts}.json")

    # M36.1 F05 documented exception: id-only lookup, not
    # resolve_portfolio_reference(). _export_backup has no workspace_id in
    # its signature and is reachable only from the rebuild_portfolio CLI
    # subcommand (operator tool) — it never receives an untrusted or
    # mismatched workspace/portfolio pair, so there is no referenceability
    # gap to close here. Threading a workspace_id through the whole CLI
    # rebuild pipeline for this alone is out of scope for this pass.
    portfolio = db.query(Portfolio).filter_by(id=portfolio_id).first()
    items     = db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id).all()
    snaps     = db.query(PortfolioSnapshot).filter_by(portfolio_id=portfolio_id).all()
    repairs   = db.query(LedgerRepair).filter_by(portfolio_id=portfolio_id).all()

    data: dict = {
        "portfolio_id":     portfolio_id,
        "backup_timestamp": datetime.utcnow().isoformat() + "Z",
        "portfolio": {
            "name":         portfolio.name          if portfolio else None,
            "cash_balance": portfolio.cash_balance  if portfolio else None,
        },
        "portfolio_items": [
            {
                "symbol":    item.symbol,
                "shares":    item.shares,
                "avg_cost":  item.avg_cost,
                "sector":    item.sector,
                "allow_swap": item.allow_swap,
            }
            for item in items
        ],
        "snapshots": [
            {
                "snapshot_date": snap.snapshot_date,
                "total_value":   snap.total_value,
                "cash_balance":  snap.cash_balance,
                "equity_value":  getattr(snap, "equity_value", None),
                "holdings_json": snap.holdings_json,
            }
            for snap in snaps
        ],
        "ledger_repairs": [
            {
                "id":             repair.id,
                "transaction_id": repair.transaction_id,
                "repair_plan_id": repair.repair_plan_id,
                "repair_type":    repair.repair_type,
                "reason":         repair.reason,
                "reason_code":    repair.reason_code,
                "payload_json":   repair.payload_json,
                "created_by":     repair.created_by,
                "created_at":     repair.created_at,
                "is_active":      repair.is_active,
            }
            for repair in repairs
        ],
    }

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, default=str)

    _log.info("backup written: portfolio=%d path=%s", portfolio_id, path)
    return path


# ──────────────────────────────────────────────────────────────────────────────
# Stage 7 — Execution plan
# ──────────────────────────────────────────────────────────────────────────────

def _values_differ(a: Any, b: Any, tol: float = 0.01) -> bool:
    """Return True when a and b are meaningfully different.

    None vs None → no difference.
    Numerics compared with absolute tolerance.
    Everything else compared as strings.
    """
    if a is None and b is None:
        return False
    if a is None or b is None:
        return True
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) > tol
    return str(a) != str(b)


def _generate_execution_plan(
    db:             Session,
    portfolio_id:   int,
    portfolio:      Portfolio,
    final_state:    _PortfolioState,
    snapshot_days:  list[_SnapshotDay],
    from_date:      str | None,
    confidence:     ConfidenceReport,
    validator:      LedgerValidationReport | None,
    skip_snapshots: bool,
) -> ReconstructionPlan:
    """Generate a deterministic, read-only execution plan.

    Lists every intended DB change without writing anything.
    Running the same replay twice on unchanged data produces an identical plan.
    The plan is the official audit trail for every reconstruction.
    """
    ops: list[PlanOperation] = []

    # ── Portfolio.cash_balance ────────────────────────────────────────────────
    new_cash = _f(final_state.cash_balance)
    port_updated_fields: list[str] = []
    if _values_differ(portfolio.cash_balance, new_cash, tol=0.001):
        port_updated_fields.append("cash_balance")
        ops.append(PlanOperation(
            table         = "Portfolio",
            operation     = "UPDATE",
            object_id     = str(portfolio_id),
            field         = "cash_balance",
            current_value = round(portfolio.cash_balance, 4) if portfolio.cash_balance is not None else None,
            new_value     = round(new_cash, 4),
            reason        = "Cash balance reconstructed from transaction ledger",
        ))

    # ── PortfolioItem rows ────────────────────────────────────────────────────
    current_items = {
        item.symbol: item
        for item in db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id).all()
    }
    # Re-keyed by report_symbol — see _reconcile_portfolio_items's identical
    # comment (TDD Stage 4: `final_state.holdings`'s own key is an int under
    # native keying, never a valid PortfolioItem.symbol value).
    final_items  = {h.report_symbol: h for h in final_state.holdings.values()}
    final_syms   = set(final_items)
    current_syms = set(current_items)
    updated_syms: set[str] = set()   # symbols with ≥1 changed field

    for sym in sorted(final_syms & current_syms):
        h          = final_items[sym]
        curr       = current_items[sym]
        new_shares = _f(h.shares)
        new_avg    = _f(h.avg_cost)

        if _values_differ(curr.shares, new_shares, tol=0.0001):
            updated_syms.add(sym)
            ops.append(PlanOperation(
                table         = "PortfolioItem",
                operation     = "UPDATE",
                object_id     = sym,
                field         = "shares",
                current_value = round(curr.shares, 6) if curr.shares is not None else None,
                new_value     = round(new_shares, 6),
                reason        = "Reconstructed from transaction ledger",
            ))

        if _values_differ(curr.avg_cost, new_avg, tol=0.01):
            updated_syms.add(sym)
            ops.append(PlanOperation(
                table         = "PortfolioItem",
                operation     = "UPDATE",
                object_id     = sym,
                field         = "avg_cost",
                current_value = round(curr.avg_cost, 6) if curr.avg_cost is not None else None,
                new_value     = round(new_avg, 6),
                reason        = "Reconstructed from transaction ledger",
            ))

    for sym in sorted(final_syms - current_syms):
        h = final_items[sym]
        ops.append(PlanOperation(
            table         = "PortfolioItem",
            operation     = "INSERT",
            object_id     = sym,
            field         = None,
            current_value = None,
            new_value     = {
                "shares":   _f(h.shares),
                "avg_cost": _f(h.avg_cost),
                "sector":   h.sector,
            },
            reason        = "Symbol found in transaction ledger but absent from PortfolioItem",
        ))

    for sym in sorted(current_syms - final_syms):
        curr = current_items[sym]
        ops.append(PlanOperation(
            table         = "PortfolioItem",
            operation     = "DELETE",
            object_id     = sym,
            field         = None,
            current_value = {"shares": curr.shares, "avg_cost": curr.avg_cost},
            new_value     = None,
            reason        = "Symbol absent from replayed final holdings; position fully closed",
        ))

    # ── PortfolioSnapshot rows ─────────────────────────────────────────────────
    snap_inserts = 0
    snap_updates = 0

    if not skip_snapshots:
        snap_q = db.query(PortfolioSnapshot).filter_by(portfolio_id=portfolio_id)
        if from_date:
            snap_q = snap_q.filter(PortfolioSnapshot.snapshot_date >= from_date)
        current_snaps = {s.snapshot_date: s for s in snap_q.all()}

        for day in snapshot_days:
            existing = current_snaps.get(day.snapshot_date)
            if existing:
                ops.append(PlanOperation(
                    table         = "PortfolioSnapshot",
                    operation     = "UPSERT",
                    object_id     = day.snapshot_date,
                    field         = None,
                    current_value = {
                        "total_value":  existing.total_value,
                        "cash_balance": existing.cash_balance,
                    },
                    new_value     = {
                        "total_value":  day.total_value,
                        "cash_balance": day.cash_balance,
                    },
                    reason        = "Historical snapshot reconstructed from transaction replay",
                ))
                snap_updates += 1
            else:
                ops.append(PlanOperation(
                    table         = "PortfolioSnapshot",
                    operation     = "INSERT",
                    object_id     = day.snapshot_date,
                    field         = None,
                    current_value = None,
                    new_value     = {
                        "total_value":  day.total_value,
                        "cash_balance": day.cash_balance,
                    },
                    reason        = "Missing historical snapshot; reconstructed from transaction replay",
                ))
                snap_inserts += 1

    # ── Summary ────────────────────────────────────────────────────────────────
    n_item_inserts = len(final_syms - current_syms)
    n_item_updates = len(updated_syms)
    n_item_deletes = len(current_syms - final_syms)

    summary = PlanSummary(
        portfolio_updated_fields = tuple(port_updated_fields),
        item_inserts             = n_item_inserts,
        item_updates             = n_item_updates,
        item_deletes             = n_item_deletes,
        snapshot_inserts         = snap_inserts,
        snapshot_updates         = snap_updates,
        snapshot_deletes         = 0,
        total_write_operations   = (
            len(port_updated_fields)
            + n_item_inserts + n_item_updates + n_item_deletes
            + snap_inserts + snap_updates
        ),
        validator_critical = len(validator.criticals) if validator else 0,
        validator_errors   = len(validator.errors)    if validator else 0,
        validator_warnings = len(validator.warnings)  if validator else 0,
        confidence_score   = confidence.overall,
    )

    return ReconstructionPlan(
        portfolio_id      = portfolio_id,
        confidence_score  = confidence.overall,
        validator_passed  = (validator is None or len(validator.criticals) == 0),
        critical_findings = len(validator.criticals) if validator else 0,
        operations        = tuple(ops),
        summary           = summary,
        generated_at      = datetime.utcnow().isoformat() + "Z",
    )


# ──────────────────────────────────────────────────────────────────────────────
# Stage 8 — Atomic commit
# ──────────────────────────────────────────────────────────────────────────────

def _snap_day_to_db_dict(day: _SnapshotDay) -> dict:
    """Convert a _SnapshotDay to a dict of PortfolioSnapshot column values."""
    return {
        "total_value":              day.total_value,
        "cash_balance":             day.cash_balance,
        "total_invested":           day.total_invested,
        "unrealized_pnl":           day.unrealized_pnl,
        "unrealized_pnl_pct":       day.unrealized_pnl_pct,
        "realized_pnl":             day.realized_pnl,
        "daily_return_pct":         day.daily_return_pct,
        "net_external_cash_flow":   day.net_external_cash_flow,
        "investment_return_pct":    day.investment_return_pct,
        "investment_return_amount": day.investment_return_amount,
        "imported_asset_value":     day.imported_asset_value,
        "manual_adjustment_value":  day.manual_adjustment_value,
        "period_realized_pnl":      day.period_realized_pnl,
        "period_dividend_income":   day.period_dividend_income,
        "period_fees_paid":         day.period_fees_paid,
        "sector_breakdown_json":    day.sector_breakdown_json,
        "holdings_json":            day.holdings_json,
        "holdings_count":           day.holdings_count,
    }


def _commit_rebuild(
    db:                    Session,
    portfolio_id:          int,
    workspace_id:          int,
    portfolio:             Portfolio,
    final_state:           _PortfolioState,
    snapshot_days:         list[_SnapshotDay],
    skip_snapshots:        bool,
    conversion_successors: dict[int, _ConversionSuccessorBinding] | None = None,
) -> None:
    """Write the reconstructed state to the database atomically.

    Caller is responsible for calling db.commit() / db.rollback().
    This function performs NO commit — it only stages ORM changes.

    conversion_successors (BANPU-WP2 Step 5): asset_id preservation is scoped
    to conversion-bearing rebuilds only (Implementation Specification §8 /
    governance scope note — lossless for THIS portfolio's conversion, not a
    general registry backfill).  The mapping is keyed by conversion
    transaction ID; the symbol-grouped view is used only to bind the final
    materialized successor identity. When empty (the overwhelming majority of
    rebuilds — no POSITION_CONVERSION in the ledger), commit behavior is
    byte-identical to before Step 5: every inserted PortfolioItem gets
    asset_id=None, exactly the pre-existing behavior.
    """
    conversion_by_symbol = _conversion_successors_by_symbol(conversion_successors)
    is_conversion_bearing = bool(conversion_by_symbol)

    # ── 1. Update Portfolio.cash_balance ─────────────────────────────────────
    portfolio.cash_balance = _f(final_state.cash_balance)

    # ── 2. Replace PortfolioItem rows ─────────────────────────────────────────
    # Deterministic pre-delete preservation map, keyed by the current stored
    # symbol — an existing DB-constraint-backed unique key
    # (uq_portfolio_symbol) per portfolio, so a duplicate/ambiguous key here
    # can only mean a data-integrity anomaly, never legitimate ledger state;
    # fail closed rather than guess. Captures allow_swap (pre-existing
    # behavior, unconditional) and asset_id (Step 5, conversion-scoped only).
    existing_items_by_symbol: dict[str, PortfolioItem] = {}
    for item in db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id).all():
        if item.symbol in existing_items_by_symbol:
            raise RuntimeError(
                f"PortfolioItem preservation key ambiguous: portfolio_id={portfolio_id} "
                f"symbol={item.symbol!r} — uq_portfolio_symbol should make this unreachable"
            )
        existing_items_by_symbol[item.symbol] = item

    db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id).delete(
        synchronize_session=False
    )

    for h in final_state.holdings.values():
        # Always report_symbol, never the internal merge key `h.symbol` — the
        # latter is an int (asset_id) under native keying, and
        # PortfolioItem.symbol is a String column (TDD Stage 4; see
        # _HoldingState's own docstring).
        existing = existing_items_by_symbol.get(h.report_symbol)

        if h.report_symbol in conversion_by_symbol:
            # Authoritative binding — never the preserved value for this
            # symbol, which (per _resolve_conversion_successors) is either
            # absent, already correct, or legitimately NULL pre-commit.  All
            # dated bindings for one shared successor carry the same ID.
            asset_id = conversion_by_symbol[h.report_symbol][0].successor_asset_id
        elif is_conversion_bearing:
            asset_id = existing.asset_id if existing else None
        else:
            # No-conversion rebuild — unchanged pre-Step-5 behavior.
            asset_id = None

        db.add(PortfolioItem(
            workspace_id = workspace_id,
            portfolio_id = portfolio_id,
            symbol       = h.report_symbol,
            shares       = _f(h.shares),
            avg_cost     = _f(h.avg_cost),
            sector       = h.sector,
            allow_swap   = existing.allow_swap if existing else True,
            asset_id     = asset_id,
        ))

    # ── 3. Upsert snapshot rows ────────────────────────────────────────────────
    if not skip_snapshots:
        for day in snapshot_days:
            if day.holdings_count > 0 and day.price_coverage < _COVERAGE_THRESHOLD:
                _log.warning(
                    "rebuild: snapshot %s coverage=%.0f%% < %.0f%% — writing anyway "
                    "(price_missing=True for affected holdings)",
                    day.snapshot_date,
                    day.price_coverage * 100,
                    _COVERAGE_THRESHOLD * 100,
                )

            # ── FORENSIC COMMIT PRE-WRITE ─────────────────────────────────
            existing  = (
                db.query(PortfolioSnapshot)
                .filter_by(portfolio_id=portfolio_id, snapshot_date=day.snapshot_date)
                .first()
            )
            print(
                f"[FORENSIC COMMIT PRE]  snap_date={day.snapshot_date}"
                f"  {'existing.id=' + str(existing.id) if existing else 'INSERT'}"
                f"  total_value={day.total_value}"
                f"  cash={day.cash_balance}"
                f"  holdings_count={day.holdings_count}"
                f"  holdings_json[:500]={day.holdings_json[:500]}"
                f"  investment_return_pct={day.investment_return_pct}"
            )
            snap_data = _snap_day_to_db_dict(day)
            if existing:
                for k, v in snap_data.items():
                    setattr(existing, k, v)
                # ── FORENSIC COMMIT POST-SETATTR ──────────────────────────
                print(
                    f"[FORENSIC COMMIT POST] snap_date={existing.snapshot_date}"
                    f"  total_value={existing.total_value}"
                    f"  cash={existing.cash_balance}"
                    f"  holdings_json[:500]={str(existing.holdings_json)[:500]}"
                )
            else:
                db.add(PortfolioSnapshot(
                    workspace_id  = workspace_id,
                    portfolio_id  = portfolio_id,
                    snapshot_date = day.snapshot_date,
                    **snap_data,
                ))


# ── Stage R1 runtime consultation (M30.3 brief; third portfolio-domain
# shadow consumer, after portfolio_snapshots.py (M30.2)) ────────────────────
#
# Two legacy assumptions in this module's replay engine have no capability
# gate today (M29 audit, SR-1 finding):
#   1. `market_value = shares × price` is computed for every held symbol
#      once historical snapshots are built — see _build_snapshot_day().
#   2. DIVIDEND transactions are folded into cash_balance unconditionally
#      during replay — see _apply_transaction()'s cash-inflow branch.
# This function asks the runtime the same two questions legacy logic already
# answers implicitly, and records any disagreement as a shadow finding —
# mirrors portfolio_snapshots._consult_runtime_for_snapshot() (M30.2)
# exactly: read-only, never raises, never gates, never changes any computed
# value. Deliberately NOT wired into _apply_transaction() itself — that
# function is a pure in-memory replay step called once per transaction
# (including inside _replay_with_date_snapshots()'s per-date loop), so a
# per-call DB-backed consultation there would be both a purity violation and
# a performance regression. Consulted once here instead, after Stage 1
# replay has already produced `final_state` and `all_txs`.
#
# `binding` on each finding is the holding's symbol, not an Asset Definition
# binding spelling — CapabilityView is deliberately anonymous (D5).
def _consult_runtime_for_rebuild(
    db: Session,
    final_state: _PortfolioState,
    all_txs: list[CanonicalTransaction],
    skip_snapshots: bool,
) -> RuntimeConsultationLog:
    """Never raises — resolve_capability_views() already turns an unminted
    symbol, an undefined asset_type, or a registry boot failure into an
    UnresolvedCapability per symbol rather than an exception; this function
    just turns that into a MISSING_BINDING finding, same as the other
    Stage R1 consumers.
    """
    dividend_tx_ids_by_symbol: dict[str, list[int]] = {}
    for ctx in all_txs:
        if ctx.transaction_type == "DIVIDEND" and ctx.raw_symbol:
            dividend_tx_ids_by_symbol.setdefault(
                ctx.raw_symbol.strip().upper(), []
            ).append(ctx.id)

    # market_value = shares × price is only ever computed when snapshots are
    # actually built (Stage 2); with skip_snapshots=True, no valuation
    # formula runs at all, so there is nothing to shadow-check.
    valuation_symbols: dict[str, str] = {}  # normalized symbol -> report_symbol
    if not skip_snapshots:
        for h in final_state.holdings.values():
            valuation_symbols[h.report_symbol.strip().upper()] = h.report_symbol

    lookup_symbols = sorted(set(valuation_symbols) | set(dividend_tx_ids_by_symbol))
    if not lookup_symbols:
        return RuntimeConsultationLog(consulted=0, agreements=0, findings=())

    views = capability_lookup_service.resolve_capability_views(db, lookup_symbols)

    findings: list[RuntimeValidationFinding] = []
    consulted  = 0
    agreements = 0

    # ── 1. market_value = shares × price ⇔ runtime permits quantity valuation ──
    for normalized, report_symbol in valuation_symbols.items():
        consulted += 1
        legacy_result = True  # replay computes market_value = shares × price unconditionally
        view = views[normalized]
        if isinstance(view, UnresolvedCapability):
            findings.append(RuntimeValidationFinding(
                category=RuntimeFindingCategory.MISSING_BINDING.value,
                check_id="RUNTIME_REBUILD_QUANTITY_VALUATION", transaction_ids=(),
                binding=report_symbol, question="permits_quantity_valuation()",
                legacy_result=legacy_result, runtime_result=None, detail=view.reason,
            ))
            continue
        runtime_result = permits_quantity_valuation(view)
        if runtime_result == legacy_result:
            agreements += 1
        else:
            findings.append(RuntimeValidationFinding(
                category=RuntimeFindingCategory.RUNTIME_MISMATCH.value,
                check_id="RUNTIME_REBUILD_QUANTITY_VALUATION", transaction_ids=(),
                binding=report_symbol, question="permits_quantity_valuation()",
                legacy_result=legacy_result, runtime_result=runtime_result,
                detail=(
                    f"rebuild replay computes market_value = shares × price for "
                    f"{report_symbol!r} unconditionally, but the runtime "
                    "capability view does not permit quantity-based valuation "
                    "for this asset."
                ),
            ))

    # ── 2. DIVIDEND transaction accepted ⇔ runtime grants FlowType.DIVIDEND ────
    for symbol, tx_ids in dividend_tx_ids_by_symbol.items():
        consulted += 1
        tx_ids_tuple = tuple(tx_ids)
        legacy_result = True  # replay credits cash_balance for DIVIDEND unconditionally
        view = views[symbol]
        if isinstance(view, UnresolvedCapability):
            findings.append(RuntimeValidationFinding(
                category=RuntimeFindingCategory.MISSING_BINDING.value,
                check_id="RUNTIME_REBUILD_DIVIDEND_FLOW", transaction_ids=tx_ids_tuple,
                binding=symbol, question="grants_dividend_flow()",
                legacy_result=legacy_result, runtime_result=None, detail=view.reason,
            ))
            continue
        runtime_result = grants_dividend_flow(view)
        if runtime_result == legacy_result:
            agreements += 1
        else:
            findings.append(RuntimeValidationFinding(
                category=RuntimeFindingCategory.RUNTIME_MISMATCH.value,
                check_id="RUNTIME_REBUILD_DIVIDEND_FLOW", transaction_ids=tx_ids_tuple,
                binding=symbol, question="grants_dividend_flow()",
                legacy_result=legacy_result, runtime_result=runtime_result,
                detail=(
                    f"{len(tx_ids_tuple)} DIVIDEND transaction(s) for {symbol!r} "
                    "are credited to cash_balance by rebuild replay "
                    "unconditionally, but the runtime capability view does not "
                    "grant FlowType.DIVIDEND for this asset."
                ),
            ))

    return RuntimeConsultationLog(consulted=consulted, agreements=agreements, findings=tuple(findings))


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

async def rebuild_portfolio(
    db:             Session,
    portfolio_id:   int,
    workspace_id:   int,
    from_date:      str | None = None,
    skip_snapshots: bool       = False,
    skip_benchmark: bool       = False,   # reserved for future benchmark series rebuild
    dry_run:        bool       = False,
    backup:         bool       = False,
    apply_repairs:  bool       = True,
    progress_cb:    Callable[[str], None] | None = None,
) -> RebuildResult:
    """Rebuild a portfolio from its transaction ledger.

    Stages
    ------
    1. Replay all transactions → final cash + holdings + realized P/L
       When apply_repairs=True, loads active LedgerRepair rows and applies
       apply_repair_overlay() before replay so excluded transactions are
       invisible to every downstream stage.
    2. Reconstruct historical portfolio state at each existing snapshot date
    3. Recalculate return metrics for each snapshot
    4. Generate a reconciliation report (current DB vs reconstructed)
    5. Run ledger validator — abort commit if any CRITICAL finding is present
       + compute multi-dimensional ConfidenceReport
       When apply_repairs=True, validates the effective ledger (mode="effective").
    6. Generate the execution plan (deterministic, read-only list of DB changes)
    7. Export pre-rebuild backup (when backup=True and not dry_run)
       — backup failure aborts the commit
    8. Commit (atomically) unless dry_run=True or Stage 5 aborted

    Args:
        db:             SQLAlchemy session (caller manages lifecycle).
        portfolio_id:   ID of the portfolio to rebuild.
        workspace_id:   Owning workspace ID.
        from_date:      "YYYY-MM-DD".  Only rebuild snapshots on/after this date.
                        Stage 1 (final state) always replays all transactions.
        skip_snapshots: Skip Stages 2–3 (only rebuild portfolio items + cash).
        skip_benchmark: (reserved) Skip benchmark series regeneration.
        dry_run:        Run all stages but do not write to the database.
        backup:         Export existing rows to JSON before committing (Stage 7).
                        If the export fails, the commit is aborted.
        apply_repairs:  When True (default), load active LedgerRepair rows and
                        apply the repair overlay before replay.  Excluded
                        transactions are omitted from every downstream stage
                        including validation and confidence scoring.
                        When False, behaviour is identical to Phase 6.7B.
        progress_cb:    Optional callable(message) for progress reporting.

    Returns:
        RebuildResult with per-stage statistics, reconciliation report,
        multi-dimensional ConfidenceReport, and execution plan.
        result.aborted=True means a CRITICAL ledger finding or backup failure
        blocked the commit.
    """
    t_start = time.monotonic()

    def _progress(msg: str) -> None:
        if progress_cb:
            progress_cb(msg)
        _log.info("rebuild portfolio=%d: %s", portfolio_id, msg)

    # ── Load portfolio ────────────────────────────────────────────────────────
    portfolio = (
        db.query(Portfolio)
        .filter_by(id=portfolio_id, workspace_id=workspace_id)
        .first()
    )
    if not portfolio:
        return RebuildResult(
            portfolio_id   = portfolio_id,
            portfolio_name = "?",
            success        = False,
            error          = f"Portfolio {portfolio_id} not found in workspace {workspace_id}",
        )

    result = RebuildResult(
        portfolio_id   = portfolio_id,
        portfolio_name = portfolio.name,
        success        = False,
        dry_run        = dry_run,
        from_date      = from_date,
        skip_snapshots = skip_snapshots,
    )

    try:
        # ── Load all transactions ──────────────────────────────────────────────
        raw_txs: list[Transaction] = (
            db.query(Transaction)
            .filter_by(portfolio_id=portfolio_id)
            .order_by(Transaction.transaction_date, Transaction.id)
            .all()
        )

        if not raw_txs:
            result.error = "No transactions found — nothing to rebuild"
            return result

        # M5 Track B Stage 4: per-portfolio replay cutover gate (never global —
        # TDD §9). NULL/False (the default) reproduces every pre-Stage-4 replay
        # exactly; only a portfolio whose flag has been explicitly flipped ON
        # (services/replay_cutover.py, after proving bit-identical parity)
        # gets asset_id-preferring keying.
        canonical_txs: list[CanonicalTransaction] = list(
            canonicalize_transactions(raw_txs, prefer_asset_id=bool(portfolio.replay_asset_id_native))
        )
        raw_canonical_count = len(canonical_txs)

        # ── BANPU-WP2 Step 3: POSITION_CONVERSION preflight ────────────────────
        # Runs once, on the raw (un-repaired) canonical list, before either
        # replay site and before the repair overlay below — so a repair can
        # never make an invalid conversion look valid. A failure here aborts
        # the whole rebuild before any replay or database mutation.
        _preflight_position_conversions(raw_txs, canonical_txs)

        # ── Repair overlay (Phase 6.7C) ────────────────────────────────────────
        active_repairs: list = []
        if apply_repairs:
            active_repairs = load_active_repairs(db, portfolio_id)
            if active_repairs:
                effective_tuple, provenance_map = apply_repair_overlay(
                    tuple(canonical_txs), active_repairs
                )
                excluded_count = sum(
                    1 for v in provenance_map.values() if v == "EXCLUDED"
                )
                all_txs = list(effective_tuple)
                result.repairs_applied            = excluded_count
                result.excluded_transaction_count = excluded_count
                result.repair_ids                 = [r.id for r in active_repairs]
                excluded_tx_ids = sorted(
                    tx_id for tx_id, prov in provenance_map.items()
                    if prov == "EXCLUDED"
                )
                # Phase 6.7G diagnostic — printed unconditionally so the
                # effective-ledger state is always visible before replay.
                print(
                    f"[PIPELINE] raw={raw_canonical_count}  "
                    f"repairs(rows)={len(active_repairs)}  "
                    f"excluded={excluded_count}  "
                    f"effective={len(all_txs)}"
                )
                if excluded_tx_ids:
                    print(f"[PIPELINE] excluded tx IDs: {excluded_tx_ids}")
                if excluded_count:
                    _progress(
                        f"Stage 1: overlay applied — "
                        f"raw={raw_canonical_count}  "
                        f"repairs_applied={excluded_count}  "
                        f"effective={len(all_txs)}"
                    )
            else:
                all_txs = canonical_txs
        else:
            all_txs = canonical_txs

        # A LedgerRepair EXCLUDE targeting a POSITION_CONVERSION row is
        # ineffective — the conversion is authoritative regardless of
        # apply_repairs or any repair overlay (§7.1). This is a no-op when
        # apply_repairs=False or no repair touched a conversion row.
        all_txs = _reinstate_excluded_conversions(all_txs, canonical_txs)

        result.effective_transaction_count = len(all_txs)
        result.transactions_replayed = len(all_txs)
        _progress(f"Stage 1: replaying {len(all_txs)} transactions...")

        # ── Stage 1: single-pass replay → final state ─────────────────────────
        final_state = _PortfolioState(Decimal("0"), {}, Decimal("0"))
        print("========================")
        print("Replay Start")
        print("portfolio =", portfolio_id)
        print("initial holdings =", final_state.holdings)
        print("id =", id(final_state.holdings))

        conversion_seen: set = set()   # Stage 1's own fresh duplicate-tracking set (Step 3)
        for ctx in all_txs:
            _apply_transaction(final_state, ctx, conversion_seen=conversion_seen)
            print(ctx)
            # print(ctx.id, ctx.transaction_type, ctx.symbol)            

        print(final_state.holdings.keys())
        result.reconstructed_holdings_count = len(final_state.holdings)
        result.reconstructed_cash           = _f(final_state.cash_balance)
        _progress(
            f"  → cash={result.reconstructed_cash:,.2f}  "
            f"holdings={result.reconstructed_holdings_count}"
        )

        # ── BANPU-WP2 Step 5: conversion successor materialization identity ────
        # Resolved once, right after Stage 1 replay succeeds and before any
        # reconciliation or persistent mutation — Stage 4 and Stage 8 below
        # both consume this same already-validated pairing rather than each
        # re-deriving it. Empty for every no-conversion rebuild (the common
        # case). Raises fail-closed on a genuine stored-identity conflict or
        # ambiguity, aborting before any reconciliation row or DB write.
        conversion_successors = _resolve_conversion_successors(db, portfolio_id, all_txs)

        # ── Stages 2–3: historical snapshots ──────────────────────────────────
        snapshot_days: list[_SnapshotDay] = []

        if not skip_snapshots:
            existing_snaps: list[PortfolioSnapshot] = (
                db.query(PortfolioSnapshot)
                .filter_by(portfolio_id=portfolio_id)
                .order_by(PortfolioSnapshot.snapshot_date)
                .all()
            )

            if from_date:
                rebuild_dates  = [s.snapshot_date for s in existing_snaps
                                   if s.snapshot_date >= from_date]
                prev_db_snap   = next(
                    (s for s in reversed(existing_snaps) if s.snapshot_date < from_date),
                    None,
                )
            else:
                rebuild_dates = [s.snapshot_date for s in existing_snaps]
                prev_db_snap  = None

            if not rebuild_dates:
                _progress("  → no snapshot dates in rebuild window; skipping Stages 2–3")
            else:
                _progress(
                    f"Stage 2: rebuilding {len(rebuild_dates)} snapshots "
                    f"({rebuild_dates[0]} → {rebuild_dates[-1]})..."
                )

                # Collect all symbols that appear in the rebuild window.
                # Use price_symbol (DR-safe raw form), not the holdings dict
                # key (ReplayKey) — canonical_symbol collapses DR certificates
                # to their US underlying ticker, which _build_price_matrix's
                # is_dr() branch must not receive (see _HoldingState.price_symbol).
                all_symbols: set[str] = {
                    (h.price_symbol or sym) for sym, h in final_state.holdings.items()
                }
                for snap in existing_snaps:
                    if snap.snapshot_date in set(rebuild_dates) and snap.holdings_json:
                        try:
                            for h in json.loads(snap.holdings_json):
                                sym = h.get("symbol")
                                if sym:
                                    all_symbols.add(sym)
                        except (ValueError, TypeError):
                            pass

                _progress(
                    f"  → fetching historical prices for {len(all_symbols)} symbol(s)..."
                )
                print(sorted(all_symbols))
                price_matrix = await _build_price_matrix(
                    symbols     = sorted(all_symbols),
                    dates       = rebuild_dates,
                    progress_cb = lambda sym: _progress(f"    price: {sym}"),
                )
                print(">>> BUILD PRICE MATRIX FINISHED <<<")

                # Replay transactions to get portfolio state at each snapshot date
                _progress("  → replaying transactions for each snapshot date...")
                state_by_date = _replay_with_date_snapshots(all_txs, rebuild_dates)

                # Build _SnapshotDay objects with NAV + return fields
                prev_snap_day: _SnapshotDay | None = None
                print("===== BEFORE LOOP =====")
                for snap_date in rebuild_dates:
                    print("LOOP", snap_date)
                    state_at = state_by_date.get(snap_date)
                    if state_at is None:
                        _log.warning(
                            "rebuild: no state for portfolio=%d date=%s",
                            portfolio_id, snap_date,
                        )
                        continue

                    # price_row stays keyed by the holdings dict key (ReplayKey)
                    # for _build_snapshot_day; the price_matrix lookup itself
                    # uses each holding's DR-safe price_symbol.
                    price_row = {
                        sym: price_matrix.get(h.price_symbol or sym, {}).get(snap_date)
                        for sym, h in state_at.holdings.items()
                    }

                    # Determine the "previous" for return calculation
                    if prev_snap_day is not None:
                        prev_date = prev_snap_day.snapshot_date
                        prev_nav  = prev_snap_day.total_value
                    elif prev_db_snap is not None:
                        prev_date = prev_db_snap.snapshot_date
                        prev_nav  = prev_db_snap.total_value
                    else:
                        prev_date = None
                        prev_nav  = None

                    day = _build_snapshot_day(
                        snapshot_date = snap_date,
                        state         = state_at,
                        price_row     = price_row,
                        all_txs       = all_txs,
                        prev_date     = prev_date,
                        prev_nav      = prev_nav,
                    )

                    # ── FORENSIC POST-BUILD ───────────────────────────────────
                    print(
                        f"[FORENSIC POST-BUILD] snap_date={day.snapshot_date}"
                        f"  holdings_count={day.holdings_count}"
                        f"  id(day)={id(day)}"
                        f"  holdings_json[:500]={day.holdings_json[:500]}"
                        f"  investment_return_pct={day.investment_return_pct}"
                    )

                    snapshot_days.append(day)
                    prev_snap_day = day
                    # Once we have our first reconstructed snapshot, drop the DB baseline
                    if prev_db_snap is not None:
                        prev_db_snap = None

                result.snapshots_processed            = len(snapshot_days)
                result.snapshots_skipped_low_coverage = sum(
                    1 for d in snapshot_days
                    if d.holdings_count > 0 and d.price_coverage < _COVERAGE_THRESHOLD
                )
                _progress(
                    f"  → processed {result.snapshots_processed} snapshot(s), "
                    f"{result.snapshots_skipped_low_coverage} with low coverage"
                )

        # ── Stage 4: reconciliation ───────────────────────────────────────────
        _progress("Stage 4: reconciling...")

        recon_rows: list[ReconciliationRow] = []
        recon_rows.extend(
            _reconcile_portfolio_items(db, portfolio_id, final_state, conversion_successors)
        )
        if not skip_snapshots and snapshot_days:
            recon_rows.extend(
                _reconcile_snapshots(db, portfolio_id, snapshot_days, from_date)
            )

        result.reconciliation_report = recon_rows

        item_rows = [r for r in recon_rows if r.entity_type == "portfolio_item"]
        snap_rows = [r for r in recon_rows if r.entity_type == "snapshot"]

        result.items_matched    = sum(1 for r in item_rows if r.status == ReconciliationStatus.MATCH)
        result.items_different  = sum(1 for r in item_rows if r.status == ReconciliationStatus.DIFFERENT)
        result.items_missing    = sum(1 for r in item_rows if r.status == ReconciliationStatus.MISSING)
        result.items_extra      = sum(1 for r in item_rows if r.status == ReconciliationStatus.EXTRA)

        result.snapshots_matched   = sum(1 for r in snap_rows if r.status == ReconciliationStatus.MATCH)
        result.snapshots_different = sum(1 for r in snap_rows if r.status == ReconciliationStatus.DIFFERENT)
        result.snapshots_missing   = sum(1 for r in snap_rows if r.status == ReconciliationStatus.MISSING)
        result.snapshots_extra     = sum(1 for r in snap_rows if r.status == ReconciliationStatus.EXTRA)

        # ── Stage 5: ledger validation gate ───────────────────────────────────
        _progress("Stage 5: validating ledger...")
        if apply_repairs:
            validation_report = await validate_portfolio_ledger(
                db           = db,
                portfolio_id = portfolio_id,
                workspace_id = workspace_id,
                repairs      = active_repairs,
                mode         = "effective",
            )
        else:
            validation_report = await validate_portfolio_ledger(
                db           = db,
                portfolio_id = portfolio_id,
                workspace_id = workspace_id,
            )
        result.validator_report  = validation_report
        result.ledger_criticals  = len(validation_report.criticals)
        result.ledger_errors     = len(validation_report.errors)
        result.ledger_warnings   = len(validation_report.warnings)

        # BANPU-WP2 Step 5: POSITION_CONVERSION_SAME_DAY_CONFLICT is the one
        # WP2-catalogued finding with a fixed ERROR severity that must still
        # block commit (§7.1/§9) — every other ERROR finding keeps the
        # existing (non-blocking) policy unchanged.
        conversion_blocking_error = _has_conversion_blocking_error(validation_report)

        if result.ledger_criticals > 0 or conversion_blocking_error:
            result.aborted = True
            if conversion_blocking_error and result.ledger_criticals == 0:
                _progress(
                    "  → ABORTED: POSITION_CONVERSION_SAME_DAY_CONFLICT (ERROR) — "
                    "commit blocked despite non-CRITICAL severity"
                )
            else:
                _progress(
                    f"  → ABORTED: {result.ledger_criticals} CRITICAL finding(s) — "
                    "commit blocked until ledger is corrected"
                )
        else:
            _progress(
                f"  → clean  (C={result.ledger_criticals} "
                f"E={result.ledger_errors} "
                f"W={result.ledger_warnings})"
            )

        # ── Stage 5 (cont.): confidence report ────────────────────────────────
        conf_report = _compute_confidence_report(result, snapshot_days)
        result.confidence_report = conf_report
        result.confidence_score  = conf_report.overall
        _progress(
            f"  → confidence {conf_report.overall:.1f}%  "
            f"(replay={conf_report.replay_confidence:.0f}% "
            f"ledger={conf_report.ledger_integrity:.0f}% "
            f"coverage={conf_report.historical_coverage:.0f}% "
            f"consistency={conf_report.snapshot_consistency:.0f}% "
            f"validator={conf_report.validator_confidence:.0f}%)"
        )

        # ── Stage 6: execution plan ────────────────────────────────────────────
        _progress("Stage 6: generating execution plan...")
        if result.excluded_transaction_count > 0:
            _progress(
                f"  → transaction summary  "
                f"raw={raw_canonical_count}  "
                f"repairs_applied={result.repairs_applied}  "
                f"effective={result.effective_transaction_count}"
            )
        exec_plan = _generate_execution_plan(
            db             = db,
            portfolio_id   = portfolio_id,
            portfolio      = portfolio,
            final_state    = final_state,
            snapshot_days  = snapshot_days,
            from_date      = from_date,
            confidence     = conf_report,
            validator      = result.validator_report,
            skip_snapshots = skip_snapshots,
        )
        result.execution_plan = exec_plan
        s = exec_plan.summary
        _progress(
            f"  → {s.total_write_operations} write operation(s) planned  "
            f"(items: +{s.item_inserts} ~{s.item_updates} -{s.item_deletes}  "
            f"snapshots: +{s.snapshot_inserts} ~{s.snapshot_updates})"
        )

        # ── Stage R1 runtime consultation (M30.3; read-only shadow, never
        # raises, never affects any value computed above or the
        # RebuildResult returned below) ────────────────────────────────────
        try:
            runtime_log = _consult_runtime_for_rebuild(db, final_state, all_txs, skip_snapshots)
        except Exception as exc:
            _log.warning(
                "runtime consultation failed for rebuild portfolio=%d: %s",
                portfolio_id, exc,
            )
        else:
            for finding in runtime_log.findings:
                _log.warning(
                    "runtime consultation finding on rebuild: check_id=%s category=%s "
                    "binding=%s detail=%s",
                    finding.check_id, finding.category, finding.binding, finding.detail,
                )

        # ── Stage 7: pre-commit backup ─────────────────────────────────────────
        if backup and not dry_run and not result.aborted:
            _progress("Stage 7: exporting backup...")
            try:
                result.backup_path = _export_backup(db, portfolio_id)
                _progress(f"  → backup written: {result.backup_path}")
            except Exception as backup_exc:
                _log.error(
                    "rebuild backup failed portfolio=%d: %s", portfolio_id, backup_exc
                )
                result.aborted = True
                result.error   = f"Backup failed (commit aborted): {backup_exc}"
                _progress(f"  → ABORTED: backup failed: {backup_exc}")

        # ── Stage 8: atomic commit ─────────────────────────────────────────────
        if not dry_run and not result.aborted:
            _progress("Stage 8: committing...")
            try:
                _commit_rebuild(
                    db                    = db,
                    portfolio_id          = portfolio_id,
                    workspace_id          = workspace_id,
                    portfolio             = portfolio,
                    final_state           = final_state,
                    snapshot_days         = snapshot_days,
                    skip_snapshots        = skip_snapshots,
                    conversion_successors = conversion_successors,
                )
                db.commit()
                result.committed = True
                _progress("  → committed successfully")
            except Exception as commit_exc:
                db.rollback()
                result.error = f"Commit failed (rolled back): {commit_exc}"
                _log.exception(
                    "rebuild commit failed portfolio=%d", portfolio_id
                )
                return result
        elif result.aborted:
            _progress("  → skipped: CRITICAL validator findings or backup failure blocked commit")
        else:
            _progress("  → dry-run: no database changes written")

        result.success = True

    except Exception as exc:
        _log.exception("rebuild_portfolio failed portfolio=%d", portfolio_id)
        result.error = str(exc)
        if not dry_run:
            try:
                db.rollback()
            except Exception:
                pass

    finally:
        result.elapsed_seconds = time.monotonic() - t_start

    return result


async def rebuild_all_portfolios(
    db:             Session,
    workspace_id:   int,
    from_date:      str | None = None,
    skip_snapshots: bool       = False,
    skip_benchmark: bool       = False,
    dry_run:        bool       = False,
    backup:         bool       = False,
    apply_repairs:  bool       = True,
    progress_cb:    Callable[[int, str, str], None] | None = None,
) -> list[RebuildResult]:
    """Rebuild every portfolio in a workspace.

    Args:
        apply_repairs:  Passed through to rebuild_portfolio().  When True
                        (default), active LedgerRepair rows are applied as an
                        overlay before each portfolio is replayed.
        progress_cb: Optional callable(portfolio_id, portfolio_name, message).
    """
    portfolios = (
        db.query(Portfolio)
        .filter_by(workspace_id=workspace_id)
        .order_by(Portfolio.id)
        .all()
    )

    if not portfolios:
        _log.warning("rebuild_all: no portfolios found in workspace %d", workspace_id)
        return []

    results: list[RebuildResult] = []

    for p in portfolios:
        _log.info("rebuild_all: starting portfolio=%d name=%s", p.id, p.name)

        def _cb(msg: str) -> None:
            if progress_cb:
                progress_cb(p.id, p.name, msg)

        r = await rebuild_portfolio(
            db             = db,
            portfolio_id   = p.id,
            workspace_id   = workspace_id,
            from_date      = from_date,
            skip_snapshots = skip_snapshots,
            skip_benchmark = skip_benchmark,
            dry_run        = dry_run,
            backup         = backup,
            apply_repairs  = apply_repairs,
            progress_cb    = _cb,
        )
        results.append(r)

    return results
