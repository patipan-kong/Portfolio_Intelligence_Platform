"""BANPU-WP3.3 fetch-layer integration tests.

These tests use deterministic provider, cache, and ledger projections.  No
network or repository database is touched.  The legacy path is exercised with
an empty canonical guard projection; converted paths are required to consume
WP3.1-shaped evidence through the WP3.2 predicates and never fall back to the
unbound quote/history or stale-cache paths.
"""

import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import services.data_fetcher as fetcher
import services.market_data.position_conversion_quote_contract as contract
from models.database import MarketDataCache
from services.transaction_canonicalizer import (
    PositionConversionBoundaryEvidence,
    PositionConversionDates,
    PositionConversionQuoteBinding,
    PositionConversionSuccessor,
)


_UTC7_MIDNIGHT_BOUNDARY_TS = 1699981200


@dataclass(frozen=True)
class _Observation:
    timestamp: int
    close: float | None


@dataclass(frozen=True)
class _Evidence:
    provider: str
    requested_symbol: str
    served_symbol: str | None
    observations: tuple[_Observation, ...]
    current_close: float | None
    previous_close: float | None
    exchange_timezone_name: str | None


class _Provider:
    def __init__(self, evidence: object | None = None):
        self.evidence = evidence
        self.quote_calls = 0
        self.evidence_calls = 0
        self.history_calls = 0
        self.history_batch_calls = 0
        self.quote_result = {
            "current_price": 7.0,
            "previous_close": 6.5,
            "last_updated": "legacy",
        }
        self.history_result = pd.DataFrame(
            {"Close": [100.0, 101.0]},
            index=pd.to_datetime(["2024-01-01", "2024-01-02"], utc=True),
        )

    def get_quote(self, _symbol: str) -> dict:
        self.quote_calls += 1
        return dict(self.quote_result)

    def get_quote_evidence(self, _symbol: str) -> object | None:
        self.evidence_calls += 1
        return self.evidence

    def get_history(self, _symbol: str, _period: str = "6mo", _interval: str = "1d"):
        self.history_calls += 1
        return self.history_result

    def get_history_batch(self, symbols: list[str], _period: str = "6mo", _interval: str = "1d"):
        self.history_batch_calls += 1
        return {symbol: self.history_result for symbol in symbols}


def _binding(
    *,
    asset_id: int = 42,
    provider: str = "yahoo_chart",
    provider_symbol: str = "SUCC.BK",
    predecessor_symbol: str = "PRED.BK",
    epoch: date = date(2023, 11, 15),
    transition: date = date(2023, 11, 15),
) -> contract.SuccessorQuoteBinding:
    successor = PositionConversionSuccessor(
        asset_id=asset_id,
        symbol="SUCC",
        provider_symbol=provider_symbol,
        shares_entitled=10,
        shares_received=100,
    )
    quote_binding = PositionConversionQuoteBinding(
        provider=provider,
        predecessor_provider_symbol=predecessor_symbol,
        successor_provider_symbol=provider_symbol,
    )
    dates = PositionConversionDates(
        legal_effective_date=date(2023, 11, 10),
        valuation_transition_date=transition,
        predecessor_last_price_date=date(2023, 11, 14),
        successor_quote_epoch_start_date=epoch,
    )
    return contract.build_successor_quote_binding(successor, quote_binding, dates)


def _evidence(
    *,
    provider: str = "yahoo_chart",
    requested_symbol: str = "SUCC.BK",
    served_symbol: str | None = "SUCC.BK",
    timestamps: tuple[int, ...] = (
        _UTC7_MIDNIGHT_BOUNDARY_TS,
        _UTC7_MIDNIGHT_BOUNDARY_TS + 86400,
    ),
    closes: tuple[float | None, ...] = (100.0, 101.0),
    current_close: float | None = 101.0,
    previous_close: float | None = 100.0,
    exchange_timezone_name: str | None = "Asia/Bangkok",
) -> _Evidence:
    return _Evidence(
        provider=provider,
        requested_symbol=requested_symbol,
        served_symbol=served_symbol,
        observations=tuple(
            _Observation(timestamp=timestamp, close=close)
            for timestamp, close in zip(timestamps, closes)
        ),
        current_close=current_close,
        previous_close=previous_close,
        exchange_timezone_name=exchange_timezone_name,
    )


def _empty_projection() -> fetcher._ConversionGuardProjection:
    return fetcher._ConversionGuardProjection(
        available=True,
        bindings_by_symbol=(),
        ambiguous_symbols=frozenset(),
    )


def _projection_for(
    *bindings: contract.SuccessorQuoteBinding,
) -> fetcher._ConversionGuardProjection:
    return fetcher._ConversionGuardProjection(
        available=True,
        bindings_by_symbol=tuple(
            (binding.provider_symbol, binding) for binding in bindings
        ),
        ambiguous_symbols=frozenset(),
        boundary_evidence_by_symbol=tuple(
            (binding.provider_symbol, _boundary_evidence())
            for binding in bindings
        ),
    )


