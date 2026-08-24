// Milestone 2 — Cross-Portfolio Wealth Overview. Pure aggregation over data
// the home page (app/page.tsx) already fetches for the existing heatmap
// (getHoldings + getPortfolioPrices per portfolio, Portfolio.cash_balance
// from listPortfolios()) — no new network calls, no new backend endpoint.
//
// Value semantics deliberately match the existing portfolio-page definition
// (components/PortfolioSummary.tsx: `shares * (current_price ?? avg_cost)`
// summed with cash_balance) and the existing home-page heatmap's live-price
// fallback chain (`live?.current_price ?? item.current_price ?? item.avg_cost`)
// — this is not a second, subtly different definition of portfolio value.

import type { Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";

export interface PortfolioWealth {
  portfolioId: number;
  name: string;
  cash: number;
  holdingsValue: number;
  /** cash + holdingsValue. Only meaningful when `failed` is false. */
  total: number;
  /** true if at least one holding had no confirmed live/DB price and fell back to avg_cost. */
  hasEstimatedPrice: boolean;
  /** true if this portfolio's holdings failed to load — total/holdingsValue are not meaningful. */
  failed: boolean;
}

export interface WealthSummary {
  /** Sum of `total` across portfolios that loaded successfully. Excludes failed portfolios. */
  totalWealth: number;
  portfolios: PortfolioWealth[];
  anyFailed: boolean;
  anyEstimated: boolean;
}

function resolveHoldingsValue(
  items: PortfolioItem[],
  prices: PriceRefreshItem[]
): { value: number; hasEstimatedPrice: boolean } {
  const liveBySymbol = new Map(prices.map((p) => [p.symbol, p]));
  let value = 0;
  let hasEstimatedPrice = false;

  for (const item of items) {
    const live = liveBySymbol.get(item.symbol);
    // A confirmed price is one we actually fetched (live this session, or
    // previously fetched and stored on the holding row). Falling all the way
    // back to avg_cost means we have no real price signal at all — flag it
    // rather than silently presenting it as a confirmed market value.
    const confirmedPrice = live?.current_price ?? item.current_price ?? null;
    const price = confirmedPrice ?? item.avg_cost;
    if (confirmedPrice == null) hasEstimatedPrice = true;
    value += item.shares * price;
  }

  return { value, hasEstimatedPrice };
}

/**
 * Aggregates per-portfolio cash + holdings value into a wealth summary.
 * `holdingsFailedMap[portfolioId] === true` means that portfolio's holdings
 * fetch failed — its value is unknown and it is excluded from `totalWealth`
 * rather than silently treated as zero (which would understate wealth).
 */
export function computeWealthSummary(
  portfolios: Portfolio[],
  holdingsMap: Record<number, PortfolioItem[]>,
  priceMap: Record<number, PriceRefreshItem[]>,
  holdingsFailedMap: Record<number, boolean>
): WealthSummary {
  const rows: PortfolioWealth[] = portfolios.map((p) => {
    if (holdingsFailedMap[p.id]) {
      return {
        portfolioId: p.id,
        name: p.name,
        cash: p.cash_balance,
        holdingsValue: 0,
        total: 0,
        hasEstimatedPrice: false,
        failed: true,
      };
    }

    const items = holdingsMap[p.id] ?? [];
    const prices = priceMap[p.id] ?? [];
    const { value, hasEstimatedPrice } = resolveHoldingsValue(items, prices);

    return {
      portfolioId: p.id,
      name: p.name,
      cash: p.cash_balance,
      holdingsValue: value,
      total: p.cash_balance + value,
      hasEstimatedPrice,
      failed: false,
    };
  });

  const totalWealth = rows.reduce((sum, row) => sum + (row.failed ? 0 : row.total), 0);

  return {
    totalWealth,
    portfolios: rows,
    anyFailed: rows.some((row) => row.failed),
    anyEstimated: rows.some((row) => row.hasEstimatedPrice),
  };
}

/**
 * A failed portfolio's share is undefined (null), not zero — its true total
 * is unknown, so treating it as 0% would misrepresent it as "confirmed
 * negligible" rather than "unmeasured". Guards totalWealth <= 0 to avoid
 * NaN/Infinity (e.g. every portfolio empty, or all-cash-zero at inception).
 */
export function sharePct(row: PortfolioWealth, totalWealth: number): number | null {
  if (row.failed) return null;
  if (totalWealth <= 0) return 0;
  return (row.total / totalWealth) * 100;
}
