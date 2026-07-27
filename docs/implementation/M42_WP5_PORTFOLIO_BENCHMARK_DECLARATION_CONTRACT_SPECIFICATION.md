# M42-WP5 — Portfolio Benchmark Declaration Contract Specification

**Work package:** M42-WP5

**Date:** 2026-07-27

**Artifact type:** Documentation-only, implementation-neutral semantic contract

**Canonical governed noun:** **Portfolio Benchmark Declaration**

**Owner:** Portfolio Intelligence

**Contract-design authority:** Portfolio Benchmark Declaration only

**Implementation authority:** `NONE`

**Persistence authority:** `NONE`

**Runtime authority:** `NONE`

**API authority:** `NONE`

**Serialization authority:** `NONE`

**Provider-mapping authority:** `NONE`

**Calculation authority:** `NONE`

**Executable-validation authority:** `NONE`

**Enforcement authority:** `NONE`

**Document status:** `COMPLETE`

**Independent Review result:** `APPROVED`

Normative terms such as **MUST**, **MUST NOT**, **REQUIRED**, and **MAY** govern
only the meaning of this documentation-only contract. They do not authorize a
schema, executable validator, runtime behavior, persistence mechanism, API,
serialization, provider integration, calculation, enforcement mechanism, or
implementation.

---

## 1. Executive Summary

This specification defines the canonical Portfolio Benchmark Declaration
contract. Its entire subject is one descriptive, portfolio-scoped declaration
of one Portfolio Benchmark choice.

Each declaration:

- belongs to exactly one cited Portfolio Identity;
- references exactly one cited Accounting Scope, which is the Accounting Scope
  corresponding to that Portfolio Identity;
- has one explicit declared name;
- declares exactly one Portfolio Benchmark value;
- instantiates exactly one of four closed forms: Single, Composite, Category,
  or explicitly None; and
- remains descriptive only.

The phrase **declares exactly one Portfolio Benchmark** means that one
declaration has one complete declared choice and one form. It does not mean
that the Composite form cites only one underlying series. It also does not
establish how many Portfolio Benchmark Declarations may exist for one
Portfolio Identity.

Portfolio Intelligence owns the declaration. It does not own the referenced
Benchmark observations. The bare noun **Benchmark** remains reserved for the
Market Intelligence-owned canonical observation type. Every Benchmark series
is cited without redefinition, derivation, maintenance, provider mapping, or
ownership transfer.

This contract defines no benchmark calculation, observation, provider,
maintenance, analytics, performance comparison, optimization, allocation,
policy, accounting behavior, implementation, persistence, runtime, API,
serialization, schema, or provider mapping. Portfolio Base Currency is not a
subject of this contract. It remains wholly governed by the frozen M42-WP2
contract under Ledger & Accounting.

---

## 2. Scope

### 2.1 Governing authority and precedence

This specification is subordinate to, and MUST be read consistently with:

1. the frozen Platform Architecture and domain constitutions;
2. the frozen [M42 Architecture Proposal](M42_ARCHITECTURE_PROPOSAL.md);
3. the confirmed
   [M42-WP1 Portfolio Canonical Vocabulary and Ownership Register](M42_WP1_PORTFOLIO_CANONICAL_VOCABULARY_AND_OWNERSHIP_REGISTER.md);
4. the confirmed
   [M42-WP2 Portfolio Identity, Accounting Scope, Membership and Base Currency Contract Specification](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md);
5. the confirmed
   [M42-WP3 Investment Universe Declaration Contract Specification](M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md);
6. the complete
   [M42-WP4 Portfolio Policy Ownership Investigation](M42_WP4_PORTFOLIO_POLICY_OWNERSHIP_INVESTIGATION.md);
7. the complete
   [M42-WP5 Benchmark and Portfolio Base Currency Ownership Validation](M42_WP5_BENCHMARK_AND_PORTFOLIO_BASE_CURRENCY_OWNERSHIP_VALIDATION.md);
