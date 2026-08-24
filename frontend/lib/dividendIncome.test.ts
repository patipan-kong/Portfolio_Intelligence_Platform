import assert from "node:assert/strict";
import { test } from "node:test";

import {
  filterDividends,
  computeTotalsByCurrency,
  computeIncomeByAsset,
  computeMonthlyIncome,
  sortRecentDividends,
  computeDividendSummary,
} from "./dividendIncome.ts";
import type { TransactionRecord } from "@/lib/api";

function tx(overrides: Partial<TransactionRecord> & { type: TransactionRecord["type"] }): TransactionRecord {
  return {
    id: 0,
    portfolio_id: 1,
    symbol: null,
    shares: null,
    price_per_share: null,
    total_amount: 0,
    fees: 0,
    taxes: 0,
    currency: "THB",
    exchange_rate: 1,
    transaction_date: "2026-01-15T00:00:00Z",
    notes: null,
    sector: null,
    created_at: null,
    ...overrides,
  };
}

function dividend(overrides: Partial<TransactionRecord> = {}): TransactionRecord {
  return tx({ type: "DIVIDEND", ...overrides });
}

test("total dividend income sums only DIVIDEND transactions", () => {
  const transactions = [
    dividend({ id: 1, symbol: "AAA", total_amount: 100 }),
    tx({ id: 2, type: "BUY", symbol: "AAA", total_amount: 5000 }),
    dividend({ id: 3, symbol: "BBB", total_amount: 50 }),
    tx({ id: 4, type: "SELL", symbol: "AAA", total_amount: 1000 }),
    tx({ id: 5, type: "DEPOSIT", total_amount: 2000 }),
  ];

  const dividends = filterDividends(transactions);
  assert.equal(dividends.length, 2);

  const totals = computeTotalsByCurrency(dividends);
  assert.deepEqual(totals, [{ currency: "THB", amount: 150 }]);
});

test("multiple dividends from the same symbol aggregate into one total", () => {
  const dividends = [
    dividend({ id: 1, symbol: "AAA", total_amount: 100 }),
    dividend({ id: 2, symbol: "AAA", total_amount: 75 }),
    dividend({ id: 3, symbol: "AAA", total_amount: 25 }),
  ];

  const byAsset = computeIncomeByAsset(dividends);
  assert.equal(byAsset.length, 1);
  assert.equal(byAsset[0].symbol, "AAA");
  assert.equal(byAsset[0].amount, 200);
  assert.equal(byAsset[0].count, 3);
});

test("dividends from different symbols remain distinct in the by-asset breakdown", () => {
  const dividends = [
    dividend({ id: 1, symbol: "AAA", total_amount: 100 }),
    dividend({ id: 2, symbol: "BBB", total_amount: 300 }),
    dividend({ id: 3, symbol: "AAA", total_amount: 50 }),
  ];

  const byAsset = computeIncomeByAsset(dividends);
  assert.equal(byAsset.length, 2);
  // Sorted descending by amount: BBB (300) before AAA (150).
  assert.equal(byAsset[0].symbol, "BBB");
  assert.equal(byAsset[0].amount, 300);
  assert.equal(byAsset[1].symbol, "AAA");
  assert.equal(byAsset[1].amount, 150);
});

test("a symbol-less dividend is retained, not dropped, and shown as its own honest row", () => {
  const dividends = [
    dividend({ id: 1, symbol: null, total_amount: 40 }),
    dividend({ id: 2, symbol: "AAA", total_amount: 100 }),
    dividend({ id: 3, symbol: null, total_amount: 10 }),
  ];

  const byAsset = computeIncomeByAsset(dividends);
  assert.equal(byAsset.length, 2);
  const noSymbolRow = byAsset.find((row) => row.symbol === null);
  assert.ok(noSymbolRow, "symbol-less dividends must not be dropped");
  assert.equal(noSymbolRow?.amount, 50);
  assert.equal(noSymbolRow?.count, 2);

  const totals = computeTotalsByCurrency(dividends);
  assert.equal(totals[0].amount, 150);
});

test("monthly grouping buckets by transaction_date's calendar month", () => {
  const dividends = [
    dividend({ id: 1, total_amount: 100, transaction_date: "2026-01-05T00:00:00Z" }),
    dividend({ id: 2, total_amount: 50, transaction_date: "2026-01-20T00:00:00Z" }),
    dividend({ id: 3, total_amount: 75, transaction_date: "2026-02-01T00:00:00Z" }),
  ];

  const byMonth = computeMonthlyIncome(dividends);
  assert.deepEqual(byMonth, [
    { month: "2026-01", currency: "THB", amount: 150 },
    { month: "2026-02", currency: "THB", amount: 75 },
  ]);
});

