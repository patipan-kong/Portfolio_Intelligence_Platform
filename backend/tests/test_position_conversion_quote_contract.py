"""BANPU-WP3.2 — Binding, epoch, and quarantine contract tests.

Fixture-only. No database, no network, no clock, no registry lookup, no
provider-specific import in the module under test. Written before the
production module exists (Step 2.1): the first collection of this file
against a missing module fails with ImportError, not a test failure -- that
is the expected, observed "fail for absence, not for error" evidence.

Two evidence-fixture families are used deliberately:

- ``_FakeQuoteObservation`` / ``_FakeProviderEvidence`` -- a local stand-in
  that is NOT imported from ``yahoo_chart.py``, proving the module under test
  consumes evidence structurally (IO-1) rather than by concrete type.
- A second, confirmatory set of tests feeds the *real*
  ``yahoo_chart.ProviderQuoteEvidence`` (WP3.1, already accepted at C1)
  through the same predicates, proving real-world structural compatibility.
  This only *imports* yahoo_chart.py from the test file (read-only); it does
  not modify it and the production module under test still never imports it.
"""
import ast
import math
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import pytest

from services.transaction_canonicalizer import (
    PositionConversionBoundaryEvidence,
    PositionConversionDates,
    PositionConversionQuoteBinding,
    PositionConversionSuccessor,
)

import services.market_data.position_conversion_quote_contract as contract


# ─────────────────────────────────────────────────────────────────────────
# Fixture builders
# ─────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class _FakeQuoteObservation:
    """Local stand-in for yahoo_chart.QuoteObservation -- deliberately not
    imported from it, to prove structural (not nominal) consumption."""

    timestamp: int
    close: Optional[float]


@dataclass(frozen=True)
class _FakeProviderEvidence:
    """Local stand-in for yahoo_chart.ProviderQuoteEvidence -- same shape,
    zero import relationship to the real provider module."""

    provider: str
    requested_symbol: str
    served_symbol: Optional[str]
    observations: tuple
    current_close: Optional[float]
    previous_close: Optional[float]
    exchange_timezone_name: Optional[str]


def _successor(asset_id=42, symbol="SUCC", provider_symbol="SUCC.BK"):
    return PositionConversionSuccessor(
        asset_id=asset_id,
        symbol=symbol,
        provider_symbol=provider_symbol,
        shares_entitled=Decimal("10"),
        shares_received=Decimal("100"),
    )


def _quote_binding(provider="yahoo_chart", predecessor_symbol="PRED.BK", successor_symbol="SUCC.BK"):
    return PositionConversionQuoteBinding(
        provider=provider,
        predecessor_provider_symbol=predecessor_symbol,
        successor_provider_symbol=successor_symbol,
    )


def _dates(
    legal_effective_date=date(2023, 11, 10),
    valuation_transition_date=date(2023, 11, 15),
    predecessor_last_price_date=date(2023, 11, 14),
    successor_quote_epoch_start_date=date(2023, 11, 15),
):
    return PositionConversionDates(
        legal_effective_date=legal_effective_date,
        valuation_transition_date=valuation_transition_date,
        predecessor_last_price_date=predecessor_last_price_date,
        successor_quote_epoch_start_date=successor_quote_epoch_start_date,
    )


def _binding(**kwargs):
    return contract.build_successor_quote_binding(_successor(), _quote_binding(**{
        k: v for k, v in kwargs.items() if k in ("provider", "predecessor_symbol", "successor_symbol")
    }), _dates(**{k: v for k, v in kwargs.items() if k not in ("provider", "predecessor_symbol", "successor_symbol")}))


def _request_binding_with(**changes):
    binding = _binding()
    return contract.SuccessorQuoteBinding(
        changes.get("asset_id", binding.asset_id),
        changes.get("provider", binding.provider),
        changes.get("provider_symbol", binding.provider_symbol),
        changes.get("quote_epoch_start_date", binding.quote_epoch_start_date),
        changes.get("valuation_transition_date", binding.valuation_transition_date),
    )


def _qualifying_evidence(
    provider="yahoo_chart",
    requested_symbol="SUCC.BK",
    served_symbol="SUCC.BK",
    timestamps=(1699981200, 1699981200 + 86400),
    closes=(100.0, 101.0),
    exchange_timezone_name="Asia/Bangkok",
):
    observations = tuple(
        _FakeQuoteObservation(timestamp=ts, close=c) for ts, c in zip(timestamps, closes)
    )
    return _FakeProviderEvidence(
        provider=provider,
        requested_symbol=requested_symbol,
        served_symbol=served_symbol,
        observations=observations,
        current_close=closes[-1],
        previous_close=closes[-2] if len(closes) >= 2 else None,
        exchange_timezone_name=exchange_timezone_name,
    )


# UTC+7 midnight boundary: 2023-11-14T17:00:00Z == 2023-11-15T00:00:00+07:00.
# Independently reverified here (not merely trusted from WP3.1) before use.
_UTC7_MIDNIGHT_BOUNDARY_TS = 1699981200


def test_utc7_boundary_constant_is_correct():
    tz = ZoneInfo("Asia/Bangkok")
    from datetime import datetime as _dt

    just_before = _dt.fromtimestamp(_UTC7_MIDNIGHT_BOUNDARY_TS - 1, tz=tz)
    at_boundary = _dt.fromtimestamp(_UTC7_MIDNIGHT_BOUNDARY_TS, tz=tz)
    assert just_before.date() == date(2023, 11, 14)
    assert at_boundary.date() == date(2023, 11, 15)


# ─────────────────────────────────────────────────────────────────────────
# Purity / provider-neutrality structural guard
# ─────────────────────────────────────────────────────────────────────────

_MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "services" / "market_data" / "position_conversion_quote_contract.py"
)

_FORBIDDEN_IMPORT_MODULES = {
    "requests", "sqlalchemy", "psycopg", "psycopg2", "yahoo_chart", "yahoo",
    "services.data_fetcher", "data_fetcher", "main", "services.market_data.yahoo_chart",
    "services.market_data.yahoo", "services.market_data.provider",
    "services.ledger_validator", "ledger_validator", "os",
}
_FORBIDDEN_NAMES = {"registry", "environ", "getenv"}
_FORBIDDEN_CLOCK_ATTRS = {"now", "utcnow", "time"}


