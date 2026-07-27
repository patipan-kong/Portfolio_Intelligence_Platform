# M42-WP6 — Portfolio Lifecycle State Reuse & Provenance Contract Specification

**Work package:** M42-WP6

**Date:** 2026-07-27

**Artifact type:** Documentation-only, implementation-neutral semantic contract

**Admission result:** `ADMIT WITH NARROWING`

**Governed surface:** Exact reuse and citation of Portfolio Lifecycle State;
preservation and carriage of already-captured Provenance; downstream handoff
to Portfolio Composition

**New governed noun:** `NONE`

**Primary constitutional owner:** Ledger & Accounting

**Portfolio Lifecycle State owner:** Ledger & Accounting

**Provenance meaning and capture owner:** Connectivity & Ingestion

**Portfolio Composition owner:** Portfolio Intelligence

**Lifecycle execution authority:** `NONE`

**Lifecycle-transition authority:** `NONE`

**Provenance-capture authority:** `NONE`

**Provenance-confidence authority:** `NONE`

**Provider-mapping authority:** `NONE`

**Implementation authority:** `NONE`

**Runtime authority:** `NONE`

**Persistence authority:** `NONE`

**API authority:** `NONE`

**Schema authority:** `NONE`

**Serialization authority:** `NONE`

**Audit authority:** `NONE`

**Event-sourcing authority:** `NONE`

**Reconciliation authority:** `NONE`

**Authorization authority:** `NONE`

**Executable-validation authority:** `NONE`

**Document status:** `COMPLETE`

**Independent Review result:** `APPROVED`

**Required corrections:** `NONE`

Normative terms such as **MUST**, **MUST NOT**, **REQUIRED**, and **MAY** govern
only the meaning and reviewability of this documentation-only contract. They
do not authorize lifecycle execution, transition behavior, provenance capture,
an implementation, a runtime, persistence, an API, a schema, serialization,
audit behavior, event sourcing, reconciliation, provider mapping,
authorization, executable validation, or production adoption.

---

## 1. Executive Summary

This specification defines the narrowed M42-WP6 semantic contract. It admits
no new vocabulary and owns neither Portfolio Lifecycle State nor Provenance.
It governs only:

1. binding a cited Portfolio Lifecycle State fact to one exact Portfolio
   Identity and its corresponding Accounting Scope;
2. reusing and citing that Ledger & Accounting-owned state exactly;
3. preserving and carrying Provenance that its source owner already captured;
   and
4. handing those cited coordinates to the Portfolio Intelligence-owned
   Portfolio Composition in M42-WP7 without changing meaning or ownership.

Portfolio Lifecycle State retains its complete frozen meaning:

> The recorded `active`, `archived`, or `closed` lifecycle state of one
> Portfolio Identity. It qualifies what the portfolio may do next and never
> rewrites Portfolio Identity, Accounting Scope, ledger history, or evaluation
> history.

That meaning is imported by citation from the canonical Glossary,
`M34-D-0002`, and `M36-WP1-A01/A09`; it is not defined anew here. Ledger &
Accounting remains its sole semantic owner.

Provenance retains its frozen generic meaning, “Where a fact came from.”
Connectivity & Ingestion retains ownership of that meaning and of capture.
WP6 specifies carriage only: already-captured Provenance remains associated
with its source fact, remains attributable to its source owner, and reaches
WP7 without omission, substitution, enrichment, reinterpretation, or
ownership transfer.

Portfolio Lifecycle State and Provenance remain distinct. Provenance does not
determine, validate, or change a lifecycle-state value. A lifecycle-state
value does not create, validate, replace, or reinterpret Provenance.

This contract defines no lifecycle execution, lifecycle transition, lifecycle
operation, provenance capture, provenance confidence, provider mapping,
implementation, runtime, persistence, API, schema, serialization, audit,
event-sourcing, reconciliation, authorization, or implementation semantic.

---

## 2. Scope

### 2.1 Governing authority and precedence

This specification is subordinate to, and MUST be read consistently with:

1. the frozen
   [Platform Architecture](../architecture/platform_architecture.md),
   including Ledger & Accounting ownership of recorded truth and replayable
   state, Connectivity & Ingestion ownership of Provenance at capture, and the
   universal provenance-and-auditability obligation;