8. frozen Market Intelligence authority for Benchmark observations, Benchmark
   series, Benchmark provider mapping, and Benchmark data; and
9. frozen Asset Foundation authority for every canonical asset vocabulary
   reference appearing in or beneath a cited Benchmark series.

On conflict, the earlier or source-owning authority controls. This
specification cites those authorities without amending, duplicating, extending,
or transferring them.

### 2.2 Included surface

The complete WP5 contract surface is:

1. the Portfolio Identity and Accounting Scope subject binding;
2. the explicit declared name;
3. exactly one declared Portfolio Benchmark value per declaration;
4. the four closed declaration forms: Single, Composite, Category, and
   explicitly None;
5. exact citation of Market Intelligence-owned Benchmark series where the
   selected form requires such citations;
6. ownership-preserving documentary invariants;
7. documentation-only positive and negative golden vectors; and
8. the exact downstream citation-and-carriage boundary.

The phrases **subject binding**, **declared value**, **form**, **series
citation**, and **explicitly None** describe facets of Portfolio Benchmark
Declaration. They are not new governed nouns, runtime types, schema fields,
independently owned objects, or vocabulary admissions.

### 2.3 Excluded surface

This contract does not define or authorize:

- benchmark observations, values, series content, provider mapping, provider
  identity, source selection, market-data normalization, retrieval, repair,
  enrichment, caching, maintenance, refresh, substitution, or publication;
- benchmark formulas, composite construction, weights, rebalancing,
  calculation, conversion, alignment, aggregation, interpolation, or
  derivation;
- alpha, attribution, return, risk, score, ranking, analytics, evaluation,
  Trust Report meaning, or any other benchmark-performance comparison;
- recommendation, optimization, target allocation, actual allocation,
  allocation drift, eligibility, constraint, limit, policy, enforcement,
  execution preference, or transaction behavior;
- Portfolio Identity, Accounting Scope, Portfolio Membership, Portfolio Base
  Currency, NAV, accounting periods, accounting events, valuation, return
  calculation, FX conversion, or any other accounting behavior;
- asset taxonomy, asset identity, identifier formats, aliases, classifications,
  mappings, or any other Asset Foundation-owned vocabulary;
- implementation, persistence, database design, schema, runtime object,
  service, API, serialization, canonical bytes, field names, field order,
  transport, UI, provider integration, executable validation, or test code;
- implicit defaults, ambient portfolio selection, inference, resolution,
  lookup, fallback, or automatic replacement; or
- the withheld Policy-derived form or any renamed equivalent.

The declaration coordinate is semantic documentation only. Nothing in this
document prescribes how a declaration is created, changed, stored, transported,
validated, resolved, displayed, or executed.

---

## 3. Subject Binding

### 3.1 Binding coordinate

One Portfolio Benchmark Declaration MUST:

1. belong to exactly one explicitly cited Portfolio Identity; and
2. reference exactly one explicitly cited Accounting Scope.

The cited Accounting Scope MUST be the Ledger & Accounting-owned Accounting
Scope corresponding to the cited Portfolio Identity. An ambient, inferred,
current, default, cross-portfolio, or mismatched subject is outside this
contract.

Portfolio Identity and Accounting Scope are cited at their frozen M42-WP2
meanings. WP5 adds no identity attribute, accounting boundary, correspondence
rule, lifecycle meaning, or alternate scope.

### 3.2 Cardinality distinction

The one-subject rule constrains each declaration:

> one Portfolio Benchmark Declaration → exactly one Portfolio Identity →
> exactly one corresponding Accounting Scope.

It does not establish whether a Portfolio Identity has zero, one, or many
Portfolio Benchmark Declarations. Portfolio-level declaration cardinality is
outside WP5 authority unless a future, separately governed authority decides
it.

