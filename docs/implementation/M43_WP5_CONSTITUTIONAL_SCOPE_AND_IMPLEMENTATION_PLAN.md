# M43-WP5 — Constitutional Scope and Implementation Plan

**Milestone:** M43 — Portfolio Analytics Contract Foundation  
**Work package:** M43-WP5 — Result, Sufficiency, Degraded State, Provenance, and Serialization  
**Artifact class:** Constitutional scope and documentary implementation plan  
**Status:** `DRAFT — RC1 REQUIRED CORRECTIONS APPLIED; REQUIRES INDEPENDENT CONFIRMATION`  
**M43 Architecture:** `COMPLETE AND FROZEN` — cited, never modified  
**M43-WP1:** `COMPLETE AND FROZEN` — cited, never modified  
**M43-WP2:** `COMPLETE AND FROZEN` — cited, never modified  
**M43-WP3:** `COMPLETE AND FROZEN` — cited, never modified  
**M43-WP4:** `COMPLETE AND FROZEN` — cited, never modified  
**Runtime authority:** `NONE`  
**Source-code authority:** `NONE`  
**Persistence/API/UI authority:** `NONE`  
**Implementation authority:** `NONE`  
**Provider authority:** `NONE`  
**Production-method authority:** `NONE`  
**Executable-validation authority:** `NONE`

---

## 0. Executive determination

M43-WP5 is the result-contract work package allocated by the frozen
[M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md). It consumes
the exact identities, closure rules, canonical representations, and
deterministic predicates frozen by M43-WP1 through M43-WP4. It does not
redesign, widen, repair, or reinterpret any of them.

WP5 shall produce the documentary contract for one immutable and auditable
Portfolio Measure Result shared by every later Portfolio method family. The
contract must close:

1. result identity;
2. value presence and absence;
3. Portfolio Input Sufficiency;
4. Portfolio Computation Outcome;
5. Portfolio Deterministic Calculation;
6. the exact reuse of Degraded State under the M34-D-0005 producing-domain
   grammar;
7. deterministic reason-code representation;
8. exact method and manifest lineage;
9. carriage, without recapture or reinterpretation, of already-captured
   Provenance;
10. compatibility with the complete Canonical Temporal Claim;
11. canonical result serialization; and
12. canonical-byte and hash stability.

The result contract is an immutable semantic envelope, not a runtime response,
database entity, transport payload, cache value, UI model, or production
calculation. It must represent success and non-success without creating a
formula, performing a calculation, fetching evidence, evaluating correctness,
or granting production authority.

No new constitutional noun is required by this plan. WP5 consumes the admitted
WP1 nouns `Portfolio Measure Result`, `Portfolio Input Sufficiency`,
`Portfolio Computation Outcome`, and `Portfolio Deterministic Calculation`,
and reuses the existing `Canonical Temporal Claim`, `Event Type`, `Producing
Domain`, `Degraded State`, and `Provenance` terms at their frozen meanings.
Reason codes, field names, identity inputs, serialization components, and
matrix rows are ordinary contract structure, not new semantic owners. If
normative drafting discovers a genuinely new noun, drafting must stop at that
boundary until the frozen downstream vocabulary rule has been completed and
independently confirmed.

---

## 1. Repository status and controlling authority

### 1.1 Repository status

This work begins from the following constitutional state:

| Artifact | Status for WP5 | Permitted WP5 use |
| --- | --- | --- |
| M43 Architecture | Complete and frozen | Citation and exact consumption only |
| M43-WP1 vocabulary, ownership, and current-state reconciliation | Complete and frozen | Citation and exact consumption only |
| M43-WP2 Definition, Method Version, applicability, and dependency contracts | Complete and frozen | Citation and exact consumption only |
| M43-WP3 Subject and Input Manifest contracts | Complete and frozen | Citation and exact consumption only |
| M43-WP4 semantic scope and deterministic predicate handoff | Complete and frozen | Citation and exact consumption only |
| Existing M1-M42 governance corpus | Canonical according to its recorded status | Citation and exact consumption only |
| Existing runtime behavior | Current-state evidence only | No constitutional precedent |

The repository may contain staged, uncommitted, or differently status-labelled
copies of frozen M43 artifacts. For this work package, the controlling status
is the confirmed status above. WP5 must not edit those artifacts to reconcile
repository metadata, wording, status labels, or effectivity evidence.

### 1.2 Authority order

WP5 is governed, in descending precedence, by:

1. the Platform Constitution and Architecture Laws;
2. frozen M34 ownership decisions, especially M34-D-0005;
3. frozen M39 Observation and generic Provenance authorities;
4. frozen M40-WP1 section 8.3 and the M40-M41 Market Measure corpus as
   external authority and mechanical precedent only;
5. frozen M42 Portfolio contracts;
6. frozen M43 Architecture;
7. frozen M43-WP1 vocabulary and ownership dispositions;
8. frozen M43-WP2 contracts;
9. frozen M43-WP3 contracts;
10. frozen M43-WP4 deterministic semantic predicates; and
11. this WP5 planning artifact, followed by the independently confirmed WP5
    normative specification.

On conflict, the earlier or source-owning authority controls. WP5 must fail
closed rather than amend an upstream contract, invent missing authority, or
launder another owner's meaning into Portfolio Intelligence.

---

## 2. External governance dependencies

WP5 depends on, but does not own:

| Dependency | Governing authority | Exact WP5 dependency | WP5 prohibition |
| --- | --- | --- | --- |
| Canonical Temporal Claim | M34-D-0005 | Complete tuple of Event Type, Producing Domain, authoritative timestamp, and Degraded State | No parallel temporal claim or omitted coordinate |
| Degraded State | Producing domain under M34-D-0005 | Exact six-value grammar and producing-domain ownership | No `Portfolio Degraded State`, seventh state, or outcome substitution |
| `UNAVAILABLE` reservation | M40-WP1 section 8.3 and frozen WP1 | `UNAVAILABLE` remains a Degraded State and never a Portfolio Computation Outcome | No relabelling as an outcome or reason |
| Provenance meaning and capture | Connectivity & Ingestion under Platform Architecture section 6.4 and M42-WP6; M42/WP3 governs the exact association carried | Carriage of exact already-captured Provenance with its association intact | No capture, recapture, reconstruction, correction, or ownership transfer |
| Portfolio coordinates and Composition | Frozen M42 contracts | Exact subject-side identity and source-owned citations consumed through WP3 | No inference, mutation, or shadow identity |
| Definition, Method Version, applicability, and dependency closure | Frozen WP2 | Exact immutable identities and declarations | No substitution, registry behavior, or altered compatibility |
| Subject and Input Manifest | Frozen WP3 | Exact identities, canonical bytes, entry closure, and provenance associations | No sidecar input, manifest repair, or new category |
| Numerical-semantic facts and predicates | Frozen WP4 | Exact deterministic handoff only | No reinterpretation of a predicate as a pre-decided WP5 classification |
| Concrete value meaning | Future WP6-WP8 method specifications under their own authority | Opaque, exact canonical value carriage only after the governing method permits it | No formula, unit invention, or method admission |

The M41 result-pattern corpus may be cited to test completeness and mechanical
separation. Its Market Intelligence-owned Result, Input Sufficiency,
Computation Outcome, Deterministic Calculation, Method Version, Manifest,
reason values, and field choices do not become Portfolio Intelligence
contracts. WP5 must derive its authority from frozen M43, not from analogy.

### 2.1 Standing governance blocks and representability gaps

The following constraints remain active and independently governed:

1. the `M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6` item
   required by frozen WP1 section 7.4;
2. the M42-WP7 section 5 Composition canonical-byte representability gap
   inherited through frozen WP3 Subject section 7.1 and Manifest section 10.3;
   and
3. the annualization-dependency representability gap recorded by frozen WP4
   section 6.7.

WP5 confirmation releases none of these constraints and closes none of these
gaps. WP5 may record their consequences, fail closed, and use expressly
artificial documentary material, but it may not supply missing Composition
bytes, admit an annualization dependency, clear WP6, or imply that another
work package has done so.

---

## 3. Constitutional scope

### 3.1 In scope

Only the following concerns are allocated to WP5:

1. the complete implementation-neutral Portfolio Measure Result contract;
2. the exact identity basis of a Portfolio Measure Result;
3. immutability, equivalence, and non-substitutability of a result;
4. exact value-presence and value-absence rules for every admitted
   sufficiency/outcome/state combination;
5. the closed value set and exact meaning of Portfolio Input Sufficiency;
6. the closed value set and exact meaning of Portfolio Computation Outcome;
7. the deterministic relation among applicability facts, manifest
   conformance, WP4 semantic predicates, Portfolio Input Sufficiency,
   Portfolio Computation Outcome, Degraded State, reason codes, and value
   presence;
8. the result-level obligations required by Portfolio Deterministic
   Calculation;
9. exact reuse of the M34-D-0005 Degraded State grammar for a result whose
   Producing Domain is Portfolio Intelligence;
10. a deterministic, closed, non-judgmental reason-code grammar;
11. the exact distinction between a reason code, a sufficiency value, an
    outcome value, and a Degraded State;
12. exact lineage to one Portfolio Measure Definition, one Portfolio Method
    Version, one Portfolio Measure Subject, one Portfolio Analytics Input
    Manifest, and every directly consumed governed calculation dependency
    already admitted through WP2/WP3;
13. exact carriage of already-captured Provenance associated with inputs,
    without recapture or reinterpretation;
14. the complete Canonical Temporal Claim compatibility mapping, including
    Event Type, Producing Domain, authoritative timestamp meaning, and
    Degraded State;
15. result-level canonical field ordering, encoding, serialization,
    reconstruction, and rejection rules;
16. deterministic result identity, canonical-byte stability, and hash
    stability;
17. explicit inclusion and exclusion of every output-affecting result
    coordinate from identity and canonical bytes;
18. documentary positive, negative, boundary, permutation, round-trip, and
    hash-stability vectors;
19. prohibited interpretations and fail-closed rules; and
20. an exact documentary handoff to WP6-WP9 without admitting a method,
    formula, runtime component, or implementation.

Result identity follows the frozen WP3 identity precedent: the normative
specification must fix the result's canonical bytes as its identity. A
different identity basis is inadmissible unless separately justified by
controlling frozen authority; this plan identifies no such authority. Any
hash is only a derived, documentary, non-substituting stability artifact. It
creates no second identity axis and no implementation, registry, or locator
authority.

### 3.2 Out of scope

WP5 must not define, amend, select, or authorize:

- any new vocabulary, owner, authority class, dependency kind,
  representability rule, or no-default philosophy;
- any change to Portfolio Identity, Accounting Scope, Membership, Portfolio
  Base Currency, Investment Universe, Portfolio Benchmark Declaration,
  Lifecycle State, Portfolio Composition, or their ownership;
- any Portfolio Measure Definition, Portfolio Method Version,
  applicability operator, dependency declaration, Subject coordinate,
  Manifest field/category/entry, canonical upstream identity, or upstream
  serialization rule;
- any nested canonical encoding absent from its source authority, including
  the missing M42-WP7 Composition canonical-byte representation;
- any WP4 temporal, currency, FX, calendar, benchmark, risk-free,
  annualization, missing-data, partial-window, numeric, rounding, or
  dependency-arithmetic semantic;
- any performance, rolling, risk, benchmark-relative, contribution, or
  attribution formula;
- any scalar, series, coordinate-set, unit, precision, threshold, or
  method-family-specific value meaning not already fixed by its governing
  Definition and Method Version;
- any accounting arithmetic, NAV, ledger replay, cost basis, cash-flow
  treatment, or resolution of open accounting questions;
- evidence acquisition, provider selection, source preference, correction,
  enrichment, retrieval, live lookup, fallback, or post-manifest discovery;
- Provenance capture, creation, repair, enrichment, or reinterpretation;
- a new temporal event type, producing domain, Degraded State, or
  Portfolio-prefixed degraded-state noun;
- correctness, trust, reliability, quality, suitability, recommendation,
  causal explanation, ranking, forecast, authorization, optimization, or
  execution meaning;
- cross-portfolio, person, household, Wealth, Decision, Evaluation, or
  Experience semantics;
- a runtime exception taxonomy, transport status, HTTP status, log event,
  observability signal, persistence lifecycle, mutable status, or retry
  policy;
- an executable algorithm, numerical method, hash implementation, serializer
  implementation, registry, kernel, adapter, API, UI, schema, migration,
  database record, cache, scheduler, provider integration, or deployment;
- executable fixtures, test code, test runners, conformance harnesses, or
  production validation behavior;
- production-method admission, capability completion, endpoint cutover,
  consumer migration, or legacy removal; or
- modification of any frozen M1-M43-WP4 artifact.

WP5 also creates no digest requirement for a Portfolio Measure Definition,
Portfolio Method Version, Portfolio Measure Subject, Portfolio Analytics
Input Manifest, or any of their source-governed constituents.

### 3.3 Essential boundary

WP5 classifies and encloses exact frozen semantic facts. It does not create
the facts and does not calculate the value.

```text
WP2 immutable definition / method / applicability / dependency identities
                                   +
WP3 exact subject / closed manifest / imported Provenance associations
                                   +
WP4 deterministic semantic facts and predicates
                                   |
                                   v
WP5 immutable result classification, lineage, temporal/provenance carriage,
identity, canonical serialization, and documentary stability obligations
                                   |
                                   v
WP6-WP8 method-specific value semantics; WP9 later implementation design
```

No arrow transfers ownership. A cited or carried object retains its original
owner and canonical meaning.

---

## 4. Vocabulary and no-expansion gate

WP1 already admitted every constitutional noun required by the frozen WP5
allocation:

| Required concept | Frozen disposition | Owner | WP5 action |
| --- | --- | --- | --- |
| Portfolio Measure Result | `ADMIT` | Portfolio Intelligence | Specify the reserved contract |
| Portfolio Input Sufficiency | `ADMIT` | Portfolio Intelligence | Specify the reserved classification |
| Portfolio Computation Outcome | `ADMIT` | Portfolio Intelligence | Specify the reserved completion axis |
| Portfolio Deterministic Calculation | `ADMIT` | Portfolio Intelligence | Specify result-level reproducibility obligations |
| Portfolio Measure | `ADMIT` | Portfolio Intelligence | Consume the frozen WP1 meaning; no WP5 action |
| Portfolio Measure Definition | `ADMIT` | Portfolio Intelligence | Consume and bind the exact WP2 identity; no WP5 action |
| Portfolio Method Version | `ADMIT` | Portfolio Intelligence | Consume and bind the exact WP2 identity; no WP5 action |
| Portfolio Measure Subject | `ADMIT` | Portfolio Intelligence | Consume and bind the exact WP3 identity/representation; no WP5 action |
| Portfolio Analytics Input Manifest | `ADMIT` | Portfolio Intelligence | Consume and bind the exact WP3 identity/representation; no WP5 action |
| Portfolio Measurement Window | `ADMIT` | Portfolio Intelligence | Consume the frozen WP1/WP2 meaning; no WP5 action |
| Portfolio Degraded State | `REUSE` | Producing domain for the exact Canonical Temporal Claim | Use `Degraded State`; never create the prefixed noun |
| Canonical Temporal Claim | `REUSE` | Producing domain under M34-D-0005 | Carry the complete frozen tuple |
| Provenance | `REUSE` | Connectivity & Ingestion under Platform Architecture section 6.4 and M42-WP6 | Carry exact existing records and M42/WP3-governed associations |

The WP5 normative specification must begin with a vocabulary-sufficiency
check. That check may confirm that ordinary structural language is sufficient;
it may not silently promote `reason`, `reason code`, `result identity`,
`canonical bytes`, `hash`, `lineage`, `value presence`, `absence`, `round
trip`, `schema version`, or a matrix label into a new constitutional noun.

If a genuinely new governed concept is unavoidable, it must receive exactly
one `ADMIT`, `REUSE`, `RENAME`, or `REJECT` disposition under the frozen
downstream vocabulary rule before reliance. This contingency does not
authorize WP5 to reopen WP1 or modify another frozen artifact.

---

## 5. Ownership matrix

Every WP5 concern has one semantic owner. Structurally adjoining fields are
separated below where their meanings have different owners.

