import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import CashAccountsPage from "@/app/cash/page";
import {
  createCashAccount, createCashAccountBaseline, createCashAccountTransaction,
  listCashAccountTransactions, listCashAccounts, reconcileCashAccount, updateCashAccount,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createCashAccount: vi.fn(),
  createCashAccountBaseline: vi.fn(),
  createCashAccountTransaction: vi.fn(),
  listCashAccountTransactions: vi.fn(),
  listCashAccounts: vi.fn(),
  reconcileCashAccount: vi.fn(),
  updateCashAccount: vi.fn(),
}));

const account = {
  id: 1,
  workspace_id: 1,
  name: "Emergency Fund",
  institution: "SCB",
  currency: "THB" as const,
  balance: 1250.5,
  is_archived: false,
  created_at: "2026-08-25T00:00:00",
  updated_at: "2026-08-25T00:00:00",
  baseline: null,
};

const listMock = vi.mocked(listCashAccounts);
const createMock = vi.mocked(createCashAccount);
const baselineMock = vi.mocked(createCashAccountBaseline);
const transactionMock = vi.mocked(createCashAccountTransaction);
const activityMock = vi.mocked(listCashAccountTransactions);
const reconcileMock = vi.mocked(reconcileCashAccount);
const updateMock = vi.mocked(updateCashAccount);

