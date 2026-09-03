"use client";

// AI Evaluation M4 — S3 Recommendation Report Card
// (`/ai-analytics/recommendations/{id}`). Three sections in pipeline order —
// plan -> execution -> outcome — matching the three lenses (§12). Renders
// GET /analytics/evaluation/recommendations/{id} verbatim; no section
// recomputes anything the backend already delivered.

import { useCallback, useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { usePortfolio } from "@/lib/PortfolioContext";
import { getRecommendationReportCard, isUnresolvedPortfolioError, type RecommendationReportCard, type ExecutionAnalysis, type DecisionGoalContextGoal } from "@/lib/api";
import BackBreadcrumb from "@/components/BackBreadcrumb";
import PortfolioSelectionNotice from "@/components/PortfolioSelectionNotice";
import VerdictSentence from "@/components/evaluation/VerdictSentence";
import DecisionStatusBadge from "@/components/evaluation/DecisionStatusBadge";
import HorizonStrip from "@/components/evaluation/HorizonStrip";
import AsOfStamp from "@/components/evaluation/AsOfStamp";

function pct(n: number | null | undefined, decimals = 1): string {
  if (n == null) return "—";
  return `${n >= 0 ? "+" : ""}${n.toFixed(decimals)}%`;
}
function pnlTone(n: number | null | undefined): string {
  if (n == null) return "text-gray-400";
  return n >= 0 ? "text-green-700" : "text-red-600";
}
function money(n: number | null | undefined): string {
  if (n == null) return "—";
  return `฿${Math.abs(n).toLocaleString("th-TH")}`;
}

function SectionCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-4 py-2.5 border-b border-gray-100 bg-gray-50/60">
        <h2 className="text-xs font-bold text-gray-600 uppercase tracking-wide">{title}</h2>
      </div>
      <div className="p-4 space-y-3">{children}</div>
    </div>
  );
}

function PlanSection({ plan }: { plan: RecommendationReportCard["plan"] }) {
  if (plan.status === "unavailable") {
    return <p className="text-sm text-gray-400 italic">Plan unavailable — {plan.reason ?? "no stored plan inputs for this snapshot"}.</p>;
  }
  const [breakdownOpen, setBreakdownOpen] = useState(false);
  const buys = plan.buy_trades ?? [];
  const sells = (plan.sell_reduce_trades ?? []) as Array<Record<string, unknown>>;

  return (
    <>
      {plan.no_action_summary && <p className="text-sm text-gray-700">{plan.no_action_summary}</p>}
      {plan.portfolio_assessment && <p className="text-xs text-gray-500">{plan.portfolio_assessment}</p>}

      {buys.length > 0 && (
        <div className="space-y-1">
          {buys.map((t, i) => (
            <div key={i} className="flex items-center gap-2 text-sm">
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-green-100 text-green-700 border border-green-200">
                {String(t.action)}
              </span>
              <span className="font-semibold text-gray-800">{String(t.symbol).replace(".BK", "")}</span>
              <span className="text-gray-500">{money(t.planned_amount as number)}</span>
            </div>
          ))}
        </div>
      )}

      {sells.length > 0 && (
        <div className="space-y-1">
          {sells.map((t, i) => {
            const necessity = String(t.necessity ?? "");
            const state = String(t.execution_state ?? "");
            const deferred = state === "DEFERRED";
            return (
              <div key={i} className="flex items-center gap-2 text-sm flex-wrap">
                <span
                  className={`text-[10px] font-bold px-1.5 py-0.5 rounded border ${
                    necessity === "NECESSARY" ? "bg-gray-800 text-white border-gray-800" : "bg-amber-50 text-amber-700 border-amber-300"
                  }`}
                >
                  {String(t.action)}
                </span>
                <span className={`font-semibold ${deferred ? "text-gray-400" : "text-gray-800"}`}>
                  {String(t.symbol).replace(".BK", "")}
                </span>
                <span className="text-xs text-gray-400">
                  Reason: {String(t.reason ?? "—").replace(/_/g, " ").toLowerCase()}
                  {deferred ? " · deferred" : ""}
                </span>
                {Boolean(t.note) && <span className="text-xs text-gray-400 italic">— {String(t.note)}</span>}
              </div>
            );
          })}
        </div>
      )}

      <div className="flex flex-wrap gap-x-6 gap-y-1 text-xs text-gray-500 pt-1 border-t">
        <span>Cash available: <strong className="text-gray-700">{money(plan.cash_available)}</strong></span>
        <span>Funding gap: <strong className="text-gray-700">{money(plan.funding_gap)}</strong></span>
      </div>

      {plan.grade && (
        <div className="pt-2 border-t">
          <div className="flex items-center justify-between">
            <p className="text-sm">
              Plan grade (day 0): <strong className="text-gray-800">{plan.grade.score != null ? `${plan.grade.score.toFixed(0)}/100` : "—"}</strong>
            </p>
            {plan.grade.detail && (
              <button onClick={() => setBreakdownOpen((v) => !v)} className="text-xs text-blue-600 hover:underline">
                {breakdownOpen ? "hide breakdown ▴" : "breakdown ▾"}
              </button>
            )}
          </div>
          {breakdownOpen && plan.grade.detail && (
            <div className="mt-2 grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs text-gray-600 bg-gray-50 rounded-lg p-3">
              {Object.entries(plan.grade.detail)
                .filter(([k]) => k.endsWith("_score") || k === "weights")
                .map(([k, v]) => (
                  <div key={k}>
                    <p className="text-gray-400">{k.replace(/_/g, " ")}</p>
                    <p className="font-semibold text-gray-700">{typeof v === "number" ? v.toFixed(0) : JSON.stringify(v)}</p>
                  </div>
                ))}
            </div>
          )}
        </div>
      )}
    </>
  );
}

