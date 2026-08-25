"""Tests for Accounting Correctness Milestone 2 — historical regeneration and
replay validation (docs/DECISION_LOG.md, "Historical Regeneration + Replay
Validation Engine").

Milestone 1 fixed the shared replay functions (_resolve_shares_from_weights,
assert_nav_conserved) so *future* rebalances stop leaking cash, but left
already-persisted ShadowPortfolio.paper_cash_balance values and
ShadowPortfolioSnapshot rows untouched. This file covers the regeneration
engine that re-derives those rows through the corrected engine, plus the
reusable replay-determinism helper.

Coverage
--------
verify_deterministic_replay (unit, no DB)
  1. A pure, stable function passes and returns its result.
  2. A function whose output changes between calls raises
     ReplayNonDeterministicError.

regenerate_static_shadow (DB-backed)
  3. Restores the correct paper_cash_balance for a shadow whose cash was
     never computed (simulates a pre-Milestone-1 row: paper_cash_balance=0.0
     despite partial-weight holdings) and rewrites its snapshot history so
     every day conserves NAV.
  4. dry_run=True computes the correct value but leaves the database
     unchanged (rollback, not commit).
  5. Regeneration is idempotent — running it twice produces identical cash
     and an unchanged ShadowPortfolioSnapshot row count (no duplicates).

regenerate_active_model_shadow / _replay_active_model_series (DB-backed)
  6. Replays a full multi-day, multi-rebalance history (95% -> 97% -> full
     liquidation, mirroring Milestone 1's own regression fixture) from a
     shadow whose paper_cash_balance was never tracked, and conserves NAV
     on every regenerated day.
  7. The pure replay component is deterministic under verify_deterministic_replay.
  8. Regeneration is idempotent — a second run produces identical snapshot
     values and does not duplicate rows.
  8b. holdings_json is refreshed on an already-existing row, not left
      stale — Accounting Correctness C5, Issue A regression.

regenerate_portfolio_paper_history (DB-backed, orchestration)
  9. Regenerates both a recommendation-keyed STATIC_FROZEN shadow and the
     ACTIVE_MODEL shadow for the same portfolio, with zero errors and no
     shadow rows created or deleted (identity preserved).

compute_ideal_series (DB-backed) — Ideal Portfolio replay determinism
  10. Two independent calls with identical inputs produce identical series,
      verified via verify_deterministic_replay (this is the "Ideal Portfolio"
      half of Milestone 2's determinism requirement; ACTIVE_MODEL's half is
      covered by test 7 above).
"""
from __future__ import annotations

import json
import sys
import os
from datetime import date, datetime, timedelta
from decimal import Decimal

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.decision_memory.shadow_tracker import (  # noqa: E402
    verify_deterministic_replay,
    ReplayNonDeterministicError,
    regenerate_static_shadow,
    regenerate_active_model_shadow,
    regenerate_portfolio_paper_history,
    _replay_active_model_series,
    _resolve_shares_from_weights,
    _carry_succession_identity,
    _conversion_ratio,
)


# ─── verify_deterministic_replay (unit, no DB) ─────────────────────────────

def test_verify_deterministic_replay_passes_for_stable_function():
    def stable(x):
        return {"a": x * 2, "b": [1.0, 2.0, {"c": x}]}

    result = verify_deterministic_replay(stable, 5)
    assert result["deterministic"] is True
    assert result["result"] == {"a": 10, "b": [1.0, 2.0, {"c": 5}]}


def test_verify_deterministic_replay_raises_on_divergence():
    calls = {"n": 0}

    def unstable():
        calls["n"] += 1
        return {"value": calls["n"]}  # different every call

    with pytest.raises(ReplayNonDeterministicError):
        verify_deterministic_replay(unstable)


def test_verify_deterministic_replay_tolerates_floating_point_noise():
    def almost_stable():
        return {"value": 100.0 + 1e-9}

    result = verify_deterministic_replay(almost_stable, tolerance=1e-6)
    assert result["deterministic"] is True


# ─── DB-backed fixtures (mirrors test_shadow_tracker_cash_accounting.py) ───

@pytest.fixture()
def db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models.database import Base
    import models.asset  # noqa: F401 — registers Asset*/asset_relationships tables

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture()
def ws_portfolio(db):
    from models.database import Workspace, Portfolio

    ws = Workspace(name="Test")
    db.add(ws)
    db.commit()
    db.refresh(ws)

    portfolio = Portfolio(workspace_id=ws.id, name="P1", cash_balance=100_000.0)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return ws, portfolio


def _seed_recommendation(db, ws, portfolio, allocations, total_portfolio_value=1_000_000.0, days_ago=0):
    from models.database import OptimizerHistory, RecommendationSnapshot

    oh = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=portfolio.id, portfolio_name=portfolio.name,
        analyzed_at=datetime.utcnow(), swap_count=0,
        result_json=json.dumps({"target_allocations": allocations, "cash_balance": 0.0}),
    )
    db.add(oh)
    db.commit()
    db.refresh(oh)

    snap = RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=portfolio.id,
        total_portfolio_value=total_portfolio_value,
        projected_allocations_json=json.dumps(allocations),
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def _seed_price_snapshot(db, ws, portfolio, prices: dict, days_ago=0):
    from models.database import PortfolioSnapshot

    holdings = [{"symbol": sym, "current_price": p} for sym, p in prices.items()]
    db.add(PortfolioSnapshot(
        workspace_id=ws.id, portfolio_id=portfolio.id,
        snapshot_date=(date.today() - timedelta(days=days_ago)).isoformat(),
        total_value=1_000_000.0, cash_balance=0.0,
        holdings_json=json.dumps(holdings),
    ))
    db.commit()


_ALLOCS_95PCT = [
    {"symbol": "AAA", "target_weight": 50.0, "action": "BUY"},
    {"symbol": "BBB", "target_weight": 45.0, "action": "BUY"},
]
_ALLOCS_97PCT = [
    {"symbol": "AAA", "target_weight": 50.0, "action": "HOLD"},
    {"symbol": "BBB", "target_weight": 47.0, "action": "BUY"},
]
_ALLOCS_93PCT = [
    {"symbol": "AAA", "target_weight": 50.0, "action": "HOLD"},
    {"symbol": "BBB", "target_weight": 43.0, "action": "SELL"},
]
_ALLOCS_FULL_LIQUIDATION: list[dict] = []


# ─── regenerate_static_shadow ──────────────────────────────────────────────

def _make_pre_fix_static_shadow(db, ws, portfolio, snap):
    """Directly construct a ShadowPortfolio row simulating pre-Milestone-1
    data: real holdings at partial weights, but paper_cash_balance hardcoded
    to 0.0 (the historical bug) instead of the correct residual.
    """
    from models.database import ShadowPortfolio

    prices = {"AAA": 100.0, "BBB": 100.0}
    holdings, _dropped_cash = _resolve_shares_from_weights(_ALLOCS_95PCT, 1_000_000.0, prices)

    shadow = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="STATIC_FROZEN",
        name="Pre-fix recommendation shadow",
        inception_date=date.today().isoformat(), inception_value=1_000_000.0,
        recommendation_snapshot_id=snap.id, execution_decision_id=None,
        inception_holdings_json=json.dumps(holdings),
        paper_cash_balance=0.0,  # the bug: never computed
        is_active=True, created_at=datetime.utcnow(),
    )
    db.add(shadow)
    db.commit()
    db.refresh(shadow)
    return shadow


