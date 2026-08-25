import assert from "node:assert/strict";
import { test } from "node:test";

import {
  computeTotalLiabilitiesHistory,
  type LiabilityAsOfEvidence,
  type TotalLiabilitiesHistoryLiability,
} from "./totalLiabilitiesHistory.ts";

function liability(id: number, createdAt: string): TotalLiabilitiesHistoryLiability {
  return { id, created_at: createdAt };
}

function available(balance: number, currency: "THB" = "THB"): LiabilityAsOfEvidence {
  return { balance, available: true, currency };
}

function unavailable(): LiabilityAsOfEvidence {
  return { balance: null, available: false, currency: "THB" };
}

// 1. single liability history
test("single liability contributes its As-Of balance on a date it exists", () => {
  const l = liability(1, "2026-01-01T00:00:00Z");
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "success",
    [l],
    { 1: { "2026-06-01": available(50_000) } },
  );

  const point = result.points[0];
  assert.equal(point.contributingCount, 1);
  assert.equal(point.expectedCount, 1);
  assert.equal(point.complete, true);
  assert.equal(point.totalLiabilities, 50_000);
});

// 2. multiple liabilities summed
test("multiple liabilities aggregate correctly", () => {
  const liabilities = [liability(1, "2026-01-01T00:00:00Z"), liability(2, "2026-01-01T00:00:00Z"), liability(3, "2026-01-01T00:00:00Z")];
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "success",
    liabilities,
    {
      1: { "2026-06-01": available(10_000) },
      2: { "2026-06-01": available(20_000) },
      3: { "2026-06-01": available(30_000) },
    },
  );

  assert.equal(result.points[0].totalLiabilities, 60_000);
  assert.equal(result.points[0].contributingCount, 3);
});

// 3. legitimate zero balance
test("a legitimate zero balance is available, distinct from missing evidence", () => {
  const l = liability(1, "2026-01-01T00:00:00Z");
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "success",
    [l],
    { 1: { "2026-06-01": available(0) } },
  );

  const point = result.points[0];
  assert.equal(point.contributingCount, 1); // counted, not treated as missing
  assert.equal(point.complete, true);
  assert.equal(point.totalLiabilities, 0);
});

// 4. first historical observation boundary
test("evidence available exactly on the first observation date", () => {
  const l = liability(1, "2026-01-01T00:00:00Z");
  const result = computeTotalLiabilitiesHistory(
    ["2026-03-01"],
    "success",
    [l],
    { 1: { "2026-03-01": available(15_000) } }, // 2026-03-01 is the first observation itself
  );

  const point = result.points[0];
  assert.equal(point.complete, true);
  assert.equal(point.totalLiabilities, 15_000);
});

// 5. unavailable before historical evidence
test("a liability that existed but has no observation on or before the date is expected but unavailable", () => {
  const l = liability(1, "2026-01-01T00:00:00Z"); // created well before, but no observation yet
  const result = computeTotalLiabilitiesHistory(
    ["2026-02-01"],
    "success",
    [l],
    { 1: { "2026-02-01": unavailable() } },
  );

  const point = result.points[0];
  assert.equal(point.expectedCount, 1);
  assert.equal(point.contributingCount, 0);
  assert.equal(point.complete, false);
  assert.equal(point.totalLiabilities, null);
});

// not-yet-created lifecycle boundary (companion to #5)
test("a liability not yet created by the date is not expected at all", () => {
  const l = liability(1, "2026-07-01T00:00:00Z"); // created after the date below
  const result = computeTotalLiabilitiesHistory(["2026-06-01"], "success", [l], {});

  const point = result.points[0];
  assert.equal(point.expectedCount, 0);
  assert.equal(point.contributingCount, 0);
  assert.equal(point.complete, true);
  assert.equal(point.totalLiabilities, 0);
});

// 6. archived liability historical inclusion
test("archived liabilities remain historically included — archive state is never consulted", () => {
  const active = liability(1, "2026-01-01T00:00:00Z");
  const archived = liability(2, "2026-01-01T00:00:00Z"); // conceptually archived; type carries no is_archived field at all
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "success",
    [active, archived],
    { 1: { "2026-06-01": available(10_000) }, 2: { "2026-06-01": available(5_000) } },
  );

  const point = result.points[0];
  assert.equal(point.expectedCount, 2);
  assert.equal(point.contributingCount, 2);
  assert.equal(point.totalLiabilities, 15_000);
});

// 7. incomplete historical evidence
test("one liability missing evidence keeps the whole point incomplete, never a partial total", () => {
  const l1 = liability(1, "2026-01-01T00:00:00Z");
  const l2 = liability(2, "2026-01-01T00:00:00Z");
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "success",
    [l1, l2],
    { 1: { "2026-06-01": available(10_000) } }, // l2 has no entry at all
  );

  const point = result.points[0];
  assert.equal(point.expectedCount, 2);
  assert.equal(point.contributingCount, 1);
  assert.equal(point.complete, false);
  assert.equal(point.totalLiabilities, null);
});

