"use client";

import { useEffect, useState } from "react";
import { getNetWorthChangeAttribution, type NetWorthChangeAttribution, type NetWorthChangeAttributionAvailable } from "@/lib/api";
import type { NetWorthHistorySummary } from "@/lib/netWorthHistory";

function fmtTHB(n: number): string {
  return Math.abs(n).toLocaleString("th-TH", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fmtSigned(n: number): string {
  return `${n >= 0 ? "+" : "-"}฿${fmtTHB(n)}`;
}

function fullDate(d: string): string {
  return new Date(d + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

// Bounded, factual explanations only — never an economic-completeness claim
// (Section 12). Reason codes come straight from the derived backend read.
const REASON_TEXT: Record<string, string> = {
  INVESTMENT_EVIDENCE_INCOMPLETE_AT_START: "Investment assets evidence is incomplete at the start date.",
  INVESTMENT_EVIDENCE_INCOMPLETE_AT_END: "Investment assets evidence is incomplete at the end date.",
  CASH_EVIDENCE_INCOMPLETE_AT_START: "External cash evidence is incomplete at the start date.",
  CASH_EVIDENCE_INCOMPLETE_AT_END: "External cash evidence is incomplete at the end date.",
  LIABILITY_EVIDENCE_INCOMPLETE_AT_START: "Liability evidence is incomplete at the start date.",
  LIABILITY_EVIDENCE_INCOMPLETE_AT_END: "Liability evidence is incomplete at the end date.",
  RECONCILIATION_FAILURE: "The balance-sheet components could not be reconciled to the Net Worth change.",
};

function reasonText(code: string): string {
  return REASON_TEXT[code] ?? "A required balance-sheet component is unavailable.";
}

type FetchState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; result: NetWorthChangeAttribution }
  | { status: "error" };

function AttributionAvailable({ result }: { result: NetWorthChangeAttributionAvailable }) {
  return (
    <div className="bg-white border rounded-xl p-5 shadow-sm space-y-4">
      <p className="text-xs text-gray-400">
        {fullDate(result.start_date)} → {fullDate(result.end_date)}
      </p>

      <div className="space-y-2">
        <div className="flex justify-between items-baseline">
          <span className="text-sm text-gray-500">Start Net Worth</span>
          <span className="text-sm font-semibold text-gray-800">฿{fmtTHB(result.start.net_worth)}</span>
        </div>
        <div className="flex justify-between items-baseline">
          <span className="text-sm text-gray-500">Investment assets</span>
          <span
            className={`text-sm font-semibold ${
              result.components.investment_assets_change >= 0 ? "text-emerald-700" : "text-red-600"
            }`}
          >
            {fmtSigned(result.components.investment_assets_change)}
          </span>
        </div>
        <div className="flex justify-between items-baseline">
          <span className="text-sm text-gray-500">External cash</span>
          <span
            className={`text-sm font-semibold ${
              result.components.external_cash_change >= 0 ? "text-emerald-700" : "text-red-600"
            }`}
          >
            {fmtSigned(result.components.external_cash_change)}
          </span>
        </div>
        <div>
          <div className="flex justify-between items-baseline">
            <span className="text-sm text-gray-500">Liability impact</span>
            <span
              className={`text-sm font-semibold ${
                result.components.liability_impact >= 0 ? "text-emerald-700" : "text-red-600"
              }`}
            >
              {fmtSigned(result.components.liability_impact)}
            </span>
          </div>
          <p className="text-xs text-gray-400 text-right mt-0.5">
            {result.components.liability_impact > 0
              ? `Liabilities decreased by ฿${fmtTHB(result.components.liability_impact)}`
              : result.components.liability_impact < 0
              ? `Liabilities increased by ฿${fmtTHB(result.components.liability_impact)}`
              : "Liabilities unchanged"}
          </p>
        </div>
        <div className="flex justify-between items-baseline pt-2 border-t">
          <span className="text-sm text-gray-500">End Net Worth</span>
          <span className="text-sm font-semibold text-gray-800">฿{fmtTHB(result.end.net_worth)}</span>
        </div>
      </div>

      {result.new_tracking_scope && (
        <p className="text-xs text-gray-400">Includes balances that began being tracked during this period.</p>
      )}
    </div>
  );
}

// Why Net Worth changed — Level-1 balance-sheet component attribution
// (ADR-013). Fetches its own single derived read for the same latest-two-
// complete-points window Net Worth History already uses; owns no historical
// evidence of its own. AVAILABLE/UNAVAILABLE are rendered as distinct states
// so an unavailable component is never shown as ฿0 (Section 22).
export default function NetWorthChangeAttributionCard({
  summary,
  loading,
}: {
  summary: NetWorthHistorySummary;
  loading: boolean;
}) {
  const startDate = summary.delta?.from.date ?? null;
  const endDate = summary.delta?.to.date ?? null;

  const [fetchState, setFetchState] = useState<FetchState>({ status: "idle" });

  useEffect(() => {
    if (!startDate || !endDate) {
      setFetchState({ status: "idle" });
      return;
    }
    let active = true;
    setFetchState({ status: "loading" });
    getNetWorthChangeAttribution(startDate, endDate)
      .then((result) => {
        if (active) setFetchState({ status: "loaded", result });
      })
      .catch(() => {
        if (active) setFetchState({ status: "error" });
      });
    return () => {
      active = false;
    };
  }, [startDate, endDate]);

  if (loading) {
    return (
      <section className="space-y-2" aria-busy="true">
        <div className="h-5 w-48 bg-gray-100 rounded animate-pulse" />
        <div className="h-32 bg-gray-100 rounded-xl animate-pulse" />
      </section>
    );
  }

  let body: React.ReactNode;
  if (!startDate || !endDate) {
    body = (
      <div className="bg-white border rounded-xl p-6 shadow-sm text-center">
        <p className="text-sm text-gray-500">Two complete Net Worth history points are needed.</p>
      </div>
    );
  } else if (fetchState.status === "idle" || fetchState.status === "loading") {
    body = <div className="h-32 bg-gray-100 rounded-xl animate-pulse" aria-busy="true" />;
  } else if (fetchState.status === "error") {
    body = (
      <div className="bg-white border rounded-xl p-6 shadow-sm text-center">
        <p className="text-sm text-red-500">Unable to load Net Worth change attribution.</p>
      </div>
    );
  } else if (fetchState.result.status === "UNAVAILABLE") {
    const result = fetchState.result;
    body = (
      <div className="bg-white border rounded-xl p-6 shadow-sm text-center space-y-1">
        <p className="text-sm text-gray-500">
          Attribution unavailable for {fullDate(result.start_date)} → {fullDate(result.end_date)}.
        </p>
        {result.reason_codes.map((code) => (
          <p key={code} className="text-xs text-gray-400">
            {reasonText(code)}
          </p>
        ))}
      </div>
    );
  } else {
    body = <AttributionAvailable result={fetchState.result} />;
  }

  return (
    <section className="space-y-3">
      <h2 className="text-base font-semibold text-gray-500 uppercase tracking-wide">Why Net Worth changed</h2>
      {body}
    </section>
  );
}
