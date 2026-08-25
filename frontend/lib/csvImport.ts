import type { BuyPayload, SellPayload, DepositPayload, WithdrawPayload, DividendPayload } from "@/lib/api";

// V1 CSV import supports only cash-flow-safe, unambiguous transaction types.
// INITIAL_POSITION / INITIAL_CASH / QUANTITY_CORRECTION / POSITION_CONVERSION
// carry accounting semantics (cost-basis seeding, non-cash-impact framing)
// that are easy to get wrong from a spreadsheet — those stay manual.
export type ImportTransactionType = "BUY" | "SELL" | "DIVIDEND" | "DEPOSIT" | "WITHDRAW";

export const SUPPORTED_TYPES: readonly ImportTransactionType[] = ["BUY", "SELL", "DIVIDEND", "DEPOSIT", "WITHDRAW"];

const REQUIRED_COLUMNS = ["date", "type", "symbol", "shares", "price", "amount", "notes"] as const;

export interface ImportRowInput {
  rowNumber: number; // 1-based, counting the first data row (header excluded)
  date: string;
  type: string;
  symbol: string;
  shares: string;
  price: string;
  amount: string;
  notes: string;
}

export type RowStatus = "VALID" | "INVALID";

export interface ParsedImportRow extends ImportRowInput {
  status: RowStatus;
  errors: string[];
  normalizedType?: ImportTransactionType;
  normalizedSymbol?: string | null;
  normalizedShares?: number | null;
  normalizedPrice?: number | null;
  normalizedAmount?: number | null;
}

export type CsvParseResult =
  | { ok: true; rows: ImportRowInput[] }
  | { ok: false; error: string };