// Historical timestamp semantics (Slice 3 finding, reconfirmed Slice 4 §H):
// UserExecutionDecision.executed_at is the decision-row creation timestamp,
// not a trade-fill time — never label it "executed".
function decisionRecordedLabel(iso: string): string {
  return `decision recorded ${iso.slice(0, 10)}`;
}

function formatGoalTargetDate(targetDate: string | null): string | null {
  if (!targetDate) return null;
  const d = new Date(targetDate);
  if (Number.isNaN(d.getTime())) return null;
  return d.toLocaleDateString("en-GB", { month: "short", year: "numeric" });
}

function formatGoalPriority(priority: string): string {
  return priority.charAt(0) + priority.slice(1).toLowerCase();
}

// Rationale chips (Slice 4 §F) — read-only display of fields already
// persisted on UserExecutionDecision (UX.2D). Renders nothing for a null
// field rather than an empty label/placeholder.
function DecisionRationale({ execution }: { execution: RecommendationReportCard["execution"] }) {
  const hasRationale =
    execution.override_type || execution.original_symbol || execution.reason_category || execution.override_notes;
  if (!hasRationale) return null;
  return (
    <div className="flex flex-wrap items-center gap-2 text-xs">
      {execution.override_type && (
        <span className="px-2 py-0.5 rounded-full border border-gray-200 bg-gray-50 text-gray-600 font-medium">
          {execution.override_type.replace(/_/g, " ")}
        </span>
      )}
      {execution.reason_category && (
        <span className="px-2 py-0.5 rounded-full border border-gray-200 bg-gray-50 text-gray-600 font-medium">
          {execution.reason_category.replace(/_/g, " ")}
        </span>
      )}
      {execution.original_symbol && (
        <span className="text-gray-500 font-mono">
          {execution.original_symbol}
          {execution.replacement_symbol && ` → ${execution.replacement_symbol}`}
        </span>
      )}
      {execution.override_notes && <span className="text-gray-500 italic">&ldquo;{execution.override_notes}&rdquo;</span>}
    </div>
  );
}

