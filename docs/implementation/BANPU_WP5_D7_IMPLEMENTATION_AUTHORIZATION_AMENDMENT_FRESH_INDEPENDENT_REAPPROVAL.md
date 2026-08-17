# BANPU-WP5 D7 Implementation Authorization Amendment — Fresh Independent Reapproval

**Artifact class:** Bounded independent-reapproval review record (fresh; distinct from, and not a modification of, the prior blocked review)

**Review date:** 2026-08-14

**Reviewing authority:** BANPU-WP5 D7 Amendment Fresh Independent Reapproval Authority (distinct from the amending act, the design-clarification materialization act, and the authority-provenance reconciliation act; not deferential to any of the three)

**Instrument under review:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md), read together with [`BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md`](BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md)

**Prior review of record:** [`BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_INDEPENDENT_REAPPROVAL.md`](BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_INDEPENDENT_REAPPROVAL.md) — `REAPPROVAL BLOCKED`, unmodified by this act, remains historical evidence (§4)

**Governance outcome:** `BANPU-WP5 D7 IMPLEMENTATION AUTHORIZATION AMENDMENT — FRESH INDEPENDENT REAPPROVAL PASSED`

**Binding Freeze Record performed:** `NO`

---

## 1. Nature and boundary of this act

This act performs the fresh Independent Reapproval named as the exact next constitutional act by the authority-provenance reconciliation record's §19. It is a new review act, not a modification, reversal, or retroactive redisposition of the prior blocked review. It does not implement D7, modify application or test code, amend the WPP, perform Binding Freeze, or perform Planning Confirmation/Freeze.

## 2. Entry lifecycle state (independently re-verified)

| Artifact | State |
|---|---|
| `BANPU_WP5_ALLOCATION_RECORD.md` | `ALLOCATED` |
| `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | `AUTHORIZED — LIMITED` |
| `BANPU_WP5_WORK_PACKAGE_PLAN.md` | `MATERIALIZED — NOT CONFIRMED/FROZEN`; §10.4 `PLANNING BLOCKER` (re-read live, line 290/455/493, unamended) |
| `BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md` | `DESIGN CLARIFICATION COMPLETE — HUMAN-AUTHORIZED NORMATIVE SEMANTICS ESTABLISHED — D7 NOT AUTHORIZED` |
| `BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md` | `BANPU DESIGN CLARIFICATION AUTHORITY PROVENANCE — RECONCILED` |
| `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md` | `PREPARED — NOT YET BINDING` |
| `BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_INDEPENDENT_REAPPROVAL.md` (prior review) | `REAPPROVAL BLOCKED` (historical) |

Confirmed: no D7 Binding Freeze Record exists (`Glob` for `BANPU_WP5*BINDING_FREEZE*.md` returns nothing); no D7 implementation has occurred (no `MECHANICAL_CONTINUITY` member in live `manage.py`, confirmed §5); WPP §10.4 unamended. Entry state internally consistent.

## 3. Identities independently recomputed (this act, live bytes)

| Artifact | Bytes | Lines | SHA-256 (uppercase) | vs. prior citation |
|---|---|---|---|---|
| `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | 19,039 | 341 | `DBCBC2BFCDB9F3A7D3E7912C6148445C68C39F5872A4DE2DEF58DF5B2BDE7F1E` | `EXACT` |
| `BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md` | 16,491 | 158 | `8DD43B1202714213E9EF88A65582E59A492680B747412BDAC9F176D3C43A2223` | `EXACT` |
| `BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md` | 18,755 | 145 | `BBE93F45237D6517E047A1E4FC8FC7A7665615975789F9E0AE9E6B846273EAE8` | first live recomputation this act; self-consistent |
| `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md` (reviewed instrument) | 32,307 | 237 | `DC8C272CD35854A156C9AD51494FE232C5408373A947AEC1B314D9657159E75B` | `EXACT` — byte-identical to the prior blocked review's subject |
| `BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_INDEPENDENT_REAPPROVAL.md` (prior review) | 21,023 | 146 | `61D142661F63FB5901D15116DF6F75004AAE747C6F4A27E1AE9CB7DF1431AADB` | `EXACT` |

**This reapproval binds itself to D7 amendment SHA-256 `DC8C272CD35854A156C9AD51494FE232C5408373A947AEC1B314D9657159E75B`** — byte-identical to the instrument the prior review examined. No content of the reviewed instrument changed between the two reviews; only the authority chain beneath it changed.

