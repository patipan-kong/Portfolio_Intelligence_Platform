"use client";

// Cross-Portfolio Exposure Snapshot — "Which symbols do I hold in more than
// one portfolio?" Exact-symbol overlap only (no security-identity inference
// across different tickers). A quiet factual empty state when there is none
// — never implied as a problem, and never implying multiple portfolios are
// required to use this page.

import type { ExposureSnapshot } from "@/lib/crossPortfolioExposure";
import { formatThb, formatPct } from "./formatting";

export default function SymbolOverlapSection({ snapshot }: { snapshot: ExposureSnapshot }) {
  return (
    <section className="space-y-3">
      <div>
        <h2 className="text-lg font-semibold">Overlapping holdings</h2>
        <p className="text-xs text-gray-400">Symbols held in more than one portfolio</p>
      </div>

      {snapshot.overlaps.length === 0 ? (
        <p className="text-sm text-gray-400">No symbols are currently held in more than one portfolio.</p>
      ) : (
        <div className="space-y-3">
          {snapshot.overlaps.map((o) => (
            <div key={o.symbol} className="space-y-1 border-b border-gray-100 pb-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">{o.symbol}</span>
                <div className="text-right">
                  <span className="text-sm font-semibold tabular-nums">{formatThb(o.totalValue)}</span>
                  <span className="text-xs text-gray-400 ml-2">
                    held in {o.portfolioCount} portfolios
                  </span>
                </div>
              </div>
              <p className="text-xs text-gray-400">
                {o.portfolios
                  .map((p) => `${p.name}: ${formatThb(p.value)} (${formatPct(p.sharePctOfSymbol)})`)
                  .join(" · ")}
              </p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
