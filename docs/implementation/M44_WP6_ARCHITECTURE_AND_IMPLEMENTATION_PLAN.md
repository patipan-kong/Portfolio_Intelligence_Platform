# M44-WP6 — Portfolio Analytics Normative Semantics: Architecture and Implementation Plan

**Work package:** M44-WP6

**Artifact class:** Non-normative architecture and implementation planning document

**Candidate status:** `PLANNING CANDIDATE — NOT AUTHORIZATION`

**Authorizing milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics Foundation

**Planning authority:** Documentary planning only

**Normative-specification authority:** `NONE` until the constitutional entry condition in §2 is satisfied through separately authorized future governance

**Implementation authority:** `NONE`

**Runtime authority:** `NONE`

**Source-code authority:** `NONE`

**Persistence/schema/migration authority:** `NONE`

**API/transport authority:** `NONE`

**UI/presentation authority:** `NONE`

**Provider authority:** `NONE`

**Production-method authority:** `NONE`

**Executable-validation authority:** `NONE`

**Frozen-artifact-amendment authority:** `NONE`

---

## 1. Candidate identity and repository status

This document materializes the architecture and implementation plan for
M44-WP6. It is additive, documentary, and non-normative. It neither begins the
frozen M44-WP6 normative-authoring scope nor changes the constitutional state
that currently withholds it.

The controlling architecture is frozen at
[M44 Architecture and Implementation Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md).
The planning candidate must be read with its
[Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md), not as an alternate
constitutional source.

The effective repository state consumed by this plan is:

| Matter | Effective state | Planning consequence |
| --- | --- | --- |
| M44-WP1 | `COMPLETE AND FROZEN` | Supplies the inherited-gate, vocabulary, and negative-corpus baseline. |
| M44-WP4 | `COMPLETE AND FROZEN`; `G-3 OPEN — PARTIAL` | The strict substantive-entry prerequisite for WP6 is not met. |
| M44-WP5 | `COMPLETE AND FROZEN`; Annualization Basis owner `MARKET INTELLIGENCE`; `G-4 OPEN` | Supplies the exact Component G named-unavailability binding. |
| M44 §12.1.1 checkpoint | `STOP` | Remains the current disposition and cannot be overridden by this plan. |
| M44-WP6 | `NOT REACHED — WITHHELD BY CHECKPOINT`; substantively unauthorized | Planning may proceed; normative authoring may not. |
| M44-WP7 | `NOT REACHED — WITHHELD BY CHECKPOINT`; substantively unauthorized | Remains strictly downstream of a future frozen WP6. |
| Implementation and runtime | `NONE` | No source, executable, or operational work is in scope. |

The authoritative records for those states are the
[M44-WP4 Freeze Record](M44_WP4_FREEZE_RECORD.md),
[M44-WP5 Freeze Record](M44_WP5_FREEZE_RECORD.md),
[Gate-State Checkpoint Disposition](M44_GATE_STATE_CHECKPOINT_DISPOSITION.md),
and [M44 Epic Closeout](M44_EPIC_CLOSEOUT.md). Where this candidate and a
frozen source could be read differently, the frozen source controls.

---

## 2. Constitutional entry condition

### 2.1 Planning may proceed now

M44-WP6 planning may proceed now. This candidate may define the intended
scope, dependency order, evidence model, review plan, and fail-closed
conditions for a future normative work package. Planning is not normative
authoring, gate disposition, implementation, or runtime authority.

The following status statements are preserved without qualification:

| Constitutional matter | Preserved planning rule |
| --- | --- |
| Planning status | M44-WP6 planning may proceed now. |
| Normative entry | Normative authoring may not begin while `G-3` remains `OPEN — PARTIAL`. |
| Checkpoint | The current checkpoint result remains `STOP`. |
| Annualization | `G-4 OPEN` is effective, frozen, and bindable only as named annualization unavailability. |
| Annualization prohibition | `G-4 OPEN` does not authorize invention of an annualization value, factor, alias, placeholder, or synthetic dependency. |
| Scope completeness | Components A–K form one atomic normative scope; partial authoring of A–J while K remains unformable is not permitted. |
| Substantive execution | M44-WP6 and M44-WP7 remain unauthorized for substantive execution. |
| Operational authority | Implementation and runtime authority remain `NONE`. |

