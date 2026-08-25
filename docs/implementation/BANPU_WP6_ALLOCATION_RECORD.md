# BANPU-WP6 — Allocation Record

**Artifact class:** Additive constitutional allocation record
**Allocation date:** 2026-08-17
**Issuing role:** BANPU-WP6 Allocation Authority
**Allocated work package:** `BANPU-WP6 — Shadow and succession-aware time-series continuity`
**Disposition:** `BANPU-WP6 ALLOCATED`
**Implementation authority created:** `NONE`
**Release authority created:** `NONE`
**BANPU-WP7+ authority created:** `NONE`

## 1. Allocation authority and constitutional boundary

Acting solely as the competent BANPU-WP6 Allocation Authority, this act
allocates the work package already defined by the canonical BANPU planning and
governance corpus. The authority exercised here is limited to:

- verifying the predecessor and dependency gates against current canonical
  repository evidence;
- binding the exact existing BANPU-WP6 scope and its inherited conditions to
  this allocation; and
- creating this additive Allocation Record.

This allocation does not create planning-amendment, implementation,
implementation-authorization, release, deployment, production-data mutation,
successor-allocation, or repository-synchronization authority. It does not
change, interpret, or supersede any frozen artifact. No proposition below is
asserted unless it is drawn from the live text of a cited artifact; where the
corpus does not explicitly establish something, that absence is stated rather
than filled by inference.

## 2. Canonical authority relied upon

This allocation relies on the following existing authority, in descending
order of scope:

1. [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   the approved and authoritative implementation specification, especially
   §12 ("Derived accounting and identity continuity" — the succession-aware
   `MERGED_INTO` lookup, non-null predecessor/successor asset ID carry,
   shadow conversion of replay-time working holdings, fractional paper-share
   preservation without broker cash-in-lieu, inception-value conservation,
   and boundary-limited regeneration) and §13–14 (migration/deployment
   strategy, confirming shadow/snapshot regeneration from the transition
   date is a later, separately controlled production act, step 13);
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md),
   especially §1 (universal package rules), §2 (package inventory), §8
   (BANPU-WP6), and §11 (strict dependency graph);
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md),
   especially §1 (strict serial sequence) and §8 (Step 6 preconditions,
   repository state, expected changes, verification, and exit criteria);
4. the completed and frozen predecessor records:
   [`BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP3_EPIC_CLOSEOUT.md`](BANPU_WP3_EPIC_CLOSEOUT.md),
   [`BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP4_EPIC_CLOSEOUT.md`](BANPU_WP4_EPIC_CLOSEOUT.md),
   [`BANPU_WP5_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP5_IMPLEMENTATION_CONFIRMATION.md),
   [`BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md), and
   [`BANPU_WP5_EPIC_CLOSEOUT.md`](BANPU_WP5_EPIC_CLOSEOUT.md); and
