"""Regression tests for services.market_data.yahoo_chart.YahooChartProvider.

Two layers:
  1. Mocked unit tests (default) — no network, deterministic, run in CI.
     Cover DataFrame shape/columns/sort/dedup and every failure mode
     (invalid symbol, HTTP error, timeout, malformed JSON).
  2. Live smoke tests — actually hit Yahoo Finance for the US/TH symbol
     list across 1mo/3mo/1y/5y. Skipped unless RUN_LIVE_MARKET_TESTS=1,
     since CI shouldn't depend on an external network call succeeding.
     Run manually with:
         RUN_LIVE_MARKET_TESTS=1 python -m pytest backend/tests/test_yahoo_chart_provider.py -v
"""
import os
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import pytest
import requests

from services.market_data.provider import get_provider
from services.market_data.yahoo import YahooProvider
from services.market_data.yahoo_chart import (
    ProviderQuoteEvidence,
    QuoteObservation,
    YahooChartProvider,
    _chart_result_to_df,
    _dedup_sessions_by_timestamp,
    _extract_provider_evidence,
    _previous_close_from_observations,
)


# ── Fixture payload builder ────────────────────────────────────────────────────

def _make_payload(
    timestamps: list[int],
    opens: list[float | None],
    highs: list[float | None],
    lows: list[float | None],
    closes: list[float | None],
    volumes: list[int | None],
    dividends: dict[str, dict] | None = None,
    splits: dict[str, dict] | None = None,
    meta_overrides: dict | None = None,
) -> dict:
    meta = {
        "regularMarketPrice": closes[-1] if closes else None,
        "previousClose": closes[-2] if len(closes) >= 2 else None,
    }
    if meta_overrides:
        meta.update(meta_overrides)
    return {
        "chart": {
            "result": [
                {
                    "meta": meta,
                    "timestamp": timestamps,
                    "events": {
                        "dividends": dividends or {},
                        "splits": splits or {},
                    },
                    "indicators": {
                        "quote": [{"open": opens, "high": highs, "low": lows, "close": closes, "volume": volumes}],
                        "adjclose": [{"adjclose": closes}],
                    },
                }
            ],
            "error": None,
        }
    }


def _error_payload(code: str = "Not Found", description: str = "No data found, symbol may be delisted") -> dict:
    return {"chart": {"result": None, "error": {"code": code, "description": description}}}


class _MockResponse:
    def __init__(self, status_code: int = 200, json_data: dict | None = None):
        self.status_code = status_code
        self._json_data = json_data

    def json(self):
        if self._json_data is None:
            raise ValueError("no json body")
        return self._json_data


_BASE_TS = [1717113600, 1717200000, 1717286400, 1717372800, 1717459200]  # 5 consecutive days (UTC)
_BASE_CLOSES = [10.0, 10.5, 10.2, 10.8, 11.0]


def _patched_get(provider_module: str = "services.market_data.yahoo_chart"):
    return patch(f"{provider_module}._session.get")


# ── get_history: happy path ────────────────────────────────────────────────────

def test_get_history_returns_required_columns():
    payload = _make_payload(_BASE_TS, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, [1000] * 5)
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, payload)
        df = YahooChartProvider().get_history("GULF.BK", period="1mo", interval="1d")

    assert df is not None
    for col in ["Open", "High", "Low", "Close", "Volume", "Adj Close", "Dividends", "Stock Splits"]:
        assert col in df.columns
    assert len(df) == 5


def test_get_history_index_is_utc_datetime_and_sorted_ascending():
    shuffled_ts = [_BASE_TS[2], _BASE_TS[0], _BASE_TS[4], _BASE_TS[1], _BASE_TS[3]]
    shuffled_closes = [10.2, 10.0, 11.0, 10.5, 10.8]
    payload = _make_payload(shuffled_ts, shuffled_closes, shuffled_closes, shuffled_closes, shuffled_closes, [1000] * 5)
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, payload)
        df = YahooChartProvider().get_history("AAPL", period="1mo", interval="1d")

    assert df is not None
    assert isinstance(df.index, pd.DatetimeIndex)
    assert str(df.index.tz) == "UTC"
    assert df.index.is_monotonic_increasing
    assert list(df["Close"]) == _BASE_CLOSES  # restored to chronological order


def test_get_history_removes_duplicate_timestamps():
    ts_with_dupe = _BASE_TS + [_BASE_TS[-1]]
    closes_with_dupe = _BASE_CLOSES + [99.0]  # duplicate ts should keep this (last) value
    payload = _make_payload(ts_with_dupe, closes_with_dupe, closes_with_dupe, closes_with_dupe, closes_with_dupe, [1000] * 6)
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, payload)
        df = YahooChartProvider().get_history("PTT.BK", period="1mo", interval="1d")

    assert df is not None
    assert len(df) == len(_BASE_TS)  # dedup'd back down
    assert df["Close"].iloc[-1] == 99.0  # kept the later duplicate


