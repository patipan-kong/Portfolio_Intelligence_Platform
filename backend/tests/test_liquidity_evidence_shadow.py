"""MUJI V2 Phase 4 Slice 4.5A — observed liquidity evidence, SHADOW MODE ONLY.

The execution-risk classifier was built for ``avg_volume * current_price`` but no
production caller ever supplied volume, so every instrument sits on its asset
baseline (Slice 4.5 investigation). ``services.optimizer.liquidity_evidence``
builds that input from each instrument's own listing history and computes the
classification it would produce — beside, never inside, the active context.

``fixtures/liquidity_evidence_shadow_frozen.json`` is a read-only export of
history 250 (stored scores and execution context), the current Registry facts
(after the AMZN01 / META01 repair) and the run-day ``market_data_cache``
daily-history rows of every listing symbol, plus underlying-ticker history for
four DRs kept only as decoys. History 249 comes from
``fixtures/dr_execution_score_frozen.json``.
"""
import copy
import json
import math
import os
import re
import sys
from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services import data_fetcher
from services.execution_instrument_facts import (
    ExecutionInstrumentFacts,
    ExecutionInstrumentForm,
    ExecutionResolutionOutcome,
    ExecutionRole,
)
from services.optimizer import execution_penalty, liquidity_evidence
from services.optimizer.execution_penalty import (
    build_execution_prompt_block,
    compute_portfolio_execution_context,
)
from services.optimizer.liquidity_evidence import (
    DailyBar,
    EvidenceStatus,
    ListingHistory,
    UnobservedReason,
    build_liquidity_evidence,
    build_liquidity_shadow,
    evaluate_listing_liquidity,
)
from services.optimizer.liquidity_evidence_source import (
    evaluate_history_liquidity_shadow,
    listing_histories_from_cache_rows,
    load_listing_histories,
)

BACKEND = os.path.join(os.path.dirname(__file__), "..")
FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")
SHADOW_FIXTURE = os.path.join(FIXTURES, "liquidity_evidence_shadow_frozen.json")
DR_FIXTURE = os.path.join(FIXTURES, "dr_execution_score_frozen.json")

# Run 250 was analysed at 11:41 Bangkok time, mid-session on 2026-11-12.
AS_OF = datetime(2026, 11, 12, 4, 41, 32, tzinfo=timezone.utc)
TODAY_BAR = datetime(2026, 11, 12, 3, 0, tzinfo=timezone.utc)      # 10:00 ICT open
CAPTURED = datetime(2026, 11, 12, 4, 40, tzinfo=timezone.utc)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _sessions(n, last=datetime(2026, 11, 11, 3, 0, tzinfo=timezone.utc)):
    """n weekday session timestamps ending at ``last`` (03:00 UTC = 10:00 ICT)."""
    out, day = [], last
    while len(out) < n:
        if day.weekday() < 5:
            out.append(day)
        day -= timedelta(days=1)
    return list(reversed(out))


def _bars(n, volume=100_000.0, close=10.0, last=datetime(2026, 11, 11, 3, 0, tzinfo=timezone.utc)):
    return tuple(DailyBar(ts, close, volume) for ts in _sessions(n, last))


def _hist(symbol, bars, *, fetched_at=CAPTURED, source="market_data_cache:history:1mo:1d"):
    return ListingHistory(listing_symbol=symbol, bars=tuple(bars), source=source,
                          fetched_at=fetched_at, cache_expired=False)


def _facts(symbol, form=ExecutionInstrumentForm.EQUITY, *, currency="THB", exchange="SET",
           status=ExecutionResolutionOutcome.RESOLVED):
    return ExecutionInstrumentFacts(
        query=symbol, resolution_status=status, instrument_form=form,
        execution_role=ExecutionRole.TRADABLE, currency=currency, exchange=exchange,
        market="Thailand")


def _dr_facts(symbol):
    return _facts(symbol, ExecutionInstrumentForm.DEPOSITARY_RECEIPT)


def _evidence(symbol="PTT.BK", histories=None, *, price=10.0, facts="equity", as_of=AS_OF, quarantine=None):
    if facts == "equity":
        facts = _facts(symbol)
    if histories is None:
        histories = [_hist(symbol, _bars(20))]
    return build_liquidity_evidence(symbol, histories, listing_price=price, facts=facts,
                                    as_of=as_of, quarantine_reason=quarantine)


def _fixture_histories(fx, key="listing_histories"):
    out = {}
    for symbol, rows in fx[key].items():
        out[symbol] = [
            ListingHistory(
                listing_symbol=symbol,
                bars=tuple(DailyBar(datetime.fromisoformat(ts), c, v) for ts, c, v in row["bars"]),
                source=f"market_data_cache:{row['cache_type']}",
                fetched_at=datetime.fromisoformat(row["fetched_at"]).replace(tzinfo=timezone.utc),
                cache_expired=None,
            )
            for row in rows
        ]
    return out


