"""Service layer for transaction execution.

Uses Python Decimal internally to avoid float-accumulation errors.
All values stored as Float in DB (SQLite/PostgreSQL compatible).

Supported transaction types:
  BUY              — buy equity; increases holding, reduces cash
  SELL             — sell equity; reduces holding, increases cash
  DEPOSIT          — add cash to portfolio
  WITHDRAW         — remove cash from portfolio (prevents negative balance)
  INITIAL_POSITION — onboarding: import existing holding, does NOT affect cash
  INITIAL_CASH     — onboarding: set starting cash balance
  QUANTITY_CORRECTION — manual share-count adjustment, does NOT affect cash

Fee accounting
--------------
All BUY and SELL fees are calculated via the shared broker fee quote engine:
    Commission   = Gross × 0.15%
    Trading Fee  = Gross × 0.006%
    Clearing Fee = Gross × 0.001%
    VAT          = (Commission + Trading + Clearing) × 7%

Stored in Transaction columns:
    fees  = commission + trading_fee + clearing_fee  (pre-VAT sub-total)
    taxes = VAT amount

Cost basis (BUY)
----------------
Fees are included in the weighted-average cost (fee-inclusive basis):
    effective_price = (gross + total_fees_incl_vat) / shares
    new_avg_cost    = (old_shares × old_avg + new_shares × effective_price)
                      / (old_shares + new_shares)

This means avg_cost already embeds the purchase cost fully, so SELL P/L
only deducts the SELL-side fees—no double-deduction of BUY fees.

Realized P/L (SELL)
-------------------
    realized_pnl = (sell_price - avg_cost) × shares - total_sell_fees_incl_vat

Because avg_cost includes BUY fees, the complete round-trip cost is:
    cost_in  = gross_buy + buy_fees_incl_vat
    cash_out = gross_sell - sell_fees_incl_vat
    true_pnl = cash_out - cost_in  (= the above formula)
"""
import logging
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from datetime import date as date_cls, datetime, time

from sqlalchemy.orm import Session

from models.database import Portfolio, PortfolioItem, Transaction
from services import asset_registry, capability_lookup_service, registry_lookup
from services.portfolio_reference import resolve_portfolio_reference
from services.broker_fees import FeeProfile, FeeQuoteStatus, TradeSide
from services.broker_fees_compat import quote_transaction_fee_compat
from services.capability_lookup_service import UnresolvedCapability
from services.capability_safety import grants_dividend_flow, permits_quantity_valuation
from services.execution_eligibility import (
    ShadowExecutionAction,
    consult_execution_eligibility_shadow,
)
from services.execution_eligibility_shadow import (
    resolve_execution_eligibility_shadow_facts,
)
from services.runtime_consultation import (
    RuntimeConsultationLog,
    RuntimeFindingCategory,
    RuntimeValidationFinding,
)
from services.transaction_canonicalizer import parse_position_conversion_payload

_QUANT = Decimal("0.000001")
_log = logging.getLogger(__name__)

_QUANTITY_VALUATION_CHECK = "RUNTIME_TRANSACTION_QUANTITY_VALUATION"
_DIVIDEND_FLOW_CHECK = "RUNTIME_TRANSACTION_DIVIDEND_FLOW"


def _d(v: float) -> Decimal:
    return Decimal(str(v))


def _f(v: Decimal) -> float:
    return float(v.quantize(_QUANT, rounding=ROUND_HALF_UP))


# ── Stage R1 runtime consultation (M30.3 brief; fourth Asset Definition
# Runtime consumer, after ledger_validator (M11), asset_registry (M12), and
# portfolio_snapshots (M30.2)) ──────────────────────────────────────────────
#
# Two legacy assumptions in this module have no capability gate today (M29
# audit, SR-1 finding):
#   1. `value = shares × price` is computed unconditionally in execute_buy(),
#      execute_sell(), and execute_initial_position().
#   2. execute_dividend() accepts a DIVIDEND transaction for any symbol (or
#      None) and credits cash unconditionally.
# This function asks the runtime the same question legacy logic already
# answers implicitly, and records any disagreement as a shadow finding —
# mirrors ledger_validator._consult_runtime_capabilities() (M11),
# asset_registry._consult_runtime_for_mint() (M12), and
# portfolio_snapshots._consult_runtime_for_snapshot() (M30.2) exactly:
# read-only, never raises, never gates, never changes any computed value.
#
# Single-symbol form (capability_lookup_service.resolve_capability_view),
# since every write path here handles exactly one symbol per call — unlike
# the batch consumers (ledger_validator, portfolio_snapshots).
#
# Every call site below invokes this AFTER db.commit(), immediately before
# building the dict returned to the caller — structurally incapable of
# affecting the transaction already recorded or the dict returned.
def _consult_runtime_for_transaction(
    db: Session,
    symbol: str | None,
    tx_id: int,
    kind: str,  # "quantity_valuation" | "dividend_flow"
) -> RuntimeConsultationLog:
    """Never raises — resolve_capability_view() already turns an unminted
    symbol, an undefined asset_type, or a registry boot failure into an
    UnresolvedCapability rather than an exception; this function just turns
    that into a MISSING_BINDING finding, same as the other Stage R1
    consumers.
    """
    if not symbol:
        return RuntimeConsultationLog(consulted=0, agreements=0, findings=())

    if kind == "quantity_valuation":
        check_id = _QUANTITY_VALUATION_CHECK
        question = "permits_quantity_valuation()"
        predicate = permits_quantity_valuation
        legacy_detail = "computes value = shares × price unconditionally"
    else:
        check_id = _DIVIDEND_FLOW_CHECK
        question = "grants_dividend_flow()"
        predicate = grants_dividend_flow
        legacy_detail = "accepts a DIVIDEND transaction and credits cash unconditionally"

    view = capability_lookup_service.resolve_capability_view(db, symbol)
    if isinstance(view, UnresolvedCapability):
        finding = RuntimeValidationFinding(
            category=RuntimeFindingCategory.MISSING_BINDING.value,
            check_id=check_id, transaction_ids=(tx_id,),
            binding=symbol, question=question,
            legacy_result=True, runtime_result=None, detail=view.reason,
        )
        return RuntimeConsultationLog(consulted=1, agreements=0, findings=(finding,))

    runtime_result = predicate(view)
    if runtime_result is True:
        return RuntimeConsultationLog(consulted=1, agreements=1, findings=())

    finding = RuntimeValidationFinding(
        category=RuntimeFindingCategory.RUNTIME_MISMATCH.value,
        check_id=check_id, transaction_ids=(tx_id,),
        binding=symbol, question=question,
        legacy_result=True, runtime_result=runtime_result,
        detail=(
            f"{symbol!r} {legacy_detail}, but the runtime capability view "
            f"disagrees ({question} -> {runtime_result})."
        ),
    )
    return RuntimeConsultationLog(consulted=1, agreements=0, findings=(finding,))


def _log_runtime_consultation(
    db: Session, symbol: str | None, tx_id: int, kind: str, fn_name: str,
) -> None:
    """Wraps _consult_runtime_for_transaction in the same try/except-and-log
    shape used by every other Stage R1 call site — never lets a consultation
    failure propagate to the caller."""
    try:
        log = _consult_runtime_for_transaction(db, symbol, tx_id, kind)
    except Exception as exc:
        _log.warning(
            "runtime consultation failed for %s tx=%s symbol=%s: %s",
            fn_name, tx_id, symbol, exc,
        )
        return
    for finding in log.findings:
        _log.warning(
            "runtime consultation finding on %s: check_id=%s category=%s "
            "binding=%s detail=%s",
            fn_name, finding.check_id, finding.category, finding.binding, finding.detail,
        )


