# Wealth OS Product Roadmap

> Last Updated: 2026-08 (v3.0 — Wealth OS product rebaseline)
>
> Current Status:
>
> **Phases 1–4 (Investment Core, Wealth Accounts, Personal Cash Flow,
> Liabilities) are complete.**
>
> **Phase 5 — True Net Worth & Wealth Intelligence** core is complete: current
> and historical Net Worth (Assets − Liabilities) are in place, together with
> Recorded Expense Coverage — a factual tracked-cash to average-recorded-
> monthly-expense ratio on Cash Flow — and an optional, user-set Recorded
> Expense Coverage target. The target is a user-supplied preference compared
> deterministically against recorded expense evidence; it is not a
> system-recommended emergency-fund target, and no `EMERGENCY_FUND`-specific
> Goal semantics exist.
>
> **Phase 6 — Planning, Goals & Scenarios is complete** as a deterministic,
> factual planning foundation. See the Phase 6 section for the delivered chain
> and for the capabilities that remain future.
>
> This roadmap states the product capability sequence, active delivery
> direction, and parallel future tracks. Platform domains, boundaries, laws,
> and evolution principles are defined by
> [platform_architecture.md](platform_architecture.md) (the constitution).
> This document is subordinate to it under the constitution's governance
> hierarchy (§11) and uses its domain vocabulary
> ([GLOSSARY.md](../GLOSSARY.md)).

---

## Product Baseline — Investment Core ✅ COMPLETE

Investment Core is the completed product baseline for trustworthy investment
management and intelligence.

### Investment accounting

- Investment portfolios, holdings, and a transaction ledger
- Deterministic replay and accounting correctness, including brokerage cash
- Portfolio snapshots, performance history, and benchmark foundations

### Investment intelligence

- Performance and risk analytics
- Optimizer, recommendation, and execution-intelligence capabilities
- AI evaluation and trust capabilities within their existing boundaries

### Multi-portfolio product capability

- Combined Wealth Overview for current investment assets
- Cross-portfolio dividend income and Investment Wealth History
- Combined cash-flow-adjusted Investment Performance

### Data portability and history

- Transaction history
- CSV import and bounded CSV export

### Bounded corporate-action capability

`POSITION_CONVERSION` is supported through the current bounded
corporate-action path and is visible in transaction history. This does not
represent a generic, complete Corporate Actions engine.

---

# Phase 2 — Wealth Accounts ✅ COMPLETE

Expand beyond investment portfolios into first-class owned wealth accounts
without weakening Investment Core semantics.

## Cash Accounts v1

Cash Accounts v1 delivers standalone external Cash Accounts with an explicit
currency, optional institution/provider, and create, edit, archive/restore,
and manual balance-update workflows, plus a baseline/start balance, an
as-of balance reconstruction, and explicit reconciliation against an
observed balance.

- Dashboard aggregation presents **Total Assets**: current investment assets
  plus external Cash Account balances.
- Portfolio cash (brokerage cash) remains inside its investment Portfolio NAV;
  it is not added again as a separate Cash Account balance.
- **Total Assets History** is now delivered (see Phase 5 / Open Engineering
  Backlog): Investment Wealth History combined with Cash Account as-of
  evidence.
- Cash-account-to-cash-account transfers are supported (paired, excluded from
  income/expense/net-flow aggregation) — see Phase 3. This is distinct from
  cash ↔ investment portfolio funding, which remains a deferred, separate
  concept.
- Asset Foundation is intentionally not the Cash Account ownership or balance
  model for this milestone.

`Total Assets` is not `Net Worth`: see Phase 5 for where liabilities enter.

---

# Phase 3 — Personal Cash Flow ✅ COMPLETE

A prospective cash ledger on top of Cash Accounts: `INCOME`, `EXPENSE`, and
`ADJUSTMENT` entries, plus paired `TRANSFER` legs between two Cash Accounts
(excluded from income/expense/net-flow aggregation — a transfer moves money,
it does not earn or spend it). Delivered:

- Month navigation with monthly income/expense/net-flow totals
- Activity/history and category breakdown, with trend visualization
- Reconciliation integration (Phase 2) surfaced in cash-flow activity
- No fabricated pre-baseline history — a Cash Account's ledger starts at its
  baseline, not before
- **Recorded Expense Coverage** — a factual tracked-cash to
  average-recorded-monthly-expense ratio, plus an optional, user-set
  **Recorded Expense Coverage target** (in months) on `/cash-flow`. The
  system performs deterministic target/gap arithmetic against recorded
  expense evidence; it does not recommend, default, or infer the number of
  months. See Phase 5 for how this relates to emergency-fund semantics.

`TRANSFER` here means a cash-account-to-cash-account transfer, not cash ↔
investment portfolio funding.

- **Investment Funding Transfer** (ADR-012) — a Cash Account movement to or
  from an investment Portfolio can be recorded as a distinct, one-sided
  factual event (`INVESTMENT_TRANSFER`). It moves the Cash Account balance
  and names the associated Portfolio as user-asserted metadata; it does not
  count as income, expense, or net cash flow, and does not affect Recorded
  Expense Coverage.

**Paired, atomic cross-domain funding remains deferred.** Recording the cash
side does not create, match, validate, or reconcile the Portfolio's ledger
transaction: no automatic `DEPOSIT`/`WITHDRAW` creation, no cross-domain
atomicity, no matching or completeness signal between the two sides. The
Portfolio-side entry remains a separate, user-initiated act through the
investment ledger (Phase 1).

- **Cash Entry Templates** — user-authored `INCOME`/`EXPENSE` templates
  (name, Cash Account, amount, category, optional note) that prefill the
  existing Add income / Add expense form on `/cash-flow`. A template is
  workspace-owned convenience metadata, not a financial fact: creating,
  editing, deleting, or invoking one never touches `CashAccountTransaction`
  or a Cash Account balance — only the user's explicit submission of the
  (editable) prefilled form does, through the same ledger endpoint as any
  other entry. No date is stored on a template (invocation uses the form's
  own fresh date default); there is no scheduled transaction, recurrence
  rule, or automatic posting. A template referencing an archived Cash
  Account remains stored and editable but cannot be invoked until the
  account is restored or the template is repointed to another active
  account.

---

# Phase 4 — Liabilities ✅ COMPLETE

First-class owned Liability records, symmetric to Cash Accounts (Phase 2), so
Net Worth (Phase 5) can subtract real debt instead of treating it as
unmodeled. Delivered:

- Liability records with a type (`MORTGAGE`, `AUTO_LOAN`, `PERSONAL_LOAN`,
  `CREDIT_CARD`, `STUDENT_LOAN`, `OTHER`), optional lender, and a current
  outstanding THB balance
- Create, edit, and archive/restore lifecycle — no delete, matching the
  WealthGoal/CashAccount precedent (an archived Liability keeps its history
  but stops receiving new activity)
- Dated balance observations recording an explicit, effective-state
  outstanding balance as of a date, plus as-of balance reconstruction for
  historical evidence (available even for an archived Liability)
- Dashboard aggregation presents **Total Liabilities** — see Phase 5 for Net
  Worth, which combines this with Total Assets — and **Total Liabilities
  History** alongside Total Assets History
- Liability observation history and historical as-of lookup are visible in
  the Liabilities UI (per-liability balance history list and a date lookup),
  reading the existing observation/as-of endpoints — no new persistence

This is a balance-tracking record, not a loan-servicing system: there is no
amortization schedule, interest forecasting, or automatic link between Cash
Flow (Phase 3) payments and a Liability's balance — a balance only ever
changes through an explicit observation or edit.

---

# Phase 5 — True Net Worth & Wealth Intelligence ✅ CORE COMPLETE

This is the first phase in which **Net Worth = Assets − Liabilities** becomes
semantically valid. Delivered: current and historical Net Worth, Total Assets
History (Investment Wealth History combined with Cash Account as-of
evidence), Recorded Expense Coverage, and an optional user-set Recorded
Expense Coverage target with deterministic target/gap arithmetic (Phase 3).

