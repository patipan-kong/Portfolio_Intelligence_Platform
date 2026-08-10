"""BANPU-WP2 Step 2 — cross-engine POSITION_CONVERSION replay fixtures.

Real in-memory SQLite database (not mocks) — required to exercise the actual
Transaction.conversion_payload JSON column, the WP1 identity/date CHECK
constraint (ck_tx_position_conversion_identity_date), and PortfolioItem
delete-and-reinsert materialization end-to-end through the public
rebuild_portfolio() / validate_portfolio_ledger() APIs. Mirrors the
db_session pattern already used by test_repair_validate_consistency.py.

Per BANPU-WP2 planning corpus (Work Package Plan §1, Implementation
Specification §5.4): before WP5 acceptance every committed rebuild in this
file uses skip_snapshots=True on a per-test, rollback-isolated in-memory
database — never a persistent development/production row — and no test here
asserts a committed full-history snapshot rebuild.

WP2 production behavior (portfolio_rebuilder.py / ledger_validator.py
POSITION_CONVERSION handling) does not exist yet — every fixture below is
expected to fail until that behavior is implemented (Steps 3-7).
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401 — registers the `assets` FK target table on Base.metadata
from models.database import Base, LedgerRepair, Portfolio, PortfolioItem, Transaction, Workspace
from services.ledger_validator import _replay_and_check, validate_portfolio_ledger
from services.portfolio_rebuilder import (
    ReconciliationStatus,
    _replay_with_date_snapshots,
    _resolve_conversion_successors,
    rebuild_portfolio,
)
from services.transaction_canonicalizer import canonicalize_transactions


# ══════════════════════════════════════════════════════════════════════════════
# DB fixtures
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


def _seed_workspace_and_portfolio(
    db,
    *,
    portfolio_id: int = 1,
    cash: float = 0.0,
    replay_asset_id_native: bool = False,
) -> Portfolio:
    db.add(Workspace(id=1, name="Default"))
    portfolio = Portfolio(
        id=portfolio_id, workspace_id=1, name="Test Portfolio",
        cash_balance=cash, created_at=datetime(2025, 1, 1),
        replay_asset_id_native=replay_asset_id_native,
    )
    db.add(portfolio)
    db.commit()
    return portfolio


def _add_tx(
    db,
    tx_id: int,
    portfolio_id: int,
    tx_type: str,
    *,
    symbol: str | None = None,
    shares: float | None = None,
    price: float | None = None,
    amount: float | None = None,
    fees: float | None = None,
    taxes: float | None = None,
    date_: datetime = datetime(2026, 1, 1),
    asset_id: int | None = None,
    conversion_payload: dict | None = None,
) -> None:
    if (
        tx_type == "POSITION_CONVERSION"
        and conversion_payload is not None
        and "successor" in conversion_payload
        and "basis" in conversion_payload
    ):
        successor = conversion_payload["successor"]
        basis = conversion_payload["basis"]
        cash_in_lieu = conversion_payload.get("cash_in_lieu")
        received = Decimal(successor["shares_received"])
        carried = Decimal(basis["carried_to_successor"])
        shares = float(received) if shares is None else shares
        price = float(carried / received) if price is None else price
        amount = float(carried) if amount is None else amount
        fees = float(Decimal(cash_in_lieu["fees"])) if fees is None and cash_in_lieu else (fees or 0.0)
        taxes = float(Decimal(cash_in_lieu["taxes"])) if taxes is None and cash_in_lieu else (taxes or 0.0)
    else:
        amount = 0.0 if amount is None else amount
        fees = 0.0 if fees is None else fees
        taxes = 0.0 if taxes is None else taxes
    db.add(Transaction(
        id=tx_id, workspace_id=1, portfolio_id=portfolio_id, symbol=symbol,
        transaction_type=tx_type, shares=shares, price_per_share=price,
        total_amount=amount, fees=fees, taxes=taxes, transaction_date=date_,
        created_at=date_, asset_id=asset_id, conversion_payload=conversion_payload,
    ))


def _payload(
    *,
    predecessor_asset_id: int,
    predecessor_symbol: str,
    shares_surrendered: str,
    successor_asset_id: int,
    successor_symbol: str,
    successor_provider_symbol: str,
    shares_entitled: str,
    shares_received: str,
    conversion_ratio: str,
    basis_before: str,
    basis_allocated: str,
    basis_carried: str,
    cash_in_lieu: dict | None = None,
    transition_date: str = "2026-03-02",
) -> dict:
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
            "legal_effective_date": transition_date,
            "valuation_transition_date": transition_date,
            "predecessor_last_price_date": transition_date,
            "successor_quote_epoch_start_date": transition_date,
        },
        "quote_binding": {
            "provider": "test-provider",
            "predecessor_provider_symbol": predecessor_symbol,
            "successor_provider_symbol": successor_provider_symbol,
        },
        "boundary_evidence": {
            "predecessor_reference_price": "1.00",
            "successor_reference_price": "1.00",
            "mechanical_nav_tolerance_pct": "1.0",
            "suspension_gap_annotation": "WP2 fixture — no suspension",
        },
        "evidence": {
            "reference": "WP2-FIXTURE",
            "source": "unit-test",
            "captured_at": "2026-03-02T00:00:00Z",
        },
    }


# ══════════════════════════════════════════════════════════════════════════════
# 1. BANPU full-share commit — successor materialized, predecessor gone, cash unchanged
# ══════════════════════════════════════════════════════════════════════════════

def test_rebuild_banpu_full_share_commits_successor_and_preserves_cash(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)

    payload = _payload(
        predecessor_asset_id=101, predecessor_symbol="PCONV1.BK", shares_surrendered="6700",
        successor_asset_id=102, successor_symbol="SCONV1.BK", successor_provider_symbol="SCONV1.BK",
        shares_entitled="2562.214", shares_received="2562.214", conversion_ratio="0.38242",
        basis_before="48709.00", basis_allocated="0", basis_carried="48709.00",
        cash_in_lieu=None,
    )
    _add_tx(db, 1, 1, "DEPOSIT", amount=100_000.0, date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="PCONV1.BK", shares=6700, price=48709.00 / 6700,
            amount=0.0, date_=datetime(2026, 1, 2))
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="PCONV1.BK", asset_id=101,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.success is True
    assert result.committed is True

    items = {i.symbol: i for i in db.query(PortfolioItem).filter_by(portfolio_id=1).all()}
    assert "PCONV1.BK" not in items
    assert "SCONV1.BK" in items
    successor = items["SCONV1.BK"]
    assert successor.shares == pytest.approx(2562.214, abs=1e-6)
    assert successor.avg_cost == pytest.approx(48709.00 / 2562.214, abs=1e-4)

    refreshed = db.query(Portfolio).filter_by(id=1).first()
    assert refreshed.cash_balance == pytest.approx(100_000.0)   # unchanged — no cash-in-lieu


# ══════════════════════════════════════════════════════════════════════════════
# 2. Native-mode replay reaches the same economic result as legacy-mode replay
# ══════════════════════════════════════════════════════════════════════════════

def test_rebuild_native_mode_matches_legacy_mode_economics(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0, replay_asset_id_native=True)

    payload = _payload(
        predecessor_asset_id=111, predecessor_symbol="NPCONV1.BK", shares_surrendered="6700",
        successor_asset_id=112, successor_symbol="NSCONV1.BK", successor_provider_symbol="NSCONV1.BK",
        shares_entitled="2562.214", shares_received="2562.214", conversion_ratio="0.38242",
        basis_before="48709.00", basis_allocated="0", basis_carried="48709.00",
        cash_in_lieu=None,
    )
    _add_tx(db, 1, 1, "DEPOSIT", amount=100_000.0, date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="NPCONV1.BK", shares=6700, price=48709.00 / 6700,
            amount=0.0, date_=datetime(2026, 1, 2), asset_id=111)
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="NPCONV1.BK", asset_id=111,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.committed is True
    items = {i.symbol: i for i in db.query(PortfolioItem).filter_by(portfolio_id=1).all()}
    assert "NSCONV1.BK" in items
    assert items["NSCONV1.BK"].shares == pytest.approx(2562.214, abs=1e-6)
    assert items["NSCONV1.BK"].avg_cost == pytest.approx(48709.00 / 2562.214, abs=1e-4)


# ══════════════════════════════════════════════════════════════════════════════
# 3. Historical null-asset predecessor fallback (native mode)
# ══════════════════════════════════════════════════════════════════════════════

def test_rebuild_null_asset_predecessor_fallback_resolves_native_mode(db_session):
    """Native mode, but the original position-creating transaction was never
    asset-ID backfilled (asset_id NULL) — replay_key() falls through to
    canonical_symbol for that holding. The conversion's own top-level
    asset_id is non-null (required by the WP1 CHECK constraint); resolution
    must still find the one canonical-symbol-keyed predecessor holding."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0, replay_asset_id_native=True)

    payload = _payload(
        predecessor_asset_id=121, predecessor_symbol="LPCONV.BK", shares_surrendered="6700",
        successor_asset_id=122, successor_symbol="LSCONV.BK", successor_provider_symbol="LSCONV.BK",
        shares_entitled="2562.214", shares_received="2562.214", conversion_ratio="0.38242",
        basis_before="48709.00", basis_allocated="0", basis_carried="48709.00",
        cash_in_lieu=None,
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="LPCONV.BK", shares=6700, price=48709.00 / 6700,
            amount=0.0, date_=datetime(2026, 1, 2), asset_id=None)   # historical, never backfilled
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="LPCONV.BK", asset_id=121,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.committed is True
    items = {i.symbol: i for i in db.query(PortfolioItem).filter_by(portfolio_id=1).all()}
    assert "LSCONV.BK" in items


