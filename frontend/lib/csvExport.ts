import type { TransactionRecord } from "@/lib/api";

// Bounded v1: exports exactly the fields already available on
// TransactionRecord (the same shape TransactionHistoryTable renders from).
// POSITION_CONVERSION's structured conversion_detail is intentionally left
// out of this schema — adding conversion-only columns would leave them empty
// for every other row type, and the milestone calls for the smaller, clearer
// contract. Realized P/L is not a field TransactionRecord exposes for
// ordinary transactions, so it is not fabricated here either.
const CSV_COLUMNS = ["Date", "Type", "Symbol", "Shares", "Price", "Total Amount", "Currency", "Fees", "Notes"] as const;

export function escapeCsvField(value: string | number | null | undefined): string {
  const s = value == null ? "" : String(value);
  if (/[",\n\r]/.test(s)) {
    return `"${s.replace(/"/g, '""')}"`;
  }
  return s;
}

function fmtNum(n: number | null | undefined): string {
  return n == null ? "" : String(n);
}

export function transactionsToCsv(transactions: TransactionRecord[]): string {
  const header = CSV_COLUMNS.join(",");
  const rows = transactions.map((tx) =>
    [
      tx.transaction_date,
      tx.type,
      tx.symbol ?? "",
      fmtNum(tx.shares),
      fmtNum(tx.price_per_share),
      fmtNum(tx.total_amount),
      tx.currency,
      fmtNum(tx.fees),
      tx.notes ?? "",
    ]
      .map(escapeCsvField)
      .join(",")
  );
  return [header, ...rows].join("\n");
}

// Prepended to the CSV Blob (not to the string transactionsToCsv() returns)
// so spreadsheet apps — Excel in particular — recognize UTF-8 and render Thai
// notes/symbols correctly. csvImport.ts's parseCsv() already strips this same
// BOM on the way back in, confirming it's an established project convention.
export const CSV_UTF8_BOM = String.fromCharCode(0xfeff);

const UNSAFE_FILENAME_CHARS = /[^a-zA-Z0-9-]+/g;

export function sanitizeFilenameFragment(raw: string): string {
  const cleaned = raw.trim().replace(UNSAFE_FILENAME_CHARS, "-").replace(/-+/g, "-").replace(/^-|-$/g, "");
  return cleaned || "portfolio";
}

export function buildExportFilename(portfolioName: string | null, isoDate: string): string {
  return `wealth-os-transactions-${sanitizeFilenameFragment(portfolioName ?? "portfolio")}-${isoDate}.csv`;
}
