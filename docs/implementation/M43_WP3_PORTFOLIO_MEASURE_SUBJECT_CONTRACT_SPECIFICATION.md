# M43-WP3 — Portfolio Measure Subject Contract Specification

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

This specification defines only the Portfolio Measure Subject contract
reserved to M43-WP3 by the frozen
[M43 Architecture and Implementation Plan](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§9. It makes mechanically exact:

1. the three subject coordinates;
2. the exact-one-Portfolio and corresponding-Accounting-Scope boundary;
3. exact citation of one immutable M42 Portfolio Composition;
4. subject coherence, identity, ordering, and canonical serialization;
5. the concrete `SUBJECT_COORDINATE` operand names consumed by
   [M43-WP2](M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md);
   and
6. fail-closed missing-coordinate, wrong-scope, cross-portfolio, provider,
   and ambient-selection rules.

The commissioning authority states that M43 Architecture, M43-WP1, and
M43-WP2 are `COMPLETE AND FROZEN`, with their independent confirmations
`APPROVED`. That record controls this work package. WP3 does not edit or
reinterpret those artifacts.

This contract consumes these frozen meanings without restatement or widening:

- **Portfolio Measure Subject** — the exact, identity-bound reference to one
  M42 Portfolio Composition about which one Portfolio Measure is derived;
- **Portfolio Composition** — the M42-WP7 immutable, deterministic,
  canonically serializable, no-derived-measure read-surface;
- **Portfolio Identity** and **Accounting Scope** — Ledger &
  Accounting-owned coordinates under M34 and M42-WP2; and
- the exact Portfolio Measure Definition and Portfolio Method Version
  contracts established by M43-WP2.

M41-WP2 Stage B is cited only as a mechanical precedent for length framing,
injective serialization, and order independence. Its Market
Intelligence-owned Measure Subject, Observation Input Manifest, Manifest
Entry, and related semantics are not reused or widened.

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

WP3 specifies the complete documentary shape needed for two independent
readers to identify the same exact Portfolio Measure Subject without
consulting Current Selection, Workspace state, a provider, a database, a
clock, or another Portfolio.

### 2.2 Out of scope

This specification does not define or authorize:

- a Portfolio Measure Definition, Portfolio Method Version, formula, named
  measure, method catalog, production method, or calculation;
- Portfolio Analytics Input Manifest entry structure, completeness, conflict,
  or invocation binding, which is specified in the companion
  [manifest contract](M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md);
- Portfolio Measurement Window, time, currency, FX, calendar, benchmark
  alignment, risk-free input, annualization, arithmetic, rounding, or
  partial-window semantics reserved to WP4;
- Portfolio Input Sufficiency, Portfolio Computation Outcome, result
  identity, Degraded State carriage, Provenance carriage, or result
  serialization reserved to WP5;
- a new Portfolio Identity, Accounting Scope, Portfolio Composition identity,
  Composition coordinate, or source-owned value;
- runtime selection, lookup, validation, registry, kernel, adapter, storage,
  API, UI, provider, cache, scheduler, migration, or executable test
  behavior; or
- modification of M1–M42, M43 Architecture, M43-WP1, M43-WP2, or
  `docs/GLOSSARY.md`.

Every example and vector is documentary and non-production.

## 3. WP3 downstream vocabulary gate

WP3 requires no new constitutional noun.

| Candidate phrase | Disposition | Proof and routing |
| --- | --- | --- |
| Portfolio Subject Coordinate | `REJECT` | `portfolio_identity`, `accounting_scope`, and `portfolio_composition` are fields of the already-admitted Portfolio Measure Subject, not independently governed objects |
| Portfolio Composition Reference | `REJECT` | Exact citation is a relationship to the existing M42 Portfolio Composition; it creates no second object or identity |
| Portfolio Measure Subject Version | `REJECT` | Contract-version syntax and canonical bytes already make the subject shape and identity exact; a second semantic version axis is unnecessary |
| Portfolio Subject Identity | `REJECT` | Identity is a property of Portfolio Measure Subject under §7, not another business object |
| Portfolio Subject Binding | `REJECT` | Binding is the relationship already present in the confirmed Portfolio Measure Subject meaning |

“Subject coordinate,” “coordinate coherence,” “canonical bytes,” “contract
version,” and “subject candidate” are ordinary specification language. Field
names and documentary result words are contract syntax. They receive no
semantic owner and MUST NOT be added to the Glossary.

The companion manifest specification records the remainder of the WP3-local
gate. No WP3 artifact admits a noun or requires Glossary synchronization.

## 4. Ownership and authority preservation

| Concern | Sole semantic owner | WP3 treatment |
| --- | --- | --- |
| Portfolio Measure Subject and Portfolio-derived measure meaning | Portfolio Intelligence | Subject relationship and canonical shape specified here |
| Portfolio Composition | Portfolio Intelligence under frozen M42-WP7 | Exact complete citation only; no new Composition identity or coordinate |
| Portfolio Identity, Accounting Scope, Membership, Base Currency, lifecycle state, and ledger facts | Ledger & Accounting | Exact source-owned citations/evidence only |
| Investment Universe declaration and Portfolio Benchmark Declaration | Portfolio Intelligence under frozen M42 | Preserved inside the exact Composition; never selected or changed here |
| Market observations, Market Measure Results, FX, calendars, and benchmark observations | Market Intelligence | Not subject coordinates; later manifest evidence only |
| Asset identity, currency dimension, Unit Semantics, Asset Classification, and taxonomy | Asset Foundation | Preserved through source-owned references; not subject identity |
| Provenance meaning and capture | Connectivity & Ingestion | Preserved by M42 Composition; never captured or reconstructed here |
| Current Selection and rendering | Experience Platform | Excluded from subject identity and selection |
| Cross-portfolio exposure and net worth | Wealth Intelligence | Excluded |

Citation, containment, canonical serialization, transport, custody, review,
or later computation transfers no ownership.

## 5. Closed Portfolio Measure Subject structure

### 5.1 Exact meaning and cardinality

A Portfolio Measure Subject is the exact, identity-bound reference to one
complete M42 Portfolio Composition about which one Portfolio Measure is
derived.

It binds:

- exactly one Portfolio Identity;
- exactly that Portfolio Identity's corresponding Accounting Scope; and
- exactly one complete immutable M42 Portfolio Composition whose
  `portfolio_identity` and `accounting_scope` coordinates are those same
  exact references.

There is no multi-Portfolio, household, person, account collection,
Workspace, current-selection, or market-context subject shape. There is no
default subject and no empty subject.

### 5.2 Required normative fields

A Portfolio Measure Subject MUST contain exactly:

| Field | Cardinality | Required content |
| --- | ---: | --- |
| `contract_version` | 1 | Exact ASCII value `M43-WP3-PORTFOLIO-MEASURE-SUBJECT-1` |
| `portfolio_identity` | 1 | Exact non-empty immutable canonical reference recognized by Ledger & Accounting as one Portfolio Identity |
| `accounting_scope` | 1 | Exact non-empty immutable canonical reference recognized by Ledger & Accounting as the corresponding Accounting Scope |
| `portfolio_composition` | 1 | Exact complete immutable canonical representation of one conforming M42-WP7 Portfolio Composition |

No additional or omitted field is permitted. No field receives a default,
alias, fallback, inferred value, provider translation, normalization, or
“latest” resolution.

`contract_version` versions this documentary record shape only. It is not a
Portfolio Method Version, M42 Composition schema version, API version,
storage version, or production-admission marker.

### 5.3 Exact coordinate coherence

The following conditions are jointly required:

1. `portfolio_composition` carries the exact M42-WP7 schema tag
   `M42-WP7-PORTFOLIO-COMPOSITION-1`.
2. The Composition's `portfolio_identity` is byte-for-byte the exact
   canonical reference in the subject's `portfolio_identity`.
3. The Composition's `accounting_scope` is byte-for-byte the exact canonical
   reference in the subject's `accounting_scope`.
4. The exact M42-WP7 Composition's own subject coherence carried in
   `portfolio_composition` evidences that the Accounting Scope corresponds to
   that Portfolio Identity. This condition authorizes no runtime, database,
   registry, or live Ledger & Accounting lookup.
5. Every coordinate inside the Composition remains subject-coherent under
   M42-WP7 §4.1.
6. The Composition is complete under M42-WP7 §§3–5, including the exact
   source-owned coordinates, owner attributions, explicit-absence
   distinctions, and coordinate-specific already-captured Provenance
   associations.

The repeated Identity and Scope references are coherence assertions, not new
copies, aliases, or owner claims. A mismatch at any level rejects the entire
subject. It MUST NOT be repaired by choosing one field as preferred.

### 5.4 Composition citation and no shadow identity

M42-WP7 states that Portfolio Composition has no independent identity: its
subject is its one exact cited Portfolio Identity. WP3 preserves that rule.

Accordingly:

- `portfolio_composition` MUST carry the complete exact immutable M42-WP7
  canonical representation used by the calculation;
- a bare Portfolio Identity, Composition database key, object address, row
  identifier, URL, digest without its governed preimage, or mutable lookup
  locator is not an exact Composition citation;
- WP3 MUST NOT mint a Composition identifier, revision, alias, or “current
  Composition” pointer; and
- two Compositions with the same Portfolio Identity but different canonical
  content produce two different Portfolio Measure Subjects.

An owning contract's canonical reference or nested canonical representation
is opaque to WP3. WP3 frames it but does not normalize, reinterpret, or
re-encode its internal meaning.

## 6. Concrete `SUBJECT_COORDINATE` operands

M43-WP2 §7.3 reserved concrete subject-coordinate names to WP3. The closed
operand-name set is:

| Exact operand name | Governing value | Operand authority |
| --- | --- | --- |
| `portfolio_identity` | Exact subject field of the same name | Ledger & Accounting under M34/M42-WP2 |
| `accounting_scope` | Exact subject field of the same name | Ledger & Accounting under M34/M42-WP2 |
| `portfolio_composition` | Exact complete subject field of the same name | Portfolio Intelligence under M42-WP7 |

No alias, nested source-field path, display label, provider symbol, storage
path, `current`, `selected`, or `latest` operand name is permitted.

WP2 operators apply without alteration:

- `PRESENT` is `MET` only when the named field is present, exact, coherent,
  and canonical under this contract;
- `EQUALS` or `IN` may be used only when the owning frozen contract supplies
  the exact canonical literal or reference bytes required for comparison;
  and
- `COUNT_AT_LEAST` remains invalid for `SUBJECT_COORDINATE`.

A present but unresolved, non-canonical, mismatched, wrong-owner, provider-
shaped, or ambiently selected coordinate is not present for applicability
purposes and yields `UNMET`. This evaluation does not establish Portfolio
Input Sufficiency, computation success, runtime availability, or production
admission.

Upon WP3 independent confirmation, this section closes the M43-WP2 §7.4
deferral only as to the concrete `SUBJECT_COORDINATE` operand names. Exact
canonical literal or reference availability, requirement-set closure, and
every other M43-WP2 gate predicate remain independently required.

## 7. Canonical identity, ordering, and serialization

### 7.1 Ordinary serialization syntax

For this WP3 corpus only:

- a canonical reference is the finite, non-empty immutable byte sequence
  supplied by the authority owning the referenced identity;
- `u32` is an unsigned 32-bit integer encoded in network byte order;
- `lp(x)` is `u32(byte_length(x))` followed by the exact bytes of `x`;
- unsigned byte equality compares every byte without normalization; and
- canonical bytes are the bytes produced by §7.2.

These are local contract mechanics, not new vocabulary, an executable
serializer, persistence format, API representation, or permission to invent
an upstream encoding.

If an owning contract cannot supply one exact immutable canonical reference
or canonical representation required here, a conforming subject cannot be
formed. WP3 does not cure the gap with JSON, display text, database identity,
a provider value, or an implementation-specific encoding.

M42-WP7 §5 currently fixes the Portfolio Composition schema tag and canonical
semantic field order, but expressly defines no exact byte representation,
including no character encoding, delimiter, escaping, container syntax,
transport, serialization library, or persistence form. Therefore, until a
separately authorized contract supplies the exact Composition canonical
bytes, no concrete Portfolio Measure Subject—and consequently no concrete
Portfolio Analytics Input Manifest—can be formed. Every WP3 example remains
an artificial documentary placeholder. Conformance MUST fail closed, and no
reader, implementation, provider, or WP3 artifact may invent an encoding.

### 7.2 Exact serialization

The Portfolio Measure Subject canonical bytes are:

```text
ASCII("PMS1")
lp(portfolio_identity_canonical_reference_bytes)
lp(accounting_scope_canonical_reference_bytes)
lp(portfolio_composition_canonical_bytes)
```

The `portfolio_composition_canonical_bytes` MUST preserve the exact M42-WP7
schema tag and canonical semantic field sequence. WP3 neither defines nor
changes nested source-owned field order or encoding.

No byte-order mark, terminator, padding, omitted field, extension field,
unknown field, alternate tag, or trailing byte is permitted.

### 7.3 Identity and order

Two records denote the same Portfolio Measure Subject if and only if their
§7.2 canonical bytes are byte-identical.

The canonical field order is exactly:

1. `contract_version`, represented by `PMS1`;
2. `portfolio_identity`;
3. `accounting_scope`; and
4. `portfolio_composition`.

Presentation order has no identity effect; canonical serialization always
uses this order. Identity does not depend on document location, object
identity, storage key, hash implementation, clock, provider, request,
Workspace, Current Selection, or registry state.

Canonical serialization MUST be injective: one valid logical subject has
exactly one canonical byte sequence, and one valid canonical byte sequence
reconstructs exactly one logical subject. A digest may later be carried as a
derived locator only under separate authority; it is not subject identity in
WP3 and never substitutes for the canonical bytes.

### 7.4 Immutability and comparison

Once specified, the subject is immutable. Any change to any canonical byte,
including a change to any coordinate carried inside the exact Composition,
produces a different Portfolio Measure Subject.

Equal Portfolio Identity alone does not establish equal subjects. Equal
Portfolio Identity and Accounting Scope alone do not establish equal
subjects. Equality requires byte-identical complete canonical subjects.

## 8. Fail-closed rules

A Portfolio Measure Subject is invalid and MUST be rejected when:

1. any required field is missing, additional, empty, unresolved, mutable, or
   non-canonical;
2. the Portfolio Identity and Accounting Scope are not exact or
   corresponding;
3. the Composition cites a different Identity or Scope;
4. any Composition coordinate belongs to another Portfolio or scope;
5. the Composition is incomplete, altered, inferred, normalized, repaired,
   enriched, or dynamically resolved;
6. a bare ORM object, request value, route parameter, session value,
   Workspace default, Current Selection, provider symbol, display label,
   “latest,” or wall-clock choice supplies any coordinate;
7. a person, household, account collection, cross-portfolio aggregate,
   Wealth object, Market Measure subject, or raw provider object is used as
   the subject;
8. any field creates or transfers source ownership;
9. missing coordinates are treated as explicit absence, Degraded State,
   Portfolio Input Sufficiency, or permission to continue; or
10. a subject candidate requires lookup of live or mutable state to know what
    exact Portfolio Composition it denotes.

Rejection creates no fallback subject, partial subject, default Portfolio,
alternate Method Version, result, outcome, or runtime side effect.

## 9. Determinism and constitutional invariants

1. One subject binds exactly one M42 Portfolio Composition, one Portfolio
   Identity, and its corresponding Accounting Scope.
2. Every source-owned coordinate retains its exact meaning and owner.
3. The subject adds no Portfolio coordinate and changes no Composition.
4. The subject is complete only with all four §5.2 fields.
5. The three concrete subject-coordinate operand names are closed.
6. Canonical bytes alone determine subject identity.
7. Identical exact inputs produce byte-identical subject bytes independent of
   presentation order, custody, clock, provider, process, storage, or user
   context.
8. No ambient choice can create or change a subject.
9. No subject field supplies a formula, measurement window, benchmark
   override, risk-free input, annualization basis, calendar, calculation
   dependency, result, judgment, recommendation, or production claim.
10. Documentary conformance grants no runtime or implementation authority.

## 10. Documentary vectors

The subject contract is exercised together with the companion manifest
contract by:

- [M43-WP3 positive documentary vectors](m43/fixtures/M43_WP3_POSITIVE_DOCUMENTARY_VECTORS.md);
  and
- [M43-WP3 negative documentary vectors](m43/fixtures/M43_WP3_NEGATIVE_DOCUMENTARY_VECTORS.md).

They are normative examples for independent constitutional review only. They
are not executable fixtures, validators, serializers, methods, Composition
instances, registry entries, or production records.

## 11. Prohibited interpretation corpus

Every statement below is constitutionally invalid:

1. “A Portfolio Identity by itself is a Portfolio Measure Subject.”
2. “The current Composition may be looked up when the method runs.”
3. “A Workspace or route-selected Portfolio determines the subject.”
4. “Two subjects with the same Portfolio Identity are always identical.”
5. “A Composition key or digest replaces the complete exact Composition.”
6. “WP3 creates an independent Portfolio Composition identity.”
7. “A mismatched Accounting Scope may be repaired from the Composition.”
8. “A missing coordinate is a degraded but usable subject.”
9. “A provider portfolio code is a canonical Portfolio Identity.”
10. “Subject serialization changes the meaning or owner of an M42
    coordinate.”
11. “A Portfolio Measure Subject is a Portfolio Measure Result or an
    accounting fact.”
12. “The `PMS1` tag is a production Method Version or API version.”
13. “A documentary subject vector proves runtime availability.”

## 12. Completion and independent-review gate

The Portfolio Measure Subject portion of M43-WP3 is complete only when
independent review confirms:

1. the exact WP1 meaning and Portfolio Intelligence ownership are preserved;
2. one and only one complete M42 Composition is bound;
3. every subject coordinate has one owner and one meaning;
4. the three exact `SUBJECT_COORDINATE` operand names are unambiguous;
5. missing, wrong-scope, cross-portfolio, provider-shaped, and ambient
   subjects fail closed;
6. two readers derive the same subject canonical bytes and identity;
7. no new constitutional noun or Glossary change is required;
8. no WP4 or WP5 contract is specified early;
9. no runtime, implementation, executable-validation, provider, persistence,
   API, UI, or production-method authority is introduced; and
10. no frozen artifact is modified;
11. confirmation closes the M43-WP2 §7.4 deferral only for the concrete
    `SUBJECT_COORDINATE` operand names, while every other WP2 gate predicate
    remains independently required; and
12. the external governance dependency in §1.1 is completed under its own
    authority before WP3 confirmation is recorded.

Until independent confirmation, this artifact is proposed and non-effective.
