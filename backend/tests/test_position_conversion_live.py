"""BANPU-WP4 — live POSITION_CONVERSION materialization (verification matrix
LM-1..LM-15, NMA-1..NMA-4, M1-2/M1-3, EQ-1).

Real in-memory SQLite database (not mocks), mirroring the db_session pattern
already used by test_position_conversion_replay.py. Every conversion row
created by this file is transient and rollback-isolated to a per-test
in-memory database — never a persistent development/production row
(BANPU-WP2 Work Package Plan §1, carried unchanged into WP4 §1.4).

Registry preparation (asset_registry.prepare_position_conversion_registry) is
always performed as its own separate, committed service act before
execute_position_conversion() is invoked (PD-WP4-1) — never inside the
conversion service itself.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, date, timezone
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401 — registers the assets/* tables on Base.metadata
from models.database import Base, Portfolio, PortfolioItem, Transaction, Workspace
from services import asset_registry as registry
from services.asset_domain import AssetClaim, AssetType
from services.asset_registry import AssetRegistryError
from services.portfolio_rebuilder import _replay_with_date_snapshots, rebuild_portfolio
from services.portfolio_transactions import (
    PositionConversionError,
    execute_position_conversion,
)
from services.transaction_canonicalizer import canonicalize_transactions, parse_position_conversion_payload


# ══════════════════════════════════════════════════════════════════════════
# Fixtures and helpers
# ══════════════════════════════════════════════════════════════════════════

@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, expire_on_commit=False)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


def _seed_workspace_and_portfolio(db, *, portfolio_id: int = 1, cash: float = 0.0) -> Portfolio:
    if db.query(Workspace).filter_by(id=1).first() is None:
        db.add(Workspace(id=1, name="Default"))
    portfolio = Portfolio(
        id=portfolio_id, workspace_id=1, name="Test Portfolio",
        cash_balance=cash, created_at=datetime(2025, 1, 1),
    )
    db.add(portfolio)
    db.commit()
    return portfolio


def _mint_and_prepare_registry(
    db,
    *,
    predecessor_symbol: str = "BANPU",
    successor_symbol: str = "BANPUU",
    predecessor_provider_symbol: str = "BANPU.BK",
    successor_provider_symbol: str = "BANPUU.BK",
    prepare: bool = True,
):
    from services.asset_domain import IdentifierRecord, IdentifierType

    predecessor = registry.mint(
        db,
        AssetClaim(canonical_symbol=predecessor_symbol, asset_type=AssetType.EQUITY,
                   market="TH", exchange="SET", currency="THB"),
        identifiers=[IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, predecessor_provider_symbol, source="test")],
    )
    successor = registry.mint(
        db,
        AssetClaim(canonical_symbol=successor_symbol, asset_type=AssetType.EQUITY,
                   market="TH", exchange="SET", currency="THB"),
    )
    if prepare:
        registry.prepare_position_conversion_registry(
            db, predecessor.id, successor.id, successor_provider_symbol, source="test",
        )
    db.commit()
    return predecessor, successor


def _add_holding(db, *, portfolio_id: int, symbol: str, shares: float, avg_cost: float,
                  asset_id: int | None = None, sector: str | None = None) -> PortfolioItem:
    item = PortfolioItem(
        workspace_id=1, portfolio_id=portfolio_id, symbol=symbol,
        shares=shares, avg_cost=avg_cost, asset_id=asset_id, sector=sector,
    )
    db.add(item)
    db.commit()
    return item


def _payload(
    *,
    predecessor_asset_id: int,
    successor_asset_id: int,
    predecessor_symbol: str = "BANPU.BK",
    successor_symbol: str = "BANPUU.BK",
    successor_provider_symbol: str = "BANPUU.BK",
    predecessor_provider_symbol: str = "BANPU.BK",
    shares_surrendered: str = "6700",
    conversion_ratio: str = "0.38242",
    shares_received: str = "2562.214",
    basis_before: str = "48709.00",
    basis_allocated: str = "0.00",
    basis_carried: str = "48709.00",
    cash_in_lieu: dict | None = None,
    valuation_transition_date: str = "2026-03-02",
) -> dict:
    shares_entitled = str(Decimal(shares_surrendered) * Decimal(conversion_ratio))
    return {
        "schema_version": 1,
        "predecessor": {
            "asset_id": predecessor_asset_id,
            "symbol": predecessor_symbol,
            "shares_surrendered": shares_surrendered,
        },
        "successor": {
            "asset_id": successor_asset_id,
            "symbol": successor_symbol,
            "provider_symbol": successor_provider_symbol,
            "shares_entitled": shares_entitled,
            "shares_received": shares_received,
        },
        "conversion_ratio": conversion_ratio,
        "basis": {
            "before": basis_before,
            "allocated_to_cash_in_lieu": basis_allocated,
            "carried_to_successor": basis_carried,
        },
        "cash_in_lieu": cash_in_lieu,
        "dates": {
            "legal_effective_date": valuation_transition_date,
            "valuation_transition_date": valuation_transition_date,
            "predecessor_last_price_date": "2026-03-01",
            "successor_quote_epoch_start_date": valuation_transition_date,
        },
        "quote_binding": {
            "provider": "YAHOO",
            "predecessor_provider_symbol": predecessor_provider_symbol,
            "successor_provider_symbol": successor_provider_symbol,
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


def _cil_payload(**overrides) -> dict:
    """A payload with a real fractional cash-in-lieu leg (Qr < Qe)."""
    defaults = dict(
        shares_received="2562",
        basis_before="48709.00",
        basis_allocated="4.07",
        basis_carried="48704.93",
        cash_in_lieu={
            "fractional_entitlement_shares": "0.214",
            "gross_proceeds": "4.50",
            "fees": "0.10",
            "taxes": "0.05",
            "net_cash": "4.35",
            "basis_allocated": "4.07",
            "realized_pnl": "0.28",
        },
    )
    defaults.update(overrides)
    return _payload(**defaults)


def _add_initial_position_ledger_row(
    db,
    *,
    portfolio_id: int,
    asset_id: int,
    symbol: str = "BANPU.BK",
    shares: float = 6700,
    basis: float = 48709.0,
    tx_id: int | None = None,
) -> Transaction:
    tx = Transaction(
        id=tx_id,
        workspace_id=1,
        portfolio_id=portfolio_id,
        symbol=symbol,
        transaction_type="INITIAL_POSITION",
        shares=shares,
        price_per_share=basis / shares,
        total_amount=basis,
        fees=0.0,
        taxes=0.0,
        transaction_date=datetime(2020, 1, 1),
        asset_id=asset_id,
    )
    db.add(tx)
    db.commit()
    return tx


def _frozen_replay_realized_pnl(db, portfolio_id: int) -> Decimal:
    rows = db.query(Transaction).filter_by(portfolio_id=portfolio_id).all()
    canonical = canonicalize_transactions(rows, prefer_asset_id=True)
    final_date = max(tx.transaction_date for tx in canonical).isoformat()
    state = _replay_with_date_snapshots(list(canonical), [final_date])[final_date]
    return state.cumulative_realized_pnl


def _insert_existing_conversion_row(
    db,
    payload: dict,
    *,
    workspace_id: int = 1,
    symbol: str = "BANPU.BK",
    shares: float = 2562.214,
    price_per_share: float = 48709.00 / 2562.214,
    total_amount: float = 48709.00,
    fees: float = 0.0,
    taxes: float = 0.0,
) -> Transaction:
    row = Transaction(
        workspace_id=workspace_id,
        portfolio_id=1,
        symbol=symbol,
        transaction_type="POSITION_CONVERSION",
        shares=shares,
        price_per_share=price_per_share,
        total_amount=total_amount,
        fees=fees,
        taxes=taxes,
        transaction_date=datetime(2026, 3, 2),
        asset_id=payload["predecessor"]["asset_id"],
        conversion_payload=payload,
    )
    db.add(row)
    db.commit()
    return row


# ══════════════════════════════════════════════════════════════════════════
# LM-1 .. LM-4 — success, merge, no-CIL, CIL
# ══════════════════════════════════════════════════════════════════════════

def test_lm1_successful_conversion(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=1000.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id, sector="Energy")

    result = execute_position_conversion(
        db, ws_id=1, portfolio_id=1,
        conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
    )

    assert result["status"] == "applied"
    items = {i.symbol: i for i in db.query(PortfolioItem).filter_by(portfolio_id=1).all()}
    assert "BANPU.BK" not in items
    assert "BANPUU.BK" in items
    successor_item = items["BANPUU.BK"]
    assert successor_item.shares == pytest.approx(2562.214, abs=1e-6)
    assert successor_item.avg_cost == pytest.approx(48709.00 / 2562.214, abs=1e-4)
    assert successor_item.asset_id == successor.id
    assert successor_item.sector == "Energy"


def test_lm2_existing_successor_merge(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    _add_holding(db, portfolio_id=1, symbol="BANPUU.BK", shares=100, avg_cost=10.0,
                 asset_id=successor.id, sector="Energy")

    execute_position_conversion(
        db, ws_id=1, portfolio_id=1,
        conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
    )

    successor_item = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPUU.BK").one()
    expected_shares = Decimal("100") + Decimal("2562.214")
    expected_basis = Decimal("100") * Decimal("10.0") + Decimal("48709.00")
    assert successor_item.shares == pytest.approx(float(expected_shares), abs=1e-6)
    assert successor_item.avg_cost == pytest.approx(float(expected_basis / expected_shares), abs=1e-4)
    assert successor_item.sector == "Energy"  # existing sector preserved


def test_lm3_no_cil_cash_and_realized_pnl_unchanged(db_session):
    """LM-3: compare cumulative realized-P/L before and after no-CIL."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=1234.56)
    predecessor, successor = _mint_and_prepare_registry(db)
    predecessor_id, successor_id = predecessor.id, successor.id
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    _add_initial_position_ledger_row(db, portfolio_id=1, asset_id=predecessor_id)

    db.add(Transaction(
        workspace_id=1, portfolio_id=1, symbol="OTHERSTOCK",
        transaction_type="INITIAL_POSITION", shares=10, price_per_share=75.0,
        total_amount=750.0, fees=0.0, taxes=0.0,
        transaction_date=datetime(2025, 1, 1),
    ))
    prior_sell = Transaction(
        workspace_id=1, portfolio_id=1, symbol="OTHERSTOCK",
        transaction_type="SELL", shares=10, price_per_share=100.0,
        total_amount=1000.0, fees=0.0, taxes=0.0,
        transaction_date=datetime(2025, 6, 1),
        notes="Realized P&L: +250.0000",
    )
    db.add(prior_sell)
    db.commit()
    realized_before = _frozen_replay_realized_pnl(db, 1)
    assert realized_before == Decimal("250.0")
    db.rollback()

    result = execute_position_conversion(
        db, ws_id=1, portfolio_id=1,
        conversion_payload=_payload(predecessor_asset_id=predecessor_id, successor_asset_id=successor_id),
    )

    assert result["cash_balance"] == pytest.approx(1234.56, abs=1e-6)
    assert _frozen_replay_realized_pnl(db, 1) == realized_before


