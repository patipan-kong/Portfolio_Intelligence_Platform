# BANPU-WP2 — Implementation Specification

**Artifact class:** Planning specification only
**Work package:** `BANPU-WP2 — Replay and independent validator`
**Status:** `PLANNING RC2 — IMPLEMENTATION NOT AUTHORIZED`
**Constitutional predecessor:** `BANPU-WP1 — FROZEN WITH RECORDED RESIDUALS`
**Authority:** Frozen `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`, `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`, `BANPU_IMPLEMENTATION_SEQUENCE.md`, and `BANPU_WP1_FREEZE_RECORD.md`

## 1. Scope

BANPU-WP2 makes the frozen version-1 `POSITION_CONVERSION` transaction readable by the portfolio rebuilder and independently auditable by the ledger validator before any live write path may create such a transaction.

WP2 is limited to:

1. a fail-closed `POSITION_CONVERSION` branch in portfolio replay;
2. predecessor removal and successor creation or merge using the frozen accounting equations;
3. basis preservation, optional cash-in-lieu cash, and realized P/L replay;
4. deterministic legacy-symbol and asset-native identity handling, including the historical null-asset predecessor fallback;
5. independent validator replay that does not import or call rebuilder state mutation;
6. conversion finding definitions and the predicates that can be evaluated from the WP1 transaction contract, transaction sequence, replay state, and materialized portfolio state;
7. conversion-portfolio reconciliation across asset ID, symbol, shares, average cost, and basis;
8. replay-layer duplicate, missing-holding, ambiguous-holding, and same-day conflict defense; and
9. focused and regression verification for both replay modes and both cash-in-lieu variants.

The minimum production implementation is confined to `portfolio_rebuilder.py` and `ledger_validator.py`. `replay_key.py` remains unchanged unless implementation proves that a pure, conversion-specific key helper cannot remain local without changing existing `replay_key()` semantics. No such need is established by this plan.

## 2. Goals

- Make a valid frozen-contract conversion replay deterministically from the append-only ledger.
- Produce the same economic result in legacy-symbol and asset-native modes.
- Preserve total predecessor basis except for basis explicitly allocated to cash-in-lieu.
- Preserve cash and realized P/L when cash-in-lieu is absent.
- Apply exactly the admitted net cash and realized P/L when cash-in-lieu is present.
- Merge an existing successor using combined shares and combined basis.
- Ensure invalid conversion rows cannot be silently ignored, partially applied, repaired away, or committed by rebuild.
- Give Stage 5 an independent, deterministic validator result.
- Keep every conversion row transient until WP5 owns and implements the hard reconstruction boundary; WP2 evidence must not establish an unbounded committed conversion rebuild as accepted behavior.
- Preserve existing replay, validation, and materialization behavior for portfolios without `POSITION_CONVERSION`.

## 3. Non-goals

WP2 does not:

- change any frozen WP1 artifact, schema, migration, model, payload type, parser, fingerprint, tolerance, or `POSITION_CONVERSION` column meaning;
- add a conversion write service, API, frontend, CLI, manifest, registry preparation, locking, retry, or live atomic materialization; those remain WP4/WP7 responsibilities;
- implement quote identity, quote epochs, cache namespacing, or quarantine evidence; those remain WP3 responsibilities;
- implement portfolio metrics classification, return attribution, snapshot recovery, holdings-JSON identity, or the hard historical rebuild boundary; those remain WP5 responsibilities;
- implement shadow, attribution, quant, horizon, or evaluation continuity; those remain WP6 responsibilities;
- resolve `MINOR-1`, `MINOR-2`, `MINOR-5`, or `NEW-MINOR-A`; their frozen future owners remain unchanged;
- modify `LedgerRepair` or make conversion suppressible, editable, or conditional on repair mode;
- create a generic corporate-action abstraction, dispatcher, event table, or transaction family;
- mutate production data, create a conversion row, rebuild production state, deploy, or authorize WP3 or any later package; or
- modify M46 status, plans, code, tests, or behavior.

WP2 also does not authorize a persistent conversion row in development, test,
rehearsal, staging, or production-like state before WP5 acceptance. Tests may
construct conversion rows only as transient, rollback-isolated fixtures.

## 4. Frozen inputs and invariants

WP2 consumes the WP1 `CanonicalTransaction.position_conversion` parse result exactly as frozen. It must not reconstruct the payload from top-level float columns and must not amend the parser.

The authoritative equations are:

```text
Qe = Qp × R
Qf = Qe - Qr
B0 = Bs + Bf
Cn = Cg - F - T
RP = Cn - Bf
As = Bs / Qr
```