Future direction: a household wealth view and system-recommended or
AI-assisted emergency-fund guidance. The Recorded Expense Coverage target
remains a user-supplied preference compared against recorded expense
evidence, not a system recommendation, and introduces no `EMERGENCY_FUND`-
specific Goal math (see Phase 6).

**Net Worth Change Attribution — Level-1 (ADR-013)** — a compact "Why Net
Worth changed" card beneath Net Worth History, for the latest two complete
Net Worth History points. `GET /net-worth/change-attribution?start&end`
decomposes the Net Worth delta into exactly three reconciled components —
investment assets change, external cash change, and liability impact (a
liability decline is a positive impact) — reusing the same
`PortfolioSnapshot.total_value` / `cash_balance_as_of()` /
`liability_balance_as_of()` authorities Net Worth History already reads, and
returns `AVAILABLE` or `UNAVAILABLE` (never a partial or zero-substituted
row). **Level-2 economic-cause attribution remains explicitly deferred** —
this card does not, and cannot yet, explain market return vs. contribution,
income vs. spending, or debt repayment vs. re-draw; see ADR-013 for the full
boundary and why each of those requires stronger evidence than the ledger
currently provides.

---

# Phase 6 — Planning, Goals & Scenarios

**Complete** as a deterministic, factual planning foundation. Delivered:

- Wealth Goals Foundation — workspace-owned goals with type, THB target,
  optional target date, priority, and archive lifecycle
- Goal Funding Allocations — explicit designations from a Cash Account or a
  Portfolio toward a goal
- Goal Progress & Funding Health — per-goal designated funding and gap, plus a
  source-centric comparison against a source's current value
- Deterministic What-If — projection under explicit user contribution and
  return assumptions
- Required Monthly Contribution — the inverse calculation against a saved
  target date
- Goal Detail / Planning UX — summary, funding sources, planning, and scenarios
- Goal Funding-Source Drill-Through — Goal Detail's Funding Sources list links
  each designation to its exact existing Cash Account or Portfolio source
  (`/cash?account=<id>` / `/portfolio?portfolio=<id>`) for factual inspection.
  Navigation only: no new backend endpoint, no scheduled or automatic action,
  and an unresolvable source is never silently replaced by another one.
- Named Scenarios — persisted, archivable per-goal assumption sets
- Scenario Comparison — two scenarios evaluated against one shared live goal
  context, with no ranking and no winner
- Workspace Goals view — per-goal funding summaries plus a cross-goal Funding
  source health view on `/goals`

Every result above is deterministic and factual. Planning math is
goal-type-agnostic: `RETIREMENT`, `FIRE`, `EMERGENCY_FUND` and the other types
are classification labels, not dedicated planning engines. A saved scenario
persists assumptions only; it is not a commitment and no contribution is
tracked against it.

Future direction, not delivered: goal-type-specific planning depth (retirement,
FIRE / financial independence, major purchases); recurring or committed
contributions and contribution tracking; probabilistic or Monte Carlo
simulation; cross-goal prioritization and conflict resolution; allocation
optimization; and advisory behavior. Goal-aware advice belongs to Phase 7.

---

# Phase 7 — AI Wealth Advisor

**Active / in progress.** Phase 7 has delivered a factual, deterministic
foundation; its Wealth Advisor direction remains future work.

Delivered foundation:

- **7.1 Goal Domain Clarification** — Wealth Goal is the canonical authority;
  the Legacy Portfolio Goal Profile is a frozen compatibility contract; Goal
  Funding Allocation is factual designation only; Portfolio Investment Mandate
  (delivered under 7.6A / ADR-010) remains a distinct concept from
  designation; and the Decision Intelligence admission
  boundary is established. `risk_personality` remains unresolved.
- **7.2 Canonical Goal Context** — `wealth.goal-context.v1`
  (`GET /wealth-goals/context`) provides valuation-free canonical Wealth Goal
  facts, funding allocations, designation totals, progress/gap, fully-
  designated state, source aggregation, and integrity/completeness semantics.
