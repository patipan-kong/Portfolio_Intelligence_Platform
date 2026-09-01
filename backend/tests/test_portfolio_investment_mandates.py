import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi import HTTPException, Response
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
import main
from models.database import (
    Base,
    GoalFundingAllocation,
    Portfolio,
    PortfolioInvestmentMandate,
    WealthGoal,
    Workspace,
)


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def make_portfolio(db, *, workspace_id=None, name="Portfolio"):
    portfolio = Portfolio(
        workspace_id=workspace_id or main._ws_id(db),
        name=name,
        cash_balance=123.0,
        goal_target_value=456.0,
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def make_goal(db, *, workspace_id=None, name="Goal", archived=False):
    goal = WealthGoal(
        workspace_id=workspace_id or main._ws_id(db),
        name=name,
        goal_type="OTHER",
        target_amount=1000.0,
        currency="THB",
        priority="MEDIUM",
        is_archived=archived,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def put(db, portfolio_id, goal_id):
    response = Response()
    payload = asyncio.run(
        main.put_portfolio_investment_mandate(portfolio_id, goal_id, response, db)
    )
    return response.status_code, payload


def list_rows(db, portfolio_id):
    return asyncio.run(main.list_portfolio_investment_mandates(portfolio_id, db))


def delete(db, portfolio_id, goal_id):
    return asyncio.run(main.delete_portfolio_investment_mandate(portfolio_id, goal_id, db))


def test_exact_minimal_persistence_contract_and_empty_list():
    db = make_session()
    portfolio = make_portfolio(db)
    columns = {column["name"] for column in inspect(db.bind).get_columns("portfolio_investment_mandates")}
    assert columns == {"id", "workspace_id", "portfolio_id", "wealth_goal_id", "created_at"}
    assert list_rows(db, portfolio.id) == []


def test_put_create_idempotency_and_deterministic_many_goal_listing():
    db = make_session()
    portfolio = make_portfolio(db)
    first_goal = make_goal(db, name="First")
    second_goal = make_goal(db, name="Second")

    first_status, first = put(db, portfolio.id, first_goal.id)
    retry_status, retry = put(db, portfolio.id, first_goal.id)
    second_status, second = put(db, portfolio.id, second_goal.id)

    assert (first_status, retry_status, second_status) == (201, 200, 201)
    assert retry == first
    assert [row["id"] for row in list_rows(db, portfolio.id)] == [first["id"], second["id"]]
    assert set(first) == {"id", "workspace_id", "portfolio_id", "wealth_goal_id", "created_at"}


def test_same_goal_can_link_to_multiple_portfolios_and_other_rows_are_untouched():
    db = make_session()
    first = make_portfolio(db, name="First")
    second = make_portfolio(db, name="Second")
    goal = make_goal(db)
    put(db, first.id, goal.id)
    _, second_row = put(db, second.id, goal.id)

    delete(db, first.id, goal.id)

    assert list_rows(db, first.id) == []
    assert list_rows(db, second.id) == [second_row]


def test_database_rejects_duplicate_pair():
    db = make_session()
    portfolio = make_portfolio(db)
    goal = make_goal(db)
    mandate = PortfolioInvestmentMandate(
        workspace_id=main._ws_id(db), portfolio_id=portfolio.id, wealth_goal_id=goal.id
    )
    db.add(mandate)
    db.commit()
    db.add(PortfolioInvestmentMandate(
        workspace_id=main._ws_id(db), portfolio_id=portfolio.id, wealth_goal_id=goal.id
    ))
    with pytest.raises(IntegrityError):
        db.commit()


def test_archived_goal_existing_put_read_remove_and_archive_restore_preserve_identity():
    db = make_session()
    portfolio = make_portfolio(db)
    goal = make_goal(db)
    _, created = put(db, portfolio.id, goal.id)

    asyncio.run(main.update_wealth_goal(goal.id, main.WealthGoalUpdate(is_archived=True), db))
    status, retry = put(db, portfolio.id, goal.id)
    assert status == 200
    assert retry == created
    assert list_rows(db, portfolio.id) == [created]

    asyncio.run(main.update_wealth_goal(goal.id, main.WealthGoalUpdate(is_archived=False), db))
    assert list_rows(db, portfolio.id)[0]["id"] == created["id"]
    response = delete(db, portfolio.id, goal.id)
    assert response.status_code == 204
    assert list_rows(db, portfolio.id) == []


def test_new_archived_goal_is_rejected_but_absent_delete_is_idempotent():
    db = make_session()
    portfolio = make_portfolio(db)
    archived = make_goal(db, archived=True)
    with pytest.raises(HTTPException) as error:
        put(db, portfolio.id, archived.id)
    assert error.value.status_code == 409

    response = delete(db, portfolio.id, archived.id)
    assert response.status_code == 204


@pytest.mark.parametrize("operation", ["list", "put", "delete"])
def test_missing_and_foreign_parents_are_indistinguishable(operation):
    db = make_session()
    own_portfolio = make_portfolio(db)
    own_goal = make_goal(db)
    other = Workspace(name="Other")
    db.add(other)
    db.commit()
    foreign_portfolio = make_portfolio(db, workspace_id=other.id, name="Foreign")
    foreign_goal = make_goal(db, workspace_id=other.id, name="Foreign Goal")

    failures = []
    pairs = [(999999, own_goal.id), (foreign_portfolio.id, own_goal.id)]
    if operation != "list":
        pairs += [(own_portfolio.id, 999999), (own_portfolio.id, foreign_goal.id)]
    for portfolio_id, goal_id in pairs:
        with pytest.raises(HTTPException) as error:
            if operation == "list":
                list_rows(db, portfolio_id)
            elif operation == "put":
                put(db, portfolio_id, goal_id)
            else:
                delete(db, portfolio_id, goal_id)
        failures.append((error.value.status_code, error.value.detail))

    expected_detail = "Portfolio not found" if operation == "list" else None
    assert all(code == 404 for code, _ in failures)
    if expected_detail:
        assert all(detail == expected_detail for _, detail in failures)
    else:
        assert failures[0][1] == failures[1][1] == "Portfolio not found"
        assert failures[2][1] == failures[3][1] == "Wealth goal not found"


def test_mandates_do_not_mutate_parents_or_couple_to_funding_designations():
    db = make_session()
    portfolio = make_portfolio(db)
    goal = make_goal(db)
    before = (portfolio.cash_balance, portfolio.goal_target_value, goal.target_amount, goal.priority)

    _, mandate = put(db, portfolio.id, goal.id)
    assert db.query(GoalFundingAllocation).count() == 0
    delete(db, portfolio.id, goal.id)
    db.refresh(portfolio)
    db.refresh(goal)

    assert before == (portfolio.cash_balance, portfolio.goal_target_value, goal.target_amount, goal.priority)
    assert db.query(GoalFundingAllocation).count() == 0
    assert mandate["portfolio_id"] == portfolio.id


def test_http_portfolio_delete_uses_orm_cascade_for_mandates():
    db = make_session()
    portfolio = make_portfolio(db, name="Delete me")
    survivor = make_portfolio(db, name="Survivor")
    goal = make_goal(db)
    put(db, portfolio.id, goal.id)
    _, surviving_mandate = put(db, survivor.id, goal.id)

    asyncio.run(main.delete_portfolio(portfolio.id, db))

    assert db.query(PortfolioInvestmentMandate).filter_by(portfolio_id=portfolio.id).count() == 0
    assert list_rows(db, survivor.id) == [surviving_mandate]
