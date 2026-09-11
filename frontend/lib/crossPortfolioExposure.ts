// Cross-Portfolio Exposure Snapshot — Slice 1. Pure aggregation over data the
// home page already fetches for the existing heatmap/wealth overview
// (getHoldings + getPortfolioPrices per portfolio, Portfolio.cash_balance
// from listPortfolios()) — no new network calls, no new backend endpoint.
//
// Current-snapshot and descriptive only: no historical trend, no
// benchmark-relative attribution, no severity/risk labels, no target
// allocation, no rebalance guidance. See docs/architecture/ROADMAP.md
// Analytics backlog and the Cross-Portfolio Exposure reconnaissance report
// for why Sector BHB attribution is explicitly out of scope here.
//
// Value semantics reuse lib/wealthOverview.ts's resolveHoldingValuations —
// the one Wealth OS definition of a holding's current value
// (live?.current_price ?? item.current_price ?? avg_cost) — so this module
// is not a second, subtly different valuation definition.
//
// Symbol identity: exact `item.symbol` string equality, matching the
// existing home-page heatmap's aggregation key. No case/whitespace/exchange
// alias normalization is invented here.
//
// Sector identity: `item.sector` trimmed, treating null/blank as "Other",
// matching lib/sectors.ts's sectorColor() null-handling convention. Cash is
// never assigned a sector — it is reported separately (see `cash` below).