| Concern | Sole semantic owner | Governing authority | WP5 authority | Non-owner boundary |
| --- | --- | --- | --- | --- |
| Portfolio Measure Result envelope, identity, immutability, and canonical representation | Portfolio Intelligence | Frozen M43 Architecture and WP1; WP5 | Define the result contract | Runtime, storage, transport, and UI gain no ownership |
| Portfolio Input Sufficiency | Portfolio Intelligence | Frozen WP1; WP5 | Define exact values, meanings, reasons, and mapping | Market Input Sufficiency and M39 Semantic Sufficiency are not reused |
| Portfolio Computation Outcome | Portfolio Intelligence | Frozen WP1; WP5 | Define exact values, meanings, reasons, and mapping | Market Computation Outcome is precedent only; Degraded State remains orthogonal |
| Portfolio Deterministic Calculation | Portfolio Intelligence | Frozen WP1; WP5 | Define result-level reproducibility obligations | No algorithm, correctness claim, runtime, or production admission |
| Result value-presence/absence relation | Portfolio Intelligence for result composition | Frozen M43 Architecture; WP5 | Define when a governed method value may or must be carried | WP6-WP8 retain concrete value meaning and formula authority |
| Concrete Portfolio measure value meaning | Portfolio Intelligence under the applicable Definition and later method specification | Frozen WP2 and later WP6-WP8 | Cite and carry exactly | WP5 may not define formula, unit, shape, or threshold |
| Portfolio Definition and Method Version identities | Portfolio Intelligence under WP2 | Frozen WP2 | Bind exact identities into lineage | WP5 may not revise or substitute them |
| Portfolio Measure Subject identity | Portfolio Intelligence under WP3 | Frozen WP3 | Bind exact identity into result and lineage | WP5 may not add a subject coordinate |
| Portfolio Analytics Input Manifest identity and bytes | Portfolio Intelligence under WP3 | Frozen WP3 | Bind exact identity/bytes into result and lineage | WP5 may not repair, extend, or reorder the manifest |
| WP4 semantic facts and predicates | Portfolio Intelligence under WP4 | Frozen WP4 | Consume and map deterministically | WP5 may not redefine their calculation-side meaning |
| Canonical Temporal Claim grammar | Producing domain for the exact claim | M34-D-0005 | Reuse complete grammar | No parallel temporal grammar |
| Result calculation event, timestamp meaning, and Degraded State | Portfolio Intelligence as Producing Domain | M34-D-0005 and frozen WP1 | Define the exact Portfolio calculation claim within the frozen grammar | Experience only renders; no state expansion |
| Provenance meaning and capture | Connectivity & Ingestion | Platform Architecture section 6.4 and M42-WP6; M42/WP3 for the exact association carried | Preserve exact supplied record and association | WP5 neither captures nor reconstructs Provenance |
| Provenance carriage relation within a Portfolio Measure Result | Portfolio Intelligence | Frozen M43 Architecture; WP5 | Define exact inclusion, ordering, and non-laundering obligations | Carriage does not transfer ownership of Provenance |
| Ledger-derived evidence meaning | Ledger & Accounting | Frozen M42 and WP3 | Cite through exact Manifest lineage | No accounting recomputation or semantic ownership |
| Market evidence meaning | Market Intelligence | Frozen M39-M41 and WP3 | Cite through exact Manifest lineage | No provider, observation, or Market Measure redefinition |
| Asset identity, classification, currency, unit, and taxonomy references | Asset Foundation | Frozen Asset Foundation authorities and WP3 | Cite through exact Manifest lineage | No local alias or taxonomy |
| Reason-code grammar and Portfolio classification reasons | Portfolio Intelligence | Frozen M43 Architecture; WP5 | Define deterministic, non-judgmental reason representation | Reasons do not become evidence, states, outcomes, or evaluations |
| Correctness and quality assessment | Trust & Evaluation | M34-D-0010 and frozen glossary | None | A result or `SUCCEEDED` never asserts correctness |
| Recommendation and action meaning | Decision Intelligence | Frozen ownership corpus | None | No result classification implies action |
| Rendering and presentation labels | Experience Platform | M34-D-0005 and Platform laws | None | Experience computes and reclassifies nothing |
| Cross-portfolio derived meaning | Wealth Intelligence | Frozen ownership corpus | None | WP5 remains one-Portfolio only |

Embedding, citation, hashing, serialization, persistence custody, transmission,
display, or computation does not transfer semantic ownership.

---

## 6. Placement matrix

Every WP5 concern has one normative home. Imported identities and bytes remain
defined only in their source contracts.

| Concern | Unique normative placement | Imported authority | Prohibited duplicate placement |
| --- | --- | --- | --- |
| WP5 scope and authoring sequence | This constitutional scope and implementation plan | Frozen M43 Architecture | Architecture, WP1-WP4, runtime design |
| Vocabulary sufficiency determination | Opening gate of the WP5 normative specification, or a separate Stage A artifact if a new noun is discovered | Frozen WP1 downstream vocabulary rule | Implicit admission in fields or fixtures |
| Portfolio Measure Result contract | WP5 primary normative specification | WP1 meaning | WP2/WP3/WP4, method-family specs, API/schema |
| Result identity and immutability | WP5 primary normative specification | Exact WP2/WP3/WP4 identities and bytes | Registry, database key, cache key, transport identifier |
| Sufficiency values and mappings | WP5 primary normative specification | WP1 meaning; WP2/WP3/WP4 facts | Manifest completeness contract, method formula, runtime validation |
| Outcome values and mappings | WP5 primary normative specification | WP1 meaning; frozen `UNAVAILABLE` reservation | Degraded State, exception status, HTTP response |
| Degraded State compatibility matrix | WP5 primary normative specification by exact reuse | M34-D-0005 | New state enum or Portfolio-prefixed state |
| Reason-code grammar | WP5 primary normative specification | WP5 allocated authority | Log taxonomy, exception hierarchy, provider status |
| Method/manifest/dependency lineage carriage | WP5 primary normative specification | Exact WP2/WP3 contracts | Reconstructed sidecar, persistence join, live lookup |
| Provenance carriage | WP5 primary normative specification | Exact WP3 associations and source-owned Provenance | Recapture service, inferred provenance, detached sidecar |
| Canonical Temporal Claim compatibility | WP5 primary normative specification | M34-D-0005 | Parallel calculation timestamp record |
| Canonical result serialization and identity framing | WP5 primary normative specification | Imported canonical bytes remain source-defined | Serializer code, wire API, database schema |
| WP2 section 5.2 Definition-record byte-equivalence expectation | Remains open under separately authorized source governance; WP2's interim documentary field-comparison rule remains in force | Frozen WP2 section 5.2 | Definition-record serializer or upstream canonical-byte rule in WP5 |
| Positive and boundary documentary vectors | `docs/implementation/m43/fixtures/M43_WP5_POSITIVE_DOCUMENTARY_VECTORS.md` | Frozen upstream documentary vectors by citation | Executable test or production catalog |
| Negative documentary vectors | `docs/implementation/m43/fixtures/M43_WP5_NEGATIVE_DOCUMENTARY_VECTORS.md` | Frozen negative corpora by citation | Runtime error catalog |
| Coordinated independent constitutional and serialization/reconstruction review | `docs/implementation/M43_WP5_INDEPENDENT_CONSTITUTIONAL_REVIEW.md`, with separately identified review dimensions, evidence, and conclusions | All controlling authorities | Self-approval in the normative specification or an unseparated combined conclusion |
| Required-corrections response, if needed | `docs/implementation/M43_WP5_REQUIRED_CORRECTIONS_RESPONSE.md` | Review findings | Editing frozen predecessors |
| Independent confirmation | `docs/implementation/M43_WP5_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md` | Corrected WP5 corpus and independent review | Status assertion without review evidence |

The primary specification may cite upstream canonical bytes or embed them
using an explicitly framed composition rule. It must never restate an upstream
serializer as though WP5 owned it.

---

## 7. Boundary definition

### 7.1 Upstream consumption and representability boundary

WP5 receives only:

- one exact Portfolio Measure Definition identity from WP2;
- one exact Portfolio Method Version identity and immutable specification
  reference from WP2;
- the exact applicability determination inputs and result from WP2, without
  relabelling applicability as sufficiency, outcome, or Degraded State;