def test_lm4_cil_applies_only_admitted_cash_and_fees_once(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    predecessor_id, successor_id = predecessor.id, successor.id
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    _add_initial_position_ledger_row(db, portfolio_id=1, asset_id=predecessor_id)
    realized_before = _frozen_replay_realized_pnl(db, 1)
    assert realized_before == Decimal("0")
    db.rollback()

    result = execute_position_conversion(
        db, ws_id=1, portfolio_id=1,
        conversion_payload=_cil_payload(predecessor_asset_id=predecessor_id, successor_asset_id=successor_id),
    )

    assert result["cash_balance"] == pytest.approx(4.35, abs=1e-6)  # net_cash only
    tx = db.query(Transaction).filter_by(id=result["transaction_id"]).one()
    assert tx.fees == pytest.approx(0.10, abs=1e-6)
    assert tx.taxes == pytest.approx(0.05, abs=1e-6)

    # The replayed cumulative outcome below proves the admitted realized P/L
    # is applied exactly once; the top-level columns independently prove the
    # cash, fee, tax, and carried-basis projections.
    assert Decimal(str(tx.total_amount)) == Decimal("48704.93")
    realized_after = _frozen_replay_realized_pnl(db, 1)
    assert realized_after - realized_before == Decimal("0.28")

    db.rollback()
    retry = execute_position_conversion(
        db, ws_id=1, portfolio_id=1,
        conversion_payload=_cil_payload(
            predecessor_asset_id=predecessor_id,
            successor_asset_id=successor_id,
        ),
    )
    assert retry["status"] == "already_applied"
    assert _frozen_replay_realized_pnl(db, 1) == realized_after


# ══════════════════════════════════════════════════════════════════════════
# LM-5, LM-6 — stale optimistic expectations
# ══════════════════════════════════════════════════════════════════════════

def test_lm5_stale_quantity_expectation_fails_closed(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6500, avg_cost=48709.00 / 6500,
                 asset_id=predecessor.id)  # held shares != payload's 6700

    with pytest.raises(PositionConversionError):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
        )

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(portfolio_id=1).count() == 0
    assert db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPU.BK").one().shares == 6500


def test_lm6_stale_basis_expectation_fails_closed(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=5.0,  # basis = 33500, not 48709
                 asset_id=predecessor.id)

    with pytest.raises(PositionConversionError):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
        )

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(portfolio_id=1).count() == 0


# ══════════════════════════════════════════════════════════════════════════
# LM-7, LM-8, LM-9 — registry mismatches
# ══════════════════════════════════════════════════════════════════════════

def test_lm7_successor_registry_mismatch_fails_closed(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db, prepare=False)
    # Registry never prepared — successor has no current PROVIDER_SYMBOL identifier.
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    with pytest.raises(AssetRegistryError):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
        )

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(portfolio_id=1).count() == 0


def test_lm8_predecessor_status_mismatch_fails_closed(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db, prepare=False)
    # Prepare only the successor identifier; predecessor is left ACTIVE / not retired.
    from services.asset_domain import IdentifierRecord, IdentifierType
    registry.attach_identifier(
        db, successor.id, IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "BANPUU.BK", source="test"),
    )
    db.commit()
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    with pytest.raises(AssetRegistryError):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
        )

    assert db.query(Transaction).filter_by(portfolio_id=1).count() == 0


def test_lm9_merged_into_mismatch_fails_closed(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    other_predecessor, _ = _mint_and_prepare_registry(
        db, predecessor_symbol="OTHERPRED", successor_symbol="OTHERSUCC",
        predecessor_provider_symbol="OTHERPRED.BK", successor_provider_symbol="OTHERSUCC.BK",
    )
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    with pytest.raises(AssetRegistryError):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            # successor_asset_id points at an unrelated asset, not predecessor's actual MERGED_INTO target
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=other_predecessor.id),
        )


# ══════════════════════════════════════════════════════════════════════════
# LM-10, LM-11 — atomicity and forced rollback
# ══════════════════════════════════════════════════════════════════════════

def test_lm10_forced_rollback_leaves_no_row_and_no_materialized_state(db_session, monkeypatch):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=500.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    real_commit = db.commit
    def _boom():
        raise RuntimeError("forced database-session failure at commit")
    monkeypatch.setattr(db, "commit", _boom)

    with pytest.raises(RuntimeError):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
        )

    monkeypatch.setattr(db, "commit", real_commit)
    assert db.in_transaction() is False

    assert db.query(Transaction).filter_by(portfolio_id=1, transaction_type="POSITION_CONVERSION").count() == 0
    predecessor_item = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPU.BK").one_or_none()
    assert predecessor_item is not None and predecessor_item.shares == 6700
    assert db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPUU.BK").one_or_none() is None
    assert db.query(Portfolio).filter_by(id=1).one().cash_balance == pytest.approx(500.0, abs=1e-6)


