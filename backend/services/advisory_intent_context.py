"""Advisory Integration V1 (Slice 1): run-scoped frozen Investor Intent context.

Built ONCE per enabled /analyze/optimizer run, before any AI call, from the
holdings that run already references. L1/L2/L3, retries and the single-shot
fallback only ever see this frozen object; none of them query Intent
persistence. Also owns the canonical common-NAV basis, the share-quantity
projection and the bounded proposal-transition ledger used by the review.

Nothing here decides who wins: hard Intent is advisory context, never an
automatic winner over policy, and soft preference is never scored.
"""
from __future__ import annotations

import hashlib
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from services.investor_intent import (
    DECREASE,
    INCREASE,
    NO_CHANGE,
    SOURCE_ADVISORY,
    SOURCE_POLICY_RISK,
    SOURCE_SYSTEM_RULE,
    STATUS_CONFIRMED,
    STATUS_NO_CONFIRMED_INTENT,
    IntentState,
)

_log = logging.getLogger(__name__)

SHARE_QUANTUM = Decimal("0.000001")
_HUNDRED = Decimal(100)
# Platform cash convention: every cash/goal/liability amount is THB-constrained
# (CheckConstraint currency = 'THB'); Portfolio.cash_balance has no currency column.
CASH_UNIT = "THB"

PRECISION_RULES = {
    "arithmetic": "decimal",
    "serialization": "exact decimal strings",
    "share_quantum": str(SHARE_QUANTUM),
    "share_rounding": "ROUND_HALF_UP",
    "display_rounding": "display fields only; never fed back into projection",
}

# ── Bounded provenance vocabulary ─────────────────────────────────────────────
EFFECT_ORIGINATE = "ORIGINATE"
EFFECT_REPLACE = "REPLACE"
EFFECT_SUPPRESS = "SUPPRESS"
EFFECT_RELABEL = "RELABEL"
EFFECT_DEFER = "DEFER"
EFFECT_SCALE = "SCALE"
EFFECTS = (EFFECT_ORIGINATE, EFFECT_REPLACE, EFFECT_SUPPRESS, EFFECT_RELABEL, EFFECT_DEFER, EFFECT_SCALE)

ACTIVE = "ACTIVE"
REPLACED = "REPLACED"
SUPPRESSED = "SUPPRESSED"
ABANDONED = "ABANDONED"

SOURCES = (SOURCE_ADVISORY, SOURCE_SYSTEM_RULE, SOURCE_POLICY_RISK)

STAGE_L1 = "L1_STRATEGIST"
STAGE_L2 = "L2_ALLOCATION"
STAGE_FALLBACK = "FALLBACK_ALLOCATION"
STAGE_FORCED_SELL = "FORCED_SELL"
STAGE_LEGACY_LOCK = "LEGACY_ALLOW_SWAP"
STAGE_HARD_POLICY = "HARD_POLICY"
STAGE_EXECUTION_CAP = "EXECUTION_QUALITY_CAP"
STAGE_RECONCILIATION = "ACTION_RECONCILIATION"
STAGE_NEUTRAL_SNAP = "NEUTRAL_SNAP"
STAGE_STABILIZATION = "STABILIZATION"
STAGE_NOISE_FILTER = "NOISE_FILTER"
STAGE_EXECUTION_SCHEDULING = "EXECUTION_SCHEDULING"

ATTEMPT_PRIMARY = "PRIMARY"
ATTEMPT_FALLBACK = "FALLBACK"

# Materiality. L1 strategist legs are intermediate advisory reasoning: once the
# accepted allocation (L2/fallback) supersedes them they stay in provenance for
# audit but never count as an owner-facing Intent conflict. The accepted
# allocation plus the deterministic system/policy mutations downstream of it is
# the material recommendation path.
MATERIAL = "MATERIAL"
INTERMEDIATE_REASONING = "INTERMEDIATE_REASONING"

