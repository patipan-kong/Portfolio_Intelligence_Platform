# BANPU Remediation — Work Package Roadmap

**Status:** APPROVED IMPLEMENTATION ROADMAP
**Authority:** `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`
**Delivery class:** Independent production incident remediation
**Implementation state:** BANPU-WP1 implementation complete; independently approved and confirmed with recorded residuals; freeze pending; BANPU-WP2 blocked

This roadmap decomposes the approved design into small, independently reviewable work packages. It does not authorize implementation by itself and cannot change the canonical design.

## 1. Universal package rules

- Packages execute in the order defined by `BANPU_IMPLEMENTATION_SEQUENCE.md`.
- A package does not begin until its predecessor is accepted.
- Every package includes focused tests for its own behavior.
- Existing transaction behavior must remain bit-compatible unless the canonical design explicitly says otherwise.
- No package may modify M46, create a general corporate-action framework, or place conversion accounting in `LedgerRepair`.
- Production data execution is not part of a code work package; it occurs only after all packages and release gates pass.
- “Expected files” is a bounded forecast. Adding another production file requires reviewer confirmation that it is strictly necessary under the canonical design.

## 2. Package inventory

| Package | Name | Depends on | Implementation size | Review size |
|---|---|---|---:|---:|
| BANPU-WP1 | Persistence and canonical contract | None | S | S |
| BANPU-WP2 | Replay and independent validator | WP1 | M | M |
| BANPU-WP3 | Quote identity and epoch protection | WP1 | M | M |
| BANPU-WP4 | Registry preparation and live materialization | WP1–WP3 | M | M |
| BANPU-WP5 | Accounting readers and bounded reconstruction | WP2–WP4 | M | M |
| BANPU-WP6 | Shadow and succession-aware time-series continuity | WP3–WP5 | M | M |
| BANPU-WP7 | Operator command and migration rehearsal | WP1–WP6 | S | M |
| BANPU-WP8 | Integrated regression and release evidence | WP1–WP7 | M | L |

Size guide: S = localized change and focused tests; M = several cooperating modules; L = broad verification or cross-domain review. Estimates are relative, not schedules.

## 3. BANPU-WP1 — Persistence and canonical contract

### Purpose

Establish the additive schema and pure typed representation required by every later package.

### Scope

- Add nullable `transactions.conversion_payload`.
- Add the conversion-only partial unique index and the conversion-specific predecessor-identity/naive-midnight constraint that makes its transition-calendar-date key canonical.
- Add ORM and SQLite compatibility support.
- Define immutable typed payload values and exact decimal parsing.
- Add canonical payload validation, parse-error representation, and deterministic fingerprinting.
- Document `POSITION_CONVERSION` in the transaction vocabulary.

### Files expected to change

- `backend/models/database.py`
- `backend/services/transaction_canonicalizer.py`
- `backend/migrations/versions/<new>_add_position_conversion_payload.py`
- `backend/tests/test_transaction_canonicalizer.py`
- New focused migration/contract test file if separation improves reviewability

### Explicit files NOT to change

- `backend/services/portfolio_rebuilder.py`
- `backend/services/ledger_validator.py`
- `backend/services/portfolio_transactions.py`
- `backend/services/portfolio_snapshots.py`
- `backend/services/market_data/yahoo_chart.py`
- `backend/manage.py`
- All `docs/implementation/M46*`

### Dependencies

None beyond the approved canonical design and current database conventions.

### Deliverables

- Additive migration with upgrade/downgrade guards.
- ORM column and partial-index declaration.
- `PositionConversion` canonical value and payload parser.
- Contract and migration tests.

### Acceptance criteria

- All existing transactions canonicalize exactly as before.
- Valid version-1 payloads produce exact `Decimal` values.
- Invalid payloads produce structured errors and cannot be mistaken for valid conversions.
- Existing rows remain null and unchanged.
- Duplicate conversion key is rejected by the database.
- Downgrade refuses when conversion rows exist.

### Verification

