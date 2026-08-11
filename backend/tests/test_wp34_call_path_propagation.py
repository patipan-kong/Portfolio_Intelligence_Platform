"""BANPU-WP3.4 — call-path propagation and regression evidence.

Exercises the actual higher-level callers named in
docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md §4.4,
not just the data_fetcher.py helpers they call through (those are already
covered exhaustively by test_quote_epoch_isolation.py, WP3.3's own suite, and
are not re-derived here). Every test in this module calls a real
``main.py`` endpoint function directly (this codebase's existing convention —
see test_watchlist_registry.py — there is no FastAPI TestClient/HTTP harness)
against a real in-memory SQLite database, and only fakes the outermost
provider I/O boundary (``services.data_fetcher._provider``) plus the
canonical conversion guard projection (``services.data_fetcher.
_read_conversion_guard_projection``), so the real WP3.2/WP3.1 enforcement
chain runs end to end:

    higher-level caller (main.py)
        -> services.data_fetcher.fetch_price_info / resolve_successor_bindings
            -> services.market_data.position_conversion_quote_contract (WP3.2)
                -> accepted result, or a deterministic quarantine

Covers:
  - the one owning call site (GET /portfolios/{id}/prices) supplies the
    WP3.2 binding for a converted successor holding and receives a real,
    accepted quote (not a refusal) — proving propagation actually happened,
    not merely that the fail-closed guard exists;
  - the same site, with propagation removed, demonstrates the counterfactual
    refusal — proving Test 1's success is attributable to propagation;
  - the same site preserves byte-for-byte legacy behavior for an ordinary,
    unconverted holding in the same call;
  - a second, deliberately unbound caller (GET /watchlist) receives the
    structured WP3.3 refusal for a converted identity rather than an
    incorrect legacy value — the register's claim, exercised for real.
"""
import asyncio
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import AgentCache, Base, PortfolioItem, Watchlist
import models.asset  # noqa: F401 — registers Asset* tables on Base.metadata
import models.registry_finding  # noqa: F401 — registers RegistryFinding table

import main
import services.data_fetcher as fetcher
import services.idea_review as idea_review_service
import services.market_data.position_conversion_quote_contract as contract
import services.portfolio_snapshots as portfolio_snapshots
from services.analytics import factor_engine
from services import registry_lookup as lookup
from services.portfolio_snapshots import SnapshotCoverageError
from services.transaction_canonicalizer import (
    PositionConversionBoundaryEvidence,
    PositionConversionDates,
    PositionConversionQuoteBinding,
    PositionConversionSuccessor,
)


# ── Fixtures shared with WP3.3's own suite (test_quote_epoch_isolation.py) ──

@dataclass(frozen=True)
class _Observation:
    timestamp: int
    close: float | None


@dataclass(frozen=True)
class _Evidence:
    provider: str
    requested_symbol: str
    served_symbol: str | None
    observations: tuple
    current_close: float | None
    previous_close: float | None
    exchange_timezone_name: str | None


class _Provider:
    """Fakes only the network boundary. Everything above it is real."""

    def __init__(self, evidence: object | None = None, quote: dict | None = None):
        self.evidence = evidence
        self.quote_result = quote or {
            "current_price": 55.0,
            "previous_close": 54.0,
            "last_updated": "legacy",
        }
        self.evidence_calls = 0
        self.quote_calls = 0

    def get_quote_evidence(self, _symbol: str) -> object | None:
        self.evidence_calls += 1
        return self.evidence

    def get_quote(self, _symbol: str) -> dict:
        self.quote_calls += 1
        return dict(self.quote_result)

    def get_fundamentals(self, _symbol: str) -> dict:
        """Benign empty result — fundamentals/history are outside WP3.4's
        fetch_price_info scope; several higher-level callers incidentally
        reach fetch_info/fetch_history (sector resolution, momentum,
        benchmark timing) on the way to the call site under test, and must
        not crash the test on an unimplemented fake method."""
        return {}

    def get_history(self, _symbol: str, _period: str, _interval: str):
        return None


