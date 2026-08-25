# BANPU-WP5 — Work Package Plan Amendment (Mechanical Continuity) Independent Reapproval

**Artifact class:** Additive independent constitutional Plan-amendment reapproval record
**Reapproval date:** 2026-08-14
**Independent reviewing authority:** Independent BANPU-WP5 Work Package Plan Amendment Reapproval Authority (distinct from the amendment-authorship authority, the design-clarification/reconciliation authorities, the D7 amendment/reapproval/binding-freeze authorities, and any future Planning Confirmation/Freeze authority)
**Candidate amendment:** [`BANPU_WP5_WORK_PACKAGE_PLAN_AMENDMENT_MECHANICAL_CONTINUITY.md`](BANPU_WP5_WORK_PACKAGE_PLAN_AMENDMENT_MECHANICAL_CONTINUITY.md)
**Candidate amendment identity:** raw SHA-256 `3ADAE8390462B8B93BCF19A3D8BF6182FB08D19D5860D97D4F8FE360851DFC4F`; 31,939 bytes; 268 physical lines
**Original Work Package Plan:** [`BANPU_WP5_WORK_PACKAGE_PLAN.md`](BANPU_WP5_WORK_PACKAGE_PLAN.md)
**Original Plan identity:** raw SHA-256 `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523`; 42,903 bytes; 604 physical lines
**Authoritative D2–D6 source:** [`BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md`](BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md); 16,491 bytes; 158 lines; SHA-256 `8DD43B1202714213E9EF88A65582E59A492680B747412BDAC9F176D3C43A2223`
**Authority-provenance reconciliation:** [`BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md`](BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md); 18,755 bytes; 145 lines; SHA-256 `BBE93F45237D6517E047A1E4FC8FC7A7665615975789F9E0AE9E6B846273EAE8`
**D7 amendment:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md); 32,307 bytes; 237 lines; SHA-256 `DC8C272CD35854A156C9AD51494FE232C5408373A947AEC1B314D9657159E75B`
**Fresh D7 Independent Reapproval:** [`BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_FRESH_INDEPENDENT_REAPPROVAL.md`](BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_FRESH_INDEPENDENT_REAPPROVAL.md); 23,848 bytes; 165 lines; SHA-256 `421FF4C0C6936B25EF3168A52B90550556791A150CA68A1912AD9BCE7BC566BA`
**D7 Binding Freeze Record:** [`BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_BINDING_FREEZE_RECORD.md`](BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_BINDING_FREEZE_RECORD.md); 22,742 bytes; 170 lines; SHA-256 `6EC85ED13623B9817964F6BC5372D578DBF90AA9BCC2B1465CE086E361A2E6E4`
**Sections independently reapproved:** Original Plan §10.4, §15, §17, §19, §22 only, as additively supplemented by the candidate
**Reapproval disposition:** `PLAN AMENDMENT INDEPENDENTLY REAPPROVED`
**Composite operational Plan:** `ORIGINAL WPP + INDEPENDENTLY REAPPROVED ADDITIVE §10.4 AMENDMENT`
**Implementation reliance on §10.4 planning:** `PERMITTED ONLY AFTER WP5 PLANNING CONFIRMATION AND PLANNING FREEZE COMPLETE (§16 BELOW) — NOT YET PERMITTED`
**Implementation or test change performed:** `NO`
**Planning Confirmation or Planning Freeze performed:** `NO`
**`MINOR-2` closed by this act:** `NO`
**Release, deployment, production execution, or production-data authority:** `NONE`

---

## 1. Nature and independence of this act

Acting only as the independent Plan-amendment reapproval authority, this act reviews the exact candidate identity above against the live original WPP, the live design clarification, reconciliation, D7 amendment, fresh D7 reapproval, and D7 Binding Freeze Record. The candidate's own report and embedded verification tables were **not** accepted as proof; every identity, semantic claim, and live-code claim was independently reproduced from live repository bytes this act (§2–§9). This act neither authors nor modifies the candidate. It performs no WP5 implementation, no code or test change, no Planning Confirmation, no Planning Freeze, no `MINOR-2` closure, no snapshot reconstruction, no production mutation, and no WP6+/M46 act.

## 2. Entry lifecycle state (independently re-verified)

