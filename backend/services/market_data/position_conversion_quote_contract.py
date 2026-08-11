"""BANPU-WP3.2 — pure binding, epoch, admissibility, and quarantine contract.

Consumes the frozen WP1 ``PositionConversionSuccessor``,
``PositionConversionQuoteBinding``, ``PositionConversionDates``, and
``PositionConversionBoundaryEvidence`` payload contracts
(``services.transaction_canonicalizer``, read-only, never amended) and a
provider-neutral quote-evidence shape (structurally consulted, never imported
from any concrete provider adapter) to answer three pure questions: what is
the successor's immutable quote binding (IO-2), which exchange-local epoch
does a provider observation fall in (PD-2), and does a converted identity's
evidence and reference price admit or quarantine (PD-3 obligation B1, PD-4
E1-E5, WP1 residual MINOR-2's WP3 half).

Correction Round (post-C2): per
docs/implementation/BANPU_WP3_REFERENCE_PRICE_ADMISSIBILITY_CLARIFICATION_RECORD.md,
a BANPU-WP3 "reference price" is exactly one of
``PositionConversionBoundaryEvidence.predecessor_reference_price`` /
``.successor_reference_price`` -- never a provider ``current_close`` /
``previous_close``. ``assess_reference_price_admissibility`` and
``check_reference_price_inadmissible`` are re-based accordingly. Provider
closes remain governed by presence (E4) and the provider-close checks in
``evidence_qualifies`` alone; decimal-exactness is never required of them.

Correction Round 2 (post-C2 re-review): provider-close admissibility
(``current_close`` must be present/numeric/finite/strictly-positive;
``previous_close`` may be ``None`` -- preserving A2 for the first
successor-epoch quote -- but when present is held to the same standard) is
enforced inside ``evidence_qualifies`` and reuses the existing
``EVIDENCE_CONTRACT_NOT_SATISFIED`` quarantine reason; no new
``QuarantineReason`` was introduced and reference-price admissibility is
unchanged.

Deliberately pure: no I/O, no clock read, no database access, no registry
lookup, no environment or configuration lookup, and no import of any provider
adapter (``yahoo_chart.py`` or otherwise) or of ``data_fetcher.py``. Every
function here is a total function of its explicit arguments.

Layering (docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md
§5.4): provider evidence (WP3.1) -> this pure contract (WP3.2) -> fetch-layer
enforcement (WP3.3, not implemented here). Nothing in this module is consumed
by anything yet; it is deliberately unwired until a future, separately
Gate-S8-scoped WP3.3.

Out of scope, by design: WP5's mechanical NAV continuity tolerance; emitting a
validator finding (``ledger_validator.py`` is never touched or imported here —
PD-3 confines that to a referred-out emitter locus); registry mutation,
identifier retirement, or ``MERGED_INTO`` authoring (WP4).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Protocol, Sequence, runtime_checkable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from services.transaction_canonicalizer import (
    PositionConversionBoundaryEvidence,
    PositionConversionDates,
    PositionConversionQuoteBinding,
    PositionConversionSuccessor,
)

__all__ = [
    "SuccessorQuoteBinding",
    "EpochClassification",
    "ReferencePriceAdmissibility",
    "QuarantineReason",
    "QuarantineResult",
    "ProviderQuoteEvidenceLike",
    "build_successor_quote_binding",
    "quote_cache_type",
    "history_cache_type",
    "exchange_local_date",
    "classify_observation_epoch",
    "evidence_qualifies",
    "assess_reference_price_admissibility",
    "check_missing_or_ambiguous_identifier",
    "evaluate_request_identity",
    "check_provider_symbol_mismatch",
    "check_cross_epoch_timestamp",
    "check_cache_namespace_mismatch",
    "check_evidence_contract_not_satisfied",
    "check_reference_price_inadmissible",
    "evaluate_candidate_quarantine",
]

# Exceptions a malformed *evidence-derived* timestamp or exchange-timezone
# name can raise out of ``datetime.fromtimestamp``/``ZoneInfo`` -- guarded at
# every evidence-consuming boundary in this module so none ever escapes as an
# implementation exception (Correction Round, C2 finding).
_EPOCH_CLASSIFICATION_EXCEPTIONS = (
    ValueError,
    TypeError,
    OverflowError,
    OSError,
    ArithmeticError,
    ZoneInfoNotFoundError,
)


# ── Step 2.2 / IO-2 — immutable successor quote binding ─────────────────────

@dataclass(frozen=True)
class SuccessorQuoteBinding:
    """The five-field successor binding, mechanically derived per IO-2.

    Never built from ``PositionConversionQuoteBinding.predecessor_provider_symbol``
    -- see ``build_successor_quote_binding``.
    """

    asset_id: int
    provider: str
    provider_symbol: str
    quote_epoch_start_date: date
    valuation_transition_date: date


def build_successor_quote_binding(
    successor: PositionConversionSuccessor,
    quote_binding: PositionConversionQuoteBinding,
    dates: PositionConversionDates,
) -> SuccessorQuoteBinding:
    """Build the immutable successor binding per IO-2's mechanical field mapping.

    Deliberately never reads ``quote_binding.predecessor_provider_symbol`` --
    that field has no parameter path into this function at all, which is the
    strongest available proof that the predecessor symbol cannot supply the
    successor binding.
    """
    return SuccessorQuoteBinding(
        asset_id=successor.asset_id,
        provider=quote_binding.provider,
        provider_symbol=quote_binding.successor_provider_symbol,
        quote_epoch_start_date=dates.successor_quote_epoch_start_date,
        valuation_transition_date=dates.valuation_transition_date,
    )


# ── Step 2.2 — deterministic, enumerable cache-key components ───────────────

def quote_cache_type(binding: SuccessorQuoteBinding) -> str:
    return f"quote:asset={binding.asset_id}:epoch={binding.quote_epoch_start_date.isoformat()}"


def history_cache_type(binding: SuccessorQuoteBinding) -> str:
    return f"history:5y:1d:asset={binding.asset_id}:epoch={binding.quote_epoch_start_date.isoformat()}"


# ── Step 2.3 — PD-2 epoch classification ────────────────────────────────────

class EpochClassification(str, Enum):
    PREDECESSOR_EPOCH = "PREDECESSOR_EPOCH"
    SUCCESSOR_EPOCH = "SUCCESSOR_EPOCH"


def exchange_local_date(timestamp: int, exchange_timezone_name: str) -> date:
    """Map one provider epoch-seconds observation timestamp to an
    exchange-local calendar date. Pure: converts the given ``timestamp``
    value only -- never reads the system clock or the system timezone.
    """
    return datetime.fromtimestamp(timestamp, tz=ZoneInfo(exchange_timezone_name)).date()


def classify_observation_epoch(
    timestamp: int,
    exchange_timezone_name: str,
    quote_epoch_start_date: date,
) -> EpochClassification:
    """PD-2: classify by exchange-local calendar date, never by UTC date.
    ``quote_epoch_start_date`` itself belongs to the successor epoch.
    """
    local_date = exchange_local_date(timestamp, exchange_timezone_name)
    if local_date >= quote_epoch_start_date:
        return EpochClassification.SUCCESSOR_EPOCH
    return EpochClassification.PREDECESSOR_EPOCH


# ── Step 2.4 — E1-E5 evidence qualification (PD-4) ──────────────────────────

@runtime_checkable
class ProviderQuoteEvidenceLike(Protocol):
    """Structural E1-E5 evidence shape (IO-1). Deliberately not imported from
    any concrete provider adapter: any object with these attributes qualifies
    structurally, including ``yahoo_chart.ProviderQuoteEvidence``, without
    this module importing ``yahoo_chart.py``.
    """

    provider: str
    requested_symbol: str
    served_symbol: Optional[str]
    observations: Sequence[object]
    current_close: Optional[float]
    previous_close: Optional[float]
    exchange_timezone_name: Optional[str]


def _provider_close_is_valid(value: object) -> bool:
    """A provider close (``current_close``/``previous_close``) is admissible
    iff it is numeric (as the evidence Protocol already permits -- ``bool``
    excluded, since ``bool`` is an ``int`` subtype in Python and is never a
    genuine price), finite, and strictly positive. Deliberately not
    decimal-exact -- see ``assess_reference_price_admissibility`` for the
    unrelated, decimal-exact reference-price value class (Correction Round
    2, C2 finding: provider-close admissibility must not be conflated with
    reference-price admissibility).
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    if isinstance(value, float) and not math.isfinite(value):
        return False
    return value > 0


