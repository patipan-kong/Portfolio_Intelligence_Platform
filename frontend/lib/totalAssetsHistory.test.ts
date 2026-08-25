import assert from "node:assert/strict";
import { test } from "node:test";

import { computeTotalAssetsHistory, type CashAsOfEvidence, type TotalAssetsHistoryCashAccount } from "./totalAssetsHistory.ts";
import type { WealthHistoryPoint } from "./wealthHistory.ts";

function ip(date: string, totalValue: number, overrides: Partial<WealthHistoryPoint> = {}): WealthHistoryPoint {
  return {
    date,
    totalValue,
    contributingCount: 1,
    expectedCount: 1,
    complete: true,
    ...overrides,
  };
}

function account(id: number, createdAt: string): TotalAssetsHistoryCashAccount {
  return { id, created_at: createdAt };
}

function available(balance: number): CashAsOfEvidence {
  return { balance, available: true };
}

function unavailable(): CashAsOfEvidence {
  return { balance: null, available: false };
}

test("investment-only history: no CashAccounts ever existed, so cash is a legitimate zero at every date", () => {
  const result = computeTotalAssetsHistory([ip("2026-06-01", 500_000)], "success", [], {});

  assert.equal(result.points.length, 1);
  const point = result.points[0];
  assert.equal(point.investmentAssets, 500_000);
  assert.equal(point.cashExpectedCount, 0);
  assert.equal(point.cashComplete, true);
  assert.equal(point.externalCash, 0);
  assert.equal(point.totalAssets, 500_000);
  assert.equal(point.complete, true);
});

test("investment + Cash after baseline: an account created before the date with available evidence contributes", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const result = computeTotalAssetsHistory(
    [ip("2026-06-01", 500_000)],
    "success",
    [acc],
    { 1: { "2026-06-01": available(20_000) } },
  );

  const point = result.points[0];
  assert.equal(point.externalCash, 20_000);
  assert.equal(point.totalAssets, 520_000);
  assert.equal(point.complete, true);
});

test("Cash account not expected before its creation date", () => {
  const acc = account(1, "2026-07-01T00:00:00Z"); // created after the investment date below
  const result = computeTotalAssetsHistory([ip("2026-06-01", 500_000)], "success", [acc], {});

  const point = result.points[0];
  assert.equal(point.cashExpectedCount, 0);
  assert.equal(point.cashContributingCount, 0);
  assert.equal(point.cashComplete, true);
  assert.equal(point.externalCash, 0);
  assert.equal(point.totalAssets, 500_000);
});

test("Cash expected but unavailable between account creation and baseline effective date", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const result = computeTotalAssetsHistory(
    [ip("2026-02-01", 500_000)],
    "success",
    [acc],
    { 1: { "2026-02-01": unavailable() } }, // account exists, but no baseline yet
  );

  const point = result.points[0];
  assert.equal(point.cashExpectedCount, 1);
  assert.equal(point.cashContributingCount, 0);
  assert.equal(point.cashComplete, false);
  assert.equal(point.externalCash, null);
  assert.equal(point.totalAssets, null);
  assert.equal(point.complete, false);
});

test("Cash available exactly on the baseline effective date", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const result = computeTotalAssetsHistory(
    [ip("2026-03-01", 500_000)],
    "success",
    [acc],
    { 1: { "2026-03-01": available(10_000) } }, // 2026-03-01 is the baseline date itself
  );

  const point = result.points[0];
  assert.equal(point.cashComplete, true);
  assert.equal(point.externalCash, 10_000);
  assert.equal(point.totalAssets, 510_000);
});

test("Cash carry-forward after baseline: later dates use whatever the As-Of evidence resolves to", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const result = computeTotalAssetsHistory(
    [ip("2026-03-01", 500_000), ip("2026-04-01", 505_000)],
    "success",
    [acc],
    {
      1: {
        "2026-03-01": available(10_000),
        "2026-04-01": available(10_000), // no ledger activity since baseline — carried forward by the backend
      },
    },
  );

  assert.equal(result.points[1].externalCash, 10_000);
  assert.equal(result.points[1].totalAssets, 515_000);
});

test("archived Cash remains historically included — archive state is never consulted", () => {
  const activeAcc = account(1, "2026-01-01T00:00:00Z");
  const archivedAcc = account(2, "2026-01-01T00:00:00Z"); // conceptually archived; type carries no is_archived field at all
  const result = computeTotalAssetsHistory(
    [ip("2026-06-01", 500_000)],
    "success",
    [activeAcc, archivedAcc],
    { 1: { "2026-06-01": available(10_000) }, 2: { "2026-06-01": available(5_000) } },
  );

  const point = result.points[0];
  assert.equal(point.cashExpectedCount, 2);
  assert.equal(point.cashContributingCount, 2);
  assert.equal(point.externalCash, 15_000);
  assert.equal(point.totalAssets, 515_000);
});

test("missing Cash evidence (no map entry at all) makes the point incomplete, never a silent zero", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const result = computeTotalAssetsHistory([ip("2026-06-01", 500_000)], "success", [acc], {});

  const point = result.points[0];
  assert.equal(point.cashExpectedCount, 1);
  assert.equal(point.cashContributingCount, 0);
  assert.equal(point.cashComplete, false);
  assert.equal(point.totalAssets, null);
});

