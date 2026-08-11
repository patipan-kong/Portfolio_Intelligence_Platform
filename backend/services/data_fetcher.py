"""Cache-aware market data facade.

Call hierarchy:
  agents / main.py
      ↓  fetch_history / fetch_info / fetch_price_info / fetch_news
  data_fetcher  ← this module (cache layer)
      ↓  on cache-miss or cache-expired
  services.market_data.YahooProvider (network I/O)
      ↓  on failure
  stale cache (served with _stale_data metadata attached)

TTL policy:
  quote             → 5 min
  history intraday  → 5 min
  history short     → 15 min (1mo / 3mo)
  history long      → 24 h  (6mo+ / weekly)
  fundamental/info  → 24 h
  benchmark         → 15 min
"""
from __future__ import annotations

import io
import json as _json
import logging
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Mapping, Optional

import pandas as pd

from models.database import MarketDataCache, SessionLocal, Transaction
from services.core.runtime_env import allow_market_fetching
from services.market_data.base import MarketDataProvider
from services.market_data.position_conversion_quote_contract import (
    QuarantineReason,
    QuarantineResult,
    SuccessorQuoteBinding,
    build_successor_quote_binding,
    evaluate_candidate_quarantine,
    evaluate_request_identity,
    history_cache_type,
    quote_cache_type,
)
from services.market_data.provider import get_provider
from services.market_data.yahoo import _is_rate_limit
from services.symbol_resolver import resolve_yfinance_symbol as _resolve_yf, is_dr as _is_dr
from services.transaction_canonicalizer import canonicalize_transactions

_log = logging.getLogger(__name__)

# DR symbol resolution is centralised in services.symbol_resolver.
# These thin wrappers exist for backward compatibility with existing callers.

# ── Provider singleton ─────────────────────────────────────────────────────────
# Selection: PRICE_PROVIDER env var — "yahoo" (default, crash-safe) or "yfinance"
# (legacy rollback). See services/market_data/provider.py.
_provider: MarketDataProvider = get_provider()

# ── TTL table (seconds) ────────────────────────────────────────────────────────
_TTL_QUOTE       = 5  * 60        # 5 min  – live prices
_TTL_FUND        = 24 * 3600      # 24 h   – P/E, ROE, sector, …
_TTL_BENCHMARK   = 15 * 60        # 15 min – index / ETF prices
_TTL_HIST_INTRA  = 5  * 60        # 5 min  – intraday bars
_TTL_HIST_SHORT  = 15 * 60        # 15 min – 1mo / 3mo daily
_TTL_HIST_LONG   = 24 * 3600      # 24 h   – 6mo+ / weekly


# WP3.3 cache payloads carry provider identity as private provenance.  The
# accepted cache namespace remains the existing (symbol, cache_type) pair;
# this marker prevents a namespaced row written by one provider from being
# consumed after provider selection changes, without adding a schema or
# changing public quote/history payloads.
_BOUND_PROVIDER_KEY = "_wp3_provider"


@dataclass(frozen=True)
class _ConversionGuardProjection:
    """One read-only projection of canonical POSITION_CONVERSION evidence.

    The projection is deliberately ephemeral.  It is rebuilt for every
    unbound request, giving it a zero staleness bound and making the G4
    empty-to-converted transition safe in the same process.  The database
    rows, canonicalized by the frozen WP1 contract, remain the only authority.
    """

    available: bool
    bindings_by_symbol: tuple[tuple[str, SuccessorQuoteBinding], ...]
    ambiguous_symbols: frozenset[str]
    boundary_evidence_by_symbol: tuple[tuple[str, object], ...] = ()

    def binding_for(self, symbol: str) -> SuccessorQuoteBinding | None:
        for candidate_symbol, binding in self.bindings_by_symbol:
            if candidate_symbol == symbol:
                return binding
        return None

    def boundary_evidence_for(
        self,
        binding: SuccessorQuoteBinding,
    ) -> object | None:
        """Return source-owned boundary evidence for an exact binding."""
        for symbol, candidate_binding in self.bindings_by_symbol:
            if candidate_binding != binding:
                continue
            for evidence_symbol, evidence in self.boundary_evidence_by_symbol:
                if evidence_symbol == symbol:
                    return evidence
            return None
        return None


def _unavailable_conversion_guard_projection() -> _ConversionGuardProjection:
    return _ConversionGuardProjection(
        available=False,
        bindings_by_symbol=(),
        ambiguous_symbols=frozenset(),
    )