def test_lm11_atomicity_no_row_without_state_no_state_without_row(db_session, monkeypatch):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    predecessor_id, successor_id = predecessor.id, successor.id
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    result = execute_position_conversion(
        db, ws_id=1, portfolio_id=1,
        conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
    )

    tx_exists = db.query(Transaction).filter_by(id=result["transaction_id"]).one_or_none() is not None
    state_exists = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPUU.BK").one_or_none() is not None
    assert tx_exists and state_exists

    db.rollback()
    _seed_workspace_and_portfolio(db, portfolio_id=2, cash=500.0)
    _add_holding(
        db, portfolio_id=2, symbol="BANPU.BK", shares=6700,
        avg_cost=48709.00 / 6700, asset_id=predecessor.id,
    )
    real_commit = db.commit

    def _fail_commit():
        raise RuntimeError("LM-11 forced commit failure")

    monkeypatch.setattr(db, "commit", _fail_commit)
    with pytest.raises(RuntimeError, match="LM-11"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=2,
            conversion_payload=_payload(
                predecessor_asset_id=predecessor_id,
                successor_asset_id=successor_id,
                valuation_transition_date="2026-03-03",
            ),
        )
    monkeypatch.setattr(db, "commit", real_commit)

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(
        portfolio_id=2, transaction_type="POSITION_CONVERSION",
    ).count() == 0
    assert db.query(PortfolioItem).filter_by(
        portfolio_id=2, symbol="BANPUU.BK",
    ).one_or_none() is None
    predecessor_after = db.query(PortfolioItem).filter_by(
        portfolio_id=2, symbol="BANPU.BK",
    ).one()
    assert predecessor_after.shares == 6700
    assert db.query(Portfolio).filter_by(id=2).one().cash_balance == pytest.approx(500.0)


# ══════════════════════════════════════════════════════════════════════════
# LM-12 — transaction 83 / prior ledger preservation
# ══════════════════════════════════════════════════════════════════════════

def test_lm12_transaction_83_and_prior_ledger_rows_untouched(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    historical = Transaction(
        id=83, workspace_id=1, portfolio_id=1, symbol="BANPU.BK",
        transaction_type="INITIAL_POSITION", shares=6700, price_per_share=48709.00 / 6700,
        total_amount=48709.00, fees=0.0, taxes=0.0, transaction_date=datetime(2020, 1, 1),
        notes="historical import",
    )
    db.add(historical)
    db.commit()
    snapshot = dict(
        id=historical.id, symbol=historical.symbol, shares=historical.shares,
        total_amount=historical.total_amount, transaction_date=historical.transaction_date,
        notes=historical.notes,
    )

    execute_position_conversion(
        db, ws_id=1, portfolio_id=1,
        conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
    )

    reloaded = db.query(Transaction).filter_by(id=83).one()
    assert reloaded.symbol == snapshot["symbol"]
    assert reloaded.shares == snapshot["shares"]
    assert reloaded.total_amount == snapshot["total_amount"]
    assert reloaded.transaction_date == snapshot["transaction_date"]
    assert reloaded.notes == snapshot["notes"]


# ══════════════════════════════════════════════════════════════════════════
# LM-13 — no public endpoint or frontend authoring path
# ══════════════════════════════════════════════════════════════════════════

def test_lm13_no_public_endpoint_or_cli_references_execute_position_conversion():
    """manage.py is excluded from this scan because it is the intentional
    internal CLI owner/caller of execute_position_conversion, not a public
    entry point; main.py and the routers/ public API surface remain scanned
    and prohibited unchanged."""
    import os

    backend_dir = os.path.join(os.path.dirname(__file__), "..")
    surfaces = [
        os.path.join(backend_dir, "main.py"),
    ]
    routers_dir = os.path.join(backend_dir, "routers")
    if os.path.isdir(routers_dir):
        for name in os.listdir(routers_dir):
            if name.endswith(".py"):
                surfaces.append(os.path.join(routers_dir, name))

    for path in surfaces:
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as fh:
            contents = fh.read()
        assert "execute_position_conversion" not in contents, (
            f"unexpected reference to execute_position_conversion in {path}"
        )


def test_lm13_no_frontend_authoring_path_for_position_conversion():
    """WP4-IIR-B6: LM-13's named surface includes frontend authoring — the
    prior test only scanned backend entry points. Scans every frontend
    source file for both the Python service name (which would be
    nonsensical there, but a copy-paste reference is still a defect) and
    any position-conversion-shaped API path a caller might have wired up
    without a corresponding backend endpoint existing."""
    import os
    import re

    backend_dir = os.path.join(os.path.dirname(__file__), "..")
    repo_root = os.path.join(backend_dir, "..")
    frontend_dir = os.path.join(repo_root, "frontend")
    assert os.path.isdir(frontend_dir), f"expected frontend directory at {frontend_dir}"

    endpoint_pattern = re.compile(r"position[-_]conversion", re.IGNORECASE)
    skip_dirs = {"node_modules", ".next", ".vercel", "dist", "build", "coverage", "graphify-out"}
    scanned = 0
    for root, dirnames, filenames in os.walk(frontend_dir):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for name in filenames:
            if not name.endswith((".ts", ".tsx", ".js", ".jsx")):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8", errors="ignore") as fh:
                contents = fh.read()
            scanned += 1
            assert "execute_position_conversion" not in contents, (
                f"unexpected reference to execute_position_conversion in {path}"
            )
            assert endpoint_pattern.search(contents) is None, (
                f"unexpected position-conversion endpoint reference in {path}"
            )

    assert scanned > 0, "expected at least one frontend source file to be scanned"


# ══════════════════════════════════════════════════════════════════════════
# LM-14, LM-15 — canonical-fingerprint idempotency (C-6 / M1-2 / M1-3)
# ══════════════════════════════════════════════════════════════════════════

def test_lm14_matching_retry_is_a_no_op(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)

    first = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)
    cash_after_first = db.query(Portfolio).filter_by(id=1).one().cash_balance
    tx_count_after_first = db.query(Transaction).filter_by(portfolio_id=1, transaction_type="POSITION_CONVERSION").count()
    db.rollback()

    second = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert second["status"] == "already_applied"
    assert second["transaction_id"] == first["transaction_id"]
    assert db.query(Transaction).filter_by(portfolio_id=1, transaction_type="POSITION_CONVERSION").count() == tx_count_after_first
    assert db.query(Portfolio).filter_by(id=1).one().cash_balance == pytest.approx(cash_after_first, abs=1e-9)


def test_lm15_conflicting_retry_fails_hard(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    first_payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=first_payload)

    # Same portfolio/predecessor/transition-date key, but a materially
    # different payload (different reference price) — distinct canonical
    # fingerprint at the same identity key must hard-fail, never silently
    # collide because of Decimal serialization precision (M1-3/M1-4).
    conflicting_payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    conflicting_payload["boundary_evidence"]["predecessor_reference_price"] = "5.61"

    with pytest.raises(PositionConversionError):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=conflicting_payload)


# ══════════════════════════════════════════════════════════════════════════
# NMA-1 .. NMA-4 — naive-midnight transaction_date authoring
# ══════════════════════════════════════════════════════════════════════════

