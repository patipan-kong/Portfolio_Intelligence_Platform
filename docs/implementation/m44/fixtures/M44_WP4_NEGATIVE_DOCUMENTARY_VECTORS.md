# M44-WP4 — Negative Documentary Vectors

**Milestone:** M44

**Work package:** M44-WP4 only

**Artifact class:** Normative documentary fixture artifact

**Contract:** [M44-WP4 Portfolio Composition Canonical Byte Representation Contract](../../M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md)

**Status:** `RC4 — SERIALIZATION CORRECTED; NOT INDEPENDENTLY SERIALIZATION-APPROVED OR CONFIRMED`

**Constitutional contract review:** `APPROVED` at RC3

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
**Ownership-determination authority:** `NONE`
**Vocabulary-admission authority:** `NONE`
**Encoding-selection authority:** `NONE`

**Fixture encoding-selection note:** NONE — every grammar element shown derives from the contract’s bounded container-level encoding selection; the fixture selects no grammar or encoding.

---

## 1. Fixture boundary and mandatory labels

These vectors are documentary rejection obligations, not executable tests.

The following classification applies separately and exactly to every synthetic
input shape and every vector ID in this artifact:

- `ARTIFICIAL`
- `NON-EFFECTIVE`
- `NON-CONFORMANCE-ESTABLISHING`

No rejected specimen supplies missing owner bytes, proves production
conformance, closes `G-3`, forms complete Composition bytes, forms a concrete
`PMS1` or `PAIM1`, or authorizes implementation.

Every table records the violated normative row, input shape, expected rejection,
constitutional reason, and `G-3` effect.

## 2. Frozen PC-NGV-01 through PC-NGV-15

