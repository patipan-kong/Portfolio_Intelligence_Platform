// Recorded Expense Coverage — factual, evidence-only workspace intelligence.
//
// This is NOT an emergency-fund target, financial advice, a health/status
// score, or a liquidity classifier. It is two separately-legible facts:
//   Tracked cash balance            — sum of active, tracked CashAccount.balance
//   Average recorded monthly expense — mean EXPENSE total over the trailing
//                                      3 calendar months with recorded evidence
// and their ratio. The repository cannot prove real-world spending is fully
// captured, so expense evidence is always "recorded", never "observed" or
// "complete". See docs review: earliest-baseline gating is a PRESENCE gate
// ("recorded evidence could exist by this month"), never a completeness claim.

import type { CashAccount, CashFlowEvent } from "./api";
import { aggregateMonthlyCashFlow, currentMonthKey, shiftMonth } from "./cashFlow.ts";

export type CashAccountsFetchStatus = "success" | "error";

export interface CoveragePopulation {
  /** False when account evidence failed to load or any tracked-active account is invalid (non-THB, non-finite, or negative balance). */
  evidenceAvailable: boolean;
  /** null whenever evidenceAvailable is false — never a stand-in for zero. */
  trackedCash: number | null;
  untrackedActiveAccountCount: number;
  /** Trailing-3-month window, filtered to months on/after the earliest tracked-active baseline. A presence gate only — not a completeness claim. */
  recordedMonths: string[];
  /** Count of tracked-active accounts whose baseline.effective_on falls within a recorded month. */
  accountsBeganDuringRecordedPeriod: number;
}

/**
 * Tracked-active accounts (`!is_archived && baseline != null`) are the same
 * population used for both the numerator (tracked cash) and the recorded-
 * month presence gate, so neither side claims more evidence than the other.
 */
export function computeCoveragePopulation(
  accountsStatus: CashAccountsFetchStatus,
  accounts: CashAccount[],
  now: Date,
): CoveragePopulation {
  const activeAccounts = accounts.filter((account) => !account.is_archived);
  const trackedActiveAccounts = activeAccounts.filter((account) => account.baseline != null);
  const untrackedActiveAccountCount = activeAccounts.length - trackedActiveAccounts.length;

  const invalidCount = trackedActiveAccounts.filter(
    (account) => account.currency !== "THB" || !Number.isFinite(account.balance) || account.balance < 0,
  ).length;
  const evidenceAvailable = accountsStatus === "success" && invalidCount === 0;

  const trackedCash = evidenceAvailable
    ? trackedActiveAccounts.reduce((sum, account) => sum + account.balance, 0)
    : null;

  let recordedMonths: string[] = [];
  let accountsBeganDuringRecordedPeriod = 0;
  if (evidenceAvailable && trackedActiveAccounts.length > 0) {
    const anchor = currentMonthKey(now);
    const windowMonths = [shiftMonth(anchor, -3), shiftMonth(anchor, -2), shiftMonth(anchor, -1)];
    const earliestBaseline = trackedActiveAccounts
      .map((account) => account.baseline!.effective_on)
      .reduce((min, effectiveOn) => (effectiveOn < min ? effectiveOn : min));
    recordedMonths = windowMonths.filter((month) => `${month}-01` >= earliestBaseline);

    const recordedMonthSet = new Set(recordedMonths);
    accountsBeganDuringRecordedPeriod = trackedActiveAccounts.filter((account) =>
      recordedMonthSet.has(account.baseline!.effective_on.slice(0, 7)),
    ).length;
  }

  return { evidenceAvailable, trackedCash, untrackedActiveAccountCount, recordedMonths, accountsBeganDuringRecordedPeriod };
}

export interface MonthlyFetchResult {
  month: string;
  status: "success" | "error";
  /** Only meaningful when status is "success". */
  events: CashFlowEvent[];
}

export type CoverageStatus = "AVAILABLE" | "NO_RECORDED_EXPENSE" | "INSUFFICIENT_EVIDENCE" | "UNAVAILABLE";

