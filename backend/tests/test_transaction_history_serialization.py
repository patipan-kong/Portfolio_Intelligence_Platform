"""Tests for _tx_row()'s POSITION_CONVERSION detail serialization (main.py).

Covers the additive `conversion_detail` field: it must expose the canonical
POSITION_CONVERSION contract (parsed via
services.transaction_canonicalizer.parse_position_conversion_payload) for
valid payloads, stay None for every other transaction type, and never crash
transaction-history retrieval when a payload is missing or malformed.

ORM rows are simulated with SimpleNamespace objects carrying the same
attribute names as the Transaction SQLAlchemy model — same convention as
test_transaction_canonicalizer.py's `_tx()` factory.
"""
import os
import sys
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import _tx_row


def _tx(
    id: int = 1,
    portfolio_id: int = 4,
    transaction_type: str = "BUY",
    symbol: str | None = "AOT.BK",
    shares: float | None = 100.0,
    price_per_share: float | None = 75.50,
    total_amount: float = 7550.0,
    fees: float = 50.0,
    taxes: float | None = 3.50,
    currency: str = "THB",
    exchange_rate: float = 1.0,
    transaction_date: datetime = datetime(2026, 3, 2, 9, 30),
    created_at: datetime = datetime(2026, 3, 2, 10, 0),
    sector: str | None = "Energy",
    notes: str | None = None,
    execution_decision_id: int | None = None,
    conversion_payload: dict | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=id,
        portfolio_id=portfolio_id,
        transaction_type=transaction_type,
        symbol=symbol,
        shares=shares,
        price_per_share=price_per_share,
        total_amount=total_amount,
        fees=fees,
        taxes=taxes,
        currency=currency,
        exchange_rate=exchange_rate,
        transaction_date=transaction_date,
        created_at=created_at,
        sector=sector,
        notes=notes,
        execution_decision_id=execution_decision_id,
        conversion_payload=conversion_payload,
    )


def _conversion_payload(*, cash_in_lieu: dict | None = None) -> dict:
    return {
        "schema_version": 1,
        "predecessor": {
            "asset_id": 27,
            "symbol": "BANPU.BK",
            "shares_surrendered": "6700",
        },
        "successor": {
            "asset_id": 123,
            "symbol": "BANPUU.BK",
            "provider_symbol": "BANPUU.BK",
            "shares_entitled": "2562.214",
            "shares_received": "2562.214" if cash_in_lieu is None else "2562",
        },
        "conversion_ratio": "0.38242",
        "basis": {
            "before": "48709.00",
            "allocated_to_cash_in_lieu": "0.00" if cash_in_lieu is None else "4.07",
            "carried_to_successor": "48709.00" if cash_in_lieu is None else "48704.93",
        },
        "cash_in_lieu": cash_in_lieu,
        "dates": {
            "legal_effective_date": "2026-03-02",
            "valuation_transition_date": "2026-03-02",
            "predecessor_last_price_date": "2026-03-01",
            "successor_quote_epoch_start_date": "2026-03-02",
        },
        "quote_binding": {
            "provider": "YAHOO",
            "predecessor_provider_symbol": "BANPU.BK",
            "successor_provider_symbol": "BANPUU.BK",
        },
        "boundary_evidence": {
            "predecessor_reference_price": "5.60",
            "successor_reference_price": "14.64",
            "mechanical_nav_tolerance_pct": "0.50",
            "suspension_gap_annotation": "Official transition boundary",
        },
        "evidence": {
            "reference": "BROKER-STATEMENT-1",
            "source": "Broker statement",
            "captured_at": "2026-08-06T10:00:00+07:00",
        },
    }


def _cil_payload() -> dict:
    return _conversion_payload(cash_in_lieu={
        "fractional_entitlement_shares": "0.214",
        "gross_proceeds": "4.50",
        "fees": "0.10",
        "taxes": "0.05",
        "net_cash": "4.35",
        "basis_allocated": "4.07",
        "realized_pnl": "0.28",
    })


