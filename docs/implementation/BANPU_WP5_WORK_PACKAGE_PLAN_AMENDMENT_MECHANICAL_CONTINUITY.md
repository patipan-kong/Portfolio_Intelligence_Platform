# BANPU-WP5 — Work Package Plan Amendment: Mechanical Continuity (§10.4)

**Artifact class:** Additive constitutional Work Package Plan amendment supplement
**Amendment date:** 2026-08-14
**Issuing authority:** BANPU-WP5 Work Package Plan Amendment Authority (distinct from the design-clarification, reconciliation, D7 amendment, both D7 reapprovals, and the D7 Binding Freeze authorities; performs no independent reapproval, no implementation, no Planning Confirmation, no Planning Freeze)
**Original Work Package Plan:** [`BANPU_WP5_WORK_PACKAGE_PLAN.md`](BANPU_WP5_WORK_PACKAGE_PLAN.md)
**Original Plan identity:** raw SHA-256 `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523`; 42,903 bytes; 604 physical lines
**Authoritative D2–D6 source:** [`BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md`](BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md), 16,491 bytes, 158 lines, SHA-256 `8DD43B1202714213E9EF88A65582E59A492680B747412BDAC9F176D3C43A2223`
**Authority-provenance reconciliation:** [`BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md`](BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md), 18,755 bytes, 145 lines, SHA-256 `BBE93F45237D6517E047A1E4FC8FC7A7665615975789F9E0AE9E6B846273EAE8`
**Authoritative D7 amendment:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md), 32,307 bytes, 237 lines, SHA-256 `DC8C272CD35854A156C9AD51494FE232C5408373A947AEC1B314D9657159E75B`
**Fresh Independent Reapproval:** [`BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_FRESH_INDEPENDENT_REAPPROVAL.md`](BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_FRESH_INDEPENDENT_REAPPROVAL.md), 23,848 bytes, 165 lines, SHA-256 `421FF4C0C6936B25EF3168A52B90550556791A150CA68A1912AD9BCE7BC566BA`
**Binding/freeze artifact:** [`BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_BINDING_FREEZE_RECORD.md`](BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_BINDING_FREEZE_RECORD.md), 22,742 bytes, 170 lines, SHA-256 `6EC85ED13623B9817964F6BC5372D578DBF90AA9BCC2B1465CE086E361A2E6E4`
**Sections amended:** Work Package Plan §10.4, §15 (acceptance matrix), §17 (residual handling), §19 (completion evidence), §22 (next act) only
**Disposition:** `PLAN AMENDMENT PREPARED — NOT YET INDEPENDENTLY REAPPROVED`
**Implementation reliance:** `PROHIBITED — IMPLEMENTATION MUST NOT YET RELY ON THE §10.4 PLANNING IN THIS AMENDMENT`
**Implementation or test change performed:** `NO`
**Independent reapproval performed by this act:** `NO`
**`MINOR-2` (WP5 half) closed by this act:** `NO`

---

## 1. Purpose

This record amends the BANPU-WP5 Work Package Plan to turn the previously blocked §10.4 mechanical-continuity reconciliation obligation into deterministic, fully specified planning, using the D2–D7 authority now bound and frozen by the artifacts cited above. It performs no implementation, no independent reapproval of itself, no Planning Confirmation, no Planning Freeze, and no `MINOR-2` closure. It follows the additive-amendment shape established by the BANPU-WP4 Retry-Order Work Package Plan Amendment, independently re-read this act (§4).

## 2. Entry planning state (independently re-verified)

