import assert from "node:assert/strict";
import { test } from "node:test";

import { parseCsv, validateRow, validateRows, buildImportPayload, type ImportRowInput } from "./csvImport.ts";

const HEADER = "date,type,symbol,shares,price,amount,notes";

function row(overrides: Partial<ImportRowInput> = {}): ImportRowInput {
  return {
    rowNumber: 1,
    date: "2026-08-10",
    type: "BUY",
    symbol: "PTT.BK",
    shares: "100",
    price: "35",
    amount: "",
    notes: "",
    ...overrides,
  };
}

test("valid BUY row passes validation and builds the correct payload", () => {
  const result = validateRow(row());
  assert.equal(result.status, "VALID");
  assert.deepEqual(result.errors, []);

  const built = buildImportPayload(result);
  assert.equal(built.type, "BUY");
  assert.deepEqual(built.payload, {
    symbol: "PTT.BK",
    shares: 100,
    price_per_share: 35,
    transaction_date: "2026-08-10",
    notes: undefined,
  });
});

test("valid DIVIDEND row passes validation and builds the correct payload", () => {
  const result = validateRow(row({ type: "DIVIDEND", symbol: "ADVANC.BK", shares: "", price: "", amount: "250" }));
  assert.equal(result.status, "VALID");

  const built = buildImportPayload(result);
  assert.equal(built.type, "DIVIDEND");
  assert.deepEqual(built.payload, {
    symbol: "ADVANC.BK",
    amount: 250,
    transaction_date: "2026-08-10",
    notes: undefined,
  });
});

test("DIVIDEND row with no symbol is still valid (symbol is optional)", () => {
  const result = validateRow(row({ type: "DIVIDEND", symbol: "", shares: "", price: "", amount: "250" }));
  assert.equal(result.status, "VALID");
  const built = buildImportPayload(result);
  assert.equal(built.payload.symbol, undefined);
});

test("unsupported transaction type is rejected, including other real backend types", () => {
  for (const t of ["INITIAL_POSITION", "INITIAL_CASH", "QUANTITY_CORRECTION", "POSITION_CONVERSION", "GARBAGE"]) {
    const result = validateRow(row({ type: t }));
    assert.equal(result.status, "INVALID");
    assert.ok(result.errors.some((e) => e.includes("Unsupported transaction type")));
  }
});

test("invalid date is rejected, including a calendar-impossible date", () => {
  for (const d of ["10-08-2026", "2026/08/10", "not-a-date", "2026-02-30"]) {
    const result = validateRow(row({ date: d }));
    assert.equal(result.status, "INVALID");
    assert.ok(result.errors.some((e) => e.includes("date")));
  }
});

test("missing required field: BUY without symbol is invalid", () => {
  const result = validateRow(row({ symbol: "" }));
  assert.equal(result.status, "INVALID");
  assert.ok(result.errors.includes("Symbol is required"));
});

test("missing required field: DEPOSIT without amount is invalid", () => {
  const result = validateRow(row({ type: "DEPOSIT", symbol: "", shares: "", price: "", amount: "" }));
  assert.equal(result.status, "INVALID");
  assert.ok(result.errors.includes("Amount must be a positive number"));
});

test("DEPOSIT/WITHDRAW forbid a symbol", () => {
  const result = validateRow(row({ type: "WITHDRAW", symbol: "PTT.BK", shares: "", price: "", amount: "500" }));
  assert.equal(result.status, "INVALID");
  assert.ok(result.errors.includes("Symbol is not allowed for DEPOSIT/WITHDRAW"));
});

test("SELL without shares/price is invalid", () => {
  const result = validateRow(row({ type: "SELL", shares: "", price: "" }));
  assert.equal(result.status, "INVALID");
  assert.ok(result.errors.includes("Shares must be a positive number"));
  assert.ok(result.errors.includes("Price must be a positive number"));
});

