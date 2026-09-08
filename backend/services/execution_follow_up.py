"""Product Intelligence Slice 2 — execution follow-up acknowledgment.

``ExecutionReview`` is the canonical retrospective assessment.  This module
owns only the separate, current-state workflow metadata that suppresses an
eligible review from the Needs Follow-up view until the user explicitly
returns it to that view.

The acknowledgement write uses a conditional UPDATE/INSERT whose predicate
includes the review's expected ``updated_at`` and current outcome.  That keeps
the optimistic stale-review guard in the same database transaction as the
write, and prevents a write that was waiting behind a concurrent review edit
from recreating stale suppression after that edit commits. PostgreSQL also
locks the canonical review row; SQLite uses its single-writer ordering plus
the conditional DML predicate because it ignores row locks.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import exists, func, insert, literal, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from models.database import ExecutionFollowUp, ExecutionReview, UserExecutionDecision
from services.execution_review import is_reviewable, valid_outcome

FOLLOW_UP_OUTCOMES = frozenset({"MIXED", "OFF_TRACK"})


class ExecutionFollowUpError(Exception):
    """Base class for expected follow-up workflow errors."""


class ExecutionFollowUpNotReviewableError(ExecutionFollowUpError):
    """The decision is system-generated and cannot have workflow state."""


class ExecutionFollowUpNotEligibleError(ExecutionFollowUpError):
    """The reviewable decision has no current MIXED/OFF_TRACK review."""


class ExecutionFollowUpStaleReviewError(ExecutionFollowUpError):
    """The client attempted to acknowledge an outdated review state."""


class ExecutionFollowUpMissingPreconditionError(ExecutionFollowUpError):
    """Acknowledgment was requested without the displayed review timestamp."""


def _utc_naive(value: datetime) -> datetime:
    """Normalize an API or database timestamp to the repo's naive UTC form."""
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def parse_expected_review_updated_at(value: datetime | str | None) -> datetime | None:
    """Parse the timestamp sent by the frontend and normalize it to UTC.

    FastAPI/Pydantic normally gives the service a ``datetime``.  Accepting a
    string as well keeps the service convenient for direct callers and tests,
    while still using the same ISO-8601 parser as the rest of the backend.
    """
    if value is None:
        return None
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if not isinstance(value, datetime):
        raise ValueError("expected_review_updated_at must be an ISO-8601 timestamp")
    return _utc_naive(value)


def _serialize_datetime(value: datetime | None) -> str | None:
    return value.isoformat() + "Z" if value is not None else None


def build_execution_follow_up_payload(follow_up: ExecutionFollowUp | None) -> dict[str, Any]:
    """Serialize the current state, including the no-row state."""
    return {
        "acknowledged_at": _serialize_datetime(follow_up.acknowledged_at if follow_up else None),
    }


def _follow_up_query(db: Session, decision_id: int, workspace_id: int):
    return (
        db.query(ExecutionFollowUp)
        .filter(
            ExecutionFollowUp.execution_decision_id == decision_id,
            ExecutionFollowUp.workspace_id == workspace_id,
        )
        .first()
    )


def _current_decision(db: Session, execution_decision: UserExecutionDecision, workspace_id: int) -> UserExecutionDecision:
    """Refresh the resolved decision and both one-to-one workflow records.

    ``populate_existing`` matters when the caller resolved the decision before
    entering this service: the write must inspect the current canonical review
    state, not an identity-map value left over from an earlier request step.
    """
    current = (
        db.query(UserExecutionDecision)
        .options(
            joinedload(UserExecutionDecision.review),
            joinedload(UserExecutionDecision.follow_up),
        )
        .filter(
            UserExecutionDecision.id == execution_decision.id,
            UserExecutionDecision.workspace_id == workspace_id,
        )
        .populate_existing()
        .first()
    )
    return current or execution_decision


def get_execution_follow_up(
    db: Session,
    execution_decision: UserExecutionDecision,
    workspace_id: int | None = None,
) -> dict[str, Any]:
    """Return current state; a missing row is represented by a null timestamp."""
    workspace = execution_decision.workspace_id if workspace_id is None else workspace_id
    return build_execution_follow_up_payload(_follow_up_query(db, execution_decision.id, workspace))


def _review_condition(decision_id: int, workspace_id: int, expected_updated_at: datetime):
    """Return the canonical review-state predicate used by conditional writes."""
    return exists(
        select(1).where(
            ExecutionReview.execution_decision_id == decision_id,
            ExecutionReview.workspace_id == workspace_id,
            ExecutionReview.outcome.in_(tuple(FOLLOW_UP_OUTCOMES)),
            ExecutionReview.updated_at == expected_updated_at,
        )
    )


