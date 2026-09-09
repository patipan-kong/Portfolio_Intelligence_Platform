import assert from "node:assert/strict";
import { test } from "node:test";

import { selectActiveGoalSummaries } from "./periodicReview.ts";
import type { FactualReviewResponse, GoalContextGoal, WealthGoal } from "@/lib/api";

function contextGoal(overrides: Partial<GoalContextGoal> & { id: number; name: string }): GoalContextGoal {
  return {
    goal_type: "OTHER",
    target_amount: 100000,
    currency: "THB",
    target_date: null,
    priority: "MEDIUM",
    is_archived: false,
    updated_at: "2026-08-30T00:00:00Z",
    allocations: [],
    designated_total: 0,
    progress_ratio: 0,
    progress_percent: 0,
    funding_gap: 100000,
    fully_designated: false,
    ...overrides,
  };
}

function wealthGoal(overrides: Partial<WealthGoal> & { id: number; name: string }): WealthGoal {
  return {
    workspace_id: 1,
    goal_type: "OTHER",
    target_amount: 100000,
    currency: "THB",
    target_date: null,
    priority: "MEDIUM",
    note: null,
    is_archived: false,
    created_at: "2026-08-30T00:00:00Z",
    updated_at: "2026-08-30T00:00:00Z",
    ...overrides,
  };
}

function review(goals: GoalContextGoal[]): FactualReviewResponse {
  return {
    contract_version: "wealth.factual-review.v1",
    review_generated_at: "2026-08-30T00:00:00Z",
    scope: { kind: "WORKSPACE", include_archived: true },
    goal_context: {
      contract_version: "wealth.goal-context.v1",
      context_generated_at: "2026-08-30T00:00:00Z",
      completeness: "COMPLETE",
      scope: { kind: "WORKSPACE", include_archived: true },
      goals,
      designation_by_source: [],
    },
    valuation_completeness: "COMPLETE",
    sources: [],
  };
}

test("active goal is included, archived goal is excluded", () => {
  const active = contextGoal({ id: 1, name: "Retirement", is_archived: false });
  const archived = contextGoal({ id: 2, name: "Old car", is_archived: true });
  const goals = [wealthGoal({ id: 1, name: "Retirement" }), wealthGoal({ id: 2, name: "Old car", is_archived: true })];

  const result = selectActiveGoalSummaries(goals, review([active, archived]));

  assert.notEqual(result, null);
  assert.deepEqual(result!.map((g) => g.id), [1]);
});

test("sorts by name then id — presentation only, no priority meaning", () => {
  const b = contextGoal({ id: 2, name: "B goal" });
  const a1 = contextGoal({ id: 3, name: "A goal" });
  const a2 = contextGoal({ id: 1, name: "A goal" });
  const goals = [
    wealthGoal({ id: 2, name: "B goal" }),
    wealthGoal({ id: 3, name: "A goal" }),
    wealthGoal({ id: 1, name: "A goal" }),
  ];

  const result = selectActiveGoalSummaries(goals, review([b, a1, a2]));

  assert.deepEqual(result!.map((g) => g.id), [1, 3, 2]);
});

test("goal count mismatch between records and Goal Context is treated as incoherent (null)", () => {
  const goals = [wealthGoal({ id: 1, name: "Retirement" }), wealthGoal({ id: 2, name: "House" })];
  const result = selectActiveGoalSummaries(goals, review([contextGoal({ id: 1, name: "Retirement" })]));
  assert.equal(result, null);
});

test("non-WORKSPACE or partial-archive scope is treated as incoherent (null)", () => {
  const goals = [wealthGoal({ id: 1, name: "Retirement" })];
  const goalContext = [contextGoal({ id: 1, name: "Retirement" })];
  const scoped = review(goalContext);
  scoped.scope = { kind: "GOAL", goal_id: 1 };
  assert.equal(selectActiveGoalSummaries(goals, scoped), null);
});

test("empty active-goal workspace returns an empty array, not null", () => {
  const archived = contextGoal({ id: 1, name: "Old goal", is_archived: true });
  const goals = [wealthGoal({ id: 1, name: "Old goal", is_archived: true })];
  const result = selectActiveGoalSummaries(goals, review([archived]));
  assert.deepEqual(result, []);
});
