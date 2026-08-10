"""Ledger Validator — read-only inspection of a portfolio's transaction ledger.

Design invariants
-----------------
* NEVER writes to the database.
* NEVER modifies replay behavior in portfolio_rebuilder.
* NEVER raises exceptions to the caller — errors produce findings, not stack traces.
* Internal replay is private; does NOT import from portfolio_rebuilder.
* Price-dependent checks require fetch_prices=True and contact yfinance.

Severity levels
---------------
  WARNING  — suspicious pattern; may or may not be a real problem
  ERROR    — likely corruption that will cause incorrect replay results
  CRITICAL — definite corruption; action required before trusting replay output

Usage
-----
  from services.ledger_validator import validate_portfolio_ledger

  report = await validate_portfolio_ledger(
      db=db, portfolio_id=4, workspace_id=1, fetch_prices=True
  )
  for f in report.findings:
      print(f.severity, f.title)
"""
from __future__ import annotations

import asyncio
import bisect
import dataclasses
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Literal

import pandas as pd
from sqlalchemy.orm import Session

from models.database import Portfolio, PortfolioItem, PortfolioSnapshot, Transaction
from services.portfolio_reference import resolve_portfolio_reference
from services.asset_definitions import (
    BindingResolver,
    DefinitionRegistry,
    DefinitionRegistryError,
    UnresolvedBindingError,
)
from services.asset_definitions.vocabulary import AcquisitionSemantics, FlowType, RelationshipKind
from services.asset_domain import AssetType
from services.data_fetcher import fetch_history
from services.ledger_repair import apply_repair_overlay
from services.replay_key import replay_key
from services.runtime_consultation import (
    RuntimeConsultationLog,
    RuntimeFindingCategory,
    RuntimeValidationFinding,
)
from services.transaction_canonicalizer import (
    CanonicalTransaction,
    canonicalize_transactions,
)

_log = logging.getLogger(__name__)

# ── Module-level thresholds (callers can override per-call) ────────────────────
_DATE_SKEW_WARNING_DAYS  = 90
_DATE_SKEW_ERROR_DAYS    = 365
_CASH_TOLERANCE          = 1.0    # THB absolute
_SHARES_TOLERANCE        = 0.001  # shares absolute

# ── Transaction type groups ────────────────────────────────────────────────────
_EQUITY_TYPES  = frozenset({"BUY", "SELL", "INITIAL_POSITION", "QUANTITY_CORRECTION"})
_BUY_TYPES     = frozenset({"BUY", "INITIAL_POSITION"})
_CASH_IN_TYPES = frozenset({"DEPOSIT", "INITIAL_CASH"})


# ══════════════════════════════════════════════════════════════════════════════
# Public data structures
# ══════════════════════════════════════════════════════════════════════════════

class FindingSeverity(str, Enum):
    WARNING  = "WARNING"
    ERROR    = "ERROR"
    CRITICAL = "CRITICAL"


_SEV_ORDER = {FindingSeverity.CRITICAL: 0, FindingSeverity.ERROR: 1, FindingSeverity.WARNING: 2}


@dataclass
class LedgerFinding:
    """One anomaly found in the transaction ledger."""
    check_id:          str
    severity:          FindingSeverity
    portfolio_id:      int
    transaction_ids:   list[int]
    symbol:            str | None
    normalized_symbol: str | None
    title:             str
    explanation:       str
    recommendation:    str
    details:           dict[str, Any] = field(default_factory=dict)
    # Populated only in effective mode: "RAW" = transaction present; None = raw mode.
    origin:            str | None     = None


@dataclass
class LedgerValidationReport:
    portfolio_id:           int
    portfolio_name:         str
    transactions_inspected: int
    findings:               list[LedgerFinding] = field(default_factory=list)
    elapsed_seconds:        float = 0.0
    price_check_performed:  bool  = False
    # Stage R1 (M11): populated only when _consult_runtime_capabilities()
    # runs (non-empty ctxs). None means "not consulted", not "no findings".
    runtime_consultation:   "RuntimeConsultationLog | None" = None

    @property
    def criticals(self) -> list[LedgerFinding]:
        return [f for f in self.findings if f.severity == FindingSeverity.CRITICAL]

    @property
    def errors(self) -> list[LedgerFinding]:
        return [f for f in self.findings if f.severity == FindingSeverity.ERROR]

    @property
    def warnings(self) -> list[LedgerFinding]:
        return [f for f in self.findings if f.severity == FindingSeverity.WARNING]

    @property
    def overall_severity(self) -> str:
        if self.criticals:
            return "CRITICAL"
        if self.errors:
            return "ERROR"
        if self.warnings:
            return "WARNING"
        return "PASS"


@dataclass(frozen=True)
class LedgerValidationComparison:
    """Side-by-side result of raw vs effective ledger validation.

    Produced by compare_ledger_validation().  No replay is performed beyond
    what the two validation runs already do; no DB writes occur.

    Fields
    ------
    raw_report         — report produced with mode="raw" (no overlay).
    effective_report   — report produced with mode="effective" (overlay applied).
    resolved_findings  — finding keys present in raw but absent in effective
                         (EXCLUDE or SUPPRESS_FINDING removed them).
    remaining_findings — finding keys present in both reports (unresolved).
    newly_introduced_findings — finding keys absent in raw but present in
                         effective (should normally be empty).
    """
    raw_report:                  LedgerValidationReport
    effective_report:            LedgerValidationReport
    resolved_findings:           tuple[str, ...]
    remaining_findings:          tuple[str, ...]
    newly_introduced_findings:   tuple[str, ...]


# ── Private helpers for comparison ────────────────────────────────────────────

def _finding_key(f: LedgerFinding) -> str:
    """Deterministic string key that uniquely identifies a finding instance.

    Uses check_id + sorted transaction_ids when present; falls back to the
    first 60 chars of title for findings with no transaction references
    (e.g. CASH_MISMATCH, HOLDINGS_MISMATCH).
    """
    if f.transaction_ids:
        tx_part = ",".join(str(i) for i in sorted(f.transaction_ids))
        return f"{f.check_id}:{tx_part}"
    return f"{f.check_id}:{f.title[:60]}"


def _ledger_confidence(report: LedgerValidationReport) -> float:
    """Confidence score 0–100 derived from finding severity counts.

    Penalty weights:  CRITICAL × 25, ERROR × 10, WARNING × 3.
    A clean ledger (no findings) yields 100.0.
    """
    if not report.findings:
        return 100.0
    penalty = (
        len(report.criticals) * 25
        + len(report.errors)   * 10
        + len(report.warnings) * 3
    )
    return max(0.0, 100.0 - float(penalty))


# ══════════════════════════════════════════════════════════════════════════════
# Structural checks (pure read of canonical transaction list)
# ══════════════════════════════════════════════════════════════════════════════

def _check_duplicate_initial_positions(
    portfolio_id: int,
    ctxs: list[CanonicalTransaction],
) -> list[LedgerFinding]:
    """CHECK 1 — Multiple INITIAL_POSITION records for the same symbol on the same date.

    Replay accumulates all of them, silently overstating the position.
    Groups by canonical_symbol so alias variants (KBANK / KBANK.BK) are detected.
    """
    groups: dict[tuple[str, str], list[CanonicalTransaction]] = defaultdict(list)
    for ctx in ctxs:
        if ctx.transaction_type != "INITIAL_POSITION":
            continue
        if not ctx.raw_symbol:
            continue
        canon    = ctx.canonical_symbol or ctx.raw_symbol
        date_str = ctx.transaction_date.strftime("%Y-%m-%d")
        groups[(canon, date_str)].append(ctx)

    findings: list[LedgerFinding] = []
    for (canon, date_str), group in sorted(groups.items()):
        if len(group) <= 1:
            continue
        tx_ids      = [c.id for c in group]
        raw_symbols = sorted({c.raw_symbol for c in group if c.raw_symbol})
        total_sh    = sum(float(c.shares) for c in group)
        entry_lines = "\n".join(
            f"  tx{c.id}  {c.raw_symbol}  {float(c.shares):.4f} @ {float(c.price_per_share):.4f}"
            for c in group
        )
        findings.append(LedgerFinding(
            check_id          = "DUP_INITIAL_POSITION",
            severity          = FindingSeverity.CRITICAL,
            portfolio_id      = portfolio_id,
            transaction_ids   = tx_ids,
            symbol            = group[0].raw_symbol,
            normalized_symbol = canon,
            title             = f"Duplicate INITIAL_POSITION: {canon} on {date_str} ({len(group)}×)",
            explanation       = (
                f"Portfolio {portfolio_id} has {len(group)} INITIAL_POSITION records "
                f"for '{canon}' on {date_str}. "
                f"Raw symbols: {raw_symbols}. "
                f"Replay will accumulate all of them (total={total_sh:.4f} shares).\n"
                f"{entry_lines}"
            ),
            recommendation    = (
                "Review manually. Identify the authoritative import record. "
                "Do NOT auto-delete. After verifying, delete the duplicate(s), "
                "then run rebuild_portfolio."
            ),
            details={
                "canonical_symbol": canon,
                "date":             date_str,
                "count":            len(group),
                "transaction_ids":  tx_ids,
                "raw_symbols":      raw_symbols,
                "total_shares":     round(total_sh, 6),
            },
        ))
    return findings


def _check_symbol_aliases(
    portfolio_id: int,
    ctxs: list[CanonicalTransaction],
) -> list[LedgerFinding]:
    """CHECK 2 — Multiple raw symbols resolve to the same ReplayKey.

    e.g. KBANK and KBANK.BK both map to KBANK.BK;
         NVDA01 and NVDA01.BK both map to NVDA.

    CRITICAL, not WARNING (ADR-005 / TDD Stage 0). Replay
    (portfolio_rebuilder.py) now keys holdings state by replay_key(ctx), so an
    aliased pair merges into one holding instead of two phantom positions —
    that part of the defect is fixed. What remains is that the merge itself
    changes previously-reported per-symbol numbers (shares, avg_cost) for any
    portfolio where this fires, which ADR-005's "Consequences" section
    requires to be individually reviewed and documented (DECISION_LOG.md)
    before that portfolio's rebuild is trusted or a golden baseline is
    captured from it. This finding is the mechanical gate for that review —
    it blocks commit (rebuild_portfolio Stage 5) until resolved, exactly as
    DUP_INITIAL_POSITION already does for its own CRITICAL condition.
    """
    # ReplayKeyT — under native (asset_id-preferring) keying (TDD Stage 4),
    # `canon` may be an int for resolved transactions while an unresolved
    # residual on the same portfolio still falls through to a str. Keys are
    # never mixed-type-compared directly (sorted() below uses str(canon) as
    # its sort key) — same crash class already fixed in portfolio_rebuilder.py
    # (_reconcile_portfolio_items et al.).
    canon_to_raw:    dict[object, set[str]]  = defaultdict(set)
    canon_to_tx_ids: dict[object, list[int]] = defaultdict(list)

    for ctx in ctxs:
        if not ctx.raw_symbol:
            continue
        canon = replay_key(ctx)
        canon_to_raw[canon].add(ctx.raw_symbol)
        canon_to_tx_ids[canon].append(ctx.id)

    findings: list[LedgerFinding] = []
    for canon, raw_set in sorted(canon_to_raw.items(), key=lambda kv: str(kv[0])):
        if len(raw_set) <= 1:
            continue
        raw_list = sorted(raw_set)
        canon_str = str(canon)
        findings.append(LedgerFinding(
            check_id          = "SYMBOL_ALIAS",
            severity          = FindingSeverity.CRITICAL,
            portfolio_id      = portfolio_id,
            transaction_ids   = canon_to_tx_ids[canon],
            symbol            = raw_list[0],
            normalized_symbol = canon_str,
            title             = f"Symbol alias: multiple raw forms resolve to '{canon_str}'",
            explanation       = (
                f"Raw symbols {raw_list} in portfolio {portfolio_id} all resolve "
                f"to the same ReplayKey '{canon}'. "
                "Replay now merges these into a single holding (ADR-005), which "
                "changes previously-reported per-symbol shares/avg_cost for this "
                "portfolio relative to any prior rebuild that treated them as "
                "separate positions. This typically results from legacy symbol "
                "storage without the .BK suffix, or from a symbol rename."
            ),
            recommendation    = (
                "Verify all raw symbols refer to the same instrument, then "
                "review the resulting merged holding before trusting this "
                "portfolio's rebuild output. Document the review in "
                "DECISION_LOG.md per ADR-005, then run rebuild_portfolio."
            ),
            details={
                "canonical_symbol":  canon_str,
                "raw_symbols":       raw_list,
                "transaction_count": len(canon_to_tx_ids[canon]),
            },
        ))
    return findings


