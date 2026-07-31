# M44-WP3 — Independent Constitutional Review Report
## 1. Review identity and independence statement
Acting as independent constitutional reviewer of M44_WP3_PERIOD_RETURN_OWNERSHIP_GOVERNANCE_CORRECTION.md at status RC1. I did not author the artifact or any of its normative rows, and I am not its advocate. This review is read-only: no repository file was created, modified, or staged. No confirmation is issued here, and no freeze is performed. Independence satisfies frozen M44 Architecture §§12.4 and 16.4.

## 2. Artifact and authority inspected
Under review: M44_WP3_PERIOD_RETURN_OWNERSHIP_GOVERNANCE_CORRECTION.md, 477 lines, untracked new file on feature/m44-wp3-period-return-governance-correction, base HEAD 38c0375.

Authorities independently read: M44 RC2 §§1.5, 3.1 G-2, 4.1–4.5, 5.1–5.3, 6 (invariants), 8.2 C2, 11 M44-WP3, 11.1, 12.1–12.7, 13.1–13.4, 16.2–16.5, 17 OQ-5; M44 Architecture Freeze Record §9; M44-WP1 Register §§4.1–4.2, 5.1–5.2, 6.1–6.4, 7, 8.1; M44-WP1 Freeze Record §§5, 12; M44-WP2 Confirmation Record §1.3; M44-WP2 Freeze Record §§4, 5, 8; M44-WP2 Closeout §§8–9; M43 Architecture §8 (raw line 174) and §9 WP6; M43-WP1 Register §§7.1–7.4; M43 Epic Closeout; platform_architecture.md §§6.3, 6.5; PORTFOLIO_CALCULATION_RULES.md §§1–10; M40-WP1 §8.3; M42 Architecture §8; M42-WP1 §3; ADR-001; ADR-004; DECISION_LOG.md.

## 3. Scope and method
I verified the authoring report rather than relying on it. Independent checks performed:

git status --short / git diff HEAD — exactly one untracked file, zero modified files, zero staged changes, no frozen-artifact path touched (INV-C1 holds).
Raw byte inspection of M43 §8 line 174 (cat -A) to confirm the quoted row's four field values verbatim against a tab-delimited source row.
Mechanical resolution of every repository-relative link in the artifact — all resolve; MISSING: 0.
Section-existence checks on every cited section of every cited authority (this surfaced F-02).
Semantic negative-language scan for closure, discharge, authorization, and transfer claims, filtered for qualifiers.
Cross-check of the D-1 prerequisite set against RC2 §§4.3, 4.5, 11.1, 12.1.1, 12.3, 12.5 and register §§4.2, 6.3, 7.
Cross-check of every authority in M43-WP1 §7.2 (nine rows) against the artifact's §3 hierarchy and §5 table.
## 4. Constitutional test matrix
Test	Subject	Result
A	Exact-row identification and quotation	PASS (see F-07, editorial)
B	Two-part ownership allocation preserved	PASS WITH FINDING (F-03, MINOR)
C	Formula, method, call-site, implementation-placement	PASS
D	Supersession mechanics and confirmation-dependence	PASS WITH FINDINGS (F-01 MAJOR; F-06 editorial)
E	Six-way separation of correction / release / block / step 4 / G-2 / D-1	PASS
F	G-2 state discipline	PASS WITH FINDING (F-05, MINOR)
G	Step-4 outstanding, lapsed vehicle, no substitute	PASS
H	D-1 complete prerequisite set	PASS WITH FINDINGS (F-04 MINOR; F-08 editorial)
I	Authority boundaries	PASS
J	Internal consistency	PASS WITH FINDING (F-04, MINOR)
K	Citation integrity	FAIL — MINOR (F-02)
L	Negative-language / prohibited-claim scan	PASS
—	Extension-basis declaration (INV-C2, RC2 §5.3)	FAIL — MAJOR (F-01)
## 5. Findings
### F-01 — Mandatory extension-basis declaration absent
Identifier: F-01
Classification: MAJOR
Location: Whole artifact; specifically the authority block (lines 15–42), §3 "Controlling authority hierarchy" (lines 114–155), §7 (lines 222–227) and §14 (lines 390–394). Both §7 and §14 rely on RC2 §5.3 by citation — "([M44 Architecture] §§5.3, 8.2, and 11 M44-WP3)" — while nowhere naming which extension basis is relied on and nowhere quoting the frozen sentence that supplies it.
Violated controlling authority: Frozen M44 RC2 §5.3 chapeau: "M44 may extend a frozen contract only on one of three exact bases, and every M44 artifact must name which basis it relies on and quote the frozen sentence that supplies it." Frozen RC2 §6 INV-C2: "Every M44 addition rests on exactly one of the extension bases E-1, E-2, or E-3 in §5.3, names which one, and quotes the exact frozen sentence that supplies it. No addition is justified by unstated silence." RC2 §5.3 E-3 assigns this exact act by name: "It supports … supplying a superseding ruling that names a defective frozen row (G-2)." Also engaged: INV-A2, requiring that a reviewer trace every asserted authority to an exact citation in the plan.
Constitutional consequence: The artifact's core act — superseding a frozen row — rests on §5.3 without discharging §5.3's own stated condition. The authority chain is therefore incompletely declared, and a confirmer applying §16.2 ("all authority declarations remain as this plan granted") cannot verify against E-3 what the artifact never names. The defect is structural, not cosmetic: the confirmed sibling artifact for the analogous G-1 act, M44-WP2 §1.3, names E-3, quotes the frozen sentence, expressly rules E-1 and E-2 inapplicable, and carries it as acceptance criterion W2-C-13. RC1 does none of these.
Required correction: Add an explicit extension-basis section (and a corresponding §17 acceptance-criteria row) that (a) names E-3 as the sole basis, (b) quotes RC2 §5.3's E-3 sentence including its express (G-2) allocation, (c) states E-1 and E-2 inapplicable with reasons, and (d) records that RC2 §5.3 itself assigns the basis, so the artifact does not self-select it.
Renewed independent review required: Yes.
Mitigating context, recorded for fairness: the frozen M44-WP1 Register §4.2 "Evidence required for disposition" list (six items) does not itself enumerate an extension-basis statement, and the register's §7 closure-matrix row for G-2 labels the closure owner as "the M43 governance sequence, exercised by M44 under frozen M43-WP1 §7.4 step 3" without an E-basis tag — unlike its G-1 and G-3 rows. This does not cure the defect: §5.3 and INV-C2 bind every M44 artifact at plan level, the register neither extends nor narrows RC2, and the register cannot discharge on WP3's behalf an obligation RC2 places on WP3's own text.

