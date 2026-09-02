"use client";

// Extracted from app/optimizer/page.tsx (Decision Continuity UX Slice 1) so
// this component can be unit-tested directly — Next's App Router only
// allows a page.tsx file to export a small fixed set of well-known names
// (default, metadata, generateStaticParams, …), so a component intended for
// direct import in tests cannot live there.
//
// TZ/DECISION_CFG/DECISION_BADGE are also consumed elsewhere in
// app/optimizer/page.tsx (date formatting, DecisionMemoryTimeline) and are
// re-exported here for that purpose — the single source of truth simply
// moved file.

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  listExecutionDecisions, getExecutionDecision, getExecutionDetail,
  getShadowPerformanceSummary, recordDecisionBySnapshot,
} from "@/lib/api";
import type {
  ExecutionDecision, ExecutionDecisionType, OverrideCategoryType,
  ShadowPerformanceSummary, ExecutionAnalysis, DecisionGoalContext,
  DecisionGoalContextGoal,
} from "@/lib/api";

export const TZ = "Asia/Bangkok";

export const DECISION_CFG: Record<ExecutionDecisionType, { label: string; cls: string; icon: string }> = {
  APPROVED:         { label: "Approve Recommendation", icon: "✓", cls: "bg-green-600 text-white hover:bg-green-700" },
  REJECTED:         { label: "Reject Recommendation", icon: "✗", cls: "border border-red-300 text-red-700 hover:bg-red-50" },
  MANUAL_OVERRIDE:  { label: "Manual Override",  icon: "✎", cls: "border border-gray-300 text-gray-600 hover:bg-gray-50" },
  PARTIAL_EXECUTION:{ label: "Partial",          icon: "½", cls: "border border-amber-300 text-amber-700 hover:bg-amber-50" },
};

export const DECISION_BADGE: Record<ExecutionDecisionType, string> = {
  APPROVED:          "bg-green-100 text-green-800 border-green-200",
  REJECTED:          "bg-red-100 text-red-800 border-red-200",
  MANUAL_OVERRIDE:   "bg-gray-100 text-gray-700 border-gray-200",
  PARTIAL_EXECUTION: "bg-amber-100 text-amber-800 border-amber-200",
};

// Decision → Transaction Linkage Completion: REJECTED decisions are evaluated
// via whole-portfolio counterfactual return (opportunity_cost.py), never via
// linked-transaction analysis, so they never get a "Record execution" entry
// point. System-generated rows (e.g. EXPIRED) had no human action to execute.
const RECORD_EXECUTION_ELIGIBLE: ReadonlySet<ExecutionDecisionType> = new Set([
  "APPROVED", "MANUAL_OVERRIDE", "PARTIAL_EXECUTION",
]);

// Execution Completion Polish (Slice 3): completion is derived solely from
// matched_count/total_planned/is_complete — never from analysis.status,
// which is a grading-measurability flag (e.g. a fully-recorded decision
// with no planned funding-source trade still reports status="partial").
// Exported so the Execution Detail page renders identical copy rather than
// re-deriving its own notion of "complete" (ENGINEERING_PRINCIPLES.md
// Single Source of Truth).
export function executionCompletionLabel(analysis: ExecutionAnalysis | null): string | null {
  if (!analysis) return null;
  const { matched_count, total_planned, is_complete } = analysis;
  // Correction pass (review finding 2/4): `no_target_allocations` is a
  // genuinely missing-evidence response (execution_ledger.py's
  // _decision_analysis short-circuits before computing anything) — distinct
  // from "plan known, zero matches yet", which always populates all three
  // fields. Never infer completion, and never interpolate undefined, when
  // evidence is absent.
  if (matched_count == null || total_planned == null || is_complete == null) {
    return "Recording status unavailable";
  }
  if (is_complete) return "Execution complete";
  if (matched_count === 0) return "Not recorded";
  return `Partially recorded (${matched_count} of ${total_planned})`;
}

