# BANPU-WP2 — Implementation Sequence

**Artifact class:** Planning only
**Status:** `PLANNING RC2 — IMPLEMENTATION NOT AUTHORIZED`
**Sequence scope:** BANPU-WP2 only
**Next-package authority:** `NONE`

## 1. Preconditions

Implementation may begin only after all of the following are true:

1. separate governance explicitly authorizes BANPU-WP2 implementation;
2. `BANPU_WP1_FREEZE_RECORD.md` remains authoritative and every frozen-corpus hash matches;
3. the repository state and existing WP1 staged corpus are recorded without modification;
4. no persistent conversion row exists in any environment; conversion rows are permitted before WP5 only as transient, rollback-isolated fixtures;
5. M46 remains implementation-suspended and its files are unchanged;
6. WP2 production and test file allowlists are accepted;
7. baseline rebuilder, validator, replay-key, repair-validation, canonicalizer, and migration test results are recorded; and
8. any unrelated dirty changes overlapping a WP2 file are resolved by the owner before implementation.

WP2 adds no WP5 runtime boundary. Until WP5 acceptance, BANPU remediation
governance must ensure that every rebuild fixture is transient and that rebuild
evidence is dry-run or `skip_snapshots=True`; committed full-history conversion
rebuild evidence is prohibited. This procedural control carries operational
risk but does not change WP5 ownership or authorize WP4/WP5 execution.

Failure of a precondition stops WP2. It does not reopen WP1 or authorize a workaround in another package.

## 2. Ordered implementation steps

### Step 1 — Freeze the WP2 working baseline

Actions:

- record branch/commit/status and the exact WP2 allowlist;
- verify all WP1 frozen hashes and aggregate identity;
- record M46 no-change evidence;
- run or record the baseline focused suites; and
- confirm `replay_key()` signature and current legacy/native behavior.

Verification after Step 1:

- no source file changed;
- all preconditions have evidence;
- pre-existing failures, if any, are explicit and non-overlapping.

Exit: reproducible WP2 entry state exists.

### Step 2 — Add focused constitutional fixtures

Actions:

- add full-share BANPU, incident-independent generic, and broker-rounded cash-in-lieu fixtures;
- add existing-successor basis-conservation and both replay-mode fixtures;
- add historical null-asset predecessor fallback, zero-match, and multi-match fixtures;
- add validator fixtures where raw ledger symbol differs from canonical/payload symbol, including native/canonical candidate union, deduplication, and conflicting paths;
- add Stage 1 final-state versus terminal Stage 2 per-date equality, complete state-copy, and fresh per-run duplicate fixtures;
- add pre-existing item asset-ID preservation, successor identity conflict, and no-registry/backfill fixtures;
- add conversion-only asset-first reconciliation with canonical fallback, ambiguity, pre-commit null-ID, post-commit match, and five independent fields;
- add payload, identity/date, duplicate, share, basis, CIL, and affected-asset same-day invalid fixtures;
- add same-day unrelated-asset fixtures proving unchanged transaction-ID order and no conversion priority;
- add raw/effective repair-mode fixtures; and
- encode expected finding IDs/severities, unchanged `_EQUITY_TYPES` membership, and exact rebuild-result field dispositions.

Verification after Step 2:

- expected arithmetic is calculated independently with `Decimal`;
- the generic valid fixture contains no BANPU identity, date, or transaction-ID dependency;
- all conversion rows are transient and rollback-isolated, and no fixture requires a committed full-history rebuild;
- tests fail only because WP2 behavior is absent;
- no frozen WP1 test or production file is changed.

Exit: executable WP2 requirements exist without implementation.

### Step 3 — Implement rebuilder preflight and identity resolution

Actions:

- add a controlled conversion replay failure type local to the rebuilder;
- validate the frozen parse result and raw-row identity/date projections once in `rebuild_portfolio()` before either replay application site;
- retain one immutable preflight verdict/metadata set for Stage 1 final-state replay and Stage 2 per-date replay;
- detect duplicate predecessor/date keys and same-day affected-equity conflicts;
- derive local legacy/native predecessor and successor candidate keys;
- deduplicate candidates and fail on zero or multiple distinct matches; and
- enforce at the rebuilder consumer boundary that repair overlay processing cannot remove or modify conversion rows, without changing `ledger_repair.py`.

Verification after Step 3:

- malformed, identity-invalid, duplicate, missing, ambiguous, and same-day cases fail before persistence;
- transaction-83 fallback succeeds only for one match;
- Stage 1 and Stage 2 consume the same preflight decision but initialize separate per-run replayed-conversion-key sets;
- an `EXCLUDE` repair is ineffective for a conversion;
- existing `replay_key()` tests and no-conversion rebuilder tests remain green.

Exit: invalid identity cannot reach conversion state mutation.

### Step 4 — Implement rebuilder accounting application

Actions:

- reconcile full predecessor shares and exact basis;
- remove predecessor only after all preconditions pass;
- create or merge successor using exact combined shares and basis;
- carry successor identity and conditional sector;
- apply only admitted net cash and realized P/L; and
- retain existing canonical ordering and unrelated holdings unchanged;
- apply the branch once per replay run at both existing application sites; and
- copy asset ID, report symbol, price symbol, exact basis, sector, shares, average cost, and all conversion-relevant state into per-date captures.

Verification after Step 4:

- full-share BANPU arithmetic passes;
- incident-independent generic arithmetic passes;
- cash-in-lieu and no-cash-in-lieu cases pass;
- existing-successor merge proves `combined_basis == existing_basis + converted_basis` before projection;
- affected-asset same-day transactions fail and unrelated same-day transactions retain transaction-ID order without a conversion priority;
- repeat replay and legacy/native economic parity pass;
- Stage 1 final state equals the terminal Stage 2 per-date state and neither site treats the other's application as a duplicate;
- no-conversion rebuilder tests remain unchanged and green.

Exit: rebuilder deterministically applies a valid conversion.

### Step 5 — Implement conversion reconciliation and Stage 5 blocking

Actions:

- construct a deterministic preservation map for every current `PortfolioItem.asset_id`, including legitimate `NULL` values;
- preserve every unaffected ID and an already-correct successor ID through delete-and-reinsert, enrich only a successor `NULL` to the payload ID, and fail on a conflicting non-null successor ID;
- do not reinsert the surrendered predecessor or transfer its asset ID;
- perform no registry lookup and no general identity backfill;
- leave ordinary symbol-keyed shares/average-cost reconciliation unchanged;
- pair only the conversion successor by asset-ID precedence, then unique canonical-symbol fallback, and fail when the paths identify different items;
- expose five independent successor rows for asset ID, symbol, shares, average cost, and basis;
- treat pre-commit null successor ID as valid fallback input but `DIFFERENT`, and require all five fields to be `MATCH` after item-only commit;
- block commit for conversion CRITICAL findings; and
- block `POSITION_CONVERSION_SAME_DAY_CONFLICT` specifically while preserving global unrelated-ERROR policy.

Verification after Step 5:

- every non-successor item retains its pre-existing asset ID in both replay modes;
- successor create/merge binds the payload ID and a conflicting non-null ID fails closed;
- clean post-commit fixture matches on all five fields, while pre-commit null-ID enrichment is independently visible as `DIFFERENT`;
- wrong symbol is independently visible when asset-ID pairing supplies the comparand; missing/extra remains reserved for genuinely unpaired items;
- ordinary portfolio-item reconciliation output is unchanged;
- invalid conversions cannot commit in dry-run/commit-path tests;
- existing execution-plan and Stage 5 tests remain green.

Exit: rebuilder output is materially reconcilable and fail-closed.

### Step 6 — Implement independent validator replay

Actions:

- add conversion recognition and raw-row preflight;
- leave `_EQUITY_TYPES` unchanged so malformed conversions produce conversion-specific rather than duplicate generic findings;
- retain the existing no-conversion validator path;
- retain the existing raw-symbol-keyed `_ReplayState` as the sole authoritative validator state and augment it with deterministic canonical-symbol/asset-ID metadata and exact basis;
- construct legacy candidates from canonical metadata over actual raw keys; construct native candidates as the union of asset-ID and canonical-fallback matches; deduplicate by actual holding key and fail on multiple distinct candidates;
- independently mutate that same state for predecessor removal, successor create/merge, cash, and realized P/L; never create a parallel conversion state;
- ensure existing sell, cash, holdings-consistency, and snapshot-cash checks consume the converted state;
- emit active WP2 findings with fixed severities and deterministic details;
- catalogue the WP3/WP5-owned finding IDs without implementing their evidence predicates; and
- enforce at the validator consumer boundary that `EXCLUDE` and `SUPPRESS_FINDING` repairs cannot remove conversion facts or findings; and
- reconcile materialized conversion state across the five required fields.

Verification after Step 6:

- every active WP2 finding has a triggering and clean case;
- raw≠canonical identity resolves correctly in both modes, candidate union is deterministic, and zero/multiple candidates map to the specified findings;
- predecessor removal and successor state are coherent with all existing validator checks;
- validator has no parallel conversion state and does not import rebuilder state, identity helper, or mutation;
- validator never throws for a WP1-representable malformed payload;
- malformed conversion finding sets prove `_EQUITY_TYPES` remains unchanged;
- no-conversion validator output is unchanged.

Exit: independent validation can accept a valid conversion and reject every WP2-owned invalid condition.

### Step 7 — Prove cross-engine and repair parity

Actions:

- run identical fixtures through both independent state machines;
- compare successor identity, shares, average cost, basis, cash, and realized P/L;
- compare legacy and native reported economic state;
- prove raw/effective validator modes retain conversion authority; and
- prove `apply_repairs` true/false cannot remove or alter conversion accounting;
- prove a conversion-targeted `EXCLUDE` is ineffective without a new finding merely for the repair's existence; and
- prove `SUPPRESS_FINDING` cannot suppress a conversion finding.

Verification after Step 7:

- all parity matrices are exact within only the frozen tolerances;
- no shared mutation helper is used to manufacture parity;
- repair-validation consistency suite passes.

Exit: deterministic economic and governance parity is proven.

### Step 8 — Run complete package verification

Actions:

- run focused WP2, rebuilder, validator, replay-key, and repair suites;
- run effective-validator, capability-shadow, registry-replay-parity, and replay-cutover owner suites;
- rerun frozen WP1 canonicalizer and migration suites without editing them;
- verify no-conversion golden behavior;
- audit imports and searches for unauthorized DB/network/registry/quote access;
- prove all conversion rows are transient and rollback-isolated and that rebuild evidence is dry-run or `skip_snapshots=True`, with no committed full-history conversion rebuild before WP5;
- verify frozen architecture/calculation-rule documents and `docs/engineering/DECISION_LOG.md` are unchanged and their synchronization remains assigned to the separately approved WP8 documentation-correction owner;
- audit changed files against the allowlist;
- recompute frozen WP1 hashes and M46 no-change evidence; and
- run `graphify update .` and review the WP2 graph surface.

Verification after Step 8:

- every specification acceptance criterion passes;
- all results and exact commands are recorded;
- only authorized WP2 files and planning/review artifacts differ;
- graph changes contain no future-package or M46 implementation.
- WP5's runtime boundary remains unimplemented by WP2 and WP3+ responsibilities are unchanged.

Exit: reviewable WP2 candidate and complete evidence exist.

### Step 9 — Independent review and constitutional disposition

Review order:

1. accounting equation and tolerance review;
2. dual replay-site, copied-state, and per-run duplicate review;
3. legacy/native/raw-key identity and ambiguity review;
4. validator single-state and independence review;
5. item-ID preservation and conversion-only reconciliation review;
6. Stage 5, repair, result-disposition, and failure-atomicity review;
7. unaffected-behavior owner-suite review; and
8. transient-evidence, file-boundary, WP1-freeze, residual, M46, deferred-documentation, and future-package governance review.

Verification after Step 9:

- all findings are closed or the candidate returns to its owning step;
- accepted evidence identifies the exact implementation candidate;
- no production action has occurred.

Exit: WP2 is either accepted under a separately recorded governance act or remains incomplete. This sequence itself does not freeze WP2 and does not authorize WP3.

## 3. Failure return rules

- A Step 3 identity failure returns to Step 3, not to WP1 contract design.
- A Step 4 arithmetic or merge failure returns to Step 4.
- A Stage 1/Stage 2 divergence or copied-state defect returns to Steps 3 and 4.
- A Step 5 asset-ID preservation, reconciliation, or gate failure returns to Step 5.
- A Step 6 candidate, authoritative-state, finding, existing-check, or independence failure returns to Step 6.
- A parity failure returns to both owning state-machine steps; neither implementation is presumed authoritative over the other.
- A frozen-hash mismatch, prohibited-file change, or future-package leakage stops review and requires governance correction before work resumes.
- A no-conversion regression blocks WP2 acceptance.
- Persistent pre-WP5 conversion state, committed full-history conversion rebuild evidence, or a WP2 runtime boundary stops review and returns to governance correction.

Later packages must never compensate for an incomplete WP2 step.

## 4. Verification command set

Use the repository-supported environment and record exact outputs:

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

If the focused WP2 file is not created, omit only that command and demonstrate equivalent named coverage in the two existing suites.

## 5. Exit criteria

BANPU-WP2 implementation is complete only when:

- a valid frozen-contract conversion replays deterministically;
- both rebuilder application sites produce equal terminal conversion state with immutable shared preflight evidence, fresh per-run duplicate tracking, and complete state copying;
- independent validation mutates one augmented authoritative raw-keyed state and reaches the same economic state without a parallel state or imported rebuilder logic;
- invalid conversion conditions cannot pass the Stage 5 commit gate;
- legacy and native replay are economically identical, including transaction-83 fallback;
- conversion reconciliation covers asset ID, symbol, shares, average cost, and basis;
- every reinserted pre-existing item asset ID is preserved, the predecessor ID is not transferred, the successor is authoritatively bound without registry lookup/backfill, and conflicts fail closed;
- conversion-only reconciliation follows asset-ID precedence and unique canonical fallback with defined pre-/post-commit outcomes while ordinary reconciliation remains unchanged;
- repair modes cannot suppress conversion authority;
- exact rebuild-result dispositions and unchanged `_EQUITY_TYPES` behavior are proven;
- all conversion rows in evidence are transient, rebuild evidence is dry-run or `skip_snapshots=True`, and no committed full-history conversion rebuild is accepted before WP5;
- all focused and regression verification passes;
- frozen WP1 hashes, residual dispositions, M46 state, and unaffected behavior remain unchanged;
- the diff contains no prohibited file or future-package implementation; and
- deferred architecture/calculation-rule/decision-log synchronization remains WP8-owned without WP8 authorization; and
- an independent review accepts the exact WP2 candidate.

Completion creates no authority to implement WP3, deploy code, mutate production data, author a conversion, amend WP1, or change M46.
