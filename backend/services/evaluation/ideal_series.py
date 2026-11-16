"""ideal_series.py — AI Evaluation M6: friction-free Ideal Portfolio series.

Computes the "Ideal" line of the Three Portfolios comparison
(OPTIMIZER_PHILOSOPHY.md §4/§5; EXECUTION_INTELLIGENCE_UX.md §1.1): what
capital would have returned if every RecommendationSnapshot's target weights
had been followed instantly and exactly — zero fees, zero timing delay, zero
funding constraints.

This is deliberately NOT the ACTIVE_MODEL shadow. That object already exists
(services/decision_memory/shadow_tracker.py) and answers a related but
different question: what has a persisted, stateful, 100%-compliant paper
portfolio accumulated since ITS OWN inception (which may predate, or not
align with, whatever period window a caller asks for). Ideal is instead
recomputed fresh, per request, for the exact requested period — directly
from RecommendationSnapshot.projected_allocations_json and PortfolioSnapshot's
own daily holdings prices (DB-only, never yfinance) — so it is always
reproducible for any window and never depends on ACTIVE_MODEL's own
valuation cadence or historical gaps (Risk R6: the friction-free-return
methodology is defined exactly once, here).

Read-only: never writes to RecommendationSnapshot, ShadowPortfolio, or any
other upstream table (implementation plan §4.1) — produces a plain dict,
persists nothing.

Methodology (documented once — do not re-derive elsewhere, Risk R6):
    1. Find every RecommendationSnapshot for the portfolio with a parseable
       projected_allocations_json, ordered by created_at. The "seed"
       allocation is the latest snapshot at or before the period start (if
       any); every later snapshot inside the window is a rebalance point.
    2. Walk daily prices from PortfolioSnapshot.holdings_json — the same
       DB-only price source shadow_tracker.py's backfill path uses (reused
       via _snapshot_price_history / _price_near_date, never re-derived).
    3. At the seed date, convert target weights to share counts at that
       day's prices (reused _resolve_shares_from_weights, base NAV = 100
       since only relative weights matter). On every later rebalance date,
       value the OLD holdings at the new day's prices, add back the carried-
       forward cash, then instantly re-derive shares + cash for the NEW
       weights at that same NAV — a zero-cost, zero-delay rebalance (the
       same "running_nav" mechanic create_active_model_shadow uses, reused
       conceptually, computed independently here so the result is
       reproducible for any window).
    4. Index the resulting NAV series to 100 at the first date used.

Paper cash accounting (correctness fix, 2026-07-07)
----------------------------------------------------
Target weights intentionally sum to less than 100% (the optimizer's own
cash floor — OPTIMIZER_PHILOSOPHY.md §2 Priority 7, policy_engine.py's
min_cash_pct enforcement). _resolve_shares_from_weights now returns the
unallocated residual as explicit cash, which this replay carries forward
across every rebalance and adds back into the NAV basis of the next one
(cash itself earns zero return between rebalances). Previously the
residual was computed nowhere and stored nowhere — silently deleted from
NAV at every rebalance, compounding multiplicatively across a period's
rebalance history. See docs/DECISION_LOG.md, "Paper Portfolio Cash-Leak
Fix," for the full root-cause analysis and worked example. This fix does
not change Gap A's formula (compute_three_portfolios /
_revalue_ai_portfolio_with_canonical_prices, below, are untouched) — Gap
A's *computed value* changes only insofar as its correctly-fixed inputs
now conserve NAV instead of leaking it.

Status is "insufficient_data" (no snapshot exists at or before the window's
end) or "no_price_history" (no PortfolioSnapshot holdings_json rows at all)
— never a fabricated flat line.

Gap A price-source unification (correctness fix, 2026-07-06)
--------------------------------------------------------------
Gap A (Ideal − AI) must isolate execution friction, not an artifact of two
hypothetical constructs being valued from two different price feeds. Ideal
values holdings from this module's own canonical `_snapshot_price_history`
walk (PortfolioSnapshot.holdings_json daily-close prices). The ACTIVE_MODEL
shadow's persisted ShadowPortfolioSnapshot rows, by contrast, are valued via
shadow_tracker.value_shadow_portfolio's live AgentCache-cache price reads —
a different, independently-sourced observation for the same calendar date,
whose day-over-day noise compounds through TWR chaining. `compute_three_
portfolios` therefore never reads compute_portfolio_attribution's
`ai_model_shadow.return_pct` for Gap A — it revalues the shadow's own
persisted holdings-per-date (`_revalue_ai_portfolio_with_canonical_prices`,
below) through this module's identical canonical price archive first. The
shadow's rebalance *events* (which weights, on which dates) are read as-is
and never altered — only the price used to value them changes. See that
function's docstring for the full analysis.

Rebalance-event-sequence alignment (verified, not a bug)
----------------------------------------------------------
Ideal's rebalance points and the ACTIVE_MODEL shadow's rebalance points are
driven by the identical trigger: main.py's optimizer-run endpoint writes one
RecommendationSnapshot and then calls create_active_model_shadow with that
same snapshot id in the same request (see main.py's analyze_optimizer
handler). The daily scheduler only calls value_all_active_shadows
(valuation, not rebalancing) — it never rebalances ACTIVE_MODEL outside an
optimizer run. So both objects replay the same RecommendationSnapshot
sequence by construction. The one legitimate divergence is that
ACTIVE_MODEL only replays from its own immutable inception_date forward
(Phase 4C.6) while Ideal replays from period_start — expected and already
surfaced via `ai_portfolio.status` / per-row None values in `chart`, not a
correctness defect.

Public API
----------
compute_ideal_series(db, portfolio_id, period_days=90) -> dict
compute_three_portfolios(db, portfolio_id, period_days=90) -> dict
    Aligns Ideal / AI (ACTIVE_MODEL shadow) / Actual / Benchmark onto one
    date axis (indexed to 100) and computes Gap A (Ideal − AI) / Gap B
    (AI − Actual). Both gaps are derived from this function's own aligned
    ideal_return/ai_return/actual_return — the same figures rendered as the
    Ideal/AI Portfolio/You headline numbers — never reconstructed from
    attribution_engine's regret_score or waterfall effects (DOGFOOD-03 fix,
    2026-09-14; see compute_three_portfolios's own docstring and
    DECISION_LOG.md).
"""
from __future__ import annotations

