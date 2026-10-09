import type { TradeEvidenceStatus } from "@/lib/api";

/**
 * One wording source for the provenance of a trade's Required / Reason
 * classification, shared by the optimizer Execution Plan and the Report Card.
 * Only VERIFIED_NAV (and non-concentration statuses) read as a plain "Required".
 */
type Status = TradeEvidenceStatus | string | null | undefined;

export function requiredLabel(status: Status): string {
  if (status === "LEGACY_RECORDED_UNVERIFIED") return "Required (as recorded)";
  if (status === "SECTOR_EQUITY_BASIS") return "Required (equity-basis)";
  return "Required";
}

export function provenanceQualifier(status: Status): string | null {
  switch (status) {
    case "LEGACY_RECORDED_UNVERIFIED":
      return "As recorded for this run — it used equity-only weights, so the policy breach behind it is not NAV-verified.";
    case "UNVERIFIED":
      return "The concentration claim for this trade could not be verified against NAV, so it is not treated as required.";
    case "SECTOR_EQUITY_BASIS":
      return "Sector policy was evaluated using the existing equity-only denominator, not NAV.";
    default:
      return null;
  }
}
