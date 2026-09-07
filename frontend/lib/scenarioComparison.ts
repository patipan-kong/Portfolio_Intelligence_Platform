// Scenario Comparison — pure composition over the existing deterministic
// What-If engine. Compares two saved Scenarios' assumptions (monthly
// contribution, annual return) against ONE shared current context: the
// goal's current target amount, current target date, and current
// designated funding. Never each scenario's save-time context, which is
// not persisted (see goalWhatIf.ts, goalFunding.ts).
//
// This module presents facts only — no ranking, scoring, or "winner". It
// reuses computeGoalWhatIf and computeRequiredMonthlyContribution verbatim;
// no projection math is duplicated here.

import {
  computeGoalWhatIf,
  computeRequiredMonthlyContribution,
  type GoalWhatIfResult,
  type RequiredMonthlyContributionResult,
} from "./goalWhatIf.ts";

export interface ScenarioComparisonAssumptions {
  name: string;
  monthlyContribution: number;
  annualReturnPct: number;
}

export interface ScenarioComparisonSide {
  name: string;
  monthlyContribution: number;
  annualReturnPct: number;
  whatIf: GoalWhatIfResult;
  /** Independent of this side's own monthlyContribution — see module docs. */
  requiredContribution: RequiredMonthlyContributionResult;
}

export interface ScenarioComparisonContext {
  targetAmount: number;
  startingValue: number;
  /** Echoed current goal target date, or null when the goal has none. */
  targetDate: string | null;
  asOfDate: string;
}

export interface ScenarioComparisonResult {
  valid: true;
  context: ScenarioComparisonContext;
  a: ScenarioComparisonSide;
  b: ScenarioComparisonSide;
}

export interface ScenarioComparisonUnavailable {
  valid: false;
  error: string;
}

export type ScenarioComparisonOutcome = ScenarioComparisonResult | ScenarioComparisonUnavailable;

function computeSide(
  assumptions: ScenarioComparisonAssumptions,
  targetAmount: number,
  startingValue: number,
  asOfDate: string,
  targetDate: string | null,
): ScenarioComparisonSide {
  return {
    name: assumptions.name,
    monthlyContribution: assumptions.monthlyContribution,
    annualReturnPct: assumptions.annualReturnPct,
    whatIf: computeGoalWhatIf({
      targetAmount,
      startingValue,
      monthlyContribution: assumptions.monthlyContribution,
      annualReturnPct: assumptions.annualReturnPct,
      asOfDate,
      targetDate,
    }),
    // computeRequiredMonthlyContribution already returns valid:false with an
    // honest error ("A saved target date is required…" / "…has passed") for
    // the null/past target-date cases — no duplicate branching needed here.
    requiredContribution: computeRequiredMonthlyContribution({
      targetAmount,
      startingValue,
      annualReturnPct: assumptions.annualReturnPct,
      asOfDate,
      targetDate,
    }),
  };
}

/**
 * `startingValue === null` means designated funding could not be honestly
 * determined (allocation evidence failed to load) — the comparison is
 * unavailable, never computed against a fabricated zero.
 */
export function computeScenarioComparison(
  targetAmount: number,
  startingValue: number | null,
  targetDate: string | null | undefined,
  asOfDate: string,
  scenarioA: ScenarioComparisonAssumptions,
  scenarioB: ScenarioComparisonAssumptions,
): ScenarioComparisonOutcome {
  if (startingValue === null) {
    return { valid: false, error: "Comparison unavailable — designated funding could not be loaded." };
  }
  const normalizedTargetDate = targetDate ?? null;
  return {
    valid: true,
    context: { targetAmount, startingValue, targetDate: normalizedTargetDate, asOfDate },
    a: computeSide(scenarioA, targetAmount, startingValue, asOfDate, normalizedTargetDate),
    b: computeSide(scenarioB, targetAmount, startingValue, asOfDate, normalizedTargetDate),
  };
}
