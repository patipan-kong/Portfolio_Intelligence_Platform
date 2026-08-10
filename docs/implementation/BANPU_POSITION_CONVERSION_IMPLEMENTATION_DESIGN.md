# BANPU Position Conversion Remediation — Canonical Implementation Design

**Status:** APPROVED IMPLEMENTATION SPECIFICATION
**Authority:** Root Cause Analysis, Independent Architectural Review, and approved implementation design
**Delivery class:** Independent production incident remediation
**M46 relationship:** None. M46 remains frozen and implementation-suspended.
**Implementation state:** BANPU-WP1 implementation complete; independently approved and confirmed with recorded residuals; freeze pending

This document is the authoritative implementation specification for the BANPU production incident remediation. Implementations, work packages, migrations, tests, operator tooling, and production execution MUST conform to it. The companion roadmap and sequence may decompose or order this design but MUST NOT alter it.

## 1. Scope

This remediation adds one append-only portfolio-ledger operation, `POSITION_CONVERSION`, and the minimum supporting behavior required to convert an existing predecessor holding into its registered successor after an amalgamation.

The implementation covers:

- one new transaction type and its structured payload;
- one additive transaction-schema migration and one duplicate-prevention index;
- canonicalization, deterministic replay, and independent ledger validation;
- atomic live `PortfolioItem` materialization;
- successor asset and provider-identifier binding;
- quote-epoch validation and fail-closed quarantine;
- bounded snapshot reconstruction that cannot reprice predecessor history;
- explicit fractional-share cash-in-lieu accounting;
- conversion-aware derived portfolio and shadow time series;
- operator-only application, verification, deployment, and recovery procedures.

The first production use is the BANPU predecessor position. The implementation MUST be data-driven through the transaction payload and asset registry; it MUST NOT contain a branch keyed to `BANPU`, `BANPU.BK`, `BANPUU.BK`, portfolio 2, or transaction 83.

## 2. Goals

1. Convert the predecessor position to its successor without rewriting the existing ledger.
2. Preserve total basis except for an explicitly admitted cash-in-lieu basis disposal.
3. Preserve cash and realized P/L when no cash-in-lieu exists.
4. Account exactly for cash, basis, fees, taxes, and realized P/L when cash-in-lieu exists.
5. Produce identical economic state under legacy-symbol and asset-native replay modes.
6. Prevent predecessor and successor quote epochs from being mixed.
7. Preserve every pre-transition portfolio and shadow snapshot value.
8. Preserve all existing behavior for portfolios without `POSITION_CONVERSION`.
9. Make conversion application idempotent, auditable, atomic, and fail-closed.

## 3. Non-goals

- A general corporate-action framework or vocabulary.
- Split, spin-off, rights, tender, dividend election, or multi-successor support.
- Changes to BUY, SELL, DEPOSIT, WITHDRAW, DIVIDEND, INITIAL_POSITION, INITIAL_CASH, or QUANTITY_CORRECTION semantics.
- A new `LedgerRepair` type or use of the repair tier as economic content.
- A public web API or frontend workflow for conversions.
- Renaming or reusing the predecessor `Asset`.
- Rewriting transaction 83 or any other existing transaction.
- Repricing or rebuilding pre-transition history from provider data.
- Rewriting immutable recommendations, optimizer history, execution decisions, or grades.
- Any M46 source, planning, status, or governance change.

## 4. Design principles