| # | Condition | Independent verification | Result |
|---|---|---|---|
| 1 | WP5 remains `ALLOCATED` | `BANPU_WP5_ALLOCATION_RECORD.md` re-read, unchanged | `CONFIRMED` |
| 2 | WP5 implementation authorization remains bounded | `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md` re-read, `AUTHORIZED — BOUNDED`, §13 implementation `NOT STARTED` | `CONFIRMED` |
| 3 | Original WPP remains `NOT CONFIRMED`/`NOT FROZEN` | header line 4 re-read live: `MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN` | `CONFIRMED` |
| 4 | Original WPP bytes unchanged | identity recomputed live (§3) — matches every prior citation exactly | `CONFIRMED` |
| 5 | D7 remains `BOUND AND FROZEN` | Binding Freeze Record §14/§21 re-read live, disposition `FREEZE APPROVED` / `D7 IMPLEMENTATION AUTHORIZATION AMENDMENT — BOUND AND FROZEN` | `CONFIRMED` |
| 6 | WPP Amendment exists, not yet independently reapproved | candidate §18 re-read live: `PLAN AMENDMENT PREPARED — NOT YET INDEPENDENTLY REAPPROVED`; no prior `*_INDEPENDENT_REAPPROVAL` file for this amendment existed before this act (`ls` confirmed absent, §3) | `CONFIRMED` |
| 7 | No Planning Confirmation exists | `ls docs/implementation/ \| grep -i "WP5.*PLANNING_CONFIRMATION"` → no match; the one `PLANNING_CONFIRMATION`-named file in the directory (`M46_PLANNING_CONFIRMATION.md`) belongs to an unrelated milestone | `CONFIRMED ABSENT` |
| 8 | No Planning Freeze exists | `ls docs/implementation/ \| grep -i "WP5.*PLANNING_FREEZE"` → the only match, `M44_WP5_PLANNING_FREEZE_RECORD.md`, opened and read (§3): it is **M44-WP5** ("Portfolio Analytics Gate Closure and Normative Semantics"), a distinct, unrelated work-package numbering scheme — not BANPU-WP5. No BANPU-WP5 Planning Freeze Record exists | `CONFIRMED ABSENT — NO NAMING COLLISION` |
| 9 | No WP5 implementation relying on §10.4 has occurred | live grep for `_evaluate_mechanical_continuity\|_audit_mechanical_continuity\|MECHANICAL_CONTINUITY` across `backend/` → zero matches anywhere in application code; `AuditCheck` enum in `backend/manage.py` (lines 800–805) has exactly five members, none named `MECHANICAL_CONTINUITY` | `CONFIRMED ABSENT` |
| 10 | `MINOR-2` remains open as an implementation obligation | Binding Freeze Record §17: `DESIGN SEMANTICS RESOLVED — D7 IMPLEMENTATION AUTHORITY BOUND — IMPLEMENTATION OBLIGATION OPEN`; candidate §14: `FULLY PLANNED — IMPLEMENTATION PENDING`; neither is `RESOLVED`/`CLOSED`/`IMPLEMENTED` | `CONFIRMED OPEN` |

All ten entry conditions hold. No mismatch found. Reapproval review proceeds.

## 3. Identity and authority continuity (recomputed live, not copied)

| Artifact | Independently reproduced identity | Determination |
|---|---|---|
| Original Work Package Plan | `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523`; 42,903 bytes; 604 lines | `EXACT` |
| Candidate WPP Amendment | `3ADAE8390462B8B93BCF19A3D8BF6182FB08D19D5860D97D4F8FE360851DFC4F`; 31,939 bytes; 268 lines | `EXACT AND REVIEWED` |
| Design clarification | `8DD43B1202714213E9EF88A65582E59A492680B747412BDAC9F176D3C43A2223`; 16,491 bytes; 158 lines | `EXACT` |
| Authority-provenance reconciliation | `BBE93F45237D6517E047A1E4FC8FC7A7665615975789F9E0AE9E6B846273EAE8`; 18,755 bytes; 145 lines | `EXACT` |
| D7 amendment | `DC8C272CD35854A156C9AD51494FE232C5408373A947AEC1B314D9657159E75B`; 32,307 bytes; 237 lines | `EXACT` |
| Fresh D7 Independent Reapproval | `421FF4C0C6936B25EF3168A52B90550556791A150CA68A1912AD9BCE7BC566BA`; 23,848 bytes; 165 lines | `EXACT` |
| D7 Binding Freeze Record | `6EC85ED13623B9817964F6BC5372D578DBF90AA9BCC2B1465CE086E361A2E6E4`; 22,742 bytes; 170 lines | `EXACT` |
| WP5 Allocation Record | `D00D0AE886E6150F84663AA331338F764E193700EBCE944C88CB0D175CA8D687`; 15,590 bytes; 280 lines | `UNCHANGED` |
| WP5 Implementation Authorization Record | `DBCBC2BFCDB9F3A7D3E7912C6148445C68C39F5872A4DE2DEF58DF5B2BDE7F1E`; 19,039 bytes; 341 lines | `UNCHANGED` |

