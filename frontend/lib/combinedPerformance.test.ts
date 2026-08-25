import assert from "node:assert/strict";
import { test } from "node:test";

import { computeCombinedPerformance, type CombinedPerformancePortfolio } from "./combinedPerformance.ts";
import type { PortfolioSnapshotRow } from "@/lib/api";

function portfolio(id: number, createdAt: string, name = `Portfolio ${id}`): CombinedPerformancePortfolio {
  return { id, name, created_at: createdAt };
}

// beginningNav/gain fully determine the row's contribution — totalValue is
// derived from them (plus any cash-flow legs) so eligibleObservation()'s
// algebraic inversion reconstructs exactly the beginningNav/gain given here.
function snapshot(
  portfolioId: number,
  date: string,
  opts: {
    beginningNav?: number;
    gain?: number;
    netExternalCashFlow?: number;
    importedAssetValue?: number;
    manualAdjustmentValue?: number;
    investmentReturnAmount?: number | null; // overrides gain-derived value when explicitly provided
    totalValueOverride?: number; // overrides the derived total_value entirely
  } = {}
): PortfolioSnapshotRow {
  const {
    beginningNav = 1000,
    gain = 0,
    netExternalCashFlow = 0,
    importedAssetValue = 0,
    manualAdjustmentValue = 0,
    investmentReturnAmount = gain,
    totalValueOverride,
  } = opts;
  const totalValue =
    totalValueOverride ??
    beginningNav + gain + netExternalCashFlow + importedAssetValue + manualAdjustmentValue;
  return {
    id: portfolioId * 1000 + date.replace(/-/g, "").length,
    portfolio_id: portfolioId,
    snapshot_date: date,
    total_value: totalValue,
    cash_balance: 0,
    total_invested: 0,
    unrealized_pnl: null,
    unrealized_pnl_pct: null,
    realized_pnl: null,
    daily_return_pct: investmentReturnAmount == null ? null : (investmentReturnAmount / beginningNav) * 100,
    investment_return_pct: investmentReturnAmount == null ? null : (investmentReturnAmount / beginningNav) * 100,
    investment_return_amount: investmentReturnAmount,
    net_external_cash_flow: netExternalCashFlow,
    imported_asset_value: importedAssetValue,
    manual_adjustment_value: manualAdjustmentValue,
    period_realized_pnl: null,
    period_dividend_income: null,
    period_fees_paid: null,
    holdings_count: null,
    sector_breakdown: null,
    holdings: null,
    created_at: null,
  };
}

test("single-portfolio combined performance equals that portfolio's own investment_return_pct", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const row = snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 50 }); // 5%
  const result = computeCombinedPerformance([a], { 1: [row] });

  assert.equal(result.points.length, 1);
  assert.ok(Math.abs(result.points[0].combinedReturnPct - 5) < 1e-9);
  assert.ok(Math.abs((result.cumulativeReturnPct ?? NaN) - 5) < 1e-9);
  assert.ok(Math.abs(result.points[0].combinedReturnPct - row.investment_return_pct!) < 1e-9);
});

test("two portfolios are weighted by beginning-of-period NAV, not equal-weighted", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z");
  // A: 100 -> +50% return. B: 900 -> 0% return.
  // Equal-weight average would be 25%. NAV-weighted correct answer is 5%.
  const result = computeCombinedPerformance(
    [a, b],
    {
      1: [snapshot(1, "2026-06-01", { beginningNav: 100, gain: 50 })],
      2: [snapshot(2, "2026-06-01", { beginningNav: 900, gain: 0 })],
    }
  );

  assert.equal(result.points.length, 1);
  assert.ok(Math.abs(result.points[0].combinedReturnPct - 5) < 1e-9);
  assert.notEqual(Math.round(result.points[0].combinedReturnPct), 25);
});

test("multi-day returns are TWR chain-linked, not summed", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const result = computeCombinedPerformance([a], {
    1: [
      snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 100 }), // +10%
      snapshot(1, "2026-06-02", { beginningNav: 1100, gain: 110 }), // +10%
      snapshot(1, "2026-06-03", { beginningNav: 1210, gain: -60.5 }), // -5%
    ],
  });

  assert.equal(result.points.length, 3);
  // 100 * 1.10 * 1.10 * 0.95 = 114.95 -> cumulative +14.95%
  assert.ok(Math.abs((result.cumulativeReturnPct ?? NaN) - 14.95) < 1e-6);
  // Not a naive sum of the three period returns (10 + 10 - 5 = 15).
  assert.notEqual(Math.round((result.cumulativeReturnPct ?? 0) * 100) / 100, 15);
});

test("a deposit into one portfolio does not create investment return", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const withoutDeposit = computeCombinedPerformance([a], {
    1: [snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 50 })],
  });
  const withDeposit = computeCombinedPerformance([a], {
    1: [snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 50, netExternalCashFlow: 5000 })],
  });

  assert.ok(Math.abs(withoutDeposit.cumulativeReturnPct! - withDeposit.cumulativeReturnPct!) < 1e-9);
});

test("a withdrawal from one portfolio does not create investment loss", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const withoutWithdrawal = computeCombinedPerformance([a], {
    1: [snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 50 })],
  });
  const withWithdrawal = computeCombinedPerformance([a], {
    1: [snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 50, netExternalCashFlow: -3000 })],
  });

  assert.ok(Math.abs(withoutWithdrawal.cumulativeReturnPct! - withWithdrawal.cumulativeReturnPct!) < 1e-9);
});