def test_get_history_drops_rows_with_no_ohlc_data():
    closes = _BASE_CLOSES + [None]
    ts = _BASE_TS + [1717545600]
    payload = _make_payload(ts, closes, closes, closes, closes, [1000] * 5 + [None])
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, payload)
        df = YahooChartProvider().get_history("KBANK.BK", period="1mo", interval="1d")

    assert df is not None
    assert len(df) == 5  # trailing all-NaN bar dropped


# ── Dividends / splits ─────────────────────────────────────────────────────────

def test_dividends_and_splits_populated_on_matching_bar():
    div_ts = str(_BASE_TS[2])
    split_ts = str(_BASE_TS[3])
    payload = _make_payload(
        _BASE_TS, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, [1000] * 5,
        dividends={div_ts: {"amount": 1.25, "date": int(div_ts)}},
        splits={split_ts: {"numerator": 2, "denominator": 1, "date": int(split_ts)}},
    )
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, payload)
        df = YahooChartProvider().get_history("ADVANC.BK", period="1mo", interval="1d")

    assert df is not None
    assert df["Dividends"].iloc[2] == 1.25
    assert df["Stock Splits"].iloc[3] == 2.0
    # all other bars stay at the sensible default
    assert df["Dividends"].sum() == 1.25
    assert df["Stock Splits"].replace(0.0, pd.NA).count() == 1


# ── Failure modes — must all return None, never raise ──────────────────────────

def test_invalid_symbol_returns_none():
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, _error_payload())
        df = YahooChartProvider().get_history("NOTASYMBOL.XX", period="1mo", interval="1d")
    assert df is None


def test_http_error_status_returns_none():
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(404, None)
        df = YahooChartProvider().get_history("AAPL", period="1mo", interval="1d")
    assert df is None


def test_network_timeout_returns_none():
    with _patched_get() as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout("simulated timeout")
        df = YahooChartProvider().get_history("GULF.BK", period="5y", interval="1d")
    assert df is None


def test_connection_error_returns_none():
    with _patched_get() as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("simulated DNS failure")
        df = YahooChartProvider().get_history("GULF.BK", period="5y", interval="1d")
    assert df is None


def test_malformed_json_returns_none():
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, None)  # .json() raises ValueError
        df = YahooChartProvider().get_history("AAPL", period="1mo", interval="1d")
    assert df is None


def test_empty_result_list_returns_none():
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, {"chart": {"result": [], "error": None}})
        df = YahooChartProvider().get_history("AAPL", period="1mo", interval="1d")
    assert df is None


def test_no_timestamps_returns_none():
    payload = _make_payload([], [], [], [], [], [])
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, payload)
        df = YahooChartProvider().get_history("AAPL", period="1mo", interval="1d")
    assert df is None


def test_chart_result_to_df_handles_garbage_without_raising():
    # Defensive: a structurally-odd-but-truthy result dict shouldn't raise.
    assert _chart_result_to_df({}) is None
    assert _chart_result_to_df({"timestamp": None}) is None


# ── Rate-limit retry ────────────────────────────────────────────────────────────

def test_429_then_200_retries_and_succeeds():
    payload = _make_payload(_BASE_TS, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, [1000] * 5)
    with _patched_get() as mock_get, patch("services.market_data.yahoo_chart.time.sleep"):
        mock_get.side_effect = [_MockResponse(429, None), _MockResponse(200, payload)]
        df = YahooChartProvider().get_history("AAPL", period="1mo", interval="1d")
    assert df is not None
    assert mock_get.call_count == 2


# ── get_quote ────────────────────────────────────────────────────────────────────

def test_get_quote_returns_previous_close():
    payload = _make_payload(_BASE_TS, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, [1000] * 5,
                             meta_overrides={"regularMarketPrice": 11.0, "previousClose": 10.8})
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(200, payload)
        quote = YahooChartProvider().get_quote("AAPL")
    assert quote["current_price"] == 11.0
    assert quote["previous_close"] == 10.8
    assert quote["last_updated"] is not None


def test_get_quote_skips_null_bar_via_timestamp_associated_derivation():
    # The bar immediately before the latest one (index 3) is null/sparse.
    # get_quote() must skip it and land on the true previous completed
    # session (249.0, index 2) -- not on meta.chartPreviousClose (250.0),
    # which is anchored to the start of the chart window, not to "yesterday".
    result = _make_raw_chart_result(
        "KBANK.BK",
        248.0,
        [250.0, 248.0, 249.0, None, 248.0],
        meta_extra={"previousClose": None, "chartPreviousClose": 250.0},
    )
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("KBANK.BK")

    assert quote["current_price"] == 248.0
    assert quote["previous_close"] == 249.0


def test_get_quote_failure_returns_none_fields():
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(404, None)
        quote = YahooChartProvider().get_quote("NOTASYMBOL.XX")
    assert quote == {"current_price": None, "previous_close": None, "last_updated": None}


