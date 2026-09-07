// Total Assets History — pure composition of the existing Investment Wealth
// History date spine (wealthHistory.ts) with the existing Cash As-Of
// contract (services/cash_account_ledger.py::cash_balance_as_of, read via
// GET /cash-accounts/{id}/as-of). No new backend endpoint, no new schema,
// no daily calendar series: every date this module can ever report comes
// from an Investment Wealth History point that already exists.
//
// Total Assets(d) = Investment Assets(d) + External Cash(d). Investment
// Assets is PortfolioSnapshot.total_value as already aggregated by
// computeWealthHistory — it already includes brokerage cash, so this module
// never adds a portfolio's cash a second time.
//
// Cash lifecycle discipline mirrors the backend's own As-Of contract:
// - a CashAccount not yet created by date d is simply not expected;
// - a CashAccount created before d but with no available As-Of evidence
//   (no baseline yet, or a failed/missing request) is expected but
//   unavailable — it keeps the date incomplete, never a fabricated zero;
// - an archived CashAccount's historical evidence remains fully included —
//   archive state is never read here and never implies zero.
//
// This module never reads a CashAccount's current `balance` — only the
// already-resolved As-Of evidence passed in by the caller (Section I:
// accepts resolved evidence, performs no network calls itself).

import type { AssetLoadStatus } from "./totalAssets";
import type { CashAccountBalanceAsOf } from "./api";
import type { WealthHistoryPoint } from "./wealthHistory";

const DISPLAY_TZ = "Asia/Bangkok";
// Same lifecycle-key convention as wealthHistory.ts/combinedPerformance.ts's
// own (unexported) createdDateKey — kept local for the same cross-runtime
// test-resolution reason those modules document.
const dateKeyFormatter = new Intl.DateTimeFormat("en-CA", {
  timeZone: DISPLAY_TZ,
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
});

function createdDateKey(isoDate: string): string {
  return dateKeyFormatter.format(new Date(isoDate));
}

export interface TotalAssetsHistoryCashAccount {
  id: number;
  created_at: string;
}

/** Already-resolved Cash As-Of evidence for one (account, date) pair. A missing map entry — never fetched, or a failed request — is treated identically to `available: false`: expected but unavailable. */
export type CashAsOfEvidence = Pick<CashAccountBalanceAsOf, "balance" | "available">;

export interface TotalAssetsHistoryPoint {
  date: string; // "YYYY-MM-DD", matches the Investment Wealth History spine
  investmentAssets: number | null;
  investmentContributingCount: number;
  investmentExpectedCount: number;
  investmentComplete: boolean;
  externalCash: number | null;
  cashContributingCount: number;
  cashExpectedCount: number;
  cashComplete: boolean;
  /** Only non-null when both investment and cash sides are complete for this date. */
  totalAssets: number | null;
  complete: boolean;
}

export interface TotalAssetsHistoryDelta {
  from: TotalAssetsHistoryPoint;
  to: TotalAssetsHistoryPoint;
  change: number;
  /** null when `from.totalAssets` is 0 — a percentage change is undefined, not infinite. */
  changePct: number | null;
}

export interface TotalAssetsHistorySummary {
  /** One point per Investment Wealth History date, ascending. May include partial-coverage points — kept for coverage explanation, never presented as a complete total. */
  points: TotalAssetsHistoryPoint[];
  /** Subset of `points` with complete coverage on both sides, ascending — the only points safe to chart/headline. */
  completePoints: TotalAssetsHistoryPoint[];
  /** Latest complete-coverage point, or null if none exists yet. */
  latest: TotalAssetsHistoryPoint | null;
  /** Between the latest two complete-coverage points, or null if fewer than two exist. */
  delta: TotalAssetsHistoryDelta | null;
  anyPartial: boolean;
  partialCount: number;
  hasAnyPoints: boolean;
}

/**
 * Composes Total Assets History from the Investment Wealth History spine and
 * already-resolved Cash As-Of evidence.
 *
 * `cashAccountsStatus` mirrors totalAssets.ts's current-Total-Assets
 * contract: the cash side can only ever be complete when the CashAccount
 * list itself loaded successfully (a "loading" or "error" status makes
 * every date's cash side incomplete, regardless of what partial evidence
 * happens to be in `cashAsOfByAccountAndDate`).
 *
 * `cashAccounts` should include BOTH active and archived accounts — archive
 * state is never consulted here, so an archived account's historical
 * evidence contributes exactly like an active one's.
 */
export function computeTotalAssetsHistory(
  investmentPoints: WealthHistoryPoint[],
  cashAccountsStatus: AssetLoadStatus,
  cashAccounts: TotalAssetsHistoryCashAccount[],
  cashAsOfByAccountAndDate: Record<number, Record<string, CashAsOfEvidence | undefined> | undefined>,
): TotalAssetsHistorySummary {
  const createdKeyById = new Map(cashAccounts.map((a) => [a.id, createdDateKey(a.created_at)]));

  const points: TotalAssetsHistoryPoint[] = investmentPoints
    .slice()
    .sort((a, b) => a.date.localeCompare(b.date))
    .map((ip) => {
      const investmentComplete = ip.complete;
      const investmentAssets = investmentComplete ? ip.totalValue : null;

      // Lifecycle: an account not yet created by this date is not expected —
      // never fabricated as missing evidence, never counted at all.
      const expectedAccounts = cashAccounts.filter((a) => (createdKeyById.get(a.id) ?? ip.date) <= ip.date);
      const cashExpectedCount = expectedAccounts.length;

      let cashContributingCount = 0;
      let cashSum = 0;
      for (const account of expectedAccounts) {
        const evidence = cashAsOfByAccountAndDate[account.id]?.[ip.date];
        // A legitimate zero balance (available: true, balance: 0) counts as
        // contributing — distinct from a missing/unavailable/failed entry.
        if (evidence != null && evidence.available && evidence.balance != null) {
          cashContributingCount += 1;
          cashSum += evidence.balance;
        }
      }

      const cashComplete = cashAccountsStatus === "success" && cashContributingCount === cashExpectedCount;
      const externalCash = cashComplete ? cashSum : null;

      const complete = investmentComplete && cashComplete;
      const totalAssets =
        complete && investmentAssets != null && externalCash != null ? investmentAssets + externalCash : null;

      return {
        date: ip.date,
        investmentAssets,
        investmentContributingCount: ip.contributingCount,
        investmentExpectedCount: ip.expectedCount,
        investmentComplete,
        externalCash,
        cashContributingCount,
        cashExpectedCount,
        cashComplete,
        totalAssets,
        complete,
      };
    });

  const completePoints = points.filter((p) => p.complete);
  const latest = completePoints.length > 0 ? completePoints[completePoints.length - 1] : null;

  let delta: TotalAssetsHistoryDelta | null = null;
  if (completePoints.length >= 2) {
    const to = completePoints[completePoints.length - 1];
    const from = completePoints[completePoints.length - 2];
    const change = to.totalAssets! - from.totalAssets!;
    delta = {
      from,
      to,
      change,
      changePct: from.totalAssets !== 0 ? (change / from.totalAssets!) * 100 : null,
    };
  }

  return {
    points,
    completePoints,
    latest,
    delta,
    anyPartial: points.length > completePoints.length,
    partialCount: points.length - completePoints.length,
    hasAnyPoints: points.length > 0,
  };
}
