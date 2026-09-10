"use client";

// Periodic Review — Evaluation section (Slice 1). Surfaces only the latest
// verdict + as_of — the coarsest honest "what changed" signal. Deliberately
// does NOT render Recent Grades or the Belief/Execution/Outcome scorecard;
// that content already has a canonical home at /ai-analytics and repeating
// it here would be pure duplication, not new evidence.

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePortfolio } from "@/lib/PortfolioContext";
import { getEvaluationScorecard, isUnresolvedPortfolioError, type EvaluationScorecard } from "@/lib/api";

const PERIOD_DAYS = 90;

type LoadState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "loaded"; data: EvaluationScorecard };

export default function EvaluationReviewSection() {
  const { currentSelection, reportUnresolvedPortfolio } = usePortfolio();
  const [state, setState] = useState<LoadState>({ status: "loading" });
  const requestIdRef = useRef<number | null>(null);

  const load = useCallback(async (portfolioId: number) => {
    setState({ status: "loading" });
    try {
      const result = await getEvaluationScorecard(portfolioId, PERIOD_DAYS);
      if (requestIdRef.current !== portfolioId) return;
      setState({ status: "loaded", data: result });
    } catch (e) {
      if (requestIdRef.current !== portfolioId) return;
      setState({ status: "error", message: e instanceof Error ? e.message : "Failed to load evaluation" });
      if (isUnresolvedPortfolioError(e)) reportUnresolvedPortfolio(portfolioId);
    }
  }, [reportUnresolvedPortfolio]);

  useEffect(() => {
    requestIdRef.current = currentSelection;
    if (currentSelection == null) return;
    void load(currentSelection);
  }, [currentSelection, load]);

  return (
    <section className="space-y-3">
      <h2 className="text-lg font-semibold">Evaluation</h2>
      {currentSelection == null ? (
        <p className="text-sm text-gray-400">Select a portfolio to view Evaluation.</p>
      ) : state.status === "loading" ? (
        <p className="text-sm text-gray-400">Loading evaluation…</p>
      ) : state.status === "error" ? (
        <p role="alert" className="text-sm text-red-600">{state.message}</p>
      ) : state.data.status === "cold_start" ? (
        <p className="text-sm text-gray-500">No recommendations to evaluate yet.</p>
      ) : (
        <div className="space-y-1.5">
          <p className="text-sm text-gray-800">{state.data.verdict.th}</p>
          <p className="text-xs text-gray-400">{state.data.verdict.en}</p>
          <p className="text-xs text-gray-400">As of {state.data.as_of.slice(0, 10)}</p>
          <Link href="/ai-analytics" className="text-xs font-semibold text-blue-600 hover:underline inline-block">
            Full AI Scorecard →
          </Link>
        </div>
      )}
    </section>
  );
}
