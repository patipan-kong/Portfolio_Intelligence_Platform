M44-WP5 — Renewed Independent Constitutional Architecture Review (RC2)
Target: M44_WP5_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md (candidate RC2)
Class: Non-normative planning document
Posture: Full re-review. No RC1 finding assumed resolved.

1. Executive summary
Eighteen of the nineteen RC1 findings are resolved correctly and durably. J-1 (frozen §6.7 proof wording), J-2 (the M43-WP2 §8.1 / M43-WP4 §6.7 list separation), J-3 (the §12.1.1 checkpoint boundary), J-4 (the INV-A1 authority block), J-5 (artifact class), J-6 (citation set), J-7 (the OQ-3 hypothesis framing), J-8 (artificiality marking), and all of N-1 through N-7 and E-1 through E-3 are addressed at frozen text, not by paraphrase. The authority ceiling is intact; no implementation, runtime, persistence, provider, serialization, or contract-authoring authority appears anywhere; no frozen artifact is modified; G-3 is untouched; §12.1.1 is expressly undispositioned; WP6 and WP7 remain unauthorized. §5's stage order remains constitutionally correct.

C-1 is not resolved correctly, and its correction introduced two regressions.

RC1 required the plan to state which frozen rule governs the OQ-3(c) branch and to cite both sides of the tension, without resolving it by assumption. RC2 resolves it by asserting that frozen M44 Architecture §17 OQ-3(c) "has precedence over the subordinate M44-WP1 register." That premise is false as a matter of frozen text. The requirement to name an exact owner in the OPEN state is not located only in the WP1 register — it is stated at the top authority level in five places inside the M44 Architecture itself: §3.1, §4.4 NON-GOALS, §10, §11 M44-WP5, and §16.2. The plan's precedence argument does not reach any of them, and §4.4 — one of the four sources the plan cites in support of its branch — states the opposite of what the plan uses it for.

The consequence is not theoretical. Under the plan's OQ-3(c) branch, the owner field carries UNRESOLVED — NO ADMISSIBLE OWNER PROVED. §16.2 defines OPEN as "the exact missing element and its exact owner are named" and admits states "from this closed vocabulary and from no other." A record without a named owner is therefore not OPEN as frozen, and is not any other listed state — the third state the plan expressly disclaims. Separately, the plan routes ownership-proof failure to a confirmed and frozen WP5 completion, while §10 calls it a determination that fails and §12.1.1's third outcome classifies an unestablished gate state as "a review defect in the producing work package." The plan never cites that third outcome.

Everything else in the document is sound. The defect is confined to the C-1 correction and to the two consequential regressions it introduced.

2. Constitutional findings
CRITICAL
C-1 — The OQ-3(c) branch authorizes a G-4 OPEN record that omits a field the frozen closed vocabulary requires, on a precedence claim that is false.

Plan §0 (C-1 response), §1, and §3 hold that "Frozen M44 Architecture… has precedence over the subordinate M44-WP1 register" and that the exact-owner requirement is therefore displaceable. The requirement is inside the M44 Architecture:

§3.1, G-4: "G-4 accordingly admits exactly two terminal states in M44: CLOSED… or OPEN, with the exact missing element and the exact owner it must come from recorded by name."
§4.4 NON-GOALS: "If ownership cannot be proved, or if the owner-domain instrument does not already exist, the correct M44 outcome is a recorded, named, open gate stating the exact missing element and its exact owner." — This addresses the failure case by name. The plan cites §4.4 as authority for the branch that contradicts it.
§10, Ownership proof failure: "…a recorded named blockage with the exact missing element and the exact owner it must come from, never an implicit owner (INV-O3)."
§11 M44-WP5, G-4 OPEN: "The requirement specification is delivered, the exact missing element and exact owner are named."
§16.2: "OPEN | The obligation is not discharged; the exact missing element and its exact owner are named", drawn "from this closed vocabulary and from no other."
§17 OQ-3(c) does not relieve the record of those fields. It is an alternative under an open question, and its own recommended answer states: "under (b) and (c) it records OPEN and specifies what is required" — an OPEN conforming to §16.2. Nothing in §17 amends §16.2.

