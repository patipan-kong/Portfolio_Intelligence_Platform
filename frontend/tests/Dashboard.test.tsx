import { beforeEach, describe, expect, test, vi } from "vitest";
import { act, render, screen, waitFor } from "@testing-library/react";
import DashboardPage from "@/app/page";
import type { CashAccount, Liability, Portfolio, PortfolioItem, PriceRefreshItem, TransactionRecord, PortfolioSnapshotRow } from "@/lib/api";

const { getHoldings, getPortfolioPrices, getTransactionHistory, getSnapshots, listCashAccounts, listLiabilities, portfolioState } = vi.hoisted(() => ({
  getHoldings: vi.fn(),
  getPortfolioPrices: vi.fn(),
  getTransactionHistory: vi.fn(),
  getSnapshots: vi.fn(),
  listCashAccounts: vi.fn(),
  listLiabilities: vi.fn(),
  portfolioState: {
    portfolios: [] as Portfolio[],
    loading: false,
    error: null as string | null,
  },
}));

vi.mock("@/lib/api", () => ({
  getHoldings,
  getPortfolioPrices,
  getTransactionHistory,
  getSnapshots,
  listCashAccounts,
  listLiabilities,
}));

vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => portfolioState,
}));

// The wealth-history chart is a recharts component behind next/dynamic — its
// own rendering isn't this suite's concern (recharts tests itself, same
// convention as DividendMonthlyChart in DividendIncomeView.test.tsx); what
// matters here is that CrossPortfolioWealthHistory computes and surfaces the
// right summary figures and coverage state.
vi.mock("@/components/WealthHistoryChart", () => ({
  default: ({ points }: { points: Array<{ date: string; totalValue: number }> }) => (
    <div data-testid="wealth-history-chart">{points.map((p) => `${p.date}=${p.totalValue}`).join(",")}</div>
  ),
}));

// Same convention as the WealthHistoryChart mock above — this suite cares
// that CrossPortfolioWealthHistory computes and surfaces the right combined
// performance figures and coverage state, not recharts' own rendering.
vi.mock("@/components/CombinedPerformanceChart", () => ({
  default: ({ points }: { points: Array<{ date: string; cumulativeReturnPct: number }> }) => (
    <div data-testid="combined-performance-chart">
      {points.map((p) => `${p.date}=${p.cumulativeReturnPct}`).join(",")}
    </div>
  ),
}));

function makePortfolio(id: number, cash_balance = 0): Portfolio {
  return {
    id,
    name: `Portfolio ${id}`,
    cash_balance,
    created_at: "2026-01-01T00:00:00Z",
  };
}

function makeCashAccount(id: number, balance: number, overrides: Partial<CashAccount> = {}): CashAccount {
  return {
    id,
    workspace_id: 1,
    name: `Cash ${id}`,
    institution: null,
    currency: "THB",
    balance,
    is_archived: false,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
    ...overrides,
  };
}

