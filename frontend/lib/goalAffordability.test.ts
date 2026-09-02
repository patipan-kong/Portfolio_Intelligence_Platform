// Pinned before any test runs so the local/UTC calendar split this module
// must never reintroduce is actually observable: in Asia/Bangkok (UTC+7) the
// first 7 hours of every month fall on the PREVIOUS month's final day in UTC.
// Without a fixed non-UTC zone the boundary tests below would pass even if
// month derivation regressed to toISOString(). node --test runs each file in
// its own process, so this affects nothing else.
process.env.TZ = "Asia/Bangkok";

import assert from "node:assert/strict";
import { test } from "node:test";

import type { CashAccount, CashFlowEvent } from "./api.ts";
import { computeRequiredMonthlyContribution } from "./goalWhatIf.ts";
import type { MonthlyFetchResult } from "./emergencyFund.ts";
import {
  computeGoalAffordability,
  goalAffordabilityCalendar,
  type GoalAffordabilityInput,
} from "./goalAffordability.ts";

const AS_OF_DATE = "2026-08-15";
// asOfDate's month is "2026-08" -> trailing completed window is May/Jun/Jul.
const MONTH_1 = "2026-05";
const MONTH_2 = "2026-06";
const MONTH_3 = "2026-07";
const TRAILING_WINDOW = [MONTH_1, MONTH_2, MONTH_3];
const MONTH_MINUS_4 = "2026-04";
const CURRENT_MONTH = "2026-08";

const trackedAccount: CashAccount = {
  id: 1,
  workspace_id: 1,
  name: "Everyday Cash",
  institution: null,
  currency: "THB",
  balance: 50_000,
  is_archived: false,
  created_at: "2026-01-01T00:00:00",
  updated_at: "2026-01-01T00:00:00",
  baseline: { id: 1, cash_account_id: 1, effective_on: "2026-01-01", observed_balance: 50_000, created_at: "2026-01-01T00:00:00" },
};

/** An account the user created but never began tracking — no baseline. */
const untrackedAccount: CashAccount = { ...trackedAccount, id: 2, name: "Unused", baseline: null };

/** A tracked account whose baseline began on the given date. */
function accountWithBaseline(effectiveOn: string): CashAccount {
  return {
    ...trackedAccount,
    baseline: { id: 1, cash_account_id: 1, effective_on: effectiveOn, observed_balance: 50_000, created_at: "2026-01-01T00:00:00" },
  };
}

// targetAmount=120,000, startingValue=0, exactly 12 months out, 0% return ->
// requiredMonthlyContribution = 120,000 / 12 = 10,000 exactly (no rounding).
function baseInput(overrides: Partial<GoalAffordabilityInput> = {}): GoalAffordabilityInput {
  return {
    targetAmount: 120_000,
    startingValue: 0,
    asOfDate: AS_OF_DATE,
    targetDate: "2027-08-15",
    trailingCompletedMonths: TRAILING_WINDOW,
    monthlyCashFlowResults: [],
    cashAccountsStatus: "success",
    cashAccounts: [trackedAccount],
    ...overrides,
  };
}

let nextEventId = 1;

function event(overrides: Partial<CashFlowEvent> & { month: string }): CashFlowEvent {
  const { month, ...rest } = overrides;
  return {
    id: nextEventId++,
    workspace_id: 1,
    cash_account_id: 1,
    account_name: "Everyday Cash",
    account_is_archived: false,
    transaction_type: "INCOME",
    amount: 0,
    signed_amount: 0,
    occurred_on: `${month}-10`,
    category: null,
    note: null,
    ...rest,
  } as CashFlowEvent;
}

function incomeEvent(month: string, amount: number, overrides: Partial<CashFlowEvent> = {}): CashFlowEvent {
  return event({ month, transaction_type: "INCOME", amount, signed_amount: amount, ...overrides });
}

function expenseEvent(month: string, amount: number, overrides: Partial<CashFlowEvent> = {}): CashFlowEvent {
  return event({ month, transaction_type: "EXPENSE", amount, signed_amount: -amount, ...overrides });
}

function adjustmentEvent(month: string, signedAmount: number): CashFlowEvent {
  return event({ month, transaction_type: "ADJUSTMENT", amount: signedAmount, signed_amount: signedAmount });
}