### 2.2 Normative authoring entry condition

Normative authoring may begin only when all of the following are true:

1. a separately authorized future governance act explicitly authorizes
   substantive M44-WP6 work;
2. every required Portfolio Composition coordinate has an owner-supplied,
   exact, immutable canonical reference, so that `G-3` is validly established
   as `CLOSED`;
3. the future governance act re-verifies the checkpoint inputs and records an
   authorizing outcome without amending, reinterpreting, or silently ignoring
   the current `STOP`; and
4. M44-WP4 and M44-WP5 remain frozen and their cited outputs remain available
   at their exact canonical paths.

`G-3 OPEN — PARTIAL` is a strict prerequisite failure for M44-WP6. While that
state remains effective, normative authoring does not begin. This plan cannot
create the eight missing coordinate references, solicit them from their owning
domains, or convert routed open elements into supply.

### 2.3 `G-4` is bindable but not curative

`G-4 OPEN` is effective and frozen. It is not a prerequisite failure for a
lawfully authorized WP6, but it constrains Component G to the sole binding:

> annualization unavailable — named missing element and named owner

The [M44-WP5 Freeze Record](M44_WP5_FREEZE_RECORD.md) identifies the owner as
`MARKET INTELLIGENCE` and the absent element as an exact owner-published
Annualization Basis calculation-dependency contract kind together with its
exact identifier, immutable version, and canonical value bytes. `G-4 OPEN`
does not authorize an annualization value, factor, alias, placeholder,
synthetic dependency, ambient `252`, `365`, or `365.25`, caller override, or
new owner-domain contract.

### 2.4 Atomic scope rule

Components A–K form one atomic normative scope. Component K must serialize or
cite formable upstream canonical bytes, including Portfolio Composition bytes.
Partial authoring of Components A–J while Component K remains unformable is
not permitted. A partial semantic contract would not satisfy the frozen
M43-WP4 allocation, would not produce a complete deterministic boundary, and
must not be represented as a completed or partially executable WP6.

---

## 3. Problem statement

Portfolio Analytics requires one method-family-independent, deterministic
semantic foundation before any Portfolio Measure Definition, Method Version,
formula, result contract, or runtime realization can rely on it. The frozen
[M43-WP4 Constitutional Scope and Implementation Plan](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md)
allocates this foundation as Components A–K: time, currency, FX, calendars,
benchmarks, risk-free evidence, annualization, missing data, numeric
arithmetic, dependencies, and canonical serialization.

Absent that foundation, a downstream method could obtain material semantics
from a wall clock, host timezone, provider convention, library default,
ambient constant, request parameter, input ordering, compatible version, or
implicit arithmetic behavior. Those sources are non-deterministic,
non-auditable, or constitutionally unauthorized.

The current `G-3 OPEN — PARTIAL` state is additionally dispositive: without
formable Portfolio Composition bytes, Component K cannot close the subject and
manifest serialization boundary. WP6 must therefore preserve an executable
planning route while refusing substantive normative authoring until a lawful
entry condition is met.

---

## 4. Goals

This plan has the following goals:

1. define one complete, non-production normative semantic contract for
   Components A–K, conditional on lawful entry;
2. make every output-affecting choice explicit, exact, owned, immutable, and
   non-overridable;
3. preserve sole ownership of Portfolio, Ledger, Asset Foundation, Market
   Intelligence, and Connectivity & Ingestion facts and meanings;
4. bind `G-4 OPEN` as a named annualization unavailability without inventing a
   dependency or admitting an annualized method;
5. make every retained or rejected semantic auditable through documentary
   vectors and a normative-row-to-vector coverage ledger;
6. enable two independent readers to derive the same selections, semantic
   predicates, exact values, and canonical bytes; and
