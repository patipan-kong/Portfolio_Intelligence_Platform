# ADR-016: Shared Funding-Source Transparency Boundary

**Status:** Accepted
**Date:** 2026-09-08
**Decision authority:** Human-approved Wealth OS Phase 6 (Shared
Funding-Source Transparency, Slice 1) architecture decision
**Scope:** Whether, and under what boundary, Wealth OS may disclose which
Wealth Goals share a single funding source and each Goal's own designated
amount toward it. Does not define per-goal shortfall attribution,
prioritization, conflict resolution, or any contribution/allocation
authority.

---

## Context

[ADR-014](ADR-014_GOAL_INTELLIGENCE_DESCRIPTIVE_COMPOSITION_BOUNDARY.md) §4
established that a funding source may fund more than one Wealth Goal, and
that `services/wealth_review.py`'s source-level `designation_coverage`
(`SUPPORTED` / `OVER_ALLOCATED` / `UNAVAILABLE`) never attributes a shared
source's shortfall to one specific Goal — but explicitly left open, as an
undecided question, whether and how Wealth OS may disclose *which* Goals
share a source and *what each one designates*, as distinct from attributing
fault for a shortfall between them.

A reconnaissance pass (2026-09-08, this branch) found that `/goals`' existing
"Funding source health" section already renders, per source, the canonical
`designated_total_in_context_scope` and `designation_coverage` computed by
`wealth_review.py` — but does not show the individual Goals composing that
total, even though `services/goal_context.py`'s `build_workspace_goal_context`
already returns, in the same response, each Goal's own `allocations` (each
carrying `source_kind`, `source_id`, and `designated_amount`). A user with two
or more Goals designating against the same Cash Account or Portfolio
currently cannot see that relationship without manually cross-referencing
each Goal individually — most acutely when the source is `OVER_ALLOCATED`
and the user cannot tell, from `/goals` alone, which Goals are drawing on it
or by how much.

## Problem

Without a binding ruling, a "shared source breakdown" feature could
plausibly cross the exact line ADR-014 §4 declined to cross: allocating an
`OVER_ALLOCATED` source's shortfall across the Goals sharing it (equally, or
in proportion to each Goal's designation), implying a priority or ranking
through display order, or feeding this composed view into a future
optimizer, Decision Intelligence, or recommendation surface simply because it
exists and looks authoritative. Any of these would grant behavioral or
interpretive authority ADR-011's default non-authority rule says must be
explicit, or assert a per-goal fact the ledger does not support — the same
category of mistake ADR-012 and ADR-013 already declined for cash/investment
funding-transfer matching and Net Worth change attribution respectively.

## Decision

### 1. Canonical source-level fact, disclosed per Goal

A funding source may be designated across multiple Wealth Goals. Wealth OS
may disclose, for such a source: which Goals designate to it, each Goal's own
`designated_amount` toward it, the source-wide designated total, the source's
valuation/evidence state, and the source-level `designation_coverage`. These
are descriptive facts already computed by `goal_context.py` and
`wealth_review.py`; this record authorizes composing and displaying them
together, not computing anything new.

### 2. No per-goal shortfall attribution

If Goal A designates 80 and Goal B designates 90 against a source valued at
100, the source may report a total designated of 170 and a shortfall of 70,
and the breakdown may show A = 80 and B = 90 — but Wealth OS must **not**
state that Goal A or Goal B is short by any amount, or that either Goal owns
any share of the 70 shortfall, unless a future explicit allocation authority
is introduced under §10 of ADR-011.

### 3. No priority semantics

The order in which Goals sharing a source are listed must not imply
importance, funding priority, a recommendation, or which Goal should be
reduced or funded first. Any ordering used for display stability (e.g., by
Goal name) is presentation-only and carries no behavioral meaning.

### 4. No behavioral authority

This view grants no behavioral authority to the optimizer, Decision
Intelligence, Execution Intelligence, Evaluation, or any automated
recommendation generation. ADR-011's default non-authority rule applies
unchanged to every fact this view discloses.

### 5. Composition, not recalculation

The shared-source breakdown composes existing canonical facts — each Goal's
own allocations from `goal_context.py`, joined by `(source_kind, source_id)`
to the source-level rows `wealth_review.py` already computes. It introduces
no independent implementation of designated totals, source valuation,
coverage, or shortfall, and no new backend query, endpoint, or persisted
table: the composition is a presentation-layer join over data the existing
`wealth.factual-review.v1` response already returns in one call.

### 6. Reconciling scope, including archived Goals

`/goals` requests the factual review with `include_archived=true`, so its
displayed source totals already include any archived Goal's designation. The
breakdown must reflect that same scope — an archived Goal sharing a source is
shown (labeled archived), not silently omitted — so the visible breakdown
always reconciles exactly with the total already displayed next to it.