def _check_null_symbols(
    portfolio_id: int,
    ctxs: list[CanonicalTransaction],
) -> list[LedgerFinding]:
    """CHECK 3 — Equity transactions with a null or empty symbol."""
    findings: list[LedgerFinding] = []
    for ctx in ctxs:
        if ctx.transaction_type not in _EQUITY_TYPES:
            continue
        if ctx.raw_symbol is not None:
            continue
        findings.append(LedgerFinding(
            check_id          = "NULL_SYMBOL",
            severity          = FindingSeverity.ERROR,
            portfolio_id      = portfolio_id,
            transaction_ids   = [ctx.id],
            symbol            = None,
            normalized_symbol = None,
            title             = f"tx{ctx.id}: {ctx.transaction_type} with null/empty symbol",
            explanation       = (
                f"tx{ctx.id} (type={ctx.transaction_type}, "
                f"date={ctx.transaction_date}) has no symbol. "
                "Replay silently skips it."
            ),
            recommendation    = (
                "Determine the correct symbol and update it, or delete "
                "this transaction if it was recorded in error."
            ),
            details={"transaction_id": ctx.id, "type": ctx.transaction_type,
                     "date": str(ctx.transaction_date)},
        ))
    return findings


def _check_zero_shares(
    portfolio_id: int,
    ctxs: list[CanonicalTransaction],
) -> list[LedgerFinding]:
    """CHECK 4 — Equity transactions with zero or null shares."""
    findings: list[LedgerFinding] = []
    for ctx in ctxs:
        if ctx.transaction_type not in _EQUITY_TYPES:
            continue
        if ctx.shares != 0:
            continue
        findings.append(LedgerFinding(
            check_id          = "ZERO_SHARES",
            severity          = FindingSeverity.ERROR,
            portfolio_id      = portfolio_id,
            transaction_ids   = [ctx.id],
            symbol            = ctx.raw_symbol,
            normalized_symbol = ctx.canonical_symbol,
            title             = (
                f"tx{ctx.id}: {ctx.transaction_type} {ctx.raw_symbol or '?'} "
                f"has zero/null shares"
            ),
            explanation       = (
                f"tx{ctx.id} ({ctx.transaction_type} {ctx.raw_symbol} on "
                f"{ctx.transaction_date}) has shares={float(ctx.shares)}. "
                "Replay skips this transaction."
            ),
            recommendation    = (
                "Correct the shares field or remove this transaction."
            ),
            details={"transaction_id": ctx.id, "shares": float(ctx.shares),
                     "type": ctx.transaction_type, "symbol": ctx.raw_symbol},
        ))
    return findings


def _check_zero_prices(
    portfolio_id: int,
    ctxs: list[CanonicalTransaction],
) -> list[LedgerFinding]:
    """CHECK 5 — BUY/INITIAL_POSITION with zero or null price_per_share.

    Zero price causes avg_cost=0, corrupting cost-basis for all future SELLs.
    """
    findings: list[LedgerFinding] = []
    for ctx in ctxs:
        if ctx.transaction_type not in {"BUY", "INITIAL_POSITION"}:
            continue
        if ctx.price_per_share != 0:
            continue
        findings.append(LedgerFinding(
            check_id          = "ZERO_PRICE",
            severity          = FindingSeverity.WARNING,
            portfolio_id      = portfolio_id,
            transaction_ids   = [ctx.id],
            symbol            = ctx.raw_symbol,
            normalized_symbol = ctx.canonical_symbol,
            title             = (
                f"tx{ctx.id}: {ctx.transaction_type} {ctx.raw_symbol or '?'} "
                f"has zero/null price_per_share"
            ),
            explanation       = (
                f"tx{ctx.id} ({ctx.transaction_type} {ctx.raw_symbol} on "
                f"{ctx.transaction_date}) has price_per_share={float(ctx.price_per_share)}. "
                "This sets avg_cost=0, causing incorrect cost-basis and "
                "unrealized P/L calculations."
            ),
            recommendation    = "Correct price_per_share for this transaction.",
            details={"transaction_id": ctx.id, "price_per_share": float(ctx.price_per_share),
                     "symbol": ctx.raw_symbol},
        ))
    return findings


def _check_pre_portfolio_transactions(
    portfolio_id:        int,
    portfolio_created_at: datetime | None,
    ctxs: list[CanonicalTransaction],
) -> list[LedgerFinding]:
    """CHECK 6 — Transactions whose date is before the portfolio was created."""
    if not portfolio_created_at:
        return []

    cutoff = (
        portfolio_created_at.date()
        if hasattr(portfolio_created_at, "date")
        else portfolio_created_at
    )
    findings: list[LedgerFinding] = []
    for ctx in ctxs:
        # ctx.transaction_date is always a date (canonicalizer guarantees this)
        tx_date = ctx.transaction_date
        if tx_date >= cutoff:
            continue
        findings.append(LedgerFinding(
            check_id          = "PRE_PORTFOLIO_TX",
            severity          = FindingSeverity.ERROR,
            portfolio_id      = portfolio_id,
            transaction_ids   = [ctx.id],
            symbol            = ctx.raw_symbol,
            normalized_symbol = ctx.canonical_symbol,
            title             = (
                f"tx{ctx.id}: {ctx.transaction_type} dated {tx_date} "
                f"before portfolio creation ({cutoff})"
            ),
            explanation       = (
                f"tx{ctx.id} has transaction_date={tx_date}, "
                f"which precedes the portfolio creation date {cutoff}. "
                "This suggests a backdated import or a transaction belonging "
                "to a different portfolio."
            ),
            recommendation    = (
                "Verify the transaction date. If backdated intentionally "
                "(historical position import), this may be acceptable. "
                "Otherwise, correct the date or move to the correct portfolio."
            ),
            details={
                "transaction_id":       ctx.id,
                "transaction_date":     str(tx_date),
                "portfolio_created_at": str(cutoff),
                "type":                 ctx.transaction_type,
                "symbol":               ctx.raw_symbol,
            },
        ))
    return findings


def _check_date_skew(
    portfolio_id: int,
    ctxs: list[CanonicalTransaction],
    warning_days: int = _DATE_SKEW_WARNING_DAYS,
    error_days:   int = _DATE_SKEW_ERROR_DAYS,
) -> list[LedgerFinding]:
    """CHECK 7 — Large gap between created_at (physical insert) and transaction_date.

    The live snapshot engine uses created_at; the rebuild engine uses
    transaction_date.  A large skew means these two engines place the
    transaction in different periods — a source of irreconcilable divergence.
    """
    findings: list[LedgerFinding] = []
    for ctx in ctxs:
        if not ctx.created_at:
            continue
        ca   = ctx.created_at.date()
        td   = ctx.transaction_date
        skew = abs((ca - td).days)
        if skew < warning_days:
            continue
        severity = FindingSeverity.ERROR if skew >= error_days else FindingSeverity.WARNING
        findings.append(LedgerFinding(
            check_id          = "LARGE_DATE_SKEW",
            severity          = severity,
            portfolio_id      = portfolio_id,
            transaction_ids   = [ctx.id],
            symbol            = ctx.raw_symbol,
            normalized_symbol = ctx.canonical_symbol,
            title             = (
                f"tx{ctx.id}: {ctx.transaction_type} "
                f"created_at vs transaction_date skew = {skew} days"
            ),
            explanation       = (
                f"tx{ctx.id} ({ctx.transaction_type} {ctx.raw_symbol or ''}) "
                f"was inserted (created_at={ctx.created_at}) "
                f"but bears a transaction_date {skew} days away "
                f"({ctx.transaction_date}). "
                "The live snapshot engine attributes this transaction to the "
                "created_at period; the rebuild engine attributes it to "
                "transaction_date.  A large skew causes these engines to "
                "disagree on which snapshot period the transaction belongs to."
            ),
            recommendation    = (
                "Verify both dates are intentional. If not, correct "
                "transaction_date to reflect the actual trade date."
            ),
            details={
                "transaction_id":   ctx.id,
                "created_at":       str(ctx.created_at),
                "transaction_date": str(ctx.transaction_date),
                "skew_days":        skew,
                "type":             ctx.transaction_type,
                "symbol":           ctx.raw_symbol,
            },
        ))
    return findings


def _check_duplicate_fingerprints(
    portfolio_id: int,
    ctxs: list[CanonicalTransaction],
) -> list[LedgerFinding]:
    """CHECK 8 — Transactions with identical (type, symbol, shares, price, date).

    Replay applies each record independently, potentially multiplying the position.
    """
    seen:            dict[tuple, list[int]]       = defaultdict(list)
    canon_for_key:   dict[tuple, str | None]      = {}

    for ctx in ctxs:
        date_str = ctx.transaction_date.strftime("%Y-%m-%d")
        key = (
            ctx.transaction_type,
            ctx.raw_symbol or "",
            round(float(ctx.shares), 6),
            round(float(ctx.price_per_share), 4),
            date_str,
        )
        seen[key].append(ctx.id)
        if key not in canon_for_key:
            canon_for_key[key] = ctx.canonical_symbol

    findings: list[LedgerFinding] = []
    for key, ids in sorted(seen.items(), key=lambda kv: kv[1][0]):
        if len(ids) <= 1:
            continue
        tx_type, sym, shares, price, date_str = key
        findings.append(LedgerFinding(
            check_id          = "DUP_TX_FINGERPRINT",
            severity          = FindingSeverity.WARNING,
            portfolio_id      = portfolio_id,
            transaction_ids   = ids,
            symbol            = sym or None,
            normalized_symbol = canon_for_key.get(key),
            title             = (
                f"Duplicate fingerprint: {tx_type} {sym} "
                f"{shares} @ {price} on {date_str} ({len(ids)}×)"
            ),
            explanation       = (
                f"Transactions {ids} share identical "
                f"(type={tx_type}, symbol={sym}, shares={shares}, "
                f"price={price}, date={date_str}). "
                "Replay applies each independently. This can be a genuine "
                "duplicate, or it can reflect legitimate repeated activity "
                "(multiple fills, staged entries, DCA, repeated orders on "
                "the same day) — human review is needed to tell them apart."
            ),
            recommendation    = (
                "Review the transactions. If they are true duplicates, keep "
                "the authoritative record and delete the duplicate(s), then "
                "run rebuild_portfolio. If they reflect distinct fills/orders, "
                "no action is needed."
            ),
            details={
                "transaction_ids": ids,
                "type":            tx_type,
                "symbol":          sym,
                "shares":          shares,
                "price":           price,
                "date":            date_str,
                "count":           len(ids),
            },
        ))
    return findings


