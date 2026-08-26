import assert from "node:assert/strict";
import { test } from "node:test";

import { computeNetWorthHistory } from "./netWorthHistory.ts";
import type { TotalAssetsHistoryPoint, TotalAssetsHistorySummary } from "./totalAssetsHistory.ts";
import type { TotalLiabilitiesHistoryPoint, TotalLiabilitiesHistorySummary } from "./totalLiabilitiesHistory.ts";

function assetsPoint(date: string, totalAssets: number | null, complete = totalAssets != null): TotalAssetsHistoryPoint {
  return {
    date,
    investmentAssets: totalAssets,
    investmentContributingCount: 1,
    investmentExpectedCount: 1,
    investmentComplete: complete,
    externalCash: 0,
    cashContributingCount: 0,
    cashExpectedCount: 0,
    cashComplete: complete,
    totalAssets,
    complete,
  };
}

function liabilitiesPoint(
  date: string,
  totalLiabilities: number | null,
  complete = totalLiabilities != null,
): TotalLiabilitiesHistoryPoint {
  return {
    date,
    totalLiabilities,
    contributingCount: complete ? 1 : 0,
    expectedCount: 1,
    complete,
  };
}

function assetsHistory(points: TotalAssetsHistoryPoint[]): Pick<TotalAssetsHistorySummary, "points"> {
  return { points };
}

function liabilitiesHistory(points: TotalLiabilitiesHistoryPoint[]): Pick<TotalLiabilitiesHistorySummary, "points"> {
  return { points };
}

// 1. basic assets minus liabilities
test("net worth is assets minus liabilities on a complete date", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", 500_000)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 200_000)]),
  );

  const point = result.points[0];
  assert.equal(point.netWorth, 300_000);
  assert.equal(point.complete, true);
});

// 2. multiple dates
test("multiple dates each compose independently", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01", "2026-06-02"],
    assetsHistory([assetsPoint("2026-06-01", 500_000), assetsPoint("2026-06-02", 520_000)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 200_000), liabilitiesPoint("2026-06-02", 190_000)]),
  );

  assert.equal(result.points[0].netWorth, 300_000);
  assert.equal(result.points[1].netWorth, 330_000);
});

// 3. zero liabilities
test("zero liabilities still produces a complete point", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", 500_000)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 0)]),
  );

  assert.equal(result.points[0].netWorth, 500_000);
  assert.equal(result.points[0].complete, true);
});

// 4. zero assets
test("zero assets still produces a complete point", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", 0)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 50_000)]),
  );

  assert.equal(result.points[0].netWorth, -50_000);
  assert.equal(result.points[0].complete, true);
});

// 5. zero net worth
test("equal assets and liabilities produce a legitimate zero net worth", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", 100_000)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 100_000)]),
  );

  assert.equal(result.points[0].netWorth, 0);
  assert.equal(result.points[0].complete, true);
});

// 6. negative net worth
test("liabilities exceeding assets produce a negative, unclamped net worth", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", 100_000)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 150_000)]),
  );

  assert.equal(result.points[0].netWorth, -50_000);
  assert.equal(result.points[0].complete, true);
});

// 7. assets incomplete
test("an incomplete Assets side keeps net worth unavailable, never falling back to zero assets", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", null, false)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 50_000)]),
  );

  const point = result.points[0];
  assert.equal(point.assetsComplete, false);
  assert.equal(point.liabilitiesComplete, true);
  assert.equal(point.complete, false);
  assert.equal(point.netWorth, null);
});

// 8. liabilities incomplete
test("an incomplete Liabilities side keeps net worth unavailable, never interpreted as zero debt", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", 500_000)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", null, false)]),
  );

  const point = result.points[0];
  assert.equal(point.assetsComplete, true);
  assert.equal(point.liabilitiesComplete, false);
  assert.equal(point.complete, false);
  assert.equal(point.netWorth, null);
});

// 9. both incomplete
test("both sides incomplete keeps net worth unavailable", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", null, false)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", null, false)]),
  );

  const point = result.points[0];
  assert.equal(point.complete, false);
  assert.equal(point.netWorth, null);
});

// 10. legitimate zero values remain valid
test("zero-valued but complete sides are distinguished from unavailable sides", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", 0)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 0)]),
  );

  const point = result.points[0];
  assert.equal(point.assetsComplete, true);
  assert.equal(point.liabilitiesComplete, true);
  assert.equal(point.totalAssets, 0);
  assert.equal(point.totalLiabilities, 0);
  assert.equal(point.netWorth, 0);
  assert.equal(point.complete, true);
});

