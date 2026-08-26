import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import GoalsPage from "@/app/goals/page";
import {
  createGoalFundingAllocation,
  createWealthGoal,
  deleteGoalFundingAllocation,
  getHoldings,
  getPortfolioPrices,
  listCashAccounts,
  listGoalFundingAllocations,
  listPortfolios,
  listWealthGoals,
  updateGoalFundingAllocation,
  updateWealthGoal,
  type CashAccount,
  type GoalFundingAllocation,
  type Portfolio,
  type PortfolioItem,
  type PriceRefreshItem,
  type WealthGoal,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createWealthGoal: vi.fn(),
  listWealthGoals: vi.fn(),
  updateWealthGoal: vi.fn(),
  listCashAccounts: vi.fn(),
  listPortfolios: vi.fn(),
  listGoalFundingAllocations: vi.fn(),
  createGoalFundingAllocation: vi.fn(),
  updateGoalFundingAllocation: vi.fn(),
  deleteGoalFundingAllocation: vi.fn(),
  getHoldings: vi.fn(),
  getPortfolioPrices: vi.fn(),
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
const createMock = vi.mocked(createWealthGoal);
const updateMock = vi.mocked(updateWealthGoal);
const cashAccountsMock = vi.mocked(listCashAccounts);
const portfoliosMock = vi.mocked(listPortfolios);
const allocationsListMock = vi.mocked(listGoalFundingAllocations);
const allocationsCreateMock = vi.mocked(createGoalFundingAllocation);
const allocationsUpdateMock = vi.mocked(updateGoalFundingAllocation);
const allocationsDeleteMock = vi.mocked(deleteGoalFundingAllocation);
const holdingsMock = vi.mocked(getHoldings);
const pricesMock = vi.mocked(getPortfolioPrices);

describe("GoalsPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([]);
    createMock.mockResolvedValue(goal);
    updateMock.mockResolvedValue(goal);
    cashAccountsMock.mockResolvedValue([cashAccount]);
    portfoliosMock.mockResolvedValue([portfolio]);
    allocationsListMock.mockResolvedValue([]);
    allocationsCreateMock.mockResolvedValue(cashAllocation);
    allocationsUpdateMock.mockResolvedValue(cashAllocation);
    allocationsDeleteMock.mockResolvedValue({ deleted: 100 });
    holdingsMock.mockResolvedValue([]);
    pricesMock.mockResolvedValue([]);
  });

  it("shows a loading state and fixed THB", () => {
    listMock.mockReturnValue(new Promise(() => {}));
    render(<GoalsPage />);
    expect(screen.getByText("Loading goals…")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Currency: THB (fixed for Wealth Goals Foundation v1)")).toBeInTheDocument();
  });

  it("shows an empty state after a successful active-only load", async () => {
    render(<GoalsPage />);
    expect(await screen.findByText("No active goals yet. Add your first goal above.")).toBeInTheDocument();
    expect(listMock).toHaveBeenCalledWith(false);
  });

  it("renders type, priority, target amount, and target date", async () => {
    listMock.mockResolvedValue([goal]);
    render(<GoalsPage />);
    expect(await screen.findByText("Retire by 55")).toBeInTheDocument();
    expect(screen.getByText("Retirement · High priority")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "฿20,000,000.00 target")).toBeInTheDocument();
    expect(screen.getByText("Target date: 2055-01-01")).toBeInTheDocument();
    expect(screen.getByText("Discussed with spouse")).toBeInTheDocument();
  });

  it("renders 'No target date set' when target_date is null, never a fabricated date", async () => {
    listMock.mockResolvedValue([{ ...goal, target_date: null }]);
    render(<GoalsPage />);
    await screen.findByText("Retire by 55");
    expect(screen.getByText("No target date set")).toBeInTheDocument();
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
  });

  it("creates a goal with no target date as null, not a fabricated date", async () => {
    render(<GoalsPage />);
    await screen.findByText("No active goals yet. Add your first goal above.");
    fireEvent.change(screen.getByLabelText("Goal name"), { target: { value: "Someday FIRE" } });
    fireEvent.change(screen.getByLabelText("Goal type"), { target: { value: "FIRE" } });
    fireEvent.change(screen.getByLabelText("Target amount"), { target: { value: "15000000" } });
    fireEvent.click(screen.getByRole("button", { name: "Add goal" }));

    await waitFor(() => expect(createMock).toHaveBeenCalledWith(expect.objectContaining({ target_date: null })));
  });

  it("edits goal metadata", async () => {
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
  });

  it("archives and restores a goal", async () => {
    let current: WealthGoal[] = [goal];
    listMock.mockImplementation(async (includeArchived = false) => includeArchived ? current : current.filter((item) => !item.is_archived));
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
  });

  it("keeps validation and API failures honest", async () => {
    listMock.mockRejectedValue(new Error("goals offline"));
    render(<GoalsPage />);
    expect(await screen.findByRole("alert")).toHaveTextContent("goals offline");

    fireEvent.change(screen.getByLabelText("Goal name"), { target: { value: "Debt-free" } });
    fireEvent.change(screen.getByLabelText("Target amount"), { target: { value: "0" } });
    fireEvent.click(screen.getByRole("button", { name: "Add goal" }));
    expect(screen.getByText("Enter a goal name and a positive target amount.")).toBeInTheDocument();
    expect(createMock).not.toHaveBeenCalled();
  });

  it("does not introduce guarantee, timeline, or advice language now that Progress/Gap/Health are real", async () => {
    listMock.mockResolvedValue([goal]);
    render(<GoalsPage />);
    await screen.findByText("Retire by 55");
    // Goal Progress & Funding Health milestone makes "Designated funding",
    // "Goal progress", "Funding gap", and "Funding health" real, allowed
    // vocabulary (see goalFunding.ts). What must still never appear is a
    // guarantee, a timeline promise, or advice.
    await screen.findByText("Goal progress");
    expect(screen.queryByText(/guaranteed|on track|projected completion|expected return|probability of success|recommended contribution|forecast/i)).not.toBeInTheDocument();
  });

  describe("Goal Progress & Funding Health", () => {
    it("shows Target, Designated funding, Goal progress, and Funding gap from allocation evidence", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000 }]);
      allocationsListMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 300000 }]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText("Goal progress")).toBeInTheDocument();
      expect(screen.getByText((_, el) => el?.textContent === "฿300,000.00")).toBeInTheDocument();
      expect(screen.getByText("30%")).toBeInTheDocument();
      expect(screen.getByText((_, el) => el?.textContent === "฿700,000.00")).toBeInTheDocument();
    });

    it("does not clamp progress over 100% and floors the funding gap at zero", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 500000 }]);
      allocationsListMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 600000 }]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText("120%")).toBeInTheDocument();
      expect(screen.getByText((_, el) => el?.textContent === "฿0.00")).toBeInTheDocument();
    });

    it("keeps Goal Progress unavailable (not 0%) when allocation evidence fails to load", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsListMock.mockRejectedValue(new Error("allocations offline"));
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText("Goal progress unavailable — funding data failed to load.")).toBeInTheDocument();
      expect(screen.queryByText("0%")).not.toBeInTheDocument();
      expect(screen.queryByText("Goal progress")).not.toBeInTheDocument();
    });

    it("reports Cash source funding health as Supported when balance covers designated amount", async () => {
      listMock.mockResolvedValue([goal]);
      cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 450000 }]);
      allocationsListMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 300000 }]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText((_, el) => el?.textContent === "Current value ฿450,000.00 · Funding health: Supported")).toBeInTheDocument();
    });

    it("warns when designated Cash funding exceeds the account's current balance", async () => {
      listMock.mockResolvedValue([goal]);
      cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 280000 }]);
      allocationsListMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 300000 }]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText((_, el) => el?.textContent === "Current value ฿280,000.00 · Attention: exceeds current value by ฿20,000.00")).toBeInTheDocument();
    });

    it("reports Portfolio source funding health from live holdings + prices, reusing the existing valuation formula", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsListMock.mockResolvedValue([portfolioAllocation]);
      holdingsMock.mockResolvedValue([holding({ symbol: "AAA", shares: 10000, avg_cost: 50 })]);
      pricesMock.mockResolvedValue([quote("AAA", 90)]); // portfolio.cash_balance (0) + 10,000 * 90 = 900,000

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText((_, el) => el?.textContent === "Current value ฿900,000.00 · Funding health: Supported")).toBeInTheDocument();
      expect(holdingsMock).toHaveBeenCalledWith(9);
      expect(pricesMock).toHaveBeenCalledWith(9);
    });

    it("shows funding health as unavailable when Portfolio valuation fails, without erasing Goal Progress", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000 }]);
      allocationsListMock.mockResolvedValue([portfolioAllocation]);
      holdingsMock.mockRejectedValue(new Error("holdings offline"));

      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText("Current value unavailable · Funding health unavailable")).toBeInTheDocument();
      // Goal Progress derives only from allocation evidence, which loaded fine —
      // it must stay based on the ฿700,000 designated, unaffected by the source's
      // valuation failure.
      expect(screen.getByText("70%")).toBeInTheDocument();
      expect(screen.getByText((_, el) => el?.textContent === "฿700,000.00")).toBeInTheDocument();
    });
  });

  describe("Funding sources", () => {
    it("shows a no-allocation state and offers active-only sources", async () => {
      listMock.mockResolvedValue([goal]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText("No funding sources designated yet.")).toBeInTheDocument();
      expect(cashAccountsMock).toHaveBeenCalledWith(false);

      const sourceSelect = screen.getByLabelText("Funding source") as HTMLSelectElement;
      const optionLabels = Array.from(sourceSelect.options).map((option) => option.textContent);
      expect(optionLabels).toContain("Wedding Savings");
    });

    it("adds a Cash Account funding source", async () => {
      listMock.mockResolvedValue([goal]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");
      await screen.findByText("No funding sources designated yet.");

      fireEvent.change(screen.getByLabelText("Funding source"), { target: { value: "5" } });
      fireEvent.change(screen.getByLabelText("Designated amount"), { target: { value: "300000" } });
      fireEvent.click(screen.getByRole("button", { name: "Add funding source" }));

      await waitFor(() => expect(allocationsCreateMock).toHaveBeenCalledWith(1, {
        cash_account_id: 5,
        portfolio_id: undefined,
        allocated_amount: 300000,
        currency: "THB",
      }));
    });

    it("adds a Portfolio funding source", async () => {
      listMock.mockResolvedValue([goal]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");
      await screen.findByText("No funding sources designated yet.");

      fireEvent.change(screen.getByLabelText("Funding source kind"), { target: { value: "PORTFOLIO" } });
      fireEvent.change(screen.getByLabelText("Funding source"), { target: { value: "9" } });
      fireEvent.change(screen.getByLabelText("Designated amount"), { target: { value: "700000" } });
      fireEvent.click(screen.getByRole("button", { name: "Add funding source" }));

      await waitFor(() => expect(allocationsCreateMock).toHaveBeenCalledWith(1, {
        cash_account_id: undefined,
        portfolio_id: 9,
        allocated_amount: 700000,
        currency: "THB",
      }));
    });

    it("renders an existing allocation, including an archived source", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsListMock.mockResolvedValue([{ ...cashAllocation, source_is_archived: true }]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText((_, el) => el?.textContent === "Wedding Savings (Cash Account, archived)")).toBeInTheDocument();
      expect(screen.getByText((_, el) => el?.textContent === "฿300,000.00 designated")).toBeInTheDocument();
    });

    it("edits a funding source's designated amount", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsListMock.mockResolvedValue([cashAllocation]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");
      await screen.findByText((_, el) => el?.textContent === "฿300,000.00 designated");

      fireEvent.click(screen.getByRole("button", { name: "Edit designated amount for Wedding Savings" }));
      fireEvent.change(screen.getByLabelText("Edit designated amount for Wedding Savings"), { target: { value: "250000" } });
      fireEvent.click(screen.getByRole("button", { name: "Save" }));

      await waitFor(() => expect(allocationsUpdateMock).toHaveBeenCalledWith(1, 100, { allocated_amount: 250000 }));
    });

    it("removes a funding source", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsListMock.mockResolvedValue([cashAllocation]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");
      await screen.findByText((_, el) => el?.textContent === "฿300,000.00 designated");

      fireEvent.click(screen.getByRole("button", { name: "Remove Wedding Savings as a funding source" }));

      await waitFor(() => expect(allocationsDeleteMock).toHaveBeenCalledWith(1, 100));
    });

    it("keeps funding-source load failures honest", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsListMock.mockRejectedValue(new Error("allocations offline"));
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(await screen.findByText("allocations offline")).toBeInTheDocument();
    });
  });

  describe("Goal What-If", () => {
    beforeEach(() => {
      // Fix "today" so reach-date/target-date output is deterministic. Only
      // Date is faked — timers stay real so Testing Library's async
      // find/waitFor polling keeps working.
      vi.useFakeTimers({ toFake: ["Date"] });
      vi.setSystemTime(new Date("2026-01-01T00:00:00Z"));
    });

    afterEach(() => {
      vi.useRealTimers();
    });

    it("is collapsed by default", async () => {
      listMock.mockResolvedValue([goal]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      expect(screen.getByRole("button", { name: "What-If" })).toBeInTheDocument();
      expect(screen.queryByLabelText(`What-If monthly contribution for ${goal.name}`)).not.toBeInTheDocument();
    });

    it("expands on user action", async () => {
      listMock.mockResolvedValue([goal]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(screen.getByLabelText(`What-If monthly contribution for ${goal.name}`)).toBeInTheDocument();
      expect(screen.getByLabelText(`What-If annual return assumption for ${goal.name}`)).toBeInTheDocument();
    });

    it("shows What-If as unavailable (not a zero projection) when allocation evidence fails to load", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsListMock.mockRejectedValue(new Error("allocations offline"));
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(await screen.findByText("What-If unavailable — funding data failed to load.")).toBeInTheDocument();
    });

    it("keeps What-If loading distinct from allocation failure or zero funding", async () => {
      listMock.mockResolvedValue([goal]);
      allocationsListMock.mockReturnValue(new Promise(() => {}));
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(screen.getByText("What-If loading — funding data is still loading.")).toBeInTheDocument();
      expect(screen.queryByText("What-If unavailable — funding data failed to load.")).not.toBeInTheDocument();
    });

    it("treats a legitimately empty allocation list as a real zero starting value, not an error", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsListMock.mockResolvedValue([]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(await screen.findByText((_, el) => el?.textContent === "Under these assumptions, designated funding would not reach ฿1,000,000.00 within 50 years.")).toBeInTheDocument();
    });

    it("defaults the contribution scenario to 0% return and a 0 monthly contribution", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsListMock.mockResolvedValue([]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(await screen.findByText((_, el) => el?.textContent === "Monthly contribution: ฿0.00 · Annual return assumption: 0%")).toBeInTheDocument();
    });

    it("shows a deterministic reach-date under a positive monthly contribution", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1200000, target_date: null }]);
      allocationsListMock.mockResolvedValue([]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      fireEvent.change(screen.getByLabelText(`What-If monthly contribution for ${goal.name}`), { target: { value: "100000" } });

      // 0% return, ฿100,000/month from a ฿0 start reaches ฿1,200,000 in exactly
      // 12 months from the fixed "today" of 2026-01-01 -> January 2027.
      expect(await screen.findByText((_, el) => el?.textContent === "Under these assumptions, designated funding would reach ฿1,200,000.00 around January 2027.")).toBeInTheDocument();
    });

    it("echoes the user-supplied annual return assumption explicitly", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      allocationsListMock.mockResolvedValue([]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      fireEvent.change(screen.getByLabelText(`What-If annual return assumption for ${goal.name}`), { target: { value: "5" } });

      expect(await screen.findByText((_, el) => el?.textContent === "Monthly contribution: ฿0.00 · Annual return assumption: 5%")).toBeInTheDocument();
    });

    it("shows the target-date projection when the goal has a saved target date", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1200000, target_date: "2027-01-01" }]);
      allocationsListMock.mockResolvedValue([]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      fireEvent.change(screen.getByLabelText(`What-If monthly contribution for ${goal.name}`), { target: { value: "50000" } });

      // asOfDate 2026-01-01 -> target 2027-01-01 is 12 months; 50,000 * 12 = 600,000, a 600,000 shortfall against 1,200,000.
      expect(await screen.findByText((_, el) => el?.textContent === "Saved target date: 2027-01-01 · Projected amount by that date: ฿600,000.00 · ฿600,000.00 below the current target")).toBeInTheDocument();
    });

    it("handles a saved target date that has already passed honestly, without blocking the reach-date result", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 600000, target_date: "2020-01-01" }]);
      allocationsListMock.mockResolvedValue([]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      fireEvent.change(screen.getByLabelText(`What-If monthly contribution for ${goal.name}`), { target: { value: "50000" } });

      expect(await screen.findByText("Saved target date (2020-01-01) has passed.")).toBeInTheDocument();
      // The reach-date scenario is still computed even though the saved target date is historical.
      expect(screen.getByText((_, el) => el?.textContent === "Under these assumptions, designated funding would reach ฿600,000.00 around January 2027.")).toBeInTheDocument();
    });

    it("keeps an OVER_ALLOCATED Funding Health warning visible alongside the What-If projection", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1000000, target_date: null }]);
      cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 100000 }]);
      allocationsListMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 300000 }]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(await screen.findByText("Funding health for this goal's sources:")).toBeInTheDocument();
      expect(screen.getAllByText((_, el) => el?.textContent === "Current value ฿100,000.00 · Attention: exceeds current value by ฿200,000.00").length).toBeGreaterThan(0);
    });

    it("uses the full designated amount even when its source is OVER_ALLOCATED", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 200000, target_date: null }]);
      cashAccountsMock.mockResolvedValue([{ ...cashAccount, balance: 100000 }]);
      allocationsListMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 300000 }]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(await screen.findByText((_, el) => el?.textContent === "Designated funding already reaches ฿200,000.00 under these assumptions.")).toBeInTheDocument();
    });

    it("sums multiple designated funding sources without using their current values", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 900000, target_date: null }]);
      allocationsListMock.mockResolvedValue([cashAllocation, portfolioAllocation]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(await screen.findByText((_, el) => el?.textContent === "Designated funding already reaches ฿900,000.00 under these assumptions.")).toBeInTheDocument();
    });

    it("does not let an UNAVAILABLE source Funding Health change the What-If starting value", async () => {
      // Designated funding is 700,000 (from the Portfolio allocation); its
      // valuation fails (holdingsMock rejects), so Funding Health is
      // UNAVAILABLE for that source — but the What-If starting value must
      // still be the full 700,000 designated, proven here by setting the
      // target below it and asserting "already reached".
      listMock.mockResolvedValue([{ ...goal, target_amount: 500000, target_date: null }]);
      allocationsListMock.mockResolvedValue([portfolioAllocation]);
      holdingsMock.mockRejectedValue(new Error("holdings offline"));
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      expect(await screen.findByText("Funding health for this goal's sources:")).toBeInTheDocument();
      expect(screen.getAllByText("Current value unavailable · Funding health unavailable").length).toBeGreaterThan(0);
      expect(screen.getByText((_, el) => el?.textContent === "Designated funding already reaches ฿500,000.00 under these assumptions.")).toBeInTheDocument();
    });

    it("never introduces forecast, probability, guarantee, or advice language in the What-If output", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 1200000, target_date: "2027-01-01" }]);
      allocationsListMock.mockResolvedValue([]);
      render(<GoalsPage />);
      await screen.findByText("Retire by 55");

      fireEvent.click(screen.getByRole("button", { name: "What-If" }));
      fireEvent.change(screen.getByLabelText(`What-If monthly contribution for ${goal.name}`), { target: { value: "50000" } });
      await screen.findByText((_, el) => el?.textContent === "Saved target date: 2027-01-01 · Projected amount by that date: ฿600,000.00 · ฿600,000.00 below the current target");

      expect(screen.queryByText(/forecast|expected return|probability|guaranteed|on track|likely to|recommended contribution|should contribute/i)).not.toBeInTheDocument();
    });
  });
});
