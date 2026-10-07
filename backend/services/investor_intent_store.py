"""Investor Intent V1 persistence: current PositionIntent + append-only revisions.

Revision rows are append-only through this module (the only supported write
path): it never updates or deletes one. That is an application guarantee, not
a database one; direct ORM/SQL writes are not prevented.

Workspace- and portfolio-scoped. Never reads or writes allow_swap, trades or
decisions, and never creates intent on anyone's behalf.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.database import PortfolioItem, PositionIntent, PositionIntentRevision
from services.advisory_intent_flag import (
    DISCLOSURE_DISABLED, advisory_intent_review_enabled, intent_disclosure,
)
from services.investor_intent import (
    AUTHOR_OWNER, INTENT_CONTRACT_VERSION, STATUS_CONFIRMED, STATUS_RECONFIRMATION_REQUIRED,
    IntentState, intent_status,
)

# Wording when Advisory Integration V1 is off (the default); see intent_disclosure().
ENFORCEMENT_DISCLOSURE = DISCLOSURE_DISABLED


class PositionNotFoundError(LookupError):
    """No held position and no existing intent for this symbol in the portfolio."""


class IntentRevisionConflictError(RuntimeError):
    """expected_revision does not match the stored revision."""


def intent_payload(intent: PositionIntent) -> dict:
    return {
        "id": intent.id,
        "portfolio_id": intent.portfolio_id,
        "position_symbol": intent.position_symbol,
        "increase_prohibited": intent.increase_prohibited,
        "decrease_prohibited": intent.decrease_prohibited,
        "soft_preference": intent.soft_preference,
        "revision": intent.revision,
        "author_kind": intent.author_kind,
        "created_at": intent.created_at.isoformat(),
        "updated_at": intent.updated_at.isoformat(),
    }


def revision_payload(row: PositionIntentRevision) -> dict:
    return {
        "position_intent_id": row.position_intent_id,
        "revision": row.revision,
        "increase_prohibited": row.increase_prohibited,
        "decrease_prohibited": row.decrease_prohibited,
        "soft_preference": row.soft_preference,
        "author_kind": row.author_kind,
        "recorded_at": row.recorded_at.isoformat(),
    }


def intent_state(intent: PositionIntent | None) -> IntentState | None:
    """Domain view of the current revision; None keeps 'no confirmed intent' distinct.

    Does not check the holding episode; use applicable_intent_state for that.
    """
    if intent is None:
        return None
    return IntentState(intent.increase_prohibited, intent.decrease_prohibited,
                       intent.soft_preference, intent.id, intent.revision)


def _confirmed_at(db: Session, intents: list[PositionIntent]) -> dict[int, datetime]:
    """recorded_at of each intent's current revision row: when the owner last confirmed it."""
    if not intents:
        return {}
    current = {intent.id: intent.revision for intent in intents}
    rows = (
        db.query(PositionIntentRevision.position_intent_id, PositionIntentRevision.revision,
                 PositionIntentRevision.recorded_at)
        .filter(PositionIntentRevision.position_intent_id.in_(list(current)))
        .all()
    )
    return {intent_id: recorded_at for intent_id, revision, recorded_at in rows
            if current.get(intent_id) == revision}


def _status(intent: PositionIntent | None, item: PortfolioItem | None, confirmed_at: datetime | None) -> str:
    return intent_status(intent is not None, item.created_at if item is not None else None, confirmed_at)


def applicable_intent_state(db: Session, workspace_id: int, portfolio_id: int, symbol: str) -> IntentState | None:
    """The intent that applies to the current holding episode, or None.

    An intent that needs re-confirmation after a same-symbol re-entry is
    treated as no confirmed intent.
    """
    intent = get_position_intent(db, workspace_id, portfolio_id, symbol)
    if intent is None:
        return None
    item = _held_item(db, workspace_id, portfolio_id, symbol)
    status = _status(intent, item, _confirmed_at(db, [intent]).get(intent.id))
    return intent_state(intent) if status == STATUS_CONFIRMED else None


