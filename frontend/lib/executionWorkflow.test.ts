import assert from "node:assert/strict";
import { test } from "node:test";

import {
  isFollowUpAssessment,
  needsFollowUp,
  needsRecording,
  needsReview,
  sortNeedsFollowUpRows,
  sortNeedsReviewRows,
} from "./executionWorkflow.ts";
import type { ExecutionLedgerRow } from "@/lib/api";

function row(overrides: Partial<ExecutionLedgerRow> = {}): ExecutionLedgerRow {
  return {
    decision_id: 1,
    snapshot_id: 10,
    date: "2026-08-20T00:00:00Z",
    decision: "APPROVED",
    execution_status: "complete",
    execution_score: 80,
    completeness_pct: 100,
    funding_fidelity_pct: null,
    recording_progress_eligible: true,
    matched_count: 2,
    total_planned: 2,
    is_complete: true,
    reviewable: true,
    has_review: false,
    review_outcome: null,
    reviewed_at: null,
    follow_up_acknowledged_at: null,
    outcome_delta: null,
    ...overrides,
  };
}

test("needsReview: true only for reviewable rows without a review", () => {
  assert.equal(needsReview(row({ reviewable: true, has_review: false })), true);
  assert.equal(needsReview(row({ reviewable: true, has_review: true })), false);
  assert.equal(needsReview(row({ reviewable: false, has_review: false })), false);
});

test("needsRecording: true only for eligible, incomplete recording", () => {
  assert.equal(needsRecording(row({ recording_progress_eligible: true, is_complete: false })), true);
  assert.equal(needsRecording(row({ recording_progress_eligible: true, is_complete: true })), false);
  assert.equal(needsRecording(row({ recording_progress_eligible: false, is_complete: false })), false);
  assert.equal(needsRecording(row({ recording_progress_eligible: true, is_complete: null })), false);
});

test("isFollowUpAssessment: true only for reviewed decisions graded MIXED or OFF_TRACK", () => {
  assert.equal(isFollowUpAssessment(row({ reviewable: true, has_review: true, review_outcome: "MIXED" })), true);
  assert.equal(isFollowUpAssessment(row({ reviewable: true, has_review: true, review_outcome: "OFF_TRACK" })), true);
  assert.equal(isFollowUpAssessment(row({ reviewable: true, has_review: true, review_outcome: "ON_TRACK" as never })), false);
  assert.equal(isFollowUpAssessment(row({ reviewable: true, has_review: false, review_outcome: null })), false);
});

test("needsFollowUp: only unacknowledged follow-up assessments", () => {
  const assessed = row({ reviewable: true, has_review: true, review_outcome: "MIXED", follow_up_acknowledged_at: null });
  const acknowledged = row({ reviewable: true, has_review: true, review_outcome: "MIXED", follow_up_acknowledged_at: "2026-08-21T00:00:00Z" });
  assert.equal(needsFollowUp(assessed), true);
  assert.equal(needsFollowUp(acknowledged), false);
});

test("a single row can satisfy more than one predicate — no invented mutual exclusivity", () => {
  const r = row({
    reviewable: true,
    has_review: true,
    review_outcome: "MIXED",
    follow_up_acknowledged_at: null,
    recording_progress_eligible: true,
    is_complete: false,
  });
  assert.equal(needsFollowUp(r), true);
  assert.equal(needsRecording(r), true);
  assert.equal(needsReview(r), false); // has_review is true, so this one is correctly excluded
});

test("sortNeedsReviewRows orders by date ascending, undated rows last", () => {
  const a = row({ decision_id: 1, date: "2026-08-20T00:00:00Z" });
  const b = row({ decision_id: 2, date: "2026-08-10T00:00:00Z" });
  const c = row({ decision_id: 3, date: null });
  const sorted = sortNeedsReviewRows([a, b, c]);
  assert.deepEqual(sorted.map((r) => r.decision_id), [2, 1, 3]);
});

test("sortNeedsFollowUpRows orders by reviewed_at ascending, undated rows last, tie-broken by decision_id", () => {
  const a = row({ decision_id: 5, reviewed_at: "2026-08-20T00:00:00Z" });
  const b = row({ decision_id: 2, reviewed_at: "2026-08-10T00:00:00Z" });
  const c = row({ decision_id: 1, reviewed_at: null });
  const d = row({ decision_id: 3, reviewed_at: null });
  const sorted = sortNeedsFollowUpRows([a, b, c, d]);
  assert.deepEqual(sorted.map((r) => r.decision_id), [2, 5, 1, 3]);
});
