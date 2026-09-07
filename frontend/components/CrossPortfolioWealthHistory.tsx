"use client";

import Link from "next/link";
import dynamic from "next/dynamic";
import { computeWealthHistory, type WealthHistoryPortfolio } from "@/lib/wealthHistory";
import { computeCombinedPerformance } from "@/lib/combinedPerformance";
import type { PortfolioSnapshotRow } from "@/lib/api";

const WealthHistoryChart = dynamic(() => import("@/components/WealthHistoryChart"), {
  ssr: false,
  loading: () => <div className="h-40 bg-gray-50 rounded-lg animate-pulse" />,
});

const CombinedPerformanceChart = dynamic(() => import("@/components/CombinedPerformanceChart"), {
  ssr: false,
  loading: () => <div className="h-40 bg-gray-50 rounded-lg animate-pulse" />,
});

function fmtTHB(n: number): string {
  return n.toLocaleString("th-TH", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fullDate(d: string): string {
  return new Date(d + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

export default function CrossPortfolioWealthHistory({
  portfolios,
  snapshotsByPortfolio,
  failedMap,
  loading,
}: {
  portfolios: WealthHistoryPortfolio[];
  snapshotsByPortfolio: Record<number, PortfolioSnapshotRow[]>;
  failedMap: Record<number, boolean>;
  loading: boolean;
}) {
  if (loading) {
    return (
      <section className="space-y-2" aria-busy="true">
        <div className="h-5 w-48 bg-gray-100 rounded animate-pulse" />
        <div className="h-40 bg-gray-100 rounded-xl animate-pulse" />
      </section>
    );
  }

  if (portfolios.length === 0) return null;

  const summary = computeWealthHistory(portfolios, snapshotsByPortfolio, failedMap);
  const performance = computeCombinedPerformance(portfolios, snapshotsByPortfolio, failedMap);
  const failedCount = portfolios.filter((p) => failedMap[p.id]).length;

  return (
    <section className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-base font-semibold text-gray-500 uppercase tracking-wide">Investment Wealth History</h2>
        <Link href="/performance" className="text-xs text-blue-600 hover:text-blue-800 font-medium">
          View Performance →
        </Link>
      </div>

      {!summary.hasAnySnapshots ? (
        <div className="bg-white border rounded-xl p-6 shadow-sm text-center space-y-1">
          <p className="text-sm text-gray-500">Investment wealth history will appear after portfolio snapshots are recorded.</p>
          {summary.anyFailed && (
            <p className="text-xs text-red-500">
              Excludes {failedCount} portfolio{failedCount === 1 ? "" : "s"} that failed to load.
            </p>
          )}
        </div>
      ) : !summary.latest ? (
        <div className="bg-white border rounded-xl p-6 shadow-sm text-center space-y-1">
          <p className="text-sm text-gray-500">
            No date yet has a complete snapshot across all your portfolios — investment wealth history will appear once one does.
          </p>
          {summary.anyFailed && (
            <p className="text-xs text-red-500">
              Excludes {failedCount} portfolio{failedCount === 1 ? "" : "s"} that failed to load.
            </p>
          )}
        </div>
      ) : (
        <div className="bg-white border rounded-xl p-5 shadow-sm space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Latest Combined Investment Wealth</p>
              <p className="text-2xl font-bold text-gray-800">฿{fmtTHB(summary.latest.totalValue)}</p>
              <p className="text-xs text-gray-400 mt-0.5">as of {fullDate(summary.latest.date)}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Value Change vs Previous Point</p>
              {summary.delta ? (
                <>
                  <p className={`text-2xl font-bold ${summary.delta.change >= 0 ? "text-emerald-700" : "text-red-600"}`}>
                    {summary.delta.change >= 0 ? "+" : ""}฿{fmtTHB(summary.delta.change)}
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {summary.delta.changePct != null
                      ? `${summary.delta.changePct >= 0 ? "+" : ""}${summary.delta.changePct.toFixed(2)}% since ${fullDate(summary.delta.from.date)}`
                      : `since ${fullDate(summary.delta.from.date)}`}
                  </p>
                </>
              ) : (
                <p className="text-sm text-gray-400">Not enough comparable history yet</p>
              )}
            </div>
          </div>

          {summary.completePoints.length >= 2 && <WealthHistoryChart points={summary.completePoints} />}

          {(summary.anyPartial || summary.anyFailed) && (
            <p className="text-xs text-gray-400">
              {summary.anyFailed && `Excludes ${failedCount} portfolio${failedCount === 1 ? "" : "s"} that failed to load. `}
              {summary.anyPartial &&
                `${summary.partialCount} historical date${summary.partialCount === 1 ? "" : "s"} excluded from the chart — incomplete portfolio coverage.`}
            </p>
          )}
        </div>
      )}

      <div className="bg-white border rounded-xl p-5 shadow-sm space-y-3">
        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Investment Performance</h3>
        <p className="text-xs text-gray-400">
          Cash-flow-adjusted investment return across your portfolios — excludes deposits, withdrawals, and imported positions.
          Distinct from the investment wealth value change above; external Cash Accounts are not included.
        </p>

        {!performance.hasAnySnapshots ? (
          <p className="text-sm text-gray-400">Investment performance will appear after portfolio snapshots are recorded.</p>
        ) : performance.cumulativeReturnPct == null ? (
          <p className="text-sm text-gray-400">
            No combined return yet — every active portfolio needs a comparable, eligible snapshot on a shared date.
          </p>
        ) : (
          <>
            <p className={`text-2xl font-bold ${performance.cumulativeReturnPct >= 0 ? "text-emerald-700" : "text-red-600"}`}>
              {performance.cumulativeReturnPct >= 0 ? "+" : ""}
              {performance.cumulativeReturnPct.toFixed(2)}%
            </p>
            <p className="text-xs text-gray-400">
              {fullDate(performance.startDate!)} – {fullDate(performance.endDate!)}
            </p>
            {performance.points.length >= 2 && <CombinedPerformanceChart points={performance.points} />}
          </>
        )}

        {(performance.excludedCount > 0 || performance.anyFailed) && (
          <p className="text-xs text-gray-400">
            {performance.anyFailed &&
              `${failedCount} portfolio${failedCount === 1 ? "" : "s"} could not be loaded and ${failedCount === 1 ? "is" : "are"} left out of this figure. `}
            {performance.excludedCount > 0 &&
              `${performance.excludedCount} date${performance.excludedCount === 1 ? "" : "s"} skipped — not every active portfolio had comparable coverage.`}
          </p>
        )}
      </div>
    </section>
  );
}
