import { formatThb } from "./GoalPlanningSections";
import {
  deriveGoalReviewCues,
  type GoalReviewCue,
  type GoalReviewCuesInput,
} from "@/lib/goalReviewCues";

function timestampLabel(value: string): string {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString();
}

function cueText(cue: GoalReviewCue): string {
  switch (cue.kind) {
    case "DESIGNATION_GAP":
      return `Designated funding is ${formatThb(cue.amount as number)} below the current target.`;
    case "TARGET_DATE_MISSING":
      return "A target date is not set, so the required monthly contribution cannot be calculated.";
    case "SOURCE_OVER_ALLOCATED":
      return `${cue.sourceName} has total designations above its observed value.`;
    case "SOURCE_VALUE_UNAVAILABLE":
      return `Observed value is unavailable for ${cue.sourceName}.`;
    case "SOURCE_EVIDENCE_INCOMPLETE":
      return `Observed value evidence is incomplete for ${cue.sourceName}.`;
    case "SOURCE_ARCHIVED":
      return `${cue.sourceName} is archived and remains a designated source.`;
    case "AFFORDABILITY_SHORTFALL":
      return "Recorded cash-flow evidence is below the required monthly contribution calculation.";
    case "AFFORDABILITY_INSUFFICIENT_DATA":
      return `Recorded cash-flow evidence is insufficient for this calculation${cue.affordabilityReason ? `: ${cue.affordabilityReason}` : "."}`;
    case "PLAN_AMENDMENT":
      return `Plan terms were previously amended (${timestampLabel(cue.recordedAt as string)}).`;
    case "FUNDING_AMENDMENT":
      return `Funding designations were previously amended (${timestampLabel(cue.recordedAt as string)}).`;
  }
}

export function GoalReviewCues({ input }: { input: GoalReviewCuesInput }) {
  const result = deriveGoalReviewCues(input);

  return (
    <section className="border rounded-lg bg-gray-50 p-3 space-y-2" aria-labelledby="goal-review-cues-heading">
      <div>
        <h2 id="goal-review-cues-heading" className="text-sm font-semibold text-gray-700">Goal review cues</h2>
        <p className="text-xs text-gray-500">Factual links to existing information that may deserve review.</p>
      </div>
      {result.cues.length > 0 ? (
        <ul className="space-y-1 text-sm">
          {result.cues.map((cue, index) => (
            <li key={`${cue.kind}:${cue.sourceName ?? ""}:${cue.recordedAt ?? ""}:${index}`}>
              <a href={cue.href} className="text-blue-600 hover:underline">{cueText(cue)}</a>
            </li>
          ))}
        </ul>
      ) : result.hasUnavailableEvidence ? (
        <p className="text-sm text-gray-500">Review cues are still loading or unavailable for some evidence.</p>
      ) : (
        <p className="text-sm text-gray-500">No review cues from the currently available evidence.</p>
      )}
      {result.cues.length > 0 && result.hasUnavailableEvidence && (
        <p className="text-xs text-gray-500">Some review evidence is still loading or unavailable.</p>
      )}
    </section>
  );
}
