import assert from "node:assert/strict";
import { test } from "node:test";

import type { CashAccount, CashFlowEvent } from "./api.ts";
import {
  computeCoveragePopulation,
  computeCoverageGap,
  computeRecordedExpenseCoverage,
  type MonthlyFetchResult,
} from "./emergencyFund.ts";

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

function expenseEvent(overrides: Partial<CashFlowEvent> = {}): CashFlowEvent {
  return {
    id: 1,
    workspace_id: 1,
    cash_account_id: 1,
    account_name: "Everyday Cash",
    account_is_archived: false,
    transaction_type: "EXPENSE",
    amount: 100,
    signed_amount: -100,
    occurred_on: "2026-06-15",
    category: "Food",
    note: null,
    ...overrides,
  } as CashFlowEvent;
}

const NOW = new Date(2026, 7, 26); // 2026-08-26 -> anchor "2026-08", window ["2026-05","2026-06","2026-07"]

// ─── computeCoveragePopulation ──────────────────────────────────────────────

test("1. zero tracked accounts yields zero tracked cash and no recorded months", () => {
  const population = computeCoveragePopulation("success", [], NOW);
  assert.equal(population.evidenceAvailable, true);
  assert.equal(population.trackedCash, 0);
  assert.deepEqual(population.recordedMonths, []);
});

test("2. a tracked account with zero balance is a legitimate zero, not unavailable", () => {
  const population = computeCoveragePopulation("success", [account({ balance: 0 })], NOW);
  assert.equal(population.evidenceAvailable, true);
  assert.equal(population.trackedCash, 0);
});

test("3. an invalid balance (negative or non-finite) makes tracked cash unavailable", () => {
  assert.equal(computeCoveragePopulation("success", [account({ balance: -1 })], NOW).trackedCash, null);
  assert.equal(computeCoveragePopulation("success", [account({ balance: Infinity })], NOW).trackedCash, null);
  assert.equal(computeCoveragePopulation("success", [account({ balance: -1 })], NOW).evidenceAvailable, false);
});

test("4. a non-THB tracked account makes tracked cash unavailable", () => {
  const population = computeCoveragePopulation("success", [account({ currency: "USD" as CashAccount["currency"] })], NOW);
  assert.equal(population.evidenceAvailable, false);
  assert.equal(population.trackedCash, null);
});

test("5. an untracked active account (no baseline) is excluded from tracked cash and disclosed", () => {
  const population = computeCoveragePopulation("success", [
    account({ id: 1, balance: 500 }),
    account({ id: 2, balance: 9000, baseline: null }),
  ], NOW);
  assert.equal(population.trackedCash, 500);
  assert.equal(population.untrackedActiveAccountCount, 1);
});

test("6. an archived account's current balance is excluded even though it has a baseline", () => {
  const population = computeCoveragePopulation("success", [
    account({ id: 1, balance: 500 }),
    account({ id: 2, balance: 8000, is_archived: true }),
  ], NOW);
  assert.equal(population.trackedCash, 500);
  assert.equal(population.untrackedActiveAccountCount, 0);
});

test("only tracked active accounts are validated: an untracked account's invalid balance or currency never makes evidence unavailable", () => {
  const untrackedNegative = computeCoveragePopulation("success", [
    account({ id: 1, balance: 500 }),
    account({ id: 2, balance: -9000, baseline: null }),
  ], NOW);
  assert.equal(untrackedNegative.evidenceAvailable, true);
  assert.equal(untrackedNegative.trackedCash, 500);
  assert.equal(untrackedNegative.untrackedActiveAccountCount, 1);

  const untrackedForeign = computeCoveragePopulation("success", [
    account({ id: 1, balance: 500 }),
    account({ id: 2, currency: "USD" as CashAccount["currency"], baseline: null }),
  ], NOW);
  assert.equal(untrackedForeign.evidenceAvailable, true);
  assert.equal(untrackedForeign.trackedCash, 500);
});