def _fixture_registry_facts(fx):
    return {
        s: ExecutionInstrumentFacts(
            query=s, resolution_status=ExecutionResolutionOutcome(f["resolution_status"]),
            instrument_form=ExecutionInstrumentForm(f["instrument_form"]),
            execution_role=ExecutionRole(f["execution_role"]), currency=f["currency"],
            market=f["market"], exchange=f["exchange"], canonical_symbol=f["canonical_symbol"],
            reason=f["reason"])
        for s, f in fx["registry_facts"].items()
    }


def _frozen_facts(run):
    """Facts as stored in the run (replays the active context exactly)."""
    return {
        sym: ExecutionInstrumentFacts(
            query=sym,
            resolution_status=ExecutionResolutionOutcome(meta["resolution_status"]),
            instrument_form=ExecutionInstrumentForm(meta["instrument_form"]),
            execution_role=ExecutionRole(meta["execution_role"]),
            reason=run["facts_reason"].get(sym),
        )
        for sym, meta in run["stored_execution_context"]["per_symbol"].items()
    }


def _scores(run):
    return {s: {**row, "symbol": s} for s, row in run["stored_scores"].items()}


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@pytest.fixture(scope="module")
def fx():
    return _load(SHADOW_FIXTURE)


@pytest.fixture(scope="module")
def shadow_250(fx):
    run = fx["runs"]["250"]
    scores = _scores(run)
    facts = _fixture_registry_facts(fx)
    active = compute_portfolio_execution_context(copy.deepcopy(scores), facts_by_symbol=facts)
    return build_liquidity_shadow(
        scores, active, histories_by_symbol=_fixture_histories(fx), facts_by_symbol=facts,
        as_of=datetime.fromisoformat(run["analyzed_at"]).replace(tzinfo=timezone.utc),
        quarantine_reasons=fx["quarantine_reasons"])


# ── A. Listing identity ───────────────────────────────────────────────────────

def test_dr_volume_comes_from_its_own_set_listing(fx, shadow_250):
    own = _fixture_histories(fx)
    for dr in fx["underlying_decoy_symbols"]:
        ev = shadow_250["per_symbol"][dr]["evidence"]
        assert ev["status"] == "OBSERVED" and ev["listing_symbol"] == dr
        rows = [r for r in own[dr] if r.source == ev["history_source"]]
        assert len(rows) == 1
        window = [b.volume for b in rows[0].bars if b.timestamp.date() < AS_OF.date()][-20:]
        assert ev["avg_volume"] == pytest.approx(sum(window) / 20)


def test_underlying_share_volume_never_substitutes_for_dr_volume(fx, shadow_250):
    run = fx["runs"]["250"]
    facts = _fixture_registry_facts(fx)
    decoys = _fixture_histories(fx, "underlying_decoys")
    for dr, underlying in fx["underlying_decoy_symbols"].items():
        und_rows = [ListingHistory(underlying, r.bars, r.source, r.fetched_at) for r in decoys[dr]]
        und_avg = sum(b.volume for b in und_rows[0].bars[-21:-1]) / 20
        own_avg = shadow_250["per_symbol"][dr]["evidence"]["avg_volume"]
        assert und_avg > 10 * own_avg, dr      # different instrument, venue and unit

        price = run["stored_scores"][dr]["current_price"]
        # 1. Underlying rows present in the mapping under their own key are never read.
        ev, hyp = evaluate_listing_liquidity(dr, True, [], listing_price=price, facts=facts[dr], as_of=AS_OF)
        assert (ev.status, ev.reason) == (EvidenceStatus.UNOBSERVED, UnobservedReason.NO_LISTING_HISTORY)
        assert hyp is None
        report = build_liquidity_shadow(
            {dr: run["stored_scores"][dr]}, {"per_symbol": {}},
            histories_by_symbol={underlying: und_rows}, facts_by_symbol=facts, as_of=AS_OF)
        assert report["per_symbol"][dr]["evidence"]["reason"] == "NO_LISTING_HISTORY"
        # 2. Underlying rows handed in for the DR are rejected, never averaged.
        ev, hyp = evaluate_listing_liquidity(dr, True, und_rows, listing_price=price, facts=facts[dr], as_of=AS_OF)
        assert ev.reason is UnobservedReason.HISTORY_SYMBOL_MISMATCH and ev.avg_volume is None and hyp is None


