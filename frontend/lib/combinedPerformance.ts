// Combined Multi-Portfolio Investment Performance — pure aggregation over
// each portfolio's already-computed, cash-flow-adjusted snapshot return
// (backend/services/portfolio_metrics.py::compute_period_metrics). This
// module does not reclassify cash flows and does not introduce a second
// return formula: it reuses investment_return_amount exactly as the backend
// computed it, weights portfolios by beginning-of-period NAV, and
// chain-links the resulting weighted daily returns into a base-100 TWR
// index — the same chain-link pattern already used for per-portfolio
// cumulative/benchmark return elsewhere in this codebase.
//
// Beginning-of-period NAV is not a separately stored field. It is
// reconstructed algebraically from fields already present on the very same
// snapshot row, by inverting the backend's own formula:
//   investment_return_amount = total_value - beginning_nav - net_external_cash_flow
//                               - imported_asset_value - manual_adjustment_value
//   => beginning_nav = total_value - investment_return_amount - net_external_cash_flow
//                       - imported_asset_value - manual_adjustment_value
// This is algebraic inversion of a trusted, already-computed result, not an
// inferred or estimated value — every quantity on the right-hand side is a
// real field on that row.
//
// Coverage discipline mirrors wealthHistory.ts: a date only produces a
// combined observation when every portfolio that already existed by that
// date (Portfolio.created_at <= date) also has an ELIGIBLE snapshot for it
// — meaning that portfolio's own investment_return_amount is non-null (the
// backend itself could establish a period return there; the first snapshot
// after a portfolio's creation has no prior NAV, so it is never eligible)
// and its reconstructed beginning NAV is strictly positive. A missing or
// ineligible snapshot makes the date unavailable for the combined series —
// never zero-filled, forward-filled, or interpolated.

import type { Portfolio, PortfolioSnapshotRow } from "@/lib/api";

// Same lifecycle rule as wealthHistory.ts's own (unexported) createdDateKey:
// a plain YYYY-MM-DD calendar-date key in the dashboard's display timezone,
// so a portfolio's created_at compares lexicographically against
// snapshot_date without a separate parse step. Kept local rather than
// imported to avoid a cross-runtime import-extension mismatch between this
// module's plain-Node pure tests and Next.js's bundler resolution — it is a
// few lines, not worth a shared module for.
const DISPLAY_TZ = "Asia/Bangkok";
const dateKeyFormatter = new Intl.DateTimeFormat("en-CA", {
  timeZone: DISPLAY_TZ,
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
});

function createdDateKey(isoDate: string): string {
  return dateKeyFormatter.format(new Date(isoDate));
}

export interface CombinedPerformancePortfolio {
  id: number;
  name: string;
  created_at: string;
}

export interface CombinedPerformancePoint {
  date: string; // "YYYY-MM-DD", matches PortfolioSnapshotRow.snapshot_date
  /** Beginning-of-period-NAV-weighted combined return for this date, as a percentage. */
  combinedReturnPct: number;
  /** Chain-linked TWR index; 100 is the (unlisted) starting point before the first observed return. */
  index: number;
  /** (index / 100 - 1) * 100 — cumulative cash-flow-adjusted return as of this point. */
  cumulativeReturnPct: number;
  /** How many portfolios contributed an eligible return observation on this date. */
  contributingCount: number;
  /** How many portfolios already existed (by Portfolio.created_at) on this date. */
  expectedCount: number;
}

export interface CombinedPerformanceSummary {
  /** Only dates with full, eligible coverage — the sole basis for the chain. Ascending. */
  points: CombinedPerformancePoint[];
  /** Cumulative cash-flow-adjusted return over the available series, or null if `points` is empty. */
  cumulativeReturnPct: number | null;
  /** First/last date actually included in `points`, or null if `points` is empty. */
  startDate: string | null;
  endDate: string | null;
  /** Dates seen at all (union across portfolios) but excluded — missing, ineligible, or degenerate coverage. */
  excludedCount: number;
  /** True if any portfolio's snapshot fetch failed — its dates can then never be complete. */
  anyFailed: boolean;
  /** True if at least one (non-failed) portfolio contributed any snapshot at all. */
  hasAnySnapshots: boolean;
}

