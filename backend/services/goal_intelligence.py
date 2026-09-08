"""Phase 7.7 Goal Intelligence v1, Slice 1: descriptive composition only.

Governed by ADR-014. This module composes existing canonical facts from
`services/goal_context.py` (designation/funding) and `services/wealth_review.py`
(source valuation/coverage) for one requested Goal. It introduces no
alternate implementation of designation totals, funding progress, funding
gap, source valuation, or source coverage — the only arithmetic it adds is
elapsed-day time classification. It grants no behavioral authority (ADR-011)
and must not be imported by optimizer, recommendation-constraint, Decision
Intelligence, or execution code.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from services.wealth_review import build_factual_wealth_review, valuation_completeness

CONTRACT_VERSION = "wealth.goal-intelligence.v1"


def _time_facts(target_date: str | None, as_of_date: date) -> dict:
    if target_date is None:
        return {
            "target_date": None,
            "has_target_date": False,
            "days_remaining": None,
            "target_date_in_past": False,
        }
    parsed_target_date = date.fromisoformat(target_date)
    days_remaining = (parsed_target_date - as_of_date).days
    return {
        "target_date": target_date,
        "has_target_date": True,
        "days_remaining": days_remaining,
        "target_date_in_past": days_remaining < 0,
    }


def _funding_source_facts(goal_payload: dict, sources_by_key: dict[tuple[str, int], dict]) -> list[dict]:
    facts = []
    for allocation in goal_payload["allocations"]:
        key = (allocation["source_kind"], allocation["source_id"])
        source_row = sources_by_key[key]
        facts.append({
            "source_kind": allocation["source_kind"],
            "source_id": allocation["source_id"],
            "source_name": allocation["source_name"],
            "source_is_archived": allocation["source_is_archived"],
            "goal_designated_amount": allocation["designated_amount"],
            "source_designated_total_in_context_scope": source_row["designated_total_in_context_scope"],
            "valuation": source_row["valuation"],
            "designation_coverage": source_row["designation_coverage"],
        })
    return facts


def build_goal_intelligence(db: Session, workspace_id: int, goal_id: int, as_of_date: date) -> dict | None:
    """Compose Goal Intelligence for one workspace-owned Goal.

    Returns None when the goal is missing or belongs to a different
    workspace, matching `goal_context.build_goal_context`'s non-enumerating
    convention. `GoalContextIntegrityError` or `WealthReviewIntegrityError`
    propagate unchanged from the composed calls on evidence corruption —
    this module defines no error type of its own.
    """
    generated_at = datetime.now(timezone.utc)
    review = build_factual_wealth_review(db, workspace_id, include_archived=True)
    goal_payload = next(
        (goal for goal in review["goal_context"]["goals"] if goal["id"] == goal_id),
        None,
    )
    if goal_payload is None:
        return None

    sources_by_key = {
        (source["source_kind"], source["source_id"]): source for source in review["sources"]
    }
    funding_sources = _funding_source_facts(goal_payload, sources_by_key)

    return {
        "contract_version": CONTRACT_VERSION,
        "generated_at": generated_at.isoformat(),
        "goal_id": goal_id,
        "as_of_date": as_of_date.isoformat(),
        "funding": {
            "designated_total": goal_payload["designated_total"],
            "progress_ratio": goal_payload["progress_ratio"],
            "funding_gap": goal_payload["funding_gap"],
            "fully_designated": goal_payload["fully_designated"],
        },
        "time": _time_facts(goal_payload["target_date"], as_of_date),
        "funding_sources": funding_sources,
        "valuation_completeness": valuation_completeness(
            [sources_by_key[(f["source_kind"], f["source_id"])] for f in funding_sources]
        ),
    }