test("only tracked active accounts are validated: an archived account's invalid balance or currency never makes evidence unavailable", () => {
  const archivedNegative = computeCoveragePopulation("success", [
    account({ id: 1, balance: 500 }),
    account({ id: 2, balance: -9000, is_archived: true }),
  ], NOW);
  assert.equal(archivedNegative.evidenceAvailable, true);
  assert.equal(archivedNegative.trackedCash, 500);

  const archivedForeign = computeCoveragePopulation("success", [
    account({ id: 1, balance: 500 }),
    account({ id: 2, currency: "USD" as CashAccount["currency"], is_archived: true }),
  ], NOW);
  assert.equal(archivedForeign.evidenceAvailable, true);
  assert.equal(archivedForeign.trackedCash, 500);
});

test("an untracked active account never blocks a recorded-month window derived from tracked baselines", () => {
  const population = computeCoveragePopulation("success", [
    account({ id: 1, balance: 500 }), // baseline 2026-01-01
    account({ id: 2, balance: 9000, baseline: null }),
  ], NOW);
  assert.deepEqual(population.recordedMonths, ["2026-05", "2026-06", "2026-07"]);
});

test("7. a baseline dated after the whole window yields zero recorded months", () => {
  const population = computeCoveragePopulation("success", [account({
    baseline: { id: 1, cash_account_id: 1, effective_on: "2026-08-01", observed_balance: 1000, created_at: "2026-08-01T00:00:00Z" },
  })], NOW);
  assert.deepEqual(population.recordedMonths, []);
});

test("8. a baseline dated on the first day of the window's last month yields exactly one recorded month", () => {
  const population = computeCoveragePopulation("success", [account({
    baseline: { id: 1, cash_account_id: 1, effective_on: "2026-07-01", observed_balance: 1000, created_at: "2026-07-01T00:00:00Z" },
  })], NOW);
  assert.deepEqual(population.recordedMonths, ["2026-07"]);
});

test("a baseline dated mid-month excludes that same month from recorded evidence", () => {
  const population = computeCoveragePopulation("success", [account({
    baseline: { id: 1, cash_account_id: 1, effective_on: "2026-07-10", observed_balance: 1000, created_at: "2026-07-10T00:00:00Z" },
  })], NOW);
  assert.deepEqual(population.recordedMonths, []);
});

test("9. a baseline dated inside the window's middle month yields exactly two recorded months", () => {
  const population = computeCoveragePopulation("success", [account({
    baseline: { id: 1, cash_account_id: 1, effective_on: "2026-06-01", observed_balance: 1000, created_at: "2026-06-01T00:00:00Z" },
  })], NOW);
  assert.deepEqual(population.recordedMonths, ["2026-06", "2026-07"]);
});

test("10. a baseline dated on or before the window start yields all three recorded months", () => {
  const population = computeCoveragePopulation("success", [account()], NOW); // baseline 2026-01-01
  assert.deepEqual(population.recordedMonths, ["2026-05", "2026-06", "2026-07"]);
});

test("18. crosses a year boundary correctly", () => {
  const januaryAnchor = new Date(2026, 0, 15); // 2026-01-15 -> anchor "2026-01" -> window ["2025-10","2025-11","2025-12"]
  const population = computeCoveragePopulation("success", [account({
    baseline: { id: 1, cash_account_id: 1, effective_on: "2025-01-01", observed_balance: 1000, created_at: "2025-01-01T00:00:00Z" },
  })], januaryAnchor);
  assert.deepEqual(population.recordedMonths, ["2025-10", "2025-11", "2025-12"]);
});

test("20. gates on the earliest baseline among multiple tracked accounts and discloses mid-window starts", () => {
  const population = computeCoveragePopulation("success", [
    account({ id: 1, baseline: { id: 1, cash_account_id: 1, effective_on: "2026-01-01", observed_balance: 1000, created_at: "2026-01-01T00:00:00Z" } }),
    account({ id: 2, baseline: { id: 2, cash_account_id: 2, effective_on: "2026-06-10", observed_balance: 500, created_at: "2026-06-10T00:00:00Z" } }),
  ], NOW);
  assert.deepEqual(population.recordedMonths, ["2026-05", "2026-06", "2026-07"]);
  assert.equal(population.accountsBeganDuringRecordedPeriod, 1);
});

