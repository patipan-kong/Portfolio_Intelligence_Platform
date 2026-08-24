import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import WealthOverview from "@/components/WealthOverview";
import type { Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";

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

  test("shows combined total wealth and correct per-portfolio cash/holdings breakdown", () => {
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

    // Total: (1000 + 600) + (500 + 125) = 2225.00
    expect(screen.getByText("฿2,225.00")).toBeInTheDocument();
    // Growth card total: 1600.00
    expect(screen.getByText("฿1,600.00")).toBeInTheDocument();
    // Income card total: 625.00
    expect(screen.getByText("฿625.00")).toBeInTheDocument();
    // Share of wealth: 1600/2225 = 71.9%, 625/2225 = 28.1%
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
    // Total Wealth card, the portfolio card's total, and its Cash line all
    // read 900.00 since holdings value is 0 (cash accounts for the whole total).
    expect(screen.getAllByText("฿900.00").length).toBe(3);
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
    // Both the Total Wealth card and Good's own card total read 110.00,
    // since Good is the only portfolio counted in the total.
    expect(screen.getAllByText("฿110.00").length).toBe(2);
    expect(screen.getByText(/Excludes 1 portfolio that failed to load/)).toBeInTheDocument();
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
});
