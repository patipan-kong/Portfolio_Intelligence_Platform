"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import {
  LegacyGoalProfileEvidence,
  type LegacyGoalProfileEvidenceState,
} from "@/components/goals/LegacyGoalProfileEvidence";
import {
  FundingSourcesSection,
  GoalSummary,
  GoalWhatIfSection,
  SavedScenariosSection,
  type GoalContextState,
  type ScenariosState,
  messageFor,
} from "@/components/goals/GoalPlanningSections";
import { FundingHistorySection, type FundingHistoryState } from "@/components/goals/FundingHistorySection";
import { PlanHistorySection, type PlanHistoryState } from "@/components/goals/PlanHistorySection";
import {
  GoalAffordabilitySection,
  type GoalAffordabilityEvidence,
} from "@/components/goals/GoalAffordabilitySection";
import { goalAffordabilityCalendar } from "@/lib/goalAffordability";
import type { CashAccountsFetchStatus } from "@/lib/emergencyFund";
import {
  sourceKey,
  factualReviewMatchesGoalContext,
  sourceFundingHealth,
  unavailableSourceFundingHealth,
  type FundingSourceKey,
  type SourceFundingHealth,
} from "@/lib/goalFunding";
import {
  createGoalScenario,
  getCashFlowReport,
  getLegacyGoalProfileEvidence,
  getWealthFactualReview,
  listCashAccounts,
  listGoalFundingAllocationHistory,
  listGoalPlanAmendmentHistory,
  listGoalScenarios,
  listPortfolios,
  listWealthGoals,
  type CashAccount,
  type FactualReviewResponse,
  type GoalContextGoal,
  type GoalFundingSourceKind,
  type LegacyGoalProfileEvidenceResponse,
  type GoalScenario,
  type Portfolio,
  type WealthGoal,
} from "@/lib/api";
import { formatThb, priorityLabel, typeLabel } from "@/components/goals/GoalPlanningSections";
import {
  evidenceEdgesForGoal,
  legacyEvidenceMatchesReferenceGoalContext,
} from "@/lib/legacyGoalProfileEvidence";

function goalRecordMatchesContext(record: WealthGoal, contextGoal: GoalContextGoal): boolean {
  return record.id === contextGoal.id
    && record.name === contextGoal.name
    && record.goal_type === contextGoal.goal_type
    && record.target_amount === contextGoal.target_amount
    && record.currency === contextGoal.currency
    && record.target_date === contextGoal.target_date
    && record.priority === contextGoal.priority
    && record.is_archived === contextGoal.is_archived
    && record.updated_at === contextGoal.updated_at;
}