Payload arithmetic uses exact `Decimal`. Replayed predecessor basis is compared to `basis.before` with absolute tolerance THB `0.01`. Top-level `shares`, `price_per_share`, `total_amount`, `fees`, and `taxes` are compatibility projections compared with absolute tolerance `0.000001` per field. Existing replay rounding behavior must not be broadened into payload arithmetic.

The frozen identity/date rules remain:

- predecessor and successor asset IDs are non-null and distinct;
- top-level `asset_id` and `symbol` identify the predecessor and agree with the payload;
- `transaction_date` is the payload `valuation_transition_date` at timezone-free naive midnight;
- the predecessor is held exactly once and the entire holding is surrendered;
- exactly one conversion key exists per portfolio, predecessor asset ID, and valuation transition calendar date;
- existing ordering remains `(transaction_date, transaction_id)`; and
- no other predecessor or successor equity transaction shares the transition calendar date.

Because frozen canonicalization intentionally hides `CanonicalTransaction.asset_id` in legacy replay mode, top-level asset/date equality must be checked against the already-loaded raw `Transaction` row in WP2 code. WP1 canonical types must not be changed to solve this WP2 concern.

### 4.1 Replay ordering analysis — no conversion priority

`POSITION_CONVERSION` does not receive a replay priority. The existing canonical order `(transaction_date, transaction_id)` remains sufficient for the approved whole-position primitive for the following reasons:

1. A BUY, SELL, INITIAL_POSITION, QUANTITY_CORRECTION, or another conversion that affects either the predecessor or successor on the valuation transition calendar date is invalid. Preflight and the independent validator must detect `POSITION_CONVERSION_SAME_DAY_CONFLICT` before applying the conversion. The transaction-ID order therefore cannot be used to make an otherwise ambiguous affected-asset sequence valid.
2. An existing successor position eligible for merge must exist before the transition date. A successor position created or changed on the transition date is a same-day conflict, not an ordering case.
3. Same-day transactions for unrelated assets operate on disjoint holding keys. Their ordinary cash and realized-P/L effects retain the repository's existing transaction-ID order. Introducing a conversion priority would rewrite that established order and could change path-sensitive diagnostics such as an intermediate negative-cash warning.
4. Cash-in-lieu is applied at the conversion row's existing canonical position. It is not authority to move the conversion ahead of or behind other same-day ledger facts.
5. Determinism is supplied by the transaction-ID tie-breaker after the calendar date; semantic ambiguity is removed by rejecting same-day affected-asset transactions, not by inventing intraday priority.

Accordingly, a same-day `BUY → POSITION_CONVERSION → SELL` sequence is handled as follows: if BUY or SELL targets the predecessor or successor, the sequence fails closed regardless of transaction IDs; if both target unrelated assets, all three rows replay in existing transaction-ID order. Supporting same-day affected-asset trading would require a separately governed intraday ordering contract and is outside WP2.

## 5. Architectural boundaries

### 5.1 Boundary with WP1

WP1 is a read-only dependency. WP2 may import and consume its immutable typed parse result, exact decimals, structured parse errors, and fingerprint. WP2 must not change any member of the 12-file frozen corpus.

### 5.2 Boundary between rebuilder and validator

The rebuilder and validator are two independent state machines:

- the rebuilder owns state mutation used to reconstruct holdings, cash, and cumulative realized P/L;
- the validator owns finding production and its own holdings/basis/cash replay;
- the validator must not import `_PortfolioState`, `_HoldingState`, `_apply_transaction`, or any other rebuilder mutation/helper;
- both may consume the frozen canonical value and the same constitutional constants, but accounting application and state mutation must be separately implemented and separately tested; and
- parity is proved by fixtures, not achieved by calling one implementation from the other.

The validator retains its existing raw-symbol-keyed `_ReplayState` as its one
authoritative economic state. WP2 augments that state with deterministic
conversion identity metadata and exact basis data, and conversion application
mutates that same state. A second or parallel conversion state is prohibited.
The validator must not import rebuilder replay state, mutation functions, or
identity helpers.

For the validator, identity metadata is derived independently for each actual
raw holding key from the validator's canonical transaction contexts. Legacy
candidate construction selects raw holding keys whose derived canonical symbol
equals the payload identity. Native construction selects the union of holding
keys matching the payload asset ID and holding keys matching the approved
canonical-symbol fallback. Candidate union is deduplicated by actual raw
holding key: zero distinct candidates is missing, one is selected, and more
than one is ambiguous. Asset-ID and canonical-symbol paths that identify
different holdings are therefore ambiguous and must never be resolved by
priority or heuristic. After validation succeeds, predecessor removal,
successor create/merge, cash, realized P/L, and identity metadata all mutate the
same `_ReplayState` consumed by `SELL_WITHOUT_HOLDING`, `CASH_MISMATCH`,
`HOLDINGS_MISMATCH`, and snapshot-cash checks.

### 5.3 Boundary with `replay_key()`