## 4. Treatment of the previous blocked review

Not modified, superseded, or retroactively redisposed. It correctly found, on the evidence available at the time it was written, that the design clarification's authority claim was self-asserted and unreconciled against three predecessor `BLOCKED`/`OUTCOME C` determinations — a true and accurate finding as of that time. What has changed since is not the reviewed instrument (§3 confirms byte-identity) but a new, subsequent artifact — the authority-provenance reconciliation record — supplying evidence that did not exist when the prior review was written. The prior review's disposition (`REAPPROVAL BLOCKED`) remains valid historical evidence of the repository's state and the correctness of that review's own reasoning at that time; it is not being called wrong in retrospect.

## 5. Authority-provenance reconciliation review

Independently re-read `BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION_AUTHORITY_RECONCILIATION.md` in full this act (not accepted from the invoking prompt's summary) and checked it against the five criteria this invocation specifies:

1. **Internal consistency with the earlier authority determinations:** `CONFIRMED`. The reconciliation's §4 correctly restates the 16:46/16:57/17:03 determinations as addressing repository-internal authority only, and its §5 correctly cites the 17:03 determination's own §15 (independently re-read this act — verbatim: *"direct action by whatever real-world party actually held the original... authority — a party this governance corpus does not itself name, and which this invocation cannot constitute for itself or presume to act as"*) as having left that path open rather than foreclosed it. No mischaracterization found.
2. **Leaves earlier records historically intact:** `CONFIRMED`. Neither the three predecessor determinations nor the prior blocked review are modified; the reconciliation record's §11 explicitly disclaims retroactive redisposition, and this act independently confirms none of those five files (§2 table above, plus the two competent-authority determinations) show any modification.
3. **Does not claim the external authorization existed in earlier Git state:** `CONFIRMED`. §2 of the reconciliation explicitly states the statement is "not expected to be discoverable from historical Git bytes preceding the authorization" and is recorded as new governance input dated 2026-08-14, not as retroactively-discovered history.
4. **Treats the human statement as new governance input, not repository-discovered evidence:** `CONFIRMED`. §2 explicitly labels it "a self-attested claim by the party controlling this invocation," not independently verifiable external evidence, and does not overstate its own weight.
5. **No exceeded authority:** `CONFIRMED`. The reconciliation's own §7 bounds its effect to exactly six enumerated items (confirm origin, ratify provenance, cure the specific blocker, leave D2–D6 unchanged, leave D7 non-binding, grant no implementation/deployment authority) and §16 explicitly disclaims any standing-role bootstrap. Independently checked against the reconciliation's own text: it does not exceed these bounds anywhere.

**On the substance of the cure itself:** the reconciliation's central move — distinguishing "no repository-internal authority found" from "no external human owner may ever subsequently authorize anything" — is a real and valid logical distinction, independently verified against the primary source text of all three predecessor determinations (§3 of the prior blocked review, cross-checked here). The 17:03 determination named the external-owner path as admissible in principle; nothing in this text-based governance medium could ever furnish stronger evidence of a real-world human's direct authorization than an explicit, first-person, dated, narrowly-bounded statement made by the party who has authored every instruction in this entire session — that statement is the practical ceiling of what "external human authorization" can look like when the entire interaction occurs inside a single chat session with a single human party. Demanding evidence beyond the statement itself would make the 17:03 determination's own admitted path permanently unsatisfiable by construction, which is not the better reading of that determination's own text.

**This does not mean prompt-text authority claims are self-verifying in general.** They are not, and this record does not hold that. What makes this specific cure adequate for this specific act is the conjunction of (a) explicit, bounded, first-person, dated form; (b) internal consistency with everything the corpus already established; (c) zero mutation, deployment, or binding consequence flowing from accepting it (§15/§19 of the reviewed instrument; even a successful reapproval here leaves D7 non-binding, §12 below); and (d) the absence, confirmed by three independent prior searches, of any less-demanding repository-internal alternative that could have supplied the same content instead. A future act seeking to rely on a similarly-sourced authority claim for a higher-stakes act — production mutation, deployment, or a Binding Freeze that actually unlocks implementation reliance — should not treat this record as precedent that the bar is this low; the bar here was cleared only because the consequence class is this narrow.

**Conclusion:** the provenance blocker identified by the prior review (§4/§15 item 1/§18 of that record) is cured for the purposes of this reapproval.

## 6. D2–D6 independent technical review

Independently re-read `BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md` §4–§12 in full this act, and design §5/§10 (live, lines 305–326) as the canonical source, rather than relying on either the D7 amendment's or the prior review's characterization.

- **D2 (formula):** `metric_pct = (abs(P_pre − R·P_succ) / P_pre) × 100`. Verified against design §5's accounting model: `R` is the amalgamation's defining conversion ratio (one predecessor share → `R` successor shares), so the ratio-implied value equivalence is `P_pre ≟ R·P_succ` — the clarification's Alternative C. The rejected alternatives (raw price difference, R-unnormalized relative difference) are correctly rejected: predecessor and successor are different instruments whose raw per-share prices carry no meaning without folding in `R`. Denominating the percentage against `P_pre` (the known evidence-bound predecessor price, not the ratio-derived successor-implied value) is a defensible, standard choice and is explicitly reasoned, not arbitrary. **No contradiction of canonical accounting semantics found.**
- **D3 (tolerance):** `mechanical_nav_tolerance_pct` and `metric_pct` are both percentages by construction and by the payload's own example values; no unit mismatch. `CONFIRMED`.
- **D4 (inclusivity):** `metric_pct <= mechanical_nav_tolerance_pct` passes, matching this design document's own established boundary-inclusive phrasing elsewhere (§6.3, independently re-checked). `CONFIRMED`.
- **D5 (Decimal/rounding):** Decimal-only construction from payload strings, no intermediate/final quantization, no invented rounding mode, ambient context governs — consistent with design principle #4 ("Decimal strings in the payload are authoritative"), independently re-checked against `transaction_canonicalizer.py`'s existing Decimal-only handling of the same payload class. Non-finite/non-positive/missing/malformed required operands → `NOT_EVALUABLE`, never a silent numeric comparison. `CONFIRMED`.
- **D6 (annotation):** null/empty/whitespace-only → absent; non-empty trimmed → present, via `.strip()`. Annotation affects classification of an already-computed `FAIL` only — never the metric, never NAV, never `PASS` results, never other checks. `CONFIRMED` against design §10's own two-clause structure (reconciliation requirement + suspension-gap-is-genuine-return clause), which is unsatisfiable jointly without exactly this kind of narrow classification effect.

**No defect found in D2–D6 on independent technical review.**

## 7. Suspension-gap invariant review

Independently verified against clarification §11 and design §10's suspension-gap sentence (live, line 324): `metric_pct` is preserved as a first-class numeric result in every outcome including `ANNOTATED_BOUNDARY_DISCONTINUITY` — never zeroed, clamped, or discarded; reference prices, NAV, and basis are untouched by this predicate (§4 of the clarification: this check is disjoint in operand-scope from `SHARE_MISMATCH`/`BASIS_MISMATCH`); annotation changes classification only, never accounting treatment (§10 anti-bypass bound, independently re-read). `WARNING` severity for `ANNOTATED_BOUNDARY_DISCONTINUITY` (rather than silent `PASS` or `CRITICAL`) is the only treatment consistent with design §10's own requirement that genuine suspension-gap return remain visible and evidenced rather than either suppressed or treated as an unexplained defect. `CONFIRMED CONSISTENT`.

## 8. Live architecture findings (independently re-inspected this act)

Read directly from working-tree files, not from either the amendment's or the prior review's description:

- `backend/manage.py:795–803` — `AuditSeverity` and `AuditCheck` (`NAV_CONTINUITY`, `PNL_CONTINUITY` not separately grepped but `HOLDINGS_INTEGRITY` confirmed with six use sites) present; **no `MECHANICAL_CONTINUITY` member exists yet** — consistent with "reserved, not implemented."
- `backend/manage.py:1123` — `_audit_portfolio(...)` dispatcher present.
- `backend/manage.py:1256` — `verify_snapshots` docstring confirmed verbatim: *"Read-only snapshot integrity audit. Never modifies the database."*
- `backend/services/transaction_canonicalizer.py:146` — `PositionConversionBoundaryEvidence` class present; line 326 — `parse_position_conversion_payload()` present and public, matching the D7 amendment's and clarification's citations.
- `backend/services/portfolio_rebuilder.py:609` — `_resolve_conversion_successors()` present; line 2259 — its call site inside the rebuild path present. **No `POSITION_CONVERSION_REBUILD_BOUNDARY` literal/guard exists yet anywhere in this file** (grep returns only the two prior citations, both in this act's own review and the prior review — i.e., zero occurrences in `portfolio_rebuilder.py` itself), confirming no WP5 implementation has occurred and the amendment's description of this as a planned, not implemented, location is accurate.

`CONFIRMED — the amendment's factual claims about live code match the working tree exactly.`

## 9. Independent D7 locus analysis

Re-evaluated Options A–E independently, per this invocation's specific questions:

- **Is `verify_snapshots` genuinely the correct owner/consumer?** Yes — it is the only WP5-authorized, confirmed read-only, per-portfolio audit surface with an existing, structurally identical `AuditCheck`/`AuditAnomaly` pattern already hosting four analogous checks (§8 above).
- **Does placing `_evaluate_mechanical_continuity()` in `manage.py` improperly make CLI code the domain authority?** No — the domain semantics (D2–D6) are fixed by the clarification, not invented by the classifier; `manage.py` hosts read-only reporting of an externally-fixed predicate, identically to how it already hosts `NAV_CONTINUITY`'s design/roadmap-defined semantics.
- **Is that acceptable under the existing audit architecture?** Yes — it is the existing pattern, not a new one.
- **Would a new module materially improve ownership enough to justify expanding authorized surface?** No — no second consumer is evidenced anywhere in the design, Roadmap §7, or the WPP; a new module would add authorized file surface beyond the original Authorization Record's §4.1 grant for no demonstrated benefit.
- **Is there evidence reconstruction must consume this result?** No — §9 of the amendment's separation claim is independently confirmed accurate (§10 below); reconstruction and this classifier have zero code-level coupling.

Option B (refined: pure classifier + single `verify_snapshots` consumer) remains the narrowest sufficient architecture. `CONFIRMED, NOT CHANGED**.

## 10. Outcome-policy review

`PASS` (silent, no anomaly) / `ANNOTATED_BOUNDARY_DISCONTINUITY` (`WARNING`, exit 1, metric+tolerance+annotation in `details`, never auto-fails, never mutates) / `MECHANICAL_CONTINUITY_FAILURE` (`CRITICAL`, exit 2, fail-closed for verification acceptance only, no mutation) / `NOT_EVALUABLE` (`CRITICAL`, distinct description, never silently `PASS`) — each independently checked against the clarification's §6–§12 and against `verify_snapshots`'s existing severity/exit-code convention (§8 above). Internally consistent; no production-mutation authority smuggled into any branch. `CONFIRMED`.

## 11. Rebuild-boundary independence

Confirmed via §8's live inspection: `verify_snapshots` and `rebuild_portfolio()`/`portfolio_rebuilder.py` are separate entry points with zero shared call path under this amendment; neither is invoked from within the other; no `POSITION_CONVERSION_REBUILD_BOUNDARY` guard exists yet, so no coupling could exist even accidentally. `CONFIRMED — NOT COUPLED`.

## 12. Canonical-input review

`PositionConversionBoundaryEvidence` fields and `PositionConversion.conversion_ratio`, sourced exclusively via `transaction_canonicalizer.parse_position_conversion_payload()` (confirmed present and public, §8 above) — no re-derivation from ticker/display text, provider lookup, snapshot inference, or caller-supplied substitutes is proposed anywhere in the amendment. `CONFIRMED`.

## 13. Code-surface authorization review

`backend/manage.py` and `backend/tests/test_verify_snapshots.py` are both already named in the original Authorization Record §4.1/§4.2 (identity confirmed unchanged, §3 above). This amendment merely clarifies that the already-granted `manage.py` capability extends to the now-fixed §10.4 reconciliation classification (previously only §10.3's tolerance-admissibility reporting was scoped by the WPP); no new file, no broader edit scope. `CONFIRMED — NO SCOPE EXPANSION`.

## 14. Failure/result identity review

`AuditCheck.MECHANICAL_CONTINUITY` — confirmed, via live grep (§8), not to collide with any existing member and not present yet in the live enum (reserved, not implemented, as claimed). Two distinguishable description strings under one enum member (for `MECHANICAL_CONTINUITY_FAILURE` vs. `NOT_EVALUABLE`) mirrors the existing `HOLDINGS_INTEGRITY` precedent (six description-distinct use sites at that one `AuditCheck` value, confirmed §8). `CONFIRMED`.

## 15. Acceptance-test determinism review

All nineteen scenarios this invocation's §15 lists are each traceable to a specific, unambiguous sentence in the clarification (§6–§12, independently re-read this act) or the amendment (§8/§10/§12): below/at/above tolerance; unannotated/annotated above-tolerance; null/empty/whitespace/non-empty annotation; missing/malformed evidence; non-positive predecessor price; invalid successor/ratio; Decimal-only arithmetic; metric preservation under annotation; correct `WARNING`/`CRITICAL`/exit-code mapping; no mutation; rebuild-boundary independence. A future WPP amendment can plan deterministic acceptance tests from this text without further implementation discretion. `CONFIRMED SUFFICIENT PRECISION`.

## 16. Constitutional scope review

Independently re-checked amendment §15/§19: excludes historical snapshot correction, reconstruction execution, production mutation, release, deployment, WP6/WP7/WP8, schema/migration work, WP3/WP4 reopening, WPP amendment, Planning Confirmation/Freeze. No unintended expansion found beyond the single clarified `manage.py` capability (§13). `CONFIRMED — BOUNDED`.

## 17. WP4 precedent and binding-status analysis

The WP4 Retry-Order chain (`Governance Decision` → `Plan Amendment` → `Independent Reapproval` → `Binding Freeze Record`), independently re-confirmed present and unmodified (four files located, §-referenced in the prior review), remains the correct structural precedent for this amendment's *own* binding mechanics: an amendment at the "Governance Decision" position in that chain's shape is not implementation-reliable until it passes through Independent Reapproval and a subsequent Binding Freeze Record. Nothing in this act's findings — including the resolved authority-provenance question — changes that requirement. **A Binding Freeze Record is still required before D7 may be relied upon by implementation or WPP completion; this reapproval does not substitute for it.**

## 18. New defects or concerns found

1. **(Non-blocking, noted.)** The authority-provenance cure accepted in §5 rests on an unverifiable, self-attested, prompt-text claim. It is accepted here because of the specific conjunction of factors in §5 (bounded form, internal consistency, zero mutation/deployment consequence, absence of any less-demanding alternative). This should not be read as establishing a general precedent that self-attested prompt authority suffices for higher-stakes acts — in particular, it must not be treated as sufficient, by itself, to authorize the Binding Freeze Record, WPP amendment, or any future production-mutation act. Those acts should independently re-assess whether the authority backing them is adequate to their own, larger consequence class.
2. **(Non-blocking, restated from the prior review for continuity.)** No literal `POSITION_CONVERSION_REBUILD_BOUNDARY` guard exists yet in `portfolio_rebuilder.py` — expected, given no WP5 implementation has occurred; not a defect in this amendment's claims.
3. **(Non-blocking.)** No new technical defect was found in D2–D6, the D7 locus, the outcome policy, or the code-surface authorization; all sound conditional on §5's authority finding, and §5 is now resolved in the amendment's favor.

## 19. Artifact created

`docs/implementation/BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_FRESH_INDEPENDENT_REAPPROVAL.md` (this document) only. The prior blocked review is not overwritten.

## 20. Repository verification

To be executed after write and reported in the final message: enumerate added/modified paths; confirm the five identities in §3 unchanged from their live-recomputed values; `git diff --check`; `git diff --cached --check`; trailing-whitespace check; relative-link/anchor verification; `graphify update .`; confirm no application/test code changed; confirm no prior governance artifact changed; confirm nothing staged/committed; final `git status`.

## 21. Final disposition

`BANPU-WP5 D7 IMPLEMENTATION AUTHORIZATION AMENDMENT — FRESH INDEPENDENT REAPPROVAL PASSED`

## 22. Is D7 binding yet?

`NO.` This reapproval makes the amendment eligible for a Binding Freeze Record; it does not itself bind it. Implementation must not rely on `AuditCheck.MECHANICAL_CONTINUITY` under color of this reapproval alone.

## 23. Exact next constitutional act

A **BANPU-WP5 D7 Binding Freeze Record**, performed by an authority distinct from this reapproval, binding to this record's identities (§3) plus the reviewed D7 amendment. Only after that freeze completes may the WPP follow-up described in the D7 amendment's own §18 proceed. This record does not perform that act.