def _read_conversion_guard_projection() -> _ConversionGuardProjection:
    """Read and canonicalize the authoritative conversion guard source.

    The only membership source is canonical POSITION_CONVERSION ledger
    evidence.  A database or parse error is represented as unavailable rather
    than as an empty set, because G3 requires refusal when membership is
    undetermined.  No registry lookup, configuration value, or environment
    setting participates in membership.
    """
    db = None
    projection = _unavailable_conversion_guard_projection()
    try:
        # Session construction is part of the guarded source read.  G3 treats
        # an open failure exactly like a query, canonicalization, or parse
        # failure: membership is unavailable and must not become an empty
        # permissive projection.
        db = SessionLocal()
        rows = (
            db.query(Transaction)
            .filter_by(transaction_type="POSITION_CONVERSION")
            .all()
        )
        canonical = canonicalize_transactions(list(rows))
        by_symbol: dict[str, SuccessorQuoteBinding] = {}
        boundary_by_symbol: dict[str, object] = {}
        ambiguous: set[str] = set()
        source_invalid = False

        for transaction in canonical:
            parsed = transaction.position_conversion
            if parsed is None or not parsed.is_valid or parsed.value is None:
                _log.warning(
                    "conversion_guard_unavailable reason=invalid_position_conversion"
                )
                source_invalid = True
                break

            binding = build_successor_quote_binding(
                parsed.value.successor,
                parsed.value.quote_binding,
                parsed.value.dates,
            )
            boundary_evidence = parsed.value.boundary_evidence
            identifier_result = evaluate_request_identity(
                binding,
                requested_symbol=binding.provider_symbol,
            )
            if identifier_result is not None:
                _log.warning(
                    "conversion_guard_unavailable reason=%s affected_asset_id=%s",
                    identifier_result.reason.value,
                    identifier_result.affected_asset_id,
                )
                source_invalid = True
                break

            symbol = binding.provider_symbol
            previous = by_symbol.get(symbol)
            previous_boundary = boundary_by_symbol.get(symbol)
            if previous is not None and (
                previous != binding or previous_boundary != boundary_evidence
            ):
                ambiguous.add(symbol)
                by_symbol.pop(symbol, None)
                boundary_by_symbol.pop(symbol, None)
            elif symbol not in ambiguous:
                by_symbol[symbol] = binding
                boundary_by_symbol[symbol] = boundary_evidence

        if not source_invalid:
            projection = _ConversionGuardProjection(
                available=True,
                bindings_by_symbol=tuple(sorted(by_symbol.items())),
                ambiguous_symbols=frozenset(ambiguous),
                boundary_evidence_by_symbol=tuple(sorted(boundary_by_symbol.items())),
            )
    except Exception as exc:
        _log.warning(
            "conversion_guard_unavailable error_type=%s",
            type(exc).__name__,
        )
        projection = _unavailable_conversion_guard_projection()
    finally:
        if db is not None:
            try:
                db.close()
            except Exception as exc:
                _log.warning(
                    "conversion_guard_unavailable error_type=%s",
                    type(exc).__name__,
                )
                projection = _unavailable_conversion_guard_projection()
    return projection


def _guard_result_from_projection(
    symbol: str,
    projection: _ConversionGuardProjection,
) -> QuarantineResult | None:
    """Apply one already-read projection to one unbound symbol."""
    if not projection.available:
        return QuarantineResult(
            QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
            0,
        )
    if symbol in projection.ambiguous_symbols:
        return QuarantineResult(
            QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
            0,
        )
    binding = projection.binding_for(symbol)
    if binding is None:
        return None
    return QuarantineResult(
        QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
        binding.asset_id,
    )


def _unbound_guard_result(symbol: str) -> QuarantineResult | None:
    """Read the guard source once and refuse when membership is known/unknown.

    A successful empty projection is the legacy/unconverted case.  Every
    other state is fail-closed: a converted symbol lacks its explicit binding,
    an ambiguous symbol has no uniquely affected identity, and an unavailable
    source cannot be treated as "not converted".  The caller of a batch path
    should reuse the returned projection for all symbols in that batch.
    """
    return _guard_result_from_projection(
        symbol,
        _read_conversion_guard_projection(),
    )


def resolve_successor_bindings(
    symbols: list[str],
) -> dict[str, SuccessorQuoteBinding]:
    """Return the canonical successor binding for each of *symbols* that has one.

    Reads the exact same WP3.3 guard projection consulted to refuse an
    unbound request for a converted identity (``_unbound_guard_result``).
    This is a read-only projection over already-canonicalized WP1 evidence —
    it performs no binding construction, no comparison, and no quarantine
    decision of its own. It exists so the one call site that owns portfolio
    identity can supply the binding WP3.3 requires, instead of receiving the
    unbound refusal. A symbol absent from the result is either unconverted,
    ambiguous, or the guard source is unavailable; the caller's existing
    unbound path (which already fails closed for the latter two cases)
    remains the correct fallback and must not be duplicated here.
    """
    projection = _read_conversion_guard_projection()
    if not projection.available:
        return {}
    wanted = set(symbols)
    return {
        symbol: binding
        for symbol, binding in projection.bindings_by_symbol
        if symbol in wanted and symbol not in projection.ambiguous_symbols
    }


