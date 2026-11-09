import type { OptimizerResult, SectorAdvisoryEvidence } from "@/lib/api";
import { SECTOR_POLICY_ADVISORY } from "@/lib/optimizerPresentation";

export function sectorAdvisoryFor(result: OptimizerResult): SectorAdvisoryEvidence | undefined {
  const policy = result.active_policy;
  if (policy?.sector_policy_mode !== SECTOR_POLICY_ADVISORY) return undefined;
  return {
    current: policy.concentration?.current,
    projected_target: policy.concentration?.projected_target,
    scheduled: result.execution_optimization?.scheduled_sector_evaluation,
    alternatives: policy.sector_alternatives,
  };
}

const money = (value: number) => `฿${value.toLocaleString("th-TH", { maximumFractionDigits: 2 })}`;

export default function SectorConcentrationAdvisory({ evidence }: { evidence: SectorAdvisoryEvidence }) {
  const stages = [
    ["Current", evidence.current],
    ["Proposed target", evidence.projected_target],
    ["Scheduled", evidence.scheduled],
  ] as const;
  const hasBreach = stages.some(([, stage]) => stage?.sectors.some((row) => row.breach_pp > 0));
  return (
    <section aria-label="Sector concentration advisory" className="space-y-2 text-xs text-gray-700">
      <h4 className="font-semibold text-amber-800">Sector concentration advisory</h4>
      <p>Sector thresholds provide decision support. Required trades use independently verified hard-policy evidence.</p>
      {hasBreach && <p>Options include keeping the plan and accepting the exposure, diversifying through eligible buys, or considering an optional trim.</p>}
      {stages.map(([label, stage]) => (
        <div key={label} className="space-y-1">
          <p className="font-medium">
            {label} · {stage ? (stage.applicable ? `${money(stage.denominator)} invested equity` : "no invested equity") : "exposure unavailable"}
          </p>
          {stage?.sectors.map((row) => (
            <div key={row.evidence_id} className="pl-2">
              <p>
                {row.sector} · {money(row.numerator)} · {row.observed_pct?.toFixed(2)}%
                {" · "}threshold {row.limit_pct}% ({row.binding_source.replace(/_/g, " ").toLowerCase()})
                {row.breach_pp > 0 && <strong className="text-amber-800">
                  {" · "}{row.breach_pp.toFixed(2)} pp {label === "Scheduled" ? "residual above threshold" : "above threshold"}
                </strong>}
              </p>
              {!!row.members?.length && <details>
                <summary className="cursor-pointer text-gray-600">Classification evidence</summary>
                <ul className="pl-3">
                  {row.members.map((member) => <li key={member.symbol}>
                    {member.symbol} · {member.classification_status ?? "unavailable"}
                    {member.classification_source && ` · ${member.classification_source.replace(/_/g, " ")}`}
                    {member.raw_sector && ` · ${member.raw_sector}`}
                  </li>)}
                </ul>
              </details>}
            </div>
          ))}
          {!!stage?.estimated_symbols.length && <p>Missing market prices · {stage.estimated_symbols.join(", ")}.</p>}
          {stage?.infeasible_within_occupied_sectors && <p>
            The occupied-sector thresholds total {stage.occupied_cap_sum_pct?.toFixed(2)}%. Meeting all thresholds would require diversifying beyond those sectors.
          </p>}
        </div>
      ))}
      {!!evidence.alternatives?.length && <div>
        <p className="font-medium">Optional sector alternatives · excluded from the schedule</p>
        <ul className="pl-2">
          {evidence.alternatives.map((idea) => (
            <li key={`${idea.symbol}:${idea.action}:${idea.estimated_amount}`}>
              {idea.action} {idea.symbol} · {money(idea.estimated_amount)}{idea.reason && ` · ${idea.reason}`}
            </li>
          ))}
        </ul>
      </div>}
    </section>
  );
}
