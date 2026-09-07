"""Net Worth Change Attribution — Level-1 balance-sheet component attribution.

Answers "why did recorded Net Worth change between two complete historical
points" strictly at the balance-sheet component level:

    N(d) = Investment assets(d) + External cash(d) - Total liabilities(d)

    delta_N = [investment_assets(end) - investment_assets(start)]
            + [external_cash(end) - external_cash(start)]
            + [total_liabilities(start) - total_liabilities(end)]

This module does not infer market return, investment contribution, income,
spending, debt repayment, or borrowing, and it never pairs a cash-side
INVESTMENT_TRANSFER with a Portfolio DEPOSIT/WITHDRAW (ADR-012). It reuses
the existing historical authorities exclusively:

  - PortfolioSnapshot.total_value for investment assets
  - services.cash_account_ledger.cash_balance_as_of for external cash
  - services.liability_balance.liability_balance_as_of for liabilities

No persistence, no schema, no new reconstruction logic. See ADR-013.
"""
from __future__ import annotations

from datetime import date as date_cls, datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from models.database import (
    CashAccount,
    CashAccountTransaction,
    Liability,
    LiabilityBalanceObservation,
    Portfolio,
    PortfolioSnapshot,
)
from services.cash_account_ledger import cash_balance_as_of
from services.liability_balance import liability_balance_as_of

# Stored snapshot precision — an AVAILABLE result must reconcile within this.
RECONCILIATION_TOLERANCE = 0.0001

# Lifecycle calendar-date authority, frozen to match the existing Net Worth
# History journey (frontend/lib/{wealthHistory,totalAssetsHistory,
# totalLiabilitiesHistory}.ts's `createdDateKey`, an Asia/Bangkok
# Intl.DateTimeFormat). Not user-selectable, not machine-local.
_LIFECYCLE_TZ = ZoneInfo("Asia/Bangkok")


def lifecycle_date(created_at: datetime) -> date_cls:
    """Asia/Bangkok calendar date for a lifecycle timestamp — the same
    authority Net Worth History already uses to decide whether a Portfolio /
    CashAccount / Liability is "expected" as of a given date.

    `Portfolio.created_at` / `CashAccount.created_at` / `Liability.created_at`
    are all `Column(DateTime, default=datetime.utcnow)` — naive timestamps
    whose wall-clock value IS UTC (models/database.py). A naive value is
    therefore interpreted as UTC before converting; a tz-aware value is
    converted as-is.
    """
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    return created_at.astimezone(_LIFECYCLE_TZ).date()


# ─── Pure arithmetic (no DB) ────────────────────────────────────────────────

def liability_impact(start_liabilities: float, end_liabilities: float) -> float:
    """A liability decline is a positive Net Worth impact."""
    return start_liabilities - end_liabilities


def component_attribution(
    start_investment_assets: float,
    end_investment_assets: float,
    start_external_cash: float,
    end_external_cash: float,
    start_total_liabilities: float,
    end_total_liabilities: float,
) -> dict[str, float]:
    return {
        "investment_assets_change": end_investment_assets - start_investment_assets,
        "external_cash_change": end_external_cash - start_external_cash,
        "liability_impact": liability_impact(start_total_liabilities, end_total_liabilities),
    }


def net_worth_change(start_net_worth: float, end_net_worth: float) -> float:
    return end_net_worth - start_net_worth


def reconciliation_difference(net_worth_change_value: float, components: dict[str, float]) -> float:
    return net_worth_change_value - sum(components.values())


def _endpoint_totals(values: dict[str, float]) -> tuple[float, float]:
    """(total_assets, net_worth) for one already-resolved endpoint composition."""
    total_assets = values["investment_assets"] + values["external_cash"]
    net_worth = total_assets - values["total_liabilities"]
    return total_assets, net_worth