def evidence_qualifies(evidence: object) -> bool:
    """PD-4: does this evidence structure supply E1-E5, over capability alone
    -- never compared against a specific binding's identity here (that
    comparison is ``check_provider_symbol_mismatch``). Silence on any element
    disqualifies. Fails closed: never raises for a malformed object, only
    returns False.

    E3 and E5 are checked semantically, not merely for truthiness: an
    unresolvable exchange-timezone name (E5) and a non-numeric, non-finite,
    or otherwise unclassifiable observation timestamp (E3) are structurally
    present but semantically unusable, and must not qualify (Correction
    Round, C2 finding -- malformed E3/E5 evidence must fail closed, never
    escape as ``ZoneInfoNotFoundError``/``TypeError``/``ValueError``/
    ``OverflowError``).

    E4 (``current_close``) is likewise checked semantically, not merely for
    presence: it must be present, numeric, finite, and strictly positive
    (Correction Round 2, C2 finding -- provider-close admissibility). This
    reuses the existing ``EVIDENCE_CONTRACT_NOT_SATISFIED`` quarantine reason
    via ``check_evidence_contract_not_satisfied``; no new
    ``QuarantineReason`` is introduced. ``previous_close`` is not part of
    E1-E5 and may legitimately be ``None`` -- preserving A2 for the first
    successor-epoch quote, which has no prior observation at all -- but when
    it *is* present, it is held to the same finite/strictly-positive
    standard as ``current_close``. Neither close is ever required to be
    decimal-exact: that property belongs exclusively to the unrelated
    boundary-evidence reference-price value class.
    """
    if not isinstance(evidence, ProviderQuoteEvidenceLike):
        return False
    if not evidence.provider:  # E1
        return False
    if not evidence.served_symbol:  # E2
        return False
    if not evidence.observations:  # E3
        return False
    if not evidence.exchange_timezone_name:  # E5
        return False
    try:
        exchange_tz = ZoneInfo(evidence.exchange_timezone_name)
    except _EPOCH_CLASSIFICATION_EXCEPTIONS:
        return False
    for obs in evidence.observations:  # E3
        timestamp = getattr(obs, "timestamp", None)
        if timestamp is None:
            return False
        if isinstance(timestamp, bool) or not isinstance(timestamp, (int, float)):
            return False
        if isinstance(timestamp, float) and not math.isfinite(timestamp):
            return False
        try:
            datetime.fromtimestamp(timestamp, tz=exchange_tz)
        except _EPOCH_CLASSIFICATION_EXCEPTIONS:
            return False
    if not _provider_close_is_valid(evidence.current_close):  # E4
        return False
    if evidence.previous_close is not None and not _provider_close_is_valid(evidence.previous_close):
        return False
    return True


