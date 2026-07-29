M44-WP5 — Independent Constitutional Architecture Review (RC1)
Target: M44_WP5_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md
Class: Non-normative planning document
Reviewer posture: Independent; the document is assumed defective until proved otherwise against frozen text.

1. Executive summary
The plan's architectural intent is constitutionally sound. It correctly identifies WP5 as a determination-only work package, correctly refuses contract-authoring authority in any corpus, correctly separates ownership proof from corpus inventory (§3, §5), correctly holds G-4 to exactly two terminal states, correctly refuses to treat 252/365/365.25 as admissible when ambient, and correctly declines to reinterpret M44-WP4's frozen G-3 OPEN — PARTIAL result. It introduces no runtime, source, provider, serialization, or contract-authoring authority, and expands no domain's ownership. On the eleven required negative checks, ten pass.

It nevertheless fails review on fidelity of consumption. In a corpus whose governing rule is exact citation at frozen meaning (RC2 §1.6.2, INV-C2), this plan paraphrases frozen normative text at three load-bearing points, misattributes a frozen five-element list to the wrong frozen section, omits the controlling frozen artifact for G-4 from its authority set, and — most seriously — has no defined fail-closed exit for a failed ownership proof, a branch that frozen RC2 §10, INV-O3, and §17 OQ-3(c) all expressly contemplate. Its stage table structurally cannot express that branch: WP5.3's entry condition is "WP5.2 selects an owner."

It also omits the §12.1.1 gate-state checkpoint entirely. Given the frozen M44-WP4 Freeze Record carries §12.1.1 checkpoint: NOT DISPOSITIONED and Gate-disposition authority: NONE, and given WP5 confirmation is the checkpoint's trigger, this is a downstream-gating defect, not an omission of detail.

None of the defects is unfixable. All are corrections to the planning document itself; none requires amending a frozen artifact or re-scoping the work package.

Determination: NOT APPROVED.

2. Constitutional findings
CRITICAL
C-1 — No fail-closed path for ownership-proof failure; the sequencing structurally presumes an owner will be proved.

Plan §1 defines the OPEN outcome solely as "No exact existing governed contract kind is found." §5 makes WP5.3's entry condition "WP5.2 selects an owner." §4.1 requires the requirement specification to name "only what that owner must supply." Every path in the document presupposes a successful ownership proof.

The frozen corpus does not:

RC2 §10, row Ownership proof failure: "The affected determination fails and no contract is authored… A failed ownership proof produces a recorded named blockage with the exact missing element and the exact owner it must come from, never an implicit owner (INV-O3)."
RC2 INV-O3: "An unresolved owner is a blocking condition, never an implicit assignment."
RC2 §17 OQ-3 alternative (c): "No admissible owner; G-4 OPEN with the ownership question itself unresolved."
RC2 §4.4 NON-GOALS: "If ownership cannot be proved… the correct M44 outcome is a recorded, named, open gate."
The plan cites none of these — not §10, not INV-O3, not OQ-3. The effect is a live constitutional hazard: if WP5.2 cannot prove an owner, the stage table offers no exit, creating structural pressure to select one so WP5.3 can begin. That is the implicit assignment INV-O3 prohibits.

This is compounded by a genuine tension the plan must resolve rather than inherit silently: frozen M44-WP1 §4.4 requires that in the OPEN state "the requirement specification is delivered and the exact missing element and exact owner are named" — a named owner in both terminal states — while RC2 §17 OQ-3(c) admits an unresolved ownership question. The plan must state which frozen rule governs and what WP5 records under (c), citing both.

MAJOR
J-1 — The frozen §6.7 proofs 1–2 are restated as class-agnostic paraphrase, dropping the named authority classes.

Frozen M43-WP4 §6.7 requires proof of "why VERSIONED_CALCULATION_DEPENDENCY is constitutionally correct" and "why GOVERNED_EVIDENCE is constitutionally incorrect for the annualization basis." Frozen M44-WP1 §4.4, evidence item (1), binds the same named classes. RC2 §8.4 C4 repeats the binary explicitly.

Plan §3 substitutes: "1. the selected authority class is constitutionally correct; 2. each plausible alternative authority class is constitutionally incorrect." This is not the frozen proposition. It permits a determination that proves some other class correct without ever addressing the two the frozen corpus names, and it converts a fixed frozen binary into an author-defined candidate set.