Existing `replay_key(ctx)` semantics and signature remain unchanged. Ordinary transaction replay continues to use it exactly as today.

Conversion identity is resolved locally from the payload:

- legacy mode uses canonical predecessor and successor symbols;
- asset-native mode prefers payload asset IDs;
- native predecessor lookup also admits the canonical predecessor-symbol fallback for historical transaction 83, whose `asset_id` is null;
- the candidate lookup set is deduplicated before matching;
- zero predecessor matches fail as missing; zero successor matches create the successor; more than one distinct holding match fails as ambiguous; and
- successor merge must also fail if asset-ID and symbol candidates resolve to conflicting existing holdings.

### 5.4 Boundaries with future packages

- WP3 supplies quote/epoch/quarantine behavior. WP2 only preserves the required `POSITION_CONVERSION_QUOTE_QUARANTINED` finding ID and severity in the conversion finding catalog; it does not fabricate or query quote evidence.
- WP4 supplies registry preparation and the only live authoring/materialization service. WP2 performs no registry query or mutation and no ledger insert.
- WP5 supplies hard `from_date` boundary enforcement, snapshot/return integration, and pre-boundary preservation. WP2 preserves `POSITION_CONVERSION_REBUILD_BOUNDARY` in the finding catalog but does not modify snapshot services or claim the WP5 gate.
- WP6 supplies derived time-series continuity.
- WP7 supplies the operator CLI and production-shaped rehearsal.
- WP8 supplies integrated release evidence.

Catalog presence in WP2 is not authorization to implement another package's evidence producer. **Presence in the catalog does not imply runtime production.** The two deferred predicates become active only in their constitutionally assigned packages.

Until WP5 is accepted, governance must keep conversion rows non-persistent in
every environment. WP2 and pre-WP5 evidence may use only transient,
rollback-isolated fixtures and dry-run or `skip_snapshots=True` rebuilds. It
must not contain a committed full-history conversion rebuild. WP4 acceptance
does not relax this sequencing rule or activate conversion authoring outside
rollback-isolated tests. The operational risk is that this is a procedural
guard rather than a WP2 runtime predicate; its owner is the BANPU remediation
governance sequence through WP5 acceptance. WP5 ownership and its future
runtime boundary remain unchanged.

## 6. Components affected

### 6.1 `backend/services/portfolio_rebuilder.py`

Required changes:

- add conversion-aware replay state sufficient to retain internal key, report symbol, asset ID, shares, average cost, sector, price symbol, and exact basis;
- add a conversion-specific controlled replay error carrying transaction ID and stable reason;
- add raw-row preflight for top-level identity/date agreement and duplicate keys;
- recognize both existing replay application sites: Stage 1 final-state replay and Stage 2 per-date snapshot replay;
- run raw-row preflight once in `rebuild_portfolio()` before either replay site, then retain its immutable verdict for both sites; Stage 2 must not invent a second raw-row interpretation;
- scope the replayed-conversion-key set to one replay invocation so Stage 1 and Stage 2 each reject duplicates within their own run without treating the other run as a duplicate;
- add local predecessor/successor candidate-key resolution without changing `replay_key()`;
- add the `POSITION_CONVERSION` application branch;
- preserve conversions regardless of `apply_repairs`; a `LedgerRepair` must never suppress or alter a permanent conversion fact;
- extend conversion-portfolio reconciliation and execution-plan reporting to asset ID and derived basis in addition to symbol, shares, and average cost;
- preserve every reinserted pre-existing `PortfolioItem.asset_id` across the existing delete-and-reinsert commit; do not transfer the removed predecessor ID; bind the conversion successor to the payload successor asset ID, fail on a conflicting non-null successor ID, and perform no registry lookup or general identity backfill;
- ensure `_PortfolioState.copy()` preserves every conversion-relevant holding field and run-local datum required by the per-date replay; and
- extend Stage 5 blocking so the required `ERROR`-severity same-day conflict is fail-closed without changing global handling of unrelated validator errors.

No snapshot-boundary, price-fetch, return-field, or quote behavior is added in WP2.

### 6.2 `backend/services/ledger_validator.py`

Required changes:

- recognize `POSITION_CONVERSION` through its conversion-specific preflight and do not add it to `_EQUITY_TYPES`; malformed conversions therefore produce their specific conversion findings without duplicate generic `NULL_SYMBOL` or `ZERO_SHARES` findings;
- add a conversion-specific validation preflight and deterministic finding mapping;
- retain the existing raw-keyed `_ReplayState`, augment it with deterministic canonical-symbol/asset-ID metadata and exact basis/average-cost data, and mutate that same authoritative state for conversion portfolios;
- construct, union, deduplicate, and classify legacy/native/canonical candidates independently from the rebuilder, including the historical null-asset fallback;
- keep the existing no-conversion replay path behaviorally unchanged;
- apply conversion arithmetic without importing rebuilder mutation;
- ensure predecessor removal and successor create/merge are immediately visible to existing sell, cash, holdings-consistency, and snapshot-cash checks;
- compare conversion portfolios to `PortfolioItem` by asset ID, symbol, shares, average cost, and basis; and
- sort findings using the existing severity/check-ID ordering and stable transaction ID/detail payloads.

