# ADR-011: Goal Objective Authority Foundation

**Status:** Accepted
**Date:** 2026-09-01
**Decision authority:** Human-approved Wealth OS Phase 7.6B architecture
decision
**Scope:** Architecture and governance only. No persistence, schema,
migration, API, UI, request field, or optimizer behavior is authorized by
this record.

---

## Context

[ADR-007](ADR-007_WEALTH_GOAL_AUTHORITY_AND_LEGACY_PORTFOLIO_GOAL_PROFILE_BOUNDARY.md)
named canonical Wealth Goal terminology, froze the Legacy Portfolio Goal
Profile, and ruled that `GoalFundingAllocation`'s factual many-to-many
cardinality "establishes no advisory or mandate cardinality." Its §7 blocked
Decision Intelligence from consuming Wealth Goal facts pending a dedicated
context-admission design.
[ADR-008](ADR-008_WEALTH_GOAL_DECISION_CONTEXT_ADMISSION.md) admitted
request-scoped Goal selection (`goal_ids`) as permanently `CONTEXT_ONLY`,
constructed strictly post-decision, granting no authority.
[ADR-009](ADR-009_GOAL_AWARE_RECOMMENDATION_CONSTRAINTS.md) authorized one
narrow, explicit, single-Goal, tightening-only exception: `target_date`,
admitted through `goal_constraint_goal_id`, may contribute a 20% maximum
single-position bound for a 0–365 day horizon.
[ADR-010](ADR-010_PORTFOLIO_INVESTMENT_MANDATE_FOUNDATION.md) authored
`PortfolioInvestmentMandate` as a purely factual, many-to-many Portfolio↔Goal
relationship, explicitly granting it zero behavioral authority, and named
Phase 7.6B, 7.6C, and 7.6D as the phases that would decide what, if
anything, a Goal's facts are permitted to mean to a decision.

Phase 7.6B is the first of those three. It asks the narrowest question left
open by ADR-007 through ADR-010: not what a Goal's investment intent *is*,
but **what rule governs whether any canonical Goal fact may ever acquire
behavioral authority, and how such authority would have to be granted.**

## Problem

Wealth OS already contains several canonical Wealth Goal facts —
`target_date`, `target_amount`, `priority`, `goal_type`, archive state, and
derived funding/designation/progress facts. Nothing about a fact being
canonical, persisted, derived, displayed, selected on a request, or attached
to a Portfolio through a Mandate currently states whether that fact is
permitted to change a decision outcome. ADR-009 already proves the platform
can grant a fact bounded behavioral authority through an explicit,
fact-specific decision — but no record states this as a general rule, which
leaves every future proposal to re-derive it from first principles, or worse,
to assume authority propagates from adjacent facts, relationships, or
visibility.

The architecture gap this record resolves is:

> Which semantic boundary governs when a canonical Wealth Goal fact may
> acquire behavioral authority?

This is not resolved by, and this ADR does not introduce: a
`GoalInvestmentObjective` entity or any categorical objective vocabulary; new
optimizer integration; or any other persisted resource. A prior planning pass
proposed such a resource and was corrected by independent architecture
review — the absence of a categorical Goal-objective field is not itself a
demonstrated gap, and this record does not reintroduce it.

## Decision

### 1. Canonical authority vocabulary

Five concepts govern this and all future Goal-fact authority questions, and
must not be collapsed into one another:

- **Canonical Goal fact** — a factual value owned by Wealth Intelligence,
  persisted or deterministically derived from canonical Goal data (for
  example: `target_date`, `target_amount`, `priority`, `goal_type`,
  funding/designation/progress facts, archive state). Being canonical grants
  source-of-truth status only. It grants no behavioral authority.
- **Fact authority** — architecture permission for a specific named fact to
  carry a specific decision meaning. It must be explicitly authorized. It
  does not propagate to other fields on the same Goal, to other Goals, from
  a Mandate, from funding or designation, or from request-scoped selection.
- **Admission** — the scoped contract through which an authorized fact is
  allowed into a particular decision context. Admission is fact- and
  use-case-specific; admitting one fact for one purpose does not admit the
  Goal, or that fact for any other purpose.
- **Behavioral authority** — permission for an admitted fact, under its
  authorized semantics, to alter a deterministic decision result: a
  constraint, a policy input, or a future objective input.