def _boundary_evidence() -> PositionConversionBoundaryEvidence:
    return PositionConversionBoundaryEvidence(
        predecessor_reference_price=Decimal("95.50"),
        successor_reference_price=Decimal("101.25"),
        mechanical_nav_tolerance_pct=Decimal("0.50"),
        suspension_gap_annotation="test fixture",
    )


def _patch_common(monkeypatch, provider: _Provider, *, projection=None):
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: True)
    monkeypatch.setattr(
        fetcher,
        "_read_conversion_guard_projection",
        lambda: _empty_projection() if projection is None else projection,
    )


def _real_cache_session(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    MarketDataCache.__table__.create(bind=engine)
    session_factory = sessionmaker(bind=engine)
    monkeypatch.setattr(fetcher, "SessionLocal", session_factory)
    return session_factory


def _seed_cache_row(session_factory, symbol, cache_type, payload):
    now = datetime.utcnow()
    db = session_factory()
    db.add(
        MarketDataCache(
            symbol=symbol,
            cache_type=cache_type,
            payload_json=json.dumps(payload),
            fetched_at=now,
            expires_at=now + timedelta(hours=1),
            hit_count=0,
        )
    )
    db.commit()
    db.close()


def test_valid_converted_successor_quote_uses_wp31_evidence_and_namespaced_cache(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    writes = []
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: writes.append(args))

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["current_price"] == 101.0
    assert result["previous_close"] == 100.0
    assert set(result) == {"current_price", "previous_close", "last_updated"}
    assert provider.evidence_calls == 1
    assert provider.quote_calls == 0
    assert writes[0][0:2] == (
        "SUCC.BK",
        "quote:asset=42:epoch=2023-11-15",
    )
    assert writes[0][2][fetcher._BOUND_PROVIDER_KEY] == "yahoo_chart"


@pytest.mark.parametrize(
    "evidence_kwargs,expected_reason",
    [
        ({"served_symbol": "OTHER.BK"}, "PROVIDER_SYMBOL_MISMATCH"),
        ({"provider": "wrong_provider"}, "PROVIDER_SYMBOL_MISMATCH"),
        (
            {"timestamps": (_UTC7_MIDNIGHT_BOUNDARY_TS - 1,)},
            "CROSS_EPOCH_TIMESTAMP",
        ),
        ({"exchange_timezone_name": "Not/A_Real_Zone"}, "EVIDENCE_CONTRACT_NOT_SATISFIED"),
        ({"current_close": None}, "EVIDENCE_CONTRACT_NOT_SATISFIED"),
    ],
)
def test_adversarial_provider_evidence_fails_closed_without_legacy_fallback(
    monkeypatch,
    evidence_kwargs,
    expected_reason,
):
    binding = _binding()
    provider = _Provider(_evidence(**evidence_kwargs))
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(
        fetcher,
        "_get_stale",
        lambda *_: pytest.fail("bound path must not request stale cache"),
    )
    monkeypatch.setattr(
        fetcher,
        "_set_cached",
        lambda *args: pytest.fail("quarantined evidence must not be cached"),
    )

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["current_price"] is None
    assert result["previous_close"] is None
    assert result["_quarantine_reason"] == expected_reason
    assert result["_quarantine_asset_id"] == 42
    assert provider.quote_calls == 0


def test_wrong_requested_binding_symbol_fails_before_cache_or_provider(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: pytest.fail("wrong requested symbol must not read a cache row"),
    )

    result = fetcher.fetch_price_info("OTHER.BK", binding=binding)

    assert result["_quarantine_reason"] == "PROVIDER_SYMBOL_MISMATCH"
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0


def test_request_identity_result_is_delegated_and_enforced_before_cache_or_provider(
    monkeypatch,
):
    binding = _binding()
    provider = _Provider(_evidence())
    calls = []

    def _request_identity(binding_arg, requested_symbol, request_provider=None):
        calls.append((binding_arg, requested_symbol, request_provider))
        return contract.QuarantineResult(
            contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH,
            binding_arg.asset_id,
        )

    monkeypatch.setattr(fetcher, "evaluate_request_identity", _request_identity)
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: pytest.fail("request identity refusal must precede cache reads"),
    )

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["_quarantine_reason"] == "PROVIDER_SYMBOL_MISMATCH"
    assert result["_quarantine_asset_id"] == binding.asset_id
    assert calls == [(binding, "SUCC.BK", None)]
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0


def test_omitted_request_provider_preserves_post_fetch_provider_quarantine(
    monkeypatch,
):
    binding = _binding()
    provider = _Provider(_evidence(provider="wrong_provider"))
    calls = []

    def _request_identity(binding_arg, requested_symbol, request_provider=None):
        calls.append((binding_arg, requested_symbol, request_provider))
        return contract.evaluate_request_identity(
            binding_arg,
            requested_symbol,
            request_provider,
        )

    monkeypatch.setattr(fetcher, "evaluate_request_identity", _request_identity)
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(
        fetcher,
        "_set_cached",
        lambda *_: pytest.fail("provider-mismatched evidence must not be cached"),
    )

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert calls == [(binding, "SUCC.BK", None)]
    assert result["_quarantine_reason"] == "PROVIDER_SYMBOL_MISMATCH"
    assert provider.evidence_calls == 1
    assert provider.quote_calls == 0


