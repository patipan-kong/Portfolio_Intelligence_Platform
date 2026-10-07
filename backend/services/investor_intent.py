"""Investor Intent V1 — pure, deterministic domain contract.

No database, network, AI, optimizer or Stock Analysis dependency. This module
does not decide who wins a disagreement: when a proposal contradicts a
confirmed owner restriction it returns CONFLICT carrying both facts.

Direction is judged on SHARE QUANTITY only. A weight change caused by price
movement is not an owner-directed increase or decrease, so callers must pass
quantities, never weights. Not wired into the production optimizer; see
docs/implementation/INVESTOR_INTENT_V1.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite

INTENT_CONTRACT_VERSION = "investor-intent.v1"

SOFT_PREFERENCES = ("NONE", "PREFER_KEEP", "PREFER_EXIT")
AUTHOR_OWNER = "OWNER"

# Same share tolerance as execute_sell's oversell check (portfolio_transactions).
QUANTITY_TOLERANCE = 0.0001

INCREASE = "INCREASE"
DECREASE = "DECREASE"
NO_CHANGE = "NO_CHANGE"

# Permission of a quantity change under intent.
ALLOWED = "ALLOWED"
PROHIBITED = "PROHIBITED"
UNRESOLVED = "UNRESOLVED"

# Outcome of a sourced proposal under intent.
CONSISTENT = "CONSISTENT"
CONFLICT = "CONFLICT"

# Who proposed the change. Owner-entered execution decisions are not evaluated
# in V1: the human is the final authority at execution.
SOURCE_ADVISORY = "ADVISORY"        # AI / advisor recommendation
SOURCE_SYSTEM_RULE = "SYSTEM_RULE"  # deterministic system rule, e.g. forced exit
SOURCE_POLICY_RISK = "POLICY_RISK"  # portfolio policy or risk guidance
PROPOSAL_SOURCES = (SOURCE_ADVISORY, SOURCE_SYSTEM_RULE, SOURCE_POLICY_RISK)

_CONFLICT_KIND = {
    SOURCE_ADVISORY: "INTENT_ADVISORY_CONFLICT",
    SOURCE_SYSTEM_RULE: "INTENT_SYSTEM_RULE_CONFLICT",
    SOURCE_POLICY_RISK: "INTENT_POLICY_CONFLICT",
}


# Intent status of one position for the current holding episode.
STATUS_CONFIRMED = "CONFIRMED"
STATUS_NO_CONFIRMED_INTENT = "NO_CONFIRMED_INTENT"
STATUS_RECONFIRMATION_REQUIRED = "RECONFIRMATION_REQUIRED"


def intent_status(
    has_intent: bool,
    holding_started_at: datetime | None,
    confirmed_at: datetime | None,
) -> str:
    """Whether a stored intent applies to the current holding episode.

    holding_started_at is PortfolioItem.created_at: the start of the current
    continuously-held (portfolio_id, symbol) episode (None when not held or a
    legacy row without a value). confirmed_at is the recorded_at of the
    intent's current revision row, i.e. when the owner last confirmed it.

    An intent last confirmed before the current episode began (a full exit and
    later same-symbol re-entry) does not carry over: RECONFIRMATION_REQUIRED.
    A missing confirmation record fails closed to RECONFIRMATION_REQUIRED.
    """
    if not has_intent:
        return STATUS_NO_CONFIRMED_INTENT
    if confirmed_at is None:
        return STATUS_RECONFIRMATION_REQUIRED
    if holding_started_at is not None and holding_started_at > confirmed_at:
        return STATUS_RECONFIRMATION_REQUIRED
    return STATUS_CONFIRMED


@dataclass(frozen=True)
class IntentState:
    """One confirmed intent revision. Absence is represented by None, not by this."""
    increase_prohibited: bool
    decrease_prohibited: bool
    soft_preference: str
    intent_id: int | None = None
    revision: int | None = None

    def __post_init__(self):
        for name in ("increase_prohibited", "decrease_prohibited"):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f"{name} must be a bool")
        if self.soft_preference not in SOFT_PREFERENCES:
            raise ValueError(f"soft_preference must be one of {SOFT_PREFERENCES}")


def _quantity(value, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite non-negative number")
    return float(value)


def quantity_direction(current_quantity: float, proposed_quantity: float) -> str:
    """Direction of a share-quantity change.

    Zero is an exact boundary: positive -> 0 is a full exit (DECREASE) and
    0 -> positive is an entry (INCREASE), however small the position. The
    transaction layer removes a holding only at <= 0 shares, so any positive
    quantity is a real holding. QUANTITY_TOLERANCE absorbs float accounting
    noise only between two non-zero quantities.
    """
    current = _quantity(current_quantity, "current_quantity")
    proposed = _quantity(proposed_quantity, "proposed_quantity")
    if current == proposed:
        return NO_CHANGE
    if proposed == 0:
        return DECREASE
    if current == 0:
        return INCREASE
    if proposed > current + QUANTITY_TOLERANCE:
        return INCREASE
    if proposed < current - QUANTITY_TOLERANCE:
        return DECREASE
    return NO_CHANGE


def _intent_ref(intent: IntentState | None) -> dict | None:
    if intent is None:
        return None
    return {"intent_id": intent.intent_id, "revision": intent.revision,
            "increase_prohibited": intent.increase_prohibited,
            "decrease_prohibited": intent.decrease_prohibited,
            "soft_preference": intent.soft_preference}


def evaluate_quantity_change(
    intent: IntentState | None,
    current_quantity: float | None,
    proposed_quantity: float,
) -> dict:
    """Permission of one quantity change: ALLOWED, PROHIBITED or UNRESOLVED.

    current_quantity=None means the position is absent from the referenced
    holdings snapshot; V1 does not define re-entry semantics, so UNRESOLVED.
    Soft preference never affects the outcome; it is returned as context.
    """
    if current_quantity is None:
        _quantity(proposed_quantity, "proposed_quantity")
        return {"contract_version": INTENT_CONTRACT_VERSION, "permission": UNRESOLVED,
                "direction": None, "reasons": ["POSITION_NOT_IN_REFERENCED_HOLDINGS"],
                "intent": _intent_ref(intent)}
    direction = quantity_direction(current_quantity, proposed_quantity)
    if direction == NO_CHANGE:
        # Not changing quantity needs no permission, with or without intent.
        permission, reasons = ALLOWED, ["NO_QUANTITY_CHANGE"]
    elif intent is None:
        permission, reasons = UNRESOLVED, ["NO_CONFIRMED_INTENT"]
    elif direction == INCREASE and intent.increase_prohibited:
        permission, reasons = PROHIBITED, ["INCREASE_PROHIBITED_BY_OWNER"]
    elif direction == DECREASE and intent.decrease_prohibited:
        permission, reasons = PROHIBITED, ["DECREASE_PROHIBITED_BY_OWNER"]
    else:
        permission, reasons = ALLOWED, ["NOT_RESTRICTED_BY_CONFIRMED_INTENT"]
    return {"contract_version": INTENT_CONTRACT_VERSION, "permission": permission,
            "direction": direction, "reasons": reasons, "intent": _intent_ref(intent)}


def evaluate_proposal(
    intent: IntentState | None,
    current_quantity: float | None,
    proposed_quantity: float,
    *,
    source: str,
    reason: str,
) -> dict:
    """Evaluate an advisory/system/policy proposal: CONSISTENT, CONFLICT or UNRESOLVED.

    A CONFLICT keeps the owner restriction AND the proposal's reason. It does
    not resolve the disagreement; the owner decides.
    """
    if source not in PROPOSAL_SOURCES:
        raise ValueError(f"source must be one of {PROPOSAL_SOURCES}")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a non-empty string")
    permission = evaluate_quantity_change(intent, current_quantity, proposed_quantity)
    outcome = {ALLOWED: CONSISTENT, PROHIBITED: CONFLICT, UNRESOLVED: UNRESOLVED}[permission["permission"]]
    return {**permission, "outcome": outcome,
            "proposal": {"source": source, "direction": permission["direction"], "reason": reason},
            "owner_restriction": permission["reasons"][0] if outcome == CONFLICT else None,
            "conflict_kind": _CONFLICT_KIND[source] if outcome == CONFLICT else None,
            "requires_owner_decision": outcome == CONFLICT}