7. provide a clean, strictly downstream handoff to M44-WP7 without defining
   result classification, lineage, or runtime behavior.

---

## 5. Planning scope now

The scope available now is limited to non-normative planning:

- lock the frozen authority baseline and the exact paths each future WP6 row
  must cite;
- define the constitutional entry gate and a hard stop when it is unmet;
- map every Component A–K concern to its owner, evidence/dependency placement,
  prohibited defaults, downstream handoff, and required documentary vectors;
- define the staged authoring and independent-review sequence;
- define acceptance criteria, risk controls, and repository boundaries; and
- preserve the current `G-3 OPEN — PARTIAL`, `G-4 OPEN`, and checkpoint `STOP`
  states exactly as frozen.

This planning scope creates no normative row, no canonical value or byte
representation, no evidence contract, no method, and no gate disposition.

---

## 6. Conditional post-authorization normative scope

If and only if §2.2 is satisfied, M44-WP6's single normative specification
must discharge every frozen M43-WP4 component below.

| Component | Conditional normative responsibility |
| --- | --- |
| A — Portfolio Measurement Window | Define schema, cardinality, boundaries, time basis, timezone/fixed-offset or calendar-free behavior, identity, immutability, canonical bytes, and rejection rules. |
| B — Economic time, record time, and stable ordering | Select exact source-owned time coordinates for inclusion, cutoff, availability, reference period, alignment, and deterministic tie-breaking. |
| C — Portfolio Base Currency and FX | Require historical Base Currency and exact Market FX evidence; define direction, path, placement, timing, rounding, and fail-closed gap behavior. |
| D — Calendar and observation alignment | Define calendar-free or exact governed-calendar semantics, session and closure behavior, DST/leap handling, selection, joins, and ordering. |
| E — Benchmark alignment | Bind the exact Benchmark Declaration and Market evidence; preserve Explicitly None; define compatible windows, joins, gaps, and alignability predicates. |
| F — Risk-free evidence | Prove governed-evidence placement, reject dependency and caller placement, and specify exact evidence identity, term, timing, unit, transformation, and alignment. |
| G — Annualization-basis dependency | Bind the frozen `G-4 OPEN` named unavailability; prohibit every annualization-dependent normative closure until the owner-domain instrument exists. |
| H — Missing data, density, and partial windows | Distinguish absent input, authoritative absence, gaps, duplicates, conflicts, sparsity, asynchronous series, and partial windows; retain only fully specified handling modes. |
| I — Numeric model and arithmetic | Define exact numeric forms, lexical/byte form, precision, scale, quantization, rounding, exceptional values, operation order, and arithmetic predicates. |
| J — Dependency arithmetic | Define exact identity/version/value compatibility, use position, closure, non-substitutability, and failures for each admissible dependency. |
| K — Canonical serialization | Define tagged, injective, round-trippable, length-delimited, order-stable, locale-independent bytes and rejection rules, while preserving upstream bytes unchanged. |

The normative scope also includes the frozen M43-WP4 explicit no-default
matrix, the risk-free authority-class proof, the Component G binding,
documentary numerical vectors, and a complete normative-row-to-vector coverage
ledger.

---

## 7. Out-of-scope items

M44-WP6 planning and any future M44-WP6 normative authoring must not:

- close, reinterpret, or otherwise cure `G-3`, `G-4`, `G-5`, or the current
  checkpoint result;
- author the missing owner-domain canonical references or the Market
  Intelligence Annualization Basis instrument;
- define a Portfolio Measure Definition, Method Version, formula, exact method
  threshold, method admission, or production method;
- define Portfolio Input Sufficiency, Portfolio Computation Outcome, reason
  codes, Degraded State, result identity, value presence, lineage, Provenance
  carriage, result serialization, or hash stability; those belong to WP7;
- create, fetch, correct, map, enrich, interpolate as source truth, or select
  Market, Ledger, Asset Foundation, or Connectivity & Ingestion facts;
- amend accounting arithmetic, NAV, ledger replay, cost basis, cash-flow
  treatment, or [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md);