def test_malformed_binding_fails_closed_without_provider_or_cache(monkeypatch):
    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_empty_projection())
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: pytest.fail("malformed binding must not read a cache row"),
    )

    result = fetcher.fetch_price_info("SUCC.BK", binding=SimpleNamespace())

    assert result["_quarantine_reason"] == "MISSING_OR_AMBIGUOUS_IDENTIFIER"
    assert result["_quarantine_asset_id"] == 0
    assert provider.evidence_calls == 0


def test_unbound_converted_identity_is_refused_and_never_falls_back(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: pytest.fail("guard refusal must precede cache reads"),
    )

    result = fetcher.fetch_price_info("SUCC.BK")

    assert result["_quarantine_reason"] == "MISSING_OR_AMBIGUOUS_IDENTIFIER"
    assert result["_quarantine_asset_id"] == 42
    assert provider.quote_calls == 0
    assert provider.evidence_calls == 0


def test_guard_projection_transition_refuses_unbound_caller_without_restart(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    projections = iter((_empty_projection(), _projection_for(binding)))
    _patch_common(monkeypatch, provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: next(projections))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: None)

    first = fetcher.fetch_price_info("SUCC.BK")
    second = fetcher.fetch_price_info("SUCC.BK")

    assert first["current_price"] == 7.0
    assert second["current_price"] is None
    assert second["_quarantine_reason"] == "MISSING_OR_AMBIGUOUS_IDENTIFIER"
    assert provider.quote_calls == 1


def test_guard_reads_canonical_position_conversion_source(monkeypatch):
    binding = _binding()
    parsed = SimpleNamespace(
        is_valid=True,
        value=SimpleNamespace(
            successor=SimpleNamespace(
                asset_id=binding.asset_id,
                provider_symbol=binding.provider_symbol,
            ),
            quote_binding=SimpleNamespace(
                provider=binding.provider,
                successor_provider_symbol=binding.provider_symbol,
            ),
            dates=SimpleNamespace(
                successor_quote_epoch_start_date=binding.quote_epoch_start_date,
                valuation_transition_date=binding.valuation_transition_date,
            ),
            boundary_evidence=_boundary_evidence(),
        ),
    )
    canonical_row = SimpleNamespace(position_conversion=parsed)
    raw_row = object()

    class _Query:
        def filter_by(self, **kwargs):
            assert kwargs == {"transaction_type": "POSITION_CONVERSION"}
            return self

        def all(self):
            return [raw_row]

    class _Session:
        def query(self, model):
            assert model is fetcher.Transaction
            return _Query()

        def close(self):
            pass

    monkeypatch.setattr(fetcher, "SessionLocal", lambda: _Session())
    monkeypatch.setattr(
        fetcher,
        "canonicalize_transactions",
        lambda rows: (canonical_row,) if rows == [raw_row] else pytest.fail("unexpected source rows"),
    )
    calls = []

    def _request_identity(binding_arg, requested_symbol, request_provider=None):
        calls.append((binding_arg, requested_symbol, request_provider))
        return contract.evaluate_request_identity(
            binding_arg,
            requested_symbol,
            request_provider,
        )

    monkeypatch.setattr(fetcher, "evaluate_request_identity", _request_identity)

    projection = fetcher._read_conversion_guard_projection()

    assert projection.available is True
    assert projection.binding_for("SUCC.BK") == binding
    assert calls == [(binding, "SUCC.BK", None)]


def test_guard_source_failure_is_not_treated_as_empty(monkeypatch):
    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", fetcher._unavailable_conversion_guard_projection)
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: pytest.fail("undetermined membership must refuse before cache"),
    )

    result = fetcher.fetch_price_info("ANY.BK")

    assert result["_quarantine_reason"] == "MISSING_OR_AMBIGUOUS_IDENTIFIER"
    assert result["_quarantine_asset_id"] == 0
    assert provider.quote_calls == 0


def test_cache_identity_separates_asset_epoch_quote_and_history_namespaces(monkeypatch):
    binding_a = _binding(asset_id=42, epoch=date(2023, 11, 15))
    binding_b = _binding(asset_id=43, epoch=date(2023, 11, 16))
    assert ("PRED.BK", "quote") != (
        "SUCC.BK",
        contract.quote_cache_type(binding_a),
    )
    assert contract.quote_cache_type(binding_a) != contract.quote_cache_type(binding_b)
    assert contract.history_cache_type(binding_a) != contract.history_cache_type(binding_b)
    assert contract.quote_cache_type(binding_a) != contract.history_cache_type(binding_a)

    provider = _Provider(_evidence())
    writes = []
    _patch_common(
        monkeypatch,
        provider,
        projection=_projection_for(binding_a, binding_b),
    )
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: writes.append(args))

    fetcher.fetch_price_info("SUCC.BK", binding=binding_a)
    provider.evidence = _evidence(
        timestamps=(
            _UTC7_MIDNIGHT_BOUNDARY_TS + 86400,
            _UTC7_MIDNIGHT_BOUNDARY_TS + 2 * 86400,
        )
    )
    fetcher.fetch_price_info("SUCC.BK", binding=binding_b)

    assert [write[1] for write in writes] == [
        "quote:asset=42:epoch=2023-11-15",
        "quote:asset=43:epoch=2023-11-16",
    ]