# ── Dashboard previous-close regression (2026-08-18 forensic investigation) ────
#
# Proven root cause: meta.chartPreviousClose is anchored to the start of the
# requested chart window ("range"), not to the trading session immediately
# before the latest bar. With a fixed 5-day window, that silently returns a
# close from ~4 trading sessions ago whenever the true previous-session value
# is absent from provider metadata (previousClose / regularMarketPreviousClose
# are unpopulated on this endpoint in practice). get_quote() must derive
# previous_close from timestamp-associated session evidence only.

def test_get_quote_ignores_stale_window_anchored_chart_previous_close():
    # Live-proven shape (PIS.BK, 2026-08-18): a 5-session window where price
    # moved meaningfully. meta.chartPreviousClose (5.15, the window-start
    # session N-4) must be ignored in favor of the true previous completed
    # session N-1 (5.60).
    closes = [5.15, 5.20, 5.20, 5.60, 5.85]  # sessions N-4 .. N (today)
    result = _make_raw_chart_result(
        "PIS.BK",
        5.85,
        closes,
        meta_extra={
            "previousClose": None,
            "chartPreviousClose": 5.15,
            "regularMarketPreviousClose": None,
        },
    )
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("PIS.BK")
    assert quote["current_price"] == 5.85
    assert quote["previous_close"] == 5.60


def test_get_quote_selects_previous_trading_session_across_holiday_gap():
    # A multi-day calendar gap between the last two bars (e.g. a market
    # holiday) must not change which session counts as "previous" --
    # selection is by trading-session order, not calendar-day arithmetic.
    base = 1_700_000_000
    timestamps = [base, base + 86400, base + 5 * 86400]  # 4 calendar days' gap before the latest bar
    closes = [10.0, 11.0, 12.0]
    result = _make_raw_chart_result("HOL.BK", 12.0, closes, timestamps=timestamps)
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("HOL.BK")
    assert quote["current_price"] == 12.0
    assert quote["previous_close"] == 11.0


def test_get_quote_skips_null_bar_across_holiday_gap():
    # Combines the holiday gap with a sparse/no-trade bar: the null bar must
    # still be skipped by timestamp, regardless of the calendar gap size.
    base = 1_700_000_000
    timestamps = [base, base + 4 * 86400, base + 5 * 86400]
    closes = [10.0, None, 12.0]
    result = _make_raw_chart_result("HOL2.BK", 12.0, closes, timestamps=timestamps)
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("HOL2.BK")
    assert quote["current_price"] == 12.0
    assert quote["previous_close"] == 10.0


def test_get_quote_flat_price_control_ignores_metadata_and_uses_session_evidence():
    # Live-proven shape (KBANK.BK, 2026-08-18): the true previous session's
    # close (249.0) happens to equal an earlier, stale session's close too --
    # so a numeric-only assertion couldn't tell "correct by evidence" apart
    # from "correct by luck". meta.chartPreviousClose is deliberately
    # poisoned with an obviously wrong value (999.0) to prove get_quote() no
    # longer reads previous-close metadata fields at all -- only
    # timestamp-associated session evidence.
    closes = [249.0, 249.0, 248.0, 249.0, 247.0]  # sessions N-4 .. N; N-4 and N-1 both 249.0
    result = _make_raw_chart_result(
        "KBANK.BK",
        247.0,
        closes,
        meta_extra={
            "previousClose": None,
            "chartPreviousClose": 999.0,
            "regularMarketPreviousClose": None,
        },
    )
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("KBANK.BK")
    assert quote["current_price"] == 247.0
    assert quote["previous_close"] == 249.0


# ── Independent-review blockers (duplicate timestamp / trailing null) ──────────
#
# Two counterexamples an independent review raised against the first pass of
# this fix, both now handled by _dedup_sessions_by_timestamp() +
# _previous_close_from_observations() (see their docstrings for the exact
# algorithm): a repeated provider timestamp must count as one session, and
# the single most-recent distinct session is always excluded from
# "previous close" candidates -- whether or not that session's own close is
# populated -- because it is treated as belonging to the live quote.

def test_dedup_sessions_by_timestamp_keeps_last_duplicate():
    # Direct unit coverage of the duplicate-timestamp policy: mirrors
    # _chart_result_to_df's existing history dedup (sort, then keep the last
    # occurrence of a repeated timestamp).
    obs = (
        QuoteObservation(timestamp=100, close=10.0),
        QuoteObservation(timestamp=200, close=11.0),
        QuoteObservation(timestamp=200, close=12.0),
    )
    assert _dedup_sessions_by_timestamp(obs) == (
        QuoteObservation(timestamp=100, close=10.0),
        QuoteObservation(timestamp=200, close=12.0),
    )


