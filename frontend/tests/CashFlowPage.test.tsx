import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import CashFlowPage from "@/app/cash-flow/page";
import {
  createCashAccountTransfer,
  createCashAccountTransaction,
  createCashEntryTemplate,
  createCashInvestmentTransfer,
  deleteCashEntryTemplate,
  getCashFlowReport,
  getCashFlowSettings,
  updateCashFlowSettings,
  updateCashEntryTemplate,
  listCashAccounts,
  listCashEntryTemplates,
  listPortfolios,
  type CashAccount,
  type CashEntryTemplate,
  type CashFlowEvent,
  type Portfolio,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createCashAccountTransfer: vi.fn(),
  createCashAccountTransaction: vi.fn(),
  createCashEntryTemplate: vi.fn(),
  createCashInvestmentTransfer: vi.fn(),
  deleteCashEntryTemplate: vi.fn(),
  getCashFlowReport: vi.fn(),
  getCashFlowSettings: vi.fn(),
  updateCashFlowSettings: vi.fn(),
  updateCashEntryTemplate: vi.fn(),
  listCashAccounts: vi.fn(),
  listCashEntryTemplates: vi.fn(),
  listPortfolios: vi.fn(),
}));

vi.mock("@/lib/cashFlow", async () => {
  const actual = await vi.importActual<typeof import("@/lib/cashFlow")>("@/lib/cashFlow");
  return { ...actual, currentMonthKey: () => "2026-08" };
});

const reportMock = vi.mocked(getCashFlowReport);
const accountsMock = vi.mocked(listCashAccounts);
const createMock = vi.mocked(createCashAccountTransaction);
const transferMock = vi.mocked(createCashAccountTransfer);
const getSettingsMock = vi.mocked(getCashFlowSettings);
const updateSettingsMock = vi.mocked(updateCashFlowSettings);
const portfoliosMock = vi.mocked(listPortfolios);
const investmentTransferMock = vi.mocked(createCashInvestmentTransfer);
const templatesMock = vi.mocked(listCashEntryTemplates);
const createTemplateMock = vi.mocked(createCashEntryTemplate);
const updateTemplateMock = vi.mocked(updateCashEntryTemplate);
const deleteTemplateMock = vi.mocked(deleteCashEntryTemplate);

function portfolio(overrides: Partial<Portfolio> = {}): Portfolio {
  return { id: 1, name: "Growth Portfolio", cash_balance: 0, created_at: "2026-08-01T00:00:00Z", ...overrides };
}

function account(overrides: Partial<CashAccount> = {}): CashAccount {
  return {
    id: 1,
    workspace_id: 1,
    name: "Everyday Cash",
    institution: "SCB",
    currency: "THB",
    balance: 1000,
    is_archived: false,
    created_at: "2026-08-01T00:00:00Z",
    updated_at: "2026-08-01T00:00:00Z",
    baseline: {
      id: 1,
      cash_account_id: 1,
      effective_on: "2026-08-01",
      observed_balance: 1000,
      created_at: "2026-08-01T00:00:00Z",
    },
    ...overrides,
  };
}

function event(overrides: Partial<CashFlowEvent> = {}): CashFlowEvent {
  return {
    id: 1,
    workspace_id: 1,
    cash_account_id: 1,
    account_name: "Everyday Cash",
    account_is_archived: false,
    transaction_type: "INCOME",
    amount: 100,
    signed_amount: 100,
    occurred_on: "2026-08-15",
    category: "Salary",
    note: null,
    created_at: "2026-08-15T08:00:00Z",
    ...overrides,
  };
}

function setReport(events: CashFlowEvent[] = []) {
  reportMock.mockResolvedValue({ month: "2026-08", events });
}

function template(overrides: Partial<CashEntryTemplate> = {}): CashEntryTemplate {
  return {
    id: 1,
    workspace_id: 1,
    name: "Monthly Salary",
    transaction_type: "INCOME",
    cash_account_id: 1,
    cash_account_name: "Everyday Cash",
    cash_account_is_archived: false,
    amount: 45000,
    category: "Salary",
    note: null,
    created_at: "2026-08-01T00:00:00Z",
    updated_at: "2026-08-01T00:00:00Z",
    ...overrides,
  };
}

