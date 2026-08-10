# BANPU-WP2 — Work Package Plan

**Artifact class:** Planning only
**Status:** `PLANNING RC2 — IMPLEMENTATION NOT AUTHORIZED`
**Package boundary:** Replay and independent validator only
**Successor authority created:** `NONE`

## 1. Preconditions and dependencies

- BANPU-WP1 is constitutionally `FROZEN WITH RECORDED RESIDUALS`.
- The exact 12-file WP1 corpus and its aggregate identity remain authoritative.
- The frozen `POSITION_CONVERSION` contract is consumed without amendment.
- M46 implementation remains suspended.
- No persistent conversion row exists in any environment; before WP5 acceptance, conversion rows are permitted only as transient, rollback-isolated fixtures.
- WP2 rebuild evidence is dry-run or `skip_snapshots=True`; no committed full-history conversion rebuild evidence is admissible before WP5.
- The WP2 implementation candidate begins from a recorded repository state with unrelated changes identified and excluded.
- Implementation requires separate authorization; this plan does not provide it.

WP2 depends only on frozen WP1. WP3, WP4, WP5, and later packages are not dependencies and are not authorized to begin.

WP5 retains exclusive ownership of the hard runtime reconstruction boundary.
WP2 adds no interim runtime gate. BANPU remediation governance owns the
procedural sequencing risk until WP5 acceptance, and WP4 acceptance does not
authorize persistent conversion rows or unbounded committed rebuild evidence.

## 2. Task plan

| Task | Work | Dependency | Deliverable/evidence |
|---|---|---|---|
| WP2-T1 | Record baseline, frozen hashes, test commands, M46 no-change evidence, and file allowlist | WP1 freeze | Reproducible entry-gate record |
| WP2-T2 | Add focused immutable fixtures for BANPU and generic arithmetic, cash-in-lieu, basis merge, raw≠canonical validator identity, both rebuilder replay sites, item-ID preservation, conversion-only reconciliation, exact failure disposition, repairs, and same-day ordering | T1 | Failing tests that express the frozen equations and RC2 architecture |
| WP2-T3 | Add rebuilder raw-row preflight owned by `rebuild_portfolio()`, immutable preflight evidence for both replay sites, per-run duplicate tracking, local identity resolution, and consumer-boundary repair preservation | T2 | Controlled fail-closed identity/date/duplicate behavior in both replay runs |
| WP2-T4 | Add rebuilder conversion application at both existing application sites: remove predecessor, create/merge successor, preserve basis, copy complete conversion state, and apply admitted cash and realized P/L | T3 | Equal Stage 1 and terminal Stage 2 state |
| WP2-T5 | Add lossless item asset-ID preservation, authoritative successor binding, conversion-only five-field reconciliation, and Stage 5 blocking | T4 | Deterministic materialization/reconciliation evidence and no invalid commit |
| WP2-T6 | Augment and mutate the validator's authoritative raw-keyed state, add independent candidate construction and conversion application, and emit active WP2 findings | T2 | One coherent independent validator state and deterministic catalog output |
| WP2-T7 | Enforce repair preservation at authorized consumers and prove raw/effective parity without modifying `ledger_repair.py` | T4, T6 | Repair-consistency evidence |
| WP2-T8 | Run parity, regression, boundary, frozen-hash, and graph verification | T5–T7 | Complete WP2 acceptance evidence |
| WP2-T9 | Independent architecture/accounting review and governance decision | T8 | Accepted candidate or returned findings; no successor authorization |

Tasks T3–T5 and T6 are logically separate implementations. They may be reviewed separately, but the package is not acceptable until cross-state-machine parity is proven.

## 3. Expected files

### 3.1 Production files expected to change

- `backend/services/portfolio_rebuilder.py`
- `backend/services/ledger_validator.py`

### 3.2 Conditional production file

- `backend/services/replay_key.py` only if implementation evidence proves a pure conversion-key helper cannot remain package-local without changing existing `replay_key()` semantics. Default decision: do not modify.

Any use of the conditional file requires an architecture review gate before the change. Its public signature and existing three-tier behavior must remain unchanged.

### 3.3 Test files expected to change or be added

- `backend/tests/test_portfolio_rebuilder.py`
- `backend/tests/test_ledger_validator.py`
- `backend/tests/test_replay_key.py` only if `replay_key.py` changes
- `backend/tests/test_repair_validate_consistency.py` only for conversion repair-parity coverage
- `backend/tests/test_position_conversion_replay.py` as the preferred new focused cross-mode fixture suite

