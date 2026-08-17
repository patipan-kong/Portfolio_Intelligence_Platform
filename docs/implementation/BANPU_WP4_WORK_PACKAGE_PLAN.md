# BANPU-WP4 — Work Package Plan

**Artifact class:** Implementation planning only
**Status:** `WORK PACKAGE PLAN MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN`
**Plan date:** 2026-08-11
**Issuing role:** BANPU-WP4 Work Package Planning Authority
**Work package:** `BANPU-WP4 — Registry preparation and live materialization`
**Authority:** [BANPU-WP4 Implementation Authorization Record](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md), disposition `BANPU-WP4 IMPLEMENTATION AUTHORIZED`, over the scope bound by [BANPU-WP4 Allocation Record](BANPU_WP4_ALLOCATION_RECORD.md)
**MINOR-1 disposition in this plan:** `BLOCKED AT THE CONDITIONAL BOUNDARY — ROADMAP §1 REVIEWER CONFIRMATION REQUIRED`
**Successor authority created:** `NONE`
**Release/deployment authority created:** `NONE`

This plan decomposes already-authorized implementation authority. It performs no
implementation. It creates no authority, no new gate, no new acceptance
criterion, no new capability, and no file surface beyond the surface the
Implementation Authorization Record already bound. Where this plan and the
frozen canonical corpus differ, the frozen corpus governs and this plan is in
error.

## 1. Objective and scope boundary

### 1.1 Objective

Add the only authorized atomic write path for `POSITION_CONVERSION` after safe
replay (WP2) and quote-epoch binding (WP3) exist, and prepare the registry
identity state that the write path validates. Operator access remains
service-only.

### 1.2 Authorized capabilities — preserved exactly

WP4 implementation covers exactly these capabilities and nothing else:

| ID | Authorized capability |
|---|---|
| C-1 | Minimal predecessor-identifier retirement support, if required |
| C-2 | Validation of successor `Asset`, current provider identifier, predecessor status, and the `MERGED_INTO` relationship |
| C-3 | `execute_position_conversion()` |
| C-4 | Portfolio and relevant-item locking |
| C-5 | Optimistic quantity and basis assertions |
| C-6 | Canonical-fingerprint idempotency |
| C-7 | Append-only conversion transaction insertion |
| C-8 | Predecessor removal or transformation |
| C-9 | Successor creation or merge |
| C-10 | Optional cash-in-lieu materialization |
| C-11 | Final shares/basis/cash/identity assertions |
| C-12 | One atomic database transaction covering C-4 through C-11 |
| C-13 | Service-only internal access |

Symbols and provider identifiers are registry-resolved, never trusted from
arbitrary input strings. The successor remains a distinct `Asset`; the
predecessor is not renamed. The ratio lives only in the transaction payload.

### 1.3 Scope boundary — excluded from WP4

WP4 implementation does not add, and this plan does not decompose:

- any CLI command or `backend/manage.py` change (operator wiring is WP7 work);
- any public endpoint or `backend/main.py` transaction-endpoint change;
- any frontend authoring path;
- any schema, model, or migration change;
- any `LedgerRepair` conversion behavior;
- any general corporate-action framework, dispatcher, or event vocabulary;
- any production execution, production-data mutation, or cache purge;
- any snapshot rebuild, shadow regeneration, or reader/accounting change
  (WP5/WP6 ownership); and
- any WP5+ or M46 work.

### 1.4 Inherited constraint carried from the frozen WP2 planning corpus

[BANPU-WP2 Work Package Plan](BANPU_WP2_WORK_PACKAGE_PLAN.md) §1 records, and
this plan carries unchanged, that no persistent conversion row exists in any
environment and that before WP5 acceptance conversion rows are permitted only as
transient, rollback-isolated fixtures, with rebuild evidence dry-run or
`skip_snapshots=True`. WP4 acceptance authorizes neither persistent conversion
rows nor committed full-history conversion rebuild evidence. All WP4 evidence in
§6 is produced under that constraint.

### 1.5 Planning determinations

These are readings of the canonical corpus recorded for reviewer inspection.
They amend nothing and are subordinate to the frozen corpus.