// Goal context at time of decision (Phase 7.4/ADR-008, CONTEXT_ONLY) — a
// factual disclosure of what a goal looked like when this recommendation
// was made, sourced entirely from the already-fetched, already-frozen
// decision_context payload above. No causal claim is made or implied; see
// OPTIMIZER_PHILOSOPHY.md and docs/decisions/ADR-008 for the CONTEXT_ONLY
// boundary this must not cross.
function formatGoalPriority(priority: string): string {
  return priority.charAt(0) + priority.slice(1).toLowerCase();
}

function formatGoalTargetDate(targetDate: string | null): string | null {
  if (!targetDate) return null;
  const d = new Date(targetDate);
  if (Number.isNaN(d.getTime())) return null;
  return d.toLocaleDateString("en-GB", { month: "short", year: "numeric" });
}

function GoalContextFactsRow({ goal }: { goal: DecisionGoalContextGoal }) {
  const targetDate = formatGoalTargetDate(goal.target_date);
  return (
    <div className="text-xs">
      <span className="font-semibold text-gray-700">{goal.name}</span>
      <span className="text-gray-500">
        {" — "}฿{goal.target_amount.toLocaleString("th-TH")} target
        {targetDate ? ` · ${targetDate}` : ""}
        {" · "}{goal.progress_percent.toFixed(0)}% funded
        {" · "}{formatGoalPriority(goal.priority)} priority
      </span>
    </div>
  );
}

function GoalContextAtDecisionTime({ goalContext }: { goalContext: DecisionGoalContext | null }) {
  if (goalContext?.context_state !== "COMPLETE" || goalContext.goals.length === 0) return null;
  return (
    <div className="mt-2.5 pt-2.5 border-t border-gray-100 space-y-1">
      <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide">
        Goal context at time of decision
      </p>
      {goalContext.goals.map((g) => <GoalContextFactsRow key={g.id} goal={g} />)}
    </div>
  );
}

function ShadowReturnChip({ label, value }: { label: string; value: number | null }) {
  if (value === null) return null;
  const positive = value >= 0;
  return (
    <div className="text-xs">
      <span className="text-gray-400">{label}: </span>
      <span className={`font-semibold ${positive ? "text-green-600" : "text-red-600"}`}>
        {positive ? "+" : ""}{value.toFixed(2)}%
      </span>
    </div>
  );
}