def _history_ttl(period: str, interval: str) -> int:
    if interval in ("1m", "2m", "5m", "15m", "30m", "60m", "1h"):
        return _TTL_HIST_INTRA
    if period in ("1d", "5d"):
        return _TTL_HIST_INTRA
    if period in ("1mo", "3mo"):
        return _TTL_HIST_SHORT
    return _TTL_HIST_LONG


# ── In-process stats counters (reset on server restart) ───────────────────────
_stats_lock = threading.Lock()
_stats: dict = {
    "cache_hits":              0,
    "cache_misses":            0,
    "stale_served":            0,
    "yahoo_requests":          0,
    "yahoo_errors":            0,
    "timeouts":                0,
    "rate_limits":             0,
    "yahoo_total_latency_ms":  0.0,
    "yahoo_latency_samples":   0,
    "started_at":              datetime.utcnow().isoformat() + "Z",
}


def _inc(key: str, amount: float = 1.0) -> None:
    with _stats_lock:
        _stats[key] = _stats.get(key, 0) + amount


def get_cache_stats() -> dict:
    """Return a copy of current in-process counters (used by /admin/cache-stats)."""
    with _stats_lock:
        s = dict(_stats)
    total = s["cache_hits"] + s["cache_misses"]
    hit_rate  = round(s["cache_hits"]  / total * 100, 1) if total else 0.0
    miss_rate = round(100 - hit_rate, 1) if total else 0.0
    avg_lat   = (
        round(s["yahoo_total_latency_ms"] / s["yahoo_latency_samples"], 1)
        if s["yahoo_latency_samples"] else 0.0
    )
    # Extrapolate to a per-day request rate
    started = datetime.fromisoformat(s["started_at"].rstrip("Z"))
    uptime_h = (datetime.utcnow() - started).total_seconds() / 3600
    req_per_day = round(s["yahoo_requests"] / uptime_h * 24, 0) if uptime_h > 0 else 0

    return {
        **s,
        "hit_rate_pct":              hit_rate,
        "miss_rate_pct":             miss_rate,
        "avg_yahoo_latency_ms":      avg_lat,
        "yahoo_requests_per_day_est": req_per_day,
        "uptime_hours":              round(uptime_h, 2),
    }


# ── Cache I/O helpers ──────────────────────────────────────────────────────────

def _get_cached(symbol: str, cache_type: str) -> Optional[dict]:
    """Return valid (non-expired) cached payload or None."""
    db = SessionLocal()
    try:
        entry: MarketDataCache | None = (
            db.query(MarketDataCache)
            .filter_by(symbol=symbol, cache_type=cache_type)
            .first()
        )
        if entry is None:
            _log.debug("cache_miss symbol=%s type=%s", symbol, cache_type)
            _inc("cache_misses")
            return None
        if entry.expires_at < datetime.utcnow():
            _log.debug("cache_expired symbol=%s type=%s", symbol, cache_type)
            _inc("cache_misses")
            return None
        entry.hit_count = (entry.hit_count or 0) + 1
        db.commit()
        _log.debug("cache_hit symbol=%s type=%s", symbol, cache_type)
        _inc("cache_hits")
        return _json.loads(entry.payload_json)
    except Exception as exc:
        _log.warning("cache_read_error symbol=%s type=%s: %s", symbol, cache_type, exc)
        return None
    finally:
        db.close()


def _set_cached(symbol: str, cache_type: str, payload: dict, ttl_secs: int) -> None:
    now     = datetime.utcnow()
    expires = now + timedelta(seconds=ttl_secs)
    payload_str = _json.dumps(payload, default=str)
    db = SessionLocal()
    try:
        entry = (
            db.query(MarketDataCache)
            .filter_by(symbol=symbol, cache_type=cache_type)
            .first()
        )
        if entry:
            entry.payload_json = payload_str
            entry.fetched_at   = now
            entry.expires_at   = expires
        else:
            db.add(MarketDataCache(
                symbol=symbol, cache_type=cache_type,
                payload_json=payload_str,
                fetched_at=now, expires_at=expires,
                hit_count=0,
            ))
        db.commit()
    except Exception as exc:
        _log.warning("cache_write_error symbol=%s type=%s: %s", symbol, cache_type, exc)
        db.rollback()
    finally:
        db.close()


