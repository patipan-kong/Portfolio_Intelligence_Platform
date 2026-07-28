# M43-WP3 — Portfolio Analytics Input Manifest Contract Specification

**Milestone:** M43 — Portfolio Analytics Contract Foundation
**Work package:** M43-WP3 only
**Artifact class:** Constitutional contract specification
**Status:** `PROPOSED — REQUIRES INDEPENDENT CONSTITUTIONAL REVIEW`
**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/API/UI authority:** `NONE`
**Implementation authority:** `NONE`
**Provider authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`

## 1. Purpose and controlling authority

This specification defines only the Portfolio Analytics Input Manifest
contract reserved to M43-WP3 by the frozen
[M43 Architecture and Implementation Plan](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§9. It makes mechanically exact:

1. manifest structure and identity;
2. the structure and identity of its constituent entry records;
3. canonical entry ordering and manifest serialization;
4. exact binding to one Portfolio Measure Subject and one Portfolio Method
   Version;
5. category closure, input completeness, and reconstructability;
6. duplicate, equivalence, conflict, and counting rules;
7. explicit invocation-parameter and calculation-dependency binding; and
8. the inputs WP5 may later use to determine Portfolio Input Sufficiency,
   without defining that determination.

The commissioning authority states that M43 Architecture, M43-WP1, and
M43-WP2 are `COMPLETE AND FROZEN`, with their independent confirmations
`APPROVED`. This work package consumes them as canonical and does not edit or
reinterpret them.

This specification relies on:

- the exact WP1 meaning of **Portfolio Analytics Input Manifest** as the
  immutable, complete, closed, and deterministically orderable binding of
  every exact governed input supplied to one Portfolio calculation;
- the companion
  [Portfolio Measure Subject contract](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md);
- M43-WP2's exact Portfolio Measure Definition pair and Portfolio Method
  Version triple;
- M43-WP2's closed seven input categories, exact dependency declarations,
  non-substitutability, applicability operators, and Portfolio Deterministic Calculation
  obligation;
- M42-WP7 Portfolio Composition; M39 Observations; M41 Market Measure Results;
  exact Ledger & Accounting evidence; Asset Foundation references; and
  already-captured Provenance; and
- ADR-001, ADR-003, and ADR-004 source-of-truth, two-timeline, and one-rule
  constraints.

M41 subject/manifest work is a mechanical precedent only. No Market
Intelligence-owned manifest type, entry type, subject, sufficiency value,
outcome value, or evidence restriction is reused or widened.

### 1.1 External governance dependency

The repository-local effectivity evidence required by the frozen WP1 and WP2
governance remains outstanding: the WP1 §9.2/§9.4 Glossary synchronization
has not been applied, repository-local WP1 and WP2 independent-confirmation
artifacts have not been recorded, and activation of the standing
`M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6` item required
by WP1 §7.4 has not been recorded.

Those actions remain governed by their own separately authorized workflows.
WP3 neither performs nor cures them, and this correction pass edits no frozen
artifact or `docs/GLOSSARY.md`. They are an external, fail-closed governance
dependency: they MUST be completed under their own authority before WP3
confirmation is recorded.

## 2. Normative boundary

### 2.1 In scope

WP3 specifies the documentary record needed for two independent readers,
given the same exact governed input package, to:

- form the same one-Portfolio subject binding;
- identify the same exact Definition and Method Version;
- enumerate the same complete input-entry set;
- detect the same duplicates and conflicts;
- derive the same input-category counts;
- produce byte-identical manifest identity; and
- reconstruct every calculation input without consulting live or mutable
  state.

### 2.2 Out of scope

WP3 does not define or authorize:

- a concrete Definition, Method Version, formula, named measure, statistical
  convention, worked numerical calculation, or production method;
- a new input category, evidence owner, source identity, source payload,
  dependency declaration, or Provenance meaning;
- Portfolio Measurement Window, timestamp selection, currency conversion,
  FX, calendar, benchmark alignment, risk-free input, annualization,
  arithmetic, rounding, or partial-window semantics reserved to WP4;
- Portfolio Input Sufficiency values, Portfolio Computation Outcome values,
  result identity, value shape, Degraded State carriage, Provenance carriage
  in a result, or result serialization reserved to WP5;
- evidence acquisition, retrieval, provider access, source preference,
  quality ranking, repair, reconciliation, or correctness judgment;
- a registry, builder, validator, serializer implementation, kernel, adapter,
  ORM model, database schema, persistence model, endpoint, UI, cache,
  scheduler, migration, test runner, or conformance harness;
- runtime invocation, production admission, method availability, or
  execution; or
- any modification to M1–M42, M43 Architecture, M43-WP1, M43-WP2, or
  `docs/GLOSSARY.md`.

All examples are artificial, documentary, non-executable, and
non-production.

## 3. WP3 downstream vocabulary gate

No new constitutional noun is required.

| Candidate phrase | Disposition | Proof and routing |
| --- | --- | --- |
| Portfolio Analytics Manifest Entry | `REJECT` | A constituent entry record is local structure inside the already-admitted Portfolio Analytics Input Manifest; it has no independent meaning, owner, or lifecycle |
| Portfolio Analytics Invocation | `REJECT` | Invocation is the relationship among an exact subject, exact Method Version, and exact manifest; it is not a third canonical object |
| Portfolio Input Role | `REJECT` | `binding_key` is ordinary contract syntax declared by the exact method specification |
| Portfolio Manifest Identity | `REJECT` | Identity is the canonical-byte property in §10, not an independent object |
| Portfolio Manifest Completeness | `REJECT` | Completeness is an invariant of the admitted manifest; Portfolio Input Sufficiency remains the distinct WP1 noun reserved to WP5 |
| Portfolio Input Conflict | `REJECT` | Conflict is a fail-closed relationship among candidate entry records under §9, not a governed result or state |
| Portfolio Input Package | `REJECT` | “Exact governed input package” is documentary shorthand for the candidate material reviewed when forming a manifest |
| Portfolio Dependency Result Reference | `REJECT` | A dependency-result reference is a field of a `CALCULATION_DEPENDENCY` entry and retains the dependency/result owner's contract |
| Portfolio Manifest Entry Key | `REJECT` | The §8.1 entry key is a manifest-local uniqueness and association tuple with no independent meaning, owner, or lifecycle |

“Entry record,” “binding key,” “category count,” “duplicate,” “conflict,”
“invocation binding,” “canonical reference,” and “canonical value” are local
contract terms. Field names, category tokens already frozen by WP2, and
documentary results do not receive semantic ownership and MUST NOT be added
to the Glossary.

Together with the companion subject gate, this is the complete WP3
downstream vocabulary gate. WP3 requires no Glossary synchronization.

## 4. Ownership and field-level authority

### 4.1 Singular ownership matrix

| Concern | Sole semantic owner | Manifest treatment |
| --- | --- | --- |
| Portfolio Analytics Input Manifest and its binding, closure, ordering, and identity | Portfolio Intelligence | Specified here |
| Portfolio Measure Subject | Portfolio Intelligence | Embedded by exact companion-contract canonical bytes |
| Portfolio Measure Definition and Portfolio Method Version | Portfolio Intelligence | Cited by exact frozen WP2 identities; never substituted |
| Portfolio Composition and Portfolio Benchmark Declaration | Portfolio Intelligence under M42 | Exact subject/input citation only |
| Portfolio Identity, Accounting Scope, Membership, Base Currency, ledger events, replay, holdings, cash, cost basis, and snapshots | Ledger & Accounting | Exact governed evidence/reference/value only |
| M39 Observations, M41 Market Measure Results, FX, calendars, benchmark observations, and market reference measures | Market Intelligence | Exact governed evidence/reference/value only |
| Asset identity, currency dimension, Unit Semantics, Asset Classification, and taxonomy | Asset Foundation | Exact immutable, versioned where governed, references/values only |
| Provenance meaning and capture | Connectivity & Ingestion | Exact already-captured records and associations only |
| Recommendations, constraints, optimization, and execution plans | Decision Intelligence | Excluded |
| Grades, reliability, causal evaluation, and human-vs-AI evaluation | Trust & Evaluation | Excluded |
| Cross-portfolio exposure and net worth | Wealth Intelligence | Excluded |
| Rendering and interaction | Experience Platform | Excluded from assembly and selection; computes nothing |

Manifest custody, framing, ordering, serialization, transport, storage, later
execution, or review creates no shared or derived ownership.

### 4.2 Common entry-field authority

Every entry record is Portfolio Intelligence-owned only as a constituent
position in the manifest. Its referenced identity, exact value, contract
kind, and semantic meaning retain the authority named in
`owning_authority`.

| Field | Authority rule |
| --- | --- |
| `input_category` | Closed by M43-WP2 §5.4 |
| `binding_key` | Exact role key declared by the bound Method Version's immutable specification reference |
| `owning_authority` | Exact constitutional owner of the referenced input or parameter semantics |
| `contract_kind` | Exact existing governed contract kind, or the exact bound non-production method specification for an invocation parameter |
| `canonical_reference` | Exact immutable reference or parameter name under the named authority; never a provider/storage locator |
| `canonical_value` | Complete owner-canonical record bytes, or only an independently canonical coordinate and exact bytes defined by that owning contract, supplied to calculation under the named contract |
| `associated_entry_key` | Exact target entry key only for already-captured Provenance association |

No field makes Portfolio Intelligence a second owner of Ledger, Market,
Asset, or Provenance facts.

## 5. Manifest prerequisites and exact invocation binding

### 5.1 Required prior records

A manifest candidate can conform only when all of the following are exact and
already fixed:

1. one valid Portfolio Measure Subject under the companion contract;
2. one exact Portfolio Method Version identity
   `(bound definition identifier, bound definition revision, method version)`
   under M43-WP2;
3. the exact immutable Portfolio Method Version normative record;
4. its exact immutable non-production specification reference;
5. its closed calculation-dependency declaration and closure;
6. its declared input-category use; and
7. every governing source contract required to supply canonical input
   references and values.

Missing, unresolved, ranged, aliased, mutable, provider-resolved, or “latest”
prerequisites prevent a conforming manifest. WP3 supplies no fallback.

### 5.2 Definition binding

The exact Portfolio Measure Definition identity is already the first two
coordinates of the bound Portfolio Method Version identity. The manifest
MUST NOT carry a second independently selectable Definition field.

The bound Method Version record MUST resolve to exactly that Definition
revision, and the subject MUST satisfy its unchanged subject declaration.
Any separately supplied Definition identity is surplus and creates an
ambiguous or conflicting invocation.

### 5.3 Method specification input roles

For a manifest to be complete, the exact immutable specification referenced
by the bound Method Version MUST make each input it consumes documentary and
inspectable by declaring:

- one stable, opaque ASCII `binding_key`, unique among the specification's
  declared roles;
- exactly one WP2 `input_category`;
- the exact owning authority;
- the exact governed contract kind;
- exact cardinality; and
- for `INVOCATION_PARAMETER`, the exact parameter name and permitted
  canonical value domain.

These declarations are content of the already-required M43-WP2
`Specification reference`; they are not a new Method Version field, a new
canonical noun, a formula, an implementation signature, or production
admission. A referenced specification that leaves a consumed input, role,
authority, contract, or cardinality implicit cannot support a conforming
manifest.

The specification MUST declare exactly one `PORTFOLIO_COMPOSITION` binding
role. Every other role is required exactly at its declared cardinality.
Optional, preferred, variadic-without-bounds, defaulted, ambient, and fallback
roles are prohibited. A declared cardinality may be zero only when it states
that the method consumes no entry under that role; no entry may then use the
key. Every declared input category MUST also contain at least one role with
positive cardinality. A Method Version whose declared category has only
zero-cardinality roles admits no conforming manifest.

### 5.4 Exact invocation binding

One manifest binds exactly:

```text
one Portfolio Measure Subject
+ one exact Portfolio Method Version identity
+ one complete canonically ordered entry set
```

The binding is non-substitutable:

- a compatible Definition revision or Method Version is still a different
  invocation binding;
- changing the subject, method identity, entry key, input identity, value, or
  Provenance association changes the manifest;
- no caller, adapter, registry, provider, or runtime may replace any exact
  coordinate; and
- no request field may override Portfolio Benchmark Declaration, risk-free
  input, annualization basis, calendar authority, Portfolio Base Currency,
  lifecycle state, Provenance, governed evidence, or a calculation
  dependency.

## 6. Closed manifest structure

### 6.1 Required normative fields

A Portfolio Analytics Input Manifest MUST contain exactly:

| Field | Cardinality | Required content |
| --- | ---: | --- |
| `contract_version` | 1 | Exact ASCII value `M43-WP3-PORTFOLIO-ANALYTICS-INPUT-MANIFEST-1` |
| `subject` | 1 | Exact complete canonical bytes of one valid Portfolio Measure Subject |
| `portfolio_method_version` | 1 | Exact M43-WP2 identity triple |
| `entries` | 1 collection | Complete non-empty set of valid §6.2 entry records |

No additional or omitted field is permitted. The Method Version's bound
Definition identity is preserved inside `portfolio_method_version` and is not
duplicated.

The entries collection is necessarily non-empty because M43-WP2 requires
`PORTFOLIO_COMPOSITION` in every Method Version's declared input-category use
and this contract requires exactly one matching Composition entry.

`contract_version` versions this documentary shape only. It is not a Method
Version, API version, storage version, or production-admission marker.
In §10.3 canonical serialization, this exact field is represented by the
`PAIM1` tag.

### 6.2 Common entry-record structure

Every entry record MUST contain exactly:

| Field | Cardinality | Required content |
| --- | ---: | --- |
| `input_category` | 1 | Exactly one closed M43-WP2 §5.4 token |
| `binding_key` | 1 | Non-empty opaque ASCII key resolving to exactly one role in the bound immutable method specification |
| `owning_authority` | 1 | Exact constitutional owner or exact controlling frozen contract |
| `contract_kind` | 1 | Exact governed contract type expected by the declared role |
| `canonical_reference` | 1 | Finite non-empty exact immutable reference bytes under the owning authority |
| `canonical_value` | 1 | Finite non-empty exact canonical bytes of the complete calculation input |
| `associated_entry_key` | 0 or 1 | Present exactly for `CAPTURED_PROVENANCE`; absent for every other category |

The common structure is contract syntax, not a newly admitted Manifest Entry
type. An entry has no identity, owner, lifecycle, or meaning outside its one
containing manifest.

`canonical_value` is the complete value actually supplied to the
calculation, not a mutable locator or permission to fetch it. The value may
be a complete owner-canonical evidence record or the exact owner-canonical
datum selected from such a record only when the owning frozen contract itself
defines that datum as a separately canonical coordinate with its own exact
bytes and the bound specification names it precisely. Otherwise, only the
complete owner-canonical record is admissible. In either case, reconstruction
requires no live lookup, clock, provider, database, cache, Workspace, or
Current Selection.

### 6.3 Category-specific rules

#### `PORTFOLIO_COMPOSITION`

- Exactly one entry is required.
- `owning_authority` is Portfolio Intelligence under M42-WP7.
- `contract_kind` is the exact M42 Portfolio Composition contract.
- `canonical_reference` is the complete subject canonical bytes, because
  M42-WP7 creates no independent Composition identifier.
- `canonical_value` is byte-identical to the exact
  `portfolio_composition_canonical_bytes` embedded in that subject.

M42-WP7 §5 supplies the semantic tag and field order but no exact Composition
byte representation. Consequently this mandatory entry—and therefore a
concrete manifest—cannot yet be formed. The §10 framing remains documentary:
WP3 fails closed and invents no nested encoding.
- `associated_entry_key` is absent.

A subject-byte reference is only the manifest-local locator for this exact
input role. It does not become, imply, or substitute for an independent M42
Portfolio Composition identity.

A bare Identity, Composition row key, digest without governed preimage, or
pointer is invalid.

#### `LEDGER_DERIVED_EVIDENCE`

- `owning_authority` is Ledger & Accounting.
- `contract_kind` identifies the exact governed Ledger-derived evidence
  contract.
- `canonical_reference` identifies the exact immutable evidence instance,
  replay boundary, or snapshot under that contract.
- `canonical_value` contains the complete exact calculation datum, including
  both economic-time and record-time coordinates wherever ADR-003 and the
  owning contract require them.
- Every portfolio-scoped fact MUST resolve to the subject's exact Accounting
  Scope; no evidence may cross a Portfolio boundary.
- `associated_entry_key` is absent.

WP3 neither defines accounting arithmetic nor validates accounting truth.

#### `MARKET_EVIDENCE`

- `owning_authority` is Market Intelligence.
- `contract_kind` is exactly an M39 Observation contract or M41 Market
  Measure Result contract.
- `canonical_reference` is the exact immutable M39 or M41 identity.
- `canonical_value` is the complete exact calculation datum with its governed
  temporal and semantic coordinates.
- Provider identifiers, ticker symbols, provider request/response identities,
  cache keys, or live answers are never canonical references.
- `associated_entry_key` is absent.

#### `ASSET_FOUNDATION_REFERENCE`

- `owning_authority` is Asset Foundation.
- `contract_kind` identifies the exact identity, classification, currency,
  Unit Semantics, or taxonomy contract.
- `canonical_reference` is the exact immutable and versioned reference where
  the owning contract defines a version.
- `canonical_value` is the exact referenced value consumed by the method.
- A display name, ticker, provider symbol, unversioned taxonomy, inferred
  classification, or Portfolio-owned alias is invalid.
- `associated_entry_key` is absent.

#### `INVOCATION_PARAMETER`

- `owning_authority` is Portfolio Intelligence under the exact bound
  non-production method specification.
- `contract_kind` is that exact immutable method specification.
- `canonical_reference` is the exact ASCII parameter name declared for the
  `binding_key`.
- `canonical_value` is one exact canonical value expressly permitted for that
  parameter.
- `associated_entry_key` is absent.

A parameter is a permitted caller choice only. It MUST NOT supply, replace,
or override governed evidence, a Portfolio declaration, risk-free input,
annualization basis, calendar authority, Base Currency, lifecycle state,
Provenance, or calculation dependency. Absence never invokes a default.

#### `CALCULATION_DEPENDENCY`

- `binding_key` is exactly one dependency key declared by the bound Method
  Version.
- `owning_authority` and `contract_kind` exactly match that declaration.
- `canonical_reference` is the exact WP2 dependency tuple
  `(owning domain, dependency contract kind, dependency identifier,
  dependency version)`.
- `canonical_value` is the exact immutable result or value supplied under
  that dependency contract.
- `associated_entry_key` is absent.

Every direct dependency whose result or value the method consumes appears
exactly once. A transitive dependency does not become an additional entry
unless the bound method specification also declares it as a directly
consumed role. The exact Method Version still commits to the full WP2
dependency closure.

If the governing dependency contract does not yet define an exact immutable
result/value representation, no conforming concrete entry can be formed.
WP3 does not invent a dependency result identity reserved to another owner or
to WP5.

#### `CAPTURED_PROVENANCE`

- `owning_authority` is Connectivity & Ingestion.
- `contract_kind` is the exact frozen Provenance contract.
- `canonical_reference` is the exact immutable reference recognized by that
  contract.
- `canonical_value` is the complete already-captured Provenance supplied for
  the association.
- `associated_entry_key` is present and equals the exact §8.1 entry key of
  one non-Provenance entry in the same manifest.

Provenance is associated, never recaptured, reconstructed, combined into
obscurity, normalized, provider-mapped, ranked, scored, or used as proof of
correctness. A Provenance entry cannot target another Provenance entry.

## 7. Manifest completeness and closure

### 7.1 Exact completeness test

A manifest is complete if and only if all of the following hold:

1. the subject and exact Method Version satisfy §5;
2. the set of distinct categories represented by entries equals the Method
   Version's declared input-category use exactly;
3. every declared method-specification `binding_key` with positive
   cardinality is represented at exactly that cardinality;
4. no undeclared, optional, unrelated, unused, or surplus entry exists;
5. exactly one Composition entry matches the exact subject;
6. every Ledger entry is confined to the subject Accounting Scope;
7. every Market and Asset entry resolves exactly under its owning contract;
8. every invocation parameter is explicitly permitted and exact;
9. every directly consumed calculation dependency matches its WP2
   declaration and exact result/value;
10. every already-captured Provenance record supplied with an input is
    included under its exact association; when any such record is supplied,
    the Method Version's declared input-category use and specification roles
    MUST include `CAPTURED_PROVENANCE`, or no conforming manifest can be
    formed; and
11. every reference and value is immutable, canonical, attributable, and
    reconstructable without live state.

Completeness is evaluated only over the exact bound method specification and
the exact supplied governed inputs. It does not authorize retrieval,
discovery, enrichment, “best available” evidence, or a search for additional
inputs.

### 7.2 No default and no surplus

An omitted required entry is missing. It MUST NOT be:

- fetched later;
- inferred from another entry;
- filled from Composition, request, Workspace, Current Selection, provider,
  cache, database, wall clock, or another Portfolio;
- replaced by a compatible Method Version or alternate dependency; or
- treated as an empty, zero, Explicitly None, degraded, partial, or default
  value unless the owning frozen contract itself defines that exact
  affirmative value and the role expressly requires it.

An undeclared or additional entry does not make the manifest “more
complete.” It makes the manifest non-conforming because the input closure is
no longer exact.

### 7.3 Boundary to Portfolio Input Sufficiency

Manifest completeness is a structural precondition input to the future WP5
Portfolio Input Sufficiency contract. WP3 does not define a sufficiency
enumeration, reason code, Portfolio Computation Outcome, Degraded State, or
result behavior.

A structurally conforming manifest does not prove:

- applicability;
- numerical adequacy;
- Portfolio Input Sufficiency;
- computation success;
- value presence;
- correctness, quality, reliability, or fitness;
- runtime availability; or
- production admission.

A non-conforming candidate cannot become a canonical manifest. WP5 may later
classify the consequence under its own authority; WP3 does not pre-assign
that classification.

## 8. Entry identity, equivalence, and counting

### 8.1 Entry-record identity

Within one manifest, entry-record identity is the exact ordered tuple:

```text
(
  input_category,
  binding_key,
  owning_authority,
  contract_kind,
  canonical_reference,
  canonical_value,
  associated_entry_key-or-absence
)
```

Every component participates. The **entry key** used only for uniqueness and
Provenance association within one manifest is the exact triple:

```text
(input_category, binding_key, canonical_reference)
```

“Entry key” is local contract syntax, not a new canonical noun. No display
field, document position, object identity, provider identity, storage
location, or source presentation order participates.

One declared role may have multiple entries only when its exact positive
cardinality permits them; each must have a distinct entry key. The same
governed input may be cited under two different binding keys only when the
bound immutable method specification declares both roles explicitly. Those
are two entry records, not two source facts.

### 8.2 Identity equivalence

Two candidate references are identity-equivalent only when the exact owning
contract determines that both resolve unambiguously to the same immutable
canonical reference and canonical value.

Equal payloads, similar meaning, shared origin, matching provider symbols,
display labels, timestamps alone, or a reviewer judgment do not establish
identity equivalence. WP3 performs no semantic deduplication.

Identity-equivalent candidates for one `binding_key` do not create a second
entry. If both are presented as separate entry records, they are a duplicate
and the candidate manifest is rejected rather than silently deduplicated.

### 8.3 Category counting for M43-WP2

For an M43-WP2 `COUNT_AT_LEAST` requirement:

1. first validate the entire candidate manifest, including duplicates and
   conflicts;
2. if it is non-conforming, the named input category is unresolved for
   applicability and the requirement is `UNMET`;
3. otherwise count the valid entry records whose `input_category` exactly
   equals the named closed token; and
4. compare that non-negative integer with the WP2 literal.

There is no deduplication phase because duplicates are invalid before
counting. When one owner-governed input legitimately supports two distinct
method-declared roles, the two distinct entry records count as two. A
Provenance entry counts only in `CAPTURED_PROVENANCE`, never again in the
category of its target.

`PORTFOLIO_COMPOSITION` count is exactly one for every conforming manifest.

Upon WP3 independent confirmation, this section closes the M43-WP2 §7.4
deferral only as to exact manifest entry identity, duplicate/conflict
handling, and category-count semantics. Canonical operand availability,
requirement-set closure, and every other M43-WP2 gate predicate remain
independently required.

## 9. Duplicate and conflict rules

### 9.1 Duplicate rules

The entire manifest candidate MUST be rejected when:

- two records have the same complete §8.1 identity;
- two records share an entry key, even if every other field is identical;
- one candidate representation of the same owner-governed identity is
  repeated under the same key;
- two Composition entries appear; or
- an entry is repeated to satisfy cardinality or `COUNT_AT_LEAST`.

Duplicates are not silently removed, merged, counted once, ranked, or
resolved by presentation order. This is stricter than treating a manifest as
a bag assembled first and normalized later: no such intermediate canonical
manifest exists.

### 9.2 Conflict rules

A conflict exists when any of the following is true:

1. one `binding_key` has more candidate references or values than its
   declared cardinality permits;
2. one canonical reference is paired with different canonical values,
   owners, or contract kinds;
3. two identity-distinct candidates compete for a role whose declared
   cardinality cannot retain both;
4. a Composition entry differs from the bound subject;
5. a Ledger entry cites another Accounting Scope;
6. a dependency entry differs from the exact WP2 dependency declaration;
7. an invocation parameter differs from its exact permitted name or value
   domain;
8. one Provenance reference has different content or associations; or
9. an owning contract reports an unresolved or ambiguous identity.

A conflict MUST NOT be resolved by:

- input order;
- source or provider priority;
- recency or wall-clock comparison;
- quality, trust, or reliability scoring;
- payload similarity;
- cache, storage, or route state;
- a caller preference;
- choosing another Portfolio, Method Version, or dependency; or
- a correctness or causal judgment.

An unresolved conflict prevents a canonical manifest from existing. WP3
defines no conflict outcome, degraded value, partial manifest, or fallback.

### 9.3 Distinct evidence that is not conflicting

Identity-distinct governed inputs may coexist only when the exact method
specification declares distinct binding keys or a cardinality that retains
all of them, and the inputs do not violate §9.2.

Different values are not automatically a conflict when they occupy different
declared roles or coordinates. Equal values are not automatically equivalent
when their governed identities differ. The owning contracts decide identity;
the bound method specification decides roles and cardinalities; WP3 decides
only manifest binding and closure.

## 10. Canonical ordering, serialization, and manifest identity

### 10.1 Ordinary serialization syntax

For this WP3 corpus only:

- a text value is a finite, non-empty sequence of Unicode scalar values
  encoded as UTF-8;
- an opaque canonical reference/value is a finite, non-empty byte sequence
  supplied under its owning contract;
- `u32` is an unsigned 32-bit integer encoded in network byte order;
- `lp(x)` is `u32(byte_length(x))` followed by the exact bytes of `x`;
- `0x00` denotes absent `associated_entry_key`;
- `0x01 || lp(associated_entry_key_bytes)` denotes its presence; and
- unsigned byte order compares bytes left-to-right as integers from `0` to
  `255`, with a proper prefix ordered before the longer sequence.

Text and opaque values MUST already be canonical under their governing
contract. WP3 performs no Unicode normalization, case folding, whitespace
trimming, alias expansion, provider translation, unit conversion, timestamp
conversion, rounding, or value normalization.

### 10.2 Canonical entry ordering

Before serialization, valid entry records MUST be sorted lexicographically by
these components, each compared as unsigned bytes:

1. UTF-8 bytes of `input_category`;
2. UTF-8 bytes of `binding_key`;
3. UTF-8 bytes of `owning_authority`;
4. UTF-8 bytes of `contract_kind`;
5. `canonical_reference` bytes;
6. `canonical_value` bytes; and
7. absent association as `0x00`, or present association as
   `0x01 || lp(associated_entry_key_bytes)`.

Earlier components dominate later components. Presentation order has no
identity effect. Sorting occurs only after the candidate has passed shape,
duplicate, conflict, binding, and completeness rules; sorting never repairs a
defect.

This ordering discipline is local contract mechanics. It does not create an
ordering owner or change any source-owned ordering inside canonical reference
or value bytes.

### 10.3 Canonical serialization

The exact Portfolio Method Version identity is serialized locally as:

```text
lp(UTF8(bound_definition_identifier))
lp(ASCII(base10(bound_definition_revision)))
lp(ASCII(method_version))
```

The revision and method-version forms MUST already satisfy M43-WP2 §§5.2 and
6.2. This framing does not reinterpret either identity.

Each entry record serializes as:

```text
lp(UTF8(input_category))
lp(UTF8(binding_key))
lp(UTF8(owning_authority))
lp(UTF8(contract_kind))
lp(canonical_reference)
lp(canonical_value)
association:
  0x00
  or
  0x01
  lp(associated_entry_key_bytes)
