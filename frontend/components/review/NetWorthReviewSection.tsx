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

import { useEffect, useRef, useState } from "react";
import { usePortfolio } from "@/lib/PortfolioContext";
import {
  getCashAccountBalanceAsOf,
  getLiabilityBalanceAsOf,
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

  const investmentHistoryPoints = computeWealthHistory(portfolios, snapshotsMap, snapshotsFailedMap).points;
  const investmentHistoryDates = investmentHistoryPoints.map((p) => p.date);

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
            const { accountId, date } = pairs[i];
            console.error(`Periodic Review: failed to load Cash As-Of for account ${accountId} on ${date}:`, result.reason);
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
            const { liabilityId, date } = pairs[i];
            console.error(`Periodic Review: failed to load Liability As-Of for liability ${liabilityId} on ${date}:`, result.reason);
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