2. the frozen `M34-D-0002` decision, which decomposes the Portfolio container
   across existing constitutional domains;
3. the frozen
   [M36-WP1 Multiple-Portfolio Foundation](M36_WP1_Multiple_Portfolio_Foundation.md),
   especially `M36-WP1-A01` and `M36-WP1-A09`;
4. the canonical [Glossary](../GLOSSARY.md) entries for Portfolio Identity,
   Accounting Scope, Portfolio Lifecycle State, Provenance, and Portfolio
   Composition;
5. the frozen
   [M42 Architecture Proposal](M42_ARCHITECTURE_PROPOSAL.md), especially its
   reuse-only WP6 allocation and terminal WP7 boundary;
6. the confirmed
   [M42-WP1 Portfolio Canonical Vocabulary and Ownership Register](M42_WP1_PORTFOLIO_CANONICAL_VOCABULARY_AND_OWNERSHIP_REGISTER.md);
7. the confirmed
   [M42-WP2 Portfolio Identity, Accounting Scope, Membership and Base Currency
   Contract Specification](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md);
8. the completed
   [M42-WP3 Investment Universe Declaration Contract Specification](M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md);
9. the completed
   [M42-WP4 Portfolio Policy Ownership Investigation](M42_WP4_PORTFOLIO_POLICY_OWNERSHIP_INVESTIGATION.md);
10. the completed
    [M42-WP5 Portfolio Benchmark Declaration Contract Specification](M42_WP5_PORTFOLIO_BENCHMARK_DECLARATION_CONTRACT_SPECIFICATION.md);
    and
11. the completed
    [M42-WP6 Ownership Validation](M42_WP6_Proposed_Architectural_Specification.md),
    whose `ADMIT WITH NARROWING` result is the admission boundary for this
    contract.

On conflict, the earlier or source-owning authority controls. This contract
cites those authorities without amending, duplicating, extending, correcting,
or transferring them.

### 2.2 Included surface

The complete WP6 contract surface is:

1. exact subject binding to one cited Portfolio Identity and its corresponding
   Accounting Scope;
2. exact reuse of the frozen Portfolio Lifecycle State meaning;
3. exact citation of one Ledger & Accounting-owned Portfolio Lifecycle State
   fact;
4. preservation of the permanent Portfolio Identity, corresponding Accounting
   Scope, ledger history, and evaluation history invariants already attached
   to that state;
5. preservation and carriage of Provenance already captured for a cited
   coordinate;
6. preservation of the association between carried Provenance and the exact
   coordinate from which it came;
7. preservation of every cited coordinate's semantic owner;
8. documentation-only positive and negative golden vectors; and
9. transfer of the cited subject, lifecycle-state, and Provenance coordinates
   to M42-WP7 for citation in Portfolio Composition.

The phrases **subject binding**, **state citation**, **provenance carriage**,
**owner attribution**, and **handoff coordinate** describe contractual
relationships. They are not new governed nouns, runtime types, schema fields,
serialized members, persistence structures, or vocabulary admissions.

### 2.3 Excluded surface

This contract does not define or authorize:

- lifecycle execution or any state machine;
- lifecycle transitions, transition graphs, transition legality, transition
  legitimacy, transition approval, or transition validation;
- create, activate, archive, close, reopen, merge, split, clone, import, or
  export behavior;
- commands, workflows, orchestration, operation ordering, retries, rollback,
  compensation, scheduling, or control flow;
- rules determining what an `active`, `archived`, or `closed` portfolio may
  read, write, execute, display, select, or do;
- Portfolio Status, Current Selection, availability, permission, authority,
  authorization, action eligibility, degradation, or runtime currentness;
- provenance capture, recapture, reconstruction, generation, enrichment,
  normalization, adjudication, reconciliation, deduplication, source
  selection, evidence classification, custody, retention, or provider mapping;
- provenance completeness at capture, provenance confidence, trust, quality,
  correctness, sufficiency, or evidentiary weight;
- an audit record, audit log, audit mechanism, event, event stream,
  event-sourcing rule, or replay mechanism;
- implementation, persistence, database design, schema, migration, backfill,
  default, cache, runtime object, service, API, serialization, canonical bytes,
  field name, field order, transport, provider integration, UI, executable
  validator, test code, production behavior, or implementation semantics; or
