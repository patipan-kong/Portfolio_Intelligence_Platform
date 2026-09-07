"use client";

// Review Workflows Slice 1 (ERR-01) — "Post-execution review" card for the
// Execution Detail page. One canonical, human-authored, editable review per
// execution decision (Option A). Never mutates the decision or its
// recommendation snapshot — read-only with respect to history; the form only
// ever writes to the review record itself. `reviewed_at` is server-owned
// (set once at first creation) and is not exposed as editable here.

import { useCallback, useEffect, useState } from "react";
import {
  getExecutionReview,
  putExecutionReview,
  type ExecutionReview,
  type ExecutionReviewOutcome,
} from "@/lib/api";

const OUTCOMES: { value: ExecutionReviewOutcome; label: string }[] = [
  { value: "ON_TRACK", label: "On Track" },
  { value: "MIXED", label: "Mixed" },
  { value: "OFF_TRACK", label: "Off Track" },
];

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

function formatReviewedAt(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso.slice(0, 10);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

export default function ExecutionReviewCard({
  portfolioId,
  decisionId,
}: {
  portfolioId: number;
  decisionId: number;
}) {
  const [review, setReview] = useState<ExecutionReview | null | undefined>(undefined);
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [editing, setEditing] = useState(false);
  const [outcome, setOutcome] = useState<ExecutionReviewOutcome | "">("");
  const [summary, setSummary] = useState("");
  const [changedContext, setChangedContext] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setLoadError(null);
    try {
      const result = await getExecutionReview(portfolioId, decisionId);
      setReview(result);
    } catch (e) {
      setLoadError(e instanceof Error ? e.message : "Failed to load review");
    } finally {
      setLoading(false);
    }
  }, [portfolioId, decisionId]);

  useEffect(() => {
    load();
  }, [load]);

  const startEdit = () => {
    setOutcome(review?.outcome ?? "");
    setSummary(review?.summary ?? "");
    setChangedContext(review?.changed_context ?? "");
    setSubmitError(null);
    setEditing(true);
  };

  const cancelEdit = () => {
    setEditing(false);
    setSubmitError(null);
  };

  const save = async () => {
    if (!outcome) {
      setSubmitError("Outcome is required");
      return;
    }
    setSubmitting(true);
    setSubmitError(null);
    try {
      const saved = await putExecutionReview(portfolioId, decisionId, {
        outcome,
        summary: summary.trim() ? summary.trim() : null,
        changed_context: changedContext.trim() ? changedContext.trim() : null,
      });
      setReview(saved);
      setEditing(false);
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : "Failed to save review");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
      <h2 className="text-sm font-bold text-gray-900">Post-execution review</h2>

      {loading && review === undefined && <div className="h-16 animate-pulse bg-gray-100 rounded-lg" />}

      {loadError && (
        <div className="p-2.5 bg-red-50 border border-red-200 text-red-700 text-xs rounded-lg">{loadError}</div>
      )}

      {!loading && !loadError && !editing && review === null && (
        <div className="space-y-2">
          <p className="text-sm text-gray-400">No review yet. Record what happened after this decision was executed.</p>
          <button
            type="button"
            onClick={startEdit}
            className="px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-600 text-white hover:bg-blue-700"
          >
            Add review
          </button>
        </div>
      )}

      {!editing && review && (
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm">
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border whitespace-nowrap ${OUTCOME_BADGE[review.outcome]}`}>
              {OUTCOME_LABEL[review.outcome]}
            </span>
            <span className="text-xs text-gray-400">Reviewed {formatReviewedAt(review.reviewed_at)}</span>
          </div>
          {review.summary && <p className="text-sm text-gray-700 whitespace-pre-wrap">{review.summary}</p>}
          {review.changed_context && (
            <div className="text-sm text-gray-700">
              <span className="font-semibold text-gray-500">Context changed: </span>
              <span className="whitespace-pre-wrap">{review.changed_context}</span>
            </div>
          )}
          <button
            type="button"
            onClick={startEdit}
            className="text-xs font-semibold text-blue-600 hover:underline"
          >
            Edit review
          </button>
        </div>
      )}

      {editing && (
        <div className="space-y-2.5">
          <div>
            <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide block mb-1">
              Outcome
            </label>
            <div className="flex gap-1.5">
              {OUTCOMES.map(({ value, label }) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => setOutcome(value)}
                  className={`px-2.5 py-1 text-xs rounded-full border transition-colors ${
                    outcome === value
                      ? "bg-gray-800 text-white border-gray-800"
                      : "border-gray-300 text-gray-600 hover:bg-gray-100"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide block mb-1">
              Summary (optional)
            </label>
            <textarea
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              placeholder="What happened after this decision was executed?"
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-1 focus:ring-blue-400"
              rows={2}
            />
          </div>

          <div>
            <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide block mb-1">
              Context changed (optional)
            </label>
            <textarea
              value={changedContext}
              onChange={(e) => setChangedContext(e.target.value)}
              placeholder="What changed since this decision was made? e.g. goal, timeline, market regime"
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-1 focus:ring-blue-400"
              rows={2}
            />
          </div>

          {submitError && <p className="text-xs text-red-500">{submitError}</p>}

          <div className="flex gap-2">
            <button
              type="button"
              onClick={save}
              disabled={submitting || !outcome}
              className="px-4 py-2 text-sm font-medium rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
            >
              {submitting ? "Saving…" : "Save review"}
            </button>
            <button
              type="button"
              onClick={cancelEdit}
              disabled={submitting}
              className="px-4 py-2 text-sm font-medium rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