No identity mismatch anywhere in the chain. The candidate's own §3 self-citations of these six artifacts are byte-identical to what this act independently reproduces. The candidate consumes exactly the currently bound authority chain — no drift, no stale citation, no substitution.

## 4. Amendment form / precedent review

Independently re-read `BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT.md` and `BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT_INDEPENDENT_REAPPROVAL.md` in full this act (not merely cited from memory).

The WP4 precedent establishes: (a) the original Plan is preserved byte-for-byte at its own identity; (b) a single additive amendment supplements only the named sections; (c) the amendment states, but does not itself perform, its own reapproval; (d) the reapproval independently reproduces every identity and semantic claim rather than trusting the amendment's self-report; (e) the reapproval determines a **composite operational Plan** (original + reapproved amendment) that controls for the amended sections only, with all other original sections unchanged; and (f) the reapproval states explicitly what implementation reliance the composite Plan now permits, bounded to the existing authorization it operates under.

The WP5 candidate correctly follows this form:

- `BANPU_WP5_WORK_PACKAGE_PLAN.md` is not modified — confirmed unchanged (§3).
- The historical §10.4 blocker text, the `WP5-BLOCKED` acceptance row, and the `BLOCKED` residual row are preserved verbatim in the original WPP — independently re-read at lines 290, 455, and 493 of the live file; none has been rewritten.
- The candidate supplements only §10.4, §15, §17, §19, and §22 — verified against the original WPP's own section structure (§5 below).
- The candidate does not claim to have been part of the original WPP; its header explicitly states `PLAN AMENDMENT PREPARED — NOT YET INDEPENDENTLY REAPPROVED` prior to this act.

This is the correct repository form. **One material divergence from the WP4 precedent is identified and addressed rather than silently inherited (§16 below):** the WP4 reapproval's disposition permitted immediate implementation reliance because WP4's Work Package Plan had already passed its own Planning Confirmation/Freeze gate earlier in WP4's lifecycle, before the retry-order amendment was ever drafted — the amendment was a **mid-implementation** planning correction. WP5's Work Package Plan has **never** passed Planning Confirmation or Planning Freeze at all; its header has read `NOT CONFIRMED — NOT FROZEN` since materialization, blocked at §10.4 the entire time. Copying WP4's "implementation may now rely on this" disposition onto WP5 without accounting for that difference would be a precedent-application error. §16 below independently establishes the correct WP5-specific next act instead of assuming WP4's shape applies unmodified.

## 5. Scope containment

Independently compared the candidate's §5 (scope) against the live original WPP's own section list (re-read in full, lines 1–604):

- **Not reopened, confirmed:** WP5-C1 through WP5-C6 (§11–§13 design, unchanged); §10.3 tolerance-admissibility planning (`PD-WP5-1`, rows `WP5-A12`–`WP5-A14`, unchanged, still present verbatim); `POSITION_CONVERSION_REBUILD_BOUNDARY` (§8–§9, unchanged; also independently confirmed via live grep that this identity exists nowhere in `backend/portfolio_rebuilder.py` — it is a deferred finding ID referenced only in `backend/tests/test_ledger_validator.py:989`, consistent with its own `OPEN — IMPLEMENTATION-TIME` status, not yet implemented by anyone); accounting-reader behavior (§11); pre-boundary preservation (§9); suspension-gap return accounting (§3 of the design clarification, restated not redesigned — §7 below); successor identity (§13); WP3 semantics (independently re-grepped in `position_conversion_quote_contract.py`: WP5's mechanical tolerance remains explicitly named "out of scope" there, line 44 — WP3's ownership boundary is untouched); WP4 semantics (not referenced by the candidate at all beyond citing its WPP-amendment convention as structural precedent); WP6+ and M46 (not referenced).
- Existing acceptance rows `WP5-A1`–`WP5-A14` and `WP5-BLOCKED` retain their original identifiers and text, unrenumbered — confirmed by direct comparison against the live original WPP §15.

No scope expansion found.

## 6. D2–D6 fidelity review

Directly compared candidate §6 against the live design clarification §6–§11 this act, sentence by sentence:

- **D2:** candidate states `metric_pct = (abs(P_pre − R·P_succ) / P_pre) × 100` in exact Decimal arithmetic — matches clarification §6 verbatim (Alternative C, selected).
- **D3:** candidate states `mechanical_nav_tolerance_pct` is the sole tolerance, dimensionally compatible — matches clarification §7 verbatim.
- **D4:** candidate states `PASS iff metric_pct <= tolerance`, equality passes — matches clarification §8 verbatim, including the inclusive-boundary rationale.
- **D5:** candidate states Decimal-only, no float, no intermediate/final quantization, no invented rounding mode, malformed/non-finite/non-positive-where-required operands → `NOT_EVALUABLE` — matches clarification §9 verbatim, including the ambient-context-governs-precision clause.
- **D6:** candidate states null/empty/whitespace-only → absent, non-empty-trimmed → present, annotation reclassifies an already-computed `FAIL` only, `PASS` is unaffected, `NOT_EVALUABLE` is unaffected — matches clarification §10–§11 verbatim, including the anti-bypass bound (an empty/whitespace annotation does not reclassify a `FAIL`).

No semantic drift, narrowing, widening, or reinterpretation found anywhere in §6. The candidate operationalizes; it does not redesign.

## 7. D7 architectural fidelity — live-verified, not merely compared to text

