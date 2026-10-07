"""Investor Intent V1 (R1): holding-episode applicability and re-confirmation.

PortfolioItem.created_at is the start of the current continuously-held
(portfolio_id, symbol) episode. The rebuilder preserves it; a full exit and a
later same-symbol re-entry start a new episode, so an intent confirmed before
it needs explicit re-confirmation.
"""
import asyncio
import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
import main
from models.database import Base, Portfolio, PortfolioItem, PositionIntentRevision, Transaction
from services.investor_intent_store import applicable_intent_state
from services.portfolio_rebuilder import (
    _commit_rebuild, _HoldingState, _PortfolioState, rebuild_portfolio,
)


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def make_portfolio(db):
    portfolio = Portfolio(workspace_id=main._ws_id(db), name="P")
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def hold(db, portfolio, symbol="PTT.BK", created_at=None, shares=10.0):
    item = PortfolioItem(workspace_id=portfolio.workspace_id, portfolio_id=portfolio.id, symbol=symbol,
                         shares=shares, avg_cost=30.0, created_at=created_at or datetime(2026, 1, 5, 9, 0))
    db.add(item)
    db.commit()
    return item


def body(increase=False, decrease=False, pref="NONE", expected=None):
    return main.PositionIntentBody(increase_prohibited=increase, decrease_prohibited=decrease,
                                   soft_preference=pref, expected_revision=expected)


def put(db, portfolio_id, payload, symbol="PTT.BK"):
    response = Response()
    result = asyncio.run(main.put_position_intent(portfolio_id, symbol, payload, response, db))
    return response.status_code, result


def row(db, portfolio_id, symbol="PTT.BK"):
    view = asyncio.run(main.list_position_intents(portfolio_id, db))
    return next(r for r in view["positions"] if r["position_symbol"] == symbol)


def revisions(db, portfolio_id, symbol="PTT.BK"):
    return asyncio.run(main.list_position_intent_revisions(portfolio_id, symbol, db))


def rebuild(db, portfolio, holdings):
    """Run the rebuilder's real commit stage (delete + re-create every PortfolioItem)."""
    state = _PortfolioState(Decimal("0"), {
        symbol: _HoldingState(symbol=symbol, report_symbol=symbol, shares=Decimal(str(shares)),
                              avg_cost=Decimal("30"))
        for symbol, shares in holdings.items()
    }, Decimal("0"))
    _commit_rebuild(db, portfolio.id, portfolio.workspace_id, portfolio, state, [], skip_snapshots=True)
    db.commit()


def full_exit(db, portfolio, symbol="PTT.BK"):
    db.query(PortfolioItem).filter_by(portfolio_id=portfolio.id, symbol=symbol).delete()
    db.commit()


def after_last_revision(db, portfolio_id, symbol="PTT.BK"):
    last = revisions(db, portfolio_id, symbol)[-1]["recorded_at"]
    return datetime.fromisoformat(last) + timedelta(microseconds=1)


@pytest.mark.parametrize("payload", [body(decrease=True), body()], ids=["restricted", "explicit-unrestricted"])
def test_confirmed_intent_survives_ordinary_rebuild(payload):
    db = make_session()
    p = make_portfolio(db)
    started = datetime(2026, 1, 5, 9, 0)
    hold(db, p, created_at=started)
    put(db, p.id, payload)
    rebuild(db, p, {"PTT.BK": 10})
    current = row(db, p.id)
    assert current["intent_status"] == "CONFIRMED"
    assert current["holding_started_at"] == started.isoformat()
    assert applicable_intent_state(db, p.workspace_id, p.id, "PTT.BK") is not None


def test_multiple_rebuilds_preserve_original_episode_start_and_other_metadata():
    db = make_session()
    p = make_portfolio(db)
    started = datetime(2026, 1, 5, 9, 0)
    item = hold(db, p, created_at=started)
    item.allow_swap = False
    db.commit()
    put(db, p.id, body(increase=True))
    for shares in (10, 12, 8):  # quantity changes while continuously held
        rebuild(db, p, {"PTT.BK": shares})
    rebuilt = db.query(PortfolioItem).filter_by(portfolio_id=p.id, symbol="PTT.BK").one()
    assert rebuilt.created_at == started
    assert rebuilt.allow_swap is False and rebuilt.shares == 8
    assert row(db, p.id)["intent_status"] == "CONFIRMED"
    assert len(revisions(db, p.id)) == 1


def test_rebuild_preserves_legacy_null_episode_start():
    db = make_session()
    p = make_portfolio(db)
    item = hold(db, p)
    item.created_at = None
    db.commit()
    put(db, p.id, body(decrease=True))
    rebuild(db, p, {"PTT.BK": 10})
    rebuilt = db.query(PortfolioItem).filter_by(portfolio_id=p.id, symbol="PTT.BK").one()
    assert rebuilt.created_at is None
    assert row(db, p.id)["intent_status"] == "CONFIRMED"


def test_rebuild_starts_a_new_episode_only_for_rows_absent_before_it():
    db = make_session()
    p = make_portfolio(db)
    hold(db, p, created_at=datetime(2026, 1, 5, 9, 0))
    before = datetime.utcnow()
    rebuild(db, p, {"PTT.BK": 10, "SCB.BK": 5})
    items = {i.symbol: i for i in db.query(PortfolioItem).filter_by(portfolio_id=p.id)}
    assert items["PTT.BK"].created_at == datetime(2026, 1, 5, 9, 0)
    assert items["SCB.BK"].created_at >= before