# Temporary mixed-basis boundary (Slice 1). Only the advisory prompt current
# weights, the allocation rows' current_weight and the canonical quantity
# projection use the frozen common NAV. Every deterministic rule keeps its
# legacy semantics; its targets are projected onto the NAV for review only.
MIXED_BASIS_BOUNDARY = "SLICE1_TEMPORARY_MIXED_BASIS"
BASIS_COMMON_NAV = "COMMON_NAV_FROZEN_QUOTES"
BASIS_LEGACY_EQUITY_ONLY = "LEGACY_EQUITY_ONLY"
SEMANTICS_ADVISORY = "ADVISORY_MODEL_OUTPUT"
SEMANTICS_LEGACY_POLICY = "LEGACY_POLICY_RULE"
SEMANTICS_LEGACY_SYSTEM = "LEGACY_SYSTEM_RULE"
_STAGE_SEMANTICS = {
    STAGE_L1: SEMANTICS_ADVISORY,
    STAGE_L2: SEMANTICS_ADVISORY,
    STAGE_FALLBACK: SEMANTICS_ADVISORY,
    STAGE_HARD_POLICY: SEMANTICS_LEGACY_POLICY,
    STAGE_EXECUTION_CAP: SEMANTICS_LEGACY_POLICY,
    STAGE_FORCED_SELL: SEMANTICS_LEGACY_SYSTEM,
    STAGE_LEGACY_LOCK: SEMANTICS_LEGACY_SYSTEM,
    STAGE_RECONCILIATION: SEMANTICS_LEGACY_SYSTEM,
    STAGE_NEUTRAL_SNAP: SEMANTICS_LEGACY_SYSTEM,
    STAGE_STABILIZATION: SEMANTICS_LEGACY_SYSTEM,
    STAGE_NOISE_FILTER: SEMANTICS_LEGACY_SYSTEM,
    STAGE_EXECUTION_SCHEDULING: SEMANTICS_LEGACY_SYSTEM,
}
MIXED_BASIS_SCOPE = {
    "name": MIXED_BASIS_BOUNDARY,
    "common_nav_applies_to": [
        "ADVISORY_PROMPT_CURRENT_WEIGHTS", "ALLOCATION_ROW_CURRENT_WEIGHT",
        "CANONICAL_QUANTITY_PROJECTION", "INTENT_REVIEW",
    ],
    "legacy_basis_retained_for": [
        "POLICY_ENVELOPE_INPUTS", "TIER1_BREACH_DETECTION", "CURRENT_SECTOR_WEIGHTS",
        "HARD_POLICY_RULES", "EXECUTION_QUALITY_CAP", "FORCED_SELL", "LEGACY_ALLOW_SWAP",
        "ACTION_RECONCILIATION", "NEUTRAL_SNAP", "STABILIZATION", "NOISE_FILTER",
        "EXECUTION_SCHEDULING",
    ],
    "note": ("Rule-derived targets keep their legacy rule semantics; the review projects the "
             "resulting target onto the frozen common NAV without implying the rule used it. "
             "Rules that read a row's current_weight read the common-NAV value when the basis "
             "resolved (row_current_weight_basis)."),
}

# Quote / valuation evidence codes.
QUOTE_OK = "OK"
QUOTE_MISSING = "QUOTE_MISSING"
QUOTE_NOT_POSITIVE = "QUOTE_ZERO_OR_NEGATIVE"
QUOTE_STALE = "QUOTE_STALE"
QUOTE_QUARANTINED = "QUOTE_QUARANTINED"
QUOTE_CACHE_MISS = "QUOTE_CACHE_MISS"
QUOTE_INVALID = "QUOTE_INVALID"

RESOLVED = "RESOLVED"
UNRESOLVED_BASIS = "UNRESOLVED"

_NEUTRAL_ACTIONS = ("HOLD", "WATCH")
_INCREASE_ACTIONS = ("BUY", "ACCUMULATE")
_DECREASE_ACTIONS = ("REDUCE", "SELL")


def to_decimal(value) -> Decimal | None:
    """Exact Decimal of a finite number (via str, so 0.1 stays 0.1), else None."""
    if value is None or isinstance(value, bool):
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None
    return result if result.is_finite() else None


def dec_str(value: Decimal | None) -> str | None:
    return None if value is None else format(value.normalize(), "f") if value != 0 else "0"


def canonical_digest(payload) -> str:
    """sha256 over sorted-key, compact JSON — the envelope canonicalization."""
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── Frozen context ────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class HeldPosition:
    symbol: str
    shares: Decimal
    holding_started_at: str | None
    legacy_allow_swap: bool
    applicability: str
    intent: IntentState | None           # applicable intent only (CONFIRMED)
    confirmed_at: str | None
    historical_intent: dict | None       # non-applicable evidence (RECONFIRMATION_REQUIRED)


