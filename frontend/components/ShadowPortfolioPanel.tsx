"use client";

import { useEffect, useMemo, useState } from "react";
import {
  getShadowPerformanceSummary,
  getAttributionSummary,
  type ShadowPerformanceSummary,
  type AttributionSummaryResponse,
} from "@/lib/api";
import { safeReturn, fmtPct, windowedDivergence, windowedAiDrawdown } from "@/lib/shadowSummary";

function pctClass(v: number | null | undefined): string {
  const safe = safeReturn(v);
  if (safe == null) return "text-gray-500";
  if (safe > 0) return "text-green-700";
  if (safe < 0) return "text-red-600";
  return "text-gray-500";
}

function MetricRow({ label, value, className }: { label: string; value: string; className?: string }) {
  return (
    <div className="flex items-center justify-between text-xs">
      <span className="text-gray-500">{label}</span>
      <span className={`font-semibold ${className ?? "text-gray-700"}`}>{value}</span>
    </div>
  );
}

export default function ShadowPortfolioPanel({ portfolioId }: { portfolioId: number }) {
  const [shadowSummary, setShadowSummary] = useState<ShadowPerformanceSummary | null>(null);
  const [attribution, setAttribution] = useState<AttributionSummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    setLoading(true);
    Promise.all([
      getShadowPerformanceSummary(portfolioId),
      getAttributionSummary(portfolioId, 30),
    ])
      .then(([summary, attr]) => {
        if (!active) return;
        setShadowSummary(summary);
        setAttribution(attr);
      })
      .catch(() => {
        if (!active) return;
        setShadowSummary(null);
        setAttribution(null);
      })
      .finally(() => {
        if (!active) return;
        setLoading(false);
      });

    const onDecision = () => {
      Promise.all([
        getShadowPerformanceSummary(portfolioId),
        getAttributionSummary(portfolioId, 30),
      ])
        .then(([summary, attr]) => {
          setShadowSummary(summary);
          setAttribution(attr);
        })
        .catch(() => {
          setShadowSummary(null);
          setAttribution(null);
        });
    };

    window.addEventListener("execution-decision-recorded", onDecision);
    return () => {
      active = false;
      window.removeEventListener("execution-decision-recorded", onDecision);
    };
  }, [portfolioId]);

  const staticShadow = shadowSummary?.summary?.static_frozen ?? null;
  const aiModel = shadowSummary?.summary?.active_model ?? null;
  const actual = attribution?.current.actual ?? null;

  // A shadow is "tracking started" when it exists but has no valid return data yet
  // (e.g. inception_return_pct is null or corrupted, snapshot_count < 2)
  const staticIsNew =
    staticShadow != null &&
    safeReturn(staticShadow.inception_return_pct) == null &&
    (staticShadow.snapshot_count ?? 0) < 2;
  const aiIsNew =
    aiModel != null &&
    safeReturn(aiModel.inception_return_pct) == null &&
    (aiModel.snapshot_count ?? 0) < 2;

  // Phase 4.23: divergence is a 30D-window comparison only (see
  // windowedDivergence); never since-inception minus 30D.
  const current = attribution?.current ?? null;
  const windowDays = current?.evaluation_window_days ?? 30;
  // The 30D selector may pick an older decision shadow than the latest frozen
  // decision shown above — identify it rather than assume they match.
  const staticSelection = current?.static_shadow_selection ?? null;
  const aiWindowDrawdown = windowedAiDrawdown(current);
  const staticDivergence = useMemo(() => windowedDivergence(current, "static"), [current]);
  const aiDivergence = useMemo(
    () => windowedDivergence(current, "ai", aiModel?.inception_date),
    [current, aiModel],
  );

  if (loading) {
    return (
      <section className="bg-white border border-gray-200 rounded-xl p-5">
        <h2 className="text-sm font-semibold text-gray-800">Shadow Portfolio Tracking</h2>
        <p className="text-xs text-gray-400 mt-2">Loading shadow portfolios...</p>
      </section>
    );
  }

  if (!shadowSummary?.has_shadows) {
    return (
      <section className="bg-white border border-gray-200 rounded-xl p-5">
        <h2 className="text-sm font-semibold text-gray-800">Shadow Portfolio Tracking</h2>
        <p className="text-xs text-gray-400 mt-2">
          No active shadow portfolios yet. Record an optimizer decision to begin paper-trading lifecycle tracking.
        </p>
      </section>
    );
  }

  return (
    <section className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-5 py-4 border-b border-gray-100">
        <h2 className="text-sm font-semibold text-gray-800">Shadow Portfolio Dashboard</h2>
        <p className="text-xs text-gray-400 mt-0.5">Counterfactual tracking for execution quality</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 p-5">
        <div className="border border-gray-200 rounded-lg p-4 bg-gray-50/50">
          <p className="text-xs uppercase tracking-wide text-gray-500">Static Shadow Portfolio</p>
          <p className="text-xs text-gray-400 mt-0.5">What if no rebalance happened?</p>
          <p className="text-[11px] font-medium text-gray-600 mt-3">
            Latest Frozen Decision — since inception
            {staticShadow?.inception_date ? ` (${staticShadow.inception_date})` : ""}
          </p>
          {staticShadow == null ? (
            <p className="text-xs text-gray-400 mt-1">No execution decision has been frozen yet.</p>
          ) : staticIsNew ? (
            <div className="mt-1 flex items-center gap-2">
              <span className="inline-block w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
              <span className="text-xs text-blue-600">Tracking started — first valuation at 17:45 ICT</span>
            </div>
          ) : (
            <div className="mt-1 space-y-2">
              <MetricRow
                label="Cumulative Return"
                value={fmtPct(staticShadow.inception_return_pct)}
                className={pctClass(staticShadow.inception_return_pct)}
              />
              <MetricRow
                label="Alpha"
                value={fmtPct(staticShadow.latest_alpha)}
                className={pctClass(staticShadow.latest_alpha)}
              />
            </div>
          )}
          <p className="text-[11px] font-medium text-gray-600 mt-3">
            Historical Attribution — {windowDays}D window
          </p>
          <p className="text-[11px] text-gray-400 mt-0.5" data-testid="static-window-shadow">
            {staticSelection?.status === "selected"
              ? `Decision shadow #${staticSelection.shadow_id}${
                  staticSelection.inception_date ? ` · frozen ${staticSelection.inception_date}` : ""
                }`
              : staticSelection?.status === "no_decision_shadow"
                ? "No frozen decision shadow exists for this window."
                : `No frozen decision shadow covers the full ${windowDays}D window.`}
          </p>
          <div className="mt-1 space-y-2">
            <MetricRow
              label="Drawdown"
              value={fmtPct(attribution?.current.static_shadow?.max_drawdown_pct ?? null)}
              className="text-red-600"
            />
            <MetricRow
              label="Divergence vs Actual"
              value={fmtPct(staticDivergence)}
              className={pctClass(staticDivergence)}
            />
          </div>
        </div>

        <div className="border border-gray-200 rounded-lg p-4 bg-blue-50/40">
          <p className="text-xs uppercase tracking-wide text-gray-500">AI Model Portfolio</p>
          <p className="text-xs text-gray-400 mt-0.5">Cumulative track record</p>
          <p className="text-[11px] font-medium text-gray-600 mt-3">
            AI Model — since inception
            {aiModel?.inception_date ? ` (${aiModel.inception_date})` : ""}
          </p>
          {aiIsNew ? (
            <div className="mt-1 flex items-center gap-2">
              <span className="inline-block w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
              <span className="text-xs text-blue-600">Tracking started — first valuation at 17:45 ICT</span>
            </div>
          ) : (
            <div className="mt-1 space-y-2">
              <MetricRow
                label="Cumulative Return"
                value={fmtPct(aiModel?.inception_return_pct)}
                className={pctClass(aiModel?.inception_return_pct)}
              />
              <MetricRow
                label="Alpha"
                value={fmtPct(aiModel?.latest_alpha)}
                className={pctClass(aiModel?.latest_alpha)}
              />
            </div>
          )}
          <p className="text-[11px] font-medium text-gray-600 mt-3">
            Historical Attribution — {windowDays}D window
          </p>
          <div className="mt-1 space-y-2">
            <MetricRow
              label="Drawdown"
              value={fmtPct(aiWindowDrawdown)}
              className="text-red-600"
            />
            <MetricRow
              label="Divergence vs Actual"
              value={fmtPct(aiDivergence)}
              className={pctClass(aiDivergence)}
            />
          </div>
        </div>
      </div>
    </section>
  );
}
