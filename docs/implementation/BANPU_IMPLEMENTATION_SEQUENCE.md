# BANPU Remediation — Mandatory Implementation Sequence

**Status:** APPROVED SEQUENCE
**Authority:** `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`
**Package source:** `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`
**Implementation state:** BANPU-WP1 implementation complete; independently approved and confirmed with recorded residuals; freeze pending; BANPU-WP2 not started and blocked

This is a strict serial sequence. No implementation step may begin before its predecessor reaches its exit criteria and is accepted. Production mutation is outside implementation and begins only after step 9.

## 1. Sequence invariants

- The repository starts from the approved RCA, review, design, roadmap, and sequence.
- M46 remains frozen and untouched at every step.
- Each step begins from a green predecessor commit or otherwise review-frozen repository state.
- A failed verification returns work to the owning step; later steps do not compensate for an incomplete predecessor.
- Source changes remain inside the files authorized by the owning work package.
- `graphify update .` runs after each accepted code step, as required by repository instructions.
- No conversion row, registry production mutation, cache purge, rebuild, or production shadow rewrite occurs during implementation.

## 2. Step 0 — Freeze the implementation baseline

**Sequence status:** Completed as the accepted predecessor to BANPU-WP1. This
historical step is not the pending WP1 constitutional freeze.

### Preconditions

- All three approved input analyses/designs are available.
- The three BANPU canonical repository documents are accepted.
- M46 planning remains frozen and implementation-suspended.

### Repository state

- Production behavior is unchanged.
- No `POSITION_CONVERSION` code or schema exists.
- Working tree is clean or unrelated user changes are identified and excluded.

### Expected code changes

None. Record the baseline commit, migration heads, relevant test commands, and source-boundary allowlist.

### Verification

- Git status and baseline commit recorded.
- Existing focused portfolio, ledger, snapshot, market-data, registry, shadow, and evaluation suites pass or pre-existing failures are explicitly recorded.
- M46 file hashes recorded for later no-change verification.

### Exit criteria

- Reproducible baseline evidence exists.
- No unexplained failure or overlapping dirty change remains.
- BANPU-WP1 is authorized to begin.

## 3. Step 1 — Complete BANPU-WP1: persistence and canonical contract

**Sequence status:** Implementation complete through RC3. Renewed Independent
Review disposition: `APPROVED WITH RECORDED RESIDUALS`. WP1 is confirmed with
those residuals; constitutional freeze remains pending.

### Preconditions

- Step 0 accepted.
- Migration head and database compatibility conventions are known.

### Repository state

- No replay, validator, market-data, or write-path conversion behavior exists.
- No production data is modified.

### Expected code changes

- Add nullable transaction payload, the conversion-specific predecessor/date
  constraint, and the retained conversion-only partial unique index.
- Add behaviorally equivalent PostgreSQL, ORM, Alembic, and legacy SQLite
  support, including SQLite INSERT and UPDATE enforcement.
- Add typed version-1 payload parsing, exact decimals, errors, and fingerprints.
- Add focused migration and canonicalizer tests and the authoritative
  `POSITION_CONVERSION` vocabulary correction.

### Verification

- Migration upgrade, repeated-upgrade, conversion INSERT/UPDATE constraint,
  normalized-midnight uniqueness, unaffected non-conversion behavior, and
  guarded downgrade tests.
- Existing transactions canonicalize identically.
- Valid/invalid conversion fixtures behave as specified.
- Graph is updated and the diff contains only WP1-authorized files.
- Real PostgreSQL execution remains the recorded `MINOR-5` residual assigned
  to the WP7 production-shaped rehearsal and WP8 release evidence.

### Exit criteria

- BANPU-WP1 acceptance criteria pass and the renewed independent review is
  `APPROVED WITH RECORDED RESIDUALS`.
- Schema is additive and inert without conversion rows.
- Contract is approved for constitutional freeze; it is not frozen by this
  sequence synchronization.
- `MINOR-1`, `MINOR-2`, `MINOR-5`, and `NEW-MINOR-A` are recorded with future
  owners and mandatory verification. `NEW-MINOR-B` and Observation 1 are
  resolved as governance findings.

