import { render, screen } from "@testing-library/react";
import { describe, expect, test, vi } from "vitest";
import DashboardPage from "@/app/page";
import type { Portfolio } from "@/lib/api";

// Section 4 of the Periodic Review Slice 1 contract: a small, obvious entry
// point from `/` to `/review`, and no cross-domain data fetch added to `/`
// merely to decorate the link (no count, no badge).
const { getHoldings, getPortfolioPrices, getTransactionHistory, getSnapshots, listCashAccounts, listLiabilities, getCashAccountBalanceAsOf, getLiabilityBalanceAsOf, getNetWorthChangeAttribution } =
  vi.hoisted(() => ({
    getHoldings: vi.fn(),
    getPortfolioPrices: vi.fn(),
    getTransactionHistory: vi.fn(),
    getSnapshots: vi.fn(),
    listCashAccounts: vi.fn(),
    listLiabilities: vi.fn(),
    getCashAccountBalanceAsOf: vi.fn(),
    getLiabilityBalanceAsOf: vi.fn(),
    getNetWorthChangeAttribution: vi.fn(),
  }));

vi.mock("@/lib/api", () => ({
  getHoldings,
  getPortfolioPrices,
  getTransactionHistory,
  getSnapshots,
  listCashAccounts,
  listLiabilities,
  getCashAccountBalanceAsOf,
  getLiabilityBalanceAsOf,
  getNetWorthChangeAttribution,
}));

const portfolioState = { portfolios: [] as Portfolio[], loading: false, error: null as string | null };
vi.mock("@/lib/PortfolioContext", () => ({ usePortfolio: () => portfolioState }));

describe("Dashboard Periodic Review entry point", () => {
  test("exposes a link to /review and fetches no review-domain data to build it", async () => {
    listCashAccounts.mockResolvedValue([]);
    listLiabilities.mockResolvedValue([]);

    render(<DashboardPage />);

    const link = await screen.findByRole("link", { name: /Periodic Review/i });
    expect(link).toHaveAttribute("href", "/review");

    // Goals/Execution/Evaluation domains belong to /review, not /.
    expect(getSnapshots).not.toHaveBeenCalled();
  });
});