The plan therefore pre-authorizes a determination record that cannot satisfy the frozen definition of the state it claims to occupy. Its mitigating language — that the tension is "exposed" and carried to independent confirmation (§7.4) — is undercut by §1 and §3, which decide the question in advance.

Required: withdraw the precedence assertion; state the OQ-3(c) tension against §3.1, §4.4, §10, §11, and §16.2 by quotation; and route the unresolved case per frozen §12.1.1 rather than by minting a substitute owner value.

C-2 — Ownership-proof failure is treated as a valid WP5 completion and freeze; the frozen corpus treats it as a failure and a review defect.

§10: "The affected determination fails and no contract is authored."
§11 M44-WP5 Completion criteria: "The ownership determination is proved with all four frozen M43-WP4 §6.7 proofs, and G-4 terminates in exactly one of two states…" — proving the four proofs is a conjunct of completion, not an alternative to it.
§12.1.1, third outcome: "Either gate's state not established | Stop. An unestablished gate state is a review defect in the producing work package and is corrected before the checkpoint is re-evaluated. | INV-B2, INV-F1."
Plan §5 routes WP5.2 failure to WP5.5 → WP5.6, whose exit is "Confirmed and frozen WP5, with unresolved findings NONE." This converts a frozen review defect into a frozen completion. The plan cites §12.1.1 three times (§0, §5.1, §9) and recites only the two G-3 rows; the third outcome — the one its own branch implicates — appears nowhere in the document.

Required: cite §12.1.1's third outcome, and state which of stop-and-correct or completion governs an unproved ownership determination, against §10 and §11's completion criteria.

MAJOR
J-1 — The frozen Component G binding rule is unformable under the OQ-3(c) branch, and §9 asserts otherwise.

Frozen §11 M44-WP6: "Where M44-WP5 terminates G-4 OPEN, Component G binds exactly one value: annualization unavailable — named missing element and named owner." Frozen §12.1.1, G-3 CLOSED row: "G-4 OPEN does not stop the milestone, because a named unavailability is a bindable outcome under frozen M43-WP4 §6.7."

Plan §9 bullet 1 states WP6 "would bind… the confirmed named blockage when G-4 OPEN" without distinguishing the two OPEN branches. An OQ-3(c) record supplies no named owner and therefore no formable Component G binding. The plan asserts a downstream consequence it has not verified against the frozen binding rule.

J-2 — UNRESOLVED — NO ADMISSIBLE OWNER PROVED is newly minted governed-status vocabulary, undeclared and outside the plan's own disclaimer.

