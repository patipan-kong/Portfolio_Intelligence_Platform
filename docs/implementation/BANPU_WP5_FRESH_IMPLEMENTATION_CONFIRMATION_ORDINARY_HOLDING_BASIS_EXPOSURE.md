# BANPU-WP5 — Fresh Implementation Confirmation: Exact Ordinary Holding Basis Exposure

**Artifact class:** Additive fresh Implementation Confirmation record for a bounded amendment
**Confirmation date:** 2026-08-19
**Issuing role:** Independent BANPU-WP5 Implementation Confirmation Authority
**Triggering determination:** [`BANPU_WP7_WP5_ORDINARY_HOLDING_BASIS_EVIDENCE_SOURCE_DETERMINATION.md`](BANPU_WP7_WP5_ORDINARY_HOLDING_BASIS_EVIDENCE_SOURCE_DETERMINATION.md), 12,658 bytes, SHA-256 `D32DEED16A0BB8C798A3A31C1705BCD64A61194A49E29B31C9E167228C5C0411`
**Amendment Authorization:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_ORDINARY_HOLDING_BASIS_EXPOSURE.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_ORDINARY_HOLDING_BASIS_EXPOSURE.md), 18,435 bytes, SHA-256 `9A8107A58AB6D4CFC6B360B1F216352F112356C89C293021EAA02D1E1942BED2`
**Fresh independent review:** [`BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_ORDINARY_HOLDING_BASIS_EXPOSURE.md`](BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_ORDINARY_HOLDING_BASIS_EXPOSURE.md), 17,893 bytes, SHA-256 `B3E1CB85734E3E8C59CD8B73A3D336190C5FD47F644614EA9FA9C52E0BFA3F82`
**Independent-review disposition:** `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION REVIEW PASSED`
**Disposition:** `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION CONFIRMED`
**Fresh Implementation Freeze performed by this act:** `NO`
**WP7 correction resumed by this act:** `NO`
**Production/release/deployment authority created:** `NONE`

---

## 1. Purpose and confirmation boundary

This record performs only the fresh Implementation Confirmation required by WP5 Implementation Freeze §P for the separately authorized ordinary-holding-basis observation. It confirms the exact two-file amendment identities in §6 under the exact determination, Authorization, and passing independent-review identities named above.

It does not modify or re-review implementation or tests, perform the Fresh Implementation Freeze, reopen unrelated historical WP5 work, resume WP7, modify LM13, synchronize the Decision Log or Implementation INDEX, or authorize production execution, release, deployment, schema/database/cache mutation, staging, commit, push, or merge. Confirmation applies only to the exact bytes bound here.

## 2. Confirmation entry-state verification

The following fail-closed premises were independently re-established from live repository bytes before this record was created:

| Premise | Live result |
|---|---|
| HEAD baseline | `ae223a42df688563748c0e6e6cb898e66bcb3da0` — exact |
| Staging area | empty; cached names/status and cached diff were empty |
| Amendment Authorization | byte-identical at `9A8107A58AB6D4CFC6B360B1F216352F112356C89C293021EAA02D1E1942BED2`; disposition re-read as `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE AMENDMENT AUTHORIZED` |
| Triggering determination | byte-identical at `D32DEED16A0BB8C798A3A31C1705BCD64A61194A49E29B31C9E167228C5C0411`; disposition remains `BANPU-WP7 BASIS EVIDENCE SOURCE RESOLVED — PREDECESSOR EXPOSURE AMENDMENT REQUIRED` |
| Reviewed production member | `backend/services/portfolio_rebuilder.py`: 129,960 bytes, SHA-256 `64026DDA722B949205F4FB3E875396BBBCC11C7EA6B4E10CC6AF87BB5AFF7947` — exact review match |
| Reviewed test member | `backend/tests/test_portfolio_rebuilder.py`: 117,056 bytes, SHA-256 `ABC8C406AA91DE405E4C1B1A9253E3BB99134EB5B072DAC41ACD136927F1B5D0` — exact review match |
| Fresh independent review | byte-identical at `B3E1CB85734E3E8C59CD8B73A3D336190C5FD47F644614EA9FA9C52E0BFA3F82`; disposition re-read as `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION REVIEW PASSED` |
| Post-review implementation/test mutation | none; both current hashes equal the review's captured identities and their write times predate the review record |
| Prior realized-P&L overlay | frozen record unchanged at `D97571815CC841B9CE8EADE4DD385FD2C739C2029D999ADF85EF815838E70ED8` |
| Prior basis Confirmation or Freeze | absent before this act |
| WP7 frozen planning | WPP `9A5F4F79…2897`, Planning Confirmation `7A44203B…E82D`, and Planning Freeze `E31AEC30…8B84` unchanged |
| WP7 consumption | `backend/manage.py` has no `reconstructed_holding_basis` reference; correction remains paused |
| LM13 | `backend/tests/test_position_conversion_live.py` unchanged at `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8` |
| Decision Log / Implementation INDEX | unchanged at `3BE8084D…EC50` / `5A1DB032…6FC` |
| Production/release/deployment activity | no repository evidence found and none performed by this act |