def test_regenerate_static_shadow_restores_correct_cash(db, ws_portfolio):
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    _seed_price_snapshot(db, ws, portfolio, {"AAA": 100.0, "BBB": 100.0})
    snap = _seed_recommendation(db, ws, portfolio, _ALLOCS_95PCT)
    shadow = _make_pre_fix_static_shadow(db, ws, portfolio, snap)

    assert shadow.paper_cash_balance == 0.0  # pre-fix state confirmed

    result = regenerate_static_shadow(db, shadow.id)
    assert result["status"] == "regenerated"
    assert result["new_cash"] == pytest.approx(50_000.0)

    db.refresh(shadow)
    assert shadow.paper_cash_balance == pytest.approx(50_000.0)

    snaps = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).all()
    assert len(snaps) >= 1
    for s in snaps:
        assert s.total_value == pytest.approx(1_000_000.0, abs=1.0)


def test_regenerate_static_shadow_dry_run_leaves_db_unchanged(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    _seed_price_snapshot(db, ws, portfolio, {"AAA": 100.0, "BBB": 100.0})
    snap = _seed_recommendation(db, ws, portfolio, _ALLOCS_95PCT)
    shadow = _make_pre_fix_static_shadow(db, ws, portfolio, snap)

    result = regenerate_static_shadow(db, shadow.id, dry_run=True)
    assert result["dry_run"] is True
    assert result["new_cash"] == pytest.approx(50_000.0)  # computed correctly...

    db.refresh(shadow)
    assert shadow.paper_cash_balance == 0.0  # ...but never committed


def test_regenerate_static_shadow_is_idempotent(db, ws_portfolio):
    from models.database import ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    _seed_price_snapshot(db, ws, portfolio, {"AAA": 100.0, "BBB": 100.0})
    snap = _seed_recommendation(db, ws, portfolio, _ALLOCS_95PCT)
    shadow = _make_pre_fix_static_shadow(db, ws, portfolio, snap)

    r1 = regenerate_static_shadow(db, shadow.id)
    count1 = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).count()

    r2 = regenerate_static_shadow(db, shadow.id)
    count2 = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).count()

    assert r1["new_cash"] == pytest.approx(r2["new_cash"])
    assert count1 == count2  # no duplicate snapshot rows


# ─── regenerate_active_model_shadow / _replay_active_model_series ─────────

def _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date):
    """Directly construct an ACTIVE_MODEL ShadowPortfolio row with
    inception_date backdated (simulating a shadow created days ago) and
    paper_cash_balance never tracked (the pre-Milestone-1 bug).
    """
    from models.database import ShadowPortfolio

    shadow = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="ACTIVE_MODEL",
        name="Pre-fix active model shadow",
        inception_date=inception_date, inception_value=1_000_000.0,
        recommendation_snapshot_id=seed_snap.id,
        inception_holdings_json=json.dumps([]),
        paper_cash_balance=0.0,  # the bug: never computed
        is_active=True, created_at=datetime.utcnow(),
    )
    db.add(shadow)
    db.commit()
    db.refresh(shadow)
    return shadow


def _seed_three_day_rebalance_history(db, ws, portfolio):
    """Seed 3 days of flat prices + 3 RecommendationSnapshots (95% -> 97% ->
    93%), a multi-rebalance history over consecutive calendar days.

    Uses non-empty allocations at every rebalance point. Full liquidation
    (an empty target_allocations list) is deliberately NOT used here: the
    history-scanning replay this function feeds (_replay_active_model_series,
    mirroring ideal_series.py's pre-existing _snapshots_for_window pattern)
    filters out snapshots with `if not allocs: continue` — an empty list is
    indistinguishable from "no usable data" under that filter, so a literal
    liquidation event is currently unrepresentable via history scanning (see
    test_liquidation_snapshot_is_skipped_not_misapplied below, and the
    Milestone 2 carried-forward design note in docs/DECISION_LOG.md). This
    is a pre-existing characteristic shared with the already-shipped Ideal
    Portfolio replay, not something Milestone 2 introduces or is scoped to
    fix (methodology changes are explicitly out of scope).
    """
    for days_ago in (2, 1, 0):
        _seed_price_snapshot(db, ws, portfolio, {"AAA": 100.0, "BBB": 100.0}, days_ago=days_ago)

    snap1 = _seed_recommendation(db, ws, portfolio, _ALLOCS_95PCT, days_ago=2)
    _seed_recommendation(db, ws, portfolio, _ALLOCS_97PCT, days_ago=1)
    _seed_recommendation(db, ws, portfolio, _ALLOCS_93PCT, days_ago=0)

    inception_date = (date.today() - timedelta(days=2)).isoformat()
    return snap1, inception_date


def test_regenerate_active_model_shadow_replays_multi_day_rebalance_history(db, ws_portfolio):
    from models.database import ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    seed_snap, inception_date = _seed_three_day_rebalance_history(db, ws, portfolio)
    shadow = _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date)

    result = regenerate_active_model_shadow(db, portfolio.id)
    assert result["status"] == "regenerated"
    assert result["rebalances_replayed"] == 2  # snap2 (97%), snap3 (93%)
    assert result["snapshots_written"] == 3    # one row per day: -2, -1, today
    # 93% deployed at the end -> 7% of NAV is cash.
    assert result["final_cash"] == pytest.approx(70_000.0, abs=1.0)

    db.refresh(shadow)
    assert len(json.loads(shadow.inception_holdings_json)) == 2
    assert shadow.paper_cash_balance == pytest.approx(70_000.0, abs=1.0)

    snaps = (
        db.query(ShadowPortfolioSnapshot)
        .filter_by(shadow_portfolio_id=shadow.id)
        .order_by(ShadowPortfolioSnapshot.snapshot_date)
        .all()
    )
    assert len(snaps) == 3
    # NAV conserved on every single regenerated day, across every rebalance —
    # the direct Milestone 2 regression test (no price movement, so every
    # day must equal the original inception NAV exactly).
    for s in snaps:
        assert s.total_value == pytest.approx(1_000_000.0, abs=1.0)


def test_liquidation_snapshot_is_skipped_not_misapplied(db, ws_portfolio):
    """Documents a discovered, pre-existing edge case shared with
    ideal_series.py's identical _snapshots_for_window filter: a literal full
    liquidation (empty target_allocations) is indistinguishable from "no
    usable data" under `if not allocs: continue`, so history-scanning replay
    treats it as though the recommendation never existed rather than as a
    liquidation event. This asserts the SAFE side of that gap — the
    snapshot is silently skipped, not misapplied as a phantom rebalance —
    and is not a Milestone 2 regression (methodology changes are out of
    scope; see docs/DECISION_LOG.md for the carried-forward design note).
    """
    ws, portfolio = ws_portfolio
    for days_ago in (1, 0):
        _seed_price_snapshot(db, ws, portfolio, {"AAA": 100.0, "BBB": 100.0}, days_ago=days_ago)
    seed_snap = _seed_recommendation(db, ws, portfolio, _ALLOCS_95PCT, days_ago=1)
    _seed_recommendation(db, ws, portfolio, _ALLOCS_FULL_LIQUIDATION, days_ago=0)

    inception_date = (date.today() - timedelta(days=1)).isoformat()
    shadow = _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date)

    result = regenerate_active_model_shadow(db, portfolio.id)
    assert result["status"] == "regenerated"
    assert result["rebalances_replayed"] == 0  # the liquidation row was skipped, not applied
    assert result["final_cash"] == pytest.approx(50_000.0, abs=1.0)  # still the 95% seed state