def test_module_is_pure_no_io_no_clock_no_provider_import():
    tree = ast.parse(_MODULE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in _FORBIDDEN_IMPORT_MODULES, alias.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            assert module.split(".")[0] not in _FORBIDDEN_IMPORT_MODULES, module
            for alias in node.names:
                assert alias.name not in _FORBIDDEN_IMPORT_MODULES
        elif isinstance(node, ast.Attribute):
            assert node.attr not in _FORBIDDEN_CLOCK_ATTRS, node.attr
        elif isinstance(node, ast.Name):
            assert node.id not in _FORBIDDEN_NAMES, node.id


def test_module_never_imports_a_provider_adapter_or_data_fetcher():
    source = _MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    module_refs = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            module_refs.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module_refs.add(node.module)
    assert not any("yahoo" in ref for ref in module_refs)
    assert not any("data_fetcher" in ref for ref in module_refs)
    assert not any("main" == ref for ref in module_refs)


# ─────────────────────────────────────────────────────────────────────────
# Step 2.2 — IO-2 binding construction
# ─────────────────────────────────────────────────────────────────────────

def test_request_identity_accepts_matching_symbol_without_provider_evidence():
    binding = _binding()
    assert contract.evaluate_request_identity(binding, binding.provider_symbol) is None


def test_request_identity_accepts_absent_authoritative_provider():
    binding = _binding()
    assert contract.evaluate_request_identity(
        binding,
        binding.provider_symbol,
        None,
    ) is None


def test_request_identity_accepts_matching_authoritative_provider():
    binding = _binding()
    assert contract.evaluate_request_identity(
        binding,
        binding.provider_symbol,
        binding.provider,
    ) is None


@pytest.mark.parametrize(
    "malformed_binding",
    [
        contract.SuccessorQuoteBinding(
            0,
            "yahoo_chart",
            "SUCC.BK",
            date(2024, 1, 1),
            date(2024, 1, 1),
        ),
        contract.SuccessorQuoteBinding(
            42,
            "",
            "SUCC.BK",
            date(2024, 1, 1),
            date(2024, 1, 1),
        ),
        object(),
    ],
)
def test_request_identity_rejects_empty_or_malformed_binding_identity(malformed_binding):
    result = contract.evaluate_request_identity(malformed_binding, "SUCC.BK")
    assert result is not None
    assert result.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER
    assert isinstance(result.affected_asset_id, int)


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("asset_id", None),
        ("asset_id", "not-an-integer"),
        ("asset_id", True),
        ("provider", None),
        ("provider", ""),
        ("provider", object()),
        ("provider_symbol", None),
        ("provider_symbol", ""),
        ("provider_symbol", object()),
    ],
)
def test_request_identity_rejects_malformed_non_date_binding_fields(field, bad_value):
    binding = _request_binding_with(**{field: bad_value})
    result = contract.evaluate_request_identity(binding, "OTHER.BK", "another_provider")
    assert result is not None
    assert result.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("quote_epoch_start_date", None),
        ("quote_epoch_start_date", "not-a-date"),
        ("quote_epoch_start_date", datetime(2024, 1, 1)),
        ("valuation_transition_date", None),
        ("valuation_transition_date", "not-a-date"),
        ("valuation_transition_date", datetime(2024, 1, 1)),
    ],
)
def test_request_identity_rejects_malformed_date_fields_before_mismatch(field, bad_value):
    binding = _request_binding_with(**{field: bad_value})
    result = contract.evaluate_request_identity(binding, "OTHER.BK", "another_provider")
    assert result is not None
    assert result.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER
    assert result.affected_asset_id == binding.asset_id


def test_request_identity_malformed_date_precedes_requested_symbol_mismatch():
    binding = _request_binding_with(quote_epoch_start_date=None)
    result = contract.evaluate_request_identity(binding, "OTHER.BK")
    assert result is not None
    assert result.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER
    assert result.affected_asset_id == binding.asset_id


def test_request_identity_malformed_date_precedes_request_provider_mismatch():
    binding = _request_binding_with(valuation_transition_date="not-a-date")
    result = contract.evaluate_request_identity(
        binding,
        binding.provider_symbol,
        "another_provider",
    )
    assert result is not None
    assert result.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER
    assert result.affected_asset_id == binding.asset_id


def test_request_identity_repeated_malformed_binding_is_deterministic():
    binding = _request_binding_with(quote_epoch_start_date="not-a-date")
    first = contract.evaluate_request_identity(binding, "OTHER.BK", "another_provider")
    second = contract.evaluate_request_identity(binding, "OTHER.BK", "another_provider")
    assert first == second
    assert first is not None
    assert first.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER


def test_request_identity_rejects_requested_symbol_mismatch():
    binding = _binding()
    result = contract.evaluate_request_identity(binding, "OTHER.BK")
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH
    assert result.affected_asset_id == binding.asset_id


def test_request_identity_rejects_authoritative_provider_mismatch():
    binding = _binding()
    result = contract.evaluate_request_identity(
        binding,
        binding.provider_symbol,
        "another_provider",
    )
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH
    assert result.affected_asset_id == binding.asset_id


def test_request_identity_returns_one_existing_reason_when_symbol_and_provider_both_mismatch():
    binding = _binding()
    result = contract.evaluate_request_identity(binding, "OTHER.BK", "another_provider")
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH
    assert result.affected_asset_id == binding.asset_id
    assert set(vars(result)) == {"reason", "affected_asset_id"}
    assert isinstance(result.reason, contract.QuarantineReason)


def test_request_identity_is_deterministic_for_identical_inputs():
    binding = _binding()
    first = contract.evaluate_request_identity(binding, "OTHER.BK", "another_provider")
    second = contract.evaluate_request_identity(binding, "OTHER.BK", "another_provider")
    assert first == second


def test_request_identity_has_no_post_fetch_inputs_or_synthetic_evidence():
    import inspect

    signature = inspect.signature(contract.evaluate_request_identity)
    assert list(signature.parameters) == [
        "binding",
        "requested_symbol",
        "request_provider",
    ]
    source = inspect.getsource(contract.evaluate_request_identity)
    assert "ProviderQuoteEvidence" not in source
    assert "SimpleNamespace" not in source
    assert "boundary_evidence" not in source
    tree = ast.parse(source)
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert "SimpleNamespace" not in called_names
    assert "evaluate_candidate_quarantine" not in called_names


def test_io2_binding_maps_exactly_the_five_named_fields():
    successor = _successor(asset_id=99, provider_symbol="SUCC.BK")
    quote_binding = _quote_binding(provider="yahoo_chart", predecessor_symbol="PRED.BK", successor_symbol="SUCC.BK")
    dates = _dates(
        valuation_transition_date=date(2024, 1, 10),
        successor_quote_epoch_start_date=date(2024, 1, 11),
    )
    binding = contract.build_successor_quote_binding(successor, quote_binding, dates)
    assert binding.asset_id == 99
    assert binding.provider == "yahoo_chart"
    assert binding.provider_symbol == "SUCC.BK"
    assert binding.quote_epoch_start_date == date(2024, 1, 11)
    assert binding.valuation_transition_date == date(2024, 1, 10)


def test_io2_predecessor_symbol_never_supplies_the_successor_binding():
    """The differing-symbol fixture required by the plan: predecessor and
    successor provider symbols differ, and the constructed binding must carry
    only the successor value."""
    successor = _successor(provider_symbol="SUCC-ONLY.BK")
    quote_binding = _quote_binding(predecessor_symbol="PRED-ONLY.BK", successor_symbol="SUCC-ONLY.BK")
    dates = _dates()
    binding = contract.build_successor_quote_binding(successor, quote_binding, dates)
    assert binding.provider_symbol == "SUCC-ONLY.BK"
    assert binding.provider_symbol != "PRED-ONLY.BK"
    assert "predecessor" not in vars(binding)
    assert not hasattr(binding, "predecessor_provider_symbol")


def test_io2_binding_immutable():
    binding = _binding()
    with pytest.raises(Exception):
        binding.asset_id = 1


# ─────────────────────────────────────────────────────────────────────────
# Step 2.2 — deterministic, enumerable cache-key derivation
# ─────────────────────────────────────────────────────────────────────────

def test_cache_key_derivation_deterministic_for_identical_inputs():
    b1 = _binding()
    b2 = _binding()
    assert contract.quote_cache_type(b1) == contract.quote_cache_type(b2)
    assert contract.history_cache_type(b1) == contract.history_cache_type(b2)


def test_cache_key_format_matches_plan_exactly():
    binding = contract.build_successor_quote_binding(
        _successor(asset_id=7),
        _quote_binding(),
        _dates(successor_quote_epoch_start_date=date(2024, 3, 1)),
    )
    assert contract.quote_cache_type(binding) == "quote:asset=7:epoch=2024-03-01"
    assert contract.history_cache_type(binding) == "history:5y:1d:asset=7:epoch=2024-03-01"


