"""Canonical Transaction Layer.

Converts raw SQLAlchemy Transaction ORM rows into immutable CanonicalTransaction
value objects. All downstream engines (Portfolio Rebuilder, Ledger Validator,
Snapshot Return Recovery) consume CanonicalTransaction instead of ORM rows,
eliminating duplicated preprocessing.

Responsibilities
----------------
* Resolve symbol aliases via get_yfinance_symbol() — once, in one place
* Preserve raw_symbol for audit trails and holdings_json lookups
* Convert numeric fields (shares, price, total_amount, fees, taxes) to Decimal
* Parse POSITION_CONVERSION version-1 payloads into exact immutable values
* Parse QUANTITY_CORRECTION notes into a signed qty_correction_delta
* Parse SELL notes into realized_pnl
* Coerce transaction_date to date; preserve created_at as datetime
* Sort by (transaction_date, id) for deterministic replay ordering

Non-responsibilities
--------------------
* No replay, no portfolio state, no cash calculation
* No snapshot generation, no yfinance calls, no network I/O
* No database reads or writes
* No validation, no error reporting
* No caching, no singleton, no mutable state

Consumers
---------
* portfolio_rebuilder  — full consumer; use canonical_symbol for holdings keys
* ledger_validator     — full consumer; use canonical_symbol for alias detection
* snapshot_return_recovery — partial consumer; use raw_symbol for holdings_json
  lookups (those keys were stored using the raw symbol at write time)
* snapshot_repair      — not a consumer; operates on stored holdings_json, not
  on Transaction rows
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, fields, is_dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from services.symbol_normalization import get_yfinance_symbol


_PLAIN_DECIMAL_RE = re.compile(r"^-?(?:0|[1-9]\d*)(?:\.\d+)?$")
_RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)

# These patterns are the single authoritative definitions.
# portfolio_rebuilder, ledger_validator, and snapshot_return_recovery each
# previously defined their own identical copies.  Those copies will be removed
# once each module is migrated to consume CanonicalTransaction.
_QCORR_RE    = re.compile(r"Quantity correction:\s*([+-]?\d[\d.]*)\s*shares", re.IGNORECASE)
_REALIZED_RE = re.compile(r"Realized P&L:\s*([-+]?\d+\.?\d*)")


def _to_decimal(v: Any) -> Decimal:
    """Convert any numeric-ish value to Decimal, returning Decimal('0') on failure."""
    try:
        return Decimal(str(v))
    except Exception:
        return Decimal("0")


def _to_date(v: Any) -> date | None:
    """Coerce a DateTime ORM column value to a plain date."""
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    return None


def _to_datetime(v: Any) -> datetime | None:
    """Return a datetime as-is; return None for anything else."""
    if isinstance(v, datetime):
        return v
    return None


@dataclass(frozen=True)
class PositionConversionParseError:
    """One deterministic, machine-readable payload contract violation."""

    code: str
    path: str
    message: str


@dataclass(frozen=True)
class PositionConversionPredecessor:
    asset_id: int
    symbol: str
    shares_surrendered: Decimal


@dataclass(frozen=True)
class PositionConversionSuccessor:
    asset_id: int
    symbol: str
    provider_symbol: str
    shares_entitled: Decimal
    shares_received: Decimal


@dataclass(frozen=True)
class PositionConversionBasis:
    before: Decimal
    allocated_to_cash_in_lieu: Decimal
    carried_to_successor: Decimal


@dataclass(frozen=True)
class PositionConversionCashInLieu:
    fractional_entitlement_shares: Decimal
    gross_proceeds: Decimal
    fees: Decimal
    taxes: Decimal
    net_cash: Decimal
    basis_allocated: Decimal
    realized_pnl: Decimal


@dataclass(frozen=True)
class PositionConversionDates:
    legal_effective_date: date
    valuation_transition_date: date
    predecessor_last_price_date: date
    successor_quote_epoch_start_date: date


@dataclass(frozen=True)
class PositionConversionQuoteBinding:
    provider: str
    predecessor_provider_symbol: str
    successor_provider_symbol: str


@dataclass(frozen=True)
class PositionConversionBoundaryEvidence:
    predecessor_reference_price: Decimal
    successor_reference_price: Decimal
    mechanical_nav_tolerance_pct: Decimal
    suspension_gap_annotation: str


@dataclass(frozen=True)
class PositionConversionEvidence:
    reference: str
    source: str
    captured_at: datetime


@dataclass(frozen=True)
class PositionConversion:
    """Immutable, exact-decimal version-1 POSITION_CONVERSION payload."""

    schema_version: int
    predecessor: PositionConversionPredecessor
    successor: PositionConversionSuccessor
    conversion_ratio: Decimal
    basis: PositionConversionBasis
    cash_in_lieu: PositionConversionCashInLieu | None
    dates: PositionConversionDates
    quote_binding: PositionConversionQuoteBinding
    boundary_evidence: PositionConversionBoundaryEvidence
    evidence: PositionConversionEvidence
    fingerprint: str


@dataclass(frozen=True)
class PositionConversionParseResult:
    """A valid value or structured errors; never both."""

    value: PositionConversion | None
    errors: tuple[PositionConversionParseError, ...]

    @property
    def is_valid(self) -> bool:
        return self.value is not None and not self.errors


class _PayloadReader:
    def __init__(self) -> None:
        self.errors: list[PositionConversionParseError] = []

    def error(self, code: str, path: str, message: str) -> None:
        self.errors.append(PositionConversionParseError(code, path, message))

    def mapping(
        self,
        value: Any,
        path: str,
        required: set[str],
    ) -> Mapping[str, Any] | None:
        if not isinstance(value, Mapping):
            self.error("TYPE_INVALID", path, "must be an object")
            return None
        for key in sorted(required - set(value)):
            self.error("FIELD_REQUIRED", f"{path}.{key}", "field is required")
        for key in sorted(set(value) - required):
            self.error("FIELD_UNKNOWN", f"{path}.{key}", "field is not permitted")
        return value

    def integer(self, obj: Mapping[str, Any] | None, key: str, path: str) -> int | None:
        value = obj.get(key) if obj is not None else None
        if isinstance(value, bool) or not isinstance(value, int):
            self.error("INTEGER_INVALID", f"{path}.{key}", "must be an integer")
            return None
        return value

    def string(self, obj: Mapping[str, Any] | None, key: str, path: str) -> str | None:
        value = obj.get(key) if obj is not None else None
        if not isinstance(value, str) or not value.strip():
            self.error("STRING_INVALID", f"{path}.{key}", "must be a non-empty string")
            return None
        return value

    def decimal(self, obj: Mapping[str, Any] | None, key: str, path: str) -> Decimal | None:
        value = obj.get(key) if obj is not None else None
        if not isinstance(value, str) or _PLAIN_DECIMAL_RE.fullmatch(value) is None:
            self.error("DECIMAL_INVALID", f"{path}.{key}", "must be a base-10 string")
            return None
        try:
            parsed = Decimal(value)
        except (InvalidOperation, ValueError):
            parsed = None
        if parsed is None or not parsed.is_finite():
            self.error("DECIMAL_INVALID", f"{path}.{key}", "must be a finite base-10 decimal string")
            return None
        return parsed

    def date(self, obj: Mapping[str, Any] | None, key: str, path: str) -> date | None:
        value = obj.get(key) if obj is not None else None
        try:
            parsed = date.fromisoformat(value) if isinstance(value, str) else None
        except ValueError:
            parsed = None
        if parsed is None:
            self.error("DATE_INVALID", f"{path}.{key}", "must be an ISO 8601 calendar date")
        return parsed

    def timestamp(self, obj: Mapping[str, Any] | None, key: str, path: str) -> datetime | None:
        value = obj.get(key) if obj is not None else None
        try:
            parsed = (
                datetime.fromisoformat(value.replace("Z", "+00:00"))
                if isinstance(value, str) and _RFC3339_RE.fullmatch(value) is not None
                else None
            )
        except ValueError:
            parsed = None
        if parsed is None or parsed.tzinfo is None:
            self.error("TIMESTAMP_INVALID", f"{path}.{key}", "must be an RFC3339 timestamp with an offset")
            return None
        return parsed


def _format_decimal_context_independent(value: Decimal) -> str:
    """Render a nonzero Decimal as plain base-10 notation from its exact
    coefficient and exponent, independent of the ambient Decimal context.

    ``Decimal.normalize()`` rounds to the active context precision before
    formatting, so two exact values differing only beyond that precision can
    serialize identically (BANPU-WP1 MINOR-1). ``format(value, "f")`` renders
    the exact coefficient with no context-applying arithmetic; only
    insignificant fractional trailing zeroes and a now-empty decimal point
    are stripped afterward.
    """
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _canonical_fingerprint_value(value: Any) -> Any:
    """Return the stable JSON value used by conversion fingerprints.

    Fingerprints describe parsed semantics, not input formatting: decimals use
    plain notation without insignificant trailing zeroes (and negative zero is
    canonicalized to zero), aware timestamps are converted to UTC with ``Z``,
    dates use ISO calendar form, and typed payload records use their declared
    field order. JSON object key order remains irrelevant when encoded.
    """

    if isinstance(value, Decimal):
        if value == 0:
            return "0"
        return _format_decimal_context_independent(value)
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return value.isoformat()
    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: _canonical_fingerprint_value(getattr(value, field.name))
            for field in fields(value)
            if field.name != "fingerprint"
        }
    if isinstance(value, Mapping):
        return {
            str(key): _canonical_fingerprint_value(item)
            for key, item in value.items()
        }
    if isinstance(value, (tuple, list)):
        return [_canonical_fingerprint_value(item) for item in value]
    return value


def _payload_fingerprint(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        _canonical_fingerprint_value(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def parse_position_conversion_payload(payload: Any) -> PositionConversionParseResult:
    """Parse and validate the exact version-1 POSITION_CONVERSION contract."""

    reader = _PayloadReader()
    root_fields = {
        "schema_version", "predecessor", "successor", "conversion_ratio",
        "basis", "cash_in_lieu", "dates", "quote_binding",
        "boundary_evidence", "evidence",
    }
    root = reader.mapping(payload, "$", root_fields)
    if root is None:
        return PositionConversionParseResult(None, tuple(reader.errors))

    version = reader.integer(root, "schema_version", "$")
    if version is not None and version != 1:
        reader.error("VERSION_UNSUPPORTED", "$.schema_version", "only schema_version 1 is supported")

    predecessor_obj = reader.mapping(
        root.get("predecessor"), "$.predecessor",
        {"asset_id", "symbol", "shares_surrendered"},
    )
    predecessor_asset_id = reader.integer(predecessor_obj, "asset_id", "$.predecessor")
    predecessor_symbol = reader.string(predecessor_obj, "symbol", "$.predecessor")
    shares_surrendered = reader.decimal(predecessor_obj, "shares_surrendered", "$.predecessor")

    successor_obj = reader.mapping(
        root.get("successor"), "$.successor",
        {"asset_id", "symbol", "provider_symbol", "shares_entitled", "shares_received"},
    )
    successor_asset_id = reader.integer(successor_obj, "asset_id", "$.successor")
    successor_symbol = reader.string(successor_obj, "symbol", "$.successor")
    successor_provider_symbol = reader.string(successor_obj, "provider_symbol", "$.successor")
    shares_entitled = reader.decimal(successor_obj, "shares_entitled", "$.successor")
    shares_received = reader.decimal(successor_obj, "shares_received", "$.successor")
    conversion_ratio = reader.decimal(root, "conversion_ratio", "$")

    basis_obj = reader.mapping(
        root.get("basis"), "$.basis",
        {"before", "allocated_to_cash_in_lieu", "carried_to_successor"},
    )
    basis_before = reader.decimal(basis_obj, "before", "$.basis")
    basis_allocated = reader.decimal(basis_obj, "allocated_to_cash_in_lieu", "$.basis")
    basis_carried = reader.decimal(basis_obj, "carried_to_successor", "$.basis")

    cash_value = root.get("cash_in_lieu")
    cash_obj = None
    cash_values: tuple[Decimal | None, ...] | None = None
    if cash_value is not None:
        cash_obj = reader.mapping(
            cash_value, "$.cash_in_lieu",
            {
                "fractional_entitlement_shares", "gross_proceeds", "fees",
                "taxes", "net_cash", "basis_allocated", "realized_pnl",
            },
        )
        cash_values = (
            reader.decimal(cash_obj, "fractional_entitlement_shares", "$.cash_in_lieu"),
            reader.decimal(cash_obj, "gross_proceeds", "$.cash_in_lieu"),
            reader.decimal(cash_obj, "fees", "$.cash_in_lieu"),
            reader.decimal(cash_obj, "taxes", "$.cash_in_lieu"),
            reader.decimal(cash_obj, "net_cash", "$.cash_in_lieu"),
            reader.decimal(cash_obj, "basis_allocated", "$.cash_in_lieu"),
            reader.decimal(cash_obj, "realized_pnl", "$.cash_in_lieu"),
        )

    dates_obj = reader.mapping(
        root.get("dates"), "$.dates",
        {
            "legal_effective_date", "valuation_transition_date",
            "predecessor_last_price_date", "successor_quote_epoch_start_date",
        },
    )
    dates_values = (
        reader.date(dates_obj, "legal_effective_date", "$.dates"),
        reader.date(dates_obj, "valuation_transition_date", "$.dates"),
        reader.date(dates_obj, "predecessor_last_price_date", "$.dates"),
        reader.date(dates_obj, "successor_quote_epoch_start_date", "$.dates"),
    )

    binding_obj = reader.mapping(
        root.get("quote_binding"), "$.quote_binding",
        {"provider", "predecessor_provider_symbol", "successor_provider_symbol"},
    )
    binding_values = (
        reader.string(binding_obj, "provider", "$.quote_binding"),
        reader.string(binding_obj, "predecessor_provider_symbol", "$.quote_binding"),
        reader.string(binding_obj, "successor_provider_symbol", "$.quote_binding"),
    )

    boundary_obj = reader.mapping(
        root.get("boundary_evidence"), "$.boundary_evidence",
        {
            "predecessor_reference_price", "successor_reference_price",
            "mechanical_nav_tolerance_pct", "suspension_gap_annotation",
        },
    )
    boundary_values = (
        reader.decimal(boundary_obj, "predecessor_reference_price", "$.boundary_evidence"),
        reader.decimal(boundary_obj, "successor_reference_price", "$.boundary_evidence"),
        reader.decimal(boundary_obj, "mechanical_nav_tolerance_pct", "$.boundary_evidence"),
        reader.string(boundary_obj, "suspension_gap_annotation", "$.boundary_evidence"),
    )

    evidence_obj = reader.mapping(
        root.get("evidence"), "$.evidence",
        {"reference", "source", "captured_at"},
    )
    evidence_values = (
        reader.string(evidence_obj, "reference", "$.evidence"),
        reader.string(evidence_obj, "source", "$.evidence"),
        reader.timestamp(evidence_obj, "captured_at", "$.evidence"),
    )

    required_numbers = (
        shares_surrendered, shares_entitled, shares_received, conversion_ratio,
        basis_before, basis_allocated, basis_carried,
    )
    if all(value is not None for value in required_numbers):
        assert shares_surrendered is not None
        assert shares_entitled is not None
        assert shares_received is not None
        assert conversion_ratio is not None
        assert basis_before is not None
        assert basis_allocated is not None
        assert basis_carried is not None
        if shares_surrendered <= 0 or conversion_ratio <= 0 or shares_received <= 0:
            reader.error("INVARIANT_VIOLATION", "$", "shares and conversion ratio must be positive")
        if shares_entitled != shares_surrendered * conversion_ratio:
            reader.error("INVARIANT_VIOLATION", "$.successor.shares_entitled", "must equal shares_surrendered times conversion_ratio")
        if shares_received > shares_entitled:
            reader.error("INVARIANT_VIOLATION", "$.successor.shares_received", "cannot exceed shares_entitled")
        if min(basis_before, basis_allocated, basis_carried) < 0:
            reader.error("INVARIANT_VIOLATION", "$.basis", "basis values cannot be negative")
        if basis_before != basis_allocated + basis_carried:
            reader.error("INVARIANT_VIOLATION", "$.basis", "before must equal allocated plus carried basis")

        fractional = shares_entitled - shares_received
        if cash_values is None:
            if fractional != 0 or basis_allocated != 0:
                reader.error("INVARIANT_VIOLATION", "$.cash_in_lieu", "must be present for fractional entitlement or allocated basis")
        elif all(value is not None for value in cash_values):
            fraction, gross, fees, taxes, net, cash_basis, pnl = cash_values
            assert fraction is not None and gross is not None and fees is not None
            assert taxes is not None and net is not None and cash_basis is not None and pnl is not None
            if fraction <= 0 or min(gross, fees, taxes, cash_basis) < 0:
                reader.error("INVARIANT_VIOLATION", "$.cash_in_lieu", "fraction must be positive and monetary inputs non-negative")
            if fraction != fractional:
                reader.error("INVARIANT_VIOLATION", "$.cash_in_lieu.fractional_entitlement_shares", "must equal entitled shares minus received shares")
            if cash_basis != basis_allocated:
                reader.error("INVARIANT_VIOLATION", "$.cash_in_lieu.basis_allocated", "must match basis.allocated_to_cash_in_lieu")
            if net != gross - fees - taxes:
                reader.error("INVARIANT_VIOLATION", "$.cash_in_lieu.net_cash", "must equal gross_proceeds minus fees and taxes")
            if pnl != net - cash_basis:
                reader.error("INVARIANT_VIOLATION", "$.cash_in_lieu.realized_pnl", "must equal net_cash minus basis_allocated")

    if predecessor_asset_id is not None and predecessor_asset_id <= 0:
        reader.error("INVARIANT_VIOLATION", "$.predecessor.asset_id", "must be positive")
    if successor_asset_id is not None and successor_asset_id <= 0:
        reader.error("INVARIANT_VIOLATION", "$.successor.asset_id", "must be positive")
    if predecessor_asset_id is not None and predecessor_asset_id == successor_asset_id:
        reader.error("INVARIANT_VIOLATION", "$.successor.asset_id", "must differ from predecessor asset_id")
    if all(value is not None for value in dates_values):
        _, transition, _, epoch_start = dates_values
        assert transition is not None and epoch_start is not None
        if epoch_start > transition:
            reader.error("INVARIANT_VIOLATION", "$.dates.successor_quote_epoch_start_date", "must be no later than valuation_transition_date")
    if successor_provider_symbol is not None and binding_values[2] is not None:
        if successor_provider_symbol != binding_values[2]:
            reader.error("INVARIANT_VIOLATION", "$.quote_binding.successor_provider_symbol", "must match successor.provider_symbol")

    if reader.errors:
        return PositionConversionParseResult(None, tuple(reader.errors))

    assert version == 1
    assert predecessor_asset_id is not None and predecessor_symbol is not None and shares_surrendered is not None
    assert successor_asset_id is not None and successor_symbol is not None and successor_provider_symbol is not None
    assert shares_entitled is not None and shares_received is not None and conversion_ratio is not None
    assert basis_before is not None and basis_allocated is not None and basis_carried is not None
    assert all(value is not None for value in dates_values + binding_values + boundary_values + evidence_values)

    cash = None
    if cash_values is not None:
        assert all(value is not None for value in cash_values)
        cash = PositionConversionCashInLieu(*cash_values)  # type: ignore[arg-type]
    predecessor = PositionConversionPredecessor(
        predecessor_asset_id, predecessor_symbol, shares_surrendered
    )
    successor = PositionConversionSuccessor(
        successor_asset_id, successor_symbol, successor_provider_symbol,
        shares_entitled, shares_received,
    )
    basis = PositionConversionBasis(basis_before, basis_allocated, basis_carried)
    dates = PositionConversionDates(*dates_values)  # type: ignore[arg-type]
    quote_binding = PositionConversionQuoteBinding(*binding_values)  # type: ignore[arg-type]
    boundary_evidence = PositionConversionBoundaryEvidence(*boundary_values)  # type: ignore[arg-type]
    evidence = PositionConversionEvidence(*evidence_values)  # type: ignore[arg-type]
    fingerprint = _payload_fingerprint({
        "schema_version": version,
        "predecessor": predecessor,
        "successor": successor,
        "conversion_ratio": conversion_ratio,
        "basis": basis,
        "cash_in_lieu": cash,
        "dates": dates,
        "quote_binding": quote_binding,
        "boundary_evidence": boundary_evidence,
        "evidence": evidence,
    })
    value = PositionConversion(
        schema_version=version,
        predecessor=predecessor,
        successor=successor,
        conversion_ratio=conversion_ratio,
        basis=basis,
        cash_in_lieu=cash,
        dates=dates,
        quote_binding=quote_binding,
        boundary_evidence=boundary_evidence,
        evidence=evidence,
        fingerprint=fingerprint,
    )
    return PositionConversionParseResult(value, ())


@dataclass(frozen=True)
class CanonicalTransaction:
    """Immutable, authoritative interpretation of one Transaction row.

    Downstream engines operate on this type instead of SQLAlchemy ORM objects.
    The ORM layer is an infrastructure concern; business engines should not
    depend on it.

    Fields
    ------
    id
        Source Transaction.id — required for audit trail (LedgerFinding.transaction_ids).
        Not a business field; carried for traceability only.

    transaction_type
        Preserved verbatim: BUY, SELL, DEPOSIT, WITHDRAW, INITIAL_POSITION,
        INITIAL_CASH, QUANTITY_CORRECTION, DIVIDEND, POSITION_CONVERSION.

    raw_symbol
        Original tx.symbol stripped and uppercased, or None for cash-only
        transactions (DEPOSIT, WITHDRAW, INITIAL_CASH, DIVIDEND).
        Use this when matching against holdings_json keys, which were stored
        using the raw symbol at write time.

    canonical_symbol
        get_yfinance_symbol(raw_symbol).  Use this for replay engine holdings
        dictionaries and for yfinance price lookups.
        None when raw_symbol is None.

    shares
        Decimal(tx.shares).  Zero if tx.shares is None or absent.

    price_per_share
        Decimal(tx.price_per_share).  Zero if None.

    total_amount
        Decimal(tx.total_amount).

    fees
        Decimal(tx.fees).  Zero if None.

    taxes
        Decimal(tx.taxes).  Zero if None.

    transaction_date
        Calendar date (date, not datetime) used for replay ordering.
        Derived from tx.transaction_date.

    created_at
        Physical insert timestamp (datetime) used by snapshot_return_recovery
        for created_at-windowed DB queries.  Preserved as-is.
        None if tx.created_at is absent.

    sector
        Preserved verbatim.  None if tx.sector is None or empty string.

    notes
        Preserved verbatim.  None if tx.notes is None or empty string.

    qty_correction_delta
        Pre-parsed signed Decimal for QUANTITY_CORRECTION transactions.
        Sign is extracted from the "Quantity correction: +5.0 shares" pattern
        in tx.notes.  Falls back to Decimal(tx.shares) when notes are absent
        or the pattern is not found — the live engine stores abs(delta) in
        tx.shares and the sign only in tx.notes, so the fallback is positive.
        None for all transaction types other than QUANTITY_CORRECTION.

    realized_pnl
        Pre-parsed float for SELL transactions.  Extracted from the
        "Realized P&L: 500.00" pattern in tx.notes.
        None when the pattern is not found in notes, or when the transaction
        type is not SELL.
        Consumers that need a numeric value when notes are absent should use:
            pnl = ctx.realized_pnl if ctx.realized_pnl is not None else 0.0

    asset_id
        M5 Track B Stage 4 (docs/implementation/M5_TRACK_B_NATIVE_INTEGRATION_TDD.md
        §2.2, §4.3). A plain, read-only reflection of tx.asset_id — never
        resolved here, never a Registry call (purity is preserved exactly as
        before; identity resolution happens once, upstream, at write time —
        services/portfolio_transactions.py, Stage 3).

        Populated only when canonicalize_transactions() is called with
        prefer_asset_id=True; None otherwise (the default). This is the one
        mechanical deviation from §2.2's literal "populated by simply reading
        that column" phrasing — necessary because the per-portfolio cutover
        gate (Portfolio.replay_asset_id_native, §9) has to live somewhere,
        and it cannot live in replay_key.py (test_replay_key.py asserts that
        function's signature stays exactly `(ctx)` — no flag parameter — so
        replay_key() keeps preferring asset_id *whenever present*,
        unconditionally, exactly as §2.1 specifies). Gating whether it is
        ever present is therefore this function's job: a portfolio still on
        legacy keying gets asset_id=None on every CanonicalTransaction it
        produces, so replay_key() naturally, correctly falls through to the
        canonical_symbol tier — with zero changes to replay_key.py itself.
    """

    id:                   int
    transaction_type:     str
    raw_symbol:           str | None
    canonical_symbol:     str | None
    shares:               Decimal
    price_per_share:      Decimal
    total_amount:         Decimal
    fees:                 Decimal
    taxes:                Decimal
    transaction_date:     date
    created_at:           datetime | None
    sector:               str | None
    notes:                str | None
    qty_correction_delta: Decimal | None
    realized_pnl:         float | None
    asset_id:             int | None = None
    position_conversion:  PositionConversionParseResult | None = None


def _canonicalize_one(tx: Any, *, prefer_asset_id: bool = False) -> CanonicalTransaction:
    raw_sym   = tx.symbol.strip().upper() if tx.symbol and tx.symbol.strip() else None
    canon_sym = get_yfinance_symbol(raw_sym) if raw_sym else None

    qty_delta: Decimal | None = None
    if tx.transaction_type == "QUANTITY_CORRECTION":
        notes_str = tx.notes or ""
        m = _QCORR_RE.search(notes_str)
        qty_delta = Decimal(m.group(1)) if m else _to_decimal(tx.shares or "0")

    realized: float | None = None
    if tx.transaction_type == "SELL" and tx.notes:
        m = _REALIZED_RE.search(tx.notes)
        if m:
            realized = float(m.group(1))

    position_conversion: PositionConversionParseResult | None = None
    if tx.transaction_type == "POSITION_CONVERSION":
        position_conversion = parse_position_conversion_payload(
            getattr(tx, "conversion_payload", None)
        )

    tx_date = _to_date(tx.transaction_date)
    if tx_date is None:
        tx_date = date.min   # defensive guard; transaction_date is non-nullable

    return CanonicalTransaction(
        id                   = tx.id,
        transaction_type     = tx.transaction_type or "",
        raw_symbol           = raw_sym,
        canonical_symbol     = canon_sym,
        shares               = _to_decimal(tx.shares),
        price_per_share      = _to_decimal(tx.price_per_share),
        total_amount         = _to_decimal(tx.total_amount),
        fees                 = _to_decimal(tx.fees),
        taxes                = _to_decimal(tx.taxes),
        transaction_date     = tx_date,
        created_at           = _to_datetime(tx.created_at),
        sector               = tx.sector if tx.sector else None,
        notes                = tx.notes if tx.notes else None,
        qty_correction_delta = qty_delta,
        realized_pnl         = realized,
        asset_id             = (getattr(tx, "asset_id", None) if prefer_asset_id else None),
        position_conversion  = position_conversion,
    )


def canonicalize_transactions(
    txs: list[Any],
    *,
    prefer_asset_id: bool = False,
) -> tuple[CanonicalTransaction, ...]:
    """Convert a list of Transaction ORM rows into a sorted immutable tuple.

    Sort order: (transaction_date, id) — matches the ordering used by both
    portfolio_rebuilder and ledger_validator, and is deterministic when
    multiple transactions share the same date.

    Pure function: no database access, no network I/O, no side effects.
    Calling it twice with the same input always produces identical output.

    Args:
        txs: List of SQLAlchemy Transaction objects (or any object with the
             same attribute names — SimpleNamespace is accepted in tests).
        prefer_asset_id: M5 Track B Stage 4. When True, each
            CanonicalTransaction's asset_id is read from tx.asset_id (a
            plain ORM attribute access — no Registry call, purity intact).
            When False (the default), asset_id is always None, which is
            what every pre-Stage-4 caller still gets automatically since
            this parameter is additive. Callers that key replay state by
            replay_key() (portfolio_rebuilder.py, ledger_validator.py) pass
            this per-portfolio, from that portfolio's own
            Portfolio.replay_asset_id_native flag — never globally.

    Returns:
        Immutable tuple of CanonicalTransaction, sorted by (transaction_date, id).
    """
    canonical = [_canonicalize_one(tx, prefer_asset_id=prefer_asset_id) for tx in txs]
    canonical.sort(key=lambda c: (c.transaction_date, c.id))
    return tuple(canonical)
