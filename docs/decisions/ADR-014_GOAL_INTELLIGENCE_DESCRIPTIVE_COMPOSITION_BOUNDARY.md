# ADR-014: Goal Intelligence Descriptive Composition Boundary

**Status:** Accepted
**Date:** 2026-09-08
**Decision authority:** Human-approved Wealth OS Phase 7.7 (Goal Intelligence
v1, Slice 1) architecture decision
**Scope:** The composition boundary and behavioral-authority status of
`wealth.goal-intelligence.v1`. Does not define goal health, success
probability, projection, affordability, or recommendation semantics.

---

## Context

[ADR-007](ADR-007_WEALTH_GOAL_AUTHORITY_AND_LEGACY_PORTFOLIO_GOAL_PROFILE_BOUNDARY.md)
named canonical `WealthGoal` and froze the Legacy Portfolio Goal Profile.
Phase 7.2's `services/goal_context.py` established valuation-free designation
facts (`designated_total`, `progress_ratio`, `funding_gap`,
`fully_designated`) per Goal. Phase 7.3A's `services/wealth_review.py`
composed those facts with persisted source valuation into per-*source*
coverage (`SUPPORTED` / `OVER_ALLOCATED`), still without inventing per-goal
attribution of a shared source's shortfall.
[ADR-011](ADR-011_GOAL_OBJECTIVE_AUTHORITY_FOUNDATION.md) then ratified the
general "default non-authority rule": no canonical Goal fact acquires
behavioral authority merely by existing, being derived, being persisted, or
being visible — authority requires an explicit, fact-specific future ADR.

Neither `goal_context.py` nor `wealth_review.py` exposes a single-Goal read
that also carries the Goal's own time horizon (`target_date`,
`days_remaining`) alongside its funding facts and the coverage evidence for
just its own funding sources. A reconnaissance pass (2026-09-08, this branch)
confirmed this composition does not exist yet, that both source services
remain unchanged and canonical, and proposed a minimal Slice 1 — one
read-only composed view, `wealth.goal-intelligence.v1` — built by joining
existing facts, not recomputing them.

## Problem

Without a binding ruling, a "Goal Intelligence" feature could plausibly:
collapse funding/time facts into an `on_track` / `at_risk` health enum;
attribute a shared source's `OVER_ALLOCATED` shortfall to one goal
specifically; recompute `designated_total` or `funding_gap` a second time
inside a new module, risking divergence from `goal_context.py`; or become an
input some future optimizer, Decision Intelligence, or evaluation change
reaches for simply because it exists and looks authoritative. Each of these
would either duplicate a rule ADR-004 says should have one implementation, or
grant behavioral authority ADR-011 says must be explicit — neither of which
this phase intends to do.

## Decision

### 1. Canonical domain

Goal Intelligence operates on canonical `WealthGoal` only. It does not
reinterpret, synchronize with, migrate from, or derive authority from the
frozen Legacy Portfolio Goal Profile (ADR-007 §3, unaffected and unextended).

### 2. Descriptive-only authority

`wealth.goal-intelligence.v1` is a read-only descriptive contract. Its
existence grants no behavioral authority to the optimizer, recommendation
constraints, Decision Intelligence, Execution Intelligence, or any
evaluation/scoring system. ADR-011's default non-authority rule (§2 of that
record) applies to every fact this contract exposes, including facts already
governed by ADR-011 §5 (funding/designation/progress remain factual only;
`target_date` and derived horizon remain bounded to the ADR-009 exception
only). Nothing in this record authorizes a second admission path for
`target_date` or horizon. Any future admission of a Goal Intelligence fact
into a behavioral system requires its own explicit ADR under ADR-011 §10.

### 3. Composition, not recalculation

Goal Intelligence composes existing canonical facts; it does not introduce
alternate implementations of goal designation totals, funding progress,
funding gap, source valuation, or source coverage. It reuses
`services/goal_context.py` for designation/funding facts and
`services/wealth_review.py` for source valuation/coverage facts, verbatim,
for the requested goal's own facts and its own funding sources' rows. The
only arithmetic this composition introduces is elapsed-day time arithmetic
(`days_remaining = target_date - as_of_date`) and its sign classification —
not a second implementation of any rule those two services already own.

### 4. Shared-source non-attribution

A funding source may fund more than one Goal. Goal Intelligence exposes the
canonical source-level coverage fact (`SUPPORTED` / `OVER_ALLOCATED` /
`UNAVAILABLE`) and the source's total designated amount across the reviewed
scope exactly as `wealth_review.py` computes them. It does not compute, infer,
or display which specific Goal is "actually short" when a shared source is
over-allocated across multiple Goals — that remains an explicitly undecided
question this record does not resolve.

### 5. Explicitly deferred semantics

This ADR does not define, and Slice 1 does not implement: `on_track` /
`attention` / `at_risk` or any other goal-health classification; probability
of success; goal success scoring; recommendation or advice of any kind;
required monthly contribution; projected target-date value; contribution
affordability; or cross-goal allocation priority/conflict resolution. A goal
health classification in particular is a deliberate departure from this
codebase's existing pattern of declining to ship collapsed health/status
scores (see `frontend/lib/emergencyFund.ts`, `frontend/lib/goalReviewCues.ts`)
and is not introduced by this record.