@pytest.mark.parametrize("payload", [body(decrease=True), body()], ids=["restricted", "explicit-unrestricted"])
def test_full_exit_then_same_symbol_reentry_requires_reconfirmation(payload):
    db = make_session()
    p = make_portfolio(db)
    hold(db, p)
    put(db, p.id, payload)
    full_exit(db, p)
    assert row(db, p.id)["currently_held"] is False
    hold(db, p, created_at=after_last_revision(db, p.id))  # later re-entry
    current = row(db, p.id)
    assert current["intent_status"] == "RECONFIRMATION_REQUIRED"
    assert current["intent"]["revision"] == 1  # history still shown, not applied
    assert applicable_intent_state(db, p.workspace_id, p.id, "PTT.BK") is None
    assert len(revisions(db, p.id)) == 1  # nothing created on the owner's behalf
    # A rebuild of the re-entered holding does not restore the old confirmation.
    rebuild(db, p, {"PTT.BK": 10})
    assert row(db, p.id)["intent_status"] == "RECONFIRMATION_REQUIRED"


def test_reconfirmation_appends_a_revision_and_confirms_for_the_current_episode():
    db = make_session()
    p = make_portfolio(db)
    hold(db, p)
    put(db, p.id, body(decrease=True, pref="PREFER_KEEP"))
    full_exit(db, p)
    hold(db, p, created_at=after_last_revision(db, p.id))
    first = revisions(db, p.id)[0]

    # Stale revision is still rejected.
    with pytest.raises(Exception) as stale:
        put(db, p.id, body(decrease=True, pref="PREFER_KEEP", expected=None))
    assert getattr(stale.value, "status_code", None) == 409

    status, result = put(db, p.id, body(decrease=True, pref="PREFER_KEEP", expected=1))
    assert status == 200 and result["status"] == "RECONFIRMED" and result["intent"]["revision"] == 2
    current = row(db, p.id)
    assert current["intent_status"] == "CONFIRMED"
    state = applicable_intent_state(db, p.workspace_id, p.id, "PTT.BK")
    assert state is not None and state.decrease_prohibited is True and state.revision == 2

    history = revisions(db, p.id)
    assert [r["revision"] for r in history] == [1, 2]
    assert history[0] == first  # old revision untouched
    assert datetime.fromisoformat(history[1]["recorded_at"]) >= datetime.fromisoformat(current["holding_started_at"])

    # Once re-confirmed, an identical write is UNCHANGED again (no extra revision).
    status, result = put(db, p.id, body(decrease=True, pref="PREFER_KEEP", expected=2))
    assert result["status"] == "UNCHANGED" and len(revisions(db, p.id)) == 2
    # And the re-confirmation survives later rebuilds.
    rebuild(db, p, {"PTT.BK": 10})
    assert row(db, p.id)["intent_status"] == "CONFIRMED"


def test_changed_values_on_reentry_revise_and_confirm():
    db = make_session()
    p = make_portfolio(db)
    hold(db, p)
    put(db, p.id, body(decrease=True))
    full_exit(db, p)
    hold(db, p, created_at=after_last_revision(db, p.id))
    _, result = put(db, p.id, body(increase=True, expected=1))
    assert result["status"] == "REVISED" and result["intent"]["revision"] == 2
    assert row(db, p.id)["intent_status"] == "CONFIRMED"


def test_identical_write_while_confirmed_records_nothing():
    db = make_session()
    p = make_portfolio(db)
    hold(db, p)
    put(db, p.id, body(decrease=True))
    _, result = put(db, p.id, body(decrease=True, expected=1))
    assert result["status"] == "UNCHANGED"
    assert db.query(PositionIntentRevision).count() == 1


def test_end_to_end_rebuild_portfolio_keeps_episode_and_intent():
    """Full rebuild_portfolio() commit path on a real ledger, not only the commit stage."""
    db = make_session()
    p = make_portfolio(db)
    ws = p.workspace_id
    db.add_all([
        Transaction(workspace_id=ws, portfolio_id=p.id, transaction_type="DEPOSIT", total_amount=1000.0,
                    fees=0, taxes=0, transaction_date=datetime(2026, 1, 2)),
        Transaction(workspace_id=ws, portfolio_id=p.id, symbol="PTT.BK", transaction_type="BUY", shares=10,
                    price_per_share=30, total_amount=300.0, fees=0, taxes=0, transaction_date=datetime(2026, 1, 5)),
    ])
    p.cash_balance = 700.0
    db.commit()
    started = datetime(2026, 1, 5, 9, 0)
    hold(db, p, created_at=started)
    put(db, p.id, body(decrease=True))

    result = asyncio.run(rebuild_portfolio(db=db, portfolio_id=p.id, workspace_id=ws,
                                           skip_snapshots=True, dry_run=False))
    assert result.success, result.error
    rebuilt = db.query(PortfolioItem).filter_by(portfolio_id=p.id, symbol="PTT.BK").one()
    assert rebuilt.created_at == started and rebuilt.shares == 10
    assert row(db, p.id)["intent_status"] == "CONFIRMED"
