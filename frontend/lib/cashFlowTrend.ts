// Cash Flow Trend — factual, historical multi-month composition over the
// existing Cash Flow report. This is NOT a forecast, NOT recurring-expense
// detection, and NOT a Goal-attribution or financial-health signal: it
// answers only "how has monthly Income, Expenses, and Net Cash Flow changed
// over recent completed months?" using the same evidence and math as the
// single-month report.
//
// Each requested month resolves to exactly one status:
//   AVAILABLE    — tracking evidence eligible, request succeeded. Values may
//                   be genuinely zero.
//   PRE_TRACKING — the month precedes the earliest tracked-active baseline
//                   (a presence gate, same concept as Recorded Expense
//                   Coverage's earliest-baseline filter, generalized to an
//                   arbitrary trailing window).
//   UNAVAILABLE  — the month should be observable but either the account
//                   evidence itself failed to load, or that month's Cash
//                   Flow report request failed.
// PRE_TRACKING and UNAVAILABLE values are always null — never a fabricated
// zero standing in for missing or failed evidence.

import type { CashAccount } from "./api.ts";
import { aggregateMonthlyCashFlow, currentMonthKey, shiftMonth } from "./cashFlow.ts";
import type { CashAccountsFetchStatus, MonthlyFetchResult } from "./emergencyFund.ts";

export const TREND_WINDOW_SIZES = [3, 6, 12] as const;
export type TrendWindowSize = (typeof TREND_WINDOW_SIZES)[number];
export const DEFAULT_TREND_WINDOW_SIZE: TrendWindowSize = 6;

function roundCurrency(value: number): number {
  return Number(value.toFixed(2));
}

/** Trailing completed months, oldest to newest. The anchor (current) month is never included. */
export function trendMonths(anchor: string, windowSize: TrendWindowSize): string[] {
  const months: string[] = [];
  for (let offset = windowSize; offset >= 1; offset -= 1) {
    months.push(shiftMonth(anchor, -offset));
  }
  return months;
}

export interface TrendPopulation {
  /** False only when the account evidence request itself failed — distinct from "no tracking exists yet". */
  evidenceAvailable: boolean;
  /** Every month in the requested trailing window, oldest to newest. */
  requestedMonths: string[];
  /** Subset of requestedMonths on/after the earliest tracked-active baseline. A presence gate, not a completeness claim. */
  eligibleMonths: string[];
}

/**
 * Tracked-active accounts (`!is_archived && baseline != null`) gate month
 * eligibility the same way Recorded Expense Coverage gates its window,
 * generalized from a fixed trailing-3 window to an arbitrary trailing size.
 * Unlike Coverage, this never validates balance/currency: Trend never reads
 * account balances, only baseline dates, so that check would be meaningless
 * here.
 */
export function computeTrendPopulation(
  accountsStatus: CashAccountsFetchStatus,
  accounts: CashAccount[],
  windowSize: TrendWindowSize,
  now: Date,
): TrendPopulation {
  const anchor = currentMonthKey(now);
  const requestedMonths = trendMonths(anchor, windowSize);
  const evidenceAvailable = accountsStatus === "success";

  if (!evidenceAvailable) {
    return { evidenceAvailable, requestedMonths, eligibleMonths: [] };
  }

  const trackedActiveAccounts = accounts.filter((account) => !account.is_archived && account.baseline != null);
  if (trackedActiveAccounts.length === 0) {
    return { evidenceAvailable, requestedMonths, eligibleMonths: [] };
  }

  const earliestBaseline = trackedActiveAccounts
    .map((account) => account.baseline!.effective_on)
    .reduce((min, effectiveOn) => (effectiveOn < min ? effectiveOn : min));
  const eligibleMonths = requestedMonths.filter((month) => `${month}-01` >= earliestBaseline);

  return { evidenceAvailable, requestedMonths, eligibleMonths };
}

export type TrendPointStatus = "AVAILABLE" | "PRE_TRACKING" | "UNAVAILABLE";

export interface CashFlowTrendPoint {
  month: string;
  status: TrendPointStatus;
  /** Null unless status is AVAILABLE. */
  income: number | null;
  expenses: number | null;
  netCashFlow: number | null;
}

export interface CashFlowTrendSummary {
  requestedMonths: number;
  availableMonths: number;
  /** Null when availableMonths is 0 — never averaged over a partial or fabricated set. */
  averageIncome: number | null;
  averageExpenses: number | null;
  averageNetCashFlow: number | null;
  /** Net Cash Flow of the most recent AVAILABLE month, or null if none. */
  latestAvailableNetCashFlow: number | null;
}

export interface CashFlowTrendResult {
  points: CashFlowTrendPoint[];
  summary: CashFlowTrendSummary;
}

/**
 * `monthlyResults` need not cover every eligible month: a missing or
 * `status: "error"` entry for an eligible month renders that single point
 * UNAVAILABLE without affecting any other month — unlike Recorded Expense
 * Coverage, a chart of independent monthly points has no reason to fail
 * closed as a whole on one month's technical failure.
 */
export function computeCashFlowTrend(
  population: TrendPopulation,
  monthlyResults: MonthlyFetchResult[],
): CashFlowTrendResult {
  const { evidenceAvailable, requestedMonths, eligibleMonths } = population;
  const eligibleSet = new Set(eligibleMonths);
  const resultByMonth = new Map(monthlyResults.map((result) => [result.month, result]));

  const points: CashFlowTrendPoint[] = requestedMonths.map((month) => {
    if (!evidenceAvailable) {
      return { month, status: "UNAVAILABLE", income: null, expenses: null, netCashFlow: null };
    }
    if (!eligibleSet.has(month)) {
      return { month, status: "PRE_TRACKING", income: null, expenses: null, netCashFlow: null };
    }
    const result = resultByMonth.get(month);
    if (!result || result.status === "error") {
      return { month, status: "UNAVAILABLE", income: null, expenses: null, netCashFlow: null };
    }
    const monthly = aggregateMonthlyCashFlow(result.events, month);
    return { month, status: "AVAILABLE", income: monthly.income, expenses: monthly.expenses, netCashFlow: monthly.netCashFlow };
  });

  const availablePoints = points.filter((point) => point.status === "AVAILABLE");
  const availableMonths = availablePoints.length;
  const average = (selector: (point: CashFlowTrendPoint) => number | null) =>
    availableMonths === 0 ? null : roundCurrency(availablePoints.reduce((sum, point) => sum + (selector(point) ?? 0), 0) / availableMonths);

  return {
    points,
    summary: {
      requestedMonths: requestedMonths.length,
      availableMonths,
      averageIncome: average((point) => point.income),
      averageExpenses: average((point) => point.expenses),
      averageNetCashFlow: average((point) => point.netCashFlow),
      latestAvailableNetCashFlow: availablePoints.length > 0 ? availablePoints[availablePoints.length - 1].netCashFlow : null,
    },
  };
}
