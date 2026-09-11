import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, test, vi } from "vitest";
import NetWorthReviewSection from "@/components/review/NetWorthReviewSection";
import type { CashAccount, Liability, Portfolio, PortfolioSnapshotRow } from "@/lib/api";

// DOGFOOD-01 — Periodic Review Net Worth request fan-out regression.
//
// The original implementation fetched Cash/Liability As-Of evidence with
// one getCashAccountBalanceAsOf/getLiabilityBalanceAsOf call per
// (account, date) / (liability, date) pair — accounts x dates HTTP
// requests. It was replaced with one getCashAccountBalancesAsOf /
// getLiabilityBalancesAsOf call per domain, regardless of account or date
// count. These tests fail if that shape regresses, in either of the two
// ways it could: back to per-pair fan-out, or a memoization regression that
// makes the batch call itself re-fire on every render.

const {
  listCashAccounts,
  listLiabilities,
  getSnapshots,
  getCashAccountBalancesAsOf,
  getLiabilityBalancesAsOf,
  getNetWorthChangeAttribution,
} = vi.hoisted(() => ({
  listCashAccounts: vi.fn(),
  listLiabilities: vi.fn(),
  getSnapshots: vi.fn(),
  getCashAccountBalancesAsOf: vi.fn(),
  getLiabilityBalancesAsOf: vi.fn(),
  getNetWorthChangeAttribution: vi.fn(),
}));

vi.mock("@/lib/api", () => ({
  listCashAccounts,
  listLiabilities,
  getSnapshots,
  getCashAccountBalancesAsOf,
  getLiabilityBalancesAsOf,
  getNetWorthChangeAttribution,
}));

let portfolioState: {
  portfolios: Portfolio[];
  loading: boolean;
  error: string | null;
} = { portfolios: [], loading: false, error: null };
vi.mock("@/lib/PortfolioContext", () => ({ usePortfolio: () => portfolioState }));

function makePortfolio(id: number): Portfolio {
  return { id, name: `Portfolio ${id}`, cash_balance: 0, created_at: "2026-01-01T00:00:00Z" };
}

function makeCashAccount(id: number): CashAccount {
  return {
    id,
    workspace_id: 1,
    name: `Cash ${id}`,
    institution: null,
    currency: "THB",
    balance: 1000,
    is_archived: false,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
  };
}

function makeLiability(id: number): Liability {
  return {
    id,
    workspace_id: 1,
    name: `Liability ${id}`,
    liability_type: "OTHER",
    lender: null,
    balance: 500,
    currency: "THB",
    note: null,
    is_archived: false,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
  };
}

function makeSnapshots(portfolioId: number, dates: string[]): PortfolioSnapshotRow[] {
  return dates.map((snapshot_date, i) => ({
    id: portfolioId * 1000 + i,
    portfolio_id: portfolioId,
    snapshot_date,
    total_value: 10000 + i,
    cash_balance: 0,
    total_invested: 10000,
    unrealized_pnl: null,
    unrealized_pnl_pct: null,
    realized_pnl: null,
    daily_return_pct: null,
    investment_return_pct: null,
    investment_return_amount: null,
  })) as PortfolioSnapshotRow[];
}

const DATES = ["2026-08-01", "2026-08-02", "2026-08-03", "2026-08-04", "2026-08-05"];

beforeEach(() => {
  listCashAccounts.mockReset().mockResolvedValue([]);
  listLiabilities.mockReset().mockResolvedValue([]);
  getSnapshots.mockReset().mockResolvedValue([]);
  getCashAccountBalancesAsOf.mockReset().mockResolvedValue({});
  getLiabilityBalancesAsOf.mockReset().mockResolvedValue({});
  getNetWorthChangeAttribution
    .mockReset()
    .mockResolvedValue({ status: "UNAVAILABLE", start_date: "2026-08-01", end_date: "2026-08-05", reason_codes: [] });
  portfolioState = { portfolios: [], loading: false, error: null };
});