The exactly-one-Portfolio-Benchmark rule likewise constrains each declaration:
one declaration contains one complete declared choice in one closed form. A
Composite choice may cite multiple Benchmark series while remaining one
declared Portfolio Benchmark value.

### 3.3 Citation without transfer

Subject binding does not transfer ownership:

- Ledger & Accounting retains sole ownership of Portfolio Identity and
  Accounting Scope;
- Portfolio Intelligence owns only the Portfolio Benchmark Declaration that
  belongs to and references those coordinates; and
- citation, adjacency, composition, or downstream carriage never creates
  shared ownership.

Portfolio Base Currency is neither part of the subject binding nor an
additional WP5 coordinate. If a downstream composition places Portfolio Base
Currency beside this declaration, it remains a separate M42-WP2 coordinate
owned by Ledger & Accounting.

---

## 4. Portfolio Benchmark Declaration Contract

### 4.1 Complete semantic coordinate

One complete Portfolio Benchmark Declaration consists semantically of:

1. the subject binding defined in §3; and
2. one explicit declared name; and
3. exactly one declared Portfolio Benchmark value in exactly one form defined
   in §4.3.

This list defines meaning, not fields, layout, syntax, object structure,
serialization, or schema.

The declaration is descriptive only. It records the portfolio's declared
comparison choice. It does not obtain observations, calculate a benchmark,
compare performance, make a decision, constrain an optimizer, direct an
allocation, enforce a policy, or produce an accounting result.

### 4.2 Declared name

Each declaration MUST have one explicit declared name. The name identifies the
declaration for documentary meaning only. It is not a Benchmark series
identifier, provider symbol, asset alias, policy label, runtime key, or
instruction.

WP5 defines no name syntax, identifier format, uniqueness scope, localization,
normalization, storage, or serialization rule. A name MUST NOT be omitted,
inferred from a cited series, or supplied by an ambient default.

### 4.3 Closed forms

Each declaration MUST instantiate exactly one, and only one, of the following
closed forms:

| Form | Documentary meaning | Citation condition |
|---|---|---|
| **Single** | One declared Portfolio Benchmark choice represented by one Market Intelligence-owned canonical Benchmark series | MUST cite exactly one canonical Benchmark series |
| **Composite** | One declared Portfolio Benchmark choice that is the frozen Portfolio Domain Model's weighted blend of reference series | MUST cite at least two canonical Benchmark series; their calculation, weighting, construction, maintenance, and observation values are not defined here |
| **Category** | One declared Portfolio Benchmark choice that is the frozen Portfolio Domain Model's peer standard for a category of strategy, represented only through exact Market Intelligence Benchmark-series citation | MUST cite one or more canonical Benchmark series; WP5 defines no category taxonomy, matching rule, provider mapping, or series-selection behavior |
| **Explicitly None** | The affirmative declaration that this portfolio has no selected Benchmark series | MUST cite no Benchmark series and MUST NOT be treated as missing, unset, unknown, defaulted, or erroneous |

No fifth form exists in this contract. Hybrid, open-ended, custom,
Policy-derived, target-allocation-derived, inferred, or defaulted forms are
outside the confirmed WP5 surface.

The four form labels classify the declaration only. They do not authorize
runtime discriminators, serialized tags, API values, database enumerations, or
implementation constants.

### 4.4 Exact Benchmark citation

For Single, Composite, and Category forms, each Benchmark series reference
MUST be an exact citation of a canonical Market Intelligence-owned Benchmark
series, expressed in the frozen `asset_id` format: the platform's own
permanent, opaque identifier, owned by Asset Foundation and defined once at
[UNIVERSAL_ASSET_ARCHITECTURE.md §2–3](../architecture/UNIVERSAL_ASSET_ARCHITECTURE.md).
This is the same citation format every canonical observation kind already
uses, because [MARKET_DATA_PLATFORM.md
§7](../architecture/MARKET_DATA_PLATFORM.md) normalizes a Benchmark
observation identically to an asset price. WP5 reuses this frozen format
exactly; it does not invent an identifier scheme, does not introduce a
provider identifier, and does not introduce a provider mapping.

