import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, act } from "@testing-library/react";
import { PortfolioProvider, usePortfolio } from "@/lib/PortfolioContext";
import TransactionHistoryPage from "@/app/history/page";
import type { Portfolio, TransactionRecord } from "@/lib/api";

const { listPortfolios, createPortfolio, deletePortfolio, getTransactionHistory, isUnresolvedPortfolioError } =
  vi.hoisted(() => ({
    listPortfolios: vi.fn(),
    createPortfolio: vi.fn(),
    deletePortfolio: vi.fn(),
    getTransactionHistory: vi.fn(),
    isUnresolvedPortfolioError: vi.fn(() => false),
  }));

vi.mock("@/lib/api", () => ({
  listPortfolios,
  createPortfolio,
  deletePortfolio,
  getTransactionHistory,
  isUnresolvedPortfolioError,
}));

// PortfolioTabs (rendered by this page) reads the current route via
// usePathname(), which next/navigation returns as null outside of an actual
// App Router — this test isn't exercising routing, so a fixed path is enough.
vi.mock("next/navigation", () => ({
  usePathname: () => "/history",
}));

function makePortfolio(id: number, name = `P${id}`): Portfolio {
  return { id, name, cash_balance: 0, created_at: "2026-01-01T00:00:00Z" };
}

function tx(overrides: Partial<TransactionRecord> = {}): TransactionRecord {
  return {
    id: 1,
    portfolio_id: 1,
    symbol: "PTT.BK",
    type: "BUY",
    shares: 100,
    price_per_share: 35,
    total_amount: 3500,
    fees: 5.5,
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

function SwitcherProbe() {
  const { selectPortfolio, clearSelection } = usePortfolio();
  return (
    <div>
      <button onClick={() => selectPortfolio(1)}>select-A</button>
      <button onClick={() => clearSelection()}>clear</button>
    </div>
  );
}

beforeEach(() => {
  localStorage.clear();
  listPortfolios.mockReset();
  getTransactionHistory.mockReset();
});

test("no portfolio selected: shows the empty/selection state and issues no request", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  expect(getTransactionHistory).not.toHaveBeenCalled();
});

test("selecting a portfolio requests that portfolio's transaction history and renders it", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([tx()]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());

  await act(async () => screen.getByText("select-A").click());

  expect(getTransactionHistory).toHaveBeenCalledWith(1);
  await waitFor(() => expect(screen.getAllByText("Buy").length).toBeGreaterThan(0));
  expect(screen.getAllByText("PTT").length).toBeGreaterThan(0);
});

test("a portfolio with no transactions shows a clear empty state, not an error", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());

  await waitFor(() => expect(screen.getByText(/No transactions recorded/)).toBeInTheDocument());
});

test("a late response for an abandoned portfolio does not repopulate the page after clearing selection", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  let resolve!: (v: TransactionRecord[]) => void;
  const pending = new Promise<TransactionRecord[]>((r) => (resolve = r));
  getTransactionHistory.mockReturnValue(pending);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());

  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(getTransactionHistory).toHaveBeenCalledWith(1));

  await act(async () => screen.getByText("clear").click());
  expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument();

  await act(async () => resolve([tx()]));
  expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument();
});
