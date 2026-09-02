import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { DecisionActionPanel } from "@/components/optimizer/DecisionActionPanel";
import type { ExecutionDecision, ExecutionDecisionDetail } from "@/lib/api";

// Decision Continuity UX Slice 1 (D): DecisionActionPanel enriches its
// existing single-decision fetch with already-persisted goal provenance
// (Phase 7.4/ADR-008, CONTEXT_ONLY) and renders a small "Goal: X" chip when
// present. These tests exercise that addition in isolation — REJECTED is
// used throughout because it is outside RECORD_EXECUTION_ELIGIBLE and not
// APPROVED, so neither the shadow-performance nor execution-linkage effects
// fire, keeping the fixture to exactly what this behavior needs.

const {
  listExecutionDecisions, getExecutionDecision, getExecutionDetail,
  getShadowPerformanceSummary, recordDecisionBySnapshot,
} = vi.hoisted(() => ({
  listExecutionDecisions: vi.fn(),
  getExecutionDecision: vi.fn(),
  getExecutionDetail: vi.fn(),
  getShadowPerformanceSummary: vi.fn(),
  recordDecisionBySnapshot: vi.fn(),
}));

vi.mock("@/lib/api", () => ({
  listExecutionDecisions, getExecutionDecision, getExecutionDetail,
  getShadowPerformanceSummary, recordDecisionBySnapshot,
}));

function baseDecision(overrides: Partial<ExecutionDecision> = {}): ExecutionDecision {
  return {
    id: 7,
    portfolio_id: 1,
    recommendation_snapshot_id: 5,
    optimizer_history_id: null,
    decision: "REJECTED",
    override_notes: null,
    override_type: null,
    original_symbol: null,
    replacement_symbol: null,
    reason_category: null,
    is_system_generated: false,
    executed_at: "2026-08-20T00:00:00Z",
    created_at: "2026-08-20T00:00:00Z",
    ...overrides,
  };
}

function decisionDetail(overrides: Partial<ExecutionDecisionDetail> = {}): ExecutionDecisionDetail {
  return {
    ...baseDecision(),
    approved_allocations: null,
    rejected_symbols: null,
    recommendation_snapshot: null,
    ...overrides,
  };
}

beforeEach(() => {
  listExecutionDecisions.mockReset();
  getExecutionDecision.mockReset();
  getExecutionDetail.mockReset();
  getShadowPerformanceSummary.mockReset();
  recordDecisionBySnapshot.mockReset();
});

describe("DecisionActionPanel goal provenance", () => {
  test("COMPLETE decision_context renders a goal chip with the goal name", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: {
          contract_version: "wealth.decision-goal-context.v1",
          source_goal_context_version: "wealth.goal-context.v1",
          decision_effect: "CONTEXT_ONLY",
          context_state: "COMPLETE",
          selected_goal_ids: [1],
          observed_at: "2026-08-20T00:00:00Z",
          goals: [{
            id: 1, name: "House Fund", goal_type: "HOUSE", priority: "HIGH",
            target_amount: 5_000_000, currency: "THB", target_date: null,
            is_archived: false, updated_at: "2026-08-20T00:00:00Z",
            designated_total: 1_000_000, progress_ratio: 0.2, progress_percent: 20,
            funding_gap: 4_000_000, fully_designated: false,
          }],
        },
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    expect(await screen.findByText(/Goal: House Fund/)).toBeInTheDocument();
  });

  test("multiple selected goals render a pluralized 'Goals:' chip listing every name", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: {
          contract_version: "wealth.decision-goal-context.v1",
          source_goal_context_version: "wealth.goal-context.v1",
          decision_effect: "CONTEXT_ONLY",
          context_state: "COMPLETE",
          selected_goal_ids: [1, 2],
          observed_at: "2026-08-20T00:00:00Z",
          goals: [
            {
              id: 1, name: "House Fund", goal_type: "HOUSE", priority: "HIGH",
              target_amount: 5_000_000, currency: "THB", target_date: null,
              is_archived: false, updated_at: "2026-08-20T00:00:00Z",
              designated_total: 1_000_000, progress_ratio: 0.2, progress_percent: 20,
              funding_gap: 4_000_000, fully_designated: false,
            },
            {
              id: 2, name: "Retirement", goal_type: "RETIREMENT", priority: "MEDIUM",
              target_amount: 10_000_000, currency: "THB", target_date: null,
              is_archived: false, updated_at: "2026-08-20T00:00:00Z",
              designated_total: 500_000, progress_ratio: 0.05, progress_percent: 5,
              funding_gap: 9_500_000, fully_designated: false,
            },
          ],
        },
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    expect(await screen.findByText("Goals: House Fund, Retirement")).toBeInTheDocument();
  });

  test("a legacy/unscoped run (decision_context null) renders no fabricated goal chip", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: null,
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    await waitFor(() => expect(getExecutionDecision).toHaveBeenCalledWith(7));
    expect(screen.queryByText(/^Goal/)).not.toBeInTheDocument();
  });

  test("an EMPTY context_state (no goals selected at run time) renders no goal chip", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: {
          contract_version: "wealth.decision-goal-context.v1",
          source_goal_context_version: "wealth.goal-context.v1",
          decision_effect: "CONTEXT_ONLY",
          context_state: "EMPTY",
          selected_goal_ids: [],
          observed_at: "2026-08-20T00:00:00Z",
          goals: [],
        },
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    await waitFor(() => expect(getExecutionDecision).toHaveBeenCalledWith(7));
    expect(screen.queryByText(/^Goal/)).not.toBeInTheDocument();
  });

  test("a getExecutionDecision failure fails closed to no goal chip, without breaking the rest of the panel", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockRejectedValue(new Error("409 integrity error"));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    expect(await screen.findByText("Decision Recorded")).toBeInTheDocument();
    await waitFor(() => expect(getExecutionDecision).toHaveBeenCalledWith(7));
    expect(screen.queryByText(/^Goal/)).not.toBeInTheDocument();
  });
});