def test_shadow_never_consults_the_dr_to_underlying_resolver(fx, monkeypatch):
    from services import symbol_resolver, symbol_normalization

    def refuse(*_a, **_k):
        raise AssertionError("underlying resolution must not be used for listing liquidity")

    monkeypatch.setattr(symbol_resolver, "resolve_yfinance_symbol", refuse)
    monkeypatch.setattr(symbol_normalization, "get_yfinance_symbol", refuse, raising=False)
    run = fx["runs"]["250"]
    facts = _fixture_registry_facts(fx)
    report = build_liquidity_shadow(_scores(run), {"per_symbol": {}}, histories_by_symbol=_fixture_histories(fx),
                                    facts_by_symbol=facts, as_of=AS_OF)
    assert report["summary"]["evidence_status"]["OBSERVED"] == 85
    source = open(liquidity_evidence.__file__, encoding="utf-8").read()
    assert "resolve_yfinance_symbol" not in source and "get_yfinance_symbol" not in source
    assert "normalize_dr_symbol" not in source


@pytest.mark.parametrize("dr", ["AMZN01.BK", "META01.BK"])
def test_amzn01_meta01_use_their_repaired_registry_identities(fx, shadow_250, dr):
    facts = fx["registry_facts"][dr]
    assert (facts["resolution_status"], facts["instrument_form"], facts["currency"]) == (
        "RESOLVED", "DEPOSITARY_RECEIPT", "THB")
    item = shadow_250["per_symbol"][dr]
    assert item["evidence"]["currency_source"] == "REGISTRY_EXECUTION_INSTRUMENT_FACTS"
    assert item["active"]["asset_type"] == "DR" and item["active"]["position_cap_pct"] == 15.0
    assert item["hypothetical"]["asset_type"] == "DR"
    assert item["hypothetical"]["classification_source"] == "REGISTRY_EXECUTION_INSTRUMENT_FACTS"
    assert (item["hypothetical"]["execution_risk"], item["hypothetical"]["position_cap_pct"]) == ("HIGH", 10.0)
    # The frozen run itself predates the repair: it classified them EQUITY.
    assert fx["runs"]["250"]["stored_execution_context"]["per_symbol"][dr]["asset_type"] == "EQUITY"


# ── B. Evidence validity ──────────────────────────────────────────────────────

def test_complete_twenty_session_history_is_observed():
    bars = [DailyBar(ts, 10.0, float(v)) for ts, v in zip(_sessions(25), range(1000, 26000, 1000))]
    ev = _evidence(histories=[_hist("PTT.BK", bars)])
    assert ev.status is EvidenceStatus.OBSERVED and ev.reason is None
    assert ev.avg_volume == sum(range(6000, 26000, 1000)) / 20       # last 20 complete sessions
    assert (ev.complete_sessions, ev.window_sessions) == (25, 20)
    assert ev.last_complete_session.isoformat() == "2026-11-11"
    assert ev.est_avg_daily_traded_value == ev.avg_volume * 10.0
    assert (ev.listing_currency, ev.currency_source) == ("THB", "REGISTRY_EXECUTION_INSTRUMENT_FACTS")


def test_incomplete_current_session_is_excluded():
    bars = list(_bars(20)) + [DailyBar(TODAY_BAR, 10.0, 7.0)]     # partial bar, tiny volume
    ev = _evidence(histories=[_hist("PTT.BK", bars)])
    assert ev.observed and ev.avg_volume == 100_000.0
    assert ev.excluded_incomplete_session.isoformat() == "2026-11-12"
    # Still excluded when evaluated after the close: the data was captured mid-session.
    evening = datetime(2026, 11, 12, 13, 0, tzinfo=timezone.utc)
    ev = _evidence(histories=[_hist("PTT.BK", bars)], as_of=evening)
    assert ev.observed and ev.avg_volume == 100_000.0
    # The observation-day bar is never trusted, so 19 complete + 1 partial is not enough.
    ev = _evidence(histories=[_hist("PTT.BK", list(_bars(19)) + [DailyBar(TODAY_BAR, 10.0, 9e9)])])
    assert ev.reason is UnobservedReason.INSUFFICIENT_SESSIONS and ev.avg_volume is None


def test_fewer_than_twenty_sessions_is_unobserved():
    ev, hyp = evaluate_listing_liquidity("PTT.BK", False, [_hist("PTT.BK", _bars(19))], listing_price=10.0,
                                         facts=_facts("PTT.BK"), as_of=AS_OF)
    assert (ev.status, ev.reason, ev.complete_sessions) == (EvidenceStatus.UNOBSERVED,
                                                           UnobservedReason.INSUFFICIENT_SESSIONS, 19)
    assert hyp is None


