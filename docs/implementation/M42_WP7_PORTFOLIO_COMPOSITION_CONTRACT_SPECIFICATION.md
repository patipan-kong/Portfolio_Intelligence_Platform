# M42-WP7 — Portfolio Composition Contract Specification

**Milestone:** M42 — Portfolio Intelligence Foundation  
**Work package:** M42-WP7 — Portfolio Composition & Projection Contract (terminal)  
**Document class:** Documentation-only constitutional semantic contract  
**Status:** READY_FOR_INDEPENDENT_REVIEW

## 1. Authority and Purpose

This contract formalizes Portfolio Composition: the one terminal, deterministic,
immutable, canonically serializable Portfolio read-surface. It binds one
Portfolio Identity's admitted coordinates, preserving each coordinate's source
meaning, owner attribution, and already-captured Provenance association. It
carries no derived measure.

It is governed by frozen M42 Architecture, frozen M42-WP1, confirmed M42-WP2,
M42-WP3, M42-WP5, and M42-WP6, the M42-WP4 REJECT disposition, and the approved
WP7 Architecture Investigation. It changes none of them.

Portfolio Intelligence owns only Portfolio Composition, its composition
relationship, subject coherence, semantic completeness, semantic determinism,
ownership preservation, coordinate association, and Provenance association.
It does not own any composed coordinate, Provenance meaning, or Provenance
capture. Citation, carriage, adjacency, and composition create no ownership,
transfer, laundering, or derived ownership.

Normative terms govern documentary semantic conformance only. They grant no
runtime, implementation, persistence, API, database, UI, calculation, workflow,
or operational authority.

## 2. Semantic Scope

Portfolio Composition is the only governed noun defined here. It is not a second
Portfolio Identity, a ledger record, lifecycle record, provenance object,
Investment Universe result, Benchmark observation, or source of cited facts.

Its exact meaning is:

> The single deterministic, immutable, canonically serializable read-surface
> binding one Portfolio Identity's complete frozen and confirmed-admitted
> coordinates, preserving exact meanings, owner attributions, and
> coordinate-specific already-captured Provenance associations, with no
> derived measure, ambient default, or unadmitted coordinate.

This contract defines only identity and subject binding, Accounting Scope binding,
coordinate admissibility and completeness, identity/ownership/Provenance
preservation, explicit absence versus missing coordinate, semantic determinism,
the schema-version tag, exact canonical field order, and downstream authority.

It does not define or authorize normalization, inference, enrichment, repair,
substitution, remapping, translation, synthesis, calculations, valuation, NAV,
FX conversion, analytics, optimization, recommendation, eligibility, Investment
Universe Membership, policy, authorization, workflow, lifecycle transition,
currentness inference, runtime behavior, or implementation behavior. It defines
no persistence model, database schema, API, UI, service, runtime object,
serializer implementation, wire format, storage format, byte encoding,
transport, executable validator, or operational conformance process.

## 3. Admissible Coordinates

A complete composition MUST cite these coordinate classes only, at their
confirmed source meanings:

| Coordinate | Owner | Authority | Required treatment |
|---|---|---|---|
| Portfolio Identity | Ledger & Accounting | Frozen M34 / WP2 | Exact citation; sole subject |
| Accounting Scope | Ledger & Accounting | Frozen M34 / WP2 | Exact corresponding-scope citation |
| Portfolio Membership | Ledger & Accounting | Frozen M34 / WP2 | Exact Ledger fact; no investment interpretation |
| Portfolio Base Currency | Ledger & Accounting | WP2 | Named unit reference only; no rate or conversion |
| Investment Universe declaration | Portfolio Intelligence | WP3 | Complete declaration citation and carriage only |
| Portfolio Benchmark Declaration | Portfolio Intelligence | WP5 | Complete declaration citation and carriage only; never bare Benchmark |
| Portfolio Lifecycle State | Ledger & Accounting | Frozen M36 / WP6 | Exact state citation only; no transition or currentness |
| Provenance associated with each supplied coordinate | Connectivity & Ingestion owns meaning and capture | WP6 / frozen Glossary | Exact coordinate-specific association preservation |

No other coordinate is admissible unless frozen authority is explicitly amended.

A composition is semantically complete only when every listed coordinate is cited
at its confirmed meaning and every already-captured Provenance item made
available for a carried coordinate remains associated with that exact coordinate.
Completeness MUST NOT be achieved by omission, invention, defaulting,
replacement, repair, enrichment, normalization, inference, synthesis, or
reinterpretation. An unsupplied coordinate is missing, not a value or authority
to complete the composition.

