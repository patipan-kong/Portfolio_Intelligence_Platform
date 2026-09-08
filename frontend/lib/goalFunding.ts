// Funding Health presentation adapters over the server-owned factual review.
// This module deliberately performs no designation, valuation, coverage, or
// shortfall arithmetic.

import type {
  FactualReviewSource,
  FactualReviewResponse,
  FactualReviewValuationProvenance,
  FactualReviewValuationQuality,
  GoalContextGoal,
  GoalFundingSourceKind,
} from "@/lib/api";

export type FundingSourceKey = `${GoalFundingSourceKind}:${number}`;

export function sourceKey(kind: GoalFundingSourceKind, id: number): FundingSourceKey {
  return `${kind}:${id}`;
}

export type FundingHealthStatus = "SUPPORTED" | "OVER_ALLOCATED" | "UNAVAILABLE";

export interface SourceFundingHealth {
  totalDesignated: number;
  currentValue: number | null;
  status: FundingHealthStatus;
  shortfall: number | null;
  asOf: string | null;
  provenance: FactualReviewValuationProvenance | null;
  quality: FactualReviewValuationQuality | null;
}

/**
 * Shared Funding-Source Transparency (ADR-016): one Goal's own designated
 * amount toward a source it shares with at least one other row in the same
 * breakdown. Descriptive only — never a shortfall share, priority, or rank
 * (ADR-016 §2-§3). Composed from `goal_context.py`'s existing per-goal
 * allocations; introduces no new arithmetic.
 */
export interface SharedGoalDesignation {
  goalId: number;
  goalName: string;
  goalIsArchived: boolean;
  designatedAmount: number;
}

export interface SourceFundingOverviewRow {
  key: FundingSourceKey;
  sourceKind: GoalFundingSourceKind;
  sourceId: number;
  sourceName: string;
  sourceIsArchived: boolean;
  health: SourceFundingHealth;
  sharedGoals: SharedGoalDesignation[];
}

export function sourceFundingHealth(source: FactualReviewSource): SourceFundingHealth {
  return {
    totalDesignated: source.designated_total_in_context_scope,
    currentValue: source.valuation.observed_value,
    status: source.designation_coverage.status,
    shortfall: source.designation_coverage.shortfall,
    asOf: source.valuation.as_of,
    provenance: source.valuation.provenance,
    quality: source.valuation.quality,
  };
}

/** Structural coherence only; coverage and shortfall remain opaque server facts. */
export function factualReviewMatchesGoalContext(review: FactualReviewResponse): boolean {
  const context = review.goal_context;
  if (review.scope.kind !== context.scope.kind
    || review.scope.include_archived !== context.scope.include_archived
    || review.scope.goal_id !== context.scope.goal_id
    || review.sources.length !== context.designation_by_source.length) return false;

  const contextByKey = new Map(context.designation_by_source.map((source) => [
    sourceKey(source.source_kind, source.source_id),
    source,
  ]));
  if (contextByKey.size !== context.designation_by_source.length) return false;
  const seen = new Set<FundingSourceKey>();
  for (const source of review.sources) {
    const key = sourceKey(source.source_kind, source.source_id);
    const designation = contextByKey.get(key);
    if (seen.has(key) || !designation
      || source.source_name !== designation.source_name
      || source.source_is_archived !== designation.source_is_archived
      || source.currency !== designation.currency
      || source.designated_total_in_context_scope !== designation.designated_total_in_context_scope) return false;
    seen.add(key);
  }
  return true;
}

/**
 * Goal Funding-Source Drill-Through: the exact existing destination for a
 * funding source's kind. Navigation/reveal only — IDs are authoritative,
 * never the source name or list position. See /cash and /portfolio's
 * `?account=`/`?portfolio=` query handling for the destination side.
 */
export function sourceDrillThroughHref(kind: GoalFundingSourceKind, id: number): string {
  return kind === "CASH_ACCOUNT" ? `/cash?account=${id}` : `/portfolio?portfolio=${id}`;
}

export function unavailableSourceFundingHealth(): SourceFundingHealth {
  return {
    totalDesignated: 0,
    currentValue: null,
    status: "UNAVAILABLE",
    shortfall: null,
    asOf: null,
    provenance: null,
    quality: null,
  };
}

/**
 * Group each Goal's own allocations by the source they designate to.
 * Pure grouping over `goal_context.py`'s already-computed per-goal
 * `allocations`: no coverage, shortfall, or valuation arithmetic (ADR-016
 * §5). Ordering is by Goal name then id — presentation only, no priority
 * meaning (ADR-016 §3).
 */
function buildSharedGoalDesignationsBySource(
  goals: GoalContextGoal[]
): Map<FundingSourceKey, SharedGoalDesignation[]> {
  const bySource = new Map<FundingSourceKey, SharedGoalDesignation[]>();
  for (const goal of goals) {
    for (const allocation of goal.allocations) {
      const key = sourceKey(allocation.source_kind, allocation.source_id);
      const designations = bySource.get(key) ?? [];
      designations.push({
        goalId: goal.id,
        goalName: goal.name,
        goalIsArchived: goal.is_archived,
        designatedAmount: allocation.designated_amount,
      });
      bySource.set(key, designations);
    }
  }
  for (const designations of bySource.values()) {
    designations.sort((a, b) => {
      if (a.goalName !== b.goalName) return a.goalName < b.goalName ? -1 : 1;
      return a.goalId - b.goalId;
    });
  }
  return bySource;
}

export function buildSourceFundingOverview(
  sources: FactualReviewSource[],
  goals: GoalContextGoal[] = []
): SourceFundingOverviewRow[] {
  const sharedGoalsBySource = buildSharedGoalDesignationsBySource(goals);
  const rows = sources.map((source) => {
    const key = sourceKey(source.source_kind, source.source_id);
    return {
      key,
      sourceKind: source.source_kind,
      sourceId: source.source_id,
      sourceName: source.source_name || "Unknown source",
      sourceIsArchived: source.source_is_archived,
      health: sourceFundingHealth(source),
      sharedGoals: sharedGoalsBySource.get(key) ?? [],
    };
  });

  rows.sort((a, b) => {
    if (a.sourceName !== b.sourceName) return a.sourceName < b.sourceName ? -1 : 1;
    if (a.sourceKind !== b.sourceKind) return a.sourceKind < b.sourceKind ? -1 : 1;
    return a.sourceId - b.sourceId;
  });
  return rows;
}
