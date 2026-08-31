import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GoalDetailPage from "@/app/goals/[id]/page";
import {
  createGoalFundingAllocation,
  createGoalScenario,
  deleteGoalFundingAllocation,
  getHoldings,
  getPortfolioPrices,
  getWealthFactualReview,
  listCashAccounts,
  listGoalFundingAllocations,
  listGoalScenarios,
  listPortfolios,
  listWealthGoals,
  updateGoalFundingAllocation,
  updateGoalScenario,
  type CashAccount,
  type FactualReviewResponse,
  type GoalContextResponse,
  type GoalFundingAllocation,
  type GoalScenario,
  type Portfolio,
  type PortfolioItem,
  type PriceRefreshItem,
  type WealthGoal,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createGoalFundingAllocation: vi.fn(),
  createGoalScenario: vi.fn(),
  deleteGoalFundingAllocation: vi.fn(),
  getHoldings: vi.fn(),
  getPortfolioPrices: vi.fn(),
  getWealthFactualReview: vi.fn(),
  listCashAccounts: vi.fn(),
  listGoalFundingAllocations: vi.fn(),
  listGoalScenarios: vi.fn(),
  listPortfolios: vi.fn(),
  listWealthGoals: vi.fn(),
  updateGoalFundingAllocation: vi.fn(),
  updateGoalScenario: vi.fn(),
}));

const goal: WealthGoal = {
  id: 1,
  workspace_id: 1,
  name: "Retire by 55",
  goal_type: "RETIREMENT",
  target_amount: 20000000,
  currency: "THB",
  target_date: "2055-01-01",
  priority: "HIGH",
  note: "Discussed with spouse",
  is_archived: false,
  created_at: "2026-08-26T00:00:00",
  updated_at: "2026-08-26T00:00:00",
};

const cashAccount: CashAccount = {
  id: 5,
  workspace_id: 1,
  name: "Wedding Savings",
  institution: null,
  currency: "THB",
  balance: 300000,
  is_archived: false,
  created_at: "2026-08-26T00:00:00",
  updated_at: "2026-08-26T00:00:00",
};

const portfolio: Portfolio = {
  id: 9,
  name: "Long-term Portfolio",
  cash_balance: 0,
  created_at: "2026-08-26T00:00:00",
};

const cashAllocation: GoalFundingAllocation = {
  id: 100,
  workspace_id: 1,
  wealth_goal_id: 1,
  source_kind: "CASH_ACCOUNT",
  cash_account_id: 5,
  portfolio_id: null,
  source_name: "Wedding Savings",
  source_is_archived: false,
  allocated_amount: 300000,
  currency: "THB",
  created_at: "2026-08-26T00:00:00",
  updated_at: "2026-08-26T00:00:00",
};

const portfolioAllocation: GoalFundingAllocation = {
  id: 101,
  workspace_id: 1,
  wealth_goal_id: 1,
  source_kind: "PORTFOLIO",
  cash_account_id: null,
  portfolio_id: 9,
  source_name: "Long-term Portfolio",
  source_is_archived: false,
  allocated_amount: 700000,
  currency: "THB",
  created_at: "2026-08-26T00:00:00",
  updated_at: "2026-08-26T00:00:00",
};

const scenario: GoalScenario = {
  id: 500,
  workspace_id: 1,
  wealth_goal_id: 1,
  name: "Aggressive contribution",
  monthly_contribution: 20000,
  annual_return_pct: 6,
  is_archived: false,
  created_at: "2026-08-26T00:00:00",
  updated_at: "2026-08-26T00:00:00",
};

const archivedScenario: GoalScenario = {
  ...scenario,
  id: 501,
  name: "Old plan",
  is_archived: true,
};

const secondScenario: GoalScenario = {
  ...scenario,
  id: 502,
  name: "Conservative plan",
  monthly_contribution: 5000,
  annual_return_pct: 2,
};

const secondGoal: WealthGoal = {
  ...goal,
  id: 2,
  name: "Buy a home",
  goal_type: "HOUSE",
  target_amount: 5000000,
  priority: "MEDIUM",
};

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((nextResolve) => { resolve = nextResolve; });
  return { promise, resolve };
}

function holding(overrides: Partial<PortfolioItem> & { symbol: string; shares: number; avg_cost: number }): PortfolioItem {
  return {
    id: 0,
    portfolio_id: 9,
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
    ...overrides,
  };
}

function quote(symbol: string, current: number): PriceRefreshItem {
  return { symbol, current_price: current, previous_close: current, change_percent: 0, last_updated: null };
}

const listMock = vi.mocked(listWealthGoals);
const allocationsMock = vi.mocked(listGoalFundingAllocations);
const contextMock = vi.mocked(getWealthFactualReview);
const cashAccountsMock = vi.mocked(listCashAccounts);
const portfoliosMock = vi.mocked(listPortfolios);
const holdingsMock = vi.mocked(getHoldings);
const pricesMock = vi.mocked(getPortfolioPrices);
const allocationsCreateMock = vi.mocked(createGoalFundingAllocation);
const allocationsUpdateMock = vi.mocked(updateGoalFundingAllocation);
const allocationsDeleteMock = vi.mocked(deleteGoalFundingAllocation);
const scenariosMock = vi.mocked(listGoalScenarios);
const scenariosCreateMock = vi.mocked(createGoalScenario);
const scenariosUpdateMock = vi.mocked(updateGoalScenario);

