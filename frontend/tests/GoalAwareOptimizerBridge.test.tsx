import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import GoalConstraintDisclosure from "@/components/optimizer/GoalConstraintDisclosure";
import OptimizerPage from "@/app/optimizer/page";
import {
  getOperationsStatus,
  getOptimizerHistory,
  getPortfolioPersona,
  listOptimizerHistory,
  listStrategyProfiles,
  listWealthGoals,
  runOptimizer,
  type GoalRecommendationConstraintEvidence,
  type OptimizerResult,
  type WealthGoal,
} from "@/lib/api";

let currentSelection: number | null = 1;
const portfolios = [
  { id: 1, name: "Core", cash_balance: 10_000, created_at: "2026-01-01" },
  { id: 2, name: "Income", cash_balance: 5_000, created_at: "2026-01-01" },
];

vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => ({
    portfolios,
    currentSelection,
    reportUnresolvedPortfolio: vi.fn(),
  }),
}));

vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(),
  useRouter: () => ({ push: vi.fn() }),
}));

vi.mock("@/lib/api", () => ({
  runOptimizer: vi.fn(),
  listOptimizerHistory: vi.fn(),
  getOptimizerHistory: vi.fn(),
  listStrategyProfiles: vi.fn(),
  getPortfolioPersona: vi.fn(),
  updatePortfolioPersona: vi.fn(),
  listWealthGoals: vi.fn(),
  recordDecisionBySnapshot: vi.fn(),
  listExecutionDecisions: vi.fn(),
  getDecisionMemoryTimeline: vi.fn(),
  getShadowPerformanceSummary: vi.fn(),
  getOperationsStatus: vi.fn(),
  isUnresolvedPortfolioError: vi.fn(() => false),
  getExecutionDetail: vi.fn(),
}));

vi.mock("@/components/WorkspaceScopeSwitcher", () => ({ default: () => <div>Portfolio switcher</div> }));
vi.mock("@/components/optimizer/ExecutionPlanCard", () => ({ default: () => null }));
vi.mock("@/components/operations-center/quant/OperationsTimeline", () => ({ default: () => null }));

const listGoalsMock = vi.mocked(listWealthGoals);
const runOptimizerMock = vi.mocked(runOptimizer);

const eligibleGoal: WealthGoal = {
  id: 11, workspace_id: 1, name: "Home", goal_type: "HOUSE", target_amount: 1_000_000,
  currency: "THB", target_date: "2030-01-01", priority: "HIGH", note: null,
  is_archived: false, created_at: "2026-01-01", updated_at: "2026-01-01",
};

const result: OptimizerResult = {
  portfolio_name: "Core", portfolio_assessment: "Assessment", optimization_notes: "Notes",
  swap_suggestions: [], watchlist_ranking: [], analyzed_at: "2026-09-02T00:00:00Z",
  portfolio_count: 1, max_reached: false,
};

function evidence(overrides: Partial<GoalRecommendationConstraintEvidence> = {}): GoalRecommendationConstraintEvidence {
  return {
    contract_version: "wealth.goal-recommendation-constraints.v1",
    rule_set: { id: "GOAL_HORIZON_SINGLE_POSITION_CAP", version: "1" },
    source: "EXPLICIT_GOAL_ACTIVATION",
    activated_goal_id: 11,
    activation: { field: "goal_constraint_goal_id", mode: "EXPLICIT" },
    observed_is_archived: false,
    target_date: "2030-01-01",
    as_of_date: "2026-09-02",
    days_remaining: 365,
    matched_rule: "TARGET_DATE_WITHIN_365_DAYS",
    contribution: { constraint: "MAX_SINGLE_POSITION_PCT", upper_bound_pct: 20 },
    resolution: {
      pre_goal_effective_pct: 25,
      post_goal_effective_pct: 20,
      relation_to_base: "STRICTER_THAN_BASE",
      application_status: "APPLIED_AND_BINDING",
      resulting_binding_source: "WEALTH_GOAL_POLICY",
    },
    ...overrides,
  };
}

beforeEach(() => {
  currentSelection = 1;
  vi.clearAllMocks();
  listGoalsMock.mockResolvedValue([eligibleGoal]);
  vi.mocked(listOptimizerHistory).mockResolvedValue([]);
  vi.mocked(getOptimizerHistory).mockResolvedValue(result);
  vi.mocked(listStrategyProfiles).mockResolvedValue({ profiles: [] });
  vi.mocked(getPortfolioPersona).mockResolvedValue({ persona: "BALANCED", profile: {} as never });
  vi.mocked(getOperationsStatus).mockResolvedValue({ portfolio_summary: { snapshot_date: null, days_since_last_rebalance: null } } as never);
  runOptimizerMock.mockResolvedValue(result);
});