def test_bound_cache_hit_requires_binding_and_provider_namespace(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    cache_type_calls = []
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda symbol, cache_type: (
            cache_type_calls.append((symbol, cache_type))
            or {
                "current_price": 101.0,
                "previous_close": 100.0,
                "last_updated": "cached",
                fetcher._BOUND_PROVIDER_KEY: "yahoo_chart",
            }
        ),
    )
    monkeypatch.setattr(
        fetcher,
        "_set_cached",
        lambda *args: pytest.fail("valid namespaced cache hit must not write"),
    )

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result == {
        "current_price": 101.0,
        "previous_close": 100.0,
        "last_updated": "cached",
    }
    assert cache_type_calls == [("SUCC.BK", "quote:asset=42:epoch=2023-11-15")]
    assert provider.evidence_calls == 0


def test_bound_quote_real_cache_read_rejects_wrong_epoch_entry(monkeypatch):
    binding = _binding(epoch=date(2023, 11, 15))
    wrong_epoch_binding = _binding(epoch=date(2023, 11, 14))
    session_factory = _real_cache_session(monkeypatch)
    wrong_cache_type = contract.quote_cache_type(wrong_epoch_binding)
    canonical_cache_type = contract.quote_cache_type(binding)
    _seed_cache_row(
        session_factory,
        "SUCC.BK",
        wrong_cache_type,
        {
            "current_price": 999.0,
            "previous_close": 998.0,
            "last_updated": "wrong-epoch",
            fetcher._BOUND_PROVIDER_KEY: "yahoo_chart",
        },
    )

    db = session_factory()
    assert (
        db.query(MarketDataCache)
        .filter_by(symbol="SUCC.BK", cache_type=canonical_cache_type)
        .first()
        is None
    )
    db.close()

    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["current_price"] == 101.0
    assert result["previous_close"] == 100.0
    assert provider.evidence_calls == 1
    db = session_factory()
    wrong_row = (
        db.query(MarketDataCache)
        .filter_by(symbol="SUCC.BK", cache_type=wrong_cache_type)
        .one()
    )
    canonical_row = (
        db.query(MarketDataCache)
        .filter_by(symbol="SUCC.BK", cache_type=canonical_cache_type)
        .one()
    )
    assert wrong_row.hit_count == 0
    assert json.loads(canonical_row.payload_json)["current_price"] == 101.0
    db.close()


def test_bound_quote_real_cache_read_retrieves_canonical_epoch_entry(monkeypatch):
    binding = _binding(epoch=date(2023, 11, 15))
    session_factory = _real_cache_session(monkeypatch)
    cache_type = contract.quote_cache_type(binding)
    _seed_cache_row(
        session_factory,
        "SUCC.BK",
        cache_type,
        {
            "current_price": 101.0,
            "previous_close": 100.0,
            "last_updated": "canonical-cache",
            fetcher._BOUND_PROVIDER_KEY: "yahoo_chart",
        },
    )

    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result == {
        "current_price": 101.0,
        "previous_close": 100.0,
        "last_updated": "canonical-cache",
    }
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0
    db = session_factory()
    row = db.query(MarketDataCache).filter_by(
        symbol="SUCC.BK", cache_type=cache_type
    ).one()
    assert row.hit_count == 1
    db.close()


def test_wrong_provider_cache_payload_is_not_reused(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    writes = []
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: {
            "current_price": 999.0,
            "previous_close": 998.0,
            "last_updated": "wrong-provider",
            fetcher._BOUND_PROVIDER_KEY: "wrong_provider",
        },
    )
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: writes.append(args))

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["current_price"] == 101.0
    assert provider.evidence_calls == 1
    assert writes[0][2][fetcher._BOUND_PROVIDER_KEY] == "yahoo_chart"


def test_bound_history_namespace_and_stale_fallback_suppression(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    writes = []
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: writes.append(args))
    monkeypatch.setattr(
        fetcher,
        "_get_stale",
        lambda *_: pytest.fail("bound history must not use stale fallback"),
    )

    result = fetcher.fetch_history("SUCC.BK", "5y", "1d", binding=binding)

    assert result is not None
    assert provider.history_calls == 1
    assert writes[0][1] == "history:5y:1d:asset=42:epoch=2023-11-15"
    assert writes[0][2][fetcher._BOUND_PROVIDER_KEY] == "yahoo_chart"