import json
import logging
import math
from datetime import date, timedelta
from typing import Any

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def _snapshots_for_window(
    db: Session, portfolio_id: int, period_start: str, period_end: str,
) -> tuple[tuple[str, list[dict]] | None, list[tuple[str, list[dict]]]]:
    """Return (seed, rebalances): seed is the latest snapshot at/before
    period_start (or None); rebalances are later snapshots inside the window,
    each (date, target_allocations), ordered ascending.
    """
    from models.database import RecommendationSnapshot

    rows = (
        db.query(RecommendationSnapshot)
        .filter(
            RecommendationSnapshot.portfolio_id == portfolio_id,
            RecommendationSnapshot.projected_allocations_json.isnot(None),
        )
        .order_by(RecommendationSnapshot.created_at.asc())
        .all()
    )

    parsed: list[tuple[str, list[dict]]] = []
    for r in rows:
        if not r.created_at:
            continue
        try:
            allocs = json.loads(r.projected_allocations_json)
        except Exception:
            continue
        if not allocs:
            continue
        parsed.append((r.created_at.date().isoformat(), allocs))

    seed: tuple[str, list[dict]] | None = None
    rebalances: list[tuple[str, list[dict]]] = []
    for d, allocs in parsed:
        if d <= period_start:
            seed = (d, allocs)  # keep the latest one at/before period_start
        elif d <= period_end:
            rebalances.append((d, allocs))
    return seed, rebalances


def _empty_result(status: str, reason: str, period_start: str, period_end: str) -> dict[str, Any]:
    return {
        "status": status,
        "reason": reason,
        "period_start": period_start,
        "period_end": period_end,
        "series": [],
        "series_start": None,
        "return_pct": None,
        "max_drawdown_pct": None,
        "annualized_volatility": None,
        "rebalance_dates": [],
        "snapshots_used": 0,
    }


def compute_ideal_series(db: Session, portfolio_id: int, period_days: int = 90) -> dict[str, Any]:
    """The friction-free Ideal Portfolio trajectory over the last `period_days`."""
    from services.decision_memory.shadow_tracker import (
        _snapshot_price_history,
        _price_near_date,
        _resolve_shares_from_weights,
        _compute_paper_value,
        assert_nav_conserved,
    )
    from services.analytics.attribution_engine import compute_max_drawdown, _compute_daily_volatility

    period_end = date.today().isoformat()
    period_start = (date.today() - timedelta(days=period_days)).isoformat()

    seed, rebalances = _snapshots_for_window(db, portfolio_id, period_start, period_end)
    if seed is None and not rebalances:
        return _empty_result(
            "insufficient_data", "no_recommendation_snapshot_at_or_before_period",
            period_start, period_end,
        )

    history = _snapshot_price_history(db)
    if not history:
        return _empty_result("no_price_history", "no_portfolio_snapshot_prices_available", period_start, period_end)

    if seed is not None:
        start_date, start_allocs = seed
    else:
        start_date, start_allocs = rebalances[0]
        rebalances = rebalances[1:]

    dates = sorted(d for d in history if start_date <= d <= period_end)
    if not dates:
        return _empty_result(
            "no_price_history", "no_price_dates_on_or_after_first_recommendation",
            period_start, period_end,
        )

    rebalance_map = {d: allocs for d, allocs in rebalances}

    seed_symbols = [a.get("symbol") for a in start_allocs if a.get("symbol")]
    seed_prices = {
        sym: p for sym in seed_symbols
        if (p := _price_near_date(history, start_date, sym))
    }

    # Bootstrap NAV = 100 — only relative weights matter, indexing is trivial.
    # Target weights summing to <100% are the optimizer's intentional cash
    # floor (OPTIMIZER_PHILOSOPHY.md §2 Priority 7) — the residual is carried
    # forward as explicit paper cash, never dropped (docs/DECISION_LOG.md,
    # "Paper Portfolio Cash-Leak Fix").
    holdings, cash = _resolve_shares_from_weights(start_allocs, 100.0, seed_prices)
    deployed_value, _ = _compute_paper_value(holdings, seed_prices)
    assert_nav_conserved(
        label=f"compute_ideal_series seed portfolio_id={portfolio_id} date={start_date}",
        expected_nav=100.0, equity=deployed_value, cash=cash,
    )

    series: list[dict[str, Any]] = []
    values: list[float] = []
    daily_returns: list[float] = []
    last_prices: dict[str, float] = dict(seed_prices)

    for d in dates:
        last_prices.update(history.get(d, {}))

        if d in rebalance_map and d != start_date:
            equity_before, _ = _compute_paper_value(holdings, last_prices)
            nav = equity_before + cash  # carry forward cash, never reset to 0
            if nav <= 0:
                nav = values[-1] if values else 100.0
            new_symbols = [a.get("symbol") for a in rebalance_map[d] if a.get("symbol")]
            for s in new_symbols:
                if s not in last_prices:
                    p = _price_near_date(history, d, s)
                    if p:
                        last_prices[s] = p
            holdings, cash = _resolve_shares_from_weights(rebalance_map[d], nav, last_prices)
            deployed_value, _ = _compute_paper_value(holdings, last_prices)
            assert_nav_conserved(
                label=f"compute_ideal_series rebalance portfolio_id={portfolio_id} date={d}",
                expected_nav=nav, equity=deployed_value, cash=cash,
            )

        total, _ = _compute_paper_value(holdings, last_prices)
        total += cash  # cash earns zero return; carried forward flat between rebalances
        if total <= 0:
            total = values[-1] if values else 100.0

        if values and values[-1] > 0:
            daily_returns.append((total - values[-1]) / values[-1] * 100)
        values.append(total)
        series.append({"date": d, "value": total})

    base = values[0]
    indexed_series = [
        {"date": row["date"], "index": round(row["value"] / base * 100, 4) if base else None}
        for row in series
    ]

    return_pct = round((values[-1] - base) / base * 100, 4) if base else None
    max_dd = compute_max_drawdown(values)
    vol = _compute_daily_volatility(daily_returns)

    return {
        "status": "ok",
        "reason": None,
        "period_start": period_start,
        "period_end": period_end,
        "series": indexed_series,
        "series_start": start_date,
        "return_pct": return_pct,
        "max_drawdown_pct": max_dd,
        "annualized_volatility": vol,
        "rebalance_dates": sorted(rebalance_map.keys()),
        "snapshots_used": 1 + len(rebalance_map),
    }


