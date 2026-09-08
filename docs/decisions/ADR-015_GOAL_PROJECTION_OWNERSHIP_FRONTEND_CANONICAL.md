# ADR-015: Goal Projection Ownership: Frontend Canonical Under Current Product Boundary

**Status:** Accepted
**Date:** 2026-09-08
**Decision authority:** Human-approved Wealth OS Phase 7.7 (Goal Intelligence
v1, Slice 2) architecture decision
**Scope:** Which runtime is the authoritative implementation of Goal
scenario projection and required-monthly-contribution calculation, and under
what condition that could change. Does not define goal health, projection
persistence, scenario-selection authority, affordability, or recommendation
semantics.

---

## Context

[ADR-014](ADR-014_GOAL_INTELLIGENCE_DESCRIPTIVE_COMPOSITION_BOUNDARY.md) §6
left one question explicitly open: `frontend/lib/goalWhatIf.ts` "remains
untouched and authoritative for its current UI behavior. This record makes
no decision about whether that math is ever ported server-side; that remains
open for a future record." Its Reopen Conditions named
"`goalWhatIf.ts`'s projection math is authorized to move server-side" as one
of the specific conditions requiring a superseding ADR that names ADR-014
explicitly.

A reconnaissance pass (2026-09-08, this branch) reconstructed the full
mathematical contract of `goalWhatIf.ts` and every consumer that calls it
(`GoalPlanningSections.tsx`'s `GoalWhatIfSection` and
`ScenarioComparisonTable`, `goalAffordability.ts`, `scenarioComparison.ts`),
the complete `GoalScenario` persistence model, and the repository's existing
precedent for calculation ownership across the frontend/backend boundary.
That reconnaissance found: every What-If and required-contribution result is
computed synchronously client-side and is presentational only — no result is
persisted, and no optimizer, recommendation, Decision Intelligence, or
Execution Intelligence consumer reads any of them; `GoalScenario` persists
only `name`, `monthly_contribution`, `annual_return_pct`, and
`is_archived` — an explicit assumption set, never a forecast, snapshot, or
optimizer input, with no default/active-scenario concept and no restriction
on how many scenarios may coexist; and no other module in
`frontend/lib/` independently re-derives a backend business rule from raw
records — every other case either renders a backend-computed value directly
or performs trivial composition over already-server-aggregated numbers
(e.g. `netWorth.ts`). `goalWhatIf.ts` is the sole exception, by ADR-014's own
design. No backend Python module implements equivalent compounding or
annuity math, and no cross-runtime parity-test or golden-vector
infrastructure exists anywhere in this repository.

## Problem

Without a binding ruling, Goal Intelligence's existence could be read as
implicit permission to add a second, backend implementation of projection or
required-contribution math — either to "complete" the Goal Intelligence
contract, or because a future backend consumer looks for it and finds none.
Any such addition would either (a) duplicate the exact closed-form
compounding/annuity rule `goalWhatIf.ts` already owns, which is the category
of mistake [ADR-004](ADR-004_ONE_IMPLEMENTATION_PER_RULE.md) exists to
prevent, or (b) invent a materially different, simplified calculation under
the same product label, silently diverging from what the interactive UI
promises the user. A related but separable risk is that a future
implementation could treat a `GoalScenario`'s saved assumptions as if they
were the canonical forecast for a Goal, when no such canonical assumption
set exists today.

## Decision

### 1. Current canonical owner

Under the current product boundary, `frontend/lib/goalWhatIf.ts` is the sole
authoritative implementation of:

- deterministic goal scenario projection (`computeGoalWhatIf`)
- inverse required-monthly-contribution calculation
  (`computeRequiredMonthlyContribution`)

No equivalent backend implementation is authorized at this time. This is an
explicit architecture decision, not an accidental gap.

### 2. Grounds for frontend ownership today

- What-If is interactive, transient presentation behavior: it recomputes
  synchronously on every relevant keystroke or slider change against live
  component state, with no debounce and no network dependency.
- No calculated projection or required-contribution result is persisted
  anywhere.
- No optimizer, recommendation, Decision Intelligence, or Execution
  Intelligence consumer uses any result this math produces.