### 6.3 Test components

Required focused coverage belongs in existing rebuilder and validator suites or one new `backend/tests/test_position_conversion_replay.py`. `test_replay_key.py` changes only if `replay_key.py` is exceptionally changed.

The mandatory regression command set also includes
`test_ledger_validator_effective.py`,
`test_portfolio_rebuilder_capability_shadow.py`,
`test_registry_replay_parity.py`, and `test_replay_cutover.py`; these suites own
raw/effective validator behavior, final-state consultation, public
reconciliation output, and native cutover behavior affected by WP2.

No frozen WP1 test is edited merely to make WP2 assertions fit; WP2 adds its own fixtures and preserves WP1 tests verbatim.

## 7. Replay changes

### 7.1 Preflight

Before applying a conversion, replay must deterministically validate:

1. the frozen parse result exists, has no errors, and contains a value;
2. the raw row's predecessor asset ID, predecessor symbol, and transition date agree with the payload;
3. predecessor and successor IDs are distinct and required symbols are present;
4. payload equations and top-level projections satisfy the frozen tolerances;
5. the conversion key has not already been replayed;
6. no same-day predecessor/successor equity conflict exists; and
7. no repair overlay can remove or mutate the conversion row.

Rebuilder raw-row preflight belongs to `rebuild_portfolio()` because that scope
owns the raw `Transaction` rows. It completes before Stage 1 or Stage 2 applies
a conversion, and its immutable conversion metadata/verdict is reused by both
replay sites. Application-local duplicate tracking is newly initialized for
each replay invocation; it is never shared between Stage 1 final-state replay
and Stage 2 per-date replay. Rebuilder preflight raises a controlled error
before database writes. Validator preflight records the corresponding finding
and does not apply the invalid conversion.

Repair-overlay enforcement occurs only at the authorized consumer boundaries
in `portfolio_rebuilder.py` and `ledger_validator.py`; `ledger_repair.py`
remains unchanged. An `EXCLUDE` repair targeting a conversion is ineffective:
the conversion remains in the effective canonical sequence and no new
conversion finding is emitted merely because the ineffective repair exists. A
`SUPPRESS_FINDING` repair cannot suppress an active conversion finding. Raw and
effective modes must therefore see identical conversion facts and findings.

### 7.2 Predecessor resolution

At the conversion point:

- the rebuilder resolves its candidates against its `replay_key()`-based holding keyspace;
- the validator resolves independently against actual keys in its authoritative raw-symbol holding state and never addresses that state directly with a registry-resolved canonical symbol;
- legacy validator candidates are the raw holding keys whose derived canonical symbol matches the canonical predecessor symbol;
- native validator candidates are the deduplicated union of asset-ID matches and canonical predecessor-symbol fallback matches;
- exactly one distinct holding must match;
- its shares must equal `shares_surrendered`; and
- its exact replay basis (`shares × average cost`, retained without float round-trip) must match `basis.before` within THB `0.01`.

Missing, multiple, partial, or split predecessor holdings fail closed.

### 7.3 Successor application

After all checks pass atomically in memory:

1. remove the predecessor holding;
2. resolve existing-successor candidates for the current replay mode;
3. create a successor holding with `Qr`, `Bs`, and `As`, or merge with an existing successor;
4. for a merge, compute `combined_basis = existing_basis + Bs`, `combined_shares = existing_shares + Qr`, and `combined_avg_cost = combined_basis / combined_shares`;
5. bind successor asset ID and canonical report symbol from the payload;
6. carry predecessor sector only when the successor has no sector;
7. add only `Cn` to cash and only `RP` to cumulative realized P/L; and
8. leave every unrelated holding unchanged.

The rebuilder uses its local `replay_key()`-compatible keyspace for successor
resolution. Independently, the validator applies the same candidate
construction form used for the predecessor to actual raw holding keys: legacy
uses derived canonical-symbol matches; native uses the deduplicated union of
asset-ID and canonical-symbol matches. Zero successor candidates means create
one canonical successor entry in the authoritative raw-keyed validator state;
one means merge it; more than one, or conflicting asset-ID/symbol paths, is
ambiguous and blocks application. Candidate metadata is then updated on that
same state so existing validator checks see only the successor after the
conversion point.

No-cash-in-lieu conversions must leave cash and realized P/L byte-equivalent to their pre-conversion values.