- the exact closed calculation-dependency declaration and exact direct
  dependency-result/value references admitted through WP2/WP3;
- one exact Portfolio Measure Subject identity and canonical representation
  from WP3;
- one exact conforming Portfolio Analytics Input Manifest identity, canonical
  representation, and closed entry set from WP3;
- every exact already-captured Provenance association carried by that
  Manifest;
- deterministic facts and predicates from WP4, including the status of
  window validity, alignment, currency/FX closure, calendar resolution,
  benchmark alignment, risk-free evidence, annualization representability,
  density/gaps/partial window, and arithmetic; and
- an exact governed method value only when the later method specification and
  the WP5 value-presence rules permit it.

An absent, invalid, non-conforming, unresolved, or unrepresentable upstream
object is not repaired by WP5. The normative specification must state the
deterministic classification consequence where frozen authority permits one,
and otherwise fail closed.

WP5 expressly inherits two upstream representability constraints:

- M42-WP7 section 5 defines no exact Composition canonical-byte
  representation. Frozen WP3 Subject section 7.1 and Manifest section 10.3
  therefore require fail-closed behavior and state that no concrete Portfolio
  Measure Subject or Portfolio Analytics Input Manifest canonical byte
  sequence can presently be emitted.
- Frozen WP4 section 6.7 leaves the annualization dependency
  representability gap open and independently governed.

WP5 cannot cure either gap. While the Composition canonical-byte gap remains
open, no concrete Portfolio Measure Result canonical byte sequence, result
identity, or hash value may be emitted or treated as normative. WP5 must not
define, name, imply, complete, or reverse-engineer a missing nested canonical
encoding. All byte-, identity-, round-trip-, permutation-, or hash-oriented
WP5 vectors must instead be visibly labelled `ARTIFICIAL`, `NON-EFFECTIVE`,
and `NOT CONFORMANCE EVIDENCE`; they cannot prove that a Subject, Manifest,
Result, method, dependency, or production representation exists.

Frozen WP2 section 5.2 anticipates Definition-record byte equivalence "once
WP5 canonical serialization exists." WP5 disposes of that expectation without
amending WP2: WP5 supplies only unambiguous result-level framing of identities
and already-source-canonical bytes. It does not define Definition-record
canonical bytes or any other upstream serializer. The WP2 record-level
equivalence concern remains open under separately authorized source
governance, and WP2's interim documentary field-comparison rule remains in
force.

### 7.2 Classification boundary

The normative specification must define a total, non-overlapping documentary
mapping for every admitted combination of:

- applicability status;
- Manifest conformance and closure;
- declared prerequisite satisfaction;
- dependency resolution;
- WP4 deterministic semantic predicates;
- calculation completion;
- value presence or absence;
- Canonical Temporal Claim;
- Degraded State; and
- one or more deterministic reasons where required.

The mapping must preserve these constitutional separations:

| Axis | Question answered | Must not mean |
| --- | --- | --- |
| Applicability | Does the Definition apply to the exact subject/invocation under WP2? | Sufficiency, completion, state, or correctness |
| Portfolio Input Sufficiency | Do exact supplied canonical inputs satisfy every declared prerequisite? | Truth, quality, freshness, completion, or trust |
| Portfolio Computation Outcome | Did the specified calculation complete with its required Portfolio measure output? | Degraded State, correctness, production availability, or runtime transport |
| Degraded State | How does Portfolio Intelligence qualify temporal availability for this result claim? | Calculation completion, exception class, or evaluation verdict |
| Reason code | Why does an exact classification or state apply? | A new classification axis, evidence, judgment, or action |
| Evaluation | Is the result correct or reliable under a separately governed assessment? | Any WP5 classification |

No value in one row may be inferred solely from a value in another row unless
the WP5 normative specification explicitly records the governing deterministic
relation and that relation is permitted by the frozen authorities.

The normative specification must also close, independently and explicitly:

1. the exact deterministic relation, or the exact affirmative non-relation,
   between every Degraded State carried by an upstream input and the consuming
   result's own Degraded State; and
2. the exact deterministic relation, or the exact affirmative non-relation,
   between a consumed dependency result's Portfolio Input Sufficiency,
   Portfolio Computation Outcome, and Degraded State and the consuming
   result's own classifications.

Either closure must preserve the upstream producing domain's M34-D-0005
ownership and the consuming result's Portfolio Intelligence producing-domain
ownership. It may not silently propagate, silently discard, relabel,
aggregate, or restate another producer's claim; create a seventh Degraded
State, new classification axis, new owner, or aggregation grammar; or infer
correctness, quality, or trust.

### 7.3 Value boundary

WP5 owns only the result-level presence and absence contract. It must require:

- no required calculated value when the admitted mapping prohibits a value;
- every required value when the admitted mapping requires one;
- no placeholder, sentinel, zero, empty value, prior value, partial value, or
  null-shaped substitute for absence;
- no value silently retained from a failed, insufficient, unresolved, or
  otherwise non-permitted calculation; and
- exact carriage, without reinterpretation, of a value whose concrete shape
  and meaning are fixed by the governing Definition and Method Version.

Whether a method may produce a partial value is not decided by this plan. The
normative specification must define the generic result-envelope requirements
for a partial value only to the extent authorized by frozen WP4 section 6.8:
full requested window, exact shorter available window, and prohibited fallback
window remain distinct. The exact method-specific permission remains with
WP6-WP8. No partial result may silently change the requested measure or
window.

### 7.4 Temporal and Degraded State boundary

Every Portfolio Measure Result must be compatible with one complete Canonical
Temporal Claim:

- Event Type must be an existing M34-D-0005 value appropriate to the result
  event;
- Producing Domain must identify the actual constitutional producer;
- authoritative timestamp must have one explicit Portfolio
  Intelligence-owned meaning for that event; and
- Degraded State must be exactly one existing M34-D-0005 value.

The frozen grammar enumerates no "non-degraded" value. Because a complete
Canonical Temporal Claim includes Degraded State, every result must carry
exactly one of the six approved M34-D-0005 values: `UNKNOWN`, `UNAVAILABLE`,
`DELAYED`, `STALE`, `PARTIAL`, or `CONFLICTING`. Carrying no state is an
incomplete claim; inventing a non-degraded marker is a prohibited seventh
state. Every result carrying any approved Degraded State is therefore subject
to the mandatory reason rule in section 8.

The normative specification must define timestamp source, meaning, canonical
representation, and identity treatment without consulting wall-clock time.
It must neither create a new event type nor treat request time, serialization
time, persistence time, cache time, response time, or UI refresh time as
authoritative by default.

`UNAVAILABLE` is exclusively a Degraded State. It is never a Portfolio
Computation Outcome, Portfolio Input Sufficiency value, reason code,
placeholder value, exception, or transport status.

An upstream input's Degraded State and a dependency result's classifications
remain claims of their respective producing domains. The consuming result's
own Degraded State, Portfolio Input Sufficiency, and Portfolio Computation
Outcome remain Portfolio Intelligence claims for that consuming result. The
normative specification must close their deterministic relation or affirmative
non-relation under section 7.2; carriage alone does not propagate a state, and
non-propagation alone does not authorize silent discard.

### 7.5 Provenance and lineage boundary

Lineage and Provenance are distinct:

- lineage binds the result to exact governed semantic identities and
  dependency/result references;
- Provenance retains exact already-captured source association and meaning.

WP5 may define how each is carried, ordered, serialized, and covered by result
identity. WP5 may not recreate missing Provenance from a manifest reference,
provider label, database row, timestamp, request, cache, or runtime context.
Carriage must be lossless, association-preserving, and non-laundering.

### 7.6 Downstream handoff

WP5 hands later work packages:

- a closed result envelope;
- exact classifications and their non-overlap rules;
- deterministic reason representation;
- exact value-presence/absence obligations;
- complete lineage and Provenance-carriage obligations;
- exact temporal/degraded-state compatibility;
- canonical result identity and serialization requirements; and
- documentary conformance vectors.

WP6-WP8 may fill only the method-specific semantic slots already reserved by
WP2-WP5. They may not redefine the result envelope or classification axes.
WP9 may design a later implementation and cutover but may not change WP5
semantics. No WP5 artifact authorizes either activity to occur early.

---

## 8. Explicit no-default matrix

