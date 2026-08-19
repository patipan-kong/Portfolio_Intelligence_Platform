# BANPU-WP5 — Implementation Authorization Amendment: Exact Ordinary Holding Basis Exposure

**Artifact class:** Additive constitutional Implementation Authorization amendment for a second bounded observation-only change to the freshly frozen WP5 result surface  
**Amendment date:** 2026-08-19  
**Issuing authority:** BANPU-WP5 Implementation Authorization Amendment Authority, acting only for the narrow result-surface exposure specified below  
**Historical WP5 Freeze / Closeout:** [`BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md), SHA-256 `8FE512A22BD0979B274C211BA48E4EB10B7CD5E82F42950C617DBE856A570E54`, disposition `BANPU-WP5 IMPLEMENTATION FROZEN`; [`BANPU_WP5_EPIC_CLOSEOUT.md`](BANPU_WP5_EPIC_CLOSEOUT.md), SHA-256 `46AC7C4B5517F5DCE3978CE292ABDD4B8D6783D6C86A20DE8191291C55103E4A`, disposition `BANPU-WP5 EPIC CLOSEOUT COMPLETE`  
**Prior freshly frozen overlay:** [`BANPU_WP5_FRESH_IMPLEMENTATION_FREEZE_REALIZED_PNL_EXPOSURE.md`](BANPU_WP5_FRESH_IMPLEMENTATION_FREEZE_REALIZED_PNL_EXPOSURE.md), SHA-256 `D97571815CC841B9CE8EADE4DD385FD2C739C2029D999ADF85EF815838E70ED8`, disposition `BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION FROZEN`  
**Triggering determination:** [`BANPU_WP7_WP5_ORDINARY_HOLDING_BASIS_EVIDENCE_SOURCE_DETERMINATION.md`](BANPU_WP7_WP5_ORDINARY_HOLDING_BASIS_EVIDENCE_SOURCE_DETERMINATION.md), SHA-256 `D32DEED16A0BB8C798A3A31C1705BCD64A61194A49E29B31C9E167228C5C0411`, disposition `BANPU-WP7 BASIS EVIDENCE SOURCE RESOLVED — PREDECESSOR EXPOSURE AMENDMENT REQUIRED`  
**Disposition:** `BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE AMENDMENT AUTHORIZED`  
**Implementation performed by this act:** `NO`  
**Release/deployment/production-mutation authority created:** `NONE`

---

## 1. Nature and boundary of this act

This is an authorization amendment only. It creates one fresh, bounded correction path for a second, exact observation on the two-member result-surface overlay already freshly frozen for realized P&L. It does not implement a field, amend the historical or fresh WP5 freeze, amend the WP7 WPP, resume the WP7 correction, perform review, Confirmation, or Freeze, change accounting, or authorize staging, commit, release, deployment, reconstruction, or production mutation.

The historical nine-member WP5 corpus remains historically frozen and closed. The realized-P&L two-member overlay remains the active freshly frozen implementation identity until the future lifecycle in §16 is completed for this distinct material change. This record does not assert that the ordinary-basis field exists.

## 2. Amendment entry-state verification

Each premise was independently checked from live repository bytes immediately before this record was written.

| Premise | Live evidence | Result |
|---|---|---|
| HEAD and staging state | HEAD `ae223a42df688563748c0e6e6cb898e66bcb3da0`; `git diff --cached --name-only` empty | `SATISFIED` |
| Historical WP5 status | Historical Freeze/Closeout retain the identities and dispositions named above | `SATISFIED` |
| Prior overlay remains freshly frozen | Its Freeze retains SHA-256 `D97571815CC841B9CE8EADE4DD385FD2C739C2029D999ADF85EF815838E70ED8`; it binds the realized-P&L Authorization `DFFFF800…D8336`, Review `3B3E8363…5925`, and Confirmation `92CB87DD…E7E4` | `SATISFIED` |
| Frozen production overlay identity | `backend/services/portfolio_rebuilder.py`: 129,464 bytes, SHA-256 `409FBC22313A98B24D9A23FFE3754CBA2584A702473C36CB2D51A36EDC19F429`, exact match to the prior overlay Freeze §6 | `SATISFIED` |
| Ordinary-basis result field absent | Repository search finds `reconstructed_holding_basis` only as the proposed candidate in the triggering determination; no production field or population exists | `SATISFIED` |
| Determination is unchanged and dispositive | 12,658 bytes, SHA-256 `D32DEED16A0BB8C798A3A31C1705BCD64A61194A49E29B31C9E167228C5C0411`; disposition exactly as named above | `SATISFIED` |
| WP7 frozen planning unchanged | WPP `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897`; Confirmation `7A44203B6E39BF5100B133DA39B96BD5A5B1059634B279B8C4706F1742A0E82D`; Planning Freeze `E31AEC306C4CFDF0820A83BA1335DE22E0E9BE6A2ABC94AB153E85A6AB708B84` | `SATISFIED` |
| WP7 correction remains blocked on this predecessor surface | `backend/manage.py` still fills ordinary basis by `round(float(shares) * float(avg_cost), 2)` from reconciliation values; the determination classifies it `NON-CANONICAL IMPLEMENTATION DERIVATION — MUST REMOVE` | `SATISFIED` |
| LM13, Decision Log, and INDEX | Respectively unchanged at `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8`, `3BE8084DDE1813BF3B4ED7FF0C655C553EC3022B8554162E5585A44B8282EC50`, and `5A1DB032AB4D35B0216A3346E7C07CE120E2067783461182872A75F1F1C466FC` | `SATISFIED` |
| Production/release/deployment act | No repository evidence found; none performed by this act | `SATISFIED` |

The pre-existing unstaged WP7 candidate and its focused test/fixture, plus prior BANPU governance records, are outside this authorization. They do not alter the freshly frozen WP5 production overlay. No baseline drift requiring failure-closed treatment was found.

## 3. Governing amendment precedent

The completed realized-P&L result-surface amendment is the closest structural precedent: it added one trailing/defaulted observation to `RebuildResult`, populated it immediately after successful Stage 1, changed neither replay nor provider behavior, and passed the fresh Authorization → independent review → Confirmation → Freeze chain. Its Freeze defines the presently active two-member overlay as `backend/services/portfolio_rebuilder.py` and `backend/tests/test_portfolio_rebuilder.py`, preserving the historical nine-member freeze intact.

WP5 Freeze §P independently requires the same sequence for every future material change to a frozen member: scoped fresh implementation authorization, fresh independent implementation review, fresh Implementation Confirmation, and fresh Implementation Freeze. Accordingly, this record is a second additive authorization amendment; it neither replaces nor folds the realized-P&L overlay into a new historical corpus.

## 4. Canonical ordinary-basis semantics

The frozen WP7 WPP §7.2 and §7.3 require both replay modes to compare holdings, basis, cash, and realized P&L. The frozen conversion Design distinguishes predecessor `B0`, carried successor `Bs`, and successor average cost `As = Bs / Qr`. Those conversion payload values are explicit conversion evidence; they are not the ordinary final-holding basis surface.

The canonical ordinary value is therefore the exact per-final-holding Stage-1 cost basis in the authoritative `rebuild_portfolio` replay state. It is neither aggregate portfolio basis nor a frontend/display value. `_HoldingState` stores `shares` and fee-inclusive `avg_cost` as `Decimal`; `_d()` uses `Decimal(str(value))`; `_f()` is a later `Decimal`-to-float projection that quantizes to six decimals with `ROUND_HALF_UP`.

## 5. Canonical source determination

The canonical predecessor invariant for every final holding is the internal Decimal relationship:

```python
h.shares * h.avg_cost
```

Primary Stage-1 code establishes it mechanically. `INITIAL_POSITION` sets or weighted-merges exact shares and average cost; `BUY` uses the exact fee-inclusive amount in its weighted average; `SELL` reduces shares while retaining average cost; and quantity correction updates the same state. For a conversion, the replay validates predecessor `shares * avg_cost` against payload `B0`, then creates or merges the successor using payload `Bs`. The final state is complete before result population, reconciliation, snapshots, provider work, or persistence.

This authorization permits exposure of that existing invariant only. It does **not** permit the prohibited WP7 reconstruction from reconciliation-report floats. Ordinary reconciliation emits projected shares and average cost only; conversion reconciliation separately emits its explicit five-field `B0`/`Bs` evidence. Multiplying the projected ordinary values after `_f()` and rounding to two decimals is lossy and remains non-canonical.

## 6. Precision determination

`Decimal` is the repository-native exact representation: it is the type of `_HoldingState.shares`, `_HoldingState.avg_cost`, transaction monetary values, and conversion-basis values. The lawful future result representation is therefore a raw `Decimal` map; no normalization, float conversion, quantization, two-decimal rounding, or new rounding rule is authorized.

The future field must carry the exact Stage-1 product as calculated. It must not be serialized to float merely to make a later WP7 consumer convenient. This differs deliberately from the pre-existing `reconstructed_cash` and realized-P&L float result surfaces, which use their own established `_f()` convention.

## 7. Identity and key determination

`report_symbol` is the established stable string identity used for reconstructed holding materialization and reconciliation. Under legacy replay, it is the same canonical-symbol/raw-symbol replay identity. Under native replay, the internal map key may be an integer asset ID, while `report_symbol` remains the only valid string identity for `PortfolioItem.symbol`; the reconciler, execution-plan builder, commit path, and holdings materialization all re-key final holdings by it. `PortfolioItem` further has the per-portfolio uniqueness constraint `uq_portfolio_symbol`.

The exact future map key is consequently `report_symbol`, not an invented asset-ID key. Existing final-state materialization already relies on one final holding per `report_symbol`; no conflicting final `report_symbol` was evidenced, and the ordinary result map must preserve that same established one-to-one output identity in both replay modes. A future implementer must fail closed rather than silently overwrite if that prerequisite is contradicted by a live final state; inventing or mixing asset-ID/provider-symbol keys is not authorized.

## 8. Exact authorized result surface and population boundary

If and only if the future bounded implementation amendment proceeds, it may append exactly one trailing/defaulted `RebuildResult` field, using the module's existing dataclass and typing conventions:

```python
reconstructed_holding_basis: dict[str, Decimal] = field(default_factory=dict)
```

The sole authorized population is immediately after successful Stage-1 replay, at the existing result-population boundary that currently sets holding count, reconstructed cash, and reconstructed realized P&L, and before conversion materialization, reconciliation, snapshot/provider stages, or persistence. It must map every final holding's `report_symbol` to the exact `h.shares * h.avg_cost` Decimal product. It must not use `_f()`, floats, snapshot values, reconciliation rows, or provider-derived values.

## 9. Conversion-specific basis preservation

The new ordinary map is complementary to, and does not replace, the conversion-successor evidence path. The latter remains the conversion-specific explicit payload evidence (`B0`/`Bs`), including the existing reconciliation fields `asset_id`, `symbol`, `shares`, `avg_cost`, and `basis`. No conversion formula, `B0` validation, `Bs` carrying/merge behavior, allocation rule, tolerance, or provenance is authorized to change.

Later WP7 work may consume both sources where its frozen semantics require: the exact ordinary map for every final holding and the separate explicit conversion evidence for a conversion successor. This authorization performs neither consumption nor comparison.

## 10. Compatibility determination

The trailing/defaulted field is backward-compatible with all inspected in-repository `RebuildResult` construction and consumption.

| Question | Finding | Result |
|---|---|---|
| Positional and keyword construction | The three non-default fields are first; all inspected constructors use keywords and omit the proposed field | `BACKWARD-COMPATIBLE` |
| Existing constructors | Failure, normal-rebuild, tests, and parity helpers receive the empty default without caller change | `BACKWARD-COMPATIBLE` |
| Equality / exact field set | No whole-`RebuildResult` equality, `fields(RebuildResult)`, `asdict(result)`, or `result.__dict__` exact-field assertion was found | `NO CURRENT CONSUMER IMPACT` |
| Serialization, API, persistence | No router, endpoint, serializer, database model, or API response serializes `RebuildResult` | `NO PUBLIC OR PERSISTED CONTRACT EXPANSION` |
| Golden/parity output | Golden-baseline extraction selects reconciliation truth and reconstructed cash explicitly; it does not serialize the result object or require this field | `NO COLLATERAL CHANGE REQUIRED` |
| Downstream consumers | `manage.py`, registry parity, replay cutover, and tests consume named fields/reconciliation data; none requires change merely to tolerate a trailing field | `BACKWARD-COMPATIBLE` |

The compatibility conclusion authorizes no caller, serializer, persistence, API, or golden-output edit.

## 11. Exact authorized production and future test surfaces

The sole authorized future production file is:

`backend/services/portfolio_rebuilder.py`

Within it, future work may make only the field addition and the minimal Stage-1 population defined in §8. It may not refactor, format, reorganize, or otherwise alter that file.

The sole authorized future test file is:

`backend/tests/test_portfolio_rebuilder.py`

Future focused proof must cover default empty-map compatibility; initial-position basis; BUY weighted-average basis; partial-SELL remaining basis; ordinary zero/empty holdings; conversion carried/merged basis where applicable; deterministic `report_symbol` keys; exact Decimal precision; `skip_snapshots=True`; no provider fetch; and compatibility with existing constructors/consumers. No test is implemented by this authorization.

## 12. Accounting, provider, and persistence non-interference

The future implementation will expose an existing Stage-1 predecessor invariant; it will not define a basis equation. Weighted-average cost, fee treatment, SELL basis retention, quantity correction, conversion `B0`/`Bs`, replay ordering, canonicalization, and all other predecessor accounting semantics remain unchanged.

The final state exists before Stages 2–3. Thus `skip_snapshots=True` remains sufficient and no provider fetch is required. The field is in-memory replay output only: no schema, persistence, cache, registry, snapshot, API, frontend, or serialization work is authorized.

## 13. Explicit exclusions

This authorization does not authorize:

- accounting, BUY/SELL, conversion, allocation, or replay-order changes;
- provider fetches, snapshots, registry/cache changes, persistence/schema changes, API/frontend serialization, or debug-print cleanup;
- result refactoring, unrelated WP5 maintenance, realized-P&L changes, or a generic result framework;
- WP7 implementation, WPP modification, planning change, or correction resumption;
- LM13 synchronization or modification; Decision Log or INDEX modification; or
- review, Confirmation, Freeze, closeout, production execution, release, deployment, staging, commit, push, merge, or any file beyond §11 in the future bounded amendment.

## 14. WP7 relationship

WP7 triggered the need but does not own `backend/services/portfolio_rebuilder.py` or its focused WP5 test. Its WPP, Planning Confirmation, and Planning Freeze remain unchanged. Its current correction remains paused: it must not treat its local rounded basis product as compliant predecessor evidence.

After the complete fresh WP5 amendment lifecycle, WP7 may resume its already bounded correction, consume the exact map, and remove the local ordinary-basis derivation while retaining conversion-specific evidence. No new WP7 planning or authorization is required solely because this predecessor observation becomes available; no WP7 work is authorized or performed here.

## 15. Authority granted and resulting state

This record grants only a future **BANPU-WP5 Bounded Implementation Amendment** within §§8 and 11. The field is `NOT IMPLEMENTED`. The realized-P&L overlay remains historically intact and presently frozen; this authorization does not re-freeze, supersede, or silently modify it.

WP5 therefore remains historically `COMPLETE / IMPLEMENTATION FROZEN / EPIC CLOSED`, with a newly authorized but unimplemented, separately bounded ordinary-basis observation path. WP7 remains `PLANNING CONFIRMED / PLANNING FROZEN`, and its basis-correction dependency remains open. No production, release, deployment, residual discharge, or WP8/M46 authority exists.

## 16. Required downstream lifecycle

WP5 Freeze §P and the realized-P&L overlay precedent require this exact sequence:

1. this Implementation Authorization Amendment;
2. **BANPU-WP5 Bounded Implementation Amendment** within §§8 and 11 only;
3. fresh independent WP5 implementation review of the amended overlay;
4. fresh WP5 Implementation Confirmation; and
5. fresh WP5 Implementation Freeze binding the new overlay identity.

Only after that Freeze may WP7 resume its separately bounded correction. It may then consume the exact map and remove its non-canonical local basis derivation; it may not jump directly from this authorization to implementation.

## 17. Artifact created and repository verification

This additive authorization record is the only file created by this act:

`docs/implementation/BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_ORDINARY_HOLDING_BASIS_EXPOSURE.md`

The post-write verification required by this act must confirm no code/test file changed; the current WP5 overlay, WP7 candidate, triggering determination, LM13, Decision Log, and INDEX are unchanged; `git diff --check` and cached diff check pass; and the index remains empty. No commit is permitted.

## 18. Authorization disposition

**`BANPU-WP5 ORDINARY-HOLDING-BASIS RESULT-SURFACE AMENDMENT AUTHORIZED`**

The authorization is narrow and observation-only. It does not implement, review, confirm, freeze, close, deploy, or release the amendment.

## 19. Exact next constitutional act

**BANPU-WP5 Bounded Implementation Amendment — expose exact ordinary reconstructed holding basis through `RebuildResult`.**

That act must stay strictly within §§8 and 11 and is not performed in this session.
