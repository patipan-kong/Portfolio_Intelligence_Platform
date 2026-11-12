"""Observed liquidity evidence — SHADOW MODE ONLY (MUJI V2 Phase 4 Slice 4.5A).

Why this exists
---------------
``execution_penalty.classify_execution`` estimates average daily traded value
as ``avg_volume * current_price`` and compares it with THB thresholds, but no
production caller has ever supplied volume (Slice 4.5 investigation). Every
instrument therefore receives its asset-type baseline. This module builds the
missing input correctly and computes the classification it *would* produce,
without letting that hypothetical reach any decision.

Isolation contract
------------------
* Pure: no database, network, clock or environment access. The caller supplies
  the listing histories, prices, Registry facts and the ``as_of`` instant.
* Read-only with respect to its inputs: ``scores_map``, Registry facts and the
  active execution context are never mutated.
* Nothing in the optimizer pipeline imports this module. Its output never
  determines position caps, slippage, eligibility, candidates, allocations,
  scheduling, policy violations or any Strategist / Challenger / Auditor /
  Committee prompt. The active execution context stays the only authority.
* Threshold constants live in ``execution_penalty`` and are reused, never
  copied: the hypothetical profile is ``classify_execution`` itself, fed only
  ``avg_volume`` (never the single-day ``volume`` fallback, which reads a
  possibly partial session).

Listing identity
----------------
Evidence comes only from the history of the exact tradable listing symbol the
optimizer quotes (``NVDA01.BK`` for NVDA01.BK). The DR-to-underlying mapping in
``symbol_resolver`` is never consulted: underlying-share volume is a different
instrument, venue and unit and must never substitute for DR volume.

Evidence rules (a single failed rule makes the evidence UNOBSERVED)
--------------------------------------------------------------------
1. The listing is not quarantined by the market-data conversion guard.
2. Units: listing currency THB (Registry facts, else the logged SET symbol
   convention), because the classifier thresholds are THB.
3. A complete session is a bar whose exchange-local date is strictly before
   the exchange-local date of the observation instant ``min(fetched_at,
   as_of)``. A bar from the observation day is never trusted, so a partial
   current session can never enter the average.
4. At least ``LIQUIDITY_WINDOW_SESSIONS`` complete sessions.
5. Fresh: the last complete session is at most ``MAX_SESSION_GAP_DAYS``
   calendar days before the as-of exchange-local date. Cache expiry alone is
   informational, because short-history rows expire after 15 minutes while
   their completed sessions stay correct.
6. Every Volume in the window is present, finite and positive. Zero is
   unusable: the provider emits 0 for both no-trade days and missing data.
7. The listing price is present, finite, positive and within
   ``PRICE_CLOSE_TOLERANCE`` of the last complete close (a unit-mismatch
   guard, e.g. an underlying price supplied for a DR).

UNOBSERVED never means "low liquidity": it produces no hypothetical profile,
and the active baseline is left as it is.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Mapping, Optional, Sequence
from zoneinfo import ZoneInfo

from services.execution_instrument_facts import (
    ExecutionInstrumentFacts,
    ExecutionResolutionOutcome,
)
from services.optimizer.execution_penalty import classify_execution
from services.symbol_market_convention import infer_market_exchange

__all__ = [
    "SHADOW_SCHEMA_VERSION",
    "LIQUIDITY_WINDOW_SESSIONS",
    "MAX_SESSION_GAP_DAYS",
    "PRICE_CLOSE_TOLERANCE",
    "SUPPORTED_LISTING_CURRENCY",
    "EvidenceStatus",
    "UnobservedReason",
    "DailyBar",
    "ListingHistory",
    "LiquidityEvidence",
    "build_liquidity_evidence",
    "evaluate_listing_liquidity",
    "hypothetical_execution_profile",
    "build_liquidity_shadow",
]

SHADOW_SCHEMA_VERSION = "liquidity_shadow.v1"
LIQUIDITY_WINDOW_SESSIONS = 20
MAX_SESSION_GAP_DAYS = 7
PRICE_CLOSE_TOLERANCE = 2.0          # price / last close must lie in [1/2, 2]
SUPPORTED_LISTING_CURRENCY = "THB"   # unit of the classifier's traded-value thresholds
_SET_EXCHANGE = "SET"
_SET_TIMEZONE = ZoneInfo("Asia/Bangkok")

CURRENCY_SOURCE_REGISTRY = "REGISTRY_EXECUTION_INSTRUMENT_FACTS"
CURRENCY_SOURCE_CONVENTION = "SYMBOL_MARKET_CONVENTION_SET_THB"

_FACT_OUTCOMES_WITH_IDENTITY = (
    ExecutionResolutionOutcome.RESOLVED,
    ExecutionResolutionOutcome.NOT_TRADABLE,
)


class EvidenceStatus(str, Enum):
    OBSERVED = "OBSERVED"
    UNOBSERVED = "UNOBSERVED"


class UnobservedReason(str, Enum):
    LISTING_QUARANTINED = "LISTING_QUARANTINED"
    NO_LISTING_HISTORY = "NO_LISTING_HISTORY"
    HISTORY_SYMBOL_MISMATCH = "HISTORY_SYMBOL_MISMATCH"
    CURRENCY_UNKNOWN = "CURRENCY_UNKNOWN"
    UNSUPPORTED_CURRENCY = "UNSUPPORTED_CURRENCY"
    INSUFFICIENT_SESSIONS = "INSUFFICIENT_SESSIONS"
    STALE_HISTORY = "STALE_HISTORY"
    VOLUME_MISSING = "VOLUME_MISSING"
    VOLUME_INVALID = "VOLUME_INVALID"
    VOLUME_ZERO = "VOLUME_ZERO"
    PRICE_MISSING = "PRICE_MISSING"
    PRICE_INVALID = "PRICE_INVALID"
    PRICE_LISTING_MISMATCH = "PRICE_LISTING_MISMATCH"


# Reasons describing the history row itself; a row failing one of these can
# never be preferred over a row that does not (see _select_history).
_ROW_REASON_RANK = {
    None: 0,
    UnobservedReason.VOLUME_ZERO: 1,
    UnobservedReason.VOLUME_INVALID: 1,
    UnobservedReason.VOLUME_MISSING: 1,
    UnobservedReason.INSUFFICIENT_SESSIONS: 2,
    UnobservedReason.STALE_HISTORY: 3,
    UnobservedReason.HISTORY_SYMBOL_MISMATCH: 4,
    UnobservedReason.NO_LISTING_HISTORY: 5,
}


@dataclass(frozen=True)
class DailyBar:
    """One provider daily bar: UTC bar timestamp, close, volume (listing units)."""

    timestamp: datetime
    close: Optional[float]
    volume: Optional[float]


@dataclass(frozen=True)
class ListingHistory:
    """One cached daily history of one listing symbol, with its provenance."""

    listing_symbol: str
    bars: tuple[DailyBar, ...]
    source: str                          # e.g. "market_data_cache:history:1mo:1d"
    fetched_at: Optional[datetime]       # when the provider data was captured (UTC)
    cache_expired: Optional[bool] = None # informational only (rule 5)


@dataclass(frozen=True)
class LiquidityEvidence:
    listing_symbol: str
    status: EvidenceStatus
    reason: Optional[UnobservedReason]
    detail: Optional[str]
    avg_volume: Optional[float]                  # mean Volume, last 20 complete sessions
    window_sessions: int
    complete_sessions: int                       # complete sessions available in the source
    first_window_session: Optional[date]
    last_complete_session: Optional[date]
    excluded_incomplete_session: Optional[date]  # observation-day bar that was dropped
    zero_volume_sessions: int
    listing_currency: Optional[str]
    currency_source: Optional[str]
    listing_price: Optional[float]
    last_complete_close: Optional[float]
    est_avg_daily_traded_value: Optional[float]  # avg_volume * listing_price (THB)
    history_source: Optional[str]
    history_fetched_at: Optional[datetime]
    cache_expired: Optional[bool]
    as_of: datetime
    quarantine_reason: Optional[str] = None
    candidates_considered: int = 0

    @property
    def observed(self) -> bool:
        return self.status is EvidenceStatus.OBSERVED

    def to_dict(self) -> dict[str, Any]:
        def iso(value):
            return None if value is None else value.isoformat()

        return {
            "listing_symbol": self.listing_symbol,
            "status": self.status.value,
            "reason": None if self.reason is None else self.reason.value,
            "detail": self.detail,
            "avg_volume": None if self.avg_volume is None else round(self.avg_volume, 2),
            "window_sessions": self.window_sessions,
            "complete_sessions": self.complete_sessions,
            "first_window_session": iso(self.first_window_session),
            "last_complete_session": iso(self.last_complete_session),
            "excluded_incomplete_session": iso(self.excluded_incomplete_session),
            "zero_volume_sessions": self.zero_volume_sessions,
            "listing_currency": self.listing_currency,
            "currency_source": self.currency_source,
            "listing_price": self.listing_price,
            "last_complete_close": self.last_complete_close,
            "est_avg_daily_traded_value": (
                None if self.est_avg_daily_traded_value is None
                else round(self.est_avg_daily_traded_value, 2)
            ),
            "history_source": self.history_source,
            "history_fetched_at": iso(self.history_fetched_at),
            "cache_expired": self.cache_expired,
            "as_of": iso(self.as_of),
            "quarantine_reason": self.quarantine_reason,
            "candidates_considered": self.candidates_considered,
        }


# ── Small pure helpers ─────────────────────────────────────────────────────────

def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _local_date(value: datetime) -> date:
    return _utc(value).astimezone(_SET_TIMEZONE).date()


def _finite(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _listing_currency(
    listing_symbol: str,
    facts: Optional[ExecutionInstrumentFacts],
) -> tuple[Optional[str], Optional[str], Optional[UnobservedReason], Optional[str]]:
    """(currency, source, reason, detail). Registry currency wins; the logged SET
    symbol convention is used only when the Registry has no listing identity."""
    if facts is not None and facts.resolution_status in _FACT_OUTCOMES_WITH_IDENTITY:
        currency = (facts.currency or "").strip().upper() or None
        if currency is None:
            return None, None, UnobservedReason.CURRENCY_UNKNOWN, "Registry facts carry no currency"
        if currency != SUPPORTED_LISTING_CURRENCY:
            return (currency, CURRENCY_SOURCE_REGISTRY, UnobservedReason.UNSUPPORTED_CURRENCY,
                    f"listing currency {currency}; thresholds are {SUPPORTED_LISTING_CURRENCY}")
        exchange = (facts.exchange or "").strip().upper()
        if exchange and exchange != _SET_EXCHANGE:
            return (currency, CURRENCY_SOURCE_REGISTRY, UnobservedReason.UNSUPPORTED_CURRENCY,
                    f"listing exchange {exchange}; sessions are evaluated on the SET calendar")
        return currency, CURRENCY_SOURCE_REGISTRY, None, None
    hint = infer_market_exchange(listing_symbol)
    if hint is None or hint.exchange != _SET_EXCHANGE:
        return None, None, UnobservedReason.CURRENCY_UNKNOWN, "no Registry currency and no SET listing convention"
    return SUPPORTED_LISTING_CURRENCY, CURRENCY_SOURCE_CONVENTION, None, None


@dataclass(frozen=True)
class _RowAssessment:
    history: ListingHistory
    reason: Optional[UnobservedReason]
    detail: Optional[str]
    complete: tuple[DailyBar, ...]
    window: tuple[DailyBar, ...]
    excluded_incomplete: Optional[date]
    zero_volume_sessions: int
    avg_volume: Optional[float]


def _assess_row(listing_symbol: str, history: ListingHistory, as_of: datetime) -> _RowAssessment:
    if history.listing_symbol != listing_symbol:
        return _RowAssessment(history, UnobservedReason.HISTORY_SYMBOL_MISMATCH,
                              f"history belongs to {history.listing_symbol}", (), (), None, 0, None)
    observed_at = _utc(as_of) if history.fetched_at is None else min(_utc(history.fetched_at), _utc(as_of))
    observation_day = _local_date(observed_at)
    by_day: dict[date, DailyBar] = {}
    for bar in sorted(history.bars, key=lambda b: _utc(b.timestamp)):
        by_day[_local_date(bar.timestamp)] = bar          # last bar per exchange day wins
    excluded = max((d for d in by_day if d >= observation_day), default=None)
    complete = tuple(bar for day, bar in sorted(by_day.items()) if day < observation_day)
    if not complete:
        return _RowAssessment(history, UnobservedReason.NO_LISTING_HISTORY,
                              "no complete sessions", (), (), excluded, 0, None)
    window = complete[-LIQUIDITY_WINDOW_SESSIONS:]
    last_day = _local_date(complete[-1].timestamp)
    gap = (_local_date(as_of) - last_day).days
    zero = 0
    reason: Optional[UnobservedReason] = None
    detail: Optional[str] = None
    if gap > MAX_SESSION_GAP_DAYS:
        reason, detail = UnobservedReason.STALE_HISTORY, (
            f"last complete session {last_day.isoformat()} is {gap} days before as-of")
    elif len(complete) < LIQUIDITY_WINDOW_SESSIONS:
        reason, detail = UnobservedReason.INSUFFICIENT_SESSIONS, (
            f"{len(complete)} complete sessions < {LIQUIDITY_WINDOW_SESSIONS}")
    else:
        volumes = [_finite(bar.volume) for bar in window]
        zero = sum(1 for v in volumes if v == 0)
        if any(v is None for v in volumes):
            reason, detail = UnobservedReason.VOLUME_MISSING, "missing or non-finite Volume in window"
        elif any(v < 0 for v in volumes):
            reason, detail = UnobservedReason.VOLUME_INVALID, "negative Volume in window"
        elif zero:
            reason, detail = UnobservedReason.VOLUME_ZERO, f"{zero} zero-Volume session(s) in window"
    avg = None
    if reason is None:
        avg = sum(float(bar.volume) for bar in window) / len(window)
    return _RowAssessment(history, reason, detail, complete, window, excluded, zero, avg)


def _select_history(
    listing_symbol: str,
    histories: Sequence[ListingHistory],
    as_of: datetime,
) -> Optional[_RowAssessment]:
    """Deterministic choice among cached rows: a usable row beats an unusable
    one; then the latest complete session, then more sessions, then the most
    recent capture, then the source name. Never dict or query order."""
    assessed = [_assess_row(listing_symbol, h, as_of) for h in histories]
    if not assessed:
        return None

    def key(a: _RowAssessment):
        last = _local_date(a.complete[-1].timestamp) if a.complete else date.min
        fetched = _utc(a.history.fetched_at) if a.history.fetched_at else datetime.min.replace(tzinfo=timezone.utc)
        return (-_ROW_REASON_RANK[a.reason], last, len(a.complete), fetched, a.history.source)

    return max(assessed, key=key)


# ── Public API ────────────────────────────────────────────────────────────────

def build_liquidity_evidence(
    listing_symbol: str,
    histories: Sequence[ListingHistory],
    *,
    listing_price: Any,
    facts: Optional[ExecutionInstrumentFacts],
    as_of: datetime,
    quarantine_reason: Optional[str] = None,
) -> LiquidityEvidence:
    """Observed-liquidity evidence for one tradable listing; never raises on bad data."""
    as_of = _utc(as_of)
    base = dict(listing_symbol=listing_symbol, window_sessions=LIQUIDITY_WINDOW_SESSIONS,
                as_of=as_of, quarantine_reason=quarantine_reason,
                candidates_considered=len(histories))

    def unobserved(reason, detail, *, row: Optional[_RowAssessment] = None,
                   currency=None, currency_source=None, price=None):
        return LiquidityEvidence(
            status=EvidenceStatus.UNOBSERVED, reason=reason, detail=detail, avg_volume=None,
            complete_sessions=len(row.complete) if row else 0,
            first_window_session=_local_date(row.window[0].timestamp) if row and row.window else None,
            last_complete_session=_local_date(row.complete[-1].timestamp) if row and row.complete else None,
            excluded_incomplete_session=row.excluded_incomplete if row else None,
            zero_volume_sessions=row.zero_volume_sessions if row else 0,
            listing_currency=currency, currency_source=currency_source, listing_price=price,
            last_complete_close=_finite(row.complete[-1].close) if row and row.complete else None,
            est_avg_daily_traded_value=None,
            history_source=row.history.source if row else None,
            history_fetched_at=row.history.fetched_at if row else None,
            cache_expired=row.history.cache_expired if row else None,
            **base,
        )

    if quarantine_reason:
        return unobserved(UnobservedReason.LISTING_QUARANTINED,
                          f"market-data guard refuses unbound history: {quarantine_reason}")
    currency, currency_source, currency_reason, currency_detail = _listing_currency(listing_symbol, facts)
    row = _select_history(listing_symbol, histories, as_of)
    if currency_reason is not None:
        return unobserved(currency_reason, currency_detail, row=row,
                          currency=currency, currency_source=currency_source)
    if row is None:
        return unobserved(UnobservedReason.NO_LISTING_HISTORY, "no cached daily history for the listing symbol",
                          currency=currency, currency_source=currency_source)
    if row.reason is not None:
        return unobserved(row.reason, row.detail, row=row, currency=currency, currency_source=currency_source)

    raw_price = listing_price
    price = _finite(raw_price)
    last_close = _finite(row.complete[-1].close)
    if raw_price is None:
        return unobserved(UnobservedReason.PRICE_MISSING, "no listing price", row=row,
                          currency=currency, currency_source=currency_source)
    if price is None or price <= 0:
        return unobserved(UnobservedReason.PRICE_INVALID, f"listing price {raw_price!r}", row=row,
                          currency=currency, currency_source=currency_source)
    if last_close is None or last_close <= 0:
        return unobserved(UnobservedReason.PRICE_LISTING_MISMATCH, "last complete session has no valid close",
                          row=row, currency=currency, currency_source=currency_source, price=price)
    ratio = price / last_close
    if not (1.0 / PRICE_CLOSE_TOLERANCE <= ratio <= PRICE_CLOSE_TOLERANCE):
        return unobserved(UnobservedReason.PRICE_LISTING_MISMATCH,
                          f"price {price} vs last complete close {last_close} (ratio {ratio:.2f})",
                          row=row, currency=currency, currency_source=currency_source, price=price)

    return LiquidityEvidence(
        status=EvidenceStatus.OBSERVED, reason=None, detail=None, avg_volume=row.avg_volume,
        complete_sessions=len(row.complete),
        first_window_session=_local_date(row.window[0].timestamp),
        last_complete_session=_local_date(row.complete[-1].timestamp),
        excluded_incomplete_session=row.excluded_incomplete,
        zero_volume_sessions=0,
        listing_currency=currency, currency_source=currency_source,
        listing_price=price, last_complete_close=last_close,
        est_avg_daily_traded_value=row.avg_volume * price,
        history_source=row.history.source, history_fetched_at=row.history.fetched_at,
        cache_expired=row.history.cache_expired,
        **base,
    )


def hypothetical_execution_profile(
    symbol: str,
    is_dr: bool,
    evidence: LiquidityEvidence,
    *,
    facts: Optional[ExecutionInstrumentFacts],
) -> Optional[dict[str, Any]]:
    """The existing classifier fed observed ``avg_volume``; None when UNOBSERVED."""
    if not evidence.observed:
        return None
    meta = classify_execution(
        symbol=symbol,
        is_dr=is_dr,
        volume=None,                       # never the single-day (possibly partial) fallback
        avg_volume=evidence.avg_volume,
        current_price=evidence.listing_price,
        facts=facts,
    )
    return {
        "asset_type": meta.asset_type,
        "liquidity_score": meta.liquidity_score,
        "spread_score": meta.spread_score,
        "execution_quality_score": meta.execution_quality_score,
        "execution_risk": meta.execution_risk,
        "execution_warnings": list(meta.execution_warnings),
        "position_cap_pct": meta.position_cap_pct,
        "slippage_cost_est_pct": meta.slippage_cost_est_pct,
        "classification_source": meta.classification_source,
    }


def evaluate_listing_liquidity(
    symbol: str,
    is_dr: bool,
    histories: Sequence[ListingHistory],
    *,
    listing_price: Any,
    facts: Optional[ExecutionInstrumentFacts],
    as_of: datetime,
    quarantine_reason: Optional[str] = None,
) -> tuple[LiquidityEvidence, Optional[dict[str, Any]]]:
    evidence = build_liquidity_evidence(symbol, histories, listing_price=listing_price, facts=facts,
                                        as_of=as_of, quarantine_reason=quarantine_reason)
    return evidence, hypothetical_execution_profile(symbol, is_dr, evidence, facts=facts)


def _cap_value(cap: Optional[float]) -> float:
    return math.inf if cap is None else float(cap)


_ACTIVE_FIELDS = ("asset_type", "execution_quality_score", "execution_risk",
                  "position_cap_pct", "slippage_cost_est_pct")


def build_liquidity_shadow(
    scores_map: Mapping[str, Mapping[str, Any]],
    active_context: Mapping[str, Any],
    *,
    histories_by_symbol: Mapping[str, Sequence[ListingHistory]],
    facts_by_symbol: Mapping[str, ExecutionInstrumentFacts],
    as_of: datetime,
    quarantine_reasons: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Shadow report for one universe. Reads ``current_price`` / ``is_dr`` from
    ``scores_map`` and the active per-symbol profile for comparison only.

    ``histories_by_symbol`` is keyed by the exact listing symbol; only that key
    is read for each instrument, so another symbol's history (an underlying)
    can never be used even if present.
    """
    quarantine_reasons = quarantine_reasons or {}
    active_per_symbol = active_context.get("per_symbol") or {}
    per_symbol: dict[str, Any] = {}
    for symbol in sorted(scores_map):
        row = scores_map[symbol]
        facts = facts_by_symbol.get(symbol)
        evidence, hypothetical = evaluate_listing_liquidity(
            symbol, bool(row.get("is_dr", False)), tuple(histories_by_symbol.get(symbol, ())),
            listing_price=row.get("current_price"), facts=facts, as_of=as_of,
            quarantine_reason=quarantine_reasons.get(symbol),
        )
        active_meta = active_per_symbol.get(symbol) or {}
        active = {k: active_meta.get(k) for k in _ACTIVE_FIELDS}
        stricter_cap = bool(
            hypothetical is not None
            and _cap_value(hypothetical["position_cap_pct"]) < _cap_value(active["position_cap_pct"])
        )
        per_symbol[symbol] = {
            "evidence": evidence.to_dict(),
            "active": active,
            "hypothetical": hypothetical,
            "risk_changed": bool(hypothetical and hypothetical["execution_risk"] != active["execution_risk"]),
            "stricter_position_cap": stricter_cap,
        }
    return {
        "schema_version": SHADOW_SCHEMA_VERSION,
        "mode": "SHADOW",
        "authoritative": False,
        "as_of": _utc(as_of).isoformat(),
        "rules": {
            "window_sessions": LIQUIDITY_WINDOW_SESSIONS,
            "max_session_gap_days": MAX_SESSION_GAP_DAYS,
            "price_close_tolerance": PRICE_CLOSE_TOLERANCE,
            "listing_currency": SUPPORTED_LISTING_CURRENCY,
            "exchange_timezone": str(_SET_TIMEZONE),
            "classifier": "services.optimizer.execution_penalty.classify_execution (unchanged thresholds)",
        },
        "per_symbol": per_symbol,
        "summary": summarize_liquidity_shadow(per_symbol),
    }