- No genuine non-browser consumer currently requires this calculation.
- `GoalScenario` stores assumptions only — explicitly not a forecast,
  probability, recommendation, optimizer input, or saved projection.
- No active or default `GoalScenario` concept exists; multiple scenarios may
  coexist with no uniqueness constraint on their assumptions.
- Because no canonical assumption set exists, Goal Intelligence has no basis
  on which to automatically select assumptions and produce a canonical
  projected outcome, even if it wanted to.

### 3. Observable semantics frozen, not implementation

The following externally observable behaviors are the product contract this
decision protects, and must survive unchanged if this decision is ever
reopened:

- monthly compounding
- end-of-month contribution timing
- calendar-month anniversary horizon behavior, with month-end clamping
  (including leap-year handling)
- accepts any finite annual return greater than `-100%`, including negative
  returns
- exact linear behavior at 0% return
- already-funded short-circuit (zero months, zero required contribution)
- bounded reachability horizon (unreachable is a defined result, not an
  unbounded search)
- required contribution rounds up to the nearest safe satang
- the inverse result is verified to actually reach the target, not merely
  algebraically implied
- invalid input returns an explicit invalid-result shape rather than silent
  coercion or a thrown exception

The specific numerical techniques used to produce these results — `log1p` /
`expm1` closed-form evaluation, the binary-search verification step — are
implementation mechanism, not product semantics, and may change freely as
long as the observable results above do not.

### 4. Scenario math, not forecast

This calculation means: given explicit assumptions supplied by the user,
what mathematical outcome follows under those assumptions. It does not mean:
what Wealth OS predicts will actually happen. Its outputs are therefore not,
by virtue of existing, forecasts, predictions, probabilities,
recommendations, advice, optimizer inputs, or Goal Intelligence facts with
behavioral authority. [ADR-011](ADR-011_GOAL_OBJECTIVE_AUTHORITY_FOUNDATION.md)'s
default non-authority rule and ADR-014's descriptive-only boundary both
apply unchanged; this record grants no new authority to any Goal
Intelligence fact.

### 5. Discharge of ADR-014's deferred question

This record resolves ADR-014 §6 and its "projection math is authorized to
move server-side" Reopen Condition: projection math remains frontend-owned,
no backend port is authorized by this decision, and Goal Intelligence Slice
1 remains factual/descriptive and projection-free. ADR-014 itself is not
modified; this record supersedes only the specific open question it named,
by reference.

### 6. Scenario-selection authority remains separate and ungranted

Projection ownership and scenario-selection authority are separate
questions. Even where this math is available, no component may infer that a
saved `GoalScenario` is the canonical projection assumption for a Goal —
there is no active or default scenario, and none is created by this record.
Goal Intelligence or any other system must not automatically select a
`GoalScenario` (first, latest, or otherwise) to stand in for a canonical
assumption set without its own separate, explicit product and architecture
decision. This forecloses a future implementation reasoning "the math
already exists on the backend, so just apply it to whichever scenario is
most recent."

## Rationale

- The repository has exactly one precedent shape for this kind of
  calculation ownership question — every other frontend module either
  renders or trivially composes backend-computed aggregates — and
  `goalWhatIf.ts` was already named, deliberately, as the sole exception in
  ADR-014 §6. This record ratifies that exception rather than quietly
  eroding it.
- ADR-004's "one implementation per rule" doctrine originates entirely from
  intra-backend duplication (three Python engines independently computing
  the same period-return fields) and has never been applied across the
  TypeScript/Python runtime boundary in this codebase. Introducing a second,
  cross-runtime implementation of the same closed-form formula today would
  be the first instance of exactly the failure mode ADR-004 exists to
  prevent, without any present consumer requiring it.
- A split-authority model, where the backend owns a narrower "projection
  primitive" while the frontend keeps its interactive copy, was considered
  and rejected: any such backend primitive would necessarily reproduce the
  identical monthly-rate derivation and annuity factor, which is
  same-formula-different-caller duplication, not a genuine semantic
  boundary.

## Consequences

Positive:

- The interactive What-If UX is fully preserved — no round trip, no
  debounce, no dual-authority risk between a local preview and a server
  confirmation.
- No migration, parity-test infrastructure, or golden-vector suite is
  required now, because none is being introduced.