function transferEvent(month: string, signedAmount: number): CashFlowEvent {
  return event({ month, transaction_type: "TRANSFER", amount: signedAmount, signed_amount: signedAmount });
}

function successMonth(month: string, events: CashFlowEvent[]): MonthlyFetchResult {
  return { month, status: "success", events };
}

/** A month whose HTTP/server request failed — never an empty or zero month. */
function errorMonth(month: string): MonthlyFetchResult {
  return { month, status: "error", events: [] };
}

// Net cash flow per month: MONTH_1 = 10,000; MONTH_2 = 15,000; MONTH_3 = 5,000.
// Mean across all three = 10,000 -> exactly equal to requiredMonthlyContribution.
function threeMonthsAtMean10000(): MonthlyFetchResult[] {
  return [
    successMonth(MONTH_1, [incomeEvent(MONTH_1, 15_000), expenseEvent(MONTH_1, 5_000)]),
    successMonth(MONTH_2, [incomeEvent(MONTH_2, 20_000), expenseEvent(MONTH_2, 5_000)]),
    successMonth(MONTH_3, [incomeEvent(MONTH_3, 10_000), expenseEvent(MONTH_3, 5_000)]),
  ];
}

function assertNoVerdict(result: ReturnType<typeof computeGoalAffordability>): void {
  assert.notEqual(result.state, "AFFORDABLE");
  assert.notEqual(result.state, "SHORTFALL");
  assert.equal(result.observedMonthlySurplus, null);
  assert.equal(result.affordabilityGap, null);
}

// ── Single calendar anchor ───────────────────────────────────────────────────

test("C1. the trailing window is the 3 completed months of the LOCAL calendar", () => {
  // 2026-09-01T00:30+07:00 — 2026-08-31T17:30Z. The completed months are
  // June/July/August. A UTC-derived anchor would say May/June/July and drop
  // August, the most recent completed month, for the first 7 hours of every
  // month in Thailand.
  const calendar = goalAffordabilityCalendar(new Date(2026, 8, 1, 0, 30));
  assert.deepEqual(calendar.trailingCompletedMonths, ["2026-06", "2026-07", "2026-08"]);
  assert.equal(calendar.asOfDate, "2026-09-01");
});

test("C2. the window is stable across the whole local/UTC split window", () => {
  for (const hour of [0, 1, 3, 6]) {
    const calendar = goalAffordabilityCalendar(new Date(2026, 8, 1, hour, 59, 59));
    assert.deepEqual(calendar.trailingCompletedMonths, ["2026-06", "2026-07", "2026-08"], `hour ${hour}`);
    assert.equal(calendar.asOfDate, "2026-09-01", `hour ${hour}`);
  }
});

test("C3. the as-of month is never itself a completed evidence month", () => {
  for (const now of [new Date(2026, 8, 1, 0, 30), new Date(2026, 8, 15, 12, 0), new Date(2026, 8, 30, 23, 59)]) {
    const calendar = goalAffordabilityCalendar(now);
    assert.equal(calendar.trailingCompletedMonths.includes(calendar.asOfDate.slice(0, 7)), false);
    assert.equal(calendar.trailingCompletedMonths.every((month) => month < calendar.asOfDate.slice(0, 7)), true);
  }
});

test("C4. January rolls back into the previous year", () => {
  const calendar = goalAffordabilityCalendar(new Date(2026, 0, 1, 0, 30));
  assert.deepEqual(calendar.trailingCompletedMonths, ["2025-10", "2025-11", "2025-12"]);
  assert.equal(calendar.asOfDate, "2026-01-01");
});

test("C5. December closes out to a January-inclusive window", () => {
  const calendar = goalAffordabilityCalendar(new Date(2025, 11, 31, 23, 59, 59));
  assert.deepEqual(calendar.trailingCompletedMonths, ["2025-09", "2025-10", "2025-11"]);
  assert.equal(calendar.asOfDate, "2025-12-31");
});

test("C6. leap-year February is a normal completed month and a valid as-of day", () => {
  assert.deepEqual(
    goalAffordabilityCalendar(new Date(2024, 2, 1, 0, 30)).trailingCompletedMonths,
    ["2023-12", "2024-01", "2024-02"],
  );
  const leapDay = goalAffordabilityCalendar(new Date(2024, 1, 29, 23, 30));
  assert.equal(leapDay.asOfDate, "2024-02-29");
  assert.deepEqual(leapDay.trailingCompletedMonths, ["2023-11", "2023-12", "2024-01"]);
});

