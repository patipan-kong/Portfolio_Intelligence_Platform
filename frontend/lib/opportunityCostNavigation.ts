// RAE-01 — the opportunity-cost ledger is the authority for these decision
// types (backend/services/evaluation/opportunity_cost.py::_DIVERGENT_DECISIONS).
// This is navigation only: it does not assert that a row is present or graded.
const OPPORTUNITY_COST_DECISIONS = new Set([
  "REJECTED",
  "PARTIAL_EXECUTION",
  "MANUAL_OVERRIDE",
  "EXPIRED",
]);

export const OPPORTUNITY_COST_TARGET_PERIOD_DAYS = 365;

export function isOpportunityCostEligibleDecision(decision: string): boolean {
  return OPPORTUNITY_COST_DECISIONS.has(decision);
}

export function opportunityCostHref(decisionId: number): string {
  return `/ai-analytics/opportunity-cost?decisionId=${decisionId}`;
}

export function parseOpportunityCostDecisionId(value: string | null): number | null {
  if (value == null || !/^\d+$/.test(value)) return null;
  const decisionId = Number(value);
  return Number.isSafeInteger(decisionId) && decisionId > 0 ? decisionId : null;
}
