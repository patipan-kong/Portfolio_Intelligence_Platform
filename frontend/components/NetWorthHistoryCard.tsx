"use client";

import dynamic from "next/dynamic";
import type { NetWorthHistorySummary } from "@/lib/netWorthHistory";

const WealthHistoryChart = dynamic(() => import("@/components/WealthHistoryChart"), {
  ssr: false,
  loading: () => <div className="h-40 bg-gray-50 rounded-lg animate-pulse" />,
});

function fmtTHB(n: number): string {
  return Math.abs(n).toLocaleString("th-TH", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fullDate(d: string): string {
  return new Date(d + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

// Net Worth History = Total Assets History - Total Liabilities History, on
// dates where both are complete. A pure derived composition — this card
// carries no historical evidence or lifecycle logic of its own. Reuses
// WealthHistoryChart directly; negative Net Worth renders naturally (the
// chart's Y axis is already auto-domained, no clamping).
export default function NetWorthHistoryCard({
  summary,
  loading,
}: {
  summary: NetWorthHistorySummary;
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
      <h2 className="text-base font-semibold text-gray-500 uppercase tracking-wide">Net Worth History</h2>

      {!summary.hasAnyPoints ? (
        <div className="bg-white border rounded-xl p-6 shadow-sm text-center">
          <p className="text-sm text-gray-500">
            Net Worth history will appear once historical dates are available.
          </p>
        </div>
      ) : !summary.latest ? (
        <div className="bg-white border rounded-xl p-6 shadow-sm text-center">
          <p className="text-sm text-gray-500">
            No date yet has complete Total Assets and Total Liabilities coverage — this section will appear once
            one does.
          </p>
        </div>
      ) : (
        <div className="bg-white border rounded-xl p-5 shadow-sm space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Latest Complete Net Worth</p>
              <p className="text-2xl font-bold text-gray-800">
                {summary.latest.netWorth! < 0 ? "-" : ""}฿{fmtTHB(summary.latest.netWorth!)}
              </p>
              <p className="text-xs text-gray-400 mt-0.5">as of {fullDate(summary.latest.date)}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Change vs Previous Point</p>
              {summary.delta ? (
                <>
                  <p className={`text-2xl font-bold ${summary.delta.change >= 0 ? "text-emerald-700" : "text-red-600"}`}>
                    {summary.delta.change >= 0 ? "+" : "-"}฿{fmtTHB(summary.delta.change)}
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {summary.delta.changePct != null
                      ? `${summary.delta.changePct >= 0 ? "+" : ""}${summary.delta.changePct.toFixed(2)}% since ${fullDate(summary.delta.from.date)}`
                      : `since ${fullDate(summary.delta.from.date)}`}
                  </p>
                </>
              ) : (
                <p className="text-sm text-gray-400">Not enough comparable Net Worth history yet</p>
              )}
            </div>
          </div>

          {summary.completePoints.length >= 2 && (
            <WealthHistoryChart
              points={summary.completePoints.map((p) => ({ date: p.date, totalValue: p.netWorth! }))}
            />
          )}

          {summary.anyPartial && (
            <p className="text-xs text-gray-400">
              {summary.partialCount} historical date{summary.partialCount === 1 ? "" : "s"} excluded — incomplete
              Total Assets or Total Liabilities coverage.
            </p>
          )}
        </div>
      )}
    </section>
  );
}