test("does not mutate its inputs", () => {
  const accounts = [account({ id: 1 }), account({ id: 2, baseline: null })];
  const snapshot = JSON.parse(JSON.stringify(accounts));
  computeCoveragePopulation("success", accounts, NOW);
  assert.deepEqual(accounts, snapshot);
});

// ─── computeRecordedExpenseCoverage ─────────────────────────────────────────

function threeMonthPopulation(trackedCash: number) {
  return computeCoveragePopulation("success", [account({ balance: trackedCash })], NOW);
}

test("11. a zero-expense recorded month still counts in the denominator", () => {
  const population = threeMonthPopulation(9000);
  const results: MonthlyFetchResult[] = [
    { month: "2026-05", status: "success", events: [] },
    { month: "2026-06", status: "success", events: [] },
    { month: "2026-07", status: "success", events: [expenseEvent({ occurred_on: "2026-07-01", amount: 30000, signed_amount: -30000 })] },
  ];
  const coverage = computeRecordedExpenseCoverage(population, results);
  assert.equal(coverage.averageRecordedMonthlyExpense, 10000);
});

test("12. all-zero recorded expenses yields NO_RECORDED_EXPENSE, never a division", () => {
  const population = threeMonthPopulation(9000);
  const results: MonthlyFetchResult[] = population.recordedMonths.map((month) => ({ month, status: "success", events: [] }));
  const coverage = computeRecordedExpenseCoverage(population, results);
  assert.equal(coverage.status, "NO_RECORDED_EXPENSE");
  assert.equal(coverage.averageRecordedMonthlyExpense, 0);
  assert.equal(coverage.coverageMonths, null);
});

test("7b. zero recorded months yields INSUFFICIENT_EVIDENCE without fetching", () => {
  const population = computeCoveragePopulation("success", [account({
    baseline: { id: 1, cash_account_id: 1, effective_on: "2026-08-01", observed_balance: 1000, created_at: "2026-08-01T00:00:00Z" },
  })], NOW);
  const coverage = computeRecordedExpenseCoverage(population, []);
  assert.equal(coverage.status, "INSUFFICIENT_EVIDENCE");
  assert.equal(coverage.trackedCash, 1000);
  assert.equal(coverage.averageRecordedMonthlyExpense, null);
});

test("13. computes AVAILABLE coverage correctly", () => {
  const population = threeMonthPopulation(42000);
  const results: MonthlyFetchResult[] = [
    { month: "2026-05", status: "success", events: [expenseEvent({ occurred_on: "2026-05-01", amount: 10000, signed_amount: -10000 })] },
    { month: "2026-06", status: "success", events: [expenseEvent({ occurred_on: "2026-06-01", amount: 10000, signed_amount: -10000 })] },
    { month: "2026-07", status: "success", events: [expenseEvent({ occurred_on: "2026-07-01", amount: 10000, signed_amount: -10000 })] },
  ];
  const coverage = computeRecordedExpenseCoverage(population, results);
  assert.equal(coverage.status, "AVAILABLE");
  assert.equal(coverage.averageRecordedMonthlyExpense, 10000);
  assert.ok(Math.abs((coverage.coverageMonths ?? 0) - 4.2) < 1e-9);
});

test("14. does not cap or clamp a huge coverage ratio", () => {
  const population = threeMonthPopulation(10_000_000);
  const results: MonthlyFetchResult[] = population.recordedMonths.map((month) => ({
    month, status: "success", events: [expenseEvent({ occurred_on: `${month}-01`, amount: 1, signed_amount: -1 })],
  }));
  const coverage = computeRecordedExpenseCoverage(population, results);
  assert.ok((coverage.coverageMonths ?? 0) > 1_000_000);
});

