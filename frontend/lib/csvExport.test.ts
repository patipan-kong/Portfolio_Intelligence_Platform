import assert from "node:assert/strict";
import { test } from "node:test";

import {
  escapeCsvField,
  transactionsToCsv,
  sanitizeFilenameFragment,
  buildExportFilename,
  CSV_UTF8_BOM,
} from "./csvExport.ts";
import type { TransactionRecord } from "./api.ts";

const HEADER = "Date,Type,Symbol,Shares,Price,Total Amount,Currency,Fees,Notes";

function tx(overrides: Partial<TransactionRecord> = {}): TransactionRecord {
  return {
    id: 1,
    portfolio_id: 4,
    symbol: "PTT.BK",
    type: "BUY",
    shares: 100,
    price_per_share: 35.5,
    total_amount: 3550,
    fees: 5,
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

test("header row lists columns in a fixed, deterministic order", () => {
  const csv = transactionsToCsv([]);
  assert.equal(csv, HEADER);
});

test("an ordinary BUY row serializes its fields in the documented order", () => {
  const csv = transactionsToCsv([tx()]);
  const lines = csv.split("\n");
  assert.equal(lines[0], HEADER);
  assert.equal(lines[1], "2026-08-10T03:00:00Z,BUY,PTT.BK,100,35.5,3550,THB,5,");
});

test("null/empty optional fields (symbol, shares, price, notes) serialize as empty, not fabricated", () => {
  const csv = transactionsToCsv([
    tx({ type: "DEPOSIT", symbol: null, shares: null, price_per_share: null, total_amount: 5000, notes: null }),
  ]);
  const row = csv.split("\n")[1];
  assert.equal(row, "2026-08-10T03:00:00Z,DEPOSIT,,,,5000,THB,5,");
});

test("commas in a field are quoted", () => {
  assert.equal(escapeCsvField("Broker fee, prorated"), '"Broker fee, prorated"');
  const csv = transactionsToCsv([tx({ notes: "Broker fee, prorated" })]);
  assert.match(csv.split("\n")[1], /"Broker fee, prorated"$/);
});

test("embedded double quotes are escaped by doubling", () => {
  assert.equal(escapeCsvField('Said "sell now"'), '"Said ""sell now"""');
  const csv = transactionsToCsv([tx({ notes: 'Said "sell now"' })]);
  assert.match(csv.split("\n")[1], /"Said ""sell now"""$/);
});

test("embedded newlines are quoted so the row stays on one logical CSV record", () => {
  assert.equal(escapeCsvField("line one\nline two"), '"line one\nline two"');
  const csv = transactionsToCsv([tx({ notes: "line one\nline two" })]);
  assert.match(csv, /"line one\nline two"/);
});

test("Unicode/Thai text is preserved as-is", () => {
  const csv = transactionsToCsv([tx({ notes: "ปันผลไตรมาส 2" })]);
  assert.match(csv.split("\n")[1], /ปันผลไตรมาส 2$/);
});

test("column ordering is stable across multiple rows regardless of transaction type mix", () => {
  const csv = transactionsToCsv([
    tx({ id: 1, type: "BUY" }),
    tx({ id: 2, type: "DIVIDEND", symbol: "ADVANC.BK", shares: null, price_per_share: null, total_amount: 320 }),
  ]);
  const lines = csv.split("\n");
  assert.equal(lines.length, 3);
  assert.equal(lines[0], HEADER);
});

test("POSITION_CONVERSION rows use the same generic columns — no conversion_detail columns, no raw JSON", () => {
  const csv = transactionsToCsv([
    tx({
      type: "POSITION_CONVERSION",
      symbol: "BANPU.BK",
      shares: 2562.214,
      price_per_share: 19.010512,
      total_amount: 48709,
      notes: "BANPU.BK -> BANPUU.BK",
      conversion_detail: {
        predecessor_symbol: "BANPU.BK",
        successor_symbol: "BANPUU.BK",
        conversion_ratio: 0.38242,
        shares_surrendered: 6700,
        shares_entitled: 2562.214,
        shares_received: 2562.214,
        legal_effective_date: "2026-03-02",
        valuation_transition_date: "2026-03-02",
        cost_basis_before: 48709,
        cost_basis_carried: 48709,
        cash_in_lieu: null,
      },
    }),
  ]);
  const lines = csv.split("\n");
  assert.equal(lines[0], HEADER);
  assert.equal(lines[1], "2026-08-10T03:00:00Z,POSITION_CONVERSION,BANPU.BK,2562.214,19.010512,48709,THB,5,BANPU.BK -> BANPUU.BK");
  assert.doesNotMatch(csv, /schema_version|predecessor_symbol|\{|\}/);
});

test("CSV_UTF8_BOM is a single leading BOM character, kept separate from the serializer's own output", () => {
  assert.equal(CSV_UTF8_BOM.length, 1);
  assert.equal(CSV_UTF8_BOM.charCodeAt(0), 0xfeff);
  assert.ok(!transactionsToCsv([tx()]).startsWith(CSV_UTF8_BOM));
});

test("sanitizeFilenameFragment strips unsafe filesystem characters and falls back when empty", () => {
  assert.equal(sanitizeFilenameFragment("Retirement Fund (THB)"), "Retirement-Fund-THB");
  assert.equal(sanitizeFilenameFragment("   "), "portfolio");
  assert.equal(sanitizeFilenameFragment("../../etc/passwd"), "etc-passwd");
});

test("buildExportFilename produces a deterministic, sanitized filename", () => {
  assert.equal(
    buildExportFilename("Retirement Fund", "2026-08-25"),
    "wealth-os-transactions-Retirement-Fund-2026-08-25.csv"
  );
  assert.equal(buildExportFilename(null, "2026-08-25"), "wealth-os-transactions-portfolio-2026-08-25.csv");
});
