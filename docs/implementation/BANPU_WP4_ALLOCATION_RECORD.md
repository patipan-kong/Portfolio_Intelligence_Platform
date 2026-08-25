# BANPU-WP4 — Allocation Record

**Artifact class:** Additive constitutional allocation record
**Allocation date:** 2026-08-11
**Issuing role:** BANPU-WP4 Allocation Authority
**Allocated work package:** `BANPU-WP4 — Registry preparation and live materialization`
**Disposition:** `BANPU-WP4 ALLOCATED`
**Implementation authority created:** `NONE`
**Release authority created:** `NONE`
**BANPU-WP5+ authority created:** `NONE`

## 1. Allocation authority and constitutional boundary

Acting solely as the competent BANPU-WP4 Allocation Authority, this act
allocates the work package already defined by the canonical BANPU planning and
governance corpus. The authority exercised here is limited to:

- verifying the predecessor and dependency gates against current canonical
  repository evidence;
- binding the exact existing BANPU-WP4 scope and its inherited conditions to
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
   §9 (live materialization), §16 (test strategy), and the WP1 residual
   register;
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md),
   especially §1 (universal package rules), §2 (package inventory), §6
   (BANPU-WP4), and §11 (strict dependency graph);
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md),
   especially §1 (strict serial sequence) and §6 (Step 4 preconditions,
   repository state, changes, verification, and exit criteria);
4. the completed and frozen predecessor records:
   [`BANPU_WP1_FREEZE_RECORD.md`](BANPU_WP1_FREEZE_RECORD.md),
   [`BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP2_EPIC_CLOSEOUT.md`](BANPU_WP2_EPIC_CLOSEOUT.md),
   [`BANPU_WP3_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP3_IMPLEMENTATION_CONFIRMATION.md),
   [`BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md),
   and [`BANPU_WP3_EPIC_CLOSEOUT.md`](BANPU_WP3_EPIC_CLOSEOUT.md); and