def _resolve_write_time_asset_id(db: Session, symbol: str | None) -> int | None:
    """Resolves `symbol` to a permanent asset_id at the moment it enters the
    ledger (M5 Track B Stage 3, TDD §2.3) — the only legitimate resolution
    point, per ASSET_REGISTRY.md §10. Reuses registry_lookup.resolve_asset(),
    the platform's single Registry authority; performs no identity logic of
    its own (ADR-004).

    Fails open, per ASSET_REGISTRY.md §4 ("resolve decisively or ask — never
    guess") and TDD §4.1: an unresolved symbol, or any unexpected error
    resolving it, returns None rather than raising or inventing an id. The
    legacy symbol is always what gets persisted regardless of this result —
    this function never blocks a write. Unresolved outcomes are logged so
    they're observable (ENGINEERING_PRINCIPLES.md "Failure Handling"),
    mirroring the existing registry_recommendation_context.py convention.
    """
    if not symbol:
        return None
    try:
        resolved = registry_lookup.resolve_asset(db, symbol)
    except Exception as exc:
        _log.warning(
            "portfolio_transactions: resolve_asset raised for symbol=%r: %s — "
            "asset_id left NULL, legacy symbol persisted unchanged",
            symbol, exc,
        )
        return None
    if isinstance(resolved, registry_lookup.AssetView):
        return int(resolved.asset_id)
    _log.info(
        "portfolio_transactions: symbol=%r unresolved at write time (reason=%s) — "
        "asset_id left NULL, legacy symbol persisted unchanged",
        symbol, getattr(resolved, "reason", "unknown"),
    )
    return None


def _observe_transaction_execution_eligibility(
    db: Session,
    symbol: str,
    legacy_action: str,
) -> None:
    """Observe eligibility only after the legacy transaction has committed."""

    try:
        facts_by_symbol = resolve_execution_eligibility_shadow_facts(db, [symbol])
        consult_execution_eligibility_shadow(
            [ShadowExecutionAction(symbol, legacy_action)],
            facts_by_symbol,
            legacy_path="PORTFOLIO_TRANSACTION_COMMITTED",
            logger=_log,
        )
    except Exception as exc:
        _log.warning(
            "execution eligibility shadow failed after committed %s symbol=%r: %s",
            legacy_action,
            symbol,
            exc,
        )


# ─── BUY ──────────────────────────────────────────────────────────────────────

