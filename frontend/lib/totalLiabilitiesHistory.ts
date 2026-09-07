// Total Liabilities History — pure composition of the shared historical date
// spine (the same dates Total Assets History / Investment Wealth History
// already use, so a later Net Worth History composition stays date-aligned)
// with the existing Liability As-Of contract
// (services/liability_balance.py::liability_balance_as_of, read via
// GET /liabilities/{id}/as-of). No new backend endpoint, no new schema.
//
// The As-Of contract is an effective-state model, not a payment ledger:
// `liability_balance_as_of` returns the latest observation with
// observed_on <= date, or null ("unavailable") when no observation exists
// on or before that date. This module never reads a Liability's current
// `balance` — only the already-resolved As-Of evidence passed in by the
// caller (accepts resolved evidence, performs no network calls itself).
//
// Lifecycle discipline mirrors Total Assets History's CashAccount handling:
// - a Liability not yet created by date d is simply not expected;
// - a Liability created before d but with no observation on or before d (or
//   a failed/missing As-Of request) is expected but unavailable — it keeps
//   the date incomplete, never a fabricated zero;
// - an archived Liability's historical evidence remains fully included —
//   archive state is never read here and never implies zero.

import type { LiabilityLoadStatus } from "./totalLiabilities";
import type { LiabilityBalanceAsOf } from "./api";

const DISPLAY_TZ = "Asia/Bangkok";
// Same lifecycle-key convention as totalAssetsHistory.ts/wealthHistory.ts's
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

export interface TotalLiabilitiesHistoryLiability {
  id: number;
  created_at: string;
}

/** Already-resolved Liability As-Of evidence for one (liability, date) pair. A missing map entry — never fetched, or a failed request — is treated identically to `available: false`: expected but unavailable. */
export type LiabilityAsOfEvidence = Pick<LiabilityBalanceAsOf, "balance" | "available" | "currency">;

export interface TotalLiabilitiesHistoryPoint {
  date: string; // "YYYY-MM-DD", matches the shared historical date spine
  /** Only non-null when every expected liability has valid THB, finite, non-negative evidence for this date. */
  totalLiabilities: number | null;
  contributingCount: number;
  expectedCount: number;
  complete: boolean;
}

export interface TotalLiabilitiesHistoryDelta {
  from: TotalLiabilitiesHistoryPoint;
  to: TotalLiabilitiesHistoryPoint;
  change: number;
  /** null when `from.totalLiabilities` is 0 — a percentage change is undefined, not infinite. */
  changePct: number | null;
}

export interface TotalLiabilitiesHistorySummary {
  /** One point per shared historical date, ascending. May include partial-coverage points — kept for coverage explanation, never presented as a complete total. */
  points: TotalLiabilitiesHistoryPoint[];
  /** Subset of `points` with complete coverage, ascending — the only points safe to chart/headline. */
  completePoints: TotalLiabilitiesHistoryPoint[];
  /** Latest complete-coverage point, or null if none exists yet. */
  latest: TotalLiabilitiesHistoryPoint | null;
  /** Between the latest two complete-coverage points, or null if fewer than two exist. */
  delta: TotalLiabilitiesHistoryDelta | null;
  anyPartial: boolean;
  partialCount: number;
  hasAnyPoints: boolean;
}

/**
 * Composes Total Liabilities History from a shared historical date spine and
 * already-resolved Liability As-Of evidence.
 *
 * `liabilityStatus` mirrors totalLiabilities.ts's current-Total-Liabilities
 * contract: the total can only ever be complete when the Liability list
 * itself loaded successfully (a "loading" or "error" status makes every
 * date incomplete, regardless of what partial evidence happens to be in
 * `asOfByLiabilityAndDate`). A successful response with zero liabilities is
 * a legitimate zero for every date, matching current Total Liabilities.
 *
 * `liabilities` should include BOTH active and archived rows — archive
 * state is never consulted here, so an archived liability's historical
 * evidence contributes exactly like an active one's.
 */
export function computeTotalLiabilitiesHistory(
  dates: string[],
  liabilityStatus: LiabilityLoadStatus,
  liabilities: TotalLiabilitiesHistoryLiability[],
  asOfByLiabilityAndDate: Record<number, Record<string, LiabilityAsOfEvidence | undefined> | undefined>,
): TotalLiabilitiesHistorySummary {
  const createdKeyById = new Map(liabilities.map((l) => [l.id, createdDateKey(l.created_at)]));

  const points: TotalLiabilitiesHistoryPoint[] = dates
    .slice()
    .sort((a, b) => a.localeCompare(b))
    .map((date) => {
      // Lifecycle: a liability not yet created by this date is not
      // expected — never fabricated as missing evidence, never counted.
      const expectedLiabilities = liabilities.filter((l) => (createdKeyById.get(l.id) ?? date) <= date);
      const expectedCount = expectedLiabilities.length;

      let contributingCount = 0;
      let sum = 0;
      for (const liability of expectedLiabilities) {
        const evidence = asOfByLiabilityAndDate[liability.id]?.[date];
        // Malformed/non-THB/non-finite/negative evidence is treated as
        // unavailable, not silently normalized into a legitimate value —
        // it keeps this date's coverage incomplete rather than rejecting
        // the whole point outright.
        if (
          evidence != null &&
          evidence.available &&
          evidence.balance != null &&
          Number.isFinite(evidence.balance) &&
          evidence.balance >= 0 &&
          evidence.currency === "THB"
        ) {
          contributingCount += 1;
          sum += evidence.balance;
        }
      }

      const complete = liabilityStatus === "success" && contributingCount === expectedCount;
      const totalLiabilities = complete && Number.isFinite(sum) ? sum : null;

      return { date, totalLiabilities, contributingCount, expectedCount, complete };
    });

  const completePoints = points.filter((p) => p.complete);
  const latest = completePoints.length > 0 ? completePoints[completePoints.length - 1] : null;

  let delta: TotalLiabilitiesHistoryDelta | null = null;
  if (completePoints.length >= 2) {
    const to = completePoints[completePoints.length - 1];
    const from = completePoints[completePoints.length - 2];
    const change = to.totalLiabilities! - from.totalLiabilities!;
    delta = {
      from,
      to,
      change,
      changePct: from.totalLiabilities !== 0 ? (change / from.totalLiabilities!) * 100 : null,
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
