# M44-WP4 — Renewed Independent Constitutional Contract Review RC2 Record

**Milestone:** M44

**Work package:** M44-WP4 only

**Artifact class:** Independent constitutional contract review record

**Review candidate:** RC2

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

**Prior review record:** [M44-WP4 Independent Constitutional Contract Review RC1](M44_WP4_INDEPENDENT_CONSTITUTIONAL_CONTRACT_REVIEW_RC1.md)

---

## Verbatim issued review body

M44-WP4 — Renewed Independent Constitutional Contract Review RC2
Reviewer role: Renewed independent constitutional contract reviewer
Review class: Read-only, fresh verification of the complete RC2 normative package against the frozen corpus
Serialization review: not performed here
Files modified: NONE
Formal Constitutional Contract Response: read, not accepted as proof; every claim verified independently in the artifacts

Executive Summary
Nine of the ten original findings are fully resolved, and I verified each correction in the artifacts rather than in the response. The routing map is now carried verbatim — a line diff against frozen M44-WP1 §6.5 is clean apart from a trailing blank line, with the M44 authority over it header, the INV-C1 clause, Same as above, and the §6.6 cross-reference all restored, and the disambiguating gloss correctly placed outside the verbatim block. WP4-NR-032 records the own-domain scoping determination normatively and negatively on all six required frozen bases, and expressly states that the non-normative plan is not the source of the boundary. The PC-NGV-11 row now quotes the exact frozen shape including byte encoding and carries the frozen §8.3 specimen-scope basis with M43-WP3 §7.2 as precedent only. Both E-1 limbs are quoted exactly. PC-NGV-01 is re-anchored to WP4-NR-002 and frozen M42-WP7 §4.1 with the container-cannot-verify statement. The ledger ranges reach -06, k and n are bound, and both fixtures carry the encoding-selection note and the unlabelled-specimen bases.

The tenth finding, WP4-CR-J-03, was corrected in a way that removes the inconsistency but crosses the constitutional boundary the whole contract exists to hold. RC2 added WP4-NR-033, which admits ASCII("active"), ASCII("archived"), and ASCII("closed") as the exact F8 bytes. Field 8 is portfolio_lifecycle_state, owned by Ledger & Accounting. Its frozen owning contract, M42-WP6, declares Serialization authority: NONE, places "canonical bytes" expressly out of scope, states at §4.2 that the citation "is a semantic citation coordinate, not a prescribed object, tuple, record, schema, payload, field list, or wire format," and makes prescribing a "canonical byte order" its own non-conforming shape NGV-28. Frozen M44-WP1 §6.2 answers question (c) once for every source-owned coordinate: M44-WP4 "may not author the byte form of any source-owned coordinate's content." WP4-NR-033 authors exactly that.

This is a NEW-CRITICAL. It exceeds the contract's own declared Encoding-selection authority bound, contradicts its preamble and WP4-NR-001, -014, -018, and -028, falsifies the very sentence added to fix WP4-CR-J-02, and inverts WP4-NV-F08 from a guard against this act into an enforcement of it. It does not change G-3, which remains correctly OPEN — PARTIAL, and the correction required is bounded and does not disturb the rest of the grammar: revert F8 to opaque owner-supplied bytes and fix the fixtures' description of the inventory cell instead — which is the branch my original finding named first.

Everything else in RC2 holds. Frozen ownership and co-ownership are preserved exactly, the §6.3 and §6.4 inventory tables remain byte-identical to frozen source, missingness and affirmative absence remain non-colliding, the Benchmark discriminator remains CONSTRAINED — NOT SUPPLIED, all fifteen PC-NGV shapes and checklist items 10–12 retain coverage, the repository boundary is clean, and no confirmation, freeze, or closure is issued.

