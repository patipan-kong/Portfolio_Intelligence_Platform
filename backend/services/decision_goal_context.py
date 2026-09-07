"""decision_goal_context.py — Phase 7.4

Derives the versioned, context-only Decision Intelligence admission envelope
(``wealth.decision-goal-context.v1``) from the canonical Goal Context for an
explicitly selected set of Wealth Goals.

This module owns only that derived envelope shape. It performs no optimizer,
provider, or valuation work, and reuses services.goal_context's existing
composition rather than duplicating funding arithmetic or source validation.

Per ADR-008, the caller (main.py) is responsible for invoking
``build_decision_goal_context`` only after the full recommendation result
already exists — this module makes no attempt to enforce that ordering
itself, since it has no visibility into when it is called.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
import logging
import math

from sqlalchemy.orm import Session

from services.goal_context import (
    CONTRACT_VERSION as SOURCE_GOAL_CONTEXT_VERSION,
    build_selected_goal_context,
)

_log = logging.getLogger(__name__)

CONTRACT_VERSION = "wealth.decision-goal-context.v1"
CONTEXT_ONLY = "CONTEXT_ONLY"
EMPTY = "EMPTY"
COMPLETE = "COMPLETE"

_INTEGRITY_MESSAGE = "Decision goal context evidence failed integrity validation."

# Explicit allowlist: only these fields from the canonical Goal Context goal
# payload are admitted into the Decision Intelligence envelope. Keeping this
# separate from services.goal_context's own field set means a future addition
# there (e.g. a valuation field) cannot leak into this contract by accident.
_ADMITTED_GOAL_FIELDS = (
    "id",
    "name",
    "goal_type",
    "priority",
    "target_amount",
    "currency",
    "target_date",
    "is_archived",
    "updated_at",
    "allocations",
    "designated_total",
    "progress_ratio",
    "progress_percent",
    "funding_gap",
    "fully_designated",
)

_TOP_LEVEL_KEYS = frozenset({
    "contract_version",
    "source_goal_context_version",
    "decision_effect",
    "context_state",
    "selected_goal_ids",
    "observed_at",
    "goals",
    "designation_by_source",
})

_GOAL_KEYS = frozenset(_ADMITTED_GOAL_FIELDS)
_ALLOCATION_KEYS = frozenset({
    "id",
    "wealth_goal_id",
    "source_kind",
    "source_id",
    "source_name",
    "source_is_archived",
    "designated_amount",
    "currency",
    "updated_at",
})
_SOURCE_KEYS = frozenset({
    "source_kind",
    "source_id",
    "source_name",
    "source_is_archived",
    "currency",
    "designated_total_in_context_scope",
})
_SOURCE_KINDS = frozenset({"CASH_ACCOUNT", "PORTFOLIO"})


class DecisionGoalContextIntegrityError(Exception):
    """Persisted decision goal context is structurally unsafe to present."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _raise_integrity(reason: str) -> None:
    _log.error("Decision goal context integrity validation failed: %s", reason)
    raise DecisionGoalContextIntegrityError(reason)


def _require_exact_keys(value: object, expected: frozenset[str], path: str) -> dict:
    if not isinstance(value, dict):
        _raise_integrity(f"{path} is not an object")
    actual = set(value)
    if actual != expected:
        _raise_integrity(
            f"{path} has invalid fields: missing={sorted(expected - actual)}, "
            f"unexpected={sorted(actual - expected)}"
        )
    return value