# ══════════════════════════════════════════════════════════════════════════════
# Internal private replay state
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class _ReplayState:
    holdings: dict[str, Decimal]
    cash:     Decimal
    # BANPU-WP2 Step 6: per-raw-holding-key exact cost basis (shares × avg
    # cost) and identity metadata (canonical_symbol, asset_id), tracked in
    # parallel with `holdings` for every symbol — not only conversion-related
    # ones — so a later POSITION_CONVERSION can independently resolve and
    # verify its predecessor/successor without importing portfolio_rebuilder's
    # own _PortfolioState/_HoldingState (Implementation Specification §5.2).
    # A key absent from `basis`/`identity` but present in `holdings` cannot
    # occur within one replay run: every branch that creates or updates a
    # holdings entry also writes basis/identity in the same step.
    basis:    dict[str, Decimal]              = field(default_factory=dict)
    identity: dict[str, tuple[str | None, int | None]] = field(default_factory=dict)

    def copy(self) -> "_ReplayState":
        return _ReplayState(
            holdings = dict(self.holdings),
            cash     = self.cash,
            basis    = dict(self.basis),
            identity = dict(self.identity),
        )


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP2 Step 6 — independent POSITION_CONVERSION validation
#
# Owns its own replay entirely separate from portfolio_rebuilder.py: no import
# of _PortfolioState, _HoldingState, _apply_transaction, replay_key(), or any
# rebuilder helper (Implementation Specification §5.2/§6.2). Candidate
# resolution, duplicate detection, and cash-in-lieu accounting are each
# reimplemented here against this module's own raw-keyed _ReplayState.
# ══════════════════════════════════════════════════════════════════════════════

_CONVERSION_BASIS_TOLERANCE      = Decimal("0.01")
_CONVERSION_PROJECTION_TOLERANCE = Decimal("0.000001")

# Transaction types whose presence on a conversion's transition calendar date,
# targeting the predecessor or successor asset, is a same-day conflict
# (Implementation Specification §4.1/§9.2). Independent of
# portfolio_rebuilder.py's own _SAME_DAY_CONFLICT_TYPES constant.
_CONVERSION_SAME_DAY_TYPES = frozenset({
    "BUY", "SELL", "INITIAL_POSITION", "QUANTITY_CORRECTION", "POSITION_CONVERSION",
})


def _conversion_finding(
    check_id:       str,
    severity:       FindingSeverity,
    portfolio_id:   int,
    ctx:            CanonicalTransaction,
    title:          str,
    explanation:    str,
    recommendation: str,
    details:        dict[str, Any],
) -> LedgerFinding:
    return LedgerFinding(
        check_id=check_id, severity=severity, portfolio_id=portfolio_id,
        transaction_ids=[ctx.id], symbol=ctx.raw_symbol, normalized_symbol=ctx.canonical_symbol,
        title=title, explanation=explanation, recommendation=recommendation, details=details,
    )


def _resolve_conversion_candidates(
    state:    _ReplayState,
    asset_id: int,
    symbol:   str,
) -> set[str]:
    """Deterministic raw-holding-key candidate resolution (Implementation
    Specification §5.2/§7.2/§7.3), independent of portfolio_rebuilder.py's own
    replay_key()-based resolution.

    Asset-ID matches and canonical-symbol matches are unioned and deduplicated
    by actual raw holding key. In legacy mode every tracked asset_id is None,
    so the asset-ID set is always empty and this degenerates to pure
    canonical-symbol matching — one formula serves both legacy and native
    validator replay without a mode flag.
    """
    candidates: set[str] = set()
    for key in state.holdings:
        key_canon, key_asset_id = state.identity.get(key, (None, None))
        if key_asset_id is not None and key_asset_id == asset_id:
            candidates.add(key)
        if key_canon == symbol:
            candidates.add(key)
    return candidates


def _apply_position_conversion(
    portfolio_id:      int,
    ctx:               CanonicalTransaction,
    all_ctxs:          list[CanonicalTransaction],
    state:             _ReplayState,
    conversion_seen:   set,
    raw_asset_id_by_id: dict[int, int | None] | None = None,
) -> list[LedgerFinding]:
    """Independent, validator-owned POSITION_CONVERSION handling.

    Mutates `state` in place only when every check passes; a failing check
    returns exactly one finding for `ctx` and leaves `state` untouched
    (Implementation Specification §10: "do not choose a winner", "do not
    coerce, round into tolerance, or repair the payload").

    raw_asset_id_by_id (BANPU-WP2 Step 7 fix): the top-level identity check
    below must compare the payload against the transaction row's OWN
    persisted asset_id — not CanonicalTransaction.asset_id, which WP1's
    canonicalizer deliberately sets to None for every row when a portfolio
    is on legacy replay keying (Portfolio.replay_asset_id_native=False, the
    default). portfolio_rebuilder.py's own preflight
    (_preflight_position_conversions) reads the raw Transaction row for
    exactly this reason, with an explicit comment explaining why ctx.asset_id
    is wrong for this specific check. Falls back to ctx.asset_id when the map
    is absent (existing direct _replay_and_check() callers in tests that
    construct ctxs without going through validate_portfolio_ledger()).
    """
    parsed = ctx.position_conversion
    if parsed is None or not parsed.is_valid or parsed.value is None:
        return [_conversion_finding(
            "POSITION_CONVERSION_PAYLOAD_INVALID", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: POSITION_CONVERSION payload invalid",
            explanation=(
                f"tx{ctx.id}'s conversion payload failed WP1 parse validation "
                f"({len(parsed.errors) if parsed else 0} error(s)). Replay cannot "
                "apply an unparseable conversion."
            ),
            recommendation="Correct the conversion payload per the version-1 schema.",
            details={"transaction_id": ctx.id,
                     "errors": [e.code for e in (parsed.errors if parsed else [])]},
        )]

    payload = parsed.value

    raw_asset_id = raw_asset_id_by_id.get(ctx.id) if raw_asset_id_by_id is not None else ctx.asset_id
    raw_asset_id_mismatch = (
        raw_asset_id != payload.predecessor.asset_id
        if raw_asset_id_by_id is not None
        else raw_asset_id is not None and raw_asset_id != payload.predecessor.asset_id
    )
    if (
        ctx.canonical_symbol != payload.predecessor.symbol
        or ctx.transaction_date != payload.dates.valuation_transition_date
        or raw_asset_id_mismatch
    ):
        return [_conversion_finding(
            "POSITION_CONVERSION_IDENTITY_INVALID", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: POSITION_CONVERSION top-level identity disagrees with payload",
            explanation=(
                f"tx{ctx.id}'s own symbol/date/asset_id do not agree with its payload "
                f"predecessor identity (payload symbol={payload.predecessor.symbol}, "
                f"transition_date={payload.dates.valuation_transition_date})."
            ),
            recommendation="Verify the transaction row's symbol, date, and asset_id match the payload predecessor.",
            details={
                "transaction_id": ctx.id,
                "row_symbol":     ctx.canonical_symbol,
                "row_date":       str(ctx.transaction_date),
                "payload_symbol": payload.predecessor.symbol,
                "payload_date":   str(payload.dates.valuation_transition_date),
            },
        )]

    dup_key = (payload.predecessor.asset_id, payload.dates.valuation_transition_date)
    if dup_key in conversion_seen:
        return [_conversion_finding(
            "POSITION_CONVERSION_DUPLICATE", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: duplicate POSITION_CONVERSION for the same predecessor/date",
            explanation=(
                f"Another POSITION_CONVERSION already replayed for predecessor "
                f"asset_id={payload.predecessor.asset_id} on "
                f"{payload.dates.valuation_transition_date}. Exactly one conversion key "
                "is permitted per portfolio, predecessor asset, and transition date."
            ),
            recommendation="Identify and remove the duplicate conversion row.",
            details={
                "transaction_id":       ctx.id,
                "predecessor_asset_id": payload.predecessor.asset_id,
                "transition_date":      str(payload.dates.valuation_transition_date),
            },
        )]
    conversion_seen.add(dup_key)

    transition_date = payload.dates.valuation_transition_date
    for other in all_ctxs:
        if other.id == ctx.id or other.transaction_type not in _CONVERSION_SAME_DAY_TYPES:
            continue
        if other.transaction_date != transition_date:
            continue
        if other.transaction_type == "POSITION_CONVERSION":
            other_parsed = other.position_conversion
            if other_parsed is not None and other_parsed.is_valid and other_parsed.value is not None:
                other_payload = other_parsed.value
                other_key = (
                    other_payload.predecessor.asset_id,
                    other_payload.dates.valuation_transition_date,
                )
                if other_key == dup_key:
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
            return [_conversion_finding(
                "POSITION_CONVERSION_SAME_DAY_CONFLICT", FindingSeverity.ERROR, portfolio_id, ctx,
                title=f"tx{ctx.id}: another equity transaction affects the predecessor/successor on the transition date",
                explanation=(
                    f"tx{other.id} ({other.transaction_type} {other.raw_symbol or ''}) also "
                    f"falls on {transition_date}, the conversion's valuation transition date, "
                    "and targets the predecessor or successor asset."
                ),
                recommendation="Move the conflicting transaction off the transition date, or verify the conversion date.",
                details={
                    "transaction_id":             ctx.id,
                    "conflicting_transaction_id": other.id,
                    "transition_date":            str(transition_date),
                },
            )]

    predecessor_candidates = _resolve_conversion_candidates(
        state, payload.predecessor.asset_id, payload.predecessor.symbol,
    )
    if len(predecessor_candidates) == 0:
        return [_conversion_finding(
            "POSITION_CONVERSION_WITHOUT_HOLDING", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: no predecessor holding found for POSITION_CONVERSION",
            explanation=(
                f"No replayed holding matches predecessor asset_id="
                f"{payload.predecessor.asset_id} / symbol={payload.predecessor.symbol}."
            ),
            recommendation="Verify the predecessor was actually held before the conversion.",
            details={"transaction_id": ctx.id, "predecessor_symbol": payload.predecessor.symbol},
        )]
    if len(predecessor_candidates) > 1:
        return [_conversion_finding(
            "POSITION_CONVERSION_AMBIGUOUS_HOLDING", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: multiple holdings match the POSITION_CONVERSION predecessor identity",
            explanation=(
                f"{len(predecessor_candidates)} distinct replayed holdings "
                f"({sorted(predecessor_candidates)}) match predecessor asset_id="
                f"{payload.predecessor.asset_id} / symbol={payload.predecessor.symbol}."
            ),
            recommendation="Resolve the symbol/asset-ID ambiguity before replaying this conversion.",
            details={"transaction_id": ctx.id, "candidates": sorted(predecessor_candidates)},
        )]
    predecessor_key = next(iter(predecessor_candidates))

    replayed_shares = state.holdings[predecessor_key]
    if replayed_shares != payload.predecessor.shares_surrendered:
        return [_conversion_finding(
            "POSITION_CONVERSION_SHARE_MISMATCH", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: predecessor shares disagree with payload shares_surrendered",
            explanation=(
                f"Replayed predecessor holding has {replayed_shares} shares, but "
                f"payload.predecessor.shares_surrendered={payload.predecessor.shares_surrendered}."
            ),
            recommendation="Verify the surrendered share count against the replayed holding.",
            details={
                "transaction_id":              ctx.id,
                "replayed_shares":              str(replayed_shares),
                "payload_shares_surrendered":   str(payload.predecessor.shares_surrendered),
            },
        )]

    if abs(ctx.shares - payload.successor.shares_received) > _CONVERSION_PROJECTION_TOLERANCE:
        return [_conversion_finding(
            "POSITION_CONVERSION_SHARE_MISMATCH", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: top-level shares disagree with successor shares_received",
            explanation=(
                f"Top-level shares={ctx.shares}, but payload.successor.shares_received="
                f"{payload.successor.shares_received} (tolerance {_CONVERSION_PROJECTION_TOLERANCE})."
            ),
            recommendation="Correct the top-level shares projection or the payload.",
            details={
                "transaction_id": ctx.id,
                "row_shares": str(ctx.shares),
                "payload_shares_received": str(payload.successor.shares_received),
            },
        )]

    replayed_basis = state.basis.get(predecessor_key, Decimal("0"))
    if abs(replayed_basis - payload.basis.before) > _CONVERSION_BASIS_TOLERANCE:
        return [_conversion_finding(
            "POSITION_CONVERSION_BASIS_MISMATCH", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: predecessor basis disagrees with payload basis.before",
            explanation=(
                f"Replayed predecessor basis is {replayed_basis}, but "
                f"payload.basis.before={payload.basis.before} "
                f"(tolerance {_CONVERSION_BASIS_TOLERANCE})."
            ),
            recommendation="Verify the predecessor's replayed cost basis against the payload.",
            details={
                "transaction_id":      ctx.id,
                "replayed_basis":      str(replayed_basis),
                "payload_basis_before": str(payload.basis.before),
            },
        )]

    expected_avg_cost = payload.basis.carried_to_successor / payload.successor.shares_received
    basis_projection_mismatches: list[str] = []
    if abs(ctx.price_per_share - expected_avg_cost) > _CONVERSION_PROJECTION_TOLERANCE:
        basis_projection_mismatches.append("price_per_share")
    if (
        abs(ctx.total_amount - payload.basis.carried_to_successor)
        > _CONVERSION_PROJECTION_TOLERANCE
    ):
        basis_projection_mismatches.append("total_amount")
    if basis_projection_mismatches:
        return [_conversion_finding(
            "POSITION_CONVERSION_BASIS_MISMATCH", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: top-level basis projection disagrees with payload",
            explanation=(
                f"Top-level field(s) {basis_projection_mismatches} do not match the payload "
                f"within tolerance {_CONVERSION_PROJECTION_TOLERANCE}."
            ),
            recommendation="Correct the top-level basis projections or the payload.",
            details={
                "transaction_id": ctx.id,
                "mismatched_fields": basis_projection_mismatches,
                "row_price_per_share": str(ctx.price_per_share),
                "payload_average_cost": str(expected_avg_cost),
                "row_total_amount": str(ctx.total_amount),
                "payload_basis_carried": str(payload.basis.carried_to_successor),
            },
        )]

    cil = payload.cash_in_lieu
    expected_fees = cil.fees if cil is not None else Decimal("0")
    expected_taxes = cil.taxes if cil is not None else Decimal("0")
    cil_projection_mismatches: list[str] = []
    if abs(ctx.fees - expected_fees) > _CONVERSION_PROJECTION_TOLERANCE:
        cil_projection_mismatches.append("fees")
    if abs(ctx.taxes - expected_taxes) > _CONVERSION_PROJECTION_TOLERANCE:
        cil_projection_mismatches.append("taxes")
    if cil_projection_mismatches:
        return [_conversion_finding(
            "POSITION_CONVERSION_CIL_INVALID", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: top-level cash-in-lieu projection disagrees with payload",
            explanation=(
                f"Top-level field(s) {cil_projection_mismatches} do not match "
                f"the {'cash-in-lieu payload' if cil is not None else 'required null-leg zero'} "
                f"within tolerance {_CONVERSION_PROJECTION_TOLERANCE}."
            ),
            recommendation="Correct the top-level cash-in-lieu projections or the payload.",
            details={
                "transaction_id":    ctx.id,
                "mismatched_fields": cil_projection_mismatches,
                "row_fees":          str(ctx.fees),
                "payload_fees":      str(expected_fees),
                "row_taxes":         str(ctx.taxes),
                "payload_taxes":     str(expected_taxes),
            },
        )]

    successor_candidates = _resolve_conversion_candidates(
        state, payload.successor.asset_id, payload.successor.symbol,
    )
    if len(successor_candidates) > 1:
        return [_conversion_finding(
            "POSITION_CONVERSION_AMBIGUOUS_HOLDING", FindingSeverity.CRITICAL, portfolio_id, ctx,
            title=f"tx{ctx.id}: multiple holdings match the POSITION_CONVERSION successor identity",
            explanation=(
                f"{len(successor_candidates)} distinct replayed holdings "
                f"({sorted(successor_candidates)}) match successor asset_id="
                f"{payload.successor.asset_id} / symbol={payload.successor.symbol}."
            ),
            recommendation="Resolve the symbol/asset-ID ambiguity before replaying this conversion.",
            details={"transaction_id": ctx.id, "candidates": sorted(successor_candidates)},
        )]

    # ── Every check passed — apply atomically ───────────────────────────────
    del state.holdings[predecessor_key]
    state.basis.pop(predecessor_key, None)
    state.identity.pop(predecessor_key, None)

    received_shares = payload.successor.shares_received
    carried_basis   = payload.basis.carried_to_successor
    net_cash        = payload.cash_in_lieu.net_cash if payload.cash_in_lieu else Decimal("0")

    if successor_candidates:
        successor_key  = next(iter(successor_candidates))
        existing_basis = state.basis.get(successor_key, Decimal("0"))
        state.holdings[successor_key] = state.holdings[successor_key] + received_shares
        state.basis[successor_key]    = existing_basis + carried_basis
    else:
        successor_key = payload.successor.symbol
        state.holdings[successor_key] = received_shares
        state.basis[successor_key]    = carried_basis
    state.identity[successor_key] = (payload.successor.symbol, payload.successor.asset_id)

    state.cash += net_cash
    return []


