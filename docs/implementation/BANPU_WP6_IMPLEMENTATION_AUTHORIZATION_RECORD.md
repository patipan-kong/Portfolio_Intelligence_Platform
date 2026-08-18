# BANPU-WP6 — Implementation Authorization Record

**Artifact class:** Additive constitutional authorization record
**Authorization date:** 2026-08-17
**Issuing role:** BANPU-WP6 Implementation Authorization Authority
**Authorized work package:** `BANPU-WP6 — Shadow and succession-aware time-series continuity`
**Disposition:** `BANPU-WP6 IMPLEMENTATION AUTHORIZED`
**Implementation authority created:** `LIMITED — see §4, §6–§9`
**Release/deployment/production-mutation authority created:** `NONE`
**BANPU-WP7+ authority created:** `NONE`

## 1. Authorization authority and boundary

Acting solely as the distinct competent BANPU-WP6 Implementation Authorization
Authority, this act authorizes implementation of the exact work package
already allocated by
[`BANPU_WP6_ALLOCATION_RECORD.md`](BANPU_WP6_ALLOCATION_RECORD.md).

The authority exercised here is limited to verifying authorization-entry
conditions, binding implementation to the allocated scope and inherited
gates, and creating this additive record. This act does not implement code,
perform a review or confirmation, freeze implementation, authorize release,
deployment, or production-data mutation, create a Work Package Plan, or
amend or synchronize any existing artifact.

Allocation is a prerequisite to this act, not evidence that an
implementation-time gate has been performed. No gate is marked satisfied
merely because WP6 was allocated. This authority is distinct from, and does
not include, the allocation authority already exercised by the Allocation
Record, any implementation authority exercised later under a Work Package
Plan this act does not create, and any release, deployment, or production
authority, which remains wholly unestablished by this act.

## 2. Canonical authority relied upon

This authorization relies on, and does not amend or reinterpret:

1. [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   the authoritative implementation specification, especially §12 ("Derived
   accounting and identity continuity" — the succession-aware `MERGED_INTO`
   lookup, non-null predecessor/successor asset ID carry, shadow conversion
   of replay-time working holdings, fractional paper-share preservation
   without broker cash-in-lieu, inception-value conservation, and
   boundary-limited regeneration) and §13–14 (migration/deployment strategy,
   confirming shadow/snapshot regeneration from the transition date is a
   later, separately controlled production act, not part of this
   authorization);
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md)
   §8 (BANPU-WP6 purpose, scope, expected files, explicit no-change surface,
   dependencies, deliverables, acceptance criteria, verification, and size
   estimates) and §11 (strict dependency graph);
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md) §8
   (Step 6 preconditions, repository state, expected code changes,
   verification, and exit criteria);