### 6. Projection boundary

`frontend/lib/goalWhatIf.ts` (closed-form monthly-compounding projection and
its required-contribution inverse) remains untouched and authoritative for
its current UI behavior. This record makes no decision about whether that
math is ever ported server-side; that remains open for a future record.

## Rationale

- Naming this boundary once, before implementation, follows the same pattern
  ADR-007 through ADR-011 already established for this domain: state the
  non-authority and non-duplication rules in a reviewable record rather than
  leaving them to be re-derived, or accidentally violated, during
  implementation.
- Citing ADR-011's default non-authority rule directly — rather than writing
  a new, parallel authority rule for Goal Intelligence specifically — avoids
  creating a second statement of the same governance principle that could
  drift from the original.
- Freezing the shared-source non-attribution boundary (§4) before
  implementation forecloses the single most tempting shortcut a
  single-Goal-scoped read invites: quietly implying the requesting Goal owns
  a shared source's entire shortfall.

## Consequences

Positive:

- `services/goal_intelligence.py` has an explicit, citable boundary before a
  single line of it is written: reuse `goal_context.py` and
  `wealth_review.py` verbatim, add only time arithmetic, grant no behavioral
  authority.
- Future proposals to let a Goal Intelligence fact influence a decision (the
  optimizer, Decision Intelligence, evaluation) must cite this record and
  ADR-011 §10 explicitly rather than treating the new endpoint's existence as
  implicit permission.
- The shared-source boundary prevents an easy-to-ship, hard-to-walk-back UI
  mistake: telling a user "this goal is short" when the shortfall is really a
  property of a source shared with another goal.

Tradeoffs:

- Slice 1 ships no goal-health signal, no projection, and no affordability
  view, even though those are the features most likely to be requested next;
  each requires its own future design and, for anything behavioral, its own
  ADR.
- Consumers of `wealth.goal-intelligence.v1` get raw composed facts, not a
  single collapsed judgment, which pushes interpretation back onto the UI
  layer for this phase.

## Alternatives Considered

1. **Add a lightweight `on_track` / `at_risk` field now, computed purely from
   `progress_ratio` and `days_remaining`, framed as "just descriptive."**
   Rejected — a two- or three-state classification is still a judgment call
   (what ratio counts as "on track" for what horizon), and this codebase has
   already declined that shape twice (`emergencyFund.ts`, `goalReviewCues.ts`).
   Introducing it here, casually, would contradict that pattern and this
   record's own §5.
2. **Recompute funding/coverage facts locally in `goal_intelligence.py` for
   convenience (e.g., to avoid a second query against `wealth_review.py`'s
   workspace-wide shape).** Rejected — this is exactly the duplicated-rule
   risk ADR-004 exists to prevent; §3 requires verbatim reuse instead.
3. **Silently attribute a shared source's `OVER_ALLOCATED` shortfall to
   whichever Goal is being requested, since the read is single-Goal-scoped
   anyway.** Rejected — this would assert a per-goal fact the ledger does not
   support, the same category of mistake ADR-013 rejected for Net Worth
   attribution and ADR-012 rejected for cash/investment funding-transfer
   matching.

## Explicit Non-Goals

This decision does not define or authorize: any goal-health enum or score;
success probability; required monthly contribution; projected target-date
value; contribution affordability; cross-goal prioritization, ranking, or
conflict resolution; any new optimizer constraint; any new Decision
Intelligence or Execution Intelligence consumption of Goal Intelligence
facts; any migration; or any change to `goalWhatIf.ts`,
`goalAffordability.ts`, `goalReviewCues.ts`, `decision_goal_context.py`, or
`goal_recommendation_constraints.py`.

## Relationship to Prior ADRs

- **ADR-007:** Unaffected and unextended. The Legacy Portfolio Goal Profile
  freeze and the canonical-Wealth-Goal naming are unchanged.
- **ADR-009:** Unaffected and not extended. Its single-Goal, tightening-only
  `target_date` exception remains the sole current behavioral use of
  `target_date`/horizon; Goal Intelligence's own `days_remaining` field is
  descriptive only and creates no second admission path.
- **ADR-011:** This record operationalizes, for one new composed read, the
  default non-authority rule ADR-011 §2 already states generally. It grants
  no fact new authority and does not reopen ADR-011.
- **ADR-013:** This record follows the same "expose the honest, narrower
  fact rather than an inferred one" posture ADR-013 used for Net Worth
  change attribution, applied here to shared-source coverage (§4).

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly addresses
one or more of the following and names this record: a specific Goal
Intelligence fact is granted behavioral authority under ADR-011 §10; a goal
health classification, success probability, or scoring signal is authorized;
`goalWhatIf.ts`'s projection math is authorized to move server-side; a
per-goal attribution of shared-source shortfall is authorized; or the
composition boundary in §3 changes. Runtime behavior, new UI language, or
persisted data drift cannot amend it by implication.
