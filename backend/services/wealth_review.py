"""DB-only factual valuation composition for Wealth Goal designations.

Phase 7.3A deliberately composes the unchanged Phase 7.2 Goal Context with
persisted source evidence.  It never fetches market data, creates snapshots,
or makes advisory inferences.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
import json
import logging
import math

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from models.database import CashAccount, PortfolioSnapshot
from services.goal_context import build_workspace_goal_context


_log = logging.getLogger(__name__)

CONTRACT_VERSION = "wealth.factual-review.v1"
AVAILABLE = "AVAILABLE"
UNAVAILABLE = "UNAVAILABLE"
COMPLETE = "COMPLETE"
PARTIAL = "PARTIAL"
UNKNOWN = "UNKNOWN"
SUPPORTED = "SUPPORTED"
OVER_ALLOCATED = "OVER_ALLOCATED"
_INTEGRITY_MESSAGE = "Factual wealth review evidence failed integrity validation."


class WealthReviewIntegrityError(Exception):
    """Persisted valuation evidence is structurally unsafe to present."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _raise_integrity(reason: str) -> None:
    _log.error("Factual wealth review integrity validation failed: %s", reason)
    raise WealthReviewIntegrityError(reason)


def _finite_nonnegative(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value >= 0
    )


def _iso_datetime(value: object, *, evidence: str) -> str:
    if not isinstance(value, datetime):
        _raise_integrity(f"{evidence} has invalid as-of timestamp={value!r}")
    return value.isoformat()


def _snapshot_date(value: object, *, snapshot_id: int) -> str:
    if not isinstance(value, str):
        _raise_integrity(f"snapshot_id={snapshot_id} has invalid snapshot_date={value!r}")
    try:
        date.fromisoformat(value)
    except ValueError:
        _raise_integrity(f"snapshot_id={snapshot_id} has invalid snapshot_date={value!r}")
    return value


def classify_snapshot_quality(snapshot: PortfolioSnapshot) -> str:
    """Classify persisted holdings price coverage without fabricating facts."""
    count = snapshot.holdings_count
    if count is not None and (
        not isinstance(count, int) or isinstance(count, bool) or count < 0
    ):
        _raise_integrity(
            f"snapshot_id={snapshot.id} has invalid holdings_count={count!r}"
        )

    if snapshot.holdings_json is None:
        return UNKNOWN
    if not isinstance(snapshot.holdings_json, str):
        _raise_integrity(
            f"snapshot_id={snapshot.id} has non-string holdings_json"
        )
    try:
        holdings = json.loads(snapshot.holdings_json)
    except (TypeError, ValueError):
        _raise_integrity(f"snapshot_id={snapshot.id} has malformed holdings_json")
    if not isinstance(holdings, list):
        _raise_integrity(f"snapshot_id={snapshot.id} holdings_json is not a list")
    if any(not isinstance(holding, dict) for holding in holdings):
        _raise_integrity(
            f"snapshot_id={snapshot.id} holdings_json contains a non-object entry"
        )
    if count is not None and count != len(holdings):
        _raise_integrity(
            f"snapshot_id={snapshot.id} holdings_count={count} disagrees with "
            f"holdings_json length={len(holdings)}"
        )

    flags: list[bool | None] = []
    for holding in holdings:
        flag = holding.get("price_missing")
        if "price_missing" in holding and not isinstance(flag, bool):
            _raise_integrity(
                f"snapshot_id={snapshot.id} has invalid price_missing={flag!r}"
            )
        flags.append(flag if "price_missing" in holding else None)

    if any(flag is True for flag in flags):
        return PARTIAL
    if count is None or any(flag is None for flag in flags):
        return UNKNOWN
    return COMPLETE


def _coverage(designated_total: float, valuation: dict) -> dict:
    if valuation["availability"] != AVAILABLE or valuation["quality"] != COMPLETE:
        return {"status": UNAVAILABLE, "shortfall": None}
    observed_value = valuation["observed_value"]
    if observed_value >= designated_total:
        return {"status": SUPPORTED, "shortfall": 0}
    return {
        "status": OVER_ALLOCATED,
        "shortfall": designated_total - observed_value,
    }


def _cash_valuations(
    db: Session,
    source_ids: set[int],
    workspace_id: int,
) -> dict[int, dict]:
    rows = (
        db.query(CashAccount).filter(CashAccount.id.in_(source_ids)).all()
        if source_ids
        else []
    )
    by_id = {row.id: row for row in rows}
    if len(by_id) != len(rows):
        _raise_integrity("cash valuation query returned duplicate source identities")
    valuations: dict[int, dict] = {}
    for source_id in source_ids:
        row = by_id.get(source_id)
        if row is None:
            _raise_integrity(f"referenced cash source_id={source_id} is missing")
        if row.workspace_id != workspace_id:
            _raise_integrity(
                f"cash source_id={source_id} belongs to workspace_id={row.workspace_id}, "
                f"expected={workspace_id}"
            )
        if row.currency != "THB":
            _raise_integrity(
                f"cash source_id={source_id} has invalid currency={row.currency!r}"
            )
        if not _finite_nonnegative(row.balance):
            _raise_integrity(
                f"cash source_id={source_id} has invalid balance={row.balance!r}"
            )
        valuations[source_id] = {
            "availability": AVAILABLE,
            "observed_value": row.balance,
            "as_of": _iso_datetime(
                row.updated_at, evidence=f"cash source_id={source_id}"
            ),
            "provenance": "CASH_ACCOUNT_CURRENT_BALANCE",
            "quality": COMPLETE,
        }
    return valuations


