// Net Worth History — a thin derived composition of the already-computed
// Total Assets History and Total Liabilities History summaries. It owns no
// evidence of its own: no Cash/Investment/Liability reconstruction, no
// lifecycle rules, no historical data fetching. Those semantics belong to
// totalAssetsHistory.ts and totalLiabilitiesHistory.ts respectively — this
// module only reads their already-resolved `points` and composes:
//
//   Net Worth(d) = Total Assets(d) - Total Liabilities(d)
//
// Net Worth(d) is only numeric when BOTH sides report a complete, finite
// value for date d. An unavailable Liability side is never interpreted as
// zero debt; an unavailable Assets side is never interpreted as zero
// assets. Negative and zero Net Worth are both legitimate, unclamped
// results.

import type { TotalAssetsHistorySummary } from "./totalAssetsHistory";
import type { TotalLiabilitiesHistorySummary } from "./totalLiabilitiesHistory";

export interface NetWorthHistoryPoint {
  date: string; // "YYYY-MM-DD", matches the shared historical date spine
  /** Total Assets History's own value for this date, independent of the Liabilities side's completeness. */
  totalAssets: number | null;
  /** Total Liabilities History's own value for this date, independent of the Assets side's completeness. */
  totalLiabilities: number | null;
  /** Only non-null when both `assetsComplete` and `liabilitiesComplete` are true. */
  netWorth: number | null;
  assetsComplete: boolean;
  liabilitiesComplete: boolean;
  complete: boolean;
}

export interface NetWorthHistoryDelta {
  from: NetWorthHistoryPoint;
  to: NetWorthHistoryPoint;
  change: number;
  /** null when `from.netWorth` is 0 — a percentage change is undefined, not infinite. */
  changePct: number | null;
}

export interface NetWorthHistorySummary {
  /** One point per shared historical date, ascending. May include partial-coverage points — kept for coverage explanation, never presented as a complete Net Worth. */
  points: NetWorthHistoryPoint[];
  /** Subset of `points` with complete coverage on both sides, ascending — the only points safe to chart/headline. */
  completePoints: NetWorthHistoryPoint[];
  /** Latest complete-coverage point, or null if none exists yet. */
  latest: NetWorthHistoryPoint | null;
  /** Between the latest two complete-coverage points, or null if fewer than two exist. */
  delta: NetWorthHistoryDelta | null;
  anyPartial: boolean;
  partialCount: number;
  hasAnyPoints: boolean;
}

/**
 * Composes Net Worth History from the shared historical date spine and the
 * already-computed Total Assets History / Total Liabilities History
 * summaries.
 *
 * `dates` is the same shared spine both underlying summaries were built
 * from (e.g. `investmentHistoryDates`). Each side's points are looked up by
 * date key, never by array position — if either summary unexpectedly lacks
 * a point for one of `dates`, that date is honestly marked incomplete
 * rather than silently paired with a mismatched point.
 */
export function computeNetWorthHistory(
  dates: string[],
  totalAssetsHistory: Pick<TotalAssetsHistorySummary, "points">,
  totalLiabilitiesHistory: Pick<TotalLiabilitiesHistorySummary, "points">,
): NetWorthHistorySummary {
  const assetsByDate = new Map(totalAssetsHistory.points.map((p) => [p.date, p]));
  const liabilitiesByDate = new Map(totalLiabilitiesHistory.points.map((p) => [p.date, p]));

  const points: NetWorthHistoryPoint[] = dates
    .slice()
    .sort((a, b) => a.localeCompare(b))
    .map((date) => {
      const assets = assetsByDate.get(date);
      const liabilities = liabilitiesByDate.get(date);

      const assetsComplete =
        assets != null && assets.complete && assets.totalAssets != null && Number.isFinite(assets.totalAssets);
      const liabilitiesComplete =
        liabilities != null &&
        liabilities.complete &&
        liabilities.totalLiabilities != null &&
        Number.isFinite(liabilities.totalLiabilities);

      const complete = assetsComplete && liabilitiesComplete;
      const netWorth = complete ? assets!.totalAssets! - liabilities!.totalLiabilities! : null;

      return {
        date,
        totalAssets: assetsComplete ? assets!.totalAssets : null,
        totalLiabilities: liabilitiesComplete ? liabilities!.totalLiabilities : null,
        netWorth: netWorth != null && Number.isFinite(netWorth) ? netWorth : null,
        assetsComplete,
        liabilitiesComplete,
        complete: complete && netWorth != null && Number.isFinite(netWorth),
      };
    });

  const completePoints = points.filter((p) => p.complete);
  const latest = completePoints.length > 0 ? completePoints[completePoints.length - 1] : null;

  let delta: NetWorthHistoryDelta | null = null;
  if (completePoints.length >= 2) {
    const to = completePoints[completePoints.length - 1];
    const from = completePoints[completePoints.length - 2];
    const change = to.netWorth! - from.netWorth!;
    delta = {
      from,
      to,
      change,
      changePct: from.netWorth !== 0 ? (change / from.netWorth!) * 100 : null,
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
