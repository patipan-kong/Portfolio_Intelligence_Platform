# M44-WP3 — Period-Return Ownership Governance Correction

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics Foundation

**Work package:** M44-WP3 only

**Artifact class:** Documentary constitutional correction

**Status:** `RC2 — REQUIRES RENEWED INDEPENDENT CONSTITUTIONAL REVIEW AND CONFIRMATION`

**Record date:** 2026-07-29

**Gate owned:** `G-2` — sole. No other gate is touched.

**Governing frozen authority:** [M44 Architecture and Implementation Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
(RC2), `COMPLETE AND FROZEN` per
[M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md) §9;
[M44-WP1 Inherited Gate Inventory and Closure Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md),
`COMPLETE AND FROZEN` and `EFFECTIVE` per
[M44-WP1 Freeze Record](M44_WP1_FREEZE_RECORD.md) §§5 and 12; and confirmed,
frozen [M44-WP2](M44_WP2_M43_ARCHITECTURE_CONFIRMATION_RECORD.md), including
its [formal constitutional response](M44_WP2_FORMAL_CONSTITUTIONAL_RESPONSE.md)
and [freeze record](M44_WP2_FREEZE_RECORD.md), whose
[closeout](M44_WP2_CLOSEOUT.md) §9 releases M44-WP3 to begin.

**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/schema/migration authority:** `NONE`
**API/transport authority:** `NONE`
**UI/presentation authority:** `NONE`
**Implementation authority:** `NONE`
**Provider authority:** `NONE`
**Scheduler/cache/observability authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`
**Capability-completion authority:** `NONE`
**Frozen-artifact-amendment authority:** `NONE`
**Step-4-vehicle authority:** `NONE`
**Gate-disposition authority:** `G-2` only, and effective only after the
independent confirmation required by frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§11
M44-WP3, 12.4, and 16.2. `NONE` for `G-1`, `G-3`, `G-4`, and `G-5`.

---

## 0. Executive determination

This record performs, subject to independent confirmation, step 3 of the
documentary correction path in frozen
[M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
§7.4. Upon successful independent confirmation, it constitutionally
supersedes the single named M43 Architecture §8 ownership row without editing
that frozen artifact and restates the already confirmed two-part allocation in
M43-WP1 §7.3
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§8.2 and 11
M44-WP3).

The RC2 determination for `G-2` is:

`RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`

That is a non-closure state. It becomes effective only after this artifact
receives independent constitutional confirmation with unresolved findings
`NONE`. Until then, `G-2` remains `NOT YET DISPOSITIONED`, the frozen steps 1–3
release condition remains undischarged, and the standing M43-WP6 block remains
in force ([M44-WP1 Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
§§4.2, 7, and 8.1; [M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§§11 M44-WP3 and 12.4).

Successful confirmation makes this record the step 3 correction, discharges
the steps 1–3 release condition, and dispositions the standing M43-WP6 block.
The separate step 4 recording obligation remains outstanding, its named
vehicle has lapsed, and this work package neither supplies nor authorizes a
substitute ([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§§3.1 `G-2`, 8.2, 12.6, and 17 OQ-5).

---

## 1. Document status and authority

This is the sole normative deliverable allocated to M44-WP3 by frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §11
M44-WP3. It is an RC2 governance record awaiting the renewed independent
review and confirmation sequence fixed by §§12.4 and 16.4–16.5 of that plan.
Following the `NOT APPROVED` RC1 review, this corrected RC2 awaits renewed
independent review before it may proceed to confirmation.

This RC2 is not self-ratifying. Its supersession, release-condition discharge,
standing-block disposition, and `G-2` determination become effective together
only upon successful independent confirmation with unresolved findings `NONE`
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§8.2, 11
M44-WP3, 12.4, and 16.2).

The strict predecessors are M44-WP1 and M44-WP2. They are satisfied:
M44-WP1 is complete, frozen, and effective, and M44-WP2 is complete and frozen
with `G-1` closed and effective
([M44-WP1 Freeze Record](M44_WP1_FREEZE_RECORD.md) §§5 and 12;
[M44-WP2 Freeze Record](M44_WP2_FREEZE_RECORD.md) §§4 and 8;
[M44-WP2 Closeout](M44_WP2_CLOSEOUT.md) §§8–9). No predecessor result
predetermines `G-2`.

## 2. Purpose

The only purpose of this record is to exercise the M43 governance sequence
under frozen M43-WP1 §7.4 step 3 by correcting one defective composite
ownership row, while keeping the release condition and final-recording
obligation constitutionally distinct
([M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
§§7.3–7.4; [M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§§3.1 `G-2`, 8.2, and 11 M44-WP3).

This record does not re-open the confirmed ownership proof. It carries that
proof into the exact correction vehicle allocated by M44
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§8.2 and 11
M44-WP3).

## 3. Controlling authority hierarchy

The following hierarchy controls this correction:

1. [Platform Architecture](../architecture/platform_architecture.md) §§6.3 and
   6.5 allocates financial truth and canonical return and metric formula inputs
   to Ledger & Accounting, while allocating canonical derived measures, their
   semantics, performance measurement, and the meaning of performance to
   Portfolio Intelligence.
2. [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md)
   §§1–9 controls the accounting semantics that determine what enters period
   return; §10 requires analytics to consume
   `PortfolioSnapshot.investment_return_pct` and forbids independent
   recomputation.
3. [ADR-001](../decisions/ADR-001_TRANSACTION_LEDGER_SINGLE_SOURCE_OF_TRUTH.md)
   makes the immutable transaction ledger the source of truth for portfolio
   state, and [ADR-004](../decisions/ADR-004_ONE_IMPLEMENTATION_PER_RULE.md)
   requires one authoritative implementation per rule. Neither ADR transfers
   semantic ownership based on source placement, as confirmed by frozen
   M43-WP1 §7.2.
4. [M40-WP1](M40_WP1_Canonical_Market_Measure_Vocabulary_and_Ownership_Specification.md)
   §8.3 reserves `portfolio measure` and portfolio-performance meaning to
   Portfolio Intelligence.
5. [M42 Architecture](M42_ARCHITECTURE_PROPOSAL.md) §8 allocates deferred
   Portfolio performance and return computation to Portfolio Intelligence as a
   derived measure consuming frozen accounting rules.
   [M42-WP1](M42_WP1_PORTFOLIO_CANONICAL_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
   §3 leaves accounting arithmetic, NAV/return formulas, and cost-basis rules
   frozen in the Portfolio Calculation Rules.
6. Frozen [M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §8
   contains the row corrected here. Frozen
   [M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
   §§7.2–7.4 supplies the confirmed evidence, two-part finding, standing block,
   correction sequence, and steps 1–3 release condition.
7. Frozen [M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
   §§3.1 `G-2`, 8.2, 11 M44-WP3, 12.3–12.6, 16.2, and 17 OQ-5 allocates this
   correction, fixes its lifecycle and result, and preserves step 4 as a
   separate outstanding obligation. The frozen
   [M44-WP1 Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
   §§4.2, 7, and 8.1 fixes the admissible `G-2` states and required evidence.

This hierarchy is applied without amending any authority in it.

## 4. Extension basis

The sole extension basis for this record is `E-3 — Addition into declared
silence, under constitution G3`. Frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §5.3 assigns
that basis through this exact sentence:

> It supports supplying a repository-local record where a frozen governance
> chain required one and none was written (G-1), and supplying a superseding
> ruling that names a defective frozen row (G-2).

`E-3` is assigned by frozen M44 Architecture §5.3 to this exact `G-2` act; it
is not self-selected by M44-WP3. This record applies that assigned basis only
to the superseding ruling in §7 for the exact M43 Architecture §8
`Canonical period-return rule` row identified in §5.

`E-1` is inapplicable because this record does not carry forward an explicit
normative must from a frozen owner-domain contract into a documentary
container contract. `E-2` is inapplicable because this record does not
complete a serialization or canonical-byte representation expressly required
by a frozen contract. Neither basis supplies the governance correction
allocated to `G-2`.

No unstated silence is used as authority. This declaration satisfies frozen
M44 Architecture §5.3 and §6 `INV-C2`: the artifact names exactly one assigned
extension basis and quotes the exact frozen sentence supplying it.

## 5. Exact superseded M43 ownership row

The exact frozen source row is
[M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §8, row
`Canonical period-return rule`:

The following is a faithful re-layout of the original tab-delimited row into
four labelled block-quote fields; it is not presented as a literal Markdown
table transcription. No field value is altered.

> **Subsystem or concern:** Canonical period-return rule
> **Owner:** Candidate: Ledger & Accounting
> **Ownership status and authority:** OWNER TO PROVE AT WP1 — Constitution
> §§6.3/6.5, ADR-001/004, and PORTFOLIO_CALCULATION_RULES.md §10
> **M43 relationship:** WP6 is blocked until disposition; no second rule is
> permitted

Frozen M43-WP1 §7.3 rejected the indivisible claim that Ledger & Accounting owns
the entire composite period-return rule because that phrase collapses two
constitutionally distinct allocations
([M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
§§7.1–7.3).

## 6. Confirmed ownership allocation

The corrected allocation has exactly two parts:

| Concern | Sole constitutional owner | Controlling authority |
| --- | --- | --- |
| Financial truth and the canonical return and metric formulas' inputs, and the accounting semantics that determine what enters period return | Ledger & Accounting | [Platform Architecture](../architecture/platform_architecture.md) §6.3; [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md) §§1–9; [ADR-001](../decisions/ADR-001_TRANSACTION_LEDGER_SINGLE_SOURCE_OF_TRUTH.md); frozen [M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §§7.2–7.3 |
| Canonical derived measures and their semantics, including the meaning of period return as Portfolio performance | Portfolio Intelligence | [Platform Architecture](../architecture/platform_architecture.md) §6.5; [M40-WP1](M40_WP1_Canonical_Market_Measure_Vocabulary_and_Ownership_Specification.md) §8.3; [M42 Architecture](M42_ARCHITECTURE_PROPOSAL.md) §8; frozen [M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §§7.2–7.3 |

Ledger & Accounting therefore supplies the exact ledger-derived inputs and
replay/snapshot evidence under its frozen ownership. Portfolio Intelligence's
ownership of derived-measure meaning does not acquire, redefine, or transfer
the accounting semantics. Conversely, Ledger & Accounting's ownership of truth
and inputs does not acquire the Portfolio-performance meaning of the derived
measure (frozen [M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
§7.3).

[Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md)
§10 and [ADR-004](../decisions/ADR-004_ONE_IMPLEMENTATION_PER_RULE.md) preserve
one implementation and prohibit independent recomputation. The location of
that implementation does not decide or transfer constitutional semantic
ownership (frozen M43-WP1 §§7.2–7.3).

## 7. Constitutional correction

Subject to the confirmation boundary in §1 of this record, the M43 Architecture
§8 row named `Canonical period-return rule` is constitutionally corrected as
follows:

1. The row's indivisible candidate allocation to Ledger & Accounting is
   rejected.
2. Ownership is replaced by the two-part allocation in §6 of this record:
   Ledger & Accounting owns financial truth, the canonical return and metric
   formulas' inputs, and the accounting semantics determining what enters the
   return; Portfolio Intelligence owns the canonical derived measure, its
   semantics, and the meaning of period return as Portfolio performance.
3. The row's prohibition on a second period-return rule remains in force.
4. The correction creates no new rule, formula, method, method version, or
   implementation and changes no accounting or Portfolio Calculation Rule.

This is the single-row step 3 correction authorized by
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§8.2 and 11
M44-WP3, carrying the confirmed finding from frozen M43-WP1 §§7.2–7.4.

## 8. Supersession effect

Upon successful independent confirmation, §7 of this record supersedes only
the ownership allocation in the named M43 Architecture §8 row. The frozen
source text remains immutable and unedited; this later, independently confirmed
constitutional record becomes the controlling allocation for that row
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§5.3,
8.2, and 11 M44-WP3).

No other M43 row, artifact, allocation, formula, accounting rule, ADR, or
open question is superseded or changed
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §8.2).

## 9. Steps 1–3 release-condition disposition

Frozen M43-WP1 §7.4 defines this four-step documentary sequence:

1. independent confirmation records whether the §7.3 finding is confirmed and
   activates the block only if confirmed;
2. the confirmed block is carried as a standing M43 governance item owned by
   the M43 governance sequence;
3. the governing M43 ownership row is reconciled by an independently reviewed
   constitutional correction before WP6 begins; and
4. final resolution is recorded in the consolidated Decision Log entry
   authorized at M43 epic closeout.

The same section fixes the release condition: steps 1–3 must be complete before
WP6 may begin. Steps 1 and 2 are already complete in the frozen M43-WP1
lifecycle. This record supplies step 3 only when independently confirmed
([M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
§7.4; [M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§§3.1 `G-2`, 8.2, and 11 M44-WP3).

Therefore, successful independent confirmation of this record discharges the
steps 1–3 release condition. RC2 correction alone does not
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§8.2, 11
M44-WP3, and 12.4).

## 10. Standing M43-WP6 block disposition

The standing item is exactly:

`M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6`

Upon successful independent confirmation of this record, the governance
correction required by that item is supplied and the standing item is
dispositioned. Before confirmation, it remains in force
([M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
§7.4; [M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§3.1
`G-2`, 8.2, and 11 M44-WP3).

This disposition concerns the inherited M43-WP6 governance-correction
condition only. It does not design M43-WP6, start successor work, or satisfy
the separate entry requirements for D-1
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§4.3, 8.2,
11 M44-WP3, and 12.3).

## 11. Step 4 outstanding-recording statement

Step 4 requires the final resolution to be recorded in the consolidated
Decision Log entry authorized at M43 epic closeout by frozen M43 §§13 and 17.
That named vehicle has passed without making this recording
([M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
§7.4; [M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§3.1
`G-2`, 12.6, and 17 OQ-5).

Step 4 remains outstanding. This artifact does not make the final recording,
does not claim final `G-2` recording, and does not create, select, or authorize
a substitute recording vehicle. Whether a later M44 Decision Log entry may
serve as a substitute is reserved to an authority outside M44-WP3
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§12.6 and
17 OQ-5).

Step 4 is a recording obligation, not part of the frozen steps 1–3 release
condition. Its continuing status therefore does not negate the conditional
release-condition discharge in §9
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§3.1
`G-2`, 11 M44-WP3, and 17 OQ-5).

## 12. D-1 complete entry preconditions

M44-WP3 alone does not permit D-1 to begin. It supplies only the `G-2` entry
gate after successful confirmation. Under frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§4.3–4.5,
11.1, 12.3–12.5, and 16, D-1 may begin only after all of the following are
true:

1. M44-WP3 is independently confirmed with unresolved findings `NONE`, which
   makes the §9 release-condition discharge and §10 standing-block disposition
   effective; M44-WP3 is also frozen as a separate D-1 prerequisite.
2. M44-WP6 is independently confirmed with unresolved findings `NONE` and
   frozen.
3. M44-WP7 is independently confirmed with unresolved findings `NONE` and
   frozen; M44-WP7 may not be confirmed before M44-WP6 is frozen.
4. The prerequisites through which M44-WP6 and M44-WP7 are reachable have been
   satisfied: M44-WP1 is complete and frozen; M44-WP4 and M44-WP5 are
   independently confirmed and frozen; `G-3` is `CLOSED`; `G-5` is `CLOSED`
   through the confirmed and frozen M44-WP6 and M44-WP7 component results; the
   §12.1.1 gate-state checkpoint has passed before M44-WP6; and the
   M44-WP6-before-M44-WP7 ordering is preserved.
5. Every applicable independent review and confirmation has unresolved
   findings `NONE`, and no checkpoint or gate state withholds the successor
   work.
6. A separate authorization to begin D-1 is granted. This record allocates no
   successor milestone and does not itself authorize downstream authoring,
   implementation, or runtime activity.

`G-4 OPEN` is not a prerequisite failure for M44-WP6 or M44-WP7, but it
constrains their content through the frozen Component G binding rule
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §12.3).
Nothing in this record changes `G-3`, `G-4`, or `G-5`.

M44-WP3 has no downstream M44 work-package consumer. Its confirmed result
supplies one entry gate for D-1 only; D-2a, D-2b, D-3, and D-4 are affected
transitively through the frozen successor sequence and retain all of their
other prerequisites
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§4.3–4.5
and 11.1; [M44-WP1 Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
§4.2).

## 13. G-2 terminal determination

The sole permitted successful result of M44-WP3 is:

`RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`

Its exact meaning is that the frozen release condition is discharged while a
separate recording obligation remains outstanding with its lapsed vehicle
named. It does not count as closure
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§11
M44-WP3 and 16.2; [M44-WP1 Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
§§4.2 and 8.1).

This RC2 records that determination prospectively. It becomes the effective
`G-2` state only after independent confirmation with unresolved findings
`NONE`. If step 3 is not performed or does not receive that confirmation, the
residual permitted result is `OPEN`, with the exact missing element and its
exact owner named
([M44-WP1 Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
§4.2).

`G-2` is not `CLOSED`. Final recording has not occurred. The successful
non-closure determination changes no terminal state of `G-1`, `G-3`, `G-4`,
or `G-5` ([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§§11 M44-WP3 and 16.2).

## 14. Authority explicitly absent

This record has no authority to:

- re-argue the confirmed M43-WP1 §7.3 ownership split;
- define or select a return formula, calculation method, method version, or
  call site;
- amend the Portfolio Calculation Rules, ADR-001, ADR-004, or any frozen
  artifact;
- design M43-WP6 or settle any Portfolio Calculation Rules §12 open question;
- make the step 4 recording, claim final `G-2` recording, or create or authorize
  a substitute recording vehicle;
- authorize runtime, source-code, implementation, executable, production,
  persistence, schema, migration, API, transport, UI, provider, scheduler,
  cache, or observability work;
- disposition `G-1`, `G-3`, `G-4`, or `G-5`;
- authorize D-1 or any other downstream work;
- update the Decision Log, Implementation INDEX, ROADMAP, or GLOSSARY; or
- declare any runtime capability or M44 Epic Closeout complete.

These absences follow from frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§4.4–4.5,
8.2, 11 M44-WP3, 12.6, 16.3, and 17 OQ-5.

## 15. Frozen-artifact preservation

Every authority cited by this record is consumed as immutable evidence.
Supersession operates through this later constitutional record; it does not
edit the frozen M43 Architecture row
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§5.3, 8.2,
and 11 M44-WP3).

This RC2 changes no M1–M43 artifact, no frozen M44 Architecture, WP1, or WP2
artifact, no Decision Log or Implementation INDEX entry, and no ROADMAP or
GLOSSARY content. Repository governance synchronization occurs only at M44
Epic Closeout under separate authorization
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§12.6 and
16.6–16.8).

## 16. Repository impact

The complete authorized repository impact of the RC2 correction package is
exactly these three WP3 files:

`docs/implementation/M44_WP3_PERIOD_RETURN_OWNERSHIP_GOVERNANCE_CORRECTION.md`

`docs/implementation/M44_WP3_INDEPENDENT_CONSTITUTIONAL_REVIEW.md`

`docs/implementation/M44_WP3_FORMAL_CONSTITUTIONAL_RESPONSE.md`

Implementation deliverables are `NONE`. No frozen file is modified. Any
renewed-review, confirmation, freeze, closeout, Decision Log, or
Implementation INDEX artifact belongs to a later, separately authorized
lifecycle step
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§11
M44-WP3, 12.4, and 12.6).

## 17. Completion and independent-review requirements

RC2 correction is not work-package completion. Completion requires:

1. independent constitutional review by a reviewer who did not author the
   normative rows;
2. a required-corrections response if findings exist;
3. renewed independent review of every correction;
4. independent constitutional confirmation with unresolved findings `NONE`;
5. confirmation that the named M43 row is superseded in substance by exactly
   the §6 allocation, without frozen-source modification;
6. confirmation that the steps 1–3 release condition and standing block are
   dispositioned only through the confirmation's effect;
7. confirmation that step 4 remains outstanding and no substitute vehicle is
   claimed;
8. confirmation of the `G-2` non-closure determination in §13; and
9. freeze after successful confirmation.

These requirements are fixed by
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§11
M44-WP3, 12.4–12.5, and 16.2–16.5, and by the
[M44-WP1 Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
§7.

## 18. Acceptance criteria

RC2 is ready for renewed independent constitutional review only if all of the
following are satisfied:

| Criterion | Required result |
| --- | --- |
| Extension basis | `E-3` is the sole basis assigned by frozen M44 Architecture §5.3; its exact supplying sentence is quoted, `E-1` and `E-2` are ruled out, and no unstated silence is used. |
| Exact row | The M43 Architecture §8 `Canonical period-return rule` row is named and quoted. |
| Singular allocation | Each of the two distinct concerns in §6 has exactly one owner. |
| Complete authority proof | Every authority listed in frozen M43-WP1 §7.2 is cited and applied. |
| Constitutional scope | Only the one named row is corrected; frozen sources remain unchanged. |
| No duplicate rule | The existing one-implementation and no-second-rule constraints remain intact. |
| No calculation invention | No formula, method, method version, or call site is introduced. |
| Release distinction | Steps 1–3 discharge is conditional on successful confirmation and is kept distinct from step 4. |
| Standing block | The exact M43-WP6 block and its confirmation-dependent disposition are recorded. |
| Recording obligation | Step 4, its lapsed vehicle, and the absence of substitute-vehicle authority are explicit. |
| Gate state | `G-2` has exactly the successful non-closure result fixed in §13; final recording is not claimed. |
| D-1 boundary | The complete prerequisite set in §12 is stated; WP3 alone grants no downstream start authority. |
| Remaining gates | `G-1`, `G-3`, `G-4`, and `G-5` are unchanged. |
| Authority boundary | Runtime, implementation, executable, and production authority remain `NONE`. |
| Repository scope | Exactly the normative RC2, preserved review, and formal response files comprise this package; no frozen file changes. |
| Review state | Renewed independent review and confirmation remain pending at RC2. |

## 19. RC2 declaration

This artifact is declared:

`M44-WP3 RC2 — READY FOR RENEWED INDEPENDENT CONSTITUTIONAL REVIEW`

The declaration means only that the corrected normative deliverable and its
review-response package are ready for renewed independent review. It does not
resolve the RC1 findings by itself, issue confirmation, make the correction
effective, disposition the standing block, establish the `G-2` terminal state,
perform the final recording, freeze M44-WP3, or authorize D-1 or any runtime
or implementation work
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§11
M44-WP3, 12.4–12.6, and 16.2–16.5).