1. **Append-only authority.** The conversion is a new `Transaction`, never an edit or replacement.
2. **Transaction tier, not repair tier.** A permanent economic fact cannot be toggled by `LedgerRepair` or disappear under `apply_repairs=False`.
3. **One narrow primitive.** `POSITION_CONVERSION` represents a whole-position predecessor-to-successor conversion only.
4. **Exact payload arithmetic.** Decimal strings in the payload are authoritative; existing floating-point columns are compatibility projections.
5. **Atomicity.** Transaction insertion, portfolio materialization, cash application, and postconditions commit or roll back together.
6. **Deterministic replay.** Live processing and replay implement the same equations, while the ledger validator retains an independent replay implementation.
7. **Identity before symbol.** Successor valuation is bound to an asset, current provider identifier, and quote epoch.
8. **Fail closed.** Invalid payload, identity ambiguity, duplicate conversion, unsafe quote epoch, or reconstruction-boundary violation prevents commit or publication.
9. **Historical immutability.** Pre-transition accounting and derived values remain unchanged. Metadata-only identity enrichment is permitted when numeric fields are proven unchanged.
10. **No unaffected drift.** Existing types, portfolios without conversions, legacy cache keys, and existing public API behavior remain unchanged.

## 5. Accounting model

Let:

- `Qp` = predecessor shares surrendered;
- `R` = conversion ratio;
- `Qe = Qp × R` = successor shares entitled;
- `Qr` = successor shares actually received;
- `Qf = Qe - Qr` = fractional entitlement settled in cash;
- `B0` = predecessor basis before conversion;
- `Bf` = basis allocated to the cash-in-lieu disposal;
- `Bs = B0 - Bf` = basis carried to successor shares;
- `Cg` = gross cash-in-lieu proceeds;
- `F` = cash-in-lieu fees;
- `T` = cash-in-lieu taxes;
- `Cn = Cg - F - T` = net cash received;
- `RP = Cn - Bf` = realized P/L;
- `As = Bs / Qr` = successor average cost.

Required equations:

```text
Qe = Qp × R
Qf = Qe - Qr
B0 = Bs + Bf
Cn = Cg - F - T
RP = Cn - Bf
As = Bs / Qr
```

Without cash-in-lieu, `Qf`, `Bf`, `Cg`, `F`, `T`, `Cn`, and `RP` are zero; therefore basis, cash, and realized P/L are unchanged.

With cash-in-lieu, the cash leg is internal disposal proceeds, not an external flow. It MUST NOT be represented by a synthetic SELL and MUST NOT contribute to deposit, withdrawal, imported-asset, or manual-adjustment values.

For the known BANPU facts before broker rounding adjudication:

```text
Qp = 6700
R  = 0.38242
Qe = 2562.214
B0 = THB 48709.00
```

If all `2562.214` shares were credited, `Bs = B0` and `As ≈ THB 19.010512`. The production manifest MUST use broker-confirmed `Qr`, cash-in-lieu, and basis allocation.

## 6. `POSITION_CONVERSION` specification

### 6.1 Existing column semantics

| Column | Required meaning |
|---|---|
| `transaction_type` | Literal `POSITION_CONVERSION` |
| `symbol` | Predecessor symbol at transition |
| `asset_id` | Mandatory predecessor asset ID; it equals `conversion_payload.predecessor.asset_id` |
| `shares` | Successor shares actually received (`Qr`) |
| `price_per_share` | Successor average cost (`As`) |
| `total_amount` | Basis carried to successor (`Bs`) |
| `fees` | `F`; zero without cash-in-lieu |
| `taxes` | `T`; zero without cash-in-lieu |
| `currency` | Cash-in-lieu currency; THB for BANPU |
| `exchange_rate` | `1.0` for BANPU |
| `transaction_date` | The timezone-free `valuation_transition_date` stored as naive midnight `YYYY-MM-DD 00:00:00`; this is a business-effective date representation, not an instant |
| `sector` | Sector carried from predecessor unless successor already has one |
| `notes` | Human-readable summary only; never parsed for accounting |
| `conversion_payload` | Authoritative structured contract below |

### 6.2 Payload contract

`conversion_payload` MUST be JSON with `schema_version = 1`. Every decimal value MUST be serialized as a base-10 string.