def test_bound_history_real_cache_read_rejects_wrong_epoch_entry(monkeypatch):
    binding = _binding(epoch=date(2023, 11, 15))
    wrong_epoch_binding = _binding(epoch=date(2023, 11, 14))
    session_factory = _real_cache_session(monkeypatch)
    wrong_cache_type = contract.history_cache_type(wrong_epoch_binding)
    canonical_cache_type = contract.history_cache_type(binding)
    wrong_history = pd.DataFrame(
        {"Close": [999.0]},
        index=pd.to_datetime(["2023-11-14"], utc=True),
    )
    wrong_payload = fetcher._df_to_payload(wrong_history)
    wrong_payload[fetcher._BOUND_PROVIDER_KEY] = "yahoo_chart"
    _seed_cache_row(session_factory, "SUCC.BK", wrong_cache_type, wrong_payload)

    db = session_factory()
    assert (
        db.query(MarketDataCache)
        .filter_by(symbol="SUCC.BK", cache_type=canonical_cache_type)
        .first()
        is None
    )
    db.close()

    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    result = fetcher.fetch_history("SUCC.BK", "5y", "1d", binding=binding)

    assert result is not None
    assert result["Close"].iloc[0] == 100.0
    assert provider.evidence_calls == 1
    assert provider.history_calls == 1
    db = session_factory()
    wrong_row = (
        db.query(MarketDataCache)
        .filter_by(symbol="SUCC.BK", cache_type=wrong_cache_type)
        .one()
    )
    canonical_row = (
        db.query(MarketDataCache)
        .filter_by(symbol="SUCC.BK", cache_type=canonical_cache_type)
        .one()
    )
    assert wrong_row.hit_count == 0
    assert "json_split" in json.loads(canonical_row.payload_json)
    db.close()


def test_bound_history_real_cache_read_retrieves_canonical_epoch_entry(monkeypatch):
    binding = _binding(epoch=date(2023, 11, 15))
    provider = _Provider(_evidence())
    session_factory = _real_cache_session(monkeypatch)
    cache_type = contract.history_cache_type(binding)
    cached_payload = fetcher._df_to_payload(provider.history_result)
    cached_payload[fetcher._BOUND_PROVIDER_KEY] = "yahoo_chart"
    _seed_cache_row(session_factory, "SUCC.BK", cache_type, cached_payload)

    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    result = fetcher.fetch_history("SUCC.BK", "5y", "1d", binding=binding)

    assert result is not None
    assert result["Close"].tolist() == [100.0, 101.0]
    assert provider.evidence_calls == 0
    assert provider.history_calls == 0
    db = session_factory()
    row = db.query(MarketDataCache).filter_by(
        symbol="SUCC.BK", cache_type=cache_type
    ).one()
    assert row.hit_count == 1
    db.close()


def test_prefetch_history_batch_uses_bound_history_namespace(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    writes = []
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: writes.append(args))

    fetcher.prefetch_history_batch(
        ["SUCC.BK"],
        period="5y",
        interval="1d",
        bindings={"SUCC.BK": binding},
    )

    assert provider.history_batch_calls == 1
    assert writes[0][1] == "history:5y:1d:asset=42:epoch=2023-11-15"


def test_legacy_unconverted_quote_cache_and_sparse_behavior_remain_unchanged(monkeypatch):
    provider = _Provider(_evidence())
    provider.quote_result = {
        "current_price": 100.0,
        "previous_close": None,
        "last_updated": "legacy-sparse",
    }
    _patch_common(monkeypatch, provider)
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: None)

    result = fetcher.fetch_price_info("PRED.BK")

    assert result == {
        "current_price": 100.0,
        "previous_close": None,
        "last_updated": "legacy-sparse",
    }
    assert provider.quote_calls == 1
    assert provider.evidence_calls == 0


def test_legacy_quote_cache_with_missing_previous_close_is_refreshed(monkeypatch):
    provider = _Provider()
    provider.quote_result = {
        "current_price": 248.0,
        "previous_close": 250.0,
        "last_updated": "refreshed",
    }
    writes = []
    _patch_common(monkeypatch, provider)
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: {
            "current_price": 248.0,
            "previous_close": None,
            "last_updated": "old-normalization",
        },
    )
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: writes.append(args))

    result = fetcher.fetch_price_info("KBANK.BK")

    assert result == {
        "current_price": 248.0,
        "previous_close": 250.0,
        "last_updated": "refreshed",
    }
    assert provider.quote_calls == 1
    assert writes[0][0:2] == ("KBANK.BK", "quote")


def test_legacy_unconverted_stale_fallback_is_preserved(monkeypatch):
    provider = _Provider()
    _patch_common(monkeypatch, provider)
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: False)
    monkeypatch.setattr(
        fetcher,
        "_get_stale",
        lambda *_: {
            "current_price": 8.0,
            "previous_close": 7.0,
            "last_updated": "stale",
            "_stale_data": True,
        },
    )

    result = fetcher.fetch_price_info("PRED.BK")

    assert result == {
        "current_price": 8.0,
        "previous_close": 7.0,
        "last_updated": "stale",
    }
    assert provider.quote_calls == 0


def test_bound_sparse_bar_uses_corrected_wp31_previous_close(monkeypatch):
    binding = _binding()
    provider = _Provider(
        _evidence(
            timestamps=(1_700_000_000, 1_700_086_400, 1_700_172_800),
            closes=(95.0, None, 100.0),
            current_close=100.0,
            previous_close=95.0,
        )
    )
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: None)

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["current_price"] == 100.0
    assert result["previous_close"] == 95.0