describe("CashAccountsPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([]);
    activityMock.mockResolvedValue([]);
    createMock.mockResolvedValue(account);
    baselineMock.mockResolvedValue({ id: 1, cash_account_id: 1, effective_on: "2026-08-25", observed_balance: 1250.5, created_at: "2026-08-25T00:00:00" });
    transactionMock.mockResolvedValue({ id: 1, workspace_id: 1, cash_account_id: 1, transaction_type: "INCOME", amount: 20, signed_amount: 20, occurred_on: "2026-08-25", category: "Salary", note: null, created_at: "2026-08-25T00:00:00" });
    reconcileMock.mockResolvedValue({ account, adjustment: null });
    updateMock.mockResolvedValue(account);
  });

  it("shows a loading state and fixed THB", () => {
    listMock.mockReturnValue(new Promise(() => {}));
    render(<CashAccountsPage />);
    expect(screen.getByText("Loading cash accounts…")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Currency: THB (fixed for Cash Accounts v1)")).toBeInTheDocument();
  });

  it("shows a clear empty state", async () => {
    render(<CashAccountsPage />);
    expect(await screen.findByText("No active cash accounts yet. Add your first account above.")).toBeInTheDocument();
  });

  it("renders active accounts and creates an explicit THB account", async () => {
    listMock.mockResolvedValue([account]);
    render(<CashAccountsPage />);
    expect(await screen.findByText("Emergency Fund")).toBeInTheDocument();
    expect(screen.getByText("SCB")).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("Account name"), { target: { value: "Daily Cash" } });
    fireEvent.change(screen.getByLabelText("Institution"), { target: { value: "KBank" } });
    fireEvent.change(screen.getByLabelText("Initial balance"), { target: { value: "42" } });
    fireEvent.click(screen.getByRole("button", { name: "Add cash account" }));

    await waitFor(() => expect(createMock).toHaveBeenCalledWith({ name: "Daily Cash", institution: "KBank", currency: "THB", balance: 42 }));
  });

  it("edits metadata, replaces a balance, and archives an account", async () => {
    listMock.mockResolvedValue([account]);
    render(<CashAccountsPage />);
    await screen.findByText("Emergency Fund");

    fireEvent.click(screen.getByRole("button", { name: "Edit" }));
    fireEvent.change(screen.getByLabelText("Edit account name"), { target: { value: "Reserve" } });
    fireEvent.click(screen.getByRole("button", { name: "Save changes" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, { name: "Reserve", institution: "SCB" }));

    fireEvent.click(screen.getByRole("button", { name: "Update balance" }));
    fireEvent.change(screen.getByLabelText("Replacement balance"), { target: { value: "500" } });
    fireEvent.click(screen.getByRole("button", { name: "Save balance" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, { balance: 500 }));

    fireEvent.click(screen.getByRole("button", { name: "Archive" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, { is_archived: true }));
  });

  it("shows archived accounts and restores them", async () => {
    const archived = { ...account, id: 2, name: "Old account", is_archived: true };
    listMock.mockResolvedValue([account, archived]);
    render(<CashAccountsPage />);
    await screen.findByText("Emergency Fund");
    fireEvent.click(screen.getByRole("button", { name: "Show archived" }));
    expect(await screen.findByText("Old account")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Restore" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(2, { is_archived: false }));
  });

  it("keeps client validation and API failures visible", async () => {
    listMock.mockRejectedValue(new Error("offline"));
    render(<CashAccountsPage />);
    expect(await screen.findByText("offline")).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("Account name"), { target: { value: "Cash" } });
    fireEvent.change(screen.getByLabelText("Initial balance"), { target: { value: "-1" } });
    fireEvent.click(screen.getByRole("button", { name: "Add cash account" }));
    expect(await screen.findByText("Enter an account name and a non-negative current balance.")).toBeInTheDocument();
    expect(createMock).not.toHaveBeenCalled();
  });

  it("starts tracking from an explicit observed baseline without claiming earlier history", async () => {
    listMock.mockResolvedValue([account]);
    render(<CashAccountsPage />);
    await screen.findByText("Emergency Fund");
    expect(screen.getByText("Cash Flow tracking has not started")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Start tracking" }));
    expect(screen.getByText(/Earlier cash history is not reconstructed/)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Baseline effective date"), { target: { value: "2026-08-20" } });
    fireEvent.change(screen.getByLabelText("Baseline observed balance"), { target: { value: "1500" } });
    fireEvent.click(screen.getAllByRole("button", { name: "Start tracking" }).find((button) => button.getAttribute("type") === "submit")!);
    await waitFor(() => expect(baselineMock).toHaveBeenCalledWith(1, { effective_on: "2026-08-20", observed_balance: 1500 }));
  });

  it("adds income and expense with required category for a tracked account", async () => {
    const tracked = { ...account, balance: 1500, baseline: { id: 1, cash_account_id: 1, effective_on: "2026-08-20", observed_balance: 1500, created_at: "2026-08-20T00:00:00" } };
    listMock.mockResolvedValue([tracked]);
    render(<CashAccountsPage />);
    await screen.findByText("Cash Flow tracking started 2026-08-20");
    fireEvent.click(screen.getByRole("button", { name: "Add income" }));
    fireEvent.change(screen.getByLabelText("Cash flow amount"), { target: { value: "50" } });
    fireEvent.click(screen.getByRole("button", { name: "Save income" }));
    expect(await screen.findByText("Enter a positive amount, date, and category.")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Cash flow category"), { target: { value: "Salary" } });
    fireEvent.click(screen.getByRole("button", { name: "Save income" }));
    await waitFor(() => expect(transactionMock).toHaveBeenCalledWith(1, expect.objectContaining({ transaction_type: "INCOME", amount: 50, category: "Salary" })));
  });

  it("reconciles a tracked account without presenting it as income or expense", async () => {
    const tracked = { ...account, baseline: { id: 1, cash_account_id: 1, effective_on: "2026-08-20", observed_balance: 1250.5, created_at: "2026-08-20T00:00:00" } };
    listMock.mockResolvedValue([tracked]);
    render(<CashAccountsPage />);
    await screen.findByText("Emergency Fund");
    fireEvent.click(screen.getByRole("button", { name: "Reconcile balance" }));
    expect(screen.getByText("A difference creates an adjustment; it is not recorded as income or expense.")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Observed balance"), { target: { value: "1300" } });
    fireEvent.click(screen.getByRole("button", { name: "Save reconciliation" }));
    await waitFor(() => expect(reconcileMock).toHaveBeenCalledWith(1, expect.objectContaining({ observed_balance: 1300 })));
  });
});