def test_replay_active_model_series_is_deterministic(db, ws_portfolio):
    from models.database import ShadowPortfolio

    ws, portfolio = ws_portfolio
    seed_snap, inception_date = _seed_three_day_rebalance_history(db, ws, portfolio)
    shadow = _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date)

    # Re-fetch fresh so the pure function reads consistent, committed state.
    shadow = db.query(ShadowPortfolio).filter_by(id=shadow.id).first()

    result = verify_deterministic_replay(_replay_active_model_series, db, portfolio.id, shadow)
    assert result["deterministic"] is True
    assert result["result"]["status"] == "ok"
    assert result["result"]["final_cash"] == pytest.approx(70_000.0, abs=1.0)


def test_regenerate_active_model_shadow_is_idempotent(db, ws_portfolio):
    from models.database import ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    seed_snap, inception_date = _seed_three_day_rebalance_history(db, ws, portfolio)
    shadow = _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date)

    r1 = regenerate_active_model_shadow(db, portfolio.id)
    rows1 = {
        s.snapshot_date: s.total_value
        for s in db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).all()
    }

    r2 = regenerate_active_model_shadow(db, portfolio.id)
    rows2 = {
        s.snapshot_date: s.total_value
        for s in db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).all()
    }

    assert r1["snapshots_written"] == r2["snapshots_written"]
    assert set(rows1.keys()) == set(rows2.keys())  # no duplicate/dropped dates
    for d in rows1:
        assert rows1[d] == pytest.approx(rows2[d], abs=1e-6)


def test_regenerate_active_model_shadow_dry_run_leaves_db_unchanged(db, ws_portfolio):
    ws, portfolio = ws_portfolio
    seed_snap, inception_date = _seed_three_day_rebalance_history(db, ws, portfolio)
    shadow = _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date)

    result = regenerate_active_model_shadow(db, portfolio.id, dry_run=True)
    assert result["dry_run"] is True
    assert result["final_cash"] == pytest.approx(70_000.0, abs=1.0)

    db.refresh(shadow)
    assert shadow.paper_cash_balance == 0.0  # never committed
    assert json.loads(shadow.inception_holdings_json) == []  # still the placeholder seeded above


# ─── regenerate_portfolio_paper_history (orchestration) ────────────────────

def test_regenerate_active_model_shadow_refreshes_holdings_json_on_existing_row(db, ws_portfolio):
    """Issue A regression (Accounting Correctness C5): regenerate_active_model_shadow
    previously updated total_value/return_pct_since_inception/daily_return_pct
    on an already-existing ShadowPortfolioSnapshot row but left holdings_json
    untouched — e.g. whatever the live daily-valuation scheduler had written
    before regeneration ran. This simulates exactly that pre-existing row
    (stale holdings, stale total_value) and asserts regeneration overwrites
    holdings_json too, so it describes the same state as the corrected
    total_value rather than a leftover composition from before the fix.
    """
    from models.database import ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    seed_snap, inception_date = _seed_three_day_rebalance_history(db, ws, portfolio)
    shadow = _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date)

    # A pre-existing row at the seed date, as the live scheduler would have
    # written before regeneration — one stale leftover holding, wrong total_value.
    stale_holdings = [{
        "symbol": "AAA", "shares": 1.0, "inception_price": 100.0,
        "price_frozen": False, "current_price": 100.0, "market_value": 100.0,
    }]
    db.add(ShadowPortfolioSnapshot(
        shadow_portfolio_id=shadow.id,
        snapshot_date=inception_date,
        total_value=999.0,
        holdings_json=json.dumps(stale_holdings),
        benchmark_symbol="^GSPC",
        created_at=datetime.utcnow(),
    ))
    db.commit()

    result = regenerate_active_model_shadow(db, portfolio.id)
    assert result["status"] == "regenerated"

    refreshed = (
        db.query(ShadowPortfolioSnapshot)
        .filter_by(shadow_portfolio_id=shadow.id, snapshot_date=inception_date)
        .one()
    )
    assert refreshed.total_value == pytest.approx(1_000_000.0, abs=1.0)

    refreshed_holdings = json.loads(refreshed.holdings_json)
    # No longer the stale single-holding placeholder — matches the 95% seed
    # allocation (AAA + BBB), the same state total_value now reflects.
    assert {h["symbol"] for h in refreshed_holdings} == {"AAA", "BBB"}

    # holdings_json and total_value must describe one consistent state: the
    # equity recorded in holdings_json plus the 5%-cash residual for a
    # 95%-deployed seed reconstructs total_value exactly.
    equity_from_holdings_json = sum(h["market_value"] for h in refreshed_holdings)
    assert equity_from_holdings_json + 50_000.0 == pytest.approx(1_000_000.0, abs=1.0)


def test_regenerate_portfolio_paper_history_regenerates_both_shadow_types(db, ws_portfolio):
    from models.database import ShadowPortfolio

    ws, portfolio = ws_portfolio
    seed_snap, inception_date = _seed_three_day_rebalance_history(db, ws, portfolio)
    _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date)
    _make_pre_fix_static_shadow(db, ws, portfolio, seed_snap)

    before_count = db.query(ShadowPortfolio).filter_by(portfolio_id=portfolio.id).count()

    result = regenerate_portfolio_paper_history(db, portfolio.id, ws.id)

    assert result["errors"] == []
    assert len(result["static_shadows"]) == 1
    assert result["static_shadows"][0]["status"] == "regenerated"
    assert result["active_model"]["status"] == "regenerated"

    after_count = db.query(ShadowPortfolio).filter_by(portfolio_id=portfolio.id).count()
    assert after_count == before_count  # identity preserved — no rows created/deleted


# ─── compute_ideal_series replay determinism (Milestone 2 acceptance) ─────

def test_compute_ideal_series_replay_is_deterministic(db, ws_portfolio):
    from services.evaluation.ideal_series import compute_ideal_series

    ws, portfolio = ws_portfolio
    for days_ago in (2, 1, 0):
        _seed_price_snapshot(db, ws, portfolio, {"AAA": 100.0, "BBB": 100.0}, days_ago=days_ago)
    _seed_recommendation(db, ws, portfolio, _ALLOCS_95PCT, days_ago=2)
    _seed_recommendation(db, ws, portfolio, _ALLOCS_97PCT, days_ago=1)

    result = verify_deterministic_replay(compute_ideal_series, db, portfolio.id, 5)
    assert result["deterministic"] is True
    assert result["result"]["status"] == "ok"


