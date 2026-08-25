"""Pure-Python Yahoo Finance Chart API provider.

Replaces yfinance's ``Ticker.history()`` for the historical-price pipeline.

Background
----------
yfinance >= 0.2.37 uses curl_cffi (a compiled native DLL) for browser
impersonation. On Windows + Python 3.13 that DLL crashes the whole
interpreter with an access violation (exit code 0xC0000005 /
-1073741819) when fetching large responses — observed for ``period="5y"``
on SET (.BK) symbols. This is a native crash, not a Python exception, so
it cannot be caught with try/except and previously took down the entire
process.

This provider talks directly to the same Yahoo Finance Chart endpoint
yfinance uses internally:

    https://query1.finance.yahoo.com/v8/finance/chart/{symbol}

via plain ``requests``. Every failure mode (network error, HTTP error,
malformed JSON, Yahoo-side error, empty result) is caught in Python and
degrades to ``None`` — it can never crash the interpreter.

``get_fundamentals()`` and ``get_news()`` have no equivalent on the chart
endpoint; those are delegated to the legacy yfinance-backed YahooProvider,
since the user-reported crash is specific to ``.history()`` on large date
ranges, not ``.info`` / ``.news``.
"""
from __future__ import annotations

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import pandas as pd
import requests

from .base import MarketDataProvider
from .execution_quote import (
    ExecutionQuoteEnvelope,
    adapt_yahoo_chart_execution_quote,
)

_log = logging.getLogger(__name__)

_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
_TIMEOUT_S = 10
_MAX_ATTEMPTS = 3
_MAX_WORKERS = 5

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

_session = requests.Session()
_session.headers.update(_HEADERS)

# Bounds concurrent outbound requests across all threads (mirrors yahoo.py's
# _YF_SEMAPHORE) to stay well under Yahoo's undocumented per-IP rate limit.
_SEMAPHORE = threading.Semaphore(_MAX_WORKERS)


def _fetch_chart_result(symbol: str, range_: str, interval: str) -> Optional[dict]:
    """GET the raw ``chart.result[0]`` payload for *symbol*, or None on any failure.

    Never raises. Every failure mode is caught and logged here so callers can
    treat None uniformly as "no data available right now".
    """
    url = _CHART_URL.format(symbol=symbol)
    params = {
        "range": range_,
        "interval": interval,
        "includeAdjustedClose": "true",
        "events": "div,splits",
    }

    for attempt in range(_MAX_ATTEMPTS):
        try:
            resp = _session.get(url, params=params, timeout=_TIMEOUT_S)
        except requests.exceptions.RequestException as e:
            _log.warning("YahooChartProvider network error symbol=%s: %s", symbol, e)
            return None

        if resp.status_code == 429 and attempt < _MAX_ATTEMPTS - 1:
            wait = (2 ** attempt) + 1.0
            _log.warning("YahooChartProvider 429 symbol=%s – retry in %.1fs", symbol, wait)
            time.sleep(wait)
            continue

        if resp.status_code != 200:
            _log.warning("YahooChartProvider HTTP %d symbol=%s", resp.status_code, symbol)
            return None

        try:
            payload = resp.json()
        except ValueError as e:
            _log.warning("YahooChartProvider invalid JSON symbol=%s: %s", symbol, e)
            return None

        chart = payload.get("chart") or {}
        if chart.get("error"):
            _log.info("YahooChartProvider chart error symbol=%s: %s", symbol, chart["error"])
            return None

        results = chart.get("result")
        if not results:
            return None
        return results[0]

    return None