- Focused canonicalizer tests.
- Migration upgrade, repeated-upgrade, uniqueness, constraint, and downgrade tests on SQLite plus the repository’s PostgreSQL migration path. Constraint verification covers conversion INSERT and UPDATE rejection for null predecessor identity, null/non-midnight/noncanonical timestamps, same-date different-time attempts, normalized-midnight duplicates, and preservation of non-conversion null-asset/intraday behavior.
- Existing transaction canonicalizer suite.

### Estimated implementation size

Small: one migration, one model field/index, one typed contract.

### Estimated review size

Small: schema safety, payload exactness, and compatibility review.

## 4. BANPU-WP2 — Replay and independent validator

### Purpose

Make the ledger authoritative and deterministically replayable before any write path can create a conversion.

### Scope

- Add the `POSITION_CONVERSION` rebuilder branch.
- Support predecessor removal, successor create/merge, basis preservation, cash-in-lieu, and realized P/L.
- Support legacy-symbol and asset-native replay, including the historical null-asset predecessor fallback.
- Add independent validator replay and all conversion findings.
- Extend conversion-portfolio reconciliation to asset ID, symbol, shares, average cost, and basis.
- Defend against replayed duplicates and ambiguous holdings.

### Files expected to change

- `backend/services/portfolio_rebuilder.py`
- `backend/services/ledger_validator.py`
- `backend/services/replay_key.py` only if a pure conversion-key helper cannot remain package-local without changing existing `replay_key()` semantics
- `backend/tests/test_portfolio_rebuilder.py`
- `backend/tests/test_ledger_validator.py`
- `backend/tests/test_replay_key.py` if the helper is added there
- New `test_position_conversion_replay.py` if useful

### Explicit files NOT to change

- `backend/services/portfolio_transactions.py`
- `backend/services/market_data/yahoo_chart.py`
- `backend/services/data_fetcher.py`
- `backend/services/portfolio_snapshots.py`
- `backend/manage.py`
- Asset registry models
- All M46 files

### Dependencies

BANPU-WP1 accepted.

Entry into BANPU-WP2 remains blocked until BANPU-WP1 constitutional freeze is
complete. Recorded WP1 residuals do not authorize WP2 work and must be handled
only by the future packages assigned in the canonical design's WP1 residual
register.

### Deliverables

- Fail-closed replay branch.
- Independent validator branch and finding catalog.
- Replay parity tests for both key modes and cash-in-lieu variants.

### Acceptance criteria

- BANPU arithmetic produces the approved quantity and basis outcome.
- Cash is unchanged without cash-in-lieu and changes only by admitted net cash with it.
- Existing successor positions merge by combined shares and basis.
- Legacy and native modes produce identical economic state.
- Malformed, duplicate, missing, or ambiguous conversions cannot pass Stage 5.
- Existing transaction replay tests remain unchanged and green.

### Verification

- Focused replay/validator suites.
- Deterministic repeat replay.
- Live-state fixture reconciliation.
- Existing portfolio rebuilder, replay-key, repair-validation, and ledger-validator suites.

### Estimated implementation size

Medium: two independent state machines plus focused helpers and tests.

### Estimated review size

Medium: accounting equations, identity-key behavior, and validator independence.

## 5. BANPU-WP3 — Quote identity and epoch protection

### Purpose

Prevent predecessor and successor price epochs from being mixed before ledger activation is possible.

### Scope

- Validate requested symbol against Yahoo chart metadata.
- Associate closes with timestamps and keep current/previous values within one epoch.
- Add conversion-bound quote context and epoch-namespaced cache keys.
- Implement fail-closed quarantine reasons.
- Prevent stale predecessor quote/history fallback for a successor.
- Preserve existing quote behavior and cache keys for unconverted assets.

### Files expected to change

- `backend/services/market_data/yahoo_chart.py`
- `backend/services/data_fetcher.py`
- The narrow holdings/price call site in `backend/main.py` if required to pass the binding
- `backend/tests/test_yahoo_chart_provider.py`
- `backend/tests/test_fetch_history.py`
- New focused quote-epoch test file if useful

### Explicit files NOT to change

- Transaction or portfolio database schema
- `backend/services/portfolio_rebuilder.py`
- `backend/services/ledger_validator.py`
- `backend/services/portfolio_transactions.py`
- Frontend transaction authoring
- All M46 files