def _get_stale(symbol: str, cache_type: str) -> Optional[dict]:
    """Return an expired cache entry as a stale fallback (includes _stale_data metadata)."""
    db = SessionLocal()
    try:
        entry = (
            db.query(MarketDataCache)
            .filter_by(symbol=symbol, cache_type=cache_type)
            .first()
        )
        if entry is None:
            return None
        payload = _json.loads(entry.payload_json)
        age_s   = (datetime.utcnow() - entry.fetched_at).total_seconds()
        payload["_stale_data"]         = True
        payload["_cache_age_minutes"]  = round(age_s / 60, 1)
        _inc("stale_served")
        _log.warning(
            "stale_cache_served symbol=%s type=%s age_min=%.1f",
            symbol, cache_type, age_s / 60,
        )
        return payload
    except Exception:
        return None
    finally:
        db.close()


# ── DataFrame serialisation ────────────────────────────────────────────────────

def _source_quote_payload(payload: dict) -> dict:
    """Return source quote fields only, dropping stale derived cache fields."""
    return {
        k: v
        for k, v in payload.items()
        if not k.startswith("_") and k != "change_percent"
    }


def _log_quarantine(
    result: QuarantineResult,
    *,
    symbol: str,
    kind: str,
) -> None:
    """Emit the deterministic, structured fetch-layer quarantine record."""
    _log.warning(
        "market_data_quarantine kind=%s symbol=%s reason=%s affected_asset_id=%s",
        kind,
        symbol,
        result.reason.value,
        result.affected_asset_id,
    )


def _quote_quarantine_response(
    result: QuarantineResult,
    *,
    symbol: str,
) -> dict:
    """Return a shape-compatible quote refusal with private diagnostics."""
    _log_quarantine(result, symbol=symbol, kind="quote")
    return {
        "current_price": None,
        "previous_close": None,
        "last_updated": None,
        "_quarantine_reason": result.reason.value,
        "_quarantine_asset_id": result.affected_asset_id,
    }


def _binding_request_identity_result(
    symbol: str,
    binding: SuccessorQuoteBinding,
) -> QuarantineResult | None:
    """Delegate all pre-fetch request identity policy to WP3.2."""
    return evaluate_request_identity(
        binding,
        requested_symbol=symbol,
    )


def _history_cache_type_for_binding(
    binding: SuccessorQuoteBinding,
    period: str,
    interval: str,
) -> str | None:
    """Return only the WP3.2-approved converted-history namespace.

    The WP3.2 contract defines one binding-aware history namespace.  Legacy
    period/interval combinations remain valid only on the unconverted path;
    they must never be projected into a second bound namespace here.
    """
    if period != "5y" or interval != "1d":
        return None
    return history_cache_type(binding)


def _boundary_evidence_for_binding(
    binding: SuccessorQuoteBinding,
) -> object | None:
    """Read boundary evidence only from the canonical conversion projection."""
    try:
        return _read_conversion_guard_projection().boundary_evidence_for(binding)
    except Exception as exc:
        # The guard projection already fails closed; this defensive envelope
        # keeps a malformed caller object from escaping into a fetch path.
        _log.warning(
            "conversion_guard_unavailable error_type=%s",
            type(exc).__name__,
        )
        return None


def _binding_evidence_result(
    evidence: object,
    *,
    symbol: str,
    binding: SuccessorQuoteBinding,
    cache_type: str,
    cache_kind: str,
) -> QuarantineResult | None:
    """Consume WP3.2's one authoritative quarantine composition path."""
    return evaluate_candidate_quarantine(
        binding=binding,
        evidence=evidence,
        boundary_evidence=_boundary_evidence_for_binding(binding),
        reference_price_field="successor_reference_price",
        candidate_cache_type=cache_type,
        cache_kind=cache_kind,
    )


def _fetch_binding_evidence(
    symbol: str,
    binding: SuccessorQuoteBinding,
    *,
    cache_type: str,
    cache_kind: str,
) -> tuple[object | None, QuarantineResult | None]:
    """Fetch WP3.1 evidence and apply the WP3.2 contract at this layer."""
    getter = getattr(_provider, "get_quote_evidence", None)
    if not callable(getter):
        return None, QuarantineResult(
            QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED,
            binding.asset_id,
        )

    try:
        evidence = getter(symbol)
    except Exception as exc:
        _log.warning(
            "provider_evidence_unavailable symbol=%s error_type=%s",
            symbol,
            type(exc).__name__,
        )
        return None, QuarantineResult(
            QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED,
            binding.asset_id,
        )

    result = _binding_evidence_result(
        evidence,
        symbol=symbol,
        binding=binding,
        cache_type=cache_type,
        cache_kind=cache_kind,
    )
    return evidence, result


