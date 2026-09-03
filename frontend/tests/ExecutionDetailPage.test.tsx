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
    analysis: {
      status: "ok", score: 80, completeness_pct: 100, funding_fidelity_pct: 95,
      matched_count: 1, total_planned: 1, is_complete: true, symbols: {},
    },
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

// Execution Completion Polish (Slice 3): completion badge/row labels must
// derive from matched_count/total_planned/is_complete, never from the
// grading-measurability `status` field — see execution_analyzer.py and
// DecisionActionPanel.executionCompletionLabel.
describe("Execution Detail — completion (Execution Completion Polish, Slice 3)", () => {
  test("a fully matched decision renders 'Execution complete' even when grading status is 'partial'", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      analysis: {
        status: "partial", score: 92, completeness_pct: 100, funding_fidelity_pct: null,
        matched_count: 1, total_planned: 1, is_complete: true,
        symbols: {
          CENTEL: {
            action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
            timing_delta_pct: 0, size_delta_pct: 0, note: null,
            transactions: [{ id: 1, transaction_date: "2026-08-20T00:00:00Z" }],
          },
        },
      },
    }));

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("Execution complete")).toBeInTheDocument();
    expect(screen.queryByText(/partial/i)).not.toBeInTheDocument();
  });

  test("a partially recorded decision shows the matched-of-total count", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      analysis: {
        status: "partial", score: 50, completeness_pct: 50, funding_fidelity_pct: null,
        matched_count: 1, total_planned: 2, is_complete: false,
        symbols: {
          CENTEL: {
            action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
            timing_delta_pct: 0, size_delta_pct: 0, note: null,
            transactions: [{ id: 1, transaction_date: "2026-08-20T00:00:00Z" }],
          },
          ADVANC: {
            action: "BUY", planned_amount: 20_000, executed_amount: null,
            timing_delta_pct: null, size_delta_pct: null, note: "no_linked_transaction",
            transactions: [],
          },
        },
      },
    }));

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("Partially recorded (1 of 2)")).toBeInTheDocument();
  });

  test("humanizes per-row note into Recorded / Not recorded and never exposes the raw enum string", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      analysis: {
        status: "partial", score: 50, completeness_pct: 50, funding_fidelity_pct: null,
        matched_count: 1, total_planned: 2, is_complete: false,
        symbols: {
          CENTEL: {
            action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
            timing_delta_pct: 0, size_delta_pct: 0, note: null,
            transactions: [{ id: 1, transaction_date: "2026-08-20T00:00:00Z" }],
          },
          ADVANC: {
            action: "BUY", planned_amount: 20_000, executed_amount: null,
            timing_delta_pct: null, size_delta_pct: null, note: "no_linked_transaction",
            transactions: [],
          },
        },
      },
    }));

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("Recorded")).toBeInTheDocument();
    expect(await screen.findByText("Not recorded")).toBeInTheDocument();
    expect(screen.queryByText("no_linked_transaction")).not.toBeInTheDocument();
  });

  test("a decision with zero actionable trades renders 'Execution complete'", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      analysis: {
        status: "ok", score: null, completeness_pct: 100, funding_fidelity_pct: null,
        matched_count: 0, total_planned: 0, is_complete: true, symbols: {},
      },
    }));

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("Execution complete")).toBeInTheDocument();
  });

  // Correction pass (review findings 2 + 4): a decision with no reconstructable
  // plan at all (execution_ledger.py's no_target_allocations short-circuit)
  // returns {"status": "unavailable", "reason": ..., "score": null} with
  // matched_count/total_planned/is_complete entirely absent — a stricter
  // degraded case than "plan known, zero linked transactions yet" (which
  // still populates every completion field). The page already renders its
  // generic "Execution analysis unavailable" branch for any status ===
  // "unavailable"; this proves that branch never reaches the completion-count
  // interpolation and so can never render undefined.
  test("missing plan evidence (no_target_allocations) never renders undefined or a fabricated completion state", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      analysis: { status: "unavailable", reason: "no_target_allocations", score: null } as ExecutionDetail["analysis"],
    }));

    render(<ExecutionDetailPage />);

    await screen.findByText(/Execution analysis unavailable/);
    expect(screen.queryByText(/undefined/)).not.toBeInTheDocument();
    expect(screen.queryByText("Execution complete")).not.toBeInTheDocument();
    expect(screen.queryByText(/Partially recorded/)).not.toBeInTheDocument();
  });
});

// Slice 4 (Decision History / Audit UX), Behavior 1: the "Record execution"
// CTA previously rendered unconditionally whenever analysis.status ===
// "unavailable", regardless of decision type — misleading for REJECTED
// (evaluated via whole-portfolio counterfactual return, never linked-
// transaction analysis) and EXPIRED (system-generated, no human action to
// execute). Eligibility now mirrors DecisionActionPanel's
// RECORD_EXECUTION_ELIGIBLE (APPROVED/MANUAL_OVERRIDE/PARTIAL_EXECUTION).
describe("Execution Detail — Record execution CTA eligibility (Slice 4)", () => {
  test("REJECTED with zero linked transactions never offers Record execution", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      decision: "REJECTED",
      analysis: { status: "unavailable", reason: "no_linked_transactions", score: null } as ExecutionDetail["analysis"],
    }));

    render(<ExecutionDetailPage />);

    await screen.findByText(/Execution analysis unavailable/);
    expect(screen.queryByText("Record execution →")).not.toBeInTheDocument();
    expect(await screen.findByText("No execution was recorded for this rejected decision.")).toBeInTheDocument();
  });

  test("EXPIRED (system-generated) never offers Record execution", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      decision: "EXPIRED",
      analysis: { status: "unavailable", reason: "no_linked_transactions", score: null } as ExecutionDetail["analysis"],
    }));

    render(<ExecutionDetailPage />);

    await screen.findByText(/Execution analysis unavailable/);
    expect(screen.queryByText("Record execution →")).not.toBeInTheDocument();
    expect(await screen.findByText("No execution was recorded for this expired recommendation.")).toBeInTheDocument();
  });

  test("APPROVED with zero linked transactions still offers Record execution (regression)", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      decision: "APPROVED",
      analysis: { status: "unavailable", reason: "no_linked_transactions", score: null } as ExecutionDetail["analysis"],
    }));

    render(<ExecutionDetailPage />);

    await screen.findByText(/Execution analysis unavailable/);
    const link = await screen.findByText("Record execution →");
    expect(link.closest("a")).toHaveAttribute("href", "/portfolio?decision=42");
  });

  test("historical timestamp is never labeled 'executed'", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({ executed_at: "2026-08-20T00:00:00Z" }));

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("decision recorded 2026-08-20")).toBeInTheDocument();
    expect(screen.queryByText(/^executed /)).not.toBeInTheDocument();
  });
});
