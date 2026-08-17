"""Tests for the Asset Registry canonical identity core (Milestone M1).

Validates the design principles in docs/architecture/ASSET_REGISTRY.md
Section 12 that are expressible as unit tests:
  1. Minting uniqueness — canonical_symbol can only ever be minted once
  2. canonical_symbol permanence — never reassigned, even across a
     real-world ticker change (display_symbol/AssetIdentifier evolve instead)
  3. asset_id is never reused or un-minted
  4. Historical identifier mappings are retained, not deleted, on supersession
  5. Conflicting identifiers (same value, two live assets) are rejected
  6. Lifecycle transitions are forward-only and illegal transitions are rejected
  7. Classification facts are dated/superseded, never deleted
  8. Relationships link listings without merging their identity
  9. Absence is data — an asset with no identifiers/classification is valid

All tests use an in-memory SQLite database; no network calls.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import Base
import models.asset  # noqa: F401 — registers Asset* tables on Base.metadata
from services import asset_registry as registry
from services.asset_domain import (
    AssetClaim,
    AssetStatus,
    AssetType,
    ClassificationDimension,
    IdentifierRecord,
    IdentifierType,
    RelationshipType,
)
from services.asset_registry import AssetRegistryError


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


def _claim(**overrides):
    defaults = dict(
        canonical_symbol="KBANK",
        asset_type=AssetType.EQUITY,
        market="TH",
        exchange="SET",
        currency="THB",
    )
    defaults.update(overrides)
    return AssetClaim(**defaults)


# ── Minting ──────────────────────────────────────────────────────────────────

def test_mint_creates_active_asset_with_permanent_id():
    db = make_session()
    asset = registry.mint(db, _claim())

    assert asset.id is not None
    assert asset.canonical_symbol == "KBANK"
    assert asset.status == AssetStatus.ACTIVE.value
    assert asset.display_symbol == "KBANK"  # defaults to canonical_symbol


def test_mint_rejects_duplicate_canonical_symbol():
    db = make_session()
    registry.mint(db, _claim())

    with pytest.raises(AssetRegistryError):
        registry.mint(db, _claim())


def test_mint_requires_market_exchange_currency():
    db = make_session()
    with pytest.raises(AssetRegistryError):
        registry.mint(db, _claim(currency=""))


def test_asset_id_never_reused_across_assets():
    db = make_session()
    a1 = registry.mint(db, _claim(canonical_symbol="KBANK"))
    a2 = registry.mint(db, _claim(canonical_symbol="PTT"))

    assert a1.id != a2.id


# ── canonical_symbol permanence vs. real-world ticker change ────────────────

def test_canonical_symbol_survives_identifier_supersession():
    """A real-world ticker/provider-symbol change must never touch
    canonical_symbol or asset_id — only the evidence tier (identifiers,
    display_symbol) moves."""
    db = make_session()
    asset = registry.mint(db, _claim())
    asset_id = asset.id

    registry.attach_identifier(
        db, asset_id,
        IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "KBANK.BK", source="yfinance"),
    )
    # Simulate a provider symbol rename (e.g. exchange re-listing)
    registry.attach_identifier(
        db, asset_id,
        IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "KBANK2.BK", source="yfinance"),
    )

    refreshed = registry.get_asset(db, asset_id)
    assert refreshed.id == asset_id
    assert refreshed.canonical_symbol == "KBANK"  # untouched
    assert refreshed.display_symbol == "KBANK2.BK"  # evidence-tier field moved


def test_superseded_identifier_retained_not_deleted():
    db = make_session()
    asset = registry.mint(db, _claim())
    asset_id = asset.id

    old = registry.attach_identifier(
        db, asset_id,
        IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "KBANK.BK", source="yfinance"),
    )
    registry.attach_identifier(
        db, asset_id,
        IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "KBANK2.BK", source="yfinance"),
    )

    all_identifiers = registry.get_identifiers(db, asset_id)
    values = {row.value for row in all_identifiers}
    assert values == {"KBANK.BK", "KBANK2.BK"}  # both retained

    current = registry.get_identifiers(db, asset_id, current_only=True)
    assert len(current) == 1
    assert current[0].value == "KBANK2.BK"

    old_row = [row for row in all_identifiers if row.value == "KBANK.BK"][0]
    assert old_row.is_current is False
    assert old_row.id == old.id  # same row, not deleted+recreated


def test_conflicting_identifier_across_two_assets_rejected():
    db = make_session()
    a1 = registry.mint(db, _claim(canonical_symbol="KBANK"))
    a2 = registry.mint(db, _claim(canonical_symbol="PTT"))

    registry.attach_identifier(
        db, a1.id, IdentifierRecord(IdentifierType.ISIN, "TH0001010006", source="manual"),
    )

    with pytest.raises(AssetRegistryError):
        registry.attach_identifier(
            db, a2.id, IdentifierRecord(IdentifierType.ISIN, "TH0001010006", source="manual"),
        )


def test_attaching_same_identifier_twice_is_idempotent():
    db = make_session()
    asset = registry.mint(db, _claim())
    ident = IdentifierRecord(IdentifierType.ISIN, "TH0001010006", source="manual")

    first = registry.attach_identifier(db, asset.id, ident)
    second = registry.attach_identifier(db, asset.id, ident)

    assert first.id == second.id
    assert len(registry.get_identifiers(db, asset.id)) == 1


# ── Lifecycle transitions ────────────────────────────────────────────────────

def test_legal_lifecycle_transition_sequence():
    db = make_session()
    asset = registry.mint(db, _claim())

    registry.transition_status(db, asset.id, AssetStatus.SUSPENDED)
    assert registry.get_asset(db, asset.id).status == AssetStatus.SUSPENDED.value

    registry.transition_status(db, asset.id, AssetStatus.ACTIVE)
    assert registry.get_asset(db, asset.id).status == AssetStatus.ACTIVE.value

    registry.transition_status(db, asset.id, AssetStatus.DELISTED)
    registry.transition_status(db, asset.id, AssetStatus.ARCHIVED)
    assert registry.get_asset(db, asset.id).status == AssetStatus.ARCHIVED.value


def test_illegal_lifecycle_transition_rejected():
    db = make_session()
    asset = registry.mint(db, _claim())
    registry.transition_status(db, asset.id, AssetStatus.DELISTED)
    registry.transition_status(db, asset.id, AssetStatus.ARCHIVED)

    with pytest.raises(AssetRegistryError):
        registry.transition_status(db, asset.id, AssetStatus.ACTIVE)  # archived is terminal


def test_asset_id_and_canonical_symbol_survive_lifecycle_transitions():
    db = make_session()
    asset = registry.mint(db, _claim())
    asset_id, canonical_symbol = asset.id, asset.canonical_symbol

    registry.transition_status(db, asset.id, AssetStatus.SUSPENDED)
    registry.transition_status(db, asset.id, AssetStatus.DELISTED)
    registry.transition_status(db, asset.id, AssetStatus.ARCHIVED)

    final = registry.get_asset(db, asset_id)
    assert final.id == asset_id
    assert final.canonical_symbol == canonical_symbol  # never un-minted


# ── Classification stewardship ───────────────────────────────────────────────

def test_classification_is_dated_and_superseded_not_deleted():
    db = make_session()
    asset = registry.mint(db, _claim())

    registry.record_classification(
        db, asset.id, ClassificationDimension.SECTOR, "Financials", source="THAI_SECTOR_MAP",
    )
    registry.record_classification(
        db, asset.id, ClassificationDimension.SECTOR, "Banking", source="THAI_SECTOR_MAP",
    )

    all_rows = registry.get_classifications(db, asset.id, dimension=ClassificationDimension.SECTOR)
    assert {row.value for row in all_rows} == {"Financials", "Banking"}  # both retained

    current = registry.get_classifications(
        db, asset.id, dimension=ClassificationDimension.SECTOR, current_only=True,
    )
    assert len(current) == 1
    assert current[0].value == "Banking"


def test_classification_value_is_not_enum_constrained():
    """Classification values are registry-managed vocabulary, not a
    compile-time enum — an arbitrary taxonomy string must be accepted."""
    db = make_session()
    asset = registry.mint(db, _claim())

    row = registry.record_classification(
        db, asset.id, ClassificationDimension.SECTOR, "ธนาคาร", source="THAI_SECTOR_MAP",
    )
    assert row.value == "ธนาคาร"


def test_empty_classification_value_rejected():
    db = make_session()
    asset = registry.mint(db, _claim())

    with pytest.raises(AssetRegistryError):
        registry.record_classification(db, asset.id, ClassificationDimension.SECTOR, "  ", source="manual")


# ── Relationships (multiple listings) ────────────────────────────────────────

def test_relationship_links_listings_without_merging_identity():
    db = make_session()
    thai = registry.mint(db, _claim(canonical_symbol="KBANK", market="TH", exchange="SET", currency="THB"))
    dr = registry.mint(db, _claim(canonical_symbol="KBANK_DR", market="US", exchange="OTC", currency="USD"))

    rel = registry.link_relationship(db, dr.id, thai.id, RelationshipType.DEPOSITARY_RECEIPT_OF)

    assert rel.from_asset_id == dr.id
    assert rel.to_asset_id == thai.id
    # both listings keep their own independent identity
    assert registry.get_asset(db, dr.id).canonical_symbol == "KBANK_DR"
    assert registry.get_asset(db, thai.id).canonical_symbol == "KBANK"


def test_relationship_rejects_self_link():
    db = make_session()
    asset = registry.mint(db, _claim())

    with pytest.raises(AssetRegistryError):
        registry.link_relationship(db, asset.id, asset.id, RelationshipType.DUAL_LISTED)


def test_duplicate_relationship_is_idempotent():
    db = make_session()
    a1 = registry.mint(db, _claim(canonical_symbol="KBANK"))
    a2 = registry.mint(db, _claim(canonical_symbol="KBANK_DR"))

    first = registry.link_relationship(db, a2.id, a1.id, RelationshipType.DEPOSITARY_RECEIPT_OF)
    second = registry.link_relationship(db, a2.id, a1.id, RelationshipType.DEPOSITARY_RECEIPT_OF)

    assert first.id == second.id
    assert len(registry.get_relationships(db, a1.id)) == 1


# ── Absence is data ───────────────────────────────────────────────────────────

def test_asset_with_no_identifiers_or_classification_is_valid():
    db = make_session()
    asset = registry.mint(db, _claim(canonical_symbol="XYZ"))

    assert registry.get_identifiers(db, asset.id) == []
    assert registry.get_classifications(db, asset.id) == []
    assert registry.get_asset(db, asset.id) is not None


# ── BANPU-WP4 — position-conversion registry preparation and validation ────

def _mint_predecessor_successor():
    db = make_session()
    predecessor = registry.mint(
        db, _claim(canonical_symbol="BANPU"),
        identifiers=[IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "BANPU.BK", source="yfinance")],
    )
    successor = registry.mint(db, _claim(canonical_symbol="BANPUU"))
    return db, predecessor, successor


def test_retire_identifier_marks_current_identifier_not_current():
    db = make_session()
    asset = registry.mint(
        db, _claim(),
        identifiers=[IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "KBANK.BK", source="yfinance")],
    )

    retired = registry.retire_identifier(db, asset.id, IdentifierType.PROVIDER_SYMBOL)

    assert len(retired) == 1
    assert registry.get_identifiers(db, asset.id, current_only=True) == []
    all_rows = registry.get_identifiers(db, asset.id)
    assert all_rows[0].is_current is False
    assert all_rows[0].value == "KBANK.BK"


def test_retire_identifier_is_idempotent():
    db = make_session()
    asset = registry.mint(
        db, _claim(),
        identifiers=[IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "KBANK.BK", source="yfinance")],
    )

    registry.retire_identifier(db, asset.id, IdentifierType.PROVIDER_SYMBOL)
    second = registry.retire_identifier(db, asset.id, IdentifierType.PROVIDER_SYMBOL)

    assert second == []  # nothing left current to retire
    assert registry.get_identifiers(db, asset.id, current_only=True) == []


def test_retire_identifier_rejects_unknown_asset():
    db = make_session()
    with pytest.raises(AssetRegistryError):
        registry.retire_identifier(db, 9999, IdentifierType.PROVIDER_SYMBOL)


def test_prepare_position_conversion_registry_establishes_full_state():
    db, predecessor, successor = _mint_predecessor_successor()

    rel = registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    assert rel.from_asset_id == predecessor.id
    assert rel.to_asset_id == successor.id
    assert rel.relationship_type == RelationshipType.MERGED_INTO.value

    refreshed_predecessor = registry.get_asset(db, predecessor.id)
    assert refreshed_predecessor.status == AssetStatus.MERGED.value
    assert registry.get_identifiers(db, predecessor.id, current_only=True) == []

    successor_current = registry.get_identifiers(db, successor.id, current_only=True)
    assert len(successor_current) == 1
    assert successor_current[0].value == "BANPUU.BK"
    assert successor_current[0].identifier_type == IdentifierType.PROVIDER_SYMBOL.value


def test_prepare_position_conversion_registry_is_idempotent():
    db, predecessor, successor = _mint_predecessor_successor()

    first = registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )
    second = registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    assert first.id == second.id
    assert len(registry.get_relationships(db, predecessor.id)) == 1
    assert registry.get_asset(db, predecessor.id).status == AssetStatus.MERGED.value


def test_prepare_position_conversion_registry_rejects_same_asset():
    db = make_session()
    asset = registry.mint(db, _claim())

    with pytest.raises(AssetRegistryError):
        registry.prepare_position_conversion_registry(
            db, asset.id, asset.id, "X.BK", source="banpu-wp4",
        )


def test_validate_position_conversion_registry_state_passes_after_preparation():
    db, predecessor, successor = _mint_predecessor_successor()
    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    registry.validate_position_conversion_registry_state(
        db, predecessor.id, successor.id, "BANPUU.BK",
        "BANPU.BK",
    )  # must not raise


def test_validate_position_conversion_registry_state_rejects_unprepared_pair():
    db, predecessor, successor = _mint_predecessor_successor()

    with pytest.raises(AssetRegistryError):
        registry.validate_position_conversion_registry_state(
            db, predecessor.id, successor.id, "BANPUU.BK",
            "BANPU.BK",
        )


def test_validate_position_conversion_registry_state_rejects_successor_provider_symbol_mismatch():
    db, predecessor, successor = _mint_predecessor_successor()
    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    with pytest.raises(AssetRegistryError):
        registry.validate_position_conversion_registry_state(
            db, predecessor.id, successor.id, "WRONG.BK",
            "BANPU.BK",
        )


def test_validate_position_conversion_registry_state_rejects_predecessor_not_merged():
    db, predecessor, successor = _mint_predecessor_successor()
    registry.attach_identifier(
        db, successor.id,
        IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "BANPUU.BK", source="banpu-wp4"),
    )
    registry.retire_identifier(db, predecessor.id, IdentifierType.PROVIDER_SYMBOL)
    registry.link_relationship(db, predecessor.id, successor.id, RelationshipType.MERGED_INTO)
    # predecessor status left ACTIVE — never transitioned to MERGED

    with pytest.raises(AssetRegistryError):
        registry.validate_position_conversion_registry_state(
            db, predecessor.id, successor.id, "BANPUU.BK",
            "BANPU.BK",
        )


def test_validate_position_conversion_registry_state_rejects_predecessor_identifier_not_retired():
    db, predecessor, successor = _mint_predecessor_successor()
    registry.attach_identifier(
        db, successor.id,
        IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "BANPUU.BK", source="banpu-wp4"),
    )
    registry.transition_status(db, predecessor.id, AssetStatus.MERGED)
    registry.link_relationship(db, predecessor.id, successor.id, RelationshipType.MERGED_INTO)
    # predecessor's PROVIDER_SYMBOL identifier was never retired

    with pytest.raises(AssetRegistryError):
        registry.validate_position_conversion_registry_state(
            db, predecessor.id, successor.id, "BANPUU.BK",
            "BANPU.BK",
        )


def test_validate_position_conversion_registry_state_rejects_missing_merged_into():
    db, predecessor, successor = _mint_predecessor_successor()
    registry.attach_identifier(
        db, successor.id,
        IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "BANPUU.BK", source="banpu-wp4"),
    )
    registry.retire_identifier(db, predecessor.id, IdentifierType.PROVIDER_SYMBOL)
    registry.transition_status(db, predecessor.id, AssetStatus.MERGED)
    # no MERGED_INTO relationship created

    with pytest.raises(AssetRegistryError):
        registry.validate_position_conversion_registry_state(
            db, predecessor.id, successor.id, "BANPUU.BK",
            "BANPU.BK",
        )


def test_validate_position_conversion_registry_state_rejects_reversed_merged_into():
    db, predecessor, successor = _mint_predecessor_successor()
    registry.attach_identifier(
        db, successor.id,
        IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "BANPUU.BK", source="banpu-wp4"),
    )
    registry.retire_identifier(db, predecessor.id, IdentifierType.PROVIDER_SYMBOL)
    registry.transition_status(db, predecessor.id, AssetStatus.MERGED)
    # reversed edge: successor -> predecessor instead of predecessor -> successor
    registry.link_relationship(db, successor.id, predecessor.id, RelationshipType.MERGED_INTO)

    with pytest.raises(AssetRegistryError):
        registry.validate_position_conversion_registry_state(
            db, predecessor.id, successor.id, "BANPUU.BK",
            "BANPU.BK",
        )


def test_validate_position_conversion_registry_state_rejects_merged_into_pointing_elsewhere():
    db, predecessor, successor = _mint_predecessor_successor()
    other = registry.mint(db, _claim(canonical_symbol="OTHER"))
    registry.attach_identifier(
        db, successor.id,
        IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, "BANPUU.BK", source="banpu-wp4"),
    )
    registry.retire_identifier(db, predecessor.id, IdentifierType.PROVIDER_SYMBOL)
    registry.transition_status(db, predecessor.id, AssetStatus.MERGED)
    registry.link_relationship(db, predecessor.id, other.id, RelationshipType.MERGED_INTO)

    with pytest.raises(AssetRegistryError):
        registry.validate_position_conversion_registry_state(
            db, predecessor.id, successor.id, "BANPUU.BK",
            "BANPU.BK",
        )


# ── WP4-IIR-B3 — registry preparation conflict safety ──────────────────────

def test_prepare_position_conversion_registry_normal_preparation_still_works():
    db, predecessor, successor = _mint_predecessor_successor()

    rel = registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    assert rel.from_asset_id == predecessor.id
    assert rel.to_asset_id == successor.id
    registry.validate_position_conversion_registry_state(
        db, predecessor.id, successor.id, "BANPUU.BK",
        "BANPU.BK",
    )  # must not raise


def test_prepare_position_conversion_registry_repeated_identical_preparation_is_idempotent():
    db, predecessor, successor = _mint_predecessor_successor()

    first = registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )
    second = registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )
    third = registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    assert first.id == second.id == third.id
    merged_into = [
        row for row in registry.get_relationships(db, predecessor.id)
        if row.relationship_type == RelationshipType.MERGED_INTO.value
    ]
    assert len(merged_into) == 1
    registry.validate_position_conversion_registry_state(
        db, predecessor.id, successor.id, "BANPUU.BK",
        "BANPU.BK",
    )  # still exactly one edge; still valid


def test_prepare_position_conversion_registry_rejects_conflicting_pre_existing_merged_into():
    """WP4-IIR-B3: a predecessor already carrying an outgoing MERGED_INTO
    edge to a DIFFERENT asset must reject a request to prepare a conversion
    to a new successor — not silently add a second edge alongside the
    conflicting one."""
    db, predecessor, successor = _mint_predecessor_successor()
    other_successor = registry.mint(db, _claim(canonical_symbol="OTHERSUCC"))

    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    with pytest.raises(AssetRegistryError):
        registry.prepare_position_conversion_registry(
            db, predecessor.id, other_successor.id, "OTHERSUCC.BK", source="banpu-wp4",
        )


def test_prepare_position_conversion_registry_conflict_persists_no_second_edge():
    """WP4-IIR-B3: after a rejected conflicting preparation attempt, the
    predecessor still carries exactly one MERGED_INTO edge — to the
    original successor, never a second edge to the conflicting one."""
    db, predecessor, successor = _mint_predecessor_successor()
    other_successor = registry.mint(db, _claim(canonical_symbol="OTHERSUCC"))

    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )
    with pytest.raises(AssetRegistryError):
        registry.prepare_position_conversion_registry(
            db, predecessor.id, other_successor.id, "OTHERSUCC.BK", source="banpu-wp4",
        )

    merged_into = [
        row for row in registry.get_relationships(db, predecessor.id)
        if row.relationship_type == RelationshipType.MERGED_INTO.value
    ]
    assert len(merged_into) == 1
    assert merged_into[0].to_asset_id == successor.id


def test_prepare_position_conversion_registry_conflict_leaves_registry_state_unchanged():
    """WP4-IIR-B3: the conflict check must run BEFORE any mutation, so a
    rejected conflicting preparation leaves the predecessor's identifier,
    status, and the successor's identifier state exactly as they were —
    the failure is not merely non-doubling of the edge, but a true no-op."""
    db, predecessor, successor = _mint_predecessor_successor()
    other_successor = registry.mint(db, _claim(canonical_symbol="OTHERSUCC"))

    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )
    predecessor_status_before = registry.get_asset(db, predecessor.id).status
    predecessor_identifiers_before = registry.get_identifiers(db, predecessor.id, current_only=True)
    other_successor_identifiers_before = registry.get_identifiers(db, other_successor.id, current_only=True)

    with pytest.raises(AssetRegistryError):
        registry.prepare_position_conversion_registry(
            db, predecessor.id, other_successor.id, "OTHERSUCC.BK", source="banpu-wp4",
        )

    assert registry.get_asset(db, predecessor.id).status == predecessor_status_before
    assert registry.get_identifiers(db, predecessor.id, current_only=True) == predecessor_identifiers_before
    assert registry.get_identifiers(db, other_successor.id, current_only=True) == other_successor_identifiers_before
    registry.validate_position_conversion_registry_state(
        db, predecessor.id, successor.id, "BANPUU.BK",
        "BANPU.BK",
    )  # original preparation is still exactly and only what is valid


# ── WP4-IIR-B2 second-renewed correction — predecessor provider symbol ─────
# resolved from registry/identifier state, never trusted from caller-
# supplied payload text.

def test_resolve_predecessor_provider_symbol_reads_retired_identifier():
    db, predecessor, successor = _mint_predecessor_successor()
    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    assert registry.resolve_predecessor_provider_symbol(db, predecessor.id) == "BANPU.BK"


def test_resolve_predecessor_provider_symbol_ignores_caller_supplied_text():
    """The resolved value depends only on registry state -- there is no
    caller-supplied parameter for it to ever be influenced by."""
    db, predecessor, successor = _mint_predecessor_successor()
    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    resolved_a = registry.resolve_predecessor_provider_symbol(db, predecessor.id)
    resolved_b = registry.resolve_predecessor_provider_symbol(db, predecessor.id)
    assert resolved_a == resolved_b == "BANPU.BK"


def test_resolve_predecessor_provider_symbol_rejects_asset_with_no_identifier():
    """Fail-closed: an asset with no PROVIDER_SYMBOL identifier of any
    currency has no registry-authoritative value to derive -- this must
    never fall back to a hard-coded or arbitrary value."""
    db = make_session()
    predecessor = registry.mint(db, _claim(canonical_symbol="NOIDENT"))

    with pytest.raises(AssetRegistryError):
        registry.resolve_predecessor_provider_symbol(db, predecessor.id)


def test_validate_position_conversion_registry_state_rejects_wrong_predecessor_provider_symbol():
    """WP4-IIR-B2 second-renewed correction: an arbitrary/adversarial
    caller-supplied predecessor provider symbol that does not match the
    registry-derived value must fail closed, exactly like the existing
    successor-provider-symbol mismatch check."""
    db, predecessor, successor = _mint_predecessor_successor()
    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    for adversarial_label in ("CALLER-PROVIDER-PRE-A", "CALLER-PROVIDER-PRE-B", ""):
        with pytest.raises(AssetRegistryError):
            registry.validate_position_conversion_registry_state(
                db, predecessor.id, successor.id, "BANPUU.BK",
                adversarial_label,
            )


def test_validate_position_conversion_registry_state_accepts_only_registry_derived_predecessor_provider_symbol():
    db, predecessor, successor = _mint_predecessor_successor()
    registry.prepare_position_conversion_registry(
        db, predecessor.id, successor.id, "BANPUU.BK", source="banpu-wp4",
    )

    registry.validate_position_conversion_registry_state(
        db, predecessor.id, successor.id, "BANPUU.BK",
        "BANPU.BK",
    )  # must not raise -- matches the registry-derived value exactly
