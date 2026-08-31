// Funding Health presentation adapters over the server-owned factual review.
// This module deliberately performs no designation, valuation, coverage, or
// shortfall arithmetic.

import type {
  FactualReviewSource,
  FactualReviewResponse,
  FactualReviewValuationProvenance,
  FactualReviewValuationQuality,
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

export interface SourceFundingOverviewRow {
  key: FundingSourceKey;
  sourceKind: GoalFundingSourceKind;
  sourceId: number;
  sourceName: string;
  sourceIsArchived: boolean;
  health: SourceFundingHealth;
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

export function buildSourceFundingOverview(sources: FactualReviewSource[]): SourceFundingOverviewRow[] {
  const rows = sources.map((source) => ({
    key: sourceKey(source.source_kind, source.source_id),
    sourceKind: source.source_kind,
    sourceId: source.source_id,
    sourceName: source.source_name || "Unknown source",
    sourceIsArchived: source.source_is_archived,
    health: sourceFundingHealth(source),
  }));

  rows.sort((a, b) => {
    if (a.sourceName !== b.sourceName) return a.sourceName < b.sourceName ? -1 : 1;
    if (a.sourceKind !== b.sourceKind) return a.sourceKind < b.sourceKind ? -1 : 1;
    return a.sourceId - b.sourceId;
  });
  return rows;
}