Directly compared candidate §7 against the D7 amendment and Binding Freeze Record §8–§9, **and independently against the live state of `backend/manage.py`** (not trusting either document's self-report):

- `_evaluate_mechanical_continuity()` / `_audit_mechanical_continuity()`: confirmed **absent** from `backend/manage.py` and from every file in `backend/` (live grep, zero matches) — no premature implementation exists, and no naming collision exists.
- `AuditCheck.MECHANICAL_CONTINUITY`: confirmed absent from the live `AuditCheck` enum (`backend/manage.py:800–805`), which currently has exactly `NAV_CONTINUITY`, `PNL_CONTINUITY`, `HOLDINGS_INTEGRITY`, `PRICE_INTEGRITY`, `RETURN_SANITY` — five members, no collision with the reserved sixth identity.
- Sole consumer `verify_snapshots` via `_audit_portfolio()`: confirmed live — `_audit_portfolio()` (`backend/manage.py:1123–1151`) is the only per-portfolio audit dispatcher in the file and is called from exactly one place, `_cmd_verify_snapshots()` (line 1290). No second dispatcher or consumer exists anywhere in `backend/`.
- Authorized surface: confirmed both named files (`backend/manage.py`, `backend/tests/test_verify_snapshots.py`) are the only ones the candidate authorizes; `backend/services/portfolio_rebuilder.py` and the WP3/WP4 modules are correctly excluded (§5 above).

No second consumer, new module, reconstruction hook, mutation path, or widened file authority is introduced. Architectural fidelity is exact.

## 8. Canonical input review — live-verified against the parser

Directly inspected `backend/services/transaction_canonicalizer.py` this act (not trusting the candidate's field-name citations):

- `PositionConversionBoundaryEvidence` (line 146) declares exactly `predecessor_reference_price`, `successor_reference_price`, `mechanical_nav_tolerance_pct`, `suspension_gap_annotation` (lines 147–150) — all four field names match the candidate's §8 citation exactly.
- `conversion_ratio` is parsed at the top-level payload (`parse_position_conversion_payload()`, line 360) and carried onto the parse result (lines 502, 526, 538) — matches the candidate's fifth canonical input exactly.
- The parser already enforces `conversion_ratio > 0` at ingestion (line 451: `if shares_surrendered <= 0 or conversion_ratio <= 0 or shares_received <= 0: ...error`). This does not weaken the candidate's `WP5-A25` row (a defensive `NOT_EVALUABLE` fixture for `R <= 0`/malformed `R` reaching the classifier) — it is consistent defense-in-depth against malformed or historical rows, not a second admissibility path, and introduces no ambiguity.
- No alternate re-derivation source (ticker/display, provider lookup, current quote, snapshot inference, caller substitute) exists anywhere near these fields in the canonicalizer. The candidate's prohibition on such sources (§8) is not merely stated but is consistent with what the live parser actually offers as the sole route to these values.

Malformed/missing canonical evidence deterministically routes to `NOT_EVALUABLE` under D5 without inventing a second parser contract. No ambiguity found.

## 9. Four-state / audit-severity review — live-verified, not trusted from the candidate's report

Read `_cmd_verify_snapshots()` (`backend/manage.py:1255–1310`) directly this act:

```text
# Exit codes: 0 = clean, 1 = warnings, 2 = critical failures
total_crit = sum(len(r.criticals) for r in results)
total_warn = sum(len(r.warnings)  for r in results)
if total_crit: return 2
if total_warn: return 1
return 0
```

This confirms, from the live implementation and not from the candidate's self-report, that the candidate's §9 outcome table is accurate: `WARNING` severity contributes only to exit code `1`; `CRITICAL` severity contributes to exit code `2`; a clean run returns `0`. The candidate's mapping of `ANNOTATED_BOUNDARY_DISCONTINUITY → WARNING/exit-1` and `MECHANICAL_CONTINUITY_FAILURE`/`NOT_EVALUABLE → CRITICAL/exit-2` is exactly consistent with this live behavior. No discrepancy found. Exactly four states are planned; no fifth is introduced anywhere in the candidate.

**One completeness observation, not a semantic defect:** acceptance rows `WP5-A21`–`WP5-A25` (the `NOT_EVALUABLE` fixtures) state the expected *result* as `NOT_EVALUABLE` but do not individually re-assert the `CRITICAL`/exit-`2` severity mapping the way `WP5-A17` does for `MECHANICAL_CONTINUITY_FAILURE`. `WP5-A26` requires the two families be "distinguishable in `AuditAnomaly` output" but does not in terms explicitly require asserting `NOT_EVALUABLE`'s severity field. §9's outcome table is itself unambiguous (`NOT_EVALUABLE → CRITICAL`), so this leaves no implementation discretion — but it is a test-evidence completeness gap worth correcting when `WP5-A21`–`WP5-A26` are implemented (each should assert `severity == AuditSeverity.CRITICAL` and the exit-code-2 contribution, not merely the state label). Flagged in §17; **non-blocking**.

## 10. Suspension-gap invariant

Candidate §12 requires: `metric_pct` preserved unmodified/unclamped/unsmoothed; remains above tolerance; produces `ANNOTATED_BOUNDARY_DISCONTINUITY`; maps to `WARNING`; no mutation of snapshot/NAV/basis/cash-flow; never becomes `PASS`. Cross-checked directly against design clarification §11 ("Annotation changes only the *classification* attached to a real, unmodified numeric discontinuity — never the discontinuity itself... An unannotated, unexplained discontinuity is not silently accepted as return"). Exact match. No clamping, smoothing, or artificial continuity is planned or permitted anywhere in the candidate or the D7 architecture it consumes.

## 11. Rebuild-boundary independence

Confirmed independently (§5 above) that `POSITION_CONVERSION_REBUILD_BOUNDARY` does not yet exist in `backend/services/portfolio_rebuilder.py` — it is presently only a deferred finding-ID string in a WP2-emission-path regression test. There is therefore, as a live-code fact and not merely a planning intention, zero call-path coupling, zero shared predicate, and zero shared result identity between it and mechanical continuity today. The candidate's §11 claim of independence is consistent with this and creates no future coupling: `WP5-A31` requires proof that the two remain independent once both are implemented. No D7 authority is added to `portfolio_rebuilder.py` by the candidate.

## 12. Acceptance matrix review — row by row, not merely counted

Individually reviewed `WP5-A15` through `WP5-A32` (18 rows) against the instruction's 27-item coverage checklist:

| Checklist item | Row(s) | Determination |
|---|---|---|
| Below tolerance | `WP5-A15` | `CONFORMING` |
| Exact tolerance (inclusive boundary) | `WP5-A16` | `CONFORMING` |
| Above tolerance + null annotation | `WP5-A17` | `CONFORMING` |
| Empty-string annotation | `WP5-A18` | `CONFORMING` |
| Whitespace-only annotation | `WP5-A19` | `CONFORMING` |
| Non-empty annotation | `WP5-A20` | `CONFORMING` |
| Annotated → `WARNING` | `WP5-A20` | `CONFORMING` |
| Unannotated → `CRITICAL` | `WP5-A17` | `CONFORMING` |
| Missing evidence | `WP5-A21` | `CONFORMING` |
| Malformed evidence | `WP5-A22` | `CONFORMING` |
| Non-finite evidence | `WP5-A23` | `CONFORMING` |
| Non-positive predecessor price | `WP5-A24` | `CONFORMING` |
| Invalid/non-positive conversion ratio | `WP5-A25` | `CONFORMING` |
| Decimal-only calculation | `WP5-A27` | `CONFORMING` |
| No quantization | `WP5-A28` | `CONFORMING` |
| Inclusive comparison | `WP5-A16` | `CONFORMING` |
| Metric preservation | `WP5-A20` | `CONFORMING` |
| Annotation does not mutate accounting | `WP5-A20`, `WP5-A30` | `CONFORMING` |
| `NOT_EVALUABLE` distinct from failure | `WP5-A26` | `CONFORMING (see §9 note above)` |
| `AuditCheck.MECHANICAL_CONTINUITY` used | `WP5-A29` | `CONFORMING` |
| Existing `WARNING` behavior preserved | `WP5-A20` | `CONFORMING` |
| Existing `CRITICAL` behavior preserved | `WP5-A17` | `CONFORMING` |
| Exit-code behavior | `WP5-A17`, `WP5-A20` | `CONFORMING (NOT_EVALUABLE rows should be extended — §9)` |
| Read-only behavior | `WP5-A30` | `CONFORMING` |
| Rebuild-boundary independence | `WP5-A31` | `CONFORMING` |
| No provider/current-quote lookup | `WP5-A32` | `CONFORMING` |
| Canonical parser sole authority | `WP5-A32` | `CONFORMING` |

Every checklist item maps to at least one concrete, independently observable row. Historical rows `WP5-A1`–`WP5-A14` and `WP5-BLOCKED` are unrenumbered and unmodified, confirmed by direct comparison. Grouping (e.g., `WP5-A20` covering annotation presence, classification, severity, and metric preservation together) leaves no obligation implicit — each grouped row names every assertion it must make. Aside from the §9 completeness note (non-blocking), no acceptance requirement leaves implementation discretion.

## 13. `MINOR-2` disposition review

Candidate §14 states `FULLY PLANNED — IMPLEMENTATION PENDING` and explicitly disclaims `RESOLVED`/`CLOSED`/`DISCHARGED`/`IMPLEMENTED`/`ACCEPTED` — independently confirmed by direct re-read of candidate §14. This is the strongest justified state: design semantics are fixed (D2–D6, bound), enforcement locus is fixed (D7, bound and frozen), but zero implementation or acceptance evidence exists (§2, §7 above) — `IMPLEMENTED`/`ACCEPTED` would be false; `RESOLVED`/`CLOSED`/`DISCHARGED` would conflate planning completion with implementation completion, contrary to the Binding Freeze Record's own §17 (`IMPLEMENTATION OBLIGATION OPEN`). Confirmed correct.

## 14. Original §10.4 blocker trace and resolution

Each of the five original unresolved elements is traced to the exact artifact that resolves it:

| Original unresolved element | Resolved by | Section |
|---|---|---|
| D2 formula | Design clarification | §6 |
| D4 inclusivity | Design clarification | §8 |
| D5 comparison precision | Design clarification | §9 |
| D6 annotation threshold/classification | Design clarification | §10–§11 |
| D7 enforcement locus | D7 amendment, bound by the Binding Freeze Record | D7 amendment §7 / Binding Freeze §9 |

All five are covered by artifacts independently confirmed unchanged and exact (§3 above) and independently confirmed content-faithful (§6–§7 above). The candidate's §15 statement — `ORIGINAL §10.4 BLOCKER RESOLVED BY ADDITIVE AUTHORITY — PLANNING NOW COMPLETE FOR THIS OBLIGATION` — is independently agreed.

## 15. Full-WPP blocker scan (independently reproduced)

The candidate's §16 reports "exactly seven matches" for the pattern `BLOCK|TBD|ambiguous|unresolved|undetermined` across the original WPP. **Independently re-running the identical pattern against the live 604-line file this act returns 17 matching lines, not seven** — a factual inaccuracy in the candidate's self-reported evidence. Each of the 17 lines was individually inspected in context rather than counted:

- 13 lines trace directly and unambiguously to the single §10.4/`WP5-BLOCKED`/`MINOR-2` obligation (the header disposition line; the §10.4 heading and three sentences of its body; the entry-table's citation of WP4's "blocked-task conventions" naming pattern; the `WP5-BLOCKED` matrix row and its two neighboring explanatory sentences; the `MINOR-2` residual row and its two neighboring sentences; the `WP5-T12` task row and its "does not block T1–T11" clarifying sentence).
- 4 lines are false-positive keyword hits on the words "block"/"blocking" used in a **non-blocker, descriptive** sense unrelated to §10.4: line 151 and line 434 both describe the §10.3 tolerance-admissibility check's *non-blocking, read-only* design property ("never blocks", "non-blocking"); these describe an already-plannable, already-`READY` obligation, not an open blocker.

No line among the 17 reveals a second, independent, previously unidentified planning blocker. The candidate's **substantive conclusion** — no planning blocker exists outside §10.4 — is independently confirmed correct despite the inaccurate match count in its own evidence table. This inaccuracy is recorded as a defect in §17 (non-blocking: it is an evidence-precision error, not a wrong conclusion, and does not by itself put any planning content in doubt).

Independent review of §3–§9, §11–§14, §16, §18, §20–§21 of the original WPP (full text, this act) found no `BLOCKED`/`TBD`/open-decision language outside §10.4 and its two residual-register echoes. The `OPEN — IMPLEMENTATION-TIME` states for `MINOR-2` and `POSITION_CONVERSION_REBUILD_BOUNDARY` are ordinary, fully-planned, pre-use gates (§11 above), not planning blockers.

**Independently confirmed: no genuine planning blocker remains in the combined corpus (original WPP + candidate amendment).**

## 16. Implementation-determinism determination

Could a competent implementer now implement §10.4 without a new architectural, economic, numerical, authority, or classification decision? **Yes.** The formula, tolerance semantics, inclusivity, numeric policy, and annotation classification are all fixed by the design clarification (§6 above) with zero remaining discretion. The enforcement locus, consumer, and audit identity are fixed by the D7 amendment and Binding Freeze Record (§7 above) with zero remaining discretion. The canonical input contract is fixed by the existing parser (§8 above). The only choices left to an implementer are ordinary coding choices that do not alter governed behavior — e.g., the exact wiring point inside `_audit_portfolio()` for portfolios whose ledger contains a `POSITION_CONVERSION`, exact `AuditAnomaly.description` wording, and closing the §9 test-completeness gap identified above. None of these require a new governed decision.

## 17. Defects or concerns found

1. **Non-blocking accuracy defect:** candidate §16 reports "exactly seven matches" for its stated blocker-scan pattern; independent re-execution of the identical pattern against the live file returns 17 matches. The underlying substantive conclusion (no blocker outside §10.4) is independently reproduced and confirmed correct (§15 above); only the reported evidence count is wrong. Does not block reapproval.
2. **Non-blocking completeness observation:** acceptance rows `WP5-A21`–`WP5-A25` (`NOT_EVALUABLE` fixtures) do not individually require asserting the `CRITICAL`/exit-code-`2` severity mapping the way `WP5-A17` does; `WP5-A26` requires distinguishability but not an explicit severity assertion for the `NOT_EVALUABLE` family. §9's outcome table is itself unambiguous, so this leaves no implementation discretion, but the eventual test implementation should close this gap explicitly (§9 above). Does not block reapproval.

No other defect, semantic drift, scope expansion, or authority overreach was found.

## 18. Constitutional / authority review

The candidate relies only on already-bound authority (§3 above: exact identity continuity for the design clarification, reconciliation, D7 amendment, fresh reapproval, and Binding Freeze Record). It creates no new design semantics (§6), no new implementation authority beyond what the D7 Binding Freeze already bound (§7, §9), no new file authority (§7, §5), no production authority, no reconstruction authority, and no release/deployment authority (§17 of the candidate, independently confirmed unexercised by anything in this review). The D7 Binding Freeze Record remains the authority source; the candidate merely plans that authority's implementation into WPP form. This reapproval likewise creates no new authority beyond confirming the candidate's fidelity to what is already bound.

## 19. Important lifecycle question — what becomes permissible after this reapproval

Independently determined, not assumed from the WP4 precedent's shape:

The WP4 Retry-Order reapproval permitted immediate implementation reliance (`BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT_INDEPENDENT_REAPPROVAL.md` §11: "Implementation may now rely on the authoritative `E8-R`... under the existing bounded WP4 Implementation Authorization"). That permission was correct **for WP4** because WP4's Work Package Plan had already separately passed Planning Confirmation/Freeze earlier in WP4's own lifecycle — the retry-order amendment was a **mid-implementation** correction layered onto an already-operative Plan, not a first-time planning completion.

WP5 is not in that position. Independently confirmed this act (§2, condition 3): the original WP5 WPP has read `NOT CONFIRMED — NOT FROZEN` continuously since materialization, with §10.4 as the sole reason the WPP as a whole could not proceed to Planning Confirmation. The original WPP's own §22 (independently re-read, unchanged) names Planning Confirmation as the next act for the plannable majority, contingent on §10.4 being separately resolved — which this reapproval now completes.

Live repository precedent for **planning-stage** (pre-implementation) work packages is BANPU-WP2 and BANPU-WP3, not WP4:

- WP2: `BANPU_WP2_PLANNING_CONFIRMATION.md` → `BANPU_WP2_PLANNING_FREEZE_READINESS_ASSESSMENT.md` → `BANPU_WP2_PLANNING_FREEZE_RECORD.md` (disposition `PLANNING FROZEN WITH RECORDED OBSERVATIONS`) — only *after* that freeze does `BANPU_WP2_IMPLEMENTATION_AUTHORIZATION_RECORD.md` cite it as a satisfied precondition.
- WP3: `BANPU_WP3_PLANNING_FREEZE_RECORD.md` (disposition `BANPU-WP3 PLANNING COMPLETE, CONFIRMED, AND FROZEN`) is independently cited by `BANPU_WP3_ALLOCATION_RECORD.md` as the dispositive precondition for allocation.

No repository precedent creates a distinct "WPP Amendment Binding Freeze Record" artifact type for a Plan-amendment specifically — the WP4 chain's own Binding Freeze Record froze the **design-level governance decision** (a predecessor act), not the WPP amendment that later synchronized the Plan to it; the WPP amendment itself received only a Reapproval, no second freeze layer. WP5's D7 chain already followed the identical shape: the Binding Freeze Record froze the **D7 design/authority** (a predecessor act, completed before this review), and this WPP Amendment receives only a Reapproval — this review — with no separate "amendment Binding Freeze Record" required or appropriate.

**Determination:** the exact next constitutional act is **BANPU-WP5 Planning Confirmation** for the Work Package Plan as a whole (now that its sole blocker is planning-complete), to be followed by **BANPU-WP5 Planning Freeze**, exactly as the original WPP's own §22 and the candidate's own §21 anticipated. Only after Planning Freeze completes may implementation of the bounded §10.4 code/test surface (already `AUTHORIZED — BOUNDED` since the original Implementation Authorization Record) actually begin. This reapproval does not perform Planning Confirmation, does not perform Planning Freeze, and does not itself authorize implementation.

## 20. Prohibited acts — compliance confirmation

This act did not: modify the original WPP; modify the WPP Amendment; modify any D2–D7 authority artifact; implement WP5; modify application code; modify tests; create a WPP Amendment Binding Freeze Record; perform Planning Confirmation; perform Planning Freeze; close `MINOR-2`; execute reconstruction; mutate production data; perform WP6+ work; deploy; release; stage; commit; or push.

## 21. Repository verification

| Verification | Result |
|---|---|
| Added/modified paths this act | exactly one new file: `docs/implementation/BANPU_WP5_WORK_PACKAGE_PLAN_AMENDMENT_MECHANICAL_CONTINUITY_INDEPENDENT_REAPPROVAL.md` |
| Original WPP identity recomputed | `PASS` — `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523`; 42,903 bytes; 604 lines |
| Candidate amendment identity recomputed | `PASS` — `3ADAE8390462B8B93BCF19A3D8BF6182FB08D19D5860D97D4F8FE360851DFC4F`; 31,939 bytes; 268 lines |
| D2–D7 authority chain (5 artifacts) recomputed | `PASS` — all `EXACT`, §3 |
| Every reviewed input unchanged | `PASS` |
| Application/test code changed by this act | `NONE` |
| Prior governance artifact changed by this act | `NONE` |
| Staging/commit status | nothing staged |

Diff-check, whitespace, link/anchor verification, `graphify update .`, and final `git status` are executed after this file is written and reported in the final message.

## 22. Reapproval disposition

**BANPU-WP5 WORK PACKAGE PLAN AMENDMENT (MECHANICAL CONTINUITY) INDEPENDENTLY REAPPROVED.**

**THE COMPOSITE OPERATIONAL PLAN IS THE ORIGINAL WPP PLUS THE EXACT ADDITIVE AMENDMENT IDENTIFIED IN §3. FOR §10.4, §15, §17, §19, AND §22, THE REAPPROVED AMENDMENT CONTROLS WHERE THE HISTORICAL ORIGINAL WPP WAS SILENT OR BLOCKED; ALL OTHER ORIGINAL WPP SEMANTICS CONTINUE UNCHANGED.**

**COMBINED PLANNING CORPUS: NO REMAINING PLANNING BLOCKER (§15).**

**`MINOR-2` REMAINS `FULLY PLANNED — IMPLEMENTATION PENDING`, NOT CLOSED.**

**IMPLEMENTATION HAS NOT STARTED AND MAY NOT YET BEGIN.**

**THIS REVIEW IS NOT PLANNING CONFIRMATION AND IS NOT PLANNING FREEZE.**

## 23. Exact next constitutional act

**BANPU-WP5 Planning Confirmation**, for the Work Package Plan as a whole (original WPP + this reapproved amendment), now that its sole planning blocker is resolved (§19 above). Planning Freeze must follow as a separate, later act before implementation may begin. This record performs neither.
