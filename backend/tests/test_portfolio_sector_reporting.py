"""Read-only sector resolution shared by the two Portfolio endpoints."""

import asyncio
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

import main
from models.database import MarketDataCache, Base, Portfolio, PortfolioItem, Transaction, Workspace
from services import registry_service
from services.asset_domain import (
    AssetClaim,
    AssetType,
    ClassificationDimension,
    IdentifierRecord,
    IdentifierType,
    RelationshipType,
)
from services.portfolio_sector import resolve_portfolio_sector
from services.optimizer.sector_policy import freeze_positions


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


def _mint(db, symbol, *, local=True):
    return registry_service.mint_asset(
        db,
        AssetClaim(
            canonical_symbol=symbol, asset_type=AssetType.EQUITY,
            market="Thailand" if local else "United States",
            exchange="SET" if local else "NASDAQ",
            currency="THB" if local else "USD",
        ),
        identifiers=[IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, symbol, source="test")],
    )


@pytest.mark.parametrize("underlying_sector", [None, "Communication Services"])
def test_current_holdings_and_allocation_share_sector_resolution(db, caplog, underlying_sector):
    workspace = Workspace(name="Portfolio sectors")
    db.add(workspace)
    db.flush()
    portfolio = Portfolio(workspace_id=workspace.id, name="TA", cash_balance=238_280.22)
    db.add(portfolio)
    db.flush()
    portfolio_id = portfolio.id

    specs = [
        ("GOOGL01.BK", "GOOGL", 2000, 35.759972, "Other"),
        ("MICRON01.BK", "MU", 5000, 20.233934, "Other"),
        ("NVDA01.BK", "NVDA", 5000, 21.018583, "Technology"),
        ("BH.BK", None, 800, 179.241173, "Healthcare"),
        ("GULF.BK", None, 2000, 58.026563, "Utilities"),
        ("GOOGL99.BK", None, 10, 10, "Other"),
    ]
    for symbol, parent, shares, cost, stored in specs:
        listing = None if symbol == "GOOGL99.BK" else _mint(db, symbol)
        if parent:
            underlying = _mint(db, parent, local=False)
            registry_service.link_relationship(
                db, listing.id, underlying.id, RelationshipType.DEPOSITARY_RECEIPT_OF,
            )
            if parent == "GOOGL" and underlying_sector:
                registry_service.record_classification(
                    db, listing.id, ClassificationDimension.SECTOR, "Industrial", source="test:listing",
                )
                registry_service.record_classification(
                    db, underlying.id, ClassificationDimension.SECTOR, "Consumer", source="test:historical",
                    as_of=datetime(2024, 1, 1),
                )
                registry_service.record_classification(
                    db, underlying.id, ClassificationDimension.SECTOR, underlying_sector,
                    source="steward:sector", as_of=datetime(2025, 1, 1),
                )
            if parent == "NVDA" and underlying_sector:
                registry_service.record_classification(
                    db, underlying.id, ClassificationDimension.SECTOR, "Technology", source="steward:sector", as_of=datetime(2025, 1, 1),
                )
        db.add(PortfolioItem(
            workspace_id=workspace.id, portfolio_id=portfolio_id, symbol=symbol,
            asset_id=listing.id if listing and symbol != "GOOGL01.BK" else None,
            shares=shares, avg_cost=cost, sector=stored,
        ))
    db.add(Transaction(
        workspace_id=workspace.id, portfolio_id=portfolio_id, symbol="GOOGL01.BK",
        transaction_type="BUY", shares=2000, price_per_share=35.759972,
        total_amount=71_519.944, fees=0, transaction_date=datetime(2026, 5, 27), sector="Other",
    ))
    db.commit()
    db.execute(text("PRAGMA query_only = ON"))

    holdings = asyncio.run(main.list_holdings(portfolio_id, db))
    breakdown = asyncio.run(main.get_sector_breakdown(portfolio_id, db))
    expected = {
        "GOOGL01.BK": underlying_sector or "Technology",
        "MICRON01.BK": "Technology",
        "NVDA01.BK": "Technology",
        "BH.BK": "Healthcare",
        "GULF.BK": "Utilities",
        "GOOGL99.BK": "Other",
    }
    assert {row["symbol"]: row["sector"] for row in holdings} == expected
    frozen = freeze_positions(holdings)
    assert {symbol: row["sector"] for symbol, row in frozen.items()} == expected
    assert frozen["GOOGL01.BK"]["sector_classification"] == next(
        row["sector_classification"] for row in holdings if row["symbol"] == "GOOGL01.BK"
    )
    assert {symbol: bucket["sector"] for bucket in breakdown["sectors"] for symbol in bucket["stocks"]} == expected
    provenance = {
        "GOOGL01.BK": ("registry_fact", "authoritative") if underlying_sector else ("static_taxonomy", "provisional"),
        "MICRON01.BK": ("static_taxonomy", "provisional"),
        "NVDA01.BK": ("registry_fact", "authoritative") if underlying_sector else ("stored_projection", "provisional"),
        "BH.BK": ("stored_projection", "provisional"),
        "GULF.BK": ("stored_projection", "provisional"),
        "GOOGL99.BK": ("unresolved", "unresolved"),
    }
    assert {row["symbol"]: (row["classification_source"], row["classification_status"]) for row in holdings} == provenance
    for bucket in breakdown["sectors"]:
        sources, statuses = zip(*(provenance[symbol] for symbol in bucket["stocks"]))
        assert bucket["classification_sources"] == sorted(set(sources))
        assert bucket["classification_status"] == ("provisional" if "provisional" in statuses else statuses[0])

    assert {row["symbol"]: (row["shares"], row["avg_cost"], row["current_price"]) for row in holdings} == {
        symbol: (shares, cost, None) for symbol, _, shares, cost, _ in specs
    }
    costs = defaultdict(float)
    for symbol, _, shares, cost, _ in specs:
        costs[expected[symbol]] += shares * cost
    total_cost = sum(costs.values())
    assert breakdown["total_value"] == round(total_cost, 2)
    assert {row["sector"]: (row["value"], row["weight_pct"]) for row in breakdown["sectors"]} == {
        sector: (round(value, 2), round(value / total_cost * 100, 1))
        for sector, value in costs.items()
    }

    assert dict(db.query(PortfolioItem.symbol, PortfolioItem.sector).all()) == {
        symbol: stored for symbol, _, _, _, stored in specs
    }
    assert portfolio.cash_balance == 238_280.22
    trade = db.query(Transaction).one()
    assert (trade.symbol, trade.shares, trade.total_amount, trade.sector) == (
        "GOOGL01.BK", 2000, 71_519.944, "Other",
    )
    if underlying_sector:
        assert "Communication Services differs from static taxonomy: Technology" in caplog.text