### F-02 — Citation to a non-existent section
Identifier: F-02
Classification: MINOR
Location: §1, line 95: "M44-WP2 Freeze Record §§5 and 11".
Violated controlling authority: Repository fact — M44_WP2_FREEZE_RECORD.md contains §§1–8 only; there is no §11. §5 ("Authority and gate boundary") does not establish the proposition cited for it. Engages RC2 §16.2 (evidence must be present as cited) and INV-A2.
Constitutional consequence: The proposition asserted — M44-WP2 complete and frozen with G-1 closed and effective — is true, but its pinpoint support does not resolve. A confirmer verifying the predecessor-satisfaction claim by citation would find a dangling reference. No substantive determination changes.
Required correction: Cite M44-WP2 Freeze Record §4 ("G-1 | CLOSED and EFFECTIVE through completed independent confirmation") and §8 ("M44-WP2 is COMPLETE AND FROZEN."). The header's parallel citations to M44-WP1 Freeze Record §§5 and 12, M44-WP2 Closeout §9, and M44 Architecture Freeze Record §9 all verified correct and need no change.
Renewed independent review required: Yes (mechanically, per RC2 §12.4: corrections require renewed review).
### F-03 — §5 table subordinates accounting semantics to "formula inputs"
Identifier: F-03
Classification: MINOR
Location: §5, line 182, concern column: "Financial truth and the canonical return and metric formulas' inputs, including the accounting semantics that determine what enters period return".
Violated controlling authority: Frozen M43-WP1 §7.3(2) is explicit that these are not the same category: "Capital-event stripping, external cash flow, imported assets, quantity corrections, NAV, cost basis, and the associated accounting arithmetic are accounting rule, not merely evidence." Platform Architecture §6.3 lists "The accounting semantics of every asset class" and "The canonical return and metric formulas' inputs" as separate owned items.
Constitutional consequence: Low. Both concerns remain with the same owner (Ledger & Accounting), so no ownership is transferred, lost, or enlarged, and the artifact's own §6.2 states them correctly as three coordinate items. The risk is that the normative table — the row a confirmer must check "in substance" — recasts an accounting rule as an input, which is precisely the collapse §7.3 guards against.
Required correction: Align §5 row 1 with the artifact's own §6.2 wording: replace "including" with a coordinate conjunction ("…formulas' inputs, and the accounting semantics that determine what enters period return").
Renewed independent review required: Yes (correction to a normative row).
### F-04 — Effectiveness trigger stated inconsistently in §11
Identifier: F-04
Classification: MINOR
Location: §11 item 1, lines 307–309: "M44-WP3 is independently confirmed with unresolved findings NONE and is frozen, making the §8 release-condition discharge and §9 standing-block disposition effective."
Violated controlling authority: Frozen RC2 §11 M44-WP3 and §8.2 C2 make confirmation the operative act ("Step 3 plus its independent confirmation discharges the frozen release condition"); §17 OQ-5 repeats it; register §7 G-2 row: "Confirmation of step 3 is the discharge of the frozen steps 1–3 release condition."
Constitutional consequence: Low, and self-limiting — RC2 §11 M44-WP3's freeze boundary is "Frozen on confirmation," so the two are coextensive in practice. But §§0, 1, 7, 8, 9, and 12 of the artifact all attribute effectiveness to confirmation alone, and §11 item 1 attributes it to confirmation and freeze. One of the two statements of the operative trigger must yield.
Required correction: Attribute effectiveness to independent confirmation with unresolved findings NONE, and keep "and frozen" as the separate D-1 prerequisite it is (RC2 §4.5, §11 freeze boundary), e.g. "M44-WP3 is independently confirmed with unresolved findings NONE — which makes the §8 discharge and §9 disposition effective — and is frozen."
Renewed independent review required: Yes.
### F-05 — Residual OPEN state restated incompletely
Identifier: F-05
Classification: MINOR
Location: §12, lines 354–357: "the residual permitted result is OPEN, with the exact missing element named."
Violated controlling authority: Frozen RC2 §16.2 and register §8.1 define OPEN as: "The obligation is not discharged; the exact missing element and its exact owner are named." The register states the vocabulary is "consumed verbatim … neither extends nor narrows it."
Constitutional consequence: Low — the state is hypothetical and not asserted. But it is a closed-vocabulary term restated with one of its two required elements dropped, inside the artifact's terminal-determination section.
Required correction: Restore "and its exact owner" to the residual OPEN description.
Renewed independent review required: Yes.
### Editorial observations (not constitutional blockers)
### F-06 — EDITORIAL. §0 lines 51–53: "It constitutionally supersedes the single named M43 Architecture §8 ownership row…" is present-tense. It is governed by the preceding clause "subject to independent confirmation" and corrected explicitly two paragraphs later and in §7, so no premature-effect claim survives a whole-text reading. Optional: carry the qualifier into the sentence itself.
### F-07 — EDITORIAL. §4 lines 163–168 renders the source row as four labelled block-quote fields. I verified the raw source (M43 §8 line 174) is a tab-delimited table row and that all four field values are reproduced verbatim, including "Candidate: Ledger & Accounting" and "WP6 is blocked until disposition; no second rule is permitted". The reformatting is faithful; noting only that it is a re-layout, not a literal transcription.
### F-08 — EDITORIAL. §11's D-1 prerequisite set does not name G-5 explicitly, reaching it through M44-WP6/WP7 confirmation and freeze instead. That is substantively equivalent (register §7 makes D-1's reachability contingent on both G-5 halves, which are exactly WP6 and WP7). Optional: name G-5 CLOSED for symmetry with G-3 CLOSED in item 4.
## 6. Ownership-allocation assessment
SATISFIED IN SUBSTANCE, subject to F-03.