def _evidence_to_quote_payload(evidence: object) -> dict:
    """Project accepted provider closes into the legacy quote response shape."""
    current_close = getattr(evidence, "current_close")
    previous_close = getattr(evidence, "previous_close")
    return {
        "current_price": round(current_close, 4),
        "previous_close": previous_close,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def _bound_cache_hit(cached: dict | None, binding: SuccessorQuoteBinding) -> bool:
    """Accept only a row written by the provider named by the binding."""
    return bool(cached) and cached.get(_BOUND_PROVIDER_KEY) == binding.provider


def _df_to_payload(df: pd.DataFrame) -> dict:
    try:
        return {"json_split": df.to_json(orient="split", date_format="iso", default_handler=str)}
    except Exception as exc:
        _log.error("df_serialize_error: %s", exc)
        return {}


def _payload_to_df(payload: dict) -> Optional[pd.DataFrame]:
    if not payload or "json_split" not in payload:
        return None
    try:
        df = pd.read_json(io.StringIO(payload["json_split"]), orient="split")
        df.index = pd.to_datetime(df.index, utc=True)
        return df
    except Exception as exc:
        _log.error("df_deserialize_error: %s", exc)
        return None


# ── DR / symbol helpers (public, consumed by agents and main.py) ───────────────

def normalize_dr_symbol(symbol: str) -> str:
    """Resolve a DR certificate to its yfinance ticker.

    Delegates to services.symbol_resolver.resolve_yfinance_symbol — kept here
    for backward compatibility with existing callers.

    AAPL01.BK   → 'AAPL'       (generic suffix stripping)
    CATL01.BK   → '300750.SZ'  (explicit map — Shenzhen)
    MICRON01.BK → 'MU'         (explicit map — company-name alias)
    PTT.BK      → 'PTT.BK'     (unchanged — regular Thai stock)
    AAPL        → 'AAPL'       (unchanged — US ticker)
    """
    return _resolve_yf(symbol)


def is_dr_symbol(symbol: str) -> bool:
    """Return True if *symbol* is a SET DR certificate (delegates to symbol_resolver)."""
    return _is_dr(symbol)


# ── Internal fetch helpers ─────────────────────────────────────────────────────

def _record_yf_call(t0: float) -> None:
    elapsed_ms = (time.monotonic() - t0) * 1000
    _inc("yahoo_total_latency_ms", elapsed_ms)
    _inc("yahoo_latency_samples")
    _log.info("yahoo_fetch_time latency_ms=%.0f", elapsed_ms)


def _record_yf_error(e: Exception) -> None:
    _inc("yahoo_errors")
    if _is_rate_limit(e):
        _inc("rate_limits")
        _log.warning("yahoo_rate_limit: %s", e)
    else:
        _log.error("yahoo_fetch_error: %s", e)


# ── Public API (same signatures as the original data_fetcher.py) ───────────────

def _fetch_history_bound(
    symbol: str,
    period: str,
    interval: str,
    binding: SuccessorQuoteBinding,
) -> Optional[pd.DataFrame]:
    request_result = _binding_request_identity_result(symbol, binding)
    if request_result is not None:
        _log_quarantine(request_result, symbol=symbol, kind="history")
        return None
    try:
        cache_type = _history_cache_type_for_binding(binding, period, interval)
    except (AttributeError, TypeError, ValueError, ArithmeticError):
        result = QuarantineResult(
            QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
            getattr(binding, "asset_id", 0)
            if isinstance(getattr(binding, "asset_id", 0), int)
            else 0,
        )
        _log_quarantine(result, symbol=symbol, kind="history")
        return None
    if cache_type is None:
        result = QuarantineResult(
            QuarantineReason.CACHE_NAMESPACE_MISMATCH,
            binding.asset_id,
        )
        _log_quarantine(result, symbol=symbol, kind="history")
        return None

    cached = _get_cached(symbol, cache_type)
    if cached:
        if _bound_cache_hit(cached, binding):
            df_cached = _payload_to_df(cached)
            if df_cached is not None and not df_cached.empty:
                return df_cached
        else:
            _log.warning(
                "bound_cache_rejected symbol=%s type=%s reason=provider_namespace_mismatch",
                symbol,
                cache_type,
            )

    # A converted/bound history request never serves an expired row.  It must
    # be revalidated from provider evidence or fail closed.
    if not allow_market_fetching():
        result = QuarantineResult(
            QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED,
            binding.asset_id,
        )
        _log_quarantine(result, symbol=symbol, kind="history")
        return None

    evidence, evidence_result = _fetch_binding_evidence(
        symbol,
        binding,
        cache_type=cache_type,
        cache_kind="history",
    )
    if evidence_result is not None or evidence is None:
        result = evidence_result or QuarantineResult(
            QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED,
            binding.asset_id,
        )
        _log_quarantine(result, symbol=symbol, kind="history")
        return None

    _inc("yahoo_requests")
    t0 = time.monotonic()
    try:
        df = _provider.get_history(symbol, period, interval)
        _record_yf_call(t0)
        _log.info("[LOCAL FETCH] yahoo_fetch symbol=%s type=%s", symbol, cache_type)
        if df is not None and not df.empty:
            payload = _df_to_payload(df)
            payload[_BOUND_PROVIDER_KEY] = getattr(evidence, "provider")
            _set_cached(symbol, cache_type, payload, _history_ttl(period, interval))
        return df
    except Exception as exc:
        _record_yf_error(exc)
        result = QuarantineResult(
            QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED,
            binding.asset_id,
        )
        _log_quarantine(result, symbol=symbol, kind="history")
        return None


def fetch_history(
    symbol: str,
    period: str = "6mo",
    interval: str = "1d",
    binding: SuccessorQuoteBinding | None = None,
) -> Optional[pd.DataFrame]:
    #print("fetch_history()", symbol)
    if binding is not None:
        return _fetch_history_bound(symbol, period, interval, binding)

    guard_result = _unbound_guard_result(symbol)
    if guard_result is not None:
        _log_quarantine(guard_result, symbol=symbol, kind="history")
        return None

    cache_type = f"history:{period}:{interval}"
    ttl        = _history_ttl(period, interval)

    cached = _get_cached(symbol, cache_type)
    if cached:
        df_cached = _payload_to_df(cached)
        if df_cached is not None and not df_cached.empty:
            return df_cached

    if not allow_market_fetching():
        _log.info("[VPS BLOCKED FETCH] fetch_history symbol=%s — returning stale cache", symbol)
        stale = _get_stale(symbol, cache_type)
        return _payload_to_df(stale) if stale else None

    _inc("yahoo_requests")
    t0 = time.monotonic()
    try:
        df = _provider.get_history(symbol, period, interval)
        _record_yf_call(t0)
        _log.info("[LOCAL FETCH] yahoo_fetch symbol=%s type=%s", symbol, cache_type)
        if df is not None and not df.empty:
            _set_cached(symbol, cache_type, _df_to_payload(df), ttl)
        return df
    except Exception as exc:
        _record_yf_error(exc)
        stale = _get_stale(symbol, cache_type)
        return _payload_to_df(stale) if stale else None


def fetch_info(symbol: str) -> dict:
    """Fetch yfinance .info for a symbol.
    Callers are responsible for normalising DR symbols via normalize_dr_symbol() first."""
    cache_type = "fundamental"

    cached = _get_cached(symbol, cache_type)
    if cached:
        return _source_quote_payload(cached)

    if not allow_market_fetching():
        _log.info("[VPS BLOCKED FETCH] fetch_info symbol=%s — returning stale cache", symbol)
        stale = _get_stale(symbol, cache_type)
        if stale:
            return _source_quote_payload(stale)
        return {}

    _inc("yahoo_requests")
    t0 = time.monotonic()
    try:
        info = _provider.get_fundamentals(symbol)
        _record_yf_call(t0)
        _log.info("[LOCAL FETCH] yahoo_fetch symbol=%s type=fundamental", symbol)
        if info:
            _set_cached(symbol, cache_type, info, _TTL_FUND)
        return info or {}
    except Exception as exc:
        _record_yf_error(exc)
        stale = _get_stale(symbol, cache_type)
        if stale:
            return {k: v for k, v in stale.items() if not k.startswith("_")}
        return {}


def calculate_change_percent(
    current_price: float | None,
    previous_close: float | None,
) -> float | None:
    if (
        current_price is None
        or previous_close is None
        or previous_close == 0
    ):
        return None

    return round(
        (current_price - previous_close)
        / previous_close
        * 100,
        2,
    )


def _fetch_price_info_bound(
    symbol: str,
    binding: SuccessorQuoteBinding,
) -> dict:
    """Fetch a converted quote through provider evidence and WP3.2 checks."""
    request_result = _binding_request_identity_result(symbol, binding)
    if request_result is not None:
        return _quote_quarantine_response(request_result, symbol=symbol)
    try:
        cache_type = quote_cache_type(binding)
    except (AttributeError, TypeError, ValueError, ArithmeticError):
        return _quote_quarantine_response(
            QuarantineResult(
                QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
                getattr(binding, "asset_id", 0)
                if isinstance(getattr(binding, "asset_id", 0), int)
                else 0,
            ),
            symbol=symbol,
        )

    cached = _get_cached(symbol, cache_type)
    if cached:
        if _bound_cache_hit(cached, binding):
            return _source_quote_payload(cached)
        _log.warning(
            "bound_cache_rejected symbol=%s type=%s reason=provider_namespace_mismatch",
            symbol,
            cache_type,
        )

    # Converted identities never receive a stale predecessor value.  A
    # cache miss on the bound path is either refreshed from qualifying
    # evidence or refused.
    if not allow_market_fetching():
        return _quote_quarantine_response(
            QuarantineResult(
                QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED,
                binding.asset_id,
            ),
            symbol=symbol,
        )

    _inc("yahoo_requests")
    t0 = time.monotonic()
    evidence, evidence_result = _fetch_binding_evidence(
        symbol,
        binding,
        cache_type=cache_type,
        cache_kind="quote",
    )
    _record_yf_call(t0)
    if evidence_result is not None or evidence is None:
        result = evidence_result or QuarantineResult(
            QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED,
            binding.asset_id,
        )
        return _quote_quarantine_response(result, symbol=symbol)

    try:
        result = _evidence_to_quote_payload(evidence)
    except Exception as exc:
        _log.warning(
            "provider_evidence_unavailable symbol=%s error_type=%s",
            symbol,
            type(exc).__name__,
        )
        return _quote_quarantine_response(
            QuarantineResult(
                QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED,
                binding.asset_id,
            ),
            symbol=symbol,
        )

    cache_payload = {**result, _BOUND_PROVIDER_KEY: getattr(evidence, "provider")}
    _log.info("[LOCAL FETCH] yahoo_fetch symbol=%s type=%s", symbol, cache_type)
    if result.get("current_price") is not None:
        _set_cached(symbol, cache_type, cache_payload, _TTL_QUOTE)
    return result


def _fetch_price_info_legacy(symbol: str) -> dict:
    """The pre-WP3.3 unbound quote path, retained byte-for-byte in behavior."""
    cache_type = "quote"

    DEBUG_BYPASS_CACHE = False
    if not DEBUG_BYPASS_CACHE:
        cached = _get_cached(symbol, cache_type)
        if cached:
            return {k: v for k, v in cached.items() if not k.startswith("_")}

        if not allow_market_fetching():
            _log.info("[VPS BLOCKED FETCH] fetch_price_info symbol=%s — returning stale cache", symbol)
            stale = _get_stale(symbol, cache_type)
            if stale:
                return {k: v for k, v in stale.items() if not k.startswith("_")}
            return {"current_price": None, "previous_close": None, "last_updated": None, "_vps_cache_miss": True}

    _inc("yahoo_requests")
    t0 = time.monotonic()
    try:
        result = _source_quote_payload(_provider.get_quote(symbol))
        _record_yf_call(t0)
        _log.info("[LOCAL FETCH] yahoo_fetch symbol=%s type=quote", symbol)
        if result.get("current_price") is not None:
            _set_cached(symbol, cache_type, result, _TTL_QUOTE)
        return result
    except Exception as exc:
        _record_yf_error(exc)
        stale = _get_stale(symbol, cache_type)
        if stale:
            return _source_quote_payload(stale)
        return {"current_price": None, "previous_close": None, "last_updated": None}


def fetch_price_info(
    symbol: str,
    binding: SuccessorQuoteBinding | None = None,
) -> dict:
    """Return {current_price, previous_close, last_updated} for a symbol.

    A binding is the only route to a converted-identity quote.  Symbol-only
    callers remain on the legacy path while the canonical guard projection is
    empty; once a conversion row exists, they receive a structured refusal.
    """
    if binding is not None:
        return _fetch_price_info_bound(symbol, binding)

    guard_result = _unbound_guard_result(symbol)
    if guard_result is not None:
        return _quote_quarantine_response(guard_result, symbol=symbol)
    return _fetch_price_info_legacy(symbol)


def fetch_news(symbol: str) -> list[dict]:
    """Callers are responsible for normalising DR symbols via normalize_dr_symbol() first."""
    if not allow_market_fetching():
        _log.info("[VPS BLOCKED FETCH] fetch_news symbol=%s — returning empty list", symbol)
        return []

    # News is short-lived and already managed by AgentCache (1 h TTL).
    _inc("yahoo_requests")
    t0 = time.monotonic()
    try:
        result = _provider.get_news(symbol)
        _record_yf_call(t0)
        _log.info("[LOCAL FETCH] yahoo_fetch symbol=%s type=news", symbol)
        return result
    except Exception as exc:
        _record_yf_error(exc)
        return []


def prefetch_history_batch(
    symbols: list[str],
    period: str = "6mo",
    interval: str = "1d",
    bindings: Mapping[str, SuccessorQuoteBinding] | None = None,
) -> None:
    """Warm the cache for a batch of symbols using yf.download() in chunks.

    Call this before a concurrent analysis burst to replace N individual
    yfinance requests with ceil(N/15) batched downloads.
    Only fetches symbols whose cache entry is missing or expired.
    Silently skips on VPS — the cache was pre-warmed by the Local Research Node.
    """
    if not allow_market_fetching():
        _log.info("[VPS BLOCKED FETCH] prefetch_history_batch — skipped on VPS")
        return

    legacy_cache_type = f"history:{period}:{interval}"
    ttl = _history_ttl(period, interval)
    bindings = bindings or {}
    guard_projection = (
        _read_conversion_guard_projection()
        if any(symbol not in bindings for symbol in symbols)
        else None
    )

    candidates: list[tuple[str, str, SuccessorQuoteBinding | None]] = []
    for symbol in symbols:
        binding = bindings.get(symbol)
        if binding is None:
            guard_result = _guard_result_from_projection(symbol, guard_projection)
            if guard_result is not None:
                _log_quarantine(guard_result, symbol=symbol, kind="history")
                continue
            cache_type = legacy_cache_type
        else:
            request_result = _binding_request_identity_result(symbol, binding)
            if request_result is not None:
                _log_quarantine(request_result, symbol=symbol, kind="history")
                continue
            try:
                cache_type = _history_cache_type_for_binding(binding, period, interval)
            except (AttributeError, TypeError, ValueError, ArithmeticError):
                result = QuarantineResult(
                    QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
                    getattr(binding, "asset_id", 0)
                    if isinstance(getattr(binding, "asset_id", 0), int)
                    else 0,
                )
                _log_quarantine(result, symbol=symbol, kind="history")
                continue
            if cache_type is None:
                result = QuarantineResult(
                    QuarantineReason.CACHE_NAMESPACE_MISMATCH,
                    binding.asset_id,
                )
                _log_quarantine(result, symbol=symbol, kind="history")
                continue

        cached = _get_cached(symbol, cache_type)
        if cached is not None and (
            binding is None or _bound_cache_hit(cached, binding)
        ):
            continue
        if cached is not None and binding is not None:
            _log.warning(
                "bound_cache_rejected symbol=%s type=%s reason=provider_namespace_mismatch",
                symbol,
                cache_type,
            )
        candidates.append((symbol, cache_type, binding))

    if not candidates:
        return

    # A binding-aware history read must establish the same provider identity,
    # served-symbol identity, and successor epoch before the separate history
    # response is used.  Unbound candidates retain the legacy batch behavior.
    bound_evidence: dict[str, object] = {}
    eligible: list[tuple[str, str, SuccessorQuoteBinding | None]] = []
    for symbol, cache_type, binding in candidates:
        if binding is None:
            eligible.append((symbol, cache_type, None))
            continue
        evidence, evidence_result = _fetch_binding_evidence(
            symbol,
            binding,
            cache_type=cache_type,
            cache_kind="history",
        )
        if evidence_result is not None or evidence is None:
            result = evidence_result or QuarantineResult(
                QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED,
                binding.asset_id,
            )
            _log_quarantine(result, symbol=symbol, kind="history")
            continue
        bound_evidence[symbol] = evidence
        eligible.append((symbol, cache_type, binding))

    if not eligible:
        return

    fetch_symbols = [symbol for symbol, _, _ in eligible]
    _log.info(
        "[LOCAL FETCH] prefetch_history_batch symbols=%d period=%s interval=%s",
        len(fetch_symbols),
        period,
        interval,
    )
    _inc("yahoo_requests", len(fetch_symbols))
    t0 = time.monotonic()
    try:
        batch = _provider.get_history_batch(fetch_symbols, period, interval)
        _record_yf_call(t0)
        by_symbol = {
            symbol: (cache_type, binding)
            for symbol, cache_type, binding in eligible
        }
        for symbol, df in batch.items():
            if df is None or df.empty or symbol not in by_symbol:
                continue
            cache_type, binding = by_symbol[symbol]
            payload = _df_to_payload(df)
            if binding is not None:
                payload[_BOUND_PROVIDER_KEY] = getattr(bound_evidence[symbol], "provider")
            _set_cached(symbol, cache_type, payload, ttl)
    except Exception as exc:
        _record_yf_error(exc)
