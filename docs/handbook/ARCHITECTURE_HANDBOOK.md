# Architecture Handbook

> Status: `DRAFT`

This handbook explains how architecture is approached, documented, reviewed,
and preserved in this repository. It is explanatory repository documentation.
It creates no architectural authority, governance act, implementation
specification, design approval, or constitutional interpretation.

Architecture questions must be answered from the applicable canonical source.
This handbook provides a map for reading and reasoning about those sources; it
does not replace them or silently extend them.

## Contents

1. [Purpose](#1-purpose)
2. [Architectural philosophy](#2-architectural-philosophy)
3. [Architecture sources](#3-architecture-sources)
4. [Architecture lifecycle](#4-architecture-lifecycle)
5. [Architecture versus implementation](#5-architecture-versus-implementation)
6. [Architectural boundaries](#6-architectural-boundaries)
7. [Architectural reasoning](#7-architectural-reasoning)
8. [Architectural evolution](#8-architectural-evolution)
9. [Common architectural mistakes](#9-common-architectural-mistakes)
10. [Relationship to governance](#10-relationship-to-governance)
11. [Relationship to review](#11-relationship-to-review)
12. [Relationship to other handbooks](#12-relationship-to-other-handbooks)
13. [Related canonical sources](#13-related-canonical-sources)

## 1. Purpose

Architecture gives a repository a durable way to describe meaning, ownership,
boundaries, dependencies, and intended behavior before implementation details
make those decisions expensive to change. This handbook explains that
architectural practice for architecture authors, implementation authors, AI
assistants, reviewers, maintainers, and developers learning the repository.

It does not decide the architecture. It does not approve a design, authorize
implementation, amend a frozen artifact, allocate a work package, perform a
review, or create runtime authority. A real decision remains governed by the
canonical source and applicable record that actually states it.

The repository uses several architectural categories that must remain distinct:

| Category | Meaning | What it does not mean |
| --- | --- | --- |
| **Constitutional architectural constraint** | A constraint that an applicable canonical source expressly treats as binding for its corpus. | This handbook does not create, amend, or interpret the constraint. |
| **Approved architecture** | A design or architectural plan adopted, approved, or frozen by the applicable source or record. | Approval does not by itself authorize implementation or runtime operation. |
| **Implementation choice** | A concrete realization in code, schemas, configuration, tests, or supporting documents. | Current behavior does not automatically redefine architectural intent. |
| **Future design possibility** | A proposal, alternative, hypothesis, or direction under consideration. | A possibility is not a requirement, approval, allocation, or authorization. |

For operating rules, source tracing, scope control, frozen artifacts, and stop
conditions, consult [AI_RULES.md](AI_RULES.md). For authority, lifecycle acts,
and governance evidence, consult [GOVERNANCE_HANDBOOK.md](GOVERNANCE_HANDBOOK.md).
For review boundaries and findings, consult
[REVIEW_HANDBOOK.md](REVIEW_HANDBOOK.md).

Two distinct repository artifacts use the phrase "Architecture Handbook".
`docs/architecture/README.md` is itself titled "Architecture Handbook" and
belongs to the architecture corpus: it introduces and organizes that corpus.
This handbook under `docs/handbook/` is an explanatory handbook of a different
artifact class. It does not replace the architecture corpus, its README, or its
canonical architecture documents.

## 2. Architectural philosophy

The repository's architectural practice is based on a few connected ideas.
They explain why architecture is documented and how it can remain useful while
implementation changes. They are guidance, not a new set of constitutional
laws.

### Architecture before implementation

Architecture before implementation means deciding the important meaning of a
system before code makes the decision accidentally. The architectural question
is not only which module to create. It is also which concept exists, who owns
it, which boundary it crosses, what it may depend on, and what is deliberately
outside the design.

Writing those decisions first gives implementation a shape to realize and gives
reviewers something more precise than personal preference against which to
reason. It does not require every detail to be known before any code exists.
The appropriate level of architecture is the level needed to prevent an
important ambiguity from being decided invisibly in implementation.

### Bounded architecture

Good architecture says where its claims stop. A bounded design names its
subject, owners, interfaces, dependencies, assumptions, non-goals, and any
predecessors it relies on. It does not claim to solve adjacent domains merely
because they are nearby or interesting.

Boundedness makes a design reviewable. A reader can distinguish a deliberate
exclusion from an omission, and a later author can extend the system without
mistaking a local decision for a platform-wide rule.

### Incremental refinement

Architecture becomes more useful as a sequence of explicit refinements. A
high-level boundary can be refined into domains, interfaces, work packages, and
implementation plans without pretending that every later detail was already
decided. Each refinement should preserve the meaning and limits of the source
above it, or state clearly where a new source is required.

Incremental refinement is not permission to fill gaps with assumptions. An
unresolved question remains unresolved until an appropriate source or decision
addresses it.

### Explicit assumptions

Every design rests on assumptions: data shape, ownership, availability,
compatibility, failure behavior, or expected future change. Naming an
assumption makes it possible to test, revisit, or reject it. An unnamed
assumption tends to become an accidental requirement in code.

An assumption is not a fact merely because it appears in an architecture
document. Record whether it is observed evidence, a chosen premise, an
external dependency, or an open question.

### Deterministic reasoning

Architectural reasoning is more reliable when a reader can follow the inputs,
constraints, trade-offs, and resulting choice. Deterministic reasoning does not
mean every design problem has one mechanically correct answer. It means the
reason for a choice is explicit enough that another reader can reproduce the
path to it, challenge an assumption, and see what would change the result.

### Stable abstractions

An abstraction is stable when it captures meaning that should survive changes
at its edges. The repository's architecture documents use stable concepts such
as ownership, identity, accounting truth, interfaces, and dependency direction
to prevent provider formats, UI details, or temporary implementation structures
from becoming permanent domain meaning.

Stability is not the same as permanence. An abstraction can be changed by the
applicable architectural process when evidence shows that its boundary is
wrong. It should not be changed merely because a local implementation is
inconvenient.

### Implementation independence

Architecture should remain intelligible when a provider, framework, database,
module layout, or user interface is replaced. Implementation independence
protects the design from accidental coupling and lets several valid
implementations realize the same intent.

Independence does not mean implementation is unimportant. Implementation is
where the design meets actual constraints, and its behavior is evidence that
can reveal a missing assumption or an inadequate boundary. The response to
such evidence is explicit architectural reasoning, not silent drift.

## 3. Architecture sources

Architecture is distributed across source types. The source that answers a
question depends on the question being asked. [AI_RULES.md §2](AI_RULES.md#2-source-of-truth-hierarchy)
defines the repository's operating hierarchy for authority and governance
questions and explains why it is not a universal ranking of all technical
documents. Use that hierarchy rather than recreating it here.

The following table describes the practical role of common sources:

| Source | What it can tell an architecture reader | Boundary to preserve |
| --- | --- | --- |
| **Frozen architecture documents** | The exact architectural content, boundaries, ownership, and constraints fixed by the applicable source or freeze record. | Frozen bytes are read-only. A later design cannot silently rewrite, normalize, or replace them. |
| **Approved implementation plans** | The bounded work, sequencing, dependencies, deliverables, and verification intended for a package or milestone. | A plan is not implementation, and its existence does not grant authority beyond its stated record. |
| **Engineering principles** | Recurring code-structure and maintenance conventions such as reuse, single source of truth, ownership, compatibility, and observable failure. | Engineering guidance is not constitutional authority unless an applicable canonical source gives it that status. |
| **Repository decisions** | The reasoning, trade-offs, and context behind a chosen design or constraint. | A decision log is context and navigation unless the applicable source expressly gives a decision a different status. |
| **Implementation code and schemas** | What the system currently does, how responsibilities are realized, and where behavior may diverge from intended architecture. | Current behavior is evidence of implementation, not automatic approval to change architecture. |
| **Tests and verification results** | Observable evidence about behavior, compatibility, invariants, and claimed implementation properties. | A passing test does not by itself establish architectural authority or prove that the design is complete. |
| **Indexes and architecture READMEs** | Where relevant sources are located and how the document set is organized. | Navigation points to the source; it does not replace or extend the linked artifact. |

### Reading a source for the question it owns

Before relying on a document, state the question:

| Question | Start with |
| --- | --- |
| What architectural constraint applies? | The applicable canonical or frozen architecture source. |
| What design is intended for the system? | The applicable architecture document or approved architecture plan. |
| What is implemented today? | Code, schemas, configuration, and implementation documentation. |
| What is scheduled or bounded for a package? | The applicable implementation plan, roadmap, allocation, and authorization records. |
| Why was a design choice made? | The relevant decision record, then the source that establishes its current status. |
| What behavior is demonstrated? | Tests, verification output, and the implementation that was actually exercised. |
| Where is a source located? | The relevant README or index, followed by the linked canonical artifact. |

When sources appear to conflict, do not resolve the conflict by preference,
convenience, or a plausible future design. Preserve the higher source's stated
boundary, identify the conflict, and follow the stop and escalation rules in
[AI_RULES.md](AI_RULES.md) when the permitted action cannot be determined.

## 4. Architecture lifecycle

The repository often develops architecture through a sequence of bounded
activities. The sequence below is a useful explanatory model, not a mandatory
universal lifecycle. A governing corpus may omit an activity, combine records
when it explicitly permits that combination, or define additional acts.

```text
Planning
    -> Architecture definition
    -> Work-package decomposition
    -> Implementation planning
    -> Implementation
    -> Review
    -> Refinement when permitted
    -> Preservation of the resulting record and identity
```

The arrows describe relationships, not permission to perform the next act. In
ordinary repository work, allocation and lifecycle authorization are not
automatically required; [AI_RULES.md §3](AI_RULES.md#3-authority-before-action)
states when the ordinary-work and governed-lifecycle lanes differ. In governed
work, the applicable corpus and records determine the actual sequence, scope,
authority, and required evidence.

| Activity | Architectural question | Boundary |
| --- | --- | --- |
| **Planning** | What problem, scope, outcome, dependency, and exclusion are being considered? | Planning describes intent; it does not silently authorize implementation. |
| **Architecture definition** | What concepts, owners, interfaces, dependencies, assumptions, and non-goals give the system its shape? | A definition is bounded by its source and corpus; it does not decide unrelated domains. |
| **Work-package decomposition** | How can a bounded design be divided into coherent, reviewable pieces? | Decomposition clarifies responsibility and sequence; it is not permission to perform every piece. |
| **Implementation planning** | What candidate will be produced, in what order, with which dependencies and verification? | A plan is not the candidate and does not prove that implementation occurred. |
| **Implementation** | How will the intended structure be realized in code, schemas, configuration, or documentary artifacts? | Implementation must remain within the applicable architectural and authorized boundaries. |
| **Review** | Does the defined subject remain within its applicable architecture, sources, scope, and evidence? | Review records findings; it does not correct, confirm, freeze, release, or redesign the subject. |
| **Refinement** | What evidence or new requirement justifies a bounded change to the design? | Refinement must use the applicable source and preserve frozen content; inconvenience alone is not authority. |
| **Preservation** | Which source, identity, status, dependencies, and limitations must remain discoverable? | Preservation records and protects a state; it does not grant a successor or runtime authority. |

The lifecycle is easier to manage when each activity leaves an explicit trail:
the question asked, the sources consulted, the boundary used, the unresolved
assumptions, and the decision or disposition actually reached. The trail is
evidence of the activity, not a substitute for the authority required for a
later activity.

## 5. Architecture versus implementation

Architecture defines intent and structure. Implementation realizes that intent
under actual technical constraints. They inform one another, but they are not
the same artifact or the same kind of claim.

| Architecture | Implementation |
| --- | --- |
| Defines concepts, ownership, boundaries, interfaces, invariants, dependencies, and non-goals. | Provides code, schemas, configuration, migrations, services, tests, and operational behavior. |
| Answers what the system means and how responsibilities are divided. | Answers how the selected design works on the current technology and data. |
| Should survive replacement of local tools and edge components when its meaning remains valid. | May change frequently as compatibility, performance, and operational needs change. |
| Supplies constraints and intent for implementation review. | Supplies evidence of current behavior and may expose a missing architectural assumption. |
| May describe a target state or approved structure. | Describes a realized state, a candidate, or a proposed change depending on its source and status. |

Architecture is not source code. A document can mention implementation details
to clarify a contract, and an implementation document can record a current
state, but the reader should classify each claim by what it is asserting. A
code path that happens to work is not automatically the intended owner of a
responsibility. Conversely, an architecture statement that has never been
implemented is not evidence that the current system already behaves that way.

For example, an architecture may place provider-specific translation at an
outer boundary and keep core engines provider-independent. An implementation
then realizes that boundary with adapters, normalization, interfaces, and
tests. If provider names begin to leak into core business logic, the code is
evidence of architectural drift; it is not a reason to redefine the boundary
without an applicable architectural decision.

The same distinction applies to accounting and derived state. An architecture
may define a recorded ledger as the source from which holdings and metrics are
derived. An implementation can choose data structures and replay algorithms,
but a cached balance cannot silently become a second source of truth merely
because it is convenient to read.

## 6. Architectural boundaries

Boundaries make responsibilities visible. They reduce long-term complexity by
limiting the number of places that must change when an edge changes, and by
making invalid dependencies easier to detect.

| Boundary concern | Question to answer | Risk reduced |
| --- | --- | --- |
| **Bounded scope** | What subject, system area, corpus, and exclusions does this design cover? | Accidental platform-wide rules and uncontrolled work expansion. |
| **Interfaces** | What crosses the boundary, in what form, with what guarantees and failure behavior? | Hidden coupling and contracts that exist only in caller assumptions. |
| **Responsibilities** | What decision or behavior belongs here, and what belongs elsewhere? | Duplicated business rules and ambiguous ownership. |
| **Dependency direction** | Which component may depend on which other component, and in which direction does information flow? | Cycles, reverse ownership, and edge concerns leaking into stable core components. |
| **Ownership** | Which domain or component is the authoritative home for a concept or rule? | Multiple competing sources of truth. |
| **Assumptions** | What must be true for the design to work, and how will it be observed? | Unnoticed environmental or data dependencies. |
| **Non-goals** | What deliberately remains outside the design? | Future possibilities being mistaken for current commitments. |

A boundary is useful when it can be explained in terms of meaning rather than
directory layout alone. A module may move while ownership remains stable; two
modules may be combined while an interface contract remains essential. The
architectural boundary is the responsibility and contract, not the current
file tree by itself.

Dependency direction also carries information. A stable domain should not need
to know the names, formats, or incidental behavior of every external provider.
An edge translates external claims into the vocabulary owned by the domain.
This keeps change near the boundary where it belongs and protects the core from
edge churn.

## 7. Architectural reasoning

Architectural reasoning is a way of making design claims inspectable. The
repository does not require one universal design method or one preferred
pattern. The approaches below are complementary tools a competent author may
choose according to the question.

### Evidence-based reasoning

Start with what is known: applicable architecture sources, existing contracts,
current implementation behavior, tests, production constraints, and recorded
decisions. Separate observed evidence from interpretation and proposal. A
design that depends on a fact should either cite the fact or identify it as an
assumption to verify.

### Trade-off analysis

A design is a choice among consequences, not a list of preferred technologies.
Describe the alternatives that matter, the constraints that eliminate or favor
them, the costs accepted, and the conditions under which the choice should be
revisited. The purpose is not to produce a theatrical comparison of every
possible option; it is to make the consequential trade-offs visible.

### Compatibility reasoning

When a design changes, examine the readers, writers, callers, stored data,
external contracts, migration path, and historical records that depend on it.
Compatibility includes meaning, not only syntax. A change can preserve a type
signature while changing ownership or identity semantics.

### Dependency analysis

Trace both directions: what the proposed component needs and what other
components will come to rely on it. Identify cycles, hidden shared state,
provider leakage, duplicated rules, and assumptions that cross ownership
boundaries. The analysis should cover failure and degraded behavior, not only
the successful path.

### Explicit assumptions and uncertainty

Record uncertainty at the point where it affects the design. State what is
unknown, what evidence would resolve it, which alternatives remain open, and
what decision is intentionally deferred. Uncertainty is not a defect when the
design makes it visible and keeps the unresolved area bounded.

### A useful reasoning sequence

Different problems need different methods. When a lightweight sequence helps,
an author can:

1. name the architectural question and exact scope;
2. identify the source that owns the answer and the implementation evidence that
   may constrain it;
3. state boundaries, assumptions, non-goals, and relevant alternatives;
4. compare the consequences, compatibility, dependencies, and failure modes;
5. record the chosen direction, its rationale, and its unresolved questions; and
6. identify what would count as evidence that the design should be revisited.

This is a reasoning aid, not a replacement for the applicable source, review,
or governance process.

## 8. Architectural evolution

Architecture evolves because evidence, capabilities, and system boundaries
change. Safe evolution distinguishes what can move freely from what carries
established meaning or an explicit preservation requirement.

### What may evolve

Subject to the applicable source and scope, the following commonly evolve:

- implementation details, internal module structure, and technology choices;
- edge adapters, provider integrations, and input translations;
- explanatory documentation and navigation;
- implementation plans and sequencing;
- proposed extensions and future design possibilities; and
- architectural details that an applicable process has expressly opened for
  refinement.

### What must remain stable

The following remain stable when the applicable source treats them as stable:

- canonical meaning and ownership of a concept;
- public interfaces and invariants that other components depend on;
- dependency direction and explicit domain boundaries;
- identity and recorded-history semantics;
- the exact bytes and scope of a frozen artifact; and
- stated exclusions, non-goals, and limitations.

The handbook does not decide which of these categories applies to a particular
artifact. Read the source and applicable record that establish its status.

### Working with frozen architecture

A frozen architectural artifact is a read-only boundary. Read it, cite it,
compare implementation against it, and use its recorded identity. Do not edit,
normalize, reorder, or replace it because a different design would be easier.
Whether a particular path is actually frozen is determined by the repository
procedure in [AI_RULES.md §4 Frozen Artifact Rules](AI_RULES.md#4-frozen-artifact-rules);
follow that procedure rather than inferring frozen status from this handbook.
If the architecture genuinely needs to change, identify the applicable
amendment, successor, or other competent process before changing content.

This distinction matters because a successor design is not the same thing as a
rewritten predecessor. The predecessor remains evidence of what was decided;
the successor must state what it changes, why, and within which scope.

### Building on previous work

New architecture should read the sources above the point where it attaches to
the existing dependency chain. Reuse established vocabulary, preserve ownership
boundaries, identify compatibility obligations, and state where the new design
is additive rather than substitutive. Similar names or nearby files are not
enough to establish inheritance.

### Why redesign is exceptional

Redesign has a larger blast radius than local implementation change. It can
move ownership, invalidate interfaces, change identity semantics, or reopen
assumptions that downstream work has already relied on. That does not make
redesign forbidden. It means the case for it should be evidence-based,
explicitly scoped, compatibility-aware, and handled through the source-backed
process applicable to the affected architecture.

## 9. Common architectural mistakes

| Mistake | Why it causes harm | Better reasoning habit |
| --- | --- | --- |
| **Implementation-first thinking** | Code decides meaning, ownership, or dependency direction accidentally under delivery pressure. | Identify the architectural question and boundary before committing to local structure. |
| **Changing frozen architecture** | The historical identity and limits of a settled source become impossible to reconstruct. | Treat frozen content as read-only and use the applicable successor or amendment path. |
| **Mixing architecture and implementation** | A temporary tool or module layout is mistaken for a durable domain decision. | Separate intent, contracts, and ownership from the current realization. |
| **Inventing requirements** | Preferences or imagined future needs become obligations with no source. | Label proposals and assumptions; trace requirements to the source that establishes them. |
| **Expanding scope** | A local design silently becomes a platform redesign or takes over another owner's domain. | State scope and non-goals, and stop when a broader source-backed decision is needed. |
| **Assuming future authority** | A roadmap, plan, or promising design is treated as permission to implement or operate. | Keep future possibilities separate from approved architecture and authorization. |
| **Designing beyond authorization** | The candidate contains work that the applicable scope did not permit, making later review and identity ambiguous. | Design and implement only within the bounded authority that actually applies. |

These mistakes are not all constitutional violations. Their classification
depends on the applicable source, artifact class, and operating lane. A useful
architecture handbook names the risk without turning every warning into a
constitutional rule.

## 10. Relationship to governance

Architecture provides technical structure: concepts, ownership, interfaces,
dependencies, invariants, assumptions, and non-goals. Governance provides
authority and evidence: what act was permitted, what scope applied, what was
reviewed, what identity was validated, and what lifecycle disposition was
recorded.

Neither replaces the other:

| Architecture answers | Governance answers |
| --- | --- |
| What does this concept mean? | Was the relevant act permitted? |
| Which domain or component owns this responsibility? | Which role and scope were competent for the act? |
| What boundary and dependency direction should the design preserve? | What act occurred, with what evidence and non-effects? |
| What behavior or compatibility does the design intend? | What lifecycle state or disposition was actually recorded? |

An architecture document can be approved or frozen by a separate applicable
record, but the status comes from that source, not from the architecture
document's existence or from this handbook. Conversely, a governance record can
authorize a bounded implementation without deciding technical details that
belong to the architecture or implementation sources.

For the distinctions among planning, allocation, authorization, implementation,
review, confirmation, identity validation, freeze, release, and closeout, follow
[GOVERNANCE_HANDBOOK.md](GOVERNANCE_HANDBOOK.md). Do not infer an architectural
or implementation permission from a roadmap, a positive review, a Git commit,
or a handbook description.

## 11. Relationship to review

Architecture and implementation are reviewed for different claims, and
governance records are reviewed for different claims again. The applicable
review scope comes from the source and operating lane; this handbook does not
create a universal review gate.

| Review activity | Primary question | What it does not establish |
| --- | --- | --- |
| **Architectural review** | Does the defined architecture fit its applicable sources, boundaries, ownership, dependencies, assumptions, and non-goals? | It does not approve implementation, amend the architecture, or authorize runtime. |
| **Implementation review** | Does the candidate or implementation realize the permitted architecture and stay within its scope? | It does not become architecture, confirmation, freeze, release, or closeout. |
| **Governance review** | Does a governance record state its act, scope, competence, evidence, disposition, and non-effects accurately? | It does not redesign the technical system or supply missing authority by inference. |
| **Independent confirmation** | Is the subject in the bounded state that the applicable record says it is in? | It is a distinct act from substantive review and does not silently re-adjudicate the review. |

An architectural reviewer may use implementation and tests as evidence, but
should not mistake current behavior for intended design. An implementation
reviewer may identify an architectural mismatch, but the correction remains a
separate act. A governance reviewer may identify that an architecture record
was not authorized or preserved, but does not solve the technical design in the
governance record.

The detailed review methodology, finding discipline, focused re-review, and
confirmation boundaries are in [REVIEW_HANDBOOK.md](REVIEW_HANDBOOK.md). A
review records findings within its scope; it does not acquire a neighboring
role merely because a next architectural step appears obvious.

## 12. Relationship to other handbooks

The handbooks are complementary. They should link to canonical sources rather
than duplicate constitutional text, engineering rules, or governance evidence.

| Document | Relationship to this handbook |
| --- | --- |
| [AI_RULES.md](AI_RULES.md) | Operating rules for source tracing, ordinary-work and governed-lifecycle lanes, authority before action, frozen artifacts, evidence, identity, stop conditions, and reporting. |
| [GOVERNANCE_HANDBOOK.md](GOVERNANCE_HANDBOOK.md) | Governance lifecycle, authority boundaries, evidence model, and corpus-bound constitutional interpretation. |
| [REVIEW_HANDBOOK.md](REVIEW_HANDBOOK.md) | Review boundaries, architectural and implementation review practice, findings, focused re-review, and confirmation guidance. |
| [AI_COLLABORATION_GUIDE.md](AI_COLLABORATION_GUIDE.md) | Human-AI collaboration, handoffs, context preservation, and communication around repository work. |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | Contributor-facing repository conventions. It guides participation and does not replace canonical architecture or governance sources. |
| [Handbook entry point](README.md) | Overall handbook inventory, design philosophy, reading order, and boundaries. |

When two handbooks touch the same topic, consult the document that owns the
operating or governance rule. This handbook explains architectural reasoning;
it does not override the source that defines authority or the source that owns
the technical contract.

## 13. Related canonical sources

These links are navigation and source pointers. The linked artifacts retain
their own content, status, scope, identity, and limitations. This handbook does
not copy their laws or silently promote a navigation document into authority.

### Architecture sources

- [Architecture documentation README](../architecture/README.md) — navigation,
  reading order, document types, and the distinction between architecture,
  domain rules, and implementation.
- [Portfolio Intelligence Platform Architecture](../architecture/platform_architecture.md)
  — the source's own constitutional architecture, permanent boundaries, and
  laws for its identified corpus.
- [Architecture Specification](../architecture/ARCHITECTURE.md) — current
  system design, subsystem contracts, and implementation details as described
  by that artifact.
- [Platform Evolution](../architecture/PLATFORM_EVOLUTION.md) — long-term
  architectural direction and design philosophy.
- [Architecture Roadmap](../architecture/ROADMAP.md) — phase history, current
  sequence, and future work direction.

### Engineering and implementation context

- [Engineering Principles](../engineering/ENGINEERING_PRINCIPLES.md) — code
  structure, reuse, ownership, compatibility, and observable failure guidance.
- [Decision Log](../engineering/DECISION_LOG.md) — design rationale and
  repository decision context.
- [Implementation Index](../implementation/INDEX.md) — non-authoritative
  navigation to implementation documents and milestone records.
- [Repository Glossary](../GLOSSARY.md) — shared vocabulary.

Read the applicable canonical artifact for the question at hand. A source's
presence in this list does not make it applicable to every architecture,
implementation, or work package.

## Status

`DRAFT`
