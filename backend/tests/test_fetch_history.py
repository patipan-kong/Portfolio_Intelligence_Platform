"""BANPU-WP3.4 Step 4.3 — real regression evidence for fetch_history()'s
unbound/legacy path.

Replaces the prior 325-byte live print script (network call to
GOOGL01.BK via yfinance, no assertions, no test functions) that
docs/implementation/BANPU_WP3_WORK_PACKAGE_PLAN.md §3.4 risk R6 names as a
recorded residual: "reliance on test_fetch_history.py, which is a 325-byte
live print script with no test functions." This file supplies the missing
pytest evidence; per the Work Package Plan, R6 itself remains recorded, not
resolved, and the roadmap text is not amended here.

No network call, no real database. The unbound/unconverted path is this
file's whole scope: with no binding and an empty canonical conversion guard
projection, fetch_history() must behave exactly as it did before BANPU-WP3 —
same cache_type, same cache-hit/cache-miss/stale-fallback behavior, same
DataFrame values. The bound/converted path is WP3.3's territory and is
already covered exhaustively by test_quote_epoch_isolation.py; it is
deliberately not duplicated here.
"""
import pandas as pd
import pytest

import services.data_fetcher as fetcher


class _Provider:
    def __init__(self, history: "pd.DataFrame | None" = None, error: Exception | None = None):
        self.history = history
        self.error = error
        self.history_calls = 0

    def get_history(self, _symbol, _period="6mo", _interval="1d"):
        self.history_calls += 1
        if self.error is not None:
            raise self.error
        return self.history


def _empty_projection() -> fetcher._ConversionGuardProjection:
    return fetcher._ConversionGuardProjection(
        available=True,
        bindings_by_symbol=(),
        ambiguous_symbols=frozenset(),
    )


@pytest.fixture(autouse=True)
def _unbound_guard(monkeypatch):
    """Every test in this file exercises the unconverted/unbound path only."""
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", _empty_projection)


def test_fetch_history_unbound_legacy_values_and_cache_type_unchanged(monkeypatch):
    df = pd.DataFrame(
        {"Close": [35.0, 35.5, 36.25]},
        index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"], utc=True),
    )
    provider = _Provider(history=df)
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: True)
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    writes = []
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: writes.append(args))

    result = fetcher.fetch_history("PTT.BK", "5y", "1d")

    assert result is not None
    assert result["Close"].tolist() == [35.0, 35.5, 36.25]
    assert provider.history_calls == 1
    # Unbound history keeps the plain "history:{period}:{interval}" namespace,
    # never an asset/epoch-namespaced one.
    assert writes[0][0:2] == ("PTT.BK", "history:5y:1d")


def test_fetch_history_unbound_cache_hit_skips_provider(monkeypatch):
    df = pd.DataFrame({"Close": [10.0]}, index=pd.to_datetime(["2024-01-02"], utc=True))
    provider = _Provider(history=df)
    cached_payload = fetcher._df_to_payload(df)
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: cached_payload)

    result = fetcher.fetch_history("PTT.BK", "1mo", "1d")

    assert result is not None
    assert result["Close"].tolist() == [10.0]
    assert provider.history_calls == 0


def test_fetch_history_unbound_falls_back_to_stale_cache_when_fetching_blocked(monkeypatch):
    provider = _Provider(history=pd.DataFrame({"Close": [1.0]}))
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: False)
    stale_df = pd.DataFrame({"Close": [42.0]}, index=pd.to_datetime(["2023-12-01"], utc=True))
    monkeypatch.setattr(fetcher, "_get_stale", lambda *_: fetcher._df_to_payload(stale_df))

    result = fetcher.fetch_history("PTT.BK", "6mo", "1d")

    assert result is not None
    assert result["Close"].tolist() == [42.0]
    assert provider.history_calls == 0


def test_fetch_history_unbound_provider_error_without_stale_returns_none(monkeypatch):
    provider = _Provider(error=RuntimeError("network unavailable"))
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: True)
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_get_stale", lambda *_: None)

    result = fetcher.fetch_history("PTT.BK", "6mo", "1d")

    assert result is None
    assert provider.history_calls == 1


def test_fetch_history_unbound_provider_error_falls_back_to_stale(monkeypatch):
    provider = _Provider(error=RuntimeError("network unavailable"))
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: True)
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    stale_df = pd.DataFrame({"Close": [7.5]}, index=pd.to_datetime(["2023-11-30"], utc=True))
    monkeypatch.setattr(fetcher, "_get_stale", lambda *_: fetcher._df_to_payload(stale_df))

    result = fetcher.fetch_history("PTT.BK", "6mo", "1d")

    assert result is not None
    assert result["Close"].tolist() == [7.5]


def test_fetch_history_dr_symbol_unbound_shape_matches_retired_print_script_scenario(monkeypatch):
    """Same symbol/period/interval the retired print script exercised
    (GOOGL01.BK, "5y", "1d") — now asserted rather than eyeballed."""
    df = pd.DataFrame(
        {
            "Open":   [100.0, 101.0],
            "High":   [102.0, 103.0],
            "Low":    [99.0, 100.5],
            "Close":  [101.0, 102.5],
            "Volume": [1000, 1500],
        },
        index=pd.to_datetime(["2024-06-01", "2024-06-02"], utc=True),
    )
    provider = _Provider(history=df)
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: True)
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: None)

    result = fetcher.fetch_history("GOOGL01.BK", "5y", "1d")

    assert result is not None
    assert result.shape == (2, 5)
    assert list(result.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert result["Close"].iloc[-1] == 102.5