| Vector | Violated normative row | Input shape | Expected rejection | Constitutional reason | `G-3` effect |
| --- | --- | --- | --- | --- | --- |
| `WP4-NV-PC-01` | `WP4-NR-002`; frozen M42-WP7 §4.1 | Opaque `portfolio_identity` and `accounting_scope` bytes are asserted by their source semantics to denote non-corresponding subjects | Reject the claim at the Portfolio Composition conformance level; the byte parser does not claim to detect it independently | Frozen `PC-NGV-01`: subject coherence remains a semantic obligation; opaque WP4 framing neither verifies, discharges, nor weakens it | No closure; `OPEN — PARTIAL` unchanged |
| `WP4-NV-PC-02` | `WP4-NR-002`, `-003`, `-011`, `-013` | `OA` attributes a Ledger coordinate or Provenance meaning to Portfolio Intelligence | Reject `OA` and the container | Frozen `PC-NGV-02`: ownership leakage; association does not transfer ownership | No closure; ownership defect is independently non-conforming |
| `WP4-NV-PC-03` | `WP4-NR-014`, `-020`, `-026` | A currency alias, provider code, Benchmark alias, or criterion byte sequence is normalized or standardized before framing | Reject the transformed nested bytes | Frozen `PC-NGV-03`: normalization and source-vocabulary theft | No closure; transformed bytes are not owner-supplied |
| `WP4-NV-PC-04` | `WP4-NR-015`, `-027` | A missing field is filled from ambient context, defaulted, inferred, or selected by the container | Reject; no conforming container exists | Frozen `PC-NGV-04`: missing-coordinate invention | Confirms prerequisite failure; remains `OPEN — PARTIAL` |
| `WP4-NV-PC-05` | `WP4-NR-009`, `-021` | An eleventh field carries NAV, price, weight, return, alpha, exposure, rate, or FX-converted value | Reject unknown field and Composition claim | Frozen `PC-NGV-05`: measure/calculation/valuation leakage | No closure; added material cannot discharge missing forms |
| `WP4-NV-PC-06` | `WP4-NR-001`, `-009`, `-021` | Input adds a belonging, eligibility, permission, compatibility, or tradability result | Reject unknown semantic material | Frozen `PC-NGV-06`: rejected Membership or policy leakage | No closure |
| `WP4-NV-PC-07` | `WP4-NR-001`, `-009`, `-021` | Input adds policy, leverage, cash floor, allocation, or execution rules | Reject unknown semantic material | Frozen `PC-NGV-07`: rejected WP4/Decision Intelligence leakage | No closure |
| `WP4-NV-PC-08` | `WP4-NR-014`, `-028` | Opaque owner-supplied lifecycle bytes are decoded as authority to act, as proof of transition/currentness, or as an invitation for WP4 to inspect their internal encoding | Reject the interpretation and conformance claim | Frozen `PC-NGV-08`: lifecycle execution/runtime leakage; field-8 opacity remains intact | No closure |
| `WP4-NV-PC-09` | `WP4-NR-012`, `-013`, `-023` | Provenance is generated, detached, moved to another field, merged, reconstructed, or used as trust evidence | Reject `PA` and the conformance claim | Frozen `PC-NGV-09`: Provenance reconstruction or judgment | No closure; missing owner content remains missing |
| `WP4-NV-PC-10` | `WP4-NR-015`, `-016`, `-027` | Missing Benchmark Declaration is encoded as an empty field or presentation text `Explicitly None` | Reject; missingness is not affirmative absence | Frozen `PC-NGV-10`: missing/absence conflation | Confirms field 7 remains partial |
| `WP4-NV-PC-11` | `WP4-NR-001`, `-006`, `-010`, authority header | The exact frozen shape: “A database, JSON, API, service, runtime object, byte encoding, or storage form is prescribed.” This includes a claim that a C3 Composition specimen prescribes bytes internally, or that the WP4 downstream container contract prescribes a nested-coordinate byte encoding or any runtime, storage, API, JSON, database, service, or implementation form | Reject the authority and Composition-conformance claim; retain only the bounded downstream container framing selected by the contract | Frozen `PC-NGV-11`; frozen M44 Architecture §8.3 C3 prescribes nothing inside a specimen; M44-WP4 is a downstream canonical container-framing contract; frozen M43-WP3 §7.2 is precedent, not authority | No effect on `G-3`; forbidden authority cannot close it |
| `WP4-NV-PC-12` | `WP4-NR-002`, `-003`, `-004`, `-009`, `-014`, `-026` | A producer places semantically field-7 opaque bytes in positional `F6` and semantically field-6 opaque bytes in positional `F7`, or parses source bytes into WP4-normalized subfields | The parser decodes the well-framed swap as a different positional Composition input and cannot reject it mechanically; reject the producer's semantic-conformance claim under frozen subject-coherence obligations, and reject any normalization | Frozen `PC-NGV-12`: producer field-order/meaning reinterpretation remains prohibited; parser observability does not discharge semantic conformance | No closure |
| `WP4-NV-PC-13` | `WP4-NR-004`, `-008`, `-022` | Raw `ASCII("M42-WP7-PORTFOLIO-COMPOSITION-2")`, a length-prefixed correct tag, or any other tag claims conformance | Reject before field decoding | Frozen `PC-NGV-13`: schema reinterpretation; direct §7 proof | No closure |
| `WP4-NV-PC-14` | `WP4-NR-001`, `-010`, `-014`, `-015`, `-017`, `-028`, `-032` | WP4 invents JSON, text, field order, identifier syntax, form-discriminator bytes, or any nested encoding for a source-owned coordinate, including a Portfolio Intelligence-owned frozen coordinate | Reject the nested bytes and complete-container claim | Frozen `PC-NGV-14`: serialization reinterpretation; frozen M42-WP7 §5 and §9 item 11; frozen `INV-C1`; own-domain meaning ownership grants no nested amendment authority | Confirms the unsupplied element; remains `OPEN — PARTIAL` |
| `WP4-NV-PC-15` | `WP4-NR-001`, `-002`, authority header | Composition is asserted to be Ledger truth, a runtime/analytical/valuation/optimization model, policy engine, or recommendation engine | Reject the authority claim | Frozen `PC-NGV-15`: authority leakage | No closure |

## 3. Required container rejection rules