export function DecisionActionPanel({
  snapshotId,
  portfolioId,
}: {
  snapshotId: number;
  portfolioId: number;
}) {
  const [existing, setExisting] = useState<ExecutionDecision | null | undefined>(undefined);
  const [confirming, setConfirming] = useState<ExecutionDecisionType | null>(null);
  const [notes, setNotes] = useState("");
  const [overrideType, setOverrideType] = useState<OverrideCategoryType | "">("");
  const [originalSymbol, setOriginalSymbol] = useState("");
  const [replacementSymbol, setReplacementSymbol] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [shadowPerf, setShadowPerf] = useState<ShadowPerformanceSummary | null>(null);
  const [linkage, setLinkage] = useState<ExecutionAnalysis | null>(null);
  const [goalContext, setGoalContext] = useState<DecisionGoalContext | null>(null);

  useEffect(() => {
    listExecutionDecisions(portfolioId, undefined, 50)
      .then((ds) => {
        const match = ds.find((d) => d.recommendation_snapshot_id === snapshotId);
        setExisting(match ?? null);
      })
      .catch(() => setExisting(null));
  }, [snapshotId, portfolioId]);

  // Fetch shadow performance once we know an APPROVED decision exists
  useEffect(() => {
    if (existing?.decision === "APPROVED") {
      getShadowPerformanceSummary(portfolioId)
        .then(setShadowPerf)
        .catch(() => setShadowPerf(null));
    }
  }, [existing, portfolioId]);

  // Reuse the existing execution-analysis evidence for a small coverage
  // indicator — no new backend endpoint or status model. Only fetched for
  // decisions linkage is meaningful for; a REJECTED/system-generated/EXPIRED
  // decision has no execution to link and would just be a wasted request.
  useEffect(() => {
    if (!existing || existing.is_system_generated || !RECORD_EXECUTION_ELIGIBLE.has(existing.decision)) {
      setLinkage(null);
      return;
    }
    getExecutionDetail(portfolioId, existing.id)
      .then((detail) => setLinkage(detail.analysis))
      .catch(() => setLinkage(null));
  }, [existing, portfolioId]);

  // Goal provenance (Phase 7.4/ADR-008, CONTEXT_ONLY) — already persisted on
  // the RecommendationSnapshot at run time; reused here via the existing
  // single-decision endpoint rather than duplicated or re-derived. Fails
  // closed to "no chip" on any error, malformed/legacy payload included.
  useEffect(() => {
    if (!existing) {
      setGoalContext(null);
      return;
    }
    getExecutionDecision(existing.id)
      .then((detail) => setGoalContext(detail.recommendation_snapshot?.decision_context ?? null))
      .catch(() => setGoalContext(null));
  }, [existing]);

  if (existing === undefined) return null; // still loading

  const handleConfirm = async () => {
    if (!confirming) return;
    setSubmitting(true);
    setError(null);
    try {
      await recordDecisionBySnapshot(snapshotId, {
        portfolio_id: portfolioId,
        recommendation_snapshot_id: snapshotId,
        decision: confirming,
        override_notes: notes.trim() || undefined,
        create_static_shadow: confirming !== "APPROVED",
        override_type: (confirming === "MANUAL_OVERRIDE" && overrideType) ? overrideType : undefined,
        original_symbol: (confirming === "MANUAL_OVERRIDE" && originalSymbol.trim()) ? originalSymbol.trim() : undefined,
        replacement_symbol: (confirming === "MANUAL_OVERRIDE" && replacementSymbol.trim()) ? replacementSymbol.trim() : undefined,
      });
      const ds = await listExecutionDecisions(portfolioId, undefined, 50);
      const match = ds.find((d) => d.recommendation_snapshot_id === snapshotId);
      setExisting(match ?? null);
      window.dispatchEvent(new CustomEvent("execution-decision-recorded", {
        detail: { portfolioId, snapshotId, decision: confirming },
      }));
      setConfirming(null);
      setNotes("");
      setOverrideType("");
      setOriginalSymbol("");
      setReplacementSymbol("");
    } catch {
      setError("Failed to record decision. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  if (existing) {
    const cfg = DECISION_CFG[existing.decision] ?? DECISION_CFG.MANUAL_OVERRIDE;
    const badgeCls = DECISION_BADGE[existing.decision] ?? DECISION_BADGE.MANUAL_OVERRIDE;
    const staticShadow = shadowPerf?.summary?.static_frozen ?? null;
    const activeShadow = shadowPerf?.summary?.active_model ?? null;
    const trackingActive = shadowPerf?.has_shadows && shadowPerf.shadows.length > 0;

    return (
      <section className="bg-white border rounded-xl p-4 shadow-sm">
        <div className="flex items-center gap-3 flex-wrap">
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Decision Recorded</span>
          <span className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${badgeCls}`}>
            {cfg.icon} {cfg.label}
          </span>
          {existing.override_type && (
            <span className="text-xs px-2 py-0.5 rounded-full border border-gray-200 bg-gray-50 text-gray-600 font-medium">
              {existing.override_type.replace(/_/g, " ")}
            </span>
          )}
          {existing.original_symbol && (
            <span className="text-xs text-gray-500 font-mono">
              {existing.original_symbol}
              {existing.replacement_symbol && ` → ${existing.replacement_symbol}`}
            </span>
          )}
          {existing.override_notes && (
            <span className="text-xs text-gray-500 italic">"{existing.override_notes}"</span>
          )}
          {goalContext?.context_state === "COMPLETE" && goalContext.goals.length > 0 && (
            <span className="text-xs px-2 py-0.5 rounded-full border border-indigo-200 bg-indigo-50 text-indigo-700 font-medium">
              {goalContext.goals.length > 1 ? "Goals: " : "Goal: "}
              {goalContext.goals.map((g) => g.name).join(", ")}
            </span>
          )}
          <span className="text-xs text-gray-400 ml-auto">
            {new Date(existing.executed_at).toLocaleString("en-GB", { dateStyle: "short", timeStyle: "short", timeZone: TZ })}
          </span>
        </div>

        <GoalContextAtDecisionTime goalContext={goalContext} />

        {/* Shadow tracking status */}
        {existing.decision === "APPROVED" && (
          <div className="mt-2.5 pt-2.5 border-t border-gray-100">
            {trackingActive ? (
              <div className="space-y-1.5">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="inline-flex items-center gap-1 text-xs font-medium text-teal-700 bg-teal-50 border border-teal-200 px-2 py-0.5 rounded-full">
                    <span className="w-1.5 h-1.5 rounded-full bg-teal-500 animate-pulse" />
                    Shadow Tracking Active
                  </span>
                  {shadowPerf?.summary?.tracking_since && (
                    <span className="text-xs text-gray-400">
                      since {shadowPerf.summary.tracking_since}
                    </span>
                  )}
                </div>
                {(staticShadow?.inception_return_pct !== undefined || activeShadow?.inception_return_pct !== undefined) && (
                  <div className="flex gap-4 flex-wrap">
                    <ShadowReturnChip label="Frozen" value={staticShadow?.inception_return_pct ?? null} />
                    <ShadowReturnChip label="AI Model" value={activeShadow?.inception_return_pct ?? null} />
                    {(staticShadow?.latest_alpha !== undefined || activeShadow?.latest_alpha !== undefined) && (
                      <div className="text-xs text-gray-400">
                        α {(activeShadow?.latest_alpha ?? staticShadow?.latest_alpha ?? 0) >= 0 ? "+" : ""}
                        {((activeShadow?.latest_alpha ?? staticShadow?.latest_alpha) ?? 0).toFixed(2)}% vs benchmark
                      </div>
                    )}
                  </div>
                )}
                {!staticShadow?.inception_return_pct && !activeShadow?.inception_return_pct && (
                  <p className="text-xs text-gray-400">Performance data available after first daily valuation (17:45 ICT).</p>
                )}
              </div>
            ) : (
              <p className="text-xs text-gray-400">
                Shadow portfolios are being initialized — data will appear after the next daily valuation.
              </p>
            )}
          </div>
        )}
        {existing.decision !== "APPROVED" && (
          <p className="text-xs text-gray-400 mt-1.5">
            Performance impact tracked. See Attribution panel below.
          </p>
        )}

        {/* AI Evaluation M7 entry point (UX §2.3): "Track this decision" ->
            the graded execution detail (S4b) for this exact decision. */}
        <div className="mt-2.5 pt-2.5 border-t border-gray-100 flex items-center gap-3 flex-wrap">
          <Link
            href={`/ai-analytics/execution/${existing.id}`}
            className="text-xs font-semibold text-blue-600 hover:underline"
          >
            Track this decision in AI Evaluation →
          </Link>
          {executionCompletionLabel(linkage) && (
            <span className="text-xs text-gray-400">{executionCompletionLabel(linkage)}</span>
          )}
          {!existing.is_system_generated && RECORD_EXECUTION_ELIGIBLE.has(existing.decision) && (
            <Link
              href={`/portfolio?decision=${existing.id}`}
              className="text-xs font-semibold text-green-700 hover:underline ml-auto"
            >
              Record execution →
            </Link>
          )}
        </div>
      </section>
    );
  }

  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm">
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
        Record Execution Decision
      </p>

      {confirming ? (
        <div className="space-y-3">
          <p className="text-sm text-gray-700">
            You are recording{" "}
            <span className={`font-semibold ${confirming === "APPROVED" ? "text-green-700" : confirming === "REJECTED" ? "text-red-700" : "text-gray-700"}`}>
              {DECISION_CFG[confirming]?.label}
            </span>{" "}
            for this optimizer recommendation.
            {confirming === "APPROVED" && (
              <span className="text-gray-500"> Two shadow portfolios will be created automatically to track performance over time.</span>
            )}
          </p>

          {confirming === "MANUAL_OVERRIDE" && (
            <div className="space-y-3 border border-gray-200 rounded-lg p-3 bg-gray-50">
              {/* Override Type */}
              <div>
                <p className="text-xs font-semibold text-gray-600 mb-1.5">Override Type</p>
                <div className="flex flex-wrap gap-2">
                  {([
                    { value: "REJECT_SWAP",        label: "Reject Swap" },
                    { value: "REPLACE_SYMBOL",     label: "Replace Symbol" },
                    { value: "INCREASE_CONVICTION",label: "Increase Conviction" },
                    { value: "REDUCE_CONVICTION",  label: "Reduce Conviction" },
                    { value: "HOLD_POSITION",      label: "Hold Position" },
                    { value: "CUSTOM",             label: "Custom" },
                  ] as { value: OverrideCategoryType; label: string }[]).map(({ value, label }) => (
                    <button
                      key={value}
                      type="button"
                      onClick={() => setOverrideType(v => v === value ? "" : value)}
                      className={`px-2.5 py-1 text-xs rounded-full border transition-colors ${
                        overrideType === value
                          ? "bg-gray-800 text-white border-gray-800"
                          : "border-gray-300 text-gray-600 hover:bg-gray-100"
                      }`}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Symbol fields */}
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide block mb-1">
                    Symbol Affected
                  </label>
                  <input
                    type="text"
                    value={originalSymbol}
                    onChange={(e) => setOriginalSymbol(e.target.value.toUpperCase())}
                    placeholder="e.g. KBANK"
                    className="w-full border border-gray-200 rounded-md px-2.5 py-1.5 text-xs font-mono bg-white focus:outline-none focus:ring-1 focus:ring-gray-400"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide block mb-1">
                    Replacement Symbol
                  </label>
                  <input
                    type="text"
                    value={replacementSymbol}
                    onChange={(e) => setReplacementSymbol(e.target.value.toUpperCase())}
                    placeholder="e.g. TOA (optional)"
                    className="w-full border border-gray-200 rounded-md px-2.5 py-1.5 text-xs font-mono bg-white focus:outline-none focus:ring-1 focus:ring-gray-400"
                  />
                </div>
              </div>
            </div>
          )}

          {(confirming === "MANUAL_OVERRIDE" || confirming === "APPROVED" || confirming === "PARTIAL_EXECUTION") && (
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder={confirming === "MANUAL_OVERRIDE" ? "Reason (required) — e.g. Higher conviction in TOA vs GUNKUL" : "Notes (optional) — e.g. partial fill, adjusted sizing…"}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-1 focus:ring-blue-400"
              rows={2}
            />
          )}

          {error && <p className="text-xs text-red-500">{error}</p>}

          <div className="flex gap-2">
            <button
              onClick={handleConfirm}
              disabled={submitting}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                confirming === "APPROVED"
                  ? "bg-green-600 text-white hover:bg-green-700"
                  : confirming === "REJECTED"
                  ? "bg-red-600 text-white hover:bg-red-700"
                  : "bg-blue-600 text-white hover:bg-blue-700"
              } disabled:opacity-50`}
            >
              {submitting ? "Saving…" : "Confirm"}
            </button>
            <button
              onClick={() => { setConfirming(null); setNotes(""); setOverrideType(""); setOriginalSymbol(""); setReplacementSymbol(""); setError(null); }}
              className="px-4 py-2 text-sm border rounded-lg text-gray-600 hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex gap-2 flex-wrap items-center">
          {(["APPROVED", "REJECTED", "MANUAL_OVERRIDE"] as ExecutionDecisionType[]).map((d) => {
            const cfg = DECISION_CFG[d];
            return (
              <button
                key={d}
                onClick={() => setConfirming(d)}
                className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${cfg.cls}`}
              >
                {cfg.icon} {cfg.label}
              </button>
            );
          })}
          <p className="text-xs text-gray-400 ml-1">
            Recording a decision activates shadow portfolio tracking.
          </p>
        </div>
      )}
    </section>
  );
}