@dataclass(frozen=True)
class QuoteEvidence:
    symbol: str
    price: Decimal | None
    status: str
    last_updated: str | None
    currency: str | None
    source: str = "data_fetcher.fetch_price_info"


@dataclass(frozen=True)
class ValuationBasis:
    status: str
    reasons: tuple[str, ...]
    unit: str | None
    cash: Decimal
    equity: Decimal | None
    nav: Decimal | None
    values: dict
    quotes: dict

    @property
    def resolved(self) -> bool:
        return self.status == RESOLVED


def _quote_evidence(symbol: str, raw: dict | None, currency: str | None) -> QuoteEvidence:
    raw = raw or {}
    last_updated = raw.get("last_updated")
    last_updated = None if last_updated is None else str(last_updated)
    if raw.get("_quarantine_reason"):
        return QuoteEvidence(symbol, None, QUOTE_QUARANTINED, last_updated, currency)
    if raw.get("_vps_cache_miss"):
        return QuoteEvidence(symbol, None, QUOTE_CACHE_MISS, last_updated, currency)
    if raw.get("current_price") is None:
        return QuoteEvidence(symbol, None, QUOTE_MISSING, last_updated, currency)
    price = to_decimal(raw.get("current_price"))
    if price is None:
        return QuoteEvidence(symbol, None, QUOTE_INVALID, last_updated, currency)
    if price <= 0:
        return QuoteEvidence(symbol, price, QUOTE_NOT_POSITIVE, last_updated, currency)
    if raw.get("_stale_data"):
        return QuoteEvidence(symbol, price, QUOTE_STALE, last_updated, currency)
    return QuoteEvidence(symbol, price, QUOTE_OK, last_updated, currency)


def build_valuation_basis(
    positions: list[HeldPosition],
    anomalies: list[dict],
    quote_evidence: dict[str, dict],
    currency_by_symbol: dict[str, str | None],
    cash_balance,
) -> ValuationBasis:
    """Common-unit NAV N = E + C from frozen held quotes, or UNRESOLVED.

    Never substitutes average cost for a missing quote and never converts
    currencies: an unestablished common unit leaves legacy advice in place and
    makes the quantity review UNRESOLVED instead of fabricating a portfolio.
    """
    reasons: list[str] = []
    cash = to_decimal(cash_balance)
    if cash is None:
        reasons.append("CASH_BALANCE_INVALID")
        cash = Decimal(0)
    for anomaly in anomalies:
        if anomaly["code"] in ("DUPLICATE_HOLDING", "NEGATIVE_SHARE_HOLDING", "INVALID_SHARE_QUANTITY"):
            reasons.append(anomaly["code"])

    quotes: dict[str, QuoteEvidence] = {}
    values: dict[str, Decimal] = {}
    units: set[str] = set()
    for position in positions:
        currency = currency_by_symbol.get(position.symbol)
        evidence = _quote_evidence(position.symbol, quote_evidence.get(position.symbol), currency)
        quotes[position.symbol] = evidence
        if evidence.status != QUOTE_OK:
            reasons.append(evidence.status)
        else:
            values[position.symbol] = position.shares * evidence.price
        if currency is None or not str(currency).strip():
            reasons.append("CURRENCY_UNKNOWN")
        else:
            units.add(str(currency).strip().upper())
    if cash != 0:
        units.add(CASH_UNIT)
    if len(units) > 1:
        reasons.append("CURRENCY_MIXED")

    reasons = sorted(set(reasons))
    if reasons:
        return ValuationBasis(UNRESOLVED_BASIS, tuple(reasons), None, cash, None, None, {}, quotes)
    equity = sum(values.values(), Decimal(0))
    nav = equity + cash
    if nav <= 0:
        return ValuationBasis(UNRESOLVED_BASIS, ("NON_POSITIVE_NAV",), None, cash, equity, nav, values, quotes)
    unit = next(iter(units)) if units else CASH_UNIT
    return ValuationBasis(RESOLVED, (), unit, cash, equity, nav, values, quotes)


# ── Canonical quantity projection ─────────────────────────────────────────────

def _weight_direction(action: str, target, current) -> str | None:
    """Direction a (action, target, current) basis implies; None if not determinable."""
    if action in _NEUTRAL_ACTIONS:
        return NO_CHANGE
    target_d, current_d = to_decimal(target), to_decimal(current)
    if action == "SELL" and target_d == 0:
        return DECREASE
    if target_d is None or current_d is None:
        return INCREASE if action in _INCREASE_ACTIONS else DECREASE if action in _DECREASE_ACTIONS else None
    if target_d > current_d:
        return INCREASE
    if target_d < current_d:
        return DECREASE
    return NO_CHANGE


