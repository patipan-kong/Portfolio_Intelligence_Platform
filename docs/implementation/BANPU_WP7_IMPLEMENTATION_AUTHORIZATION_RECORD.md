# BANPU-WP7 — Implementation Authorization Record

**Artifact class:** Additive constitutional authorization record
**Authorization date:** 2026-08-18
**Issuing role:** BANPU-WP7 Implementation Authorization Authority
**Authorized work package:** `BANPU-WP7 — Operator command and migration rehearsal`
**Disposition:** `BANPU-WP7 IMPLEMENTATION AUTHORIZED`
**Implementation authority created:** `LIMITED — see §4, §6–§9`
**Release/deployment/production-mutation authority created:** `NONE`
**BANPU-WP8+ authority created:** `NONE`

## 1. Authorization authority and boundary

Acting solely as the distinct competent BANPU-WP7 Implementation Authorization
Authority, this act authorizes implementation of the exact work package
already allocated by
[`BANPU_WP7_ALLOCATION_RECORD.md`](BANPU_WP7_ALLOCATION_RECORD.md).

The authority exercised here is limited to verifying authorization-entry
conditions, binding implementation to the allocated scope and inherited
gates, and creating this additive record. This act does not implement code,
perform a review or confirmation, freeze implementation, authorize release,
deployment, or production-data mutation, create a Work Package Plan, or
amend or synchronize any existing artifact.

Allocation is a prerequisite to this act, not evidence that an
implementation-time gate has been performed. No gate is marked satisfied
merely because WP7 was allocated. This authority is distinct from, and does
not include, the allocation authority already exercised by the Allocation
Record, any implementation authority exercised later under a Work Package
Plan this act does not create, and any release, deployment, or production
authority, which remains wholly unestablished by this act.

## 2. Canonical authority relied upon

This authorization relies on, and does not amend or reinterpret:

1. [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   the authoritative implementation specification, as the originating
   authority for the operator command and rehearsal surface that the Roadmap
   and Sequence decompose into BANPU-WP7;
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md)
   §9 (BANPU-WP7 purpose, scope, files expected to change, explicit files not
   to change, dependencies, deliverables, acceptance criteria, verification,
   and size estimates) and §11 (strict dependency graph);
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md) §9
   (Step 7 preconditions, repository state, expected code changes,
   verification, and exit criteria);
