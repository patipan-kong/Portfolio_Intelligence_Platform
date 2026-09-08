"use client";

// Product Intelligence Slice 2 — current follow-up acknowledgment for the
// canonical ExecutionReview. This is intentionally a separate compact card:
// acknowledgment removes a queue item for now and does not edit the review,
// decision, evidence, or any objective evaluation.

import { useCallback, useEffect, useState } from "react";
import {
  getExecutionFollowUp,
  putExecutionFollowUp,
  type ExecutionFollowUp,
  type ExecutionReview,
} from "@/lib/api";

function formatDate(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso.slice(0, 10);
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function isEligible(review: ExecutionReview | null | undefined, reviewable: boolean): boolean {
  return (
    reviewable &&
    review != null &&
    (review.outcome === "MIXED" || review.outcome === "OFF_TRACK")
  );
}

function isConflict(error: unknown): boolean {
  return error instanceof Error && /^API 409(?:$|:)/.test(error.message);
}

export default function ExecutionFollowUpCard({
  portfolioId,
  decisionId,
  reviewable,
  review,
  refreshToken = 0,
  onConflict,
}: {
  portfolioId: number;
  decisionId: number;
  reviewable: boolean;
  review: ExecutionReview | null | undefined;
  /** Parent reloads the canonical review after an optimistic conflict. */
  onConflict?: () => void;
  /** Parent-triggered reload, kept separate from review ownership. */
  refreshToken?: number;
}) {
  const [followUp, setFollowUp] = useState<ExecutionFollowUp | undefined>(undefined);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conflictError, setConflictError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await getExecutionFollowUp(portfolioId, decisionId);
      setFollowUp(result);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to load follow-up state");
    } finally {
      setLoading(false);
    }
  }, [portfolioId, decisionId, refreshToken, review?.updated_at, review?.outcome]);

  useEffect(() => {
    // Clear the previous state while a review edit is being reconciled. This
    // prevents a just-edited outcome from briefly rendering stale suppression.
    setFollowUp(undefined);
    if (!isEligible(review, reviewable)) return;
    load();
  }, [load, review, reviewable]);

  useEffect(() => {
    // Keep a stale-review message visible through the follow-up reload. Clear
    // it only after the canonical review object itself has changed.
    setConflictError(null);
  }, [review?.updated_at, review?.outcome]);

  if (!isEligible(review, reviewable)) {
    return null;
  }

  const acknowledge = async (acknowledged: boolean) => {
    const expectedReviewUpdatedAt = review?.updated_at;
    if (acknowledged && !expectedReviewUpdatedAt) {
      setError("Refresh the current review before acknowledging follow-up.");
      return;
    }
    setSubmitting(true);
    setError(null);
    setConflictError(null);
    try {
      const result = acknowledged
        ? await putExecutionFollowUp(portfolioId, decisionId, {
            acknowledged: true,
            expected_review_updated_at: expectedReviewUpdatedAt as string,
          })
        : await putExecutionFollowUp(portfolioId, decisionId, { acknowledged: false });
      setFollowUp(result);
    } catch (caught) {
      if (isConflict(caught)) {
        // Set this before asking the parent to refresh. Otherwise a fast
        // canonical-review reload can clear the old message first and this
        // async handler would put it back after the refreshed review arrives.
        setConflictError("This review changed while you were viewing it. The current review is being refreshed.");
        onConflict?.();
        await load();
      } else {
        setError(caught instanceof Error ? caught.message : "Failed to update follow-up state");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 space-y-2">
      <h2 className="text-sm font-bold text-gray-900">Follow-up attention</h2>

      {loading && followUp === undefined && (
        <div className="h-12 animate-pulse bg-gray-100 rounded-lg" />
      )}

      {(conflictError ?? error) && (
        <div className="p-2.5 bg-red-50 border border-red-200 text-red-700 text-xs rounded-lg" role="alert">
          {conflictError ?? error}
        </div>
      )}

      {!loading && followUp !== undefined && followUp.acknowledged_at == null && (
        <div className="space-y-2">
          <p className="text-sm text-gray-600">
            Remove this decision from Needs follow-up for now. This does not change your review or mean the issue is resolved.
          </p>
          <button
            type="button"
            onClick={() => acknowledge(true)}
            disabled={submitting}
            className="px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {submitting ? "Saving…" : "Acknowledge follow-up"}
          </button>
        </div>
      )}

      {!loading && followUp !== undefined && followUp.acknowledged_at != null && (
        <div className="space-y-2">
          <p className="text-sm text-gray-600">
            Follow-up acknowledged on {formatDate(followUp.acknowledged_at)}.
          </p>
          <button
            type="button"
            onClick={() => acknowledge(false)}
            disabled={submitting}
            className="text-xs font-semibold text-blue-600 hover:underline disabled:opacity-50"
          >
            {submitting ? "Saving…" : "Return to Needs follow-up"}
          </button>
        </div>
      )}
    </div>
  );
}
