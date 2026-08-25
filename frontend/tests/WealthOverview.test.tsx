import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import WealthOverview from "@/components/WealthOverview";
import type { CashAccount, Liability, Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";

const { selectPortfolio } = vi.hoisted(() => ({
  selectPortfolio: vi.fn(),
}));

vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => ({ selectPortfolio }),
}));

function makePortfolio(id: number, name: string, cash: number): Portfolio {
  return { id, name, cash_balance: cash, created_at: "2026-01-01T00:00:00Z" };
}

function makeHolding(overrides: Partial<PortfolioItem> & { symbol: string; shares: number; avg_cost: number }): PortfolioItem {
  return {
    id: 0,
    portfolio_id: 0,
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
    ...overrides,
  };
}

function makeQuote(symbol: string, current: number): PriceRefreshItem {
  return { symbol, current_price: current, previous_close: current, change_percent: 0, last_updated: null };
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

beforeEach(() => {
  selectPortfolio.mockReset();
});

describe("WealthOverview", () => {
  test("loading state renders a skeleton, not a total", () => {
    render(
      <WealthOverview
        portfolios={[]}
        holdingsMap={{}}
        priceMap={{}}
        holdingsFailedMap={{}}
        pricesLoaded={false}
        loading
      />
    );
    expect(screen.queryByText(/Total Wealth/)).not.toBeInTheDocument();
  });

  test("no portfolios shows an empty state with a way to create one", () => {
    render(
      <WealthOverview
        portfolios={[]}
        holdingsMap={{}}
        priceMap={{}}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
      />
    );
    expect(screen.getByText(/No portfolios yet/)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Create your first portfolio/ })).toHaveAttribute("href", "/portfolio");
  });

  test("shows investment assets and correct per-portfolio brokerage cash/holdings breakdown", () => {
    const portfolios = [makePortfolio(1, "Growth", 1000), makePortfolio(2, "Income", 500)];
    const holdingsMap = {
      1: [makeHolding({ symbol: "AAA", shares: 10, avg_cost: 50 })],
      2: [makeHolding({ symbol: "BBB", shares: 5, avg_cost: 20 })],
    };
    const priceMap = {
      1: [makeQuote("AAA", 60)], // 600
      2: [makeQuote("BBB", 25)], // 125
    };

    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={holdingsMap}
        priceMap={priceMap}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
      />
    );

    // Investment Assets: (1000 + 600) + (500 + 125) = 2225.00.
    // With no external accounts, Total Assets is the same value.
    expect(screen.getAllByText("฿2,225.00")).toHaveLength(2);
    // Growth card total: 1600.00
    expect(screen.getByText("฿1,600.00")).toBeInTheDocument();
    // Income card total: 625.00
    expect(screen.getByText("฿625.00")).toBeInTheDocument();
    // Share of investment assets: 1600/2225 = 71.9%, 625/2225 = 28.1%
    expect(screen.getByText("71.9%")).toBeInTheDocument();
    expect(screen.getByText("28.1%")).toBeInTheDocument();
  });

  test("a portfolio with no holdings shows its cash balance as the total", () => {
    const portfolios = [makePortfolio(1, "Empty", 900)];
    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={{ 1: [] }}
        priceMap={{}}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
      />
    );
    // Investment Assets, Total Assets, portfolio total, and brokerage cash all
    // read 900.00 since holdings value is 0.
    expect(screen.getAllByText("฿900.00").length).toBe(4);
    expect(screen.getByText("100.0%")).toBeInTheDocument();
  });

  test("a portfolio whose holdings failed to load is flagged and excluded from the total, other portfolios still shown", () => {
    const portfolios = [makePortfolio(1, "Good", 100), makePortfolio(2, "Broken", 5000)];
    const holdingsMap = { 1: [makeHolding({ symbol: "AAA", shares: 1, avg_cost: 10 })] };
    const priceMap = { 1: [makeQuote("AAA", 10)] };

    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={holdingsMap}
        priceMap={priceMap}
        holdingsFailedMap={{ 2: true }}
        pricesLoaded
        loading={false}
      />
    );

    // Total excludes the broken portfolio's (much larger) unknown value.
    // Investment Assets is unavailable while one portfolio is failed; only
    // the healthy portfolio card shows its known 110.00 value.
    expect(screen.getAllByText("฿110.00").length).toBe(1);
    expect(screen.getByText(/Investment Assets unavailable/)).toBeInTheDocument();
    expect(screen.getByText(/Unable to load holdings/)).toBeInTheDocument();
    // The healthy portfolio is unaffected.
    expect(screen.getByText("Good")).toBeInTheDocument();
    expect(screen.getByText("Broken")).toBeInTheDocument();
  });

  test("never renders NaN% or Infinity% when total wealth is zero", () => {
    const portfolios = [makePortfolio(1, "P1", 0), makePortfolio(2, "P2", 0)];
    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={{}}
        priceMap={{}}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
      />
    );
    expect(screen.queryByText(/NaN/)).not.toBeInTheDocument();
    expect(screen.queryByText(/Infinity/)).not.toBeInTheDocument();
    expect(screen.getAllByText("0.0%").length).toBe(2);
  });

  test("clicking a portfolio card selects it and links into the existing portfolio experience", () => {
    const portfolios = [makePortfolio(7, "Retirement", 100)];
    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={{ 7: [] }}
        priceMap={{}}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
      />
    );
    const card = screen.getByRole("link", { name: /Retirement/ });
    expect(card).toHaveAttribute("href", "/portfolio");
    fireEvent.click(card);
    expect(selectPortfolio).toHaveBeenCalledWith(7);
  });

  test("flags an estimated (avg_cost fallback) price without hiding the total", () => {
    const portfolios = [makePortfolio(1, "P1", 0)];
    const holdingsMap = { 1: [makeHolding({ symbol: "AAA", shares: 3, avg_cost: 40, current_price: null })] };

    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={holdingsMap}
        priceMap={{}}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
      />
    );

    expect(screen.getByText(/last-known price/)).toBeInTheDocument();
    expect(screen.getAllByText("฿120.00").length).toBeGreaterThan(0);
  });

  test("flags a stale (expired-cache fallback) price without hiding the total or the value it contributed", () => {
    const portfolios = [makePortfolio(1, "P1", 0)];
    const holdingsMap = { 1: [makeHolding({ symbol: "AAA", shares: 3, avg_cost: 40 })] };
    const priceMap = { 1: [{ ...makeQuote("AAA", 50), is_stale: true }] };

    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={holdingsMap}
        priceMap={priceMap}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
      />
    );

    // Reuses the existing honesty-banner block, not a second warning system —
    // and the number is the real (stale) price, not the avg_cost fallback.
    expect(screen.getByText(/live fetch was unavailable/)).toBeInTheDocument();
    expect(screen.getAllByText("฿150.00").length).toBeGreaterThan(0);
    expect(screen.queryByText(/last-known price/)).not.toBeInTheDocument();
  });

  test("does not show the stale banner when every price is fresh", () => {
    const portfolios = [makePortfolio(1, "P1", 0)];
    const holdingsMap = { 1: [makeHolding({ symbol: "AAA", shares: 1, avg_cost: 40 })] };
    const priceMap = { 1: [makeQuote("AAA", 50)] };

    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={holdingsMap}
        priceMap={priceMap}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
      />
    );

    expect(screen.queryByText(/live fetch was unavailable/)).not.toBeInTheDocument();
  });

  test("adds active external cash once and exposes the cash management link", () => {
    const portfolios = [makePortfolio(1, "Growth", 1000)];
    const holdingsMap = { 1: [makeHolding({ symbol: "AAA", shares: 10, avg_cost: 50 })] };
    const priceMap = { 1: [makeQuote("AAA", 60)] };

    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={holdingsMap}
        priceMap={priceMap}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
        cashAccounts={[makeCashAccount(1, 200)]}
        cashStatus="success"
      />
    );

    // Investment Assets already includes the portfolio's 1,000 brokerage cash
    // and 600 market value; only the standalone 200 is added here.
    expect(screen.getAllByText("฿1,600.00").length).toBeGreaterThan(0);
    expect(screen.getByText("฿200.00")).toBeInTheDocument();
    expect(screen.getByText("฿1,800.00")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Manage Cash Accounts/ })).toHaveAttribute("href", "/cash");
  });

  test("shows current active Total Liabilities without changing asset totals", () => {
    const portfolios = [makePortfolio(1, "Growth", 1000)];
    const holdingsMap = { 1: [makeHolding({ symbol: "AAA", shares: 10, avg_cost: 50 })] };
    const priceMap = { 1: [makeQuote("AAA", 60)] };

    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={holdingsMap}
        priceMap={priceMap}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
        cashAccounts={[makeCashAccount(1, 200)]}
        cashStatus="success"
        liabilities={[makeLiability(1, 300), makeLiability(2, 50)]}
        liabilityStatus="success"
      />
    );

    expect(screen.getByText("Investment Assets")).toBeInTheDocument();
    expect(screen.getByText("External Cash")).toBeInTheDocument();
    expect(screen.getByText("Total Assets")).toBeInTheDocument();
    expect(screen.getByText("Total Liabilities")).toBeInTheDocument();
    expect(screen.getByText("฿1,800.00")).toBeInTheDocument();
    expect(screen.getByText("Total Liabilities").parentElement).toHaveTextContent("฿350.00");
    expect(screen.getByRole("link", { name: /Manage liabilities/ })).toHaveAttribute("href", "/liabilities");
    expect(screen.queryByText(/Net Worth/i)).not.toBeInTheDocument();
  });

  test("successful empty liabilities show zero, while a failed phase stays unavailable", () => {
    const baseProps = {
      portfolios: [],
      holdingsMap: {} as Record<number, PortfolioItem[]>,
      priceMap: {} as Record<number, PriceRefreshItem[]>,
      holdingsFailedMap: {},
      pricesLoaded: true,
      loading: false,
    };

    const { rerender } = render(
      <WealthOverview {...baseProps} liabilities={[]} liabilityStatus="success" />
    );
    expect(screen.getByText("Total Liabilities").parentElement).toHaveTextContent("฿0.00");

    rerender(<WealthOverview {...baseProps} liabilities={[]} liabilityStatus="error" />);
    expect(screen.getByText(/Liabilities unavailable/)).toBeInTheDocument();
    expect(screen.getByText("Total Liabilities").parentElement).toHaveTextContent("Unavailable");
  });

  test("archived and malformed liability rows do not become a numeric dashboard total", () => {
    render(
      <WealthOverview
        portfolios={[]}
        holdingsMap={{}}
        priceMap={{}}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
        liabilities={[
          makeLiability(1, 200, { is_archived: true }),
          makeLiability(2, -1),
        ]}
        liabilityStatus="success"
      />
    );

    expect(screen.getByText(/Liabilities unavailable/)).toBeInTheDocument();
    expect(screen.getByText("Total Liabilities").parentElement).toHaveTextContent("Unavailable");
    expect(screen.queryByText("฿200.00")).not.toBeInTheDocument();
  });

  test("cash failure shows known investment assets but no total assets number", () => {
    const portfolios = [makePortfolio(1, "Growth", 1000)];
    render(
      <WealthOverview
        portfolios={portfolios}
        holdingsMap={{ 1: [] }}
        priceMap={{}}
        holdingsFailedMap={{}}
        pricesLoaded
        loading={false}
        cashStatus="error"
      />
    );

    expect(screen.getByText("Investment Assets")).toBeInTheDocument();
    expect(screen.getAllByText("฿1,000.00").length).toBeGreaterThan(0);
    expect(screen.getByText(/Cash Accounts unavailable — Total Assets cannot be calculated/)).toBeInTheDocument();
    expect(screen.getAllByText("Unavailable").length).toBe(2);
  });

  test("empty investment core plus valid cash produces a cash-only total", () => {
    render(
      <WealthOverview
        portfolios={[]}
        holdingsMap={{}}
        priceMap={{}}
        holdingsFailedMap={{}}
        pricesLoaded={false}
        loading={false}
        cashAccounts={[makeCashAccount(1, 350)]}
        cashStatus="success"
      />
    );

    expect(screen.getByText("Investment Assets").parentElement).toHaveTextContent("฿0.00");
    expect(screen.getAllByText("฿350.00")).toHaveLength(2);
    expect(screen.getByText(/No portfolios yet/)).toBeInTheDocument();
  });
});