# ─── BANPU-WP6 — succession-aware shadow holdings identity ─────────────────
# WP6-A3 through A8, A13, A14, A15 (BANPU_WP6_WORK_PACKAGE_PLAN.md §10).

def _mint_conversion_pair(db, *, predecessor_symbol="OLDX", successor_symbol="NEWX",
                           effective_date):
    from services import asset_registry as registry
    from services.asset_domain import AssetClaim, AssetType, RelationshipType

    def _claim(symbol):
        return AssetClaim(
            canonical_symbol=symbol, asset_type=AssetType.EQUITY,
            market="TH", exchange="SET", currency="THB",
        )

    predecessor = registry.mint(db, _claim(predecessor_symbol))
    successor = registry.mint(db, _claim(successor_symbol))
    registry.link_relationship(
        db, predecessor.id, successor.id, RelationshipType.MERGED_INTO,
        effective_date=effective_date,
    )
    return predecessor, successor


def _seed_conversion_transaction(db, ws, portfolio, *, predecessor, successor,
                                  ratio: str, transaction_date, valuation_transition_date=None):
    """*valuation_transition_date* (payload field) defaults to
    *transaction_date*'s own calendar date but may be supplied separately —
    the ledger row's own `transaction_date` column and its payload's
    declared transition date are not the same thing at the DB layer (only
    the CHECK constraint on midnight-exact time ties them), so a test
    proving WP6-IIR-B4's schedule-mismatch rejection, or two distinct ledger
    rows that both declare the same transition date (WP6-IIR-B3 ambiguous
    evidence), needs to set them independently."""
    from models.database import Transaction

    vtd = valuation_transition_date or transaction_date.date()
    midnight = datetime.combine(transaction_date.date(), datetime.min.time())
    db.add(Transaction(
        workspace_id=ws.id, portfolio_id=portfolio.id,
        symbol=predecessor.canonical_symbol, transaction_type="POSITION_CONVERSION",
        asset_id=predecessor.id,
        total_amount=0.0, fees=0.0, taxes=0.0, transaction_date=midnight,
        conversion_payload={
            "schema_version": 1,
            "predecessor": {
                "asset_id": predecessor.id, "symbol": predecessor.canonical_symbol,
                "shares_surrendered": "100",
            },
            "successor": {
                "asset_id": successor.id, "symbol": successor.canonical_symbol,
                "provider_symbol": successor.canonical_symbol,
                "shares_entitled": str(round(100 * float(ratio), 6)),
                "shares_received": str(round(100 * float(ratio), 6)),
            },
            "conversion_ratio": ratio,
            "basis": {"before": "1000.00", "allocated_to_cash_in_lieu": "0.00", "carried_to_successor": "1000.00"},
            "cash_in_lieu": None,
            "dates": {
                "legal_effective_date": vtd.isoformat(),
                "valuation_transition_date": vtd.isoformat(),
                "predecessor_last_price_date": (vtd - timedelta(days=1)).isoformat(),
                "successor_quote_epoch_start_date": vtd.isoformat(),
            },
            "quote_binding": {
                "provider": "YAHOO",
                "predecessor_provider_symbol": predecessor.canonical_symbol,
                "successor_provider_symbol": successor.canonical_symbol,
            },
            "boundary_evidence": {
                "predecessor_reference_price": "10.00", "successor_reference_price": "26.16",
                "mechanical_nav_tolerance_pct": "0.50",
                "suspension_gap_annotation": "Official transition boundary",
            },
            "evidence": {
                "reference": "TEST-FIXTURE", "source": "test",
                "captured_at": "2026-08-18T10:00:00+07:00",
            },
        },
    ))
    db.commit()


def _seed_agent_cache_price(db, symbol: str, price: float):
    from models.database import AgentCache

    db.add(AgentCache(symbol=symbol, agent="technical", result_json=json.dumps({"current_price": price})))
    db.commit()


def test_holdings_json_carries_successor_identity_at_boundary(db, ws_portfolio):
    """WP6-A3/A4/A6/A7/A8: value_shadow_portfolio's persisted holdings_json
    carries a non-null asset_id, the successor's symbol on/after the
    boundary, exact fractional shares (no cash-in-lieu rounding), and
    inception_price divided by the ratio (inception value conserved)."""
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    boundary = datetime.utcnow() - timedelta(days=1)  # yesterday: "today" is on/after
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.38242", transaction_date=boundary,
    )
    _seed_agent_cache_price(db, successor.canonical_symbol, 26.16)

    shadow = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="STATIC_FROZEN",
        name="Conversion test shadow",
        inception_date=(boundary - timedelta(days=1)).date().isoformat(), inception_value=1000.0,
        inception_holdings_json=json.dumps([
            {"symbol": predecessor.canonical_symbol, "action": "BUY",
             "shares": 100.0, "inception_price": 10.0, "price_frozen": False},
        ]),
        paper_cash_balance=0.0, is_active=True, created_at=datetime.utcnow(),
    )
    db.add(shadow)
    db.commit()
    db.refresh(shadow)

    from services.decision_memory.shadow_tracker import value_shadow_portfolio
    value_shadow_portfolio(db, shadow.id)

    snap = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).one()
    holdings = json.loads(snap.holdings_json)
    assert len(holdings) == 1
    h = holdings[0]

    assert h["asset_id"] == successor.id                        # WP6-A4
    assert h["symbol"] == successor.canonical_symbol             # WP6-A3
    assert h["shares"] == pytest.approx(38.242)                  # WP6-A6 (exact ratio, fractional)
    assert h["inception_price"] == pytest.approx(10.0 / 0.38242)  # WP6-A8 (inception value conserved)
    # WP6-A7: no cash-in-lieu leg — shares is the exact ratio product, not
    # reduced by any fractional-entitlement cash deduction.
    assert h["shares"] == pytest.approx(100.0 * 0.38242)


def test_predecessor_identity_before_boundary(db, ws_portfolio):
    """WP6-A3: a holding's identity resolves to the predecessor, unchanged,
    when valued before the conversion's effective_date."""
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    boundary = datetime.utcnow() + timedelta(days=30)  # in the future: "today" is before it
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=boundary,
    )
    _seed_agent_cache_price(db, predecessor.canonical_symbol, 10.0)

    shadow = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="STATIC_FROZEN",
        name="Pre-boundary shadow",
        inception_date=date.today().isoformat(), inception_value=1000.0,
        inception_holdings_json=json.dumps([
            {"symbol": predecessor.canonical_symbol, "action": "BUY",
             "shares": 100.0, "inception_price": 10.0, "price_frozen": False},
        ]),
        paper_cash_balance=0.0, is_active=True, created_at=datetime.utcnow(),
    )
    db.add(shadow)
    db.commit()
    db.refresh(shadow)

    from services.decision_memory.shadow_tracker import value_shadow_portfolio
    value_shadow_portfolio(db, shadow.id)

    snap = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).one()
    h = json.loads(snap.holdings_json)[0]
    assert h["asset_id"] == predecessor.id
    assert h["symbol"] == predecessor.canonical_symbol
    assert h["shares"] == pytest.approx(100.0)  # unrescaled — no conversion applies yet