```json
{
  "schema_version": 1,
  "predecessor": {
    "asset_id": 27,
    "symbol": "BANPU.BK",
    "shares_surrendered": "6700"
  },
  "successor": {
    "asset_id": 123,
    "symbol": "BANPUU.BK",
    "provider_symbol": "BANPUU.BK",
    "shares_entitled": "2562.214",
    "shares_received": "2562.214"
  },
  "conversion_ratio": "0.38242",
  "basis": {
    "before": "48709.00",
    "allocated_to_cash_in_lieu": "0.00",
    "carried_to_successor": "48709.00"
  },
  "cash_in_lieu": null,
  "dates": {
    "legal_effective_date": "YYYY-MM-DD",
    "valuation_transition_date": "YYYY-MM-DD",
    "predecessor_last_price_date": "YYYY-MM-DD",
    "successor_quote_epoch_start_date": "YYYY-MM-DD"
  },
  "quote_binding": {
    "provider": "YAHOO",
    "predecessor_provider_symbol": "BANPU.BK",
    "successor_provider_symbol": "BANPUU.BK"
  },
  "boundary_evidence": {
    "predecessor_reference_price": "DECIMAL",
    "successor_reference_price": "DECIMAL",
    "mechanical_nav_tolerance_pct": "0.50",
    "suspension_gap_annotation": "TEXT"
  },
  "evidence": {
    "reference": "BROKER_OR_OFFICIAL_REFERENCE",
    "source": "TEXT",
    "captured_at": "RFC3339_TIMESTAMP"
  }
}
```

When cash-in-lieu exists, `cash_in_lieu` MUST contain decimal strings for `fractional_entitlement_shares`, `gross_proceeds`, `fees`, `taxes`, `net_cash`, `basis_allocated`, and `realized_pnl`. Otherwise it MUST be JSON null and every corresponding top-level numeric projection MUST be zero.

### 6.3 Invariants

- Predecessor and successor asset IDs are non-null, distinct, and registry-resolved.
- The predecessor is held exactly once at the replay point.
- `shares_surrendered` equals the entire predecessor holding.
- All equations in section 5 hold under `Decimal` arithmetic.
- Replayed predecessor basis equals `basis.before` within the authoritative absolute basis tolerance of THB `0.01`.
- Top-level `shares`, `price_per_share`, `total_amount`, `fees`, and `taxes` match their payload projections within the authoritative absolute storage tolerance of `0.000001` per field. The tolerance exists only for the legacy floating-point columns; payload arithmetic remains exact `Decimal` arithmetic.
- `transaction_date` equals the timezone-free ISO calendar date in `valuation_transition_date` and stores it as naive midnight `YYYY-MM-DD 00:00:00`. Database-session, host-timezone, UTC, and offset conversion do not participate in its interpretation.
- The successor quote epoch begins no later than the valuation transition date.
- No other predecessor or successor equity transaction shares the transition calendar date.
- Exactly one `POSITION_CONVERSION` may exist for the same portfolio, non-null predecessor asset ID, and timezone-free valuation transition calendar date. The database rejects a conversion whose top-level predecessor `asset_id` is null or whose `transaction_date` is not its naive-midnight representation.
- Invalid or unsupported payload versions are not replayable.

## 7. Database schema

Add exactly one nullable column to `transactions`:

```text
conversion_payload JSON NULL
```

Use PostgreSQL `JSONB` in production and SQLAlchemy `JSON` for SQLite tests. Existing rows remain null. The column is required by application validation only when `transaction_type = 'POSITION_CONVERSION'`.

Add one partial unique index:

```text
uq_tx_position_conversion_portfolio_predecessor_date
    ON transactions (portfolio_id, asset_id, transaction_date)
    WHERE transaction_type = 'POSITION_CONVERSION'
```

Add one named conversion-specific constraint:

```text
ck_tx_position_conversion_identity_date
    transaction_type <> 'POSITION_CONVERSION'
    OR (
        asset_id IS NOT NULL
        AND transaction_date IS NOT NULL
        AND transaction_date is the timezone-free naive-midnight representation
    )
```