function makeLiability(id: number, balance: number, overrides: Partial<Liability> = {}): Liability {
  return {
    id,
    workspace_id: 1,
    name: `Liability ${id}`,
    liability_type: "OTHER",
    lender: null,
    balance,
    currency: "THB",
    note: null,
    is_archived: false,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
    ...overrides,
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

function snapshot(portfolioId: number, date: string, totalValue: number): PortfolioSnapshotRow {
  return {
    id: portfolioId * 1000 + date.replace(/-/g, "").length,
    portfolio_id: portfolioId,
    snapshot_date: date,
    total_value: totalValue,
    cash_balance: 0,
    total_invested: 0,
    unrealized_pnl: null,
    unrealized_pnl_pct: null,
    realized_pnl: null,
    daily_return_pct: null,
    investment_return_pct: null,
    investment_return_amount: null,
    net_external_cash_flow: null,
    imported_asset_value: null,
    manual_adjustment_value: null,
    period_realized_pnl: null,
    period_dividend_income: null,
    period_fees_paid: null,
    holdings_count: null,
    sector_breakdown: null,
    holdings: null,
    created_at: null,
  };
}

// beginningNav/gain fully determine the row's eligibility and weight — see
// frontend/lib/combinedPerformance.ts's own eligibleObservation() for the
// algebraic inversion this fixture's total_value must satisfy.
function perfSnapshot(
  portfolioId: number,
  date: string,
  opts: { beginningNav?: number; gain?: number | null; netExternalCashFlow?: number }
): PortfolioSnapshotRow {
  const { beginningNav = 1000, gain = 0, netExternalCashFlow = 0 } = opts;
  const totalValue = gain == null ? beginningNav : beginningNav + gain + netExternalCashFlow;
  return {
    ...snapshot(portfolioId, date, totalValue),
    investment_return_amount: gain,
    investment_return_pct: gain == null ? null : (gain / beginningNav) * 100,
    net_external_cash_flow: netExternalCashFlow,
  };
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
  getSnapshots.mockReset();
  getSnapshots.mockResolvedValue([]);
  listCashAccounts.mockReset();
  listCashAccounts.mockResolvedValue([]);
  listLiabilities.mockReset();
  listLiabilities.mockResolvedValue([]);
  portfolioState.portfolios = [];
  portfolioState.loading = false;
  portfolioState.error = null;
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
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿200.00"));

    // The abandoned first request returns after the current portfolio has
    // rendered. It must not replace the current portfolio's quote map.
    await act(async () => { firstPrices.resolve([makeQuote("AAA", 999, 1)]); });

    expect(screen.getByRole("link", { name: /BBB/ })).toHaveTextContent("+100.00%");
    expect(screen.queryByRole("link", { name: /AAA/ })).not.toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿200.00"));
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
    // The healthy portfolio card still shows its known value, but the current
    // Investment Assets/Total Assets headline remains unavailable because one
    // required portfolio failed. Wait for the live price phase to settle.
    await waitFor(() => expect(screen.getAllByText("฿110.00").length).toBe(1));
    expect(screen.getByText(/Investment Assets unavailable/)).toBeInTheDocument();
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

describe("Dashboard current assets and external cash", () => {
  test("fetches active cash accounts and adds external cash exactly once", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([makeQuote("AAA", 900, 800)]);
    listCashAccounts.mockResolvedValue([makeCashAccount(1, 200)]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getAllByText("฿1,200.00").length).toBeGreaterThanOrEqual(2));
    expect(listCashAccounts).toHaveBeenCalledWith(false);
    expect(screen.getByText("Investment Assets")).toBeInTheDocument();
    expect(screen.getByText("External Cash")).toBeInTheDocument();
    expect(screen.getByText("Total Assets")).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿1,200.00"));
    expect(screen.getByText("฿200.00")).toBeInTheDocument();
    // Portfolio brokerage cash is already part of Investment Assets (100 + 900).
    expect(screen.queryByText("฿1,300.00")).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Manage Cash Accounts/ })).toHaveAttribute("href", "/cash");
  });

  test("zero external cash keeps Total Assets equal to Investment Assets", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([makeQuote("AAA", 900, 800)]);
    listCashAccounts.mockResolvedValue([]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getAllByText("฿1,000.00").length).toBeGreaterThanOrEqual(2));
    expect(screen.getByText("External Cash").parentElement).toHaveTextContent("฿0.00");
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿1,000.00"));
    expect(screen.queryByText("฿1,200.00")).not.toBeInTheDocument();
  });

  test("no portfolios is a valid empty Investment Core and cash becomes the total", async () => {
    portfolioState.portfolios = [];
    listCashAccounts.mockResolvedValue([makeCashAccount(1, 350)]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getAllByText("฿350.00").length).toBe(3));
    expect(screen.getByText("Investment Assets").parentElement).toHaveTextContent("฿0.00");
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿350.00"));
    expect(screen.getByText(/No portfolios yet/)).toBeInTheDocument();
    expect(screen.queryByText("Unavailable")).not.toBeInTheDocument();
  });

  test("archived cash rows never contribute to Total Assets", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([makeQuote("AAA", 900, 800)]);
    listCashAccounts.mockResolvedValue([
      makeCashAccount(1, 200),
      makeCashAccount(2, 999, { is_archived: true }),
    ]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getAllByText("฿1,200.00").length).toBeGreaterThanOrEqual(2));
    expect(screen.queryByText("฿2,199.00")).not.toBeInTheDocument();
  });

  test("cash failure shows known investment assets but prevents a Total Assets claim", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([makeQuote("AAA", 900, 800)]);
    listCashAccounts.mockRejectedValue(new Error("cash backend unavailable"));

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText(/Cash Accounts unavailable — Total Assets cannot be calculated/)).toBeInTheDocument());
    await waitFor(() => expect(screen.getAllByText("฿1,000.00").length).toBeGreaterThanOrEqual(2));
    expect(screen.getAllByText("Unavailable").length).toBe(3);
    expect(screen.queryByText("฿1,200.00")).not.toBeInTheDocument();
  });

  test("investment failure shows known cash but prevents a Total Assets claim", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockRejectedValue(new Error("investment backend unavailable"));
    getPortfolioPrices.mockResolvedValue([]);
    listCashAccounts.mockResolvedValue([makeCashAccount(1, 200)]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText(/Investment Assets unavailable/)).toBeInTheDocument());
    expect(screen.getByText("฿200.00")).toBeInTheDocument();
    expect(screen.getAllByText("Unavailable").length).toBe(3);
    expect(screen.queryByText("฿200.00")).not.toBeNull();
  });

  test("malformed non-THB cash is not silently summed", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([makeQuote("AAA", 900, 800)]);
    listCashAccounts.mockResolvedValue([
      makeCashAccount(1, 200, { currency: "USD" as CashAccount["currency"] }),
    ]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText(/Cash Accounts unavailable — Total Assets cannot be calculated/)).toBeInTheDocument());
    expect(screen.queryByText("฿1,200.00")).not.toBeInTheDocument();
    expect(screen.queryByText("฿200.00")).not.toBeInTheDocument();
  });

  test("Cash Accounts do not alter investment history or combined performance", async () => {
    const portfolio = makePortfolio(1, 0);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    listCashAccounts.mockResolvedValue([makeCashAccount(1, 999)]);
    getSnapshots.mockResolvedValue([
      perfSnapshot(portfolio.id, "2026-06-01", { beginningNav: 1000, gain: 100 }),
      perfSnapshot(portfolio.id, "2026-06-02", { beginningNav: 1100, gain: 0 }),
    ]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByTestId("wealth-history-chart")).toBeInTheDocument());
    expect(screen.getByText("Investment Wealth History")).toBeInTheDocument();
    expect(screen.getByTestId("wealth-history-chart")).toHaveTextContent("2026-06-01=1100");
    expect(screen.getByText("+10.00%")).toBeInTheDocument();
    expect(screen.queryByText("฿2,099.00")).not.toBeInTheDocument();
  });

  test("a late cash response cannot overwrite a newer context fetch", async () => {
    const first = makePortfolio(1);
    const second = makePortfolio(2);
    const firstCash = deferred<CashAccount[]>();
    const secondCash = deferred<CashAccount[]>();

    portfolioState.portfolios = [first];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    listCashAccounts
      .mockImplementationOnce(() => firstCash.promise)
      .mockImplementationOnce(() => secondCash.promise);

    const view = render(<DashboardPage />);
    await waitFor(() => expect(listCashAccounts).toHaveBeenCalledWith(false));

    portfolioState.portfolios = [second];
    view.rerender(<DashboardPage />);
    await waitFor(() => expect(listCashAccounts).toHaveBeenCalledTimes(2));

    await act(async () => { secondCash.resolve([makeCashAccount(2, 200)]); });
    await waitFor(() => expect(screen.getAllByText("฿200.00").length).toBe(3));
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿200.00"));

    await act(async () => { firstCash.resolve([makeCashAccount(1, 999)]); });
    expect(screen.getAllByText("฿200.00").length).toBe(3);
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿200.00"));
    expect(screen.queryByText("฿999.00")).not.toBeInTheDocument();
  });
});