def test_stale_history_is_rejected_and_never_preferred():
    stale = _hist("PTT.BK", _bars(250, last=datetime(2026, 6, 30, 3, 0, tzinfo=timezone.utc)),
                  fetched_at=datetime(2026, 7, 1, 1, 0, tzinfo=timezone.utc), source="market_data_cache:history:5y:1d")
    ev = _evidence(histories=[stale])
    assert ev.reason is UnobservedReason.STALE_HISTORY and ev.avg_volume is None
    assert ev.last_complete_session.isoformat() == "2026-06-30"
    fresh = _hist("PTT.BK", _bars(21, volume=50_000.0))
    for order in ([stale, fresh], [fresh, stale]):      # never dict / query order
        ev = _evidence(histories=order)
        assert ev.observed and ev.avg_volume == 50_000.0 and ev.history_source.endswith("1mo:1d")
    # A one-week gap is tolerated (holidays); eight days is stale.
    ok = _hist("PTT.BK", _bars(20, last=datetime(2026, 11, 5, 3, 0, tzinfo=timezone.utc)))
    assert _evidence(histories=[ok]).observed
    old = _hist("PTT.BK", _bars(20, last=datetime(2026, 11, 4, 3, 0, tzinfo=timezone.utc)))
    assert _evidence(histories=[old]).reason is UnobservedReason.STALE_HISTORY


def test_cache_expiry_alone_does_not_reject_completed_sessions():
    row = ListingHistory("PTT.BK", _bars(20), "market_data_cache:history:1mo:1d", CAPTURED, cache_expired=True)
    ev = _evidence(histories=[row])
    assert ev.observed and ev.cache_expired is True


def test_quarantined_listing_is_rejected_even_with_good_history():
    ev, hyp = evaluate_listing_liquidity("BANPU.BK", False, [_hist("BANPU.BK", _bars(25))], listing_price=10.0,
                                         facts=_facts("BANPU.BK"), as_of=AS_OF,
                                         quarantine_reason="MISSING_OR_AMBIGUOUS_IDENTIFIER")
    assert (ev.reason, ev.quarantine_reason) == (UnobservedReason.LISTING_QUARANTINED,
                                                 "MISSING_OR_AMBIGUOUS_IDENTIFIER")
    assert ev.avg_volume is None and hyp is None


def test_unbound_history_guard_reasons_mirror_fetch_history_refusal(monkeypatch):
    from services.market_data.position_conversion_quote_contract import QuarantineReason

    projection = data_fetcher._ConversionGuardProjection(
        available=True, bindings_by_symbol=(), ambiguous_symbols=frozenset({"BANPU.BK"}))
    monkeypatch.setattr(data_fetcher, "_read_conversion_guard_projection", lambda: projection)
    assert data_fetcher.unbound_history_guard_reasons(["BANPU.BK", "PTT.BK"]) == {
        "BANPU.BK": QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER.value}
    monkeypatch.setattr(data_fetcher, "_read_conversion_guard_projection",
                        data_fetcher._unavailable_conversion_guard_projection)
    assert set(data_fetcher.unbound_history_guard_reasons(["BANPU.BK", "PTT.BK"])) == {"BANPU.BK", "PTT.BK"}


@pytest.mark.parametrize("bad, reason", [
    (0.0, UnobservedReason.VOLUME_ZERO),
    (None, UnobservedReason.VOLUME_MISSING),
    (float("nan"), UnobservedReason.VOLUME_MISSING),
    (float("inf"), UnobservedReason.VOLUME_MISSING),
    (-5.0, UnobservedReason.VOLUME_INVALID),
])
def test_zero_missing_or_invalid_volume_is_unusable(bad, reason):
    bars = list(_bars(20))
    bars[7] = DailyBar(bars[7].timestamp, 10.0, bad)
    ev, hyp = evaluate_listing_liquidity("PTT.BK", False, [_hist("PTT.BK", bars)], listing_price=10.0,
                                         facts=_facts("PTT.BK"), as_of=AS_OF)
    assert ev.reason is reason and ev.avg_volume is None and hyp is None
    if bad == 0.0:
        assert ev.zero_volume_sessions == 1
    # Outside the 20-session window it does not matter.
    bars = [DailyBar(_sessions(21)[0], 10.0, bad)] + list(_bars(20))
    assert _evidence(histories=[_hist("PTT.BK", bars)]).observed


@pytest.mark.parametrize("price, reason", [
    (None, UnobservedReason.PRICE_MISSING),
    (0.0, UnobservedReason.PRICE_INVALID),
    (-1.0, UnobservedReason.PRICE_INVALID),
    (float("nan"), UnobservedReason.PRICE_INVALID),
    ("n/a", UnobservedReason.PRICE_INVALID),
    (True, UnobservedReason.PRICE_INVALID),
    (230.0, UnobservedReason.PRICE_LISTING_MISMATCH),   # e.g. an underlying USD price
    (4.9, UnobservedReason.PRICE_LISTING_MISMATCH),
])
def test_missing_or_invalid_listing_price_is_rejected(price, reason):
    ev, hyp = evaluate_listing_liquidity("PTT.BK", False, [_hist("PTT.BK", _bars(20))], listing_price=price,
                                         facts=_facts("PTT.BK"), as_of=AS_OF)
    assert ev.reason is reason and ev.est_avg_daily_traded_value is None and hyp is None


