# BANPU-WP1 — Confirmation

**Artifact class:** WP1 confirmation record
**Confirmation date:** 2026-08-06
**Disposition:** `CONFIRMED WITH RECORDED RESIDUALS`
**Freeze performed:** `NO`
**WP2 authority:** `NONE`

## 1. Confirmation boundary

This record confirms the reviewed BANPU-WP1 implementation candidate only. It
does not freeze the candidate, authorize BANPU-WP2, change production data, or
grant replay, validator, live-materialization, market-data, snapshot, CLI, or
deployment authority.

## 2. Approved implementation

The confirmed WP1 candidate establishes the additive persistence and canonical
contract required by later packages:

- nullable `transactions.conversion_payload`, using PostgreSQL JSONB and the
  repository's SQLite-compatible JSON representation;
- immutable typed version-1 `POSITION_CONVERSION` parsing, exact Decimal
  payload values, structured deterministic errors, and canonical typed-value
  fingerprinting;
- mandatory top-level predecessor `asset_id` and a timezone-free transition
  date stored as naive midnight in `transaction_date`;
- named conversion-specific PostgreSQL/SQLite enforcement for non-null
  predecessor identity and canonical stored midnight;
- the retained conversion-only partial unique index over portfolio,
  predecessor asset, and canonical stored transition date;
- Alembic upgrade, repeated-upgrade, and guarded-downgrade behavior, plus
  legacy SQLite INSERT and UPDATE enforcement;
- authoritative transaction-vocabulary documentation and focused contract and
  migration tests.

No conversion write path, replay behavior, validator behavior, live portfolio
materialization, quote protection, snapshot behavior, CLI, frontend, M46, or
production-data change is part of this confirmation.

## 3. Independent review history

| Candidate | Review outcome | Resulting action |
|---|---|---|
| RC1 | Scope and additive contract were substantially sound; MAJOR-1 and focused contract/environment findings remained | Recovery and repair were required; WP1 was not frozen |
| RC2 | Canonical fingerprinting, SQLite compatibility, and focused edge coverage were repaired; MAJOR-1 remained a design-level database-invariant issue | Architecture Owner Design Decision Gate convened; no implementation proceeded until Alternative 3 was approved |
| RC3 | Implemented approved Alternative 3, completed vocabulary/tolerance corrections, and retained the approved partial unique index | Renewed Independent Review returned `APPROVED WITH RECORDED RESIDUALS` |

The Architecture Owner approved Alternative 3 before RC3 implementation:
`valuation_transition_date` is the timezone-free business date,
`transaction_date` stores that date as naive midnight, top-level `asset_id` is
the mandatory predecessor identity, and the named constraint plus retained
partial unique index jointly enforce the database key.

## 4. Governance findings

- `NEW-MINOR-B`: `RESOLVED` — all three BANPU canonical documents are included
  in the version-controlled confirmation candidate and are prepared for freeze.
- Observation 1: `RESOLVED` — the mandatory implementation sequence now states
  the approved RC3 constraint/index design, the renewed-review disposition,
  the pending freeze, and the WP2 entry block consistently with the design and
  roadmap.
- No open WP1 implementation finding remains.

## 5. Recorded residuals

The authoritative detailed register is in
[Canonical Implementation Design §16](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md#wp1-review-deferrals-and-residuals).

| Finding | Confirmation disposition | Future owner and verification gate |
|---|---|---|
| `MINOR-1` | Deferred precision improvement; not open WP1 work | WP4 before fingerprint idempotency use; high-precision distinctness plus retry/conflict tests |
| `MINOR-2` | Deferred consumer-domain validation; not open WP1 work | WP3 reference-price validation and WP5 tolerance validation, each with focused rejection tests |
| `MINOR-5` | Accepted PostgreSQL execution-verification residual | WP7 real-PostgreSQL rehearsal; WP8 retains release evidence |
| `NEW-MINOR-A` | Accepted PostgreSQL typed-storage/coercion residual; no schema redesign | WP4 naive-midnight authoring and payload/date tests; WP7 real-PostgreSQL coercion and stored-invariant probes |

These residuals are explicit future gates. They neither reopen WP1 nor waive
their assigned verification.

## 6. Confirmation decision

BANPU-WP1 is **`CONFIRMED WITH RECORDED RESIDUALS`**. The implementation is
complete, the renewed independent review is authoritative and approved, the
governance findings required before confirmation are resolved, and no open
implementation finding remains.

BANPU-WP1 is not frozen by this record. BANPU-WP2 remains blocked until a
separate constitutional freeze act completes.

## 7. Exact next constitutional act

The exact next authorized constitutional act is **BANPU-WP1 Constitutional
Freeze** over the confirmed candidate. That act must verify the candidate's
content identity and repository inclusion, record the frozen corpus, and grant
no implicit BANPU-WP2 implementation authority.