The token is uppercase and em-dash-suffixed, formatted exactly like the frozen §16.2 status vocabulary (OPEN — PARTIAL, RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE), and is used as a record field value in a governance determination — §§0, 1, 3. §5's non-governed-label declaration covers only stage-output descriptions ("Authority intake", "hypothesis record", "corpus inventory", "candidate record", "absence record"); it does not reach this token. The header declares Vocabulary-admission authority NONE, and §8's own risk control requires any new governed noun to pass the frozen five-part vocabulary gate before use. This is a regression introduced by the C-1 correction. (The header's G-4 ONLY, SUBJECT TO INDEPENDENT CONFIRMATION is a lesser instance of the same pattern.)

J-3 — Frozen §3.1 is not cited anywhere, despite being the definitional source of the plan's central claim.

The header cites §§4–6, 8.4, 10, 11 M44-WP5, 12.1.1, 12.3, 12.5, 13.1, 16.2, and 17 OQ-3; §2 repeats a narrower set. §3.1 — which inventories G-4, fixes its two terminal states, and states the exact-owner condition — is absent from both. §16.2 is cited by number only; its OPEN row is never quoted. Had either been quoted, C-1 could not have been drafted as it stands. Under INV-B2 and the §14 integration check ("every cited path and section exists and says what the citation claims"), the §4.4 citation in §0 fails that test directly.

MINOR
N-1 — §7's lead-in is self-defeating: a determination is "eligible for constitutional review only when it supplies all seven disposition-evidence items," but item 7 is independent review and confirmation. Item 7's own text ("before a terminal result is effective") contradicts the lead-in. WP1 §4.4 lists item 7 as an element of disposition, not of review eligibility.
N-2 — §0's opening claim that the corrections "do not redesign the… two-state G-4 model" is inaccurate: §1's outcome table went from two rows to three and acquired a new owner-field value. Whether or not that change is sustained, the self-characterization should match it.
N-3 — §1's branch labels "G-4 OPEN — owner proved" and "G-4 OPEN — ownership proof failed" use the em-dash suffix, which is the frozen convention for a distinct state (OPEN — PARTIAL). The disclaimer paragraph mitigates but does not remove the collision; branches should not carry the state-suffix form.
N-4 — §2's M44 Architecture row cites a narrower set than the header (omits §§3.1, 4.4, 11 M44-WP5, 16.2). The two citation sets in one document should be identical.
N-5 — §2 states WP5's outcome "is a strict input to M44-WP6's Component G binding" without the §12.3 conditions (G-3 CLOSED and the checkpoint passed). §9 supplies them 200 lines later; a cross-reference at §2 would prevent a partial reading.
N-6 — §9's final bullet disclaims disposition of G-3 and G-5 only; G-1 and G-2 should be named for completeness, since §2 recites G-2's state.
EDITORIAL
E-1 — §0 embeds the RC1 review-response record inside the planning document. Sibling M44 work packages produced response records as separate governance artifacts. If the embedding is deliberate, say so; otherwise the plan is simultaneously the corrected artifact and the response to its own review.
E-2 — §5's non-governed-label list does not match the labels actually used in the table ("corpus inventory" vs "Existing-contract corpus inventory"). Align the enumeration to the terms in use, or the disclaimer's coverage is arguable — a point that matters given J-2.
E-3 — The header carries both Candidate: RC2 and Revision: RC1 FINDINGS ADDRESSED — CANDIDATE FOR INDEPENDENT RC2 CONSTITUTIONAL ARCHITECTURE REVIEW. One suffices.
3. Required-verification results
Verification	Result
Every RC1 finding resolved correctly	No — 18 of 19; C-1 resolved on a false premise
No constitutional regression introduced	No — J-2 (new status token) and N-3 (state-suffix branches) originate in the C-1 correction
Fail-closed behavior complete	No — C-1, C-2; §12.1.1's third outcome uncited
Ownership determination constitutionally correct	Partially — §3's success path is exact and faithful; the failure path is not
Authority boundaries unchanged	Yes — the INV-A1 block is complete and correct
Dependency citations accurate	No — §3.1 absent (J-3); §4.4 cited against its own text (C-1)
Downstream gating correct	Partially — G-3 handling in §5.1 and §9 is exact; J-1 and C-2 are gaps
No new governed vocabulary	No — J-2
No implementation/runtime/provider/serialization/contract-authoring authority	Yes — none present anywhere
No frozen artifact modified or reinterpreted	Modified: no (tree clean, one new file). Reinterpreted: yes — §4.4
G-3 unchanged	Yes
§12.1.1 undispositioned	Yes — stated explicitly in §5.1 and §9
WP6 and WP7 unauthorized	Yes — §4.2, §5.1, §9
4. Overall determination
NOT APPROVED

Two CRITICAL and three MAJOR findings, all confined to the ownership-proof-failure branch and its consequences. The rest of the document — scope boundary, authority ceiling, stage order, the §6.7 proof restoration, the M43-WP2 §8.1 / M43-WP4 §6.7 separation, the checkpoint boundary, and the downstream D-1/D-2b/D-3/D-7 statements — is constitutionally correct and should be carried into RC3 unchanged. The RC1 C-1 instruction stands unmet: the tension between §17 OQ-3(c) and the frozen exact-owner requirement must be exposed by quotation from §3.1, §4.4, §10, §11, and §16.2 and routed through §12.1.1, not settled by an asserted precedence hierarchy or by a substitute owner value.