Portfolio Policy, all WP4-rejected concepts, Investment Universe Membership and
all belonging/evaluation equivalents, policy, limits, eligibility, authorization,
allocation, execution, provider answers, runtime lookups, ambient context,
defaults, and every derived measure are prohibited.

## 4. Normative Rules

### 4.1 Identity, subject, scope, and membership

A composition has no independent identity: its subject is one exact cited
Portfolio Identity. It MUST NOT mint, replace, merge, split, alias, rename, or
act as a shadow identity. Every coordinate MUST bind to that Identity and its
corresponding Accounting Scope. Cross-subject composition is prohibited.

Accounting Scope remains the Ledger & Accounting-owned boundary. Composition
MUST NOT create another scope, broaden it, or change holdings, transactions,
cash, or balances meaning. Membership remains a Ledger fact; it never proves
Investment Universe Membership or eligibility.

### 4.2 Meaning and ownership preservation

Every coordinate retains its exact source identity and confirmed meaning.
Composition MUST NOT normalize, translate, map, reclassify, substitute,
summarize as a replacement, deduplicate, repair, enrich, infer, or reinterpret
a coordinate or its source references.

Base Currency supplies no FX, conversion, valuation, NAV, rate, or reporting
calculation. Investment Universe is carried complete and is never evaluated
against an instrument. Portfolio Benchmark Declaration remains one of its four
admitted forms and never becomes a Benchmark observation or calculated series.
Lifecycle State establishes no transition, legitimacy, authorization,
availability, action eligibility, or runtime currentness.

Composition MUST preserve every source owner. It MUST NOT make a coordinate
jointly owned, copy source authority, or make Portfolio Intelligence a second
source of Ledger & Accounting, Connectivity & Ingestion, Market Intelligence,
Asset Foundation, or Decision Intelligence facts.

### 4.3 Provenance

Provenance retains its frozen meaning, Where a fact came from, and Connectivity
& Ingestion retains ownership of its meaning and capture. For each coordinate
with already-captured Provenance, composition MUST preserve the complete
available Provenance, its association with that exact coordinate, the
coordinate's exact meaning and owner, and separation from other coordinates'
Provenance.

Composition MUST NOT capture, recapture, reconstruct, generate, combine into
obscurity, detach, summarize as a substitute, rank, score, trust-grade,
provider-map, validate, reconcile, repair, enrich, normalize, translate, or
invent Provenance. Provenance is not proof of correctness, currentness,
legitimacy, authorization, availability, actionability, or quality.

### 4.4 Explicit absence and determinism

An explicit absence is admissible only where a source contract defines it as an
affirmative state. WP5 Explicitly None is such a state: the declaration is
present and its required Benchmark-series citations are explicitly absent.
Omitted, unavailable, unknown, unset, or unsupplied coordinates are missing and
MUST NOT become Explicitly None, an empty declaration, a default, fallback,
inferred value, invalidity verdict, or repaired coordinate.

Given the same complete coordinates, absence state, owner attributions, and
Provenance associations, independent readers MUST derive the same semantic
composition and §5 field sequence. No clock, provider, model, market data,
runtime state, user selection, storage location, session, or ambient default
may affect meaning.

## 5. Canonical Serialization Boundary

Frozen M42 and WP1 reserve canonical serialization, exact canonical field order,
a schema-version tag, and canonical-byte obligations to WP7. This contract
preserves them without removal, deferral, weakening, reassignment, or
reinterpretation.

The schema-version tag is exactly M42-WP7-PORTFOLIO-COMPOSITION-1.

The canonical semantic field order is exactly:

1. schema_version;
2. portfolio_identity;
3. accounting_scope;
4. portfolio_membership;
5. portfolio_base_currency;
6. investment_universe_declaration;
7. portfolio_benchmark_declaration, including Explicitly None where applicable;
8. portfolio_lifecycle_state;
9. coordinate_owner_attributions; and
10. coordinate_provenance_associations.

This does not define nested field order inside any source-owned coordinate or
alter an upstream coordinate. Owner attribution and Provenance association
preserve association only; neither creates a new owner or Provenance meaning.

A representation may claim canonical bytes only if it preserves this tag, this
order, exact citations, owner attributions, Provenance associations, and the
explicit-absence distinction. This documentation-only contract defines no byte
or character encoding, delimiter, escaping, container syntax, transport,
serialization library, or persistence form. Those implementation details are
outside scope. Their exclusion does not remove or defer the frozen canonical-byte
obligation.

## 6. Downstream Authority

Downstream consumers MAY cite Portfolio Composition as the terminal M42
semantic-definition surface and rely only on its cited meanings, subject
coherence, owner attribution, Provenance association, explicit-absence
distinction, determinism, and serialization boundary.