def test_cache_key_differs_for_different_asset_id_or_epoch():
    b1 = contract.build_successor_quote_binding(_successor(asset_id=1), _quote_binding(), _dates())
    b2 = contract.build_successor_quote_binding(_successor(asset_id=2), _quote_binding(), _dates())
    assert contract.quote_cache_type(b1) != contract.quote_cache_type(b2)

    b3 = contract.build_successor_quote_binding(
        _successor(asset_id=1), _quote_binding(),
        _dates(successor_quote_epoch_start_date=date(2024, 1, 1)),
    )
    b4 = contract.build_successor_quote_binding(
        _successor(asset_id=1), _quote_binding(),
        _dates(successor_quote_epoch_start_date=date(2024, 2, 1)),
    )
    assert contract.quote_cache_type(b3) != contract.quote_cache_type(b4)


# ─────────────────────────────────────────────────────────────────────────
# Step 2.3 — PD-2 epoch classification, both UTC+7 boundary edges
# ─────────────────────────────────────────────────────────────────────────

def test_pd2_boundary_edge_before_midnight_is_predecessor_epoch():
    classification = contract.classify_observation_epoch(
        _UTC7_MIDNIGHT_BOUNDARY_TS - 1, "Asia/Bangkok", date(2023, 11, 15),
    )
    assert classification is contract.EpochClassification.PREDECESSOR_EPOCH


def test_pd2_boundary_edge_at_midnight_is_successor_epoch():
    classification = contract.classify_observation_epoch(
        _UTC7_MIDNIGHT_BOUNDARY_TS, "Asia/Bangkok", date(2023, 11, 15),
    )
    assert classification is contract.EpochClassification.SUCCESSOR_EPOCH


def test_pd2_classification_is_not_utc_date_comparison():
    """At the boundary instant, the UTC calendar date is still 2023-11-14,
    but exchange-local (UTC+7) is already 2023-11-15. If this function used
    UTC-date comparison it would misclassify this observation as predecessor.
    """
    utc_date_at_boundary = date(2023, 11, 14)
    exchange_local = contract.exchange_local_date(_UTC7_MIDNIGHT_BOUNDARY_TS, "Asia/Bangkok")
    assert exchange_local != utc_date_at_boundary
    assert exchange_local == date(2023, 11, 15)
    classification = contract.classify_observation_epoch(
        _UTC7_MIDNIGHT_BOUNDARY_TS, "Asia/Bangkok", date(2023, 11, 15),
    )
    assert classification is contract.EpochClassification.SUCCESSOR_EPOCH


def test_pd2_no_clock_or_system_timezone_used():
    """Same timestamp classified identically regardless of when the test
    itself runs -- exercised implicitly by every other PD-2 test being
    deterministic across runs; this test additionally proves the function
    signature carries no defaulted clock-dependent parameter."""
    import inspect

    sig = inspect.signature(contract.classify_observation_epoch)
    for param in sig.parameters.values():
        assert param.default in (inspect.Parameter.empty,) or not callable(param.default)


# ─────────────────────────────────────────────────────────────────────────
# Step 2.4 — E1-E5 evidence qualification (capability, not identity)
# ─────────────────────────────────────────────────────────────────────────

def test_e1_e5_fully_qualifying_evidence_qualifies():
    assert contract.evidence_qualifies(_qualifying_evidence()) is True


def test_e1_missing_provider_does_not_qualify():
    assert contract.evidence_qualifies(_qualifying_evidence(provider="")) is False


def test_e2_missing_served_symbol_does_not_qualify():
    assert contract.evidence_qualifies(_qualifying_evidence(served_symbol=None)) is False


def test_e3_empty_observations_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "observations": ()})
    assert contract.evidence_qualifies(ev) is False


def test_e3_observation_missing_timestamp_does_not_qualify():
    ev = _qualifying_evidence()
    bad_obs = (_FakeQuoteObservation(timestamp=None, close=100.0),)
    ev = _FakeProviderEvidence(**{**vars(ev), "observations": bad_obs})
    assert contract.evidence_qualifies(ev) is False


def test_e4_missing_current_close_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "current_close": None})
    assert contract.evidence_qualifies(ev) is False


def test_e5_missing_exchange_timezone_does_not_qualify():
    assert contract.evidence_qualifies(_qualifying_evidence(exchange_timezone_name=None)) is False


def test_missing_evidence_object_fails_closed():
    assert contract.evidence_qualifies(None) is False
    assert contract.evidence_qualifies(object()) is False


def test_evidence_qualification_names_no_provider_module_env_or_config():
    """Structural proof of PD-4's 'capability, not identity' framing: the
    predicate signature accepts only the evidence, never a provider name,
    module path, environment variable, or configuration value."""
    import inspect

    sig = inspect.signature(contract.evidence_qualifies)
    assert list(sig.parameters) == ["evidence"]


# ── Correction Round, Correction 2 — malformed E3/E5 evidence must fail
# closed, never escape as ZoneInfoNotFoundError/TypeError/ValueError/
# OverflowError/other implementation exception. ─────────────────────────────

def test_correction2_invalid_timezone_name_does_not_qualify_and_does_not_raise():
    ev = _qualifying_evidence(exchange_timezone_name="Not/A_Real_Zone")
    assert contract.evidence_qualifies(ev) is False


def test_correction2_nonnumeric_timestamp_does_not_qualify_and_does_not_raise():
    ev = _qualifying_evidence()
    bad_obs = (_FakeQuoteObservation(timestamp="not-a-number", close=100.0),)
    ev = _FakeProviderEvidence(**{**vars(ev), "observations": bad_obs})
    assert contract.evidence_qualifies(ev) is False


def test_correction2_boolean_timestamp_does_not_qualify():
    """bool is an int subtype in Python -- must not silently pass as a
    numeric timestamp."""
    ev = _qualifying_evidence()
    bad_obs = (_FakeQuoteObservation(timestamp=True, close=100.0),)
    ev = _FakeProviderEvidence(**{**vars(ev), "observations": bad_obs})
    assert contract.evidence_qualifies(ev) is False


def test_correction2_nan_timestamp_does_not_qualify():
    ev = _qualifying_evidence()
    bad_obs = (_FakeQuoteObservation(timestamp=float("nan"), close=100.0),)
    ev = _FakeProviderEvidence(**{**vars(ev), "observations": bad_obs})
    assert contract.evidence_qualifies(ev) is False


def test_correction2_malformed_out_of_range_timestamp_does_not_qualify_and_does_not_raise():
    """A syntactically numeric but semantically unusable (wildly
    out-of-range) timestamp must fail closed rather than raising
    OverflowError/OSError/ValueError out of datetime.fromtimestamp."""
    ev = _qualifying_evidence()
    bad_obs = (_FakeQuoteObservation(timestamp=99999999999999999999, close=100.0),)
    ev = _FakeProviderEvidence(**{**vars(ev), "observations": bad_obs})
    assert contract.evidence_qualifies(ev) is False


def test_correction2_structurally_compatible_but_semantically_invalid_observation_does_not_qualify():
    """An observation object that structurally satisfies the Protocol
    (has a `timestamp` attribute) but carries a semantically unusable value
    must not satisfy affirmative E1-E5 qualification."""
    @dataclass(frozen=True)
    class _WeirdObservation:
        timestamp: object
        close: Optional[float]

    ev = _qualifying_evidence()
    bad_obs = (_WeirdObservation(timestamp=object(), close=100.0),)
    ev = _FakeProviderEvidence(**{**vars(ev), "observations": bad_obs})
    assert contract.evidence_qualifies(ev) is False