_EPOCH = date(2024, 1, 2)
_EPOCH_TS = int(datetime(2024, 1, 2, 10, 0, tzinfo=ZoneInfo("Asia/Bangkok")).timestamp())


def _binding(asset_id: int = 42, provider_symbol: str = "SUCC.BK") -> contract.SuccessorQuoteBinding:
    successor = PositionConversionSuccessor(
        asset_id=asset_id, symbol="SUCC", provider_symbol=provider_symbol,
        shares_entitled=10, shares_received=100,
    )
    quote_binding = PositionConversionQuoteBinding(
        provider="yahoo_chart",
        predecessor_provider_symbol="PRED.BK",
        successor_provider_symbol=provider_symbol,
    )
    dates = PositionConversionDates(
        legal_effective_date=date(2023, 12, 28),
        valuation_transition_date=_EPOCH,
        predecessor_last_price_date=date(2024, 1, 1),
        successor_quote_epoch_start_date=_EPOCH,
    )
    return contract.build_successor_quote_binding(successor, quote_binding, dates)


def _evidence(**overrides) -> _Evidence:
    defaults = dict(
        provider="yahoo_chart",
        requested_symbol="SUCC.BK",
        served_symbol="SUCC.BK",
        observations=(_Observation(timestamp=_EPOCH_TS, close=101.0),),
        current_close=101.0,
        previous_close=100.0,
        exchange_timezone_name="Asia/Bangkok",
    )
    defaults.update(overrides)
    return _Evidence(**defaults)


def _boundary_evidence() -> PositionConversionBoundaryEvidence:
    return PositionConversionBoundaryEvidence(
        predecessor_reference_price=Decimal("95.50"),
        successor_reference_price=Decimal("101.25"),
        mechanical_nav_tolerance_pct=Decimal("0.50"),
        suspension_gap_annotation="test fixture",
    )


def _projection_for(binding: contract.SuccessorQuoteBinding) -> fetcher._ConversionGuardProjection:
    return fetcher._ConversionGuardProjection(
        available=True,
        bindings_by_symbol=((binding.provider_symbol, binding),),
        ambiguous_symbols=frozenset(),
        boundary_evidence_by_symbol=((binding.provider_symbol, _boundary_evidence()),),
    )


def _empty_projection() -> fetcher._ConversionGuardProjection:
    return fetcher._ConversionGuardProjection(
        available=True, bindings_by_symbol=(), ambiguous_symbols=frozenset(),
    )


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


def _add_portfolio(db, name="P1"):
    ws_id = main._ws_id(db)
    from models.database import Portfolio
    p = Portfolio(workspace_id=ws_id, name=name, cash_balance=0.0)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def _add_item(db, portfolio, symbol, shares=10.0, avg_cost=50.0):
    ws_id = main._ws_id(db)
    item = PortfolioItem(
        workspace_id=ws_id, portfolio_id=portfolio.id,
        symbol=symbol, shares=shares, avg_cost=avg_cost,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@pytest.fixture(autouse=True)
def _fetch_layer(monkeypatch):
    """Fake only the network/DB boundary owned by data_fetcher.py itself.
    ``resolve_successor_bindings`` and ``fetch_price_info`` run for real."""
    monkeypatch.setattr(fetcher, "allow_market_fetching", lambda: True)
    monkeypatch.setattr(fetcher, "_get_cached", lambda *_: None)
    monkeypatch.setattr(fetcher, "_set_cached", lambda *args: None)
    monkeypatch.setattr(
        fetcher, "_get_stale",
        lambda *_: pytest.fail("no test in this module expects a stale-cache read"),
    )


# ── The owning call site: GET /portfolios/{id}/prices ───────────────────────

def test_owning_call_site_propagates_binding_and_serves_converted_successor_quote(monkeypatch):
    binding = _binding()
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "SUCC.BK")

    rows = asyncio.run(main.get_portfolio_prices(portfolio.id, db))

    assert len(rows) == 1
    assert rows[0]["symbol"] == "SUCC.BK"
    assert rows[0]["current_price"] == 101.0
    assert rows[0]["previous_close"] == 100.0
    assert "_quarantine_reason" not in rows[0]
    # The dual-derivation evidence path was used, never the legacy get_quote().
    assert provider.evidence_calls == 1
    assert provider.quote_calls == 0