def set_execution_follow_up(
    db: Session,
    execution_decision: UserExecutionDecision,
    workspace_id: int,
    acknowledged: bool,
    expected_review_updated_at: datetime | str | None = None,
) -> dict[str, Any]:
    """Set the desired current acknowledgment state and return its payload.

    ``False`` is an idempotent clear for any reviewable decision.  ``True``
    requires a current MIXED/OFF_TRACK review and the exact review timestamp
    displayed by the client.  The conditional database mutation repeats those
    predicates at write time, so an outcome edit that commits concurrently
    cannot leave stale suppression behind.
    """
    decision = _current_decision(db, execution_decision, workspace_id)
    if not is_reviewable(decision):
        raise ExecutionFollowUpNotReviewableError(
            "This decision is system-generated and cannot have follow-up acknowledgment"
        )

    current = _follow_up_query(db, decision.id, workspace_id)

    if not acknowledged:
        if current is None or current.acknowledged_at is None:
            return build_execution_follow_up_payload(current)
        current.acknowledged_at = None
        db.commit()
        return get_execution_follow_up(db, decision, workspace_id)

    review = decision.review
    if review is None or valid_outcome(review.outcome) not in FOLLOW_UP_OUTCOMES:
        raise ExecutionFollowUpNotEligibleError(
            "A follow-up can be acknowledged only for a current MIXED or OFF_TRACK review"
        )

    expected = parse_expected_review_updated_at(expected_review_updated_at)
    if expected is None:
        raise ExecutionFollowUpMissingPreconditionError(
            "expected_review_updated_at is required when acknowledging follow-up"
        )

    # PostgreSQL permits concurrent writers on different tables. Lock the
    # canonical review row before the comparison and conditional DML so a
    # review edit already in progress must finish first; this closes the race
    # where an INSERT could otherwise observe the old outcome after the review
    # transaction had already run its invalidation update. SQLite ignores
    # SELECT FOR UPDATE, but its single-writer locking plus the repeated
    # conditional predicate on the DML provides the equivalent ordering.
    bind = db.get_bind()
    if bind is not None and bind.dialect.name != "sqlite":
        review = (
            db.query(ExecutionReview)
            .filter(
                ExecutionReview.execution_decision_id == decision.id,
                ExecutionReview.workspace_id == workspace_id,
            )
            .populate_existing()
            .with_for_update()
            .first()
        )
        if review is None or valid_outcome(review.outcome) not in FOLLOW_UP_OUTCOMES:
            raise ExecutionFollowUpNotEligibleError(
                "A follow-up can be acknowledged only for a current MIXED or OFF_TRACK review"
            )

    if _utc_naive(review.updated_at) != expected:
        raise ExecutionFollowUpStaleReviewError(
            "The review changed while this item was open; refresh the current review before acknowledging follow-up"
        )

    now = datetime.utcnow()
    condition = _review_condition(decision.id, workspace_id, expected)

    try:
        if current is not None:
            result = db.execute(
                update(ExecutionFollowUp)
                .where(
                    ExecutionFollowUp.id == current.id,
                    ExecutionFollowUp.execution_decision_id == decision.id,
                    ExecutionFollowUp.workspace_id == workspace_id,
                    condition,
                )
                # COALESCE preserves the first server-owned timestamp on repeated
                # acknowledgment; it never accepts a client timestamp.
                .values(acknowledged_at=func.coalesce(ExecutionFollowUp.acknowledged_at, now))
            )
            if result.rowcount != 1:
                db.rollback()
                raise ExecutionFollowUpStaleReviewError(
                    "The review changed while this item was open; refresh the current review before acknowledging follow-up"
                )
        else:
            result = db.execute(
                insert(ExecutionFollowUp).from_select(
                    ["workspace_id", "execution_decision_id", "acknowledged_at"],
                    select(literal(workspace_id), literal(decision.id), literal(now)).where(condition),
                )
            )
            if result.rowcount != 1:
                db.rollback()
                raise ExecutionFollowUpStaleReviewError(
                    "The review changed while this item was open; refresh the current review before acknowledging follow-up"
                )

        db.commit()
    except IntegrityError as exc:
        # A concurrent first acknowledgment can win the unique decision
        # constraint. Re-read after rolling back; if its review state is still
        # the expected one, the desired state has already been achieved.
        db.rollback()
        current = _follow_up_query(db, decision.id, workspace_id)
        latest = _current_decision(db, decision, workspace_id)
        latest_review = latest.review
        if (
            current is not None
            and current.acknowledged_at is not None
            and latest_review is not None
            and valid_outcome(latest_review.outcome) in FOLLOW_UP_OUTCOMES
            and _utc_naive(latest_review.updated_at) == expected
        ):
            return build_execution_follow_up_payload(current)
        raise ExecutionFollowUpStaleReviewError(
            "The review changed while this item was open; refresh the current review before acknowledging follow-up"
        ) from exc

    return get_execution_follow_up(db, decision, workspace_id)