PostgreSQL enforces naive midnight by equality with `date_trunc('day', transaction_date)`. SQLite enforces an offset-free `YYYY-MM-DD 00:00:00` representation; its legacy compatibility path may use equivalent `BEFORE INSERT` and `BEFORE UPDATE` triggers where SQLite cannot add a table constraint in place. Physical DDL may differ, but both dialects MUST reject the same conversion values.

The constraint and the unchanged partial unique index jointly enforce uniqueness by portfolio, predecessor asset, and transition calendar date. Top-level `asset_id` is the indexed predecessor identity. WP2 independently detects identity/date mismatches during replay, and WP4 ensures top-level `asset_id` equals the registry-resolved payload predecessor; the database does not compare JSON paths.

No new table, successor column, ratio column, transaction status, or repair schema is permitted.

The migration and SQLite compatibility path MUST be idempotent. Downgrade MUST refuse to remove the column while any `POSITION_CONVERSION` row exists.

## 8. Replay model

### 8.1 Canonicalization

Add an immutable typed `PositionConversion` value to `CanonicalTransaction`. Canonicalization parses payload decimals and dates once and performs no database or network access.

Malformed payloads remain representable with a structured parse error so ledger validation can report them. Replay MUST raise a controlled fail-closed error rather than ignore such a row.

### 8.2 Application

The rebuilder branch MUST:

1. validate the typed payload;
2. locate exactly one predecessor holding;
3. reconcile `Qp` and `B0`;
4. remove the predecessor;
5. create or merge the successor using `Qr` and `Bs`;
6. set successor average cost to combined successor basis divided by combined successor shares;
7. carry the sector and bind the successor provider symbol;
8. add only admitted `Cn` to cash and `RP` to cumulative realized P/L;
9. leave every unrelated holding unchanged.

An existing successor holding is supported by combining its existing shares and basis with the converted shares and basis.

### 8.3 Replay identity modes

Legacy mode uses canonical predecessor and successor symbols. Asset-native mode prefers asset IDs. Because historical transaction 83 has null `asset_id`, native predecessor lookup MUST also check the canonical predecessor-symbol fallback. Exactly one key may match; zero or multiple matches fail.

The conversion MUST produce identical shares, basis, cash, and realized P/L under both portfolio replay modes.

### 8.4 Ordering and reconstruction boundary

Existing canonical ordering `(transaction_date, transaction_id)` remains unchanged. Same-day affected-asset transactions are rejected to avoid creating an intraday ordering model.

Snapshots before the transition contain the predecessor. Snapshots on and after it contain the successor.

If a portfolio contains a conversion, snapshot rebuilding MUST fail with `POSITION_CONVERSION_REBUILD_BOUNDARY` when `from_date` is absent or predates the earliest transition. Pre-transition snapshots MUST be priced from their stored values and MUST NOT be re-fetched under a reused ticker.

## 9. Live materialization

Add a CLI-consumed `execute_position_conversion()` service. Its inputs are portfolio ID, both asset IDs, expected predecessor quantity and basis, ratio, broker-confirmed received quantity, optional cash-in-lieu facts, dates, and evidence reference. Symbols and provider identifiers are resolved from the registry, not trusted from arbitrary input strings.

Within one database transaction the service MUST:

1. lock the portfolio and relevant `PortfolioItem` rows;
2. resolve and validate both assets and current identifiers;
3. locate the predecessor by asset ID with a controlled legacy-symbol fallback;
4. verify optimistic quantity and basis expectations;
5. reject a conflicting duplicate and return `already_applied` for an identical canonical fingerprint;
6. insert the append-only transaction;
7. remove or transform the predecessor materialization;
8. create or merge the successor materialization;
9. apply the optional cash-in-lieu cash leg;
10. assert final shares, basis, cash, and identity before commit.