Original Findings Disposition
Finding	Original severity	Disposition	RC2 evidence	Remaining concern
WP4-CR-J-01	MAJOR	RESOLVED	New WP4-NR-032 (§1.1) resolves the own-domain question in the negative and names all six required bases: frozen M44-WP1 §6.6, frozen M44 §17 OQ-1, M42-WP7 §5 (quoted — "does not define nested field order inside any source-owned coordinate"), M42-WP7 §9 item 11, PC-NGV-14, and INV-C1. States container authority does not become nested amendment authority by ownership of the nested noun, and that the non-normative plan is not the source of the boundary. Carried at §3.3, §7 PC-NGV-14, §8 items 11–12, §8.1, ledger row WP4-NR-032, WP4-PV-AUTH-01, WP4-PV-INV-01, WP4-NV-AUTH-01, WP4-NV-PC-14, WP4-NV-CL-12.	None
WP4-CR-J-02	MAJOR	RESOLVED	§7 PC-NGV-11 quotes the exact frozen shape including "byte encoding", applies the frozen M44 §8.3 specimen-scope basis, identifies WP4 as a downstream container-framing contract under E-1/E-2, and treats frozen M43-WP3 §7.2 as precedent not grant. WP4-NV-PC-11 restated to match.	Its closing sentence — "This contract prescribes no nested-coordinate byte encoding" — is falsified by WP4-NR-033. The defect is in WP4-NR-033, not in this correction; tracked under NEW-CRITICAL-01.
WP4-CR-J-03	MAJOR	PARTIALLY RESOLVED	The inventory cell is preserved verbatim; §3.3 and §10 state field 8 is supplied and not routed; the positive fixture's per-field conclusion now reads "Fields 2–7 and field 10"; WP4-PV-F08 and WP4-NV-F08 were rewritten. The contract/fixture contradiction is gone.	The means is unconstitutional. WP4-NR-033 selects a source-owned byte encoding, failing verification criterion 4 ("no new authority introduced") and creating fresh contradictions with WP4-NR-001, -014, -018, -028, the header bound, the preamble, §7 PC-NGV-08 and PC-NGV-12, and §8 item 11. See NEW-CRITICAL-01.
WP4-CR-N-01	MINOR	RESOLVED	§3.3 now carries frozen M44-WP1 §6.5 verbatim — diff against source lines 506–522 is clean but for one trailing blank line. Header M44 authority over it, the INV-C1 clause, — see §6.6, and Same as above all restored. The §6.6 gloss and the WP4-NR-032 linkage sit outside the verbatim block, which is the correct technique.	None
WP4-CR-N-02	MINOR	RESOLVED	Ledger rows WP4-NR-006 and WP4-NR-024 now read WP4-PV-U32-00–WP4-PV-U32-06; row WP4-NR-007 reads WP4-PV-LP-00–WP4-PV-LP-06. All 35 positive IDs fall inside a ledger range or an explicit reference; negative IDs remain fully symmetric. New rows added for WP4-NR-032 and WP4-NR-033.	None
WP4-CR-N-03	MINOR	RESOLVED	§7 PC-NGV-01 re-anchored to WP4-NR-002 and frozen M42-WP7 §4.1, and states that the opaque-byte container "cannot independently verify semantic coherence across nested bytes" while neither discharging nor weakening the obligation. WP4-NV-PC-01 restated with the matching rows and reason, adding "the byte parser does not claim to detect it independently."	None
WP4-CR-N-04	MINOR	RESOLVED	§1.1 adds the exact second limb — "Their exclusion does not remove or defer the frozen canonical-byte obligation." — verified against frozen M42-WP7 §5, with an explanation of what it defeats. Carried into §8 checklist item 12 and WP4-NV-CL-12.	None
WP4-CR-E-01	EDITORIAL	RESOLVED	Both fixtures retain Encoding-selection authority: NONE and add the note that every grammar element shown derives from the contract's bounded container-level selection and the fixture selects no grammar or encoding.	None
WP4-CR-E-02	EDITORIAL	RESOLVED	§4.4 adds "For every OA_i, k = owner_count_i"; §4.5 adds "For every PA_i, n = item_count_i". Neither envelope otherwise changed.	None
WP4-CR-E-03	EDITORIAL	RESOLVED	Positive fixture §1 adds the intentionally-unlabelled paragraph naming the four bases; §4.1 adds an explicit basis for WP4-PV-OA-01; §7 adds a "Basis for no artificial labels" column; WP4-PV-F09 carries "no synthetic nested bytes".	The basis given for WP4-PV-F08 — "Frozen exact literals" — is only valid if WP4-NR-033 stands. Tracked under NEW-CRITICAL-01.
Constitutional Authority Assessment
The fourteen NONE classes are unchanged across all three artifacts, and Encoding-selection authority remains LIMITED TO THE PORTFOLIO COMPOSITION CONTAINER REPRESENTATION ALLOCATED TO M44-WP4. The extension basis is now complete: E-1 carries both constitutive limbs verbatim, E-2 is exact, E-3 is neither invoked nor available, and WP4-NR-001 rejects declared and undeclared silence. WP4-NR-032 closes the last open authority question by refusing own-domain nested-form authority on frozen grounds. WP4-NR-008 continues to treat frozen M43-WP3 §7.2 as precedent rather than grant.