def _chart_result_to_df(result: dict) -> Optional[pd.DataFrame]:
    """Convert a raw ``chart.result[0]`` dict into an OHLCV DataFrame, or None if empty."""
    timestamps = result.get("timestamp")
    if not timestamps:
        return None

    indicators = result.get("indicators") or {}
    quote_list = indicators.get("quote") or [{}]
    quote = quote_list[0] if quote_list else {}
    adjclose_list = indicators.get("adjclose") or []
    adjclose = adjclose_list[0].get("adjclose") if adjclose_list else None

    index = pd.to_datetime(timestamps, unit="s", utc=True)
    df = pd.DataFrame(
        {
            "Open":   quote.get("open"),
            "High":   quote.get("high"),
            "Low":    quote.get("low"),
            "Close":  quote.get("close"),
            "Volume": quote.get("volume"),
        },
        index=index,
    )
    df["Adj Close"] = adjclose if adjclose is not None else df["Close"]

    # Sort + dedupe before mapping events onto bars — asof() requires a
    # monotonic, unique index.
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]

    df["Dividends"] = 0.0
    df["Stock Splits"] = 0.0

    events = result.get("events") or {}
    for ts_str, ev in (events.get("dividends") or {}).items():
        ts = pd.to_datetime(int(ts_str), unit="s", utc=True)
        nearest = df.index.asof(ts)
        if pd.notna(nearest):
            df.loc[nearest, "Dividends"] = ev.get("amount", 0.0)
    for ts_str, ev in (events.get("splits") or {}).items():
        ts = pd.to_datetime(int(ts_str), unit="s", utc=True)
        nearest = df.index.asof(ts)
        denom = ev.get("denominator")
        if pd.notna(nearest) and denom:
            df.loc[nearest, "Stock Splits"] = ev.get("numerator", 1) / denom

    df = df.dropna(how="all", subset=["Open", "High", "Low", "Close"])
    return df if not df.empty else None


# ── BANPU-WP3.1 provider evidence (E1-E5) ───────────────────────────────────
#
# Provider-neutral, conversion-unaware. This section supplies the raw
# provider-reported facts named by the WP3 Provider Evidence Contract
# (docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md
# §6.3). It makes no comparison, no binding, and no quarantine decision, and
# never references PositionConversion or any conversion concept. WP3.2
# consumes this shape structurally, without importing this module.

_PROVIDER_ID = "yahoo_chart"  # same identity convention already used by
                               # execution_quote.py's adapt_yahoo_chart_execution_quote()


@dataclass(frozen=True)
class QuoteObservation:
    """One (timestamp, close) pair from a single provider chart response.

    ``timestamp`` is the provider's raw epoch-seconds value, unmodified, in
    provider-returned order. ``close`` may be ``None`` (a sparse/no-trade
    bar) -- carried as-is, never dropped or substituted here.
    """

    timestamp: int
    close: Optional[float]


@dataclass(frozen=True)
class ProviderQuoteEvidence:
    """Provider-neutral, conversion-unaware evidence for one quote response.

    Immutable. Fields correspond 1:1 to the WP3 Provider Evidence Contract:

        E1 provider                  -- the provider identity this adapter acts as
        E2 served_symbol              -- raw meta.symbol, uncompared against anything
        E3 observations                -- raw (timestamp, close) pairs, provider order
        E4 current_close/previous_close -- derived from this one response only
        E5 exchange_timezone_name       -- raw meta.exchangeTimezoneName

    ``previous_close`` is derived by timestamp-associated matching (skipping
    sparse/null bars and collapsing duplicate timestamps), never by
    positional indexing -- this is the PD-1 corrected derivation.
    ``get_quote()`` calls ``_extract_provider_evidence`` and reuses this same
    ``previous_close`` value, so the legacy dictionary and this evidence
    structure share one definition of "previous close".

    Invariant (see ``_previous_close_from_observations`` for the exact
    algorithm): the observation at the highest chart timestamp is treated as
    belonging to the same trading session as ``current_close``
    (``meta.regularMarketPrice``), whether or not that bar's own close is
    populated -- this matches every provider response observed for the
    5-day/1-day request this method issues, where the last returned bar is
    always today's. ``previous_close`` is the close of the most recent
    *distinct* session strictly before that one. This is not a general
    exchange-calendar/trading-session classification; it relies on that one
    observed provider convention and nothing stronger.
    """

    provider: str
    requested_symbol: str
    served_symbol: Optional[str]
    observations: "tuple[QuoteObservation, ...]"
    current_close: Optional[float]
    previous_close: Optional[float]
    exchange_timezone_name: Optional[str]


def _dedup_sessions_by_timestamp(
    observations: "tuple[QuoteObservation, ...]",
) -> "tuple[QuoteObservation, ...]":
    """Collapse same-timestamp observations into one session per timestamp.

    Sorts ascending by timestamp, then for any repeated timestamp keeps the
    *last* provider-returned value for it. This mirrors the duplicate-index
    policy ``_chart_result_to_df`` already applies to the same chart payload
    (``sort_index()`` then ``duplicated(keep="last")``): a stable sort
    preserves each duplicate's original relative order, so "last after a
    stable sort" is exactly "last in provider-returned order" -- the same
    row the history path treats as authoritative.
    """
    ordered = sorted(observations, key=lambda obs: obs.timestamp)
    by_timestamp: dict[int, QuoteObservation] = {}
    for obs in ordered:
        by_timestamp[obs.timestamp] = obs  # a later duplicate overwrites the earlier one
    return tuple(by_timestamp[ts] for ts in sorted(by_timestamp))