describe("Dashboard current liabilities", () => {
  test("fetches active liabilities and aggregates multiple observed balances exactly once", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([makeQuote("AAA", 900, 800)]);
    listCashAccounts.mockResolvedValue([makeCashAccount(1, 200)]);
    listLiabilities.mockResolvedValue([makeLiability(1, 125), makeLiability(2, 75)]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText("Total Liabilities").parentElement).toHaveTextContent("฿200.00"));
    expect(listLiabilities).toHaveBeenCalledWith(false);
    expect(screen.getByText("Total Liabilities")).toBeInTheDocument();
    expect(screen.getByText("Total Liabilities").parentElement).toHaveTextContent("฿200.00");
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿1,000.00"));
    // Total Assets remains investment assets (1,000) plus external cash (200),
    // and never subtracts or double-adds the liability balance.
    await waitFor(() => expect(screen.getByText("Total Assets").parentElement).toHaveTextContent("฿1,200.00"));
    expect(screen.queryByText("฿2,200.00")).not.toBeInTheDocument();
  });

  test("successful empty active response shows zero, distinct from a failure", async () => {
    portfolioState.portfolios = [];
    listLiabilities.mockResolvedValue([]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText("Total Liabilities")).toBeInTheDocument());
    expect(screen.getByText("Total Liabilities").parentElement).toHaveTextContent("฿0.00");
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿0.00"));
    expect(screen.queryByText(/Liabilities unavailable/)).not.toBeInTheDocument();
  });

  test("a liability-only workspace produces a negative current Net Worth", async () => {
    portfolioState.portfolios = [];
    listCashAccounts.mockResolvedValue([]);
    listLiabilities.mockResolvedValue([makeLiability(1, 400)]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿-400.00"));
    expect(screen.getByText("Total Assets").parentElement).toHaveTextContent("฿0.00");
    expect(screen.getByText("Total Liabilities").parentElement).toHaveTextContent("฿400.00");
  });

  test("zero-balance active rows remain a known zero and archived rows do not contribute", async () => {
    portfolioState.portfolios = [];
    listLiabilities.mockResolvedValue([
      makeLiability(1, 0),
      makeLiability(2, 999_999, { is_archived: true }),
    ]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText("Total Liabilities")).toBeInTheDocument());
    expect(screen.getByText("Total Liabilities").parentElement).toHaveTextContent("฿0.00");
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿0.00"));
    expect(screen.queryByText("฿999,999.00")).not.toBeInTheDocument();
  });

  test("liability failure shows unavailable without invalidating known asset figures", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([makeQuote("AAA", 900, 800)]);
    listCashAccounts.mockResolvedValue([makeCashAccount(1, 200)]);
    listLiabilities.mockRejectedValue(new Error("liability backend unavailable"));

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText(/Liabilities unavailable/)).toBeInTheDocument());
    await waitFor(() => expect(screen.getByText("Total Assets").parentElement).toHaveTextContent("฿1,200.00"));
    const metric = screen.getByText("Total Liabilities").parentElement;
    expect(metric).toHaveTextContent("Unavailable");
    expect(metric).not.toHaveTextContent("฿0.00");
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("Unavailable"));
  });

  test("asset failure does not suppress known total liabilities", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockRejectedValue(new Error("investment backend unavailable"));
    getPortfolioPrices.mockResolvedValue([]);
    listCashAccounts.mockResolvedValue([makeCashAccount(1, 200)]);
    listLiabilities.mockResolvedValue([makeLiability(1, 350)]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText(/Investment Assets unavailable/)).toBeInTheDocument());
    const metric = screen.getByText("Total Liabilities").parentElement;
    expect(metric).toHaveTextContent("฿350.00");
    expect(screen.getByText("฿200.00")).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("Unavailable"));
  });

  test("cash failure does not fabricate Total Assets while liabilities remain visible", async () => {
    const portfolio = makePortfolio(1, 100);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([makeHolding(portfolio.id, 1, "AAA")]);
    getPortfolioPrices.mockResolvedValue([makeQuote("AAA", 900, 800)]);
    listCashAccounts.mockRejectedValue(new Error("cash backend unavailable"));
    listLiabilities.mockResolvedValue([makeLiability(1, 350)]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText(/Cash Accounts unavailable — Total Assets cannot be calculated/)).toBeInTheDocument());
    const liabilityMetric = screen.getByText("Total Liabilities").parentElement;
    expect(liabilityMetric).toHaveTextContent("฿350.00");
    const assetsMetric = screen.getByText("Total Assets").parentElement;
    expect(assetsMetric).toHaveTextContent("Unavailable");
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("Unavailable"));
  });

  test("defensive invalid current liability data is unavailable rather than silently summed", async () => {
    portfolioState.portfolios = [];
    listLiabilities.mockResolvedValue([
      makeLiability(1, 200, { currency: "USD" as Liability["currency"] }),
    ]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText(/Liabilities unavailable/)).toBeInTheDocument());
    const metric = screen.getByText("Total Liabilities").parentElement;
    expect(metric).toHaveTextContent("Unavailable");
    expect(metric).not.toHaveTextContent("฿200.00");
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("Unavailable"));
  });

  test("a stale liability response cannot overwrite a newer dashboard context", async () => {
    const first = makePortfolio(1);
    const second = makePortfolio(2);
    const firstLiabilities = deferred<Liability[]>();
    const secondLiabilities = deferred<Liability[]>();

    portfolioState.portfolios = [first];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    listLiabilities
      .mockImplementationOnce(() => firstLiabilities.promise)
      .mockImplementationOnce(() => secondLiabilities.promise);

    const view = render(<DashboardPage />);
    await waitFor(() => expect(listLiabilities).toHaveBeenCalledWith(false));

    portfolioState.portfolios = [second];
    view.rerender(<DashboardPage />);
    await waitFor(() => expect(listLiabilities).toHaveBeenCalledTimes(2));

    await act(async () => { secondLiabilities.resolve([makeLiability(2, 200)]); });
    await waitFor(() => expect(screen.getByText("฿200.00")).toBeInTheDocument());

    await act(async () => { firstLiabilities.resolve([makeLiability(1, 999)]); });
    const metric = screen.getByText("Total Liabilities").parentElement;
    expect(metric).toHaveTextContent("฿200.00");
    expect(metric).not.toHaveTextContent("฿999.00");
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿-200.00"));
  });

  test("liabilities do not enter investment wealth history, performance, or dividend income", async () => {
    const portfolio = makePortfolio(1, 0);
    portfolioState.portfolios = [portfolio];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    listLiabilities.mockResolvedValue([makeLiability(1, 999)]);
    getTransactionHistory.mockResolvedValue([dividend(portfolio.id, 1, 100)]);
    getSnapshots.mockResolvedValue([
      perfSnapshot(portfolio.id, "2026-06-01", { beginningNav: 1000, gain: 100 }),
      perfSnapshot(portfolio.id, "2026-06-02", { beginningNav: 1100, gain: 0 }),
    ]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByTestId("wealth-history-chart")).toBeInTheDocument());
    expect(screen.getByTestId("wealth-history-chart")).toHaveTextContent("2026-06-01=1100");
    expect(screen.getByText("+10.00%")).toBeInTheDocument();
    expect(screen.getAllByText("THB 100.00").length).toBeGreaterThan(0);
    expect(screen.getByText("฿999.00")).toBeInTheDocument();
    expect(screen.queryByText("฿1,099.00")).not.toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿-999.00"));
  });

  test("provides the liability management link and keeps asset terminology separate", async () => {
    portfolioState.portfolios = [];
    listLiabilities.mockResolvedValue([]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByRole("link", { name: /Manage liabilities/ })).toBeInTheDocument());
    expect(screen.getByRole("link", { name: /Manage liabilities/ })).toHaveAttribute("href", "/liabilities");
    expect(screen.getByText("External Cash")).toBeInTheDocument();
    expect(screen.getByText("Total Assets")).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("Net Worth").parentElement).toHaveTextContent("฿0.00"));
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

