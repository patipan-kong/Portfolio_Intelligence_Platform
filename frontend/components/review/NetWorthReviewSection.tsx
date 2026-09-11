"use client";

// Periodic Review — Net Worth section (Slice 1). Deliberately duplicates the
// existing Net Worth History phase pipeline from app/page.tsx rather than
// refactoring that page into a shared hook: `/` is a heavily-tested,
// intricately request-guarded page, and this section's own contract
// forbids a broad component refactor merely to maximize reuse. What it does
// reuse verbatim, unmodified, is the actual computation and rendering:
// computeWealthHistory / computeTotalAssetsHistory /
// computeTotalLiabilitiesHistory / computeNetWorthHistory and
// NetWorthChangeAttributionCard itself. No new arithmetic is introduced
// here — every number this section shows is produced by those existing
// pure functions or that existing component.
//
// DOGFOOD-01: Cash/Liability As-Of evidence is fetched via the batch
// endpoints (getCashAccountBalancesAsOf / getLiabilityBalancesAsOf — one
// request per domain, for every account/liability and every history date at
// once) rather than one getCashAccountBalanceAsOf/getLiabilityBalanceAsOf
// call per (account, date) pair. That per-pair fan-out — accounts x dates,
// liabilities x dates — was the original implementation here and is what
// produced the request storm; the batch endpoints compose the same
// cash_balance_as_of/liability_balance_as_of primitives server-side and
// return an identically-shaped evidence map, so computeTotalAssetsHistory /
// computeTotalLiabilitiesHistory are unchanged.

import { useEffect, useMemo, useRef, useState } from "react";
import { usePortfolio } from "@/lib/PortfolioContext";
import {
  getCashAccountBalancesAsOf,
  getLiabilityBalancesAsOf,
  getSnapshots,
  listCashAccounts,
  listLiabilities,
} from "@/lib/api";
import type {
  CashAccount,
  CashAccountBalanceAsOf,
  Liability,
  LiabilityBalanceAsOf,
  PortfolioSnapshotRow,
} from "@/lib/api";
import type { AssetLoadStatus } from "@/lib/totalAssets";
import type { LiabilityLoadStatus } from "@/lib/totalLiabilities";
import { computeWealthHistory } from "@/lib/wealthHistory";
import { computeTotalAssetsHistory } from "@/lib/totalAssetsHistory";
import { computeTotalLiabilitiesHistory } from "@/lib/totalLiabilitiesHistory";
import { computeNetWorthHistory } from "@/lib/netWorthHistory";
import NetWorthChangeAttributionCard from "@/components/NetWorthChangeAttributionCard";

// Matches the Performance page's / Dashboard's own getSnapshots() default.
const MAX_SNAPSHOTS = 365;