def test_unsupported_or_unknown_currency_is_rejected():
    usd = _facts("AMZN", currency="USD", exchange="NASDAQ")
    assert _evidence("AMZN", [_hist("AMZN", _bars(20))], facts=usd).reason is UnobservedReason.UNSUPPORTED_CURRENCY
    thb_other_venue = _facts("X.BK", exchange="NASDAQ")
    assert _evidence("X.BK", [_hist("X.BK", _bars(20))], facts=thb_other_venue).reason is (
        UnobservedReason.UNSUPPORTED_CURRENCY)
    no_currency = _facts("X.BK", currency=None)
    assert _evidence("X.BK", [_hist("X.BK", _bars(20))], facts=no_currency).reason is UnobservedReason.CURRENCY_UNKNOWN
    # No Registry identity: only the logged SET convention (".BK" / DR shape) supplies THB.
    assert _evidence("AAPL", [_hist("AAPL", _bars(20))], facts=None).reason is UnobservedReason.CURRENCY_UNKNOWN
    unknown = _facts("PTT.BK", status=ExecutionResolutionOutcome.UNKNOWN, currency=None)
    ev = _evidence("PTT.BK", facts=unknown)
    assert ev.observed and ev.currency_source == "SYMBOL_MARKET_CONVENTION_SET_THB"


def test_missing_history_is_unobserved_not_low_liquidity():
    ev, hyp = evaluate_listing_liquidity("PTT.BK", False, [], listing_price=10.0, facts=_facts("PTT.BK"),
                                         as_of=AS_OF)
    assert ev.reason is UnobservedReason.NO_LISTING_HISTORY and hyp is None
    empty = _hist("PTT.BK", ())
    assert _evidence(histories=[empty]).reason is UnobservedReason.NO_LISTING_HISTORY
    only_partial = _hist("PTT.BK", [DailyBar(TODAY_BAR, 10.0, 1.0)])
    assert _evidence(histories=[only_partial]).reason is UnobservedReason.NO_LISTING_HISTORY


def test_evidence_schema_is_stable_and_json_serialisable():
    payload = _evidence().to_dict()
    assert list(payload) == [
        "listing_symbol", "status", "reason", "detail", "avg_volume", "window_sessions",
        "complete_sessions", "first_window_session", "last_complete_session",
        "excluded_incomplete_session", "zero_volume_sessions", "listing_currency", "currency_source",
        "listing_price", "last_complete_close", "est_avg_daily_traded_value", "history_source",
        "history_fetched_at", "cache_expired", "as_of", "quarantine_reason", "candidates_considered"]
    json.dumps(payload)


# ── C. Classifier boundaries (existing THB thresholds, unchanged) ─────────────

# est. ADTV (THB) -> (liquidity, spread, quality, risk, cap, slippage)
EQUITY_BOUNDARIES = {
    999_999:     (48.0, 50.0, 48.8, "HIGH", None, 0.65),
    1_000_000:   (58.0, 57.0, 57.6, "MEDIUM", None, 0.3),
    4_999_999:   (58.0, 57.0, 57.6, "MEDIUM", None, 0.3),
    5_000_000:   (68.0, 65.0, 66.8, "MEDIUM", None, 0.3),
    20_000_000:  (68.0, 65.0, 66.8, "MEDIUM", None, 0.3),
    20_000_001:  (76.0, 65.0, 71.6, "LOW", None, 0.15),
    100_000_000: (76.0, 65.0, 71.6, "LOW", None, 0.15),
    100_000_001: (83.0, 65.0, 75.8, "LOW", None, 0.15),
}
DR_BOUNDARIES = {
    999_999:     (35.0, 33.0, 34.2, "CRITICAL", 10.0, 1.7),
    1_000_000:   (45.0, 40.0, 43.0, "HIGH", 10.0, 0.85),
    4_999_999:   (45.0, 40.0, 43.0, "HIGH", 10.0, 0.85),
    5_000_000:   (55.0, 48.0, 52.2, "MEDIUM", 15.0, 0.5),
    20_000_000:  (55.0, 48.0, 52.2, "MEDIUM", 15.0, 0.5),
    20_000_001:  (63.0, 48.0, 57.0, "MEDIUM", 15.0, 0.5),
    100_000_000: (63.0, 48.0, 57.0, "MEDIUM", 15.0, 0.5),
    100_000_001: (70.0, 48.0, 61.2, "MEDIUM", 15.0, 0.5),
}


