# M44-WP4 — Independent Constitutional Contract Review RC1 Record

**Milestone:** M44

**Work package:** M44-WP4 only

**Artifact class:** Independent constitutional contract review record

**Review candidate:** RC1

**Overall result:** `NOT APPROVED`

**Confirmation issued:** `NO`

**Freeze performed:** `NO`

**WP4 closed:** `NO`

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

## Verbatim issued review body

M44-WP4 — Independent Constitutional Contract Review
Reviewer role: Independent constitutional contract reviewer (fresh session)
Review class: Read-only constitutional review of the RC1 normative package
Artifacts reviewed: the RC1 contract, the positive documentary vectors, the negative documentary vectors, verified directly against the frozen corpus
Serialization review: not performed here
Files modified: NONE

Executive Summary
The RC1 package stays inside M44-WP4 constitutional authority. It defines only the Portfolio Composition container representation, treats every source-owned nested coordinate as opaque, preserves the frozen tag and ten-field order exactly, carries the binding M44-WP1 two-axis inventory verbatim, reaches the correct terminal state G-3 OPEN — PARTIAL, preserves the downstream fail-closed consequence, and asserts no runtime, source-code, persistence, API, UI, provider, production-method, executable-validation, capability-completion, frozen-artifact-amendment, ownership-determination, or vocabulary-admission authority. The single non-NONE class, Encoding-selection authority, is bounded on its face to the container representation allocated to WP4 and is denied for every source-owned nested coordinate by WP4-NR-001, -010, -014, -017, and -028. Repository boundary is clean: only the three authorized deliverables exist, no frozen artifact changed, and no governance record was touched.

I verified the two most falsifiable claims mechanically. Frozen M44-WP1 §6.3 and §6.4 are carried into contract §3.1 and §3.2 byte-identically — a line-level diff of both tables returns no difference. The E-1 and E-2 quotations reproduce frozen M42-WP7 §5 and frozen M43-WP3 §7.1 exactly. M34-D-0010 is cited by its exact register title and the exact consequence sentence.

Three MAJOR findings prevent this RC1 from being confirmable as authored. None is a closure error, an invented encoding, an ownership defect, or a frozen-artifact amendment; G-3 OPEN — PARTIAL is correct and survives all three.

The own-domain nested-form scoping determination is not recorded in the normative instrument. Frozen M44 RC2 §17 OQ-1 assigns that scoping determination to M44-WP4, and frozen M44-WP1 §6.6 refers it by name. The contract resolves it only by implication and never states it, never gives its frozen basis, and actually deletes the pointer to §6.6 when paraphrasing the routing map.
The PC-NGV-11 non-triggering statement omits the one clause the contract's own grammar engages — "byte encoding" — and does not carry the frozen §8.3 non-triggering basis.
The package contradicts itself on field 8. The carried inventory records portfolio_lifecycle_state as supplied on both axes, while WP4-NR-010, WP4-PV-F08, and WP4-NV-F08 treat its byte form as unsupplied — and no §3.3 routing row or §10 missing-element entry names it.
There are no CRITICAL findings, and I found nothing that inflates the lifecycle: each finding names a specific frozen requirement and a bounded correction.

Constitutional Authority Assessment
Authority declarations. Fourteen classes are declared NONE in all three artifacts. Encoding-selection authority is LIMITED TO THE PORTFOLIO COMPOSITION CONTAINER REPRESENTATION ALLOCATED TO M44-WP4 in the contract. That limitation is honoured operatively: §4.3 leaves F2–F8 as opaque owner-supplied byte sequences; §4.4 selects an encoding only for field 9, which frozen M44-WP1 §6.3 row 9 records as "framing … available to M44-WP4 because the element is the container's own"; §4.5 frames the association only and holds every P_i_j opaque. The preamble sentence — "It creates no serializer, executable fixture, runtime behavior, persistence form, API form, production method, or source-owned coordinate encoding" — is consistent with every normative row I checked.

Both fixture artifacts declare Encoding-selection authority: NONE. This is not an inconsistency in substance — the fixtures select nothing and §11 states "Vectors derive from the normative rows above. No normative row derives from a fixture" — but the derivation relationship is left implicit while WP4-PV-OA-01 exhibits a full envelope grammar. Recorded as WP4-CR-E-01.

