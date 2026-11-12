"""Read-only loaders for the Slice 4.5A liquidity shadow diagnostic.

Reads existing ``market_data_cache`` daily-history rows for exact listing
symbols with a plain SELECT. Unlike ``data_fetcher.fetch_history`` it never
increments cache hit counters, never writes the cache and never fetches from a
provider, so a diagnostic run performs no database writes and no network I/O.

Only the unbound ``history:{period}:1d`` namespace is read. Converted listings
(position-conversion successors) are refused by the same WP3.3 guard that
``fetch_history`` applies and are reported as quarantined, never read.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from sqlalchemy.orm import Session

from models.database import MarketDataCache, OptimizerHistory, RecommendationSnapshot
from services.data_fetcher import history_payload_to_frame, unbound_history_guard_reasons
from services.execution_instrument_facts import resolve_execution_instruments
from services.optimizer.execution_penalty import compute_portfolio_execution_context
from services.optimizer.liquidity_evidence import DailyBar, ListingHistory, build_liquidity_shadow

__all__ = [
    "listing_histories_from_cache_rows",
    "load_listing_histories",
    "evaluate_history_liquidity_shadow",
]

_DAILY_HISTORY_LIKE = "history:%:1d"


def _aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


def listing_histories_from_cache_rows(
    rows: Sequence[tuple[str, str, str, datetime | None, datetime | None]],
    *,
    as_of: datetime,
) -> dict[str, list[ListingHistory]]:
    """Decode ``(symbol, cache_type, payload_json, fetched_at, expires_at)`` rows."""
    out: dict[str, list[ListingHistory]] = {}
    as_of = _aware(as_of)
    for symbol, cache_type, payload_json, fetched_at, expires_at in rows:
        try:
            frame = history_payload_to_frame(json.loads(payload_json))
        except (TypeError, ValueError):
            frame = None
        bars: tuple[DailyBar, ...] = ()
        if frame is not None and not frame.empty:
            close = frame["Close"] if "Close" in frame.columns else None
            volume = frame["Volume"] if "Volume" in frame.columns else None
            bars = tuple(
                DailyBar(
                    timestamp=ts.to_pydatetime(),
                    close=None if close is None else _plain(close.iloc[i]),
                    volume=None if volume is None else _plain(volume.iloc[i]),
                )
                for i, ts in enumerate(frame.index)
            )
        expires = _aware(expires_at)
        out.setdefault(symbol, []).append(ListingHistory(
            listing_symbol=symbol,
            bars=bars,
            source=f"market_data_cache:{cache_type}",
            fetched_at=_aware(fetched_at),
            cache_expired=None if expires is None else expires < as_of,
        ))
    for histories in out.values():
        histories.sort(key=lambda h: h.source)
    return out


def _plain(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return None if number != number else number   # NaN -> None


def load_listing_histories(
    db: Session,
    listing_symbols: Sequence[str],
    *,
    as_of: datetime,
) -> dict[str, list[ListingHistory]]:
    """All unbound daily-history cache rows for exactly these listing symbols."""
    symbols = sorted(set(listing_symbols))
    if not symbols:
        return {}
    rows = (
        db.query(MarketDataCache.symbol, MarketDataCache.cache_type, MarketDataCache.payload_json,
                 MarketDataCache.fetched_at, MarketDataCache.expires_at)
        .filter(MarketDataCache.symbol.in_(symbols))
        .filter(MarketDataCache.cache_type.like(_DAILY_HISTORY_LIKE))
        .all()
    )
    return listing_histories_from_cache_rows([tuple(r) for r in rows], as_of=as_of)


def _decode(value: Any) -> Any:
    while isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            break
    return value


def evaluate_history_liquidity_shadow(
    db: Session,
    history_id: int,
    *,
    as_of: datetime | None = None,
    quarantine_reasons: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Shadow report for the universe of one stored optimizer run.

    Reads the run's stored scores map (frozen prices, ``is_dr``) and current
    Registry facts; recomputes the active execution context exactly as the
    optimizer would today (no volume), and evaluates observed liquidity beside
    it. Stored runs and snapshots are only read. ``as_of`` defaults to the
    run's ``analyzed_at``.
    """
    history = db.query(OptimizerHistory).filter_by(id=history_id).first()
    if history is None:
        raise LookupError(f"optimizer history {history_id} not found")
    snapshot = db.query(RecommendationSnapshot).filter_by(optimizer_history_id=history_id).first()
    if snapshot is None or not snapshot.scores_map_json:
        raise LookupError(f"optimizer history {history_id} has no stored scores map")
    scores_map = _decode(snapshot.scores_map_json)
    as_of = _aware(as_of or history.analyzed_at)
    symbols = tuple(scores_map)
    facts = resolve_execution_instruments(db, symbols)
    active = compute_portfolio_execution_context(scores_map, facts_by_symbol=facts)
    if quarantine_reasons is None:
        quarantine_reasons = unbound_history_guard_reasons(list(symbols))
    histories = load_listing_histories(db, symbols, as_of=as_of)
    report = build_liquidity_shadow(
        scores_map, active,
        histories_by_symbol=histories, facts_by_symbol=facts,
        as_of=as_of, quarantine_reasons=quarantine_reasons,
    )
    report["source"] = {"optimizer_history_id": history_id,
                        "analyzed_at": _aware(history.analyzed_at).isoformat(),
                        "active_context": "recomputed with current Registry facts; no volume (as production)"}
    return report
