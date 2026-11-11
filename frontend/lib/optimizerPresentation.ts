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

const REGIME_SENTENCES: Record<string, string> = {
  HIGH_VOLATILITY: "Market volatility is high.",
  RISK_OFF: "Markets are in a risk-off phase.",
  DEFENSIVE_REGIME: "Market conditions are defensive.",
  TRANSITION_RISK_OFF: "Markets are shifting toward risk-off.",
  TRANSITION_RISK_ON: "Markets are shifting toward risk-on.",
  RISK_ON: "Markets are in a risk-on phase.",
  SIDEWAYS: "Markets are moving sideways.",
};

const UNCERTAINTY_LABELS: Record<string, string> = {
  NO_ELIGIBLE_ACTION: "No alternative action had enough verified evidence.",
  AUDITOR_UNAVAILABLE: "Auditor review was unavailable.",
  AUDITOR_REVIEWS_MISSING: "Auditor review was incomplete.",
  INCOMPLETE_AUDITOR_COVERAGE: "Auditor review was incomplete.",
  MATERIAL_CONFLICT_UNRESOLVED: "A material conflict in the evidence was not resolved.",
  CURRENT_NAV_UNAVAILABLE: "Current portfolio value was unavailable.",
  CURRENT_CASH_UNAVAILABLE: "Current cash balance was unavailable.",
  MODEL_SCORE_ONLY_SUPPORT: "Support rests on model scores only.",
  INDEPENDENT_SUPPORT_UNVERIFIED: "Independent support was not verified.",
  BUY_SUPPORT_UNVERIFIED: "Support for buying was not verified.",
  UNVERIFIED_SELL: "Support for selling was not verified.",
  ADVISORY_ONLY_OR_UNVERIFIED: "Some evidence is advisory only or unverified.",
};

const humanize = (code: string) => {
  const text = code.toLowerCase().replace(/_/g, " ");
  return text.charAt(0).toUpperCase() + text.slice(1);
};
const uncertaintyText = (item: unknown): string | null => {
  if (typeof item !== "string" || !item.trim()) return null;
  if (UNCERTAINTY_LABELS[item]) return UNCERTAINTY_LABELS[item];
  return /^[A-Z0-9_]+$/.test(item) ? `${humanize(item)}.` : item;
};

type CommitteeView = ReturnType<typeof committeeDecisionPresentation>;

/** Plain-language summary derived only from existing run data. Presentation only. */
export function committeeSummaryPresentation(result: OptimizerResult, view: CommitteeView) {
  const regime = result.market_regime?.regime;
  const regimeSentence = typeof regime === "string" ? REGIME_SENTENCES[regime] ?? null : null;
  const join = (...parts: (string | null)[]) => parts.filter(Boolean).join(" ");
  if (view.owner !== "Committee" || view.unavailable || !view.selection) {
    return { headline: "Recommendation Unavailable", showHoldings: false,
      explanation: "The Committee's selection evidence is missing or could not be validated, so no strategy decision is shown. The legacy consensus assessment is not a substitute for it.",
      cautions: ["Missing evidence does not mean low risk."] };
  }
  const { selection, candidate } = view;
  const cautions = [...new Set((selection.material_uncertainty ?? []).map(uncertaintyText)
    .filter((item): item is string => item != null))];
  if (selection.state === "ABSTAINED") return { cautions, showHoldings: false, headline: "No Recommendation",
    explanation: join("The Committee abstained, so no strategy was selected or approved.", regimeSentence) };
  if (selection.state === "HUMAN_REVIEW_REQUIRED") return { cautions, showHoldings: false, headline: "Human Review Required",
    explanation: join("The evidence does not support an automatic recommendation. No strategy is approved for action.", regimeSentence) };
  if (view.altered) cautions.push("Safeguards changed the selected plan; see technical details for the effective allocation.");
  if (candidate?.id === "hold-current") {
    const weakEvidence = selection.reason_codes?.includes("CAUTIONED_HOLD")
      || selection.material_uncertainty?.includes("NO_ELIGIBLE_ACTION");
    cautions.push("Holding is a cautious default, not a guarantee that it is the best outcome.");
    return { cautions, showHoldings: true, headline: "Hold Current Portfolio",
      explanation: join("Keep the current portfolio unchanged.", regimeSentence,
        weakEvidence ? "The available evidence does not establish that rebalancing would be better." : null) };
  }
  return { cautions, showHoldings: true, headline: candidate ? humanize(candidate.family) : "Selected strategy",
    explanation: join("The Committee selected this plan over holding the current portfolio.", regimeSentence,
      "This is a recommendation, not a recorded transaction.") };
}
