"use client";

// Cross-Portfolio Exposure Snapshot — "What sectors am I exposed to across
// all portfolios?" Deliberately no Low/Medium/High/Critical labels, no HHI,
// no concentration flags — those are SectorConcentrationPanel's authorized,
// single-portfolio vocabulary and are not reused or implied here. Cash is
// disclosed separately and is never assigned a sector.

import { sectorColor } from "@/lib/sectors";
import type { ExposureSnapshot } from "@/lib/crossPortfolioExposure";
import { formatThb, formatPct } from "./formatting";

export default function SectorExposureSection({ snapshot }: { snapshot: ExposureSnapshot }) {
  return (
    <section className="space-y-3">
      <div>
        <h2 className="text-lg font-semibold">Aggregate sector exposure</h2>
        <p className="text-xs text-gray-400">% of total invested holdings value — cash is excluded from this share</p>
      </div>

      {snapshot.sectors.length === 0 ? (
        <p className="text-sm text-gray-400">No holdings to show.</p>
      ) : (
        <div className="space-y-3">
          {snapshot.sectors.map((s) => (
            <div key={s.sector} className="space-y-1">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="inline-block w-2.5 h-2.5 rounded-full" style={{ backgroundColor: sectorColor(s.sector) }} />
                  <span className="text-sm font-medium">{s.sector}</span>
                </div>
                <div className="text-right">
                  <span className="text-sm font-semibold tabular-nums">{formatThb(s.value)}</span>
                  <span className="text-xs text-gray-400 tabular-nums ml-2">{formatPct(s.sharePctOfHoldings)}</span>
                </div>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                <div
                  className="h-1.5 rounded-full"
                  style={{ width: `${Math.min(s.sharePctOfHoldings, 100)}%`, backgroundColor: sectorColor(s.sector) }}
                />
              </div>
              <p className="text-xs text-gray-400">
                {s.portfolios.map((p) => `${p.name} ${formatPct(p.sharePctOfSector)}`).join(" · ")}
              </p>
            </div>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between text-xs text-gray-400 pt-2 border-t border-gray-100">
        <span>Cash (not sector-classified)</span>
        <span className="tabular-nums">
          {formatThb(snapshot.totalCash)} · {formatPct(snapshot.totalValue > 0 ? (snapshot.totalCash / snapshot.totalValue) * 100 : 0)} of total portfolio value
        </span>
      </div>
    </section>
  );
}
