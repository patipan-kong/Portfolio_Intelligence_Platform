# BANPU-WP5 — Implementation Authorization Record

**Artifact class:** Additive constitutional authorization record
**Authorization date:** 2026-08-14
**Issuing role:** BANPU-WP5 Implementation Authorization Authority
**Authorized work package:** `BANPU-WP5 — Accounting readers and bounded reconstruction`
**Disposition:** `BANPU-WP5 IMPLEMENTATION AUTHORIZED`
**Implementation authority created:** `LIMITED — see §4, §6–§9`
**Release/deployment/production-mutation authority created:** `NONE`
**BANPU-WP6+ authority created:** `NONE`

## 1. Authorization authority and boundary

Acting solely as the distinct competent BANPU-WP5 Implementation Authorization
Authority, this act authorizes implementation of the exact work package
already allocated by
[`BANPU_WP5_ALLOCATION_RECORD.md`](BANPU_WP5_ALLOCATION_RECORD.md).

The authority exercised here is limited to verifying authorization-entry
conditions, binding implementation to the allocated scope and inherited
gates, and creating this additive record. This act does not implement code,
perform a review or confirmation, freeze implementation, authorize release,
deployment, or production-data mutation, or amend or synchronize any existing
artifact.

Allocation is a prerequisite to this act, not evidence that an
implementation-time gate has been performed. No gate is marked satisfied
merely because WP5 was allocated.

## 2. Canonical authority relied upon

This authorization relies on, and does not amend or reinterpret:

1. [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   the authoritative implementation specification, especially the
   `from_date`/`POSITION_CONVERSION_REBUILD_BOUNDARY` rebuild-refusal
   requirement, §13–14 (migration/deployment strategy, confirming bounded
   reconstruction is a WP5 implementation act while full production snapshot
   correction is a later, separately controlled deployment act), §16 test
   strategy, and the WP1 residual register;
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md)
   §7 (BANPU-WP5 purpose, scope, expected files, explicit no-change surface,
   dependencies, deliverables, acceptance criteria, and verification) and §11
   (strict dependency graph);
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md) §7
   (Step 5 preconditions, repository state, expected code changes,
   verification, and exit criteria);
4. the frozen predecessor evidence:
   [`BANPU_WP1_FREEZE_RECORD.md`](BANPU_WP1_FREEZE_RECORD.md) §7 (`MINOR-2`
   row: WP3 owns reference-price admissibility, WP5 owns mechanical
   tolerance admissibility),
   [`BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md`](BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md),
   [`BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md`](BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md)
   (finding-catalogue row: `POSITION_CONVERSION_REBUILD_BOUNDARY`, `CRITICAL`,
   predicate WP5-owned),
   [`BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP2_EPIC_CLOSEOUT.md`](BANPU_WP2_EPIC_CLOSEOUT.md),
   [`BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP3_EPIC_CLOSEOUT.md`](BANPU_WP3_EPIC_CLOSEOUT.md),
   [`BANPU_WP4_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP4_IMPLEMENTATION_CONFIRMATION.md),
   [`BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md), and
   [`BANPU_WP4_EPIC_CLOSEOUT.md`](BANPU_WP4_EPIC_CLOSEOUT.md);
