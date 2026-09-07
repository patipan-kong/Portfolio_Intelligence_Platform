"use client";

// Review Workflows Slice 3 — shared outcome badge extracted from
// ExecutionReviewCard (Slice 1) so the Execution Intelligence ledger can
// render the same human-authored review outcome without duplicating the
// label/style maps. Visual semantics unchanged from Slice 1. Mirrors the
// DecisionStatusBadge pattern.

import type { ExecutionReviewOutcome } from "@/lib/api";

const OUTCOME_BADGE: Record<ExecutionReviewOutcome, string> = {
  ON_TRACK: "bg-green-100 text-green-800 border-green-200",
  MIXED: "bg-amber-100 text-amber-800 border-amber-200",
  OFF_TRACK: "bg-red-100 text-red-800 border-red-200",
};

const OUTCOME_LABEL: Record<ExecutionReviewOutcome, string> = {
  ON_TRACK: "On Track",
  MIXED: "Mixed",
  OFF_TRACK: "Off Track",
};

export default function ReviewOutcomeBadge({ outcome }: { outcome: ExecutionReviewOutcome }) {
  return (
    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border whitespace-nowrap ${OUTCOME_BADGE[outcome]}`}>
      {OUTCOME_LABEL[outcome]}
    </span>
  );
}