def test_owning_call_site_without_propagation_fails_closed(monkeypatch):
    """Counterfactual control: with the same converted binding available but
    resolve_successor_bindings short-circuited to return nothing (simulating
    propagation having been removed), WP3.3's unbound guard refuses the
    request instead of silently serving a price — proving Test 1's success
    is attributable to real propagation, not coincidence."""
    binding = _binding()
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))
    monkeypatch.setattr(main, "resolve_successor_bindings", lambda symbols: {})

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "SUCC.BK")

    rows = asyncio.run(main.get_portfolio_prices(portfolio.id, db))

    assert len(rows) == 1
    assert rows[0]["current_price"] is None
    assert rows[0]["_quarantine_reason"] == "MISSING_OR_AMBIGUOUS_IDENTIFIER"
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0


def test_owning_call_site_preserves_legacy_behavior_for_unconverted_holding(monkeypatch):
    provider = _Provider(quote={
        "current_price": 55.0, "previous_close": None, "last_updated": "legacy-sparse",
    })
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", _empty_projection)

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "PTT.BK")

    rows = asyncio.run(main.get_portfolio_prices(portfolio.id, db))

    assert len(rows) == 1
    assert rows[0]["symbol"] == "PTT.BK"
    assert rows[0]["current_price"] == 55.0
    assert rows[0]["previous_close"] is None
    assert rows[0]["change_percent"] is None
    assert provider.quote_calls == 1
    assert provider.evidence_calls == 0


def test_owning_call_site_handles_mixed_converted_and_unconverted_holdings_independently(monkeypatch):
    binding = _binding()
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "SUCC.BK")
    _add_item(db, portfolio, "PTT.BK")

    rows = asyncio.run(main.get_portfolio_prices(portfolio.id, db))
    by_symbol = {row["symbol"]: row for row in rows}

    assert by_symbol["SUCC.BK"]["current_price"] == 101.0
    assert "_quarantine_reason" not in by_symbol["SUCC.BK"]
    # The unconverted holding is unaffected — it falls to the legacy
    # get_quote() path exactly as before propagation was introduced.
    assert by_symbol["PTT.BK"]["current_price"] == 55.0
    assert provider.evidence_calls == 1
    assert provider.quote_calls == 1


# ── A second, deliberately unbound caller: GET /watchlist ───────────────────

def test_non_owning_call_site_watchlist_refuses_converted_symbol(monkeypatch):
    """The WP3.4 unbound call-site register attributes this site's
    protection to WP3.3 refusal, not to a consumer edit — list_watchlist is
    never given a binding. Proven here against the real fetch_price_info."""
    binding = _binding()
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))
    monkeypatch.setattr(
        lookup, "resolve_many",
        lambda db, queries: {q: lookup.Unresolved(query=str(q), reason="not evaluated") for q in queries},
    )

    db = make_session()
    ws_id = main._ws_id(db)
    db.add(Watchlist(workspace_id=ws_id, symbol="SUCC.BK", sector="Other"))
    db.commit()

    rows = asyncio.run(main.list_watchlist(db))

    assert len(rows) == 1
    assert rows[0]["symbol"] == "SUCC.BK"
    # list_watchlist's response never surfaces current_price/previous_close
    # directly (only derived fields like upside_pct) — the observable proof
    # of refusal is that no provider call was ever made for the converted
    # identity, exactly as an accepted price would require one.
    assert rows[0]["upside_pct"] is None
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0


# ── Step 4.1: exhaustive per-site evidence for the remaining call sites ─────
#
# The eleven-site register (docs/implementation/BANPU_WP3_WORK_PACKAGE_
# DECOMPOSITION_AND_ROADMAP.md §4.4) names exactly one owning call site
# (covered above) and ten deliberately unbound call sites. Two of the ten
# sites live inside the owning endpoint's own function body (its DR-parent
# lookups) and inside the watchlist endpoint's own function body — this
# module attributes each one separately, per the register's own requirement
# that co-located call sites still receive individually identifiable
# evidence.


