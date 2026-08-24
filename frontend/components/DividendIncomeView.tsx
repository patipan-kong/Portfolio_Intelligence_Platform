"use client";

import dynamic from "next/dynamic";
import { computeDividendSummary } from "@/lib/dividendIncome";
import TransactionHistoryTable from "@/components/TransactionHistoryTable";
import type { TransactionRecord } from "@/lib/api";

const DividendMonthlyChart = dynamic(() => import("@/components/DividendMonthlyChart"), {
  ssr: false,
  loading: () => <div className="h-40 animate-pulse bg-gray-100 rounded-xl" />,
});

function fmt(n: number): string {
  return n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export default function DividendIncomeView({
  transactions,
  loading,
}: {
  transactions: TransactionRecord[];
  loading: boolean;
}) {
  if (loading) {
    return (
      <div className="space-y-4" aria-busy="true">
        <div className="h-24 bg-gray-100 rounded-xl animate-pulse" />
        <div className="h-40 bg-gray-100 rounded-xl animate-pulse" />
        <div className="h-56 bg-gray-100 rounded-xl animate-pulse" />
      </div>
    );
  }

  const summary = computeDividendSummary(transactions, 10);

  if (summary.dividends.length === 0) {
    return (
      <div className="bg-white border rounded-xl p-8 shadow-sm text-center">
        <p className="text-sm text-gray-500">No dividend income recorded for this portfolio yet.</p>
        <p className="text-xs text-gray-400 mt-1">
          Dividends you record from the portfolio page will show up here.
        </p>
      </div>
    );
  }

  const primaryCurrency = summary.totalsByCurrency[0].currency;
  const primaryMonthly = summary.byMonth
    .filter((row) => row.currency === primaryCurrency)
    .map((row) => ({ month: row.month, amount: row.amount }));

  return (
    <div className="space-y-6">
      {/* ── Total dividend income ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {summary.totalsByCurrency.map((row) => (
          <div key={row.currency} className="bg-white border rounded-xl p-6 shadow-sm">
            <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">
              Total Dividend Income {summary.mixedCurrency ? `(${row.currency})` : ""}
            </p>
            <p className="text-3xl font-bold text-emerald-700">
              {row.currency} {fmt(row.amount)}
            </p>
          </div>
        ))}
      </div>
      {summary.mixedCurrency && (
        <p className="text-xs text-gray-400 -mt-3">
          This portfolio has dividends in more than one currency — totals are kept separate rather than summed together.
        </p>
      )}

      {/* ── Income over time ── */}
      <div className="bg-white border rounded-xl p-5 shadow-sm">
        <h2 className="text-sm font-semibold text-gray-800 mb-3">
          Monthly Income {summary.mixedCurrency ? `(${primaryCurrency})` : ""}
        </h2>
        <DividendMonthlyChart data={primaryMonthly} currency={primaryCurrency} />
      </div>

      {/* ── Income by asset ── */}
      <div className="bg-white border rounded-xl p-5 shadow-sm">
        <h2 className="text-sm font-semibold text-gray-800 mb-3">Income by Asset</h2>
        <div className="space-y-2">
          {summary.byAsset.map((row) => (
            <div
              key={`${row.symbol ?? "none"}::${row.currency}`}
              className="flex items-center justify-between text-sm border-b last:border-0 border-gray-100 pb-2 last:pb-0"
            >
              <span className="font-medium text-gray-800">
                {row.symbol ? row.symbol.replace(".BK", "") : "No symbol recorded"}
              </span>
              <span className="text-gray-500 text-xs">
                {row.count} payment{row.count === 1 ? "" : "s"}
              </span>
              <span className="font-semibold text-gray-800">
                {row.currency} {fmt(row.amount)}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* ── Recent dividends ── */}
      <div>
        <h2 className="text-base font-semibold text-gray-500 uppercase tracking-wide mb-2">Recent Dividends</h2>
        <TransactionHistoryTable transactions={summary.recent} />
      </div>
    </div>
  );
}