The successor MUST be a new `Asset`. The predecessor asset is not renamed. Registry preparation MUST establish a current successor `PROVIDER_SYMBOL`, retire the predecessor identifier (`is_current=False`), transition the predecessor to `MERGED`, and link predecessor to successor with the existing `MERGED_INTO` relationship. The ratio belongs only in the transaction payload.

The only write entry point is an operator CLI:

```text
python manage.py apply_position_conversion --manifest FILE --dry-run
python manage.py apply_position_conversion --manifest FILE --commit
```

Dry-run is the default. No public API or frontend authoring surface is added.

## 10. Market-data protection

Provider adaptation MUST verify normalized requested symbol against provider `meta.symbol`, associate each close with its timestamp, and derive current and previous close from one result. A close before the successor epoch MUST never become successor `previous_close`; on the first successor observation, `previous_close = None` is valid.

Converted holdings use an explicit binding:

```text
asset_id + provider + provider_symbol + quote_epoch_start_date + valuation_transition_date
```

Their existing market-data cache rows are namespaced through `cache_type`, for example:

```text
quote:asset=<asset_id>:epoch=<date>
history:5y:1d:asset=<asset_id>:epoch=<date>
```

No cache schema change is required. Unconverted assets retain existing symbol-based keys.

Before activation, mechanical boundary value MUST reconcile within the payload tolerance using evidence-bound reference prices. A genuine price move over the trading suspension is recorded as investment return through `suspension_gap_annotation`; it is not an external flow or repair.

The converted holding is quarantined for missing or ambiguous identifiers, provider-symbol mismatch, cross-epoch timestamps, wrong cache namespace, missing/non-positive prices, mechanical continuity failure, or an unannotated boundary discontinuity. Quarantine returns no usable affected price, serves no predecessor stale cache, blocks affected snapshots and downstream optimizer/evaluation refresh, and emits a structured reason. Unaffected assets continue normally.

## 11. Validator changes

`POSITION_CONVERSION` becomes a symbol-bearing equity type. The independent validator replay MUST mirror the accounting equations without importing the rebuilder's state mutation.

Required findings:

| Check ID | Severity |
|---|---|
| `POSITION_CONVERSION_PAYLOAD_INVALID` | CRITICAL |
| `POSITION_CONVERSION_IDENTITY_INVALID` | CRITICAL |
| `POSITION_CONVERSION_DUPLICATE` | CRITICAL |
| `POSITION_CONVERSION_WITHOUT_HOLDING` | CRITICAL |
| `POSITION_CONVERSION_AMBIGUOUS_HOLDING` | CRITICAL |
| `POSITION_CONVERSION_SHARE_MISMATCH` | CRITICAL |
| `POSITION_CONVERSION_BASIS_MISMATCH` | CRITICAL |
| `POSITION_CONVERSION_CIL_INVALID` | CRITICAL |
| `POSITION_CONVERSION_SAME_DAY_CONFLICT` | ERROR |
| `POSITION_CONVERSION_REBUILD_BOUNDARY` | CRITICAL |
| `POSITION_CONVERSION_QUOTE_QUARANTINED` | CRITICAL |

For a portfolio containing a conversion, validation compares materialized successor asset ID, symbol, shares, average cost, and basis with replay. Portfolios without conversions retain their current finding behavior.

Duplicate defense is mandatory at write-path, database-index, and replay layers.

## 12. Derived accounting and identity continuity

Portfolio metrics, live snapshots, rebuild return fields, and snapshot return recovery MUST deliberately classify conversion as zero external/import/manual flow. They include cash-in-lieu fees and realized P/L only when the payload admits that leg.

Derived BANPU holdings JSON MUST carry a non-null predecessor asset ID before the boundary and successor asset ID after it. Metadata-only enrichment of pre-boundary rows is permitted only when hashes or field comparisons prove all numeric values unchanged.

