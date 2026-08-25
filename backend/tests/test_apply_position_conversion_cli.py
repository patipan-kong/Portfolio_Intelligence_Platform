"""BANPU-WP7 — focused CLI tests for `manage.py apply_position_conversion`.

Real in-memory SQLite database (not mocks), mirroring the db_session pattern
already used by test_position_conversion_live.py / test_delete_portfolio.py.
`manage.SessionLocal` is patched per-test to return a pre-built in-memory
session (test_delete_portfolio.py precedent) — the command's own
`db.close()` is harmless against the SQLite `:memory:` SingletonThreadPool
used here, so post-call assertions against the same session object remain
valid.

Covers the WP7 Work Package Plan §10 acceptance matrix items evaluable
without a live rehearsal environment: WP7-A1-A5, A7-A9, A16-A19.
"""
from __future__ import annotations

import asyncio
import json
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401 -- registers the assets/* tables on Base.metadata
from models.database import Base, Portfolio, PortfolioItem, Transaction, Workspace
from services import asset_registry as registry
from services.asset_domain import AssetClaim, AssetType, IdentifierRecord, IdentifierType
from services.portfolio_rebuilder import (
    RebuildResult,
    ReconciliationRow,
    ReconciliationStatus,
)
from services.portfolio_rebuilder import rebuild_portfolio as _real_rebuild_portfolio

from manage import (
    _cmd_apply_position_conversion,
    _diff_reconstructed_holdings,
    _extract_reconstructed_holdings,
    _preflight_replay_mode_sanity,
)


# ══════════════════════════════════════════════════════════════════════════
# DB / fixture helpers
# ══════════════════════════════════════════════════════════════════════════

FIXTURE_PATH = "tests/fixtures/banpu_wp7_position_conversion_manifest.json"


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)()


def _seed_workspace_and_portfolio(db, *, portfolio_id: int = 1, cash: float = 0.0) -> Portfolio:
    db.add(Workspace(id=1, name="Default"))
    portfolio = Portfolio(
        id=portfolio_id, workspace_id=1, name="Test Portfolio",
        cash_balance=cash, created_at=datetime(2025, 1, 1),
    )
    db.add(portfolio)
    db.commit()
    return portfolio


def _mint_predecessor_and_successor(
    db,
    *,
    predecessor_symbol: str = "BANPU",
    successor_symbol: str = "BANPUU",
    predecessor_provider_symbol: str = "BANPU.BK",
):
    """Mint both assets with the predecessor carrying a current PROVIDER_SYMBOL
    identifier, but WITHOUT preparing the registry — apply_position_conversion
    --commit is the thing under test that must call
    prepare_position_conversion_registry() itself."""
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
    db.commit()
    return predecessor, successor


def _add_holding(db, *, portfolio_id: int, symbol: str, shares: float, avg_cost: float, asset_id: int) -> PortfolioItem:
    item = PortfolioItem(
        workspace_id=1, portfolio_id=portfolio_id, symbol=symbol,
        shares=shares, avg_cost=avg_cost, asset_id=asset_id,
    )
    db.add(item)
    db.commit()
    return item


def _add_initial_position_ledger_row(
    db, *, portfolio_id: int, asset_id: int, symbol: str = "BANPU.BK",
    shares: float = 6700, basis: float = 48709.00,
) -> Transaction:
    """Backs the directly-seeded PortfolioItem with a real ledger entry, so
    rebuild_portfolio's full transaction replay (used by the both-replay-mode
    sanity preflight) has a predecessor holding to convert, matching how a
    live portfolio always reaches this state through the transaction ledger."""
    tx = Transaction(
        workspace_id=1, portfolio_id=portfolio_id, symbol=symbol,
        transaction_type="INITIAL_POSITION", shares=shares,
        price_per_share=basis / shares, total_amount=basis,
        fees=0.0, taxes=0.0, transaction_date=datetime(2020, 1, 1),
        asset_id=asset_id,
    )
    db.add(tx)
    db.commit()
    return tx


def _manifest_dict(*, predecessor_asset_id: int, successor_asset_id: int, **overrides) -> dict:
    with open(FIXTURE_PATH, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    payload["predecessor"]["asset_id"] = predecessor_asset_id
    payload["successor"]["asset_id"] = successor_asset_id
    for path, value in overrides.items():
        # dotted path override, e.g. "boundary_evidence.successor_reference_price"
        keys = path.split(".")
        node = payload
        for key in keys[:-1]:
            node = node[key]
        node[keys[-1]] = value
    return payload


def _write_manifest(tmp_path, payload: dict, name: str = "manifest.json") -> str:
    p = tmp_path / name
    p.write_text(json.dumps(payload), encoding="utf-8")
    return str(p)


def _args(*, manifest: str, portfolio: int | None = 1, commit: bool = False, dry_run: bool = False) -> SimpleNamespace:
    return SimpleNamespace(manifest=manifest, portfolio=portfolio, commit=commit, dry_run=dry_run)


def _patch_session(db):
    return patch("manage.SessionLocal", return_value=db)


def _seed_full_scenario(tmp_path, *, manifest_overrides: dict | None = None):
    """Seed workspace + portfolio + predecessor/successor assets (registry
    unprepared) + a matching predecessor holding, and write a manifest file
    pointing at them. Returns (db, portfolio_id, manifest_path, predecessor, successor)."""
    db = make_session()
    portfolio = _seed_workspace_and_portfolio(db)
    predecessor, successor = _mint_predecessor_and_successor(db)
    _add_initial_position_ledger_row(db, portfolio_id=portfolio.id, asset_id=predecessor.id)
    _add_holding(db, portfolio_id=portfolio.id, symbol="BANPU.BK", shares=6700, avg_cost=48709.00 / 6700, asset_id=predecessor.id)
    payload = _manifest_dict(
        predecessor_asset_id=predecessor.id,
        successor_asset_id=successor.id,
        **(manifest_overrides or {}),
    )
    manifest_path = _write_manifest(tmp_path, payload)
    return db, portfolio.id, manifest_path, predecessor, successor


def _run(db, args) -> int:
    with _patch_session(db):
        return asyncio.run(_cmd_apply_position_conversion(args))


# ══════════════════════════════════════════════════════════════════════════
# Identity ingress (WP7-A7)
# ══════════════════════════════════════════════════════════════════════════

def test_missing_portfolio_fails_closed_no_write(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    exit_code = _run(db, _args(manifest=manifest, portfolio=None))
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0


def test_nonexistent_portfolio_fails_closed_no_write(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    exit_code = _run(db, _args(manifest=manifest, portfolio=999999))
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0


def test_workspace_derived_from_portfolio_not_caller_supplied(tmp_path):
    """ws_id must come from Portfolio.workspace_id — the command never reads
    a caller-supplied ws_id or db.query(Workspace).first()."""
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    # A second workspace with id != 1 exists; if the command wrongly used
    # Workspace.first() this would still resolve to workspace_id=1 by luck,
    # so assert explicitly on the portfolio's own column instead.
    portfolio = db.query(Portfolio).filter_by(id=pid).one()
    expected_ws_id = portfolio.workspace_id
    assert expected_ws_id == 1
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert exit_code == 0
    tx = db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").one()
    assert tx.workspace_id == expected_ws_id


# ══════════════════════════════════════════════════════════════════════════
# Manifest loading / schema validation
# ══════════════════════════════════════════════════════════════════════════

def test_malformed_json_fails_closed(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{not valid json", encoding="utf-8")
    exit_code = _run(db, _args(manifest=str(bad_path), portfolio=pid))
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0


def test_schema_invalid_manifest_fails_closed(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    incomplete_path = tmp_path / "incomplete.json"
    incomplete_path.write_text(json.dumps({"schema_version": 1}), encoding="utf-8")
    exit_code = _run(db, _args(manifest=str(incomplete_path), portfolio=pid))
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0


# ══════════════════════════════════════════════════════════════════════════
# No-write default / --dry-run (WP7-A1, A2, A8)
# ══════════════════════════════════════════════════════════════════════════

def test_no_flags_default_performs_no_write(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid))
    assert exit_code == 0
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0
    assert db.query(PortfolioItem).filter_by(symbol="BANPUU.BK").count() == 0


def test_explicit_dry_run_performs_no_write(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid, dry_run=True))
    assert exit_code == 0
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0


# ══════════════════════════════════════════════════════════════════════════
# Preflight chain — independent fail-closed proof (WP7-A3, A9)
# ══════════════════════════════════════════════════════════════════════════

def test_registry_preconditions_failure_blocks_commit(tmp_path):
    """Predecessor/successor asset_id pointing at a nonexistent asset must
    fail the registry-preconditions preflight and refuse --commit."""
    db, pid, manifest, pred, succ = _seed_full_scenario(
        tmp_path, manifest_overrides={"successor.asset_id": 999999},
    )
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0


def test_quote_gate_manifest_mismatch_blocks_commit(tmp_path):
    """successor.provider_symbol disagreeing with quote_binding.successor_provider_symbol
    must fail the manifest-only quote-gate preflight."""
    db, pid, manifest, pred, succ = _seed_full_scenario(
        tmp_path, manifest_overrides={"successor.provider_symbol": "WRONG.BK"},
    )
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0


def test_mechanical_continuity_not_evaluable_blocks_commit(tmp_path):
    """BANPU-WP7 Independent Implementation Review §9/§16 correction: this
    test previously claimed to prove MECHANICAL_CONTINUITY_FAILURE (an
    unannotated above-tolerance gap). That branch is schema-unreachable —
    parse_position_conversion_payload requires a non-empty
    suspension_gap_annotation on every valid payload, so an above-tolerance
    gap always classifies ANNOTATED_BOUNDARY_DISCONTINUITY, not
    MECHANICAL_CONTINUITY_FAILURE, and WPP §7.2 step 3 treats
    ANNOTATED_BOUNDARY_DISCONTINUITY as non-blocking (PASS or
    ANNOTATED_BOUNDARY_DISCONTINUITY both proceed). This test is renamed to
    accurately state what it actually proves: a negative tolerance drives
    _evaluate_mechanical_continuity() to NOT_EVALUABLE, the one continuity
    outcome a schema-valid manifest can still reach to fail this preflight.
    No fabricated schema-invalid manifest is used to force the unreachable
    branch, and the underlying implementation behavior is unchanged."""
    db, pid, manifest, pred, succ = _seed_full_scenario(
        tmp_path,
        manifest_overrides={"boundary_evidence.mechanical_nav_tolerance_pct": "-0.50"},
    )
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0


def test_mechanical_continuity_annotated_discontinuity_does_not_block(tmp_path):
    """An above-tolerance but annotated gap is ANNOTATED_BOUNDARY_DISCONTINUITY,
    which WPP §7.2 step 3 treats as passing (non-blocking) — proves the
    preflight distinguishes it from MECHANICAL_CONTINUITY_FAILURE/NOT_EVALUABLE."""
    db, pid, manifest, pred, succ = _seed_full_scenario(
        tmp_path,
        manifest_overrides={"boundary_evidence.successor_reference_price": "1.00"},
    )
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid))  # dry-run
    assert exit_code == 0


def test_rebuild_boundary_inconsistency_blocks_commit(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(
        tmp_path,
        manifest_overrides={"dates.successor_quote_epoch_start_date": "2026-03-05"},
    )
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").count() == 0


def test_commit_refused_when_any_preflight_fails_no_registry_mutation(tmp_path):
    """A failed preflight must block --commit unconditionally — including
    never calling prepare_position_conversion_registry() (WP7-A18 boundary)."""
    db, pid, manifest, pred, succ = _seed_full_scenario(
        tmp_path, manifest_overrides={"successor.asset_id": 999999},
    )
    pred_id = pred.id
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert exit_code == 1
    # Predecessor must remain ACTIVE (never transitioned to MERGED)
    refreshed_pred = registry.get_asset(db, pred_id)
    assert refreshed_pred.status == "ACTIVE"


# ══════════════════════════════════════════════════════════════════════════
# --commit golden path, idempotency, conflict (WP7-A4, A5)
# ══════════════════════════════════════════════════════════════════════════

def test_commit_applies_conversion_and_prepares_registry(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    pred_id, succ_id = pred.id, succ.id
    exit_code = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert exit_code == 0

    tx = db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").one()
    assert tx.portfolio_id == pid

    refreshed_pred = registry.get_asset(db, pred_id)
    assert refreshed_pred.status == "MERGED"

    relationships = registry.get_relationships(db, pred_id)
    merged_into = [r for r in relationships if r.from_asset_id == pred_id and r.relationship_type == "MERGED_INTO"]
    assert len(merged_into) == 1
    assert merged_into[0].to_asset_id == succ_id

    # predecessor holding removed, successor holding created
    assert db.query(PortfolioItem).filter_by(portfolio_id=pid, symbol="BANPU.BK").count() == 0
    successor_item = db.query(PortfolioItem).filter_by(portfolio_id=pid, symbol="BANPUU.BK").one()
    assert float(successor_item.shares) == pytest.approx(2562.214)


def test_commit_retry_same_manifest_is_already_applied_noop(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    first = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert first == 0

    tx_count_after_first = db.query(Transaction).count()

    second = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert second == 0
    assert db.query(Transaction).count() == tx_count_after_first  # no-op, no duplicate row


def test_commit_conflicting_manifest_fails_closed(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    pred_id, succ_id = pred.id, succ.id
    first = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    assert first == 0
    tx_count_after_first = db.query(Transaction).count()

    conflicting_payload = _manifest_dict(
        predecessor_asset_id=pred_id, successor_asset_id=succ_id,
        **{"successor.shares_received": "1.000", "successor.shares_entitled": "1.000"},
    )
    conflicting_manifest = _write_manifest(tmp_path, conflicting_payload, name="conflict.json")

    exit_code = _run(db, _args(manifest=conflicting_manifest, portfolio=pid, commit=True))
    assert exit_code == 1
    assert db.query(Transaction).count() == tx_count_after_first


# ══════════════════════════════════════════════════════════════════════════
# BANPU-WP7 Bounded Implementation Correction (WP7-IIR-B1)
#
# Corrects _preflight_replay_mode_sanity() so that (1) either replay mode's
# own reported failure or an unexpected exception fails closed immediately,
# and (2) a genuine dual-success comparison covers cash, holdings, basis, and
# canonical reconstructed realized P&L — not merely cash and holdings count.
# ══════════════════════════════════════════════════════════════════════════

def _fake_portfolio(*, id: int = 1, workspace_id: int = 1, replay_asset_id_native: bool = False):
    return SimpleNamespace(id=id, workspace_id=workspace_id, replay_asset_id_native=replay_asset_id_native)


def _result_with_holding(
    symbol: str, shares: float, avg_cost: float, *,
    ordinary_basis: Decimal = Decimal("1000.00"), cash: float = 0.0,
    realized_pnl: float | None = 0.0, success: bool = True,
) -> RebuildResult:
    """A synthetic RebuildResult whose reconciliation_report matches the
    exact per-field shape _reconcile_portfolio_items emits for an ordinary
    (non-conversion-successor) held symbol — used to exercise
    _preflight_replay_mode_sanity's comparison logic at the same
    rebuild_portfolio dependency boundary the review's §11 permits mocking,
    without needing a live DR/asset-ID-merge scenario to force a real
    divergence."""
    rows = [
        ReconciliationRow(entity_type="portfolio_item", identifier=symbol, field="shares",
                           current_value=None, reconstructed_value=shares, status=ReconciliationStatus.DIFFERENT),
        ReconciliationRow(entity_type="portfolio_item", identifier=symbol, field="avg_cost",
                           current_value=None, reconstructed_value=avg_cost, status=ReconciliationStatus.DIFFERENT),
    ]
    return RebuildResult(
        portfolio_id=1, portfolio_name="Test", success=success,
        reconstructed_cash=cash, reconstructed_realized_pnl=realized_pnl,
        reconstructed_holding_basis={symbol: ordinary_basis}, reconstructed_holdings_count=1,
        reconciliation_report=rows,
    )


def _result_with_conversion_successor_holding(
    symbol: str, shares: float, avg_cost: float, basis: float, *,
    ordinary_basis: Decimal = Decimal("1000.00"), cash: float = 0.0,
    realized_pnl: float | None = 0.0,
) -> RebuildResult:
    """Mirrors the extended five-field reconciliation shape
    _reconcile_portfolio_items emits for a conversion-successor symbol,
    where "basis" is its own explicit field rather than derived — used to
    prove a basis-only divergence (shares and avg_cost both matching) is
    still independently detected."""
    rows = [
        ReconciliationRow(entity_type="portfolio_item", identifier=symbol, field="shares",
                           current_value=shares, reconstructed_value=shares, status=ReconciliationStatus.MATCH),
        ReconciliationRow(entity_type="portfolio_item", identifier=symbol, field="avg_cost",
                           current_value=avg_cost, reconstructed_value=avg_cost, status=ReconciliationStatus.MATCH),
        ReconciliationRow(entity_type="portfolio_item", identifier=symbol, field="basis",
                           current_value=basis, reconstructed_value=basis, status=ReconciliationStatus.MATCH),
    ]
    return RebuildResult(
        portfolio_id=1, portfolio_name="Test", success=True,
        reconstructed_cash=cash, reconstructed_realized_pnl=realized_pnl,
        reconstructed_holding_basis={symbol: ordinary_basis}, reconstructed_holdings_count=1,
        reconciliation_report=rows,
    )


def _empty_result(*, cash: float = 0.0, realized_pnl: float | None = 0.0, success: bool = True, error: str | None = None) -> RebuildResult:
    return RebuildResult(
        portfolio_id=1, portfolio_name="Test", success=success, error=error,
        reconstructed_cash=cash, reconstructed_realized_pnl=realized_pnl, reconstructed_holdings_count=0, reconciliation_report=[],
    )


def _run_replay_check(db, portfolio, *, side_effect):
    with patch("manage.rebuild_portfolio", new=AsyncMock(side_effect=side_effect)):
        return asyncio.run(_preflight_replay_mode_sanity(db, portfolio, label="test"))


# ── Pure-function unit coverage: extraction and diffing (§12) ──────────────

def test_extract_reconstructed_holdings_from_individual_field_rows():
    result = _result_with_holding("BANPUU.BK", shares=100.0, avg_cost=10.0)
    holdings = _extract_reconstructed_holdings(result)
    assert holdings["BANPUU.BK"]["shares"] == 100.0
    assert holdings["BANPUU.BK"]["avg_cost"] == 10.0
    assert "basis" not in holdings["BANPUU.BK"]


def test_extract_reconstructed_holdings_from_whole_row_missing_dict():
    rows = [ReconciliationRow(
        entity_type="portfolio_item", identifier="BANPUU.BK", field="*",
        current_value=None, reconstructed_value={"shares": 50.0, "avg_cost": 20.0},
        status=ReconciliationStatus.MISSING,
    )]
    result = RebuildResult(portfolio_id=1, portfolio_name="T", success=True,
                            reconstructed_cash=0.0, reconstructed_holdings_count=1,
                            reconciliation_report=rows)
    holdings = _extract_reconstructed_holdings(result)
    assert holdings["BANPUU.BK"] == {"shares": 50.0, "avg_cost": 20.0}


def test_diff_reconstructed_holdings_detects_shares_mismatch():
    diffs = _diff_reconstructed_holdings(
        {"BANPUU.BK": {"shares": 100.0, "avg_cost": 10.0, "basis": 1000.0}},
        {"BANPUU.BK": {"shares": 105.0, "avg_cost": 10.0, "basis": 1050.0}},
    )
    assert any("field=shares" in d for d in diffs)


def test_diff_reconstructed_holdings_detects_avg_cost_mismatch():
    diffs = _diff_reconstructed_holdings(
        {"BANPUU.BK": {"shares": 100.0, "avg_cost": 10.0, "basis": 1000.0}},
        {"BANPUU.BK": {"shares": 100.0, "avg_cost": 10.50, "basis": 1050.0}},
    )
    assert any("field=avg_cost" in d for d in diffs)


def test_diff_reconstructed_holdings_detects_basis_only_mismatch():
    """Shares and avg_cost agree; only basis differs — must still be caught
    independently, proving basis is not silently implied by the other two."""
    diffs = _diff_reconstructed_holdings(
        {"BANPUU.BK": {"shares": 100.0, "avg_cost": 10.0, "basis": 1000.0}},
        {"BANPUU.BK": {"shares": 100.0, "avg_cost": 10.0, "basis": 950.0}},
    )
    assert any("field=basis" in d for d in diffs)


def test_diff_reconstructed_holdings_detects_symbol_only_in_one_mode():
    diffs = _diff_reconstructed_holdings(
        {"BANPUU.BK": {"shares": 100.0, "avg_cost": 10.0, "basis": 1000.0}},
        {},
    )
    assert any("present under only one replay mode" in d for d in diffs)


def test_diff_reconstructed_holdings_no_diff_when_equal():
    diffs = _diff_reconstructed_holdings(
        {"BANPUU.BK": {"shares": 100.0, "avg_cost": 10.0, "basis": 1000.0}},
        {"BANPUU.BK": {"shares": 100.0, "avg_cost": 10.0, "basis": 1000.0}},
    )
    assert diffs == []


# ── Replay failure must fail closed (§5, §11) ───────────────────────────────

def test_replay_legacy_mode_reported_failure_blocks_preflight():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(),
        side_effect=[_empty_result(success=False, error="INJECTED_LEGACY_FAILURE"), _empty_result()],
    )
    assert check.passed is False
    assert "legacy-mode replay" in check.detail
    assert "REPLAY_FAILED" in check.detail
    assert "INJECTED_LEGACY_FAILURE" not in check.detail


def test_replay_native_mode_reported_failure_blocks_preflight():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(),
        side_effect=[_empty_result(), _empty_result(success=False, error="INJECTED_NATIVE_FAILURE")],
    )
    assert check.passed is False
    assert "native-mode replay" in check.detail
    assert "REPLAY_FAILED" in check.detail
    assert "INJECTED_NATIVE_FAILURE" not in check.detail


def test_replay_legacy_mode_error_bearing_success_blocks_preflight_and_rolls_back():
    db = make_session()
    portfolio = _fake_portfolio()
    original = portfolio.replay_asset_id_native
    sentinel = "TOKEN_SENTINEL"
    with patch.object(db, "rollback", wraps=db.rollback) as rollback:
        check = _run_replay_check(
            db, portfolio,
            side_effect=[_empty_result(success=True, error=sentinel), _empty_result()],
        )
    assert check.passed is False
    assert "legacy-mode replay REPLAY_FAILED" in check.detail
    assert sentinel not in check.detail
    assert portfolio.replay_asset_id_native == original
    assert rollback.call_count == 1


def test_replay_native_mode_error_bearing_success_blocks_preflight_and_rolls_back():
    db = make_session()
    portfolio = _fake_portfolio()
    original = portfolio.replay_asset_id_native
    sentinel = "TOKEN_SENTINEL"
    with patch.object(db, "rollback", wraps=db.rollback) as rollback:
        check = _run_replay_check(
            db, portfolio,
            side_effect=[_empty_result(), _empty_result(success=True, error=sentinel)],
        )
    assert check.passed is False
    assert "native-mode replay REPLAY_FAILED" in check.detail
    assert sentinel not in check.detail
    assert portfolio.replay_asset_id_native == original
    assert rollback.call_count == 1


@pytest.mark.parametrize("error", [None, ""])
def test_replay_empty_canonical_error_is_accepted_when_all_evidence_is_complete(error):
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(),
        side_effect=[_empty_result(error=error), _empty_result(error=error)],
    )
    assert check.passed is True


def test_replay_whitespace_canonical_error_blocks_preflight():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(),
        side_effect=[_empty_result(error=" "), _empty_result()],
    )
    assert check.passed is False
    assert "REPLAY_FAILED" in check.detail


def test_replay_unexpected_exception_blocks_preflight_both_modes():
    db = make_session()

    async def boom(*args, **kwargs):
        raise RuntimeError("INJECTED_UNEXPECTED_ERROR")

    check = _run_replay_check(db, _fake_portfolio(), side_effect=boom)
    assert check.passed is False
    assert "REPLAY_EXCEPTION" in check.detail
    assert "INJECTED_UNEXPECTED_ERROR" not in check.detail


def test_replay_failure_never_accepted_as_equivalence_despite_matching_defaults():
    """A failed mode's result carries only default/empty comparison values
    (cash=0.0, holdings_count=0) — proves the fail-closed branch fires from
    `success is False` alone, never falling through to a spurious "0 == 0"
    match against the other, genuinely-empty mode."""
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(),
        side_effect=[_empty_result(success=False, error="INJECTED_FAILURE"), _empty_result(success=True)],
    )
    assert check.passed is False


# ── Full frozen result-set comparison (§6, §12) ─────────────────────────────

def test_replay_mismatch_detected_cash_only():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(),
        side_effect=[_empty_result(cash=100.0), _empty_result(cash=200.0)],
    )
    assert check.passed is False
    assert "cash:" in check.detail


def test_replay_missing_cash_vs_zero_blocks_preflight():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(), side_effect=[_empty_result(cash=None), _empty_result(cash=0.0)],
    )
    assert check.passed is False
    assert "cash evidence unavailable" in check.detail


def test_replay_missing_cash_on_both_modes_blocks_preflight():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(), side_effect=[_empty_result(cash=None), _empty_result(cash=None)],
    )
    assert check.passed is False
    assert "cash evidence unavailable" in check.detail


def test_replay_zero_cash_agrees():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(), side_effect=[_empty_result(cash=0.0), _empty_result(cash=0.0)],
    )
    assert check.passed is True


def test_replay_equal_nonzero_cash_agrees():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(), side_effect=[_empty_result(cash=1.001), _empty_result(cash=1.001)],
    )
    assert check.passed is True


def test_replay_subcent_cash_mismatch_blocks_preflight():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(), side_effect=[_empty_result(cash=1.001), _empty_result(cash=1.002)],
    )
    assert check.passed is False
    assert "cash:" in check.detail


def test_replay_mismatch_detected_holdings_count_only():
    db = make_session()
    legacy = _result_with_holding("BANPUU.BK", 100.0, 10.0)
    native = _empty_result()
    native.reconstructed_holdings_count = 0
    legacy.reconstructed_holdings_count = 1
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is False
    assert "holdings_count:" in check.detail


def test_replay_mismatch_detected_holdings_basis_via_conversion_successor_shape():
    db = make_session()
    legacy = _result_with_conversion_successor_holding("BANPUU.BK", 100.0, 10.0, 1000.0)
    native = _result_with_conversion_successor_holding("BANPUU.BK", 100.0, 10.0, 950.0)
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is False
    assert "field=basis" in check.detail


def test_replay_no_mismatch_full_agreement_passes():
    db = make_session()
    legacy = _result_with_holding("BANPUU.BK", 100.0, 10.0, cash=500.0)
    native = _result_with_holding("BANPUU.BK", 100.0, 10.0, cash=500.0)
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is True
    assert "realized P&L agree" in check.detail


def test_replay_equal_exact_ordinary_basis_map_passes():
    db = make_session()
    exact_basis = Decimal("100.00004040000016")
    legacy = _result_with_holding("BANPUU.BK", 100.0, 10.0, ordinary_basis=exact_basis)
    native = _result_with_holding("BANPUU.BK", 100.0, 10.0, ordinary_basis=exact_basis)
    assert _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native]).passed is True


def test_replay_ordinary_basis_only_mismatch_blocks_preflight_without_local_formula():
    """Shares/avg_cost remain identical, so only the predecessor map can catch it."""
    db = make_session()
    legacy = _result_with_holding(
        "BANPUU.BK", 100.0, 10.0, ordinary_basis=Decimal("100.00004040000016"),
    )
    native = _result_with_holding(
        "BANPUU.BK", 100.0, 10.0, ordinary_basis=Decimal("100.00004040000017"),
    )
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is False
    assert "ordinary basis symbol=BANPUU.BK" in check.detail


def test_replay_high_precision_ordinary_basis_mismatch_blocks_preflight():
    db = make_session()
    legacy = _result_with_holding(
        "BANPUU.BK", 100.0, 10.0, ordinary_basis=Decimal("1.00000000000001"),
    )
    native = _result_with_holding(
        "BANPUU.BK", 100.0, 10.0, ordinary_basis=Decimal("1.00000000000002"),
    )
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is False
    assert "ordinary basis symbol=BANPUU.BK" in check.detail


def test_replay_missing_ordinary_basis_entry_blocks_preflight():
    db = make_session()
    legacy = _result_with_holding("BANPUU.BK", 100.0, 10.0)
    native = _result_with_holding("BANPUU.BK", 100.0, 10.0)
    native.reconstructed_holding_basis = {}
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is False
    assert "native ordinary basis missing: symbol=BANPUU.BK" in check.detail


def test_replay_non_decimal_ordinary_basis_value_blocks_preflight():
    db = make_session()
    legacy = _result_with_holding("BANPUU.BK", 100.0, 10.0)
    native = _result_with_holding("BANPUU.BK", 100.0, 10.0)
    native.reconstructed_holding_basis["BANPUU.BK"] = 1000.0
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is False
    assert "native ordinary basis value invalid: symbol=BANPUU.BK" in check.detail


def test_replay_unexpected_ordinary_basis_entry_blocks_preflight():
    db = make_session()
    legacy = _result_with_holding("BANPUU.BK", 100.0, 10.0)
    native = _result_with_holding("BANPUU.BK", 100.0, 10.0)
    native.reconstructed_holding_basis["UNEXPECTED.BK"] = Decimal("1.00")
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is False
    assert "native ordinary basis unexpected: symbol=UNEXPECTED.BK" in check.detail


def test_replay_empty_portfolio_with_empty_ordinary_basis_map_passes():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(), side_effect=[_empty_result(), _empty_result()],
    )
    assert check.passed is True


def test_replay_realized_pnl_equal_passes():
    db = make_session()
    legacy = _result_with_holding("BANPUU.BK", 100.0, 10.0, cash=500.0, realized_pnl=125.50)
    native = _result_with_holding("BANPUU.BK", 100.0, 10.0, cash=500.0, realized_pnl=125.50)
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is True


def test_replay_realized_pnl_mismatch_blocks_preflight():
    db = make_session()
    legacy = _result_with_holding("BANPUU.BK", 100.0, 10.0, realized_pnl=125.50)
    native = _result_with_holding("BANPUU.BK", 100.0, 10.0, realized_pnl=124.50)
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is False
    assert "realized P&L:" in check.detail


def test_replay_missing_realized_pnl_evidence_blocks_preflight():
    db = make_session()
    legacy = _empty_result(realized_pnl=None)
    native = _empty_result(realized_pnl=0.0)
    check = _run_replay_check(db, _fake_portfolio(), side_effect=[legacy, native])
    assert check.passed is False
    assert "realized P&L evidence unavailable" in check.detail


def test_replay_zero_realized_pnl_agrees():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(), side_effect=[_empty_result(realized_pnl=0.0), _empty_result(realized_pnl=0.0)],
    )
    assert check.passed is True


def test_replay_zero_vs_nonzero_realized_pnl_blocks_preflight():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(), side_effect=[_empty_result(realized_pnl=0.0), _empty_result(realized_pnl=0.01)],
    )
    assert check.passed is False
    assert "realized P&L:" in check.detail


def test_replay_subcent_realized_pnl_mismatch_blocks_preflight():
    db = make_session()
    check = _run_replay_check(
        db, _fake_portfolio(), side_effect=[_empty_result(realized_pnl=1.001), _empty_result(realized_pnl=1.002)],
    )
    assert check.passed is False
    assert "realized P&L:" in check.detail


# ── Replay-toggle no-lasting-mutation, corrected coverage (§10) ─────────────

def test_replay_toggle_restored_after_successful_dual_replay(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    portfolio = db.query(Portfolio).filter_by(id=pid).one()
    original = portfolio.replay_asset_id_native
    asyncio.run(_preflight_replay_mode_sanity(db, portfolio, label="test"))
    assert portfolio.replay_asset_id_native == original
    refreshed = db.query(Portfolio).filter_by(id=pid).one()
    assert refreshed.replay_asset_id_native == original
    # Session must remain usable for whatever the next required boundary is.
    db.query(Portfolio).filter_by(id=pid).first()


def test_replay_toggle_restored_after_one_replay_failure(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    portfolio = db.query(Portfolio).filter_by(id=pid).one()
    original = portfolio.replay_asset_id_native
    with patch("manage.rebuild_portfolio", new=AsyncMock(side_effect=[
        _empty_result(success=False, error="INJECTED"), _empty_result(),
    ])):
        check = asyncio.run(_preflight_replay_mode_sanity(db, portfolio, label="test"))
    assert check.passed is False
    assert portfolio.replay_asset_id_native == original
    db.query(Portfolio).filter_by(id=pid).first()


def test_replay_toggle_restored_after_mismatch(tmp_path):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    portfolio = db.query(Portfolio).filter_by(id=pid).one()
    original = portfolio.replay_asset_id_native
    legacy = _result_with_holding("BANPUU.BK", 100.0, 10.0)
    native = _result_with_holding("BANPUU.BK", 105.0, 10.0)
    with patch("manage.rebuild_portfolio", new=AsyncMock(side_effect=[legacy, native])):
        check = asyncio.run(_preflight_replay_mode_sanity(db, portfolio, label="test"))
    assert check.passed is False
    assert portfolio.replay_asset_id_native == original
    db.query(Portfolio).filter_by(id=pid).first()


# ── Induced post-commit mismatch — T8 evidence (§13, WP7-A17) ──────────────

def test_commit_post_commit_realized_pnl_mismatch_reports_critical_without_misreporting_not_applied(tmp_path, capsys):
    """Reaches the successful commit/application path, then forces the
    fourth rebuild_portfolio call (post-commit native-mode replay) to
    diverge from the real reconstructed value — proving mandatory
    post-commit verification independently detects a mismatch on the
    now-materialized conversion, reports CRITICAL, exits non-zero, invents
    no automated rollback, and never claims the conversion was "not
    applied" even though it was, in fact, persisted (WP7 Bounded
    Correction §9, addressing the failed review's A17 finding)."""
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    call_count = {"n": 0}

    async def fake_rebuild(*args, **kwargs):
        call_count["n"] += 1
        result = await _real_rebuild_portfolio(*args, **kwargs)
        if call_count["n"] == 4:  # post-commit native-mode replay
            result.reconstructed_realized_pnl = (result.reconstructed_realized_pnl or 0.0) + 999.0
        return result

    with _patch_session(db), patch("manage.rebuild_portfolio", side_effect=fake_rebuild):
        exit_code = asyncio.run(
            _cmd_apply_position_conversion(_args(manifest=manifest, portfolio=pid, commit=True))
        )

    assert call_count["n"] == 4
    assert exit_code == 1

    # The conversion WAS persisted before post-commit verification ran.
    tx = db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").one()
    assert tx.portfolio_id == pid

    captured = capsys.readouterr()
    assert "Status: applied" in captured.out
    assert "CRITICAL: post-commit both-replay-mode verification mismatch" in captured.err
    assert "not applied" not in captured.out.lower()
    assert "not applied" not in captured.err.lower()


def test_commit_post_commit_ordinary_basis_only_mismatch_reports_critical(tmp_path, capsys):
    """The applied conversion remains truthful while exact basis parity fails."""
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    call_count = {"n": 0}

    async def fake_rebuild(*args, **kwargs):
        call_count["n"] += 1
        result = await _real_rebuild_portfolio(*args, **kwargs)
        if call_count["n"] == 4:  # post-commit native-mode replay
            symbol = next(iter(result.reconstructed_holding_basis))
            result.reconstructed_holding_basis[symbol] += Decimal("0.00000000000001")
        return result

    with _patch_session(db), patch("manage.rebuild_portfolio", side_effect=fake_rebuild):
        exit_code = asyncio.run(
            _cmd_apply_position_conversion(_args(manifest=manifest, portfolio=pid, commit=True))
        )

    assert call_count["n"] == 4
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").one().portfolio_id == pid
    captured = capsys.readouterr()
    assert "Status: applied" in captured.out
    assert "ordinary basis symbol=BANPUU.BK" in captured.out
    assert "CRITICAL: post-commit both-replay-mode verification mismatch" in captured.err
    assert "Post-commit operator instructions" not in captured.out
    assert "rollback" not in captured.out.lower()


def test_commit_post_commit_missing_cash_reports_critical_without_misreporting_not_applied(tmp_path, capsys):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    call_count = {"n": 0}

    async def fake_rebuild(*args, **kwargs):
        call_count["n"] += 1
        result = await _real_rebuild_portfolio(*args, **kwargs)
        if call_count["n"] == 4:  # post-commit native-mode replay
            result.reconstructed_cash = None
        return result

    with _patch_session(db), patch("manage.rebuild_portfolio", side_effect=fake_rebuild):
        exit_code = asyncio.run(
            _cmd_apply_position_conversion(_args(manifest=manifest, portfolio=pid, commit=True))
        )

    assert call_count["n"] == 4
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").one().portfolio_id == pid
    captured = capsys.readouterr()
    assert "Status: applied" in captured.out
    assert "cash evidence unavailable" in captured.out
    assert "CRITICAL: post-commit both-replay-mode verification mismatch" in captured.err
    assert "Post-commit operator instructions" not in captured.out


def test_commit_post_commit_error_bearing_success_reports_sanitized_critical_without_instructions(tmp_path, capsys):
    """An applied conversion must still fail closed when a post-commit replay
    reports success together with its populated canonical error surface."""
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    call_count = {"n": 0}
    sentinel = "TOKEN_SENTINEL RAW_PAYLOAD_SENTINEL 0xDEADBEEF"

    async def fake_rebuild(*args, **kwargs):
        call_count["n"] += 1
        result = await _real_rebuild_portfolio(*args, **kwargs)
        if call_count["n"] == 4:  # post-commit native-mode replay
            result.error = sentinel
        return result

    with _patch_session(db), patch("manage.rebuild_portfolio", side_effect=fake_rebuild):
        exit_code = asyncio.run(
            _cmd_apply_position_conversion(_args(manifest=manifest, portfolio=pid, commit=True))
        )

    assert call_count["n"] == 4
    assert exit_code == 1
    assert db.query(Transaction).filter_by(transaction_type="POSITION_CONVERSION").one().portfolio_id == pid
    captured = capsys.readouterr()
    assert "Status: applied" in captured.out
    assert "REPLAY_FAILED" in captured.out
    assert "CRITICAL: post-commit both-replay-mode verification mismatch" in captured.err
    assert sentinel not in captured.out
    assert sentinel not in captured.err
    assert "Post-commit operator instructions" not in captured.out
    assert "rollback" not in captured.out.lower()


def test_replay_errors_are_sanitized_in_operator_output(tmp_path, capsys):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    sentinel = "TOKEN_SENTINEL RAW_PAYLOAD_SENTINEL 0xDEADBEEF"

    async def boom(*args, **kwargs):
        raise RuntimeError(sentinel)

    with _patch_session(db), patch("manage.rebuild_portfolio", side_effect=boom):
        exit_code = asyncio.run(_cmd_apply_position_conversion(_args(manifest=manifest, portfolio=pid)))

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "REPLAY_EXCEPTION" in captured.out
    assert sentinel not in captured.out
    assert sentinel not in captured.err


def test_reported_replay_errors_are_sanitized_in_operator_output(tmp_path, capsys):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    sentinel = "TOKEN_SENTINEL RAW_PAYLOAD_SENTINEL 0xDEADBEEF"

    with _patch_session(db), patch(
        "manage.rebuild_portfolio",
        new=AsyncMock(side_effect=[_empty_result(success=False, error=sentinel), _empty_result()]),
    ):
        exit_code = asyncio.run(_cmd_apply_position_conversion(_args(manifest=manifest, portfolio=pid)))

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "REPLAY_FAILED" in captured.out
    assert sentinel not in captured.out
    assert sentinel not in captured.err


def test_outer_unexpected_error_is_sanitized_in_operator_output(tmp_path, capsys):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    sentinel = "TOKEN_SENTINEL RAW_PAYLOAD_SENTINEL 0xDEADBEEF"

    with _patch_session(db), patch("manage._load_conversion_manifest", side_effect=RuntimeError(sentinel)):
        exit_code = asyncio.run(_cmd_apply_position_conversion(_args(manifest=manifest, portfolio=pid)))

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "APPLY_POSITION_CONVERSION_UNEXPECTED_FAILURE" in captured.err
    assert sentinel not in captured.out
    assert sentinel not in captured.err


# ══════════════════════════════════════════════════════════════════════════
# Deterministic and sanitized reporting — T8 evidence (§14, §15, WP7-A10)
# ══════════════════════════════════════════════════════════════════════════

def test_dry_run_report_is_deterministic(tmp_path, capsys):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    _run(db, _args(manifest=manifest, portfolio=pid))
    first = capsys.readouterr().out
    _run(db, _args(manifest=manifest, portfolio=pid))
    second = capsys.readouterr().out
    assert first == second
    assert "Preflight: PASS" in first


def test_failed_preflight_report_is_deterministic(tmp_path, capsys):
    db, pid, manifest, pred, succ = _seed_full_scenario(
        tmp_path, manifest_overrides={"successor.asset_id": 999999},
    )
    _run(db, _args(manifest=manifest, portfolio=pid))
    first = capsys.readouterr().out
    _run(db, _args(manifest=manifest, portfolio=pid))
    second = capsys.readouterr().out
    assert first == second
    assert "Preflight: FAIL" in first


def test_successful_commit_report_is_deterministic(tmp_path, capsys):
    first_dir, second_dir = tmp_path / "first", tmp_path / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    first_db, first_pid, first_manifest, _, _ = _seed_full_scenario(first_dir)
    first_exit = _run(first_db, _args(manifest=first_manifest, portfolio=first_pid, commit=True))
    first_out = capsys.readouterr().out
    second_db, second_pid, second_manifest, _, _ = _seed_full_scenario(second_dir)
    second_exit = _run(second_db, _args(manifest=second_manifest, portfolio=second_pid, commit=True))
    second_out = capsys.readouterr().out
    assert first_exit == second_exit == 0
    assert first_out == second_out
    assert "Status: applied" in first_out
    assert "successor_symbol: BANPUU.BK" in first_out
    assert "transaction_id:" in first_out


def test_already_applied_retry_report_is_deterministic(tmp_path, capsys):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    capsys.readouterr()
    first_exit = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    first_out = capsys.readouterr().out
    second_exit = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    second_out = capsys.readouterr().out
    assert first_exit == second_exit == 0
    assert first_out == second_out
    assert "Status: already_applied" in first_out


def test_conflict_report_is_deterministic(tmp_path, capsys):
    db, pid, manifest, pred, succ = _seed_full_scenario(tmp_path)
    pred_id, succ_id = pred.id, succ.id  # capture before _run()'s db.close() detaches pred/succ
    _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    capsys.readouterr()
    # A schema-valid change to evidence.captured_at alone changes the
    # payload's fingerprint (transaction_canonicalizer._payload_fingerprint
    # covers the full canonical payload including evidence), so this reaches
    # execute_position_conversion's genuine conflicting-retry (E8-R) path
    # rather than a schema rejection at manifest-load time.
    conflicting_payload = _manifest_dict(
        predecessor_asset_id=pred_id, successor_asset_id=succ_id,
        **{"evidence.captured_at": "2026-03-02T11:00:00+07:00"},
    )
    conflicting_manifest = _write_manifest(tmp_path, conflicting_payload, name="conflict_report.json")
    first_exit = _run(db, _args(manifest=conflicting_manifest, portfolio=pid, commit=True))
    first = capsys.readouterr()
    second_exit = _run(db, _args(manifest=conflicting_manifest, portfolio=pid, commit=True))
    second = capsys.readouterr()
    assert first_exit == second_exit == 1
    assert first.out == second.out
    assert first.err == second.err
    assert "ERROR: POSITION_CONVERSION_FAILED" in first.err


def test_post_commit_anomaly_report_is_deterministic(tmp_path, capsys):
    def run_once(scenario_dir):
        db, pid, manifest, _, _ = _seed_full_scenario(scenario_dir)
        calls = {"n": 0}

        async def fake_rebuild(*args, **kwargs):
            calls["n"] += 1
            result = await _real_rebuild_portfolio(*args, **kwargs)
            if calls["n"] == 4:
                result.reconstructed_realized_pnl = (result.reconstructed_realized_pnl or 0.0) + 999.0
            return result

        with _patch_session(db), patch("manage.rebuild_portfolio", side_effect=fake_rebuild):
            exit_code = asyncio.run(
                _cmd_apply_position_conversion(_args(manifest=manifest, portfolio=pid, commit=True))
            )
        assert calls["n"] == 4
        return exit_code, capsys.readouterr()

    first_dir, second_dir = tmp_path / "first", tmp_path / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    first_exit, first = run_once(first_dir)
    second_exit, second = run_once(second_dir)
    assert first_exit == second_exit == 1
    assert first.out == second.out
    assert first.err == second.err
    assert "Status: applied" in first.out
    assert "CRITICAL: post-commit both-replay-mode verification mismatch" in first.err


def test_report_never_emits_manifest_evidence_sentinel(tmp_path, capsys):
    """Controlled, unmistakably fake sentinel — never a real credential —
    planted in the manifest's evidence block; proves the CLI report never
    echoes it back across both dry-run and a full --commit."""
    sentinel = "FAKE-SENTINEL-DO-NOT-EMIT-6f0c9e2a"
    db, pid, manifest, pred, succ = _seed_full_scenario(
        tmp_path,
        manifest_overrides={
            "evidence.reference": sentinel,
            "evidence.source": f"FAKE-CREDENTIAL-TOKEN-{sentinel}",
        },
    )
    _run(db, _args(manifest=manifest, portfolio=pid))
    dry_run_output = capsys.readouterr()
    assert sentinel not in dry_run_output.out
    assert sentinel not in dry_run_output.err

    exit_code = _run(db, _args(manifest=manifest, portfolio=pid, commit=True))
    commit_output = capsys.readouterr()
    assert exit_code == 0
    assert sentinel not in commit_output.out
    assert sentinel not in commit_output.err
