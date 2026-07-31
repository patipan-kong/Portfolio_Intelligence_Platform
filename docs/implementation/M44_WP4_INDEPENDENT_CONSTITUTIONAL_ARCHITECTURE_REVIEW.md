# M44-WP4 — Independent Constitutional Architecture Review

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics
Foundation

**Work package:** M44-WP4 only

**Artifact class:** Independent constitutional architecture review record

**Repository status:** Governing RC1 review recorded for review-chain completeness

**Review status:** `NOT APPROVED`

**Confirmation issued:** `NO`

**Freeze performed:** `NO`

**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/schema/migration authority:** `NONE`
**API/transport authority:** `NONE`
**UI/presentation authority:** `NONE`
**Implementation authority:** `NONE`
**Provider authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`
**Capability-completion authority:** `NONE`
**Frozen-artifact-amendment authority:** `NONE`
**Gate-disposition authority:** `NONE`
**Ownership-determination authority:** `NONE`
**Vocabulary-admission authority:** `NONE`
**Encoding-selection authority:** `NONE`

---

## Verbatim independent review record

M44-WP4 — Independent Constitutional Architecture Review
Artifact under review: M44_WP4_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md (548 lines)
Reviewer role: Independent constitutional architecture review, fresh session
Review date: 2026-07-29
Method: Every authority allocation, dependency, boundary, and acceptance criterion independently re-verified against the frozen corpus — M44 RC2 §§1.5, 3.1, 5.3, 5.4, 8.3, 11 (M44-WP4), 12.1.1, 12.3–12.5, 13.1, 16.2, 17 OQ-1; M44-WP1 register §4.3; M44-WP1 reconciliation §6; M44-WP1 Freeze Record §11.1; M42-WP7 §§3, 5, 8, 9; M43-WP3 Subject §§7.1–7.3.

Executive Summary
The plan is directionally sound and, in its core constitutional posture, correct. It grounds WP4 on extension bases E-1 and E-2 and expressly forbids silence-as-authority (§2) — exactly the re-grounding the RC1 adjudication mandated. It keeps the container/nested boundary intact, treats owner bytes as opaque, refuses to represent missingness, preserves the affirmative-absence distinction, refuses to declare the §12.1.1 checkpoint, and states the two-state CLOSED / OPEN — PARTIAL vocabulary without blending. Its §3 characterization of the frozen WP1 pre-inventory (two determined, one partial, seven unsatisfied, six source-owned) matches the frozen tally exactly. Dependencies are acyclic and the strict predecessor (M44-WP1 confirmed and frozen) is genuinely satisfied. Repository hygiene is clean: one added file, no frozen path touched.

It is nonetheless not approvable as written. Two defects are load-bearing. First, the acceptance criteria demand a PC-NGV non-triggering proof over only four of the fifteen frozen M42-WP7 §8 shapes, whereas frozen RC2 §8.3 conditions conformance on proving non-instantiation of any §8 shape, vector by vector; a contract built to this plan would be non-conforming by frozen definition. Second, the plan instructs WP4 to "test every coordinate against exactness and written-form requirements" and to classify every reference itself, while never stating that the M44-WP1 nested-coordinate pre-inventory is binding as written and may not be re-derived — the single control that protects the G-3 determination from drifting away from frozen evidence.

Beyond those, the document carries no authority-class declaration block (INV-A1 requires one of every M44 artifact), is itself a repository artifact not enumerated in frozen §11/§13.1 while its own §6 declares "exactly three planned deliverables," contains an acceptance criterion ("exactly one cited owner") that its own allocation table falsifies, collapses WP1's deliberate two-axis test into one axis, and silently decides the principal question WP1 §6.6 formally referred to WP4 without naming it.

None of these is a redesign trigger. All are correctable inside the existing architecture.

CRITICAL
C-1 — PC-NGV non-triggering proof is under-scoped; a conforming contract cannot result
Affected section: §4 Scope ("Explicit conformance proofs for PC-NGV-11 through PC-NGV-14"); §11 acceptance criterion 12; §10 Outputs.
Explanation. The plan's testable gate requires individual treatment of PC-NGV-11 through PC-NGV-14 only. The frozen requirement is broader in two independent ways. (i) Frozen RC2 §8.3 states: "C3 is not conforming unless it proves, vector by vector, that it does not instantiate any frozen M42-WP7 §8 non-conforming shape, with these four addressed individually and by name." M42-WP7 §8 contains fifteen shapes, PC-NGV-01 through PC-NGV-15. The four named ones are a floor, not the set. (ii) Frozen RC2 §8.3 additionally requires "one negative vector each" for PC-NGV-12 and PC-NGV-13, and frozen §11 M44-WP4 requires each proof to carry "a direct conformance statement and at least one negative vector." Criterion 12 requires neither. A WP4 contract satisfying every one of the plan's 24 acceptance criteria would therefore still be non-conforming under frozen §8.3 and would fail confirmation.
Constitutional basis. Frozen M44 RC2 §8.3 (required conformance proofs); §5.4 ("The frozen M42-WP7 §8 non-conforming-shape vectors PC-NGV-01 through PC-NGV-14 … M44-WP4 must prove non-triggering against them; it may not read any of them as narrowed, inapplicable, or superseded"); §11 M44-WP4 required tests; M42-WP7 §8.
Recommended correction. Restate §4 and criterion 12 as: non-triggering proved against every frozen M42-WP7 §8 shape vector by vector, with PC-NGV-11, -12, -13, and -14 addressed individually and by name, and at least one negative vector for each of the four. Add the §5.4 no-narrowing sentence to §7 authority boundaries.
C-2 — The plan directs WP4 to re-derive the frozen, binding M44-WP1 pre-inventory
Affected section: §12 (WP4.3 — "Test every coordinate against exactness and written-form requirements"); §11 criterion 3 ("Every reference is classified as supplied, partial or unsupplied"); §8 Dependencies; §9 Inputs.
Explanation. Frozen RC2 §11 M44-WP1 fixes the freeze boundary: "later M44 work packages cite it and may not re-derive the inventory." Frozen M44-WP1 Freeze Record §11.1 makes the consequence explicit — the register's "nested-coordinate pre-inventory [is] binding on M44-WP2 through M44-WP7 as written." Frozen WP1 reconciliation §6.7 restates it for this work package by name: "M44-WP4 consumes this pre-inventory; it does not re-derive it." The plan's §9 correctly lists the pre-inventory as an input, but §12 WP4.3 then allocates independent testing of every coordinate, and criterion 3 makes independent classification an acceptance condition — with no statement anywhere that the frozen determinations are binding and unmodifiable. The two instructions contradict each other, and the plan gives a WP4 author no rule for resolving the contradiction. The failure mode is not cosmetic: a re-derived classification that diverges upward from frozen WP1 is the only realistic path to a spurious G-3 CLOSED, which is the milestone's designated critical risk (frozen RC2 R-2, R-14).
Constitutional basis. Frozen M44 RC2 §11 M44-WP1 freeze boundary; frozen M44-WP1 Freeze Record §11.1; frozen M44-WP1 reconciliation §6.7 consequence 1; frozen RC2 §17 OQ-1 ("The WP1 pre-inventory is the deciding evidence for both").
Recommended correction. Add a normative statement to §8/§9 that the frozen WP1 per-field and per-facet pre-inventory is binding as written and may not be re-derived, re-classified, widened, or narrowed; recast WP4.3 as applying the frozen classifications to the closure/routing determination; recast criterion 3 as "every field's classification is carried verbatim from frozen WP1 §6.3–§6.4, with any perceived divergence raised as a review finding rather than resolved by WP4."
MAJOR
M-1 — The document declares no authority classes, artifact class, or status
Affected section: Document header (absent).
Explanation. The document opens directly at "Executive summary." It carries no Runtime authority: NONE, Implementation authority: NONE, Production-method authority: NONE, etc.; no artifact class; no status line; no governing-frozen-authority line. Every other M44 artifact — the architecture, the WP1 register, the WP1 reconciliation, the WP1/WP2/WP3 freeze records — carries the full block, and WP1 additionally carries Gate-disposition, Ownership-determination, Vocabulary-admission, and (in its freeze record) Encoding-selection authority as NONE. The plan's closing "READY FOR IMPLEMENTATION" recommendation, absent any declaration of what the document itself is or authorizes, is precisely the shape a later reader can misread as an authorization instrument. The review checklist's requirement that "implementation authority remains NONE, runtime authority remains NONE, production authority remains NONE" is therefore not verifiable from the artifact: it is inferable from §5 and the closing paragraph, but nowhere declared.
Constitutional basis. Frozen M44 RC2 INV-A1 ("Every M44 artifact declares runtime, source-code, persistence, schema, API, UI, provider, implementation, production-method, and executable-validation authority as NONE"); INV-A2; established M44 artifact convention.
Recommended correction. Add the standard M44 header block, including Gate-disposition authority: NONE and Encoding-selection authority: NONE, plus artifact class, status, and governing frozen authority with exact paths.
M-2 — The artifact is not enumerated in the frozen deliverable grant, and §6 understates repository impact
Affected section: §6 Repository impact; "Suggested repository artifacts."
Explanation. Frozen RC2 §1.5 grants "authority to author the documentary governance, contract, and normative-specification artifacts enumerated in §11, in docs/ only." Frozen §11 M44-WP4 enumerates exactly three architectural deliverables and Implementation deliverables: NONE; frozen §13.1 lists no per-work-package architecture or implementation plan for any M44 work package, and M44-WP1, WP2, and WP3 each proceeded without one. This document is a fourth file in docs/implementation/, and §6 — the section a reviewer uses to verify minimal repository impact — declares "Exactly three planned deliverables" without accounting for the document itself. The later "Suggested repository artifacts" section then adds up to seven further review-chain files. §6 is therefore neither complete nor consistent with the rest of the document.
Constitutional basis. Frozen M44 RC2 §1.5; §11 M44-WP4 architectural deliverables; §13.1 new-files table; INV-A2.
Recommended correction. Either (a) declare the document non-normative working material outside the canonical corpus, or (b) record it in §6 as an additive, unenumerated planning artifact that asserts no authority, adds no normative row, and is superseded in full by the WP4 contract — and restate §6 as a complete repository-impact forecast covering this document, the three deliverables, and the review-chain artifacts.
M-3 — Acceptance criterion 2 is falsified by the plan's own allocation table and by frozen evidence
Affected section: §11 criterion 2 ("Every field has exactly one cited owner"); §2 Constitutional allocation.
Explanation. The plan's §2 table cites multiple domains for single coordinates — Benchmark Declaration to "Portfolio Intelligence, Market Intelligence, and Asset Foundation as allocated", and the Identity/Scope/Membership/Base-Currency row to "Ledger & Accounting, with Asset Foundation authority where allocated." That framing is faithful to frozen WP1 §6.3, which records field 5 as "Ledger & Accounting (coordinate); Asset Foundation (the currency-of-denomination dimension)", field 6 as "Portfolio Intelligence (declaration); Asset Foundation (criterion vocabulary)", field 7 as three domains, and field 10 as two. Criterion 2 as written is therefore unsatisfiable against the binding evidence, and an author who satisfies it literally will drop a frozen co-allocation — an ownership defect under M42-WP7 §9 item 3. A second, smaller inaccuracy: the §2 row attaches "Asset Foundation where allocated" to all four Ledger coordinates, whereas frozen allocation attaches it to Base Currency alone.
Constitutional basis. Frozen M44-WP1 reconciliation §6.3 (binding under Freeze Record §11.1); M42-WP7 §3 and §9 item 3; frozen RC2 INV-O1.
Recommended correction. Restate criterion 2 as "every field carries the exact frozen owner allocation of M42-WP7 §3 as recorded in frozen WP1 §6.3, including each co-allocated domain, with no owner added, merged, or dropped." Split the §2 grouped row so Asset Foundation attaches only to Base Currency.
M-4 — Acceptance criterion 3 collapses WP1's deliberate two-axis test
Affected section: §11 criterion 3; §12 WP4.3.
Explanation. Frozen WP1 §6.2 decomposes the M43-WP3 §7.1 test into two separable questions — (a) reference exactness and (b) written-form determinacy — and states that separating them "is required, not stylistic." The distinction is decisive: fields 2, 3, 5, 6, 7, and 8 are SUPPLIED — EXACT on (a) while five of them are NOT SUPPLIED on (b); fields 4 and 10 fail (a) as well. Criterion 3's single "supplied / partial / unsupplied" axis cannot express that, and a field recorded "supplied" on (a) alone would wrongly count toward CLOSED under criterion 18. The facet level has the same problem: frozen §6.4 classifies six Investment Universe facets, five Benchmark facets, and three Provenance facets separately, and §10 of the plan asks for "composite-coordinate facet analysis" — but no acceptance criterion tests it.
Constitutional basis. Frozen M44-WP1 reconciliation §6.2, §6.3, §6.4; frozen M43-WP3 §7.1; frozen RC2 §11 M44-WP4 completion criteria.
Recommended correction. Replace criterion 3 with a two-axis criterion carrying (a) and (b) per field, add a criterion requiring per-facet classification for fields 6, 7, and 10, and state that CLOSED requires both axes satisfied at field and facet level.
M-5 — The principal referred question is decided implicitly, without being named
Affected section: §2 (Investment Universe row); §7 ("may not redefine a nested coordinate even where Portfolio Intelligence owns its meaning"); §14 risk row 4; §15 Open questions.
Explanation. Frozen WP1 §6.6 records, as "the pre-inventory's principal referred question," whether M44-WP4 may supply the nested forms for the two coordinates that frozen M42-WP7 §3 allocates to Portfolio Intelligence itself — the Investment Universe declaration's nested form and three Benchmark Declaration facets. It sets out frozen text on both sides, expressly declines to resolve it, and refers it to M44-WP4 under frozen RC2 §17 OQ-1, whose decision deadline is "Before M44-WP4 begins for the scoping question," under WP4's own independent confirmation. The plan resolves it — in the negative — but only implicitly, through §2's "Consume; no amendment" and §7's prohibition. It never names the question, never cites WP1 §6.6 or RC2 §17 OQ-1, never states the constitutional basis for choosing the "Against" branch, and includes no acceptance criterion by which a reviewer can test the resolution. §15 "Open questions" lists five items and omits the one the frozen corpus formally referred. A decision of this weight, reached silently, is not independently reviewable.
Constitutional basis. Frozen M44-WP1 reconciliation §6.6; frozen RC2 §17 OQ-1 (decision deadline and affected work packages); INV-C2 (every extension names its basis and quotes the frozen sentence).
Recommended correction. Add an explicit §15 item naming the referred question, citing WP1 §6.6 and RC2 §17 OQ-1, stating the resolution and its basis (M42-WP7 §5 "any source-owned coordinate", §9 item 11's unqualified owner, PC-NGV-14, INV-C1), and add an acceptance criterion that the resolution is recorded in the contract and independently confirmed.
M-6 — Reviewer distinctness is under-specified
Affected section: §13 Review strategy.
Explanation. The plan requires "two independent disciplines" and states "The author cannot be the sole reviewer." Frozen RC2 §12.4 requires more: "M44-WP4, M44-WP6, and M44-WP7 additionally require an independent serialization/numerical review distinct from the constitutional reviewer." As written, one reviewer could discharge both disciplines and satisfy the plan while violating the frozen rule. Frozen WP1 register §4.3 evidence item (9) states the same requirement independently.
Constitutional basis. Frozen M44 RC2 §12.4; frozen M44-WP1 register §4.3 evidence item 9.
Recommended correction. State in §13 and in acceptance criterion 21 that the serialization review is performed by a reviewer distinct from the constitutional reviewer and from the author, and that corrections require renewed review by the same discipline.
M-7 — A frozen required test is missing from the acceptance criteria
Affected section: §11 criterion 4; §10 Outputs.
Explanation. Frozen §11 M44-WP4 required tests include "a preservation check proving the tag and field order are byte-order-identical to frozen M42-WP7 §5"; frozen WP1 register §4.3 evidence item (7) repeats it. The plan's criterion 4 covers the tag only ("The exact frozen schema tag is preserved") and criterion 1 covers order only as an inventory ("inventoried in frozen order"). No criterion requires the byte-order-identity preservation check over both.
Constitutional basis. Frozen M44 RC2 §11 M44-WP4 required tests; frozen M44-WP1 register §4.3 evidence item 7; M42-WP7 §9 item 10.
Recommended correction. Add a criterion requiring an explicit preservation check demonstrating that the tag and the ten-field order in the contract are byte-order-identical to frozen M42-WP7 §5.
MINOR
m-1 — u32 / lp(x) described as a cross-corpus frozen convention. §4 and §9 call these "the frozen M43 mechanical convention." M43-WP3 §7.1 defines them "For this WP3 corpus only" and adds that they are "local contract mechanics, not new vocabulary, an executable serializer, persistence format, API representation, or permission to invent an upstream encoding." Correction: state that WP4 defines its own identical primitives in its own contract, citing M43-WP3 §7.1 as precedent and noting its corpus-local scoping.
m-2 — Non-exact citations in §8 Dependencies. "M34 ownership and Provenance decisions" where frozen §8.3 Inputs names M34-D-0010 exactly; "M44 architecture RC2" and "Frozen M44-WP1 inventory and reconciliation" cited without repository paths, and the freeze records that establish "confirmed and frozen — satisfied" are not cited at all. Correction: cite by exact path and identifier throughout, consistent with the rest of the M44 corpus.
m-3 — Criterion 16 is not marked CLOSED-only. Frozen §11 M44-WP4 states byte-identical derivation by two independent readers "is required for closure and is unattainable while any coordinate is routed; the two criteria are therefore never asserted together." The plan applies it to "every fully representable vector," which under OPEN — PARTIAL means artificial specimens. §10's ARTIFICIAL / NON-CONFORMANCE-ESTABLISHING labelling guards this, but §11 does not. Correction: annotate criterion 16 as a container-mechanics test that is never evidence for CLOSED.
m-4 — The Benchmark form-discriminator constraint is never named. Frozen WP1 §6.4 records it as CONSTRAINED — NOT SUPPLIED, citing M42-WP5 §4.3: the four form labels "do not authorize runtime discriminators, serialized tags, API values, database enumerations, or implementation constants" — so a byte form must distinguish the four forms without using the labels as tags, and no frozen authority supplies how. It is the sharpest encoding trap in the package. Correction: name it in §4 and in the routing set, recording that it is nested content routed to its owner and not framed by WP4.
m-5 — Acceptance criteria omit authority-basis and gate-reporting tests. §10 requires an "extension-basis proof" and §13 verifies "E-1/E-2 are the sole authority bases," but no criterion in §11 tests INV-C2 (name the basis, quote the frozen sentence) or INV-B2 (every inherited open gate named and cited by exact path and section). Frozen R-15 assigns the "declared silence" regression risk to WP4 specifically. Correction: add both as acceptance criteria.
m-6 — Review-artifact naming left open (§15 item 5). Frozen §13.1 does permit convention-based naming for per-work-package review artifacts, so this is admissible — but frozen WP1 §3.1 and Freeze Record §2.1 record that filing-path divergence at architecture level blocked every M44 work package until a rename was performed. Correction: pin the exact WP4 review-chain paths in §6 before authoring begins.
m-7 — Checkpoint recording vehicle not noted. Frozen §12.1.1 states the checkpoint outcome "is recorded in the M44-WP1 closure register," which is now frozen; the plan's §5 correctly excludes changes to WP1 artifacts and roadmap step 17 depends on the checkpoint. The tension is inherited, not WP4's to resolve. Correction: record it as a noted inherited question with an explicit statement that WP4 neither resolves it nor recharacterizes it.
m-8 — Rejection vocabulary drifts from frozen terms. Frozen §11 M44-WP4 names "unknown fields, alternate forms, duplicate keys, non-canonical numbers, trailing bytes, and Unicode ambiguity"; §4 substitutes "non-canonical textual substitutions" and moves Unicode to criterion 11. Correction: restate the frozen list verbatim, then map each term to its container-level treatment.
m-9 — Risk register omissions. §14 has no row for re-derivation of the frozen WP1 pre-inventory (C-2), for reviewer non-distinctness (M-6), for unenumerated repository artifacts (M-2), or for the frozen R-15 carry-forward ("authority restated as declared silence by a later author"), which frozen RC2 assigns to WP4. Correction: add the four rows with treatments.
EDITORIAL
e-1 — §3 tally wording. "Seven fields without complete written-form determinacy" would number eight if the partial field is included; frozen WP1 §6.3 says "unsatisfied for seven" and "partially satisfied for one" as disjoint categories. Use WP1's vocabulary verbatim.
e-2 — §4 envelope is not indexed to the frozen field order. The nine lp(...) lines plus the tag do correspond correctly to frozen fields 1–10, with the tag as field 1 schema_version — but the mapping is left for the reader to reconstruct. Annotate each line with its frozen §5 field number and name.
e-3 — §15 item 2 omits the on-point precedent. M43-WP3 §7.2 frames its own contract tag as raw ASCII("PMS1"), unframed and fixed-length, which is directly relevant evidence for the tag-framing decision. Cite it.
e-4 — §12 and "Implementation sequencing" partially duplicate the "Implementation roadmap." Three overlapping sequence statements invite drift under correction. Consolidate to one.
Checklist disposition
#	Checklist item	Result
1	Constitutional authority — justification, no expansion, no transfer, no silence-as-authority	PASS with M-5. E-1/E-2 correctly named and exclusive; silence expressly disclaimed; no ownership transfer or expansion found. The referred own-domain question is resolved without being named.
2	Repository scope — minimal, justified, no hidden modification	FAIL — M-2. No hidden modifications (verified: one added file, no frozen path). §6 is incomplete and inconsistent with the artifact list, and the document is unenumerated in the frozen grant.
3	Scope boundaries — complete; implementation / runtime / production authority NONE	FAIL — M-1. In-scope and out-of-scope are substantively complete and faithful to frozen §11. The NONE declarations are absent as declarations.
4	Dependencies — predecessors cited, none missing, no circularity	PASS with m-2. Strict predecessor M44-WP1 confirmed and frozen — independently verified. No circular dependency. Citation exactness is below corpus standard.
5	Acceptance criteria — objective, testable, internally consistent	FAIL — C-1, M-3, M-4, M-7.
6	Risks — complete and constitutionally accurate	PASS with m-9. The eleven listed risks are accurate and correctly treated; four required rows are missing.
7	Review strategy — sufficient, preserves independence	FAIL — M-6. Two disciplines correctly identified; reviewer distinctness not required.
Overall Result
NOT APPROVED

Two CRITICAL findings (C-1, C-2) and seven MAJOR findings must be corrected and the corrected plan re-reviewed before WP4 documentary authoring begins. No finding requires redesign of the M44 architecture, and none disturbs the plan's central determination: the frozen evidence continues to indicate G-3 OPEN — PARTIAL as the expected terminal state, which remains a valid completion of M44-WP4 and is not a closure.
