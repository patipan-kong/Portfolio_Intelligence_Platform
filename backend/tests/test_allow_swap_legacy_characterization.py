"""Characterization of legacy PortfolioItem.allow_swap — documents, does not endorse.

These pin CURRENT behavior, including known contradictions recorded as
follow-up findings in docs/implementation/INVESTOR_INTENT_V1.md. Investor
Intent V1 deliberately does not change or reinterpret any of it. If a later
slice migrates lock semantics, update these tests in that slice.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import agents.optimizer as optimizer_module
import models.asset  # noqa: F401
import models.registry_finding  # noqa: F401
from models.database import Base, Portfolio, PortfolioItem, Workspace
from services.funding_source_analysis import build_funding_sources
from services.portfolio_transactions import execute_sell


def _run(monkeypatch, holdings, l2_allocations):
    responses = {
        "layer1": {"swaps": [], "top_buys": [], "sector_flags": [], "priority": ""},
        "layer2": {"allocations": l2_allocations, "status": "REBALANCE"},
        "layer3": {"risk_flags": [], "safer_choice": "layer2", "final_risk_level": "low"},
    }
    monkeypatch.setattr(optimizer_module, "call_ai", lambda *a, **k: {
        "latency_ms": 1, "text": json.dumps(responses[k["usage_layer"]]),
    })
    result = optimizer_module.run_layered_optimizer(holdings, [], "P", cash_balance=0.0)
    return {a["symbol"]: a for a in result["target_allocations"]}, result["swap_suggestions"]


def _holding(symbol, signal, allow_swap):
    return {"symbol": symbol, "shares": 10, "current_price": 100, "signal": signal,
            "sector": "Energy", "allow_swap": allow_swap}


def test_lock_holds_allocation_against_forced_sell_but_swap_list_still_emits_forced_exit(monkeypatch):
    allocations, swaps = _run(monkeypatch,
        [_holding("LOCKED", "SELL", False), _holding("FREE", "HOLD", True)],
        [{"s": "LOCKED", "tw": 0, "sig": "SELL", "r": "exit"},
         {"s": "FREE", "tw": 50, "sig": "HOLD", "r": "keep"}])
    # Allocation: the lock silently wins over the forced exit.
    assert allocations["LOCKED"]["action"] == "HOLD"
    assert allocations["LOCKED"]["target_weight"] == allocations["LOCKED"]["current_weight"] == 50
    # Swap suggestions: the forced exit is still emitted for the same symbol.
    forced = [s for s in swaps if s["sell_symbol"] == "LOCKED"]
    assert forced and forced[0]["type"] == "SELL"
    assert forced[0]["reason"] == "Forced exit: SELL signal."


@pytest.mark.parametrize("sig,target", [("BUY", 70), ("ACCUMULATE", 60), ("REDUCE", 30), ("SELL", 0)])
def test_lock_blocks_both_increase_and_decrease_in_optimizer_allocations(monkeypatch, sig, target):
    allocations, _ = _run(monkeypatch,
        [_holding("LOCKED", "HOLD", False), _holding("FREE", "HOLD", True)],
        [{"s": "LOCKED", "tw": target, "sig": sig, "r": "ai"},
         {"s": "FREE", "tw": 50, "sig": "HOLD", "r": "keep"}])
    assert allocations["LOCKED"]["action"] == "HOLD"
    assert allocations["LOCKED"]["allocation_change_percent"] == 0.0


def test_unlocked_sell_label_forces_exit_regardless_of_ai(monkeypatch):
    allocations, _ = _run(monkeypatch,
        [_holding("FREE", "SELL", True), _holding("OTHER", "HOLD", True)],
        [{"s": "FREE", "tw": 50, "sig": "HOLD", "r": "keep"},
         {"s": "OTHER", "tw": 50, "sig": "HOLD", "r": "keep"}])
    assert allocations["FREE"]["action"] == "SELL"
    assert allocations["FREE"]["target_weight"] == 0.0


def test_decision_workspace_funding_has_no_lock_input_and_uses_locked_sell_label():
    # build_funding_sources receives no allow_swap; a locked holding labelled SELL
    # is offered as a funding source exactly like an unlocked one.
    result = build_funding_sources(
        item_values={"LOCKED": 1000.0}, signal_map={"LOCKED": "SELL"},
        cash_available=0.0, buy_set={"NEW"}, total_deployment=500.0,
    )
    funded = [s.symbol for s in result.sell_sources + result.reduce_sources + result.deferred_sources]
    assert "LOCKED" in funded


def test_transaction_layer_does_not_check_allow_swap():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    ws = Workspace(name="W")
    db.add(ws)
    db.flush()
    portfolio = Portfolio(workspace_id=ws.id, name="P", cash_balance=0.0)
    db.add(portfolio)
    db.flush()
    db.add(PortfolioItem(workspace_id=ws.id, portfolio_id=portfolio.id, symbol="PIS.BK",
                         shares=10, avg_cost=10, allow_swap=False))
    db.commit()
    execute_sell(db, ws.id, portfolio.id, "PIS.BK", 4, 12.0)
    item = db.query(PortfolioItem).filter_by(portfolio_id=portfolio.id, symbol="PIS.BK").one()
    assert item.shares == 6 and item.allow_swap is False