// 8. failed As-Of read
test("a failed As-Of request (represented as a missing entry) makes the affected point incomplete", () => {
  const l1 = liability(1, "2026-01-01T00:00:00Z");
  const l2 = liability(2, "2026-01-01T00:00:00Z");
  // l2's request failed — the caller never wrote an entry for it, same
  // representation as "never fetched". This must not become a fabricated 0.
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "success",
    [l1, l2],
    { 1: { "2026-06-01": available(10_000) }, 2: {} },
  );

  const point = result.points[0];
  assert.equal(point.contributingCount, 1);
  assert.equal(point.complete, false);
  assert.equal(point.totalLiabilities, null);
});

// 9. malformed/non-finite/negative evidence
test("non-finite or negative evidence is treated as unavailable, not a fabricated value", () => {
  const l1 = liability(1, "2026-01-01T00:00:00Z");
  const l2 = liability(2, "2026-01-01T00:00:00Z");
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "success",
    [l1, l2],
    {
      1: { "2026-06-01": { balance: Number.NaN, available: true, currency: "THB" } },
      2: { "2026-06-01": { balance: -5_000, available: true, currency: "THB" } },
    },
  );

  const point = result.points[0];
  assert.equal(point.contributingCount, 0);
  assert.equal(point.complete, false);
  assert.equal(point.totalLiabilities, null);
});

// 10. non-THB evidence
test("non-THB evidence is treated as unavailable", () => {
  const l = liability(1, "2026-01-01T00:00:00Z");
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "success",
    [l],
    { 1: { "2026-06-01": available(10_000, "USD" as "THB") } },
  );

  const point = result.points[0];
  assert.equal(point.contributingCount, 0);
  assert.equal(point.complete, false);
  assert.equal(point.totalLiabilities, null);
});

// 11. latest complete point
test("latest complete point ignores a later incomplete point", () => {
  const l = liability(1, "2026-01-01T00:00:00Z");
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01", "2026-06-02"],
    "success",
    [l],
    { 1: { "2026-06-01": available(10_000) } }, // no evidence for 06-02
  );

  assert.equal(result.latest?.date, "2026-06-01");
  assert.equal(result.latest?.totalLiabilities, 10_000);
});

// 12. previous comparable complete point (delta)
test("change uses comparable complete points only, skipping an incomplete point in between", () => {
  const l = liability(1, "2026-01-01T00:00:00Z");
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01", "2026-06-02", "2026-06-03"],
    "success",
    [l],
    {
      1: {
        "2026-06-01": available(10_000),
        // no entry for 06-02 — keeps it incomplete
        "2026-06-03": available(8_000),
      },
    },
  );

  assert.ok(result.delta);
  assert.equal(result.delta!.from.date, "2026-06-01");
  assert.equal(result.delta!.to.date, "2026-06-03");
  assert.equal(result.delta!.change, -2_000);
});

// 13. no fabricated zero
test("an incomplete point's totalLiabilities stays null, never a partial sum presented as complete", () => {
  const l1 = liability(1, "2026-01-01T00:00:00Z");
  const l2 = liability(2, "2026-01-01T00:00:00Z");
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "success",
    [l1, l2],
    { 1: { "2026-06-01": available(10_000) } },
  );

  assert.equal(result.points[0].totalLiabilities, null);
  assert.equal(result.completePoints.length, 0);
});

// 14. date alignment with the accepted shared history spine
test("points come exactly from the supplied date spine, sorted ascending, with no synthesized dates", () => {
  const result = computeTotalLiabilitiesHistory(
    ["2026-06-03", "2026-06-01", "2026-06-02"],
    "success",
    [],
    {},
  );

  assert.deepEqual(result.points.map((p) => p.date), ["2026-06-01", "2026-06-02", "2026-06-03"]);
});

test("no liabilities ever existed: a successful empty response is a legitimate zero at every date", () => {
  const result = computeTotalLiabilitiesHistory(["2026-06-01"], "success", [], {});
  const point = result.points[0];
  assert.equal(point.expectedCount, 0);
  assert.equal(point.complete, true);
  assert.equal(point.totalLiabilities, 0);
});

test("liabilityStatus other than success makes every date incomplete, regardless of evidence present", () => {
  const l = liability(1, "2026-01-01T00:00:00Z");
  const loading = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "loading",
    [l],
    { 1: { "2026-06-01": available(10_000) } },
  );
  assert.equal(loading.points[0].complete, false);
  assert.equal(loading.points[0].totalLiabilities, null);

  const errored = computeTotalLiabilitiesHistory(
    ["2026-06-01"],
    "error",
    [l],
    { 1: { "2026-06-01": available(10_000) } },
  );
  assert.equal(errored.points[0].complete, false);
  assert.equal(errored.points[0].totalLiabilities, null);
});

test("empty date spine produces no points, no latest, no delta", () => {
  const result = computeTotalLiabilitiesHistory([], "success", [], {});
  assert.deepEqual(result.points, []);
  assert.equal(result.hasAnyPoints, false);
  assert.equal(result.latest, null);
  assert.equal(result.delta, null);
});
