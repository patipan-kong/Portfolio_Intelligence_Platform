import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ExecutionDetailPage from "@/app/ai-analytics/(hub)/execution/[id]/page";
import type { ExecutionDetail, ExecutionReview } from "@/lib/api";

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

const { getExecutionDetail, isUnresolvedPortfolioError, getExecutionReview, putExecutionReview } = vi.hoisted(() => ({
  getExecutionDetail: vi.fn(),
  isUnresolvedPortfolioError: vi.fn(() => false),
  getExecutionReview: vi.fn(),
  putExecutionReview: vi.fn(),
}));

vi.mock("@/lib/api", () => ({
  getExecutionDetail, isUnresolvedPortfolioError, getExecutionReview, putExecutionReview,
}));

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

function executionReview(overrides: Partial<ExecutionReview> = {}): ExecutionReview {
  return {
    id: 1,
    execution_decision_id: 42,
    reviewed_at: "2026-09-07T10:00:00Z",
    outcome: "MIXED",
    summary: "Partially worked out.",
    changed_context: "Goal target date moved up.",
    created_at: "2026-09-07T10:00:00Z",
    updated_at: "2026-09-07T10:00:00Z",
    ...overrides,
  };
}

beforeEach(() => {
  getExecutionDetail.mockReset();
  isUnresolvedPortfolioError.mockReset().mockReturnValue(false);
  getExecutionReview.mockReset().mockResolvedValue(null);
  putExecutionReview.mockReset();
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
    const link = screen.getByText("Review opportunity-cost evaluation →");
    expect(link.closest("a")).toHaveAttribute("href", "/ai-analytics/opportunity-cost?decisionId=42");
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

describe("RAE-01: Execution Detail opportunity-cost navigation", () => {
  test("a REJECTED decision keeps execution evidence distinct and links to its evaluation", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      decision: "REJECTED",
      analysis: { status: "unavailable", reason: "no_linked_transactions", score: null } as ExecutionDetail["analysis"],
    }));

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("No execution was recorded for this rejected decision.")).toBeInTheDocument();
    const link = screen.getByText("Review opportunity-cost evaluation →");
    expect(link.closest("a")).toHaveAttribute("href", "/ai-analytics/opportunity-cost?decisionId=42");
    expect(screen.queryByText(/counterfactual.*%|opportunity cost.*%/i)).not.toBeInTheDocument();
  });

  test.each(["PARTIAL_EXECUTION", "MANUAL_OVERRIDE"])("%s preserves execution detail and receives its evaluation link", async (decision) => {
    getExecutionDetail.mockResolvedValue(executionDetail({ decision }));

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("Execution complete")).toBeInTheDocument();
    const link = screen.getByText("Review opportunity-cost evaluation →");
    expect(link.closest("a")).toHaveAttribute("href", "/ai-analytics/opportunity-cost?decisionId=42");
  });

  test("an APPROVED decision has no divergent-decision evaluation link", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({ decision: "APPROVED" }));

    render(<ExecutionDetailPage />);

    await screen.findByText("Execution complete");
    expect(screen.queryByText("Review opportunity-cost evaluation →")).not.toBeInTheDocument();
  });
});

// DEM-01: the "Recorded as" cell already received linked-transaction data
// (id, transaction_date) but rendered it as inert text. It now drills
// through to the transaction's row on /history — navigation only, no new
// claim about success/settlement/completeness.
describe("Execution Detail — recorded-transaction drill-through (DEM-01)", () => {
  test("a single linked transaction renders as a link to /history?transactionId=<id>", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      analysis: {
        status: "ok", score: 80, completeness_pct: 100, funding_fidelity_pct: 95,
        matched_count: 1, total_planned: 1, is_complete: true,
        symbols: {
          CENTEL: {
            action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
            timing_delta_pct: 0, size_delta_pct: 0, note: null,
            transactions: [{ id: 501, transaction_date: "2026-08-20T00:00:00Z" }],
          },
        },
      },
    }));

    render(<ExecutionDetailPage />);

    const link = await screen.findByText("#501 (20 Aug 26)");
    expect(link.closest("a")).toHaveAttribute("href", "/history?transactionId=501");
  });

  test("multiple linked transactions render as independent links in payload order", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      analysis: {
        status: "ok", score: 80, completeness_pct: 100, funding_fidelity_pct: 95,
        matched_count: 1, total_planned: 1, is_complete: true,
        symbols: {
          CENTEL: {
            action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
            timing_delta_pct: 0, size_delta_pct: 0, note: null,
            transactions: [
              { id: 501, transaction_date: "2026-08-20T00:00:00Z" },
              { id: 502, transaction_date: "2026-08-21T00:00:00Z" },
            ],
          },
        },
      },
    }));

    render(<ExecutionDetailPage />);

    const first = await screen.findByText("#501 (20 Aug 26)");
    const second = await screen.findByText("#502 (21 Aug 26)");
    expect(first.closest("a")).toHaveAttribute("href", "/history?transactionId=501");
    expect(second.closest("a")).toHaveAttribute("href", "/history?transactionId=502");
    // payload order preserved, not re-sorted
    expect(first.compareDocumentPosition(second) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  test("zero linked transactions keeps the existing neutral '—', not a link", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      analysis: {
        status: "partial", score: 50, completeness_pct: 50, funding_fidelity_pct: null,
        matched_count: 0, total_planned: 1, is_complete: false,
        symbols: {
          ADVANC: {
            action: "BUY", planned_amount: 20_000, executed_amount: null,
            timing_delta_pct: null, size_delta_pct: null, note: "no_linked_transaction",
            transactions: [],
          },
        },
      },
    }));

    render(<ExecutionDetailPage />);

    expect(await screen.findAllByText("Not recorded")).not.toHaveLength(0);
    expect(screen.getAllByText("—").length).toBeGreaterThan(0);
    expect(screen.queryByRole("link", { name: /^#/ })).not.toBeInTheDocument();
  });

  test("no unsupported success/settlement wording accompanies the evidence link", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail({
      analysis: {
        status: "ok", score: 80, completeness_pct: 100, funding_fidelity_pct: 95,
        matched_count: 1, total_planned: 1, is_complete: true,
        symbols: {
          CENTEL: {
            action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
            timing_delta_pct: 0, size_delta_pct: 0, note: null,
            transactions: [{ id: 501, transaction_date: "2026-08-20T00:00:00Z" }],
          },
        },
      },
    }));

    render(<ExecutionDetailPage />);

    await screen.findByText("#501 (20 Aug 26)");
    const bodyText = document.body.textContent ?? "";
    expect(bodyText).not.toMatch(/settled|verified|matched|executed successfully/i);
  });
});