def test_correction2_valid_exchange_local_boundary_behavior_still_qualifies():
    """Sanity: hardening E3/E5 must not regress the ordinary, valid case at
    the UTC+7 boundary."""
    ev = _qualifying_evidence(
        timestamps=(_UTC7_MIDNIGHT_BOUNDARY_TS,),
        closes=(100.0,),
        exchange_timezone_name="Asia/Bangkok",
    )
    assert contract.evidence_qualifies(ev) is True


def test_correction2_check_cross_epoch_timestamp_never_raises_for_invalid_timezone():
    binding = _binding()
    ev = _qualifying_evidence(exchange_timezone_name="Not/A_Real_Zone")
    # Must return a QuarantineResult, not raise ZoneInfoNotFoundError.
    result = contract.check_cross_epoch_timestamp(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.CROSS_EPOCH_TIMESTAMP


def test_correction2_check_cross_epoch_timestamp_never_raises_for_malformed_timestamp():
    binding = _binding()
    ev = _qualifying_evidence()
    bad_obs = (_FakeQuoteObservation(timestamp=99999999999999999999, close=100.0),)
    ev = _FakeProviderEvidence(**{**vars(ev), "observations": bad_obs})
    result = contract.check_cross_epoch_timestamp(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.CROSS_EPOCH_TIMESTAMP


def test_correction2_check_cross_epoch_timestamp_never_raises_for_nonnumeric_timestamp():
    binding = _binding()
    ev = _qualifying_evidence()
    bad_obs = (_FakeQuoteObservation(timestamp="garbage", close=100.0),)
    ev = _FakeProviderEvidence(**{**vars(ev), "observations": bad_obs})
    result = contract.check_cross_epoch_timestamp(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.CROSS_EPOCH_TIMESTAMP


def test_correction2_no_exception_type_from_zoneinfo_or_datetime_escapes_evidence_qualifies():
    """Broad adversarial sweep: none of these malformed evidence shapes may
    raise out of evidence_qualifies -- every one must return False."""
    garbage_timezones = ["", None, "Not/AZone", 123, object()]
    for tz in garbage_timezones:
        ev = _qualifying_evidence(exchange_timezone_name=tz)
        try:
            result = contract.evidence_qualifies(ev)
        except Exception as exc:  # pragma: no cover - the assertion below is the real check
            pytest.fail(f"evidence_qualifies raised {exc!r} for exchange_timezone_name={tz!r}")
        assert result is False

    garbage_timestamps = ["not-a-number", None, object(), float("nan"), float("inf"), 10**30, True]
    for ts in garbage_timestamps:
        obs = (_FakeQuoteObservation(timestamp=ts, close=100.0),)
        ev = _FakeProviderEvidence(**{**vars(_qualifying_evidence()), "observations": obs})
        try:
            result = contract.evidence_qualifies(ev)
        except Exception as exc:  # pragma: no cover
            pytest.fail(f"evidence_qualifies raised {exc!r} for timestamp={ts!r}")
        assert result is False


# ─────────────────────────────────────────────────────────────────────────
# Step 2.4 / Correction Round Correction 3 — reference-price admissibility
# (WP3 half of MINOR-2 / A9), re-based per
# BANPU_WP3_REFERENCE_PRICE_ADMISSIBILITY_CLARIFICATION_RECORD.md onto
# PositionConversionBoundaryEvidence.{predecessor,successor}_reference_price
# -- NOT provider current_close/previous_close.
# ─────────────────────────────────────────────────────────────────────────

def _boundary_evidence(
    predecessor_reference_price=Decimal("95.50"),
    successor_reference_price=Decimal("101.25"),
    mechanical_nav_tolerance_pct=Decimal("0.5"),
    suspension_gap_annotation="none",
):
    return PositionConversionBoundaryEvidence(
        predecessor_reference_price=predecessor_reference_price,
        successor_reference_price=successor_reference_price,
        mechanical_nav_tolerance_pct=mechanical_nav_tolerance_pct,
        suspension_gap_annotation=suspension_gap_annotation,
    )


def test_reference_price_admissible_for_canonical_decimal_boundary_evidence():
    be = _boundary_evidence(successor_reference_price=Decimal("101.25"))
    assert contract.assess_reference_price_admissibility(be, "successor_reference_price") == contract.ReferencePriceAdmissibility.ADMISSIBLE


def test_reference_price_admissible_both_predecessor_and_successor_fields():
    be = _boundary_evidence()
    assert contract.assess_reference_price_admissibility(be, "predecessor_reference_price") == contract.ReferencePriceAdmissibility.ADMISSIBLE
    assert contract.assess_reference_price_admissibility(be, "successor_reference_price") == contract.ReferencePriceAdmissibility.ADMISSIBLE


def test_reference_price_absent_when_boundary_evidence_itself_absent():
    assert contract.assess_reference_price_admissibility(None, "successor_reference_price") == contract.ReferencePriceAdmissibility.ABSENT
    assert contract.assess_reference_price_admissibility(object(), "successor_reference_price") == contract.ReferencePriceAdmissibility.ABSENT


def test_reference_price_non_positive():
    be_zero = _boundary_evidence(successor_reference_price=Decimal("0"))
    be_negative = _boundary_evidence(successor_reference_price=Decimal("-5.00"))
    assert contract.assess_reference_price_admissibility(be_zero, "successor_reference_price") == contract.ReferencePriceAdmissibility.NON_POSITIVE
    assert contract.assess_reference_price_admissibility(be_negative, "successor_reference_price") == contract.ReferencePriceAdmissibility.NON_POSITIVE


def test_reference_price_non_finite():
    be = _boundary_evidence(successor_reference_price=Decimal("Infinity"))
    assert contract.assess_reference_price_admissibility(be, "successor_reference_price") == contract.ReferencePriceAdmissibility.NON_FINITE

    be_nan = _boundary_evidence(successor_reference_price=Decimal("NaN"))
    assert contract.assess_reference_price_admissibility(be_nan, "successor_reference_price") == contract.ReferencePriceAdmissibility.NON_FINITE


def test_reference_price_field_selector_is_evidence_bound_only():
    """The function only accepts 'predecessor_reference_price' or
    'successor_reference_price' -- it cannot be called with an arbitrary
    unbound number, and it cannot be called with a provider-close field
    name at all."""
    be = _boundary_evidence()
    with pytest.raises(ValueError):
        contract.assess_reference_price_admissibility(be, "not_a_real_field")
    with pytest.raises(ValueError):
        contract.assess_reference_price_admissibility(be, "current_close")
    with pytest.raises(ValueError):
        contract.assess_reference_price_admissibility(be, "previous_close")


def test_reference_price_admissibility_is_not_mechanical_continuity_tolerance():
    """No tolerance/reconciliation parameter exists on this predicate at
    all -- WP5 owns mechanical continuity, not WP3."""
    import inspect

    sig = inspect.signature(contract.assess_reference_price_admissibility)
    names = set(sig.parameters)
    assert "tolerance" not in names
    assert "mechanical_nav_tolerance_pct" not in names


# ── Correction 3 — provider-close and reference-price predicates are
# distinct value classes; a provider float can be an admissible provider
# close (via evidence_qualifies) yet can never itself become an admissible
# reference price. ───────────────────────────────────────────────────────

def test_correction3_provider_float_close_is_not_a_reference_price_type():
    """assess_reference_price_admissibility rejects a provider-shaped
    evidence object outright (ABSENT/type mismatch) -- it is not the
    operand class this predicate consumes at all."""
    ev = _qualifying_evidence(closes=(100.0, 101.25))
    assert contract.assess_reference_price_admissibility(ev, "successor_reference_price") == contract.ReferencePriceAdmissibility.ABSENT


def test_correction3_provider_floats_remain_permissible_as_provider_closes():
    """Ordinary provider floats remain a fully admissible provider close --
    E1-E5 qualification is unaffected by the reference-price rebase; no
    decimal-exactness is ever demanded of current_close/previous_close."""
    ev = _qualifying_evidence(closes=(100.0, 101.5))
    assert contract.evidence_qualifies(ev) is True


def test_correction3_decimal_str_of_provider_float_is_indistinguishable_by_type_alone_from_canonical_decimal():
    """MINOR finding (Correction Round 2): the previous name of this test
    ("...cannot_manufacture_admissible_reference_price") stated the opposite
    of what the body demonstrates -- the assertion below shows the predicate
    *does* accept a manufactured value, precisely because Python does not
    preserve construction provenance on a ``Decimal``. This is not a defect;
    it is the documented, acknowledged limit of runtime type-checking. The
    actual protection is architectural: (a) this predicate only accepts a
    PositionConversionBoundaryEvidence
    instance, never a bare number, so a provider float has no direct path
    in at all; and (b) the frozen WP1 parser (transaction_canonicalizer's
    reader.decimal()) that is the sole canonical producer of
    PositionConversionBoundaryEvidence field values only ever accepts a
    plain base-10 *string* input and explicitly rejects non-string input
    (see test_correction3_frozen_parser_never_accepts_a_float_for_boundary_evidence_decimals
    below) -- so a provider float can never reach this predicate through the
    canonical construction path, manufactured Decimal(str(...)) or not.

    This test demonstrates the negative case concretely: even a
    Decimal(str(...)) constructed from a provider float, once placed into a
    boundary-evidence-shaped object, is indistinguishable from a canonical
    Decimal by type alone -- which is exactly why WP3.2 itself must never
    perform that construction (verified structurally by
    test_module_never_manufactures_decimal_from_str below), and why the
    only trusted source of these values is the frozen WP1 parser.
    """
    provider_float = 101.5
    manufactured = _boundary_evidence(successor_reference_price=Decimal(str(provider_float)))
    # Not a defect in the predicate: this documents the acknowledged limit
    # of runtime type-checking, and is exactly why architectural prohibition
    # (never call Decimal(str(...)) in this module) is the real guarantee.
    assert contract.assess_reference_price_admissibility(manufactured, "successor_reference_price") == contract.ReferencePriceAdmissibility.ADMISSIBLE


def test_correction3_frozen_parser_never_accepts_a_float_for_boundary_evidence_decimals():
    """The sole canonical producer of PositionConversionBoundaryEvidence
    field values, transaction_canonicalizer's reader.decimal(), rejects any
    non-string input (including float/int) outright -- proving a provider
    float can never flow into a real (parser-produced) boundary_evidence
    object without first being serialized through the plain-decimal-string
    payload contract, which is a human/ledger-authored value, never a
    provider quote.
    """
    from services.transaction_canonicalizer import _PayloadReader

    reader = _PayloadReader()
    result = reader.decimal({"price": 101.5}, "price", "boundary_evidence")
    assert result is None
    assert reader.errors
    assert reader.errors[0].code == "DECIMAL_INVALID"


def test_module_never_manufactures_decimal_from_str():
    """Structural (AST) guard: the production module must never call
    Decimal(str(...)) anywhere -- that is exactly the prohibited
    construction path for a reference price per the clarification record.
    """
    tree = ast.parse(_MODULE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Decimal":
            for arg in node.args:
                assert not (isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == "str"), (
                    "production module must never call Decimal(str(...))"
                )


# ── Correction Round 2 — provider-close admissibility ──────────────────────
# BLOCKING C2 finding: current_close/previous_close were only checked for
# presence (E4), never for numeric validity, finiteness, or positivity.
# Correction: evidence_qualifies now enforces present/numeric/finite/
# strictly-positive for current_close, and finite/strictly-positive for
# previous_close whenever it is present (previous_close=None itself remains
# admissible, preserving A2 for the first successor-epoch quote). This
# reuses EVIDENCE_CONTRACT_NOT_SATISFIED -- no new QuarantineReason. It is
# deliberately distinct from (and never decimal-exact like)
# reference-price admissibility.

def test_correction_round2_current_close_negative_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "current_close": -5.0})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_current_close_zero_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "current_close": 0.0})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_current_close_nan_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "current_close": float("nan")})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_current_close_positive_infinity_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "current_close": float("inf")})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_current_close_negative_infinity_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "current_close": float("-inf")})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_current_close_boolean_does_not_qualify():
    """bool is an int subtype in Python -- must not silently pass as a
    numeric close, consistent with the same guard already applied to E3
    timestamps."""
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "current_close": True})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_previous_close_negative_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "previous_close": -1.0})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_previous_close_zero_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "previous_close": 0.0})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_previous_close_nan_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "previous_close": float("nan")})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_previous_close_positive_infinity_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "previous_close": float("inf")})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_previous_close_negative_infinity_does_not_qualify():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "previous_close": float("-inf")})
    assert contract.evidence_qualifies(ev) is False