| Item | Verification | Result |
|---|---|---|
| `BANPU_WP5_ALLOCATION_RECORD.md` | present, `BANPU-WP5 ALLOCATED` | `CONFIRMED` |
| `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | present, `BANPU-WP5 IMPLEMENTATION AUTHORIZED`, `AUTHORIZED — BOUNDED`, implementation `NOT STARTED` (§13) | `CONFIRMED` |
| `BANPU_WP5_WORK_PACKAGE_PLAN.md` | present, header status `WORK PACKAGE PLAN MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN`, re-read in full live this act | `CONFIRMED` |
| WPP §10.4 | live-grepped: line 290 `### 10.4 Part (b) — the reconciliation/comparison itself — \`PLANNING BLOCKER\``; line 9 header restates the same; §15 row `WP5-BLOCKED`; §17 residual row `BLOCKED` — all four occurrences trace to the identical §10.4 obligation, no other WPP blocker found (§15 below) | `CONFIRMED — SOLE PLANNING BLOCKER` |
| Design §5, §10, §16 | re-read live from `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`; §10's sentence is the exact provision the design clarification (§6 below) interprets; unchanged | `CONFIRMED` |
| Roadmap §7, Sequence Step 5 | matched exactly by the WPP's own §2 entry-verification table, itself re-read live this act; no independent divergence found on re-inspection | `CONFIRMED` |
| Human-authorized design clarification | present, unchanged, D2/D4/D5/D6 bound (§6 below) | `CONFIRMED` |
| Authority-provenance reconciliation | present, unchanged, `RECONCILED` | `CONFIRMED` |
| D7 Implementation Authorization Amendment | present, unchanged, `PREPARED` at its own time, now `BOUND AND FROZEN` per the Binding Freeze Record | `CONFIRMED` |
| Fresh D7 Independent Reapproval | present, unchanged, `FRESH INDEPENDENT REAPPROVAL PASSED` | `CONFIRMED` |
| D7 Binding Freeze Record | present, unchanged, `BOUND AND FROZEN`, WPP state recorded there as `NOT YET AMENDED OR REAPPROVED` (accurate as of its own writing; this act is that amendment) | `CONFIRMED` |
| WP3 Reference-Price Admissibility (`position_conversion_quote_contract.py`) | live-grepped; module/`QuarantineReason` docstrings still name "WP5's mechanical NAV continuity tolerance" and "mechanical continuity failure" / "unannotated boundary discontinuity" as WP5-owned and deliberately absent from WP3's enumeration | `CONFIRMED — WP3 SURFACE UNTOUCHED, OWNERSHIP BOUNDARY UNCHANGED` |
| WP1 `MINOR-2` row | live-grepped from `BANPU_WP1_FREEZE_RECORD.md` line 127: `WP3 for reference prices; WP5 for mechanical tolerance` | `CONFIRMED` |
| No prior WP5 WPP amendment | `ls docs/implementation/ \| grep -i "WP5.*WORK_PACKAGE_PLAN_AMENDMENT\|WP5.*AMENDMENT.*MECHANICAL"` returns only the D7 Implementation Authorization Amendment (a different, already-bound artifact) — no WPP-amendment file exists | `CONFIRMED ABSENT` |
| No Planning Confirmation / Planning Freeze consuming the old blocker | `ls docs/implementation/BANPU_WP5*.md` (re-run this act) lists exactly: Allocation, Authorization, WPP, two competent-authority determinations, reconciliation governance decision, D7 amendment, both D7 reapprovals, D7 Binding Freeze Record — no `PLANNING_CONFIRMATION` or `PLANNING_FREEZE` file exists | `CONFIRMED ABSENT` |
| `MINOR-2` WP5-implementation-obligation state | design clarification §13/§16: `DESIGN SEMANTICS RESOLVED — IMPLEMENTATION OBLIGATION OPEN`; Binding Freeze §17: `DESIGN SEMANTICS RESOLVED — D7 IMPLEMENTATION AUTHORITY BOUND — IMPLEMENTATION OBLIGATION OPEN` | `CONFIRMED OPEN` |
| `manage.py` live grep for `MECHANICAL_CONTINUITY` | absent | `CONFIRMED — NO D7 IMPLEMENTATION HAS OCCURRED` |
| WP4 Retry-Order WPP-amendment precedent chain (four files) | present, unchanged, re-read in full this act (§4) | `CONFIRMED` |

All ten numbered premises this invocation lists are true. No mismatch found; the amendment proceeds.

## 3. Authority identities consumed (recomputed live this act)

