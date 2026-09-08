import assert from "node:assert/strict";
import { test } from "node:test";

import {
  buildSourceFundingOverview,
  factualReviewMatchesGoalContext,
  sourceDrillThroughHref,
  sourceFundingHealth,
  sourceKey,
} from "./goalFunding.ts";
import type {
  FactualReviewResponse,
  FactualReviewSource,
  GoalContextAllocation,
  GoalContextGoal,
  GoalContextResponse,
} from "@/lib/api";

function source(kind: "CASH_ACCOUNT" | "PORTFOLIO", id: number, overrides: Partial<FactualReviewSource> = {}): FactualReviewSource {
  return {
    source_kind: kind,
    source_id: id,
    source_name: `${kind} ${id}`,
    source_is_archived: false,
    currency: "THB",
    designated_total_in_context_scope: 700,
    valuation: {
      availability: "AVAILABLE",
      observed_value: 123,
      as_of: "2026-08-30",
      provenance: kind === "CASH_ACCOUNT" ? "CASH_ACCOUNT_CURRENT_BALANCE" : "PORTFOLIO_SNAPSHOT",
      quality: "COMPLETE",
    },
    designation_coverage: { status: "SUPPORTED", shortfall: 999 },
    ...overrides,
  };
}

function allocation(
  goalId: number,
  kind: "CASH_ACCOUNT" | "PORTFOLIO",
  sourceId: number,
  amount: number,
  overrides: Partial<GoalContextAllocation> = {}
): GoalContextAllocation {
  return {
    id: goalId * 1000 + sourceId,
    wealth_goal_id: goalId,
    source_kind: kind,
    source_id: sourceId,
    source_name: `${kind} ${sourceId}`,
    source_is_archived: false,
    designated_amount: amount,
    currency: "THB",
    updated_at: "2026-08-30T00:00:00Z",
    ...overrides,
  };
}

function goal(
  id: number,
  name: string,
  allocations: GoalContextAllocation[],
  overrides: Partial<GoalContextGoal> = {}
): GoalContextGoal {
  const designated_total = allocations.reduce((sum, item) => sum + item.designated_amount, 0);
  return {
    id,
    name,
    goal_type: "OTHER",
    target_amount: 1000,
    currency: "THB",
    target_date: null,
    priority: "MEDIUM",
    is_archived: false,
    updated_at: "2026-08-30T00:00:00Z",
    allocations,
    designated_total,
    progress_ratio: designated_total / 1000,
    progress_percent: (designated_total / 1000) * 100,
    funding_gap: Math.max(1000 - designated_total, 0),
    fully_designated: designated_total >= 1000,
    ...overrides,
  };
}

function review(sources: FactualReviewSource[]): FactualReviewResponse {
  const designation_by_source = sources.map(({ valuation: _valuation, designation_coverage: _coverage, ...designation }) => designation);
  const goal_context: GoalContextResponse = {
    contract_version: "wealth.goal-context.v1",
    context_generated_at: "2026-08-30T00:00:00Z",
    completeness: "COMPLETE",
    scope: { kind: "WORKSPACE", include_archived: true },
    goals: [],
    designation_by_source,
  };
  return {
    contract_version: "wealth.factual-review.v1",
    review_generated_at: "2026-08-30T00:00:00Z",
    scope: goal_context.scope,
    goal_context,
    valuation_completeness: "COMPLETE",
    sources,
  };
}

test("typed source identity keeps Cash Account and Portfolio ids distinct", () => {
  assert.notEqual(sourceKey("CASH_ACCOUNT", 1), sourceKey("PORTFOLIO", 1));
  assert.equal(buildSourceFundingOverview([source("CASH_ACCOUNT", 1), source("PORTFOLIO", 1)]).length, 2);
});

test("Funding Health facts are copied from the server without recomputation", () => {
  const server = source("CASH_ACCOUNT", 1);
  const health = sourceFundingHealth(server);
  assert.deepEqual(health, {
    totalDesignated: 700,
    currentValue: 123,
    status: "SUPPORTED",
    shortfall: 999,
    asOf: "2026-08-30",
    provenance: "CASH_ACCOUNT_CURRENT_BALANCE",
    quality: "COMPLETE",
  });
});

test("UNAVAILABLE preserves a nonzero observed partial value and null shortfall", () => {
  const health = sourceFundingHealth(source("PORTFOLIO", 2, {
    valuation: { availability: "AVAILABLE", observed_value: 42, as_of: "2020-01-01", provenance: "PORTFOLIO_SNAPSHOT", quality: "PARTIAL" },
    designation_coverage: { status: "UNAVAILABLE", shortfall: null },
  }));
  assert.equal(health.currentValue, 42);
  assert.equal(health.status, "UNAVAILABLE");
  assert.equal(health.shortfall, null);
});

