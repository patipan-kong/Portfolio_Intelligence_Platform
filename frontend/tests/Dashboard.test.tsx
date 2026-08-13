import { beforeEach, describe, expect, test, vi } from "vitest";
import { act, render, screen, waitFor } from "@testing-library/react";
import DashboardPage from "@/app/page";
import type { Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";

const { getHoldings, getPortfolioPrices, portfolioState } = vi.hoisted(() => ({
  getHoldings: vi.fn(),
  getPortfolioPrices: vi.fn(),
  portfolioState: {
    portfolios: [] as Portfolio[],
    loading: false,
  },
}));

vi.mock("@/lib/api", () => ({
  getHoldings,
  getPortfolioPrices,
}));

vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => portfolioState,
}));

function makePortfolio(id: number): Portfolio {
  return {
    id,
    name: `Portfolio ${id}`,
    cash_balance: 0,
    created_at: "2026-01-01T00:00:00Z",
  };
}

function makeHolding(portfolioId: number, id: number, symbol: string): PortfolioItem {
  return {
    id,
    portfolio_id: portfolioId,
    symbol,
    shares: 1,
    avg_cost: 1,
    current_price: null,
    previous_close: null,
    change_percent: null,
    last_updated: null,
    latest_signal: null,
    signal_confidence: null,
    analyzed_at: null,
    reasoning: null,
    risks: null,
    ta_score: null,
    fa_score: null,
    allow_swap: true,
    target_price: null,
    upside_pct: null,
    risk_level: null,
  };
}

function makeQuote(symbol: string, current: number, previous: number): PriceRefreshItem {
  return {
    symbol,
    current_price: current,
    previous_close: previous,
    change_percent: Number((((current - previous) / previous) * 100).toFixed(2)),
    last_updated: "2026-08-13T00:00:00Z",
  };
}

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((next) => { resolve = next; });
  return { promise, resolve };
}

beforeEach(() => {
  getHoldings.mockReset();
  getPortfolioPrices.mockReset();
  portfolioState.portfolios = [];
  portfolioState.loading = false;
});

describe("Dashboard pricing", () => {
  test("keeps each holding's current/previous-close quote pair when refresh rows arrive in another order", async () => {
    const portfolio = makePortfolio(1);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([
      makeHolding(portfolio.id, 1, "AAA"),
      makeHolding(portfolio.id, 2, "BBB"),
    ]);
    // Deliberately reverse the holdings order. Each quote's current price and
    // previous close must stay attached to its symbol.
    getPortfolioPrices.mockResolvedValue([
      makeQuote("BBB", 300, 150),
      makeQuote("AAA", 100, 80),
    ]);

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByRole("link", { name: /AAA/ })).toHaveTextContent("+25.00%");
      expect(screen.getByRole("link", { name: /BBB/ })).toHaveTextContent("+100.00%");
    });

    // The current prices also determine each tile's market-value weight.
    expect(screen.getByRole("link", { name: /AAA/ })).toHaveStyle({ flexBasis: "24.5%" });
    expect(screen.getByRole("link", { name: /BBB/ })).toHaveStyle({ flexBasis: "74.5%" });
  });

  test("ignores a late price response from a previous portfolio load", async () => {
    const first = makePortfolio(1);
    const second = makePortfolio(2);
    const firstPrices = deferred<PriceRefreshItem[]>();
    const secondPrices = deferred<PriceRefreshItem[]>();

    portfolioState.portfolios = [first];
    getHoldings.mockImplementation((portfolioId: number) => Promise.resolve([
      makeHolding(portfolioId, portfolioId, portfolioId === 1 ? "AAA" : "BBB"),
    ]));
    getPortfolioPrices.mockImplementation((portfolioId: number) => (
      portfolioId === 1 ? firstPrices.promise : secondPrices.promise
    ));

    const view = render(<DashboardPage />);
    await waitFor(() => expect(getPortfolioPrices).toHaveBeenCalledWith(first.id));

    portfolioState.portfolios = [second];
    view.rerender(<DashboardPage />);
    await waitFor(() => expect(getPortfolioPrices).toHaveBeenCalledWith(second.id));

    await act(async () => { secondPrices.resolve([makeQuote("BBB", 200, 100)]); });
    await waitFor(() => expect(screen.getByRole("link", { name: /BBB/ })).toHaveTextContent("+100.00%"));

    // The abandoned first request returns after the current portfolio has
    // rendered. It must not replace the current portfolio's quote map.
    await act(async () => { firstPrices.resolve([makeQuote("AAA", 999, 1)]); });

    expect(screen.getByRole("link", { name: /BBB/ })).toHaveTextContent("+100.00%");
    expect(screen.queryByRole("link", { name: /AAA/ })).not.toBeInTheDocument();
  });
});