def _reindex_to_100(
    dated_values: dict[str, float], axis: list[str], rebase: bool = True,
) -> tuple[list[float | None], str | None]:
    """Forward-fill *dated_values* onto *axis*.

    rebase=True (default, ideal/ai/benchmark): re-index to 100 at the first
    axis date with an observation — correct for series that are already
    self-normalized to exactly 100 at their own start (compute_ideal_series,
    _revalue_ai_portfolio_with_canonical_prices), where this is a no-op.

    rebase=False (actual): forward-fill only, values passed through as-is.
    compute_actual_indexed_series's TWR chain is already absolute-scaled
    (its own first value need not be exactly 100 — e.g. it may already
    carry a return earned before the shared axis's first date coincides
    with it); rebasing a second time here would renormalize that value
    back to 100 and silently erase the return it represents (Accounting
    Correctness C5, Issue B).

    Returns (values, base_date); base_date is None when dated_values has no
    observation anywhere on/before the axis, and is unused when rebase=False.
    """
    if not dated_values or not axis:
        return [None] * len(axis), None

    sorted_items = sorted(dated_values.items())
    out: list[float | None] = []
    base_value: float | None = None
    base_date: str | None = None
    last: float | None = None
    idx = 0
    n = len(sorted_items)

    for d in axis:
        while idx < n and sorted_items[idx][0] <= d:
            last = sorted_items[idx][1]
            idx += 1
        if last is None:
            out.append(None)
            continue
        if not rebase:
            out.append(round(last, 4))
            continue
        if base_value is None:
            base_value = last
            base_date = d
        out.append(round(last / base_value * 100, 4) if base_value else None)
    return out, base_date


# Persisted holdings_json market_value is round(shares * price, 2) (see
# shadow_tracker._compute_paper_value), so each holding contributes at most
# 0.005 of rounding between the row's total_value and its holdings' sum.
_MARKET_VALUE_ROUNDING_TOLERANCE = 0.01


def _derive_snapshot_cash(holdings: list[dict], stored_total_value: Any) -> tuple[float | None, str | None]:
    """Recover one ShadowPortfolioSnapshot row's own paper cash.

    Every ACTIVE_MODEL row writer persists one consistent state:
    value_shadow_portfolio writes total_value = Σ shares × price +
    paper_cash_balance (as of that day) with the enriched holdings it priced,
    and _replay_active_model_series / regenerate_active_model_shadow write
    total_value = equity_today + cash with that date's enriched holdings
    (Accounting Correctness C5, Issue A). So, on the row's own valuation
    basis:

        cash_t = total_value_t − Σ holdings_json[].market_value_t

    The persisted price source (live AgentCache or replay) cancels out here;
    only cash remains. Returns (cash, None), or (None, reason) when this row
    does not let that cash be recovered reliably. Callers must treat that as
    missing data and never substitute another cash figure (in particular
    ShadowPortfolio.paper_cash_balance, which is today's cash, overwritten
    at every rebalance).
    """
    try:
        total = float(stored_total_value)
    except (TypeError, ValueError):
        return None, "invalid_stored_total_value"
    if not math.isfinite(total) or total <= 0:
        return None, "invalid_stored_total_value"

    equity = 0.0
    priced = 0
    for h in holdings:
        if not isinstance(h, dict):
            return None, "invalid_holding_entry"
        try:
            shares = float(h.get("shares") or 0)
        except (TypeError, ValueError):
            return None, "invalid_shares"
        if not math.isfinite(shares):
            return None, "invalid_shares"
        if shares <= 0:
            continue  # persisted as market_value 0.0 ("zero_shares")
        mv_raw = h.get("market_value")
        if mv_raw is None:
            # Either a legacy row written without enriched valuation fields,
            # or a holding the writer could not price (price_source
            # "missing"), which includes every NAV-floor-fallback row,
            # where total_value is a carried-forward NAV, not cash + equity.
            return None, "missing_market_value"
        try:
            mv = float(mv_raw)
        except (TypeError, ValueError):
            return None, "invalid_market_value"
        if not math.isfinite(mv) or mv < 0:
            return None, "invalid_market_value"
        price = h.get("current_price")
        if price is not None:
            try:
                price_f = float(price)
            except (TypeError, ValueError):
                return None, "invalid_market_value"
            # Same valuation basis: market_value must be shares × the
            # price the writer recorded alongside it.
            if abs(shares * price_f - mv) > _MARKET_VALUE_ROUNDING_TOLERANCE + 1e-9 * abs(mv):
                return None, "market_value_mismatch"
        equity += mv
        priced += 1

    cash = total - equity
    # Paper cash is never negative by construction (_resolve_shares_from_weights
    # returns max(0, residual) and scales over-100% weights down), so a
    # negative residual beyond rounding means total_value and holdings_json
    # do not describe the same state. Reject it; never clamp it to 0.
    if cash < -_MARKET_VALUE_ROUNDING_TOLERANCE * (priced + 1):
        return None, "negative_derived_cash"
    return cash, None