// Slice 2 (Decision Explainability Polish): the panel already fetches a full
// DecisionGoalContextGoal per selected goal (amount/date/priority/progress)
// but previously discarded everything but the name. These tests exercise the
// additive "Goal context at time of decision" block — it must render beside
// the existing name-only chip (all tests above keep passing unmodified),
// stay CONTEXT_ONLY (no causal language), and degrade gracefully.
describe("DecisionActionPanel goal context at time of decision", () => {
  test("COMPLETE context renders the historical-context label and goal name", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: {
          contract_version: "wealth.decision-goal-context.v1",
          source_goal_context_version: "wealth.goal-context.v1",
          decision_effect: "CONTEXT_ONLY",
          context_state: "COMPLETE",
          selected_goal_ids: [1],
          observed_at: "2026-08-20T00:00:00Z",
          goals: [{
            id: 1, name: "Retirement", goal_type: "RETIREMENT", priority: "HIGH",
            target_amount: 5_000_000, currency: "THB", target_date: "2035-12-15",
            is_archived: false, updated_at: "2026-08-20T00:00:00Z",
            designated_total: 3_100_000, progress_ratio: 0.62, progress_percent: 62,
            funding_gap: 1_900_000, fully_designated: false,
          }],
        },
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    expect(await screen.findByText("Goal context at time of decision")).toBeInTheDocument();
    // Existing Slice 1 chip is untouched:
    expect(await screen.findByText(/Goal: Retirement/)).toBeInTheDocument();
  });

  test("renders target amount, target date, priority, and funding progress from the fixture", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: {
          contract_version: "wealth.decision-goal-context.v1",
          source_goal_context_version: "wealth.goal-context.v1",
          decision_effect: "CONTEXT_ONLY",
          context_state: "COMPLETE",
          selected_goal_ids: [1],
          observed_at: "2026-08-20T00:00:00Z",
          goals: [{
            id: 1, name: "Retirement", goal_type: "RETIREMENT", priority: "HIGH",
            target_amount: 5_000_000, currency: "THB", target_date: "2035-12-15",
            is_archived: false, updated_at: "2026-08-20T00:00:00Z",
            designated_total: 3_100_000, progress_ratio: 0.62, progress_percent: 62,
            funding_gap: 1_900_000, fully_designated: false,
          }],
        },
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    const row = await screen.findByText(/฿5,000,000 target/);
    // Frozen fixture values only — never a live/current recomputation.
    expect(row.textContent).toContain("Dec 2035");
    expect(row.textContent).toContain("62% funded");
    expect(row.textContent).toContain("High priority");
  });

  test("multiple goals are all represented, in payload order", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: {
          contract_version: "wealth.decision-goal-context.v1",
          source_goal_context_version: "wealth.goal-context.v1",
          decision_effect: "CONTEXT_ONLY",
          context_state: "COMPLETE",
          selected_goal_ids: [2, 1],
          observed_at: "2026-08-20T00:00:00Z",
          goals: [
            {
              id: 2, name: "Retirement", goal_type: "RETIREMENT", priority: "MEDIUM",
              target_amount: 10_000_000, currency: "THB", target_date: null,
              is_archived: false, updated_at: "2026-08-20T00:00:00Z",
              designated_total: 500_000, progress_ratio: 0.05, progress_percent: 5,
              funding_gap: 9_500_000, fully_designated: false,
            },
            {
              id: 1, name: "House Fund", goal_type: "HOUSE", priority: "HIGH",
              target_amount: 5_000_000, currency: "THB", target_date: null,
              is_archived: false, updated_at: "2026-08-20T00:00:00Z",
              designated_total: 1_000_000, progress_ratio: 0.2, progress_percent: 20,
              funding_gap: 4_000_000, fully_designated: false,
            },
          ],
        },
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    await screen.findByText("Goal context at time of decision");
    const names = screen.getAllByText(/Retirement|House Fund/, { selector: "span.font-semibold" });
    expect(names.map((n) => n.textContent)).toEqual(["Retirement", "House Fund"]);
  });

  test("a missing target date degrades gracefully — no crash, no fabricated date", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: {
          contract_version: "wealth.decision-goal-context.v1",
          source_goal_context_version: "wealth.goal-context.v1",
          decision_effect: "CONTEXT_ONLY",
          context_state: "COMPLETE",
          selected_goal_ids: [1],
          observed_at: "2026-08-20T00:00:00Z",
          goals: [{
            id: 1, name: "Retirement", goal_type: "RETIREMENT", priority: "LOW",
            target_amount: 5_000_000, currency: "THB", target_date: null,
            is_archived: false, updated_at: "2026-08-20T00:00:00Z",
            designated_total: 3_100_000, progress_ratio: 0.62, progress_percent: 62,
            funding_gap: 1_900_000, fully_designated: false,
          }],
        },
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    const row = await screen.findByText(/฿5,000,000 target/);
    expect(row.textContent).not.toMatch(/·\s*·/); // no doubled/empty separator
    expect(row.textContent).toContain("62% funded");
  });

  test("null decision_context renders no goal context block", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: null,
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    await waitFor(() => expect(getExecutionDecision).toHaveBeenCalledWith(7));
    expect(screen.queryByText("Goal context at time of decision")).not.toBeInTheDocument();
  });

  test("a getExecutionDecision failure leaves decision mechanics usable and renders no goal context block", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockRejectedValue(new Error("409 integrity error"));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    expect(await screen.findByText("Decision Recorded")).toBeInTheDocument();
    await waitFor(() => expect(getExecutionDecision).toHaveBeenCalledWith(7));
    expect(screen.queryByText("Goal context at time of decision")).not.toBeInTheDocument();
  });

  test("the goal-context block never contains causal language", async () => {
    listExecutionDecisions.mockResolvedValue([baseDecision()]);
    getExecutionDecision.mockResolvedValue(decisionDetail({
      recommendation_snapshot: {
        id: 5, persona: "Balanced", total_portfolio_value: 1_000_000,
        created_at: "2026-08-20T00:00:00Z", regime: null, consensus: null, projected_allocations: null,
        decision_context: {
          contract_version: "wealth.decision-goal-context.v1",
          source_goal_context_version: "wealth.goal-context.v1",
          decision_effect: "CONTEXT_ONLY",
          context_state: "COMPLETE",
          selected_goal_ids: [1],
          observed_at: "2026-08-20T00:00:00Z",
          goals: [{
            id: 1, name: "Retirement", goal_type: "RETIREMENT", priority: "HIGH",
            target_amount: 5_000_000, currency: "THB", target_date: "2035-12-15",
            is_archived: false, updated_at: "2026-08-20T00:00:00Z",
            designated_total: 3_100_000, progress_ratio: 0.62, progress_percent: 62,
            funding_gap: 1_900_000, fully_designated: false,
          }],
        },
      },
    }));

    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);

    const block = await screen.findByText("Goal context at time of decision");
    const container = block.closest("div") ?? block;
    const text = container.textContent?.toLowerCase() ?? "";
    expect(text).not.toMatch(/because|caused by|recommended due to/);
  });
});