def test_unbound_history_and_prefetch_refuse_converted_symbol(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: pytest.fail("guard refusal must precede history cache reads"),
    )

    assert fetcher.fetch_history("SUCC.BK") is None
    fetcher.prefetch_history_batch(["SUCC.BK"])
    assert provider.history_calls == 0
    assert provider.history_batch_calls == 0


def test_data_fetcher_does_not_reimplement_wp5_or_reference_decimal_parsing():
    source = Path(fetcher.__file__).read_text(encoding="utf-8")
    assert "mechanical_nav_tolerance_pct" not in source
    assert "Decimal(str(" not in source
    assert "reconcil" not in source.lower()


def _assert_unavailable_guard_refuses_before_cache(monkeypatch):
    provider = _Provider()
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: True)
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: pytest.fail("unavailable guard must refuse before cache"),
    )

    result = fetcher.fetch_price_info("ANY.BK")

    assert result["current_price"] is None
    assert result["_quarantine_reason"] == "MISSING_OR_AMBIGUOUS_IDENTIFIER"
    assert result["_quarantine_asset_id"] == 0
    assert provider.quote_calls == 0


def test_guard_session_construction_failure_is_unavailable_and_fail_closed(monkeypatch):
    def _open_failure():
        raise RuntimeError("session open failed")

    monkeypatch.setattr(fetcher, "SessionLocal", _open_failure)
    _assert_unavailable_guard_refuses_before_cache(monkeypatch)


def test_guard_query_failure_is_unavailable_and_fail_closed(monkeypatch):
    class _Session:
        def query(self, _model):
            raise RuntimeError("query failed")

        def close(self):
            self.closed = True

    session = _Session()
    monkeypatch.setattr(fetcher, "SessionLocal", lambda: session)
    _assert_unavailable_guard_refuses_before_cache(monkeypatch)
    assert session.closed is True


def test_guard_canonicalization_failure_is_unavailable_and_fail_closed(monkeypatch):
    class _Query:
        def filter_by(self, **_kwargs):
            return self

        def all(self):
            return []

    class _Session:
        def query(self, _model):
            return _Query()

        def close(self):
            self.closed = True

    session = _Session()

    def _canonicalization_failure(_rows):
        raise RuntimeError("canonicalization failed")

    monkeypatch.setattr(fetcher, "SessionLocal", lambda: session)
    monkeypatch.setattr(fetcher, "canonicalize_transactions", _canonicalization_failure)
    _assert_unavailable_guard_refuses_before_cache(monkeypatch)
    assert session.closed is True


def test_guard_cleanup_failure_is_unavailable_and_fail_closed(monkeypatch):
    class _Query:
        def filter_by(self, **_kwargs):
            return self

        def all(self):
            return []

    class _Session:
        def query(self, _model):
            return _Query()

        def close(self):
            raise RuntimeError("close failed")

    monkeypatch.setattr(fetcher, "SessionLocal", lambda: _Session())
    projection = fetcher._read_conversion_guard_projection()
    assert projection.available is False
    _assert_unavailable_guard_refuses_before_cache(monkeypatch)


@pytest.mark.parametrize(
    ("period", "interval"),
    [("6mo", "1d"), ("5y", "1h")],
)
def test_bound_history_rejects_unsupported_namespace_before_any_cache_or_stale_read(
    monkeypatch,
    period,
    interval,
):
    binding = _binding()
    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: pytest.fail("unsupported bound history must not read cache"),
    )
    monkeypatch.setattr(
        fetcher,
        "_get_stale",
        lambda *_: pytest.fail("unsupported bound history must not read stale cache"),
    )
    monkeypatch.setattr(
        fetcher,
        "_set_cached",
        lambda *_: pytest.fail("unsupported bound history must not write cache"),
    )

    result = fetcher.fetch_history(
        "SUCC.BK", period, interval, binding=binding
    )

    assert result is None
    assert fetcher._history_cache_type_for_binding(binding, period, interval) is None
    assert provider.evidence_calls == 0
    assert provider.history_calls == 0


@pytest.mark.parametrize(
    ("period", "interval"),
    [("6mo", "1d"), ("5y", "1h")],
)
def test_prefetch_bound_history_rejects_unsupported_namespace_without_cache_io(
    monkeypatch,
    period,
    interval,
):
    binding = _binding()
    provider = _Provider(_evidence())
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *_: pytest.fail("unsupported bound prefetch must not read cache"),
    )
    monkeypatch.setattr(
        fetcher,
        "_set_cached",
        lambda *_: pytest.fail("unsupported bound prefetch must not write cache"),
    )

    fetcher.prefetch_history_batch(
        ["SUCC.BK"],
        period=period,
        interval=interval,
        bindings={"SUCC.BK": binding},
    )

    assert provider.evidence_calls == 0
    assert provider.history_batch_calls == 0


def test_provider_evidence_rejects_requested_and_served_symbol_not_matching_binding(
    monkeypatch,
):
    binding = _binding(provider_symbol="SUCC.BK")
    provider = _Provider(
        _evidence(requested_symbol="OTHER.BK", served_symbol="OTHER.BK")
    )
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["_quarantine_reason"] == "PROVIDER_SYMBOL_MISMATCH"
    assert provider.evidence_calls == 1
    assert provider.quote_calls == 0