# ══════════════════════════════════════════════════════════════════════════════
# 4-6. Fail-closed identity conditions
# ══════════════════════════════════════════════════════════════════════════════

def test_rebuild_zero_predecessor_candidates_fails_closed(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=50_000.0)
    payload = _payload(
        predecessor_asset_id=201, predecessor_symbol="ZPRED.BK", shares_surrendered="10",
        successor_asset_id=202, successor_symbol="ZSUCC.BK", successor_provider_symbol="ZSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "POSITION_CONVERSION", symbol="ZPRED.BK", asset_id=201,   # no predecessor holding at all
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.success is False
    assert result.aborted is False
    assert result.committed is False
    assert result.error

    items = db.query(PortfolioItem).filter_by(portfolio_id=1).all()
    assert items == []   # nothing was written


def test_rebuild_multiple_predecessor_candidates_fail_closed(db_session):
    """The rebuilder's _PortfolioState.holdings is keyed by replay_key(), which
    already canonicalizes every raw symbol (unlike the validator's raw-keyed
    _ReplayState) — so two raw-symbol variants of the same canonical symbol
    merge into ONE holding during ordinary replay, never producing rebuilder-
    side ambiguity by themselves. The only way the rebuilder can see more than
    one candidate for a single predecessor identity is native mode: one
    transaction resolved to an asset-ID-keyed holding, another (unrelated, or
    never backfilled) transaction resolved to a canonical-symbol-keyed holding
    that also happens to match the payload's predecessor symbol."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0, replay_asset_id_native=True)
    payload = _payload(
        predecessor_asset_id=211, predecessor_symbol="APRED.BK", shares_surrendered="10",
        successor_asset_id=212, successor_symbol="ASUCC.BK", successor_provider_symbol="ASUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    # Candidate 1 — matches by asset_id (211), different raw/canonical symbol.
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="OTHER.BK", shares=5, price=10, amount=0.0,
            date_=datetime(2026, 1, 1), asset_id=211)
    # Candidate 2 — matches by canonical symbol only (never asset-ID backfilled).
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="APRED.BK", shares=5, price=10, amount=0.0,
            date_=datetime(2026, 1, 2), asset_id=None)
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="APRED.BK", asset_id=211,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.success is False
    assert result.committed is False
    assert result.error


def test_rebuild_conflicting_successor_asset_id_fails_closed(db_session):
    """BANPU-WP2 Step 5: a stored successor item paired by symbol but
    carrying a DIFFERENT non-null asset_id is a controlled materialization
    conflict (_resolve_conversion_successors) — fails before Stage 4
    reconciliation or Stage 8 commit ever runs. Atomicity (§6): cash and the
    pre-existing item must both be byte-unchanged, not just the item."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=42_000.0)
    # Pre-existing successor item already carries a DIFFERENT non-null asset_id.
    db.add(PortfolioItem(workspace_id=1, portfolio_id=1, symbol="CSUCC.BK",
                          shares=1.0, avg_cost=1.0, asset_id=9999))
    db.commit()

    payload = _payload(
        predecessor_asset_id=221, predecessor_symbol="CPRED.BK", shares_surrendered="10",
        successor_asset_id=402, successor_symbol="CSUCC.BK", successor_provider_symbol="CSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="CPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="CPRED.BK", asset_id=221,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.success is False
    assert result.committed is False
    assert result.error

    unchanged = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="CSUCC.BK").first()
    assert unchanged is not None
    assert unchanged.asset_id == 9999   # untouched — commit never happened

    refreshed_portfolio = db.query(Portfolio).filter_by(id=1).first()
    assert refreshed_portfolio.cash_balance == 42_000.0   # untouched — atomicity


# ══════════════════════════════════════════════════════════════════════════════
# 7. Same-day conflict blocks commit (Stage 5) despite ERROR severity
# ══════════════════════════════════════════════════════════════════════════════

def test_rebuild_same_day_conflict_blocks_commit(db_session):
    """Corrected from the original Step 2 draft: same-day affected-asset
    conflict is a REBUILDER preflight check (Implementation Specification
    §7.1 item 6), not a Stage-5-active validator finding — Step 3 explicitly
    excludes implementing Stage 5 blocking. A preflight failure returns
    success=False/aborted=False/committed=False per §10's first bucket, not
    the second (success=True/aborted=True) bucket, which describes a
    Stage-5-active finding surfaced by the validator (out of Step 3 scope,
    and never reached here since preflight raises before Stage 5 runs)."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=100_000.0)
    payload = _payload(
        predecessor_asset_id=231, predecessor_symbol="DPRED.BK", shares_surrendered="10",
        successor_asset_id=232, successor_symbol="DSUCC.BK", successor_provider_symbol="DSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="DPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "BUY", symbol="DPRED.BK", shares=1, price=10, amount=10,
            date_=datetime(2026, 3, 2))   # same calendar date as the conversion, targets predecessor
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="DPRED.BK", asset_id=231,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.success is False
    assert result.aborted is False
    assert result.committed is False
    assert result.error


# ══════════════════════════════════════════════════════════════════════════════
# 8-9. Materialization — asset_id preservation and authoritative successor binding
# ══════════════════════════════════════════════════════════════════════════════

def test_rebuild_preserves_unrelated_portfolio_item_asset_id(db_session):
    """Spec §6.1: every reinserted pre-existing PortfolioItem.asset_id must
    survive the conversion-driven delete-and-reinsert unchanged."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="UNREL.BK", shares=10, price=5, amount=0.0,
            date_=datetime(2026, 1, 1))
    payload = _payload(
        predecessor_asset_id=241, predecessor_symbol="UPRED.BK", shares_surrendered="10",
        successor_asset_id=242, successor_symbol="USUCC.BK", successor_provider_symbol="USUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="UPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="UPRED.BK", asset_id=241,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    # First rebuild materializes UNREL.BK as a PortfolioItem row; simulate a
    # prior asset-ID backfill pass (services/ledger_asset_backfill.py, a
    # separate process the rebuild engine itself never runs) by stamping the
    # ID directly, then rebuild again from the same unchanged ledger.
    asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    unrelated = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="UNREL.BK").first()
    assert unrelated is not None
    unrelated.asset_id = 555
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True

    refreshed = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="UNREL.BK").first()
    assert refreshed is not None
    assert refreshed.asset_id == 555


def test_rebuild_successor_gets_authoritative_asset_id(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=251, predecessor_symbol="APRED2.BK", shares_surrendered="10",
        successor_asset_id=999, successor_symbol="ASUCC2.BK", successor_provider_symbol="ASUCC2.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="APRED2.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="APRED2.BK", asset_id=251,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True

    successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="ASUCC2.BK").first()
    assert successor is not None
    assert successor.asset_id == 999


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP2 Step 3 — preflight and identity resolution (new fixtures)
# ══════════════════════════════════════════════════════════════════════════════

def test_rebuild_malformed_payload_fails_before_replay(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="MPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="MPRED.BK", asset_id=271,
            date_=datetime(2026, 3, 2), conversion_payload={"schema_version": 2})   # malformed
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.success is False
    assert result.aborted is False
    assert result.committed is False
    assert result.error

    items = db.query(PortfolioItem).filter_by(portfolio_id=1).all()
    assert items == []   # preflight failure — no persistent mutation staged or committed


