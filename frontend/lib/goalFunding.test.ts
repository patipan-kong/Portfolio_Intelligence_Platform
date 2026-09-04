import assert from "node:assert/strict";
import { test } from "node:test";

import {
  buildSourceFundingOverview,
  factualReviewMatchesGoalContext,
  sourceDrillThroughHref,
  sourceFundingHealth,
  sourceKey,
} from "./goalFunding.ts";
import type { FactualReviewResponse, FactualReviewSource, GoalContextResponse } from "@/lib/api";

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