- any ownership transfer or any new noun such as Portfolio Provenance,
  Lifecycle Provenance, Lifecycle Event, or Lifecycle Transition.

The contract is semantic documentation only. Nothing here prescribes how a
state or Provenance is produced, changed, recorded, stored, queried,
transported, serialized, displayed, validated, reconciled, audited, or acted
upon.

---

## 3. Subject Binding

### 3.1 Binding coordinate

Each Portfolio Lifecycle State citation governed by WP6 MUST:

1. name exactly one explicitly cited Portfolio Identity;
2. name exactly one explicitly cited Accounting Scope; and
3. bind the cited state fact to that Portfolio Identity and its corresponding
   Accounting Scope.

Portfolio Identity and Accounting Scope are reused at their exact frozen
M42-WP2 meanings. WP6 adds no identity attribute, identity variant,
accounting boundary, correspondence rule, membership rule, or alternate
subject.

An ambient, inferred, current, selected, default, unnamed, cross-portfolio, or
mismatched subject is outside this contract.

### 3.2 Binding invariants

The following invariants are preserved by citation:

1. Portfolio Identity is permanent across lifecycle qualification.
2. The corresponding Accounting Scope is not rewritten, re-keyed, merged,
   split, replaced, or deleted by the cited lifecycle state.
3. Ledger history is not rewritten by the cited lifecycle state.
4. Evaluation history is not rewritten by the cited lifecycle state.
5. Subject binding does not depend on Current Selection, Portfolio Status,
   source availability, actor authority, permission, action eligibility,
   transition legitimacy, or a runtime clock.

These are preservation constraints on meaning. They define no transition,
operation, temporal evaluation, persistence behavior, replay behavior, or
runtime enforcement.

### 3.3 Citation without transfer

Subject binding does not transfer ownership:

- Ledger & Accounting retains sole ownership of Portfolio Identity,
  Accounting Scope, and Portfolio Lifecycle State;
- Connectivity & Ingestion retains ownership of Provenance meaning and
  capture;
- each other source owner retains ownership of any other coordinate whose
  already-captured Provenance is carried under this contract;
- Portfolio Intelligence owns only the terminal Portfolio Composition that
  may cite and carry those coordinates under WP7; and
- citation, adjacency, preservation, carriage, or composition creates no
  shared ownership.

---

## 4. Portfolio Lifecycle State Reuse and Citation

### 4.1 Exact reuse rule

WP6 MUST reuse Portfolio Lifecycle State exactly as frozen. Exact reuse means:

1. the canonical term remains **Portfolio Lifecycle State**;
2. the only cited state values are exactly `active`, `archived`, and `closed`;
3. the complete frozen meaning quoted in §1 remains unchanged;
4. Ledger & Accounting remains the sole semantic owner;
5. all frozen non-collision and history-preservation invariants remain intact;
   and
6. no new state, synonym, alias, transition, operation, exception, default, or
   implementation inference is introduced.

Exact reuse is semantic citation. It does not mean code reuse, object reuse,
runtime-state reuse, cached-state reuse, copying, cloning, restoration, or
reuse of a persisted representation.

### 4.2 Exact state citation

One WP6 lifecycle citation MUST identify:

1. the exact subject binding from §3; and
2. exactly one Ledger & Accounting-owned Portfolio Lifecycle State fact whose
   cited value is `active`, `archived`, or `closed`.

This is a semantic citation coordinate, not a prescribed object, tuple,
record, schema, payload, field list, or wire format.

The citation MUST preserve the source-owned state value without:

- renaming or translating it into a different canonical value;
- normalizing it into a broader or narrower state;
- inferring it from behavior, availability, selection, authority, permission,
  history, or another coordinate;
- replacing it with a default, fallback, approximation, status, or derived
  value; or
- treating the citation as authority to originate or change the state.

This per-fact exactness does not define how many lifecycle facts exist across
history, which fact is current at runtime, when a fact applies, or how any
fact came to be recorded.

### 4.3 Closed vocabulary and non-collisions

For WP6 citation purposes, no value other than `active`, `archived`, or
`closed` is admissible. In particular, WP6 MUST NOT introduce or treat as a
Portfolio Lifecycle State value:

- draft, pending, suspended, disabled, deleted, unavailable, degraded,
  imported, merging, cloned, pre-activation, or unknown;
