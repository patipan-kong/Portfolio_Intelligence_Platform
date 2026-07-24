# M42 — Work Package Roadmap Reconciliation (Post-WP1)

**Date:** 2026-07-24

**Document class:** Milestone-planning reconciliation note (non-normative,
non-constitutional)

**Depends on:** [M42-WP1 Candidate Vocabulary and Ownership
Register](M42_WP1_PORTFOLIO_CANONICAL_VOCABULARY_AND_OWNERSHIP_REGISTER.md),
status `READY_FOR_INDEPENDENT_CONFIRMATION`

**Effective when:** WP1 reaches Independent Confirmation. Until then, this
note describes what the confirmed roadmap **will** read, not what it reads
today. Nothing here is authorized for reliance ahead of that confirmation.

**Amends:** Nothing. This note **does not modify**
[M42_ARCHITECTURE_PROPOSAL.md](M42_ARCHITECTURE_PROPOSAL.md), which remains
frozen and unedited. Every change recorded below is an exercise of a branch
the frozen proposal already wrote into itself, not an amendment of it — see
§4.

---

## 1. Purpose

WP1 reached two dispositions with direct consequences for the seven-WP
decomposition the M42 Architecture Proposal laid out at its §6 and §7:
`REJECT` for Portfolio Policy and `ADMIT` (Ledger & Accounting) for Portfolio
Base Currency. This note reconciles milestone planning against those outcomes —
which work packages proceed, which do not, and what the dependency graph and
roadmap steps should say once WP1 is confirmed. It makes no architectural
decision WP1 did not already make, and it reopens no frozen text.

## 2. What Changes

### 2.1 M42-WP4 — cancelled

**Proposal, as written (§6 table):** *"M42-WP4 — Portfolio Policy Declaration
Contract *(blocked)* — Component D — unproven, WP1 must prove — Portfolio
Policy (admission-blocked until owner proven — RC-4)."*

**WP1 finding (register §6.2):** `REJECT`. Portfolio Policy is not a single,
distinctly ownable noun — its constraint-shaped fields (allowed markets/
classes/currencies, leverage, cash requirement) are already Decision Policy /
Portfolio Limits (Decision Intelligence, `M34-D-0007`); its settlement field
is already Accounting Scope (Ledger & Accounting, `M34-D-0002`); its two
remaining descriptive fields (fractional permission, tax/wrapper context) are
at most unnamed fields of the already-admitted Portfolio Strategy Metadata.

**Reconciliation:** M42-WP4 **does not proceed**, on WP1 confirmation, per the
Architecture Proposal's own already-written branch (§11 step 4: *"If WP1
proves the concept is not distinctly ownable by Portfolio Intelligence, this
WP does not proceed"*). The seven-WP decomposition becomes a **six-WP
decomposition** for execution purposes: WP1, WP2, WP3, WP5 (reduced, §2.2),
WP6, WP7. WP4's row in the §6 table is struck from the active work plan, not
rewritten — its text remains accurate as a record of what was proposed and
why it was withheld.

**Consequence, restated from the register:** the two surviving descriptive
fields (fractional-trading portfolio-side permission, tax/wrapper context) are
not carried anywhere by this cancellation. If a future milestone wants to name
them, that is a new, separately chartered admission against Portfolio Strategy
Metadata's already-frozen allocation — never a revival of M42-WP4 under a
different number.

### 2.2 M42-WP5 — scope reduced to Benchmark only

**Proposal, as written (§6 table):** *"M42-WP5 — Benchmark & Base-Currency
Contract — Component E — Portfolio Intelligence (Benchmark); Base Currency
owner unproven — Benchmark; Portfolio Base Currency (base-currency
admission-blocked — RC-4)."*

**WP1 finding (register §6.4, corrected):** `ADMIT` — owner Ledger &
Accounting. Portfolio Base Currency is not a Portfolio Intelligence
coordinate. It is admitted as a **new, named coordinate** on the register's
own five-part-gate proof — not asserted to have been already silently
present, unnamed, inside `M34-D-0002`'s frozen text. The Portfolio Domain
Model's own §3 placement of Base Currency under "Portfolio Identity," not
under Universe, Policy, or Benchmark, was the starting hypothesis this
admission independently tested and confirmed, rather than a claim treated as
self-proving.