Extension basis. E-1 and E-2 are named as exclusive, E-3 is not invoked and is affirmatively rejected as an authority route by WP4-NV-AUTH-01, and WP4-NR-001 states plainly that constitutional silence — declared or undeclared — is not authority. Both quotations are exact against source. One limb is missing: frozen M44 §5.3 defines E-1 as a contract that states the conforming conditions and states that its own silence does not extinguish the obligation, and quotes both sentences. The contract quotes only the first. Recorded as WP4-CR-N-04.

Container versus nested authority. Verified affirmatively. The contract defines container tag framing (§4.2), field framing (§4.3), container-owned owner-attribution association (§4.4), and container-owned Provenance-association framing (§4.5), and nothing else. It defines no Portfolio Identity, Accounting Scope, Portfolio Membership, Base Currency, Investment Universe nested, Benchmark nested, Lifecycle State, or Provenance content encoding. WP4-NR-008's treatment of frozen M43-WP3 §7.2 ASCII("PMS1") as "precedent for this decision only; it is not an authority grant" is the correct constitutional posture and matches the E-2 boundary.

Frozen Ownership Assessment
Contract §2 and the §4.4 envelope table were checked field by field against frozen M44-WP1 §6.3 (itself quoting frozen M42-WP7 §3). Every allocation matches, including all co-allocations and their order:

Field	Frozen allocation	§2	§4.4 owner sequence and count	WP4-PV-OA-01
5	Ledger & Accounting — coordinate; Asset Foundation — currency-of-denomination dimension	✓	✓ (2)	✓
6	Portfolio Intelligence — declaration; Asset Foundation — criterion vocabulary	✓	✓ (2)	✓
7	Portfolio Intelligence — declaration; Market Intelligence — series; Asset Foundation — asset_id	✓	✓ (3)	✓
9	Portfolio Intelligence — association only	✓	✓ (1)	✓
10	Connectivity & Ingestion — Provenance meaning and capture; Portfolio Intelligence — association only	✓	✓ (2)	✓
Fields 1–4 and 8 also match. The role qualifiers are retained as normative in §4.4's closing paragraph, so the envelope carries names while §2 carries roles — no qualifier is lost. WP4-NR-011 and WP4-NR-013 state expressly that the envelope creates no shared ownership and transfers no meaning, which satisfies frozen M42-WP7 §5's "neither creates a new owner or Provenance meaning" and §4.2's prohibition on making Portfolio Intelligence a second source. WP4-NV-PC-02 and WP4-NV-F09 give the corresponding rejection shapes.

The ASCII domain-name literals in §4.4 are correctly distinguished from prohibited presentation text: WP4-NR-028 bars presentation text used as canonical nested bytes, and field 9 is container-owned, not nested. That distinction is stated explicitly in §4.4 and is sound.

Binding Inventory Assessment
Verbatim carriage — verified mechanically. Contract §3.1 (lines 133–144) against frozen M44-WP1 §6.3 (lines 433–444): identical. Contract §3.2 (lines 148–176) against frozen §6.4 (lines 474–502): identical. No cell is re-derived, reclassified, widened, narrowed, repaired, simplified, or collapsed; both axes survive separately; all six field-6 facets, all five field-7 facets, and all three field-10 facets are present with their notes and their frozen evidence intact, including the Composite weights — Not applicable row. WP4-NR-005 correctly states that routing records an obligation and does not discharge it, and §3's preamble correctly routes a perceived divergence to contract review rather than to WP4 resolution.

Routing map — paraphrased, not verbatim. Contract §3.3 diverges from frozen §6.5 in three places: the column header reads "WP4 authority over it" where the frozen text reads "M44 authority over it"; the Base Currency owner cell is reformatted; and the Investment Universe row drops "which INV-C1 forbids — see §6.6", with the Benchmark row's "Same as above" expanded in kind. §3 claims verbatim carriage only for §§6.3–6.4, so this is not a false verbatim claim — but frozen M44-WP1 Freeze Record §11.1 makes the pre-inventory binding on WP2–WP7 "as written", and the deleted clause is the pointer to the referred question at the centre of WP4-CR-J-01. Recorded as WP4-CR-N-01.

Tally. §3.3's summary — two satisfied, one partial, seven unsatisfied for axis (b); six source-owned coordinates without a frozen written form; axis (a) additionally unsatisfied for portfolio_membership and the carried Provenance content — reproduces the frozen §6.3 tally exactly, including the correct exclusion of the container-owned field 9 from the six.