def test_dedup_sessions_by_timestamp_last_by_appearance_not_input_order():
    # "Last" means last in provider-returned (appearance) order, not last
    # after the caller happens to list it -- shuffling which duplicate
    # appears first in the input tuple must not change the winner.
    obs = (
        QuoteObservation(timestamp=200, close=11.0),
        QuoteObservation(timestamp=100, close=10.0),
        QuoteObservation(timestamp=200, close=12.0),
    )
    assert _dedup_sessions_by_timestamp(obs) == (
        QuoteObservation(timestamp=100, close=10.0),
        QuoteObservation(timestamp=200, close=12.0),
    )


def test_previous_close_from_observations_duplicate_timestamp_blocker():
    # Independent-review Blocker 1 counterexample. Without deduplication,
    # sorting [10, 11, 12] at timestamps [100, 200, 200] and taking the
    # second-most-recent non-null close would wrongly return 11 (the earlier
    # of the two same-session observations at timestamp 200). This would
    # fail against the pre-correction implementation.
    obs = (
        QuoteObservation(timestamp=100, close=10.0),
        QuoteObservation(timestamp=200, close=11.0),
        QuoteObservation(timestamp=200, close=12.0),
    )
    assert _previous_close_from_observations(obs) == 10.0


def test_get_quote_deduplicates_repeated_timestamp_keeping_last_value():
    # End-to-end version of the duplicate-timestamp blocker through
    # get_quote(). Would fail (return 11.0) against the pre-correction
    # implementation, which sorted non-null closes and took the
    # second-to-last without collapsing the repeated timestamp first.
    result = _make_raw_chart_result("DUP.BK", 12.0, [10.0, 11.0, 12.0], timestamps=[100, 200, 200])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("DUP.BK")
    assert quote["current_price"] == 12.0
    assert quote["previous_close"] == 10.0


def test_previous_close_from_observations_trailing_null_blocker():
    # Independent-review Blocker 2 counterexample. The latest session (300)
    # has no completed close yet; the pre-correction implementation filtered
    # nulls out entirely and then took the second-to-last of what remained
    # (10, at timestamp 100) instead of the most recent *completed* session
    # (11, at timestamp 200).
    obs = (
        QuoteObservation(timestamp=100, close=10.0),
        QuoteObservation(timestamp=200, close=11.0),
        QuoteObservation(timestamp=300, close=None),
    )
    assert _previous_close_from_observations(obs) == 11.0


def test_get_quote_uses_last_completed_session_when_latest_bar_is_null():
    # End-to-end version of the trailing-null blocker through get_quote().
    # meta.regularMarketPrice (12.0, the live quote) is preserved as
    # current_price unchanged; previous_close must be the most recent
    # *completed* session (11.0), not two sessions back (10.0). Would fail
    # (return 10.0) against the pre-correction implementation.
    result = _make_raw_chart_result("TRAIL.BK", 12.0, [10.0, 11.0, None], timestamps=[100, 200, 300])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("TRAIL.BK")
    assert quote["current_price"] == 12.0
    assert quote["previous_close"] == 11.0