A citation:

- identifies the referenced canonical series without reproducing its
  observations or provider representation;
- preserves Market Intelligence ownership of the observation type, series,
  provider mapping, and data;
- preserves Asset Foundation ownership of every canonical asset vocabulary
  reference carried by or beneath the cited series; and
- grants Portfolio Intelligence no authority to derive, normalize, price,
  map, fetch, update, maintain, repair, enrich, or copy the series.

The declaration MUST NOT use bare **Benchmark** as its own name or as an
abbreviation for Portfolio Benchmark Declaration. Bare **Benchmark** denotes
the Market Intelligence-owned observation type.

### 4.5 Declaration invariants

Every conforming Portfolio Benchmark Declaration satisfies all of the
following:

1. It belongs to exactly one Portfolio Identity.
2. It references exactly one corresponding Accounting Scope.
3. It has one explicit declared name.
4. It declares exactly one complete Portfolio Benchmark value.
5. It uses exactly one of the four closed forms.
6. It is descriptive only.
7. It carries no executable semantics.
8. It carries no optimization semantics.
9. It carries no allocation semantics.
10. It carries no policy semantics.
11. It carries no accounting semantics.
12. It carries no provider semantics.
13. It carries no implementation semantics.
14. It contains no observation value, calculation, analytic result, or
    performance-comparison result.
15. It introduces no ambient default or inferred replacement.
16. It cites every externally owned coordinate without acquiring, sharing, or
    transferring ownership.

The phrase **carries no executable semantics** includes matching, selection,
resolution, validation, permission, refusal, enforcement, triggering, and
control flow. The declaration has no operational answer to produce.

### 4.6 No hidden semantics

The presence, absence, form, or cited series of a Portfolio Benchmark
Declaration MUST NOT be interpreted by this contract as:

- a recommendation that the portfolio should hold an instrument;
- a target, model, ideal, shadow, current, or permitted allocation;
- an optimizer objective, constraint, preference, input, or fitness function;
- a Portfolio Limit, Decision Policy, Portfolio Policy, compliance rule, or
  execution rule;
- proof of suitability, eligibility, risk, expected return, performance, or
  quality;
- an accounting unit, Portfolio Base Currency, FX path, valuation method, NAV
  rule, return formula, or accounting event; or
- an instruction to obtain, calculate, maintain, or compare Benchmark data.

Explicitly None is meaningful only as the declared absence of a selected
Benchmark series. It is not a default request, waiver, failure, fallback,
policy exemption, or instruction to select a substitute.

---

## 5. Ownership Boundary

### 5.1 Ownership matrix

| Coordinate or meaning | Sole owner | WP5 authority |
|---|---|---|
| Portfolio Benchmark Declaration | Portfolio Intelligence | Define the declaration coordinate within this contract |
| Benchmark observation type | Market Intelligence | Citation only |
| Benchmark observation | Market Intelligence | None; citation only where source authority permits |
| Benchmark series | Market Intelligence | Exact citation only |
| Benchmark provider mapping | Market Intelligence | None |
| Benchmark data and maintenance | Market Intelligence | None |
| Portfolio Identity | Ledger & Accounting | Subject citation only |
| Accounting Scope | Ledger & Accounting | Subject citation only |
| Portfolio Base Currency | Ledger & Accounting | None; frozen M42-WP2 citation only when boundary explanation requires it |
| Decision Policy and Portfolio Limits | Decision Intelligence | None |
| Optimizer behavior and execution preferences | Decision Intelligence | None |
| Canonical asset vocabulary | Asset Foundation | Exact citation only; no local taxonomy, alias, or mapping |

### 5.2 Boundary rules

