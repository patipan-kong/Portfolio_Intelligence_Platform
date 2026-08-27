# ADR-007: Wealth Goal Authority and Legacy Portfolio Goal Profile Boundary

**Status:** Accepted
**Date:** 2026-08-27
**Decision authority:** Human-approved Wealth OS Phase 7.1 architecture decision
**Scope:** Architecture and governance only; no runtime, schema, API, data, or
optimizer authority

---

## Context

Phase 6 introduced workspace-owned `WealthGoal` objects and explicit
`GoalFundingAllocation` designations. The older Portfolio Goal Profile remains
in the product as five nullable fields on `Portfolio`, exposed through
`/portfolios/{id}/goal` and `/portfolios/{id}/goal-profile` and rendered by the
Goal Discovery Wizard and Operations Center.

The two surfaces use overlapping life-goal language but have separate storage,
vocabularies, and behavior:

- `WealthGoal` carries a goal type, target amount, optional target date, and
  priority at workspace scope.
- the Portfolio Goal Profile carries `goal_type`, `goal_priority`,
  `goal_target_date`, `goal_target_value`, and `risk_personality` at portfolio
  scope;
- mutations of either surface do not synchronize or mutate the other;
- a funding source may designate amounts to several Wealth Goals, and a Wealth
  Goal may receive designations from several Cash Accounts and/or Portfolios;
- the Operations Center computes its existing portfolio progress percentage
  from latest `PortfolioSnapshot.total_value / Portfolio.goal_target_value`;
  and
- neither surface is consumed by the current optimizer. The optimizer does
  consume the separate `Portfolio.strategy_persona`, portfolio settings,
  resolved constraints, policy, regime, and execution context.

This creates a naming and authority collision that must be resolved before
Phase 7 introduces factual goal context or goal-aware advice.

The governing evidence is:

- [Platform Architecture](../architecture/platform_architecture.md), especially
  §§6.5, 6.6, 6.8, 11, and 12;
- [Canonical Glossary](../GLOSSARY.md), especially Goal Target, Portfolio
  Strategy Metadata, Decision Policy, and Persona;
- [Portfolio Domain Model](../architecture/PORTFOLIO_DOMAIN_MODEL.md), whose
  older goal-profile statements are classified below;
- [Wealth OS Product Roadmap](../architecture/ROADMAP.md), Phase 6 and Phase 7;
- [Optimizer Philosophy](../investment/OPTIMIZER_PHILOSOPHY.md);
- `backend/models/database.py`, `backend/main.py`,
  `backend/services/goal_profile.py`, and
  `backend/services/operations_center.py`;
- `backend/services/optimizer/`, `backend/agents/optimizer.py`, and the live
  optimizer call path in `backend/main.py`;
- `frontend/components/goal/GoalWizard.tsx`,
  `frontend/components/operations-center/muji/GoalProfileCard.tsx`,
  `frontend/app/goals/`, and `frontend/lib/api.ts`; and
- `backend/tests/test_wealth_goals.py` and
  `backend/tests/test_goal_funding_allocations.py`.

## Problem

Without a binding boundary, later work could silently choose any of several
incompatible interpretations: treat the legacy profile as a second canonical
goal, rename it wholesale as an Investment Mandate, infer mandate from a
funding designation, map incompatible enums during an automatic migration, or
feed ambiguous goal and risk fields into Decision Intelligence. Any of those
choices would manufacture authority that the current data and product do not
possess.

## Decision

### 1. Canonical terminology

This decision uses the terms registered in the canonical glossary:

| Term | Binding Phase 7.1 ruling |
| --- | --- |
| [Wealth Goal](../GLOSSARY.md#wealth-goal) | The sole canonical workspace-level life or financial objective. Canonical goal type, target amount, target date, and priority belong here. |
| [Legacy Portfolio Goal Profile](../GLOSSARY.md#legacy-portfolio-goal-profile) | The current mixed compatibility contract. It is not a canonical Goal and is semantically frozen. |
| [Portfolio Investment Mandate](../GLOSSARY.md#portfolio-investment-mandate) | A future, distinct user-facing concept describing why and how a Portfolio is managed. It is not an alias or wholesale rename for the legacy profile. |

Examples such as retirement, FIRE, a house, a wedding, and education are
Wealth Goals when represented as whole-life financial objectives.

### 2. Semantic authority

| Concern | Semantic authority | Phase 7.1 boundary |
| --- | --- | --- |
| Life-goal facts: type, target amount, target date, priority | Wealth Intelligence, through Wealth Goal | Portfolio fields may retain historical values but do not author new Wealth Intelligence meaning. |
| Funding designations | Wealth Intelligence, through `GoalFundingAllocation` | A factual amount designation only; no money movement, policy, mandate, or advice. |
| Portfolio Strategy Metadata | Portfolio Intelligence | Remains distinct from Goal Target and Decision Policy. |
| Enforceable constraints and Decision Policy | Decision Intelligence | No goal field becomes enforceable merely by being stored, displayed, or designated. |
| `risk_personality` | Unresolved | It is not classified as canonical user risk tolerance, risk capacity, portfolio risk policy, optimizer policy, a `strategy_persona` replacement, or a Wealth Goal fact. |
| Future Portfolio Investment Mandate context | No monolithic semantic owner is approved | It must compose references without absorbing authority: Portfolio Strategy Metadata remains Portfolio Intelligence-owned, enforceable Decision Policy remains Decision Intelligence-owned, and life-goal facts remain Wealth Intelligence-owned. Association semantics and the owner of any assembled read context require later design. |
| Legacy Portfolio Goal Profile compatibility | Existing Portfolio storage/API/runtime stewardship only | Preservation grants no canonical semantic authority and no authority to reinterpret historical values. |

No future mandate object may become a broad authority object merely because it
assembles these references for presentation.

### 3. Legacy field disposition

The current Portfolio Goal Profile remains stored exactly as it is. Its fields
are classified as follows:

| Existing field | Phase 7.1 classification | Disposition |
| --- | --- | --- |
| `goal_type` | Legacy duplication of a life-goal concept | Preserve; do not migrate, map, synchronize, or reinterpret. |
| `goal_priority` | Legacy duplication of a life-goal concept | Preserve; do not migrate, map, synchronize, or reinterpret. |
| `goal_target_date` | Legacy duplication of a life-goal concept | Preserve; do not migrate, synchronize, or reinterpret. |
| `goal_target_value` | Legacy duplication of a life-goal concept and the current Operations Center compatibility denominator | Preserve existing behavior; do not migrate, synchronize, or reinterpret. |
| `risk_personality` | Unresolved | Preserve without granting it risk or policy authority. |

The differing goal-type and priority vocabularies are not equivalent mappings.
No mapping such as `FINANCIAL_FREEDOM` to `FIRE` or `ESSENTIAL` to `HIGH` is
authorized.

### 4. Non-synchronization and disagreement

A Wealth Goal and a Legacy Portfolio Goal Profile may disagree. Phase 7.1
authorizes no synchronization, conflict resolution, precedence rewrite,
automatic migration, automatic Wealth Goal creation, linking, or historical
reinterpretation.

Wealth Goal is canonical for new Wealth Intelligence semantics. That
forward-looking authority does not rewrite the meaning or behavior of a legacy
profile value already stored or displayed. A consumer that must show both in a
future factual context may report the discrepancy with provenance; it must not
silently resolve it.

### 5. Funding designation is not mandate

`GoalFundingAllocation` means only:

> This amount from this Cash Account or Portfolio is designated toward this
> Wealth Goal.

It does not imply that:

- a goal owns a Portfolio or a Portfolio owns a goal;
- the source is segregated for the goal;
- the source has sufficient current or future capacity;
- the Portfolio is managed for the goal;
- the goal is advisory context for that Portfolio;
- the designation is a Portfolio Investment Mandate; or
- the goal is an optimizer objective or constraint.

Funding designation is many-to-many by current design: a Portfolio may fund no
goals, one goal, or several goals, and a goal may be funded by several
Portfolios and/or Cash Accounts. This factual cardinality establishes no
advisory or mandate cardinality. No zero/one/many advisory relationship is
approved in Phase 7.1.

### 6. Compatibility boundary

Phase 7.1 preserves without modification:

- all five Portfolio columns;
- `PATCH /portfolios/{id}/goal`;
- `GET` and `PUT /portfolios/{id}/goal-profile`;
- current Goal Discovery Wizard and Goal Profile display behavior;
- current legacy validation vocabularies; and
- current Operations Center behavior.

The Operations Center percentage is specifically a legacy portfolio-scoped
calculation using the latest portfolio snapshot value divided by
`goal_target_value`. It is not Wealth Goal progress, does not consume funding
allocations, and may disagree with the Goals experience. Preserving it during
Phase 7.1 does not make it canonical for new Wealth Intelligence semantics.

### 7. Decision Intelligence boundary

Neither Wealth Goal nor Legacy Portfolio Goal Profile authorizes any optimizer,
recommendation-ranking, constraint, glide-path, or Decision Policy change.
Funding allocations must not be used to infer an optimizer objective or
Portfolio mandate.

Before any future goal context enters Decision Intelligence, a separate
context-admission design must define at least:

- which canonical facts are admitted and for which Portfolio;
- advisory association and cardinality;
- conflict and cross-goal priority rules;
- authority, as-of time, completeness, and provenance;
- immutable capture or freeze of the exact goal context used by a recorded
  recommendation; and
- deterministic translation, if any, from context into an approved Decision
  Policy or recommendation constraint.

Until that design receives separate human approval, goal context may be used
only for separately authorized factual Wealth Intelligence reads, not judgment.

### 8. Phase 7 progression

Phase 7 proceeds in this order:

1. **7.1 Goal Domain Clarification** — this decision.
2. **7.2 Server-side Factual Goal Context Assembly.**
3. **7.3 Goal-aware Factual Wealth Review.**
4. **7.4 Decision Intelligence Context Admission.**
5. **7.5 Goal-aware Recommendation Constraints.**
6. **7.6 Cross-goal Objectives / Optimization.**

#### READY AFTER 7.1

The following are ready for design, not implementation by this ADR:

- factual server-side Goal Context;
- factual discrepancy and context reporting; and
- factual Wealth Review.

#### STILL BLOCKED

The following remain blocked:

- goal-aware recommendation constraints;
- advisory Portfolio-to-Wealth-Goal association and cardinality;
- cross-goal priority and conflict resolution;
- goal-type-specific policy effects;
- target-date policy effects and glide paths;
- cross-goal optimization;
- probability-of-success, success, or “on track” semantics; and
- automatic synchronization, migration, linking, or deprecation.

## Rationale

- A single word carrying two owners is the failure this platform's canonical
  vocabulary exists to prevent. Naming one canonical life-goal concept costs
  nothing today and removes the ambiguity before any consumer depends on it.
- Canonical authority is scoped forward deliberately. Declaring Wealth Goal
  canonical for *new* semantics settles the collision without retroactively
  restating what a stored legacy value has always meant to its existing users.
- The legacy contract is mixed, not merely misnamed: four fields duplicate
  life-goal concepts while `risk_personality` belongs to an unresolved
  question. A wholesale rename would therefore have to decide that question
  silently, so the contract is frozen instead of renamed.
- Funding designation is factually many-to-many. Inferring an advisory or
  mandate relationship from it would manufacture cardinality the data does not
  carry, so the factual and advisory questions are separated explicitly.
- A future mandate concept is described as a composition of references so it
  cannot accumulate authority its constituent owners never ceded — the same
  reasoning that keeps Persona a preset rather than a domain.
- Blocking optimizer admission rather than deciding it preserves the
  judgment/arithmetic boundary. Goal context that has no defined authority,
  as-of time, completeness, or provenance cannot safely enter a graded
  recommendation record, and that design deserves its own human decision.

## Open Human Decisions

Phase 7.1 deliberately does not resolve:

1. the final semantics and owner of `risk_personality`, including its
   relationship to `strategy_persona`, risk tolerance, risk capacity, and
   Decision Policy;
2. what “this Portfolio is managed for this Wealth Goal” means;
3. whether a Portfolio may have zero, one, or many advisory-relevant Wealth
   Goals;
4. cross-goal priority, conflict, and trade-off rules;
5. any goal-type-specific policy effects;
6. any target-date-specific policy effects;
7. the immutable goal-context capture required for recommendations; and
8. compatibility deprecation, migration, and historical-data policy.

These questions are not prerequisites for stating Phase 7.1 or designing
factual Phase 7.2–7.3 reads. They are prerequisites where identified above for
advisory or optimizer behavior.

## Historical and Conflicting Documentation

The [Portfolio Domain Model](../architecture/PORTFOLIO_DOMAIN_MODEL.md) contains
historical statements that describe a Portfolio as having “one goal,” call the
older goal profile Portfolio strategy metadata that shapes recommendations,
and anticipate target-date glide-path policy. Source comments also call the
legacy fields “recommendation-input fields.” Those statements are evidence of
the earlier product direction, not authority to treat the current mixed
contract as a canonical goal or a current optimizer input.

Under the Platform Architecture hierarchy, this level-3 ADR binds the point
ruling over the older level-4 design statements. They remain unchanged as
historical/conflicting evidence; they must not be silently used to override
this decision. The Roadmap's statement that goal-aware advice belongs to Phase
7 remains future direction and does not authorize stages 7.4–7.6.

## Consequences

- New Wealth Intelligence work has one canonical life-goal source.
- Existing Portfolio Goal Profile users retain storage, API, and presentation
  compatibility without a forced migration.
- Contradictions can be reported factually later without inventing a resolver.
- Portfolio funding designations remain useful without becoming hidden advice.
- Portfolio Investment Mandate remains available as a future product concept
  while its internal authorities stay separated.
- Phase 7.2 and 7.3 may be designed after independent review of this record.
- Phase 7.4 and later receive no authority from this ADR.

## Alternatives Considered

1. **Leave both goal concepts unchanged and ambiguous.** Rejected because one
   term would continue to carry two incompatible meanings and owners.
2. **Rename the current Portfolio Goal Profile wholesale to Portfolio
   Investment Mandate.** Rejected because four fields duplicate life-goal
   concepts and `risk_personality` is unresolved.
3. **Delete the Portfolio Goal Profile now.** Rejected because existing storage,
   APIs, UI, and Operations Center compatibility behavior remain active.
4. **Infer mandate from `GoalFundingAllocation`.** Rejected because designation
   is many-to-many factual metadata and conveys no advisory authority.
5. **Synchronize or migrate automatically.** Rejected because vocabularies,
   cardinality, conflicts, historical meaning, and risk semantics are not
   resolved.

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly addresses one
or more of the open human decisions and names this record. Runtime behavior,
new UI language, or persisted data drift cannot amend it by implication.

This ADR records no implementation authorization, no data migration, no Goal
Context contract, and no Phase 7.2–7.6 completion.