def test_rebuild_raw_row_identity_mismatch_fails_before_replay(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=281, predecessor_symbol="IPRED.BK", shares_surrendered="10",
        successor_asset_id=282, successor_symbol="ISUCC.BK", successor_provider_symbol="ISUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="IPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    # Raw tx.asset_id (999) disagrees with payload.predecessor.asset_id (281).
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="IPRED.BK", asset_id=999,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.success is False
    assert result.aborted is False
    assert result.committed is False
    assert result.error


def test_rebuild_repair_exclude_cannot_remove_conversion_from_rebuilder_input(db_session):
    """An EXCLUDE repair targeting the conversion transaction must not remove
    it from the rebuilder's effective input — the zero-candidate fixture
    proves this: if EXCLUDE had worked, the conversion would vanish from
    replay and the rebuild would succeed trivially (nothing left to fail on).
    Because the conversion is reinstated, preflight/identity still runs and
    still fails closed for the same reason as the no-repair case."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=50_000.0)
    payload = _payload(
        predecessor_asset_id=311, predecessor_symbol="RXPRED.BK", shares_surrendered="10",
        successor_asset_id=312, successor_symbol="RXSUCC.BK", successor_provider_symbol="RXSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "POSITION_CONVERSION", symbol="RXPRED.BK", asset_id=311,   # no predecessor holding
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    exclude = LedgerRepair(portfolio_id=1, transaction_id=1, repair_plan_id="p-exclude",
                            repair_type="EXCLUDE", reason="test", created_by="test", is_active=True)
    db.add(exclude)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False, apply_repairs=True,
    ))

    assert result.success is False   # still fails — the conversion was NOT actually excluded
    assert result.error


def test_rebuild_null_asset_predecessor_fallback_resolves_single_candidate_without_error(db_session):
    """Step-3-scoped companion to the existing (Step-4-scoped)
    test_rebuild_null_asset_predecessor_fallback_resolves_native_mode: proves
    identity resolution alone succeeds (no error) for the historical
    null-asset predecessor fallback, without requiring successor
    materialization (Step 4/5, not yet implemented)."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0, replay_asset_id_native=True)
    payload = _payload(
        predecessor_asset_id=321, predecessor_symbol="NAPRED.BK", shares_surrendered="10",
        successor_asset_id=322, successor_symbol="NASUCC.BK", successor_provider_symbol="NASUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="NAPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1), asset_id=None)   # historical, never backfilled
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="NAPRED.BK", asset_id=321,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True,
    ))

    assert not result.error
    assert result.success is True


def test_rebuild_conflicting_successor_candidates_during_replay_fail_closed(db_session):
    """Distinct from test_rebuild_conflicting_successor_asset_id_fails_closed
    (a Step 5 materialization-time concern comparing replay output against an
    old stored PortfolioItem row): this is Step 3's own replay-time successor
    CANDIDATE resolution (§7.3) — an asset-ID-matching ledger holding and a
    symbol-matching ledger holding that point at two different existing
    positions must fail closed, the same way predecessor ambiguity does."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0, replay_asset_id_native=True)
    payload = _payload(
        predecessor_asset_id=331, predecessor_symbol="CSPRED.BK", shares_surrendered="10",
        successor_asset_id=402, successor_symbol="CSSUCC.BK", successor_provider_symbol="CSSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="CSPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1), asset_id=331)
    # Successor candidate 1 — matches by asset_id (402), different raw/canonical symbol.
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="OTHERSUCC.BK", shares=3, price=10, amount=0.0,
            date_=datetime(2026, 1, 2), asset_id=402)
    # Successor candidate 2 — matches by canonical symbol only, never asset-ID backfilled.
    _add_tx(db, 3, 1, "INITIAL_POSITION", symbol="CSSUCC.BK", shares=4, price=10, amount=0.0,
            date_=datetime(2026, 1, 3), asset_id=None)
    _add_tx(db, 4, 1, "POSITION_CONVERSION", symbol="CSPRED.BK", asset_id=331,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.success is False
    assert result.committed is False
    assert result.error


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP2 Step 5 — materialization identity preservation and
# conversion-scoped five-field reconciliation
# ══════════════════════════════════════════════════════════════════════════════

def test_rebuild_successor_matching_asset_id_merges_without_conflict(db_session):
    """A stored successor already carrying the SAME non-null asset_id as the
    payload is not a conflict. Note this stored row has no corresponding
    ledger transaction, so replay's OWN economic merge (Step 4, ledger-driven
    only — see _resolve_conversion_successor_key) never sees it and the
    reconstructed successor is a fresh Qr-share holding; the stored row only
    supplies asset-ID identity for the Step 5 conflict/preservation check,
    never economics — the delete-and-reinsert always writes the reconstructed
    (ledger-driven) shares/avg_cost, not a blend with stale DB values."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    db.add(PortfolioItem(workspace_id=1, portfolio_id=1, symbol="MASUCC.BK",
                          shares=5.0, avg_cost=20.0, asset_id=999))
    db.commit()

    payload = _payload(
        predecessor_asset_id=501, predecessor_symbol="MAPRED.BK", shares_surrendered="10",
        successor_asset_id=999, successor_symbol="MASUCC.BK", successor_provider_symbol="MASUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="MAPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="MAPRED.BK", asset_id=501,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True

    successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="MASUCC.BK").first()
    assert successor is not None
    assert successor.asset_id == 999   # preserved — matched, no conflict
    assert successor.shares == pytest.approx(10.0)     # Qr only — ledger has no prior MASUCC.BK holding
    assert successor.avg_cost == pytest.approx(10.0)   # Bs(100) / Qr(10)


def test_rebuild_successor_null_asset_id_symbol_fallback_valid_precommit(db_session):
    """A stored successor matched only by symbol, with asset_id NULL, is
    valid pre-commit merge input (not a conflict) — the committed row is
    then authoritatively bound to the payload successor asset ID."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    db.add(PortfolioItem(workspace_id=1, portfolio_id=1, symbol="NASUCC.BK",
                          shares=2.0, avg_cost=10.0, asset_id=None))
    db.commit()

    payload = _payload(
        predecessor_asset_id=511, predecessor_symbol="NAPRED2.BK", shares_surrendered="10",
        successor_asset_id=888, successor_symbol="NASUCC.BK", successor_provider_symbol="NASUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="NAPRED2.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="NAPRED2.BK", asset_id=511,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True

    successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="NASUCC.BK").first()
    assert successor is not None
    assert successor.asset_id == 888   # bound authoritatively, was NULL pre-commit


def test_rebuild_successor_stored_identity_ambiguous_candidates_fail_closed(db_session):
    """Materialization-time counterpart to
    test_rebuild_conflicting_successor_candidates_during_replay_fail_closed:
    here the ambiguity is between two STORED PortfolioItem rows (not two
    ledger holdings) — one matched by asset_id, a different one matched by
    symbol. _resolve_conversion_successors must fail closed, never guess."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=77_000.0)
    db.add(PortfolioItem(workspace_id=1, portfolio_id=1, symbol="OLDNAME.BK",
                          shares=1.0, avg_cost=1.0, asset_id=402))            # matches by asset_id
    db.add(PortfolioItem(workspace_id=1, portfolio_id=1, symbol="AMSUCC.BK",
                          shares=1.0, avg_cost=1.0, asset_id=None))           # matches by symbol
    db.commit()

    payload = _payload(
        predecessor_asset_id=521, predecessor_symbol="AMPRED.BK", shares_surrendered="10",
        successor_asset_id=402, successor_symbol="AMSUCC.BK", successor_provider_symbol="AMSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="AMPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="AMPRED.BK", asset_id=521,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))

    assert result.success is False
    assert result.committed is False
    assert result.error

    refreshed_portfolio = db.query(Portfolio).filter_by(id=1).first()
    assert refreshed_portfolio.cash_balance == 77_000.0   # untouched


