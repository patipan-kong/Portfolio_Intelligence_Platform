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
    reviewable: true,
    has_review: false,
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

describe("Execution Intelligence — Review Queue (Slice 2)", () => {
  test("Needs review shows only reviewable decisions with no review, oldest executed_at first", async () => {
    const reviewedApproved = row({
      decision_id: 201, snapshot_id: 301, date: "2026-08-10T00:00:00Z",
      reviewable: true, has_review: true,
    });
    const oldestUnreviewed = row({
      decision_id: 202, snapshot_id: 302, date: "2026-08-01T00:00:00Z", decision: "REJECTED",
      recording_progress_eligible: false, matched_count: null, total_planned: null, is_complete: null,
      reviewable: true, has_review: false,
    });
    const newestUnreviewed = row({
      decision_id: 203, snapshot_id: 303, date: "2026-08-15T00:00:00Z",
      reviewable: true, has_review: false,
    });
    const expiredNonReviewable = row({
      decision_id: 204, snapshot_id: 304, date: "2026-07-01T00:00:00Z", decision: "EXPIRED",
      recording_progress_eligible: false, matched_count: null, total_planned: null, is_complete: null,
      reviewable: false, has_review: false,
    });
    getExecutionLedger.mockResolvedValue(ledger([reviewedApproved, oldestUnreviewed, newestUnreviewed, expiredNonReviewable]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#301");

    fireEvent.click(screen.getByRole("button", { name: "Needs review" }));

    await waitFor(() => expect(screen.queryByText("#301")).not.toBeInTheDocument());
    expect(screen.queryByText("#304")).not.toBeInTheDocument();
    // EvidenceLedger renders both a desktop table and a mobile card list for
    // the same rows (CSS-hidden, not DOM-removed, under jsdom) — dedupe.
    const rows = Array.from(new Set(screen.getAllByText(/^#30[23]$/).map((el) => el.textContent)));
    expect(rows).toEqual(["#302", "#303"]);
    expect(screen.getByText("Decisions needing a review")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Show all decisions" })).toHaveAttribute("aria-pressed", "true");
  });

  test("row navigation still targets Execution Detail while Needs review is active", async () => {
    const unreviewed = row({ decision_id: 202, snapshot_id: 302, reviewable: true, has_review: false });
    getExecutionLedger.mockResolvedValue(ledger([unreviewed]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#302");

    fireEvent.click(screen.getByRole("button", { name: "Needs review" }));
    await waitFor(() => expect(screen.getAllByText("#302")).not.toHaveLength(0));
    fireEvent.click(screen.getAllByText("#302")[0]);
    expect(push).toHaveBeenCalledWith("/ai-analytics/execution/202");
  });

  test("uses factual empty copy when nothing needs review", async () => {
    const reviewed = row({ reviewable: true, has_review: true });
    getExecutionLedger.mockResolvedValue(ledger([reviewed]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#201");

    fireEvent.click(screen.getByRole("button", { name: "Needs review" }));
    expect(await screen.findByText("No decisions need review right now.")).toBeInTheDocument();
  });

  test("Needs review and Needs recording are mutually exclusive", async () => {
    const incompleteRecording = row({
      decision_id: 102, snapshot_id: 202, matched_count: 1, total_planned: 3, is_complete: false,
      reviewable: true, has_review: true,
    });
    const needsReviewRow = row({
      decision_id: 205, snapshot_id: 305, is_complete: true, reviewable: true, has_review: false,
    });
    getExecutionLedger.mockResolvedValue(ledger([incompleteRecording, needsReviewRow], 1));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#202");

    fireEvent.click(screen.getByRole("button", { name: "Needs recording" }));
    await waitFor(() => expect(screen.getByRole("button", { name: "Show all decisions" })).toHaveAttribute("aria-pressed", "true"));
    expect(screen.getByRole("button", { name: "Needs review" })).toHaveAttribute("aria-pressed", "false");
    expect(screen.queryByText("#305")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Needs review" }));
    await waitFor(() => expect(screen.queryByText("#202")).not.toBeInTheDocument());
    expect(screen.getByRole("button", { name: "Needs recording" })).toHaveAttribute("aria-pressed", "false");
    expect(screen.getAllByText("#305")).not.toHaveLength(0);
  });

  test("normal ledger order is unaffected by Review Queue ordering logic", async () => {
    const older = row({ decision_id: 301, snapshot_id: 401, date: "2026-08-01T00:00:00Z" });
    const newer = row({ decision_id: 302, snapshot_id: 402, date: "2026-08-20T00:00:00Z" });
    getExecutionLedger.mockResolvedValue(ledger([newer, older]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#401");

    const orderedIds = Array.from(new Set(screen.getAllByText(/^#40[12]$/).map((el) => el.textContent)));
    expect(orderedIds).toEqual(["#402", "#401"]);
  });
});