### Dependencies

BANPU-WP1 accepted so the binding can consume the canonical payload contract.

### Deliverables

- Provider metadata/timestamp validation.
- Converted-asset cache namespace.
- Quarantine result and logging contract.
- Regression tests for unaffected quote callers.

### Acceptance criteria

- Cross-symbol or cross-epoch results never produce a usable quote.
- First successor-epoch quote may return `previous_close=None` but never a predecessor close.
- Converted cache entries are asset/epoch-bound.
- Unconverted quote dictionaries and cache keys retain current behavior.
- Quarantine blocks only the affected converted identity.

### Verification

- Provider fixture tests for matching, mismatch, missing metadata, sparse closes, and epoch boundaries.
- Cache hit, stale fallback, and namespace tests.
- Existing Yahoo chart and data-fetcher suites.

### Estimated implementation size

Medium: adapter validation, cache namespace, and one bounded call-path change.

### Estimated review size

Medium: provider evidence, cache isolation, and compatibility.

## 6. BANPU-WP4 — Registry preparation and live materialization

### Purpose

Add the only authorized atomic write path after safe replay and quote binding exist.

### Scope

- Add minimal predecessor-identifier retirement support if not already callable.
- Validate successor `Asset`, current provider identifier, predecessor status, and `MERGED_INTO` relationship.
- Add `execute_position_conversion()` with locking, optimistic quantity/basis checks, canonical fingerprint idempotency, transaction insertion, successor merge, and cash-in-lieu handling.
- Keep operator access service-only; CLI wiring is deferred to WP7.

### Files expected to change

- `backend/services/portfolio_transactions.py`
- `backend/services/asset_registry.py`
- `backend/services/asset_repository.py` only for the minimal identifier-retirement operation
- `backend/tests/test_portfolio_transactions_capability_shadow.py` or a new focused live-conversion test
- `backend/tests/test_asset_registry.py` or `test_registry_service.py`

### Explicit files NOT to change

- `backend/models/asset.py`
- `backend/services/ledger_repair.py`
- `backend/models/database.py` except changes already accepted in WP1
- `backend/main.py` transaction endpoints
- Frontend files
- `backend/manage.py`
- All M46 files

### Dependencies

BANPU-WP1 through BANPU-WP3 accepted.

### Deliverables

- Atomic live service.
- Idempotent registry preparation/validation behavior.
- Tests for transaction/item/cash atomicity and rollback.

### Acceptance criteria

- No public endpoint can create a conversion.
- Transaction and materialized state commit or roll back together.
- Transaction 83 and all prior ledger rows are untouched.
- Matching retries are no-ops; conflicting retries fail.
- Predecessor is a distinct merged asset; successor is active and current.
- Live outcome equals replay outcome.

### Verification

- Database-session tests for success, existing successor, no-CIL, CIL, stale optimistic expectations, duplicate, registry mismatch, and forced rollback.
- Existing fee, write-path asset-ID, registry, and portfolio-transaction suites.

### Estimated implementation size

Medium: one service function, narrow registry support, and transactional tests.

### Estimated review size

Medium: atomicity, idempotency, registry semantics, and append-only compliance.

## 7. BANPU-WP5 — Accounting readers and bounded reconstruction

### Purpose

Ensure snapshots and return fields represent conversion and optional cash-in-lieu correctly without touching predecessor history.

### Scope

- Classify conversion as zero external/import/manual flow.
- Include only admitted cash-in-lieu fees and realized P/L.
- Add the hard `from_date` conversion boundary to portfolio rebuilding.
- Preserve stored pre-boundary prices and values.
- Recognize evidence-annotated suspension-gap return without “repairing” it away.
- Emit successor asset identity in post-boundary holdings JSON.

### Files expected to change

- `backend/services/portfolio_metrics.py`
- `backend/services/portfolio_snapshots.py`
- `backend/services/snapshot_return_recovery.py`
- `backend/services/portfolio_rebuilder.py` only for bounded historical reconstruction and return-field integration not already delivered in WP2
- `backend/manage.py` only if `verify_snapshots` needs conversion-boundary classification
- `backend/tests/test_portfolio_metrics.py`
- `backend/tests/test_portfolio_metrics_parity.py`
- `backend/tests/test_snapshot_return_recovery.py`
- `backend/tests/test_portfolio_rebuilder.py`
- `backend/tests/test_verify_snapshots.py`