def summarize_liquidity_shadow(per_symbol: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    status = Counter()
    reasons = Counter()
    hypothetical = Counter()
    by_type: dict[str, Counter] = {}
    stricter: list[dict[str, Any]] = []
    unobserved: dict[str, list[str]] = {}
    for symbol, item in per_symbol.items():
        ev = item["evidence"]
        asset_type = item["active"].get("asset_type") or "UNKNOWN"
        status[ev["status"]] += 1
        if ev["status"] == EvidenceStatus.OBSERVED.value:
            risk = item["hypothetical"]["execution_risk"]
            hypothetical[risk] += 1
            by_type.setdefault(asset_type, Counter())[risk] += 1
        else:
            reasons[ev["reason"]] += 1
            unobserved.setdefault(ev["reason"], []).append(symbol)
            by_type.setdefault(asset_type, Counter())["UNOBSERVED"] += 1
        if item["stricter_position_cap"]:
            stricter.append({
                "symbol": symbol,
                "active_cap_pct": item["active"]["position_cap_pct"],
                "hypothetical_cap_pct": item["hypothetical"]["position_cap_pct"],
                "active_risk": item["active"]["execution_risk"],
                "hypothetical_risk": item["hypothetical"]["execution_risk"],
                "est_avg_daily_traded_value": ev["est_avg_daily_traded_value"],
            })
    return {
        "instruments": len(per_symbol),
        "evidence_status": dict(sorted(status.items())),
        "unobserved_reasons": dict(sorted(reasons.items())),
        "unobserved_symbols": {k: sorted(v) for k, v in sorted(unobserved.items())},
        "hypothetical_risk": dict(sorted(hypothetical.items())),
        "by_active_asset_type": {k: dict(sorted(v.items())) for k, v in sorted(by_type.items())},
        "stricter_position_cap": sorted(stricter, key=lambda x: x["symbol"]),
    }
