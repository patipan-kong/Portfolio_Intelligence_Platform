import assert from "node:assert/strict";
import test from "node:test";
import type {
  FactualReviewSource,
  GoalContextGoal,
  GoalFundingAllocationHistory,
  GoalPlanAmendmentHistory,
} from "./api.ts";
import type { GoalAffordabilityResult } from "./goalAffordability.ts";
import { deriveGoalReviewCues, type GoalReviewCuesInput } from "./goalReviewCues.ts";

const context = (overrides: Partial<GoalContextGoal> = {}): GoalContextGoal => ({
  id: 1,
  name: "Home",
  goal_type: "HOUSE",
  target_amount: 1_000,
  currency: "THB",
  target_date: "2030-01-01",
  priority: "HIGH",
  is_archived: false,
  updated_at: "2026-09-04T00:00:00Z",
  allocations: [],
  designated_total: 1_000,
  progress_ratio: 1,
  progress_percent: 100,
  funding_gap: 0,
  fully_designated: true,
  ...overrides,
});

const source = (overrides: Partial<FactualReviewSource> = {}): FactualReviewSource => ({
  source_kind: "CASH_ACCOUNT",
  source_id: 5,
  source_name: "Savings",
  source_is_archived: false,
  currency: "THB",
  designated_total_in_context_scope: 1_000,
  valuation: {
    availability: "AVAILABLE",
    observed_value: 1_000,
    as_of: "2001-01-01T00:00:00Z",
    provenance: "CASH_ACCOUNT_CURRENT_BALANCE",
    quality: "COMPLETE",
  },
  designation_coverage: { status: "SUPPORTED", shortfall: 0 },
  ...overrides,
});

const affordability = (overrides: Partial<GoalAffordabilityResult> = {}): GoalAffordabilityResult => ({
  state: "AFFORDABLE",
  requiredMonthlyContribution: 100,
  observedMonthlySurplus: 200,
  affordabilityGap: 100,
  evidenceMonthCount: 3,
  evidenceMonths: ["2026-06", "2026-07", "2026-08"],
  reason: null,
  reasonCode: null,
  ...overrides,
});

const planEvent = (recorded_at = "2026-09-04T10:00:00Z"): GoalPlanAmendmentHistory => ({
  id: 1,
  workspace_id: 1,
  wealth_goal_id: 1,
  previous_target_amount: 900,
  resulting_target_amount: 1_000,
  previous_target_date: "2029-01-01",
  resulting_target_date: "2030-01-01",
  previous_priority: "MEDIUM",
  resulting_priority: "HIGH",
  recorded_at,
});

const fundingEvent = (recorded_at = "2026-09-04T10:00:00Z"): GoalFundingAllocationHistory => ({
  id: 2,
  workspace_id: 1,
  wealth_goal_id: 1,
  source_kind: "CASH_ACCOUNT",
  source_id: 5,
  source_name: "Savings",
  action: "UPDATE",
  previous_designated_amount: 900,
  resulting_designated_amount: 1_000,
  currency: "THB",
  recorded_at,
});

const input = (overrides: Partial<GoalReviewCuesInput> = {}): GoalReviewCuesInput => ({
  goalContext: context(),
  factualSources: [source()],
  affordability: affordability(),
  planHistory: [],
  fundingHistory: [],
  ...overrides,
});

const kinds = (value: GoalReviewCuesInput) => deriveGoalReviewCues(value).cues.map((cue) => cue.kind);

test("designation gap uses the accepted context gap and disappears when current context closes it", () => {
  const result = deriveGoalReviewCues(input({
    goalContext: context({ designated_total: 400, funding_gap: 123, progress_ratio: 0.4, progress_percent: 40, fully_designated: false }),
  }));
  assert.deepEqual(kinds(input()), []);
  assert.deepEqual(result.cues, [{ kind: "DESIGNATION_GAP", href: "#funding-heading", amount: 123 }]);
});

test("missing or failed designation evidence never becomes a designation assertion", () => {
  const result = deriveGoalReviewCues(input({ goalContext: { error: "Goal Context unavailable" } }));
  assert.equal(result.hasUnavailableEvidence, true);
  assert.equal(result.eligibility.designationGap, "UNAVAILABLE");
  assert.deepEqual(result.cues, []);
});

test("target-date cue is factual and does not invent another planning input", () => {
  assert.deepEqual(kinds(input({ goalContext: context({ target_date: null }) })), ["TARGET_DATE_MISSING"]);
  assert.deepEqual(kinds(input()), []);
});

