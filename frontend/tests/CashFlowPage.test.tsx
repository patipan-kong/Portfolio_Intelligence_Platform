import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import CashFlowPage from "@/app/cash-flow/page";
import {
  createCashAccountTransaction,
  getCashFlowReport,
  listCashAccounts,
  type CashAccount,
  type CashFlowEvent,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createCashAccountTransaction: vi.fn(),
  getCashFlowReport: vi.fn(),
  listCashAccounts: vi.fn(),
}));

vi.mock("@/lib/cashFlow", async () => {
  const actual = await vi.importActual<typeof import("@/lib/cashFlow")>("@/lib/cashFlow");
  return { ...actual, currentMonthKey: () => "2026-08" };
});

const reportMock = vi.mocked(getCashFlowReport);
const accountsMock = vi.mocked(listCashAccounts);
const createMock = vi.mocked(createCashAccountTransaction);

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

describe("CashFlowPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    accountsMock.mockResolvedValue([account()]);
    setReport();
    createMock.mockResolvedValue(event({ id: 9 }));
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
});
