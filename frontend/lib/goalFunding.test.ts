import assert from "node:assert/strict";
import { test } from "node:test";

import {
  aggregateDesignatedBySource,
  computeGoalFunding,
  computeSourceFundingHealth,
  sourceKey,
} from "./goalFunding.ts";
import type { GoalFundingAllocation } from "@/lib/api";

function allocation(overrides: Partial<GoalFundingAllocation> & { id: number; wealth_goal_id: number; allocated_amount: number }): GoalFundingAllocation {
  return {
    workspace_id: 1,
    source_kind: "CASH_ACCOUNT",
    cash_account_id: 1,
    portfolio_id: null,
    source_name: "Source",
    source_is_archived: false,
    currency: "THB",
    created_at: "2026-01-01T00:00:00",
    updated_at: "2026-01-01T00:00:00",
    ...overrides,
  };
}

// ─── computeGoalFunding ─────────────────────────────────────────────────────

test("no allocations (successfully loaded, empty) => 0 designated, 0% progress, full gap", () => {
  const result = computeGoalFunding(500_000, []);
  assert.equal(result.designatedFunding, 0);
  assert.equal(result.progressPercent, 0);
  assert.equal(result.fundingGap, 500_000);
  assert.equal(result.fullyDesignated, false);
});

test("one allocation", () => {
  const result = computeGoalFunding(500_000, [allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 100_000 })]);
  assert.equal(result.designatedFunding, 100_000);
  assert.equal(result.progressPercent, 20);
  assert.equal(result.fundingGap, 400_000);
});

test("multiple allocations sum", () => {
  const result = computeGoalFunding(500_000, [
    allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 100_000 }),
    allocation({ id: 2, wealth_goal_id: 1, allocated_amount: 150_000 }),
  ]);
  assert.equal(result.designatedFunding, 250_000);
  assert.equal(result.progressPercent, 50);
});

test("Cash + Portfolio allocations both count toward designated funding", () => {
  const result = computeGoalFunding(1_000_000, [
    allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 300_000, source_kind: "CASH_ACCOUNT", cash_account_id: 5, portfolio_id: null }),
    allocation({ id: 2, wealth_goal_id: 1, allocated_amount: 500_000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 9 }),
  ]);
  assert.equal(result.designatedFunding, 800_000);
  assert.equal(result.progressPercent, 80);
});

test("exactly 100% progress", () => {
  const result = computeGoalFunding(500_000, [allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 500_000 })]);
  assert.equal(result.progressPercent, 100);
  assert.equal(result.fundingGap, 0);
  assert.equal(result.fullyDesignated, true);
});

test("over 100% progress remains over 100%, not clamped", () => {
  const result = computeGoalFunding(500_000, [allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 600_000 })]);
  assert.equal(result.progressPercent, 120);
});

test("funding gap floors at zero when over-designated", () => {
  const result = computeGoalFunding(500_000, [allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 600_000 })]);
  assert.equal(result.fundingGap, 0);
});

test("failed allocation evidence => unavailable, not zero", () => {
  const result = computeGoalFunding(500_000, null);
  assert.equal(result.designatedFunding, null);
  assert.equal(result.progressPercent, null);
  assert.equal(result.fundingGap, null);
  assert.equal(result.fullyDesignated, null);
});

test("one source funding multiple goals: each goal's progress uses only its own allocation", () => {
  const houseFunding = computeGoalFunding(1_000_000, [allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 600_000, cash_account_id: 5 })]);
  const retirementFunding = computeGoalFunding(2_000_000, [allocation({ id: 2, wealth_goal_id: 2, allocated_amount: 500_000, cash_account_id: 5 })]);
  assert.equal(houseFunding.designatedFunding, 600_000);
  assert.equal(retirementFunding.designatedFunding, 500_000);
});

