# BANPU-WP5 — Allocation Record

**Artifact class:** Additive constitutional allocation record
**Allocation date:** 2026-08-14
**Issuing role:** BANPU-WP5 Allocation Authority
**Allocated work package:** `BANPU-WP5 — Accounting readers and bounded reconstruction`
**Disposition:** `BANPU-WP5 ALLOCATED`
**Implementation authority created:** `NONE`
**Release authority created:** `NONE`
**BANPU-WP6+ authority created:** `NONE`

## 1. Allocation authority and constitutional boundary

Acting solely as the competent BANPU-WP5 Allocation Authority, this act
allocates the work package already defined by the canonical BANPU planning and
governance corpus. The authority exercised here is limited to:

- verifying the predecessor and dependency gates against current canonical
  repository evidence;
- binding the exact existing BANPU-WP5 scope and its inherited conditions to
  this allocation; and
- creating this additive Allocation Record.

This allocation does not create planning-amendment, implementation,
implementation-authorization, release, deployment, production-data mutation,
successor-allocation, or repository-synchronization authority. It does not
change, interpret, or supersede any frozen artifact.

## 2. Canonical authority relied upon

This allocation relies on the following existing authority, in descending
order of scope:

1. [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   the approved and authoritative implementation specification, especially
   §12 (accounting-reader classification and rebuild boundary), §13–14
   (migration/deployment strategy establishing that snapshot rebuild is a
   later, separately controlled production act), and the WP1 residual
   register (`MINOR-2` WP5 half);
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md),
   especially §1 (universal package rules), §2 (package inventory), §7
   (BANPU-WP5), and §11 (strict dependency graph);
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md),
   especially §1 (strict serial sequence) and §7 (Step 5 preconditions,
   repository state, expected changes, verification, and exit criteria);
4. the completed and frozen predecessor records:
   [`BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP2_EPIC_CLOSEOUT.md`](BANPU_WP2_EPIC_CLOSEOUT.md),
   [`BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP3_EPIC_CLOSEOUT.md`](BANPU_WP3_EPIC_CLOSEOUT.md),
   [`BANPU_WP4_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP4_IMPLEMENTATION_CONFIRMATION.md),
   [`BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md), and
   [`BANPU_WP4_EPIC_CLOSEOUT.md`](BANPU_WP4_EPIC_CLOSEOUT.md); and