def test_get_quote_session_identity_not_confused_by_matching_price():
    # Equal-price ambiguity: meta.regularMarketPrice (10.0) numerically
    # matches an earlier session's close (N-2, also 10.0). Session identity
    # must come from timestamp order, not from searching for a close equal
    # to the current price -- the correct previous session is N-1 (20.0).
    result = _make_raw_chart_result("EQ.BK", 10.0, [10.0, 20.0, 10.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("EQ.BK")
    assert quote["current_price"] == 10.0
    assert quote["previous_close"] == 20.0


# ── BANPU-WP3 Stage 0 / Step 1.1 — PD-1 characterization (locked) ──────────────
#
# These fixtures and expected values reproduce, verbatim, the Stage 0 Step 0.3
# baseline capture (BANPU-WP3 Work Package Plan Sec 3.0.3). Every expected
# value below is a literal constant transcribed from that capture, never
# recomputed from production code. Construction mirrors the raw
# `chart.result[0]` shape `_fetch_chart_result` returns; patched in directly
# so these tests exercise exactly what Stage 0 characterized, independent of
# the `_session.get`/`_make_payload` HTTP-layer fixture machinery used
# elsewhere in this file. Scope: `get_quote()` only (yahoo_chart.py's own
# function) — `fetch_price_info()` lives in data_fetcher.py, which is outside
# WP3.1's authorized file surface.

def _make_raw_chart_result(
    symbol_meta,
    regular_market_price,
    closes,
    timestamps=None,
    include_meta=True,
    meta_extra=None,
):
    n = len(closes)
    if timestamps is None:
        base = 1_700_000_000
        timestamps = [base + i * 86400 for i in range(n)]
    result = {
        "timestamp": timestamps,
        "indicators": {
            "quote": [{
                "open": closes,
                "high": closes,
                "low": closes,
                "close": closes,
                "volume": [1000] * n,
            }],
        },
    }
    if include_meta:
        meta = {
            "symbol": symbol_meta,
            "regularMarketPrice": regular_market_price,
            "chartPreviousClose": closes[-2] if len(closes) >= 2 else None,
        }
        if meta_extra:
            meta.update(meta_extra)
        result["meta"] = meta
    return result


def _patched_fetch_chart_result(result_payload):
    return patch("services.market_data.yahoo_chart._fetch_chart_result", return_value=result_payload)


def test_characterization_f1_dense_matching_symbol():
    result = _make_raw_chart_result("F1SYM.BK", 105.5, [100.0, 102.0, 105.5])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F1SYM.BK")
    assert quote["current_price"] == 105.5
    assert quote["previous_close"] == 102.0


def test_characterization_f2_sparse_latest_bar_absent():
    # Timestamp-associated derivation (shared with get_quote_evidence()):
    # the null bar at index 1 is skipped, and the true previous non-null
    # session (95.0) is used -- get_quote() no longer returns None here.
    result = _make_raw_chart_result("F2SYM.BK", 100.0, [95.0, None, 100.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F2SYM.BK")
    assert quote["current_price"] == 100.0
    assert quote["previous_close"] == 95.0


def test_characterization_f3_meta_symbol_mismatch():
    # Current code performs no comparison of requested vs. served symbol.
    result = _make_raw_chart_result("OTHER.BK", 50.0, [48.0, 49.0, 50.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F3SYM.BK")
    assert quote["current_price"] == 50.0
    assert quote["previous_close"] == 49.0


def test_characterization_f4a_meta_absent():
    # current_price still depends on meta.regularMarketPrice and stays None
    # when meta is absent. previous_close no longer does -- it comes from the
    # observations array (timestamp-associated derivation), independent of
    # whether meta is present at all.
    result = _make_raw_chart_result(None, None, [10.0, 11.0, 12.0], include_meta=False)
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F4SYM.BK")
    assert quote["current_price"] is None
    assert quote["previous_close"] == 11.0


def test_characterization_f4b_meta_incomplete():
    result = _make_raw_chart_result("F4SYM.BK", None, [10.0, 11.0, 12.0])
    del result["meta"]["regularMarketPrice"]
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F4SYM.BK")
    assert quote["current_price"] is None
    assert quote["previous_close"] == 11.0


def test_characterization_f5_null_at_closes_minus_2():
    # Same shape as F2: the null bar is skipped by timestamp, landing on the
    # true previous non-null session (55.0) instead of None.
    result = _make_raw_chart_result("F5SYM.BK", 58.0, [55.0, None, 58.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F5SYM.BK")
    assert quote["current_price"] == 58.0
    assert quote["previous_close"] == 55.0


# 2023-11-14T17:00:00Z == 2023-11-15T00:00:00+07:00 -- an exact UTC+7
# exchange-local midnight boundary, independently verified via zoneinfo
# (Asia/Bangkok) rather than assumed.
_UTC7_MIDNIGHT_BOUNDARY_TS = 1699981200


def test_characterization_f6_utc7_boundary_both_edges_identical():
    # Identical closes, timestamps straddling the exact UTC+7 midnight
    # boundary from both sides: get_quote() derives previous_close from
    # session *order* (sorted timestamps), not from any absolute calendar
    # boundary, so shifting every timestamp by the same offset across this
    # boundary must produce identical output.
    edge_before = [
        _UTC7_MIDNIGHT_BOUNDARY_TS - 3600,
        _UTC7_MIDNIGHT_BOUNDARY_TS - 1,
        _UTC7_MIDNIGHT_BOUNDARY_TS,
    ]
    edge_after = [
        _UTC7_MIDNIGHT_BOUNDARY_TS,
        _UTC7_MIDNIGHT_BOUNDARY_TS + 1,
        _UTC7_MIDNIGHT_BOUNDARY_TS + 3600,
    ]
    result_before = _make_raw_chart_result("F6SYM.BK", 72.0, [70.0, 71.0, 72.0], timestamps=edge_before)
    result_after = _make_raw_chart_result("F6SYM.BK", 72.0, [70.0, 71.0, 72.0], timestamps=edge_after)

    with _patched_fetch_chart_result(result_before):
        quote_before = YahooChartProvider().get_quote("F6SYM.BK")
    with _patched_fetch_chart_result(result_after):
        quote_after = YahooChartProvider().get_quote("F6SYM.BK")

    assert quote_before["current_price"] == 72.0
    assert quote_before["previous_close"] == 71.0
    assert quote_after["current_price"] == quote_before["current_price"]
    assert quote_after["previous_close"] == quote_before["previous_close"]


def test_characterization_f6_non_boundary_timestamps_same_output():
    # Non-triggering companion (Step 1.4): timestamps far from any day
    # boundary must produce the same values too.
    midday = [1_700_000_000, 1_700_000_000 + 43200, 1_700_000_000 + 86400]
    result = _make_raw_chart_result("F6SYM.BK", 72.0, [70.0, 71.0, 72.0], timestamps=midday)
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F6SYM.BK")
    assert quote["current_price"] == 72.0
    assert quote["previous_close"] == 71.0


def test_characterization_f7_dr_symbol_no_normalization():
    # get_quote() performs zero DR normalization; the raw requested symbol is
    # what gets sent, and whatever meta.symbol comes back is used as-is.
    result = _make_raw_chart_result("NVDA01", 135.0, [130.0, 132.0, 135.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("NVDA01")
    assert quote["current_price"] == 135.0
    assert quote["previous_close"] == 132.0


def test_characterization_f7_non_dr_symbol_unaffected():
    # Non-triggering companion (Step 1.4): an ordinary (non-DR) symbol
    # behaves identically.
    result = _make_raw_chart_result("PTT.BK", 40.0, [38.0, 39.0, 40.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("PTT.BK")
    assert quote["current_price"] == 40.0
    assert quote["previous_close"] == 39.0


def test_get_quote_shape_unchanged():
    result = _make_raw_chart_result("SHAPE.BK", 10.0, [9.0, 10.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("SHAPE.BK")
    assert set(quote.keys()) == {"current_price", "previous_close", "last_updated"}


# ── BANPU-WP3.1 Steps 1.2-1.3 — provider evidence extraction (E1-E5) ───────────

def test_evidence_e1_provider_identity_constant():
    result = _make_raw_chart_result("ANY.BK", 10.0, [9.0, 10.0])
    evidence = _extract_provider_evidence(result, requested_symbol="ANY.BK")
    assert evidence.provider == "yahoo_chart"


def test_evidence_e2_served_symbol_matching():
    result = _make_raw_chart_result("MATCH.BK", 10.0, [9.0, 10.0])
    evidence = _extract_provider_evidence(result, requested_symbol="MATCH.BK")
    assert evidence.served_symbol == "MATCH.BK"
    assert evidence.requested_symbol == "MATCH.BK"


def test_evidence_e2_served_symbol_mismatched_carried_without_comparison():
    # The structure carries the raw fact only -- no rejection, no flag, no
    # comparison logic of any kind (that is WP3.2's job).
    result = _make_raw_chart_result("OTHER.BK", 10.0, [9.0, 10.0])
    evidence = _extract_provider_evidence(result, requested_symbol="REQUESTED.BK")
    assert evidence.served_symbol == "OTHER.BK"
    assert evidence.requested_symbol == "REQUESTED.BK"


def test_evidence_e2_served_symbol_missing_metadata():
    result = _make_raw_chart_result(None, None, [9.0, 10.0], include_meta=False)
    evidence = _extract_provider_evidence(result, requested_symbol="ANY.BK")
    assert evidence.served_symbol is None


def test_evidence_e3_observations_pair_timestamps_with_closes():
    ts = [111, 222, 333]
    closes = [1.0, None, 3.0]
    result = _make_raw_chart_result("E3.BK", 3.0, closes, timestamps=ts)
    evidence = _extract_provider_evidence(result, requested_symbol="E3.BK")
    assert evidence.observations == (
        QuoteObservation(timestamp=111, close=1.0),
        QuoteObservation(timestamp=222, close=None),
        QuoteObservation(timestamp=333, close=3.0),
    )


def test_evidence_e4_previous_close_timestamp_associated_on_sparse_fixture():
    # Same F2 fixture as the locked characterization test above. get_quote()
    # reuses this same E4 derivation, so both correctly skip the null bar and
    # find 95.0 (see test_get_quote_and_get_quote_evidence_agree_on_previous_close).
    result = _make_raw_chart_result("F2SYM.BK", 100.0, [95.0, None, 100.0])
    evidence = _extract_provider_evidence(result, requested_symbol="F2SYM.BK")
    assert evidence.current_close == 100.0
    assert evidence.previous_close == 95.0


def test_evidence_e4_dense_series_matches_positional_result():
    # When there is no sparseness, the corrected derivation agrees with the
    # existing positional one -- they only diverge in the sparse case.
    result = _make_raw_chart_result("F1SYM.BK", 105.5, [100.0, 102.0, 105.5])
    evidence = _extract_provider_evidence(result, requested_symbol="F1SYM.BK")
    assert evidence.current_close == 105.5
    assert evidence.previous_close == 102.0


def test_evidence_e4_previous_close_deduplicates_repeated_timestamp():
    # Same duplicate-timestamp blocker as test_get_quote_deduplicates_..., at
    # the evidence-structure level: get_quote() and get_quote_evidence()
    # share this derivation, so both must be fixed together.
    result = _make_raw_chart_result("DUP.BK", 12.0, [10.0, 11.0, 12.0], timestamps=[100, 200, 200])
    evidence = _extract_provider_evidence(result, requested_symbol="DUP.BK")
    assert evidence.previous_close == 10.0


def test_evidence_e5_exchange_timezone_present():
    result = _make_raw_chart_result(
        "E5.BK", 10.0, [9.0, 10.0], meta_extra={"exchangeTimezoneName": "Asia/Bangkok"}
    )
    evidence = _extract_provider_evidence(result, requested_symbol="E5.BK")
    assert evidence.exchange_timezone_name == "Asia/Bangkok"


def test_evidence_e5_exchange_timezone_missing():
    result = _make_raw_chart_result("E5.BK", 10.0, [9.0, 10.0])
    evidence = _extract_provider_evidence(result, requested_symbol="E5.BK")
    assert evidence.exchange_timezone_name is None


def test_evidence_e5_is_sufficient_basis_for_exchange_local_date_derivation():
    # E5's purpose (PD-2): "a deterministic basis for mapping observation
    # timestamps to exchange-local calendar dates". WP3.1 supplies the raw
    # ingredients (exchange_timezone_name + per-observation timestamps) only
    # -- actual epoch classification is WP3.2's (Architecture and
    # Implementation Plan Sec 5.4 layering). This test proves, using only
    # what the evidence structure exposes, that a deterministic exchange-
    # local calendar date CAN be derived -- entirely test-side, nothing
    # produced here is added to yahoo_chart.py.
    from zoneinfo import ZoneInfo
    from datetime import datetime as _dt, timezone as _tz

    edge_before_ts = _UTC7_MIDNIGHT_BOUNDARY_TS - 1  # 2023-11-14T23:59:59+07:00
    edge_after_ts = _UTC7_MIDNIGHT_BOUNDARY_TS        # 2023-11-15T00:00:00+07:00

    result = _make_raw_chart_result(
        "F6SYM.BK", 72.0, [70.0, 71.0],
        timestamps=[edge_before_ts, edge_after_ts],
        meta_extra={"exchangeTimezoneName": "Asia/Bangkok"},
    )
    evidence = _extract_provider_evidence(result, requested_symbol="F6SYM.BK")
    tz = ZoneInfo(evidence.exchange_timezone_name)

    local_dates = [
        _dt.fromtimestamp(obs.timestamp, tz=_tz.utc).astimezone(tz).date()
        for obs in evidence.observations
    ]
    assert local_dates[0] != local_dates[1]  # the two observations fall on different exchange-local days
    assert str(local_dates[0]) == "2023-11-14"
    assert str(local_dates[1]) == "2023-11-15"  # deterministic, reproducible from the raw evidence alone


def test_evidence_structure_is_immutable():
    result = _make_raw_chart_result("IMM.BK", 10.0, [9.0, 10.0])
    evidence = _extract_provider_evidence(result, requested_symbol="IMM.BK")
    with pytest.raises(FrozenInstanceError):
        evidence.provider = "tampered"
    obs = evidence.observations[0]
    with pytest.raises(FrozenInstanceError):
        obs.close = 999.0


def test_evidence_structure_carries_no_comparison_or_quarantine_fields():
    # Structural guarantee: the dataclass exposes exactly the E1-E5 fields,
    # nothing resembling a comparison/binding/quarantine decision.
    field_names = set(ProviderQuoteEvidence.__dataclass_fields__.keys())
    assert field_names == {
        "provider", "requested_symbol", "served_symbol", "observations",
        "current_close", "previous_close", "exchange_timezone_name",
    }


def test_evidence_dr_symbol_carried_without_normalization():
    result = _make_raw_chart_result("NVDA01", 135.0, [130.0, 132.0, 135.0])
    evidence = _extract_provider_evidence(result, requested_symbol="NVDA01")
    assert evidence.served_symbol == "NVDA01"
    assert evidence.requested_symbol == "NVDA01"


# ── get_quote_evidence(): single-response derivation, unreachable/uncalled ────

def test_get_quote_evidence_single_fetch_call():
    result = _make_raw_chart_result("SINGLE.BK", 20.0, [19.0, 20.0])
    with patch(
        "services.market_data.yahoo_chart._fetch_chart_result", return_value=result
    ) as mock_fetch:
        evidence = YahooChartProvider().get_quote_evidence("SINGLE.BK")
    mock_fetch.assert_called_once_with("SINGLE.BK", range_="5d", interval="1d")
    assert evidence.current_close == 20.0
    assert evidence.previous_close == 19.0


def test_get_quote_evidence_returns_none_on_fetch_failure():
    with patch("services.market_data.yahoo_chart._fetch_chart_result", return_value=None):
        evidence = YahooChartProvider().get_quote_evidence("NOTASYMBOL.XX")
    assert evidence is None


def test_get_quote_and_get_quote_evidence_agree_on_previous_close():
    # get_quote() and get_quote_evidence() must not disagree about what
    # "previous close" means -- both derive it from the same
    # timestamp-associated, skip-null logic against the same fixture.
    result = _make_raw_chart_result("F2SYM.BK", 100.0, [95.0, None, 100.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F2SYM.BK")
        evidence = YahooChartProvider().get_quote_evidence("F2SYM.BK")
    assert quote["previous_close"] == 95.0
    assert evidence.previous_close == 95.0
    assert quote["previous_close"] == evidence.previous_close


def test_module_never_imports_position_conversion_types():
    # Provider-neutrality structural guard: yahoo_chart.py must stay
    # conversion-unaware and must not couple to the WP1 payload contract or
    # to the data_fetcher.py cache/fetch layer that WP3.3 owns. Checked via
    # AST (actual imports and code-level references only) so this doesn't
    # false-positive on prose in comments/docstrings explaining the
    # constraint itself.
    import ast
    import services.market_data.yahoo_chart as _mod

    source = Path(_mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)

    forbidden_modules = ("transaction_canonicalizer", "services.data_fetcher", "data_fetcher")
    forbidden_names = {
        "PositionConversion",
        "PositionConversionQuoteBinding",
        "PositionConversionSuccessor",
        "PositionConversionDates",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not any(f in alias.name for f in forbidden_modules), f"forbidden import: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            assert not any(f in mod for f in forbidden_modules), f"forbidden import: {mod}"
        elif isinstance(node, ast.Name):
            assert node.id not in forbidden_names, f"forbidden reference: {node.id}"
        elif isinstance(node, ast.Attribute):
            assert node.attr not in forbidden_names, f"forbidden reference: {node.attr}"


# ── get_history_batch ────────────────────────────────────────────────────────────

def test_get_history_batch_returns_all_successful_symbols():
    payload = _make_payload(_BASE_TS, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, _BASE_CLOSES, [1000] * 5)

    def _get(url, params=None, timeout=None):
        if "BADSYM" in url:
            return _MockResponse(200, _error_payload())
        return _MockResponse(200, payload)

    with patch("services.market_data.yahoo_chart._session.get", side_effect=_get):
        result = YahooChartProvider().get_history_batch(
            ["AAPL", "GULF.BK", "BADSYM.BK"], period="1mo", interval="1d"
        )

    assert set(result.keys()) == {"AAPL", "GULF.BK"}
    for df in result.values():
        assert df.index.is_monotonic_increasing


def test_get_history_batch_empty_symbol_list():
    assert YahooChartProvider().get_history_batch([], period="1mo", interval="1d") == {}


# ── get_fundamentals / get_news delegate to legacy provider ─────────────────────

def test_get_fundamentals_delegates_to_legacy_provider():
    with patch.object(YahooProvider, "get_fundamentals", return_value={"sector": "Energy"}) as mock_fund:
        info = YahooChartProvider().get_fundamentals("PTT.BK")
    mock_fund.assert_called_once_with("PTT.BK")
    assert info == {"sector": "Energy"}


def test_get_news_delegates_to_legacy_provider():
    with patch.object(YahooProvider, "get_news", return_value=[{"title": "x"}]) as mock_news:
        news = YahooChartProvider().get_news("PTT.BK")
    mock_news.assert_called_once_with("PTT.BK")
    assert news == [{"title": "x"}]


# ── Provider factory ─────────────────────────────────────────────────────────────

def test_factory_defaults_to_yahoo_chart_provider(monkeypatch):
    monkeypatch.delenv("PRICE_PROVIDER", raising=False)
    assert isinstance(get_provider(), YahooChartProvider)


def test_factory_yahoo_explicit(monkeypatch):
    monkeypatch.setenv("PRICE_PROVIDER", "yahoo")
    assert isinstance(get_provider(), YahooChartProvider)


def test_factory_yfinance_rollback(monkeypatch):
    monkeypatch.setenv("PRICE_PROVIDER", "yfinance")
    assert isinstance(get_provider(), YahooProvider)


def test_factory_explicit_name_overrides_env(monkeypatch):
    monkeypatch.setenv("PRICE_PROVIDER", "yfinance")
    assert isinstance(get_provider("yahoo"), YahooChartProvider)


def test_factory_unknown_value_falls_back_to_default(monkeypatch):
    monkeypatch.setenv("PRICE_PROVIDER", "bogus")
    assert isinstance(get_provider(), YahooChartProvider)


# ── Live smoke tests (network, opt-in only) ──────────────────────────────────────

_RUN_LIVE = os.environ.get("RUN_LIVE_MARKET_TESTS") == "1"

_US_SYMBOLS = ["AAPL", "MSFT", "NVDA"]
_TH_SYMBOLS = ["SCB.BK", "KBANK.BK", "PTT.BK", "ADVANC.BK", "GULF.BK"]
_PERIODS = ["1mo", "3mo", "1y", "5y"]


@pytest.mark.skipif(not _RUN_LIVE, reason="set RUN_LIVE_MARKET_TESTS=1 to hit the real Yahoo Finance API")
@pytest.mark.parametrize("symbol", _US_SYMBOLS + _TH_SYMBOLS)
@pytest.mark.parametrize("period", _PERIODS)
def test_live_get_history(symbol, period):
    df = YahooChartProvider().get_history(symbol, period=period, interval="1d")
    assert df is not None, f"no data returned for {symbol} {period}"
    assert not df.empty
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        assert col in df.columns
    assert df.index.is_monotonic_increasing
    assert not df.index.duplicated().any()
    assert str(df.index.tz) == "UTC"