No consumer receives authority to change, validate, evaluate, calculate, value,
convert, optimize, recommend, authorize, execute, transition, repair, normalize,
infer, enrich, select, rank, reconcile, or operationalize any coordinate. It
receives no Ledger truth, runtime-model, analytical-model, valuation-model,
optimization-model, policy-engine, recommendation-engine, API, persistence,
schema, or executable-system authority.

WP7 terminates only the M42 semantic-definition pipeline. It neither replaces a
source authority nor creates an executable system.

## 7. Positive Documentary Vectors

| ID | Documentary specimen | Conforming property |
|---|---|---|
| PC-PGV-01 | PI-01 cites corresponding AS-01; exact Membership, Base Currency, Investment Universe, Benchmark Declaration, and Lifecycle State citations share that subject. | Every admitted coordinate is subject coherent. |
| PC-PGV-02 | Base Currency is cited solely as a named unit reference, with no FX, NAV, price, rate, conversion, or return. | No measure or accounting leakage. |
| PC-PGV-03 | Investment Universe is carried with exact name, criteria, references, and revision condition; no instrument is tested. | Complete declaration, no Membership/evaluation. |
| PC-PGV-04 | Benchmark Declaration is complete in an admitted form and cited series remain unchanged. | Nested ownership preserved. |
| PC-PGV-05 | An Explicitly None Benchmark Declaration is present; series citations are explicitly absent. | Explicit absence preserved. |
| PC-PGV-06 | Lifecycle State archived is cited without a transition, currentness, or action conclusion. | Lifecycle citation only. |
| PC-PGV-07 | Each coordinate retains its own already-captured Provenance association and owner attribution. | Provenance and ownership preservation. |
| PC-PGV-08 | Independent readers with identical inputs derive identical meaning and §5 sequence. | Semantic determinism. |
| PC-PGV-09 | The exact tag and ten-field order are stated while upstream coordinates remain exact citations. | Serialization boundary preserved. |
| PC-PGV-10 | A later consumer cites composition but states no result or new source authority. | Downstream citation only. |

## 8. Negative Documentary Vectors

| ID | Non-conforming shape | Constitutional defect |
|---|---|---|
| PC-NGV-01 | PI-01 is composed with non-corresponding AS-02. | Cross-subject composition. |
| PC-NGV-02 | Portfolio Intelligence owns a cited Ledger coordinate or Provenance. | Ownership leakage. |
| PC-NGV-03 | A currency alias, provider code, Benchmark alias, or criterion is standardized. | Normalization or source-vocabulary theft. |
| PC-NGV-04 | A missing coordinate is filled, defaulted, selected from context, or inferred. | Inference and missing-coordinate invention. |
| PC-NGV-05 | NAV, price, weight, return, alpha, exposure, rate, or FX-converted value appears. | Measure/calculation/valuation leakage. |
| PC-NGV-06 | An instrument is classified as belonging, eligible, permitted, compatible, or tradable. | Rejected Membership or policy leakage. |
| PC-NGV-07 | Policy, leverage, cash floor, allocation, or execution rule appears. | Rejected WP4/Decision Intelligence leakage. |
| PC-NGV-08 | Lifecycle state authorizes action or proves lawful transition/currentness. | Lifecycle execution/runtime leakage. |
| PC-NGV-09 | Provenance is generated, detached, merged, reconstructed, or used as trust. | Provenance reconstruction/judgment. |
| PC-NGV-10 | Missing Benchmark Declaration becomes Explicitly None. | Missing/absence conflation. |
| PC-NGV-11 | A database, JSON, API, service, runtime object, byte encoding, or storage form is prescribed. | Implementation/runtime leakage. |
| PC-NGV-12 | §5 order changes or source fields are treated as WP7-normalized fields. | Field-order/meaning reinterpretation. |
| PC-NGV-13 | Another schema tag claims conformance. | Schema reinterpretation. |
| PC-NGV-14 | Canonical-byte language defines upstream encoding, fields, schema, or identifiers. | Serialization reinterpretation. |
| PC-NGV-15 | Composition is Ledger truth, a runtime/analytical/valuation/optimization model, policy engine, or recommendation engine. | Authority leakage. |

## 9. Constitutional Acceptance Checklist

Independent Review MUST verify all of the following:

1. Portfolio Composition is the sole governed noun and is solely Portfolio Intelligence-owned.
2. PI ownership is limited exactly to composition, relationship, coherence, completeness, determinism, ownership preservation, coordinate association, and Provenance association.
3. Every source owner in §3 remains unchanged; no shared or derived ownership arises.
4. One exact Identity and its corresponding Scope bind every coordinate.
5. Every admissible coordinate is exact, complete, source-owned, and non-reinterpreted.
6. No unadmitted, WP4-rejected, Membership, policy, eligibility, transition, currentness, measure, calculation, analytics, valuation, optimization, recommendation, or runtime semantic occurs.
7. Each available Provenance item stays with its exact coordinate; no capture, reconstruction, merging, or judgment occurs.
8. Explicitly None is distinct from missing; no absence is invented.
9. Determinism excludes live, ambient, provider, clock, model, runtime, and default dependence.
10. The tag is exactly M42-WP7-PORTFOLIO-COMPOSITION-1 and the order is exactly §5.
11. No source-owned nested coordinate is reordered, normalized, encoded, or reinterpreted.
12. Canonical-byte obligations are preserved without invented encoding or removal, deferral, or weakening.
13. Positive and negative vectors cover all required constitutional boundaries.
14. No implementation, persistence, API, schema implementation, UI, service, runtime, database, calculation, validator, or workflow authority is claimed.
15. No frozen authority is altered and no downstream authority beyond terminal semantic composition is granted.

## 10. Final Normative Boundary

M42-WP7 begins with the complete, subject-coherent frozen and confirmed-admitted
coordinate set and any already-captured Provenance associated with those
coordinates. It ends with one deterministic Portfolio Composition whose field
sequence, source meanings, owner attributions, and Provenance associations remain
unchanged.

It terminates the M42 semantic-definition pipeline only. It is not Ledger truth,
a runtime model, analytical model, valuation model, optimization model, policy
engine, recommendation engine, or executable system.

## Appendix A. Composition Constitutional Gate Table

This appendix summarizes existing §§1–6 normative rules as a single gate. It
introduces no new coordinate, semantic, or authority.

| Gate | Statement |
|---|---|
| Permitted Subject | One exact cited Portfolio Identity and its corresponding Accounting Scope (§4.1). |
| Permitted Inputs | The eight admitted coordinate classes of §3, at their confirmed source meanings, with any already-captured Provenance associated with a supplied coordinate (§3, §4.3). |
| Output Meaning | One deterministic, immutable, canonically serializable Portfolio Composition binding those coordinates in the exact §5 field order, preserving source meanings, owner attributions, and Provenance associations, with no derived measure (§2, §5). |
| Prohibited Inputs | Any coordinate not listed in §3, including Portfolio Policy, all WP4-rejected concepts, Investment Universe Membership or belonging/evaluation equivalents, limits, eligibility, authorization, allocation, execution, provider answers, runtime lookups, or ambient context (§3). |
| Prohibited Semantics | Normalization, inference, enrichment, repair, substitution, remapping, translation, synthesis, calculation, valuation, NAV, FX conversion, analytics, optimization, recommendation, lifecycle transition, currentness inference, Provenance reconstruction, or any implementation/runtime/persistence/API behavior (§2, §4.2, §4.3, §6). |

## Appendix B. Frozen Authority Compatibility Matrix

This appendix summarizes the relationship §1 already declares between WP7 and
each frozen or confirmed authority it cites. It grants no new authority and
changes no ownership or semantics.

| Authority | Relationship | Ownership transferred? | Semantic modification? |
|---|---|---|---|
| M42 Architecture | Preservation — WP7 fulfills the canonical-serialization reservation frozen M42 assigns to it (§5) | NO | NO |
| WP1 | Preservation — WP7 fulfills the schema-version tag and field-order reservation frozen WP1 assigns to it (§5) | NO | NO |
| WP2 | Citation — Portfolio Identity, Accounting Scope, Portfolio Membership, and Portfolio Base Currency are cited at their confirmed WP2 meanings (§3) | NO | NO |
| WP3 | Citation/carriage — the Investment Universe declaration is cited and carried complete, never evaluated (§3, §4.2) | NO | NO |
| WP4 (REJECT) | Reuse of disposition — the WP4 REJECT disposition is reused to exclude Portfolio Policy and all WP4-rejected concepts as inadmissible (§1, §3) | NO | NO |
| WP5 | Citation/carriage — the Portfolio Benchmark Declaration, including Explicitly None, is cited in one of its four admitted forms (§3, §4.2, §4.4) | NO | NO |
| WP6 | Citation/preservation — the Portfolio Lifecycle State and coordinate Provenance associations are cited and preserved at their confirmed WP6 meanings (§3, §4.3) | NO | NO |

READY_FOR_INDEPENDENT_REVIEW