def _revalue_ai_portfolio_with_canonical_prices(
    db: Session,
    portfolio_id: int,
    history: dict[str, dict[str, float]],
    period_start: str,
    period_end: str,
) -> dict[str, Any]:
    """Re-derive the ACTIVE_MODEL shadow's NAV series from the identical
    canonical price archive (_snapshot_price_history — PortfolioSnapshot.
    holdings_json, the same source compute_ideal_series uses) instead of its
    persisted total_value/daily_return_pct.

    Root cause this exists to fix: ShadowPortfolioSnapshot rows are normally
    written by shadow_tracker.value_shadow_portfolio, which prices holdings
    via _fetch_cached_prices (AgentCache "technical" live cache, 15-min TTL,
    read at whatever moment the daily valuation job ran) — a different,
    independently-sourced price observation than the once-daily-close prices
    Ideal reads from PortfolioSnapshot.holdings_json. Both nominally trace
    back to yfinance, but at different times of day through different
    caches, so day-over-day deltas (TWR-chained into the persisted
    return_pct_since_inception) can diverge from what Ideal sees for the
    same calendar date — and that divergence compounds daily. This function
    does NOT change what the shadow held or when it rebalanced (its
    persisted holdings_json per date is read as-is, untouched) — only which
    price values those same holdings, so Gap A compares Ideal and AI
    Portfolio at one shared set of price observations.

    This is deliberately scoped to the Three Portfolios / Gap A view only.
    It does not change compute_portfolio_attribution's own ai_model_shadow
    figure, which remains the correct "what has our persisted paper account
    actually returned using its live valuation policy" answer used elsewhere
    (Scorecard, S4, S5, the attribution waterfall) — a legitimately
    different question from "controlling for identical market data, how
    much of the Ideal-vs-AI gap is friction."

    Per-date cash (Historical Shadow Cash Integrity, Phase 4.19): each row
    is valued as canonical equity of its own holdings + that row's OWN cash
    (_derive_snapshot_cash), never ShadowPortfolio.paper_cash_balance.
    That column holds today's cash and is overwritten in place at every
    ACTIVE_MODEL rebalance, so adding it to every historical date shifted
    each row by (cash_now − cash_t). The curve then jumped at every
    rebalance that changed the cash weight, inflating return, drawdown,
    volatility and both gaps. A row whose cash cannot be recovered reliably
    (legacy/unenriched holdings, unpriced holdings, NAV-floor fallback,
    inconsistent total vs holdings) or whose holdings cannot be fully
    canonically valued is excluded and logged. It is never filled with a
    substitute value. The surrounding valid rows still define the series, and
    status is "incomplete_snapshot_data" only when no row survives.
    """
    from models.database import ShadowPortfolio, ShadowPortfolioSnapshot
    from services.decision_memory.shadow_tracker import _price_near_date, _compute_paper_value
    from services.analytics.attribution_engine import compute_max_drawdown, _compute_daily_volatility

    shadow = (
        db.query(ShadowPortfolio)
        .filter_by(portfolio_id=portfolio_id, shadow_type="ACTIVE_MODEL", is_active=True)
        .order_by(ShadowPortfolio.created_at.desc())
        .first()
    )
    if not shadow:
        return {"status": "unavailable", "return_pct": None, "max_drawdown_pct": None,
                "annualized_volatility": None, "series": []}

    snaps = (
        db.query(ShadowPortfolioSnapshot)
        .filter(
            ShadowPortfolioSnapshot.shadow_portfolio_id == shadow.id,
            ShadowPortfolioSnapshot.snapshot_date >= period_start,
            ShadowPortfolioSnapshot.snapshot_date <= period_end,
        )
        .order_by(ShadowPortfolioSnapshot.snapshot_date.asc())
        .all()
    )
    if not snaps:
        return {"status": "no_snapshots_in_window", "return_pct": None, "max_drawdown_pct": None,
                "annualized_volatility": None, "series": []}

    series: list[dict[str, Any]] = []
    values: list[float] = []
    daily_returns: list[float] = []
    excluded: list[dict[str, str]] = []

    for snap in snaps:
        if not snap.holdings_json:
            # Pre-fix rows with no holdings record cannot be revalued at all.
            excluded.append({"date": snap.snapshot_date, "reason": "missing_holdings_json"})
            continue
        try:
            holdings = json.loads(snap.holdings_json)
        except Exception:
            excluded.append({"date": snap.snapshot_date, "reason": "invalid_holdings_json"})
            continue
        if not isinstance(holdings, list):
            excluded.append({"date": snap.snapshot_date, "reason": "invalid_holdings_json"})
            continue

        cash, reason = _derive_snapshot_cash(holdings, snap.total_value)
        if reason is not None:
            excluded.append({"date": snap.snapshot_date, "reason": reason})
            continue

        symbols = [h.get("symbol") for h in holdings if h.get("symbol")]
        canonical_prices = {
            sym: p for sym in symbols
            if (p := _price_near_date(history, snap.snapshot_date, sym))
        }
        equity, enriched = _compute_paper_value(holdings, canonical_prices)
        if any(e.get("price_source") == "missing" for e in enriched):
            # Dropping a held position from NAV would fabricate a loss.
            excluded.append({"date": snap.snapshot_date, "reason": "canonical_price_unavailable"})
            continue
        total = equity + cash
        if total <= 0:
            excluded.append({"date": snap.snapshot_date, "reason": "non_positive_nav"})
            continue
        if values and values[-1] > 0:
            daily_returns.append((total - values[-1]) / values[-1] * 100)
        values.append(total)
        series.append({"date": snap.snapshot_date, "value": total})

    if excluded:
        logger.warning(
            "[IDEAL_SERIES] AI Portfolio revaluation excluded %d of %d ACTIVE_MODEL "
            "snapshot rows (shadow_id=%s) whose historical cash/valuation could not be "
            "recovered reliably: %s",
            len(excluded), len(snaps), shadow.id, excluded[:10],
        )

    if not values:
        has_holdings_rows = any(
            e["reason"] not in ("missing_holdings_json", "invalid_holdings_json") for e in excluded
        )
        return {"status": "incomplete_snapshot_data" if has_holdings_rows else "no_price_history",
                "return_pct": None, "max_drawdown_pct": None,
                "annualized_volatility": None, "series": [], "excluded_rows": excluded}

    base = values[0]
    indexed_series = [
        {"date": row["date"], "index": round(row["value"] / base * 100, 4) if base else None}
        for row in series
    ]
    return_pct = round((values[-1] - base) / base * 100, 4) if base else None

    return {
        "status": "ok",
        "return_pct": return_pct,
        "max_drawdown_pct": compute_max_drawdown(values),
        "annualized_volatility": _compute_daily_volatility(daily_returns),
        "series": indexed_series,
        "excluded_rows": excluded,
    }