## 4. Step 2 — Complete BANPU-WP2: replay and validator

**Sequence status:** Not started. Entry is blocked until the separately
authorized BANPU-WP1 constitutional freeze completes.

### Preconditions

- Step 1 confirmed and constitutionally frozen; an approved implementation
  candidate that is only freeze-ready does not satisfy this precondition.

### Repository state

- Database can store a conversion, but no authorized write path exists.
- Existing production transaction behavior remains active.

### Expected code changes

- Add fail-closed rebuilder application.
- Add legacy/native identity bridging.
- Add independent validator replay and conversion findings.
- Add basis-aware conversion reconciliation.

### Verification

- BANPU arithmetic, cash-in-lieu, existing-successor, duplicate, missing, and ambiguous cases.
- Live-state fixture and replay parity under both key modes.
- Existing rebuilder, validator, repair-consistency, and replay-key suites.
- Graph and file-boundary audit.

### Exit criteria

- A valid conversion replays deterministically.
- Invalid conversions cannot pass validation or commit through rebuild.
- Existing transaction replay remains unchanged.

## 5. Step 3 — Complete BANPU-WP3: quote identity and epoch protection

### Preconditions

- Step 2 accepted.
- Conversion identity and dates are available through the canonical contract.

### Repository state

- Conversion replay exists, but no live authoring path exists.
- Quote fetching still requires successor-epoch protection.

### Expected code changes

- Validate provider symbol metadata and timestamped closes.
- Add successor asset/epoch binding and cache namespace.
- Add quarantine conditions and affected-call-path propagation.
- Preserve unconverted quote behavior.

### Verification

- Matching/mismatching metadata, first successor close, cross-epoch previous close, cache isolation, stale fallback, and quarantine fixtures.
- Existing Yahoo provider and data-fetcher tests.
- No unrelated API response regression.

### Exit criteria

- A converted identity cannot consume predecessor-epoch market data.
- Unconverted assets retain their existing path.
- Quote protection is independently deployable before ledger activation.

## 6. Step 4 — Complete BANPU-WP4: registry and live materialization

### Preconditions

- Steps 1–3 accepted.
- Replay and quote validation can safely consume any row the live service creates.

### Repository state

- Conversion is readable and quote-safe.
- No public or operator write path exists.

### Expected code changes

- Add minimal registry identifier-retirement support if needed.
- Add atomic `execute_position_conversion()` service.
- Add locking, optimistic assertions, duplicate fingerprint handling, successor merge, and cash-in-lieu materialization.

### Verification

- Success, retry, conflict, stale expectation, registry mismatch, existing successor, CIL/no-CIL, and forced rollback tests.
- Compare live materialization to replay output.
- Confirm no public API or frontend path was added.

### Exit criteria

- Live and replay accounting are identical.
- Writes are atomic and append-only.
- The service remains unreachable except by direct internal invocation pending WP7.

## 7. Step 5 — Complete BANPU-WP5: accounting and bounded reconstruction

### Preconditions

- Step 4 accepted.
- Conversion accounting is stable in live and replay state.

### Repository state

- Current holdings can convert safely.
- Snapshot/return readers and historical rebuild guard are not yet complete.

### Expected code changes

- Add intentional conversion classification in metrics, snapshots, and recovery.
- Add cash-in-lieu realized P/L and fee treatment.
- Enforce the conversion rebuild boundary before provider fetching or writes.
- Add boundary return annotation handling and successor holdings identity.

### Verification

- Return decomposition parity with and without cash-in-lieu.
- Refusal of full/pre-boundary rebuild.
- Bounded reconstruction from the transition date.
- Pre-boundary fixture hashes/numeric fields unchanged.
- Existing snapshot, metrics, recovery, coverage, and verification suites.

### Exit criteria

- Conversion cannot contaminate external flows or manual adjustments.
- Predecessor history cannot be re-fetched by an ordinary rebuild.
- Annotated suspension return remains genuine investment return.

