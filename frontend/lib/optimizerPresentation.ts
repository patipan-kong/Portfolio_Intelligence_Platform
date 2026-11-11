import type { OptimizerResult, ActivePolicy, StrategySelection, StrategicCandidateEnvelope, CandidateAudit, TargetAllocation } from "./api";
import { deriveExecutionPlan, NO_ACTION_REASON_LABELS } from "./executionPlan";

export const SECTOR_POLICY_ADVISORY = "wealth.optimizer-sector-advisory.v1";
export const OPTIMIZER_POLICY_MUJI_V2 = "wealth.optimizer-muji.v2";
export const STRATEGY_SELECTION_V1 = "wealth.strategy-selection.v1";

export function committeeDecisionPresentation(input: {
  active_policy?: Pick<ActivePolicy, "optimizer_policy_mode" | "strategy_selection_mode"> | null;
  strategy_selection?: StrategySelection | null;
  strategic_candidates?: StrategicCandidateEnvelope | null;
  candidate_audit?: CandidateAudit | null;
  target_allocations?: TargetAllocation[] | null;
}) {
  const policy = input.active_policy;
  if (policy?.optimizer_policy_mode !== OPTIMIZER_POLICY_MUJI_V2 ||
      policy?.strategy_selection_mode !== STRATEGY_SELECTION_V1) return { owner: "Challenger" as const };
  const selection = input.strategy_selection;
  const envelope = input.strategic_candidates;
  if (!selection || selection.version !== STRATEGY_SELECTION_V1 ||
      !["SELECTED", "ABSTAINED", "HUMAN_REVIEW_REQUIRED"].includes(selection.state) ||
      !Array.isArray(selection.reason_codes) || !Array.isArray(selection.material_uncertainty) ||
      !Array.isArray(selection.supporting_evidence_refs ?? []) ||
      !Array.isArray(selection.opposing_evidence_refs ?? []) ||
      !envelope || envelope.version !== "wealth.strategic-candidates.v1" ||
      envelope.status !== "PREPARED_NOT_SELECTED" || !Array.isArray(envelope.candidates) ||
      !envelope.candidates.every((item) => item && typeof item.id === "string")) {
    return { owner: "Committee" as const, unavailable: true };
  }
  const candidate = selection.state === "SELECTED"
    ? envelope.candidates.find((item) => item.id === selection.selected_candidate_id) : undefined;
  if (selection.state === "SELECTED" && (!candidate || candidate.eligibility_status !== "ELIGIBLE" ||
      typeof candidate.family !== "string" || !Array.isArray(candidate.proposed_allocations) ||
      !candidate.proposed_allocations.every((row) => row && typeof row.symbol === "string" &&
        typeof row.action === "string" && typeof row.target_weight === "number"))) {
    return { owner: "Committee" as const, unavailable: true };
  }
  const catalog = envelope.observed_evidence_catalog ?? {};
  const support = (selection.supporting_evidence_refs ?? []).map((ref) => ({
    ref, value: candidate?.observed_evidence_refs?.[ref],
  }));
  const opposition = (selection.opposing_evidence_refs ?? []).map((ref) => ({ ref, value: catalog[ref] }));
  const reviewed = candidate && input.candidate_audit?.reviews?.[candidate.id];
  const cautionedHold = candidate?.id === "hold-current" && selection.reason_codes.includes("CAUTIONED_HOLD");
  const refsValid = [...support, ...opposition].every((item) =>
    typeof item.ref === "string" && item.value !== undefined) &&
    (candidate?.id === "hold-current" || !candidate || support.length > 0) &&
    (!candidate || cautionedHold || (input.candidate_audit?.status === "AVAILABLE" && reviewed &&
      support.every(({ ref }) => reviewed.supporting_refs?.includes(ref)) &&
      opposition.every(({ ref }) => reviewed.opposing_refs?.includes(ref))));
  if (!refsValid) {
    return { owner: "Committee" as const, unavailable: true };
  }
  return { owner: "Committee" as const, selection, candidate, support, opposition,
    effective: input.target_allocations, altered: selection.downstream_outcome?.status === "ALTERED_BY_SAFEGUARDS" };
}

export function assessment(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

// Availability only: scheduling and trade classification stay owned by the
// backend. Never turn an absent/partial summary into a confirmed empty plan.
export function executionEvidenceAvailable(result: OptimizerResult): boolean {
  if (result.execution_policy_evidence_status === "unsupported_optimizer_policy_evidence") return false;
  if (result.active_policy?.optimizer_policy_mode === OPTIMIZER_POLICY_MUJI_V2 &&
      (result.execution_optimization?.scheduled_changes == null ||
       result.execution_optimization?.estimated_trade_costs == null ||
       result.execution_optimization?.scheduled_buys == null)) return false;
  if (result.active_policy?.sector_policy_mode === SECTOR_POLICY_ADVISORY
      && result.execution_optimization?.scheduled_buys == null) return false;
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