def test_nma1_valid_payload_date_stores_naive_midnight(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    result = execute_position_conversion(
        db, ws_id=1, portfolio_id=1,
        conversion_payload=_payload(
            predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
            valuation_transition_date="2026-03-02",
        ),
    )

    tx = db.query(Transaction).filter_by(id=result["transaction_id"]).one()
    assert tx.transaction_date == datetime(2026, 3, 2, 0, 0, 0)
    assert tx.transaction_date.tzinfo is None
    assert tx.transaction_date.date() == date(2026, 3, 2)


def test_nma2_offset_bearing_date_string_rejected_before_insertion(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    payload["dates"]["valuation_transition_date"] = "2026-03-02T10:00:00+07:00"  # offset-bearing, not a plain date

    with pytest.raises(PositionConversionError):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert db.query(Transaction).filter_by(portfolio_id=1).count() == 0
    assert db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPU.BK").one().shares == 6700


def test_nma3_time_bearing_non_midnight_date_string_rejected_before_insertion(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    payload["dates"]["valuation_transition_date"] = "2026-03-02T10:00:00"  # time-bearing, non-midnight

    with pytest.raises(PositionConversionError):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert db.query(Transaction).filter_by(portfolio_id=1).count() == 0


def test_nma4_stored_date_equals_payload_calendar_date_independent_of_host_timezone(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    result = execute_position_conversion(
        db, ws_id=1, portfolio_id=1,
        conversion_payload=_payload(
            predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
            valuation_transition_date="2026-03-02",
        ),
    )

    tx = db.query(Transaction).filter_by(id=result["transaction_id"]).one()
    payload_date = date.fromisoformat("2026-03-02")
    # No astimezone()/utcnow()/host-timezone conversion participates —
    # direct calendar-date comparison, independent of session/host timezone.
    assert tx.transaction_date.date() == payload_date


# ══════════════════════════════════════════════════════════════════════════
# EQ-1 — live outcome equals frozen WP2 replay outcome
# ══════════════════════════════════════════════════════════════════════════

def _run_async_isolated(coro):
    """Runs ``coro`` to completion via ``asyncio.run()``, then restores a
    fresh current event loop for this thread afterward.

    WP4-IIR-B6: ``asyncio.run()`` unconditionally clears the thread's
    current event loop (``asyncio.set_event_loop(None)``) when it finishes.
    In a combined-process pytest run, later-collected legacy tests that
    still use the ``asyncio.get_event_loop().run_until_complete(...)``
    pattern (e.g. test_fee_accounting.py) then find no current loop and
    fail — a real test-isolation defect the independent review reproduced
    (`730 passed, 3 failed` in one combined-process run: the known
    pre-existing capability-shadow failure plus two fee-accounting
    event-loop failures). This helper contains that side effect to this
    test alone rather than reaching into test_fee_accounting.py, which is
    outside WP4's authorized surface.
    """
    try:
        return asyncio.run(coro)
    finally:
        asyncio.set_event_loop(asyncio.new_event_loop())


def test_eq1_live_outcome_equals_frozen_replay_outcome(db_session):
    """Applies the same conversion through both engines on parallel,
    independently-seeded portfolios in one rollback-isolated in-memory
    database, and asserts identical shares/basis/cash/successor identity,
    plus realized P/L (WP4-IIR-B6 — the Work Package Plan's EQ-1 row
    requires this comparison; WP4 test authority does not extend to
    inventing a later-package exemption for it).

    Realized P/L is derived independently from live materialized cash/basis
    deltas and from the frozen replay engine's cumulative accounting state.
    """
    db = db_session
    live_portfolio_before = _seed_workspace_and_portfolio(db, portfolio_id=1, cash=0.0)  # live path
    _seed_workspace_and_portfolio(db, portfolio_id=2, cash=0.0)  # replay path
    predecessor, successor = _mint_and_prepare_registry(db)

    payload = _cil_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)

    # Live path: portfolio 1. Capture the predecessor's materialized basis
    # and the portfolio's materialized cash BEFORE conversion -- these,
    # together with the successor's and portfolio's materialized state
    # AFTER conversion (queried below), are the only inputs the live
    # realized-P/L derivation may use (WP4-IIR-B6 second-renewed
    # correction). Reads the already-loaded ORM objects' attributes rather
    # than issuing a fresh query -- db_session's expire_on_commit=False
    # keeps them populated post-commit without opening a new implicit
    # transaction, preserving execute_position_conversion()'s idle-Session
    # requirement (WP4-IIR-B4).
    predecessor_holding = _add_holding(
        db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
        asset_id=predecessor.id,
    )
    predecessor_basis_before = Decimal(str(predecessor_holding.shares)) * Decimal(str(predecessor_holding.avg_cost))
    cash_before_live = Decimal(str(live_portfolio_before.cash_balance))
    live_result = execute_position_conversion(
        db, ws_id=1, portfolio_id=1, conversion_payload=payload,
    )
    live_successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPUU.BK").one()

    # Replay path: portfolio 2, built purely from the raw ledger.
    db.add(Transaction(
        id=901, workspace_id=1, portfolio_id=2, symbol="BANPU.BK",
        transaction_type="INITIAL_POSITION", shares=6700, price_per_share=48709.00 / 6700,
        total_amount=48709.00, fees=0.0, taxes=0.0, transaction_date=datetime(2020, 1, 1),
        asset_id=predecessor.id,
    ))
    shares_received = Decimal(payload["successor"]["shares_received"])
    basis_carried = Decimal(payload["basis"]["carried_to_successor"])
    cil = payload["cash_in_lieu"]
    db.add(Transaction(
        id=902, workspace_id=1, portfolio_id=2, symbol="BANPU.BK",
        transaction_type="POSITION_CONVERSION",
        shares=float(shares_received), price_per_share=float(basis_carried / shares_received),
        total_amount=float(basis_carried), fees=float(Decimal(cil["fees"])), taxes=float(Decimal(cil["taxes"])),
        transaction_date=datetime(2026, 3, 2), asset_id=predecessor.id,
        conversion_payload=payload,
    ))
    db.commit()

    replay_result = _run_async_isolated(rebuild_portfolio(
        db=db, portfolio_id=2, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert replay_result.success is True
    assert replay_result.committed is True
    replay_successor = db.query(PortfolioItem).filter_by(portfolio_id=2, symbol="BANPUU.BK").one()
    replay_portfolio = db.query(Portfolio).filter_by(id=2).one()
    live_portfolio = db.query(Portfolio).filter_by(id=1).one()

    assert live_successor.shares == pytest.approx(replay_successor.shares, abs=1e-6)
    assert live_successor.avg_cost == pytest.approx(replay_successor.avg_cost, abs=1e-4)
    assert live_successor.asset_id == replay_successor.asset_id == successor.id
    assert live_portfolio.cash_balance == pytest.approx(replay_portfolio.cash_balance, abs=1e-6)
    assert live_result["cash_balance"] == pytest.approx(live_portfolio.cash_balance, abs=1e-9)

    # Independently derive the live outcome from observed materialized cash
    # delta and actual successor materialized basis (WP4-IIR-B6
    # second-renewed correction) -- never from live_result["basis_carried"],
    # which is populated directly from the input payload (the exact proxy
    # the second-renewed review rejected as not independently derived).
    # live_successor.shares/.avg_cost are the actual PortfolioItem columns
    # E13 itself asserted post-write; predecessor_basis_before and
    # cash_before_live were captured from materialized state prior to the
    # call, above -- no leg of this computation reads the conversion
    # payload.
    live_cash_delta = Decimal(str(live_portfolio.cash_balance)) - cash_before_live
    live_successor_basis = Decimal(str(live_successor.shares)) * Decimal(str(live_successor.avg_cost))
    live_basis_allocated = predecessor_basis_before - live_successor_basis
    live_realized_pnl = live_cash_delta - live_basis_allocated
    replay_realized_pnl = _frozen_replay_realized_pnl(db, 2)
    assert replay_realized_pnl == Decimal("0.28")
    # THB 0.01 tolerance -- the same absolute basis tolerance already used
    # throughout this service (E6, E13) -- because live_successor_basis is
    # reconstructed from the actually-persisted, _f()-quantized avg_cost
    # column, not from unrounded payload arithmetic.
    assert abs(live_realized_pnl - replay_realized_pnl) <= Decimal("0.01")


# ══════════════════════════════════════════════════════════════════════════
# BANPU-WP4 Retry-Order correction evidence (WP4-IIR-B1..B6, RTO-1..13)
#
# The Retry-Order Work Package Plan Amendment (independently reapproved)
# refines Plan §3.2's runtime order at the retry-disposition point (E8-R)
# and requires RTO-1..13 evidence in addition to the original LM/NMA/M1/EQ
# matrix above. These tests exercise that evidence directly, alongside the
# WP4-IIR-B2, B4, and B5 corrections.
# ══════════════════════════════════════════════════════════════════════════

def test_wp4_iir_b2_caller_supplied_symbol_cannot_redirect_conversion(db_session):
    """WP4-IIR-B2: a mismatching caller-supplied payload symbol must not
    redirect holdings lookup or become the persisted transaction/holding
    symbol. Asset IDs remain authoritative; only the registry-resolved
    display symbol is ever written or matched against."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    predecessor_id, successor_id = predecessor.id, successor.id
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    payload["predecessor"]["symbol"] = "CALLER-PREDECESSOR"
    payload["successor"]["symbol"] = "CALLER-SUCCESSOR"

    result = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert result["status"] == "applied"
    assert result["successor_symbol"] == "BANPUU.BK"
    tx = db.query(Transaction).filter_by(id=result["transaction_id"]).one()
    assert tx.symbol == "BANPU.BK"
    assert tx.conversion_payload["predecessor"]["symbol"] == "BANPU.BK"
    assert tx.conversion_payload["successor"]["symbol"] == "BANPUU.BK"
    stored = parse_position_conversion_payload(tx.conversion_payload)
    assert stored.is_valid and stored.value is not None
    assert stored.value.fingerprint == result["fingerprint"]

    items = {i.symbol: i for i in db.query(PortfolioItem).filter_by(portfolio_id=1).all()}
    assert "CALLER-PREDECESSOR" not in items
    assert "CALLER-SUCCESSOR" not in items
    assert "BANPU.BK" not in items
    assert "BANPUU.BK" in items
    assert items["BANPUU.BK"].asset_id == successor.id

    db.rollback()
    differently_false = _payload(
        predecessor_asset_id=predecessor_id,
        successor_asset_id=successor_id,
        predecessor_symbol="ANOTHER-CALLER-PREDECESSOR",
        successor_symbol="ANOTHER-CALLER-SUCCESSOR",
    )
    retry = execute_position_conversion(
        db, ws_id=1, portfolio_id=1, conversion_payload=differently_false,
    )
    assert retry["status"] == "already_applied"
    assert retry["transaction_id"] == result["transaction_id"]


def test_wp4_iir_b2_caller_supplied_predecessor_provider_symbol_cannot_survive_or_alter_fingerprint(db_session):
    """WP4-IIR-B2 second-renewed correction: an arbitrary caller-supplied
    ``quote_binding.predecessor_provider_symbol`` label must not survive
    into the persisted canonical payload and must not independently alter
    the canonical fingerprint or retry disposition -- it is always
    overwritten with the registry-derived value (the predecessor's own
    retired PROVIDER_SYMBOL identifier). Two requests differing only in
    that caller-supplied label must resolve to the identical persisted
    payload, identical fingerprint, and a matching (not conflicting)
    retry."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    predecessor_id, successor_id = predecessor.id, successor.id
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    payload = _payload(
        predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        predecessor_provider_symbol="CALLER-PROVIDER-PRE-A",
    )
    result = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert result["status"] == "applied"
    tx = db.query(Transaction).filter_by(id=result["transaction_id"]).one()
    assert tx.conversion_payload["quote_binding"]["predecessor_provider_symbol"] == "BANPU.BK"
    assert tx.conversion_payload["quote_binding"]["predecessor_provider_symbol"] != "CALLER-PROVIDER-PRE-A"
    stored = parse_position_conversion_payload(tx.conversion_payload)
    assert stored.is_valid and stored.value is not None
    assert stored.value.fingerprint == result["fingerprint"]

    db.rollback()
    differently_false = _payload(
        predecessor_asset_id=predecessor_id, successor_asset_id=successor_id,
        predecessor_provider_symbol="CALLER-PROVIDER-PRE-B",
    )
    retry = execute_position_conversion(
        db, ws_id=1, portfolio_id=1, conversion_payload=differently_false,
    )
    assert retry["status"] == "already_applied"
    assert retry["transaction_id"] == result["transaction_id"]
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == 1


def test_wp4_iir_b5_corrupted_successor_basis_before_e13_fails_and_rolls_back(db_session, monkeypatch):
    """WP4-IIR-B5: E13 must detect a corrupted refreshed successor
    avg_cost/basis immediately before the sole commit and roll back the
    entire transaction — proving the final-invariant assertion is no
    longer fail-open. Mirrors the independent review's own probe technique
    (corrupting the refreshed successor avg_cost immediately before final
    assertions)."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=500.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    real_refresh = db.refresh

    def _corrupting_refresh(instance, *args, **kwargs):
        real_refresh(instance, *args, **kwargs)
        if isinstance(instance, PortfolioItem) and instance.symbol == "BANPUU.BK":
            instance.avg_cost = 999.0

    monkeypatch.setattr(db, "refresh", _corrupting_refresh)

    with pytest.raises(PositionConversionError, match="basis invariant"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
        )

    monkeypatch.setattr(db, "refresh", real_refresh)
    db.rollback()

    assert db.query(Transaction).filter_by(portfolio_id=1, transaction_type="POSITION_CONVERSION").count() == 0
    predecessor_item = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPU.BK").one_or_none()
    assert predecessor_item is not None and predecessor_item.shares == 6700
    assert db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPUU.BK").one_or_none() is None
    assert db.query(Portfolio).filter_by(id=1).one().cash_balance == pytest.approx(500.0, abs=1e-6)


def test_b5_e13_corrupted_transaction_identity_fails_and_rolls_back(db_session, monkeypatch):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=500.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(
        db, portfolio_id=1, symbol="BANPU.BK", shares=6700,
        avg_cost=48709.00 / 6700, asset_id=predecessor.id,
    )
    real_flush = db.flush
    corrupted = False

    def _corrupting_flush(*args, **kwargs):
        nonlocal corrupted
        real_flush(*args, **kwargs)
        if not corrupted:
            for instance in tuple(db.identity_map.values()):
                if isinstance(instance, Transaction) and instance.transaction_type == "POSITION_CONVERSION":
                    instance.asset_id = successor.id
                    instance.symbol = "CORRUPTED"
                    corrupted = True
                    break

    monkeypatch.setattr(db, "flush", _corrupting_flush)
    with pytest.raises(PositionConversionError, match="identity invariant"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(
                predecessor_asset_id=predecessor.id,
                successor_asset_id=successor.id,
            ),
        )
    monkeypatch.setattr(db, "flush", real_flush)

    assert corrupted
    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == 0
    predecessor_item = db.query(PortfolioItem).filter_by(
        portfolio_id=1, symbol="BANPU.BK",
    ).one()
    assert predecessor_item.shares == 6700
    assert predecessor_item.asset_id == predecessor.id
    assert db.query(PortfolioItem).filter_by(
        portfolio_id=1, symbol="BANPUU.BK",
    ).one_or_none() is None
    assert db.query(Portfolio).filter_by(id=1).one().cash_balance == pytest.approx(500.0)


def _corrupt_pending_row_payload_after_first_flush(db, monkeypatch, mutate):
    """WP4-IIR-B5 second-renewed correction test helper: reproduces the
    second-renewed review's own adversarial probe technique -- mutating the
    pending POSITION_CONVERSION transaction row's ``conversion_payload``
    dict in place, in Python memory, after it has already been flushed to
    the database but before the sole commit. ``mutate`` receives the live
    payload dict and edits it in place. Returns a ``corrupted`` flag
    ``list`` (mutable box) the caller can inspect after the call."""
    real_flush = db.flush
    corrupted = [False]

    def _corrupting_flush(*args, **kwargs):
        real_flush(*args, **kwargs)
        if not corrupted[0]:
            for instance in tuple(db.identity_map.values()):
                if isinstance(instance, Transaction) and instance.transaction_type == "POSITION_CONVERSION":
                    mutate(instance.conversion_payload)
                    corrupted[0] = True
                    break

    monkeypatch.setattr(db, "flush", _corrupting_flush)
    return corrupted


def _assert_conversion_fully_rolled_back(db):
    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == 0
    predecessor_item = db.query(PortfolioItem).filter_by(
        portfolio_id=1, symbol="BANPU.BK",
    ).one()
    assert predecessor_item.shares == 6700
    assert predecessor_item.asset_id is not None
    assert db.query(PortfolioItem).filter_by(
        portfolio_id=1, symbol="BANPUU.BK",
    ).one_or_none() is None
    assert db.query(Portfolio).filter_by(id=1).one().cash_balance == pytest.approx(500.0)


def test_wp4_iir_b5_e13_post_flush_predecessor_symbol_corruption_fails_and_rolls_back(db_session, monkeypatch):
    """WP4-IIR-B5 second-renewed correction: E13 must reparse the pending
    row's ACTUAL persisted ``conversion_payload`` -- not the pre-write
    in-memory typed ``payload`` object -- so a post-flush, pre-commit
    mutation of ``tx.conversion_payload`` is detected and rolls back the
    whole transaction, rather than committing fail-open as the
    second-renewed review's probe proved."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=500.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700,
                 avg_cost=48709.00 / 6700, asset_id=predecessor.id)

    corrupted = _corrupt_pending_row_payload_after_first_flush(
        db, monkeypatch,
        lambda payload: payload.__setitem__(
            "predecessor", {**payload["predecessor"], "symbol": "POST-FLUSH-CORRUPTION"},
        ),
    )
    with pytest.raises(PositionConversionError, match="conversion_payload fingerprint"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
        )

    assert corrupted[0]
    db.rollback()
    _assert_conversion_fully_rolled_back(db)


def test_wp4_iir_b5_e13_post_flush_predecessor_provider_symbol_corruption_fails_and_rolls_back(db_session, monkeypatch):
    """WP4-IIR-B5 second-renewed correction, provider variant: a post-flush
    mutation of the pending row's ``quote_binding.predecessor_provider_symbol``
    must be detected exactly like a predecessor-symbol mutation -- E13's
    persisted-payload reparse covers the whole payload, not only the
    symbol fields."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=500.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700,
                 avg_cost=48709.00 / 6700, asset_id=predecessor.id)

    corrupted = _corrupt_pending_row_payload_after_first_flush(
        db, monkeypatch,
        lambda payload: payload["quote_binding"].__setitem__(
            "predecessor_provider_symbol", "POST-FLUSH-PROVIDER-CORRUPTION",
        ),
    )
    with pytest.raises(PositionConversionError, match="conversion_payload fingerprint"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
        )

    assert corrupted[0]
    db.rollback()
    _assert_conversion_fully_rolled_back(db)


def test_wp4_iir_b5_e13_post_flush_numeric_payload_field_corruption_fails_and_rolls_back(db_session, monkeypatch):
    """WP4-IIR-B5 second-renewed correction, numeric variant: a post-flush
    mutation of a numeric payload field (here, the boundary-evidence
    mechanical NAV tolerance -- chosen because it carries no cross-field
    invariant that would instead surface as a parse failure) must also be
    detected by E13's persisted-payload fingerprint check."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=500.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700,
                 avg_cost=48709.00 / 6700, asset_id=predecessor.id)

    corrupted = _corrupt_pending_row_payload_after_first_flush(
        db, monkeypatch,
        lambda payload: payload["boundary_evidence"].__setitem__(
            "mechanical_nav_tolerance_pct", "9.99",
        ),
    )
    with pytest.raises(PositionConversionError, match="conversion_payload fingerprint"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id),
        )

    assert corrupted[0]
    db.rollback()
    _assert_conversion_fully_rolled_back(db)


def test_wp4_iir_b4_invalid_payload_and_matching_retry_leave_no_open_transaction(db_session):
    """WP4-IIR-B4 / RTO-10 / RTO-12: an invalid payload and a matching-retry
    no-op must both deterministically finish the transaction and release
    the portfolio lock — reproducing the independent review's own probe
    (``Session.in_transaction() == False`` after each exit)."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    predecessor_id, successor_id = predecessor.id, successor.id
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    assert db.in_transaction() is False

    with pytest.raises(PositionConversionError):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload={"not": "valid"})
    assert db.in_transaction() is False

    payload = _payload(predecessor_asset_id=predecessor_id, successor_asset_id=successor_id)
    execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)
    assert db.in_transaction() is False

    second = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)
    assert second["status"] == "already_applied"
    assert db.in_transaction() is False


def test_b1_b4_caller_owned_pending_work_is_neither_committed_nor_rolled_back(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(
        db, portfolio_id=1, symbol="BANPU.BK", shares=6700,
        avg_cost=48709.00 / 6700, asset_id=predecessor.id,
    )
    unrelated = Workspace(id=99, name="caller-owned pending work")
    db.add(unrelated)
    assert inspect(unrelated).pending

    with pytest.raises(PositionConversionError, match="idle Session"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(
                predecessor_asset_id=predecessor.id,
                successor_asset_id=successor.id,
            ),
        )

    assert db.in_transaction() is True
    assert inspect(unrelated).pending
    assert unrelated in db.new
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == 0
    db.commit()
    assert db.query(Workspace).filter_by(id=99).one().name == "caller-owned pending work"


def test_rto1_success_uses_one_service_owned_transaction_and_one_commit(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(
        db, portfolio_id=1, symbol="BANPU.BK", shares=6700,
        avg_cost=48709.00 / 6700, asset_id=predecessor.id,
    )
    engine = db.get_bind()
    events = []

    def _on_begin(_connection):
        events.append("begin")

    def _on_commit(_connection):
        events.append("commit")

    event.listen(engine, "begin", _on_begin)
    event.listen(engine, "commit", _on_commit)
    try:
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(
                predecessor_asset_id=predecessor.id,
                successor_asset_id=successor.id,
            ),
        )
    finally:
        event.remove(engine, "begin", _on_begin)
        event.remove(engine, "commit", _on_commit)

    assert events == ["begin", "commit"]
    assert db.in_transaction() is False


def test_rto1_common_boundary_precedes_retry_disposition(db_session):
    """RTO-1: E3 registry validation (a common-boundary element) must
    execute — and can fail — even when a row already exists at the exact
    canonical conversion identity a matching retry would use. E8-R
    disposition never runs ahead of the common boundary."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db, prepare=False)
    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)

    # A Transaction row shaped like a prior matching conversion, inserted
    # directly (never through execute_position_conversion, since registry
    # preparation never ran).
    db.add(Transaction(
        workspace_id=1, portfolio_id=1, symbol="BANPU.BK",
        transaction_type="POSITION_CONVERSION", shares=2562.214,
        price_per_share=48709.00 / 2562.214, total_amount=48709.00,
        fees=0.0, taxes=0.0, transaction_date=datetime(2026, 3, 2),
        asset_id=predecessor.id, conversion_payload=payload,
    ))
    db.commit()

    with pytest.raises(AssetRegistryError):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)