Portfolio Intelligence owns the act and meaning of declaring the portfolio's
comparison choice. It does not own anything that supplies, observes,
calculates, maintains, evaluates, or acts upon that choice.

Market Intelligence ownership is unchanged when the declaration cites one or
more Benchmark series. A Composite or Category declaration does not create a
Portfolio Intelligence-owned observation series, calculation, provider map, or
maintenance obligation.

Ledger & Accounting ownership is unchanged when the declaration binds to
Portfolio Identity and Accounting Scope. WP5 does not redefine, duplicate, or
extend Portfolio Base Currency. Base Currency is not a declaration form,
series property, default, conversion instruction, or comparison result.

Decision Intelligence ownership is unchanged by the declaration. A declared
Portfolio Benchmark is not a policy, limit, optimizer objective, target
allocation, execution preference, or recommendation input under this contract.
The Policy-derived form remains withheld.

Asset Foundation ownership is unchanged by any asset reference carried by a
cited Benchmark series. WP5 creates no competing asset vocabulary or
identifier representation.

### 5.3 Citation never transfers ownership

Citation records a relationship to source-owned meaning. It does not:

- copy the source authority into this contract;
- make the cited coordinate jointly owned;
- permit redefinition, extension, normalization, or mapping;
- grant calculation, observation, provider, accounting, policy, or
  implementation authority; or
- allow a downstream consumer to attribute its own behavior to WP5.

This rule applies equally to Portfolio Identity, Accounting Scope, Benchmark
series, Asset Foundation vocabulary, Portfolio Base Currency when mentioned
for boundary clarity, and every downstream composition.

---

## 6. Positive Golden Vectors

These vectors are normative documentary examples. They are not serialized
records, schema specimens, API payloads, executable tests, validator outputs,
provider mappings, or instructions to fetch or calculate data. Abstract labels
such as `PI-01` and `AS-01` stand for exact citations whose identifier form
remains owned elsewhere. Abstract labels such as `MI-BENCH-01` stand for exact
`asset_id` citations of a canonical Market Intelligence-owned Benchmark
series, per §4.4; the specific opaque values shown are illustrative only.

| ID | Documentary declaration | Why it conforms |
|---|---|---|
| PGV-01 | Portfolio Identity `PI-01`; corresponding Accounting Scope `AS-01`; name “Primary Comparison”; exactly one declared Portfolio Benchmark in Single form citing `asset_id` `MI-BENCH-01`. | One explicit subject, name, corresponding scope, declared choice, and exact Market Intelligence series citation in the frozen `asset_id` format |
| PGV-02 | Portfolio Identity `PI-02`; corresponding Accounting Scope `AS-02`; name “Blended Comparison”; exactly one declared Portfolio Benchmark in Composite form — the frozen Portfolio Domain Model's weighted blend of reference series — citing `asset_id` `MI-BENCH-02` and `asset_id` `MI-BENCH-03`. | Multiple underlying series remain one Composite declaration; no weights, formula, observation, or maintenance semantics are added |
| PGV-03 | Portfolio Identity `PI-03`; corresponding Accounting Scope `AS-03`; name “Fixed-Income Category Comparison”; exactly one declared Portfolio Benchmark in Category form — the frozen Portfolio Domain Model's peer standard for a category of strategy — represented only through exact citation of canonical series `asset_id` `MI-BENCH-04`. | Category expresses the frozen peer-standard-for-a-category-of-strategy meaning and cites source-owned series without defining taxonomy, selection, matching, or provider behavior |
| PGV-04 | Portfolio Identity `PI-04`; corresponding Accounting Scope `AS-04`; name “Not Benchmarked”; exactly one declared Portfolio Benchmark in Explicitly None form, with no series citation. | Explicit absence is a complete declaration, not a missing value or request for a default |
| PGV-05 | Portfolio Identity `PI-05`; corresponding Accounting Scope `AS-05`; name “Asset-Referenced Comparison”; a Composite declaration cites `asset_id` `MI-BENCH-05` and `asset_id` `MI-BENCH-06`, whose underlying asset references remain governed by Asset Foundation. | Nested citation preserves both Market Intelligence and Asset Foundation ownership |
| PGV-06 | A downstream Portfolio Composition cites and carries the complete PGV-01 declaration beside the independently cited M42-WP2 Portfolio Base Currency coordinate. | Adjacency preserves distinct owners and meanings; neither coordinate defaults, converts, or alters the other |
| PGV-07 | A downstream analytics capability reads the cited declaration under its own future authority, while this WP5 declaration contains no observation or comparison result. | The declaration remains descriptive; downstream use does not retroactively grant analytics authority to WP5 |