For every existing-successor merge, the following are explicit acceptance invariants evaluated with `Decimal` before any storage projection:

```text
existing_basis   = existing_shares × existing_avg_cost
converted_basis  = Bs
combined_basis   = existing_basis + converted_basis
combined_shares  = existing_shares + Qr
combined_avg_cost = combined_basis / combined_shares
combined_shares × combined_avg_cost = combined_basis
```

`Bf` is excluded from `converted_basis` because it is the basis disposed through cash-in-lieu. Neither `Cg`, `Cn`, fees, taxes, nor realized P/L may enter successor basis. The pre-merge existing successor basis and the carried conversion basis must each be independently recoverable from test evidence; an implementation that merely arrives at a plausible average cost without satisfying `combined_basis == existing_basis + converted_basis` is invalid.

### 7.4 Determinism

The rebuilder remains single-pass **per replay run** in canonical order. One
rebuild has two application sites over the same effective transaction list:
Stage 1 final-state replay and Stage 2 per-date snapshot replay. Each site owns
a fresh replay state and a fresh replayed-conversion-key set, consumes the same
preflight verdict, and applies each conversion exactly once in that run.
`_PortfolioState.copy()` must copy asset ID, report symbol, price symbol, exact
basis, sector, shares, average cost, and every other conversion-relevant field
used by a captured per-date state.

Replaying the same immutable input twice must produce equal holdings keys,
asset IDs, symbols, shares, basis, average costs, cash, realized P/L, findings,
and reconciliation output. For a conversion portfolio, the Stage 1 final state
and the terminal Stage 2 per-date state for the same terminal date must also be
equal. Legacy and native modes may use different internal keys but must produce
identical reported economic state.

## 8. Materialization changes

WP2 does not add the WP4 live materialization service. Its only materialization interaction is the existing rebuilder's reconstruction output and optional commit path.

For a conversion portfolio, reconstructed final state must:

- omit the predecessor item;
- contain exactly one successor item;
- set successor `asset_id` to the payload successor asset ID;
- set successor symbol to the canonical payload successor symbol;
- set shares and average cost from exact replay, quantized only at the existing storage boundary;
- preserve combined successor basis within the authoritative tolerance; and
- update portfolio cash only by admitted `Cn`.

Before delete-and-reinsert, rebuild materialization must construct a
deterministic preservation map from every current portfolio item. Unaffected
items are reinserted with their exact pre-existing `asset_id`, including
legitimate `NULL` values. The conversion successor is instead bound
authoritatively to the payload successor asset ID. If an existing successor
has a different non-null asset ID, materialization fails closed. Preservation
must use only already-loaded materialized identity and replay output: WP2 may
perform no registry lookup and no general identity backfill. Legacy and native
replay must produce the same persisted asset IDs.

The preservation map is keyed by the current item identity available before
deletion: the unique current symbol for ordinary items, and the conversion-only
asset-first/canonical-fallback pairing below for the successor. Each
reconstructed report symbol may consume at most one preservation entry; a
collision or conflicting mapping fails closed. The surrendered predecessor is
intentionally not reinserted and its asset ID is never transferred to another
item. Every other reinserted current item preserves its prior ID exactly.

Ordinary portfolio-item reconciliation remains the existing symbol-keyed,
two-field shares/average-cost behavior. Only the conversion successor uses the
five-field reconciliation path. That path pairs current and reconstructed
successor items by the following deterministic rule:

1. a unique current non-null `asset_id` equal to the payload successor asset ID has precedence;
2. when no asset-ID candidate exists, a unique canonical-symbol match is admitted, including a current item whose `asset_id` is `NULL`;
3. asset-ID and canonical-symbol paths that identify different items are ambiguous and fail closed; and
4. no candidate remains `MISSING`, while an unpaired current item remains `EXTRA`; the implementation must not invent a comparand.

After pairing, reconciliation reports five independent rows for `asset_id`,
`symbol`, `shares`, `avg_cost`, and derived `basis = shares × avg_cost`. A
pre-commit `NULL asset_id` admitted through symbol fallback is valid merge input
but is `DIFFERENT` from the authoritative payload successor ID. A different
non-null ID is a conflict. Before commit, every actual field delta is visible;
after a successful item-only commit, all five successor rows must be `MATCH`.
A symbol mismatch is independently visible when asset-ID pairing supplies the
real comparand. Rebuilder commit remains atomic under its existing transaction
boundary and remains blocked by conversion-critical findings and the same-day
conflict error.

WP2 must not create or update `Transaction`, `Asset`, `AssetIdentifier`, `AssetRelationship`, cache, or snapshot rows as conversion-specific behavior.

## 9. Validator interactions

### 9.1 Finding catalog