| ID | Determination | Canonical basis |
|---|---|---|
| PD-WP4-1 | Registry preparation is a distinct, idempotent service act performed **before** the conversion call. `execute_position_conversion()` validates registry invariants and fails closed; it never performs preparation implicitly. | Design §9 in-transaction list contains "resolve and validate", not "prepare"; §13 step 3 and §14 step 6 place preparation ahead of conversion (§14 step 11) |
| PD-WP4-2 | `backend/services/asset_repository.py` is planned as **not modified**. The repository primitive `mark_identifier_not_current()` already exists; the missing capability is a service-level retirement operation belonging in `asset_registry.py`. The conditional repository file remains available under §2.1 if implementation proves a primitive is genuinely absent. | Roadmap §6 and Authorization §4.1 admit the repository file "only for the minimal identifier-retirement operation" |
| PD-WP4-3 | `MINOR-1` cannot be satisfied inside the §2.1 production surface. See §4. | Fingerprint serialization is produced entirely inside the frozen canonicalizer |
| PD-WP4-4 | WP4 test evidence executes on the repository's test database path and therefore proves that locking is issued over the authorized rows and that the optimistic assertions fail closed; it does not prove production-dialect row-lock semantics. This plan records that limitation as a WP4 evidence note and **assigns it to no other package**. | Sequence §1 and Authorization §9; no canonical artifact assigns lock-dialect proof elsewhere |

## 2. Authorized implementation surface

No file outside this section may be modified by WP4 implementation.

### 2.1 Production surface (authorized)

| File | Planned WP4 change | Capabilities |
|---|---|---|
| `backend/services/portfolio_transactions.py` | Add `execute_position_conversion()` and its private helpers | C-3 to C-13 |
| `backend/services/asset_registry.py` | Add the minimal service-level predecessor-identifier retirement operation and the conversion registry-invariant validation used by C-2; reuse the existing `transition_status()` and `link_relationship()` behavior unchanged | C-1, C-2 |
| `backend/services/asset_repository.py` | **Planned: no change** (PD-WP4-2). Admitted only for the minimal identifier-retirement primitive if implementation proves one is absent | C-1 |

### 2.2 Test surface (authorized)

| File | Role |
|---|---|
| `backend/tests/test_position_conversion_live.py` | Preferred new focused live-conversion module (the Authorization §4.2 "one new focused live-conversion test module" option) |
| `backend/tests/test_portfolio_transactions_capability_shadow.py` | Alternative locus if the reviewer prefers coverage in the existing module; used for capability-shadow non-regression either way |
| `backend/tests/test_asset_registry.py` | Registry preparation, retirement, status, and `MERGED_INTO` validation cases |
| `backend/tests/test_registry_service.py` | Alternative registry locus permitted by Authorization §4.2 |
| Additional focused tests | Only where strictly necessary to prove an authorized WP4 verification obligation in §6, and only without introducing another production capability |

### 2.3 Conditional surface — not presently implementation-editable

- `backend/services/transaction_canonicalizer.py`
- `backend/tests/test_transaction_canonicalizer.py`

These files are **NOT** implementation-editable under this plan. Any edit
requires prior roadmap §1 reviewer confirmation of strict necessity, limited
solely to the minimal `MINOR-1` precision correction and its required vectors.
This plan does not grant that confirmation and does not make these files
editable. See §4.

### 2.4 Explicit no-change surface (canonical, restated as scope evidence)

`backend/models/asset.py`; `backend/services/ledger_repair.py`;
`backend/models/database.py` except the changes already accepted in WP1;
`backend/main.py` transaction endpoints; all frontend files; `backend/manage.py`;
all WP2/WP3 production modules accepted under their own packages; every frozen
BANPU governance artifact; and all M46 files.

## 3. Implementation decomposition and order

### 3.1 Task sequence (dependency-ordered)

