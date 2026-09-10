import { render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, test, vi } from "vitest";
import PeriodicReviewPage from "@/app/review/page";
import type {
  EvaluationScorecard,
  ExecutionLedger,
  ExecutionLedgerRow,
  FactualReviewResponse,
  GoalContextGoal,
  Portfolio,
  WealthGoal,
} from "@/lib/api";

const {
  listCashAccounts,
  listLiabilities,
  getSnapshots,
  getCashAccountBalanceAsOf,
  getLiabilityBalanceAsOf,
  getNetWorthChangeAttribution,
  listWealthGoals,
  getWealthFactualReview,
  getExecutionLedger,
  getEvaluationScorecard,
  isUnresolvedPortfolioError,
} = vi.hoisted(() => ({
  listCashAccounts: vi.fn(),
  listLiabilities: vi.fn(),
  getSnapshots: vi.fn(),
  getCashAccountBalanceAsOf: vi.fn(),
  getLiabilityBalanceAsOf: vi.fn(),
  getNetWorthChangeAttribution: vi.fn(),
  listWealthGoals: vi.fn(),
  getWealthFactualReview: vi.fn(),
  getExecutionLedger: vi.fn(),
  getEvaluationScorecard: vi.fn(),
  isUnresolvedPortfolioError: vi.fn(() => false),
}));

vi.mock("@/lib/api", () => ({
  listCashAccounts,
  listLiabilities,
  getSnapshots,
  getCashAccountBalanceAsOf,
  getLiabilityBalanceAsOf,
  getNetWorthChangeAttribution,
  listWealthGoals,
  getWealthFactualReview,
  getExecutionLedger,
  getEvaluationScorecard,
  isUnresolvedPortfolioError,
}));

let portfolioState: {
  portfolios: Portfolio[];
  currentSelection: number | null;
  loading: boolean;
  error: string | null;
  reportUnresolvedPortfolio: ReturnType<typeof vi.fn>;
} = {
  portfolios: [],
  currentSelection: null,
  loading: false,
  error: null,
  reportUnresolvedPortfolio: vi.fn(),
};
vi.mock("@/lib/PortfolioContext", () => ({ usePortfolio: () => portfolioState }));

function makePortfolio(id: number): Portfolio {
  return { id, name: `Portfolio ${id}`, cash_balance: 0, created_at: "2026-01-01T00:00:00Z" };
}

function makeGoal(overrides: Partial<WealthGoal> & { id: number; name: string }): WealthGoal {
  return {
    workspace_id: 1,
    goal_type: "OTHER",
    target_amount: 100000,
    currency: "THB",
    target_date: null,
    priority: "MEDIUM",
    note: null,
    is_archived: false,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
    ...overrides,
  };
}

function makeContextGoal(overrides: Partial<GoalContextGoal> & { id: number; name: string }): GoalContextGoal {
  return {
    goal_type: "OTHER",
    target_amount: 100000,
    currency: "THB",
    target_date: null,
    priority: "MEDIUM",
    is_archived: false,
    updated_at: "2026-01-01T00:00:00Z",
    allocations: [],
    designated_total: 0,
    progress_ratio: 0,
    progress_percent: 0,
    funding_gap: 100000,
    fully_designated: false,
    ...overrides,
  };
}

function makeFactualReview(goals: GoalContextGoal[]): FactualReviewResponse {
  return {
    contract_version: "wealth.factual-review.v1",
    review_generated_at: "2026-01-01T00:00:00Z",
    scope: { kind: "WORKSPACE", include_archived: true },
    goal_context: {
      contract_version: "wealth.goal-context.v1",
      context_generated_at: "2026-01-01T00:00:00Z",
      completeness: "COMPLETE",
      scope: { kind: "WORKSPACE", include_archived: true },
      goals,
      designation_by_source: [],
    },
    valuation_completeness: "COMPLETE",
    sources: [],
  };
}

function makeRow(overrides: Partial<ExecutionLedgerRow> = {}): ExecutionLedgerRow {
  return {
    decision_id: 1,
    snapshot_id: 10,
    date: "2026-01-05T00:00:00Z",
    decision: "APPROVED",
    execution_status: "complete",
    execution_score: 80,
    completeness_pct: 100,
    funding_fidelity_pct: null,
    recording_progress_eligible: true,
    matched_count: 2,
    total_planned: 2,
    is_complete: true,
    reviewable: true,
    has_review: false,
    review_outcome: null,
    reviewed_at: null,
    follow_up_acknowledged_at: null,
    outcome_delta: null,
    ...overrides,
  };
}

