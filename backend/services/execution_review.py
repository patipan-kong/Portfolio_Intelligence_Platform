"""Execution Review service layer (Review Workflows Slice 1, ERR-01).

One canonical, human-authored retrospective review per UserExecutionDecision
(Option A — editable over time, never append-only). Read-only with respect
to history: never mutates UserExecutionDecision or RecommendationSnapshot.

`reviewed_at` is server-generated at first creation only; edits advance
`updated_at`, never `reviewed_at` (no backdating UX/API in this slice).

Public API:
    valid_outcome(raw) -> str | None
    is_reviewable(execution_decision) -> bool
    build_execution_review_payload(review) -> dict
    get_execution_review(db, execution_decision) -> dict | None
    upsert_execution_review(db, execution_decision, workspace_id, outcome, summary, changed_context)
        -> tuple[dict, bool]   (payload, created)
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from models.database import ExecutionReview, UserExecutionDecision

OUTCOMES = ("ON_TRACK", "MIXED", "OFF_TRACK")


def valid_outcome(raw: str | None) -> str | None:
    if not raw or not isinstance(raw, str):
        return None
    code = raw.strip().upper()
    return code if code in OUTCOMES else None


def is_reviewable(execution_decision: UserExecutionDecision) -> bool:
    """A decision can acquire a review iff it is human-authored (Slice 2/3
    invariant, frozen). System-generated EXPIRED rows are never reviewable —
    the same rule the execution ledger uses for its `reviewable` field."""
    return not execution_decision.is_system_generated


def build_execution_review_payload(review: ExecutionReview) -> dict:
    # "Z" suffix matches every other naive-UTC datetime this page's sibling
    # endpoint (execution_ledger.py) already serializes — e.g. executed_at,
    # as_of — so the frontend parses all of them the same way.
    return {
        "id": review.id,
        "execution_decision_id": review.execution_decision_id,
        "reviewed_at": review.reviewed_at.isoformat() + "Z",
        "outcome": review.outcome,
        "summary": review.summary,
        "changed_context": review.changed_context,
        "created_at": review.created_at.isoformat() + "Z",
        "updated_at": review.updated_at.isoformat() + "Z",
    }


def get_execution_review(db: Session, execution_decision: UserExecutionDecision) -> dict | None:
    """The canonical review for this decision, or None if none has been recorded yet."""
    review = (
        db.query(ExecutionReview)
        .filter(ExecutionReview.execution_decision_id == execution_decision.id)
        .first()
    )
    return build_execution_review_payload(review) if review is not None else None


def upsert_execution_review(
    db: Session,
    execution_decision: UserExecutionDecision,
    workspace_id: int,
    outcome: str,
    summary: str | None,
    changed_context: str | None,
) -> tuple[dict, bool]:
    """Create the canonical review if absent, else update it in place.

    Returns (payload, created). Never touches execution_decision itself or
    its RecommendationSnapshot.
    """
    review = (
        db.query(ExecutionReview)
        .filter(ExecutionReview.execution_decision_id == execution_decision.id)
        .first()
    )
    created = review is None
    if review is None:
        review = ExecutionReview(
            workspace_id=workspace_id,
            execution_decision_id=execution_decision.id,
            outcome=outcome,
            summary=summary,
            changed_context=changed_context,
        )
        db.add(review)
    else:
        review.outcome = outcome
        review.summary = summary
        review.changed_context = changed_context

    db.commit()
    db.refresh(review)
    return build_execution_review_payload(review), created
