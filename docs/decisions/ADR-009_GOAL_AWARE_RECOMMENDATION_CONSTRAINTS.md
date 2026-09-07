# ADR-009: Goal-Aware Recommendation Constraints

**Status:** Accepted
**Date:** 2026-09-01
**Decision authority:** Human-approved Wealth OS Phase 7.5 architecture decision
**Scope:** The narrow pre-decision policy effect of one explicitly activated Wealth Goal

---

## Context

[ADR-008](ADR-008_WEALTH_GOAL_DECISION_CONTEXT_ADMISSION.md) established
`wealth.decision-goal-context.v1` as permanently `CONTEXT_ONLY`. It remains
selected through `goal_ids`, post-decision, snapshot-owned, and behaviorally
non-authoritative. Phase 7.5 introduces a separate, explicit pre-decision
policy path; it does not reinterpret or extend Phase 7.4 context.

## Problem

A near-term Goal may require a stricter concentration ceiling, but admitting
Goal semantics broadly would create unapproved ranking, allocation, valuation,
progress, risk-personality, or cross-Goal behavior. The policy must therefore
be explicit, deterministic, auditable, and unable to loosen existing safety.

## Decision

1. Behavioral activation uses the optional `goal_constraint_goal_id`; exactly
   one Goal may be activated, it need not appear in `goal_ids`, and activation
   never modifies `goal_ids`.
2. V1 admits only Goal identity, archive state, and `target_date`.
3. One UTC `as_of_date` is captured per activated request. Horizon is the
   signed integer count of calendar days from that date to `target_date`.
4. A horizon from 0 through 365 days inclusive contributes a 20% maximum
   single-position bound. A horizon above 365 days is valid `NOT_APPLICABLE`.
5. Archived Goals, Goals without a target date, and past-target Goals cannot
   drive a new recommendation.
6. Goal policy is deterministic, is never derived or reinterpreted by AI, and
   composes through Decision Intelligence constraint authority. It may tighten
   but never loosen the existing single-position bound.
7. Persisted application status is exactly `APPLIED_AND_BINDING`,
   `APPLIED_BUT_DOMINATED`, or `NOT_APPLICABLE`. Equality is non-binding and
   preserves the existing binding source.
8. Canonical Goal-policy evidence is persisted in
   `OptimizerHistory.result_json`. `RecommendationSnapshot` remains
   best-effort; no Goal-policy migration or table is introduced.
9. Activated hard-constraint failures fail closed only when the system cannot
   safely derive, compose, propagate, or deterministically enforce the Goal
   constraint. Unrelated optimizer, model, provider, parse, and consensus
   failures retain their established failure and fallback behavior.
10. Phase 7.4 context remains separate and `CONTEXT_ONLY`. Multi-Goal ranking,
    intersection, and objective behavior remain Phase 7.6 or later.

## Rationale

Explicit single-Goal activation makes authority unambiguous. A deterministic
upper bound can reuse the existing constraint envelope and enforcement system,
while canonical history evidence preserves what was applied without future
reads of mutable Goal state.

## Consequences

- Near-term Goals can only reduce the effective single-position ceiling.
- AI receives effective generic policy, not raw Goal facts or provenance.
- Goal context selection and Goal constraint activation remain independent.
- No Goal types, amounts, gaps, progress, priorities, allocations, valuations,
  scenarios, legacy Goal Profile facts, or risk-personality facts gain policy
  authority.

## Alternatives Considered

1. Infer activation from `goal_ids`. Rejected because it would violate the
   permanent Phase 7.4 context-only contract.
2. Admit multiple Goals or rank them. Rejected as unapproved cross-Goal policy.
3. Encode Goal20 directly in AI prompts or a Goal-specific optimizer clamp.
   Rejected because hard policy must be deterministic and share the existing
   constraint authority.
