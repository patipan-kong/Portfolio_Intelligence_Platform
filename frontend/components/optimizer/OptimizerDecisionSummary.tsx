import type { OptimizerResult } from "@/lib/api";
import { assessment, economicRecommendation, intentReviewSummary, primarySchedulingReason, scheduledTradeCount } from "@/lib/optimizerPresentation";

export default function OptimizerDecisionSummary({ result, historyId, historical, loading }: {
  result: OptimizerResult | null; historyId: number | null; historical: boolean; loading: boolean;
}) {
  const count = result ? scheduledTradeCount(result) : null;
  const score = assessment(result?.consensus?.consensus_strength_score ?? result?.final_consensus_score);
  const date = result?.analyzed_at ? new Date(result.analyzed_at) : null;
  return <section aria-label="Selected analysis decision" className="bg-white border border-blue-200 rounded-xl p-4 shadow-sm space-y-3 min-w-0">
    <h2 className="font-semibold text-gray-900">{historical ? "Historical analysis" : "Analysis just completed"}{historyId != null ? ` #${historyId}` : " — run identity unavailable"}</h2>
    <p className="text-xs text-gray-500">{date && !Number.isNaN(date.getTime()) ? `${date.toLocaleString("en-GB", { timeZone: "Asia/Bangkok" })} · Bangkok time` : "Analysis timestamp unavailable"}. This plan reflects the analysis time, not current prices.</p>
    {loading ? <p role="status">Loading selected analysis — recommendation and scheduled actions unavailable.</p>
      : <>
        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
          <div className="min-w-0"><dt className="text-xs text-gray-500">Economic recommendation</dt><dd className="font-semibold break-words">{result ? economicRecommendation(result) : "Recommendation unavailable"}</dd></div>
          <div><dt className="text-xs text-gray-500">Scheduled trades in this plan</dt><dd className="font-semibold">{count == null ? "Unavailable — execution evidence missing" : count}</dd></div>
          <div className="sm:col-span-2"><dt className="text-xs text-gray-500">Scheduling explanation</dt><dd>{result ? primarySchedulingReason(result) : "Scheduling reason unavailable"}</dd></div>
          <div className="sm:col-span-2"><dt className="text-xs text-gray-500">Your intent</dt><dd>{result ? intentReviewSummary(result) : "Intent review unavailable"}</dd></div>
        </dl>
        <p className="text-xs text-gray-600">{!result ? "Auditor evidence unavailable." : result.layer3_result?.claim_validation_version
          ? "Evidence-backed auditor observations are separated from unscored opinions and advisory concerns below. Unscored does not mean risk-free."
          : "Historical model claims were not independently validated by Auditor V2. They are recorded opinions, not verified policy breaches."}</p>
        <p className="text-xs text-gray-500">{score == null ? "Consensus assessment unavailable." : `Stored consensus assessment: ${score}/100.`} Scores are assessments, not probabilities of returns or investment success.</p>
      </>}
  </section>;
}