// 11. latest complete point skips later incomplete dates
test("latest complete point ignores a later incomplete point", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01", "2026-06-02"],
    assetsHistory([assetsPoint("2026-06-01", 500_000), assetsPoint("2026-06-02", null, false)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 200_000), liabilitiesPoint("2026-06-02", 190_000)]),
  );

  assert.equal(result.latest?.date, "2026-06-01");
  assert.equal(result.latest?.netWorth, 300_000);
});

// 12 & 13. previous comparable complete point + delta calculation
test("delta compares the two most recent complete points, skipping an incomplete one in between", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01", "2026-06-02", "2026-06-03"],
    assetsHistory([
      assetsPoint("2026-06-01", 500_000),
      assetsPoint("2026-06-02", null, false),
      assetsPoint("2026-06-03", 530_000),
    ]),
    liabilitiesHistory([
      liabilitiesPoint("2026-06-01", 200_000),
      liabilitiesPoint("2026-06-02", 190_000),
      liabilitiesPoint("2026-06-03", 180_000),
    ]),
  );

  assert.ok(result.delta);
  assert.equal(result.delta!.from.date, "2026-06-01");
  assert.equal(result.delta!.to.date, "2026-06-03");
  assert.equal(result.delta!.from.netWorth, 300_000);
  assert.equal(result.delta!.to.netWorth, 350_000);
  assert.equal(result.delta!.change, 50_000);
});

// 14. mismatched/missing date evidence is not silently paired
test("a date present in the spine but missing from one side's points is honestly marked incomplete, not paired by position", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01", "2026-06-02"],
    assetsHistory([assetsPoint("2026-06-01", 500_000)]), // no point for 2026-06-02 at all
    liabilitiesHistory([liabilitiesPoint("2026-06-01", 200_000), liabilitiesPoint("2026-06-02", 190_000)]),
  );

  const missing = result.points.find((p) => p.date === "2026-06-02")!;
  assert.equal(missing.assetsComplete, false);
  assert.equal(missing.complete, false);
  assert.equal(missing.netWorth, null);
  // The 06-01 point must be unaffected by the mismatch on 06-02.
  const present = result.points.find((p) => p.date === "2026-06-01")!;
  assert.equal(present.netWorth, 300_000);
});

// 15. empty history
test("empty date spine produces no points, no latest, no delta", () => {
  const result = computeNetWorthHistory([], assetsHistory([]), liabilitiesHistory([]));
  assert.deepEqual(result.points, []);
  assert.equal(result.hasAnyPoints, false);
  assert.equal(result.latest, null);
  assert.equal(result.delta, null);
});

// 16. input immutability
test("does not mutate the input summaries' points arrays", () => {
  const assetsPoints = [assetsPoint("2026-06-02", 500_000), assetsPoint("2026-06-01", 490_000)];
  const liabilityPoints = [liabilitiesPoint("2026-06-02", 200_000), liabilitiesPoint("2026-06-01", 190_000)];
  const assetsSnapshot = [...assetsPoints];
  const liabilitiesSnapshot = [...liabilityPoints];

  computeNetWorthHistory(
    ["2026-06-01", "2026-06-02"],
    assetsHistory(assetsPoints),
    liabilitiesHistory(liabilityPoints),
  );

  assert.deepEqual(assetsPoints, assetsSnapshot);
  assert.deepEqual(liabilityPoints, liabilitiesSnapshot);
});

test("unavailable liability history never becomes zero debt, even when assets are complete and liabilities total would otherwise be small", () => {
  const result = computeNetWorthHistory(
    ["2026-06-01"],
    assetsHistory([assetsPoint("2026-06-01", 1_000)]),
    liabilitiesHistory([liabilitiesPoint("2026-06-01", null, false)]),
  );

  const point = result.points[0];
  assert.notEqual(point.totalLiabilities, 0);
  assert.equal(point.totalLiabilities, null);
  assert.equal(point.netWorth, null);
});

test("points come exactly from the supplied date spine, sorted ascending, with no synthesized dates", () => {
  const result = computeNetWorthHistory(
    ["2026-06-03", "2026-06-01", "2026-06-02"],
    assetsHistory([
      assetsPoint("2026-06-01", 1),
      assetsPoint("2026-06-02", 1),
      assetsPoint("2026-06-03", 1),
    ]),
    liabilitiesHistory([
      liabilitiesPoint("2026-06-01", 0),
      liabilitiesPoint("2026-06-02", 0),
      liabilitiesPoint("2026-06-03", 0),
    ]),
  );

  assert.deepEqual(result.points.map((p) => p.date), ["2026-06-01", "2026-06-02", "2026-06-03"]);
});