def _previous_close_from_observations(
    observations: "tuple[QuoteObservation, ...]",
) -> Optional[float]:
    """Derive previous_close per the invariant documented on ProviderQuoteEvidence.

    1. Collapse duplicate timestamps to one session each (``keep last``).
    2. Drop the single most-recent distinct session -- it is treated as the
       same session as the live quote (``current_close``), regardless of
       whether that session's own close is populated (a null close there
       means today hasn't produced a completed bar yet; a non-null close
       there means the chart's last bar already reflects today).
    3. Return the close of the most recent remaining session that has a
       non-null close, skipping any sparse/no-trade bars in between.
    """
    sessions = _dedup_sessions_by_timestamp(observations)
    if len(sessions) < 2:
        return None
    for obs in reversed(sessions[:-1]):
        if obs.close is not None:
            return obs.close
    return None


def _extract_provider_evidence(result: dict, requested_symbol: str) -> ProviderQuoteEvidence:
    """Build the WP3 provider evidence structure from one raw chart result.

    Pure: no I/O, no clock, no registry lookup, no conversion awareness.
    ``result`` is the same ``chart.result[0]`` shape ``_fetch_chart_result``
    returns -- the caller supplies it so evidence and any corrected
    derivation come from a single fetched response (E4).
    """
    meta = result.get("meta") or {}
    indicators = result.get("indicators") or {}
    quote_list = indicators.get("quote") or [{}]
    quote0 = quote_list[0] if quote_list else {}
    closes = quote0.get("close") or []
    timestamps = result.get("timestamp") or []

    observations = tuple(
        QuoteObservation(timestamp=ts, close=c) for ts, c in zip(timestamps, closes)
    )

    # E4 -- see _previous_close_from_observations for the exact algorithm.
    # This evidence contract is separate from the legacy quote dictionary's
    # former metadata-driven behavior; get_quote() now reuses this same
    # derivation instead.
    previous_close = _previous_close_from_observations(observations)

    return ProviderQuoteEvidence(
        provider=_PROVIDER_ID,
        requested_symbol=requested_symbol,
        served_symbol=meta.get("symbol"),
        observations=observations,
        current_close=meta.get("regularMarketPrice"),
        previous_close=previous_close,
        exchange_timezone_name=meta.get("exchangeTimezoneName"),
    )