- Portfolio Status;
- Current Selection;
- source availability;
- actor authority or permission;
- action eligibility; or
- transition legitimacy.

The phrase **Active Portfolio** is not a canonical concept and MUST NOT replace
an exact citation. The value `active` qualifies one cited Portfolio Identity;
it does not identify the portfolio a person is viewing and does not prove that
an action is permitted.

### 4.4 No lifecycle inference

The state citation has no independently authored operational consequence.
This contract MUST NOT interpret any cited value as:

- a command or request;
- evidence that a transition occurred lawfully;
- authority to perform an operation;
- permission to read, write, trade, calculate, or display;
- proof of availability or unavailability;
- a Current Selection or navigation instruction;
- a Portfolio Status or analytical judgment; or
- a rule governing what happens next.

The frozen definition's phrase “qualifies what the portfolio may do next” is
preserved exactly as source-owned meaning. WP6 does not elaborate that phrase
into an eligibility rule, transition rule, authorization rule, workflow, or
runtime behavior.

---

## 5. Provenance Carriage

### 5.1 Exact Provenance citation

Provenance retains the canonical Glossary meaning **“Where a fact came
from.”** WP6 cites that meaning and does not define a Portfolio-specific or
lifecycle-specific specialization.

When a source-owned coordinate is supplied with already-captured Provenance,
WP6 carriage MUST preserve:

1. the complete Provenance supplied by its source authority;
2. the association between that Provenance and the exact coordinate to which
   the source authority attached it;
3. the source coordinate's exact meaning;
4. the Provenance meaning as owned by Connectivity & Ingestion; and
5. the semantic-owner attribution of every cited coordinate.

“Complete” in this section means no part of the already-captured Provenance
made available by its source authority may be intentionally omitted,
substituted, or rewritten during semantic carriage. It does not define what
must have been captured, a capture format, a confidence threshold, an
evidence class, a storage shape, or a completeness test.

### 5.2 Preservation rules

Already-captured Provenance MUST be carried without:

- recapture, regeneration, reconstruction, or invention;
- parsing into a new canonical meaning;
- summarization that replaces the captured Provenance;
- normalization, enrichment, repair, correction, or translation;
- source ranking, source selection, confidence scoring, trust grading, or
  quality judgment;
- provider remapping or substitution;
- combination with another coordinate's Provenance in a way that obscures
  which origin belongs to which coordinate;
- detachment from its cited coordinate;
- attribution to Ledger & Accounting, Portfolio Intelligence, WP6, or WP7 as
  a new capture owner; or
- treatment as an audit record, transition record, authorization record, or
  correctness certificate.

WP6 MUST NOT manufacture Provenance when none was supplied by an upstream
source authority. This is a boundary on WP6 authority, not a statement about
whether an upstream source conformed to its own capture obligations.

### 5.3 State and Provenance independence

Portfolio Lifecycle State and Provenance are separate cited coordinates:

- Provenance does not determine or modify whether the cited state value is
  `active`, `archived`, or `closed`;
- Provenance is not proof that the state is correct, current, legitimate,
  authorized, available, or actionable;
- a state value does not create, validate, enrich, replace, or rank
  Provenance;
- a mismatch, absence, or concern outside this semantic contract grants WP6
  no reconciliation, correction, refusal, or adjudication authority; and
- carrying the two coordinates together does not merge their meanings or
  owners.

### 5.4 Carriage of other WP7 inputs

The provenance-carriage rule also applies when WP7 receives another frozen or
independently confirmed portfolio coordinate with already-captured
Provenance. WP6 does not define, validate, or reinterpret that coordinate. It
requires only that:

1. the coordinate be cited at its own confirmed meaning;
2. its already-captured Provenance remain associated with it;
3. its source owner remain explicit and unchanged; and
4. WP7 receive the coordinate and Provenance without semantic laundering.

This rule does not admit a rejected or unresolved coordinate, determine which
coordinates WP7 may compose, or create a portfolio-wide Provenance object.
WP7's separately governed contract controls the Portfolio Composition
surface.

---

## 6. Ownership Boundary

### 6.1 Ownership matrix

