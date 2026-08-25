"""Tests for the BANPU-WP6 succession-lookup mechanism (WP6-C1).

Covers WP6-A1 (succession lookup correctness) and WP6-A2 (effective-date
correctness) from BANPU_WP6_WORK_PACKAGE_PLAN.md §10. Pure unit tests
against an in-memory SQLite database — mirrors test_asset_registry.py's
fixture pattern (no network calls).
"""
import os
import sys
from datetime import datetime

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import Base
import models.asset  # noqa: F401 — registers Asset* tables on Base.metadata
from services import asset_registry as registry
from services import position_conversion as pc
from services.asset_domain import AssetClaim, AssetType, RelationshipType


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


def _claim(**overrides):
    defaults = dict(
        canonical_symbol="BANPU",
        asset_type=AssetType.EQUITY,
        market="TH",
        exchange="SET",
        currency="THB",
    )
    defaults.update(overrides)
    return AssetClaim(**defaults)


def _mint_pair(db, *, predecessor_symbol="BANPU", successor_symbol="BANPUNVDR", effective_date=None):
    predecessor = registry.mint(db, _claim(canonical_symbol=predecessor_symbol))
    successor = registry.mint(db, _claim(canonical_symbol=successor_symbol))
    registry.link_relationship(
        db, predecessor.id, successor.id, RelationshipType.MERGED_INTO,
        effective_date=effective_date,
    )
    return predecessor, successor


# ── WP6-A1: succession lookup correctness ──────────────────────────────────

def test_resolves_predecessor_before_boundary():
    db = make_session()
    predecessor, successor = _mint_pair(
        db, effective_date=datetime(2026, 6, 1),
    )

    result = pc.resolve_identity(db, asset_id=predecessor.id, as_of_date="2026-05-31")

    assert result.asset_id == predecessor.id
    assert result.symbol == predecessor.canonical_symbol
    assert result.converted is False


def test_resolves_successor_at_boundary_inclusive():
    db = make_session()
    predecessor, successor = _mint_pair(
        db, effective_date=datetime(2026, 6, 1),
    )

    result = pc.resolve_identity(db, asset_id=predecessor.id, as_of_date="2026-06-01")

    assert result.asset_id == successor.id
    assert result.symbol == successor.canonical_symbol
    assert result.converted is True


def test_resolves_successor_after_boundary():
    db = make_session()
    predecessor, successor = _mint_pair(
        db, effective_date=datetime(2026, 6, 1),
    )

    result = pc.resolve_identity(db, asset_id=predecessor.id, as_of_date="2026-12-31")

    assert result.asset_id == successor.id
    assert result.converted is True


def test_resolves_by_symbol_not_only_asset_id():
    db = make_session()
    predecessor, successor = _mint_pair(
        db, effective_date=datetime(2026, 6, 1),
    )

    result = pc.resolve_identity(db, symbol=predecessor.canonical_symbol, as_of_date="2026-06-01")

    assert result.asset_id == successor.id
    assert result.converted is True


def test_no_relationship_resolves_to_own_identity():
    db = make_session()
    asset = registry.mint(db, _claim(canonical_symbol="KBANK"))

    result = pc.resolve_identity(db, asset_id=asset.id, as_of_date="2026-06-01")

    assert result.asset_id == asset.id
    assert result.symbol == "KBANK"
    assert result.converted is False


def test_single_hop_only_no_chain_walking():
    """A successor's own later conversion is out of scope — WPP §7.1, §8 #3."""
    db = make_session()
    predecessor, successor = _mint_pair(
        db, predecessor_symbol="A", successor_symbol="B",
        effective_date=datetime(2026, 1, 1),
    )
    third = registry.mint(db, _claim(canonical_symbol="C"))
    registry.link_relationship(
        db, successor.id, third.id, RelationshipType.MERGED_INTO,
        effective_date=datetime(2026, 6, 1),
    )

    # Even after both boundaries, resolving from the ORIGINAL predecessor
    # stops at the first hop (B), never chases B's own conversion to C.
    result = pc.resolve_identity(db, asset_id=predecessor.id, as_of_date="2026-12-31")

    assert result.asset_id == successor.id
    assert result.symbol == "B"
    assert result.converted is True


def test_unknown_asset_id_raises():
    db = make_session()
    with pytest.raises(pc.PositionConversionLookupError):
        pc.resolve_identity(db, asset_id=999999, as_of_date="2026-06-01")


def test_unknown_symbol_raises():
    db = make_session()
    with pytest.raises(pc.PositionConversionLookupError):
        pc.resolve_identity(db, symbol="NOSUCHSYMBOL", as_of_date="2026-06-01")


def test_requires_exactly_one_of_asset_id_or_symbol():
    db = make_session()
    with pytest.raises(ValueError):
        pc.resolve_identity(db, as_of_date="2026-06-01")
    with pytest.raises(ValueError):
        pc.resolve_identity(db, asset_id=1, symbol="X", as_of_date="2026-06-01")


# ── WP6-A2: effective-date correctness ──────────────────────────────────────

def test_unset_effective_date_never_resolves_successor():
    db = make_session()
    predecessor, successor = _mint_pair(db, effective_date=None)

    result = pc.resolve_identity(db, asset_id=predecessor.id, as_of_date="2099-01-01")

    assert result.asset_id == predecessor.id
    assert result.converted is False
