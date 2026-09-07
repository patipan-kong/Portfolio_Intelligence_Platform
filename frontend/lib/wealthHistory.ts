// Cross-Portfolio Wealth History — pure aggregation over each portfolio's
// existing daily PortfolioSnapshot history (getSnapshots), reusing the same
// total_value the per-portfolio Performance page and EquityCurveChart already
// use. No new backend endpoint, no new schema — only a merge-by-date.
//
// Core rule: never fabricate a portfolio's value on a date it has no
// snapshot for. A date's combined total only ever sums the portfolios that
// actually have a snapshot row for that date; every point carries its own
// coverage metadata (contributingCount vs expectedCount) rather than
// pretending a partial sum is the whole picture.

import type { Portfolio, PortfolioSnapshotRow } from "@/lib/api";

export interface WealthHistoryPoint {
  date: string; // "YYYY-MM-DD", matches PortfolioSnapshotRow.snapshot_date
  /** Sum of total_value across portfolios that have a snapshot for this date. Not meaningful alone without `complete`. */
  totalValue: number;
  /** How many portfolios actually contributed a snapshot on this date. */
  contributingCount: number;
  /**
   * How many portfolios were expected to have a snapshot on this date —
   * i.e. already existed (created_at <= date) — counted across ALL supplied
   * portfolios, including ones whose fetch failed. A failed fetch can never
   * make a date look complete: if that portfolio existed on this date, its
   * absence from `contributingCount` correctly keeps this date incomplete.
   */
  expectedCount: number;
  /** True only when every expected portfolio actually contributed and at least one was expected. */
  complete: boolean;
}

export interface WealthHistoryDelta {
  from: WealthHistoryPoint;
  to: WealthHistoryPoint;
  change: number;
  /** null when `from.totalValue` is 0 — a percentage change is undefined, not infinite. */
  changePct: number | null;
}

export interface WealthHistorySummary {
  /** Every date with at least one contributing snapshot, ascending. May include partial-coverage points. */
  points: WealthHistoryPoint[];
  /** Subset of `points` with complete coverage, ascending — the only points safe to chart/headline as "total wealth". */
  completePoints: WealthHistoryPoint[];
  /** Latest complete-coverage point, or null if none exists yet. */
  latest: WealthHistoryPoint | null;
  /** Between the latest two complete-coverage points, or null if fewer than two exist. */
  delta: WealthHistoryDelta | null;
  /** True if any date had partial (not complete) coverage. */
  anyPartial: boolean;
  /** How many dates had partial coverage — i.e. excluded from `completePoints`. */
  partialCount: number;
  /** True if any portfolio's snapshot fetch failed. */
  anyFailed: boolean;
  /** True if any portfolio contributed at least one snapshot at all. */
  hasAnySnapshots: boolean;
}

const DISPLAY_TZ = "Asia/Bangkok";
// en-CA formats as YYYY-MM-DD directly, matching PortfolioSnapshotRow.snapshot_date's
// plain calendar-date form, so a portfolio's created_at compares lexicographically
// against snapshot_date without a separate parse step.
const dateKeyFormatter = new Intl.DateTimeFormat("en-CA", {
  timeZone: DISPLAY_TZ,
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
});

function createdDateKey(isoDate: string): string {
  return dateKeyFormatter.format(new Date(isoDate));
}

export interface WealthHistoryPortfolio {
  id: number;
  name: string;
  created_at: string;
}

/**
 * Aggregates per-portfolio daily snapshot history into a combined series.
 * `failed[portfolioId] === true` means that portfolio's snapshot fetch could
 * not be loaded — its snapshots are treated as entirely unknown (not zero),
 * and it still counts toward `expectedCount` on any date it already existed,
 * so a failure never lets a date appear complete.
 */
export function computeWealthHistory(
  portfolios: WealthHistoryPortfolio[] | Portfolio[],
  snapshotsByPortfolio: Record<number, PortfolioSnapshotRow[]>,
  failed: Record<number, boolean> = {}
): WealthHistorySummary {
  const createdKeyById = new Map(portfolios.map((p) => [p.id, createdDateKey(p.created_at)]));
  const anyFailed = portfolios.some((p) => failed[p.id]);

  const byDate = new Map<string, { sum: number; contributingCount: number }>();
  for (const p of portfolios) {
    if (failed[p.id]) continue;
    for (const row of snapshotsByPortfolio[p.id] ?? []) {
      const entry = byDate.get(row.snapshot_date) ?? { sum: 0, contributingCount: 0 };
      entry.sum += row.total_value;
      entry.contributingCount += 1;
      byDate.set(row.snapshot_date, entry);
    }
  }

  const points: WealthHistoryPoint[] = Array.from(byDate.entries())
    .map(([date, { sum, contributingCount }]) => {
      const expectedCount = portfolios.filter((p) => (createdKeyById.get(p.id) ?? date) <= date).length;
      return {
        date,
        totalValue: sum,
        contributingCount,
        expectedCount,
        complete: expectedCount > 0 && contributingCount === expectedCount,
      };
    })
    .sort((a, b) => a.date.localeCompare(b.date));

  const completePoints = points.filter((p) => p.complete);
  const latest = completePoints.length > 0 ? completePoints[completePoints.length - 1] : null;

  let delta: WealthHistoryDelta | null = null;
  if (completePoints.length >= 2) {
    const to = completePoints[completePoints.length - 1];
    const from = completePoints[completePoints.length - 2];
    delta = {
      from,
      to,
      change: to.totalValue - from.totalValue,
      changePct: from.totalValue !== 0 ? ((to.totalValue - from.totalValue) / from.totalValue) * 100 : null,
    };
  }

  return {
    points,
    completePoints,
    latest,
    delta,
    anyPartial: points.length > completePoints.length,
    partialCount: points.length - completePoints.length,
    anyFailed,
    hasAnySnapshots: points.length > 0,
  };
}