def _return_over_window(
    series: list[dict], start_date: str, end_date: str | None = None,
) -> tuple[float | None, float | None, float | None]:
    """(return_pct, max_drawdown_pct, annualized_volatility) for a
    [{date, index}] series restricted to [start_date, end_date] (end_date
    None = the series' own last observation) — used to align Ideal and AI
    Portfolio to a common comparison window (see compute_three_portfolios
    docstring, "Shared comparison window")."""
    from services.analytics.attribution_engine import compute_max_drawdown, _compute_daily_volatility

    obs = [row for row in series if row.get("date") and row.get("index") is not None]
    # Base observation: the latest valuation on/before start_date, else the
    # first one after it (mirrors _price_near_date). The tail is
    # every observation strictly AFTER the base — re-appending the base
    # itself (as before Phase 4.21, whenever start_date was an observation)
    # injected a fabricated 0% first interval into the volatility.
    before = [row for row in obs if row["date"] <= start_date]
    base_row = before[-1] if before else (obs[0] if obs else None)
    base = base_row["index"] if base_row else None
    tail = [
        row["index"] for row in obs
        if base_row is not None and row["date"] > base_row["date"]
        and (end_date is None or row["date"] <= end_date)
    ]
    if base is None or not base or not tail:
        return None, None, None

    values = [base] + tail
    daily_returns = []
    prev = values[0]
    for v in values[1:]:
        if prev:
            daily_returns.append((v - prev) / prev * 100)
        prev = v

    return_pct = round((values[-1] - base) / base * 100, 4)
    return return_pct, compute_max_drawdown(values), _compute_daily_volatility(daily_returns)


def _valuation_dates(series: list[dict]) -> set[str]:
    """Dates carrying a usable point-in-time valuation in a [{date, index}]
    series (Ideal, AI canonical) — every one can open or close a window."""
    return {row["date"] for row in series if row.get("date") and row.get("index") is not None}


def _owner_window_dates(snaps: list[Any]) -> tuple[set[str], set[str]]:
    """(start-capable, end-capable) dates for the owner portfolio.

    Owner rows carry a valuation (total_value) AND a return since the
    PREVIOUS row (investment_return_pct), so the two roles differ. Any row
    with a positive NAV is a valid starting valuation: returns of later rows
    are measured from it. Only a row that carries its own return can close
    a window — ending on a row whose return is missing would silently treat
    that last interval as flat. When no row in the window has an adjusted
    return at all (legacy pre-Phase-3B.8 history), the existing raw-NAV
    fallback of _actual_portfolio_metrics applies and every valid-NAV row
    is also end-capable.
    """
    valid = [s for s in snaps if s.total_value and s.total_value > 0]
    starts = {s.snapshot_date for s in valid}
    if any(s.investment_return_pct is not None for s in valid):
        ends = {s.snapshot_date for s in valid if s.investment_return_pct is not None}
    else:
        ends = set(starts)
    return starts, ends