describe("NetWorthReviewSection request shape", () => {
  test("fetches Cash/Liability As-Of evidence via exactly one batch call each, not one per account/liability x date pair", async () => {
    portfolioState = { portfolios: [makePortfolio(1)], loading: false, error: null };
    listCashAccounts.mockResolvedValue([makeCashAccount(1), makeCashAccount(2), makeCashAccount(3)]);
    listLiabilities.mockResolvedValue([makeLiability(1), makeLiability(2)]);
    getSnapshots.mockResolvedValue(makeSnapshots(1, DATES));
    getCashAccountBalancesAsOf.mockResolvedValue({
      "1": Object.fromEntries(DATES.map((d) => [d, { balance: 100, available: true }])),
      "2": Object.fromEntries(DATES.map((d) => [d, { balance: 200, available: true }])),
      "3": Object.fromEntries(DATES.map((d) => [d, { balance: 300, available: true }])),
    });
    getLiabilityBalancesAsOf.mockResolvedValue({
      "1": Object.fromEntries(DATES.map((d) => [d, { balance: 50, available: true, currency: "THB" }])),
      "2": Object.fromEntries(DATES.map((d) => [d, { balance: 60, available: true, currency: "THB" }])),
    });

    render(<NetWorthReviewSection />);

    await waitFor(() => expect(getCashAccountBalancesAsOf).toHaveBeenCalled());
    await waitFor(() => expect(getLiabilityBalancesAsOf).toHaveBeenCalled());

    // Exactly one call per domain — never one per (account, date) or
    // (liability, date) pair (which would be 3*5=15 and 2*5=10 respectively
    // under the old fan-out).
    expect(getCashAccountBalancesAsOf).toHaveBeenCalledTimes(1);
    expect(getLiabilityBalancesAsOf).toHaveBeenCalledTimes(1);

    // The single call carries every history date and reads all accounts
    // (include_archived=true), not a per-account/per-date slice.
    const [datesArg, includeArchivedArg] = getCashAccountBalancesAsOf.mock.calls[0];
    expect(new Set(datesArg)).toEqual(new Set(DATES));
    expect(includeArchivedArg).toBe(true);
  });

  test("does not re-fire the batch calls on unrelated re-renders (memoized date spine)", async () => {
    portfolioState = { portfolios: [makePortfolio(1)], loading: false, error: null };
    listCashAccounts.mockResolvedValue([makeCashAccount(1)]);
    listLiabilities.mockResolvedValue([]);
    getSnapshots.mockResolvedValue(makeSnapshots(1, DATES));
    getCashAccountBalancesAsOf.mockResolvedValue({
      "1": Object.fromEntries(DATES.map((d) => [d, { balance: 100, available: true }])),
    });

    const { rerender } = render(<NetWorthReviewSection />);

    await waitFor(() => expect(getCashAccountBalancesAsOf).toHaveBeenCalledTimes(1));

    // Force several additional renders of the same component instance —
    // an unmemoized investmentHistoryDates array would give the fetch
    // effect a new reference each time and re-trigger the batch fetch.
    rerender(<NetWorthReviewSection />);
    rerender(<NetWorthReviewSection />);
    rerender(<NetWorthReviewSection />);

    // Give any wrongly-retriggered fetch a chance to resolve and re-render.
    await new Promise((resolve) => setTimeout(resolve, 20));

    expect(getCashAccountBalancesAsOf).toHaveBeenCalledTimes(1);
  });

  test("no cash accounts or liabilities: batch endpoints are never called", async () => {
    portfolioState = { portfolios: [makePortfolio(1)], loading: false, error: null };
    getSnapshots.mockResolvedValue(makeSnapshots(1, DATES));

    render(<NetWorthReviewSection />);

    await screen.findByText("Net Worth");
    await new Promise((resolve) => setTimeout(resolve, 20));

    expect(getCashAccountBalancesAsOf).not.toHaveBeenCalled();
    expect(getLiabilityBalancesAsOf).not.toHaveBeenCalled();
  });
});