def test_unrelated_symbol_not_remapped(db, ws_portfolio):
    """WP6-A15: a holding whose symbol was never registered as an Asset at
    all is valued exactly as before WP6 — no asset_id key, no remapping."""
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    _seed_agent_cache_price(db, "UNRELATED", 50.0)

    shadow = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="STATIC_FROZEN",
        name="Unrelated symbol shadow",
        inception_date=date.today().isoformat(), inception_value=1000.0,
        inception_holdings_json=json.dumps([
            {"symbol": "UNRELATED", "action": "BUY",
             "shares": 20.0, "inception_price": 50.0, "price_frozen": False},
        ]),
        paper_cash_balance=0.0, is_active=True, created_at=datetime.utcnow(),
    )
    db.add(shadow)
    db.commit()
    db.refresh(shadow)

    from services.decision_memory.shadow_tracker import value_shadow_portfolio
    result = value_shadow_portfolio(db, shadow.id)
    assert result["total_value"] == pytest.approx(1000.0)

    snap = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).one()
    h = json.loads(snap.holdings_json)[0]
    assert h["symbol"] == "UNRELATED"
    assert "asset_id" not in h


def test_regeneration_boundary_skips_pre_boundary_writes_and_protects_existing_rows(db, ws_portfolio):
    """WP6-A13, strengthened per WP6-IIR-B2/B7 (BANPU_WP6_INDEPENDENT_
    IMPLEMENTATION_REVIEW.md §6, §15): regenerate_static_shadow's write loop
    must not touch ANY pre-boundary ShadowPortfolioSnapshot row's persisted
    fields at all — recomputing an equal value is explicitly NOT the frozen
    requirement (WPP §7.2 "writes only rows on or after the boundary").

    A pre-existing pre-boundary row is seeded with deliberately wrong
    sentinel field values before regeneration runs. If regeneration ever
    wrote to it — even to recompute a "correct" value — the sentinel would
    be overwritten and this test would fail. It stays wrong across two
    regeneration runs, proving the row is genuinely never touched, not
    coincidentally recomputed to the same number (the prior test's flaw per
    WP6-IIR-B7: "does not seed a sentinel persisted row").
    """
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    boundary = date.today() - timedelta(days=1)
    boundary_dt = datetime.combine(boundary, datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=boundary_dt,
    )
    _seed_price_snapshot(db, ws, portfolio, {predecessor.canonical_symbol: 10.0}, days_ago=2)
    _seed_price_snapshot(db, ws, portfolio, {successor.canonical_symbol: 20.0}, days_ago=1)
    _seed_price_snapshot(db, ws, portfolio, {successor.canonical_symbol: 22.0}, days_ago=0)

    holdings = [{"symbol": predecessor.canonical_symbol, "target_weight_pct": 100.0,
                 "shares": 100.0, "inception_price": 10.0, "price_frozen": False}]
    shadow = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="STATIC_FROZEN",
        name="Boundary write-protection test shadow",
        inception_date=(date.today() - timedelta(days=2)).isoformat(), inception_value=1_000.0,
        inception_holdings_json=json.dumps(holdings),
        paper_cash_balance=0.0, is_active=True, created_at=datetime.utcnow(),
    )
    db.add(shadow)
    db.commit()
    db.refresh(shadow)

    pre_boundary_date = (date.today() - timedelta(days=2)).isoformat()
    SENTINEL_VALUE = 999_999.0
    SENTINEL_HOLDINGS = json.dumps([{"symbol": "SENTINEL_UNTOUCHED", "shares": 1.0}])
    db.add(ShadowPortfolioSnapshot(
        shadow_portfolio_id=shadow.id, snapshot_date=pre_boundary_date,
        total_value=SENTINEL_VALUE, return_pct_since_inception=SENTINEL_VALUE,
        daily_return_pct=SENTINEL_VALUE, holdings_json=SENTINEL_HOLDINGS,
        benchmark_symbol="SENTINEL", created_at=datetime.utcnow(),
    ))
    db.commit()

    def _sentinel_row():
        return (
            db.query(ShadowPortfolioSnapshot)
            .filter_by(shadow_portfolio_id=shadow.id, snapshot_date=pre_boundary_date)
            .one()
        )

    r1 = regenerate_static_shadow(db, shadow.id)
    assert r1["status"] == "regenerated"
    s = _sentinel_row()
    assert s.total_value == SENTINEL_VALUE
    assert s.return_pct_since_inception == SENTINEL_VALUE
    assert s.daily_return_pct == SENTINEL_VALUE
    assert s.holdings_json == SENTINEL_HOLDINGS
    assert s.benchmark_symbol == "SENTINEL"

    r2 = regenerate_static_shadow(db, shadow.id)
    assert r2["status"] == "regenerated"
    s2 = _sentinel_row()
    assert s2.total_value == SENTINEL_VALUE
    assert s2.holdings_json == SENTINEL_HOLDINGS


def test_regeneration_rerun_converges_full_business_fields_no_orphans(db, ws_portfolio):
    """WP6-A14, strengthened per WP6-IIR-B1/B7: a second regeneration run
    converges every on/after-boundary ShadowPortfolioSnapshot row's full
    business fields (asset_id, symbol, shares, market_value — not merely
    total_value) to the identical first-run result, creates no duplicate or
    orphan rows, and produces the same row count and date set. Also proves
    WP6-C6's "writes only rows on/after the boundary" directly: the
    pre-boundary date never gets a row at all."""
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    boundary = date.today() - timedelta(days=1)
    boundary_dt = datetime.combine(boundary, datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=boundary_dt,
    )
    _seed_price_snapshot(db, ws, portfolio, {predecessor.canonical_symbol: 10.0}, days_ago=2)
    _seed_price_snapshot(db, ws, portfolio, {successor.canonical_symbol: 20.0}, days_ago=1)
    _seed_price_snapshot(db, ws, portfolio, {successor.canonical_symbol: 22.0}, days_ago=0)

    holdings = [{"symbol": predecessor.canonical_symbol, "target_weight_pct": 100.0,
                 "shares": 100.0, "inception_price": 10.0, "price_frozen": False}]
    shadow = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="STATIC_FROZEN",
        name="Rerun convergence test shadow",
        inception_date=(date.today() - timedelta(days=2)).isoformat(), inception_value=1_000.0,
        inception_holdings_json=json.dumps(holdings),
        paper_cash_balance=0.0, is_active=True, created_at=datetime.utcnow(),
    )
    db.add(shadow)
    db.commit()
    db.refresh(shadow)

    def _full_state():
        rows = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).all()
        return {
            s.snapshot_date: {
                "total_value": s.total_value,
                "return_pct_since_inception": s.return_pct_since_inception,
                "daily_return_pct": s.daily_return_pct,
                "holdings": json.loads(s.holdings_json) if s.holdings_json else None,
            }
            for s in rows
        }

    r1 = regenerate_static_shadow(db, shadow.id)
    assert r1["status"] == "regenerated"
    state1 = _full_state()

    boundary_str = boundary.isoformat()
    pre_boundary_date = (date.today() - timedelta(days=2)).isoformat()
    assert pre_boundary_date not in state1              # WP6-C6: never written at all
    assert all(d >= boundary_str for d in state1)
    assert len(state1) == 2                              # boundary day + today only

    for d, row in state1.items():
        assert row["holdings"], f"holdings_json missing for {d}"   # WP6-IIR-B1
        h = row["holdings"][0]
        assert h["asset_id"] == successor.id                       # WP6-A4
        assert h["symbol"] == successor.canonical_symbol            # WP6-A3
        assert h["shares"] == pytest.approx(50.0)                   # WP6-A6: 100 * 0.5
        assert h["market_value"] is not None

    r2 = regenerate_static_shadow(db, shadow.id)
    assert r2["status"] == "regenerated"
    state2 = _full_state()

    assert set(state1.keys()) == set(state2.keys())      # no orphan/duplicate rows
    row_count2 = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).count()
    assert row_count2 == len(state1)

    for d in state1:
        assert state1[d]["total_value"] == pytest.approx(state2[d]["total_value"], abs=1e-9)
        assert state1[d]["holdings"] == state2[d]["holdings"]  # full business fields, byte-identical


