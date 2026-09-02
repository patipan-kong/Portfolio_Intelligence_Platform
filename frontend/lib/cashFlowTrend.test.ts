import assert from "node:assert/strict";
import { test } from "node:test";

import type { CashAccount, CashFlowEvent } from "./api.ts";
import {
  computeCashFlowTrend,
  computeTrendPopulation,
  trendMonths,
  type CashFlowTrendPoint,
} from "./cashFlowTrend.ts";
import type { MonthlyFetchResult } from "./emergencyFund.ts";

function account(overrides: Partial<CashAccount> = {}): CashAccount {
  return {
    id: 1,
    workspace_id: 1,
    name: "Everyday Cash",
    institution: "SCB",
    currency: "THB",
    balance: 1000,
    is_archived: false,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
    baseline: {
      id: 1,
      cash_account_id: 1,
      effective_on: "2026-01-01",
      observed_balance: 1000,
      created_at: "2026-01-01T00:00:00Z",
    },
    ...overrides,
  };
}

function event(overrides: Partial<CashFlowEvent> = {}): CashFlowEvent {
  return {
    id: 1,
    workspace_id: 1,
    cash_account_id: 1,
    account_name: "Everyday Cash",
    account_is_archived: false,
    transaction_type: "INCOME",
    amount: 100,
    signed_amount: 100,
    occurred_on: "2026-08-15",
    category: "Salary",
    note: null,
    created_at: "2026-08-15T08:00:00Z",
    ...overrides,
  };
}

function pointFor(points: CashFlowTrendPoint[], month: string): CashFlowTrendPoint {
  const point = points.find((p) => p.month === month);
  assert.ok(point, `expected a point for ${month}`);
  return point!;
}

const NOW = new Date(2026, 7, 26); // 2026-08-26 -> anchor "2026-08"

// ─── trendMonths ─────────────────────────────────────────────────────────────

test("3M window returns 3 trailing completed months, excluding the anchor month", () => {
  assert.deepEqual(trendMonths("2026-08", 3), ["2026-05", "2026-06", "2026-07"]);
});

test("6M window returns 6 trailing completed months", () => {
  assert.deepEqual(trendMonths("2026-08", 6), ["2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07"]);
});

test("12M window crosses a year boundary correctly", () => {
  assert.deepEqual(trendMonths("2026-08", 12), [
    "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
    "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07",
  ]);
});

test("window anchored in January rolls back into the previous year", () => {
  assert.deepEqual(trendMonths("2026-01", 3), ["2025-10", "2025-11", "2025-12"]);
});

test("current (anchor) month is never included in any window size", () => {
  for (const size of [3, 6, 12] as const) {
    assert.ok(!trendMonths("2026-08", size).includes("2026-08"));
  }
});

// ─── computeTrendPopulation ──────────────────────────────────────────────────

test("all requested months are eligible when the baseline predates the window", () => {
  const population = computeTrendPopulation("success", [account()], 6, NOW);
  assert.equal(population.evidenceAvailable, true);
  assert.deepEqual(population.eligibleMonths, population.requestedMonths);
});

test("months before the earliest tracked-active baseline are excluded from eligibility", () => {
  const acc = account({ baseline: { id: 1, cash_account_id: 1, effective_on: "2026-06-01", observed_balance: 500, created_at: "2026-06-01T00:00:00Z" } });
  const population = computeTrendPopulation("success", [acc], 6, NOW);
  assert.deepEqual(population.eligibleMonths, ["2026-06", "2026-07"]);
});

test("no tracked-active accounts yields evidenceAvailable true but zero eligible months", () => {
  const population = computeTrendPopulation("success", [account({ baseline: null })], 6, NOW);
  assert.equal(population.evidenceAvailable, true);
  assert.deepEqual(population.eligibleMonths, []);
});

test("archived accounts are excluded from baseline gating even with an early baseline", () => {
  const acc = account({ is_archived: true, baseline: { id: 1, cash_account_id: 1, effective_on: "2020-01-01", observed_balance: 1, created_at: "2020-01-01T00:00:00Z" } });
  const population = computeTrendPopulation("success", [acc], 3, NOW);
  assert.deepEqual(population.eligibleMonths, []);
});