# ── Step 2.4 — reference-price admissibility (WP3 half of MINOR-2) ──────────

class ReferencePriceAdmissibility(str, Enum):
    ADMISSIBLE = "ADMISSIBLE"
    ABSENT = "ABSENT"
    NON_POSITIVE = "NON_POSITIVE"
    NON_FINITE = "NON_FINITE"
    NON_DECIMAL_EXACT = "NON_DECIMAL_EXACT"


_REFERENCE_PRICE_FIELDS = ("predecessor_reference_price", "successor_reference_price")


def assess_reference_price_admissibility(
    boundary_evidence: object,
    field: str,
) -> ReferencePriceAdmissibility:
    """WP3's half of WP1 residual MINOR-2 / A9.

    Per
    docs/implementation/BANPU_WP3_REFERENCE_PRICE_ADMISSIBILITY_CLARIFICATION_RECORD.md
    §3-§5, a BANPU-WP3 "reference price" is exactly one of
    ``PositionConversionBoundaryEvidence.predecessor_reference_price`` /
    ``.successor_reference_price`` from the frozen WP1 parsed
    ``POSITION_CONVERSION`` payload -- never a provider ``current_close`` /
    ``previous_close`` (those are a distinct value class; see
    ``evidence_qualifies``'s E4 element). Does not implement WP5's mechanical
    continuity tolerance -- no tolerance/reconciliation parameter exists
    here at all.

    Takes the boundary-evidence object and a field selector rather than a
    bare number, so a reference price can never be assessed except as read
    directly off the frozen WP1 boundary-evidence contract -- evidence-bound
    by construction (clarification record §5.4: both ``boundary_evidence``
    and ``evidence`` are mandatory, non-optional members of a valid parsed
    ``PositionConversion``, so consuming this object already establishes
    evidence-boundedness structurally).

    "Decimal-exact" (element 2) requires the value to literally be a
    ``decimal.Decimal`` instance -- the type the frozen WP1 parser's
    ``reader.decimal()`` exclusively produces, itself only ever accepting a
    plain base-10 *string* input (never a Python ``float``). This module
    never constructs a reference-price ``Decimal`` via ``Decimal(str(...))``
    or any path other than consuming an already-parsed
    ``PositionConversionBoundaryEvidence`` instance; no numeric
    decimal-place, precision, or exponent threshold is imposed anywhere in
    this predicate.
    """
    if field not in _REFERENCE_PRICE_FIELDS:
        raise ValueError(
            f"field must be one of {_REFERENCE_PRICE_FIELDS!r}, got {field!r}"
        )
    if boundary_evidence is None or not isinstance(
        boundary_evidence, PositionConversionBoundaryEvidence
    ):
        return ReferencePriceAdmissibility.ABSENT
    value = getattr(boundary_evidence, field, None)
    if value is None:
        return ReferencePriceAdmissibility.ABSENT
    if not isinstance(value, Decimal):
        return ReferencePriceAdmissibility.NON_DECIMAL_EXACT
    if not value.is_finite():
        return ReferencePriceAdmissibility.NON_FINITE
    if value <= 0:
        return ReferencePriceAdmissibility.NON_POSITIVE
    return ReferencePriceAdmissibility.ADMISSIBLE


