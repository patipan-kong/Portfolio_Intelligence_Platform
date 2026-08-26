"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { usePortfolio } from "@/lib/PortfolioContext";
import {
  getHoldings,
  getPortfolioPrices,
  getTransactionHistory,
  getSnapshots,
  listCashAccounts,
  listLiabilities,
  getCashAccountBalanceAsOf,
  getLiabilityBalanceAsOf,
} from "@/lib/api";
import type {
  CashAccount,
  CashAccountBalanceAsOf,
  Liability,
  LiabilityBalanceAsOf,
  Portfolio,
  PortfolioItem,
  PriceRefreshItem,
  TransactionRecord,
  PortfolioSnapshotRow,
} from "@/lib/api";
import type { AssetLoadStatus } from "@/lib/totalAssets";
import type { LiabilityLoadStatus } from "@/lib/totalLiabilities";
import { computeWealthHistory } from "@/lib/wealthHistory";
import { computeTotalAssetsHistory } from "@/lib/totalAssetsHistory";
import { computeTotalLiabilitiesHistory } from "@/lib/totalLiabilitiesHistory";
import { computeNetWorthHistory } from "@/lib/netWorthHistory";
import WealthOverview from "@/components/WealthOverview";
import CrossPortfolioIncome from "@/components/CrossPortfolioIncome";
import CrossPortfolioWealthHistory from "@/components/CrossPortfolioWealthHistory";
import TotalAssetsHistoryCard from "@/components/TotalAssetsHistoryCard";
import TotalLiabilitiesHistoryCard from "@/components/TotalLiabilitiesHistoryCard";
import NetWorthHistoryCard from "@/components/NetWorthHistoryCard";

// Matches the per-portfolio Income page's cap (backend's hard limit is 500)
// so cross-portfolio dividend aggregation isn't silently truncated either.
const MAX_TRANSACTIONS = 500;
// Matches the Performance page's own getSnapshots() default — a full year of
// daily history per portfolio, the backend's own cap (min(limit, 365)).
const MAX_SNAPSHOTS = 365;

function heatTileColor(cp: number | null, pricesLoaded: boolean): string {
  if (!pricesLoaded) return "#374151"; // dark gray — still loading
  if (cp == null) return "#1F2937";   // near-black — confirmed no data
  if (Math.abs(cp) < 0.3) return "#4B5563"; // neutral
  const intensity = Math.min(Math.abs(cp) / 5, 1);
  if (cp > 0) {
    return `hsl(142, ${Math.round(50 + intensity * 30)}%, ${Math.round(38 - intensity * 10)}%)`;
  }
  return `hsl(0, ${Math.round(60 + intensity * 20)}%, ${Math.round(50 - intensity * 12)}%)`;
}