def get_position_intent(db: Session, workspace_id: int, portfolio_id: int, symbol: str) -> PositionIntent | None:
    return (
        db.query(PositionIntent)
        .filter(PositionIntent.workspace_id == workspace_id,
                PositionIntent.portfolio_id == portfolio_id,
                PositionIntent.position_symbol == symbol)
        .first()
    )


def _held_item(db: Session, workspace_id: int, portfolio_id: int, symbol: str) -> PortfolioItem | None:
    return (
        db.query(PortfolioItem)
        .filter(PortfolioItem.workspace_id == workspace_id,
                PortfolioItem.portfolio_id == portfolio_id,
                PortfolioItem.symbol == symbol)
        .first()
    )


def list_position_intent_view(db: Session, workspace_id: int, portfolio_id: int) -> dict:
    """Held positions plus any intents whose position is no longer held."""
    items = (
        db.query(PortfolioItem)
        .filter(PortfolioItem.workspace_id == workspace_id, PortfolioItem.portfolio_id == portfolio_id)
        .all()
    )
    intents = {
        row.position_symbol: row for row in
        db.query(PositionIntent)
        .filter(PositionIntent.workspace_id == workspace_id, PositionIntent.portfolio_id == portfolio_id)
        .all()
    }
    held = {item.symbol: item for item in items}
    confirmed_at = _confirmed_at(db, list(intents.values()))
    positions = []
    for symbol in sorted(set(held) | set(intents)):
        item, intent = held.get(symbol), intents.get(symbol)
        positions.append({
            "position_symbol": symbol,
            "currently_held": item is not None,
            # Legacy lock is shown as-is; it is never interpreted as intent.
            "legacy_allow_swap": item.allow_swap if item is not None else None,
            "legacy_lock_status": (
                "LEGACY_LOCKED_INTENT_UNCONFIRMED" if item is not None and not item.allow_swap else None
            ),
            # Start of the current continuously-held episode (PortfolioItem.created_at).
            "holding_started_at": (
                item.created_at.isoformat() if item is not None and item.created_at is not None else None
            ),
            "intent_status": _status(intent, item, confirmed_at.get(intent.id) if intent is not None else None),
            # Shown even when re-confirmation is required, as history; it does not apply then.
            "intent": intent_payload(intent) if intent is not None else None,
        })
    # Even with Advisory Integration V1 on, intent is advisory context plus a
    # deterministic review, never enforcement: enforced_by_optimizer stays False.
    return {"contract_version": INTENT_CONTRACT_VERSION, "portfolio_id": portfolio_id,
            "enforced_by_optimizer": False, "disclosure": intent_disclosure(),
            "advisory_review_enabled": advisory_intent_review_enabled(),
            "positions": positions}


def held_intent_applicability(
    db: Session, workspace_id: int, portfolio_id: int, items: list[PortfolioItem],
) -> dict[str, dict]:
    """Bulk applicability of intent for the given held items (two queries).

    Returns {symbol: {"status", "intent", "confirmed_at"}} for every item.
    "intent" is the applicable IntentState only when CONFIRMED; for
    RECONFIRMATION_REQUIRED it is None and "historical_intent" carries the
    stored revision as non-applicable evidence.
    """
    symbols = sorted({item.symbol for item in items})
    intents = {
        row.position_symbol: row for row in
        db.query(PositionIntent)
        .filter(PositionIntent.workspace_id == workspace_id,
                PositionIntent.portfolio_id == portfolio_id,
                PositionIntent.position_symbol.in_(symbols))
        .all()
    } if symbols else {}
    confirmed_at = _confirmed_at(db, list(intents.values()))
    result: dict[str, dict] = {}
    for item in items:
        intent = intents.get(item.symbol)
        when = confirmed_at.get(intent.id) if intent is not None else None
        status = _status(intent, item, when)
        result[item.symbol] = {
            "status": status,
            "intent": intent_state(intent) if status == STATUS_CONFIRMED else None,
            "confirmed_at": when,
            "historical_intent": (
                {**intent_payload(intent), "confirmed_at": when.isoformat() if when else None}
                if intent is not None and status != STATUS_CONFIRMED else None
            ),
        }
    return result