def test_rto3_rto10_rto13_matching_retry_ignores_successor_state_and_cleans_up(db_session):
    """RTO-3 / RTO-10 / RTO-13: a matching retry classifies correctly,
    performs no mutation, does not consult current successor materialized
    state, and leaves no open transaction."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)

    first = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)
    # (see the B4 test above for why a successful application's own
    # autobegin state is not asserted here — RTO-10 governs the matching
    # no-op below, not this first application.)

    # Simulate legitimate later successor activity (e.g. a subsequent BUY)
    # that changes current successor materialized state.
    successor_item = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPUU.BK").one()
    successor_item.shares = 99999.0
    successor_item.avg_cost = 1.23
    db.commit()

    second = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert second["status"] == "already_applied"
    assert second["transaction_id"] == first["transaction_id"]
    assert db.in_transaction() is False
    reloaded = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPUU.BK").one()
    assert reloaded.shares == 99999.0
    assert reloaded.avg_cost == 1.23


def test_rto4_rto8_rto11_conflicting_retry_cleans_up_and_performs_no_mutation(db_session):
    """RTO-4 / RTO-8 / RTO-11: a conflicting retry (unequal regenerated
    fingerprint at the same canonical identity) hard-fails without mutating
    state and without leaving an open transaction."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    first_payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=first_payload)
    # (see the B4 test above for why a successful application's own
    # autobegin state is not asserted here — RTO-11 governs the conflict
    # exit below, not this first application.)

    conflicting_payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    conflicting_payload["boundary_evidence"]["predecessor_reference_price"] = "5.61"

    tx_count_before = db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count()
    cash_before = db.query(Portfolio).filter_by(id=1).one().cash_balance
    db.rollback()

    with pytest.raises(PositionConversionError):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=conflicting_payload)

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == tx_count_before
    assert db.query(Portfolio).filter_by(id=1).one().cash_balance == pytest.approx(cash_before, abs=1e-9)