# ── Step 2.5 — enumerated quarantine reasons and consultable result ─────────

class QuarantineReason(str, Enum):
    """Exhaustive over design §10's WP3-scoped quarantine conditions plus
    E1-E5 non-satisfaction. Mechanical continuity failure and unannotated
    boundary discontinuity are design §10's WP5-owned half (mechanical NAV
    continuity tolerance) and are deliberately absent from this enumeration.
    """

    MISSING_OR_AMBIGUOUS_IDENTIFIER = "MISSING_OR_AMBIGUOUS_IDENTIFIER"
    PROVIDER_SYMBOL_MISMATCH = "PROVIDER_SYMBOL_MISMATCH"
    CROSS_EPOCH_TIMESTAMP = "CROSS_EPOCH_TIMESTAMP"
    CACHE_NAMESPACE_MISMATCH = "CACHE_NAMESPACE_MISMATCH"
    EVIDENCE_CONTRACT_NOT_SATISFIED = "EVIDENCE_CONTRACT_NOT_SATISFIED"
    REFERENCE_PRICE_INADMISSIBLE = "REFERENCE_PRICE_INADMISSIBLE"


@dataclass(frozen=True)
class QuarantineResult:
    """PD-3 obligation B1: a deterministic, consultable artifact carrying
    exactly one enumerated reason and exactly one affected identity. WP3 owns
    this predicate and result only -- it emits no validator finding and is
    never passed to ``ledger_validator.py``.
    """

    reason: QuarantineReason
    affected_asset_id: int


def check_missing_or_ambiguous_identifier(binding: SuccessorQuoteBinding) -> Optional[QuarantineResult]:
    if binding.asset_id is None or binding.asset_id <= 0 or not binding.provider or not binding.provider_symbol:
        return QuarantineResult(QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER, binding.asset_id)
    return None


def evaluate_request_identity(
    binding: SuccessorQuoteBinding,
    requested_symbol: str,
    request_provider: str | None = None,
) -> Optional[QuarantineResult]:
    """Evaluate identity known before a provider request is made.

    This entry point deliberately consumes only authoritative request-side
    values.  It does not require provider evidence, served-symbol evidence,
    boundary evidence, cache state, or any runtime service object.  The
    post-fetch identity and evidence checks remain in
    ``evaluate_candidate_quarantine``.
    """
    try:
        if not isinstance(binding, SuccessorQuoteBinding):
            asset_id = getattr(binding, "asset_id", 0)
            if isinstance(asset_id, bool) or not isinstance(asset_id, int):
                asset_id = 0
            return QuarantineResult(
                QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
                asset_id,
            )

        result = check_missing_or_ambiguous_identifier(binding)
        if result is not None:
            return result

        if isinstance(binding.asset_id, bool) or not isinstance(binding.asset_id, int):
            return QuarantineResult(
                QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
                0,
            )
        if not isinstance(binding.provider, str) or not binding.provider.strip():
            return QuarantineResult(
                QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
                binding.asset_id,
            )
        if not isinstance(binding.provider_symbol, str) or not binding.provider_symbol.strip():
            return QuarantineResult(
                QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
                binding.asset_id,
            )
        if type(binding.quote_epoch_start_date) is not date:
            return QuarantineResult(
                QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
                binding.asset_id,
            )
        if type(binding.valuation_transition_date) is not date:
            return QuarantineResult(
                QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
                binding.asset_id,
            )
    except (AttributeError, TypeError, ValueError, ArithmeticError):
        asset_id = getattr(binding, "asset_id", 0)
        if isinstance(asset_id, bool) or not isinstance(asset_id, int):
            asset_id = 0
        return QuarantineResult(
            QuarantineReason.MISSING_OR_AMBIGUOUS_IDENTIFIER,
            asset_id,
        )

    if requested_symbol != binding.provider_symbol:
        return QuarantineResult(
            QuarantineReason.PROVIDER_SYMBOL_MISMATCH,
            binding.asset_id,
        )
    if request_provider is not None and request_provider != binding.provider:
        return QuarantineResult(
            QuarantineReason.PROVIDER_SYMBOL_MISMATCH,
            binding.asset_id,
        )
    return None