| Task | Work | Depends on | Deliverable / evidence |
|---|---|---|---|
| WP4-T1 | Record entry baseline: repository state, frozen WP1/WP2/WP3 identities, test commands, pre-existing failures, and the §2 file allowlist | Authorization | Reproducible entry-gate record |
| WP4-T2 | Author failing focused tests for registry preparation, retirement, status transition, and `MERGED_INTO` validation (C-1, C-2) | T1 | Registry obligations expressed before code |
| WP4-T3 | Implement the minimal service-level identifier retirement and the conversion registry-invariant validator in `asset_registry.py` | T2 | Idempotent, fail-closed registry preparation and validation |
| WP4-T4 | Author failing focused tests for the live conversion: success, existing-successor merge, no-CIL, CIL, stale quantity, stale basis, registry mismatches, `MERGED_INTO` mismatch, forced rollback, atomicity, ledger preservation | T1 | Verification matrix §6 rows LM-1 … LM-13 expressed before code |
| WP4-T5 | Author failing `NEW-MINOR-A` authoring/date tests (§5) | T1 | Rows NMA-1 … NMA-4 expressed before code |
| WP4-T6 | Implement `execute_position_conversion()` through the runtime order in §3.2, with the fingerprint idempotency branch present but **inert** behind the `MINOR-1` pre-use gate | T3, T4, T5 | Atomic conversion service; no active fingerprint idempotency |
| WP4-T7 | **Conditional / blocked.** Assemble and submit the `MINOR-1` reviewer-confirmation evidence package defined in §4.4 | T6 | Reviewer submission; no code edit performed |
| WP4-T8 | **Conditional / blocked until T7 is confirmed by the roadmap §1 reviewer.** Apply the minimal `MINOR-1` precision correction and its vectors, then activate fingerprint idempotency | T7 confirmation | Rows M1-1 … M1-4 and rows LM-14/LM-15 (retry/conflict) |
| WP4-T9 | Prove live-versus-replay outcome equality against the frozen WP2 replay path under transient, rollback-isolated fixtures | T6, T8 | Row EQ-1 |
| WP4-T10 | Run the full §6 matrix and the §6.3 regression suites; run boundary/diff and graph verification | T8, T9 | Complete WP4 evidence set |
| WP4-T11 | Prepare the independent implementation-review submission | T10 | Review-ready candidate; no confirmation, freeze, or closeout performed |

Tasks T7 and T8 are the only tasks that touch the conditional surface. They are
stopped at the boundary by this plan. All other tasks proceed under the existing
authorization. WP4 cannot reach its exit criteria (§9) while T7/T8 remain
unconfirmed, because C-6 is a mandatory authorized capability.

### 3.2 Runtime order inside `execute_position_conversion()`

Registry preparation (E0) is a separate service act performed before the call
(PD-WP4-1). Steps E1 to E13 execute inside exactly one database transaction.

| Step | Action | Notes |
|---|---|---|
| E0 | **Registry preparation** — establish the current successor `PROVIDER_SYMBOL`, retire the predecessor identifier (`is_current=False`), transition the predecessor to `MERGED`, and create the `MERGED_INTO` relationship. Idempotent and repeatable | Outside the conversion transaction; performed by `asset_registry.py` |
| E1 | **Open the single transaction scope.** No intermediate `db.commit()` occurs anywhere between E1 and E13 | Distinguishes this service from the existing per-call-commit executors in the same module |
| E2 | **Acquire locks** on the portfolio row and the relevant `PortfolioItem` rows (predecessor and successor) | C-4; PD-WP4-4 limitation applies |
| E3 | **Validate registry invariants**: successor `Asset` exists and is distinct; successor current provider identifier is present and current; predecessor status is `MERGED`; predecessor identifier is retired; exactly one `MERGED_INTO` edge links predecessor to successor; predecessor is not renamed. Any failure aborts before any write | C-2; fail-closed |
| E4 | **Resolve conversion inputs**: symbols and provider identifiers from the registry; decimals from the caller's typed facts; `transaction_date` constructed solely from the payload's timezone-free `valuation_transition_date` as naive midnight (§5). Parse the assembled payload through the frozen canonicalizer and require a clean typed `PositionConversion` | C-7 input contract; `NEW-MINOR-A` |
| E5 | **Locate the predecessor holding** by asset ID with the controlled legacy-symbol fallback; zero or multiple matches fail closed | Design §9.3, §8.3 |
| E6 | **Check optimistic expectations**: expected predecessor quantity and expected basis must match the located holding within the canonical tolerances. Mismatch aborts | C-5 |
| E7 | **`MINOR-1` pre-use gate.** Fingerprint idempotency may not execute unless the `MINOR-1` obligation is complete. Until then the service refuses to proceed past this step rather than using an unproven fingerprint | §4; mandatory pre-use gate |
| E8 | **Evaluate idempotency**: an identical canonical fingerprint returns `already_applied` as a no-op with no write; a conflicting fingerprint for the same portfolio/predecessor/transition date is a hard failure | C-6 |
| E9 | **Insert the append-only conversion transaction row** | C-7; never an edit or replacement |
| E10 | **Transform predecessor state**: remove or transform the predecessor materialization | C-8 |
| E11 | **Create or merge the successor position**: combined shares and combined basis; average cost derived from combined basis over combined shares; carry the sector; bind the successor identity | C-9 |
| E12 | **Materialize cash-in-lieu when admitted**: add only admitted net cash `Cn` and realized P/L `RP`. Without cash-in-lieu, cash and realized P/L are unchanged | C-10 |
| E13 | **Assert final invariants** — shares, basis, cash, and identity — then commit. Any failure at any step from E1 rolls the entire unit back, leaving no transaction row and no materialized state | C-11, C-12 |

