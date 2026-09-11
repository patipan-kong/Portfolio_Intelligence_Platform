import assert from "node:assert/strict";
import { test } from "node:test";

import { computeExposureSnapshot } from "./crossPortfolioExposure.ts";
import type { Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";

function portfolio(id: number, name: string, cash: number): Portfolio {
  return { id, name, cash_balance: cash, created_at: "2026-01-01T00:00:00Z" };
}

function holding(
  overrides: Partial<PortfolioItem> & { symbol: string; shares: number; avg_cost: number }
): PortfolioItem {
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
    sector: null,
    ...overrides,
  };
}

function quote(symbol: string, current: number): PriceRefreshItem {
  return { symbol, current_price: current, previous_close: current, change_percent: 0, last_updated: null };
}

test("aggregates portfolio value as cash + holdings and shares against total across portfolios", () => {
  const portfolios = [portfolio(1, "Growth", 1000), portfolio(2, "Income", 500)];
  const holdingsMap = {
    1: [holding({ symbol: "AAA", shares: 10, avg_cost: 50, sector: "Technology" })],
    2: [holding({ symbol: "BBB", shares: 5, avg_cost: 20, sector: "Healthcare" })],
  };
  const priceMap = { 1: [quote("AAA", 60)], 2: [quote("BBB", 25)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  assert.equal(snap.portfolios[0].total, 1000 + 600);
  assert.equal(snap.portfolios[1].total, 500 + 125);
  assert.equal(snap.totalValue, 1000 + 600 + 500 + 125);
  const expectedShare0 = ((1000 + 600) / snap.totalValue) * 100;
  assert.ok(Math.abs(snap.portfolios[0].sharePctOfTotalValue! - expectedShare0) < 1e-9);
});

test("cash is included in portfolio total but excluded from the sector/holdings denominator", () => {
  const portfolios = [portfolio(1, "P1", 1000)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 10, avg_cost: 50, sector: "Technology" })] };
  const priceMap = { 1: [quote("AAA", 60)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  assert.equal(snap.totalCash, 1000);
  assert.equal(snap.totalInvestedHoldings, 600);
  assert.equal(snap.totalValue, 1600);
  assert.equal(snap.sectors.length, 1);
  assert.equal(snap.sectors[0].sector, "Technology");
  assert.equal(snap.sectors[0].value, 600);
  assert.equal(snap.sectors[0].sharePctOfHoldings, 100); // cash never dilutes this
});

test("aggregates sector value and share of holdings across portfolios", () => {
  const portfolios = [portfolio(1, "P1", 0), portfolio(2, "P2", 0)];
  const holdingsMap = {
    1: [holding({ symbol: "AAA", shares: 10, avg_cost: 10, sector: "Technology" })], // 100
    2: [
      holding({ symbol: "BBB", shares: 10, avg_cost: 10, sector: "Technology" }), // 100
      holding({ symbol: "CCC", shares: 10, avg_cost: 10, sector: "Healthcare" }), // 100
    ],
  };
  const priceMap = {
    1: [quote("AAA", 10)],
    2: [quote("BBB", 10), quote("CCC", 10)],
  };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  const tech = snap.sectors.find((s) => s.sector === "Technology")!;
  const health = snap.sectors.find((s) => s.sector === "Healthcare")!;
  assert.equal(tech.value, 200);
  assert.equal(health.value, 100);
  assert.equal(snap.totalInvestedHoldings, 300);
  assert.ok(Math.abs(tech.sharePctOfHoldings - (200 / 300) * 100) < 1e-9);
  assert.ok(Math.abs(health.sharePctOfHoldings - (100 / 300) * 100) < 1e-9);
});

test("unknown or blank sector is grouped as Other, holdings are never discarded", () => {
  const portfolios = [portfolio(1, "P1", 0)];
  const holdingsMap = {
    1: [
      holding({ symbol: "AAA", shares: 1, avg_cost: 100, sector: null }),
      holding({ symbol: "BBB", shares: 1, avg_cost: 100, sector: "   " }),
      holding({ symbol: "CCC", shares: 1, avg_cost: 100, sector: "Other" }),
    ],
  };
  const priceMap = { 1: [quote("AAA", 100), quote("BBB", 100), quote("CCC", 100)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  assert.equal(snap.sectors.length, 1);
  assert.equal(snap.sectors[0].sector, "Other");
  assert.equal(snap.sectors[0].value, 300);
  assert.equal(snap.totalInvestedHoldings, 300);
});

test("a symbol held in exactly two portfolios is a duplicate overlap with per-portfolio contribution", () => {
  const portfolios = [portfolio(1, "P1", 0), portfolio(2, "P2", 0)];
  const holdingsMap = {
    1: [holding({ symbol: "AAA", shares: 10, avg_cost: 10 })], // 100
    2: [holding({ symbol: "AAA", shares: 20, avg_cost: 10 })], // 200
  };
  const priceMap = { 1: [quote("AAA", 10)], 2: [quote("AAA", 10)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  assert.equal(snap.overlaps.length, 1);
  const overlap = snap.overlaps[0];
  assert.equal(overlap.symbol, "AAA");
  assert.equal(overlap.totalValue, 300);
  assert.equal(overlap.portfolioCount, 2);
  const p1Share = overlap.portfolios.find((p) => p.portfolioId === 1)!;
  const p2Share = overlap.portfolios.find((p) => p.portfolioId === 2)!;
  assert.equal(p1Share.value, 100);
  assert.ok(Math.abs(p1Share.sharePctOfSymbol - (100 / 300) * 100) < 1e-9);
  assert.equal(p2Share.value, 200);
  assert.ok(Math.abs(p2Share.sharePctOfSymbol - (200 / 300) * 100) < 1e-9);
});

test("the same symbol held in three portfolios is one overlap row with three contributions", () => {
  const portfolios = [portfolio(1, "P1", 0), portfolio(2, "P2", 0), portfolio(3, "P3", 0)];
  const holdingsMap = {
    1: [holding({ symbol: "AAA", shares: 1, avg_cost: 10 })],
    2: [holding({ symbol: "AAA", shares: 1, avg_cost: 10 })],
    3: [holding({ symbol: "AAA", shares: 1, avg_cost: 10 })],
  };
  const priceMap = { 1: [quote("AAA", 10)], 2: [quote("AAA", 10)], 3: [quote("AAA", 10)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  assert.equal(snap.overlaps.length, 1);
  assert.equal(snap.overlaps[0].portfolioCount, 3);
  assert.equal(snap.overlaps[0].portfolios.length, 3);
});

test("a symbol held in exactly one portfolio is excluded from the overlap list", () => {
  const portfolios = [portfolio(1, "P1", 0), portfolio(2, "P2", 0)];
  const holdingsMap = {
    1: [holding({ symbol: "AAA", shares: 1, avg_cost: 10 })],
    2: [holding({ symbol: "BBB", shares: 1, avg_cost: 10 })],
  };
  const priceMap = { 1: [quote("AAA", 10)], 2: [quote("BBB", 10)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  assert.equal(snap.overlaps.length, 0);
});

test("a portfolio whose holdings failed to load is excluded from every total, not treated as zero", () => {
  const portfolios = [portfolio(1, "Good", 1000), portfolio(2, "Broken", 500)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 10, avg_cost: 10, sector: "Technology" })] };
  const priceMap = { 1: [quote("AAA", 10)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, { 2: true });

  const broken = snap.portfolios.find((p) => p.portfolioId === 2)!;
  assert.equal(broken.failed, true);
  assert.equal(broken.sharePctOfTotalValue, null);
  assert.equal(snap.totalValue, 1100); // 1000 cash + 100 holdings; Broken's 500 cash excluded
  assert.deepEqual(snap.failedPortfolioNames, ["Broken"]);
  assert.equal(snap.includedPortfolioCount, 1);
});

test("missing confirmed price falls back to avg_cost and is flagged as estimated, not zeroed", () => {
  const portfolios = [portfolio(1, "P1", 0)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 10, avg_cost: 25, sector: "Technology" })] };
  const priceMap = { 1: [] }; // no live quote at all

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  assert.equal(snap.sectors[0].value, 250); // 10 * avg_cost(25), never 0
  assert.equal(snap.anyEstimatedPrice, true);
  assert.equal(snap.anyStalePrice, false);
});

test("zero portfolios yields an empty, non-throwing snapshot", () => {
  const snap = computeExposureSnapshot([], {}, {}, {});
  assert.deepEqual(snap.portfolios, []);
  assert.equal(snap.totalValue, 0);
  assert.deepEqual(snap.sectors, []);
  assert.deepEqual(snap.overlaps, []);
});

test("a single portfolio still produces sector exposure with no overlaps", () => {
  const portfolios = [portfolio(1, "Only", 100)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 1, avg_cost: 100, sector: "Technology" })] };
  const priceMap = { 1: [quote("AAA", 100)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  assert.equal(snap.sectors.length, 1);
  assert.equal(snap.overlaps.length, 0);
  assert.equal(snap.portfolios[0].sharePctOfTotalValue, 100);
});

test("sectors and overlaps are ordered deterministically by value descending, ties broken alphabetically", () => {
  const portfolios = [portfolio(1, "P1", 0)];
  const holdingsMap = {
    1: [
      holding({ symbol: "ZZZ", shares: 1, avg_cost: 50, sector: "Zeta" }),
      holding({ symbol: "AAA", shares: 1, avg_cost: 50, sector: "Alpha" }),
      holding({ symbol: "BBB", shares: 1, avg_cost: 100, sector: "Beta" }),
    ],
  };
  const priceMap = { 1: [quote("ZZZ", 50), quote("AAA", 50), quote("BBB", 100)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});

  assert.deepEqual(
    snap.sectors.map((s) => s.sector),
    ["Beta", "Alpha", "Zeta"] // 100 first, then the two 50-value sectors alphabetically
  );
});

test("the snapshot never derives severity, risk, target, or recommendation fields", () => {
  const portfolios = [portfolio(1, "P1", 100)];
  const holdingsMap = { 1: [holding({ symbol: "AAA", shares: 1, avg_cost: 100, sector: "Technology" })] };
  const priceMap = { 1: [quote("AAA", 100)] };

  const snap = computeExposureSnapshot(portfolios, holdingsMap, priceMap, {});
  const forbidden = ["severity", "risk", "hhi", "target", "rebalance", "recommend", "priority", "score", "flag"];

  const json = JSON.stringify(snap).toLowerCase();
  for (const word of forbidden) {
    assert.ok(!json.includes(word), `snapshot unexpectedly contains "${word}"`);
  }
});