class YahooChartProvider(MarketDataProvider):
    """MarketDataProvider backed directly by the Yahoo Finance Chart API.

    Pure-Python HTTP (requests) — no curl_cffi, no native dependency in the
    historical-price path. Cannot crash the interpreter; every failure mode
    degrades to None / {} / [].
    """

    def __init__(self) -> None:
        self._legacy: Optional[MarketDataProvider] = None

    def _legacy_provider(self) -> MarketDataProvider:
        """Lazily-built yfinance-backed provider, used only for .info / .news."""
        if self._legacy is None:
            from .yahoo import YahooProvider
            self._legacy = YahooProvider()
        return self._legacy

    def get_quote(self, symbol: str) -> dict:
        with _SEMAPHORE:
            t0 = time.perf_counter()
            result = _fetch_chart_result(symbol, range_="5d", interval="1d")
            elapsed = time.perf_counter() - t0
            # print(
            #     symbol,
            #     "5d",
            #     "1d",
            #     round(elapsed, 3),
            # )
        if result is None:
            return {"current_price": None, "previous_close": None, "last_updated": None}

        # Previous close is derived by the same timestamp-associated,
        # duplicate-collapsing, skip-null evidence logic get_quote_evidence()
        # uses (E4) -- not from meta.previousClose / meta.chartPreviousClose /
        # meta.regularMarketPreviousClose. Only meta.chartPreviousClose has
        # been demonstrated (live, 2026-08-18) to be unsuitable as canonical
        # previous-session evidence: with this method's fixed 5-day window it
        # is anchored to the start of that window rather than to the session
        # immediately before the latest bar, so it silently returns a close
        # from several trading sessions ago. previousClose and
        # regularMarketPreviousClose were unpopulated (None) in every
        # response observed and were never proven to share that same
        # window-anchoring behavior; they simply aren't consulted anymore
        # either, since one shared, provider-response-derived definition
        # keeps get_quote() and get_quote_evidence() from disagreeing about
        # what "previous close" means.
        evidence = _extract_provider_evidence(result, requested_symbol=symbol)
        current_price = evidence.current_close
        prev_close = evidence.previous_close

        return {
            "current_price": round(current_price, 4) if current_price is not None else None,
            "previous_close": prev_close,
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    def get_execution_quote_envelope(self, symbol: str) -> ExecutionQuoteEnvelope | None:
        """Fetch one additive M32.3E2 quote envelope.

        This is deliberately separate from ``get_quote`` so legacy consumers
        retain their existing three-field dictionary.  The receipt instant is
        captured at this I/O boundary and passed to the pure adapter.
        """

        with _SEMAPHORE:
            result = _fetch_chart_result(symbol, range_="5d", interval="1d")
            received_at = datetime.now(timezone.utc)
        if result is None:
            return None
        return adapt_yahoo_chart_execution_quote(
            result,
            requested_symbol=symbol,
            provider_symbol=symbol,
            received_at=received_at,
        )

    def get_execution_quote_envelopes(
        self,
        symbols: list[str],
    ) -> dict[str, ExecutionQuoteEnvelope | None]:
        """Bounded concurrent Chart evidence fetches; the endpoint has no batch API."""

        unique_symbols = list(dict.fromkeys(symbols))
        if not unique_symbols:
            return {}
        results: dict[str, ExecutionQuoteEnvelope | None] = {}
        with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as executor:
            futures = {
                executor.submit(self.get_execution_quote_envelope, symbol): symbol
                for symbol in unique_symbols
            }
            for future in as_completed(futures):
                symbol = futures[future]
                try:
                    results[symbol] = future.result()
                except Exception as exc:  # defensive: preserve per-symbol isolation
                    _log.warning("YahooChartProvider execution quote failed symbol=%s: %s", symbol, exc)
                    results[symbol] = None
        return results

    def get_quote_evidence(self, symbol: str) -> Optional[ProviderQuoteEvidence]:
        """Fetch one WP3 provider evidence structure (E1-E5).

        ``get_quote()`` derives its ``previous_close`` from this same
        ``_extract_provider_evidence`` logic, so the two methods cannot
        disagree about what "previous close" means -- they differ only in
        return shape (this one is the full E1-E5 evidence structure, built
        from a single fetched response). This method has no knowledge of
        PositionConversion, binding, epoch, or quarantine concepts.
        """
        with _SEMAPHORE:
            result = _fetch_chart_result(symbol, range_="5d", interval="1d")
        if result is None:
            return None
        return _extract_provider_evidence(result, requested_symbol=symbol)

    def get_history(
        self, symbol: str, period: str = "6mo", interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        with _SEMAPHORE:
            result = _fetch_chart_result(symbol, range_=period, interval=interval)
        if result is None:
            return None
        try:
            return _chart_result_to_df(result)
        except Exception as e:
            _log.error("YahooChartProvider parse error symbol=%s period=%s: %s", symbol, period, e)
            return None

    def get_fundamentals(self, symbol: str) -> dict:
        return self._legacy_provider().get_fundamentals(symbol)

    def get_news(self, symbol: str) -> list[dict]:
        return self._legacy_provider().get_news(symbol)

    def get_history_batch(
        self, symbols: list[str], period: str = "6mo", interval: str = "1d"
    ) -> dict[str, pd.DataFrame]:
        """Concurrent per-symbol fetch — the chart endpoint has no native multi-symbol batch call."""
        result: dict[str, pd.DataFrame] = {}
        if not symbols:
            return result
        with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as ex:
            futures = {ex.submit(self.get_history, sym, period, interval): sym for sym in symbols}
            for fut in as_completed(futures):
                sym = futures[fut]
                try:
                    df = fut.result()
                except Exception as e:
                    _log.warning("YahooChartProvider batch fetch failed symbol=%s: %s", sym, e)
                    df = None
                if df is not None and not df.empty:
                    result[sym] = df
        return result