5. the completed BANPU-WP5 repository synchronizations in the
   [Decision Log](../engineering/DECISION_LOG.md#banpu-wp5-decision-log-synchronization)
   and [Implementation INDEX](INDEX.md#banpu-wp5--accounting-readers-and-bounded-reconstruction).

The design, roadmap, and sequence are frozen members of the BANPU-WP1 corpus
recorded by the BANPU-WP1 Freeze Record §4. This act relies on their canonical
recorded authority and current repository presence; it does not restate or
replace their frozen identities.

Before relying on it, the BANPU-WP5 terminal state was independently re-read
against live repository bytes rather than accepted from prompt text alone.
`BANPU_WP5_EPIC_CLOSEOUT.md` §22 reads exactly `BANPU-WP5 EPIC CLOSEOUT
COMPLETE`, and its §8/§21 already record an independent byte-level
recomputation of the nine-member frozen implementation corpus against the
canonical-LF aggregate `8646BEE6C08C92F938F5B8B530039F032CDAA9A92E803E4A847DB661B960AC0D`
with zero drift; this act relies on that already-performed recomputation
rather than duplicating it. The Decision Log's `BANPU-WP5 Decision Log
Synchronization` entry and the Implementation INDEX's BANPU-WP5 row were
independently read and found mutually consistent: both record BANPU-WP5 as
`COMPLETE`, `FROZEN`, and `CLOSED`, and the Implementation INDEX additionally
states in terms specific to WP6 that "WP6's Decision Log and Implementation
INDEX entry prerequisites are both now satisfied; WP6 remains `NOT ALLOCATED`
and `NOT AUTHORIZED`." BANPU-WP3 and BANPU-WP4 were independently re-read and
each confirmed `COMPLETE`, `FROZEN`, and `CLOSED` in both the Decision Log and
the Implementation INDEX. A repository-wide search for `BANPU_WP6_*` found no
prior artifact of any kind.

## 3. Exact allocated scope

The allocation is exactly `BANPU-WP6 — Shadow and succession-aware
time-series continuity`, with this canonical purpose: prevent the identity
transition from splitting derived portfolio, shadow, attribution, and
evaluation series.

The allocated scope is exactly:

- add a narrow effective-dated succession lookup using `MERGED_INTO`;
- carry non-null asset IDs in affected holdings JSON;
- apply conversion to replay-time shadow holdings on the boundary;
- keep paper fractional shares; do not apply broker cash-in-lieu to
  hypothetical portfolios;
- normalize post-boundary valuation subjects while preserving immutable
  source evidence; and
- restrict persisted regeneration to on/after the boundary.

The canonical expected implementation surface, recorded here as scope
evidence and not as implementation authority, is:

- a new narrow service such as `backend/services/position_conversion.py`
  only if needed for pure succession/conversion helpers;
- `backend/services/decision_memory/shadow_tracker.py`;
- `backend/services/decision_memory/attribution.py`;
- `backend/services/analytics/quant_engine.py`;
- `backend/services/evaluation/horizon_grader.py`;
- `backend/services/evaluation/ideal_series.py`; and
- corresponding focused tests, especially `test_shadow_regeneration.py`,
  `test_horizon_grader.py`, and `test_ideal_series.py`.

The Roadmap §8 explicit no-change surface remains binding as scope evidence:
`RecommendationSnapshot`, `OptimizerHistory`, `UserExecutionDecision`, and
`RecommendationGrade` schema; historical recommendation or decision payloads;
transaction schema or write path; general asset-definition vocabulary; and
all M46 files. The Roadmap §8 acceptance criteria additionally bind that no
general corporate-action dispatcher or event vocabulary is introduced and no
unrelated symbol is remapped.

Allocation does not change, narrow, widen, or implement this scope.

## 4. Prerequisite and gate determination

| Requirement | Canonical evidence | Determination |
|---|---|---|
| BANPU-WP3 accepted, confirmed, frozen, and closed | `BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP3_EPIC_CLOSEOUT.md`; Implementation INDEX line 220 reads `BANPU-WP3 is COMPLETE, FROZEN, and CLOSED` | `SATISFIED` |
| BANPU-WP4 accepted, confirmed, frozen, and closed | `BANPU_WP4_IMPLEMENTATION_CONFIRMATION.md`, `BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP4_EPIC_CLOSEOUT.md`; Implementation INDEX §"BANPU-WP4" table | `SATISFIED` |
| BANPU-WP5 accepted, confirmed, frozen, and closed | `BANPU_WP5_IMPLEMENTATION_CONFIRMATION.md`, `BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP5_EPIC_CLOSEOUT.md` §22 — re-read in §2 above | `SATISFIED` |
| Roadmap dependency `BANPU-WP3–WP5` | Roadmap §2 line 29 and §8 | `SATISFIED` |
| Sequence Step 6 precondition: Step 5 accepted | Sequence §8 precondition; completed WP5 lifecycle evidence in §2 above | `SATISFIED` |
| Sequence Step 6 precondition: portfolio snapshots expose correct effective-dated identities and prices | WP5 accounting-reader classification and rebuild boundary are confirmed and frozen (WP5 Closeout §11, Roadmap/Sequence scope items `PASS`) | `SATISFIED` |
| BANPU-WP5 Decision Log synchronization | [Decision Log](../engineering/DECISION_LOG.md#banpu-wp5-decision-log-synchronization) — `BANPU-WP5 DECISION LOG SYNCHRONIZED` | `SATISFIED` |
| BANPU-WP5 Implementation INDEX synchronization | [Implementation INDEX](INDEX.md#banpu-wp5--accounting-readers-and-bounded-reconstruction) — BANPU-WP5 row records `COMPLETE`, `FROZEN`, `CLOSED`; text states WP6's Decision Log and Implementation INDEX entry prerequisites are both satisfied | `SATISFIED` |
| Prior BANPU-WP6 allocation absent | Repository search found no `BANPU_WP6_*` or equivalent artifact existing before this act | `SATISFIED` |

BANPU-WP5 completion, confirmation, freeze, and both repository
synchronizations therefore satisfy the immediate-predecessor requirement. The
constitutional prerequisites for allocation are satisfied.

Entry-prerequisite satisfaction is distinct from allocation, and allocation is
distinct from Implementation Authorization. This act performs only
allocation; it does not treat WP5's authority, or the mere existence of the
satisfied entry prerequisite recorded by the Decision Log and Implementation
INDEX, as automatically flowing into WP6 authorization or implementation.

## 5. Residuals and inherited conditions

Allocation resolves, defines, weakens, reinterprets, or waives none of the
following. No canonical artifact read for this act assigns `MINOR-2` or
`POSITION_CONVERSION_REBUILD_BOUNDARY` to BANPU-WP6; both remain WP5-owned
obligations, carried forward undischarged by the WP5 Epic Closeout, and are
recorded here without reassignment:

- BANPU-WP1 `MINOR-2`, WP5 half (mechanical NAV continuity tolerance
  admissibility). `BANPU_WP5_EPIC_CLOSEOUT.md` §13 classifies it exactly
  `TECHNICALLY SATISFIED — CARRIED FORWARD; NOT DISCHARGED BY THIS CLOSEOUT`,
  reserving discharge authority to an unnamed future act. This allocation
  preserves that classification unchanged and does not assign the residual to
  BANPU-WP6;
- `POSITION_CONVERSION_REBUILD_BOUNDARY`. `BANPU_WP5_EPIC_CLOSEOUT.md` §14
  applies identical reasoning and classification —
  `TECHNICALLY SATISFIED — CARRIED FORWARD; NOT DISCHARGED BY THIS CLOSEOUT`.
  This allocation preserves that classification unchanged and does not assign
  the residual to BANPU-WP6;
- BANPU-WP1 `MINOR-1` and `NEW-MINOR-A`, assigned to BANPU-WP4 and carried
  forward by the BANPU-WP4 Epic Closeout without resolution, reinterpretation,
  or expansion;
- BANPU-WP1 `MINOR-5`, whose remaining ownership stays with BANPU-WP7
  rehearsal and BANPU-WP8 release evidence;
- BANPU-WP2 residual identifiers `MINOR-A`, `MINOR-B`, and `OBSERVATION-A`,
  carried forward at BANPU-WP2 Epic Closeout, not resolved or reinterpreted;
- BANPU-WP3 `OBSERVATION-IC-1`, `OBSERVATION-IC-2`, `OBSERVATION-SR-1`, and
  `OBSERVATION-SR-2`, carried forward at BANPU-WP3 Epic Closeout as
  non-blocking, with no further WP3 work (`OBSERVATION-IC-3` separately
  closed by the WP3 Status Reconciliation Record);
- the `PD-3` emitter-locus item, explicitly "referred out" and recorded as
  "not a WP3 decision, residual, or obligation"; `BANPU_WP5_EPIC_CLOSEOUT.md`
  §15 records that a live search of the WP5 governance corpus found no
  artifact that claims or discharges it, and it remains unassigned and open;
  this allocation does not claim or assign it to BANPU-WP6; and
- BANPU-WP4's carried baseline missing-log assertion and reviewed
  temporary-path permission condition, and `B1`–`B6`, `RTO-1`–`RTO-13`,
  `PIA-1`–`PIA-4`, carried forward at BANPU-WP4 Epic Closeout unchanged.

No inherited item above is recorded by any canonical WP2, WP3, WP4, or WP5
closeout or synchronization as a WP6 allocation-entry blocker; §4 records that
every named entry gate is instead `SATISFIED`.

No condition in this section is satisfied by allocation itself. Any condition
that governs implementation remains unsatisfied until demonstrated by the
separately authorized act that owns it.

## 6. Allocation disposition

**`BANPU-WP6 ALLOCATED`**

The allocation binds only the exact scope in §3 and the unchanged inherited
conditions in §5. It creates no implementation authority. No production,
service, model, migration, test, CLI, frontend, or production-data change may
be made under color of this record. BANPU-WP6 implementation remains **not
authorized** and **not started**.

## 7. Explicit exclusions

This act does **not**:

- authorize or perform BANPU-WP6 implementation;
- create or perform BANPU-WP6 Implementation Authorization;
- create a BANPU-WP6 Work Package Plan;
- amend, reopen, rewrite, synchronize, or reinterpret the canonical design,
  roadmap, sequence, or any frozen planning, implementation, confirmation,
  freeze, closeout, Decision Log, or INDEX artifact;
- resolve, define, close, weaken, or waive any residual or referred item,
  including `MINOR-2`'s WP5 half or the `POSITION_CONVERSION_REBUILD_BOUNDARY`
  predicate;
- modify `RecommendationSnapshot`, `OptimizerHistory`, `UserExecutionDecision`,
  or `RecommendationGrade` schema;
- mutate or rewrite any historical recommendation or decision payload;
- redesign the transaction schema or write path;
- expand the general asset-definition vocabulary;
- introduce a general corporate-action dispatcher or event vocabulary;
- remap any unrelated symbol;
- add a public endpoint, operator CLI, frontend path, schema, or migration;
- authorize release, deployment, production execution, cache mutation,
  portfolio conversion, or production-data mutation;
- mutate, rebuild, regenerate, or otherwise touch any snapshot or shadow row,
  historical or otherwise — this act performs no regeneration of any kind;
- allocate, authorize, plan, or begin BANPU-WP7 or any later package;
- grant authority over M46; or
- stage, commit, push, merge, or publish repository changes.

The canonical explicit no-change surface remains binding as scope evidence:
`RecommendationSnapshot`/`OptimizerHistory`/`UserExecutionDecision`/
`RecommendationGrade` schema, historical recommendation or decision payloads,
transaction schema or write path, general asset-definition vocabulary, and
all M46 files.

## 8. Resulting constitutional state

- BANPU-WP1: `COMPLETE AND FROZEN`;
- BANPU-WP2: `COMPLETE AND FROZEN`;
- BANPU-WP3: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP4: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP5: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP5 implementation authority: `EXHAUSTED / CLOSED`;
- BANPU-WP5 release authority: `NONE`;
- BANPU-WP6 allocation: `COMPLETE — ALLOCATED`;
- BANPU-WP6 implementation authority: `NONE`;
- BANPU-WP6 implementation: `NOT AUTHORIZED / NOT STARTED`;
- BANPU-WP6 release and deployment authority: `NONE`;
- BANPU-WP7 and later packages: `NOT ALLOCATED / NOT AUTHORIZED`; and
- frozen BANPU artifacts, Decision Log, and Implementation INDEX: unchanged.

## 9. Exact next constitutional act

The exact next required constitutional act is **BANPU-WP6 Implementation
Authorization**, performed by a distinct competent authorization authority
over the exact allocated scope and inherited conditions recorded here.

That future act must determine implementation entry against every applicable
canonical gate. It may not infer that this allocation satisfied any of them.
Implementation remains a separate later act even if authorization is granted.

This record performs no part of that authorization or implementation.

## 10. Repository verification

| Verification | Result |
|---|---|
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP6_ALLOCATION_RECORD.md` |
| Frozen BANPU artifacts modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX files modified | `NONE` |
| Snapshot or shadow data or code touched | `NONE` |
| Prior BANPU-WP6 artifact of any kind | `NONE` found before this act |
| Nothing staged before this act | `SATISFIED` — `git diff --cached --name-only` empty |
| Commit created | `NO` |