WP5 introduces output-affecting result-contract choices, so inherited
no-default philosophy is necessary but not sufficient. The normative
specification must explicitly close every row below. This plan requires each
choice to be made and reviewed. Where frozen architecture or a frozen
predecessor already fixes a closure, this plan carries that closure forward
rather than reopening it.

| Output-affecting concern | Required explicit closure | Forbidden default or inference |
| --- | --- | --- |
| Result schema/version | Exact immutable version and compatibility meaning | Latest schema, tolerant reinterpretation, or runtime-selected version |
| Result field set | Exact closed required/conditional/forbidden fields | Extra fields, omitted required fields, or open extension bags |
| Field order | One canonical order | Object insertion order, language/runtime order, or alphabetical assumption |
| Imported identity framing | Exact unambiguous framing of WP2/WP3 identities/bytes | Concatenation without boundaries or reserialization under WP5 rules |
| Identity basis | Result canonical bytes are the result identity, following frozen WP3 precedent; explicitly include/exclude every semantic coordinate | A second identifier axis, digest substitution, database key, creation time, cache key, request id, or implementation detail |
| Identity equivalence | Byte-identical result canonical bytes; semantic reconstruction must preserve that identity | Locale, case-folding, coercion, alias, compatible-version substitution, or hash equality as identity |
| Hash relationship | Any hash is a derived, documentary, non-substituting stability artifact; its documentary mechanism and representation must be exact and create no implementation, registry, or locator authority | Hash as identity, upstream digest requirement, platform/library default, salted/runtime hash, or mutable algorithm |
| Upstream representability | Inherit WP3 sections 7.1/10.3 and WP4 section 6.7 fail-closed gaps; no normative result bytes, identity, or hash while required nested canonical bytes are unavailable | WP5-created nested encoding, implied upstream bytes, or artificial bytes treated as effective/conforming |
| Text encoding | Exact encoding and rejection rules | Host encoding, locale, BOM guess, lossy replacement |
| Unicode handling | Exact permitted form and normalization/rejection rule | Runtime normalization or visually equivalent substitution |
| Number carriage | Exact source-governed canonical number bytes | Binary float formatting, scientific-notation preference, or locale formatting |
| Timestamp carriage | Exact representation, precision, zone/offset rule, and semantic source | Current time, local timezone, serializer time, or precision truncation |
| Absence | Exact structural representation and permitted coordinates | `null`, empty, zero, NaN, sentinel, prior value, or omission treated interchangeably |
| Value presence | Exact mapping from admitted classifications | Best effort, stale reuse, partial fallback, or caller preference |
| Portfolio Input Sufficiency | Closed exact values and total prerequisite mapping | Market-owned values copied by assumption or truth/quality inference |
| Portfolio Computation Outcome | Closed exact values and total completion mapping | Market-owned values copied by assumption, `UNAVAILABLE`, or exception status |
| Degraded State | Exact existing six-value grammar and total permitted interaction matrix | Seventh value, prefixed state, outcome conversion, or UI status |
| Upstream input-state relation | Exact deterministic relation or exact affirmative non-relation between carried upstream Degraded States and the result's own Degraded State | Silent propagation, silent discard, ownership laundering, aggregation, or restatement |
| Dependency-result classification relation | Exact deterministic relation or exact affirmative non-relation between consumed dependency-result sufficiency/outcome/state and the consuming result's own classifications | Silent propagation/discard, inherited success, new axis/state/owner, or aggregation grammar |
| Reason requirement | At least one deterministic reason for every result carrying any of the six approved M34-D-0005 Degraded States and for every non-success Portfolio Computation Outcome or non-satisfied Portfolio Input Sufficiency; close all other cardinalities exactly | `optional` or `forbidden` for those classifications, a missing required reason, an implied non-degraded value, or an invented generic reason |
| Reason vocabulary | Closed codes, exact meanings, and governing condition | Free text as canonical identity, provider errors, log strings, or catch-all fallback |
| Multiple-reason ordering | Exact order, duplicate rule, and conflict rule | Encounter order, set/hash order, severity guess, or arbitrary first reason |
| Manifest lineage | Exact identity/bytes reference and inclusion rule | Rebuilt manifest, partial lineage, live lookup, or sidecar completion |
| Method lineage | Exact Definition/Method Version/dependency binding | Latest-compatible method, range, alias, or registry default |
| Provenance carriage | Exact association, cardinality, order, and imported representation | Recapture, inferred source, detached provenance, or omission for convenience |
| Canonical Temporal Claim | Complete tuple and exact mapping | Implicit Event Type/domain, wall clock, missing state, or UI timestamp |
| Partial result | Exact generic envelope rule plus explicit method permission | Silent shortening, implicit partial value, or changed requested window |
| Unknown fields/values | Exact fail-closed rejection behavior | Forward-compatible ignore, fallback enum, or permissive parsing |
| Round trip | Exact reconstruction and equality obligation | Semantically approximate parsing or non-canonical re-emission |
| Canonical rejection | Exact rejection of alternative encodings for one semantic result | Accept-many/emit-one ambiguity without constitutional authorization |

Any row left to a language, serializer, hash library, database, provider,
clock, locale, operating system, caller, cache, registry, or UI fails WP5.
The frozen M43 completion rule is mandatory: every unavailable or degraded
result explains why through at least one deterministic reason.

---

## 9. Documentary vectors

### 9.1 Vector purpose and status

WP5 vectors are normative documentary examples for independent reading,
manual reconstruction, and future separately authorized conformance design.
They are not:

- executable fixtures;
- test code or a test runner;
- a serializer or hash implementation;
- a production registry entry;
- a concrete method admission;
- proof of runtime behavior; or
- authority to modify an upstream fixture.

Every vector must cite the exact frozen rule it demonstrates. Imported WP2,
WP3, and WP4 objects must be cited or reproduced only under the framing rules
permitted by their source contracts.

Because the M42-WP7 Composition canonical-byte gap prevents concrete Subject,
Manifest, and Result bytes, every WP5 vector concerning canonical bytes,
identity, round trip, permutation, or hash must be conspicuously labelled
`ARTIFICIAL`, `NON-EFFECTIVE`, and `NOT CONFORMANCE EVIDENCE`. Such a vector
tests only the documentary rule under an explicit hypothetical. It cannot
establish conformance, effectivity, production existence, or closure of an
upstream representability gap.

### 9.2 Required positive and boundary vectors

The positive corpus must include, at minimum:

1. one complete permitted value-bearing result;
2. each admitted Portfolio Input Sufficiency value;
3. each admitted Portfolio Computation Outcome value;
4. every permitted outcome/value-presence combination;
5. every existing Degraded State in at least one constitutionally valid
   result combination;
6. explicit demonstration that `UNAVAILABLE` remains a state and not an
   outcome;
7. a total outcome/sufficiency/degradation/value-presence matrix;
8. one reason and multiple deterministically ordered reasons;
   this coverage must include at least one required reason for every
   approved M34-D-0005 Degraded State, non-success outcome, and non-satisfied
   sufficiency classification;
9. exact binding to Definition, Method Version, Subject, Manifest, and direct
   dependency identities;
10. lossless Provenance carriage with association preserved;
11. one complete Canonical Temporal Claim with exact timestamp meaning;
12. identical semantic inputs producing identical identity, canonical bytes,
    and hash representation;
13. round-trip reconstruction yielding the same complete semantic result;
14. permutation invariance for every canonically ordered collection;
15. identity sensitivity for every included semantic coordinate;
16. identity independence for every explicitly excluded non-semantic
    coordinate;
17. exact absence representation with no placeholder value;
18. a permitted partial-result envelope if, and only if, the frozen semantic
    contract in WP4 section 6.8 retains that possibility, preserving the full
    requested window / exact shorter available window / prohibited fallback
    window distinctions;
19. boundary text, timestamp, numeric, and imported-byte representations; and
20. a documentary handoff showing that a later method-specific value can be
    carried without WP5 defining its formula;
21. every admitted deterministic relation or affirmative non-relation between
    upstream input Degraded States and the result's own Degraded State; and
22. every admitted deterministic relation or affirmative non-relation between
    dependency-result sufficiency/outcome/state and the consuming result's own
    classifications, with producing-domain ownership preserved.

### 9.3 Required negative vectors

