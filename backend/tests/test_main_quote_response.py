"""main.py's _quote_response() — stale-price data-trust translation.

Proves the `_stale_data` -> `is_stale` contract added for the stale-price
data-trust indicator:
  - a price served from data_fetcher's expired-cache fallback path
    (`_stale_data: True`) is reported as `is_stale: true`;
  - a live/fresh-cache price (no `_stale_data` key at all) is `is_stale: false`;
  - the private `_stale_data` key never survives into the response dict;
  - a missing price (current_price is None) is never reported as stale, even
    defensively if `_stale_data` were somehow present alongside it.

Uses main._quote_response directly (pure function, no DB) — see
test_main_get_sector_registry.py for this codebase's "import main.py
directly, no FastAPI TestClient harness" convention.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main


def test_stale_fallback_price_is_reported_as_is_stale_true():
    price = {
        "current_price": 8.0,
        "previous_close": 7.0,
        "last_updated": "stale",
        "_stale_data": True,
    }

    result = main._quote_response(price)

    assert result["is_stale"] is True
    assert result["current_price"] == 8.0
    assert "_stale_data" not in result


def test_live_fetch_result_is_reported_as_is_stale_false():
    price = {
        "current_price": 100.0,
        "previous_close": 98.0,
        "last_updated": "2026-08-24T09:00:00Z",
    }

    result = main._quote_response(price)

    assert result["is_stale"] is False
    assert result["current_price"] == 100.0


def test_fresh_valid_cache_hit_is_not_marked_stale():
    # A non-expired cache hit never carries `_stale_data` in the first place
    # (only data_fetcher's expired-cache fallback path sets it) — confirms
    # the absence of the marker is treated as fresh, not as "unknown".
    price = {
        "current_price": 55.5,
        "previous_close": 55.0,
        "last_updated": "2026-08-24T08:00:00Z",
    }

    result = main._quote_response(price)

    assert result["is_stale"] is False


def test_missing_price_is_never_reported_as_stale():
    price = {"current_price": None, "previous_close": None, "last_updated": None}

    result = main._quote_response(price)

    assert result["is_stale"] is False
    assert result["current_price"] is None


def test_missing_price_stays_non_stale_even_if_stale_marker_is_defensively_present():
    # Should not happen by construction (data_fetcher only sets _stale_data
    # alongside a real cached price), but _quote_response must not misreport
    # a null price as stale even if this invariant were ever violated upstream.
    price = {
        "current_price": None,
        "previous_close": None,
        "last_updated": None,
        "_stale_data": True,
    }

    result = main._quote_response(price)

    assert result["is_stale"] is False
    assert result["current_price"] is None


def test_quarantine_response_is_not_marked_stale():
    # A quarantined quote (fetch-layer identity refusal) has its own private
    # diagnostics but no price and no `_stale_data` — must read as "no data",
    # not "stale data".
    price = {
        "current_price": None,
        "previous_close": None,
        "last_updated": None,
        "_quarantine_reason": "evidence_contract_not_satisfied",
        "_quarantine_asset_id": 42,
    }

    result = main._quote_response(price)

    assert result["is_stale"] is False
    assert result["current_price"] is None