5. the completed BANPU-WP4 repository synchronizations in the
   [Decision Log](../engineering/DECISION_LOG.md#banpu-wp4-decision-log-synchronization)
   and [Implementation INDEX](INDEX.md#banpu-wp4--registry-preparation-and-live-materialization); and
6. the BANPU-WP5 Allocation Record, 15,590 raw working-tree bytes, 280
   physical lines, SHA-256
   `D00D0AE886E6150F84663AA331338F764E193700EBCE944C88CB0D175CA8D687`,
   disposition `BANPU-WP5 ALLOCATED`.

Before relying on them, the design's WP5 rebuild-boundary language, the
Roadmap §7 text, and the Sequence §7 text were independently re-read from the
live working tree rather than accepted from the Allocation Record's summary
or from prompt text; all three were found to match the Allocation Record's
§3 restatement exactly. The `MINOR-2` WP1 Freeze Record row and the
`POSITION_CONVERSION_REBUILD_BOUNDARY` WP2 specification row were likewise
independently re-read and confirmed to name WP5 as the owner of the
respective open obligation. The repository was searched for any prior
BANPU-WP5 Implementation Authorization artifact and for any BANPU-WP5
reference in the Decision Log; neither exists. The design, roadmap, and
sequence remain frozen members of the BANPU-WP1 corpus; their recorded
identities and authority are relied upon as canonical and are not replaced
by a new identity convention here.

## 3. Exact authorized implementation scope

Authorization is granted exactly for `BANPU-WP5 — Accounting readers and
bounded reconstruction`, whose canonical purpose is to ensure snapshots and
return fields represent conversion and optional cash-in-lieu correctly
without touching predecessor history.

Implementation authority covers exactly these capabilities:

- classifying conversion as zero external/import/manual flow;
- including only admitted cash-in-lieu fees and realized P/L, appearing
  exactly once;
- adding the hard `from_date` conversion boundary to portfolio rebuilding,
  refusing a full or pre-boundary rebuild before any write or provider fetch;
- preserving stored pre-boundary prices and values exactly (bounded rebuild
  changes no pre-boundary numeric field);
- recognizing evidence-annotated suspension-gap return as genuine investment
  return, without "repairing" it away; and
- emitting successor asset identity in post-boundary holdings JSON.

## 4. Authorized file surface

### 4.1 Production surface

- `backend/services/portfolio_metrics.py`;
- `backend/services/portfolio_snapshots.py`;
- `backend/services/snapshot_return_recovery.py`;
- `backend/services/portfolio_rebuilder.py`, strictly bounded to the
  historical-reconstruction and return-field integration not already
  delivered by BANPU-WP2 — no other change to that file is authorized; and
- `backend/manage.py`, strictly bounded to conversion-boundary classification
  inside `verify_snapshots`, and only if that classification is required to
  satisfy this scope — no other `manage.py` change is authorized.

### 4.2 Test surface

- `backend/tests/test_portfolio_metrics.py`;
- `backend/tests/test_portfolio_metrics_parity.py`;
- `backend/tests/test_snapshot_return_recovery.py`;
- `backend/tests/test_portfolio_rebuilder.py`; and
- `backend/tests/test_verify_snapshots.py`.

No production file outside §4.1 and no test file outside §4.2 is authorized.
A different file or capability requires a distinct constitutional
authorization; it cannot be inferred from the roadmap's "expected files"
language.

## 5. Prerequisite and implementation-entry determination

| Requirement | Evidence and classification | State at authorization |
|---|---|---|
| BANPU-WP5 allocation exists | Allocation Record disposition `BANPU-WP5 ALLOCATED`; identity bound in §2 | `SATISFIED` |
| BANPU-WP2 accepted, frozen, and closed | BANPU-WP2 Implementation Freeze Record and Epic Closeout | `SATISFIED` |
| BANPU-WP3 accepted, confirmed, frozen, and closed | BANPU-WP3 Implementation Confirmation, Implementation Freeze Record, and Epic Closeout | `SATISFIED` |
| BANPU-WP4 accepted, confirmed, frozen, and closed | BANPU-WP4 Implementation Confirmation, Implementation Freeze Record, and Epic Closeout — independently re-verified this act (§2) | `SATISFIED` |
| Roadmap dependency WP2–WP4 | Roadmap §7 "Dependencies: BANPU-WP2 through BANPU-WP4 accepted" | `SATISFIED` |
| Sequence Step 5 precondition: Step 4 accepted | Sequence §7 precondition; completed WP4 lifecycle evidence above | `SATISFIED` |
| Sequence Step 5 precondition: conversion accounting stable in live and replay state | WP2 replay frozen and closed; WP4 live materialization confirmed and frozen | `SATISFIED` |
| BANPU-WP4 Decision Log synchronization | [Decision Log](../engineering/DECISION_LOG.md#banpu-wp4-decision-log-synchronization) — `BANPU-WP4 DECISION LOG SYNCHRONIZED` | `SATISFIED` |
| BANPU-WP4 Implementation INDEX synchronization | [Implementation INDEX](INDEX.md#banpu-wp4--registry-preparation-and-live-materialization) | `SATISFIED` |
| Review-frozen repository state with no overlapping implementation change | Current `git status` shows only WP4-authorized files modified/untracked (`asset_registry.py`, `portfolio_transactions.py`, `transaction_canonicalizer.py`, their tests, `test_position_conversion_live.py`) plus the additive BANPU-WP4/WP5 governance corpus; no file in the §4.1/§4.2 WP5 surface is touched | `SATISFIED` |
| No earlier BANPU-WP5 implementation authority | Repository search found no prior `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md` or equivalent artifact | `SATISFIED` |
| No conflicting authority | WP4 implementation authority exhausted/closed; WP6+, release, deployment, production-data mutation, and M46 remain unauthorized | `SATISFIED` |
| `MINOR-2` WP5 half (mechanical NAV continuity tolerance admissibility) | Pre-use implementation-time gate, not a pre-authorization gate — see §6 | `OPEN — IMPLEMENTATION-TIME` |
| `POSITION_CONVERSION_REBUILD_BOUNDARY` predicate | Pre-use implementation-time gate, not a pre-authorization gate — see §7 | `OPEN — IMPLEMENTATION-TIME` |

All authorization-entry prerequisites are satisfied. Open implementation-time
conditions remain open and are not satisfied, waived, or bypassed by this
act.

## 6. Treatment of BANPU-WP1 `MINOR-2` (WP5 half)

`MINOR-2` records deferred consumer-domain validation split across two
owners: WP3 for reference-price admissibility (already discharged under
WP3's closed implementation authority) and WP5 for mechanical NAV continuity
tolerance admissibility. Its canonical verification point, per the WP1
Freeze Record §7 row, is **focused rejection tests before the tolerance
value is consumed**.

It is therefore:

- not a pre-authorization gate;
- a mandatory implementation-time pre-use gate, to be satisfied before any
  mechanical continuity-tolerance value is consumed by the bounded rebuild
  or snapshot-verification path authorized in §3–§4;
- an exit/confirmation evidence obligation requiring focused tests proving
  an inadmissible tolerance value is rejected before use; and
- not resolved, narrowed, or waived by this authorization.

WP5 may not treat a continuity-tolerance value as trusted input. WP5 may not
be confirmed, frozen, or closed without the required rejection-test
evidence.

## 7. Treatment of `POSITION_CONVERSION_REBUILD_BOUNDARY`

This finding, catalogued as `CRITICAL` by the BANPU-WP2 Implementation
Specification, records that an ordinary portfolio rebuild must refuse a
full or pre-boundary reconstruction rather than silently re-fetching or
repricing predecessor history. Its predicate is recorded there as WP5-owned
and, per the design's rebuild-boundary requirement and the Roadmap §7
acceptance criteria, is the central acceptance gate of this work package.

It is therefore:

- not a pre-authorization gate;
- the mandatory implementation-time gate requiring: (a) refusal of a full or
  pre-boundary rebuild before any write or unsafe provider fetch, and (b)
  bounded reconstruction from the transition date that changes no
  pre-boundary numeric field, proven by hash/field comparison of
  pre-boundary fixtures; and
- not discharged, narrowed, or waived by this authorization.

## 8. Inherited residuals and referred items

This authorization preserves, without definition, resolution, waiver, or
reinterpretation:

- BANPU-WP1 `MINOR-1` and `NEW-MINOR-A`, assigned to and carried forward
  by the closed BANPU-WP4 Epic Closeout;
- BANPU-WP1 `MINOR-5`, whose remaining ownership stays with BANPU-WP7
  rehearsal and BANPU-WP8 release evidence;
- BANPU-WP2 residual identifiers `MINOR-A`, `MINOR-B`, and `OBSERVATION-A`
  through `OBSERVATION-E`, inherited by WP5 through WP8 unchanged;
- WP3 residual R6, the WP3-scoped R7 formal waiver (creating no relief or
  precedent for WP5), and WP3's non-blocking closeout observations;
- BANPU-WP4's carried baseline missing-log assertion and reviewed
  temporary-path permission condition, and B1–B6, RTO-1 through RTO-13,
  PIA-1 through PIA-4, `MINOR-1`, and `NEW-MINOR-A` exactly as classified by
  the BANPU-WP4 Third Renewed Independent Implementation Review,
  Implementation Confirmation, Implementation Freeze Record, and Epic
  Closeout; and
- the emitter-locus item referred out by WP3 PD-3 to the authority governing
  the canonical design, roadmap, and package inventory.

No canonical WP1–WP4 artifact classifies any item above as a WP5
authorization-entry gate. This authority therefore neither invents an
obligation nor infers a blocker from an item's presence. Each remains a
binding unresolved condition exactly as carried, resolved only by the act
that already owns it.

## 9. Mandatory implementation boundaries and exit evidence

Implementation must preserve all Roadmap §7 and Sequence §7 acceptance and
exit criteria and must prove:

- conversion never appears as an external cash flow, import, or quantity
  correction;
- cash-in-lieu fees and realized P/L appear exactly once;
- a full or pre-boundary rebuild fails before any write or unsafe provider
  fetch;
- a bounded rebuild changes no pre-boundary numeric field, demonstrated by
  hash/field comparison of pre-boundary fixtures;
- genuine annotated suspension-period return remains investment return, not
  "repaired" away;
- predecessor history cannot be re-fetched by an ordinary rebuild; and
- metrics-parity, snapshot-recovery, coverage, return-decomposition,
  price-matrix, rebuild, and snapshot-verification suites pass together.

No production snapshot rebuild, repair, repricing, cache purge, or
production shadow rewrite may occur during implementation. This is a
development/test-fixture-level implementation authorization only; it grants
no production execution authority. A failed verification returns work to
WP5; no later package may compensate for it.

## 10. Authorization granted

**BANPU-WP5 implementation is authorized**, strictly within §§3–4 and
subject to every gate and obligation in §§5–9.

This is a scoped grant of implementation authority, not implementation
itself. It grants no authority to skip an open implementation-time gate,
change a frozen artifact, expand the production surface, or treat
allocation as verification evidence.

## 11. Explicit exclusions

This act creates:

- `NO` implementation performed by this record;
- `NO` schema, migration, or model authority, and `NO` authority to modify
  `backend/models/asset.py`, `backend/models/database.py`,
  `backend/services/ledger_repair.py`, `backend/main.py` endpoints, or any
  frontend file;
- `NO` public endpoint, operator CLI, frontend authoring path, general
  corporate-action framework, or `LedgerRepair` conversion behavior;
- `NO` authority to amend, reopen, synchronize, or reinterpret the design,
  roadmap, sequence, Allocation Record, or any frozen predecessor artifact;
- `NO` authority to resolve or waive `MINOR-2`'s WP5 half, the
  `POSITION_CONVERSION_REBUILD_BOUNDARY` predicate, or any other inherited
  residual or referred item;
- `NO` implementation review, confirmation, freeze, epic closeout, Decision
  Log synchronization, or Implementation INDEX synchronization;
- `NO` release, deployment, production execution, cache mutation, snapshot
  reconstruction, or production-data mutation authority of any kind — this
  act performs and authorizes no snapshot mutation;
- `NO` BANPU-WP6 or later-package allocation or implementation authority;
- `NO` M46 authority; and
- `NO` authority to stage, commit, push, merge, or publish changes.

## 12. Authorization disposition

**`BANPU-WP5 IMPLEMENTATION AUTHORIZED`**

Authorization is bound to the Allocation Record identity in §2 and the exact
scope and conditions in this record. `MINOR-2`'s WP5 half, the
`POSITION_CONVERSION_REBUILD_BOUNDARY` predicate, and all other inherited
residuals and referred items remain in the states recorded above. No
implementation has begun under this act.

## 13. Resulting constitutional state

- BANPU-WP1: `COMPLETE AND FROZEN`;
- BANPU-WP2: `COMPLETE AND FROZEN`;
- BANPU-WP3: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP4: `COMPLETE`, `FROZEN`, and `CLOSED`; implementation authority
  `EXHAUSTED / CLOSED`;
- BANPU-WP5 allocation: `COMPLETE — ALLOCATED`;
- BANPU-WP5 implementation authority: `AUTHORIZED — BOUNDED`;
- BANPU-WP5 implementation: `AUTHORIZED / NOT STARTED`;
- BANPU-WP5 release, deployment, and production-mutation authority: `NONE`;
- BANPU-WP6 and later packages: `NOT ALLOCATED / NOT AUTHORIZED`;
- M46 authority: `NONE`; and
- frozen artifacts, Decision Log, and Implementation INDEX: unchanged.

## 14. Exact next constitutional act

Following the established BANPU authorization sequence (BANPU-WP4's
Authorization Record §14 names its own successor as "BANPU-WP4 Work Package
Plan"), the exact next constitutional act is **BANPU-WP5 Work Package
Plan**.

That plan must decompose the exact authorized scope in §3–§4, place
`MINOR-2`'s WP5 half and the `POSITION_CONVERSION_REBUILD_BOUNDARY`
predicate at their canonical implementation-time verification points, and
carry all inherited residuals and referred items unchanged. It may not
widen this authorization.

This record creates no Work Package Plan and performs no implementation.

## 15. Repository verification

| Verification | Result |
|---|---|
| Allocation Record identity | `EXACT` — 15,590 bytes, 280 lines, SHA-256 `D00D0AE886E6150F84663AA331338F764E193700EBCE944C88CB0D175CA8D687` |
| BANPU-WP4 frozen implementation corpus (six files, canonical LF) | `EXACT` against `BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md` §F.2/§F.3, re-verified this act |
| Tracked or staged repository diff before this act | Only pre-existing WP4-authorized modifications/untracked files and the additive BANPU-WP4/WP5 governance corpus; no WP5 production/test file touched |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX file modified by this act | `NONE` |
| Frozen artifact modified | `NONE` |
| No earlier BANPU-WP5 implementation-authorization artifact | `CONFIRMED` — repository search found none |
| Trailing-whitespace verification | see final report |
| Markdown relative-link target verification | see final report |
| Markdown fragment-heading verification | see final report |
| `git diff --check` | see final report |
| `git diff --cached --check` | see final report |
| `graphify update .` | see final report |
| Final `git status --short --untracked-files=all` | see final report |
| Commit created | `NO` |