test("overview sorting and archived metadata are presentation-only", () => {
  const rows = buildSourceFundingOverview([
    source("CASH_ACCOUNT", 9, { source_name: "Zeta", source_is_archived: true }),
    source("CASH_ACCOUNT", 3, { source_name: "Alpha" }),
  ]);
  assert.deepEqual(rows.map((row) => row.sourceName), ["Alpha", "Zeta"]);
  assert.equal(rows[1].sourceIsArchived, true);
});

test("review and embedded Goal Context source facts must match exactly", () => {
  const valid = review([source("CASH_ACCOUNT", 1), source("PORTFOLIO", 1)]);
  assert.equal(factualReviewMatchesGoalContext(valid), true);
  valid.sources[0].designated_total_in_context_scope += 1;
  assert.equal(factualReviewMatchesGoalContext(valid), false);
});

test("review and embedded Goal Context scopes must match", () => {
  const value = review([]);
  value.scope = { kind: "WORKSPACE", include_archived: false };
  assert.equal(factualReviewMatchesGoalContext(value), false);
});

test("sourceDrillThroughHref preserves the exact source kind and id — never inferred from name or position", () => {
  assert.equal(sourceDrillThroughHref("CASH_ACCOUNT", 5), "/cash?account=5");
  assert.equal(sourceDrillThroughHref("PORTFOLIO", 9), "/portfolio?portfolio=9");
  assert.notEqual(sourceDrillThroughHref("CASH_ACCOUNT", 5), sourceDrillThroughHref("CASH_ACCOUNT", 6));
});

// ─── Shared Funding-Source Transparency (ADR-016) ─────────────────────────

test("one source with one goal is exposed as a single shared designation", () => {
  const goals = [goal(1, "Retirement", [allocation(1, "CASH_ACCOUNT", 1, 700)])];
  const rows = buildSourceFundingOverview([source("CASH_ACCOUNT", 1)], goals);
  assert.equal(rows[0].sharedGoals.length, 1);
  assert.deepEqual(rows[0].sharedGoals[0], {
    goalId: 1,
    goalName: "Retirement",
    goalIsArchived: false,
    designatedAmount: 700,
  });
});

test("one source shared by multiple goals lists each goal's own designation", () => {
  const goals = [
    goal(1, "House", [allocation(1, "CASH_ACCOUNT", 1, 80)]),
    goal(2, "Wedding", [allocation(2, "CASH_ACCOUNT", 1, 90)]),
  ];
  const rows = buildSourceFundingOverview([source("CASH_ACCOUNT", 1)], goals);
  assert.equal(rows[0].sharedGoals.length, 2);
  assert.deepEqual(rows[0].sharedGoals.map((item) => [item.goalName, item.designatedAmount]), [
    ["House", 80],
    ["Wedding", 90],
  ]);
});

test("multiple sources each get their own independent shared-goal breakdown", () => {
  const goals = [
    goal(1, "House", [allocation(1, "CASH_ACCOUNT", 1, 50)]),
    goal(2, "Wedding", [allocation(2, "PORTFOLIO", 2, 60)]),
  ];
  const rows = buildSourceFundingOverview(
    [source("CASH_ACCOUNT", 1), source("PORTFOLIO", 2)],
    goals
  );
  const byKey = new Map(rows.map((row) => [row.key, row]));
  assert.deepEqual(byKey.get(sourceKey("CASH_ACCOUNT", 1))?.sharedGoals.map((item) => item.goalName), ["House"]);
  assert.deepEqual(byKey.get(sourceKey("PORTFOLIO", 2))?.sharedGoals.map((item) => item.goalName), ["Wedding"]);
});

test("a goal designating to two different sources appears independently under each", () => {
  const goals = [
    goal(1, "Retirement", [
      allocation(1, "CASH_ACCOUNT", 1, 40),
      allocation(1, "PORTFOLIO", 2, 60),
    ]),
  ];
  const rows = buildSourceFundingOverview(
    [source("CASH_ACCOUNT", 1), source("PORTFOLIO", 2)],
    goals
  );
  const byKey = new Map(rows.map((row) => [row.key, row]));
  assert.equal(byKey.get(sourceKey("CASH_ACCOUNT", 1))?.sharedGoals[0].designatedAmount, 40);
  assert.equal(byKey.get(sourceKey("PORTFOLIO", 2))?.sharedGoals[0].designatedAmount, 60);
});

test("source identity collision protection: same numeric id, different kind, never merges", () => {
  const goals = [
    goal(1, "Cash Goal", [allocation(1, "CASH_ACCOUNT", 1, 10)]),
    goal(2, "Portfolio Goal", [allocation(2, "PORTFOLIO", 1, 20)]),
  ];
  const rows = buildSourceFundingOverview(
    [source("CASH_ACCOUNT", 1), source("PORTFOLIO", 1)],
    goals
  );
  const byKey = new Map(rows.map((row) => [row.key, row]));
  assert.deepEqual(byKey.get(sourceKey("CASH_ACCOUNT", 1))?.sharedGoals.map((item) => item.goalName), ["Cash Goal"]);
  assert.deepEqual(byKey.get(sourceKey("PORTFOLIO", 1))?.sharedGoals.map((item) => item.goalName), ["Portfolio Goal"]);
});