def test_rebuild_unrelated_item_null_asset_id_stays_null(db_session):
    """A legitimate pre-existing NULL asset_id on an unaffected item must
    remain NULL after a conversion-bearing rebuild — not coerced to any
    other value by the preservation map."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    db.add(PortfolioItem(workspace_id=1, portfolio_id=1, symbol="STAYSNULL.BK",
                          shares=3.0, avg_cost=7.0, asset_id=None))
    db.commit()
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="STAYSNULL.BK", shares=3, price=7, amount=0.0,
            date_=datetime(2026, 1, 1))

    payload = _payload(
        predecessor_asset_id=531, predecessor_symbol="NNPRED.BK", shares_surrendered="10",
        successor_asset_id=532, successor_symbol="NNSUCC.BK", successor_provider_symbol="NNSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="NNPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="NNPRED.BK", asset_id=531,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True

    unrelated = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="STAYSNULL.BK").first()
    assert unrelated is not None
    assert unrelated.asset_id is None


def test_rebuild_legacy_and_native_persist_same_successor_identity(db_session):
    """Legacy and native replay must persist the same reported successor
    identity (symbol + authoritative asset_id) even though they use
    different internal replay keys (Implementation Specification §8)."""
    db = db_session
    db.add(Workspace(id=1, name="Default"))
    legacy_portfolio = Portfolio(id=1, workspace_id=1, name="Legacy", cash_balance=0.0,
                                  created_at=datetime(2025, 1, 1), replay_asset_id_native=False)
    native_portfolio = Portfolio(id=2, workspace_id=1, name="Native", cash_balance=0.0,
                                  created_at=datetime(2025, 1, 1), replay_asset_id_native=True)
    db.add(legacy_portfolio)
    db.add(native_portfolio)
    db.commit()

    payload = _payload(
        predecessor_asset_id=541, predecessor_symbol="PARPRED.BK", shares_surrendered="10",
        successor_asset_id=542, successor_symbol="PARSUCC.BK", successor_provider_symbol="PARSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    for portfolio_id, native in [(1, False), (2, True)]:
        _add_tx(db, portfolio_id * 10 + 1, portfolio_id, "INITIAL_POSITION", symbol="PARPRED.BK",
                shares=10, price=10, amount=0.0, date_=datetime(2026, 1, 1),
                asset_id=541 if native else None)
        _add_tx(db, portfolio_id * 10 + 2, portfolio_id, "POSITION_CONVERSION", symbol="PARPRED.BK",
                asset_id=541, date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    legacy_result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    native_result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=2, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert legacy_result.committed is True
    assert native_result.committed is True

    legacy_succ = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="PARSUCC.BK").first()
    native_succ = db.query(PortfolioItem).filter_by(portfolio_id=2, symbol="PARSUCC.BK").first()
    assert legacy_succ is not None and native_succ is not None
    assert legacy_succ.symbol == native_succ.symbol == "PARSUCC.BK"
    assert legacy_succ.asset_id == native_succ.asset_id == 542
    assert legacy_succ.shares == native_succ.shares == pytest.approx(10.0)
    assert legacy_succ.avg_cost == native_succ.avg_cost == pytest.approx(10.0)


def test_rebuild_precommit_five_field_reconciliation_shows_independent_fields(db_session):
    """Before commit, a stored successor (matched by symbol, NULL asset_id,
    different shares/avg_cost) must produce five independent reconciliation
    rows — asset_id DIFFERENT (NULL vs authoritative), symbol MATCH (same
    string), shares/avg_cost/basis DIFFERENT (stale stored values)."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    db.add(PortfolioItem(workspace_id=1, portfolio_id=1, symbol="PCSUCC.BK",
                          shares=2.0, avg_cost=5.0, asset_id=None))
    db.commit()

    payload = _payload(
        predecessor_asset_id=551, predecessor_symbol="PCPRED.BK", shares_surrendered="10",
        successor_asset_id=552, successor_symbol="PCSUCC.BK", successor_provider_symbol="PCSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="PCPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="PCPRED.BK", asset_id=551,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True,
    ))
    assert not result.error

    rows = {
        r.field: r for r in result.reconciliation_report
        if r.entity_type == "portfolio_item" and r.identifier == "PCSUCC.BK"
    }
    assert set(rows) == {"asset_id", "symbol", "shares", "avg_cost", "basis"}
    assert rows["asset_id"].status.value       == "DIFFERENT"   # NULL vs 552
    assert rows["asset_id"].current_value      is None
    assert rows["asset_id"].reconstructed_value == 552
    assert rows["symbol"].status.value         == "MATCH"       # same string both sides
    assert rows["shares"].status.value         == "DIFFERENT"   # stored 2 vs reconstructed Qr=10
    assert rows["avg_cost"].status.value       == "DIFFERENT"
    assert rows["basis"].status.value          == "DIFFERENT"


def test_rebuild_postcommit_five_field_reconciliation_all_match(db_session):
    """After a successful commit, re-running reconciliation against the same
    unchanged ledger must show all five successor fields MATCH."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=561, predecessor_symbol="POCPRED.BK", shares_surrendered="10",
        successor_asset_id=562, successor_symbol="POCSUCC.BK", successor_provider_symbol="POCSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="POCPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="POCPRED.BK", asset_id=561,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    first = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert first.committed is True

    second = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True,
    ))
    assert not second.error

    rows = {
        r.field: r for r in second.reconciliation_report
        if r.entity_type == "portfolio_item" and r.identifier == "POCSUCC.BK"
    }
    assert set(rows) == {"asset_id", "symbol", "shares", "avg_cost", "basis"}
    for field_name, row in rows.items():
        assert row.status.value == "MATCH", f"{field_name}: {row.current_value} vs {row.reconstructed_value}"


def test_rebuild_ordinary_reconciliation_unchanged_no_conversion(db_session):
    """A no-conversion rebuild must keep the existing two-field (shares,
    avg_cost) reconciliation behavior — no asset_id/symbol/basis rows for
    ordinary items."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="ORD.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True,
    ))
    assert not result.error

    item_rows = [r for r in result.reconciliation_report if r.entity_type == "portfolio_item"]
    fields = {r.field for r in item_rows}
    assert fields <= {"shares", "avg_cost", "*"}
    assert "asset_id" not in fields
    assert "basis" not in fields


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP2 Step 7 — cross-engine and repair parity
#
# Every fixture below runs the SAME ledger through both engines' own public
# entry points independently: rebuild_portfolio() (portfolio_rebuilder.py)
# and _validator_state()/validate_portfolio_ledger() (ledger_validator.py).
# Neither call site imports from or invokes the other's private helpers, and
# expected values are computed from the payload/fixture data alone — never
# derived from one engine's output and asserted against the other's.
# ══════════════════════════════════════════════════════════════════════════════

def _validator_state(db, portfolio_id: int):
    """Independently exercise the validator's own replay entry point against
    the same DB rows the rebuilder reads. Mirrors the load/canonicalize
    steps of validate_portfolio_ledger() (services/ledger_validator.py) but
    calls _replay_and_check() directly to obtain the final _ReplayState for
    economic comparison — validate_portfolio_ledger() itself returns only a
    LedgerValidationReport (findings), not replay state. Never imports from
    or calls into portfolio_rebuilder.py.
    """
    portfolio = db.query(Portfolio).filter_by(id=portfolio_id).first()
    raw_txs = (
        db.query(Transaction)
        .filter_by(portfolio_id=portfolio_id)
        .order_by(Transaction.transaction_date, Transaction.id)
        .all()
    )
    ctxs = list(canonicalize_transactions(
        raw_txs, prefer_asset_id=bool(portfolio.replay_asset_id_native),
    ))
    raw_asset_id_by_id = {tx.id: tx.asset_id for tx in raw_txs}
    state, findings, _ = _replay_and_check(portfolio_id, ctxs, raw_asset_id_by_id=raw_asset_id_by_id)
    return state, findings


# ── Objective 2 — cross-engine economic parity (9 required fixtures) ──────────