| Check ID | Severity | WP2 predicate status |
|---|---|---|
| `POSITION_CONVERSION_PAYLOAD_INVALID` | CRITICAL | Active in WP2 |
| `POSITION_CONVERSION_IDENTITY_INVALID` | CRITICAL | Active in WP2 |
| `POSITION_CONVERSION_DUPLICATE` | CRITICAL | Active in WP2 |
| `POSITION_CONVERSION_WITHOUT_HOLDING` | CRITICAL | Active in WP2 |
| `POSITION_CONVERSION_AMBIGUOUS_HOLDING` | CRITICAL | Active in WP2 |
| `POSITION_CONVERSION_SHARE_MISMATCH` | CRITICAL | Active in WP2 |
| `POSITION_CONVERSION_BASIS_MISMATCH` | CRITICAL | Active in WP2 |
| `POSITION_CONVERSION_CIL_INVALID` | CRITICAL | Active in WP2 |
| `POSITION_CONVERSION_SAME_DAY_CONFLICT` | ERROR | Active and Stage-5-blocking in WP2 |
| `POSITION_CONVERSION_REBUILD_BOUNDARY` | CRITICAL | Catalogued in WP2; predicate remains WP5-owned |
| `POSITION_CONVERSION_QUOTE_QUARANTINED` | CRITICAL | Catalogued in WP2; predicate remains WP3-owned |

### 9.2 Deterministic predicate mapping

- Parser/schema/version errors map to `PAYLOAD_INVALID`.
- Top-level/payload identity or transition-date disagreement, same-asset conversion, or unusable identity fields map to `IDENTITY_INVALID`.
- A repeated predecessor/date conversion key maps to `DUPLICATE`.
- Zero predecessor matches maps to `WITHOUT_HOLDING`; multiple distinct matches maps to `AMBIGUOUS_HOLDING`.
- Full-position, entitlement, received-share, or top-level share projection disagreement maps to `SHARE_MISMATCH`.
- Replay basis, basis allocation, carried basis, average-cost, or top-level basis projection disagreement maps to `BASIS_MISMATCH`.
- Null/non-null cash-leg inconsistency or any `Cg/F/T/Cn/Bf/RP` equation or projection disagreement maps to `CIL_INVALID`.
- Another predecessor/successor equity transaction on the transition calendar date maps to `SAME_DAY_CONFLICT`.
- `POSITION_CONVERSION` is not added to `_EQUITY_TYPES`; its required symbol and projection checks map only through the conversion-specific predicates above.

One invalid transaction may produce multiple non-duplicative findings when independent invariants fail. Findings must contain the conversion transaction ID, stable symbols, and exact decimal values serialized as strings in details.

### 9.3 Stage 5 and repairs

- Any active WP2 CRITICAL finding blocks rebuild commit.
- `POSITION_CONVERSION_SAME_DAY_CONFLICT` blocks rebuild commit despite its constitutionally fixed `ERROR` severity.
- Conversion findings must not be suppressible through `LedgerRepair`.
- Raw and effective validation modes must include the same conversion rows and conversion findings; repair overlays may continue to affect only already-supported non-conversion behavior.
- Portfolios without conversions retain existing finding behavior and existing Stage 5 policy.

## 10. Failure behavior

- Rebuilder preflight or replay failure before Stage 5 returns `success=False`, `aborted=False`, `committed=False`, and a stable non-empty conversion error; no persistent mutation is staged or committed.
- A Stage-5-active conversion CRITICAL or `POSITION_CONVERSION_SAME_DAY_CONFLICT` returns `success=True`, `aborted=True`, and `committed=False` through the existing completed-but-blocked boundary.
- A commit exception returns `success=False`, `aborted=False`, `committed=False` after rollback. Dry-run success without an active blocking finding returns `success=True`, `aborted=False`, `committed=False`.
- Validator: emit deterministic findings, skip application of the invalid conversion, continue only far enough to report independent ledger evidence safely, and never throw for an ordinary malformed payload already representable by the WP1 parse result.
- Duplicate or ambiguous identity: do not choose a winner.
- Projection or arithmetic mismatch: do not coerce, round into tolerance, or repair the payload.
- Existing-successor conflict: do not merge when identity candidates disagree.
- Cash-in-lieu failure: apply neither cash nor realized P/L.
- Unexpected internal exception: preserve the existing outer rollback behavior and expose a stable failure result; no conversion-specific catch may turn an exception into success.
- No-conversion portfolio: follow the current path with no new findings or state changes.

Rollback during WP2 development is code-only: revert the WP2 implementation
and tests as one package after rolling back every transient conversion fixture.
The unused additive WP1 schema remains valid and frozen. No WP1 downgrade or
amendment is part of WP2 rollback. Once a persistent conversion row is later
authorized after the WP5 gate, conversion-unaware code must not be used there;
this is a future deployment concern, not WP2 production authority.