def project_quantity(position: HeldPosition, basis: ValuationBasis, action, target_weight) -> dict:
    """Share-quantity projection of one finalized (action, target weight).

    HOLD/WATCH is the explicit unchanged control (q0); SELL to 0 is the
    explicit full exit; otherwise target_amount = N*t/100 at the frozen quote.
    Direction comes from quantities, never from whichever label looks
    compliant: if the action's direction and the quantity's disagree, the
    projection is UNRESOLVED.
    """
    action = str(action or "").upper()
    q0 = position.shares
    out = {"action": action or None, "target_weight": dec_str(to_decimal(target_weight)),
           "kind": None, "resolved": False, "reasons": [],
           "referenced_shares": dec_str(q0), "proposed_shares": None, "proposed_shares_raw": None,
           "delta_shares_raw": None, "target_amount": None, "delta_amount": None,
           "current_value": None, "current_weight": None, "direction": None}
    value = basis.values.get(position.symbol)
    price = basis.quotes[position.symbol].price if position.symbol in basis.quotes else None
    if basis.resolved and value is not None:
        out["current_value"] = dec_str(value)
        out["current_weight"] = dec_str(_HUNDRED * value / basis.nav)

    if action in _NEUTRAL_ACTIONS:
        out.update(kind="UNCHANGED_CONTROL", resolved=True, proposed_shares=dec_str(q0),
                   proposed_shares_raw=dec_str(q0), delta_shares_raw="0", direction=NO_CHANGE,
                   target_amount=dec_str(value) if value is not None else None,
                   delta_amount="0" if value is not None else None)
        return out
    t = to_decimal(target_weight)
    if action == "SELL" and t == 0:
        out.update(kind="FULL_EXIT", resolved=True, proposed_shares="0", proposed_shares_raw="0",
                   delta_shares_raw=dec_str(-q0), direction=DECREASE, target_amount="0",
                   delta_amount=dec_str(-value) if value is not None else None)
        return out
    if action not in _INCREASE_ACTIONS + _DECREASE_ACTIONS:
        out["reasons"].append("UNKNOWN_ACTION")
        return out
    out["kind"] = "TARGET_WEIGHT"
    if t is None or t < 0 or t > _HUNDRED:
        out["reasons"].append("INVALID_TARGET_WEIGHT")
        return out
    if not basis.resolved or value is None or price is None:
        out["reasons"].append("VALUATION_BASIS_UNRESOLVED")
        return out
    target_amount = basis.nav * t / _HUNDRED
    raw = target_amount / price
    proposed = raw.quantize(SHARE_QUANTUM, rounding=ROUND_HALF_UP)
    direction = INCREASE if proposed > q0 else DECREASE if proposed < q0 else NO_CHANGE
    out.update(proposed_shares=dec_str(proposed), proposed_shares_raw=dec_str(raw),
               delta_shares_raw=dec_str(raw - q0), target_amount=dec_str(target_amount),
               delta_amount=dec_str(target_amount - value), direction=direction)
    implied = INCREASE if action in _INCREASE_ACTIONS else DECREASE
    if direction != implied:
        out["reasons"].append("ACTION_QUANTITY_DIRECTION_MISMATCH")
        return out
    out["resolved"] = True
    return out


def project_direction_only(position: HeldPosition, action: str) -> dict:
    """An L1 swap leg names a direction but no target: quantity is not resolvable."""
    action = str(action or "").upper()
    direction = INCREASE if action in _INCREASE_ACTIONS else DECREASE if action in _DECREASE_ACTIONS else None
    return {"action": action, "target_weight": None, "kind": "DIRECTION_ONLY",
            "resolved": direction is not None, "reasons": [] if direction else ["UNKNOWN_ACTION"],
            "referenced_shares": dec_str(position.shares), "proposed_shares": None,
            "proposed_shares_raw": None, "delta_shares_raw": None, "target_amount": None,
            "delta_amount": None, "current_value": None, "current_weight": None,
            "direction": direction}


# ── Bounded proposal provenance ───────────────────────────────────────────────

