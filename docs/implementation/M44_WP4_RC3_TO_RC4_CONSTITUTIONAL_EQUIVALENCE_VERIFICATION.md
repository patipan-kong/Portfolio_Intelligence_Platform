# M44-WP4 — RC3-to-RC4 Constitutional Equivalence Verification

**Milestone:** M44

**Work package:** M44-WP4 only

**Artifact class:** Independent constitutional equivalence verification record

**Compared candidates:** RC3 constitutionally approved package and RC4 final package

**Overall result:** `CONSTITUTIONALLY EQUIVALENT`

**Point-4 eligibility:** `ELIGIBLE`

**Confirmation issued:** `NO`

**Freeze performed:** `NO`

**WP4 closed:** `NO`

**G-3:** `OPEN — PARTIAL`

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

**Review chain:**

- [M44-WP4 Renewed Independent Constitutional Contract Review RC3](M44_WP4_RENEWED_INDEPENDENT_CONSTITUTIONAL_CONTRACT_REVIEW_RC3.md)
- [M44-WP4 Independent Serialization Review RC3](M44_WP4_INDEPENDENT_SERIALIZATION_REVIEW_RC3.md)
- [M44-WP4 Formal Serialization Response](M44_WP4_FORMAL_SERIALIZATION_RESPONSE.md)
- [M44-WP4 Renewed Independent Serialization Review RC4](M44_WP4_RENEWED_INDEPENDENT_SERIALIZATION_REVIEW_RC4.md)
- [M44-WP4 Portfolio Composition Canonical Byte Representation Contract](M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md)
- [M44-WP4 Positive Documentary Vectors](m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md)
- [M44-WP4 Negative Documentary Vectors](m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md)

---

## Verification Scope

Fresh, read-only verification of whether the RC3 package that received APPROVED independent constitutional contract review, and the final RC4 package, are constitutionally equivalent. No repository files were created, modified, staged, or committed. No confirmation is issued by this verification.

## Artifacts Examined

M44_WP4_INDEPENDENT_CONSTITUTIONAL_CONTRACT_REVIEW_RC1.md
M44_WP4_RENEWED_INDEPENDENT_CONSTITUTIONAL_CONTRACT_REVIEW_RC2.md
M44_WP4_RENEWED_INDEPENDENT_CONSTITUTIONAL_CONTRACT_REVIEW_RC3.md
M44_WP4_FORMAL_CONSTITUTIONAL_CONTRACT_RESPONSE.md
M44_WP4_INDEPENDENT_SERIALIZATION_REVIEW_RC3.md
M44_WP4_FORMAL_SERIALIZATION_RESPONSE.md
M44_WP4_RENEWED_INDEPENDENT_SERIALIZATION_REVIEW_RC4.md
M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md (current/RC4 candidate, read directly — not inferred from responses)
m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md (current/RC4 candidate)
m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md (current/RC4 candidate)

Because the working tree holds only the current (final) state of the contract and both fixtures — there is no separately preserved RC3 snapshot of these three files, and no prior git commit to diff against — the RC3-to-RC4 change inventory below is reconstructed by cross-checking the current file content directly against what the RC3 constitutional review and the RC3 serialization review each recorded as true of the RC3 package, and against what the Formal Serialization Response claims changed. Every change claim was checked against the current artifact text itself, not accepted from the response alone.

## RC3-to-RC4 Change Inventory

| Artifact and section | Change summary | Classification | Constitutional effect |
| --- | --- | --- | --- |
| Contract §5 (WP4-NR-022), PC-NGV-10/12 rows, checklist item 10 | Text narrowed from an implied byte-level rejection of semantic F2/F3 payload swaps to an explicit statement that parser-visible order defects are limited to malformed framing and explicit OA/PA field-number sequence errors, and that opaque F2–F8 semantic misassignment is not independently observable | SERIALIZATION-MECHANICAL ONLY | None — clarifies parser capability, does not alter grammar, ownership, or authority |
| Negative vectors, WP4-NV-ORDER-01 | Rewritten from a semantic F2/F3 payload-swap test to an explicit, reproducible OA field-number order defect (order 1,3,2,4,5,6,7,8,9,10), with an exact byte fragment | SERIALIZATION-MECHANICAL ONLY / DOCUMENTARY-PROOF ONLY | None — corrects a non-mechanically-rejectable test to a mechanically valid one; no grammar or authority change |
| Positive vectors §5.1, §4.1, §4.2 | a2, a4_1, a4_2 assigned exact octets; OA (440 octets) and PA (77 octets) expanded to exact byte payloads; one complete 591-octet stream with exact input/decode/re-encode equality supplied | DOCUMENTARY-PROOF ONLY | None — makes an existing proof reproducible; introduces no new grammar, field identifier, or encoding rule |
| Contract §12, header Revision/Status lines | RC3 — CORRECTED... → RC4 — SERIALIZATION CORRECTED...; explicit statement that RC4 "preserves the approved RC3 constitutional contract review result" | EDITORIAL ONLY | None |
| Contract §8.1 heading | "Additional RC3 conformance findings" → "Additional RC4 conformance findings"; content (own-domain scoping, field-8 boundary) unchanged | EDITORIAL ONLY | None |