| Vector | Violated normative row | Input shape | Expected rejection | Constitutional reason | `G-3` effect |
| --- | --- | --- | --- | --- | --- |
| `WP4-NV-UNKNOWN-01` | `WP4-NR-009`, `-018`, `-021` | Valid-looking fields 1–10 followed by an eleventh length-prefixed field | Reject unknown field and unread material | Fixed ten-field grammar; unknown fields prohibited | No closure |
| `WP4-NV-TAG-01` | `WP4-NR-008`, `-022` | Correct tag encoded as `lp(ASCII(tag))` instead of 31 raw octets | Reject alternate schema-tag framing | Exactly one admitted tag form | No closure |
| `WP4-NV-ORDER-01` | `WP4-NR-004`, `-009`, `-011`, `-022` | Starting from the exact `WP4-PV-OA-01` bytes, exchange the complete field-2 and field-3 entries so the explicit OA field-number sequence is `1,3,2,4,5,6,7,8,9,10`; the malformed envelope begins `00 00 00 0a 00 00 00 01 ... 00 00 00 03 00 00 00 01 00 00 00 13 4c 65 64 67 65 72 20 26 20 41 63 63 6f 75 6e 74 69 6e 67 00 00 00 02 ...` | Reject when the second OA entry carries explicit field number 3 instead of required field number 2 | The OA field numbers make this order defect mechanically observable; frozen M42-WP7 §5 order remains exact | No closure |
| `WP4-NV-DUP-KEY-01` | `WP4-NR-009`, `-019`, `-023` | A map-like form repeats `portfolio_identity`, or a positional encoding inserts an extra top-level `lp` framing component between the first and second source-coordinate components | Reject duplicate key or structurally excess framing; the positional parser consumes exactly nine top-level components and rejects the resulting OA/PA misparse or unread suffix | Duplicate keys and excess framing components are not admitted | No closure |
| `WP4-NV-DUP-OA-01` | `WP4-NR-011`, `-023` | `OA` repeats field 7 or repeats `Asset Foundation` within field 7 | Reject `OA` | Exact owner count and one association per field | No closure |
| `WP4-NV-DUP-PA-01` | `WP4-NR-012`, `-023` | `PA` repeats coordinate entry 4 or repeats the same Provenance item twice within entry 4 | Reject `PA` | Duplicate association entries are prohibited | No closure |
| `WP4-NV-NUM-01` | `WP4-NR-006`, `-020`, `-024` | Length `1` is encoded as one octet `01`, little-endian `01 00 00 00`, signed text `-1`, or decimal text `1` | Reject non-canonical number | Only four-octet network-byte-order `u32` is admitted | No closure |
| `WP4-NV-LEN-01` | `WP4-NR-007`, `-019`, `-024` | Prefix declares length 2 but only one payload octet follows, or declares 1 and consumes 2 | Reject truncation or length mismatch | `lp` must delimit exactly one byte sequence | No closure |
| `WP4-NV-TRAIL-01` | `WP4-NR-007`, `-018`, `-025` | One `00` octet follows a fully decoded field 10 | Reject trailing byte | Complete input consumption is mandatory | No closure |
| `WP4-NV-UNICODE-01` | `WP4-NR-014`, `-020`, `-026` | Nested bytes are decoded as text then NFC-normalized, case-folded, locale-transformed, or re-encoded | Reject transformed input and conformance claim | Nested bytes are opaque; Unicode ambiguity is prohibited | No closure |
| `WP4-NV-PRESENT-01` | `WP4-NR-014`, `-017`, `-028` | Display name, form label, specimen identifier, provider value, API value, database key, or implementation constant is substituted for owner bytes | Reject substituted value | Presentation text is evidence only, never canonical nested bytes | Usually confirms missing owner form; never closes |
| `WP4-NV-INVENT-01` | `WP4-NR-010`, `-014`, `-028` | WP4 authors a textual or binary nested identifier because the owner supplied none | Reject invented nested encoding | Container authority does not include source-coordinate encoding | Confirms `OPEN — PARTIAL` |
| `WP4-NV-MISSING-01` | `WP4-NR-015`, `-027` | Required field represented as `lp(empty)`, null, sentinel, omission, or inferred default | Reject whole container | Missing required coordinate has no representation | Confirms `OPEN — PARTIAL` |
| `WP4-NV-ABS-01` | `WP4-NR-015`, `-016`, `-027` | Missing Benchmark is encoded as zero length, while zero length is asserted to mean `Explicitly None` | Reject collision | Affirmative absence must be present owner-supplied bytes | Confirms field 7 remains partial |
| `WP4-NV-OWNER-01` | `WP4-NR-010`, `-014` | Nested payload is non-empty but its source owner has not supplied it as canonical bytes | Reject despite syntactic length validity | Non-empty bytes are not sufficient; owner supply is mandatory | Confirms `OPEN — PARTIAL` |
| `WP4-NV-BENCH-01` | `WP4-NR-016`, `-017`, `-028` | ASCII `Single`, `Composite`, `Category`, or `Explicitly None` is used as a serialized discriminator | Reject Benchmark nested bytes | Discriminator is `CONSTRAINED — NOT SUPPLIED`; labels are presentation-only | Confirms field 7 remains partial |

