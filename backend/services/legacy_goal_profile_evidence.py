"""Read-only coexistence evidence for designated Portfolio goal metadata.

This service joins the canonical Goal Context allocation edge to the legacy
planning fields persisted on that edge's Portfolio.  The allocation is only a
funding designation; no goal identity, precedence, or synchronization is
inferred here.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
import logging
import re

from sqlalchemy.orm import Session

from models.database import Portfolio
from services.goal_context import build_workspace_goal_context
from services.goal_profile import build_goal_profile


_log = logging.getLogger(__name__)

CONTRACT_VERSION = "wealth.legacy-profile-evidence.v1"
COMPLETE = "COMPLETE"
UNSET = "UNSET"
UNCHANGED = "UNCHANGED"
NORMALIZED = "NORMALIZED"
UNRECOGNIZED = "UNRECOGNIZED"
SAME_RECORDED_CODE = "SAME_RECORDED_CODE"
DIFFERENT_RECORDED_CODES = "DIFFERENT_RECORDED_CODES"
SAME_RECORDED_DATE = "SAME_RECORDED_DATE"
DIFFERENT_RECORDED_DATES = "DIFFERENT_RECORDED_DATES"
NOT_COMPARABLE = "NOT_COMPARABLE"
NO_FIELDS_RECORDED = "NO_FIELDS_RECORDED"
PARTIAL_FIELDS_RECORDED = "PARTIAL_FIELDS_RECORDED"
ALL_FIELDS_RECORDED = "ALL_FIELDS_RECORDED"
UNSPECIFIED_IN_LEGACY_CONTRACT = "UNSPECIFIED_IN_LEGACY_CONTRACT"

_INTEGRITY_MESSAGE = (
    "Legacy goal profile evidence failed integrity validation."
)
_STRICT_DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


class LegacyGoalProfileEvidenceIntegrityError(Exception):
    """Persisted coexistence evidence is structurally unsafe to present."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _raise_integrity(reason: str) -> None:
    _log.error("Legacy goal profile evidence integrity validation failed: %s", reason)
    raise LegacyGoalProfileEvidenceIntegrityError(reason)


def _projection_status(raw_value: object, projection: object) -> str:
    if raw_value is None:
        return UNSET
    if projection is None:
        return UNRECOGNIZED
    return UNCHANGED if raw_value == projection else NORMALIZED


def _strict_iso_date(value: object) -> bool:
    if not isinstance(value, str) or _STRICT_DATE.fullmatch(value) is None:
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _code_comparison(canonical: object, projection: object) -> str:
    if not isinstance(canonical, str) or not isinstance(projection, str):
        return NOT_COMPARABLE
    return SAME_RECORDED_CODE if canonical == projection else DIFFERENT_RECORDED_CODES


def _date_comparison(
    canonical: object,
    raw_value: object,
    projection: object,
    projection_status: str,
) -> str:
    if (
        projection_status != UNCHANGED
        or not _strict_iso_date(raw_value)
        or not _strict_iso_date(canonical)
        or projection != raw_value
    ):
        return NOT_COMPARABLE
    return SAME_RECORDED_DATE if canonical == projection else DIFFERENT_RECORDED_DATES


def _availability(portfolio: Portfolio) -> str:
    values = (
        portfolio.goal_type,
        portfolio.goal_priority,
        portfolio.goal_target_date,
        portfolio.goal_target_value,
    )
    recorded = sum(value is not None for value in values)
    if recorded == 0:
        return NO_FIELDS_RECORDED
    if recorded == len(values):
        return ALL_FIELDS_RECORDED
    return PARTIAL_FIELDS_RECORDED