def _reinstate_excluded_conversions(
    all_ctxs:       list[CanonicalTransaction],
    effective_ctxs: list[CanonicalTransaction],
) -> list[CanonicalTransaction]:
    """An EXCLUDE repair targeting POSITION_CONVERSION is ineffective — the
    conversion remains in the effective canonical sequence and its findings
    are still produced (Implementation Specification §7.1/§9.3).

    Independent of portfolio_rebuilder.py's own
    _reinstate_excluded_conversions(); neither imports the other.
    """
    effective_ids = {ctx.id for ctx in effective_ctxs}
    missing = [
        ctx for ctx in all_ctxs
        if ctx.transaction_type == "POSITION_CONVERSION" and ctx.id not in effective_ids
    ]
    if not missing:
        return effective_ctxs
    merged = list(effective_ctxs) + missing
    merged.sort(key=lambda c: (c.transaction_date, c.id))
    return merged


# ══════════════════════════════════════════════════════════════════════════════
# Replay-based checks (single-pass, private replay — no import from rebuilder)
# ══════════════════════════════════════════════════════════════════════════════

def _replay_and_check(
    portfolio_id:       int,
    ctxs:               list[CanonicalTransaction],
    snapshot_dates:     list[str] | None = None,
    raw_asset_id_by_id: dict[int, int | None] | None = None,
) -> tuple[_ReplayState, list[LedgerFinding], dict[str, _ReplayState]]:
    """Single-pass replay that detects balance anomalies and captures snapshot states.

    snapshot_dates must be sorted ascending.  State is captured end-of-day:
    transactions on or before each date are included.

    Replay keys holdings by raw_symbol to preserve behavioral equivalence with
    the live portfolio engine, which stores holdings under each transaction's
    original symbol form.

    Returns:
        (final_state, findings, state_by_date)
    """
    state    = _ReplayState(holdings={}, cash=Decimal("0"))
    findings: list[LedgerFinding] = []

    snap_sorted = sorted(snapshot_dates or [])
    snap_idx    = 0
    state_by_date: dict[str, _ReplayState] = {}

    # BANPU-WP2 Step 6: local, replay-scoped duplicate-conversion-key tracking
    # (Implementation Specification §9.2 "repeated predecessor/date conversion
    # key"). Never persisted or shared across calls.
    conversion_seen: set = set()

    for ctx in ctxs:
        tx_type = ctx.transaction_type
        amount  = ctx.total_amount
        sym     = ctx.raw_symbol   # holdings key — raw for behavioral equivalence
        tx_date = ctx.transaction_date.strftime("%Y-%m-%d")

        # Capture snapshot states for all dates that are now "past" (< current tx_date)
        while snap_idx < len(snap_sorted) and snap_sorted[snap_idx] < tx_date:
            state_by_date[snap_sorted[snap_idx]] = state.copy()
            snap_idx += 1

        if tx_type in _CASH_IN_TYPES or tx_type == "DIVIDEND":
            state.cash += amount

        elif tx_type == "WITHDRAW":
            state.cash -= amount

        elif tx_type == "BUY":
            if not sym or ctx.shares <= 0:
                continue
            shares = ctx.shares
            state.cash -= amount
            if state.cash < Decimal("-0.01"):
                findings.append(LedgerFinding(
                    check_id          = "NEG_CASH_BALANCE",
                    severity          = FindingSeverity.WARNING,
                    portfolio_id      = portfolio_id,
                    transaction_ids   = [ctx.id],
                    symbol            = sym,
                    normalized_symbol = ctx.canonical_symbol,
                    title             = f"tx{ctx.id}: BUY {sym} drives cash negative ({float(state.cash):,.2f})",
                    explanation       = (
                        f"After tx{ctx.id} (BUY {sym} {float(ctx.shares)} @ "
                        f"{float(ctx.price_per_share)} on {ctx.transaction_date}), "
                        f"replayed cash drops to {float(state.cash):,.2f}. "
                        "Possible missing DEPOSIT, incorrect total_amount, or "
                        "out-of-order transaction dates."
                    ),
                    recommendation    = (
                        "Verify all deposits are recorded and that total_amount "
                        "and transaction ordering are correct."
                    ),
                    details={
                        "transaction_id": ctx.id,
                        "cash_after":     round(float(state.cash), 2),
                        "buy_amount":     round(float(amount), 2),
                        "date":           tx_date,
                    },
                ))
            state.holdings[sym] = state.holdings.get(sym, Decimal("0")) + shares
            # BANPU-WP2 Step 6: net buy amount is this holding's cost-basis
            # contribution, mirroring portfolio_rebuilder.py's own avg_cost
            # accumulation formula (independently reimplemented here).
            state.basis[sym]    = state.basis.get(sym, Decimal("0")) + amount
            state.identity[sym] = (ctx.canonical_symbol, ctx.asset_id)

        elif tx_type == "SELL":
            if not sym or ctx.shares <= 0:
                continue
            shares = ctx.shares

            if sym not in state.holdings:
                findings.append(LedgerFinding(
                    check_id          = "SELL_WITHOUT_HOLDING",
                    severity          = FindingSeverity.CRITICAL,
                    portfolio_id      = portfolio_id,
                    transaction_ids   = [ctx.id],
                    symbol            = sym,
                    normalized_symbol = ctx.canonical_symbol,
                    title             = f"tx{ctx.id}: SELL {sym} — no prior holding",
                    explanation       = (
                        f"tx{ctx.id} (SELL {sym} {float(ctx.shares)} on {ctx.transaction_date}) "
                        f"was reached during replay but {sym} was not in the portfolio. "
                        "Possible causes: missing BUY/INITIAL_POSITION, symbol alias "
                        "mismatch, or orphan SELL transaction."
                    ),
                    recommendation    = (
                        "Locate the original BUY or INITIAL_POSITION. If the symbol "
                        "was stored under a different alias, normalise it. "
                        "If the SELL is spurious, delete it."
                    ),
                    details={
                        "transaction_id": ctx.id, "symbol": sym,
                        "shares": float(shares), "date": tx_date,
                    },
                ))
                state.cash += amount
                continue

            state.cash += amount
            old_shares = state.holdings[sym]
            old_basis  = state.basis.get(sym, Decimal("0"))
            new_shares = old_shares - shares

            if new_shares < Decimal("-0.001"):
                findings.append(LedgerFinding(
                    check_id          = "NEG_SHARE_BALANCE",
                    severity          = FindingSeverity.CRITICAL,
                    portfolio_id      = portfolio_id,
                    transaction_ids   = [ctx.id],
                    symbol            = sym,
                    normalized_symbol = ctx.canonical_symbol,
                    title             = f"tx{ctx.id}: SELL {sym} creates negative share balance ({float(new_shares):.4f})",
                    explanation       = (
                        f"tx{ctx.id} (SELL {sym} {float(ctx.shares)} on {ctx.transaction_date}) "
                        f"reduces {sym} shares from {float(state.holdings[sym]):.4f} "
                        f"to {float(new_shares):.4f}. "
                        "Indicates incorrect SELL quantity, missing prior BUY, "
                        "or symbol alias mismatch."
                    ),
                    recommendation    = (
                        "Verify the SELL quantity against broker statements. "
                        "Check whether prior BUYs used a different symbol alias."
                    ),
                    details={
                        "transaction_id": ctx.id,
                        "symbol":         sym,
                        "shares_sold":    round(float(shares), 6),
                        "shares_before":  round(float(state.holdings[sym]), 6),
                        "shares_after":   round(float(new_shares), 6),
                        "date":           tx_date,
                    },
                ))

            if new_shares <= Decimal("0.001"):
                del state.holdings[sym]
                state.basis.pop(sym, None)
                state.identity.pop(sym, None)
            else:
                state.holdings[sym] = new_shares
                # Avg cost is unchanged by a SELL (mirrors portfolio_rebuilder.py);
                # basis scales proportionally with the remaining shares.
                if old_shares != 0:
                    state.basis[sym] = old_basis * new_shares / old_shares

        elif tx_type == "INITIAL_POSITION":
            if not sym or ctx.shares <= 0:
                continue
            state.holdings[sym] = state.holdings.get(sym, Decimal("0")) + ctx.shares
            state.basis[sym]    = state.basis.get(sym, Decimal("0")) + ctx.shares * ctx.price_per_share
            state.identity[sym] = (ctx.canonical_symbol, ctx.asset_id)

        elif tx_type == "QUANTITY_CORRECTION":
            if not sym:
                continue
            # qty_correction_delta is pre-parsed by the canonicalizer
            delta = ctx.qty_correction_delta  # type: ignore[assignment]

            if sym not in state.holdings:
                findings.append(LedgerFinding(
                    check_id          = "QCORR_WITHOUT_HOLDING",
                    severity          = FindingSeverity.ERROR,
                    portfolio_id      = portfolio_id,
                    transaction_ids   = [ctx.id],
                    symbol            = sym,
                    normalized_symbol = ctx.canonical_symbol,
                    title             = f"tx{ctx.id}: QUANTITY_CORRECTION for {sym} — not in holdings",
                    explanation       = (
                        f"tx{ctx.id} is a QUANTITY_CORRECTION for {sym} "
                        f"(delta={float(delta):+.4f} on {ctx.transaction_date}), "
                        f"but {sym} was not in the replayed portfolio at that point. "
                        "Replay silently skips corrections on absent symbols."
                    ),
                    recommendation    = (
                        "Check whether this correction targets a different symbol "
                        "or whether a prior BUY/INITIAL_POSITION is missing."
                    ),
                    details={
                        "transaction_id": ctx.id, "symbol": sym,
                        "delta": round(float(delta), 4), "date": tx_date,
                    },
                ))
                continue

            old_shares = state.holdings[sym]
            old_basis  = state.basis.get(sym, Decimal("0"))
            new_shares = old_shares + delta
            if delta > 0:
                # Avg cost recomputed on an increase (mirrors portfolio_rebuilder.py).
                new_basis = old_basis + delta * ctx.price_per_share
            elif old_shares != 0:
                # Avg cost unchanged on a decrease; basis scales proportionally.
                new_basis = old_basis * new_shares / old_shares
            else:
                new_basis = old_basis
            if new_shares < Decimal("-0.001"):
                findings.append(LedgerFinding(
                    check_id          = "NEG_SHARE_BALANCE",
                    severity          = FindingSeverity.CRITICAL,
                    portfolio_id      = portfolio_id,
                    transaction_ids   = [ctx.id],
                    symbol            = sym,
                    normalized_symbol = ctx.canonical_symbol,
                    title             = f"tx{ctx.id}: QUANTITY_CORRECTION {sym} creates negative balance ({float(new_shares):.4f})",
                    explanation       = (
                        f"tx{ctx.id} (QUANTITY_CORRECTION {sym} delta={float(delta):+.4f} "
                        f"on {ctx.transaction_date}) would leave {float(new_shares):.4f} shares."
                    ),
                    recommendation    = "Review and correct the quantity correction delta.",
                    details={
                        "transaction_id": ctx.id,
                        "symbol":         sym,
                        "delta":          round(float(delta), 4),
                        "shares_before":  round(float(state.holdings[sym]), 6),
                        "shares_after":   round(float(new_shares), 6),
                    },
                ))

            if new_shares <= Decimal("0.001"):
                del state.holdings[sym]
                state.basis.pop(sym, None)
                state.identity.pop(sym, None)
            else:
                state.holdings[sym] = new_shares
                state.basis[sym]    = new_basis

        elif tx_type == "POSITION_CONVERSION":
            findings.extend(_apply_position_conversion(
                portfolio_id, ctx, ctxs, state, conversion_seen, raw_asset_id_by_id,
            ))

    # Capture remaining snapshot dates (on or after last transaction)
    while snap_idx < len(snap_sorted):
        state_by_date[snap_sorted[snap_idx]] = state.copy()
        snap_idx += 1

    return state, findings, state_by_date