test("15. never renders Infinity when tracked cash is positive and expenses are zero", () => {
  const population = threeMonthPopulation(5000);
  const results: MonthlyFetchResult[] = population.recordedMonths.map((month) => ({ month, status: "success", events: [] }));
  const coverage = computeRecordedExpenseCoverage(population, results);
  assert.equal(coverage.coverageMonths, null);
  assert.equal(coverage.status, "NO_RECORDED_EXPENSE");
});

test("fails closed to UNAVAILABLE if any required month fetch fails, never averaging a partial subset", () => {
  const population = threeMonthPopulation(9000);
  const results: MonthlyFetchResult[] = [
    { month: "2026-05", status: "success", events: [expenseEvent({ occurred_on: "2026-05-01", amount: 30000, signed_amount: -30000 })] },
    { month: "2026-06", status: "error", events: [] },
    { month: "2026-07", status: "success", events: [expenseEvent({ occurred_on: "2026-07-01", amount: 30000, signed_amount: -30000 })] },
  ];
  const coverage = computeRecordedExpenseCoverage(population, results);
  assert.equal(coverage.status, "UNAVAILABLE");
  assert.equal(coverage.averageRecordedMonthlyExpense, null);
});

test("account evidence unavailable yields UNAVAILABLE regardless of month evidence", () => {
  const population = computeCoveragePopulation("error", [], NOW);
  const coverage = computeRecordedExpenseCoverage(population, []);
  assert.equal(coverage.status, "UNAVAILABLE");
  assert.equal(coverage.trackedCash, null);
});

test("flags archived-account expense evidence within recorded months", () => {
  const population = threeMonthPopulation(9000);
  const results: MonthlyFetchResult[] = [
    { month: "2026-05", status: "success", events: [] },
    { month: "2026-06", status: "success", events: [] },
    { month: "2026-07", status: "success", events: [expenseEvent({ occurred_on: "2026-07-01", amount: 1000, signed_amount: -1000, account_is_archived: true })] },
  ];
  const coverage = computeRecordedExpenseCoverage(population, results);
  assert.equal(coverage.hasArchivedAccountExpenses, true);
});

test("19. aggregates a February leap-year expense correctly (reuses aggregateMonthlyCashFlow)", () => {
  const anchor = new Date(2024, 4, 10); // 2024-05-10 -> anchor "2024-05", window ["2024-02","2024-03","2024-04"]
  const population = computeCoveragePopulation("success", [account({
    baseline: { id: 1, cash_account_id: 1, effective_on: "2024-01-01", observed_balance: 1000, created_at: "2024-01-01T00:00:00Z" },
  })], anchor);
  assert.deepEqual(population.recordedMonths, ["2024-02", "2024-03", "2024-04"]);
  const results: MonthlyFetchResult[] = [
    { month: "2024-02", status: "success", events: [expenseEvent({ occurred_on: "2024-02-29", amount: 300, signed_amount: -300 })] },
    { month: "2024-03", status: "success", events: [] },
    { month: "2024-04", status: "success", events: [] },
  ];
  const coverage = computeRecordedExpenseCoverage(population, results);
  assert.ok(Math.abs((coverage.averageRecordedMonthlyExpense ?? 0) - 100) < 1e-9);
});

test("17. is deterministic and repeatable for identical inputs", () => {
  const population = threeMonthPopulation(9000);
  const results: MonthlyFetchResult[] = population.recordedMonths.map((month) => ({
    month, status: "success", events: [expenseEvent({ occurred_on: `${month}-01`, amount: 1000, signed_amount: -1000 })],
  }));
  const first = computeRecordedExpenseCoverage(population, results);
  const second = computeRecordedExpenseCoverage(population, results);
  assert.deepEqual(first, second);
});

test("16. does not mutate the population or monthlyResults inputs", () => {
  const population = threeMonthPopulation(9000);
  const results: MonthlyFetchResult[] = population.recordedMonths.map((month) => ({
    month, status: "success", events: [expenseEvent({ occurred_on: `${month}-01`, amount: 1000, signed_amount: -1000 })],
  }));
  const populationSnapshot = JSON.parse(JSON.stringify(population));
  const resultsSnapshot = JSON.parse(JSON.stringify(results));
  computeRecordedExpenseCoverage(population, results);
  assert.deepEqual(population, populationSnapshot);
  assert.deepEqual(results, resultsSnapshot);
});