No change was classified:

`CONSTITUTIONALLY MATERIAL`

No change touches: the 31-octet schema tag, the ten-field order, u32/lp primitives, the OA/PA productions or their counts, field ownership/co-ownership, WP4-NR-010/-014/-018 (F2–F8 opacity), WP4-NR-032 (own-domain boundary), the binding inventory carriage, the Benchmark discriminator, missingness/affirmative-absence treatment, or G-3.

## SER-001 Equivalence Assessment

Verified directly against the current contract and negative vectors, not merely against the response's claim:

- Top-level emitted grammar (raw tag + nine lp components in fixed order) is unchanged — confirmed by reading §4/§5 of the current contract.
- Fixed positional order and the producer's obligation to supply the frozen semantic order are preserved (WP4-NR-004, -009, checklist item 10).
- The correction is confined to characterizing parser observability: an opaque F2–F8 semantic misassignment is now expressly stated as unobservable, which is a description correction, not a capability change — no prior text in the approved RC3 constitutional record claimed such a swap was mechanically rejectable at the byte level.
- No field identifier is introduced into F2–F8; both remain positionally opaque, length-prefixed values.
- Ownership, authority, inventory, vocabulary, missingness, and G-3 are untouched by this correction; the current contract's ownership/inventory tables were independently checked above and match what RC1–RC3 constitutional reviews recorded as frozen-identical.
- WP4-NV-ORDER-01's replacement (unobservable payload-content swap → observable OA field-number order defect) is a documentary/mechanical test correction: I confirmed the replacement vector's byte fragment actually encodes field-number 3 in the position where 2 is required, which is a structurally detectable defect, consistent with the claim.

Classification: SERIALIZATION-MECHANICAL / DOCUMENTARY-PROOF ONLY. No constitutionally material effect.

## SER-002 Equivalence Assessment

Verified by decoding the actual byte stream in the current positive vectors, independent of the response's arithmetic claims:

- a2 = a2, a4_1 = a4 01, a4_2 = a4 02 are assigned exact octets in §5.1/§4.2 of the positive vectors.
- The OA payload's length prefix (00 00 01 b8 = 440 decimal) and PA payload's length prefix (00 00 00 4d = 77 decimal) were decoded by hand from the current fixture and match the review's stated 440/77 exactly.
- Byte-offset arithmetic recomputed independently: 31 (tag) + 7×5 (F2–F8 as lp fields) = 66; 66 + 444 (lp(OA) = 4-byte prefix + 440-byte payload) = 510; 510 + 81 (lp(PA) = 4 + 77) = 591 — matches the RC4 serialization review's offset table exactly and matches the actual 591-octet stream printed in the fixture.
- The OA payload's internal structure (owner count 10, owner counts per field 1,1,1,1,2,2,3,1,1,2) was decoded by hand from the raw bytes and matches the frozen ownership table verified across all three constitutional review candidates.
- The PA payload's internal structure (count 7, item counts 1,0,2,0,0,0,0 across fields 2–8) was decoded by hand and matches the review's claim.
- Round-trip is asserted as encode(decode(stream)) = stream for the single 591-octet specimen; this is internally consistent with the printed bytes.
- No artificial byte is asserted as owner-supplied canonical content — the fixture explicitly disclaims source-owner conformance, G-3 closure, complete production Composition bytes, concrete PMS1, and concrete PAIM1.
- No normative grammar, owner allocation, source-owned opacity, missingness treatment, or G-3 statement changed as part of this correction.
- No implementation or runtime authority is introduced; all fifteen authority-class declarations in the RC4 serialization review remain NONE.

Classification: DOCUMENTARY-PROOF ONLY. No constitutionally material effect.

## Constitutionally Material Invariants

All 29 required invariants were checked directly against the current contract text (not the response), cross-referenced to the RC3 constitutional review's record of what RC3 approved:

1–4 (authority declarations, bounded encoding-selection authority, E-1/E-2 exclusivity, silence-is-not-authority) — unchanged; WP4-NR-001 and the header authority block are identical in substance to RC3.

5–7 (exact tag, ten-field order, frozen field names) — unchanged; §4 framing rules unaltered.

8 (frozen ownership/co-ownership) — unchanged; §2/§4.4 owner table re-verified against the frozen counts (1,1,1,1,2,2,3,1,1,2) by direct byte decode above.

9–10 (F2–F8 opaque, no source-owned nested encoding authored by WP4) — unchanged; WP4-NR-010, -014, -018 still require F2–F8 as owner-supplied opaque bytes with no carve-out; WP4-NR-033 (the RC2 regression admitting ASCII lifecycle literals) does not appear anywhere in the current contract or either fixture — confirmed by repository-wide search; it survives only inside the historical RC2/RC3 review records and the response, where it is correctly recorded as withdrawn.