- **7.3A Factual Wealth Review** — `wealth.factual-review.v1`
  (`GET /wealth-goals/factual-review`) provides DB-only factual valuation
  composition from Cash Account balances and persisted PortfolioSnapshot
  evidence, with explicit as-of/source-quality semantics, designation coverage,
  and funding-support composition. The Workspace Goals view surfaces its
  server-owned valuation-completeness state alongside source health. It performs
  no provider fetches or advisory inference.
- **7.3B Legacy Goal Profile Evidence** —
  `wealth.legacy-profile-evidence.v1`
  (`GET /wealth-goals/legacy-profile-evidence`) provides allocation-edge
  coexistence evidence, raw Legacy Portfolio Goal Profile facts, existing
  compatibility projections, authorized literal code/date comparisons, and
  side-by-side priority/target-value evidence. It creates no canonical-to-
  legacy mapping, precedence, synchronization, goal identity inference, or
  advisory authority; `risk_personality` is excluded from this contract. Goal
  Detail is its current consumer.

- **7.4 Decision Intelligence Context Admission** (ADR-008) —
  `wealth.decision-goal-context.v1` admits Wealth Goal IDs the caller
  explicitly names on an optimizer request and captures their factual state on
  the resulting `RecommendationSnapshot` only, constructed strictly after the
  recommendation already exists. Capture is permanently `decision_effect:
  CONTEXT_ONLY` — it never reaches L1/L2/L3, policy, constraints, scoring, or
  consensus, and `OptimizerHistory` remains unchanged and unconditional.
- **7.5 Goal-aware Recommendation Constraints** (ADR-009) — an independent,
  optional `goal_constraint_goal_id` activates exactly one non-archived Wealth
  Goal with a target date. A horizon of 0–365 days contributes a 20% maximum
  single-position bound that may only tighten, never loosen, the existing
  constraint envelope; the resulting application status is persisted as
  canonical evidence on `OptimizerHistory.result_json`. This does not extend
  or reinterpret Phase 7.4 context selection.
- **7.6A Portfolio Investment Mandate Foundation** (ADR-010) — a canonical,
  user-authored factual Portfolio ↔ Goal relationship records what Goal or
  Goals a Portfolio is managed for. It has no behavioral authority, optimizer
  objective, Goal priority, conflict/tie/gap resolution, or inference from
  Goal designation, funding, allocation, or coverage. Goal designation ≠
  Portfolio Investment Mandate.
- **7.6B Goal Objective Authority Foundation** (ADR-011) — freezes the
  authority vocabulary governing all Goal-fact behavioral questions
  (canonical Goal fact / fact authority / admission / behavioral authority /
  optimizer consumption) and the default rule that a canonical Wealth Goal
  fact carries no behavioral authority merely from existing, being
  persisted, being derived, being selected on a request, or belonging to a
  mandated Goal. ADR-009 remains the sole currently-authorized Goal-derived
  behavioral exception. This introduces no persistence, schema, migration,
  API, UI, or optimizer change, and no Goal-objective entity or categorical
  objective vocabulary.

Still open: **7.6C–7.6D Cross-Goal Objectives / Optimization** remain
future:

  - **7.6C Cross-Goal Conflict Policy** — priority, insufficient-capital,
    shared-portfolio, tie, and gap semantics. Not automatically next after
    7.6B; architecture planning should be revisited only when a genuine
    multi-Goal behavioral conflict surface exists.
  - **7.6D Cross-Goal Optimization Integration** — integrating the
    already-defined mandate/authority/conflict model into optimizer behavior.

Future direction continues to include natural-language whole-life wealth
review, goal-aware recommendations beyond the narrow Phase 7.5 single-position
bound, risk-aware coaching, and scenario-aware advice. These capabilities,
canonical-to-legacy synchronization or automatic goal mapping, multi-goal or
cross-Goal Decision Intelligence policy,
general recommendation/advisory authority, canonical `risk_personality`
interpretation, and cross-goal optimizer admission are not yet delivered.
Learning and evaluation remain constrained by the existing trust and
configuration boundaries; current AI investment evaluation is not yet a
whole-life Wealth Advisor.

