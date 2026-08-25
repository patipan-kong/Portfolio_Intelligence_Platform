import assert from "node:assert/strict";
import { test } from "node:test";

import type { CashFlowEvent } from "./api.ts";
import { aggregateMonthlyCashFlow, formatMonthLabel, shiftMonth } from "./cashFlow.ts";

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

test("income contributes to Income", () => {
  assert.equal(aggregateMonthlyCashFlow([event({ amount: 125 })], "2026-08").income, 125);
});

test("expense contributes to Expenses", () => {
  assert.equal(
    aggregateMonthlyCashFlow([event({ transaction_type: "EXPENSE", amount: 45, signed_amount: -45, category: "Food" })], "2026-08").expenses,
    45,
  );
});

test("Net Cash Flow equals Income minus Expenses", () => {
  const summary = aggregateMonthlyCashFlow([
    event({ id: 1, amount: 500 }),
    event({ id: 2, transaction_type: "EXPENSE", amount: 125, signed_amount: -125, category: "Rent" }),
  ], "2026-08");
  assert.equal(summary.netCashFlow, 375);
});

test("ADJUSTMENT is excluded from Income, Expenses, and Net Cash Flow", () => {
  const summary = aggregateMonthlyCashFlow([
    event({ transaction_type: "ADJUSTMENT", amount: 250, signed_amount: 250, category: "Reconciliation" }),
  ], "2026-08");
  assert.equal(summary.income, 0);
  assert.equal(summary.expenses, 0);
  assert.equal(summary.netCashFlow, 0);
  assert.equal(summary.adjustments, 250);
  assert.equal(summary.eventCount, 1);
});

test("first and last day of the selected month are included", () => {
  const summary = aggregateMonthlyCashFlow([
    event({ id: 1, occurred_on: "2026-08-01", amount: 10 }),
    event({ id: 2, occurred_on: "2026-08-31", amount: 20 }),
  ], "2026-08");
  assert.equal(summary.income, 30);
});

test("adjacent months are excluded", () => {
  const summary = aggregateMonthlyCashFlow([
    event({ id: 1, occurred_on: "2026-07-31", amount: 10 }),
    event({ id: 2, occurred_on: "2026-09-01", amount: 20 }),
  ], "2026-08");
  assert.deepEqual(summary.events, []);
  assert.equal(summary.eventCount, 0);
});

test("multiple accounts aggregate into one workspace summary", () => {
  const summary = aggregateMonthlyCashFlow([
    event({ id: 1, cash_account_id: 1, account_name: "Everyday Cash", amount: 100 }),
    event({ id: 2, cash_account_id: 2, account_name: "Reserve", amount: 250 }),
  ], "2026-08");
  assert.equal(summary.income, 350);
  assert.deepEqual(summary.events.map((row) => row.account_name), ["Reserve", "Everyday Cash"]);
});

test("negative Net Cash Flow is supported", () => {
  const summary = aggregateMonthlyCashFlow([
    event({ transaction_type: "EXPENSE", amount: 900, signed_amount: -900, category: "Rent" }),
  ], "2026-08");
  assert.equal(summary.netCashFlow, -900);
});

test("an empty month returns a deterministic zero summary", () => {
  assert.deepEqual(aggregateMonthlyCashFlow([], "2026-08"), {
    month: "2026-08",
    income: 0,
    expenses: 0,
    netCashFlow: 0,
    adjustments: 0,
    eventCount: 0,
    events: [],
    expenseCategories: {},
    incomeCategories: {},
  });
});

test("expense category totals reconcile to Expenses", () => {
  const summary = aggregateMonthlyCashFlow([
    event({ id: 1, transaction_type: "EXPENSE", amount: 75, signed_amount: -75, category: "Food" }),
    event({ id: 2, transaction_type: "EXPENSE", amount: 25, signed_amount: -25, category: "Food" }),
    event({ id: 3, transaction_type: "EXPENSE", amount: 100, signed_amount: -100, category: "Rent" }),
  ], "2026-08");
  assert.equal(Object.values(summary.expenseCategories).reduce((total, value) => total + value, 0), summary.expenses);
  assert.deepEqual(summary.expenseCategories, { Food: 100, Rent: 100 });
});

test("an archived-account event remains eligible for pure aggregation", () => {
  const summary = aggregateMonthlyCashFlow([
    event({ account_is_archived: true, amount: 40 }),
  ], "2026-08");
  assert.equal(summary.income, 40);
  assert.equal(summary.events[0].account_is_archived, true);
});

test("activity is newest first with id tie-break ordering", () => {
  const summary = aggregateMonthlyCashFlow([
    event({ id: 2, occurred_on: "2026-08-10", amount: 20 }),
    event({ id: 3, occurred_on: "2026-08-10", amount: 30 }),
    event({ id: 1, occurred_on: "2026-08-20", amount: 10 }),
  ], "2026-08");
  assert.deepEqual(summary.events.map((row) => row.id), [1, 3, 2]);
});

test("month navigation and labels use calendar keys", () => {
  assert.equal(shiftMonth("2026-01", -1), "2025-12");
  assert.equal(shiftMonth("2026-12", 1), "2027-01");
  assert.equal(formatMonthLabel("2026-08"), "August 2026");
});