11 (own-domain determination in WP4-NR-032) — present and unchanged (contract lines 104, 242, 536, 580, 639).

12–14 (WP1 inventory carriage, both axes, field/facet classifications) — unchanged; §3.1/§3.2 unaltered by this correction set.

15–16 (field 8 supplied/unrouted/opaque; Benchmark discriminator CONSTRAINED — NOT SUPPLIED) — unchanged; §8.1's "Field 8 boundary" row is identical in substance to the RC3-approved text, only the section heading's revision label changed.

17 (missingness vs. affirmative absence) — unchanged.

18 (PC-NGV-01–15) — unchanged in substance; only PC-NGV-10/12's parser-observability wording was clarified, which does not narrow, dismiss, or supersede the vector.

19 (checklist items 10–12) — item 10's text was clarified per the SER-001 correction; items 11–12 unchanged.

20 (M34-D-0010 inherited treatment) — unchanged.

21 (G-3: OPEN — PARTIAL) — unchanged, stated identically throughout.

22–24 (no complete effective Composition bytes, no concrete PMS1/PAIM1) — unchanged; the RC4 serialization review and current fixtures both retain the disclaimer.

25–28 (§12.1.1 not dispositioned, WP6/WP7 not authorized, WP4 open and unfrozen) — unchanged; stated identically in the current contract §12 and the RC4 serialization review.

29 (no implementation/runtime/etc. authority) — unchanged; all fifteen authority classes remain NONE in every artifact examined.

All 29 invariants preserved.

## Grammar Identity Assessment

Compared directly against the current contract's own text (tag, F2–F8 framing, OA/PA productions, u32, lp, top-level order, counts, complete-consumption rule, trailing-byte rejection) and against what the RC1–RC3 constitutional reviews each independently re-verified as identical to the frozen source. No structural difference found. The Formal Serialization Response's own claim ("Grammar changed: NO" for both corrections) is corroborated by direct inspection, not merely accepted.

Emitted grammar changed:
NO

## Authority Regression Assessment

Checked specifically for: softened authority language, new encoding claims, fixture-derived normative rules, artificial bytes promoted to effective evidence, altered ownership/inventory wording, altered G-3 language, altered downstream stop, newly authorized implementation/runtime behavior, stale RC3 references misidentifying the final candidate, and contradictions between RC4 status and recorded review history.

- WP4-NR-033 and the ASCII lifecycle literals (active/archived/closed) do not reappear in the current contract or fixtures — no regression of the RC2 defect.
- Encoding-selection authority remains bounded to the WP4-owned container representation in the current contract's header, identical to RC3.
- No fixture-derived rule was found; §11's derivation direction (rules → fixtures, never the reverse) holds for every changed vector.
- No artificial byte is claimed as effective evidence anywhere in the current fixtures.
- G-3 language is stated identically (OPEN — PARTIAL) in the contract, both fixtures, and the RC4 serialization review.
- The downstream stop (no complete Composition bytes, no concrete PMS1/PAIM1, §12.1.1 undeclared, WP6/WP7 blocked) is repeated without exception in the current contract §12.
- One stale-reference item, found and judged non-material: §8.1's heading was "Additional RC3 conformance findings" per the RC3 constitutional review and now reads "Additional RC4 conformance findings" in the current contract — this is the expected revision-label update, not a misidentification, since the content under that heading is unchanged.
- No contradiction found between the current RC4 status declarations and the recorded RC1→RC2→RC3 constitutional review history or the RC3→RC4 serialization review history.

## G-3 and Downstream Assessment

G-3 is stated as OPEN — PARTIAL identically across the current contract, both current fixtures, and the RC4 serialization review. No routing row, missing-element entry, or terminal-state determination changed between RC3 and RC4. The downstream stop (§12.1.1 undeclared, M44-WP6/M44-WP7 blocked, no complete Composition bytes, no concrete PMS1/PAIM1) is preserved without exception.

## Findings

### CRITICAL
NONE

### MAJOR
NONE

### MINOR
NONE

### EDITORIAL

Contract §12 revision/status line and §8.1 heading updated from RC3 to RC4 labeling — expected lifecycle bookkeeping, no constitutional or grammar effect.

## Final Determination

Constitutional equivalence findings unresolved:
NONE

Emitted grammar changed:
NO

RC3 constitutional approval applicable to RC4:
YES

Overall Result:

CONSTITUTIONALLY EQUIVALENT

Requirement for renewed full RC4 constitutional review:

NOT REQUIRED

Eligibility for frozen M44 Architecture §12.5 point-4 confirmation:

ELIGIBLE

G-3 status:

OPEN — PARTIAL

M44-WP4 status:

OPEN AND UNFROZEN

This verification issues no point-4 confirmation, performs no freeze, performs no closeout, does not disposition §12.1.1, and authorizes no implementation, runtime, M44-WP6, or M44-WP7. No repository file was created, modified, staged, or committed in the course of this verification.
