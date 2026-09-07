import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, test, vi } from "vitest";
import ExecutionLedgerPage from "@/app/ai-analytics/(hub)/execution/page";
import type { ExecutionLedger, ExecutionLedgerRow } from "@/lib/api";

const { getExecutionLedger, isUnresolvedPortfolioError, push } = vi.hoisted(() => ({
  getExecutionLedger: vi.fn(),
  isUnresolvedPortfolioError: vi.fn(() => false),
  push: vi.fn(),
}));

vi.mock("@/lib/api", () => ({ getExecutionLedger, isUnresolvedPortfolioError }));
vi.mock("next/navigation", () => ({ useRouter: () => ({ push }) }));

let portfolioState = { currentSelection: 1 as number | null, reportUnresolvedPortfolio: vi.fn() };
vi.mock("@/lib/PortfolioContext", () => ({ usePortfolio: () => portfolioState }));

function row(overrides: Partial<ExecutionLedgerRow> = {}): ExecutionLedgerRow {
  return {
    decision_id: 101,
    snapshot_id: 201,
    date: "2026-08-20T00:00:00Z",
    decision: "APPROVED",
    execution_status: "partial",
    execution_score: 75,
    completeness_pct: 50,
    funding_fidelity_pct: null,
    recording_progress_eligible: true,
    matched_count: 1,
    total_planned: 2,
    is_complete: false,
    outcome_delta: null,
    ...overrides,
  };
}

function ledger(rows: ExecutionLedgerRow[], incompleteRecordingCount = 0): ExecutionLedger {
  return {
    portfolio_id: 1,
    period_days: 90,
    as_of: "2026-08-21T00:00:00Z",
    status: "ok",
    summary: {
      total_decisions: rows.length,
      decision_counts: { APPROVED: rows.length },
      incomplete_recording_count: incompleteRecordingCount,
      acceptance_by_class: {},
      acceptance_note: "Decision-level acceptance only.",
      avg_execution_score: null,
      avg_timing_delta_pct: null,
      avg_funding_fidelity_pct: null,
    },
    rows,
  };
}

beforeEach(() => {
  getExecutionLedger.mockReset();
  isUnresolvedPortfolioError.mockReset().mockReturnValue(false);
  push.mockReset();
  portfolioState = { currentSelection: 1, reportUnresolvedPortfolio: vi.fn() };
});

describe("Execution Intelligence — execution recording follow-up (EFR-01)", () => {
  test("keeps the normal list intact, then filters to only canonically incomplete eligible decisions and resets", async () => {
    const complete = row({ decision_id: 101, snapshot_id: 201, matched_count: 3, total_planned: 3, is_complete: true });
    const incomplete = row({ decision_id: 102, snapshot_id: 202, matched_count: 1, total_planned: 3, is_complete: false });
    const rejected = row({
      decision_id: 103, snapshot_id: 203, decision: "REJECTED",
      recording_progress_eligible: false, matched_count: null, total_planned: null, is_complete: null,
    });
    getExecutionLedger.mockResolvedValue(ledger([complete, incomplete, rejected], 1));

    render(<ExecutionLedgerPage />);

    await screen.findAllByText("#201");
    expect(screen.getAllByText("#202")).not.toHaveLength(0);
    expect(screen.getAllByText("#203")).not.toHaveLength(0);
    expect(screen.getByText("1 decision has incomplete transaction recording.")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Needs recording" }));

    await waitFor(() => expect(screen.queryByText("#201")).not.toBeInTheDocument());
    expect(screen.getAllByText("#202")).not.toHaveLength(0);
    expect(screen.queryByText("#203")).not.toBeInTheDocument();
    expect(screen.getAllByText("1 / 3 recorded")).not.toHaveLength(0);
    expect(screen.getByRole("button", { name: "Show all decisions" })).toHaveAttribute("aria-pressed", "true");

    fireEvent.click(screen.getByRole("button", { name: "Show all decisions" }));
    await screen.findAllByText("#201");
    expect(screen.getAllByText("#203")).not.toHaveLength(0);
  });

  test("preserves the period filter while Needs recording is active and keeps row navigation", async () => {
    const incomplete = row({ decision_id: 102, snapshot_id: 202, matched_count: 1, total_planned: 3, is_complete: false });
    getExecutionLedger.mockResolvedValue(ledger([incomplete], 1));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#202");

    fireEvent.click(screen.getByRole("button", { name: "Needs recording" }));
    fireEvent.click(screen.getByRole("button", { name: "30D" }));

    await waitFor(() => expect(getExecutionLedger).toHaveBeenLastCalledWith(1, 30));
    expect(screen.getAllByText("#202")).not.toHaveLength(0);
    fireEvent.click(screen.getAllByText("#202")[0]);
    expect(push).toHaveBeenCalledWith("/ai-analytics/execution/102");
  });

  test("uses factual empty copy when no eligible decision has incomplete recording", async () => {
    const complete = row({ matched_count: 0, total_planned: 0, is_complete: true });
    const rejected = row({
      decision_id: 103, snapshot_id: 203, decision: "REJECTED",
      recording_progress_eligible: false, matched_count: null, total_planned: null, is_complete: null,
    });
    getExecutionLedger.mockResolvedValue(ledger([complete, rejected], 0));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#201");
    expect(screen.getByText("0 decisions have incomplete transaction recording.")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Needs recording" }));
    expect(await screen.findByText("No decisions with incomplete transaction recording in this view.")).toBeInTheDocument();
    expect(document.body.textContent).not.toMatch(/settled|failed trade|unexecuted/i);
  });
});