def current_intent_revisions(
    db: Session, workspace_id: int, portfolio_id: int, symbols: list[str],
) -> dict[str, int]:
    """Current stored revision per symbol (for "changed since this run" display only)."""
    if not symbols:
        return {}
    return {
        row.position_symbol: row.revision for row in
        db.query(PositionIntent)
        .filter(PositionIntent.workspace_id == workspace_id,
                PositionIntent.portfolio_id == portfolio_id,
                PositionIntent.position_symbol.in_(sorted(set(symbols))))
        .all()
    }


def put_position_intent(
    db: Session,
    workspace_id: int,
    portfolio_id: int,
    symbol: str,
    *,
    increase_prohibited: bool,
    decrease_prohibited: bool,
    soft_preference: str,
    expected_revision: int | None,
) -> tuple[PositionIntent, str]:
    """Create (expected_revision=None) or revise an intent.

    Returns (row, CREATED|REVISED|RECONFIRMED|UNCHANGED). Creating requires a
    currently held position. Revising an existing intent is allowed after the
    position is sold, so the owner can still change it. An identical write
    records no new revision, except when the intent needs re-confirmation for
    the current holding episode: then it appends a revision (RECONFIRMED),
    whose recorded_at confirms the intent for this episode.
    """
    IntentState(increase_prohibited, decrease_prohibited, soft_preference)  # validates values
    existing = get_position_intent(db, workspace_id, portfolio_id, symbol)
    if existing is None:
        if expected_revision is not None:
            raise IntentRevisionConflictError("Intent does not exist; expected_revision must be null")
        if _held_item(db, workspace_id, portfolio_id, symbol) is None:
            raise PositionNotFoundError(symbol)
        now = datetime.utcnow()
        intent = PositionIntent(
            workspace_id=workspace_id, portfolio_id=portfolio_id, position_symbol=symbol,
            increase_prohibited=increase_prohibited, decrease_prohibited=decrease_prohibited,
            soft_preference=soft_preference, revision=1, author_kind=AUTHOR_OWNER,
            created_at=now, updated_at=now,
        )
        db.add(intent)
        try:
            db.flush()
        except IntegrityError as exc:
            db.rollback()
            raise IntentRevisionConflictError("Intent was created concurrently") from exc
        status = "CREATED"
    else:
        if expected_revision != existing.revision:
            raise IntentRevisionConflictError(
                f"Intent is at revision {existing.revision}; expected_revision was {expected_revision}"
            )
        unchanged = (existing.increase_prohibited, existing.decrease_prohibited, existing.soft_preference) == (
            increase_prohibited, decrease_prohibited, soft_preference
        )
        if unchanged:
            item = _held_item(db, workspace_id, portfolio_id, symbol)
            needs_reconfirmation = _status(
                existing, item, _confirmed_at(db, [existing]).get(existing.id)
            ) == STATUS_RECONFIRMATION_REQUIRED
            if not needs_reconfirmation:
                return existing, "UNCHANGED"
        intent = existing
        now = datetime.utcnow()
        intent.increase_prohibited = increase_prohibited
        intent.decrease_prohibited = decrease_prohibited
        intent.soft_preference = soft_preference
        intent.revision = existing.revision + 1
        intent.updated_at = now
        status = "RECONFIRMED" if unchanged else "REVISED"
    db.add(PositionIntentRevision(
        workspace_id=workspace_id, position_intent_id=intent.id, revision=intent.revision,
        increase_prohibited=intent.increase_prohibited, decrease_prohibited=intent.decrease_prohibited,
        soft_preference=intent.soft_preference, author_kind=AUTHOR_OWNER, recorded_at=now,
    ))
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise IntentRevisionConflictError("Intent was revised concurrently") from exc
    db.refresh(intent)
    return intent, status


def list_revisions(db: Session, workspace_id: int, portfolio_id: int, symbol: str) -> list[dict]:
    intent = get_position_intent(db, workspace_id, portfolio_id, symbol)
    if intent is None:
        raise PositionNotFoundError(symbol)
    return [revision_payload(row) for row in intent.revisions]
