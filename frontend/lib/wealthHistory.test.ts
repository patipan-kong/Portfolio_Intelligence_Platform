import assert from "node:assert/strict";
import { test } from "node:test";

import { computeWealthHistory, type WealthHistoryPortfolio } from "./wealthHistory.ts";
import type { PortfolioSnapshotRow } from "@/lib/api";

function portfolio(id: number, createdAt: string, name = `Portfolio ${id}`): WealthHistoryPortfolio {
  return { id, name, created_at: createdAt };
}

function snapshot(portfolioId: number, date: string, totalValue: number): PortfolioSnapshotRow {
  return {
    id: portfolioId * 1000 + date.replace(/-/g, "").length, // unique-enough dummy id, not asserted on
    portfolio_id: portfolioId,
    snapshot_date: date,
    total_value: totalValue,
    cash_balance: 0,
    total_invested: 0,
    unrealized_pnl: null,
    unrealized_pnl_pct: null,
    realized_pnl: null,
    daily_return_pct: null,
    investment_return_pct: null,
    investment_return_amount: null,
    net_external_cash_flow: null,
    imported_asset_value: null,
    manual_adjustment_value: null,
    period_realized_pnl: null,
    period_dividend_income: null,
    period_fees_paid: null,
    holdings_count: null,
    sector_breakdown: null,
    holdings: null,
    created_at: null,
  };
}

test("two portfolios with aligned dates sum correctly", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z");
  const result = computeWealthHistory([a, b], {
    1: [snapshot(1, "2026-06-01", 500_000)],
    2: [snapshot(2, "2026-06-01", 300_000)],
  });

  assert.equal(result.points.length, 1);
  assert.equal(result.points[0].totalValue, 800_000);
  assert.equal(result.points[0].contributingCount, 2);
  assert.equal(result.points[0].expectedCount, 2);
  assert.equal(result.points[0].complete, true);
});

test("a portfolio with no snapshots at all does not get a fabricated zero — its date is marked incomplete instead", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z"); // existed, but never has any snapshot
  const result = computeWealthHistory([a, b], {
    1: [snapshot(1, "2026-06-01", 500_000)],
    2: [],
  });

  assert.equal(result.points.length, 1);
  // Sum reflects only the portfolio that actually reported — never 500_000 + 0.
  assert.equal(result.points[0].totalValue, 500_000);
  assert.equal(result.points[0].contributingCount, 1);
  assert.equal(result.points[0].expectedCount, 2);
  assert.equal(result.points[0].complete, false);
  assert.equal(result.completePoints.length, 0);
});

test("partially covered dates are identified as partial (complete: false), fully covered dates are not", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z");
  const result = computeWealthHistory([a, b], {
    1: [snapshot(1, "2026-06-01", 500_000), snapshot(1, "2026-06-02", 500_000)],
    2: [snapshot(2, "2026-06-01", 300_000)], // missing on 06-02
  });

  const monday = result.points.find((p) => p.date === "2026-06-01")!;
  const tuesday = result.points.find((p) => p.date === "2026-06-02")!;
  assert.equal(monday.complete, true);
  assert.equal(tuesday.complete, false);
  assert.deepEqual(result.completePoints.map((p) => p.date), ["2026-06-01"]);
});

test("a missing snapshot does not create a false headline wealth loss", () => {
  // Doc example: Monday A+B = 800,000. Tuesday only A = 500,000 reports —
  // this must never read as an 800,000 -> 500,000 loss.
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z");
  const result = computeWealthHistory([a, b], {
    1: [
      snapshot(1, "2026-06-01", 500_000),
      snapshot(1, "2026-06-02", 500_000), // B absent this day
      snapshot(1, "2026-06-03", 520_000),
    ],
    2: [snapshot(2, "2026-06-01", 300_000), snapshot(2, "2026-06-03", 300_000)],
  });

  // The partial Tuesday point is never used for the headline delta.
  assert.notEqual(result.delta?.change, 500_000 - 800_000);
  assert.equal(result.delta?.from.date, "2026-06-01");
  assert.equal(result.delta?.to.date, "2026-06-03");
  assert.equal(result.delta?.change, 820_000 - 800_000);
});

