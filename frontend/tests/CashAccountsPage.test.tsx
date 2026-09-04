import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import CashAccountsPage from "@/app/cash/page";
import {
  createCashAccount, createCashAccountBaseline, createCashAccountTransaction,
  getCashAccountBalanceAsOf, listCashAccountTransactions, listCashAccounts, reconcileCashAccount, updateCashAccount,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createCashAccount: vi.fn(),
  createCashAccountBaseline: vi.fn(),
  createCashAccountTransaction: vi.fn(),
  getCashAccountBalanceAsOf: vi.fn(),
  listCashAccountTransactions: vi.fn(),
  listCashAccounts: vi.fn(),
  reconcileCashAccount: vi.fn(),
  updateCashAccount: vi.fn(),
}));

let mockSearchParams = new URLSearchParams();

// Goal Funding-Source Drill-Through: /cash reads ?account=<id> via
// next/navigation's useSearchParams. Mocked per the existing
// PortfolioPageDecisionLinkage.test.tsx convention for pages that read query
// params outside a real Next router.
vi.mock("next/navigation", () => ({
  useSearchParams: () => mockSearchParams,
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
const asOfMock = vi.mocked(getCashAccountBalanceAsOf);

let scrollIntoViewMock: ReturnType<typeof vi.fn>;

describe("CashAccountsPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    mockSearchParams = new URLSearchParams();
    // jsdom doesn't implement scrollIntoView; stub it so the drill-through
    // reveal effect can call it, and so tests can verify which element (via
    // mock.contexts, i.e. `this`) it actually targeted.
    scrollIntoViewMock = vi.fn();
    window.HTMLElement.prototype.scrollIntoView = scrollIntoViewMock as unknown as typeof window.HTMLElement.prototype.scrollIntoView;
    listMock.mockResolvedValue([]);
    activityMock.mockResolvedValue([]);
    createMock.mockResolvedValue(account);
    baselineMock.mockResolvedValue({ id: 1, cash_account_id: 1, effective_on: "2026-08-25", observed_balance: 1250.5, created_at: "2026-08-25T00:00:00" });
    transactionMock.mockResolvedValue({ id: 1, workspace_id: 1, cash_account_id: 1, transaction_type: "INCOME", amount: 20, signed_amount: 20, occurred_on: "2026-08-25", category: "Salary", note: null, created_at: "2026-08-25T00:00:00" });
    reconcileMock.mockResolvedValue({ account, adjustment: null });
    updateMock.mockResolvedValue(account);
    asOfMock.mockResolvedValue({ cash_account_id: 1, date: "2026-08-25", currency: "THB", balance: 1250.5, available: true, baseline_effective_on: "2026-08-20" });
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

  it("shows transfer legs with directional account-level labels", async () => {
    const tracked = { ...account, baseline: { id: 1, cash_account_id: 1, effective_on: "2026-08-20", observed_balance: 1250.5, created_at: "2026-08-20T00:00:00Z" } };
    listMock.mockResolvedValue([tracked]);
    activityMock.mockResolvedValue([{
      id: 9,
      workspace_id: 1,
      cash_account_id: 1,
      transaction_type: "TRANSFER",
      amount: -100,
      signed_amount: -100,
      occurred_on: "2026-08-25",
      category: null,
      note: null,
      transfer_id: 4,
      transfer_destination_account_name: "Savings B",
      transfer_direction: "OUT",
      created_at: "2026-08-25T00:00:00Z",
    }]);
    render(<CashAccountsPage />);
    expect(await screen.findByText(/Transfer to Savings B/)).toBeInTheDocument();
    expect(screen.getByText(/−฿100.00/)).toBeInTheDocument();
  });

  it("looks up a historical balance for a tracked account", async () => {
    const tracked = { ...account, baseline: { id: 1, cash_account_id: 1, effective_on: "2026-08-20", observed_balance: 1250.5, created_at: "2026-08-20T00:00:00" } };
    listMock.mockResolvedValue([tracked]);
    render(<CashAccountsPage />);
    await screen.findByText("Emergency Fund");

    fireEvent.click(screen.getByRole("button", { name: "Balance on date" }));
    expect(screen.getByText(/never the current balance/)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-25" } });
    fireEvent.click(screen.getByRole("button", { name: "Look up" }));
    await waitFor(() => expect(asOfMock).toHaveBeenCalledWith(1, "2026-08-25"));
    expect(await screen.findByText(/THB as of 2026-08-25/)).toBeInTheDocument();
  });

  it("reports a pre-baseline date as unavailable, never as zero", async () => {
    const tracked = { ...account, baseline: { id: 1, cash_account_id: 1, effective_on: "2026-08-20", observed_balance: 1250.5, created_at: "2026-08-20T00:00:00" } };
    listMock.mockResolvedValue([tracked]);
    asOfMock.mockResolvedValue({ cash_account_id: 1, date: "2026-08-01", currency: "THB", balance: null, available: false, baseline_effective_on: "2026-08-20" });
    render(<CashAccountsPage />);
    await screen.findByText("Emergency Fund");

    fireEvent.click(screen.getByRole("button", { name: "Balance on date" }));
    fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-01" } });
    fireEvent.click(screen.getByRole("button", { name: "Look up" }));
    expect(await screen.findByText(/Unavailable — before tracking began \(2026-08-20\)/)).toBeInTheDocument();
  });

  describe("Goal Funding-Source Drill-Through", () => {
    it("focuses the exact active account requested via ?account=<id> among several, never a different one", async () => {
      mockSearchParams = new URLSearchParams("account=3");
      listMock.mockResolvedValue([account, { ...account, id: 3, name: "Second Account" }]);
      render(<CashAccountsPage />);
      await screen.findByText("Second Account");
      // A requested id might be archived — the initial fetch always includes
      // archived accounts when any id is requested, so the source can still
      // be found regardless of which it turns out to be (Section 21).
      expect(listMock).toHaveBeenCalledWith(true);
      expect(screen.queryByText("The requested cash account could not be found.")).not.toBeInTheDocument();
      const target = screen.getByText("Second Account").closest('[tabindex="-1"]');
      const other = screen.getByText("Emergency Fund").closest('[tabindex="-1"]');
      expect(target).not.toBeNull();
      expect(other).not.toBeNull();
      await waitFor(() => expect(document.activeElement).toBe(target));
      expect(document.activeElement).not.toBe(other);
      expect(target).toHaveAttribute("tabindex", "-1");
      expect(scrollIntoViewMock.mock.contexts[0]).toBe(target);
    });

    it("reveals an archived account requested via ?account=<id>, auto-expanding the archived section without restoring or repointing it", async () => {
      const archived = { ...account, id: 2, name: "Old Reserve", is_archived: true };
      mockSearchParams = new URLSearchParams(`account=${archived.id}`);
      listMock.mockResolvedValue([account, archived]);
      render(<CashAccountsPage />);
      // A requested archived account is fetched with archived included from
      // the first request — never a transient false "not found" while an
      // active-only fetch is in flight (Section 21).
      await waitFor(() => expect(listMock).toHaveBeenCalledWith(true));
      expect(await screen.findByText("Old Reserve")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Hide archived" })).toBeInTheDocument();
      expect(screen.queryByText("The requested cash account could not be found.")).not.toBeInTheDocument();
      expect(updateMock).not.toHaveBeenCalled();
      const target = screen.getByText("Old Reserve").closest('[tabindex="-1"]');
      expect(target).not.toBeNull();
      await waitFor(() => expect(document.activeElement).toBe(target));
      expect(scrollIntoViewMock.mock.contexts[0]).toBe(target);
    });

    it("fails closed for an unknown account id without representing an existing account as the requested source", async () => {
      mockSearchParams = new URLSearchParams("account=999");
      listMock.mockResolvedValue([account, { ...account, id: 3, name: "Second Account" }]);
      render(<CashAccountsPage />);
      await screen.findByText("Emergency Fund");
      expect(await screen.findByText("The requested cash account could not be found.")).toBeInTheDocument();
      expect(scrollIntoViewMock).not.toHaveBeenCalled();
      expect(document.activeElement).not.toBe(screen.getByText("Emergency Fund").closest('[tabindex="-1"]'));
    });

    it("fails closed for a malformed account id", async () => {
      mockSearchParams = new URLSearchParams("account=abc");
      listMock.mockResolvedValue([account]);
      render(<CashAccountsPage />);
      expect(await screen.findByText("The requested cash account could not be found.")).toBeInTheDocument();
      expect(scrollIntoViewMock).not.toHaveBeenCalled();
      expect(document.activeElement).not.toBe(screen.getByText("Emergency Fund").closest('[tabindex="-1"]'));
    });

    it("preserves ordinary default behavior with no account param", async () => {
      listMock.mockResolvedValue([account]);
      render(<CashAccountsPage />);
      await screen.findByText("Emergency Fund");
      expect(listMock).toHaveBeenCalledWith(false);
      expect(screen.queryByText("The requested cash account could not be found.")).not.toBeInTheDocument();
      expect(scrollIntoViewMock).not.toHaveBeenCalled();
    });

    it("resolves the requested source only once the async account load completes, not before", async () => {
      mockSearchParams = new URLSearchParams("account=3");
      let resolveList!: (value: (typeof account)[]) => void;
      listMock.mockReturnValue(new Promise((resolve) => { resolveList = resolve; }));
      render(<CashAccountsPage />);
      expect(screen.getByText("Loading cash accounts…")).toBeInTheDocument();
      expect(scrollIntoViewMock).not.toHaveBeenCalled();

      await act(async () => resolveList([account, { ...account, id: 3, name: "Second Account" }]));

      await waitFor(() => expect(scrollIntoViewMock).toHaveBeenCalledTimes(1));
      expect(document.activeElement).toBe(screen.getByText("Second Account").closest('[tabindex="-1"]'));
    });

    it("loads archived-capable data when an already mounted no-query page receives an archived query", async () => {
      const archived = { ...account, id: 2, name: "Old Reserve", is_archived: true };
      listMock.mockImplementation(async (includeArchived) => includeArchived ? [account, archived] : [account]);
      const view = render(<CashAccountsPage />);
      await screen.findByText("Emergency Fund");
      expect(listMock).toHaveBeenLastCalledWith(false);

      mockSearchParams = new URLSearchParams("account=2");
      view.rerender(<CashAccountsPage />);

      expect(await screen.findByText("Old Reserve")).toBeInTheDocument();
      expect(listMock).toHaveBeenLastCalledWith(true);
      expect(screen.queryByText("The requested cash account could not be found.")).not.toBeInTheDocument();
      expect(document.activeElement).toBe(screen.getByText("Old Reserve").closest('[tabindex="-1"]'));
    });

    it("restores ordinary archived-section behavior when an archived source query is removed in place", async () => {
      const archived = { ...account, id: 2, name: "Old Reserve", is_archived: true };
      listMock.mockImplementation(async (includeArchived) => includeArchived ? [account, archived] : [account]);
      mockSearchParams = new URLSearchParams("account=2");
      const view = render(<CashAccountsPage />);
      expect(await screen.findByText("Old Reserve")).toBeInTheDocument();
      expect(document.activeElement).toBe(screen.getByText("Old Reserve").closest('[tabindex="-1"]'));

      mockSearchParams = new URLSearchParams();
      view.rerender(<CashAccountsPage />);

      await screen.findByText("Emergency Fund");
      expect(listMock).toHaveBeenLastCalledWith(false);
      expect(screen.getByRole("button", { name: "Show archived" })).toBeInTheDocument();
      expect(screen.queryByText("Archived accounts")).not.toBeInTheDocument();
      expect(screen.queryByText("No archived cash accounts.")).not.toBeInTheDocument();
      expect(screen.queryByText("The requested cash account could not be found.")).not.toBeInTheDocument();
      expect(screen.getByText("Emergency Fund").closest('[tabindex="-1"]')).not.toHaveClass("ring-2");
      expect(document.activeElement).not.toBe(screen.getByText("Emergency Fund").closest('[tabindex="-1"]'));
    });

    it("clears stale resolution state and resolves the latest query across archived, active, and unknown transitions", async () => {
      const archived = { ...account, id: 2, name: "Old Reserve", is_archived: true };
      const active = { ...account, id: 3, name: "Daily Cash" };
      listMock.mockResolvedValue([active, archived]);
      mockSearchParams = new URLSearchParams("account=2");
      const view = render(<CashAccountsPage />);
      expect(await screen.findByText("Old Reserve")).toBeInTheDocument();
      expect(document.activeElement).toBe(screen.getByText("Old Reserve").closest('[tabindex="-1"]'));

      mockSearchParams = new URLSearchParams("account=3");
      view.rerender(<CashAccountsPage />);
      await waitFor(() => expect(document.activeElement).toBe(screen.getByText("Daily Cash").closest('[tabindex="-1"]')));
      expect(screen.queryByText("The requested cash account could not be found.")).not.toBeInTheDocument();

      mockSearchParams = new URLSearchParams("account=999");
      view.rerender(<CashAccountsPage />);
      expect(await screen.findByText("The requested cash account could not be found.")).toBeInTheDocument();
      expect(screen.getByText("Daily Cash").closest('[tabindex="-1"]')).not.toHaveClass("ring-2");

      mockSearchParams = new URLSearchParams("account=3");
      view.rerender(<CashAccountsPage />);
      await waitFor(() => expect(document.activeElement).toBe(screen.getByText("Daily Cash").closest('[tabindex="-1"]')));
      expect(screen.queryByText("The requested cash account could not be found.")).not.toBeInTheDocument();
    });

    it("keeps the latest query intent when an earlier archived-capable load resolves late", async () => {
      const first = { ...account, id: 2, name: "First Account" };
      const latest = { ...account, id: 3, name: "Latest Account", is_archived: true };
      let resolveFirst!: (value: (typeof account)[]) => void;
      let resolveLatest!: (value: (typeof account)[]) => void;
      listMock.mockImplementationOnce(() => new Promise((resolve) => { resolveFirst = resolve; }))
        .mockImplementationOnce(() => new Promise((resolve) => { resolveLatest = resolve; }));
      mockSearchParams = new URLSearchParams("account=2");
      const view = render(<CashAccountsPage />);

      mockSearchParams = new URLSearchParams("account=3");
      view.rerender(<CashAccountsPage />);
      await act(async () => resolveLatest([account, latest]));
      expect(await screen.findByText("Latest Account")).toBeInTheDocument();
      expect(document.activeElement).toBe(screen.getByText("Latest Account").closest('[tabindex="-1"]'));

      await act(async () => resolveFirst([account, first]));
      expect(document.activeElement).toBe(screen.getByText("Latest Account").closest('[tabindex="-1"]'));
      expect(screen.queryByText("First Account")).not.toBeInTheDocument();
      expect(screen.queryByText("The requested cash account could not be found.")).not.toBeInTheDocument();
    });
  });
});
