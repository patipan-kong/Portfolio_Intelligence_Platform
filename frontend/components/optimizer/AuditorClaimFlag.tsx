import type { RiskFlag } from "@/lib/api";

export default function AuditorClaimFlag({ flag }: { flag: RiskFlag }) {
  const label = flag.category === "OWNER_INTENT_REVIEW" ? "Owner review"
    : flag.validation_status === "VERIFIED" ? flag.claim_kind === "INVESTMENT_OBSERVATION" ? "Evidence-backed investment risk" : "Verified restriction"
    : flag.validation_status === "MODEL_OPINION" ? "Model investment opinion — unscored"
    : flag.validation_status === "ADVISORY" ? "Advisory — unscored"
    : flag.validation_status === "UNSUPPORTED" ? "Unsupported — unscored" : "Historical model flag";
  // Unscored claims do not use the red verified-risk presentation.
  const color = flag.scoring_eligible === false ? "text-gray-600 bg-gray-50 border-gray-200"
    : ["HIGH", "CRITICAL"].includes(flag.severity) ? "text-red-700 bg-red-50 border-red-300"
    : "text-amber-700 bg-amber-50 border-amber-300";
  return <div className={`border rounded-lg px-3 py-2 text-xs ${color}`}>
    <span className="font-bold mr-1.5">[{label}]</span>
    {flag.scoring_eligible !== false && <span className="mr-1.5">{flag.severity}</span>}
    <span className="font-semibold mr-1">{flag.symbol}</span>{flag.issue}
    {flag.provenance && <p className="mt-1 text-gray-500">Evidence: {typeof flag.provenance === "string"
      ? flag.provenance : JSON.stringify(flag.provenance)}</p>}
  </div>;
}
