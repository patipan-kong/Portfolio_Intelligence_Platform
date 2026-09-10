// Execution Ledger workflow predicates — extracted verbatim from
// app/ai-analytics/(hub)/execution/page.tsx so a second surface (Periodic
// Review) can reuse the exact same canonical "deserves review" facts instead
// of re-deriving them. This module performs no classification of its own:
// every predicate here already existed on that page before extraction, and
// the three views remain mutually exclusive for the same reason they were
// there — reviewable/has_review/review_outcome/follow_up_acknowledged_at/
// recording_progress_eligible/is_complete are server-owned facts, not
// something this module computes.

import type { ExecutionLedgerRow } from "@/lib/api";

export function needsReview(row: ExecutionLedgerRow): boolean {
  return row.reviewable && !row.has_review;
}

export function needsRecording(row: ExecutionLedgerRow): boolean {
  return row.recording_progress_eligible && row.is_complete === false;
}

export function isFollowUpAssessment(row: ExecutionLedgerRow): boolean {
  return (
    row.reviewable === true &&
    row.has_review === true &&
    (row.review_outcome === "MIXED" || row.review_outcome === "OFF_TRACK")
  );
}

export function needsFollowUp(row: ExecutionLedgerRow): boolean {
  return isFollowUpAssessment(row) && row.follow_up_acknowledged_at == null;
}

function reviewTimestamp(value: string | null): number | null {
  if (!value) return null;
  const timestamp = new Date(value).getTime();
  return Number.isFinite(timestamp) ? timestamp : null;
}

/**
 * Oldest-review-first — the same view-level sort the Execution Ledger page
 * already applies to its "Needs follow-up" view. `reviewed_at` is set when
 * the canonical review is first created and does not advance when the
 * review is edited, so this orders by review-creation time, not by last
 * follow-up activity.
 */
export function sortNeedsFollowUpRows(rows: ExecutionLedgerRow[]): ExecutionLedgerRow[] {
  return rows.slice().sort((a, b) => {
    const at = reviewTimestamp(a.reviewed_at);
    const bt = reviewTimestamp(b.reviewed_at);

    if (at == null && bt == null) return a.decision_id - b.decision_id;
    if (at == null) return 1;
    if (bt == null) return -1;
    return at - bt || a.decision_id - b.decision_id;
  });
}

/**
 * Oldest-waiting-first — the same view-level sort the Execution Ledger page
 * already applies to its "Needs review" view.
 */
export function sortNeedsReviewRows(rows: ExecutionLedgerRow[]): ExecutionLedgerRow[] {
  return rows.slice().sort((a, b) => {
    const at = a.date ? new Date(a.date).getTime() : Infinity;
    const bt = b.date ? new Date(b.date).getTime() : Infinity;
    return at - bt;
  });
}
