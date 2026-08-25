# BANPU-WP5 — Fresh Independent Implementation Review: Exact Ordinary Holding Basis Exposure

**Artifact class:** Additive fresh independent implementation-review record for a bounded amendment to the freshly frozen WP5 result surface  
**Review date:** 2026-08-19  
**Review boundary:** Independent review only; no implementation/test correction, Confirmation, Freeze, WP7 resumption, LM13 synchronization, staging, commit, release, deployment, or production act  
**Authorization:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_ORDINARY_HOLDING_BASIS_EXPOSURE.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_ORDINARY_HOLDING_BASIS_EXPOSURE.md), 18,435 bytes, SHA-256 `9A8107A58AB6D4CFC6B360B1F216352F112356C89C293021EAA02D1E1942BED2`  
**Triggering determination:** [`BANPU_WP7_WP5_ORDINARY_HOLDING_BASIS_EVIDENCE_SOURCE_DETERMINATION.md`](BANPU_WP7_WP5_ORDINARY_HOLDING_BASIS_EVIDENCE_SOURCE_DETERMINATION.md), 12,658 bytes, SHA-256 `D32DEED16A0BB8C798A3A31C1705BCD64A61194A49E29B31C9E167228C5C0411`  
**Disposition:** `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION REVIEW PASSED`

---

## 1. Review entry-state verification

The live entry state was independently established before review work:

| Item | Independently established result |
|---|---|
| HEAD | `ae223a42df688563748c0e6e6cb898e66bcb3da0` |
| Staging area | empty; cached name/status and cached diff were empty |
| Amendment Authorization | identity/disposition exactly as stated above; `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE AMENDMENT AUTHORIZED` |
| Basis-source determination | identity exactly as stated above; `BANPU-WP7 BASIS EVIDENCE SOURCE RESOLVED — PREDECESSOR EXPOSURE AMENDMENT REQUIRED` |
| Active realized-P&L overlay | frozen record unchanged at `D97571815CC841B9CE8EADE4DD385FD2C739C2029D999ADF85EF815838E70ED8`; it continues to bind Authorization `DFFFF800…D8336`, Review `3B3E8363…5925`, Confirmation `92CB87DD…E7E4`, and disposition `BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION FROZEN` |
| Amended production member | `backend/services/portfolio_rebuilder.py`: 129,960 raw bytes, SHA-256 `64026DDA722B949205F4FB3E875396BBBCC11C7EA6B4E10CC6AF87BB5AFF7947`; canonical-LF 127,289 bytes, SHA-256 `2F035255181354E24CBA5FEF59BF23C85E2C9FE761E488778AFE2EBD81C936E1` |
| Amended test member | `backend/tests/test_portfolio_rebuilder.py`: 117,056 raw bytes, SHA-256 `ABC8C406AA91DE405E4C1B1A9253E3BB99134EB5B072DAC41ACD136927F1B5D0`; canonical-LF 114,848 bytes, SHA-256 `13D8AB7991D4C7DA2538D95B869C9B7E5F3DC5A7DC902EE1F1ACD39CDC292E23` |
| WP7 frozen planning | WPP `9A5F4F79…2897`, Planning Confirmation `7A44203B…E82D`, Planning Freeze `E31AEC30…8B84`, and historical failed review `59D39B92…DF74` remain exact |
| WP7 implementation surface | `backend/manage.py` and its focused test/fixture all pre-date the basis Authorization and the two basis implementation mtimes; none contains `reconstructed_holding_basis` |
| LM13 | `backend/tests/test_position_conversion_live.py` unchanged at `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8` |
| Decision Log / INDEX | unchanged at `3BE8084D…EC50` / `5A1DB032…6FC` |
| Prior basis Confirmation/Freeze | absent; repository filename/content search found only the determination and Authorization for this basis lifecycle before this record |
| Production/release/deployment | no repository evidence found; none performed by this review |

The WP7 candidate files were last written before the determination and Authorization; the basis Authorization was then written before both amended WP5 members. The complete two-file diff and this chronology separate the basis amendment cleanly from pre-existing WP7 work. Entry hashes were retained for post-review continuity verification; no post-entry implementation/test mutation occurred.