test("monthly grouping uses Bangkok local time, matching how the same transaction's date is displayed elsewhere in the app", () => {
  // 2026-01-31T19:00:00Z is 2026-02-01T02:00 in Asia/Bangkok (UTC+7) — a
  // naive UTC-month bucketing would wrongly put this dividend in January,
  // while the Recent Dividends list (Asia/Bangkok display) shows it as
  // received on February 1st. The two must agree.
  const dividends = [
    dividend({ id: 1, total_amount: 100, transaction_date: "2026-01-31T19:00:00Z" }),
  ];

  const byMonth = computeMonthlyIncome(dividends);
  assert.deepEqual(byMonth, [{ month: "2026-02", currency: "THB", amount: 100 }]);
});

test("no dividend rows produces an empty, zero-safe summary", () => {
  const transactions = [
    tx({ id: 1, type: "BUY", total_amount: 1000 }),
    tx({ id: 2, type: "DEPOSIT", total_amount: 500 }),
  ];

  const summary = computeDividendSummary(transactions);
  assert.equal(summary.dividends.length, 0);
  assert.deepEqual(summary.totalsByCurrency, []);
  assert.equal(summary.mixedCurrency, false);
  assert.deepEqual(summary.byAsset, []);
  assert.deepEqual(summary.byMonth, []);
  assert.deepEqual(summary.recent, []);
});

test("recent dividends are ordered most-recent-first and respect the limit", () => {
  const dividends = [
    dividend({ id: 1, total_amount: 10, transaction_date: "2026-01-01T00:00:00Z" }),
    dividend({ id: 2, total_amount: 20, transaction_date: "2026-03-01T00:00:00Z" }),
    dividend({ id: 3, total_amount: 30, transaction_date: "2026-02-01T00:00:00Z" }),
  ];

  const recent = sortRecentDividends(dividends, 2);
  assert.equal(recent.length, 2);
  assert.equal(recent[0].id, 2); // March — most recent
  assert.equal(recent[1].id, 3); // February
});

test("non-DIVIDEND transaction types never contribute to income calculations", () => {
  const transactions = [
    tx({ id: 1, type: "BUY", symbol: "AAA", total_amount: 100000 }),
    tx({ id: 2, type: "SELL", symbol: "AAA", total_amount: 100000 }),
    tx({ id: 3, type: "DEPOSIT", total_amount: 100000 }),
    tx({ id: 4, type: "WITHDRAW", total_amount: 100000 }),
    tx({ id: 5, type: "INITIAL_POSITION", symbol: "AAA", total_amount: 100000 }),
    tx({ id: 6, type: "INITIAL_CASH", total_amount: 100000 }),
    tx({ id: 7, type: "QUANTITY_CORRECTION", symbol: "AAA", total_amount: 100000 }),
    tx({ id: 8, type: "POSITION_CONVERSION", symbol: "AAA", total_amount: 100000 }),
  ];

  const summary = computeDividendSummary(transactions);
  assert.equal(summary.dividends.length, 0);
  assert.equal(summary.totalsByCurrency.length, 0);
});

test("mixed currencies are never summed together — each keeps its own total", () => {
  const dividends = [
    dividend({ id: 1, symbol: "AAA", total_amount: 100, currency: "THB" }),
    dividend({ id: 2, symbol: "AAPL", total_amount: 5, currency: "USD" }),
    dividend({ id: 3, symbol: "AAA", total_amount: 50, currency: "THB" }),
  ];

  const totals = computeTotalsByCurrency(dividends);
  assert.equal(totals.length, 2);
  const thb = totals.find((t) => t.currency === "THB");
  const usd = totals.find((t) => t.currency === "USD");
  assert.equal(thb?.amount, 150);
  assert.equal(usd?.amount, 5);

  const summary = computeDividendSummary(dividends);
  assert.equal(summary.mixedCurrency, true);

  // Same symbol in different currencies must not be merged in the by-asset view.
  const byAsset = computeIncomeByAsset([
    dividend({ id: 4, symbol: "AAA", total_amount: 10, currency: "THB" }),
    dividend({ id: 5, symbol: "AAA", total_amount: 3, currency: "USD" }),
  ]);
  assert.equal(byAsset.length, 2);
});

test("no NaN or Infinity for an empty dividend set", () => {
  const summary = computeDividendSummary([]);
  assert.equal(Number.isFinite(summary.totalsByCurrency.length), true);
  assert.deepEqual(summary.totalsByCurrency, []);
  assert.deepEqual(summary.byAsset, []);
  assert.deepEqual(summary.byMonth, []);
});
