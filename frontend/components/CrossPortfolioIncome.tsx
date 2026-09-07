"use client";

import Link from "next/link";
import { computeCrossPortfolioIncome } from "@/lib/dividendIncome";
import type { TransactionRecord } from "@/lib/api";

function fmt(n: number): string {
  return n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export default function CrossPortfolioIncome({
  portfolios,
  transactionsByPortfolio,
  failedMap,
  loading,
}: {
  portfolios: Array<{ id: number; name: string }>;
  transactionsByPortfolio: Record<number, TransactionRecord[]>;
  failedMap: Record<number, boolean>;
  loading: boolean;
}) {
  if (loading) {
    return (
      <section className="space-y-2" aria-busy="true">
        <div className="h-5 w-48 bg-gray-100 rounded animate-pulse" />
        <div className="h-32 bg-gray-100 rounded-xl animate-pulse" />
      </section>
    );
  }

  if (portfolios.length === 0) return null;

  const summary = computeCrossPortfolioIncome(portfolios, transactionsByPortfolio, failedMap);
  const failedCount = summary.byPortfolio.filter((row) => row.failed).length;
  const contributors = summary.byPortfolio.filter((row) => !row.failed && row.totalsByCurrency.length > 0);

  return (
    <section className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-base font-semibold text-gray-500 uppercase tracking-wide">Dividend Income</h2>
        <Link href="/income" className="text-xs text-blue-600 hover:text-blue-800 font-medium">
          View Income page →
        </Link>
      </div>

      {summary.totalsByCurrency.length === 0 ? (
        <div className="bg-white border rounded-xl p-6 shadow-sm text-center">
          <p className="text-sm text-gray-500">No dividend income recorded across your portfolios yet.</p>
        </div>
      ) : (
        <div className="bg-white border rounded-xl p-5 shadow-sm space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {summary.totalsByCurrency.map((row) => (
              <div key={row.currency}>
                <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">
                  Total {summary.mixedCurrency ? `(${row.currency})` : ""}
                </p>
                <p className="text-2xl font-bold text-emerald-700">
                  {row.currency} {fmt(row.amount)}
                </p>
              </div>
            ))}
            {summary.currentYearTotalsByCurrency.map((row) => (
              <div key={`year-${row.currency}`}>
                <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">
                  This Year {summary.mixedCurrency ? `(${row.currency})` : ""}
                </p>
                <p className="text-2xl font-bold text-gray-800">
                  {row.currency} {fmt(row.amount)}
                </p>
              </div>
            ))}
            {summary.trailing12MonthTotalsByCurrency.map((row) => (
              <div key={`t12-${row.currency}`}>
                <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">
                  Trailing 12 Months {summary.mixedCurrency ? `(${row.currency})` : ""}
                </p>
                <p className="text-2xl font-bold text-gray-800">
                  {row.currency} {fmt(row.amount)}
                </p>
              </div>
            ))}
          </div>

          {contributors.length > 0 && (
            <div className="space-y-1.5 pt-1 border-t border-gray-100">
              {contributors.map((row) => (
                <div key={row.portfolioId} className="flex items-center justify-between text-sm">
                  <span className="text-gray-700">{row.name}</span>
                  <span className="text-gray-800 font-medium">
                    {row.totalsByCurrency.map((t) => `${t.currency} ${fmt(t.amount)}`).join(" · ")}
                  </span>
                </div>
              ))}
            </div>
          )}

          {summary.anyFailed && (
            <p className="text-xs text-red-500">
              Excludes {failedCount} portfolio{failedCount === 1 ? "" : "s"} that failed to load.
            </p>
          )}
        </div>
      )}
    </section>
  );
}
