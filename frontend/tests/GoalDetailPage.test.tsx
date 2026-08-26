import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GoalDetailPage from "@/app/goals/[id]/page";
import {
  createGoalFundingAllocation,
  deleteGoalFundingAllocation,
  getHoldings,
  getPortfolioPrices,
  listCashAccounts,
  listGoalFundingAllocations,
  listPortfolios,
  listWealthGoals,
  updateGoalFundingAllocation,
  type CashAccount,
  type GoalFundingAllocation,
  type Portfolio,
  type PortfolioItem,
  type PriceRefreshItem,
  type WealthGoal,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createGoalFundingAllocation: vi.fn(),
  deleteGoalFundingAllocation: vi.fn(),
  getHoldings: vi.fn(),
  getPortfolioPrices: vi.fn(),
  listCashAccounts: vi.fn(),
  listGoalFundingAllocations: vi.fn(),
  listPortfolios: vi.fn(),
  listWealthGoals: vi.fn(),
  updateGoalFundingAllocation: vi.fn(),
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
const cashAccountsMock = vi.mocked(listCashAccounts);
const portfoliosMock = vi.mocked(listPortfolios);
const holdingsMock = vi.mocked(getHoldings);
const pricesMock = vi.mocked(getPortfolioPrices);
const allocationsCreateMock = vi.mocked(createGoalFundingAllocation);
const allocationsUpdateMock = vi.mocked(updateGoalFundingAllocation);
const allocationsDeleteMock = vi.mocked(deleteGoalFundingAllocation);

describe("GoalDetailPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([goal]);
    allocationsMock.mockResolvedValue([]);
    cashAccountsMock.mockResolvedValue([cashAccount]);
    portfoliosMock.mockResolvedValue([portfolio]);
    holdingsMock.mockResolvedValue([]);
    pricesMock.mockResolvedValue([]);
    allocationsCreateMock.mockResolvedValue(cashAllocation);
    allocationsUpdateMock.mockResolvedValue(cashAllocation);
    allocationsDeleteMock.mockResolvedValue({ deleted: 100 });
  });

  it("loads a valid URL-anchored goal and keeps a back link", async () => {
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(screen.getByText("Loading goal…")).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "Retire by 55" })).toBeInTheDocument();
    expect(listMock).toHaveBeenCalledWith(true);
    expect(allocationsMock).toHaveBeenCalledWith(1);
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

    fireEvent.click(screen.getByRole("button", { name: "Edit designated amount for Wedding Savings" }));
    fireEvent.change(screen.getByLabelText("Edit designated amount for Wedding Savings"), { target: { value: "200000" } });
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    await waitFor(() => expect(allocationsUpdateMock).toHaveBeenCalledWith(1, 100, { allocated_amount: 200000 }));

    fireEvent.click(screen.getByRole("button", { name: "Remove Wedding Savings as a funding source" }));
    await waitFor(() => expect(allocationsDeleteMock).toHaveBeenCalledWith(1, 100));
  });

  it("reports Funding Health as supported", async () => {
    cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 450000 }]);
    allocationsMock.mockResolvedValue([cashAllocation]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    await screen.findByText((_, element) => element?.textContent === "Current value ฿450,000.00 · Funding health: Supported");
  });

  it("reports Funding Health as over-allocated", async () => {
    cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 100000 }]);
    allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 300000 }]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText((_, element) => element?.textContent === "Current value ฿100,000.00 · Attention: exceeds current value by ฿200,000.00")).toBeInTheDocument();
  });

  it("uses complete cross-goal allocation evidence for shared-source Funding Health", async () => {
    cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 400000 }]);
    listMock.mockResolvedValue([goal, secondGoal]);
    allocationsMock.mockImplementation(async (goalId) => goalId === 1
      ? [cashAllocation]
      : [{ ...cashAllocation, id: 200, wealth_goal_id: 2, allocated_amount: 200000 }]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText((_, element) => element?.textContent === "Current value ฿400,000.00 · Attention: exceeds current value by ฿100,000.00")).toBeInTheDocument();
  });

  it("keeps Funding Health unavailable when another goal's allocation evidence fails", async () => {
    listMock.mockResolvedValue([goal, secondGoal]);
    allocationsMock.mockImplementation(async (goalId) => {
      if (goalId === 1) return [cashAllocation];
      throw new Error("other allocation read failed");
    });
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("Current value unavailable · Funding health unavailable")).toBeInTheDocument();
  });

  it("keeps Funding Health unavailable when source valuation fails", async () => {
    allocationsMock.mockResolvedValue([portfolioAllocation]);
    holdingsMock.mockRejectedValue(new Error("holdings offline"));
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText("Current value unavailable · Funding health unavailable")).toBeInTheDocument();
    expect(screen.getByText("Goal progress")).toBeInTheDocument();
    expect(screen.getByText("4%")).toBeInTheDocument();
  });

  it("derives Portfolio Funding Health from holdings and prices", async () => {
    allocationsMock.mockResolvedValue([portfolioAllocation]);
    holdingsMock.mockResolvedValue([holding({ symbol: "AAA", shares: 10000, avg_cost: 50 })]);
    pricesMock.mockResolvedValue([quote("AAA", 90)]);
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(await screen.findByText((_, element) => element?.textContent === "Current value ฿900,000.00 · Funding health: Supported")).toBeInTheDocument();
    expect(holdingsMock).toHaveBeenCalledWith(9);
    expect(pricesMock).toHaveBeenCalledWith(9);
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
    expect(await screen.findByText("Current value unavailable · Funding health unavailable")).toBeInTheDocument();
    expect(screen.getByText("70%")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "฿700,000.00")).toBeInTheDocument();
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
});