describe("CashFlowPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    accountsMock.mockResolvedValue([account()]);
    setReport();
    getSettingsMock.mockResolvedValue({ target_coverage_months: null });
    updateSettingsMock.mockImplementation(async (body) => body);
    createMock.mockResolvedValue(event({ id: 9 }));
    // Empty by default so existing tests (written before Investment Transfer
    // existed) keep seeing exactly "Add income"/"Add expense"/"Transfer" —
    // only the tests in the "Investment transfer" describe block below
    // override this to a non-empty list.
    portfoliosMock.mockResolvedValue([]);
    templatesMock.mockResolvedValue([]);
    createTemplateMock.mockResolvedValue(template());
    updateTemplateMock.mockResolvedValue(template());
    deleteTemplateMock.mockResolvedValue({ deleted: 1 });
    investmentTransferMock.mockResolvedValue(event({
      id: 11,
      transaction_type: "INVESTMENT_TRANSFER",
      amount: -300,
      signed_amount: -300,
      category: null,
      counterparty_portfolio_id: 1,
      counterparty_portfolio_name: "Growth Portfolio",
      investment_direction: "TO_PORTFOLIO",
    }));
    transferMock.mockResolvedValue({
      id: 7,
      workspace_id: 1,
      source_cash_account_id: 1,
      destination_cash_account_id: 2,
      source_account_name: "Savings A",
      destination_account_name: "Savings B",
      amount: 100,
      occurred_on: "2026-08-15",
      note: null,
      created_at: "2026-08-15T08:00:00Z",
    });
  });

  it("shows the current-month empty state with zero summary", async () => {
    render(<CashFlowPage />);
    expect(await screen.findByText("August 2026")).toBeInTheDocument();
    expect(screen.getByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.")).toBeInTheDocument();
    expect(screen.getAllByText(/฿0\.00/).length).toBeGreaterThanOrEqual(3);
  });

  it("shows Income, Expenses, and positive Net Cash Flow", async () => {
    setReport([
      event({ id: 1, amount: 500 }),
      event({ id: 2, transaction_type: "EXPENSE", amount: 125, signed_amount: -125, category: "Food" }),
    ]);
    render(<CashFlowPage />);
    const summary = await screen.findByRole("region", { name: "Monthly summary" });
    expect(summary).toHaveTextContent("฿500.00");
    expect(summary).toHaveTextContent("฿125.00");
    expect(summary).toHaveTextContent("฿375.00");
    expect(screen.getByText("Food")).toBeInTheDocument();
  });

  it("supports negative Net Cash Flow", async () => {
    setReport([event({ transaction_type: "EXPENSE", amount: 900, signed_amount: -900, category: "Rent" })]);
    render(<CashFlowPage />);
    const summary = await screen.findByRole("region", { name: "Monthly summary" });
    expect(summary).toHaveTextContent(/-฿900\.00|−฿900\.00/);
  });

  it("excludes adjustments from summary while showing them honestly in activity", async () => {
    setReport([
      event({ id: 1, amount: 100 }),
      event({ id: 2, transaction_type: "ADJUSTMENT", amount: -25, signed_amount: -25, category: "Reconciliation", note: "Bank check" }),
    ]);
    render(<CashFlowPage />);
    expect(await screen.findByText("Adjustments:")).toBeInTheDocument();
    expect(screen.getAllByText(/Reconciliation/).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("Adjustment · Reconciliation")).toBeInTheDocument();
    expect(screen.getAllByText(/−฿25\.00/).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(/excluded from Income, Expenses, and Net Cash Flow/)).toBeInTheDocument();
  });

  it("aggregates multiple accounts and retains archived historical activity", async () => {
    setReport([
      event({ id: 1, cash_account_id: 1, amount: 75 }),
      event({ id: 2, cash_account_id: 2, account_name: "Old Reserve", account_is_archived: true, amount: 25 }),
    ]);
    render(<CashFlowPage />);
    expect(await screen.findByRole("region", { name: "Monthly summary" })).toHaveTextContent("฿100.00");
    expect(screen.getByText(/Old Reserve \(Archived\)/)).toBeInTheDocument();
    expect(screen.getByText(/2026-08-15 · Everyday Cash/)).toBeInTheDocument();
  });

  it("keeps first and last selected-month dates and excludes adjacent dates", async () => {
    setReport([
      event({ id: 1, occurred_on: "2026-07-31", amount: 5 }),
      event({ id: 2, occurred_on: "2026-08-01", amount: 10 }),
      event({ id: 3, occurred_on: "2026-08-31", amount: 20 }),
      event({ id: 4, occurred_on: "2026-09-01", amount: 40 }),
    ]);
    render(<CashFlowPage />);
    const summary = await screen.findByRole("region", { name: "Monthly summary" });
    expect(summary).toHaveTextContent("฿30.00");
    expect(screen.getByText("2026-08-01 · Everyday Cash")).toBeInTheDocument();
    expect(screen.getByText("2026-08-31 · Everyday Cash")).toBeInTheDocument();
    expect(screen.queryByText("2026-07-31 · Everyday Cash")).not.toBeInTheDocument();
    expect(screen.queryByText("2026-09-01 · Everyday Cash")).not.toBeInTheDocument();
  });

  it("navigates to the previous month and does not offer a future month", async () => {
    reportMock.mockImplementation(async (selectedMonth) => ({ month: selectedMonth, events: [] }));
    render(<CashFlowPage />);
    await screen.findByText("August 2026");
    expect(screen.getByRole("button", { name: "Next month" })).toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: "Previous month" }));
    expect(await screen.findByText("July 2026")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Today" })).toBeInTheDocument();
    expect(reportMock).toHaveBeenLastCalledWith("2026-07");
  });

  it("offers only active tracked accounts and adds income", async () => {
    accountsMock.mockResolvedValue([
      account({ id: 1, name: "Tracked" }),
      account({ id: 2, name: "Untracked", baseline: null }),
      account({ id: 3, name: "Archived", is_archived: true }),
    ]);
    let events: CashFlowEvent[] = [];
    reportMock.mockImplementation(async (selectedMonth) => ({ month: selectedMonth, events }));
    createMock.mockImplementation(async (id, body) => {
      events = [event({ id: 8, cash_account_id: id, account_name: "Tracked", amount: body.amount, occurred_on: body.occurred_on })];
      return events[0];
    });
    render(<CashFlowPage />);
    await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
    fireEvent.click(screen.getByRole("button", { name: "Add income" }));
    expect(screen.getByRole("option", { name: "Tracked" })).toBeInTheDocument();
    expect(screen.queryByRole("option", { name: "Untracked" })).not.toBeInTheDocument();
    expect(screen.queryByRole("option", { name: "Archived" })).not.toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Cash flow amount"), { target: { value: "250" } });
    fireEvent.change(screen.getByLabelText("Cash flow category"), { target: { value: "Salary" } });
    fireEvent.click(screen.getByRole("button", { name: "Save income" }));
    await waitFor(() => expect(createMock).toHaveBeenCalledWith(1, expect.objectContaining({ transaction_type: "INCOME", amount: 250, category: "Salary" })));
    expect(await screen.findByRole("region", { name: "Monthly summary" })).toHaveTextContent("฿250.00");
  });

  it("adds an expense and refreshes the selected-month report", async () => {
    let events: CashFlowEvent[] = [];
    reportMock.mockImplementation(async (selectedMonth) => ({ month: selectedMonth, events }));
    createMock.mockImplementation(async (id, body) => {
      events = [event({ id: 10, cash_account_id: id, transaction_type: "EXPENSE", amount: body.amount, signed_amount: -body.amount, category: body.category })];
      return events[0];
    });
    render(<CashFlowPage />);
    await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
    fireEvent.click(screen.getByRole("button", { name: "Add expense" }));
    fireEvent.change(screen.getByLabelText("Cash flow amount"), { target: { value: "80" } });
    fireEvent.change(screen.getByLabelText("Cash flow category"), { target: { value: "Food" } });
    fireEvent.click(screen.getByRole("button", { name: "Save expense" }));
    await waitFor(() => expect(createMock).toHaveBeenCalledWith(1, expect.objectContaining({ transaction_type: "EXPENSE", amount: 80, category: "Food" })));
    expect((await screen.findAllByText(/−฿80\.00/)).length).toBeGreaterThanOrEqual(1);
    expect(reportMock.mock.calls.length).toBeGreaterThanOrEqual(2);
  });

  it("offers Transfer only for active tracked accounts and renders one neutral logical activity", async () => {
    const savings = account({ id: 1, name: "Savings A" });
    const emergency = account({ id: 2, name: "Savings B", balance: 500 });
    accountsMock.mockResolvedValue([
      savings,
      emergency,
      account({ id: 3, name: "Untracked", baseline: null }),
      account({ id: 4, name: "Archived", is_archived: true }),
    ]);
    let events: CashFlowEvent[] = [];
    reportMock.mockImplementation(async (selectedMonth) => ({ month: selectedMonth, events }));
    transferMock.mockImplementation(async (body) => {
      events = [event({
        id: 7,
        transaction_type: "TRANSFER",
        amount: body.amount,
        signed_amount: 0,
        category: null,
        transfer_id: 7,
        transfer_source_account_name: "Savings A",
        transfer_destination_account_name: "Savings B",
      })];
      return {
        id: 7,
        workspace_id: 1,
        source_cash_account_id: body.source_cash_account_id,
        destination_cash_account_id: body.destination_cash_account_id,
        source_account_name: "Savings A",
        destination_account_name: "Savings B",
        amount: body.amount,
        occurred_on: body.occurred_on,
        note: body.note ?? null,
        created_at: "2026-08-15T08:00:00Z",
      };
    });
    render(<CashFlowPage />);
    await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
    fireEvent.click(screen.getByRole("button", { name: "Transfer" }));
    expect(screen.getByRole("option", { name: "Savings A" })).toBeInTheDocument();
    expect(screen.getAllByRole("option", { name: "Savings B" })).toHaveLength(2);
    expect(screen.queryByRole("option", { name: "Untracked" })).not.toBeInTheDocument();
    expect(screen.queryByRole("option", { name: "Archived" })).not.toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Transfer preview: Savings A → Savings B")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Transfer amount"), { target: { value: "100" } });
    fireEvent.click(screen.getByRole("button", { name: "Save transfer" }));
    await waitFor(() => expect(transferMock).toHaveBeenCalledWith(expect.objectContaining({
      source_cash_account_id: 1,
      destination_cash_account_id: 2,
      amount: 100,
    })));
    expect(await screen.findByText("2026-08-15 · Savings A → Savings B")).toBeInTheDocument();
    expect(screen.getAllByText("Transfer").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByRole("region", { name: "Monthly summary" })).toHaveTextContent("฿0.00");
    expect(screen.getAllByText(/Savings A → Savings B/)).toHaveLength(1);
  });

  describe("Investment transfer", () => {
    it("is hidden when no portfolio exists, even with a tracked account", async () => {
      portfoliosMock.mockResolvedValue([]);
      render(<CashFlowPage />);
      await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
      expect(screen.queryByRole("button", { name: "Investment transfer" })).not.toBeInTheDocument();
    });

    it("submits an outbound (Cash → Investment) transfer with a positive-magnitude payload", async () => {
      portfoliosMock.mockResolvedValue([portfolio()]);
      let events: CashFlowEvent[] = [];
      reportMock.mockImplementation(async (selectedMonth) => ({ month: selectedMonth, events }));
      investmentTransferMock.mockImplementation(async (accountId, body) => {
        const created = event({
          id: 11,
          cash_account_id: accountId,
          transaction_type: "INVESTMENT_TRANSFER",
          amount: -body.amount,
          signed_amount: -body.amount,
          category: null,
          occurred_on: body.occurred_on,
          counterparty_portfolio_id: body.portfolio_id,
          counterparty_portfolio_name: "Growth Portfolio",
          investment_direction: "TO_PORTFOLIO",
        });
        events = [created];
        return created;
      });
      render(<CashFlowPage />);
      await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
      fireEvent.click(await screen.findByRole("button", { name: "Investment transfer" }));
      fireEvent.change(screen.getByLabelText("Investment transfer amount"), { target: { value: "300" } });
      fireEvent.click(screen.getByRole("button", { name: "Record transfer" }));
      await waitFor(() => expect(investmentTransferMock).toHaveBeenCalledWith(1, expect.objectContaining({
        portfolio_id: 1,
        direction: "TO_PORTFOLIO",
        amount: 300,
      })));
      expect(await screen.findByText("2026-08-01 · Everyday Cash → Growth Portfolio")).toBeInTheDocument();
      expect(screen.getAllByText("Investment transfer").length).toBeGreaterThanOrEqual(1);
      expect(screen.getByRole("region", { name: "Monthly summary" })).toHaveTextContent("฿0.00");
    });

    it("submits an inbound (Investment → Cash) transfer with the reverse direction", async () => {
      portfoliosMock.mockResolvedValue([portfolio()]);
      let events: CashFlowEvent[] = [];
      reportMock.mockImplementation(async (selectedMonth) => ({ month: selectedMonth, events }));
      investmentTransferMock.mockImplementation(async (accountId, body) => {
        const created = event({
          id: 12,
          cash_account_id: accountId,
          transaction_type: "INVESTMENT_TRANSFER",
          amount: body.amount,
          signed_amount: body.amount,
          category: null,
          occurred_on: body.occurred_on,
          counterparty_portfolio_id: body.portfolio_id,
          counterparty_portfolio_name: "Growth Portfolio",
          investment_direction: "FROM_PORTFOLIO",
        });
        events = [created];
        return created;
      });
      render(<CashFlowPage />);
      await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
      fireEvent.click(await screen.findByRole("button", { name: "Investment transfer" }));
      fireEvent.change(screen.getByLabelText("Investment transfer direction"), { target: { value: "FROM_PORTFOLIO" } });
      fireEvent.change(screen.getByLabelText("Investment transfer amount"), { target: { value: "150" } });
      fireEvent.click(screen.getByRole("button", { name: "Record transfer" }));
      await waitFor(() => expect(investmentTransferMock).toHaveBeenCalledWith(1, expect.objectContaining({
        direction: "FROM_PORTFOLIO",
        amount: 150,
      })));
      expect(await screen.findByText("2026-08-01 · Growth Portfolio → Everyday Cash")).toBeInTheDocument();
    });

    it("falls back to a neutral label when the counterparty Portfolio has been deleted", async () => {
      portfoliosMock.mockResolvedValue([portfolio()]);
      setReport([event({
        id: 13,
        transaction_type: "INVESTMENT_TRANSFER",
        amount: -300,
        signed_amount: -300,
        category: null,
        counterparty_portfolio_id: null,
        counterparty_portfolio_name: null,
        investment_direction: "TO_PORTFOLIO",
      })]);
      render(<CashFlowPage />);
      expect(await screen.findByText("2026-08-15 · Everyday Cash → Investment portfolio (no longer available)")).toBeInTheDocument();
    });

    it("shows an inline error and creates nothing on API failure, without claiming automatic pairing anywhere", async () => {
      portfoliosMock.mockResolvedValue([portfolio()]);
      investmentTransferMock.mockRejectedValue(new Error("Cash activity cannot make the observed balance negative"));
      render(<CashFlowPage />);
      await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
      fireEvent.click(await screen.findByRole("button", { name: "Investment transfer" }));
      fireEvent.change(screen.getByLabelText("Investment transfer amount"), { target: { value: "300" } });
      fireEvent.click(screen.getByRole("button", { name: "Record transfer" }));
      expect(await screen.findByRole("alert")).toHaveTextContent("Cash activity cannot make the observed balance negative");
      expect(screen.getByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.")).toBeInTheDocument();
      const bodyText = document.body.textContent ?? "";
      for (const banned of ["Incomplete", "Unmatched", "Missing deposit", "Pending", "Awaiting confirmation"]) {
        expect(bodyText).not.toContain(banned);
      }
    });

    it("does not disturb the existing Add income / Add expense / Transfer flows", async () => {
      portfoliosMock.mockResolvedValue([portfolio()]);
      accountsMock.mockResolvedValue([account({ id: 1, name: "Savings A" }), account({ id: 2, name: "Savings B" })]);
      render(<CashFlowPage />);
      await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
      expect(screen.getByRole("button", { name: "Add income" })).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Add expense" })).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Transfer" })).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Investment transfer" })).toBeInTheDocument();
    });
  });

  it("prevents selecting the same account and handles insufficient funds honestly", async () => {
    accountsMock.mockResolvedValue([account({ id: 1, name: "Savings A" }), account({ id: 2, name: "Savings B" })]);
    transferMock.mockRejectedValue(new Error("Insufficient funds in source cash account"));
    render(<CashFlowPage />);
    await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
    fireEvent.click(screen.getByRole("button", { name: "Transfer" }));
    const destination = screen.getByLabelText("Transfer to account") as HTMLSelectElement;
    expect(Array.from(destination.options).map((option) => option.text)).toEqual(["Savings B"]);
    fireEvent.change(screen.getByLabelText("Transfer amount"), { target: { value: "100" } });
    fireEvent.click(screen.getByRole("button", { name: "Save transfer" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Insufficient funds in source cash account");
    expect(screen.getByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.")).toBeInTheDocument();
  });

  it("explains that transfers need two tracked accounts", async () => {
    accountsMock.mockResolvedValue([account({ id: 1, name: "Only account" })]);
    render(<CashFlowPage />);
    expect(await screen.findByText(/Transfer requires at least two active tracked Cash Accounts/)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Add or start tracking another account/ })).toHaveAttribute("href", "/cash");
  });

  it("guides the user to Cash Accounts when no active tracked account exists", async () => {
    accountsMock.mockResolvedValue([account({ baseline: null })]);
    setReport([]);
    render(<CashFlowPage />);
    expect(await screen.findByText(/No active tracked cash account is available/)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Start tracking under Cash Accounts/ })).toHaveAttribute("href", "/cash");
  });

  it("does not fabricate a zero report when the reporting request fails", async () => {
    reportMock.mockRejectedValue(new Error("report offline"));
    render(<CashFlowPage />);
    expect(await screen.findByRole("alert")).toHaveTextContent("report offline");
    expect(screen.queryByText("Monthly summary")).not.toBeInTheDocument();
    expect(screen.queryByText(/No cash flow events/)).not.toBeInTheDocument();
  });

  it("does not let a stale month response overwrite the newer selection", async () => {
    const pending: Array<{ month: string; resolve: (value: { month: string; events: CashFlowEvent[] }) => void }> = [];
    let callCount = 0;
    reportMock.mockImplementation(async (selectedMonth) => {
      callCount += 1;
      if (callCount === 1) return { month: selectedMonth, events: [] };
      return await new Promise((resolve) => pending.push({ month: selectedMonth, resolve }));
    });
    render(<CashFlowPage />);
    await screen.findByText("No cash flow events in August 2026. Income, Expenses, and Net Cash Flow are all ฿0.00.");
    fireEvent.click(screen.getByRole("button", { name: "Previous month" }));
    fireEvent.click(screen.getByRole("button", { name: "Next month" }));
    const latest = pending.find((request) => request.month === "2026-08");
    const stale = pending.find((request) => request.month === "2026-07");
    latest?.resolve({ month: "2026-08", events: [event({ amount: 200 })] });
    expect(await screen.findByRole("region", { name: "Monthly summary" })).toHaveTextContent("฿200.00");
    stale?.resolve({ month: "2026-07", events: [event({ amount: 999 })] });
    await waitFor(() => expect(screen.getByText("August 2026")).toBeInTheDocument());
    expect(screen.queryByText(/฿999\.00/)).not.toBeInTheDocument();
  });

  describe("Recorded expense coverage", () => {
    const earlyBaseline = { id: 1, cash_account_id: 1, effective_on: "2026-01-01", observed_balance: 1000, created_at: "2026-01-01T00:00:00Z" };
    // With currentMonthKey mocked to "2026-08", the recorded window is ["2026-05", "2026-06", "2026-07"].

    function reportForMonths(byMonth: Record<string, CashFlowEvent[]>) {
      reportMock.mockImplementation(async (selectedMonth) => ({ month: selectedMonth, events: byMonth[selectedMonth] ?? [] }));
    }

    it("renders the section above the month stepper with the not-affected-by-selection note", async () => {
      accountsMock.mockResolvedValue([account({ balance: 42000, baseline: earlyBaseline })]);
      reportForMonths({
        "2026-05": [event({ id: 1, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-05-01" })],
        "2026-06": [event({ id: 2, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-06-01" })],
        "2026-07": [event({ id: 3, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-07-01" })],
      });
      const { container } = render(<CashFlowPage />);
      const coverageHeading = await screen.findByRole("heading", { name: "Recorded expense coverage" });
      expect(screen.getByText("Not affected by the selected month.")).toBeInTheDocument();
      const selectedMonthLabel = screen.getByText("Selected month");
      expect(coverageHeading.compareDocumentPosition(selectedMonthLabel) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      expect(container).toBeInTheDocument();
    });

    it("computes an AVAILABLE result and does not change it when the selected month picker moves", async () => {
      accountsMock.mockResolvedValue([account({ balance: 42000, baseline: earlyBaseline })]);
      reportForMonths({
        "2026-05": [event({ id: 1, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-05-01" })],
        "2026-06": [event({ id: 2, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-06-01" })],
        "2026-07": [event({ id: 3, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-07-01" })],
      });
      render(<CashFlowPage />);
      await screen.findByText(/Tracked cash covers 4\.2 months/);
      // Cash Flow Trend's default 6-month window legitimately overlaps this
      // Coverage window (both request 2026-05/06/07, and Trend additionally
      // requests 2026-02/03/04 independently) — that duplication is accepted
      // by design (see docs). This test only proves Coverage's own fixed
      // window never moves when the month picker moves, so it compares deltas
      // rather than asserting an absolute call count.
      const callsFor = (target: string) => reportMock.mock.calls.filter((call) => call[0] === target).length;
      const baselineCalls05 = callsFor("2026-05");

      fireEvent.click(screen.getByRole("button", { name: "Previous month" }));
      await screen.findByText("July 2026");
      // A selection-derived window would have re-entered its loading state
      // synchronously as the effect fired; an independent one never reloads.
      expect(screen.queryByText("Loading recorded monthly expense evidence…")).not.toBeInTheDocument();
      fireEvent.click(screen.getByRole("button", { name: "Previous month" }));
      await screen.findByText("June 2026");
      expect(screen.queryByText("Loading recorded monthly expense evidence…")).not.toBeInTheDocument();

      // Let every pending promise settle, then prove the window never moved:
      // no new request for 2026-05 was made even though it was never selected.
      await waitFor(() => expect(reportMock).toHaveBeenCalledWith("2026-06"));
      await act(async () => { await Promise.resolve(); await Promise.resolve(); });
      expect(callsFor("2026-05")).toBe(baselineCalls05);
      expect(screen.getByText(/Tracked cash covers 4\.2 months/)).toBeInTheDocument();
    });

    it("refreshes coverage after a mutation even when the account payload is referentially identical", async () => {
      // Pins the real refresh signal: the accountsLoading true→false toggle,
      // NOT the identity of a freshly-parsed accounts array. A back-dated
      // expense can leave every account value unchanged and must still refresh.
      const stableAccounts = [account({ balance: 1000, baseline: earlyBaseline })];
      accountsMock.mockResolvedValue(stableAccounts);
      reportForMonths({ "2026-05": [], "2026-06": [], "2026-07": [] });
      createMock.mockResolvedValue(event({ id: 9 }));
      render(<CashFlowPage />);
      await screen.findByText(/No recorded expenses in the recorded months/);
      const coverageCallsBefore = reportMock.mock.calls.filter((call) => call[0] === "2026-06").length;

      fireEvent.click(screen.getByRole("button", { name: "Add expense" }));
      fireEvent.change(screen.getByLabelText("Cash flow amount"), { target: { value: "50" } });
      fireEvent.change(screen.getByLabelText("Cash flow category"), { target: { value: "Food" } });
      fireEvent.change(screen.getByLabelText("Cash flow date"), { target: { value: "2026-06-10" } });
      fireEvent.click(screen.getByRole("button", { name: "Save expense" }));

      await waitFor(() => expect(createMock).toHaveBeenCalled());
      await waitFor(() =>
        expect(reportMock.mock.calls.filter((call) => call[0] === "2026-06").length).toBeGreaterThan(coverageCallsBefore),
      );
    });

    it("shows a tracked-cash-balance loading state before account evidence resolves", async () => {
      let resolveAccounts: (value: CashAccount[]) => void = () => {};
      accountsMock.mockImplementation(() => new Promise((resolve) => { resolveAccounts = resolve; }));
      render(<CashFlowPage />);
      expect(await screen.findByText("Loading tracked cash balance…")).toBeInTheDocument();
      resolveAccounts([account({ balance: 1000, baseline: null })]);
      await waitFor(() => expect(screen.queryByText("Loading tracked cash balance…")).not.toBeInTheDocument());
    });

    it("shows a monthly-evidence loading state while recorded-month reports are in flight", async () => {
      accountsMock.mockResolvedValue([account({ balance: 1000, baseline: earlyBaseline })]);
      const pending: Array<{ month: string; resolve: (value: { month: string; events: CashFlowEvent[] }) => void }> = [];
      reportMock.mockImplementation(async (selectedMonth) => {
        if (selectedMonth === "2026-08") return { month: selectedMonth, events: [] };
        return await new Promise((resolve) => pending.push({ month: selectedMonth, resolve }));
      });
      render(<CashFlowPage />);
      expect(await screen.findByText("Loading recorded monthly expense evidence…")).toBeInTheDocument();
      pending.forEach((p) => p.resolve({ month: p.month, events: [] }));
      await waitFor(() => expect(screen.queryByText("Loading recorded monthly expense evidence…")).not.toBeInTheDocument());
    });

    it("shows INSUFFICIENT_EVIDENCE when the only baseline falls inside the current month", async () => {
      accountsMock.mockResolvedValue([account({ balance: 1000 })]); // default baseline effective_on "2026-08-01"
      render(<CashFlowPage />);
      expect(await screen.findByText("Not enough recorded history yet to calculate recorded expense coverage.")).toBeInTheDocument();
      expect(screen.getByText("0 of 3 months recorded")).toBeInTheDocument();
    });

    it("shows NO_RECORDED_EXPENSE when every recorded month has zero recorded expenses", async () => {
      accountsMock.mockResolvedValue([account({ balance: 9000, baseline: earlyBaseline })]);
      reportForMonths({ "2026-05": [], "2026-06": [], "2026-07": [] });
      render(<CashFlowPage />);
      expect(await screen.findByText(/No recorded expenses in the recorded months/)).toBeInTheDocument();
    });

    it("shows UNAVAILABLE when the account evidence fails to load, with a retry", async () => {
      accountsMock.mockRejectedValue(new Error("accounts offline"));
      render(<CashFlowPage />);
      expect(await screen.findByText("Recorded expense coverage is unavailable right now.")).toBeInTheDocument();
      const retry = screen.getAllByRole("button", { name: "Try again" }).find((button) => button.closest("section")?.getAttribute("aria-label") === "Recorded expense coverage");
      expect(retry).toBeTruthy();
    });

    it("shows UNAVAILABLE and fails closed when one recorded-month fetch fails, never averaging a partial subset", async () => {
      accountsMock.mockResolvedValue([account({ balance: 9000, baseline: earlyBaseline })]);
      reportMock.mockImplementation(async (selectedMonth) => {
        if (selectedMonth === "2026-06") throw new Error("month offline");
        return { month: selectedMonth, events: selectedMonth === "2026-07" ? [event({ transaction_type: "EXPENSE", amount: 30000, signed_amount: -30000, occurred_on: "2026-07-01" })] : [] };
      });
      render(<CashFlowPage />);
      expect(await screen.findByText("Recorded expense coverage is unavailable right now.")).toBeInTheDocument();
      expect(screen.queryByText(/Tracked cash covers/)).not.toBeInTheDocument();
    });

    it("retries a failed coverage load", async () => {
      accountsMock.mockResolvedValue([account({ balance: 9000, baseline: earlyBaseline })]);
      let fail = true;
      reportMock.mockImplementation(async (selectedMonth) => {
        if (selectedMonth === "2026-08") return { month: selectedMonth, events: [] };
        if (fail) throw new Error("month offline");
        return { month: selectedMonth, events: [] };
      });
      render(<CashFlowPage />);
      const coverageSection = (await screen.findByText("Recorded expense coverage is unavailable right now.")).closest("section")!;
      fail = false;
      fireEvent.click(within(coverageSection).getByRole("button", { name: "Try again" }));
      await waitFor(() => expect(within(coverageSection).getByText(/No recorded expenses in the recorded months/)).toBeInTheDocument());
    });

    it("discloses untracked active accounts", async () => {
      accountsMock.mockResolvedValue([
        account({ id: 1, balance: 9000, baseline: earlyBaseline }),
        account({ id: 2, name: "Untracked", balance: 5000, baseline: null }),
      ]);
      reportForMonths({ "2026-05": [], "2026-06": [], "2026-07": [] });
      render(<CashFlowPage />);
      expect(await screen.findByText("1 active cash account is not tracked and is not included.")).toBeInTheDocument();
    });

    it("discloses recorded expenses from archived accounts", async () => {
      accountsMock.mockResolvedValue([account({ balance: 9000, baseline: earlyBaseline })]);
      reportForMonths({
        "2026-05": [],
        "2026-06": [],
        "2026-07": [event({ transaction_type: "EXPENSE", amount: 500, signed_amount: -500, occurred_on: "2026-07-01", account_name: "Old Reserve", account_is_archived: true })],
      });
      render(<CashFlowPage />);
      expect(await screen.findByText("Recorded expenses include archived account(s) whose balances are not counted.")).toBeInTheDocument();
    });

    it("always discloses that goal designations are not deducted whenever tracked cash is shown", async () => {
      accountsMock.mockResolvedValue([account({ balance: 9000, baseline: earlyBaseline })]);
      reportForMonths({ "2026-05": [], "2026-06": [], "2026-07": [] });
      render(<CashFlowPage />);
      expect(await screen.findByText("Amounts designated toward goals are not deducted here.")).toBeInTheDocument();
    });

    it("discloses when tracking for an account began during the recorded period", async () => {
      accountsMock.mockResolvedValue([
        account({ id: 1, balance: 5000, baseline: earlyBaseline }),
        account({ id: 2, balance: 4000, baseline: { id: 2, cash_account_id: 2, effective_on: "2026-06-15", observed_balance: 4000, created_at: "2026-06-15T00:00:00Z" } }),
      ]);
      reportForMonths({ "2026-05": [], "2026-06": [], "2026-07": [] });
      render(<CashFlowPage />);
      expect(await screen.findByText("Cash tracking for 1 account began during this period.")).toBeInTheDocument();
    });

    it("updates coverage after a mutation refreshes account evidence", async () => {
      let accountsCall = 0;
      accountsMock.mockImplementation(async () => {
        accountsCall += 1;
        return [account({ balance: accountsCall === 1 ? 1000 : 1250, baseline: earlyBaseline })];
      });
      reportForMonths({ "2026-05": [], "2026-06": [], "2026-07": [] });
      createMock.mockResolvedValue(event({ id: 9 }));
      render(<CashFlowPage />);
      expect(await screen.findByText(/฿1,000\.00/)).toBeInTheDocument();
      fireEvent.click(screen.getByRole("button", { name: "Add income" }));
      fireEvent.change(screen.getByLabelText("Cash flow amount"), { target: { value: "250" } });
      fireEvent.change(screen.getByLabelText("Cash flow category"), { target: { value: "Salary" } });
      fireEvent.click(screen.getByRole("button", { name: "Save income" }));
      await waitFor(() => expect(screen.getByText(/฿1,250\.00/)).toBeInTheDocument());
    });

    it("drops a stale coverage response once a newer account reload has started", async () => {
      let accountsCall = 0;
      accountsMock.mockImplementation(async () => {
        accountsCall += 1;
        return [account({ balance: accountsCall === 1 ? 1000 : 9000, baseline: earlyBaseline })];
      });
      const pending: Array<{ month: string; resolve: (value: { month: string; events: CashFlowEvent[] }) => void }> = [];
      reportMock.mockImplementation(async (selectedMonth) => {
        if (selectedMonth === "2026-08") return { month: selectedMonth, events: [] };
        return await new Promise((resolve) => pending.push({ month: selectedMonth, resolve }));
      });
      createMock.mockResolvedValue(event({ id: 9 }));
      render(<CashFlowPage />);
      await screen.findByText("Loading recorded monthly expense evidence…");
      // 3 from Recorded Expense Coverage's fixed window + 6 from Cash Flow
      // Trend's default 6-month window (both fetch against the same
      // earlyBaseline account, and the overlap is accepted by design).
      await waitFor(() => expect(pending.length).toBe(9));
      fireEvent.click(screen.getByRole("button", { name: "Add income" }));
      fireEvent.change(screen.getByLabelText("Cash flow amount"), { target: { value: "1" } });
      fireEvent.change(screen.getByLabelText("Cash flow category"), { target: { value: "Test" } });
      fireEvent.click(screen.getByRole("button", { name: "Save income" }));
      await waitFor(() => expect(accountsCall).toBe(2));
      await waitFor(() => expect(pending.length).toBe(18));
      // Resolve the NEWER generation first, then let the stale one land last.
      // Without a generation guard the stale response would win by arriving
      // last, so this ordering is what actually discriminates.
      const [staleGeneration, newGeneration] = [pending.slice(0, 9), pending.slice(9)];
      newGeneration.forEach((p) => p.resolve({ month: p.month, events: [] }));
      await waitFor(() => expect(screen.getByText(/฿9,000\.00/)).toBeInTheDocument());
      staleGeneration.forEach((p) => p.resolve({ month: p.month, events: [] }));
      await waitFor(() => expect(screen.getByText(/฿9,000\.00/)).toBeInTheDocument());
      expect(screen.queryByText(/฿1,000\.00/)).not.toBeInTheDocument();
    });

    it("re-fetches account evidence when retrying after the account request failed", async () => {
      // A retry that only re-ran loadCoverage would recompute the same stale
      // failure without ever asking for the evidence that was missing.
      let accountsCall = 0;
      accountsMock.mockImplementation(async () => {
        accountsCall += 1;
        if (accountsCall === 1) throw new Error("accounts offline");
        return [account({ balance: 9000, baseline: earlyBaseline })];
      });
      reportForMonths({ "2026-05": [], "2026-06": [], "2026-07": [] });
      render(<CashFlowPage />);
      const coverageSection = (await screen.findByText("Recorded expense coverage is unavailable right now.")).closest("section")!;
      fireEvent.click(within(coverageSection).getByRole("button", { name: "Try again" }));
      await waitFor(() => expect(accountsCall).toBe(2));
      await waitFor(() =>
        expect(within(coverageSection).getByText(/No recorded expenses in the recorded months/)).toBeInTheDocument(),
      );
    });

    it("still discloses untracked accounts when there is not enough recorded history", async () => {
      // A ฿0.00 tracked cash balance with no recorded months is precisely the
      // figure that must not appear unexplained.
      accountsMock.mockResolvedValue([
        account({ id: 1, name: "Untracked A", balance: 4000, baseline: null }),
        account({ id: 2, name: "Untracked B", balance: 5000, baseline: null }),
      ]);
      render(<CashFlowPage />);
      expect(await screen.findByText("Not enough recorded history yet to calculate recorded expense coverage.")).toBeInTheDocument();
      expect(screen.getByText("2 active cash accounts are not tracked and are not included.")).toBeInTheDocument();
      expect(screen.getByText("Amounts designated toward goals are not deducted here.")).toBeInTheDocument();
    });

    it("does not introduce a duplicate cash-accounts fetch", async () => {
      accountsMock.mockResolvedValue([account({ balance: 9000, baseline: earlyBaseline })]);
      reportForMonths({ "2026-05": [], "2026-06": [], "2026-07": [] });
      render(<CashFlowPage />);
      await screen.findByText(/No recorded expenses in the recorded months/);
      expect(accountsMock).toHaveBeenCalledTimes(1);
    });

    it("never uses prohibited terminology", async () => {
      accountsMock.mockResolvedValue([account({ balance: 42000, baseline: earlyBaseline })]);
      reportForMonths({
        "2026-05": [event({ id: 1, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-05-01" })],
        "2026-06": [event({ id: 2, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-06-01" })],
        "2026-07": [event({ id: 3, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-07-01" })],
      });
      render(<CashFlowPage />);
      await screen.findByText(/Tracked cash covers 4\.2 months/);
      const bodyText = document.body.textContent ?? "";
      for (const banned of ["observed", "eligible", "liquid fund", "safe", "should", "fully tracked", "complete evidence", "complete expense history"]) {
        expect(bodyText.toLowerCase()).not.toContain(banned);
      }
    });

    describe("Coverage target", () => {
      function availableCoverageFixture() {
        accountsMock.mockResolvedValue([account({ balance: 42000, baseline: earlyBaseline })]);
        reportForMonths({
          "2026-05": [event({ id: 1, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-05-01" })],
          "2026-06": [event({ id: 2, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-06-01" })],
          "2026-07": [event({ id: 3, transaction_type: "EXPENSE", amount: 10000, signed_amount: -10000, occurred_on: "2026-07-01" })],
        });
      }

      it("shows no saved target and an option to set one, with no gap shown", async () => {
        availableCoverageFixture();
        getSettingsMock.mockResolvedValue({ target_coverage_months: null });
        render(<CashFlowPage />);
        await screen.findByText(/Tracked cash covers 4\.2 months/);
        expect(await screen.findByText("No target set.")).toBeInTheDocument();
        expect(screen.getByRole("button", { name: "Set target" })).toBeInTheDocument();
        expect(screen.queryByText(/more tracked cash would reach your target/)).not.toBeInTheDocument();
        expect(screen.queryByText(/above your target/)).not.toBeInTheDocument();
      });

      it("shows the saved target and derived gap when coverage is AVAILABLE", async () => {
        availableCoverageFixture();
        getSettingsMock.mockResolvedValue({ target_coverage_months: 6 });
        render(<CashFlowPage />);
        await screen.findByText(/Tracked cash covers 4\.2 months/);
        expect(await screen.findByText(/Your target: 6 months/)).toBeInTheDocument();
        expect(screen.getByText(/more tracked cash would reach your target/)).toBeInTheDocument();
      });

      it("sets a target: saves through the API and confirms it in the UI", async () => {
        availableCoverageFixture();
        getSettingsMock.mockResolvedValue({ target_coverage_months: null });
        updateSettingsMock.mockResolvedValue({ target_coverage_months: 6 });
        render(<CashFlowPage />);
        await screen.findByText("No target set.");
        fireEvent.click(screen.getByRole("button", { name: "Set target" }));
        fireEvent.change(screen.getByLabelText("Target coverage months"), { target: { value: "6" } });
        fireEvent.click(screen.getByRole("button", { name: "Save" }));
        await waitFor(() => expect(updateSettingsMock).toHaveBeenCalledWith({ target_coverage_months: 6 }));
        expect(await screen.findByText(/Your target: 6 months/)).toBeInTheDocument();
      });

      it("clears a saved target: calls the API with null and removes the gap", async () => {
        availableCoverageFixture();
        getSettingsMock.mockResolvedValue({ target_coverage_months: 6 });
        updateSettingsMock.mockResolvedValue({ target_coverage_months: null });
        render(<CashFlowPage />);
        await screen.findByText(/Your target: 6 months/);
        fireEvent.click(screen.getByRole("button", { name: "Clear" }));
        await waitFor(() => expect(updateSettingsMock).toHaveBeenCalledWith({ target_coverage_months: null }));
        expect(await screen.findByText("No target set.")).toBeInTheDocument();
        expect(screen.queryByText(/more tracked cash would reach your target/)).not.toBeInTheDocument();
      });

      it("keeps the last confirmed target and shows an error when clearing fails", async () => {
        availableCoverageFixture();
        getSettingsMock.mockResolvedValue({ target_coverage_months: 6 });
        updateSettingsMock.mockRejectedValue(new Error("clear offline"));
        render(<CashFlowPage />);
        await screen.findByText(/Your target: 6 months/);
        expect(screen.getByText(/more tracked cash would reach your target/)).toBeInTheDocument();
        fireEvent.click(screen.getByRole("button", { name: "Clear" }));
        await waitFor(() => expect(updateSettingsMock).toHaveBeenCalledWith({ target_coverage_months: null }));
        expect(await screen.findByRole("alert")).toHaveTextContent("clear offline");
        expect(screen.getByText(/Your target: 6 months/)).toBeInTheDocument();
        expect(screen.getByText(/more tracked cash would reach your target/)).toBeInTheDocument();
        expect(screen.getByRole("button", { name: "Clear" })).toBeInTheDocument();
      });

      it("keeps the last confirmed target and shows an error when saving fails", async () => {
        availableCoverageFixture();
        getSettingsMock.mockResolvedValue({ target_coverage_months: null });
        updateSettingsMock.mockRejectedValue(new Error("save offline"));
        render(<CashFlowPage />);
        await screen.findByText("No target set.");
        fireEvent.click(screen.getByRole("button", { name: "Set target" }));
        fireEvent.change(screen.getByLabelText("Target coverage months"), { target: { value: "6" } });
        fireEvent.click(screen.getByRole("button", { name: "Save" }));
        expect(await screen.findByRole("alert")).toHaveTextContent("save offline");
        expect(screen.queryByText(/Your target:/)).not.toBeInTheDocument();
        expect(screen.getByLabelText("Target coverage months")).toBeInTheDocument();
      });

      it("shows the saved target but no gap when coverage evidence is not AVAILABLE", async () => {
        accountsMock.mockResolvedValue([account({ balance: 9000, baseline: earlyBaseline })]);
        reportForMonths({ "2026-05": [], "2026-06": [], "2026-07": [] });
        getSettingsMock.mockResolvedValue({ target_coverage_months: 6 });
        render(<CashFlowPage />);
        expect(await screen.findByText(/No recorded expenses in the recorded months/)).toBeInTheDocument();
        expect(await screen.findByText(/Your target: 6 months/)).toBeInTheDocument();
        expect(screen.queryByText(/more tracked cash would reach your target/)).not.toBeInTheDocument();
        expect(screen.queryByText(/above your target/)).not.toBeInTheDocument();
      });
    });
  });

  describe("Cash Flow Trend", () => {
    const earlyBaseline = { id: 1, cash_account_id: 1, effective_on: "2026-01-01", observed_balance: 1000, created_at: "2026-01-01T00:00:00Z" };
    const WINDOW_3M = ["2026-05", "2026-06", "2026-07"];
    const WINDOW_6M = ["2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07"];

    function reportForMonths(byMonth: Record<string, CashFlowEvent[]>) {
      reportMock.mockImplementation(async (selectedMonth) => ({ month: selectedMonth, events: byMonth[selectedMonth] ?? [] }));
    }

    function allZero(months: string[]): Record<string, CashFlowEvent[]> {
      return Object.fromEntries(months.map((month) => [month, []]));
    }

    it("defaults to a 6-month window and reports full availability", async () => {
      accountsMock.mockResolvedValue([account({ baseline: earlyBaseline })]);
      reportForMonths(allZero(WINDOW_6M));
      render(<CashFlowPage />);
      const trendSection = await screen.findByRole("region", { name: "Cash flow trend" });
      expect(await within(trendSection).findByText("6 of 6 months available.")).toBeInTheDocument();
      for (const trendMonth of WINDOW_6M) {
        expect(reportMock.mock.calls.some((call) => call[0] === trendMonth)).toBe(true);
      }
    });

    it("switches to a 3-month window on request and requests exactly those months", async () => {
      accountsMock.mockResolvedValue([account({ baseline: earlyBaseline })]);
      reportForMonths(allZero(WINDOW_6M));
      render(<CashFlowPage />);
      const trendSection = await screen.findByRole("region", { name: "Cash flow trend" });
      await within(trendSection).findByText("6 of 6 months available.");
      fireEvent.click(within(trendSection).getByRole("button", { name: "3M" }));
      expect(await within(trendSection).findByText("3 of 3 months available.")).toBeInTheDocument();
      for (const trendMonth of WINDOW_3M) {
        expect(reportMock.mock.calls.some((call) => call[0] === trendMonth)).toBe(true);
      }
    });

    it("renders a genuine zero month as AVAILABLE, not a gap", async () => {
      accountsMock.mockResolvedValue([account({ baseline: earlyBaseline })]);
      reportForMonths(allZero(WINDOW_6M));
      render(<CashFlowPage />);
      const trendSection = await screen.findByRole("region", { name: "Cash flow trend" });
      expect(await within(trendSection).findByText("6 of 6 months available.")).toBeInTheDocument();
      expect(within(trendSection).queryByText(/before tracking began/)).not.toBeInTheDocument();
      expect(within(trendSection).queryByText(/could not load/)).not.toBeInTheDocument();
    });

    it("renders pre-tracking months as a distinct gap, never as ฿0", async () => {
      const lateBaseline = { id: 1, cash_account_id: 1, effective_on: "2026-06-01", observed_balance: 500, created_at: "2026-06-01T00:00:00Z" };
      accountsMock.mockResolvedValue([account({ baseline: lateBaseline })]);
      reportForMonths(allZero(["2026-06", "2026-07"]));
      render(<CashFlowPage />);
      const trendSection = await screen.findByRole("region", { name: "Cash flow trend" });
      expect(await within(trendSection).findByText("2 of 6 months available.")).toBeInTheDocument();
      expect(within(trendSection).getByText(/4 months before tracking began/)).toBeInTheDocument();
      expect(within(trendSection).queryByText(/could not load/)).not.toBeInTheDocument();
    });

    it("renders a technical fetch failure as a distinct unavailable gap, never as ฿0", async () => {
      accountsMock.mockResolvedValue([account({ baseline: earlyBaseline })]);
      reportMock.mockImplementation(async (selectedMonth) => {
        if (selectedMonth === "2026-04") throw new Error("month offline");
        return { month: selectedMonth, events: [] };
      });
      render(<CashFlowPage />);
      const trendSection = await screen.findByRole("region", { name: "Cash flow trend" });
      expect(await within(trendSection).findByText("5 of 6 months available.")).toBeInTheDocument();
      expect(within(trendSection).getByText(/1 month could not load/)).toBeInTheDocument();
      expect(within(trendSection).queryByText(/before tracking began/)).not.toBeInTheDocument();
    });

    it("shows a consolidated error with retry when every trend month fails", async () => {
      accountsMock.mockResolvedValue([account({ baseline: earlyBaseline })]);
      reportMock.mockImplementation(async (selectedMonth) => {
        if (selectedMonth === "2026-08") return { month: selectedMonth, events: [] };
        throw new Error("month offline");
      });
      render(<CashFlowPage />);
      const trendSection = await screen.findByRole("region", { name: "Cash flow trend" });
      expect(await within(trendSection).findByText("Unable to load Cash Flow Trend.")).toBeInTheDocument();
      expect(within(trendSection).getByRole("button", { name: "Try again" })).toBeInTheDocument();
    });

    it("does not let a stale window-switch response overwrite the newer selection", async () => {
      accountsMock.mockResolvedValue([account({ baseline: earlyBaseline })]);
      const pending: Array<{ month: string; resolve: (value: { month: string; events: CashFlowEvent[] }) => void }> = [];
      reportMock.mockImplementation(async (selectedMonth) => {
        if (selectedMonth === "2026-08") return { month: selectedMonth, events: [] };
        return await new Promise((resolve) => pending.push({ month: selectedMonth, resolve }));
      });
      render(<CashFlowPage />);
      const trendSection = await screen.findByRole("region", { name: "Cash flow trend" });
      await within(trendSection).findByText("Loading Cash Flow Trend…");
      // 3 from Recorded Expense Coverage's fixed window + 6 from Cash Flow
      // Trend's initial default 6-month window (accepted overlap by design).
      await waitFor(() => expect(pending.length).toBe(9));
      fireEvent.click(within(trendSection).getByRole("button", { name: "12M" }));
      fireEvent.click(within(trendSection).getByRole("button", { name: "6M" }));
      await waitFor(() => expect(pending.length).toBeGreaterThan(6));
      const finalGeneration = pending.slice(-6);
      const staleGenerations = pending.slice(0, pending.length - 6);
      finalGeneration.forEach((p) => p.resolve({ month: p.month, events: [] }));
      expect(await within(trendSection).findByText("6 of 6 months available.")).toBeInTheDocument();
      staleGenerations.forEach((p) => p.resolve({ month: p.month, events: [event({ amount: 12345 })] }));
      await waitFor(() => expect(within(trendSection).getByText("6 of 6 months available.")).toBeInTheDocument());
    });
  });

  describe("Cash Entry Templates", () => {
    it("lists templates with type, amount, category, and account", async () => {
      templatesMock.mockResolvedValue([template()]);
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      expect(within(section).getByText("Monthly Salary")).toBeInTheDocument();
      expect(within(section).getByText(/Income · Salary · ฿45,000\.00 · Everyday Cash/)).toBeInTheDocument();
    });

    it("shows an archived-account template as visible but unusable", async () => {
      templatesMock.mockResolvedValue([template({
        cash_account_name: "Old Reserve",
        cash_account_is_archived: true,
      })]);
      // The account itself is archived, so it is absent from listCashAccounts(false)
      // — the template's cash_account_name/is_archived fields are the only source.
      accountsMock.mockResolvedValue([account({ id: 2, name: "Other Active" })]);
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      expect(within(section).getByText(/Old Reserve \(Archived\)/)).toBeInTheDocument();
      const useButton = within(section).getByRole("button", { name: "Account archived" });
      expect(useButton).toBeDisabled();
      expect(within(section).getByRole("button", { name: "Edit" })).toBeInTheDocument();
      expect(within(section).getByRole("button", { name: "Delete" })).toBeInTheDocument();
    });

    it("creates a template through the compact management form", async () => {
      let stored: CashEntryTemplate[] = [];
      templatesMock.mockImplementation(async () => stored);
      createTemplateMock.mockImplementation(async (body) => {
        const created = template({ id: 5, name: body.name, transaction_type: body.transaction_type, amount: body.amount, category: body.category });
        stored = [created];
        return created;
      });
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      fireEvent.click(within(section).getByRole("button", { name: "Add template" }));
      fireEvent.change(within(section).getByLabelText("Template name"), { target: { value: "Rent" } });
      fireEvent.change(within(section).getByLabelText("Template type"), { target: { value: "EXPENSE" } });
      fireEvent.change(within(section).getByLabelText("Template amount"), { target: { value: "15000" } });
      fireEvent.change(within(section).getByLabelText("Template category"), { target: { value: "Housing" } });
      fireEvent.click(within(section).getByRole("button", { name: "Save template" }));
      await waitFor(() => expect(createTemplateMock).toHaveBeenCalledWith(expect.objectContaining({
        name: "Rent", transaction_type: "EXPENSE", amount: 15000, category: "Housing",
      })));
      expect(await within(section).findByText("Rent")).toBeInTheDocument();
    });

    it("edits an existing template", async () => {
      let stored = [template()];
      templatesMock.mockImplementation(async () => stored);
      updateTemplateMock.mockImplementation(async (id, body) => {
        stored = [{ ...stored[0], ...body } as CashEntryTemplate];
        return stored[0];
      });
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      await within(section).findByText("Monthly Salary");
      fireEvent.click(within(section).getByRole("button", { name: "Edit" }));
      const nameInput = within(section).getByLabelText("Template name") as HTMLInputElement;
      expect(nameInput.value).toBe("Monthly Salary");
      fireEvent.change(nameInput, { target: { value: "Salary v2" } });
      fireEvent.click(within(section).getByRole("button", { name: "Save template" }));
      await waitFor(() => expect(updateTemplateMock).toHaveBeenCalledWith(1, expect.objectContaining({ name: "Salary v2" })));
      expect(await within(section).findByText("Salary v2")).toBeInTheDocument();
    });

    it("saves a metadata-only edit for an archived-account template without resending the archived account (CET-01)", async () => {
      let stored = [template({
        cash_account_id: 9, cash_account_name: "Old Reserve", cash_account_is_archived: true,
      })];
      templatesMock.mockImplementation(async () => stored);
      // The archived account is absent from listCashAccounts(false) — same as
      // the "visible but unusable" test above — plus an unrelated active
      // account, to prove the editor never silently substitutes it in.
      accountsMock.mockResolvedValue([account({ id: 2, name: "Other Active" })]);
      updateTemplateMock.mockImplementation(async (id, body) => {
        stored = [{ ...stored[0], ...body } as CashEntryTemplate];
        return stored[0];
      });
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      await within(section).findByText("Monthly Salary");
      fireEvent.click(within(section).getByRole("button", { name: "Edit" }));

      expect(within(section).getByText(/Current account: Old Reserve — Archived/)).toBeInTheDocument();
      const accountSelect = within(section).getByLabelText("Template cash account") as HTMLSelectElement;
      // Defaults to the "keep current" sentinel, never silently to Other Active.
      expect(accountSelect.value).toBe("");

      fireEvent.change(within(section).getByLabelText("Template name"), { target: { value: "Salary v2" } });
      fireEvent.click(within(section).getByRole("button", { name: "Save template" }));

      await waitFor(() => expect(updateTemplateMock).toHaveBeenCalledTimes(1));
      const [, payload] = updateTemplateMock.mock.calls[0];
      expect(payload).toMatchObject({ name: "Salary v2" });
      expect(payload).not.toHaveProperty("cash_account_id");
      expect(await within(section).findByText("Salary v2")).toBeInTheDocument();
      expect(within(section).getByText(/Old Reserve \(Archived\)/)).toBeInTheDocument();
    });

    it("lets the user explicitly repoint an archived-account template to a different active account", async () => {
      let stored = [template({
        cash_account_id: 9, cash_account_name: "Old Reserve", cash_account_is_archived: true,
      })];
      templatesMock.mockImplementation(async () => stored);
      accountsMock.mockResolvedValue([account({ id: 2, name: "Other Active" })]);
      updateTemplateMock.mockImplementation(async (id, body) => {
        stored = [{
          ...stored[0], ...body,
          cash_account_name: body.cash_account_id === 2 ? "Other Active" : stored[0].cash_account_name,
          cash_account_is_archived: body.cash_account_id === 2 ? false : stored[0].cash_account_is_archived,
        } as CashEntryTemplate];
        return stored[0];
      });
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      await within(section).findByText("Monthly Salary");
      fireEvent.click(within(section).getByRole("button", { name: "Edit" }));

      fireEvent.change(within(section).getByLabelText("Template cash account"), { target: { value: "2" } });
      fireEvent.click(within(section).getByRole("button", { name: "Save template" }));

      await waitFor(() => expect(updateTemplateMock).toHaveBeenCalledWith(1, expect.objectContaining({ cash_account_id: 2 })));
      expect(await within(section).findByRole("button", { name: "Use template" })).toBeEnabled();
    });

    it("deletes a template", async () => {
      let stored = [template()];
      templatesMock.mockImplementation(async () => stored);
      deleteTemplateMock.mockImplementation(async (id) => {
        stored = stored.filter((row) => row.id !== id);
        return { deleted: id };
      });
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      await within(section).findByText("Monthly Salary");
      fireEvent.click(within(section).getByRole("button", { name: "Delete" }));
      await waitFor(() => expect(deleteTemplateMock).toHaveBeenCalledWith(1));
      expect(await within(section).findByText(/No templates yet/)).toBeInTheDocument();
    });

    it("prefills the Add income form from an Income template and does not submit until the user explicitly does", async () => {
      accountsMock.mockResolvedValue([account({ id: 1, name: "Everyday Cash" })]);
      templatesMock.mockResolvedValue([template({ cash_account_id: 1, note: "From my job" })]);
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      fireEvent.click(await within(section).findByRole("button", { name: "Use template" }));

      expect(screen.getByRole("heading", { name: "Add income" })).toBeInTheDocument();
      expect((screen.getByLabelText("Cash flow account") as HTMLSelectElement).value).toBe("1");
      expect((screen.getByLabelText("Cash flow amount") as HTMLInputElement).value).toBe("45000");
      expect((screen.getByLabelText("Cash flow category") as HTMLInputElement).value).toBe("Salary");
      expect((screen.getByLabelText("Cash flow note") as HTMLInputElement).value).toBe("From my job");
      // The date is the form's own fresh default, never a value stored on the template.
      expect((screen.getByLabelText("Cash flow date") as HTMLInputElement).value).toBe("2026-08-01");

      // Explicit-submit boundary: opening/prefilling the form must not itself call the ledger endpoint.
      expect(createMock).not.toHaveBeenCalled();

      fireEvent.click(screen.getByRole("button", { name: "Save income" }));
      await waitFor(() => expect(createMock).toHaveBeenCalledTimes(1));
      expect(createMock).toHaveBeenCalledWith(1, expect.objectContaining({
        transaction_type: "INCOME", amount: 45000, category: "Salary", note: "From my job",
      }));
    });

    it("prefills the Add expense form from an Expense template", async () => {
      accountsMock.mockResolvedValue([account({ id: 1, name: "Everyday Cash" })]);
      templatesMock.mockResolvedValue([template({
        transaction_type: "EXPENSE", cash_account_id: 1, name: "Rent", amount: 15000, category: "Housing",
      })]);
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      fireEvent.click(await within(section).findByRole("button", { name: "Use template" }));
      expect(screen.getByRole("heading", { name: "Add expense" })).toBeInTheDocument();
      expect((screen.getByLabelText("Cash flow amount") as HTMLInputElement).value).toBe("15000");
      expect((screen.getByLabelText("Cash flow category") as HTMLInputElement).value).toBe("Housing");
    });

    it("lets the user change prefilled values before submitting", async () => {
      accountsMock.mockResolvedValue([account({ id: 1, name: "Everyday Cash" })]);
      templatesMock.mockResolvedValue([template({ cash_account_id: 1 })]);
      render(<CashFlowPage />);
      const section = await screen.findByRole("region", { name: "Cash entry templates" });
      fireEvent.click(await within(section).findByRole("button", { name: "Use template" }));
      fireEvent.change(screen.getByLabelText("Cash flow amount"), { target: { value: "50000" } });
      fireEvent.change(screen.getByLabelText("Cash flow category"), { target: { value: "Bonus" } });
      fireEvent.change(screen.getByLabelText("Cash flow date"), { target: { value: "2026-08-15" } });
      fireEvent.click(screen.getByRole("button", { name: "Save income" }));
      await waitFor(() => expect(createMock).toHaveBeenCalledWith(1, expect.objectContaining({
        amount: 50000, category: "Bonus", occurred_on: "2026-08-15",
      })));
    });
  });
});