Against that, WP4-NR-033 sits outside the declared bound. Field 8 is not "the Portfolio Composition container representation"; it is a Ledger & Accounting-owned coordinate carried inside the container. The contract's own preamble promises it "creates no … source-owned coordinate encoding", and WP4-NR-001 promises "Nested source-owned canonical bytes remain opaque." WP4-NR-033 selects US-ASCII, one octet per character, for that coordinate's three frozen state values, and then polices the inside of F8 for "normalization, case-folding, alternate spelling, terminator, padding, or additional framing." A rule that inspects the interior of a field is by definition not treating it as opaque.

The §4.1 primitive definition makes the overreach visible on its own terms: ASCII(s) is defined as the encoding "of the stated fixed contract literal" — a WP4-owned literal such as the schema tag or an owner-domain name. WP4-NR-033 applies that WP4-local primitive to a value the contract does not own.

Architecture-stage versus contract-stage separation remains correct. §1 keeps the WP4 plan non-normative, WP4-NR-032 says so explicitly for the boundary it records, and §12 reserves the point-4 confirmation and records it as not issued.

Frozen Ownership Assessment
Unchanged from RC1 and still exact. §2, the §4.4 envelope table, and WP4-PV-OA-01 agree cell for cell with frozen M44-WP1 §6.3 and frozen M42-WP7 §3, including counts and co-owner order for fields 5 (2), 6 (2), 7 (3), and 10 (2), and the association-only qualifiers on fields 9 and 10. WP4-NR-011 and WP4-NR-013 still deny ownership transfer, and WP4-NV-PC-02 and WP4-NV-F09 still guard it. No owner is added, merged, dropped, renamed, or reordered anywhere in RC2.

WP4-NR-033 does not reassign field 8's ownership — §2 and §3.1 still name Ledger & Accounting, and WP4-PV-OA-01 still attributes field 8 to Ledger & Accounting. The defect is that WP4 exercises a representational power over a coordinate whose owner it correctly names, which is the ownership-preserving form of the same breach PC-NGV-14 describes.

Binding Inventory Assessment
The §3.1 per-field table and the §3.2 facet tables remain byte-identical to frozen M44-WP1 §6.3 and §6.4 — re-verified by diff in this pass. Both axes survive separately for all ten fields; all six field-6 facets, all five field-7 facets, and all three field-10 facets are intact with their notes and frozen evidence. Field 8's cell is untouched and still reads SUPPLIED — EXACT / SUPPLIED — CLOSED LITERAL VOCABULARY. The §3.3 tally is unchanged and correct, and the new field-8 sentence — supplied, not an unsupplied or routed element — is itself faithful to the frozen cell.