### 7. Discharge of ADR-014's deferred question

This record resolves the presentation half of ADR-014 §4's open question:
Wealth OS may disclose which Goals share a funding source and each Goal's own
designation. ADR-014 §4's non-attribution rule itself is not modified — it is
restated here (§2) and extended with the ordering (§3) and scope (§6) detail
needed to implement disclosure safely. ADR-014 is not otherwise modified.

### 8. Explicitly deferred

This record does not authorize: cross-goal prioritization or ranking; any
allocation or apportionment of a shared source's value or shortfall between
Goals; suggested or automatic reallocation; a contribution or commitment
plan; goal-health classification; or any optimizer, Decision Intelligence, or
Execution Intelligence consumption of this view. Reopening any of these
requires its own explicit ADR that names this record, per ADR-011 §10.

## Rationale

- ADR-014 §4 named this exact disclosure question and deliberately left it
  open rather than deciding it implicitly during Slice 1's implementation;
  this record follows the same pattern the Goal domain's ADR chain has used
  throughout (ADR-007 through ADR-015) of freezing a boundary before writing
  the code that could otherwise drift across it.
- The two facts needed for disclosure — per-goal allocations and per-source
  coverage — are both already canonical and already returned in the same API
  response consumed by `/goals`; the only genuine design question was the
  attribution boundary, not the data's existence or trustworthiness.
- Freezing the non-attribution and non-priority rules (§2–§3) before
  implementation forecloses the same easy-to-ship, hard-to-walk-back mistake
  ADR-014 §4 already identified: implying one Goal in a shared-source list is
  "the problem."

## Consequences

Positive:

- Users with Goals sharing a funding source can see that relationship
  directly on `/goals`, closing a real, previously named gap, without any new
  backend surface or persisted state.
- The disclosure boundary is explicit and citable before implementation,
  matching this repository's established pattern for the Goal domain.
- No new duplicated arithmetic is introduced anywhere in the stack.

Tradeoffs:

- Users still cannot ask Wealth OS "which Goal should I reduce" when a source
  is over-allocated — that judgment remains entirely theirs, by design.
- The breakdown surfaces archived Goals' designations where they exist,
  which may show more detail than a user expects on first encounter; this is
  accepted because omitting them would make the displayed total
  unreconcilable, which is a worse outcome.

## Alternatives Considered

1. **Attribute the shortfall proportionally to each Goal's designation share
   (e.g., Goal A owns 80/170 of the 70 shortfall).** Rejected — this asserts
   a per-goal fact the ledger does not support, the exact mistake ADR-014 §4
   already declined, and it would imply a resolution policy (proportional
   apportionment) that has never been decided as a product behavior.
2. **Omit archived Goals from the breakdown to keep the list "clean."**
   Rejected — the displayed source-wide total already includes archived
   Goals' designations (per the page's `include_archived=true` request), so
   omitting them from the breakdown would make the visible numbers fail to
   reconcile, which is a worse transparency failure than showing an archived
   label.
3. **Defer this entirely until a Goal Contribution Planning or cross-goal
   priority feature exists, on the theory that shared-source visibility is
   only useful alongside those.** Rejected — the disclosure itself has
   standalone value (a user can act on this information today, e.g. by
   manually adjusting one Goal's target or designation), and gating it behind
   unrelated, unscoped future work would leave a known gap open with no
   articulated reason tied to this feature specifically.

## Explicit Non-Goals

This decision does not define or authorize: per-goal shortfall attribution or
apportionment; cross-goal prioritization, ranking, or conflict resolution;
suggested or automatic reallocation of a shared source's value; a
contribution or commitment plan; goal-health classification, success
probability, or scoring; any new backend endpoint, schema, or migration; or
any optimizer, Decision Intelligence, or Execution Intelligence consumption
of this view.

## Relationship to Prior ADRs

- **ADR-011:** This record operationalizes the default non-authority rule for
  one new composed presentation view. It grants no fact new authority and
  does not reopen ADR-011.
- **ADR-014:** This record discharges ADR-014 §4's open disclosure question by
  authorizing presentation of the shared-goal breakdown, while restating and
  preserving its non-attribution rule unchanged. ADR-014 is not otherwise
  modified.
- **ADR-012 / ADR-013:** This record follows the same "expose the honest,
  narrower fact rather than an inferred one" posture those records used for
  funding-transfer matching and Net Worth change attribution, applied here to
  shared-source disclosure.

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly addresses one
or more of the following and names this record: a specific per-goal
shortfall-attribution or allocation authority is authorized under ADR-011
§10; cross-goal prioritization or conflict resolution (Phase 7.6C) is
authorized and needs to define how it interacts with this view; or the
composition boundary in §5 changes (e.g., a new backend endpoint is
introduced for this data). Runtime behavior, new UI language, or persisted
data drift cannot amend this record by implication.
