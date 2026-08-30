"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import {
  FundingSourcesSection,
  GoalSummary,
  GoalWhatIfSection,
  SavedScenariosSection,
  type GoalContextState,
  type ScenariosState,
  messageFor,
} from "@/components/goals/GoalPlanningSections";
import {
  computeSourceFundingHealth,
  sourceKey,
  type SourceFundingHealth,
} from "@/lib/goalFunding";
import { computePortfolioCurrentValue } from "@/lib/wealthOverview";
import {
  createGoalScenario,
  getWealthGoalsContext,
  getHoldings,
  getPortfolioPrices,
  listCashAccounts,
  listGoalScenarios,
  listPortfolios,
  listWealthGoals,
  type CashAccount,
  type GoalContextGoal,
  type GoalContextResponse,
  type GoalFundingSourceKind,
  type GoalScenario,
  type Portfolio,
  type WealthGoal,
} from "@/lib/api";
import { priorityLabel, typeLabel } from "@/components/goals/GoalPlanningSections";

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
  const [goalContext, setGoalContext] = useState<GoalContextResponse | { error: string } | undefined>(undefined);
  const [scenarios, setScenarios] = useState<ScenariosState>(undefined);
  // Lifted above GoalWhatIfSection so "Load scenario" can populate its
  // transient assumptions from the Saved Scenarios section.
  const [whatIfExpanded, setWhatIfExpanded] = useState(false);
  const [whatIfMode, setWhatIfMode] = useState<"forward" | "required">("forward");
  const [whatIfMonthlyContribution, setWhatIfMonthlyContribution] = useState("");
  const [whatIfAnnualReturnPct, setWhatIfAnnualReturnPct] = useState("0");
  const [cashAccounts, setCashAccounts] = useState<CashAccount[]>([]);
  const [allCashAccounts, setAllCashAccounts] = useState<CashAccount[]>([]);
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [portfolioValueById, setPortfolioValueById] = useState<Record<number, number | "error" | undefined>>({});
  const [sourceLoadError, setSourceLoadError] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [errorGoalId, setErrorGoalId] = useState<number | null>(null);

  const load = useCallback(async () => {
    const generation = ++loadGenerationRef.current;
    contextRefreshGenerationRef.current += 1;
    const isCurrentLoad = () => loadGenerationRef.current === generation && activeGoalIdRef.current === goalId;
    setLoading(true);
    setError("");
    setErrorGoalId(null);
    setGoal(null);
    setGoalContext(undefined);
    setPortfolioValueById({});
    setSourceLoadError("");
    setScenarios(undefined);
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
      // Goal Context is fetched once and is the canonical source for the
      // selected goal's allocations/derived facts and cross-goal aggregates.
      const [goalsResult, contextResult] = await Promise.allSettled([
        listWealthGoals(true),
        getWealthGoalsContext(true),
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
      setGoalContext(contextResult.status === "fulfilled"
        ? contextResult.value
        : { error: messageFor(contextResult.reason, "Unable to load Goal Context.") });

      const [cashResult, allCashResult, portfolioResult, scenariosResult] = await Promise.allSettled([
        listCashAccounts(false),
        listCashAccounts(true),
        listPortfolios(),
        listGoalScenarios(goalId, true),
      ]);
      if (!isCurrentLoad()) return;
      if (cashResult.status === "fulfilled") setCashAccounts(cashResult.value);
      if (allCashResult.status === "fulfilled") setAllCashAccounts(allCashResult.value);
      if (portfolioResult.status === "fulfilled") setPortfolios(portfolioResult.value);
      if (cashResult.status === "rejected" || allCashResult.status === "rejected" || portfolioResult.status === "rejected") {
        setSourceLoadError("Some funding source data could not be loaded; affected Funding Health is unavailable.");
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

  const contextResponse = goalContext && "goals" in goalContext ? goalContext : null;
  const contextGoal = contextResponse?.goals.find((candidate) => candidate.id === goalId);
  const contextMatchesGoals = contextResponse !== null
    && contextResponse.contract_version === "wealth.goal-context.v1"
    && contextResponse.completeness === "COMPLETE"
    && contextResponse.scope.kind === "WORKSPACE"
    && contextResponse.scope.include_archived === true
    && contextResponse.goals.length === allGoals.length
    && allGoals.every((candidate) => {
      const contextCandidate = contextResponse.goals.find((contextGoal) => contextGoal.id === candidate.id);
      return contextCandidate !== undefined && goalRecordMatchesContext(candidate, contextCandidate);
    });
  const selectedGoalContext: GoalContextState = goalContext === undefined
    ? undefined
    : goalContext && "error" in goalContext
      ? goalContext
      : contextMatchesGoals && contextGoal
        ? contextGoal
        : { error: "Goal Context is unavailable for this goal." };

  const referencedPortfolioIds = useMemo(() => {
    const ids = new Set<number>();
    for (const designation of contextResponse?.designation_by_source ?? []) {
      if (designation.source_kind === "PORTFOLIO") ids.add(designation.source_id);
    }
    return ids;
  }, [contextResponse]);

  useEffect(() => {
    let cancelled = false;
    if (!contextMatchesGoals || !contextGoal || !contextResponse) return () => { cancelled = true; };
    for (const portfolioId of referencedPortfolioIds) {
      if (portfolioValueById[portfolioId] !== undefined) continue;
      const portfolio = portfolios.find((item) => item.id === portfolioId);
      if (!portfolio) continue;
      void (async () => {
        try {
          const [items, prices] = await Promise.all([getHoldings(portfolioId), getPortfolioPrices(portfolioId)]);
          if (cancelled) return;
          const { value } = computePortfolioCurrentValue(portfolio, items, prices);
          setPortfolioValueById((prev) => ({ ...prev, [portfolioId]: value }));
        } catch {
          if (cancelled) return;
          setPortfolioValueById((prev) => ({ ...prev, [portfolioId]: "error" }));
        }
      })();
    }
    return () => { cancelled = true; };
    // The referenced IDs and portfolio catalogue are the request inputs. The
    // value map is intentionally omitted to avoid restarting in-flight reads.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [contextGoal, contextMatchesGoals, contextResponse, referencedPortfolioIds, portfolios]);

  const designatedBySource = useMemo(() => {
    const totals = new Map<string, number>();
    for (const designation of contextResponse?.designation_by_source ?? []) {
      totals.set(sourceKey(designation.source_kind, designation.source_id), designation.designated_total_in_context_scope);
    }
    return totals;
  }, [contextResponse]);

  function fundingHealthForSource(kind: GoalFundingSourceKind, id: number): SourceFundingHealth {
    // A missing or mismatched Goal Context means the cross-goal total is not
    // known. Keep the health claim unavailable instead of treating it as 0.
    if (!contextMatchesGoals || !contextGoal || !contextResponse) return computeSourceFundingHealth(0, null);
    const totalDesignated = designatedBySource.get(sourceKey(kind, id));
    if (totalDesignated === undefined) return computeSourceFundingHealth(0, null);
    const currentValue = kind === "CASH_ACCOUNT"
      ? allCashAccounts.find((account) => account.id === id)?.balance ?? null
      : (typeof portfolioValueById[id] === "number" ? portfolioValueById[id] as number : null);
    return computeSourceFundingHealth(totalDesignated, currentValue);
  }

  const reloadGoalContext = useCallback(async () => {
    if (!Number.isInteger(goalId) || goalId <= 0) return;
    const generation = loadGenerationRef.current;
    const contextGeneration = ++contextRefreshGenerationRef.current;
    setGoalContext(undefined);
    setPortfolioValueById({});
    try {
      const result = await getWealthGoalsContext(true);
      if (loadGenerationRef.current !== generation
        || contextRefreshGenerationRef.current !== contextGeneration
        || activeGoalIdRef.current !== goalId) return;
      setGoalContext(result);
    } catch (err) {
      if (loadGenerationRef.current !== generation
        || contextRefreshGenerationRef.current !== contextGeneration
        || activeGoalIdRef.current !== goalId) return;
      setGoalContext({ error: messageFor(err, "Unable to refresh Goal Context.") });
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
              onReload={reloadGoalContext}
              fundingHealthForSource={fundingHealthForSource}
            />
          </section>

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
