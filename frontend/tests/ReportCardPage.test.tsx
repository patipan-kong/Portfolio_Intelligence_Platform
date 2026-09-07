import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import ReportCardPage from "@/app/ai-analytics/(hub)/recommendations/[id]/page";
import type { RecommendationReportCard, ExecutionSymbolDelta } from "@/lib/api";

// Slice 4 (Decision History / Audit UX), Behaviors 3 & 4: the Report Card
// already receives execution.decision_id but had no link out to the full
// Execution Detail page, and dropped already-persisted decision rationale
// (UX.2D) and frozen goal context (Phase 7.4/ADR-008, CONTEXT_ONLY) that the
// backend now surfaces on the same execution section.

const { getRecommendationReportCard, isUnresolvedPortfolioError } = vi.hoisted(() => ({
  getRecommendationReportCard: vi.fn(),
  isUnresolvedPortfolioError: vi.fn(() => false),
}));

vi.mock("@/lib/api", () => ({ getRecommendationReportCard, isUnresolvedPortfolioError }));

vi.mock("next/navigation", () => ({
  useParams: () => ({ id: "99" }),
  useRouter: () => ({ back: vi.fn(), push: vi.fn(), replace: vi.fn() }),
}));

let portfolioState = { currentSelection: 1 as number | null, reportUnresolvedPortfolio: vi.fn() };
vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => portfolioState,
}));

function reportCard(overrides: Partial<RecommendationReportCard> = {}): RecommendationReportCard {
  return {
    snapshot_id: 99,
    portfolio_id: 1,
    date: "2026-08-19T00:00:00Z",
    persona: "BALANCED",
    regime: "NEUTRAL",
    consensus_type: "STRONG_CONSENSUS",
    confidence: 80,
    plan: { status: "ok", buy_trades: [], sell_reduce_trades: [], cash_available: 0, funding_gap: 0 },
    decision: { decision: "APPROVED", is_system_generated: false, executed_at: "2026-08-20T00:00:00Z" },
    execution: {
      status: "ok",
      decision_id: 456,
      decision: "APPROVED",
      executed_at: "2026-08-20T00:00:00Z",
      analysis: { status: "unavailable", reason: "no_linked_transactions", score: null },
    },
    outcomes: {},
    verdict: { en: "Too early to grade." },
    as_of: "2026-08-21T00:00:00Z",
    ...overrides,
  } as RecommendationReportCard;
}

beforeEach(() => {
  getRecommendationReportCard.mockReset();
  isUnresolvedPortfolioError.mockReset().mockReturnValue(false);
  portfolioState = { currentSelection: 1, reportUnresolvedPortfolio: vi.fn() };
});

describe("Report Card — Execution Detail navigation (Slice 4, Behavior 3)", () => {
  test("links to Execution Detail using execution.decision_id when a decision exists", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard());

    render(<ReportCardPage />);

    const link = await screen.findByText("View full execution detail →");
    expect(link.closest("a")).toHaveAttribute("href", "/ai-analytics/execution/456");
  });

  test("no link is rendered when no decision has been recorded", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      decision: null,
      execution: { status: "no_decision_recorded" },
    }));

    render(<ReportCardPage />);

    await screen.findByText("No decision recorded yet for this recommendation.");
    expect(screen.queryByText("View full execution detail →")).not.toBeInTheDocument();
  });
});