def _two_binding_projection(
    binding_a: contract.SuccessorQuoteBinding,
    binding_b: contract.SuccessorQuoteBinding,
) -> fetcher._ConversionGuardProjection:
    return fetcher._ConversionGuardProjection(
        available=True,
        bindings_by_symbol=(
            (binding_a.provider_symbol, binding_a),
            (binding_b.provider_symbol, binding_b),
        ),
        ambiguous_symbols=frozenset(),
        boundary_evidence_by_symbol=(
            (binding_a.provider_symbol, _boundary_evidence()),
            (binding_b.provider_symbol, _boundary_evidence()),
        ),
    )


def test_owning_call_site_dr_parent_price_remains_unbound(monkeypatch):
    """main.py:759 — the same GET /portfolios/{id}/prices endpoint that owns
    holding identity also fetches a DR holding's *parent* ticker for
    upside_pct. The parent is not the portfolio's holding identity, so this
    second call site inside the owning function is never given a binding,
    even though propagation is active for the endpoint's primary site."""
    # Bound to "SUCC" — the *parent* ticker (normalize_dr_symbol strips the
    # "01" DR suffix), not the DR holding symbol itself, so only the
    # parent-price call site is exercisable against this binding.
    binding = _binding(provider_symbol="SUCC")
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "SUCC01.BK")  # DR-format holding; parent -> "SUCC"
    ws_id = main._ws_id(db)
    import json as _json
    db.add(AgentCache(
        symbol="SUCC01.BK", agent="fundamental",
        result_json=_json.dumps({"target_price": 120.0}),
    ))
    db.commit()

    rows = asyncio.run(main.get_portfolio_prices(portfolio.id, db))

    assert len(rows) == 1
    # The DR holding's own symbol ("SUCC01.BK") has no binding of its own
    # and proceeds on the ordinary legacy path — resolve_successor_bindings
    # only ever supplies what the guard actually binds. The parent-price
    # lookup for "SUCC" IS guard-bound, but this call site (main.py:759)
    # never propagates a binding into it, so WP3.3's unbound guard refuses
    # it exactly as an unbound caller — upside_pct cannot be computed from a
    # converted-identity guess.
    assert rows[0]["upside_pct"] is None
    # Zero evidence calls (no binding ever reached the bound quote path);
    # exactly one legacy quote call — the DR holding's own unbound price.
    # The refused parent-price lookup made no provider call at all.
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 1


def test_non_owning_call_site_add_holding_refuses_converted_symbol(monkeypatch):
    """main.py:883 — POST /portfolios/{id}/holdings prices the symbol being
    newly added. BPA-1 authorizes propagation only for the GET .../prices
    read path; add_holding is not that call site, so a converted identity
    fails closed here exactly as any other unbound caller."""
    binding = _binding()
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))

    db = make_session()
    portfolio = _add_portfolio(db)

    result = asyncio.run(main.add_holding(
        portfolio.id, main.HoldingCreate(symbol="SUCC.BK", shares=10.0, avg_cost=50.0), db,
    ))

    assert result["symbol"] == "SUCC.BK"
    assert result.get("current_price") is None
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0


def test_non_owning_call_site_watchlist_dr_parent_remains_unbound(monkeypatch):
    """main.py:1052 — GET /watchlist's own DR-parent price lookup, distinct
    from its primary per-item lookup already proven refused above."""
    binding = _binding(provider_symbol="SUCC")  # bound to the parent, not the DR symbol
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))
    monkeypatch.setattr(
        lookup, "resolve_many",
        lambda db, queries: {q: lookup.Unresolved(query=str(q), reason="not evaluated") for q in queries},
    )

    db = make_session()
    ws_id = main._ws_id(db)
    db.add(Watchlist(workspace_id=ws_id, symbol="SUCC01.BK", sector="Other"))
    db.commit()
    import json as _json
    db.add(AgentCache(
        symbol="SUCC01.BK", agent="fundamental",
        result_json=_json.dumps({"target_price": 120.0}),
    ))
    db.commit()

    rows = asyncio.run(main.list_watchlist(db))

    assert len(rows) == 1
    assert rows[0]["upside_pct"] is None
    # One legacy quote call for the watchlist item's own unbound price
    # (main.py:1047); zero further calls for the refused parent lookup.
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 1