The negative corpus must reject, at minimum:

1. a value where the admitted mapping prohibits one;
2. a missing value where the admitted mapping requires one;
3. `null`, zero, empty, NaN, sentinel, previous, cached, or partial value used
   as an ungoverned absence substitute;
4. `UNAVAILABLE` used as a Portfolio Computation Outcome;
5. a new or Portfolio-prefixed Degraded State;
6. an incomplete Canonical Temporal Claim;
7. an ambient or wall-clock authoritative timestamp;
8. missing or substituted Definition, Method Version, Subject, Manifest, or
   dependency lineage;
9. a compatible/latest Method Version substituted for the exact version;
10. omitted, detached, reconstructed, corrected, or laundered Provenance;
11. a provider, runtime, database, cache, request, Workspace, Current
    Selection, or UI value entering identity or classification;
12. unordered, duplicate, conflicting, unknown, or free-text canonical
    reasons contrary to the reason grammar;
13. a reason code used as an outcome, state, evidence item, or evaluation;
14. a sufficiency value inferred from truth, quality, freshness, or trust;
15. `SUCCEEDED` or its eventual admitted equivalent interpreted as correct,
    trusted, current, production-ready, or runtime-available;
16. an applicability result relabelled as sufficiency, outcome, or state;
17. a WP4 predicate relabelled directly without the WP5 mapping;
18. altered imported upstream canonical bytes;
19. ambiguous framing or identity collision;
20. alternate field order, encoding, normalization, timestamp, numeric, or
    absence form claiming the same canonical bytes;
21. unknown fields or enum values accepted permissively;
22. a partial result without explicit method permission;
23. a result spanning more than one Portfolio;
24. a Market Measure Result relabelled as a Portfolio Measure Result; and
25. any fixture that asserts executable, runtime, provider, persistence, API,
    UI, or production authority;
26. a degraded, non-success, or non-satisfied result with no deterministic
    reason;
27. an upstream input Degraded State silently propagated to, silently
    discarded from, aggregated into, or restated as the result's own state
    without the exact governed relation;
28. a dependency result's sufficiency, outcome, or state silently propagated
    to, silently discarded from, aggregated into, or relabelled as the
    consuming result's classifications;
29. artificial Subject, Manifest, or Result bytes, identity, or hash presented
    as effective, concrete, normative, or conformance evidence; and
30. a WP5-defined or implied nested encoding that purports to close the
    M42-WP7 Composition-byte or WP4 annualization gap.

### 9.4 Vector format

Each documentary vector must record:

- stable vector identifier;
- purpose;
- authorities cited;
- all exact preconditions;
- exact imported identities or documentary placeholders with unmistakable
  non-production labels;
- candidate semantic result;
- expected admission or rejection;
- expected classification relation;
- expected value-presence decision;
- expected reason ordering where applicable;
- expected canonical representation and identity/hash evidence when the
  vector tests those concerns;
- for every byte-, identity-, round-trip-, permutation-, or hash-oriented
  vector, the exact labels `ARTIFICIAL`, `NON-EFFECTIVE`, and
  `NOT CONFORMANCE EVIDENCE`;
- rule traceability; and
- a statement that the vector is non-executable and non-production.

No expected value may be produced by invoking repository code. Independent
readers must be able to derive the expected documentary result solely from
the confirmed contracts and the vector's exact stated inputs.

---

## 10. Fixture strategy

WP5 fixture work is documentary and additive.

### 10.1 Corpus organization

The planned corpus is:

- `docs/implementation/m43/fixtures/M43_WP5_POSITIVE_DOCUMENTARY_VECTORS.md`;
- `docs/implementation/m43/fixtures/M43_WP5_NEGATIVE_DOCUMENTARY_VECTORS.md`.

The positive file contains admitted and boundary cases, including canonical
bytes, identity, round-trip, and hash-stability expectations. The negative
file contains structural, semantic, authority, classification, and
serialization rejection cases.

All canonical-byte, identity, round-trip, permutation, and hash-stability
expectations remain artificial, non-effective, and incapable of establishing
conformance while the inherited Composition-byte gap is open.

### 10.2 Fixture derivation

Fixtures must be derived in dependency order:

1. select or cite a frozen WP2 documentary Definition and Method Version;
2. select or cite a frozen WP3 Subject and conforming Manifest;
3. state exact frozen WP4 predicate inputs without changing them;
4. apply only the WP5 classification and envelope rules under review;
5. assemble the complete result semantics;
6. derive expressly artificial canonical representation, identity, and hash
   evidence using the normative documentary rules, without defining or
   implying any missing nested encoding; and
7. have an independent reviewer reconstruct the same result without using
   production or repository calculation code.

Where the frozen upstream corpus deliberately uses artificial documentary
identities, WP5 must preserve that label. A documentary placeholder does not
prove that a production dependency, method, Composition, or result exists.
Every affected WP5 vector must add the exact `ARTIFICIAL`, `NON-EFFECTIVE`,
and `NOT CONFORMANCE EVIDENCE` labels. No fixture may cure, conceal, or
supersede the M42-WP7 Composition canonical-byte gap or the WP4 section 6.7
annualization gap.

### 10.3 Traceability and coverage

A fixture traceability table must map every:

- result field and conditional-presence rule;
- sufficiency value;
- outcome value;
- Degraded State interaction;
- upstream input-state relation or affirmative non-relation;
- dependency-result classification relation or affirmative non-relation;
- reason rule;
- lineage coordinate;
- Provenance-carriage rule;
- temporal-claim coordinate;
- identity inclusion/exclusion;
- canonical serialization choice;
- inherited representability constraint and artificial-evidence label;
- no-default row; and
- prohibited interpretation

to at least one positive or boundary vector and at least one applicable
negative vector. Uncovered normative rules block confirmation.

---

## 11. Dependency-safe implementation sequence

“Implementation” in this section means documentary specification work only.
It grants no source-code or runtime authority.

1. **Freeze the baseline.** Record M43 Architecture and WP1-WP4 as immutable
   citations. Capture a repository diff proving they are not edited.
2. **Confirm the authority ledger.** Enumerate every WP5 concern with one
   semantic owner, governing authority, and unique placement.
3. **Run the vocabulary-sufficiency gate.** Confirm that frozen WP1 nouns and
   reused external nouns cover the complete scope. If a new noun is found,
   stop only the dependent drafting path and run the separately reviewed
   downstream vocabulary workflow.
4. **Build the upstream handoff register.** Cite exact WP2 identities and
   applicability/dependency boundaries, exact WP3 Subject/Manifest and
   Provenance-association boundaries, exact WP4 predicates, the WP2 section
   5.2 byte-equivalence disposition, both inherited representability gaps,
   and the standing WP1 section 7.4 WP6 block.
5. **Draft the result-envelope boundary.** Specify closed composition,
   immutability, equivalence, and value-presence surfaces without defining
   concrete method values.
6. **Specify Portfolio Input Sufficiency.** Close its values, meanings,
   reason obligations, and total mapping from exact declared prerequisites.
7. **Specify Portfolio Computation Outcome.** Close its values, meanings,
   reason obligations, and total completion mapping while preserving the
   `UNAVAILABLE` reservation.
8. **Specify orthogonality and interaction.** Complete the applicability /
   sufficiency / outcome / state / reason / value-presence matrix without
   importing Market-owned values by assumption. Close the deterministic
   relation or affirmative non-relation for upstream input states and
   dependency-result classifications while preserving producing-domain
   ownership.
9. **Specify Canonical Temporal Claim compatibility.** Bind the complete
   M34-D-0005 tuple and define exact timestamp meaning without ambient time.
10. **Specify lineage and Provenance carriage.** Bind exact WP2/WP3
    identities, preserve input association, and prohibit recapture or
    laundering.
11. **Specify Portfolio Deterministic Calculation obligations.** State the
    complete semantic reproducibility and non-default invariants without an
    algorithm or runtime design.
12. **Close the no-default register.** Resolve every row in section 8,
    explicitly recording retained and rejected alternatives.
13. **Specify canonical identity and serialization.** Close field set/order,
    framing, encoding, absence, imported bytes, identity inclusion/exclusion,
    rejection, and round-trip obligations. Fix result canonical bytes as
    identity; constrain any hash to a derived documentary non-substituting
    artifact; and preserve the fail-closed prohibition on concrete result
    bytes, identity, or hash while nested canonical bytes remain unavailable.