def test_step7_cross_engine_parity_banpu_full_share_no_cil(db_session):
    """Fixture 1/9: BANPU full-share conversion, no cash-in-lieu. Expected
    values are computed from the payload alone."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=101, predecessor_symbol="S7PCONV1.BK", shares_surrendered="6700",
        successor_asset_id=102, successor_symbol="S7SCONV1.BK", successor_provider_symbol="S7SCONV1.BK",
        shares_entitled="2562.214", shares_received="2562.214", conversion_ratio="0.38242",
        basis_before="48709.00", basis_allocated="0", basis_carried="48709.00",
        cash_in_lieu=None,
    )
    _add_tx(db, 1, 1, "DEPOSIT", amount=100_000.0, date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="S7PCONV1.BK", shares=6700, price=48709.00 / 6700,
            amount=0.0, date_=datetime(2026, 1, 2))
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="S7PCONV1.BK", asset_id=101,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    expected_shares = Decimal("2562.214")
    expected_basis  = Decimal("48709.00")
    expected_cash   = 100_000.0

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True
    successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="S7SCONV1.BK").first()
    assert successor is not None and successor.asset_id == 102
    assert successor.shares == pytest.approx(float(expected_shares), abs=1e-6)
    assert successor.shares * successor.avg_cost == pytest.approx(float(expected_basis), abs=0.01)
    refreshed = db.query(Portfolio).filter_by(id=1).first()
    assert refreshed.cash_balance == pytest.approx(expected_cash)

    state, findings = _validator_state(db, 1)
    assert findings == []
    assert state.holdings["S7SCONV1.BK"] == expected_shares
    assert state.basis["S7SCONV1.BK"] == expected_basis
    assert state.identity["S7SCONV1.BK"] == ("S7SCONV1.BK", 102)
    assert state.cash == Decimal(str(expected_cash))


def test_step7_cross_engine_parity_generic_full_share_no_cil(db_session):
    """Fixture 2/9: incident-independent generic full-share conversion,
    legacy-symbol replay (Portfolio.replay_asset_id_native defaults False)."""
    db = db_session
    # Note: Portfolio.cash_balance is a materialized cache, not the source of
    # truth — a full rebuild replays only the Transaction ledger, so seeding
    # cash here without a matching DEPOSIT/INITIAL_CASH row would be
    # overwritten to 0.0 on commit. Expected cash is therefore 0.0 (no
    # cash-affecting transaction exists in this fixture at all).
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=2101, predecessor_symbol="S7GEN1PRED.BK", shares_surrendered="100",
        successor_asset_id=2102, successor_symbol="S7GEN1SUCC.BK", successor_provider_symbol="S7GEN1SUCC.BK",
        shares_entitled="100", shares_received="100", conversion_ratio="1",
        basis_before="1000", basis_allocated="0", basis_carried="1000",
        cash_in_lieu=None,
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7GEN1PRED.BK", shares=100, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="S7GEN1PRED.BK", asset_id=2101,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True
    successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="S7GEN1SUCC.BK").first()
    assert successor is not None and successor.asset_id == 2102
    assert successor.shares == pytest.approx(100.0)
    assert successor.avg_cost == pytest.approx(10.0)
    refreshed = db.query(Portfolio).filter_by(id=1).first()
    assert refreshed.cash_balance == pytest.approx(0.0)

    state, findings = _validator_state(db, 1)
    assert findings == []
    assert state.holdings["S7GEN1SUCC.BK"] == Decimal("100")
    assert state.basis["S7GEN1SUCC.BK"] == Decimal("1000")
    assert state.identity["S7GEN1SUCC.BK"] == ("S7GEN1SUCC.BK", 2102)
    assert state.cash == Decimal("0")


def test_step7_cross_engine_parity_generic_cash_in_lieu(db_session):
    """Fixture 3/9: generic cash-in-lieu conversion."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=2301, predecessor_symbol="S7CILPRED.BK", shares_surrendered="8",
        successor_asset_id=2302, successor_symbol="S7CILSUCC.BK", successor_provider_symbol="S7CILSUCC.BK",
        shares_entitled="10", shares_received="9.5", conversion_ratio="1.25",
        basis_before="240", basis_allocated="12", basis_carried="228",
        cash_in_lieu={
            "fractional_entitlement_shares": "0.5", "gross_proceeds": "15",
            "fees": "1", "taxes": "0.5", "net_cash": "13.5",
            "basis_allocated": "12", "realized_pnl": "1.5",
        },
    )
    _add_tx(db, 1, 1, "DEPOSIT", amount=1_000.0, date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="S7CILPRED.BK", shares=8, price=30, amount=0.0,
            date_=datetime(2026, 1, 2))
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="S7CILPRED.BK", asset_id=2301,
            date_=datetime(2026, 3, 2), amount=228.0, fees=1.0, taxes=0.5,
            conversion_payload=payload)
    db.commit()

    expected_cash = 1_000.0 + 13.5   # starting cash plus admitted net cash-in-lieu (Cn)

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True
    successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="S7CILSUCC.BK").first()
    assert successor is not None
    assert successor.shares == pytest.approx(9.5)
    assert successor.shares * successor.avg_cost == pytest.approx(228.0, abs=0.01)
    refreshed = db.query(Portfolio).filter_by(id=1).first()
    assert refreshed.cash_balance == pytest.approx(expected_cash)

    state, findings = _validator_state(db, 1)
    assert findings == []
    assert state.holdings["S7CILSUCC.BK"] == Decimal("9.5")
    assert state.basis["S7CILSUCC.BK"] == Decimal("228")
    assert state.cash == Decimal(str(expected_cash))


def test_step7_cross_engine_parity_existing_successor_merge(db_session):
    """Fixture 4/9: existing-successor merge — both engines see the merge
    purely from the ledger (a prior INITIAL_POSITION on the successor
    symbol), not from any stored PortfolioItem row."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=2401, predecessor_symbol="S7MRGPRED.BK", shares_surrendered="10",
        successor_asset_id=2402, successor_symbol="S7MRGSUCC.BK", successor_provider_symbol="S7MRGSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7MRGSUCC.BK", shares=5, price=20, amount=0.0,
            date_=datetime(2026, 1, 1))   # pre-existing ledger successor holding, basis=100
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="S7MRGPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 2))
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="S7MRGPRED.BK", asset_id=2401,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    expected_shares = 15.0
    expected_basis  = 200.0   # 100 existing + 100 carried

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True
    successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="S7MRGSUCC.BK").first()
    assert successor.shares == pytest.approx(expected_shares)
    assert successor.shares * successor.avg_cost == pytest.approx(expected_basis, abs=0.01)

    state, findings = _validator_state(db, 1)
    assert findings == []
    assert state.holdings["S7MRGSUCC.BK"] == Decimal("15")
    assert state.basis["S7MRGSUCC.BK"] == Decimal("200")


def test_step7_replay_mode_parity_legacy_vs_native_same_economics(db_session):
    """Fixtures 5+6/9 (legacy-symbol replay, asset-native replay) plus
    objective 6: legacy and native modes use different internal replay keys
    but must report the same economic state, in BOTH engines."""
    db = db_session
    db.add(Workspace(id=1, name="Default"))
    legacy = Portfolio(id=1, workspace_id=1, name="Legacy", cash_balance=0.0,
                        created_at=datetime(2025, 1, 1), replay_asset_id_native=False)
    native = Portfolio(id=2, workspace_id=1, name="Native", cash_balance=0.0,
                        created_at=datetime(2025, 1, 1), replay_asset_id_native=True)
    db.add(legacy); db.add(native)
    db.commit()

    payload = _payload(
        predecessor_asset_id=2501, predecessor_symbol="S7PARPRED.BK", shares_surrendered="10",
        successor_asset_id=2502, successor_symbol="S7PARSUCC.BK", successor_provider_symbol="S7PARSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    for pid, native_mode in [(1, False), (2, True)]:
        _add_tx(db, pid * 10 + 1, pid, "INITIAL_POSITION", symbol="S7PARPRED.BK",
                shares=10, price=10, amount=0.0, date_=datetime(2026, 1, 1),
                asset_id=2501 if native_mode else None)
        _add_tx(db, pid * 10 + 2, pid, "POSITION_CONVERSION", symbol="S7PARPRED.BK",
                asset_id=2501, date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    legacy_result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    native_result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=2, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert legacy_result.committed is True
    assert native_result.committed is True

    legacy_item = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="S7PARSUCC.BK").first()
    native_item = db.query(PortfolioItem).filter_by(portfolio_id=2, symbol="S7PARSUCC.BK").first()
    assert legacy_item.asset_id == native_item.asset_id == 2502
    assert legacy_item.shares == native_item.shares == pytest.approx(10.0)
    assert legacy_item.avg_cost == native_item.avg_cost == pytest.approx(10.0)

    legacy_state, legacy_findings = _validator_state(db, 1)
    native_state, native_findings = _validator_state(db, 2)
    assert legacy_findings == [] and native_findings == []
    assert legacy_state.holdings["S7PARSUCC.BK"] == native_state.holdings["S7PARSUCC.BK"] == Decimal("10")
    assert legacy_state.basis["S7PARSUCC.BK"] == native_state.basis["S7PARSUCC.BK"] == Decimal("100")
    assert legacy_state.identity["S7PARSUCC.BK"] == native_state.identity["S7PARSUCC.BK"] == ("S7PARSUCC.BK", 2502)


def test_step7_cross_engine_parity_historical_null_asset_fallback(db_session):
    """Fixture 7/9: native-mode portfolio, but the predecessor's own
    creating transaction was never asset-ID backfilled — both engines must
    resolve it via the canonical-symbol fallback tier."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0, replay_asset_id_native=True)
    payload = _payload(
        predecessor_asset_id=2701, predecessor_symbol="S7NAFPRED.BK", shares_surrendered="10",
        successor_asset_id=2702, successor_symbol="S7NAFSUCC.BK", successor_provider_symbol="S7NAFSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7NAFPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1), asset_id=None)   # never backfilled
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="S7NAFPRED.BK", asset_id=2701,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True
    successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="S7NAFSUCC.BK").first()
    assert successor.shares == pytest.approx(10.0)

    state, findings = _validator_state(db, 1)
    assert findings == []
    assert state.holdings["S7NAFSUCC.BK"] == Decimal("10")


