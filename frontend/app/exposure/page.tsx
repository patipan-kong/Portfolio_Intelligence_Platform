"use client";

// Cross-Portfolio Exposure Snapshot (Slice 1) — current-snapshot, descriptive
// only. Answers: how is current value distributed across portfolios, what is
// the aggregate sector exposure, and which symbols are held in more than one
// portfolio. No historical trend, no benchmark-relative attribution, no
// severity/risk labels, no target allocation, no rebalance guidance — see
// the Cross-Portfolio Exposure reconnaissance/slice reports for why those
// are explicitly out of scope.
//
// Reuses the exact same two-phase holdings-then-prices fan-out the home
// page already pays for its heatmap/wealth overview (Promise.allSettled per
// portfolio, holdings phase gating the price phase) — no new backend
// endpoint, no new request pattern.

import { useEffect, useRef, useState } from "react";
import { usePortfolio } from "@/lib/PortfolioContext";
import { getHoldings, getPortfolioPrices } from "@/lib/api";
import type { PortfolioItem, PriceRefreshItem } from "@/lib/api";
import { computeExposureSnapshot } from "@/lib/crossPortfolioExposure";
import PortfolioContributionSection from "@/components/exposure/PortfolioContributionSection";
import SectorExposureSection from "@/components/exposure/SectorExposureSection";
import SymbolOverlapSection from "@/components/exposure/SymbolOverlapSection";

export default function ExposurePage() {
  const { portfolios, loading: ctxLoading, error: portfolioError } = usePortfolio();
  const [holdingsMap, setHoldingsMap] = useState<Record<number, PortfolioItem[]>>({});
  const [holdingsFailedMap, setHoldingsFailedMap] = useState<Record<number, boolean>>({});
  const [priceMap, setPriceMap] = useState<Record<number, PriceRefreshItem[]>>({});
  const [loadingHoldings, setLoadingHoldings] = useState(true);
  const [holdingsSettled, setHoldingsSettled] = useState(false);
  const [pricesLoaded, setPricesLoaded] = useState(false);
  const [error, setError] = useState("");

  const holdingsRequestIdRef = useRef(0);
  const priceRequestIdRef = useRef(0);

  // Phase 1: holdings, one request per portfolio — Promise.allSettled so one
  // portfolio's failure never hides the others; the failed one is flagged,
  // not silently dropped or treated as zero.
  useEffect(() => {
    const requestId = ++holdingsRequestIdRef.current;
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

  // Phase 2: live prices, once holdings have settled (same fallback-to-
  // avg_cost convention as the rest of the app — never zeroed).
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
          console.error(`Failed to load prices for portfolio ${portfolios[i].id}:`, result.reason);
        }
      });
      setPriceMap(map);
      setPricesLoaded(true);
    });

    return () => { active = false; };
  }, [holdingsSettled, portfolios]);

  if (portfolioError) {
    return (
      <div className="max-w-4xl">
        <h1 className="text-2xl font-bold mb-2">Cross-Portfolio Exposure</h1>
        <p className="text-sm text-red-500">{portfolioError}</p>
      </div>
    );
  }

  if (ctxLoading || (loadingHoldings && !holdingsSettled)) {
    return (
      <div className="max-w-4xl">
        <h1 className="text-2xl font-bold mb-2">Cross-Portfolio Exposure</h1>
        <p className="text-sm text-gray-400">Loading portfolios…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl">
        <h1 className="text-2xl font-bold mb-2">Cross-Portfolio Exposure</h1>
        <p className="text-sm text-red-500">{error}</p>
      </div>
    );
  }

  if (portfolios.length === 0) {
    return (
      <div className="max-w-4xl">
        <h1 className="text-2xl font-bold mb-2">Cross-Portfolio Exposure</h1>
        <p className="text-sm text-gray-400">No portfolios yet — add a portfolio to see current exposure.</p>
      </div>
    );
  }

  const snapshot = computeExposureSnapshot(portfolios, holdingsMap, priceMap, holdingsFailedMap);

  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold">Cross-Portfolio Exposure</h1>
        <p className="text-sm text-gray-500 mt-1">
          Current value distribution, aggregate sector exposure, and holdings overlap across your portfolios.
        </p>
      </div>

      {snapshot.failedPortfolioNames.length > 0 && (
        <p className="text-sm text-amber-600 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2">
          Could not load holdings for: {snapshot.failedPortfolioNames.join(", ")}. Totals below exclude{" "}
          {snapshot.failedPortfolioNames.length === 1 ? "this portfolio" : "these portfolios"} — they are not
          counted as zero.
        </p>
      )}

      {!pricesLoaded && (
        <p className="text-xs text-gray-400 flex items-center gap-1">
          <span className="inline-block w-2.5 h-2.5 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
          Loading live prices…
        </p>
      )}

      {pricesLoaded && snapshot.anyEstimatedPrice && (
        <p className="text-xs text-gray-400">
          Some holdings have no confirmed live price and use their average cost instead.
        </p>
      )}

      <PortfolioContributionSection snapshot={snapshot} />
      <SectorExposureSection snapshot={snapshot} />
      <SymbolOverlapSection snapshot={snapshot} />
    </div>
  );
}
