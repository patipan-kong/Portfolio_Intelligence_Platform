import { test, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, act } from "@testing-library/react";
import { PortfolioProvider, usePortfolio } from "@/lib/PortfolioContext";
import DividendIncomePage from "@/app/income/page";
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

vi.mock("next/navigation", () => ({
  usePathname: () => "/income",
}));

vi.mock("@/components/DividendMonthlyChart", () => ({
  default: () => <div data-testid="monthly-chart" />,
}));

function makePortfolio(id: number, name = `P${id}`): Portfolio {
  return { id, name, cash_balance: 0, created_at: "2026-01-01T00:00:00Z" };
}

function dividend(overrides: Partial<TransactionRecord> = {}): TransactionRecord {
  return {
    id: 1,
    portfolio_id: 1,
    symbol: "PTT.BK",
    type: "DIVIDEND",
    shares: null,
    price_per_share: null,
    total_amount: 250,
    fees: 0,
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
      <button onClick={() => selectPortfolio(2)}>select-B</button>
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
      <DividendIncomePage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  expect(getTransactionHistory).not.toHaveBeenCalled();
});

test("selecting a portfolio requests that portfolio's transaction history and renders its dividend income", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([dividend()]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <DividendIncomePage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());

  await act(async () => screen.getByText("select-A").click());

  expect(getTransactionHistory).toHaveBeenCalledWith(1, undefined, 500);
  // Total card + the single by-asset row both read the same amount.
  await waitFor(() => expect(screen.getAllByText("THB 250.00").length).toBe(2));
});

test("a portfolio with no dividends shows a clear empty state, not an error", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <DividendIncomePage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());

  await waitFor(() => expect(screen.getByText(/No dividend income recorded/)).toBeInTheDocument());
});

test("switching to a different portfolio requests and renders that portfolio's own income", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1), makePortfolio(2)]);
  getTransactionHistory.mockImplementation((portfolioId: number) =>
    Promise.resolve(portfolioId === 1 ? [dividend({ total_amount: 250 })] : [dividend({ total_amount: 999 })])
  );

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <DividendIncomePage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());

  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(screen.getAllByText("THB 250.00").length).toBe(2));

  await act(async () => screen.getByText("select-B").click());
  expect(getTransactionHistory).toHaveBeenCalledWith(2, undefined, 500);
  await waitFor(() => expect(screen.getAllByText("THB 999.00").length).toBe(2));
  expect(screen.queryByText("THB 250.00")).not.toBeInTheDocument();
});

test("a late response for an abandoned portfolio does not repopulate the page after clearing selection", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  let resolve!: (v: TransactionRecord[]) => void;
  const pending = new Promise<TransactionRecord[]>((r) => (resolve = r));
  getTransactionHistory.mockReturnValue(pending);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <DividendIncomePage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());

  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(getTransactionHistory).toHaveBeenCalledWith(1, undefined, 500));

  await act(async () => screen.getByText("clear").click());
  expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument();

  await act(async () => resolve([dividend()]));
  expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument();
});