14. **Author positive and boundary vectors.** Cover every admitted
    classification and representation choice.
15. **Author negative vectors.** Cover every authority leak, invalid
    combination, prohibited default, collision, and non-canonical variant.
16. **Complete traceability.** Map every normative rule and no-default row to
    documentary evidence.
17. **Perform whole-corpus scans.** Search for new nouns, copied Market
    ownership, `Portfolio Degraded State`, `UNAVAILABLE` as outcome, hidden
    defaults, value-on-failure, provenance recapture, live state, runtime
    behavior, formulas, and edits to frozen artifacts.
18. **Perform independent constitutional review.** Review scope, ownership,
    placement, classification closure, external-authority preservation,
    vocabulary, and non-authority.
19. **Perform independent serialization and reconstruction review.** A
    separate reviewer reconstructs identities, canonical representations,
    round trips, reason order, and hash evidence without repository code.
20. **Apply required corrections only within WP5 artifacts.** Never cure a
    finding by modifying or reinterpreting M43 Architecture or WP1-WP4.
21. **Obtain independent confirmation.** Freeze WP5 only when all acceptance
    criteria pass and unresolved findings are `NONE`.
22. **Preserve downstream gates.** WP5 confirmation supplies a citable
    contract but does not admit WP6-WP8 methods, authorize WP9 implementation,
    mark a roadmap capability complete, release the WP1 section 7.4 WP6
    governance block, or close the WP4 section 6.7 annualization gap.

The sequence is dependency-safe because composition is specified only after
authority, vocabulary, and upstream handoffs; classifications are fixed
before their serialization; identity is fixed before stability vectors; and
review occurs only after complete traceability.

---

## 12. Independent review strategy

### 12.1 Constitutional review

The constitutional reviewer must verify:

- exact match to the frozen M43-WP5 allocation;
- no redesign of M43 or WP1-WP4;
- no new noun without the downstream vocabulary gate;
- exactly one semantic owner and one normative placement per concern;
- exact distinction among applicability, Portfolio Input Sufficiency,
  Portfolio Computation Outcome, Degraded State, reasons, and Evaluation;
- exact M34-D-0005 reuse with no `Portfolio Degraded State`;
- `UNAVAILABLE` remains only a Degraded State;
- Market result patterns are precedent only and no Market-owned type/value is
  silently widened;
- no change to Provenance meaning or capture;
- Connectivity & Ingestion remains the sole owner of Provenance meaning and
  capture, while WP5 owns only the result carriage relation;
- exact inheritance of the WP3 Composition-byte and WP4 annualization
  representability gaps, with no nested encoding supplied or implied;
- exact disposition of the WP2 section 5.2 expectation without an upstream
  serializer;
- exact closure of upstream-state and dependency-result relations or
  affirmative non-relations without propagation, discard, aggregation, or
  ownership transfer;
- every degraded, non-success, or non-satisfied result has at least one
  deterministic reason;
- result canonical bytes are identity and every hash is derived,
  documentary, and non-substituting;
- WP5 confirmation releases neither the standing WP6 block nor the
  annualization gap;
- no value/formula/method-family authority;
- no capability, runtime, implementation, provider, persistence, API, UI, or
  production expansion;
- complete no-default closure;
- unique repository placement; and
- no frozen artifact modification.

### 12.2 Serialization and reconstruction review

An independent reviewer must:

- reconstruct each positive result from its exact documentary inputs;
- verify the closed field set and every conditional-presence rule;
- verify exact reason cardinality, ordering, duplication, and conflict rules;
- verify imported identities and canonical bytes remain unchanged;
- verify every affected vector is visibly artificial, non-effective, and not
  conformance evidence;
- verify identity sensitivity and independence;
- verify canonical bytes are the sole result identity and no hash substitutes
  for identity or creates an upstream digest requirement;
- derive the same canonical representation and hash evidence;
- round-trip every admitted representation to the same semantic result;
- reject each non-canonical alternative and collision vector;
- verify cross-platform independence from locale, host encoding, object
  ordering, clock, database, provider, cache, and runtime; and
- confirm that no executable artifact was used as normative authority.

### 12.3 Fixture and boundary review

The fixture reviewer must verify:

- total coverage of every sufficiency/outcome/state/value combination;
- positive and negative coverage of every no-default row;
- correct boundaries among applicability, manifest conformance, WP4
  predicates, classification, and value presence;
- complete lineage and lossless Provenance association;
- explicit artificial-documentary labels where required;
- positive and negative coverage of upstream-state and dependency-result
  relation/non-relation rules;
- no fixture silently admits a formula or production method; and
- two independent readers reach the same admission/rejection conclusion.

### 12.4 Mandatory independence

The primary normative author must not self-confirm WP5. Constitutional and
serialization conclusions may appear in one coordinated review artifact only
when the artifact identifies separate review dimensions, evidence, and
conclusions. Final confirmation must cite resolved findings and state
unresolved findings as `NONE`.

---

## 13. Acceptance criteria

WP5 is complete only when all of the following are true:

1. every frozen WP5 scope item has one normative rule;
2. every concern has exactly one semantic owner;
3. every concern has exactly one normative placement;
4. no new constitutional noun exists, or any unavoidable noun has completed
   the frozen downstream vocabulary gate without reopening WP1;
5. Portfolio Measure Result has one closed immutable semantic contract;
6. its canonical bytes are its sole identity, identity equivalence and
   immutability are exact, and any hash is derived, documentary,
   non-substituting, and creates no implementation, registry, locator, or
   upstream digest authority;
7. Portfolio Input Sufficiency has a closed, Portfolio Intelligence-owned
   value set, exact meanings, reason obligations, and total mapping;
8. Portfolio Computation Outcome has a closed, Portfolio Intelligence-owned
   value set, exact meanings, reason obligations, and total mapping;
9. Portfolio Deterministic Calculation has exact result-level reproducibility
   obligations and creates no algorithm or correctness claim;
10. applicability, sufficiency, outcome, Degraded State, reason, and
    Evaluation remain orthogonal;
11. `UNAVAILABLE` is only a Degraded State and never an outcome;
12. no `Portfolio Degraded State` noun or seventh state is introduced;
13. the exact deterministic relation or exact affirmative non-relation between
    upstream input Degraded States and the result's own Degraded State is
    closed, preserves producing-domain ownership, and creates no aggregation
    grammar;
14. the exact deterministic relation or exact affirmative non-relation between
    consumed dependency-result sufficiency/outcome/state and the consuming
    result's classifications is closed, preserves producing-domain ownership,
    and creates no new state, axis, owner, or aggregation grammar;
15. every admitted classification combination has an exact value-presence or
    value-absence rule;
16. prohibited value cases cannot carry a placeholder, sentinel, stale,
    prior, partial, or default value;
17. every result cites exact Definition, Method Version, Subject, Manifest,
    and direct dependency lineage as required;
18. already-captured Provenance is carried exactly, losslessly, and with its
    association intact, without recapture or reinterpretation;
19. Connectivity & Ingestion remains the sole owner of Provenance meaning and
    capture under Platform Architecture section 6.4 and M42-WP6, while
    Portfolio Intelligence owns only the WP5 result carriage relation;
20. every result carries a complete Canonical Temporal Claim compatible with
    M34-D-0005;
21. authoritative timestamp meaning and representation are explicit and
    independent of ambient time;
22. every reason is deterministic, ordered, non-judgmental, and incapable of
    creating a new classification axis;
23. at least one deterministic reason is required for every result carrying
    any of the six approved M34-D-0005 Degraded States and for every
    non-success Portfolio Computation Outcome or non-satisfied Portfolio Input
    Sufficiency; `optional` and `forbidden` are inadmissible for those cases,
    and no non-degraded value is implied or introduced;
24. every no-default row is explicitly resolved;
25. canonical representation is independent of runtime, language, locale,
    database, provider, cache, UI, and host configuration;
26. positive, negative, boundary, permutation, round-trip, identity, and
    hash-stability vectors are complete and traceable;
27. every byte-, identity-, round-trip-, permutation-, and hash-oriented
    vector is visibly `ARTIFICIAL`, `NON-EFFECTIVE`, and
    `NOT CONFORMANCE EVIDENCE`;