## 4. M42-WP7 checklist items 10–12

| Vector | Violated normative row | Input shape | Expected rejection | Constitutional reason | `G-3` effect |
| --- | --- | --- | --- | --- | --- |
| `WP4-NV-CL-10` | `WP4-NR-003`, `-004`, `-008`, `-009`, `-011`, `-012` | Correct source-coordinate framing with an alternate tag or length-prefixed tag; an omitted, excess, or duplicated top-level framing component; or an explicit OA/PA field-number sequence error | Reject the mechanically malformed tag, component structure, or envelope order | Checklist item 10 requires the exact tag and producer semantic order; parser-visible order rejection is limited to represented structural defects | No closure |
| `WP4-NV-CL-11` | `WP4-NR-010`, `-014`, `-018`, `-032` | Decoder parses, reorders, normalizes, encodes, or reinterprets any source-owned nested coordinate | Reject decoder and conformance claim | Checklist item 11 prohibits those operations; own-domain ownership does not create an exception | No closure; invented form cannot supply evidence |
| `WP4-NV-CL-12` | `WP4-NR-001`, `-002`, `-015`, `-017`, `-032` | A missing nested form is declared removed, deferred, optional, supplied by a label, or unnecessary because M42-WP7 did not encode it | Reject weakened obligation and conformance claim | Checklist item 12 and the second `E-1` limb preserve canonical-byte obligations without invention, removal, deferral, or weakening | Confirms `OPEN — PARTIAL` |

## 5. Per-field negative documentary coverage

| Vector | Violated normative row | Input shape | Expected rejection | Constitutional reason | `G-3` effect |
| --- | --- | --- | --- | --- | --- |
| `WP4-NV-F01` | `WP4-NR-003`, `-004`, `-008` | `schema_version` differs by one octet or uses length-prefix framing | Reject tag | Exact frozen literal and raw framing | No closure |
| `WP4-NV-F02` | `WP4-NR-010`, `-014`, `-028` | Presentation identifier `PI-01` is encoded without owner-supplied canonical bytes | Reject field 2 | Ledger & Accounting supplies no frozen written form | Confirms field-2 gap |
| `WP4-NV-F03` | `WP4-NR-010`, `-014`, `-028` | Presentation identifier `AS-01` is encoded without owner-supplied canonical bytes | Reject field 3 | Ledger & Accounting supplies no frozen written form | Confirms field-3 gap |
| `WP4-NV-F04` | `WP4-NR-010`, `-014`, `-028` | WP4 sorts membership identifiers and serializes the invented set | Reject field 4 | Representation, elements, cardinality, and order are unsupplied | Confirms field-4 gap |
| `WP4-NV-F05` | `WP4-NR-010`, `-014`, `-028` | Display text `USD` is used as Base Currency canonical bytes | Reject field 5 | Exact identifier format is expressly not supplied | Confirms field-5 gap |
| `WP4-NV-F06` | `WP4-NR-010`, `-014`, `-028` | WP4 invents a JSON/envelope/order for the six Investment Universe facets | Reject field 6 | Frozen Stage B supplies no nested form or order | Confirms field-6 gap |
| `WP4-NV-F07` | `WP4-NR-016`, `-017`, `-028` | A frozen Benchmark form label or display `asset_id` is encoded | Reject field 7 | Discriminator and several facet forms are unsupplied | Confirms field-7 partial state |
| `WP4-NV-F08` | `WP4-NR-001`, `-010`, `-014`, `-018` | WP4 assumes or prescribes ASCII bytes for `active`, `archived`, or `closed` solely because the literal vocabulary is frozen | Reject the WP4-authored field-8 encoding claim; the owner-supplied bytes must remain opaque | Semantic vocabulary determinacy does not grant encoding authority; field 8 is source-owned by Ledger & Accounting | No change to `G-3`; field 8 remains supplied and is not routed |
| `WP4-NV-F09` | `WP4-NR-003`, `-011` | `OA` omits Asset Foundation from field 6 or omits the association-only qualifier in the normative allocation | Reject field 9 | Exact co-allocation and role preservation are mandatory | No closure |
| `WP4-NV-F10` | `WP4-NR-012`, `-013`, `-014` | WP4 serializes Provenance from presentation JSON or merges items across coordinates | Reject field 10 | Connectivity & Ingestion content form is unsupplied and opaque | Confirms field-10 gap |