| Coordinate or meaning | Sole owner | WP6 authority |
|---|---|---|
| Portfolio Identity | Ledger & Accounting | Exact subject citation only |
| Accounting Scope | Ledger & Accounting | Exact corresponding-scope citation only |
| Portfolio Lifecycle State | Ledger & Accounting | Exact reuse and citation only |
| Lifecycle transitions and transition legitimacy | Existing governing boundaries; not allocated to WP6 | None |
| Provenance meaning | Connectivity & Ingestion | Exact citation only |
| Provenance capture | Connectivity & Ingestion | None |
| Already-captured Provenance | Its meaning and capture remain Connectivity & Ingestion-owned; its associated fact retains its own semantic owner | Preservation and carriage only |
| Other frozen or independently confirmed WP7 input | Its established source owner | Citation and provenance carriage only |
| Portfolio Composition | Portfolio Intelligence under M42-WP7 | Downstream handoff only |

### 6.2 Boundary rules

Ledger & Accounting's ownership is unchanged when WP6 cites Portfolio
Identity, Accounting Scope, and Portfolio Lifecycle State. WP6 has no
authority to originate, change, approve, reject, or execute a lifecycle state
or transition.

Connectivity & Ingestion's ownership is unchanged when WP6 preserves and
carries already-captured Provenance. Carriage does not become capture,
recapture, custody, reconciliation, audit, provider mapping, or evidence
judgment.

The source owner of every other cited coordinate remains unchanged.
Provenance carriage does not make Ledger & Accounting the semantic owner of an
Investment Universe, Portfolio Benchmark Declaration, Benchmark observation,
asset reference, or any other source-domain fact.

Portfolio Intelligence owns Portfolio Composition, not the coordinates it
cites. WP7 composition does not make Portfolio Intelligence a second source
of Ledger & Accounting facts or the owner of Provenance capture.

### 6.3 Citation and carriage never transfer ownership

Citation and carriage do not:

- copy source authority into WP6 or WP7;
- make a coordinate jointly owned;
- permit redefinition, extension, normalization, mapping, or correction;
- convert Provenance carriage into Provenance capture;
- convert composition into semantic ownership;
- grant lifecycle, transition, authorization, audit, reconciliation, provider,
  runtime, persistence, API, schema, serialization, or implementation
  authority; or
- allow a downstream consumer to attribute its own behavior to this contract.

---

## 7. Positive Golden Vectors

These vectors are normative documentary examples. They are not serialized
records, schema specimens, API payloads, events, commands, audit entries,
runtime scenarios, transition tests, validator outputs, or implementation
instructions. Labels such as `PI-01`, `AS-01`, `LS-01`, and `PROV-01` stand
only for exact source-owned citations; they prescribe no identifier or
representation.

| ID | Documentary specimen | Why it conforms |
|---|---|---|
| PGV-01 | Exact Portfolio Identity `PI-01`; its corresponding Accounting Scope `AS-01`; Ledger-owned state fact `LS-01` cites `active`; already-captured Provenance `PROV-01` remains attached to `LS-01`. | Exact subject, exact frozen value, exact owner, and unchanged provenance association |
| PGV-02 | Exact Portfolio Identity `PI-02`; corresponding Accounting Scope `AS-02`; Ledger-owned state fact `LS-02` cites `archived`; identity, scope, ledger history, and evaluation history remain cited without rewrite; `PROV-02` is carried unchanged. | Reuses the archived state and frozen preservation invariants without transition or deletion semantics |
| PGV-03 | Exact Portfolio Identity `PI-03`; corresponding Accounting Scope `AS-03`; Ledger-owned state fact `LS-03` cites `closed`; no permission, availability, selection, or action-eligibility conclusion is stated; `PROV-03` is carried unchanged. | Exact closed-state citation remains separate from operational consequence |
| PGV-04 | WP7 receives the `PI-01` / `AS-01` / `LS-01` citations and the associated `PROV-01`, and cites them in Portfolio Composition at their source-owned meanings. | Complete downstream handoff with no ownership transfer |
| PGV-05 | A confirmed Investment Universe coordinate enters WP7 with already-captured `PROV-IU-01`; the coordinate remains Portfolio Intelligence-owned, the Provenance meaning and capture remain Connectivity & Ingestion-owned, and WP6 adds no interpretation. | The generic carriage rule preserves coordinate-specific ownership and lineage |
| PGV-06 | A Portfolio Composition places a Ledger-owned lifecycle citation beside a Portfolio Intelligence-owned Portfolio Benchmark Declaration, carrying each coordinate's already-captured Provenance separately. | Adjacency and composition preserve distinct facts, associations, meanings, and owners |
| PGV-07 | A source supplies an exact lifecycle-state citation but supplies no Provenance to WP6; WP6 does not invent, infer, reconstruct, or claim Provenance. | Respects the no-capture boundary without deciding upstream conformance |
| PGV-08 | Two documentary handoff descriptions cite the same source-owned state fact and the same source-captured Provenance using different prose while preserving identical semantic meaning and association. | Semantic carriage is exact without prescribing serialization, bytes, fields, or syntax |

