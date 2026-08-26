import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GoalsPage from "@/app/goals/page";
import { createWealthGoal, listWealthGoals, updateWealthGoal, type WealthGoal } from "@/lib/api";

vi.mock("@/lib/api", () => ({
  createWealthGoal: vi.fn(),
  listWealthGoals: vi.fn(),
  updateWealthGoal: vi.fn(),
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

const listMock = vi.mocked(listWealthGoals);
const createMock = vi.mocked(createWealthGoal);
const updateMock = vi.mocked(updateWealthGoal);

describe("GoalsPage", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    listMock.mockResolvedValue([]);
    createMock.mockResolvedValue(goal);
    updateMock.mockResolvedValue(goal);
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

  it("does not introduce a progress bar, funding linkage, or projection language in the v1 experience", async () => {
    listMock.mockResolvedValue([goal]);
    render(<GoalsPage />);
    await screen.findByText("Retire by 55");
    // The header explicitly disclaims progress/funding ("is not progress, and is
    // not linked to..."), so this checks for an actual progress/funding feature
    // (a computed percentage, a funding source, a projection), not the word.
    expect(screen.queryByText(/%\s*(complete|funded|toward)|funding source|projected to reach|forecast/i)).not.toBeInTheDocument();
  });
});