§3.3's routing block is now verbatim carriage of frozen §6.5, and WP4-NR-005 still binds both axes without alteration.

The inventory problem in RC2 is not in the carriage but in the reading. Frozen M44-WP1 §6.2 separates three questions and states that separating them "is required, not stylistic." Question (b) asks what written form the reference takes; question (c) asks whether M44-WP4 may supply the byte form. Question (c) is answered once, for every source-owned coordinate, without exception:

"M44-WP4 may therefore frame the container and carry the exact citations; it may not author the byte form of any source-owned coordinate's content."

WP4-NR-033 treats field 8's satisfied (b) as if it also answered (c). It does not. A closed literal vocabulary fixes which values Ledger & Accounting may cite; it does not fix, and M42-WP6 expressly declines to fix, the octets those values become. Collapsing (b) into (c) for one field is precisely the kind of axis-merging WP4-NV-INV-01 exists to reject.

Missingness and Explicit-Absence Assessment
Unchanged and sound. WP4-NR-015, -016, and -027 are identical to RC1: a missing required coordinate has no conforming representation and cannot be empty, zero-length, null, sentinel, omitted, or defaulted; an affirmative owner-defined absence including a valid Explicitly None is a present coordinate carried only by owner-supplied bytes; and WP4 declines to invent those bytes because frozen authority does not supply them. WP4-PV-ABS-01 still proves only the container distinction and still disclaims Benchmark-form, production, and conformance meaning. WP4-NV-MISSING-01 and WP4-NV-ABS-01 are unchanged.

The Benchmark discriminator remains CONSTRAINED — NOT SUPPLIED at §3.2 and WP4-NR-017, with the four frozen labels barred from serialized-tag, runtime, API, database, and implementation-constant use, matching frozen M42-WP5 §4.3. WP4-NV-BENCH-01 and WP4-NV-F07 are intact.

I note the asymmetry WP4-NR-033 creates: WP4-NR-016 refuses to select bytes for Explicitly None because frozen authority does not supply them, while WP4-NR-033 selects bytes for the lifecycle vocabulary on the reasoning that frozen authority supplies the literals. Both nouns have a frozen closed vocabulary and neither owner has published a byte form. The two rules cannot both be right about WP4's power.

G-3 Disposition Assessment
G-3 OPEN — PARTIAL is correct and unchanged, and I re-derived it independently. Axis (a) alone is unsatisfied for portfolio_membership and for the carried Provenance content, so the frozen register §4.3 CLOSED condition — every one of the ten coordinates having an owner-supplied exact immutable canonical reference — fails on the frozen criterion by itself. WP4-NR-030's two-axis field-and-facet rule reaches the same result and matches frozen acceptance criterion 18.

The eight routed elements and their owners are unchanged and correct, WP4-NR-031 preserves the downstream stop without exception, no complete Composition bytes, concrete PMS1, or concrete PAIM1 is claimed, and the §12.1.1 checkpoint outcome is not declared. The register §4.3 citation by path and section is retained. WP4-NV-G3-01, WP4-NV-INCOMPLETE-01, and WP4-NV-DOWNSTREAM-01 are unchanged.

WP4-NR-033 does not alter the gate. Field 8 is not a routed element under either reading, because frozen §6.2 routes on unsatisfied (b) and field 8's (b) is satisfied. Withdrawing WP4-NR-033 therefore requires no change to §3.3, §10, or the terminal state — the correction is confined to how F8 is admitted.

PC-NGV and Checklist Coverage Assessment
All fifteen frozen shapes retain a direct statement and exactly one named negative vector, all defined. No frozen vector is narrowed, dismissed, superseded, or declared inapplicable. PC-NGV-11 through -14 each carry a **Direct:** statement and a dedicated vector, satisfying frozen M44 §8.3 and register §4.3 evidence item (5). PC-NGV-11 and PC-NGV-01 are materially improved and now correct as reasoning. PC-NGV-14 picks up WP4-NR-032. Checklist items 10, 11, and 12 each carry a direct proof and a named vector, and the tag-and-order preservation proof is retained via WP4-PV-PR-01 and WP4-PV-ORD-01. §8.1 adds a useful RC2 findings table.