# ─── BANPU-WP6 correction — conversion-ratio provenance (WP6-IIR-B3/B4) ────

def test_conversion_ratio_rejects_unrelated_conversion_in_same_portfolio(db, ws_portfolio):
    """A POSITION_CONVERSION transaction for a DIFFERENT predecessor/
    successor pair in the same portfolio must never be selected for this
    relationship (WP6-IIR-B3 'unrelated conversions')."""
    ws, portfolio = ws_portfolio
    boundary_dt = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
    predecessor, successor = _mint_conversion_pair(
        db, predecessor_symbol="OLDX", successor_symbol="NEWX", effective_date=boundary_dt,
    )
    other_pred, other_succ = _mint_conversion_pair(
        db, predecessor_symbol="OTHA", successor_symbol="OTHB", effective_date=boundary_dt,
    )
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=other_pred, successor=other_succ,
        ratio="0.75", transaction_date=boundary_dt,
    )

    ratio = _conversion_ratio(
        db, portfolio_id=portfolio.id,
        predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        effective_date=boundary_dt.date(),
    )
    assert ratio is None


def test_conversion_ratio_rejects_date_mismatch(db, ws_portfolio):
    """WP6-IIR-B4: a transaction whose payload valuation_transition_date
    does not equal the resolved relationship's effective_date must not be
    bound — the two canonical schedules must be proven equal, not assumed
    (closes the ideal_series.py 'common transition schedule' gap, §9)."""
    ws, portfolio = ws_portfolio
    relationship_boundary = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
    transaction_date = datetime.combine(date.today() - timedelta(days=3), datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=relationship_boundary)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=transaction_date,  # deliberately mismatched
    )

    ratio = _conversion_ratio(
        db, portfolio_id=portfolio.id,
        predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        effective_date=relationship_boundary.date(),
    )
    assert ratio is None


def test_conversion_ratio_rejects_ambiguous_duplicate_evidence(db, ws_portfolio):
    """WP6-IIR-B3: two ledger rows (e.g. a duplicate/re-recorded entry) that
    both declare the exact same predecessor/successor/valuation_transition_
    date triple is ambiguous evidence and must not resolve to either ratio
    silently. The two rows use different `transaction_date` COLUMN values
    (the DB's own (portfolio_id, asset_id, transaction_date) uniqueness
    constraint forbids two rows sharing that column) while their PAYLOADS
    both declare the identical `valuation_transition_date` — exactly the
    ambiguity `_conversion_ratio` must detect and reject."""
    ws, portfolio = ws_portfolio
    boundary_dt = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=boundary_dt,
        valuation_transition_date=boundary_dt.date(),
    )
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=boundary_dt + timedelta(days=1),
        valuation_transition_date=boundary_dt.date(),
    )

    ratio = _conversion_ratio(
        db, portfolio_id=portfolio.id,
        predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        effective_date=boundary_dt.date(),
    )
    assert ratio is None


def test_conversion_ratio_rejects_missing_evidence(db, ws_portfolio):
    """WP6-IIR-B3: no POSITION_CONVERSION transaction recorded at all for
    this portfolio resolves to None (unverifiable), not a raise or a guess."""
    ws, portfolio = ws_portfolio
    boundary_dt = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)

    ratio = _conversion_ratio(
        db, portfolio_id=portfolio.id,
        predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        effective_date=boundary_dt.date(),
    )
    assert ratio is None


def test_conversion_ratio_rejects_malformed_payload(db, ws_portfolio):
    """WP6-IIR-B3: a POSITION_CONVERSION row whose payload fails schema
    validation must not be selected."""
    from models.database import Transaction

    ws, portfolio = ws_portfolio
    boundary_dt = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    db.add(Transaction(
        workspace_id=ws.id, portfolio_id=portfolio.id,
        symbol=predecessor.canonical_symbol, transaction_type="POSITION_CONVERSION",
        asset_id=predecessor.id, total_amount=0.0, fees=0.0, taxes=0.0,
        transaction_date=boundary_dt,
        conversion_payload={"schema_version": 1},  # missing required fields
    ))
    db.commit()

    ratio = _conversion_ratio(
        db, portfolio_id=portfolio.id,
        predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        effective_date=boundary_dt.date(),
    )
    assert ratio is None


def test_conversion_ratio_binds_correctly_among_repeated_historical_conversions(db, ws_portfolio):
    """WP6-IIR-B3 'repeated historical conversions': this portfolio's ledger
    carries an older, unrelated-successor conversion recorded for the same
    predecessor symbol string, plus the real one — only the transaction
    matching this exact predecessor/successor/date triple is selected."""
    ws, portfolio = ws_portfolio
    old_boundary = datetime.combine(date.today() - timedelta(days=400), datetime.min.time())
    boundary_dt = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    _, stale_successor = _mint_conversion_pair(
        db, predecessor_symbol="OLDX2", successor_symbol="STALESUCC", effective_date=old_boundary,
    )
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=stale_successor,
        ratio="0.9", transaction_date=old_boundary,
    )
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=boundary_dt,
    )

    ratio = _conversion_ratio(
        db, portfolio_id=portfolio.id,
        predecessor_asset_id=predecessor.id, successor_asset_id=successor.id,
        effective_date=boundary_dt.date(),
    )
    assert ratio == Decimal("0.5")


def test_carry_succession_identity_fails_closed_on_unbound_ratio(db, ws_portfolio, caplog):
    """WP6-IIR-B3: a holding whose registry relationship admits a successor
    as of *as_of_date* but has no unambiguous ledger ratio evidence bound to
    it keeps its predecessor identity — never switches to the successor
    symbol with an unconverted quantity (the exact defect the review found:
    "silently produces successor identity with predecessor quantity"), and
    is logged, never silent (ENGINEERING_PRINCIPLES.md "Failure Handling")."""
    ws, portfolio = ws_portfolio
    boundary_dt = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    # No POSITION_CONVERSION transaction recorded at all — ratio unverifiable.

    holdings = [{"symbol": predecessor.canonical_symbol, "target_weight_pct": 100.0,
                 "shares": 100.0, "inception_price": 10.0, "price_frozen": False}]
    with caplog.at_level("WARNING"):
        out = _carry_succession_identity(db, holdings, date.today().isoformat(), portfolio.id)

    assert len(out) == 1
    assert out[0]["symbol"] == predecessor.canonical_symbol   # NOT switched to successor
    assert out[0]["asset_id"] == predecessor.id
    assert out[0]["shares"] == pytest.approx(100.0)            # unconverted, consistent with identity
    assert any("no unambiguous conversion-ratio evidence" in r.message for r in caplog.records)