def check_provider_symbol_mismatch(
    evidence: object,
    binding: SuccessorQuoteBinding,
) -> Optional[QuarantineResult]:
    """Two-part identity validation, both required:

    (a) the provider-served symbol matches the symbol actually requested
        (R5's requested-vs-served comparison, using ``requested_symbol`` on
        the evidence itself -- no DR-specific normalization import is
        required or performed here); and
    (b) that requested/served symbol matches the immutable successor
        binding's ``provider_symbol`` (IO-2).

    (a) alone is insufficient: it proves the provider didn't silently
    substitute a different symbol than what was asked for, but says nothing
    about whether the *right* symbol was asked for in the first place. A
    binding for "SUCC.BK" evaluated against evidence that consistently
    requested/served "OTHER.BK" must still be rejected -- that is (b).

    Never reads ``predecessor_provider_symbol`` -- that field has no
    parameter path into this function.
    """
    if getattr(evidence, "provider", None) != binding.provider:
        return QuarantineResult(QuarantineReason.PROVIDER_SYMBOL_MISMATCH, binding.asset_id)
    requested_symbol = getattr(evidence, "requested_symbol", None)
    served_symbol = getattr(evidence, "served_symbol", None)
    if served_symbol != requested_symbol:
        return QuarantineResult(QuarantineReason.PROVIDER_SYMBOL_MISMATCH, binding.asset_id)
    if requested_symbol != binding.provider_symbol:
        return QuarantineResult(QuarantineReason.PROVIDER_SYMBOL_MISMATCH, binding.asset_id)
    return None


def check_cross_epoch_timestamp(
    evidence: object,
    binding: SuccessorQuoteBinding,
) -> Optional[QuarantineResult]:
    """Missing E5/E3 is its own reason (``check_evidence_contract_not_satisfied``);
    this check returns None rather than raising when evidence carries no
    exchange-timezone name at all, to keep exactly one reason per failure
    path.

    A timestamp or exchange-timezone name that *is* present but cannot
    actually be classified (invalid IANA name, non-numeric or out-of-range
    timestamp) can never be certified as belonging to the successor epoch --
    that is itself a cross-epoch-integrity failure, so it fails closed as
    ``CROSS_EPOCH_TIMESTAMP`` rather than letting the underlying
    ``ZoneInfoNotFoundError``/``TypeError``/``ValueError``/``OverflowError``
    escape (Correction Round, C2 finding). This guard is defense-in-depth:
    ``evidence_qualifies`` already rejects such evidence via E3/E5, so in the
    deterministic composite path (``evaluate_candidate_quarantine``) this
    function is only ever reached with evidence that already passed E1-E5.
    """
    exchange_timezone_name = getattr(evidence, "exchange_timezone_name", None)
    observations = getattr(evidence, "observations", None) or ()
    if not exchange_timezone_name:
        return None
    for obs in observations:
        timestamp = getattr(obs, "timestamp", None)
        if timestamp is None:
            continue
        try:
            classification = classify_observation_epoch(timestamp, exchange_timezone_name, binding.quote_epoch_start_date)
        except _EPOCH_CLASSIFICATION_EXCEPTIONS:
            return QuarantineResult(QuarantineReason.CROSS_EPOCH_TIMESTAMP, binding.asset_id)
        if classification is EpochClassification.PREDECESSOR_EPOCH:
            return QuarantineResult(QuarantineReason.CROSS_EPOCH_TIMESTAMP, binding.asset_id)
    return None


