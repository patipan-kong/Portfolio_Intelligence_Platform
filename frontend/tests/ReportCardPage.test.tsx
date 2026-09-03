import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import ReportCardPage from "@/app/ai-analytics/(hub)/recommendations/[id]/page";
import type { RecommendationReportCard } from "@/lib/api";

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