// Goal context at time of decision (Slice 4 §G; Phase 7.4/ADR-008,
// CONTEXT_ONLY) — frozen historical evidence from RecommendationSnapshot,
// never causal. Omits cleanly when absent/EMPTY, matching
// DecisionActionPanel's existing GoalContextAtDecisionTime treatment.
function GoalContextAtDecisionTime({ goalContext }: { goalContext: RecommendationReportCard["execution"]["goal_context"] }) {
  if (!goalContext || goalContext.context_state !== "COMPLETE" || goalContext.goals.length === 0) return null;
  return (
    <div className="pt-2 border-t border-gray-100 space-y-1">
      <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Goal context at time of decision</p>
      {goalContext.goals.map((g: DecisionGoalContextGoal) => {
        const targetDate = formatGoalTargetDate(g.target_date);
        return (
          <div key={g.id} className="text-xs">
            <span className="font-semibold text-gray-700">{g.name}</span>
            <span className="text-gray-500">
              {" — "}฿{g.target_amount.toLocaleString("th-TH")} target
              {targetDate ? ` · ${targetDate}` : ""}
              {" · "}{g.progress_percent.toFixed(0)}% funded
              {" · "}{formatGoalPriority(g.priority)} priority
            </span>
          </div>
        );
      })}
    </div>
  );
}

function ExecutionSection({ execution, decision }: { execution: RecommendationReportCard["execution"]; decision: RecommendationReportCard["decision"] }) {
  if (execution.status === "no_decision_recorded") {
    return <p className="text-sm text-gray-400 italic">No decision recorded yet for this recommendation.</p>;
  }
  const analysis = execution.analysis as ExecutionAnalysis | undefined;
  return (
    <>
      <div className="flex items-center gap-2 flex-wrap text-sm">
        <span className="text-gray-500">Your decision:</span>
        <DecisionStatusBadge decision={execution.decision} />
        {execution.executed_at && <span className="text-gray-400 text-xs">{decisionRecordedLabel(execution.executed_at)}</span>}
        {decision?.is_system_generated && <span className="text-xs text-gray-400 italic">(system-generated)</span>}
        {execution.decision_id != null && (
          <Link
            href={`/ai-analytics/execution/${execution.decision_id}`}
            className="text-xs font-semibold text-blue-600 hover:underline ml-auto"
          >
            View full execution detail →
          </Link>
        )}
      </div>

      <DecisionRationale execution={execution} />
      <GoalContextAtDecisionTime goalContext={execution.goal_context} />

      {analysis && (
        analysis.status === "unavailable" ? (
          <p className="text-sm text-gray-400 italic">Execution analysis unavailable — {analysis.reason ?? "no linked transactions"}.</p>
        ) : (
          <>
            <div className="flex flex-wrap gap-x-6 gap-y-1 text-xs text-gray-500">
              <span>Execution score: <strong className="text-gray-700">{analysis.score != null ? analysis.score.toFixed(0) : "—"}</strong></span>
              <span>Completeness: <strong className="text-gray-700">{analysis.completeness_pct != null ? `${analysis.completeness_pct.toFixed(0)}%` : "—"}</strong></span>
              <span>Funding fidelity: <strong className="text-gray-700">{analysis.funding_fidelity_pct != null ? `${analysis.funding_fidelity_pct.toFixed(0)}%` : "n/a"}</strong></span>
              {analysis.status === "partial" && <span className="text-amber-600 font-semibold">⚠ partial execution</span>}
            </div>
            {Object.keys(analysis.symbols ?? {}).length > 0 && (
              <div className="space-y-1 pt-1">
                {Object.entries(analysis.symbols ?? {}).map(([sym, d]) => (
                  <div key={sym} className="flex items-center gap-3 text-xs text-gray-600 flex-wrap">
                    <span className="font-semibold text-gray-800 w-16">{sym.replace(".BK", "")}</span>
                    <span>Timing: {d.timing_delta_pct != null ? pct(d.timing_delta_pct) : "not measurable"}</span>
                    <span>Size: {d.size_delta_pct != null ? pct(d.size_delta_pct, 0) : "not measurable"}</span>
                    {d.note && <span className="text-gray-400 italic">{d.note}</span>}
                  </div>
                ))}
              </div>
            )}
          </>
        )
      )}
    </>
  );
}