def _is_id(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _require_id(value: object, path: str) -> int:
    if not _is_id(value):
        _raise_integrity(f"{path} is not a positive integer id")
    return value


def _require_string(value: object, path: str) -> str:
    if not isinstance(value, str):
        _raise_integrity(f"{path} is not a string")
    return value


def _require_number(value: object, path: str, *, positive: bool = False) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        _raise_integrity(f"{path} is not a finite number")
    if positive and value <= 0:
        _raise_integrity(f"{path} is not positive")
    if not positive and value < 0:
        _raise_integrity(f"{path} is negative")
    return float(value)


def _require_timestamp(value: object, path: str, *, timezone_required: bool = False) -> str:
    text = _require_string(value, path)
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        _raise_integrity(f"{path} is not an ISO-8601 timestamp")
    if timezone_required and parsed.utcoffset() is None:
        _raise_integrity(f"{path} is not timezone-aware")
    return text


def _require_goal_ids(value: object) -> list[int]:
    if not isinstance(value, list):
        _raise_integrity("selected_goal_ids is not a list")
    if any(not _is_id(goal_id) for goal_id in value):
        _raise_integrity("selected_goal_ids contains a non-integer or invalid id")
    if value != sorted(set(value)):
        _raise_integrity("selected_goal_ids is not unique and ascending")
    return value


def _validate_allocation(value: object, path: str, goal_id: int) -> dict:
    allocation = _require_exact_keys(value, _ALLOCATION_KEYS, path)
    _require_id(allocation["id"], f"{path}.id")
    if _require_id(allocation["wealth_goal_id"], f"{path}.wealth_goal_id") != goal_id:
        _raise_integrity(f"{path}.wealth_goal_id does not match its goal")
    if allocation["source_kind"] not in _SOURCE_KINDS:
        _raise_integrity(f"{path}.source_kind is unsupported")
    _require_id(allocation["source_id"], f"{path}.source_id")
    _require_string(allocation["source_name"], f"{path}.source_name")
    if not isinstance(allocation["source_is_archived"], bool):
        _raise_integrity(f"{path}.source_is_archived is not a boolean")
    _require_number(allocation["designated_amount"], f"{path}.designated_amount", positive=True)
    if allocation["currency"] != "THB":
        _raise_integrity(f"{path}.currency is unsupported")
    _require_timestamp(allocation["updated_at"], f"{path}.updated_at")
    return allocation


def _validate_goal(value: object, path: str) -> dict:
    goal = _require_exact_keys(value, _GOAL_KEYS, path)
    goal_id = _require_id(goal["id"], f"{path}.id")
    for field in ("name", "goal_type", "priority"):
        _require_string(goal[field], f"{path}.{field}")
    target_amount = _require_number(goal["target_amount"], f"{path}.target_amount", positive=True)
    if goal["currency"] != "THB":
        _raise_integrity(f"{path}.currency is unsupported")
    if goal["target_date"] is not None:
        target_date = _require_string(goal["target_date"], f"{path}.target_date")
        try:
            date.fromisoformat(target_date)
        except ValueError:
            _raise_integrity(f"{path}.target_date is not an ISO-8601 date")
    if not isinstance(goal["is_archived"], bool):
        _raise_integrity(f"{path}.is_archived is not a boolean")
    _require_timestamp(goal["updated_at"], f"{path}.updated_at")
    if not isinstance(goal["allocations"], list):
        _raise_integrity(f"{path}.allocations is not a list")
    allocations = [
        _validate_allocation(item, f"{path}.allocations[{index}]", goal_id)
        for index, item in enumerate(goal["allocations"])
    ]
    allocation_ids = [item["id"] for item in allocations]
    if allocation_ids != sorted(set(allocation_ids)):
        _raise_integrity(f"{path}.allocations is not unique and id-ordered")

    designated_total = _require_number(goal["designated_total"], f"{path}.designated_total")
    progress_ratio = _require_number(goal["progress_ratio"], f"{path}.progress_ratio")
    progress_percent = _require_number(goal["progress_percent"], f"{path}.progress_percent")
    funding_gap = _require_number(goal["funding_gap"], f"{path}.funding_gap")
    if not isinstance(goal["fully_designated"], bool):
        _raise_integrity(f"{path}.fully_designated is not a boolean")

    allocation_total = sum(float(item["designated_amount"]) for item in allocations)
    expected_ratio = allocation_total / target_amount
    if not math.isclose(designated_total, allocation_total):
        _raise_integrity(f"{path}.designated_total disagrees with allocations")
    if not math.isclose(progress_ratio, expected_ratio):
        _raise_integrity(f"{path}.progress_ratio disagrees with factual totals")
    if not math.isclose(progress_percent, expected_ratio * 100):
        _raise_integrity(f"{path}.progress_percent disagrees with factual totals")
    if not math.isclose(funding_gap, max(target_amount - allocation_total, 0)):
        _raise_integrity(f"{path}.funding_gap disagrees with factual totals")
    if goal["fully_designated"] != (allocation_total >= target_amount):
        _raise_integrity(f"{path}.fully_designated disagrees with factual totals")
    return goal


def _validate_source(value: object, path: str) -> dict:
    source = _require_exact_keys(value, _SOURCE_KEYS, path)
    if source["source_kind"] not in _SOURCE_KINDS:
        _raise_integrity(f"{path}.source_kind is unsupported")
    _require_id(source["source_id"], f"{path}.source_id")
    _require_string(source["source_name"], f"{path}.source_name")
    if not isinstance(source["source_is_archived"], bool):
        _raise_integrity(f"{path}.source_is_archived is not a boolean")
    if source["currency"] != "THB":
        _raise_integrity(f"{path}.currency is unsupported")
    _require_number(
        source["designated_total_in_context_scope"],
        f"{path}.designated_total_in_context_scope",
        positive=True,
    )
    return source


def _validate_context_payload(payload: object) -> dict:
    envelope = _require_exact_keys(payload, _TOP_LEVEL_KEYS, "persisted decision context")
    if envelope["contract_version"] != CONTRACT_VERSION:
        _raise_integrity(f"unsupported decision context contract_version={envelope['contract_version']!r}")
    if envelope["source_goal_context_version"] != SOURCE_GOAL_CONTEXT_VERSION:
        _raise_integrity(
            f"unsupported source_goal_context_version={envelope['source_goal_context_version']!r}"
        )
    if envelope["decision_effect"] != CONTEXT_ONLY:
        _raise_integrity(f"unexpected decision_effect={envelope['decision_effect']!r}")
    if envelope["context_state"] not in (EMPTY, COMPLETE):
        _raise_integrity(f"unexpected context_state={envelope['context_state']!r}")

    selected_goal_ids = _require_goal_ids(envelope["selected_goal_ids"])
    _require_timestamp(envelope["observed_at"], "observed_at", timezone_required=True)
    if not isinstance(envelope["goals"], list):
        _raise_integrity("goals is not a list")
    goals = [_validate_goal(item, f"goals[{index}]") for index, item in enumerate(envelope["goals"])]
    goal_ids = [goal["id"] for goal in goals]
    if goal_ids != [goal["id"] for goal in sorted(goals, key=lambda item: (item["name"], item["id"]))]:
        _raise_integrity("goals is not deterministically ordered")
    if sorted(goal_ids) != selected_goal_ids or len(goal_ids) != len(set(goal_ids)):
        _raise_integrity("goal identities do not exactly match selected_goal_ids")

    if not isinstance(envelope["designation_by_source"], list):
        _raise_integrity("designation_by_source is not a list")
    sources = [
        _validate_source(item, f"designation_by_source[{index}]")
        for index, item in enumerate(envelope["designation_by_source"])
    ]
    expected_source_order = sorted(
        sources,
        key=lambda item: (item["source_name"], item["source_kind"], item["source_id"]),
    )
    if sources != expected_source_order:
        _raise_integrity("designation_by_source is not deterministically ordered")

    allocation_sources: dict[tuple[str, int], dict] = {}
    source_totals: dict[tuple[str, int], float] = {}
    for goal in goals:
        for allocation in goal["allocations"]:
            key = (allocation["source_kind"], allocation["source_id"])
            metadata = {
                "source_kind": allocation["source_kind"],
                "source_id": allocation["source_id"],
                "source_name": allocation["source_name"],
                "source_is_archived": allocation["source_is_archived"],
                "currency": allocation["currency"],
            }
            if key in allocation_sources and allocation_sources[key] != metadata:
                _raise_integrity("allocation source metadata is inconsistent")
            allocation_sources[key] = metadata
            source_totals[key] = source_totals.get(key, 0.0) + float(allocation["designated_amount"])

    source_keys = [(source["source_kind"], source["source_id"]) for source in sources]
    if len(source_keys) != len(set(source_keys)) or set(source_keys) != set(allocation_sources):
        _raise_integrity("designation_by_source does not exactly match allocation sources")
    for source in sources:
        key = (source["source_kind"], source["source_id"])
        if {field: source[field] for field in allocation_sources[key]} != allocation_sources[key]:
            _raise_integrity("designation_by_source metadata disagrees with allocations")
        if not math.isclose(float(source["designated_total_in_context_scope"]), source_totals[key]):
            _raise_integrity("designation_by_source total disagrees with allocations")

    if envelope["context_state"] == EMPTY:
        if selected_goal_ids or goals or sources:
            _raise_integrity("EMPTY context contains populated factual content")
    elif not selected_goal_ids:
        _raise_integrity("COMPLETE context has no selected goals")
    return envelope


def build_decision_goal_context(db: Session, workspace_id: int, goal_ids: list[int]) -> dict:
    """Build the frozen, versioned Decision Intelligence admission payload.

    ``goal_ids`` must already have been pre-run validated as existing and
    workspace-owned (see services.goal_context.selected_goal_ids_exist). An
    empty list produces an EMPTY context; a non-empty list produces a
    COMPLETE context, or raises GoalContextIntegrityError if the canonical
    Goal Context can no longer be assembled at capture time.
    """
    observed_at = datetime.now(timezone.utc)
    raw_context = build_selected_goal_context(db, workspace_id, goal_ids)
    goals = [
        {key: goal[key] for key in _ADMITTED_GOAL_FIELDS}
        for goal in raw_context["goals"]
    ]
    return {
        "contract_version": CONTRACT_VERSION,
        "source_goal_context_version": raw_context["contract_version"],
        "decision_effect": CONTEXT_ONLY,
        "context_state": COMPLETE if goals else EMPTY,
        "selected_goal_ids": raw_context["scope"]["goal_ids"],
        "observed_at": observed_at.isoformat(),
        "goals": goals,
        "designation_by_source": raw_context["designation_by_source"],
    }


def load_persisted_decision_context(raw_json: str | None) -> dict | None:
    """Fail-closed loader for a historically persisted decision context.

    Returns None when no capture was attempted (legacy or unscoped run —
    SQL NULL). Raises DecisionGoalContextIntegrityError for any persisted
    value that is not valid JSON, not the expected shape, or not this
    contract's version — the caller maps that to a generic 409, matching the
    existing Goal Context / Legacy Evidence integrity-response pattern.
    """
    if raw_json is None:
        return None

    import json

    try:
        payload = json.loads(raw_json)
    except Exception:
        _raise_integrity("persisted decision context is not valid JSON")

    return _validate_context_payload(payload)


def integrity_error_detail() -> dict:
    """Stable, non-enumerating public error body for decision-context corruption."""
    return {"code": "DECISION_GOAL_CONTEXT_DATA_INTEGRITY", "message": _INTEGRITY_MESSAGE}