- A future contributor cannot treat Goal Intelligence's existence as
  implicit permission to add a second implementation of this math; this
  record must be cited and superseded first.

Tradeoffs:

- No non-browser surface (report generation, notification/digest, backend
  evaluation) can reuse this calculation today; each such need must wait for
  a future decision under this record's reopen condition.
- Goal Intelligence's descriptive contract remains projection-free, matching
  ADR-014 §5's existing scope rather than expanding it.

## Alternatives Considered

1. **Port the calculation to the backend now (backend canonical).** Rejected
   — no current backend or non-browser consumer requires it; porting the
   full documented edge-case contract (leap years, month-end clamping,
   satang rounding, bounded-reachability search, forward-verified inverse)
   is a real correctness-risk migration; and making What-If backend-canonical
   would either force a network round trip per interactive input or require
   keeping a duplicate client-side copy anyway, defeating the purpose.
2. **Maintain parallel TypeScript and Python implementations reconciled by
   golden vectors (dual-runtime with parity tests).** Rejected for the
   current state — this is still two implementations of one rule, this
   repository has no existing cross-runtime financial-math parity
   infrastructure to build on, and it would impose a permanent
   synchronization burden with no present consumer to justify it.
3. **Split frontend/backend projection primitives (Model D).** Rejected —
   the backend primitive under any credible design would compute the same
   economic quantity via the same formula as the frontend, which is
   duplication under a different name rather than a genuinely separate
   responsibility. No second implementation is created merely because Goal
   Intelligence now exists.

## Explicit Non-Goals

This decision does not define or authorize: any change to the observable
mathematical behavior of `goalWhatIf.ts`; any backend implementation of
projection or required-contribution math; any new API contract, endpoint, or
Goal Intelligence field; any `GoalScenario` schema, default-scenario, or
active-scenario concept; any automatic selection of a `GoalScenario` by any
system; any golden-vector fixture or cross-runtime parity test; goal health
classification, success probability, affordability as a feature,
cross-guide prioritization, or any optimizer/Decision Intelligence/Execution
Intelligence consumption of projection results.

## Relationship to Prior ADRs

- **ADR-004:** This record treats ADR-004's "one implementation per rule"
  doctrine as the reason a second, cross-runtime implementation of the same
  projection formula is not introduced now, extending that doctrine's
  application to the frontend/backend boundary for the first time in this
  repository, in the negative direction (declining to duplicate) rather than
  by consolidating an existing duplication.
- **ADR-011:** Unaffected and not extended. The default non-authority rule
  continues to apply to every fact `goalWhatIf.ts` or any future projection
  surface produces; this record grants no fact new behavioral authority.
- **ADR-014:** This record discharges ADR-014 §6's deferred question and its
  "projection math is authorized to move server-side" Reopen Condition by
  explicitly declining to authorize a server-side port at this time.
  ADR-014's descriptive composition boundary, its shared-source
  non-attribution rule, and its own Explicit Non-Goals are otherwise
  unaffected and unextended. ADR-014 is not modified by this record.

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly addresses
one or more of the following and names this record: a genuine non-browser
consumer (a server-generated report, a notification or digest, a backend
evaluation, or similar) requires this calculation outside the frontend
runtime. A hypothetical future consumer alone is insufficient; the
qualifying requirement must be real. If reopened, the superseding decision
must, at minimum: make an explicit new architecture decision rather than
treating the change as incidental; define a versioned projection contract;
port the complete observable semantics documented in §3 above, not a
simplified subset; build comprehensive cross-runtime golden vectors covering
at least zero/positive/negative return, already-funded, zero starting value,
zero contribution, one-month and multi-year horizons, leap-year behavior,
month-end clamping, past target date, unreachable horizon,
growth-alone-reaches-target, and satang rounding boundary cases; prove
parity before changing authority; migrate consumers deliberately; and retire
duplicate authority rather than leaving two canonical implementations
indefinitely. Separately and independently, any future decision to let Goal
Intelligence or any other system automatically select a `GoalScenario` as a
canonical assumption set requires its own explicit product and architecture
decision — reopening this record alone does not grant that authority.
Runtime behavior, new UI language, or persisted data drift cannot amend this
record by implication.
