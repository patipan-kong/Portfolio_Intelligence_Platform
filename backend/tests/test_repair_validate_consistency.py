"""Single-source-of-truth regression test — apply_repair vs validate_ledger.

Both `manage.py apply_repair` and `manage.py validate_ledger --effective` /
`--compare` must derive their findings from the exact same code path:
services.ledger_validator.validate_portfolio_ledger(mode="effective").

repair_plan_executor.py has no private replay logic of its own — it only
calls validate_portfolio_ledger() (imported, never reimplemented). This test
proves that invariant end-to-end against a real database: a repair plan
applied for real (committed, not dry-run) produces an effective_after report
that is byte-for-byte identical (by finding key + severity) to a report
computed independently afterwards, in a fresh session, via
compare_ledger_validation() — the same call validate_ledger --compare uses.

Uses a real in-memory SQLite database (not mocks) so the comparison is
meaningful: mocked validate_portfolio_ledger (as in
test_ledger_repair_executor.py) cannot detect a divergence between the two
call sites.
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401 — registers the `assets` FK target table on Base.metadata
from models.database import Base, LedgerRepair, Portfolio, Transaction, Workspace
from services.ledger_repair import load_active_repairs
from services.ledger_validator import _finding_key, compare_ledger_validation, validate_portfolio_ledger
from services.portfolio_rebuilder import rebuild_portfolio
from services.repair_plan_executor import RepairPlan, RepairPlanOperation, apply_repair_plan


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


@pytest.fixture()
def seeded_portfolio(db_session):
    """One portfolio with a duplicate INITIAL_POSITION (triggers DUP_INITIAL_POSITION CRITICAL)."""
    ws = Workspace(id=1, name="Default")
    db_session.add(ws)

    created_at = datetime(2026, 1, 1)
    portfolio = Portfolio(
        id=1, workspace_id=1, name="Test Portfolio",
        cash_balance=0.0, created_at=created_at,
    )
    db_session.add(portfolio)

    tx_date = datetime(2026, 2, 1)
    tx1 = Transaction(
        id=10, workspace_id=1, portfolio_id=1, symbol="GULF.BK",
        transaction_type="INITIAL_POSITION", shares=100, price_per_share=10,
        total_amount=1000, fees=0, taxes=0, transaction_date=tx_date,
        created_at=tx_date,
    )
    tx2 = Transaction(
        id=11, workspace_id=1, portfolio_id=1, symbol="GULF.BK",
        transaction_type="INITIAL_POSITION", shares=100, price_per_share=10,
        total_amount=1000, fees=0, taxes=0, transaction_date=tx_date,
        created_at=tx_date,
    )
    db_session.add_all([tx1, tx2])
    db_session.commit()
    return db_session


def test_apply_repair_commit_matches_independent_compare(seeded_portfolio):
    """After a real (non-dry-run) apply, a fresh compare_ledger_validation() call
    must report the exact same effective findings apply_repair_plan returned.
    """
    db = seeded_portfolio

    plan = RepairPlan(
        schema_version="1.0",
        portfolio_id=1,
        repair_plan_id="plan-consistency-001",
        generated_at="2026-02-02T00:00:00Z",
        operations=[RepairPlanOperation(
            repair_type="EXCLUDE",
            transaction_id=11,
            reason="Duplicate INITIAL_POSITION, keep tx10",
            reason_code="DUP_INITIAL_POSITION",
        )],
    )

    with patch("services.repair_plan_executor._backup_repairs", return_value="/tmp/fake-backup.json"):
        result = asyncio.run(apply_repair_plan(
            db=db, plan=plan, portfolio_id=1, workspace_id=1,
            dry_run=False, force=True,
        ))

    assert result.error is None
    assert result.rollback is False
    assert result.operations_inserted == 1
    assert result.effective_after is not None

    # Independently re-derive the effective report the same way
    # `manage.py validate_ledger --compare --effective` does: load the
    # now-committed repairs in a fresh query and run compare_ledger_validation().
    repairs = load_active_repairs(db, 1)
    assert len(repairs) == 1
    assert isinstance(repairs[0], LedgerRepair)

    comparison = asyncio.run(compare_ledger_validation(
        db=db, portfolio_id=1, workspace_id=1, repairs=repairs,
    ))

    apply_keys = {_finding_key(f) for f in result.effective_after.findings}
    compare_keys = {_finding_key(f) for f in comparison.effective_report.findings}
    assert apply_keys == compare_keys

    apply_sev = {_finding_key(f): f.severity for f in result.effective_after.findings}
    compare_sev = {_finding_key(f): f.severity for f in comparison.effective_report.findings}
    assert apply_sev == compare_sev

    # The duplicate INITIAL_POSITION finding must be resolved in both views.
    dup_key_prefix = "DUP_INITIAL_POSITION:"
    assert not any(k.startswith(dup_key_prefix) for k in apply_keys)
    assert not any(k.startswith(dup_key_prefix) for k in compare_keys)
    assert any(k.startswith(dup_key_prefix) for k in comparison.resolved_findings)


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP2 Step 2 — conversion repair-parity fixtures
#
# Work Package Plan §5 WP2-T7 / Implementation Specification §9.3: repairs must
# never remove or suppress conversion authority. WP2 production behavior does
# not exist yet, so every fixture below is expected to fail until it is added
# at the ledger_validator.py / portfolio_rebuilder.py consumer boundary.
# ══════════════════════════════════════════════════════════════════════════════

def _conv_payload(
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


@pytest.fixture()
def conversion_without_holding_portfolio(db_session):
    """One portfolio with a POSITION_CONVERSION row that has no predecessor
    holding at all — deterministically triggers POSITION_CONVERSION_WITHOUT_HOLDING
    once WP2 is implemented, in both raw and effective validation modes."""
    db = db_session
    db.add(Workspace(id=1, name="Default"))
    db.add(Portfolio(id=1, workspace_id=1, name="Test Portfolio",
                      cash_balance=0.0, created_at=datetime(2025, 1, 1)))
    payload = _conv_payload(
        predecessor_asset_id=301, predecessor_symbol="RPRED.BK", shares_surrendered="10",
        successor_asset_id=302, successor_symbol="RSUCC.BK", successor_provider_symbol="RSUCC.BK",
        shares_entitled="10", shares_received="10", conversion_ratio="1",
        basis_before="100", basis_allocated="0", basis_carried="100",
    )
    db.add(Transaction(
        id=1, workspace_id=1, portfolio_id=1, symbol="RPRED.BK",
        transaction_type="POSITION_CONVERSION", asset_id=301,
        total_amount=0.0, fees=0.0, taxes=0.0,
        transaction_date=datetime(2026, 3, 2), created_at=datetime(2026, 3, 2),
        conversion_payload=payload,
    ))
    db.commit()
    return db


def test_position_conversion_exclude_repair_is_ineffective(conversion_without_holding_portfolio):
    """An EXCLUDE repair targeting the conversion transaction must not remove
    its finding from the effective report — the conversion remains in the
    effective canonical sequence regardless of repair overlays."""
    db = conversion_without_holding_portfolio

    raw_report = asyncio.run(validate_portfolio_ledger(db=db, portfolio_id=1, workspace_id=1, mode="raw"))
    raw_matches = [f for f in raw_report.findings if f.check_id == "POSITION_CONVERSION_WITHOUT_HOLDING"]
    assert len(raw_matches) == 1

    exclude = LedgerRepair(portfolio_id=1, transaction_id=1, repair_plan_id="p-exclude",
                            repair_type="EXCLUDE", reason="test", created_by="test", is_active=True)
    db.add(exclude)
    db.commit()

    eff_report = asyncio.run(validate_portfolio_ledger(
        db=db, portfolio_id=1, workspace_id=1, repairs=[exclude], mode="effective",
    ))
    eff_matches = [f for f in eff_report.findings if f.check_id == "POSITION_CONVERSION_WITHOUT_HOLDING"]
    assert len(eff_matches) == 1
    assert _finding_key(eff_matches[0]) == _finding_key(raw_matches[0])


def test_position_conversion_suppress_finding_repair_cannot_suppress(conversion_without_holding_portfolio):
    """A SUPPRESS_FINDING repair naming the conversion's check_id must not
    silence an active conversion finding."""
    db = conversion_without_holding_portfolio

    suppress = LedgerRepair(
        portfolio_id=1, transaction_id=1, repair_plan_id="p-suppress",
        repair_type="SUPPRESS_FINDING", reason_code="POSITION_CONVERSION_WITHOUT_HOLDING",
        reason="test", created_by="test", is_active=True,
    )
    db.add(suppress)
    db.commit()

    eff_report = asyncio.run(validate_portfolio_ledger(
        db=db, portfolio_id=1, workspace_id=1, repairs=[suppress], mode="effective",
    ))
    matches = [f for f in eff_report.findings if f.check_id == "POSITION_CONVERSION_WITHOUT_HOLDING"]
    assert len(matches) == 1


def test_position_conversion_apply_repairs_true_false_identical_economics(db_session):
    """rebuild_portfolio(apply_repairs=True) and apply_repairs=False must reach
    the same conversion economics when no repair targets the conversion or its
    predecessor — both must reflect the *correct* post-conversion cash, not
    merely agree with each other."""
    db = db_session
    db.add(Workspace(id=1, name="Default"))
    db.add(Portfolio(id=1, workspace_id=1, name="Test Portfolio",
                      cash_balance=0.0, created_at=datetime(2025, 1, 1)))
    payload = _conv_payload(
        predecessor_asset_id=401, predecessor_symbol="EPRED.BK", shares_surrendered="8",
        successor_asset_id=402, successor_symbol="ESUCC.BK", successor_provider_symbol="ESUCC.BK",
        shares_entitled="10", shares_received="9.5", conversion_ratio="1.25",
        basis_before="240", basis_allocated="12", basis_carried="228",
        cash_in_lieu={
            "fractional_entitlement_shares": "0.5", "gross_proceeds": "15",
            "fees": "1", "taxes": "0.5", "net_cash": "13.5",
            "basis_allocated": "12", "realized_pnl": "1.5",
        },
    )
    db.add(Transaction(id=1, workspace_id=1, portfolio_id=1, symbol=None,
                        transaction_type="DEPOSIT", total_amount=1_000.0, fees=0.0, taxes=0.0,
                        transaction_date=datetime(2026, 1, 1), created_at=datetime(2026, 1, 1)))
    db.add(Transaction(id=2, workspace_id=1, portfolio_id=1, symbol="EPRED.BK",
                        transaction_type="INITIAL_POSITION", shares=8, price_per_share=30,
                        total_amount=0.0, fees=0.0, taxes=0.0,
                        transaction_date=datetime(2026, 1, 2), created_at=datetime(2026, 1, 2)))
    db.add(Transaction(id=3, workspace_id=1, portfolio_id=1, symbol="EPRED.BK",
                        transaction_type="POSITION_CONVERSION", asset_id=401,
                        shares=9.5, price_per_share=24.0,
                        total_amount=228.0, fees=1.0, taxes=0.5,
                        transaction_date=datetime(2026, 3, 2), created_at=datetime(2026, 3, 2),
                        conversion_payload=payload))
    db.commit()

    expected_cash = 1_000.0 + 13.5   # starting DEPOSIT plus admitted net cash-in-lieu (Cn)

    result_true = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True, apply_repairs=True,
    ))
    result_false = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True, apply_repairs=False,
    ))

    assert result_true.reconstructed_cash == pytest.approx(expected_cash)
    assert result_false.reconstructed_cash == pytest.approx(expected_cash)


# ══════════════════════════════════════════════════════════════════════════════
# BANPU-WP2 Step 7 — repair parity (objective 5), extending the cash-only
# check above to the full successor economic state.
# ══════════════════════════════════════════════════════════════════════════════

def test_position_conversion_apply_repairs_true_false_identical_successor_state(db_session):
    """apply_repairs=True and apply_repairs=False must reach identical
    successor asset_id/symbol/shares/avg_cost/basis — not just cash — when no
    repair targets the conversion or its predecessor."""
    db = db_session
    db.add(Workspace(id=1, name="Default"))
    db.add(Portfolio(id=1, workspace_id=1, name="Test Portfolio",
                      cash_balance=0.0, created_at=datetime(2025, 1, 1)))
    payload = _conv_payload(
        predecessor_asset_id=451, predecessor_symbol="S7RPPRED.BK", shares_surrendered="8",
        successor_asset_id=452, successor_symbol="S7RPSUCC.BK", successor_provider_symbol="S7RPSUCC.BK",
        shares_entitled="10", shares_received="9.5", conversion_ratio="1.25",
        basis_before="240", basis_allocated="12", basis_carried="228",
        cash_in_lieu={
            "fractional_entitlement_shares": "0.5", "gross_proceeds": "15",
            "fees": "1", "taxes": "0.5", "net_cash": "13.5",
            "basis_allocated": "12", "realized_pnl": "1.5",
        },
    )
    db.add(Transaction(id=1, workspace_id=1, portfolio_id=1, symbol=None,
                        transaction_type="DEPOSIT", total_amount=1_000.0, fees=0.0, taxes=0.0,
                        transaction_date=datetime(2026, 1, 1), created_at=datetime(2026, 1, 1)))
    db.add(Transaction(id=2, workspace_id=1, portfolio_id=1, symbol="S7RPPRED.BK",
                        transaction_type="INITIAL_POSITION", shares=8, price_per_share=30,
                        total_amount=0.0, fees=0.0, taxes=0.0,
                        transaction_date=datetime(2026, 1, 2), created_at=datetime(2026, 1, 2)))
    db.add(Transaction(id=3, workspace_id=1, portfolio_id=1, symbol="S7RPPRED.BK",
                        transaction_type="POSITION_CONVERSION", asset_id=451,
                        shares=9.5, price_per_share=24.0,
                        total_amount=228.0, fees=1.0, taxes=0.5,
                        transaction_date=datetime(2026, 3, 2), created_at=datetime(2026, 3, 2),
                        conversion_payload=payload))
    db.commit()

    result_true = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True, apply_repairs=True,
    ))
    result_false = asyncio.run(rebuild_portfolio(
        db=db, portfolio_id=1, workspace_id=1, skip_snapshots=True, dry_run=True, apply_repairs=False,
    ))

    # No PortfolioItem row pre-exists for the successor symbol, so
    # _reconcile_portfolio_items takes its MISSING branch (field="*",
    # reconstructed_value={"shares": ..., "avg_cost": ...}) rather than the
    # five-field conversion_successors branch (which requires a pre-existing
    # stored row to compare against — see
    # test_rebuild_precommit_five_field_reconciliation_shows_independent_fields
    # in test_position_conversion_replay.py for that case).
    rows_true = [
        r for r in result_true.reconciliation_report
        if r.entity_type == "portfolio_item" and r.identifier == "S7RPSUCC.BK"
    ]
    rows_false = [
        r for r in result_false.reconciliation_report
        if r.entity_type == "portfolio_item" and r.identifier == "S7RPSUCC.BK"
    ]
    assert len(rows_true) == 1 and len(rows_false) == 1
    assert rows_true[0].reconstructed_value == rows_false[0].reconstructed_value
    assert rows_true[0].reconstructed_value["shares"] == pytest.approx(9.5)
    shares = rows_true[0].reconstructed_value["shares"]
    avg_cost = rows_true[0].reconstructed_value["avg_cost"]
    assert shares * avg_cost == pytest.approx(228.0, abs=0.01)