def check_cache_namespace_mismatch(
    candidate_cache_type: str,
    binding: SuccessorQuoteBinding,
    *,
    kind: str,
) -> Optional[QuarantineResult]:
    if kind not in ("quote", "history"):
        raise ValueError(f"kind must be 'quote' or 'history', got {kind!r}")
    expected = quote_cache_type(binding) if kind == "quote" else history_cache_type(binding)
    if candidate_cache_type != expected:
        return QuarantineResult(QuarantineReason.CACHE_NAMESPACE_MISMATCH, binding.asset_id)
    return None


def check_evidence_contract_not_satisfied(
    evidence: object,
    binding: SuccessorQuoteBinding,
) -> Optional[QuarantineResult]:
    if not evidence_qualifies(evidence):
        return QuarantineResult(QuarantineReason.EVIDENCE_CONTRACT_NOT_SATISFIED, binding.asset_id)
    return None


def check_reference_price_inadmissible(
    boundary_evidence: object,
    field: str,
    binding: SuccessorQuoteBinding,
) -> Optional[QuarantineResult]:
    """``boundary_evidence`` is a ``PositionConversionBoundaryEvidence``
    instance from the frozen WP1 parsed payload -- never provider evidence.
    """
    if assess_reference_price_admissibility(boundary_evidence, field) != ReferencePriceAdmissibility.ADMISSIBLE:
        return QuarantineResult(QuarantineReason.REFERENCE_PRICE_INADMISSIBLE, binding.asset_id)
    return None


# ── Correction Round — deterministic composite quarantine decision ─────────

def evaluate_candidate_quarantine(
    *,
    binding: SuccessorQuoteBinding,
    evidence: object,
    boundary_evidence: object,
    reference_price_field: str,
    candidate_cache_type: str,
    cache_kind: str,
) -> Optional[QuarantineResult]:
    """The single authoritative composite decision path (Correction Round,
    C2 finding): a caller evaluating one candidate binding + evidence pair
    must get exactly one deterministic enumerated result, never a set of
    competing ``check_*`` failures to choose among.

    Precedence is fixed and encoded in exactly this one place, in this exact
    order -- callers must not, and cannot, reorder it:

        1. MISSING_OR_AMBIGUOUS_IDENTIFIER  -- is the binding itself even
           well-formed? Nothing downstream is meaningful if not.
        2. EVIDENCE_CONTRACT_NOT_SATISFIED  -- E1-E5. Nothing that reads the
           evidence's symbol or timestamps (steps 3-4) can be trusted before
           this passes.
        3. PROVIDER_SYMBOL_MISMATCH         -- identity, over qualifying
           evidence.
        4. CROSS_EPOCH_TIMESTAMP            -- epoch integrity, over
           qualifying, identity-matched evidence.
        5. CACHE_NAMESPACE_MISMATCH         -- mechanical bookkeeping.
        6. REFERENCE_PRICE_INADMISSIBLE     -- an entirely separate value
           (boundary-evidence reference price, not provider evidence);
           evaluated last since it is independent of steps 2-5.

    Returns ``None`` only if every check passes. Identical inputs always
    produce the identical result (every check called is itself a pure,
    total-over-its-evidence-domain function -- see ``evidence_qualifies``
    and ``check_cross_epoch_timestamp`` for how each fails closed rather
    than raising on malformed evidence).

    ``reference_price_field`` and ``cache_kind`` are caller-supplied literal
    selectors (e.g. ``"successor_reference_price"``, ``"quote"``), never
    evidence-derived -- an invalid selector is a caller programming error
    and still raises ``ValueError`` here, exactly as the underlying
    ``check_reference_price_inadmissible`` / ``check_cache_namespace_mismatch``
    already do; this is intentionally not swallowed, so a real caller bug is
    never silently reinterpreted as a quarantine condition. No
    evidence-derived input can reach either raise: every value drawn from
    ``evidence`` or ``boundary_evidence`` is handled by the fail-closed
    ``check_*`` functions this composes, none of which raise for malformed
    evidence.
    """
    result = check_missing_or_ambiguous_identifier(binding)
    if result is not None:
        return result

    result = check_evidence_contract_not_satisfied(evidence, binding)
    if result is not None:
        return result

    result = check_provider_symbol_mismatch(evidence, binding)
    if result is not None:
        return result

    result = check_cross_epoch_timestamp(evidence, binding)
    if result is not None:
        return result

    result = check_cache_namespace_mismatch(candidate_cache_type, binding, kind=cache_kind)
    if result is not None:
        return result

    result = check_reference_price_inadmissible(boundary_evidence, reference_price_field, binding)
    if result is not None:
        return result

    return None