describe("Report Card — historical decision rationale (Slice 4, Behavior 4)", () => {
  test("renders persisted MANUAL_OVERRIDE rationale fields", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      decision: { decision: "MANUAL_OVERRIDE", is_system_generated: false, executed_at: "2026-08-20T00:00:00Z" },
      execution: {
        status: "ok",
        decision_id: 456,
        decision: "MANUAL_OVERRIDE",
        executed_at: "2026-08-20T00:00:00Z",
        analysis: { status: "unavailable", reason: "no_linked_transactions", score: null },
        override_type: "REPLACE_SYMBOL",
        original_symbol: "KBANK",
        replacement_symbol: "TOA",
        reason_category: "HIGHER_CONVICTION",
        override_notes: "Higher conviction in TOA.",
        goal_context: null,
      },
    }));

    render(<ReportCardPage />);

    expect(await screen.findByText("REPLACE SYMBOL")).toBeInTheDocument();
    expect(await screen.findByText("HIGHER CONVICTION")).toBeInTheDocument();
    expect(await screen.findByText((_, el) => el?.textContent === "KBANK → TOA")).toBeInTheDocument();
    expect(await screen.findByText(/Higher conviction in TOA\./)).toBeInTheDocument();
  });

  test("null rationale fields render no empty labels or placeholders", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard());

    render(<ReportCardPage />);

    await screen.findByText("View full execution detail →");
    expect(screen.queryByText(/null/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/undefined/i)).not.toBeInTheDocument();
  });

  test("frozen goal context renders with historical, non-causal wording", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: {
        status: "ok",
        decision_id: 456,
        decision: "APPROVED",
        executed_at: "2026-08-20T00:00:00Z",
        analysis: { status: "unavailable", reason: "no_linked_transactions", score: null },
        goal_context: {
          contract_version: "wealth.decision-goal-context.v1",
          source_goal_context_version: "wealth.goal-context.v1",
          decision_effect: "CONTEXT_ONLY",
          context_state: "COMPLETE",
          selected_goal_ids: [1],
          observed_at: "2026-08-19T00:00:00Z",
          goals: [{
            id: 1, name: "House Down Payment", goal_type: "HOUSE", priority: "HIGH",
            target_amount: 500_000, currency: "THB", target_date: "2027-01-01",
            is_archived: false, updated_at: "2026-08-01T00:00:00Z",
            designated_total: 100_000, progress_ratio: 0.2, progress_percent: 20,
            funding_gap: 400_000, fully_designated: false,
          }],
        },
      },
    }));

    render(<ReportCardPage />);

    expect(await screen.findByText("Goal context at time of decision")).toBeInTheDocument();
    expect(await screen.findByText("House Down Payment")).toBeInTheDocument();
    expect(screen.queryByText(/recommended because/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/caused the recommendation/i)).not.toBeInTheDocument();
  });

  test("missing goal context (EMPTY/null) omits the block cleanly", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: {
        status: "ok",
        decision_id: 456,
        decision: "APPROVED",
        executed_at: "2026-08-20T00:00:00Z",
        analysis: { status: "unavailable", reason: "no_linked_transactions", score: null },
        goal_context: null,
      },
    }));

    render(<ReportCardPage />);

    await screen.findByText("View full execution detail →");
    expect(screen.queryByText("Goal context at time of decision")).not.toBeInTheDocument();
  });
});

describe("Report Card — historical timestamp semantics (Slice 4 §H)", () => {
  test("decision timestamp is never labeled 'executed'", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard());

    render(<ReportCardPage />);

    expect(await screen.findByText("decision recorded 2026-08-20")).toBeInTheDocument();
    expect(screen.queryByText(/^executed /)).not.toBeInTheDocument();
  });
});