Missingness and Explicit-Absence Assessment
WP4-NR-015 states that a missing required coordinate has no conforming byte representation and cannot be empty bytes, zero length, null, a sentinel, an omission, an inferred default, or any invented form, and that no complete conforming Composition byte sequence exists while any required owner bytes are missing. WP4-NR-016 requires an affirmative owner-defined absence — including a valid Explicitly None — to be a present coordinate carried by owner-supplied canonical bytes for that affirmative state, and records that WP4 does not invent those bytes because frozen authority does not supply them. WP4-NR-027 closes the substitution routes at rejection level. This preserves frozen M42-WP7 §4.4 and frozen PC-NGV-10 without weakening.

The container distinction is proved without over-claiming: WP4-PV-ABS-01 establishes only that a present one-octet value is distinct from a missing slot and from lp(empty), and the fixture states in terms that aa "is not a Benchmark form, Explicitly None representation, production value, or source-owner conformance evidence." WP4-PV-LP-00 is careful to admit lp(empty) as valid primitive mechanics while recording that WP4-NR-015 prohibits it as a required coordinate. WP4-NV-MISSING-01 and WP4-NV-ABS-01 supply both rejection directions, and WP4-NV-ABS-01 correctly targets the collision itself rather than the encoding.

No artificial byte anywhere in the package is treated as owner-supplied evidence; WP4-NV-OWNER-01 states directly that syntactic non-emptiness does not satisfy owner supply.

Benchmark discriminator. WP4-NR-017 holds the discriminator at CONSTRAINED — NOT SUPPLIED and bars the four frozen labels from use as serialized tags, runtime discriminators, API values, database values, implementation constants, or canonical bytes. This tracks frozen M42-WP5 §4.3 exactly, including its "serialized tags" clause. Routing is correct on both halves: the nested form to Portfolio Intelligence under frozen M42-WP5, the asset_id lexical form to Asset Foundation. WP4-NV-BENCH-01 and WP4-NV-F07 cover it negatively; WP4-PV-F07 is careful not to use a frozen form label.

G-3 Disposition Assessment
G-3 OPEN — PARTIAL is the correct terminal state and is correctly reached. Under the frozen M44-WP1 register §4.3 permitted-terminal-state definition, CLOSED requires every one of the ten frozen coordinates to have an owner-supplied exact immutable canonical reference; axis (a) alone fails for portfolio_membership and for the carried Provenance content, so OPEN — PARTIAL follows on the frozen criterion by itself. WP4-NR-030's stricter two-axis field-and-facet rule reaches the same result and matches frozen WP4 acceptance criterion 18.

The disposition is stated as exactly one state, never blended with CLOSED, and WP4-NR-030 expressly denies that routing or artificial specimens constitute supply. WP4-NR-031 preserves the downstream consequence without exception, claims no complete Composition bytes, no concrete PMS1, and no concrete PAIM1, declines to declare the §12.1.1 checkpoint outcome, and correctly records that WP4 may complete while G-3 remains partial — which matches the frozen §11 M44-WP4 completion criteria. The exact inherited gate is cited by repository path and section (register §4.3). WP4-NV-G3-01, WP4-NV-INCOMPLETE-01, and WP4-NV-DOWNSTREAM-01 guard closure, completeness, and downstream release respectively.

Missing-element enumeration is incomplete in one respect. §3.3 and §10 name eight elements with their frozen owners, which matches frozen §6.5. But WP4-NR-010 requires owner-supplied canonical bytes for F8, and both fixtures state that field 8's byte form is not owner-supplied — while §3.3 and §10 name no field-8 element and route none. See WP4-CR-J-03. The terminal state is unaffected.

PC-NGV and Checklist Coverage Assessment
All fifteen frozen PC-NGV-01 through PC-NGV-15 receive a direct conformance statement in §7 and exactly one named negative vector each, and every one of those vectors is defined in the negative fixture. No frozen vector is narrowed, dismissed, superseded, or declared inapplicable; §7's opening sentence states this affirmatively. Note that frozen M44 §5.4 enumerates only PC-NGV-01 through PC-NGV-14, so covering all fifteen is a superset and not a defect.

PC-NGV-11 through PC-NGV-14 each carry a Direct: statement and a dedicated negative vector, satisfying the form of frozen M44 §8.3 and register §4.3 evidence item (5). Substantively:

PC-NGV-12 — sound. WP4-NR-003, -004, and -009 do preserve the exact §5 order and do treat every source field as opaque.
PC-NGV-13 — sound. WP4-NR-008 admits exactly one tag form; WP4-NV-PC-13 names the alternate-tag and length-prefixed-tag shapes.
PC-NGV-14 — sound and complete, and correctly extends the prohibition to Portfolio Intelligence-owned frozen coordinates.
PC-NGV-11 — not proved on its own terms. See WP4-CR-J-02.
Checklist items 10, 11, and 12 each have a direct proof and a named negative vector (WP4-NV-CL-10, -11, -12). The tag-and-order preservation proof required by frozen register §4.3 evidence item (7) is present: §8's closing paragraph names WP4-PV-PR-01 and WP4-PV-ORD-01, and the positive fixture §3 states the check concretely — the first 31 octets are raw ASCII("M42-WP7-PORTFOLIO-COMPOSITION-1"), the next nine components are fields 2–10 in frozen order, and decode yields field numbers 1 through 10 exactly with re-encode preserving order. The frozen ten-field list reproduced in the fixture matches frozen M42-WP7 §5 item for item.

One precision defect: §7's PC-NGV-01 statement asserts that "§4 admits only owner-supplied, subject-coherent exact coordinate bytes", but no §4 normative row states a subject-coherence requirement, and the container cannot assess coherence across opaque bytes. Recorded as WP4-CR-N-03.

Documentary-Vector Boundary Assessment
The labelling rule is stated exactly once, in positive-fixture §1, and is scoped: "Every specimen containing synthetic nested bytes is labelled exactly ARTIFICIAL, NON-EFFECTIVE, NON-CONFORMANCE-ESTABLISHING." Applied against that rule, coverage is correct. Every specimen carrying synthetic nested bytes bears all three labels — WP4-PV-LP-01 through -06, ORD-01, PERM-01, OPAQUE-01, ABS-01, RT-01, F02–F08, F10, and the a2/a4_1/a4_2 items inside WP4-PV-PA-01. The unlabelled specimens are correctly outside the rule: the U32 vectors carry no nested bytes; LP-00 carries no payload; PR-01 and F01 are the frozen exact literal, which is genuinely effective; OA-01 and F09 are container-owned association mechanics mirroring the frozen allocation; and AUTH-01, INV-01, M34-01 are documentary reading expectations, not byte specimens. The negative fixture applies the three labels as a blanket to every input shape and every vector ID.

The disclaimers are exact and do the required work. Positive-fixture §1: artificial specimens "do not prove a valid production Composition, source-owner conformance, G-3 closure, complete Composition bytes, a concrete PMS1 subject, or a concrete PAIM1 manifest." §8: agreement between two readers on container mechanics "is never evidence for G-3 closure." Negative-fixture §1 and §7 mirror this and add that no rejected specimen supplies missing owner bytes or authorizes implementation. Hexadecimal is declared documentary notation and A × n is declared not to be an alternate grammar — both necessary, both present. WP4-PV-LP-04 is explicitly "documentary boundary only, not materialized."

I found no vector anywhere in the package used to establish source-owner conformance, effective complete Composition bytes, G-3 closure, a concrete PMS1 or PAIM1, or runtime or production conformance.

Cross-Artifact Consistency Assessment
Normative-row identifiers. WP4-NR-001 through WP4-NR-031 are all defined in the contract and all appear in the §11 coverage ledger, each with positive-or-boundary and negative coverage. Every normative row cited inside either fixture resolves to a defined contract row.

Vector identifiers. All 49 negative vector IDs defined in the fixture are referenced by the contract, and every contract reference resolves — fully symmetric. On the positive side, 35 IDs are defined but the §11 ledger's range notation stops at -04, leaving WP4-PV-U32-05, WP4-PV-U32-06, WP4-PV-LP-05, and WP4-PV-LP-06 outside the ledger. Each still maps back to a normative row inside the fixture (WP4-NR-006/-024 and WP4-NR-007), so the derivation principle holds and no rule is inferred from a fixture; the ledger is simply incomplete. Recorded as WP4-CR-N-02.

Grammar, framing, counts, order. WP4-PV-OA-01 reproduces §4.4 exactly — u32(10), ten entries in field order, owner counts 1,1,1,1,2,2,3,1,1,2, co-owner sequences matching the §4.4 table cell for cell. WP4-PV-PA-01 reproduces §4.5 exactly — u32(7) and seven entries for fields 2 through 8 in frozen order. Field framing, tag framing, and the u32/lp primitives are stated identically across all three artifacts. WP4-NR-010's 4,294,967,295-octet ceiling agrees with WP4-PV-U32-04 and WP4-PV-LP-04.

