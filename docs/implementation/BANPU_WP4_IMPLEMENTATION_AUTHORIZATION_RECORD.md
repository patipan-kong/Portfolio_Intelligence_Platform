# BANPU-WP4 — Implementation Authorization Record

**Artifact class:** Additive constitutional authorization record
**Authorization date:** 2026-08-11
**Issuing role:** BANPU-WP4 Implementation Authorization Authority
**Authorized work package:** `BANPU-WP4 — Registry preparation and live materialization`
**Disposition:** `BANPU-WP4 IMPLEMENTATION AUTHORIZED`
**Implementation authority created:** `LIMITED — see §8–§11`
**Release/deployment authority created:** `NONE`
**BANPU-WP5+ authority created:** `NONE`

## 1. Authorization authority and boundary

Acting solely as the distinct competent BANPU-WP4 Implementation Authorization
Authority, this act authorizes implementation of the exact work package already
allocated by
[`BANPU_WP4_ALLOCATION_RECORD.md`](BANPU_WP4_ALLOCATION_RECORD.md).

The authority exercised here is limited to verifying authorization-entry
conditions, binding implementation to the allocated scope and inherited gates,
and creating this additive record. This act does not implement code, perform a
review or confirmation, freeze implementation, authorize release or deployment,
or amend or synchronize any existing artifact.

Allocation is a prerequisite to this act, not evidence that an implementation
gate has been performed. No gate is marked satisfied merely because WP4 was
allocated.

## 2. Canonical authority relied upon

This authorization relies on, and does not amend or reinterpret:

1. [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   the authoritative implementation specification, especially §9 live
   materialization, §16 test strategy, and its WP1 residual register;
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md),
   especially §1 universal rules, §2 dependency inventory, §6 BANPU-WP4, and
   §11 strict dependency graph;
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md),
   especially §1 sequence invariants and §6 Step 4;