Succession-aware lookups in quant, attribution, shadow, horizon grading, and ideal-series consumers use the effective-dated `MERGED_INTO` edge. Source recommendations and historical decisions retain their original symbols and are never rewritten.

Shadow portfolios apply the same conversion schedule to replay-time working holdings. Paper shares use the exact ratio and remain fractional; broker-specific cash-in-lieu is not applied to hypothetical holdings. Shadow `inception_price` is divided by the ratio to preserve inception value. Regeneration may replay from inception in memory but writes only rows on or after the boundary and proves pre-boundary rows unchanged.

## 13. Migration strategy

1. Apply the additive schema migration with no transaction backfill.
2. Deploy read, canonicalization, replay, validation, and quarantine support before any conversion row exists.
3. Prepare registry data idempotently.
4. Populate the conversion only through a reviewed manifest and operator command.
5. Enrich only required BANPU-derived identity metadata; preserve all numeric history.
6. Rebuild portfolio and shadow rows only from the transition date.

The manifest, registry preparation, conversion insertion, cache purge, and rebuild commands MUST be safe to repeat. A matching conversion fingerprint is a no-op; a conflicting fingerprint is an error.

## 14. Deployment strategy

1. Quarantine BANPU valuation, snapshots, optimizer runs, and shadow refresh.
2. Capture a scoped backup of portfolio, ledger, items, snapshots, registry, caches, and affected shadow rows.
3. Deploy quote identity/epoch protection first.
4. Apply the additive migration.
5. Deploy conversion readers, replay, validator, accounting, shadow, and CLI support with no conversion row present.
6. Prepare successor registry identity and relationship.
7. Purge predecessor and successor quote/history caches.
8. Validate successor-epoch quote evidence.
9. Dry-run the broker-confirmed conversion manifest.
10. Verify both replay modes and all validator gates.
11. Commit conversion and live materialization atomically.
12. Rebuild portfolio snapshots from the transition date only.
13. Regenerate affected shadow snapshots from that date only.
14. Run production verification and remove quarantine only after every gate passes.

## 15. Rollback strategy

Before conversion commit, application code may be rolled back and the unused additive migration may remain or be safely downgraded.

The conversion write and live materialization are one transaction; a failure before commit rolls back both.

After conversion commit, code that does not understand `POSITION_CONVERSION` MUST NOT be deployed. The portfolio remains quarantined and recovery proceeds forward with conversion-aware code.

If the committed manifest is materially wrong but the remediated state has not left the maintenance window, restore the scoped pre-operation backup or point-in-time state. Do not manually edit or delete individual ledger rows. Once published or consumed, any correction requires separately governed compensating accounting and is outside this remediation.

Migration downgrade MUST abort while conversion rows exist.

## 16. Test strategy

### Unit tests

- Payload schema, version, required fields, exact decimal parsing, and canonical fingerprint.
- All accounting equations with and without cash-in-lieu.
- Fractional entitlement, rounding, fees, taxes, net cash, and realized P/L.
- Registry identity, identifier retirement, relationship, and provider binding.
- Same-asset, missing-asset, duplicate, ambiguity, and same-day conflict rejection.
- Quote metadata, timestamp, cache namespace, first-epoch previous-close, continuity, and quarantine behavior.

### Replay and validator tests

- BANPU arithmetic and basis preservation.
- Existing successor-position merge.
- Legacy and asset-native replay with the historical null `asset_id` predecessor transaction.
- Live/replay parity and independent validator parity.
- Duplicate and already-absent predecessor defense.
- Deterministic repeated replay.
- Refusal of full or pre-boundary snapshot rebuild.
- Byte-for-byte preservation of pre-boundary snapshot values.

### Migration tests

