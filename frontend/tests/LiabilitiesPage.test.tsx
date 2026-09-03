import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import LiabilitiesPage from "@/app/liabilities/page";
import {
  createLiability,
  createLiabilityBalanceObservation,
  getLiabilityBalanceAsOf,
  listLiabilities,
  listLiabilityBalanceObservations,
  updateLiability,
  type Liability,
  type LiabilityBalanceAsOf,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createLiability: vi.fn(),
  createLiabilityBalanceObservation: vi.fn(),
  getLiabilityBalanceAsOf: vi.fn(),
  listLiabilities: vi.fn(),
  listLiabilityBalanceObservations: vi.fn(),
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
const recordMock = vi.mocked(createLiabilityBalanceObservation);
const historyMock = vi.mocked(listLiabilityBalanceObservations);
const asOfMock = vi.mocked(getLiabilityBalanceAsOf);

describe("LiabilitiesPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([]);
    createMock.mockResolvedValue(liability);
    updateMock.mockResolvedValue(liability);
    recordMock.mockResolvedValue({ id: 1, workspace_id: 1, liability_id: 1, balance: 2500000, observed_on: "2026-08-25", created_at: "2026-08-25T00:00:00" });
    historyMock.mockResolvedValue([]);
    asOfMock.mockResolvedValue({ liability_id: 1, date: "2026-08-10", currency: "THB", balance: null, available: false });
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

  it("records a dated balance observation and shows tracking status, never payment/Net Worth terms", async () => {
    let current: Liability[] = [liability];
    listMock.mockImplementation(async () => current);
    recordMock.mockImplementation(async (id, body) => {
      current = current.map((item) => item.id === id ? { ...item, first_observation_on: body.observed_on, balance: body.balance } : item) as Liability[];
      return { id: 1, workspace_id: 1, liability_id: id, balance: body.balance, observed_on: body.observed_on, created_at: "2026-08-25T00:00:00" };
    });
    render(<LiabilitiesPage />);
    await screen.findByText("Home Loan");
    expect(screen.getByText("No balance history recorded yet")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Record balance" }));
    expect(screen.queryByText(/amortization|APR|payoff schedule/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Net Worth/i)).not.toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Observed date"), { target: { value: "2026-08-10" } });
    fireEvent.change(screen.getByLabelText("Observed balance on date"), { target: { value: "2450000" } });
    fireEvent.click(screen.getAllByRole("button", { name: "Record balance" }).find((button) => button.getAttribute("type") === "submit")!);

    await waitFor(() => expect(recordMock).toHaveBeenCalledWith(1, { balance: 2450000, observed_on: "2026-08-10" }));
    expect(await screen.findByText("History tracking started 2026-08-10")).toBeInTheDocument();
  });

  it("surfaces a failed balance recording without silently succeeding", async () => {
    listMock.mockResolvedValue([liability]);
    recordMock.mockRejectedValue(new Error("observation rejected"));
    render(<LiabilitiesPage />);
    await screen.findByText("Home Loan");

    fireEvent.click(screen.getByRole("button", { name: "Record balance" }));
    fireEvent.change(screen.getByLabelText("Observed date"), { target: { value: "2026-08-10" } });
    fireEvent.change(screen.getByLabelText("Observed balance on date"), { target: { value: "2450000" } });
    fireEvent.click(screen.getAllByRole("button", { name: "Record balance" }).find((button) => button.getAttribute("type") === "submit")!);

    expect(await screen.findByText("observation rejected")).toBeInTheDocument();
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

  describe("Balance history", () => {
    it("opens and displays fetched observations", async () => {
      listMock.mockResolvedValue([liability]);
      historyMock.mockResolvedValue([
        { id: 2, workspace_id: 1, liability_id: 1, balance: 2400000, observed_on: "2026-08-20", created_at: "2026-08-20T00:00:00" },
        { id: 1, workspace_id: 1, liability_id: 1, balance: 2500000, observed_on: "2026-08-01", created_at: "2026-08-01T00:00:00" },
      ]);
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance history" }));

      expect(await screen.findByText("Balance history — Home Loan")).toBeInTheDocument();
      expect(historyMock).toHaveBeenCalledWith(1);
      expect(screen.getByText("Observed on 2026-08-20")).toBeInTheDocument();
      expect(screen.getByText("Observed on 2026-08-01")).toBeInTheDocument();
    });

    it("renders multiple observations with correct dates and balances", async () => {
      listMock.mockResolvedValue([liability]);
      historyMock.mockResolvedValue([
        { id: 3, workspace_id: 1, liability_id: 1, balance: 2300000, observed_on: "2026-08-25", created_at: "2026-08-25T00:00:00" },
        { id: 2, workspace_id: 1, liability_id: 1, balance: 2400000, observed_on: "2026-08-10", created_at: "2026-08-10T00:00:00" },
        { id: 1, workspace_id: 1, liability_id: 1, balance: 2500000, observed_on: "2026-08-01", created_at: "2026-08-01T00:00:00" },
      ]);
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance history" }));

      const rows = await screen.findAllByRole("listitem");
      expect(rows.map((row) => row.textContent)).toEqual([
        expect.stringContaining("2026-08-25"),
        expect.stringContaining("2026-08-10"),
        expect.stringContaining("2026-08-01"),
      ]);
      expect(screen.getByText((_, el) => el?.textContent === "฿2,300,000.00")).toBeInTheDocument();
    });

    it("preserves the API's newest-first ordering without re-sorting", async () => {
      listMock.mockResolvedValue([liability]);
      historyMock.mockResolvedValue([
        { id: 2, workspace_id: 1, liability_id: 1, balance: 900, observed_on: "2026-08-20", created_at: "2026-08-20T00:00:00" },
        { id: 1, workspace_id: 1, liability_id: 1, balance: 1000, observed_on: "2026-08-01", created_at: "2026-08-01T00:00:00" },
      ]);
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance history" }));

      const rows = await screen.findAllByRole("listitem");
      expect(rows[0].textContent).toContain("2026-08-20");
      expect(rows[1].textContent).toContain("2026-08-01");
    });

    it("shows a factual empty state with no history", async () => {
      listMock.mockResolvedValue([liability]);
      historyMock.mockResolvedValue([]);
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance history" }));

      expect(await screen.findByText("No recorded balance observations yet.")).toBeInTheDocument();
    });

    it("shows a fetch error without fabricating balances", async () => {
      listMock.mockResolvedValue([liability]);
      historyMock.mockRejectedValue(new Error("history offline"));
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance history" }));

      expect(await screen.findByText("history offline")).toBeInTheDocument();
      expect(screen.queryByText(/฿0\.00/)).not.toBeInTheDocument();
    });

    it("never labels observations as payments or repayments", async () => {
      listMock.mockResolvedValue([liability]);
      historyMock.mockResolvedValue([
        { id: 1, workspace_id: 1, liability_id: 1, balance: 2400000, observed_on: "2026-08-20", created_at: "2026-08-20T00:00:00" },
      ]);
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance history" }));
      const panel = (await screen.findByText("Balance history — Home Loan")).closest("div")!.parentElement as HTMLElement;

      expect(within(panel).queryByText(/payments?/i)).not.toBeInTheDocument();
      expect(within(panel).queryByText(/repayments?/i)).not.toBeInTheDocument();
    });

    it("refreshes visible history after recording a new observation", async () => {
      listMock.mockResolvedValue([liability]);
      historyMock.mockResolvedValueOnce([
        { id: 1, workspace_id: 1, liability_id: 1, balance: 2500000, observed_on: "2026-08-01", created_at: "2026-08-01T00:00:00" },
      ]);
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");
      fireEvent.click(screen.getByRole("button", { name: "Balance history" }));
      await screen.findByText("Observed on 2026-08-01");

      historyMock.mockResolvedValueOnce([
        { id: 2, workspace_id: 1, liability_id: 1, balance: 2400000, observed_on: "2026-08-15", created_at: "2026-08-15T00:00:00" },
        { id: 1, workspace_id: 1, liability_id: 1, balance: 2500000, observed_on: "2026-08-01", created_at: "2026-08-01T00:00:00" },
      ]);
      fireEvent.click(screen.getByRole("button", { name: "Record balance" }));
      fireEvent.change(screen.getByLabelText("Observed date"), { target: { value: "2026-08-15" } });
      fireEvent.change(screen.getByLabelText("Observed balance on date"), { target: { value: "2400000" } });
      fireEvent.click(screen.getAllByRole("button", { name: "Record balance" }).find((button) => button.getAttribute("type") === "submit")!);

      expect(await screen.findByText("Observed on 2026-08-15")).toBeInTheDocument();
      expect(historyMock).toHaveBeenCalledTimes(2);
    });

    it("does not leak observations between liabilities", async () => {
      const second = { ...liability, id: 2, name: "Card" };
      listMock.mockResolvedValue([liability, second]);
      historyMock.mockImplementation(async (id) =>
        id === 1
          ? [{ id: 10, workspace_id: 1, liability_id: 1, balance: 100, observed_on: "2026-08-01", created_at: "2026-08-01T00:00:00" }]
          : [{ id: 20, workspace_id: 1, liability_id: 2, balance: 200, observed_on: "2026-08-05", created_at: "2026-08-05T00:00:00" }]
      );
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getAllByRole("button", { name: "Balance history" })[0]);
      expect(await screen.findByText("Balance history — Home Loan")).toBeInTheDocument();
      expect(screen.getByText("Observed on 2026-08-01")).toBeInTheDocument();

      fireEvent.click(screen.getAllByRole("button", { name: "Balance history" })[1]);
      expect(await screen.findByText("Balance history — Card")).toBeInTheDocument();
      expect(screen.getByText("Observed on 2026-08-05")).toBeInTheDocument();
      expect(screen.queryByText("Observed on 2026-08-01")).not.toBeInTheDocument();
    });
  });

  describe("Historical as-of lookup", () => {
    it("sends the exact selected date to the as-of API helper", async () => {
      listMock.mockResolvedValue([liability]);
      asOfMock.mockResolvedValue({ liability_id: 1, date: "2026-08-10", currency: "THB", balance: 2400000, available: true });
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance on date" }));
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-10" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));

      await waitFor(() => expect(asOfMock).toHaveBeenCalledWith(1, "2026-08-10"));
    });

    it("renders an available historical balance", async () => {
      listMock.mockResolvedValue([liability]);
      asOfMock.mockResolvedValue({ liability_id: 1, date: "2026-08-10", currency: "THB", balance: 2400000, available: true });
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance on date" }));
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-10" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));

      expect(await screen.findByText((_, el) => el?.textContent === "฿2,400,000.00")).toBeInTheDocument();
      expect(screen.getByText(/THB as of 2026-08-10/)).toBeInTheDocument();
    });

    it("shows unavailable state rather than zero when evidence is missing", async () => {
      listMock.mockResolvedValue([liability]);
      asOfMock.mockResolvedValue({ liability_id: 1, date: "2026-07-01", currency: "THB", balance: null, available: false });
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance on date" }));
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-07-01" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));

      expect(await screen.findByText("No recorded liability balance is available for this date.")).toBeInTheDocument();
      expect(screen.queryByText(/฿0\.00/)).not.toBeInTheDocument();
    });

    it("updates the displayed result when a second lookup uses a different date", async () => {
      listMock.mockResolvedValue([liability]);
      asOfMock.mockResolvedValueOnce({ liability_id: 1, date: "2026-08-01", currency: "THB", balance: 2500000, available: true });
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance on date" }));
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-01" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));
      expect(await screen.findByText((_, el) => el?.textContent === "฿2,500,000.00")).toBeInTheDocument();

      asOfMock.mockResolvedValueOnce({ liability_id: 1, date: "2026-08-20", currency: "THB", balance: 2300000, available: true });
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-20" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));

      expect(await screen.findByText((_, el) => el?.textContent === "฿2,300,000.00")).toBeInTheDocument();
      expect(screen.queryByText(/THB as of 2026-08-01/)).not.toBeInTheDocument();
      expect(screen.getByText(/THB as of 2026-08-20/)).toBeInTheDocument();
    });

    it("distinguishes a fetch error from unavailable evidence", async () => {
      listMock.mockResolvedValue([liability]);
      asOfMock.mockRejectedValue(new Error("as-of offline"));
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance on date" }));
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-10" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));

      expect(await screen.findByText("as-of offline")).toBeInTheDocument();
      expect(screen.queryByText("No recorded liability balance is available for this date.")).not.toBeInTheDocument();
    });

    it("does not leak an as-of result across different liabilities", async () => {
      const second = { ...liability, id: 2, name: "Card" };
      listMock.mockResolvedValue([liability, second]);
      asOfMock.mockResolvedValueOnce({ liability_id: 1, date: "2026-08-10", currency: "THB", balance: 2400000, available: true });
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getAllByRole("button", { name: "Balance on date" })[0]);
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-10" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));
      await screen.findByText((_, el) => el?.textContent === "฿2,400,000.00");

      fireEvent.click(screen.getAllByRole("button", { name: "Balance on date" })[1]);
      expect(screen.getByText("Historical balance — Card")).toBeInTheDocument();
      expect(screen.queryByText((_, el) => el?.textContent === "฿2,400,000.00")).not.toBeInTheDocument();
    });

    it("discards a deferred as-of response for liability A after switching to liability B (LHR-1)", async () => {
      const second = { ...liability, id: 2, name: "Card" };
      listMock.mockResolvedValue([liability, second]);
      let resolveA!: (value: LiabilityBalanceAsOf) => void;
      const pendingA = new Promise<LiabilityBalanceAsOf>((resolve) => { resolveA = resolve; });
      asOfMock.mockReturnValueOnce(pendingA);
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getAllByRole("button", { name: "Balance on date" })[0]);
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-10" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));
      expect(await screen.findByText("Looking up…")).toBeInTheDocument();

      fireEvent.click(screen.getAllByRole("button", { name: "Balance on date" })[1]);
      expect(screen.getByText("Historical balance — Card")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Look up" })).toBeInTheDocument();

      resolveA({ liability_id: 1, date: "2026-08-10", currency: "THB", balance: 2400000, available: true });
      await Promise.resolve();
      await Promise.resolve();

      expect(screen.queryByText((_, el) => el?.textContent === "฿2,400,000.00")).not.toBeInTheDocument();
      expect(screen.getByText("Historical balance — Card")).toBeInTheDocument();
      expect(screen.queryByText("Looking up…")).not.toBeInTheDocument();
    });

    it("discards a stale earlier-date response after a newer date lookup resolves first (LHR-1)", async () => {
      listMock.mockResolvedValue([liability]);
      let resolveFirst!: (value: LiabilityBalanceAsOf) => void;
      const pendingFirst = new Promise<LiabilityBalanceAsOf>((resolve) => { resolveFirst = resolve; });
      asOfMock.mockReturnValueOnce(pendingFirst);
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance on date" }));
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-01" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));

      asOfMock.mockResolvedValueOnce({ liability_id: 1, date: "2026-08-20", currency: "THB", balance: 2300000, available: true });
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-20" } });
      fireEvent.click(screen.getByRole("button", { name: /Look up|Looking up/ }));
      expect(await screen.findByText((_, el) => el?.textContent === "฿2,300,000.00")).toBeInTheDocument();

      resolveFirst({ liability_id: 1, date: "2026-08-01", currency: "THB", balance: 2500000, available: true });
      await Promise.resolve();
      await Promise.resolve();

      expect(screen.getByText((_, el) => el?.textContent === "฿2,300,000.00")).toBeInTheDocument();
      expect(screen.queryByText(/THB as of 2026-08-01/)).not.toBeInTheDocument();
    });

    it("does not repopulate a closed as-of panel with a late-arriving response (LHR-1)", async () => {
      listMock.mockResolvedValue([liability]);
      let resolvePending!: (value: LiabilityBalanceAsOf) => void;
      const pending = new Promise<LiabilityBalanceAsOf>((resolve) => { resolvePending = resolve; });
      asOfMock.mockReturnValueOnce(pending);
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");

      fireEvent.click(screen.getByRole("button", { name: "Balance on date" }));
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-10" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));
      fireEvent.click(screen.getByRole("button", { name: "Cancel" }));
      expect(screen.queryByText("Historical balance — Home Loan")).not.toBeInTheDocument();

      resolvePending({ liability_id: 1, date: "2026-08-10", currency: "THB", balance: 2400000, available: true });
      await Promise.resolve();
      await Promise.resolve();

      expect(screen.queryByText("Historical balance — Home Loan")).not.toBeInTheDocument();
      expect(screen.queryByText((_, el) => el?.textContent === "฿2,400,000.00")).not.toBeInTheDocument();
    });
  });

  describe("Archived liability read-only access (LHR-2)", () => {
    async function renderWithArchived() {
      const archivedItem = { ...liability, id: 2, name: "Archived Card", is_archived: true, balance: 900 };
      listMock.mockImplementation(async (includeArchived = false) =>
        includeArchived ? [liability, archivedItem] : [liability]
      );
      render(<LiabilitiesPage />);
      await screen.findByText("Home Loan");
      fireEvent.click(screen.getByRole("button", { name: "Show archived" }));
      await screen.findByText("Archived Card");
      return archivedItem;
    }

    it("exposes Balance history for a visible archived liability", async () => {
      historyMock.mockResolvedValue([
        { id: 1, workspace_id: 1, liability_id: 2, balance: 900, observed_on: "2026-08-05", created_at: "2026-08-05T00:00:00" },
      ]);
      await renderWithArchived();

      const historyButtons = screen.getAllByRole("button", { name: "Balance history" });
      expect(historyButtons).toHaveLength(2);
      fireEvent.click(historyButtons[1]);

      expect(await screen.findByText("Balance history — Archived Card")).toBeInTheDocument();
      expect(historyMock).toHaveBeenCalledWith(2);
      expect(screen.getByText("Observed on 2026-08-05")).toBeInTheDocument();
    });

    it("exposes Balance on date for a visible archived liability", async () => {
      asOfMock.mockResolvedValue({ liability_id: 2, date: "2026-08-05", currency: "THB", balance: 900, available: true });
      await renderWithArchived();

      const asOfButtons = screen.getAllByRole("button", { name: "Balance on date" });
      expect(asOfButtons).toHaveLength(2);
      fireEvent.click(asOfButtons[1]);
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-05" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));

      await waitFor(() => expect(asOfMock).toHaveBeenCalledWith(2, "2026-08-05"));
      expect(await screen.findByText((_, el) => el?.textContent === "฿900.00")).toBeInTheDocument();
    });

    it("does not expose mutation controls on an archived liability", async () => {
      await renderWithArchived();

      const archivedRow = screen.getByText("Archived Card").closest("div")!.parentElement as HTMLElement;
      expect(within(archivedRow).queryByRole("button", { name: "Edit" })).not.toBeInTheDocument();
      expect(within(archivedRow).queryByRole("button", { name: "Update balance" })).not.toBeInTheDocument();
      expect(within(archivedRow).queryByRole("button", { name: "Record balance" })).not.toBeInTheDocument();
      expect(within(archivedRow).queryByRole("button", { name: "Archive" })).not.toBeInTheDocument();
      expect(within(archivedRow).getByRole("button", { name: "Restore" })).toBeInTheDocument();
    });

    it("keeps as-of isolation intact across an active-to-archived switch", async () => {
      asOfMock.mockResolvedValueOnce({ liability_id: 1, date: "2026-08-10", currency: "THB", balance: 2400000, available: true });
      const archivedItem = await renderWithArchived();

      fireEvent.click(screen.getAllByRole("button", { name: "Balance on date" })[0]);
      fireEvent.change(screen.getByLabelText("As-of date"), { target: { value: "2026-08-10" } });
      fireEvent.click(screen.getByRole("button", { name: "Look up" }));
      await screen.findByText((_, el) => el?.textContent === "฿2,400,000.00");

      fireEvent.click(screen.getAllByRole("button", { name: "Balance on date" })[1]);
      expect(screen.getByText(`Historical balance — ${archivedItem.name}`)).toBeInTheDocument();
      expect(screen.queryByText((_, el) => el?.textContent === "฿2,400,000.00")).not.toBeInTheDocument();
    });
  });
});