## 2. Authorization-scope verification

The complete Authorization was read. It authorizes only one trailing/defaulted `RebuildResult` field, exact Stage-1 population from every final holding's `h.shares * h.avg_cost`, `report_symbol` keys, raw `Decimal` values, a deterministic duplicate-key failure guard, and focused evidence in `test_portfolio_rebuilder.py`.

It expressly excludes accounting equations, BUY/SELL/conversion behavior, allocation or replay ordering, provider/snapshot work, Registry/cache changes, persistence/schema, API/frontend/serialization, realized-P&L changes, WP7 work, LM13, Decision Log/INDEX edits, debug-print cleanup, and unrelated refactoring. The submitted amendment stays within that boundary.

## 3. Actual diff review

The complete attributable delta was reviewed against the freshly frozen realized-P&L overlay and against HEAD for surrounding context.

Production adds only:

```python
reconstructed_holding_basis: dict[str, Decimal] = field(default_factory=dict)
```

and, immediately after successful Stage 1, a local `dict[str, Decimal]` populated by `h.report_symbol` and `h.shares * h.avg_cost`, with a duplicate-key `ValueError` before publication. No accounting transition, transaction flow, provider/snapshot, reconciliation, conversion, formatting/refactor, or debug-print line is attributable to this basis amendment.

Test changes attributable to the basis amendment are the `asset_id` option in the existing canonical-transaction helper, two compatibility/empty-map assertions, and six focused basis tests. They are all necessary evidence for the authorized surface. The realized-P&L field/assignment/tests visible in the HEAD diff belong to the already frozen predecessor overlay and were not re-attributed to this amendment.

## 4. Canonical basis provenance

`_HoldingState.shares` and `_HoldingState.avg_cost` are `Decimal`. Their invariant predates this amendment:

- `INITIAL_POSITION` creates or weighted-merges exact shares and average cost;
- `BUY` uses exact fee-inclusive `total_amount` and weighted average;
- partial `SELL` reduces shares without changing average cost;
- conversion validates predecessor `shares * avg_cost` against `B0`, then creates/merges the successor from carried `Bs`;
- quantity correction and all replay ordering remain unchanged.

None of those formulas appears in the attributable diff. The new field observes only the final state after `_apply_transaction` has completed for every effective transaction.

## 5. Exact basis-map semantics

The map is exactly:

```text
report_symbol -> exact final Stage-1 holding basis
```

for every remaining final holding. It is not aggregate portfolio basis, a reconciliation projection, a snapshot/display value, conversion-only evidence, or an asset-ID keyed map. Conversion-specific `B0`/`Bs` evidence remains separately present in reconciliation.

## 6. Decimal precision finding

The value expression contains no `_f()`, float conversion, quantization, two-decimal rounding, or serialization. The result type and runtime values remain `Decimal` through publication.

**Finding: exact Decimal preservation is satisfied.**

## 7. `report_symbol` identity finding

`report_symbol` is the pre-existing reconstructed output identity used by reconciliation, execution-plan generation, and commit materialization. Legacy replay's internal key is the same string identity. Native replay's internal key can be integer `asset_id`, but holding creation still binds `report_symbol` to the canonical/raw string and all `PortfolioItem.symbol` consumers re-key by it. Conversion merge/create also explicitly binds the successor `report_symbol` from the payload.

The public map never exposes an asset-ID key. The focused native/legacy test exercises both internal-key forms, and source inspection—not merely the passing assertion—confirms the semantic identity is stable across modes.

## 8. Duplicate-key handling

Two distinct native internal holdings can theoretically carry one `report_symbol`, even though normal materialization expects uniqueness. The guard iterates deterministically, raises before assigning the local map to the result, and is caught by `rebuild_portfolio`'s repository-standard exception path. The returned form is `RebuildResult(success=False, error=...)`; the published basis map remains its empty default; no provider work occurs; no database/accounting mutation is introduced; and no key silently overwrites another.

The guard is harmless in invariant-conforming runs and expressly within Authorization.

## 9. Default/empty-map evidence