test("headline delta uses two comparable complete-coverage observations", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z");
  const result = computeWealthHistory([a, b], {
    1: [snapshot(1, "2026-06-01", 500_000), snapshot(1, "2026-06-02", 999_999), snapshot(1, "2026-06-03", 510_000)],
    2: [snapshot(2, "2026-06-01", 300_000), snapshot(2, "2026-06-03", 310_000)], // absent 06-02
  });

  assert.ok(result.delta);
  assert.equal(result.delta!.from.complete, true);
  assert.equal(result.delta!.to.complete, true);
  assert.equal(result.delta!.from.date, "2026-06-01");
  assert.equal(result.delta!.to.date, "2026-06-03");
});

test("fewer than two comparable complete points produces an unavailable delta, not a manufactured one", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const onlyOnePoint = computeWealthHistory([a], { 1: [snapshot(1, "2026-06-01", 500_000)] });
  assert.equal(onlyOnePoint.delta, null);
  assert.equal(onlyOnePoint.latest?.totalValue, 500_000);

  const noPoints = computeWealthHistory([a], { 1: [] });
  assert.equal(noPoints.delta, null);
  assert.equal(noPoints.latest, null);
});

test("empty portfolio set is safe", () => {
  const result = computeWealthHistory([], {});
  assert.deepEqual(result.points, []);
  assert.deepEqual(result.completePoints, []);
  assert.equal(result.latest, null);
  assert.equal(result.delta, null);
  assert.equal(result.hasAnySnapshots, false);
  assert.equal(result.anyPartial, false);
  assert.equal(result.anyFailed, false);
});

test("a failed portfolio fetch is represented honestly — never a silent zero, and it keeps affected dates incomplete", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z"); // existed on the date below, but its fetch failed
  const result = computeWealthHistory(
    [a, b],
    { 1: [snapshot(1, "2026-06-01", 500_000)], 2: [snapshot(2, "2026-06-01", 999_999)] },
    { 2: true }
  );

  assert.equal(result.anyFailed, true);
  // b's snapshot data is excluded entirely, not treated as 0 or as its real value.
  assert.equal(result.points[0].totalValue, 500_000);
  assert.equal(result.points[0].contributingCount, 1);
  assert.equal(result.points[0].expectedCount, 2);
  assert.equal(result.points[0].complete, false);
  assert.equal(result.completePoints.length, 0);
  assert.equal(result.latest, null);
});

test("portfolios with differing historical start dates follow the creation-date lifecycle rule deterministically", () => {
  const early = portfolio(1, "2026-01-01T00:00:00Z");
  const late = portfolio(2, "2026-02-01T00:00:00Z"); // does not exist yet in January

  const result = computeWealthHistory([early, late], {
    1: [snapshot(1, "2026-01-15", 500_000), snapshot(1, "2026-02-10", 500_000)],
    2: [snapshot(2, "2026-02-10", 300_000)], // late didn't exist on 01-15, so no snapshot expected then
  });

  const january = result.points.find((p) => p.date === "2026-01-15")!;
  const february = result.points.find((p) => p.date === "2026-02-10")!;

  // January: only `early` was expected to exist — its lone snapshot is complete coverage.
  assert.equal(january.expectedCount, 1);
  assert.equal(january.complete, true);
  assert.equal(january.totalValue, 500_000);

  // February: both portfolios existed and both reported — complete, summed.
  assert.equal(february.expectedCount, 2);
  assert.equal(february.complete, true);
  assert.equal(february.totalValue, 800_000);
});

test("totals are summed as plain numbers, consistent with the existing single-currency snapshot/Wealth Overview convention", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z");
  const result = computeWealthHistory([a, b], {
    1: [snapshot(1, "2026-06-01", 123.45)],
    2: [snapshot(2, "2026-06-01", 67.89)],
  });

  assert.equal(typeof result.points[0].totalValue, "number");
  assert.equal(result.points[0].totalValue, 123.45 + 67.89);
});