async function configuredGoalContext(): Promise<GoalContextResponse> {
  const latestListResult = listMock.mock.results[listMock.mock.results.length - 1] as
    { value: unknown } | undefined;
  const loadedGoals: WealthGoal[] = latestListResult
    ? await Promise.resolve(latestListResult.value).catch(() => []) as WealthGoal[]
    : [];
  const sourceTotals = new Map<string, {
    source_kind: "CASH_ACCOUNT" | "PORTFOLIO";
    source_id: number;
    source_name: string;
    source_is_archived: boolean;
    currency: "THB";
    designated_total_in_context_scope: number;
  }>();
  const allocationImplementation = allocationsMock.getMockImplementation() as
    ((goalId: number) => Promise<GoalFundingAllocation[]> | GoalFundingAllocation[]) | undefined;
  const goals = await Promise.all(loadedGoals.map(async (record) => {
    // Read the configured fixture implementation directly.  Production must
    // obtain this complete payload with one Goal Context request and make no
    // legacy per-goal allocation reads.
    const historicalAllocations = allocationImplementation ? await allocationImplementation(record.id) : [];
    const allocations = historicalAllocations.map((allocation) => {
      const sourceId = (allocation.cash_account_id ?? allocation.portfolio_id) as number;
      const contextAllocation = {
        id: allocation.id,
        wealth_goal_id: allocation.wealth_goal_id,
        source_kind: allocation.source_kind,
        source_id: sourceId,
        source_name: allocation.source_name ?? "Unknown source",
        source_is_archived: allocation.source_is_archived,
        designated_amount: allocation.allocated_amount,
        currency: allocation.currency,
        updated_at: allocation.updated_at,
      };
      const key = `${allocation.source_kind}:${sourceId}`;
      const existing = sourceTotals.get(key);
      if (existing) existing.designated_total_in_context_scope += allocation.allocated_amount;
      else sourceTotals.set(key, {
        source_kind: allocation.source_kind,
        source_id: sourceId,
        source_name: contextAllocation.source_name,
        source_is_archived: contextAllocation.source_is_archived,
        currency: "THB",
        designated_total_in_context_scope: allocation.allocated_amount,
      });
      return contextAllocation;
    });
    const designatedTotal = allocations.reduce((sum, allocation) => sum + allocation.designated_amount, 0);
    const progressRatio = designatedTotal / record.target_amount;
    return {
      id: record.id,
      name: record.name,
      goal_type: record.goal_type,
      target_amount: record.target_amount,
      currency: record.currency,
      target_date: record.target_date,
      priority: record.priority,
      is_archived: record.is_archived,
      updated_at: record.updated_at,
      allocations,
      designated_total: designatedTotal,
      progress_ratio: progressRatio,
      progress_percent: progressRatio * 100,
      funding_gap: Math.max(record.target_amount - designatedTotal, 0),
      fully_designated: designatedTotal >= record.target_amount,
    };
  }));
  return {
    contract_version: "wealth.goal-context.v1",
    context_generated_at: "2026-08-26T00:00:00Z",
    completeness: "COMPLETE",
    scope: { kind: "WORKSPACE", include_archived: true },
    goals,
    designation_by_source: [...sourceTotals.values()],
  };
}

async function configuredFactualReview(): Promise<FactualReviewResponse> {
  const goal_context = await configuredGoalContext();
  const cashImplementation = cashAccountsMock.getMockImplementation() as
    ((includeArchived?: boolean) => Promise<CashAccount[]> | CashAccount[]) | undefined;
  const accountList = cashImplementation ? await cashImplementation(true) : [];
  return {
    contract_version: "wealth.factual-review.v1",
    review_generated_at: "2026-08-26T00:00:00Z",
    scope: goal_context.scope,
    goal_context,
    valuation_completeness: "COMPLETE",
    sources: goal_context.designation_by_source.map((designation) => {
      const account = designation.source_kind === "CASH_ACCOUNT"
        ? accountList.find((candidate) => candidate.id === designation.source_id)
        : undefined;
      const observed = account?.balance ?? null;
      return {
        ...designation,
        valuation: {
          availability: observed === null ? "UNAVAILABLE" as const : "AVAILABLE" as const,
          observed_value: observed,
          as_of: account?.updated_at ?? null,
          provenance: account ? "CASH_ACCOUNT_CURRENT_BALANCE" as const : null,
          quality: account ? "COMPLETE" as const : null,
        },
        designation_coverage: {
          status: observed === null ? "UNAVAILABLE" as const
            : observed < designation.designated_total_in_context_scope ? "OVER_ALLOCATED" as const : "SUPPORTED" as const,
          shortfall: observed !== null && observed < designation.designated_total_in_context_scope
            ? designation.designated_total_in_context_scope - observed : null,
        },
      };
    }),
  };
}

