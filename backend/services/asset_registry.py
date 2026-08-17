"""Asset Registry — business rules (Milestone M1).

AssetRegistryService is the sole place lifecycle legality, identity
uniqueness, and classification/identifier stewardship rules are enforced.
services/asset_repository.py performs no validation of its own — this
module is the one authoritative implementation of those rules (ADR-004).

Nothing in the existing platform calls this service yet (M1 Definition of
Done). It exists as a self-contained foundation for later milestones.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, FrozenSet, Optional, Sequence

from sqlalchemy.orm import Session

from models.asset import Asset, AssetClassification, AssetIdentifier, AssetRelationship
from services import asset_repository as repo
from services.asset_definitions import DefinitionRegistry, DefinitionRegistryError
from services.asset_definitions.enforcement_gate import (
    EnforcementMode,
    evaluate_mint_enforcement,
)
from services.asset_domain import (
    AssetClaim,
    AssetId,
    AssetStatus,
    AssetType,
    ClassificationDimension,
    IdentifierRecord,
    IdentifierType,
    RelationshipType,
)
from services.runtime_consultation import (
    RuntimeConsultationLog,
    RuntimeFindingCategory,
    RuntimeValidationFinding,
)

_log = logging.getLogger(__name__)

# Legal forward-only transitions out of each status (ASSET_REGISTRY.md
# Section 6). ARCHIVED is terminal. Minting always produces ACTIVE, never
# any of these states directly, so there is no entry for "pre-mint".
_ALLOWED_TRANSITIONS: Dict[AssetStatus, FrozenSet[AssetStatus]] = {
    AssetStatus.ACTIVE: frozenset({AssetStatus.SUSPENDED, AssetStatus.DELISTED, AssetStatus.MERGED}),
    AssetStatus.SUSPENDED: frozenset({AssetStatus.ACTIVE, AssetStatus.DELISTED}),
    AssetStatus.DELISTED: frozenset({AssetStatus.ARCHIVED}),
    AssetStatus.MERGED: frozenset({AssetStatus.ARCHIVED}),
    AssetStatus.ARCHIVED: frozenset(),
}


class AssetRegistryError(ValueError):
    """Raised when a Registry operation would violate an identity or
    lifecycle invariant. Never raised for ordinary not-found lookups —
    callers should check for None themselves in that case."""


# ── Stage R1 runtime consultation (M12 brief, first Asset Registry consumer) ──
#
# mint() has no AssetType allow-list today — every one of AssetType's nine
# members is structurally accepted (ASSET_REGISTRY.md defines lifecycle and
# identity rules, not which asset types may exist). That absence of a gate
# *is* the legacy decision being shadowed here: "legacy permits minting this
# asset_type" is always True, and the runtime counterpart is
# DefinitionRegistry.exists(asset_type.value) — does the Asset Definition
# Library actually have a canonical definition for it? For CASH/EQUITY the
# two agree. For the other seven members (ETF, FUND, BOND, CRYPTO,
# COMMODITY, PROPERTY, OTHER) they disagree by construction — this is the
# exact gap M9 TDD Section 10.2 already documented ("mint gate needed").
# Recording it as a finding makes that documented gap observable per-mint,
# without acting on it: mint() still succeeds regardless (R1 = observe only,
# gating is R2's job).
def _consult_runtime_for_mint(asset_type: AssetType) -> RuntimeConsultationLog:
    """Never raises — a runtime boot failure becomes one MissingBinding
    finding, consistent with the pattern established for the ledger
    validator (M11)."""
    try:
        registry = DefinitionRegistry.build()
    except DefinitionRegistryError as exc:
        finding = RuntimeValidationFinding(
            category        = RuntimeFindingCategory.MISSING_BINDING.value,
            check_id        = "RUNTIME_REGISTRY_BOOT_FAILED",
            transaction_ids = (),
            binding         = asset_type.value,
            question        = "DefinitionRegistry.build()",
            legacy_result   = True,
            runtime_result  = None,
            detail          = str(exc),
        )
        return RuntimeConsultationLog(consulted=0, agreements=0, findings=(finding,))

    legacy_result = True  # mint() has no AssetType allow-list; every member is structurally accepted
    runtime_result = registry.exists(asset_type.value)

    if runtime_result == legacy_result:
        return RuntimeConsultationLog(consulted=1, agreements=1, findings=())

    finding = RuntimeValidationFinding(
        category        = RuntimeFindingCategory.UNKNOWN_CAPABILITY.value,
        check_id        = "RUNTIME_MINT_ASSET_TYPE_DEFINITION",
        transaction_ids = (),
        binding         = asset_type.value,
        question        = f"DefinitionRegistry.exists({asset_type.value!r})",
        legacy_result   = legacy_result,
        runtime_result  = runtime_result,
        detail          = (
            f"mint() accepted asset_type={asset_type.value!r} (no legacy allow-list exists), but the "
            "Asset Definition Runtime has no canonical definition registered for it yet (M9 TDD Section 10.2)."
        ),
    )
    return RuntimeConsultationLog(consulted=1, agreements=0, findings=(finding,))


def mint(
    db: Session,
    claim: AssetClaim,
    *,
    identifiers: Optional[Sequence[IdentifierRecord]] = None,
    enforcement_mode: Optional[EnforcementMode] = None,
) -> Asset:
    """The one irreversible moment: creates a permanent asset_id and
    canonical_symbol from a pre-mint claim. Minting always produces status
    ACTIVE — ClaimStatus (Discovery/Candidate) is pre-mint vocabulary only
    and is not itself persisted.

    Stage R1 (M12): consults the Asset Definition Runtime as a read-only
    shadow (see _consult_runtime_for_mint()) — observational only, never
    raised, never gates minting. The runtime is not yet a source of truth.

    Stage R2 (M14): additionally evaluates the M13 enforcement decision
    table (see services/asset_definitions/enforcement_gate.py). `blocked`
    can only ever be True when `enforcement_mode` resolves to ENFORCE *and*
    that asset_type's recorded decision is future_action=REJECT — as of
    this milestone no decision is REJECT, so ENFORCE is a documented no-op
    against real data. `enforcement_mode` defaults to None, which resolves
    to the ASSET_MINT_ENFORCEMENT_MODE environment variable, which itself
    defaults to OFF — an existing caller that never passes this argument
    gets byte-identical behavior to before this milestone.
    """
    if not claim.canonical_symbol or not claim.canonical_symbol.strip():
        raise AssetRegistryError("canonical_symbol must be non-empty")
    if not claim.market or not claim.exchange or not claim.currency:
        raise AssetRegistryError("market, exchange, and currency are required to mint an asset")

    try:
        runtime_log = _consult_runtime_for_mint(claim.asset_type)
    except Exception as exc:
        _log.warning("runtime consultation failed for mint asset_type=%s: %s", claim.asset_type.value, exc)
    else:
        for finding in runtime_log.findings:
            _log.warning(
                "runtime consultation finding on mint: check_id=%s category=%s binding=%s detail=%s",
                finding.check_id, finding.category, finding.binding, finding.detail,
            )

    enforcement = evaluate_mint_enforcement(claim.asset_type, mode=enforcement_mode)
    _log.info(
        "asset_definition_enforcement: asset_type=%s mode=%s gap_type=%s intended_action=%s "
        "effective_action=%s reason=%s",
        enforcement.asset_type, enforcement.mode.value, enforcement.gap_type,
        enforcement.intended_action.value, enforcement.effective_action.value, enforcement.reason,
    )
    if enforcement.blocked:
        raise AssetRegistryError(
            f"minting asset_type={claim.asset_type.value!r} is blocked by Asset Definition Runtime "
            f"Stage R2 enforcement (mode={enforcement.mode.value}): {enforcement.reason}"
        )

    existing = repo.get_asset_by_canonical_symbol(db, claim.canonical_symbol)
    if existing is not None:
        raise AssetRegistryError(
            f"canonical_symbol '{claim.canonical_symbol}' is already minted as asset_id={existing.id}; "
            "canonical_symbol is permanent and may never be reassigned"
        )

    row = repo.create_asset(
        db,
        canonical_symbol=claim.canonical_symbol,
        asset_type=claim.asset_type.value,
        market=claim.market,
        exchange=claim.exchange,
        currency=claim.currency,
        status=AssetStatus.ACTIVE.value,
        display_symbol=claim.display_symbol or claim.canonical_symbol,
        tradable=claim.tradable,
        fractional_support=claim.fractional_support,
        lot_size=claim.lot_size,
        settlement_cycle=claim.settlement_cycle,
    )

    for identifier in identifiers or ():
        attach_identifier(db, AssetId(row.id), identifier)

    return row


def get_asset(db: Session, asset_id: AssetId) -> Optional[Asset]:
    return repo.get_asset(db, asset_id)


def get_asset_by_canonical_symbol(db: Session, canonical_symbol: str) -> Optional[Asset]:
    return repo.get_asset_by_canonical_symbol(db, canonical_symbol)


def attach_identifier(db: Session, asset_id: AssetId, identifier: IdentifierRecord) -> AssetIdentifier:
    """Records an evidence-tier identifier. A real-world ticker/identifier
    change is expressed here — the prior current mapping for the same
    (asset_id, identifier_type) is superseded (is_current=False, retained
    forever), never edited or deleted, and the new mapping becomes current.

    Rejects attaching an identifier value that is already the CURRENT
    mapping for a different asset (conflicting identifiers, ASSET_REGISTRY.md
    Section 7) — the same real-world identifier cannot simultaneously
    point at two live assets.
    """
    asset = repo.get_asset(db, asset_id)
    if asset is None:
        raise AssetRegistryError(f"no asset with asset_id={asset_id}")

    conflict = repo.find_current_identifier(db, identifier.identifier_type.value, identifier.value)
    if conflict is not None and conflict.asset_id != asset_id:
        raise AssetRegistryError(
            f"identifier {identifier.identifier_type.value}:{identifier.value} is already the current "
            f"mapping for asset_id={conflict.asset_id}; cannot also attach it to asset_id={asset_id}"
        )
    if conflict is not None and conflict.asset_id == asset_id:
        return conflict  # already attached and current; idempotent

    current_same_type = [
        row for row in repo.get_identifiers(db, asset_id, current_only=True)
        if row.identifier_type == identifier.identifier_type.value
    ]
    for row in current_same_type:
        repo.mark_identifier_not_current(db, row)

    new_row = repo.add_identifier(
        db,
        asset_id=asset_id,
        identifier_type=identifier.identifier_type.value,
        value=identifier.value,
        source=identifier.source,
        as_of=identifier.as_of,
    )

    if identifier.identifier_type.value == "PROVIDER_SYMBOL":
        repo.update_display_symbol(db, asset, identifier.value)

    return new_row


def get_identifiers(db: Session, asset_id: AssetId, *, current_only: bool = False) -> Sequence[AssetIdentifier]:
    return repo.get_identifiers(db, asset_id, current_only=current_only)


def transition_status(db: Session, asset_id: AssetId, new_status: AssetStatus) -> Asset:
    """Enforces the forward-only lifecycle graph. asset_id is never reused
    and never un-minted regardless of the resulting status."""
    asset = repo.get_asset(db, asset_id)
    if asset is None:
        raise AssetRegistryError(f"no asset with asset_id={asset_id}")

    current_status = AssetStatus(asset.status)
    allowed = _ALLOWED_TRANSITIONS.get(current_status, frozenset())
    if new_status not in allowed:
        raise AssetRegistryError(
            f"illegal status transition for asset_id={asset_id}: "
            f"{current_status.value} -> {new_status.value}"
        )

    return repo.update_status(db, asset, new_status.value)


def link_relationship(
    db: Session,
    from_asset_id: AssetId,
    to_asset_id: AssetId,
    relationship_type: RelationshipType,
    *,
    effective_date: Optional[datetime] = None,
) -> AssetRelationship:
    """Links two listings without merging their records (ASSET_REGISTRY.md
    Section 5 — the unit of identity is the listing, not the entity)."""
    if from_asset_id == to_asset_id:
        raise AssetRegistryError("an asset cannot have a relationship to itself")
    if repo.get_asset(db, from_asset_id) is None:
        raise AssetRegistryError(f"no asset with asset_id={from_asset_id}")
    if repo.get_asset(db, to_asset_id) is None:
        raise AssetRegistryError(f"no asset with asset_id={to_asset_id}")

    for row in repo.get_relationships(db, from_asset_id):
        if (
            row.from_asset_id == from_asset_id
            and row.to_asset_id == to_asset_id
            and row.relationship_type == relationship_type.value
        ):
            return row  # idempotent

    return repo.add_relationship(
        db,
        from_asset_id=from_asset_id,
        to_asset_id=to_asset_id,
        relationship_type=relationship_type.value,
        effective_date=effective_date,
    )


def get_relationships(db: Session, asset_id: AssetId) -> Sequence[AssetRelationship]:
    return repo.get_relationships(db, asset_id)


# ── BANPU-WP4 — position-conversion registry preparation and validation ────
#
# WP4 Work Package Plan PD-WP4-1: registry preparation is a distinct,
# idempotent service act performed BEFORE execute_position_conversion()
# opens its transaction — never performed implicitly by that service.
# PD-WP4-2: mark_identifier_not_current() already exists in asset_repository
# (M1); the missing capability was only the service-level retirement
# operation below, which composes it. transition_status() and
# link_relationship() (both M1, above) are reused unchanged.

def retire_identifier(
    db: Session, asset_id: AssetId, identifier_type: IdentifierType,
) -> Sequence[AssetIdentifier]:
    """Retires (is_current=False) every currently-current identifier of
    `identifier_type` for asset_id, recording no replacement.

    Distinct from attach_identifier()'s supersession, which retires the
    prior mapping only as a side effect of adding a new one. A predecessor
    identity that is merging away — not being renamed — needs retirement
    without succession as its own act. Idempotent: already-retired
    identifiers are untouched, and calling this again once nothing of that
    type is current is a no-op that retires nothing.
    """
    asset = repo.get_asset(db, asset_id)
    if asset is None:
        raise AssetRegistryError(f"no asset with asset_id={asset_id}")

    current = [
        row for row in repo.get_identifiers(db, asset_id, current_only=True)
        if row.identifier_type == identifier_type.value
    ]
    for row in current:
        repo.mark_identifier_not_current(db, row)
    return current


def prepare_position_conversion_registry(
    db: Session,
    predecessor_asset_id: AssetId,
    successor_asset_id: AssetId,
    successor_provider_symbol: str,
    *,
    source: str,
    effective_date: Optional[datetime] = None,
) -> AssetRelationship:
    """BANPU-WP4 registry preparation (Work Package Plan §3.2 step E0).

    Establishes the current successor PROVIDER_SYMBOL identifier, retires
    the predecessor's current PROVIDER_SYMBOL identifier, transitions the
    predecessor to MERGED, and links predecessor -> successor with the
    existing MERGED_INTO relationship type. Idempotent and repeatable:
    re-running against an already-prepared pair performs no redundant
    mutation and reaches the same end state. Fail-closed — an illegal
    predecessor lifecycle transition (e.g. from DELISTED or ARCHIVED)
    raises AssetRegistryError exactly as transition_status() already does.

    This is a separate service act, never invoked by
    execute_position_conversion() itself (PD-WP4-1) — that service only
    validates the state this function establishes.
    """
    if predecessor_asset_id == successor_asset_id:
        raise AssetRegistryError("predecessor and successor asset_id must be distinct")

    predecessor = repo.get_asset(db, predecessor_asset_id)
    if predecessor is None:
        raise AssetRegistryError(f"no asset with asset_id={predecessor_asset_id}")
    if repo.get_asset(db, successor_asset_id) is None:
        raise AssetRegistryError(f"no asset with asset_id={successor_asset_id}")

    # WP4-IIR-B3: fail closed on a conflicting pre-existing outgoing
    # MERGED_INTO edge BEFORE any mutation below. link_relationship()'s own
    # idempotency check only matches the exact (from, to, type) triple, so
    # without this guard a predecessor already merged into some other asset
    # would silently gain a second MERGED_INTO edge instead of rejecting the
    # conflicting request. An edge to this exact successor is left to
    # link_relationship()'s existing idempotent handling below.
    conflicting_merged_into = [
        row for row in repo.get_relationships(db, predecessor_asset_id)
        if row.from_asset_id == predecessor_asset_id
        and row.relationship_type == RelationshipType.MERGED_INTO.value
        and row.to_asset_id != successor_asset_id
    ]
    if conflicting_merged_into:
        raise AssetRegistryError(
            f"predecessor asset_id={predecessor_asset_id} already carries a MERGED_INTO "
            f"relationship to asset_id={conflicting_merged_into[0].to_asset_id}; cannot also "
            f"link it to asset_id={successor_asset_id}"
        )

    attach_identifier(
        db, successor_asset_id,
        IdentifierRecord(
            IdentifierType.PROVIDER_SYMBOL, successor_provider_symbol,
            source=source, as_of=effective_date,
        ),
    )

    retire_identifier(db, predecessor_asset_id, IdentifierType.PROVIDER_SYMBOL)

    if AssetStatus(predecessor.status) != AssetStatus.MERGED:
        transition_status(db, predecessor_asset_id, AssetStatus.MERGED)

    return link_relationship(
        db, predecessor_asset_id, successor_asset_id, RelationshipType.MERGED_INTO,
        effective_date=effective_date,
    )


def resolve_predecessor_provider_symbol(db: Session, predecessor_asset_id: AssetId) -> str:
    """Derives the predecessor's provider symbol from registry/identifier
    state — never from caller-supplied payload text (WP4-IIR-B2 second-
    renewed correction).

    E0 retirement (retire_identifier(), called by
    prepare_position_conversion_registry()) flips the predecessor's current
    PROVIDER_SYMBOL identifier's is_current to False; it does not delete the
    row. Historical mappings are retained forever (ASSET_REGISTRY.md
    Section 3), so the identifier value that was current immediately before
    retirement remains readable — it is the most recently attached
    PROVIDER_SYMBOL row for this asset_id, since get_identifiers() orders by
    created_at ascending and attach_identifier() only ever adds one new
    current row per real-world change (never edits or reorders existing
    rows).

    Fail-closed: raises AssetRegistryError if the predecessor carries no
    PROVIDER_SYMBOL identifier at all — registry preparation (E0) is
    incomplete or never ran, so no registry-authoritative value exists to
    derive. This function never falls back to an arbitrary or hard-coded
    value in that case.
    """
    provider_symbol_identifiers = [
        row for row in repo.get_identifiers(db, predecessor_asset_id, current_only=False)
        if row.identifier_type == IdentifierType.PROVIDER_SYMBOL.value
    ]
    if not provider_symbol_identifiers:
        raise AssetRegistryError(
            f"predecessor asset_id={predecessor_asset_id} has no PROVIDER_SYMBOL "
            "identifier of any currency to resolve a predecessor provider symbol "
            "from; registry preparation is incomplete"
        )
    return provider_symbol_identifiers[-1].value


def validate_position_conversion_registry_state(
    db: Session,
    predecessor_asset_id: AssetId,
    successor_asset_id: AssetId,
    successor_provider_symbol: str,
    predecessor_provider_symbol: str,
) -> None:
    """Fail-closed validation of the WP4 conversion registry invariants.

    Performed by execute_position_conversion() (step E3) before any write —
    this function never prepares registry state itself (PD-WP4-1); it only
    verifies that prepare_position_conversion_registry() already ran and
    reached a consistent end state. Raises AssetRegistryError with a
    descriptive reason on the first failing invariant; read-only otherwise.

    Verifies exactly:
      - both assets exist and are distinct;
      - the successor has a current PROVIDER_SYMBOL identifier equal to
        successor_provider_symbol;
      - the predecessor status is MERGED;
      - the predecessor no longer carries a current PROVIDER_SYMBOL
        identifier (retired);
      - predecessor_provider_symbol equals resolve_predecessor_provider_symbol()
        for the predecessor — never trusted as arbitrary caller-supplied text
        (WP4-IIR-B2 second-renewed correction);
      - exactly one MERGED_INTO relationship links predecessor to
        successor (not absent, not reversed, not pointing elsewhere).
    """
    if predecessor_asset_id == successor_asset_id:
        raise AssetRegistryError("predecessor and successor asset_id must be distinct")

    predecessor = repo.get_asset(db, predecessor_asset_id)
    if predecessor is None:
        raise AssetRegistryError(f"no asset with asset_id={predecessor_asset_id}")
    if repo.get_asset(db, successor_asset_id) is None:
        raise AssetRegistryError(f"no asset with asset_id={successor_asset_id}")

    successor_identifier = repo.find_current_identifier(
        db, IdentifierType.PROVIDER_SYMBOL.value, successor_provider_symbol,
    )
    if successor_identifier is None or successor_identifier.asset_id != successor_asset_id:
        raise AssetRegistryError(
            f"successor asset_id={successor_asset_id} has no current PROVIDER_SYMBOL "
            f"identifier {successor_provider_symbol!r}"
        )

    if AssetStatus(predecessor.status) != AssetStatus.MERGED:
        raise AssetRegistryError(
            f"predecessor asset_id={predecessor_asset_id} status is "
            f"{predecessor.status!r}, expected {AssetStatus.MERGED.value!r}"
        )

    predecessor_current = [
        row for row in repo.get_identifiers(db, predecessor_asset_id, current_only=True)
        if row.identifier_type == IdentifierType.PROVIDER_SYMBOL.value
    ]
    if predecessor_current:
        raise AssetRegistryError(
            f"predecessor asset_id={predecessor_asset_id} still has a current "
            "PROVIDER_SYMBOL identifier; expected retired"
        )

    resolved_predecessor_provider_symbol = resolve_predecessor_provider_symbol(db, predecessor_asset_id)
    if predecessor_provider_symbol != resolved_predecessor_provider_symbol:
        raise AssetRegistryError(
            f"predecessor asset_id={predecessor_asset_id} provider symbol "
            f"{predecessor_provider_symbol!r} does not match the registry-derived "
            f"value {resolved_predecessor_provider_symbol!r}"
        )

    merged_into = [
        row for row in repo.get_relationships(db, predecessor_asset_id)
        if row.from_asset_id == predecessor_asset_id
        and row.relationship_type == RelationshipType.MERGED_INTO.value
    ]
    if len(merged_into) != 1 or merged_into[0].to_asset_id != successor_asset_id:
        raise AssetRegistryError(
            f"predecessor asset_id={predecessor_asset_id} does not carry exactly one "
            f"MERGED_INTO relationship to successor asset_id={successor_asset_id}"
        )


def record_classification(
    db: Session,
    asset_id: AssetId,
    dimension: ClassificationDimension,
    value: str,
    source: str,
    *,
    as_of: Optional[datetime] = None,
) -> AssetClassification:
    """Records a dated, provenance-tagged classification fact
    (ASSET_REGISTRY.md Section 8). `value` is registry-managed vocabulary
    (a plain string), not an enum member — see services/asset_domain.py.
    Superseded facts are retained (is_current=False), never deleted.
    """
    if repo.get_asset(db, asset_id) is None:
        raise AssetRegistryError(f"no asset with asset_id={asset_id}")
    if not value or not value.strip():
        raise AssetRegistryError("classification value must be non-empty")

    current = [
        row for row in repo.get_classifications(db, asset_id, dimension=dimension.value, current_only=True)
    ]
    if current and current[0].value == value and current[0].source == source:
        return current[0]  # identical fact already current; idempotent

    for row in current:
        repo.mark_classification_not_current(db, row)

    return repo.add_classification(
        db,
        asset_id=asset_id,
        dimension=dimension.value,
        value=value,
        source=source,
        as_of=as_of,
    )


def get_classifications(
    db: Session, asset_id: AssetId, *, dimension: Optional[ClassificationDimension] = None, current_only: bool = False,
) -> Sequence[AssetClassification]:
    return repo.get_classifications(
        db, asset_id, dimension=dimension.value if dimension else None, current_only=current_only,
    )