def build_available_result(
    start_date: str,
    end_date: str,
    start_values: dict[str, float],
    end_values: dict[str, float],
) -> dict | None:
    """Pure — start_values/end_values are already-resolved evidence:
    {"investment_assets", "external_cash", "total_liabilities"} (floats).

    Returns None when the reconciliation guard rejects the composition
    (Section 4): the difference between the independently-computed Net
    Worth delta and the summed components exceeds RECONCILIATION_TOLERANCE.
    """
    start_total_assets, start_net_worth = _endpoint_totals(start_values)
    end_total_assets, end_net_worth = _endpoint_totals(end_values)

    components = component_attribution(
        start_values["investment_assets"], end_values["investment_assets"],
        start_values["external_cash"], end_values["external_cash"],
        start_values["total_liabilities"], end_values["total_liabilities"],
    )
    nw_change = net_worth_change(start_net_worth, end_net_worth)
    recon_diff = reconciliation_difference(nw_change, components)

    if abs(recon_diff) > RECONCILIATION_TOLERANCE:
        return None

    return {
        "status": "AVAILABLE",
        "start_date": start_date,
        "end_date": end_date,
        "start": {
            "investment_assets": start_values["investment_assets"],
            "external_cash": start_values["external_cash"],
            "total_assets": start_total_assets,
            "total_liabilities": start_values["total_liabilities"],
            "net_worth": start_net_worth,
        },
        "end": {
            "investment_assets": end_values["investment_assets"],
            "external_cash": end_values["external_cash"],
            "total_assets": end_total_assets,
            "total_liabilities": end_values["total_liabilities"],
            "net_worth": end_net_worth,
        },
        "components": components,
        "net_worth_change": nw_change,
        "reconciliation_difference": recon_diff,
    }


# ─── Domain evidence resolution (DB) ────────────────────────────────────────
#
# Each resolver reuses the same historical authority the existing Net Worth
# History journey already reads (frontend/lib/{wealthHistory,
# totalAssetsHistory,totalLiabilitiesHistory}.ts) — this module never
# reconstructs Portfolio NAV, Cash ledger, or Liability state independently.
# Lifecycle expectation mirrors those modules' `createdKeyById` rule: an
# entity not yet created by the as-of date is simply not expected — using
# the same Asia/Bangkok lifecycle_date() authority those modules use.

def _created_on_or_before(created_at, as_of_date: str) -> bool:
    return lifecycle_date(created_at) <= date_cls.fromisoformat(as_of_date)


def _resolve_investment_assets(db: Session, workspace_id: int, as_of_date: str) -> tuple[float | None, bool]:
    """Sum of complete PortfolioSnapshot.total_value across every Portfolio
    expected to exist on as_of_date. Unavailable (None, False) unless every
    expected Portfolio has a snapshot dated exactly as_of_date — matching
    Investment Wealth History's own completeness rule (at least one expected
    Portfolio is required; zero portfolios is never a legitimate zero)."""
    portfolios = db.query(Portfolio).filter(Portfolio.workspace_id == workspace_id).all()
    expected = [p for p in portfolios if _created_on_or_before(p.created_at, as_of_date)]
    if not expected:
        return None, False

    snapshots = (
        db.query(PortfolioSnapshot)
        .filter(
            PortfolioSnapshot.workspace_id == workspace_id,
            PortfolioSnapshot.snapshot_date == as_of_date,
            PortfolioSnapshot.portfolio_id.in_([p.id for p in expected]),
        )
        .all()
    )
    if len(snapshots) != len(expected):
        return None, False
    return sum(s.total_value for s in snapshots), True


def _resolve_external_cash(db: Session, workspace_id: int, as_of_date: str) -> tuple[float | None, bool]:
    """Sum of cash_balance_as_of across every CashAccount (active and
    archived — archive state is never consulted) expected to exist on
    as_of_date. Zero expected accounts is a legitimate zero, matching
    Total Assets History's cash-side rule."""
    accounts = db.query(CashAccount).filter(CashAccount.workspace_id == workspace_id).all()
    expected = [a for a in accounts if _created_on_or_before(a.created_at, as_of_date)]

    total = 0.0
    contributing = 0
    for account in expected:
        baseline = account.baseline
        events = (
            (tx.transaction_type, tx.amount, tx.occurred_on)
            for tx in db.query(CashAccountTransaction)
            .filter(
                CashAccountTransaction.cash_account_id == account.id,
                CashAccountTransaction.workspace_id == workspace_id,
            )
            .all()
        ) if baseline is not None else ()
        balance = cash_balance_as_of(
            baseline.effective_on if baseline is not None else None,
            baseline.observed_balance if baseline is not None else None,
            events,
            as_of_date,
        )
        if balance is not None:
            contributing += 1
            total += balance

    complete = contributing == len(expected)
    return (total if complete else None), complete


