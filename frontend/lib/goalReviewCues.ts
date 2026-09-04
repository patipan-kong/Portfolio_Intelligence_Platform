import type {
  FactualReviewSource,
  GoalContextGoal,
  GoalFundingAllocationHistory,
  GoalPlanAmendmentHistory,
} from "./api";
import type { GoalAffordabilityResult } from "./goalAffordability";

export type ReviewEvidenceState<T extends object> = T | { error: string } | undefined;
export type GoalReviewAffordabilityState = GoalAffordabilityResult | { error: string } | undefined;

export type GoalReviewCueKind =
  | "DESIGNATION_GAP"
  | "TARGET_DATE_MISSING"
  | "SOURCE_OVER_ALLOCATED"
  | "SOURCE_VALUE_UNAVAILABLE"
  | "SOURCE_EVIDENCE_INCOMPLETE"
  | "SOURCE_ARCHIVED"
  | "AFFORDABILITY_SHORTFALL"
  | "AFFORDABILITY_INSUFFICIENT_DATA"
  | "PLAN_AMENDMENT"
  | "FUNDING_AMENDMENT";

export interface GoalReviewCue {
  kind: GoalReviewCueKind;
  href: string;
  sourceName?: string;
  amount?: number;
  recordedAt?: string;
  affordabilityReason?: string;
}

export type GoalReviewCueEligibility = "PRESENT" | "ABSENT" | "UNAVAILABLE";

export interface GoalReviewCuesResult {
  cues: GoalReviewCue[];
  /** Internal eligibility is explicit so a missing source never reads as an absent condition. */
  eligibility: {
    targetDate: GoalReviewCueEligibility;
    designationGap: GoalReviewCueEligibility;
    fundingSourceEvidence: GoalReviewCueEligibility;
    affordability: GoalReviewCueEligibility;
    planHistory: GoalReviewCueEligibility;
    fundingHistory: GoalReviewCueEligibility;
  };
  /** Some independent evidence is still loading or failed, so absence is not completeness. */
  hasUnavailableEvidence: boolean;
}

export interface GoalReviewCuesInput {
  /** Accepted only after Goal Detail's record/context structural agreement. */
  goalContext: ReviewEvidenceState<GoalContextGoal>;
  /** Accepted only after Goal Detail's factual-review/context structural agreement. */
  factualSources: ReviewEvidenceState<FactualReviewSource[]>;
  /** The single existing affordability evaluation; this module never recalculates it. */
  affordability: GoalReviewAffordabilityState;
  planHistory: ReviewEvidenceState<GoalPlanAmendmentHistory[]>;
  fundingHistory: ReviewEvidenceState<GoalFundingAllocationHistory[]>;
}

function isError<T extends object>(state: ReviewEvidenceState<T>): state is { error: string } {
  return state !== undefined && "error" in state;
}

function unavailable<T extends object>(state: ReviewEvidenceState<T>): boolean {
  return state === undefined || isError(state);
}

function accepted<T extends object>(state: ReviewEvidenceState<T>): state is T {
  return !unavailable(state);
}

function sourceOrder(a: FactualReviewSource, b: FactualReviewSource): number {
  if (a.source_kind !== b.source_kind) return a.source_kind < b.source_kind ? -1 : 1;
  return a.source_id - b.source_id;
}

/**
 * Pure presentation derivation over accepted Goal Detail evidence.  It adds no
 * financial calculation, freshness policy, ranking, or action instruction.
 * The fixed output order follows the detail page's information architecture:
 * current plan, designation, source evidence, affordability, then histories.
 */
