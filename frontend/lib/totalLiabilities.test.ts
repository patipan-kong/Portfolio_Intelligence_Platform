import test from "node:test";
import assert from "node:assert/strict";
import { computeTotalLiabilities, type TotalLiabilitiesInput } from "./totalLiabilities.ts";
import type { Liability } from "./api.ts";

function liability(overrides: Partial<Liability> = {}): Liability {
  return {
    id: 1,
    workspace_id: 1,
    name: "Mortgage",
    liability_type: "MORTGAGE",
    lender: "Bank",
    balance: 200_000,
    currency: "THB",
    note: null,
    is_archived: false,
    created_at: "2026-08-01T00:00:00Z",
    updated_at: "2026-08-01T00:00:00Z",
    ...overrides,
  };
}

function input(overrides: Partial<TotalLiabilitiesInput> = {}): TotalLiabilitiesInput {
  return {
    liabilities: [liability()],
    liabilityStatus: "success",
    ...overrides,
  };
}

test("sums multiple active observed liabilities exactly once", () => {
  const summary = computeTotalLiabilities(input({
    liabilities: [liability({ id: 1, balance: 200_000 }), liability({ id: 2, balance: 50_000 })],
  }));
  assert.equal(summary.totalLiabilities, 250_000);
});

test("successful empty active set is a known zero", () => {
  const summary = computeTotalLiabilities(input({ liabilities: [] }));
  assert.equal(summary.totalLiabilities, 0);
  assert.equal(summary.liabilityComplete, true);
});

test("zero-balance active liability contributes zero without warning", () => {
  const summary = computeTotalLiabilities(input({ liabilities: [liability({ balance: 0 })] }));
  assert.equal(summary.totalLiabilities, 0);
  assert.equal(summary.invalidLiabilityCount, 0);
});

test("archived liabilities are excluded defensively", () => {
  const summary = computeTotalLiabilities(input({
    liabilities: [liability({ balance: 125_000 }), liability({ id: 2, balance: 999_999, is_archived: true })],
  }));
  assert.equal(summary.totalLiabilities, 125_000);
  assert.equal(summary.archivedLiabilityCount, 1);
});

test("only THB balances are accepted", () => {
  const summary = computeTotalLiabilities(input({ liabilities: [liability({ currency: "USD" as Liability["currency"] })] }));
  assert.equal(summary.totalLiabilities, null);
  assert.equal(summary.liabilityComplete, false);
  assert.equal(summary.invalidLiabilityCount, 1);
});

test("negative balances are unavailable rather than negated", () => {
  const summary = computeTotalLiabilities(input({ liabilities: [liability({ balance: -10 })] }));
  assert.equal(summary.totalLiabilities, null);
  assert.equal(summary.invalidLiabilityCount, 1);
});

test("NaN balances are unavailable", () => {
  const summary = computeTotalLiabilities(input({ liabilities: [liability({ balance: Number.NaN })] }));
  assert.equal(summary.totalLiabilities, null);
  assert.equal(summary.invalidLiabilityCount, 1);
});

test("infinite balances are unavailable", () => {
  const summary = computeTotalLiabilities(input({ liabilities: [liability({ balance: Number.POSITIVE_INFINITY })] }));
  assert.equal(summary.totalLiabilities, null);
  assert.equal(summary.invalidLiabilityCount, 1);
});

test("a failed liability request is unavailable even when the rows are empty", () => {
  const summary = computeTotalLiabilities(input({ liabilities: [], liabilityStatus: "error" }));
  assert.equal(summary.totalLiabilities, null);
  assert.equal(summary.liabilityComplete, false);
});

test("balances remain positive owed amounts with no double-sign behavior", () => {
  const summary = computeTotalLiabilities(input({ liabilities: [liability({ balance: 1_250 })] }));
  assert.equal(summary.totalLiabilities, 1_250);
  assert.notEqual(summary.totalLiabilities, -1_250);
});
