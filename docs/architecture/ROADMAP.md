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
> monthly-expense ratio on Cash Flow. Emergency-fund target semantics are not
> defined.
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

# Phase 2 — Wealth Accounts

Expand beyond investment portfolios into first-class owned wealth accounts
without weakening Investment Core semantics.

## Cash Accounts v1

Cash Accounts v1 introduces standalone external Cash Accounts with a current
observed balance. They support an explicit currency, optional
institution/provider, and create, edit, archive, and manual balance-update
workflows.

- Dashboard aggregation will present **Total Assets**: current investment
  assets plus external Cash Account balances.
- Portfolio cash (brokerage cash) remains inside its investment Portfolio NAV;
  it must not be added again as a separate Cash Account balance.
- The existing historical chart remains **Investment Wealth History**. Cash
  Accounts v1 has no cash historical series yet.
- Asset Foundation is intentionally not the Cash Account ownership or balance
  model for this milestone.

`Total Assets` is not `Net Worth`: liabilities are not yet represented.

---

# Phase 3 — Personal Cash Flow

Future direction: income, expenses, transfers, recurring flows, and
cash-account ledger discipline.

---

# Phase 4 — Liabilities

Future direction: debts, loans, mortgages, other obligations, and payment
tracking.

---

# Phase 5 — True Net Worth & Wealth Intelligence

This is the first phase in which **Net Worth = Assets − Liabilities** becomes
semantically valid. Future direction includes a household wealth view,
historical net-worth evolution, emergency-fund intelligence, and cash-flow /
wealth insight.

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

Future direction includes natural-language wealth review, goal-aware
recommendations, risk-aware coaching, and scenario-aware advice. Learning and
evaluation remain constrained by the existing trust and configuration
boundaries; current AI investment evaluation is not yet a whole-life Wealth
Advisor.

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

- Complete and expose Decision → Transaction linkage where coverage remains
  incomplete
- System-deferral pricing

## Analytics

- Sector BHB attribution
- Cross-portfolio exposure and allocation analysis
- Total Assets History after external Cash Accounts have dated balance evidence

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