describe("GoalDetailPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([goal]);
    allocationsMock.mockResolvedValue([]);
    contextMock.mockImplementation(configuredFactualReview);
    cashAccountsMock.mockResolvedValue([cashAccount]);
    portfoliosMock.mockResolvedValue([portfolio]);
    holdingsMock.mockResolvedValue([]);
    pricesMock.mockResolvedValue([]);
    allocationsCreateMock.mockResolvedValue(cashAllocation);
    allocationsUpdateMock.mockResolvedValue(cashAllocation);
    allocationsDeleteMock.mockResolvedValue({ deleted: 100 });
    scenariosMock.mockResolvedValue([]);
    scenariosCreateMock.mockResolvedValue(scenario);
    scenariosUpdateMock.mockResolvedValue(scenario);
  });

  it("loads a valid URL-anchored goal and keeps a back link", async () => {
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(screen.getByText("Loading goal…")).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "Retire by 55" })).toBeInTheDocument();
    expect(listMock).toHaveBeenCalledWith(true);
    expect(contextMock).toHaveBeenCalledWith(true);
    expect(contextMock).toHaveBeenCalledTimes(1);
    expect(allocationsMock).not.toHaveBeenCalled();
    expect(screen.getByRole("link", { name: "← Back to goals" })).toHaveAttribute("href", "/goals");
  });

  it("renders goal metadata, target, progress, and funding gap", async () => {
    listMock.mockResolvedValue([{ ...goal, target_amount: 1000000 }]);
    allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 300000 }]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    await screen.findByRole("heading", { name: "Retire by 55" });
    expect(screen.getByText("Goal Summary")).toBeInTheDocument();
    expect(screen.getByText("Retirement · High priority")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "฿1,000,000.00 target")).toBeInTheDocument();
    expect(screen.getByText("Target date: 2055-01-01")).toBeInTheDocument();
    expect(screen.getByText("Designated funding")).toBeInTheDocument();
    expect(screen.getByText("Goal progress")).toBeInTheDocument();
    expect(screen.getByText("30%")).toBeInTheDocument();
    expect(screen.getByText("Funding gap")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "฿700,000.00")).toBeInTheDocument();
  });

  it("renders allocations and preserves add, edit, and remove semantics", async () => {
    allocationsMock.mockResolvedValue([cashAllocation]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    await screen.findByText((_, element) => element?.textContent === "Wedding Savings (Cash Account)");

    fireEvent.change(screen.getByLabelText("Funding source"), { target: { value: "5" } });
    fireEvent.change(screen.getByLabelText("Designated amount"), { target: { value: "250000" } });
    fireEvent.click(screen.getByRole("button", { name: "Add funding source" }));
    await waitFor(() => expect(allocationsCreateMock).toHaveBeenCalledWith(1, {
      cash_account_id: 5,
      portfolio_id: undefined,
      allocated_amount: 250000,
      currency: "THB",
    }));
    await waitFor(() => expect(contextMock).toHaveBeenCalledTimes(2));

    fireEvent.click(screen.getByRole("button", { name: "Edit designated amount for Wedding Savings" }));
    fireEvent.change(screen.getByLabelText("Edit designated amount for Wedding Savings"), { target: { value: "200000" } });
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    await waitFor(() => expect(allocationsUpdateMock).toHaveBeenCalledWith(1, 100, { allocated_amount: 200000 }));
    await waitFor(() => expect(contextMock).toHaveBeenCalledTimes(3));

    fireEvent.click(screen.getByRole("button", { name: "Remove Wedding Savings as a funding source" }));
    await waitFor(() => expect(allocationsDeleteMock).toHaveBeenCalledWith(1, 100));
    await waitFor(() => expect(contextMock).toHaveBeenCalledTimes(4));
  });

  it("removes stale pre-mutation totals when Goal Context refresh fails", async () => {
    allocationsMock.mockResolvedValue([cashAllocation]);
    contextMock
      .mockImplementationOnce(configuredFactualReview)
      .mockRejectedValueOnce(new Error("context refresh offline"));
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("฿300,000.00 designated")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Remove Wedding Savings as a funding source" }));
    expect(await screen.findByText("context refresh offline")).toBeInTheDocument();
    expect(screen.queryByText("฿300,000.00 designated")).not.toBeInTheDocument();
    expect(screen.getByText("Goal progress unavailable — funding data failed to load.")).toBeInTheDocument();
  });

  it("reports Funding Health as supported", async () => {
    cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 450000 }]);
    allocationsMock.mockResolvedValue([cashAllocation]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    await screen.findByText((_, element) => element?.textContent === "Observed value ฿450,000.00 · Funding health: Supported");
  });

  it("renders opaque server-returned coverage without recomputing it", async () => {
    allocationsMock.mockResolvedValue([cashAllocation]);
    contextMock.mockImplementation(async () => {
      const response = await configuredFactualReview();
      response.sources[0].valuation.observed_value = 900000;
      response.sources[0].designation_coverage = { status: "OVER_ALLOCATED", shortfall: 17 };
      return response;
    });
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText((_, element) => element?.textContent === "Observed value ฿900,000.00 · Attention: exceeds observed value by ฿17.00")).toBeInTheDocument();
  });

  it("fails closed when factual-review source facts disagree with embedded Goal Context", async () => {
    allocationsMock.mockResolvedValue([cashAllocation]);
    contextMock.mockImplementation(async () => {
      const response = await configuredFactualReview();
      response.sources[0].currency = "USD" as "THB";
      return response;
    });
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("Goal progress unavailable — funding data failed to load.")).toBeInTheDocument();
    expect(screen.queryByText(/Funding health: Supported/)).not.toBeInTheDocument();
  });

  it("reports Funding Health as over-allocated", async () => {
    cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 100000 }]);
    allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 300000 }]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText((_, element) => element?.textContent === "Observed value ฿100,000.00 · Attention: exceeds observed value by ฿200,000.00")).toBeInTheDocument();
  });

  it("uses complete cross-goal allocation evidence for shared-source Funding Health", async () => {
    cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 400000 }]);
    listMock.mockResolvedValue([goal, secondGoal]);
    allocationsMock.mockImplementation(async (goalId) => goalId === 1
      ? [cashAllocation]
      : [{ ...cashAllocation, id: 200, wealth_goal_id: 2, allocated_amount: 200000 }]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText((_, element) => element?.textContent === "Observed value ฿400,000.00 · Attention: exceeds observed value by ฿100,000.00")).toBeInTheDocument();
  });

  it("fails the selected goal honestly when the complete workspace Goal Context fails", async () => {
    listMock.mockResolvedValue([goal, secondGoal]);
    allocationsMock.mockImplementation(async (goalId) => {
      if (goalId === 1) return [cashAllocation];
      throw new Error("other allocation read failed");
    });
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("other allocation read failed")).toBeInTheDocument();
    expect(screen.getByText("Goal progress unavailable — funding data failed to load.")).toBeInTheDocument();
    expect(screen.queryByText("฿300,000.00 designated")).not.toBeInTheDocument();
  });

  it("keeps Funding Health unavailable when source valuation fails", async () => {
    allocationsMock.mockResolvedValue([portfolioAllocation]);
    holdingsMock.mockRejectedValue(new Error("holdings offline"));
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("Observed value unavailable · Funding health unavailable")).toBeInTheDocument();
    expect(screen.getByText("Goal progress")).toBeInTheDocument();
    expect(screen.getByText("4%")).toBeInTheDocument();
  });

  it("uses server review evidence and makes no Portfolio holdings or price requests", async () => {
    allocationsMock.mockResolvedValue([portfolioAllocation]);
    holdingsMock.mockResolvedValue([holding({ symbol: "AAA", shares: 10000, avg_cost: 50 })]);
    pricesMock.mockResolvedValue([quote("AAA", 90)]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("Observed value unavailable · Funding health unavailable")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Long-term Portfolio: observed value unavailable")).toBeInTheDocument();
    expect(holdingsMock).not.toHaveBeenCalled();
    expect(pricesMock).not.toHaveBeenCalled();
  });

  it("runs the forward What-If from designated funding", async () => {
    allocationsMock.mockResolvedValue([]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    await screen.findByRole("heading", { name: "Retire by 55" });
    fireEvent.click(screen.getByRole("button", { name: "What-If" }));
    fireEvent.change(screen.getByLabelText("What-If monthly contribution for Retire by 55"), { target: { value: "100000" } });
    expect(await screen.findByText(/Monthly contribution: ฿100,000\.00 · Annual return assumption: 0%/)).toBeInTheDocument();
  });

  it("runs the required monthly contribution calculation", async () => {
    listMock.mockResolvedValue([{ ...goal, target_amount: 1200000, target_date: "2027-01-01" }]);
    allocationsMock.mockResolvedValue([]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    await screen.findByRole("heading", { name: "Retire by 55" });
    fireEvent.click(screen.getByRole("button", { name: "What-If" }));
    fireEvent.click(screen.getByRole("button", { name: "How much per month do I need?" }));
    expect(await screen.findByText(/Under this assumption, contributing ฿[\d,]+\.\d{2} per month would reach the current target by 2027-01-01\./)).toBeInTheDocument();
    expect(screen.getByText("Saved target date: 2027-01-01 · Annual return assumption: 0%")).toBeInTheDocument();
  });

  it("keeps allocation failure honest across progress, funding, and What-If", async () => {
    allocationsMock.mockRejectedValue(new Error("allocations offline"));
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("allocations offline")).toBeInTheDocument();
    expect(screen.getByText("Goal progress unavailable — funding data failed to load.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "What-If" }));
    expect(screen.getByText("What-If unavailable — funding data failed to load.")).toBeInTheDocument();
  });

  it("does not treat portfolio valuation failure as zero or erase designated progress", async () => {
    listMock.mockResolvedValue([{ ...goal, target_amount: 1000000 }]);
    allocationsMock.mockResolvedValue([portfolioAllocation]);
    holdingsMock.mockRejectedValue(new Error("valuation offline"));
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("Observed value unavailable · Funding health unavailable")).toBeInTheDocument();
    expect(screen.getByText("70%")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "฿700,000.00")).toBeInTheDocument();
  });

  it("rejects mismatched editable-record and Goal Context generations", async () => {
    allocationsMock.mockResolvedValue([cashAllocation]);
    contextMock.mockImplementation(async () => {
      const response = await configuredFactualReview();
      response.goal_context.goals[0].updated_at = "2026-08-26T00:00:01";
      return response;
    });
    render(<GoalDetailPage params={{ id: "1" }} />);

    expect(await screen.findByText("Goal progress unavailable — funding data failed to load.")).toBeInTheDocument();
    expect(screen.queryByText("฿300,000.00 designated")).not.toBeInTheDocument();
  });

  it("renders a goal-not-found state", async () => {
    listMock.mockResolvedValue([]);
    render(<GoalDetailPage params={{ id: "99" }} />);
    expect(await screen.findByRole("alert")).toHaveTextContent("Goal not found.");
  });

  it("renders an API failure state", async () => {
    listMock.mockRejectedValue(new Error("goals offline"));
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByRole("alert")).toHaveTextContent("goals offline");
  });

  it("does not render an older goal after a dynamic route transition", async () => {
    const firstResponse = deferred<WealthGoal[]>();
    listMock.mockImplementationOnce(() => firstResponse.promise).mockResolvedValueOnce([secondGoal]);
    const { rerender } = render(<GoalDetailPage params={{ id: "1" }} />);
    await waitFor(() => expect(listMock).toHaveBeenCalledWith(true));
    rerender(<GoalDetailPage params={{ id: "2" }} />);
    expect(await screen.findByRole("heading", { name: "Buy a home" })).toBeInTheDocument();
    firstResponse.resolve([goal]);
    await waitFor(() => expect(screen.queryByRole("heading", { name: "Retire by 55" })).not.toBeInTheDocument());
    expect(screen.getByRole("heading", { name: "Buy a home" })).toBeInTheDocument();
  });

  it("keeps archived goal planning read-only while preserving its evidence", async () => {
    listMock.mockResolvedValue([{ ...goal, is_archived: true }]);
    allocationsMock.mockResolvedValue([cashAllocation]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("Funding sources are read-only while this goal is archived.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Add funding source" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Edit designated amount for Wedding Savings" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Remove Wedding Savings as a funding source" })).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "What-If" })).toBeInTheDocument();
  });

  it("uses a responsive, sectioned mobile-friendly structure", async () => {
    render(<GoalDetailPage params={{ id: "1" }} />);
    const main = await screen.findByRole("main");
    expect(main).toHaveClass("max-w-4xl");
    expect(screen.getByRole("heading", { name: "Goal Summary" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Funding" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Planning / What-If" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Saved Scenarios" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "What-If" }));
    expect(screen.getByLabelText("What-If monthly contribution for Retire by 55")).toHaveClass("mt-1", "block", "w-full");
  });

  it("does not introduce predictive, advisory, or guarantee wording", async () => {
    listMock.mockResolvedValue([{ ...goal, target_amount: 1200000, target_date: "2027-01-01" }]);
    allocationsMock.mockResolvedValue([]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    await screen.findByRole("heading", { name: "Retire by 55" });
    fireEvent.click(screen.getByRole("button", { name: "What-If" }));
    fireEvent.change(screen.getByLabelText("What-If monthly contribution for Retire by 55"), { target: { value: "50000" } });
    await screen.findByText(/Saved target date: 2027-01-01/);
    expect(screen.queryByText(/forecast|expected return|probability|guaranteed|on track|likely to|recommended contribution|should contribute|advice/i)).not.toBeInTheDocument();
  });

  describe("Saved Scenarios", () => {
    // 1. empty state
    it("shows an empty state when no scenarios are saved", async () => {
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByRole("heading", { name: "Retire by 55" });
      expect(await screen.findByText("No saved scenarios yet.")).toBeInTheDocument();
    });

    // 17. assumptions-only disclosure
    it("shows the assumptions-only disclosure", async () => {
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByRole("heading", { name: "Retire by 55" });
      expect(await screen.findByText(
        "Saved scenarios store assumptions only. Results use the goal's current target and designated funding.",
      )).toBeInTheDocument();
    });

    // 2. save current What-If assumptions
    it("saves the current forward What-If assumptions as a named scenario", async () => {
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByRole("heading", { name: "Retire by 55" });
      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      fireEvent.change(screen.getByLabelText("What-If monthly contribution for Retire by 55"), { target: { value: "20000" } });
      fireEvent.change(screen.getByLabelText("What-If annual return assumption for Retire by 55"), { target: { value: "6" } });
      fireEvent.click(screen.getByRole("button", { name: "Save scenario" }));
      fireEvent.change(screen.getByLabelText("Scenario name for Retire by 55"), { target: { value: "Aggressive contribution" } });
      fireEvent.click(screen.getByRole("button", { name: "Save" }));
      await waitFor(() => expect(scenariosCreateMock).toHaveBeenCalledWith(1, {
        name: "Aggressive contribution",
        monthly_contribution: 20000,
        annual_return_pct: 6,
      }));
      expect(await screen.findByText("Scenario saved.")).toBeInTheDocument();
    });

    // 3. scenario list
    it("lists saved scenarios with their assumptions", async () => {
      scenariosMock.mockResolvedValue([scenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText((_, element) => element?.textContent === "Aggressive contribution (฿20,000.00/month · 6% annual return assumption)")).toBeInTheDocument();
    });

    // 4, 5. load scenario populates What-If fields and recomputes live
    it("loads a scenario into the What-If assumptions and recomputes against current goal state", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000 }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockResolvedValue([scenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByRole("heading", { name: "Retire by 55" });

      fireEvent.click(await screen.findByRole("button", { name: "Load Aggressive contribution scenario" }));

      expect(await screen.findByLabelText("What-If monthly contribution for Retire by 55")).toHaveValue(20000);
      expect(screen.getByLabelText("What-If annual return assumption for Retire by 55")).toHaveValue(6);
      // Recomputed live against the current designated funding (100,000), not any value stored on the scenario.
      expect(await screen.findByText(/Monthly contribution: ฿20,000\.00 · Annual return assumption: 6%/)).toBeInTheDocument();
    });

    // 6, 7. goal/funding changes are never stored on the scenario
    it("does not persist the goal's target or designated funding when saving a scenario", async () => {
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByRole("heading", { name: "Retire by 55" });
      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      fireEvent.change(screen.getByLabelText("What-If monthly contribution for Retire by 55"), { target: { value: "20000" } });
      fireEvent.change(screen.getByLabelText("What-If annual return assumption for Retire by 55"), { target: { value: "6" } });
      fireEvent.click(screen.getByRole("button", { name: "Save scenario" }));
      fireEvent.change(screen.getByLabelText("Scenario name for Retire by 55"), { target: { value: "Aggressive contribution" } });
      fireEvent.click(screen.getByRole("button", { name: "Save" }));
      await waitFor(() => expect(scenariosCreateMock).toHaveBeenCalled());
      const [, body] = scenariosCreateMock.mock.calls[0];
      expect(Object.keys(body)).toEqual(["name", "monthly_contribution", "annual_return_pct"]);
    });

    // 8. edit scenario
    it("edits a scenario's name and assumptions", async () => {
      scenariosMock.mockResolvedValue([scenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByRole("button", { name: "Edit Aggressive contribution scenario" });

      fireEvent.click(screen.getByRole("button", { name: "Edit Aggressive contribution scenario" }));
      fireEvent.change(screen.getByLabelText("Edit name for Aggressive contribution"), { target: { value: "Renamed plan" } });
      fireEvent.change(screen.getByLabelText("Edit monthly contribution for Aggressive contribution"), { target: { value: "25000" } });
      fireEvent.change(screen.getByLabelText("Edit annual return assumption for Aggressive contribution"), { target: { value: "7" } });
      fireEvent.click(screen.getByRole("button", { name: "Save" }));

      await waitFor(() => expect(scenariosUpdateMock).toHaveBeenCalledWith(1, 500, {
        name: "Renamed plan",
        monthly_contribution: 25000,
        annual_return_pct: 7,
      }));
    });

    // 9. archive
    it("archives an active scenario", async () => {
      scenariosMock.mockResolvedValue([scenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      fireEvent.click(await screen.findByRole("button", { name: "Archive Aggressive contribution scenario" }));
      await waitFor(() => expect(scenariosUpdateMock).toHaveBeenCalledWith(1, 500, { is_archived: true }));
    });

    // 10. archived section
    it("reveals archived scenarios behind a toggle", async () => {
      scenariosMock.mockResolvedValue([scenario, archivedScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByText((_, element) => element?.textContent === "Aggressive contribution (฿20,000.00/month · 6% annual return assumption)");
      expect(screen.queryByText(/Old plan/)).not.toBeInTheDocument();

      fireEvent.click(screen.getByRole("button", { name: "Show archived scenarios (1)" }));
      expect(await screen.findByText(/Old plan/)).toBeInTheDocument();
    });

    // 11. restore
    it("restores an archived scenario", async () => {
      scenariosMock.mockResolvedValue([archivedScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      fireEvent.click(await screen.findByRole("button", { name: "Show archived scenarios (1)" }));
      fireEvent.click(await screen.findByRole("button", { name: "Restore Old plan scenario" }));
      await waitFor(() => expect(scenariosUpdateMock).toHaveBeenCalledWith(1, 501, { is_archived: false }));
    });

    // 12. archived scenario cannot edit
    it("does not offer an edit control for an archived scenario", async () => {
      scenariosMock.mockResolvedValue([archivedScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      fireEvent.click(await screen.findByRole("button", { name: "Show archived scenarios (1)" }));
      await screen.findByRole("button", { name: "Restore Old plan scenario" });
      expect(screen.queryByRole("button", { name: "Edit Old plan scenario" })).not.toBeInTheDocument();
    });

    // 13. archived parent read-only
    it("hides create, edit, archive, and restore controls while the parent goal is archived, but keeps Load available", async () => {
      listMock.mockResolvedValue([{ ...goal, is_archived: true }]);
      scenariosMock.mockResolvedValue([scenario, archivedScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByText((_, element) => element?.textContent === "Aggressive contribution (฿20,000.00/month · 6% annual return assumption)");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(screen.queryByRole("button", { name: "Save scenario" })).not.toBeInTheDocument();
      expect(screen.queryByRole("button", { name: "Edit Aggressive contribution scenario" })).not.toBeInTheDocument();
      expect(screen.queryByRole("button", { name: "Archive Aggressive contribution scenario" })).not.toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Load Aggressive contribution scenario" })).toBeInTheDocument();

      fireEvent.click(screen.getByRole("button", { name: "Show archived scenarios (1)" }));
      expect(screen.queryByRole("button", { name: "Restore Old plan scenario" })).not.toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Load Old plan scenario" })).toBeInTheDocument();
    });

    // 14. scenario API failure honesty
    it("reports a scenario list failure honestly", async () => {
      scenariosMock.mockRejectedValue(new Error("scenarios offline"));
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText("scenarios offline")).toBeInTheDocument();
    });

    // 15. route transition isolation
    it("does not show the previous goal's scenarios after a route transition", async () => {
      scenariosMock.mockImplementation(async (goalId) => (goalId === 1 ? [scenario] : []));
      const { rerender } = render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByText((_, element) => element?.textContent === "Aggressive contribution (฿20,000.00/month · 6% annual return assumption)");

      listMock.mockResolvedValue([goal, secondGoal]);
      rerender(<GoalDetailPage params={{ id: "2" }} />);
      await screen.findByRole("heading", { name: "Buy a home" });
      expect(screen.getByText("No saved scenarios yet.")).toBeInTheDocument();
      expect(screen.queryByText(/Aggressive contribution/)).not.toBeInTheDocument();
    });

    it("does not let a stale scenario-list response overwrite the next goal", async () => {
      const firstScenarios = deferred<GoalScenario[]>();
      scenariosMock.mockImplementation((goalId) => goalId === 1 ? firstScenarios.promise : Promise.resolve([]));
      const { rerender } = render(<GoalDetailPage params={{ id: "1" }} />);
      await waitFor(() => expect(scenariosMock).toHaveBeenCalledWith(1, true));

      listMock.mockResolvedValue([goal, secondGoal]);
      rerender(<GoalDetailPage params={{ id: "2" }} />);
      await screen.findByRole("heading", { name: "Buy a home" });

      firstScenarios.resolve([scenario]);
      await waitFor(() => expect(screen.getByText("No saved scenarios yet.")).toBeInTheDocument());
      expect(screen.queryByText(/Aggressive contribution/)).not.toBeInTheDocument();
    });

    it("resets the loaded What-If assumptions after a route transition", async () => {
      scenariosMock.mockResolvedValue([scenario]);
      const { rerender } = render(<GoalDetailPage params={{ id: "1" }} />);
      fireEvent.click(await screen.findByRole("button", { name: "Load Aggressive contribution scenario" }));
      expect(await screen.findByLabelText("What-If monthly contribution for Retire by 55")).toHaveValue(20000);

      listMock.mockResolvedValue([goal, secondGoal]);
      scenariosMock.mockResolvedValue([]);
      rerender(<GoalDetailPage params={{ id: "2" }} />);
      await screen.findByRole("heading", { name: "Buy a home" });
      expect(screen.queryByRole("button", { name: "What-If" })).toBeInTheDocument();
      expect(screen.queryByLabelText("What-If monthly contribution for Buy a home")).not.toBeInTheDocument();
    });

    it("does not refresh the next goal when a previous-route scenario save completes", async () => {
      const saveResult = deferred<GoalScenario>();
      let firstGoalOneScenarioRead = true;
      scenariosMock.mockImplementation((goalId) => {
        if (goalId !== 1) return Promise.resolve([]);
        if (firstGoalOneScenarioRead) {
          firstGoalOneScenarioRead = false;
          return Promise.resolve([]);
        }
        return Promise.resolve([scenario]);
      });
      scenariosCreateMock.mockReturnValueOnce(saveResult.promise);
      const { rerender } = render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByRole("heading", { name: "Retire by 55" });
      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      fireEvent.click(screen.getByRole("button", { name: "Save scenario" }));
      fireEvent.change(screen.getByLabelText("Scenario name for Retire by 55"), { target: { value: "Aggressive contribution" } });
      fireEvent.click(screen.getByRole("button", { name: "Save" }));
      await waitFor(() => expect(scenariosCreateMock).toHaveBeenCalled());

      listMock.mockResolvedValue([goal, secondGoal]);
      rerender(<GoalDetailPage params={{ id: "2" }} />);
      await screen.findByRole("heading", { name: "Buy a home" });

      saveResult.resolve(scenario);
      await waitFor(() => expect(scenariosMock).toHaveBeenCalledWith(1, true));
      expect(screen.getByText("No saved scenarios yet.")).toBeInTheDocument();
      expect(screen.queryByText(/Aggressive contribution/)).not.toBeInTheDocument();
    });

    // 16, 18. no persisted-output / forecast / advisory wording anywhere in the Saved Scenarios surface
    it("does not introduce persisted-output, forecast, or advisory wording", async () => {
      scenariosMock.mockResolvedValue([scenario, archivedScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByText((_, element) => element?.textContent === "Aggressive contribution (฿20,000.00/month · 6% annual return assumption)");
      fireEvent.click(screen.getByRole("button", { name: "Show archived scenarios (1)" }));
      await screen.findByText(/Old plan/);
      expect(screen.queryByText(/forecast|expected return|probability|guaranteed|on track|likely to|recommended contribution|should contribute|advice|projected value|reach date/i)).not.toBeInTheDocument();
    });
  });

  describe("Scenario Comparison", () => {
    async function selectBothScenarios() {
      await screen.findByText((_, element) => element?.textContent === "Aggressive contribution (฿20,000.00/month · 6% annual return assumption)");
      fireEvent.change(screen.getByLabelText("Compare scenario A for Retire by 55"), { target: { value: String(scenario.id) } });
      fireEvent.change(screen.getByLabelText("Compare scenario B for Retire by 55"), { target: { value: String(secondScenario.id) } });
    }

    // 1. fewer than two scenarios
    it("shows an unavailable state with fewer than two active scenarios", async () => {
      scenariosMock.mockResolvedValue([scenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByText((_, element) => element?.textContent === "Aggressive contribution (฿20,000.00/month · 6% annual return assumption)");
      expect(screen.getByText("Save at least two active scenarios to compare them.")).toBeInTheDocument();
      expect(screen.queryByLabelText("Compare scenario A for Retire by 55")).not.toBeInTheDocument();
    });

    // 2. select two scenarios / 4. scenario assumptions display
    it("compares two selected scenarios and displays each side's assumptions", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: "2030-01-01" }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();

      expect(await screen.findByText("Compare scenarios")).toBeInTheDocument();
      expect(screen.getByText("Monthly contribution")).toBeInTheDocument();
      expect(screen.getByText("Annual return assumption")).toBeInTheDocument();
      expect(screen.getByText("Reach date")).toBeInTheDocument();
      // Column headers name each side.
      expect(screen.getByRole("columnheader", { name: "Aggressive contribution" })).toBeInTheDocument();
      expect(screen.getByRole("columnheader", { name: "Conservative plan" })).toBeInTheDocument();
    });

    // 3. same scenario cannot occupy both sides
    it("rejects selecting the same scenario for both sides", async () => {
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByText((_, element) => element?.textContent === "Aggressive contribution (฿20,000.00/month · 6% annual return assumption)");
      fireEvent.change(screen.getByLabelText("Compare scenario A for Retire by 55"), { target: { value: String(scenario.id) } });
      fireEvent.change(screen.getByLabelText("Compare scenario B for Retire by 55"), { target: { value: String(scenario.id) } });
      expect(await screen.findByText("Choose two different scenarios to compare.")).toBeInTheDocument();
      expect(screen.queryByText("Reach date")).not.toBeInTheDocument();
    });

    // 5. both sides use the same current designated funding / 8. reach-date comparison
    it("computes both sides' reach dates from the same current designated funding", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      const rows = await screen.findAllByRole("row");
      const reachRow = rows.find((row) => row.textContent?.startsWith("Reach date"));
      expect(reachRow).toBeDefined();
      // Higher contribution + higher return assumption for Aggressive should reach sooner than Conservative.
      expect(reachRow?.textContent).toMatch(/Reach date.+20\d\d.+20\d\d/);
    });

    // 6. current target change affects both
    it("recomputes both sides when the goal's current target changes", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 100000, target_date: null }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 150000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      const { unmount } = render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findAllByText("Already reached")).toHaveLength(2);
      unmount();

      // A fresh load (e.g. the next page visit) picks up the goal's new current target.
      listMock.mockResolvedValue([{ ...goal, target_amount: 50000000, target_date: null }]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText("Reach date")).toBeInTheDocument();
      expect(screen.queryAllByText("Already reached")).toHaveLength(0);
    });

    // 7. funding change affects both
    it("recomputes both sides when designated funding changes", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 100000, target_date: null }]);
      allocationsMock.mockResolvedValue([]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(screen.queryAllByText("Already reached")).toHaveLength(0);

      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 500000 }]);
      fireEvent.change(screen.getByLabelText("Funding source kind"), { target: { value: "CASH_ACCOUNT" } });
      fireEvent.change(screen.getByLabelText("Funding source"), { target: { value: "5" } });
      fireEvent.change(screen.getByLabelText("Designated amount"), { target: { value: "500000" } });
      fireEvent.click(screen.getByRole("button", { name: "Add funding source" }));
      await waitFor(() => expect(screen.getAllByText("Already reached")).toHaveLength(2));
    });

    // 9. target-date projected-value comparison / 10. required-contribution comparison
    it("shows target-date projected value and required contribution for a future target date", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: "2030-01-01" }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText("Projected amount by 2030-01-01")).toBeInTheDocument();
      expect(screen.getByText("Required monthly contribution")).toBeInTheDocument();
    });

    // 11. no target date
    it("omits target-date projection and required contribution when the goal has no target date", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText(/This goal has no target date/)).toBeInTheDocument();
      expect(screen.queryByText("Required monthly contribution")).not.toBeInTheDocument();
    });

    // 12. past target date
    it("states that the saved target date has passed and omits target-date figures", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: "2020-01-01" }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText(/Saved target date \(2020-01-01\) has passed/)).toBeInTheDocument();
      expect(screen.queryByText("Required monthly contribution")).not.toBeInTheDocument();
    });

    // 13. one unreachable
    it("shows one scenario unreachable while the other reaches its target", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 100000000, target_date: null }]);
      allocationsMock.mockResolvedValue([]);
      const reachableScenario: GoalScenario = { ...scenario, id: 600, name: "Reachable", monthly_contribution: 500000, annual_return_pct: 8 };
      const unreachableScenario: GoalScenario = { ...scenario, id: 601, name: "Unreachable", monthly_contribution: 1, annual_return_pct: 0 };
      scenariosMock.mockResolvedValue([reachableScenario, unreachableScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByText((_, element) => element?.textContent === "Reachable (฿500,000.00/month · 8% annual return assumption)");
      fireEvent.change(screen.getByLabelText("Compare scenario A for Retire by 55"), { target: { value: "600" } });
      fireEvent.change(screen.getByLabelText("Compare scenario B for Retire by 55"), { target: { value: "601" } });
      expect(await screen.findByText("Not reachable within 50 years")).toBeInTheDocument();
    });

    // 14. negative-return scenario
    it("compares a negative-return scenario without editorializing", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      const negativeScenario: GoalScenario = { ...secondScenario, annual_return_pct: -3 };
      scenariosMock.mockResolvedValue([scenario, negativeScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText("-3%")).toBeInTheDocument();
      expect(screen.queryByText(/risk|warning|caution/i)).not.toBeInTheDocument();
    });

    // 15. already funded
    it("shows both scenarios already reached when designated funding already meets the target", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 100000, target_date: "2030-01-01" }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 250000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findAllByText("Already reached")).toHaveLength(2);
    });

    // 16. Funding Health warning shown once, shared (not once per scenario side or allocation)
    it("shows shared Funding Health once per source near the comparison", async () => {
      cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 50000 }]);
      allocationsMock.mockResolvedValue([
        { ...cashAllocation, allocated_amount: 100000 },
        { ...cashAllocation, id: 102, allocated_amount: 100000 },
      ]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      await screen.findByText("Reach date");
      const compareContainer = screen.getByText("Compare scenarios").closest("div") as HTMLElement;
      const warnings = within(compareContainer).getAllByText(
        (_, element) => element?.textContent === "Observed value ฿50,000.00 · Attention: exceeds observed value by ฿150,000.00",
      );
      expect(warnings).toHaveLength(1);
    });

    // 17. allocation failure => unavailable
    it("marks the comparison unavailable when allocation evidence fails to load", async () => {
      allocationsMock.mockRejectedValue(new Error("allocations offline"));
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByText((_, element) => element?.textContent === "Aggressive contribution (฿20,000.00/month · 6% annual return assumption)");
      fireEvent.change(screen.getByLabelText("Compare scenario A for Retire by 55"), { target: { value: String(scenario.id) } });
      fireEvent.change(screen.getByLabelText("Compare scenario B for Retire by 55"), { target: { value: String(secondScenario.id) } });
      expect(await screen.findByText("Comparison unavailable — designated funding could not be loaded.")).toBeInTheDocument();
    });

    // 18. source valuation failure does not block comparison
    it("still computes the comparison when a source's current-value lookup fails", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsMock.mockResolvedValue([portfolioAllocation]);
      holdingsMock.mockRejectedValue(new Error("valuation offline"));
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText("Monthly contribution")).toBeInTheDocument();
      expect(screen.getAllByText("Observed value unavailable · Funding health unavailable").length).toBeGreaterThan(0);
    });

    // 19. scenario edit refresh
    it("refreshes comparison results after editing a selected scenario", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      scenariosUpdateMock.mockResolvedValue({ ...scenario, monthly_contribution: 99000 });
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText("฿20,000.00")).toBeInTheDocument();

      scenariosMock.mockResolvedValue([{ ...scenario, monthly_contribution: 99000 }, secondScenario]);
      fireEvent.click(screen.getByRole("button", { name: "Edit Aggressive contribution scenario" }));
      fireEvent.change(screen.getByLabelText("Edit monthly contribution for Aggressive contribution"), { target: { value: "99000" } });
      fireEvent.click(screen.getAllByRole("button", { name: "Save" })[0]);
      await waitFor(() => expect(scenariosUpdateMock).toHaveBeenCalled());
      expect(await screen.findByText("฿99,000.00")).toBeInTheDocument();
    });

    // 20. scenario archive removes selection
    it("drops a selection and its result when that scenario becomes archived", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText("Reach date")).toBeInTheDocument();

      scenariosMock.mockResolvedValue([{ ...secondScenario, is_archived: true }, scenario]);
      fireEvent.click(screen.getByRole("button", { name: "Archive Conservative plan scenario" }));
      await waitFor(() => expect(screen.queryByText("Reach date")).not.toBeInTheDocument());
      // Only one active scenario remains — the comparison selectors are withdrawn entirely, not left stale.
      expect(screen.getByText("Save at least two active scenarios to compare them.")).toBeInTheDocument();
      expect(screen.queryByLabelText("Compare scenario B for Retire by 55")).not.toBeInTheDocument();
    });

    // 21. route transition reset
    it("resets comparison selection after a route transition", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockImplementation(async (goalId) => (goalId === 1 ? [scenario, secondScenario] : []));
      const { rerender } = render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText("Reach date")).toBeInTheDocument();

      listMock.mockResolvedValue([goal, secondGoal]);
      rerender(<GoalDetailPage params={{ id: "2" }} />);
      await screen.findByRole("heading", { name: "Buy a home" });
      expect(screen.queryByText("Reach date")).not.toBeInTheDocument();
      expect(screen.getByText("No saved scenarios yet.")).toBeInTheDocument();
    });

    // 22. no recommendation / ranking language
    it("does not declare a winner, best, or recommended scenario", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: "2030-01-01" }]);
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 100000 }]);
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      await screen.findByText("Reach date");
      expect(screen.queryByText(/winner|best|recommended|optimal|safer|better|preferred|should choose|success chance/i)).not.toBeInTheDocument();
    });

    // 23. live-context disclosure
    it("shows the live-context comparison disclosure", async () => {
      scenariosMock.mockResolvedValue([scenario, secondScenario]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await selectBothScenarios();
      expect(await screen.findByText(
        "Scenarios are compared using the goal's current target and designated funding.",
      )).toBeInTheDocument();
    });
  });
});
