import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GoalsPage from "@/app/goals/page";
import type {
  CashAccount,
  GoalContextResponse,
  GoalFundingAllocation,
  Portfolio,
  PortfolioItem,
  PriceRefreshItem,
  WealthGoal,
} from "@/lib/api";

const {
  createWealthGoal,
  getWealthGoalsContext,
  listGoalFundingAllocations,
  listWealthGoals,
  updateWealthGoal,
  listCashAccounts,
  getHoldings,
  getPortfolioPrices,
  portfolioState,
} = vi.hoisted(() => ({
  createWealthGoal: vi.fn(),
  getWealthGoalsContext: vi.fn(),
  listGoalFundingAllocations: vi.fn(),
  listWealthGoals: vi.fn(),
  updateWealthGoal: vi.fn(),
  listCashAccounts: vi.fn(),
  getHoldings: vi.fn(),
  getPortfolioPrices: vi.fn(),
  portfolioState: {
    portfolios: [] as Portfolio[],
    loading: false,
    error: null as string | null,
  },
}));

vi.mock("@/lib/api", () => ({
  createWealthGoal,
  getWealthGoalsContext,
  listGoalFundingAllocations,
  listWealthGoals,
  updateWealthGoal,
  listCashAccounts,
  getHoldings,
  getPortfolioPrices,
}));

vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => portfolioState,
}));

function makeGoal(overrides: Partial<WealthGoal> & { id: number; name: string; target_amount: number }): WealthGoal {
  return {
    workspace_id: 1,
    goal_type: "OTHER",
    currency: "THB",
    target_date: null,
    priority: "MEDIUM",
    note: null,
    is_archived: false,
    created_at: "2026-08-26T00:00:00",
    updated_at: "2026-08-26T00:00:00",
    ...overrides,
  };
}

function makeAllocation(
  overrides: Partial<GoalFundingAllocation> & { id: number; wealth_goal_id: number; allocated_amount: number }
): GoalFundingAllocation {
  return {
    workspace_id: 1,
    source_kind: "CASH_ACCOUNT",
    cash_account_id: 1,
    portfolio_id: null,
    source_name: "Source",
    source_is_archived: false,
    currency: "THB",
    created_at: "2026-08-26T00:00:00",
    updated_at: "2026-08-26T00:00:00",
    ...overrides,
  };
}

function makeCashAccount(id: number, balance: number, overrides: Partial<CashAccount> = {}): CashAccount {
  return {
    id,
    workspace_id: 1,
    name: `Cash ${id}`,
    institution: null,
    currency: "THB",
    balance,
    is_archived: false,
    created_at: "2026-01-01T00:00:00",
    updated_at: "2026-01-01T00:00:00",
    ...overrides,
  };
}

function makePortfolio(id: number, name: string, cash: number): Portfolio {
  return { id, name, cash_balance: cash, created_at: "2026-01-01T00:00:00" };
}