Ordering rules that implementation may not relax:

1. E7 precedes E8. Fingerprint idempotency must not become active before
   `MINOR-1` is satisfied.
2. E3 and E6 precede every write. No row is inserted or mutated before
   registry invariants and optimistic expectations pass.
3. E9 precedes E10 to E12, and all of them share the E1 transaction scope.
4. E13 is the only commit boundary. There is no partial-success outcome.

## 4. `MINOR-1` plan

### 4.1 Obligation carried unchanged

`MINOR-1` records that fingerprint serialization can lose distinctions beyond
the default `Decimal` context precision. Its canonical verification point is
**before `execute_position_conversion()` uses the fingerprint for idempotency**.
It is a mandatory implementation-time pre-use gate, not a pre-authorization
gate, and it is also an exit/confirmation evidence obligation. This plan changes
none of that.

### 4.2 Determination — can the authorized surface satisfy it?

**No.** The determination is `MINOR-1 CANNOT BE SATISFIED WITHIN THE §2.1
PRODUCTION SURFACE`.

Exact minimal reason: the canonical fingerprint is produced entirely inside
`backend/services/transaction_canonicalizer.py`. Its decimal serialization step
normalizes each parsed `Decimal` under the ambient decimal context, so two
payload values that parse to distinct exact `Decimal` values but differ only
beyond 28 significant digits serialize to the same canonical string and hash to
the same fingerprint. No file in §2.1 participates in that serialization, so no
change inside §2.1 can make the two payloads produce distinct fingerprints.

A non-committed read-only probe run during planning confirms the mechanism:
parsed values remain distinct, while their normalized serializations are equal.
No file was modified to obtain it.

Two alternatives were considered and are **not** planned:

- computing a second, WP4-local fingerprint inside
  `portfolio_transactions.py` — rejected: it would create a competing canonical
  identity for a contract the canonical design assigns solely to
  canonicalization, and it is not among the authorized capabilities in §1.2; and
- rejecting high-significand payloads at the service boundary — rejected: it
  would narrow the frozen WP1 payload contract, which admits any finite base-10
  decimal string, and it is a refusal rather than the precision improvement the
  canonical residual register describes.

### 4.3 Consequence for this plan

Planning **STOPS** at the conditional boundary for that portion of the work:

- tasks WP4-T7 and WP4-T8 are recorded as blocked;
- `backend/services/transaction_canonicalizer.py` and
  `backend/tests/test_transaction_canonicalizer.py` remain **not**
  implementation-editable;
- this plan does **not** grant roadmap §1 reviewer confirmation and has no
  authority to do so;
- fingerprint idempotency (C-6, step E8) remains inert until confirmation is
  recorded and the correction is complete; and
- WP4 may not be confirmed, frozen, or closed while this remains open.

### 4.4 Evidence required for roadmap §1 reviewer confirmation

The reviewer confirmation submission (WP4-T7) must contain:

1. the exact defect locus and mechanism inside the canonicalizer's decimal
   serialization, with the reproducible non-committed probe;