Status, disposition, authority. All three artifacts carry RC1 status, unconfirmed and unfrozen. G-3 OPEN — PARTIAL is stated identically in the contract §10, positive fixture §7 and §8, and negative fixture §7, and every negative vector's G-3 effect column is consistent with it. Missing-element routing is identical between §3.3 and §10.

Contradictions. One: the field-8 treatment described under WP4-CR-J-03. No other vector contradicts the contract, and apart from the field-8 gap I found no contract obligation lacking vector coverage.

Lifecycle and repository boundary. git status shows exactly the three authorized deliverables plus the m44/fixtures/ directory as new, and one modified tracked file — the architecture plan, which belongs to the already-confirmed planning stage. No frozen artifact changed. DECISION_LOG.md, INDEX.md, ROADMAP.md, and Graphify are untouched, and none references the contract. The contract issues no confirmation, performs no freeze, closes no work package, authorizes no checkpoint, and releases no downstream work package. §12 correctly reserves M44_WP4_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md as the frozen §12.5 point-4 confirmation, records it as not issued, and states that the architecture-stage confirmation does not substitute for it.

Findings
CRITICAL
NONE

MAJOR
WP4-CR-J-01 — The own-domain nested-form scoping determination is not recorded in the normative contract

Severity: MAJOR
Affected artifact and section: Contract §1.1, §3.3, §5 (WP4-NR-017), §10 — the resolution is absent throughout
Explanation. Frozen M44 RC2 §17 OQ-1 sets a decision deadline "Before M44-WP4 begins for the scoping question," and frozen M44-WP1 §6.6 refers the question by name: may M44-WP4 supply the nested forms for the Investment Universe Declaration and the three unsupplied Benchmark Declaration facets merely because Portfolio Intelligence owns those coordinates? §6.6 sets out frozen text on both sides and states that it "does not resolve it," assigning resolution to M44-WP4 under its own independent confirmation. The RC1 contract answers the question only by implication — through the §3.3 routing cells and WP4-NR-017 — and never states the answer, never names the question, and never gives its frozen basis. It also deletes the "see §6.6" pointer when paraphrasing the routing map, so a reader of the contract alone cannot tell the question was ever put. The determination therefore exists today only in the confirmed WP4 architecture plan, which the contract itself declares non-normative planning guidance at §1.
Constitutional basis. Frozen M44 RC2 §17 OQ-1; frozen M44-WP1 §6.6; frozen M44-WP1 Freeze Record §11.1 (the pre-inventory binds WP2–WP7 "as written"); confirmed WP4 architecture §15 item 1 and acceptance criterion 21, which require the contract to record the resolution and independent review to confirm it.
Required correction. Add an express normative statement resolving the question in the negative, supported directly from the frozen sources: M42-WP7 §5's "any source-owned coordinate," M42-WP7 §9 checklist item 11's unqualified use of "source-owned," PC-NGV-14, and frozen M44 INV-C1. State that the ownership domain of a nested noun does not convert container authority into amendment authority. Cite frozen M44-WP1 §6.6 and frozen RC2 §17 OQ-1 by path and section.
Blocks final serialization review? No. This is purely constitutional and does not touch the grammar. It does block §12.5 point-4 confirmation.
WP4-CR-J-02 — The PC-NGV-11 non-triggering statement omits the "byte encoding" clause and the frozen non-triggering basis

