import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import ExposurePage from "@/app/exposure/page";
import type { Portfolio, PortfolioItem, PriceRefreshItem } from "@/lib/api";

const { getHoldings, getPortfolioPrices, portfolioState } = vi.hoisted(() => ({
  getHoldings: vi.fn(),
  getPortfolioPrices: vi.fn(),
  portfolioState: {
    portfolios: [] as Portfolio[],
    loading: false,
    error: null as string | null,
  },
}));

vi.mock("@/lib/api", () => ({
  getHoldings,
  getPortfolioPrices,
}));

vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => portfolioState,
}));

function portfolio(id: number, name: string, cash: number): Portfolio {
  return { id, name, cash_balance: cash, created_at: "2026-01-01T00:00:00Z" };
}

function holding(
  overrides: Partial<PortfolioItem> & { symbol: string; shares: number; avg_cost: number }
): PortfolioItem {
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
    sector: null,
    ...overrides,
  };
}

function quote(symbol: string, current: number): PriceRefreshItem {
  return { symbol, current_price: current, previous_close: current, change_percent: 0, last_updated: null };
}

describe("ExposurePage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    portfolioState.portfolios = [];
    portfolioState.loading = false;
    portfolioState.error = null;
  });

  it("shows a quiet empty state with zero portfolios", async () => {
    portfolioState.portfolios = [];
    render(<ExposurePage />);
    expect(await screen.findByText(/no portfolios yet/i)).toBeInTheDocument();
  });

  it("shows the portfolio-list error when the context failed to load", () => {
    portfolioState.error = "Cannot connect to backend";
    render(<ExposurePage />);
    expect(screen.getByText("Cannot connect to backend")).toBeInTheDocument();
  });

  it("shows a loading state before holdings settle", () => {
    portfolioState.portfolios = [portfolio(1, "Growth", 1000)];
    getHoldings.mockReturnValue(new Promise(() => {})); // never resolves
    render(<ExposurePage />);
    expect(screen.getByText(/loading portfolios/i)).toBeInTheDocument();
  });

  it("renders overall portfolio contribution, sector exposure, and overlap for two portfolios", async () => {
    portfolioState.portfolios = [portfolio(1, "Growth", 1000), portfolio(2, "Income", 500)];
    getHoldings.mockImplementation((id: number) =>
      Promise.resolve(
        id === 1
          ? [holding({ symbol: "AAA", shares: 10, avg_cost: 10, sector: "Technology" })]
          : [holding({ symbol: "AAA", shares: 5, avg_cost: 10, sector: "Technology" })]
      )
    );
    getPortfolioPrices.mockResolvedValue([quote("AAA", 10)]);

    render(<ExposurePage />);

    expect(await screen.findByText("Growth")).toBeInTheDocument();
    expect(screen.getByText("Income")).toBeInTheDocument();
    expect(screen.getByText("Portfolio contribution")).toBeInTheDocument();
    expect(screen.getByText("Aggregate sector exposure")).toBeInTheDocument();
    expect(screen.getByText("Technology")).toBeInTheDocument();

    // AAA is held by both portfolios — overlap section should list it.
    expect(await screen.findByText("Overlapping holdings")).toBeInTheDocument();
    expect(screen.getAllByText("AAA").length).toBeGreaterThan(0);
    expect(screen.getByText(/held in 2 portfolios/i)).toBeInTheDocument();
  });

  it("shows a quiet no-overlap state for a single portfolio", async () => {
    portfolioState.portfolios = [portfolio(1, "Only", 100)];
    getHoldings.mockResolvedValue([holding({ symbol: "AAA", shares: 1, avg_cost: 100, sector: "Technology" })]);
    getPortfolioPrices.mockResolvedValue([quote("AAA", 100)]);

    render(<ExposurePage />);

    expect(await screen.findByText(/no symbols are currently held in more than one portfolio/i)).toBeInTheDocument();
  });

  it("discloses a portfolio whose holdings failed to load instead of hiding it", async () => {
    portfolioState.portfolios = [portfolio(1, "Good", 1000), portfolio(2, "Broken", 500)];
    getHoldings.mockImplementation((id: number) =>
      id === 1
        ? Promise.resolve([holding({ symbol: "AAA", shares: 10, avg_cost: 10, sector: "Technology" })])
        : Promise.reject(new Error("network error"))
    );
    getPortfolioPrices.mockResolvedValue([quote("AAA", 10)]);

    render(<ExposurePage />);

    expect(await screen.findByText(/could not load holdings for: broken/i)).toBeInTheDocument();
    expect(screen.getByText(/excluded from totals/i)).toBeInTheDocument();
  });

  it("never renders unauthorized normative or advisory language", async () => {
    portfolioState.portfolios = [portfolio(1, "Growth", 1000)];
    getHoldings.mockResolvedValue([holding({ symbol: "AAA", shares: 10, avg_cost: 10, sector: "Technology" })]);
    getPortfolioPrices.mockResolvedValue([quote("AAA", 10)]);

    render(<ExposurePage />);
    await screen.findByText("Portfolio contribution");

    const bodyText = document.body.textContent!.toLowerCase();
    const forbidden = [
      "overweight",
      "underweight",
      "too concentrated",
      "rebalance",
      "should reduce",
      "target weight",
      "recommend",
      "high risk",
      "critical",
    ];
    for (const phrase of forbidden) {
      expect(bodyText).not.toContain(phrase);
    }
  });
});