def test_ambiguous_dr_relationship_does_not_certify_stored_or_static_sector(db):
    listing = _mint(db, "MICRON01.BK")
    for symbol in ("MU", "MU-ALT"):
        parent = _mint(db, symbol, local=False)
        registry_service.link_relationship(
            db, listing.id, parent.id, RelationshipType.DEPOSITARY_RECEIPT_OF,
        )
        registry_service.record_classification(
            db, parent.id, ClassificationDimension.SECTOR, "Technology", source="test:stewarded",
        )
    holding = PortfolioItem(symbol="MICRON01.BK", asset_id=listing.id, sector="Technology")
    db.commit()
    db.execute(text("PRAGMA query_only = ON"))

    result = resolve_portfolio_sector(db, holding)
    assert (result.sector, result.classification_status) == ("Other", "unresolved")
    assert result.conflict_reason == "Ambiguous Registry underlying"

@pytest.mark.parametrize(
    ("raw", "fresh", "expected", "source"),
    [
        ("Communication Services", True, "Communication Services", "provider_metadata"),
        ("Communication Services", False, "Technology", "stored_projection"),
        ("Unmapped Sector", True, "Technology", "stored_projection"),
    ],
)
def test_provider_evidence_is_fresh_matched_and_provisional(db, raw, fresh, expected, source):
    listing = _mint(db, "GOOGL01.BK")
    underlying = _mint(db, "GOOGL", local=False)
    registry_service.link_relationship(db, listing.id, underlying.id, RelationshipType.DEPOSITARY_RECEIPT_OF)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    registry_service.record_classification(
        db, underlying.id, ClassificationDimension.SECTOR, "Industrial",
        source="seed:sector_taxonomy", as_of=now - timedelta(days=1),
    )
    for symbol, label in [("GOOGL", raw), ("GOOGL01.BK", "Financial")]:
        db.add(MarketDataCache(
            symbol=symbol, cache_type="fundamental", payload_json=json.dumps({"sector": label}),
            fetched_at=now - timedelta(hours=2),
            expires_at=now + timedelta(hours=1 if fresh else -1),
        ))
    db.commit()
    db.execute(text("PRAGMA query_only = ON"))
    result = resolve_portfolio_sector(db, PortfolioItem(
        asset_id=listing.id, symbol="GOOGL01.BK", sector="Technology",
    ))
    assert (result.sector, result.classification_source, result.classification_status) == (expected, source, "provisional")
    assert (result.held_asset_id, result.classified_asset_id) == (listing.id, underlying.id)
    if source == "provider_metadata":
        assert result.evidence_source == "yahoo:GOOGL"
        assert "stored projection: Technology" in result.conflict_reason


