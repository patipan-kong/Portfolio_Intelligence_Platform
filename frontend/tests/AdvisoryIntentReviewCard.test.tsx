import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import AdvisoryIntentReviewCard from "@/components/optimizer/AdvisoryIntentReviewCard";
import type {
  AdvisoryIntentReview,
  AdvisoryPositionReview,
  AdvisoryProposalReview,
  OptimizerResult,
} from "@/lib/api";

const consistent: AdvisoryProposalReview = {
  outcome: "CONSISTENT", direction: "NO_CHANGE", restriction: null, reasons: ["NO_QUANTITY_CHANGE"],
};

function position(overrides: Partial<AdvisoryPositionReview> & { symbol: string }): AdvisoryPositionReview {
  return {
    applicability: "CONFIRMED",
    hard_restrictions: { increase_prohibited: false, decrease_prohibited: true },
    proposal: { final_effective: { direction: "NO_CHANGE", action: "HOLD" } },
    review: { final: consistent, retained: [], status: "CONSISTENT", requires_owner_decision: false,
              unresolved_reasons: [] },
    display: { final_disposition: "UNCHANGED", show: false },
    ...overrides,
  };
}

function envelope(positions: AdvisoryPositionReview[], coverage: Partial<AdvisoryIntentReview["coverage"]> = {}): AdvisoryIntentReview {
  return {
    contract_version: "wealth.advisory-intent-review.v1",
    identity: { review_id: "r", created_at: "2026-10-07T00:00:00+00:00" },
    positions,
    coverage: {
      referenced_positive_held_count: positions.length, resolved_count: positions.length,
      unresolved_positions: [], conflict_positions: [], final_conflict_positions: [],
      retained_conflict_positions: [], all_resolved_and_consistent: false, ...coverage,
    },
    review: { result: "CONSISTENT", requires_owner_decision: false },
  };
}

function result(fields: Partial<OptimizerResult>): OptimizerResult {
  return { portfolio_name: "P", portfolio_assessment: "", optimization_notes: "", swap_suggestions: [],
           watchlist_ranking: [], analyzed_at: "", portfolio_count: 1, max_reached: false,
           ...fields } as OptimizerResult;
}