5. the completed BANPU-WP3 repository synchronizations in the
   [Decision Log](../engineering/DECISION_LOG.md#banpu-wp3-decision-log-synchronization)
   and [Implementation INDEX](INDEX.md#banpu-wp3--quote-identity-and-epoch-protection).

The design, roadmap, and sequence are frozen members of the BANPU-WP1 corpus
recorded by the BANPU-WP1 Freeze Record §4. This act relies on their canonical
recorded authority and current repository presence; it does not restate or
replace their frozen identities.

## 3. Exact allocated scope

The allocation is exactly `BANPU-WP4 — Registry preparation and live
materialization`, with this canonical purpose: add the only authorized atomic
write path after safe replay and quote binding exist.

The allocated scope is exactly:

- add minimal predecessor-identifier retirement support if not already
  callable;
- validate successor `Asset`, current provider identifier, predecessor status,
  and the `MERGED_INTO` relationship;
- add `execute_position_conversion()` with locking, optimistic quantity and
  basis checks, canonical-fingerprint idempotency, transaction insertion,
  successor merge, and cash-in-lieu handling; and
- keep operator access service-only; CLI wiring remains deferred to BANPU-WP7.

The canonical expected implementation surface, recorded here as scope evidence
and not as implementation authority, is:

- `backend/services/portfolio_transactions.py`;
- `backend/services/asset_registry.py`;
- `backend/services/asset_repository.py` only for the minimal
  identifier-retirement operation;
- `backend/tests/test_portfolio_transactions_capability_shadow.py` or a new
  focused live-conversion test; and
- `backend/tests/test_asset_registry.py` or `test_registry_service.py`.

Allocation does not change, narrow, widen, or implement this scope.

## 4. Prerequisite and gate determination

| Requirement | Canonical evidence | Determination |
|---|---|---|
| BANPU-WP1 accepted and frozen | BANPU-WP1 Freeze Record: frozen with recorded future-package gates | `SATISFIED` |
| BANPU-WP2 accepted, frozen, and closed | BANPU-WP2 Implementation Freeze Record and Epic Closeout | `SATISFIED` |
| BANPU-WP3 accepted, confirmed, frozen, and closed | BANPU-WP3 Implementation Confirmation, Implementation Freeze Record, and Epic Closeout | `SATISFIED` |
| Roadmap dependency `BANPU-WP1–WP3` | Roadmap §2 and BANPU-WP4 §6 | `SATISFIED` |
| Sequence Steps 1–3 accepted | Mandatory Sequence §6 precondition; completed WP1–WP3 lifecycle evidence above | `SATISFIED` |
| Replay and quote validation can safely consume rows created by the future live service | WP2 replay/validator implementation is frozen; WP3 quote protection is confirmed and frozen | `SATISFIED` |
| Gate S7: WP4 does not begin until WP3 is confirmed and frozen | WP3 Epic Closeout §5, Decision Log synchronization, and Implementation INDEX each explicitly record S7 satisfied | `SATISFIED` |
| Prior BANPU-WP4 allocation absent | No earlier `BANPU_WP4_ALLOCATION_RECORD.md` or WP4 implementation-authorization artifact existed before this act | `SATISFIED` |

BANPU-WP3 completion and freeze therefore satisfy the immediate-predecessor
requirement. The constitutional prerequisites for allocation are satisfied.

## 5. Residuals and inherited conditions

Allocation resolves, defines, weakens, reinterprets, or waives none of the
following:

- BANPU-WP1 `MINOR-1`, assigned to WP4 before fingerprint-based idempotency is
  active: focused distinct-payload fingerprint vectors beyond 28 significant
  digits and WP4 retry/conflict evidence remain required;
- BANPU-WP1 `NEW-MINOR-A`, assigned to WP4 authoring: naive-midnight authoring,
  rejection of offset-bearing authoring inputs, and payload/date equality
  evidence remain required;
- BANPU-WP1 `MINOR-2` and `MINOR-5`, whose remaining ownership stays with their
  canonically assigned later packages;
- BANPU-WP1's separately recorded `backend/models/database.py` identity
  residual and the historical WP2 Step 8 gate language;
- BANPU-WP2 residual identifiers `MINOR-A`, `MINOR-B`, and `OBSERVATION-A`
  through `OBSERVATION-E`, which remain unresolved and are inherited by
  BANPU-WP4 through BANPU-WP8 unchanged;
- WP3 residual R6, the WP3-scoped R7 formal waiver, and WP3's non-blocking
  closeout observations; and
- the emitter-locus item referred out by WP3 PD-3 to the authority governing
  the canonical design, roadmap, and package inventory.

The canonical corpus classifies the WP1 items assigned to WP4 as future
implementation-time verification gates, not open WP1 findings. The WP2 labels
and other carried conditions are preserved without interpretation. None is
recorded by the canonical WP3 closeout or synchronizations as blocking WP4
allocation; those records instead state expressly that S7 is satisfied.

No condition in this section is satisfied by allocation itself. Any condition
that governs implementation remains unsatisfied until demonstrated by the
separately authorized act that owns it.

## 6. Allocation disposition

**`BANPU-WP4 ALLOCATED`**

The allocation binds only the exact scope in §3 and the unchanged inherited
conditions in §5. It creates no implementation authority. No production,
service, model, migration, test, CLI, frontend, or production-data change may
be made under color of this record.

## 7. Explicit exclusions

This act does **not**:

- authorize or perform BANPU-WP4 implementation;
- create or perform BANPU-WP4 Implementation Authorization;
- amend, reopen, rewrite, synchronize, or reinterpret the canonical design,
  roadmap, sequence, or any frozen planning, implementation, confirmation,
  freeze, closeout, Decision Log, or INDEX artifact;
- resolve, define, close, weaken, or waive any residual or referred item;
- add a public endpoint, operator CLI, frontend path, schema, migration,
  general corporate-action framework, or `LedgerRepair` behavior;
- authorize release, deployment, production execution, cache mutation,
  portfolio conversion, or production-data mutation;
- allocate, authorize, plan, or begin BANPU-WP5 or any later package;
- grant authority over M46; or
- stage, commit, push, merge, or publish repository changes.

The canonical explicit no-change surface remains binding as scope evidence:
`backend/models/asset.py`, `backend/services/ledger_repair.py`,
`backend/models/database.py` except the already accepted WP1 changes,
`backend/main.py` transaction endpoints, frontend files, `backend/manage.py`,
and all M46 files.

## 8. Resulting constitutional state

- BANPU-WP1: `COMPLETE AND FROZEN`;
- BANPU-WP2: `COMPLETE AND FROZEN`;
- BANPU-WP3: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP3 implementation authority: `EXHAUSTED / CLOSED`;
- BANPU-WP3 release authority: `NONE`;
- BANPU-WP4 allocation: `COMPLETE — ALLOCATED`;
- BANPU-WP4 implementation authority: `NONE`;
- BANPU-WP4 implementation: `NOT AUTHORIZED / NOT STARTED`;
- BANPU-WP4 release and deployment authority: `NONE`;
- BANPU-WP5 and later packages: `NOT ALLOCATED / NOT AUTHORIZED`; and
- frozen BANPU artifacts, Decision Log, and Implementation INDEX: unchanged.

## 9. Exact next constitutional act

The exact next required constitutional act is **BANPU-WP4 Implementation
Authorization**, performed by a distinct competent authorization authority over
the exact allocated scope and inherited conditions recorded here.

That future act must determine implementation entry against every applicable
canonical gate, including the WP4-owned `MINOR-1` and `NEW-MINOR-A`
verification obligations. It may not infer that this allocation satisfied
them. Implementation remains a separate later act even if authorization is
granted.

This record performs no part of that authorization or implementation.

## 10. Repository verification

| Verification | Result |
|---|---|
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP4_ALLOCATION_RECORD.md` |
| Frozen BANPU artifacts modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX files modified | `NONE` |
| Trailing-whitespace verification | `PASS` |
| Markdown relative-link target verification | `PASS` — 11 targets checked |
| Markdown fragment-heading verification | `PASS` |
| `git diff --check` | `PASS` |
| `git diff --cached --check` | `PASS` — nothing staged |
| `graphify update .` | `PASS` — code graph rebuilt; no implementation change introduced |
| Final `git status --short --untracked-files=all` | Exactly one entry: `?? docs/implementation/BANPU_WP4_ALLOCATION_RECORD.md` |
| Commit created | `NO` |
