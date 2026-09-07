import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import PortfolioInvestmentMandates from "@/components/PortfolioInvestmentMandates";
import {
  deletePortfolioInvestmentMandate,
  listPortfolioInvestmentMandates,
  listWealthGoals,
  putPortfolioInvestmentMandate,
  type PortfolioInvestmentMandate,
  type WealthGoal,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  deletePortfolioInvestmentMandate: vi.fn(),
  listPortfolioInvestmentMandates: vi.fn(),
  listWealthGoals: vi.fn(),
  putPortfolioInvestmentMandate: vi.fn(),
}));

const activeLinked: WealthGoal = {
  id: 1, workspace_id: 1, name: "Retirement", goal_type: "RETIREMENT",
  target_amount: 1_000_000, currency: "THB", target_date: null,
  priority: "HIGH", note: null, is_archived: false,
  created_at: "2026-09-01T00:00:00", updated_at: "2026-09-01T00:00:00",
};
const archivedLinked: WealthGoal = {
  ...activeLinked, id: 2, name: "Old home plan", is_archived: true,
};
const activeCandidate: WealthGoal = {
  ...activeLinked, id: 3, name: "Education",
};
const firstMandate: PortfolioInvestmentMandate = {
  id: 10, workspace_id: 1, portfolio_id: 9, wealth_goal_id: 1,
  created_at: "2026-09-01T00:00:00",
};
const archivedMandate: PortfolioInvestmentMandate = {
  id: 11, workspace_id: 1, portfolio_id: 9, wealth_goal_id: 2,
  created_at: "2026-09-01T00:00:00",
};

const listMandatesMock = vi.mocked(listPortfolioInvestmentMandates);
const listGoalsMock = vi.mocked(listWealthGoals);
const putMock = vi.mocked(putPortfolioInvestmentMandate);
const deleteMock = vi.mocked(deletePortfolioInvestmentMandate);

beforeEach(() => {
  vi.clearAllMocks();
  listMandatesMock.mockResolvedValue([firstMandate, archivedMandate]);
  listGoalsMock.mockResolvedValue([activeLinked, archivedLinked, activeCandidate]);
  putMock.mockResolvedValue({
    id: 12, workspace_id: 1, portfolio_id: 9, wealth_goal_id: 3,
    created_at: "2026-09-01T00:00:00",
  });
  deleteMock.mockResolvedValue(undefined);
});

describe("PortfolioInvestmentMandates", () => {
  it("renders linked and archived goals while offering only active unlinked candidates", async () => {
    render(<PortfolioInvestmentMandates portfolioId={9} />);

    expect(await screen.findByText("Retirement")).toBeInTheDocument();
    expect(screen.getByText("Old home plan")).toBeInTheDocument();
    expect(screen.getByText("Archived")).toBeInTheDocument();
    const select = screen.getByLabelText("Goal to add") as HTMLSelectElement;
    expect(within(select).getByRole("option", { name: "Education" })).toBeInTheDocument();
    expect(within(select).queryByRole("option", { name: "Retirement" })).not.toBeInTheDocument();
    expect(within(select).queryByRole("option", { name: "Old home plan" })).not.toBeInTheDocument();
    expect(select.value).toBe("");
    expect(putMock).not.toHaveBeenCalled();
    expect(deleteMock).not.toHaveBeenCalled();
    expect(listGoalsMock).toHaveBeenCalledWith(true);
  });

  it("authors only after explicit Add and removes an archived link only after explicit Remove", async () => {
    render(<PortfolioInvestmentMandates portfolioId={9} />);
    await screen.findByText("Old home plan");

    fireEvent.change(screen.getByLabelText("Goal to add"), { target: { value: "3" } });
    expect(putMock).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "Add" }));
    await waitFor(() => expect(putMock).toHaveBeenCalledWith(9, 3));
    expect(await screen.findByText("Education")).toBeInTheDocument();

    const archivedRow = screen.getByText("Old home plan").closest("li");
    expect(archivedRow).not.toBeNull();
    expect(deleteMock).not.toHaveBeenCalled();
    fireEvent.click(within(archivedRow as HTMLElement).getByRole("button", { name: "Remove" }));
    await waitFor(() => expect(deleteMock).toHaveBeenCalledWith(9, 2));
    await waitFor(() => expect(screen.queryByText("Old home plan")).not.toBeInTheDocument());
  });

  it("reloads factual state when the selected portfolio changes", async () => {
    listMandatesMock.mockImplementation(async (portfolioId) => portfolioId === 9 ? [firstMandate] : [{
      id: 20, workspace_id: 1, portfolio_id: 10, wealth_goal_id: 3,
      created_at: "2026-09-01T00:00:00",
    }]);
    const view = render(<PortfolioInvestmentMandates portfolioId={9} />);
    expect(await screen.findByText("Retirement")).toBeInTheDocument();

    view.rerender(<PortfolioInvestmentMandates portfolioId={10} />);

    expect(await screen.findByText("Education")).toBeInTheDocument();
    await waitFor(() => {
      const linkedRows = screen.getAllByRole("listitem");
      expect(linkedRows).toHaveLength(1);
      expect(linkedRows[0]).toHaveTextContent("Education");
      expect(linkedRows[0]).not.toHaveTextContent("Retirement");
    });
    expect(listMandatesMock).toHaveBeenLastCalledWith(10);
    expect(putMock).not.toHaveBeenCalled();
  });

  it("does not let a pending mutation from a previous portfolio contaminate the newly selected portfolio's displayed state", async () => {
    const portfolioBGoal: WealthGoal = { ...activeLinked, id: 4, name: "Home renovation" };
    const portfolioBMandate: PortfolioInvestmentMandate = {
      id: 30, workspace_id: 1, portfolio_id: 10, wealth_goal_id: 4,
      created_at: "2026-09-01T00:00:00",
    };
    listGoalsMock.mockResolvedValue([activeLinked, archivedLinked, activeCandidate, portfolioBGoal]);
    listMandatesMock.mockImplementation(async (portfolioId) =>
      portfolioId === 9 ? [firstMandate] : [portfolioBMandate]);

    let resolvePendingAdd: (mandate: PortfolioInvestmentMandate) => void = () => {};
    const pendingAdd = new Promise<PortfolioInvestmentMandate>((resolve) => { resolvePendingAdd = resolve; });
    putMock.mockReturnValue(pendingAdd);

    const view = render(<PortfolioInvestmentMandates portfolioId={9} />);
    await screen.findByText("Retirement");

    fireEvent.change(screen.getByLabelText("Goal to add"), { target: { value: "3" } });
    fireEvent.click(screen.getByRole("button", { name: "Add" }));
    await waitFor(() => expect(putMock).toHaveBeenCalledWith(9, 3));

    view.rerender(<PortfolioInvestmentMandates portfolioId={10} />);
    await screen.findByText("Home renovation");

    resolvePendingAdd({
      id: 99, workspace_id: 1, portfolio_id: 9, wealth_goal_id: 3,
      created_at: "2026-09-01T00:00:00",
    });

    await waitFor(() => {
      const rows = screen.getAllByRole("listitem");
      expect(rows).toHaveLength(1);
      expect(rows[0]).toHaveTextContent("Home renovation");
      expect(rows[0]).not.toHaveTextContent("Education");
    });
  });
});