@dataclass
class _Proposal:
    proposal_id: str
    symbol: str
    attempt: str
    source: str
    stage: str
    reason_code: str
    reason_text: str
    action: str | None
    target_weight: object
    current_weight: object
    direction_only: bool = False
    materiality: str = MATERIAL
    target_stage: str | None = None        # stage that last set target_weight
    disposition: str = ACTIVE
    replaced_proposal_id: str | None = None
    replaced_by: str | None = None
    suppressed_by: str | None = None
    deferred_by: list = field(default_factory=list)

    @property
    def target_semantics(self) -> str | None:
        return _STAGE_SEMANTICS.get(self.target_stage)

    def as_dict(self) -> dict:
        return {"proposal_id": self.proposal_id, "symbol": self.symbol, "attempt": self.attempt,
                "source": self.source, "stage": self.stage, "reason_code": self.reason_code,
                "reason_text": self.reason_text, "action": self.action,
                "target_weight": dec_str(to_decimal(self.target_weight)),
                "target_origin_stage": self.target_stage, "target_origin_semantics": self.target_semantics,
                "direction_only": self.direction_only, "materiality": self.materiality,
                "disposition": self.disposition,
                "replaced_proposal_id": self.replaced_proposal_id, "replaced_by": self.replaced_by,
                "suppressed_by": self.suppressed_by, "deferred_by": list(self.deferred_by)}


class ProposalLedger:
    """Run-scoped proposal transitions for held symbols. Not event sourcing.

    Mutation sites report (before, after) at the moment they mutate a row;
    nothing is reconstructed from the final row. A proposal from an abandoned
    attempt (primary pipeline that fell back) is ABANDONED and never reviewed.
    """

    def __init__(self, held: set[str], row_current_weight_basis: str = BASIS_LEGACY_EQUITY_ONLY):
        self._held = set(held)
        self.row_current_weight_basis = row_current_weight_basis
        self._attempt = ATTEMPT_PRIMARY
        self._seq = 0
        self._proposals: list[_Proposal] = []
        self._active: dict[str, _Proposal] = {}
        self.transitions: list[dict] = []
        self.scheduled: dict[str, dict] = {}
        self.capture_errors: list[str] = []

    @property
    def attempt(self) -> str:
        return self._attempt

    def begin_attempt(self, attempt: str) -> None:
        self._attempt = attempt

    def abandon_attempt(self, attempt: str) -> None:
        for proposal in self._proposals:
            if proposal.attempt == attempt and proposal.disposition != ABANDONED:
                proposal.disposition = ABANDONED
        self._active = {s: p for s, p in self._active.items() if p.attempt != attempt}

    def proposals(self, symbol: str) -> list[_Proposal]:
        return [p for p in self._proposals if p.symbol == symbol]

    def active(self, symbol: str) -> _Proposal | None:
        return self._active.get(symbol)

    def _new(self, symbol, source, stage, reason_code, reason_text, after, direction_only=False,
             materiality=MATERIAL) -> _Proposal:
        proposal = _Proposal(
            proposal_id=f"P{len(self._proposals) + 1}", symbol=symbol, attempt=self._attempt,
            source=source, stage=stage, reason_code=reason_code, reason_text=reason_text,
            action=(after or {}).get("action"), target_weight=(after or {}).get("target_weight"),
            current_weight=(after or {}).get("current_weight"), direction_only=direction_only,
            materiality=materiality, target_stage=stage,
        )
        self._proposals.append(proposal)
        self._active[symbol] = proposal
        return proposal

    def observe(self, symbol: str, *, stage: str, source: str, effect: str, reason_code: str,
                reason_text: str = "", before: dict | None = None, after: dict | None = None,
                direction_only: bool = False, scheduled: dict | None = None) -> None:
        if symbol not in self._held:
            return
        if effect not in EFFECTS or source not in SOURCES:
            raise ValueError(f"unbounded provenance value: {effect}/{source}")
        current = self._active.get(symbol)
        if effect == EFFECT_ORIGINATE and current is not None:
            effect = EFFECT_REPLACE
        if effect == EFFECT_SCALE and before and after:
            flip = _weight_direction(before.get("action"), before.get("target_weight"), before.get("current_weight")) \
                != _weight_direction(after.get("action"), after.get("target_weight"), after.get("current_weight"))
            if flip:
                effect = EFFECT_REPLACE   # a trim that reverses direction is a new proposal
        replaced = None
        if effect in (EFFECT_ORIGINATE, EFFECT_REPLACE) or (effect == EFFECT_SUPPRESS and after):
            # An L1 leg is intermediate reasoning, and so is the placeholder left
            # when the legacy lock drops that leg; everything else is material.
            intermediate = stage == STAGE_L1 or (
                effect == EFFECT_SUPPRESS and stage == STAGE_LEGACY_LOCK
                and current is not None and current.materiality == INTERMEDIATE_REASONING)
            if current is not None:
                current.disposition = REPLACED if effect == EFFECT_REPLACE else SUPPRESSED
                if effect == EFFECT_SUPPRESS:
                    current.suppressed_by = stage
                replaced = current.proposal_id
            proposal = self._new(symbol, source, stage, reason_code, reason_text, after, direction_only,
                                 INTERMEDIATE_REASONING if intermediate else MATERIAL)
            proposal.replaced_proposal_id = replaced
            if current is not None and effect == EFFECT_REPLACE:
                current.replaced_by = proposal.proposal_id
        elif current is None:
            self.capture_errors.append(f"{symbol}:{stage}:{effect}:NO_ACTIVE_PROPOSAL")
            return
        else:
            proposal = current
            if effect in (EFFECT_SCALE, EFFECT_RELABEL) and after:
                if to_decimal(after.get("target_weight")) != to_decimal(proposal.target_weight):
                    proposal.target_stage = stage   # e.g. a policy cap: the target is now rule-derived
                proposal.action = after.get("action")
                proposal.target_weight = after.get("target_weight")
                proposal.current_weight = after.get("current_weight")
            elif effect == EFFECT_DEFER:
                proposal.deferred_by.append(stage)
            if scheduled is not None:
                self.scheduled[symbol] = scheduled
        self._seq += 1
        self.transitions.append({
            "seq": self._seq, "symbol": symbol, "attempt": self._attempt,
            "proposal_id": proposal.proposal_id, "replaced_proposal_id": replaced,
            "source": source, "stage": stage, "effect": effect, "reason_code": reason_code,
            "reason_text": reason_text,
            "rule_semantics": _STAGE_SEMANTICS.get(stage),
            "row_current_weight_basis": self.row_current_weight_basis,
            "materiality": proposal.materiality,
            "before": _basis_view(before), "after": _basis_view(after),
            "resulting_disposition": proposal.disposition,
        })

    def proposals_view(self) -> list[dict]:
        return [p.as_dict() for p in self._proposals]