2. proof that no §2.1 file participates in canonical fingerprint serialization;
3. the two rejected alternatives in §4.2 with their reasons;
4. the exact minimal proposed correction, bounded to context-independent decimal
   serialization, with no other canonicalizer behavior changed and no payload
   contract change;
5. the exact test vectors to be added and the assertion that no existing frozen
   canonicalizer vector changes its expected value; and
6. a statement that the confirmation is requested solely for `MINOR-1` and
   authorizes no other WP1 change.

### 4.5 Required eventual `MINOR-1` evidence (unchanged)

- distinct payload fingerprint vectors with values differing beyond 28
  significant digits;
- retry behavior for identical canonical payloads;
- conflict behavior for distinct payloads; and
- proof that distinct payloads cannot collide because of `Decimal` precision
  serialization.

No `MINOR-1` test is authored before confirmation. The pre-confirmation artifact
is the non-committed evidence probe in the submission, not a committed test.

## 5. `NEW-MINOR-A` plan

### 5.1 Obligation carried unchanged

WP4 must construct `transaction_date` only from the payload's timezone-free date
as a naive-midnight typed value. The later real-PostgreSQL coercion and
stored-invariant probes remain assigned to WP7, and release evidence remains
with WP8. This plan pulls neither into WP4.

### 5.2 Implementation obligations (in `portfolio_transactions.py`, step E4)

| ID | Obligation |
|---|---|
| NMA-I1 | The service exposes no caller-supplied `transaction_date` parameter for the conversion. The value is derived solely from the payload's `dates.valuation_transition_date` |
| NMA-I2 | The derived value is a canonical naive-midnight typed construction: `tzinfo is None`, time component exactly `00:00:00`, date equal to the payload calendar date |
| NMA-I3 | Offset-bearing authoring inputs are rejected before insertion — a timezone-aware `datetime`, an offset-bearing or time-bearing date string, or any non-midnight time component fails closed with a structured error and no write |
| NMA-I4 | Database-session, host-timezone, UTC, and offset conversion do not participate in the interpretation of the value |

### 5.3 Test obligations (in the §2.2 live-conversion module)

| ID | Case | Expected |
|---|---|---|
| NMA-1 | Valid timezone-free payload date | Inserted `transaction_date` is naive, midnight, and equal to the payload calendar date |
| NMA-2 | Offset-bearing date string in the payload | Rejected before insertion; no transaction row and no materialized state |
| NMA-3 | Timezone-aware or non-midnight authoring input offered to the service | Rejected before insertion; no partial write |
| NMA-4 | Payload/date equality proof | Stored value equals the payload's timezone-free ISO calendar date under direct comparison, independent of session or host timezone |

## 6. Mandatory verification matrix

### 6.1 Live materialization and registry

| ID | Case | Locus |
|---|---|---|
| LM-1 | Successful conversion | live module |
| LM-2 | Existing-successor merge: combined shares and `existing_basis + carried_basis`; average cost from combined values | live module |
| LM-3 | No-CIL conversion: cash and realized P/L unchanged | live module |
| LM-4 | CIL conversion: only admitted `Cn` and `RP` applied; fees and taxes exactly once | live module |
| LM-5 | Stale quantity expectation | live module |
| LM-6 | Stale basis expectation | live module |
| LM-7 | Successor registry mismatch (missing successor, non-current or absent provider identifier, non-distinct asset) | registry + live modules |
| LM-8 | Predecessor registry mismatch / status mismatch (identifier not retired, status not `MERGED`) | registry + live modules |
| LM-9 | `MERGED_INTO` mismatch (absent, reversed, or pointing elsewhere) | registry + live modules |
| LM-10 | Forced database-session rollback | live module |
| LM-11 | Atomicity of transaction row + materialized state (no row without state, no state without row) | live module |
| LM-12 | Preservation of transaction 83 and all prior ledger rows | live module |
| LM-13 | No public endpoint or frontend authoring path exists for conversions | live module (surface assertion) |
| LM-14 | Matching retry → `already_applied` no-op | blocked on §4 |
| LM-15 | Conflicting retry → hard fail | blocked on §4 |

