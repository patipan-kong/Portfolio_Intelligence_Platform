# BANPU-WP5 — Fresh Implementation Freeze: Exact Ordinary Holding Basis Exposure

**Artifact class:** Additive Fresh Implementation Freeze record for a bounded amendment to a historically frozen/closed WP5 corpus
**Freeze date:** 2026-08-19
**Issuing role:** Independent BANPU-WP5 Fresh Implementation Freeze Authority
**Triggering determination:** [`BANPU_WP7_WP5_ORDINARY_HOLDING_BASIS_EVIDENCE_SOURCE_DETERMINATION.md`](BANPU_WP7_WP5_ORDINARY_HOLDING_BASIS_EVIDENCE_SOURCE_DETERMINATION.md), 12,658 bytes, SHA-256 `D32DEED16A0BB8C798A3A31C1705BCD64A61194A49E29B31C9E167228C5C0411`
**Amendment Authorization:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_ORDINARY_HOLDING_BASIS_EXPOSURE.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_ORDINARY_HOLDING_BASIS_EXPOSURE.md), 18,435 bytes, SHA-256 `9A8107A58AB6D4CFC6B360B1F216352F112356C89C293021EAA02D1E1942BED2`
**Fresh independent review:** [`BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_ORDINARY_HOLDING_BASIS_EXPOSURE.md`](BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_ORDINARY_HOLDING_BASIS_EXPOSURE.md), 17,893 bytes, SHA-256 `B3E1CB85734E3E8C59CD8B73A3D336190C5FD47F644614EA9FA9C52E0BFA3F82`
**Fresh Implementation Confirmation:** [`BANPU_WP5_FRESH_IMPLEMENTATION_CONFIRMATION_ORDINARY_HOLDING_BASIS_EXPOSURE.md`](BANPU_WP5_FRESH_IMPLEMENTATION_CONFIRMATION_ORDINARY_HOLDING_BASIS_EXPOSURE.md), 15,137 bytes, SHA-256 `C655877C8FA90891E6304D198A9C1081970B2D53349767896DFEE93458B1530D`
**Prior realized-P&L Fresh Freeze:** [`BANPU_WP5_FRESH_IMPLEMENTATION_FREEZE_REALIZED_PNL_EXPOSURE.md`](BANPU_WP5_FRESH_IMPLEMENTATION_FREEZE_REALIZED_PNL_EXPOSURE.md), 14,006 bytes, SHA-256 `D97571815CC841B9CE8EADE4DD385FD2C739C2029D999ADF85EF815838E70ED8`
**Disposition:** `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION FROZEN`
**WP7 correction resumed by this act:** `NO`
**Production/release/deployment authority created:** `NONE`

---

## 1. Freeze authority and boundary

