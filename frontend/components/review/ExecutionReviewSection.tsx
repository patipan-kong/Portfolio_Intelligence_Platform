"use client";

// Periodic Review — Execution section (Slice 1). Reuses the three existing
// canonical Execution Ledger workflow predicates verbatim (see
// @/lib/executionWorkflow, extracted from /ai-analytics/execution) instead
// of re-deriving "deserves review". A row may satisfy more than one
// predicate; this section renders them as separate factual groups rather
// than inventing a combined severity/priority count.

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePortfolio } from "@/lib/PortfolioContext";
import { getExecutionLedger, isUnresolvedPortfolioError, type ExecutionLedger, type ExecutionLedgerRow } from "@/lib/api";
import { needsFollowUp, needsRecording, needsReview, sortNeedsFollowUpRows, sortNeedsReviewRows } from "@/lib/executionWorkflow";

const PERIOD_DAYS = 90;
const MAX_ROWS_SHOWN = 5;

type LoadState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "loaded"; data: ExecutionLedger };

function RowList({ rows, emptyMessage }: { rows: ExecutionLedgerRow[]; emptyMessage: string }) {
  if (rows.length === 0) return <p className="text-xs text-gray-500">{emptyMessage}</p>;
  return (
    <ul className="space-y-1">
      {rows.slice(0, MAX_ROWS_SHOWN).map((row) => (
        <li key={row.decision_id} className="text-sm">
          <Link href={`/ai-analytics/execution/${row.decision_id}`} className="text-blue-600 hover:underline">
            #{row.snapshot_id} · {row.decision}{row.date ? ` · ${row.date.slice(0, 10)}` : ""}
          </Link>
        </li>
      ))}
      {rows.length > MAX_ROWS_SHOWN && (
        <li className="text-xs text-gray-400">and {rows.length - MAX_ROWS_SHOWN} more</li>
      )}
    </ul>
  );
}

export default function ExecutionReviewSection() {
  const { currentSelection, reportUnresolvedPortfolio } = usePortfolio();
  const [state, setState] = useState<LoadState>({ status: "loading" });
  const requestIdRef = useRef<number | null>(null);

  const load = useCallback(async (portfolioId: number) => {
    setState({ status: "loading" });
    try {
      const result = await getExecutionLedger(portfolioId, PERIOD_DAYS);
      if (requestIdRef.current !== portfolioId) return;
      setState({ status: "loaded", data: result });
    } catch (e) {
      if (requestIdRef.current !== portfolioId) return;
      setState({ status: "error", message: e instanceof Error ? e.message : "Failed to load execution ledger" });
      if (isUnresolvedPortfolioError(e)) reportUnresolvedPortfolio(portfolioId);
    }
  }, [reportUnresolvedPortfolio]);

  useEffect(() => {
    requestIdRef.current = currentSelection;
    if (currentSelection == null) return;
    void load(currentSelection);
  }, [currentSelection, load]);

  return (
    <section className="space-y-3">
      <h2 className="text-lg font-semibold">Execution</h2>
      {currentSelection == null ? (
        <p className="text-sm text-gray-400">Select a portfolio to view Execution.</p>
      ) : state.status === "loading" ? (
        <p className="text-sm text-gray-400">Loading execution…</p>
      ) : state.status === "error" ? (
        <p role="alert" className="text-sm text-red-600">{state.message}</p>
      ) : state.data.status === "cold_start" ? (
        <p className="text-sm text-gray-500">No decisions recorded yet in this window.</p>
      ) : (
        (() => {
          const rows = state.data.rows;
          const reviewRows = sortNeedsReviewRows(rows.filter(needsReview));
          const followUpRows = sortNeedsFollowUpRows(rows.filter(needsFollowUp));
          const recordingCount = rows.filter(needsRecording).length;
          return (
            <div className="space-y-3">
              <div>
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
                  Needs review ({reviewRows.length})
                </p>
                <RowList rows={reviewRows} emptyMessage="No decisions need review right now." />
              </div>
              <div>
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
                  Needs follow-up ({followUpRows.length})
                </p>
                <RowList rows={followUpRows} emptyMessage="No decisions eligible for human review in this window have a mixed or off-track review." />
              </div>
              <p className="text-xs text-gray-500">
                {recordingCount === 0
                  ? "No decisions with incomplete transaction recording in this window."
                  : `${recordingCount} ${recordingCount === 1 ? "decision has" : "decisions have"} incomplete transaction recording.`}
              </p>
              <Link href="/ai-analytics/execution" className="text-xs font-semibold text-blue-600 hover:underline">
                Full Execution Ledger →
              </Link>
            </div>
          );
        })()
      )}
    </section>
  );
}
