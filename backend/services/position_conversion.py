"""position_conversion.py — BANPU-WP6 succession-lookup mechanism (WP6-C1).

Narrow, read-only helper: given a starting identity (asset_id or symbol) and
an as-of date, resolves the identity (asset_id, canonical symbol) that
should be used for valuation/evaluation purposes on that date — the
predecessor's own identity if no admissible succession applies as of that
date, or the successor's identity if one does.

Built entirely from already-existing, already-frozen registry primitives
(asset_repository.get_asset_by_canonical_symbol / get_relationships). Adds
no new registry primitive and no schema change — only a read-only
composition of what WP1/WP4 already built (ENGINEERING_PRINCIPLES.md
"Reuse Before Create"). See BANPU_WP6_WORK_PACKAGE_PLAN.md §7.1.

Single-hop only: follows at most one outgoing MERGED_INTO edge from the
starting asset — does not walk a chain of successive conversions. This is a
deliberate scope boundary (WPP §7.1, §8 #3), not an oversight.

This module performs no write of its own: it creates, modifies, or retires
no AssetRelationship, AssetIdentifier, or asset lifecycle status, and does
not compute conversion ratios or share quantities (that remains
shadow_tracker.py's responsibility, WPP §7.2).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from sqlalchemy.orm import Session

from services import asset_repository as repo
from services.asset_domain import AssetId, RelationshipType


class PositionConversionLookupError(ValueError):
    """Raised only when the caller-supplied asset_id/symbol does not resolve
    to any Asset at all. Never raised for the ordinary "no succession as of
    this date" case — absence of a conversion is ALWAYS a normal, silent,
    fail-toward-predecessor result (WPP §7.1 "Failure behavior")."""


@dataclass(frozen=True)
class ResolvedIdentity:
    """The identity to use for valuation/evaluation purposes as of the
    caller's as-of date, plus whether an admissible succession applied."""

    asset_id: int
    symbol: str
    converted: bool


@dataclass(frozen=True)
class SuccessionBoundary:
    """The single outgoing MERGED_INTO relationship for an identity,
    independent of any as-of date — the exact predecessor/successor/
    effective-date triple `resolve_identity` uses for its own boundary
    decision, exposed so a caller can bind evidence (e.g. a ledger
    conversion-ratio row) to precisely this relationship rather than an
    independently derived date (WP6-IIR-B3/B4 correction; see
    shadow_tracker.py's `_conversion_ratio`/`_carry_succession_identity`
    and `_shadow_conversion_boundary`)."""

    predecessor_asset_id: int
    predecessor_symbol: str
    successor_asset_id: int
    successor_symbol: str
    effective_date: date


def _parse_as_of_date(as_of_date: str) -> date:
    return datetime.strptime(as_of_date, "%Y-%m-%d").date()


def _resolve_starting_asset(
    db: Session, *, asset_id: int | None, symbol: str | None,
):
    if (asset_id is None) == (symbol is None):
        raise ValueError("exactly one of asset_id or symbol must be supplied")
    if asset_id is not None:
        return repo.get_asset(db, AssetId(asset_id))
    return repo.get_asset_by_canonical_symbol(db, symbol)


def _outgoing_merge_relationships(db: Session, asset) -> list:
    """Single-hop only (WPP §7.1, §8 #3): only *asset*'s own outgoing edges
    are inspected — a successor's own later conversion, if any, is out of
    scope and is never chased. An edge with `effective_date IS NULL` is not
    yet effective-dated and is excluded (WPP §8 #4)."""
    relationships = repo.get_relationships(db, AssetId(asset.id))
    return [
        r for r in relationships
        if r.from_asset_id == asset.id
        and r.relationship_type == RelationshipType.MERGED_INTO.value
        and r.effective_date is not None
    ]


def resolve_identity(
    db: Session,
    *,
    asset_id: int | None = None,
    symbol: str | None = None,
    as_of_date: str,
) -> ResolvedIdentity:
    """Resolve the identity that should be used for valuation/evaluation
    purposes as of *as_of_date*.

    Exactly one of *asset_id* / *symbol* must be supplied. Boundary
    inclusivity is `>=`: `as_of_date >= effective_date` resolves to the
    successor; `as_of_date < effective_date` resolves to the predecessor
    (WPP §7.1, §8 #2 — mirrors the `from_date >= earliest_transition_date`
    convention BANPU_WP5_WORK_PACKAGE_PLAN.md §8 already established for the
    identical boundary-date family). A relationship whose `effective_date`
    is None is not yet effective-dated and never resolves a successor
    (WPP §8 #4).

    Raises PositionConversionLookupError only if the starting identity does
    not resolve to any Asset at all.
    """
    asset = _resolve_starting_asset(db, asset_id=asset_id, symbol=symbol)
    if asset is None:
        identifier = asset_id if asset_id is not None else symbol
        raise PositionConversionLookupError(
            f"no asset resolves for identity={identifier!r}"
        )

    as_of = _parse_as_of_date(as_of_date)

    for rel in _outgoing_merge_relationships(db, asset):
        if as_of >= rel.effective_date.date():
            successor = repo.get_asset(db, AssetId(rel.to_asset_id))
            if successor is not None:
                return ResolvedIdentity(
                    asset_id=successor.id,
                    symbol=successor.canonical_symbol,
                    converted=True,
                )

    return ResolvedIdentity(asset_id=asset.id, symbol=asset.canonical_symbol, converted=False)


def find_succession_boundary(
    db: Session,
    *,
    asset_id: int | None = None,
    symbol: str | None = None,
) -> SuccessionBoundary | None:
    """Read-only: the single outgoing MERGED_INTO relationship for the given
    identity, independent of any as-of date. Returns None if the identity
    does not resolve to any Asset, or resolves but has no admissible
    outgoing succession (the common, non-BANPU case).

    Exists so a caller needing the exact predecessor asset_id, successor
    asset_id, and effective_date together (to bind ledger evidence to this
    specific relationship, or to compute a persisted-regeneration write
    boundary) can do so without independently re-deriving what
    `resolve_identity` already establishes as this identity's one
    admissible transition (WP6-IIR-B3/B4/B2 correction — see
    `BANPU_WP6_INDEPENDENT_IMPLEMENTATION_REVIEW.md` §7, §15).
    """
    asset = _resolve_starting_asset(db, asset_id=asset_id, symbol=symbol)
    if asset is None:
        return None

    outgoing = _outgoing_merge_relationships(db, asset)
    if not outgoing:
        return None

    # The registry's existing single-outgoing-edge invariant (WP4's
    # WP4-IIR-B3 guard) makes this at most one relationship in practice;
    # `min` is a defensive tie-break, not chain-walking.
    rel = min(outgoing, key=lambda r: r.effective_date)
    successor = repo.get_asset(db, AssetId(rel.to_asset_id))
    if successor is None:
        return None

    return SuccessionBoundary(
        predecessor_asset_id=asset.id,
        predecessor_symbol=asset.canonical_symbol,
        successor_asset_id=successor.id,
        successor_symbol=successor.canonical_symbol,
        effective_date=rel.effective_date.date(),
    )