// DEM-01: the Report Card already receives the same execution.analysis
// payload as Execution Detail (including per-symbol linked transactions)
// but never rendered them. This proves the evidence now surfaces, without
// implying settlement/success, and that its absence is never presented as
// execution failure.
describe("Report Card — recorded execution evidence (DEM-01)", () => {
  function executionWithSymbols(symbols: Record<string, ExecutionSymbolDelta>) {
    return {
      status: "ok" as const,
      decision_id: 456,
      decision: "APPROVED",
      executed_at: "2026-08-20T00:00:00Z",
      analysis: {
        status: "ok" as const, score: 80, completeness_pct: 100, funding_fidelity_pct: 95,
        matched_count: 1, total_planned: 1, is_complete: true,
        symbols,
      },
    };
  }

  test("renders linked transaction evidence with a correct href when present", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithSymbols({
        CENTEL: {
          action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
          timing_delta_pct: 0, size_delta_pct: 0, note: null,
          transactions: [{ id: 501, transaction_date: "2026-08-20T00:00:00Z" }],
        },
      }),
    }));

    render(<ReportCardPage />);

    expect(await screen.findByText(/Recorded execution evidence/)).toBeInTheDocument();
    const link = await screen.findByText("#501 (20 Aug 26)");
    expect(link.closest("a")).toHaveAttribute("href", "/history?transactionId=501");
  });

  test("multiple linked transactions render as independent links", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithSymbols({
        CENTEL: {
          action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
          timing_delta_pct: 0, size_delta_pct: 0, note: null,
          transactions: [
            { id: 501, transaction_date: "2026-08-20T00:00:00Z" },
            { id: 502, transaction_date: "2026-08-21T00:00:00Z" },
          ],
        },
      }),
    }));

    render(<ReportCardPage />);

    const first = await screen.findByText("#501 (20 Aug 26)");
    const second = await screen.findByText("#502 (21 Aug 26)");
    expect(first.closest("a")).toHaveAttribute("href", "/history?transactionId=501");
    expect(second.closest("a")).toHaveAttribute("href", "/history?transactionId=502");
  });

  test("absent transaction evidence omits the row entirely — never implies execution failure", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithSymbols({
        ADVANC: {
          action: "BUY", planned_amount: 20_000, executed_amount: null,
          timing_delta_pct: null, size_delta_pct: null, note: "no_linked_transaction",
          transactions: [],
        },
      }),
    }));

    render(<ReportCardPage />);

    await screen.findByText("ADVANC");
    expect(screen.queryByText(/Recorded execution evidence/)).not.toBeInTheDocument();
    expect(screen.queryByText(/not executed/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/no execution/i)).not.toBeInTheDocument();
  });

  test("existing timing and size analysis is unchanged by the added evidence row", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithSymbols({
        CENTEL: {
          action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
          timing_delta_pct: 2.5, size_delta_pct: -1,
          note: null,
          transactions: [{ id: 501, transaction_date: "2026-08-20T00:00:00Z" }],
        },
      }),
    }));

    render(<ReportCardPage />);

    expect(await screen.findByText("Timing: +2.5%")).toBeInTheDocument();
    expect(await screen.findByText("Size: -1%")).toBeInTheDocument();
  });

  test("no settlement/success/correctness wording is introduced by the evidence row", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithSymbols({
        CENTEL: {
          action: "BUY", planned_amount: 30_000, executed_amount: 30_000,
          timing_delta_pct: 0, size_delta_pct: 0, note: null,
          transactions: [{ id: 501, transaction_date: "2026-08-20T00:00:00Z" }],
        },
      }),
    }));

    render(<ReportCardPage />);

    await screen.findByText("#501 (20 Aug 26)");
    const bodyText = document.body.textContent ?? "";
    expect(bodyText).not.toMatch(/settled|verified|matched|executed successfully|right call|wrong call/i);
  });
});