## 11. Acceptance criteria

WP2 is acceptable only when all of the following are demonstrated:

1. Frozen-corpus hashes remain exactly those in `BANPU_WP1_FREEZE_RECORD.md`.
2. No prohibited file or M46 file changes.
3. BANPU fixture `Qp=6700`, `R=0.38242`, `Qe=2562.214`, `B0=48709.00` produces the approved full-share outcome when `Qr=Qe`: successor basis `48709.00`, cash delta `0`, realized-P/L delta `0`, and average cost derived from exact basis/shares.
4. An incident-independent generic fixture uses arbitrary asset identities and `Qp=8`, `R=1.25`, `Qe=10`, `Qr=9.5`, `Qf=0.5`, `B0=240`, `Bf=12`, `Bs=228`, `Cg=15`, `F=1`, `T=0.5`, `Cn=13.5`, and `RP=1.5`; it must satisfy every frozen equation without BANPU symbols, dates, or transaction IDs.
5. A broker-rounded fixture applies exact admitted `Qr`, `Bf`, `Bs`, `Cn`, and `RP` and no synthetic SELL/external-flow behavior.
6. Existing successor merge satisfies `combined_basis == existing_basis + converted_basis`, `combined_shares == existing_shares + Qr`, and `combined_avg_cost == combined_basis / combined_shares` using exact pre-projection values.
7. Legacy-symbol and asset-native modes produce identical reported asset ID, symbol, shares, average cost, basis, cash, and realized P/L.
8. Native replay succeeds for the historical null-asset predecessor fallback only when exactly one predecessor match exists.
9. A raw ledger predecessor symbol that differs from its canonical and payload symbol resolves to exactly one validator holding in both replay modes; zero and multiple distinct raw candidates fail with the specified findings, and existing validator consistency checks observe the converted state.
10. A same-day affected-asset BUY/SELL/correction fails closed; same-day unrelated transactions retain `(transaction_date, transaction_id)` order; no conversion priority exists.
11. Malformed, identity-invalid, duplicate, missing, ambiguous, share-mismatched, basis-mismatched, cash-in-lieu-invalid, and same-day-conflict cases cannot commit through rebuild.
12. Stage 1 final-state replay and the terminal Stage 2 per-date replay state are equal for a conversion portfolio, with fresh per-run duplicate tracking and complete state copying.
13. Every reinserted pre-existing `PortfolioItem.asset_id` is preserved through conversion-portfolio delete-and-reinsert: unaffected IDs remain exact, an already-correct successor ID remains exact, a successor `NULL` is authoritatively bound to the payload ID, and a conflicting non-null successor ID fails closed without registry access or backfill; the surrendered predecessor is intentionally not reinserted and its ID is never transferred.
14. Conversion-only reconciliation uses asset-ID precedence and unique canonical-symbol fallback; ambiguity fails closed, pre-commit null-ID binding is `DIFFERENT`, post-commit successor identity is `MATCH`, and all five fields are independently visible. Ordinary reconciliation remains unchanged.
15. Repeated replay is deterministic and idempotent in memory.
16. Conversion remains authoritative in raw/effective and `apply_repairs` true/false paths; an `EXCLUDE` repair is ineffective and a conversion finding cannot be suppressed.
17. Before WP5 acceptance, all conversion rows used by WP2 evidence are transient and rollback-isolated; rebuild evidence is dry-run or `skip_snapshots=True`, and no committed full-history conversion rebuild is accepted.
18. Failure fixtures assert the exact `success`, `aborted`, and `committed` disposition defined in §10.
19. Existing rebuilder, validator, replay-key, repair-validation, effective-validator, capability-shadow, registry-parity, and replay-cutover tests remain green without changed expected behavior for no-conversion portfolios.
20. No database/network/registry/quote access is introduced into canonicalization or local conversion-key derivation.
21. No live authoring path, CLI, API, registry mutation, snapshot boundary, or future-package implementation is present.

## 12. Verification strategy

### 12.1 Focused unit and state-machine tests

- full-share BANPU arithmetic;
- the incident-independent generic arithmetic fixture;
- cash-in-lieu with fractional entitlement, fees, taxes, net cash, basis allocation, and realized P/L;
- no-cash-in-lieu invariance;
- existing-successor create/merge with explicit combined-basis conservation;
- legacy, native, historical-null-asset fallback, zero-match, and multi-match identity cases;
- raw-symbol validator holdings whose canonical and payload symbols differ, including candidate union, deduplication, and conflicting match paths;
- top-level/payload identity and date mismatch;
- duplicate predecessor/date key and repeated replay;
- all active WP2 finding IDs and exact severities;
- same-day conflict Stage 5 blocking;
- no-priority ordering proof: affected-asset same-day rejection and unrelated-asset transaction-ID ordering;
- equality of Stage 1 final state and terminal Stage 2 per-date state, including `_PortfolioState.copy()` coverage and fresh per-run duplicate tracking;
- raw/effective repair parity, ineffective conversion `EXCLUDE`, and unsuppressible conversion findings;
- preservation of every pre-existing item asset ID, authoritative successor binding, conflict detection, and no registry/backfill behavior;
- conversion-only five-field reconciliation, null-ID pre-commit difference, and post-commit match;
- exact rebuild-result field dispositions for replay failure, Stage-5 blocking, dry run, and commit failure; and
- exact malformed-conversion finding sets proving `_EQUITY_TYPES` is unchanged.

