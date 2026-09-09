"use client";

// Periodic Review — Goals section (Slice 1). A current-state snapshot, not
// Goal-history intelligence: no funding/plan-history fan-out, no "recently
// changed" claim, no reinterpretation of a funding source's OVER_ALLOCATED/
// UNAVAILABLE coverage status as a Goal-level "needs review" signal (that
// status is a per-source fact — ADR-016 — and is already shown in full on
// /goals; this section reuses only the same active-Goal list and compact
// funding summary that page already renders).

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { GoalFundingSummary, messageFor, priorityLabel, typeLabel } from "@/components/goals/GoalPlanningSections";
import { selectActiveGoalSummaries } from "@/lib/periodicReview";
import { getWealthFactualReview, listWealthGoals, type GoalContextGoal, type WealthGoal } from "@/lib/api";

type LoadState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "incoherent" }
  | { status: "loaded"; goals: GoalContextGoal[] };

export default function GoalsReviewSection() {
  const [state, setState] = useState<LoadState>({ status: "loading" });
  const mountedRef = useRef(true);
  const generationRef = useRef(0);

  useEffect(() => {
    mountedRef.current = true;
    return () => { mountedRef.current = false; };
  }, []);

  const refresh = useCallback(async () => {
    const generation = ++generationRef.current;
    const isCurrent = () => mountedRef.current && generationRef.current === generation;
    setState({ status: "loading" });

    const [goalsResult, reviewResult] = await Promise.allSettled([
      listWealthGoals(true),
      getWealthFactualReview(true),
    ]);
    if (!isCurrent()) return;

    if (goalsResult.status === "rejected") {
      setState({ status: "error", message: messageFor(goalsResult.reason, "Unable to load goals.") });
      return;
    }
    if (reviewResult.status === "rejected") {
      setState({ status: "error", message: messageFor(reviewResult.reason, "Unable to load factual wealth review.") });
      return;
    }

    const goals: WealthGoal[] = goalsResult.value;
    const active = selectActiveGoalSummaries(goals, reviewResult.value);
    if (active === null) {
      setState({ status: "incoherent" });
      return;
    }
    setState({ status: "loaded", goals: active });
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return (
    <section className="space-y-3">
      <h2 className="text-lg font-semibold">Current goals</h2>
      {state.status === "loading" ? (
        <p className="text-sm text-gray-400">Loading current goals…</p>
      ) : state.status === "error" ? (
        <div className="text-sm text-red-600 space-y-1">
          <p role="alert">{state.message}</p>
          <button type="button" onClick={() => void refresh()} className="text-blue-600 hover:underline">Try again</button>
        </div>
      ) : state.status === "incoherent" ? (
        <p role="alert" className="text-sm text-red-600">Current goals are unavailable — Goal Context evidence is incomplete.</p>
      ) : state.goals.length === 0 ? (
        <p className="text-sm text-gray-500">No active goals yet.</p>
      ) : (
        <div className="space-y-2">
          {state.goals.map((goal) => (
            <article key={goal.id} className="bg-white border rounded-xl p-3 shadow-sm space-y-2">
              <div className="flex items-start justify-between gap-3 flex-wrap">
                <div>
                  <p className="font-medium">{goal.name}</p>
                  <p className="text-xs text-gray-500">{typeLabel(goal.goal_type)} · {priorityLabel(goal.priority)} priority</p>
                </div>
                <Link href={`/goals/${goal.id}`} className="text-sm text-blue-600 hover:underline">View plan →</Link>
              </div>
              <GoalFundingSummary goalContext={goal} compact />
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
