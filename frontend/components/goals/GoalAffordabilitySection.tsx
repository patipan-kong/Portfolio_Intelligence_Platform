"use client";

import type { GoalAffordabilityCalendar } from "@/lib/goalAffordability";
import type { MonthlyFetchResult } from "@/lib/emergencyFund";
import { formatThb } from "./GoalPlanningSections";
import type { GoalReviewAffordabilityState } from "@/lib/goalReviewCues";

function monthWord(count: number): string {
  return `${count} completed month${count === 1 ? "" : "s"}`;
}

/**
 * The trailing months and the as-of date always travel together, from the
 * one instant the Goal page read. This component reads no clock of its own,
 * so the months that were fetched and the months that are evaluated cannot
 * drift apart on a second calendar.
 */
export interface GoalAffordabilityEvidence {
  calendar: GoalAffordabilityCalendar;
  monthlyCashFlowResults: MonthlyFetchResult[];
}

export interface GoalAffordabilitySectionProps {
  /** Evaluated once by Goal Detail from the existing affordability helper. */
  result: GoalReviewAffordabilityState;
}

/**
 * Presentational only. Goal Detail supplies the existing affordability result
 * so this section and Goal Review Cues read the same accepted evaluation.
 */
export function GoalAffordabilitySection({
  result,
}: GoalAffordabilitySectionProps) {
  if (result === undefined) {
    return <p className="text-sm text-gray-400">Checking affordability…</p>;
  }
  if ("error" in result) {
    return <p className="text-sm text-gray-500">Affordability could not be assessed: {result.error}</p>;
  }

  return (
    <div className="space-y-2 pt-3 border-t" aria-label="Goal affordability">
      <h3 className="text-sm font-semibold text-gray-700">Can I afford this goal?</h3>

      {result.state === "NO_CONTRIBUTION_REQUIRED" && (
        <p className="text-sm text-gray-700">
          This goal&apos;s designated funding already meets its target — no monthly contribution is required.
        </p>
      )}

      {result.state === "INSUFFICIENT_DATA" && (
        <p className="text-sm text-gray-500">Affordability can&apos;t be assessed yet — {result.reason}</p>
      )}

      {result.state === "AFFORDABLE" && result.requiredMonthlyContribution !== null && result.observedMonthlySurplus !== null && (
        <p className="text-sm text-gray-700">
          Based on your recorded cash flow over the last {monthWord(result.evidenceMonthCount)}, your average monthly
          surplus is {formatThb(result.observedMonthlySurplus)}, enough to cover the{" "}
          {formatThb(result.requiredMonthlyContribution)}/month this goal needs.
        </p>
      )}

      {result.state === "SHORTFALL" && result.requiredMonthlyContribution !== null && result.observedMonthlySurplus !== null && result.affordabilityGap !== null && (
        <p className="text-sm text-gray-700">
          Based on your recorded cash flow over the last {monthWord(result.evidenceMonthCount)}, your average monthly
          surplus is {formatThb(result.observedMonthlySurplus)}, which is {formatThb(Math.abs(result.affordabilityGap))}{" "}
          short of the {formatThb(result.requiredMonthlyContribution)}/month this goal needs.
        </p>
      )}

      {(result.state === "AFFORDABLE" || result.state === "SHORTFALL") && (
        <p className="text-xs text-gray-500">
          This reflects recorded cash flow in your tracked accounts only. It is not reserved for this goal and may
          already be committed elsewhere. Each goal is evaluated independently.
        </p>
      )}
    </div>
  );
}
