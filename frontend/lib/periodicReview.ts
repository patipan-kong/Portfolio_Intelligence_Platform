// Periodic Review presentation adapter (Slice 1). Deliberately performs no
// financial arithmetic, no Goal health/attention classification, and no
// cross-domain ranking. Every function here is selection, filtering, or
// presentation ordering over facts already computed by an existing
// canonical service.

import { factualReviewMatchesGoalContext } from "./goalFunding.ts";
import type { FactualReviewResponse, GoalContextGoal, WealthGoal } from "@/lib/api";

/**
 * Current, active (non-archived) Goals for the "Current goals" section —
 * a factual snapshot, never a "recently changed" or "needs review" claim.
 * Reuses the exact same structural-coherence check `/goals` performs before
 * trusting Goal Context against the goal record list, minus the per-field
 * drift check that page needs only because it just performed a mutation.
 * Returns null when the two responses are not coherent with each other —
 * callers must render this as "unavailable", never as an empty goal list.
 */
export function selectActiveGoalSummaries(
  goals: WealthGoal[],
  review: FactualReviewResponse
): GoalContextGoal[] | null {
  const context = review.goal_context;
  const coherent =
    review.contract_version === "wealth.factual-review.v1" &&
    review.scope.kind === "WORKSPACE" &&
    review.scope.include_archived === true &&
    factualReviewMatchesGoalContext(review) &&
    context.contract_version === "wealth.goal-context.v1" &&
    context.completeness === "COMPLETE" &&
    context.scope.kind === "WORKSPACE" &&
    context.scope.include_archived === true &&
    context.goals.length === goals.length &&
    goals.every((goal) => context.goals.some((candidate) => candidate.id === goal.id));

  if (!coherent) return null;

  return context.goals
    .filter((goal) => !goal.is_archived)
    .slice()
    .sort((a, b) => (a.name === b.name ? a.id - b.id : a.name < b.name ? -1 : 1));
}