Three statements in this section are now internally false because of WP4-NR-033, and I record them as evidence for the new finding rather than as separate defects:

§7 PC-NGV-08: "Lifecycle bytes remain opaque" — WP4-NR-033 makes them a closed three-value set with interior checks.
§7 PC-NGV-12: "treat every source field as opaque rather than WP4-normalized" — field 8 is no longer treated that way.
§8 item 11: asserts opacity for source-owned nested bytes and, in the same sentence, that "Field 8 uses only the exact frozen written literals under WP4-NR-033." Frozen checklist item 11 prohibits a source-owned nested coordinate being "reordered, normalized, encoded, or reinterpreted." A rule that names the admitted octets is an encoding of that coordinate, so item 11's proof now contains its own counterexample.
Documentary-Vector Boundary Assessment
The labelling regime is now fully explained and correctly applied. Positive fixture §1 states the synthetic-bytes scope and adds the intentionally-unlabelled paragraph naming the four permitted bases; §4.1 gives WP4-PV-OA-01 its basis; §7 adds a bases column for AUTH-01, INV-01, and M34-01. Every specimen carrying synthetic nested bytes still bears all three labels, and the negative fixture still applies them as a blanket to every input shape and vector ID. The non-effect disclaimers are intact in both fixtures and in the §8 conclusion, and no vector is used to establish source-owner conformance, complete Composition bytes, G-3 closure, a concrete PMS1 or PAIM1, or runtime or production conformance.

The fixtures remain properly subordinate: both declare Encoding-selection authority: NONE with the new derivation note, and §11 still states that vectors derive from normative rows and no normative row derives from a fixture. I confirmed that direction holds for every RC2 addition — WP4-NR-032 and WP4-NR-033 are both authored in the contract first and only then exercised in the fixtures.

The one boundary defect is WP4-NV-F08. In RC1 it rejected the act now performed: "WP4 assumes ASCII bytes for active solely because the literal vocabulary is frozen … WP4 may carry but not author source-owned byte encoding." In RC2 it rejects only deviations from WP4's chosen bytes — ASCII("Active"), ASCII("ACTIVE"), alternate spellings, inner framing. The vector that guarded the boundary now polices compliance with the crossing. WP4-PV-F08's classification changed correspondingly from artificial to "Frozen exact literals; no synthetic nested bytes."

Cross-Artifact Consistency Assessment
Identifiers. WP4-NR-001 through WP4-NR-033 are all defined and all appear in the §11 ledger. Every normative row cited in either fixture resolves. All 49 negative vector IDs are defined and referenced, fully symmetric. All 35 positive vector IDs now fall within a ledger range or an explicit reference; the WP4-CR-N-02 orphans are gone.

Grammar and framing. §4.2, §4.3, §4.4, and §4.5 agree with WP4-PV-PR-01, WP4-PV-ORD-01, WP4-PV-OA-01, and WP4-PV-PA-01. WP4-PV-OA-01 still reproduces u32(10) with ten entries and exact counts; WP4-PV-PA-01 still reproduces u32(7) with entries 2 through 8. The k/n bindings match the fixture specimens. Tag framing, u32/lp primitives, the octet ceiling, ordering, rejection rules, injectivity, and round-trip are identical across all three artifacts.

Status, disposition, ownership. All three carry RC2 status, unconfirmed and unfrozen. G-3 OPEN — PARTIAL is stated identically in the contract §10, positive fixture §7 and §8, and negative fixture §7, and every G-3 effect cell is consistent with it. Missing-element routing is identical between §3.3 and §10. Owner allocations agree everywhere.