- Empty and production-shaped upgrades on PostgreSQL-compatible and SQLite paths.
- Repeated upgrade safety.
- Null payload on every existing row.
- Partial uniqueness only for `POSITION_CONVERSION`.
- Rejection of conversion inserts and updates with null predecessor `asset_id`, null `transaction_date`, intraday timestamps, or offset-bearing/noncanonical SQLite representations.
- Same-date different-time conversions cannot bypass the database constraint, normalized-midnight duplicates are rejected by the unchanged partial unique index, and non-conversion rows retain their existing null-asset and intraday behavior.
- Safe downgrade without conversions and refused downgrade with conversions.

### WP1 review deferrals and residuals

The renewed independent review disposition is `APPROVED WITH RECORDED RESIDUALS`.
None of the following is open WP1 implementation work:

| Finding | Disposition | Responsible future work package | Required future verification |
|---|---|---|---|
| `MINOR-1` — fingerprint serialization can lose distinctions beyond the default Decimal context precision | Deferred precision improvement; accepted as a WP1 residual because the fingerprint is not yet an active write-path idempotency key | WP4, before `execute_position_conversion()` uses the fingerprint for idempotency | Focused canonicalizer vectors with distinct values beyond 28 significant digits, followed by WP4 retry/conflict tests proving distinct payloads cannot collide |
| `MINOR-2` — boundary-evidence decimal sign/range validation is not yet consumer-specific | Deferred domain validation; accepted as a WP1 residual | WP3 owns provider/reference-price admissibility; WP5 owns mechanical continuity tolerance admissibility | Focused WP3 tests reject inadmissible reference prices; focused WP5 tests reject negative or otherwise inadmissible continuity tolerances before comparison |
| `MINOR-5` — PostgreSQL migration has not executed against a real PostgreSQL database in this environment | Accepted execution-verification residual | WP7 production-shaped migration rehearsal, with WP8 retaining the release evidence | Real PostgreSQL upgrade, repeated upgrade, constraint/index INSERT and UPDATE probes, guarded downgrade, and schema-introspection evidence |
| `NEW-MINOR-A` — PostgreSQL `timestamp without time zone` enforcement proves the canonical stored midnight value but cannot preserve or inspect the lexical presence of an offset after PostgreSQL input coercion | Accepted typed-storage residual; no schema redesign and no WP1 implementation reopening | WP4 must construct `transaction_date` only from the payload's timezone-free date as a naive-midnight typed value; WP7 must exercise the production dialect | WP4 service tests reject offset-bearing authoring inputs and prove payload/date equality; WP7 real-PostgreSQL probes document coercion behavior and prove persisted rows and service-authored rows satisfy the canonical stored-value invariant |

`NEW-MINOR-B` is resolved by placing the three BANPU canonical documents under
repository version control for the confirmation candidate. Renewed-review
Observation 1 is resolved by synchronizing the mandatory sequence with this
design and the roadmap. Neither resolution changes an implementation decision.

### Regression tests

- Golden behavior for all existing transaction types.
- Unconverted quote, cache, snapshot, return, optimizer, and evaluation behavior.
- No `LedgerRepair` conversion behavior.
- No public API requirement.
- No M46 file, status, or behavior change.

### Production verification

- One conversion row; transaction 83 unchanged.
- Correct predecessor/successor registry state and relationship.
- Broker-confirmed successor quantity, carried basis, average cost, cash, and realized P/L.
- Valid successor quote identity and epoch with no predecessor cache use.
- Unchanged pre-boundary portfolio and shadow values.
- Correct post-boundary successor identity and valuation.
- Clean validator results under both replay modes.
- Mechanical continuity verified and suspension return annotated.
- Immutable recommendation and optimizer evidence unchanged.
- Quarantine removed only after all checks pass.

## 17. Authority boundary

This specification is complete for implementation. Any proposal to add transaction families, generalized event dispatch, new corporate-action tables, editable conversion state, public authoring APIs, M46 changes, or broader accounting redesign is outside authority and requires separate approval.
