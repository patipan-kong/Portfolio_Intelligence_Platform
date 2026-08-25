import assert from "node:assert/strict";
import { test } from "node:test";

import { computeWealthSummary, sharePct, type PortfolioWealth } from "./wealthOverview.ts";
import type { Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";

function portfolio(id: number, name: string, cash: number): Portfolio {
  return { id, name, cash_balance: cash, created_at: "2026-01-01T00:00:00Z" };
}

function holding(overrides: Partial<PortfolioItem> & { symbol: string; shares: number; avg_cost: number }): PortfolioItem {
  return {
    id: 0,
    portfolio_id: 0,
    current_price: null,
    previous_close: null,
    change_percent: null,
    last_updated: null,
    latest_signal: null,
    signal_confidence: null,
    analyzed_at: null,
    reasoning: null,
    risks: null,
    ta_score: null,
    fa_score: null,
    allow_swap: true,
    target_price: null,
    upside_pct: null,
    risk_level: null,
    ...overrides,
  };
}

function quote(symbol: string, current: number): PriceRefreshItem {
  return { symbol, current_price: current, previous_close: current, change_percent: 0, last_updated: null };
}

test("combines cash + priced holdings across two portfolios into one total", () => {
  const portfolios = [portfolio(1, "Growth", 1000), portfolio(2, "Income", 500)];
  const holdingsMap = {
    1: [holding({ symbol: "AAA", shares: 10, avg_cost: 50 })],
    2: [holding({ symbol: "BBB", shares: 5, avg_cost: 20 })],
  };
  const priceMap = {
    1: [quote("AAA", 60)], // 10 * 60 = 600
    2: [quote("BBB", 25)], // 5 * 25 = 125
  };

  const summary = computeWealthSummary(portfolios, holdingsMap, priceMap, {});

  assert.equal(summary.portfolios[0].total, 1000 + 600);
  assert.equal(summary.portfolios[1].total, 500 + 125);
  assert.equal(summary.totalWealth, 1000 + 600 + 500 + 125);
});

test("separates cash from holdings value in the per-portfolio breakdown", () => {
  const portfolios = [portfolio(1, "P1", 250)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 2, avg_cost: 100 })] };
  const priceMap = { 1: [quote("AAA", 150)] };

  const [row] = computeWealthSummary(portfolios, holdingsMap, priceMap, {}).portfolios;

  assert.equal(row.cash, 250);
  assert.equal(row.holdingsValue, 300);
  assert.equal(row.total, 550);
});

test("computes each portfolio's percentage share of total wealth", () => {
  const portfolios = [portfolio(1, "P1", 300), portfolio(2, "P2", 700)];
  const summary = computeWealthSummary(portfolios, {}, {}, {});

  assert.equal(sharePct(summary.portfolios[0], summary.totalWealth), 30);
  assert.equal(sharePct(summary.portfolios[1], summary.totalWealth), 70);
});

test("a portfolio with no holdings contributes cash only, with zero holdings value", () => {
  const portfolios = [portfolio(1, "Empty", 900)];
  const summary = computeWealthSummary(portfolios, { 1: [] }, {}, {});

  assert.equal(summary.portfolios[0].holdingsValue, 0);
  assert.equal(summary.portfolios[0].total, 900);
  assert.equal(summary.portfolios[0].hasEstimatedPrice, false);
  assert.equal(summary.totalWealth, 900);
});

test("zero portfolios produces zero total wealth and an empty breakdown", () => {
  const summary = computeWealthSummary([], {}, {}, {});
  assert.equal(summary.totalWealth, 0);
  assert.deepEqual(summary.portfolios, []);
});

test("a portfolio whose holdings fetch failed is excluded from the total, not counted as zero silently", () => {
  const portfolios = [portfolio(1, "Good", 100), portfolio(2, "Broken", 5000)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 1, avg_cost: 10 })] };
  const priceMap = { 1: [quote("AAA", 10)] };

  const summary = computeWealthSummary(portfolios, holdingsMap, priceMap, { 2: true });

  // Total reflects only the portfolio we could actually price — the broken
  // one's real (much larger) value is never silently folded in as 0.
  assert.equal(summary.totalWealth, 110);
  assert.equal(summary.anyFailed, true);
  const failedRow = summary.portfolios.find((r) => r.portfolioId === 2) as PortfolioWealth;
  assert.equal(failedRow.failed, true);
  assert.equal(sharePct(failedRow, summary.totalWealth), null);
});

test("a holding with no confirmed live or DB price falls back to avg_cost and is flagged estimated", () => {
  const portfolios = [portfolio(1, "P1", 0)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 3, avg_cost: 40, current_price: null })] };

  const summary = computeWealthSummary(portfolios, holdingsMap, {}, {});

  assert.equal(summary.portfolios[0].holdingsValue, 120); // 3 * 40 (avg_cost fallback)
  assert.equal(summary.portfolios[0].hasEstimatedPrice, true);
  assert.equal(summary.anyEstimated, true);
});

test("a live-refreshed price takes priority over a stale DB current_price", () => {
  const portfolios = [portfolio(1, "P1", 0)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 1, avg_cost: 10, current_price: 12 })] };
  const priceMap = { 1: [quote("AAA", 20)] };

  const summary = computeWealthSummary(portfolios, holdingsMap, priceMap, {});

  assert.equal(summary.portfolios[0].holdingsValue, 20);
  assert.equal(summary.portfolios[0].hasEstimatedPrice, false);
});

test("a holding priced from an expired-cache fallback is flagged stale, not estimated — the number still contributes to the total", () => {
  const portfolios = [portfolio(1, "P1", 0)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 2, avg_cost: 10 })] };
  const priceMap = { 1: [{ ...quote("AAA", 30), is_stale: true }] };

  const summary = computeWealthSummary(portfolios, holdingsMap, priceMap, {});

  assert.equal(summary.portfolios[0].holdingsValue, 60); // the stale price is still used, not discarded
  assert.equal(summary.portfolios[0].hasStalePrice, true);
  assert.equal(summary.portfolios[0].hasEstimatedPrice, false); // distinct concern: we do have a real price
  assert.equal(summary.anyStale, true);
});

test("a fresh live price is never flagged stale", () => {
  const portfolios = [portfolio(1, "P1", 0)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 1, avg_cost: 10 })] };
  const priceMap = { 1: [quote("AAA", 15)] }; // is_stale omitted, like a real fresh quote

  const summary = computeWealthSummary(portfolios, holdingsMap, priceMap, {});

  assert.equal(summary.portfolios[0].hasStalePrice, false);
  assert.equal(summary.anyStale, false);
});

test("sharePct never returns NaN or Infinity when total wealth is zero", () => {
  const portfolios = [portfolio(1, "P1", 0), portfolio(2, "P2", 0)];
  const summary = computeWealthSummary(portfolios, {}, {}, {});

  assert.equal(summary.totalWealth, 0);
  for (const row of summary.portfolios) {
    const pct = sharePct(row, summary.totalWealth);
    assert.equal(pct, 0);
    assert.equal(Number.isFinite(pct), true);
  }
});

test("sharePct is finite even for a negative-cash portfolio sitting alongside positive ones", () => {
  const portfolios = [portfolio(1, "Overdrawn", -100), portfolio(2, "Healthy", 500)];
  const summary = computeWealthSummary(portfolios, {}, {}, {});

  assert.equal(summary.totalWealth, 400);
  const pcts = summary.portfolios.map((r) => sharePct(r, summary.totalWealth));
  for (const pct of pcts) {
    assert.equal(Number.isFinite(pct), true);
  }
});