# ══════════════════════════════════════════════════════════════════════════════
# DB consistency checks (compare replayed state against stored DB rows)
# ══════════════════════════════════════════════════════════════════════════════

def _check_cash_consistency(
    portfolio_id:  int,
    portfolio_cash: float,
    replayed_cash:  Decimal,
    tolerance:      float = _CASH_TOLERANCE,
) -> list[LedgerFinding]:
    """CHECK 8 (consistency) — Replayed final cash vs Portfolio.cash_balance."""
    diff = float(replayed_cash) - portfolio_cash
    if abs(diff) <= tolerance:
        return []
    return [LedgerFinding(
        check_id          = "CASH_MISMATCH",
        severity          = FindingSeverity.ERROR,
        portfolio_id      = portfolio_id,
        transaction_ids   = [],
        symbol            = None,
        normalized_symbol = None,
        title             = (
            f"Cash mismatch: replayed={float(replayed_cash):,.2f}  "
            f"stored={portfolio_cash:,.2f}  (Δ{diff:+,.2f})"
        ),
        explanation       = (
            f"Replaying all transactions for portfolio {portfolio_id} produces "
            f"a final cash balance of {float(replayed_cash):,.2f}, "
            f"but Portfolio.cash_balance is {portfolio_cash:,.2f} "
            f"(difference: {diff:+,.2f}). "
            "The live portfolio state has drifted from the transaction ledger."
        ),
        recommendation    = (
            "Run rebuild_portfolio to resynchronise the portfolio state from "
            "the ledger.  If the ledger is itself corrupted, identify the root "
            "cause first."
        ),
        details={
            "replayed_cash": round(float(replayed_cash), 2),
            "stored_cash":   round(portfolio_cash, 2),
            "difference":    round(diff, 2),
        },
    )]


def _check_holdings_consistency(
    portfolio_id:    int,
    portfolio_items: list[Any],
    replay_state:    _ReplayState,
    shares_tol:      float = _SHARES_TOLERANCE,
    conversion_aware: bool = False,
) -> list[LedgerFinding]:
    """CHECK 9 — Replayed final holdings vs current PortfolioItem rows."""
    if conversion_aware:
        return _check_conversion_holdings_consistency(
            portfolio_id, portfolio_items, replay_state, shares_tol,
        )

    findings: list[LedgerFinding] = []
    current = {item.symbol.strip().upper(): item for item in portfolio_items}
    replay  = replay_state.holdings

    for sym in sorted(set(current) | set(replay)):
        curr = current.get(sym)
        repl = replay.get(sym)

        if curr and repl is None:
            findings.append(LedgerFinding(
                check_id          = "HOLDINGS_MISMATCH",
                severity          = FindingSeverity.ERROR,
                portfolio_id      = portfolio_id,
                transaction_ids   = [],
                symbol            = sym,
                normalized_symbol = sym,
                title             = f"Holdings mismatch: {sym} in DB but not in replay",
                explanation       = (
                    f"PortfolioItem({sym}, shares={curr.shares}) exists in the DB "
                    "but the ledger replay produces no position for this symbol. "
                    "The portfolio state has diverged from the transaction ledger."
                ),
                recommendation    = "Run rebuild_portfolio to resync holdings.",
                details={"symbol": sym, "db_shares": curr.shares, "replay_shares": None},
            ))
        elif repl is not None and curr is None:
            findings.append(LedgerFinding(
                check_id          = "HOLDINGS_MISMATCH",
                severity          = FindingSeverity.ERROR,
                portfolio_id      = portfolio_id,
                transaction_ids   = [],
                symbol            = sym,
                normalized_symbol = sym,
                title             = f"Holdings mismatch: {sym} in replay but not in DB",
                explanation       = (
                    f"Ledger replay produces {float(repl):.4f} shares of {sym}, "
                    "but no PortfolioItem row exists for this symbol in the DB."
                ),
                recommendation    = "Run rebuild_portfolio to add missing holdings.",
                details={"symbol": sym, "db_shares": None, "replay_shares": round(float(repl), 6)},
            ))
        elif curr and repl is not None:
            diff = float(repl) - float(curr.shares)
            if abs(diff) > shares_tol:
                findings.append(LedgerFinding(
                    check_id          = "HOLDINGS_MISMATCH",
                    severity          = FindingSeverity.ERROR,
                    portfolio_id      = portfolio_id,
                    transaction_ids   = [],
                    symbol            = sym,
                    normalized_symbol = sym,
                    title             = (
                        f"Holdings mismatch: {sym} shares differ "
                        f"(DB={curr.shares:.4f} replay={float(repl):.4f})"
                    ),
                    explanation       = (
                        f"{sym}: DB has {curr.shares:.6f} shares, "
                        f"replay produces {float(repl):.6f} (Δ{diff:+.6f})."
                    ),
                    recommendation    = "Run rebuild_portfolio to resync holdings.",
                    details={
                        "symbol":        sym,
                        "db_shares":     round(float(curr.shares), 6),
                        "replay_shares": round(float(repl), 6),
                        "difference":    round(diff, 6),
                    },
                ))

    return findings


