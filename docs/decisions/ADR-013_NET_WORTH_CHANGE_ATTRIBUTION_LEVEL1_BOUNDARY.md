# ADR-013: Net Worth Change Attribution — Level-1 Balance-Sheet Boundary

**Status:** Accepted
**Date:** 2026-09-03
**Decision authority:** Human-approved Wealth OS bounded design and
implementation authorization decision
**Scope:** What a "why did Net Worth change" feature is permitted to claim
between two complete historical Net Worth points. Does not define any
economic-cause attribution (market return, contribution, income, spending,
debt repayment, borrowing).

---

## Context

Net Worth History already tells a user *that* their historical Net Worth
changed between two complete points (the existing "Change vs Previous
Point" card). It does not tell them *why*. The repository has real fragments
that look tempting to promote into a "why": `PortfolioSnapshot`'s
`net_external_cash_flow` / `investment_return_amount` fields, `CashAccount`
ledger event types (`INCOME`, `EXPENSE`, `ADJUSTMENT`, `TRANSFER`,
`INVESTMENT_TRANSFER`), and `LiabilityBalanceObservation`'s dated balances.
A bounded design/semantic-freeze inspection (2026-09-03) traced what each
fragment actually proves, concluded that a full economic-cause attribution
is not safely supported today, and selected a narrower, always-honest slice
for implementation. This ADR records that decision.

## Problem

Without a binding ruling, an implementation could plausibly: label a
Portfolio NAV residual as "market return" despite `net_external_cash_flow`
being windowed by `Transaction.created_at` rather than the attribution
period's exact dates; call a liability balance decline "debt repayment"
despite `LiabilityBalanceObservation` being an effective-state model with no
payment ledger; or automatically pair a cash-side `INVESTMENT_TRANSFER` with
a Portfolio `DEPOSIT`/`WITHDRAW` despite ADR-012 explicitly forbidding that
inference. Any of these would assert economic knowledge the platform does
not have, and once shipped as a labeled UI claim would be difficult to walk
back without eroding trust in every other number on the page.

## Decision

### 1. Level-1 only: balance-sheet component attribution

This feature explains Net Worth movement strictly at the balance-sheet
component level — the three components the existing Net Worth formula is
already built from:

```
investment_assets_change = investment_assets(end) - investment_assets(start)
external_cash_change     = external_cash(end) - external_cash(start)
liability_impact         = total_liabilities(start) - total_liabilities(end)
```

It never infers investment contribution, market return, income, spending,
debt repayment, borrowing, interest, or any cross-domain funding cause. That
class of claim is Level-2 economic attribution and is explicitly deferred
(see Reopen Conditions).

### 2. Reconciliation identity is mandatory, not decorative

For complete endpoint evidence, `N(d) = Investment(d) + Cash(d) - Liabilities(d)`,
so:

```
net_worth_change = [investment_assets(end) - investment_assets(start)]
                  + [external_cash(end) - external_cash(start)]
                  + [total_liabilities(start) - total_liabilities(end)]
```

`services/net_worth_change_attribution.py` computes `net_worth_change` and
the summed components as two separately-expressed quantities and requires
`abs(net_worth_change - sum(components)) <= 0.0001` (the stored snapshot
precision) before returning a numeric result. This is a boundary guard
against a future evidence-resolution bug, not proof that Level-1 attribution
can diverge under correct inputs — under the pure arithmetic in this module
it cannot, by construction.

### 3. Liability sign convention

A liability decline is a **positive** Net Worth impact:
`liability_impact = liabilities(start) - liabilities(end)`. The UI must
state the balance direction explicitly ("Liabilities decreased by ฿X" /
"increased by ฿X") and must never call a decline "debt repayment" — no
payment ledger exists to support that claim, only
`LiabilityBalanceObservation`'s effective-state balance history.

### 4. AVAILABLE / UNAVAILABLE, never a partial numeric row

The derived read returns exactly one of two statuses. `AVAILABLE` requires
complete evidence for all three components at both endpoint dates,
reusing the same historical authorities Net Worth History already reads
(`PortfolioSnapshot.total_value`, `cash_balance_as_of()`,
`liability_balance_as_of()`) and the same lifecycle completeness rule
(an entity not yet created by a date is not expected; zero expected cash
accounts or liabilities is a legitimate zero; zero expected portfolios is
never a legitimate zero — mirroring `frontend/lib/{wealthHistory,
totalAssetsHistory,totalLiabilitiesHistory}.ts` exactly). Anything less
returns `UNAVAILABLE` with bounded evidence-problem reason codes. Zero is
never substituted for unavailable evidence, and no `Other`/rounding bucket
absorbs a reconciliation gap.

### 5. ADR-012's funding non-matching boundary applies unchanged

This feature reads `CashAccountTransaction` balances (via
`cash_balance_as_of()`) exactly as they are — it never inspects
`transaction_type` or `counterparty_portfolio_id` to pair an
`INVESTMENT_TRANSFER` with a Portfolio `DEPOSIT`/`WITHDRAW`. A half-recorded
funding window (cash side recorded, Portfolio side not yet recorded, or vice
versa) reports exactly the recorded component movement — never "spending,"
"investment loss," "withdrawal," or "unmatched funding."

## Rationale

- The three components are exactly the terms the existing Net Worth formula
  already decomposes into — no new historical model, no new completeness
  rule, no new reconstruction logic. Section 5's evidence reuse keeps this
  feature a pure derived read rather than a second accounting system.
- A mandatory reconciliation guard converts "the three rows visually seem to
  add up" into an enforced invariant, matching this codebase's existing
  preference (ADR-002) for failing loud over silently absorbing drift.
- Deferring Level-2 avoids repeating the exact mistake ADR-012 already
  named and rejected for cash-side funding: manufacturing cross-domain
  economic authority the ledger does not grant, in a new surface where it
  would be easy to reintroduce independently.

## Consequences

- Users get a reconciled, trustworthy explanation of *what moved* on the
  balance sheet, immediately available for the same latest-two-complete-point
  window the existing Net Worth History journey already computes.
- Users do **not** get an explanation of *why* investment value moved
  (market return vs. contribution), *why* cash moved (spending vs. funding
  vs. adjustment), or *why* a liability moved (payment vs. re-draw) — those
  remain open, undecided questions this ADR takes no position on beyond
  naming them out of scope.
- No schema, persistence, or migration is introduced; the endpoint is a
  derived read only, computed fresh from the same authorities on every call.

## Alternatives Considered

1. **Full economic attribution (Level-2), using `net_external_cash_flow`,
   `investment_return_amount`, and cash event types as causes.** Rejected —
   `net_external_cash_flow` is windowed by `Transaction.created_at`, not
   arbitrary attribution dates, so it cannot honestly answer an
   arbitrary-date query; cash event types conflate genuine economic
   categories (income, spending) with non-economic ones (adjustment,
   internal transfer, investment funding) that this feature would have to
   correctly exclude to avoid the exact `EXPENSE`-path defect ADR-012
   already fixed once.
2. **A hybrid: Level-1 rows plus a best-effort Level-2 hint where evidence
   happens to be strong.** Rejected — a "sometimes-labeled" cause column
   invites users to trust the label even on the dates where the evidence is
   actually weak, and blurs the AVAILABLE/UNAVAILABLE boundary Section 4
   depends on.
3. **Compute attribution client-side, mirroring how Net Worth History itself
   is composed today (frontend pure functions over per-entity As-Of
   fetches).** Rejected for this feature specifically — reconciling three
   cross-domain sums with a mandatory tolerance guard is safer as one
   server-side derived read than as a fan-out of per-account/per-liability
   client requests recombined in the browser; it does not reopen or
   supersede the existing client-side Net Worth History composition, which
   is unchanged.

## Explicit Non-Goals

This decision does not define: investment contribution or market-return
decomposition; a cash-side income/spending/adjustment cause attribution;
debt repayment, borrowing, or interest attribution; any pairing or matching
between `INVESTMENT_TRANSFER` and Portfolio `DEPOSIT`/`WITHDRAW` (ADR-012
governs and is unchanged); a generic historical-period selector beyond
explicit `start`/`end` dates; or persistence of any attribution result.

## Relationship to Prior ADRs

- **ADR-002 (no compensation for ledger defects):** The reconciliation guard
  in Section 2 follows the same fail-loud posture — an inconsistent
  composition returns `UNAVAILABLE`, never a silently-adjusted number.
- **ADR-004 (one implementation per rule):** Investment, cash, and liability
  evidence are read through the existing single authoritative
  implementations (`PortfolioSnapshot.total_value`, `cash_balance_as_of()`,
  `liability_balance_as_of()`) rather than a second reconstruction.
- **ADR-012 (Investment Funding Transfer representation):** This decision
  inherits ADR-012's non-matching boundary unchanged — Section 5 restates it
  in this feature's specific context rather than reopening it.

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly addresses
one or more of the following and names this record: a Level-2
economic-cause attribution becomes authorized on stronger evidence (e.g. an
attribution-period-aligned return decomposition, a payment ledger for
liabilities, or an authorized cross-domain funding-matching subsystem); the
reconciliation tolerance or guard behavior changes; or the liability sign
convention changes. Runtime behavior, new UI language, or persisted data
drift cannot amend it by implication.