// Review Workflows Slice 4 — compact, read-only "Post-execution review"
// block inside "2 · What Happened". Attaches to the same execution.decision
// already rendered above it; never a second fetch, never an edit surface.
describe("Report Card — post-execution review (Review Workflows Slice 4)", () => {
  function executionWithReview(overrides: Record<string, unknown>) {
    return {
      status: "ok" as const,
      decision_id: 456,
      decision: "APPROVED",
      executed_at: "2026-08-20T00:00:00Z",
      analysis: { status: "unavailable", reason: "no_linked_transactions", score: null },
      reviewable: true,
      execution_review: null,
      ...overrides,
    };
  }

  test("reviewed decision renders label, badge, reviewed date, and summary", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithReview({
        execution_review: { outcome: "ON_TRACK", reviewed_at: "2026-09-07T00:00:00Z", summary: "Held up well." },
      }),
    }));

    render(<ReportCardPage />);

    expect(await screen.findByText("Post-execution review")).toBeInTheDocument();
    expect(await screen.findByText("On Track")).toBeInTheDocument();
    expect(await screen.findByText("Reviewed Sep 7, 2026")).toBeInTheDocument();
    expect(await screen.findByText("Held up well.")).toBeInTheDocument();
  });

  test("null summary renders no empty paragraph or placeholder", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithReview({
        execution_review: { outcome: "MIXED", reviewed_at: "2026-09-07T00:00:00Z", summary: null },
      }),
    }));

    render(<ReportCardPage />);

    await screen.findByText("Mixed");
    expect(screen.queryByText(/null/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/undefined/i)).not.toBeInTheDocument();
  });

  test("reviewable decision without a review shows a subtle 'Not reviewed yet' state", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithReview({ reviewable: true, execution_review: null }),
    }));

    render(<ReportCardPage />);

    expect(await screen.findByText("Post-execution review")).toBeInTheDocument();
    expect(await screen.findByText("Not reviewed yet")).toBeInTheDocument();
  });

  test("system-generated decision with no review renders no review block at all", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      decision: { decision: "EXPIRED", is_system_generated: true, executed_at: "2026-08-20T00:00:00Z" },
      execution: executionWithReview({ reviewable: false, execution_review: null }),
    }));

    render(<ReportCardPage />);

    await screen.findByText("View full execution detail →");
    expect(screen.queryByText("Post-execution review")).not.toBeInTheDocument();
    expect(screen.queryByText("Not reviewed yet")).not.toBeInTheDocument();
  });

  test("system-generated decision with a legacy review still renders it, read-only", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      decision: { decision: "EXPIRED", is_system_generated: true, executed_at: "2026-08-20T00:00:00Z" },
      execution: executionWithReview({
        reviewable: false,
        execution_review: { outcome: "OFF_TRACK", reviewed_at: "2026-09-07T00:00:00Z", summary: "Regime shifted." },
      }),
    }));

    render(<ReportCardPage />);

    expect(await screen.findByText("Post-execution review")).toBeInTheDocument();
    expect(await screen.findByText("Off Track")).toBeInTheDocument();
    expect(await screen.findByText("Regime shifted.")).toBeInTheDocument();
  });

  test("no decision recorded renders no review section", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      decision: null,
      execution: { status: "no_decision_recorded" },
    }));

    render(<ReportCardPage />);

    await screen.findByText("No decision recorded yet for this recommendation.");
    expect(screen.queryByText("Post-execution review")).not.toBeInTheDocument();
    expect(screen.queryByText("Not reviewed yet")).not.toBeInTheDocument();
  });

  test("no edit affordance (no textarea, Save, Add review, or Edit review control) ever renders on Report Card", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithReview({
        execution_review: { outcome: "ON_TRACK", reviewed_at: "2026-09-07T00:00:00Z", summary: "Held up well." },
      }),
    }));

    render(<ReportCardPage />);

    await screen.findByText("Post-execution review");
    expect(document.querySelector("textarea")).not.toBeInTheDocument();
    expect(screen.queryByText("Save review")).not.toBeInTheDocument();
    expect(screen.queryByText("Add review")).not.toBeInTheDocument();
    expect(screen.queryByText("Edit review")).not.toBeInTheDocument();
  });

  test("Execution Detail navigation remains unchanged and is not duplicated by the review block", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithReview({
        execution_review: { outcome: "ON_TRACK", reviewed_at: "2026-09-07T00:00:00Z", summary: "Held up well." },
      }),
    }));

    render(<ReportCardPage />);

    const links = await screen.findAllByText("View full execution detail →");
    expect(links).toHaveLength(1);
    expect(links[0].closest("a")).toHaveAttribute("href", "/ai-analytics/execution/456");
  });

  test("objective Outcome section still renders independently of the review block", async () => {
    getRecommendationReportCard.mockResolvedValue(reportCard({
      execution: executionWithReview({
        execution_review: { outcome: "ON_TRACK", reviewed_at: "2026-09-07T00:00:00Z", summary: "Held up well." },
      }),
      outcomes: {
        H30: { status: "graded", return_pct: 4.2, benchmark_return_pct: 2.1, alpha: 2.1, directional_correct: true },
      },
    }));

    render(<ReportCardPage />);

    expect(await screen.findByText("3 · Outcome (frozen shadow vs benchmark)")).toBeInTheDocument();
    expect(await screen.findByText("Post-execution review")).toBeInTheDocument();
  });
});