This act performs only the Fresh Implementation Freeze required by the original [`BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md) §P for a material change to a historically frozen member. It binds the exact two-member result-surface corpus in §5 as frozen predecessor functionality under the continuous determination → Authorization → implementation → Fresh Review → Confirmation chain.

It does not modify implementation or tests, re-perform review or Confirmation, reopen the historical WP5 corpus, resume or implement WP7, modify LM13, synchronize the Decision Log or Implementation INDEX, execute production work, release, deploy, mutate cache/schema/database state, stage, commit, push, merge, or perform any WP8/M46 act.

## 2. Freeze entry-state verification

All mandatory fail-closed premises were independently rechecked from live bytes before this record was created:

| Premise | Result |
|---|---|
| HEAD baseline | `ae223a42df688563748c0e6e6cb898e66bcb3da0` — exact |
| Staging area | empty; cached names and cached diff were empty |
| Basis-source determination | exact at `D32DEED16A0BB8C798A3A31C1705BCD64A61194A49E29B31C9E167228C5C0411`; disposition remains `BANPU-WP7 BASIS EVIDENCE SOURCE RESOLVED — PREDECESSOR EXPOSURE AMENDMENT REQUIRED` |
| Amendment Authorization | exact at `9A8107A58AB6D4CFC6B360B1F216352F112356C89C293021EAA02D1E1942BED2`; disposition remains `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE AMENDMENT AUTHORIZED` |
| Production member | `backend/services/portfolio_rebuilder.py`, 129,960 bytes, SHA-256 `64026DDA722B949205F4FB3E875396BBBCC11C7EA6B4E10CC6AF87BB5AFF7947` — exact reviewed and confirmed identity |
| Test member | `backend/tests/test_portfolio_rebuilder.py`, 117,056 bytes, SHA-256 `ABC8C406AA91DE405E4C1B1A9253E3BB99134EB5B072DAC41ACD136927F1B5D0` — exact reviewed and confirmed identity |
| Fresh independent review | exact at `B3E1CB85734E3E8C59CD8B73A3D336190C5FD47F644614EA9FA9C52E0BFA3F82`; disposition re-read as `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION REVIEW PASSED` |
| Fresh Implementation Confirmation | exact at `C655877C8FA90891E6304D198A9C1081970B2D53349767896DFEE93458B1530D`; disposition re-read as `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION CONFIRMED` |
| Post-Confirmation member mutation | none; both live hashes equal the confirmed identities and both member write times precede the Confirmation record |
| Earlier basis Fresh Freeze | absent before this act |
| Historical WP5 Freeze / Closeout | unchanged at `8FE512A22BD0979B274C211BA48E4EB10B7CD5E82F42950C617DBE856A570E54` / `46AC7C4B5517F5DCE3978CE292ABDD4B8D6783D6C86A20DE8191291C55103E4A` |
| Prior realized-P&L Fresh Freeze | unchanged at `D97571815CC841B9CE8EADE4DD385FD2C739C2029D999ADF85EF815838E70ED8` |
| WP7 frozen planning | WPP `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897`, Planning Confirmation `7A44203B6E39BF5100B133DA39B96BD5A5B1059634B279B8C4706F1742A0E82D`, and Planning Freeze `E31AEC306C4CFDF0820A83BA1335DE22E0E9BE6A2ABC94AB153E85A6AB708B84` unchanged |
| WP7 consumption and correction state | zero `reconstructed_holding_basis` references in the WP7 CLI, focused test, and fixture; correction remains paused |
| LM13 | `backend/tests/test_position_conversion_live.py` unchanged at `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8` |
| Decision Log / Implementation INDEX | unchanged at `3BE8084DDE1813BF3B4ED7FF0C655C553EC3022B8554162E5585A44B8282EC50` / `5A1DB032AB4D35B0216A3346E7C07CE120E2067783461182872A75F1F1C466FC` |
| Production/release/deployment activity | no repository evidence found and none performed by this act |

No identity drift, missing prerequisite, post-Confirmation mutation, earlier basis Freeze, or contradictory lifecycle state was found. Freeze proceeds.

## 3. Freeze precedent and confirmation sufficiency

The original WP5 Freeze supplies the controlling Freeze and §P change-control model: independently verify the Confirmation, exact implementation identity continuity, bounded corpus, review evidence, residual carry-forward, exclusions, and successor. Its established raw-continuity and canonical-LF aggregate conventions are used without alteration. The D7 binding-freeze form establishes that a bounded amendment is additive and does not silently rebind unrelated historical members. The realized-P&L Fresh Freeze supplies the directly analogous two-member observation-surface form. No realized-P&L-specific numeric meaning is imported.

The ordinary-basis Fresh Implementation Confirmation was read in full, not accepted from its disposition alone. It sufficiently binds the exact determination, Authorization, reviewed members, passing review, canonical Stage-1 provenance, raw `Decimal` precision, stable `report_symbol` identity, duplicate-key failure, provider-free Stage-1 availability, compatibility, accounting/replay/provider non-interference, independently reproduced governing regression evidence, runtime classification, and WP7/LM13 boundaries. It is therefore a sufficient Freeze input.

## 4. Frozen corpus and overlay model

The historical WP5 nine-member corpus remains historically frozen and closed at its original identity; it is neither re-frozen nor substituted. The former realized-P&L result-surface amendment was an additive two-member overlay over that corpus.

This basis amendment is the next additive semantic overlay, but it changes the same two physical members. Consequently it **replaces the active two-member byte identity** rather than creating simultaneous active identities for either path. The previously frozen realized-P&L semantic delta is preserved as incorporated frozen history: the newly frozen bytes contain both trailing result-surface observations, `reconstructed_realized_pnl` and `reconstructed_holding_basis`. The prior realized-P&L Freeze record remains immutable evidence of its completed lifecycle; it is not overwritten, invalidated, or reopened.

The active freshly frozen WP5 result-surface corpus has cardinality **2**:

1. `backend/services/portfolio_rebuilder.py`
2. `backend/tests/test_portfolio_rebuilder.py`

These two current byte identities are the sole active result-surface overlay for those paths. Thus no ambiguous concurrent byte identities exist for the same file, while both additive semantic deltas remain frozen.

## 5. Cryptographic identity verification

| Member | Raw bytes | Raw SHA-256 | Canonical LF bytes | Canonical LF SHA-256 |
|---|---:|---|---:|---|
| `backend/services/portfolio_rebuilder.py` | 129,960 | `64026DDA722B949205F4FB3E875396BBBCC11C7EA6B4E10CC6AF87BB5AFF7947` | 127,289 | `2F035255181354E24CBA5FEF59BF23C85E2C9FE761E488778AFE2EBD81C936E1` |
| `backend/tests/test_portfolio_rebuilder.py` | 117,056 | `ABC8C406AA91DE405E4C1B1A9253E3BB99134EB5B072DAC41ACD136927F1B5D0` | 114,848 | `13D8AB7991D4C7DA2538D95B869C9B7E5F3DC5A7DC902EE1F1ACD39CDC292E23` |

The raw continuity aggregate follows original WP5 Freeze §E and realized-P&L Freeze §5: UTF-8 rows in the table order, `path<TAB>M<TAB>SHA256<TAB>bytes<LF>`. The canonical identity of record follows original WP5 Freeze §H: each raw file is normalized to LF by stripping only line-ending carriage returns, then UTF-8 rows in the same order, `path<TAB>SHA256<TAB>canonical-bytes<LF>`. Both files are CRLF in this checkout, so the raw and canonical values intentionally differ.

```text
Raw continuity aggregate              = E1F8B3E559AC9BD6683F9C1B69FD685C6B9A39934703B6E76AD3FE4720DEDC08
Canonical-LF aggregate (record value) = 89AA23712BE8177F8D363587343B520CB7DCC2C950BB6AE8B08E27A6D519C6F0
```

The canonical-LF aggregate is the active frozen overlay identity of record. The raw aggregate preserves byte continuity with the Review and Confirmation. All six required predecessor identities listed in this record's header were recomputed live and match exactly.

## 6. Exact frozen semantic, precision, and identity locks

This Freeze binds exactly the trailing/defaulted observation field:

```python
reconstructed_holding_basis: dict[str, Decimal] = field(default_factory=dict)
```

After successful Stage 1 it publishes, once per final holding:

```text
report_symbol -> exact h.shares * h.avg_cost
```

The values are exact predecessor `Decimal` products. They may not later be reinterpreted as cents-rounded, `_f()`-projected, six-decimal, float-derived, or presentation basis. A later WP7 consumer must consume this field directly and must not reconstruct ordinary basis from projected shares or average cost.

`report_symbol` is frozen as the only map key: it is stable across legacy and asset-native replay, does not expose an asset-ID key for ordinary holdings, and is not replaced with a provider symbol. A duplicate or conflicting `report_symbol` raises before assignment/publication; the standard failed `RebuildResult` therefore retains the default empty map and cannot silently overwrite a value.

## 7. Conversion and accounting non-interference

The ordinary map is final Stage-1 holding basis. It neither replaces nor derives conversion-specific evidence: conversion reconciliation continues to use explicit predecessor `B0`, successor `Bs`, and the existing conversion reconciliation fields, equations, and tolerances. No conversion allocation, formula, tolerance, or provenance changes.

The Freeze preserves all historical accounting and replay semantics unchanged: INITIAL_POSITION behavior, BUY fee-inclusive weighted average, SELL basis retention, quantity correction, conversion B0/Bs behavior, realized P&L, transaction order, validator equations, and reconciliation accounting. It binds an observation of their pre-existing final state only; it creates no equation or replay mechanism.

## 8. Provider, snapshot, replay, and compatibility preservation

The frozen map is available after Stage 1 and before conversion materialization, reconciliation, price-matrix work, provider fetching, and snapshot stages. It is available with `skip_snapshots=True`; no provider fetch, price matrix, or snapshot is required. There is no registry, cache, schema, persistence, database, API, frontend, serializer, golden-output, or replay-mode mechanic change.

The reviewed trailing/defaulted dataclass field preserves keyword construction compatibility. Consumer review found no positional `RebuildResult` construction, whole-result equality/field-set assumption, result `asdict`/`__dict__` serialization, public result serializer, persistence/schema path, or golden-output dependency. Existing callers can omit the defaulted field.

## 9. Regression evidence and runtime treatment

This Freeze does not re-run tests. It binds the Fresh Review's independently reproduced WP5 Freeze §O governing corpus exactly:

```text
213 passed, 247 warnings
```

The review also recorded eight focused tests as `8 passed, 10 warnings` and the rebuilder test file as `104 passed, 38 warnings`; neither result is substituted for the independently defined governing corpus.

The review and Confirmation establish that both environments use Python 3.13.3; `backend/.venv` lacks pytest, while `backend/venv-test` supplies pytest 9.1.1 and is the established WP5 review runtime. The pytest cache-permission warning is environmental only. Its carried classification is **`ENVIRONMENTAL / NON-BLOCKING`** and is not frozen implementation semantics.

## 10. Prior realized-P&L preservation and WP7 successor boundary

`reconstructed_realized_pnl` remains frozen, observation-only predecessor functionality. The active bytes in §5 preserve it alongside the new exact ordinary-basis map. This Freeze makes the complete two-member WP5 result surface competent predecessor functionality without reopening either amendment.

The frozen WP7 WPP requires both replay modes to compare holdings, basis, cash, and realized P/L, and the determination identifies its existing local `round(float(shares) * float(avg_cost), 2)` as `NON-CANONICAL IMPLEMENTATION DERIVATION — MUST REMOVE`. The completed WP5 freeze condition in that determination permits a later, separate resumption of WP7's already-authorized bounded correction. That correction may consume `RebuildResult.reconstructed_holding_basis` directly and compare exact predecessor basis across modes; it must remove the lossy local derivation. It does not need a WPP amendment or new WP7 Authorization solely for this predecessor consumption, and it may not modify either WP5 frozen member.

This act does not resume, implement, review, or confirm WP7.

## 11. LM13, residuals, and change control

LM13 remains separate stale predecessor-test debt and is neither modified nor synchronized. No residual is discharged or altered: `MINOR-5`, `NEW-MINOR-A`, `PD-3`, rehearsal-dependent WP7-A11/A12/A14/A15, WP8 release evidence, and M46 remain under their existing owners and states.

The active two-member identity in §5 is immutable under WP5 Freeze §P. Any material change to either member requires a new bounded lifecycle: Authorization → implementation → fresh independent review → Confirmation → Fresh Freeze. No silent edit can preserve this frozen identity.

## 12. Authority explicitly not granted

This Freeze grants no further WP5 change; no WP7 implementation within this act; no LM13 synchronization; no release, deployment, production execution, schema/database/cache mutation, WP8/M46 work, staging, commit, push, or merge. It only completes the WP5 ordinary-basis amendment lifecycle and establishes the successor boundary.

## 13. Artifact and repository verification

This file is the single additive artifact created by this act:

`docs/implementation/BANPU_WP5_FRESH_IMPLEMENTATION_FREEZE_ORDINARY_HOLDING_BASIS_EXPOSURE.md`

Immediately after writing, the two production/test members, determination, Authorization, Fresh Review, Fresh Confirmation, historical WP5 Freeze/Closeout, realized-P&L Fresh Freeze, WP7 planning artifacts, LM13, Decision Log, and Implementation INDEX are re-verified unchanged. Pre-existing unstaged WP7 candidate/governance files and prior WP5 amendment files remain separately attributable. This act adds only this record. Repository whitespace and cached-diff checks remain required and are reported after creation.

## 14. Resulting constitutional state and exact next act

- Historical WP5 remains complete, frozen, and closed at its original nine-member identity.
- The realized-P&L delta remains frozen as incorporated history.
- The active two-member WP5 result-surface overlay is now authorized, implemented, independently reviewed, confirmed, and freshly frozen at canonical-LF identity `89AA23712BE8177F8D363587343B520CB7DCC2C950BB6AE8B08E27A6D519C6F0`; it includes both realized-P&L exposure and exact ordinary holding-basis exposure.
- WP7 remains planning-confirmed/planning-frozen and paused; it has not yet consumed the new field.
- No residual, release, deployment, production, WP8, or M46 authority is created.

The exact next constitutional act is:

**Resume BANPU-WP7 Bounded Implementation Correction**, consuming the now-frozen exact `reconstructed_holding_basis` map and removing the prohibited local basis reconstruction.

This Freeze performs no part of that correction.

## 15. Fresh Implementation Freeze disposition

**`BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE IMPLEMENTATION FROZEN`**