Plan §3(4) additionally drops "ownership of source" from the frozen "transfer ownership of source calendar meaning," and drops the frozen M44-WP1 §4.4 qualifier "out of Market Intelligence."

J-2 — "Canonical value bytes" is misattributed to frozen M43-WP2 §8; the frozen §8.1 Dependency key is dropped.

Frozen M43-WP2 §8.1's declaration record contains exactly five fields: Dependency key, Owning domain, Dependency contract kind, Dependency identifier, Dependency version. Canonical value bytes is not among them. That term originates in frozen M43-WP4 §6.7 ("an exact owner, existing governed contract kind, identifier, immutable version, and canonical value bytes"), which is a different five-element list that omits Dependency key.

The plan conflates the two lists and attributes the result to M43-WP2 §8 in five places — §2 ("Exact five-coordinate calculation-dependency declaration"), §4.1, §5 WP5.3 and WP5.4, §7.3, and the §8 risk row ("require all five M43-WP2 §8 coordinates"). RC2 §11 M44-WP5 is careful not to make this attribution; it cites M43-WP2 §8.2 for closure vectors and sources the five owner-published fields separately.

J-3 — The mandatory §12.1.1 gate-state checkpoint is absent from the plan.

Frozen RC2 §12.1.1 places a mandatory milestone halt "After M44-WP4 and M44-WP5 are confirmed and before M44-WP6 begins." §12.5 point 5 makes it an independent confirmation point. Frozen M44-WP1 §4.4 states the G-4 governance path as "independent constitutional review → independent confirmation… then the §12.1.1 checkpoint confirmation." The frozen M44-WP4 Freeze Record carries §12.1.1 checkpoint: NOT DISPOSITIONED and Gate-disposition authority: NONE.

The plan never names §12.1.1. §5.6's exit condition is "Confirmed and frozen WP5" with nothing after it. §9 proceeds directly to "M44-WP6 may bind the annualization state in Component G", with the checkpoint — the actual mechanism standing between WP5 freeze and WP6 — unmentioned. The plan also never disclaims checkpoint-disposition authority, which its sibling frozen records do explicitly.

Concretely: with G-3 currently OPEN — PARTIAL, WP5 confirmation triggers a checkpoint whose frozen outcome is "Stop, or formally re-scope." A plan whose §9 says WP6 "may bind" without stating this is under-gating its own downstream boundary.

J-4 — The authority declaration block is incomplete against INV-A1.

RC2 INV-A1: "Every M44 artifact declares runtime, source-code, persistence, schema, API, UI, provider, implementation, production-method, and executable-validation authority as NONE."

The plan declares Implementation, Runtime, Source-code, "Persistence/API/UI/provider", and contract-authoring/registration/extension/versioning/serialization. It omits schema/migration, production-method, and executable-validation. It also omits capability-completion, frozen-artifact-amendment, gate-disposition, and vocabulary-admission — all of which the frozen M44-WP1 and M44-WP4 records carry. INV-A1 is directly falsifiable against the header as written.

J-5 — §6 mislabels the WP5 deliverable's artifact class as "normative."

§6: "The frozen M44 architecture assigns exactly one normative deliverable path to WP5." The frozen architecture makes no such assignment. RC2 §2.1 reserves "normative specification" for items 5–6 (WP6/WP7); item 4 — the annualization work — is deliberately not so described. RC2 §11 M44-WP5 calls it an "Architectural deliverable." The adjudicated Finding 2 disposition, and the plan's own §4.1 and §7.6, require the requirement specification to be explicitly non-normative. §6 contradicts §7.6 of the same document.

J-6 — The governing-authority set omits the controlling frozen artifact for G-4.

The header cites RC2 §§4–5, 7, 11 M44-WP5, 12.2, 16.2, plus the Architecture Freeze Record and frozen M43 sections. §2 cites the M44-WP1 Freeze Record — but not M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md §4.4, which is where G-4's constitutional purpose, governing frozen authority, exact closure authority, permitted terminal states, and the seven-item evidence required for disposition are actually bound. WP5 cannot be assessed against, or comply with, a register it does not cite.