test("imported positions and manual quantity corrections remain neutral — already excluded upstream", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const baseline = computeCombinedPerformance([a], {
    1: [snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 50 })],
  });
  const withImportAndAdjustment = computeCombinedPerformance([a], {
    1: [
      snapshot(1, "2026-06-01", {
        beginningNav: 1000,
        gain: 50,
        importedAssetValue: 20000,
        manualAdjustmentValue: -750,
      }),
    ],
  });

  assert.ok(Math.abs(baseline.cumulativeReturnPct! - withImportAndAdjustment.cumulativeReturnPct!) < 1e-9);
});

test("a missing required snapshot date is excluded, not zero-filled", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z");
  const result = computeCombinedPerformance(
    [a, b],
    {
      1: [
        snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 100 }),
        snapshot(1, "2026-06-02", { beginningNav: 1100, gain: 50 }),
      ],
      2: [snapshot(2, "2026-06-01", { beginningNav: 500, gain: 0 })], // missing on 06-02
    }
  );

  assert.deepEqual(result.points.map((p) => p.date), ["2026-06-01"]);
  assert.equal(result.excludedCount, 1);
});

test("a portfolio created later does not alter earlier historical combined performance", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-06-03T00:00:00Z"); // does not exist yet on 06-01/06-02
  const withoutB = computeCombinedPerformance([a], {
    1: [
      snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 100 }),
      snapshot(1, "2026-06-02", { beginningNav: 1100, gain: -20 }),
    ],
  });
  const withB = computeCombinedPerformance([a, b], {
    1: [
      snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 100 }),
      snapshot(1, "2026-06-02", { beginningNav: 1100, gain: -20 }),
    ],
    2: [],
  });

  assert.deepEqual(
    withB.points.map((p) => [p.date, Math.round(p.combinedReturnPct * 1e6)]),
    withoutB.points.map((p) => [p.date, Math.round(p.combinedReturnPct * 1e6)])
  );
});

test("a newly created portfolio only joins the combined series once it has an eligible return observation", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-06-03T00:00:00Z");
  const result = computeCombinedPerformance(
    [a, b],
    {
      1: [
        snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 100 }),
        snapshot(1, "2026-06-02", { beginningNav: 1100, gain: 0 }),
        snapshot(1, "2026-06-03", { beginningNav: 1100, gain: 55 }),
        snapshot(1, "2026-06-04", { beginningNav: 1155, gain: 0 }),
      ],
      // B's first-ever snapshot has no prior NAV, matching the backend's own
      // convention: investment_return_amount is null on that first row.
      2: [
        snapshot(2, "2026-06-03", { investmentReturnAmount: null, totalValueOverride: 2000 }),
        snapshot(2, "2026-06-04", { beginningNav: 2000, gain: 40 }),
      ],
    }
  );

  // 06-03: B exists but is not yet eligible (no prior NAV) -> excluded.
  // 06-04: B now has a valid period return -> included, combining both.
  assert.deepEqual(result.points.map((p) => p.date), ["2026-06-01", "2026-06-02", "2026-06-04"]);
  const day4 = result.points.find((p) => p.date === "2026-06-04")!;
  assert.equal(day4.contributingCount, 2);
  assert.equal(day4.expectedCount, 2);
});

test("zero combined beginning NAV produces an unavailable period, not a fabricated 0% return", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  // beginningNav reconstructs to exactly 0 (total_value equals the gain alone).
  const row = snapshot(1, "2026-06-01", { beginningNav: 0, gain: 500, totalValueOverride: 500 });
  const result = computeCombinedPerformance([a], { 1: [row] });

  assert.equal(result.points.length, 0);
  assert.equal(result.excludedCount, 1);
  assert.equal(result.cumulativeReturnPct, null);
});

test("empty input is safe", () => {
  const result = computeCombinedPerformance([], {});
  assert.deepEqual(result.points, []);
  assert.equal(result.cumulativeReturnPct, null);
  assert.equal(result.startDate, null);
  assert.equal(result.endDate, null);
  assert.equal(result.excludedCount, 0);
  assert.equal(result.hasAnySnapshots, false);
  assert.equal(result.anyFailed, false);
});

test("a failed portfolio fetch never lets a date qualify as complete", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z");
  const result = computeCombinedPerformance(
    [a, b],
    { 1: [snapshot(1, "2026-06-01", { beginningNav: 1000, gain: 100 })], 2: [] },
    { 2: true }
  );

  assert.equal(result.points.length, 0);
  assert.equal(result.anyFailed, true);
});

test("coverage and date-range metadata are deterministic regardless of input ordering", () => {
  const a = portfolio(1, "2026-01-01T00:00:00Z");
  const b = portfolio(2, "2026-01-01T00:00:00Z");
  const snapshotsByPortfolio = {
    1: [
      snapshot(1, "2026-06-02", { beginningNav: 1000, gain: 10 }),
      snapshot(1, "2026-06-01", { beginningNav: 990, gain: 10 }),
    ],
    2: [
      snapshot(2, "2026-06-01", { beginningNav: 500, gain: 5 }),
      snapshot(2, "2026-06-02", { beginningNav: 505, gain: 5 }),
    ],
  };

  const result1 = computeCombinedPerformance([a, b], snapshotsByPortfolio);
  const result2 = computeCombinedPerformance([b, a], snapshotsByPortfolio);

  assert.deepEqual(result1.points.map((p) => p.date), ["2026-06-01", "2026-06-02"]);
  assert.equal(result1.startDate, "2026-06-01");
  assert.equal(result1.endDate, "2026-06-02");
  assert.deepEqual(
    result1.points.map((p) => p.date),
    result2.points.map((p) => p.date)
  );
  assert.ok(Math.abs(result1.cumulativeReturnPct! - result2.cumulativeReturnPct!) < 1e-9);
});
