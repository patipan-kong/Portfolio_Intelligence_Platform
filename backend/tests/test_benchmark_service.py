"""Regression coverage for the benchmark ingestion crash/stale-ingestion bug.

Root cause: benchmark_service._fetch_close_on_date() used to call
yf.Ticker(symbol).history(...) directly. On this Windows + Python 3.13 stack,
yfinance's curl_cffi-based impersonation layer crashes the whole interpreter
with a native access violation (0xC0000005) whenever it receives a non-empty
response — reproduced live for both "^SET.BK" and "QQQ". Because the crash is
native, no try/except can catch it, so the scheduler job's benchmark-fetch
step (the last step of snapshot_scheduler._run_snapshots_core, run AFTER
portfolio snapshots are already written and committed) took the entire
backend process down before benchmark_prices rows for the day were ever
persisted. That produced the observed symptom: portfolio snapshots kept
advancing daily while benchmark_prices silently stopped gaining new rows
(^SET.BK last row 2026-08-21, QQQ last row 2026-08-20, while snapshots
continued through 2026-08-24).

The fix routes _fetch_close_on_date() through the already-existing crash-safe
YahooChartProvider (see yahoo_chart.py's module docstring for the original
diagnosis of this exact crash class) instead of raw yfinance. These tests
exercise the resulting "on or before price_date" selection logic with a
stubbed provider — no network, no real DB (in-memory SQLite for the
persistence test).
"""
from __future__ import annotations