def test_carry_succession_identity_converts_when_ratio_unambiguously_bound(db, ws_portfolio):
    """Positive-path companion to the fail-closed test above: when exactly
    one matching conversion transaction exists, the boundary-crossed
    holding correctly switches to the successor identity with the
    ratio-scaled quantity."""
    ws, portfolio = ws_portfolio
    boundary_dt = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=boundary_dt,
    )

    holdings = [{"symbol": predecessor.canonical_symbol, "target_weight_pct": 100.0,
                 "shares": 100.0, "inception_price": 10.0, "price_frozen": False}]
    out = _carry_succession_identity(db, holdings, date.today().isoformat(), portfolio.id)

    assert out[0]["symbol"] == successor.canonical_symbol
    assert out[0]["asset_id"] == successor.id
    assert out[0]["shares"] == pytest.approx(50.0)
    assert out[0]["inception_price"] == pytest.approx(20.0)


# ─── BANPU-WP6 correction — active-model rebalance valuation (WP6-IIR-B5) ──

def test_active_model_rebalance_values_old_holdings_under_current_succession_identity(db, ws_portfolio):
    """WP6-IIR-B5: create_active_model_shadow's rebalance path must value
    old_holdings under THIS date's own succession identity before computing
    running_nav. The prior version valued old_holdings raw (unconverted), so
    a holding that had already crossed its boundary was priced under its
    stale predecessor symbol — for which no cached price exists once the
    quote feed has switched to the successor's own ticker — instead of the
    correct, currently-cached successor price."""
    from services.decision_memory.shadow_tracker import create_active_model_shadow
    from models.database import ShadowPortfolio, RecommendationSnapshot, OptimizerHistory

    ws, portfolio = ws_portfolio
    boundary_dt = datetime.combine(date.today() - timedelta(days=1), datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="1.0", transaction_date=boundary_dt,
    )
    # Only the SUCCESSOR's price is cached — mirrors production once the
    # provider's quote feed has switched to the successor's own ticker.
    _seed_agent_cache_price(db, successor.canonical_symbol, 20.0)

    existing = ShadowPortfolio(
        workspace_id=ws.id, portfolio_id=portfolio.id, shadow_type="ACTIVE_MODEL",
        name="Active model pre-rebalance test",
        inception_date=(date.today() - timedelta(days=5)).isoformat(), inception_value=1000.0,
        inception_holdings_json=json.dumps([
            {"symbol": predecessor.canonical_symbol, "shares": 100.0,
             "inception_price": 10.0, "price_frozen": False},
        ]),
        paper_cash_balance=0.0, is_active=True, created_at=datetime.utcnow(),
    )
    db.add(existing)
    db.commit()
    db.refresh(existing)

    oh = OptimizerHistory(
        workspace_id=ws.id, portfolio_id=portfolio.id, portfolio_name=portfolio.name,
        analyzed_at=datetime.utcnow(), swap_count=0,
        result_json=json.dumps({"target_allocations": [], "cash_balance": 0.0}),
    )
    db.add(oh)
    db.commit()
    db.refresh(oh)
    new_snap = RecommendationSnapshot(
        workspace_id=ws.id, optimizer_history_id=oh.id, portfolio_id=portfolio.id,
        total_portfolio_value=2000.0,
        projected_allocations_json=json.dumps([
            {"symbol": successor.canonical_symbol, "target_weight": 100.0, "action": "BUY"},
        ]),
        created_at=datetime.utcnow(),
    )
    db.add(new_snap)
    db.commit()
    db.refresh(new_snap)

    result = create_active_model_shadow(db, portfolio.id, new_snap.id, ws.id)

    assert result["action"] == "rebalanced"
    # 100 predecessor shares * 1.0 ratio = 100 successor shares @ 20.0 = 2000.0.
    # The pre-fix code could only value the stale predecessor identity, for
    # which no cached price exists here at all (only the successor's price
    # is cached), silently degrading the NAV basis instead of using 2000.0.
    assert result["running_nav"] == pytest.approx(2000.0, abs=1.0)


# ─── BANPU-WP6 second correction — active-model persistence boundary ──────
# (WP6-RR-B1, BANPU_WP6_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW.md §5, §13)

def test_regenerate_active_model_shadow_skips_pre_boundary_writes_and_protects_existing_rows(
    db, ws_portfolio,
):
    """WP6-RR-B1 / active-model WP6-A13: reproduces the re-review's exact
    defect and proves the fix. regenerate_active_model_shadow's persistence
    loop must not touch ANY pre-boundary ShadowPortfolioSnapshot row's
    persisted fields — the same 'writes only rows on or after the boundary'
    rule already proven for regenerate_static_shadow (WP6-IIR-B2), now
    applied to the active-model writer the re-review found unguarded.

    A pre-existing pre-boundary row is seeded with deliberately wrong
    sentinel field values before regeneration runs (the re-review's own
    reproduction technique: 'a deliberately wrong sentinel row on
    2026-08-16... changed the protected sentinel's total_value... and
    holdings_json'). If regeneration ever wrote to it — even to recompute a
    'correct' value — the sentinel would be overwritten and this test would
    fail. It stays wrong across two regeneration runs, proving the row is
    genuinely never touched.
    """
    from models.database import ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    boundary = date.today() - timedelta(days=1)
    boundary_dt = datetime.combine(boundary, datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=boundary_dt,
    )
    _seed_price_snapshot(db, ws, portfolio, {predecessor.canonical_symbol: 10.0}, days_ago=2)
    _seed_price_snapshot(db, ws, portfolio, {successor.canonical_symbol: 20.0}, days_ago=1)
    _seed_price_snapshot(db, ws, portfolio, {successor.canonical_symbol: 22.0}, days_ago=0)

    seed_allocs = [{"symbol": predecessor.canonical_symbol, "target_weight": 100.0, "action": "BUY"}]
    seed_snap = _seed_recommendation(db, ws, portfolio, seed_allocs, total_portfolio_value=1_000_000.0, days_ago=2)
    inception_date = (date.today() - timedelta(days=2)).isoformat()
    shadow = _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date)
    shadow.inception_value = 1_000_000.0
    db.commit()

    pre_boundary_date = inception_date  # days_ago=2, strictly before boundary (days_ago=1)
    SENTINEL_VALUE = 999_999.0
    SENTINEL_HOLDINGS = json.dumps([{"symbol": "SENTINEL_UNTOUCHED", "shares": 1.0}])
    db.add(ShadowPortfolioSnapshot(
        shadow_portfolio_id=shadow.id, snapshot_date=pre_boundary_date,
        total_value=SENTINEL_VALUE, return_pct_since_inception=SENTINEL_VALUE,
        daily_return_pct=SENTINEL_VALUE, holdings_json=SENTINEL_HOLDINGS,
        benchmark_symbol="SENTINEL", created_at=datetime.utcnow(),
    ))
    db.commit()

    def _sentinel_row():
        return (
            db.query(ShadowPortfolioSnapshot)
            .filter_by(shadow_portfolio_id=shadow.id, snapshot_date=pre_boundary_date)
            .one()
        )

    r1 = regenerate_active_model_shadow(db, portfolio.id)
    assert r1["status"] == "regenerated"
    s = _sentinel_row()
    assert s.total_value == SENTINEL_VALUE
    assert s.return_pct_since_inception == SENTINEL_VALUE
    assert s.daily_return_pct == SENTINEL_VALUE
    assert s.holdings_json == SENTINEL_HOLDINGS
    assert s.benchmark_symbol == "SENTINEL"

    r2 = regenerate_active_model_shadow(db, portfolio.id)
    assert r2["status"] == "regenerated"
    s2 = _sentinel_row()
    assert s2.total_value == SENTINEL_VALUE
    assert s2.return_pct_since_inception == SENTINEL_VALUE
    assert s2.daily_return_pct == SENTINEL_VALUE
    assert s2.holdings_json == SENTINEL_HOLDINGS
    assert s2.benchmark_symbol == "SENTINEL"

    # Sanity: the on/after-boundary rows ARE written and DO carry successor
    # identity — the fix protects only pre-boundary rows, not all rows.
    boundary_str = boundary.isoformat()
    written_dates = {
        s3.snapshot_date
        for s3 in db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).all()
        if s3.snapshot_date != pre_boundary_date
    }
    assert written_dates and all(d >= boundary_str for d in written_dates)


