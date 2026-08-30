// Funding Health — pure composition over server Goal Context source
// designation facts and live source values.
//
// Three separate claims, deliberately never conflated:
//   Goal Target    — WealthGoal.target_amount (owned by Goal Context)
//   Goal Funding   — Goal Context designated_total (owned by Goal Context)
//   Source Capacity — a source's current value (CashAccount.balance, or
//                      derived live Portfolio value)
//
// Goal progress/funding gap are returned by Goal Context and never depend on
// a source's current value. This module keeps only the separate, source-centric
// Funding Health comparison. A source over-allocated across multiple goals does
// not tell the system which goal's designation to reduce, so over-allocation is
// surfaced as a fact, never resolved automatically.

import type { GoalContextSourceDesignation, GoalFundingSourceKind } from "@/lib/api";

export type FundingSourceKey = `${GoalFundingSourceKind}:${number}`;

export function sourceKey(kind: GoalFundingSourceKind, id: number): FundingSourceKey {
  return `${kind}:${id}`;
}

export type FundingHealthStatus = "SUPPORTED" | "OVER_ALLOCATED" | "UNAVAILABLE";

export interface SourceFundingHealth {
  totalDesignated: number;
  /** null whenever status is UNAVAILABLE — current value could not be honestly determined. */
  currentValue: number | null;
  status: FundingHealthStatus;
  /** totalDesignated - currentValue; set only when status is OVER_ALLOCATED. */
  shortfall: number | null;
}

/**
 * `currentValue === null`, non-finite, or negative all mean "cannot honestly
 * determine this source's current value" and collapse to UNAVAILABLE — never
 * treated as zero capacity (a real zero balance is a valid, finite input and
 * is NOT unavailable). Allocations are never mutated, clamped, or
 * redistributed here — this only reports the comparison.
 */
export function computeSourceFundingHealth(totalDesignated: number, currentValue: number | null): SourceFundingHealth {
  if (currentValue === null || !Number.isFinite(currentValue) || currentValue < 0) {
    return { totalDesignated, currentValue: null, status: "UNAVAILABLE", shortfall: null };
  }
  if (totalDesignated > currentValue) {
    return { totalDesignated, currentValue, status: "OVER_ALLOCATED", shortfall: totalDesignated - currentValue };
  }
  return { totalDesignated, currentValue, status: "SUPPORTED", shortfall: null };
}

export interface SourceFundingOverviewRow {
  key: FundingSourceKey;
  sourceKind: GoalFundingSourceKind;
  sourceId: number;
  sourceName: string;
  sourceIsArchived: boolean;
  health: SourceFundingHealth;
}

/**
 * Workspace-level, goal-independent view of every distinct funding source.
 * The server Goal Context is the authority for designation aggregation; this
 * function only combines those already-aggregated facts with live source
 * values and applies the unchanged Funding Health comparison.
 *
 * `currentValueBySource` uses `null` (or a missing key) for "unavailable" —
 * never a stand-in for zero — and flows straight into
 * computeSourceFundingHealth unchanged.
 */
export function buildSourceFundingOverview(
  designations: GoalContextSourceDesignation[],
  currentValueBySource: ReadonlyMap<FundingSourceKey, number | null>
): SourceFundingOverviewRow[] {
  const rows: SourceFundingOverviewRow[] = designations.map((designation) => {
    const sourceKind = designation.source_kind;
    const sourceId = designation.source_id;
    const key = sourceKey(sourceKind, sourceId);
    const totalDesignated = designation.designated_total_in_context_scope;
    const currentValue = currentValueBySource.get(key) ?? null;
    return {
      key,
      sourceKind,
      sourceId,
      sourceName: designation.source_name || "Unknown source",
      sourceIsArchived: designation.source_is_archived,
      health: computeSourceFundingHealth(totalDesignated, currentValue),
    };
  });

  rows.sort((a, b) => {
    if (a.sourceName !== b.sourceName) return a.sourceName < b.sourceName ? -1 : 1;
    if (a.sourceKind !== b.sourceKind) return a.sourceKind < b.sourceKind ? -1 : 1;
    return a.sourceId - b.sourceId;
  });

  return rows;
}