def _check_conversion_holdings_consistency(
    portfolio_id:    int,
    portfolio_items: list[Any],
    replay_state:    _ReplayState,
    shares_tol:      float,
) -> list[LedgerFinding]:
    """Five-field DB comparison for a conversion-bearing replay.

    Pair by authoritative asset ID first and canonical symbol second, then
    expose asset_id, symbol, shares, average cost, and basis independently.
    The legacy symbol-only CHECK 9 path remains byte-for-byte unchanged.
    """
    findings: list[LedgerFinding] = []
    current_by_symbol = {item.symbol.strip().upper(): item for item in portfolio_items}
    current_by_asset_id = {
        item.asset_id: item
        for item in portfolio_items
        if getattr(item, "asset_id", None) is not None
    }
    paired_item_ids: set[int] = set()

    def add_finding(symbol: str, field_name: str, current_value: Any, replay_value: Any) -> None:
        findings.append(LedgerFinding(
            check_id="HOLDINGS_MISMATCH",
            severity=FindingSeverity.ERROR,
            portfolio_id=portfolio_id,
            transaction_ids=[],
            symbol=symbol,
            normalized_symbol=symbol,
            title=f"Holdings mismatch: {symbol} {field_name} differs",
            explanation=(
                f"{symbol}: DB {field_name}={current_value!r}, "
                f"replay {field_name}={replay_value!r}."
            ),
            recommendation="Run rebuild_portfolio to resync holdings.",
            details={
                "symbol": symbol,
                "field": field_name,
                "db_value": current_value,
                "replay_value": replay_value,
            },
        ))

    for raw_key in sorted(replay_state.holdings):
        replay_shares = replay_state.holdings[raw_key]
        replay_basis = replay_state.basis.get(raw_key, Decimal("0"))
        canonical_symbol, replay_asset_id = replay_state.identity.get(raw_key, (raw_key, None))
        replay_symbol = (canonical_symbol or raw_key).strip().upper()
        current_item = (
            current_by_asset_id.get(replay_asset_id)
            if replay_asset_id is not None
            else None
        ) or current_by_symbol.get(replay_symbol)

        if current_item is None:
            add_finding(replay_symbol, "*", None, {
                "asset_id": replay_asset_id,
                "symbol": replay_symbol,
                "shares": str(replay_shares),
                "average_cost": str(replay_basis / replay_shares),
                "basis": str(replay_basis),
            })
            continue

        paired_item_ids.add(id(current_item))
        current_symbol = current_item.symbol.strip().upper()
        current_shares = Decimal(str(current_item.shares))
        current_avg_cost = Decimal(str(current_item.avg_cost))
        current_basis = current_shares * current_avg_cost
        replay_avg_cost = replay_basis / replay_shares

        comparisons = [
            ("asset_id", getattr(current_item, "asset_id", None), replay_asset_id, Decimal("0")),
            ("symbol", current_symbol, replay_symbol, Decimal("0")),
            ("shares", current_shares, replay_shares, Decimal(str(shares_tol))),
            ("average_cost", current_avg_cost, replay_avg_cost, _CONVERSION_BASIS_TOLERANCE),
            ("basis", current_basis, replay_basis, _CONVERSION_BASIS_TOLERANCE),
        ]
        for field_name, current_value, replay_value, tolerance in comparisons:
            if isinstance(current_value, Decimal) and isinstance(replay_value, Decimal):
                matches = abs(current_value - replay_value) <= tolerance
            else:
                matches = current_value == replay_value
            if not matches:
                add_finding(
                    replay_symbol,
                    field_name,
                    str(current_value) if isinstance(current_value, Decimal) else current_value,
                    str(replay_value) if isinstance(replay_value, Decimal) else replay_value,
                )

    for current_item in portfolio_items:
        if id(current_item) not in paired_item_ids:
            symbol = current_item.symbol.strip().upper()
            add_finding(symbol, "*", {
                "asset_id": getattr(current_item, "asset_id", None),
                "symbol": symbol,
                "shares": current_item.shares,
                "average_cost": current_item.avg_cost,
            }, None)

    return findings


def _check_snapshot_cash_consistency(
    portfolio_id:  int,
    snapshots:     list[Any],
    state_by_date: dict[str, _ReplayState],
    cash_tol:      float = _CASH_TOLERANCE,
) -> list[LedgerFinding]:
    """CHECK 10 — Replayed cash at each snapshot date vs stored snapshot.cash_balance.

    This check is free (no yfinance) and catches the most common snapshot drift.
    """
    findings: list[LedgerFinding] = []
    for snap in snapshots:
        date = snap.snapshot_date
        if date not in state_by_date:
            continue
        replay_cash = float(state_by_date[date].cash)
        stored_cash = float(snap.cash_balance or 0.0)
        diff        = replay_cash - stored_cash
        if abs(diff) <= cash_tol:
            continue
        findings.append(LedgerFinding(
            check_id          = "SNAPSHOT_CASH_MISMATCH",
            severity          = FindingSeverity.WARNING,
            portfolio_id      = portfolio_id,
            transaction_ids   = [],
            symbol            = None,
            normalized_symbol = None,
            title             = (
                f"Snapshot {date}: cash mismatch "
                f"(replayed={replay_cash:,.2f} stored={stored_cash:,.2f} Δ{diff:+,.2f})"
            ),
            explanation       = (
                f"On {date}, replaying the ledger yields cash={replay_cash:,.2f}, "
                f"but the stored snapshot has cash_balance={stored_cash:,.2f} "
                f"(Δ{diff:+,.2f}). "
                "Indicates a transaction was recorded/modified after the snapshot "
                "was taken, or the snapshot was computed with stale cash data."
            ),
            recommendation    = "Run rebuild_portfolio to recalculate this snapshot.",
            details={
                "snapshot_date": date,
                "snapshot_id":   snap.id,
                "replay_cash":   round(replay_cash, 2),
                "stored_cash":   round(stored_cash, 2),
                "difference":    round(diff, 2),
            },
        ))
    return findings


# ══════════════════════════════════════════════════════════════════════════════
# Price-gated check (optional, async, requires yfinance)
# ══════════════════════════════════════════════════════════════════════════════

async def _check_impossible_prices(
    portfolio_id:        int,
    ctxs:                list[CanonicalTransaction],
    price_deviation_pct: float = 100.0,
) -> list[LedgerFinding]:
    """CHECK 11 — Import/buy prices deviating wildly from historical market prices.

    Requires yfinance.  Gracefully skips symbols where data is unavailable.
    """
    findings: list[LedgerFinding] = []

    equity_ctxs = [
        ctx for ctx in ctxs
        if ctx.transaction_type in _BUY_TYPES
        and ctx.raw_symbol
        and ctx.price_per_share > 0
    ]
    if not equity_ctxs:
        return findings

    # yfinance symbols and date range
    yf_symbols = list({ctx.canonical_symbol for ctx in equity_ctxs if ctx.canonical_symbol})
    min_date   = min(ctx.transaction_date for ctx in equity_ctxs)
    min_date_dt = datetime(min_date.year, min_date.month, min_date.day)
    delta_days  = (datetime.utcnow() - min_date_dt).days
    period      = "max" if delta_days > 5 * 365 else "10y" if delta_days > 3 * 365 else "5y"

    # Build {yf_symbol: {date_str: close_price}}
    price_matrix: dict[str, dict[str, float | None]] = {}

    for yf_sym in yf_symbols:
        try:
            df: pd.DataFrame | None = await asyncio.to_thread(
                fetch_history, yf_sym, period, "1d"
            )
        except Exception as exc:
            _log.warning("price_check: fetch failed sym=%s: %s", yf_sym, exc)
            continue

        if df is None or df.empty:
            continue

        df_sorted = df.sort_index()
        df_dates  = df_sorted.index.strftime("%Y-%m-%d").tolist()
        df_closes = [
            float(v) if pd.notna(v) and float(v) > 0 else None
            for v in df_sorted["Close"]
        ]

        date_price: dict[str, float | None] = {}
        for ctx in equity_ctxs:
            if ctx.canonical_symbol != yf_sym:
                continue
            ds = ctx.transaction_date.strftime("%Y-%m-%d")
            if ds not in date_price:
                idx = bisect.bisect_right(df_dates, ds) - 1
                date_price[ds] = df_closes[idx] if idx >= 0 else None

        price_matrix[yf_sym] = date_price

    # Compare recorded vs market price
    for ctx in equity_ctxs:
        yf_sym   = ctx.canonical_symbol or ""
        date_str = ctx.transaction_date.strftime("%Y-%m-%d")
        market   = price_matrix.get(yf_sym, {}).get(date_str)
        if market is None:
            continue
        recorded  = float(ctx.price_per_share)
        deviation = abs(recorded - market) / market * 100
        if deviation <= price_deviation_pct:
            continue
        findings.append(LedgerFinding(
            check_id          = "IMPOSSIBLE_PRICE",
            severity          = FindingSeverity.ERROR,
            portfolio_id      = portfolio_id,
            transaction_ids   = [ctx.id],
            symbol            = ctx.raw_symbol,
            normalized_symbol = yf_sym,
            title             = (
                f"tx{ctx.id}: {ctx.transaction_type} {ctx.raw_symbol} "
                f"price {recorded:.2f} deviates {deviation:.0f}% "
                f"from market {market:.2f}"
            ),
            explanation       = (
                f"tx{ctx.id} ({ctx.transaction_type} {ctx.raw_symbol} on {date_str}) "
                f"records price={recorded:.4f}, but yfinance shows ≈{market:.4f} "
                f"on that date (deviation={deviation:.1f}%). "
                "Possible causes: price entry error, split-adjustment mismatch, "
                "currency conversion not applied, or wrong symbol."
            ),
            recommendation    = (
                "Verify against broker contract note. "
                "Check for stock splits or currency issues. "
                "Correct price_per_share if needed."
            ),
            details={
                "transaction_id":  ctx.id,
                "symbol":          ctx.raw_symbol,
                "yfinance_symbol": yf_sym,
                "date":            date_str,
                "recorded_price":  round(recorded, 4),
                "market_price":    round(market, 4),
                "deviation_pct":   round(deviation, 1),
                "type":            ctx.transaction_type,
            },
        ))
    return findings


