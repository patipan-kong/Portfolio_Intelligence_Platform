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
    review_outcome: null,
    reviewed_at: null,
    follow_up_acknowledged_at: null,
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

describe("Execution Intelligence — Decision Feedback Loop (Slice 3)", () => {
  test("reviewed human decision shows the Review outcome badge", async () => {
    const reviewed = row({
      decision_id: 401, snapshot_id: 501, reviewable: true, has_review: true, review_outcome: "ON_TRACK",
    });
    getExecutionLedger.mockResolvedValue(ledger([reviewed]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#501");

    const badges = Array.from(new Set(screen.getAllByText("On Track").map((el) => el.textContent)));
    expect(badges).toEqual(["On Track"]);
  });

  test("reviewable unreviewed decision shows a muted Needs review indicator", async () => {
    const unreviewed = row({ decision_id: 402, snapshot_id: 502, reviewable: true, has_review: false });
    getExecutionLedger.mockResolvedValue(ledger([unreviewed]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#502");

    const chips = Array.from(new Set(screen.getAllByText("Needs review").map((el) => el.textContent)));
    expect(chips).toEqual(["Needs review"]);
  });

  test("system-generated unreviewed decision shows neither a badge nor Needs review", async () => {
    const expired = row({
      decision_id: 403, snapshot_id: 503, decision: "EXPIRED",
      recording_progress_eligible: false, matched_count: null, total_planned: null, is_complete: null,
      reviewable: false, has_review: false,
    });
    getExecutionLedger.mockResolvedValue(ledger([expired]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#503");

    // "Needs review" also names the toggle button — that one instance is
    // expected; the row itself must contribute no chip of its own.
    expect(screen.getAllByText("Needs review")).toHaveLength(1);
    expect(screen.queryByText("On Track")).not.toBeInTheDocument();
    expect(screen.queryByText("Mixed")).not.toBeInTheDocument();
    expect(screen.queryByText("Off Track")).not.toBeInTheDocument();
  });

  test("persisted inconsistent review on a system-generated decision displays read-only and does not become queue-eligible", async () => {
    const legacy = row({
      decision_id: 404, snapshot_id: 504, decision: "EXPIRED",
      recording_progress_eligible: false, matched_count: null, total_planned: null, is_complete: null,
      reviewable: false, has_review: true, review_outcome: "OFF_TRACK",
    });
    getExecutionLedger.mockResolvedValue(ledger([legacy]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#504");
    expect(Array.from(new Set(screen.getAllByText("Off Track").map((el) => el.textContent)))).toEqual(["Off Track"]);

    // Still gated on `reviewable`, not `has_review` — a legacy review must
    // not make a system-generated decision queue-eligible.
    fireEvent.click(screen.getByRole("button", { name: "Needs review" }));
    expect(await screen.findByText("No decisions need review right now.")).toBeInTheDocument();
    expect(screen.queryByText("#504")).not.toBeInTheDocument();
  });
});

describe("Execution Intelligence — Decision Follow-up Queue (Slice 1)", () => {
  test("includes only reviewable decisions with a current MIXED or OFF_TRACK review", async () => {
    const mixed = row({ decision_id: 501, snapshot_id: 601, has_review: true, review_outcome: "MIXED", reviewed_at: "2026-08-05T00:00:00Z" });
    const offTrack = row({ decision_id: 502, snapshot_id: 602, has_review: true, review_outcome: "OFF_TRACK", reviewed_at: "2026-08-06T00:00:00Z" });
    const onTrack = row({ decision_id: 503, snapshot_id: 603, has_review: true, review_outcome: "ON_TRACK", reviewed_at: "2026-08-07T00:00:00Z" });
    const noReview = row({ decision_id: 504, snapshot_id: 604, has_review: false, review_outcome: null });
    const legacy = row({ decision_id: 505, snapshot_id: 605, reviewable: false, has_review: true, review_outcome: "OFF_TRACK", reviewed_at: "2026-08-01T00:00:00Z" });
    const malformed = row({ decision_id: 506, snapshot_id: 606, has_review: false, review_outcome: "MIXED" });
    const nullOutcome = row({ decision_id: 507, snapshot_id: 607, has_review: true, review_outcome: null });
    getExecutionLedger.mockResolvedValue(ledger([mixed, offTrack, onTrack, noReview, legacy, malformed, nullOutcome]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#601");
    fireEvent.click(screen.getByRole("button", { name: "Needs follow-up" }));

    const visible = Array.from(new Set(screen.getAllByText(/^#60[1-7]$/).map((el) => el.textContent)));
    expect(visible).toEqual(["#601", "#602"]);
    expect(screen.getByText("2 decisions eligible for human review in this window have a current review of mixed or off track.")).toBeInTheDocument();
    expect(screen.queryByText("#603")).not.toBeInTheDocument();
    expect(screen.queryByText("#605")).not.toBeInTheDocument();
    expect(screen.queryByText("#606")).not.toBeInTheDocument();
    expect(screen.queryByText("#607")).not.toBeInTheDocument();
  });

  test("hides acknowledged rows from the queue while retaining the assessment count", async () => {
    const acknowledged = row({
      decision_id: 508,
      snapshot_id: 608,
      has_review: true,
      review_outcome: "MIXED",
      follow_up_acknowledged_at: "2026-09-08T03:00:00Z",
    });
    const open = row({
      decision_id: 509,
      snapshot_id: 609,
      has_review: true,
      review_outcome: "OFF_TRACK",
    });
    getExecutionLedger.mockResolvedValue(ledger([acknowledged, open]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#608");
    expect(screen.getByText("2 decisions eligible for human review in this window have a current review of mixed or off track.")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Needs follow-up" }));
    expect(screen.queryByText("#608")).not.toBeInTheDocument();
    expect(screen.getAllByText("#609")).not.toHaveLength(0);
  });

  test("uses the exact follow-up heading, explanation, ordering hint, and empty state copy", async () => {
    getExecutionLedger.mockResolvedValue(ledger([row({ has_review: true, review_outcome: "ON_TRACK" })]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#201");
    fireEvent.click(screen.getByRole("button", { name: "Needs follow-up" }));

    expect(screen.getByText("Decisions you reviewed as mixed or off track")).toBeInTheDocument();
    expect(screen.getByText("Based on your current retrospective reviews. Acknowledged items are hidden from this view; acknowledgment does not mean resolution.")).toBeInTheDocument();
    expect(screen.getByText("Oldest review first, based on when the review was first recorded.")).toBeInTheDocument();
    expect(screen.getByText("0 decisions eligible for human review in this window have a current review of mixed or off track.")).toBeInTheDocument();
    expect(screen.getByText("No decisions eligible for human review in this window have a mixed or off-track review.")).toBeInTheDocument();
  });

  test("keeps all three attention views mutually exclusive and restores all decisions from the active control", async () => {
    const recording = row({ decision_id: 601, snapshot_id: 701, is_complete: false, has_review: true, review_outcome: "ON_TRACK" });
    const review = row({ decision_id: 602, snapshot_id: 702, is_complete: true, has_review: false, review_outcome: null });
    const followUp = row({ decision_id: 603, snapshot_id: 703, is_complete: true, has_review: true, review_outcome: "MIXED", reviewed_at: "2026-08-01T00:00:00Z" });
    getExecutionLedger.mockResolvedValue(ledger([recording, review, followUp]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#701");

    const recordingButton = () => screen.getByRole("button", { name: "Needs recording" });
    const reviewButton = () => screen.getByRole("button", { name: "Needs review" });
    const followUpButton = () => screen.getByRole("button", { name: "Needs follow-up" });
    const activeButton = () => screen.getByRole("button", { name: "Show all decisions" });

    fireEvent.click(recordingButton());
    expect(activeButton()).toHaveAttribute("aria-pressed", "true");
    expect(reviewButton()).toHaveAttribute("aria-pressed", "false");
    expect(followUpButton()).toHaveAttribute("aria-pressed", "false");

    fireEvent.click(reviewButton());
    expect(recordingButton()).toHaveAttribute("aria-pressed", "false");
    expect(activeButton()).toHaveAttribute("aria-pressed", "true");
    expect(followUpButton()).toHaveAttribute("aria-pressed", "false");

    fireEvent.click(followUpButton());
    expect(recordingButton()).toHaveAttribute("aria-pressed", "false");
    expect(reviewButton()).toHaveAttribute("aria-pressed", "false");
    expect(activeButton()).toHaveAttribute("aria-pressed", "true");

    fireEvent.click(recordingButton());
    expect(activeButton()).toHaveAttribute("aria-pressed", "true");
    expect(reviewButton()).toHaveAttribute("aria-pressed", "false");
    expect(followUpButton()).toHaveAttribute("aria-pressed", "false");

    fireEvent.click(followUpButton());
    expect(recordingButton()).toHaveAttribute("aria-pressed", "false");
    expect(reviewButton()).toHaveAttribute("aria-pressed", "false");
    expect(activeButton()).toHaveAttribute("aria-pressed", "true");

    fireEvent.click(reviewButton());
    expect(recordingButton()).toHaveAttribute("aria-pressed", "false");
    expect(activeButton()).toHaveAttribute("aria-pressed", "true");
    expect(followUpButton()).toHaveAttribute("aria-pressed", "false");

    fireEvent.click(activeButton());
    expect(recordingButton()).toHaveAttribute("aria-pressed", "false");
    expect(reviewButton()).toHaveAttribute("aria-pressed", "false");
    expect(followUpButton()).toHaveAttribute("aria-pressed", "false");
    expect(screen.getAllByText("#701")).not.toHaveLength(0);
    expect(screen.getAllByText("#702")).not.toHaveLength(0);
    expect(screen.getAllByText("#703")).not.toHaveLength(0);
  });

  test("sorts by reviewed_at ascending, then decision_id, with invalid timestamps last", async () => {
    const laterReview = row({ decision_id: 710, snapshot_id: 810, has_review: true, review_outcome: "MIXED", reviewed_at: "2026-08-04T00:00:00Z", date: "2026-08-01T00:00:00Z" });
    const tiedHigherId = row({ decision_id: 712, snapshot_id: 812, has_review: true, review_outcome: "OFF_TRACK", reviewed_at: "2026-08-02T00:00:00Z", date: "2026-08-30T00:00:00Z" });
    const tiedLowerId = row({ decision_id: 711, snapshot_id: 811, has_review: true, review_outcome: "MIXED", reviewed_at: "2026-08-02T00:00:00Z", date: "2026-08-31T00:00:00Z" });
    const invalidHigherId = row({ decision_id: 714, snapshot_id: 814, has_review: true, review_outcome: "OFF_TRACK", reviewed_at: "not-a-date" });
    const missingLowerId = row({ decision_id: 713, snapshot_id: 813, has_review: true, review_outcome: "MIXED", reviewed_at: null });
    getExecutionLedger.mockResolvedValue(ledger([laterReview, tiedHigherId, tiedLowerId, invalidHigherId, missingLowerId]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#810");
    fireEvent.click(screen.getByRole("button", { name: "Needs follow-up" }));

    const ordered = Array.from(new Set(screen.getAllByText(/^#81[0-4]$/).map((el) => el.textContent)));
    expect(ordered).toEqual(["#811", "#812", "#810", "#813", "#814"]);
  });

  test("preserves default order after leaving follow-up and keeps the review badge and detail navigation", async () => {
    const newer = row({ decision_id: 720, snapshot_id: 820, date: "2026-08-20T00:00:00Z", has_review: true, review_outcome: "OFF_TRACK", reviewed_at: "2026-08-02T00:00:00Z" });
    const older = row({ decision_id: 721, snapshot_id: 821, date: "2026-08-01T00:00:00Z", has_review: true, review_outcome: "MIXED", reviewed_at: "2026-08-01T00:00:00Z" });
    getExecutionLedger.mockResolvedValue(ledger([newer, older]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#820");
    fireEvent.click(screen.getByRole("button", { name: "Needs follow-up" }));
    expect(screen.getAllByText("Off Track")).not.toHaveLength(0);
    fireEvent.click(screen.getByRole("button", { name: "Show all decisions" }));

    const ordered = Array.from(new Set(screen.getAllByText(/^#82[01]$/).map((el) => el.textContent)));
    expect(ordered).toEqual(["#820", "#821"]);
    fireEvent.click(screen.getAllByText("#820")[0]);
    expect(push).toHaveBeenCalledWith("/ai-analytics/execution/720");
  });

  test("keeps the count stable across attention switches and updates it for refreshed period data", async () => {
    const followUp = row({ decision_id: 730, snapshot_id: 830, has_review: true, review_outcome: "MIXED", reviewed_at: "2026-08-01T00:00:00Z" });
    const review = row({ decision_id: 731, snapshot_id: 831, has_review: false, review_outcome: null });
    getExecutionLedger.mockResolvedValueOnce(ledger([followUp, review]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#830");
    expect(screen.getByText("1 decision eligible for human review in this window has a current review of mixed or off track.")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Needs follow-up" }));
    expect(screen.getByText("1 decision eligible for human review in this window has a current review of mixed or off track.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Show all decisions" }));
    expect(screen.getByText("1 decision eligible for human review in this window has a current review of mixed or off track.")).toBeInTheDocument();

    getExecutionLedger.mockResolvedValueOnce(ledger([row({ decision_id: 732, snapshot_id: 832, has_review: true, review_outcome: "OFF_TRACK", reviewed_at: "2026-08-02T00:00:00Z" }), row({ decision_id: 733, snapshot_id: 833, has_review: true, review_outcome: "MIXED", reviewed_at: "2026-08-03T00:00:00Z" })]));
    fireEvent.click(screen.getByRole("button", { name: "30D" }));
    await waitFor(() => expect(getExecutionLedger).toHaveBeenLastCalledWith(1, 30));
    expect(screen.getByText("2 decisions eligible for human review in this window have a current review of mixed or off track.")).toBeInTheDocument();
  });

  test("updates the count when the selected portfolio response changes", async () => {
    getExecutionLedger.mockResolvedValueOnce(ledger([row({ decision_id: 734, snapshot_id: 834, has_review: true, review_outcome: "MIXED" })]));
    const { rerender } = render(<ExecutionLedgerPage />);
    await screen.findAllByText("#834");
    expect(screen.getByText("1 decision eligible for human review in this window has a current review of mixed or off track.")).toBeInTheDocument();

    getExecutionLedger.mockResolvedValueOnce(ledger([
      row({ decision_id: 735, snapshot_id: 835, has_review: true, review_outcome: "OFF_TRACK" }),
      row({ decision_id: 736, snapshot_id: 836, has_review: true, review_outcome: "MIXED" }),
    ]));
    portfolioState.currentSelection = 2;
    rerender(<ExecutionLedgerPage />);
    await waitFor(() => expect(getExecutionLedger).toHaveBeenLastCalledWith(2, 90));
    expect(screen.getByText("2 decisions eligible for human review in this window have a current review of mixed or off track.")).toBeInTheDocument();
  });

  test("adds and removes follow-up membership when refreshed review outcomes change", async () => {
    const onTrack = row({ decision_id: 740, snapshot_id: 840, has_review: true, review_outcome: "ON_TRACK", reviewed_at: "2026-08-01T00:00:00Z" });
    const mixed = row({ decision_id: 740, snapshot_id: 840, has_review: true, review_outcome: "MIXED", reviewed_at: "2026-08-01T00:00:00Z" });
    getExecutionLedger.mockResolvedValueOnce(ledger([onTrack])).mockResolvedValueOnce(ledger([mixed])).mockResolvedValueOnce(ledger([onTrack]));

    render(<ExecutionLedgerPage />);
    await screen.findAllByText("#840");
    fireEvent.click(screen.getByRole("button", { name: "Needs follow-up" }));
    expect(await screen.findByText("No decisions eligible for human review in this window have a mixed or off-track review.")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "30D" }));
    await waitFor(() => expect(getExecutionLedger).toHaveBeenLastCalledWith(1, 30));
    expect(screen.getAllByText("#840")).not.toHaveLength(0);

    fireEvent.click(screen.getByRole("button", { name: "90D" }));
    await waitFor(() => expect(getExecutionLedger).toHaveBeenLastCalledWith(1, 90));
    expect(screen.getByText("No decisions eligible for human review in this window have a mixed or off-track review.")).toBeInTheDocument();
  });
});