Severity: MAJOR
Affected artifact and section: Contract §7, PC-NGV-11 row; negative fixture §2, WP4-NV-PC-11
Explanation. Frozen PC-NGV-11 names seven prescribed shapes: "A database, JSON, API, service, runtime object, byte encoding, or storage form is prescribed." The contract's Direct statement enumerates database, JSON, API, service, runtime-object, storage, executable, persistence, and implementation authority — and omits "byte encoding," which is the single clause the WP4 container grammar actually engages. WP4-NV-PC-11 repeats the omission, substituting "byte-storage form." Frozen M44 §8.3 supplies the argument the contract needs and the contract does not reproduce it: that PC-NGV-11 governs the shape of a conforming Composition specimen, which must remain representation-free; that C3 prescribes nothing inside a specimen; and that a downstream contract may define canonical byte framing, as frozen M43-WP3 §7.2 already does for PMS1 while embedding lp(portfolio_composition_canonical_bytes). As written the row asserts non-triggering by enumerating around the triggering term rather than proving it, which does not meet the frozen standard "C3 is not conforming unless it proves, vector by vector."
Constitutional basis. Frozen M42-WP7 §8 PC-NGV-11; frozen M44 §8.3 required conformance proofs; frozen M44-WP1 register §4.3 evidence item (5); frozen M44 §5.4, which forbids reading any frozen vector as narrowed.
Required correction. Restate the PC-NGV-11 row to address "byte encoding" expressly and to carry the frozen §8.3 non-triggering basis — specimen-scope reading plus the frozen M43-WP3 §7.2 precedent — while retaining the existing authority denials. Align WP4-NV-PC-11's input shape with the frozen wording.
Blocks final serialization review? No, but the serialization reviewer should be told this row is under correction, since the corrected text will characterize what the grammar is.
WP4-CR-J-03 — Field 8 is treated inconsistently across the contract and the fixtures, and its byte form is neither named nor routed