### 3.4 Mandatory unchanged regression owners

These suites need not be edited, but they must be run because they own behavior
or public surfaces affected by WP2:

- `backend/tests/test_ledger_validator_effective.py`
- `backend/tests/test_portfolio_rebuilder_capability_shadow.py`
- `backend/tests/test_registry_replay_parity.py`
- `backend/tests/test_replay_cutover.py`

### 3.5 Planning and review artifacts

- `docs/implementation/BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md`
- `docs/implementation/BANPU_WP2_WORK_PACKAGE_PLAN.md`
- `docs/implementation/BANPU_WP2_IMPLEMENTATION_SEQUENCE.md`
- a future WP2 review/acceptance record only if separately requested by governance

## 4. Explicit files prohibited from modification

### 4.1 Frozen WP1 corpus — absolute prohibition

- `backend/models/database.py`
- `backend/services/transaction_canonicalizer.py`
- `backend/migrations/versions/b7d9f1a3c5e7_add_position_conversion_payload.py`
- `backend/tests/test_transaction_canonicalizer.py`
- `backend/tests/test_position_conversion_migration.py`
- `docs/architecture/ARCHITECTURE.md`
- `docs/investment/PORTFOLIO_CALCULATION_RULES.md`
- `docs/implementation/BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`
- `docs/implementation/BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`
- `docs/implementation/BANPU_IMPLEMENTATION_SEQUENCE.md`
- `docs/implementation/BANPU_WP1_CONFIRMATION.md`
- `docs/implementation/BANPU_WP1_FREEZE_READINESS_ASSESSMENT.md`

`docs/implementation/BANPU_WP1_FREEZE_RECORD.md` is also constitutionally immutable even though it is a lifecycle artifact outside the 12-file manifest.

### 4.2 Future-package and out-of-scope production files

- `backend/services/portfolio_transactions.py`
- `backend/services/portfolio_snapshots.py`
- `backend/services/portfolio_metrics.py`
- `backend/services/snapshot_return_recovery.py`
- `backend/services/market_data/yahoo_chart.py`
- `backend/services/data_fetcher.py`
- `backend/services/asset_registry.py`
- `backend/services/asset_repository.py`
- `backend/services/ledger_repair.py`
- `backend/models/asset.py`
- `backend/manage.py`
- `backend/main.py`
- `docs/engineering/DECISION_LOG.md`
- all frontend files
- all shadow, attribution, quant, horizon, optimizer, recommendation, and evaluation production modules
- every `docs/implementation/M46*` file and every M46 implementation file

No new migration, model, table, public endpoint, CLI command, registry primitive, cache namespace, or generic corporate-action module is permitted.

The frozen `docs/architecture/ARCHITECTURE.md` and
`docs/investment/PORTFOLIO_CALCULATION_RULES.md` remain unchanged when WP2 is
accepted even though their activation wording will then require later
synchronization. That synchronization, together with any BANPU business-rule
entry in `docs/engineering/DECISION_LOG.md`, is explicitly deferred to the
separately approved WP8 documentation-correction owner. This deferral does not
authorize WP8 and does not permit a WP2 documentation edit outside the three
planning artifacts.

If implementation appears to require any prohibited file, work stops and returns to architecture/governance review. A reviewer cannot expand the allowlist informally.

## 5. Detailed task acceptance

### WP2-T1 — Baseline

- Frozen file SHA-256 values match the freeze record.
- Existing dirty WP1 files are recognized as the frozen staged corpus and are not edited.
- Baseline test results and any pre-existing failures are recorded.
- No unexplained overlapping user change exists in WP2 files.

### WP2-T2 — Tests first

- Expected values are constructed independently from production helpers.
- At least one valid accounting fixture uses arbitrary non-BANPU identities and facts.
- Ordering fixtures prove affected-asset same-day rejection and unchanged transaction-ID ordering for unrelated assets; no conversion priority is introduced.
- Validator fixtures include a raw ledger symbol different from canonical/payload symbol, candidate union/deduplication, and conflicting asset-ID versus symbol paths in both replay modes.
- Rebuilder fixtures compare Stage 1 final state with terminal Stage 2 per-date state and prove fresh per-run duplicate tracking and complete state copying.
- Materialization fixtures cover every pre-existing item asset ID, successor binding/conflict, and conversion-only five-field reconciliation before and after item-only commit.
- Result fixtures assert exact `success`/`aborted`/`committed` values, and malformed-conversion fixtures assert that `_EQUITY_TYPES` remains unchanged.
- Every active WP2 finding has at least one positive and one non-triggering case.
- Deferred WP3/WP5 finding IDs are asserted as catalogued but no fabricated evidence predicate is introduced; presence in the catalog does not imply runtime production.