4. the frozen predecessor evidence:
   [`BANPU_WP1_FREEZE_RECORD.md`](BANPU_WP1_FREEZE_RECORD.md) §7 (`MINOR-5`
   row: WP7 rehearsal / WP8 release-evidence split; `NEW-MINOR-A` row: WP4
   authoring / WP7 production-dialect-rehearsal split),
   [`BANPU_WP3_ALLOCATION_RECORD.md`](BANPU_WP3_ALLOCATION_RECORD.md) (`PD-3`
   referred out, not a WP3 decision/residual/obligation),
   [`BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP4_EPIC_CLOSEOUT.md`](BANPU_WP4_EPIC_CLOSEOUT.md),
   [`BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP5_EPIC_CLOSEOUT.md`](BANPU_WP5_EPIC_CLOSEOUT.md),
   [`BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md),
   and
   [`BANPU_WP6_EPIC_CLOSEOUT.md`](BANPU_WP6_EPIC_CLOSEOUT.md) §17 ("WP7
   successor boundary");
5. the completed BANPU-WP6 repository synchronizations in the
   [Decision Log](../engineering/DECISION_LOG.md#banpu-wp6-decision-log-synchronization)
   and [Implementation INDEX](INDEX.md#banpu-wp6--shadow-and-succession-aware-time-series-continuity);
   and
6. the BANPU-WP7 Allocation Record, 19,609 raw working-tree bytes, 329
   physical lines, SHA-256
   `1aa24cd242c95039b81df1a43f061b04140ea0ed5e0a2e7405ae18945900f4f1`,
   disposition `BANPU-WP7 ALLOCATED`.

Before relying on them, the Roadmap §9 text and the Sequence §9 text were
independently re-read from the live working tree rather than accepted from
the Allocation Record's summary or from prompt text; both were found to
match the Allocation Record's §3 restatement exactly. `BANPU_WP1_FREEZE_RECORD.md`
§7 was independently re-read and confirms `MINOR-5` splits into a WP7
rehearsal portion and a WP8 release-evidence portion, and `NEW-MINOR-A`
splits into a WP4 authoring portion (closed) and a WP7 production-dialect
rehearsal portion. `PD-3`'s referred-out, unassigned status was independently
re-confirmed by grepping `BANPU_WP4_ALLOCATION_RECORD.md`,
`BANPU_WP5_ALLOCATION_RECORD.md`, `BANPU_WP6_ALLOCATION_RECORD.md`, and
`BANPU_WP6_EPIC_CLOSEOUT.md` §15, none of which assign it to WP7. The
Decision Log and Implementation INDEX were independently re-read and confirm
BANPU-WP6 as `COMPLETE`, `FROZEN`, and `CLOSED` (`INDEX.md` lines 264–291;
`DECISION_LOG.md` line 3051, `BANPU-WP6 DECISION LOG SYNCHRONIZED`), with no
BANPU-WP7 entry present in either file.

A repository-wide search for `BANPU_WP7_*` found exactly one prior artifact —
the Allocation Record cited above — and no BANPU-WP7 Implementation
Authorization artifact, Work Package Plan, or implementation artifact of any
kind. Current `git status --porcelain` shows only that single untracked
Allocation Record file from the prior act; nothing is staged; HEAD remains
`ae223a42df688563748c0e6e6cb898e66bcb3da0`, unchanged since the Allocation
act. The design, roadmap, and sequence remain frozen members of the
BANPU-WP1 corpus; their recorded identities and authority are relied upon as
canonical and are not replaced by a new identity convention here.

Live precedent on lifecycle ordering was independently checked:
`BANPU_WP6_PLANNING_FREEZE_RECORD.md` §11 and §5 establish, from the WP6
authority chain itself, that "WP6's Allocation and Authorization already
occurred, prior to and independently of the Work Package Plan, Planning
Confirmation, and \[Planning] Freeze — the same later-established sequencing
WP5 itself used," explicitly superseding the earlier WP2/WP3 "Work Package
Plan Gate 1" model under which a package-specific Work Package Plan had to be
frozen before allocation. BANPU-WP7's Allocation Record, created without an
antecedent BANPU-WP7 Work Package Plan, is therefore consistent with the
current, twice-confirmed (WP5, WP6) established precedent, not a departure
from it. This authorization record relies on that same current precedent and
does not require, and did not require, a BANPU-WP7 Work Package Plan to
exist before this act.

## 3. Exact authorized implementation scope

Authorization is granted exactly for `BANPU-WP7 — Operator command and
migration rehearsal`, whose canonical purpose is to provide a safe,
idempotent, CLI-only path to prepare and apply the reviewed production
manifest.

Implementation authority covers exactly these capabilities (Roadmap §9
"Scope"):

- adding the `apply_position_conversion` CLI with dry-run default and
  explicit `--commit`;
- validating manifest schema, registry state, broker facts, quote epoch,
  continuity evidence, rebuild boundary, and both replay modes;
- producing a deterministic before/after report without exposing
  credentials or raw provider payloads; and
- adding cache-purge and bounded-rebuild instructions, without executing
  production changes in the package.

## 4. Authorized file surface

### 4.1 Production/operational surface

- `backend/manage.py` — CLI command addition only, bounded to §3;
- operational documentation, only if strictly required by the canonical
  design, and not M46 documentation — no other new production or
  documentation file is authorized.

### 4.2 Test surface

- a new sanitized test manifest under `backend/tests/fixtures/`;
- a new focused CLI test file strictly bounded to the capabilities in §3.

No production file outside §4.1 and no test file outside §4.2 is authorized.
A different file or capability requires a distinct constitutional
authorization; it cannot be inferred from the roadmap's "expected files"
language.

## 5. Prerequisite and implementation-entry determination

| Requirement | Evidence and classification | State at authorization |
|---|---|---|
| BANPU-WP7 allocation exists | Allocation Record disposition `BANPU-WP7 ALLOCATED`; identity bound in §2 | `SATISFIED` |
| BANPU-WP1 accepted, confirmed, frozen | `BANPU_WP1_FREEZE_RECORD.md`; Roadmap §9 dependency `WP1–WP6` | `SATISFIED` |
| BANPU-WP2 accepted, confirmed, frozen | `BANPU_WP2_EPIC_CLOSEOUT.md` | `SATISFIED` |
| BANPU-WP3 accepted, confirmed, frozen, closed | `BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP3_EPIC_CLOSEOUT.md` | `SATISFIED` |
| BANPU-WP4 accepted, confirmed, frozen, closed | `BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP4_EPIC_CLOSEOUT.md` | `SATISFIED` |
| BANPU-WP5 accepted, confirmed, frozen, closed | `BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP5_EPIC_CLOSEOUT.md` | `SATISFIED` |
| BANPU-WP6 accepted, confirmed, frozen, closed | `BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP6_EPIC_CLOSEOUT.md` line 6 — independently re-verified this act (§2) | `SATISFIED` |
| Roadmap dependency WP1–WP6 | Roadmap §9 "Dependencies: BANPU-WP1 through BANPU-WP6 accepted" | `SATISFIED` |
| Sequence Step 7 precondition: Steps 1–6 accepted | Sequence §9 precondition 1; completed WP1–WP6 lifecycle evidence above | `SATISFIED` |
| Sequence Step 7 precondition: all runtime readers and writers understand the conversion | Sequence §9 repository-state line: "Internal conversion service exists."; WP6 Closeout §11/§12 (18/18 capability-completion and acceptance rows `PASS`) | `SATISFIED` |
| BANPU-WP6 Decision Log synchronization | [Decision Log](../engineering/DECISION_LOG.md#banpu-wp6-decision-log-synchronization) — `BANPU-WP6 DECISION LOG SYNCHRONIZED` | `SATISFIED` |
| BANPU-WP6 Implementation INDEX synchronization | [Implementation INDEX](INDEX.md#banpu-wp6--shadow-and-succession-aware-time-series-continuity) — BANPU-WP6 row records `COMPLETE`, `FROZEN`, `CLOSED` | `SATISFIED` |
| Review-frozen repository state with no overlapping implementation change | Current `git status --porcelain` shows only the untracked BANPU-WP7 Allocation Record; no file in the §4.1/§4.2 WP7 surface is touched | `SATISFIED` |
| No earlier BANPU-WP7 implementation authority | Repository search found no prior `BANPU_WP7_IMPLEMENTATION_AUTHORIZATION_RECORD.md` or equivalent artifact | `SATISFIED` |
| No conflicting authority | WP6 implementation authority exhausted/closed; WP8+, release, deployment, production-data mutation, and M46 remain unauthorized | `SATISFIED` |
| No WP7-specific pre-authorization residual gate | `MINOR-5` (WP7 rehearsal portion) and `NEW-MINOR-A` (WP7 production-dialect-rehearsal portion) are implementation-time/exit-evidence obligations, not pre-authorization gates — see §6 | `NOT APPLICABLE` |
| Roadmap §9 acceptance criteria / Sequence §9 exit criteria | Pre-use implementation-time and exit-evidence obligations, not pre-authorization gates — see §7 | `OPEN — IMPLEMENTATION-TIME` |

All authorization-entry prerequisites are satisfied. Open implementation-time
conditions remain open and are not satisfied, waived, or bypassed by this
act.

## 6. Treatment of `MINOR-5`, `NEW-MINOR-A`, and `PD-3`

Neither the whole of `MINOR-5` nor the whole of `NEW-MINOR-A` is assigned to
BANPU-WP7 by any canonical artifact read for this act; each is a split
residual with only one function-defined portion bound here:

- `MINOR-5`: `BANPU_WP1_FREEZE_RECORD.md` §7 assigns only the rehearsal
  portion (real PostgreSQL upgrade rehearsal, repeated-upgrade rehearsal,
  constraint/index probes, guarded-downgrade rehearsal, performed within the
  isolated production-shaped rehearsal) to BANPU-WP7. The release-evidence
  portion remains BANPU-WP8-owned;
- `NEW-MINOR-A`: `BANPU_WP1_FREEZE_RECORD.md` §7 assigns only the
  production-dialect-rehearsal portion to BANPU-WP7; the authoring portion
  is closed at BANPU-WP4 and is not reopened.

This authorization:

- binds BANPU-WP7 implementation to demonstrate exactly these two rehearsal
  portions as part of its exit evidence (§7), and to no more;
- does not treat either portion as a pre-authorization gate — both are
  implementation-time/exit-evidence obligations, consistent with how
  `MINOR-2` and `POSITION_CONVERSION_REBUILD_BOUNDARY` were treated as
  non-gating at WP6 authorization;
- does not assign, claim, or discharge the WP8 release-evidence portion of
  `MINOR-5`, or the WP4 authoring portion of `NEW-MINOR-A`; and
- does not resolve, narrow, or waive either bound portion — it remains open
  until BANPU-WP7 implementation produces the required rehearsal evidence.

`PD-3` (the emitter-locus item) is explicitly "referred out" and recorded as
"not a WP3 decision, residual, or obligation." `BANPU_WP4_ALLOCATION_RECORD.md`,
`BANPU_WP5_ALLOCATION_RECORD.md`, `BANPU_WP6_ALLOCATION_RECORD.md`, and
`BANPU_WP6_EPIC_CLOSEOUT.md` §15 each independently confirm no artifact
claims or discharges it. This authorization:

- does **not** assign `PD-3` to BANPU-WP7;
- does **not** treat it as a WP7 pre-authorization or implementation-time
  gate;
- does **not** treat it as a WP7 acceptance criterion or implementation
  obligation; and
- preserves it exactly as `UNASSIGNED / OPEN` at WP level.

## 7. Mandatory implementation boundaries and exit evidence

Implementation must preserve all Roadmap §9 and Sequence §9 acceptance,
verification, and exit criteria, and must prove:

- no flags performs no write;
- `--dry-run` performs no write;
- `--commit` is explicit and refuses any failed preflight;
- re-running the same manifest is an `already_applied` no-op;
- a conflicting manifest fails;
- the command never broadens scope to generic corporate actions;
- CLI parser and transaction-boundary tests pass;
- the dry-run database diff equals zero;
- the isolated production-shaped rehearsal covers migration, registry
  preparation, quote gate, conversion, bounded rebuild, shadow
  regeneration, and transaction rollback, including the `MINOR-5`
  rehearsal portion (real PostgreSQL upgrade, repeated upgrade,
  constraint/index probes, guarded downgrade) and the `NEW-MINOR-A`
  production-dialect-rehearsal portion (§6); and
- no public conversion endpoint exists.

No production execution, cache mutation, or production-data mutation may
occur during implementation. This is a CLI/rehearsal-level implementation
authorization only, exercised against an isolated production-shaped copy; it
grants no production execution authority. A failed verification returns work
to WP7; no later package may compensate for it.

## 8. Inherited residuals and referred items

This authorization preserves, without definition, resolution, waiver, or
reinterpretation:

- `MINOR-5` and `NEW-MINOR-A`, exactly as split and bound in §6;
- `PD-3`, exactly as treated in §6;
- BANPU-WP1 `MINOR-1`, assigned to and closed at BANPU-WP4, not reopened;
- BANPU-WP1 `MINOR-2` (WP3/WP5-owned) and `POSITION_CONVERSION_REBUILD_BOUNDARY`
  (WP5-owned), classified by `BANPU_WP5_EPIC_CLOSEOUT.md` §13–14 as
  `TECHNICALLY SATISFIED — CARRIED FORWARD; NOT DISCHARGED`, not WP7-owned
  and not assigned here;
- BANPU-WP2 residual identifiers `MINOR-A`, `MINOR-B`, and `OBSERVATION-A`,
  carried forward at BANPU-WP2 Epic Closeout, not resolved or reinterpreted;
- BANPU-WP3 `OBSERVATION-IC-1`, `OBSERVATION-IC-2`, `OBSERVATION-SR-1`, and
  `OBSERVATION-SR-2`, carried forward at BANPU-WP3 Epic Closeout as
  non-blocking; and
- BANPU-WP4's carried baseline missing-log assertion and reviewed
  temporary-path permission condition, and `B1`–`B6`, `RTO-1`–`RTO-13`,
  `PIA-1`–`PIA-4`, carried forward at BANPU-WP4 Epic Closeout unchanged.

No canonical WP1–WP6 artifact classifies any item above as a WP7
authorization-entry gate. This authority therefore neither invents an
obligation nor infers a blocker from an item's presence. Each remains a
binding unresolved condition exactly as carried, resolved only by the act
that already owns it.

## 9. Authorization granted

**BANPU-WP7 implementation is authorized**, strictly within §§3–4 and
subject to every gate and obligation in §§5–8.

This is a scoped grant of implementation authority, not implementation
itself. It grants no authority to skip an open implementation-time
obligation, change a frozen artifact, expand the production surface, treat
allocation as verification evidence, or treat this authorization as evidence
that `MINOR-5`, `NEW-MINOR-A`, or `PD-3` have been resolved.

## 10. Explicit exclusions

This act creates:

- `NO` implementation performed by this record;
- `NO` execution, dry-run, or commit of `apply_position_conversion` against
  any database, isolated or production;
- `NO` production-shaped rehearsal, migration, registry preparation,
  quote-gate action, conversion, bounded rebuild, shadow regeneration, or
  transaction rollback performed by this record;
- `NO` schema, migration, or model authority, and `NO` authority to modify
  public API routes, frontend files, or core accounting equations accepted
  in prior packages;
- `NO` public conversion endpoint or frontend authoring path;
- `NO` authority to amend, reopen, synchronize, or reinterpret the design,
  roadmap, sequence, Allocation Record, or any frozen predecessor artifact;
- `NO` authority to resolve or waive `MINOR-5`'s WP8 portion, `NEW-MINOR-A`'s
  WP4 portion, `MINOR-2`, `POSITION_CONVERSION_REBUILD_BOUNDARY`, `PD-3`, or
  any other inherited residual or referred item;
- `NO` BANPU-WP7 Work Package Plan;
- `NO` implementation review, confirmation, freeze, epic closeout, Decision
  Log synchronization, or Implementation INDEX synchronization;
- `NO` release, deployment, production execution, cache mutation, or
  production-data mutation authority of any kind;
- `NO` BANPU-WP8 or later-package allocation or implementation authority;
- `NO` M46 authority; and
- `NO` authority to stage, commit, push, merge, or publish changes.

## 11. Resulting constitutional state

- BANPU-WP1: `COMPLETE AND FROZEN`;
- BANPU-WP2: `COMPLETE AND FROZEN`;
- BANPU-WP3: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP4: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP5: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP6: `COMPLETE`, `FROZEN`, and `CLOSED`; implementation authority
  `EXHAUSTED / CLOSED`;
- BANPU-WP7 allocation: `COMPLETE — ALLOCATED`;
- BANPU-WP7 implementation authority: `AUTHORIZED — BOUNDED`;
- BANPU-WP7 implementation: `AUTHORIZED / NOT STARTED`;
- BANPU-WP7 Work Package Plan: `NOT CREATED`;
- BANPU-WP7 release, deployment, and production-mutation authority: `NONE`;
- BANPU-WP7 bound residual scope: `MINOR-5` rehearsal portion and
  `NEW-MINOR-A` production-dialect-rehearsal portion remain open,
  implementation-time obligations;
- `PD-3`: `UNASSIGNED / OPEN`, not BANPU-WP7-owned;
- BANPU-WP8 and later packages: `NOT ALLOCATED / NOT AUTHORIZED`;
- M46 authority: `NONE`; and
- frozen artifacts, Decision Log, and Implementation INDEX: unchanged.

## 12. Exact next constitutional act

Following the established BANPU authorization sequence (the BANPU-WP6
Implementation Authorization Record §12 names its own successor as "BANPU-WP6
Work Package Plan," itself following the BANPU-WP5 precedent), the exact next
constitutional act is **BANPU-WP7 Work Package Plan**.

That plan must decompose the exact authorized scope in §3–§4, carry
`MINOR-5`'s WP7 rehearsal portion and `NEW-MINOR-A`'s WP7
production-dialect-rehearsal portion unchanged as implementation-time
obligations, carry `PD-3` unchanged as unassigned/open and not WP7-owned,
place the Roadmap §9 acceptance criteria and Sequence §9 exit criteria at
their canonical implementation-time verification points, and carry all other
inherited residuals and referred items unchanged. It may not widen this
authorization.

This record creates no Work Package Plan and performs no implementation.

## 13. Repository verification

| Verification | Result |
|---|---|
| Allocation Record identity | `EXACT` — 19,609 bytes, 329 lines, SHA-256 `1aa24cd242c95039b81df1a43f061b04140ea0ed5e0a2e7405ae18945900f4f1` |
| Tracked or staged repository diff before this act | Only the additive untracked BANPU-WP7 Allocation Record; no WP7 production/test file touched |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX file modified by this act | `NONE` |
| Frozen artifact modified | `NONE` |
| No earlier BANPU-WP7 implementation-authorization artifact | `CONFIRMED` — repository search found none |
| No BANPU-WP7 Work Package Plan | `CONFIRMED` — repository search found none |
| No BANPU-WP7 implementation artifact or change | `CONFIRMED` — no file in §4.1/§4.2 exists or is modified |
| Commit created | `NO` |
