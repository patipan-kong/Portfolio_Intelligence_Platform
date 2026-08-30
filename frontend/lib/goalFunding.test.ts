import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";

import {
  buildSourceFundingOverview,
  computeSourceFundingHealth,
  sourceKey,
  type FundingSourceKey,
} from "./goalFunding.ts";
import type { GoalContextSourceDesignation } from "@/lib/api";

type TaggedValue = number | { non_finite: "NaN" | "Infinity" | "-Infinity" };
type GoldenScalar = TaggedValue | boolean | null;
type GoldenFixture = {
  schema_version: number;
  contract_version: string;
  goal_funding_cases: Array<{
    id: string;
    target_amount: TaggedValue;
    allocations: Array<{ id: number; source_kind: string; source_id: number; amount: TaggedValue }>;
    expected: Record<string, GoldenScalar>;
  }>;
  source_aggregation_cases: Array<{
    id: string;
    metadata?: { source_kind: "CASH_ACCOUNT" | "PORTFOLIO"; source_id: number; source_name: string; source_is_archived: boolean };
    allocations: Array<{ id: number; goal_id: number; source_kind: "CASH_ACCOUNT" | "PORTFOLIO"; source_id: number; amount: number }>;
    expected: Array<{ source_kind: "CASH_ACCOUNT" | "PORTFOLIO"; source_id: number; designated_total: number }>;
  }>;
};

const golden = JSON.parse(
  readFileSync(new URL("../../test-fixtures/goal-funding-golden.json", import.meta.url), "utf8"),
) as GoldenFixture;

function decode(value: TaggedValue): number {
  if (typeof value === "number") return value;
  return value.non_finite === "NaN" ? NaN : value.non_finite === "Infinity" ? Infinity : -Infinity;
}

function assertGoldenValue(actual: unknown, expected: GoldenScalar): void {
  if (expected === null) {
    assert.equal(actual, null);
    return;
  }
  if (typeof expected === "boolean") {
    assert.equal(actual, expected);
    return;
  }
  const expectedNumber = decode(expected);
  if (Number.isNaN(expectedNumber)) assert.ok(typeof actual === "number" && Number.isNaN(actual));
  else assert.equal(actual, expectedNumber);
}

/**
 * Historical TypeScript arithmetic retained in the parity test only. The
 * production owner has moved to server Goal Context facts; this helper proves
 * the shared fixture records the exact pre-cutover behavior, including its
 * invalid-target/non-finite edge cases.
 */
function historicalGoalFunding(targetAmount: TaggedValue, allocations: Array<{ amount: TaggedValue }>) {
  const target = decode(targetAmount);
  if (!Number.isFinite(target) || target <= 0) {
    return { designated_total: null, progress_ratio: null, progress_percent: null, funding_gap: null, fully_designated: null };
  }
  const designated = allocations.reduce((sum, allocation) => sum + decode(allocation.amount), 0);
  const ratio = designated / target;
  return {
    designated_total: designated,
    progress_ratio: ratio,
    progress_percent: ratio * 100,
    funding_gap: Math.max(target - designated, 0),
    fully_designated: designated >= target,
  };
}

test("shared golden fixture matches historical goal-funding arithmetic", () => {
  assert.equal(golden.schema_version, 1);
  assert.equal(golden.contract_version, "wealth.goal-context.v1");
  for (const example of golden.goal_funding_cases) {
    const actual = historicalGoalFunding(example.target_amount, example.allocations);
    for (const [field, expected] of Object.entries(example.expected)) {
      assertGoldenValue(actual[field as keyof typeof actual], expected);
    }
  }
});

function sourceDesignation(
  sourceKind: "CASH_ACCOUNT" | "PORTFOLIO",
  sourceId: number,
  total: number,
  overrides: Partial<GoalContextSourceDesignation> = {},
): GoalContextSourceDesignation {
  return {
    source_kind: sourceKind,
    source_id: sourceId,
    source_name: `${sourceKind} ${sourceId}`,
    source_is_archived: false,
    currency: "THB",
    designated_total_in_context_scope: total,
    ...overrides,
  };
}

function valueMap(entries: [FundingSourceKey, number | null][]): ReadonlyMap<FundingSourceKey, number | null> {
  return new Map(entries);
}

function metadataKey(sourceKind: string, sourceId: number): string {
  return `${sourceKind}:${sourceId}`;
}

/**
 * Test-only copy of the retired source aggregation behavior.  The parity
 * assertion deliberately starts with fixture allocations, not the server
 * response, so a change in the historical grouping rules cannot be hidden by
 * feeding expected totals back into the assertion.
 */