Field 8. Contract §4.3, WP4-NR-010, WP4-NR-033, §8.1, §10, WP4-PV-F08, the positive fixture's per-field conclusion, WP4-PV-INV-01, and WP4-NV-F08 are mutually consistent with each other. They are inconsistent with WP4-NR-001, WP4-NR-014, WP4-NR-018, WP4-NR-028, the authority header, the preamble, §7 PC-NGV-08, §7 PC-NGV-11, §7 PC-NGV-12, and §8 item 11 — all of which assert opacity for every source-owned coordinate.

Repository and lifecycle. Clean. Only the three authorized deliverables plus the contract-stage response are new; the other WP4 files are architecture-stage artifacts. No frozen artifact changed, git diff HEAD touches only the architecture plan, and DECISION_LOG.md, INDEX.md, ROADMAP.md, and Graphify are untouched with no reference to the contract. No confirmation, freeze, closure, checkpoint authorization, or downstream release is issued anywhere in the package.

M34-D-0010. Unchanged and correct: exact register title "Decompose the instrument-analysis product contract," the single exact consequence sentence, the frozen M44 §8.3 characterization divergence recorded without correction, WP4-NR-029, WP4-PV-M34-01, and WP4-NV-M34-01 all consistent.

New Findings
NEW-CRITICAL
WP4-CR2-J-04 — WP4-NR-033 authors the byte form of a source-owned coordinate

Severity: NEW-CRITICAL
Affected artifacts and sections: Contract §4.3 (WP4-NR-010, WP4-NR-033), §8 item 11, §8.1, §10; positive fixture §6 (WP4-PV-F08 and per-field conclusion) and §7 (WP4-PV-INV-01); negative fixture §4 (WP4-NV-CL-11) and §5 (WP4-NV-F08)
Explanation. WP4-NR-033 states that "The admitted F8 owner bytes are exactly ASCII("active"), ASCII("archived"), or ASCII("closed")," and forbids normalization, case-folding, alternate spelling, terminator, padding, or additional framing inside F8. Field 8 is portfolio_lifecycle_state, owned by Ledger & Accounting under frozen M42-WP7 §3 and M42-WP6. The frozen owning contract has not published a byte form and expressly declines to: its header declares Serialization authority: NONE; its §2 out-of-scope list names "serialization, canonical bytes, field name, field order, transport"; §4.2 states the citation "is a semantic citation coordinate, not a prescribed object, tuple, record, schema, payload, field list, or wire format"; and NGV-28 makes "a canonical byte order is prescribed" a non-conforming shape in that contract's own negative corpus. Frozen M44-WP1 §6.2 answers question (c) once, for every source-owned coordinate: WP4 "may not author the byte form of any source-owned coordinate's content." The frozen SUPPLIED — CLOSED LITERAL VOCABULARY cell answers question (b) — which values may be cited — and WP4-NR-033 reads it as though it also answered (c). The rule additionally exceeds the contract's own Encoding-selection authority bound, contradicts its preamble and WP4-NR-001, -014, -018, and -028, applies the §4.1 ASCII(s) primitive — defined for "the stated fixed contract literal" — to a value WP4 does not own, and falsifies the sentence added to resolve WP4-CR-J-02 ("This contract prescribes no nested-coordinate byte encoding"). WP4-NV-F08 has been inverted from a guard against this act into an enforcement of it, and WP4-NV-CL-11 now cites -033 as a basis for rejecting departures from WP4's selection.
Constitutional basis. Frozen M42-WP6 header Serialization authority: NONE, §2 out-of-scope list, §4.2, and NGV-28; frozen M44-WP1 §6.2 question (c); frozen M42-WP7 §5 ("does not define nested field order inside any source-owned coordinate") and §9 checklist item 11 ("No source-owned nested coordinate is reordered, normalized, encoded, or reinterpreted"); frozen PC-NGV-14; frozen M44 §5.3 ("M44 defines no nested source-owned encoding, field, schema, or identifier") and INV-C4 ("No M44 artifact reaches upstream"); frozen M44 §8.3 prohibited responsibilities ("defining nested source-owned encoding"); and the contract's own WP4-NR-001, -014, -018, -028, and -032.
Required correction. Withdraw WP4-NR-033. Restore F8 to the treatment every other source-owned coordinate receives: WP4-NR-010 reverts to requiring F2 through F8 to be owner-supplied canonical bytes with no carve-out, and WP4-NR-018 again treats F2–F8 as opaque. Resolve WP4-CR-J-03 on the branch that does not cross the boundary: keep the §3.1 cell verbatim, keep §3.3 and §10 unchanged (field 8 stays supplied and unrouted, because frozen §6.2 routes only on unsatisfied (b)), and correct the fixtures instead — restore WP4-NV-F08 to reject WP4-authored ASCII bytes for active and state in WP4-PV-F08 that field 8's frozen closed vocabulary is carried opaquely as owner-supplied bytes, so the field is neither an unsupplied element nor one WP4 may encode. Revise the positive fixture's per-field conclusion to distinguish the two ideas — "supplied on both frozen axes" and "not WP4-encodable" — rather than treating them as the same property. Remove -033 from §8 item 11, §8.1, WP4-NV-CL-11, and the ledger. Restore §7 PC-NGV-08 and PC-NGV-12 to unqualified accuracy.
Effect on G-3. None. G-3 remains OPEN — PARTIAL before and after the correction, and no routing row or missing-element entry changes.
Blocks final serialization review? The serialization reviewer may proceed on the container grammar, which is otherwise unchanged from RC1, but must be told WP4-NR-033 is under constitutional challenge and treat F8 as opaque. The review cannot become final until the rule is withdrawn.
NEW-MAJOR
NONE

