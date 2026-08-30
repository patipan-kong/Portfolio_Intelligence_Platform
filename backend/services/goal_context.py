"""Canonical, valuation-free factual context for Wealth Goals.

This module deliberately reads only WealthGoal, GoalFundingAllocation, and
their explicitly referenced CashAccount/Portfolio records.  It neither values
sources nor imports any market-data, snapshot, profile, or optimizer code.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import logging
import math
from typing import Iterable, Mapping

from sqlalchemy.orm import Session

from models.database import CashAccount, GoalFundingAllocation, Portfolio, WealthGoal


_log = logging.getLogger(__name__)

CONTRACT_VERSION = "wealth.goal-context.v1"
COMPLETE = "COMPLETE"
_INTEGRITY_MESSAGE = "Goal Context evidence failed integrity validation."


class GoalContextIntegrityError(Exception):
    """Persisted goal evidence is structurally unsafe to present as facts."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _value(record: object, name: str):
    return record[name] if isinstance(record, Mapping) else getattr(record, name)


def _finite_positive(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def _raise_integrity(reason: str) -> None:
    # Keep diagnosis in application logs while the HTTP boundary deliberately
    # returns a stable, non-enumerating error to callers.
    _log.error("Goal Context integrity validation failed: %s", reason)
    raise GoalContextIntegrityError(reason)


def compute_goal_funding(target_amount: float, allocations: Iterable[object]) -> dict:
    """Compute valuation-free designation facts from already-valid evidence."""
    designated_total = sum(float(_value(allocation, "allocated_amount")) for allocation in allocations)
    progress_ratio = designated_total / target_amount
    return {
        "designated_total": designated_total,
        "progress_ratio": progress_ratio,
        "progress_percent": progress_ratio * 100,
        "funding_gap": max(target_amount - designated_total, 0),
        "fully_designated": designated_total >= target_amount,
    }


def aggregate_designations_by_source(allocations: Iterable[object]) -> dict[tuple[str, int], float]:
    """Aggregate designated amounts by the typed source identity."""
    totals: dict[tuple[str, int], float] = defaultdict(float)
    for allocation in allocations:
        cash_account_id = _value(allocation, "cash_account_id")
        portfolio_id = _value(allocation, "portfolio_id")
        if (cash_account_id is None) == (portfolio_id is None):
            _raise_integrity("allocation does not have exactly one source foreign key")
        source_kind, source_id = (
            ("CASH_ACCOUNT", cash_account_id) if cash_account_id is not None else ("PORTFOLIO", portfolio_id)
        )
        totals[(source_kind, source_id)] += float(_value(allocation, "allocated_amount"))
    return dict(totals)


def _validate_goal(goal: WealthGoal, workspace_id: int) -> None:
    if goal.workspace_id != workspace_id:
        _raise_integrity(f"goal_id={goal.id} belongs to workspace_id={goal.workspace_id}, expected={workspace_id}")
    if goal.currency != "THB":
        _raise_integrity(f"goal_id={goal.id} has invalid currency={goal.currency!r}")
    if not _finite_positive(goal.target_amount):
        _raise_integrity(f"goal_id={goal.id} has invalid target_amount={goal.target_amount!r}")


def _validate_allocations(
    allocations: list[GoalFundingAllocation],
    goals_by_id: Mapping[int, WealthGoal],
    workspace_id: int,
) -> None:
    seen: set[tuple[int, str, int]] = set()
    for allocation in allocations:
        goal = goals_by_id.get(allocation.wealth_goal_id)
        if goal is None:
            _raise_integrity(f"allocation_id={getattr(allocation, 'id', None)} does not belong to a selected goal")
        if allocation.workspace_id != workspace_id or allocation.workspace_id != goal.workspace_id:
            _raise_integrity(
                f"allocation_id={getattr(allocation, 'id', None)} workspace_id={allocation.workspace_id} "
                f"disagrees with goal_id={goal.id} workspace_id={goal.workspace_id} expected={workspace_id}"
            )
        if allocation.currency != "THB":
            _raise_integrity(f"allocation_id={getattr(allocation, 'id', None)} has invalid currency={allocation.currency!r}")
        if not _finite_positive(allocation.allocated_amount):
            _raise_integrity(f"allocation_id={getattr(allocation, 'id', None)} has invalid amount={allocation.allocated_amount!r}")
        if (allocation.cash_account_id is None) == (allocation.portfolio_id is None):
            _raise_integrity(f"allocation_id={getattr(allocation, 'id', None)} does not have exactly one source foreign key")
        source_kind, source_id = (
            ("CASH_ACCOUNT", allocation.cash_account_id)
            if allocation.cash_account_id is not None
            else ("PORTFOLIO", allocation.portfolio_id)
        )
        key = (allocation.wealth_goal_id, source_kind, source_id)
        if key in seen:
            _raise_integrity(f"duplicate allocation evidence for goal_id={allocation.wealth_goal_id}, source={source_kind}:{source_id}")
        seen.add(key)


def _source_metadata(
    db: Session,
    allocations: list[GoalFundingAllocation],
    workspace_id: int,
) -> dict[tuple[str, int], dict]:
    cash_ids = {allocation.cash_account_id for allocation in allocations if allocation.cash_account_id is not None}
    portfolio_ids = {allocation.portfolio_id for allocation in allocations if allocation.portfolio_id is not None}

    # Exactly one set query per referenced source type.  Deliberately do not
    # scope these queries by workspace, so a foreign reference is detected as
    # integrity corruption rather than silently disappearing.
    cash_by_id = {
        source.id: source
        for source in (db.query(CashAccount).filter(CashAccount.id.in_(cash_ids)).all() if cash_ids else [])
    }
    portfolio_by_id = {
        source.id: source
        for source in (db.query(Portfolio).filter(Portfolio.id.in_(portfolio_ids)).all() if portfolio_ids else [])
    }

    metadata: dict[tuple[str, int], dict] = {}
    for source_id in cash_ids:
        source = cash_by_id.get(source_id)
        if source is None:
            _raise_integrity(f"referenced cash source_id={source_id} is missing")
        if source.workspace_id != workspace_id:
            _raise_integrity(f"cash source_id={source_id} belongs to workspace_id={source.workspace_id}, expected={workspace_id}")
        if source.currency != "THB":
            _raise_integrity(f"cash source_id={source_id} has invalid currency={source.currency!r}")
        metadata[("CASH_ACCOUNT", source_id)] = {
            "source_kind": "CASH_ACCOUNT",
            "source_id": source_id,
            "source_name": source.name,
            "source_is_archived": bool(source.is_archived),
            "currency": source.currency,
        }
    for source_id in portfolio_ids:
        source = portfolio_by_id.get(source_id)
        if source is None:
            _raise_integrity(f"referenced portfolio source_id={source_id} is missing")
        if source.workspace_id != workspace_id:
            _raise_integrity(f"portfolio source_id={source_id} belongs to workspace_id={source.workspace_id}, expected={workspace_id}")
        metadata[("PORTFOLIO", source_id)] = {
            "source_kind": "PORTFOLIO",
            "source_id": source_id,
            "source_name": source.name,
            "source_is_archived": False,
            "currency": "THB",
        }
    return metadata


def _timestamp(value: datetime) -> str:
    return value.isoformat()


def _assemble_context(
    db: Session,
    goals: list[WealthGoal],
    workspace_id: int,
    scope: dict,
    generated_at: datetime,
) -> dict:
    for goal in goals:
        _validate_goal(goal, workspace_id)

    goal_ids = [goal.id for goal in goals]
    # Query by goal id (rather than allocation workspace) so corrupted
    # allocation-workspace evidence cannot be silently omitted.
    allocations = (
        db.query(GoalFundingAllocation)
        .filter(GoalFundingAllocation.wealth_goal_id.in_(goal_ids))
        .order_by(GoalFundingAllocation.wealth_goal_id, GoalFundingAllocation.id)
        .all()
        if goal_ids
        else []
    )
    goals_by_id = {goal.id: goal for goal in goals}
    _validate_allocations(allocations, goals_by_id, workspace_id)
    source_meta = _source_metadata(db, allocations, workspace_id)
    totals_by_source = aggregate_designations_by_source(allocations)

    allocations_by_goal: dict[int, list[GoalFundingAllocation]] = defaultdict(list)
    for allocation in allocations:
        allocations_by_goal[allocation.wealth_goal_id].append(allocation)

    goal_payloads = []
    for goal in goals:
        goal_allocations = allocations_by_goal[goal.id]
        derived = compute_goal_funding(goal.target_amount, goal_allocations)
        allocation_payloads = []
        for allocation in goal_allocations:
            source_kind, source_id = (
                ("CASH_ACCOUNT", allocation.cash_account_id)
                if allocation.cash_account_id is not None
                else ("PORTFOLIO", allocation.portfolio_id)
            )
            metadata = source_meta[(source_kind, source_id)]
            allocation_payloads.append({
                "id": allocation.id,
                "wealth_goal_id": allocation.wealth_goal_id,
                "source_kind": source_kind,
                "source_id": source_id,
                "source_name": metadata["source_name"],
                "source_is_archived": metadata["source_is_archived"],
                "designated_amount": allocation.allocated_amount,
                "currency": allocation.currency,
                "updated_at": _timestamp(allocation.updated_at),
            })
        goal_payloads.append({
            "id": goal.id,
            "name": goal.name,
            "goal_type": goal.goal_type,
            "target_amount": goal.target_amount,
            "currency": goal.currency,
            "target_date": goal.target_date,
            "priority": goal.priority,
            "is_archived": bool(goal.is_archived),
            "updated_at": _timestamp(goal.updated_at),
            "allocations": allocation_payloads,
            **derived,
        })

    designation_by_source = [
        {
            **source_meta[key],
            "designated_total_in_context_scope": total,
        }
        for key, total in totals_by_source.items()
    ]
    designation_by_source.sort(key=lambda item: (item["source_name"], item["source_kind"], item["source_id"]))
    return {
        "contract_version": CONTRACT_VERSION,
        "context_generated_at": _timestamp(generated_at),
        "completeness": COMPLETE,
        "scope": scope,
        "goals": goal_payloads,
        "designation_by_source": designation_by_source,
    }


def build_workspace_goal_context(db: Session, workspace_id: int, include_archived: bool = False) -> dict:
    """Build a complete context for selected active (or all) workspace goals."""
    generated_at = datetime.now(timezone.utc)
    query = db.query(WealthGoal).filter(WealthGoal.workspace_id == workspace_id)
    if not include_archived:
        query = query.filter(WealthGoal.is_archived.is_(False))
    goals = query.order_by(WealthGoal.name, WealthGoal.id).all()
    return _assemble_context(
        db,
        goals,
        workspace_id,
        {"kind": "WORKSPACE", "include_archived": include_archived},
        generated_at,
    )


def build_goal_context(db: Session, workspace_id: int, goal_id: int) -> dict | None:
    """Build a complete context for one owned goal; missing/foreign is None."""
    generated_at = datetime.now(timezone.utc)
    goal = (
        db.query(WealthGoal)
        .filter(WealthGoal.id == goal_id, WealthGoal.workspace_id == workspace_id)
        .first()
    )
    if goal is None:
        return None
    return _assemble_context(
        db,
        [goal],
        workspace_id,
        {"kind": "GOAL", "goal_id": goal_id},
        generated_at,
    )


def integrity_error_detail() -> dict:
    """Stable public error body used by the API boundary."""
    return {"code": "GOAL_CONTEXT_DATA_INTEGRITY", "message": _INTEGRITY_MESSAGE}