5. the completed BANPU-WP4 repository synchronizations in the
   [Decision Log](../engineering/DECISION_LOG.md#banpu-wp4-decision-log-synchronization)
   and [Implementation INDEX](INDEX.md#banpu-wp4--registry-preparation-and-live-materialization).

The design, roadmap, and sequence are frozen members of the BANPU-WP1 corpus
recorded by the BANPU-WP1 Freeze Record §4. This act relies on their canonical
recorded authority and current repository presence; it does not restate or
replace their frozen identities.

Before relying on it, the BANPU-WP4 terminal state was independently
re-verified against live repository bytes rather than accepted from prompt
text or the Implementation INDEX narrative alone: all six frozen BANPU-WP4
corpus files were re-hashed under the Git-canonical LF convention fixed by
`BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md` §F.1, and all six reproduced the
Freeze Record §F.2 identities and the §F.3 aggregate identity
`2C22C139F1C013CFF8DAB210CFBABA866A4DF42BBBFF05EBDD735603488D9FBE` exactly.
The Decision Log's `BANPU-WP4 Decision Log Synchronization` entry and the
Implementation INDEX's BANPU-WP4 row were independently read and found
mutually consistent: both record BANPU-WP4 as `COMPLETE`, `FROZEN`, and
`CLOSED`, and both record WP5's entry prerequisite as satisfied while WP5
itself remains `NOT ALLOCATED` and `NOT AUTHORIZED`.

## 3. Exact allocated scope

The allocation is exactly `BANPU-WP5 — Accounting readers and bounded
reconstruction`, with this canonical purpose: ensure snapshots and return
fields represent conversion and optional cash-in-lieu correctly without
touching predecessor history.

The allocated scope is exactly:

- classify conversion as zero external/import/manual flow;
- include only admitted cash-in-lieu fees and realized P/L;
- add the hard `from_date` conversion boundary to portfolio rebuilding;
- preserve stored pre-boundary prices and values;
- recognize evidence-annotated suspension-gap return without "repairing" it
  away; and
- emit successor asset identity in post-boundary holdings JSON.

The canonical expected implementation surface, recorded here as scope evidence
and not as implementation authority, is:

- `backend/services/portfolio_metrics.py`;
- `backend/services/portfolio_snapshots.py`;
- `backend/services/snapshot_return_recovery.py`;
- `backend/services/portfolio_rebuilder.py` only for bounded historical
  reconstruction and return-field integration not already delivered in WP2;
- `backend/manage.py` only if `verify_snapshots` needs conversion-boundary
  classification;
- `backend/tests/test_portfolio_metrics.py`;
- `backend/tests/test_portfolio_metrics_parity.py`;
- `backend/tests/test_snapshot_return_recovery.py`;
- `backend/tests/test_portfolio_rebuilder.py`; and
- `backend/tests/test_verify_snapshots.py`.

The Roadmap §7 explicit no-change surface remains binding as scope evidence:
transaction write semantics delivered by WP4, market-data provider semantics
delivered by WP3, shadow and evaluation modules, immutable
recommendation/optimizer tables, and all M46 files.

Allocation does not change, narrow, widen, or implement this scope.

## 4. Prerequisite and gate determination

| Requirement | Canonical evidence | Determination |
|---|---|---|
| BANPU-WP2 accepted, frozen, and closed | BANPU-WP2 Implementation Freeze Record and Epic Closeout | `SATISFIED` |
| BANPU-WP3 accepted, confirmed, frozen, and closed | BANPU-WP3 Implementation Confirmation, Implementation Freeze Record, and Epic Closeout | `SATISFIED` |
| BANPU-WP4 accepted, confirmed, frozen, and closed | BANPU-WP4 Implementation Confirmation, Implementation Freeze Record, and Epic Closeout — independently re-hashed in §2 above | `SATISFIED` |
| Roadmap dependency `BANPU-WP2–WP4` | Roadmap §2 and BANPU-WP5 §7 | `SATISFIED` |
| Sequence Step 5 precondition: Step 4 accepted | Mandatory Sequence §7 precondition; completed WP4 lifecycle evidence above | `SATISFIED` |
| Sequence Step 5 precondition: conversion accounting stable in live and replay state | WP2 replay is frozen and closed; WP4 live materialization is confirmed and frozen | `SATISFIED` |
| BANPU-WP4 Decision Log synchronization | [Decision Log](../engineering/DECISION_LOG.md#banpu-wp4-decision-log-synchronization) — `BANPU-WP4 DECISION LOG SYNCHRONIZED` | `SATISFIED` |
| BANPU-WP4 Implementation INDEX synchronization | [Implementation INDEX](INDEX.md#banpu-wp4--registry-preparation-and-live-materialization) — BANPU-WP4 row records `COMPLETE`, `FROZEN`, `CLOSED`; WP5 entry prerequisite satisfied | `SATISFIED` |
| Prior BANPU-WP5 allocation absent | No earlier `BANPU_WP5_ALLOCATION_RECORD.md` or WP5 implementation-authorization artifact existed before this act | `SATISFIED` |

BANPU-WP4 completion, confirmation, freeze, and both repository
synchronizations therefore satisfy the immediate-predecessor requirement. The
constitutional prerequisites for allocation are satisfied.

Entry-prerequisite satisfaction is distinct from allocation, and allocation is
distinct from Implementation Authorization. This act performs only
allocation; it does not treat WP4's authority, or the mere existence of the
satisfied entry prerequisite recorded by the Decision Log and Implementation
INDEX, as automatically flowing into WP5 authorization or implementation.

## 5. Residuals and inherited conditions

Allocation resolves, defines, weakens, reinterprets, or waives none of the
following:

- BANPU-WP1 `MINOR-2`, WP5 half: mechanical NAV continuity tolerance
  admissibility. `BANPU_WP1_FREEZE_RECORD.md` §7,
  `BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` §9.2/A9, and
  `BANPU_WP4_WORK_PACKAGE_PLAN.md` each record this as WP5's named remaining
  obligation ("the remaining mechanical-tolerance obligation belongs to
  WP5"). It is a future WP5 implementation-time verification gate, not an
  open WP1 finding and not an allocation blocker;
- the `POSITION_CONVERSION_REBUILD_BOUNDARY` finding, catalogued by
  `BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md` with its evidence predicate
  recorded as WP5-owned; the predicate remains unimplemented and is bound to
  the already-recorded §3 scope item, not created or discharged by this act;
- BANPU-WP1 `MINOR-1` and `NEW-MINOR-A`, assigned to BANPU-WP4 and carried
  forward by the BANPU-WP4 Epic Closeout without resolution, reinterpretation,
  or expansion;
- BANPU-WP1 `MINOR-5`, whose remaining ownership stays with BANPU-WP7
  rehearsal and BANPU-WP8 release evidence;
- BANPU-WP2 residual identifiers `MINOR-A`, `MINOR-B`, and `OBSERVATION-A`
  through `OBSERVATION-E`, which remain unresolved and are inherited by
  BANPU-WP5 through BANPU-WP8 unchanged;
- WP3 residual R6, the WP3-scoped R7 formal waiver, and WP3's non-blocking
  closeout observations;
- BANPU-WP4's carried baseline missing-log assertion and reviewed
  temporary-path permission condition, and B1–B6, RTO-1 through RTO-13,
  PIA-1 through PIA-4, and MINOR-1/NEW-MINOR-A as classified by the BANPU-WP4
  Third Renewed Independent Implementation Review, Implementation
  Confirmation, Implementation Freeze Record, and Epic Closeout; and
- the emitter-locus item referred out by WP3 PD-3 to the authority governing
  the canonical design, roadmap, and package inventory.

No inherited item above is recorded by any canonical WP2, WP3, or WP4 closeout
or synchronization as a WP5 allocation-entry blocker; §4 records that every
named entry gate is instead `SATISFIED`. `MINOR-2`'s WP5 half and the
`POSITION_CONVERSION_REBUILD_BOUNDARY` predicate are WP5-owned obligations for
the future implementation act, not conditions this allocation resolves.

No condition in this section is satisfied by allocation itself. Any condition
that governs implementation remains unsatisfied until demonstrated by the
separately authorized act that owns it.

## 6. Allocation disposition

**`BANPU-WP5 ALLOCATED`**

The allocation binds only the exact scope in §3 and the unchanged inherited
conditions in §5. It creates no implementation authority. No production,
service, model, migration, test, CLI, frontend, or production-data change may
be made under color of this record. BANPU-WP5 implementation remains **not
authorized** and **not started**.

## 7. Explicit exclusions

This act does **not**:

- authorize or perform BANPU-WP5 implementation;
- create or perform BANPU-WP5 Implementation Authorization;
- amend, reopen, rewrite, synchronize, or reinterpret the canonical design,
  roadmap, sequence, or any frozen planning, implementation, confirmation,
  freeze, closeout, Decision Log, or INDEX artifact;
- resolve, define, close, weaken, or waive any residual or referred item,
  including `MINOR-2`'s WP5 half or the `POSITION_CONVERSION_REBUILD_BOUNDARY`
  predicate;
- add a public endpoint, operator CLI, frontend path, schema, migration,
  general corporate-action framework, or `LedgerRepair` behavior;
- authorize release, deployment, production execution, cache mutation,
  portfolio conversion, or production-data mutation;
- mutate, rebuild, repair, or otherwise touch any snapshot, historical or
  otherwise — this act performs no reconstruction of any kind;
- allocate, authorize, plan, or begin BANPU-WP6 or any later package;
- grant authority over M46; or
- stage, commit, push, merge, or publish repository changes.

The canonical explicit no-change surface remains binding as scope evidence:
transaction write semantics delivered by WP4, market-data provider semantics
delivered by WP3, shadow and evaluation modules, immutable
recommendation/optimizer tables, and all M46 files.

## 8. Resulting constitutional state

- BANPU-WP1: `COMPLETE AND FROZEN`;
- BANPU-WP2: `COMPLETE AND FROZEN`;
- BANPU-WP3: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP4: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP4 implementation authority: `EXHAUSTED / CLOSED`;
- BANPU-WP4 release authority: `NONE`;
- BANPU-WP5 allocation: `COMPLETE — ALLOCATED`;
- BANPU-WP5 implementation authority: `NONE`;
- BANPU-WP5 implementation: `NOT AUTHORIZED / NOT STARTED`;
- BANPU-WP5 release and deployment authority: `NONE`;
- BANPU-WP6 and later packages: `NOT ALLOCATED / NOT AUTHORIZED`; and
- frozen BANPU artifacts, Decision Log, and Implementation INDEX: unchanged.

## 9. Snapshot correction boundary — separately reported

This allocation does not determine, own, or advance historical snapshot
correction authority beyond binding the WP5 scope items in §3 that already
name rebuild-boundary enforcement and pre-boundary preservation. The
canonical design (§13–14) places the actual bounded-rebuild-from-transition
-date act inside a "separately controlled production deployment sequence"
gated on BANPU-WP8 acceptance (Roadmap §12), executed through the BANPU-WP7
operator CLI, which BANPU-WP7's own roadmap scope explicitly forbids from
executing production changes as a code package. No WP1–WP8 code package, this
allocation included, mutates a snapshot. This finding is reported in full in
the final report below and is not restated as a disposition field on this
record.

## 10. Exact next constitutional act

The exact next required constitutional act is **BANPU-WP5 Implementation
Authorization**, performed by a distinct competent authorization authority over
the exact allocated scope and inherited conditions recorded here.

That future act must determine implementation entry against every applicable
canonical gate, including the WP5-owned `MINOR-2` half and the
`POSITION_CONVERSION_REBUILD_BOUNDARY` predicate obligations. It may not infer
that this allocation satisfied them. Implementation remains a separate later
act even if authorization is granted.

This record performs no part of that authorization or implementation.

## 11. Repository verification

| Verification | Result |
|---|---|
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP5_ALLOCATION_RECORD.md` |
| Frozen BANPU artifacts modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX files modified | `NONE` |
| Snapshot data or snapshot code touched | `NONE` |
| BANPU-WP4 frozen corpus re-verified (six files, canonical LF) | `PASS` — all six exact against `BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md` §F.2/§F.3 |
| Trailing-whitespace verification | `PASS` |
| Markdown relative-link target verification | `PASS` — all linked targets exist in `docs/implementation/` and `docs/engineering/DECISION_LOG.md` |
| Markdown fragment-heading verification | `PASS` |
| `git diff --check` | see final report |
| `git diff --cached --check` | see final report |
| Nothing staged | see final report |
| `graphify update .` | see final report |
| Commit created | `NO` |
