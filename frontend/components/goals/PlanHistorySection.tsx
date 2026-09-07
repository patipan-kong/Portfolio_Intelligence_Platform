import type { GoalPlanAmendmentHistory, WealthGoalPriority } from "@/lib/api";
import { formatThb, priorityLabel } from "./GoalPlanningSections";

export type PlanHistoryState = GoalPlanAmendmentHistory[] | { error: string } | undefined;

export const PLAN_HISTORY_DISCLOSURE =
  "Planning amendments only. This is not funding, contribution, transfer, or recommendation evidence.";

function dateLabel(value: string | null): string {
  return value ?? "No target date";
}

function priorityText(value: WealthGoalPriority): string {
  return `${priorityLabel(value)} priority`;
}

function changesFor(event: GoalPlanAmendmentHistory): string[] {
  const changes: string[] = [];
  if (event.previous_target_amount !== event.resulting_target_amount) {
    changes.push(`Target amount changed from ${formatThb(event.previous_target_amount)} to ${formatThb(event.resulting_target_amount)}.`);
  }
  if (event.previous_target_date !== event.resulting_target_date) {
    changes.push(`Target date changed from ${dateLabel(event.previous_target_date)} to ${dateLabel(event.resulting_target_date)}.`);
  }
  if (event.previous_priority !== event.resulting_priority) {
    changes.push(`Priority changed from ${priorityText(event.previous_priority)} to ${priorityText(event.resulting_priority)}.`);
  }
  return changes;
}

function timestampLabel(recordedAt: string): string {
  const parsed = new Date(recordedAt);
  return Number.isNaN(parsed.getTime()) ? recordedAt : parsed.toLocaleString();
}

export function PlanHistorySection({ state }: { state: PlanHistoryState }) {
  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="plan-history-heading">
      <h2 id="plan-history-heading" className="text-lg font-semibold">Plan history</h2>
      <p className="text-xs text-gray-500">{PLAN_HISTORY_DISCLOSURE}</p>
      {state === undefined ? (
        <p className="text-sm text-gray-400">Loading plan history…</p>
      ) : "error" in state ? (
        <p role="alert" className="text-sm text-red-600">{state.error || "Unable to load plan history."}</p>
      ) : state.length === 0 ? (
        <p className="text-sm text-gray-500">No plan amendments recorded yet.</p>
      ) : (
        <ol className="space-y-2">
          {state.map((event) => (
            <li key={event.id} className="border-b last:border-0 pb-2 text-sm">
              {changesFor(event).map((change) => <p key={change} className="text-gray-700">{change}</p>)}
              <p className="text-xs text-gray-400 mt-0.5">Plan amended · {timestampLabel(event.recorded_at)}</p>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
