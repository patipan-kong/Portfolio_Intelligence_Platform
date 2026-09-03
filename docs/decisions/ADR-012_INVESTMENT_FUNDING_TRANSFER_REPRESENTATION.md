# ADR-012: Investment Funding Transfer Representation

**Status:** Accepted
**Date:** 2026-09-03
**Decision authority:** Human-approved Wealth OS bounded design and
implementation authorization decision
**Scope:** The cash-side representation of "money moved between a Cash
Account and an investment Portfolio." Does not define paired, atomic, or
cross-domain funding.

---

## Context

Phase 3 shipped `INCOME`, `EXPENSE`, `ADJUSTMENT`, and paired `TRANSFER`
`CashAccountTransaction` types. The Phase 3 roadmap entry explicitly named
the gap: *"`TRANSFER` here means a cash-account-to-cash-account transfer, not
cash ↔ investment portfolio funding — that remains a deferred, separate
concept."* Before this decision, a user funding a Portfolio from a Cash
Account had exactly two ways to record it, both defective:

- **As an `EXPENSE`** — inflates `expenses`, `netCashFlow`, expense
  categories, the Cash Flow trend, `averageRecordedMonthlyExpense`, and
  therefore both Recorded Expense Coverage and its target/gap arithmetic
  (Phase 5). This is a live correctness defect, not a cosmetic one.
- **As a reconciliation `ADJUSTMENT`** — arithmetically clean, but the
  resulting row carries category `"Reconciliation"` and a generic note; it
  records that the balance changed, not why, and gives no durable
  association with the Portfolio the money went to.

A bounded design/semantic-freeze inspection (2026-09-03) traced this defect
against the repository's actual behavior, classified the existing
`TRANSFER`↔`CashAccountTransfer` pairing invariant, evaluated four
representation alternatives, and selected one for implementation. This ADR
records that decision.

## Problem

Without a binding ruling, an implementation could plausibly: overload the
existing `TRANSFER` type to mean two different things (a paired cash↔cash
leg and an unpaired cash↔Portfolio leg) distinguishable only by which
optional field is set; invent a second sign convention independent of
`services/cash_account_ledger.py`; let a Portfolio foreign key imply a
matching Portfolio-side transaction, amount, or date; or treat a
cash-recorded-only state as an error requiring a "missing deposit" warning
the system has no authority to assert. Any of these would either weaken an
existing invariant this repository already relies on, or manufacture
cross-domain authority the investment ledger does not grant.

## Decision

### 1. Canonical semantics

A new `CashAccountTransaction.transaction_type` value,
`INVESTMENT_TRANSFER`, means exactly:

> The user recorded that money moved between this Cash Account and a
> Portfolio. This is a Cash Account fact only.

It does **not** mean, and no code may treat it as meaning: a matching
Portfolio-side transaction exists; the Portfolio ledger has been updated;
amounts or dates match anything on the Portfolio side; the two sides are
atomically paired; or the movement has been reconciled.

### 2. `TRANSFER` is not overloaded

`TRANSFER` continues to mean exactly what it meant before this decision: one
leg of a paired cash↔cash `CashAccountTransfer`. `INVESTMENT_TRANSFER` is a
distinct type. A `ck_cash_account_transactions_transfer_leg_type` CHECK
constraint (`transfer_id IS NULL OR transaction_type = 'TRANSFER'`) makes it
impossible, at the schema level, for a row to be both a cash↔cash transfer
leg and an investment funding leg simultaneously.

### 3. Counterparty is metadata only

`counterparty_portfolio_id` (nullable, `ondelete="SET NULL"`) means only
that the user associates this cash movement with this Portfolio — the same
"factual, no behavioral or matching authority" shape ADR-010 already
established for Portfolio Investment Mandates. A
`ck_cash_account_transactions_counterparty_type` CHECK constraint
(`counterparty_portfolio_id IS NULL OR transaction_type = 'INVESTMENT_TRANSFER'`)
makes it impossible for any other transaction type — `EXPENSE`, `INCOME`,
`ADJUSTMENT`, or a cash↔cash `TRANSFER` — to carry a counterparty Portfolio.
No code may read this column to change, infer, validate, or reconcile
Portfolio state.