def _shared_comparison_window(participants: dict[str, tuple[set[str], set[str]]]) -> dict[str, Any]:
    """One comparison interval shared by every participating series.

    participants: name -> (start-capable dates, end-capable dates). A series
    with no start-capable date does not participate (it has no data in the
    window; its own status already says so). start is the earliest date on
    which EVERY participant has a starting valuation; end is the latest date
    after start on which every participant can close. Both bounds are real
    observations of each series — never a forward-filled value — so no
    series is credited with a flat, fabricated interval at either edge.
    """
    present = {k: v for k, v in participants.items() if v[0]}
    names = sorted(present)
    if len(present) < 2:
        return {"status": "not_applicable", "start": None, "end": None, "series": names}
    starts = set.intersection(*(v[0] for v in present.values()))
    ends = set.intersection(*(v[1] for v in present.values()))
    start = min(starts) if starts else None
    later_ends = [d for d in ends if start is not None and d > start]
    if start is None or not later_ends:
        return {"status": "insufficient_overlap", "start": None, "end": None, "series": names}
    return {"status": "aligned", "start": start, "end": max(later_ends), "series": names}


def _owner_window_metrics(
    snaps: list[Any], start: str, end: str,
) -> tuple[float | None, float | None, float | None]:
    """(return_pct, max_drawdown_pct, annualized_volatility) for the owner
    over [start, end], using the unchanged production formulas
    (_actual_portfolio_metrics: flow-adjusted TWR, return-index drawdown,
    daily volatility; raw-NAV fallback only for legacy rows).

    The start row is the opening valuation: its own return covers the
    interval BEFORE start (previous row -> start), so it is masked out.
    Persisted rows are never modified — the mask is a read-only view.
    """
    from types import SimpleNamespace
    from services.analytics.attribution_engine import _actual_portfolio_metrics, _safe_return

    rows = [
        SimpleNamespace(
            snapshot_date=s.snapshot_date,
            total_value=s.total_value,
            investment_return_pct=None if s.snapshot_date == start else s.investment_return_pct,
            daily_return_pct=None if s.snapshot_date == start else s.daily_return_pct,
        )
        for s in snaps
        if start <= s.snapshot_date <= end
    ]
    ret, dd, vol = _actual_portfolio_metrics(rows)
    return _safe_return(ret), dd, vol


def _owner_window_chart_points(snaps: list[Any], start: str, end: str) -> dict[str, float]:
    """Owner index over [start, end], 100 at the start valuation — the same
    observations _owner_window_metrics chains, so the last point equals
    100 + actual.return_pct.

    Flow-adjusted rows: the start row's own return is excluded (it covers
    the interval before start), and each later row with a return adds one
    point. A row without a return gets no point: it is not carried forward
    or bridged. Legacy windows with no adjusted return at all use the raw-NAV
    fallback, start and end only, as the headline and the previous chart did.
    """
    rows = [s for s in snaps if start <= s.snapshot_date <= end and s.total_value and s.total_value > 0]
    if not rows or rows[0].snapshot_date != start:
        return {}
    later = rows[1:]
    if any(s.investment_return_pct is not None for s in later):
        running = 100.0
        points = {start: 100.0}
        for s in later:
            if s.investment_return_pct is None:
                continue
            running *= 1.0 + s.investment_return_pct / 100.0
            points[s.snapshot_date] = round(running, 4)
        return points
    last = rows[-1]
    if last.snapshot_date != end:
        return {start: 100.0}
    return {start: 100.0, end: round(last.total_value / rows[0].total_value * 100, 4)}


def _window_chart(
    start: str,
    end: str,
    ideal_dated: dict[str, float],
    ai_dated: dict[str, float],
    actual_points: dict[str, float],
    bench_dated: dict[str, float],
) -> list[dict[str, Any]]:
    """Chart rows for the shared comparison window [start, end] (Phase 4.21).

    - Only observations inside [start, end]; the axis is the union of their
      dates.
    - Ideal / AI / You are all 100 at the shared start valuation, so each
      line's last point equals 100 + its headline return_pct.
    - The benchmark (display only, not part of any metric) is rebased to 100
      at its own first observation inside the window, as before.
    - A series without an observation on an axis date gets None there. Values
      are never carried forward, and no zero-return day is invented.
    """
    def _rebased(dated: dict[str, float], anchor: str | None) -> dict[str, float]:
        inside = {d: v for d, v in dated.items() if start <= d <= end and v is not None}
        if not inside:
            return {}
        base_date = anchor if anchor is not None else min(inside)
        base = inside.get(base_date)
        if not base:
            return {}
        return {d: round(v / base * 100, 4) for d, v in inside.items()}

    lines = {
        "ideal": _rebased(ideal_dated, start),
        "ai": _rebased(ai_dated, start),
        "actual": actual_points,
        "benchmark": _rebased(bench_dated, None),
    }
    axis = sorted(set().union(*(set(v) for v in lines.values())))
    return [{"date": d, **{k: v.get(d) for k, v in lines.items()}} for d in axis]