@pytest.mark.parametrize("current_close", [0.0, -1.0, float("nan"), float("inf")])
def test_provider_current_close_invalid_values_fail_closed_at_fetch_layer(
    monkeypatch,
    current_close,
):
    binding = _binding()
    provider = _Provider(_evidence(current_close=current_close))
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(
        fetcher,
        "_set_cached",
        lambda *_: pytest.fail("invalid evidence must not be cached"),
    )

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["current_price"] is None
    assert result["_quarantine_reason"] == "EVIDENCE_CONTRACT_NOT_SATISFIED"
    assert provider.quote_calls == 0


@pytest.mark.parametrize("previous_close", [0.0, -1.0, float("nan"), float("inf")])
def test_provider_previous_close_invalid_present_values_fail_closed(
    monkeypatch,
    previous_close,
):
    binding = _binding()
    provider = _Provider(_evidence(previous_close=previous_close))
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["current_price"] is None
    assert result["_quarantine_reason"] == "EVIDENCE_CONTRACT_NOT_SATISFIED"


def test_provider_previous_close_none_remains_accepted(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence(previous_close=None))
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *_: None)

    result = fetcher.fetch_price_info("SUCC.BK", binding=binding)

    assert result["current_price"] == 101.0
    assert result["previous_close"] is None


@pytest.mark.parametrize(
    ("evidence_kwargs", "expected_reason"),
    [
        ({"provider": "wrong_provider"}, "PROVIDER_SYMBOL_MISMATCH"),
        (
            {"requested_symbol": "OTHER.BK", "served_symbol": "OTHER.BK"},
            "PROVIDER_SYMBOL_MISMATCH",
        ),
        (
            {"timestamps": (_UTC7_MIDNIGHT_BOUNDARY_TS - 1,)},
            "CROSS_EPOCH_TIMESTAMP",
        ),
        ({"exchange_timezone_name": "Not/A_Real_Zone"}, "EVIDENCE_CONTRACT_NOT_SATISFIED"),
    ],
)
def test_bound_history_evidence_mismatch_and_malformed_values_fail_closed(
    monkeypatch,
    caplog,
    evidence_kwargs,
    expected_reason,
):
    binding = _binding()
    provider = _Provider(_evidence(**evidence_kwargs))
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(
        fetcher,
        "_get_stale",
        lambda *_: pytest.fail("bound history must not use stale fallback"),
    )
    monkeypatch.setattr(
        fetcher,
        "_set_cached",
        lambda *_: pytest.fail("quarantined history must not be cached"),
    )

    result = fetcher.fetch_history("SUCC.BK", "5y", "1d", binding=binding)

    assert result is None
    assert provider.history_calls == 0
    assert provider.evidence_calls == 1
    # History returns no public diagnostic shape; its structured reason is
    # observable through the deterministic fetch-layer quarantine log.
    assert any(expected_reason in record.message for record in caplog.records)


def test_bound_history_wrong_provider_cache_entry_is_not_reused(monkeypatch):
    binding = _binding()
    provider = _Provider(_evidence())
    wrong_provider_payload = fetcher._df_to_payload(provider.history_result)
    wrong_provider_payload[fetcher._BOUND_PROVIDER_KEY] = "wrong_provider"
    writes = []
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: wrong_provider_payload)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: writes.append(args))

    result = fetcher.fetch_history("SUCC.BK", "5y", "1d", binding=binding)

    assert result is not None
    assert provider.evidence_calls == 1
    assert provider.history_calls == 1
    assert writes[0][1] == "history:5y:1d:asset=42:epoch=2023-11-15"


def test_bound_retrieval_rejects_wrong_namespace_entries_and_preserves_cache_isolation(
    monkeypatch,
):
    binding = _binding()
    provider = _Provider(_evidence())
    legacy_quote = {
        "current_price": 999.0,
        "previous_close": 998.0,
        "last_updated": "legacy",
        fetcher._BOUND_PROVIDER_KEY: "yahoo_chart",
    }
    legacy_history = fetcher._df_to_payload(provider.history_result)
    legacy_history[fetcher._BOUND_PROVIDER_KEY] = "yahoo_chart"
    store = {
        ("SUCC.BK", "quote"): legacy_quote,
        ("SUCC.BK", "history:5y:1d"): legacy_history,
        ("PRED.BK", "quote:asset=42:epoch=2023-11-15"): legacy_quote,
    }
    reads = []
    writes = []
    _patch_common(monkeypatch, provider, projection=_projection_for(binding))

    def _get(symbol, cache_type):
        reads.append((symbol, cache_type))
        return store.get((symbol, cache_type))

    monkeypatch.setattr(fetcher, "_get_cached", _get)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: writes.append(args))

    quote = fetcher.fetch_price_info("SUCC.BK", binding=binding)
    history = fetcher.fetch_history("SUCC.BK", "5y", "1d", binding=binding)

    assert quote["current_price"] == 101.0
    assert history is not None
    assert reads == [
        ("SUCC.BK", "quote:asset=42:epoch=2023-11-15"),
        ("SUCC.BK", "history:5y:1d:asset=42:epoch=2023-11-15"),
    ]
    assert provider.quote_calls == 0
    assert provider.history_calls == 1
    assert [write[1] for write in writes] == [
        "quote:asset=42:epoch=2023-11-15",
        "history:5y:1d:asset=42:epoch=2023-11-15",
    ]