def test_step7_cross_engine_parity_raw_symbol_differs_from_canonical(db_session):
    """Fixture 8/9: raw ledger symbol differs from the canonical/payload
    symbol. "RAWDIFFSYM" (bare, pure-alphabetic) canonicalizes to
    "RAWDIFFSYM.BK" (services.symbol_normalization rule 5, Thai default
    suffixing) — the raw ledger holding key differs from the payload's
    predecessor symbol. The conversion row itself also carries the bare
    "RAWDIFFSYM" raw form (not "RAWDIFFSYM.BK") — using a different raw form
    on the conversion row than on the predecessor row would itself trigger
    an unrelated CRITICAL SYMBOL_ALIAS finding (ADR-005, two raw forms
    resolving to the same canonical symbol), which is not what this fixture
    is testing."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=2801, predecessor_symbol="RAWDIFFSYM.BK", shares_surrendered="10",
        successor_asset_id=2802, successor_symbol="RAWDIFFSUCC.BK", successor_provider_symbol="RAWDIFFSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="RAWDIFFSYM", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="RAWDIFFSYM", asset_id=2801,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True
    successor = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="RAWDIFFSUCC.BK").first()
    assert successor is not None
    assert successor.shares == pytest.approx(10.0)

    state, findings = _validator_state(db, 1)
    assert findings == []
    assert "RAWDIFFSYM" not in state.holdings
    assert state.holdings["RAWDIFFSUCC.BK"] == Decimal("10")


def test_step7_repeated_replay_is_deterministic_both_engines(db_session):
    """Fixture 9/9 plus objective 7 (determinism): the same immutable ledger
    must produce byte-identical results across repeated runs, in both
    engines independently."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=2901, predecessor_symbol="S7DETPRED.BK", shares_surrendered="10",
        successor_asset_id=2902, successor_symbol="S7DETSUCC.BK", successor_provider_symbol="S7DETSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7DETPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="S7DETPRED.BK", asset_id=2901,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    r1 = asyncio.run(rebuild_portfolio(db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True))
    r2 = asyncio.run(rebuild_portfolio(db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True))
    assert r1.reconstructed_cash == r2.reconstructed_cash
    assert r1.reconstructed_holdings_count == r2.reconstructed_holdings_count
    rows1 = {(r.identifier, r.field): r.reconstructed_value for r in r1.reconciliation_report}
    rows2 = {(r.identifier, r.field): r.reconstructed_value for r in r2.reconciliation_report}
    assert rows1 == rows2

    state1, findings1 = _validator_state(db, 1)
    state2, findings2 = _validator_state(db, 1)
    assert state1.holdings == state2.holdings
    assert state1.basis == state2.basis
    assert state1.identity == state2.identity
    assert state1.cash == state2.cash
    assert [f.check_id for f in findings1] == [f.check_id for f in findings2]


# ── Objective 4 — invalid-fixture disposition parity (10 categories) ──────────

def test_step7_invalid_malformed_payload_both_engines_agree(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7MALPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="S7MALPRED.BK", asset_id=3001,
            date_=datetime(2026, 3, 2), conversion_payload={"schema_version": 2})
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(db=db, portfolio_id=1, workspace_id=1, mode="raw"))
    matches = [f for f in report.findings if f.check_id == "POSITION_CONVERSION_PAYLOAD_INVALID"]
    assert len(matches) == 1
    assert matches[0].severity.value == "CRITICAL"


def test_step7_invalid_raw_asset_id_mismatch_both_engines_agree(db_session):
    """Step 7 surfaced and fixed a real gap here: in legacy replay mode,
    CanonicalTransaction.asset_id is always None (WP1 design), so the
    validator's IDENTITY_INVALID check previously compared against nothing
    and silently passed a conversion whose RAW asset_id column disagrees
    with its payload's predecessor.asset_id — while the rebuilder's
    preflight (which reads the raw Transaction row directly, per its own
    documented rationale) always caught it. ledger_validator.py now threads
    the raw asset_id through validate_portfolio_ledger() ->
    _replay_and_check() -> _apply_position_conversion() so both engines
    agree on this legacy-mode disposition."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)   # legacy mode (default)
    payload = _payload(
        predecessor_asset_id=3101, predecessor_symbol="S7IDPRED.BK", shares_surrendered="10",
        successor_asset_id=3102, successor_symbol="S7IDSUCC.BK", successor_provider_symbol="S7IDSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7IDPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    # Raw tx.asset_id (999) disagrees with payload.predecessor.asset_id (3101);
    # symbol/date/shares/basis otherwise all agree.
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="S7IDPRED.BK", asset_id=999,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(db=db, portfolio_id=1, workspace_id=1, mode="raw"))
    matches = [f for f in report.findings if f.check_id == "POSITION_CONVERSION_IDENTITY_INVALID"]
    assert len(matches) == 1


def test_step7_invalid_missing_predecessor_both_engines_agree(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=3301, predecessor_symbol="S7NHPRED.BK", shares_surrendered="10",
        successor_asset_id=3302, successor_symbol="S7NHSUCC.BK", successor_provider_symbol="S7NHSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "POSITION_CONVERSION", symbol="S7NHPRED.BK", asset_id=3301,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(db=db, portfolio_id=1, workspace_id=1, mode="raw"))
    matches = [f for f in report.findings if f.check_id == "POSITION_CONVERSION_WITHOUT_HOLDING"]
    assert len(matches) == 1


def test_step7_invalid_ambiguous_predecessor_both_engines_agree(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0, replay_asset_id_native=True)
    payload = _payload(
        predecessor_asset_id=3401, predecessor_symbol="S7AMBPRED.BK", shares_surrendered="10",
        successor_asset_id=3402, successor_symbol="S7AMBSUCC.BK", successor_provider_symbol="S7AMBSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7AMBOTHER.BK", shares=5, price=10, amount=0.0,
            date_=datetime(2026, 1, 1), asset_id=3401)   # matches by asset_id
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="S7AMBPRED.BK", shares=5, price=10, amount=0.0,
            date_=datetime(2026, 1, 2), asset_id=None)   # matches by canonical symbol only
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="S7AMBPRED.BK", asset_id=3401,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(db=db, portfolio_id=1, workspace_id=1, mode="raw"))
    matches = [f for f in report.findings if f.check_id == "POSITION_CONVERSION_AMBIGUOUS_HOLDING"]
    assert len(matches) == 1


def test_step7_invalid_share_mismatch_both_engines_agree(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=3501, predecessor_symbol="S7SMPRED.BK", shares_surrendered="999",
        successor_asset_id=3502, successor_symbol="S7SMSUCC.BK", successor_provider_symbol="S7SMSUCC.BK",
        shares_entitled="999", shares_received="999", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7SMPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="S7SMPRED.BK", asset_id=3501,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(db=db, portfolio_id=1, workspace_id=1, mode="raw"))
    matches = [f for f in report.findings if f.check_id == "POSITION_CONVERSION_SHARE_MISMATCH"]
    assert len(matches) == 1


def test_step7_invalid_basis_mismatch_both_engines_agree(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=3601, predecessor_symbol="S7BMPRED.BK", shares_surrendered="10",
        successor_asset_id=3602, successor_symbol="S7BMSUCC.BK", successor_provider_symbol="S7BMSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="999.00", basis_allocated="0", basis_carried="999.00",   # real basis is 100
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7BMPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="S7BMPRED.BK", asset_id=3601,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(db=db, portfolio_id=1, workspace_id=1, mode="raw"))
    matches = [f for f in report.findings if f.check_id == "POSITION_CONVERSION_BASIS_MISMATCH"]
    assert len(matches) == 1


def test_step7_invalid_cash_in_lieu_fails_rebuilder_preflight_and_validator(db_session):
    """Both independent engines reject a top-level cash-leg projection mismatch.

    Rebuilder preflight is the primary surfacing site, so the exact §10
    bullet-1 result triple is required; the validator independently emits the
    corresponding active CRITICAL finding.
    """
    db = db_session
    _seed_workspace_and_portfolio(db, cash=1_000.0)
    payload = _payload(
        predecessor_asset_id=3701, predecessor_symbol="S7CILBADPRED.BK", shares_surrendered="8",
        successor_asset_id=3702, successor_symbol="S7CILBADSUCC.BK", successor_provider_symbol="S7CILBADSUCC.BK",
        shares_entitled="10", shares_received="9.5", conversion_ratio="1.25",
        basis_before="240", basis_allocated="12", basis_carried="228",
        cash_in_lieu={
            "fractional_entitlement_shares": "0.5", "gross_proceeds": "15",
            "fees": "1", "taxes": "0.5", "net_cash": "13.5",
            "basis_allocated": "12", "realized_pnl": "1.5",
        },
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7CILBADPRED.BK", shares=8, price=30, amount=0.0,
            date_=datetime(2026, 1, 1))
    # Top-level fees column (999.0) disagrees with payload cash_in_lieu.fees ("1").
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="S7CILBADPRED.BK", asset_id=3701,
            date_=datetime(2026, 3, 2), amount=228.0, fees=999.0, taxes=0.5,
            conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.aborted is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(db=db, portfolio_id=1, workspace_id=1, mode="raw"))
    matches = [f for f in report.findings if f.check_id == "POSITION_CONVERSION_CIL_INVALID"]
    assert len(matches) == 1
    assert matches[0].severity.value == "CRITICAL"


def test_step7_invalid_same_day_conflict_both_engines_agree(db_session):
    db = db_session
    _seed_workspace_and_portfolio(db, cash=100_000.0)
    payload = _payload(
        predecessor_asset_id=3801, predecessor_symbol="S7SDPRED.BK", shares_surrendered="10",
        successor_asset_id=3802, successor_symbol="S7SDSUCC.BK", successor_provider_symbol="S7SDSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7SDPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "BUY", symbol="S7SDPRED.BK", shares=1, price=10, amount=10,
            date_=datetime(2026, 3, 2))   # same calendar date, targets predecessor
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="S7SDPRED.BK", asset_id=3801,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.aborted is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(db=db, portfolio_id=1, workspace_id=1, mode="raw"))
    matches = [f for f in report.findings if f.check_id == "POSITION_CONVERSION_SAME_DAY_CONFLICT"]
    assert len(matches) == 1
    assert matches[0].severity.value == "ERROR"


@pytest.mark.parametrize("first_conversion_id,second_conversion_id", [(2, 3), (3, 2)])
def test_same_day_conversion_chain_fails_closed_in_both_id_orderings(
    db_session, first_conversion_id, second_conversion_id,
):
    """CRITICAL-1: transaction-ID order cannot make X→Y→Z valid."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    first_payload = _payload(
        predecessor_asset_id=3901, predecessor_symbol="CHAINX.BK", shares_surrendered="10",
        successor_asset_id=3902, successor_symbol="CHAINY.BK", successor_provider_symbol="CHAINY.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    second_payload = _payload(
        predecessor_asset_id=3902, predecessor_symbol="CHAINY.BK", shares_surrendered="10",
        successor_asset_id=3903, successor_symbol="CHAINZ.BK", successor_provider_symbol="CHAINZ.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="CHAINX.BK", shares=10, price=10,
            date_=datetime(2026, 1, 1))
    _add_tx(db, first_conversion_id, 1, "POSITION_CONVERSION", symbol="CHAINX.BK",
            asset_id=3901, date_=datetime(2026, 3, 2), conversion_payload=first_payload)
    _add_tx(db, second_conversion_id, 1, "POSITION_CONVERSION", symbol="CHAINY.BK",
            asset_id=3902, date_=datetime(2026, 3, 2), conversion_payload=second_payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.aborted is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(
        db=db, portfolio_id=1, workspace_id=1, mode="raw",
    ))
    assert any(
        finding.check_id == "POSITION_CONVERSION_SAME_DAY_CONFLICT"
        for finding in report.findings
    )