- select a provider, library, module, call site, algorithm implementation,
  transport, persistence form, API, schema, migration, cache, scheduler, UI,
  or deployment behavior; or
- create source code, executable fixtures, test runners, runtime behavior, or
  capability-completion claims.

---

## 8. Architecture

The architecture is a deterministic calculation-side interpretation layer. It
consumes exact, already-bound evidence and dependency values; it neither
obtains evidence nor classifies the final result.

```text
Frozen Method Version / immutable specification
  + exact Subject and Input Manifest
  + owner-governed Ledger, Asset, and Market evidence
  + formable Composition bytes (strict G-3 condition)
                         |
                         v
M44-WP6 normative semantics
  A–E  selection and alignment
  F–H  evidence, dependency, and completeness predicates
  I–J  exact arithmetic and dependency closure
  K    canonical representation
                         |
                         v
Deterministic semantic facts only
                         |
                         v
M44-WP7 result/sufficiency/outcome contract
```

The diagram is a dependency model, not a runtime component design. Every
input is bound before semantic interpretation; every output is a deterministic
semantic fact until WP7 maps it into result semantics.

### 8.1 Architectural layers

1. **Selection and alignment (A–E).** Establish the exact analytical window,
   controlling time, currency and FX interpretation, calendar behavior, and
   benchmark evidence alignment.
2. **Evidence and completeness (F–H).** Establish which exact evidence can be
   consumed, whether annualization is unavailable, and whether data-density or
   partial-window predicates hold.
3. **Exact calculation mechanics (I–J).** Eliminate ambient numeric behavior
   by fixing representations, operation order, rounding, and dependency
   closure.
4. **Canonical representation (K).** Give every WP6-owned rule and expected
   documentary value one unambiguous byte representation while embedding or
   citing upstream bytes unchanged.

### 8.2 Ownership-preserving boundary

The architecture relies on the frozen contracts for
[M43-WP2 Method Version](M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md),
[M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md),
[M43-WP3 Input Manifest](M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md),
and [M42-WP7 Portfolio Composition](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md).
Citation, arithmetic consumption, byte embedding, or transport custody never
transfers ownership.

Portfolio Intelligence owns only the analytical semantics allocated by the
frozen corpus. Ledger & Accounting retains historical Portfolio and accounting
facts; Asset Foundation retains identifiers and unit/currency references;
Market Intelligence retains FX, calendars, benchmark observations, and
observed risk-free facts; Connectivity & Ingestion retains Provenance meaning
and capture. The higher-order boundary is governed by the
[Platform Architecture](../architecture/platform_architecture.md).

---

## 9. Non-negotiable semantic rules

| Rule | Mandatory effect |
| --- | --- |
| Exact binding | Every output-affecting fact, dependency, version, role, time coordinate, and numeric rule is explicit and immutable. |
| No ambient defaults | No wall clock, host locale/timezone, provider convention, library default, request value, input order, cache, `latest`, range, or compatible version supplies semantics. |
| Fail closed | Missing, ambiguous, stale, incompatible, unversioned, cyclic, duplicate, or non-canonical input is rejected or produces a named semantic failure predicate; it is never repaired silently. |
| Owner preservation | WP6 consumes exact owner-governed evidence and never originates, normalizes as source truth, or reassigns it. |
| No result leakage | Components A–K produce predicates and canonical representations only; WP7 alone owns result classifications and envelopes. |
| `G-4` discipline | The named annualization unavailability blocks affected rows; it does not permit a factor, placeholder, alias, artificial dependency, or caller override. |
| Deterministic arithmetic | Numeric form, scale, precision, rounding/tie behavior, exceptional values, quantization points, and operation order are closed. |
| Canonical bytes | WP6 canonical forms are tagged, injective, length-delimited, round-trippable, order-stable, locale-independent, and reject alternate forms. |
| Vector derivation | Documentary vectors derive from confirmed normative rows; vectors never create missing semantics or authority. |
| Atomicity | A–K is one scope. A–J cannot be authored as a substitute for a complete WP6 contract while K remains unformable. |