None of these vectors decides how declarations are represented, persisted,
transported, resolved, evaluated, compared, or enforced. None establishes how
many declarations a Portfolio Identity may have.

---

## 7. Negative Golden Vectors

These are prohibited documentary shapes. Their classification expresses
contract analysis only. It does not define executable validation, runtime
rejection, transaction refusal, error codes, or enforcement behavior.

| ID | Prohibited specimen | Contract breach |
|---|---|---|
| NGV-01 | “Use the currently selected portfolio.” | Ambient subject; no exact Portfolio Identity citation |
| NGV-02 | One declaration belongs to `PI-A` and `PI-B`. | A declaration must belong to exactly one Portfolio Identity |
| NGV-03 | `PI-A` is paired with two Accounting Scopes. | A declaration must reference exactly one corresponding Accounting Scope |
| NGV-04 | `PI-A` is paired with an Accounting Scope that does not correspond to it. | Redefines or breaks the cited Ledger & Accounting subject binding |
| NGV-05 | The declared name is omitted or inferred from the cited series. | Violates the explicit-name coordinate and introduces inference |
| NGV-06 | One declaration contains both Single and Category forms. | A declaration must contain exactly one declared value in exactly one closed form |
| NGV-07 | Single cites `MI-BENCH-01` and `MI-BENCH-02`. | Single requires exactly one Benchmark series citation |
| NGV-08 | Composite cites only `MI-BENCH-01`. | Composite requires more than one Benchmark series citation |
| NGV-09 | Explicitly None cites `MI-BENCH-01`. | Explicit absence cannot also select a series |
| NGV-10 | A missing declaration silently becomes Explicitly None. | Explicitly None is affirmative and cannot be inferred from missing state |
| NGV-11 | Explicitly None defaults to a broad equity index. | Introduces an ambient substitute and contradicts explicit absence |
| NGV-12 | Form is `Policy-derived`, `Allocation-derived`, `Custom`, or `Other`. | Adds an unconfirmed fifth form; Policy-derived remains withheld |
| NGV-13 | “Benchmark” is used as an abbreviation for Portfolio Benchmark Declaration. | Collides with Market Intelligence's reserved canonical noun |
| NGV-14 | A provider symbol is stored as the canonical Benchmark series reference. | Introduces provider mapping and a competing identifier |
| NGV-15 | The declaration contains current or historical Benchmark observations. | Acquires Market Intelligence observation/data semantics |
| NGV-16 | Composite declares weights, a formula, rebalancing dates, or calculation rules. | Adds benchmark construction, allocation, calculation, and maintenance semantics |
| NGV-17 | Category chooses a series by runtime lookup or provider response. | Adds selection, resolution, provider, and runtime semantics |
| NGV-18 | “Calculate portfolio return minus the declared Benchmark return.” | Adds benchmark-performance comparison and calculation |
| NGV-19 | “Use the declared Benchmark as the optimizer objective.” | Adds Decision Intelligence and executable optimization semantics |
| NGV-20 | “Allocate 60% to assets represented by the Benchmark.” | Adds allocation behavior |
| NGV-21 | “Only instruments in the declared Benchmark may be held or traded.” | Adds policy, eligibility, enforcement, and execution behavior |
| NGV-22 | “The declared Benchmark determines Portfolio Base Currency.” | Redefines a Ledger & Accounting coordinate and adds accounting semantics |
| NGV-23 | “Convert Benchmark observations into Portfolio Base Currency using the latest FX rate.” | Adds observation, clock, conversion, calculation, and accounting behavior |
| NGV-24 | The declaration changes Portfolio Identity or Accounting Scope. | Acquires Ledger & Accounting authority |
| NGV-25 | WP5 defines an asset alias, taxonomy, or identifier format for a cited series. | Acquires Asset Foundation vocabulary authority |
| NGV-26 | A document labels Portfolio Benchmark Declaration itself as bare Benchmark. | Erases the canonical ownership distinction |
| NGV-27 | “Reject a declaration whose series is unavailable.” | Adds availability evaluation, runtime validation, and refusal semantics |
| NGV-28 | A database table, JSON object, API field, event, command, or wire format is prescribed by this contract. | Introduces schema, persistence, serialization, API, or implementation authority |
| NGV-29 | “Every Portfolio Identity must have exactly one Portfolio Benchmark Declaration.” | Invents portfolio-level declaration cardinality not decided by this contract |
| NGV-30 | A downstream consumer enriches, repairs, substitutes, or remaps a cited series and attributes the result to WP5. | Violates exact citation, source ownership, and downstream authority |
| NGV-31 | A Composite declaration is treated as a Portfolio Intelligence-owned calculated Benchmark series. | Transfers Market Intelligence calculation, observation, and maintenance ownership |

