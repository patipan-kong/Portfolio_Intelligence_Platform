"""Historical comparison of two recommendation snapshots.

This module intentionally compares only the persisted, user-facing inputs that
are part of Product Intelligence Slice 3.  It does not inspect live portfolio
state, reconstruct optimizer output, or write comparison records.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Iterable

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session


_MISSING = object()
_UNAVAILABLE = object()

_REGIME_FIELDS = (
    ("regime", "Regime", False),
    ("confidence_pct", "Confidence", True),
    ("transition_stability", "Transition stability", False),
)
_CONSTRAINT_FIELDS = (
    ("effective_single_position_pct", "Single position cap", True),
    ("effective_cash_min_pct", "Minimum cash", True),
    ("effective_turnover_max_pct", "Maximum turnover", True),
    ("emergency_active", "Emergency active", False),
)
_POLICY_FIELDS = (
    ("deployment_bias", "Deployment bias", False),
    ("strictness_level", "Strictness level", False),
    ("risk_budget", "Risk budget", True),
    ("confidence_discount", "Confidence discount", True),
)
_CONSENSUS_FIELDS = (
    ("consensus_type", "Consensus type", False),
    ("consensus_strength_score", "Consensus strength", True),
)
_DNA_FIELDS = (
    ("growth", "Growth", True),
    ("value", "Value", True),
    ("momentum", "Momentum", True),
    ("quality", "Quality", True),
    ("dividend", "Dividend", True),
)
_STYLE_FIELDS = (
    ("drift_score", "Drift score", True),
    ("drift_severity", "Drift severity", False),
    ("rebalance_urgency", "Rebalance urgency", False),
)


def _decode_json(raw: str | None, expected: type | tuple[type, ...]) -> dict | list | object:
    """Decode one persisted JSON value, preserving unavailable vs empty."""
    if not raw:
        return _UNAVAILABLE
    try:
        value = json.loads(raw)
    except (TypeError, ValueError, json.JSONDecodeError):
        return _UNAVAILABLE
    if not isinstance(value, expected):
        return _UNAVAILABLE
    return value


def _timestamp(value: datetime | None) -> str | None:
    if value is None:
        return None
    # RecommendationSnapshot currently stores naive UTC datetimes.  Handling
    # an aware value as well keeps this endpoint consistent if the model is
    # migrated to timezone-aware storage later.
    if value.tzinfo is not None:
        value = value.astimezone(timezone.utc).replace(tzinfo=None)
    return value.isoformat() + "Z"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_comparison_value(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _has_invalid_scalar_values(
    previous: dict[str, Any],
    current: dict[str, Any],
    definitions: Iterable[tuple[str, str, bool]],
) -> bool:
    return any(
        not _is_comparison_value(value)
        for values in (previous, current)
        for key, _, _ in definitions
        for value in (values.get(key, _MISSING),)
        if value is not _MISSING
    )


def _scalar_fields(
    previous: dict[str, Any],
    current: dict[str, Any],
    definitions: Iterable[tuple[str, str, bool]],
) -> list[dict[str, Any]]:
    fields: list[dict[str, Any]] = []
    for key, label, numeric in definitions:
        before = previous.get(key, _MISSING)
        after = current.get(key, _MISSING)
        if before is _MISSING and after is _MISSING:
            continue
        if before is not _MISSING and after is not _MISSING and before == after:
            continue

        field: dict[str, Any] = {
            "key": key,
            "label": label,
            "previous": None if before is _MISSING else before,
            "current": None if after is _MISSING else after,
        }
        if (
            numeric
            and before is not _MISSING
            and after is not _MISSING
            and _is_number(before)
            and _is_number(after)
        ):
            field["delta"] = after - before
        fields.append(field)
    return fields


def _unavailable_section(key: str, label: str) -> dict[str, Any]:
    return {
        "key": key,
        "label": label,
        "status": "unavailable",
        "changed": False,
        "fields": [],
        "reason": "missing_or_unparseable_source",
    }


def _scalar_section(
    key: str,
    label: str,
    previous: object,
    current: object,
    definitions: Iterable[tuple[str, str, bool]],
) -> dict[str, Any] | None:
    if previous is _UNAVAILABLE or current is _UNAVAILABLE:
        return _unavailable_section(key, label)
    if _has_invalid_scalar_values(previous, current, definitions):  # type: ignore[arg-type]
        return _unavailable_section(key, label)
    fields = _scalar_fields(previous, current, definitions)  # type: ignore[arg-type]
    if not fields:
        return None
    return {
        "key": key,
        "label": label,
        "status": "ok",
        "changed": True,
        "fields": fields,
    }


def _sector_entries(previous: Any, current: Any) -> tuple[list[dict[str, Any]], bool]:
    if not isinstance(previous, dict) or not isinstance(current, dict):
        return [], True
    if any(not isinstance(sector, str) or not _is_number(value) for values in (previous, current) for sector, value in values.items()):
        return [], True

    entries: list[dict[str, Any]] = []
    for sector in sorted(set(previous) | set(current)):
        before = previous.get(sector, _MISSING)
        after = current.get(sector, _MISSING)
        if before is _MISSING:
            entries.append({"sector": sector, "status": "added", "current": after})
        elif after is _MISSING:
            entries.append({"sector": sector, "status": "removed", "previous": before})
        elif before != after:
            item: dict[str, Any] = {
                "sector": sector,
                "status": "changed",
                "previous": before,
                "current": after,
            }
            if _is_number(before) and _is_number(after):
                item["delta"] = after - before
            entries.append(item)
    return entries, False


def _constraint_section(previous: object, current: object) -> dict[str, Any] | None:
    section = _scalar_section(
        "constraint_envelope",
        "Constraint envelope",
        previous,
        current,
        _CONSTRAINT_FIELDS,
    )
    if previous is _UNAVAILABLE or current is _UNAVAILABLE:
        return section

    previous_limits = previous.get("effective_sector_limits", _MISSING)  # type: ignore[union-attr]
    current_limits = current.get("effective_sector_limits", _MISSING)  # type: ignore[union-attr]
    sectors, sectors_unavailable = _sector_entries(previous_limits, current_limits)
    if section is None and not sectors and not sectors_unavailable:
        return None
    if section is None:
        section = {
            "key": "constraint_envelope",
            "label": "Constraint envelope",
            "status": "ok",
            "changed": False,
            "fields": [],
        }
    section["sectors"] = sectors
    if sectors:
        section["changed"] = True
    if sectors_unavailable:
        section["sectors_status"] = "unavailable"
        # Keep valid scalar envelope comparisons useful when only the nested
        # sector-limit map is missing.  The nested status tells clients which
        # part is unavailable; the whole section is unavailable only when it
        # has no comparable content at all.
        if not section["fields"] and not sectors:
            section["status"] = "unavailable"
    return section


def _allocation_entries(previous: Any, current: Any) -> tuple[list[dict[str, Any]], bool]:
    if not isinstance(previous, list) or not isinstance(current, list):
        return [], True

    def by_symbol(values: list[Any]) -> dict[str, dict[str, Any]] | None:
        result: dict[str, dict[str, Any]] = {}
        for item in values:
            if not isinstance(item, dict) or not isinstance(item.get("symbol"), str) or not item["symbol"]:
                return None
            weight = item.get("target_weight")
            action = item.get("action")
            if (weight is not None and not _is_number(weight)) or (action is not None and not isinstance(action, str)):
                return None
            # Snapshot generation detects duplicate final symbols but does not
            # reject the write.  A dict overwrite here would silently discard
            # one persisted allocation, so retain historical truth by making
            # this comparison unavailable instead of inventing precedence.
            if item["symbol"] in result:
                return None
            result[item["symbol"]] = item
        return result

    before_by_symbol = by_symbol(previous)
    after_by_symbol = by_symbol(current)
    if before_by_symbol is None or after_by_symbol is None:
        return [], True

    entries: list[dict[str, Any]] = []
    for symbol in sorted(set(before_by_symbol) | set(after_by_symbol)):
        before = before_by_symbol.get(symbol)
        after = after_by_symbol.get(symbol)
        if before is None:
            entries.append({
                "symbol": symbol,
                "status": "added",
                "current_target_weight": after.get("target_weight"),
                "current_action": after.get("action"),
            })
            continue
        if after is None:
            entries.append({
                "symbol": symbol,
                "status": "removed",
                "previous_target_weight": before.get("target_weight"),
                "previous_action": before.get("action"),
            })
            continue

        before_weight = before.get("target_weight")
        after_weight = after.get("target_weight")
        before_action = before.get("action")
        after_action = after.get("action")
        if before_weight == after_weight and before_action == after_action:
            continue
        entry: dict[str, Any] = {
            "symbol": symbol,
            "status": "changed",
            "previous_target_weight": before_weight,
            "current_target_weight": after_weight,
            "previous_action": before_action,
            "current_action": after_action,
        }
        if _is_number(before_weight) and _is_number(after_weight):
            entry["delta"] = after_weight - before_weight
        entries.append(entry)
    return entries, False


def _allocation_section(previous: object, current: object) -> dict[str, Any] | None:
    if previous is _UNAVAILABLE or current is _UNAVAILABLE:
        return _unavailable_section("allocations", "Target allocation")
    entries, unavailable = _allocation_entries(previous, current)
    if unavailable:
        return _unavailable_section("allocations", "Target allocation")
    if not entries:
        return None
    return {
        "key": "allocations",
        "label": "Target allocation",
        "status": "ok",
        "changed": True,
        "fields": [],
        "entries": entries,
    }


def _portfolio_characteristics_section(
    previous_dna: object,
    current_dna: object,
    previous_style: object,
    current_style: object,
) -> dict[str, Any] | None:
    sub_sections: dict[str, dict[str, Any]] = {}
    all_fields: list[dict[str, Any]] = []
    unavailable = False
    changed = False

    for name, before, after, definitions in (
        ("dna", previous_dna, current_dna, _DNA_FIELDS),
        ("style", previous_style, current_style, _STYLE_FIELDS),
    ):
        if before is _UNAVAILABLE or after is _UNAVAILABLE:
            sub_sections[name] = {
                "status": "unavailable",
                "changed": False,
                "fields": [],
                "reason": "missing_or_unparseable_source",
            }
            unavailable = True
            continue
        if _has_invalid_scalar_values(before, after, definitions):  # type: ignore[arg-type]
            sub_sections[name] = {
                "status": "unavailable",
                "changed": False,
                "fields": [],
                "reason": "missing_or_unparseable_source",
            }
            unavailable = True
            continue
        fields = _scalar_fields(before, after, definitions)  # type: ignore[arg-type]
        if fields:
            sub_sections[name] = {"status": "ok", "changed": True, "fields": fields}
            all_fields.extend(fields)
            changed = True

    if not changed and not unavailable:
        return None
    section: dict[str, Any] = {
        "key": "portfolio_characteristics",
        "label": "Portfolio characteristics",
        "status": "unavailable" if unavailable else "ok",
        "changed": changed,
        "fields": all_fields,
    }
    section.update(sub_sections)
    return section


def get_recommendation_comparison(
    db: Session,
    portfolio_id: int,
    snapshot_id: int,
    workspace_id: int | None = None,
) -> dict[str, Any] | None:
    """Return the frozen, same-portfolio predecessor comparison.

    ``None`` means only that the selected snapshot is not visible in the
    requested workspace and portfolio.  A visible snapshot without a
    predecessor is a successful ``no_previous`` response.
    """
    from models.database import RecommendationSnapshot, Workspace

    if workspace_id is None:
        ws_row = db.query(Workspace).order_by(Workspace.id).first()
        workspace_id = ws_row.id if ws_row else 1

    current = (
        db.query(RecommendationSnapshot)
        .filter_by(id=snapshot_id, workspace_id=workspace_id, portfolio_id=portfolio_id)
        .first()
    )
    if current is None:
        return None

    previous = None
    if current.created_at is not None:
        previous = (
            db.query(RecommendationSnapshot)
            .filter(
                RecommendationSnapshot.workspace_id == workspace_id,
                RecommendationSnapshot.portfolio_id == portfolio_id,
                or_(
                    RecommendationSnapshot.created_at < current.created_at,
                    and_(
                        RecommendationSnapshot.created_at == current.created_at,
                        RecommendationSnapshot.id < current.id,
                    ),
                ),
            )
            .order_by(RecommendationSnapshot.created_at.desc(), RecommendationSnapshot.id.desc())
            .limit(1)
            .first()
        )

    current_meta = {"snapshot_id": current.id, "created_at": _timestamp(current.created_at)}
    previous_meta = (
        {"snapshot_id": previous.id, "created_at": _timestamp(previous.created_at)}
        if previous is not None
        else None
    )
    if previous is None:
        return {
            "current": current_meta,
            "previous": None,
            "status": "no_previous",
            "sections": [],
            "as_of": _timestamp(datetime.utcnow()),
        }

    previous_regime = _decode_json(previous.regime_snapshot_json, dict)
    current_regime = _decode_json(current.regime_snapshot_json, dict)
    previous_constraints = _decode_json(previous.constraint_envelope_json, dict)
    current_constraints = _decode_json(current.constraint_envelope_json, dict)
    previous_policy = _decode_json(previous.active_policy_json, dict)
    current_policy = _decode_json(current.active_policy_json, dict)
    previous_consensus = _decode_json(previous.consensus_json, dict)
    current_consensus = _decode_json(current.consensus_json, dict)
    previous_allocations = _decode_json(previous.projected_allocations_json, list)
    current_allocations = _decode_json(current.projected_allocations_json, list)
    previous_dna = _decode_json(previous.portfolio_dna_json, dict)
    current_dna = _decode_json(current.portfolio_dna_json, dict)
    previous_style = _decode_json(previous.style_drift_json, dict)
    current_style = _decode_json(current.style_drift_json, dict)

    sections: list[dict[str, Any]] = []
    for section in (
        _scalar_section("regime", "Market regime", previous_regime, current_regime, _REGIME_FIELDS),
        _constraint_section(previous_constraints, current_constraints),
        _scalar_section("policy_posture", "Policy posture", previous_policy, current_policy, _POLICY_FIELDS),
        _scalar_section("consensus", "Consensus", previous_consensus, current_consensus, _CONSENSUS_FIELDS),
        _allocation_section(previous_allocations, current_allocations),
        _portfolio_characteristics_section(previous_dna, current_dna, previous_style, current_style),
    ):
        if section is not None:
            sections.append(section)

    return {
        "current": current_meta,
        "previous": previous_meta,
        "status": "ok",
        "sections": sections,
        "as_of": _timestamp(datetime.utcnow()),
    }