// ── Verdicts ─────────────────────────────────────────────────────────────────

test("1. surplus > required -> AFFORDABLE", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_1, [incomeEvent(MONTH_1, 17_000), expenseEvent(MONTH_1, 5_000)]),
      successMonth(MONTH_2, [incomeEvent(MONTH_2, 20_000), expenseEvent(MONTH_2, 5_000)]),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 14_000), expenseEvent(MONTH_3, 5_000)]),
    ],
  }));
  assert.equal(result.state, "AFFORDABLE");
  assert.equal(result.observedMonthlySurplus, 12_000);
  assert.equal(result.requiredMonthlyContribution, 10_000);
});

test("2. surplus == required (boundary) -> AFFORDABLE", () => {
  const result = computeGoalAffordability(baseInput({ monthlyCashFlowResults: threeMonthsAtMean10000() }));
  assert.equal(result.state, "AFFORDABLE");
  assert.equal(result.observedMonthlySurplus, 10_000);
  assert.equal(result.requiredMonthlyContribution, 10_000);
  assert.equal(result.affordabilityGap, 0);
});

test("3. surplus < required -> SHORTFALL", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_1, [incomeEvent(MONTH_1, 10_000), expenseEvent(MONTH_1, 5_000)]),
      successMonth(MONTH_2, [incomeEvent(MONTH_2, 12_000), expenseEvent(MONTH_2, 5_000)]),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 11_000), expenseEvent(MONTH_3, 5_000)]),
    ],
  }));
  assert.equal(result.state, "SHORTFALL");
  assert.equal(result.observedMonthlySurplus, 6_000);
  assert.equal(result.affordabilityGap, -4_000);
});

test("4. negative surplus -> SHORTFALL", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_1, [incomeEvent(MONTH_1, 2_000), expenseEvent(MONTH_1, 9_000)]),
      successMonth(MONTH_2, [incomeEvent(MONTH_2, 2_000), expenseEvent(MONTH_2, 9_000)]),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 2_000), expenseEvent(MONTH_3, 9_000)]),
    ],
  }));
  assert.equal(result.state, "SHORTFALL");
  assert.equal(result.observedMonthlySurplus, -7_000);
});

test("5. already reached -> NO_CONTRIBUTION_REQUIRED, takes precedence over zero evidence", () => {
  const result = computeGoalAffordability(baseInput({
    startingValue: 200_000,
    monthlyCashFlowResults: [],
  }));
  assert.equal(result.state, "NO_CONTRIBUTION_REQUIRED");
  assert.equal(result.requiredMonthlyContribution, 0);
  assert.equal(result.evidenceMonthCount, 0);
});

test("5b. already reached also takes precedence over a technical retrieval failure", () => {
  const result = computeGoalAffordability(baseInput({
    startingValue: 200_000,
    monthlyCashFlowResults: TRAILING_WINDOW.map(errorMonth),
  }));
  assert.equal(result.state, "NO_CONTRIBUTION_REQUIRED");
});

test("6. no target date -> INSUFFICIENT_DATA with goalWhatIf's own reason", () => {
  const result = computeGoalAffordability(baseInput({ targetDate: null, monthlyCashFlowResults: threeMonthsAtMean10000() }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "REQUIRED_SIDE_INVALID");
  assert.equal(result.reason, "A saved target date is required for this calculation.");
  assert.equal(result.requiredMonthlyContribution, null);
});

test("7. overdue target date -> INSUFFICIENT_DATA with goalWhatIf's own reason", () => {
  const result = computeGoalAffordability(baseInput({ targetDate: "2026-01-01", monthlyCashFlowResults: threeMonthsAtMean10000() }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "REQUIRED_SIDE_INVALID");
  assert.equal(result.reason, "The saved target date has passed.");
});

test("8. too-short horizon -> INSUFFICIENT_DATA with goalWhatIf's own reason", () => {
  const result = computeGoalAffordability(baseInput({ targetDate: "2026-08-20", monthlyCashFlowResults: threeMonthsAtMean10000() }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reason, "No completed monthly contribution periods are available before the saved target date.");
});

test("9. zero completed evidence months -> INSUFFICIENT_DATA, never fabricates a number", () => {
  const result = computeGoalAffordability(baseInput({ monthlyCashFlowResults: [] }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "NO_RECORDED_MONTH");
  assert.equal(result.reason, "No completed month of recorded cash flow is available yet.");
  assert.equal(result.observedMonthlySurplus, null);
  assert.equal(result.evidenceMonthCount, 0);
});

// ── Genuine sparse history (retrieval succeeded) ─────────────────────────────

test("10. one genuinely recorded month -> uses exactly that one month", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [successMonth(MONTH_3, [incomeEvent(MONTH_3, 14_000), expenseEvent(MONTH_3, 5_000)])],
  }));
  assert.equal(result.state, "SHORTFALL");
  assert.equal(result.evidenceMonthCount, 1);
  assert.deepEqual(result.evidenceMonths, [MONTH_3]);
  assert.equal(result.observedMonthlySurplus, 9_000);
});