function makeLedger(rows: ExecutionLedgerRow[]): ExecutionLedger {
  return {
    portfolio_id: 1,
    period_days: 90,
    as_of: "2026-01-10T00:00:00Z",
    status: "ok",
    summary: {
      total_decisions: rows.length,
      decision_counts: {},
      incomplete_recording_count: 0,
      acceptance_by_class: {},
      acceptance_note: "",
      avg_execution_score: null,
      avg_timing_delta_pct: null,
      avg_funding_fidelity_pct: null,
    },
    rows,
  };
}

function makeScorecard(): EvaluationScorecard {
  return {
    portfolio_id: 1,
    period_days: 90,
    status: "ok",
    as_of: "2026-01-10T00:00:00Z",
    belief: {} as never,
    execution: {} as never,
    outcome: {} as never,
    verdict: { en: "AI is ahead this period.", th: "AI นำอยู่ในช่วงนี้", branch: "ai_ahead" },
    recent_grades: [{ recommendation_snapshot_id: 99, grade_kind: "PRIMARY", graded_at: "2026-01-09" } as never],
  };
}

beforeEach(() => {
  listCashAccounts.mockReset().mockResolvedValue([]);
  listLiabilities.mockReset().mockResolvedValue([]);
  getSnapshots.mockReset().mockResolvedValue([]);
  getCashAccountBalanceAsOf.mockReset();
  getLiabilityBalanceAsOf.mockReset();
  getNetWorthChangeAttribution.mockReset();
  listWealthGoals.mockReset().mockResolvedValue([]);
  getWealthFactualReview.mockReset().mockResolvedValue(makeFactualReview([]));
  getExecutionLedger.mockReset();
  getEvaluationScorecard.mockReset();
  isUnresolvedPortfolioError.mockReset().mockReturnValue(false);
  portfolioState = {
    portfolios: [],
    currentSelection: null,
    loading: false,
    error: null,
    reportUnresolvedPortfolio: vi.fn(),
  };
});