function makeHolding(overrides: Partial<PortfolioItem> & { symbol: string; shares: number; avg_cost: number }): PortfolioItem {
  return {
    id: 0,
    portfolio_id: 0,
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

function makeQuote(symbol: string, current: number): PriceRefreshItem {
  return { symbol, current_price: current, previous_close: current, change_percent: 0, last_updated: null };
}

const goal: WealthGoal = makeGoal({
  id: 1,
  name: "Retire by 55",
  goal_type: "RETIREMENT",
  target_amount: 20000000,
  target_date: "2055-01-01",
  priority: "HIGH",
  note: "Discussed with spouse",
});

const cashAllocation: GoalFundingAllocation = makeAllocation({
  id: 100,
  wealth_goal_id: 1,
  source_kind: "CASH_ACCOUNT",
  cash_account_id: 5,
  portfolio_id: null,
  source_name: "Wedding Savings",
  allocated_amount: 300000,
});

const listMock = vi.mocked(listWealthGoals);
const createMock = vi.mocked(createWealthGoal);
const updateMock = vi.mocked(updateWealthGoal);
const allocationsMock = vi.mocked(listGoalFundingAllocations);
const contextMock = vi.mocked(getWealthGoalsContext);
const cashAccountsMock = vi.mocked(listCashAccounts);
const holdingsMock = vi.mocked(getHoldings);
const pricesMock = vi.mocked(getPortfolioPrices);

async function configuredGoalContext(): Promise<GoalContextResponse> {
  const latestListResult = listMock.mock.results[listMock.mock.results.length - 1];
  const loadedGoals: WealthGoal[] = latestListResult
    ? await Promise.resolve(latestListResult.value).catch(() => [])
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
    // Read the configured test fixture implementation directly so the
    // production path can prove it made zero legacy allocation requests.
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

describe("GoalsPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([]);
    createMock.mockResolvedValue(goal);
    updateMock.mockResolvedValue(goal);
    allocationsMock.mockResolvedValue([]);
    contextMock.mockImplementation(configuredGoalContext);
    cashAccountsMock.mockResolvedValue([]);
    holdingsMock.mockResolvedValue([]);
    pricesMock.mockResolvedValue([]);
    portfolioState.portfolios = [];
    portfolioState.loading = false;
    portfolioState.error = null;
  });

  it("shows a loading state and fixed THB", () => {
    listMock.mockReturnValue(new Promise(() => {}));
    render(<GoalsPage />);
    expect(screen.getByText("Loading goals…")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Currency: THB (fixed for Wealth Goals Foundation v1)")).toBeInTheDocument();
  });

  it("shows an empty state after a successful workspace-wide load, including archived goals in one request", async () => {
    render(<GoalsPage />);
    expect(await screen.findByText("No active goals yet. Add your first goal above.")).toBeInTheDocument();
    expect(await screen.findByText("No funding sources to show yet.")).toBeInTheDocument();
    expect(listMock).toHaveBeenCalledWith(true);
    expect(listMock).toHaveBeenCalledTimes(1);
    expect(contextMock).toHaveBeenCalledWith(true);
    expect(contextMock).toHaveBeenCalledTimes(1);
    expect(allocationsMock).not.toHaveBeenCalled();
  });

  it("renders a compact card with metadata, funding facts, and a detail link", async () => {
    listMock.mockResolvedValue([{ ...goal, target_amount: 1000000 }]);
    allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 300000 }]);
    render(<GoalsPage />);

    expect(await screen.findByText("Retire by 55")).toBeInTheDocument();
    expect(await screen.findByText("Designated funding")).toBeInTheDocument();
    expect(screen.getByText("Retirement · High priority")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "฿1,000,000.00 target · by 2055-01-01")).toBeInTheDocument();
    expect(screen.getByText("Goal progress")).toBeInTheDocument();
    expect(screen.getByText("30%")).toBeInTheDocument();
    expect(screen.getByText("Funding gap")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "View plan →" })).toHaveAttribute("href", "/goals/1");
    // Notes and planning-heavy content belong to the detail route.
    expect(screen.queryByText("Discussed with spouse")).not.toBeInTheDocument();
    expect(screen.queryByText("Funding Sources")).not.toBeInTheDocument();
    expect(screen.queryByText("What-If")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Add funding source" })).not.toBeInTheDocument();
  });

  it("renders server-supplied arithmetic without recomputing it from allocations", async () => {
    listMock.mockResolvedValue([{ ...goal, target_amount: 1000000 }]);
    allocationsMock.mockResolvedValue([]);
    contextMock.mockImplementation(async () => {
      const response = await configuredGoalContext();
      Object.assign(response.goals[0], {
        designated_total: 123456,
        progress_ratio: 0.123456,
        progress_percent: 47.6,
        funding_gap: 876544,
        fully_designated: false,
      });
      return response;
    });
    render(<GoalsPage />);

    expect(await screen.findByText("฿123,456.00")).toBeInTheDocument();
    expect(screen.getByText("48%")).toBeInTheDocument();
    expect(screen.getByText("฿876,544.00")).toBeInTheDocument();
  });

  it("marks a record/context generation mismatch unavailable instead of showing mixed facts", async () => {
    listMock.mockResolvedValue([goal]);
    contextMock.mockImplementation(async () => {
      const response = await configuredGoalContext();
      response.goals[0].updated_at = "2026-08-26T00:00:01";
      return response;
    });
    render(<GoalsPage />);

    expect(await screen.findByText("Goal progress unavailable — funding data failed to load.")).toBeInTheDocument();
    expect(screen.getByText("Funding source health is unavailable — Goal Context evidence is incomplete.")).toBeInTheDocument();
  });

  it("renders an honest no-target-date summary", async () => {
    listMock.mockResolvedValue([{ ...goal, target_date: null }]);
    render(<GoalsPage />);
    await screen.findByText("Retire by 55");
    expect(screen.getByText((_, element) => element?.textContent === "฿20,000,000.00 target · no target date")).toBeInTheDocument();
  });

  it("keeps compact progress unavailable when allocation evidence fails", async () => {
    listMock.mockResolvedValue([goal]);
    allocationsMock.mockRejectedValue(new Error("allocations offline"));
    render(<GoalsPage />);
    await screen.findByText("Retire by 55");
    expect(await screen.findByText("Goal progress unavailable — funding data failed to load.")).toBeInTheDocument();
    expect(screen.queryByText("0%")).not.toBeInTheDocument();
    expect(screen.queryByText("Funding Sources")).not.toBeInTheDocument();
    expect(contextMock).toHaveBeenCalledTimes(1);
    expect(allocationsMock).not.toHaveBeenCalled();
  });

  it("creates a goal with the explicit THB contract", async () => {
    render(<GoalsPage />);
    await screen.findByText("No active goals yet. Add your first goal above.");
    fireEvent.change(screen.getByLabelText("Goal name"), { target: { value: "House Down Payment" } });
    fireEvent.change(screen.getByLabelText("Goal type"), { target: { value: "HOUSE" } });
    fireEvent.change(screen.getByLabelText("Target amount"), { target: { value: "3000000" } });
    fireEvent.change(screen.getByLabelText("Target date"), { target: { value: "2030-06-01" } });
    fireEvent.change(screen.getByLabelText("Goal priority"), { target: { value: "MEDIUM" } });
    fireEvent.change(screen.getByLabelText("Note"), { target: { value: "Bangkok condo" } });
    fireEvent.click(screen.getByRole("button", { name: "Add goal" }));

    await waitFor(() => expect(createMock).toHaveBeenCalledWith({
      name: "House Down Payment",
      goal_type: "HOUSE",
      target_amount: 3000000,
      currency: "THB",
      target_date: "2030-06-01",
      priority: "MEDIUM",
      note: "Bangkok condo",
    }));
    await waitFor(() => expect(contextMock).toHaveBeenCalledTimes(2));
  });

  it("creates a goal with no target date as null", async () => {
    render(<GoalsPage />);
    await screen.findByText("No active goals yet. Add your first goal above.");
    fireEvent.change(screen.getByLabelText("Goal name"), { target: { value: "Someday FIRE" } });
    fireEvent.change(screen.getByLabelText("Target amount"), { target: { value: "15000000" } });
    fireEvent.click(screen.getByRole("button", { name: "Add goal" }));
    await waitFor(() => expect(createMock).toHaveBeenCalledWith(expect.objectContaining({ target_date: null })));
  });

  it("edits goal metadata from the canonical list-page editor", async () => {
    listMock.mockResolvedValue([goal]);
    render(<GoalsPage />);
    await screen.findByText("Retire by 55");
    fireEvent.click(screen.getByRole("button", { name: "Edit" }));
    fireEvent.change(screen.getByLabelText("Edit goal name"), { target: { value: "Retire by 50" } });
    fireEvent.change(screen.getByLabelText("Edit target amount"), { target: { value: "25000000" } });
    fireEvent.change(screen.getByLabelText("Edit goal priority"), { target: { value: "MEDIUM" } });
    fireEvent.click(screen.getByRole("button", { name: "Save changes" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, {
      name: "Retire by 50",
      goal_type: "RETIREMENT",
      target_amount: 25000000,
      target_date: "2055-01-01",
      priority: "MEDIUM",
      note: "Discussed with spouse",
    }));
    await waitFor(() => expect(contextMock).toHaveBeenCalledTimes(2));
  });

  it("archives and restores a goal via a coherent refresh, without ever requesting an active-only list", async () => {
    let current: WealthGoal[] = [goal];
    listMock.mockImplementation(async () => current);
    updateMock.mockImplementation(async (id, body) => {
      current = current.map((item) => item.id === id ? { ...item, ...body } : item) as WealthGoal[];
      return current.find((item) => item.id === id)!;
    });
    render(<GoalsPage />);
    await screen.findByText("Retire by 55");
    fireEvent.click(screen.getByRole("button", { name: "Archive" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, { is_archived: true }));
    expect(await screen.findByText("No active goals yet. Add your first goal above.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Show archived" }));
    expect(await screen.findByText("Retire by 55")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Restore" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, { is_archived: false }));
    await waitFor(() => expect(contextMock).toHaveBeenCalledTimes(3));
    expect(listMock).toHaveBeenCalledWith(true);
    expect(listMock).not.toHaveBeenCalledWith(false);
  });

  it("toggling 'Show archived' is presentation-only and causes no network request", async () => {
    listMock.mockResolvedValue([goal, makeGoal({ id: 2, name: "Archived Goal", target_amount: 500000, is_archived: true })]);
    render(<GoalsPage />);
    await screen.findByText("Retire by 55");
    const callsBefore = listMock.mock.calls.length;
    const contextCallsBefore = contextMock.mock.calls.length;
    const allocationCallsBefore = allocationsMock.mock.calls.length;

    fireEvent.click(screen.getByRole("button", { name: "Show archived" }));
    expect(await screen.findByText("Archived Goal")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Hide archived" }));
    expect(screen.queryByText("Archived Goal")).not.toBeInTheDocument();

    expect(listMock.mock.calls.length).toBe(callsBefore);
    expect(contextMock.mock.calls.length).toBe(contextCallsBefore);
    expect(allocationsMock.mock.calls.length).toBe(allocationCallsBefore);
  });

  it("keeps validation and API failures honest", async () => {
    listMock.mockRejectedValue(new Error("goals offline"));
    render(<GoalsPage />);
    const alerts = await screen.findAllByRole("alert");
    expect(alerts.some((el) => el.textContent === "goals offline")).toBe(true);
    fireEvent.change(screen.getByLabelText("Goal name"), { target: { value: "Debt-free" } });
    fireEvent.change(screen.getByLabelText("Target amount"), { target: { value: "0" } });
    fireEvent.click(screen.getByRole("button", { name: "Add goal" }));
    expect(screen.getByText("Enter a goal name and a positive target amount.")).toBeInTheDocument();
    expect(createMock).not.toHaveBeenCalled();
  });

  describe("Funding source health", () => {
    it("uses one workspace Goal Context request and aggregates a Cash Account shared by two active goals", async () => {
      const goalB = makeGoal({ id: 2, name: "House Down Payment", target_amount: 500000 });
      listMock.mockResolvedValue([goal, goalB]);
      allocationsMock.mockImplementation(async (goalId: number) => {
        if (goalId === 1) return [makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 100000, cash_account_id: 5, source_name: "Shared Cash" })];
        return [makeAllocation({ id: 2, wealth_goal_id: 2, allocated_amount: 50000, cash_account_id: 5, source_name: "Shared Cash" })];
      });
      cashAccountsMock.mockResolvedValue([makeCashAccount(5, 200000)]);

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(contextMock).toHaveBeenCalledTimes(1);
      expect(contextMock).toHaveBeenCalledWith(true);
      expect(allocationsMock).not.toHaveBeenCalled();

      expect(await screen.findByText("฿150,000.00 designated")).toBeInTheDocument();
      expect(screen.getByText((_, el) => el?.textContent === "Current value ฿200,000.00 · Funding health: Supported")).toBeInTheDocument();
    });

    it("includes an archived goal's allocation in cross-goal aggregation, and shows a source referenced only by an archived goal", async () => {
      const archivedGoal = makeGoal({ id: 3, name: "Old Goal", target_amount: 200000, is_archived: true });
      listMock.mockResolvedValue([goal, archivedGoal]);
      allocationsMock.mockImplementation(async (goalId: number) => {
        if (goalId === 1) return [makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 200000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 9, source_name: "Growth Portfolio" })];
        return [makeAllocation({ id: 2, wealth_goal_id: 3, allocated_amount: 5000, cash_account_id: 7, source_name: "Archived-Only Cash", source_is_archived: true })];
      });
      cashAccountsMock.mockResolvedValue([makeCashAccount(7, 1000, { is_archived: true })]);
      portfolioState.portfolios = [makePortfolio(9, "Growth Portfolio", 50000)];
      holdingsMock.mockResolvedValue([makeHolding({ symbol: "AAA", shares: 10, avg_cost: 100, current_price: 200 })]);
      pricesMock.mockResolvedValue([makeQuote("AAA", 200)]);

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      // Portfolio 9: designated 200,000, current value = 50,000 cash + 10*200 = 52,000 -> over-allocated by 148,000.
      expect(await screen.findByText("฿200,000.00 designated")).toBeInTheDocument();
      expect(screen.getByText((_, el) => el?.textContent === "Current value ฿52,000.00 · Over-allocated by ฿148,000.00")).toBeInTheDocument();

      // Cash 7 is referenced only by the archived goal, and still appears.
      expect(screen.getByText((_, el) => el?.textContent === "Archived-Only Cash (Cash Account, archived)")).toBeInTheDocument();
      expect(screen.getByText("฿5,000.00 designated")).toBeInTheDocument();
    });

    it("shows an allocation-evidence-incomplete state with no rows when any goal's allocation request fails", async () => {
      const goalB = makeGoal({ id: 2, name: "House Down Payment", target_amount: 500000 });
      listMock.mockResolvedValue([goal, goalB]);
      allocationsMock.mockImplementation(async (goalId: number) => {
        if (goalId === 1) return [makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 100000, cash_account_id: 5, source_name: "Shared Cash" })];
        throw new Error("offline");
      });
      cashAccountsMock.mockResolvedValue([makeCashAccount(5, 200000)]);

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText("Funding source health is unavailable — Goal Context evidence is incomplete.")).toBeInTheDocument();
      expect(screen.queryByText("฿100,000.00 designated")).not.toBeInTheDocument();
      expect(screen.queryByText("Shared Cash")).not.toBeInTheDocument();
    });

    it("distinguishes 'goals exist but nothing is designated' from 'no goals at all'", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsMock.mockResolvedValue([]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");
      expect(await screen.findByText("No funding sources designated yet.")).toBeInTheDocument();
      expect(screen.queryByText("No funding sources to show yet.")).not.toBeInTheDocument();
      expect(screen.queryByText("Funding source health is unavailable — Goal Context evidence is incomplete.")).not.toBeInTheDocument();
    });

    it("treats an ARCHIVED goal's failed allocation request as incomplete evidence and suppresses every row", async () => {
      // The archived goal is not rendered as a card, but its allocations are
      // still workspace evidence: an unknown archived designation could be
      // hiding an over-allocation on the very source the active goal uses.
      const archivedGoal = makeGoal({ id: 3, name: "Old Goal", target_amount: 200000, is_archived: true });
      listMock.mockResolvedValue([goal, archivedGoal]);
      allocationsMock.mockImplementation(async (goalId: number) => {
        if (goalId === 1) return [makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 100000, cash_account_id: 5, source_name: "Shared Cash" })];
        throw new Error("offline");
      });
      cashAccountsMock.mockResolvedValue([makeCashAccount(5, 200000)]);

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText("Funding source health is unavailable — Goal Context evidence is incomplete.")).toBeInTheDocument();
      expect(screen.queryByText("Shared Cash")).not.toBeInTheDocument();
      expect(screen.queryByText("฿100,000.00 designated")).not.toBeInTheDocument();
      expect(screen.queryByText(/Funding health: Supported/)).not.toBeInTheDocument();
    });

    it("computes canonical portfolio value (cash + holdings) with exactly one holdings and one prices request", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsMock.mockResolvedValue([
        makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 40000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 9, source_name: "Growth Portfolio" }),
      ]);
      portfolioState.portfolios = [makePortfolio(9, "Growth Portfolio", 10000)];
      holdingsMock.mockResolvedValue([makeHolding({ symbol: "AAA", shares: 5, avg_cost: 100, current_price: 300 })]);
      pricesMock.mockResolvedValue([makeQuote("AAA", 300)]);

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      // 10,000 cash + 5*300 = 1,500 holdings = 11,500 current value; 40,000 designated -> over-allocated by 28,500.
      expect(await screen.findByText((_, el) => el?.textContent === "Current value ฿11,500.00 · Over-allocated by ฿28,500.00")).toBeInTheDocument();
      expect(holdingsMock).toHaveBeenCalledTimes(1);
      expect(pricesMock).toHaveBeenCalledTimes(1);
      expect(holdingsMock).toHaveBeenCalledWith(9);
    });

    it("issues exactly one holdings and one prices request per referenced portfolio when several are referenced", async () => {
      const goalB = makeGoal({ id: 2, name: "House Down Payment", target_amount: 500000 });
      listMock.mockResolvedValue([goal, goalB]);
      allocationsMock.mockImplementation(async (goalId: number) => {
        if (goalId === 1) {
          return [
            makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 1000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 9, source_name: "P Nine" }),
            makeAllocation({ id: 2, wealth_goal_id: 1, allocated_amount: 1000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 10, source_name: "P Ten" }),
          ];
        }
        return [
          // Duplicate reference to portfolio 9 from a second goal must not re-fetch.
          makeAllocation({ id: 3, wealth_goal_id: 2, allocated_amount: 1000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 9, source_name: "P Nine" }),
          makeAllocation({ id: 4, wealth_goal_id: 2, allocated_amount: 1000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 11, source_name: "P Eleven" }),
        ];
      });
      portfolioState.portfolios = [
        makePortfolio(9, "P Nine", 100000),
        makePortfolio(10, "P Ten", 100000),
        makePortfolio(11, "P Eleven", 100000),
      ];
      // Staggered resolution: each settling value re-renders, which must not
      // re-launch the still-in-flight requests for the other portfolios.
      holdingsMock.mockImplementation(
        (portfolioId: number) => new Promise((resolve) => setTimeout(() => resolve([]), portfolioId - 8))
      );
      pricesMock.mockImplementation(
        (portfolioId: number) => new Promise((resolve) => setTimeout(() => resolve([]), portfolioId - 8))
      );

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");
      await waitFor(() => expect(screen.getAllByText(/Funding health: Supported/)).toHaveLength(3));

      expect(holdingsMock).toHaveBeenCalledTimes(3);
      expect(pricesMock).toHaveBeenCalledTimes(3);
      expect(holdingsMock.mock.calls.map((call) => call[0]).sort((a, b) => a - b)).toEqual([9, 10, 11]);
      expect(pricesMock.mock.calls.map((call) => call[0]).sort((a, b) => a - b)).toEqual([9, 10, 11]);
    });

    it("isolates a single portfolio's valuation failure without affecting other sources", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsMock.mockResolvedValue([
        makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 10000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 9, source_name: "Good Portfolio" }),
        makeAllocation({ id: 2, wealth_goal_id: 1, allocated_amount: 20000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 10, source_name: "Bad Portfolio" }),
      ]);
      portfolioState.portfolios = [makePortfolio(9, "Good Portfolio", 50000), makePortfolio(10, "Bad Portfolio", 50000)];
      holdingsMock.mockImplementation(async (portfolioId: number) => {
        if (portfolioId === 10) throw new Error("holdings offline");
        return [];
      });
      pricesMock.mockResolvedValue([]);

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText((_, el) => el?.textContent === "Current value ฿50,000.00 · Funding health: Supported")).toBeInTheDocument();
      expect(screen.getByText("Current value unavailable · Funding health unavailable")).toBeInTheDocument();
    });

    it("isolates a Cash Account catalog failure to Cash rows only", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsMock.mockResolvedValue([
        makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 10000, cash_account_id: 5, source_name: "Cash Source" }),
        makeAllocation({ id: 2, wealth_goal_id: 1, allocated_amount: 10000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 9, source_name: "Portfolio Source" }),
      ]);
      cashAccountsMock.mockRejectedValue(new Error("cash offline"));
      portfolioState.portfolios = [makePortfolio(9, "Portfolio Source", 10000)];
      holdingsMock.mockResolvedValue([]);
      pricesMock.mockResolvedValue([]);

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText((_, el) => el?.textContent === "Current value ฿10,000.00 · Funding health: Supported")).toBeInTheDocument();
      expect(screen.getByText("Current value unavailable · Funding health unavailable")).toBeInTheDocument();
    });

    it("isolates a Portfolio catalog failure to Portfolio rows only, and never calls holdings/prices", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsMock.mockResolvedValue([
        makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 10000, cash_account_id: 5, source_name: "Cash Source" }),
        makeAllocation({ id: 2, wealth_goal_id: 1, allocated_amount: 10000, source_kind: "PORTFOLIO", cash_account_id: null, portfolio_id: 9, source_name: "Portfolio Source" }),
      ]);
      cashAccountsMock.mockResolvedValue([makeCashAccount(5, 10000)]);
      portfolioState.portfolios = [];
      portfolioState.error = "Cannot load portfolios";

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText((_, el) => el?.textContent === "Current value ฿10,000.00 · Funding health: Supported")).toBeInTheDocument();
      expect(screen.getByText("Current value unavailable · Funding health unavailable")).toBeInTheDocument();
      expect(holdingsMock).not.toHaveBeenCalled();
      expect(pricesMock).not.toHaveBeenCalled();
    });

    it("rejects a stale refresh's response when a newer refresh has already started", async () => {
      let resolveFirst!: (goals: WealthGoal[]) => void;
      const first = new Promise<WealthGoal[]>((resolve) => { resolveFirst = resolve; });
      const goalB = makeGoal({ id: 2, name: "Second Load Goal", target_amount: 999999 });
      listMock.mockReturnValueOnce(first).mockResolvedValueOnce([goalB]);

      render(<GoalsPage />);
      // Trigger a second, overlapping refresh before the first resolves.
      fireEvent.change(screen.getByLabelText("Goal name"), { target: { value: "Trigger Refresh" } });
      fireEvent.change(screen.getByLabelText("Target amount"), { target: { value: "1000" } });
      fireEvent.click(screen.getByRole("button", { name: "Add goal" }));
      await waitFor(() => expect(createMock).toHaveBeenCalled());
      await screen.findByText("Second Load Goal");

      // The first (now-stale) refresh resolves late — it must not clobber the newer state.
      resolveFirst([goal]);
      await new Promise((resolve) => setTimeout(resolve, 0));
      expect(screen.queryByText("Retire by 55")).not.toBeInTheDocument();
      expect(screen.getByText("Second Load Goal")).toBeInTheDocument();
    });

    it("drops a response that resolves after unmount, launching no follow-on evidence requests", async () => {
      let resolveGoals!: (goals: WealthGoal[]) => void;
      listMock.mockReturnValue(new Promise((resolve) => { resolveGoals = resolve; }));
      const { unmount } = render(<GoalsPage />);
      unmount();

      expect(() => resolveGoals([goal])).not.toThrow();
      await new Promise((resolve) => setTimeout(resolve, 0));

      // The continuation must short-circuit at the mounted guard: everything
      // downstream of it (cash catalog, per-goal allocations, and therefore
      // the portfolio valuation fan-out) must never be requested.
      expect(cashAccountsMock).not.toHaveBeenCalled();
      expect(allocationsMock).not.toHaveBeenCalled();
      expect(holdingsMock).not.toHaveBeenCalled();
      expect(pricesMock).not.toHaveBeenCalled();
    });

    it("does not introduce predictive, guarantee, advice, ranking, or urgency language", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsMock.mockResolvedValue([
        makeAllocation({ id: 1, wealth_goal_id: 1, allocated_amount: 40000, cash_account_id: 5, source_name: "Over Cash" }),
      ]);
      cashAccountsMock.mockResolvedValue([makeCashAccount(5, 10000)]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");
      await screen.findByText("฿40,000.00 designated");
      expect(
        screen.queryByText(
          /guaranteed|on track|projected completion|expected return|probability of success|recommended contribution|forecast|advice|attention|needs attention|urgency|urgent|ranking|recommend/i
        )
      ).not.toBeInTheDocument();
    });
  });
});