def test_multi_date_shared_successor_retains_each_binding_and_parity(db_session):
    """STEP9-MINOR-5 reassessment: dated A→S and B→S remain independent.

    The successor materialization view may group the final S row, but the
    authoritative relation map must retain both conversion transaction IDs.
    The fixture also exercises native mode's historical-null-asset fallback,
    then compares both modes against the independent validator replay.
    """
    def _run_mode(db, *, native: bool):
        _seed_workspace_and_portfolio(db, cash=0.0, replay_asset_id_native=native)
        db.add(PortfolioItem(
            workspace_id=1, portfolio_id=1, symbol="SHARED.BK",
            shares=1.0, avg_cost=1.0, asset_id=6103,
        ))
        first_payload = _payload(
            predecessor_asset_id=6101, predecessor_symbol="PRED_A.BK", shares_surrendered="10",
            successor_asset_id=6103, successor_symbol="SHARED.BK", successor_provider_symbol="SHARED.BK",
            shares_entitled="10", shares_received="10", conversion_ratio="1",
            basis_before="100", basis_allocated="0", basis_carried="100",
            transition_date="2026-03-02",
        )
        second_payload = _payload(
            predecessor_asset_id=6102, predecessor_symbol="PRED_B.BK", shares_surrendered="20",
            successor_asset_id=6103, successor_symbol="SHARED.BK", successor_provider_symbol="SHARED.BK",
            shares_entitled="20", shares_received="20", conversion_ratio="1",
            basis_before="400", basis_allocated="0", basis_carried="400",
            transition_date="2026-03-04",
        )
        _add_tx(
            db, 1, 1, "INITIAL_POSITION", symbol="PRED_A.BK", asset_id=6101,
            shares=10, price=10, amount=0.0, date_=datetime(2026, 1, 1),
        )
        # B's historical row has no asset_id; native conversion predecessor
        # resolution must use the approved canonical-symbol fallback.
        _add_tx(
            db, 2, 1, "INITIAL_POSITION", symbol="PRED_B.BK", asset_id=None,
            shares=20, price=20, amount=0.0, date_=datetime(2026, 1, 2),
        )
        _add_tx(
            db, 3, 1, "POSITION_CONVERSION", symbol="PRED_A.BK", asset_id=6101,
            date_=datetime(2026, 3, 2), conversion_payload=first_payload,
        )
        _add_tx(
            db, 4, 1, "POSITION_CONVERSION", symbol="PRED_B.BK", asset_id=6102,
            date_=datetime(2026, 3, 4), conversion_payload=second_payload,
        )
        db.commit()

        raw = (
            db.query(Transaction)
            .filter_by(portfolio_id=1)
            .order_by(Transaction.transaction_date, Transaction.id)
            .all()
        )
        ctxs = list(canonicalize_transactions(raw, prefer_asset_id=native))
        bindings = _resolve_conversion_successors(db, 1, ctxs)
        assert set(bindings) == {3, 4}
        assert [
            (tx_id, binding.successor_symbol, binding.successor_asset_id)
            for tx_id, binding in sorted(bindings.items())
        ] == [
            (3, "SHARED.BK", 6103),
            (4, "SHARED.BK", 6103),
        ]

        dates = ["2026-03-02", "2026-03-04"]
        replay_one = _replay_with_date_snapshots(ctxs, dates)
        replay_two = _replay_with_date_snapshots(ctxs, dates)

        def _rebuilder_signature(states):
            return {
                date: sorted(
                    (h.report_symbol, str(h.shares), str(h.avg_cost), h.price_symbol)
                    for h in state.holdings.values()
                )
                for date, state in states.items()
            }

        assert _rebuilder_signature(replay_one) == _rebuilder_signature(replay_two)
        d1 = replay_one["2026-03-02"]
        d2 = replay_one["2026-03-04"]
        d1_successor = next(h for h in d1.holdings.values() if h.report_symbol == "SHARED.BK")
        d2_successor = next(h for h in d2.holdings.values() if h.report_symbol == "SHARED.BK")
        assert d1_successor.shares == Decimal("10")
        assert d1_successor.avg_cost == Decimal("10")
        assert d2_successor.shares == Decimal("30")
        assert abs(d2_successor.shares * d2_successor.avg_cost - Decimal("500")) <= Decimal("0.000001")
        assert {h.report_symbol for h in d2.holdings.values()} == {"SHARED.BK"}

        validator_final, validator_findings, validator_snapshots = _replay_and_check(
            1,
            ctxs,
            dates,
            raw_asset_id_by_id={tx.id: tx.asset_id for tx in raw},
        )
        assert validator_findings == []
        assert validator_final.holdings == {"SHARED.BK": Decimal("30")}
        assert validator_final.basis == {"SHARED.BK": Decimal("500")}
        assert validator_final.identity == {"SHARED.BK": ("SHARED.BK", 6103)}
        assert validator_snapshots["2026-03-02"].holdings["SHARED.BK"] == Decimal("10")
        assert validator_snapshots["2026-03-04"].holdings["SHARED.BK"] == Decimal("30")

        result = asyncio.run(rebuild_portfolio(
            db=db, portfolio_id=1, workspace_id=1,
            skip_snapshots=True, dry_run=False,
        ))
        assert result.success is True
        assert result.committed is True
        successor_rows = [
            row for row in result.reconciliation_report
            if row.entity_type == "portfolio_item" and row.identifier == "SHARED.BK"
        ]
        assert {row.field for row in successor_rows} == {
            "asset_id", "symbol", "shares", "avg_cost", "basis",
        }
        assert next(row for row in successor_rows if row.field == "asset_id").status == ReconciliationStatus.MATCH
        successor = db.query(PortfolioItem).filter_by(
            portfolio_id=1, symbol="SHARED.BK",
        ).one()
        return {
            "shares": successor.shares,
            "avg_cost": successor.avg_cost,
            "asset_id": successor.asset_id,
            "cash": db.query(Portfolio).filter_by(id=1).one().cash_balance,
        }

    legacy = _run_mode(db_session, native=False)

    native_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(native_engine)
    NativeSession = sessionmaker(bind=native_engine)
    native_db = NativeSession()
    try:
        native = _run_mode(native_db, native=True)
    finally:
        native_db.close()
        native_engine.dispose()

    assert native == legacy


