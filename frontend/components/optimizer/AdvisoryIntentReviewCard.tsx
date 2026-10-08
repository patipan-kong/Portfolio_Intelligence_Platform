"use client";

import type {
  AdvisoryIntentReview,
  AdvisoryIntentReviewStatus,
  AdvisoryPositionReview,
  AdvisoryProposalReview,
  AdvisoryRetainedProposal,
  OptimizerResult,
} from "@/lib/api";

// Advisory Integration V1 — renders the FROZEN Intent review captured with an
// optimizer run. Nothing is recomputed here: a history view shows exactly what
// was reviewed at run time. A conflict is disagreement for the owner to
// decide; it never blocks a trade and never changes the plan.

const RESTRICTION_LABEL: Record<string, string> = {
  INCREASE_PROHIBITED_BY_OWNER: "Do not increase",
  DECREASE_PROHIBITED_BY_OWNER: "Do not decrease",
};

const UNRESOLVED_LABEL: Record<string, string> = {
  NO_CONFIRMED_INTENT: "no intent saved",
  RECONFIRMATION_REQUIRED: "intent needs re-confirmation for this holding",
  CONTEXT_UNAVAILABLE: "your intent could not be loaded",
  VALUATION_BASIS_UNRESOLVED: "prices or currencies could not be put on one basis",
  MISSING_ALLOCATION: "the recommendation did not cover this position",
  DUPLICATE_ALLOCATION: "the recommendation listed this position twice",
  ACTION_QUANTITY_DIRECTION_MISMATCH: "the recommended action and its target disagree",
  QUANTITY_DIRECTION_TOLERANCE_AMBIGUITY: "the change is too small to classify reliably",
  PROVENANCE_CAPTURE_FAILED: "the recommendation's history could not be traced",
  PROVENANCE_MISSING: "the recommendation's history could not be traced",
  INVALID_TARGET_WEIGHT: "the target weight is invalid",
  UNKNOWN_ACTION: "the recommended action is not recognized",
};

function verb(review: AdvisoryProposalReview, fullExit: boolean): string {
  if (review.direction === "INCREASE") return "increase";
  return fullExit ? "exit" : "reduce";
}

function restriction(review: AdvisoryProposalReview): string {
  return review.restriction ? RESTRICTION_LABEL[review.restriction] ?? review.restriction : "";
}

function conflictCount(review: AdvisoryIntentReview): number {
  return review.positions.reduce((total, p) => total
    + (p.review.final.outcome === "CONFLICT" ? 1 : 0)
    + p.review.retained.filter((r) => r.review.outcome === "CONFLICT").length, 0);
}

function retainedSentence(symbol: string, r: AdvisoryRetainedProposal): string {
  const action = verb(r.review, r.projection?.kind === "FULL_EXIT");
  const how = r.disposition === "DEFERRED"
    ? "it is deferred for now"
    : r.disposition === "SUPPRESSED"
      ? "another control suppressed it"
      : "a later step replaced it";
  return `The system identified a reason to ${action} ${symbol}, which conflicts with your `
    + `'${restriction(r.review)}' restriction; ${how}.`;
}

function PositionDetail({ position }: { position: AdvisoryPositionReview }) {
  const { symbol, review } = position;
  const final = review.final;
  const retainedConflicts = review.retained.filter((r) => r.review.outcome === "CONFLICT");
  const unchanged = position.proposal.final_effective.direction === "NO_CHANGE";
  return (
    <li className="border rounded-lg px-3 py-2 text-xs space-y-1" aria-label={`Intent review for ${symbol}`}>
      <p className="font-medium text-gray-800">{symbol}</p>
      {final.outcome === "CONFLICT" && (
        <p className="text-red-800">
          The system sees a reason to {verb(final, position.proposal.final_effective.action === "SELL")} {symbol}.
          {position.proposal.scheduled?.execution_state === "DEFERRED" && (
            <> No {final.direction === "INCREASE" ? "increase" : "reduction"} is scheduled today.</>
          )}
          {" "}You marked &lsquo;{restriction(final)}&rsquo;.
        </p>
      )}
      {final.outcome === "UNRESOLVED" && (
        <p className="text-gray-600">
          Not checked against your intent: {review.unresolved_reasons
            .map((code) => UNRESOLVED_LABEL[code] ?? code).join("; ")}.
        </p>
      )}
      {final.outcome !== "CONFLICT" && unchanged && retainedConflicts.length > 0 && (
        <p className="text-gray-700">No quantity change is proposed in the final plan.</p>
      )}
      {retainedConflicts.map((r) => (
        <p key={r.proposal_id} className="text-amber-800">{retainedSentence(symbol, r)}</p>
      ))}
    </li>
  );
}

export default function AdvisoryIntentReviewCard({ result }: { result: OptimizerResult }) {
  const status: AdvisoryIntentReviewStatus | undefined = result.advisory_intent_review_status;
  const review = result.advisory_intent_review ?? null;
  if (!review && !status) return null;   // feature off: nothing to show

  if (!review) {
    return (
      <section className="bg-white border rounded-xl p-4 shadow-sm" aria-labelledby="intent-review-heading">
        <h2 id="intent-review-heading" className="text-sm font-semibold text-gray-700">Your intent</h2>
        <p className="text-xs text-gray-500 mt-1">
          {status === "EVIDENCE_INVALID"
            ? "The intent review saved with this run could not be verified, so it is not shown."
            : "No intent review was captured for this run."}
        </p>
      </section>
    );
  }

  const conflicts = conflictCount(review);
  const coverage = review.coverage;
  const shown = review.positions.filter((p) => p.display.show);
  const changes = result.advisory_intent_changes_since_run ?? [];

  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm space-y-2" aria-labelledby="intent-review-heading">
      <h2 id="intent-review-heading" className="text-sm font-semibold text-gray-700">Your intent</h2>
      {conflicts > 0 ? (
        <p role="status" className="text-sm font-medium text-red-800">
          {conflicts} proposal{conflicts !== 1 ? "s" : ""} conflict{conflicts === 1 ? "s" : ""} with your intent — review required.
        </p>
      ) : coverage.all_resolved_and_consistent ? (
        <p role="status" className="text-sm font-medium text-green-800">Recommendation respects your intent.</p>
      ) : (
        <p role="status" className="text-sm text-gray-700">
          Checked {coverage.resolved_count} of {coverage.referenced_positive_held_count} held positions
          against your intent; {coverage.unresolved_positions.length} could not be checked.
        </p>
      )}
      {shown.length > 0 && (
        <ul className="space-y-2">
          {shown.map((p) => <PositionDetail key={p.symbol} position={p} />)}
        </ul>
      )}
      {changes.length > 0 && (
        <p className="text-xs text-gray-500">
          Your intent changed after this run for {changes.map((c) => c.symbol).join(", ")}. This review
          reflects your intent at the time of the run.
        </p>
      )}
      <p role="note" className="text-[11px] text-gray-500">
        This is a check, not a block: nothing is prevented and you decide. Only this optimizer
        reviews held positions against your intent — position sizing, risk budget, idea review and
        Decision Workspace do not read your intent yet.
      </p>
    </section>
  );
}
