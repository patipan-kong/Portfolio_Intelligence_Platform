# BANPU-WP7 — Allocation Record

**Artifact class:** Additive constitutional allocation record
**Allocation date:** 2026-08-18
**Issuing role:** BANPU-WP7 Allocation Authority
**Allocated work package:** `BANPU-WP7 — Operator command and migration rehearsal`
**Disposition:** `BANPU-WP7 ALLOCATED`
**Implementation authority created:** `NONE`
**Release authority created:** `NONE`
**BANPU-WP8+ authority created:** `NONE`

## 1. Allocation authority and constitutional boundary

Acting solely as the competent BANPU-WP7 Allocation Authority, this act
allocates the work package already defined by the canonical BANPU planning and
governance corpus. The authority exercised here is limited to:

- verifying the predecessor and dependency gates against current canonical
  repository evidence;
- binding the exact existing BANPU-WP7 scope and its inherited conditions to
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
   the approved and authoritative implementation specification, as the
   originating authority for the operator command and rehearsal surface that
   the Roadmap and Sequence decompose into BANPU-WP7;
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md),
   especially §1 (universal package rules), §2 (package inventory, line 30:
   `BANPU-WP7 | Operator command and migration rehearsal | WP1–WP6 | S | M`),
   §9 (BANPU-WP7 purpose, scope, files expected to change, explicit files not
   to change, dependencies, deliverables, acceptance criteria, verification),
   and §11 (strict dependency graph);
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md),
   especially §1 (strict serial sequence) and §9 (Step 7 preconditions,
   repository state, expected changes, verification, and exit criteria);