test("11. two genuinely recorded months -> averages exactly those two", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_2, [incomeEvent(MONTH_2, 13_000), expenseEvent(MONTH_2, 5_000)]),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 17_000), expenseEvent(MONTH_3, 5_000)]),
    ],
  }));
  assert.equal(result.state, "AFFORDABLE");
  assert.equal(result.evidenceMonthCount, 2);
  assert.equal(result.observedMonthlySurplus, 10_000);
});

test("12. three completed evidence months -> averages exactly those three", () => {
  const result = computeGoalAffordability(baseInput({ monthlyCashFlowResults: threeMonthsAtMean10000() }));
  assert.equal(result.evidenceMonthCount, 3);
  assert.deepEqual(result.evidenceMonths, [MONTH_1, MONTH_2, MONTH_3]);
  assert.equal(result.observedMonthlySurplus, 10_000);
});

test("13. a missing month inside the trailing window is excluded, never fabricated as zero", () => {
  const twoOfThree = threeMonthsAtMean10000().filter((entry) => entry.month !== MONTH_2);
  const result = computeGoalAffordability(baseInput({ monthlyCashFlowResults: twoOfThree }));
  assert.equal(result.evidenceMonthCount, 2);
  assert.deepEqual(result.evidenceMonths, [MONTH_1, MONTH_3]);
  // Mean of MONTH_1 (10,000) and MONTH_3 (5,000) only -> 7,500. If the
  // missing MONTH_2 had been fabricated as zero, this would be 5,000.
  assert.equal(result.observedMonthlySurplus, 7_500);
});

// ── Technical retrieval failure fails closed (never sparse history) ──────────

test("14. one failed month among three fails closed — no AFFORDABLE/SHORTFALL claim", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_1, [incomeEvent(MONTH_1, 15_000), expenseEvent(MONTH_1, 5_000)]),
      errorMonth(MONTH_2),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 10_000), expenseEvent(MONTH_3, 5_000)]),
    ],
  }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "CASH_FLOW_UNAVAILABLE");
  assert.equal(result.reason, "Cash Flow data could not be fully loaded. Try again.");
  assertNoVerdict(result);
});

test("15. a failed month cannot be rescued by two comfortably positive months", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      errorMonth(MONTH_1),
      successMonth(MONTH_2, [incomeEvent(MONTH_2, 90_000), expenseEvent(MONTH_2, 5_000)]),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 90_000), expenseEvent(MONTH_3, 5_000)]),
    ],
  }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "CASH_FLOW_UNAVAILABLE");
  assertNoVerdict(result);
});

test("16. a failed month cannot produce a SHORTFALL claim from two negative months either", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      errorMonth(MONTH_1),
      successMonth(MONTH_2, [incomeEvent(MONTH_2, 1_000), expenseEvent(MONTH_2, 9_000)]),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 1_000), expenseEvent(MONTH_3, 9_000)]),
    ],
  }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "CASH_FLOW_UNAVAILABLE");
  assertNoVerdict(result);
});

test("17. all three months failing is a retrieval failure, not an absence of history", () => {
  const result = computeGoalAffordability(baseInput({ monthlyCashFlowResults: TRAILING_WINDOW.map(errorMonth) }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "CASH_FLOW_UNAVAILABLE");
  assert.notEqual(result.reason, "No completed month of recorded cash flow is available yet.");
  assertNoVerdict(result);
});

test("18. a failed month OUTSIDE the trailing window is ignored, not a fail-closed trigger", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [...threeMonthsAtMean10000(), errorMonth(MONTH_MINUS_4)],
  }));
  assert.equal(result.state, "AFFORDABLE");
  assert.equal(result.evidenceMonthCount, 3);
});