None of these vectors determines how a state or Provenance is captured,
represented, persisted, transported, serialized, validated, audited,
reconciled, displayed, or acted upon.

---

## 8. Negative Golden Vectors

These are prohibited documentary shapes. Their classification expresses
contract analysis only. It does not define executable validation, runtime
rejection, transition refusal, error handling, audit behavior, or enforcement.

| ID | Prohibited specimen | Contract breach |
|---|---|---|
| NGV-01 | “Use the currently selected portfolio's lifecycle state.” | Ambient subject and collision with Current Selection |
| NGV-02 | One lifecycle citation names `PI-A` and `PI-B`. | No exact single Portfolio Identity binding |
| NGV-03 | State for `PI-A` is paired with an Accounting Scope belonging to `PI-B`. | Breaks the exact corresponding Accounting Scope binding |
| NGV-04 | State value is `draft`, `pending`, `suspended`, `deleted`, `unknown`, or `imported`. | Introduces a non-canonical lifecycle value |
| NGV-05 | `enabled` replaces `active`, or `inactive` replaces `archived` or `closed`. | Renames or normalizes a frozen value |
| NGV-06 | “Active Portfolio” means the portfolio currently displayed. | Conflates Portfolio Lifecycle State with Current Selection |
| NGV-07 | `archived` is treated as Portfolio Status, source unavailability, or degraded analytical data. | Collides with separately governed meanings |
| NGV-08 | `closed` means the Portfolio Identity or Accounting Scope no longer exists. | Rewrites permanent identity and accounting boundary |
| NGV-09 | `archived` deletes, rewrites, or re-keys ledger or evaluation history. | Violates frozen history-preservation invariants |
| NGV-10 | `active` grants permission or proves action eligibility. | Adds authorization and operational meaning |
| NGV-11 | `closed` proves that a prior transition was legitimate. | Adds transition-legitimacy meaning |
| NGV-12 | The contract describes create, activate, archive, close, reopen, merge, split, clone, import, or export behavior. | Adds excluded lifecycle execution or operation semantics |
| NGV-13 | A state machine, transition graph, workflow, command, event, or event-sourcing rule is prescribed. | Adds excluded transition, runtime, audit, or persistence authority |
| NGV-14 | Already-captured Provenance is omitted while its associated fact is carried. | Breaks mandatory preservation and carriage |
| NGV-15 | Captured Provenance is replaced by a summary, digest, provider label, storage key, or locally reconstructed description. | Substitutes for source-captured Provenance |
| NGV-16 | WP6 enriches, normalizes, repairs, translates, or reclassifies Provenance. | Reinterprets an externally owned meaning |
| NGV-17 | Provenance for `LS-A` is attached to `LS-B`. | Breaks the coordinate-to-Provenance association |
| NGV-18 | Provenance from several coordinates is merged so their individual origins cannot be recovered. | Launders coordinate-specific origin |
| NGV-19 | WP6 creates Provenance when the source supplied none. | Acquires provenance-capture authority |
| NGV-20 | WP6 ranks sources, selects a preferred source, assigns confidence, or declares trust. | Adds source adjudication and provenance-confidence semantics |
| NGV-21 | Provenance is treated as proof that a lifecycle state is correct, current, authorized, legitimate, or actionable. | Conflates origin with correctness or authority |
| NGV-22 | A lifecycle-state value creates, validates, or replaces Provenance. | Conflates state with origin |
| NGV-23 | Ledger & Accounting is declared owner of Provenance capture because it owns Portfolio Lifecycle State. | Transfers Connectivity & Ingestion ownership |
| NGV-24 | Portfolio Intelligence becomes owner of Portfolio Lifecycle State or Provenance capture because WP7 composes them. | Transfers source ownership through composition |
| NGV-25 | WP6 defines Portfolio Provenance, Lifecycle Provenance, Lifecycle Event, or Lifecycle Transition. | Introduces an unauthorized governed noun |
| NGV-26 | WP6 defines provider identifiers, provider mappings, reconciliation rules, audit records, evidence classes, confidence scores, or retention rules. | Adds expressly excluded authority |
| NGV-27 | WP7 omits, defaults, repairs, enriches, substitutes, remaps, or reinterprets a handed-off lifecycle or Provenance coordinate. | Exceeds exact downstream citation-and-carriage authority |
| NGV-28 | A database table, JSON object, API field, schema, event payload, wire format, or canonical byte order is prescribed. | Adds implementation, persistence, API, schema, or serialization authority |
| NGV-29 | A runtime clock or lookup determines which lifecycle citation WP6 treats as current. | Adds runtime and temporal-selection semantics |
| NGV-30 | A missing provenance citation is declared proof that the state is invalid, or is silently filled with a default origin. | Adds evidentiary judgment, inference, and capture |