---

## 10. Dependencies and required states

| Dependency | Required state before substantive WP6 | Effect on WP6 |
| --- | --- | --- |
| M44 Architecture and M44-WP1 | Frozen and available at exact cited paths | Supplies authority order, gate inventory, vocabulary, and negative corpus. |
| M44-WP4 / `G-3` | `G-3 CLOSED` | Strict prerequisite. Exact Composition bytes must be formable for Component K. |
| §12.1.1 checkpoint | Valid future authorizing disposition | The current `STOP` remains controlling until separately superseded by lawful governance. |
| M44-WP5 / `G-4` | `OPEN — EFFECTIVE AND FROZEN` | Supplies Component G's named annualization unavailability. It does not block WP6 after `G-3 CLOSED`. |
| M43-WP4 | Frozen | Supplies the complete A–K allocation, no-default matrix, vector requirements, and acceptance criteria. |
| M43-WP2 and M43-WP3 | Frozen and formable | Supply immutable Method Version, Subject, Manifest, role, dependency, identity, ordering, and byte-binding constraints. |
| M42 contracts | Frozen | Supply Portfolio Identity, Accounting Scope, Membership, Base Currency, Investment Universe, Benchmark Declaration, Lifecycle State, Provenance carriage, and Composition boundaries. |
| M39/M41 contracts | Frozen | Supply the governed Market Observation and Market Measure evidence boundary. |
| Market Intelligence annualization instrument | Absent; not a WP6 prerequisite | Its absence must be bound as Component G unavailability. Annualization-dependent later work remains blocked. |

The `G-3` prerequisite is intentionally narrower and stricter than `G-4`.
M44-WP6 must not equate the two or use the bindable annualization blockage to
justify work past the unformable Composition boundary.

---

## 11. Internal execution stages

The following stages are an internal future execution sequence, not new M44
constitutional work packages. Stages WP6-1 through WP6-6 cannot begin unless
WP6-0 passes. No stage has source-code or runtime authority.

### WP6-0 — Entry authorization

- Verify the separately authorized future governance act, `G-3 CLOSED`
  evidence, and an authorizing checkpoint disposition.
- Reconfirm that M44-WP4 and M44-WP5 remain frozen and that their exact output
  paths resolve.
- Verify that the current `STOP` is not being bypassed by implication.
- Stop immediately if any condition is absent. WP6-0 does not create missing
  references, close a gate, or author any normative row.

### WP6-1 — Baseline lock and semantic-surface register

- Build a complete A–K register recording: concern, exact owner, upstream
  contract, input role/dependency placement, immutable binding, prohibited
  defaults, downstream handoff, and vector obligations.
- Record every frozen source path and section used by the future normative
  artifact.
- Run the vocabulary gate for any unavoidable new governed noun; the expected
  result is no new noun.
- Establish a conflict scan for ambient defaults, provider semantics, early
  result semantics, early formulas, and frozen-artifact amendments.

### WP6-2 — Context and alignment semantics

- Author Components A–E in dependency order: Measurement Window; economic
  versus record time and ordering; Base Currency and FX; calendar and
  observation alignment; then benchmark alignment.
- Bind only exact declared Benchmark evidence and preserve Explicitly None.
- Define no formula, result classification, provider lookup, or fallback
  window.

### WP6-3 — Evidence and completeness semantics

- Author Components F–H.
- Complete the risk-free authority-class proof before accepting any risk-free
  evidence role; reject dependency and caller placement if the proof requires.
- Bind Component G exactly to the frozen named annualization unavailability.
- Define missing-data, gap, density, duplicate, asynchronous, and
  partial-window predicates without converting them into WP7 outcomes.

### WP6-4 — Arithmetic and dependency semantics

- Author Components I–J.
- Fix numeric representation, canonical lexical form, working and output
  precision, rounding and ties, exceptional values, operation order, and
  negative-zero behavior.
- Define exact identity, immutable version, compatibility, arithmetic-use
  position, transitive closure, cycle rejection, and substitution rejection
  for constitutionally admissible dependencies.

