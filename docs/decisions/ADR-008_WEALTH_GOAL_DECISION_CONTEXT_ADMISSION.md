# ADR-008: Wealth Goal Decision Context Admission

**Status:** Accepted
**Date:** 2026-08-31
**Decision authority:** Human-approved Wealth OS Phase 7.4 architecture decision
**Scope:** Architecture and governance only; no implementation-detail authority
(migration recipe, JSON field schema, HTTP mechanics, and exhaustive test
coverage are implementation decisions, not part of this record)

---

## Context

[ADR-007](ADR-007_WEALTH_GOAL_AUTHORITY_AND_LEGACY_PORTFOLIO_GOAL_PROFILE_BOUNDARY.md)
§7 named Wealth Goal context as blocked from Decision Intelligence until a
separate context-admission design defines: which canonical facts are
admitted, advisory association and cardinality, conflict and cross-goal
priority rules, authority/as-of-time/completeness/provenance, immutable
capture of the exact context used by a recorded recommendation, and any
deterministic translation into Decision Policy. Phase 7.2 (factual Goal
Context) and Phase 7.3 (factual Wealth Review) since shipped as read-only
Wealth Intelligence surfaces with no optimizer authority.

Phase 7.4 is the first Decision Intelligence-adjacent milestone. It asks the
narrowest possible question: may a caller explicitly name a set of Wealth
Goals on an optimizer request so that request's eventual recommendation
record carries a durable, factual account of what those goals looked like at
that time — without that naming influencing the recommendation itself.

## Problem

Without a binding ruling, an implementation could plausibly: infer goal
relevance from allocation overlap with the requested Portfolio; let selection
presence bias scoring or ranking; treat priority or target-date as a
recommendation input; invent conflict or comparison semantics for multiple
selected goals; consult the frozen Legacy Portfolio Goal Profile or
`risk_personality` as compatibility context; or persist context under
`OptimizerHistory`, changing what that table has always meant. Any of these
would manufacture advisory or optimizer authority ADR-007 explicitly withheld.

## Decision

1. **Explicit selection only.** Wealth Goal context is admitted to a
   recommendation record only when the caller names goal IDs on the request.
   No relevance, ownership, or allocation-based inference selects goals
   automatically.
2. **No advisory association.** Naming a goal on a Portfolio's optimizer
   request creates no cardinality, mandate, ownership, fit, or relevance
   relationship between that Portfolio and the goal. Optimizer Portfolio
   identity and selected Wealth Goal IDs remain independent request
   dimensions, exactly as ADR-007 §5 already holds for funding designation.
3. **CONTEXT_ONLY invariant.** The admitted payload carries a `decision_effect`
   of context-only. It is a historical record, not a decision input, and
   nothing computed from it may re-enter the optimizer, its policy,
   constraints, prompts, scoring, or consensus for this milestone.
4. **Post-decision construction.** The full factual context is constructed
   only after the recommendation result already exists — after L1/L2/L3,
   policy, constraints, scoring, consensus, and deterministic
   post-processing/stabilization have all completed. No Wealth Goal object
   exists while that pipeline runs. This is what makes invariant 3
   structurally true rather than merely promised.
5. **RecommendationSnapshot is the sole persistence owner.** `OptimizerHistory`
   — the canonical, unconditional optimizer history — remains unchanged and
   carries no Wealth Goal context. The derived, best-effort
   `RecommendationSnapshot` is the only place captured context is stored.
   Snapshot persistence remains best-effort: its failure, including a failure
   to capture Wealth Goal context, never blocks the optimizer response and
   never leaves `OptimizerHistory` in question.
6. **No legacy or risk consultation.** This milestone does not read the
   Legacy Portfolio Goal Profile, its compatibility projections, or
   `risk_personality`. ADR-007's freeze of that contract is unaffected;
   nothing here reopens it.
7. **No mandate, ranking, comparison, or cross-goal optimization.** Multiple
   selected goals are captured as independent factual records. This decision
   authorizes no comparison, divergence detection, ranking, primary-goal
   designation, merged objective, or cross-goal trade-off — those remain
   blocked exactly as ADR-007 §8 left them.
## Rationale

- Placing construction strictly after the decision already exists is the only
  design that makes non-influence a structural property of the code rather
  than a convention someone could violate later. It costs nothing today and
  removes an entire class of future accidental-influence bugs.
- Keeping `OptimizerHistory` untouched preserves the one guarantee every
  existing consumer of that table already depends on: it is committed
  unconditionally and never a `Wealth Goal service was reachable` question.
  Extending best-effort `RecommendationSnapshot` instead costs one nullable
  column and no new failure mode.
- ADR-007 already resolved that funding designation carries no advisory
  cardinality. Extending that same non-inference stance to request-scoped
  goal selection is the same ruling applied to a new surface, not a new
  judgment call.
- Deferring legacy/risk consultation and cross-goal semantics keeps this
  milestone inside the boundary ADR-007 actually cleared (factual admission)
  instead of quietly reaching into the still-blocked stages (7.5, 7.6).

## Consequences

- A recommendation record can now answer "what did the caller's selected
  Wealth Goals look like when this recommendation was produced" without that
  answer having been able to shape the recommendation.
- `OptimizerHistory` keeps its existing unconditional-commit contract; no
  caller of `/analyze/optimizer` observes a new failure mode from this
  change.
- Historical `RecommendationSnapshot` rows written before this milestone, and
  rows for requests that name no goals, carry no Wealth Goal context — this
  is an absence of capture, not a claim that no goals existed.
- Advisory Portfolio-to-Wealth-Goal association, cross-goal priority and
  conflict rules, goal-type or target-date policy effects, and cross-goal
  optimization remain exactly as blocked as ADR-007 §8 left them. This
  decision grants Phase 7.5 and 7.6 no authority.

## Alternatives Considered

1. **Construct context before or during the recommendation pipeline and pass
   it as optimizer input.** Rejected — this is precisely the advisory
   admission ADR-007 §7 deferred, and it would make non-influence a
   convention rather than a structural guarantee.
2. **Persist Wealth Goal context on `OptimizerHistory` instead of a derived
   table.** Rejected — it would change what the one table every existing
   consumer treats as unconditionally canonical actually means, and would tie
   a best-effort concern to a row that must always commit.
3. **Infer goal relevance from funding-allocation overlap with the requested
   Portfolio.** Rejected — ADR-007 §5 already ruled out manufacturing
   advisory cardinality from allocation facts; this would silently reopen
   that ruling for a new surface.
4. **Admit Legacy Portfolio Goal Profile or `risk_personality` alongside
   Wealth Goal context for continuity.** Rejected — both remain unresolved or
   frozen by ADR-007; admitting either here would grant Decision Intelligence
   authority ADR-007 explicitly withheld.

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly addresses
Phase 7.5 (goal-aware recommendation constraints) or Phase 7.6 (cross-goal
optimization) and names this record. It authorizes no implementation of
either stage.