@pytest.mark.parametrize(
    ("delta", "expect_valid"),
    [
        (Decimal("0"), True),
        (Decimal("0.0000009"), True),    # just inside tolerance
        (Decimal("0.000001"), True),     # exactly at tolerance -- inclusive boundary
        (Decimal("0.0000011"), False),   # just outside tolerance
        (Decimal("-0.0000009"), True),
        (Decimal("-0.000001"), True),
        (Decimal("-0.0000011"), False),
    ],
)
def test_b1_numeric_projection_tolerance_boundary(db_session, delta, expect_valid):
    """WP4-IIR-B1 second-renewed correction: a stored legacy ``shares``
    value within the frozen Design's authorized 0.000001 absolute storage
    tolerance of the payload's exact ``shares_received`` projection is a
    valid existing row -- a matching incoming fingerprint resolves to
    ``already_applied``. Outside that tolerance the row is invalid existing
    state and fails closed, never silently matching or conflicting.
    Reproduces the second-renewed review's own boundary example
    (``2562.2140005`` against a ``2562.214`` projection)."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    exact_shares = Decimal("2562.214")
    stored_shares = float(exact_shares + delta)
    _insert_existing_conversion_row(db, payload, shares=stored_shares)

    if expect_valid:
        result = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)
        assert result["status"] == "already_applied"
    else:
        with pytest.raises(PositionConversionError, match="inconsistent with canonical identity/payload"):
            execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == 1
    assert db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPU.BK").one().shares == 6700
    assert db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPUU.BK").one_or_none() is None


def test_rto5_rto9_rto12_invalid_stored_payload_fails_closed_and_cleans_up(db_session):
    """RTO-5 / RTO-9 / RTO-12: a malformed stored conversion_payload on an
    existing row at the same canonical identity establishes neither
    matching nor conflicting retry authority; it fails closed with no
    business mutation and no retained transaction/lock. The multiple-row
    ("zero-or-multiple") sub-case of RTO-9 is structurally prevented by the
    WP1 partial unique index on (portfolio_id, predecessor asset_id,
    conversion type, transaction_date) and so cannot be independently
    constructed here without violating that constraint."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)

    db.add(Transaction(
        workspace_id=1, portfolio_id=1, symbol="BANPU.BK",
        transaction_type="POSITION_CONVERSION", shares=2562.214,
        price_per_share=48709.00 / 2562.214, total_amount=48709.00,
        fees=0.0, taxes=0.0, transaction_date=datetime(2026, 3, 2),
        asset_id=predecessor.id, conversion_payload={"schema_version": 1},
    ))
    db.commit()

    with pytest.raises(PositionConversionError, match="invalid stored conversion_payload"):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(portfolio_id=1, transaction_type="POSITION_CONVERSION").count() == 1
    assert db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPU.BK").one().shares == 6700