### WP6-5 — Canonical serialization

- Author Component K only after WP6-0 establishes formable Composition bytes
  and all upstream bindings are exact.
- Define tagged, injective, round-trippable, length-delimited, order-stable,
  locale-independent encodings for every WP6-owned rule and expected value.
- Embed or cite M43-WP2, M43-WP3, and Composition bytes unchanged; reject
  unknown fields, alternate forms, trailing bytes, duplicate keys,
  non-canonical numbers, and Unicode ambiguity.

### WP6-6 — Evidence corpus and review

- Create documentary positive, boundary, negative, permutation, and
  determinism vectors only after their source rows are complete.
- Complete a normative-row-to-vector ledger with no uncovered row.
- Perform independent constitutional and numerical/serialization reviews,
  including independent recomputation of expected values and bytes.
- Correct only WP6-authorized artifacts; re-review every correction; obtain
  confirmation and freeze only with unresolved findings `NONE`.

---

## 12. Risk analysis

| Risk | Consequence | Mandatory control |
| --- | --- | --- |
| Planning is mistaken for substantive authorization | Frozen `STOP` and `G-3` prerequisite are bypassed. | Prominent candidate status, WP6-0 hard gate, and explicit no-authority clauses. |
| `G-3 OPEN — PARTIAL` is treated as enough for A–J | A partial contract is presented as usable while K is unformable. | Enforce the atomic A–K rule; do not author any normative component before valid entry. |
| `G-4 OPEN` is turned into a factor or contract | Unauthorized annualization semantics and false dependency closure. | Bind only named unavailability; reject values, aliases, placeholders, synthetic dependencies, and ambient constants. |
| Source ownership leaks into Portfolio Intelligence | Local rules silently recreate Market, Ledger, Asset, or Provenance semantics. | Require one source owner and exact evidence/dependency placement for every row. |
| Ambient behavior changes outputs | Results vary by clock, locale, provider, library, version, or input order. | Expand the no-default matrix into direct negative vectors and deterministic ordering rules. |
| Result semantics leak from WP7 into WP6 | The result contract is pre-decided without its separate review boundary. | Restrict WP6 outputs to semantic predicates and byte forms; prohibit result fields and classifications. |
| Vectors reverse-author missing rules | Fixtures become a hidden source of semantics. | Trace every vector from a confirmed row and mark artificial examples non-effective. |
| Canonical serialization drifts | Two equivalent analytical inputs receive different identities or bytes. | Require injectivity, round trip, ordering, rejection, and independent byte recomputation. |
| Review pressure merges WP6 and WP7 | Semantic and result authority lose separate auditability. | Retain separate artifacts, independent confirmation points, and strict downstream sequencing. |
| Repository synchronization occurs early | Decision Log, Index, Glossary, or Roadmap diverges from frozen governance sequencing. | Reserve those updates for separately authorized M44 epic closeout only. |

---

## 13. Acceptance criteria

### 13.1 Planning acceptance criteria

This planning artifact is ready for independent planning review only when it:

1. states that planning may proceed now while substantive normative authoring
   remains unavailable;
2. preserves `G-3 OPEN — PARTIAL`, `G-4 OPEN`, and checkpoint `STOP` exactly;
3. defines the lawful entry condition and the WP6-0 hard stop;
4. maps every Component A–K, owner boundary, dependency, prohibition, and
   vector class;
5. preserves A–K atomicity and prohibits partial A–J authoring;
6. identifies `G-4 OPEN` as bindable named unavailability without supplying
   an annualization value or dependency;
7. defines an auditable authoring, review, and freeze sequence; and
8. grants no constitutional redesign, implementation, runtime, or
   frozen-artifact-amendment authority.

### 13.2 Substantive-entry acceptance criteria

No future normative authoring may begin unless all §2.2 conditions are
independently verified. If any condition fails, the correct result is
`NOT AUTHORIZED`; no partial normative artifact is created and no stage after
WP6-0 begins.

### 13.3 Future normative-completion acceptance criteria

