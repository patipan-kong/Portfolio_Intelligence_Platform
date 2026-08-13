import { describe, expect, test, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import PortfolioTable from "@/components/PortfolioTable";
import type { PortfolioItem } from "@/lib/api";

function holding(overrides: Partial<PortfolioItem> = {}): PortfolioItem {
  return {
    id: 104,
    portfolio_id: 4,
    symbol: "KBANK.BK",
    shares: 10,
    avg_cost: 200,
    current_price: 248,
    previous_close: 250,
    change_percent: -0.8,
    last_updated: "2026-08-13T04:33:15Z",
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

describe("Portfolio detail quote rendering", () => {
  test("renders the API-mapped current price and Day% from previous close", () => {
    render(
      <PortfolioTable
        rows={[holding()]}
        onRemove={vi.fn(async () => {})}
        onReanalyze={vi.fn(async () => {})}
        onToggleSwap={vi.fn(async () => {})}
      />
    );

    expect(screen.getAllByText("248.00").length).toBeGreaterThan(0);
    expect(screen.getAllByText("-0.80%").length).toBeGreaterThan(0);
  });

  test("renders the same fields for a DR-shaped holding", () => {
    render(
      <PortfolioTable
        rows={[holding({
          id: 102,
          symbol: "AAPL01.BK",
          current_price: 29.5,
          previous_close: 30.5,
          change_percent: -3.28,
        })]}
        onRemove={vi.fn(async () => {})}
        onReanalyze={vi.fn(async () => {})}
        onToggleSwap={vi.fn(async () => {})}
      />
    );

    expect(screen.getAllByText("29.50").length).toBeGreaterThan(0);
    expect(screen.getAllByText("-3.28%").length).toBeGreaterThan(0);
  });
});