Also absent: RC2 §6 (INV-A1, INV-C2, INV-C4, INV-O3, INV-F1, INV-B2), §8.4 (C4 — the component-model definition of this work), §10 (failure and boundary behavior), §12.1.1, §12.3, §12.5, §13.1, and §17 OQ-3.

J-7 — §2 pre-commits the search corpus to Market Intelligence before WP5.2 runs.

The §2 frozen-baseline row reads: "M39 and M40–M41 frozen Market Intelligence corpus | The governed Market Observation, Market Measure, calendar, and versioning surfaces against which an existing owner-domain contract may be assessed." This equates "the owner-domain corpus" with Market Intelligence as a settled premise.

Frozen RC2 §17 OQ-3 is explicit that this is "an architectural deduction, not a repository-confirmed fact, and M44-WP5 must prove or reject it." §2 as written silently converts a hypothesis into a baseline, undercutting the ownership-proof/corpus-inventory independence that §3 and §5 otherwise establish correctly. The row must carry the OQ-3 framing: M39/M41 are available for search if and only if WP5.2 proves Market Intelligence the owner.

J-8 — Positive documentary vectors are required without the frozen artificiality marking.

§4.1 and §7.8 require "positive, boundary, and negative" vectors covering dependency closure. Under G-4 OPEN, any positive dependency-closure vector necessarily exhibits a contract-kind label that does not exist. Frozen M43-WP4 §6.7 permits illustrative examples "only when marked artificial, non-effective, and incapable of passing the future gate," and states categorically that "no artificial label in a fixture can satisfy WP2 closure." The plan carries neither constraint, while §7.8 simultaneously demands a negative vector rejecting M44-authored kinds — the two requirements collide without the marking rule.