The §5 allocation reproduces frozen M43-WP1 §7.3 with one owner per distinct concern, and every one of the nine authorities in §7.2 is cited and applied (Platform Architecture §6.3 and §6.5; M40-WP1 §8.3; M42 Architecture §8; M42-WP1 §3; PCR §§1–9 and §10; ADR-001; ADR-004). I verified each against source text: §6.3 "Owns. Financial truth. … The canonical return and metric formulas' inputs"; §6.5 "Owns. The canonical derived measures and their semantics. … The meaning of 'performance' on this platform"; M40-WP1 §8.3 "portfolio measure, portfolio performance … SHALL remain Portfolio Intelligence meaning"; M42 Architecture §8 row "Portfolio performance / return computation | Portfolio Intelligence"; M42-WP1 §3 leaving "accounting arithmetic, NAV/return formulas, or cost-basis rules" frozen; PCR §10 "Never recompute return inside an analytics/attribution module."

No sentence transfers, duplicates, narrows, or enlarges either allocation. The bidirectional non-acquisition sentences at lines 185–191 are present and correctly directional, satisfying INV-O2. The placement-does-not-decide-ownership rule at lines 193–197 matches §7.2's ADR-004 row and §7.3's compute_period_metrics() row. The no-second-rule prohibition is expressly carried forward (§6.3), and no formula, method, method version, or call site appears anywhere in the artifact — Test C passes without finding.

## 7. G-2 and step-4 assessment
CORRECT, subject to F-05.

G-2 carries exactly the one admissible successful state, RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE, matching RC2 §11 M44-WP3, §16.2, and register §8.1 (which prohibits CLOSED expressly). The state is declared non-closure in three places, CLOSED is affirmatively negated, and the pre-confirmation state is stated as NOT YET DISPOSITIONED, matching register §4.1's table. My semantic scan found no sentence equivalent to "G-2 is closed", "final recording has occurred", or "step 4 is discharged".

Step 4 is handled correctly and separately: the lapsed vehicle is named (the consolidated Decision Log entry authorized at M43 epic closeout by frozen M43 §§13 and 17), the artifact disclaims making the recording, disclaims creating/selecting/authorizing a substitute, and reserves the vehicle question to OQ-5. I independently verified the lapse: M43_EPIC_CLOSEOUT.md states "This closeout does not close an inherited gate," and DECISION_LOG.md contains no period-return ownership resolution entry. §10's statement that step 4 is a recording obligation outside the steps 1–3 release condition matches RC2 §3.1 G-2, §12.6, and OQ-5 exactly. Test E passes: all six events — step 3 correction, steps 1–3 discharge, block disposition, step 4, G-2 disposition, D-1 authorization — are held distinct, with none collapsed into another.

## 8. D-1 boundary assessment
COMPLETE, subject to F-04 and the editorial F-08.

I reconstructed the prerequisite set independently from RC2 §§4.3, 4.5, 11.1, 12.1.1, 12.3, 12.5 and register §§4.2, 6.3, 7, and the artifact's §11 matches it: WP3 confirmed and frozen; WP6 and WP7 confirmed and frozen with WP7 not confirmable before WP6 is frozen; WP1 complete and frozen; WP4 and WP5 confirmed and frozen; G-3 CLOSED; the §12.1.1 checkpoint passed before WP6; every applicable review and confirmation at unresolved findings NONE; and a separate authorization to begin. The G-4 OPEN handling is correct — content-constraining through the Component G binding rule, not a prerequisite failure (RC2 §12.3, register §6.3). The statement that M44-WP3 has no downstream M44 work-package consumer quotes the frozen position exactly (RC2 §11.1; register §6.3 "G-2 gates D-1 only"). WP3 nowhere releases or authorizes D-1, and §13 disclaims it explicitly.

## 9. Authority-boundary assessment
SATISFIED.