def test_non_owning_call_site_optimizer_scoring_refuses_converted_symbol(monkeypatch):
    """main.py:2038 and :2045 — inside POST /analyze/optimizer's nested
    _get_scores closure: a candidate's own price (2038) and, for a DR
    candidate, its parent's price (2045). Scoring context owns no portfolio
    holding identity and is not the WP3.4 propagation site.

    _get_scores is a closure, not independently importable, so it is
    exercised through the real endpoint function with a spy wrapped around
    the module-level fetch_price_info binding (the same binding _get_scores
    itself calls through) to attribute both calls individually. Everything
    downstream of scoring (timing enrichment, execution-penalty context,
    factor-engine DNA) is outside WP3.4's authorized surface and is allowed
    to fail past the point this evidence is captured — this test asserts
    only what Step 4.1 is scoped to prove. The final AI swap-synthesis stage
    (agents.optimizer.run_layered_optimizer) is explicitly stubbed out
    rather than merely left to fail: it is a real network call to a live LLM
    provider and must never fire inside a unit test regardless of what
    exception handling would otherwise contain it."""
    binding_a = _binding(asset_id=42, provider_symbol="SUCC")   # candidate's own price (2038)
    binding_b = _binding(asset_id=43, provider_symbol="AAPL")   # DR parent's price (2045)
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(
        fetcher, "_read_conversion_guard_projection",
        lambda: _two_binding_projection(binding_a, binding_b),
    )
    monkeypatch.setattr(main, "run_layered_optimizer", lambda *a, **k: {})

    calls: list[tuple[str, object]] = []
    real_fetch = main.fetch_price_info

    def _spy(symbol, binding=None):
        calls.append((symbol, binding))
        return real_fetch(symbol, binding)

    monkeypatch.setattr(main, "fetch_price_info", _spy)

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "SUCC")
    ws_id = main._ws_id(db)
    db.add(Watchlist(workspace_id=ws_id, symbol="AAPL01.BK", sector="Other"))
    db.commit()
    import json as _json
    now = datetime.utcnow()
    for sym in ("SUCC", "AAPL01.BK"):
        db.add(AgentCache(
            symbol=sym, agent="technical",
            result_json=_json.dumps({"ta_score": 50, "trend": "sideways"}),
            cached_at=now,
        ))
        db.add(AgentCache(
            symbol=sym, agent="fundamental",
            result_json=_json.dumps({"fa_score": 50}),
            cached_at=now,
        ))
    db.commit()

    body = main.OptimizerRequest(portfolio_id=portfolio.id)
    try:
        asyncio.run(main.analyze_optimizer(body, db))
    except Exception:
        pass  # downstream of _get_scores; outside WP3.4's authorized surface

    own_price_calls = [c for c in calls if c[0] == "SUCC"]
    parent_price_calls = [c for c in calls if c[0] == "AAPL"]  # normalize_dr_symbol("AAPL01.BK")

    assert own_price_calls, "expected a candidate-price call for the converted symbol"
    assert all(b is None for _, b in own_price_calls), "2038 must never receive a binding"
    assert parent_price_calls, "expected a DR-parent-price call for the converted parent symbol"
    assert all(b is None for _, b in parent_price_calls), "2045 must never receive a binding"
    # Both "SUCC" (2038) and "AAPL" (2045) are guard-bound and refused before
    # any provider call; the watchlist item's own unbound, unconverted price
    # ("AAPL01.BK" itself, a distinct symbol from its parent) is the only
    # legacy quote made in this scenario.
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 1