import type { Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";
import { resolveHoldingValuations } from "./wealthOverview.ts";

export interface PortfolioContribution {
  portfolioId: number;
  name: string;
  cash: number;
  holdingsValue: number;
  /** cash + holdingsValue. Only meaningful when `failed` is false. */
  total: number;
  /** % of total current portfolio value (cash + holdings, across portfolios
   * that loaded successfully). Null when `failed` is true — a failed
   * portfolio's true share is unknown, not zero. */
  sharePctOfTotalValue: number | null;
  failed: boolean;
}

export interface PortfolioSectorShare {
  portfolioId: number;
  name: string;
  value: number;
  /** % of this sector's own aggregate value (not of the whole workspace). */
  sharePctOfSector: number;
}

export interface SectorExposure {
  /** "Other" for null/blank sector values — never invented beyond that. */
  sector: string;
  value: number;
  /** % of total invested holdings value (cash excluded — see `cash` on the
   * snapshot for where cash sits). */
  sharePctOfHoldings: number;
  portfolios: PortfolioSectorShare[];
}

export interface PortfolioSymbolShare {
  portfolioId: number;
  name: string;
  value: number;
  /** % of this symbol's own aggregate value across portfolios. */
  sharePctOfSymbol: number;
}

export interface SymbolOverlap {
  symbol: string;
  totalValue: number;
  /** % of total invested holdings value. */
  sharePctOfHoldings: number;
  portfolioCount: number;
  portfolios: PortfolioSymbolShare[];
}

export interface ExposureSnapshot {
  portfolios: PortfolioContribution[];
  /** cash + holdings, summed across portfolios that loaded successfully. */
  totalValue: number;
  /** Sum of holdingsValue across portfolios that loaded successfully —
   * the denominator for every sector/symbol percentage below. */
  totalInvestedHoldings: number;
  /** Sum of cash across portfolios that loaded successfully. Not
   * sector-classified; disclosed here so cash's effect on the sector
   * denominator (holdings-only, excludes cash) is explicit rather than
   * silently dropped. */
  totalCash: number;
  sectors: SectorExposure[];
  /** Symbols held in more than one successfully-loaded portfolio, richest first. */
  overlaps: SymbolOverlap[];
  includedPortfolioCount: number;
  failedPortfolioNames: string[];
  anyEstimatedPrice: boolean;
  anyStalePrice: boolean;
}

function sectorKey(sector: string | null): string {
  const trimmed = sector?.trim();
  return trimmed ? trimmed : "Other";
}

/**
 * Builds the Cross-Portfolio Exposure Snapshot from already-fetched,
 * already-canonical per-portfolio data. Mirrors computeWealthSummary's
 * failed-portfolio handling: a portfolio whose holdings fetch failed is
 * excluded from every aggregate (its true contribution is unknown, not
 * zero) rather than silently treated as empty.
 */
export function computeExposureSnapshot(
  portfolios: Portfolio[],
  holdingsMap: Record<number, PortfolioItem[]>,
  priceMap: Record<number, PriceRefreshItem[]>,
  holdingsFailedMap: Record<number, boolean>
): ExposureSnapshot {
  const contributions: PortfolioContribution[] = portfolios.map((p) => {
    const failed = holdingsFailedMap[p.id] === true;
    if (failed) {
      return {
        portfolioId: p.id,
        name: p.name,
        cash: p.cash_balance,
        holdingsValue: 0,
        total: 0,
        sharePctOfTotalValue: null,
        failed: true,
      };
    }
    const valuations = resolveHoldingValuations(holdingsMap[p.id] ?? [], priceMap[p.id] ?? []);
    const holdingsValue = valuations.reduce((sum, v) => sum + v.value, 0);
    return {
      portfolioId: p.id,
      name: p.name,
      cash: p.cash_balance,
      holdingsValue,
      total: p.cash_balance + holdingsValue,
      sharePctOfTotalValue: null, // filled in below once totalValue is known
      failed: false,
    };
  });

  const totalValue = contributions.reduce((sum, c) => sum + (c.failed ? 0 : c.total), 0);
  const totalCash = contributions.reduce((sum, c) => sum + (c.failed ? 0 : c.cash), 0);
  const totalInvestedHoldings = contributions.reduce((sum, c) => sum + (c.failed ? 0 : c.holdingsValue), 0);

  const portfoliosOut = contributions.map((c) => ({
    ...c,
    sharePctOfTotalValue: c.failed ? null : totalValue > 0 ? (c.total / totalValue) * 100 : 0,
  }));

  const included = portfolios.filter((p) => !holdingsFailedMap[p.id]);

  // symbol -> portfolioId -> value
  const symbolMap = new Map<string, Map<number, number>>();
  // sector -> portfolioId -> value
  const sectorMap = new Map<string, Map<number, number>>();
  let anyEstimatedPrice = false;
  let anyStalePrice = false;

  for (const p of included) {
    const valuations = resolveHoldingValuations(holdingsMap[p.id] ?? [], priceMap[p.id] ?? []);
    for (const v of valuations) {
      if (v.isEstimated) anyEstimatedPrice = true;
      if (v.isStale) anyStalePrice = true;

      const bySymbolPortfolio = symbolMap.get(v.symbol) ?? new Map<number, number>();
      bySymbolPortfolio.set(p.id, (bySymbolPortfolio.get(p.id) ?? 0) + v.value);
      symbolMap.set(v.symbol, bySymbolPortfolio);

      const sec = sectorKey(v.sector);
      const bySectorPortfolio = sectorMap.get(sec) ?? new Map<number, number>();
      bySectorPortfolio.set(p.id, (bySectorPortfolio.get(p.id) ?? 0) + v.value);
      sectorMap.set(sec, bySectorPortfolio);
    }
  }

  const nameById = new Map(included.map((p) => [p.id, p.name]));

  const sectors: SectorExposure[] = Array.from(sectorMap.entries())
    .map(([sector, byPortfolio]) => {
      const value = Array.from(byPortfolio.values()).reduce((s, v) => s + v, 0);
      const portfolioShares: PortfolioSectorShare[] = Array.from(byPortfolio.entries())
        .map(([portfolioId, v]) => ({
          portfolioId,
          name: nameById.get(portfolioId) ?? "",
          value: v,
          sharePctOfSector: value > 0 ? (v / value) * 100 : 0,
        }))
        .sort((a, b) => b.value - a.value || a.portfolioId - b.portfolioId);
      return {
        sector,
        value,
        sharePctOfHoldings: totalInvestedHoldings > 0 ? (value / totalInvestedHoldings) * 100 : 0,
        portfolios: portfolioShares,
      };
    })
    .sort((a, b) => b.value - a.value || a.sector.localeCompare(b.sector));

  const overlaps: SymbolOverlap[] = Array.from(symbolMap.entries())
    .filter(([, byPortfolio]) => byPortfolio.size > 1)
    .map(([symbol, byPortfolio]) => {
      const totalSymbolValue = Array.from(byPortfolio.values()).reduce((s, v) => s + v, 0);
      const portfolioShares: PortfolioSymbolShare[] = Array.from(byPortfolio.entries())
        .map(([portfolioId, v]) => ({
          portfolioId,
          name: nameById.get(portfolioId) ?? "",
          value: v,
          sharePctOfSymbol: totalSymbolValue > 0 ? (v / totalSymbolValue) * 100 : 0,
        }))
        .sort((a, b) => b.value - a.value || a.portfolioId - b.portfolioId);
      return {
        symbol,
        totalValue: totalSymbolValue,
        sharePctOfHoldings: totalInvestedHoldings > 0 ? (totalSymbolValue / totalInvestedHoldings) * 100 : 0,
        portfolioCount: byPortfolio.size,
        portfolios: portfolioShares,
      };
    })
    .sort((a, b) => b.totalValue - a.totalValue || a.symbol.localeCompare(b.symbol));

  return {
    portfolios: portfoliosOut,
    totalValue,
    totalInvestedHoldings,
    totalCash,
    sectors,
    overlaps,
    includedPortfolioCount: included.length,
    failedPortfolioNames: contributions.filter((c) => c.failed).map((c) => c.name),
    anyEstimatedPrice,
    anyStalePrice,
  };
}