def _legacy_profile(portfolio: Portfolio, canonical_goal: dict) -> dict:
    # Compatibility normalization is owned by goal_profile.  Deliberately
    # allowlist individual projections: configured, risk fields, and any future
    # additions to that service can never enter this contract accidentally.
    projected = build_goal_profile(portfolio)

    raw_type = portfolio.goal_type
    projected_type = projected["goal_type"]
    type_status = _projection_status(raw_type, projected_type)

    raw_priority = portfolio.goal_priority
    projected_priority = projected["goal_priority"]
    priority_status = _projection_status(raw_priority, projected_priority)

    raw_date = portfolio.goal_target_date
    projected_date = projected["goal_target_date"]
    date_status = _projection_status(raw_date, projected_date)

    raw_value = portfolio.goal_target_value
    projected_value = projected["goal_target_value"]
    # This compatibility field is a passthrough rather than a normalizing
    # projection, so its only factual states are absent or unchanged.
    value_status = UNSET if raw_value is None else UNCHANGED

    return {
        "evidence_availability": _availability(portfolio),
        "goal_type": {
            "raw_value": raw_type,
            "compatibility_projection": projected_type,
            "compatibility_label_th": projected["goal_label_th"],
            "projection_status": type_status,
            "comparison": _code_comparison(
                canonical_goal.get("goal_type"), projected_type
            ),
            "provenance": "PORTFOLIO.GOAL_TYPE",
        },
        "goal_priority": {
            "raw_value": raw_priority,
            "compatibility_projection": projected_priority,
            "compatibility_label_th": projected["goal_priority_label_th"],
            "projection_status": priority_status,
            "provenance": "PORTFOLIO.GOAL_PRIORITY",
        },
        "goal_target_date": {
            "raw_value": raw_date,
            "compatibility_projection": projected_date,
            "projection_status": date_status,
            "comparison": _date_comparison(
                canonical_goal.get("target_date"),
                raw_date,
                projected_date,
                date_status,
            ),
            "provenance": "PORTFOLIO.GOAL_TARGET_DATE",
        },
        "goal_target_value": {
            "raw_value": raw_value,
            "compatibility_projection": projected_value,
            "projection_status": value_status,
            "unit_status": UNSPECIFIED_IN_LEGACY_CONTRACT,
            "provenance": "PORTFOLIO.GOAL_TARGET_VALUE",
        },
    }


def build_legacy_goal_profile_evidence(
    db: Session,
    workspace_id: int,
    include_archived: bool = False,
) -> dict:
    """Build complete allocation-edge coexistence evidence for a workspace."""
    generated_at = datetime.now(timezone.utc)
    goal_context = build_workspace_goal_context(
        db, workspace_id, include_archived=include_archived
    )

    portfolio_ids = {
        allocation["source_id"]
        for goal in goal_context["goals"]
        for allocation in goal["allocations"]
        if allocation["source_kind"] == "PORTFOLIO"
    }
    rows = (
        db.query(Portfolio).filter(Portfolio.id.in_(portfolio_ids)).all()
        if portfolio_ids
        else []
    )
    portfolios_by_id = {row.id: row for row in rows}
    if len(portfolios_by_id) != len(rows):
        _raise_integrity("portfolio evidence query returned duplicate identities")

    for portfolio_id in portfolio_ids:
        portfolio = portfolios_by_id.get(portfolio_id)
        if portfolio is None:
            _raise_integrity(f"referenced portfolio source_id={portfolio_id} is missing")
        if portfolio.workspace_id != workspace_id:
            _raise_integrity(
                f"portfolio source_id={portfolio_id} belongs to "
                f"workspace_id={portfolio.workspace_id}, expected={workspace_id}"
            )

    edges: list[dict] = []
    for goal in goal_context["goals"]:
        for allocation in goal["allocations"]:
            source_kind = allocation.get("source_kind")
            if source_kind == "CASH_ACCOUNT":
                continue
            if source_kind != "PORTFOLIO":
                _raise_integrity(
                    f"allocation_id={allocation.get('id')} has unknown "
                    f"source_kind={source_kind!r}"
                )
            if allocation.get("wealth_goal_id") != goal.get("id"):
                _raise_integrity(
                    f"allocation_id={allocation.get('id')} disagrees with its goal identity"
                )
            portfolio_id = allocation.get("source_id")
            portfolio = portfolios_by_id.get(portfolio_id)
            if portfolio is None:
                _raise_integrity(
                    f"allocation_id={allocation.get('id')} references missing portfolio"
                )
            if allocation.get("source_name") != portfolio.name:
                _raise_integrity(
                    f"allocation_id={allocation.get('id')} source metadata disagrees"
                )
            edges.append(
                {
                    "wealth_goal": {
                        key: goal[key]
                        for key in (
                            "id",
                            "name",
                            "goal_type",
                            "target_amount",
                            "currency",
                            "target_date",
                            "priority",
                            "is_archived",
                            "updated_at",
                        )
                    },
                    "designation": dict(allocation),
                    "portfolio": {"id": portfolio.id, "name": portfolio.name},
                    "legacy_profile": _legacy_profile(portfolio, goal),
                }
            )

    edges.sort(
        key=lambda edge: (
            edge["wealth_goal"]["name"],
            edge["wealth_goal"]["id"],
            edge["designation"]["id"],
        )
    )
    return {
        "contract_version": CONTRACT_VERSION,
        "generated_at": generated_at.isoformat(),
        "completeness": COMPLETE,
        "scope": goal_context["scope"],
        "goal_context": goal_context,
        "evidence_edges": edges,
    }


def integrity_error_detail() -> dict:
    """Stable, non-enumerating public error body for evidence corruption."""
    return {
        "code": "LEGACY_GOAL_PROFILE_EVIDENCE_DATA_INTEGRITY",
        "message": _INTEGRITY_MESSAGE,
    }
