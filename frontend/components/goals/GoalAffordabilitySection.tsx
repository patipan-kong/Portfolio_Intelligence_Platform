"use client";

import { computeGoalAffordability, type GoalAffordabilityCalendar } from "@/lib/goalAffordability";
import type { CashAccountsFetchStatus, MonthlyFetchResult } from "@/lib/emergencyFund";
import type { CashAccount } from "@/lib/api";
import { formatThb, type GoalContextState } from "./GoalPlanningSections";

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
  goalContext: GoalContextState;
  /** undefined while the trailing 3-month Cash Flow fetch is still in flight. */
  evidence: GoalAffordabilityEvidence | undefined;
  cashAccountsStatus: CashAccountsFetchStatus;
  cashAccounts: CashAccount[];
}

/**
 * Presentational only. All affordability semantics live in
 * computeGoalAffordability (frontend/lib/goalAffordability.ts) — this
 * component renders its result and never derives a number of its own.
 */
export function GoalAffordabilitySection({
  goalContext,
  evidence,
  cashAccountsStatus,
  cashAccounts,
}: GoalAffordabilitySectionProps) {
  if (goalContext === undefined || evidence === undefined) {
    return <p className="text-sm text-gray-400">Checking affordability…</p>;
  }
  if ("error" in goalContext) {
    return <p className="text-sm text-gray-500">Affordability could not be assessed: {goalContext.error}</p>;
  }

  const result = computeGoalAffordability({
    targetAmount: goalContext.target_amount,
    startingValue: goalContext.designated_total,
    asOfDate: evidence.calendar.asOfDate,
    targetDate: goalContext.target_date,
    trailingCompletedMonths: evidence.calendar.trailingCompletedMonths,
    monthlyCashFlowResults: evidence.monthlyCashFlowResults,
    cashAccountsStatus,
    cashAccounts,
  });

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