def test_non_owning_call_site_admin_validate_portfolio_refuses_converted_symbol(monkeypatch):
    """main.py:4712 — GET /admin/validate-portfolio/{id} is a read-only
    accounting-integrity diagnostic, not the authorized holdings-price
    serving path. A converted holding must fail closed and be excluded from
    live_equity rather than silently priced at zero or a stale value."""
    binding = _binding()
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "SUCC.BK")

    result = asyncio.run(main.admin_validate_portfolio(portfolio.id, db))

    assert result["checks"]["nav_reconciliation"]["status"] == "no_snapshot"
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0


def test_non_owning_call_site_snapshot_generation_refuses_converted_symbol(monkeypatch):
    """services/portfolio_snapshots.py:333 — generate_daily_snapshot is the
    scheduler/admin-driven snapshot engine, structurally outside main.py and
    never given a binding. With its sole holding converted and unbound, the
    live-price coverage check sees 0% coverage and aborts rather than
    silently substituting avg_cost — SnapshotCoverageError is the
    observable fail-closed outcome for this caller (distinct in shape from
    the quarantine dict other sites surface, but attributable to the same
    guard refusal: zero provider calls were ever made)."""
    binding = _binding()
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "SUCC.BK")
    ws_id = main._ws_id(db)

    with pytest.raises(SnapshotCoverageError):
        asyncio.run(portfolio_snapshots.generate_daily_snapshot(db, portfolio.id, ws_id))

    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0


def test_non_owning_call_site_idea_review_refuses_converted_symbol(monkeypatch):
    """services/idea_review.py:396 — the AI Committee Review's existing-
    portfolio market-value pass prices each current holding to compute
    weights for a user-submitted idea evaluation. It is not the holdings-
    price serving path and never receives a binding; the converted holding's
    contribution to portfolio value falls back to avg_cost (idea_review's
    own pre-existing except-clause fallback, not a WP3.4 concern), and the
    fail-closed guard was consulted with zero provider calls."""
    binding = _binding()
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "SUCC.BK", shares=10.0, avg_cost=50.0)
    ws_id = main._ws_id(db)

    result = idea_review_service.review_ideas(["PTT"], portfolio.id, db, ws_id)

    assert "reviews" in result
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0


def test_non_owning_call_site_factor_engine_refuses_converted_symbol(monkeypatch):
    """services/analytics/factor_engine.py:797 —
    compute_portfolio_factor_exposure prices each holding to compute
    portfolio weights for Portfolio DNA / style classification. It is not
    the holdings-price serving path and never receives a binding. Only the
    unrelated per-symbol fundamentals/momentum gathering (fetch_info /
    fetch_history — outside WP3.4's fetch_price_info scope) and the
    15-minute in-process result cache are stubbed out; the fetch_price_info
    call itself runs for real against the same fake provider/guard used
    everywhere else in this module."""
    binding = _binding()
    provider = _Provider(evidence=_evidence())
    monkeypatch.setattr(fetcher, "_provider", provider)
    monkeypatch.setattr(fetcher, "_read_conversion_guard_projection", lambda: _projection_for(binding))
    monkeypatch.setattr(factor_engine, "get_cached", lambda *a, **k: None)
    monkeypatch.setattr(factor_engine, "set_cached", lambda *a, **k: None)
    monkeypatch.setattr(factor_engine, "_gather_info", lambda symbol: {})
    monkeypatch.setattr(factor_engine, "_gather_momentum", lambda symbol: {
        "return_30d": None, "return_90d": None, "ma_alignment": None, "rsi_14": None,
    })

    db = make_session()
    portfolio = _add_portfolio(db)
    _add_item(db, portfolio, "SUCC.BK", shares=10.0, avg_cost=50.0)
    ws_id = main._ws_id(db)

    result = factor_engine.compute_portfolio_factor_exposure(db, portfolio.id, ws_id)

    assert result["per_stock_scores"][0]["symbol"] == "SUCC.BK"
    assert provider.evidence_calls == 0
    assert provider.quote_calls == 0
