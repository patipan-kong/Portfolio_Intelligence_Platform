"use client";

import Link from "next/link";
import { usePortfolio } from "@/lib/PortfolioContext";
import { computeWealthSummary, sharePct } from "@/lib/wealthOverview";
import { computeTotalAssets, type AssetLoadStatus } from "@/lib/totalAssets";
import type { CashAccount, Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";

function fmtTHB(n: number): string {
  return n.toLocaleString("th-TH", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fmtMetric(n: number | null): string {
  return n == null ? "Unavailable" : `฿${fmtTHB(n)}`;
}

export default function WealthOverview({
  portfolios,
  holdingsMap,
  priceMap,
  holdingsFailedMap,
  pricesLoaded,
  loading,
  cashAccounts = [],
  cashStatus = "success",
  portfolioLoadError = null,
}: {
  portfolios: Portfolio[];
  holdingsMap: Record<number, PortfolioItem[]>;
  priceMap: Record<number, PriceRefreshItem[]>;
  holdingsFailedMap: Record<number, boolean>;
  pricesLoaded: boolean;
  loading: boolean;
  cashAccounts?: CashAccount[];
  cashStatus?: AssetLoadStatus;
  portfolioLoadError?: string | null;
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

  const summary = computeWealthSummary(portfolios, holdingsMap, priceMap, holdingsFailedMap);
  // The empty portfolio set is a valid, fully-known Investment Core state.
  // Non-empty portfolios require the current price phase and every holdings
  // request to settle before Total Assets can be claimed.
  const investmentComplete = !portfolioLoadError &&
    (portfolios.length === 0 || (pricesLoaded && !summary.anyFailed));
  const totalAssets = computeTotalAssets({
    investmentAssets: summary.totalWealth,
    investmentComplete,
    cashStatus,
    cashAccounts,
  });
  const failedCount = summary.portfolios.filter((row) => row.failed).length;
  const investmentMessage = portfolioLoadError
    ? "Investment Assets unavailable — portfolios could not be loaded."
    : summary.anyFailed
    ? `Investment Assets unavailable — ${failedCount} portfolio${failedCount === 1 ? "" : "s"} failed to load.`
    : !investmentComplete
    ? "Loading current investment prices…"
    : null;
  const cashMessage = totalAssets.invalidCashAccountCount > 0 || cashStatus === "error"
    ? "Cash Accounts unavailable — Total Assets cannot be calculated."
    : cashStatus === "loading"
    ? "Loading Cash Accounts…"
    : null;

  return (
    <section className="space-y-4">
      <div className="bg-white border rounded-xl p-6 shadow-sm">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Investment Assets</p>
            <p className="text-2xl font-bold text-gray-800">{fmtMetric(totalAssets.investmentAssets)}</p>
            <p className="text-xs text-gray-400 mt-0.5">Portfolios, including brokerage cash</p>
          </div>
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Cash</p>
            <p className="text-2xl font-bold text-gray-800">{fmtMetric(totalAssets.externalCash)}</p>
            <p className="text-xs text-gray-400 mt-0.5">Active external Cash Accounts</p>
          </div>
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">Total Assets</p>
            <p className="text-2xl font-bold text-gray-800">{fmtMetric(totalAssets.totalAssets)}</p>
            <p className="text-xs text-gray-400 mt-0.5">Only shown when both sides are complete</p>
          </div>
        </div>
        {(investmentMessage || cashMessage || summary.anyEstimated || summary.anyStale) && (
          <div className="mt-3 flex flex-col gap-0.5 text-xs text-gray-400">
            {investmentMessage && <span className={summary.anyFailed || portfolioLoadError ? "text-red-500" : ""}>{investmentMessage}</span>}
            {cashMessage && <span className="text-red-500">{cashMessage}</span>}
            {!cashMessage && !investmentMessage && summary.anyEstimated && (
              <span>Some holdings use a last-known price — Investment Assets may be approximate.</span>
            )}
            {!cashMessage && !investmentMessage && summary.anyStale && (
              <span>Some holdings show a cached price because a live fetch was unavailable — Investment Assets may not be fully current.</span>
            )}
            {!cashMessage && !investmentMessage && !totalAssets.investmentComplete && totalAssets.cashComplete && (
              <span className="text-red-500">Investment Assets unavailable — Total Assets cannot be calculated.</span>
            )}
          </div>
        )}
        <Link href="/cash" className="inline-block mt-3 text-xs text-blue-600 hover:text-blue-800 font-medium">
          Manage Cash Accounts →
        </Link>
      </div>

      {portfolios.length === 0 ? (
        <div className="bg-white border rounded-xl p-8 shadow-sm text-center">
          {portfolioLoadError ? (
            <p className="text-sm text-red-500">Unable to load portfolios.</p>
          ) : (
            <>
              <p className="text-sm text-gray-500">No portfolios yet.</p>
              <Link
                href="/portfolio"
                className="inline-block mt-2 text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                Create your first portfolio →
              </Link>
            </>
          )}
        </div>
      ) : (
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
                          <span>Brokerage cash</span>
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
                          <span>Share of investment assets</span>
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
      )}
    </section>
  );
}
