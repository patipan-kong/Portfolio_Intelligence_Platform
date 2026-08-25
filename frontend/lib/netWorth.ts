import type { TotalAssetsSummary } from "./totalAssets";
import type { TotalLiabilitiesSummary } from "./totalLiabilities";

export interface NetWorthSummary {
  netWorth: number | null;
  netWorthComplete: boolean;
}

/**
 * Composes the already-validated current balance-sheet aggregates.
 *
 * This helper deliberately does not inspect or re-sum portfolios, CashAccounts,
 * or Liability rows. A null source aggregate means that side is unavailable,
 * so Net Worth remains unavailable rather than treating an unknown value as
 * zero.
 */
export function computeNetWorth(
  totalAssetsResult: Pick<TotalAssetsSummary, "totalAssets">,
  totalLiabilitiesResult: Pick<TotalLiabilitiesSummary, "totalLiabilities">,
): NetWorthSummary {
  const assets = totalAssetsResult.totalAssets;
  const liabilities = totalLiabilitiesResult.totalLiabilities;

  if (assets == null || liabilities == null || !Number.isFinite(assets) || !Number.isFinite(liabilities)) {
    return { netWorth: null, netWorthComplete: false };
  }

  const netWorth = assets - liabilities;
  return {
    netWorth: Number.isFinite(netWorth) ? netWorth : null,
    netWorthComplete: Number.isFinite(netWorth),
  };
}
