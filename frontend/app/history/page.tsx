"use client";

import { useEffect, useState, useCallback, useRef, useMemo } from "react";
import { usePortfolio } from "@/lib/PortfolioContext";
import PortfolioTabs from "@/components/PortfolioTabs";
import TransactionHistoryTable, { TYPE_STYLE } from "@/components/TransactionHistoryTable";
import { getTransactionHistory, isUnresolvedPortfolioError } from "@/lib/api";
import type { TransactionRecord, TransactionType } from "@/lib/api";
import { DEFAULT_FILTERS, filterTransactions, hasActiveFilters, type TransactionFilters } from "@/lib/transactionFilters";
import { transactionsToCsv, buildExportFilename, CSV_UTF8_BOM } from "@/lib/csvExport";

const TYPE_OPTIONS = Object.entries(TYPE_STYLE) as [TransactionType, { label: string }][];

// The history endpoint hard-caps at 500 server-side (backend/main.py). Export
// draws from the same fetched array as the on-screen history — no second,
// export-only request — so requesting the endpoint's actual maximum here is
// what makes "Exports up to the most recent 500 transactions" true.
const HISTORY_FETCH_LIMIT = 500;

export default function TransactionHistoryPage() {
  const { currentSelection: portfolioId, portfolios, reportUnresolvedPortfolio } = usePortfolio();

  // Captures the portfolio a request was issued for, so a response that
  // lands after the user has switched portfolios (or cleared selection) is
  // ignored instead of repopulating the page with the wrong portfolio's data.
  const requestIdRef = useRef<number | null>(null);
  const [transactions, setTransactions] = useState<TransactionRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<TransactionFilters>(DEFAULT_FILTERS);

  const load = useCallback(async () => {
    if (portfolioId == null) return;
    const pid = portfolioId;
    setLoading(true);
    setError(null);
    try {
      const data = await getTransactionHistory(pid, undefined, HISTORY_FETCH_LIMIT);
      if (requestIdRef.current !== pid) return; // stale — user switched or cleared since this request began
      setTransactions(data);
    } catch (e) {
      if (requestIdRef.current !== pid) return;
      setError(e instanceof Error ? e.message : "Failed to load transaction history");
      if (isUnresolvedPortfolioError(e)) reportUnresolvedPortfolio(pid);
    } finally {
      if (requestIdRef.current === pid) setLoading(false);
    }
  }, [portfolioId, reportUnresolvedPortfolio]);

  useEffect(() => {
    requestIdRef.current = portfolioId;
    // A newly selected portfolio starts unfiltered — carrying a search term,
    // type, or date range over from the previous portfolio would silently
    // hide data with no visible reason on the new one.
    setFilters(DEFAULT_FILTERS);
    if (portfolioId == null) {
      setTransactions([]);
      setError(null);
      setLoading(false);
      return;
    }
    load();
  }, [portfolioId, load]);

  // Filtering is purely client-side over the already-fetched array — it
  // never triggers another getTransactionHistory() request.
  const filtered = useMemo(() => filterTransactions(transactions, filters), [transactions, filters]);
  const filtersActive = hasActiveFilters(filters);
  const clearFilters = () => setFilters(DEFAULT_FILTERS);

  // Exports the loaded history (`transactions`), not the filtered view
  // (`filtered`) — search/type/date are viewing tools, so "Export CSV"
  // means the bounded history currently loaded for this portfolio.
  function handleExport() {
    if (portfolioId == null || transactions.length === 0) return;
    const csv = transactionsToCsv(transactions);
    const blob = new Blob([CSV_UTF8_BOM + csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    const portfolioName = portfolios.find((p) => p.id === portfolioId)?.name ?? null;
    a.download = buildExportFilename(portfolioName, new Date().toISOString().slice(0, 10));
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <main className="max-w-5xl mx-auto px-4 py-6 space-y-6">
      {/* Portfolio hub tabs (Phase 4C.2A) */}
      <PortfolioTabs />

      <div>
        <h1 className="text-xl font-bold text-gray-900">Transaction History</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          {transactions.length > 0
            ? `${transactions.length} transaction${transactions.length !== 1 ? "s" : ""}`
            : "Every buy, sell, deposit, withdrawal, and correction recorded for this portfolio"}
        </p>
      </div>

      {portfolioId == null ? (
        <p className="text-center text-gray-400 text-sm py-8">
          Select a portfolio from the navbar to view its transaction history.
        </p>
      ) : error ? (
        <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">
          {error}
          <button onClick={load} className="ml-4 underline hover:no-underline text-xs">
            Retry
          </button>
        </div>
      ) : loading ? (
        <div className="space-y-3">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-14 animate-pulse bg-gray-100 rounded-xl" />
          ))}
        </div>
      ) : transactions.length === 0 ? (
        <TransactionHistoryTable transactions={[]} />
      ) : (
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row sm:flex-wrap sm:items-center gap-2">
            <input
              type="text"
              value={filters.search}
              onChange={(e) => setFilters((f) => ({ ...f, search: e.target.value }))}
              placeholder="Search symbol or notes"
              aria-label="Search transactions"
              className="flex-1 min-w-0 border rounded-lg px-3 py-1.5 text-sm"
            />
            <select
              value={filters.type}
              onChange={(e) => setFilters((f) => ({ ...f, type: e.target.value as TransactionFilters["type"] }))}
              aria-label="Transaction type"
              className="border rounded-lg px-2 py-1.5 text-sm"
            >
              <option value="ALL">All types</option>
              {TYPE_OPTIONS.map(([type, meta]) => (
                <option key={type} value={type}>{meta.label}</option>
              ))}
            </select>
            <div className="flex items-center gap-1 text-sm text-gray-500">
              <label htmlFor="history-from-date">From</label>
              <input
                id="history-from-date"
                type="date"
                value={filters.from}
                onChange={(e) => setFilters((f) => ({ ...f, from: e.target.value }))}
                className="border rounded-lg px-2 py-1.5 text-sm"
              />
            </div>
            <div className="flex items-center gap-1 text-sm text-gray-500">
              <label htmlFor="history-to-date">To</label>
              <input
                id="history-to-date"
                type="date"
                value={filters.to}
                onChange={(e) => setFilters((f) => ({ ...f, to: e.target.value }))}
                className="border rounded-lg px-2 py-1.5 text-sm"
              />
            </div>
            {filtersActive && (
              <button
                onClick={clearFilters}
                className="text-xs text-blue-700 underline hover:no-underline whitespace-nowrap"
              >
                Clear filters
              </button>
            )}
            <div className="flex items-center gap-2 sm:ml-auto">
              <button
                type="button"
                onClick={handleExport}
                className="text-xs border rounded-lg px-3 py-1.5 text-gray-700 hover:bg-gray-50 whitespace-nowrap"
              >
                Export CSV
              </button>
              <span className="text-xs text-gray-400 whitespace-nowrap">
                Exports up to the most recent {HISTORY_FETCH_LIMIT} transactions.
              </span>
            </div>
          </div>

          {filtersActive && (
            <p className="text-xs text-gray-500">
              {filtered.length} of {transactions.length} transaction{transactions.length !== 1 ? "s" : ""}
            </p>
          )}

          {filtered.length === 0 ? (
            <p className="text-gray-500 text-sm py-8 text-center">
              No transactions match these filters.
            </p>
          ) : (
            <TransactionHistoryTable transactions={filtered} />
          )}
        </div>
      )}
    </main>
  );
}