function fmtTHB(n: number): string {
  return n.toLocaleString("th-TH", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export default function NetWorthReviewSection() {
  const { portfolios, loading: ctxLoading, error: portfolioError } = usePortfolio();

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
        console.error("Periodic Review: failed to load Cash Accounts for Net Worth section:", reason);
        setCashAccountsAll([]);
        setCashAccountsAllStatus("error");
      });

    return () => { active = false; };
  }, [portfolios, ctxLoading, portfolioError]);

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
        console.error("Periodic Review: failed to load Liabilities for Net Worth section:", reason);
        setLiabilitiesAll([]);
        setLiabilitiesAllStatus("error");
      });

    return () => { active = false; };
  }, [portfolios, ctxLoading, portfolioError]);

  const [snapshotsMap, setSnapshotsMap] = useState<Record<number, PortfolioSnapshotRow[]>>({});
  const [snapshotsFailedMap, setSnapshotsFailedMap] = useState<Record<number, boolean>>({});
  const [loadingSnapshots, setLoadingSnapshots] = useState(false);
  const snapshotsRequestIdRef = useRef(0);

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
      portfolios.map((p) => getSnapshots(p.id, MAX_SNAPSHOTS).then((items) => ({ id: p.id, items })))
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
            console.error(`Periodic Review: failed to load snapshots for portfolio ${pid}:`, result.reason);
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

  // Memoized: computeWealthHistory returns a new points array each call, and
  // an unmemoized derivation here would hand the effects below a new
  // `investmentHistoryDates` array reference on every render (even when the
  // underlying dates are unchanged), which — because that array is a
  // dependency of the fetch effects below — would re-trigger those fetches
  // on every render (including the re-renders those fetches themselves
  // cause), a self-sustaining request loop layered on top of the fan-out
  // this file's batch endpoints already fix.
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

    if (ctxLoading || loadingSnapshots || cashAccountsAllStatus === "loading") {
      return () => { active = false; };
    }

    if (cashAccountsAllStatus === "error" || cashAccountsAll.length === 0 || investmentHistoryDates.length === 0) {
      setCashAsOfMap({});
      setCashAsOfLoading(false);
      return () => { active = false; };
    }

    setCashAsOfLoading(true);
    getCashAccountBalancesAsOf(investmentHistoryDates, true)
      .then((response) => {
        if (!active || cashAsOfRequestIdRef.current !== requestId) return;
        const map: Record<number, Record<string, CashAccountBalanceAsOf>> = {};
        for (const [accountIdStr, byDate] of Object.entries(response)) {
          const accountId = Number(accountIdStr);
          map[accountId] = {};
          for (const [date, evidence] of Object.entries(byDate)) {
            map[accountId][date] = {
              cash_account_id: accountId,
              date,
              currency: "THB",
              balance: evidence.balance,
              available: evidence.available,
              // Not returned by the batch endpoint; computeTotalAssetsHistory
              // never reads it (only balance/available — see CashAsOfEvidence).
              baseline_effective_on: null,
            };
          }
        }
        setCashAsOfMap(map);
      })
      .catch((reason) => {
        if (!active || cashAsOfRequestIdRef.current !== requestId) return;
        console.error("Periodic Review: failed to load Cash As-Of balances:", reason);
        setCashAsOfMap({});
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

  const [liabilityAsOfMap, setLiabilityAsOfMap] = useState<Record<number, Record<string, LiabilityBalanceAsOf>>>({});
  const [liabilityAsOfLoading, setLiabilityAsOfLoading] = useState(false);
  const liabilityAsOfRequestIdRef = useRef(0);

  useEffect(() => {
    const requestId = ++liabilityAsOfRequestIdRef.current;
    let active = true;

    if (ctxLoading || loadingSnapshots || liabilitiesAllStatus === "loading") {
      return () => { active = false; };
    }

    if (liabilitiesAllStatus === "error" || liabilitiesAll.length === 0 || investmentHistoryDates.length === 0) {
      setLiabilityAsOfMap({});
      setLiabilityAsOfLoading(false);
      return () => { active = false; };
    }

    setLiabilityAsOfLoading(true);
    getLiabilityBalancesAsOf(investmentHistoryDates, true)
      .then((response) => {
        if (!active || liabilityAsOfRequestIdRef.current !== requestId) return;
        const map: Record<number, Record<string, LiabilityBalanceAsOf>> = {};
        for (const [liabilityIdStr, byDate] of Object.entries(response)) {
          const liabilityId = Number(liabilityIdStr);
          map[liabilityId] = {};
          for (const [date, evidence] of Object.entries(byDate)) {
            map[liabilityId][date] = {
              liability_id: liabilityId,
              date,
              currency: evidence.currency,
              balance: evidence.balance,
              available: evidence.available,
            };
          }
        }
        setLiabilityAsOfMap(map);
      })
      .catch((reason) => {
        if (!active || liabilityAsOfRequestIdRef.current !== requestId) return;
        console.error("Periodic Review: failed to load Liability As-Of balances:", reason);
        setLiabilityAsOfMap({});
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

  const netWorthHistoryLoading = totalAssetsHistoryLoading || totalLiabilitiesHistoryLoading;
  const netWorthHistorySummary = computeNetWorthHistory(
    investmentHistoryDates,
    totalAssetsHistorySummary,
    totalLiabilitiesHistorySummary
  );

  return (
    <section className="space-y-3">
      <h2 className="text-lg font-semibold">Net Worth</h2>
      {portfolioError && <p className="text-sm text-red-500">{portfolioError}</p>}
      {!netWorthHistoryLoading && netWorthHistorySummary.latest && (
        <p className="text-sm text-gray-600">
          Latest recorded Net Worth: <strong>฿{fmtTHB(netWorthHistorySummary.latest.netWorth as number)}</strong>
          <span className="text-xs text-gray-400"> as of {netWorthHistorySummary.latest.date}</span>
        </p>
      )}
      <NetWorthChangeAttributionCard summary={netWorthHistorySummary} loading={netWorthHistoryLoading} />
    </section>
  );
}