@pytest.mark.parametrize(
    ("field", "corrupt_value"),
    [
        ("workspace_id", 2),
        ("symbol", "CORRUPTED"),
        ("shares", 1.0),
        ("price_per_share", 1.0),
        ("total_amount", 1.0),
        ("fees", 1.0),
        ("taxes", 1.0),
    ],
)
@pytest.mark.parametrize("incoming_conflict", [False, True])
def test_rto7_rto8_rto9_rto12_parseable_inconsistent_row_fails_before_classification(
    db_session, field, corrupt_value, incoming_conflict,
):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=50.0)
    db.add(Workspace(id=2, name="wrong row workspace"))
    db.commit()
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(
        db, portfolio_id=1, symbol="BANPU.BK", shares=6700,
        avg_cost=48709.00 / 6700, asset_id=predecessor.id,
    )
    stored_payload = _payload(
        predecessor_asset_id=predecessor.id,
        successor_asset_id=successor.id,
    )
    kwargs = {field: corrupt_value}
    _insert_existing_conversion_row(db, stored_payload, **kwargs)

    incoming = _payload(
        predecessor_asset_id=predecessor.id,
        successor_asset_id=successor.id,
    )
    if incoming_conflict:
        incoming["boundary_evidence"]["predecessor_reference_price"] = "5.61"

    with pytest.raises(PositionConversionError, match="inconsistent with canonical identity/payload"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1, conversion_payload=incoming,
        )

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == 1
    predecessor_item = db.query(PortfolioItem).filter_by(
        portfolio_id=1, symbol="BANPU.BK",
    ).one()
    assert predecessor_item.shares == 6700
    assert db.query(PortfolioItem).filter_by(
        portfolio_id=1, symbol="BANPUU.BK",
    ).one_or_none() is None
    assert db.query(Portfolio).filter_by(id=1).one().cash_balance == pytest.approx(50.0)


@pytest.mark.parametrize(
    ("payload_path", "corrupt_value"),
    [
        (("predecessor", "symbol"), "NONCANONICAL-PREDECESSOR"),
        (("successor", "symbol"), "NONCANONICAL-SUCCESSOR"),
        # WP4-IIR-B2 second-renewed correction: an existing row whose
        # stored payload carries an arbitrary predecessor provider symbol
        # not derivable from current registry state is invalid existing
        # state -- it must not establish matching or conflicting retry
        # authority (RTO-5, RTO-7, RTO-9, RTO-12 extension).
        (("quote_binding", "predecessor_provider_symbol"), "CALLER-PROVIDER-PRE-CORRUPT"),
    ],
)
def test_rto9_rto12_parseable_noncanonical_payload_projection_fails_closed(
    db_session, payload_path, corrupt_value,
):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(
        db, portfolio_id=1, symbol="BANPU.BK", shares=6700,
        avg_cost=48709.00 / 6700, asset_id=predecessor.id,
    )
    stored_payload = _payload(
        predecessor_asset_id=predecessor.id,
        successor_asset_id=successor.id,
    )
    stored_payload[payload_path[0]][payload_path[1]] = corrupt_value
    assert parse_position_conversion_payload(stored_payload).is_valid
    _insert_existing_conversion_row(db, stored_payload)

    with pytest.raises(PositionConversionError, match="inconsistent with canonical identity/payload"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(
                predecessor_asset_id=predecessor.id,
                successor_asset_id=successor.id,
            ),
        )

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == 1
    assert db.query(PortfolioItem).filter_by(
        portfolio_id=1, symbol="BANPU.BK",
    ).one().shares == 6700


