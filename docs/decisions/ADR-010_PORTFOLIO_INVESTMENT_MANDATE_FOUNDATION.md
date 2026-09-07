# ADR-010: Portfolio Investment Mandate Foundation

**Status:** Accepted
**Date:** 2026-09-01
**Decision authority:** Human-approved Wealth OS Phase 7.6A architecture
decision
**Scope:** Architecture and governance only; no implementation exists yet.
Exact migration recipe, index selection, and HTTP status-code test coverage
are implementation decisions, not part of this record.

---

## Context

[ADR-007](ADR-007_WEALTH_GOAL_AUTHORITY_AND_LEGACY_PORTFOLIO_GOAL_PROFILE_BOUNDARY.md)
named "Portfolio Investment Mandate" as a future, distinct user-facing
concept and explicitly deferred it, leaving open (among others) **Open Human
Decision #2** ("what 'this Portfolio is managed for this Wealth Goal'
means") and **Open Human Decision #3** ("whether a Portfolio may have zero,
one, or many advisory-relevant Wealth Goals"). ADR-007 §5 separately ruled
that `GoalFundingAllocation` is factually many-to-many and that this factual
cardinality "establishes no advisory or mandate cardinality" — the factual
and advisory questions were deliberately kept apart.
[ADR-008](ADR-008_WEALTH_GOAL_DECISION_CONTEXT_ADMISSION.md) and
[ADR-009](ADR-009_GOAL_AWARE_RECOMMENDATION_CONSTRAINTS.md) since shipped
Phase 7.4 and 7.5 on a narrower, request-scoped, `CONTEXT_ONLY`/single-Goal
basis; neither persists a durable Portfolio↔Goal relationship, and neither
grants this decision any authority.

Phase 7.6A asks the narrowest possible question left over from ADR-007: may a
user explicitly author the durable *fact* that a Portfolio is managed for a
Goal, independent of and prior to any decision about what that fact is
allowed to do.

This is distinct from three existing surfaces:

- **`GoalFundingAllocation`** — a factual money designation ("this amount is
  designated toward this Goal"), not a management relationship (ADR-007 §5).
- **Legacy Portfolio Goal Profile** — a semantically frozen, portfolio-scoped
  compatibility contract (ADR-007 §3); not a canonical Goal and not this
  concept.
- **ADR-008/009 request-scoped Goal admission** (`goal_ids`,
  `goal_constraint_goal_id`) — per-request selections that create no
  cardinality or association between a Portfolio and a Goal, and that leave
  no durable record of "this Portfolio is managed for this Goal" once the
  request completes.

## Problem

Without a binding ruling, an implementation could plausibly: infer mandate
from funding-allocation overlap (exactly what ADR-007 §5 forbade); treat
request-scoped Goal selection as if it recorded a standing relationship;
reuse or rename the frozen Legacy Portfolio Goal Profile; invent priority,
weight, or optimizer-relevance fields on the new relationship before any
authority decision approves them; or silently let a factual many-to-many
schema decision be read as also deciding the separate advisory-cardinality
question ADR-007 #3 raised. Any of these would manufacture authority this
decision does not have standing to grant.

## Decision

### 1. Canonical semantics

One Portfolio Investment Mandate row means exactly:

> A user explicitly authored the current fact that this Portfolio is
> intentionally managed to serve this Wealth Goal.

Absence of a row means only that no such fact has been authored for that
Portfolio–Goal pair. Absence does not classify the Portfolio as unmanaged,
unrestricted, general-purpose, optimizer-included, optimizer-excluded, or
unrelated to Goals.

### 2. Factual cardinality only

Cardinality is many-to-many: a Portfolio may be linked to zero, one, or many
Wealth Goals; a Wealth Goal may be linked to zero, one, or many Portfolios;
each pair exists at most once. **This is factual cardinality only.** It does
not establish, and must not be read as having established:

- advisory cardinality;
- how many of a Portfolio's linked Goals, if any, may simultaneously carry
  behavioral or optimizer authority;
- primary/secondary Goal designation or priority; or
- optimizer participation, objective, or conflict behavior.

Those remain Phase 7.6B/7.6C questions, decided independently of this
record.

### 3. Persistence

A dedicated association, `PortfolioInvestmentMandate`
(`portfolio_investment_mandates`), carries only: `id`, `workspace_id`,
`portfolio_id`, `wealth_goal_id`, `created_at`, with
`UniqueConstraint(portfolio_id, wealth_goal_id)`. It carries no priority,
weight, percentage, allocation, objective, policy, role, risk, conflict, or
optimizer metadata, and no `updated_at` — a mandate row has no mutable field
once created, so there is nothing to timestamp.

Workspace integrity follows this repository's established pattern for
cross-entity association tables (`GoalFundingAllocation`,
`main.py::create_goal_funding_allocation`): the request's workspace is
resolved once, both the Portfolio and the Wealth Goal are resolved by
`id + workspace_id` before any write, and only then is the mandate row
created with that resolved workspace. There is no database-level
cross-table workspace constraint; correctness rests on scoped lookups
happening before every write, exactly as it already does for funding
allocations. Missing and foreign-workspace identifiers remain externally
indistinguishable, matching the same convention ADR-008 already relies on
for `goal_ids`.

### 4. Lifecycle

Create: explicit user action, one relationship at a time; a duplicate create
is idempotent; a new relationship to an archived Wealth Goal is rejected —
this mirrors the existing, unrelated precedent in
`create_goal_funding_allocation`, which already rejects new allocations
against an archived Goal.

Remove: explicit, individual, hard delete; repeated removal is idempotent;
an existing relationship whose Goal has since archived remains removable.

Portfolio delete: mandate rows for that Portfolio are removed. Both a
database-level `ondelete="CASCADE"` and an ORM-level
`cascade="all, delete-orphan"` relationship are required — not redundant —
because this repository's test suite builds schema via
`Base.metadata.create_all()` against SQLite, and SQLite does not enforce FK
actions without a PRAGMA this codebase does not set (the same reason
`Portfolio.goal_funding_allocations` already carries both).

Goal archive: an existing mandate survives, remains readable and removable;
no new mandate may be created against it; restoring the Goal mutates no
mandate row.

### 5. API idempotency, and why it differs from the nearest precedent

`GET/PUT/DELETE /portfolios/{portfolio_id}/investment-mandates[/{wealth_goal_id}]`,
portfolio-first only; no goal-first mutation endpoint, no bulk replace
endpoint, no optimizer request field.

- **PUT, relationship already exists:** returns the existing representation;
  no mutation occurs; the Goal having since archived does not turn this
  idempotent retry into a failure.
- **PUT, relationship does not exist and the Goal is archived:** `409`,
  because this would author a new relationship against an archived Goal.
- **DELETE, relationship already absent (parents still valid):** `204`,
  idempotent.

This intentionally differs from `update_goal_funding_allocation` (which
blocks even an update against an archived Goal) and
`delete_goal_funding_allocation` (which `404`s on a missing row): those
endpoints mutate a value (`allocated_amount`) and are keyed by a surrogate
row id, so a stricter, existence-sensitive contract is correct there. A
mandate PUT-retry mutates nothing, and mandate DELETE is addressed by the
natural `(portfolio_id, wealth_goal_id)` pair rather than a surrogate id, so
idempotent semantics are the correct contract here instead — not an
inconsistency with existing precedent, but the same "does this mutate a
value, and is it keyed naturally or by surrogate id" reasoning applied to a
different shape of resource.

### 6. No backfill

No mandate row may be derived from existing Portfolios, existing Wealth
Goals, `GoalFundingAllocation`, the Legacy Portfolio Goal Profile,
`goal_ids`, `goal_constraint_goal_id`, optimizer history, recommendation
snapshots, or any other existing evidence. The migration creates the new,
empty structure only; every existing Portfolio begins with zero explicitly
authored mandate facts. This ADR does not freeze
a specific migration revision identifier as domain semantics; the migration
chains onto whatever the current Alembic head is at implementation time
(verified at that time to be `e5f7a9b1c3d6`, with no other head present in
the 46-file revision graph).

### 7. Optimizer non-influence

The permanent invariant is behavioral, not literal:

> Portfolio Investment Mandates have no behavioral authority and cannot
> influence recommendation construction, policy, scoring, constraints,
> consensus, prompts, or optimizer output unless and until a later ADR
> explicitly reopens this record.

This is a permanent authority boundary, not a Phase 7.6A-only rule: behavioral
authority for mandates cannot be acquired implicitly by a later phase shipping
new code — it requires a later ADR that names this record, per Reopen
Conditions below.

Separately, for Phase 7.6A specifically, implementation must remain
structurally isolated from the *current pre-decision* recommendation path:
no mandate dependency in `agents/optimizer.py`,
`services/optimizer/constraint_resolver.py`,
`services/goal_recommendation_constraints.py`, or any other code reachable
before a recommendation is finalized. This is the current-phase
implementation requirement that enforces the permanent invariant above; it is
not the invariant itself, and a future phase's isolation surface may need to
expand as the recommendation pipeline changes. This ADR does **not** freeze a
permanent, whole-codebase "no code may ever query
`portfolio_investment_mandates`" rule: ADR-008 already established, for a
different table, that a strictly *post-decision* read (constructed only
after the recommendation already exists) is what makes non-influence
structural rather than conventional — that same pattern remains available
to a later, separately authorized phase for mandate data. Phase 7.6A
authorizes no such capture; it only requires that none exist yet.

### 8. Frontend

A minimum explicit-authoring surface on the active Portfolio UI: show
current mandate Goals; explicit add (offering only active Goals); explicit
remove (offered for archived-linked Goals too); no preselection, no
autosave, no inference, no funding-allocation coupling, no optimizer
coupling.

### 9. Non-inference invariants

- Goal designation ≠ Portfolio Investment Mandate.
- Request-scoped Goal selection (`goal_ids`, `goal_constraint_goal_id`) ≠
  Portfolio Investment Mandate.
- Legacy Portfolio Goal Profile ≠ Portfolio Investment Mandate.
- Funding-allocation mutations never mutate mandates, and mandate mutations
  never mutate funding allocations, Goals, or Portfolios.
- Optimizer requests never author or mutate mandates; frontend load or
  default rendering never authors a mandate.

## Rationale

- A dedicated, minimal association table is the smallest structure that can
  hold a durable factual relationship without smuggling in fields (weight,
  priority, role) that no approved decision yet authorizes.
- Many-to-many is the only cardinality that doesn't invent an exclusivity
  rule the human decision didn't ask for — a Portfolio genuinely can be
  managed for more than one Goal at once as a plain fact, independent of
  whether any of those Goals will later carry behavioral priority.
- Scoping the optimizer invariant to "no behavioral authority" rather than
  "no query, ever" keeps this ADR internally consistent with ADR-008's own
  reasoning about what makes non-influence structural, and avoids
  foreclosing a legitimate future ADR-008-shaped capture pattern that this
  ADR has no standing to rule on either way.
- Reusing this repository's existing workspace-scoped-lookup and
  archived-Goal-rejects-new-relationship precedents (from
  `GoalFundingAllocation`) rather than inventing new integrity mechanisms
  keeps the two closest association tables in this domain behaviorally
  consistent where their shapes are actually the same, and lets this record
  explain, rather than hide, the two places their contracts intentionally
  diverge.

## Consequences

- The platform gains one canonical, user-authored factual answer to "what
  Goal or Goals is this Portfolio managed for," resolving ADR-007 Open Human
  Decisions #2 and #3 in their factual sense only.
- The separate advisory/behavioral half of both of those open decisions —
  how many mandate Goals may carry priority, and what "managed for" means
  behaviorally — remains open, owned by Phase 7.6B and 7.6C, and receives no
  answer from this record.
- The optimizer, its policy, constraints, scoring, and consensus gain no new
  input; Phase 7.6A changes no recommendation.
- Existing Portfolios are unaffected until a user explicitly authors a
  mandate fact.
- Phase 7.6B, 7.6C, and 7.6D receive no authority from this ADR beyond the
  factual relationship it defines for them to build on.

## Alternatives Considered

1. **FK directly on `Portfolio` (single nullable `wealth_goal_id`) or on
   `WealthGoal`.** Rejected — forces a one-to-many or many-to-one shape the
   authorized decision does not ask for and cannot express a Portfolio
   managed for two Goals at once.
2. **One-to-one or one-to-many cardinality.** Rejected — no existing
   evidence or authorized decision supports an exclusivity rule; it would
   manufacture cardinality the same way ADR-007 §5 already ruled out for
   funding allocations.
3. **Reuse or extend `GoalFundingAllocation`.** Rejected — that table means
   a factual money designation (ADR-007 §5); overloading it with a
   management relationship would collapse two ADR-007 explicitly separated
   concepts into one.
4. **Rename or extend the Legacy Portfolio Goal Profile.** Rejected — ADR-007
   §3 froze that contract; this decision does not reopen it.
5. **Infer mandate from `goal_ids` or `goal_constraint_goal_id`.** Rejected —
   ADR-008 §2 and ADR-009 already rule that request-scoped selection creates
   no cardinality or association; inferring a durable fact from a per-request
   field would silently reverse that.
6. **Postpone persistence until Phase 7.6B/7.6D decide behavioral
   authority.** Rejected — the factual relationship is independently useful
   and independently decidable now; deferring it would block later phases on
   a question this one can already resolve.
7. **Bulk replace-set mutation endpoint.** Rejected — unnecessary for a
   foundation milestone with no priority or ordering semantics; individual
   create/remove is sufficient and simpler to make idempotent correctly.

## Explicit Non-Goals

This decision does not define: behavioral or advisory authority for any
mandate; optimizer objectives, constraints, or admission; cross-Goal
priority, conflict, tie, or gap resolution; goal-type or target-date policy
effects on a mandate; a Goal-first or bulk mutation API; or any migration,
synchronization, or inference between mandates and `GoalFundingAllocation`,
the Legacy Portfolio Goal Profile, or ADR-008/009 request-scoped selection.
These remain Phase 7.6B, 7.6C, and 7.6D questions.

## Relationship to Prior ADRs

- **ADR-007:** This decision explicitly names ADR-007 and resolves Open
  Human Decisions #2 and #3 — but only in their factual sense. It does not
  resolve, and does not claim to resolve, the advisory/behavioral half of
  either question; ADR-007's remaining boundaries (§7 Decision Intelligence
  boundary, §8 still-blocked list) stay fully intact and unaffected outside
  the narrow factual relationship defined here.
- **ADR-008:** Unaffected. This decision persists no request-scoped context
  and grants Phase 7.4's `CONTEXT_ONLY` admission no new authority.
- **ADR-009:** Unaffected. This decision grants Phase 7.5's single-Goal hard
  policy no new authority and activates no new constraint.

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly addresses
one or more of the following and names this record: mandate cardinality
must change; a mandate gains behavioral or optimizer meaning; mandate
history or audit trail becomes required; archive-interaction semantics
change; implicit derivation from another surface is proposed; or a mandate
becomes an optimizer input. Runtime behavior, new UI language, or persisted
data drift cannot amend it by implication. This ADR records no
implementation authorization beyond the factual structure and constraints
stated in Decision §§1–9.