test("a failed account fetch yields evidenceAvailable false and zero eligible months", () => {
  const population = computeTrendPopulation("error", [account()], 6, NOW);
  assert.equal(population.evidenceAvailable, false);
  assert.deepEqual(population.eligibleMonths, []);
});

// ─── computeCashFlowTrend ────────────────────────────────────────────────────

test("an eligible month with a successful zero-event fetch is AVAILABLE with genuine zero values", () => {
  const population = computeTrendPopulation("success", [account()], 3, NOW);
  const monthlyResults: MonthlyFetchResult[] = population.eligibleMonths.map((month) => ({ month, status: "success", events: [] }));
  const trend = computeCashFlowTrend(population, monthlyResults);
  const point = pointFor(trend.points, "2026-07");
  assert.equal(point.status, "AVAILABLE");
  assert.equal(point.income, 0);
  assert.equal(point.expenses, 0);
  assert.equal(point.netCashFlow, 0);
});

test("an eligible month with real events is AVAILABLE with non-zero values", () => {
  const population = computeTrendPopulation("success", [account()], 3, NOW);
  const monthlyResults: MonthlyFetchResult[] = population.eligibleMonths.map((month) => ({
    month,
    status: "success",
    events: month === "2026-07"
      ? [event({ id: 1, occurred_on: "2026-07-05", amount: 500 }), event({ id: 2, transaction_type: "EXPENSE", amount: 200, signed_amount: -200, occurred_on: "2026-07-10", category: "Rent" })]
      : [],
  }));
  const trend = computeCashFlowTrend(population, monthlyResults);
  const point = pointFor(trend.points, "2026-07");
  assert.equal(point.status, "AVAILABLE");
  assert.equal(point.income, 500);
  assert.equal(point.expenses, 200);
  assert.equal(point.netCashFlow, 300);
});

test("a month before the earliest baseline is PRE_TRACKING with null values", () => {
  const acc = account({ baseline: { id: 1, cash_account_id: 1, effective_on: "2026-07-01", observed_balance: 500, created_at: "2026-07-01T00:00:00Z" } });
  const population = computeTrendPopulation("success", [acc], 3, NOW);
  const trend = computeCashFlowTrend(population, []);
  const point = pointFor(trend.points, "2026-05");
  assert.equal(point.status, "PRE_TRACKING");
  assert.equal(point.income, null);
  assert.equal(point.expenses, null);
  assert.equal(point.netCashFlow, null);
});

test("a single failed month fetch is UNAVAILABLE without affecting sibling months", () => {
  const population = computeTrendPopulation("success", [account()], 3, NOW);
  const monthlyResults: MonthlyFetchResult[] = population.eligibleMonths.map((month) => ({
    month,
    status: month === "2026-06" ? "error" : "success",
    events: month === "2026-07" ? [event({ amount: 400, occurred_on: "2026-07-05" })] : [],
  }));
  const trend = computeCashFlowTrend(population, monthlyResults);
  assert.equal(pointFor(trend.points, "2026-06").status, "UNAVAILABLE");
  assert.equal(pointFor(trend.points, "2026-06").income, null);
  assert.equal(pointFor(trend.points, "2026-05").status, "AVAILABLE");
  assert.equal(pointFor(trend.points, "2026-07").status, "AVAILABLE");
  assert.equal(pointFor(trend.points, "2026-07").income, 400);
});

test("mixed available and unavailable months coexist without failing the whole result closed", () => {
  const population = computeTrendPopulation("success", [account()], 3, NOW);
  const monthlyResults: MonthlyFetchResult[] = [
    { month: "2026-05", status: "success", events: [] },
    { month: "2026-06", status: "error", events: [] },
    { month: "2026-07", status: "success", events: [event({ amount: 100 })] },
  ];
  const trend = computeCashFlowTrend(population, monthlyResults);
  const statuses = trend.points.map((p) => p.status);
  assert.deepEqual(statuses, ["AVAILABLE", "UNAVAILABLE", "AVAILABLE"]);
});

