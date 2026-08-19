# BANPU-WP7 / BANPU-WP5 — Ordinary Holding Basis Evidence Surface Authority Determination

**Artifact class:** Bounded read-only authority and provenance determination record  
**Decision date:** 2026-08-19  
**Question resolved:** What canonical predecessor source supplies ordinary reconstructed holding basis for WP7's two-replay comparison, and what is the smallest lawful evidence surface required to expose it?  
**Implementation performed:** `NO`  
**Authority/amendment granted:** `NO`  
**Frozen planning artifact amended:** `NO`

---

## 1. Boundary and entry-state verification

This additive record performs only the requested read-only determination. It does not modify implementation, tests, WP5, WP7 planning, LM13, the Decision Log, or the Implementation INDEX; it does not authorize a later amendment; and it stages, commits, releases, deploys, or executes nothing.

The following entry identities were independently recomputed:

| Item | Result |
|---|---|
| HEAD | `ae223a42df688563748c0e6e6cb898e66bcb3da0` |
| Staging area | empty |
| WP7 WPP | `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897` (53,998 bytes) |
| WP7 Planning Confirmation | `7A44203B6E39BF5100B133DA39B96BD5A5B1059634B279B8C4706F1742A0E82D` (39,845 bytes) |
| WP7 Planning Freeze | `E31AEC306C4CFDF0820A83BA1335DE22E0E9BE6A2ABC94AB153E85A6AB708B84` (31,901 bytes) |
| WP7 first failed review | `59D39B92DDDB8BFAACE785C49D4453EC3F423C85C2D8FC15B8E025DF601DDF74` (10,558 bytes) |
| WP7 fresh failed review | `C79564232FE269488AB3D9EDB4AE38B3B265238F2447AB6C038BEDF28D2BA6BD` (18,810 bytes) |
| current WP7 candidate `backend/manage.py` | `8329CF676B2A05283D15000BD130C8CC3185B1F77215C97072D16E76E5655802` (259,543 bytes) |
| current focused WP7 test | `DBD4BDDC601D2BED072522931793E60F17170E93D11EAC55C6C0F3B5E3139779` (47,257 bytes) |
| WP5 freshly frozen production overlay | `backend/services/portfolio_rebuilder.py` = `409FBC22313A98B24D9A23FFE3754CBA2584A702473C36CB2D51A36EDC19F429` (129,464 bytes) |
| WP5 freshly frozen test overlay | `backend/tests/test_portfolio_rebuilder.py` = `F42FFF2084A568CE165D0F58B0C3EA0109881E38736BB9CE299E330F49808B25` (108,142 bytes) |
| LM13 | `backend/tests/test_position_conversion_live.py` = `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8` |
| Decision Log / Implementation INDEX | unchanged at `3BE8084DDE1813BF3B4ED7FF0C655C553EC3022B8554162E5585A44B8282EC50` / `5A1DB032AB4D35B0216A3346E7C07CE120E2067783461182872A75F1F1C466FC` |

The WP5 realized-P&L amendment lineage remains freshly frozen: Authorization `DFFFF800…8336`, Review `3B3E8363…5925`, Confirmation `92CB87DD…E7E4`, and Freeze `D9757181…0ED8`. Repository search found no prior ordinary-basis amendment, authorization, or exposure artifact. The current WP7 candidate still contains its local `round(float(shares) * float(avg_cost), 2)` fallback. No repository evidence of a production/release/deployment act was found, and none occurred in this determination.

## 2. Frozen requirement and canonical meaning

WP7 WPP §7.2 requires legacy and asset-native dry-run replays to compare **holdings, basis, cash, and realized P/L**. The canonical Design §8.3 makes the same requirement substantive: the conversion must produce identical shares, basis, cash, and realized P/L in both modes. Its accounting model defines `B0` as predecessor basis before conversion, `Bs` as basis carried to the successor, and `As = Bs / Qr` as successor average cost.