- **Optimizer consumption** — the concrete runtime mechanism through which
  authorized, admitted, behaviorally-authoritative Goal-derived semantics
  actually affect optimization or recommendation behavior.

> Canonical source of truth ≠ fact authority ≠ admission ≠ behavioral
> authority ≠ optimizer consumption.

### 2. Default non-authority rule

This is the central decision of this record:

> A canonical Wealth Goal fact does not possess behavioral authority merely
> because it exists, is persisted, is derived, is selected in a request,
> belongs to a mandated Goal, or is visible to Decision Intelligence.

Behavioral authority requires explicit, fact-specific architecture
authorization and a scoped admission contract, established at minimum by a
later ADR. This is a default rule, not a permanent prohibition: a future ADR
may explicitly authorize a specific Goal fact for a specific behavioral
purpose, following the procedure in §10.

### 3. Explicit non-inference rules

Behavioral authority is not inferred from any of the following. Each retains
exactly the factual semantics its own governing ADR already assigns it, and
gains nothing further from this record:

- Goal existence;
- `GoalFundingAllocation`, funding designation, funded amount, funding gap,
  or progress ratio;
- Portfolio Investment Mandate (ADR-010 §7 is unaffected and unextended by
  this record);
- Goal priority;
- Goal type;
- target amount;
- the Legacy Portfolio Goal Profile;
- `risk_personality`;
- generic `goal_ids` (ADR-008 `CONTEXT_ONLY` is unaffected);
- historical use of a field elsewhere in the codebase;
- mere availability to, or visibility from, Decision Intelligence.

### 4. ADR-009 exception preserved exactly

ADR-009 remains, unmodified, the sole currently-authorized Goal-derived
behavioral exception. Its boundary, restated without reinterpretation:
activation is explicit, through the request field `goal_constraint_goal_id`;
exactly one Goal may be activated; the admitted facts are limited to Goal
identity, archive state, and `target_date`; a 0–365 day horizon may
contribute a tightening-only 20% maximum single-position bound; it carries
no multi-Goal semantics and no general Goal-objective semantics; and it
grants no authority to any other fact, on that Goal or any other.

This record extracts only one general principle from ADR-009, and no more:

> A canonical Goal fact may acquire bounded behavioral authority through
> explicit, fact-specific architecture authorization and a scoped admission
> contract.

This is not generalized into a requirement, expectation, or recommendation
that Wealth OS build one generic admission engine. Whether a reusable
admission mechanism is ever worth building is a separate, open question this
record does not decide.

### 5. Current Goal-derived authority state

| Fact / Surface | Current Authority | Governing Boundary |
|---|---|---|
| `target_date` | Bounded, ADR-009 only | `goal_constraint_goal_id` activation |
| Derived horizon (days to target) | Bounded, ADR-009 only | Same as `target_date` |
| `target_amount` | No behavioral authority | — |
| `priority` | No behavioral authority | — |
| `goal_type` | No behavioral authority | — |
| Funding / designation / progress facts | Factual only | ADR-007 §5 |
| `is_archived` | Eligibility/lifecycle gate where predecessor rules use it (blocks new Mandate creation, blocks new ADR-009 activation); not investment-behavior content authority | ADR-009 §5, ADR-010 §4 |
| Portfolio Investment Mandate | Zero behavioral authority | ADR-010 §7 |
| Generic `goal_ids` | `CONTEXT_ONLY` | ADR-008 |
| `goal_constraint_goal_id` | Trigger for the ADR-009 exception only | ADR-009 |
| Legacy Portfolio Goal Profile | Frozen | ADR-007 §3 |
| `risk_personality` | No current authority | Remains unresolved; its final semantics and ownership remain open under ADR-007 |

> No general Goal-derived behavioral authority exists beyond explicitly
> authorized predecessor rules, currently ADR-009 only.

This statement does not imply optimizer inclusion, optimizer exclusion,
unrestricted optimization, recommendation availability or unavailability,
Mandate validity or invalidity, a default Portfolio strategy, or automatic
ADR-009 activation.

### 6. Portfolio Investment Mandate relationship