test("every eligible month failing yields all UNAVAILABLE points, never fabricated zeros", () => {
  const population = computeTrendPopulation("success", [account()], 3, NOW);
  const monthlyResults: MonthlyFetchResult[] = population.eligibleMonths.map((month) => ({ month, status: "error", events: [] }));
  const trend = computeCashFlowTrend(population, monthlyResults);
  assert.ok(trend.points.every((p) => p.status === "UNAVAILABLE"));
  assert.ok(trend.points.every((p) => p.income === null && p.expenses === null && p.netCashFlow === null));
});

test("an account-evidence failure marks every requested month UNAVAILABLE, not PRE_TRACKING", () => {
  const population = computeTrendPopulation("error", [account()], 3, NOW);
  const trend = computeCashFlowTrend(population, []);
  assert.ok(trend.points.every((p) => p.status === "UNAVAILABLE"));
});

test("a missing monthly result for an eligible month is treated as UNAVAILABLE", () => {
  const population = computeTrendPopulation("success", [account()], 3, NOW);
  const trend = computeCashFlowTrend(population, []);
  assert.ok(trend.points.every((p) => p.status === "UNAVAILABLE"));
});

// ─── summary ─────────────────────────────────────────────────────────────────

test("summary averages only AVAILABLE months and discloses the evidence count", () => {
  const population = computeTrendPopulation("success", [account()], 3, NOW);
  const monthlyResults: MonthlyFetchResult[] = [
    { month: "2026-05", status: "success", events: [event({ amount: 100, occurred_on: "2026-05-05" })] },
    { month: "2026-06", status: "error", events: [] },
    { month: "2026-07", status: "success", events: [event({ amount: 300, occurred_on: "2026-07-05" })] },
  ];
  const trend = computeCashFlowTrend(population, monthlyResults);
  assert.equal(trend.summary.requestedMonths, 3);
  assert.equal(trend.summary.availableMonths, 2);
  assert.equal(trend.summary.averageIncome, 200);
  assert.equal(trend.summary.averageExpenses, 0);
  assert.equal(trend.summary.averageNetCashFlow, 200);
});

test("latestAvailableNetCashFlow is the most recent AVAILABLE month, skipping trailing gaps", () => {
  const population = computeTrendPopulation("success", [account()], 3, NOW);
  const monthlyResults: MonthlyFetchResult[] = [
    { month: "2026-05", status: "success", events: [event({ transaction_type: "EXPENSE", amount: 900, signed_amount: -900 })] },
    { month: "2026-06", status: "success", events: [] },
    { month: "2026-07", status: "error", events: [] },
  ];
  const trend = computeCashFlowTrend(population, monthlyResults);
  assert.equal(trend.summary.latestAvailableNetCashFlow, 0);
});

test("no AVAILABLE months yields null averages rather than fabricated zeros", () => {
  const population = computeTrendPopulation("success", [account({ baseline: null })], 3, NOW);
  const trend = computeCashFlowTrend(population, []);
  assert.equal(trend.summary.availableMonths, 0);
  assert.equal(trend.summary.averageIncome, null);
  assert.equal(trend.summary.averageExpenses, null);
  assert.equal(trend.summary.averageNetCashFlow, null);
  assert.equal(trend.summary.latestAvailableNetCashFlow, null);
});

test("negative Net Cash Flow is preserved through aggregation, not clamped", () => {
  const population = computeTrendPopulation("success", [account()], 3, NOW);
  const monthlyResults: MonthlyFetchResult[] = [
    { month: "2026-05", status: "success", events: [] },
    { month: "2026-06", status: "success", events: [] },
    { month: "2026-07", status: "success", events: [event({ transaction_type: "EXPENSE", amount: 900, signed_amount: -900, category: "Rent", occurred_on: "2026-07-10" })] },
  ];
  const trend = computeCashFlowTrend(population, monthlyResults);
  assert.equal(pointFor(trend.points, "2026-07").netCashFlow, -900);
  assert.equal(trend.summary.averageNetCashFlow, -300);
});