No identity drift, missing prerequisite, post-review mutation, pre-existing basis Confirmation/Freeze, or contradictory lifecycle state was found. The entry gate passes.

## 3. Confirmation precedent and authority chain

The immediately preceding realized-P&L Fresh Implementation Confirmation supplies the structural form: an additive standalone record independently re-hashes the authorization, reviewed implementation members, and passing review; verifies review sufficiency and compatibility; preserves earlier frozen/closed records; denies Freeze and operational effects; and names the exact next constitutional act. Its realized-P&L numeric substance is not imported.

WP5 Freeze §P supplies the controlling lifecycle rule for a material change to a frozen member: scoped authorization, bounded implementation, fresh independent review, fresh Implementation Confirmation, then fresh Implementation Freeze. The complete unbroken chain is:

```text
historical frozen/closed WP5
  → realized-P&L fresh frozen overlay
  → WP7 basis-evidence blocker
  → basis-source determination
  → ordinary-basis Amendment Authorization
  → bounded implementation amendment
  → Fresh Independent Implementation Review PASS
  → this Confirmation
```

No lifecycle act is missing before Confirmation. The only remaining lifecycle act is the Fresh Implementation Freeze; it is not performed here.

## 4. Exact confirmed amendment scope

The sole confirmed production semantics are the trailing/defaulted result field:

```python
reconstructed_holding_basis: dict[str, Decimal] = field(default_factory=dict)
```

and, after successful Stage 1, exactly one observation of every final holding:

```text
report_symbol -> h.shares * h.avg_cost
```

The values are the exact internal `Decimal` products. A duplicate/conflicting `report_symbol` raises before the local map is published, so the standard failure result retains the default empty map and no silent overwrite is possible. No other production behavior is confirmed.

## 5. Canonical provenance and precision confirmation

Live source and the full independent review confirm that `_HoldingState.shares` and `_HoldingState.avg_cost` are pre-existing `Decimal` state. The amendment does not alter pre-existing INITIAL_POSITION construction/merge, BUY fee-inclusive weighted average, partial-SELL average-cost retention, quantity correction, conversion predecessor `B0` validation, successor `Bs` carrying/merge, replay order, or any accounting equation. It observes only fully replayed Stage-1 state.

The published values use no `_f()`, float conversion, quantization, local rounding, or serialization conversion. The precision counterexample is decisive: actual INITIAL_POSITION replay of `1.0000004` shares at `100.0000004` cost yields `Decimal("100.00004040000016")`; the WP7 projected, six-decimal float route produces `100.0`, losing `0.00004040000016`. Exact predecessor exposure is therefore intentional and required; a WP7 projected reconstruction is not an acceptable substitute.

## 6. Cryptographic identities bound

| Bound artifact | Bytes | SHA-256 |
|---|---:|---|
| Basis-source determination | 12,658 | `D32DEED16A0BB8C798A3A31C1705BCD64A61194A49E29B31C9E167228C5C0411` |
| Amendment Authorization | 18,435 | `9A8107A58AB6D4CFC6B360B1F216352F112356C89C293021EAA02D1E1942BED2` |
| `backend/services/portfolio_rebuilder.py` | 129,960 | `64026DDA722B949205F4FB3E875396BBBCC11C7EA6B4E10CC6AF87BB5AFF7947` |
| `backend/tests/test_portfolio_rebuilder.py` | 117,056 | `ABC8C406AA91DE405E4C1B1A9253E3BB99134EB5B072DAC41ACD136927F1B5D0` |
| Fresh independent implementation review | 17,893 | `B3E1CB85734E3E8C59CD8B73A3D336190C5FD47F644614EA9FA9C52E0BFA3F82` |
| Prior realized-P&L Fresh Freeze | 14,006 | `D97571815CC841B9CE8EADE4DD385FD2C739C2029D999ADF85EF815838E70ED8` |

The production and test identities are exactly the bytes reviewed as PASS. No code or test byte changed between that review and this Confirmation.

## 7. Identity, conversion, and stage/provider boundaries

`report_symbol` is the established cross-mode result/materialization identity: legacy replay uses a string identity, while native replay can use an internal asset-ID key but retains the same `report_symbol`. The focused evidence independently exercises both forms; no asset-ID key leaks into the map. The deterministic duplicate guard fails closed before assignment and forbids a silent overwrite.

The ordinary map complements rather than replaces conversion-specific evidence. Conversion reconciliation continues to expose the existing `B0`/`Bs` provenance and `asset_id`, `symbol`, `shares`, `avg_cost`, and `basis` fields; no conversion formula, tolerance, allocation, or provenance is reopened.

Population occurs after successful Stage 1 and before conversion materialization, reconciliation, provider/snapshot stages, and `_build_price_matrix`. It remains available with `skip_snapshots=True`, requires no provider fetch, and failures before successful Stage-1 publication retain the default empty map as applicable.

