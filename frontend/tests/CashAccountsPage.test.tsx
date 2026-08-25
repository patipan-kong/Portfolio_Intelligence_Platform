import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import CashAccountsPage from "@/app/cash/page";
import { createCashAccount, listCashAccounts, updateCashAccount } from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createCashAccount: vi.fn(),
  listCashAccounts: vi.fn(),
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
};

const listMock = vi.mocked(listCashAccounts);
const createMock = vi.mocked(createCashAccount);
const updateMock = vi.mocked(updateCashAccount);

describe("CashAccountsPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([]);
    createMock.mockResolvedValue(account);
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
});