test("extra columns in the CSV are ignored", () => {
  const text = `${HEADER},broker,account_id\n2026-08-10,BUY,PTT.BK,100,35,,note text,SET,ACC-1`;
  const parsed = parseCsv(text);
  assert.equal(parsed.ok, true);
  if (!parsed.ok) return;
  assert.equal(parsed.rows.length, 1);
  assert.equal(parsed.rows[0].symbol, "PTT.BK");
  assert.equal(parsed.rows[0].notes, "note text");
});

test("a quoted field with an embedded comma is parsed as a single value", () => {
  const text = `${HEADER}\n2026-08-10,BUY,PTT.BK,100,35,,"bought on dip, averaging down"`;
  const parsed = parseCsv(text);
  assert.equal(parsed.ok, true);
  if (!parsed.ok) return;
  assert.equal(parsed.rows.length, 1);
  assert.equal(parsed.rows[0].notes, "bought on dip, averaging down");
});

test("an escaped double quote inside a quoted field is unescaped", () => {
  const text = `${HEADER}\n2026-08-10,BUY,PTT.BK,100,35,,"broker said ""hold"" for now"`;
  const parsed = parseCsv(text);
  assert.equal(parsed.ok, true);
  if (!parsed.ok) return;
  assert.equal(parsed.rows[0].notes, 'broker said "hold" for now');
});

test("CRLF line endings parse the same rows as LF", () => {
  const text = `${HEADER}\r\n2026-08-10,BUY,AAA.BK,1,10,,\r\n2026-08-11,SELL,BBB.BK,1,10,,`;
  const parsed = parseCsv(text);
  assert.equal(parsed.ok, true);
  if (!parsed.ok) return;
  assert.deepEqual(parsed.rows.map((r) => r.symbol), ["AAA.BK", "BBB.BK"]);
});

test("UTF-8 Thai notes are preserved through parsing and payload building", () => {
  const text = `${HEADER}\n2026-08-10,BUY,PTT.BK,100,35,,ซื้อรอบแรก`;
  const parsed = parseCsv(text);
  assert.equal(parsed.ok, true);
  if (!parsed.ok) return;
  assert.equal(parsed.rows[0].notes, "ซื้อรอบแรก");

  const validated = validateRow(parsed.rows[0]);
  const built = buildImportPayload(validated);
  assert.equal(built.payload.notes, "ซื้อรอบแรก");
});

test("parseCsv rejects a file missing a required column", () => {
  const text = "date,type,symbol,shares,price,notes\n2026-08-10,BUY,PTT.BK,100,35,note";
  const parsed = parseCsv(text);
  assert.equal(parsed.ok, false);
  if (parsed.ok) return;
  assert.match(parsed.error, /amount/);
});

test("parseCsv rejects an empty file", () => {
  const parsed = parseCsv("");
  assert.equal(parsed.ok, false);
});

test("parseCsv rejects a header-only file with no data rows", () => {
  const parsed = parseCsv(HEADER);
  assert.equal(parsed.ok, false);
});

test("parseCsv preserves original row order and assigns 1-based row numbers", () => {
  const text = `${HEADER}\n2026-08-10,BUY,AAA.BK,1,10,,\n2026-08-11,SELL,BBB.BK,1,10,,`;
  const parsed = parseCsv(text);
  assert.equal(parsed.ok, true);
  if (!parsed.ok) return;
  assert.deepEqual(parsed.rows.map((r) => r.rowNumber), [1, 2]);
  assert.deepEqual(parsed.rows.map((r) => r.symbol), ["AAA.BK", "BBB.BK"]);
});

test("validateRows maps validateRow over every row independently", () => {
  const results = validateRows([row({ rowNumber: 1 }), row({ rowNumber: 2, symbol: "" })]);
  assert.equal(results[0].status, "VALID");
  assert.equal(results[1].status, "INVALID");
});

test("buildImportPayload throws for an invalid row", () => {
  const result = validateRow(row({ symbol: "" }));
  assert.throws(() => buildImportPayload(result));
});
