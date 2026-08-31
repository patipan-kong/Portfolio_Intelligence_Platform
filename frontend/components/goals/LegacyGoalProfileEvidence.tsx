import { formatThb } from "@/components/goals/GoalPlanningSections";
import {
  goalTypeComparisonLabel,
  projectionStatusLabel,
  recordedValue,
  targetDateComparisonLabel,
} from "@/lib/legacyGoalProfileEvidence";
import type { LegacyGoalProfileEvidenceEdge } from "@/lib/api";

export type LegacyGoalProfileEvidenceState =
  | LegacyGoalProfileEvidenceEdge[]
  | { error: string }
  | undefined;

function RawProjection({
  raw,
  projection,
  status,
}: {
  raw: string | number | null;
  projection: string | number | null;
  status: LegacyGoalProfileEvidenceEdge["legacy_profile"]["goal_type"]["projection_status"];
}) {
  const exactRaw = typeof raw === "string" ? JSON.stringify(raw) : recordedValue(raw);
  return (
    <span>
      raw <span className="font-medium text-gray-700 whitespace-pre-wrap">{exactRaw}</span>
      {projection !== null && <> · compatibility projection <span className="font-medium text-gray-700">{recordedValue(projection)}</span></>}
      {` · ${projectionStatusLabel(status)}`}
    </span>
  );
}

export function LegacyGoalProfileEvidence({ state }: { state: LegacyGoalProfileEvidenceState }) {
  if (state === undefined) {
    return <p className="text-xs text-gray-400 pt-3 border-t">Loading legacy Portfolio goal-profile evidence…</p>;
  }
  if (!Array.isArray(state)) {
    return <p role="alert" className="text-xs text-gray-500 pt-3 border-t">{state.error}</p>;
  }
  if (state.length === 0) return null;

  return (
    <div className="pt-3 border-t space-y-3" aria-label="Legacy Portfolio goal-profile evidence">
      <div>
        <h3 className="text-sm font-semibold text-gray-700">Legacy Portfolio goal-profile evidence</h3>
        <p className="text-xs text-gray-500">
          This legacy planning metadata is shown because each Portfolio below is a designated funding source. No synchronization or precedence is implied.
        </p>
      </div>
      {state.map((edge) => {
        const legacy = edge.legacy_profile;
        return (
          <article key={edge.designation.id} className="rounded-lg border p-3 space-y-2" aria-label={`Legacy evidence for designation ${edge.designation.id}`}>
            <p className="text-sm font-medium text-gray-700">
              {edge.portfolio.name}{edge.designation.source_is_archived ? " (archived)" : ""}
            </p>
            <p className="text-xs text-gray-500">
              {formatThb(edge.designation.designated_amount)} from this Portfolio is designated toward {edge.wealth_goal.name}.
            </p>
            <dl className="grid gap-2 text-xs text-gray-500 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <dt className="font-medium text-gray-600">Goal type</dt>
                <dd>Canonical recorded code: <span className="font-medium text-gray-700">{edge.wealth_goal.goal_type}</span></dd>
                <dd>Legacy: <RawProjection raw={legacy.goal_type.raw_value} projection={legacy.goal_type.compatibility_projection} status={legacy.goal_type.projection_status} /></dd>
                <dd className="mt-1 rounded bg-gray-50 p-2">
                  {goalTypeComparisonLabel(legacy.goal_type.comparison)} This literal code evidence does not establish that the Wealth Goal and legacy Portfolio Goal Profile represent the same intended goal.
                </dd>
              </div>
              <div>
                <dt className="font-medium text-gray-600">Priority (separate vocabularies)</dt>
                <dd>Canonical: <span className="font-medium text-gray-700">{edge.wealth_goal.priority}</span></dd>
                <dd>Legacy: <RawProjection raw={legacy.goal_priority.raw_value} projection={legacy.goal_priority.compatibility_projection} status={legacy.goal_priority.projection_status} /></dd>
              </div>
              <div>
                <dt className="font-medium text-gray-600">Target date</dt>
                <dd>Canonical: <span className="font-medium text-gray-700">{recordedValue(edge.wealth_goal.target_date)}</span></dd>
                <dd>Legacy: <RawProjection raw={legacy.goal_target_date.raw_value} projection={legacy.goal_target_date.compatibility_projection} status={legacy.goal_target_date.projection_status} /></dd>
                <dd className="mt-1 rounded bg-gray-50 p-2">
                  {targetDateComparisonLabel(legacy.goal_target_date.comparison)} This literal date evidence does not establish that the Wealth Goal and legacy Portfolio Goal Profile represent the same intended goal.
                </dd>
              </div>
              <div className="sm:col-span-2">
                <dt className="font-medium text-gray-600">Target value (side-by-side facts)</dt>
                <dd>Canonical: <span className="font-medium text-gray-700">{formatThb(edge.wealth_goal.target_amount)} {edge.wealth_goal.currency}</span></dd>
                <dd>Legacy: <RawProjection raw={legacy.goal_target_value.raw_value} projection={legacy.goal_target_value.compatibility_projection} status={legacy.goal_target_value.projection_status} /></dd>
                <dd>Legacy unit: unspecified in the legacy contract.</dd>
              </div>
            </dl>
          </article>
        );
      })}
    </div>
  );
}