def _basis_view(basis: dict | None) -> dict | None:
    if basis is None:
        return None
    return {"action": basis.get("action"), "target_weight": dec_str(to_decimal(basis.get("target_weight"))),
            "current_weight": dec_str(to_decimal(basis.get("current_weight")))}


# ── Prompt context ────────────────────────────────────────────────────────────

LAYER_L1 = "L1"
LAYER_L2 = "L2"
LAYER_L3 = "L3"
LAYER_L1_RETRY = "L1_RETRY"
LAYER_FALLBACK = "FALLBACK"
HARD_LAYERS = (LAYER_L1, LAYER_L1_RETRY, LAYER_L2, LAYER_L3, LAYER_FALLBACK)
SOFT_LAYERS = (LAYER_L2, LAYER_FALLBACK)   # fallback substitutes for L2 allocation reasoning

_SOFT_TEXT = {"PREFER_KEEP": "prefers to keep", "PREFER_EXIT": "prefers to exit"}


# ── The run object handed to the optimizer ────────────────────────────────────

class AdvisoryIntentRun:
    """Frozen per-run context plus the ledger. The only Intent object L1/L2/L3 see."""

    def __init__(self, *, workspace_id: int, portfolio_id: int, positions: list[HeldPosition],
                 anomalies: list[dict], basis: ValuationBasis, cash_balance,
                 context_error: str | None = None):
        self.review_id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.workspace_id = workspace_id
        self.portfolio_id = portfolio_id
        self.positions = tuple(sorted(positions, key=lambda p: p.symbol))
        self.by_symbol = {p.symbol: p for p in self.positions}
        self.anomalies = list(anomalies)
        self.basis = basis
        self.cash_balance = cash_balance
        self.context_error = context_error
        # The optimizer substitutes common-NAV current weights into pc_map (and so
        # into every allocation row's current_weight) exactly when the basis resolves.
        self.ledger = ProposalLedger(set(self.by_symbol),
                                     BASIS_COMMON_NAV if basis.resolved and basis.values
                                     else BASIS_LEGACY_EQUITY_ONLY)
        self.prompt_path: list[dict] = []
        self.run_disposition: dict = {}
        self._blocks = {layer: self._render_block(layer) for layer in HARD_LAYERS}

    # Optimizer-facing API ----------------------------------------------------
    def prompt_block(self, layer: str) -> str:
        return self._blocks.get(layer, "")

    def note_prompt(self, layer: str, attempt: str, outcome: str) -> None:
        block = self._blocks.get(layer, "")
        self.prompt_path.append({
            "layer": layer, "attempt": attempt, "outcome": outcome,
            "context": ("HARD_AND_SOFT" if layer in SOFT_LAYERS else "HARD") if block else "NONE",
            "context_digest": hashlib.sha256(block.encode("utf-8")).hexdigest() if block else None,
        })

    def canonical_current_weights(self) -> dict[str, float] | None:
        """Common-NAV current weights (2dp, display/AI basis) or None when unresolved."""
        if not self.basis.resolved:
            return None
        return {
            symbol: float((_HUNDRED * value / self.basis.nav).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            for symbol, value in self.basis.values.items()
        }

    def observe(self, symbol: str, **kwargs) -> None:
        """Record one proposal transition; a capture failure never breaks the run."""
        try:
            self.ledger.observe(symbol, **kwargs)
        except Exception as exc:  # fail closed in the review, not in the advice
            _log.exception("advisory intent provenance capture failed for %s", symbol)
            self.ledger.capture_errors.append(f"{symbol}:{type(exc).__name__}")

    def begin_attempt(self, attempt: str) -> None:
        self.ledger.begin_attempt(attempt)

    def abandon_attempt(self, attempt: str) -> None:
        self.ledger.abandon_attempt(attempt)
        for entry in self.prompt_path:
            if entry["attempt"] == attempt and entry["outcome"] == "SUCCESS":
                entry["outcome"] = "ABANDONED"

    # Context rendering -------------------------------------------------------
    def frozen_context_view(self) -> list[dict]:
        return [{
            "symbol": p.symbol, "referenced_shares": dec_str(p.shares),
            "holding_started_at": p.holding_started_at, "legacy_allow_swap": p.legacy_allow_swap,
            "applicability": p.applicability,
            "intent_id": p.intent.intent_id if p.intent else None,
            "intent_revision": p.intent.revision if p.intent else None,
            "confirmed_at": p.confirmed_at if p.intent else None,
            "increase_prohibited": p.intent.increase_prohibited if p.intent else None,
            "decrease_prohibited": p.intent.decrease_prohibited if p.intent else None,
            "soft_preference": p.intent.soft_preference if p.intent else None,
            "historical_intent": p.historical_intent,
        } for p in self.positions]

    def _render_block(self, layer: str) -> str:
        if self.context_error or not self.positions:
            return ""
        hard, unrestricted, unconfirmed, soft = [], [], [], []
        for p in self.positions:
            if p.intent is None:
                label = "re-confirmation required" if p.applicability != STATUS_NO_CONFIRMED_INTENT else "no confirmed intent"
                unconfirmed.append(f"{p.symbol} ({label})")
                continue
            rules = [text for flag, text in ((p.intent.increase_prohibited, "do not increase"),
                                             (p.intent.decrease_prohibited, "do not decrease")) if flag]
            (hard if rules else unrestricted).append(f"- {p.symbol}: {', '.join(rules)}" if rules else p.symbol)
            if p.intent.soft_preference in _SOFT_TEXT:
                soft.append(f"- {p.symbol}: owner {_SOFT_TEXT[p.intent.soft_preference]}")
        lines = [
            "[OWNER INVESTOR INTENT — ADVISORY CONTEXT FOR CURRENTLY HELD POSITIONS]",
            "These are the owner's confirmed wishes about share quantity, not system rules. They do "
            "not override policy, risk limits or forced exits, and those do not override them. If your "
            "analysis concludes a position should move in a direction the owner restricted, keep that "
            "conclusion, say so explicitly and name the restriction. Do not silently drop or rewrite a "
            "proposal to appear compliant, and do not treat either side as automatically winning.",
        ]
        if hard:
            lines.append("Owner hard restrictions:")
            lines.extend(hard)
        if unrestricted:
            lines.append("Owner confirmed no hard restriction: " + ", ".join(unrestricted))
        if unconfirmed:
            lines.append("No applicable owner intent (assume neither permission nor restriction): "
                         + ", ".join(unconfirmed))
        if layer in SOFT_LAYERS and soft:
            lines.append("Owner soft preferences (a leaning to weigh in your reasoning; not a restriction, "
                         "not a score, never a rule):")
            lines.extend(soft)
        return "\n".join(lines) + "\n\n"


def build_advisory_run(db, workspace_id: int, portfolio, holdings: list, *,
                       quote_evidence: dict[str, dict], execution_facts: dict) -> AdvisoryIntentRun:
    """Bulk-load the frozen run context once, before any AI reasoning."""
    from services.investor_intent_store import held_intent_applicability

    anomalies: list[dict] = []
    counts: dict[str, int] = {}
    for item in holdings:
        counts[item.symbol] = counts.get(item.symbol, 0) + 1
    for symbol, count in sorted(counts.items()):
        if count > 1:
            anomalies.append({"code": "DUPLICATE_HOLDING", "symbol": symbol, "rows": count})

    positive = []
    for item in holdings:
        shares = to_decimal(item.shares)
        if shares is None:
            anomalies.append({"code": "INVALID_SHARE_QUANTITY", "symbol": item.symbol})
        elif shares < 0:
            anomalies.append({"code": "NEGATIVE_SHARE_HOLDING", "symbol": item.symbol, "shares": dec_str(shares)})
        elif shares == 0:
            anomalies.append({"code": "ZERO_SHARE_HOLDING", "symbol": item.symbol})
        else:
            positive.append((item, shares))

    applicability = held_intent_applicability(db, workspace_id, portfolio.id, [i for i, _ in positive])
    positions: dict[str, HeldPosition] = {}
    for item, shares in positive:
        if item.symbol in positions:
            continue  # duplicate: already an anomaly that leaves the basis UNRESOLVED
        entry = applicability[item.symbol]
        positions[item.symbol] = HeldPosition(
            symbol=item.symbol, shares=shares,
            holding_started_at=item.created_at.isoformat() if item.created_at else None,
            legacy_allow_swap=bool(item.allow_swap), applicability=entry["status"],
            intent=entry["intent"],
            confirmed_at=entry["confirmed_at"].isoformat() if entry["confirmed_at"] else None,
            historical_intent=entry["historical_intent"],
        )
    currency_by_symbol = {
        symbol: getattr(execution_facts.get(symbol), "currency", None) for symbol in positions
    }
    basis = build_valuation_basis(list(positions.values()), anomalies, quote_evidence,
                                  currency_by_symbol, portfolio.cash_balance or 0.0)
    return AdvisoryIntentRun(workspace_id=workspace_id, portfolio_id=portfolio.id,
                             positions=list(positions.values()), anomalies=anomalies, basis=basis,
                             cash_balance=portfolio.cash_balance or 0.0)


CONTEXT_UNAVAILABLE = "CONTEXT_UNAVAILABLE"


def unavailable_advisory_run(workspace_id: int, portfolio, holdings: list, error: str) -> AdvisoryIntentRun:
    """Context could not be loaded: no prompt context, every held position UNRESOLVED."""
    positions: dict[str, HeldPosition] = {}
    for item in holdings:
        shares = to_decimal(item.shares)
        if shares is not None and shares > 0 and item.symbol not in positions:
            positions[item.symbol] = HeldPosition(
                symbol=item.symbol, shares=shares, holding_started_at=None,
                legacy_allow_swap=bool(item.allow_swap), applicability=CONTEXT_UNAVAILABLE,
                intent=None, confirmed_at=None, historical_intent=None,
            )
    basis = ValuationBasis(UNRESOLVED_BASIS, (CONTEXT_UNAVAILABLE,), None,
                           to_decimal(portfolio.cash_balance or 0.0) or Decimal(0), None, None, {}, {})
    return AdvisoryIntentRun(workspace_id=workspace_id, portfolio_id=portfolio.id,
                             positions=list(positions.values()), anomalies=[], basis=basis,
                             cash_balance=portfolio.cash_balance or 0.0, context_error=error)


def is_confirmed(position: HeldPosition) -> bool:
    return position.applicability == STATUS_CONFIRMED and position.intent is not None