// ERR-01 (Review Workflows Slice 1): "Post-execution review" card on the
// Execution Detail page — one canonical, human-authored, editable review per
// decision. GET returning null means "no review yet", never a 404.
describe("ERR-01: Post-execution review", () => {
  test("no-review state shows the empty copy and an Add review action", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail());
    getExecutionReview.mockResolvedValue(null);

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("Post-execution review")).toBeInTheDocument();
    expect(await screen.findByText("No review yet. Record what happened after this decision was executed.")).toBeInTheDocument();
    expect(screen.getByText("Add review")).toBeInTheDocument();
    expect(getExecutionReview).toHaveBeenCalledWith(1, 42);
  });

  test("existing-review state shows outcome, reviewed date, summary, and changed context", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail());
    getExecutionReview.mockResolvedValue(executionReview());

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("Mixed")).toBeInTheDocument();
    expect(screen.getByText("Reviewed Sep 7, 2026")).toBeInTheDocument();
    expect(screen.getByText("Partially worked out.")).toBeInTheDocument();
    expect(screen.getByText("Goal target date moved up.")).toBeInTheDocument();
    expect(screen.getByText("Edit review")).toBeInTheDocument();
    expect(screen.queryByText("Add review")).not.toBeInTheDocument();
  });

  test("add review: fills the inline form and PUTs outcome + summary + changed_context", async () => {
    const user = userEvent.setup();
    getExecutionDetail.mockResolvedValue(executionDetail());
    getExecutionReview.mockResolvedValue(null);
    putExecutionReview.mockResolvedValue(executionReview({ outcome: "ON_TRACK", summary: "Looking good" }));

    render(<ExecutionDetailPage />);

    await user.click(await screen.findByText("Add review"));
    await user.click(screen.getByText("On Track"));
    await user.type(screen.getByPlaceholderText("What happened after this decision was executed?"), "Looking good");
    await user.click(screen.getByText("Save review"));

    await waitFor(() => {
      expect(putExecutionReview).toHaveBeenCalledWith(1, 42, {
        outcome: "ON_TRACK",
        summary: "Looking good",
        changed_context: null,
      });
    });
    expect(await screen.findByText("On Track")).toBeInTheDocument();
  });

  test("edit review: prefills the form from the existing review and PUTs the revision", async () => {
    const user = userEvent.setup();
    getExecutionDetail.mockResolvedValue(executionDetail());
    getExecutionReview.mockResolvedValue(executionReview({ outcome: "MIXED", summary: "Partially worked out." }));
    putExecutionReview.mockResolvedValue(executionReview({ outcome: "OFF_TRACK", summary: "Worse than expected." }));

    render(<ExecutionDetailPage />);

    await user.click(await screen.findByText("Edit review"));
    const summaryBox = screen.getByDisplayValue("Partially worked out.");
    await user.clear(summaryBox);
    await user.type(summaryBox, "Worse than expected.");
    await user.click(screen.getByText("Off Track"));
    await user.click(screen.getByText("Save review"));

    await waitFor(() => {
      expect(putExecutionReview).toHaveBeenCalledWith(1, 42, {
        outcome: "OFF_TRACK",
        summary: "Worse than expected.",
        changed_context: "Goal target date moved up.",
      });
    });
    expect(await screen.findByText("Off Track")).toBeInTheDocument();
  });

  test("does not mutate decision/analysis rendering — review card is additive only", async () => {
    getExecutionDetail.mockResolvedValue(executionDetail());
    getExecutionReview.mockResolvedValue(executionReview());

    render(<ExecutionDetailPage />);

    expect(await screen.findByText("Decision #42")).toBeInTheDocument();
    expect(screen.getByText("Execution complete")).toBeInTheDocument();
  });
});
