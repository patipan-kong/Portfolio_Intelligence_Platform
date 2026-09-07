"use client";

import dynamic from "next/dynamic";
import type { TotalAssetsHistorySummary } from "@/lib/totalAssetsHistory";

const WealthHistoryChart = dynamic(() => import("@/components/WealthHistoryChart"), {
  ssr: false,
  loading: () => <div className="h-40 bg-gray-50 rounded-lg animate-pulse" />,
});

function fmtTHB(n: number): string {
  return n.toLocaleString("th-TH", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fullDate(d: string): string {
  return new Date(d + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

// Total Assets History = Investment Wealth History (already includes
// brokerage cash) + External Cash, evaluated as-of the same historical
// dates. Reuses WealthHistoryChart directly rather than a new chart
// component — same visual language as Investment Wealth History above it.
export default function TotalAssetsHistoryCard({
  summary,
  loading,
}: {
  summary: TotalAssetsHistorySummary;
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

  return (
    <section className="space-y-3">
      <h2 className="text-base font-semibold text-gray-500 uppercase tracking-wide">Total Assets History</h2>

      {!summary.hasAnyPoints ? (
        <div className="bg-white border rounded-xl p-6 shadow-sm text-center">
          <p className="text-sm text-gray-500">
            Total Assets history will appear once Investment Wealth History has recorded points.
          </p>
        </div>
      ) : !summary.latest ? (
        <div className="bg-white border rounded-xl p-6 shadow-sm text-center">
          <p className="text-sm text-gray-500">
            No date yet has complete Total Assets coverage on both investment and Cash Account sides — this section
            will appear once one does.
          </p>
        </div>
      ) : (
        <div className="bg-white border rounded-xl p-5 shadow-sm space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Latest Complete Total Assets</p>
              <p className="text-2xl font-bold text-gray-800">฿{fmtTHB(summary.latest.totalAssets!)}</p>
              <p className="text-xs text-gray-400 mt-0.5">as of {fullDate(summary.latest.date)}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Change vs Previous Point</p>
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
                <p className="text-sm text-gray-400">Not enough comparable Total Assets history yet</p>
              )}
            </div>
          </div>

          {summary.completePoints.length >= 2 && (
            <WealthHistoryChart
              points={summary.completePoints.map((p) => ({ date: p.date, totalValue: p.totalAssets! }))}
            />
          )}

          {summary.anyPartial && (
            <p className="text-xs text-gray-400">
              {summary.partialCount} historical date{summary.partialCount === 1 ? "" : "s"} excluded — incomplete
              investment or Cash Account coverage.
            </p>
          )}
        </div>
      )}
    </section>
  );
}