### 12.2 Parity fixtures

Run each valid economic fixture through the rebuilder state machine and the independent validator state machine. Compare final successor asset ID, symbol, shares, basis, average cost, cash, and realized P/L. The test must not share expected-state construction through either implementation.

### 12.3 Regression suites

At minimum:

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
```

Add the focused WP2 test file to the command set if created. Run from the repository's supported test environment and record exact commands and results.

### 12.4 Boundary and governance verification

- compare all 12 frozen WP1 file hashes to the freeze record;
- inspect `git diff --name-only` against the WP2 allowlist;
- verify M46 hashes/status are unchanged;
- search for unauthorized conversion write paths, API/CLI/frontend additions, registry mutation, quote/cache code, snapshot-boundary code, and generic corporate-action abstractions;
- prove all conversion rows in WP2 evidence are transient, all rebuild evidence is dry-run or `skip_snapshots=True`, and no committed full-history conversion rebuild is present before WP5 acceptance;
- defer synchronization of frozen `ARCHITECTURE.md` and `PORTFOLIO_CALCULATION_RULES.md`, and any BANPU business-rule entry in `docs/engineering/DECISION_LOG.md`, to the separately approved WP8 documentation-correction owner; WP2 must not modify any of those files; and
- run `graphify update .` after accepted implementation changes and review the scoped graph change surface.

## 13. Implementation risks and rollback considerations

| Risk | Required mitigation | Rollback consideration |
|---|---|---|
| Legacy/native keys identify the same holding twice | Deduplicate candidate keys and fail on multiple distinct matches | Revert WP2; never select a candidate heuristically |
| Validator accidentally reuses rebuilder logic | Separate private state and mutation, parity only through fixtures | Reject review; independence is an acceptance gate |
| Float projections contaminate exact basis | Carry `Decimal` basis through replay; quantize only at existing persistence/report boundaries | No data repair; revert code before conversion authoring exists |
| Existing successor merge loses basis | Test combined-basis equation directly | Revert package; do not compensate in WP4 |
| Repair overlay suppresses a conversion | Preserve conversion rows in both modes and add explicit tests | Reject commit; do not modify `LedgerRepair` data |
| Same-day `ERROR` passes current CRITICAL-only gate | Add check-ID-specific blocking without changing global error policy | Revert isolated gate change with WP2 |
| Rebuilder commit drops or misbinds `asset_id` | Reconcile asset ID before commit and verify successor materialization | Existing transaction rows remain append-only; rollback transaction on failure |
| Rebuilder delete-and-reinsert erases unrelated item identity | Preserve every current item asset ID deterministically; override only the authorized successor and fail on conflict | Roll back the entire rebuild transaction; perform no registry repair or backfill |
| Validator canonical lookup misses raw-keyed holding or creates parallel authority | Mutate one augmented raw-keyed `_ReplayState`; test raw≠canonical candidate union and existing checks | Revert WP2 validator changes; never use a parallel conversion state |
| Stage 1 and Stage 2 replay diverge | Share immutable preflight evidence, use fresh per-run duplicate sets, copy all conversion fields, and assert terminal equality | Reject the candidate; do not accept one replay site as authoritative |
| Pre-WP5 full-history rebuild rewrites predecessor history | Permit only transient rows and dry-run/`skip_snapshots` evidence; prohibit committed full-history evidence until WP5 | Remove the transient fixture state; no runtime boundary is added in WP2 |
| Conversion reconciliation hides symbol/asset mismatch | Use conversion-only asset-first pairing, unique canonical fallback, and five independent rows | Reject ambiguous pairing; leave ordinary reconciliation unchanged |
| Catalog wording leaks into WP3/WP5 | Keep deferred predicates dormant and explicitly owned by later packages | Remove unauthorized implementation, not the frozen catalog IDs |
| No-conversion behavior drifts | Retain existing validator path and golden regression tests | Revert WP2 production files together |
| WP1 corpus is accidentally edited | Hash gate before review and acceptance | Restore only from the frozen corpus identity under governance; do not amend |

No production rollback is authorized by this plan. WP2 must be completed and accepted while no authorized conversion write path exists.