@pytest.mark.parametrize("native", [False, True], ids=["legacy", "native"])
def test_same_day_shared_successor_still_fails_closed(db_session, native):
    """CRITICAL-1 remains authoritative for A→S/B→S on one date."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0, replay_asset_id_native=native)
    first_payload = _payload(
        predecessor_asset_id=6201, predecessor_symbol="SAME_A.BK", shares_surrendered="10",
        successor_asset_id=6203, successor_symbol="SAME_S.BK", successor_provider_symbol="SAME_S.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
        transition_date="2026-03-02",
    )
    second_payload = _payload(
        predecessor_asset_id=6202, predecessor_symbol="SAME_B.BK", shares_surrendered="20",
        successor_asset_id=6203, successor_symbol="SAME_S.BK", successor_provider_symbol="SAME_S.BK",
        shares_entitled="20", shares_received="20", conversion_ratio="1",
        basis_before="400", basis_allocated="0", basis_carried="400",
        transition_date="2026-03-02",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="SAME_A.BK", asset_id=6201,
            shares=10, price=10, amount=0.0, date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "INITIAL_POSITION", symbol="SAME_B.BK", asset_id=6202,
            shares=20, price=20, amount=0.0, date_=datetime(2026, 1, 2))
    _add_tx(db, 3, 1, "POSITION_CONVERSION", symbol="SAME_A.BK", asset_id=6201,
            date_=datetime(2026, 3, 2), conversion_payload=first_payload)
    _add_tx(db, 4, 1, "POSITION_CONVERSION", symbol="SAME_B.BK", asset_id=6202,
            date_=datetime(2026, 3, 2), conversion_payload=second_payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.aborted is False
    assert result.committed is False

    report = asyncio.run(validate_portfolio_ledger(
        db=db, portfolio_id=1, workspace_id=1, mode="raw",
    ))
    assert any(
        finding.check_id == "POSITION_CONVERSION_SAME_DAY_CONFLICT"
        for finding in report.findings
    )


@pytest.mark.parametrize(
    "projection_overrides,expected_reason",
    [
        ({"shares": 999.0}, "POSITION_CONVERSION_SHARE_MISMATCH"),
        ({"price": 999.0}, "POSITION_CONVERSION_BASIS_MISMATCH"),
        ({"amount": 999.0}, "POSITION_CONVERSION_BASIS_MISMATCH"),
        ({"fees": 1.0}, "POSITION_CONVERSION_CIL_INVALID"),
        ({"taxes": 1.0}, "POSITION_CONVERSION_CIL_INVALID"),
    ],
)
def test_top_level_projection_mismatches_fail_both_engines(
    db_session, projection_overrides, expected_reason,
):
    """CRITICAL-2: all five compatibility projections are enforced."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    payload = _payload(
        predecessor_asset_id=4001, predecessor_symbol="PROJPRED.BK", shares_surrendered="10",
        successor_asset_id=4002, successor_symbol="PROJSUCC.BK", successor_provider_symbol="PROJSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="PROJPRED.BK", shares=10, price=10,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="PROJPRED.BK", asset_id=4001,
            date_=datetime(2026, 3, 2), conversion_payload=payload, **projection_overrides)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.aborted is False
    assert result.committed is False
    assert expected_reason in result.error

    report = asyncio.run(validate_portfolio_ledger(
        db=db, portfolio_id=1, workspace_id=1, mode="raw",
    ))
    assert any(finding.check_id == expected_reason for finding in report.findings)


def test_native_null_asset_fallback_merges_later_successor_trade(db_session):
    """CRITICAL-3: fallback resolution cannot split the native successor."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=1_000.0, replay_asset_id_native=True)
    payload = _payload(
        predecessor_asset_id=4101, predecessor_symbol="FALLPRED.BK", shares_surrendered="10",
        successor_asset_id=4102, successor_symbol="FALLSUCC.BK", successor_provider_symbol="FALLSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="FALLPRED.BK", shares=10, price=10,
            asset_id=None, date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="FALLPRED.BK", asset_id=4101,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    _add_tx(db, 3, 1, "BUY", symbol="FALLSUCC.BK", asset_id=4102, shares=2, price=10,
            amount=20.0, date_=datetime(2026, 3, 3))
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.committed is True
    items = db.query(PortfolioItem).filter_by(portfolio_id=1, symbol="FALLSUCC.BK").all()
    assert len(items) == 1
    assert items[0].asset_id == 4102
    assert items[0].shares == pytest.approx(12.0)
    assert items[0].avg_cost == pytest.approx(10.0)


def test_reconciliation_uses_asset_paired_successor_when_symbols_differ(db_session):
    """MAJOR-1: consume the Step-5 asset-first pairing at reconciliation."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=0.0)
    db.add(PortfolioItem(
        workspace_id=1, portfolio_id=1, symbol="LEGACYNAME.BK",
        shares=2.0, avg_cost=5.0, asset_id=4202,
    ))
    payload = _payload(
        predecessor_asset_id=4201, predecessor_symbol="PAIRPRED.BK", shares_surrendered="10",
        successor_asset_id=4202, successor_symbol="PAIRSUCC.BK", successor_provider_symbol="PAIRSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="PAIRPRED.BK", shares=10, price=10,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="PAIRPRED.BK", asset_id=4201,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True,
    ))
    rows = [
        row for row in result.reconciliation_report
        if row.entity_type == "portfolio_item" and row.identifier == "PAIRSUCC.BK"
    ]
    assert {row.field for row in rows} == {"asset_id", "symbol", "shares", "avg_cost", "basis"}
    assert next(row for row in rows if row.field == "symbol").status.value == "DIFFERENT"
    assert not any(
        row.identifier == "LEGACYNAME.BK" and row.field == "*"
        for row in result.reconciliation_report
    )


def test_step7_conflicting_successor_identity_is_rebuilder_only_by_design(db_session):
    """The tenth invalid category (conflicting successor identity) is a
    materialization-time concern: it compares the conversion's authoritative
    successor identity against a currently STORED PortfolioItem row the
    ledger alone never reveals (BANPU-WP2 Step 5,
    _resolve_conversion_successors). The frozen finding catalog has no
    counterpart for it — PositionConversionReplayError's own docstring says
    so explicitly. Per Step 7 objective 4's closing instruction ("do not
    invent a new validator finding for a rebuilder-only materialization
    conflict unless the frozen catalog requires one"), the correct
    disposition is: rebuilder fails closed, validator produces NO finding at
    all (it never sees PortfolioItem rows) — a deliberate, architecturally
    scoped asymmetry, not a defect."""
    db = db_session
    _seed_workspace_and_portfolio(db, cash=42_000.0)
    db.add(PortfolioItem(workspace_id=1, portfolio_id=1, symbol="S7CSUCC.BK",
                          shares=1.0, avg_cost=1.0, asset_id=9999))
    db.commit()

    payload = _payload(
        predecessor_asset_id=3901, predecessor_symbol="S7CPRED.BK", shares_surrendered="10",
        successor_asset_id=4002, successor_symbol="S7CSUCC.BK", successor_provider_symbol="S7CSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    _add_tx(db, 1, 1, "INITIAL_POSITION", symbol="S7CPRED.BK", shares=10, price=10, amount=0.0,
            date_=datetime(2026, 1, 1))
    _add_tx(db, 2, 1, "POSITION_CONVERSION", symbol="S7CPRED.BK", asset_id=3901,
            date_=datetime(2026, 3, 2), conversion_payload=payload)
    db.commit()

    result = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=False,
    ))
    assert result.success is False
    assert result.committed is False

    # The validator has no visibility into stored PortfolioItem rows at all —
    # by ledger inspection alone this conversion is entirely valid.
    state, findings = _validator_state(db, 1)
    assert findings == []
    assert state.holdings["S7CSUCC.BK"] == Decimal("10")