### 6.2 Residual, parity, and gate rows

| ID | Case | Locus |
|---|---|---|
| EQ-1 | Live outcome equals frozen WP2 replay outcome (shares, basis, cash, realized P/L, successor identity) under transient rollback-isolated fixtures with dry-run or `skip_snapshots=True` | live module |
| NMA-1 … NMA-4 | `NEW-MINOR-A` authoring/date cases (§5.3) | live module |
| M1-1 | Distinct payload vectors beyond 28 significant digits produce distinct fingerprints | conditional surface — blocked on §4 |
| M1-2 | Identical canonical payload retry is a no-op at the canonical verification point | blocked on §4 |
| M1-3 | Distinct canonical payload conflict fails hard at the canonical verification point | blocked on §4 |
| M1-4 | Precision/collision proof: distinct payloads cannot collide because of `Decimal` precision serialization | blocked on §4 |

Rows LM-14, LM-15 and M1-1 … M1-4 are the only matrix rows blocked at the
conditional boundary. Every other row is executable under current authority.

### 6.3 Existing regression suites that must remain green

- `backend/tests/test_portfolio_transactions_capability_shadow.py`
- `backend/tests/test_write_path_asset_id.py`
- `backend/tests/test_fee_accounting.py`
- `backend/tests/test_fee_quote_m32_1.py`
- `backend/tests/test_transaction_symbol_normalization.py`
- `backend/tests/test_asset_registry.py`
- `backend/tests/test_asset_registry_enforcement.py`
- `backend/tests/test_asset_registry_runtime_consultation.py`
- `backend/tests/test_registry_service.py`
- `backend/tests/test_registry_lookup.py`
- `backend/tests/test_registry_replay_parity.py`
- `backend/tests/test_transaction_canonicalizer.py`
- `backend/tests/test_position_conversion_migration.py`
- `backend/tests/test_position_conversion_replay.py`
- `backend/tests/test_position_conversion_quote_contract.py`
- `backend/tests/test_portfolio_rebuilder.py`
- `backend/tests/test_ledger_validator.py`

Suggested command set:

```text
pytest backend/tests/test_position_conversion_live.py
pytest backend/tests/test_asset_registry.py
pytest backend/tests/test_registry_service.py
pytest backend/tests/test_portfolio_transactions_capability_shadow.py
pytest backend/tests/test_write_path_asset_id.py
pytest backend/tests/test_fee_accounting.py
pytest backend/tests/test_fee_quote_m32_1.py
pytest backend/tests/test_transaction_symbol_normalization.py
pytest backend/tests/test_asset_registry_enforcement.py
pytest backend/tests/test_asset_registry_runtime_consultation.py
pytest backend/tests/test_registry_lookup.py
pytest backend/tests/test_registry_replay_parity.py
pytest backend/tests/test_transaction_canonicalizer.py
pytest backend/tests/test_position_conversion_migration.py
pytest backend/tests/test_position_conversion_replay.py
pytest backend/tests/test_position_conversion_quote_contract.py
pytest backend/tests/test_portfolio_rebuilder.py
pytest backend/tests/test_ledger_validator.py
graphify update .
```

## 7. Inherited residuals

Carried unchanged, without definition, resolution, waiver, reinterpretation, or
invented obligation text:

| Item | Carried state |
|---|---|
| WP1 `MINOR-2` | Remaining mechanical-tolerance obligation belongs to WP5; untouched by WP4 |
| WP1 `MINOR-5` | Assigned to WP7 rehearsal and WP8 release evidence; untouched by WP4 |
| WP1 `backend/models/database.py` identity residual | Carried unchanged; WP4 modifies no schema or model |
| Historical WP2 Step 8 gate language | Carried unchanged as recorded |
| WP2 `MINOR-A`, `MINOR-B`, `OBSERVATION-A` … `OBSERVATION-E` | Inherited unchanged. The repository carries these identifiers without accompanying obligation text; this plan neither invents obligation text nor infers a blocker from its absence |
| WP3 `R6` | Carried unchanged under its separately governed documentation-correction status |
| WP3 `R7` waiver | WP3-scoped; creates no relief or precedent for WP4 |
| WP3 non-blocking closeout observations | Carried unchanged; recorded as gating nothing |
| WP3 `PD-3` emitter-locus referral | Belongs to the authority governing the canonical design, roadmap, and package inventory. No WP4 acceptance criterion depends on it |