4. the frozen predecessor evidence:
   [`BANPU_WP1_FREEZE_RECORD.md`](BANPU_WP1_FREEZE_RECORD.md) §7 (`MINOR-2`
   row: WP3/WP5 ownership; no WP6 row),
   [`BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md`](BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md)
   (finding catalogue: `POSITION_CONVERSION_REBUILD_BOUNDARY` is WP5-owned,
   not WP6-owned),
   [`BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP3_EPIC_CLOSEOUT.md`](BANPU_WP3_EPIC_CLOSEOUT.md),
   [`BANPU_WP4_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP4_IMPLEMENTATION_CONFIRMATION.md),
   [`BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP4_EPIC_CLOSEOUT.md`](BANPU_WP4_EPIC_CLOSEOUT.md),
   [`BANPU_WP5_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP5_IMPLEMENTATION_CONFIRMATION.md),
   [`BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md), and
   [`BANPU_WP5_EPIC_CLOSEOUT.md`](BANPU_WP5_EPIC_CLOSEOUT.md);
5. the completed BANPU-WP5 repository synchronizations in the
   [Decision Log](../engineering/DECISION_LOG.md#banpu-wp5-decision-log-synchronization)
   and [Implementation INDEX](INDEX.md#banpu-wp5--accounting-readers-and-bounded-reconstruction); and
6. the BANPU-WP6 Allocation Record, 16,307 raw working-tree bytes, 282
   physical lines, SHA-256
   `208c2b236d669141bc947a96d82c5c249535e95eb54483c25496c1b6908d9d58`,
   disposition `BANPU-WP6 ALLOCATED`.

Before relying on them, the design's §12–14 text, the Roadmap §8 text, and
the Sequence §8 text were independently re-read from the live working tree
rather than accepted from the Allocation Record's summary or from prompt
text; all three were found to match the Allocation Record's §2–§3
restatement exactly. `BANPU_WP1_FREEZE_RECORD.md` was searched for a WP6 row
in its residual-ownership register and none exists; the WP1/WP2 residual and
finding-catalogue evidence cited in §2.4 confirms `MINOR-2` and
`POSITION_CONVERSION_REBUILD_BOUNDARY` are WP3/WP5-owned, not WP6-owned. The
Decision Log and Implementation INDEX were independently re-read and
confirmed to record BANPU-WP3, BANPU-WP4, and BANPU-WP5 each as `COMPLETE`,
`FROZEN`, and `CLOSED` (Implementation INDEX lines 220, 240, and 260), with
no BANPU-WP6 entry present in either file. The repository was searched for
any prior BANPU-WP6 Implementation Authorization artifact, any BANPU-WP6
Work Package Plan, and any BANPU-WP6 implementation artifact; none exists.
Current `git status --porcelain=v1` shows only the single untracked
Allocation Record file from the prior act; nothing is staged. The design,
roadmap, and sequence remain frozen members of the BANPU-WP1 corpus; their
recorded identities and authority are relied upon as canonical and are not
replaced by a new identity convention here.

## 3. Exact authorized implementation scope

Authorization is granted exactly for `BANPU-WP6 — Shadow and
succession-aware time-series continuity`, whose canonical purpose is to
prevent the identity transition from splitting derived portfolio, shadow,
attribution, and evaluation series.

Implementation authority covers exactly these capabilities:

- adding a narrow effective-dated succession lookup using `MERGED_INTO`;
- carrying non-null asset IDs in affected holdings JSON;
- applying conversion to replay-time shadow holdings on the boundary;
- keeping paper fractional shares, without applying broker cash-in-lieu
  treatment to hypothetical portfolios;
- normalizing post-boundary valuation subjects while preserving immutable
  source evidence; and
- restricting persisted regeneration to on/after the boundary.

## 4. Authorized file surface

### 4.1 Production surface

- a new narrow service such as `backend/services/position_conversion.py`,
  only if strictly needed for pure succession/conversion helpers — no other
  new production file is authorized;
- `backend/services/decision_memory/shadow_tracker.py`;
- `backend/services/decision_memory/attribution.py`;
- `backend/services/analytics/quant_engine.py`;
- `backend/services/evaluation/horizon_grader.py`; and
- `backend/services/evaluation/ideal_series.py`.

### 4.2 Test surface

- `backend/tests/test_shadow_regeneration.py`;
- `backend/tests/test_horizon_grader.py`;
- `backend/tests/test_ideal_series.py`; and
- other corresponding focused tests strictly bounded to the capabilities in
  §3, for the files listed in §4.1.

No production file outside §4.1 and no test file outside §4.2 is authorized.
A different file or capability requires a distinct constitutional
authorization; it cannot be inferred from the roadmap's "expected files"
language.

## 5. Prerequisite and implementation-entry determination

| Requirement | Evidence and classification | State at authorization |
|---|---|---|
| BANPU-WP6 allocation exists | Allocation Record disposition `BANPU-WP6 ALLOCATED`; identity bound in §2 | `SATISFIED` |
| BANPU-WP3 accepted, confirmed, frozen, and closed | Implementation INDEX line 220: `BANPU-WP3 is COMPLETE, FROZEN, and CLOSED` | `SATISFIED` |
| BANPU-WP4 accepted, confirmed, frozen, and closed | Implementation INDEX line 240: `BANPU-WP4 is COMPLETE, FROZEN, and CLOSED` | `SATISFIED` |
| BANPU-WP5 accepted, confirmed, frozen, and closed | Implementation INDEX line 260: `BANPU-WP5 is COMPLETE, FROZEN, and CLOSED` — independently re-verified this act (§2) | `SATISFIED` |
| Roadmap dependency WP3–WP5 | Roadmap §8 "Dependencies: BANPU-WP3 through BANPU-WP5 accepted" | `SATISFIED` |
| Sequence Step 6 precondition: Step 5 accepted | Sequence §8 precondition; completed WP5 lifecycle evidence above | `SATISFIED` |
| Sequence Step 6 precondition: portfolio snapshots expose correct effective-dated identities and prices | Sequence §8 repository-state line: "Real portfolio accounting is complete."; WP5 accounting-reader classification and rebuild boundary confirmed and frozen | `SATISFIED` |
| BANPU-WP5 Decision Log synchronization | [Decision Log](../engineering/DECISION_LOG.md#banpu-wp5-decision-log-synchronization) — `BANPU-WP5 DECISION LOG SYNCHRONIZED` | `SATISFIED` |
| BANPU-WP5 Implementation INDEX synchronization | [Implementation INDEX](INDEX.md#banpu-wp5--accounting-readers-and-bounded-reconstruction) — BANPU-WP5 row records `COMPLETE`, `FROZEN`, `CLOSED` | `SATISFIED` |
| Review-frozen repository state with no overlapping implementation change | Current `git status --porcelain=v1` shows only the untracked BANPU-WP6 Allocation Record; no file in the §4.1/§4.2 WP6 surface is touched | `SATISFIED` |
| No earlier BANPU-WP6 implementation authority | Repository search found no prior `BANPU_WP6_IMPLEMENTATION_AUTHORIZATION_RECORD.md` or equivalent artifact | `SATISFIED` |
| No conflicting authority | WP5 implementation authority exhausted/closed; WP7+, release, deployment, production-data mutation, and M46 remain unauthorized | `SATISFIED` |
| No WP6-specific pre-authorization residual gate | `BANPU_WP1_FREEZE_RECORD.md` §7 residual-ownership register contains no WP6 row; `MINOR-2` and `POSITION_CONVERSION_REBUILD_BOUNDARY` remain WP3/WP5-owned, not WP6-owned — see §6 | `NOT APPLICABLE` |
| Roadmap §8 acceptance criteria / Sequence §8 exit criteria | Pre-use implementation-time and exit-evidence obligations, not pre-authorization gates — see §7 | `OPEN — IMPLEMENTATION-TIME` |

All authorization-entry prerequisites are satisfied. Open implementation-time
conditions remain open and are not satisfied, waived, or bypassed by this
act.

## 6. Treatment of `MINOR-2` and `POSITION_CONVERSION_REBUILD_BOUNDARY`

Neither `MINOR-2` (WP5 half) nor `POSITION_CONVERSION_REBUILD_BOUNDARY` is
assigned to BANPU-WP6 by any canonical artifact read for this act.
`BANPU_WP1_FREEZE_RECORD.md` §7 names WP3 and WP5 as the sole owners of
`MINOR-2`; `BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md` names WP5 as the sole
owner of the `POSITION_CONVERSION_REBUILD_BOUNDARY` predicate.
`BANPU_WP5_EPIC_CLOSEOUT.md` §13–14 classifies both, under WP5's ownership,
exactly as `TECHNICALLY SATISFIED — CARRIED FORWARD; NOT DISCHARGED BY THIS
CLOSEOUT`.

This authorization:

- does not assign either item to BANPU-WP6;
- does not treat either item as a WP6 pre-authorization or
  implementation-time gate;
- does not resolve, narrow, discharge, or waive either item; and
- preserves both exactly in the state carried forward by the WP5 Epic
  Closeout, under their existing WP3/WP5 ownership.

## 7. Mandatory implementation boundaries and exit evidence

Implementation must preserve all Roadmap §8 and Sequence §8 acceptance and
exit criteria and must prove:

- a pre-boundary predecessor holding becomes the successor on the correct
  shadow valuation date;
- shadow inception value is conserved mechanically;
- pre-boundary shadow rows remain unchanged;
- recommendations retain original evidence while post-boundary evaluation
  follows the successor;
- no unrelated symbol is remapped;
- no general corporate-action dispatcher or event vocabulary is introduced;
- historical recommendation and optimizer payloads remain unchanged; and
- every identified derived consumer (shadow, attribution, quant, horizon,
  ideal-series) maintains successor continuity without silent divergence or
  inception-evidence rewriting.

No production snapshot rebuild, repair, repricing, cache purge, or
production shadow rewrite may occur during implementation. This is a
development/test-fixture-level implementation authorization only; it grants
no production execution authority. A failed verification returns work to
WP6; no later package may compensate for it.

## 8. Inherited residuals and referred items

This authorization preserves, without definition, resolution, waiver, or
reinterpretation:

- BANPU-WP1 `MINOR-2` (WP3/WP5-owned) and `POSITION_CONVERSION_REBUILD_BOUNDARY`
  (WP5-owned), exactly as treated in §6;
- BANPU-WP1 `MINOR-1` and `NEW-MINOR-A`, assigned to and carried forward by
  the closed BANPU-WP4 Epic Closeout;
- BANPU-WP1 `MINOR-5`, whose remaining ownership stays with BANPU-WP7
  rehearsal and BANPU-WP8 release evidence;
- BANPU-WP2 residual identifiers `MINOR-A`, `MINOR-B`, and `OBSERVATION-A`,
  carried forward at BANPU-WP2 Epic Closeout, not resolved or reinterpreted;
- BANPU-WP3 `OBSERVATION-IC-1`, `OBSERVATION-IC-2`, `OBSERVATION-SR-1`, and
  `OBSERVATION-SR-2`, carried forward at BANPU-WP3 Epic Closeout as
  non-blocking;
- the `PD-3` emitter-locus item, referred out and recorded by
  `BANPU_WP5_EPIC_CLOSEOUT.md` §15 as unassigned and open; this authorization
  does not claim or assign it to BANPU-WP6; and
- BANPU-WP4's carried baseline missing-log assertion and reviewed
  temporary-path permission condition, and `B1`–`B6`, `RTO-1`–`RTO-13`,
  `PIA-1`–`PIA-4`, carried forward at BANPU-WP4 Epic Closeout unchanged.

No canonical WP1–WP5 artifact classifies any item above as a WP6
authorization-entry gate. This authority therefore neither invents an
obligation nor infers a blocker from an item's presence. Each remains a
binding unresolved condition exactly as carried, resolved only by the act
that already owns it.

## 9. Authorization granted

**BANPU-WP6 implementation is authorized**, strictly within §§3–4 and
subject to every gate and obligation in §§5–8.

This is a scoped grant of implementation authority, not implementation
itself. It grants no authority to skip an open implementation-time
obligation, change a frozen artifact, expand the production surface, or
treat allocation as verification evidence.

## 10. Explicit exclusions

This act creates:

- `NO` implementation performed by this record;
- `NO` schema, migration, or model authority, and `NO` authority to modify
  `RecommendationSnapshot`, `OptimizerHistory`, `UserExecutionDecision`, or
  `RecommendationGrade` schema, historical recommendation or decision
  payloads, the transaction schema or write path, or any frontend file;
- `NO` public endpoint, operator CLI, frontend authoring path, general
  asset-definition vocabulary expansion, or general corporate-action
  dispatcher or event vocabulary;
- `NO` unrelated-symbol remapping;
- `NO` authority to amend, reopen, synchronize, or reinterpret the design,
  roadmap, sequence, Allocation Record, or any frozen predecessor artifact;
- `NO` authority to resolve or waive `MINOR-2`, the
  `POSITION_CONVERSION_REBUILD_BOUNDARY` predicate, or any other inherited
  residual or referred item;
- `NO` BANPU-WP6 Work Package Plan;
- `NO` implementation review, confirmation, freeze, epic closeout, Decision
  Log synchronization, or Implementation INDEX synchronization;
- `NO` release, deployment, production execution, cache mutation, snapshot
  or shadow reconstruction, or production-data mutation authority of any
  kind — this act performs and authorizes no snapshot or shadow mutation;
- `NO` BANPU-WP7 or later-package allocation or implementation authority;
- `NO` M46 authority; and
- `NO` authority to stage, commit, push, merge, or publish changes.

## 11. Resulting constitutional state

- BANPU-WP1: `COMPLETE AND FROZEN`;
- BANPU-WP2: `COMPLETE AND FROZEN`;
- BANPU-WP3: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP4: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP5: `COMPLETE`, `FROZEN`, and `CLOSED`; implementation authority
  `EXHAUSTED / CLOSED`;
- BANPU-WP6 allocation: `COMPLETE — ALLOCATED`;
- BANPU-WP6 implementation authority: `AUTHORIZED — BOUNDED`;
- BANPU-WP6 implementation: `AUTHORIZED / NOT STARTED`;
- BANPU-WP6 Work Package Plan: `NOT CREATED`;
- BANPU-WP6 release, deployment, and production-mutation authority: `NONE`;
- BANPU-WP7 and later packages: `NOT ALLOCATED / NOT AUTHORIZED`;
- M46 authority: `NONE`; and
- frozen artifacts, Decision Log, and Implementation INDEX: unchanged.

## 12. Exact next constitutional act

Following the established BANPU authorization sequence (the BANPU-WP5
Implementation Authorization Record §14 names its own successor as "BANPU-WP5
Work Package Plan"), the exact next constitutional act is **BANPU-WP6 Work
Package Plan**.

That plan must decompose the exact authorized scope in §3–§4, carry
`MINOR-2` and the `POSITION_CONVERSION_REBUILD_BOUNDARY` predicate unchanged
under their existing WP3/WP5 ownership, place the Roadmap §8 acceptance
criteria and Sequence §8 exit criteria at their canonical implementation-time
verification points, and carry all other inherited residuals and referred
items unchanged. It may not widen this authorization.

This record creates no Work Package Plan and performs no implementation.

## 13. Repository verification

| Verification | Result |
|---|---|
| Allocation Record identity | `EXACT` — 16,307 bytes, 282 lines, SHA-256 `208c2b236d669141bc947a96d82c5c249535e95eb54483c25496c1b6908d9d58` |
| Tracked or staged repository diff before this act | Only the additive untracked BANPU-WP6 Allocation Record; no WP6 production/test file touched |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX file modified by this act | `NONE` |
| Frozen artifact modified | `NONE` |
| No earlier BANPU-WP6 implementation-authorization artifact | `CONFIRMED` — repository search found none |
| No BANPU-WP6 Work Package Plan | `CONFIRMED` — repository search found none |
| No BANPU-WP6 implementation artifact or change | `CONFIRMED` — no file in §4.1/§4.2 exists or is modified |
| `git diff --check` | see final report |
| `git diff --cached --check` | see final report |
| `graphify update .` | see final report |
| Final `git status --porcelain=v1` | see final report |
| Commit created | `NO` |