MINOR
N-1 — §9 states D-2b "needs both the WP5 determination and… the separately authorized owner-domain instrument before it can proceed." Frozen RC2 §4.3 also blocks D-2b on D-1. The "needs both" phrasing implies sufficiency.
N-2 — §9 never names D-7, and omits D-3. Frozen M44-WP1 §4.4, evidence item (4), requires the OPEN record to state "the consequences for D-2b and D-7"; RC2 §11 M44-WP5 lists D-3 as a downstream consumer.
N-3 — §2 paraphrases G-2's state as "released with final recording pending" rather than the §16.2 closed-vocabulary term RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE. §16.2 requires terminal states drawn "from this closed vocabulary and from no other."
N-4 — §2 cites "M44-WP4 Freeze Record and Epic Closeout" without noting the closeout is work-package-scoped. That artifact states it "does not close, and makes no claim about, the M44 milestone/epic as a whole." No M44_EPIC_CLOSEOUT.md exists.
N-5 — §7.5: a governed version-bound 252 "may be admitted only once all required coordinates are supplied." WP5 holds no admission authority. Restate as admissibility, not admission.
N-6 — §5 introduces working labels — "citation register", "candidate ledger", "absence ledger" — without declaring them non-governed internal labels, given RC2 §9.7 and the plan's own §8 vocabulary-drift risk row.
N-7 — §5 WP5.1's exit is "no owner determination yet," but its responsibility includes establishing "candidate alternative authority classes" — an input to the §6.7 proof. Harmless, but the intake/proof boundary should be stated so candidate-set framing is not later treated as proof.
EDITORIAL
E-1 — §3 is titled "Ownership model" but describes a determination method, not a model.
E-2 — §1 outcome table, CLOSED row: "It may be cited by a later…" — the antecedent of "It" (the contract kind) is not stated.
E-3 — The header carries no candidate/revision label (RC1), unlike sibling M44 planning artifacts whose review lifecycle is tracked by RC number.
3. Required corrections
(C-1) Add an explicit fail-closed branch for ownership-proof failure. Cite RC2 §10 "Ownership proof failure", INV-O3, §4.4 NON-GOALS, and §17 OQ-3(c). Give WP5.3 a defined non-entry path, and state in §1 what WP5 records under OQ-3(c) — reconciling against frozen M44-WP1 §4.4's requirement that OPEN name an exact owner. Do not resolve the tension by assumption.
(J-1) Restore the frozen §6.7 proofs verbatim, including VERSIONED_CALCULATION_DEPENDENCY, GOVERNED_EVIDENCE, "ownership of source calendar meaning", and "out of Market Intelligence." Any generalization must be additive to, never a substitute for, the frozen propositions.
(J-2) Separate the two frozen lists. Attribute the M43-WP2 §8.1 declaration record (including Dependency key) to §8.1; attribute owner, kind, identifier, immutable version, and canonical value bytes to M43-WP4 §6.7; cite M43-WP2 §8.2 for closure. Remove every instance of "five M43-WP2 §8 coordinates."
(J-3) Add the §12.1.1 checkpoint to §5 (as a post-WP5.6 boundary, not a stage) and to §9. State that WP5 holds no gate-disposition authority beyond G-4, does not disposition the checkpoint or G-3, and that with G-3 currently OPEN — PARTIAL the frozen checkpoint outcome is stop or formally re-scope. Cite RC2 §12.1.1, §12.3, §12.5 point 5, and M44-WP1 §4.4.
(J-4) Complete the header authority block per INV-A1 — add schema/migration, production-method, executable-validation — plus capability-completion, frozen-artifact-amendment, vocabulary-admission, and a scoped gate-disposition declaration.
(J-5) Remove "normative" from §6. Use RC2 §11's term ("architectural deliverable") and state the artifact class consistently with §4.1 and §7.6.
(J-6) Add frozen M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md §4.4 to the governing authority and to §2, and map its seven disposition-evidence items onto §7. Add RC2 §6, §8.4, §10, §12.1.1, §12.3, §12.5, §13.1, and §17 OQ-3 to the citation set.
(J-7) Rewrite the §2 M39/M40–M41 row to carry the OQ-3 framing: Market Intelligence ownership is a hypothesis WP5.2 must prove or reject, and the corpus to be searched is fixed only by WP5.2's outcome.
(J-8) Carry the frozen M43-WP4 §6.7 marking rule into §4.1 and §7.8: any illustrative positive example must be marked artificial, non-effective, and incapable of passing the future gate, and no artificial label satisfies M43-WP2 closure.
(N-1 – N-7, E-1 – E-3) Apply as stated.
4. Assessment against the required checks
Required check	Result
No new governed vocabulary	Pass, with N-6
No expansion of Portfolio Intelligence ownership	Pass (§3, §4.2)
No implementation authority	Pass in substance; header incomplete (J-4)
No runtime authority	Pass
No contract-authoring authority	Pass — §4.2 and the header are unambiguous
No serialization authorization	Pass
No provider-behavior authorization	Pass (§8 closing paragraph)
No frozen-milestone reinterpretation	Fail — J-1, J-2 paraphrase frozen normative text
Does not change G-3	Pass (§4.2, §9)
Does not disposition §12.1.1	Pass in effect, unstated — J-3
Does not authorize WP6/WP7	Pass (§4.2, §9 bullet 3); §9 bullet 1 needs the checkpoint caveat
Ownership proof independent of corpus inventory	Pass in §3/§5; undercut by §2 (J-7)
Ownership proof independent of admissibility	Pass — WP5.2/WP5.4 are separate stages
Ownership proof independent of downstream implementation	Pass
G-4 terminal states exactly two	Pass — no third state is introduced
Failure always fail-closed	Fail — C-1
M43 dependencies correctly consumed	Fail — J-1, J-2
M44-WP1…WP4 consumed by citation only	Pass, but incompletely — J-6
No frozen artifact modified	Pass — §4.2 excludes it; no repository change proposed
No authority transferred	Pass
Work decomposition: stages WP5.1 → WP5.6 are correctly ordered, non-redundant, and do not improperly combine responsibilities. Ownership proof precedes corpus inventory precedes admissibility precedes record precedes lifecycle — this is the correct constitutional order and the plan's principal strength. Two things are missing, not misordered: the ownership-proof-failure branch (C-1) and the post-freeze §12.1.1 hand-off (J-3).

5. Overall determination
NOT APPROVED

One CRITICAL and eight MAJOR findings. The work package's scope, authority ceiling, ownership posture, and stage ordering are constitutionally correct and should be retained unchanged. The failures are in fidelity of consumption and in an unspecified fail-closed branch — both correctable within the planning document, without amending any frozen artifact and without re-scoping WP5. Re-submission should be reviewed as RC2 against the ten required corrections above.