test("a source's over-allocation does not alter either goal's progress", () => {
  // Same Cash Account (id 5) funds both goals; combined 1,100,000 designated
  // exceeds any plausible balance, but each goal's progress is computed only
  // from its own allocation evidence, independent of the source's capacity.
  const house = allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 600_000, cash_account_id: 5 });
  const retirement = allocation({ id: 2, wealth_goal_id: 2, allocated_amount: 500_000, cash_account_id: 5 });

  const houseFunding = computeGoalFunding(1_000_000, [house]);
  const retirementFunding = computeGoalFunding(2_000_000, [retirement]);
  assert.equal(houseFunding.designatedFunding, 600_000);
  assert.equal(houseFunding.progressPercent, 60);
  assert.equal(retirementFunding.designatedFunding, 500_000);
  assert.equal(retirementFunding.progressPercent, 25);

  const health = computeSourceFundingHealth(
    aggregateDesignatedBySource([house, retirement]).get(sourceKey("CASH_ACCOUNT", 5)) ?? 0,
    1_000_000
  );
  assert.equal(health.status, "OVER_ALLOCATED");
  assert.equal(health.shortfall, 100_000);
  // The over-allocation fact above changed nothing about houseFunding/retirementFunding computed earlier.
  assert.equal(houseFunding.progressPercent, 60);
  assert.equal(retirementFunding.progressPercent, 25);
});

test("archived source allocation remains counted in Goal Progress", () => {
  const result = computeGoalFunding(500_000, [allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 300_000, source_is_archived: true })]);
  assert.equal(result.designatedFunding, 300_000);
});

// ─── aggregateDesignatedBySource ────────────────────────────────────────────

test("aggregateDesignatedBySource sums multiple goals funded by one source", () => {
  const totals = aggregateDesignatedBySource([
    allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 600_000, cash_account_id: 5 }),
    allocation({ id: 2, wealth_goal_id: 2, allocated_amount: 500_000, cash_account_id: 5 }),
  ]);
  assert.equal(totals.get(sourceKey("CASH_ACCOUNT", 5)), 1_100_000);
});

test("aggregateDesignatedBySource keeps Cash and Portfolio totals separate", () => {
  const totals = aggregateDesignatedBySource([
    allocation({ id: 1, wealth_goal_id: 1, allocated_amount: 100_000, source_kind: "CASH_ACCOUNT", cash_account_id: 5, portfolio_id: null }),
    allocation({ id: 2, wealth_goal_id: 1, allocated_amount: 200_000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 5 }),
  ]);
  assert.equal(totals.get(sourceKey("CASH_ACCOUNT", 5)), 100_000);
  assert.equal(totals.get(sourceKey("PORTFOLIO", 5)), 200_000);
});

// ─── computeSourceFundingHealth ─────────────────────────────────────────────

test("source exactly supported (designated equals current value)", () => {
  const health = computeSourceFundingHealth(300_000, 300_000);
  assert.equal(health.status, "SUPPORTED");
  assert.equal(health.shortfall, null);
});

test("source under capacity", () => {
  const health = computeSourceFundingHealth(300_000, 450_000);
  assert.equal(health.status, "SUPPORTED");
});

test("source over-allocated reports shortfall", () => {
  const health = computeSourceFundingHealth(800_000, 650_000);
  assert.equal(health.status, "OVER_ALLOCATED");
  assert.equal(health.shortfall, 150_000);
});

test("source with zero current value: zero designated is supported, positive designated is over-allocated", () => {
  assert.equal(computeSourceFundingHealth(0, 0).status, "SUPPORTED");
  assert.equal(computeSourceFundingHealth(1, 0).status, "OVER_ALLOCATED");
});

test("source capacity unavailable (null) never presented as zero", () => {
  const health = computeSourceFundingHealth(300_000, null);
  assert.equal(health.status, "UNAVAILABLE");
  assert.equal(health.currentValue, null);
  assert.equal(health.shortfall, null);
});

test("invalid/non-finite current value fails honestly as unavailable", () => {
  assert.equal(computeSourceFundingHealth(300_000, NaN).status, "UNAVAILABLE");
  assert.equal(computeSourceFundingHealth(300_000, Infinity).status, "UNAVAILABLE");
});

test("negative current value fails honestly as unavailable", () => {
  const health = computeSourceFundingHealth(300_000, -100);
  assert.equal(health.status, "UNAVAILABLE");
});