No negative vector authorizes the behavior it illustrates. “Prohibited” is a
documentary boundary classification, not an operational verdict.

---

## 8. Downstream Authority

### 8.1 Exact handoff coordinate

After this contract is independently confirmed, M42-WP7 may receive one
complete Portfolio Benchmark Declaration coordinate consisting semantically
of:

1. the exact Portfolio Identity citation;
2. the exact corresponding Accounting Scope citation;
3. the explicit declared name;
4. exactly one declared Portfolio Benchmark value;
5. exactly one of the four closed forms; and
6. every exact Market Intelligence Benchmark series citation required by that
   form, or the explicit absence of such citations for Explicitly None.

Completeness means that no facet defined by §§3–4 is omitted, inferred,
replaced, repaired, or supplemented during handoff. It does not prescribe a
serialized envelope, field name, field order, identifier representation,
schema, canonical bytes, transport, runtime object, or implementation.

### 8.2 Permitted downstream use

Under its own separately confirmed authority, a downstream work package MAY:

- cite and carry the complete Portfolio Benchmark Declaration;
- compose it beside other independently owned coordinates while preserving
  every source owner and meaning; and
- define its own authorized composition or serialization concerns without
  attributing those concerns to WP5.

Future benchmark analytics or performance-comparison work may cite this
declaration only under separately established authority. This contract does
not pre-authorize that work or define any analytic input, method, output, or
result.

### 8.3 Prohibited authority transfer

This handoff grants no downstream authority to:

- omit, infer, default, enrich, repair, normalize, substitute, remap,
  reclassify, or reinterpret any declaration facet or cited reference;
- turn the declaration into a Benchmark observation or calculated series;
- acquire Market Intelligence observation, series, provider, data, or
  maintenance ownership;
- acquire Ledger & Accounting identity, scope, Base Currency, valuation,
  return, or conversion ownership;
- acquire Decision Intelligence policy, limits, optimizer, allocation, or
  execution authority;
- acquire Asset Foundation vocabulary or identifier authority;
- perform analytics or performance comparison under WP5 authority;
- derive a portfolio-level zero/one/many declaration rule; or
- attribute a schema, API, persistence model, serialization, provider mapping,
  runtime behavior, executable validator, or implementation to this contract.

