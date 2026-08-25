"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { usePortfolio } from "@/lib/PortfolioContext";
import PortfolioTabs from "@/components/PortfolioTabs";
import DividendIncomeView from "@/components/DividendIncomeView";
import { getTransactionHistory, isUnresolvedPortfolioError } from "@/lib/api";
import type { TransactionRecord } from "@/lib/api";

// 500 is the backend's hard cap (min(limit, 500) in list_transactions) — the
// highest coverage this endpoint can give without a backend change, so
// dividend aggregation isn't silently truncated by the default limit of 100.
const MAX_TRANSACTIONS = 500;

export default function DividendIncomePage() {
  const { currentSelection: portfolioId, reportUnresolvedPortfolio } = usePortfolio();

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
      const data = await getTransactionHistory(pid, undefined, MAX_TRANSACTIONS);
      if (requestIdRef.current !== pid) return; // stale — user switched or cleared since this request began
      setTransactions(data);
    } catch (e) {
      if (requestIdRef.current !== pid) return;
      setError(e instanceof Error ? e.message : "Failed to load dividend income");
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
      <PortfolioTabs />

      <div>
        <h1 className="text-xl font-bold text-gray-900">Dividend Income</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          Actual dividend payments recorded for this portfolio — no forecasts, no yield estimates.
        </p>
      </div>

      {portfolioId == null ? (
        <p className="text-center text-gray-400 text-sm py-8">
          Select a portfolio from the navbar to view its dividend income.
        </p>
      ) : error ? (
        <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">
          {error}
          <button onClick={load} className="ml-4 underline hover:no-underline text-xs">
            Retry
          </button>
        </div>
      ) : (
        <DividendIncomeView transactions={transactions} loading={loading} />
      )}
    </main>
  );
}