28. while the M42-WP7 Composition canonical-byte gap remains open, no concrete
    Portfolio Measure Result canonical byte sequence, identity, or hash is
    emitted or treated as normative, and WP5 defines or implies no missing
    nested encoding;
29. two independent readers reconstruct the same semantic result, artificial
    canonical representation, identity, reasons, and hash evidence;
30. all Market-owned vocabulary and result patterns remain externally owned
    precedent only;
31. WP1-WP4 vocabulary dispositions, ownership, identities, canonical bytes,
    semantics, predicates, and
    representability rules are consumed without amendment;
32. the WP2 section 5.2 Definition-record byte-equivalence expectation is
    expressly left open under separately authorized source governance, WP2's
    interim documentary field-comparison rule remains in force, and WP5
    defines no upstream serializer;
33. partial-result envelope rules cite and preserve frozen WP4 section 6.8,
    including the full requested window, exact shorter available window, and
    prohibited fallback window distinctions;
34. concrete value meaning and formulas remain with WP2 and WP6-WP8;
35. runtime, source-code, implementation, persistence, API, UI, provider,
    production-method, and executable-validation authority remain `NONE`;
36. WP5 confirmation does not release the WP1 section 7.4 WP6 governance block
    and does not close the WP4 section 6.7 annualization representability gap;
37. no capability is declared implemented or complete;
38. no frozen M1-M43-WP4 artifact is modified;
39. the documentary implementation order is dependency-safe;
40. independent constitutional review is approved;
41. independent serialization/reconstruction review is approved; and
42. unresolved findings are `NONE`.

Failure of any item blocks confirmation.

---

## 14. Risks and mandatory responses

| Risk | Mandatory response |
| --- | --- |
| M41 Market result contract is copied and relabelled | Use it only as mechanical review precedent; derive every WP5 choice from frozen M43 authority |
| Market-owned sufficiency or outcome values are silently inherited | Independently specify the Portfolio-owned closed sets under WP1 meaning and review every collision |
| `UNAVAILABLE` becomes an outcome | Reject it; preserve M34-D-0005 and M40-WP1 section 8.3 |
| A new `Portfolio Degraded State` axis appears | Reject the noun and reuse exact Degraded State grammar |
| Manifest completeness is treated as sufficiency | Preserve WP3 as one structural precondition; WP5 owns the later total mapping |
| Applicability is treated as outcome or insufficiency | Preserve WP2 orthogonality and specify an explicit relation without relabelling |
| WP4 predicates pre-decide WP5 classifications | Consume facts and define the WP5 mapping under WP5 authority |
| Upstream states or dependency-result classifications silently propagate or disappear | Require an exact deterministic relation or affirmative non-relation, preserve each producing-domain claim, and cover propagation and discard with positive and negative vectors |
| Non-success carries a plausible value | Enforce exact presence/absence rules and direct negative vectors |
| A degraded, unavailable, non-success, or non-satisfied result has no reason | Require at least one deterministic reason; `optional` and `forbidden` are inadmissible for those cases |
| Partial result silently changes method meaning | Require explicit later method permission and exact envelope rules; otherwise reject |
| Provenance is reconstructed from lineage | Carry only exact already-captured Provenance and preserve associations |
| Serialization redefines upstream bytes | Import with exact framing; never reserialize as source authority |
| Artificial bytes conceal an upstream representability gap | Apply all three artificial/non-effective/non-conformance labels and prohibit WP5 from defining or implying the missing nested encoding |
| Database, API, or cache identifiers become semantic identity | Exclude non-semantic implementation coordinates explicitly |
| Timestamp is generated from wall clock | Require one frozen-authority-compatible semantic timestamp source and fail closed otherwise |
| Hash becomes a second identity axis | Make result canonical bytes the sole identity and constrain any hash to a derived, documentary, non-substituting artifact |
| WP2 section 5.2 is read as upstream-serialization authority | Keep its interim field comparison in force and route record-level bytes to separately authorized source governance |
| Reason text becomes a new judgment axis | Use closed deterministic codes and keep free text non-canonical or prohibited as specified |
| Unknown fields are accepted for convenience | Require explicit fail-closed schema/version behavior |
| Documentary vectors become executable authority | Keep Markdown/data-only evidence and prohibit runners or conformance harnesses |
| WP5 defines a formula or value shape | Carry only exact later method-governed values; retain formula authority in WP6-WP8 |
| Result semantics imply correctness or production readiness | Restate the Trust & Evaluation and production-admission exclusions in contract and vectors |
| WP5 confirmation is inferred to release WP6 or annualization work | State in the contract, review, and confirmation that both standing constraints remain independently governed and active |
| Frozen predecessors are edited to resolve a WP5 issue | Correct WP5 only or fail closed pending separately authorized upstream governance |

---

## 15. Repository modifications

### 15.1 Modification authorized by this work item

This work item creates only:

- `docs/implementation/M43_WP5_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md`.

It creates no normative WP5 contract, fixture, review, confirmation, runtime,
or production behavior.

### 15.2 Planned WP5 documentary artifacts

Later, separately reviewed steps within the documentary WP5 sequence may add:

- `docs/implementation/M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md`;
- `docs/implementation/m43/fixtures/M43_WP5_POSITIVE_DOCUMENTARY_VECTORS.md`;
- `docs/implementation/m43/fixtures/M43_WP5_NEGATIVE_DOCUMENTARY_VECTORS.md`;
- `docs/implementation/M43_WP5_INDEPENDENT_CONSTITUTIONAL_REVIEW.md`;
- `docs/implementation/M43_WP5_REQUIRED_CORRECTIONS_RESPONSE.md`, only if
  required; and
- `docs/implementation/M43_WP5_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md`.

If a new noun is discovered, any vocabulary-gate artifact and confirmed
Glossary synchronization must occur only through the separately authorized
downstream vocabulary workflow. This plan predicts that no such noun is
required and authorizes no Glossary change.

### 15.3 Prohibited repository effect

WP5 must not modify:

- M43 Architecture or WP1-WP4 artifacts;
- any M1-M42 frozen artifact;
- backend or frontend source;
- executable tests or fixtures;
- database schemas or migrations;
- API, UI, provider, operational, deployment, or cache files;
- ROADMAP capability-completion status;
- production registries or methods; or
- consolidated index, status, or decision-log files except under a separately
  authorized M43 closeout workflow.

---

## 16. Completion report requirements

The WP5 planning completion report must state:

1. **Implementation summary** — that the constitutional scope and documentary
   implementation plan was created, with no implementation or runtime work;
2. **Files created** — the exact repository-relative path of this artifact;
3. **Validation performed** — scope trace, ownership/placement audit,
   vocabulary scan, authority/non-authority audit, dependency-order review,
   frozen-artifact diff review, and documentary-only verification;
4. **Frozen-work-package confirmation** — an explicit statement that M43
   Architecture and WP1-WP4 remain complete, canonical, unmodified, and
   frozen;
5. **Authority confirmation** — runtime, source-code, persistence/API/UI,
   implementation, provider, production-method, and executable-validation
   authority remain `NONE`;
6. **Repository effect** — no production behavior or roadmap capability was
   changed; and
7. **Open findings** — every unresolved issue, or `NONE`.

The completion report for the later full WP5 documentary package must also
list the normative specification, fixtures, independent review,
required-corrections response if any, and independent confirmation, together
with their status and unresolved findings.

---

## 17. Final constitutional boundary

M43-WP5 defines how one exact Portfolio calculation is represented as one
immutable, reproducible, owner-explicit Portfolio Measure Result. It consumes
frozen identities and deterministic facts, classifies them under the admitted
Portfolio-owned axes, carries exact lineage and already-captured Provenance,
reuses the complete Canonical Temporal Claim and Degraded State grammar, and
fixes result identity and canonical representation.

It does not calculate a Portfolio measure, define a formula, choose a method,
obtain evidence, infer a missing coordinate, evaluate correctness, produce a
recommendation, implement a serializer, persist a result, expose an API,
render a UI, select a provider, or authorize production behavior.

All prior M43 decisions remain frozen. WP5 fills only the result-contract
space that the frozen architecture reserved to WP5.