No negative vector authorizes the behavior it illustrates. “Prohibited” is a
documentation boundary classification, not an operational verdict.

---

## 9. Downstream Authority

### 9.1 Exact WP7 handoff coordinate

After this contract is independently confirmed, M42-WP7 MAY receive:

1. the exact Portfolio Identity citation;
2. the exact corresponding Accounting Scope citation;
3. the exact Ledger & Accounting-owned Portfolio Lifecycle State citation;
4. the already-captured Provenance associated with that cited state fact; and
5. for any other WP7-admissible source coordinate, that coordinate's
   already-captured Provenance and unchanged source-owner attribution.

Handoff completeness means that no cited semantic coordinate or
already-captured Provenance made available for carriage is omitted, inferred,
defaulted, replaced, repaired, enriched, or reassigned. It does not prescribe
a container, envelope, field, order, syntax, identifier, schema,
serialization, transport, runtime object, or persistence form.

### 9.2 Permitted downstream use

Under its own separately confirmed authority, M42-WP7 MAY:

- cite and carry the complete WP6 handoff;
- compose the cited Portfolio Lifecycle State beside other frozen or
  independently confirmed coordinates;
- preserve already-captured Provenance for each composed coordinate;
- preserve every coordinate's exact meaning and semantic owner; and
- define only the Portfolio Composition concerns independently admitted to
  WP7, without attributing them to WP6.

### 9.3 Prohibited authority transfer

The handoff grants WP7 no authority to:

- originate, alter, translate, normalize, default, infer, select, or validate
  a Portfolio Lifecycle State;
- define lifecycle transitions, lifecycle operations, transition legality,
  action eligibility, authorization, availability, or runtime currentness;
- capture, recapture, reconstruct, enrich, repair, combine, rank, score,
  adjudicate, reconcile, or provider-map Provenance;
- omit or replace available already-captured Provenance;
- detach Provenance from its source coordinate;
- treat Provenance as correctness, trust, legitimacy, authorization, or
  confidence;
- acquire Ledger & Accounting, Connectivity & Ingestion, or another source
  owner's authority;
- admit a rejected or unresolved coordinate; or
- attribute an implementation, runtime, persistence model, API, schema,
  serialization, audit mechanism, event-sourcing mechanism, reconciliation
  behavior, authorization rule, provider mapping, or executable validator to
  WP6.

The exact downstream boundary is:

> WP7 may cite and carry the exact subject-bound Portfolio Lifecycle State and
> each coordinate's already-captured Provenance, preserving association,
> meaning, and ownership, with no lifecycle execution, provenance capture,
> reinterpretation, or authority transfer.

---

## 10. Acceptance Criteria

This specification is acceptable only if Independent Review confirms all of
the following:

1. No new governed noun is admitted.
2. Portfolio Lifecycle State is reused exactly at its frozen canonical
   meaning and remains solely owned by Ledger & Accounting.
3. The only cited lifecycle-state values are exactly `active`, `archived`, and
   `closed`.