describe("AdvisoryIntentReviewCard", () => {
  it("renders nothing when the feature is off", () => {
    const { container } = render(<AdvisoryIntentReviewCard result={result({})} />);
    expect(container).toBeEmptyDOMElement();
  });

  it("says the recommendation respects intent only when everything is resolved and consistent", () => {
    const review = envelope([position({ symbol: "PTT.BK" })], { all_resolved_and_consistent: true });
    render(<AdvisoryIntentReviewCard result={result({ advisory_intent_review: review,
                                                       advisory_intent_review_status: "CAPTURED" })} />);
    expect(screen.getByRole("status")).toHaveTextContent("Recommendation respects your intent.");
    expect(screen.getByRole("note")).toHaveTextContent("do not read your intent yet");
    expect(screen.getByRole("note")).toHaveTextContent("This is a check, not a block");
  });

  it("does not claim respect when a position could not be checked", () => {
    const unresolved = position({
      symbol: "SCB.BK", applicability: "NO_CONFIRMED_INTENT", hard_restrictions: null,
      review: { final: { outcome: "UNRESOLVED", direction: "NO_CHANGE", restriction: null, reasons: ["NO_CONFIRMED_INTENT"] },
                retained: [], status: "UNRESOLVED", requires_owner_decision: false,
                unresolved_reasons: ["NO_CONFIRMED_INTENT"] },
      display: { final_disposition: "UNCHANGED", show: true },
    });
    const review = envelope([unresolved], { resolved_count: 0, unresolved_positions: ["SCB.BK"] });
    render(<AdvisoryIntentReviewCard result={result({ advisory_intent_review: review,
                                                       advisory_intent_review_status: "CAPTURED" })} />);
    expect(screen.queryByText(/respects your intent/)).toBeNull();
    expect(screen.getByRole("status")).toHaveTextContent("Checked 0 of 1 held positions");
    expect(screen.getByText(/Not checked against your intent: no intent saved/)).toBeInTheDocument();
  });

  it("explains a final-plan conflict in owner language", () => {
    const conflict = position({
      symbol: "KBANK.BK",
      proposal: { final_effective: { direction: "DECREASE", action: "REDUCE" } },
      review: { final: { outcome: "CONFLICT", direction: "DECREASE", restriction: "DECREASE_PROHIBITED_BY_OWNER",
                         reasons: ["DECREASE_PROHIBITED_BY_OWNER"] },
                retained: [], status: "CONFLICT", requires_owner_decision: true, unresolved_reasons: [] },
      display: { final_disposition: "CHANGE_PROPOSED", show: true },
    });
    render(<AdvisoryIntentReviewCard result={result({ advisory_intent_review: envelope([conflict]),
                                                       advisory_intent_review_status: "CAPTURED" })} />);
    expect(screen.getByRole("status")).toHaveTextContent("1 proposal conflicts with your intent — review required.");
    expect(screen.getByText(/The system sees a reason to reduce KBANK\.BK\./)).toHaveTextContent(
      "You marked ‘Do not decrease’.");
    expect(screen.queryByText(/No reduction is scheduled/)).not.toBeInTheDocument();
  });

  it("connects the economic conflict to frozen deferred scheduling without erasing review", () => {
    const conflict = position({
      symbol: "AAA",
      proposal: {
        final_effective: { direction: "DECREASE", action: "REDUCE" },
        scheduled: { execution_state: "DEFERRED", executed_amount: 0 },
      },
      review: {
        final: { outcome: "CONFLICT", direction: "DECREASE", restriction: "DECREASE_PROHIBITED_BY_OWNER", reasons: [] },
        retained: [], status: "CONFLICT", requires_owner_decision: true, unresolved_reasons: [],
      },
      display: { final_disposition: "CHANGE_PROPOSED", show: true },
    });
    const { rerender } = render(<AdvisoryIntentReviewCard result={result({ advisory_intent_review: envelope([conflict]) })} />);
    expect(screen.getByRole("status")).toHaveTextContent("review required");
    expect(screen.getByText(/The system sees a reason/)).toHaveTextContent(
      "The system sees a reason to reduce AAA. No reduction is scheduled today. You marked ‘Do not decrease’.");
    // Full scheduling evidence must not inherit the deferred wording.
    conflict.proposal.scheduled = { execution_state: "FULL", executed_amount: 1000 };
    rerender(<AdvisoryIntentReviewCard result={result({ advisory_intent_review: envelope([conflict]) })} />);
    expect(screen.queryByText(/No reduction is scheduled/)).not.toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveTextContent("review required");
  });

  it("keeps a suppressed exit visible next to an unchanged final plan", () => {
    const suppressed = position({
      symbol: "PTT.BK",
      review: {
        final: consistent, status: "CONFLICT", requires_owner_decision: true, unresolved_reasons: [],
        retained: [{
          proposal_id: "P2", source: "SYSTEM_RULE", stage: "FORCED_SELL", reason_code: "FORCED_EXIT_SELL_SIGNAL",
          action: "SELL", disposition: "SUPPRESSED", suppressed_by: "LEGACY_ALLOW_SWAP",
          projection: { kind: "FULL_EXIT" },
          review: { outcome: "CONFLICT", direction: "DECREASE", restriction: "DECREASE_PROHIBITED_BY_OWNER",
                    reasons: ["DECREASE_PROHIBITED_BY_OWNER"] },
        }],
      },
      display: { final_disposition: "UNCHANGED", show: true },
    });
    render(<AdvisoryIntentReviewCard result={result({ advisory_intent_review: envelope([suppressed]),
                                                       advisory_intent_review_status: "CAPTURED" })} />);
    expect(screen.getByText("No quantity change is proposed in the final plan.")).toBeInTheDocument();
    expect(screen.getByText(
      "The system identified a reason to exit PTT.BK, which conflicts with your 'Do not decrease' "
      + "restriction; another control suppressed it.")).toBeInTheDocument();
    expect(screen.queryByText(/respects your intent/)).toBeNull();
  });

  it("reports missing and invalid history evidence without recomputing", () => {
    const { rerender } = render(<AdvisoryIntentReviewCard result={result({ advisory_intent_review: null,
      advisory_intent_review_status: "NOT_CAPTURED" })} />);
    expect(screen.getByText("No intent review was captured for this run.")).toBeInTheDocument();
    rerender(<AdvisoryIntentReviewCard result={result({ advisory_intent_review: null,
      advisory_intent_review_status: "EVIDENCE_INVALID" })} />);
    expect(screen.getByText(/could not be verified/)).toBeInTheDocument();
  });

  it("notes intent changed since the run without rewriting the review", () => {
    const review = envelope([position({ symbol: "PTT.BK" })], { all_resolved_and_consistent: true });
    render(<AdvisoryIntentReviewCard result={result({
      advisory_intent_review: review, advisory_intent_review_status: "CAPTURED",
      advisory_intent_changes_since_run: [{ symbol: "PTT.BK", run_intent_revision: 1, current_intent_revision: 2 }],
    })} />);
    expect(screen.getByText(/Your intent changed after this run for PTT\.BK/)).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveTextContent("Recommendation respects your intent.");
  });
});