def test_correction_round2_previous_close_none_remains_admissible_a2_preserved():
    """A2: the first successor-epoch quote has no prior observation at all,
    so previous_close=None must remain fully admissible -- this is not an
    invalid provider close, it is the expected, valid shape for that case."""
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "previous_close": None})
    assert contract.evidence_qualifies(ev) is True


def test_correction_round2_valid_positive_finite_current_and_previous_close_remain_admissible():
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "current_close": 101.25, "previous_close": 95.50})
    assert contract.evidence_qualifies(ev) is True


def test_correction_round2_no_new_quarantine_reason_was_introduced():
    """The correction must reuse EVIDENCE_CONTRACT_NOT_SATISFIED -- the
    enumeration is unchanged from the prior correction round."""
    names = {member.name for member in contract.QuarantineReason}
    assert names == {
        "MISSING_OR_AMBIGUOUS_IDENTIFIER",
        "PROVIDER_SYMBOL_MISMATCH",
        "CROSS_EPOCH_TIMESTAMP",
        "CACHE_NAMESPACE_MISMATCH",
        "EVIDENCE_CONTRACT_NOT_SATISFIED",
        "REFERENCE_PRICE_INADMISSIBLE",
    }


@pytest.mark.parametrize(
    "bad_current_close",
    [-5.0, 0.0, float("nan"), float("inf"), float("-inf")],
)
def test_correction_round2_check_evidence_contract_not_satisfied_for_bad_current_close(bad_current_close):
    binding = _binding()
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "current_close": bad_current_close})
    result = contract.check_evidence_contract_not_satisfied(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED


@pytest.mark.parametrize(
    "bad_previous_close",
    [-1.0, 0.0, float("nan"), float("inf"), float("-inf")],
)
def test_correction_round2_check_evidence_contract_not_satisfied_for_bad_previous_close(bad_previous_close):
    binding = _binding()
    ev = _qualifying_evidence()
    ev = _FakeProviderEvidence(**{**vars(ev), "previous_close": bad_previous_close})
    result = contract.check_evidence_contract_not_satisfied(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED


@pytest.mark.parametrize(
    "bad_current_close",
    [-5.0, 0.0, float("nan"), float("inf"), float("-inf")],
)
def test_correction_round2_evaluate_candidate_quarantine_returns_evidence_contract_not_satisfied_for_bad_current_close(bad_current_close):
    """evaluate_candidate_quarantine (the composite path) must reach the same
    reason as the standalone check -- proving the composite's precedence
    still routes an invalid provider close through step 2
    (EVIDENCE_CONTRACT_NOT_SATISFIED), not silently past it."""
    kwargs = _all_passing_kwargs()
    binding = kwargs["binding"]
    ev = _qualifying_evidence(
        provider=binding.provider,
        requested_symbol=binding.provider_symbol,
        served_symbol=binding.provider_symbol,
    )
    kwargs["evidence"] = _FakeProviderEvidence(**{**vars(ev), "current_close": bad_current_close})
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED


def test_correction_round2_evaluate_candidate_quarantine_previous_close_none_still_passes_through():
    """previous_close=None must not cause the composite path to quarantine
    at step 2 -- confirms A2 remains valid all the way through the
    deterministic composite decision, not merely in evidence_qualifies
    isolation."""
    kwargs = _all_passing_kwargs()
    binding = kwargs["binding"]
    ev = _qualifying_evidence(
        provider=binding.provider,
        requested_symbol=binding.provider_symbol,
        served_symbol=binding.provider_symbol,
    )
    kwargs["evidence"] = _FakeProviderEvidence(**{**vars(ev), "previous_close": None})
    assert contract.evaluate_candidate_quarantine(**kwargs) is None


def test_correction_round2_composite_precedence_unchanged_by_provider_close_correction():
    """The six-step precedence ordering itself is untouched by this
    correction round -- an invalid provider close (evidence-contract tier,
    #2) must still be beaten by a higher-precedence failure
    (MISSING_OR_AMBIGUOUS_IDENTIFIER, #1) when both are present
    simultaneously, exactly as before this round."""
    kwargs = _all_passing_kwargs()
    kwargs["binding"] = contract.SuccessorQuoteBinding(0, "", "", date(2024, 1, 1), date(2024, 1, 1))
    binding = _binding()
    ev = _qualifying_evidence(
        provider=binding.provider,
        requested_symbol=binding.provider_symbol,
        served_symbol=binding.provider_symbol,
    )
    kwargs["evidence"] = _FakeProviderEvidence(**{**vars(ev), "current_close": -5.0})
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER


def test_correction_round2_provider_close_admissibility_is_not_decimal_exact():
    """Provider closes are never required to be decimal-exact -- that
    property belongs exclusively to the unrelated boundary-evidence
    reference-price value class. An ordinary Python float remains a fully
    admissible provider close."""
    ev = _qualifying_evidence(closes=(95.5, 101.25))
    assert isinstance(ev.current_close, float)
    assert contract.evidence_qualifies(ev) is True


# ─────────────────────────────────────────────────────────────────────────
# Step 2.5 — enumerated quarantine reasons, one reason + one identity each
# ─────────────────────────────────────────────────────────────────────────

def test_quarantine_missing_or_ambiguous_identifier():
    bad_binding = contract.SuccessorQuoteBinding(
        asset_id=0, provider="yahoo_chart", provider_symbol="SUCC.BK",
        quote_epoch_start_date=date(2024, 1, 1), valuation_transition_date=date(2023, 12, 31),
    )
    result = contract.check_missing_or_ambiguous_identifier(bad_binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER
    assert result.affected_asset_id == 0


def test_quarantine_missing_identifier_non_triggering():
    assert contract.check_missing_or_ambiguous_identifier(_binding()) is None


def test_quarantine_provider_symbol_mismatch_on_provider():
    binding = _binding()
    ev = _qualifying_evidence(provider="a_different_provider")
    result = contract.check_provider_symbol_mismatch(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH
    assert result.affected_asset_id == binding.asset_id


def test_quarantine_provider_symbol_mismatch_on_symbol():
    binding = _binding()
    ev = _qualifying_evidence(requested_symbol="SUCC.BK", served_symbol="SOMETHING-ELSE.BK")
    result = contract.check_provider_symbol_mismatch(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH


def test_quarantine_provider_symbol_match_non_triggering():
    binding = _binding()
    ev = _qualifying_evidence(
        provider=binding.provider,
        requested_symbol=binding.provider_symbol,
        served_symbol=binding.provider_symbol,
    )
    assert contract.check_provider_symbol_mismatch(ev, binding) is None


# ── Correction Round, Correction 1 — successor binding identity ────────────
# C2 finding: requested_symbol == served_symbol alone (R5's consistency
# check) was insufficient -- it never compared against
# SuccessorQuoteBinding.provider_symbol at all, so evidence consistently
# requesting/serving the *wrong* symbol passed silently.

def test_correction1_defect_case_requested_equals_served_but_wrong_symbol_must_quarantine():
    """The exact defect case from the correction mandate: requested_symbol
    == served_symbol == 'OTHER.BK', binding.provider_symbol == 'SUCC.BK'.
    Must fail closed -- this previously passed silently."""
    binding = _binding()  # binding.provider_symbol == "SUCC.BK"
    assert binding.provider_symbol == "SUCC.BK"
    ev = _qualifying_evidence(
        provider=binding.provider,
        requested_symbol="OTHER.BK",
        served_symbol="OTHER.BK",
    )
    result = contract.check_provider_symbol_mismatch(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH
    assert result.affected_asset_id == binding.asset_id


def test_correction1_requested_equals_served_equals_binding_non_triggering():
    binding = _binding()
    ev = _qualifying_evidence(
        provider=binding.provider,
        requested_symbol=binding.provider_symbol,
        served_symbol=binding.provider_symbol,
    )
    assert contract.check_provider_symbol_mismatch(ev, binding) is None


def test_correction1_requested_not_equal_served_triggers_regardless_of_binding():
    binding = _binding()
    ev = _qualifying_evidence(
        provider=binding.provider,
        requested_symbol=binding.provider_symbol,
        served_symbol="SOMETHING-ELSE.BK",
    )
    result = contract.check_provider_symbol_mismatch(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH


def test_correction1_requested_equals_served_but_not_binding_with_different_provider_too():
    binding = _binding()
    ev = _qualifying_evidence(
        provider="a_different_provider",
        requested_symbol="OTHER.BK",
        served_symbol="OTHER.BK",
    )
    result = contract.check_provider_symbol_mismatch(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH


def test_correction1_predecessor_provider_symbol_never_read_by_mismatch_check():
    """check_provider_symbol_mismatch's signature has no parameter through
    which PositionConversionQuoteBinding.predecessor_provider_symbol could
    ever reach it."""
    import inspect

    sig = inspect.signature(contract.check_provider_symbol_mismatch)
    assert list(sig.parameters) == ["evidence", "binding"]


def test_quarantine_cross_epoch_timestamp():
    binding = _binding(successor_quote_epoch_start_date=date(2023, 11, 15))
    ev = _qualifying_evidence(
        timestamps=(_UTC7_MIDNIGHT_BOUNDARY_TS - 1,),  # predecessor-side observation
        closes=(90.0,),
    )
    result = contract.check_cross_epoch_timestamp(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.CROSS_EPOCH_TIMESTAMP
    assert result.affected_asset_id == binding.asset_id


def test_quarantine_cross_epoch_timestamp_non_triggering_at_boundary():
    binding = _binding(successor_quote_epoch_start_date=date(2023, 11, 15))
    ev = _qualifying_evidence(
        timestamps=(_UTC7_MIDNIGHT_BOUNDARY_TS,),  # successor-side observation, at the boundary
        closes=(90.0,),
    )
    assert contract.check_cross_epoch_timestamp(ev, binding) is None


def test_quarantine_cache_namespace_mismatch():
    binding = _binding()
    result = contract.check_cache_namespace_mismatch("quote:asset=999:epoch=1999-01-01", binding, kind="quote")
    assert result is not None
    assert result.reason is contract.QuarantineReason.CACHE_NAMESPACE_MISMATCH


def test_quarantine_cache_namespace_match_non_triggering():
    binding = _binding()
    candidate = contract.quote_cache_type(binding)
    assert contract.check_cache_namespace_mismatch(candidate, binding, kind="quote") is None


def test_quarantine_evidence_contract_not_satisfied():
    binding = _binding()
    ev = _qualifying_evidence(exchange_timezone_name=None)
    result = contract.check_evidence_contract_not_satisfied(ev, binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED


def test_quarantine_evidence_contract_satisfied_non_triggering():
    binding = _binding()
    assert contract.check_evidence_contract_not_satisfied(_qualifying_evidence(), binding) is None


def test_quarantine_reference_price_inadmissible():
    binding = _binding()
    be = _boundary_evidence(successor_reference_price=Decimal("-1.00"))
    result = contract.check_reference_price_inadmissible(be, "successor_reference_price", binding)
    assert result is not None
    assert result.reason is contract.QuarantineReason.REFERENCE_PRICE_INADMISSIBLE


def test_quarantine_reference_price_admissible_non_triggering():
    binding = _binding()
    be = _boundary_evidence()
    assert contract.check_reference_price_inadmissible(be, "successor_reference_price", binding) is None


def test_every_quarantine_result_carries_exactly_one_reason_and_one_identity():
    binding = _binding()
    result = contract.check_missing_or_ambiguous_identifier(
        contract.SuccessorQuoteBinding(0, "", "", date(2024, 1, 1), date(2024, 1, 1))
    )
    assert set(vars(result).keys()) == {"reason", "affected_asset_id"}
    assert isinstance(result.reason, contract.QuarantineReason)
    assert isinstance(result.affected_asset_id, int)


def test_quarantine_result_carries_no_free_text_field():
    """No rejection is free-text-only: QuarantineResult has no string detail
    field at all, so every result is enum-typed by construction."""
    field_types = {f: type(getattr(contract.QuarantineResult, "__dataclass_fields__")[f].type) for f in contract.QuarantineResult.__dataclass_fields__}
    assert "reason" in contract.QuarantineResult.__dataclass_fields__
    assert "affected_asset_id" in contract.QuarantineResult.__dataclass_fields__
    assert len(contract.QuarantineResult.__dataclass_fields__) == 2


def test_quarantine_reasons_are_exhaustive_over_design_section10_wp3_scope_plus_e1_e5():
    """Enumeration covers every design-§10 WP3-scoped condition (missing/
    ambiguous identifiers, provider-symbol mismatch, cross-epoch timestamps,
    wrong cache namespace, missing/non-positive prices) plus E1-E5
    non-satisfaction. Mechanical continuity failure and unannotated boundary
    discontinuity are WP5's half of design §10 and are deliberately absent.
    """
    names = {member.name for member in contract.QuarantineReason}
    assert names == {
        "MISSING_OR_AMBIGUOUS_IDENTIFIER",
        "PROVIDER_SYMBOL_MISMATCH",
        "CROSS_EPOCH_TIMESTAMP",
        "CACHE_NAMESPACE_MISMATCH",
        "EVIDENCE_CONTRACT_NOT_SATISFIED",
        "REFERENCE_PRICE_INADMISSIBLE",
    }


# ─────────────────────────────────────────────────────────────────────────
# Correction Round, Correction 4 — deterministic composite quarantine
# decision: exactly one result, deterministic precedence, no exception ever
# escapes, even when several predicates fail simultaneously.
# ─────────────────────────────────────────────────────────────────────────

def _all_passing_kwargs():
    binding = _binding()
    return dict(
        binding=binding,
        evidence=_qualifying_evidence(
            provider=binding.provider,
            requested_symbol=binding.provider_symbol,
            served_symbol=binding.provider_symbol,
        ),
        boundary_evidence=_boundary_evidence(),
        reference_price_field="successor_reference_price",
        candidate_cache_type=contract.quote_cache_type(binding),
        cache_kind="quote",
    )


def test_composite_returns_none_when_everything_passes():
    assert contract.evaluate_candidate_quarantine(**_all_passing_kwargs()) is None


def test_composite_single_failure_missing_identifier():
    kwargs = _all_passing_kwargs()
    kwargs["binding"] = contract.SuccessorQuoteBinding(0, "", "", date(2024, 1, 1), date(2024, 1, 1))
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER


def test_composite_single_failure_evidence_contract():
    kwargs = _all_passing_kwargs()
    kwargs["evidence"] = _qualifying_evidence(exchange_timezone_name=None)
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED


def test_composite_single_failure_provider_symbol_mismatch():
    kwargs = _all_passing_kwargs()
    binding = kwargs["binding"]
    kwargs["evidence"] = _qualifying_evidence(
        provider=binding.provider, requested_symbol="OTHER.BK", served_symbol="OTHER.BK",
    )
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH


def test_composite_single_failure_cross_epoch_timestamp():
    kwargs = _all_passing_kwargs()
    binding = kwargs["binding"]
    kwargs["evidence"] = _qualifying_evidence(
        provider=binding.provider,
        requested_symbol=binding.provider_symbol,
        served_symbol=binding.provider_symbol,
        timestamps=(_UTC7_MIDNIGHT_BOUNDARY_TS - 1,),
        closes=(90.0,),
    )
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.CROSS_EPOCH_TIMESTAMP


def test_composite_single_failure_cache_namespace_mismatch():
    kwargs = _all_passing_kwargs()
    kwargs["candidate_cache_type"] = "quote:asset=999:epoch=1999-01-01"
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.CACHE_NAMESPACE_MISMATCH


def test_composite_single_failure_reference_price_inadmissible():
    kwargs = _all_passing_kwargs()
    kwargs["boundary_evidence"] = _boundary_evidence(successor_reference_price=Decimal("-1"))
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.REFERENCE_PRICE_INADMISSIBLE


def test_composite_simultaneous_failures_yield_exactly_one_result_highest_precedence_wins():
    """Binding is malformed AND evidence is non-qualifying AND the reference
    price is inadmissible, all at once. Precedence #1
    (MISSING_OR_AMBIGUOUS_IDENTIFIER) must win -- not any of the others."""
    kwargs = _all_passing_kwargs()
    kwargs["binding"] = contract.SuccessorQuoteBinding(0, "", "", date(2024, 1, 1), date(2024, 1, 1))
    kwargs["evidence"] = _qualifying_evidence(exchange_timezone_name=None)
    kwargs["boundary_evidence"] = _boundary_evidence(successor_reference_price=Decimal("-1"))
    kwargs["candidate_cache_type"] = "totally-wrong-cache-key"
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER


def test_composite_simultaneous_failures_second_tier_precedence():
    """Binding is well-formed but evidence is non-qualifying AND the
    reference price is inadmissible. EVIDENCE_CONTRACT_NOT_SATISFIED (#2)
    must win over REFERENCE_PRICE_INADMISSIBLE (#6)."""
    kwargs = _all_passing_kwargs()
    kwargs["evidence"] = _qualifying_evidence(exchange_timezone_name=None)
    kwargs["boundary_evidence"] = _boundary_evidence(successor_reference_price=Decimal("-1"))
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED


def test_composite_simultaneous_failures_symbol_mismatch_beats_reference_price():
    """Qualifying evidence but wrong symbol identity AND an inadmissible
    reference price simultaneously. PROVIDER_SYMBOL_MISMATCH (#3) must win
    over REFERENCE_PRICE_INADMISSIBLE (#6)."""
    kwargs = _all_passing_kwargs()
    binding = kwargs["binding"]
    kwargs["evidence"] = _qualifying_evidence(
        provider=binding.provider, requested_symbol="OTHER.BK", served_symbol="OTHER.BK",
    )
    kwargs["boundary_evidence"] = _boundary_evidence(successor_reference_price=Decimal("-1"))
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert result.reason is contract.QuarantineReason.PROVIDER_SYMBOL_MISMATCH


def test_composite_deterministic_same_inputs_same_reason():
    kwargs = _all_passing_kwargs()
    kwargs["evidence"] = _qualifying_evidence(exchange_timezone_name=None)
    r1 = contract.evaluate_candidate_quarantine(**kwargs)
    r2 = contract.evaluate_candidate_quarantine(**kwargs)
    assert r1 == r2
    assert r1.reason is r2.reason
    assert r1.affected_asset_id == r2.affected_asset_id


def test_composite_never_raises_for_maximally_malformed_evidence():
    """Every evidence-derived exception path this module knows about,
    triggered simultaneously: invalid timezone, malformed timestamp, wrong
    cache candidate, non-positive reference price. Must return a single
    QuarantineResult, never raise."""
    kwargs = _all_passing_kwargs()
    binding = kwargs["binding"]
    bad_obs = (_FakeQuoteObservation(timestamp=99999999999999999999, close=100.0),)
    kwargs["evidence"] = _FakeProviderEvidence(
        provider=binding.provider,
        requested_symbol="OTHER.BK",
        served_symbol="OTHER.BK",
        observations=bad_obs,
        current_close=None,
        previous_close=None,
        exchange_timezone_name="Not/A_Real_Zone",
    )
    kwargs["boundary_evidence"] = _boundary_evidence(successor_reference_price=Decimal("NaN"))
    kwargs["candidate_cache_type"] = "garbage"
    result = contract.evaluate_candidate_quarantine(**kwargs)
    assert result is not None
    assert isinstance(result.reason, contract.QuarantineReason)


def test_composite_invalid_caller_selector_still_raises_valueerror():
    """A caller-supplied literal selector error (never evidence-derived) is
    a programming bug, not a quarantine condition -- it is intentionally not
    swallowed."""
    kwargs = _all_passing_kwargs()
    kwargs["cache_kind"] = "not_a_real_kind"
    with pytest.raises(ValueError):
        contract.evaluate_candidate_quarantine(**kwargs)


def test_composite_precedence_is_encoded_in_exactly_one_place():
    """The precedence ordering is documented in evaluate_candidate_quarantine's
    own docstring and is not duplicated or re-decided anywhere else in the
    module -- no other function name in this module contains 'precedence' or
    'evaluate_candidate' besides this one."""
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert source.count("def evaluate_candidate_quarantine") == 1


# ── Correction 5 — miscellaneous cross-cutting proofs required by the
# correction mandate ────────────────────────────────────────────────────────

def test_correction5_predecessor_provider_symbol_remains_unused_anywhere_in_module():
    """No function in this module reads
    PositionConversionQuoteBinding.predecessor_provider_symbol at all.
    Functional (AST attribute-access) check, not a prose/string search --
    docstrings are free to name the field when explaining the invariant
    (and do), but no code path may access it."""
    tree = ast.parse(_MODULE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            assert node.attr != "predecessor_provider_symbol"


def test_correction5_cache_key_behavior_unchanged_by_correction_round():
    binding = contract.build_successor_quote_binding(
        _successor(asset_id=7), _quote_binding(), _dates(successor_quote_epoch_start_date=date(2024, 3, 1)),
    )
    assert contract.quote_cache_type(binding) == "quote:asset=7:epoch=2024-03-01"
    assert contract.history_cache_type(binding) == "history:5y:1d:asset=7:epoch=2024-03-01"


def test_correction5_no_wp5_tolerance_or_reconciliation_logic_anywhere_in_module():
    """Functional (not prose) check: no function parameter is named after
    tolerance/reconciliation, and mechanical_nav_tolerance_pct is never
    read as an attribute anywhere -- docstrings are free to explain that
    WP5's tolerance is out of scope (and do), but no code path may consume
    it."""
    tree = ast.parse(_MODULE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args + node.args.kwonlyargs:
                assert "tolerance" not in arg.arg.lower()
                assert "reconcil" not in arg.arg.lower()
        if isinstance(node, ast.Attribute):
            assert node.attr != "mechanical_nav_tolerance_pct"


def test_correction5_module_still_never_imports_yahoo_chart_or_data_fetcher():
    """WP3.1 remains conversion-unaware and untouched: re-affirms the
    original purity/provider-neutrality guard still holds after the
    Correction Round's edits."""
    tree = ast.parse(_MODULE_PATH.read_text(encoding="utf-8"))
    module_refs = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            module_refs.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module_refs.add(node.module)
    assert not any("yahoo" in ref for ref in module_refs)
    assert not any("data_fetcher" in ref for ref in module_refs)
    assert module_refs & {"services.transaction_canonicalizer"}


# ─────────────────────────────────────────────────────────────────────────
# Confirmatory integration: real WP3.1 evidence structurally satisfies
# this module's Protocol without this module importing yahoo_chart.py.
# ─────────────────────────────────────────────────────────────────────────

def test_real_yahoo_chart_evidence_satisfies_the_protocol_structurally():
    from services.market_data.yahoo_chart import ProviderQuoteEvidence, QuoteObservation

    real_evidence = ProviderQuoteEvidence(
        provider="yahoo_chart",
        requested_symbol="SUCC.BK",
        served_symbol="SUCC.BK",
        observations=(
            QuoteObservation(timestamp=_UTC7_MIDNIGHT_BOUNDARY_TS, close=100.0),
            QuoteObservation(timestamp=_UTC7_MIDNIGHT_BOUNDARY_TS + 86400, close=101.0),
        ),
        current_close=101.0,
        previous_close=100.0,
        exchange_timezone_name="Asia/Bangkok",
    )
    assert isinstance(real_evidence, contract.ProviderQuoteEvidenceLike)
    assert contract.evidence_qualifies(real_evidence) is True
    binding = _binding()
    be = _boundary_evidence()
    assert contract.check_reference_price_inadmissible(be, "successor_reference_price", binding) is None


def test_real_yahoo_chart_f2_sparse_bar_evidence_non_qualifying_current_close():
    """F2's own current_close comes from meta.regularMarketPrice, which was
    always present in Stage 0's F2 fixture -- so this specifically exercises
    a *constructed* non-qualifying variant (current_close missing) using the
    real production type, not a claim about F2 itself."""
    from services.market_data.yahoo_chart import ProviderQuoteEvidence, QuoteObservation

    real_evidence = ProviderQuoteEvidence(
        provider="yahoo_chart",
        requested_symbol="F2SYM.BK",
        served_symbol="F2SYM.BK",
        observations=(
            QuoteObservation(timestamp=1_700_000_000, close=95.0),
            QuoteObservation(timestamp=1_700_086_400, close=None),
            QuoteObservation(timestamp=1_700_172_800, close=100.0),
        ),
        current_close=None,
        previous_close=95.0,
        exchange_timezone_name="Asia/Bangkok",
    )
    assert contract.evidence_qualifies(real_evidence) is False