## 8. Step 6 — Complete BANPU-WP6: shadow and time-series continuity

### Preconditions

- Step 5 accepted.
- Portfolio snapshots expose correct effective-dated identities and prices.

### Repository state

- Real portfolio accounting is complete.
- Shadow, attribution, quant, and evaluation series may still split at the identity boundary.

### Expected code changes

- Add narrow succession resolution through `MERGED_INTO`.
- Apply conversion to working shadow holdings.
- Add asset identity to affected derived holdings.
- Make post-boundary shadow persistence bounded.
- Bridge evaluation windows without rewriting source evidence.

### Verification

- STATIC_FROZEN and ACTIVE_MODEL fixtures spanning the transition.
- Quant, attribution, horizon, and ideal-series cross-boundary fixtures.
- Inception/mechanical NAV conservation.
- Pre-boundary derived rows unchanged.
- Historical recommendation and optimizer payloads unchanged.

### Exit criteria

- Every identified derived consumer maintains successor continuity.
- Shadow histories neither diverge silently nor rewrite inception evidence.
- No generic event framework was introduced.

## 9. Step 7 — Complete BANPU-WP7: operator command and rehearsal

### Preconditions

- Steps 1–6 accepted.
- All runtime readers and writers understand the conversion.

### Repository state

- Internal conversion service exists.
- Production remains unchanged and no operator command has executed against it.

### Expected code changes

- Add CLI manifest parsing, preflight, dry-run default, explicit commit, deterministic reporting, and idempotent retry behavior.
- Add sanitized manifest fixture and CLI tests.

### Verification

- No-flag and dry-run database diffs are zero.
- Commit succeeds only after every preflight.
- Same manifest retries as no-op; conflict fails.
- Isolated production-shaped rehearsal covers migration, registry preparation, quote gate, conversion, bounded rebuild, shadow regeneration, and transaction rollback.

### Exit criteria

- Operator tooling is safe, scoped, and deterministic.
- Rehearsal produces the expected accounting result without touching production.
- No public conversion endpoint exists.

## 10. Step 8 — Complete BANPU-WP8: integrated regression and release evidence

### Preconditions

- Step 7 accepted.
- No package-local acceptance criterion remains open.

### Repository state

- All intended remediation code exists.
- Production ledger and data remain unchanged.

### Expected code changes

- Integration tests and sanitized evidence only, except corrections returned to and reviewed within the owning package.
- Optional remediation-specific release verification record if governance requires it.

### Verification

- Full focused and relevant regression suites.
- Golden parity for every existing transaction type.
- Both replay modes, conversion/no-conversion portfolios, caches, snapshots, shadows, and evaluation.
- Migration rehearsal on a production-shaped copy.
- Git diff allowlist and graph change-surface review.
- M46 hashes match step 0.

### Exit criteria

- All technical and operational gates pass.
- Release evidence contains commands, expected outputs, owners, and stop conditions.
- No blocker remains.
- Implementation is ready for a separately authorized production deployment.

## 11. Step 9 — Production deployment handoff

### Preconditions

- Step 8 accepted.
- Separate production-change authorization exists.
- Broker statement has fixed `shares_received`, rounding, cash-in-lieu, and basis allocation.
- Scoped backup and maintenance window are ready.

### Repository state

- Conversion-aware release is complete and immutable for deployment.
- Production still contains no new conversion row.

### Expected code changes

None. Any code change returns to its owning implementation step and repeats downstream verification.

### Verification

- Follow the canonical deployment strategy exactly: quarantine, backup, quote guard, migration, compatible code, registry preparation, cache purge, evidence validation, dry-run, dual replay verification, atomic commit, bounded portfolio rebuild, bounded shadow regeneration, final verification.

### Exit criteria

- Production verification checklist passes and quarantine is removed; or
- Deployment stops safely with quarantine retained and the canonical rollback strategy invoked.

## 12. Sequence completion rule

The implementation sequence is complete only after step 8. Step 9 is an operational handoff, not implicit authority to change production. No predecessor may be waived, combined, or bypassed without a separately approved revision to the canonical design and these implementation documents.
