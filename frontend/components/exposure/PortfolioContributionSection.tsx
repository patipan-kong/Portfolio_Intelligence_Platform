"use client";

// Cross-Portfolio Exposure Snapshot — "How is my current value distributed
// across portfolios?" Factual current value and share only — no ranking,
// no best/worst framing.

import type { ExposureSnapshot } from "@/lib/crossPortfolioExposure";
import { formatThb, formatPct } from "./formatting";

export default function PortfolioContributionSection({ snapshot }: { snapshot: ExposureSnapshot }) {
  return (
    <section className="space-y-3">
      <div>
        <h2 className="text-lg font-semibold">Portfolio contribution</h2>
        <p className="text-xs text-gray-400">% of total current portfolio value (cash + holdings)</p>
      </div>

      {snapshot.portfolios.length === 0 ? (
        <p className="text-sm text-gray-400">No portfolios to show.</p>
      ) : (
        <div className="space-y-2">
          {snapshot.portfolios.map((p) => (
            <div key={p.portfolioId} className="flex items-center justify-between border-b border-gray-100 py-2">
              <div>
                <p className="text-sm font-medium">{p.name}</p>
                {p.failed ? (
                  <p className="text-xs text-red-500">Could not load holdings — excluded from totals</p>
                ) : (
                  <p className="text-xs text-gray-400">
                    {formatThb(p.holdingsValue)} holdings + {formatThb(p.cash)} cash
                  </p>
                )}
              </div>
              <div className="text-right">
                {p.failed ? (
                  <span className="text-sm text-gray-400">—</span>
                ) : (
                  <>
                    <p className="text-sm font-semibold tabular-nums">{formatThb(p.total)}</p>
                    <p className="text-xs text-gray-400 tabular-nums">{formatPct(p.sharePctOfTotalValue!)}</p>
                  </>
                )}
              </div>
            </div>
          ))}
          <div className="flex items-center justify-between pt-2 font-semibold">
            <span className="text-sm">Total</span>
            <span className="text-sm tabular-nums">{formatThb(snapshot.totalValue)}</span>
          </div>
        </div>
      )}
    </section>
  );
}
