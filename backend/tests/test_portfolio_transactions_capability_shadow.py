"""Stage R1 (M30.3 brief): portfolio_transactions.py's shadow consultation of
the Asset Definition Runtime via _consult_runtime_for_transaction(), plus the
wiring into execute_buy() / execute_sell() / execute_dividend() /
execute_initial_position().

Fourth Stage R1 consumer, after ledger_validator (M11), asset_registry (M12),
and portfolio_snapshots (M30.2). Mirrors all three: read-only, never raises,
never gates, never changes any computed value. Unlike the batch consumers,
this module handles exactly one symbol per call, so it uses the single-symbol
form (capability_lookup_service.resolve_capability_view).

Coverage:
  1. _consult_runtime_for_transaction() in isolation — agreement / mismatch /
     missing-binding / registry-boot-failure outcomes for both questions this
     module shadows (quantity valuation, dividend flow), plus the symbol=None
     short-circuit (execute_dividend allows a None symbol).
  2. execute_buy() / execute_sell() / execute_initial_position() /
     execute_dividend() end-to-end — the returned dict and the persisted
     Transaction/PortfolioItem/Portfolio rows are unaffected whether the
     consultation agrees, disagrees, or raises outright.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import Base, Portfolio, PortfolioItem, Transaction, Workspace
import models.asset  # noqa: F401 — registers Asset* tables (portfolio_items.asset_id FK target)
import models.registry_finding  # noqa: F401 — registers RegistryFinding table

from services import asset_registry as registry
from services import capability_lookup_service as lookup_service
from services import registry_lookup
from services.asset_domain import AssetClaim, AssetType, IdentifierRecord, IdentifierType
from services.runtime_consultation import RuntimeFindingCategory
import services.portfolio_transactions as txn_module
from services.portfolio_transactions import (
    _consult_runtime_for_transaction,
    execute_buy,
    execute_dividend,
    execute_initial_position,
    execute_sell,
)


# ── Fixtures / helpers ────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def _reset_cache():
    registry_lookup.invalidate_cache()
    yield
    registry_lookup.invalidate_cache()


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def _seed(db, cash: float = 0.0):
    ws = Workspace(name="Test")
    db.add(ws)
    db.flush()
    p = Portfolio(workspace_id=ws.id, name="Test", cash_balance=cash)
    db.add(p)
    db.commit()
    return ws, p


def _mint_with_symbol(db, symbol, asset_type):
    claim = AssetClaim(canonical_symbol=symbol, asset_type=asset_type, market="TH", exchange="SET", currency="THB")
    return registry.mint(
        db, claim,
        identifiers=(IdentifierRecord(identifier_type=IdentifierType.PROVIDER_SYMBOL, value=symbol, source="test"),),
    )


# ── 1. Quantity valuation: agreement / mismatch / missing binding ─────────

def test_quantity_valuation_agrees_for_equity():
    db = make_session()
    _mint_with_symbol(db, "SHADOW_EQ", AssetType.EQUITY)

    log = _consult_runtime_for_transaction(db, "SHADOW_EQ", 1, "quantity_valuation")

    assert log.consulted == 1
    assert log.agreements == 1
    assert log.findings == ()


def test_quantity_valuation_mismatches_for_cash():
    """CASH declares quantity_equals_value=True, so permits_quantity_valuation()
    is False — but execute_buy/sell/initial_position compute
    value = shares × price unconditionally, so this is a real disagreement."""
    db = make_session()
    _mint_with_symbol(db, "SHADOW_CASH", AssetType.CASH)

    log = _consult_runtime_for_transaction(db, "SHADOW_CASH", 42, "quantity_valuation")

    assert log.consulted == 1
    assert log.agreements == 0
    assert len(log.findings) == 1
    finding = log.findings[0]
    assert finding.category == RuntimeFindingCategory.RUNTIME_MISMATCH.value
    assert finding.check_id == "RUNTIME_TRANSACTION_QUANTITY_VALUATION"
    assert finding.binding == "SHADOW_CASH"
    assert finding.transaction_ids == (42,)
    assert finding.legacy_result is True
    assert finding.runtime_result is False


def test_quantity_valuation_missing_binding_for_never_minted_symbol():
    db = make_session()

    log = _consult_runtime_for_transaction(db, "NEVER_MINTED", 1, "quantity_valuation")

    assert len(log.findings) == 1
    finding = log.findings[0]
    assert finding.category == RuntimeFindingCategory.MISSING_BINDING.value
    assert finding.detail == lookup_service._REASON_UNKNOWN_ASSET
    assert finding.runtime_result is None


# ── 2. Dividend flow: agreement / mismatch ─────────────────────────────────

def test_dividend_flow_agrees_for_equity():
    db = make_session()
    _mint_with_symbol(db, "SHADOW_EQ", AssetType.EQUITY)

    log = _consult_runtime_for_transaction(db, "SHADOW_EQ", 1, "dividend_flow")

    assert log.consulted == 1
    assert log.agreements == 1
    assert log.findings == ()


def test_dividend_flow_mismatches_for_bond():
    """BOND grants FlowType.COUPON, not DIVIDEND — but execute_dividend()
    accepts a DIVIDEND transaction for any symbol and credits cash
    unconditionally."""
    db = make_session()
    _mint_with_symbol(db, "SHADOW_BOND", AssetType.BOND)

    log = _consult_runtime_for_transaction(db, "SHADOW_BOND", 7, "dividend_flow")

    assert log.consulted == 1
    assert log.agreements == 0
    assert len(log.findings) == 1
    finding = log.findings[0]
    assert finding.category == RuntimeFindingCategory.RUNTIME_MISMATCH.value
    assert finding.check_id == "RUNTIME_TRANSACTION_DIVIDEND_FLOW"
    assert finding.transaction_ids == (7,)
    assert finding.runtime_result is False


def test_dividend_flow_none_symbol_returns_empty_log():
    """execute_dividend() allows symbol=None (unattributed dividend income) —
    there is nothing to look up, so the consultation is a no-op."""
    db = make_session()

    log = _consult_runtime_for_transaction(db, None, 1, "dividend_flow")

    assert log.consulted == 0
    assert log.findings == ()


# ── 3. Registry boot failure ───────────────────────────────────────────────

def test_registry_boot_failure_yields_missing_binding_never_raises():
    import services.asset_definitions.library as library

    db = make_session()
    _mint_with_symbol(db, "SHADOW_EQ", AssetType.EQUITY)

    original = dict(library.PINNED_FINGERPRINTS)
    try:
        library.PINNED_FINGERPRINTS[(AssetType.CASH.value, "v1")] = "0" * 64
        log = _consult_runtime_for_transaction(db, "SHADOW_EQ", 1, "quantity_valuation")
    finally:
        library.PINNED_FINGERPRINTS.clear()
        library.PINNED_FINGERPRINTS.update(original)

    assert len(log.findings) == 1
    assert log.findings[0].category == RuntimeFindingCategory.MISSING_BINDING.value
    assert log.findings[0].detail == lookup_service._REASON_REGISTRY_BOOT_FAILED


# ── 4. Integration: execute_buy() / execute_dividend() are unaffected ─────

def test_execute_buy_unaffected_by_capability_mismatch(caplog):
    """A CASH-typed symbol (guaranteed quantity-valuation mismatch) must
    still buy exactly as before — the shadow finding is logged, but never
    changes the transaction, holding, or cash balance."""
    db = make_session()
    _mint_with_symbol(db, "SHADOW_CASH", AssetType.CASH)
    ws, p = _seed(db, cash=1_000.0)

    with caplog.at_level("WARNING", logger="services.portfolio_transactions"):
        result = execute_buy(db, ws.id, p.id, "SHADOW_CASH", shares=10.0, price_per_share=2.0)

    assert result["shares"] == 10.0
    assert result["holding"]["shares"] == 10.0
    assert any("RUNTIME_TRANSACTION_QUANTITY_VALUATION" in r.message for r in caplog.records)

    item = db.query(PortfolioItem).filter_by(portfolio_id=p.id, symbol="SHADOW_CASH").first()
    assert item.shares == 10.0


def test_execute_sell_unaffected_by_capability_mismatch(caplog):
    """A CASH-typed symbol (guaranteed quantity-valuation mismatch) must
    still sell exactly as before: the shadow finding is logged exactly once,
    correctly attributed to execute_sell, and cash/holding/persisted
    Transaction/realized P&L all match the documented SELL contract."""
    db = make_session()
    _mint_with_symbol(db, "SHADOW_CASH", AssetType.CASH)
    ws, p = _seed(db, cash=0.0)
    execute_buy(db, ws.id, p.id, "SHADOW_CASH", shares=10.0, price_per_share=2.0)
    avg_cost_before_sell = (
        db.query(PortfolioItem).filter_by(portfolio_id=p.id, symbol="SHADOW_CASH").first().avg_cost
    )
    cash_before_sell = p.cash_balance
    caplog.clear()

    with caplog.at_level("WARNING", logger="services.portfolio_transactions"):
        result = execute_sell(db, ws.id, p.id, "SHADOW_CASH", shares=4.0, price_per_share=3.0)

    # Observability: exactly one quantity-valuation finding, attributed to execute_sell —
    # not merely a matching check_id under some other operation label.
    quantity_valuation_warnings = [
        r for r in caplog.records if "RUNTIME_TRANSACTION_QUANTITY_VALUATION" in r.message
    ]
    assert len(quantity_valuation_warnings) == 1
    assert "runtime consultation finding on execute_sell:" in quantity_valuation_warnings[0].message

    # Business result
    assert result["shares"] == 4.0
    assert result["holding"]["shares"] == 6.0

    # Cash transition: balance moves by exactly the returned net proceeds
    db.refresh(p)
    assert p.cash_balance == pytest.approx(cash_before_sell + result["total_amount"])

    # Persisted holding
    item = db.query(PortfolioItem).filter_by(portfolio_id=p.id, symbol="SHADOW_CASH").first()
    assert item.shares == 6.0

    # Persisted Transaction
    tx = db.query(Transaction).filter_by(
        portfolio_id=p.id, symbol="SHADOW_CASH", transaction_type="SELL"
    ).one()
    assert tx.shares == 4.0
    assert tx.price_per_share == 3.0

    # Realized P&L matches the documented formula (module docstring for execute_sell):
    # (sell_price - avg_cost) × shares - total_sell_fees_incl_vat
    expected_pnl = (3.0 - avg_cost_before_sell) * 4.0 - result["fee_breakdown"]["total_incl_vat"]
    assert result["realized_pnl"] == pytest.approx(expected_pnl)


def test_execute_initial_position_unaffected_by_capability_mismatch(caplog):
    """A CASH-typed symbol (guaranteed quantity-valuation mismatch) must
    still import exactly as before: the shadow finding is logged exactly
    once, correctly attributed to execute_initial_position, cash stays
    neutral, and the persisted Transaction/holding match the onboarding
    import contract."""
    db = make_session()
    _mint_with_symbol(db, "SHADOW_CASH", AssetType.CASH)
    ws, p = _seed(db, cash=0.0)
    cash_before = p.cash_balance

    with caplog.at_level("WARNING", logger="services.portfolio_transactions"):
        result = execute_initial_position(db, ws.id, p.id, "SHADOW_CASH", shares=10.0, avg_cost=2.0)

    # Observability: exactly one quantity-valuation finding, attributed to
    # execute_initial_position — not merely a matching check_id under some
    # other operation label.
    quantity_valuation_warnings = [
        r for r in caplog.records if "RUNTIME_TRANSACTION_QUANTITY_VALUATION" in r.message
    ]
    assert len(quantity_valuation_warnings) == 1
    assert (
        "runtime consultation finding on execute_initial_position:"
        in quantity_valuation_warnings[0].message
    )

    # Business result
    assert result["shares"] == 10.0
    assert result["holding"]["shares"] == 10.0

    # Cash neutrality: onboarding import must never move cash
    db.refresh(p)
    assert p.cash_balance == pytest.approx(cash_before)

    # Persisted holding
    item = db.query(PortfolioItem).filter_by(portfolio_id=p.id, symbol="SHADOW_CASH").first()
    assert item.shares == 10.0

    # Persisted Transaction
    tx = db.query(Transaction).filter_by(
        portfolio_id=p.id, symbol="SHADOW_CASH", transaction_type="INITIAL_POSITION"
    ).one()
    assert tx.shares == 10.0
    assert tx.price_per_share == 2.0


def test_execute_dividend_unaffected_by_capability_mismatch(caplog):
    """A BOND-typed symbol (guaranteed dividend-flow mismatch) must still
    credit cash exactly as before — the shadow finding is logged, never
    enforced."""
    db = make_session()
    _mint_with_symbol(db, "SHADOW_BOND", AssetType.BOND)
    ws, p = _seed(db, cash=0.0)

    with caplog.at_level("WARNING", logger="services.portfolio_transactions"):
        result = execute_dividend(db, ws.id, p.id, "SHADOW_BOND", amount=25.0)

    assert result["cash_balance"] == pytest.approx(25.0)
    assert any("RUNTIME_TRANSACTION_DIVIDEND_FLOW" in r.message for r in caplog.records)

    db.refresh(p)
    assert p.cash_balance == pytest.approx(25.0)


def test_execute_buy_succeeds_even_when_capability_consultation_raises(monkeypatch):
    """Mirrors the same never-raises-out-of-caller proof used by every other
    Stage R1 consumer: even if the consultation itself raised unexpectedly,
    execute_buy() must swallow it and still complete."""
    def _boom(db, symbol, tx_id, kind):
        raise RuntimeError("simulated unexpected failure")

    monkeypatch.setattr(txn_module, "_consult_runtime_for_transaction", _boom)

    db = make_session()
    ws, p = _seed(db, cash=1_000.0)

    result = execute_buy(db, ws.id, p.id, "BOOM.BK", shares=10.0, price_per_share=2.0)

    assert result["shares"] == 10.0
    item = db.query(PortfolioItem).filter_by(portfolio_id=p.id, symbol="BOOM.BK").first()
    assert item is not None
    assert item.shares == 10.0