The header declares runtime, source-code, persistence/schema/migration, API/transport, UI, implementation, provider, scheduler/cache/observability, production-method, executable-validation, capability-completion, frozen-artifact-amendment, and step-4-vehicle authority all NONE, satisfying INV-A1 and exceeding its enumeration. Gate-disposition authority is confined to G-2 and expressly NONE for G-1, G-3, G-4, G-5, satisfying INV-A3. §13's twelve absence statements track RC2 §§4.4–4.5, 8.2, 11 M44-WP3, 12.6, 16.3, and OQ-5. No Decision Log, INDEX, ROADMAP, or GLOSSARY synchronization is claimed or performed (RC2 §12.6). No epic-closeout authority is asserted (RC2 §16.9). The only authority-chain defect is F-01, which concerns the declaration of the extension basis, not an assertion of authority beyond what RC2 granted.

## 10. Repository-scope assessment
SATISFIED AS AUTHORED.

Verified directly, not from the authoring report: git status --short returns exactly one entry, ?? docs/implementation/M44_WP3_PERIOD_RETURN_OWNERSHIP_GOVERNANCE_CORRECTION.md; git diff HEAD is empty; no staged changes; no frozen-artifact path appears (INV-C1 holds). The declared path matches RC2 §13.1's WP3 row character-for-character. Every repository-relative link in the artifact resolves. docs/decisions/, docs/architecture/ROADMAP.md, docs/GLOSSARY.md, docs/engineering/DECISION_LOG.md, and docs/implementation/INDEX.md are untouched, consistent with RC2 §§13.2–13.3 and §12.6.

## 11. Required corrections
ID	Class	Correction required
F-01	MAJOR	Add an extension-basis declaration naming E-3, quoting RC2 §5.3's E-3 sentence (including its express (G-2) allocation), ruling E-1 and E-2 inapplicable, and recording that RC2 §5.3 assigns the basis; add the matching §17 acceptance-criteria row.
F-02	MINOR	Replace the M44-WP2 Freeze Record "§§5 and 11" citation with §§4 and 8.
F-03	MINOR	In §5 row 1, replace "including" with a coordinate conjunction, matching the artifact's own §6.2.
F-04	MINOR	In §11 item 1, attribute effectiveness to confirmation; retain freeze as a separate D-1 prerequisite.
F-05	MINOR	In §12, restore "and its exact owner" to the residual OPEN description.
F-06–F-08	EDITORIAL	Optional. Not constitutional blockers; may be adopted or declined without affecting eligibility.
## 12. Final determination
NOT APPROVED

The artifact performs the substance of its allocated act well: it names and faithfully quotes the exact M43 §8 row, supersedes it through a later record without touching the frozen source, preserves the confirmed two-part split with one owner per concern, preserves the no-second-rule and one-implementation constraints, invents no formula or method, keeps all six governance events distinct, holds step 4 outstanding with its lapsed vehicle named and no substitute claimed, states the complete D-1 prerequisite set, and assigns G-2 exactly the permitted non-closure state. Tests A, C, E, G, I, and L pass without finding.

It is nonetheless not yet conforming: RC2 §5.3 and INV-C2 require every M44 artifact to name its extension basis and quote the frozen sentence supplying it, and RC2 §5.3 assigns this exact act — "supplying a superseding ruling that names a defective frozen row (G-2)" — to E-3. RC1 relies on §5.3 twice without discharging §5.3's own condition. That is a MAJOR finding, which forecloses "APPROVED WITH MINOR CORRECTIONS."

Unresolved constitutional findings: 5 — CRITICAL 0, MAJOR 1, MINOR 4. Editorial observations: 3 (excluded from the count; none is a blocker).
Formal Constitutional Response required: YES — for F-01 through F-05.
Corrected RC2 requires renewed independent review: YES — per frozen RC2 §12.4 ("corrections require renewed review") and §16.4.
Eligible to proceed directly to independent confirmation: NO — confirmation requires unresolved findings NONE (RC2 §12.4, §16.2, §16.5; register §4.2 evidence item 6).
No confirmation is issued by this review, and no repository file was modified.