Severity: MAJOR
Affected artifacts and sections: Contract §3.1 row 8, §3.3, §4.3 (WP4-NR-010), §10; positive fixture §6 (WP4-PV-F08 and the closing paragraph); negative fixture §5 (WP4-NV-F08)
Explanation. The carried binding inventory records portfolio_lifecycle_state as SUPPLIED — EXACT on axis (a) and SUPPLIED — CLOSED LITERAL VOCABULARY on axis (b) — exactly active, archived, closed. Consistent with that, §3.3 counts field 8 among the two satisfied fields and neither §3.3 nor §10 routes anything for it. But WP4-NR-010 requires F8 to be owner-supplied canonical bytes; WP4-PV-F08 frames field 8 as artificial and states "WP4 does not select its source-owned byte encoding"; WP4-NV-F08 rejects an ASCII encoding of active "absent owner-supplied canonical bytes"; and the positive fixture's §6 closing sentence places fields 2–8 among those "not presently constitutionally representable as effective complete nested canonical content under the binding WP1 inventory" — grounding the claim in the very inventory that records field 8 as supplied on both axes. The package therefore holds both that field 8's written form is determinate and that field 8 has no owner-supplied canonical byte form, and if the latter reading is correct, the §3.3 routing table and the §10 missing-element list are incomplete: the octet-encoding element for the frozen lifecycle vocabulary is unnamed and unrouted to Ledger & Accounting. Review directive 9 requires the package to name every missing element and its frozen owner.
Constitutional basis. Frozen M44-WP1 §6.3 row 8 and §6.5; WP4-NR-005 (the inventory binds without alteration and may not be reclassified); frozen M44-WP1 register §4.3 evidence item (1); confirmed WP4 acceptance criterion 19.
Required correction. Choose one reading and make all three artifacts consistent with it. If field 8's octet encoding is a source-owned selection WP4 may not make — which the fixtures assert and which WP4-NR-010 implies — add that element to §3.3 and to §10 routed to Ledger & Accounting, and restate the positive fixture's §6 closing sentence so it no longer attributes the non-representability of field 8 to an inventory cell that records it as supplied. If instead field 8 is representable, reconcile WP4-PV-F08 and WP4-NV-F08 accordingly. Either way, do not alter the carried inventory cell.
Blocks final serialization review? No. G-3 OPEN — PARTIAL is unaffected under either reading. The correction changes the missing-element enumeration, not the grammar.
MINOR
WP4-CR-N-01 — §3.3 paraphrases the frozen §6.5 routing map and drops a substantive clause.
Contract §3.3 changes the frozen column header from "M44 authority over it" to "WP4 authority over it", reformats the Base Currency owner cell, and drops "which INV-C1 forbids — see §6.6" from the Investment Universe row (expanding the Benchmark row's "Same as above" in kind). §3 claims verbatim carriage only for §§6.3–6.4, so no false claim is made, but §1 cites §§6.3–6.7 as binding and frozen M44-WP1 Freeze Record §11.1 binds the pre-inventory "as written". The dropped clause is also the pointer to WP4-CR-J-01. Correction: carry §6.5 verbatim, or state expressly that §3.3 is a restatement, retain the INV-C1 reference, and preserve the §6.6 cross-reference. Does not block final serialization review.

WP4-CR-N-02 — Four positive vectors fall outside the §11 coverage-ledger ranges.
WP4-PV-U32-05, WP4-PV-U32-06, WP4-PV-LP-05, and WP4-PV-LP-06 are defined in the positive fixture but excluded by the ledger's -00–-04 range notation. Each maps back to a normative row within the fixture, so no rule derives from a fixture, but the ledger is not bidirectionally complete as frozen register §4.3 evidence item (6) and frozen M44 §12.7 step 3 contemplate. Correction: extend the two ranges to -06, or remove the four vectors. Does not block final serialization review.

WP4-CR-N-03 — §7's PC-NGV-01 statement attributes subject coherence to §4, which states no such rule.
The row reads "§4 admits only owner-supplied, subject-coherent exact coordinate bytes", but no §4 normative row imposes subject coherence, and the container cannot assess it across opaque bytes. The correct basis is WP4-NR-002, which preserves frozen M42-WP7 §4.1. Correction: re-anchor the row on WP4-NR-002 and state that the subject-coherence obligation remains with frozen M42-WP7 §4.1 and is neither discharged nor verifiable at container level. Does not block final serialization review.

WP4-CR-N-04 — §1.1 quotes only one of E-1's two constitutive limbs.
Frozen M44 §5.3 defines E-1 as a frozen contract that states the conforming conditions and states that its own silence on mechanism does not extinguish the obligation, and quotes both sentences from M42-WP7 §5. The contract quotes the first only, omitting "their exclusion does not remove or defer the frozen canonical-byte obligation" — the limb that defeats a silence-based reading and that frozen R-15 identifies as the recurring failure mode. Correction: quote the preservation sentence alongside the conditional-permission sentence under E-1. Does not block final serialization review.

EDITORIAL
WP4-CR-E-01 — Both fixtures declare Encoding-selection authority: NONE while exhibiting the container grammar the contract's bounded authority selects. The relationship is correct and §11 states the derivation direction, but a one-line note in each fixture header ("NONE — every grammar element shown derives from the contract's bounded selection") would remove the apparent conflict at a glance.

WP4-CR-E-02 — The §4.4 and §4.5 productions introduce k and n without binding them to owner_count_i and item_count_i. WP4-NR-011 and WP4-NR-012 fix the counts, so no ambiguity survives a full read; the productions should nonetheless be self-contained.

WP4-CR-E-03 — Positive-fixture §1 scopes the three-label rule to "specimens containing synthetic nested bytes." That scoping is coherent and correctly applied, but the exclusion of WP4-PV-OA-01, WP4-PV-F09, WP4-PV-AUTH-01, WP4-PV-INV-01, and WP4-PV-M34-01 would be easier for an independent reader to verify if each unlabelled specimen carried a one-word basis for its exclusion.

Final Determination
Unresolved findings:

WP4-CR-J-01 (MAJOR)
WP4-CR-J-02 (MAJOR)
WP4-CR-J-03 (MAJOR)
WP4-CR-N-01 (MINOR)
WP4-CR-N-02 (MINOR)
WP4-CR-N-03 (MINOR)
WP4-CR-N-04 (MINOR)
WP4-CR-E-01, WP4-CR-E-02, WP4-CR-E-03 (EDITORIAL)
Overall Result:

NOT APPROVED

Contract-stage constitutional review status:

COMPLETE

Independent serialization review:

MAY PROCEED, BUT CANNOT BECOME FINAL UNTIL CONSTITUTIONAL FINDINGS ARE RESOLVED

None of the ten findings changes the container grammar, the tag framing, the field order, the primitives, the association envelopes, the rejection rules, or the terminal G-3 state, so the serialization reviewer can work against the RC1 grammar as authored. The reviewer should be told that WP4-CR-J-02 will change how §7 characterizes that grammar and that WP4-CR-J-03 may add one routed element to §3.3 and §10.

Eligibility for frozen M44 Architecture §12.5 point-4 confirmation:

ELIGIBLE ONLY AFTER DISTINCT INDEPENDENT SERIALIZATION REVIEW

— and, additionally, only after the findings above are resolved and receive renewed constitutional review by this discipline. This review issues no confirmation, performs no freeze, and does not close M44-WP4. M44-WP4 remains OPEN AND UNFROZEN; G-3 remains OPEN — PARTIAL; the §12.1.1 checkpoint remains unauthorized and its outcome undeclared.