function OutcomeSection({ outcomes }: { outcomes: RecommendationReportCard["outcomes"] }) {
  return (
    <div className="space-y-2">
      <HorizonStrip strip={outcomes} />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs text-gray-500 pt-1">
        {Object.entries(outcomes).map(([kind, cell]) => (
          <div key={kind}>
            <p className="text-gray-400">{kind}</p>
            {cell.status === "graded" ? (
              <p>
                <span className={`font-semibold ${pnlTone(cell.return_pct)}`}>{pct(cell.return_pct)}</span>{" "}
                vs {pct(cell.benchmark_return_pct)}
                {cell.alpha != null && <span className="block text-gray-400">alpha {pct(cell.alpha)}</span>}
              </p>
            ) : (
              <p className="text-gray-400">{cell.status === "maturing" ? `grades ${cell.due_date}` : "pending grading"}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default function ReportCardPage() {
  const params = useParams();
  const snapshotId = Number(params?.id);
  const { currentSelection, reportUnresolvedPortfolio } = usePortfolio();
  const portfolioId = currentSelection;

  const [data, setData] = useState<RecommendationReportCard | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // M36.1 WP4C F04 — captured Portfolio Identity; a response arriving after
  // Current Selection has moved to a different portfolio (or cleared to
  // NONE) is discarded instead of repopulating the page.
  const requestIdRef = useRef<number | null>(null);

  const load = useCallback(async () => {
    if (portfolioId == null || !snapshotId) return;
    const pid = portfolioId;
    setLoading(true);
    setError(null);
    try {
      const result = await getRecommendationReportCard(pid, snapshotId);
      if (requestIdRef.current !== pid) return;
      setData(result);
    } catch (e) {
      if (requestIdRef.current !== pid) return;
      setError(e instanceof Error ? e.message : "Failed to load report card");
      if (isUnresolvedPortfolioError(e)) reportUnresolvedPortfolio(pid);
    } finally {
      if (requestIdRef.current === pid) setLoading(false);
    }
  }, [portfolioId, snapshotId, reportUnresolvedPortfolio]);

  useEffect(() => {
    requestIdRef.current = portfolioId;
    if (portfolioId == null) {
      setData(null);
      setError(null);
      setLoading(false);
      return;
    }
    load();
  }, [portfolioId, load]);

  if (portfolioId == null) {
    return <PortfolioSelectionNotice label="this Recommendation Report Card" />;
  }

  return (
    <div className="space-y-4">
      <BackBreadcrumb parent="Recommendations" current={`#${snapshotId}`} href="/ai-analytics/recommendations" />

      {error && <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">{error}</div>}

      {loading && !data && (
        <div className="space-y-3">
          {[0, 1, 2].map((i) => (
            <div key={i} className="h-32 animate-pulse bg-gray-100 rounded-xl" />
          ))}
        </div>
      )}

      {!loading && !data && !error && <p className="text-sm text-gray-400 py-10 text-center">Recommendation not found.</p>}

      {data && (
        <>
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Rec #{data.snapshot_id} · {data.date?.slice(0, 10) ?? "—"}
              </h1>
              <p className="text-sm text-gray-500 mt-0.5">
                {data.consensus_type ?? "—"}
                {data.regime && ` · ${data.regime}`}
                {data.persona && ` · ${data.persona}`}
                {data.confidence != null && ` · Confidence ${data.confidence.toFixed(0)}%`}
              </p>
            </div>
            <AsOfStamp asOf={data.as_of} />
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
            <VerdictSentence verdict={data.verdict} />
          </div>

          <SectionCard title="1 · The Plan (immutable record)">
            <PlanSection plan={data.plan} />
          </SectionCard>

          <SectionCard title="2 · What Happened">
            <ExecutionSection execution={data.execution} decision={data.decision} />
          </SectionCard>

          <SectionCard title="3 · Outcome (frozen shadow vs benchmark)">
            <OutcomeSection outcomes={data.outcomes} />
          </SectionCard>
        </>
      )}
    </div>
  );
}