test("19. a failed cash-account list fails closed rather than assuming no population", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccountsStatus: "error",
    cashAccounts: [],
    monthlyCashFlowResults: threeMonthsAtMean10000(),
  }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "CASH_ACCOUNTS_UNAVAILABLE");
  assertNoVerdict(result);
});

// ── Evidence population gate ─────────────────────────────────────────────────

test("20. no tracked population + three successful empty months -> INSUFFICIENT_DATA, not ฿0", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [],
    monthlyCashFlowResults: TRAILING_WINDOW.map((month) => successMonth(month, [])),
  }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "NO_TRACKED_CASH_FLOW");
  assert.equal(result.reason, "Not enough recorded cash flow to assess affordability yet.");
  assertNoVerdict(result);
});

test("21. an account that was never begun (no baseline) is not a tracked population", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [untrackedAccount],
    monthlyCashFlowResults: TRAILING_WINDOW.map((month) => successMonth(month, [])),
  }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "NO_TRACKED_CASH_FLOW");
});

test("22. a tracked population makes a successful empty month a legitimate zero-flow month", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [trackedAccount],
    monthlyCashFlowResults: [successMonth(MONTH_3, [])],
  }));
  assert.equal(result.state, "SHORTFALL");
  assert.equal(result.evidenceMonthCount, 1);
  assert.equal(result.observedMonthlySurplus, 0);
  assert.equal(result.affordabilityGap, -10_000);
});

test("23. a zero-flow month averages in as a real zero alongside recorded months", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_1, [incomeEvent(MONTH_1, 20_000), expenseEvent(MONTH_1, 5_000)]),
      successMonth(MONTH_2, []),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 20_000), expenseEvent(MONTH_3, 5_000)]),
    ],
  }));
  // (15,000 + 0 + 15,000) / 3 = 10,000 — the empty month is a divisor, unlike
  // a missing month (test 13) or a failed month (test 14).
  assert.equal(result.evidenceMonthCount, 3);
  assert.equal(result.observedMonthlySurplus, 10_000);
});

test("24. recorded events prove a population even when the account list cannot (archived-only history)", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [],
    monthlyCashFlowResults: [
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 14_000, { account_is_archived: true }), expenseEvent(MONTH_3, 5_000, { account_is_archived: true })]),
    ],
  }));
  assert.equal(result.state, "SHORTFALL");
  assert.equal(result.observedMonthlySurplus, 9_000);
});

// ── W1: pre-tracking months are not a measured zero ─────────────────────────
// MONTH_1=2026-05 (M-3), MONTH_2=2026-06 (M-2), MONTH_3=2026-07 (M-1, most
// recent completed month). required contribution is 10,000/month throughout.

test("W1-1. tracking starts in M-1 (July): M-2/M-3 empty pre-tracking months are excluded, not fabricated as zero", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [accountWithBaseline("2026-07-01")],
    monthlyCashFlowResults: [
      successMonth(MONTH_1, []),
      successMonth(MONTH_2, []),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 21_000)]),
    ],
  }));
  // Diluted (wrong) result would be (0 + 0 + 21,000) / 3 = 7,000 -> SHORTFALL.
  assert.equal(result.state, "AFFORDABLE");
  assert.equal(result.evidenceMonthCount, 1);
  assert.deepEqual(result.evidenceMonths, [MONTH_3]);
  assert.equal(result.observedMonthlySurplus, 21_000);
  assert.equal(result.affordabilityGap, 11_000);
});

test("W1-2. tracking starts in M-2 (June): M-3 (May) is excluded, June+July average the eligible pair", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [accountWithBaseline("2026-06-01")],
    monthlyCashFlowResults: [
      successMonth(MONTH_1, []),
      successMonth(MONTH_2, [incomeEvent(MONTH_2, 12_000)]),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 8_000)]),
    ],
  }));
  assert.equal(result.evidenceMonthCount, 2);
  assert.deepEqual(result.evidenceMonths, [MONTH_2, MONTH_3]);
  assert.equal(result.observedMonthlySurplus, 10_000);
  assert.equal(result.state, "AFFORDABLE");
});