### WP2-T3/T4 — Rebuilder

- Controlled failure occurs before persistence for invalid conversions.
- Exactly one predecessor is removed and one successor state remains.
- Existing successor merge proves `combined_basis == existing_basis + converted_basis` and derives average cost from combined basis/shares.
- Both modes and transaction-83 fallback are deterministic.
- No-cash-in-lieu preserves cash and realized P/L.
- Raw-row preflight is performed once before both replay sites; immutable evidence is shared, while replayed-key sets are fresh per run.
- `_PortfolioState.copy()` retains every conversion-relevant field, and Stage 1 final state equals terminal Stage 2 state.

### WP2-T5 — Reconciliation and gate

- Every current item asset ID is preserved through delete-and-reinsert: unaffected values remain exact, an already-correct successor ID remains exact, and only a successor `NULL` is enriched to the payload ID.
- The surrendered predecessor is intentionally not reinserted and its asset ID is never transferred to another item.
- Successor materialization rejects a conflicting non-null ID and performs no registry lookup or identity backfill.
- Conversion-successor pairing uses asset-ID precedence, unique canonical-symbol fallback, and fail-closed ambiguity; five comparison fields are independently visible.
- Pre-commit null successor ID is `DIFFERENT`; after item-only commit all five successor fields are `MATCH`. Ordinary item reconciliation remains unchanged.
- Every CRITICAL conversion finding and `POSITION_CONVERSION_SAME_DAY_CONFLICT` blocks commit.
- Unrelated `ERROR` findings retain current Stage 5 behavior.

### WP2-T6 — Independent validator

- Validator retains and mutates one authoritative raw-keyed state, augmented with conversion identity/basis metadata; no parallel conversion state exists.
- Legacy candidates use canonical metadata over actual raw keys; native candidates union asset-ID and canonical-fallback matches, deduplicate by actual holding, and fail on ambiguity.
- Predecessor removal and successor creation/merge are visible to existing sell, cash, holdings-consistency, and snapshot-cash checks.
- Validator imports no rebuilder state, identity helper, or mutation.
- Validator uses exact basis arithmetic for conversion portfolios.
- Finding IDs, severities, transaction IDs, symbols, and details are deterministic.
- No-conversion validation output remains unchanged.

### WP2-T7 — Repair boundary

- Conversion rows are identical in raw/effective validation.
- `apply_repairs=True` and `False` cannot remove or alter conversion accounting.
- An `EXCLUDE` repair targeting a conversion is ineffective and emits no new finding merely because the ineffective repair exists; `SUPPRESS_FINDING` cannot suppress a conversion finding.
- No conversion-specific `LedgerRepair` behavior is added.

### WP2-T8/T9 — Closure

- All acceptance criteria in the implementation specification pass.
- File-boundary and frozen-hash audits pass.
- Graph is current.
- All conversion rows in evidence are transient and rollback-isolated; all rebuild evidence is dry-run or `skip_snapshots=True`, with no committed full-history conversion rebuild before WP5.
- Independent review confirms accounting, identity, validator independence, and future-package boundaries.
- Closure grants no WP3 authority.

## 6. Verification matrix

