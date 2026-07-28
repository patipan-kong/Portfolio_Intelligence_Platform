# M43-WP2 — Portfolio Measure Definition, Method Version, and Applicability Contract Specification

**Milestone:** M43 — Portfolio Analytics Contract Foundation  
**Work package:** M43-WP2 only  
**Artifact class:** Constitutional contract specification  
**Status:** `CORRECTED AFTER INDEPENDENT CONSTITUTIONAL REVIEW — REQUIRES INDEPENDENT CONFIRMATION`  
**Runtime authority:** `NONE`  
**Source-code authority:** `NONE`  
**Persistence/API/UI authority:** `NONE`  
**Implementation authority:** `NONE`  
**Provider authority:** `NONE`  
**Production-method authority:** `NONE`  
**Executable-validation authority:** `NONE`

## 1. Purpose and controlling authority

This artifact specifies only the M43-WP2 constitutional contracts required by
the frozen
[M43 Architecture and Implementation Plan](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§9:

1. Portfolio Measure Definition identity and revision;
2. immutable Portfolio Method Version identity;
3. Definition-level and Method-Version-level applicability requirements;
4. exact calculation-dependency declaration and closure;
5. compatibility rules;
6. invariants for a future registry;
7. the future non-production method-specification gate; and
8. positive and negative documentary vectors.

The commissioning authority states that M43 Architecture and M43-WP1 are
`COMPLETE AND FROZEN` and that Independent Constitutional Confirmation is
`APPROVED`. That commissioning record is controlling for this work package.
The repository-local M43 and WP1 status headers have not been synchronized to
that state. WP2 neither reopens nor edits those canonical artifacts.

This specification relies on the exact meanings and sole ownership confirmed
by
[M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md):

- Portfolio Measure;
- Portfolio Measure Definition;
- Portfolio Method Version;
- Portfolio Measure Subject;
- Portfolio Analytics Input Manifest;
- Portfolio Measurement Window;
- Portfolio Input Sufficiency;
- Portfolio Measure Result;
- Portfolio Computation Outcome;
- Portfolio Deterministic Calculation; and
- the exact reuse of the existing Degraded State grammar, with no
  `Portfolio Degraded State` noun.

The M41 contract is reused only as a mechanical precedent. No M41
Market-Intelligence-owned type, subject, method, requirement, or result is
reused or widened to accept a Portfolio.

### 1.1 External governance dependency

The independent WP2 review confirmed that the repository-local WP1
effectivity evidence remains unsynchronized: no repository-local WP1
independent-confirmation artifact exists, the WP1 header still requires
independent confirmation, and the WP1-authorized Glossary synchronization has
not been applied. This is not a WP2 contract defect and does not authorize WP2
to modify M43 Architecture, WP1, or `docs/GLOSSARY.md`.

Before WP2 independent confirmation is recorded, the separately authorized
WP1 confirmation workflow MUST:

1. record the WP1 independent confirmation under its own authority;
2. perform and verify the WP1 §9.2/§9.4 Glossary synchronization; and
3. record activation of the standing `M43-WP6 BLOCKED — GOVERNANCE CORRECTION
   REQUIRED BEFORE WP6` item required by WP1 §7.4.

WP2 records this as an external, fail-closed governance dependency only.
M-3 is therefore `PARTIALLY ACCEPTED`: its dependency is recorded here, while
its required repository changes remain exclusively in the independently
authorized WP1 confirmation workflow.

## 2. Normative boundary

### 2.1 In scope

WP2 establishes the complete specification-time structure needed for two
independent readers to identify the same Portfolio Measure Definition, the
same Portfolio Method Version, the same applicability result for a supplied
documentary context, and the same closed dependency set.

### 2.2 Out of scope

WP2 does not specify or authorize:

- a concrete Portfolio measure, formula, named metric, statistical convention,
  worked numerical calculation, or production method;
- the Portfolio Measure Subject fields or the Portfolio Analytics Input
  Manifest schema, ordering, identity, conflict, or serialization rules
  reserved to WP3;
- temporal, currency, calendar, benchmark-alignment, risk-free-input,
  annualization, arithmetic, rounding, or partial-window semantics reserved
  to WP4;
- result identity, value shape, outcome values, sufficiency classification,
  Degraded State carriage, Provenance carriage, or canonical result
  serialization reserved to WP5;
- the performance, risk, benchmark-relative, or attribution method
  specifications reserved to WP6–WP8;
- a registry implementation, executable gate, kernel, adapter, schema,
  persistence model, cache, scheduler, endpoint, user interface, migration,
  test runner, or conformance harness;
- admission, activation, availability, or discoverability of any production
  method; or
- any modification to M1–M42, M43 Architecture, M43-WP1, or
  `docs/GLOSSARY.md`.

Every example and vector in this work package is documentary and
non-production.

## 3. WP2-local vocabulary gate

WP2 introduces no new constitutional noun. The following possible nouns were
tested under the frozen downstream vocabulary rule:

| Candidate phrase | Disposition | Reason and routing |
| --- | --- | --- |
| Portfolio Applicability Requirement | `REJECT` | Applicability is an embedded contract property expressed by ordinary requirement records; it is not an independently owned business object |
| Portfolio Definition Revision | `REJECT` | Revision is a required identity field of Portfolio Measure Definition, not a separate object or version axis |
| Portfolio Calculation Dependency | `REJECT` | “Governed calculation dependency” remains ordinary descriptive language for an exact dependency retaining its existing owner |
| Portfolio Measure Family | `REJECT` | The permitted family labels in §5 are closed field values, not independently governed objects |
| Portfolio Method Admission | `REJECT` | The future gate makes a binary specification-conformance decision; WP2 admits neither an object nor a production method |

“Applicability requirement,” “dependency declaration,” “compatibility
classification,” “future gate,” and “future registry” are ordinary contract
language. They are not capitalized canonical terms, do not receive semantic
ownership, and must not be placed in the Glossary. Consequently WP2 requires
no Glossary synchronization.

## 4. Ownership and authority preservation

| Concern | Sole owner | WP2 treatment |
| --- | --- | --- |
| Portfolio Measure Definition, Portfolio Method Version, and Portfolio-derived measure meaning | Portfolio Intelligence | Specified here |
| Portfolio Identity, Accounting Scope, Membership, Base Currency, lifecycle state, ledger events, replay, holdings, cash, cost basis, and snapshots | Ledger & Accounting | Exact references or evidence only; never redefined |
| Portfolio Composition and Portfolio Benchmark Declaration | Portfolio Intelligence under frozen M42 | Exact references only; no mutation, inference, or override |
| Market observations, Market Measure Results, FX, calendars, benchmark observations, and market reference measures | Market Intelligence | Exact governed evidence or dependency references only |
| Asset identity, currency dimension, Unit Semantics, Asset Classification, and taxonomy | Asset Foundation | Exact versioned references only |
| Provenance meaning and capture | Connectivity & Ingestion | Already-captured Provenance may later be carried; never recaptured here |
| Recommendations, constraints, optimization, and execution plans | Decision Intelligence | Excluded |
| Grades, causal evaluation, reliability, and human-vs-AI evaluation | Trust & Evaluation | Excluded |
| Cross-portfolio exposure and net worth | Wealth Intelligence | Excluded |
| Rendering and interaction | Experience Platform | Downstream rendering only; computes nothing |

Custody, invocation, storage, execution, rendering, or review does not
transfer semantic ownership.

## 5. Portfolio Measure Definition contract

### 5.1 Exact meaning and owner

A Portfolio Measure Definition is the immutable semantic identity and
revision of one kind of Portfolio Measure, stating what the measure means
independently of any particular calculation method, invocation, or result.

Its sole semantic owner is Portfolio Intelligence.

### 5.2 Canonical identity

The canonical identity of one Portfolio Measure Definition is the exact pair:

```text
(definition identifier, revision)
```

The definition identifier is a stable, opaque, platform-assigned ASCII
identifier. The revision is a positive base-10 integer with no leading zero.
The identifier is never a formula name, provider term, display label, asset
identifier, Portfolio identifier, storage key, or implementation symbol.

Two records carrying the same canonical identity MUST be byte-for-byte
equivalent in every normative field once WP5 canonical serialization exists.
Before WP5, independent documentary comparison MUST find every normative
field equal. Any new candidate sharing an already accepted identity is an
identity collision and the candidate fails closed, whether its content
differs or is identical. The previously accepted immutable record is
unchanged. If two candidates in the same atomic candidate set collide, both
fail. A collision is never merged or silently deduplicated.

Identity never depends on location, ordering in a document, “latest,” clock
time, runtime availability, provider state, or registry build order.

### 5.3 Required normative fields

A Portfolio Measure Definition MUST contain exactly the following normative
fields:

| Field | Required content |
| --- | --- |
| Definition identifier | Stable identifier satisfying §5.2 |
| Revision | Positive integer satisfying §5.2 |
| Semantic statement | Provider-neutral, implementation-neutral statement of the single Portfolio-derived question answered; it MUST NOT contain a formula or judgment |
| Measure-kind label | Exactly one of `PERFORMANCE`, `RISK`, `BENCHMARK_RELATIVE`, or `DETERMINISTIC_CONTRIBUTION` |
| Subject declaration | Exact citation of Portfolio Measure Subject and its frozen constraint to exactly one M42 Portfolio Composition representing one Portfolio Identity and its corresponding Accounting Scope |
| Permitted input-category set | A non-empty subset of the closed categories in §5.4, in ascending code-point order |
| Applicability requirement set | Zero or more records conforming to §7, in ascending requirement-key order |

No omitted field receives a default. Non-normative annotations such as a
display label, prose rationale, review record, or document location MUST NOT
participate in identity or semantic interpretation and MUST be mechanically
separable from the normative record.

The measure-kind labels are routing labels within this contract. They do not
admit any concrete measure or method and do not transfer ownership.

### 5.4 Closed permitted input categories

The permitted input-category set may contain only:

1. `PORTFOLIO_COMPOSITION` — one exact M42 Portfolio Composition;
2. `LEDGER_DERIVED_EVIDENCE` — exact evidence retaining Ledger & Accounting
   ownership;
3. `MARKET_EVIDENCE` — exact M39 observations or M41 Market Measure Results;
4. `ASSET_FOUNDATION_REFERENCE` — exact identity, classification, currency,
   unit, or taxonomy references;
5. `INVOCATION_PARAMETER` — only a choice a confirmed method contract
   explicitly classifies as invocation-bound;
6. `CALCULATION_DEPENDENCY` — an exact governed calculation dependency; and
7. `CAPTURED_PROVENANCE` — already-captured Provenance associated with an
   input.

This is a permission ceiling, not a claim that every invocation must contain
every permitted category. Exact manifest entries and sufficiency are deferred
to WP3 and WP5.

An invocation parameter MUST NOT establish or override Portfolio Benchmark
Declaration, risk-free input, annualization basis, calendar authority,
Portfolio Base Currency, lifecycle state, Provenance, or any governed evidence
or calculation dependency.

### 5.5 Revision and immutability rules

Every revision remains immutable and exactly referenceable forever.

A record may retain the same definition identifier at a higher revision only
when all of the following hold:

1. the semantic statement answers the same Portfolio-derived question;
2. the measure-kind label is unchanged;
3. the subject declaration is unchanged;
4. no permitted input category required by a Portfolio Method Version already
   bound to an earlier revision is removed;
5. any applicability change is additive or narrowing for future bindings and
   does not retroactively change an earlier revision; and
6. the higher revision does not reinterpret any frozen external term.

A change to the question answered, measure-kind label, or subject meaning
requires a new definition identifier. A correction never edits an existing
revision in place.

No Portfolio Method Version automatically follows a higher revision. It
binds exactly one revision and remains bound to that revision.

### 5.6 Prohibited interpretations

A Portfolio Measure Definition is not:

- a formula, method, result, Portfolio Composition, Market Measure Definition,
  Asset Definition, accounting rule, benchmark declaration, or provider
  product;
- evidence that a Portfolio Method Version exists;
- evidence of production admission, runtime availability, correctness,
  suitability, or reliability; or
- authority to compute across Portfolios or to mutate any frozen input.

## 6. Portfolio Method Version contract

### 6.1 Exact meaning and owner

A Portfolio Method Version is one immutable, version-identified,
non-production calculation specification bound to exactly one Portfolio
Measure Definition and to explicit calculation dependencies.

Its sole semantic owner is Portfolio Intelligence. A dependency it cites
retains its existing owner.

### 6.2 Canonical identity

The canonical identity is the exact triple:

```text
(bound definition identifier, bound definition revision, method version)
```

The method version MUST be an ASCII `MAJOR.MINOR.PATCH` triple. Each component
is a non-negative base-10 integer with no leading zero except `0`. Suffixes,
ranges, wildcards, aliases, dates, build metadata, and “latest” are forbidden.

The identity tuple names exactly one immutable normative record. A new
candidate sharing an already accepted tuple collides and fails closed whether
its normative fields differ or are identical; the previously accepted record
is unchanged. Two colliding candidates in the same atomic candidate set both
fail. No collision is merged or silently deduplicated.

Every Portfolio Method Version identity is non-substitutable. Neither semantic
version ordering nor compatibility classification permits a caller, registry,
adapter, or runtime to replace one exact identity with another.

### 6.3 Required normative fields

| Field | Required content |
| --- | --- |
| Bound Portfolio Measure Definition reference | Exact definition identifier and revision |
| Method version | Exact `MAJOR.MINOR.PATCH` value |
| Specification reference | Exact immutable reference to one non-production calculation specification artifact; until WP6–WP8 admit concrete specifications, only documentary placeholders are permitted |
| Declared input-category use | Exact non-empty subset of the bound Definition's permitted input-category set, including `PORTFOLIO_COMPOSITION`, in ascending code-point order |
| Declared calculation dependencies | Closed list conforming to §8, in ascending dependency-key order |
| Applicability requirement set | Zero or more records conforming to §7, in ascending requirement-key order |
| Compatibility declaration | One value from §9.2 and the exact predecessor identity to which it applies, or `INITIAL` with no predecessor |
| Determinism conformance declaration | Exact value `CONFORMS_TO_PORTFOLIO_DETERMINISTIC_CALCULATION`, citing the frozen WP1 `PA-V10` meaning without restatement or waiver |

The specification reference does not admit the referenced calculation for
production. It only prevents a Portfolio Method Version from being a version
label detached from exact specification text.

No field may contain an executable body, module path, class, function,
provider identifier, endpoint, storage schema, cache key, clock value,
randomness, ambient default, or mutable process state.

### 6.4 Binding integrity and immutability

The bound Definition MUST exist at the exact cited revision. The declared
input-category use field makes mechanically checkable that every category the
Method Version uses is permitted by that Definition. Its applicability
requirements may equal or narrow the Definition requirements but MUST NOT
weaken, remove, contradict, or widen them.

Once specified, no normative field may change. Every change creates a new
Portfolio Method Version identity. A semantic-version increment does not edit
or supersede the older record and does not make the newer record production
admitted.

### 6.5 Portfolio Deterministic Calculation obligation

Every Portfolio Method Version MUST carry the §6.3 determinism conformance
declaration. The declaration is a specification obligation, not executable
proof in WP2. A missing, altered, qualified, conditional, or waived
declaration fails the future gate.

The future WP3–WP5 contracts must make it possible for identical exact
Portfolio Measure Subject, Portfolio Analytics Input Manifest, invocation
parameters, Portfolio Method Version identity, dependency identities, and
dependency results to produce a byte-identical Portfolio Measure Result.
WP2 does not define those later contracts.

### 6.6 Prohibited interpretations

A Portfolio Method Version is not:

- a Market Intelligence Method Version, Asset Definition Version, library
  version, deployment version, API version, or provider version;
- a production method, runtime registration, implementation, availability
  promise, or preferred/default method;
- permission to select a benchmark, risk-free input, annualization basis,
  calendar, currency, fallback, or substitute dependency at invocation time;
  or
- a correctness, recommendation, confidence, evaluation, or trust claim.

## 7. Applicability contract

### 7.1 Contract placement

Applicability is not a third canonical object. It is expressed by embedded
requirement records in a Portfolio Measure Definition and a Portfolio Method
Version. The record structure below is ordinary contract syntax and creates
no new constitutional noun.

Definition requirements state conditions every realizing method must honor.
Method Version requirements may only narrow those conditions for that exact
method.

### 7.2 Required record fields

Each applicability requirement record MUST contain:

| Field | Required content |
| --- | --- |
| Requirement key | Stable, opaque ASCII key unique within the declaring record |
| Operand category | Exactly one of the values in §7.3 |
| Operand authority | Exact owning domain or exact controlling frozen contract |
| Operand name | Exact governed coordinate, declaration, category, parameter, or dependency key; no provider or implementation path |
| Operator | Exactly one operator permitted by §7.4 |
| Expected value | Canonical literal required by the operator, or explicitly absent for `PRESENT` |

Requirement keys are local identities only. They do not become canonical
business vocabulary.

### 7.3 Closed operand categories

| Operand category | What may be referenced |
| --- | --- |
| `SUBJECT_COORDINATE` | A coordinate within the exact-one-Portfolio subject boundary frozen by [M43 Architecture §7](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md#7-architectural-boundaries); WP3 will define the concrete Portfolio Measure Subject field set and operand names |
| `PORTFOLIO_DECLARATION` | An exact declaration already governed by M42, including Portfolio Base Currency, lifecycle state, or Portfolio Benchmark Declaration |
| `INPUT_CATEGORY` | One category from §5.4 |
| `INVOCATION_PARAMETER` | One exact parameter explicitly permitted by the bound Definition and Method Version |
| `CALCULATION_DEPENDENCY` | One dependency key declared by the Method Version under §8 |

The operand category does not grant ownership. The operand authority MUST
match the frozen owner. A mismatch makes the requirement malformed.

`INVOCATION_PARAMETER` and `CALCULATION_DEPENDENCY` are permitted only in a
Portfolio Method Version's applicability requirement set. A Portfolio Measure
Definition does not declare an invocation-parameter key or dependency key, so
a Definition-level requirement naming either category is malformed.

### 7.4 Closed operators and evaluation

The operators are:

- `PRESENT` — the exact operand exists with an exact governed value or
  resolved exact identity;
- `EQUALS` — the operand is present and exactly equals the declared canonical
  literal;
- `IN` — the operand is present and exactly equals one member of a non-empty,
  duplicate-free, ascending-code-point-ordered list of canonical literals;
  and
- `COUNT_AT_LEAST` — the exact count of entries in the named input category is
  greater than or equal to a non-negative integer literal.

`PRESENT` requires no expected value. `EQUALS` requires one literal. `IN`
requires one list. `COUNT_AT_LEAST` is valid only for `INPUT_CATEGORY` and
requires one non-negative integer.

Canonical literal encoding is delegated to the owning frozen contract and,
where not yet defined, to WP3–WP4. A WP2 requirement cannot invent or
normalize another owner's value. Until an exact literal encoding exists, a
concrete requirement using that literal cannot pass the future gate.

The same deferral gate applies to operands whose evaluation domain is not yet
confirmed:

- a concrete `SUBJECT_COORDINATE` requirement cannot pass the future gate
  until WP3 confirms the Portfolio Measure Subject field set and the exact
  operand name it uses; and
- a concrete `COUNT_AT_LEAST` requirement cannot pass the future gate until
  WP3 confirms manifest-entry identity, duplicate, conflict, and counting
  semantics for the named input category.

More generally, a concrete requirement cannot pass while the governing
contract for its operand name, value domain, identity, or count remains
unconfirmed. Documentary contexts may state values expressly to demonstrate
the binary evaluation rule, but that demonstration is not candidate
admission.

For a supplied documentary calculation context, each well-formed requirement
returns exactly `MET` or `UNMET`:

- the operator's condition true yields `MET`;
- the operator's condition false yields `UNMET`;
- a missing, unresolved, ambiguous, conflicting, wrong-owner, or non-canonical
  operand yields `UNMET`; and
- malformed requirements are rejected at specification review and are never
  evaluated.

The overall applicability result is `APPLICABLE` if and only if every
Definition requirement and every Method Version requirement is `MET`.
Otherwise it is `INAPPLICABLE`. There is no third, partial, provisional,
confidence-weighted, or fallback result.

`MET`, `UNMET`, `APPLICABLE`, and `INAPPLICABLE` are closed documentary result
tokens in this contract, not new business nouns, Portfolio Computation
Outcome values, Degraded States, or Portfolio Input Sufficiency values.

### 7.5 Orthogonality

Applicability asks whether the declared kind of subject and input conditions
permit use of an exact Portfolio Method Version in principle.

Portfolio Input Sufficiency, reserved to WP5, asks whether the complete exact
inputs for one invocation are sufficient to calculate a result. An
`APPLICABLE` determination does not imply sufficient inputs, successful
computation, value presence, production admission, or runtime availability.
An `INAPPLICABLE` determination is not a Degraded State and not a Portfolio
Computation Outcome.

### 7.6 Fail-closed rules

No unmet or malformed requirement may trigger:

- another Portfolio Method Version;
- a default, fallback, heuristic, best-effort, or partial calculation;
- a caller-supplied governed value;
- inference from Current Selection, Workspace, wall-clock time, provider
  state, storage state, or cross-portfolio state; or
- weakening of a Definition requirement by a Method Version.

## 8. Calculation-dependency contract

### 8.1 Declaration record

Every declared calculation dependency MUST contain:

| Field | Required content |
| --- | --- |
| Dependency key | Stable opaque ASCII key unique within the declaring Portfolio Method Version |
| Owning domain | Exact constitutional owner of the dependency |
| Dependency contract kind | Exact existing governed contract type; it is never inferred from a module or provider |
| Dependency identifier | Exact stable identifier under the owning contract |
| Dependency version | Exact immutable version under the owning contract |

All dependencies are mandatory. Optional, preferred, default, range-bound, or
fallback dependencies are forbidden. A method with no dependencies declares
an explicit empty list.

The list MUST be duplicate-free and ordered by dependency key in ascending
Unicode code-point order. No two keys may resolve to the same
`(owning domain, contract kind, identifier, version)` tuple within one Method
Version.

### 8.2 Closure

Dependency closure is the transitive set containing every directly declared
dependency and every exact dependency declared by those dependencies.

A Portfolio Method Version passes closure only when:

1. every direct and transitive reference resolves to exactly one immutable,
   governed version;
2. every owner and contract kind match the controlling frozen authority;
3. every dependency declaration is itself closed;
4. no cycle reaches the declaring Portfolio Method Version or repeats a node
   in the same traversal;
5. no version range, alias, “latest,” dynamic lookup, provider identifier, or
   ambient resolution is present; and
6. two independent traversals produce the same set of exact dependency
   tuples.

Unresolved, ambiguous, conflicting, duplicated, or cyclic closure rejects the
Portfolio Method Version. It never degrades, substitutes, or truncates the
dependency set.

### 8.3 Evidence is not a dependency declaration

Ledger-derived evidence, observations, Market Measure Results, Asset
Foundation references, and captured Provenance are invocation inputs to be
bound by WP3. They MUST NOT be smuggled into a dependency declaration merely
to avoid the future manifest contract.

Conversely, an exact governed calculation dependency MUST NOT be supplied or
overridden as a free invocation parameter.

## 9. Compatibility and non-substitutability

### 9.1 Definition revisions

Definition revision compatibility is directional:

- a later revision is `DEFINITION_COMPATIBLE` with an earlier revision only
  when every rule in §5.5 holds;
- otherwise it requires a new definition identifier and cannot be described
  as a revision; and
- compatibility never changes an existing Method Version's exact binding.

### 9.2 Method Version change classes

Each non-initial Portfolio Method Version declares exactly one predecessor and
one of:

| Declaration | Permitted specification relationship |
| --- | --- |
| `PATCH_COMPATIBLE` | Same outputs and applicability for every input in the predecessor's domain; only non-semantic correction or clarification |
| `MINOR_COMPATIBLE` | Same outputs for every input in the predecessor's domain; applicability may be additively broadened only where the exact bound Definition permits it |
| `MAJOR_CHANGE` | Output semantics, dependency semantics, applicability over the overlapping domain, or another calculation-significant rule may differ |
| `INITIAL` | No predecessor exists |

A changed dependency identifier or version is never
`PATCH_COMPATIBLE`. It is `MINOR_COMPATIBLE` only if documentary proof
establishes identical outputs throughout the predecessor's domain; otherwise
it is `MAJOR_CHANGE`.

The version triple MUST reflect the declaration relative to the predecessor:

- `PATCH_COMPATIBLE` increments PATCH by exactly one and leaves MAJOR and
  MINOR unchanged;
- `MINOR_COMPATIBLE` increments MINOR by exactly one, leaves MAJOR unchanged,
  and resets PATCH to zero; and
- `MAJOR_CHANGE` increments MAJOR by exactly one and resets MINOR and PATCH to
  zero.

No greater increment, skipped version, or non-adjacent predecessor is
permitted within one declared lineage.

A predecessor MUST bind the same Portfolio Measure Definition identifier. It
MAY bind either the same Definition revision or an earlier revision for which
the successor's bound revision is `DEFINITION_COMPATIBLE` under §9.1. Every
intervening Definition revision MUST also be `DEFINITION_COMPATIBLE`.
Cross-revision lineage does not rebind or mutate the predecessor, and the
compatibility declaration is evaluated over the predecessor's domain. A
Method Version bound to a different Definition identifier starts a distinct
lineage with `INITIAL`.

### 9.3 No automatic substitution

All compatibility declarations are documentary promises subject to future
conformance evidence. They do not authorize automatic upgrade, downgrade,
fallback, range resolution, default selection, or replacement. Every
invocation and result must cite one exact Portfolio Method Version.

## 10. Future non-production method-specification gate

### 10.1 Gate predicates

A future, separately authorized mechanism evaluating a candidate Portfolio
Measure Definition or Portfolio Method Version MUST check all applicable
predicates:

1. required-field completeness and absence of implicit defaults;
2. exact owner and five-part constitutional boundary compliance under
   [M43-WP1 §2](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md#2-constitutional-admission-procedure):
   permitted subject, permitted inputs, output meaning, exactly one owner,
   and prohibited semantics;
3. canonical identity syntax and unconditional uniqueness;
4. same-identity field equality and duplicate rejection;
5. Definition revision compliance under §5.5;
6. exact Definition binding integrity;
7. input-category subset compatibility;
8. applicability record well-formedness, owner correctness, confirmed operand
   name/value/count domain, canonical literal availability, ordering, valid
   declaring-record placement, and no Definition weakening;
9. dependency uniqueness, exact resolution, ordering, transitive closure, and
   acyclicity;
10. compatibility-declaration and version-increment consistency;
11. specification-reference exactness and immutability;
12. Portfolio Deterministic Calculation obligation;
13. absence of provider, ambient, runtime, implementation, judgment,
    cross-portfolio, and forbidden caller-override semantics; and
14. explicit proof that the candidate is non-production.

Failure of any predicate rejects the entire candidate. There is no partial,
provisional, warning-only, or fallback admission.

### 10.2 Gate result and non-exercise

The future gate has exactly two documentary specification-conformance results:
`ACCEPTED_FOR_NON_PRODUCTION_SPECIFICATION` and `REJECTED`.

The first result means only that the framework record conforms to this WP2
contract. It does not admit a formula, named metric, implementation, registry
entry, runtime method, endpoint, or production behavior. Production-method
admission requires separate authority outside M43.

WP2 specifies but does not build or exercise this gate. All WP2 examples
remain rejected as production methods regardless of documentary validity.

## 11. Future registry invariants

A future separately authorized registry holding these records MUST:

1. accept only records that passed the §10 gate;
2. build atomically and fail closed;
3. permit an empty set of production records;
4. preserve every admitted record immutably;
5. enforce unconditional identity uniqueness and reject identical duplicates;
6. resolve only exact identities, never “latest,” ranges, defaults, or aliases;
7. preserve exact Definition bindings and full dependency closure;
8. preserve canonical requirement and dependency ordering;
9. detect and reject cycles before a usable build exists;
10. produce equivalent content from the same exact admitted-record set,
    independent of build order, clock, process, storage, or provider state;
11. grant no owner, provider, capability, implementation, production, or
    runtime authority; and
12. never treat compatibility as permission to substitute identities.

No registry is created, named as a canonical noun, persisted, or operated by
WP2.

## 12. Documentary vectors

The associated constitutional artifacts are:

- [positive documentary vectors](m43/fixtures/M43_WP2_POSITIVE_DOCUMENTARY_VECTORS.md);
  and
- [negative documentary vectors](m43/fixtures/M43_WP2_NEGATIVE_DOCUMENTARY_VECTORS.md).

They are normative examples for independent reading and review. They are not
executable fixtures, numerical golden vectors, methods, registry entries, or
production admissions.

## 13. Relationship to later M43 work packages

- WP3 consumes exact Definition and Method Version identities and specifies
  the Portfolio Measure Subject and Portfolio Analytics Input Manifest.
- WP4 supplies the exact governed literal and binding semantics for temporal,
  currency, calendar, benchmark, risk-free, annualization, and arithmetic
  concerns.
- WP5 specifies sufficiency, outcome, Degraded State, result identity,
  Provenance carriage, and serialization.
- WP6–WP8 may propose concrete non-production method specifications only
  after their own prerequisites and governance gates are satisfied.
- WP9 may design implementation and cutover only under its separate frozen
  scope.

WP2 creates no authority for any later work package to begin early. In
particular, it does not alter the WP1-recorded WP6 governance block.

## 14. Prohibited interpretation corpus

Every statement below is constitutionally invalid:

1. “A Portfolio Measure Definition is a formula.”
2. “A Portfolio Method Version is production-ready because it has a semantic
   version.”
3. “The latest compatible method may be selected automatically.”
4. “A Method Version may widen or weaken its Definition requirements.”
5. “An applicability result is Portfolio Input Sufficiency, a Portfolio
   Computation Outcome, or a Degraded State.”
6. “An unmet requirement may invoke a fallback method.”
7. “A request benchmark, risk-free rate, annualization basis, calendar, or
   Portfolio Base Currency is an invocation parameter.”
8. “A dependency range, provider symbol, cache entry, or live lookup is an
   exact dependency.”
9. “Missing dependency closure may be treated as partial applicability.”
10. “A Portfolio Method Version may bind to an unspecified or latest
    Definition revision.”
11. “A compatible revision retroactively changes an older Method Version.”
12. “Market Intelligence's Method Version may be widened to accept a
    Portfolio.”
13. “Ledger evidence ownership transfers Portfolio measure semantics to
    Ledger & Accounting.”
14. “A registry implements or admits a production method merely by containing
    a conforming specification.”
15. “Experience may choose, substitute, or calculate a method.”
16. “A WP2 documentary vector is an executable fixture or production
    catalog entry.”
17. “WP2 authorizes code, persistence, API, UI, provider, or operational
    changes.”

## 15. Completion and confirmation gate

WP2 is complete only when independent review confirms:

1. every required field has exactly one owner and no ownership leakage;
2. two readers derive the same Definition and Method Version identities;
3. same-identity collisions fail in both differing-content and
   identical-duplicate cases;
4. every version remains exact and non-substitutable;
5. two readers derive the same requirement-level and overall applicability
   results for every documentary vector;
6. two readers derive the same direct and transitive dependency set and reject
   ambiguity, duplication, and cycles;
7. Definition and Method compatibility rules cannot mutate old bindings;
8. the future gate and registry remain specification-only;
9. no new canonical noun or Glossary change is required;
10. no concrete formula, named metric, manifest, arithmetic convention, result
    contract, runtime, implementation, or production method is admitted;
11. no M1–M42, M43 Architecture, or M43-WP1 artifact is modified; and
12. the only changed files are this specification and its two WP2 documentary
    vector artifacts; and
13. the external WP1 governance dependency in §1.1 is completed under its own
    authority before WP2 confirmation is recorded.

Until that confirmation, this WP2 corpus is proposed and non-effective.

## 16. Required-corrections change summary

This correction pass implements only the independent review's authorized WP2
findings:

1. added the declared input-category use and determinism conformance fields to
   the complete Portfolio Method Version field closure;
2. closed the applicability deferral gate over unconfirmed subject-coordinate
   names and manifest-entry count semantics;
3. restricted invocation-parameter and calculation-dependency applicability
   operands to Method Version records;
4. cited the frozen subject boundary and the complete WP1 five-part gate;
5. fixed semantic-version increment magnitude and cross-Definition-revision
   lineage;
6. added positive coverage for `EQUALS`, `IN`, `MINOR_COMPATIBLE`, and
   `MAJOR_CHANGE`;
7. added the requested caller-override and normative-rule negative coverage;
8. scoped artificial dependency vectors to closure-algorithm and traversal
   demonstrations rather than accepted governed closure; and
9. recorded M-3 as an external WP1 confirmation dependency without modifying
   or attempting to resolve any WP1 artifact.

No canonical noun, owner, capability, formula, runtime, implementation, or
production-method authority was added. No M43 Architecture, WP1, Glossary, or
other repository file was changed.

## 17. Required-corrections response matrix

| Finding | Classification | Constitutional justification and implemented response |
| --- | --- | --- |
| `M-1` | `ACCEPTED` | §6.3 now declares exact input-category use and exact Portfolio Deterministic Calculation conformance as required normative fields. §§6.4–6.5 and gate predicates 7/12 are now mechanically checkable from record content; P-02 carries both fields. |
| `M-2` | `ACCEPTED` | §7.4 now prevents a concrete subject-coordinate or entry-count requirement from passing the future gate before WP3 confirms its field names and identity/duplicate/conflict/count semantics. Documentary evaluation remains possible only from expressly supplied context and creates no admission. |
| `M-3` | `PARTIALLY ACCEPTED` | §1.1 and completion criterion 13 record the unsatisfied WP1 confirmation, Glossary synchronization, and standing WP6-block activation as a fail-closed external governance dependency. Performing those changes would exceed WP2 authority and remains assigned to the independently authorized WP1 confirmation workflow. |
| `M-4` | `ACCEPTED` | N-54–N-58 exercise request-supplied benchmark, risk-free input, annualization basis, calendar authority, and inferred Base Currency prohibitions individually. |
| `M-5` | `ACCEPTED` | P-09 demonstrates `EQUALS` and `IN` with exact frozen M42-WP5 literals; P-10 and P-11 demonstrate exact `MINOR_COMPATIBLE` and `MAJOR_CHANGE` increments and resets. |
| `m-1` | `ACCEPTED` | §9.2 now requires an increment of exactly one on the selected semantic-version axis and rejects greater or skipped increments. |
| `m-2` | `ACCEPTED` | §9.2 now permits lineage across revisions only for the same Definition identifier and only through directionally compatible revisions; P-12 and N-74 cover the permitted and prohibited cases. |
| `m-3` | `ACCEPTED` | §7.3 makes `INVOCATION_PARAMETER` and `CALCULATION_DEPENDENCY` malformed in a Definition-level requirement because only a Method Version declares their exact keys. |
| `m-4` | `ACCEPTED` | N-59–N-72 cover identical Method duplication, atomic collisions, missing fields, formula text, Definition revision conditions 3–5, ordering, forbidden field values, and ambient/cross-portfolio inference. |
| `m-5` | `ACCEPTED` | P-04 and P-05 now state expressly that artificial contract kinds demonstrate traversal only and cannot satisfy §8.2(2) or pass the future gate. |
| `m-6` | `ACCEPTED` | Gate predicate 2 now cites M43-WP1 §2 and enumerates all five boundary questions without altering them. |
| `m-7` | `ACCEPTED` | §7.3 now cites M43 Architecture §7 as the frozen subject boundary and leaves concrete Portfolio Measure Subject fields and operand names to WP3. |
