import type { CashFlowEvent } from "./api";

const MONTH_PATTERN = /^(\d{4})-(0[1-9]|1[0-2])$/;
const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

export interface CashFlowSummary {
  month: string;
  income: number;
  expenses: number;
  netCashFlow: number;
  adjustments: number;
  eventCount: number;
  events: CashFlowEvent[];
  expenseCategories: Record<string, number>;
  incomeCategories: Record<string, number>;
}

function parseMonth(month: string): { year: number; month: number } {
  const match = MONTH_PATTERN.exec(month);
  if (!match) throw new Error("month must use YYYY-MM calendar format");
  return { year: Number(match[1]), month: Number(match[2]) };
}

function daysInMonth(year: number, month: number): number {
  // UTC is used only for deterministic calendar arithmetic; no event date is
  // converted from a timestamp or interpreted in a timezone.
  return new Date(Date.UTC(year, month, 0)).getUTCDate();
}

function monthBounds(month: string): { start: string; end: string } {
  const parsed = parseMonth(month);
  return {
    start: `${month}-01`,
    end: `${month}-${String(daysInMonth(parsed.year, parsed.month)).padStart(2, "0")}`,
  };
}

function roundCurrency(value: number): number {
  return Number(value.toFixed(2));
}

function eventSignedAmount(event: CashFlowEvent): number {
  if (event.transaction_type === "INCOME") return Math.abs(event.amount);
  if (event.transaction_type === "EXPENSE") return -Math.abs(event.amount);
  return Number.isFinite(event.signed_amount) ? event.signed_amount : event.amount;
}

function addCategory(target: Record<string, number>, category: string, amount: number): void {
  const label = category.trim() || "Uncategorized";
  target[label] = roundCurrency((target[label] ?? 0) + amount);
}

/**
 * Aggregate only the selected calendar month from normalized ledger events.
 * Baselines are not represented in CashFlowEvent, and ADJUSTMENT rows remain
 * visible in `events` while being excluded from all economic flow totals.
 */
export function aggregateMonthlyCashFlow(events: CashFlowEvent[], month: string): CashFlowSummary {
  const { start, end } = monthBounds(month);
  const selected = events
    .filter((event) => event.occurred_on >= start && event.occurred_on <= end)
    .slice()
    .sort((a, b) => b.occurred_on.localeCompare(a.occurred_on) || b.id - a.id);

  let income = 0;
  let expenses = 0;
  let adjustments = 0;
  const expenseCategories: Record<string, number> = {};
  const incomeCategories: Record<string, number> = {};

  for (const event of selected) {
    if (event.transaction_type === "INCOME") {
      income += Math.abs(event.amount);
      addCategory(incomeCategories, event.category, Math.abs(event.amount));
    } else if (event.transaction_type === "EXPENSE") {
      expenses += Math.abs(event.amount);
      addCategory(expenseCategories, event.category, Math.abs(event.amount));
    } else if (event.transaction_type === "ADJUSTMENT") {
      adjustments += eventSignedAmount(event);
    }
  }

  const roundedIncome = roundCurrency(income);
  const roundedExpenses = roundCurrency(expenses);
  return {
    month,
    income: roundedIncome,
    expenses: roundedExpenses,
    netCashFlow: roundCurrency(roundedIncome - roundedExpenses),
    adjustments: roundCurrency(adjustments),
    eventCount: selected.length,
    events: selected,
    expenseCategories,
    incomeCategories,
  };
}

export function currentMonthKey(now = new Date()): string {
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
}

export function shiftMonth(month: string, delta: number): string {
  const parsed = parseMonth(month);
  const absolute = parsed.year * 12 + parsed.month - 1 + delta;
  const year = Math.floor(absolute / 12);
  const monthNumber = (absolute % 12) + 1;
  return `${year}-${String(monthNumber).padStart(2, "0")}`;
}

export function formatMonthLabel(month: string): string {
  const parsed = parseMonth(month);
  return `${MONTH_NAMES[parsed.month - 1]} ${parsed.year}`;
}

export function signedPresentationAmount(event: CashFlowEvent): number {
  return eventSignedAmount(event);
}