/**
 * Reconstructs a snapshot row's beginning-of-period NAV and pure gain, or
 * null when the row cannot participate in a combined observation: no prior
 * period was established (investment_return_amount is null) or the
 * reconstructed beginning NAV is not strictly positive.
 */
function eligibleObservation(row: PortfolioSnapshotRow): { beginningNav: number; gain: number } | null {
  if (row.investment_return_amount == null) return null;
  const netExternalCashFlow = row.net_external_cash_flow ?? 0;
  const importedAssetValue = row.imported_asset_value ?? 0;
  const manualAdjustmentValue = row.manual_adjustment_value ?? 0;
  const beginningNav =
    row.total_value - row.investment_return_amount - netExternalCashFlow - importedAssetValue - manualAdjustmentValue;
  if (!(beginningNav > 0)) return null;
  return { beginningNav, gain: row.investment_return_amount };
}

/**
 * Aggregates per-portfolio daily snapshot history into a combined,
 * cash-flow-adjusted investment performance series.
 * `failed[portfolioId] === true` means that portfolio's snapshot fetch
 * could not be loaded — its snapshots are treated as entirely unknown (not
 * zero, not skipped from the universe), so it still counts as "expected" on
 * any date it already existed, and a failure can never let a date qualify
 * as complete.
 */
export function computeCombinedPerformance(
  portfolios: CombinedPerformancePortfolio[] | Portfolio[],
  snapshotsByPortfolio: Record<number, PortfolioSnapshotRow[]>,
  failed: Record<number, boolean> = {}
): CombinedPerformanceSummary {
  const createdKeyById = new Map(portfolios.map((p) => [p.id, createdDateKey(p.created_at)]));
  const anyFailed = portfolios.some((p) => failed[p.id]);

  const rowsByDate = new Map<string, Map<number, PortfolioSnapshotRow>>();
  let hasAnySnapshots = false;
  for (const p of portfolios) {
    if (failed[p.id]) continue;
    for (const row of snapshotsByPortfolio[p.id] ?? []) {
      hasAnySnapshots = true;
      let byPortfolio = rowsByDate.get(row.snapshot_date);
      if (!byPortfolio) {
        byPortfolio = new Map();
        rowsByDate.set(row.snapshot_date, byPortfolio);
      }
      byPortfolio.set(p.id, row);
    }
  }

  const allDates = Array.from(rowsByDate.keys()).sort();

  const points: CombinedPerformancePoint[] = [];
  let excludedCount = 0;

  for (const date of allDates) {
    const rowsForDate = rowsByDate.get(date)!;
    const expectedPortfolios = portfolios.filter((p) => (createdKeyById.get(p.id) ?? date) <= date);
    const expectedCount = expectedPortfolios.length;

    let contributingCount = 0;
    let gainSum = 0;
    let navSum = 0;

    for (const p of expectedPortfolios) {
      const row = rowsForDate.get(p.id);
      if (!row) continue;
      const obs = eligibleObservation(row);
      if (!obs) continue;
      contributingCount += 1;
      gainSum += obs.gain;
      navSum += obs.beginningNav;
    }

    const complete = expectedCount > 0 && contributingCount === expectedCount;
    if (!complete || !(navSum > 0)) {
      excludedCount += 1;
      continue;
    }

    const combinedReturnPct = (gainSum / navSum) * 100;
    const prevIndex = points.length > 0 ? points[points.length - 1].index : 100;
    const index = prevIndex * (1 + combinedReturnPct / 100);
    points.push({
      date,
      combinedReturnPct,
      index,
      cumulativeReturnPct: (index / 100 - 1) * 100,
      contributingCount,
      expectedCount,
    });
  }

  const last = points.length > 0 ? points[points.length - 1] : null;

  return {
    points,
    cumulativeReturnPct: last ? last.cumulativeReturnPct : null,
    startDate: points.length > 0 ? points[0].date : null,
    endDate: last ? last.date : null,
    excludedCount,
    anyFailed,
    hasAnySnapshots,
  };
}