**Reconciliation:** M42-WP5, on WP1 confirmation, retitles to **"Portfolio
Benchmark Declaration Contract"** (Component E, Benchmark declaration leg
only) and proceeds with Portfolio Intelligence as sole owner. The
Base-Currency leg does **not** proceed as a Portfolio-Intelligence admission
under Component E — again exercising a branch the proposal already wrote
(§11 step 4: *"the Base-Currency leg of WP5 does not begin until WP1 has
proven their owner; if unproven they are withheld"*), except that the owner
question is now resolved (Ledger & Accounting), not left open. Component E's
text in §5 of the proposal remains accurate as written (it already frames
Base Currency's ownership as contingent); only the execution plan narrows.

**Consequence, restated from the register:** carrying the Base Currency
coordinate is now **confirmed, owned work for M42-WP2** (Component B,
"Portfolio Identity, Accounting Scope & Membership Contract," owned by Ledger
& Accounting), not an optional citation. WP2's contract text must supply the
coordinate's exact currency-reference format and its event-sourced-change
invariant as part of its own future contract-review obligation; WP2 carries
this as a confirmed `ADMIT` from WP1, not as a reuse-only field it may
choose whether to name.

### 2.3 Dependency graph (§7 of the proposal)

The proposal's ASCII dependency graph shows WP4 as one of three parallel
branches beside WP3 and WP5 under WP2, feeding into WP7. On WP1 confirmation:

- the WP4 branch is removed from the *active* graph (it remains correct as a
  historical record of what the frozen proposal proposed);
- the WP5 branch is read as "Benchmark" only, not "Benchmark · Base Ccy"; and
- WP7 is unaffected in shape — it was already specified to compose "only
  confirmed WP2–WP6 coordinates" (proposal §7), which structurally already
  excludes an unconfirmed or cancelled WP4 and an unconfirmed Base-Currency
  leg without any wording change.

No other edge changes. WP2 still precedes WP3/WP5/WP6; WP3, WP5, WP6 remain
mutually independent and parallelizable; WP7 remains terminal.

### 2.4 Roadmap steps (§11 of the proposal)

Step 4 of the recommended roadmap (*"M42-WP3, WP4, WP5, WP6... proceed only
for candidates WP1 confirmed"*) already states the precondition that produces
this exact outcome; its recommended sequencing sentence ("then WP5
(Benchmark) and, if unblocked, WP4...") resolves, on confirmation, to: run
WP3 and WP6 first, then WP5 (Benchmark only) — WP4 is not scheduled at all,
not merely deprioritized.

## 3. What Does Not Change

- No frozen coordinate is reopened: Decision Policy, Portfolio Limits, Sector
  Limits, Portfolio Identity, and Accounting Scope retain their `M34-D-0002`/
  `M34-D-0007` text exactly as today.
- Component B (WP2), Component C (WP3), Component F (WP6), and Component G
  (WP7)'s purposes and owners are unchanged.
- The M42 Architecture Proposal document itself is not edited. It is cited,
  not amended — Section 0's non-reopening rule applies to this note with the
  same force it applies to any other artifact.
- Epic Closeout's own reconciliation obligations (proposal §11 step 6) are
  unchanged by this note; this note is a milestone-planning aid, not a
  substitute for Closeout's whole-corpus verification.

## 4. Why No Architecture Amendment Is Required

Platform Architecture §10 requires an amendment only when a document's Laws,
Relationships, or (for a domain constitution) governed boundary actually
changes meaning. The M42 Architecture Proposal's §6 and §11 already wrote the
conditional branches this reconciliation exercises — "if WP1 proves the
concept is not distinctly ownable, this WP does not proceed" and "if unproven
they are withheld." WP1 did not change what those sentences mean; it supplied
the proof they were always waiting on. Recording the resulting six-WP
execution plan is therefore ordinary milestone-planning bookkeeping (Platform
Architecture §11, G3 — "deciding something the constitution never addressed
is normal work... recorded at its proper level"), not a Level-1 amendment.

## 5. Status

This reconciliation is **provisional on WP1's own Independent Confirmation**.
If WP1's Independent Review returns required corrections that change the
Portfolio Policy or Portfolio Base Currency disposition, this note is
superseded without needing its own correction cycle — it simply no longer
describes the confirmed outcome, and a revised version (or a fresh one) is
produced once WP1 is actually confirmed.

**`PROVISIONAL — PENDING WP1 INDEPENDENT CONFIRMATION`**