| Artifact | Bytes | Lines | SHA-256 (uppercase) | vs. prior citation |
|---|---|---|---|---|
| `BANPU_WP5_WORK_PACKAGE_PLAN.md` (original, being amended additively) | 42,903 | 604 | `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523` | first live computation of the full current file; internal citations within it (Allocation/Authorization identities) independently cross-checked and `EXACT` |
| `BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md` | 16,491 | 158 | `8DD43B1202714213E9EF88A65582E59A492680B747412BDAC9F176D3C43A2223` | `EXACT` |
| `BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md` | 18,755 | 145 | `BBE93F45237D6517E047A1E4FC8FC7A7665615975789F9E0AE9E6B846273EAE8` | `EXACT` |
| `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md` | 32,307 | 237 | `DC8C272CD35854A156C9AD51494FE232C5408373A947AEC1B314D9657159E75B` | `EXACT` |
| `BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_FRESH_INDEPENDENT_REAPPROVAL.md` | 23,848 | 165 | `421FF4C0C6936B25EF3168A52B90550556791A150CA68A1912AD9BCE7BC566BA` | `EXACT` |
| `BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_BINDING_FREEZE_RECORD.md` | 22,742 | 170 | `6EC85ED13623B9817964F6BC5372D578DBF90AA9BCC2B1465CE086E361A2E6E4` | first live recomputation this act; self-consistent with the record's own §3 self-citation of its predecessors |

No mismatch. This amendment binds itself to the exact frozen D7 authority (`DC8C272C…59E75B`, bound at `6EC85ED1…2E6E4`) and the exact original WPP (`0455ABA9…1DF523`) it supplements.

## 4. Amendment strategy and artifact treatment

Independently re-read `BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT.md` in full this act. Repository convention, confirmed there (§2): the original Plan is preserved byte-for-byte at its own identity; a single additive amendment artifact supplements named sections; the amendment states which original sections it "amends" without rewriting their bytes; and the amendment does not become operative implementation authority until its own independent reapproval completes. This amendment follows that convention exactly:

- `BANPU_WP5_WORK_PACKAGE_PLAN.md` is not modified. Its identity (§3) is unchanged by this act.
- This is the sole Work Package Plan-amendment artifact created by this act.
- The original WPP's §10.4 text, its `WP5-BLOCKED` acceptance-matrix row, and its `BLOCKED` residual-register row remain exactly as written — the historical fact that a genuine planning blocker existed and was later resolved by separate governance/authority acts is preserved, not erased (per this invocation's §3 instruction and the WP4 precedent's own §2.3 principle that "historical text remains evidence unless an independently reviewed and confirmed additive supplement is bound or recognized as successor").
- This amendment becomes the recognized successor for §10.4 planning only after its own independent reapproval (§16 below), exactly mirroring the WP4 pattern.

## 5. Scope of amendment

This amendment supplements Work Package Plan §10.4, §15 (adds rows `WP5-A15`…`WP5-A32`), §17 (updates the two `MINOR-2` WP5-half residual rows), §19 (adds the §10.4 evidence conditions to the completion-evidence gate), and §22 (restates the next act now that §10.4 is planned). It does not reopen, redesign, or modify:

- WP5-C1 through WP5-C6 or their existing §11–§13 design;
- §10.3 tolerance-admissibility planning (`PD-WP5-1`, rows `WP5-A12`–`WP5-A14`) — unchanged, inherited by reference;
- the accounting-reader design (§11), rebuild-boundary design (§8–§9), pre-boundary preservation contract (§9), suspension-gap return behavior (§12), or successor-identity design (§13);
- any existing acceptance row `WP5-A1` through `WP5-A14`, which keep their original identifiers and content unchanged;
- §16 regression requirements, §18 sequencing tasks `WP5-T1`–`WP5-T11`, `WP5-T13`–`WP5-T14` (`WP5-T12`, "submit §10.4 for a separate planning decision," is now discharged by this amendment — §14 below), or §20 prohibited acts; or
- any downstream residual classification in §17 not naming `MINOR-2`'s WP5 reconciliation half.

All unaffected original WPP content is inherited unchanged by reference.

## 6. D2–D6 binding contract consumed (not reopened)

Restated for planning completeness from the frozen design clarification (§3 identity), with no reinterpretation:

- **D2 — formula:** `implied_successor_value = R × P_succ`; `absolute_gap = abs(P_pre − implied_successor_value)`; `metric_pct = (absolute_gap / P_pre) × 100`, all in exact `Decimal` arithmetic (clarification §6).
- **D3 — tolerance:** `mechanical_nav_tolerance_pct` only; no second tolerance; dimensionally compatible with `metric_pct` (clarification §7).
- **D4 — inclusivity:** `PASS` iff `metric_pct <= mechanical_nav_tolerance_pct`; equality passes (clarification §8).
- **D5 — numeric policy:** `Decimal` construction from payload strings only; no binary float; no intermediate quantization; no final quantization; no new rounding mode; ambient `Decimal` context governs residual precision; non-finite/malformed/missing operands → `NOT_EVALUABLE`, never a numeric comparison (clarification §9).
- **D6 — annotation:** `null`/`""`/whitespace-only → absent; non-empty after `.strip()` → present; an unannotated `FAIL` → `MECHANICAL_CONTINUITY_FAILURE`; an annotated `FAIL` → `ANNOTATED_BOUNDARY_DISCONTINUITY`; a `PASS` is `PASS` regardless of annotation; annotation never affects `NOT_EVALUABLE`, never suppresses computation of `metric_pct`, never widens the tolerance, never affects any other check (clarification §10–§11).

No amendment discretion is exercised over any of the above; this section is planning consumption, not re-derivation.

## 7. D7 architecture planned

Bound unchanged from the D7 amendment and Binding Freeze Record (§3 identity):

- **Pure classifier — `_evaluate_mechanical_continuity()`:** consumes the canonical parsed `PositionConversionBoundaryEvidence` plus `conversion_ratio`; computes D2; applies D3/D4; normalizes and applies D6; returns the exact semantic state (`PASS` / `MECHANICAL_CONTINUITY_FAILURE` / `ANNOTATED_BOUNDARY_DISCONTINUITY` / `NOT_EVALUABLE`) plus `metric_pct` and sufficient evidence fields for audit reporting; performs no mutation; contains no CLI exit-code policy.
- **Audit consumer — `_audit_mechanical_continuity()`:** consumes the classifier result; maps it into the existing `verify_snapshots` `AuditAnomaly`/severity model (§9 below); preserves `metric_pct` and evidence in `details`; performs no mutation.
- **Sole consumer:** `verify_snapshots`, invoked from `_audit_portfolio()` only for a portfolio whose ledger contains a `POSITION_CONVERSION`. No reconstruction consumer; no second runtime consumer.
- **Audit identity:** `AuditCheck.MECHANICAL_CONTINUITY`, a new member of the already-authorized `AuditCheck` enum in `manage.py`, confirmed by live grep still absent and non-colliding with `NAV_CONTINUITY`, `PNL_CONTINUITY`, `HOLDINGS_INTEGRITY`, `PRICE_INTEGRITY`, `RETURN_SANITY`, and distinct from `POSITION_CONVERSION_REBUILD_BOUNDARY` (which is not an `AuditCheck` member at all — it is a `rebuild_portfolio()` refusal, §10 below).

## 8. Canonical input plan

D7 obtains all inputs exclusively through the frozen WP1 canonical parser output (`parse_position_conversion_payload()` → `PositionConversionBoundaryEvidence`), specifically:

- `boundary_evidence.predecessor_reference_price` (`P_pre`);
- `boundary_evidence.successor_reference_price` (`P_succ`);
- `boundary_evidence.mechanical_nav_tolerance_pct`;
- `boundary_evidence.suspension_gap_annotation`; and
- the canonical `conversion_ratio` from `conversion_payload.conversion_ratio`.

**Explicitly prohibited re-derivation sources:** ticker/display strings, provider lookup, current quote lookup, snapshot inference, or any caller-provided substitute value. No such source is authorized anywhere in the D7 architecture (§7), and this amendment introduces no exception.

**Missing/malformed handling:** any of the five canonical values absent, non-`Decimal`-parseable, non-finite, or (for `P_pre`) non-positive routes the classifier to `NOT_EVALUABLE` (D5, §6 above) without inventing an alternate parser contract, a default value, or a second admissibility path distinct from the one WP1 already establishes. The classifier performs no parsing of its own beyond consuming the already-typed `PositionConversionBoundaryEvidence` fields; it is not a second implementation of `parse_position_conversion_payload()`.

## 9. Outcome handling planned (four states, no fifth invented)

