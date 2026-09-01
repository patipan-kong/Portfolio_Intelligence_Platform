"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import {
  deletePortfolioInvestmentMandate,
  listPortfolioInvestmentMandates,
  listWealthGoals,
  putPortfolioInvestmentMandate,
  type PortfolioInvestmentMandate,
  type WealthGoal,
} from "@/lib/api";

export default function PortfolioInvestmentMandates({ portfolioId }: { portfolioId: number }) {
  const [mandates, setMandates] = useState<PortfolioInvestmentMandate[]>([]);
  const [goals, setGoals] = useState<WealthGoal[]>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [loading, setLoading] = useState(true);
  const [workingGoalId, setWorkingGoalId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const currentPortfolioIdRef = useRef(portfolioId);

  useEffect(() => {
    currentPortfolioIdRef.current = portfolioId;
    let active = true;
    setLoading(true);
    setError(null);
    setMandates([]);
    setGoals([]);
    setSelectedGoalId("");
    setWorkingGoalId(null);
    Promise.all([listPortfolioInvestmentMandates(portfolioId), listWealthGoals(true)])
      .then(([nextMandates, nextGoals]) => {
        if (!active) return;
        setMandates(nextMandates);
        setGoals(nextGoals);
      })
      .catch((err: unknown) => {
        if (active) setError(err instanceof Error ? err.message : "Unable to load investment mandates");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, [portfolioId]);

  const goalsById = useMemo(() => new Map(goals.map((goal) => [goal.id, goal])), [goals]);
  const linkedGoalIds = useMemo(() => new Set(mandates.map((mandate) => mandate.wealth_goal_id)), [mandates]);
  const candidates = goals.filter((goal) => !goal.is_archived && !linkedGoalIds.has(goal.id));

  async function addMandate() {
    if (!selectedGoalId) return;
    const goalId = Number(selectedGoalId);
    const requestPortfolioId = portfolioId;
    setWorkingGoalId(goalId);
    setError(null);
    try {
      const mandate = await putPortfolioInvestmentMandate(portfolioId, goalId);
      if (currentPortfolioIdRef.current !== requestPortfolioId) return;
      setMandates((current) => current.some((item) => item.id === mandate.id) ? current : [...current, mandate]);
      setSelectedGoalId("");
    } catch (err) {
      if (currentPortfolioIdRef.current !== requestPortfolioId) return;
      setError(err instanceof Error ? err.message : "Unable to add investment mandate");
    } finally {
      if (currentPortfolioIdRef.current === requestPortfolioId) setWorkingGoalId(null);
    }
  }

  async function removeMandate(goalId: number) {
    const requestPortfolioId = portfolioId;
    setWorkingGoalId(goalId);
    setError(null);
    try {
      await deletePortfolioInvestmentMandate(portfolioId, goalId);
      if (currentPortfolioIdRef.current !== requestPortfolioId) return;
      setMandates((current) => current.filter((item) => item.wealth_goal_id !== goalId));
    } catch (err) {
      if (currentPortfolioIdRef.current !== requestPortfolioId) return;
      setError(err instanceof Error ? err.message : "Unable to remove investment mandate");
    } finally {
      if (currentPortfolioIdRef.current === requestPortfolioId) setWorkingGoalId(null);
    }
  }

  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm" aria-labelledby="investment-mandates-heading">
      <h2 id="investment-mandates-heading" className="text-sm font-semibold text-gray-700">
        Portfolio Investment Mandates
      </h2>
      <p className="text-xs text-gray-500 mt-1">Goals this portfolio is intentionally managed to serve.</p>

      {loading ? <p className="text-sm text-gray-400 mt-3">Loading…</p> : (
        <div className="mt-3 space-y-3">
          {mandates.length === 0 ? (
            <p className="text-sm text-gray-500">No investment mandates authored.</p>
          ) : (
            <ul className="space-y-2">
              {mandates.map((mandate) => {
                const goal = goalsById.get(mandate.wealth_goal_id);
                return (
                  <li key={mandate.id} className="flex items-center justify-between gap-3 border rounded-lg px-3 py-2">
                    <span className="text-sm text-gray-700">
                      {goal?.name ?? `Wealth Goal #${mandate.wealth_goal_id}`}
                      {goal?.is_archived && <span className="ml-2 text-xs text-amber-700">Archived</span>}
                    </span>
                    <button
                      type="button"
                      onClick={() => removeMandate(mandate.wealth_goal_id)}
                      disabled={workingGoalId === mandate.wealth_goal_id}
                      className="text-xs text-red-600 border border-red-200 rounded px-2.5 py-1 hover:bg-red-50 disabled:opacity-40"
                    >
                      Remove
                    </button>
                  </li>
                );
              })}
            </ul>
          )}

          <div className="flex flex-wrap gap-2">
            <label className="sr-only" htmlFor={`mandate-goal-${portfolioId}`}>Goal to add</label>
            <select
              id={`mandate-goal-${portfolioId}`}
              value={selectedGoalId}
              onChange={(event) => setSelectedGoalId(event.target.value)}
              className="text-sm border rounded px-2.5 py-1.5 min-w-52"
            >
              <option value="">Select an active goal</option>
              {candidates.map((goal) => <option key={goal.id} value={goal.id}>{goal.name}</option>)}
            </select>
            <button
              type="button"
              onClick={addMandate}
              disabled={!selectedGoalId || workingGoalId !== null}
              className="text-sm bg-blue-600 text-white rounded px-3 py-1.5 hover:bg-blue-700 disabled:opacity-40"
            >
              Add
            </button>
          </div>
        </div>
      )}
      {error && <p role="alert" className="text-xs text-red-600 mt-2">{error}</p>}
    </section>
  );
}