test("accepted source states produce only their corresponding evidence cues", () => {
  assert.deepEqual(kinds(input({ factualSources: [source({ designation_coverage: { status: "OVER_ALLOCATED", shortfall: 200 } })] })), ["SOURCE_OVER_ALLOCATED"]);
  assert.deepEqual(kinds(input({ factualSources: [source({ valuation: { availability: "UNAVAILABLE", observed_value: null, as_of: null, provenance: null, quality: null }, designation_coverage: { status: "UNAVAILABLE", shortfall: null } })] })), ["SOURCE_VALUE_UNAVAILABLE"]);
  assert.deepEqual(kinds(input({ factualSources: [source({ valuation: { ...source().valuation, quality: "PARTIAL" }, designation_coverage: { status: "UNAVAILABLE", shortfall: null } })] })), ["SOURCE_EVIDENCE_INCOMPLETE"]);
  assert.deepEqual(kinds(input({ factualSources: [source({ source_is_archived: true })] })), ["SOURCE_ARCHIVED"]);
});

test("old valid as-of evidence is not reclassified as stale", () => {
  const result = deriveGoalReviewCues(input({ factualSources: [source()] }));
  assert.deepEqual(result.cues, []);
  assert.equal(result.hasUnavailableEvidence, false);
});

test("affordability reuses accepted negative states and never creates a verdict from success or failure", () => {
  assert.deepEqual(kinds(input({ affordability: affordability({ state: "SHORTFALL", observedMonthlySurplus: 0, affordabilityGap: -100 }) })), ["AFFORDABILITY_SHORTFALL"]);
  assert.deepEqual(kinds(input({ affordability: affordability({ state: "INSUFFICIENT_DATA", requiredMonthlyContribution: null, observedMonthlySurplus: null, affordabilityGap: null, reason: "Cash Flow data could not be fully loaded. Try again.", reasonCode: "CASH_FLOW_UNAVAILABLE" }) })), ["AFFORDABILITY_INSUFFICIENT_DATA"]);
  const failed = deriveGoalReviewCues(input({ affordability: { error: "cash flow unavailable" } }));
  assert.deepEqual(failed.cues, []);
  assert.equal(failed.hasUnavailableEvidence, true);
});

test("required-side invalidity is not mislabeled as insufficient cash-flow evidence", () => {
  const result = deriveGoalReviewCues(input({
    affordability: affordability({
      state: "INSUFFICIENT_DATA",
      requiredMonthlyContribution: null,
      observedMonthlySurplus: null,
      affordabilityGap: null,
      reason: "Target date is in the past.",
      reasonCode: "REQUIRED_SIDE_INVALID",
    }),
  }));
  assert.deepEqual(result.cues, []);
  assert.equal(result.eligibility.affordability, "ABSENT");
});

test("newest accepted history record is documentary context; unavailable history is not empty history", () => {
  const result = deriveGoalReviewCues(input({
    planHistory: [planEvent("2026-09-04T12:00:00Z"), planEvent("2026-09-04T10:00:00Z")],
    fundingHistory: [fundingEvent("2026-09-04T11:00:00Z")],
  }));
  assert.deepEqual(result.cues, [
    { kind: "PLAN_AMENDMENT", href: "#plan-history-heading", recordedAt: "2026-09-04T12:00:00Z" },
    { kind: "FUNDING_AMENDMENT", href: "#funding-history-heading", recordedAt: "2026-09-04T11:00:00Z" },
  ]);
  const failed = deriveGoalReviewCues(input({ planHistory: { error: "history unavailable" }, fundingHistory: { error: "history unavailable" } }));
  assert.deepEqual(failed.cues, []);
  assert.equal(failed.hasUnavailableEvidence, true);
});

test("display order is fixed by page information architecture, not priority", () => {
  const common = {
    goalContext: context({ target_date: null, designated_total: 100, funding_gap: 900, progress_ratio: 0.1, progress_percent: 10, fully_designated: false }),
    factualSources: [source({ source_is_archived: true, designation_coverage: { status: "OVER_ALLOCATED", shortfall: 100 } })],
    affordability: affordability({ state: "SHORTFALL", observedMonthlySurplus: 0, affordabilityGap: -100 }),
    planHistory: [planEvent()],
    fundingHistory: [fundingEvent()],
  } satisfies Partial<GoalReviewCuesInput>;
  const high = kinds(input({ ...common, goalContext: context({ ...common.goalContext, priority: "HIGH" }) }));
  const low = kinds(input({ ...common, goalContext: context({ ...common.goalContext, priority: "LOW" }) }));
  assert.deepEqual(high, ["TARGET_DATE_MISSING", "DESIGNATION_GAP", "SOURCE_ARCHIVED", "SOURCE_OVER_ALLOCATED", "AFFORDABILITY_SHORTFALL", "PLAN_AMENDMENT", "FUNDING_AMENDMENT"]);
  assert.deepEqual(low, high);
});
