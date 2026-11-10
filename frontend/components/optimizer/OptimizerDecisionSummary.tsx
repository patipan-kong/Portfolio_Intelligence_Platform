import type { OptimizerResult } from "@/lib/api";
import { OPTIMIZER_POLICY_MUJI_V2, assessment, economicRecommendation, executionEvidenceAvailable, intentReviewSummary, primarySchedulingReason, scheduledTradeCount } from "@/lib/optimizerPresentation";

export default function OptimizerDecisionSummary({ result, historyId, historical, loading }: {
  result: OptimizerResult | null; historyId: number | null; historical: boolean; loading: boolean;
}) {
  const count = result ? scheduledTradeCount(result) : null;
  const score = assessment(result?.consensus?.consensus_strength_score ?? result?.final_consensus_score);
  const date = result?.analyzed_at ? new Date(result.analyzed_at) : null;
  const muji = result?.active_policy?.optimizer_policy_mode === OPTIMIZER_POLICY_MUJI_V2;
  const schedule = result && muji && executionEvidenceAvailable(result)
    ? result.execution_optimization : null;
  const actions = result?.target_allocations ?? [];
  const projectedCash = schedule?.idle_cash_after;
  const friction = schedule?.estimated_trade_costs
    ? Object.values(schedule.estimated_trade_costs).reduce((sum, amount) => sum + amount, 0) : null;
  return <section aria-label="Selected analysis decision" className="bg-white border border-blue-200 rounded-xl p-4 shadow-sm space-y-3 min-w-0">
    <h2 className="font-semibold text-gray-900">{historical ? "Historical analysis" : "Analysis just completed"}{historyId != null ? ` #${historyId}` : " — run identity unavailable"}</h2>
    <p className="text-xs text-gray-500">{date && !Number.isNaN(date.getTime()) ? `${date.toLocaleString("en-GB", { timeZone: "Asia/Bangkok" })} · Bangkok time` : "Analysis timestamp unavailable"}. This plan reflects the analysis time, not current prices.</p>
    {loading ? <p role="status">Loading selected analysis — recommendation and scheduled actions unavailable.</p>
      : <>
        {muji && <div className="space-y-3 text-sm" data-testid="muji-primary-result">
          <div><h3 className="font-semibold">Portfolio Outlook</h3>
            <p>Market regime: {result?.market_regime?.regime?.replace(/_/g, " ") ?? "Unavailable"}.</p>
            <p>{result?.portfolio_assessment || "Portfolio assessment unavailable."}</p>
            <p className="text-xs text-gray-500">Goal alignment: {result?.goal_recommendation_constraints
              ? "Recorded goal constraint context available below; goal-achievement probability unavailable."
              : "Goal evidence unavailable."}</p></div>
          <div><h3 className="font-semibold">Key Reasons</h3>
            <p>{result?.consensus?.recommended_action || result?.optimization_notes || "Recorded investment rationale unavailable."}</p>
            <p className="text-xs text-gray-500">Portfolio risk: {result?.layer3_result?.final_risk_level
              ? `${result.layer3_result.final_risk_level} (recorded Auditor assessment)` : "Unavailable"}.
              Model opinions are not independently verified investment outcomes.</p></div>
          <div><h3 className="font-semibold">Recommended Actions</h3>
            {actions.length ? <ul className="space-y-1">{actions.map((allocation) => {
              const sale = schedule?.trades.find((trade) => trade.symbol === allocation.symbol);
              const buy = schedule?.scheduled_buys?.[allocation.symbol];
              const amount = sale?.executed_amount || buy || 0;
              const status = !schedule ? "Schedule unavailable"
                : amount > 0 ? `Scheduled advisory THB ${amount.toLocaleString("en-US", { maximumFractionDigits: 2 })}`
                : sale?.evidence_status === "UNVERIFIED" ? "Unverified — deferred"
                : allocation.action === "HOLD" || allocation.action === "WATCH" ? "No trade scheduled"
                : "Deferred — no trade scheduled";
              return <li key={allocation.symbol}><strong>{sale?.original_action || allocation.action} {allocation.symbol}</strong>
                {allocation.reason ? ` — ${allocation.reason}` : ""} <span className="text-gray-500">· {status}</span></li>;
            })}</ul> : <p>Recommendation unavailable.</p>}
            {schedule && <p>CASH: estimated after scheduled actions THB {projectedCash?.toLocaleString("en-US", { maximumFractionDigits: 2 }) ?? "unavailable"}; no cash transaction recorded by this plan.</p>}
          </div>
          <div><h3 className="font-semibold">Expected Impact &amp; Uncertainty</h3>
            <p>{schedule ? `Estimated trading friction (0.15% per side) THB ${friction?.toLocaleString("en-US", { maximumFractionDigits: 2 }) ?? "unavailable"}; starting cash THB ${schedule.cash_available.toLocaleString("en-US", { maximumFractionDigits: 2 })}.`
              : "Estimated monetary impact unavailable — frozen schedule evidence is missing or unsupported."}</p>
            <p className="text-xs text-gray-500">Advisory estimates only. Settlement, broker fees, returns, downside outcomes, and goal-achievement probability are unavailable.</p></div>
          <div><h3 className="font-semibold">Doing Nothing</h3><p>{result?.no_action_summary ||
            "Quantified HOLD comparison unavailable."}</p></div>
        </div>}
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