Portfolio Investment Mandate remains, exactly as ADR-010 defined it, a
factual Portfolio↔Goal relationship. A Mandate does not: admit Goal facts;
grant Goal facts authority; create an optimizer objective; choose a primary
Goal; create conflict precedence; or imply behavioral ownership of any Goal
fact by either the Portfolio or the relationship itself. This record does
not alter ADR-010. Any future change to Mandate behavioral semantics
requires architecture authority that explicitly reopens ADR-010, per that
record's own Reopen Conditions.

### 7. Multi-Goal boundary

This record authorizes no multi-Goal resolution behavior. Not authorized:
primary-Goal designation, first-Goal-wins, strictest-wins,
earliest-deadline-wins, priority ranking, min/max aggregation, averaging,
weighting, a blended objective, or any other conflict resolution. No
concrete cross-Goal behavioral conflict surface currently exists, because
ADR-009 remains single-Goal and this record introduces no second authority
for it to conflict with.

### 8. Phase 7.6C sequencing

> Closing Phase 7.6B does not automatically authorize or require Phase 7.6C
> architecture planning.

Phase 7.6C (Cross-Goal Conflict Policy) should be revisited only when at
least two concrete Goal-derived behavioral authorities may coexist or
conflict, or when another explicitly authorized proposal introduces a
genuine multi-Goal authority conflict surface. Until then, Cross-Goal
Conflict Policy planning is deferred as premature. This record does not
delete, redefine, or resolve the Phase 7.6C roadmap item.

### 9. Phase 7.6D boundary

Phase 7.6D (Cross-Goal Optimization Integration) remains future
optimizer-integration work. This record grants it no authority to begin. No
Goal fact beyond the ADR-009 exception is authorized for optimizer
consumption.

### 10. Future authority procedure

Before any currently factual Goal field may gain behavioral authority, a
future architecture proposal must establish, at minimum:

- the exact canonical fact;
- the reason behavioral authority is needed;
- the exact decision semantics;
- the admission contract;
- the consumer (where in the codebase the authority is actually exercised);
- the scope;
- the single-Goal vs. multi-Goal boundary;
- lifecycle/archive implications where relevant;
- audit/evidence requirements;
- interaction with predecessor ADRs (ADR-007 through ADR-010 and this
  record);
- interaction with any other existing Goal-derived authority.

This is an architecture requirement for how such a proposal must be framed,
not a new runtime framework, service, or validation mechanism.

## Rationale

- Every ADR in this chain (007–010) already independently enforces "no
  implicit authority" for its own surface; this record states that pattern
  once, generally, instead of leaving it to be re-derived ADR-by-ADR, which
  is what actually produced the risk an earlier planning pass fell into
  (assuming a new fact needed inventing to answer "objective authority"
  rather than recognizing the answer was a rule, not a resource).
- Naming the five-concept vocabulary (fact / fact authority / admission /
  behavioral authority / optimizer consumption) gives every future Goal-fact
  proposal, including Phase 7.6C and 7.6D, a stable, citable definition to
  build on instead of re-litigating terms each time.
- Extracting only the narrow principle from ADR-009 — not a generic
  admission engine — keeps this record from authorizing infrastructure no
  concrete use case yet justifies, consistent with this repository's
  "smallest structure that resolves the actual decision" pattern already
  used in ADR-010 §Rationale.
- Leaving Phase 7.6C sequencing conditional on an actual conflict surface
  existing, rather than scheduled by roadmap position alone, avoids planning
  a conflict-resolution policy for authorities that do not yet exist.

## Consequences

Positive:

- Prevents accidental authority-by-storage: a Goal fact cannot silently
  acquire decision meaning by being persisted, displayed, or linked through
  a Mandate.
- Prevents Portfolio Investment Mandate from becoming policy implicitly,
  reinforcing ADR-010 §7's permanent invariant rather than creating a
  second, competing statement of it.
- Creates stable vocabulary that Phase 7.6C, Phase 7.6D, and any future
  single-fact authority proposal (per §10) can cite directly instead of
  re-deriving.
- Makes future behavioral expansion auditable: every future grant of
  authority must be traceable to a specific ADR naming a specific fact.
- Protects ADR-008's `CONTEXT_ONLY` invariant and ADR-009's narrow,
  single-Goal scope from being read as precedent for broader authority.
- Avoids inventing objective schema, persistence, or vocabulary prematurely,
  ahead of any concrete consuming use case.

Tradeoffs:

- Every new Goal-derived behavioral use requires explicit architecture work;
  none can be added by implementation convenience alone.
- Some future proposals will require their own additional ADRs; this record
  does not pre-clear any of them.
- This record creates no direct user-visible capability — Phase 7.6B remains
  an architecture-governance milestone, not a shipped feature.
- Cross-Goal planning (Phase 7.6C) remains intentionally deferred until a
  concrete conflict surface exists, which may leave the roadmap item
  formally open for an extended period.

None of the above are treated as defects; they are the intended effect of
keeping behavioral authority explicit rather than ambient.

## Alternatives Considered

1. **Introduce a `GoalInvestmentObjective` entity now, with categorical
   values (e.g. GROWTH/INCOME/CAPITAL_PRESERVATION).** Rejected — this was
   the original planning proposal for this phase and was retracted after
   independent architecture review found no ADR-007 through ADR-010 clause,
   and no Roadmap text, that actually requires a new persisted resource;
   only a rule was required.
2. **Build a generic, reusable Goal-fact admission engine now, generalizing
   ADR-009's mechanism.** Rejected — no second concrete use case exists yet
   to generalize from; building one from a single instance risks guessing
   the wrong shape, and §4 explicitly declines to draw this conclusion from
   ADR-009 alone.
3. **Fold this vocabulary into ADR-009 as an amendment.** Rejected — ADR-009
   is scoped to one narrow exception and explicitly must not be reinterpreted
   as a general authority framework; amending it would blur that boundary
   this record is built to preserve.
4. **Skip a new ADR; document the vocabulary only in the Roadmap or an
   architecture note.** Considered and rejected for this decision, though a
   close call: this vocabulary is materially load-bearing for ADR-010 §7's
   reopening condition and for Phase 7.6C/7.6D, and an ADR gives it the same
   review durability as the boundaries it protects, rather than leaving it
   as prose a future edit could drift without the same scrutiny.
5. **Resolve Phase 7.6C (cross-Goal conflict) in the same record, since both
   are "Goal Objective Authority" by roadmap label.** Rejected — no concrete
   multi-Goal authority conflict exists yet for a conflict policy to
   resolve; deciding precedence rules now would manufacture heuristics no
   authorized decision has asked for, exactly what §7 of this record
   forbids.

## Explicit Non-Goals

This decision does not define or authorize: objective categories or
vocabulary of any kind; a `GoalInvestmentObjective` or any other new
persisted resource; any migration; any API; any UI; any runtime
implementation or request-field change; a generic reusable admission engine;
any new Goal-derived optimizer constraint beyond ADR-009's existing one;
optimizer integration; multi-Goal conflict policy, ranking, or weighting;
any behavioral semantics for Portfolio Investment Mandate; or resolution of
`risk_personality`'s open status. These remain Phase 7.6C, Phase 7.6D, or a
future single-fact authority proposal under §10.

## Relationship to Prior ADRs

- **ADR-007:** Unaffected and unextended. This record does not reopen the
  Legacy Portfolio Goal Profile freeze, does not resolve `risk_personality`,
  and does not alter §7's Decision Intelligence boundary — it operationalizes
  that boundary as a general rule rather than changing it.
- **ADR-008:** Unaffected. `CONTEXT_ONLY` and post-decision construction
  remain exactly as defined; this record grants `goal_ids` no new authority.
- **ADR-009:** Unaffected and not extended. Its single-Goal, tightening-only
  exception is restated accurately in §4 and is the only current instance
  of the general principle this record names — not a template this record
  requires future proposals to follow.
- **ADR-010:** Unaffected. Portfolio Investment Mandate remains purely
  factual with zero behavioral authority; this record does not reopen
  ADR-010 §7, and cannot substitute for the "later ADR that names this
  record" ADR-010 §7 requires to reopen it.

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly addresses
one or more of the following and names this record: a specific canonical
Goal fact is granted new behavioral authority under the §10 procedure; the
five-concept vocabulary in §1 requires revision; the ADR-009 exception is
extended, generalized, or joined by a second exception; a generic admission
mechanism is authorized; or Phase 7.6C or 7.6D is formally opened. Runtime
behavior, new UI language, or persisted data drift cannot amend it by
implication. This record authorizes no implementation beyond the vocabulary
and default rule stated in Decision §§1–10.
