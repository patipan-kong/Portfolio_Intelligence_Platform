import type { GoalRecommendationConstraintEvidence } from "@/lib/api";

function formatPct(value: number): string {
  return `${value.toFixed(1)}%`;
}

function StatusDetail({ evidence }: { evidence: GoalRecommendationConstraintEvidence }) {
  const status: string = evidence.resolution.application_status;
  const relation: string = evidence.resolution.relation_to_base;
  const before = evidence.resolution.pre_goal_effective_pct;
  const after = evidence.resolution.post_goal_effective_pct;

  if (status === "APPLIED_AND_BINDING") {
    return (
      <>
        <p className="font-medium text-emerald-700">Applied and binding</p>
        {relation === "STRICTER_THAN_BASE" && before != null && after != null ? (
          <p>Goal constraint tightened max single-position exposure from {formatPct(before)} to {formatPct(after)}.</p>
        ) : (
          <p>The backend reported the Goal constraint as binding, but did not provide a confirmed cap-tightening detail.</p>
        )}
      </>
    );
  }

  if (status === "APPLIED_BUT_DOMINATED") {
    return (
      <>
        <p className="font-medium text-amber-700">Applied, but not binding</p>
        {relation === "EQUAL_TO_BASE" ? (
          <p>
            The existing max single-position cap was already equal
            {after != null ? ` at ${formatPct(after)}` : ""} and retained control.
          </p>
        ) : relation === "LOOSER_THAN_BASE" ? (
          <p>
            Another existing constraint was already tighter
            {before != null ? ` at ${formatPct(before)}` : ""}
            {evidence.contribution ? ` than the ${formatPct(evidence.contribution.upper_bound_pct)} Goal candidate` : ""}.
          </p>
        ) : (
          <p>The backend reported that the Goal candidate did not control the final cap.</p>
        )}
      </>
    );
  }

  if (status === "NOT_APPLICABLE") {
    return <p className="font-medium text-gray-700">Not applicable for this run</p>;
  }

  return (
    <p className="font-medium text-gray-700">
      Status unavailable{status ? ` (${status})` : ""}
    </p>
  );
}

export default function GoalConstraintDisclosure({
  evidence,
  currentGoalName,
  expectedEvidence = false,
}: {
  evidence?: GoalRecommendationConstraintEvidence | null;
  currentGoalName?: string | null;
  expectedEvidence?: boolean;
}) {
  if (!evidence) {
    if (!expectedEvidence) return null;
    return (
      <section
        aria-label="Goal constraint metadata warning"
        className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800"
      >
        Optimizer completed, but Goal constraint outcome metadata was unavailable.
      </section>
    );
  }

  return (
    <section
      aria-label="Goal constraint outcome"
      className="rounded-lg border border-blue-200 bg-blue-50/60 px-4 py-3 text-sm text-gray-700"
    >
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h3 className="font-semibold text-gray-900">Goal constraint</h3>
        <span className="text-xs text-gray-500">Goal #{evidence.activated_goal_id}</span>
      </div>
      {currentGoalName && (
        <p className="mt-1 text-xs text-gray-500">Current Goal name: {currentGoalName}</p>
      )}
      <dl className="mt-2 flex flex-wrap gap-x-5 gap-y-1 text-xs">
        <div>
          <dt className="inline text-gray-500">Target date: </dt>
          <dd className="inline font-medium text-gray-700">{evidence.target_date}</dd>
        </div>
        <div>
          <dt className="inline text-gray-500">Horizon: </dt>
          <dd className="inline font-medium text-gray-700">{evidence.days_remaining} days remaining</dd>
        </div>
      </dl>
      <div className="mt-2 space-y-1 text-xs">
        <StatusDetail evidence={evidence} />
      </div>
    </section>
  );
}