@pytest.mark.parametrize("profile, table", [("EQUITY", EQUITY_BOUNDARIES), ("DR", DR_BOUNDARIES)])
@pytest.mark.parametrize("adtv", sorted(EQUITY_BOUNDARIES))
def test_traded_value_boundaries(profile, table, adtv):
    symbol = "SYM01.BK" if profile == "DR" else "SYM.BK"
    facts = _dr_facts(symbol) if profile == "DR" else _facts(symbol)
    bars = _bars(20, volume=float(adtv), close=1.0)
    ev, hyp = evaluate_listing_liquidity(symbol, profile == "DR", [_hist(symbol, bars)], listing_price=1.0,
                                         facts=facts, as_of=AS_OF)
    assert ev.est_avg_daily_traded_value == adtv
    assert hyp["asset_type"] == profile
    got = (hyp["liquidity_score"], hyp["spread_score"], hyp["execution_quality_score"],
           hyp["execution_risk"], hyp["position_cap_pct"], hyp["slippage_cost_est_pct"])
    assert got == table[adtv]


def test_threshold_and_profile_constants_are_unchanged():
    assert execution_penalty._LIQUIDITY_BASELINES == {"DR": 55.0, "ETF": 75.0, "INDEX": 90.0,
                                                      "EQUITY": 68.0, "OTHER": 68.0}
    assert execution_penalty._SPREAD_BASELINES == {"DR": 48.0, "ETF": 72.0, "INDEX": 88.0,
                                                   "EQUITY": 65.0, "OTHER": 65.0}
    assert execution_penalty._SLIPPAGE_ESTIMATES == {"LOW": 0.15, "MEDIUM": 0.30, "HIGH": 0.65, "CRITICAL": 1.50}
    assert (execution_penalty.DR_MAX_POSITION_PCT, execution_penalty.ILLIQUID_POSITION_CAP_PCT,
            execution_penalty._DR_SLIPPAGE_PREMIUM) == (15.0, 10.0, 0.20)
    source = open(execution_penalty.__file__, encoding="utf-8").read()
    for literal in ("est_adtv > 100_000_000", "est_adtv > 20_000_000", "est_adtv < 1_000_000",
                    "est_adtv < 5_000_000"):
        assert source.count(literal) == 1, literal


def test_hypothetical_never_uses_the_single_day_volume_fallback(monkeypatch):
    seen = {}
    real = execution_penalty.classify_execution

    def spy(**kwargs):
        seen.update(kwargs)
        return real(**kwargs)

    monkeypatch.setattr(liquidity_evidence, "classify_execution", spy)
    evaluate_listing_liquidity("PTT.BK", False, [_hist("PTT.BK", _bars(20))], listing_price=10.0,
                               facts=_facts("PTT.BK"), as_of=AS_OF)
    assert seen["volume"] is None and seen["avg_volume"] == 100_000.0 and seen["current_price"] == 10.0


# ── D. Shadow isolation ───────────────────────────────────────────────────────

def _isolation_case(run, histories, current_facts, as_of):
    scores = _scores(run)
    scores_before = copy.deepcopy(scores)
    stored = run["stored_execution_context"]
    stored_before = copy.deepcopy(stored)
    active = compute_portfolio_execution_context(scores, facts_by_symbol=_frozen_facts(run))
    assert _canonical(active) == _canonical(stored)               # byte-identical replay
    prompt_before = build_execution_prompt_block(active)

    report = build_liquidity_shadow(scores, active, histories_by_symbol=histories,
                                    facts_by_symbol=current_facts, as_of=as_of)

    assert scores == scores_before                                 # raw scores untouched
    assert not any(k in row for row in scores.values()
                   for k in ("volume", "avg_volume", "liquidity_evidence", "observed_liquidity"))
    assert _canonical(active) == _canonical(stored) and stored == stored_before
    after = compute_portfolio_execution_context(scores, facts_by_symbol=_frozen_facts(run))
    assert _canonical(after) == _canonical(stored)                 # caps, slippage, warnings
    assert build_execution_prompt_block(after) == prompt_before
    assert report["authoritative"] is False and report["mode"] == "SHADOW"
    return report


def test_frozen_run_250_active_context_is_byte_identical(fx):
    run = fx["runs"]["250"]
    report = _isolation_case(run, _fixture_histories(fx), _fixture_registry_facts(fx),
                             datetime.fromisoformat(run["analyzed_at"]).replace(tzinfo=timezone.utc))
    assert report["summary"]["hypothetical_risk"]["HIGH"] == 10    # the shadow did run


def test_frozen_run_249_active_context_is_byte_identical(fx):
    run = _load(DR_FIXTURE)["runs"]["249"]
    run = {**run, "stored_scores": {s: {k: v for k, v in r.items() if k != "execution_penalized"}
                                    for s, r in run["stored_scores"].items()}}
    as_of = datetime(2026, 11, 12, 3, 54, 45, tzinfo=timezone.utc)
    report = _isolation_case(run, _fixture_histories(fx), _fixture_registry_facts(fx), as_of)
    assert report["summary"]["instruments"] == 89


PRODUCTION_ALLOWED = {
    os.path.normpath("services/optimizer/liquidity_evidence.py"),
    os.path.normpath("services/optimizer/liquidity_evidence_source.py"),
    os.path.normpath("manage.py"),
}


