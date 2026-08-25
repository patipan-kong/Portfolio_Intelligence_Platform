import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import LiabilitiesPage from "@/app/liabilities/page";
import { createLiability, listLiabilities, updateLiability, type Liability } from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createLiability: vi.fn(),
  listLiabilities: vi.fn(),
  updateLiability: vi.fn(),
}));

const liability: Liability = {
  id: 1,
  workspace_id: 1,
  name: "Home Loan",
  liability_type: "MORTGAGE",
  lender: "SCB",
  balance: 2500000,
  currency: "THB",
  note: "Observed manually",
  is_archived: false,
  created_at: "2026-08-25T00:00:00",
  updated_at: "2026-08-25T00:00:00",
};

const listMock = vi.mocked(listLiabilities);
const createMock = vi.mocked(createLiability);
const updateMock = vi.mocked(updateLiability);

describe("LiabilitiesPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([]);
    createMock.mockResolvedValue(liability);
    updateMock.mockResolvedValue(liability);
  });

  it("shows a loading state and fixed THB", () => {
    listMock.mockReturnValue(new Promise(() => {}));
    render(<LiabilitiesPage />);
    expect(screen.getByText("Loading liabilities…")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Currency: THB (fixed for Liability Foundation v1)")).toBeInTheDocument();
  });

  it("shows an empty state after a successful active-only load", async () => {
    render(<LiabilitiesPage />);
    expect(await screen.findByText("No active liabilities yet. Add your first liability above.")).toBeInTheDocument();
    expect(listMock).toHaveBeenCalledWith(false);
    expect(screen.getByText((_, element) => element?.textContent === "Total Outstanding: ฿0.00")).toBeInTheDocument();
  });

  it("renders type and lender and computes Total Outstanding from active rows", async () => {
    const second = { ...liability, id: 2, name: "Card", liability_type: "CREDIT_CARD" as const, lender: "KBank", balance: 12500 };
    listMock.mockResolvedValue([liability, second]);
    render(<LiabilitiesPage />);
    expect(await screen.findByText("Home Loan")).toBeInTheDocument();
    expect(screen.getByText("Mortgage · SCB")).toBeInTheDocument();
    expect(screen.getByText("Credit card · KBank")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Total Outstanding: ฿2,512,500.00")).toBeInTheDocument();
  });

  it("creates a liability with the explicit THB contract", async () => {
    render(<LiabilitiesPage />);
    await screen.findByText("No active liabilities yet. Add your first liability above.");
    fireEvent.change(screen.getByLabelText("Liability name"), { target: { value: "Car loan" } });
    fireEvent.change(screen.getByLabelText("Liability type"), { target: { value: "AUTO_LOAN" } });
    fireEvent.change(screen.getByLabelText("Lender"), { target: { value: "KBank" } });
    fireEvent.change(screen.getByLabelText("Initial balance"), { target: { value: "450000" } });
    fireEvent.change(screen.getByLabelText("Note"), { target: { value: "Current statement" } });
    fireEvent.click(screen.getByRole("button", { name: "Add liability" }));

    await waitFor(() => expect(createMock).toHaveBeenCalledWith({
      name: "Car loan",
      liability_type: "AUTO_LOAN",
      lender: "KBank",
      balance: 450000,
      currency: "THB",
      note: "Current statement",
    }));
  });

  it("edits metadata and replaces the observed balance", async () => {
    listMock.mockResolvedValue([liability]);
    render(<LiabilitiesPage />);
    await screen.findByText("Home Loan");

    fireEvent.click(screen.getByRole("button", { name: "Edit" }));
    fireEvent.change(screen.getByLabelText("Edit liability name"), { target: { value: "Refinanced loan" } });
    fireEvent.change(screen.getByLabelText("Edit liability type"), { target: { value: "PERSONAL_LOAN" } });
    fireEvent.change(screen.getByLabelText("Edit lender"), { target: { value: "SCB Prime" } });
    fireEvent.change(screen.getByLabelText("Edit note"), { target: { value: "Updated" } });
    fireEvent.click(screen.getByRole("button", { name: "Save changes" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, {
      name: "Refinanced loan",
      liability_type: "PERSONAL_LOAN",
      lender: "SCB Prime",
      note: "Updated",
    }));

    fireEvent.click(screen.getByRole("button", { name: "Update balance" }));
    fireEvent.change(screen.getByLabelText("Observed balance"), { target: { value: "2400000" } });
    fireEvent.click(screen.getByRole("button", { name: "Save balance" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, { balance: 2400000 }));
  });

  it("keeps zero-balance active liabilities visible as Paid off", async () => {
    listMock.mockResolvedValue([{ ...liability, balance: 0 }]);
    render(<LiabilitiesPage />);
    expect(await screen.findByText("Paid off")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Total Outstanding: ฿0.00")).toBeInTheDocument();
  });

  it("archives and restores while excluding archived balances from the active total", async () => {
    let current: Liability[] = [liability, { ...liability, id: 2, name: "Archived card", balance: 900, is_archived: true }];
    listMock.mockImplementation(async (includeArchived = false) => includeArchived ? current : current.filter((item) => !item.is_archived));
    updateMock.mockImplementation(async (id, body) => {
      current = current.map((item) => item.id === id ? { ...item, ...body } : item) as Liability[];
      return current.find((item) => item.id === id)!;
    });
    render(<LiabilitiesPage />);
    await screen.findByText("Home Loan");
    expect(screen.queryByText("Archived card")).not.toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Total Outstanding: ฿2,500,000.00")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Archive" }));
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, { is_archived: true }));
    fireEvent.click(screen.getByRole("button", { name: "Show archived" }));
    expect(await screen.findByText("Archived card")).toBeInTheDocument();
    expect(screen.getByText("Home Loan")).toBeInTheDocument();
    expect(screen.getByText((_, element) => element?.textContent === "Total Outstanding: ฿0.00")).toBeInTheDocument();
    fireEvent.click(screen.getAllByRole("button", { name: "Restore" })[0]);
    await waitFor(() => expect(updateMock).toHaveBeenCalledWith(1, { is_archived: false }));
  });

  it("keeps validation and API failures honest", async () => {
    listMock.mockRejectedValue(new Error("liabilities offline"));
    render(<LiabilitiesPage />);
    expect(await screen.findAllByRole("alert")).toEqual(expect.arrayContaining([expect.objectContaining({ textContent: "liabilities offline" })]));
    expect(screen.getByText((_, element) => element?.textContent === "Total Outstanding: Unavailable")).toBeInTheDocument();
    expect(screen.queryByText(/฿0\.00/)).not.toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("Liability name"), { target: { value: "Debt" } });
    fireEvent.change(screen.getByLabelText("Initial balance"), { target: { value: "-1" } });
    fireEvent.click(screen.getByRole("button", { name: "Add liability" }));
    expect(screen.getByText("Enter a liability name and a non-negative observed balance.")).toBeInTheDocument();
    expect(createMock).not.toHaveBeenCalled();
  });

  it("does not introduce Net Worth terminology in the v1 experience", async () => {
    render(<LiabilitiesPage />);
    await screen.findByText("No active liabilities yet. Add your first liability above.");
    expect(screen.queryByText(/Net Worth/i)).not.toBeInTheDocument();
  });
});