def execute_buy(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    symbol: str,
    shares: float,
    price_per_share: float,
    currency: str = "THB",
    exchange_rate: float = 1.0,
    transaction_date: datetime | None = None,
    notes: str | None = None,
    sector: str | None = None,
    fee_profile: FeeProfile | None = None,
    execution_decision_id: int | None = None,
) -> dict:
    """Create a BUY transaction, upsert the holding, and reduce portfolio cash.

    Fee profile is auto-selected from the symbol (DR vs SET) unless overridden.
    Avg cost uses weighted-average formula with fee-inclusive effective price:
        effective_price = (gross + all_fees) / shares
    Cash is allowed to go negative so users can record purchases before depositing.

    execution_decision_id (AI Evaluation M2, P5): optional, metadata-only
    link to the UserExecutionDecision that led to this trade. Populated only
    when the caller passes one (app buy/sell flow after an APPROVED/PARTIAL
    decision) — never inferred or backfilled by this function. The
    canonicalizer, portfolio_rebuilder, and ledger validators must never read
    this column; it rides on the ledger as evaluation-layer metadata, not
    ledger data itself.
    """
    portfolio = resolve_portfolio_reference(db, portfolio_id, ws_id)
    if not portfolio:
        raise ValueError(f"Portfolio {portfolio_id} not found")

    d_shares = _d(shares)
    d_price  = _d(price_per_share)
    d_gross  = d_shares * d_price
    tx_date = transaction_date or datetime.utcnow()

    fee_quote = quote_transaction_fee_compat(
        symbol,
        side=TradeSide.BUY,
        quantity=d_shares,
        unit_price=d_price,
        currency=currency,
        quoted_at=tx_date,
        effective_at=tx_date,
        profile_override=fee_profile,
    )
    assert fee_quote.status == FeeQuoteStatus.QUOTED
    assert fee_quote.net_cash_effect is not None
    bd = fee_quote.to_fee_breakdown()

    total    = -fee_quote.net_cash_effect                 # cash out
    eff_price = total / d_shares                          # fee-inclusive cost per share

    resolved_asset_id = _resolve_write_time_asset_id(db, symbol)

    item = db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id, symbol=symbol).first()
    if item:
        old_shares = _d(item.shares)
        old_cost   = _d(item.avg_cost)
        new_shares = old_shares + d_shares
        # weighted-average using fee-inclusive total cost of this lot
        new_avg = (old_shares * old_cost + total) / new_shares
        item.shares  = _f(new_shares)
        item.avg_cost = _f(new_avg)
        if sector and not item.sector:
            item.sector = sector
        if resolved_asset_id is not None and item.asset_id is None:
            item.asset_id = resolved_asset_id
    else:
        item = PortfolioItem(
            workspace_id=ws_id,
            portfolio_id=portfolio_id,
            symbol=symbol,
            shares=_f(d_shares),
            avg_cost=_f(eff_price),       # fee-inclusive from the start
            sector=sector,
            asset_id=resolved_asset_id,
        )
        db.add(item)

    portfolio.cash_balance = _f(_d(portfolio.cash_balance) - total)

    tx = Transaction(
        workspace_id=ws_id,
        portfolio_id=portfolio_id,
        symbol=symbol,
        transaction_type="BUY",
        shares=_f(d_shares),
        price_per_share=_f(d_price),
        total_amount=_f(total),
        fees=_f(bd.total_fees_excl_vat),   # commission + trading + clearing
        taxes=_f(bd.vat),                  # VAT portion
        currency=currency,
        exchange_rate=exchange_rate,
        transaction_date=tx_date,
        notes=notes,
        sector=sector or (item.sector if item else None),
        execution_decision_id=execution_decision_id,
        asset_id=resolved_asset_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    db.refresh(item)

    _log_runtime_consultation(db, symbol, tx.id, "quantity_valuation", "execute_buy")

    result = {
        "transaction_id": tx.id,
        "type": "BUY",
        "symbol": symbol,
        "shares": tx.shares,
        "price_per_share": tx.price_per_share,
        "gross_amount": _f(d_gross),
        "total_amount": tx.total_amount,
        "fees": tx.fees,
        "taxes": tx.taxes,
        "fee_profile": fee_quote.schedule_id,
        "fee_breakdown": bd.to_dict(),
        "transaction_date": tx.transaction_date.isoformat() + "Z",
        "notes": tx.notes,
        "cash_balance": portfolio.cash_balance if portfolio else None,
        "holding": {
            "shares": item.shares,
            "avg_cost": item.avg_cost,
            "sector": item.sector,
        },
    }
    _observe_transaction_execution_eligibility(db, symbol, "BUY")
    return result


# ─── SELL ─────────────────────────────────────────────────────────────────────

def execute_sell(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    symbol: str,
    shares: float,
    price_per_share: float,
    currency: str = "THB",
    exchange_rate: float = 1.0,
    transaction_date: datetime | None = None,
    notes: str | None = None,
    remove_if_zero: bool = True,
    fee_profile: FeeProfile | None = None,
    execution_decision_id: int | None = None,
) -> dict:
    """Create a SELL transaction, reduce the holding, and increase portfolio cash.

    Fee profile is auto-selected from the symbol unless overridden.

    Raises ValueError if:
    - No holding exists for the symbol
    - Selling more shares than currently held (oversell prevention)

    Realized P/L = (sell_price - avg_cost) × shares - total_sell_fees_incl_vat
    Because avg_cost already embeds the BUY-side fees, this correctly reflects
    the complete round-trip cost of the position.
    """
    portfolio = resolve_portfolio_reference(db, portfolio_id, ws_id)
    if not portfolio:
        raise ValueError(f"Portfolio {portfolio_id} not found")

    item = db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id, symbol=symbol).first()
    if not item:
        raise ValueError(f"No holding found for {symbol} in this portfolio")

    resolved_asset_id = _resolve_write_time_asset_id(db, symbol)
    if resolved_asset_id is not None and item.asset_id is None:
        item.asset_id = resolved_asset_id

    d_shares = _d(shares)
    d_price  = _d(price_per_share)
    d_gross  = d_shares * d_price
    d_held   = _d(item.shares)

    if d_shares > d_held + Decimal("0.0001"):
        raise ValueError(
            f"Cannot sell {shares} shares of {symbol}; only {item.shares} held"
        )

    tx_date = transaction_date or datetime.utcnow()
    fee_quote = quote_transaction_fee_compat(
        symbol,
        side=TradeSide.SELL,
        quantity=d_shares,
        unit_price=d_price,
        currency=currency,
        quoted_at=tx_date,
        effective_at=tx_date,
        profile_override=fee_profile,
    )
    assert fee_quote.status == FeeQuoteStatus.QUOTED
    assert fee_quote.net_cash_effect is not None
    bd = fee_quote.to_fee_breakdown()

    net_proceeds = fee_quote.net_cash_effect   # cash in
    d_avg        = _d(item.avg_cost)
    realized_pnl = (d_price - d_avg) * d_shares - bd.total_fees_incl_vat

    new_shares   = d_held - d_shares
    holding_removed = False

    pnl_note  = f"Realized P&L: {_f(realized_pnl):+.4f}"
    full_notes = f"{pnl_note}. {notes}" if notes else pnl_note

    if _f(new_shares) <= 0 and remove_if_zero:
        remaining_shares = 0.0
        remaining_avg    = item.avg_cost
        db.delete(item)
        holding_removed  = True
    else:
        item.shares = _f(new_shares)
        remaining_shares = item.shares
        remaining_avg    = item.avg_cost   # avg_cost unchanged on partial sell

    portfolio.cash_balance = _f(_d(portfolio.cash_balance) + net_proceeds)

    tx = Transaction(
        workspace_id=ws_id,
        portfolio_id=portfolio_id,
        symbol=symbol,
        transaction_type="SELL",
        shares=_f(d_shares),
        price_per_share=_f(d_price),
        total_amount=_f(abs(net_proceeds)),
        fees=_f(bd.total_fees_excl_vat),
        taxes=_f(bd.vat),
        currency=currency,
        exchange_rate=exchange_rate,
        transaction_date=tx_date,
        notes=full_notes,
        execution_decision_id=execution_decision_id,
        asset_id=resolved_asset_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    _log_runtime_consultation(db, symbol, tx.id, "quantity_valuation", "execute_sell")

    result = {
        "transaction_id": tx.id,
        "type": "SELL",
        "symbol": symbol,
        "shares": tx.shares,
        "price_per_share": tx.price_per_share,
        "gross_amount": _f(d_gross),
        "total_amount": tx.total_amount,
        "fees": tx.fees,
        "taxes": tx.taxes,
        "fee_profile": fee_quote.schedule_id,
        "fee_breakdown": bd.to_dict(),
        "realized_pnl": _f(realized_pnl),
        "transaction_date": tx.transaction_date.isoformat() + "Z",
        "notes": tx.notes,
        "holding_removed": holding_removed,
        "cash_balance": portfolio.cash_balance if portfolio else None,
        "holding": None if holding_removed else {
            "shares": remaining_shares,
            "avg_cost": remaining_avg,
        },
    }
    _observe_transaction_execution_eligibility(db, symbol, "SELL")
    return result


# ─── DEPOSIT ──────────────────────────────────────────────────────────────────

def execute_deposit(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    amount: float,
    currency: str = "THB",
    exchange_rate: float = 1.0,
    transaction_date: datetime | None = None,
    notes: str | None = None,
) -> dict:
    """Add cash to the portfolio. No equity holding is affected."""
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")

    d_amount = _d(amount)
    tx_date  = transaction_date or datetime.utcnow()

    portfolio = resolve_portfolio_reference(db, portfolio_id, ws_id)
    if not portfolio:
        raise ValueError("Portfolio not found")

    portfolio.cash_balance = _f(_d(portfolio.cash_balance) + d_amount)

    tx = Transaction(
        workspace_id=ws_id,
        portfolio_id=portfolio_id,
        symbol=None,
        transaction_type="DEPOSIT",
        shares=None,
        price_per_share=None,
        total_amount=_f(d_amount),
        fees=0.0,
        taxes=0.0,
        currency=currency,
        exchange_rate=exchange_rate,
        transaction_date=tx_date,
        notes=notes,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return {
        "transaction_id": tx.id,
        "type": "DEPOSIT",
        "symbol": None,
        "amount": tx.total_amount,
        "total_amount": tx.total_amount,
        "transaction_date": tx.transaction_date.isoformat() + "Z",
        "notes": tx.notes,
        "cash_balance": portfolio.cash_balance,
    }


# ─── WITHDRAW ─────────────────────────────────────────────────────────────────

def execute_withdraw(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    amount: float,
    currency: str = "THB",
    exchange_rate: float = 1.0,
    transaction_date: datetime | None = None,
    notes: str | None = None,
) -> dict:
    """Remove cash from the portfolio. Raises ValueError if insufficient cash."""
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")

    d_amount = _d(amount)
    tx_date  = transaction_date or datetime.utcnow()

    portfolio = resolve_portfolio_reference(db, portfolio_id, ws_id)
    if not portfolio:
        raise ValueError("Portfolio not found")

    new_cash = _d(portfolio.cash_balance) - d_amount
    if new_cash < Decimal("0"):
        raise ValueError(
            f"Insufficient cash: balance is {portfolio.cash_balance:.2f}, "
            f"cannot withdraw {amount:.2f}"
        )

    portfolio.cash_balance = _f(new_cash)

    tx = Transaction(
        workspace_id=ws_id,
        portfolio_id=portfolio_id,
        symbol=None,
        transaction_type="WITHDRAW",
        shares=None,
        price_per_share=None,
        total_amount=_f(d_amount),
        fees=0.0,
        taxes=0.0,
        currency=currency,
        exchange_rate=exchange_rate,
        transaction_date=tx_date,
        notes=notes,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return {
        "transaction_id": tx.id,
        "type": "WITHDRAW",
        "symbol": None,
        "amount": tx.total_amount,
        "total_amount": tx.total_amount,
        "transaction_date": tx.transaction_date.isoformat() + "Z",
        "notes": tx.notes,
        "cash_balance": portfolio.cash_balance,
    }


# ─── DIVIDEND ─────────────────────────────────────────────────────────────────

def execute_dividend(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    symbol: str | None,
    amount: float,
    currency: str = "THB",
    exchange_rate: float = 1.0,
    transaction_date: datetime | None = None,
    notes: str | None = None,
) -> dict:
    """Record a dividend received from a holding. Increases cash balance."""
    if amount <= 0:
        raise ValueError("Dividend amount must be positive")

    d_amount = _d(amount)
    tx_date  = transaction_date or datetime.utcnow()

    portfolio = resolve_portfolio_reference(db, portfolio_id, ws_id)
    if not portfolio:
        raise ValueError("Portfolio not found")

    portfolio.cash_balance = _f(_d(portfolio.cash_balance) + d_amount)

    resolved_asset_id = _resolve_write_time_asset_id(db, symbol)

    tx = Transaction(
        workspace_id=ws_id,
        portfolio_id=portfolio_id,
        symbol=symbol,
        transaction_type="DIVIDEND",
        shares=None,
        price_per_share=None,
        total_amount=_f(d_amount),
        fees=0.0,
        taxes=0.0,
        currency=currency,
        exchange_rate=exchange_rate,
        transaction_date=tx_date,
        notes=notes,
        asset_id=resolved_asset_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    _log_runtime_consultation(db, symbol, tx.id, "dividend_flow", "execute_dividend")

    return {
        "transaction_id": tx.id,
        "type": "DIVIDEND",
        "symbol": symbol,
        "amount": tx.total_amount,
        "total_amount": tx.total_amount,
        "transaction_date": tx.transaction_date.isoformat() + "Z",
        "notes": tx.notes,
        "cash_balance": portfolio.cash_balance,
        "holding": None,
    }


# ─── INITIAL_POSITION ─────────────────────────────────────────────────────────

def execute_initial_position(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    symbol: str,
    shares: float,
    avg_cost: float,
    transaction_date: datetime | None = None,
    notes: str | None = None,
    sector: str | None = None,
) -> dict:
    """Import an existing holding as INITIAL_POSITION.

    Does NOT affect cash balance (this is an onboarding import, not a new trade).
    The avg_cost is taken as-is — no fee adjustment (the original purchase costs
    are unknown at import time).
    """
    if shares <= 0:
        raise ValueError("shares must be positive")
    if avg_cost <= 0:
        raise ValueError("avg_cost must be positive")
    if resolve_portfolio_reference(db, portfolio_id, ws_id) is None:
        raise ValueError(f"Portfolio {portfolio_id} not found")

    d_shares = _d(shares)
    d_avg    = _d(avg_cost)
    total    = d_shares * d_avg
    tx_date  = transaction_date or datetime.utcnow()

    resolved_asset_id = _resolve_write_time_asset_id(db, symbol)

    item = db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id, symbol=symbol).first()
    if item:
        old_shares = _d(item.shares)
        old_cost   = _d(item.avg_cost)
        new_shares = old_shares + d_shares
        new_avg    = (old_shares * old_cost + d_shares * d_avg) / new_shares
        item.shares   = _f(new_shares)
        item.avg_cost = _f(new_avg)
        if sector and not item.sector:
            item.sector = sector
        if resolved_asset_id is not None and item.asset_id is None:
            item.asset_id = resolved_asset_id
    else:
        item = PortfolioItem(
            workspace_id=ws_id,
            portfolio_id=portfolio_id,
            symbol=symbol,
            shares=_f(d_shares),
            avg_cost=_f(d_avg),
            sector=sector,
            asset_id=resolved_asset_id,
        )
        db.add(item)

    tx = Transaction(
        workspace_id=ws_id,
        portfolio_id=portfolio_id,
        symbol=symbol,
        transaction_type="INITIAL_POSITION",
        shares=_f(d_shares),
        price_per_share=_f(d_avg),
        total_amount=_f(total),
        fees=0.0,
        taxes=0.0,
        transaction_date=tx_date,
        notes=notes,
        sector=sector or (item.sector if item else None),
        asset_id=resolved_asset_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    db.refresh(item)

    _log_runtime_consultation(db, symbol, tx.id, "quantity_valuation", "execute_initial_position")

    result = {
        "transaction_id": tx.id,
        "type": "INITIAL_POSITION",
        "symbol": symbol,
        "shares": tx.shares,
        "price_per_share": tx.price_per_share,
        "total_amount": tx.total_amount,
        "transaction_date": tx.transaction_date.isoformat() + "Z",
        "notes": tx.notes,
        "holding": {
            "shares": item.shares,
            "avg_cost": item.avg_cost,
            "sector": item.sector,
        },
    }
    _observe_transaction_execution_eligibility(db, symbol, "INITIAL_POSITION")
    return result


# ─── QUANTITY_CORRECTION ──────────────────────────────────────────────────────

def execute_quantity_correction(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    symbol: str,
    shares_delta: float,
    price_per_share: float,
    transaction_date: datetime | None = None,
    notes: str | None = None,
) -> dict:
    """Apply a share-count correction to an existing position.

    Records a QUANTITY_CORRECTION transaction so the snapshot engine can
    classify the equity change as a balance-sheet event and exclude it from
    investment_return_pct.

    shares_delta may be positive (adding missing shares) or negative
    (removing erroneously recorded shares). avg_cost is recalculated on
    additions using a weighted average.

    Does NOT affect cash_balance — purely a record-keeping correction.
    """
    if shares_delta == 0:
        raise ValueError("shares_delta must be non-zero")
    if price_per_share <= 0:
        raise ValueError("price_per_share must be positive")
    if resolve_portfolio_reference(db, portfolio_id, ws_id) is None:
        raise ValueError(f"Portfolio {portfolio_id} not found")

    d_delta = _d(shares_delta)
    d_price = _d(price_per_share)
    tx_date = transaction_date or datetime.utcnow()

    item = db.query(PortfolioItem).filter_by(portfolio_id=portfolio_id, symbol=symbol).first()
    if not item:
        raise ValueError(f"No holding found for {symbol} in portfolio {portfolio_id}")

    resolved_asset_id = _resolve_write_time_asset_id(db, symbol)
    if resolved_asset_id is not None and item.asset_id is None:
        item.asset_id = resolved_asset_id

    old_shares = _d(item.shares)
    new_shares = old_shares + d_delta
    if new_shares < 0:
        raise ValueError(
            f"Correction would result in negative shares: {_f(old_shares)} + {_f(d_delta)}"
        )

    if d_delta > 0:
        old_cost = _d(item.avg_cost)
        new_avg  = (old_shares * old_cost + d_delta * d_price) / new_shares
        item.avg_cost = _f(new_avg)

    item.shares = _f(new_shares)

    tx = Transaction(
        workspace_id=ws_id,
        portfolio_id=portfolio_id,
        symbol=symbol,
        transaction_type="QUANTITY_CORRECTION",
        shares=_f(abs(d_delta)),
        price_per_share=_f(d_price),
        total_amount=_f(abs(d_delta) * d_price),
        fees=0.0,
        taxes=0.0,
        transaction_date=tx_date,
        notes=notes or f"Quantity correction: {'+' if d_delta > 0 else ''}{_f(d_delta)} shares",
        sector=item.sector,
        asset_id=resolved_asset_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    db.refresh(item)

    return {
        "transaction_id": tx.id,
        "type": "QUANTITY_CORRECTION",
        "symbol": symbol,
        "shares_delta": shares_delta,
        "price_per_share": tx.price_per_share,
        "total_amount": tx.total_amount,
        "transaction_date": tx.transaction_date.isoformat() + "Z",
        "notes": tx.notes,
        "holding": {
            "shares": item.shares,
            "avg_cost": item.avg_cost,
            "sector": item.sector,
        },
    }


# ─── INITIAL_CASH ─────────────────────────────────────────────────────────────

def execute_initial_cash(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    amount: float,
    currency: str = "THB",
    transaction_date: datetime | None = None,
    notes: str | None = None,
) -> dict:
    """Set the starting cash for onboarding. Adds to (does not replace) cash balance."""
    if amount <= 0:
        raise ValueError("Initial cash amount must be positive")

    d_amount = _d(amount)
    tx_date  = transaction_date or datetime.utcnow()

    portfolio = resolve_portfolio_reference(db, portfolio_id, ws_id)
    if not portfolio:
        raise ValueError("Portfolio not found")

    portfolio.cash_balance = _f(_d(portfolio.cash_balance) + d_amount)

    tx = Transaction(
        workspace_id=ws_id,
        portfolio_id=portfolio_id,
        symbol=None,
        transaction_type="INITIAL_CASH",
        shares=None,
        price_per_share=None,
        total_amount=_f(d_amount),
        fees=0.0,
        taxes=0.0,
        currency=currency,
        exchange_rate=1.0,
        transaction_date=tx_date,
        notes=notes or "Initial cash balance",
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return {
        "transaction_id": tx.id,
        "type": "INITIAL_CASH",
        "symbol": None,
        "amount": tx.total_amount,
        "total_amount": tx.total_amount,
        "transaction_date": tx.transaction_date.isoformat() + "Z",
        "notes": tx.notes,
        "cash_balance": portfolio.cash_balance,
    }


# ─── POSITION_CONVERSION (BANPU-WP4) ───────────────────────────────────────
#
# The only authorized atomic write path for a whole-position predecessor-to-
# successor conversion (BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md
# §9; BANPU-WP4 Work Package Plan §3.2). Service-only — no CLI or public
# endpoint calls this (CLI wiring is BANPU-WP7 work; C-13).
#
# Registry preparation (asset_registry.prepare_position_conversion_registry,
# E0) is a distinct, idempotent service act performed by the caller BEFORE
# this function is invoked — this function only validates the registry
# state E0 established (E3); it never prepares registry state itself
# (PD-WP4-1).
#
# E1-E13 execute inside exactly one database transaction: no intermediate
# db.commit() occurs between the portfolio lock and the final commit at E13,
# and any exception anywhere in that span rolls the entire unit back,
# leaving no transaction row and no materialized-state mutation. A matching
# retry at E8-R is the one non-exception early exit; it explicitly rolls
# back (rather than commits) before returning, since it performs no writes
# of its own (BANPU-WP4 Retry-Order Work Package Plan Amendment §3.2).


class PositionConversionError(ValueError):
    """Raised by execute_position_conversion() when the request cannot
    proceed: invalid payload, registry invariant violated, stale optimistic
    expectation, absent/ambiguous holding, or a conflicting duplicate.
    Never raised for a matching duplicate — that returns an
    ``already_applied`` no-op result instead (C-6)."""


def _position_conversion_asset_ids(conversion_payload: dict) -> tuple[int, int]:
    """Read only the authoritative asset IDs needed for registry resolution."""
    if not isinstance(conversion_payload, dict):
        raise PositionConversionError("POSITION_CONVERSION payload must be an object")
    predecessor = conversion_payload.get("predecessor")
    successor = conversion_payload.get("successor")
    if not isinstance(predecessor, dict) or not isinstance(successor, dict):
        raise PositionConversionError(
            "POSITION_CONVERSION payload predecessor and successor must be objects"
        )
    predecessor_asset_id = predecessor.get("asset_id")
    successor_asset_id = successor.get("asset_id")
    for path, value in (
        ("predecessor.asset_id", predecessor_asset_id),
        ("successor.asset_id", successor_asset_id),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise PositionConversionError(f"{path} must be a positive integer")
    return predecessor_asset_id, successor_asset_id


def _canonical_conversion_payload(
    conversion_payload: dict,
    *,
    predecessor_symbol: str,
    successor_symbol: str,
    predecessor_provider_symbol: str,
) -> dict:
    """Assemble the sole persisted payload with registry-authoritative labels."""
    canonical_payload = deepcopy(conversion_payload)
    canonical_payload["predecessor"]["symbol"] = predecessor_symbol
    canonical_payload["successor"]["symbol"] = successor_symbol
    quote_binding = canonical_payload.get("quote_binding")
    if not isinstance(quote_binding, dict):
        raise PositionConversionError("POSITION_CONVERSION payload quote_binding must be an object")
    quote_binding["predecessor_provider_symbol"] = predecessor_provider_symbol
    return canonical_payload


# BANPU-WP4-IIR-B1 (second-renewed correction): the frozen Design's
# authoritative absolute storage tolerance for the legacy floating-point
# transaction columns (BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md
# §"Top-level shares, price_per_share, total_amount, fees, and taxes match
# their payload projections within the authoritative absolute storage
# tolerance of 0.000001 per field"). Payload arithmetic itself remains exact
# Decimal arithmetic — this tolerance exists only for the legacy float
# columns, and is exactly the precision _f()/_QUANT already write at.
_NUMERIC_PROJECTION_TOLERANCE = Decimal("0.000001")


def _within_numeric_projection_tolerance(actual: float | None, expected: Decimal) -> bool:
    """True iff a stored legacy float column is within the Design's
    authorized 0.000001 absolute tolerance of its exact Decimal payload
    projection. The boundary is inclusive ("within"). A missing or
    non-numeric stored value fails closed rather than raising."""
    if actual is None:
        return False
    try:
        actual_decimal = _d(actual)
    except Exception:
        return False
    return abs(actual_decimal - expected) <= _NUMERIC_PROJECTION_TOLERANCE


def _validate_conversion_transaction_projection(
    tx: Transaction,
    *,
    ws_id: int,
    portfolio_id: int,
    predecessor_asset_id: int,
    predecessor_symbol: str,
    successor_asset_id: int,
    successor_symbol: str,
    transaction_date: datetime,
    payload,
) -> None:
    """Fail closed unless a row is the exact projection of its typed payload.

    Identity fields (ownership, type, asset identity, symbols, dates) are
    compared for exact equality. The five legacy float columns governed by
    the Design's 0.000001 absolute storage tolerance (shares,
    price_per_share, total_amount, fees, taxes) are compared within that
    tolerance instead of by exact float equality (WP4-IIR-B1 second-renewed
    correction) — a numerically valid legacy projection must not be
    rejected merely because it predates this convention or differs from a
    freshly `_f()`-quantized recomputation by less than the authorized
    tolerance.
    """
    cash = payload.cash_in_lieu
    expected_fees = cash.fees if cash else Decimal("0")
    expected_taxes = cash.taxes if cash else Decimal("0")
    expected_price = payload.basis.carried_to_successor / payload.successor.shares_received

    exact_invariant_values = (
        ("workspace identity", tx.workspace_id, ws_id),
        ("portfolio identity", tx.portfolio_id, portfolio_id),
        ("transaction type", tx.transaction_type, "POSITION_CONVERSION"),
        ("predecessor asset identity", tx.asset_id, predecessor_asset_id),
        ("canonical symbol", tx.symbol, predecessor_symbol),
        ("transaction date", tx.transaction_date, transaction_date),
        ("payload predecessor asset identity", payload.predecessor.asset_id, predecessor_asset_id),
        ("payload predecessor symbol", payload.predecessor.symbol, predecessor_symbol),
        ("payload successor asset identity", payload.successor.asset_id, successor_asset_id),
        ("payload successor symbol", payload.successor.symbol, successor_symbol),
        ("payload transition date", payload.dates.valuation_transition_date, transaction_date.date()),
    )
    for name, actual, expected in exact_invariant_values:
        if actual != expected:
            raise PositionConversionError(
                f"POSITION_CONVERSION transaction {name} invariant failed: "
                f"actual={actual!r} expected={expected!r}"
            )

    numeric_projection_values = (
        ("shares", tx.shares, payload.successor.shares_received),
        ("price_per_share", tx.price_per_share, expected_price),
        ("total_amount", tx.total_amount, payload.basis.carried_to_successor),
        ("fees", tx.fees, expected_fees),
        ("taxes", tx.taxes, expected_taxes),
    )
    for name, actual, expected in numeric_projection_values:
        if not _within_numeric_projection_tolerance(actual, expected):
            raise PositionConversionError(
                f"POSITION_CONVERSION transaction {name} invariant failed: "
                f"actual={actual!r} expected={expected!r} "
                f"tolerance={_NUMERIC_PROJECTION_TOLERANCE}"
            )


def execute_position_conversion(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    conversion_payload: dict,
    *,
    currency: str = "THB",
    exchange_rate: float = 1.0,
    notes: str | None = None,
) -> dict:
    """Materialize one whole-position POSITION_CONVERSION.

    ``conversion_payload`` is the caller-provided version-1 payload template
    (BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md §6.2) — the same
    typed contract WP1's canonicalizer and WP2's replay already consume, so
    this service introduces no second payload-assembly algorithm and no
    competing accounting identity (mirrors the MINOR-1 rejected-alternative
    reasoning: one canonical implementation per rule, ADR-004). The
    payload's own ``predecessor.shares_surrendered`` and ``basis.before``
    fields ARE the caller's optimistic expectation checked at E6 — no
    separate "expected_*" parameters are needed.

    Runtime order (BANPU-WP4 Retry-Order Work Package Plan Amendment §3.2,
    independently reapproved — refines the original Plan §3.2's unqualified
    E1-E13 order at the retry-disposition point only; E0-E4, E9-E13, and the
    sole successful commit boundary are otherwise unchanged):

      E1  lock the portfolio row (workspace/portfolio ownership, the
          primary serialization boundary) — this function's first database
          access; every exit below is inside the rollback-protected
          boundary this establishes (WP4-IIR-B4).
      --  read authoritative predecessor/successor asset IDs, then
          registry-resolve their identity, symbols, and predecessor
          provider symbol; asset IDs remain authoritative and the
          caller-supplied payload symbols/predecessor provider symbol are
          never trusted for lookup or persistence (WP4-IIR-B2, second-
          renewed correction)
      --  assemble, parse, and validate the canonical version-1 payload
      E2  lock the relevant existing PortfolioItem rows, using the
          registry-resolved symbols for the legacy-symbol fallback match
      E3  validate registry invariants (asset_registry), including
          predecessor provider symbol identity — fail closed
      E4  derive transaction_date solely from the payload's timezone-free
          valuation_transition_date (NEW-MINOR-A)
      E7  MINOR-1 pre-use gate (fingerprint serialization is now
          context-independent; see transaction_canonicalizer.py)
      E8-R canonical retry preflight: a read-only lookup by exact canonical
          conversion identity. No prior row is not a retry — E5/E6 remain
          mandatory. Exactly one valid prior row has its stored
          conversion_payload reparsed and its fingerprint regenerated with
          the sole canonical algorithm; exact equality with the incoming
          fingerprint is a matching retry (bypasses only E5/E6, no
          mutation, no-op, ``already_applied``), inequality is a
          conflicting retry (bypasses only E5/E6, no mutation, hard
          failure). A malformed or ambiguous existing row establishes
          neither and fails closed. Current successor materialized state
          is never a predicate (RTO-13).
      E5  locate the predecessor holding by asset ID with the controlled
          registry-resolved-symbol fallback; zero or multiple matches fail
          closed
      E6  verify optimistic predecessor quantity/basis expectations
      E9  insert the append-only conversion transaction row
      E10 remove the predecessor materialization
      E11 create or merge the successor materialization
      E12 apply the admitted cash-in-lieu cash leg
      E13 assert final invariants — predecessor removal, successor shares,
          successor basis, successor identity, and cash; reparse the
          pending row's actual persisted conversion_payload and
          refingerprint it against the canonically assembled payload
          (WP4-IIR-B5, second-renewed correction); revalidate registry
          provider identity from that persisted payload — then commit;
          the only commit boundary

    Ordering rules preserved exactly: E7 precedes E8-R; E3 and E6 precede
    every first-application write; E9 precedes E10-E12; E13 is the sole
    commit boundary. Every exit — success, no-op, conflict, or failure —
    deterministically finishes this function's one transaction and releases
    every lock it took (RTO-10, RTO-11, RTO-12).
    """
    if db.in_transaction():
        raise PositionConversionError(
            "execute_position_conversion requires an idle Session; "
            "caller-owned transaction left untouched"
        )

    try:
        # E1 — lock the portfolio row. First database access; the
        # surrounding try/except is this function's sole rollback boundary,
        # covering every exit from this point on (WP4-IIR-B4).
        portfolio = (
            db.query(Portfolio)
            .filter(Portfolio.id == portfolio_id, Portfolio.workspace_id == ws_id)
            .with_for_update()
            .one_or_none()
        )
        if portfolio is None:
            raise PositionConversionError(f"Portfolio {portfolio_id} not found")

        # Read only the authoritative IDs needed to resolve registry symbols.
        # Full payload parsing follows assembly of the canonical symbol labels.
        predecessor_asset_id, successor_asset_id = _position_conversion_asset_ids(
            conversion_payload
        )

        # Registry-resolved predecessor/successor identity and symbols
        # (WP4-IIR-B2). Asset IDs remain authoritative; the caller-supplied
        # payload.predecessor.symbol / payload.successor.symbol are never
        # used to locate holdings, write the transaction symbol, or
        # relabel the successor — only the registry's own display_symbol
        # (falling back to canonical_symbol) is used for every
        # persisted/lookup symbol below.
        predecessor_asset = asset_registry.get_asset(db, predecessor_asset_id)
        if predecessor_asset is None:
            raise PositionConversionError(f"no asset with asset_id={predecessor_asset_id}")
        successor_asset = asset_registry.get_asset(db, successor_asset_id)
        if successor_asset is None:
            raise PositionConversionError(f"no asset with asset_id={successor_asset_id}")
        if predecessor_asset.id == successor_asset.id:
            raise PositionConversionError("predecessor and successor asset_id must be distinct")
        predecessor_symbol = predecessor_asset.display_symbol or predecessor_asset.canonical_symbol
        successor_symbol = successor_asset.display_symbol or successor_asset.canonical_symbol
        # Registry-resolved predecessor provider symbol (WP4-IIR-B2
        # second-renewed correction): derived from the predecessor's own
        # retired PROVIDER_SYMBOL identifier row, never trusted from the
        # caller-supplied payload.quote_binding.predecessor_provider_symbol
        # text.
        predecessor_provider_symbol = asset_registry.resolve_predecessor_provider_symbol(
            db, predecessor_asset_id
        )

        canonical_payload = _canonical_conversion_payload(
            conversion_payload,
            predecessor_symbol=predecessor_symbol,
            successor_symbol=successor_symbol,
            predecessor_provider_symbol=predecessor_provider_symbol,
        )
        parsed = parse_position_conversion_payload(canonical_payload)
        if not parsed.is_valid or parsed.value is None:
            raise PositionConversionError(
                "invalid POSITION_CONVERSION payload: "
                + "; ".join(f"{e.code}:{e.path}:{e.message}" for e in parsed.errors)
            )
        payload = parsed.value

        # E2 — lock the portfolio's PortfolioItem rows plausibly relevant to
        # either side of the conversion (existing rows only; a not-yet-
        # existing successor has nothing to lock, matching every other
        # execute_* function's behavior for a brand-new symbol). The
        # legacy-symbol fallback uses the registry-resolved symbols, not
        # the caller-supplied payload symbols (WP4-IIR-B2).
        candidate_items = (
            db.query(PortfolioItem)
            .filter(
                PortfolioItem.portfolio_id == portfolio_id,
                (
                    (PortfolioItem.asset_id == predecessor_asset_id)
                    | (PortfolioItem.symbol == predecessor_symbol)
                    | (PortfolioItem.asset_id == successor_asset_id)
                    | (PortfolioItem.symbol == successor_symbol)
                ),
            )
            .with_for_update()
            .all()
        )

        # E3 — registry invariants, fail-closed, before any write.
        asset_registry.validate_position_conversion_registry_state(
            db, predecessor_asset_id, successor_asset_id,
            payload.successor.provider_symbol,
            payload.quote_binding.predecessor_provider_symbol,
        )

        # E4 — transaction_date derived solely from the payload's
        # timezone-free valuation_transition_date (NEW-MINOR-A). The typed
        # PositionConversionDates.valuation_transition_date field is a
        # `date`, never a `datetime` — the frozen canonicalizer's
        # date-only parser (`_PayloadReader.date`) already fails closed on
        # any offset-bearing or time-bearing authoring string before this
        # point is ever reached (NMA-I3), so this construction only adds
        # the canonical naive-midnight representation with no host-clock,
        # session-timezone, or UTC participation of its own (NMA-I4).
        transition_date = payload.dates.valuation_transition_date
        if not isinstance(transition_date, date_cls) or isinstance(transition_date, datetime):
            raise PositionConversionError(
                "valuation_transition_date must be a naive calendar date"
            )
        transaction_date = datetime.combine(transition_date, time.min)
        if transaction_date.tzinfo is not None or transaction_date.time() != time.min:
            raise PositionConversionError(
                "derived transaction_date must be naive midnight"
            )

        # E7 — MINOR-1 pre-use gate. Fingerprint idempotency below is
        # permitted to run because transaction_canonicalizer.py's Decimal
        # serialization is now context-independent (MINOR-1 correction) —
        # a 64-character SHA-256 hex digest is not a value that particular
        # defect could still be masking.
        fingerprint = payload.fingerprint
        if not isinstance(fingerprint, str) or len(fingerprint) != 64:
            raise PositionConversionError("payload fingerprint is not a valid SHA-256 digest")

        # E8-R — canonical retry preflight (BANPU-WP4 Retry-Order Work
        # Package Plan Amendment §3.2, independently reapproved). Read-only
        # lookup by exact canonical conversion identity: (portfolio_id,
        # predecessor asset_id, conversion type, transaction_date) is
        # exactly the key the WP1 partial unique index enforces. `.all()`
        # rather than `.one_or_none()` so a zero-or-multiple existing-row
        # anomaly is itself classified as invalid state (RTO-9) instead of
        # raising an uncontrolled SQLAlchemy error.
        existing_rows = (
            db.query(Transaction)
            .filter(
                Transaction.portfolio_id == portfolio_id,
                Transaction.transaction_type == "POSITION_CONVERSION",
                Transaction.asset_id == predecessor_asset_id,
                Transaction.transaction_date == transaction_date,
            )
            .all()
        )
        if len(existing_rows) > 1:
            # Invalid/ambiguous existing state: zero-or-multiple where
            # uniqueness is required establishes neither a matching nor a
            # conflicting disposition. Not a repair opportunity — fail
            # closed with no business mutation (RTO-9).
            raise PositionConversionError(
                "ambiguous existing POSITION_CONVERSION state for "
                f"portfolio_id={portfolio_id} predecessor asset_id={predecessor_asset_id} "
                f"transaction_date={transaction_date}: {len(existing_rows)} rows"
            )
        existing = existing_rows[0] if existing_rows else None
        if existing is not None:
            # The existing row's stored canonical conversion_payload is
            # reparsed and its fingerprint regenerated from that payload
            # with the sole canonical algorithm — never a detached/stored
            # digest, caller-supplied digest, partial comparison, or
            # alternate fingerprint (RTO-5, RTO-6).
            existing_parsed = parse_position_conversion_payload(existing.conversion_payload)
            if not existing_parsed.is_valid or existing_parsed.value is None:
                # Malformed/noncanonical stored payload: invalid existing
                # state establishes neither match nor conflict authority.
                # Fail closed, no business mutation, no repair (RTO-9).
                raise PositionConversionError(
                    "existing POSITION_CONVERSION row transaction_id="
                    f"{existing.id} has an invalid stored conversion_payload"
                )
            existing_payload = existing_parsed.value
            try:
                _validate_conversion_transaction_projection(
                    existing,
                    ws_id=ws_id,
                    portfolio_id=portfolio_id,
                    predecessor_asset_id=predecessor_asset_id,
                    predecessor_symbol=predecessor_symbol,
                    successor_asset_id=successor_asset_id,
                    successor_symbol=successor_symbol,
                    transaction_date=transaction_date,
                    payload=existing_payload,
                )
                asset_registry.validate_position_conversion_registry_state(
                    db,
                    existing_payload.predecessor.asset_id,
                    existing_payload.successor.asset_id,
                    existing_payload.successor.provider_symbol,
                    existing_payload.quote_binding.predecessor_provider_symbol,
                )
            except Exception as exc:
                raise PositionConversionError(
                    "existing POSITION_CONVERSION row transaction_id="
                    f"{existing.id} is inconsistent with canonical identity/payload"
                ) from exc
            if existing_payload.fingerprint == fingerprint:
                # Matching retry (RTO-3, RTO-7): bypass only E5/E6. No
                # business mutation, repair, reconciliation, replay, or
                # snapshot action. Current successor materialized state is
                # never consulted (RTO-13). Deterministically finish this
                # read-only transaction and release every lock before
                # returning (RTO-10). The id is captured BEFORE rollback —
                # Session.rollback() expires ORM objects by default, so an
                # attribute access on `existing` after rollback would
                # trigger a lazy-load that reopens a new transaction.
                existing_transaction_id = existing.id
                db.rollback()
                return {
                    "status": "already_applied",
                    "transaction_id": existing_transaction_id,
                    "type": "POSITION_CONVERSION",
                }
            # Conflicting retry (RTO-4, RTO-8): bypass only E5/E6. No
            # business mutation or repair. The outer except below
            # deterministically rolls back and releases every lock before
            # this propagates (RTO-11).
            raise PositionConversionError(
                "conflicting POSITION_CONVERSION already exists for "
                f"portfolio_id={portfolio_id} predecessor asset_id={predecessor_asset_id} "
                f"transaction_date={transaction_date}"
            )

        # No prior canonical conversion row: this is a first application,
        # not a retry. E5 and E6 remain mandatory and precede every write
        # (RTO-2).

        # E5 — locate the predecessor holding by asset ID with the
        # controlled registry-resolved-symbol fallback; zero or multiple
        # matches fail closed.
        predecessor_candidates = {
            item.id: item for item in candidate_items
            if item.asset_id == predecessor_asset_id
            or item.symbol == predecessor_symbol
        }
        if len(predecessor_candidates) == 0:
            raise PositionConversionError(
                f"no predecessor holding found for asset_id={predecessor_asset_id} "
                f"symbol={predecessor_symbol!r} in portfolio {portfolio_id}"
            )
        if len(predecessor_candidates) > 1:
            raise PositionConversionError(
                f"ambiguous predecessor holding for asset_id={predecessor_asset_id} "
                f"symbol={predecessor_symbol!r} in portfolio {portfolio_id}"
            )
        predecessor_item = next(iter(predecessor_candidates.values()))

        # E6 — optimistic quantity/basis expectations, mirroring the WP2
        # replay tolerances exactly (exact share equality, THB 0.01 basis
        # tolerance) so live materialization and replay reconcile (EQ-1).
        held_shares = _d(predecessor_item.shares)
        if held_shares != payload.predecessor.shares_surrendered:
            raise PositionConversionError(
                f"predecessor shares mismatch: held={held_shares} "
                f"expected={payload.predecessor.shares_surrendered}"
            )
        held_basis = held_shares * _d(predecessor_item.avg_cost)
        if abs(held_basis - payload.basis.before) > Decimal("0.01"):
            raise PositionConversionError(
                f"predecessor basis mismatch: held={held_basis} "
                f"expected={payload.basis.before}"
            )

        # Resolve the successor merge target (existing holding or none)
        # before inserting the transaction row, so the row's own `sector`
        # column reflects the final materialized sector (mirrors every
        # other execute_* function's `sector=sector or item.sector`
        # convention).
        successor_candidates = {
            item.id: item for item in candidate_items
            if item.id not in predecessor_candidates
            and (item.asset_id == successor_asset_id or item.symbol == successor_symbol)
        }
        if len(successor_candidates) > 1:
            raise PositionConversionError(
                f"ambiguous successor holding for asset_id={successor_asset_id} "
                f"symbol={successor_symbol!r} in portfolio {portfolio_id}"
            )
        successor_item = next(iter(successor_candidates.values()), None)
        if (
            successor_item is not None
            and successor_item.asset_id is not None
            and successor_item.asset_id != successor_asset_id
        ):
            raise PositionConversionError(
                f"successor holding asset_id={successor_item.asset_id} conflicts with "
                f"payload successor asset_id={successor_asset_id}"
            )

        predecessor_sector = predecessor_item.sector
        final_sector = (
            successor_item.sector if successor_item is not None and successor_item.sector
            else predecessor_sector
        )

        received_shares = payload.successor.shares_received
        carried_basis = payload.basis.carried_to_successor
        avg_cost = carried_basis / received_shares
        fees = payload.cash_in_lieu.fees if payload.cash_in_lieu else Decimal("0")
        taxes = payload.cash_in_lieu.taxes if payload.cash_in_lieu else Decimal("0")
        net_cash = payload.cash_in_lieu.net_cash if payload.cash_in_lieu else Decimal("0")

        # E9 — insert the append-only conversion transaction row. The
        # registry-resolved predecessor symbol is stored, never the
        # caller-supplied payload symbol (WP4-IIR-B2).
        tx = Transaction(
            workspace_id=ws_id,
            portfolio_id=portfolio_id,
            symbol=predecessor_symbol,
            transaction_type="POSITION_CONVERSION",
            shares=_f(received_shares),
            price_per_share=_f(avg_cost),
            total_amount=_f(carried_basis),
            fees=_f(fees),
            taxes=_f(taxes),
            currency=currency,
            exchange_rate=exchange_rate,
            transaction_date=transaction_date,
            notes=notes,
            sector=final_sector,
            asset_id=predecessor_asset_id,
            conversion_payload=canonical_payload,
        )
        db.add(tx)

        # E10 — remove the predecessor materialization. shares_surrendered
        # equals the entire predecessor holding (canonicalizer invariant +
        # E6 exact-equality check above), so full removal is correct.
        predecessor_item_id = predecessor_item.id
        db.delete(predecessor_item)

        # E11 — create or merge the successor materialization, using the
        # registry-resolved successor symbol, never the caller-supplied
        # payload symbol (WP4-IIR-B2).
        if successor_item is not None:
            existing_shares = _d(successor_item.shares)
            existing_basis = existing_shares * _d(successor_item.avg_cost)
            combined_shares = existing_shares + received_shares
            combined_basis = existing_basis + carried_basis
            successor_item.shares = _f(combined_shares)
            successor_item.avg_cost = _f(combined_basis / combined_shares)
            successor_item.symbol = successor_symbol
            if successor_item.asset_id is None:
                successor_item.asset_id = successor_asset_id
            if not successor_item.sector:
                successor_item.sector = predecessor_sector
            final_successor_shares = combined_shares
            final_successor_basis = combined_basis
        else:
            successor_item = PortfolioItem(
                workspace_id=ws_id,
                portfolio_id=portfolio_id,
                symbol=successor_symbol,
                shares=_f(received_shares),
                avg_cost=_f(avg_cost),
                sector=predecessor_sector,
                asset_id=successor_asset_id,
            )
            db.add(successor_item)
            final_successor_shares = received_shares
            final_successor_basis = carried_basis

        # E12 — admitted cash-in-lieu cash leg only; unchanged without it.
        cash_before = _d(portfolio.cash_balance)
        portfolio.cash_balance = _f(cash_before + net_cash)

        # E13 — final invariants, then the sole commit boundary.
        # WP4-IIR-B5: the refreshed successor basis is recomputed from its
        # post-write shares × avg_cost and asserted against the expected
        # carried/combined basis, using the same THB 0.01 tolerance as E6 —
        # a corrupted refreshed avg_cost is no longer fail-open.
        db.flush()
        db.refresh(successor_item)
        if db.query(PortfolioItem).filter(PortfolioItem.id == predecessor_item_id).first() is not None:
            raise PositionConversionError("post-write predecessor removal invariant failed")
        if _d(successor_item.shares) != final_successor_shares:
            raise PositionConversionError("post-write successor shares invariant failed")
        refreshed_basis = _d(successor_item.shares) * _d(successor_item.avg_cost)
        if abs(refreshed_basis - final_successor_basis) > Decimal("0.01"):
            raise PositionConversionError("post-write successor basis invariant failed")
        if successor_item.asset_id != successor_asset_id:
            raise PositionConversionError("post-write successor identity invariant failed")
        if _f(cash_before + net_cash) != portfolio.cash_balance:
            raise PositionConversionError("post-write cash invariant failed")

        # WP4-IIR-B5 (second-renewed correction): validate the actual
        # pending row's persisted conversion_payload, not the pre-write
        # in-memory `payload` typed object. `tx.conversion_payload` is read
        # exactly as currently attached to the ORM object at this point —
        # no db.refresh(tx) — so a post-flush, pre-commit mutation of that
        # JSON column (in-process or otherwise) is detected here rather
        # than committed fail-open. Reparsed with the sole canonical
        # parser and refingerprinted with the sole canonical algorithm; a
        # detached/stored/alternate fingerprint is never trusted.
        persisted_parsed = parse_position_conversion_payload(tx.conversion_payload)
        if not persisted_parsed.is_valid or persisted_parsed.value is None:
            raise PositionConversionError(
                "post-write conversion_payload is not a canonically valid "
                "POSITION_CONVERSION payload"
            )
        persisted_payload = persisted_parsed.value
        if persisted_payload.fingerprint != fingerprint:
            raise PositionConversionError(
                "post-write conversion_payload fingerprint does not match the "
                "canonical payload assembled for this conversion"
            )

        _validate_conversion_transaction_projection(
            tx,
            ws_id=ws_id,
            portfolio_id=portfolio_id,
            predecessor_asset_id=predecessor_asset_id,
            predecessor_symbol=predecessor_symbol,
            successor_asset_id=successor_asset_id,
            successor_symbol=successor_symbol,
            transaction_date=transaction_date,
            payload=persisted_payload,
        )
        asset_registry.validate_position_conversion_registry_state(
            db,
            predecessor_asset_id,
            successor_asset_id,
            persisted_payload.successor.provider_symbol,
            persisted_payload.quote_binding.predecessor_provider_symbol,
        )

        result = {
            "status": "applied",
            "transaction_id": tx.id,
            "type": "POSITION_CONVERSION",
            "predecessor_asset_id": predecessor_asset_id,
            "successor_asset_id": successor_asset_id,
            "successor_symbol": successor_symbol,
            "shares_received": _f(received_shares),
            "avg_cost": _f(avg_cost),
            "basis_carried": _f(carried_basis),
            "cash_balance": _f(cash_before + net_cash),
            "transaction_date": transaction_date.isoformat() + "Z",
            "fingerprint": fingerprint,
            "notes": notes,
        }

        db.commit()
    except Exception:
        db.rollback()
        raise

    return result
