"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import {
  FundingSourcesSection,
  GoalSummary,
  GoalWhatIfSection,
  SavedScenariosSection,
  type AllocationsState,
  type ScenariosState,
  messageFor,
} from "@/components/goals/GoalPlanningSections";
import {
  aggregateDesignatedBySource,
  computeSourceFundingHealth,
  sourceKey,
  type SourceFundingHealth,
} from "@/lib/goalFunding";
import { computePortfolioCurrentValue } from "@/lib/wealthOverview";
import {
  createGoalScenario,
  getHoldings,
  getPortfolioPrices,
  listCashAccounts,
  listGoalFundingAllocations,
  listGoalScenarios,
  listPortfolios,
  listWealthGoals,
  type CashAccount,
  type GoalFundingAllocation,
  type GoalFundingSourceKind,
  type GoalScenario,
  type Portfolio,
  type WealthGoal,
} from "@/lib/api";
import { priorityLabel, typeLabel } from "@/components/goals/GoalPlanningSections";

export default function GoalDetailPage({ params }: { params: { id: string } }) {
  const goalId = Number(params.id);
  const activeGoalIdRef = useRef(goalId);
  const loadGenerationRef = useRef(0);
  activeGoalIdRef.current = goalId;
  const [goal, setGoal] = useState<WealthGoal | null>(null);
  const [allGoals, setAllGoals] = useState<WealthGoal[]>([]);
  const [allocations, setAllocations] = useState<AllocationsState>(undefined);
  const [allocationsByGoal, setAllocationsByGoal] = useState<Record<number, AllocationsState>>({});
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
    const isCurrentLoad = () => loadGenerationRef.current === generation && activeGoalIdRef.current === goalId;
    setLoading(true);
    setError("");
    setErrorGoalId(null);
    setGoal(null);
    setAllocations(undefined);
    setAllocationsByGoal({});
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
      // The current WealthGoal API exposes a workspace list, not GET-by-id.
      // Load the list once and select the URL-anchored goal; no unrelated goal
      // state is rendered or used for planning.
      const goals = await listWealthGoals(true);
      if (!isCurrentLoad()) return;
      const selectedGoal = goals.find((item) => item.id === goalId);
      if (!selectedGoal) {
        setError("Goal not found.");
        setErrorGoalId(goalId);
        setAllGoals(goals);
        return;
      }

      setAllGoals(goals);
      setGoal(selectedGoal);

      // Funding Health is intentionally source-centric and aggregates
      // designation across all goals. The API has no aggregate endpoint, so
      // retain that existing semantic with explicit allocation evidence while
      // keeping all planning calculations anchored to the selected goal.
      const readAllocations = async (candidateId: number): Promise<AllocationsState> => {
        try {
          return await listGoalFundingAllocations(candidateId);
        } catch (err) {
          return { error: messageFor(err, "Unable to load funding sources.") };
        }
      };
      // The selected goal is the primary planning payload. Cross-goal
      // allocation reads continue in the background solely to complete the
      // existing aggregate Funding Health claim; they must not delay the
      // selected goal's summary, CRUD, or What-If surface.
      const selectedAllocations = await readAllocations(goalId);
      if (!isCurrentLoad()) return;
      setAllocationsByGoal({ [goalId]: selectedAllocations });
      setAllocations(selectedAllocations);
      const otherGoals = goals.filter((candidate) => candidate.id !== goalId);
      void Promise.all(otherGoals.map(async (candidate) => [candidate.id, await readAllocations(candidate.id)] as const)).then((entries) => {
        if (!isCurrentLoad()) return;
        setAllocationsByGoal((previous) => {
          const next = { ...previous };
          for (const [candidateId, result] of entries) next[candidateId] = result;
          return next;
        });
      });

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

  const referencedPortfolioIds = useMemo(() => {
    const ids = new Set<number>();
    if (!Array.isArray(allocations)) return ids;
    for (const allocation of allocations) {
      if (allocation.portfolio_id != null) ids.add(allocation.portfolio_id);
    }
    return ids;
  }, [allocations]);

  useEffect(() => {
    let cancelled = false;
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
  }, [referencedPortfolioIds, portfolios]);

  const designatedBySource = useMemo(() => {
    const loaded: GoalFundingAllocation[] = [];
    for (const result of Object.values(allocationsByGoal)) {
      if (Array.isArray(result)) loaded.push(...result);
    }
    return aggregateDesignatedBySource(loaded);
  }, [allocationsByGoal]);

  const allocationEvidenceComplete = allGoals.length > 0
    && allGoals.every((candidate) => Array.isArray(allocationsByGoal[candidate.id]));

  function fundingHealthForSource(kind: GoalFundingSourceKind, id: number): SourceFundingHealth {
    // A missing allocation list means the cross-goal total is not known. Keep
    // the health claim unavailable instead of treating missing evidence as 0.
    if (!allocationEvidenceComplete) return computeSourceFundingHealth(0, null);
    const totalDesignated = designatedBySource.get(sourceKey(kind, id)) ?? 0;
    const currentValue = kind === "CASH_ACCOUNT"
      ? allCashAccounts.find((account) => account.id === id)?.balance ?? null
      : (typeof portfolioValueById[id] === "number" ? portfolioValueById[id] as number : null);
    return computeSourceFundingHealth(totalDesignated, currentValue);
  }

  const reloadAllocations = useCallback(async () => {
    if (!Number.isInteger(goalId) || goalId <= 0) return;
    try {
      const result = await listGoalFundingAllocations(goalId);
      if (activeGoalIdRef.current !== goalId) return;
      setAllocations(result);
      setAllocationsByGoal((prev) => ({ ...prev, [goalId]: result }));
    } catch (err) {
      if (activeGoalIdRef.current !== goalId) return;
      const failure = { error: messageFor(err, "Unable to load funding sources.") };
      setAllocations(failure);
      setAllocationsByGoal((prev) => ({ ...prev, [goalId]: failure }));
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
            <GoalSummary item={currentGoal} allocations={allocations} />
          </section>

          <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="funding-heading">
            <h2 id="funding-heading" className="text-lg font-semibold">Funding</h2>
            <FundingSourcesSection
              key={currentGoal.id}
              goalId={currentGoal.id}
              readOnly={currentGoal.is_archived}
              cashAccounts={cashAccounts}
              portfolios={portfolios}
              allocations={allocations}
              onReload={reloadAllocations}
              fundingHealthForSource={fundingHealthForSource}
            />
          </section>

          <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="planning-heading">
            <h2 id="planning-heading" className="text-lg font-semibold">Planning / What-If</h2>
            <GoalWhatIfSection
              item={currentGoal}
              allocations={allocations}
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
