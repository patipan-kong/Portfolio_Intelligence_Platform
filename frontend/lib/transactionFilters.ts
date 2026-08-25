import type { TransactionRecord, TransactionType } from "@/lib/api";

export interface TransactionFilters {
  search: string;
  type: TransactionType | "ALL";
  from: string; // "YYYY-MM-DD" (Asia/Bangkok calendar date) or "" for no lower bound
  to: string;   // "YYYY-MM-DD" (Asia/Bangkok calendar date) or "" for no upper bound
}

export const DEFAULT_FILTERS: TransactionFilters = { search: "", type: "ALL", from: "", to: "" };

export function hasActiveFilters(filters: TransactionFilters): boolean {
  return filters.search.trim() !== "" || filters.type !== "ALL" || filters.from !== "" || filters.to !== "";
}

// Must agree with TransactionHistoryTable's display convention (also
// Asia/Bangkok, see its `TZ` constant) — otherwise a transaction timestamped
// between Bangkok midnight and 07:00 UTC would compare against a different
// calendar date than the one the row visibly shows, mirroring the bug
// previously found in Dividend Income's monthly grouping.
const DISPLAY_TZ = "Asia/Bangkok";
const dateKeyFormatter = new Intl.DateTimeFormat("en-US", {
  timeZone: DISPLAY_TZ,
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
});

export function bangkokDateKey(isoDate: string): string {
  const parts = dateKeyFormatter.formatToParts(new Date(isoDate));
  const year = parts.find((p) => p.type === "year")?.value ?? "0000";
  const month = parts.find((p) => p.type === "month")?.value ?? "00";
  const day = parts.find((p) => p.type === "day")?.value ?? "00";
  return `${year}-${month}-${day}`;
}

export function filterTransactions(
  transactions: TransactionRecord[],
  filters: TransactionFilters
): TransactionRecord[] {
  const query = filters.search.trim().toLowerCase();

  return transactions.filter((tx) => {
    if (query) {
      const symbolMatch = tx.symbol?.toLowerCase().includes(query) ?? false;
      const notesMatch = tx.notes?.toLowerCase().includes(query) ?? false;
      if (!symbolMatch && !notesMatch) return false;
    }

    if (filters.type !== "ALL" && tx.type !== filters.type) return false;

    if (filters.from || filters.to) {
      const key = bangkokDateKey(tx.transaction_date);
      if (filters.from && key < filters.from) return false;
      if (filters.to && key > filters.to) return false;
    }

    return true;
  });
}