def compute_three_portfolios(db: Session, portfolio_id: int, period_days: int = 90) -> dict[str, Any]:
    """Ideal / AI (ACTIVE_MODEL) / Actual / Benchmark, aligned + Gap A/B (UX S7).

    DOGFOOD-03 correctness fix (2026-09-14): Gap B (AI − Actual) is now
    computed from this function's OWN already-aligned ai_return/actual_return
    — the identical two numbers rendered as the "AI Portfolio"/"You" headline
    figures on the same Three Portfolios screen. It previously read
    attribution_engine's `regret_score`, which is AI-model-return-minus-
    actual but sources "AI" from compute_portfolio_attribution's
    `ai_model_shadow.return_pct` — a different, undisplayed figure valued via
    live AgentCache prices over the full (untruncated) evaluation window, not
    the canonical-priced, overlap-truncated `ai_return` shown as "AI
    Portfolio" on this same screen (see "Gap A Correctness Patch" below —
    that patch deliberately re-sourced Gap A's AI figure but left Gap B
    reading the old one, on the reasoning that Actual-vs-official-valuation
    is a legitimate real-world comparison in isolation). It did not account
    for this screen's own "The Two Gaps" caption ("What explains the
    difference between the three portfolios") asserting that Gap A and Gap B
    reconcile with the three headline numbers directly above it — which,
    for Gap B, was false whenever the two AI figures diverged (confirmed on
    live portfolio 4: displayed AI Portfolio +3.52%, You +4.66%, implying
    Gap B ≈ -1.14%, while the old formula reported +2.49% — sourced from an
    undisplayed ai_model_shadow return of +7.15% for the same window). See
    docs/engineering/DECISION_LOG.md, "GAP B Semantic Fix (DOGFOOD-03)."
    compute_portfolio_attribution's own `regret_score` field is untouched and
    remains correct for its existing consumers (Scorecard, Trust Report,
    verdict_composer.compose_scorecard_verdict) — this fix is scoped to
    `three_portfolios.gap_b` only.

    Gap A (Ideal − AI) is different: both sides are hypothetical, friction-
    free constructs, so a fair comparison requires valuing them from the
    SAME price observations. ai_return here is therefore sourced from
    _revalue_ai_portfolio_with_canonical_prices (see its docstring for the
    price-source root cause), not from compute_portfolio_attribution's
    ai_model_shadow. The aligned chart's "ai" line uses this same canonical
    series for consistency with the Gap A number shown alongside it.

    Event-sequence alignment: Ideal replays every RecommendationSnapshot
    from period_start forward. The ACTIVE_MODEL shadow replays the same
    snapshots (both are driven by the same optimizer-run trigger — see
    module docstring), but only from its own immutable inception_date
    forward, which can postdate period_start by a wide margin (e.g. after
    an admin reset-inception, Phase 4C.6). Comparing a full period_days
    Ideal return against a much-shorter AI Portfolio return would silently
    conflate "different time horizons" with "friction cost." Both sides are
    therefore truncated to their overlap before return_pct/max_drawdown_pct/
    annualized_volatility are computed.

    Shared comparison window (Phase 4.21, window alignment): the overlap
    above previously bounded only Ideal and AI, and only at the START.
    "You" was measured over the full period_days cutoff window, and no
    series was bounded at the END. That broke two things:
      - Ideal/AI observations are point-in-time valuations, but an owner row
        carries the return since the PREVIOUS row. So the first in-window
        owner return (previous row -> first row) covered an interval before
        the Ideal/AI base valuation, and "You" chained one more interval
        than AI or Ideal.
      - The AI shadow is valued later in the day than owner snapshots exist,
        so its series could run days past Ideal/You.
    Gap A, Gap B and the Scorecard's Implementation Shortfall (which reads
    gap_a) then compared unequal intervals. Now all three series share ONE
    window (_shared_comparison_window). It starts at the earliest date where
    every participating series has a real valuation and ends at the latest
    later date where every one can close (an owner close requires that row's
    own return). For "You", the start row's return is masked out
    (_owner_window_metrics); its formulas, cash-flow adjustment and
    drawdown index are otherwise unchanged. Nothing is forward-filled at
    either edge. With no shared interval, gaps are None and each headline
    keeps its own-window figure. The interval is exposed as
    comparison_window.

    Chart rows follow the same window (_window_chart). When aligned, they hold
    only observations inside [start, end]. Ideal / AI / You are indexed to
    100 at the shared start valuation, so each line ends at 100 + its
    headline return. A missing observation is None, never carried forward.
    insufficient_overlap draws no chart, since there is no valid comparison;
    not_applicable keeps the previous single-series display.
    compute_portfolio_attribution (Scorecard outcome lens, regret_score) is
    untouched.
    """
    from models.database import BenchmarkPrice
    from services.analytics.attribution_engine import (
        compute_portfolio_attribution, compute_actual_indexed_series, _get_actual_snapshots,
    )
    from services.decision_memory.shadow_tracker import _snapshot_price_history

    cutoff = (date.today() - timedelta(days=period_days)).isoformat()
    today = date.today().isoformat()

    ideal = compute_ideal_series(db, portfolio_id, period_days)
    attribution = compute_portfolio_attribution(db, portfolio_id, period_days)

    actual = attribution.get("actual") or {}

    history = _snapshot_price_history(db)
    ai_canonical = _revalue_ai_portfolio_with_canonical_prices(
        db, portfolio_id, history, ideal["period_start"], ideal["period_end"],
    )

    # ── Shared comparison window (Phase 4.21) ─────────────────────────────
    # (see "Shared comparison window" in the docstring above)
    ideal_series_list = ideal.get("series") or []
    ai_series_list = ai_canonical.get("series") or []
    owner_snaps = _get_actual_snapshots(db, portfolio_id, cutoff)

    ideal_dates = _valuation_dates(ideal_series_list)
    ai_dates = _valuation_dates(ai_series_list)
    window = _shared_comparison_window({
        "ideal": (ideal_dates, ideal_dates),
        "ai": (ai_dates, ai_dates),
        "actual": _owner_window_dates(owner_snaps),
    })

    if window["status"] == "aligned":
        w_start, w_end = window["start"], window["end"]
        none3 = (None, None, None)
        ideal_return, ideal_max_dd, ideal_vol = (
            _return_over_window(ideal_series_list, w_start, w_end) if "ideal" in window["series"] else none3
        )
        ai_return, ai_max_dd, ai_vol = (
            _return_over_window(ai_series_list, w_start, w_end) if "ai" in window["series"] else none3
        )
        actual_return, actual_max_dd, actual_vol = (
            _owner_window_metrics(owner_snaps, w_start, w_end) if "actual" in window["series"] else none3
        )
        gap_a = round(ideal_return - ai_return, 4) if ideal_return is not None and ai_return is not None else None
        # DOGFOOD-03 fix: reuse this function's own aligned ai_return/actual_return
        # (the exact figures rendered as "AI Portfolio"/"You" on this screen) —
        # never attribution's regret_score, which sources "AI" from a different,
        # undisplayed, live-priced valuation. See docstring above and DECISION_LOG.
        gap_b = round(ai_return - actual_return, 4) if ai_return is not None and actual_return is not None else None
    else:
        # Nothing to compare (fewer than two series have data) or no shared
        # interval: each headline keeps its own-window figure, and no gap is
        # computed — a gap across mismatched intervals is not a comparison.
        ideal_return = ideal.get("return_pct")
        ideal_max_dd = ideal.get("max_drawdown_pct")
        ideal_vol = ideal.get("annualized_volatility")
        ai_return = ai_canonical.get("return_pct")
        ai_max_dd = ai_canonical.get("max_drawdown_pct")
        ai_vol = ai_canonical.get("annualized_volatility")
        actual_return = actual.get("return_pct")
        actual_max_dd = actual.get("max_drawdown_pct")
        actual_vol = actual.get("annualized_volatility")
        gap_a = gap_b = None

    # ── Aligned chart series (display only) ───────────────────────────────
    # Issue B (Accounting Correctness C5): "actual" must be the same
    # cash-flow-adjusted TWR series the summary card's actual.return_pct
    # already uses (attribution.actual, via _actual_portfolio_metrics) —
    # never a raw total_value ratio, which double-counts deposits/
    # withdrawals as investment return. See compute_actual_indexed_series.
    actual_dated = compute_actual_indexed_series(db, portfolio_id, cutoff)

    ai_dated = {
        row["date"]: row["index"] for row in ai_canonical.get("series", []) if row.get("index") is not None
    }

    bench_rows = (
        db.query(BenchmarkPrice.price_date, BenchmarkPrice.close_price)
        .filter(BenchmarkPrice.symbol == "^SET.BK", BenchmarkPrice.price_date >= cutoff)
        .all()
    )
    bench_dated = {d: v for d, v in bench_rows}

    ideal_dated = {row["date"]: row["index"] for row in ideal.get("series", []) if row.get("index") is not None}

    if window["status"] == "aligned":
        # Phase 4.21: the chart covers exactly the interval the headline
        # figures and both gaps were measured over (see _window_chart).
        chart = _window_chart(
            window["start"], window["end"],
            ideal_dated if "ideal" in window["series"] else {},
            ai_dated if "ai" in window["series"] else {},
            _owner_window_chart_points(owner_snaps, window["start"], window["end"])
            if "actual" in window["series"] else {},
            bench_dated,
        )
    elif window["status"] == "insufficient_overlap":
        # Several series have data but share no interval: there is no valid
        # comparison to draw. Plotting each on its own base would read as one
        # (gaps are None for the same reason).
        chart = []
    else:
        # not_applicable (at most one series has data): unchanged display.
        axis = sorted(set(ideal_dated) | set(ai_dated) | set(actual_dated) | set(bench_dated))

        ideal_chart, _ = _reindex_to_100(ideal_dated, axis) if axis else ([], None)
        ai_chart, _ = _reindex_to_100(ai_dated, axis) if axis else ([], None)
        actual_chart, _ = _reindex_to_100(actual_dated, axis, rebase=False) if axis else ([], None)
        bench_chart, _ = _reindex_to_100(bench_dated, axis) if axis else ([], None)

        chart = [
            {
                "date": axis[i],
                "ideal": ideal_chart[i] if i < len(ideal_chart) else None,
                "ai": ai_chart[i] if i < len(ai_chart) else None,
                "actual": actual_chart[i] if i < len(actual_chart) else None,
                "benchmark": bench_chart[i] if i < len(bench_chart) else None,
            }
            for i in range(len(axis))
        ]

    # BenchmarkPrice is a global (not portfolio-scoped) table synced
    # independently of any portfolio's own activity — its presence alone must
    # never flip status to "ok" for a portfolio with no data of its own
    # (would otherwise silently show a cold-start portfolio as "ok").
    has_portfolio_data = bool(ideal_dated) or bool(ai_dated) or bool(actual_dated)
    status = "ok" if has_portfolio_data else "insufficient_data"

    from datetime import datetime as _datetime

    return {
        "portfolio_id": portfolio_id,
        "period_days": period_days,
        "status": status,
        "as_of": _datetime.utcnow().isoformat() + "Z",
        "chart": chart,
        "ideal": {
            "status": ideal.get("status"),
            "return_pct": ideal_return,
            "max_drawdown_pct": ideal_max_dd,
            "annualized_volatility": ideal_vol,
        },
        "ai_portfolio": {
            "status": ai_canonical.get("status"),
            "return_pct": ai_return,
            "max_drawdown_pct": ai_max_dd,
            "annualized_volatility": ai_vol,
        },
        "actual": {
            "status": attribution.get("status"),
            "return_pct": actual_return,
            "max_drawdown_pct": actual_max_dd,
            "annualized_volatility": actual_vol,
        },
        "gap_a": {"value": gap_a, "label": "Ideal − AI"},
        "gap_b": {"value": gap_b, "label": "AI − You"},
        # Additive (Phase 4.21): the interval every compared headline and
        # both gaps were measured over. status: aligned | insufficient_overlap
        # | not_applicable (fewer than two series have data).
        "comparison_window": {
            "status": window["status"],
            "start": window["start"],
            "end": window["end"],
            "series": window["series"],
        },
    }