For this determination, ordinary reconstructed holding basis means the per-final-holding cost basis produced by the authoritative `rebuild_portfolio` Stage-1 replay, keyed by the stable reconstructed holding identity used for materialization/reporting (`report_symbol`). It is neither aggregate portfolio basis nor a frontend presentation value. Conversion-successor `B0`/`Bs` remains payload-defined accounting evidence, not a substitute for the basis of every ordinary final holding.

## 3. Provenance and accounting findings

`portfolio_rebuilder.py` keeps each Stage-1 holding in private `_HoldingState` as exact `Decimal` `shares` and fee-inclusive `avg_cost`; no rounding occurs while those values are updated. `_d()` receives values through `Decimal(str(value))`, and `_f()` is a later projection that quantizes to `0.000001` with `ROUND_HALF_UP`.

The ordinary replay rules establish the cost-basis invariant mechanically:

- `INITIAL_POSITION` creates or weighted-merges share count and average cost.
- `BUY` adds the net, fee-inclusive buy amount into the weighted average.
- `SELL` retains average cost and reduces the remaining share count.
- Quantity corrections update the same state.
- A position conversion verifies the predecessor's `shares * avg_cost` against payload `B0`, then carries the payload's exact `Bs` into the successor or a successor merge.

The independently implemented ledger validator corroborates this meaning. Its private `_ReplayState.basis` is an exact-Decimal per-holding cost-basis map for all holdings; it records BUY net amount, proportional remaining basis after a SELL, exact initial-position basis, correction effects, and exact conversion `Bs`. It expressly documents the `shares × avg_cost` cost-basis relation. That validator state is not, however, an appropriate WP7 result surface: it is private, raw-symbol keyed, and its public `LedgerValidationReport` exposes only findings rather than the successful final state.

Thus the internal relationship is a real predecessor accounting invariant, but WP7 has no public, precision-preserving predecessor result carrying the ordinary per-holding value from the actual Stage-1 rebuild it runs.

## 4. Conversion-successor distinction

Conversion-successor basis already reaches the reconciliation report only in the conversion-specific five-field comparison (`asset_id`, `symbol`, `shares`, `avg_cost`, `basis`). It is sourced from the conversion's explicit canonical payload (`B0`/`Bs`) and is compared with the established `0.01` reconciliation tolerance. Ordinary holdings take the separate two-field reconciliation path (`shares`, `avg_cost`) and emit no basis row. The two mechanisms are therefore not interchangeable.

## 5. Existing result-surface classification

| Candidate | Classification | Reason |
|---|---|---|
| `RebuildResult.reconstructed_cash` / `reconstructed_realized_pnl` | NOT APPLICABLE | canonical scalar observations, but not ordinary holding basis |
| `RebuildResult.reconciliation_report`, ordinary rows | DERIVED / PRESENTATIONAL | exposes only values projected through `_f()`/rounding; ordinary rows omit basis |
| reconciliation report, conversion-successor basis row | CANONICAL AND DIRECTLY CONSUMABLE for conversion successor only | explicit payload-derived conversion evidence; not an ordinary-holding surface |
| `_PortfolioState.holdings` / `_HoldingState` | CANONICAL BUT NOT EXPOSED | actual Stage-1 exact-Decimal holding state, private to WP5's rebuilder |
| ledger validator `_ReplayState.basis` | CANONICAL BUT NOT EXPOSED | exact independent accounting state, private and not mode/result compatible |
| `LedgerValidationReport` / findings | INSUFFICIENT | contains anomalies, not a successful ordinary-basis map |
| `PortfolioItem`, snapshots, execution plan, golden parity output | DERIVED / PRESENTATIONAL or INSUFFICIENT | float/rounded or reconciliation-derived projection; no exact ordinary basis result |

`skip_snapshots=True` still constructs the Stage-1 final state, then its reconciliation report and validator report, before returning. No provider fetch is required for that path. A suitable result field populated directly at the Stage-1 boundary would therefore be available to WP7's existing fetch-free dry-run call.

## 6. Precision, identity, and current WP7 classification