def test_regenerate_active_model_shadow_rerun_converges_full_business_fields_no_orphans(
    db, ws_portfolio,
):
    """WP6-RR-B1 / active-model WP6-A14 (Contract-B): strengthens the
    re-review's finding that the prior idempotency test 'compares only
    total_value, date keys, and write count' and 'does not compare active
    persisted holdings fields or independently prove no orphan rows.' Runs
    regenerate_active_model_shadow twice with unchanged canonical inputs and
    proves, from independently reloaded persisted rows: the same row/date
    set, the same persisted holdings identity (asset_id, symbol), the same
    fractional shares (no compounded conversion ratio across the two runs —
    each run re-derives from the original RecommendationSnapshot ledger, not
    from the previous run's own output), the same market values and
    aggregate total_value, no duplicate/orphan rows, and that the protected
    pre-boundary sentinel row remains unchanged after BOTH runs.
    """
    from models.database import ShadowPortfolioSnapshot

    ws, portfolio = ws_portfolio
    boundary = date.today() - timedelta(days=1)
    boundary_dt = datetime.combine(boundary, datetime.min.time())
    predecessor, successor = _mint_conversion_pair(db, effective_date=boundary_dt)
    _seed_conversion_transaction(
        db, ws, portfolio, predecessor=predecessor, successor=successor,
        ratio="0.5", transaction_date=boundary_dt,
    )
    _seed_price_snapshot(db, ws, portfolio, {predecessor.canonical_symbol: 10.0}, days_ago=2)
    _seed_price_snapshot(db, ws, portfolio, {successor.canonical_symbol: 20.0}, days_ago=1)
    _seed_price_snapshot(db, ws, portfolio, {successor.canonical_symbol: 22.0}, days_ago=0)

    seed_allocs = [{"symbol": predecessor.canonical_symbol, "target_weight": 100.0, "action": "BUY"}]
    seed_snap = _seed_recommendation(db, ws, portfolio, seed_allocs, total_portfolio_value=1_000_000.0, days_ago=2)
    inception_date = (date.today() - timedelta(days=2)).isoformat()
    shadow = _make_pre_fix_active_model_shadow(db, ws, portfolio, seed_snap, inception_date)
    shadow.inception_value = 1_000_000.0
    db.commit()

    pre_boundary_date = inception_date
    SENTINEL_VALUE = 999_999.0
    SENTINEL_HOLDINGS = json.dumps([{"symbol": "SENTINEL_UNTOUCHED", "shares": 1.0}])
    db.add(ShadowPortfolioSnapshot(
        shadow_portfolio_id=shadow.id, snapshot_date=pre_boundary_date,
        total_value=SENTINEL_VALUE, return_pct_since_inception=SENTINEL_VALUE,
        daily_return_pct=SENTINEL_VALUE, holdings_json=SENTINEL_HOLDINGS,
        benchmark_symbol="SENTINEL", created_at=datetime.utcnow(),
    ))
    db.commit()

    def _full_state():
        rows = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).all()
        return {
            s.snapshot_date: {
                "total_value": s.total_value,
                "return_pct_since_inception": s.return_pct_since_inception,
                "daily_return_pct": s.daily_return_pct,
                "holdings": json.loads(s.holdings_json) if s.holdings_json else None,
            }
            for s in rows
        }

    r1 = regenerate_active_model_shadow(db, portfolio.id)
    assert r1["status"] == "regenerated"
    state1 = _full_state()

    boundary_str = boundary.isoformat()
    assert pre_boundary_date in state1                    # sentinel row still exists (untouched, not deleted)
    assert state1[pre_boundary_date]["total_value"] == SENTINEL_VALUE
    written_dates_1 = {d for d in state1 if d != pre_boundary_date}
    assert written_dates_1 and all(d >= boundary_str for d in written_dates_1)  # WP6-C6

    for d in written_dates_1:
        row = state1[d]
        assert row["holdings"], f"holdings_json missing for {d}"   # WP6-IIR-B1
        h = row["holdings"][0]
        assert h["asset_id"] == successor.id                        # WP6-A4
        assert h["symbol"] == successor.canonical_symbol             # WP6-A3
        assert h["shares"] == pytest.approx(50_000.0)                # WP6-A6: 100_000 * 0.5, no compounding
        assert h["market_value"] is not None

    r2 = regenerate_active_model_shadow(db, portfolio.id)
    assert r2["status"] == "regenerated"
    state2 = _full_state()

    assert set(state1.keys()) == set(state2.keys())       # no orphan/duplicate rows
    row_count2 = db.query(ShadowPortfolioSnapshot).filter_by(shadow_portfolio_id=shadow.id).count()
    assert row_count2 == len(state1)

    # Protected sentinel row unchanged after the SECOND run too.
    assert state2[pre_boundary_date]["total_value"] == SENTINEL_VALUE
    assert state2[pre_boundary_date]["holdings"] == [{"symbol": "SENTINEL_UNTOUCHED", "shares": 1.0}]

    for d in written_dates_1:
        assert state1[d]["total_value"] == pytest.approx(state2[d]["total_value"], abs=1e-9)
        assert state1[d]["holdings"] == state2[d]["holdings"]  # full business fields, byte-identical
        # No compounded conversion ratio: shares must not have shrunk further
        # on the second run (a compounding bug would apply the 0.5 ratio
        # again, producing 25_000 instead of 50_000).
        assert state2[d]["holdings"][0]["shares"] == pytest.approx(50_000.0)