describe("Goal-aware Optimizer selector", () => {
  it("keeps ordinary optimization available while Goals load", async () => {
    let resolveGoals: (goals: WealthGoal[]) => void = () => {};
    listGoalsMock.mockReturnValue(new Promise((resolve) => { resolveGoals = resolve; }));
    render(<OptimizerPage />);

    expect(screen.getByLabelText("Goal constraint")).toBeDisabled();
    expect(screen.getByRole("button", { name: "Run Optimizer" })).toBeEnabled();
    resolveGoals([eligibleGoal]);
    expect(await screen.findByRole("option", { name: "Home — target 2030-01-01" })).toBeInTheDocument();
  });

  it("shows eligible Goals, excludes archived ones, and describes unavailable active Goals", async () => {
    listGoalsMock.mockResolvedValue([
      eligibleGoal,
      { ...eligibleGoal, id: 12, name: "Future", target_date: "2099-01-01" },
      { ...eligibleGoal, id: 13, name: "Old", is_archived: true },
      { ...eligibleGoal, id: 14, name: "No date", target_date: null },
      { ...eligibleGoal, id: 15, name: "Past", target_date: "2020-01-01" },
    ]);
    render(<OptimizerPage />);

    const select = await screen.findByLabelText("Goal constraint") as HTMLSelectElement;
    expect(within(select).getByRole("option", { name: "Home — target 2030-01-01" })).toBeInTheDocument();
    expect(within(select).getByRole("option", { name: "Future — target 2099-01-01" })).toBeInTheDocument();
    expect(within(select).queryByRole("option", { name: /Old|No date|Past/ })).not.toBeInTheDocument();
    expect(screen.getByText(/missing a target date/)).toBeInTheDocument();
    expect(screen.getByText(/past target date/)).toBeInTheDocument();
  });

  it("does not block the run on Goal fetch failure and retries", async () => {
    listGoalsMock.mockRejectedValueOnce(new Error("offline")).mockResolvedValueOnce([eligibleGoal]);
    render(<OptimizerPage />);

    expect(await screen.findByText("Goal constraints are unavailable.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Run Optimizer" })).toBeEnabled();
    fireEvent.click(screen.getByRole("button", { name: "Retry" }));
    expect(await screen.findByRole("option", { name: "Home — target 2030-01-01" })).toBeInTheDocument();
  });

  it("states when no active Goal is eligible", async () => {
    listGoalsMock.mockResolvedValue([
      { ...eligibleGoal, target_date: null },
      { ...eligibleGoal, id: 12, target_date: "2020-01-01" },
      { ...eligibleGoal, id: 13, is_archived: true },
    ]);
    render(<OptimizerPage />);

    expect(await screen.findByText("No eligible Goals are available.")).toBeInTheDocument();
  });

  it("sends the captured selected ID, deselects it, and disables the selector during a run", async () => {
    let resolveRun: (value: OptimizerResult) => void = () => {};
    runOptimizerMock.mockReturnValue(new Promise((resolve) => { resolveRun = resolve; }));
    render(<OptimizerPage />);
    const select = await screen.findByLabelText("Goal constraint") as HTMLSelectElement;
    await waitFor(() => expect(listOptimizerHistory).toHaveBeenCalled());

    fireEvent.change(select, { target: { value: "11" } });
    fireEvent.click(screen.getByRole("button", { name: "Run Optimizer" }));
    await waitFor(() => expect(runOptimizerMock).toHaveBeenCalledWith(1, undefined, undefined, undefined, 11));
    expect(select).toBeDisabled();
    resolveRun(result);
    await waitFor(() => expect(screen.getByRole("button", { name: "Run Optimizer" })).toBeEnabled());

    fireEvent.change(screen.getByLabelText("Goal constraint"), { target: { value: "" } });
    fireEvent.click(screen.getByRole("button", { name: "Run Optimizer" }));
    await waitFor(() => expect(runOptimizerMock).toHaveBeenLastCalledWith(1, undefined, undefined, undefined, null));
  });

  it("resets the selector when the portfolio changes", async () => {
    const view = render(<OptimizerPage />);
    const select = await screen.findByLabelText("Goal constraint") as HTMLSelectElement;
    fireEvent.change(select, { target: { value: "11" } });
    expect(select.value).toBe("11");

    currentSelection = 2;
    view.rerender(<OptimizerPage />);

    await waitFor(() => expect(screen.getByLabelText("Goal constraint")).toHaveValue(""));
  });

  it("does not show the live missing-evidence warning for bootstrapped historical analysis", async () => {
    listOptimizerHistory.mockResolvedValue([{ id: 42, analyzed_at: "2026-09-01T00:00:00Z" } as never]);
    render(<OptimizerPage />);

    await waitFor(() => expect(getOptimizerHistory).toHaveBeenCalledWith(42));
    expect(screen.queryByText(/Goal constraint outcome metadata was unavailable/)).not.toBeInTheDocument();
  });
});

