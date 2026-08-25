import { beforeEach, describe, expect, test, vi } from "vitest";
import { act, render, screen, waitFor } from "@testing-library/react";
import DashboardPage from "@/app/page";
import type { Portfolio, PortfolioItem, PriceRefreshItem, TransactionRecord } from "@/lib/api";

const { getHoldings, getPortfolioPrices, getTransactionHistory, portfolioState } = vi.hoisted(() => ({
  getHoldings: vi.fn(),
  getPortfolioPrices: vi.fn(),
  getTransactionHistory: vi.fn(),
  portfolioState: {
    portfolios: [] as Portfolio[],
    loading: false,
  },
}));

vi.mock("@/lib/api", () => ({
  getHoldings,
  getPortfolioPrices,
  getTransactionHistory,
}));

vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => portfolioState,
}));

function makePortfolio(id: number, cash_balance = 0): Portfolio {
  return {
    id,
    name: `Portfolio ${id}`,
    cash_balance,
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

function dividend(portfolioId: number, id: number, amount: number, date = "2026-06-01T00:00:00Z"): TransactionRecord {
  return {
    id,
    portfolio_id: portfolioId,
    symbol: "AAA",
    type: "DIVIDEND",
    shares: null,
    price_per_share: null,
    total_amount: amount,
    fees: 0,
    taxes: 0,
    currency: "THB",
    exchange_rate: 1,
    transaction_date: date,
    notes: null,
    sector: null,
    created_at: null,
  };
}

beforeEach(() => {
  getHoldings.mockReset();
  getPortfolioPrices.mockReset();
  getTransactionHistory.mockReset();
  getTransactionHistory.mockResolvedValue([]);
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

  test("one portfolio's holdings request failing does not block the others from loading", async () => {
    const good = makePortfolio(1, 100);
    const broken = makePortfolio(2, 5000);
    portfolioState.portfolios = [good, broken];
    getHoldings.mockImplementation((portfolioId: number) =>
      portfolioId === good.id
        ? Promise.resolve([makeHolding(good.id, 1, "AAA")])
        : Promise.reject(new Error("backend unavailable"))
    );
    getPortfolioPrices.mockImplementation((portfolioId: number) =>
      portfolioId === good.id ? Promise.resolve([makeQuote("AAA", 10, 10)]) : Promise.resolve([])
    );

    render(<DashboardPage />);

    // The healthy portfolio's holding still renders in the heatmap.
    await waitFor(() => expect(screen.getByRole("link", { name: /AAA/ })).toBeInTheDocument());

    // Wealth Overview reflects only the portfolio it could load — the
    // broken one's much larger value is never silently counted as 0. Both
    // the Total Wealth card and the healthy portfolio's own card read
    // 110.00, since it's the only portfolio counted in the total. Wait for
    // the live price (Phase 2) to land, not just holdings (Phase 1).
    await waitFor(() => expect(screen.getAllByText("฿110.00").length).toBe(2));
    expect(screen.getByText(/Excludes 1 portfolio that failed to load/)).toBeInTheDocument();
  });

  test("marks a tile with a stale-price indicator when its live quote came from an expired-cache fallback", async () => {
    const portfolio = makePortfolio(1);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([
      { ...makeQuote("AAA", 100, 80), is_stale: true },
    ]);

    render(<DashboardPage />);

    await waitFor(() => {
      const tile = screen.getByRole("link", { name: /AAA/ });
      expect(tile).toHaveAttribute("title", "Live price unavailable; showing the last cached price.");
    });
    // The numeric price signal (Day%) is still shown alongside the cue — a
    // stale price is not hidden or treated as an error/no-data state.
    expect(screen.getByRole("link", { name: /AAA/ })).toHaveTextContent("+25.00%");
  });

  test("does not mark a tile stale when its live quote is fresh", async () => {
    const portfolio = makePortfolio(1);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([makeQuote("AAA", 100, 80)]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByRole("link", { name: /AAA/ })).toHaveTextContent("+25.00%"));
    expect(screen.getByRole("link", { name: /AAA/ })).not.toHaveAttribute("title");
  });
});

describe("Cross-portfolio dividend income", () => {
  test("aggregates dividend income from multiple portfolios into one total with per-portfolio contribution", async () => {
    const p1 = makePortfolio(1);
    const p2 = makePortfolio(2);
    portfolioState.portfolios = [p1, p2];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getTransactionHistory.mockImplementation((portfolioId: number) =>
      Promise.resolve(portfolioId === 1 ? [dividend(1, 1, 100)] : [dividend(2, 2, 50)])
    );

    render(<DashboardPage />);

    // The combined total appears in more than one summary figure (all-time,
    // this-year, trailing-12-months all agree for such recent dividends).
    await waitFor(() => expect(screen.getAllByText("THB 150.00").length).toBeGreaterThan(0));
    // Per-portfolio contribution breakdown — each figure is unique to its row.
    expect(screen.getByText("THB 100.00")).toBeInTheDocument();
    expect(screen.getByText("THB 50.00")).toBeInTheDocument();
  });

  test("a portfolio with no dividend transactions contributes zero without an error", async () => {
    const p1 = makePortfolio(1);
    const p2 = makePortfolio(2);
    portfolioState.portfolios = [p1, p2];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getTransactionHistory.mockImplementation((portfolioId: number) =>
      Promise.resolve(portfolioId === 1 ? [dividend(1, 1, 100)] : [])
    );

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getAllByText("THB 100.00").length).toBeGreaterThan(0));
    expect(screen.queryByText(/Excludes/)).not.toBeInTheDocument();
  });

  test("no portfolios have any dividends shows a graceful empty state, not an error", async () => {
    const p1 = makePortfolio(1);
    portfolioState.portfolios = [p1];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getTransactionHistory.mockResolvedValue([]);

    render(<DashboardPage />);

    await waitFor(() =>
      expect(screen.getByText(/No dividend income recorded across your portfolios yet/)).toBeInTheDocument()
    );
  });

  test("one portfolio's transaction request failing does not fabricate a total and is reported honestly", async () => {
    const good = makePortfolio(1);
    const broken = makePortfolio(2);
    portfolioState.portfolios = [good, broken];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getTransactionHistory.mockImplementation((portfolioId: number) =>
      portfolioId === good.id
        ? Promise.resolve([dividend(good.id, 1, 100)])
        : Promise.reject(new Error("backend unavailable"))
    );

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getAllByText("THB 100.00").length).toBeGreaterThan(0));
    expect(screen.getByText(/Excludes 1 portfolio that failed to load/)).toBeInTheDocument();
  });

  test("a stale response from a previous portfolio set does not overwrite the current one's income figures", async () => {
    const first = makePortfolio(1);
    const second = makePortfolio(2);
    const firstTx = deferred<TransactionRecord[]>();
    const secondTx = deferred<TransactionRecord[]>();

    portfolioState.portfolios = [first];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getTransactionHistory.mockImplementation((portfolioId: number) => (
      portfolioId === 1 ? firstTx.promise : secondTx.promise
    ));

    const view = render(<DashboardPage />);
    await waitFor(() => expect(getTransactionHistory).toHaveBeenCalledWith(first.id, undefined, 500));

    portfolioState.portfolios = [second];
    view.rerender(<DashboardPage />);
    await waitFor(() => expect(getTransactionHistory).toHaveBeenCalledWith(second.id, undefined, 500));

    await act(async () => { secondTx.resolve([dividend(2, 2, 200)]); });
    await waitFor(() => expect(screen.getAllByText("THB 200.00").length).toBeGreaterThan(0));

    // The abandoned first request resolves after the second portfolio has
    // already rendered its own figures — it must not replace them.
    await act(async () => { firstTx.resolve([dividend(1, 1, 999999)]); });

    expect(screen.getAllByText("THB 200.00").length).toBeGreaterThan(0);
    expect(screen.queryByText(/999,999/)).not.toBeInTheDocument();
  });
});