test("a failed Cash As-Of request (represented as a missing entry) makes the affected point incomplete", () => {
  const acc1 = account(1, "2026-01-01T00:00:00Z");
  const acc2 = account(2, "2026-01-01T00:00:00Z");
  // acc2's request failed — the caller never wrote an entry for it, same
  // representation as "never fetched". This must not become a fabricated 0.
  const result = computeTotalAssetsHistory(
    [ip("2026-06-01", 500_000)],
    "success",
    [acc1, acc2],
    { 1: { "2026-06-01": available(10_000) } },
  );

  const point = result.points[0];
  assert.equal(point.cashExpectedCount, 2);
  assert.equal(point.cashContributingCount, 1);
  assert.equal(point.cashComplete, false);
  assert.equal(point.externalCash, null);
  assert.equal(point.totalAssets, null);
});

test("a legitimate zero Cash balance is available, distinct from missing evidence", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const result = computeTotalAssetsHistory(
    [ip("2026-06-01", 500_000)],
    "success",
    [acc],
    { 1: { "2026-06-01": available(0) } },
  );

  const point = result.points[0];
  assert.equal(point.cashContributingCount, 1); // counted, not treated as missing
  assert.equal(point.cashComplete, true);
  assert.equal(point.externalCash, 0);
  assert.equal(point.totalAssets, 500_000);
});

test("brokerage cash is not double-counted — Investment Assets is used exactly as supplied", () => {
  // The investment point's totalValue already includes brokerage cash (per
  // PortfolioSnapshot.total_value); this module adds nothing beyond externalCash.
  const result = computeTotalAssetsHistory([ip("2026-06-01", 500_000)], "success", [], {});
  assert.equal(result.points[0].investmentAssets, 500_000);
  assert.equal(result.points[0].totalAssets, 500_000);
});

test("multiple CashAccounts aggregate correctly", () => {
  const accounts = [account(1, "2026-01-01T00:00:00Z"), account(2, "2026-01-01T00:00:00Z"), account(3, "2026-01-01T00:00:00Z")];
  const result = computeTotalAssetsHistory(
    [ip("2026-06-01", 500_000)],
    "success",
    accounts,
    {
      1: { "2026-06-01": available(1_000) },
      2: { "2026-06-01": available(2_000) },
      3: { "2026-06-01": available(3_000) },
    },
  );

  assert.equal(result.points[0].externalCash, 6_000);
  assert.equal(result.points[0].totalAssets, 506_000);
});

test("an investment-incomplete point remains incomplete even with full Cash coverage", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const result = computeTotalAssetsHistory(
    [ip("2026-06-01", 500_000, { complete: false })],
    "success",
    [acc],
    { 1: { "2026-06-01": available(10_000) } },
  );

  const point = result.points[0];
  assert.equal(point.investmentComplete, false);
  assert.equal(point.cashComplete, true);
  assert.equal(point.complete, false);
  assert.equal(point.totalAssets, null);
});

test("latest complete point ignores a later partial point", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const result = computeTotalAssetsHistory(
    [
      ip("2026-06-01", 500_000),
      ip("2026-06-02", 999_999, { complete: false }), // investment side incomplete this day
    ],
    "success",
    [acc],
    { 1: { "2026-06-01": available(10_000), "2026-06-02": available(10_000) } },
  );

  assert.equal(result.latest?.date, "2026-06-01");
  assert.equal(result.latest?.totalAssets, 510_000);
});

test("change uses comparable complete points only, skipping a partial point in between", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const result = computeTotalAssetsHistory(
    [
      ip("2026-06-01", 500_000),
      ip("2026-06-02", 999_999, { complete: false }),
      ip("2026-06-03", 520_000),
    ],
    "success",
    [acc],
    {
      1: {
        "2026-06-01": available(10_000),
        "2026-06-02": available(10_000),
        "2026-06-03": available(10_000),
      },
    },
  );

  assert.ok(result.delta);
  assert.equal(result.delta!.from.date, "2026-06-01");
  assert.equal(result.delta!.to.date, "2026-06-03");
  assert.equal(result.delta!.change, 530_000 - 510_000);
});

test("empty history produces no points, no latest, no delta", () => {
  const result = computeTotalAssetsHistory([], "success", [], {});
  assert.deepEqual(result.points, []);
  assert.equal(result.hasAnyPoints, false);
  assert.equal(result.latest, null);
  assert.equal(result.delta, null);
});

test("no current CashAccount.balance fallback — a raw account-like object's extraneous balance field is never read", () => {
  const acc = { id: 1, created_at: "2026-01-01T00:00:00Z", balance: 999_999 } as TotalAssetsHistoryCashAccount & { balance: number };
  // No As-Of evidence supplied for this date — the function must not fall
  // back to the account's live `balance` field, even though it is present
  // on the object passed in.
  const result = computeTotalAssetsHistory([ip("2026-06-01", 500_000)], "success", [acc], {});

  const point = result.points[0];
  assert.equal(point.cashComplete, false);
  assert.equal(point.externalCash, null);
  assert.equal(point.totalAssets, null);
});

test("cashAccountsStatus other than success makes every date's cash side incomplete, regardless of evidence present", () => {
  const acc = account(1, "2026-01-01T00:00:00Z");
  const loading = computeTotalAssetsHistory(
    [ip("2026-06-01", 500_000)],
    "loading",
    [acc],
    { 1: { "2026-06-01": available(10_000) } },
  );
  assert.equal(loading.points[0].cashComplete, false);
  assert.equal(loading.points[0].totalAssets, null);

  const errored = computeTotalAssetsHistory(
    [ip("2026-06-01", 500_000)],
    "error",
    [acc],
    { 1: { "2026-06-01": available(10_000) } },
  );
  assert.equal(errored.points[0].cashComplete, false);
  assert.equal(errored.points[0].totalAssets, null);
});