export interface RecordedExpenseCoverageResult {
  status: CoverageStatus;
  trackedCash: number | null;
  untrackedActiveAccountCount: number;
  recordedMonths: string[];
  accountsBeganDuringRecordedPeriod: number;
  /** null whenever status is not AVAILABLE or NO_RECORDED_EXPENSE. */
  averageRecordedMonthlyExpense: number | null;
  /** null whenever status is not AVAILABLE. No cap, no clamp. */
  coverageMonths: number | null;
  /** True if any recorded-month EXPENSE event belongs to an archived account. */
  hasArchivedAccountExpenses: boolean;
}

/**
 * `monthlyResults` must contain exactly one entry per `population.recordedMonths`
 * entry, or the result fails closed to UNAVAILABLE (a partial subset is never
 * averaged). Expense totals are read from `aggregateMonthlyCashFlow` only —
 * this never re-derives Cash Flow transaction math.
 */
export function computeRecordedExpenseCoverage(
  population: CoveragePopulation,
  monthlyResults: MonthlyFetchResult[],
): RecordedExpenseCoverageResult {
  const { evidenceAvailable, trackedCash, untrackedActiveAccountCount, recordedMonths, accountsBeganDuringRecordedPeriod } = population;
  const base = { trackedCash, untrackedActiveAccountCount, recordedMonths, accountsBeganDuringRecordedPeriod };

  if (!evidenceAvailable) {
    return { ...base, status: "UNAVAILABLE", averageRecordedMonthlyExpense: null, coverageMonths: null, hasArchivedAccountExpenses: false };
  }
  if (recordedMonths.length === 0) {
    return { ...base, status: "INSUFFICIENT_EVIDENCE", averageRecordedMonthlyExpense: null, coverageMonths: null, hasArchivedAccountExpenses: false };
  }
  const monthsFetched = new Set(monthlyResults.map((result) => result.month));
  const complete = recordedMonths.every((month) => monthsFetched.has(month));
  const anyFailed = monthlyResults.some((result) => result.status === "error");
  if (!complete || anyFailed) {
    return { ...base, status: "UNAVAILABLE", averageRecordedMonthlyExpense: null, coverageMonths: null, hasArchivedAccountExpenses: false };
  }

  let totalExpense = 0;
  let hasArchivedAccountExpenses = false;
  for (const result of monthlyResults) {
    const summary = aggregateMonthlyCashFlow(result.events, result.month);
    totalExpense += summary.expenses;
    if (summary.events.some((event) => event.transaction_type === "EXPENSE" && event.account_is_archived)) {
      hasArchivedAccountExpenses = true;
    }
  }
  const averageRecordedMonthlyExpense = totalExpense / recordedMonths.length;

  if (averageRecordedMonthlyExpense === 0) {
    return { ...base, status: "NO_RECORDED_EXPENSE", averageRecordedMonthlyExpense: 0, coverageMonths: null, hasArchivedAccountExpenses };
  }

  return {
    ...base,
    status: "AVAILABLE",
    averageRecordedMonthlyExpense,
    coverageMonths: (trackedCash as number) / averageRecordedMonthlyExpense,
    hasArchivedAccountExpenses,
  };
}

export interface CoverageGap {
  targetMonths: number;
  targetAmount: number;
  /** trackedCash - targetAmount. Negative = shortfall, positive = surplus, zero = exactly at target. */
  gapAmount: number;
}

/**
 * Derives a THB target and gap from a user-supplied months target — never
 * a system-suggested one. Only defined when coverage evidence is AVAILABLE;
 * insufficient or unavailable evidence must never be interpreted as zero
 * expense or zero tracked cash, so this returns null rather than fabricate
 * a target/gap in those states. The saved target itself is still valid to
 * display even when this returns null.
 */
export function computeCoverageGap(
  targetMonths: number | null,
  coverage: RecordedExpenseCoverageResult,
): CoverageGap | null {
  if (targetMonths === null) return null;
  if (coverage.status !== "AVAILABLE" || coverage.averageRecordedMonthlyExpense === null || coverage.trackedCash === null) {
    return null;
  }
  const targetAmount = targetMonths * coverage.averageRecordedMonthlyExpense;
  return { targetMonths, targetAmount, gapAmount: coverage.trackedCash - targetAmount };
}
