import assert from "node:assert/strict";
import { test } from "node:test";

import { DEFAULT_FILTERS, bangkokDateKey, filterTransactions, hasActiveFilters, type TransactionFilters } from "./transactionFilters.ts";
import type { TransactionRecord } from "@/lib/api";

function tx(overrides: Partial<TransactionRecord> = {}): TransactionRecord {
  return {
    id: 1,
    portfolio_id: 1,
    symbol: "PTT.BK",
    type: "BUY",
    shares: 100,
    price_per_share: 35,
    total_amount: 3500,
    fees: 5.5,
    taxes: 0,
    currency: "THB",
    exchange_rate: 1,
    transaction_date: "2026-08-10T03:00:00Z",
    notes: null,
    sector: "Energy",
    created_at: "2026-08-10T03:00:01Z",
    ...overrides,
  };
}

function filters(overrides: Partial<TransactionFilters> = {}): TransactionFilters {
  return { ...DEFAULT_FILTERS, ...overrides };
}

test("no filters active returns every record, in original order", () => {
  const records = [tx({ id: 1, symbol: "AAA.BK" }), tx({ id: 2, symbol: "BBB.BK" })];
  const result = filterTransactions(records, DEFAULT_FILTERS);
  assert.deepEqual(result.map((r) => r.id), [1, 2]);
});

test("search matches on symbol", () => {
  const records = [tx({ id: 1, symbol: "BANPU.BK" }), tx({ id: 2, symbol: "PTT.BK" })];
  const result = filterTransactions(records, filters({ search: "banpu" }));
  assert.deepEqual(result.map((r) => r.id), [1]);
});

test("search matches on notes", () => {
  const records = [
    tx({ id: 1, notes: "quarterly rebalance" }),
    tx({ id: 2, notes: "tax loss harvest" }),
  ];
  const result = filterTransactions(records, filters({ search: "rebalance" }));
  assert.deepEqual(result.map((r) => r.id), [1]);
});

test("search is case-insensitive and trims surrounding whitespace", () => {
  const records = [tx({ id: 1, symbol: "BANPU.BK" })];
  const result = filterTransactions(records, filters({ search: "  BaNpU  " }));
  assert.deepEqual(result.map((r) => r.id), [1]);
});

test("a transaction with no symbol or matching notes never matches a non-empty search", () => {
  const records = [tx({ id: 1, symbol: null, notes: null, type: "DEPOSIT" })];
  const result = filterTransactions(records, filters({ search: "banpu" }));
  assert.deepEqual(result, []);
});

test("empty search string applies no restriction", () => {
  const records = [tx({ id: 1 }), tx({ id: 2 })];
  const result = filterTransactions(records, filters({ search: "   " }));
  assert.equal(result.length, 2);
});

test("type filter restricts to the exact transaction type", () => {
  const records = [
    tx({ id: 1, type: "BUY" }),
    tx({ id: 2, type: "DIVIDEND" }),
    tx({ id: 3, type: "SELL" }),
  ];
  const result = filterTransactions(records, filters({ type: "DIVIDEND" }));
  assert.deepEqual(result.map((r) => r.id), [2]);
});

test("From date is inclusive", () => {
  const records = [
    tx({ id: 1, transaction_date: "2026-08-09T12:00:00Z" }),
    tx({ id: 2, transaction_date: "2026-08-10T12:00:00Z" }),
  ];
  const result = filterTransactions(records, filters({ from: bangkokDateKey("2026-08-10T12:00:00Z") }));
  assert.deepEqual(result.map((r) => r.id), [2]);
});

test("To date is inclusive", () => {
  const records = [
    tx({ id: 1, transaction_date: "2026-08-10T12:00:00Z" }),
    tx({ id: 2, transaction_date: "2026-08-11T12:00:00Z" }),
  ];
  const result = filterTransactions(records, filters({ to: bangkokDateKey("2026-08-10T12:00:00Z") }));
  assert.deepEqual(result.map((r) => r.id), [1]);
});

test("date comparison uses the Asia/Bangkok calendar date, not the raw UTC date", () => {
  // 2026-08-10T20:00:00Z is 2026-08-11 03:00 in Bangkok (UTC+7) — a
  // From=2026-08-11 filter must include it even though the UTC date is
  // still the 10th, matching how TransactionHistoryTable displays the row.
  const records = [tx({ id: 1, transaction_date: "2026-08-10T20:00:00Z" })];
  const result = filterTransactions(records, filters({ from: "2026-08-11" }));
  assert.deepEqual(result.map((r) => r.id), [1]);
});

test("a transaction just before the Bangkok day boundary is excluded from the next day's From filter", () => {
  // 2026-08-10T16:59:59Z is 2026-08-10 23:59:59 in Bangkok — still the 10th.
  const records = [tx({ id: 1, transaction_date: "2026-08-10T16:59:59Z" })];
  const result = filterTransactions(records, filters({ from: "2026-08-11" }));
  assert.deepEqual(result, []);
});

test("combined filters use AND semantics", () => {
  const records = [
    tx({ id: 1, symbol: "BANPU.BK", type: "BUY", transaction_date: "2026-08-10T03:00:00Z" }),
    tx({ id: 2, symbol: "BANPU.BK", type: "SELL", transaction_date: "2026-08-10T03:00:00Z" }),
    tx({ id: 3, symbol: "PTT.BK", type: "BUY", transaction_date: "2026-08-10T03:00:00Z" }),
    tx({ id: 4, symbol: "BANPU.BK", type: "BUY", transaction_date: "2026-01-01T03:00:00Z" }),
  ];
  const result = filterTransactions(
    records,
    filters({ search: "BANPU", type: "BUY", from: "2026-06-01" })
  );
  assert.deepEqual(result.map((r) => r.id), [1]);
});

test("clearing filters (DEFAULT_FILTERS) restores the complete list", () => {
  const records = [tx({ id: 1 }), tx({ id: 2 }), tx({ id: 3 })];
  const narrowed = filterTransactions(records, filters({ search: "nonexistent" }));
  assert.deepEqual(narrowed, []);
  const restored = filterTransactions(records, DEFAULT_FILTERS);
  assert.deepEqual(restored.map((r) => r.id), [1, 2, 3]);
});

test("hasActiveFilters is false only when every field is at its default", () => {
  assert.equal(hasActiveFilters(DEFAULT_FILTERS), false);
  assert.equal(hasActiveFilters(filters({ search: "x" })), true);
  assert.equal(hasActiveFilters(filters({ type: "BUY" })), true);
  assert.equal(hasActiveFilters(filters({ from: "2026-01-01" })), true);
  assert.equal(hasActiveFilters(filters({ to: "2026-01-01" })), true);
  assert.equal(hasActiveFilters(filters({ search: "   " })), false); // whitespace-only search is not active
});