# ══════════════════════════════════════════════════════════════════════════════
# Runtime consultation (Stage R1 — Asset Definition Runtime, read-only shadow)
# ══════════════════════════════════════════════════════════════════════════════
#
# M11 brief: introduce the Ledger Validator as the runtime's first consumer.
# Legacy transaction-type logic remains authoritative; the runtime is asked
# the same question a second way and any disagreement is recorded as a
# RuntimeValidationFinding — never raised, never allowed to change
# report.findings or report.overall_severity.
#
# The ledger carries no per-transaction asset_type column at all (M9 TDD
# Section 10 challenge: "cash is a column, not an asset"; Transaction only
# ever names a raw symbol string or nothing). So this stage can only shadow
# the decisions the legacy code already makes *implicitly* by which
# transaction_type it is looking at:
#
#   1. DIVIDEND transactions are accepted as a valid cash-additive flow
#      (_replay_and_check) with no per-asset validation. The only kind in
#      the library capable of paying a dividend is EQUITY, so the runtime
#      counterpart question is: does EQUITY grant FlowType.DIVIDEND?
#   2. SYMBOL_ALIAS (_check_symbol_aliases) merges multiple raw symbols that
#      resolve to the same ReplayKey into one holding, unconditionally
#      (ADR-005). The runtime counterpart: does EQUITY permit
#      RelationshipKind.SAME_ENTITY?
#   3. DEPOSIT / WITHDRAW / INITIAL_CASH never touch state.holdings, only
#      state.cash (_replay_and_check) — legacy already treats them as
#      non-share-bearing cash movements. The runtime counterpart exercises
#      BindingResolver.resolve_numeraire() (M9 TDD Section 2.3's documented
#      transitional special case for cash, unused by any caller until now):
#      is the numeraire's acquisition_semantics NOT_TRANSACTABLE?
#
# Deliberately absent: an Axis-6 (event-family) consultation. No transaction
# type in this ledger schema corresponds to SPLIT/MERGER/SPIN_OFF/RENAME/
# SUSPENSION/DELISTING, so there is no legacy decision to shadow — inventing
# one would compare the runtime against a fabricated "legacy result" rather
# than a real one.

def _consult_runtime_capabilities(
    ctxs: list[CanonicalTransaction],
) -> RuntimeConsultationLog:
    """Ask the Asset Definition Runtime the questions Legacy logic already
    answers implicitly; record any disagreement. Never raises — a defect in
    the runtime itself (e.g. boot validation failure) becomes one
    MissingBinding finding, consistent with this module's "never raises to
    the caller" invariant.
    """
    try:
        registry = DefinitionRegistry.build()
    except DefinitionRegistryError as exc:
        return RuntimeConsultationLog(
            consulted=0,
            agreements=0,
            findings=(RuntimeValidationFinding(
                category        = RuntimeFindingCategory.MISSING_BINDING.value,
                check_id        = "RUNTIME_REGISTRY_BOOT_FAILED",
                transaction_ids = (),
                binding         = "-",
                question        = "DefinitionRegistry.build()",
                legacy_result   = True,
                runtime_result  = None,
                detail          = str(exc),
            ),),
        )

    resolver = BindingResolver(registry)
    findings: list[RuntimeValidationFinding] = []
    consulted  = 0
    agreements = 0

    # ── 1. DIVIDEND ⇔ EQUITY grants FlowType.DIVIDEND ─────────────────────
    dividend_ids = tuple(ctx.id for ctx in ctxs if ctx.transaction_type == "DIVIDEND")
    if dividend_ids:
        consulted += 1
        legacy_result = True  # legacy accepts DIVIDEND unconditionally today
        try:
            runtime_result = resolver.resolve(AssetType.EQUITY.value).grants_flow(FlowType.DIVIDEND)
        except UnresolvedBindingError as exc:
            findings.append(RuntimeValidationFinding(
                category=RuntimeFindingCategory.MISSING_BINDING.value,
                check_id="RUNTIME_DIVIDEND_FLOW", transaction_ids=dividend_ids,
                binding=AssetType.EQUITY.value, question="grants_flow(DIVIDEND)",
                legacy_result=legacy_result, runtime_result=None, detail=str(exc),
            ))
        else:
            if runtime_result == legacy_result:
                agreements += 1
            else:
                findings.append(RuntimeValidationFinding(
                    category=RuntimeFindingCategory.RUNTIME_MISMATCH.value,
                    check_id="RUNTIME_DIVIDEND_FLOW", transaction_ids=dividend_ids,
                    binding=AssetType.EQUITY.value, question="grants_flow(DIVIDEND)",
                    legacy_result=legacy_result, runtime_result=runtime_result,
                    detail=(
                        f"{len(dividend_ids)} DIVIDEND transaction(s) are accepted as a "
                        "valid cash flow by legacy replay, but the runtime's EQUITY "
                        "capability view does not grant FlowType.DIVIDEND."
                    ),
                ))

    # ── 2. SYMBOL_ALIAS merge ⇔ EQUITY permits RelationshipKind.SAME_ENTITY ─
    raw_by_key: dict[object, set[str]] = defaultdict(set)
    ids_by_key: dict[object, list[int]] = defaultdict(list)
    for ctx in ctxs:
        if not ctx.raw_symbol:
            continue
        key = replay_key(ctx)
        raw_by_key[key].add(ctx.raw_symbol)
        ids_by_key[key].append(ctx.id)
    merged_tx_ids = tuple(
        tx_id
        for key, raws in raw_by_key.items()
        if len(raws) > 1
        for tx_id in ids_by_key[key]
    )
    if merged_tx_ids:
        consulted += 1
        legacy_result = True  # legacy merges aliased symbols unconditionally (ADR-005)
        try:
            runtime_result = resolver.resolve(AssetType.EQUITY.value).permits_relationship(
                RelationshipKind.SAME_ENTITY
            )
        except UnresolvedBindingError as exc:
            findings.append(RuntimeValidationFinding(
                category=RuntimeFindingCategory.MISSING_BINDING.value,
                check_id="RUNTIME_SYMBOL_ALIAS_RELATIONSHIP", transaction_ids=merged_tx_ids,
                binding=AssetType.EQUITY.value, question="permits_relationship(SAME_ENTITY)",
                legacy_result=legacy_result, runtime_result=None, detail=str(exc),
            ))
        else:
            if runtime_result == legacy_result:
                agreements += 1
            else:
                findings.append(RuntimeValidationFinding(
                    category=RuntimeFindingCategory.RUNTIME_MISMATCH.value,
                    check_id="RUNTIME_SYMBOL_ALIAS_RELATIONSHIP", transaction_ids=merged_tx_ids,
                    binding=AssetType.EQUITY.value, question="permits_relationship(SAME_ENTITY)",
                    legacy_result=legacy_result, runtime_result=runtime_result,
                    detail=(
                        f"{len(merged_tx_ids)} transaction(s) across aliased raw symbols "
                        "are merged into one holding by legacy replay (ADR-005), but the "
                        "runtime's EQUITY capability view does not permit "
                        "RelationshipKind.SAME_ENTITY."
                    ),
                ))

    # ── 3. Cash-movement types ⇔ CASH numeraire is NOT_TRANSACTABLE ────────
    cash_move_ids = tuple(
        ctx.id for ctx in ctxs if ctx.transaction_type in _CASH_IN_TYPES or ctx.transaction_type == "WITHDRAW"
    )
    if cash_move_ids:
        consulted += 1
        legacy_result = True  # legacy never routes these through the holdings/shares path
        try:
            runtime_result = (
                resolver.resolve_numeraire().acquisition_semantics() == AcquisitionSemantics.NOT_TRANSACTABLE
            )
        except Exception as exc:  # NumeraireNotResolvedError — library defect, not a per-asset one
            findings.append(RuntimeValidationFinding(
                category=RuntimeFindingCategory.MISSING_BINDING.value,
                check_id="RUNTIME_CASH_NUMERAIRE", transaction_ids=cash_move_ids,
                binding=AssetType.CASH.value, question="resolve_numeraire().acquisition_semantics()",
                legacy_result=legacy_result, runtime_result=None, detail=str(exc),
            ))
        else:
            if runtime_result == legacy_result:
                agreements += 1
            else:
                findings.append(RuntimeValidationFinding(
                    category=RuntimeFindingCategory.RUNTIME_MISMATCH.value,
                    check_id="RUNTIME_CASH_NUMERAIRE", transaction_ids=cash_move_ids,
                    binding=AssetType.CASH.value, question="resolve_numeraire().acquisition_semantics()",
                    legacy_result=legacy_result, runtime_result=runtime_result,
                    detail=(
                        f"{len(cash_move_ids)} DEPOSIT/WITHDRAW/INITIAL_CASH transaction(s) are "
                        "replayed as non-share-bearing cash movements by legacy logic, but the "
                        "runtime's CASH numeraire capability view is not NOT_TRANSACTABLE."
                    ),
                ))

    return RuntimeConsultationLog(consulted=consulted, agreements=agreements, findings=tuple(findings))


# ══════════════════════════════════════════════════════════════════════════════
# Public API
# ══════════════════════════════════════════════════════════════════════════════

