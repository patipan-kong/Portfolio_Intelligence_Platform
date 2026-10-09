import { listExecutionDecisions } from "@/lib/api";
import type { ExecutionDecision } from "@/lib/api";

/**
 * Snapshot-specific owner-decision lookup.
 *
 * - found:       a verified row for exactly this portfolio + snapshot.
 * - none:        the server answered an exact snapshot filter with an empty list.
 *                Only this state means "no decision has been recorded".
 * - unavailable: anything else — request failure, malformed payload, or any row
 *                that is not this portfolio's decision for this snapshot (which is
 *                also what an older backend that ignores the filter looks like).
 *                Callers must not offer recording controls in this state.
 */
export type SnapshotDecisionLookup =
  | { status: "found"; decision: ExecutionDecision }
  | { status: "none" }
  | { status: "unavailable"; reason: "REQUEST_FAILED" | "MALFORMED_RESPONSE" | "IDENTITY_MISMATCH" };

function isVerifiedRow(row: unknown, portfolioId: number, snapshotId: number): row is ExecutionDecision {
  if (!row || typeof row !== "object") return false;
  const r = row as Partial<ExecutionDecision>;
  return r.recommendation_snapshot_id === snapshotId && r.portfolio_id === portfolioId;
}

export async function lookupSnapshotDecision(
  portfolioId: number,
  snapshotId: number,
): Promise<SnapshotDecisionLookup> {
  let rows: unknown;
  try {
    // Exact server-side filter, applied before the limit: no pagination window to outgrow.
    rows = await listExecutionDecisions(portfolioId, undefined, 1, snapshotId);
  } catch {
    return { status: "unavailable", reason: "REQUEST_FAILED" };
  }
  if (!Array.isArray(rows)) return { status: "unavailable", reason: "MALFORMED_RESPONSE" };
  if (rows.some((row) => !isVerifiedRow(row, portfolioId, snapshotId))) {
    return { status: "unavailable", reason: "IDENTITY_MISMATCH" };
  }
  if (rows.length === 0) return { status: "none" };
  return { status: "found", decision: rows[0] as ExecutionDecision };
}
