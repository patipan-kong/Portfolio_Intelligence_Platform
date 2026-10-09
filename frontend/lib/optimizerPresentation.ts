import type { OptimizerResult } from "./api";
import { deriveExecutionPlan, NO_ACTION_REASON_LABELS } from "./executionPlan";

export function assessment(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

// Availability only: scheduling and trade classification stay owned by the
// backend. Never turn an absent/partial summary into a confirmed empty plan.
export function executionEvidenceAvailable(result: OptimizerResult): boolean {
  const summary = result.action_summary;
  if (!summary || ![summary.sell, summary.reduce, summary.accumulate, summary.new_position, summary.hold]
    .every((group) => Array.isArray(group) && group.every((row) => row != null && typeof row.symbol === "string" && row.symbol.trim()))) return false;
  const symbols = [summary.sell, summary.reduce, summary.accumulate, summary.new_position, summary.hold].flat().map((row) => row.symbol);
  if (new Set(symbols).size !== symbols.length) return false;
  const sells = [...summary.sell, ...summary.reduce];
  return sells.every((row) => result.execution_optimization?.trades?.some((trade) =>
    trade.symbol === row.symbol && ["FULL", "SCALED", "DEFERRED"].includes(trade.execution_state)));
}

export function scheduledTradeCount(result: OptimizerResult): number | null {
  return executionEvidenceAvailable(result)
    ? deriveExecutionPlan(result.action_summary, result.target_allocations, result.execution_optimization).trades.length : null;
}

export function economicRecommendation(result: OptimizerResult): string {
  // Retain economic changes even when scheduling has deferred them. If the
  // response has already suppressed an action, do not reconstruct its origin.
  const allocations = result.target_allocations;
  if (!Array.isArray(allocations) || allocations.length === 0) return "Recommendation unavailable";
  if (allocations.some((a) => typeof a.symbol !== "string" || !a.symbol.trim()) || new Set(allocations.map((a) => a.symbol)).size !== allocations.length) return "Recommendation unavailable";
  if (allocations.some((a) => a.noise_suppressed)) return "Original economic recommendation unavailable — a change was suppressed";
  const actions = allocations.map((a) => ({ symbol: a.symbol, action: a.action }));
  if (actions.some((a) => !["BUY", "ACCUMULATE", "REDUCE", "SELL", "HOLD", "WATCH"].includes(a.action))) return "Recommendation unavailable";
  const changes = actions.filter((a) => !["HOLD", "WATCH"].includes(a.action));
  return changes.length ? changes.map((a) => `${a.action} ${a.symbol}`).join("; ") : "Keep held positions unchanged";
}

export function primarySchedulingReason(result: OptimizerResult): string {
  return result.stabilization?.reason || result.no_action_summary
    || (result.no_action_reason ? NO_ACTION_REASON_LABELS[result.no_action_reason] ?? result.no_action_reason : "Scheduling reason unavailable");
}

export function intentReviewSummary(result: OptimizerResult): string {
  const review = result.advisory_intent_review;
  if (!review && result.advisory_intent_review_status !== "EVIDENCE_INVALID") return "Intent review not captured";
  if (!review || result.advisory_intent_review_status === "EVIDENCE_INVALID") return "Intent review unavailable";
  const conflicts = review.positions.reduce((n, p) => n + (p.review.final.outcome === "CONFLICT" ? 1 : 0)
    + p.review.retained.filter((r) => r.review.outcome === "CONFLICT").length, 0);
  if (conflicts) return `${conflicts} proposal${conflicts === 1 ? " conflicts" : "s conflict"} with your intent — review required`;
  if (review.coverage.all_resolved_and_consistent) return "Recommendation respects your intent at run time";
  return `Intent checked for ${review.coverage.resolved_count} of ${review.coverage.referenced_positive_held_count} held positions; remaining checks unavailable`;
}