describe("Cross-portfolio wealth history", () => {
  test("aggregates combined wealth history from multiple portfolios with aligned dates", async () => {
    const p1 = makePortfolio(1);
    const p2 = makePortfolio(2);
    portfolioState.portfolios = [p1, p2];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getSnapshots.mockImplementation((portfolioId: number) =>
      Promise.resolve(portfolioId === 1 ? [snapshot(1, "2026-06-01", 500_000)] : [snapshot(2, "2026-06-01", 300_000)])
    );

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText("฿800,000.00")).toBeInTheDocument());
    expect(screen.queryByText(/Excludes/)).not.toBeInTheDocument();
  });

  test("computes the headline delta between the two most recent complete-coverage points", async () => {
    const p1 = makePortfolio(1);
    const p2 = makePortfolio(2);
    portfolioState.portfolios = [p1, p2];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getSnapshots.mockImplementation((portfolioId: number) =>
      Promise.resolve(
        portfolioId === 1
          ? [snapshot(1, "2026-06-01", 500_000), snapshot(1, "2026-06-02", 520_000)]
          : [snapshot(2, "2026-06-01", 300_000), snapshot(2, "2026-06-02", 300_000)]
      )
    );

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText("฿820,000.00")).toBeInTheDocument());
    expect(screen.getByText("+฿20,000.00")).toBeInTheDocument();
  });

  test("a partially covered date is excluded from the headline and does not fabricate a wealth loss", async () => {
    const p1 = makePortfolio(1);
    const p2 = makePortfolio(2);
    portfolioState.portfolios = [p1, p2];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    // 06-01: both report (complete, 800,000). 06-02: only p1 reports a much
    // smaller number alone — this must never read as an 800,000 -> 500,000 loss.
    getSnapshots.mockImplementation((portfolioId: number) =>
      Promise.resolve(
        portfolioId === 1
          ? [snapshot(1, "2026-06-01", 500_000), snapshot(1, "2026-06-02", 500_000)]
          : [snapshot(2, "2026-06-01", 300_000)]
      )
    );

    render(<DashboardPage />);

    // Latest combined wealth falls back to the last COMPLETE point (06-01),
    // not the partial 06-02 point.
    await waitFor(() => expect(screen.getByText("฿800,000.00")).toBeInTheDocument());
    // Only one complete point exists, so no delta can be computed — never a
    // manufactured -300,000 "loss".
    expect(screen.getByText(/Not enough comparable history yet/)).toBeInTheDocument();
    expect(screen.queryByText(/-฿300,000/)).not.toBeInTheDocument();
    expect(screen.getByText(/1 historical date excluded from the chart/)).toBeInTheDocument();
  });

  test("no snapshots recorded yet shows a graceful empty state, not an error", async () => {
    const p1 = makePortfolio(1);
    portfolioState.portfolios = [p1];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getSnapshots.mockResolvedValue([]);

    render(<DashboardPage />);

    await waitFor(() =>
      expect(screen.getByText(/Investment wealth history will appear after portfolio snapshots are recorded/)).toBeInTheDocument()
    );
  });

  test("one portfolio's snapshot request failing is reported honestly and never yields a fabricated complete total", async () => {
    const good = makePortfolio(1);
    const broken = makePortfolio(2);
    portfolioState.portfolios = [good, broken];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getSnapshots.mockImplementation((portfolioId: number) =>
      portfolioId === good.id
        ? Promise.resolve([snapshot(good.id, "2026-06-01", 500_000)])
        : Promise.reject(new Error("backend unavailable"))
    );

    render(<DashboardPage />);

    // broken's snapshot for 06-01 is unknown, not zero — that date never
    // qualifies as complete, so no combined total is shown as if it were whole.
    await waitFor(() => expect(screen.getByText(/Excludes 1 portfolio that failed to load/)).toBeInTheDocument());
    expect(screen.queryByText("฿500,000.00")).not.toBeInTheDocument();
  });

  test("a stale snapshot response from a previous portfolio set does not overwrite the current view", async () => {
    const first = makePortfolio(1);
    const second = makePortfolio(2);
    const firstSnaps = deferred<PortfolioSnapshotRow[]>();
    const secondSnaps = deferred<PortfolioSnapshotRow[]>();

    portfolioState.portfolios = [first];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getSnapshots.mockImplementation((portfolioId: number) => (
      portfolioId === 1 ? firstSnaps.promise : secondSnaps.promise
    ));

    const view = render(<DashboardPage />);
    await waitFor(() => expect(getSnapshots).toHaveBeenCalledWith(first.id, 365));

    portfolioState.portfolios = [second];
    view.rerender(<DashboardPage />);
    await waitFor(() => expect(getSnapshots).toHaveBeenCalledWith(second.id, 365));

    await act(async () => { secondSnaps.resolve([snapshot(2, "2026-06-01", 200_000)]); });
    await waitFor(() => expect(screen.getByText("฿200,000.00")).toBeInTheDocument());

    // The abandoned first request resolves after the second portfolio set has
    // already rendered its own figures — it must not replace them.
    await act(async () => { firstSnaps.resolve([snapshot(1, "2026-06-01", 999_999)]); });

    expect(screen.getByText("฿200,000.00")).toBeInTheDocument();
    expect(screen.queryByText(/999,999/)).not.toBeInTheDocument();
  });
});