test("shared-goal breakdown is ordered by goal name then id, carrying no priority meaning", () => {
  const goals = [
    goal(9, "Zeta", [allocation(9, "CASH_ACCOUNT", 1, 5)]),
    goal(2, "Alpha", [allocation(2, "CASH_ACCOUNT", 1, 5)]),
    goal(1, "Alpha", [allocation(1, "CASH_ACCOUNT", 1, 5)]),
  ];
  const rows = buildSourceFundingOverview([source("CASH_ACCOUNT", 1)], goals);
  assert.deepEqual(rows[0].sharedGoals.map((item) => item.goalId), [1, 2, 9]);
});

test("archived goals remain in the shared-goal breakdown, labeled, so the total still reconciles", () => {
  const goals = [
    goal(1, "Active Goal", [allocation(1, "CASH_ACCOUNT", 1, 30)]),
    goal(2, "Old Goal", [allocation(2, "CASH_ACCOUNT", 1, 20)], { is_archived: true }),
  ];
  const rows = buildSourceFundingOverview(
    [source("CASH_ACCOUNT", 1, { designated_total_in_context_scope: 50 })],
    goals
  );
  const shared = rows[0].sharedGoals;
  assert.equal(shared.length, 2);
  assert.equal(shared.find((item) => item.goalId === 2)?.goalIsArchived, true);
  const sum = shared.reduce((total, item) => total + item.designatedAmount, 0);
  assert.equal(sum, rows[0].health.totalDesignated);
});

test("reconciliation invariant: shared-goal amounts sum to the canonical source total", () => {
  const goals = [
    goal(1, "Goal A", [allocation(1, "CASH_ACCOUNT", 1, 80)]),
    goal(2, "Goal B", [allocation(2, "CASH_ACCOUNT", 1, 90)]),
  ];
  const rows = buildSourceFundingOverview(
    [source("CASH_ACCOUNT", 1, { designated_total_in_context_scope: 170 })],
    goals
  );
  const sum = rows[0].sharedGoals.reduce((total, item) => total + item.designatedAmount, 0);
  assert.equal(sum, 170);
  assert.equal(sum, rows[0].health.totalDesignated);
});

test("over-allocated source exposes each goal's own designation without attributing the shortfall", () => {
  const goals = [
    goal(1, "Goal A", [allocation(1, "CASH_ACCOUNT", 1, 80)]),
    goal(2, "Goal B", [allocation(2, "CASH_ACCOUNT", 1, 90)]),
  ];
  const rows = buildSourceFundingOverview(
    [
      source("CASH_ACCOUNT", 1, {
        designated_total_in_context_scope: 170,
        valuation: {
          availability: "AVAILABLE",
          observed_value: 100,
          as_of: "2026-08-30",
          provenance: "CASH_ACCOUNT_CURRENT_BALANCE",
          quality: "COMPLETE",
        },
        designation_coverage: { status: "OVER_ALLOCATED", shortfall: 70 },
      }),
    ],
    goals
  );
  const row = rows[0];
  assert.equal(row.health.status, "OVER_ALLOCATED");
  assert.equal(row.health.shortfall, 70);
  assert.equal(row.health.totalDesignated, 170);
  assert.deepEqual(row.sharedGoals.map((item) => [item.goalName, item.designatedAmount]), [
    ["Goal A", 80],
    ["Goal B", 90],
  ]);
  for (const item of row.sharedGoals) {
    assert.equal("shortfall" in item, false);
    assert.equal("shortfallShare" in item, false);
  }
});

test("UNAVAILABLE valuation still shows the shared-goal breakdown — designation is independent of valuation", () => {
  const goals = [goal(1, "Goal A", [allocation(1, "PORTFOLIO", 2, 500)])];
  const rows = buildSourceFundingOverview(
    [
      source("PORTFOLIO", 2, {
        designated_total_in_context_scope: 500,
        valuation: { availability: "UNAVAILABLE", observed_value: null, as_of: null, provenance: null, quality: null },
        designation_coverage: { status: "UNAVAILABLE", shortfall: null },
      }),
    ],
    goals
  );
  assert.equal(rows[0].health.status, "UNAVAILABLE");
  assert.deepEqual(rows[0].sharedGoals.map((item) => item.designatedAmount), [500]);
});

test("no shared allocations for a source yields an empty breakdown, not a fabricated row", () => {
  const rows = buildSourceFundingOverview([source("CASH_ACCOUNT", 1)], []);
  assert.deepEqual(rows[0].sharedGoals, []);
});

test("omitting the goals argument preserves prior call sites' behavior with an empty breakdown", () => {
  const rows = buildSourceFundingOverview([source("CASH_ACCOUNT", 1)]);
  assert.deepEqual(rows[0].sharedGoals, []);
});