## 6. Inventory, authority, inherited matter, and gate disposition

| Vector | Violated normative row | Input shape | Expected rejection | Constitutional reason | `G-3` effect |
| --- | --- | --- | --- | --- | --- |
| `WP4-NV-AUTH-01` | `WP4-NR-001` | Author relies on constitutional silence or `E-3` to invent a nested form or grant implementation authority | Reject authority basis | `E-1` and `E-2` are exclusive; silence is not authority | No closure |
| `WP4-NV-INV-01` | `WP4-NR-005` | Contract reclassifies a `NOT SUPPLIED` cell as supplied, combines the two axes, removes a facet, or treats a perceived divergence as a WP4 correction | Reject inventory and disposition | Frozen WP1 inventory binds verbatim | Any false closure is invalid; actual state remains partial |
| `WP4-NV-M34-01` | `WP4-NR-029` | Contract retitles `M34-D-0010` as “Provenance association rules,” quotes another consequence, or claims to correct the frozen M44 description | Reject inherited-matter statement | Exact title/consequence and non-correction boundary are required | No closure |
| `WP4-NV-G3-01` | `WP4-NR-005`, `-030` | Artificial mechanics vectors or routing records are cited as owner-supplied evidence and `G-3 CLOSED` is declared | Reject closure determination | Both inventory axes must be supplied at field and facet level; routing and fixtures are not supply | Correct result remains `OPEN — PARTIAL` |
| `WP4-NV-INCOMPLETE-01` | `WP4-NR-015`, `-030`, `-031` | Container omits a missing source field or substitutes artificial bytes, then claims complete Composition bytes | Reject container and completeness claim | A missing required coordinate has no conforming representation | Confirms `OPEN — PARTIAL`; no complete bytes |
| `WP4-NV-DOWNSTREAM-01` | `WP4-NR-031` | Partial or artificial Composition bytes are embedded in a claimed concrete `PMS1` or `PAIM1`, or used to release M44-WP6/WP7 | Reject downstream claim | Frozen M43-WP3 §7.1 and frozen G-3 consequence require fail-closed behavior | No concrete subject/manifest; downstream stop remains |

## 7. Coverage conclusion

Every frozen `PC-NGV-01` through `PC-NGV-15` has a direct named vector.
`PC-NGV-11` through `PC-NGV-14` each has its own direct contract statement and
negative vector. Checklist items 10, 11, and 12 each have a direct contract
proof and named negative vector. Every frozen field has a positive documentary
case and a negative documentary case.

The rejected inputs confirm container boundaries only. They do not alter the
binding inventory or the terminal determination `G-3 OPEN — PARTIAL`, and they
declare no M44 §12.1.1 checkpoint outcome.
