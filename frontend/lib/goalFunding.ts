// Goal Progress & Funding Health — pure composition over explicit
// GoalFundingAllocation evidence.
//
// Three separate claims, deliberately never conflated:
//   Goal Target    — WealthGoal.target_amount
//   Goal Funding   — sum of GoalFundingAllocation.allocated_amount for a goal
//   Source Capacity — a source's current value (CashAccount.balance, or
//                      derived live Portfolio value)
//
// Goal Progress/Funding Gap derive ONLY from allocation evidence and a
// target amount — they never depend on a source's current value, and a
// source losing value never reduces them. Funding Health is a separate,
// source-centric comparison against current value. A source over-allocated
// across multiple goals does not tell the system which goal's designation
// to reduce, so over-allocation is surfaced as a fact, never resolved
// automatically.

import type { GoalFundingAllocation, GoalFundingSourceKind } from "@/lib/api";

export interface GoalFundingResult {
  targetAmount: number;
  /** null only when allocation evidence failed to load — never a stand-in for zero. */
  designatedFunding: number | null;
  progressRatio: number | null;
  progressPercent: number | null;
  fundingGap: number | null;
  fullyDesignated: boolean | null;
}

/**
 * `allocations === null` means the allocation list failed to load: the
 * result is "unavailable" (all nulls), never silently zero. An empty array
 * (successfully loaded, no allocations yet) is a legitimate zero. Progress is
 * not clamped at 100% — over-designation stays visible rather than being
 * silently normalized away.
 */
export function computeGoalFunding(targetAmount: number, allocations: GoalFundingAllocation[] | null): GoalFundingResult {
  if (allocations === null || !Number.isFinite(targetAmount) || targetAmount <= 0) {
    return {
      targetAmount,
      designatedFunding: null,
      progressRatio: null,
      progressPercent: null,
      fundingGap: null,
      fullyDesignated: null,
    };
  }

  const designatedFunding = allocations.reduce((sum, allocation) => sum + allocation.allocated_amount, 0);
  const progressRatio = designatedFunding / targetAmount;

  return {
    targetAmount,
    designatedFunding,
    progressRatio,
    progressPercent: progressRatio * 100,
    fundingGap: Math.max(targetAmount - designatedFunding, 0),
    fullyDesignated: designatedFunding >= targetAmount,
  };
}

export type FundingSourceKey = `${GoalFundingSourceKind}:${number}`;

export function sourceKey(kind: GoalFundingSourceKind, id: number): FundingSourceKey {
  return `${kind}:${id}`;
}

/**
 * Total designated per source, across ALL goals that reference it — not
 * per-goal. A source may legitimately fund multiple goals; this is the basis
 * for Funding Health, which compares this total (not any single goal's
 * allocation) against the source's current value. Archived-source or
 * archived-goal allocations are included: archiving does not erase existing
 * designation evidence.
 */
export function aggregateDesignatedBySource(allocations: GoalFundingAllocation[]): Map<FundingSourceKey, number> {
  const totals = new Map<FundingSourceKey, number>();
  for (const allocation of allocations) {
    const key = allocation.cash_account_id != null
      ? sourceKey("CASH_ACCOUNT", allocation.cash_account_id)
      : sourceKey("PORTFOLIO", allocation.portfolio_id as number);
    totals.set(key, (totals.get(key) ?? 0) + allocation.allocated_amount);
  }
  return totals;
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