def test_no_production_decision_path_imports_the_shadow():
    """Caps, slippage, eligibility, candidates, allocations, scheduling, policy and
    every Strategist / Challenger / Auditor / Committee prompt are built from
    modules that never import the shadow evaluator."""
    offenders = []
    for root, dirs, files in os.walk(BACKEND):
        rel_root = os.path.relpath(root, BACKEND)
        parts = set(rel_root.split(os.sep))
        if parts & {"tests", ".venv", "venv", "node_modules", "__pycache__", "alembic"} or any(
                p.startswith(".") and p != "." for p in parts):
            dirs[:] = []
            continue
        for name in files:
            if not name.endswith(".py"):
                continue
            rel = os.path.normpath(os.path.join(rel_root, name))
            if rel in PRODUCTION_ALLOWED:
                continue
            try:
                text = open(os.path.join(root, name), encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                continue
            if re.search(r"liquidity_evidence", text):
                offenders.append(rel)
    assert offenders == []


def test_manage_command_imports_the_shadow_lazily_and_only_there():
    source = open(os.path.join(BACKEND, "manage.py"), encoding="utf-8").read()
    head = source.split("def _cmd_liquidity_shadow", 1)[0]
    assert "liquidity_evidence" not in head.split('"""', 2)[2]   # no module-level import
    body = source.split("def _cmd_liquidity_shadow", 1)[1].split("\ndef ", 1)[0]
    assert "SET TRANSACTION READ ONLY" in body and "db.rollback()" in body


def test_cache_loader_reads_only_unbound_daily_rows_and_writes_nothing():
    from sqlalchemy import create_engine, event
    from sqlalchemy.orm import sessionmaker
    from models.database import Base, MarketDataCache

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    frame = pd.DataFrame({"Close": [10.0] * 3, "Volume": [5.0, None, 7.0]},
                         index=pd.to_datetime(_sessions(3), utc=True))
    payload = json.dumps(data_fetcher._df_to_payload(frame))
    fetched = datetime(2026, 11, 12, 4, 40)
    for sym, ct in [("PTT.BK", "history:1mo:1d"), ("PTT.BK", "history:1y:1wk"), ("PTT.BK", "quote"),
                    ("PTT.BK", "history:5y:1d:asset=7:epoch=2026-01-01"), ("PTT", "history:1mo:1d"),
                    ("OTHER.BK", "history:1mo:1d")]:
        db.add(MarketDataCache(symbol=sym, cache_type=ct, payload_json=payload, fetched_at=fetched,
                               expires_at=fetched + timedelta(minutes=15), hit_count=3))
    db.commit()
    statements = []
    event.listen(engine, "before_cursor_execute", lambda *a: statements.append(a[2].strip().split()[0].upper()))
    out = load_listing_histories(db, ["PTT.BK"], as_of=AS_OF)
    assert set(statements) == {"SELECT"}
    assert list(out) == ["PTT.BK"] and [h.source for h in out["PTT.BK"]] == ["market_data_cache:history:1mo:1d"]
    hist = out["PTT.BK"][0]
    assert [b.volume for b in hist.bars] == [5.0, None, 7.0] and hist.cache_expired is False
    assert hist.fetched_at == fetched.replace(tzinfo=timezone.utc)
    assert {r.hit_count for r in db.query(MarketDataCache).all()} == {3}
    assert listing_histories_from_cache_rows([("X.BK", "history:1mo:1d", "not json", None, None)],
                                             as_of=AS_OF)["X.BK"][0].bars == ()


def test_history_diagnostic_reads_a_stored_run_without_changing_it(fx):
    from sqlalchemy import create_engine, event
    from sqlalchemy.orm import sessionmaker
    import models.asset  # noqa: F401
    import models.registry_finding  # noqa: F401
    from models.database import Base, MarketDataCache, OptimizerHistory, RecommendationSnapshot

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    run = fx["runs"]["250"]
    scores = {s: {**r, "symbol": s} for s, r in list(run["stored_scores"].items())[:6]}
    analyzed = datetime.fromisoformat(run["analyzed_at"])
    db.add(OptimizerHistory(id=250, workspace_id=1, portfolio_id=1, portfolio_name="p", analyzed_at=analyzed,
                            swap_count=0, result_json="{}"))
    db.flush()
    db.add(RecommendationSnapshot(optimizer_history_id=250, workspace_id=1, portfolio_id=1,
                                  scores_map_json=json.dumps(scores)))
    for sym in scores:
        for row in fx["listing_histories"].get(sym, []):
            frame = pd.DataFrame({"Close": [b[1] for b in row["bars"]], "Volume": [b[2] for b in row["bars"]]},
                                 index=pd.to_datetime([b[0] for b in row["bars"]], utc=True))
            db.add(MarketDataCache(symbol=sym, cache_type=row["cache_type"],
                                   payload_json=json.dumps(data_fetcher._df_to_payload(frame)),
                                   fetched_at=datetime.fromisoformat(row["fetched_at"]),
                                   expires_at=datetime.fromisoformat(row["expires_at"]), hit_count=0))
    db.commit()
    snapshot_before = db.query(RecommendationSnapshot).one().scores_map_json
    statements = []
    event.listen(engine, "before_cursor_execute", lambda *a: statements.append(a[2].strip().split()[0].upper()))
    report = evaluate_history_liquidity_shadow(db, 250, quarantine_reasons={})
    assert set(statements) <= {"SELECT"} and not db.new and not db.dirty
    assert db.query(RecommendationSnapshot).one().scores_map_json == snapshot_before
    assert report["source"]["optimizer_history_id"] == 250 and report["summary"]["instruments"] == 6
    assert report["as_of"].startswith(run["analyzed_at"][:19])
    with pytest.raises(LookupError):
        evaluate_history_liquidity_shadow(db, 999, quarantine_reasons={})


# ── E. Reporting ──────────────────────────────────────────────────────────────

def test_history_250_shadow_report(shadow_250):
    s = shadow_250["summary"]
    assert s["instruments"] == 89
    assert s["evidence_status"] == {"OBSERVED": 85, "UNOBSERVED": 4}
    assert s["unobserved_symbols"] == {
        "INSUFFICIENT_SESSIONS": ["ABNB06.BK", "AIA06.BK"],   # short histories
        "STALE_HISTORY": ["BANPU.BK"],                        # provider history ends 2026-08-11
        "VOLUME_ZERO": ["PIS.BK"],                            # unusable Volume in window
    }
    assert s["hypothetical_risk"] == {"CRITICAL": 2, "HIGH": 10, "LOW": 59, "MEDIUM": 14}
    assert s["by_active_asset_type"] == {
        "DR": {"CRITICAL": 2, "HIGH": 8, "MEDIUM": 9, "UNOBSERVED": 2},
        "EQUITY": {"HIGH": 2, "LOW": 59, "MEDIUM": 5, "UNOBSERVED": 2},
    }
    stricter = {r["symbol"]: (r["active_cap_pct"], r["hypothetical_cap_pct"], r["hypothetical_risk"])
                for r in s["stricter_position_cap"]}
    assert stricter == {
        "AAPL01.BK": (15.0, 10.0, "HIGH"), "AMZN01.BK": (15.0, 10.0, "HIGH"),
        "BABA01.BK": (15.0, 10.0, "CRITICAL"), "GOLDM01.BK": (15.0, 10.0, "HIGH"),
        "META01.BK": (15.0, 10.0, "HIGH"), "MSFT01.BK": (15.0, 10.0, "HIGH"),
        "ORCL01.BK": (15.0, 10.0, "CRITICAL"), "SMIC01.BK": (15.0, 10.0, "HIGH"),
        "TSLA01.BK": (15.0, 10.0, "HIGH"), "VRT01.BK": (15.0, 10.0, "HIGH"),
    }
    equity_high = sorted(k for k, v in shadow_250["per_symbol"].items()
                         if v["active"]["asset_type"] == "EQUITY" and (v["hypothetical"] or {}).get(
                             "execution_risk") == "HIGH")
    assert equity_high == ["PREB.BK", "SYNTEC.BK"]          # HIGH equities keep no cap (non-DR rule)
    for item in shadow_250["per_symbol"].values():           # active context: baseline everywhere
        assert item["active"]["execution_risk"] == "MEDIUM"
        if item["evidence"]["status"] == "UNOBSERVED":
            assert item["hypothetical"] is None and not item["stricter_position_cap"]


def test_unobserved_reasons_are_explicit_in_the_report(shadow_250):
    for symbol in ("ABNB06.BK", "AIA06.BK", "BANPU.BK", "PIS.BK"):
        ev = shadow_250["per_symbol"][symbol]["evidence"]
        assert ev["status"] == "UNOBSERVED" and ev["reason"] and ev["detail"]
        assert ev["avg_volume"] is None and ev["est_avg_daily_traded_value"] is None
    assert shadow_250["per_symbol"]["BANPU.BK"]["evidence"]["last_complete_session"] == "2026-08-11"
    assert shadow_250["per_symbol"]["ABNB06.BK"]["evidence"]["complete_sessions"] == 19


def test_shadow_fixture_is_a_read_only_export(fx):
    assert "read-only export" in fx["source"]
    assert set(fx["runs"]) == {"250"}
    assert len(fx["runs"]["250"]["stored_scores"]) == 89 and len(fx["listing_histories"]) == 89
    assert math.isclose(fx["runs"]["250"]["stored_scores"]["AMZN01.BK"]["current_price"], 26.25)