function DashboardHeatmap({
  holdingsMap,
  priceMap,
  pricesLoaded,
  portfolios,
}: {
  holdingsMap: Record<number, PortfolioItem[]>;
  priceMap: Record<number, PriceRefreshItem[]>;
  pricesLoaded: boolean;
  portfolios: Portfolio[];
}) {
  const aggregated = new Map<string, {
    symbol: string;
    mv: number;
    cp: number | null;
    livePrice: number | null;
    priceConfirmed: boolean;
    isStale: boolean;
  }>();

  portfolios.forEach((p) => {
    const liveBySymbol = new Map((priceMap[p.id] ?? []).map((pr) => [pr.symbol, pr]));

    (holdingsMap[p.id] ?? []).forEach((item) => {
      const live = liveBySymbol.get(item.symbol);
      const price = live?.current_price ?? item.current_price ?? item.avg_cost;
      const mv = item.shares * price;
      const cp = live?.change_percent ?? null;
      // live?.current_price may itself be null (quarantined/no-data quote),
      // so a truthy `live` lookup alone doesn't mean we have a confirmed price.
      const livePrice = live?.current_price ?? null;
      const priceConfirmed = pricesLoaded && livePrice != null;
      // is_stale is only ever true alongside a real current_price, so this
      // never fires for the "no data" case above.
      const isStale = live?.is_stale === true;

      const existing = aggregated.get(item.symbol);
      if (existing) {
        existing.mv += mv;
        if (cp != null) existing.cp = cp;
        if (livePrice != null) existing.livePrice = livePrice;
        if (priceConfirmed) existing.priceConfirmed = true;
        if (isStale) existing.isStale = true;
      } else {
        aggregated.set(item.symbol, { symbol: item.symbol, mv, cp, livePrice, priceConfirmed, isStale });
      }
    });
  });

  const tiles = Array.from(aggregated.values()).sort((a, b) => b.mv - a.mv);
  if (tiles.length === 0) return null;

  const totalValue = tiles.reduce((s, t) => s + t.mv, 0);

  return (
    <section>
      <div className="flex items-center gap-3 mb-2">
        <h2 className="text-base font-semibold text-gray-500 uppercase tracking-wide">Portfolio Heatmap</h2>
        {!pricesLoaded && (
          <span className="text-xs text-gray-400 flex items-center gap-1">
            <span className="inline-block w-2.5 h-2.5 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
            Loading prices…
          </span>
        )}
      </div>
      <div className="flex flex-wrap gap-1">
        {tiles.map((tile) => {
          const weightPct = totalValue > 0 ? (tile.mv / totalValue) * 100 : 100 / tiles.length;
          const display = tile.symbol.replace(".BK", "");

          let changeText: string;
          let changeColor: string;
          if (!pricesLoaded) {
            changeText = "…";
            changeColor = "text-gray-400";
          } else if (!tile.priceConfirmed) {
            // no confirmed current price at all (fetch failed/quarantined) — the only true "no data" case
            changeText = "No price data";
            changeColor = "text-gray-500";
          } else if (tile.cp == null) {
            // current price is confirmed but daily change is unavailable (e.g. no previous close) —
            // fall back to the price itself rather than mislabeling this as "no price data"
            changeText = tile.livePrice != null ? `฿${tile.livePrice.toFixed(2)}` : "No change data";
            changeColor = "text-gray-300";
          } else {
            changeText = `${tile.cp > 0 ? "+" : ""}${tile.cp.toFixed(2)}%`;
            changeColor = tile.cp > 0.3 ? "text-green-200" : tile.cp < -0.3 ? "text-red-200" : "text-gray-300";
          }

          return (
            <Link
              key={tile.symbol}
              href={`/stock/${encodeURIComponent(tile.symbol)}`}
              title={tile.isStale ? "Live price unavailable; showing the last cached price." : undefined}
              style={{
                flexBasis: `${Math.max(6, weightPct - 0.5)}%`,
                flexGrow: 0,
                flexShrink: 1,
                background: heatTileColor(tile.cp, pricesLoaded || tile.priceConfirmed),
                minWidth: 72,
                minHeight: 72,
                position: "relative",
              }}
              className="rounded-lg p-2 flex flex-col justify-between hover:brightness-110 transition-all cursor-pointer"
            >
              {tile.isStale && (
                <span
                  className="absolute top-1 right-1 text-amber-300 text-[10px] leading-none"
                  aria-label="Stale price"
                >
                  ⏱
                </span>
              )}
              <span className="text-white text-xs font-bold truncate leading-tight">{display}</span>
              <div>
                <div className={`text-xs font-semibold leading-tight ${changeColor}`}>{changeText}</div>
                <div className="text-xs text-white/50">{weightPct.toFixed(1)}%</div>
              </div>
            </Link>
          );
        })}
      </div>
    </section>
  );
}

