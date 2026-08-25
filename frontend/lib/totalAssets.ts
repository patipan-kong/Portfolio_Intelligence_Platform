import type { CashAccount } from "./api";

export type AssetLoadStatus = "loading" | "success" | "error";

export interface TotalAssetsInput {
  /** Existing combined portfolio value, including brokerage cash. */
  investmentAssets: number | null;
  /** False when the investment side is loading or any required portfolio data failed. */
  investmentComplete: boolean;
  /** CashAccount API lifecycle, kept separate from investment loading/failure. */
  cashStatus: AssetLoadStatus;
  cashAccounts: CashAccount[];
}

export interface TotalAssetsSummary {
  investmentAssets: number | null;
  externalCash: number | null;
  totalAssets: number | null;
  investmentComplete: boolean;
  cashComplete: boolean;
  /** Active rows that violate the THB-only/non-negative balance contract. */
  invalidCashAccountCount: number;
  /** Defensive count only; archived rows never contribute to externalCash. */
  archivedCashAccountCount: number;
}

/**
 * Combines the already-computed investment value with standalone active cash.
 *
 * This helper intentionally accepts one investment value rather than Portfolio
 * cash fields: Portfolio.cash_balance is brokerage cash already inside that
 * value and must never be added a second time here.
 */
export function computeTotalAssets(input: TotalAssetsInput): TotalAssetsSummary {
  const investmentAssets =
    input.investmentComplete && input.investmentAssets != null && Number.isFinite(input.investmentAssets)
      ? input.investmentAssets
      : null;

  const archivedCashAccountCount = input.cashAccounts.filter((account) => account.is_archived).length;
  const activeAccounts = input.cashAccounts.filter((account) => !account.is_archived);
  const invalidCashAccountCount = activeAccounts.filter(
    (account) => account.currency !== "THB" || !Number.isFinite(account.balance) || account.balance < 0,
  ).length;
  const cashComplete = input.cashStatus === "success" && invalidCashAccountCount === 0;
  const externalCash = cashComplete
    ? activeAccounts.reduce((sum, account) => sum + account.balance, 0)
    : null;

  return {
    investmentAssets,
    externalCash,
    totalAssets: investmentAssets != null && externalCash != null ? investmentAssets + externalCash : null,
    investmentComplete: investmentAssets != null,
    cashComplete,
    invalidCashAccountCount,
    archivedCashAccountCount,
  };
}
