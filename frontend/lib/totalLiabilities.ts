import type { Liability } from "./api";

export type LiabilityLoadStatus = "loading" | "success" | "error";

export interface TotalLiabilitiesInput {
  /** Current observed liability rows returned by the active-only API phase. */
  liabilities: Liability[];
  /** Liability API lifecycle, kept independent from the asset-side phases. */
  liabilityStatus: LiabilityLoadStatus;
}

export interface TotalLiabilitiesSummary {
  totalLiabilities: number | null;
  liabilityComplete: boolean;
  /** Active rows that violate the THB-only/non-negative finite balance contract. */
  invalidLiabilityCount: number;
  /** Defensive count only; archived rows never contribute to the total. */
  archivedLiabilityCount: number;
}

/**
 * Sums current observed outstanding THB balances without inventing debt data.
 *
 * A successful empty response is a known zero. An API failure, an in-flight
 * request, or malformed active data is unavailable rather than silently
 * normalized into a legitimate total.
 */
export function computeTotalLiabilities(input: TotalLiabilitiesInput): TotalLiabilitiesSummary {
  const archivedLiabilityCount = input.liabilities.filter((liability) => liability.is_archived).length;
  const activeLiabilities = input.liabilities.filter((liability) => !liability.is_archived);
  const invalidLiabilityCount = activeLiabilities.filter(
    (liability) =>
      liability.currency !== "THB" ||
      !Number.isFinite(liability.balance) ||
      liability.balance < 0,
  ).length;

  const liabilityComplete = input.liabilityStatus === "success" && invalidLiabilityCount === 0;
  let totalLiabilities: number | null = null;
  if (liabilityComplete) {
    const total = activeLiabilities.reduce((sum, liability) => sum + liability.balance, 0);
    // Individual balances are finite, but a defensive aggregate check avoids
    // presenting Infinity if an extreme fixture/API payload overflows the sum.
    if (Number.isFinite(total) && total >= 0) totalLiabilities = total;
  }

  return {
    totalLiabilities,
    liabilityComplete: totalLiabilities != null,
    invalidLiabilityCount,
    archivedLiabilityCount,
  };
}