Once lawfully entered, a future M44-WP6 normative artifact is complete only
when all of the following are true:

1. every Component A–K has complete normative rows;
2. every frozen no-default concern has an exact permitted closure and direct
   rejection coverage;
3. every owner, evidence role, dependency identity, immutable version, and
   input/output boundary is exact;
4. Component G contains only the frozen named-unavailability binding while
   the Market Intelligence instrument remains absent;
5. Component K rests on proven formable upstream canonical bytes and preserves
   them unchanged;
6. every retained or rejected optional semantic has the required vector
   coverage, and the coverage ledger has no uncovered normative row;
7. two independent readers derive identical selections, predicates, values,
   and bytes from the same documentary inputs;
8. no result semantics, formula admission, source code, runtime behavior, or
   provider behavior has entered the artifact;
9. independent constitutional and numerical/serialization reviews are
   approved, every correction is re-reviewed, and unresolved findings are
   `NONE`; and
10. the artifact is independently confirmed and frozen before WP7 begins.

---

## 14. Repository impact

### 14.1 This planning artifact

This plan adds only:

`docs/implementation/M44_WP6_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md`

It does not modify any frozen artifact, source file, fixture, configuration,
or governance index.

### 14.2 Conditional future normative artifacts

Only after lawful substantive entry, the frozen M44 architecture prescribes:

| Path | Purpose |
| --- | --- |
| `docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md` | The M44-authorized normative semantics specification at the frozen M43-named binding path. |
| `docs/implementation/m44/fixtures/M44_WP6_POSITIVE_DOCUMENTARY_VECTORS.md` | Positive and boundary documentary vectors. |
| `docs/implementation/m44/fixtures/M44_WP6_NEGATIVE_DOCUMENTARY_VECTORS.md` | Rejection, fail-closed, and prohibition vectors. |

Any independent review, correction, confirmation, or freeze record must remain
additive and within separately authorized WP6 documentation scope. It must not
be used to amend a frozen source in place.

### 14.3 Reserved repository updates

This plan does not update, and future WP6 work must not update:

- `docs/engineering/DECISION_LOG.md`;
- `docs/implementation/INDEX.md`;
- `docs/GLOSSARY.md`; or
- `docs/architecture/ROADMAP.md`.

Those synchronization actions remain reserved for separately authorized M44
epic closeout, consistent with the
[M44-WP5 Freeze Record](M44_WP5_FREEZE_RECORD.md) and the frozen M44
architecture.

---

## 15. Authority limitations

This candidate does not:

- authorize M44-WP6 or M44-WP7 substantive execution;
- authorize a different checkpoint result, close `G-3`, close `G-4`, or
  otherwise alter an effective frozen state;
- supply any missing canonical reference, annualization dependency, contract
  kind, identifier, immutable version, or canonical value bytes;
- create a new constitutional noun, owner, shared ownership model, or domain
  allocation;
- amend M42, M43, M44-WP1, M44-WP4, M44-WP5, the Platform Architecture, or
  any other frozen source;
- authorize implementation, source code, persistence, migration, API,
  transport, UI, provider access, runtime behavior, executable validation, or
  production capability; or
- authorize Decision Log, Implementation INDEX, Glossary, or Roadmap
  synchronization.

Any conflict, missing authority, changed gate state, or new requirement must
be handled by separately authorized governance. This candidate records the
condition; it does not cure it.

---

## 16. Final planning determination

**M44-WP6 planning may proceed now.** This document provides the complete
planning baseline for a future deterministic, auditable, non-production
Portfolio Analytics Normative Semantics Specification.

**M44-WP6 normative authoring may not begin while `G-3` remains
`OPEN — PARTIAL`.** The current checkpoint result remains `STOP`.
`G-4 OPEN` remains effective, frozen, and bindable only as named
annualization unavailability; it is not authority to invent a value, factor,
alias, placeholder, or synthetic dependency.

Components A–K remain one atomic normative scope. M44-WP6 and M44-WP7 remain
unauthorized for substantive execution. Implementation and runtime authority
remain `NONE`.
