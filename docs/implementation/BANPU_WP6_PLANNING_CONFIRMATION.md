# BANPU-WP6 — Planning Confirmation

**Artifact class:** BANPU-WP6 planning confirmation record
**Confirmation date:** 2026-08-18
**Independent confirming authority:** BANPU-WP6 Planning Confirmation Authority (distinct from the BANPU-WP6 Work Package Planning Authority that materialized the plan and from the authority that performed the WPP's idempotency amendment)
**Confirmation boundary:** `PLANNING CONFIRMATION ONLY — NOT PLANNING FREEZE — NOT IMPLEMENTATION AUTHORIZATION`
**Freeze performed:** `NO`
**Implementation authority granted by this act:** `NONE`
**Former ambiguity #14 resolution status:** confirmed operative by this act, not re-decided by it

---

## 1. Purpose and review boundary

This record independently reviews the complete, current, amended BANPU-WP6 Work Package Plan and determines whether it is sufficiently complete, internally consistent, subordinate to controlling authority, bounded to authorized scope, mechanically determinate, testable, and free of implementation-critical planning ambiguity to receive Planning Confirmation. It performs no implementation, no Planning Freeze, no amendment, and no residual discharge. Confirmation is not granted merely because former ambiguity #14 was resolved by the prior amendment act — the whole plan was reviewed.

## 2. Confirmation standard applied

Derived from live re-reading of `BANPU_WP5_PLANNING_CONFIRMATION.md` (325 lines), the closest valid standalone Planning Confirmation precedent in the repository. That record establishes, and this record applies without strengthening or weakening:

- the exact planning corpus is identified and hashed from live bytes;
- prior amendment/interpretation content is cross-checked against current corpus content, not merely counted as resolved;
- non-blocking observations may be recorded without being treated as resolved;
- the confirmed corpus is **not** frozen and grants **no** implementation authority;
- a distinct, later Planning Freeze act remains required before implementation; and
- an exact next constitutional act is named.

WP5's precedent also establishes a specific sub-standard this record relies on directly (§7 below): a "confirm-or-implement" contingency inside a Work Package Plan — where implementation must verify a preliminary finding and, if a narrow defect is found, fix it within an already-authorized file surface — "does not leave open discretion over outcome, only over whether a source edit is needed, which is a normal implementation-time finding, not a governed decision" (`BANPU_WP5_PLANNING_CONFIRMATION.md` §11, independently re-read this act). This record applies that exact sub-standard to WP6's identical pattern in WPP §7.4/§8 item 12.

## 3. Exact WPP identity reviewed

| Artifact | Bytes | Lines | SHA-256 (recomputed live) |
|---|---:|---:|---|
| `BANPU_WP6_WORK_PACKAGE_PLAN.md` | 53,844 | 725 | `1cc7f17c916639dad08507aef5875ea72a60d028d0573e7ceafa1b57d766601a` |

Single-document corpus — the WPP as amended (§14.2 of that document), not a separate amendment file. No other WP6 planning artifact exists.

## 4. Entry-state verification

Independently recomputed live, immediately before review:

| # | Item | Result |
|---|---|---|
| 1 | `BANPU_WP6_ALLOCATION_RECORD.md` present, `BANPU-WP6 ALLOCATED`, 16,307 bytes / 282 lines / SHA-256 `208c2b236d669141bc947a96d82c5c249535e95eb54483c25496c1b6908d9d58` | `CONFIRMED` |
| 2 | `BANPU_WP6_IMPLEMENTATION_AUTHORIZATION_RECORD.md` present, `BANPU-WP6 IMPLEMENTATION AUTHORIZED`, 18,660 bytes / 323 lines / SHA-256 `442426729c8d7582961cb0ba3b7706356995a39333662042c5bea260b95bfd0f` | `CONFIRMED` |
| 3 | WPP present, maturity `MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN`, 53,844 bytes / 725 lines / SHA-256 `1cc7f17c9...` (§3) | `CONFIRMED` |
| 4 | WPP contains the completed amendment resolving former ambiguity #14 (§14.2, §8 item 14, §7.2, §9, §10, §13, §15) | `CONFIRMED` — live-read in full this act |
| 5 | WPP records Contract B required, Contract A subsumed, Contract C not required | `CONFIRMED` — §7.2 and §8 item 14, live-read |
| 6 | No `WP6-BLOCKED` acceptance criterion remains active | `CONFIRMED` — §10 grep, zero live matches as an active row; the string appears only in §14.2's historical amendment-record table |
| 7 | No implementation-critical ambiguity remains open in §8's table | `CONFIRMED` — see §6 below |
| 8 | Acceptance matrix contains `WP6-A1`–`WP6-A18`, none marked `PASS` | `CONFIRMED` — all 18 rows read, status column reads "Not evaluated" throughout |
| 9 | No WP6 Planning Confirmation artifact already exists | `CONFIRMED ABSENT` before this act's write |
| 10 | No WP6 Planning Freeze artifact exists | `CONFIRMED ABSENT` |
| 11 | No WP6 implementation has started | `CONFIRMED` — `backend/services/position_conversion.py` and `backend/tests/test_position_conversion.py` both absent |
| 12 | No production/test/schema/migration/CLI/frontend file modified for WP6 | `CONFIRMED` — `git status --porcelain=v1` shows only the three untracked WP6 governance docs |
| 13 | Allocation/Authorization Records unchanged from the identities the WPP relies on | `CONFIRMED` — hashes in row 1/2 match the WPP's own header citations exactly |
| 14 | Nothing staged | `CONFIRMED` — `git diff --cached --name-only` empty |

All fourteen premises match. No fail-closed condition exists. Review proceeds.

## 5. Independent review corpus

Live-read or live-grepped this act, not accepted from the WPP's own citations:

- `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` — §12 (line 358, 360) and §13 (lines 362–371) re-read verbatim.
- `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md` §8 (lines 374–439) re-read in full.
- `BANPU_IMPLEMENTATION_SEQUENCE.md` §8 / Step 6 (lines 230–262) re-read in full.
- `BANPU_WP6_ALLOCATION_RECORD.md`, `BANPU_WP6_IMPLEMENTATION_AUTHORIZATION_RECORD.md` — identity and scope re-confirmed (§4).
- `backend/models/asset.py` line 122 (`effective_date` column).
- `backend/services/asset_registry.py` lines 376–392 (`WP4-IIR-B3` guard).
- `backend/services/portfolio_rebuilder.py` line 41 (Stage 9 idempotency docstring).
- `backend/services/decision_memory/shadow_tracker.py` — function locations (lines 1148, 1463, 1707), the `.delete()` call (line 1407), and upsert language (lines 1157, 1720, 1725).
- `backend/services/evaluation/horizon_grader.py` lines 63–126 (`score_directional_calls`, full body).
- `backend/services/analytics/quant_engine.py` lines 640–736 (`calculate_buy_win_rate`, `calculate_sell_accuracy`, full body).
- `backend/services/evaluation/ideal_series.py` line 345 (`_revalue_ai_portfolio_with_canonical_prices` presence).
- `backend/services/decision_memory/attribution.py` lines 49, 62 (`_portfolio_sector_return`, `compute_attribution` presence).
- `BANPU_WP5_PLANNING_CONFIRMATION.md` (full, 235 lines) — structural and burden-of-review precedent.

## 6. Scope-conformance review

Roadmap §8 "Scope" (six bullets, lines 382–387) matches WPP §4's six capabilities `WP6-C1`–`WP6-C6` one-for-one; no seventh capability appears anywhere in the WPP. Roadmap §8 "Files expected to change" (lines 389–397) matches WPP §5.1/§5.2 exactly, including the conditional narrow `position_conversion.py`. Roadmap §8 "Explicit files NOT to change" (lines 399–405) matches WPP §12's exclusion list exactly (schema/model changes, `RecommendationSnapshot`/`OptimizerHistory`/`UserExecutionDecision`/`RecommendationGrade`, transaction write path, general asset-definition vocabulary, all M46 files). No planned production file, test file, or task in §13 references any path outside §5.1/§5.2.

**Result: `CONFORMS`.**

## 7. Mechanical-determinacy review

Each classification in WPP §8 independently re-checked against live source rather than accepted:

| # | Item | Live-source finding | Determination |
|---|---|---|---|
| 1 | Uses `AssetRelationship.effective_date` | Column exists, nullable `DateTime` (`asset.py:122`) | `SUPPORTED` |
| 2 | Boundary inclusivity `>=` | No controlling text states inclusivity directly; WPP's structural analogy to WP5's accepted `from_date >=` convention is the same technique WP5's own Planning Confirmation validated for an equivalent gap (§9 of that record) | `SUPPORTED` |
| 3 | Single-hop succession only | `WP4-IIR-B3` guard (`asset_registry.py:384-392`) confirmed to fail-close a predecessor asset acquiring a second outgoing `MERGED_INTO` edge — the registry invariant WPP cites as the basis for well-defined single-hop resolution is real, not asserted | `SUPPORTED` |
| 4 | Unset `effective_date` never resolves a successor | Fail-closed default; no controlling text contradicts it | `SUPPORTED` |
| 5–8 | Fractional-share arithmetic, no cash-in-lieu, immutable evidence, pre-boundary write protection | Design §12 verbatim (line 358, 360), re-read and matches WPP's quotations exactly, character for character | `SUPPORTED` |
| 9 | Per-row boundary evaluation | Direct structural analogy to `portfolio_rebuilder.py`'s own per-date filtering, already accepted at WP5 Planning Confirmation (§9 of that record) | `SUPPORTED` |
| 10 | Canonical-symbol resolution reuses `asset_repository.get_asset_by_canonical_symbol()` | Not independently re-derived from source this act beyond confirming no second resolver was found in the reviewed surface; consistent with WP4/WP5's own resolver usage | `SUPPORTED` |
| 11 | `horizon_grader.py` cross-identity defect | `score_directional_calls` (lines 63–126) independently re-read in full: `inception_holdings` keyed by frozen symbol (line 98), matched against `horizon_holdings` built from `horizon_holdings_json` (lines 88–90) by exact string key (line 103); a converted holding's frozen predecessor symbol will not match a post-boundary snapshot keyed by the successor symbol once WPP §7.2 lands, and the mismatch falls silently into the existing `continue` branch (lines 105–106), not an error. The docstring's own "Pure function — no DB access" (line 69–70) is independently confirmed to be the exact contract WPP §7.3 flags as needing to change. This is a real, verified defect site, not a hypothetical one | `SUPPORTED` |
| 12 | `quant_engine.py`/`ideal_series.py`/`attribution.py` confirm-or-implement, labeled `MECHANICALLY DERIVABLE, PENDING IMPLEMENTATION-TIME CONFIRMATION` | `calculate_buy_win_rate`/`calculate_sell_accuracy` (lines 640–736) independently read in full: win/loss determination uses `_snap_value_map`/`_value_at_or_after` against aggregate portfolio-level snapshot values; `sig.symbol` appears only inside the returned `details` list as a display field, never as a lookup key. This directly confirms WPP §7.4's preliminary finding of "no source change required" for this file. `_revalue_ai_portfolio_with_canonical_prices` (`ideal_series.py:345`) and `_portfolio_sector_return`/`compute_attribution` (`attribution.py:49,62`) confirmed present at the cited locations; their preliminary "likely inherits correctness, to be confirmed" findings are not independently re-derived line-by-line by this act, but the pattern itself — a binary, already-bounded confirm-or-implement contingency inside the already-authorized §5.1 file surface, with no policy fork and no new architecture on either branch — is the identical pattern WP5's own Planning Confirmation (§11 of that record) already validated as "a normal implementation-time finding, not a governed decision." Applying that precedent directly: this is not a planning-critical ambiguity disguised as implementation-time confirmation | `SUPPORTED — NOT A CONFIRMATION BLOCKER` |
| 13 | Direct read of `PortfolioItem.asset_id` without M29/M30 capability-safety routing | WP5's own accepted, frozen WPP already read this exact column directly with no gate invoked; no BANPU governance artifact references the M29/M30 track. Not independently re-derived further this act beyond confirming the WP5 precedent claim is consistent with this act's own review of `BANPU_WP5_PLANNING_CONFIRMATION.md`, which raises no M29/M30 objection anywhere in its own review | `SUPPORTED` |
| 14 | Idempotent rerun (Contract B required, Contract C not required) | Reviewed independently in §8 below | `SUPPORTED` |

No item requires implementation to choose between multiple materially different behaviors that authority leaves open. Item 12 is the closest candidate for such a fork and is resolved by direct, on-point WP5 precedent, not by mere labeling.

**Result: `SUPPORTED IN FULL`.**

## 8. Idempotency-amendment review

Independently re-derived, not accepted from the amendment's own assertion:

- Design §13 step 6 (line 369, re-read verbatim): *"Rebuild portfolio and shadow rows only from the transition date."* This is the only place in the controlling corpus that names "shadow rows" as a rebuild target, and it appears inside the same enumerated step whose immediately following closing sentence (line 371) reads: *"The manifest, registry preparation, conversion insertion, cache purge, and rebuild commands MUST be safe to repeat."* The word "rebuild" in the closing sentence has no antecedent other than step 6's own definition two lines above it, which explicitly includes shadow rows. Read in isolation from the WPP's own reasoning, this act reaches the identical textual conclusion: "rebuild commands... safe to repeat" governs WP6's shadow regeneration, not only WP4's registry-level acts.
- Roadmap §8 (WP6's own section) contains no rebuild or idempotency language of its own — confirmed by full re-read (lines 374–439) — so §13's cross-cutting clause is the only controlling text reaching WP6's rerun behavior at all.
- `portfolio_rebuilder.py` line 41 (re-read verbatim): *"Stage 9 — Idempotency (upsert pattern; running twice = same state)."* This is WP5's own frozen, accepted realization of the identical §13 closing-sentence clause for its sibling half (portfolio rows). It demonstrates persistence-state convergence via upsert, not byte-identical/zero-write rerun. No other realized precedent for this clause exists anywhere in the accepted corpus.
- No controlling artifact (design, Roadmap §8, Sequence Step 6 — independently re-read, lines 230–262, confirmed to contain no idempotency language at all) states or implies a byte-identical/zero-mutation requirement.

This independently reproduces, rather than merely accepts, the WPP's Contract B/A/C disposition: **Contract B (persistence-state idempotency) required; Contract A (semantic determinism) necessarily included within B; Contract C (byte-identical/zero-write rerun) not required.**

`regenerate_static_shadow`'s `.delete()` call (`shadow_tracker.py:1407`, independently re-read) is a real, verified structural difference from the other two regeneration functions' upsert pattern (`_rebuild_shadow_snapshots` line 1157, `regenerate_active_model_shadow` line 1720/1725, both independently re-read and confirmed to document upsert). The WPP's treatment of this as an implementation-time compliance point — not a planning blocker, not authority to redesign — is correct: Contract B's *requirement* is already fixed by controlling authority (this section, above); what remains is whether `regenerate_static_shadow`'s specific delete-then-recreate mechanism, combined with the pre-boundary guard WPP §7.2 already specifies, in fact converges to the same persisted state on rerun. That is a question of whether a fixed requirement is met by particular code, not a question of what the requirement is — an implementation-and-test question, not an open planning fork.

**Result: `CORRECTLY DERIVED FROM CONTROLLING AUTHORITY; NOT MERELY ASSERTED`.**

## 9. Implementation-decomposition review

WPP §6–§7 reviewed against §5's authorized file surface and §8's determinacy table:

- The narrow succession-lookup mechanism (§7.1) is legitimately necessary rather than speculative: design §12's single sentence names five independent consumers of the identical effective-dated lookup (quant, attribution, shadow, horizon grading, ideal-series), and building it once is the only reading consistent with "narrow" (the word both the Allocation and Authorization Records use) and with avoiding five duplicated implementations of the same registry composition.
- Shadow holdings JSON (§7.2) is correctly identified as the capability-dense center: four of six capabilities (`WP6-C2`, `WP6-C3`, `WP6-C4`, `WP6-C6`) are decomposed there, and `shadow_tracker.py` is independently confirmed to be the only module that constructs `inception_holdings_json`/`ShadowPortfolioSnapshot.holdings_json`.
- The horizon-grader defect (§7.3) is real, independently verified in §7 item 11 above, not hypothetical.
- The `attribution.py`/`quant_engine.py`/`ideal_series.py` confirm-or-implement treatment (§7.4) is sufficiently bounded, independently verified in §7 item 12 above.
- §13's task table is test-first throughout (T2 before T3, T4/T6 before T5/T7, T9 after T8) and every task references only files within §5.1/§5.2. No task requires authority the Authorization Record does not already grant.

**Result: `SOUND`.**

## 10. Acceptance-matrix review

All eighteen rows (`WP6-A1`–`WP6-A18`) independently re-read: each traces to a named governing source (design §12/§13, Roadmap §8, Authorization §7/§10, or a stated mechanical derivation), each names a concrete test/evidence surface within the authorized §5.2 test list, and each is testable in principle from the mechanics §7 already fixes. `WP6-A14` (the amended rerun-convergence criterion) is independently confirmed to assert persistence-state convergence of business fields, absence of compounding/duplicate/orphan rows, and preservation of `WP6-A13`'s pre-boundary protection — it does not assert byte-identical rerun, no unchanged timestamp, and no zero-write requirement anywhere in its text. It does not accidentally impose Contract C. Every status cell reads "Not evaluated"; none reads "PASS."

**Result: `SOUND — NO CONTRACT-C DRIFT`.**

## 11. Residual and exclusion review

WPP §9 independently re-read: `MINOR-2` and `POSITION_CONVERSION_REBUILD_BOUNDARY` both carry `NOT WP6-OWNED — CARRIED FORWARD UNCHANGED, NOT PLANNED, NOT DISCHARGED`, matching the header block's own disposition lines exactly. `PD-3` is stated as unassigned and not claimed by WP6. All WP1–WP4 residual/observation rows are restated without alteration. The removal of "Ambiguity #14" from §9's table is independently confirmed to be a removal-as-no-longer-an-open-item, not a residual discharge — no residual disposition value differs from its pre-amendment text.

WPP §12 independently re-read against Roadmap §8's exclusion list (§6 above): no schema/model/migration change, no transaction write-path change, no touching of WP3/WP4/WP5's frozen surfaces, no rewriting of historical recommendation/decision payloads, no general corporate-action framework, no unrelated-symbol remapping, no endpoint/CLI/frontend work, no production regeneration, no release/deployment claim, no M46 modification, no WP7+ act — all explicitly listed as prohibited in §12, none appears anywhere else in the document as something actually planned.

**Result: `NO RESIDUAL CLAIMED; NO UNAUTHORIZED SURFACE`.**

## 12. Blockers

**None.**

## 13. Non-blocking observations

1. WPP §7.3 records, without resolving, a genuine implementation-time contract choice (keep `score_directional_calls` DB-touching via a single §7.1 read, or have its caller pre-resolve the translated symbol map to preserve purity). This is correctly left to implementation as an ordinary local coding choice — the WPP does not claim it has already been decided, and no controlling authority mandates one form over the other.
2. `MECHANICALLY DERIVABLE` item 10 (canonical-symbol resolution reusing `asset_repository.get_asset_by_canonical_symbol()`) and item 13 (M29/M30 non-gating) were reviewed at lower independent depth than items 1–9, 11, 12, and 14, consistent with the review corpus in §5 — both are corroborated by direct WP4/WP5 precedent already re-confirmed during this act's review of `BANPU_WP5_PLANNING_CONFIRMATION.md`, and neither raises a live contradiction anywhere in the reviewed corpus. Neither rises to a blocker.

Neither observation withholds confirmation.

## 14. Confirmation disposition

**`BANPU-WP6 PLANNING CONFIRMED`**

The complete, current, amended BANPU-WP6 Work Package Plan is complete, internally consistent, subordinate to controlling authority, bounded to its authorized six-capability/named-file scope, mechanically determinate (including the amended idempotency determination, independently re-derived rather than merely accepted), testable against an explicit and Contract-C-clean eighteen-row acceptance matrix, protective of frozen WP3/WP4/WP5 surfaces and immutable historical evidence, and free of any implementation-critical planning ambiguity requiring deferral. Confirmation does not freeze the plan and grants no implementation authority.

## 15. Artifact created

This file: `docs/implementation/BANPU_WP6_PLANNING_CONFIRMATION.md`. The WPP itself was not modified by this act.

## 16. Resulting WP6 constitutional state

- Allocation: `COMPLETE — ALLOCATED`
- Implementation authority: `AUTHORIZED — BOUNDED`
- Implementation: `AUTHORIZED / NOT STARTED`
- Work Package Plan: `MATERIALIZED — AMENDED (§14.2) — PLANNING CONFIRMED — NOT FROZEN`
- Release/deployment/production-mutation authority: `NONE`
- BANPU-WP7+: `NOT ALLOCATED / NOT AUTHORIZED`

## 17. Exact next constitutional act

**BANPU-WP6 Planning Freeze**, over the exact WPP identity confirmed in §3 (53,844 bytes / 725 lines / SHA-256 `1cc7f17c916639dad08507aef5875ea72a60d028d0573e7ceafa1b57d766601a`), performed by an authority distinct from this confirming authority, following the same structure `BANPU_WP5_PLANNING_FREEZE_RECORD.md` used for WP5.

**This record performs no part of that act.**
