"""Investor Intent V1 persistence, API contract and ownership isolation."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException, Response
from pydantic import ValidationError
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
import main
from manage import _delete_portfolio_cascade
from models.database import (
    Base, Portfolio, PortfolioItem, PositionIntent, PositionIntentRevision, Workspace,
)


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def make_portfolio(db, *, workspace_id=None, name="P"):
    portfolio = Portfolio(workspace_id=workspace_id or main._ws_id(db), name=name)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def hold(db, portfolio, symbol="PTT.BK", allow_swap=True, shares=10.0):
    item = PortfolioItem(workspace_id=portfolio.workspace_id, portfolio_id=portfolio.id,
                         symbol=symbol, shares=shares, avg_cost=30.0, allow_swap=allow_swap)
    db.add(item)
    db.commit()
    return item


def body(increase=False, decrease=False, pref="NONE", expected=None):
    return main.PositionIntentBody(increase_prohibited=increase, decrease_prohibited=decrease,
                                   soft_preference=pref, expected_revision=expected)


def put(db, portfolio_id, symbol, payload):
    response = Response()
    result = asyncio.run(main.put_position_intent(portfolio_id, symbol, payload, response, db))
    return response.status_code, result


def view(db, portfolio_id):
    return asyncio.run(main.list_position_intents(portfolio_id, db))


def revisions(db, portfolio_id, symbol):
    return asyncio.run(main.list_position_intent_revisions(portfolio_id, symbol, db))


def test_exact_persistence_contract():
    db = make_session()
    columns = {c["name"] for c in inspect(db.bind).get_columns("position_intents")}
    assert columns == {"id", "workspace_id", "portfolio_id", "position_symbol", "increase_prohibited",
                       "decrease_prohibited", "soft_preference", "revision", "author_kind",
                       "created_at", "updated_at"}
    history = {c["name"] for c in inspect(db.bind).get_columns("position_intent_revisions")}
    assert history == {"id", "workspace_id", "position_intent_id", "revision", "increase_prohibited",
                       "decrease_prohibited", "soft_preference", "author_kind", "recorded_at"}


def test_no_intent_is_reported_distinctly_and_legacy_lock_is_not_converted():
    db = make_session()
    p = make_portfolio(db)
    hold(db, p, "PTT.BK", allow_swap=False)
    hold(db, p, "AOT.BK")
    result = view(db, p.id)
    assert result["enforced_by_optimizer"] is False
    assert "not yet read or enforced" in result["disclosure"]
    rows = {r["position_symbol"]: r for r in result["positions"]}
    assert rows["PTT.BK"]["intent_status"] == "NO_CONFIRMED_INTENT" and rows["PTT.BK"]["intent"] is None
    assert rows["PTT.BK"]["legacy_allow_swap"] is False
    assert rows["PTT.BK"]["legacy_lock_status"] == "LEGACY_LOCKED_INTENT_UNCONFIRMED"
    assert rows["AOT.BK"]["legacy_lock_status"] is None
    assert db.query(PositionIntent).count() == 0


def test_create_revise_unchanged_and_revision_history():
    db = make_session()
    p = make_portfolio(db)
    hold(db, p)
    status, created = put(db, p.id, "ptt.bk", body(decrease=True, pref="PREFER_KEEP"))
    assert status == 201 and created["status"] == "CREATED"
    assert created["intent"]["revision"] == 1 and created["intent"]["author_kind"] == "OWNER"
    assert created["intent"]["position_symbol"] == "PTT.BK"
    assert created["enforced_by_optimizer"] is False

    status, same = put(db, p.id, "PTT.BK", body(decrease=True, pref="PREFER_KEEP", expected=1))
    assert status == 200 and same["status"] == "UNCHANGED" and same["intent"]["revision"] == 1

    status, revised = put(db, p.id, "PTT.BK", body(pref="NONE", expected=1))
    assert status == 200 and revised["status"] == "REVISED" and revised["intent"]["revision"] == 2
    assert revised["intent"]["decrease_prohibited"] is False

    history = revisions(db, p.id, "PTT.BK")
    assert [(h["revision"], h["decrease_prohibited"], h["soft_preference"]) for h in history] == [
        (1, True, "PREFER_KEEP"), (2, False, "NONE")]
    # Unrestricted explicit intent is still CONFIRMED, not absence.
    assert view(db, p.id)["positions"][0]["intent_status"] == "CONFIRMED"


@pytest.mark.parametrize("expected", [None, 2, 0])
def test_stale_or_missing_expected_revision_is_409(expected):
    db = make_session()
    p = make_portfolio(db)
    hold(db, p)
    put(db, p.id, "PTT.BK", body(increase=True))
    with pytest.raises(HTTPException) as exc:
        put(db, p.id, "PTT.BK", body(decrease=True, expected=expected))
    assert exc.value.status_code == 409
    assert db.query(PositionIntentRevision).count() == 1


def test_create_with_expected_revision_is_409():
    db = make_session()
    p = make_portfolio(db)
    hold(db, p)
    with pytest.raises(HTTPException) as exc:
        put(db, p.id, "PTT.BK", body(expected=1))
    assert exc.value.status_code == 409


def test_cannot_attach_intent_to_unheld_symbol():
    db = make_session()
    p = make_portfolio(db)
    with pytest.raises(HTTPException) as exc:
        put(db, p.id, "PTT.BK", body())
    assert exc.value.status_code == 404
    assert db.query(PositionIntent).count() == 0


def test_cross_portfolio_and_cross_workspace_isolation():
    db = make_session()
    mine = make_portfolio(db, name="Mine")
    sibling = make_portfolio(db, name="Sibling")
    other_ws = Workspace(name="Other")
    db.add(other_ws)
    db.commit()
    foreign = make_portfolio(db, workspace_id=other_ws.id, name="Foreign")
    hold(db, sibling, "PTT.BK")
    hold(db, foreign, "PTT.BK")

    # Held in a sibling portfolio does not make it a position of this one.
    with pytest.raises(HTTPException) as exc:
        put(db, mine.id, "PTT.BK", body())
    assert exc.value.status_code == 404
    # A portfolio of another workspace is not referenceable at all.
    for call in (lambda: put(db, foreign.id, "PTT.BK", body()),
                 lambda: view(db, foreign.id),
                 lambda: revisions(db, foreign.id, "PTT.BK")):
        with pytest.raises(HTTPException) as exc:
            call()
        assert exc.value.status_code == 404
    assert db.query(PositionIntent).count() == 0

    put(db, sibling.id, "PTT.BK", body(increase=True))
    assert view(db, mine.id)["positions"] == []
    with pytest.raises(HTTPException) as exc:
        revisions(db, mine.id, "PTT.BK")
    assert exc.value.status_code == 404


def test_intent_history_survives_full_sale_and_remains_revisable():
    # Rebuild and re-entry semantics: tests/test_position_intent_reentry.py.
    db = make_session()
    p = make_portfolio(db)
    item = hold(db, p)
    put(db, p.id, "PTT.BK", body(decrease=True))
    # A full sale deletes the PortfolioItem row; intent is keyed by symbol.
    db.delete(item)
    db.commit()
    row = view(db, p.id)["positions"][0]
    assert row["currently_held"] is False and row["intent"]["decrease_prohibited"] is True
    # Owner may still revise an intent whose position is no longer held.
    status, revised = put(db, p.id, "PTT.BK", body(expected=1))
    assert status == 200 and revised["intent"]["revision"] == 2
    hold(db, p)
    assert view(db, p.id)["positions"][0]["currently_held"] is True


def test_intent_write_never_touches_allow_swap():
    db = make_session()
    p = make_portfolio(db)
    item = hold(db, p, allow_swap=False)
    put(db, p.id, "PTT.BK", body())
    db.refresh(item)
    assert item.allow_swap is False


def test_request_validation_is_strict():
    for bad in ({"increase_prohibited": "true", "decrease_prohibited": False, "soft_preference": "NONE"},
                {"increase_prohibited": True, "decrease_prohibited": False, "soft_preference": "PREFER_ADD"},
                {"increase_prohibited": True, "decrease_prohibited": False, "soft_preference": "NONE",
                 "locked": True},
                {"increase_prohibited": True, "soft_preference": "NONE"}):
        with pytest.raises(ValidationError):
            main.PositionIntentBody(**bad)


def test_portfolio_deletion_removes_intents_via_orm_and_cli_paths():
    db = make_session()
    keep = make_portfolio(db, name="Keep")
    gone = make_portfolio(db, name="Gone")
    cli = make_portfolio(db, name="Cli")
    for portfolio in (keep, gone, cli):
        hold(db, portfolio)
        put(db, portfolio.id, "PTT.BK", body(increase=True))
    asyncio.run(main.delete_portfolio(gone.id, db))
    counts = _delete_portfolio_cascade(db, cli.id)
    db.commit()
    assert counts["position_intents"] == 1
    assert [i.portfolio_id for i in db.query(PositionIntent).all()] == [keep.id]
    assert db.query(PositionIntentRevision).count() == 1
