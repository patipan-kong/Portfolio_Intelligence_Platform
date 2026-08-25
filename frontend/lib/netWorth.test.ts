import test from "node:test";
import assert from "node:assert/strict";
import { computeNetWorth, type NetWorthSummary } from "./netWorth.ts";
import type { TotalAssetsSummary } from "./totalAssets.ts";
import type { TotalLiabilitiesSummary } from "./totalLiabilities.ts";

function assets(totalAssets: number | null): Pick<TotalAssetsSummary, "totalAssets"> {
  return { totalAssets };
}

function liabilities(totalLiabilities: number | null): Pick<TotalLiabilitiesSummary, "totalLiabilities"> {
  return { totalLiabilities };
}

function result(totalAssets: number | null, totalLiabilities: number | null): NetWorthSummary {
  return computeNetWorth(assets(totalAssets), liabilities(totalLiabilities));
}

test("subtracts complete assets and liabilities", () => {
  assert.deepEqual(result(1000, 400), { netWorth: 600, netWorthComplete: true });
});

test("preserves complete zero-liability and zero-asset results", () => {
  assert.deepEqual(result(1000, 0), { netWorth: 1000, netWorthComplete: true });
  assert.deepEqual(result(0, 0), { netWorth: 0, netWorthComplete: true });
  assert.deepEqual(result(0, 400), { netWorth: -400, netWorthComplete: true });
});

test("preserves negative and equal-value results without clamping", () => {
  assert.deepEqual(result(100, 150), { netWorth: -50, netWorthComplete: true });
  assert.deepEqual(result(1000, 1000), { netWorth: 0, netWorthComplete: true });
});

test("keeps Net Worth unavailable when either aggregate is unavailable", () => {
  assert.deepEqual(result(null, 400), { netWorth: null, netWorthComplete: false });
  assert.deepEqual(result(1000, null), { netWorth: null, netWorthComplete: false });
  assert.deepEqual(result(null, null), { netWorth: null, netWorthComplete: false });
});

test("does not mutate source aggregate objects", () => {
  const totalAssets = assets(1000);
  const totalLiabilities = liabilities(400);
  const originalAssets = { ...totalAssets };
  const originalLiabilities = { ...totalLiabilities };

  assert.deepEqual(computeNetWorth(totalAssets, totalLiabilities), {
    netWorth: 600,
    netWorthComplete: true,
  });
  assert.deepEqual(totalAssets, originalAssets);
  assert.deepEqual(totalLiabilities, originalLiabilities);
});