### Explicit files NOT to change

- Transaction write semantics delivered by WP4
- Market-data provider semantics delivered by WP3
- Shadow and evaluation modules
- Immutable recommendation/optimizer tables
- All M46 files

### Dependencies

BANPU-WP2 through BANPU-WP4 accepted.

### Deliverables

- Accounting-reader classification.
- Rebuild boundary enforcement.
- Boundary-aware snapshot verification.
- Preservation and regression tests.

### Acceptance criteria

- Conversion never appears as an external cash flow, import, or quantity correction.
- Cash-in-lieu fees and realized P/L appear exactly once.
- Full or pre-boundary rebuild fails before writes or unsafe provider fetches.
- Bounded rebuild changes no pre-boundary numeric field.
- Genuine annotated suspension-period return remains investment return.

### Verification

- Metrics parity and snapshot recovery tests.
- Hash/field comparison of pre-boundary fixtures.
- Coverage, return decomposition, price-matrix, rebuild, and snapshot-verification suites.

### Estimated implementation size

Medium: several narrow type classifications plus a critical rebuild gate.

### Estimated review size

Medium: return attribution, history protection, and failure ordering.

## 8. BANPU-WP6 — Shadow and succession-aware time-series continuity

### Purpose

Prevent the identity transition from splitting derived portfolio, shadow, attribution, and evaluation series.

### Scope

- Add a narrow effective-dated succession lookup using `MERGED_INTO`.
- Carry non-null asset IDs in affected holdings JSON.
- Apply conversion to replay-time shadow holdings on the boundary.
- Keep paper fractional shares; do not apply broker cash-in-lieu to hypothetical portfolios.
- Normalize post-boundary valuation subjects while preserving immutable source evidence.
- Restrict persisted regeneration to on/after the boundary.

### Files expected to change

- New narrow service such as `backend/services/position_conversion.py` only if needed for pure succession/conversion helpers
- `backend/services/decision_memory/shadow_tracker.py`
- `backend/services/decision_memory/attribution.py`
- `backend/services/analytics/quant_engine.py`
- `backend/services/evaluation/horizon_grader.py`
- `backend/services/evaluation/ideal_series.py`
- Corresponding focused tests, especially `test_shadow_regeneration.py`, `test_horizon_grader.py`, and `test_ideal_series.py`

### Explicit files NOT to change

- `RecommendationSnapshot`, `OptimizerHistory`, `UserExecutionDecision`, and `RecommendationGrade` schema
- Historical recommendation or decision payloads
- Transaction schema or write path
- General asset-definition vocabulary
- All M46 files

### Dependencies

BANPU-WP3 through BANPU-WP5 accepted.

### Deliverables

- Effective-dated successor resolution.
- Shadow conversion applicator and bounded persistence.
- Cross-boundary attribution/grading continuity tests.

### Acceptance criteria

- A pre-boundary predecessor holding becomes the successor on the correct shadow valuation date.
- Shadow inception value is conserved mechanically.
- Pre-boundary shadow rows remain unchanged.
- Recommendations retain original evidence while post-boundary evaluation follows the successor.
- No unrelated symbol is remapped.
- No general corporate-action dispatcher or event vocabulary is introduced.

### Verification

- Static and ACTIVE_MODEL shadow fixtures across the boundary.
- Attribution, quant, horizon-grade, and ideal-series fixtures spanning the relationship date.
- Existing shadow cash-accounting and regeneration suites.

### Estimated implementation size

Medium: one narrow helper and bounded adaptations across five consumers.

### Estimated review size

Medium: identity continuity, evidence immutability, and shadow accounting.

## 9. BANPU-WP7 — Operator command and migration rehearsal

### Purpose

Provide a safe, idempotent, CLI-only path to prepare and apply the reviewed production manifest.

### Scope