## 8. Compatibility confirmation

All current `RebuildResult` construction and consumer sites were independently re-enumerated. No positional construction was found; existing production, parity, WP7, and rebuilder construction is keyword-based and may omit the trailing default. There is no whole-result equality, exact field-set, `asdict(RebuildResult)`, or `__dict__` consumer; the repository's generic `asdict` use applies to other dataclasses.

No API/frontend serializer, persistence/schema/database path, golden output, or CLI serializes the whole `RebuildResult`; named consumers select existing fields. The raw Decimal map therefore creates no current public serialization contract or compatibility break.

## 9. Independent-review sufficiency and regression evidence

The Fresh Independent Review was read in full and independently checked against live identities, source/diff scope, consumers, and the authority chain. It sufficiently establishes the authorized diff, canonical provenance, exact map semantics, Decimal precision, `report_symbol` identity, duplicate-key failure, default map, INITIAL_POSITION, BUY, partial SELL, conversion, the precision counterexample, provider-free `skip_snapshots=True`, compatibility, accounting/provider/replay non-interference, counterexample search, WP7/LM13 non-interference, focused tests, and governing regressions.

This Confirmation does not re-run tests. It binds only the fresh review's independently reproduced evidence: eight focused tests passed (`8 passed, 10 warnings`); the WP5 Freeze §O governing corpus of `test_portfolio_rebuilder.py`, `test_portfolio_metrics.py`, `test_snapshot_return_recovery.py`, and `test_verify_snapshots.py` passed exactly as `213 passed, 247 warnings`; the rebuilder test file alone passed as `104 passed, 38 warnings`. There is no count discrepancy for the defined governing invocation.

## 10. Test-runtime treatment

The review established that both relevant environments use Python 3.13.3, `backend/.venv` lacks pytest, and `backend/venv-test` provides pytest 9.1.1 and is the established runtime used in earlier independent WP5 reviews. The governing file set and semantics are unchanged. The pytest-cache permission warning affects cache writing only.

**Classification: `ENVIRONMENTAL / NON-BLOCKING`.**

## 11. WP7, residual, and LM13 boundaries

WP7 triggered the missing predecessor observation but owns neither confirmed WP5 member. Its WPP, Planning Confirmation, Planning Freeze, candidate, focused test, and fixture remain unchanged; it still does not consume the basis map, and its correction remains paused. This Confirmation does not authorize its resumption. WP7 may resume only after the Fresh WP5 Implementation Freeze.

No residual is discharged or affected: `MINOR-5`, `NEW-MINOR-A`, `PD-3`, rehearsal-dependent WP7 acceptance, WP8 authority, and LM13 remain unchanged. No conversion, replay, provider, persistence, registry, cache, schema, or accounting scope is widened.

## 12. Confirmation determination

The Authorization, determination, reviewed two-file corpus, and review record are exact and continuous; scope, precision, identity, compatibility, provider boundary, and non-interference are satisfied; and the independently reproduced governing corpus is green.

**`BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION CONFIRMED`**

This confirms only the exact bounded amendment bytes in §6. It does not replace historical WP5 records, re-freeze the realized-P&L overlay, or freshly freeze this second observation.

## 13. Authority explicitly not granted

This Confirmation grants no authority for additional WP5 implementation, WP7 correction or resumption, LM13 synchronization, production execution, release, deployment, schema/database/cache mutation, API/frontend/serialization work, WP8/M46 work, staging, commit, push, merge, Decision Log synchronization, or Implementation INDEX synchronization.

## 14. Artifact created and repository boundary

This single additive record is the only artifact created by this Confirmation act:

`docs/implementation/BANPU_WP5_FRESH_IMPLEMENTATION_CONFIRMATION_ORDINARY_HOLDING_BASIS_EXPOSURE.md`

The production/test members, determination, Authorization, independent review, realized-P&L overlay, historical WP5 records, WP7 state, LM13, Decision Log, and Implementation INDEX are not modified by this act. Pre-existing unstaged WP7 candidate/governance files and the already reviewed WP5 implementation amendment remain separately attributable.

## 15. Resulting constitutional state and exact next act

- Historical WP5 remains complete, implementation-frozen, and closed at its historical corpus identity.
- The realized-P&L result-surface overlay remains freshly frozen and unchanged.
- The ordinary-holding-basis result-surface amendment is authorized, boundedly implemented, freshly independently reviewed as PASS, and now confirmed, but is not freshly frozen.
- WP7 remains planning-confirmed/planning-frozen, does not consume this field, and its correction remains paused.
- No production/release/deployment authority, residual discharge, or WP8/M46 authority exists.

The exact next constitutional act is:

**BANPU-WP5 Fresh Implementation Freeze — Exact Ordinary Holding Basis Exposure**

over the exact confirmed amended implementation identities in §6 and this Confirmation record. This act performs no part of that Freeze.