### 4. Sign convention

No second sign convention is introduced. `signed_amount()`
(`services/cash_account_ledger.py`) gains one branch: `INVESTMENT_TRANSFER`
returns the stored amount unchanged, exactly like `TRANSFER` and
`ADJUSTMENT` already do. `resulting_balance()` and `cash_balance_as_of()`
require no change — both delegate through `signed_amount()` (ADR-004: one
implementation per rule). The API accepts only a positive magnitude plus an
explicit `direction`; the server derives the stored sign
(`TO_PORTFOLIO` → negative, `FROM_PORTFOLIO` → positive).

### 5. Portfolio deletion

Portfolios are hard-deletable (`DELETE /portfolios/{id}` performs an actual
row delete, not an archive). `counterparty_portfolio_id` uses
`ondelete="SET NULL"` at the schema level — matching the existing
`Transaction.execution_decision_id` precedent for a metadata-only reference
to a deletable entity — plus an ORM-level `relationship()` from `Portfolio`
(deliberately without delete/delete-orphan cascade) so the association is
actually nulled out when a Portfolio is deleted. Both are required, not
redundant, for the same reason ADR-010 §4 already documented for
`goal_funding_allocations`: this repository's test suite builds schema via
`Base.metadata.create_all()` against SQLite, and SQLite does not enforce FK
`ondelete` actions without a PRAGMA this codebase does not set. The cash
fact — amount, sign, date, note, balance effect — survives Portfolio
deletion unchanged; only the counterparty attribution is lost, which is
truthful, since the referenced Portfolio genuinely no longer exists.

### 6. Aggregation exclusion

Investment funding is neither income nor expense. `INVESTMENT_TRANSFER` is
excluded from `income`, `expenses`, `netCashFlow`, both category maps,
`adjustments`, the Cash Flow trend, `averageRecordedMonthlyExpense`,
Recorded Expense Coverage, and the coverage target/gap — by construction,
not by a new rule: `frontend/lib/cashFlow.ts::aggregateMonthlyCashFlow` is a
whitelist over `INCOME`/`EXPENSE`/`ADJUSTMENT`, so an unrecognized type
contributes to none of those totals without any code change. This closes
the original `EXPENSE`-path correctness defect described in Context.

### 7. Half-recorded state is valid

A Cash Account funding record with no corresponding Portfolio-side
`DEPOSIT`/`WITHDRAW` is a normal, expected state — not an error. The system
has no authority to know whether, when, or how the Portfolio side will be
recorded, so no code may describe this state as "incomplete," "unmatched,"
"missing," or "pending." Portfolio state changes only through the existing
investment-ledger authority (`execute_deposit`/`execute_withdraw`); this
decision grants no new path to it and requires none.

### 8. No backfill

No `INVESTMENT_TRANSFER` row may be inferred from existing `EXPENSE`,
`INCOME`, or `ADJUSTMENT` rows that may have represented investment funding
in the past. Historical rows remain exactly as recorded; this decision
creates a new, empty capability going forward only.

## Rationale

- Reusing `TRANSFER` for both cash↔cash and cash↔Portfolio movements would
  make one type mean two different things, distinguishable only by which
  optional field happened to be set — the same anti-pattern ADR-010 rejected
  for reusing `GoalFundingAllocation` to mean a management relationship.
  `GET /cash-flow`'s existing paired-transfer branch
  (`transfer is None → continue`) would also need to grow a second,
  differently-shaped case to avoid silently dropping an unpaired leg —
  exactly the regression risk this decision avoids by not touching that
  branch at all.
- A distinct type is served by the *existing* main Cash Flow query (which
  excludes only `transaction_type != TRANSFER`) and is excluded from
  aggregation by the *existing* whitelist in `aggregateMonthlyCashFlow` —
  both with zero changes to either function. The required invariants
  (§6 above) hold by construction rather than by a new rule two engineers
  could implement inconsistently.
- The counterparty-as-metadata-only pattern is not new: it mirrors both
  `Transaction.execution_decision_id` (a metadata-only FK to a deletable
  entity) and ADR-010's Portfolio Investment Mandate (a factual,
  no-behavioral-authority association). Reusing an established pattern
  rather than inventing a new one keeps the platform's "factual vs.
  advisory" boundary consistent across domains.