- Add `apply_position_conversion` CLI with dry-run default and explicit `--commit`.
- Validate manifest schema, registry state, broker facts, quote epoch, continuity evidence, rebuild boundary, and both replay modes.
- Produce a deterministic before/after report without exposing credentials or raw provider payloads.
- Add cache purge and bounded rebuild instructions; do not execute production changes in the package.

### Files expected to change

- `backend/manage.py`
- New sanitized test manifest under `backend/tests/fixtures/`
- New focused CLI test file
- Operational documentation only if required by the canonical design; not M46 documentation

### Explicit files NOT to change

- Public API routes
- Frontend files
- Core accounting equations accepted in prior packages
- Production database or production cache
- All M46 files

### Dependencies

BANPU-WP1 through BANPU-WP6 accepted.

### Deliverables

- Dry-run/commit CLI.
- Sanitized manifest fixture.
- Deterministic preflight and result report.
- Rehearsal evidence against an isolated database copy.

### Acceptance criteria

- No flags performs no write.
- `--dry-run` performs no write.
- `--commit` is explicit and refuses any failed preflight.
- Re-running the same manifest is an `already_applied` no-op.
- A conflicting manifest fails.
- The command never broadens scope to generic corporate actions.

### Verification

- CLI parser and transaction-boundary tests.
- Dry-run database diff equals zero.
- Rehearsal upgrade, apply, bounded rebuild, and rollback on an isolated production-shaped copy.

### Estimated implementation size

Small: one command wrapping accepted services and checks.

### Estimated review size

Medium: operator safety, reporting, idempotency, and rehearsal evidence.

## 10. BANPU-WP8 — Integrated regression and release evidence

### Purpose

Prove the complete remediation is safe to deploy without adding new production behavior.

### Scope

- Run the complete focused and regression suite.
- Establish pre/post golden evidence for transaction types, portfolio state, snapshots, quotes, shadows, and evaluation.
- Verify source-change boundaries and M46 immutability.
- Produce the production verification checklist and release candidate evidence.
- No production conversion execution.

### Files expected to change

- Focused integration tests under `backend/tests/`
- Sanitized fixtures only
- A remediation-specific release verification record under `docs/implementation/` if governance requests one

### Explicit files NOT to change

- Production source except fixes strictly required to close a failed acceptance criterion in its owning prior work package
- Production data
- M46 files
- Approved canonical design, roadmap, or sequence except through separately approved documentation correction

### Dependencies

BANPU-WP1 through BANPU-WP7 accepted.

### Deliverables

- Green focused and regression results.
- Golden before/after evidence.
- Source-boundary audit.
- Deployment readiness recommendation and blocker register.

### Acceptance criteria

- All package acceptance criteria remain satisfied together.
- Existing transaction-type golden behavior is unchanged.
- Pre-boundary portfolio and shadow values are unchanged.
- No M46 diff exists.
- No public API, corporate-action framework, or repair-tier economic content exists.
- Every production verification step has an owner, command, expected output, and stop condition.

### Verification

- Full relevant backend test suite.
- Migration rehearsal on a production-shaped copy.
- Graph refresh and graph query confirming expected change surface.
- Git diff audit restricted to approved remediation files.

### Estimated implementation size

Medium: integration fixtures and evidence, with little or no new production logic.

### Estimated review size

Large: final cross-package accounting, operations, and regression review.

## 11. Dependency graph

```text
BANPU-WP1 Persistence and canonical contract
    ↓
BANPU-WP2 Replay and validator
    ↓
BANPU-WP3 Quote identity and epoch protection
    ↓
BANPU-WP4 Registry and live materialization
    ↓
BANPU-WP5 Accounting readers and bounded reconstruction
    ↓
BANPU-WP6 Shadow and time-series continuity
    ↓
BANPU-WP7 Operator command and rehearsal
    ↓
BANPU-WP8 Integrated regression and release evidence
```

The strict sequence favors review certainty over parallel implementation. Deployment still places the WP3 quote guard into production before any conversion row is authored.

## 12. Roadmap completion condition

The roadmap is complete only when BANPU-WP8 is accepted. Completion authorizes a separately controlled production deployment sequence; it does not itself authorize mutation of production data.
