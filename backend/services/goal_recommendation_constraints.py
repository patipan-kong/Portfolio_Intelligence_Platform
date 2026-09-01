"""Deterministic Phase 7.5 Goal recommendation-constraint admission and policy."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from sqlalchemy.orm import Session

from models.database import WealthGoal
from services.optimizer.constraint_resolver import SinglePositionUpperBoundCandidate

CONTRACT_VERSION = "wealth.goal-recommendation-constraints.v1"
RULE_SET_ID = "GOAL_HORIZON_SINGLE_POSITION_CAP"
RULE_SET_VERSION = "1"
GOAL_BINDING_SOURCE = "WEALTH_GOAL_POLICY"
GOAL_MAX_SINGLE_POSITION_PCT = 20.0


class GoalRecommendationConstraintIntegrityError(ValueError):
    """Persisted admitted Goal facts cannot be interpreted safely."""


@dataclass(frozen=True)
class GoalConstraintAdmission:
    goal_id: int
    is_archived: bool
    target_date: date | None


@dataclass(frozen=True)
class GoalConstraintEvaluation:
    admission: GoalConstraintAdmission
    as_of_date: date
    days_remaining: int
    matched_rule: str | None
    candidate: SinglePositionUpperBoundCandidate | None


def load_goal_constraint_admission(
    db: Session,
    workspace_id: int,
    goal_id: int,
) -> GoalConstraintAdmission | None:
    """Read only the three Goal facts admitted to Phase 7.5 policy."""
    row = (
        db.query(WealthGoal.id, WealthGoal.is_archived, WealthGoal.target_date)
        .filter(WealthGoal.workspace_id == workspace_id, WealthGoal.id == goal_id)
        .first()
    )
    if row is None:
        return None
    raw_id, raw_archived, raw_target_date = row
    if not isinstance(raw_id, int) or isinstance(raw_id, bool):
        raise GoalRecommendationConstraintIntegrityError("invalid goal identity")
    if not isinstance(raw_archived, bool):
        raise GoalRecommendationConstraintIntegrityError("invalid archive state")
    if raw_target_date is None:
        target_date = None
    elif isinstance(raw_target_date, str):
        try:
            target_date = date.fromisoformat(raw_target_date)
        except ValueError as exc:
            raise GoalRecommendationConstraintIntegrityError("invalid target date") from exc
    else:
        raise GoalRecommendationConstraintIntegrityError("invalid target date type")
    return GoalConstraintAdmission(raw_id, raw_archived, target_date)


def evaluate_goal_recommendation_constraint(
    admission: GoalConstraintAdmission,
    as_of_date: date,
) -> GoalConstraintEvaluation:
    """Derive the frozen Goal horizon rule without consulting a clock or AI."""
    if admission.target_date is None:
        raise ValueError("target date required")
    days_remaining = (admission.target_date - as_of_date).days
    if days_remaining < 0:
        raise ValueError("target date past")
    if days_remaining > 365:
        return GoalConstraintEvaluation(admission, as_of_date, days_remaining, None, None)
    return GoalConstraintEvaluation(
        admission,
        as_of_date,
        days_remaining,
        "TARGET_DATE_WITHIN_365_DAYS",
        SinglePositionUpperBoundCandidate(
            upper_bound_pct=GOAL_MAX_SINGLE_POSITION_PCT,
            binding_source=GOAL_BINDING_SOURCE,
            tightened_reason="Request-scoped policy upper bound: capped at 20%",
        ),
    )


def build_goal_constraint_evidence(evaluation: GoalConstraintEvaluation, outcome=None) -> dict:
    """Build canonical history evidence from frozen admission and composition facts."""
    contribution = None
    if evaluation.candidate is not None:
        contribution = {
            "constraint": "MAX_SINGLE_POSITION_PCT",
            "upper_bound_pct": evaluation.candidate.upper_bound_pct,
        }
    if outcome is None:
        resolution = {
            "pre_goal_effective_pct": None,
            "post_goal_effective_pct": None,
            "relation_to_base": "NOT_APPLICABLE",
            "application_status": "NOT_APPLICABLE",
            "resulting_binding_source": None,
        }
    else:
        status = (
            "APPLIED_AND_BINDING"
            if outcome.relation_to_base == "STRICTER_THAN_BASE"
            else "APPLIED_BUT_DOMINATED"
        )
        resolution = {
            "pre_goal_effective_pct": outcome.pre_effective_pct,
            "post_goal_effective_pct": outcome.post_effective_pct,
            "relation_to_base": outcome.relation_to_base,
            "application_status": status,
            "resulting_binding_source": outcome.resulting_binding_source,
        }
    return {
        "contract_version": CONTRACT_VERSION,
        "rule_set": {"id": RULE_SET_ID, "version": RULE_SET_VERSION},
        "source": "EXPLICIT_GOAL_ACTIVATION",
        "activated_goal_id": evaluation.admission.goal_id,
        "activation": {"field": "goal_constraint_goal_id", "mode": "EXPLICIT"},
        "observed_is_archived": evaluation.admission.is_archived,
        "target_date": evaluation.admission.target_date.isoformat(),
        "as_of_date": evaluation.as_of_date.isoformat(),
        "days_remaining": evaluation.days_remaining,
        "matched_rule": evaluation.matched_rule,
        "contribution": contribution,
        "resolution": resolution,
    }