| Concern | Focused verification | Regression verification |
|---|---|---|
| Accounting | BANPU, generic, and CIL exact-Decimal fixtures | Existing BUY/SELL/initial/correction replay |
| Ordering | Affected-asset same-day rejection; unrelated-asset transaction-ID order; no conversion priority | Existing canonical ordering tests |
| Identity | Legacy/native/null-asset/raw≠canonical/candidate-union/ambiguous cases | Existing replay-key and replay-cutover suites |
| Basis merge | Existing-successor `old_basis + converted_basis` invariant | Existing avg-cost reconciliation tests |
| Dual replay sites | Stage 1 versus terminal Stage 2 equality; copy and per-run duplicate state | Existing portfolio-rebuilder suite |
| Validator | One authoritative raw-keyed state, one fixture per active finding, and clean parity | Ledger-validator and effective-validator suites |
| Stage 5 | CRITICAL and same-day blocking tests | Existing error/warning gate behavior |
| Repairs | Conversion cannot be excluded/suppressed at consumer boundaries | Repair-validation consistency and effective-validator suites |
| Materialization | All reinserted item IDs preserved; predecessor ID not transferred; successor bind/conflict; conversion-only five-field pre/post commit | Existing dry-run/commit planning tests and registry-parity suite |
| Compatibility | No-conversion golden outputs | Rebuilder, validator, capability-shadow, registry-parity, and replay-cutover suites |
| Governance | Frozen hashes, diff allowlist, transient rows, and no committed full-history evidence | M46 no-change, WP5-ownership, deferred-doc, and graph audit |

Suggested command set:

```text
pytest backend/tests/test_position_conversion_replay.py
pytest backend/tests/test_portfolio_rebuilder.py
pytest backend/tests/test_ledger_validator.py
pytest backend/tests/test_replay_key.py
pytest backend/tests/test_repair_validate_consistency.py
pytest backend/tests/test_ledger_validator_effective.py
pytest backend/tests/test_portfolio_rebuilder_capability_shadow.py
pytest backend/tests/test_registry_replay_parity.py
pytest backend/tests/test_replay_cutover.py
pytest backend/tests/test_transaction_canonicalizer.py
pytest backend/tests/test_position_conversion_migration.py
graphify update .
```

The focused-file command is omitted if coverage is intentionally kept in existing test files.

## 7. Review gates

### Gate 1 — Entry authority

- Separate WP2 implementation authorization exists.
- WP1 freeze identity passes.
- Scope and file allowlist are acknowledged.

### Gate 2 — Rebuilder accounting review

- Exact equations, identity fallback, duplicate defense, successor merge, dual replay-site parity, item-ID preservation, conversion-only reconciliation, result disposition, and failure atomicity pass.
- No frozen or future-package code is present.

### Gate 3 — Validator independence review

- One augmented authoritative raw-keyed state is mutated; no parallel state and no rebuilder state/helper reuse exist.
- Candidate construction, union, deduplication, ambiguity, predecessor removal, successor create/merge, and existing-check integration pass.
- Finding predicates and severities match the canonical design.
- Deferred WP3/WP5 predicates remain outside WP2.

### Gate 4 — Compatibility review

- No-conversion and unaffected-asset behavior is unchanged.
- Repair, effective-validator, capability-shadow, registry-parity, replay-cutover, replay-key, and Stage 5 regression evidence passes.
- All conversion evidence is transient and uses dry-run or `skip_snapshots=True`; no committed full-history conversion rebuild is accepted before WP5.

### Gate 5 — Constitutional acceptance

- Complete verification evidence is reproducible.
- Diff is allowlisted; frozen hashes and M46 state are unchanged.
- Residual register is unchanged.
- WP3+ ownership is unchanged, the WP5 runtime boundary remains dormant in WP2, and deferred documentation is assigned to the separately approved WP8 correction owner without authorizing WP8.
- WP2 may be accepted or returned for correction. Acceptance does not authorize WP3, deployment, or production mutation.

## 8. Rollback plan

Before any future conversion authoring is enabled, WP2 rollback is the coordinated removal/revert of WP2 production and test changes. The frozen additive WP1 schema remains in place and is not downgraded or amended.

Rollback triggers include:

- frozen hash mismatch;
- unexpected no-conversion replay or validator drift;
- rebuilder/validator economic divergence;
- ambiguous identity being resolved heuristically;
- invalid conversion reaching a commit path;
- conversion being suppressible by repairs;
- prohibited-file or future-package scope leakage;
- validator dependence on rebuilder mutation;
- a second validator conversion state;
- Stage 1/Stage 2 conversion divergence or incomplete copied state;
- loss of any pre-existing item asset ID, successor identity conflict, or registry/backfill access;
- ambiguous conversion-successor reconciliation being resolved heuristically;
- persistent pre-WP5 conversion state or committed full-history conversion rebuild evidence; or
- unauthorized edits to deferred architecture, calculation-rule, or decision-log documentation.

No manual ledger edit, row deletion, migration downgrade, production restore, or compensating transaction is authorized by WP2 planning.
