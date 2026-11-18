// Phase 4.23 — pure display helpers for the Shadow Performance panels.
// Missing evidence (null/undefined) is never rendered as a number; a genuine
// 0 is.
import type { PortfolioAttributionResult } from "@/lib/api";

/** Plausibility clamp: suppresses corrupted -100% / absurd values. */
export function safeReturn(v: number | null | undefined): number | null {
  if (v == null) return null;
  if (v <= -99.5 || v > 999) return null;
  return v;
}

/** "+1.23%" / "0.00%" / "-"; null/undefined → "-" (never "+0.00%"). */
export function fmtPct(v: number | null | undefined): string {
  const safe = safeReturn(v);
  if (safe == null) return "-";
  const sign = safe > 0 ? "+" : "";
  return `${sign}${safe.toFixed(2)}%`;
}

/**
 * Divergence vs Actual over the attribution window ONLY. Both operands come
 * from the same /attribution-summary payload and window, and the shadow side
 * must be proven to span that window:
 *  - static: Phase 4.22 selector reported status "selected" (edge-coverage
 *    verified against the same window);
 *  - ACTIVE_MODEL: the backend's ai_model_shadow_coverage reports its
 *    valuations cover both the owner's first and last in-window snapshot
 *    (inception <= period_start alone does not prove that).
 * Otherwise null — never a since-inception vs windowed subtraction.
 */
export function windowedDivergence(
  current: PortfolioAttributionResult | null | undefined,
  which: "static" | "ai",
  aiInceptionDate?: string | null,
): number | null {
  if (!current) return null;
  const actual = safeReturn(current.actual?.return_pct);
  if (actual == null) return null;
  let shadowReturn: number | null | undefined;
  if (which === "static") {
    if (current.static_shadow_selection?.status !== "selected") return null;
    shadowReturn = current.static_shadow?.return_pct;
  } else {
    if (!aiInceptionDate || aiInceptionDate > current.period_start) return null;
    if (current.ai_model_shadow_coverage?.window_covered !== true) return null;
    shadowReturn = current.ai_model_shadow?.return_pct;
  }
  const sr = safeReturn(shadowReturn);
  return sr == null ? null : sr - actual;
}