def _portfolio_valuations(
    db: Session,
    source_ids: set[int],
    workspace_id: int,
) -> dict[int, dict]:
    if not source_ids:
        return {}

    latest_dates = (
        db.query(
            PortfolioSnapshot.portfolio_id.label("portfolio_id"),
            func.max(PortfolioSnapshot.snapshot_date).label("snapshot_date"),
        )
        .filter(PortfolioSnapshot.portfolio_id.in_(source_ids))
        .group_by(PortfolioSnapshot.portfolio_id)
        .subquery()
    )
    rows = (
        db.query(PortfolioSnapshot)
        .join(
            latest_dates,
            and_(
                PortfolioSnapshot.portfolio_id == latest_dates.c.portfolio_id,
                PortfolioSnapshot.snapshot_date == latest_dates.c.snapshot_date,
            ),
        )
        .all()
    )
    by_portfolio_id: dict[int, PortfolioSnapshot] = {}
    for row in rows:
        if row.portfolio_id not in source_ids:
            _raise_integrity(
                f"snapshot_id={row.id} references unexpected portfolio_id={row.portfolio_id}"
            )
        if row.portfolio_id in by_portfolio_id:
            _raise_integrity(
                f"multiple latest snapshots returned for portfolio_id={row.portfolio_id}"
            )
        if row.workspace_id != workspace_id:
            _raise_integrity(
                f"snapshot_id={row.id} belongs to workspace_id={row.workspace_id}, "
                f"expected={workspace_id}"
            )
        if not _finite_nonnegative(row.total_value):
            _raise_integrity(
                f"snapshot_id={row.id} has invalid total_value={row.total_value!r}"
            )
        by_portfolio_id[row.portfolio_id] = row

    valuations: dict[int, dict] = {}
    for source_id in source_ids:
        snapshot = by_portfolio_id.get(source_id)
        if snapshot is None:
            valuations[source_id] = {
                "availability": UNAVAILABLE,
                "observed_value": None,
                "as_of": None,
                "provenance": None,
                "quality": None,
            }
            continue
        valuations[source_id] = {
            "availability": AVAILABLE,
            "observed_value": snapshot.total_value,
            "as_of": _snapshot_date(snapshot.snapshot_date, snapshot_id=snapshot.id),
            "provenance": "PORTFOLIO_SNAPSHOT",
            "quality": classify_snapshot_quality(snapshot),
        }
    return valuations


def _valuation_completeness(sources: list[dict]) -> str:
    if not sources or all(
        source["valuation"]["availability"] == AVAILABLE
        and source["valuation"]["quality"] == COMPLETE
        for source in sources
    ):
        return COMPLETE
    if any(source["valuation"]["availability"] == AVAILABLE for source in sources):
        return PARTIAL
    return UNAVAILABLE


def build_factual_wealth_review(
    db: Session,
    workspace_id: int,
    include_archived: bool = False,
) -> dict:
    """Compose Goal Context with persisted, as-of valuation evidence."""
    generated_at = datetime.now(timezone.utc)
    goal_context = build_workspace_goal_context(
        db, workspace_id, include_archived=include_archived
    )
    designation_rows = goal_context["designation_by_source"]
    cash_ids = {
        row["source_id"]
        for row in designation_rows
        if row["source_kind"] == "CASH_ACCOUNT"
    }
    portfolio_ids = {
        row["source_id"]
        for row in designation_rows
        if row["source_kind"] == "PORTFOLIO"
    }
    cash_valuations = _cash_valuations(db, cash_ids, workspace_id)
    portfolio_valuations = _portfolio_valuations(db, portfolio_ids, workspace_id)

    sources = []
    for row in designation_rows:
        key = row["source_id"]
        if row["source_kind"] == "CASH_ACCOUNT":
            valuation = cash_valuations[key]
        elif row["source_kind"] == "PORTFOLIO":
            valuation = portfolio_valuations[key]
        else:
            _raise_integrity(f"Goal Context returned unknown source_kind={row['source_kind']!r}")
        sources.append(
            {
                **row,
                "valuation": valuation,
                "designation_coverage": _coverage(
                    row["designated_total_in_context_scope"], valuation
                ),
            }
        )

    return {
        "contract_version": CONTRACT_VERSION,
        "review_generated_at": generated_at.isoformat(),
        "scope": goal_context["scope"],
        "goal_context": goal_context,
        "valuation_completeness": _valuation_completeness(sources),
        "sources": sources,
    }


def integrity_error_detail() -> dict:
    """Stable, non-enumerating public error body for valuation corruption."""
    return {"code": "WEALTH_REVIEW_DATA_INTEGRITY", "message": _INTEGRITY_MESSAGE}
