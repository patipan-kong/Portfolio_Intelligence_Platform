"""Regression test for DOGFOOD-05.

regime_detector._fetch_benchmark_history used to call yfinance's
Ticker.history(), whose internal parser was observed to crash the whole
backend process (native access violation / STATUS_ACCESS_VIOLATION, no
Python traceback, no way for any try/except to catch it) when Yahoo returns
a degraded single-datapoint chart response — reproduced deterministically
for the "^SET.BK" benchmark symbol used by the regime detector.

The fetch now goes through `requests` directly with manual JSON parsing,
which never touches the crashing code path. These tests assert that
contract and that the same response shapes are handled exactly as before.
"""
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.analytics import regime_detector


# Real payload captured from Yahoo's chart API for "^SET.BK" — a single data
# point despite a 6-month range request. This is exactly the response shape
# that crashed yfinance's history parser in DOGFOOD-05.
_DEGRADED_SINGLE_POINT_RESPONSE = {
    "chart": {
        "result": [{
            "meta": {"symbol": "^SET.BK"},
            "timestamp": [1789530786],
            "indicators": {
                "quote": [{"close": [1576.260009765625]}],
            },
        }],
        "error": None,
    }
}

_NORMAL_MULTI_ROW_RESPONSE = {
    "chart": {
        "result": [{
            "meta": {"symbol": "^GSPC"},
            "timestamp": [1700000000, 1700086400, 1700172800],
            "indicators": {
                "quote": [{"close": [100.0, 101.5, None]}],
            },
        }],
        "error": None,
    }
}


def _mock_response(payload):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = payload
    resp.raise_for_status.return_value = None
    return resp


def test_fetch_benchmark_history_uses_requests_not_yfinance():
    """Must go through `requests`, never yfinance.Ticker — that internal
    parser is what segfaulted the server in DOGFOOD-05."""
    with patch("requests.get", return_value=_mock_response(_DEGRADED_SINGLE_POINT_RESPONSE)) as mock_get, \
         patch("services.core.runtime_env.allow_market_fetching", return_value=True):
        regime_detector._fetch_benchmark_history("^SET.BK", days=95)

    assert mock_get.called, "expected the fetch to go through requests.get"
    called_url = mock_get.call_args.args[0] if mock_get.call_args.args else mock_get.call_args.kwargs.get("url")
    assert "query2.finance.yahoo.com" in called_url


def test_fetch_benchmark_history_handles_degraded_single_point_response():
    """The real ^SET.BK payload that crashed the process must degrade
    gracefully to a valid 1-row DataFrame, not raise or crash."""
    with patch("requests.get", return_value=_mock_response(_DEGRADED_SINGLE_POINT_RESPONSE)), \
         patch("services.core.runtime_env.allow_market_fetching", return_value=True):
        df = regime_detector._fetch_benchmark_history("^SET.BK", days=95)

    assert len(df) == 1
    assert "Close" in df.columns
    assert round(float(df["Close"].iloc[0]), 2) == 1576.26


def test_fetch_benchmark_history_parses_normal_multi_row_response():
    with patch("requests.get", return_value=_mock_response(_NORMAL_MULTI_ROW_RESPONSE)), \
         patch("services.core.runtime_env.allow_market_fetching", return_value=True):
        df = regime_detector._fetch_benchmark_history("^GSPC", days=95)

    # the None close is dropped; index must be sorted ascending and tz-naive
    assert len(df) == 2
    assert df.index.tz is None
    assert list(df["Close"]) == [100.0, 101.5]


def test_fetch_benchmark_history_returns_empty_on_malformed_response():
    malformed = {"chart": {"result": [{
        "timestamp": [1, 2],
        "indicators": {"quote": [{"close": [1.0]}]},  # length mismatch
    }]}}
    with patch("requests.get", return_value=_mock_response(malformed)), \
         patch("services.core.runtime_env.allow_market_fetching", return_value=True):
        df = regime_detector._fetch_benchmark_history("^BAD", days=95)

    assert df.empty


def test_fetch_benchmark_history_blocked_on_vps():
    with patch("services.core.runtime_env.allow_market_fetching", return_value=False), \
         patch("requests.get") as mock_get:
        df = regime_detector._fetch_benchmark_history("^GSPC", days=95)

    assert df.empty
    assert not mock_get.called
