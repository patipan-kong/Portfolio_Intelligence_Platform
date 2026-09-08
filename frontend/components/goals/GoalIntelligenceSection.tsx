import type { GoalIntelligenceResponse } from "@/lib/api";
import { formatThb } from "./GoalPlanningSections";

export type GoalIntelligenceState = GoalIntelligenceResponse | { error: string } | undefined;

function sourceKindLabel(kind: GoalIntelligenceResponse["funding_sources"][number]["source_kind"]): string {
  return kind === "CASH_ACCOUNT" ? "Cash Account" : "Portfolio";
}

function timeLabel(time: GoalIntelligenceResponse["time"]): string {
  if (!time.has_target_date) return "No target date is set for this goal.";
  if (time.target_date_in_past) {
    return `Target date ${time.target_date} has passed (${Math.abs(time.days_remaining as number)} days ago).`;
  }
  if (time.days_remaining === 0) return `Target date is today (${time.target_date}).`;
  return `${time.days_remaining} days remaining until ${time.target_date}.`;
}

function coverageLabel(status: GoalIntelligenceResponse["funding_sources"][number]["designation_coverage"]["status"]): string {
  if (status === "SUPPORTED") return "Observed value supports this designation.";
  if (status === "OVER_ALLOCATED") return "Total designated to this source exceeds its observed value.";
  return "Valuation evidence unavailable for this source.";
}

function valuationDisplay(source: GoalIntelligenceResponse["funding_sources"][number]): string {
  const { valuation } = source;
  if (valuation.observed_value === null) return "Observed value unavailable";
  return `${formatThb(valuation.observed_value)} observed${valuation.as_of ? ` as of ${valuation.as_of}` : ""}`;
}

function completenessLabel(status: GoalIntelligenceResponse["valuation_completeness"]): string {
  if (status === "COMPLETE") return "All relevant funding-source valuations are complete.";
  if (status === "PARTIAL") return "Some funding-source valuations are incomplete or unavailable.";
  return "Funding-source valuation evidence is unavailable.";
}

export function GoalIntelligenceSection({ state }: { state: GoalIntelligenceState }) {
  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="goal-intelligence-heading">
      <h2 id="goal-intelligence-heading" className="text-lg font-semibold">Goal Intelligence</h2>
      <p className="text-xs text-gray-500">
        Descriptive facts composed from Funding and Factual Wealth Review evidence. No health rating
        or recommendation is computed here.
      </p>
      {state === undefined ? (
        <p className="text-sm text-gray-400">Loading Goal Intelligence…</p>
      ) : "error" in state ? (
        <p role="alert" className="text-sm text-red-600">{state.error || "Unable to load Goal Intelligence."}</p>
      ) : (
        <div className="space-y-3">
          <dl className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
            <dt className="text-gray-500">Designated total</dt>
            <dd className="text-gray-800">{formatThb(state.funding.designated_total)}</dd>
            <dt className="text-gray-500">Remaining to target</dt>
            <dd className="text-gray-800">{formatThb(state.funding.funding_gap)}</dd>
            <dt className="text-gray-500">Designation progress</dt>
            <dd className="text-gray-800">{(state.funding.progress_ratio * 100).toFixed(1)}%{state.funding.fully_designated ? " (fully designated)" : ""}</dd>
          </dl>

          <p className="text-sm text-gray-700">{timeLabel(state.time)}</p>

          <p className="text-xs text-gray-500">{completenessLabel(state.valuation_completeness)}</p>

          {state.funding_sources.length > 0 && (
            <div className="pt-2 border-t space-y-1">
              <h3 className="text-sm font-semibold text-gray-700">Funding sources</h3>
              {state.funding_sources.map((source) => (
                <div key={`${source.source_kind}:${source.source_id}`} className="text-xs text-gray-500">
                  <p>
                    {source.source_name}{source.source_is_archived ? " (archived)" : ""}
                    {" "}({sourceKindLabel(source.source_kind)}): designated {formatThb(source.goal_designated_amount)}
                    {source.source_designated_total_in_context_scope !== source.goal_designated_amount
                      && ` · ${formatThb(source.source_designated_total_in_context_scope)} designated to this source across all goals`}
                  </p>
                  <p>{valuationDisplay(source)} · {coverageLabel(source.designation_coverage.status)}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  );
}
