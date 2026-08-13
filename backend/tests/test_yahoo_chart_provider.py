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
    _extract_provider_evidence,
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


def test_get_quote_uses_provider_previous_close_when_latest_chart_bar_is_sparse():
    result = _make_raw_chart_result(
        "KBANK.BK",
        248.0,
        [250.0, 248.0, 249.0, None, 248.0],
        meta_extra={"previousClose": None, "chartPreviousClose": 250.0},
    )
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("KBANK.BK")

    assert quote["current_price"] == 248.0
    assert quote["previous_close"] == 250.0


def test_get_quote_failure_returns_none_fields():
    with _patched_get() as mock_get:
        mock_get.return_value = _MockResponse(404, None)
        quote = YahooChartProvider().get_quote("NOTASYMBOL.XX")
    assert quote == {"current_price": None, "previous_close": None, "last_updated": None}


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
    # The provider metadata is absent here, so the legacy quote path must not
    # synthesize a previous close from the sparse chart bars.
    result = _make_raw_chart_result("F2SYM.BK", 100.0, [95.0, None, 100.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F2SYM.BK")
    assert quote["current_price"] == 100.0
    assert quote["previous_close"] is None


def test_characterization_f3_meta_symbol_mismatch():
    # Current code performs no comparison of requested vs. served symbol.
    result = _make_raw_chart_result("OTHER.BK", 50.0, [48.0, 49.0, 50.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F3SYM.BK")
    assert quote["current_price"] == 50.0
    assert quote["previous_close"] == 49.0


def test_characterization_f4a_meta_absent():
    result = _make_raw_chart_result(None, None, [10.0, 11.0, 12.0], include_meta=False)
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F4SYM.BK")
    assert quote["current_price"] is None
    assert quote["previous_close"] is None


def test_characterization_f4b_meta_incomplete():
    result = _make_raw_chart_result("F4SYM.BK", None, [10.0, 11.0, 12.0])
    del result["meta"]["regularMarketPrice"]
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F4SYM.BK")
    assert quote["current_price"] is None
    assert quote["previous_close"] == 11.0


def test_characterization_f5_null_at_closes_minus_2():
    result = _make_raw_chart_result("F5SYM.BK", 58.0, [55.0, None, 58.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F5SYM.BK")
    assert quote["current_price"] == 58.0
    assert quote["previous_close"] is None


# 2023-11-14T17:00:00Z == 2023-11-15T00:00:00+07:00 -- an exact UTC+7
# exchange-local midnight boundary, independently verified via zoneinfo
# (Asia/Bangkok) rather than assumed.
_UTC7_MIDNIGHT_BOUNDARY_TS = 1699981200


def test_characterization_f6_utc7_boundary_both_edges_identical():
    # Identical closes, timestamps straddling the exact UTC+7 midnight
    # boundary from both sides: current (pre-WP3) get_quote() never reads
    # `timestamp`, so both edges must produce identical output.
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
    # returns previous_close=None (positional); this evidence structure's E4
    # derivation correctly skips the null bar and finds 95.0.
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


def test_get_quote_evidence_sparse_bar_is_separate_from_metadata_quote_path():
    # Both paths are tested independently against the SAME fixture: the
    # evidence method returns the corrected, timestamp-associated value while
    # the legacy quote path remains metadata-driven and has no metadata here.
    result = _make_raw_chart_result("F2SYM.BK", 100.0, [95.0, None, 100.0])
    with _patched_fetch_chart_result(result):
        quote = YahooChartProvider().get_quote("F2SYM.BK")
        evidence = YahooChartProvider().get_quote_evidence("F2SYM.BK")
    assert quote["previous_close"] is None
    assert evidence.previous_close == 95.0


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