import asyncio

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401 -- registers the assets/* tables on Base.metadata
import services.benchmark_service as benchmark_service
from models.database import Base, BenchmarkPrice
from services.benchmark_service import _fetch_close_on_date, fetch_and_store_benchmarks


# ── Fixtures ──────────────────────────────────────────────────────────────────

def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)()


class _StubProvider:
    """Minimal stand-in for MarketDataProvider.get_history()."""

    def __init__(self, history: "pd.DataFrame | None" = None, error: Exception | None = None):
        self.history = history
        self.error = error
        self.calls: list[tuple[str, str, str]] = []

    def get_history(self, symbol, period="6mo", interval="1d"):
        self.calls.append((symbol, period, interval))
        if self.error is not None:
            raise self.error
        return self.history


def _bars(dates: list[str], closes: list[float]) -> pd.DataFrame:
    return pd.DataFrame({"Close": closes}, index=pd.to_datetime(dates, utc=True))


@pytest.fixture(autouse=True)
def _local_env(monkeypatch):
    monkeypatch.setattr(benchmark_service, "allow_market_fetching", lambda: True)


# ── _fetch_close_on_date: no longer touches yfinance ──────────────────────────

def test_benchmark_service_no_longer_imports_yfinance():
    """Structural regression guard for the actual root cause: the module must
    not hold a reference to the raw yfinance library, since that is the
    library whose curl_cffi layer crashes the interpreter."""
    assert not hasattr(benchmark_service, "yf")


def test_fetch_close_on_date_uses_configured_provider(monkeypatch):
    stub = _StubProvider(history=_bars(["2026-08-21"], [1619.37]))
    monkeypatch.setattr(benchmark_service, "get_provider", lambda: stub)

    result = _fetch_close_on_date("^SET.BK", "2026-08-21")

    assert result == pytest.approx(1619.37)
    assert stub.calls == [("^SET.BK", "1mo", "1d")]


# ── on-or-before / LOCF-at-the-source selection ────────────────────────────────

def test_fetch_close_on_date_reproduces_aug24_gap_by_carrying_last_close(monkeypatch):
    """Direct reproduction of the observed symptom: benchmark_prices has no
    row for 2026-08-24 (a trading day) because the old crash killed that
    day's fetch. With the fix, a provider that HAS a fresh bar for 08-24
    returns it; this test locks in that the "on or before" selection returns
    the most recent bar not later than price_date."""
    stub = _StubProvider(history=_bars(
        ["2026-08-19", "2026-08-20", "2026-08-21", "2026-08-24"],
        [1612.86, 1620.22, 1619.37, 1601.05],
    ))
    monkeypatch.setattr(benchmark_service, "get_provider", lambda: stub)

    assert _fetch_close_on_date("^SET.BK", "2026-08-21") == pytest.approx(1619.37)
    assert _fetch_close_on_date("^SET.BK", "2026-08-24") == pytest.approx(1601.05)


def test_fetch_close_on_date_falls_back_to_prior_session_over_weekend(monkeypatch):
    """price_date lands on a weekend/holiday gap with no bar of its own —
    the last available session's close is used (mirrors the old 6-day
    lookback window's intent, preserving LOCF-friendly behavior upstream)."""
    stub = _StubProvider(history=_bars(
        ["2026-08-20", "2026-08-21"], [710.93, 713.44],
    ))
    monkeypatch.setattr(benchmark_service, "get_provider", lambda: stub)

    # Saturday — no bar published; nearest prior session (Fri 08-21) wins.
    assert _fetch_close_on_date("QQQ", "2026-08-22") == pytest.approx(713.44)


def test_fetch_close_on_date_excludes_bars_after_price_date(monkeypatch):
    stub = _StubProvider(history=_bars(
        ["2026-08-17", "2026-08-24"], [105.0, 999.0],
    ))
    monkeypatch.setattr(benchmark_service, "get_provider", lambda: stub)

    result = _fetch_close_on_date("QQQ", "2026-08-18")

    assert result == pytest.approx(105.0)


# ── failure modes remain non-fatal ────────────────────────────────────────────

def test_fetch_close_on_date_returns_none_on_empty_history(monkeypatch):
    stub = _StubProvider(history=pd.DataFrame({"Close": []}, index=pd.DatetimeIndex([])))
    monkeypatch.setattr(benchmark_service, "get_provider", lambda: stub)

    assert _fetch_close_on_date("^SET.BK", "2026-08-24") is None


def test_fetch_close_on_date_returns_none_when_provider_returns_none(monkeypatch):
    stub = _StubProvider(history=None)
    monkeypatch.setattr(benchmark_service, "get_provider", lambda: stub)

    assert _fetch_close_on_date("^SET.BK", "2026-08-24") is None


def test_fetch_close_on_date_returns_none_when_no_bar_before_price_date(monkeypatch):
    stub = _StubProvider(history=_bars(["2026-08-24"], [1601.05]))
    monkeypatch.setattr(benchmark_service, "get_provider", lambda: stub)

    assert _fetch_close_on_date("^SET.BK", "2026-08-17") is None


def test_fetch_close_on_date_returns_none_on_provider_exception(monkeypatch):
    stub = _StubProvider(error=RuntimeError("network unavailable"))
    monkeypatch.setattr(benchmark_service, "get_provider", lambda: stub)

    assert _fetch_close_on_date("QQQ", "2026-08-24") is None


# ── fetch_and_store_benchmarks: fresh rows actually persist ───────────────────

def test_fetch_and_store_benchmarks_persists_fresh_row_after_stale_gap(monkeypatch):
    """End-to-end reproduction at the scheduler-facing entry point: seed the
    DB with the exact stale state observed live (^SET.BK's last row is
    2026-08-21), then run the daily fetch for 2026-08-24 with a provider that
    now has a fresh bar. A new row must be persisted — this is the ingestion
    resuming, which is what was broken."""
    db = make_session()
    db.add(BenchmarkPrice(symbol="^SET.BK", price_date="2026-08-21", close_price=1619.37, sync_status="ok"))
    db.commit()

    stub = _StubProvider(history=_bars(["2026-08-24"], [1601.05]))
    monkeypatch.setattr(benchmark_service, "get_provider", lambda: stub)

    results = asyncio.run(fetch_and_store_benchmarks(db, symbols=["^SET.BK"], price_date="2026-08-24"))

    assert results == {"^SET.BK": pytest.approx(1601.05)}
    rows = db.query(BenchmarkPrice).filter_by(symbol="^SET.BK").order_by(BenchmarkPrice.price_date).all()
    assert [r.price_date for r in rows] == ["2026-08-21", "2026-08-24"]
    assert rows[-1].close_price == pytest.approx(1601.05)


def test_fetch_and_store_benchmarks_one_symbol_failure_does_not_block_the_other(monkeypatch):
    """A provider failure for one benchmark must not prevent the other from
    persisting — guards against the 'one benchmark failure aborting the
    rest' defect class."""
    db = make_session()

    def _get_history_for(symbol, period="6mo", interval="1d"):
        if symbol == "^SET.BK":
            raise RuntimeError("boom")
        return _bars(["2026-08-24"], [713.44])

    class _MultiStub:
        def get_history(self, symbol, period="6mo", interval="1d"):
            return _get_history_for(symbol, period, interval)

    monkeypatch.setattr(benchmark_service, "get_provider", lambda: _MultiStub())

    results = asyncio.run(
        fetch_and_store_benchmarks(db, symbols=["^SET.BK", "QQQ"], price_date="2026-08-24")
    )

    assert results == {"^SET.BK": None, "QQQ": pytest.approx(713.44)}
    rows = db.query(BenchmarkPrice).all()
    assert [(r.symbol, r.price_date) for r in rows] == [("QQQ", "2026-08-24")]