NEW-MINOR
NONE

NEW-EDITORIAL
WP4-CR2-E-04 — Stale RC1 self-reference in §12. The status header, revision note, and both fixtures read RC2, but §12 opens "This RC1 contract and its two documentary fixture artifacts require an independent constitutional contract review…". Correction: update to RC2. No constitutional effect.

Final Determination
Original findings unresolved:

WP4-CR-J-03 (PARTIALLY RESOLVED — corrected in form, unconstitutional in means)
New findings:

WP4-CR2-J-04 (NEW-CRITICAL)
WP4-CR2-E-04 (NEW-EDITORIAL)
Overall Result:

NOT APPROVED

The approval rule is not met on two counts: WP4-CR-J-03 is not fully resolved, and a new constitutional finding exists. G-3 is correctly determined and no ownership, lifecycle, or repository defect remains — the sole substantive blocker is WP4-NR-033.

Contract-stage constitutional review status:

COMPLETE

Independent serialization review:

MAY PROCEED, BUT CANNOT BECOME FINAL UNTIL CONSTITUTIONAL FINDINGS ARE RESOLVED

The tag framing, primitives, top-level order, OA and PA envelopes, injectivity, round-trip, and rejection rules are unchanged from RC1 and stable for review. The serialization reviewer must be informed that WP4-NR-033 is under constitutional challenge and should assess F8 as an opaque owner-supplied byte sequence.

Eligibility for frozen M44 Architecture §12.5 point-4 confirmation:

ELIGIBLE ONLY AFTER DISTINCT INDEPENDENT SERIALIZATION REVIEW

— and only after WP4-CR2-J-04 is corrected, WP4-CR-J-03 is completed on the non-crossing branch, and both receive renewed constitutional review by this discipline. This review issues no confirmation, performs no freeze, and does not close M44-WP4. M44-WP4 remains OPEN AND UNFROZEN; G-3 remains OPEN — PARTIAL; the §12.1.1 checkpoint remains unauthorized and its outcome undeclared.