The current WP7 fallback reads reconciliation values, converts them to float, multiplies, and rounds to two decimals. That cannot recover the exact Decimal state: `_f()` has already quantized values to six decimals, snapshot values have different presentation rounding, and division during weighted-average or conversion successor allocation can retain precision beyond a projected average-cost value. Equal two-decimal products can consequently conceal distinct canonical results. The frozen requirement cannot be weakened to make that derivation acceptable.

`report_symbol` is the correct deterministic evidence key for this narrow surface because it is the rebuilder's stable output/materialization identity in both modes; the native internal map key may be an asset ID while legacy mode uses a symbol. Asset ID must not be invented for ordinary positions merely to form this evidence surface. The existing conversion-specific asset-ID evidence remains distinct and unchanged.

The WP7-local expression is therefore classified:

**`NON-CANONICAL IMPLEMENTATION DERIVATION — MUST REMOVE`**

It reproduces an internal invariant only after lossy projection, rather than consuming a canonical predecessor observation.

## 7. Resolution analysis and ownership

- **Resolution A — existing public surface:** rejected. No public result supplies exact ordinary reconstructed basis.
- **Resolution B — canonical internal value not exposed:** selected. The rebuilder's final holding state is the appropriate predecessor source and is not exposed through `RebuildResult`.
- **Resolution C — WP7 derivation permitted:** rejected. The internal relation is mechanically established, but the fields presently available to WP7 are rounded projections; a WP7-local calculation is not precision-safe or a direct predecessor result.
- **Resolution D — accounting clarification:** rejected. Frozen Design conversion semantics, the fee-inclusive average-cost decision, both replay implementations, and predecessor tests resolve the accounting meaning; the gap is observation, not undefined accounting semantics.

The owning frozen implementation surface is WP5's `backend/services/portfolio_rebuilder.py`, with the matching focused test surface `backend/tests/test_portfolio_rebuilder.py`. WP7 owns neither file. The recently completed realized-P&L amendment is structurally applicable as precedent: it used a trailing/defaulted `RebuildResult` observation, populated from Stage-1 state without changing replay, accounting, provider, snapshot, or persistence semantics, and then required a fresh WP5 amendment lifecycle.

## 8. Smallest later surface and change control

If a competent later WP5 authorization is issued, the smallest additive candidate is one trailing/defaulted `RebuildResult` field:

```python
reconstructed_holding_basis: dict[str, Decimal] = field(default_factory=dict)
```

It would be populated once, after successful Stage-1 replay, from each final holding's stable `report_symbol` and the rebuilder's exact-Decimal basis invariant (`h.shares * h.avg_cost`), before any snapshot/provider stage. This is an exposure of existing Stage-1 accounting state, not a new equation, tolerance, provider fetch, replay pass, persistence field, API surface, or WP7 calculation. A future WP7 correction would consume the map directly and compare Decimal values fail-closed; it would retain the existing separate conversion-successor evidence path.

The later authorization must also restrict focused proof to `backend/tests/test_portfolio_rebuilder.py`: default compatibility; ordinary initial/BUY/partial-SELL exact basis; conversion carried/merged basis; `skip_snapshots=True`; no provider fetch; deterministic `report_symbol` keys; and no accounting/replay/persistence change.

Because `portfolio_rebuilder.py` is part of the freshly frozen WP5 overlay, WP5 Freeze §P requires the complete new additive chain: narrowly scoped **Implementation Authorization Amendment** → bounded WP5 implementation amendment → fresh independent WP5 implementation review → fresh WP5 Implementation Confirmation → fresh WP5 Implementation Freeze. Only after that freeze may WP7 resume its separately bounded correction.

## 9. Artifact and final disposition

The closest read-only competent-authority determination precedent creates one additive record and modifies no frozen artifact. This record is that sole artifact. It grants no amendment or implementation authority.

**`BANPU-WP7 BASIS EVIDENCE SOURCE RESOLVED — PREDECESSOR EXPOSURE AMENDMENT REQUIRED`**

The exact next constitutional act is:

**BANPU-WP5 Implementation Authorization Amendment — expose exact ordinary reconstructed holding basis through `RebuildResult`.**

That later act must be limited to the surface identified in §8. It is not performed by this determination.