describe("Periodic Review page", () => {
  test("renders all four domain sections in fixed order: Net Worth, Goals, Execution, Evaluation", async () => {
    render(<PeriodicReviewPage />);
    const headings = await screen.findAllByRole("heading", { level: 2 });
    const texts = headings.map((h) => h.textContent);
    expect(texts).toEqual(["Net Worth", "Current goals", "Execution", "Evaluation"]);
  });

  test("Net Worth: insufficient history shows the truthful existing empty state, never a fabricated zero", async () => {
    render(<PeriodicReviewPage />);
    expect(await screen.findByText("Two complete Net Worth history points are needed.")).toBeInTheDocument();
    expect(getNetWorthChangeAttribution).not.toHaveBeenCalled();
  });

  test("Goals: active goal renders, archived goal does not", async () => {
    listWealthGoals.mockResolvedValue([
      makeGoal({ id: 1, name: "Retirement" }),
      makeGoal({ id: 2, name: "Old car", is_archived: true }),
    ]);
    getWealthFactualReview.mockResolvedValue(
      makeFactualReview([
        makeContextGoal({ id: 1, name: "Retirement" }),
        makeContextGoal({ id: 2, name: "Old car", is_archived: true }),
      ])
    );

    render(<PeriodicReviewPage />);

    expect(await screen.findByText("Retirement")).toBeInTheDocument();
    expect(screen.queryByText("Old car")).not.toBeInTheDocument();
  });

  test("Goals: no source coverage status language leaks into this section", async () => {
    listWealthGoals.mockResolvedValue([makeGoal({ id: 1, name: "Retirement" })]);
    getWealthFactualReview.mockResolvedValue(makeFactualReview([makeContextGoal({ id: 1, name: "Retirement" })]));

    render(<PeriodicReviewPage />);
    await screen.findByText("Retirement");

    for (const forbidden of ["OVER_ALLOCATED", "over-allocated", "UNAVAILABLE", "needs review", "at risk"]) {
      expect(screen.queryByText(new RegExp(forbidden, "i"))).not.toBeInTheDocument();
    }
  });

  test("Execution: reviewable-without-review row appears under Needs review; a reviewed row does not", async () => {
    portfolioState = { ...portfolioState, portfolios: [makePortfolio(1)], currentSelection: 1 };
    getExecutionLedger.mockResolvedValue(
      makeLedger([
        makeRow({ decision_id: 101, snapshot_id: 201, reviewable: true, has_review: false }),
        makeRow({ decision_id: 102, snapshot_id: 202, reviewable: true, has_review: true, review_outcome: "ON_TRACK" as never }),
      ])
    );
    getEvaluationScorecard.mockResolvedValue(makeScorecard());

    render(<PeriodicReviewPage />);

    const section = (await screen.findByText("Needs review (1)")).closest("div") as HTMLElement;
    expect(within(section).getByText(/#201/)).toBeInTheDocument();
    expect(within(section).queryByText(/#202/)).not.toBeInTheDocument();
  });

  test("Evaluation: renders verdict and as_of, never the Recent Grades list, and links to /ai-analytics", async () => {
    portfolioState = { ...portfolioState, portfolios: [makePortfolio(1)], currentSelection: 1 };
    getExecutionLedger.mockResolvedValue(makeLedger([]));
    getEvaluationScorecard.mockResolvedValue(makeScorecard());

    render(<PeriodicReviewPage />);

    expect(await screen.findByText("AI is ahead this period.")).toBeInTheDocument();
    expect(screen.getByText(/As of 2026-01-10/)).toBeInTheDocument();
    expect(screen.queryByText("Recent Grades")).not.toBeInTheDocument();
    expect(screen.queryByText(/Rec #99/)).not.toBeInTheDocument();
    const link = screen.getByRole("link", { name: /Full AI Scorecard/i });
    expect(link).toHaveAttribute("href", "/ai-analytics");
  });

  test("mixed scope: no selected portfolio leaves Net Worth and Goals functional and shows a truthful unavailable state for Execution/Evaluation", async () => {
    listWealthGoals.mockResolvedValue([makeGoal({ id: 1, name: "Retirement" })]);
    getWealthFactualReview.mockResolvedValue(makeFactualReview([makeContextGoal({ id: 1, name: "Retirement" })]));
    portfolioState = { ...portfolioState, portfolios: [], currentSelection: null };

    render(<PeriodicReviewPage />);

    expect(await screen.findByText("Retirement")).toBeInTheDocument();
    expect(screen.getByText("Two complete Net Worth history points are needed.")).toBeInTheDocument();
    expect(screen.getByText("Select a portfolio to view Execution.")).toBeInTheDocument();
    expect(screen.getByText("Select a portfolio to view Evaluation.")).toBeInTheDocument();
    expect(getExecutionLedger).not.toHaveBeenCalled();
    expect(getEvaluationScorecard).not.toHaveBeenCalled();
  });

  test("failure isolation: Execution request failing does not remove Goals, Net Worth, or Evaluation", async () => {
    portfolioState = { ...portfolioState, portfolios: [makePortfolio(1)], currentSelection: 1 };
    listWealthGoals.mockResolvedValue([makeGoal({ id: 1, name: "Retirement" })]);
    getWealthFactualReview.mockResolvedValue(makeFactualReview([makeContextGoal({ id: 1, name: "Retirement" })]));
    getExecutionLedger.mockRejectedValue(new Error("boom"));
    getEvaluationScorecard.mockResolvedValue(makeScorecard());

    render(<PeriodicReviewPage />);

    await waitFor(() => expect(screen.getByRole("alert")).toHaveTextContent("boom"));
    expect(screen.getByText("Retirement")).toBeInTheDocument();
    expect(screen.getByText("Two complete Net Worth history points are needed.")).toBeInTheDocument();
    expect(await screen.findByText("AI is ahead this period.")).toBeInTheDocument();
  });

  test("scope disclosure names the selected portfolio", async () => {
    portfolioState = { ...portfolioState, portfolios: [makePortfolio(1)], currentSelection: 1 };
    getExecutionLedger.mockResolvedValue(makeLedger([]));
    getEvaluationScorecard.mockResolvedValue(makeScorecard());

    render(<PeriodicReviewPage />);

    expect(await screen.findByText("Execution and evaluation reflect Portfolio 1.")).toBeInTheDocument();
  });
});