# ══════════════════════════════════════════════════════════════════════════
# Provider-Identity Governance Decision evidence (PIA-1..PIA-4)
#
# BANPU_WP4_PROVIDER_IDENTITY_GOVERNANCE_DECISION.md, OUTCOME 1: registry
# resolution governs exactly the five PIA-1 members; quote_binding.provider
# is authored payload content under the frozen WP1 contract (PIA-3), never
# registry-resolved (PIA-2), and a valid-but-changed provider value at the
# same canonical identity is a conformant controlled conflict (PIA-4).
# ══════════════════════════════════════════════════════════════════════════

def test_wp4_pia1_all_five_registry_authoritative_fields_persist_correctly(db_session):
    """PIA-1: exactly five payload members are registry-resolved --
    predecessor.symbol, successor.symbol, successor.provider_symbol,
    quote_binding.successor_provider_symbol, and
    quote_binding.predecessor_provider_symbol. Arbitrary caller text for
    the three silently-corrected members (predecessor.symbol,
    successor.symbol, quote_binding.predecessor_provider_symbol) does not
    survive; the persisted payload carries the registry-authoritative
    value for all five."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    payload["predecessor"]["symbol"] = "CALLER-PREDECESSOR"
    payload["successor"]["symbol"] = "CALLER-SUCCESSOR"
    payload["quote_binding"]["predecessor_provider_symbol"] = "CALLER-PROVIDER-PRE"

    result = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)
    assert result["status"] == "applied"

    persisted = db.query(Transaction).filter_by(id=result["transaction_id"]).one().conversion_payload
    assert persisted["predecessor"]["symbol"] == "BANPU.BK"
    assert persisted["successor"]["symbol"] == "BANPUU.BK"
    assert persisted["successor"]["provider_symbol"] == "BANPUU.BK"
    assert persisted["quote_binding"]["successor_provider_symbol"] == "BANPUU.BK"
    assert persisted["quote_binding"]["predecessor_provider_symbol"] == "BANPU.BK"


def test_wp4_pia1_successor_provider_symbol_mismatch_fails_closed(db_session):
    """PIA-1: unlike predecessor_provider_symbol, successor.provider_symbol
    / quote_binding.successor_provider_symbol are not silently corrected --
    E0 registry preparation already establishes the current successor
    PROVIDER_SYMBOL identifier, so E3 requires the caller's value to
    already equal it. A wrong (but internally self-consistent, satisfying
    the frozen canonicalizer's own successor.provider_symbol ==
    quote_binding.successor_provider_symbol invariant) pair fails closed
    with no mutation, proving this PIA-1 member is registry-authoritative
    too."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    payload = _payload(
        predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        successor_provider_symbol="CALLER-PROVIDER-SUCC-WRONG",
    )

    with pytest.raises(AssetRegistryError):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert db.query(Transaction).filter_by(portfolio_id=1).count() == 0
    assert db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="BANPU.BK").one().shares == 6700


def test_rto5_rto9_rto12_existing_row_successor_provider_symbol_mismatch_fails_closed(db_session):
    """RTO-5 / RTO-9 / RTO-12 extension under PIA-1: an existing row whose
    stored successor provider-symbol pair (self-consistent, so still
    parseable) no longer matches the registry's current successor
    PROVIDER_SYMBOL identifier is invalid existing state -- it must not
    establish matching or conflicting retry authority."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(
        db, portfolio_id=1, symbol="BANPU.BK", shares=6700,
        avg_cost=48709.00 / 6700, asset_id=predecessor.id,
    )
    stored_payload = _payload(
        predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        successor_provider_symbol="STALE-PROVIDER-SUCC",
    )
    assert parse_position_conversion_payload(stored_payload).is_valid
    _insert_existing_conversion_row(db, stored_payload)

    with pytest.raises(PositionConversionError, match="inconsistent with canonical identity/payload"):
        execute_position_conversion(
            db, ws_id=1, portfolio_id=1,
            conversion_payload=_payload(
                predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
            ),
        )

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == 1
    assert db.query(PortfolioItem).filter_by(
        portfolio_id=1, symbol="BANPU.BK",
    ).one().shares == 6700


def test_wp4_pia4_valid_provider_change_yields_controlled_conflict_not_defect(db_session):
    """PIA-3/PIA-4: quote_binding.provider is authored payload content
    governed only by the frozen WP1 contract (present, string, non-empty),
    not a registry identifier. It fully participates in the sole canonical
    fingerprint, so a second request at the same canonical identity (same
    portfolio, same predecessor asset, same transition date) differing
    only in a valid, non-empty provider value regenerates a different
    fingerprint and is correctly classified as a controlled conflict --
    conformant fail-closed behavior, not a defect (retry-order Governance
    Decision Sec 7.3, restated as PIA-4)."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    first_payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    first_payload["quote_binding"]["provider"] = "YAHOO"
    result = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=first_payload)
    assert result["status"] == "applied"

    second_payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    second_payload["quote_binding"]["provider"] = "SET-SMART"

    tx_count_before = db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count()
    cash_before = db.query(Portfolio).filter_by(id=1).one().cash_balance
    db.rollback()

    with pytest.raises(PositionConversionError, match="conflicting POSITION_CONVERSION"):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=second_payload)

    assert db.in_transaction() is False
    assert db.query(Transaction).filter_by(
        portfolio_id=1, transaction_type="POSITION_CONVERSION",
    ).count() == tx_count_before
    assert db.query(Portfolio).filter_by(id=1).one().cash_balance == pytest.approx(cash_before, abs=1e-9)


def test_wp4_pia2_provider_value_accepted_regardless_of_runtime_price_provider(db_session, monkeypatch):
    """PIA-2: quote_binding.provider is never compared against runtime
    PRICE_PROVIDER / market-data evidence identity inside WP4's write
    path. A payload whose provider value ("SET-SMART") differs from both
    the default runtime evidence identity ("yahoo_chart") and the Design's
    illustrative "YAHOO" succeeds unconditionally, and setting
    PRICE_PROVIDER has no effect on WP4's own disposition -- proving WP4
    does not read runtime provider configuration while canonicalizing."""
    db = db_session
    monkeypatch.setenv("PRICE_PROVIDER", "some_other_provider_entirely")
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)

    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    payload["quote_binding"]["provider"] = "SET-SMART"

    result = execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)

    assert result["status"] == "applied"
    tx = db.query(Transaction).filter_by(id=result["transaction_id"]).one()
    assert tx.conversion_payload["quote_binding"]["provider"] == "SET-SMART"


def test_rto6_payload_cannot_supply_its_own_fingerprint_field(db_session):
    """RTO-6: the version-1 payload contract has no caller-authorable
    fingerprint field — parse_position_conversion_payload rejects an
    unknown top-level ``fingerprint`` key, so a caller-supplied digest can
    never reach E8-R disposition; the fingerprint used there is always
    regenerated by the sole canonical algorithm."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    predecessor, successor = _mint_and_prepare_registry(db)
    _add_holding(db, portfolio_id=1, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700,
                 asset_id=predecessor.id)
    payload = _payload(predecessor_asset_id=predecessor.id, successor_asset_id=successor.id)
    payload["fingerprint"] = "0" * 64

    with pytest.raises(PositionConversionError):
        execute_position_conversion(db, ws_id=1, portfolio_id=1, conversion_payload=payload)
