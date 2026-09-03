import { beforeEach, describe, expect, test, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import NetWorthChangeAttributionCard from "@/components/NetWorthChangeAttributionCard";
import type { NetWorthHistoryPoint, NetWorthHistorySummary } from "@/lib/netWorthHistory";
import type { NetWorthChangeAttribution } from "@/lib/api";

const { getNetWorthChangeAttribution } = vi.hoisted(() => ({
  getNetWorthChangeAttribution: vi.fn(),
}));

vi.mock("@/lib/api", () => ({
  getNetWorthChangeAttribution,
}));

beforeEach(() => {
  getNetWorthChangeAttribution.mockReset();
});

function point(date: string, netWorth: number): NetWorthHistoryPoint {
  return {
    date,
    totalAssets: netWorth,
    totalLiabilities: 0,
    netWorth,
    assetsComplete: true,
    liabilitiesComplete: true,
    complete: true,
  };
}

function summaryWithDelta(fromDate: string, toDate: string, fromNW: number, toNW: number): NetWorthHistorySummary {
  const from = point(fromDate, fromNW);
  const to = point(toDate, toNW);
  return {
    points: [from, to],
    completePoints: [from, to],
    latest: to,
    delta: {
      from,
      to,
      change: toNW - fromNW,
      changePct: fromNW !== 0 ? ((toNW - fromNW) / fromNW) * 100 : null,
    },
    anyPartial: false,
    partialCount: 0,
    hasAnyPoints: true,
  };
}

const emptySummary: NetWorthHistorySummary = {
  points: [],
  completePoints: [],
  latest: null,
  delta: null,
  anyPartial: false,
  partialCount: 0,
  hasAnyPoints: false,
};

describe("NetWorthChangeAttributionCard", () => {
  test("fewer than two complete points shows the required empty state and never fetches", async () => {
    render(<NetWorthChangeAttributionCard summary={emptySummary} loading={false} />);
    expect(await screen.findByText("Two complete Net Worth history points are needed.")).toBeInTheDocument();
    expect(getNetWorthChangeAttribution).not.toHaveBeenCalled();
  });

  test("renders exact dates, start/end Net Worth, and the three component rows", async () => {
    const result: NetWorthChangeAttribution = {
      status: "AVAILABLE",
      start_date: "2026-08-12",
      end_date: "2026-08-13",
      start: { investment_assets: 200000, external_cash: 100000, total_assets: 300000, total_liabilities: 0, net_worth: 300000 },
      end: { investment_assets: 250000, external_cash: 90000, total_assets: 340000, total_liabilities: 10000, net_worth: 330000 },
      components: { investment_assets_change: 50000, external_cash_change: -10000, liability_impact: -10000 },
      net_worth_change: 30000,
      reconciliation_difference: 0,
      new_tracking_scope: false,
    };
    getNetWorthChangeAttribution.mockResolvedValue(result);

    render(<NetWorthChangeAttributionCard summary={summaryWithDelta("2026-08-12", "2026-08-13", 300000, 330000)} loading={false} />);

    await waitFor(() => expect(getNetWorthChangeAttribution).toHaveBeenCalledWith("2026-08-12", "2026-08-13"));
    expect(await screen.findByText(/12 Aug 2026/)).toBeInTheDocument();
    expect(screen.getByText(/13 Aug 2026/)).toBeInTheDocument();
    expect(screen.getByText("฿300,000.00")).toBeInTheDocument();
    expect(screen.getByText("฿330,000.00")).toBeInTheDocument();
    expect(screen.getByText("+฿50,000.00")).toBeInTheDocument();
    expect(screen.getAllByText("-฿10,000.00")).toHaveLength(2);
    expect(screen.getByText(/Liabilities increased by/)).toBeInTheDocument();
  });

  test("zero Net Worth delta still renders a full attribution", async () => {
    const result: NetWorthChangeAttribution = {
      status: "AVAILABLE",
      start_date: "2026-08-12",
      end_date: "2026-08-13",
      start: { investment_assets: 200000, external_cash: 100000, total_assets: 300000, total_liabilities: 0, net_worth: 300000 },
      end: { investment_assets: 250000, external_cash: 50000, total_assets: 300000, total_liabilities: 0, net_worth: 300000 },
      components: { investment_assets_change: 50000, external_cash_change: -50000, liability_impact: 0 },
      net_worth_change: 0,
      reconciliation_difference: 0,
      new_tracking_scope: false,
    };
    getNetWorthChangeAttribution.mockResolvedValue(result);

    render(<NetWorthChangeAttributionCard summary={summaryWithDelta("2026-08-12", "2026-08-13", 300000, 300000)} loading={false} />);

    expect(await screen.findByText(/Liabilities unchanged/)).toBeInTheDocument();
    expect(screen.getAllByText("฿300,000.00")).toHaveLength(2);
  });

  test("liability decline renders the decrease wording", async () => {
    const result: NetWorthChangeAttribution = {
      status: "AVAILABLE",
      start_date: "2026-08-12",
      end_date: "2026-08-13",
      start: { investment_assets: 0, external_cash: 100000, total_assets: 100000, total_liabilities: 50000, net_worth: 50000 },
      end: { investment_assets: 0, external_cash: 100000, total_assets: 100000, total_liabilities: 20000, net_worth: 80000 },
      components: { investment_assets_change: 0, external_cash_change: 0, liability_impact: 30000 },
      net_worth_change: 30000,
      reconciliation_difference: 0,
      new_tracking_scope: false,
    };
    getNetWorthChangeAttribution.mockResolvedValue(result);

    render(<NetWorthChangeAttributionCard summary={summaryWithDelta("2026-08-12", "2026-08-13", 50000, 80000)} loading={false} />);

    expect(await screen.findByText(/Liabilities decreased by ฿30,000.00/)).toBeInTheDocument();
  });

  test("UNAVAILABLE never fabricates a zero attribution and shows the reason", async () => {
    const result: NetWorthChangeAttribution = {
      status: "UNAVAILABLE",
      start_date: "2026-08-12",
      end_date: "2026-08-13",
      reason_codes: ["INVESTMENT_EVIDENCE_INCOMPLETE_AT_START"],
    };
    getNetWorthChangeAttribution.mockResolvedValue(result);

    render(<NetWorthChangeAttributionCard summary={summaryWithDelta("2026-08-12", "2026-08-13", 300000, 330000)} loading={false} />);

    expect(await screen.findByText(/Attribution unavailable/)).toBeInTheDocument();
    expect(screen.getByText("Investment assets evidence is incomplete at the start date.")).toBeInTheDocument();
    expect(screen.queryByText("฿0.00")).not.toBeInTheDocument();
    expect(screen.queryByText(/^\+?฿0\.00$/)).not.toBeInTheDocument();
  });

  test("half-recorded funding movement never renders forbidden economic-cause labels", async () => {
    const result: NetWorthChangeAttribution = {
      status: "AVAILABLE",
      start_date: "2026-08-12",
      end_date: "2026-08-13",
      start: { investment_assets: 200000, external_cash: 100000, total_assets: 300000, total_liabilities: 0, net_worth: 300000 },
      end: { investment_assets: 200000, external_cash: 50000, total_assets: 250000, total_liabilities: 0, net_worth: 250000 },
      components: { investment_assets_change: 0, external_cash_change: -50000, liability_impact: 0 },
      net_worth_change: -50000,
      reconciliation_difference: 0,
      new_tracking_scope: false,
    };
    getNetWorthChangeAttribution.mockResolvedValue(result);

    const { container } = render(
      <NetWorthChangeAttributionCard summary={summaryWithDelta("2026-08-12", "2026-08-13", 300000, 250000)} loading={false} />
    );

    await waitFor(() => expect(getNetWorthChangeAttribution).toHaveBeenCalled());
    const text = container.textContent ?? "";
    for (const forbidden of ["market return", "investment return", "debt repayment", "spending", "withdrawal", "unmatched"]) {
      expect(text.toLowerCase()).not.toContain(forbidden);
    }
  });

  test("new tracking scope disclosure renders when the backend reports it", async () => {
    const result: NetWorthChangeAttribution = {
      status: "AVAILABLE",
      start_date: "2026-08-12",
      end_date: "2026-08-13",
      start: { investment_assets: 0, external_cash: 0, total_assets: 0, total_liabilities: 0, net_worth: 0 },
      end: { investment_assets: 0, external_cash: 5000, total_assets: 5000, total_liabilities: 0, net_worth: 5000 },
      components: { investment_assets_change: 0, external_cash_change: 5000, liability_impact: 0 },
      net_worth_change: 5000,
      reconciliation_difference: 0,
      new_tracking_scope: true,
    };
    getNetWorthChangeAttribution.mockResolvedValue(result);

    render(<NetWorthChangeAttributionCard summary={summaryWithDelta("2026-08-12", "2026-08-13", 0, 5000)} loading={false} />);

    expect(await screen.findByText("Includes balances that began being tracked during this period.")).toBeInTheDocument();
  });

  test("loading prop shows a skeleton instead of fetching", () => {
    render(<NetWorthChangeAttributionCard summary={emptySummary} loading={true} />);
    expect(getNetWorthChangeAttribution).not.toHaveBeenCalled();
  });
});