def test_fetcher_delegates_request_and_candidate_policy_to_wp32_entry_points():
    source = Path(fetcher.__file__).read_text(encoding="utf-8")
    request_start = source.index("def _binding_request_identity_result")
    request_end = source.index("def _history_cache_type_for_binding", request_start)
    request_body = source[request_start:request_end]
    assert "evaluate_request_identity(" in request_body
    assert "request_provider=" not in request_body
    assert "check_missing_or_ambiguous_identifier" not in request_body
    assert "check_provider_symbol_mismatch" not in request_body
    assert "SimpleNamespace" not in source
    assert "check_missing_or_ambiguous_identifier" not in source
    assert "check_provider_symbol_mismatch" not in source

    guard_start = source.index("def _read_conversion_guard_projection")
    guard_end = source.index("def _guard_result_from_projection", guard_start)
    guard_body = source[guard_start:guard_end]
    assert "evaluate_request_identity(" in guard_body
    assert "request_provider=" not in guard_body

    start = source.index("def _binding_evidence_result")
    end = source.index("def _fetch_binding_evidence", start)
    body = source[start:end]

    assert "evaluate_candidate_quarantine(" in body
    assert "check_evidence_contract_not_satisfied" not in body
    assert "check_provider_symbol_mismatch" not in body
    assert "check_cross_epoch_timestamp" not in body
    assert "check_cache_namespace_mismatch" not in body
    assert "check_contract_namespace" not in body


def _g4_conversion_payload() -> dict:
    return {
        "schema_version": 1,
        "predecessor": {
            "asset_id": 41,
            "symbol": "PRED.BK",
            "shares_surrendered": "10",
        },
        "successor": {
            "asset_id": 42,
            "symbol": "SUCC.BK",
            "provider_symbol": "SUCC.BK",
            "shares_entitled": "10",
            "shares_received": "10",
        },
        "conversion_ratio": "1",
        "basis": {
            "before": "100",
            "allocated_to_cash_in_lieu": "0",
            "carried_to_successor": "100",
        },
        "cash_in_lieu": None,
        "dates": {
            "legal_effective_date": "2023-11-15",
            "valuation_transition_date": "2023-11-15",
            "predecessor_last_price_date": "2023-11-14",
            "successor_quote_epoch_start_date": "2023-11-15",
        },
        "quote_binding": {
            "provider": "yahoo_chart",
            "predecessor_provider_symbol": "PRED.BK",
            "successor_provider_symbol": "SUCC.BK",
        },
        "boundary_evidence": {
            "predecessor_reference_price": "10",
            "successor_reference_price": "10",
            "mechanical_nav_tolerance_pct": "0.5",
            "suspension_gap_annotation": "test source",
        },
        "evidence": {
            "reference": "G4-TEST",
            "source": "unit-test",
            "captured_at": "2023-11-15T00:00:00Z",
        },
    }


def _g4_raw_conversion_row() -> SimpleNamespace:
    return SimpleNamespace(
        id=1,
        transaction_type="POSITION_CONVERSION",
        symbol="PRED.BK",
        shares=10.0,
        price_per_share=10.0,
        total_amount=100.0,
        fees=0.0,
        taxes=0.0,
        transaction_date=datetime(2023, 11, 15),
        created_at=datetime(2023, 11, 15),
        sector=None,
        notes=None,
        conversion_payload=_g4_conversion_payload(),
    )


def test_g4_actual_canonical_source_transition_refuses_same_process(monkeypatch):
    rows: list[SimpleNamespace] = []

    class _Query:
        def filter_by(self, **kwargs):
            assert kwargs == {"transaction_type": "POSITION_CONVERSION"}
            return self

        def all(self):
            return list(rows)

    class _Session:
        def query(self, model):
            assert model is fetcher.Transaction
            return _Query()

        def close(self):
            pass

    provider = _Provider()
    reads = []
    monkeypatch.setattr(fetcher, "SessionLocal", lambda: _Session())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: True)
    monkeypatch.setattr(
        fetcher,
        "_get_cached",
        lambda *args: reads.append(args) or None,
    )
    monkeypatch.setattr(fetcher, "_set_cached", lambda *_: None)

    first = fetcher.fetch_price_info("SUCC.BK")
    rows.append(_g4_raw_conversion_row())
    second = fetcher.fetch_price_info("SUCC.BK")

    assert first["current_price"] == 7.0
    assert second["current_price"] is None
    assert second["_quarantine_reason"] == "MISSING_OR_AMBIGUOUS_IDENTIFIER"
    assert provider.quote_calls == 1
    # The second request refuses before it can read the legacy quote row.
    assert reads == [("SUCC.BK", "quote")]