def test_valid_position_conversion_payload_is_exposed_correctly():
    row = _tx_row(_tx(transaction_type="POSITION_CONVERSION", conversion_payload=_conversion_payload()))
    detail = row["conversion_detail"]
    assert detail is not None
    assert set(detail) == {
        "predecessor_symbol", "successor_symbol", "conversion_ratio",
        "shares_surrendered", "shares_entitled", "shares_received",
        "legal_effective_date", "valuation_transition_date",
        "cost_basis_before", "cost_basis_carried", "cash_in_lieu",
    }


def test_predecessor_and_successor_identity_survives_serialization():
    row = _tx_row(_tx(transaction_type="POSITION_CONVERSION", conversion_payload=_conversion_payload()))
    detail = row["conversion_detail"]
    assert detail["predecessor_symbol"] == "BANPU.BK"
    assert detail["successor_symbol"] == "BANPUU.BK"


def test_ratio_and_share_quantities_survive_without_semantic_alteration():
    row = _tx_row(_tx(transaction_type="POSITION_CONVERSION", conversion_payload=_conversion_payload()))
    detail = row["conversion_detail"]
    assert detail["conversion_ratio"] == float(Decimal("0.38242"))
    assert detail["shares_surrendered"] == float(Decimal("6700"))
    assert detail["shares_entitled"] == float(Decimal("2562.214"))
    assert detail["shares_received"] == float(Decimal("2562.214"))
    # entitled/received match exactly here (no fractional cash-in-lieu leg) —
    # the caller can rely on this equality without cross-checking cash_in_lieu.
    assert detail["shares_entitled"] == detail["shares_received"]


def test_dates_survive_correctly():
    row = _tx_row(_tx(transaction_type="POSITION_CONVERSION", conversion_payload=_conversion_payload()))
    detail = row["conversion_detail"]
    assert detail["legal_effective_date"] == "2026-03-02"
    assert detail["valuation_transition_date"] == "2026-03-02"


def test_cost_basis_fields_survive_where_present():
    row = _tx_row(_tx(transaction_type="POSITION_CONVERSION", conversion_payload=_conversion_payload()))
    detail = row["conversion_detail"]
    assert detail["cost_basis_before"] == float(Decimal("48709.00"))
    assert detail["cost_basis_carried"] == float(Decimal("48709.00"))
    assert detail["cash_in_lieu"] is None


def test_cash_in_lieu_fields_survive_where_present():
    row = _tx_row(_tx(transaction_type="POSITION_CONVERSION", conversion_payload=_cil_payload()))
    detail = row["conversion_detail"]
    assert detail["shares_entitled"] != detail["shares_received"]  # fractional leg cashed out
    assert detail["cost_basis_carried"] == float(Decimal("48704.93"))
    cil = detail["cash_in_lieu"]
    assert cil is not None
    assert cil["fractional_entitlement_shares"] == float(Decimal("0.214"))
    assert cil["net_cash"] == float(Decimal("4.35"))
    assert cil["realized_pnl"] == float(Decimal("0.28"))


def test_ordinary_transaction_serialization_remains_unchanged():
    row = _tx_row(_tx(transaction_type="BUY"))
    assert row["conversion_detail"] is None
    # every pre-existing field is still present and untouched
    assert row["symbol"] == "AOT.BK"
    assert row["shares"] == 100.0
    assert row["price_per_share"] == 75.50
    assert row["total_amount"] == 7550.0
    assert row["currency"] == "THB"


def test_missing_conversion_payload_does_not_crash_and_is_not_fabricated():
    row = _tx_row(_tx(transaction_type="POSITION_CONVERSION", conversion_payload=None))
    assert row["conversion_detail"] is None


def test_malformed_legacy_conversion_payload_does_not_crash_and_is_not_fabricated():
    row = _tx_row(_tx(transaction_type="POSITION_CONVERSION", conversion_payload={"not": "a conversion payload"}))
    assert row["conversion_detail"] is None