describe("Goal constraint disclosure", () => {
  it("renders binding evidence with frozen facts and current metadata", () => {
    render(<GoalConstraintDisclosure evidence={evidence()} currentGoalName="Renamed Home" />);

    expect(screen.getByText("Goal #11")).toBeInTheDocument();
    expect(screen.getByText("Target date:")).toHaveTextContent("Target date:");
    expect(screen.getByText("2030-01-01")).toBeInTheDocument();
    expect(screen.getByText("365 days remaining")).toBeInTheDocument();
    expect(screen.getByText("Applied and binding")).toBeInTheDocument();
    expect(screen.getByText(/25.0% to 20.0%/)).toBeInTheDocument();
    expect(screen.getByText("Current Goal name: Renamed Home")).toBeInTheDocument();
  });

  it("does not claim tightening for binding evidence whose relation is inconsistent", () => {
    render(<GoalConstraintDisclosure evidence={evidence({ resolution: {
      pre_goal_effective_pct: 25, post_goal_effective_pct: 20, relation_to_base: "EQUAL_TO_BASE",
      application_status: "APPLIED_AND_BINDING", resulting_binding_source: "WEALTH_GOAL_POLICY",
    } })} />);

    expect(screen.queryByText(/tightened max single-position exposure/)).not.toBeInTheDocument();
    expect(screen.getByText(/did not provide a confirmed cap-tightening detail/)).toBeInTheDocument();
  });

  it("renders equal, looser, and not-applicable backend statuses without inferring a rule", () => {
    const { rerender } = render(<GoalConstraintDisclosure evidence={evidence({ resolution: {
      pre_goal_effective_pct: 20, post_goal_effective_pct: 20, relation_to_base: "EQUAL_TO_BASE",
      application_status: "APPLIED_BUT_DOMINATED", resulting_binding_source: "REGIME_POLICY",
    } })} />);
    expect(screen.getByText("Applied, but not binding")).toBeInTheDocument();
    expect(screen.getByText(/already equal/)).toBeInTheDocument();

    rerender(<GoalConstraintDisclosure evidence={evidence({ resolution: {
      pre_goal_effective_pct: 18, post_goal_effective_pct: 18, relation_to_base: "LOOSER_THAN_BASE",
      application_status: "APPLIED_BUT_DOMINATED", resulting_binding_source: "REGIME_POLICY",
    } })} />);
    expect(screen.getByText(/already tighter/)).toBeInTheDocument();

    rerender(<GoalConstraintDisclosure evidence={evidence({ days_remaining: 366, matched_rule: null, contribution: null, resolution: {
      pre_goal_effective_pct: null, post_goal_effective_pct: null, relation_to_base: "NOT_APPLICABLE",
      application_status: "NOT_APPLICABLE", resulting_binding_source: null,
    } })} />);
    expect(screen.getByText("Not applicable for this run")).toBeInTheDocument();
    expect(screen.getByText("366 days remaining")).toBeInTheDocument();
  });

  it("handles missing evidence, null evidence, future statuses, and live missing metadata safely", () => {
    const { rerender } = render(<GoalConstraintDisclosure />);
    expect(screen.queryByLabelText("Goal constraint outcome")).not.toBeInTheDocument();

    rerender(<GoalConstraintDisclosure evidence={null} />);
    expect(screen.queryByLabelText("Goal constraint outcome")).not.toBeInTheDocument();

    rerender(<GoalConstraintDisclosure evidence={evidence({ resolution: {
      pre_goal_effective_pct: null, post_goal_effective_pct: null, relation_to_base: "NOT_APPLICABLE",
      application_status: "FUTURE_STATUS" as never, resulting_binding_source: null,
    } })} />);
    expect(screen.getByText(/Status unavailable \(FUTURE_STATUS\)/)).toBeInTheDocument();

    rerender(<GoalConstraintDisclosure evidence={null} expectedEvidence />);
    expect(screen.getByText(/Goal constraint outcome metadata was unavailable/)).toBeInTheDocument();
  });
});