| State | Severity | Exit-code contribution | Mutation | Notes |
|---|---|---|---|---|
| `PASS` | none | none | none | No `AuditAnomaly` emitted; normal verification continues (design clarification §12; D4 inclusive) |
| `ANNOTATED_BOUNDARY_DISCONTINUITY` | `WARNING` | contributes to exit `1` only, per `verify_snapshots`' existing WARNING semantics | none | Metric and evidence remain visible in `details`; never becomes `PASS`; never becomes `CRITICAL` solely for exceeding tolerance; genuine suspension-gap return remains genuine return (§12 below) |
| `MECHANICAL_CONTINUITY_FAILURE` | `CRITICAL` | contributes to exit `2`, existing CRITICAL semantics | none | Fail-closed for verification acceptance only; no reconstruction or quarantine authority created |
| `NOT_EVALUABLE` | `CRITICAL` | contributes to exit `2` | none | Diagnostic text distinct from `MECHANICAL_CONTINUITY_FAILURE`; never silently treated as `PASS` |

No fifth state is planned or authorized.

## 10. Authorized implementation surface (unchanged, distinguished from existing §6 planning)

Both files were already named in the original WPP §6 table and the Authorization Record §4.1/§4.2; this amendment authorizes no new file.

| File | Existing WPP §6 planning (§10.3 only) | New §10.4 addition planned by this amendment |
|---|---|---|
| `backend/manage.py` | additive audit check reporting `mechanical_nav_tolerance_pct` admissibility only (`ADMISSIBLE`/`NEGATIVE`/`NON_FINITE`/`NON_DECIMAL_EXACT`/`ABSENT`); no reconciliation comparison, no `MECHANICAL_CONTINUITY_FAILURE`/`ANNOTATED_BOUNDARY_DISCONTINUITY` finding | add `_evaluate_mechanical_continuity()` (pure classifier, §7), `_audit_mechanical_continuity()` (audit consumer, §7), and the `AuditCheck.MECHANICAL_CONTINUITY` enum member; invoke the new audit consumer from `_audit_portfolio()` alongside (not merged with) the existing §10.3 tolerance-admissibility check, for the same class of `POSITION_CONVERSION`-bearing portfolios |
| `backend/tests/test_verify_snapshots.py` | `WP5-A12`–`WP5-A14` (tolerance admissibility only) | add `WP5-A15`–`WP5-A32` (§13 below) |

Existing structures reused: the `_audit_portfolio()` per-portfolio audit loop, the `AuditAnomaly`/severity model, the `AuditCheck` enum, and the §10.3 pattern of a read-only, non-blocking finding. Nothing outside these two files is authorized; `portfolio_rebuilder.py`, the WP3 quote-contract module, and WP4's canonicalization/materialization modules remain explicitly unauthorized for this obligation (Authorization Record §4, §11; reaffirmed unchanged by the D7 amendment §15 and both reapprovals).

## 11. Rebuild-boundary separation (preserved)

`POSITION_CONVERSION_REBUILD_BOUNDARY` (in `portfolio_rebuilder.py`, §8–§9 of the original WPP) and mechanical continuity (D7, this amendment) remain two separate WP5 obligations:

- the rebuild boundary protects the admissible reconstruction range — it is a refusal gate inside `rebuild_portfolio()`, raised before any write or provider fetch;
- mechanical continuity audits canonical conversion evidence — it is a read-only, non-blocking `verify_snapshots` finding;
- either may conceptually succeed or fail independently of the other — a portfolio can fail the rebuild-boundary guard while passing mechanical continuity, or vice versa, with no shared predicate;
- D7 does not authorize reconstruction, and this amendment grants no such authority; and
- D7 does not alter the existing rebuild-boundary planning at WPP §8–§9, which this amendment leaves untouched (§5 above).

No shared result identity, shared predicate, or shared invocation point is planned. `AuditCheck.MECHANICAL_CONTINUITY` and the `PositionConversionRebuildBoundaryError`/`POSITION_CONVERSION_REBUILD_BOUNDARY` mechanism remain distinct.

## 12. Suspension-gap invariant (planned proof obligation)

Implementation and tests must demonstrate that an annotated above-tolerance result:

- retains the computed `metric_pct` unmodified, unclamped, unsmoothed (clarification §11);
- remains above `mechanical_nav_tolerance_pct`;
- produces `ANNOTATED_BOUNDARY_DISCONTINUITY`;
- maps to `WARNING` (§9 above);
- performs no mutation of any snapshot, NAV, basis, or cash-flow field; and
- does not become `PASS`.

No clamping, smoothing, or artificial continuity is planned or permitted anywhere in the D7 architecture (§7).

## 13. Acceptance matrix amendment

Existing rows `WP5-A1`–`WP5-A14` and `WP5-BLOCKED` are unchanged and keep their identifiers (§5). The following rows are added, extending §15 of the original WPP:

| ID | Obligation | Governing requirement/source | Implementation surface | Required test/evidence | Expected result | Failure condition |
|---|---|---|---|---|---|---|
| `WP5-A15` | Below-tolerance reconciliation | clarification §6, §8 (D2, D4) | `manage.py` | `test_verify_snapshots.py`, `metric_pct < tolerance` fixture | `PASS`, no `AuditAnomaly` | anomaly reported |
| `WP5-A16` | Exact-tolerance reconciliation (boundary inclusivity) | clarification §8 (D4) | `manage.py` | same, `metric_pct == tolerance` fixture | `PASS` | `FAIL`/anomaly reported |
| `WP5-A17` | Above-tolerance, no annotation (`null`) | clarification §10 (D6) | `manage.py` | same, `metric_pct > tolerance`, `suspension_gap_annotation = null` | `MECHANICAL_CONTINUITY_FAILURE`, `CRITICAL`, exit-2 contribution | `PASS`, `WARNING`, or silent |
| `WP5-A18` | Above-tolerance, empty-string annotation | clarification §10 (D6 normalization) | `manage.py` | same, `annotation = ""` | same as `WP5-A17` | reclassified as annotated |
| `WP5-A19` | Above-tolerance, whitespace-only annotation | clarification §10 (D6 normalization) | `manage.py` | same, `annotation = "   "` | same as `WP5-A17` | reclassified as annotated |
| `WP5-A20` | Above-tolerance, non-empty trimmed annotation | clarification §10 (D6) | `manage.py` | same, `annotation = "<evidence text>"` | `ANNOTATED_BOUNDARY_DISCONTINUITY`, `WARNING`, exit-1 contribution only, `metric_pct` preserved unmodified in `details`, no snapshot/NAV/basis/cash-flow field mutated | `PASS`, `CRITICAL`, or metric altered/dropped |
| `WP5-A21` | Missing required boundary evidence | clarification §6 (D2 missing-operand rule) | `manage.py` | fixture with `P_pre`, `P_succ`, tolerance, or `conversion_ratio` absent | `NOT_EVALUABLE` | numeric comparison attempted |
| `WP5-A22` | Malformed required numeric evidence (non-`Decimal`-parseable string) | clarification §6, §9 (D5) | `manage.py` | fixture with malformed numeric string | `NOT_EVALUABLE` | comparison attempted or crash |
| `WP5-A23` | Non-finite numeric evidence (`NaN`/`Infinity`) | clarification §6, §9 (D5) | `manage.py` | fixture with non-finite value | `NOT_EVALUABLE` | numeric comparison attempted |
| `WP5-A24` | Non-positive predecessor reference price | clarification §6 (D2 zero/invalid-denominator rule) | `manage.py` | fixture with `P_pre <= 0` | `NOT_EVALUABLE` | division attempted or `PASS`/`FAIL` returned |
| `WP5-A25` | Invalid/non-positive conversion ratio | clarification §6; canonical input contract (§8 above) | `manage.py` | fixture with `R <= 0` or malformed `R` | `NOT_EVALUABLE` | comparison computed with invalid `R` |
| `WP5-A26` | `NOT_EVALUABLE` distinct from `MECHANICAL_CONTINUITY_FAILURE`, never silent `PASS` | clarification §6, §12 | `manage.py` | assert distinct diagnostic text/finding code across `WP5-A21`–`WP5-A25` vs. `WP5-A17`–`WP5-A19` | distinguishable in `AuditAnomaly` output | states conflated or `NOT_EVALUABLE` silently dropped |
| `WP5-A27` | Decimal-only arithmetic | clarification §9 (D5) | `manage.py` | static/type assertion or fixture proving no `float()` conversion occurs in the classifier | all intermediate/final values are `Decimal` | any `float` participates |
| `WP5-A28` | No intermediate/final quantization | clarification §9 (D5) | `manage.py` | fixture with a value requiring more precision than a rounded result would retain | full-precision `Decimal` result, no premature rounding | quantized/rounded intermediate or final value |
| `WP5-A29` | `AuditCheck.MECHANICAL_CONTINUITY` used and distinct | §7 above; D7 amendment §7 | `manage.py` | assert the emitted `AuditAnomaly.check == AuditCheck.MECHANICAL_CONTINUITY`, distinct from `NAV_CONTINUITY`/other members | correct, distinct identity | wrong/missing check identity |
| `WP5-A30` | No mutation performed by the D7 audit path | §7, §9 above (`verify_snapshots` read-only) | `manage.py` | before/after DB-state comparison across a `_audit_mechanical_continuity()` invocation for every outcome state | zero DB writes | any row written/modified |
| `WP5-A31` | No coupling to `POSITION_CONVERSION_REBUILD_BOUNDARY` | §11 above | `manage.py`, `portfolio_rebuilder.py` (regression only, not edited) | fixture portfolio failing mechanical continuity but passing/unaffected by the rebuild-boundary guard, and vice versa | independent outcomes, no shared predicate or call path | either outcome influences the other |
| `WP5-A32` | Canonical parser is sole input authority; no provider/current-quote lookup | §8 above | `manage.py` | assert the classifier performs no network/provider/ticker-lookup call; inputs traced only to `PositionConversionBoundaryEvidence`/`conversion_ratio` | no such call occurs | any provider/quote/ticker-derived substitute value used |