export function deriveGoalReviewCues(input: GoalReviewCuesInput): GoalReviewCuesResult {
  const cues: GoalReviewCue[] = [];
  const eligibility: GoalReviewCuesResult["eligibility"] = {
    targetDate: "UNAVAILABLE",
    designationGap: "UNAVAILABLE",
    fundingSourceEvidence: "UNAVAILABLE",
    affordability: "UNAVAILABLE",
    planHistory: "UNAVAILABLE",
    fundingHistory: "UNAVAILABLE",
  };

  if (!accepted(input.goalContext)) {
  } else {
    if (input.goalContext.target_date === null) {
      cues.push({ kind: "TARGET_DATE_MISSING", href: "#planning-heading" });
      eligibility.targetDate = "PRESENT";
    } else {
      eligibility.targetDate = "ABSENT";
    }
    if (input.goalContext.designated_total < input.goalContext.target_amount) {
      cues.push({
        kind: "DESIGNATION_GAP",
        href: "#funding-heading",
        amount: input.goalContext.funding_gap,
      });
      eligibility.designationGap = "PRESENT";
    } else {
      eligibility.designationGap = "ABSENT";
    }
  }

  if (!accepted(input.factualSources)) {
  } else {
    const cueCountBeforeSources = cues.length;
    for (const source of [...input.factualSources].sort(sourceOrder)) {
      if (source.source_is_archived) {
        cues.push({ kind: "SOURCE_ARCHIVED", href: "#funding-heading", sourceName: source.source_name });
      }
      if (source.designation_coverage.status === "OVER_ALLOCATED") {
        cues.push({ kind: "SOURCE_OVER_ALLOCATED", href: "#funding-heading", sourceName: source.source_name });
      }
      if (source.valuation.availability === "UNAVAILABLE") {
        cues.push({ kind: "SOURCE_VALUE_UNAVAILABLE", href: "#funding-heading", sourceName: source.source_name });
      } else if (source.valuation.quality !== "COMPLETE") {
        cues.push({ kind: "SOURCE_EVIDENCE_INCOMPLETE", href: "#funding-heading", sourceName: source.source_name });
      } else if (source.designation_coverage.status === "UNAVAILABLE") {
        cues.push({ kind: "SOURCE_EVIDENCE_INCOMPLETE", href: "#funding-heading", sourceName: source.source_name });
      }
    }
    eligibility.fundingSourceEvidence = cues.length > cueCountBeforeSources ? "PRESENT" : "ABSENT";
  }

  if (input.affordability === undefined || "error" in input.affordability) {
  } else if (input.affordability.state === "SHORTFALL") {
    cues.push({ kind: "AFFORDABILITY_SHORTFALL", href: "#planning-heading" });
    eligibility.affordability = "PRESENT";
  } else if (input.affordability.state === "INSUFFICIENT_DATA"
    && input.affordability.reasonCode !== "REQUIRED_SIDE_INVALID") {
    cues.push({
      kind: "AFFORDABILITY_INSUFFICIENT_DATA",
      href: "#planning-heading",
      affordabilityReason: input.affordability.reason ?? undefined,
    });
    eligibility.affordability = "PRESENT";
  } else {
    // A missing target date is already represented above. Other required-side
    // invalidity (for example a past date) remains in the existing planning
    // surface rather than being mislabeled as missing cash-flow evidence.
    eligibility.affordability = "ABSENT";
  }

  if (!accepted(input.planHistory)) {
  } else if (input.planHistory.length > 0) {
    cues.push({ kind: "PLAN_AMENDMENT", href: "#plan-history-heading", recordedAt: input.planHistory[0].recorded_at });
    eligibility.planHistory = "PRESENT";
  } else {
    eligibility.planHistory = "ABSENT";
  }

  if (!accepted(input.fundingHistory)) {
  } else if (input.fundingHistory.length > 0) {
    cues.push({ kind: "FUNDING_AMENDMENT", href: "#funding-history-heading", recordedAt: input.fundingHistory[0].recorded_at });
    eligibility.fundingHistory = "PRESENT";
  } else {
    eligibility.fundingHistory = "ABSENT";
  }

  return {
    cues,
    eligibility,
    hasUnavailableEvidence: Object.values(eligibility).includes("UNAVAILABLE"),
  };
}