function historicalAggregateDesignatedBySource(
  allocations: Array<{ source_kind: "CASH_ACCOUNT" | "PORTFOLIO"; source_id: number; amount: number }>,
): Array<{ source_kind: "CASH_ACCOUNT" | "PORTFOLIO"; source_id: number; designated_total: number }> {
  const totals = new Map<string, { source_kind: "CASH_ACCOUNT" | "PORTFOLIO"; source_id: number; designated_total: number }>();
  for (const allocation of allocations) {
    const key = metadataKey(allocation.source_kind, allocation.source_id);
    const existing = totals.get(key);
    if (existing) {
      existing.designated_total += allocation.amount;
    } else {
      totals.set(key, {
        source_kind: allocation.source_kind,
        source_id: allocation.source_id,
        designated_total: allocation.amount,
      });
    }
  }
  return [...totals.values()].sort((left, right) =>
    left.source_kind.localeCompare(right.source_kind) || left.source_id - right.source_id,
  );
}

function normalizeSourceTotals(
  totals: Array<{ source_kind: "CASH_ACCOUNT" | "PORTFOLIO"; source_id: number; designated_total: number }>,
) {
  return [...totals].sort((left, right) =>
    left.source_kind.localeCompare(right.source_kind) || left.source_id - right.source_id,
  );
}

test("historical source aggregation matches golden allocation cases", () => {
  for (const example of golden.source_aggregation_cases) {
    assert.deepEqual(
      historicalAggregateDesignatedBySource(example.allocations),
      normalizeSourceTotals(example.expected),
      example.id,
    );
  }
});

test("Goal Context source aggregates consume server totals without recomputing them", () => {
  for (const example of golden.source_aggregation_cases) {
    const designations = example.expected.map((expected) => {
      const metadata = example.metadata
        && metadataKey(example.metadata.source_kind, example.metadata.source_id) === metadataKey(expected.source_kind, expected.source_id)
        ? example.metadata
        : undefined;
      return sourceDesignation(expected.source_kind, expected.source_id, expected.designated_total, metadata && {
        source_name: metadata.source_name,
        source_is_archived: metadata.source_is_archived,
      });
    });
    const rows = buildSourceFundingOverview(designations, valueMap([]));
    assert.deepEqual(
      normalizeSourceTotals(rows.map((row) => ({
        source_kind: row.sourceKind,
        source_id: row.sourceId,
        designated_total: row.health.totalDesignated,
      }))),
      normalizeSourceTotals(example.expected),
      example.id,
    );
  }
});

test("source identity keeps Cash and Portfolio with the same numeric id separate", () => {
  const designations = [
    sourceDesignation("CASH_ACCOUNT", 1, 100_000),
    sourceDesignation("PORTFOLIO", 1, 200_000),
  ];
  const rows = buildSourceFundingOverview(designations, valueMap([
    [sourceKey("CASH_ACCOUNT", 1), 100_000],
    [sourceKey("PORTFOLIO", 1), 200_000],
  ]));
  assert.equal(rows.length, 2);
  assert.equal(rows.find((row) => row.key === sourceKey("CASH_ACCOUNT", 1))?.health.status, "SUPPORTED");
  assert.equal(rows.find((row) => row.key === sourceKey("PORTFOLIO", 1))?.health.status, "SUPPORTED");
});

test("archived source metadata and presentation ordering come from Goal Context", () => {
  const rows = buildSourceFundingOverview([
    sourceDesignation("CASH_ACCOUNT", 9, 10, { source_name: "Zeta", source_is_archived: true }),
    sourceDesignation("CASH_ACCOUNT", 3, 20, { source_name: "Alpha" }),
  ], valueMap([]));
  assert.deepEqual(rows.map((row) => row.sourceName), ["Alpha", "Zeta"]);
  assert.equal(rows[1].sourceIsArchived, true);
  assert.equal(rows[1].health.status, "UNAVAILABLE");
});

test("Funding Health semantics remain unchanged", () => {
  assert.equal(computeSourceFundingHealth(300_000, 300_000).status, "SUPPORTED");
  assert.equal(computeSourceFundingHealth(300_000, 450_000).status, "SUPPORTED");
  assert.deepEqual(computeSourceFundingHealth(800_000, 650_000), {
    totalDesignated: 800_000,
    currentValue: 650_000,
    status: "OVER_ALLOCATED",
    shortfall: 150_000,
  });
  assert.equal(computeSourceFundingHealth(0, 0).status, "SUPPORTED");
  assert.equal(computeSourceFundingHealth(1, 0).status, "OVER_ALLOCATED");
  assert.equal(computeSourceFundingHealth(300_000, null).status, "UNAVAILABLE");
  assert.equal(computeSourceFundingHealth(300_000, NaN).status, "UNAVAILABLE");
  assert.equal(computeSourceFundingHealth(300_000, Infinity).status, "UNAVAILABLE");
  assert.equal(computeSourceFundingHealth(300_000, -100).status, "UNAVAILABLE");
});
