import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  evidenceEdgesForGoal,
  goalTypeComparisonLabel,
  legacyEvidenceMatchesGoalContext,
  legacyEvidenceMatchesReferenceGoalContext,
  recordedValue,
} from "./legacyGoalProfileEvidence.ts";
import type {
  GoalContextGoal,
  GoalContextResponse,
  LegacyGoalProfileEvidenceEdge,
  LegacyGoalProfileEvidenceResponse,
} from "@/lib/api";

function goal(id: number, allocationId: number): GoalContextGoal {
  return {
    id,
    name: `Goal ${id}`,
    goal_type: id === 1 ? "RETIREMENT" : "HOUSE",
    target_amount: 1_000_000,
    currency: "THB",
    target_date: "2050-01-01",
    priority: "HIGH",
    is_archived: false,
    updated_at: "2026-08-31T00:00:00Z",
    allocations: [{
      id: allocationId,
      wealth_goal_id: id,
      source_kind: "PORTFOLIO",
      source_id: 9,
      source_name: "Long-term Portfolio",
      source_is_archived: false,
      designated_amount: 500_000,
      currency: "THB",
      updated_at: "2026-08-31T00:00:00Z",
    }],
    designated_total: 500_000,
    progress_ratio: 0.5,
    progress_percent: 50,
    funding_gap: 500_000,
    fully_designated: false,
  };
}

function context(goals = [goal(1, 101)]): GoalContextResponse {
  return {
    contract_version: "wealth.goal-context.v1",
    context_generated_at: "2026-08-31T00:00:00Z",
    completeness: "COMPLETE",
    scope: { kind: "WORKSPACE", include_archived: true },
    goals,
    designation_by_source: [{
      source_kind: "PORTFOLIO",
      source_id: 9,
      source_name: "Long-term Portfolio",
      source_is_archived: false,
      currency: "THB",
      designated_total_in_context_scope: goals.length * 500_000,
    }],
  };
}

function edge(goalRecord: GoalContextGoal): LegacyGoalProfileEvidenceEdge {
  const designation = goalRecord.allocations[0];
  return {
    wealth_goal: {
      id: goalRecord.id,
      name: goalRecord.name,
      goal_type: goalRecord.goal_type,
      target_amount: goalRecord.target_amount,
      currency: goalRecord.currency,
      target_date: goalRecord.target_date,
      priority: goalRecord.priority,
      is_archived: goalRecord.is_archived,
      updated_at: goalRecord.updated_at,
    },
    designation,
    portfolio: { id: 9, name: "Long-term Portfolio" },
    legacy_profile: {
      evidence_availability: "ALL_FIELDS_RECORDED",
      goal_type: {
        raw_value: " retirement ",
        compatibility_projection: "RETIREMENT",
        compatibility_label_th: "เกษียณ",
        projection_status: "NORMALIZED",
        comparison: goalRecord.goal_type === "RETIREMENT" ? "SAME_RECORDED_CODE" : "DIFFERENT_RECORDED_CODES",
        provenance: "PORTFOLIO.GOAL_TYPE",
      },
      goal_priority: {
        raw_value: "IMPORTANT",
        compatibility_projection: "IMPORTANT",
        compatibility_label_th: "สำคัญ",
        projection_status: "UNCHANGED",
        provenance: "PORTFOLIO.GOAL_PRIORITY",
      },
      goal_target_date: {
        raw_value: "2050-01-01",
        compatibility_projection: "2050-01-01",
        projection_status: "UNCHANGED",
        comparison: "SAME_RECORDED_DATE",
        provenance: "PORTFOLIO.GOAL_TARGET_DATE",
      },
      goal_target_value: {
        raw_value: 1_000_000,
        compatibility_projection: 1_000_000,
        projection_status: "UNCHANGED",
        unit_status: "UNSPECIFIED_IN_LEGACY_CONTRACT",
        provenance: "PORTFOLIO.GOAL_TARGET_VALUE",
      },
    },
  };
}

function response(goals = [goal(1, 101)]): LegacyGoalProfileEvidenceResponse {
  return {
    contract_version: "wealth.legacy-profile-evidence.v1",
    generated_at: "2026-08-31T00:00:00Z",
    completeness: "COMPLETE",
    scope: { kind: "WORKSPACE", include_archived: true },
    goal_context: context(goals),
    evidence_edges: goals.map(edge),
  };
}

describe("legacy goal-profile evidence helpers", () => {
  it("accepts normalized raw and projected codes without reinterpreting the backend comparison", () => {
    const value = response();
    assert.equal(legacyEvidenceMatchesGoalContext(value), true);
    assert.equal(value.evidence_edges[0].legacy_profile.goal_type.raw_value, " retirement ");
    assert.equal(value.evidence_edges[0].legacy_profile.goal_type.compatibility_projection, "RETIREMENT");
    assert.equal(goalTypeComparisonLabel("SAME_RECORDED_CODE"), "The recorded codes are identical.");
  });

  it("keeps every shared-Portfolio allocation as a separate selected-goal edge", () => {
    const value = response([goal(1, 101), goal(2, 202)]);
    assert.equal(legacyEvidenceMatchesGoalContext(value), true);
    assert.equal(value.evidence_edges.length, 2);
    assert.deepEqual(evidenceEdgesForGoal(value, 1)?.map((item) => item.designation.id), [101]);
    assert.deepEqual(evidenceEdgesForGoal(value, 2)?.map((item) => item.designation.id), [202]);
  });

  it("fails closed when an edge differs from its embedded Goal Context", () => {
    const value = response();
    value.evidence_edges[0].designation = {
      ...value.evidence_edges[0].designation,
      designated_amount: 499_999,
    };
    assert.equal(legacyEvidenceMatchesGoalContext(value), false);
    assert.equal(evidenceEdgesForGoal(value, 1), null);
  });

  it("fails closed when supplemental and already accepted Goal Context facts differ", () => {
    const value = response();
    const reference = context();
    reference.goals[0].target_amount = 2_000_000;
    assert.equal(legacyEvidenceMatchesReferenceGoalContext(value, reference), false);
  });

  it("keeps unknown and empty raw evidence visible without client normalization", () => {
    assert.equal(recordedValue("OLD_CUSTOM_GOAL"), "OLD_CUSTOM_GOAL");
    assert.equal(recordedValue(""), "(empty string)");
    assert.equal(recordedValue(null), "Not recorded");
    assert.equal(goalTypeComparisonLabel("DIFFERENT_RECORDED_CODES"), "The recorded codes are different.");
  });
});