export default function GoalDetailPage({ params }: { params: { id: string } }) {
  const goalId = Number(params.id);
  const activeGoalIdRef = useRef(goalId);
  const loadGenerationRef = useRef(0);
  const contextRefreshGenerationRef = useRef(0);
  activeGoalIdRef.current = goalId;
  const [goal, setGoal] = useState<WealthGoal | null>(null);
  const [allGoals, setAllGoals] = useState<WealthGoal[]>([]);
  const [factualReview, setFactualReview] = useState<FactualReviewResponse | { error: string } | undefined>(undefined);
  const [legacyEvidence, setLegacyEvidence] = useState<LegacyGoalProfileEvidenceResponse | { error: string } | undefined>(undefined);
  const [scenarios, setScenarios] = useState<ScenariosState>(undefined);
  const [fundingHistory, setFundingHistory] = useState<FundingHistoryState>(undefined);
  const [planHistory, setPlanHistory] = useState<PlanHistoryState>(undefined);
  // Lifted above GoalWhatIfSection so "Load scenario" can populate its
  // transient assumptions from the Saved Scenarios section.
  const [whatIfExpanded, setWhatIfExpanded] = useState(false);
  const [whatIfMode, setWhatIfMode] = useState<"forward" | "required">("forward");
  const [whatIfMonthlyContribution, setWhatIfMonthlyContribution] = useState("");
  const [whatIfAnnualReturnPct, setWhatIfAnnualReturnPct] = useState("0");
  const [cashAccounts, setCashAccounts] = useState<CashAccount[]>([]);
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [affordabilityEvidence, setAffordabilityEvidence] = useState<GoalAffordabilityEvidence | undefined>(undefined);
  // Fail closed until the cash-account list is known to have loaded: an
  // unknown population must never read as a measured absence of cash flow.
  const [cashAccountsStatus, setCashAccountsStatus] = useState<CashAccountsFetchStatus>("error");
  const [sourceLoadError, setSourceLoadError] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [errorGoalId, setErrorGoalId] = useState<number | null>(null);

  const load = useCallback(async () => {
    const generation = ++loadGenerationRef.current;
    const contextGeneration = ++contextRefreshGenerationRef.current;
    const isCurrentLoad = () => loadGenerationRef.current === generation && activeGoalIdRef.current === goalId;
    const isCurrentEvidenceLoad = () => isCurrentLoad()
      && contextRefreshGenerationRef.current === contextGeneration;
    setLoading(true);
    setError("");
    setErrorGoalId(null);
    setGoal(null);
    setFactualReview(undefined);
    setLegacyEvidence(undefined);
    setCashAccounts([]);
    setPortfolios([]);
    setAffordabilityEvidence(undefined);
    setCashAccountsStatus("error");
    setSourceLoadError("");
    setScenarios(undefined);
    setFundingHistory(undefined);
    setPlanHistory(undefined);
    setWhatIfExpanded(false);
    setWhatIfMode("forward");
    setWhatIfMonthlyContribution("");
    setWhatIfAnnualReturnPct("0");

    if (!Number.isInteger(goalId) || goalId <= 0) {
      setError("Goal not found.");
      setErrorGoalId(goalId);
      setLoading(false);
      return;
    }

    try {
      // WealthGoal records remain the editable metadata source. The workspace
      // Factual review owns the accepted Goal Context used by this page. The
      // supplemental legacy response embeds another copy that must agree
      // structurally before any legacy evidence is rendered.
      void Promise.resolve()
        .then(() => getLegacyGoalProfileEvidence(true))
        .then(
          (result) => {
            if (isCurrentEvidenceLoad()) setLegacyEvidence(result);
          },
          () => {
            if (isCurrentEvidenceLoad()) {
              setLegacyEvidence({ error: "Legacy Portfolio goal-profile evidence is unavailable." });
            }
          },
        );
      // Goal Affordability Bridge: fetch the trailing 3 completed calendar
      // months of Cash Flow (current month never participates). Runs
      // independently of the goal load so a slow or failed Cash Flow
      // fetch never blocks or fails rendering of the Goal itself — a
      // failed month is recorded as "error", which fails the assessment
      // closed rather than silently narrowing the sample or reading as zero.
      void (() => {
        // One calendar anchor for the whole feature: the months requested
        // here are exactly the months the helper evaluates, and the as-of
        // date used for the required side comes from the same instant on the
        // same local calendar. Nothing downstream reads a second clock.
        const calendar = goalAffordabilityCalendar(new Date());
        const trailingMonths = calendar.trailingCompletedMonths;
        return Promise.allSettled(trailingMonths.map((month) => getCashFlowReport(month))).then((settled) => {
          if (!isCurrentLoad()) return;
          setAffordabilityEvidence({
            calendar,
            monthlyCashFlowResults: trailingMonths.map((month, index) => {
              const outcome = settled[index];
              return outcome.status === "fulfilled"
                ? { month, status: "success" as const, events: outcome.value.events }
                : { month, status: "error" as const, events: [] };
            }),
          });
        });
      })();
      const [goalsResult, contextResult] = await Promise.allSettled([
        listWealthGoals(true),
        getWealthFactualReview(true),
      ]);
      if (!isCurrentLoad()) return;
      if (goalsResult.status === "rejected") throw goalsResult.reason;

      const goals = goalsResult.value;
      const selectedGoal = goals.find((item) => item.id === goalId);
      setAllGoals(goals);
      if (!selectedGoal) {
        setError("Goal not found.");
        setErrorGoalId(goalId);
        return;
      }

      setGoal(selectedGoal);
      // Funding history is supplementary evidence. Its request intentionally
      // does not participate in the Goal Detail load, so a failure cannot
      // block current funding, planning, or factual-review state.
      void Promise.resolve()
        .then(() => listGoalFundingAllocationHistory(goalId))
        .then(
          (result) => {
            if (isCurrentLoad()) setFundingHistory(result);
          },
          (err) => {
            if (isCurrentLoad()) setFundingHistory({ error: messageFor(err, "Unable to load funding history.") });
          },
        );
      // Plan history is documentary evidence only. Like funding history, it
      // must never block the authoritative current-goal and review surfaces.
      void Promise.resolve()
        .then(() => listGoalPlanAmendmentHistory(goalId))
        .then(
          (result) => {
            if (isCurrentLoad()) setPlanHistory(result);
          },
          (err) => {
            if (isCurrentLoad()) setPlanHistory({ error: messageFor(err, "Unable to load plan history.") });
          },
        );
      setFactualReview(contextResult.status === "fulfilled"
        ? contextResult.value
        : { error: messageFor(contextResult.reason, "Unable to load factual wealth review.") });

      const [cashResult, portfolioResult, scenariosResult] = await Promise.allSettled([
        listCashAccounts(false),
        listPortfolios(),
        listGoalScenarios(goalId, true),
      ]);
      if (!isCurrentLoad()) return;
      setCashAccounts(cashResult.status === "fulfilled" ? cashResult.value : []);
      setCashAccountsStatus(cashResult.status === "fulfilled" ? "success" : "error");
      setPortfolios(portfolioResult.status === "fulfilled" ? portfolioResult.value : []);
      if (cashResult.status === "rejected" || portfolioResult.status === "rejected") {
        setSourceLoadError("Some funding source catalogs could not be loaded; allocation editing may be limited.");
      }
      setScenarios(scenariosResult.status === "fulfilled"
        ? scenariosResult.value
        : { error: messageFor(scenariosResult.reason, "Unable to load saved scenarios.") });
    } catch (err) {
      if (!isCurrentLoad()) return;
      setError(messageFor(err, "Unable to load goal."));
      setErrorGoalId(goalId);
      setGoal(null);
    } finally {
      if (isCurrentLoad()) setLoading(false);
    }
  }, [goalId]);

  useEffect(() => {
    void load();
  }, [load]);

  const reviewResponse = factualReview && "goal_context" in factualReview ? factualReview : null;
  const contextResponse = reviewResponse?.goal_context ?? null;
  const contextGoal = contextResponse?.goals.find((candidate) => candidate.id === goalId);
  const contextMatchesGoals = contextResponse !== null
    && reviewResponse?.contract_version === "wealth.factual-review.v1"
    && reviewResponse.scope.kind === "WORKSPACE"
    && reviewResponse.scope.include_archived === true
    && factualReviewMatchesGoalContext(reviewResponse)
    && contextResponse.contract_version === "wealth.goal-context.v1"
    && contextResponse.completeness === "COMPLETE"
    && contextResponse.scope.kind === "WORKSPACE"
    && contextResponse.scope.include_archived === true
    && contextResponse.goals.length === allGoals.length
    && allGoals.every((candidate) => {
      const contextCandidate = contextResponse.goals.find((contextGoal) => contextGoal.id === candidate.id);
      return contextCandidate !== undefined && goalRecordMatchesContext(candidate, contextCandidate);
    });
  const selectedGoalContext: GoalContextState = factualReview === undefined
    ? undefined
    : factualReview && "error" in factualReview
      ? factualReview
      : contextMatchesGoals && contextGoal
        ? contextGoal
        : { error: "Goal Context is unavailable for this goal." };

  const selectedLegacyEvidence: LegacyGoalProfileEvidenceState = legacyEvidence === undefined
    ? undefined
    : "error" in legacyEvidence
      ? legacyEvidence
      : factualReview === undefined
        ? undefined
        : contextMatchesGoals && contextResponse
          && legacyEvidence.scope.kind === "WORKSPACE"
          && legacyEvidence.scope.include_archived === true
          && legacyEvidenceMatchesReferenceGoalContext(legacyEvidence, contextResponse)
          ? evidenceEdgesForGoal(legacyEvidence, goalId) ?? { error: "Legacy Portfolio goal-profile evidence is unavailable because its Goal Context is inconsistent." }
          : { error: "Legacy Portfolio goal-profile evidence is unavailable because its Goal Context is inconsistent." };

  const factualSourceByKey = useMemo(() => {
    const sources = new Map<FundingSourceKey, FactualReviewResponse["sources"][number]>();
    if (contextMatchesGoals) {
      for (const source of reviewResponse?.sources ?? []) {
        sources.set(sourceKey(source.source_kind, source.source_id), source);
      }
    }
    return sources;
  }, [contextMatchesGoals, reviewResponse]);

  const selectedFactualSources = useMemo(() => {
    if (!contextGoal || !contextMatchesGoals) return [];
    const keys = new Set(contextGoal.allocations.map((allocation) => sourceKey(allocation.source_kind, allocation.source_id)));
    return [...factualSourceByKey.entries()]
      .filter(([key]) => keys.has(key))
      .map(([, source]) => source);
  }, [contextGoal, contextMatchesGoals, factualSourceByKey]);

  function fundingHealthForSource(kind: GoalFundingSourceKind, id: number): SourceFundingHealth {
    // A missing or mismatched Goal Context means the cross-goal total is not
    // known. Keep the health claim unavailable instead of treating it as 0.
    if (!contextMatchesGoals || !contextGoal || !contextResponse) return unavailableSourceFundingHealth();
    const source = factualSourceByKey.get(sourceKey(kind, id));
    return source ? sourceFundingHealth(source) : unavailableSourceFundingHealth();
  }

  const reloadGoalContext = useCallback(async () => {
    if (!Number.isInteger(goalId) || goalId <= 0) return;
    const generation = loadGenerationRef.current;
    const contextGeneration = ++contextRefreshGenerationRef.current;
    const isCurrentRefresh = () => loadGenerationRef.current === generation
      && contextRefreshGenerationRef.current === contextGeneration
      && activeGoalIdRef.current === goalId;
    setFactualReview(undefined);
    setLegacyEvidence(undefined);
    void Promise.resolve()
      .then(() => getLegacyGoalProfileEvidence(true))
      .then(
        (result) => {
          if (isCurrentRefresh()) setLegacyEvidence(result);
        },
        () => {
          if (isCurrentRefresh()) {
            setLegacyEvidence({ error: "Legacy Portfolio goal-profile evidence is unavailable." });
          }
        },
      );
    try {
      const result = await getWealthFactualReview(true);
      if (!isCurrentRefresh()) return;
      setFactualReview(result);
    } catch (err) {
      if (!isCurrentRefresh()) return;
      setFactualReview({ error: messageFor(err, "Unable to refresh factual wealth review.") });
    }
  }, [goalId]);

  const reloadScenarios = useCallback(async () => {
    if (!Number.isInteger(goalId) || goalId <= 0) return;
    try {
      const result = await listGoalScenarios(goalId, true);
      if (activeGoalIdRef.current !== goalId) return;
      setScenarios(result);
    } catch (err) {
      if (activeGoalIdRef.current !== goalId) return;
      setScenarios({ error: messageFor(err, "Unable to load saved scenarios.") });
    }
  }, [goalId]);

  const reloadFundingHistory = useCallback(async () => {
    if (!Number.isInteger(goalId) || goalId <= 0) return;
    setFundingHistory(undefined);
    try {
      const result = await listGoalFundingAllocationHistory(goalId);
      if (activeGoalIdRef.current === goalId) setFundingHistory(result);
    } catch (err) {
      if (activeGoalIdRef.current === goalId) {
        setFundingHistory({ error: messageFor(err, "Unable to load funding history.") });
      }
    }
  }, [goalId]);

  const handleLoadScenario = useCallback((scenario: GoalScenario) => {
    setWhatIfExpanded(true);
    setWhatIfMode("forward");
    setWhatIfMonthlyContribution(String(scenario.monthly_contribution));
    setWhatIfAnnualReturnPct(String(scenario.annual_return_pct));
  }, []);

  const handleSaveScenario = useCallback(async (monthlyContribution: number, annualReturnPct: number, name: string) => {
    await createGoalScenario(goalId, { name, monthly_contribution: monthlyContribution, annual_return_pct: annualReturnPct });
    await reloadScenarios();
  }, [goalId, reloadScenarios]);

  // Next can reuse this client component while the dynamic URL changes. Do
  // not briefly render the previous goal under the new URL while its effect
  // starts, and never let its asynchronous reads replace the new route.
  const currentGoal = goal?.id === goalId ? goal : null;
  const currentError = errorGoalId === goalId ? error : "";

  return (
    <main className="space-y-6 max-w-4xl">
      <Link href="/goals" className="text-sm text-blue-600 hover:underline">← Back to goals</Link>

      {(loading || (!currentGoal && !currentError)) && <p className="text-sm text-gray-400">Loading goal…</p>}

      {!loading && currentError && (
        <div className="space-y-2">
          <p role="alert" className="text-sm text-red-600">{currentError}</p>
          <button type="button" onClick={() => void load()} className="text-sm text-blue-600 hover:underline">Try again</button>
        </div>
      )}

      {!loading && !currentError && currentGoal && (
        <article className="space-y-5">
          <header className="border-b pb-4">
            <p className="text-xs uppercase tracking-wide text-gray-400">Goal plan</p>
            <h1 className="text-2xl font-bold">{currentGoal.name}</h1>
            <p className="text-sm text-gray-500 mt-1">{typeLabel(currentGoal.goal_type)} · {priorityLabel(currentGoal.priority)} priority · {currentGoal.is_archived ? "Archived" : "Active"}</p>
            {sourceLoadError && <p className="text-xs text-gray-500 mt-2">{sourceLoadError}</p>}
          </header>

          <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="goal-summary-heading">
            <h2 id="goal-summary-heading" className="text-lg font-semibold">Goal Summary</h2>
            <GoalSummary item={currentGoal} goalContext={selectedGoalContext} />
          </section>

          <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="funding-heading">
            <h2 id="funding-heading" className="text-lg font-semibold">Funding</h2>
            <FundingSourcesSection
              key={currentGoal.id}
              goalId={currentGoal.id}
              readOnly={currentGoal.is_archived}
              cashAccounts={cashAccounts}
              portfolios={portfolios}
              goalContext={selectedGoalContext}
              onReload={async () => {
                await reloadGoalContext();
                void reloadFundingHistory();
              }}
              fundingHealthForSource={fundingHealthForSource}
            />
            <FactualValuationEvidence sources={selectedFactualSources} />
            <LegacyGoalProfileEvidence state={selectedLegacyEvidence} />
          </section>

          <FundingHistorySection state={fundingHistory} />

          <PlanHistorySection state={planHistory} />

          <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="planning-heading">
            <h2 id="planning-heading" className="text-lg font-semibold">Planning / What-If</h2>
            <GoalWhatIfSection
              item={currentGoal}
              goalContext={selectedGoalContext}
              fundingHealthForSource={fundingHealthForSource}
              readOnly={currentGoal.is_archived}
              onSaveScenario={handleSaveScenario}
              whatIf={{
                expanded: whatIfExpanded,
                setExpanded: setWhatIfExpanded,
                mode: whatIfMode,
                setMode: setWhatIfMode,
                monthlyContribution: whatIfMonthlyContribution,
                setMonthlyContribution: setWhatIfMonthlyContribution,
                annualReturnPct: whatIfAnnualReturnPct,
                setAnnualReturnPct: setWhatIfAnnualReturnPct,
              }}
            />
            {!currentGoal.is_archived && (
              <GoalAffordabilitySection
                goalContext={selectedGoalContext}
                evidence={affordabilityEvidence}
                cashAccountsStatus={cashAccountsStatus}
                cashAccounts={cashAccounts}
              />
            )}
          </section>

          <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="saved-scenarios-heading">
            <h2 id="saved-scenarios-heading" className="text-lg font-semibold">Saved Scenarios</h2>
            <SavedScenariosSection
              key={currentGoal.id}
              goalId={currentGoal.id}
              item={currentGoal}
              goalContext={selectedGoalContext}
              fundingHealthForSource={fundingHealthForSource}
              readOnly={currentGoal.is_archived}
              scenarios={scenarios}
              onReload={reloadScenarios}
              onLoadScenario={handleLoadScenario}
            />
          </section>
        </article>
      )}
    </main>
  );
}

function FactualValuationEvidence({ sources }: { sources: FactualReviewResponse["sources"] }) {
  if (sources.length === 0) return null;
  return (
    <div className="pt-3 border-t space-y-1" aria-label="Factual valuation evidence">
      <h3 className="text-sm font-semibold text-gray-700">Valuation evidence</h3>
      {sources.map((source) => (
        <p key={sourceKey(source.source_kind, source.source_id)} className="text-xs text-gray-500">
          {source.source_name}{source.source_is_archived ? " (archived)" : ""}: {source.valuation.observed_value === null
            ? "observed value unavailable"
            : `${formatThb(source.valuation.observed_value)} observed`}
          {source.valuation.provenance ? ` · ${source.valuation.provenance}` : ""}
          {source.valuation.as_of ? ` · as of ${source.valuation.as_of}` : ""}
          {source.valuation.quality ? ` · quality ${source.valuation.quality}` : ""}
        </p>
      ))}
    </div>
  );
}
