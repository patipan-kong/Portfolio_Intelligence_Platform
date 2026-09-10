"use client";

// Periodic Review (Slice 1) — "What changed, and what deserves review?"
// Pure frontend composition over four already-canonical domains, each
// fetched and rendered independently so one domain's failure never hides
// another's. Fixed domain order only: Net Worth, Goals, Execution,
// Evaluation — no cross-domain ranking, no synthesized urgency.

import { usePortfolio } from "@/lib/PortfolioContext";
import NetWorthReviewSection from "@/components/review/NetWorthReviewSection";
import GoalsReviewSection from "@/components/review/GoalsReviewSection";
import ExecutionReviewSection from "@/components/review/ExecutionReviewSection";
import EvaluationReviewSection from "@/components/review/EvaluationReviewSection";

export default function PeriodicReviewPage() {
  const { portfolios, currentSelection } = usePortfolio();
  const selectedPortfolio = portfolios.find((p) => p.id === currentSelection) ?? null;

  return (
    <div className="space-y-8 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold">Periodic Review</h1>
        <p className="text-sm text-gray-500 mt-1">What changed, and what deserves review?</p>
      </div>

      <NetWorthReviewSection />
      <GoalsReviewSection />

      <p className="text-xs text-gray-400 pt-2 border-t">
        {selectedPortfolio
          ? `Execution and evaluation reflect ${selectedPortfolio.name}.`
          : "Execution and evaluation reflect the currently selected portfolio."}
      </p>

      <ExecutionReviewSection />
      <EvaluationReviewSection />
    </div>
  );
}
