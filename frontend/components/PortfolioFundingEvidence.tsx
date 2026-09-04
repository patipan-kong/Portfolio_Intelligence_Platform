"use client";

import { useEffect, useRef, useState } from "react";
import { getPortfolioFundingEvidence, type PortfolioFundingEvidenceEvent } from "@/lib/api";

const DISCLOSURE =
  "Recorded cash-side investment-funding events that named this portfolio. This is documentary evidence only — it does not prove a portfolio transaction, settlement, or reconciliation occurred.";

const EMPTY_STATE = "No recorded cash-side investment funding evidence for this portfolio.";

function formatThb(value: number): string {
  return value.toLocaleString("th-TH", { style: "currency", currency: "THB", minimumFractionDigits: 2 });
}

function directionLabel(event: PortfolioFundingEvidenceEvent): string {
  return event.investment_direction === "FROM_PORTFOLIO" ? "Recorded from this portfolio" : "Recorded to this portfolio";
}

export default function PortfolioFundingEvidence({ portfolioId }: { portfolioId: number }) {
  const [events, setEvents] = useState<PortfolioFundingEvidenceEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const currentPortfolioIdRef = useRef(portfolioId);

  useEffect(() => {
    currentPortfolioIdRef.current = portfolioId;
    let active = true;
    setLoading(true);
    setError(null);
    setEvents([]);
    getPortfolioFundingEvidence(portfolioId)
      .then((next) => {
        if (!active) return;
        setEvents(next);
      })
      .catch((err: unknown) => {
        if (active) setError(err instanceof Error ? err.message : "Unable to load funding evidence");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, [portfolioId]);

  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm" aria-labelledby="funding-evidence-heading">
      <h2 id="funding-evidence-heading" className="text-sm font-semibold text-gray-700">
        Portfolio Funding Evidence
      </h2>
      <p className="text-xs text-gray-500 mt-1">{DISCLOSURE}</p>

      {loading ? (
        <p className="text-sm text-gray-400 mt-3">Loading…</p>
      ) : error ? (
        <p role="alert" className="text-xs text-red-600 mt-3">{error}</p>
      ) : events.length === 0 ? (
        <p className="text-sm text-gray-500 mt-3">{EMPTY_STATE}</p>
      ) : (
        <ul className="mt-3 space-y-2">
          {events.map((event) => (
            <li key={event.id} className="border rounded-lg px-3 py-2 text-sm">
              <div className="flex items-center justify-between gap-3">
                <span className="text-gray-700">{formatThb(Math.abs(event.amount))} · {directionLabel(event)}</span>
                <span className="text-xs text-gray-400 whitespace-nowrap">{event.occurred_on}</span>
              </div>
              <p className="text-xs text-gray-500 mt-0.5">
                {event.account_name}
                {event.account_is_archived ? " (Archived)" : ""}
                {" · Portfolio name at recording: "}
                {event.counterparty_portfolio_name_snapshot}
              </p>
              {event.note && <p className="text-xs text-gray-600 mt-1 break-words">{event.note}</p>}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
