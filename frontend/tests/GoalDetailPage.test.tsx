import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import GoalDetailPage from "@/app/goals/[id]/page";
import {
  createGoalFundingAllocation,
  createGoalScenario,
  deleteGoalFundingAllocation,
  getCashFlowReport,
  getHoldings,
  getLegacyGoalProfileEvidence,
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
  type CashFlowEvent,
  type FactualReviewResponse,
  type GoalContextResponse,
  type GoalFundingAllocation,
  type LegacyGoalProfileEvidenceResponse,
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
  getCashFlowReport: vi.fn(),
  getHoldings: vi.fn(),
  getLegacyGoalProfileEvidence: vi.fn(),
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
const legacyEvidenceMock = vi.mocked(getLegacyGoalProfileEvidence);
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
const cashFlowMock = vi.mocked(getCashFlowReport);

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

async function configuredLegacyEvidence(): Promise<LegacyGoalProfileEvidenceResponse> {
  const goal_context = await configuredGoalContext();
  const edges = goal_context.goals.flatMap((contextGoal) => contextGoal.allocations
    .filter((allocation) => allocation.source_kind === "PORTFOLIO")
    .map((designation) => ({
      wealth_goal: {
        id: contextGoal.id,
        name: contextGoal.name,
        goal_type: contextGoal.goal_type,
        target_amount: contextGoal.target_amount,
        currency: contextGoal.currency,
        target_date: contextGoal.target_date,
        priority: contextGoal.priority,
        is_archived: contextGoal.is_archived,
        updated_at: contextGoal.updated_at,
      },
      designation,
      portfolio: { id: designation.source_id, name: designation.source_name },
      legacy_profile: {
        evidence_availability: "ALL_FIELDS_RECORDED" as const,
        goal_type: {
          raw_value: " retirement ",
          compatibility_projection: "RETIREMENT",
          compatibility_label_th: "เกษียณ",
          projection_status: "NORMALIZED" as const,
          comparison: contextGoal.goal_type === "RETIREMENT" ? "SAME_RECORDED_CODE" as const : "DIFFERENT_RECORDED_CODES" as const,
          provenance: "PORTFOLIO.GOAL_TYPE" as const,
        },
        goal_priority: {
          raw_value: "IMPORTANT",
          compatibility_projection: "IMPORTANT",
          compatibility_label_th: "สำคัญ",
          projection_status: "UNCHANGED" as const,
          provenance: "PORTFOLIO.GOAL_PRIORITY" as const,
        },
        goal_target_date: {
          raw_value: "2055-01-01",
          compatibility_projection: "2055-01-01",
          projection_status: "UNCHANGED" as const,
          comparison: "SAME_RECORDED_DATE" as const,
          provenance: "PORTFOLIO.GOAL_TARGET_DATE" as const,
        },
        goal_target_value: {
          raw_value: 20_000_000,
          compatibility_projection: 20_000_000,
          projection_status: "UNCHANGED" as const,
          unit_status: "UNSPECIFIED_IN_LEGACY_CONTRACT" as const,
          provenance: "PORTFOLIO.GOAL_TARGET_VALUE" as const,
        },
      },
    })));
  return {
    contract_version: "wealth.legacy-profile-evidence.v1",
    generated_at: "2026-08-31T00:00:00Z",
    completeness: "COMPLETE",
    scope: goal_context.scope,
    goal_context,
    evidence_edges: edges,
  };
}

describe("GoalDetailPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([goal]);
    allocationsMock.mockResolvedValue([]);
    contextMock.mockImplementation(configuredFactualReview);
    legacyEvidenceMock.mockImplementation(configuredLegacyEvidence);
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
    cashFlowMock.mockImplementation((month: string) => Promise.resolve({ month, events: [] }));
  });

  it("loads a valid URL-anchored goal and keeps a back link", async () => {
    render(<GoalDetailPage params={{ id: "1" }} />);
    expect(screen.getByText("Loading goal…")).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "Retire by 55" })).toBeInTheDocument();
    expect(listMock).toHaveBeenCalledWith(true);
    expect(contextMock).toHaveBeenCalledWith(true);
    expect(contextMock).toHaveBeenCalledTimes(1);
    expect(legacyEvidenceMock).toHaveBeenCalledWith(true);
    expect(allocationsMock).not.toHaveBeenCalled();
    expect(screen.getByRole("link", { name: "← Back to goals" })).toHaveAttribute("href", "/goals");
  });

  describe("Legacy Portfolio goal-profile evidence", () => {
    it("renders each designation edge after valuation with neutral raw/projection facts and adjacent disclosure", async () => {
      allocationsMock.mockResolvedValue([portfolioAllocation]);
      render(<GoalDetailPage params={{ id: "1" }} />);

      const section = await screen.findByLabelText("Legacy Portfolio goal-profile evidence");
      expect(within(section).getByText("Long-term Portfolio")).toBeInTheDocument();
      expect(within(section).getByText(/฿700,000.00 from this Portfolio is designated toward Retire by 55/)).toBeInTheDocument();
      expect(section).toHaveTextContent(/raw " retirement " · compatibility projection RETIREMENT/);
      expect(within(section).getAllByText("RETIREMENT").length).toBeGreaterThanOrEqual(1);
      const comparison = within(section).getByText(/The recorded codes are identical/);
      expect(comparison).toHaveTextContent(/does not establish.*same intended goal/i);
      const dateComparison = within(section).getByText(/The strict recorded dates are identical/);
      expect(dateComparison).toHaveTextContent(/does not establish.*same intended goal/i);
      expect(section.compareDocumentPosition(screen.getByLabelText("Factual valuation evidence")) & Node.DOCUMENT_POSITION_PRECEDING).toBeTruthy();
      expect(within(section).getByText(/Priority \(separate vocabularies\)/)).toBeInTheDocument();
      expect(within(section).getByText(/Legacy unit: unspecified in the legacy contract/)).toBeInTheDocument();
      expect(within(section).queryByText(/risk_personality|configured/i)).not.toBeInTheDocument();
      expect(within(section).queryByText(/equal target|target.*match|delta|ratio|coverage|shortfall/i)).not.toBeInTheDocument();
    });

    it("preserves separate evidence cards for multiple allocations using the same Portfolio", async () => {
      allocationsMock.mockResolvedValue([
        portfolioAllocation,
        { ...portfolioAllocation, id: 102, allocated_amount: 200000 },
      ]);
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByLabelText("Legacy evidence for designation 101");
      expect(screen.getByLabelText("Legacy evidence for designation 102")).toBeInTheDocument();
      expect(within(screen.getByLabelText("Legacy Portfolio goal-profile evidence")).getAllByText("Long-term Portfolio")).toHaveLength(2);
    });

    it("shows partial and unknown raw fields independently without rendering excluded runtime fields", async () => {
      allocationsMock.mockResolvedValue([portfolioAllocation]);
      legacyEvidenceMock.mockImplementation(async () => {
        const value = await configuredLegacyEvidence();
        const profile = value.evidence_edges[0].legacy_profile;
        profile.evidence_availability = "PARTIAL_FIELDS_RECORDED";
        profile.goal_type = {
          ...profile.goal_type,
          raw_value: "OLD_CUSTOM_GOAL",
          compatibility_projection: null,
          compatibility_label_th: null,
          projection_status: "UNRECOGNIZED",
          comparison: "NOT_COMPARABLE",
        };
        profile.goal_priority = { ...profile.goal_priority, raw_value: null, compatibility_projection: null, compatibility_label_th: null, projection_status: "UNSET" };
        Object.assign(profile as object, { risk_personality: "AGGRESSIVE", configured: false });
        return value;
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      const section = await screen.findByLabelText("Legacy Portfolio goal-profile evidence");
      expect(within(section).getByText('"OLD_CUSTOM_GOAL"')).toBeInTheDocument();
      expect(within(section).getByText(/recorded but unrecognized/)).toBeInTheDocument();
      expect(within(section).getByText(/Priority/).parentElement).toHaveTextContent("Not recorded");
      expect(within(section).queryByText("AGGRESSIVE")).not.toBeInTheDocument();
      expect(within(section).queryByText("false")).not.toBeInTheDocument();
    });

    it("keeps evidence failure local while funding editing and factual valuation remain available", async () => {
      allocationsMock.mockResolvedValue([portfolioAllocation]);
      legacyEvidenceMock.mockRejectedValue(new Error("evidence offline"));
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText("Legacy Portfolio goal-profile evidence is unavailable.")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Add funding source" })).toBeInTheDocument();
      expect(screen.getByLabelText("Factual valuation evidence")).toBeInTheDocument();
      expect(screen.getByRole("heading", { name: "Retire by 55" })).toBeInTheDocument();
    });

    it("does not hold the core Goal Detail behind a pending supplemental request", async () => {
      allocationsMock.mockResolvedValue([portfolioAllocation]);
      const pending = deferred<LegacyGoalProfileEvidenceResponse>();
      legacyEvidenceMock.mockReturnValue(pending.promise);
      render(<GoalDetailPage params={{ id: "1" }} />);

      expect(await screen.findByRole("heading", { name: "Retire by 55" })).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Add funding source" })).toBeInTheDocument();
      expect(screen.getByLabelText("Factual valuation evidence")).toBeInTheDocument();
      expect(screen.getByText("Loading legacy Portfolio goal-profile evidence…")).toBeInTheDocument();
    });

    it("does not hold a funding refresh behind a pending supplemental refresh", async () => {
      allocationsMock.mockResolvedValue([cashAllocation]);
      const pending = deferred<LegacyGoalProfileEvidenceResponse>();
      legacyEvidenceMock
        .mockImplementationOnce(configuredLegacyEvidence)
        .mockReturnValueOnce(pending.promise);
      render(<GoalDetailPage params={{ id: "1" }} />);
      const remove = await screen.findByRole("button", { name: "Remove Wedding Savings as a funding source" });

      fireEvent.click(remove);
      await waitFor(() => expect(allocationsDeleteMock).toHaveBeenCalledWith(1, 100));
      await waitFor(() => expect(contextMock).toHaveBeenCalledTimes(2));
      await waitFor(() => expect(screen.getByRole("button", { name: "Remove Wedding Savings as a funding source" })).toBeEnabled());
      expect(screen.getByLabelText("Factual valuation evidence")).toBeInTheDocument();
      expect(screen.getByText("Loading legacy Portfolio goal-profile evidence…")).toBeInTheDocument();
    });

    it("fails closed locally when evidence differs from the accepted Goal Context", async () => {
      allocationsMock.mockResolvedValue([portfolioAllocation]);
      legacyEvidenceMock.mockImplementation(async () => {
        const value = await configuredLegacyEvidence();
        value.evidence_edges[0].designation.designated_amount += 1;
        return value;
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(/Goal Context is inconsistent/)).toBeInTheDocument();
      expect(screen.queryByLabelText("Legacy Portfolio goal-profile evidence")).not.toBeInTheDocument();
      expect(screen.getByRole("heading", { name: "Retire by 55" })).toBeInTheDocument();
    });

    it("does not apply an older evidence response after a rapid route transition", async () => {
      const oldEvidence = await configuredLegacyEvidence();
      const pending = deferred<LegacyGoalProfileEvidenceResponse>();
      legacyEvidenceMock.mockReturnValueOnce(pending.promise);
      const { rerender } = render(<GoalDetailPage params={{ id: "1" }} />);

      listMock.mockResolvedValue([goal, secondGoal]);
      allocationsMock.mockImplementation(async (id) => id === 2 ? [{ ...portfolioAllocation, id: 202, wealth_goal_id: 2 }] : [portfolioAllocation]);
      rerender(<GoalDetailPage params={{ id: "2" }} />);
      expect(await screen.findByRole("heading", { name: "Buy a home" })).toBeInTheDocument();
      expect(await screen.findByLabelText("Legacy evidence for designation 202")).toBeInTheDocument();

      pending.resolve(oldEvidence);
      await waitFor(() => expect(screen.queryByLabelText("Legacy evidence for designation 101")).not.toBeInTheDocument());
      expect(screen.getByRole("heading", { name: "Buy a home" })).toBeInTheDocument();
    });
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

  describe("Goal Affordability Bridge", () => {
    // Fixed "today" so the trailing completed-month window is deterministic:
    // local 2026-08-15 -> window is 2026-05, 2026-06, 2026-07.
    let nextAffordabilityEventId = 9000;

    // A cash account the user has actually begun tracking. A baseline is the
    // repository's marker for that (the same marker Recorded Expense Coverage
    // uses); the default `cashAccount` fixture deliberately has none.
    const trackedCashAccount: CashAccount = {
      ...cashAccount,
      baseline: {
        id: 1,
        cash_account_id: cashAccount.id,
        effective_on: "2026-01-01",
        observed_balance: 300000,
        created_at: "2026-01-01T00:00:00",
      },
    };

    /** A tracked account whose baseline began on the given date (W1: pre-tracking presence gate). */
    function trackedAccountWithBaseline(effectiveOn: string): CashAccount {
      return {
        ...cashAccount,
        baseline: {
          id: 1,
          cash_account_id: cashAccount.id,
          effective_on: effectiveOn,
          observed_balance: 300000,
          created_at: "2026-01-01T00:00:00",
        },
      };
    }

    beforeEach(() => {
      vi.setSystemTime(new Date("2026-08-15T12:00:00Z"));
      listMock.mockResolvedValue([{ ...goal, target_amount: 120_000, target_date: "2027-08-15" }]);
    });

    afterEach(() => {
      vi.useRealTimers();
    });

    function flowEvent(month: string, overrides: Partial<CashFlowEvent> = {}): CashFlowEvent {
      return {
        id: nextAffordabilityEventId++,
        workspace_id: 1,
        cash_account_id: 5,
        account_name: "Wedding Savings",
        account_is_archived: false,
        transaction_type: "INCOME",
        amount: 0,
        signed_amount: 0,
        occurred_on: `${month}-10`,
        category: null,
        note: null,
        created_at: "2026-08-26T00:00:00",
        ...overrides,
      };
    }

    function income(month: string, amount: number): CashFlowEvent {
      return flowEvent(month, { transaction_type: "INCOME", amount, signed_amount: amount });
    }

    function expense(month: string, amount: number): CashFlowEvent {
      return flowEvent(month, { transaction_type: "EXPENSE", amount, signed_amount: -amount });
    }

    function withMonthlyCashFlow(byMonth: Record<string, CashFlowEvent[] | "error">) {
      cashFlowMock.mockImplementation((month: string) => {
        const value = byMonth[month];
        if (value === "error") return Promise.reject(new Error("cash flow offline"));
        return Promise.resolve({ month, events: value ?? [] });
      });
    }

    it("does not block Goal rendering while affordability data is loading", async () => {
      const pending = deferred<{ month: string; events: CashFlowEvent[] }>();
      cashFlowMock.mockReturnValue(pending.promise);
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByRole("heading", { name: "Retire by 55" })).toBeInTheDocument();
      expect(await screen.findByText("Checking affordability…")).toBeInTheDocument();
    });

    it("renders AFFORDABLE with the standing and independent-goal disclosures", async () => {
      withMonthlyCashFlow({
        "2026-05": [income("2026-05", 17_000), expense("2026-05", 5_000)],
        "2026-06": [income("2026-06", 20_000), expense("2026-06", 5_000)],
        "2026-07": [income("2026-07", 14_000), expense("2026-07", 5_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByRole("heading", { name: "Can I afford this goal?" })).toBeInTheDocument();
      expect(await screen.findByText(
        /Based on your recorded cash flow over the last 3 completed months, your average monthly surplus is ฿12,000\.00, enough to cover the ฿10,000\.00\/month this goal needs\./,
      )).toBeInTheDocument();
      expect(screen.getByText(/not reserved for this goal and may/)).toBeInTheDocument();
      expect(screen.getByText(/Each goal is evaluated independently\./)).toBeInTheDocument();
    });

    it("renders SHORTFALL using the exact recorded evidence-month count", async () => {
      withMonthlyCashFlow({
        "2026-05": [income("2026-05", 10_000), expense("2026-05", 5_000)],
        "2026-06": [income("2026-06", 12_000), expense("2026-06", 5_000)],
        "2026-07": [income("2026-07", 11_000), expense("2026-07", 5_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        /Based on your recorded cash flow over the last 3 completed months, your average monthly surplus is ฿6,000\.00, which is ฿4,000\.00 short of the ฿10,000\.00\/month this goal needs\./,
      )).toBeInTheDocument();
    });

    it("requests exactly the three completed calendar months and never the current one", async () => {
      withMonthlyCashFlow({});
      render(<GoalDetailPage params={{ id: "1" }} />);
      await waitFor(() => expect(cashFlowMock).toHaveBeenCalledTimes(3));
      expect(cashFlowMock.mock.calls.map(([month]) => month)).toEqual(["2026-05", "2026-06", "2026-07"]);
      expect(cashFlowMock).not.toHaveBeenCalledWith("2026-08");
    });

    it("derives the requested months from the local calendar just after a month boundary", async () => {
      // Local 2026-09-01T00:00:30. In Thailand (UTC+7) this instant is still
      // 2026-08-31 in UTC, so a toISOString()-derived anchor would request
      // May/June/July and silently drop August — the most recent completed
      // month — for the first 7 hours of every month.
      vi.setSystemTime(new Date(2026, 8, 1, 0, 0, 30));
      withMonthlyCashFlow({});
      render(<GoalDetailPage params={{ id: "1" }} />);
      await waitFor(() => expect(cashFlowMock).toHaveBeenCalledTimes(3));
      expect(cashFlowMock.mock.calls.map(([month]) => month)).toEqual(["2026-06", "2026-07", "2026-08"]);
      expect(cashFlowMock).not.toHaveBeenCalledWith("2026-09");
    });

    it("derives the requested months from the local calendar just before a month boundary", async () => {
      vi.setSystemTime(new Date(2026, 7, 31, 23, 59, 30));
      withMonthlyCashFlow({});
      render(<GoalDetailPage params={{ id: "1" }} />);
      await waitFor(() => expect(cashFlowMock).toHaveBeenCalledTimes(3));
      expect(cashFlowMock.mock.calls.map(([month]) => month)).toEqual(["2026-05", "2026-06", "2026-07"]);
    });

    it("fails closed when one month fails technically, never degrading to a smaller sample", async () => {
      withMonthlyCashFlow({
        "2026-06": [income("2026-06", 13_000), expense("2026-06", 5_000)],
        "2026-07": [income("2026-07", 17_000), expense("2026-07", 5_000)],
        "2026-05": "error",
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        "Affordability can't be assessed yet — Cash Flow data could not be fully loaded. Try again.",
      )).toBeInTheDocument();
      expect(screen.queryByText(/the last 2 completed months/)).not.toBeInTheDocument();
      expect(screen.queryByText(/completed month/)).not.toBeInTheDocument();
      expect(screen.queryByText(/enough to cover|short of/)).not.toBeInTheDocument();
    });

    it("fails closed on a technical failure even when the surviving months are negative", async () => {
      withMonthlyCashFlow({
        "2026-05": "error",
        "2026-06": [income("2026-06", 1_000), expense("2026-06", 9_000)],
        "2026-07": [income("2026-07", 1_000), expense("2026-07", 9_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        "Affordability can't be assessed yet — Cash Flow data could not be fully loaded. Try again.",
      )).toBeInTheDocument();
      expect(screen.queryByText(/enough to cover|short of/)).not.toBeInTheDocument();
    });

    it("reports a total retrieval failure as unavailable data, not as an absence of history", async () => {
      withMonthlyCashFlow({ "2026-05": "error", "2026-06": "error", "2026-07": "error" });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        "Affordability can't be assessed yet — Cash Flow data could not be fully loaded. Try again.",
      )).toBeInTheDocument();
      expect(screen.queryByText(/No completed month of recorded cash flow/)).not.toBeInTheDocument();
      expect(screen.queryByText(/enough to cover|short of/)).not.toBeInTheDocument();
    });

    it("fails closed when the cash-account population itself could not be loaded", async () => {
      // Only the page's own listCashAccounts(false) read fails; the Goal
      // Context fixture's include_archived read still resolves, so this
      // isolates the population load from the factual-review load.
      cashAccountsMock.mockImplementation((includeArchived?: boolean) => (includeArchived
        ? Promise.resolve([cashAccount])
        : Promise.reject(new Error("cash accounts offline"))));
      withMonthlyCashFlow({
        "2026-05": [income("2026-05", 17_000), expense("2026-05", 5_000)],
        "2026-06": [income("2026-06", 20_000), expense("2026-06", 5_000)],
        "2026-07": [income("2026-07", 14_000), expense("2026-07", 5_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        "Affordability can't be assessed yet — Cash account data could not be fully loaded. Try again.",
      )).toBeInTheDocument();
      expect(screen.queryByText(/enough to cover|short of/)).not.toBeInTheDocument();
    });

    it("does not give an untracked user a confident ฿0.00 shortfall from three empty months", async () => {
      cashAccountsMock.mockResolvedValue([]);
      withMonthlyCashFlow({ "2026-05": [], "2026-06": [], "2026-07": [] });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        "Affordability can't be assessed yet — Not enough recorded cash flow to assess affordability yet.",
      )).toBeInTheDocument();
      expect(screen.queryByText(/average monthly surplus/)).not.toBeInTheDocument();
      expect(screen.queryByText(/enough to cover|short of/)).not.toBeInTheDocument();
    });

    it("treats a genuinely empty month as a real zero once cash flow is actually tracked", async () => {
      // Every month retrieved successfully and the workspace tracks a cash
      // account, so the empty month is measured zero flow, not missing
      // evidence: (15,000 + 0 + 15,000) / 3 = 10,000.
      cashAccountsMock.mockResolvedValue([trackedCashAccount]);
      withMonthlyCashFlow({
        "2026-05": [income("2026-05", 20_000), expense("2026-05", 5_000)],
        "2026-06": [],
        "2026-07": [income("2026-07", 20_000), expense("2026-07", 5_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        /over the last 3 completed months, your average monthly surplus is ฿10,000\.00, enough to cover the ฿10,000\.00\/month/,
      )).toBeInTheDocument();
    });

    it("keeps a sparse but genuinely recorded history assessable", async () => {
      // The Goal page always resolves all three window months, so a genuine
      // 1-2 month sample reaches the helper as successful zero-flow months.
      // The helper's own 1-2 month evidence path is proven directly in
      // lib/goalAffordability.test.ts (missing-month and month -4 cases).
      cashAccountsMock.mockResolvedValue([trackedCashAccount]);
      withMonthlyCashFlow({
        "2026-05": [],
        "2026-06": [],
        "2026-07": [income("2026-07", 26_000), expense("2026-07", 5_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        /your average monthly surplus is ฿7,000\.00, which is ฿3,000\.00 short of the ฿10,000\.00\/month/,
      )).toBeInTheDocument();
    });

    it("W1: one month of evidence when tracking begins in the latest completed month — older empty responses never dilute it", async () => {
      // Baseline begins in July (the most recent completed month). May and
      // June predate tracking and hold no events, so they must be excluded
      // rather than diluting the average: (0 + 0 + 21,000) / 3 = 7,000 would
      // wrongly read SHORTFALL; the correct read is July alone, AFFORDABLE.
      cashAccountsMock.mockResolvedValue([trackedAccountWithBaseline("2026-07-01")]);
      withMonthlyCashFlow({
        "2026-05": [],
        "2026-06": [],
        "2026-07": [income("2026-07", 21_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        /Based on your recorded cash flow over the last 1 completed month, your average monthly surplus is ฿21,000\.00, enough to cover the ฿10,000\.00\/month this goal needs\./,
      )).toBeInTheDocument();
    });

    it("W1: two months of evidence when tracking begins in the middle completed month", async () => {
      // Baseline begins in June; May predates tracking and is excluded.
      cashAccountsMock.mockResolvedValue([trackedAccountWithBaseline("2026-06-01")]);
      withMonthlyCashFlow({
        "2026-05": [],
        "2026-06": [income("2026-06", 12_000)],
        "2026-07": [income("2026-07", 8_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        /Based on your recorded cash flow over the last 2 completed months, your average monthly surplus is ฿10,000\.00, enough to cover the ฿10,000\.00\/month this goal needs\./,
      )).toBeInTheDocument();
    });

    it("W1: three months of evidence when tracking began on the first day of the window", async () => {
      // Baseline begins exactly on the first day of the oldest window month,
      // so all three completed months qualify.
      cashAccountsMock.mockResolvedValue([trackedAccountWithBaseline("2026-05-01")]);
      withMonthlyCashFlow({
        "2026-05": [income("2026-05", 15_000), expense("2026-05", 5_000)],
        "2026-06": [income("2026-06", 20_000), expense("2026-06", 5_000)],
        "2026-07": [income("2026-07", 10_000), expense("2026-07", 5_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        /Based on your recorded cash flow over the last 3 completed months, your average monthly surplus is ฿10,000\.00, enough to cover the ฿10,000\.00\/month this goal needs\./,
      )).toBeInTheDocument();
    });

    it("W1: a real historical event before the active baseline remains admitted as evidence", async () => {
      // Baseline begins in July, but May already has a recorded event (e.g.
      // an archived account's history) proving population there too, so May
      // is rescued despite predating the baseline; June has neither and stays
      // excluded: (5,000 + 21,000) / 2 = 13,000.
      cashAccountsMock.mockResolvedValue([trackedAccountWithBaseline("2026-07-01")]);
      withMonthlyCashFlow({
        "2026-05": [income("2026-05", 5_000)],
        "2026-06": [],
        "2026-07": [income("2026-07", 21_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        /Based on your recorded cash flow over the last 2 completed months, your average monthly surplus is ฿13,000\.00, enough to cover the ฿10,000\.00\/month this goal needs\./,
      )).toBeInTheDocument();
    });

    it("W1: a technical failure still fails closed even when a tracking baseline is established", async () => {
      cashAccountsMock.mockResolvedValue([trackedAccountWithBaseline("2026-07-01")]);
      withMonthlyCashFlow({
        "2026-05": "error",
        "2026-06": [],
        "2026-07": [income("2026-07", 21_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        "Affordability can't be assessed yet — Cash Flow data could not be fully loaded. Try again.",
      )).toBeInTheDocument();
      expect(screen.queryByText(/enough to cover|short of/)).not.toBeInTheDocument();
    });

    it("never renders one goal's affordability under another after a route transition", async () => {
      listMock.mockResolvedValue([
        { ...goal, target_amount: 120_000, target_date: "2027-08-15" },
        { ...secondGoal, target_amount: 120_000, target_date: "2027-08-15" },
      ]);
      const firstGoalMonths = [
        deferred<{ month: string; events: CashFlowEvent[] }>(),
        deferred<{ month: string; events: CashFlowEvent[] }>(),
        deferred<{ month: string; events: CashFlowEvent[] }>(),
      ];
      let callIndex = 0;
      cashFlowMock.mockImplementation((month: string) => {
        callIndex += 1;
        if (callIndex <= 3) return firstGoalMonths[callIndex - 1].promise;
        return Promise.resolve({ month, events: [income(month, 17_000), expense(month, 5_000)] });
      });

      const { rerender } = render(<GoalDetailPage params={{ id: "1" }} />);
      await waitFor(() => expect(cashFlowMock).toHaveBeenCalledTimes(3));
      rerender(<GoalDetailPage params={{ id: "2" }} />);
      expect(await screen.findByRole("heading", { name: "Buy a home" })).toBeInTheDocument();
      expect(await screen.findByText(/your average monthly surplus is ฿12,000\.00/)).toBeInTheDocument();

      // Goal 1's in-flight Cash Flow now lands with a wildly different surplus.
      firstGoalMonths.forEach((pending, index) => {
        const month = ["2026-05", "2026-06", "2026-07"][index];
        pending.resolve({ month, events: [income(month, 905_000), expense(month, 5_000)] });
      });
      await waitFor(() => expect(screen.getByText(/your average monthly surplus is ฿12,000\.00/)).toBeInTheDocument());
      expect(screen.queryByText(/฿900,000\.00/)).not.toBeInTheDocument();
    });

    it("reports INSUFFICIENT_DATA using goalWhatIf's own reason when no target date is saved", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 120_000, target_date: null }]);
      withMonthlyCashFlow({
        "2026-05": [income("2026-05", 17_000), expense("2026-05", 5_000)],
        "2026-06": [income("2026-06", 20_000), expense("2026-06", 5_000)],
        "2026-07": [income("2026-07", 14_000), expense("2026-07", 5_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        "Affordability can't be assessed yet — A saved target date is required for this calculation.",
      )).toBeInTheDocument();
    });

    it("reports NO_CONTRIBUTION_REQUIRED when designated funding already meets the target, regardless of Cash Flow", async () => {
      allocationsMock.mockResolvedValue([{ ...cashAllocation, allocated_amount: 500_000 }]);
      withMonthlyCashFlow({ "2026-05": "error", "2026-06": "error", "2026-07": "error" });
      render(<GoalDetailPage params={{ id: "1" }} />);
      expect(await screen.findByText(
        "This goal's designated funding already meets its target — no monthly contribution is required.",
      )).toBeInTheDocument();
    });

    it("does not render the Affordability Bridge for an archived Goal", async () => {
      listMock.mockResolvedValue([{ ...goal, target_amount: 120_000, target_date: "2027-08-15", is_archived: true }]);
      withMonthlyCashFlow({
        "2026-05": [income("2026-05", 17_000), expense("2026-05", 5_000)],
        "2026-06": [income("2026-06", 20_000), expense("2026-06", 5_000)],
        "2026-07": [income("2026-07", 14_000), expense("2026-07", 5_000)],
      });
      render(<GoalDetailPage params={{ id: "1" }} />);
      await screen.findByRole("heading", { name: "Retire by 55" });
      expect(screen.queryByText("Can I afford this goal?")).not.toBeInTheDocument();
    });
  });
});
