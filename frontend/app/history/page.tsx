"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { usePortfolio } from "@/lib/PortfolioContext";
import PortfolioTabs from "@/components/PortfolioTabs";
import TransactionHistoryTable from "@/components/TransactionHistoryTable";
import { getTransactionHistory, isUnresolvedPortfolioError } from "@/lib/api";
import type { TransactionRecord } from "@/lib/api";

export default function TransactionHistoryPage() {
  const { currentSelection: portfolioId, reportUnresolvedPortfolio } = usePortfolio();

  // Captures the portfolio a request was issued for, so a response that
  // lands after the user has switched portfolios (or cleared selection) is
  // ignored instead of repopulating the page with the wrong portfolio's data.
  const requestIdRef = useRef<number | null>(null);
  const [transactions, setTransactions] = useState<TransactionRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (portfolioId == null) return;
    const pid = portfolioId;
    setLoading(true);
    setError(null);
    try {
      const data = await getTransactionHistory(pid);
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
    if (portfolioId == null) {
      setTransactions([]);
      setError(null);
      setLoading(false);
      return;
    }
    load();
  }, [portfolioId, load]);

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
      ) : (
        <TransactionHistoryTable transactions={transactions} />
      )}
    </main>
  );
}