4. Every lifecycle-state citation binds explicitly to exactly one Portfolio
   Identity and its corresponding Accounting Scope.
5. Portfolio Identity and Accounting Scope are cited at their frozen M42-WP2
   meanings without redefinition or ownership transfer.
6. Permanent identity, corresponding Accounting Scope, ledger history, and
   evaluation history are preserved without adding transition, temporal,
   persistence, replay, or runtime semantics.
7. Portfolio Lifecycle State remains distinct from Portfolio Status, Current
   Selection, availability, permission, authority, action eligibility,
   degradation, runtime currentness, and transition legitimacy.
8. The phrase “qualifies what the portfolio may do next” is preserved by
   exact citation and is not elaborated into an eligibility, authorization,
   transition, workflow, or runtime rule.
9. No lifecycle execution, state machine, transition, transition legality,
   create, activate, archive, close, reopen, merge, split, clone, import,
   export, command, or workflow semantic is defined.
10. Provenance retains exactly its frozen generic meaning and Connectivity &
    Ingestion retains ownership of Provenance meaning and capture.
11. WP6 governs preservation and carriage of already-captured Provenance only;
    it defines no capture, recapture, reconstruction, generation, or
    completion-at-capture rule.
12. Every carried Provenance remains associated with the exact source
    coordinate to which it was attached.
13. No available already-captured Provenance is omitted, substituted,
    summarized as a replacement, normalized, enriched, repaired, translated,
    remapped, merged into obscurity, or reassigned during carriage.
14. WP6 manufactures no Provenance when an upstream source supplies none and
    makes no judgment about upstream conformance from that absence.
15. Provenance is never treated as proof of state correctness, currentness,
    transition legitimacy, authority, permission, availability, action
    eligibility, confidence, trust, or quality.
16. Portfolio Lifecycle State is never treated as a source, creator,
    validator, replacement, or interpretation of Provenance.
17. No provenance confidence, evidence class, provider mapping, source
    ranking, source adjudication, audit, event sourcing, reconciliation,
    deduplication, custody, or retention meaning is authored.
18. Each non-lifecycle coordinate carried toward WP7 retains its own confirmed
    meaning and source owner; the generic carriage rule does not admit,
    validate, or reinterpret that coordinate.
19. Ledger & Accounting does not acquire Provenance-capture ownership through
    lifecycle ownership.
20. Portfolio Intelligence does not acquire Portfolio Lifecycle State,
    Provenance-capture, or another source coordinate's ownership through
    Portfolio Composition.
21. WP7 receives the exact subject, lifecycle-state, Provenance, association,
    and owner-attribution coordinates without omission, defaulting, repair,
    enrichment, substitution, reinterpretation, or ownership transfer.
22. The positive golden vectors cover all three frozen lifecycle values,
    exact subject binding, history preservation, state/operation separation,
    exact Provenance carriage, no-capture behavior, other-coordinate carriage,
    distinct ownership, and the WP7 handoff.
23. The negative golden vectors cover subject ambiguity, value widening,
    vocabulary collision, history rewrite, lifecycle execution, transition
    and authorization leakage, provenance omission and laundering, capture,
    confidence, provider mapping, ownership transfer, downstream mutation,
    runtime inference, and implementation leakage.
24. Implementation, runtime, persistence, API, schema, serialization, audit,
    event-sourcing, reconciliation, provenance-capture,
    provenance-confidence, provider-mapping, authorization, and
    executable-validation authority remain `NONE`.
25. This contract modifies no frozen M34, M36, M42 Architecture, M42-WP1
    through M42-WP5, canonical Glossary, or domain-constitution statement.
26. Creation of this contract modifies no repository artifact outside this
    new M42-WP6 specification.

---

## Final Normative Boundary

M42-WP6 begins with one exact M42-WP2 subject, one exact Ledger &
Accounting-owned Portfolio Lifecycle State citation, and any Provenance
already captured for the cited coordinates. It ends by handing those same
semantic coordinates to M42-WP7 with their association, meanings, and owners
unchanged.

It owns no lifecycle state, Provenance, transition, or capture. It creates no
new noun, no implementation authority, no runtime authority, and no ownership
transfer.

## Final Status

**`COMPLETE — INDEPENDENT REVIEW APPROVED — NO CORRECTIONS REQUIRED`**