WP4-owned open items remain exactly `MINOR-1` (§4) and `NEW-MINOR-A` (§5).

## 8. Explicit prohibitions

WP4 implementation may **not**:

- mutate production data;
- execute a BANPU conversion against production;
- rebuild or rewrite a production snapshot;
- purge production cache;
- modify transaction 83 or any historical ledger row;
- add a CLI command, public endpoint, or frontend authoring path;
- expand into BANPU-WP5 or any later package, or into M46;
- modify any frozen governance artifact;
- edit the §2.3 conditional surface before roadmap §1 reviewer confirmation;
- add a schema, model, or migration change;
- add `LedgerRepair` conversion behavior or a general corporate-action framework;
- leave a persistent conversion row or produce committed full-history conversion
  rebuild evidence (§1.4); or
- stage, commit, push, merge, or publish repository changes under color of this
  plan.

## 9. Acceptance and exit criteria

WP4 may enter independent implementation review only when all of the following
hold:

1. every authorized capability C-1 … C-13 is implemented within §2 and nothing
   outside §2 is modified;
2. the §3.2 runtime order holds, including the E7-before-E8 rule and the single
   commit boundary at E13;
3. `MINOR-1` is complete at its canonical pre-use verification point: reviewer
   confirmation recorded, the minimal correction applied within the confirmed
   bound, and rows M1-1 … M1-4 plus LM-14/LM-15 green;
4. `NEW-MINOR-A` is complete: obligations NMA-I1 … NMA-I4 implemented and rows
   NMA-1 … NMA-4 green;
5. the full §6.1 and §6.2 verification matrix is green with no row waived,
   deferred, or substituted;
6. every §6.3 regression suite is green, with pre-existing failures recorded
   against the T1 baseline;
7. live outcome equals frozen WP2 replay outcome (EQ-1);
8. no public endpoint or frontend authoring path exists (LM-13), and the service
   remains reachable only by direct internal invocation;
9. transaction 83 and all prior ledger rows are provably untouched (LM-12);
10. all conversion evidence is transient and rollback-isolated per §1.4;
11. the diff is allowlisted to §2, frozen WP1/WP2/WP3 identities and M46 state
    are unchanged, and `graphify update .` has been run; and
12. all §7 residuals are carried unchanged and no §8 prohibition was breached.

A failed criterion returns work to WP4; no later package may compensate for it.

This plan authorizes **no** confirmation, freeze, closeout, release,
deployment, or production execution. Satisfying these criteria makes WP4
review-ready and nothing more.

## 10. Repository verification of this planning act

| Verification | Result |
|---|---|
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP4_WORK_PACKAGE_PLAN.md` |
| Allocation Record or Implementation Authorization Record modified | `NONE` |
| Frozen BANPU artifacts modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX files modified | `NONE` |
| Conditional §2.3 surface modified | `NONE` |
| Trailing-whitespace verification | `PASS` |
| Markdown relative-link target verification | `PASS` — 3 relative links, all resolving to existing sibling artifacts |
| Markdown fragment-heading verification | `PASS` — no fragment links used |
| `git diff --check` | `PASS` |
| `git diff --cached --check` | `PASS` — nothing staged |
| `graphify update .` | `PASS` — code graph rebuilt; no implementation change introduced |
| Final `git status --short --untracked-files=all` | Exactly the two additive WP4 constitutional records and this plan are untracked |
| Commit created | `NO` |

## 11. Exact next constitutional act

The exact next constitutional act is **roadmap §1 reviewer confirmation of
strict necessity for the conditional `MINOR-1` canonicalizer surface**, on the
evidence package defined in §4.4, performed by a competent reviewer other than
this planning authority.

Until that act occurs, WP4 implementation may proceed only on tasks WP4-T1
through WP4-T6 and WP4-T9 (partially, excluding fingerprint-dependent
assertions), and WP4 cannot reach its §9 exit criteria.

This plan performs no implementation, grants no confirmation, and creates no
successor authority.