describe("Cross-portfolio investment performance", () => {
  test("renders a beginning-NAV-weighted combined return, distinct from equal-weighting", async () => {
    const p1 = makePortfolio(1);
    const p2 = makePortfolio(2);
    portfolioState.portfolios = [p1, p2];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    // A: 100 -> +50% return. B: 900 -> 0% return.
    // Equal-weight average would read +25.00%; NAV-weighted correct answer is +5.00%.
    getSnapshots.mockImplementation((portfolioId: number) =>
      Promise.resolve(
        portfolioId === 1
          ? [perfSnapshot(1, "2026-06-01", { beginningNav: 100, gain: 50 })]
          : [perfSnapshot(2, "2026-06-01", { beginningNav: 900, gain: 0 })]
      )
    );

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText("Investment Performance")).toBeInTheDocument());
    expect(screen.getByText("+5.00%")).toBeInTheDocument();
    expect(screen.queryByText("+25.00%")).not.toBeInTheDocument();
  });

  test("Wealth History and Investment Performance are visibly distinguished, with no combined benchmark shown", async () => {
    const p1 = makePortfolio(1);
    portfolioState.portfolios = [p1];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getSnapshots.mockResolvedValue([perfSnapshot(1, "2026-06-01", { beginningNav: 1000, gain: 100 })]);

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText("Investment Performance")).toBeInTheDocument());
    expect(screen.getByText("Investment Wealth History")).toBeInTheDocument();
    expect(screen.getByText("Value Change vs Previous Point")).toBeInTheDocument();
    expect(screen.queryByText(/Return vs Previous Point/)).not.toBeInTheDocument();
    expect(screen.queryByText("SET")).not.toBeInTheDocument();
    expect(screen.queryByText("Benchmark")).not.toBeInTheDocument();
  });

  test("incomplete coverage across portfolios is disclosed and excluded from the combined return", async () => {
    const p1 = makePortfolio(1);
    const p2 = makePortfolio(2);
    portfolioState.portfolios = [p1, p2];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getSnapshots.mockImplementation((portfolioId: number) =>
      Promise.resolve(
        portfolioId === 1
          ? [
              perfSnapshot(1, "2026-06-01", { beginningNav: 1000, gain: 100 }),
              perfSnapshot(1, "2026-06-02", { beginningNav: 1100, gain: 50 }),
            ]
          : [perfSnapshot(2, "2026-06-01", { beginningNav: 500, gain: 0 })] // missing on 06-02
      )
    );

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText(/1 date skipped/)).toBeInTheDocument());
    // Only the complete 06-01 observation contributes: (100+0)/(1000+500) = +6.67%.
    expect(screen.getByText("+6.67%")).toBeInTheDocument();
  });

  test("no eligible snapshot data yet shows a graceful empty state, not an error", async () => {
    const p1 = makePortfolio(1);
    portfolioState.portfolios = [p1];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    // First-ever snapshot: no prior NAV, matching the backend's own convention.
    getSnapshots.mockResolvedValue([perfSnapshot(1, "2026-06-01", { beginningNav: 1000, gain: null })]);

    render(<DashboardPage />);

    await waitFor(() =>
      expect(
        screen.getByText(/No combined return yet — every active portfolio needs a comparable, eligible snapshot/)
      ).toBeInTheDocument()
    );
  });

  test("one portfolio's snapshot fetch failing never fabricates a combined return", async () => {
    const good = makePortfolio(1);
    const broken = makePortfolio(2);
    portfolioState.portfolios = [good, broken];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getSnapshots.mockImplementation((portfolioId: number) =>
      portfolioId === good.id
        ? Promise.resolve([perfSnapshot(good.id, "2026-06-01", { beginningNav: 1000, gain: 100 })])
        : Promise.reject(new Error("backend unavailable"))
    );

    render(<DashboardPage />);

    await waitFor(() => expect(screen.getByText("Investment Performance")).toBeInTheDocument());
    expect(
      screen.getByText(/No combined return yet — every active portfolio needs a comparable, eligible snapshot/)
    ).toBeInTheDocument();
    expect(screen.queryByText("+10.00%")).not.toBeInTheDocument();
  });

  test("a stale portfolio-set snapshot response cannot overwrite the current combined performance", async () => {
    const first = makePortfolio(1);
    const second = makePortfolio(2);
    const firstSnaps = deferred<PortfolioSnapshotRow[]>();
    const secondSnaps = deferred<PortfolioSnapshotRow[]>();

    portfolioState.portfolios = [first];
    getHoldings.mockResolvedValue([]);
    getPortfolioPrices.mockResolvedValue([]);
    getSnapshots.mockImplementation((portfolioId: number) => (
      portfolioId === 1 ? firstSnaps.promise : secondSnaps.promise
    ));

    const view = render(<DashboardPage />);
    await waitFor(() => expect(getSnapshots).toHaveBeenCalledWith(first.id, 365));

    portfolioState.portfolios = [second];
    view.rerender(<DashboardPage />);
    await waitFor(() => expect(getSnapshots).toHaveBeenCalledWith(second.id, 365));

    await act(async () => {
      secondSnaps.resolve([perfSnapshot(2, "2026-06-01", { beginningNav: 1000, gain: 40 })]);
    });
    await waitFor(() => expect(screen.getByText("+4.00%")).toBeInTheDocument());

    // The abandoned first request resolves after the second portfolio set has
    // already rendered its own figures — it must not replace them.
    await act(async () => {
      firstSnaps.resolve([perfSnapshot(1, "2026-06-01", { beginningNav: 1000, gain: 999 })]);
    });

    expect(screen.getByText("+4.00%")).toBeInTheDocument();
    expect(screen.queryByText(/99\.90%/)).not.toBeInTheDocument();
  });
});