The exact downstream boundary is:

> cite and carry the complete descriptive Portfolio Benchmark Declaration,
> preserving every meaning and owner, with no calculation, observation,
> analytics, performance comparison, policy, accounting behavior, enrichment,
> reinterpretation, or authority transfer.

---

## 9. Acceptance Criteria

This specification is acceptable only if Independent Review confirms all of
the following:

1. Portfolio Benchmark Declaration is the sole governed noun defined by this
   contract and remains solely owned by Portfolio Intelligence.
2. The bare noun Benchmark remains reserved for Market Intelligence and is
   never used as an abbreviation for Portfolio Benchmark Declaration.
3. Every declaration belongs explicitly to exactly one Portfolio Identity and
   references exactly one corresponding Accounting Scope.
4. Portfolio Identity and Accounting Scope remain solely owned by Ledger &
   Accounting and are cited without redefinition or ownership transfer.
5. The one-subject rule does not create a zero/one/many declarations-per-
   portfolio rule.
6. Every declaration has one explicit declared name, while WP5 defines no name
   syntax, identifier format, uniqueness, persistence, or serialization rule.
7. Every declaration declares exactly one complete Portfolio Benchmark value
   in exactly one closed form.
8. The only admitted forms are Single, Composite, Category, and Explicitly
   None.
9. Single cites exactly one canonical Market Intelligence Benchmark series;
   Composite cites at least two; Category cites one or more; Explicitly None
   cites none.
10. A Composite form remains one declared Portfolio Benchmark value even though
   it cites multiple underlying series.
11. Explicitly None is an affirmative valid declaration and is never
    collapsed into missing, unset, unknown, invalid, defaulted, or fallback
    state.
12. The Policy-derived form and every renamed target-allocation-derived
    equivalent remain withheld.
13. Every Benchmark series is cited exactly at its Market Intelligence-owned
    meaning, in the frozen `asset_id` citation format owned by Asset
    Foundation, with no invented identifier, no provider identifier, no
    provider mapping, and no redefinition, derivation, copying, observation,
    data, or maintenance authority.
14. Every referenced canonical asset vocabulary coordinate remains solely
    owned by Asset Foundation.
15. Portfolio Base Currency remains solely owned by Ledger & Accounting under
    frozen M42-WP2 authority and is neither defined, duplicated, extended, nor
    used as a declaration input, default, conversion instruction, or result.
16. The declaration is descriptive only and carries no executable,
    optimization, allocation, policy, accounting, provider, or implementation
    semantics.
17. No benchmark calculation, observation, provider, maintenance, analytics,
    performance comparison, recommendation, enforcement, or execution
    behavior appears in the contract.
18. No ambient subject, implicit default, inference, runtime lookup,
    resolution, repair, enrichment, substitution, or mapping appears.
19. Citation is explicitly non-transferring for Ledger & Accounting, Market
    Intelligence, Decision Intelligence, and Asset Foundation authority.
20. The positive vectors demonstrate all four forms — including the frozen
    weighted-blend-of-reference-series meaning for Composite and the frozen
    peer-standard-for-a-category-of-strategy meaning for Category — exact
    subject binding, the frozen `asset_id` citation format, nested source
    ownership, Base-Currency separation, and downstream carriage without
    adding behavior.
21. The negative vectors cover subject ambiguity, form/cardinality errors,
    bare-name collision, provider mapping, observations, calculations,
    analytics, optimization, allocation, policy, accounting, implementation,
    and downstream authority leakage.
22. The downstream handoff carries the complete declaration without omission,
    defaulting, enrichment, repair, reinterpretation, or ownership transfer.
23. Implementation, persistence, runtime, API, serialization, schema,
    provider-mapping, calculation, executable-validation, and enforcement
    authority remain `NONE`.
24. Creation of this contract modifies no repository file outside this new
    M42-WP5 specification.