test("W1-3. tracking starts before the entire window -> all three successful months remain eligible", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [accountWithBaseline("2026-04-01")],
    monthlyCashFlowResults: threeMonthsAtMean10000(),
  }));
  assert.equal(result.evidenceMonthCount, 3);
  assert.deepEqual(result.evidenceMonths, [MONTH_1, MONTH_2, MONTH_3]);
  assert.equal(result.observedMonthlySurplus, 10_000);
});

test("W1-4. a post-tracking successful empty month still enters the denominator as a real zero", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [accountWithBaseline("2026-06-01")],
    monthlyCashFlowResults: [
      successMonth(MONTH_1, []),
      successMonth(MONTH_2, []),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 21_000)]),
    ],
  }));
  // May is pre-tracking (excluded); June is post-tracking and genuinely empty
  // (a real zero, not omitted): (0 + 21,000) / 2 = 10,500.
  assert.equal(result.evidenceMonthCount, 2);
  assert.deepEqual(result.evidenceMonths, [MONTH_2, MONTH_3]);
  assert.equal(result.observedMonthlySurplus, 10_500);
  assert.equal(result.state, "AFFORDABLE");
});

test("W1-5. a real historical event rescues an otherwise pre-baseline month", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [accountWithBaseline("2026-07-01")],
    monthlyCashFlowResults: [
      successMonth(MONTH_1, [incomeEvent(MONTH_1, 5_000)]),
      successMonth(MONTH_2, []),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 21_000)]),
    ],
  }));
  // May predates the July baseline but holds a real event, so it is rescued.
  // June predates the baseline and holds no event, so it stays excluded.
  assert.equal(result.evidenceMonthCount, 2);
  assert.deepEqual(result.evidenceMonths, [MONTH_1, MONTH_3]);
  assert.equal(result.observedMonthlySurplus, 13_000);
});

test("W1-6. archived-only historical event remains evidence even with no active tracked account, while the empty siblings stay excluded", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [],
    monthlyCashFlowResults: [
      successMonth(MONTH_1, []),
      successMonth(MONTH_2, [incomeEvent(MONTH_2, 5_000, { account_is_archived: true })]),
      successMonth(MONTH_3, []),
    ],
  }));
  assert.equal(result.evidenceMonthCount, 1);
  assert.deepEqual(result.evidenceMonths, [MONTH_2]);
  assert.equal(result.observedMonthlySurplus, 5_000);
  assert.equal(result.state, "SHORTFALL");
});

test("W1-7. a baseline effective mid-month does not admit that partial month — only the following month counts", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [accountWithBaseline("2026-07-15")],
    monthlyCashFlowResults: [
      successMonth(MONTH_1, []),
      successMonth(MONTH_2, []),
      successMonth(MONTH_3, []),
    ],
  }));
  // July's baseline is mid-month, so July itself (`2026-07-01 < 2026-07-15`)
  // does not qualify, and it holds no historical events to rescue it either.
  // No window month is eligible.
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "NO_TRACKED_CASH_FLOW");
  assert.equal(result.evidenceMonthCount, 0);
});

test("W1-8. a technical retrieval failure still fails closed even with a tracking baseline established", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [accountWithBaseline("2026-07-01")],
    monthlyCashFlowResults: [
      errorMonth(MONTH_1),
      successMonth(MONTH_2, []),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 21_000)]),
    ],
  }));
  assert.equal(result.state, "INSUFFICIENT_DATA");
  assert.equal(result.reasonCode, "CASH_FLOW_UNAVAILABLE");
  assertNoVerdict(result);
});

// ── Cash Flow transaction-type semantics ─────────────────────────────────────

test("25. ADJUSTMENT events do not affect observed surplus", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 10_000), expenseEvent(MONTH_3, 0), adjustmentEvent(MONTH_3, 999_999)]),
    ],
  }));
  assert.equal(result.observedMonthlySurplus, 10_000);
});

test("26. TRANSFER events do not affect observed surplus", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 10_000), expenseEvent(MONTH_3, 0), transferEvent(MONTH_3, 500_000)]),
    ],
  }));
  assert.equal(result.observedMonthlySurplus, 10_000);
});