// Minimal RFC4180-style split: handles quoted fields, embedded commas, and
// "" as an escaped quote. Does not support newlines embedded inside a quoted
// field — out of scope for V1 (see milestone section I).
function splitCsvLine(line: string): string[] {
  const fields: string[] = [];
  let cur = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (inQuotes) {
      if (ch === '"') {
        if (line[i + 1] === '"') {
          cur += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        cur += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ",") {
      fields.push(cur);
      cur = "";
    } else {
      cur += ch;
    }
  }
  fields.push(cur);
  return fields;
}

export function parseCsv(text: string): CsvParseResult {
  // Strip a UTF-8 BOM, which Excel commonly prepends to exported CSVs.
  const cleaned = text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
  const lines = cleaned.split(/\r\n|\r|\n/).filter((l) => l.trim() !== "");
  if (lines.length === 0) {
    return { ok: false, error: "File is empty." };
  }

  const headerFields = splitCsvLine(lines[0]).map((h) => h.trim().toLowerCase());
  const colIndex: Record<string, number> = {};
  headerFields.forEach((h, i) => {
    colIndex[h] = i;
  });

  const missing = REQUIRED_COLUMNS.filter((c) => !(c in colIndex));
  if (missing.length > 0) {
    return { ok: false, error: `Missing required column(s): ${missing.join(", ")}` };
  }

  const dataLines = lines.slice(1);
  if (dataLines.length === 0) {
    return { ok: false, error: "No transaction rows found in file." };
  }

  const rows: ImportRowInput[] = dataLines.map((line, idx) => {
    const fields = splitCsvLine(line);
    const get = (col: (typeof REQUIRED_COLUMNS)[number]) => (fields[colIndex[col]] ?? "").trim();
    return {
      rowNumber: idx + 1,
      date: get("date"),
      type: get("type"),
      symbol: get("symbol"),
      shares: get("shares"),
      price: get("price"),
      amount: get("amount"),
      notes: get("notes"),
    };
  });

  return { ok: true, rows };
}

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

function isValidDate(s: string): boolean {
  if (!DATE_RE.test(s)) return false;
  const [y, m, d] = s.split("-").map(Number);
  const parsed = new Date(Date.UTC(y, m - 1, d));
  // Date rolls invalid day/month combinations (e.g. 2026-02-30) forward —
  // comparing the parts back out catches that instead of silently accepting it.
  return parsed.getUTCFullYear() === y && parsed.getUTCMonth() === m - 1 && parsed.getUTCDate() === d;
}

function toNumberOrNull(raw: string): number | null {
  if (raw === "") return null;
  const n = Number(raw);
  return Number.isFinite(n) ? n : NaN; // NaN signals "present but not a number"
}

export function validateRow(input: ImportRowInput): ParsedImportRow {
  const errors: string[] = [];
  const rawType = input.type.trim().toUpperCase();
  const typeSupported = (SUPPORTED_TYPES as readonly string[]).includes(rawType);

  if (!rawType) {
    errors.push("Missing transaction type");
  } else if (!typeSupported) {
    errors.push(`Unsupported transaction type "${input.type.trim()}"`);
  }

  const dateTrimmed = input.date.trim();
  if (!dateTrimmed) {
    errors.push("Missing date");
  } else if (!isValidDate(dateTrimmed)) {
    errors.push("Invalid date (expected YYYY-MM-DD)");
  }

  const symbol = input.symbol.trim().toUpperCase();
  const shares = toNumberOrNull(input.shares.trim());
  const price = toNumberOrNull(input.price.trim());
  const amount = toNumberOrNull(input.amount.trim());

  if (Number.isNaN(shares)) errors.push("Shares is not a number");
  if (Number.isNaN(price)) errors.push("Price is not a number");
  if (Number.isNaN(amount)) errors.push("Amount is not a number");

  if (typeSupported) {
    if (rawType === "BUY" || rawType === "SELL") {
      if (!symbol) errors.push("Symbol is required");
      if (!(shares != null && !Number.isNaN(shares) && shares > 0)) errors.push("Shares must be a positive number");
      if (!(price != null && !Number.isNaN(price) && price > 0)) errors.push("Price must be a positive number");
    } else if (rawType === "DIVIDEND") {
      if (!(amount != null && !Number.isNaN(amount) && amount > 0)) errors.push("Amount must be a positive number");
    } else if (rawType === "DEPOSIT" || rawType === "WITHDRAW") {
      if (symbol) errors.push("Symbol is not allowed for DEPOSIT/WITHDRAW");
      if (!(amount != null && !Number.isNaN(amount) && amount > 0)) errors.push("Amount must be a positive number");
    }
  }

  const status: RowStatus = errors.length === 0 ? "VALID" : "INVALID";

  return {
    ...input,
    status,
    errors,
    ...(status === "VALID"
      ? {
          normalizedType: rawType as ImportTransactionType,
          normalizedSymbol: symbol || null,
          normalizedShares: shares,
          normalizedPrice: price,
          normalizedAmount: amount,
        }
      : {}),
  };
}

export function validateRows(rows: ImportRowInput[]): ParsedImportRow[] {
  return rows.map(validateRow);
}

export type ImportPayload =
  | { type: "BUY"; payload: BuyPayload }
  | { type: "SELL"; payload: SellPayload }
  | { type: "DIVIDEND"; payload: DividendPayload }
  | { type: "DEPOSIT"; payload: DepositPayload }
  | { type: "WITHDRAW"; payload: WithdrawPayload };

export function buildImportPayload(row: ParsedImportRow): ImportPayload {
  if (row.status !== "VALID" || !row.normalizedType) {
    throw new Error("Cannot build a payload for an invalid row");
  }
  const transaction_date = row.date.trim();
  const notes = row.notes.trim() || undefined;

  switch (row.normalizedType) {
    case "BUY":
      return {
        type: "BUY",
        payload: { symbol: row.normalizedSymbol!, shares: row.normalizedShares!, price_per_share: row.normalizedPrice!, transaction_date, notes },
      };
    case "SELL":
      return {
        type: "SELL",
        payload: {
          symbol: row.normalizedSymbol!,
          shares: row.normalizedShares!,
          price_per_share: row.normalizedPrice!,
          transaction_date,
          notes,
          remove_if_zero: true,
        },
      };
    case "DIVIDEND":
      return {
        type: "DIVIDEND",
        payload: { symbol: row.normalizedSymbol ?? undefined, amount: row.normalizedAmount!, transaction_date, notes },
      };
    case "DEPOSIT":
      return { type: "DEPOSIT", payload: { amount: row.normalizedAmount!, transaction_date, notes } };
    case "WITHDRAW":
      return { type: "WITHDRAW", payload: { amount: row.normalizedAmount!, transaction_date, notes } };
  }
}
