import test from "node:test";
import assert from "node:assert/strict";
import { computeTotalAssets, type TotalAssetsInput } from "./totalAssets.ts";
import type { CashAccount } from "./api.ts";

function account(overrides: Partial<CashAccount> = {}): CashAccount {
  return {
    id: 1,
    workspace_id: 1,
    name: "Main account",
    institution: null,
    currency: "THB",
    balance: 200,
    is_archived: false,
    created_at: "2026-08-01T00:00:00Z",
    updated_at: "2026-08-01T00:00:00Z",
    ...overrides,
  };
}

function input(overrides: Partial<TotalAssetsInput> = {}): TotalAssetsInput {
  return {
    investmentAssets: 1000,
    investmentComplete: true,
    cashStatus: "success",
    cashAccounts: [account()],
    ...overrides,
  };
}

test("adds external cash to investment assets exactly once", () => {
  const summary = computeTotalAssets(input());
  assert.equal(summary.investmentAssets, 1000);
  assert.equal(summary.externalCash, 200);
  assert.equal(summary.totalAssets, 1200);
});

test("zero external cash preserves the investment-only total", () => {
  const summary = computeTotalAssets(input({ cashAccounts: [] }));
  assert.equal(summary.externalCash, 0);
  assert.equal(summary.totalAssets, 1000);
});

test("a valid empty investment core produces a cash-only total", () => {
  const summary = computeTotalAssets(input({ investmentAssets: 0, cashAccounts: [account({ balance: 350 })] }));
  assert.equal(summary.totalAssets, 350);
});

test("brokerage cash is not separately added by the helper", () => {
  // The 1,000 input already includes brokerage cash from Portfolio NAV.
  const summary = computeTotalAssets(input({ investmentAssets: 1000, cashAccounts: [account({ balance: 200 })] }));
  assert.equal(summary.totalAssets, 1200);
});

test("archived rows are excluded from external cash", () => {
  const summary = computeTotalAssets(input({
    cashAccounts: [account({ balance: 200 }), account({ id: 2, balance: 999, is_archived: true })],
  }));
  assert.equal(summary.externalCash, 200);
  assert.equal(summary.totalAssets, 1200);
  assert.equal(summary.archivedCashAccountCount, 1);
});

test("malformed non-THB cash fails the cash side instead of being silently summed", () => {
  const summary = computeTotalAssets(input({ cashAccounts: [account({ currency: "USD" as CashAccount["currency"] })] }));
  assert.equal(summary.externalCash, null);
  assert.equal(summary.totalAssets, null);
  assert.equal(summary.cashComplete, false);
  assert.equal(summary.invalidCashAccountCount, 1);
});

test("incomplete investment data prevents a total", () => {
  const summary = computeTotalAssets(input({ investmentComplete: false }));
  assert.equal(summary.investmentAssets, null);
  assert.equal(summary.totalAssets, null);
});

test("cash failure prevents a total", () => {
  const summary = computeTotalAssets(input({ cashStatus: "error" }));
  assert.equal(summary.externalCash, null);
  assert.equal(summary.totalAssets, null);
});

test("empty inputs are deterministic", () => {
  const summary = computeTotalAssets(input({ investmentAssets: 0, cashAccounts: [] }));
  assert.deepEqual(summary, {
    investmentAssets: 0,
    externalCash: 0,
    totalAssets: 0,
    investmentComplete: true,
    cashComplete: true,
    invalidCashAccountCount: 0,
    archivedCashAccountCount: 0,
  });
});