test("27. an ADJUSTMENT/TRANSFER-only month is zero economic flow, not absent evidence", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [trackedAccount],
    monthlyCashFlowResults: [
      successMonth(MONTH_3, [adjustmentEvent(MONTH_3, 40_000), transferEvent(MONTH_3, 60_000)]),
    ],
  }));
  assert.equal(result.state, "SHORTFALL");
  assert.equal(result.evidenceMonthCount, 1);
  assert.equal(result.observedMonthlySurplus, 0);
});

test("28. ADJUSTMENT/TRANSFER rows are themselves proof of a recording population", () => {
  const result = computeGoalAffordability(baseInput({
    cashAccounts: [],
    monthlyCashFlowResults: [successMonth(MONTH_3, [transferEvent(MONTH_3, 60_000)])],
  }));
  assert.equal(result.state, "SHORTFALL");
  assert.equal(result.observedMonthlySurplus, 0);
});

test("29. archived-account historical events remain included, matching the /cash-flow contract", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 5_000, { account_is_archived: true })]),
    ],
  }));
  assert.equal(result.observedMonthlySurplus, 5_000);
});

// ── Fixed trailing window ────────────────────────────────────────────────────

test("30. the current (incomplete) month never participates even if supplied", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      ...threeMonthsAtMean10000(),
      successMonth(CURRENT_MONTH, [incomeEvent(CURRENT_MONTH, 1_000_000)]),
    ],
  }));
  assert.equal(result.evidenceMonthCount, 3);
  assert.equal(result.observedMonthlySurplus, 10_000);
});

test("31. R4 — month -4 never backfills a missing month inside the window", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      // Month -4 is available and would raise the mean if it were used.
      successMonth(MONTH_MINUS_4, [incomeEvent(MONTH_MINUS_4, 500_000)]),
      successMonth(MONTH_1, [incomeEvent(MONTH_1, 15_000), expenseEvent(MONTH_1, 5_000)]),
      // MONTH_2 is absent entirely.
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 10_000), expenseEvent(MONTH_3, 5_000)]),
    ],
  }));
  assert.equal(result.evidenceMonthCount, 2);
  assert.deepEqual(result.evidenceMonths, [MONTH_1, MONTH_3]);
  // Mean of MONTH_1 (10,000) and MONTH_3 (5,000) only.
  assert.equal(result.observedMonthlySurplus, 7_500);
});

test("32. the evaluated months are exactly the caller's window, never re-derived", () => {
  const shiftedWindow = ["2026-02", "2026-03", "2026-04"];
  const result = computeGoalAffordability(baseInput({
    trailingCompletedMonths: shiftedWindow,
    monthlyCashFlowResults: [
      ...threeMonthsAtMean10000(),
      successMonth("2026-03", [incomeEvent("2026-03", 21_000), expenseEvent("2026-03", 5_000)]),
    ],
  }));
  assert.deepEqual(result.evidenceMonths, ["2026-03"]);
  assert.equal(result.observedMonthlySurplus, 16_000);
});

// ── Composition ──────────────────────────────────────────────────────────────

test("33. required contribution always uses a 0% return assumption", () => {
  const result = computeGoalAffordability(baseInput({ monthlyCashFlowResults: threeMonthsAtMean10000() }));
  const direct = computeRequiredMonthlyContribution({
    targetAmount: 120_000,
    startingValue: 0,
    annualReturnPct: 0,
    asOfDate: AS_OF_DATE,
    targetDate: "2027-08-15",
  });
  assert.equal(direct.valid, true);
  assert.equal(result.requiredMonthlyContribution, direct.valid ? direct.requiredMonthlyContribution : null);
});

test("34. affordability gap arithmetic is observedMonthlySurplus - requiredMonthlyContribution", () => {
  const result = computeGoalAffordability(baseInput({
    monthlyCashFlowResults: [
      successMonth(MONTH_1, [incomeEvent(MONTH_1, 10_000), expenseEvent(MONTH_1, 5_000)]),
      successMonth(MONTH_2, [incomeEvent(MONTH_2, 12_000), expenseEvent(MONTH_2, 5_000)]),
      successMonth(MONTH_3, [incomeEvent(MONTH_3, 11_000), expenseEvent(MONTH_3, 5_000)]),
    ],
  }));
  assert.equal(result.observedMonthlySurplus, 6_000);
  assert.equal(result.requiredMonthlyContribution, 10_000);
  assert.equal(result.affordabilityGap, 6_000 - 10_000);
});