async def validate_portfolio_ledger(
    db:                  Session,
    portfolio_id:        int,
    workspace_id:        int,
    fetch_prices:        bool  = False,
    price_deviation_pct: float = 100.0,
    date_skew_warning:   int   = _DATE_SKEW_WARNING_DAYS,
    date_skew_error:     int   = _DATE_SKEW_ERROR_DAYS,
    cash_tolerance:      float = _CASH_TOLERANCE,
    shares_tolerance:    float = _SHARES_TOLERANCE,
    repairs:             list[Any] | None = None,
    mode:                Literal["raw", "effective"] = "raw",
) -> LedgerValidationReport:
    """Validate the transaction ledger for a single portfolio.

    Read-only.  Never modifies the database.  Never raises.

    Args:
        db:                  SQLAlchemy session (caller manages lifecycle).
        portfolio_id:        Portfolio to validate.
        workspace_id:        Owning workspace.
        fetch_prices:        Enable IMPOSSIBLE_PRICE check (contacts yfinance).
        price_deviation_pct: Flag price deviations beyond this % from market.
        date_skew_warning:   Days of created_at/transaction_date skew → WARNING.
        date_skew_error:     Days of skew → ERROR.
        cash_tolerance:      Absolute THB tolerance for cash comparison.
        shares_tolerance:    Absolute shares tolerance for holdings comparison.
        repairs:             Active LedgerRepair rows for this portfolio.  When
                             None, behaviour is identical to Phase 6.7A (mode is
                             ignored).
        mode:                "raw"       — ignore repairs completely (default).
                             "effective" — apply apply_repair_overlay() before
                             running every validation rule; also suppresses
                             findings covered by SUPPRESS_FINDING repairs.
                             Has no effect when repairs is None.
    """
    t_start = time.monotonic()

    # ── Load portfolio ────────────────────────────────────────────────────────
    portfolio = resolve_portfolio_reference(db, portfolio_id, workspace_id)
    if portfolio is None:
        return LedgerValidationReport(
            portfolio_id           = portfolio_id,
            portfolio_name         = "?",
            transactions_inspected = 0,
            findings               = [LedgerFinding(
                check_id="PORTFOLIO_NOT_FOUND",
                severity=FindingSeverity.CRITICAL,
                portfolio_id=portfolio_id,
                transaction_ids=[],
                symbol=None, normalized_symbol=None,
                title=f"Portfolio {portfolio_id} not found in workspace {workspace_id}",
                explanation=f"No portfolio with id={portfolio_id}.",
                recommendation="Verify the portfolio ID.",
            )],
            elapsed_seconds = time.monotonic() - t_start,
        )

    # ── Load data ─────────────────────────────────────────────────────────────
    raw_txs: list[Transaction] = (
        db.query(Transaction)
        .filter_by(portfolio_id=portfolio_id)
        .order_by(Transaction.transaction_date, Transaction.id)
        .all()
    )
    portfolio_items: list[PortfolioItem] = (
        db.query(PortfolioItem)
        .filter_by(portfolio_id=portfolio_id)
        .all()
    )
    snapshots: list[PortfolioSnapshot] = (
        db.query(PortfolioSnapshot)
        .filter_by(portfolio_id=portfolio_id)
        .order_by(PortfolioSnapshot.snapshot_date)
        .all()
    )
    snap_dates = [s.snapshot_date for s in snapshots]

    # ── Canonicalize — single preprocessing pass ──────────────────────────────
    # M5 Track B Stage 4: same per-portfolio cutover gate as portfolio_rebuilder.py
    # (never global — TDD §9). See that file's own comment for the full rationale.
    ctxs: list[CanonicalTransaction] = list(
        canonicalize_transactions(raw_txs, prefer_asset_id=bool(portfolio.replay_asset_id_native))
    )

    # ── Effective mode: apply repair overlay ──────────────────────────────────
    # Build provenance map and SUPPRESS_FINDING lookup before running checks.
    # When repairs is None the mode parameter is ignored (Phase 6.7A compat).
    _effective = mode == "effective" and repairs is not None
    _provenance: dict[int, str] = {}
    _suppress_keys: set[tuple[str, int]] = set()

    if _effective:
        _raw_ctxs = ctxs
        effective_tuple, _provenance = apply_repair_overlay(tuple(ctxs), repairs)
        # BANPU-WP2 §7.1/§9.3: an EXCLUDE repair targeting a POSITION_CONVERSION
        # is ineffective — the conversion remains in the effective canonical
        # sequence regardless of any repair overlay. ledger_repair.py itself is
        # unchanged; this is the validator's own consumer-boundary enforcement,
        # independent of portfolio_rebuilder.py's equivalent guarantee.
        ctxs = _reinstate_excluded_conversions(_raw_ctxs, list(effective_tuple))
        for r in repairs:  # type: ignore[union-attr]
            if (
                getattr(r, "repair_type", None) == "SUPPRESS_FINDING"
                and getattr(r, "reason_code", None)
                and getattr(r, "transaction_id", None) is not None
            ):
                _suppress_keys.add((r.reason_code, r.transaction_id))

    report = LedgerValidationReport(
        portfolio_id           = portfolio_id,
        portfolio_name         = portfolio.name,
        transactions_inspected = len(ctxs),
    )
    if not ctxs:
        return report

    # ── Stage R1 runtime consultation (read-only shadow; never raises) ────────
    try:
        report.runtime_consultation = _consult_runtime_capabilities(ctxs)
    except Exception as exc:
        _log.warning("runtime consultation failed portfolio=%d: %s", portfolio_id, exc)
        report.runtime_consultation = None

    findings: list[LedgerFinding] = []

    # ── Structural checks ─────────────────────────────────────────────────────
    findings.extend(_check_duplicate_initial_positions(portfolio_id, ctxs))
    findings.extend(_check_symbol_aliases(portfolio_id, ctxs))
    findings.extend(_check_null_symbols(portfolio_id, ctxs))
    findings.extend(_check_zero_shares(portfolio_id, ctxs))
    findings.extend(_check_zero_prices(portfolio_id, ctxs))
    findings.extend(_check_pre_portfolio_transactions(portfolio_id, portfolio.created_at, ctxs))
    findings.extend(_check_date_skew(portfolio_id, ctxs, date_skew_warning, date_skew_error))
    findings.extend(_check_duplicate_fingerprints(portfolio_id, ctxs))

    # ── Replay-based checks ───────────────────────────────────────────────────
    # BANPU-WP2 Step 7: raw asset_id map, independent of CanonicalTransaction's
    # legacy-mode-gated asset_id, so POSITION_CONVERSION identity validation
    # can compare against the transaction row's own persisted asset_id exactly
    # as portfolio_rebuilder.py's preflight does (see _apply_position_conversion's
    # docstring). raw_txs is the same already-loaded query result used above.
    _raw_asset_id_by_id = {tx.id: getattr(tx, "asset_id", None) for tx in raw_txs}
    final_state, replay_findings, state_by_date = _replay_and_check(
        portfolio_id       = portfolio_id,
        ctxs               = ctxs,
        snapshot_dates     = snap_dates,
        raw_asset_id_by_id = _raw_asset_id_by_id,
    )
    findings.extend(replay_findings)

    # ── DB consistency checks ─────────────────────────────────────────────────
    findings.extend(_check_cash_consistency(
        portfolio_id   = portfolio_id,
        portfolio_cash = float(portfolio.cash_balance),
        replayed_cash  = final_state.cash,
        tolerance      = cash_tolerance,
    ))
    findings.extend(_check_holdings_consistency(
        portfolio_id    = portfolio_id,
        portfolio_items = portfolio_items,
        replay_state    = final_state,
        shares_tol      = shares_tolerance,
        conversion_aware = any(
            ctx.transaction_type == "POSITION_CONVERSION" for ctx in ctxs
        ),
    ))
    findings.extend(_check_snapshot_cash_consistency(
        portfolio_id  = portfolio_id,
        snapshots     = snapshots,
        state_by_date = state_by_date,
    ))

    # ── Price check (optional, async) ─────────────────────────────────────────
    if fetch_prices:
        try:
            price_findings = await _check_impossible_prices(
                portfolio_id        = portfolio_id,
                ctxs                = ctxs,
                price_deviation_pct = price_deviation_pct,
            )
            findings.extend(price_findings)
            report.price_check_performed = True
        except Exception as exc:
            _log.warning("price check failed portfolio=%d: %s", portfolio_id, exc)
            findings.append(LedgerFinding(
                check_id          = "PRICE_CHECK_FAILED",
                severity          = FindingSeverity.WARNING,
                portfolio_id      = portfolio_id,
                transaction_ids   = [],
                symbol            = None,
                normalized_symbol = None,
                title             = "IMPOSSIBLE_PRICE check could not complete",
                explanation       = f"yfinance error: {exc}",
                recommendation    = "Check network connectivity and retry with --price-check.",
                details={"error": str(exc)},
            ))

    # ── Effective mode: tag findings with provenance and suppress as needed ───
    # Every finding produced in effective mode is tagged with origin="RAW".
    # Findings covered by a SUPPRESS_FINDING repair (check_id matches
    # reason_code AND at least one transaction_id matches) are dropped from
    # the report — they become "resolved" in the comparison.
    # This block is a no-op when repairs is None (raw mode, Phase 6.7A compat).
    if _effective:
        tagged: list[LedgerFinding] = []
        for f in findings:
            # BANPU-WP2 §9.3: a SUPPRESS_FINDING repair must never silence an
            # active POSITION_CONVERSION finding.
            is_suppressed = bool(
                _suppress_keys
                and not f.check_id.startswith("POSITION_CONVERSION_")
                and any(
                    (f.check_id, tx_id) in _suppress_keys
                    for tx_id in f.transaction_ids
                )
            )
            if not is_suppressed:
                tagged.append(dataclasses.replace(f, origin="RAW"))
            # suppressed findings are intentionally dropped
        findings = tagged

    # ── Sort findings: CRITICAL first, then ERROR, then WARNING; within each
    #    severity sort by check_id for deterministic output ────────────────────
    report.findings = sorted(findings, key=lambda f: (_SEV_ORDER[f.severity], f.check_id))
    report.elapsed_seconds = time.monotonic() - t_start
    return report


async def validate_all_ledgers(
    db:                  Session,
    workspace_id:        int,
    fetch_prices:        bool  = False,
    price_deviation_pct: float = 100.0,
    date_skew_warning:   int   = _DATE_SKEW_WARNING_DAYS,
    date_skew_error:     int   = _DATE_SKEW_ERROR_DAYS,
    cash_tolerance:      float = _CASH_TOLERANCE,
    shares_tolerance:    float = _SHARES_TOLERANCE,
) -> list[LedgerValidationReport]:
    """Validate every portfolio in a workspace."""
    portfolios = (
        db.query(Portfolio)
        .filter_by(workspace_id=workspace_id)
        .order_by(Portfolio.id)
        .all()
    )
    results: list[LedgerValidationReport] = []
    for p in portfolios:
        r = await validate_portfolio_ledger(
            db                  = db,
            portfolio_id        = p.id,
            workspace_id        = workspace_id,
            fetch_prices        = fetch_prices,
            price_deviation_pct = price_deviation_pct,
            date_skew_warning   = date_skew_warning,
            date_skew_error     = date_skew_error,
            cash_tolerance      = cash_tolerance,
            shares_tolerance    = shares_tolerance,
        )
        results.append(r)
    return results


async def compare_ledger_validation(
    db:                  Session,
    portfolio_id:        int,
    workspace_id:        int,
    repairs:             list[Any],
    fetch_prices:        bool  = False,
    price_deviation_pct: float = 100.0,
    date_skew_warning:   int   = _DATE_SKEW_WARNING_DAYS,
    date_skew_error:     int   = _DATE_SKEW_ERROR_DAYS,
    cash_tolerance:      float = _CASH_TOLERANCE,
    shares_tolerance:    float = _SHARES_TOLERANCE,
) -> LedgerValidationComparison:
    """Validate the ledger in both raw and effective modes and return a comparison.

    Runs validate_portfolio_ledger() twice — once with mode="raw" and once with
    mode="effective" using the supplied repairs — then computes the sets of
    resolved, remaining, and newly-introduced findings.

    Read-only.  Never modifies the database.  Never raises.

    Args:
        repairs: Active LedgerRepair rows pre-loaded by the caller.  An empty
                 list is valid; effective_report will equal raw_report.
    """
    common: dict[str, Any] = dict(
        db                  = db,
        portfolio_id        = portfolio_id,
        workspace_id        = workspace_id,
        fetch_prices        = fetch_prices,
        price_deviation_pct = price_deviation_pct,
        date_skew_warning   = date_skew_warning,
        date_skew_error     = date_skew_error,
        cash_tolerance      = cash_tolerance,
        shares_tolerance    = shares_tolerance,
    )
    raw_report = await validate_portfolio_ledger(mode="raw", **common)
    eff_report = await validate_portfolio_ledger(
        repairs=repairs, mode="effective", **common
    )

    raw_keys = {_finding_key(f) for f in raw_report.findings}
    eff_keys = {_finding_key(f) for f in eff_report.findings}

    return LedgerValidationComparison(
        raw_report               = raw_report,
        effective_report         = eff_report,
        resolved_findings        = tuple(sorted(raw_keys - eff_keys)),
        remaining_findings       = tuple(sorted(raw_keys & eff_keys)),
        newly_introduced_findings= tuple(sorted(eff_keys - raw_keys)),
    )