def _resolve_total_liabilities(db: Session, workspace_id: int, as_of_date: str) -> tuple[float | None, bool]:
    """Sum of liability_balance_as_of across every Liability (active and
    archived) expected to exist on as_of_date. Zero expected liabilities is
    a legitimate zero, matching Total Liabilities History's rule."""
    liabilities = db.query(Liability).filter(Liability.workspace_id == workspace_id).all()
    expected = [l for l in liabilities if _created_on_or_before(l.created_at, as_of_date)]

    total = 0.0
    contributing = 0
    for liability in expected:
        observations = (
            (row.observed_on, row.balance)
            for row in db.query(LiabilityBalanceObservation)
            .filter(LiabilityBalanceObservation.liability_id == liability.id)
            .all()
        )
        balance = liability_balance_as_of(observations, as_of_date)
        if balance is not None:
            contributing += 1
            total += balance

    complete = contributing == len(expected)
    return (total if complete else None), complete


def _newly_tracked_scope(db: Session, workspace_id: int, start_date: str, end_date: str) -> bool:
    """True when a Portfolio, CashAccount, or Liability is expected at
    end_date but was not yet expected at start_date — i.e. tracked scope
    widened within the period (Section 17 disclosure). Never persisted;
    derived per request."""
    portfolios = db.query(Portfolio).filter(Portfolio.workspace_id == workspace_id).all()
    accounts = db.query(CashAccount).filter(CashAccount.workspace_id == workspace_id).all()
    liabilities = db.query(Liability).filter(Liability.workspace_id == workspace_id).all()
    for entity in (*portfolios, *accounts, *liabilities):
        if (
            not _created_on_or_before(entity.created_at, start_date)
            and _created_on_or_before(entity.created_at, end_date)
        ):
            return True
    return False


# ─── Orchestration ───────────────────────────────────────────────────────────

def get_change_attribution(db: Session, workspace_id: int, start_date: str, end_date: str) -> dict:
    """Derived read: AVAILABLE or UNAVAILABLE. Never persists, never mutates,
    never substitutes zero for unavailable evidence."""
    inv_start, inv_start_ok = _resolve_investment_assets(db, workspace_id, start_date)
    inv_end, inv_end_ok = _resolve_investment_assets(db, workspace_id, end_date)
    cash_start, cash_start_ok = _resolve_external_cash(db, workspace_id, start_date)
    cash_end, cash_end_ok = _resolve_external_cash(db, workspace_id, end_date)
    liab_start, liab_start_ok = _resolve_total_liabilities(db, workspace_id, start_date)
    liab_end, liab_end_ok = _resolve_total_liabilities(db, workspace_id, end_date)

    reasons: list[str] = []
    if not inv_start_ok:
        reasons.append("INVESTMENT_EVIDENCE_INCOMPLETE_AT_START")
    if not inv_end_ok:
        reasons.append("INVESTMENT_EVIDENCE_INCOMPLETE_AT_END")
    if not cash_start_ok:
        reasons.append("CASH_EVIDENCE_INCOMPLETE_AT_START")
    if not cash_end_ok:
        reasons.append("CASH_EVIDENCE_INCOMPLETE_AT_END")
    if not liab_start_ok:
        reasons.append("LIABILITY_EVIDENCE_INCOMPLETE_AT_START")
    if not liab_end_ok:
        reasons.append("LIABILITY_EVIDENCE_INCOMPLETE_AT_END")

    if reasons:
        return {
            "status": "UNAVAILABLE",
            "start_date": start_date,
            "end_date": end_date,
            "reason_codes": reasons,
        }

    result = build_available_result(
        start_date,
        end_date,
        {"investment_assets": inv_start, "external_cash": cash_start, "total_liabilities": liab_start},
        {"investment_assets": inv_end, "external_cash": cash_end, "total_liabilities": liab_end},
    )
    if result is None:
        return {
            "status": "UNAVAILABLE",
            "start_date": start_date,
            "end_date": end_date,
            "reason_codes": ["RECONCILIATION_FAILURE"],
        }

    result["new_tracking_scope"] = _newly_tracked_scope(db, workspace_id, start_date, end_date)
    return result