def test_conflicting_stewarded_facts_are_unresolved(db):
    from models.asset import AssetClassification

    listing = _mint(db, "BH.BK")
    for value in ("Healthcare", "Technology"):
        db.add(AssetClassification(
            asset_id=listing.id, dimension=ClassificationDimension.SECTOR.value, value=value,
            source="steward:sector", as_of=datetime(2025, 1, 1), is_current=True,
        ))
    db.commit()
    result = resolve_portfolio_sector(db, PortfolioItem(asset_id=listing.id, symbol="BH.BK", sector="Healthcare"))
    assert result.classification_status == "unresolved"
    assert "Conflicting" in result.conflict_reason


def test_googl_expiry_uses_static_fallback_and_ignores_local_provider(db):
    listing = _mint(db, "GOOGL01.BK")
    underlying = _mint(db, "GOOGL", local=False)
    registry_service.link_relationship(db, listing.id, underlying.id, RelationshipType.DEPOSITARY_RECEIPT_OF)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    registry_service.record_classification(
        db, underlying.id, ClassificationDimension.SECTOR, "Industrial",
        source="steward:sector", as_of=now + timedelta(days=1),
    )
    for symbol, sector, expires_at in (
        ("GOOGL", "Communication Services", now - timedelta(seconds=1)),
        ("GOOGL01.BK", "Financial", now + timedelta(hours=1)),
    ):
        db.add(MarketDataCache(
            symbol=symbol, cache_type="fundamental", payload_json=json.dumps({"sector": sector}),
            fetched_at=now - timedelta(hours=2), expires_at=expires_at,
        ))
    db.commit()
    db.execute(text("PRAGMA query_only = ON"))
    result = resolve_portfolio_sector(db, PortfolioItem(asset_id=listing.id, symbol="GOOGL01.BK", sector="Other"))
    assert (result.sector, result.classification_source, result.classification_status) == (
        "Technology", "static_taxonomy", "provisional",
    )


@pytest.mark.parametrize("future_link", [False, True])
def test_googl_requires_applicable_underlying_even_with_listing_sector(db, future_link):
    listing = _mint(db, "GOOGL01.BK")
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    registry_service.record_classification(
        db, listing.id, ClassificationDimension.SECTOR, "Technology",
        source="steward:sector", as_of=now - timedelta(days=1),
    )
    if future_link:
        underlying = _mint(db, "GOOGL", local=False)
        registry_service.link_relationship(
            db, listing.id, underlying.id, RelationshipType.DEPOSITARY_RECEIPT_OF,
            effective_date=now + timedelta(days=1),
        )
    db.commit()
    result = resolve_portfolio_sector(db, PortfolioItem(asset_id=listing.id, symbol="GOOGL01.BK", sector="Technology"))
    assert (result.sector, result.classification_status, result.classified_asset_id) == ("Other", "unresolved", None)
