import type { GoalFundingAllocationHistory } from "@/lib/api";
import { formatThb } from "./GoalPlanningSections";

export type FundingHistoryState = GoalFundingAllocationHistory[] | { error: string } | undefined;

function sourceKindLabel(kind: GoalFundingAllocationHistory["source_kind"]): string {
  return kind === "CASH_ACCOUNT" ? "Cash Account" : "Portfolio";
}

function eventDescription(event: GoalFundingAllocationHistory): string {
  if (event.action === "CREATE") {
    return `${event.source_name} designated ${formatThb(event.resulting_designated_amount as number)}.`;
  }
  if (event.action === "UPDATE") {
    return `${event.source_name} designation changed from ${formatThb(event.previous_designated_amount as number)} to ${formatThb(event.resulting_designated_amount as number)}.`;
  }
  return `${event.source_name} designation removed (${formatThb(event.previous_designated_amount as number)}).`;
}

function timestampLabel(recordedAt: string): string {
  const parsed = new Date(recordedAt);
  return Number.isNaN(parsed.getTime()) ? recordedAt : parsed.toLocaleString();
}

export function FundingHistorySection({ state }: { state: FundingHistoryState }) {
  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="funding-history-heading">
      <h2 id="funding-history-heading" className="text-lg font-semibold">Funding history</h2>
      <p className="text-xs text-gray-500">Designation changes only. This is not a record of contributions, transfers, or available funds.</p>
      {state === undefined ? (
        <p className="text-sm text-gray-400">Loading funding history…</p>
      ) : "error" in state ? (
        <p role="alert" className="text-sm text-red-600">{state.error || "Unable to load funding history."}</p>
      ) : state.length === 0 ? (
        <p className="text-sm text-gray-500">No funding designation changes recorded yet.</p>
      ) : (
        <ol className="space-y-2">
          {state.map((event) => (
            <li key={event.id} className="border-b last:border-0 pb-2 text-sm">
              <p className="text-gray-700">{eventDescription(event)}</p>
              <p className="text-xs text-gray-400 mt-0.5">
                Historical source: {event.source_name} ({sourceKindLabel(event.source_kind)}) · {timestampLabel(event.recorded_at)}
              </p>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
