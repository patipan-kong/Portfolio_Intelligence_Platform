"""Current sector classification for Portfolio reporting."""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal

from sqlalchemy.orm import Session

from models.database import PortfolioItem
from services import identity_resolver, registry_service
from services.asset_domain import ClassificationDimension, IdentifierRecord, IdentifierType, RelationshipType
from services.resolver_domain import ResolutionClaim, ResolutionVerdict
from services.sector_taxonomy import normalize_sector, static_sector_lookup

_log = logging.getLogger(__name__)


@dataclass(frozen=True)
class PortfolioSectorClassification:
    sector: str
    classification_source: Literal["registry_fact", "stored_projection", "static_taxonomy", "unresolved"]
    classification_status: Literal["authoritative", "provisional", "unresolved"]


_UNRESOLVED = PortfolioSectorClassification("Other", "unresolved", "unresolved")


def resolve_portfolio_sector(db: Session, holding: PortfolioItem) -> PortfolioSectorClassification:
    """Resolve a reporting label without changing the holding or its instrument."""
    symbol = holding.symbol.strip().upper()
    stored_sector = normalize_sector(holding.sector)
    stored_classification = (
        PortfolioSectorClassification(stored_sector, "stored_projection", "provisional")
        if stored_sector != "Other" else _UNRESOLVED
    )
    asset_id = holding.asset_id
    if asset_id is None:
        resolution = identity_resolver.resolve(
            db,
            ResolutionClaim(identifiers=(
                IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, symbol, source="portfolio_sector"),
            )),
            record_finding=False,
        )
        if resolution.verdict in (ResolutionVerdict.AMBIGUOUS, ResolutionVerdict.CONFLICT):
            return stored_classification
        asset_id = resolution.resolved_asset_id

    underlying_ids = []
    if asset_id is not None:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        underlying_ids = [
            link.to_asset_id for link in registry_service.get_relationships(db, asset_id)
            if link.from_asset_id == asset_id
            and link.relationship_type == RelationshipType.DEPOSITARY_RECEIPT_OF.value
            and (link.effective_date is None or link.effective_date <= now)
        ]
        if len(underlying_ids) > 1:
            _log.warning("Ambiguous Registry underlying for Portfolio holding %s", symbol)
            return _UNRESOLVED

    # A prefix can select a fallback bucket only after the Registry establishes the DR link.
    mapped_sector = static_sector_lookup(symbol, is_dr=bool(underlying_ids))
    if asset_id is not None:
        sector_asset_id = underlying_ids[0] if underlying_ids else asset_id
        facts = registry_service.get_classifications(
            db, sector_asset_id, dimension=ClassificationDimension.SECTOR, current_only=True,
        )
        for fact in facts:
            if fact.as_of is not None and fact.as_of > now:
                continue
            registry_sector = fact.value.strip()
            if registry_sector and registry_sector != "Other":
                if mapped_sector and registry_sector != mapped_sector:
                    _log.warning(
                        "Portfolio sector conflict for %s: Registry asset %s reports %s "
                        "(source %s), static taxonomy reports %s",
                        symbol, sector_asset_id, registry_sector, fact.source, mapped_sector,
                    )
                return PortfolioSectorClassification(registry_sector, "registry_fact", "authoritative")

    if stored_classification is not _UNRESOLVED:
        return stored_classification
    if mapped_sector:
        return PortfolioSectorClassification(mapped_sector, "static_taxonomy", "provisional")
    return _UNRESOLVED