- Direct `RebuildResult(...)` construction omitting the new field returns a fresh `{}`.
- A successful DEPOSIT-only Stage-1 replay has no final holdings and returns `{}`.
- Not-found, no-transaction, preflight, and other pre-publication failures use the defaulted result and therefore remain compatible.
- Duplicate failure publishes no partial map.

## 10. Initial-position evidence

The focused test passes a real `CanonicalTransaction` through `rebuild_portfolio` and `_apply_transaction`; it does not mock the basis map. It produces the final holding and exact `Decimal("100.00004040000016")`, uses `skip_snapshots=True`, and independently verifies `_build_price_matrix` was not called.

## 11. BUY evidence

The BUY test uses fixture facts: three initial shares at `10.1234567` plus a two-share BUY whose exact admitted amount is `40.2469134`. The expected final basis `70.6172835` is the sum of those fixture costs, not a copy of the production weighted-average implementation. The observed product therefore arises through the predecessor replay semantics and distinguishes it from projected float reconstruction.

## 12. Partial-SELL evidence

The partial-SELL test begins with 7.25 shares at `12.3456789`, sells 2.25, and observes the exact remaining five-share basis `61.7283945`. Source diff review confirms the SELL branch was not changed; shares decrease and predecessor average cost is retained.

## 13. Conversion evidence

The conversion test exercises the existing conversion replay with predecessor `B0=240`, allocated basis `12`, carried successor basis `Bs=228`, and 9.5 received shares. It observes ordinary final basis `{successor: Decimal("228")}` and separately asserts that the existing conversion reconciliation still contains `asset_id`, `symbol`, `shares`, `avg_cost`, and `basis`. No B0/Bs evidence was replaced or weakened.

## 14. Precision-counterexample evidence

The replayed INITIAL_POSITION values `1.0000004` shares and `100.0000004` average cost produce exact internal basis:

```text
Decimal("1.0000004") * Decimal("100.0000004")
= Decimal("100.00004040000016")
```

The predecessor WP7 projection path rounds both ordinary reconciliation components to six decimals, producing `1.0` and `100.0`, then reconstructs/rounds basis to `100.0`. It loses `0.00004040000016`. This is not an unreachable synthetic arithmetic-only case: the focused test drives those values through actual Stage-1 INITIAL_POSITION replay and the same Decimal conversion convention used by canonical transactions.

**Finding: direct predecessor exposure is materially necessary and the counterexample is valid.**

## 15. `skip_snapshots` / provider-free evidence

Population occurs directly after the Stage-1 replay loop and before conversion-successor materialization, reconciliation, Stages 2–3, and `_build_price_matrix`. With `skip_snapshots=True`, the provider branch is not entered. Independent provider-spy execution passed for initial-position, empty-holding, and duplicate cases; each asserted `_build_price_matrix` was never called.

## 16. Compatibility finding

All repository `RebuildResult(` constructors and consumers were searched. Constructors in production, WP7 tests, registry replay parity, and rebuilder tests use keywords and may omit the new trailing default. No positional construction was found. No whole-result equality, `fields(RebuildResult)`, exact `__dict__`, or `asdict(RebuildResult)` consumer exists. The generic `asdict` use in registry replay parity applies to its separate `GoldenBaseline`, not `RebuildResult`.

No JSON/API/frontend serializer, persistence/schema path, golden snapshot, or CLI currently serializes the entire object. Existing CLI consumers select named fields. A Decimal map therefore creates no current serialization or equality break. WP7 still has zero references to `reconstructed_holding_basis`.

**Finding: backward-compatible.**

## 17. Accounting non-interference

The attributable diff contains no change to INITIAL_POSITION, BUY weighted average, SELL semantics, corrections, conversion B0/Bs handling, cash-in-lieu, realized P&L, basis allocation, replay ordering, validator logic, or reconciliation equations. Exact predecessor formulas and bytes remain outside the amendment.

## 18. Provider/snapshot/replay non-interference

No change was found in provider fetch, historical pricing, snapshots, replay-mode mechanics, Registry, cache, persistence, schema, or database paths. The new observation reads already-complete Stage-1 state only.

## 19. Focused test result

The exact eight focused nodes were independently executed under `backend/venv-test`:

```text
8 passed, 10 warnings in 2.15s
```

