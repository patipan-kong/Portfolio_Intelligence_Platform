# M44-WP4 — Portfolio Composition Canonical Byte Representation Contract — Architecture and Implementation Plan

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics
Foundation

**Work package:** M44-WP4 only

**Artifact class:** Non-normative additive architecture and implementation
planning artifact

**Status:** `RC4 — REVIEW RECORDS COMPLETED AND PATHS PINNED AFTER RENEWED INDEPENDENT CONSTITUTIONAL ARCHITECTURE
REVIEW; SUBMITTED FOR RENEWED INDEPENDENT REVIEW`

**Revision:** RC4. Supersedes RC3 in full upon successful renewed independent
constitutional architecture review. RC4 preserves the approved WP4 architecture
and applies only the record-chain and path-pinning corrections recorded in
[M44-WP4 Formal Constitutional Response](M44_WP4_FORMAL_CONSTITUTIONAL_RESPONSE.md).

**Governing frozen authority:**
[M44 Architecture and Implementation Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
(RC2), `COMPLETE AND FROZEN` under
[M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md), and the
binding frozen M44-WP1 evidence established by
[M44-WP1 Freeze Record](M44_WP1_FREEZE_RECORD.md) §11.1

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

This artifact is additive, unenumerated planning material outside the frozen
M44 §11 normative deliverable grant. It asserts no authority, adds no normative
row, and will be superseded in full by the independently confirmed WP4
Portfolio Composition canonical-byte contract. Its recommendation does not
authorize documentary implementation until renewed review accepts RC4.

---

## Executive summary

M44-WP4 is a documentary, non-runtime Portfolio Intelligence work package
defining the container-level canonical byte representation of Portfolio
Composition.

Its authority is narrow:

- It may define the Portfolio Composition container framing.
- It may preserve and carry opaque canonical references supplied by coordinate
  owners.
- It may frame owner-attribution and Provenance associations without
  redefining their meaning.
- It may disposition inherited gate `G-3` — **Portfolio Composition
  canonical-byte obligation undischarged** — as recorded at
  [M44-WP1 Inherited Gate Inventory and Closure Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
  §4.3. Its exact terminal states are `CLOSED` and `OPEN — PARTIAL`, never a
  blend; `OPEN — PARTIAL` is not closure and blocks M44-WP6 and M44-WP7 without
  exception pending the M44 §12.1.1 checkpoint.
- It may not define or repair the canonical form of any nested source-owned
  coordinate.
- It may not change frozen M42 or M43 contracts.
- It may not implement serializers, schemas, APIs, persistence, or executable
  tests.

The frozen WP1 pre-inventory establishes that several required coordinate forms
are absent. Unless WP4 finds exact owner-supplied forms already present in the
frozen authoritative corpus, the constitutionally expected result is:

> M44-WP4 complete and frozen; `G-3 OPEN — PARTIAL`.

That is a valid completion of WP4, but not a closure of `G-3`. It would prevent
M44-WP6 and M44-WP7 from beginning and require the independently confirmed
stop-or-formal-re-scope checkpoint.

The corrected architecture is sufficiently complete and fail-closed to be
submitted for renewed independent review. Documentary implementation may begin
only after that review accepts RC4.

---

## Recommended WP4 architecture

### 1. Objective

Produce the exact, persistence-neutral, container-level canonical byte contract
for the frozen Portfolio Composition noun and determine whether all ten required
fields are representable using exact owner-supplied canonical references.

WP4 must make one of two mutually exclusive determinations:

1. `G-3 CLOSED` — all required references exist and complete Composition bytes
   are formable.
2. `G-3 OPEN — PARTIAL` — one or more required references are absent; the
   missing elements and their owners are recorded exactly.

WP4 does not need to close `G-3` to complete its work package.

### 2. Constitutional allocation

| Responsibility | Constitutional owner | WP4 authority |
| --- | --- | --- |
| Portfolio Composition container framing | Portfolio Intelligence | Define normatively |
| Portfolio Identity coordinate meaning/form | Ledger & Accounting | Consume only |
| Accounting Scope coordinate meaning/form | Ledger & Accounting | Consume only |
| Portfolio Membership coordinate meaning/form | Ledger & Accounting | Consume only |
| Portfolio Base Currency coordinate meaning/form | Ledger & Accounting for the coordinate; Asset Foundation for the currency-of-denomination dimension | Consume only |
| Investment Universe Declaration meaning/form | Portfolio Intelligence — declaration; Asset Foundation — criterion vocabulary | Consume; no amendment of frozen declaration contract |
| Portfolio Benchmark Declaration meaning/form | Portfolio Intelligence, Market Intelligence, and Asset Foundation as allocated | Consume; no amendment |
| Portfolio Lifecycle State meaning/form | Ledger & Accounting | Consume only |
| Owner-attribution association framing | Portfolio Intelligence — association only | Define association framing only |
| Provenance meaning and capture | Connectivity & Ingestion | Consume opaque owner-supplied content only |
| Provenance-to-coordinate association framing | Portfolio Intelligence — association only | Define association framing only |
| `G-3` disposition | M44-WP4 | Determine `CLOSED` or `OPEN — PARTIAL` |
| Stop/proceed checkpoint | Independent checkpoint authority under M44 §12.1.1 | WP4 supplies evidence but may not declare the checkpoint outcome |

The authority basis is exclusively frozen extension bases `E-1` and `E-2`:

- `E-1` — [M42-WP7](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md)
  §5 expressly permits the representation: “A representation may claim
  canonical bytes only if it preserves this tag, this order, exact citations,
  owner attributions, Provenance associations, and the explicit-absence
  distinction.”
- `E-2` —
  [M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md)
  §7.1 names the required separately authorized contract: “until a separately
  authorized contract supplies the exact Composition canonical bytes, no
  concrete Portfolio Measure Subject — and consequently no concrete Portfolio
  Analytics Input Manifest — can be formed.”

WP4 must not invoke “constitutional silence” as authority.

### 3. Problem statement

M42-WP7 fixes Portfolio Composition’s meaning, exact schema tag, ten-field
semantic order, ownership, Provenance associations, and explicit-absence
distinction, but intentionally supplies no byte representation.

M43-WP3 embeds `portfolio_composition_canonical_bytes` in `PMS1`.
Consequently:

```text
Missing exact coordinate reference
        ↓
No complete Composition canonical bytes
        ↓
No concrete PMS1 subject
        ↓
No concrete PAIM1 manifest
        ↓
No canonical Portfolio Measure Result identity
```

The frozen WP1 pre-inventory reports:

- two fields with determined written forms;
- one field with partially satisfied written-form determinacy;
- seven fields with unsatisfied written-form determinacy.

These disjoint categories total exactly ten fields.

WP4 must therefore separate:

1. the container framing it owns; and
2. the nested canonical content it does not own.

### 4. Scope

WP4 includes:

- A complete ten-field canonical-reference obligation ledger.
- Exact preservation of the frozen schema tag:
  `M42-WP7-PORTFOLIO-COMPOSITION-1`.
- Exact preservation of the frozen ten-field order.
- A tagged, length-delimited, injective, round-trippable, order-stable and
  locale-independent container grammar.
- Definition by the WP4 contract of its own corpus-local primitives, identical
  in mechanics to the precedent in frozen M43-WP3 §7.1 but not inherited as a
  cross-corpus convention:
  - `u32` as unsigned 32-bit network-byte-order length;
  - `lp(x) = u32(byte_length(x)) || x`.
- Treatment of coordinate canonical bytes as opaque.
- Container-owned framing for owner attributions and coordinate-to-Provenance
  associations.
- Preservation of owner-defined affirmative absence as distinct from a missing
  coordinate.
- Rejection of the frozen M44 §11 vocabulary: unknown fields, alternate forms,
  duplicate keys, non-canonical numbers, trailing bytes, and Unicode ambiguity.
  At container level these map respectively to material outside the fixed
  grammar, any non-admitted tag/order/framing, repeated association keys,
  non-canonical numeric framing, unread suffix bytes, and any text-dependent
  alternate representation.
- Per-coordinate closure or fail-closed routing.
- Documentary positive, boundary and negative vectors.
- Vector-by-vector non-triggering proof against every frozen M42-WP7 §8 shape,
  `PC-NGV-01` through `PC-NGV-15`, with `PC-NGV-11`, `PC-NGV-12`,
  `PC-NGV-13`, and `PC-NGV-14` addressed individually and by name and at least
  one negative vector for each of those four.
- Direct conformance findings for M42-WP7 §9 checklist items 10, 11 and 12.
- Final `G-3` disposition.

The Benchmark form-discriminator constraint is binding nested content. Frozen
M44-WP1 §6.4 records it as `CONSTRAINED — NOT SUPPLIED` because frozen M42-WP5
§4.3 does not authorize the four form labels as runtime discriminators,
serialized tags, API values, database enumerations, or implementation
constants. WP4 must route that unsupplied representation to its frozen owner;
it may not frame or invent a discriminator.

#### Recommended framing model

The representation should be a fixed positional envelope:

```text
field 1  schema_version: exact schema tag
field 2  portfolio_identity: lp(portfolio_identity_owner_bytes)
field 3  accounting_scope: lp(accounting_scope_owner_bytes)
field 4  portfolio_membership: lp(portfolio_membership_owner_bytes)
field 5  portfolio_base_currency: lp(portfolio_base_currency_owner_bytes)
field 6  investment_universe_declaration: lp(investment_universe_declaration_owner_bytes)
field 7  portfolio_benchmark_declaration: lp(portfolio_benchmark_declaration_owner_bytes)
field 8  portfolio_lifecycle_state: lp(portfolio_lifecycle_state_owner_bytes)
field 9  coordinate_owner_attributions: lp(container_owned_owner_attribution_bytes)
field 10 coordinate_provenance_associations: lp(container_owned_provenance_association_bytes)
```

The final contract must decide whether the schema tag itself is raw fixed ASCII
or length-prefixed ASCII. Whichever form is selected must have exactly one
admitted representation and reject the other.
[M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md)
§7.2 provides directly relevant precedent by using fixed, unframed raw
`ASCII("PMS1")`; it is evidence for WP4's selection, not authority that decides
the WP4 tag form.

Nested values remain opaque. WP4 must never parse, reorder, normalize,
case-fold, numerically rewrite, Unicode-normalize, or otherwise reinterpret
owner-supplied bytes.

A missing required coordinate has no byte representation. It must not be
represented using an empty string, null, zero length, sentinel, omission, or
inferred default.

An affirmative owner-defined absence—such as a valid benchmark “Explicitly
None”—is a present coordinate value represented by its owner-supplied canonical
bytes. It is not container-level missingness.

### 5. Out of scope

WP4 excludes:

- Any runtime serializer or deserializer.
- Source-code changes.
- Database schemas or migrations.
- DTO, API, JSON, transport or service contracts.
- Persistence or cache formats.
- Executable fixtures or test harnesses.
- Hash algorithm selection.
- Modification of `PMS1` or `PAIM1`.
- Addition, deletion, renaming or reordering of Composition coordinates.
- New coordinate identifiers or value domains.
- Nested source-owned field order or encoding.
- Portfolio method formulas or analytics semantics.
- Annualization ownership or dependency contracts.
- Period-return ownership or governance.
- Changes to WP1, WP2 or WP3 artifacts.
- Roadmap capability-completion declarations.
- Decision Log or Implementation INDEX synchronization.
- Soliciting or authoring contracts in other constitutional domains.
- Treating documentary specimen labels as real canonical values.

### 6. Repository impact

#### Additive planning artifact

This RC4 planning artifact is:

- `docs/implementation/M44_WP4_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md`

It is not one of the three frozen M44 §11 normative WP4 deliverables. It adds
no normative row, asserts no documentary implementation authority, and is
superseded in full by the independently confirmed WP4 contract.

#### Normative repository impact after RC4 approval

Exactly three planned deliverables:

1. `docs/implementation/M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md`
2. `docs/implementation/m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md`
3. `docs/implementation/m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md`

#### Exact review-chain and lifecycle paths

The WP4 architecture-stage lifecycle is pinned before documentary authorship:

1. `docs/implementation/M44_WP4_INDEPENDENT_CONSTITUTIONAL_ARCHITECTURE_REVIEW.md`
2. `docs/implementation/M44_WP4_FORMAL_CONSTITUTIONAL_RESPONSE.md`
3. `docs/implementation/M44_WP4_RENEWED_INDEPENDENT_CONSTITUTIONAL_ARCHITECTURE_REVIEW_RC2.md`
4. `docs/implementation/M44_WP4_RENEWED_INDEPENDENT_CONSTITUTIONAL_ARCHITECTURE_REVIEW_RC3.md`
5. Any subsequent renewed architecture review uses
   `docs/implementation/M44_WP4_RENEWED_INDEPENDENT_CONSTITUTIONAL_ARCHITECTURE_REVIEW_RC{candidate}.md`,
   where `{candidate}` is the architecture revision reviewed. A completed
   review record is immutable and may never be overwritten by a later review.
6. `docs/implementation/M44_WP4_INDEPENDENT_CONSTITUTIONAL_ARCHITECTURE_CONFIRMATION.md`

The architecture-stage confirmation in item 6 confirms only the lifecycle of
this non-normative planning artifact. It does not satisfy frozen M44
Architecture §12.5 point 4, confirm the WP4 normative contract, authorize the
§12.1.1 checkpoint, authorize M44-WP6 or M44-WP7, or freeze or close M44-WP4.

The later contract-stage lifecycle is distinct and is pinned as:

1. `docs/implementation/M44_WP4_INDEPENDENT_CONSTITUTIONAL_CONTRACT_REVIEW.md`
2. `docs/implementation/M44_WP4_INDEPENDENT_SERIALIZATION_REVIEW.md`
3. `docs/implementation/M44_WP4_CONTRACT_FORMAL_CONSTITUTIONAL_RESPONSE.md`,
   only if contract-stage findings exist
4. `docs/implementation/M44_WP4_RENEWED_INDEPENDENT_CONSTITUTIONAL_CONTRACT_REVIEW.md`,
   only if constitutional contract corrections occur
5. `docs/implementation/M44_WP4_RENEWED_INDEPENDENT_SERIALIZATION_REVIEW.md`,
   only if serialization corrections occur
6. `docs/implementation/M44_WP4_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md`
7. `docs/implementation/M44_WP4_FREEZE_RECORD.md`
8. `docs/implementation/M44_WP4_CLOSEOUT.md`

The completed architecture-stage lifecycle never discharges or substitutes for
the contract-stage constitutional review. The contract-stage
`docs/implementation/M44_WP4_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md` is the
M44-WP4 confirmation required by frozen M44 Architecture §12.5 point 4. These
records prove review and lifecycle state only and add no normative
responsibility.

#### Prohibited repository impact

No changes to:

- `backend/`
- `frontend/`
- `scripts/`
- `.github/`
- configuration
- database or migrations
- executable tests
- `docs/architecture/ROADMAP.md`
- `docs/engineering/DECISION_LOG.md`
- `docs/implementation/INDEX.md`
- any frozen M1–M43 or completed M44 artifact

Decision Log and INDEX synchronization remain epic-closeout responsibilities
under separate authority.

### 7. Authority boundaries

WP4 may:

- author a new Portfolio Intelligence serialization contract;
- define the Composition’s container framing;
- define deterministic framing for Composition-owned association fields;
- cite and carry exact owner-supplied nested bytes;
- establish documentary validation requirements;
- record missing elements and their frozen owners;
- disposition `G-3`.

WP4 may not:

- expand Portfolio Intelligence ownership;
- redefine a nested coordinate even where Portfolio Intelligence owns its
  meaning under a frozen contract;
- amend M42-WP3, M42-WP5, M42-WP6 or M42-WP7;
- supply bytes on behalf of Ledger & Accounting, Asset Foundation, Market
  Intelligence, or Connectivity & Ingestion;
- treat routing as discharge;
- declare the §12.1.1 checkpoint passed;
- authorize WP6 or WP7;
- claim runtime or production conformance.

WP4 must prove non-triggering against every frozen M42-WP7 §8 shape and may not
read any frozen `PC-NGV` shape as narrowed, inapplicable, or superseded.

### 8. Dependencies

Strict predecessor:

- [M44-WP1 Inherited Gate Inventory and Closure Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
  and
  [M44-WP1 Roadmap and Current-State Reconciliation](M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
  confirmed and frozen under
  [M44-WP1 Freeze Record](M44_WP1_FREEZE_RECORD.md) §§5, 8, and 11.1 —
  satisfied.

Controlling dependencies:

- [Platform Architecture](../architecture/platform_architecture.md) Laws 1–15
  and §§6–8, 11–12.
- `M34-D-0010`, titled **“Decompose the instrument-analysis product
  contract,”** in the
  [M34 decision register](m34/audit/registers/decision_register.md)
  §`M34-D-0010`. The only consequence relied upon is: “Every field preserves
  semantic owner, source and temporal provenance, and applicable degraded
  state.” Frozen M44 §8.3 characterizes this input as “M34-D-0010 Provenance
  association rules”; WP4 must record that inherited description/title
  divergence and may neither correct nor recharacterize it.
- [M42-WP2](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md):
  Portfolio Identity, Accounting Scope, Membership and Base Currency.
- [M42-WP3 Stage B](M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md):
  Investment Universe Declaration.
- [M42-WP5](M42_WP5_PORTFOLIO_BENCHMARK_DECLARATION_CONTRACT_SPECIFICATION.md):
  Portfolio Benchmark Declaration.
- [M42-WP6](M42_WP6_PORTFOLIO_LIFECYCLE_STATE_REUSE_AND_PROVENANCE_CONTRACT_SPECIFICATION.md):
  Lifecycle and Provenance carriage.
- [M42-WP7](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md):
  Portfolio Composition.
- [M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md)
  and
  [M43-WP3 Manifest](M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md):
  `PMS1` and `PAIM1`.
- [M44 Architecture RC2](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md), frozen
  under
  [M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md).
- The frozen M44-WP1 register and reconciliation cited above.

The frozen M44-WP1 per-field and per-facet pre-inventory is binding as written.
WP4 may not re-derive, reclassify, widen, or narrow any determination. A
perceived divergence is a review finding against the frozen evidence, not a
classification that WP4 may resolve.

WP2 and WP3 are constitutionally adjacent but not WP4 prerequisites. Their
completed status does not widen WP4 authority.

### 9. Inputs

WP4 must consume:

- The frozen ten-field order and schema tag.
- The frozen coordinate-owner allocation.
- The binding frozen WP1 per-field and per-facet pre-inventory, carried
  verbatim and never re-derived, reclassified, widened, or narrowed.
- WP1’s obligation-routing map.
- Every exact owner-supplied reference form found in frozen authoritative
  contracts.
- Frozen M43-WP3 §7.1 as corpus-local precedent for WP4's own identical `u32`
  and `lp(x)` primitives, not as a cross-corpus grant.
- Every frozen M42-WP7 §8 shape, `PC-NGV-01` through `PC-NGV-15`, including
  individual named treatment of `PC-NGV-11` through `PC-NGV-14`.
- M42-WP7 checklist items 10–12.
- The full M43 and M44 negative corpora.
- Frozen explicit-absence and Provenance-association requirements.

Existing source code, stored records and documentary specimen identifiers are
evidence only and cannot supply canonical semantics.

### 10. Outputs

The normative contract should contain:

- authority and non-authority declarations;
- controlling-authority hierarchy;
- extension-basis proof;
- exact byte primitives and grammar;
- canonical decode and validation rules;
- ten-field obligation and closure matrix;
- composite-coordinate facet analysis;
- owner-attribution representation;
- Provenance-association representation;
- missing-versus-affirmative-absence rule;
- rejection matrix;
- vector-by-vector `PC-NGV-01` through `PC-NGV-15` non-triggering proof, with
  `PC-NGV-11` through `PC-NGV-14` addressed individually and by name and at
  least one negative vector for each of those four;
- M42-WP7 checklist conformance;
- an explicit preservation check proving that the exact tag and ten-field
  order are byte-order-identical to frozen M42-WP7 §5;
- exact authority-basis proof naming `E-1` and `E-2`, quoting their frozen
  sentences, and excluding silence as authority;
- exact inherited-gate reporting by repository path and section;
- exact citation of `M34-D-0010` by title and the consequence sentence relied
  upon, with the frozen input-description divergence recorded as inherited and
  unresolved by WP4;
- normative-row-to-vector coverage ledger;
- `G-3` terminal determination;
- downstream consequences;
- freeze and versioning boundary.

Fixture outputs should provide:

- positive mechanical framing vectors;
- boundary-length vectors;
- presentation-permutation/order-stability vectors;
- explicit-absence-versus-missing vectors;
- one positive and one negative case per frozen field;
- per-prohibition negative vectors;
- incomplete-reference vectors producing `OPEN — PARTIAL`.

Synthetic bytes may test framing, but must be labelled `ARTIFICIAL`,
`NON-EFFECTIVE` and `NON-CONFORMANCE-ESTABLISHING`. They cannot stand in for
missing owner-supplied references.

### 11. Acceptance criteria

WP4 is acceptable only if:

1. All ten fields are inventoried in frozen order.
2. Every field carries the exact frozen owner allocation of M42-WP7 §3 as
   recorded in frozen M44-WP1 §6.3, including each co-allocated domain, with no
   owner added, merged, or dropped.
3. Each field carries verbatim the frozen WP1 §6.3 two-axis determination:
   (a) reference exactness and (b) written-form determinacy. Each facet of
   fields 6, 7, and 10 also carries verbatim the frozen WP1 §6.4 two-axis
   determination. Any perceived divergence is raised as a review finding and
   is not resolved by WP4.
4. The exact frozen schema tag is preserved.
5. An explicit preservation check proves that the tag and ten-field order are
   byte-order-identical to frozen M42-WP7 §5.
6. No nested source-owned encoding is authored, including the unsupplied
   Benchmark form discriminator.
7. The container grammar is injective and round-trippable.
8. Presentation permutation cannot change canonical bytes.
9. Missing and affirmative absence cannot collide.
10. Unknown fields, alternate forms, duplicate keys, non-canonical numbers,
    trailing bytes, and Unicode ambiguity are rejected and mapped to exact
    container-level rules.
11. No ambient locale, Unicode, numeric or library behavior influences bytes.
12. Every frozen M42-WP7 §8 non-conforming shape, `PC-NGV-01` through
    `PC-NGV-15`, receives a vector-by-vector non-triggering proof;
    `PC-NGV-11`, `PC-NGV-12`, `PC-NGV-13`, and `PC-NGV-14` are addressed
    individually and by name, with a direct conformance statement and at least
    one negative vector for each.
13. Checklist items 10, 11 and 12 each have a direct proof and negative vector.
14. Each frozen field has positive and negative vector coverage.
15. Vector expectations derive from normative rows, never the reverse.
16. Two independent readers agree on container bytes for every fully
    representable vector. This criterion is required as evidence for `CLOSED`
    only when every coordinate is formable. Agreement on artificial
    container-mechanics specimens during `OPEN — PARTIAL` is never evidence for
    `CLOSED`, and routed coordinates and this criterion are never asserted
    together as closure evidence.
17. The terminal state is exactly `CLOSED` or `OPEN — PARTIAL`.
18. `CLOSED` is used only if both reference exactness and written-form
    determinacy are satisfied at field and facet level for every
    owner-supplied canonical form.
19. Every unsupplied element, including the Benchmark form discriminator, is
    named and routed to its exact frozen owner.
20. No subject, manifest or complete Composition bytes are claimed when the
    state is partial.
21. The contract records directly from frozen sources that WP4 may not supply a
    missing nested form even for a Portfolio Intelligence-owned coordinate,
    relying on M42-WP7 §5's “any source-owned coordinate,” M42-WP7 §9 item 11,
    `PC-NGV-14`, and frozen M44 `INV-C1`; independent review confirms that
    resolution.
22. `E-1` and `E-2` are named as the sole extension bases, their controlling
    frozen sentences are quoted, and no declared or undeclared silence is used
    as authority, satisfying `INV-C2`.
23. Every inherited open gate and its WP4 consequence is named and cited by
    exact repository path and section, satisfying `INV-B2`.
24. The independent serialization reviewer is distinct from the independent
    constitutional reviewer and from the author.
25. Any constitutional correction receives renewed constitutional review by
    that discipline, and any serialization correction receives renewed
    serialization review by that discipline.
26. Final independent constitutional confirmation has unresolved findings
    `NONE`.
27. Frozen artifacts and non-document repository paths remain unchanged.
28. The contract cites `M34-D-0010` by its exact title, identifies only the
    exact consequence sentence relied upon, records the divergence from frozen
    M44 §8.3's “Provenance association rules” characterization, and states that
    WP4 neither corrects nor recharacterizes the inherited matter.
29. The contract-stage
    `M44_WP4_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md` is explicitly recorded
    as the frozen M44 Architecture §12.5 point-4 M44-WP4 confirmation. The
    architecture-stage confirmation is recorded as planning-artifact lifecycle
    evidence only and does not confirm the contract, satisfy §12.5 point 4,
    authorize the §12.1.1 checkpoint, authorize M44-WP6 or M44-WP7, or freeze
    or close M44-WP4.

### 12. Implementation work packages

| Internal package | Responsibility | Principal output |
| --- | --- | --- |
| WP4.1 — Authority and obligation baseline | Lock exact citations, ten-field inventory, frozen owner matrix, binding verbatim pre-inventory carriage and negative corpus | Evidence and authority matrix |
| WP4.2 — Container grammar | Specify primitives, fixed order, opaque-reference framing, association framing and decoder rejection rules | Normative serialization rows |
| WP4.3 — Gate determination | Apply the binding frozen WP1 per-field and per-facet two-axis classifications to closure/routing without re-derivation or reclassification | `G-3` disposition matrix |
| WP4.4 — Documentary vectors | Produce positive, boundary and negative vectors and coverage ledger | Two fixture artifacts |
| WP4.5 — Constitutional conformance | Prove E-1/E-2 authority, frozen preservation and `PC-NGV` non-triggering | Conformance chapters |
| WP4.6 — Contract-stage independent review and freeze | Independent constitutional contract review, independent serialization review by a different reviewer, formal response where findings exist, discipline-specific renewed review, final constitutional confirmation and freeze | Contract review chain and frozen WP4 |

The architecture-stage review, formal response, renewed architecture review and
architecture confirmation are prerequisite lifecycle records, not WP4.6
contract-stage review. Internal packages describe responsibility partitioning
only; the Implementation Roadmap is the sole execution sequence.

### 13. Review strategy

WP4 has two distinct review stages.

#### Architecture-stage lifecycle

The architecture-stage lifecycle uses, in order, the exact paths pinned in §6
for the independent constitutional architecture review, the Formal
Constitutional Response, every versioned renewed independent constitutional
architecture review, and independent constitutional architecture confirmation.
It must complete before documentary implementation begins. Its confirmation is
only planning-artifact lifecycle evidence and does not satisfy frozen M44
Architecture §12.5 point 4, confirm the normative contract, authorize the
§12.1.1 checkpoint, authorize M44-WP6 or M44-WP7, or freeze or close M44-WP4.

#### Contract-stage lifecycle

The contract and documentary vectors require the two independent disciplines
below, using the exact contract-stage paths pinned in §6.

#### Constitutional review

Verify:

- E-1/E-2 are the sole authority bases.
- No silence-based authority appears.
- No nested ownership is transferred or expanded.
- No frozen artifact is amended.
- No WP1, WP2 or WP3 responsibility is duplicated.
- Routing is not presented as closure.
- The terminal-state vocabulary is exact.
- WP4 does not declare the checkpoint outcome.

#### Serialization review

Verify:

- injectivity;
- round-trip decoding;
- fixed field order;
- length-boundary behavior;
- alternate-form rejection;
- missing/absence separation;
- deterministic association ordering;
- trailing-byte rejection;
- exact owner-byte opacity;
- two-reader byte identity where representable;
- complete coverage of the `PC-NGV` and checklist obligations.

The contract-stage constitutional reviewer must be independent of the author.
The serialization reviewer must be independent of both the author and the
contract-stage constitutional reviewer. One reviewer may not discharge both
disciplines. Findings require the pinned contract-stage formal response; each
correction requires the pinned renewed review by the same discipline that
identified or governs it. Freeze requires final independent constitutional
confirmation with unresolved findings `NONE`. That contract-stage confirmation
is the frozen M44 Architecture §12.5 point-4 M44-WP4 confirmation. No
architecture-stage review or confirmation may be reused as contract-stage
review or confirmation evidence.

### 14. Risk assessment

| Risk | Likelihood | Impact | Treatment |
| --- | ---: | ---: | --- |
| Silent amendment of M42-WP7 | Medium | Critical | Fixed preservation proof and independent constitutional review |
| Invented nested coordinate encoding | High | Critical | Opaque-byte boundary and per-coordinate authority matrix |
| `G-3` cannot close | High | Critical downstream | Complete honestly as `OPEN — PARTIAL`; trigger checkpoint |
| Own-domain meaning mistaken for WP4 encoding authority | High | High | Treat frozen M42-WP3/WP5 nouns as separate owned contracts; no amendment |
| Fixtures become de facto semantics | Medium | High | Artificial/non-effective labels; rows precede vectors |
| Missing encoded as empty or null | Medium | Critical | Missing has no conforming byte representation |
| Explicit absence collides with missing | Medium | Critical | Affirmative absence must be present owner-supplied bytes |
| Association order becomes nondeterministic | Medium | High | Fixed coordinate order; reject duplicates and alternate orders |
| Text/Unicode/number normalization introduces alternate bytes | Medium | High | Opaque bytes; no normalization; reject non-grammar forms |
| Partial completion reported as closure | Medium | Critical | Closed two-state vocabulary and independent confirmation |
| WP4 treated as runtime authorization | Medium | Critical | Every implementation authority class remains `NONE` |
| Binding frozen WP1 pre-inventory is re-derived or reclassified | Medium | Critical | Carry both axes and every composite facet verbatim; treat divergence as a review finding |
| Constitutional and serialization reviews are performed by the same person | Medium | Critical | Require an author-independent constitutional reviewer and a different author-independent serialization reviewer |
| Unenumerated planning or review artifacts are mistaken for normative deliverables | Medium | High | Complete path forecast; explicit non-normative status; no normative rows; contract supersession |
| A later author restates authority as declared silence (frozen R-15) | Medium | Critical | Quote `E-1` and `E-2`, test `INV-C2`, and prohibit silence-based authority |

The largest residual risk is intentionally accepted by the frozen architecture:
the work may complete without making Composition bytes formable.

### 15. Open questions

These are WP4 resolution questions, not reasons to redesign the architecture:

1. **Own-domain nested-form scoping question — resolved for RC4.**
   Frozen
   [M44-WP1 Reconciliation](M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
   §6.6 refers the principal question from frozen M44 RC2 §17 `OQ-1`: may WP4
   supply the nested forms for the Investment Universe Declaration and the
   three unsupplied Benchmark Declaration facets merely because Portfolio
   Intelligence owns those coordinates?

   **Resolution: No.** WP4 may define the Composition container but may not
   supply a nested form that a frozen source-owned coordinate contract does not
   supply. This chooses the “Against” branch on the controlling basis that
   M42-WP7 §5 protects nested order inside **any source-owned coordinate**,
   M42-WP7 §9 item 11 uses the unqualified source owner, `PC-NGV-14` prohibits
   invention, and frozen M44 `INV-C1` prohibits silent amendment of a frozen
   M42 contract. The ownership domain of the nested noun does not convert WP4
   container authority into amendment authority. The WP4 contract must record
   this resolution and independent review must confirm it.

2. **Exact `G-3` result.**
   The frozen evidence strongly indicates `OPEN — PARTIAL`. WP4 must formally
   confirm this through the ten-field ledger.

3. **Exact tag framing.**
   WP4 must select one canonical treatment of the full frozen tag—fixed raw
   ASCII or length-prefixed ASCII—and reject every alternative.
   Frozen M43-WP3 §7.2's raw fixed `ASCII("PMS1")` tag is on-point precedent,
   not a decision for WP4.

4. **Composition-owned association grammar.**
   The exact deterministic envelope for owner attributions and Provenance
   associations must be specified without encoding the carried source-owned
   content.

5. **Documentary positive vectors under partial representability.**
   Positive vectors should validate container mechanics using explicitly
   artificial opaque inputs; they must not claim a valid complete production
   Composition.

6. **Inherited checkpoint-recording vehicle tension — noted, not resolved.**
   Frozen M44 §12.1.1 says the checkpoint outcome is recorded in the
   M44-WP1 closure register, but that register is frozen and WP4 may not modify
   it. WP4 neither resolves nor recharacterizes this inherited tension. It
   supplies evidence only; the independent checkpoint authority must act under
   separate constitutional authority.

7. **Inherited `M34-D-0010` characterization divergence — noted, not
   resolved.**
   Frozen M44 §8.3 calls `M34-D-0010` “Provenance association rules,” while
   [the underlying decision](m34/audit/registers/decision_register.md)
   §`M34-D-0010` is titled “Decompose the instrument-analysis product contract.”
   The exact consequence relied upon is: “Every field preserves semantic
   owner, source and temporal provenance, and applicable degraded state.” The
   WP4 contract must cite the exact title and consequence and record the
   inherited divergence. WP4 neither corrects the frozen description nor
   recharacterizes the underlying decision.

None of these requires amendment of the M44 architecture.

---

## Implementation roadmap

1. Complete the architecture-stage review, Formal Constitutional Response,
   every versioned renewed architecture review, and architecture confirmation
   using the exact §6 paths. Record that architecture confirmation as
   non-normative planning-lifecycle evidence only, with none of the frozen
   §12.5 point-4, checkpoint, downstream-release, freeze, or closeout effects.
2. Confirm the WP4 workspace starts from frozen WP1–WP3 and an absent WP4
   contract.
3. Build the authority/citation matrix.
4. Carry the frozen WP1 two-axis field and facet classifications verbatim into
   the WP4 evidence matrix; do not reconcile, re-derive, or reclassify them.
5. Decide container primitives and the one admitted grammar.
6. Specify owner-attribution and Provenance-association envelopes.
7. Specify canonical decoder and rejection behavior.
8. Produce the per-coordinate closure/routing determination.
9. Record exactly one `G-3` terminal state.
10. Author positive, boundary and negative documentary vectors.
11. Complete the row-to-vector coverage ledger.
12. Perform the contract-stage independent constitutional review.
13. Perform the independent serialization review by a reviewer distinct from
    the author and contract-stage constitutional reviewer.
14. Record a contract-stage formal response where findings exist.
15. Apply any required corrections.
16. Obtain renewed independent reviews from each governing discipline where
    corrections occurred.
17. Obtain final contract-stage independent constitutional confirmation with
    findings `NONE` and record it as the frozen M44 Architecture §12.5 point-4
    M44-WP4 confirmation.
18. Freeze WP4.
19. Do not proceed directly to WP6. Await WP5 completion and independent
    confirmation of the §12.1.1 checkpoint.

If `G-3 OPEN — PARTIAL`, the sequence reaches the separately authorized
checkpoint and then stops or proceeds only under a new, independently reviewed
architecture revision.

---

## Suggested repository artifacts

Required normative artifacts:

- `docs/implementation/M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md`
- `docs/implementation/m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md`
- `docs/implementation/m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md`

Justified review-chain artifacts:

- the exact architecture, review, response, renewed-review, serialization,
  confirmation, freeze, and closeout paths pinned in §6.

These review artifacts do not add normative responsibility; they prove the
lifecycle required by the frozen architecture.

Controlling repository evidence includes:

- `docs/implementation/M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md`;
- `docs/implementation/M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md`;
- `docs/implementation/M44_WP1_FREEZE_RECORD.md`;
- `docs/implementation/M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md`;
- `docs/implementation/M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md`.

---

## Implementation sequencing

The single controlling sequence is the `Implementation roadmap` above.
Internal packages in §12 describe responsibility partitioning only and do not
create a second order of execution. No alternate or abbreviated sequence is
authorized.

M44-WP4 does not authorize or perform the checkpoint and does not release
M44-WP6 or M44-WP7.

---

## Recommendation

**READY FOR IMPLEMENTATION**

This means ready to author and review the documentary WP4 contract and vectors.
For this RC4 candidate, that recommendation becomes actionable only after
successful renewed independent constitutional architecture review. It does not
authorize source code, runtime behavior, persistence, APIs, or executable
tests.

The expected constitutional outcome, based on frozen WP1 evidence, is
`G-3 OPEN — PARTIAL`; that outcome is a valid WP4 completion and must not be
reported as closure.