4. the frozen predecessor evidence:
   [`BANPU_WP1_FREEZE_RECORD.md`](BANPU_WP1_FREEZE_RECORD.md),
   [`BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md`](BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md),
   [`BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md),
   [`BANPU_WP2_EPIC_CLOSEOUT.md`](BANPU_WP2_EPIC_CLOSEOUT.md),
   [`BANPU_WP3_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP3_IMPLEMENTATION_CONFIRMATION.md),
   [`BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md),
   and [`BANPU_WP3_EPIC_CLOSEOUT.md`](BANPU_WP3_EPIC_CLOSEOUT.md);
5. the completed WP3 repository synchronizations in the
   [Decision Log](../engineering/DECISION_LOG.md#banpu-wp3-decision-log-synchronization)
   and [Implementation INDEX](INDEX.md#banpu-wp3--quote-identity-and-epoch-protection);
   and
6. the BANPU-WP4 Allocation Record, 11,180 raw working-tree bytes, 214 physical
   lines, SHA-256
   `CEE6F01C4113697BE6485AE56BB80FE0E9E99CB8555C08BC5D3E3CD67B94BAA9`,
   disposition `BANPU-WP4 ALLOCATED`.

The design, roadmap, and sequence remain frozen members of the BANPU-WP1
corpus. Their recorded identities and authority are relied upon as canonical;
this act does not replace them with a new identity convention.

## 3. Exact authorized implementation scope

Authorization is granted exactly for `BANPU-WP4 — Registry preparation and
live materialization`, whose canonical purpose is to add the only authorized
atomic write path after safe replay and quote binding exist.

Implementation authority covers exactly these capabilities:

- minimal predecessor-identifier retirement support if not already callable;
- validation of successor `Asset`, current provider identifier, predecessor
  status, and the `MERGED_INTO` relationship;
- `execute_position_conversion()` with portfolio and relevant-item locking,
  optimistic quantity and basis assertions, canonical-fingerprint idempotency,
  append-only transaction insertion, predecessor removal or transformation,
  successor creation or merge, optional cash-in-lieu materialization, and final
  shares/basis/cash/identity assertions in one database transaction; and
- service-only internal access. Operator CLI wiring remains BANPU-WP7 work.

Symbols and provider identifiers must be registry-resolved rather than trusted
from arbitrary inputs. The successor must remain a distinct `Asset`; the
predecessor is not renamed. Registry preparation must establish the current
successor `PROVIDER_SYMBOL`, retire the predecessor identifier, transition the
predecessor to `MERGED`, and create the existing `MERGED_INTO` relationship.
The ratio remains only in the transaction payload.

## 4. Authorized file surface

### 4.1 Production surface

- `backend/services/portfolio_transactions.py`;
- `backend/services/asset_registry.py`; and
- `backend/services/asset_repository.py`, only for the minimal
  identifier-retirement operation.

### 4.2 Test surface

- `backend/tests/test_portfolio_transactions_capability_shadow.py` or one new
  focused live-conversion test module;
- `backend/tests/test_asset_registry.py` or `test_registry_service.py`; and
- focused tests strictly required to prove the mandatory WP4 verification
  matrix without introducing another production capability.

### 4.3 Conditional MINOR-1 surface

The canonical WP1 residual register assigns the fingerprint precision
improvement to WP4 even though the roadmap's expected-file forecast does not
list the frozen WP1 canonicalizer surface. Roadmap §1 therefore applies:
another production file requires reviewer confirmation that it is strictly
necessary under the canonical design.

Accordingly, this authorization does **not** presently permit an edit to
`backend/services/transaction_canonicalizer.py`. That file and the corresponding
focused vector surface in `backend/tests/test_transaction_canonicalizer.py`
become implementation-editable only after a reviewer records strict necessity
under roadmap §1, and only for the minimal `MINOR-1` precision correction and
its required vectors. The confirmation cannot authorize any other WP1 change.

No production file outside §4.1 and that conditionally admitted §4.3 surface is
authorized. A different file or capability requires a distinct constitutional
authorization; it cannot be inferred from the roadmap's “expected files”
language.

## 5. Prerequisite and implementation-entry determination

| Requirement | Evidence and classification | State at authorization |
|---|---|---|
| BANPU-WP4 allocation exists | Allocation Record disposition `BANPU-WP4 ALLOCATED`; identity bound in §2 | `SATISFIED` |
| BANPU-WP1 accepted and frozen | BANPU-WP1 Freeze Record; residuals carried as future-package gates | `SATISFIED` |
| BANPU-WP2 accepted, frozen, and closed | BANPU-WP2 Implementation Freeze and Epic Closeout | `SATISFIED` |
| BANPU-WP3 accepted, confirmed, frozen, and closed | BANPU-WP3 Confirmation, Freeze, Epic Closeout, Decision Log, and INDEX | `SATISFIED` |
| Roadmap dependency WP1–WP3 | Roadmap §2 and §6 | `SATISFIED` |
| Sequence Steps 1–3 accepted | Sequence §6 precondition and predecessor lifecycle evidence | `SATISFIED` |
| Replay and quote validation safely consume future live-service rows | Frozen WP2 replay/validator and frozen WP3 quote protection | `SATISFIED` |
| Gate S7: WP3 confirmed and frozen before WP4 begins | Explicitly satisfied by WP3 Epic Closeout, Decision Log, and INDEX | `SATISFIED` |
| Review-frozen repository state with no overlapping implementation change | No tracked or staged diff; only the additive WP4 Allocation Record existed before this act | `SATISFIED` |
| No earlier WP4 implementation authority | No prior WP4 Implementation Authorization Record existed | `SATISFIED` |
| No conflicting authority | WP3 authority exhausted/closed; WP5+, release, deployment, M46, and production execution remain unauthorized | `SATISFIED` |
| `MINOR-1` completion | Pre-use and conditional-file gate, not a pre-authorization gate | `OPEN — IMPLEMENTATION-TIME` |
| `NEW-MINOR-A` completion | WP4 authoring/test obligation, not a pre-authorization gate | `OPEN — IMPLEMENTATION-TIME` |
| Reviewer confirmation for any production file outside roadmap forecast | Conditional pre-edit gate under roadmap §1 | `OPEN AS TO §4.3 ONLY` |

All authorization-entry prerequisites are satisfied. Open implementation-time
conditions remain open and are not satisfied, waived, or bypassed by this act.

## 6. Treatment of BANPU-WP1 `MINOR-1`

`MINOR-1` records that fingerprint serialization can lose distinctions beyond
the default Decimal context precision. Its canonical verification point is
**before `execute_position_conversion()` uses the fingerprint for
idempotency**.

It is therefore:

- not a pre-authorization gate;
- a mandatory implementation-time pre-use gate;
- subject to the roadmap §1 reviewer-confirmation gate before any edit to the
  conditional canonicalizer surface in §4.3; and
- an exit/confirmation evidence obligation requiring focused vectors with
  distinct values beyond 28 significant digits, followed by WP4 retry and
  conflict tests proving distinct payloads cannot collide.

Fingerprint idempotency may not become active until the precision obligation
and its pre-use evidence are complete. WP4 may not be confirmed, frozen, or
closed without the required vectors and retry/conflict evidence.

## 7. Treatment of BANPU-WP1 `NEW-MINOR-A`

`NEW-MINOR-A` is the accepted PostgreSQL typed-storage/coercion residual. The
WP4 obligation is to construct `transaction_date` only from the payload's
timezone-free date as a naive-midnight typed value.

It is therefore:

- not a pre-authorization gate;
- a mandatory WP4 implementation-time authoring obligation; and
- an exit/confirmation evidence obligation requiring service tests that reject
  offset-bearing authoring inputs and prove payload/date equality and canonical
  naive-midnight construction.

The later real-PostgreSQL coercion and stored-invariant probes remain assigned
to BANPU-WP7, with release evidence retained by BANPU-WP8. This authorization
does not pull those later-package obligations into WP4.

## 8. Inherited residuals and referred items

This authorization preserves, without definition, resolution, waiver, or
reinterpretation:

- WP1 `MINOR-2`, whose remaining mechanical-tolerance obligation belongs to
  WP5;
- WP1 `MINOR-5`, assigned to WP7 rehearsal and WP8 release evidence;
- WP1's `backend/models/database.py` identity residual and historical WP2 Step
  8 gate language;
- WP2 residual identifiers `MINOR-A`, `MINOR-B`, and `OBSERVATION-A` through
  `OBSERVATION-E`;
- WP3 R6 and its separately governed documentation-correction status;
- the WP3-scoped R7 waiver, which creates no relief or precedent for WP4;
- WP3 closeout observations, expressly recorded as non-blocking and gating
  nothing; and
- the emitter-locus item referred out by WP3 PD-3.

The seven WP2 residuals are inherited by WP4 unchanged, but the repository
contains their identifiers without accompanying obligation text. No canonical
WP4 artifact classifies them as implementation-authorization gates or assigns
them a WP4 verification point. This authority therefore neither invents an
obligation nor infers a blocker from the absence of text. They remain binding
unresolved conditions exactly as carried.

The PD-3 emitter-locus item belongs to the authority governing the canonical
design, roadmap, and package inventory. No canonical artifact assigns it to
WP4, and no WP4 acceptance criterion depends on its disposition. It does not
block this authorization and is not resolved by it.

## 9. Mandatory implementation boundaries and exit evidence

Implementation must preserve all roadmap acceptance criteria and must prove:

- no public endpoint or frontend path can create a conversion;
- transaction and materialized state commit or roll back together;
- transaction 83 and all prior ledger rows remain untouched;
- matching retries are no-ops and conflicting retries fail;
- predecessor and successor registry states and their `MERGED_INTO`
  relationship are exact;
- live outcome equals frozen WP2 replay outcome; and
- success, existing-successor, no-CIL, CIL, stale-expectation, duplicate,
  registry-mismatch, and forced-rollback database-session cases pass together
  with existing fee, asset-ID write-path, registry, and portfolio-transaction
  suites.

No conversion row, registry production mutation, cache purge, rebuild, or
production shadow rewrite may occur during implementation. A failed
verification returns work to WP4; no later package may compensate for it.

## 10. Authorization granted

**BANPU-WP4 implementation is authorized**, strictly within §§3–4 and subject
to every gate and obligation in §§5–9.

This is a scoped grant of implementation authority, not implementation itself.
It grants no authority to skip an open implementation-time gate, change a
frozen artifact, expand the production surface, or treat allocation as
verification evidence.

## 11. Explicit exclusions

This act creates:

- `NO` implementation performed by this record;
- `NO` authority to edit the conditional §4.3 surface before roadmap §1
  reviewer confirmation;
- `NO` schema or migration authority and `NO` authority to modify
  `backend/models/asset.py`, `backend/models/database.py`,
  `backend/services/ledger_repair.py`, `backend/main.py` transaction endpoints,
  frontend files, or `backend/manage.py`;
- `NO` public endpoint, operator CLI, frontend authoring path, general
  corporate-action framework, or `LedgerRepair` conversion behavior;
- `NO` authority to amend, reopen, synchronize, or reinterpret the design,
  roadmap, sequence, Allocation Record, or any frozen predecessor artifact;
- `NO` authority to resolve or waive an inherited residual or referred item;
- `NO` implementation review, confirmation, freeze, epic closeout, Decision Log
  synchronization, or Implementation INDEX synchronization;
- `NO` release, deployment, production execution, cache mutation, portfolio
  conversion, or production-data mutation authority;
- `NO` BANPU-WP5 or later-package allocation or implementation authority;
- `NO` M46 authority; and
- `NO` authority to stage, commit, push, merge, or publish changes.

## 12. Authorization disposition

**`BANPU-WP4 IMPLEMENTATION AUTHORIZED`**

Authorization is bound to the Allocation Record identity in §2 and the exact
scope and conditions in this record. `MINOR-1`, `NEW-MINOR-A`, the conditional
reviewer gate, inherited residuals, and referred items remain in the states
recorded above. No implementation has begun under this act.

## 13. Resulting constitutional state

- BANPU-WP1: `COMPLETE AND FROZEN`;
- BANPU-WP2: `COMPLETE AND FROZEN`;
- BANPU-WP3: `COMPLETE`, `FROZEN`, and `CLOSED`;
- BANPU-WP3 implementation authority: `EXHAUSTED / CLOSED`;
- BANPU-WP4 allocation: `COMPLETE — ALLOCATED`;
- BANPU-WP4 implementation authority: `AUTHORIZED — BOUNDED`;
- BANPU-WP4 implementation: `AUTHORIZED / NOT STARTED`;
- BANPU-WP4 release and deployment authority: `NONE`;
- BANPU-WP5 and later packages: `NOT ALLOCATED / NOT AUTHORIZED`;
- M46 authority: `NONE`; and
- frozen artifacts, Decision Log, and Implementation INDEX: unchanged.

## 14. Exact next constitutional act

Following the established BANPU authorization sequence, the exact next
constitutional act is **BANPU-WP4 Work Package Plan**.

That plan must decompose the exact authorized scope, place `MINOR-1` and
`NEW-MINOR-A` at their canonical verification points, preserve the conditional
roadmap §1 reviewer gate for the canonicalizer surface, and carry all inherited
residuals and referred items unchanged. It may not widen this authorization.

This record creates no Work Package Plan and performs no implementation.

## 15. Repository verification

| Verification | Result |
|---|---|
| Allocation Record identity | `EXACT` — 11,180 bytes, 214 lines, SHA-256 `CEE6F01C4113697BE6485AE56BB80FE0E9E99CB8555C08BC5D3E3CD67B94BAA9` |
| Frozen WP3 implementation corpus | `EXACT` — all 9 canonical LF member identities and aggregate `E2C44B920D533D386FE3C470C48A8701806D14BA4C1866A7F9058C700FB0E7B8` recomputed |
| Frozen WP2 implementation content | `EXACT` under the previously accepted LF verification representation — aggregate `6E50F5B5E2AAA008EA1C3DA25D1FC34C41F9CBAE81A293A463FB3F6BF5DA4159` |
| Tracked or staged repository diff before and after this act | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX file modified | `NONE` |
| Frozen artifact modified | `NONE` |
| Trailing-whitespace verification | `PASS` for both additive WP4 records |
| Markdown relative-link target verification | `PASS` — 13 targets checked in this record |
| Markdown fragment-heading verification | `PASS` |
| `git diff --check` | `PASS` |
| `git diff --cached --check` | `PASS` — nothing staged |
| `graphify update .` | `PASS` — code graph rebuilt; no implementation change introduced |
| Final `git status --short --untracked-files=all` | Exactly the additive WP4 Allocation Record and this Authorization Record are untracked |
| Commit created | `NO` |