// ─── computeCoverageGap ──────────────────────────────────────────────────

test("computeCoverageGap: no target returns null even when coverage is AVAILABLE", () => {
  const population = threeMonthPopulation(42000);
  const results: MonthlyFetchResult[] = population.recordedMonths.map((month) => ({
    month, status: "success", events: [expenseEvent({ occurred_on: `${month}-01`, amount: 10000, signed_amount: -10000 })],
  }));
  const coverage = computeRecordedExpenseCoverage(population, results);
  assert.equal(coverage.status, "AVAILABLE");
  assert.equal(computeCoverageGap(null, coverage), null);
});

test("computeCoverageGap: shortfall (target above tracked cash) is a negative gap", () => {
  const population = threeMonthPopulation(140000);
  const results: MonthlyFetchResult[] = population.recordedMonths.map((month) => ({
    month, status: "success", events: [expenseEvent({ occurred_on: `${month}-01`, amount: 30000, signed_amount: -30000 })],
  }));
  const coverage = computeRecordedExpenseCoverage(population, results);
  const gap = computeCoverageGap(6, coverage);
  assert.ok(gap);
  assert.equal(gap!.targetMonths, 6);
  assert.equal(gap!.targetAmount, 180000);
  assert.equal(gap!.gapAmount, -40000);
});

test("computeCoverageGap: surplus (tracked cash above target) is a positive gap", () => {
  const population = threeMonthPopulation(200000);
  const results: MonthlyFetchResult[] = population.recordedMonths.map((month) => ({
    month, status: "success", events: [expenseEvent({ occurred_on: `${month}-01`, amount: 30000, signed_amount: -30000 })],
  }));
  const coverage = computeRecordedExpenseCoverage(population, results);
  const gap = computeCoverageGap(6, coverage);
  assert.ok(gap);
  assert.equal(gap!.targetAmount, 180000);
  assert.equal(gap!.gapAmount, 20000);
});

test("computeCoverageGap: tracked cash exactly at target yields a zero gap", () => {
  const population = threeMonthPopulation(180000);
  const results: MonthlyFetchResult[] = population.recordedMonths.map((month) => ({
    month, status: "success", events: [expenseEvent({ occurred_on: `${month}-01`, amount: 30000, signed_amount: -30000 })],
  }));
  const coverage = computeRecordedExpenseCoverage(population, results);
  const gap = computeCoverageGap(6, coverage);
  assert.ok(gap);
  assert.equal(gap!.gapAmount, 0);
});

test("computeCoverageGap: never fabricates a target/gap for any non-AVAILABLE status", () => {
  const noExpensePopulation = threeMonthPopulation(9000);
  const noExpenseResults: MonthlyFetchResult[] = noExpensePopulation.recordedMonths.map((month) => ({ month, status: "success", events: [] }));
  const noExpenseCoverage = computeRecordedExpenseCoverage(noExpensePopulation, noExpenseResults);
  assert.equal(noExpenseCoverage.status, "NO_RECORDED_EXPENSE");
  assert.equal(computeCoverageGap(6, noExpenseCoverage), null);

  const insufficientPopulation = computeCoveragePopulation("success", [account({
    baseline: { id: 1, cash_account_id: 1, effective_on: "2026-08-01", observed_balance: 1000, created_at: "2026-08-01T00:00:00Z" },
  })], NOW);
  const insufficientCoverage = computeRecordedExpenseCoverage(insufficientPopulation, []);
  assert.equal(insufficientCoverage.status, "INSUFFICIENT_EVIDENCE");
  assert.equal(computeCoverageGap(6, insufficientCoverage), null);

  const unavailablePopulation = computeCoveragePopulation("error", [], NOW);
  const unavailableCoverage = computeRecordedExpenseCoverage(unavailablePopulation, []);
  assert.equal(unavailableCoverage.status, "UNAVAILABLE");
  assert.equal(computeCoverageGap(6, unavailableCoverage), null);
});