export default function DashboardPage() {
  const { portfolios, loading: ctxLoading, error: portfolioError } = usePortfolio();
  const [holdingsMap, setHoldingsMap] = useState<Record<number, PortfolioItem[]>>({});
  const [holdingsFailedMap, setHoldingsFailedMap] = useState<Record<number, boolean>>({});
  const [priceMap, setPriceMap] = useState<Record<number, PriceRefreshItem[]>>({});
  const [loadingHoldings, setLoadingHoldings] = useState(false);
  // True once Phase 1 has settled (every portfolio either loaded or failed) —
  // distinct from holdingsMap containing every id, since a failed portfolio
  // never gets a holdingsMap entry. Gates Phase 2 so it doesn't fire against
  // a stale/incomplete holdingsMap from a previous portfolio list.
  const [holdingsSettled, setHoldingsSettled] = useState(false);
  const [pricesLoaded, setPricesLoaded] = useState(false);
  const [error, setError] = useState("");
  const holdingsRequestIdRef = useRef(0);
  const priceRequestIdRef = useRef(0);

  // External cash is an independent dashboard phase. It intentionally does
  // not enter PortfolioContext or any investment loading/error state.
  const [cashAccounts, setCashAccounts] = useState<CashAccount[]>([]);
  const [cashStatus, setCashStatus] = useState<AssetLoadStatus>("loading");
  const cashRequestIdRef = useRef(0);

  // Liability data is an independent current-balance phase. It intentionally
  // does not enter PortfolioContext or any investment/asset loading state.
  const [liabilities, setLiabilities] = useState<Liability[]>([]);
  const [liabilityStatus, setLiabilityStatus] = useState<LiabilityLoadStatus>("loading");
  const liabilityRequestIdRef = useRef(0);

  // Dividend income aggregation — independent of holdings/prices, so it runs
  // as its own phase rather than gating on (or being gated by) Phase 1/2.
  const [transactionsMap, setTransactionsMap] = useState<Record<number, TransactionRecord[]>>({});
  const [transactionsFailedMap, setTransactionsFailedMap] = useState<Record<number, boolean>>({});
  const [loadingTransactions, setLoadingTransactions] = useState(false);
  const transactionsRequestIdRef = useRef(0);

  // Wealth history aggregation — same independence rationale as the dividend
  // income phase: reads DB snapshot history only, no yfinance, own phase.
  const [snapshotsMap, setSnapshotsMap] = useState<Record<number, PortfolioSnapshotRow[]>>({});
  const [snapshotsFailedMap, setSnapshotsFailedMap] = useState<Record<number, boolean>>({});
  const [loadingSnapshots, setLoadingSnapshots] = useState(false);
  const snapshotsRequestIdRef = useRef(0);

  // Cash phase — active accounts only. The request id and effect cleanup keep
  // a response from an abandoned portfolio/context state from overwriting the
  // current dashboard's cash state.
  useEffect(() => {
    const requestId = ++cashRequestIdRef.current;
    let active = true;
    setCashStatus("loading");
    setCashAccounts([]);

    listCashAccounts(false)
      .then((accounts) => {
        if (!active || cashRequestIdRef.current !== requestId) return;
        setCashAccounts(accounts);
        setCashStatus("success");
      })
      .catch((reason) => {
        if (!active || cashRequestIdRef.current !== requestId) return;
        console.error("Failed to load cash accounts:", reason);
        setCashAccounts([]);
        setCashStatus("error");
      });

    return () => { active = false; };
  }, [portfolios, ctxLoading, portfolioError]);

  // Liability phase — active workspace liabilities only. The request id and
  // effect cleanup mirror the CashAccount phase so a late response from an
  // abandoned dashboard context cannot overwrite current debt state.
  useEffect(() => {
    const requestId = ++liabilityRequestIdRef.current;
    let active = true;
    setLiabilityStatus("loading");
    setLiabilities([]);

    listLiabilities(false)
      .then((items) => {
        if (!active || liabilityRequestIdRef.current !== requestId) return;
        setLiabilities(items);
        setLiabilityStatus("success");
      })
      .catch((reason) => {
        if (!active || liabilityRequestIdRef.current !== requestId) return;
        console.error("Failed to load liabilities:", reason);
        setLiabilities([]);
        setLiabilityStatus("error");
      });

    return () => { active = false; };
  }, [portfolios, ctxLoading, portfolioError]);

  // Phase 1: load holdings from DB (fast, no yfinance)
  useEffect(() => {
    const requestId = ++holdingsRequestIdRef.current;
    // Any holdings reload invalidates an in-flight price response as well.
    // The quote set belongs to the holdings request that triggered it.
    ++priceRequestIdRef.current;
    let active = true;

    if (ctxLoading || portfolios.length === 0) {
      setHoldingsMap({});
      setHoldingsFailedMap({});
      setPriceMap({});
      setPricesLoaded(false);
      setLoadingHoldings(false);
      setHoldingsSettled(!ctxLoading);
      return () => { active = false; };
    }

    setLoadingHoldings(true);
    setHoldingsSettled(false);
    setPricesLoaded(false);
    setPriceMap({});
    setError("");
    // Promise.allSettled — one portfolio's holdings request failing must not
    // wipe out the others. The dashboard/wealth overview should still show
    // every portfolio it *could* load; the failed one is flagged, not hidden.
    Promise.allSettled(
      portfolios.map((p) => getHoldings(p.id).then((items) => ({ id: p.id, items })))
    )
      .then((results) => {
        if (!active || holdingsRequestIdRef.current !== requestId) return;
        const map: Record<number, PortfolioItem[]> = {};
        const failed: Record<number, boolean> = {};
        results.forEach((result, i) => {
          const pid = portfolios[i].id;
          if (result.status === "fulfilled") {
            map[result.value.id] = result.value.items;
          } else {
            failed[pid] = true;
            console.error(`Failed to load holdings for portfolio ${pid}:`, result.reason);
          }
        });
        setHoldingsMap(map);
        setHoldingsFailedMap(failed);
        setError(Object.keys(failed).length === portfolios.length ? "Cannot connect to backend" : "");
      })
      .finally(() => {
        if (active && holdingsRequestIdRef.current === requestId) {
          setLoadingHoldings(false);
          setHoldingsSettled(true);
        }
      });

    return () => { active = false; };
  }, [portfolios, ctxLoading]);

  // Phase 2: fetch live prices once holdings are known (hits yfinance cache)
  useEffect(() => {
    const requestId = ++priceRequestIdRef.current;
    const holdingsRequestId = holdingsRequestIdRef.current;
    let active = true;

    if (!holdingsSettled || portfolios.length === 0) {
      return () => { active = false; };
    }

    setPriceMap({});
    setPricesLoaded(false);
    Promise.allSettled(
      portfolios.map((p) => getPortfolioPrices(p.id).then((prices) => ({ id: p.id, prices })))
    ).then((results) => {
      if (
        !active ||
        priceRequestIdRef.current !== requestId ||
        holdingsRequestIdRef.current !== holdingsRequestId
      ) return;
      const map: Record<number, PriceRefreshItem[]> = {};
      results.forEach((result, i) => {
        if (result.status === "fulfilled") {
          map[result.value.id] = result.value.prices;
        } else {
          // one portfolio's price fetch failing must not discard the others —
          // heatmap shows "No price data" for just this portfolio's holdings
          console.error(`Failed to load prices for portfolio ${portfolios[i].id}:`, result.reason);
        }
      });
      setPriceMap(map);
      setPricesLoaded(true);
    });

    return () => { active = false; };
  }, [holdingsSettled, holdingsMap, portfolios]);

  // Dividend income phase — reads DB transaction history only, no yfinance,
  // so it can run independently of the holdings/price phases above.
  useEffect(() => {
    const requestId = ++transactionsRequestIdRef.current;
    let active = true;

    if (ctxLoading || portfolios.length === 0) {
      setTransactionsMap({});
      setTransactionsFailedMap({});
      setLoadingTransactions(false);
      return () => { active = false; };
    }

    setLoadingTransactions(true);
    Promise.allSettled(
      portfolios.map((p) =>
        getTransactionHistory(p.id, undefined, MAX_TRANSACTIONS).then((items) => ({ id: p.id, items }))
      )
    )
      .then((results) => {
        if (!active || transactionsRequestIdRef.current !== requestId) return;
        const map: Record<number, TransactionRecord[]> = {};
        const failed: Record<number, boolean> = {};
        results.forEach((result, i) => {
          const pid = portfolios[i].id;
          if (result.status === "fulfilled") {
            map[result.value.id] = result.value.items;
          } else {
            failed[pid] = true;
            console.error(`Failed to load transactions for portfolio ${pid}:`, result.reason);
          }
        });
        setTransactionsMap(map);
        setTransactionsFailedMap(failed);
      })
      .finally(() => {
        if (active && transactionsRequestIdRef.current === requestId) setLoadingTransactions(false);
      });

    return () => { active = false; };
  }, [portfolios, ctxLoading]);

  // Wealth history phase — reads DB snapshot history only, no yfinance, so it
  // can run independently of the holdings/price/transactions phases above.
  useEffect(() => {
    const requestId = ++snapshotsRequestIdRef.current;
    let active = true;

    if (ctxLoading || portfolios.length === 0) {
      setSnapshotsMap({});
      setSnapshotsFailedMap({});
      setLoadingSnapshots(false);
      return () => { active = false; };
    }

    setLoadingSnapshots(true);
    Promise.allSettled(
      portfolios.map((p) =>
        getSnapshots(p.id, MAX_SNAPSHOTS).then((items) => ({ id: p.id, items }))
      )
    )
      .then((results) => {
        if (!active || snapshotsRequestIdRef.current !== requestId) return;
        const map: Record<number, PortfolioSnapshotRow[]> = {};
        const failed: Record<number, boolean> = {};
        results.forEach((result, i) => {
          const pid = portfolios[i].id;
          if (result.status === "fulfilled") {
            map[result.value.id] = result.value.items;
          } else {
            failed[pid] = true;
            console.error(`Failed to load snapshots for portfolio ${pid}:`, result.reason);
          }
        });
        setSnapshotsMap(map);
        setSnapshotsFailedMap(failed);
      })
      .finally(() => {
        if (active && snapshotsRequestIdRef.current === requestId) setLoadingSnapshots(false);
      });

    return () => { active = false; };
  }, [portfolios, ctxLoading]);

  // Total Assets History (Phase 5, Milestone 1) — composes the Investment
  // Wealth History date spine above with the existing Cash As-Of contract.
  // Two dependent phases: (a) ALL CashAccounts, active + archived, since
  // archived accounts' historical evidence remains valid; (b) a bounded
  // Cash As-Of fan-out over (account × investment-history-date) pairs only
  // — never a daily calendar series, never every possible date.
  const [cashAccountsAll, setCashAccountsAll] = useState<CashAccount[]>([]);
  const [cashAccountsAllStatus, setCashAccountsAllStatus] = useState<AssetLoadStatus>("loading");
  const cashAccountsAllRequestIdRef = useRef(0);

  useEffect(() => {
    const requestId = ++cashAccountsAllRequestIdRef.current;
    let active = true;
    setCashAccountsAllStatus("loading");
    setCashAccountsAll([]);

    listCashAccounts(true)
      .then((accounts) => {
        if (!active || cashAccountsAllRequestIdRef.current !== requestId) return;
        setCashAccountsAll(accounts);
        setCashAccountsAllStatus("success");
      })
      .catch((reason) => {
        if (!active || cashAccountsAllRequestIdRef.current !== requestId) return;
        console.error("Failed to load Cash Accounts (including archived) for Total Assets History:", reason);
        setCashAccountsAll([]);
        setCashAccountsAllStatus("error");
      });

    return () => { active = false; };
  }, [portfolios, ctxLoading, portfolioError]);

  // The canonical historical spine: reuses the same computeWealthHistory
  // aggregation CrossPortfolioWealthHistory itself calls, over the same
  // already-fetched snapshotsMap — no new snapshot fetch, no competing
  // investment calculation.
  const investmentHistoryPoints = useMemo(
    () => computeWealthHistory(portfolios, snapshotsMap, snapshotsFailedMap).points,
    [portfolios, snapshotsMap, snapshotsFailedMap]
  );
  const investmentHistoryDates = useMemo(
    () => investmentHistoryPoints.map((p) => p.date),
    [investmentHistoryPoints]
  );

  const [cashAsOfMap, setCashAsOfMap] = useState<Record<number, Record<string, CashAccountBalanceAsOf>>>({});
  const [cashAsOfLoading, setCashAsOfLoading] = useState(false);
  const cashAsOfRequestIdRef = useRef(0);

  useEffect(() => {
    const requestId = ++cashAsOfRequestIdRef.current;
    let active = true;

    // Wait for both dependent phases to settle before fanning out — firing
    // against a stale/incomplete snapshotsMap or account list would just be
    // discarded work and risks racing the settled state below.
    if (ctxLoading || loadingSnapshots || cashAccountsAllStatus === "loading") {
      return () => { active = false; };
    }

    if (cashAccountsAllStatus === "error" || cashAccountsAll.length === 0 || investmentHistoryDates.length === 0) {
      setCashAsOfMap({});
      setCashAsOfLoading(false);
      return () => { active = false; };
    }

    setCashAsOfLoading(true);
    const pairs = cashAccountsAll.flatMap((account) =>
      investmentHistoryDates.map((date) => ({ accountId: account.id, date }))
    );

    Promise.allSettled(
      pairs.map(({ accountId, date }) =>
        getCashAccountBalanceAsOf(accountId, date).then((result) => ({ accountId, date, result }))
      )
    )
      .then((results) => {
        if (!active || cashAsOfRequestIdRef.current !== requestId) return;
        const map: Record<number, Record<string, CashAccountBalanceAsOf>> = {};
        results.forEach((result, i) => {
          if (result.status === "fulfilled") {
            const { accountId, date, result: asOf } = result.value;
            if (!map[accountId]) map[accountId] = {};
            map[accountId][date] = asOf;
          } else {
            // One failed pair must not fabricate a zero and must not discard
            // every other pair's evidence — it simply stays absent from the
            // map, which the pure helper treats as expected-but-unavailable.
            const { accountId, date } = pairs[i];
            console.error(`Failed to load Cash As-Of for account ${accountId} on ${date}:`, result.reason);
          }
        });
        setCashAsOfMap(map);
      })
      .finally(() => {
        if (active && cashAsOfRequestIdRef.current === requestId) setCashAsOfLoading(false);
      });

    return () => { active = false; };
  }, [ctxLoading, loadingSnapshots, cashAccountsAllStatus, cashAccountsAll, investmentHistoryDates]);

  const totalAssetsHistoryLoading =
    ctxLoading || loadingSnapshots || cashAccountsAllStatus === "loading" || cashAsOfLoading;
  const totalAssetsHistorySummary = computeTotalAssetsHistory(
    investmentHistoryPoints,
    cashAccountsAllStatus,
    cashAccountsAll,
    cashAsOfMap
  );

  // Total Liabilities History (Phase 5, Milestone 2) — composes the same
  // shared historical date spine (investmentHistoryDates, above) with the
  // existing Liability As-Of contract. Independent phase pair, same shape
  // as the Cash phases above: (a) ALL Liabilities, active + archived, since
  // archived liabilities' historical evidence remains valid; (b) a bounded
  // Liability As-Of fan-out over (liability × investment-history-date)
  // pairs only — never a daily calendar series.
  const [liabilitiesAll, setLiabilitiesAll] = useState<Liability[]>([]);
  const [liabilitiesAllStatus, setLiabilitiesAllStatus] = useState<LiabilityLoadStatus>("loading");
  const liabilitiesAllRequestIdRef = useRef(0);

  useEffect(() => {
    const requestId = ++liabilitiesAllRequestIdRef.current;
    let active = true;
    setLiabilitiesAllStatus("loading");
    setLiabilitiesAll([]);

    listLiabilities(true)
      .then((items) => {
        if (!active || liabilitiesAllRequestIdRef.current !== requestId) return;
        setLiabilitiesAll(items);
        setLiabilitiesAllStatus("success");
      })
      .catch((reason) => {
        if (!active || liabilitiesAllRequestIdRef.current !== requestId) return;
        console.error("Failed to load liabilities (including archived) for Total Liabilities History:", reason);
        setLiabilitiesAll([]);
        setLiabilitiesAllStatus("error");
      });

    return () => { active = false; };
  }, [portfolios, ctxLoading, portfolioError]);

  const [liabilityAsOfMap, setLiabilityAsOfMap] = useState<Record<number, Record<string, LiabilityBalanceAsOf>>>({});
  const [liabilityAsOfLoading, setLiabilityAsOfLoading] = useState(false);
  const liabilityAsOfRequestIdRef = useRef(0);

  useEffect(() => {
    const requestId = ++liabilityAsOfRequestIdRef.current;
    let active = true;

    // Wait for both dependent phases to settle before fanning out, same
    // rationale as the Cash As-Of fan-out above.
    if (ctxLoading || loadingSnapshots || liabilitiesAllStatus === "loading") {
      return () => { active = false; };
    }

    if (liabilitiesAllStatus === "error" || liabilitiesAll.length === 0 || investmentHistoryDates.length === 0) {
      setLiabilityAsOfMap({});
      setLiabilityAsOfLoading(false);
      return () => { active = false; };
    }

    setLiabilityAsOfLoading(true);
    const pairs = liabilitiesAll.flatMap((liability) =>
      investmentHistoryDates.map((date) => ({ liabilityId: liability.id, date }))
    );

    Promise.allSettled(
      pairs.map(({ liabilityId, date }) =>
        getLiabilityBalanceAsOf(liabilityId, date).then((result) => ({ liabilityId, date, result }))
      )
    )
      .then((results) => {
        if (!active || liabilityAsOfRequestIdRef.current !== requestId) return;
        const map: Record<number, Record<string, LiabilityBalanceAsOf>> = {};
        results.forEach((result, i) => {
          if (result.status === "fulfilled") {
            const { liabilityId, date, result: asOf } = result.value;
            if (!map[liabilityId]) map[liabilityId] = {};
            map[liabilityId][date] = asOf;
          } else {
            // One failed pair must not fabricate a zero and must not discard
            // every other pair's evidence — it simply stays absent from the
            // map, which the pure helper treats as expected-but-unavailable.
            const { liabilityId, date } = pairs[i];
            console.error(`Failed to load Liability As-Of for liability ${liabilityId} on ${date}:`, result.reason);
          }
        });
        setLiabilityAsOfMap(map);
      })
      .finally(() => {
        if (active && liabilityAsOfRequestIdRef.current === requestId) setLiabilityAsOfLoading(false);
      });

    return () => { active = false; };
  }, [ctxLoading, loadingSnapshots, liabilitiesAllStatus, liabilitiesAll, investmentHistoryDates]);

  const totalLiabilitiesHistoryLoading =
    ctxLoading || loadingSnapshots || liabilitiesAllStatus === "loading" || liabilityAsOfLoading;
  const totalLiabilitiesHistorySummary = computeTotalLiabilitiesHistory(
    investmentHistoryDates,
    liabilitiesAllStatus,
    liabilitiesAll,
    liabilityAsOfMap
  );

  // Net Worth History (Phase 5, Milestone 3) — a pure derived composition of
  // the two summaries above, on the same shared date spine. No new fetch, no
  // new phase: it owns no evidence of its own.
  const netWorthHistoryLoading = totalAssetsHistoryLoading || totalLiabilitiesHistoryLoading;
  const netWorthHistorySummary = computeNetWorthHistory(
    investmentHistoryDates,
    totalAssetsHistorySummary,
    totalLiabilitiesHistorySummary
  );

  const isLoading = ctxLoading || loadingHoldings;

  return (
    <div className="space-y-10">
      <section>
        <h1 className="text-2xl font-bold mb-1">Wealth Overview</h1>
        {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
        {portfolioError && <p className="mt-2 text-sm text-red-500">{portfolioError}</p>}
      </section>

      <WealthOverview
        portfolios={portfolios}
        holdingsMap={holdingsMap}
        priceMap={priceMap}
        holdingsFailedMap={holdingsFailedMap}
        pricesLoaded={pricesLoaded}
        loading={isLoading}
        cashAccounts={cashAccounts}
        cashStatus={cashStatus}
        liabilities={liabilities}
        liabilityStatus={liabilityStatus}
        portfolioLoadError={portfolioError}
      />

      <CrossPortfolioIncome
        portfolios={portfolios}
        transactionsByPortfolio={transactionsMap}
        failedMap={transactionsFailedMap}
        loading={ctxLoading || loadingTransactions}
      />

      <CrossPortfolioWealthHistory
        portfolios={portfolios}
        snapshotsByPortfolio={snapshotsMap}
        failedMap={snapshotsFailedMap}
        loading={ctxLoading || loadingSnapshots}
      />

      <TotalAssetsHistoryCard summary={totalAssetsHistorySummary} loading={totalAssetsHistoryLoading} />

      <TotalLiabilitiesHistoryCard summary={totalLiabilitiesHistorySummary} loading={totalLiabilitiesHistoryLoading} />

      <NetWorthHistoryCard summary={netWorthHistorySummary} loading={netWorthHistoryLoading} />

      {isLoading ? (
        <p className="text-sm text-gray-400">Loading…</p>
      ) : (
        <DashboardHeatmap
          holdingsMap={holdingsMap}
          priceMap={priceMap}
          pricesLoaded={pricesLoaded}
          portfolios={portfolios}
        />
      )}
    </div>
  );
}
