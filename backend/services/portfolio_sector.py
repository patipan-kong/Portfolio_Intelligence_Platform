"""Canonical sector resolution for current reporting and new optimizer runs."""

import json
import logging
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Literal

from sqlalchemy.orm import Session

from models.database import MarketDataCache, PortfolioItem, Watchlist
from services import identity_resolver, registry_service
from services.asset_domain import ClassificationDimension, IdentifierRecord, IdentifierType, RelationshipType
from services.resolver_domain import ResolutionClaim, ResolutionVerdict
from services.sector_taxonomy import dr_prefix, normalize_sector, static_sector_lookup


_log = logging.getLogger(__name__)
SECTOR_CLASSIFICATION_VERSION = "wealth.sector-classification.v1"
# Exact source tags only. A fact also needs an applicable as-of date.
STEWARD_SECTOR_SOURCES = frozenset({"steward:sector"})


@dataclass(frozen=True)
class PortfolioSectorClassification:
    sector: str
    classification_source: Literal["registry_fact", "provider_metadata", "stored_projection", "static_taxonomy", "unresolved"]
    classification_status: Literal["authoritative", "provisional", "unresolved"]
    raw_sector: str | None = None
    observed_at: str | None = None
    held_asset_id: int | None = None
    classified_asset_id: int | None = None
    conflict_reason: str | None = None
    evidence_source: str | None = None


_UNRESOLVED = PortfolioSectorClassification("Other", "unresolved", "unresolved")


def _provider_evidence(db: Session, asset_id: int, now: datetime):
    identifiers = registry_service.get_identifiers(db, asset_id, current_only=True)
    symbols = {
        item.value for item in identifiers
        if item.identifier_type == IdentifierType.PROVIDER_SYMBOL.value
        and (item.as_of is None or item.as_of <= now)
    }
    if not symbols:
        return []
    rows = db.query(MarketDataCache).filter(
        MarketDataCache.symbol.in_(symbols),
        MarketDataCache.cache_type == "fundamental",
        MarketDataCache.fetched_at <= now,
        MarketDataCache.expires_at > now,
    ).order_by(MarketDataCache.fetched_at.desc(), MarketDataCache.symbol).all()
    evidence = []
    for row in rows:
        resolution = identity_resolver.resolve(
            db, ResolutionClaim(identifiers=(
                IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, row.symbol, source="sector_provider_cache"),
            )), record_finding=False,
        )
        if resolution.resolved_asset_id != asset_id:
            continue
        try:
            raw = json.loads(row.payload_json).get("sector")
        except (ValueError, AttributeError):
            continue
        if isinstance(raw, str) and raw.strip():
            evidence.append((raw.strip(), row.fetched_at.isoformat() + "Z", f"yahoo:{row.symbol}"))
    return evidence


def resolve_portfolio_sector(db: Session, holding: PortfolioItem | Watchlist) -> PortfolioSectorClassification:
    """Resolve exposure without writing identity, sector or market data."""
    symbol = holding.symbol.strip().upper()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    asset_id = holding.asset_id
    if asset_id is None:
        resolution = identity_resolver.resolve(
            db, ResolutionClaim(identifiers=(
                IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, symbol, source="portfolio_sector"),
            )), record_finding=False,
        )
        if resolution.verdict in (ResolutionVerdict.AMBIGUOUS, ResolutionVerdict.CONFLICT):
            return replace(_UNRESOLVED, conflict_reason="Ambiguous or conflicting held identity")
        asset_id = resolution.resolved_asset_id

    result = replace(_UNRESOLVED, held_asset_id=asset_id)
    links = [
        link for link in registry_service.get_relationships(db, asset_id)
        if link.from_asset_id == asset_id
        and link.relationship_type == RelationshipType.DEPOSITARY_RECEIPT_OF.value
    ] if asset_id is not None else []
    underlying_ids = {
        link.to_asset_id for link in links if link.effective_date is None or link.effective_date <= now
    }
    # The symbol pattern is only a reason to withhold look-through, never proof of identity.
    if len(underlying_ids) > 1:
        return replace(result, conflict_reason="Ambiguous Registry underlying")
    if not underlying_ids and (links or (symbol.endswith(".BK") and dr_prefix(symbol))):
        return replace(result, conflict_reason="No applicable verified Registry underlying")
    classified_id = next(iter(underlying_ids), asset_id)
    result = replace(result, classified_asset_id=classified_id)

    stored = normalize_sector(holding.sector)
    mapped = static_sector_lookup(symbol, is_dr=bool(underlying_ids))
    provider = []
    facts = []
    if classified_id is not None:
        facts = [
            fact for fact in registry_service.get_classifications(
                db, classified_id, dimension=ClassificationDimension.SECTOR, current_only=True,
            )
            if fact.source in STEWARD_SECTOR_SOURCES and fact.as_of is not None and fact.as_of <= now
        ]
        provider = _provider_evidence(db, classified_id, now)

    provider_keys = {normalize_sector(raw) for raw, _, _ in provider} - {"Other"}
    fact_keys = {normalize_sector(fact.value) for fact in facts}
    if facts and (len(fact_keys) != 1 or "Other" in fact_keys):
        return replace(result, raw_sector=", ".join(sorted({fact.value for fact in facts})),
                       conflict_reason="Conflicting or unmapped stewarded sector facts")
    if not facts and len(provider_keys) > 1:
        return replace(result, raw_sector=", ".join(sorted({raw for raw, _, _ in provider})),
                       conflict_reason="Conflicting fresh provider sectors")

    if facts:
        fact = max(facts, key=lambda fact: (fact.as_of, fact.id))
        result = replace(result, sector=normalize_sector(fact.value), classification_source="registry_fact",
                         classification_status="authoritative", raw_sector=fact.value,
                         observed_at=fact.as_of.isoformat() + "Z", evidence_source=fact.source)
    elif provider_keys:
        raw, timestamp, source = next(row for row in provider if normalize_sector(row[0]) != "Other")
        result = replace(result, sector=normalize_sector(raw), classification_source="provider_metadata",
                         classification_status="provisional", raw_sector=raw, observed_at=timestamp,
                         evidence_source=source)
    elif stored != "Other":
        result = replace(result, sector=stored, classification_source="stored_projection",
                         classification_status="provisional", raw_sector=holding.sector)
    elif mapped:
        result = replace(result, sector=mapped, classification_source="static_taxonomy",
                         classification_status="provisional", raw_sector=mapped)
    elif provider:
        raw, timestamp, source = provider[0]
        return replace(result, raw_sector=raw, observed_at=timestamp, evidence_source=source,
                       conflict_reason="Unmapped provider sector")

    disagreements = [
        f"{label}: {sector}" for label, sector in (
            ("stored projection", stored), ("static taxonomy", mapped),
            *(("provider metadata", key) for key in sorted(provider_keys)),
        ) if sector and sector not in ("Other", result.sector)
    ]
    unmapped = sorted({raw for raw, _, _ in provider if normalize_sector(raw) == "Other" and raw != "Other"})
    reasons = []
    if disagreements:
        reasons.append(f"{result.sector} differs from " + ", ".join(disagreements))
    if unmapped:
        reasons.append("Unmapped provider sector: " + ", ".join(unmapped))
    if reasons:
        reason = ". ".join(reasons)
        _log.warning("Sector classification conflict for %s: %s", symbol, reason)
        result = replace(result, conflict_reason=reason)
    return result