---

## Multi-Asset Investment Evolution

Investment instrument expansion is a parallel track that can proceed
independently when prioritized. Candidate classes include ETFs, Mutual Funds,
Gold, Crypto, and Property or other valued assets where the architecture
supports them.

Asset-definition groundwork alone does not indicate complete user-facing
support for a class. In particular, Mutual Funds are a separate multi-asset
investment milestone, not part of Phase 2 Wealth Accounts.

## Asset Foundation Status

**Asset Foundation is partially integrated platform infrastructure.** Canonical
asset identity and asset definitions exist; nullable ledger identity links are
live; selected read/write and guarded replay paths use registry identity.
Registry-native adoption remains staged, and public asset search remains
feature-flagged. Cash Accounts v1 intentionally does not use Asset Foundation
as its ownership or balance model.

---

## Parallel Platform Evolution

These platform capabilities can continue without redefining the active Wealth
OS product phase:

- Registry-native adoption
- Broader corporate-action support
- Market-provider maturity and market calendar capabilities
- Historical services
- Advanced analytics and attribution

## Parallel SaaS / Commercialization Track

SaaS operational widening is a future parallel track, not a mandatory
predecessor to Personal Wealth development. Potential capabilities include
multi-workspace support, team accounts, RBAC, usage reporting,
credits/billing, API keys, and audit logs. These are not represented as
complete product capabilities today.

---

# Open Engineering Backlog

These important engineering improvements remain outside product phase gates.
The roadmap tracks product capabilities; perpetual engineering quality work is
tracked here ([ENGINEERING_PRINCIPLES.md](../engineering/ENGINEERING_PRINCIPLES.md),
"Capability vs. Quality").

## Accounting

- STATIC_FROZEN fallback correction

## Portfolio

- ~~Complete and expose Decision → Transaction linkage where coverage remains
  incomplete~~ — delivered: `execution_decision_id` is now writable end to
  end (APPROVED/PARTIAL_EXECUTION/MANUAL_OVERRIDE, BUY/SELL only) via a
  "Record execution →" deep link from the optimizer decision panel and S4b
  into `/portfolio?decision=<id>`, with backend workspace/portfolio
  ownership validation on write. Forward-only in v1 — no retroactive
  linking and no unlink/relink, since the ledger has no transaction-edit
  path; historical decisions and imported transactions stay unlinked by
  design, not backfilled.
- System-deferral pricing

## Analytics

- Sector BHB attribution
- Cross-portfolio exposure and allocation analysis
- ~~Total Assets History after external Cash Accounts have dated balance
  evidence~~ — delivered: `TotalAssetsHistoryCard` combines Investment Wealth
  History with Cash Account as-of evidence on the dashboard.

## Architecture

- Domain Modularization
- Event Bus
- Shared Analytics Library
- AI Routing Layer
- Prompt Layer Cleanup
- Internal API Simplification
- Cache Improvements

## Platform

- Accessibility (WCAG)
- UI consistency
- Performance optimization

---

## Historical Architecture Evolution Baseline

The prior v2.0 roadmap recorded the 2026-07 architecture-era evolution:

Portfolio Platform → Investment Intelligence → Multi-Asset Platform groundwork
→ SaaS operational widening → Personal Wealth Platform → AI Wealth Advisor.

It remains useful historical architectural context, but it is no longer the
active product-delivery phase numbering. The product roadmap above preserves
that intent while sequencing the Wealth OS capabilities from the completed
Investment Core.

# Governance

This roadmap is an implementation-level product artifact under the
constitution's governance hierarchy
([platform_architecture.md](platform_architecture.md) §11). The constitution
owns the platform's domains, boundaries, laws, and architectural evolution
principles; this roadmap expresses product capability sequence, active
delivery direction, and parallel tracks. Where they appear to disagree, the
constitution states the intent and this document states the delivery plan.
