import type { TransactionRecord } from "@/lib/api";

export interface CurrencyTotal {
  currency: string;
  amount: number;
}

export interface AssetIncome {
  symbol: string | null; // null = dividend recorded without a symbol
  currency: string;
  amount: number;
  count: number;
}

export interface MonthlyIncome {
  month: string; // "YYYY-MM", from transaction_date
  currency: string;
  amount: number;
}

export interface DividendSummary {
  dividends: TransactionRecord[];
  totalsByCurrency: CurrencyTotal[];
  mixedCurrency: boolean;
  byAsset: AssetIncome[];
  byMonth: MonthlyIncome[];
  recent: TransactionRecord[];
}

export function filterDividends(transactions: TransactionRecord[]): TransactionRecord[] {
  return transactions.filter((tx) => tx.type === "DIVIDEND");
}

// Never summed across currencies — each currency gets its own total so a
// mixed-currency ledger can't silently misrepresent the amount received.
export function computeTotalsByCurrency(dividends: TransactionRecord[]): CurrencyTotal[] {
  const totals = new Map<string, number>();
  for (const tx of dividends) {
    totals.set(tx.currency, (totals.get(tx.currency) ?? 0) + tx.total_amount);
  }
  return Array.from(totals.entries())
    .map(([currency, amount]) => ({ currency, amount }))
    .sort((a, b) => b.amount - a.amount);
}

export function computeIncomeByAsset(dividends: TransactionRecord[]): AssetIncome[] {
  const totals = new Map<string, AssetIncome>();
  for (const tx of dividends) {
    // symbol is part of the grouping key (not just currency) so a null
    // symbol never gets merged into a real one, and different currencies
    // for the same symbol are kept apart too.
    const key = `${tx.symbol ?? ""}::${tx.currency}`;
    const existing = totals.get(key);
    if (existing) {
      existing.amount += tx.total_amount;
      existing.count += 1;
    } else {
      totals.set(key, { symbol: tx.symbol, currency: tx.currency, amount: tx.total_amount, count: 1 });
    }
  }
  return Array.from(totals.values()).sort((a, b) => b.amount - a.amount);
}

// Must agree with TransactionHistoryTable's display convention (also
// Asia/Bangkok, see its `TZ` constant) — otherwise a dividend timestamped
// between Bangkok midnight and 07:00 buckets into the *previous* UTC month
// here while the Recent Dividends list right below this chart shows it
// dated the next day/month, and the two disagree on the same page.
const DISPLAY_TZ = "Asia/Bangkok";
const monthKeyFormatter = new Intl.DateTimeFormat("en-US", {
  timeZone: DISPLAY_TZ,
  year: "numeric",
  month: "2-digit",
});

function monthKey(isoDate: string): string {
  const parts = monthKeyFormatter.formatToParts(new Date(isoDate));
  const year = parts.find((p) => p.type === "year")?.value ?? "0000";
  const month = parts.find((p) => p.type === "month")?.value ?? "00";
  return `${year}-${month}`;
}

export function computeMonthlyIncome(dividends: TransactionRecord[]): MonthlyIncome[] {
  const totals = new Map<string, MonthlyIncome>();
  for (const tx of dividends) {
    const month = monthKey(tx.transaction_date);
    const key = `${month}::${tx.currency}`;
    const existing = totals.get(key);
    if (existing) {
      existing.amount += tx.total_amount;
    } else {
      totals.set(key, { month, currency: tx.currency, amount: tx.total_amount });
    }
  }
  return Array.from(totals.values()).sort((a, b) => a.month.localeCompare(b.month));
}

export function sortRecentDividends(dividends: TransactionRecord[], limit = 10): TransactionRecord[] {
  return [...dividends]
    .sort((a, b) => new Date(b.transaction_date).getTime() - new Date(a.transaction_date).getTime())
    .slice(0, limit);
}

export function computeDividendSummary(transactions: TransactionRecord[], recentLimit = 10): DividendSummary {
  const dividends = filterDividends(transactions);
  const totalsByCurrency = computeTotalsByCurrency(dividends);
  return {
    dividends,
    totalsByCurrency,
    mixedCurrency: totalsByCurrency.length > 1,
    byAsset: computeIncomeByAsset(dividends),
    byMonth: computeMonthlyIncome(dividends),
    recent: sortRecentDividends(dividends, recentLimit),
  };
}