Historical rows `WP5-A1`–`WP5-A14` are not renumbered. `WP5-BLOCKED` (§15 of the original WPP) is superseded for planning purposes by `WP5-A17`–`WP5-A32` and is retained in the matrix, unmodified, as the historical record that the obligation was once blocked (§4 above).

## 14. `MINOR-2` planning disposition

Effective for this amendment and all subsequent lifecycle acts that consume it:

**`FULLY PLANNED — IMPLEMENTATION PENDING`**

This does not mean `RESOLVED`, `CLOSED`, `DISCHARGED`, `IMPLEMENTED`, or `ACCEPTED` — those require implementation and acceptance evidence (§15's matrix), which this amendment does not perform. The original WPP header's `PARTIALLY PLANNABLE — TOLERANCE ADMISSIBILITY READY; RECONCILIATION FORMULA BLOCKED AT A PLANNING BOUNDARY` disposition is preserved as historical text at the original WPP's unchanged identity (§3); it is superseded prospectively, for planning purposes, by this section.

## 15. Status of the original §10.4 blocker

**`ORIGINAL §10.4 BLOCKER RESOLVED BY ADDITIVE AUTHORITY — PLANNING NOW COMPLETE FOR THIS OBLIGATION.`**

This is a planning-level resolution only, for subsequent lifecycle acts. It does not mean:

- the original WPP's §10.4 text, `WP5-BLOCKED` row, or `BLOCKED` residual row have been rewritten (§4 — they have not);
- implementation of D7 has occurred (it has not — §2, live grep confirmed absent);
- `MINOR-2` is closed (§14 — it is not); or
- WP5 Planning Confirmation or Planning Freeze have occurred (§2 — confirmed absent).

## 16. Full-WPP blocker scan and overall readiness

Independent re-inspection of the entire original WPP (all 604 lines, re-read in full this act, §2) for any `BLOCKED`, `TBD`, unresolved decision, missing authority, or acceptance ambiguity outside §10.4:

- a live grep for `BLOCK|TBD|ambiguous|unresolved|undetermined` across the full WPP returns exactly seven matches, all of which trace to the single §10.4 obligation (the header disposition line, the §10.4 heading, its body text, the `WP5-BLOCKED` matrix row and its two neighboring explanatory sentences, and the `MINOR-2` residual row) — no other blocker, ambiguity, or undetermined item exists anywhere in the document;
- §3–§9, §11–§14, §16, §18, §20–§21 contain no `BLOCKED`/`TBD`/open-decision language;
- the only other "`OPEN`" states in the corpus (`MINOR-2` WP5-half implementation obligation, `POSITION_CONVERSION_REBUILD_BOUNDARY` predicate, both recorded `OPEN — IMPLEMENTATION-TIME` in the Authorization Record §5) are ordinary, expected implementation-time pre-use gates, not planning blockers — the WPP already plans both of them fully (rebuild-boundary at §8–§9; tolerance admissibility at §10.3; mechanical continuity now at §6–§13 of this amendment) and treats their implementation-time discharge as a later evidence obligation, exactly as this amendment treats §10.4.

No other planning blocker exists.

**Overall WPP readiness: Outcome A — `WPP AMENDMENT COMPLETE — NO REMAINING PLANNING BLOCKERS`.**

## 17. Exclusions

This amendment does not: implement D7; modify application code; modify test code; reopen D2–D7; modify the design clarification, authority reconciliation, D7 amendment, either D7 reapproval, or the D7 Binding Freeze Record; perform Independent Reapproval of itself; perform Planning Confirmation; perform Planning Freeze; close `MINOR-2`; execute snapshot reconstruction; mutate production data; perform WP6/WP7/WP8 work; release or deploy; or stage, commit, or push.

## 18. Reliance boundary and lifecycle state

This amendment is authored but has not been independently reapproved. Its current lifecycle state is therefore:

```text
D7 IMPLEMENTATION AUTHORIZATION AMENDMENT BOUND / FROZEN / AUTHORITATIVE
WPP AMENDMENT PREPARED — NOT YET INDEPENDENTLY REAPPROVED
IMPLEMENTATION MAY NOT YET RELY ON THE §10.4 PLANNING IN THIS AMENDMENT
```

The author of this record cannot supply its own independent reapproval. Until that separate act completes, no implementer or implementation reviewer may treat §6–§13 of this amendment as operative Plan authority, and WP5-T12 (originally "submit §10.4 for a separate planning decision") is satisfied by this amendment's existence but does not itself authorize starting `WP5-T10`/`T11`-equivalent implementation for §10.4 ahead of reapproval.

## 19. Repository verification

All identities in §3 were recomputed from live repository bytes before this artifact was created. Additional verification (diff-check, whitespace, links, graphify, final `git status`) is performed after this file is written and reported in the final message.

| Verification | Result |
|---|---|
| Original WPP identity | recomputed live — `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523`; 42,903 bytes; 604 lines |
| Design clarification identity | `EXACT` |
| Authority reconciliation identity | `EXACT` |
| D7 amendment identity | `EXACT` |
| Fresh D7 reapproval identity | `EXACT` |
| D7 Binding Freeze Record identity | `EXACT` |
| Implementation or test change attributable to this act | `NONE` |
| Frozen/bound authority artifact modified | `NONE` |
| Original WPP bytes modified | `NONE` |
| Decision Log or Implementation INDEX changed by this act | `NONE` — repository convention does not require either during amendment authorship |
| Staging, commit, push, release, or deployment | `NONE` |

## 20. Plan-amendment disposition

**BANPU-WP5 WORK PACKAGE PLAN AMENDMENT (MECHANICAL CONTINUITY) PREPARED — NOT YET INDEPENDENTLY REAPPROVED.**

**IMPLEMENTATION MAY NOT YET RELY ON THIS AMENDMENT'S §10.4 PLANNING.**

## 21. Exact next constitutional act

Following the BANPU-WP4 Retry-Order amendment precedent (§4 above), the exact next constitutional act is **Independent BANPU-WP5 Work Package Plan Amendment Reapproval**, limited to this additive amendment's §10.4 planning (§6–§16). That reviewer must independently verify: the original WPP identity, the six authority identities in §3, exact semantic conformity of §6–§9 to the bound D2–D7 contract, scope preservation (§5), the acceptance-matrix additions (§13), the `MINOR-2` planning disposition (§14), the full-WPP blocker scan (§16), and the continuing implementation-reliance prohibition (§18). Only after that reapproval completes may WP5 Planning Confirmation and Planning Freeze — which govern the WPP as a whole, not merely §10.4 — be sought as later, separate acts. This act performs no part of that independent reapproval and does not perform Planning Confirmation or Planning Freeze.
