import type {
  GoalContextAllocation,
  GoalContextGoal,
  GoalContextResponse,
  LegacyGoalDateComparison,
  LegacyGoalProfileEvidenceEdge,
  LegacyGoalProfileEvidenceResponse,
  LegacyGoalProfileProjectionStatus,
  LegacyGoalTypeComparison,
} from "@/lib/api";

function sameScope(
  left: LegacyGoalProfileEvidenceResponse["scope"],
  right: LegacyGoalProfileEvidenceResponse["scope"],
): boolean {
  return left.kind === right.kind
    && left.include_archived === right.include_archived
    && left.goal_id === right.goal_id;
}

function sameContextGoal(left: GoalContextGoal, right: GoalContextGoal): boolean {
  return sameGoal(left, right)
    && left.designated_total === right.designated_total
    && left.progress_ratio === right.progress_ratio
    && left.progress_percent === right.progress_percent
    && left.funding_gap === right.funding_gap
    && left.fully_designated === right.fully_designated
    && left.allocations.length === right.allocations.length
    && left.allocations.every((allocation, index) => sameDesignation(allocation, right.allocations[index]));
}

function sameGoal(edge: LegacyGoalProfileEvidenceEdge["wealth_goal"], goal: GoalContextGoal): boolean {
  return edge.id === goal.id
    && edge.name === goal.name
    && edge.goal_type === goal.goal_type
    && edge.target_amount === goal.target_amount
    && edge.currency === goal.currency
    && edge.target_date === goal.target_date
    && edge.priority === goal.priority
    && edge.is_archived === goal.is_archived
    && edge.updated_at === goal.updated_at;
}

function sameDesignation(left: GoalContextAllocation, right: GoalContextAllocation): boolean {
  return left.id === right.id
    && left.wealth_goal_id === right.wealth_goal_id
    && left.source_kind === right.source_kind
    && left.source_id === right.source_id
    && left.source_name === right.source_name
    && left.source_is_archived === right.source_is_archived
    && left.designated_amount === right.designated_amount
    && left.currency === right.currency
    && left.updated_at === right.updated_at;
}

/**
 * Checks structural parity with the embedded Goal Context. It deliberately
 * treats the backend's projection and comparison facts as opaque values.
 */
export function legacyEvidenceMatchesGoalContext(response: LegacyGoalProfileEvidenceResponse): boolean {
  const context = response.goal_context;
  if (response.contract_version !== "wealth.legacy-profile-evidence.v1"
    || response.completeness !== "COMPLETE"
    || context.contract_version !== "wealth.goal-context.v1"
    || context.completeness !== "COMPLETE"
    || !sameScope(response.scope, context.scope)) return false;

  const portfolioAllocations = new Map<number, { goal: GoalContextGoal; allocation: GoalContextAllocation }>();
  for (const goal of context.goals) {
    for (const allocation of goal.allocations) {
      if (allocation.source_kind !== "PORTFOLIO") continue;
      if (portfolioAllocations.has(allocation.id)) return false;
      portfolioAllocations.set(allocation.id, { goal, allocation });
    }
  }
  if (portfolioAllocations.size !== response.evidence_edges.length) return false;

  const seen = new Set<number>();
  for (const edge of response.evidence_edges) {
    const expected = portfolioAllocations.get(edge.designation.id);
    if (!expected || seen.has(edge.designation.id)
      || edge.designation.source_kind !== "PORTFOLIO"
      || edge.portfolio.id !== edge.designation.source_id
      || edge.portfolio.name !== edge.designation.source_name
      || !sameGoal(edge.wealth_goal, expected.goal)
      || !sameDesignation(edge.designation, expected.allocation)) return false;
    seen.add(edge.designation.id);
  }
  return true;
}

export function evidenceEdgesForGoal(
  response: LegacyGoalProfileEvidenceResponse,
  goalId: number,
): LegacyGoalProfileEvidenceEdge[] | null {
  if (!legacyEvidenceMatchesGoalContext(response)) return null;
  return response.evidence_edges.filter((edge) => edge.wealth_goal.id === goalId);
}

/** Requires the supplemental response to describe the same current facts already accepted by Goal Detail. */
export function legacyEvidenceMatchesReferenceGoalContext(
  response: LegacyGoalProfileEvidenceResponse,
  reference: GoalContextResponse,
): boolean {
  const embedded = response.goal_context;
  if (!legacyEvidenceMatchesGoalContext(response)
    || !sameScope(embedded.scope, reference.scope)
    || embedded.goals.length !== reference.goals.length
    || embedded.designation_by_source.length !== reference.designation_by_source.length) return false;

  return embedded.goals.every((goal, index) => sameContextGoal(goal, reference.goals[index]))
    && embedded.designation_by_source.every((source, index) => {
      const expected = reference.designation_by_source[index];
      return source.source_kind === expected.source_kind
        && source.source_id === expected.source_id
        && source.source_name === expected.source_name
        && source.source_is_archived === expected.source_is_archived
        && source.currency === expected.currency
        && source.designated_total_in_context_scope === expected.designated_total_in_context_scope;
    });
}

export function projectionStatusLabel(status: LegacyGoalProfileProjectionStatus): string {
  return {
    UNSET: "not recorded",
    UNCHANGED: "recorded as recognized",
    NORMALIZED: "compatibility-normalized",
    UNRECOGNIZED: "recorded but unrecognized",
  }[status];
}

export function goalTypeComparisonLabel(comparison: LegacyGoalTypeComparison): string {
  return {
    SAME_RECORDED_CODE: "The recorded codes are identical.",
    DIFFERENT_RECORDED_CODES: "The recorded codes are different.",
    NOT_COMPARABLE: "The recorded codes are not comparable.",
  }[comparison];
}

export function targetDateComparisonLabel(comparison: LegacyGoalDateComparison): string {
  return {
    SAME_RECORDED_DATE: "The strict recorded dates are identical.",
    DIFFERENT_RECORDED_DATES: "The strict recorded dates are different.",
    NOT_COMPARABLE: "The recorded dates are not comparable.",
  }[comparison];
}

export function recordedValue(value: string | number | null): string {
  if (value === null) return "Not recorded";
  if (typeof value === "string" && value.length === 0) return "(empty string)";
  return String(value);
}
