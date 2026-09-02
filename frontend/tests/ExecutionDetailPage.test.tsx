import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import ExecutionDetailPage from "@/app/ai-analytics/(hub)/execution/[id]/page";
import type { ExecutionDetail } from "@/lib/api";

// Decision Explainability Polish — Slice 2 (C): Execution Detail already has
// `snapshot_id` in hand but had no way back to the recommendation that
// produced the decision. This test proves the added "See why this was
// recommended" bridge links to the existing, deterministic historical
// Recommendation Report Card (/ai-analytics/recommendations/{snapshot_id})
// — pure navigation, no duplicated content, no new page.
//
// Follows the existing usePortfolio mocking convention from
// tests/Dashboard.test.tsx (a lighter alternative to full PortfolioProvider
// wiring, matched to this page's actual dependency surface).

const { getExecutionDetail, isUnresolvedPortfolioError } = vi.hoisted(() => ({
  getExecutionDetail: vi.fn(),
  isUnresolvedPortfolioError: vi.fn(() => false),
}));

vi.mock("@/lib/api", () => ({ getExecutionDetail, isUnresolvedPortfolioError }));

vi.mock("next/navigation", () => ({
  useParams: () => ({ id: "42" }),
  useRouter: () => ({ back: vi.fn(), push: vi.fn(), replace: vi.fn() }),
}));

let portfolioState = { currentSelection: 1 as number | null, reportUnresolvedPortfolio: vi.fn() };
vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => portfolioState,
}));

function executionDetail(overrides: Partial<ExecutionDetail> = {}): ExecutionDetail {
  return {
    decision_id: 42,
    snapshot_id: 99,
    portfolio_id: 1,
    decision: "APPROVED",
    executed_at: "2026-08-20T00:00:00Z",
    analysis: { status: "ok", score: 80, completeness_pct: 100, funding_fidelity_pct: 95, symbols: {} } as ExecutionDetail["analysis"],
    partial_warning: null,
    as_of: "2026-08-21T00:00:00Z",
    ...overrides,
  };
}

beforeEach(() => {
  getExecutionDetail.mockReset();
  isUnresolvedPortfolioError.mockReset().mockReturnValue(false);
  portfolioState = { currentSelection: 1, reportUnresolvedPortfolio: vi.fn() };
});

describe("Execution Detail — recommendation bridge", () => {
  test("links to the historical Recommendation Report Card using snapshot_id", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({ snapshot_id: 99 }));

    render(<ExecutionDetailPage />);

    const link = await screen.findByText("See why this was recommended →");
    expect(link.closest("a")).toHaveAttribute("href", "/ai-analytics/recommendations/99");
  });

  test("does not route the bridge link back to the live /optimizer page", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({ snapshot_id: 99 }));

    render(<ExecutionDetailPage />);

    const link = await screen.findByText("See why this was recommended →");
    expect(link.closest("a")?.getAttribute("href")).not.toMatch(/^\/optimizer/);
  });
});