The selection covered constructor default, zero holdings/provider-free replay, initial position/precision, BUY, partial SELL, native/legacy identity, duplicate symbol, and conversion.

## 20. Governing WP5 regression result

WP5 Freeze §O defines the governing test membership as:

- `tests/test_portfolio_rebuilder.py`
- `tests/test_portfolio_metrics.py`
- `tests/test_snapshot_return_recovery.py`
- `tests/test_verify_snapshots.py`

Independent execution returned:

```text
213 passed, 247 warnings in 3.02s
```

The rebuilder file was also independently run alone:

```text
104 passed, 38 warnings in 1.91s
```

These counts exactly reproduce the reported current results. The six new basis tests explain the predecessor corpus's increase from 207 to 213.

## 21. Test-runtime classification

Both environments use Python 3.13.3. `backend/.venv` reports `No module named pytest`; `backend/venv-test` provides pytest 9.1.1 and is the established runtime named and used in earlier independent WP5 reviews. Test semantics and the governing file set are unchanged. A pytest-cache permission warning affected cache writing only and no test execution.

**Classification: `ENVIRONMENTAL / NON-BLOCKING`.**

## 22. WP7 non-interference

The basis amendment did not modify `backend/manage.py`, WP7 CLI tests, the WP7 fixture, WPP, Planning Confirmation, Planning Freeze, or failed reviews. Their mtimes/hashes establish that the WP7 candidate work preceded the determination/Authorization and the amended WP5 files. `backend/manage.py` still contains its non-canonical rounded ordinary-basis derivation and has no `reconstructed_holding_basis` reference; WP7 correction therefore remains paused and has not consumed the new surface.

## 23. LM13 non-interference

LM13 remains byte-identical at `FF7CE1F4…918D8`, is absent from the attributable two-file diff, and remains outside this WP5 act.

## 24. Counterexample-search result

Attempts covered zero holdings, initial position, multiple-lot BUY/weighted average, partial SELL, conversion, native/legacy identity, high precision, duplicate symbol, `skip_snapshots=True`, provider spy, and an existing constructor omitting the field. Source inspection also covered failed/pre-Stage-1 paths and all consumers.

**No counterexample falsifying the amendment was found.**

## 25. Additional defects/observations

- The current Authorization and implementation have no separate bounded-implementation report artifact carrying post-write hashes. This does not block review: current identities were captured at entry, the complete attributable diff is narrow, mtime chronology separates it from WP7, and the identities remained stable throughout review. The review/Confirmation/Freeze lifecycle records—not an implementation report—are the constitutional identity gates.
- Existing debug `print()` statements remain present and unchanged, consistent with the Authorization's explicit exclusion of cleanup.
- The pytest cache warning is environmental and did not alter the green result.
- No blocking or non-blocking implementation defect was found.

## 26. Review artifact created

The realized-P&L fresh independent review establishes that a successful fresh review is recorded as one standalone additive artifact, separate from later Confirmation and Freeze. This file is therefore the sole artifact created by this act:

`docs/implementation/BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_ORDINARY_HOLDING_BASIS_EXPOSURE.md`

No Confirmation or Freeze record was created.

## 27. Repository/diff verification

At review completion:

- production/test bytes remained at the entry identities in §1;
- the Authorization, determination, active realized-P&L overlay, WP7 planning/candidate surfaces, LM13, Decision Log, and INDEX remained unchanged;
- only this standalone review record is attributable to the review;
- `git diff --check` and `git diff --cached --check` pass;
- the cached diff and cached name/status remain empty;
- nothing is staged;
- no implementation/test correction, commit, release, deployment, or production act occurred.

## 28. Fresh independent-review disposition

**`BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION REVIEW PASSED`**

The implementation complies exactly with authority, preserves raw Decimal basis, uses deterministic cross-mode `report_symbol` identity, changes no accounting/replay/provider behavior, remains compatible with existing consumers, has sufficient focused evidence, passes the governing regression corpus, and does not interfere with WP7 or LM13.

## 29. Exact next constitutional act

**BANPU-WP5 Fresh Implementation Confirmation — Exact Ordinary Holding Basis Exposure**

That Confirmation is not performed in this session.
