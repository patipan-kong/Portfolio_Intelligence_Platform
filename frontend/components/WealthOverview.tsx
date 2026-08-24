"use client";

import Link from "next/link";
import { usePortfolio } from "@/lib/PortfolioContext";
import { computeWealthSummary, sharePct } from "@/lib/wealthOverview";
import type { Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";

function fmtTHB(n: number): string {
  return n.toLocaleString("th-TH", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export default function WealthOverview({
  portfolios,
  holdingsMap,
  priceMap,
  holdingsFailedMap,
  pricesLoaded,
  loading,
}: {
  portfolios: Portfolio[];
  holdingsMap: Record<number, PortfolioItem[]>;
  priceMap: Record<number, PriceRefreshItem[]>;
  holdingsFailedMap: Record<number, boolean>;
  pricesLoaded: boolean;
  loading: boolean;
}) {
  const { selectPortfolio } = usePortfolio();

  if (loading) {
    return (
      <section className="space-y-3" aria-busy="true">
        <div className="h-28 bg-gray-100 rounded-xl animate-pulse" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {[0, 1, 2].map((i) => (
            <div key={i} className="h-32 bg-gray-100 rounded-xl animate-pulse" />
          ))}
        </div>
      </section>
    );
  }

  if (portfolios.length === 0) {
    return (
      <section className="bg-white border rounded-xl p-8 shadow-sm text-center">
        <p className="text-sm text-gray-500">No portfolios yet.</p>
        <Link
          href="/portfolio"
          className="inline-block mt-2 text-sm text-blue-600 hover:text-blue-800 font-medium"
        >
          Create your first portfolio →
        </Link>
      </section>
    );
  }

  const summary = computeWealthSummary(portfolios, holdingsMap, priceMap, holdingsFailedMap);
  const failedCount = summary.portfolios.filter((row) => row.failed).length;

  return (
    <section className="space-y-4">
      <div className="bg-white border rounded-xl p-6 shadow-sm">
        <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Total Wealth</p>
        <p className="text-3xl font-bold text-gray-800">฿{fmtTHB(summary.totalWealth)}</p>
        {(!pricesLoaded || summary.anyEstimated || summary.anyStale || summary.anyFailed) && (
          <div className="mt-2 flex flex-col gap-0.5 text-xs text-gray-400">
            {!pricesLoaded && (
              <span className="flex items-center gap-1">
                <span className="inline-block w-2.5 h-2.5 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
                Loading live prices…
              </span>
            )}
            {summary.anyEstimated && (
              <span>Some holdings use a last-known price — totals may be approximate.</span>
            )}
            {summary.anyStale && (
              <span>Some holdings show a cached price because a live fetch was unavailable — totals may not be fully current.</span>
            )}
            {summary.anyFailed && (
              <span className="text-red-500">
                Excludes {failedCount} portfolio{failedCount === 1 ? "" : "s"} that failed to load.
              </span>
            )}
          </div>
        )}
      </div>

      <div>
        <h2 className="text-base font-semibold text-gray-500 uppercase tracking-wide mb-2">Portfolios</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {summary.portfolios.map((row) => {
            const pct = sharePct(row, summary.totalWealth);
            return (
              <Link
                key={row.portfolioId}
                href="/portfolio"
                onClick={() => selectPortfolio(row.portfolioId)}
                className="block bg-white border rounded-xl p-4 shadow-sm hover:border-blue-300 hover:shadow-md transition-all"
              >
                <p className="text-sm font-semibold text-gray-800 truncate">{row.name}</p>
                {row.failed ? (
                  <p className="text-xs text-red-500 mt-2">Unable to load holdings — tap to open</p>
                ) : (
                  <>
                    <p className="text-xl font-bold text-gray-800 mt-1">฿{fmtTHB(row.total)}</p>
                    <div className="mt-2 space-y-0.5 text-xs text-gray-400">
                      <div className="flex justify-between">
                        <span>Cash</span>
                        <span>฿{fmtTHB(row.cash)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Holdings</span>
                        <span>
                          ฿{fmtTHB(row.holdingsValue)}
                          {row.hasEstimatedPrice && (
                            <span className="ml-1 text-amber-500" title="Uses a last-known price">*</span>
                          )}
                          {row.hasStalePrice && (
                            <span className="ml-1 text-amber-500" title="Live price unavailable; showing the last cached price.">⏱</span>
                          )}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>Share of wealth</span>
                        <span>{pct != null ? `${pct.toFixed(1)}%` : "—"}</span>
                      </div>
                    </div>
                  </>
                )}
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
}