## Consequences

- A user can record cash-side investment funding as a first-class, honest
  fact instead of an `EXPENSE` (which corrupts Recorded Expense Coverage) or
  an under-described reconciliation `ADJUSTMENT`.
- `Total Assets`/Net Worth may show a real, temporary dip or bump between
  recording the cash side and separately recording the Portfolio side — this
  is a pre-existing property of recording one domain before the other
  (identical under every representation available before this decision,
  including `EXPENSE` and `ADJUSTMENT`), not something this decision
  introduces or worsens.
- The Portfolio ledger, replay, snapshots, and metrics gain no new input and
  are structurally untouched: no code path from `INVESTMENT_TRANSFER`
  reaches `services/portfolio_transactions.py`,
  `services/portfolio_rebuilder.py`, or portfolio snapshot generation.
- Existing cash↔cash `CashAccountTransfer` behavior — pairing, signs, activity
  deduplication, income/expense exclusion, as-of reconstruction, the
  distinct-account constraint — is unweakened; the new
  `ck_cash_account_transactions_transfer_leg_type` constraint only tightens
  the existing model, and every row that existed before this decision
  already satisfies it.

## Alternatives Considered

1. **Reuse `TRANSFER` with a nullable `counterparty_portfolio_id`, leaving
   `transfer_id` null.** Rejected — overloads a type that means "one leg of
   a paired cash↔cash transfer" everywhere else in the codebase (payload
   fields, activity rendering, the dedicated `/cash-account-transfers`
   endpoint), and would force a second case into
   `GET /cash-flow`'s existing paired-transfer branch, the exact regression
   boundary this decision protects.
2. **Record as a reconciliation `ADJUSTMENT` with funding-reason metadata.**
   Rejected — abuses reconciliation semantics for a known, deliberate
   movement, and would enter the `adjustments` aggregate, which reconciling
   an *actually* unexplained balance difference should not be diluted by.
3. **A separate, cross-domain factual funding-event entity joining a Cash
   Account leg and a Portfolio leg.** Rejected as unnecessary for this
   decision's scope — the balance movement must be a `CashAccountTransaction`
   regardless, so a second entity would add a table, a join, and a new
   incentive toward cross-domain matching/reconciliation logic (which §7
   explicitly forbids) without buying anything this slice needs. Remains the
   correct shape if a future decision authorizes a paired, atomic funding
   subsystem — this decision does not foreclose that, and does not authorize
   it either.

## Explicit Non-Goals

This decision does not define: automatic creation of the Portfolio-side
`DEPOSIT`/`WITHDRAW`; any pairing, matching, atomicity, or cross-domain
completeness signal between a Cash Account funding record and a Portfolio
transaction; a funding-provenance report or contribution-tracking surface;
edit/delete/relink semantics beyond the existing append-only Cash Account
transaction lifecycle; or multi-currency support. These remain open,
independently decidable questions this ADR takes no position on.

## Relationship to Prior ADRs

- **ADR-004 (one implementation per rule):** `signed_amount()` gains one
  branch; `resulting_balance()` and `cash_balance_as_of()` are unmodified,
  preserving the single authoritative balance-movement rule.
- **ADR-010 (Portfolio Investment Mandate Foundation):** This decision reuses
  the same "user-authored, factual, no behavioral/matching authority"
  pattern ADR-010 established for Portfolio↔Goal association, applied here
  to a Cash Account transaction's Portfolio counterparty.

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly addresses
one or more of the following and names this record: a paired, atomic
cross-domain funding subsystem becomes authorized; `counterparty_portfolio_id`
gains behavioral, matching, or reconciliation authority; `INVESTMENT_TRANSFER`
must affect Cash Flow aggregation, Recorded Expense Coverage, or the
existing cash↔cash `TRANSFER` semantics; or historical `EXPENSE`/`ADJUSTMENT`
rows require backfill or reclassification into `INVESTMENT_TRANSFER`.
Runtime behavior, new UI language, or persisted data drift cannot amend it
by implication.