4. the completed and frozen predecessor records:
   [`BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md)
   and
   [`BANPU_WP6_EPIC_CLOSEOUT.md`](BANPU_WP6_EPIC_CLOSEOUT.md), whose §17
   ("WP7 successor boundary") directly addresses this allocation's
   predecessor and synchronization gates and holds that this allocation
   requires both a completed BANPU-WP6 Decision Log synchronization and a
   completed BANPU-WP6 Implementation INDEX synchronization; and
5. the completed BANPU-WP6 repository synchronizations in the
   [Decision Log](../engineering/DECISION_LOG.md#banpu-wp6-decision-log-synchronization)
   and [Implementation INDEX](INDEX.md#banpu-wp6--shadow-and-succession-aware-time-series-continuity).

The design, roadmap, and sequence are frozen members of the BANPU-WP1 corpus
recorded by the BANPU-WP1 Freeze Record §4. This act relies on their canonical
recorded authority and current repository presence; it does not restate or
replace their frozen identities.

Before relying on it, the BANPU-WP6 terminal state was independently re-read
against live repository bytes rather than accepted from prior text alone, in
this same act. `BANPU_WP6_EPIC_CLOSEOUT.md` line 6 reads exactly
`**Disposition:** \`BANPU-WP6 EPIC CLOSEOUT COMPLETE\``, and its §21 already
records an independent byte-level recomputation of the frozen implementation
corpus with zero drift; this act relies on that already-performed
recomputation rather than duplicating it. The Epic Closeout's §17 ("WP7
successor boundary") was independently re-read and confirms, in terms
specific to this allocation: the WP1–WP6 predecessor dependency was already
satisfied by WP6's own Implementation Confirmation and Freeze; the Closeout
itself allocates and authorizes nothing; and WP7 allocation requires both
completed WP6 Decision Log and Implementation INDEX synchronization.

The Decision Log's `BANPU-WP6 Decision Log Synchronization` entry
(`DECISION_LOG.md` line 3051 onward) and the Implementation INDEX's BANPU-WP6
row (`INDEX.md` lines 264–291) were independently re-read in this act and
found mutually consistent: both record BANPU-WP6 as `COMPLETE`, `FROZEN`, and
`CLOSED`, and the Implementation INDEX additionally states, in terms specific
to WP7: "WP7's Decision Log and Implementation INDEX entry prerequisites are
both now satisfied; WP7 remains `NOT ALLOCATED` and `NOT AUTHORIZED`."
`INDEX.md` lines 284–287 confirm WP6 carries forward zero WP6-native
residuals and that `MINOR-2` and `POSITION_CONVERSION_REBUILD_BOUNDARY`
remain WP5-owned, not WP6-owned.

Repository state was re-verified live immediately before this act: HEAD is
`ae223a42df688563748c0e6e6cb898e66bcb3da0` (`fix(market-data): correct Yahoo
previous-close session derivation`), identical to the HEAD examined by the
immediately preceding BANPU-WP7 Pre-Allocation Constitutional Verification;
the working tree and staging area are clean (`git status` reports "nothing to
commit, working tree clean"). Because HEAD has not moved and the tree is
clean, the content of every artifact cited above is provably unchanged since
that verification. A repository-wide search for `BANPU_WP7_*` and a full
`git log --all` search for any prior BANPU-WP7 artifact both found none; the
only history hit for a "WP7" token is the unrelated `M38-WP7` milestone
lineage (`2ae58ee M38-WP7: Freeze Experience Composition Runtime`), which is
a distinct, non-BANPU naming system.

## 3. Exact allocated scope

The allocation is exactly `BANPU-WP7 — Operator command and migration
rehearsal`, with this canonical purpose: provide a safe, idempotent,
CLI-only path to prepare and apply the reviewed production manifest.

The allocated scope is exactly (Roadmap §9 "Scope"):

- add `apply_position_conversion` CLI with dry-run default and explicit
  `--commit`;
- validate manifest schema, registry state, broker facts, quote epoch,
  continuity evidence, rebuild boundary, and both replay modes;
- produce a deterministic before/after report without exposing credentials
  or raw provider payloads; and
- add cache purge and bounded rebuild instructions; do not execute
  production changes in the package.

The canonical expected implementation surface, recorded here as scope
evidence and not as implementation authority, is (Roadmap §9 "Files expected
to change"):

- `backend/manage.py`;
- a new sanitized test manifest under `backend/tests/fixtures/`;
- a new focused CLI test file; and
- operational documentation only if required by the canonical design, and
  not M46 documentation.

The Roadmap §9 explicit no-change surface remains binding as scope evidence:
public API routes; frontend files; core accounting equations accepted in
prior packages; the production database or production cache; and all M46
files. The Roadmap §9 acceptance criteria additionally bind that: no flags
performs no write; `--dry-run` performs no write; `--commit` is explicit and
refuses any failed preflight; re-running the same manifest is an
`already_applied` no-op; a conflicting manifest fails; and the command never
broadens scope to generic corporate actions.

Sequence §9 (Step 7) additionally records, as scope evidence carried forward
unchanged: the expected code changes are CLI manifest parsing, preflight,
dry-run default, explicit commit, deterministic reporting, and idempotent
retry behavior, plus a sanitized manifest fixture and CLI tests; verification
requires zero-diff no-flag/dry-run runs, a commit gate behind every
preflight, no-op retry and conflict-fails behavior, and an isolated
production-shaped rehearsal covering migration, registry preparation, quote
gate, conversion, bounded rebuild, shadow regeneration, and transaction
rollback; and the exit criteria require that no public conversion endpoint
exists and that the rehearsal touches no production system.

Allocation does not change, narrow, widen, or implement this scope.

## 4. Prerequisite and gate determination

| Requirement | Canonical evidence | Determination |
|---|---|---|
| BANPU-WP1 accepted, confirmed, frozen | `BANPU_WP1_FREEZE_RECORD.md`; Roadmap §2/§9 line 30 dependency `WP1–WP6` | `SATISFIED` |
| BANPU-WP2 accepted, confirmed, frozen | `BANPU_WP2_EPIC_CLOSEOUT.md`; Roadmap §9 dependency `WP1–WP6` | `SATISFIED` |
| BANPU-WP3 accepted, confirmed, frozen, closed | `BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP3_EPIC_CLOSEOUT.md` | `SATISFIED` |
| BANPU-WP4 accepted, confirmed, frozen, closed | `BANPU_WP4_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP4_EPIC_CLOSEOUT.md` | `SATISFIED` |
| BANPU-WP5 accepted, confirmed, frozen, closed | `BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP5_EPIC_CLOSEOUT.md` | `SATISFIED` |
| BANPU-WP6 accepted, confirmed, frozen, closed | `BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md`, `BANPU_WP6_EPIC_CLOSEOUT.md` line 6 (`BANPU-WP6 EPIC CLOSEOUT COMPLETE`) — re-read live in §2 above | `SATISFIED` |
| Roadmap dependency `BANPU-WP1–WP6` (Roadmap §2/§9 line 30) | Roadmap §2 line 30; §9 "Dependencies" | `SATISFIED` |
| Sequence Step 7 precondition: Steps 1–6 accepted | Sequence §9 precondition 1; completed WP1–WP6 lifecycle evidence above | `SATISFIED` |
| Sequence Step 7 precondition: all runtime readers and writers understand the conversion | WP6 Closeout §11/§12 (18/18 capability-completion and acceptance rows `PASS` across shadow/attribution/quant/grader/ideal-series consumers) | `SATISFIED` |
| BANPU-WP6 Decision Log synchronization | [Decision Log](../engineering/DECISION_LOG.md#banpu-wp6-decision-log-synchronization) — `BANPU-WP6 DECISION LOG SYNCHRONIZED`, re-read live in §2 above | `SATISFIED` |
| BANPU-WP6 Implementation INDEX synchronization | [Implementation INDEX](INDEX.md#banpu-wp6--shadow-and-succession-aware-time-series-continuity) — BANPU-WP6 row records `COMPLETE`, `FROZEN`, `CLOSED`; text states WP7's Decision Log and Implementation INDEX entry prerequisites are both satisfied, re-read live in §2 above | `SATISFIED` |
| WP6 Epic Closeout's own §17 determination of the WP7 predecessor/synchronization gates | `BANPU_WP6_EPIC_CLOSEOUT.md` §17, re-read live in §2 above | Confirms all of the above; `SATISFIED` |
| Prior BANPU-WP7 allocation absent | Repository search found no `BANPU_WP7_*` or equivalent artifact existing before this act; full `git log --all` found none | `SATISFIED` |

BANPU-WP6 completion, confirmation, freeze, closure, and both repository
synchronizations therefore satisfy the immediate-predecessor requirement. The
constitutional prerequisites for allocation are satisfied.

Entry-prerequisite satisfaction is distinct from allocation, and allocation is
distinct from Implementation Authorization. This act performs only
allocation; it does not treat WP6's authority, or the mere existence of the
satisfied entry prerequisite recorded by the Decision Log and Implementation
INDEX, as automatically flowing into WP7 authorization or implementation.

## 5. Residuals and inherited conditions

Allocation resolves, defines, weakens, reinterprets, or waives none of the
following. The residuals with an explicit WP7 dimension are bound to their
**exact recorded partial scope only** — never the whole residual — and every
other residual is recorded here without reassignment:

- **BANPU-WP1 `MINOR-5`** (accepted PostgreSQL execution-verification
  residual). `BANPU_WP1_FREEZE_RECORD.md` §7 splits this residual by
  function, not by percentage: this allocation binds to BANPU-WP7 only the
  **rehearsal portion** — real PostgreSQL upgrade rehearsal, repeated-upgrade
  rehearsal, constraint/index probes, and guarded-downgrade rehearsal,
  performed within the isolated production-shaped rehearsal required by
  Sequence §9. The **release-evidence portion remains BANPU-WP8-owned** and
  is not bound, claimed, discharged, or superseded by this allocation;
- **`NEW-MINOR-A`** (accepted PostgreSQL typed-storage/coercion residual).
  `BANPU_WP1_FREEZE_RECORD.md` §7 splits this residual into a WP4 authoring
  portion, already closed and not reopened or reinterpreted by this act, and
  a **production-dialect-rehearsal portion**, which alone is bound to
  BANPU-WP7 by this allocation;
- the `PD-3` emitter-locus item, explicitly "referred out" and recorded as
  "not a WP3 decision, residual, or obligation." `BANPU_WP4_ALLOCATION_RECORD.md`,
  `BANPU_WP5_ALLOCATION_RECORD.md`, `BANPU_WP6_ALLOCATION_RECORD.md`, and
  `BANPU_WP6_EPIC_CLOSEOUT.md` §15 each independently confirm no artifact
  claims or discharges it; it remains **unassigned and open at WP level**.
  This allocation does **not** absorb it, allocate it to BANPU-WP7,
  reinterpret it as a WP7 prerequisite, or claim to resolve it;
- BANPU-WP1 `MINOR-2`, WP3/WP5-owned (reference prices / mechanical
  tolerance). `BANPU_WP5_EPIC_CLOSEOUT.md` §13 classifies it exactly
  `TECHNICALLY SATISFIED — CARRIED FORWARD; NOT DISCHARGED`. This allocation
  preserves that classification unchanged and does not assign the residual
  to BANPU-WP7;
- `POSITION_CONVERSION_REBUILD_BOUNDARY`, WP5-owned. `BANPU_WP5_EPIC_CLOSEOUT.md`
  §14 applies identical reasoning and classification. This allocation
  preserves it unchanged and does not assign it to BANPU-WP7;
- BANPU-WP1 `MINOR-1`, assigned to and closed at BANPU-WP4, not reopened;
- BANPU-WP2 residual identifiers `MINOR-A`, `MINOR-B`, and `OBSERVATION-A`,
  carried forward at BANPU-WP2 Epic Closeout, not resolved or reinterpreted;
- BANPU-WP3 `OBSERVATION-IC-1`, `OBSERVATION-IC-2`, `OBSERVATION-SR-1`, and
  `OBSERVATION-SR-2`, carried forward at BANPU-WP3 Epic Closeout as
  non-blocking (`OBSERVATION-IC-3` separately closed by the WP3 Status
  Reconciliation Record); and
- BANPU-WP4's carried baseline missing-log assertion and reviewed
  temporary-path permission condition, and `B1`–`B6`, `RTO-1`–`RTO-13`,
  `PIA-1`–`PIA-4`, carried forward at BANPU-WP4 Epic Closeout unchanged.

No inherited item above is recorded by any canonical WP1–WP6 closeout,
freeze record, or allocation record as a WP7 allocation-entry blocker; §4
records that every named entry gate is instead `SATISFIED`. Allocation grants
no authority to resolve, narrow, or reassign any residual owned by WP1–WP6,
WP8, another authority, or no WP-level owner.

No condition in this section is satisfied by allocation itself. Any condition
that governs implementation — including the WP7-bound rehearsal portions of
`MINOR-5` and `NEW-MINOR-A` — remains unsatisfied until demonstrated by the
separately authorized act that owns it.

## 6. Allocation disposition

**`BANPU-WP7 ALLOCATED`**

The allocation binds only the exact scope in §3 and the unchanged inherited
conditions in §5. It creates no implementation authority. No production,
service, model, migration, test, CLI, frontend, or production-data change may
be made under color of this record. BANPU-WP7 implementation remains **not
authorized** and **not started**.

## 7. Explicit exclusions

This act does **not**:

- authorize or perform BANPU-WP7 implementation;
- create or perform BANPU-WP7 Implementation Authorization;
- create a BANPU-WP7 Work Package Plan;
- amend, reopen, rewrite, synchronize, or reinterpret the canonical design,
  roadmap, sequence, or any frozen planning, implementation, confirmation,
  freeze, closeout, Decision Log, or INDEX artifact for WP1–WP6;
- resolve, define, close, weaken, or waive any residual or referred item,
  including `MINOR-5`'s WP8 release-evidence portion, `NEW-MINOR-A`'s WP4
  authoring portion, `MINOR-2`'s WP3/WP5 scope, the
  `POSITION_CONVERSION_REBUILD_BOUNDARY` predicate, or `PD-3`;
- assign, claim, or absorb `PD-3` into BANPU-WP7 scope;
- run, execute, dry-run, or commit `apply_position_conversion` against any
  database, isolated or production;
- perform any production-shaped rehearsal, migration, registry preparation,
  quote-gate action, conversion, bounded rebuild, shadow regeneration, or
  transaction rollback;
- add or modify public API routes, frontend files, core accounting
  equations accepted in prior packages, or the production database or
  cache;
- modify `backend/manage.py`, add a CLI, or add any test or fixture;
- authorize release, deployment, production execution, cache mutation,
  portfolio conversion, or production-data mutation;
- mutate, rebuild, regenerate, or otherwise touch any snapshot or shadow row,
  historical or otherwise — this act performs no regeneration of any kind;
- allocate, authorize, plan, or begin BANPU-WP8 or any later package;
- grant authority over M46; or
- stage, commit, push, merge, or publish repository changes.

The canonical explicit no-change surface remains binding as scope evidence:
public API routes, frontend files, core accounting equations accepted in
prior packages, the production database or production cache, and all M46
files.

## 8. Resulting constitutional state

- BANPU-WP1: `COMPLETE AND FROZEN`;
- BANPU-WP2: `COMPLETE AND FROZEN`;
- BANPU-WP3: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP4: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP5: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP6: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP6 implementation authority: `EXHAUSTED / CLOSED`;
- BANPU-WP6 release authority: `NONE`;
- BANPU-WP7 allocation: `COMPLETE — ALLOCATED`;
- BANPU-WP7 implementation authority: `NONE`;
- BANPU-WP7 implementation: `NOT AUTHORIZED / NOT STARTED`;
- BANPU-WP7 release and deployment authority: `NONE`;
- BANPU-WP7 bound residual scope: `MINOR-5` rehearsal portion and
  `NEW-MINOR-A` production-dialect-rehearsal portion recorded as inherited,
  unsatisfied conditions — not discharged;
- `PD-3`: `UNASSIGNED / OPEN`, not BANPU-WP7-owned;
- BANPU-WP8 and later packages: `NOT ALLOCATED / NOT AUTHORIZED`; and
- frozen BANPU artifacts, Decision Log, and Implementation INDEX: unchanged.

## 9. Exact next constitutional act

The exact next required constitutional act is **BANPU-WP7 Implementation
Authorization**, performed by a distinct competent authorization authority
over the exact allocated scope and inherited conditions recorded here.

That future act must determine implementation entry against every applicable
canonical gate. It may not infer that this allocation satisfied any of them.
Implementation, including any part of the `MINOR-5` or `NEW-MINOR-A`
rehearsal, remains a separate later act even if authorization is granted.

This record performs no part of that authorization or implementation.

## 10. Repository verification

| Verification | Result |
|---|---|
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP7_ALLOCATION_RECORD.md` |
| Frozen BANPU artifacts modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX files modified | `NONE` |
| Snapshot or shadow data or code touched | `NONE` |
| Prior BANPU-WP7 artifact of any kind | `NONE` found before this act |
| Nothing staged before this act | `SATISFIED` — working tree clean before this act |
| Commit created | `NO` |
