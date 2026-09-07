import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import PortfolioFundingEvidence from "@/components/PortfolioFundingEvidence";
import { getPortfolioFundingEvidence, type PortfolioFundingEvidenceEvent } from "@/lib/api";

vi.mock("@/lib/api", () => ({
  getPortfolioFundingEvidence: vi.fn(),
}));

const getMock = vi.mocked(getPortfolioFundingEvidence);

const toPortfolioEvent: PortfolioFundingEvidenceEvent = {
  id: 1,
  workspace_id: 1,
  cash_account_id: 5,
  transaction_type: "INVESTMENT_TRANSFER",
  amount: -300,
  signed_amount: -300,
  occurred_on: "2026-08-15",
  category: null,
  note: "September contribution",
  counterparty_portfolio_id: 9,
  counterparty_portfolio_name: "Growth Portfolio",
  counterparty_portfolio_id_snapshot: 9,
  counterparty_portfolio_name_snapshot: "Growth Portfolio",
  investment_direction: "TO_PORTFOLIO",
  created_at: "2026-08-15T00:00:00",
  account_name: "Everyday Cash",
  account_is_archived: false,
};

beforeEach(() => {
  vi.clearAllMocks();
});

describe("PortfolioFundingEvidence", () => {
  it("renders the evidence section on the Portfolio page with the documentary disclaimer visible", async () => {
    getMock.mockResolvedValue([toPortfolioEvent]);
    render(<PortfolioFundingEvidence portfolioId={9} />);

    expect(await screen.findByText("Portfolio Funding Evidence")).toBeInTheDocument();
    expect(
      screen.getByText(/does not prove a portfolio transaction, settlement, or reconciliation occurred/)
    ).toBeInTheDocument();
  });

  it("renders matching events with truthful amount, date, and historical portfolio identity", async () => {
    getMock.mockResolvedValue([toPortfolioEvent]);
    render(<PortfolioFundingEvidence portfolioId={9} />);

    await screen.findByText("2026-08-15");
    expect(screen.getByText(/Recorded to this portfolio/)).toBeInTheDocument();
    expect(screen.getByText(/Everyday Cash/)).toBeInTheDocument();
    expect(screen.getByText(/Growth Portfolio/)).toBeInTheDocument();
    expect(screen.getByText("September contribution")).toBeInTheDocument();
  });

  it("shows a neutral empty state that does not assert absence of funding", async () => {
    getMock.mockResolvedValue([]);
    render(<PortfolioFundingEvidence portfolioId={9} />);

    expect(await screen.findByText("No recorded cash-side investment funding evidence for this portfolio.")).toBeInTheDocument();
    expect(screen.queryByText(/never been funded/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/no deposits/i)).not.toBeInTheDocument();
  });

  it("shows a bounded error without throwing when the request fails", async () => {
    getMock.mockRejectedValue(new Error("network down"));
    render(<PortfolioFundingEvidence portfolioId={9} />);

    expect(await screen.findByRole("alert")).toHaveTextContent("network down");
  });

  it("never claims matched, reconciled, or settled status for an individual evidence row", async () => {
    getMock.mockResolvedValue([toPortfolioEvent]);
    render(<PortfolioFundingEvidence portfolioId={9} />);
    const row = (await screen.findByText("2026-08-15")).closest("li");
    expect(row).not.toBeNull();

    const rowText = (row as HTMLElement).textContent ?? "";
    expect(rowText).not.toMatch(/matched/i);
    expect(rowText).not.toMatch(/reconciled/i);
    expect(rowText).not.toMatch(/settled/i);
    expect(rowText).not.toMatch(/portfolio transaction/i);
  });

  it("renders archived-account context and preserves ordering as returned by the API", async () => {
    const secondEvent: PortfolioFundingEvidenceEvent = {
      ...toPortfolioEvent,
      id: 2,
      occurred_on: "2026-08-01",
      account_name: "Old Savings",
      account_is_archived: true,
      note: null,
    };
    getMock.mockResolvedValue([toPortfolioEvent, secondEvent]);
    render(<PortfolioFundingEvidence portfolioId={9} />);

    const dates = await screen.findAllByText(/2026-08-(15|01)/);
    expect(dates[0]).toHaveTextContent("2026-08-15");
    expect(dates[1]).toHaveTextContent("2026-08-01");
    expect(screen.getByText(/Old Savings/)).toBeInTheDocument();
    expect(screen.getByText(/\(Archived\)/)).toBeInTheDocument();
  });

  it("reloads when the selected portfolio changes and does not contaminate the new selection with a slow prior request", async () => {
    let resolveFirst: (value: PortfolioFundingEvidenceEvent[]) => void = () => {};
    const firstRequest = new Promise<PortfolioFundingEvidenceEvent[]>((resolve) => { resolveFirst = resolve; });
    getMock.mockReturnValueOnce(firstRequest);
    getMock.mockResolvedValueOnce([
      { ...toPortfolioEvent, id: 2, counterparty_portfolio_name_snapshot: "Other Portfolio", note: "Unrelated portfolio's contribution" },
    ]);

    const view = render(<PortfolioFundingEvidence portfolioId={9} />);
    view.rerender(<PortfolioFundingEvidence portfolioId={10} />);
    await screen.findByText(/Other Portfolio/);

    resolveFirst([toPortfolioEvent]);
    await waitFor(() => expect(screen.queryByText("September contribution")).not.toBeInTheDocument());
  });
});