```

The associated entry key bytes are:

```text
lp(UTF8(target_input_category))
lp(UTF8(target_binding_key))
lp(target_canonical_reference)
```

The complete manifest serializes as:

```text
ASCII("PAIM1")
lp(subject_canonical_bytes)
lp(portfolio_method_version_identity_bytes)
u32(entry_count)
repeat entries in §10.2 canonical order:
  lp(entry_canonical_bytes)
```

No byte-order mark, terminator, padding, omitted field, extension field,
unknown field, alternate tag, or trailing byte is permitted.

The embedded subject MUST independently conform to the companion `PMS1`
contract. Every reference and value remains opaque to WP3 after its owning
contract supplies the canonical bytes.

Because M42-WP7 §5 does not yet supply exact Composition canonical bytes, no
valid concrete `PMS1` subject or `PAIM1` manifest byte sequence can presently
be emitted. The framing above remains an artificial documentary contract and
MUST NOT be used to invent the missing nested encoding.

The canonical manifest field order is exactly:

1. `contract_version`, represented by `PAIM1`;
2. `subject`;
3. `portfolio_method_version`; and
4. `entries`, represented by `entry_count` followed by the §10.2 ordered
   entry records.

### 10.4 Manifest identity and determinism

Two records denote the same Portfolio Analytics Input Manifest if and only if
their §10.3 canonical bytes are byte-identical.

Canonical bytes are manifest identity. WP3 creates no separate manifest
identifier, revision, mutable key, registry address, or digest requirement.
A future digest may be a derived locator under separate authority; it never
substitutes for the canonical bytes.

Canonical serialization MUST be injective and round-trippable: one valid
logical manifest has exactly one byte sequence, and one valid byte sequence
reconstructs exactly one `contract_version`, subject, Method Version identity,
entry count, ordered entry set, and association set without external
ordering, defaults, lookups, or interpretation.

Given identical exact subject bytes, Method Version identity, source-
canonical references, source-canonical values, and associations, independent
readers MUST produce byte-identical manifest identity regardless of:

- candidate presentation order;
- document or storage location;
- object identity or process;
- provider, network, database, or cache state;
- wall-clock time;
- Workspace or Current Selection;
- registry build order; or
- caller identity.

## 11. Applicability and sufficiency-precondition inputs

### 11.1 `SUBJECT_COORDINATE`

The manifest supplies the exact complete subject against which the companion
contract's closed operands `portfolio_identity`, `accounting_scope`, and
`portfolio_composition` are evaluated.

### 11.2 `INPUT_CATEGORY`

The manifest supplies the exact §8.3 category counts used by M43-WP2
`COUNT_AT_LEAST`.

Conditional on WP3 independent confirmation, this closes only WP2 §7.4's
deferred category-count semantics. Every other WP2 applicability gate
predicate remains independently required.

### 11.3 `INVOCATION_PARAMETER`

The operand name is the exact parameter name in the matching
`INVOCATION_PARAMETER` entry. It is present only when the complete entry is
valid and unambiguous. Comparison uses the exact `canonical_value`.

### 11.4 `CALCULATION_DEPENDENCY`

The operand name is the exact dependency key in the matching
`CALCULATION_DEPENDENCY` entry. `PRESENT` requires exact match to the bound
Method Version declaration and an exact canonical dependency result/value.

### 11.5 Fail-closed evaluation

For any applicability operand, a missing, duplicated, conflicting,
wrong-owner, wrong-category, non-canonical, unresolved, or surplus entry makes
that operand unresolved and its requirement `UNMET` under M43-WP2.

An otherwise complete and applicable manifest supplies documentary inputs to
future WP5 sufficiency review. It does not determine Portfolio Input
Sufficiency or authorize calculation.

## 12. Constitutional invariants

1. One manifest binds exactly one Portfolio Measure Subject and one exact
   Portfolio Method Version.
2. The Definition identity is fixed through that Method Version and is not
   independently selectable.
3. Exactly one Composition entry is present and matches the subject.
4. The category set equals the Method Version's declared input-category use.
5. Every positive-cardinality method-declared role is exact and complete; no
   surplus role exists.
6. Every entry is attributable to exactly one semantic owner and exact
   governing contract.
7. Every input is self-contained for calculation reconstruction; no live
   lookup or ambient resolution remains.
8. Duplicate and conflicting candidates prevent a canonical manifest.
9. Entry counting occurs only after full conformance and is deterministic.
10. Presentation order never changes identity.
11. Exact method and dependency identities are non-substitutable.
12. Invocation parameters cannot override governed declarations, evidence,
    authority, or dependencies.
13. Provenance remains already captured, owner-preserved, and associated with
    one exact input.
14. No provider identity, Current Selection, Workspace state, wall clock,
    cross-portfolio state, model output, recommendation, evaluation, or
    runtime default participates.
15. No formula, result, outcome, sufficiency value, production method,
    implementation, or runtime capability is created.

## 13. Documentary vectors

This contract and the companion subject contract are exercised by:

- [M43-WP3 positive documentary vectors](m43/fixtures/M43_WP3_POSITIVE_DOCUMENTARY_VECTORS.md);
  and
- [M43-WP3 negative documentary vectors](m43/fixtures/M43_WP3_NEGATIVE_DOCUMENTARY_VECTORS.md).

They are normative examples for independent review, not executable fixtures,
validators, serializers, concrete methods, registry records, or production
admissions.

## 14. Prohibited interpretation corpus

Every statement below is constitutionally invalid:

1. “The manifest may contain whatever inputs happen to be available.”
2. “An extra entry makes the manifest safer or more complete.”
3. “Duplicate entries can be silently deduplicated before counting.”
4. “Conflicting evidence may be resolved by source priority or recency.”
5. “A provider symbol is an exact Market or Asset reference.”
6. “A reference is sufficient even when calculation needs a live lookup for
   its value.”
7. “A request benchmark, risk-free rate, annualization basis, calendar, or
   Base Currency is an invocation parameter.”
8. “A compatible Method Version may replace the exact bound version.”
9. “A governed dependency can be supplied as a free parameter.”
10. “A missing entry can be loaded from the current Workspace or selected
    Portfolio.”
11. “Ledger evidence from another Accounting Scope may be aggregated into the
    same manifest.”
12. “Provenance may be reconstructed or used as a quality score.”
13. “Structural manifest completeness is Portfolio Input Sufficiency.”
14. “A conflict is a Degraded State or Portfolio Computation Outcome defined
    by WP3.”
15. “`PAIM1` is an API, database, or production Method Version.”
16. “Canonical serialization authorizes a serializer implementation.”
17. “A documentary manifest vector is a production invocation.”

## 15. Completion and independent-review gate

The Portfolio Analytics Input Manifest portion of M43-WP3 is complete only
when independent review confirms:

1. the exact WP1 meaning and Portfolio Intelligence ownership are preserved;
2. all seven categories retain their exact WP2 meanings and source owners;
3. subject, Definition, Method Version, and dependency bindings are exact and
   non-substitutable;
4. every input role, reference, value, association, and category count is
   deterministic;
5. completeness excludes both missing and surplus entries;
6. duplicate, equivalence, and conflict rules yield one result for every
   vector and never silently choose;
7. wrong-scope, cross-portfolio, missing-coordinate, duplicate-entry,
   conflicting-evidence, provider-symbol, and ambient-selection vectors fail
   closed;
8. two readers produce the same entry ordering, category counts, canonical
   bytes, and manifest identity;
9. every input is attributable and reconstructable without consulting live
   state;
10. no new constitutional noun or Glossary change is required;
11. no WP4 temporal, currency, calendar, benchmark, risk-free,
    annualization, arithmetic, or rounding rule is specified;
12. no WP5 sufficiency, outcome, result, Degraded State, Provenance-carriage,
    or result-serialization contract is specified;
13. no runtime, implementation, executable-validation, provider,
    persistence, API, UI, or production-method authority is introduced; and
14. no frozen artifact is modified;
15. confirmation closes the M43-WP2 §7.4 deferral only for manifest entry
    identity, duplicate/conflict handling, and `COUNT_AT_LEAST` counting
    semantics, while every other WP2 gate predicate remains independently
    required; and
16. the external governance dependency in §1.1 is completed under its own
    authority before WP3 confirmation is recorded.

Until independent confirmation, this artifact is proposed and non-effective.
