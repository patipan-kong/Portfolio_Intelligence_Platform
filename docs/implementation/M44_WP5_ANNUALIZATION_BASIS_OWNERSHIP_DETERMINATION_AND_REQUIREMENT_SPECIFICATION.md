# M44-WP5 — Annualization Basis Ownership Determination and Requirement Specification

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics

**Work package:** M44-WP5 only

**Candidate:** `RC6.3` — owner-corpus boundary and RC6 review-chain
evidence-completion correction for `RC6.2-MAJOR-1` and `RC6.2-MAJOR-2`,
preserving the RC6.1 and RC6.2 evidence corrections recorded in §12.1

**Artifact class:** Architectural deliverable, in the sense frozen M44
Architecture §11 M44-WP5 uses under **Architectural deliverables**

**Artifact identity:** The single M44-WP5 determination and requirement
specification allocated by frozen M44 Architecture §11 and §13.1

**Ownership-determination and requirement-specification authority:** `LIMITED
TO THE FROZEN M44 ARCHITECTURE §8.4 AND §11 ALLOCATION`

**Ownership proposed by this RC6.3 candidate:** `MARKET INTELLIGENCE — NOT
EFFECTIVE BEFORE §13 COMPLETES`

**G-3 disposition authority:** `NONE`

**G-4 terminal state proposed by this RC6.3 candidate:** `OPEN — NOT EFFECTIVE
BEFORE §13 COMPLETES`

**§12.1.1 checkpoint disposition authority:** `NONE`

**M44-WP6 authorization:** `NONE`

**M44-WP7 authorization:** `NONE`

**Implementation authority:** `NONE`

**Runtime authority:** `NONE`

**Source-code authority:** `NONE`

**Persistence authority:** `NONE`

**Schema and migration authority:** `NONE`

**API and transport authority:** `NONE`

**UI and presentation authority:** `NONE`

**Provider authority:** `NONE`

**Production-method authority:** `NONE`

**Executable-validation authority:** `NONE`

**Contract-authoring, registration, extension, versioning, and serialization
authority:** `NONE`

**Vocabulary-admission authority:** `NONE`

**Frozen-artifact-amendment authority:** `NONE`

**Capability-completion authority:** `NONE`

---

## 1. Purpose

This document is the sole M44-WP5 architectural deliverable allocated at:

`docs/implementation/M44_WP5_ANNUALIZATION_BASIS_OWNERSHIP_DETERMINATION_AND_REQUIREMENT_SPECIFICATION.md`

It defines the constitutional process by which the M44-WP5 determination
contained in this same deliverable must attempt to prove the owner of the
Annualization Basis. It defines:

- the evidence that may and may not participate in the determination;
- the required order of analysis;
- the proof standard;
- the conditions that stop the determination;
- the conditions that make a proposed determination fail;
- the repository evidence that must support a proposed determination; and
- the constitutional outputs required before any proposed determination may
  become effective.

This corrected RC6.3 candidate applies that process through frozen WP5.5 in the
integrated determination record at §12.1. It proposes Market Intelligence as
the proved owner, records the exhaustive search of that proved owner's frozen
corpus, and proposes `G-4 OPEN` because no conforming exact existing governed
Annualization Basis contract kind is present. Those are candidate conclusions
only. They have no constitutional effect unless and until §13 completes. No
separate WP5 determination, requirement-specification, or
constitutional-process artifact is permitted.

The governing posture is determination-only and fail-closed. Consumption of an
Annualization Basis by Portfolio Analytics does not transfer ownership to
Portfolio Intelligence. Similarity to a calendar, market session count,
provider field, configuration value, library facility, or current repository
implementation does not prove ownership.

## 2. Authority and constitutional basis

Normative-authoring authority originates only from the frozen
[M44 Architecture and Implementation
Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md):

- §1.5 grants, after architecture confirmation, authority to author the
  documentary governance, contract, and normative-specification artifacts
  enumerated in §11, in `docs/` only;
- §8.4 grants determination and requirement-specification authority only and
  fixes `docs/implementation/` as the expected location;
- §11 allocates this single M44-WP5 determination and requirement
  specification and fixes its authority ceiling; and
- §13.1 fixes this exact path.

That grant is confirmed by [M44 Architecture Freeze Record
§3.1](M44_ARCHITECTURE_FREEZE_RECORD.md), which grants "[a]uthority to author
the documentary governance, contract, and normative-specification artifacts
enumerated in frozen RC2 §11, in `docs/` only, after each passes its own
independent review and confirmation chain." The final clause is part of the
grant, not a gloss on it; it is carried into §13 of this specification and is
not satisfied by this candidate. The planning freeze, planning closeout,
Decision Log, this candidate, and any author instruction grant no additional
authority.

This specification is also bounded by, and must be read with:

- the frozen [M44 Architecture and Implementation
  Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md),
  especially §§3.1, 4.4, 5–6, 8.4, 10, 11 M44-WP5, 12.1.1, 12.3, 12.5,
  13.1, 16.2, and 17 OQ-3;
- the frozen [M44 Architecture Freeze
  Record](M44_ARCHITECTURE_FREEZE_RECORD.md);
- the frozen [M44-WP1 Inherited Gate Inventory and Closure
  Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
  §4.4;
- the frozen [Platform
  Architecture](../architecture/platform_architecture.md) §§6.2 and 6.5;
- frozen [M43-WP2 Portfolio Measure Definition, Method Version, and
  Applicability Contract
  Specification](M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md)
  §§8.1–8.2;
- frozen [M43-WP4 Constitutional Scope and Implementation
  Plan](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md)
  §§5.2 and 6.7; and
- the frozen, non-normative [M44-WP5 Architecture and Implementation
  Plan](M44_WP5_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md), as a planning
  constraint baseline and never as the source of normative-authoring
  authority.

The M44-WP5 planning-governance corpus is exactly the set enumerated in
[M44-WP5 Planning Freeze Record](M44_WP5_PLANNING_FREEZE_RECORD.md) §1, which
records that corpus `COMPLETE AND FROZEN` at planning candidate `RC3`. It
supplies architectural intent and constraints. It remains non-normative and
immutable. This specification does not convert any planning statement into an
ownership result and does not amend or reinterpret any frozen statement.

The authority exercised here is limited to ownership determination and
requirement specification within the frozen allocation. This RC6.3 candidate
performs the pre-confirmation determination recorded at §12.1 but does not
confirm, freeze, or make it effective. The allocation is not authority to
author an owner-domain governance instrument, disposition the §12.1.1
checkpoint, or authorize downstream work.

### 2.1 Extension basis

Frozen M44 Architecture §5.3 requires that "every M44 artifact must name which
basis it relies on and quote the frozen sentence that supplies it." Frozen
`INV-C2` states the same duty: "Every M44 addition rests on exactly one of the
extension bases E-1, E-2, or E-3 in §5.3, names which one, and quotes the exact
frozen sentence that supplies it. No addition is justified by unstated silence."
Frozen §14 makes it falsifiable as "an extension-basis check confirming every
M44 addition names E-1, E-2, or E-3 and quotes its frozen sentence." Following
the pattern of frozen [M44-WP2 §1.3](M44_WP2_M43_ARCHITECTURE_CONFIRMATION_RECORD.md),
this deliverable rests on exactly one basis:

> **E-3 — Addition into declared silence, under constitution G3.** Residual and
> subordinate to E-1 and E-2. "It supports supplying a repository-local record
> where a frozen governance chain required one and none was written (G-1), and
> supplying a superseding ruling that names a defective frozen row (G-2)."

The declared silence is ownership. Frozen M43-WP4 §6.7 requires the owner of
the annualization basis to be proved and names no owner. Frozen M44
Architecture §17 OQ-3 records the ownership question as open. Frozen M44-WP1
§4.4 records that "[n]o annualization-basis governance instrument exists at any
path in the repository." This deliverable adds the determination and
requirement-specification process into that silence, and adds nothing else.

The quoted `E-3` sentence names `G-1` and `G-2` and does not name `G-4`. Whether
that sentence enumerates `E-3`'s only supported cases or illustrates a residual
basis stated by its own defining clause is a question the frozen text does not
settle, and this specification does not settle it either. Both readings are
recorded; neither is ranked, and neither is used to widen or narrow `E-3`. Under
the enumerative reading no frozen basis is named for this deliverable, which
would be a defect in the frozen corpus and not a matter this specification may
cure. The route for a defect in frozen architecture is fixed by frozen M44
Architecture Freeze Record §9 — "[a] defect in it is corrected only by a new
independently confirmed architecture revision that names the defect
(constitution G5), never by editing it in place" — and by frozen M44
Architecture §1.6 rule 3. Citing that route here is not exercising it: this
deliverable does not initiate, request, authorize, draft, or prescribe any
revision, and names no defect on the architecture's behalf. This citation is
authoring-time and is not the branch-conditioned §10.1 route, which opens only
where the evidence establishes that the §4 ownership ambiguity prevented the
determination; §4's preserved ambiguity is not enlarged by this paragraph.
Under the residual reading, `E-3` is the basis named above. This declaration is
made so that no addition rests on unstated silence under either reading.

**`E-1` is inapplicable.** `E-1` requires a frozen contract that "states the
conditions under which the extension is conforming" and "that its own silence
on the mechanism does not extinguish the obligation." No frozen contract states
conditions of conformance for an annualization-basis ownership determination,
and this deliverable adds no coordinate, field, form, or state to any frozen
contract.

**`E-2` is inapplicable.** `E-2` requires "[a] remedy the frozen corpus names
but does not supply," where a frozen artifact "identifies the instrument
required to discharge an obligation and declines to produce it." The instrument
frozen M43-WP4 §6.7 names and declines to produce is the separately authorized
owner-domain governance instrument recorded as deferred obligation `D-7`. This
deliverable is not that instrument, may never become it, and is forbidden by §14
from authoring it.

This deliverable extends no frozen contract and reaches into no other domain's
corpus (`INV-C4`). No addition is justified by unstated silence.

Frozen §5.3's opening clause states the naming duty for extending "a frozen
contract," while `INV-C2` and the frozen §14 check state it for "every M44
addition." Those two frozen statements differ in reach, and this specification
ranks neither. This section is written to satisfy the wider reading, and is
sufficient under the narrower one. No precedence is created; no provision is
waived, narrowed, or generalized.

### 2.2 Review-chain provenance

Frozen M44 Architecture §12.4 fixes the lifecycle as "independent
constitutional review → required-corrections response if findings exist →
independent confirmation → freeze," and frozen §13.1 allocates
"[p]er-work-package independent review, corrections-response, and confirmation
artifacts" to the review chain. A claim of corrected status is inspectable only
from filed records. The state of that chain for this deliverable is:

- the `RC1` independent constitutional review of this deliverable is filed at
  [M44_WP5_RC1_INDEPENDENT_CONSTITUTIONAL_REVIEW.md](M44_WP5_RC1_INDEPENDENT_CONSTITUTIONAL_REVIEW.md),
  determination `NOT APPROVED`;
- the disposition of every `RC1` finding is filed at
  [M44_WP5_RC1_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md](M44_WP5_RC1_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md);
- the `RC2` independent constitutional review of this deliverable is filed at
  [M44_WP5_RC2_INDEPENDENT_CONSTITUTIONAL_REVIEW.md](M44_WP5_RC2_INDEPENDENT_CONSTITUTIONAL_REVIEW.md),
  determination `NOT APPROVED`, and the `RC3` candidate corrected that review's
  findings. That record discloses at its §3.1 that the original `RC2` narrative
  was not preserved and that its per-finding rationale is a disclosed
  reconstruction; that limit is a property of the filed record and is neither
  cured nor enlarged here;
- the disposition of every `RC2` finding is filed at
  [M44_WP5_RC2_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md](M44_WP5_RC2_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md),
  added at commit `e02a50bfe929c3a2ccfbce8455f47d812595ba67`. That record
  discloses that it inherits the `RC2` review record's reconstruction limit;
- the `RC3` independent constitutional review of this deliverable is filed at
  [M44_WP5_RC3_INDEPENDENT_CONSTITUTIONAL_REVIEW.md](M44_WP5_RC3_INDEPENDENT_CONSTITUTIONAL_REVIEW.md),
  added at commit `6cb7e1a461d70e9cc7c7a762640f5585e3248777`, determination
  `NOT APPROVED`, and the `RC4` candidate corrected that review's findings;
- the disposition of every `RC3` finding is filed at
  [M44_WP5_RC3_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md](M44_WP5_RC3_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md),
  added at the same commit `e02a50bfe929c3a2ccfbce8455f47d812595ba67`. That
  record claims no independent validation and records six of the nine `RC3`
  findings `ADDRESSED — REQUIRES RE-VALIDATION`;
- the `RC4` independent constitutional review of the `RC4` candidate is filed at
  [M44_WP5_RC4_INDEPENDENT_CONSTITUTIONAL_REVIEW.md](M44_WP5_RC4_INDEPENDENT_CONSTITUTIONAL_REVIEW.md),
  added at commit `5c4e587c43c931791e69aca403c70873d1a27d86`, determination
  `NOT APPROVED`, on three active findings — one `CRITICAL`, one `MAJOR`, one
  `MINOR`, none `EDITORIAL`. That record discloses at its §3.1 and §11 that the
  original `RC4` narrative was not preserved, that its per-finding rationale is
  a disclosed reconstruction, and that the filing act was not
  author-independent; those limits are properties of the filed record and are
  neither cured nor enlarged here. The record states at its §9 that the
  specification is "NOT READY" for Independent Constitutional Confirmation, and
  this candidate does not disturb that statement;
- the disposition of every `RC4` finding is filed at
  [M44_WP5_RC4_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md](M44_WP5_RC4_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md),
  added at commit `f32c33ba2ec694327f6014d08b3d8d4d8e8df565`. That record
  records all three `RC4` findings `ADDRESSED — REQUIRES RE-VALIDATION`, none
  `RESOLVED` and none `INTENTIONALLY UNCHANGED`, claims no independent
  validation, and states that it discharges no finding;
- the `RC5` candidate is the correction of the `RC4` review's findings;
- the `RC5` independent constitutional review is repository-filed at
  [M44_WP5_RC5_INDEPENDENT_CONSTITUTIONAL_REVIEW.md](M44_WP5_RC5_INDEPENDENT_CONSTITUTIONAL_REVIEW.md),
  determination `NOT APPROVED`. It independently records
  `RC4-CRITICAL-1`, `RC4-MAJOR-1`, and `RC3-MINOR-4` as `RESOLVED` and raises
  `RC5-CRITICAL-1` and `RC5-MAJOR-1`;
- the `RC5` constitutional corrections response is repository-filed at
  [M44_WP5_RC5_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md](M44_WP5_RC5_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md).
  It accepts `RC5-CRITICAL-1` for correction and records that the separate
  constitutional challenge concluded that no exact frozen authority requires
  explicit §8.1 → §10.1 routing and recommended treating `RC5-MAJOR-1` as
  non-blocking architectural guidance. That author response is not independent
  validation, creates no lifecycle stage, and does not itself amend or
  disposition frozen authority;
- the `RC6` candidate corrected accepted `RC5-CRITICAL-1` by incorporating the
  applied determination through frozen WP5.5 into this sole deliverable and
  made no normative change for `RC5-MAJOR-1`;
- the `RC6` independent constitutional review is repository-filed at
  [M44_WP5_RC6_INDEPENDENT_CONSTITUTIONAL_REVIEW.md](M44_WP5_RC6_INDEPENDENT_CONSTITUTIONAL_REVIEW.md),
  blob `a828170ed3ab4e68015ddc9ffa98f91e613a0330`. It reviewed the
  uncommitted RC6 working-tree blob
  `b10d755805f827a47ab3e337017279ad4f0af6c4` over base commit
  `052358fb7b93985b34a4c9a156d5fc92b4293e60`, returned `NOT APPROVED`,
  recorded `RC5-CRITICAL-1` as resolved as to the identified method-only
  defect, and raised `RC6-CRITICAL-1` and `RC6-MAJOR-1`;
- the `RC6` formal constitutional corrections response is repository-filed at
  [M44_WP5_RC6_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md](M44_WP5_RC6_FORMAL_CONSTITUTIONAL_CORRECTIONS_RESPONSE.md),
  blob `36dce6ce0c45b06e35182e256396c57460a8a1f2`. It records both
  `RC6-CRITICAL-1` and `RC6-MAJOR-1` as `ACCEPTED FOR CORRECTION` and
  `NOT DISCHARGED`. It grants no approval, confirmation, freeze, lifecycle,
  implementation, or downstream authority; the response does not
  constitutionally discharge either finding, and both remain subject to later
  author-independent whole-record re-validation;
- the `RC6.1` candidate completed the repository review-chain account and the
  initially identified M41 proved-owner corpus evidence for
  `RC6-CRITICAL-1` and `RC6-MAJOR-1`;
- the `RC6.2` candidate completed the additional M40 owner-corpus evidence for
  `RC6-MAJOR-1` by inspecting and recording M40-WP2 and M40-WP3. It does not
  reopen the ownership method, lifecycle, review chain, or `RC5-MAJOR-1`;
- this `RC6.3` candidate completes the M39–M41 corpus-boundary proof and the
  RC6 review-chain account without changing any review disposition or
  conferring lifecycle authority; and
- no independent constitutional review of this `RC6.3` candidate is filed at any
  repository path, and no independent constitutional confirmation of this
  deliverable is filed at any repository path.

The bullets above state the repository state of the review chain and nothing
further. They record no approval, no completion of review, and no confirmation
readiness. Because no independent review of this candidate and no independent
confirmation are filed, the review chain for this deliverable MUST NOT be
treated as complete, and this candidate MUST NOT be treated as approved,
reviewed to conclusion, independently confirmed, or frozen. A claim of
corrected status made by this candidate about itself is an author statement
under §6.1 and is not lifecycle evidence.

Those records are review-chain governance records under frozen §13.1. They are
not WP5 determination, requirement-specification, or constitutional-process
artifacts, and §1 and §12 continue to permit no additional artifact of those
classes. Filing a review-chain record grants no authority and dispositions
nothing; a filed review is lifecycle evidence only, under §6.1.

## 3. Normative language and process-local terms

`MUST`, `MUST NOT`, `REQUIRED`, `SHALL`, `SHALL NOT`, and `MAY` are normative
within the determination and requirement-specification scope of this
deliverable.

The following terms are process-local descriptions only. They do not create
governed business vocabulary, terminal states, contract kinds, identifiers, or
repository artifact classes:

- **determination record:** the applied determination sections incorporated
  into this same sole deliverable;
- **evidence manifest:** the cited inventory of evidence evaluated by that
  record;
- **candidate owner:** a hypothesis under evaluation, never an assignment;
- **proved owner:** an owner supported by the complete proof required in §7
  and made effective only through §13;
- **corpus boundary:** the exact, frozen repository scope attributed to a
  proved owner and eligible for the search in §8; and
- **assessment:** a documentary conclusion that has no admission,
  registration, runtime, or implementation effect.

These descriptions MUST NOT be emitted as governed status tokens or used to
extend the closed terminal-state vocabulary in frozen M44 Architecture §16.2.

## 4. Preserved frozen ownership ambiguity

The frozen corpus contains a constitutional tension that this specification
does not resolve:

- M44 Architecture §§3.1, 4.4, 10, 11 M44-WP5, and 16.2 require a conforming
  `G-4 OPEN` record to name both the exact missing element and its exact owner.
- M44 Architecture §17 OQ-3(c) contemplates no admissible owner and `G-4 OPEN`
  with the ownership question itself unresolved.

No precedence between those provisions is created here. No provision is
waived, ranked, narrowed, or generalized. No substitute or placeholder owner
may be supplied.

If the process cannot prove an owner, M44-WP5 cannot form a terminal `G-4`
record without deciding constitutional meaning outside its authority.
Accordingly, the process MUST stop under §10.1. It MUST NOT characterize that
stop as `G-4 OPEN`, `G-4 CLOSED`, a variant of `OPEN`, or a third terminal
state.

The frozen corpus states two things about the §12.1.1 checkpoint on that branch
that do not sit together, and this specification ranks neither. Frozen M44
Architecture §12.1.1 opens "After M44-WP4 and M44-WP5 are confirmed and before
M44-WP6 begins," which on its own terms is not reached by an M44-WP5 that has
not completed, confirmed, or frozen. Frozen M44-WP5 plan §3, §5 `WP5.2` exit,
and §5.1 characterize ownership-proof failure as stopping "under §12.1.1's third
outcome." Both are frozen text. §10.1 carries both citations and the
consequences that hold under either reading. The frozen checkpoint's
unestablished-state row remains a governing constraint on any future checkpoint
evaluation; nothing here is a checkpoint disposition performed by this
specification.

A defect in the attempted M44-WP5 determination and an ambiguity in frozen
architecture are distinct constitutional matters. A determination record MUST
identify each precisely and MUST NOT silently convert one into the other. This
specification creates no remedy or amendment authority for either, and documents
the frozen correction route in §10.1 without exercising it.

## 5. Determination invariants

Every application of this specification MUST preserve all of the following:

1. Ownership is proved before an owner-domain corpus is selected or searched.
2. Ownership proof is independent of contract availability.
3. Contract availability is independent of current implementation practice.
4. An unresolved, ambiguous, or conflicting owner is blocking and never an
   implicit assignment.
5. All four frozen M43-WP4 §6.7 propositions are conjunctive; partial proof is
   failure.
6. No owner is selected by convention, convenience, proximity, repository
   location, provider behavior, or consumer need.
7. No authority is transferred into or out of Portfolio Intelligence, Market
   Intelligence, or any other domain by the determination process.
8. Source calendar meaning is not transferred out of Market Intelligence.
9. The process creates no dependency, contract kind, identifier, version,
   canonical value bytes, annualization factor, calendar, default, or
   serialization.
10. Every missing, ambiguous, conflicting, inaccessible, or unbounded
    evidentiary condition fails closed. M44 has no freshness concept: evidence
    is exact and manifest-bound or absent.
11. A requirement statement is never treated as an existing owner-domain
    governance instrument.
12. No result becomes effective without the independent constitutional
    lifecycle in §13.

## 6. Evidence rules

### 6.1 Admissible evidence

Evidence is admissible only when its authority, identity, scope, and frozen
state can be established by exact repository citation. Admissible evidence is
limited to:

1. **Frozen constitutional allocations.** Exact text from frozen Platform
   Architecture laws, frozen ADRs, frozen milestone architecture, and frozen
   owner-domain governance artifacts that expressly allocate the relevant
   semantic concern.
2. **Confirmed constitutional determinations.** A repository-filed,
   independently confirmed determination that expressly addresses the
   relevant ownership proposition and has not been superseded or amended.
3. **Exact owner-domain publications.** For the availability stage only, an
   artifact already published in the proved owner's frozen corpus, with exact
   path, section, identifier, immutable version, and owner attribution.
4. **Canonical-value evidence.** Canonical value bytes only where the proved
   owner already publishes them under the exact governed contract being
   assessed. Bytes constructed, inferred, normalized, or serialized by M44 are
   inadmissible.
5. **Repository identity evidence.** Commit identifiers, blob identifiers,
   exact paths, and clean-diff evidence used to prove which text was examined
   and that frozen artifacts were not modified.
6. **Exhaustive absence evidence.** A reproducible inventory of a proved
   owner's exact frozen corpus, including the declared boundary, search method,
   search terms, inspected paths, exclusions, and evidence that the boundary
   is complete. Absence from an undefined or incomplete corpus is not
   admissible absence evidence.

An evidence item MUST be assessed at its frozen meaning. Citation does not make
an artifact relevant; the cited text must state the proposition for which it
is offered.

Review and confirmation are lifecycle evidence produced only after a
reviewable candidate reaches WP5.6. They are not ownership evidence and are
not prerequisites for constitutional reviewability.

### 6.2 Inadmissible evidence

The following MUST NOT prove or contribute weight toward ownership:

- the M44-WP5 planning documents by themselves;
- M44 Architecture §17 OQ-3's recommended hypothesis by itself;
- the mere existence of M39, M40, M41, or another domain corpus;
- a module name, directory, type name, field name, database shape, API,
  serializer, provider adapter, test, fixture, or current runtime behavior;
- current source-code placement or historical implementation practice;
- a provider response, vendor convention, market convention, common industry
  practice, or live external service;
- the fact that Portfolio Analytics consumes or needs the Annualization Basis;
- calendar-like semantics, session-count semantics, or conceptual similarity
  to an already owned noun;
- an unstated, ambient, implicit, caller-supplied, or unversioned `252`, `365`,
  `365.25`, or other value;
- a range, alias, “latest” selector, mutable reference, compatible-version
  fallback, or transitive-only reference;
- a requirement statement, proposed contract, artificial contract kind,
  M44-authored kind, placeholder, example, or illustrative fixture;
- an illustrative item marked artificial or non-effective, regardless of its
  additional documentary labels;
- silence in a frozen artifact;
- absence from an unbounded, incomplete, inaccessible, or presumptive corpus;
- an unstated precedence rule, inferred hierarchy, majority of citations,
  recency, or author preference;
- `G-3`, `G-5`, §12.1.1, WP6, WP7, D-2b, D-3, or D-7 status as proof of
  ownership; or
- a prior candidate, review opinion, or unconfirmed conclusion treated as an
  effective determination.

No gate status is admissible as evidence of Annualization Basis availability.
In particular, frozen `G-3 OPEN — PARTIAL` MUST NOT be treated as evidence
that an Annualization Basis is available. This preserves frozen M44-WP5 plan
§4.2.

Inadmissible evidence MUST be recorded as rejected when materially presented.
It MUST NOT be repaired, normalized, or converted into admissible evidence.

## 7. Ownership proof standard

A proposed owner may be proved only when the determination record establishes
all four frozen M43-WP4 §6.7 propositions:

1. why `VERSIONED_CALCULATION_DEPENDENCY` is constitutionally correct;
2. why `GOVERNED_EVIDENCE` is constitutionally incorrect for the
   Annualization Basis;
3. why caller override is constitutionally rejected; and
4. why the proposed owner and placement do not expand Portfolio Intelligence
   authority or transfer ownership of source calendar meaning out of Market
   Intelligence.

In addition, the record MUST:

- cite the exact frozen authority that allocates the relevant meaning to the
  proposed owner;
- show that the proposed placement does not create shared, inferred, or
  consumer ownership;
- identify and reject every materially plausible alternative using admissible
  evidence;
- show that no relied-upon statement requires a new precedence rule or
  reinterpretation;
- distinguish ownership of source calendar meaning from ownership of the
  versioned calculation dependency; and
- show that two independent readers applying the cited rules to the same
  frozen evidence would reach the same ownership conclusion, as required by
  frozen M44 Architecture `INV-D2`: "Two independent readers applying an M44
  normative rule to the same inputs reach the same result, including the same
  rounding, ordering, and tie-break outcome." No dependency-closure
  rule is relied on at this stage; ownership proof is independent of contract
  availability (§5 invariant 2).

The proof is conjunctive. A missing, circular, ambiguous, conflicting, or
inference-dependent proposition means that ownership is not proved. Strength
in one proposition cannot compensate for failure in another.

No owner name is supplied in advance by the determination method. Market
Intelligence MUST be treated only as the first hypothesis required by frozen
OQ-3; it MUST be proved or rejected under the same standard as any other
materially supported hypothesis.

## 8. Ordered determination workflow

The workflow is strictly sequential.

The specification sections correspond to the frozen planning stages as
follows. This mapping preserves the frozen sequence and creates no new work
package or stage:

| Specification section | Frozen stage | Constitutional correspondence |
| --- | --- | --- |
| §8.1 | WP5.1 | Authority intake and boundary lock |
| §§8.2–8.3 | WP5.1 outputs | Evidence manifest and hypothesis record |
| §8.4 | WP5.2 | Ownership proof |
| §§8.5–8.6 | WP5.3–WP5.4 | Proved-owner corpus inventory and existing-contract assessment, together with every test frozen WP5.4 assigns — "[a]pply M43-WP2 §8.2 closure; test the distinct M43-WP4 §6.7 information, caller-override rejection, and version non-substitutability" |
| §8.7 | WP5.4–WP5.5 | Terminal-state proposal, and the requirement and consequence record |
| §13 | WP5.6 | Independent governance lifecycle, only after WP5.5 completes |

### 8.1 Boundary lock

Before evaluating any owner hypothesis, the determination record MUST:

- identify this specification and the frozen authorities in §2;
- record the repository commit under examination;
- record exact blob identifiers for every controlling frozen artifact;
- verify that no frozen artifact has been modified;
- declare every authority ceiling carried in this specification;
- state that ownership, `G-4`, `G-3`, and §12.1.1 are not already determined
  or dispositioned by the record; and
- record the exclusions in §12.

Failure to establish the boundary lock stops the process.

### 8.2 Evidence manifest

The record MUST enumerate every evidence item with:

- exact repository path and section;
- commit and blob identity;
- frozen or confirmed status;
- asserted proposition;
- constitutional owner of the cited statement;
- admissibility result under §6; and
- rejection reason for every material inadmissible item.

The manifest MUST distinguish evidence supporting ownership from evidence
reserved for the later availability assessment.

### 8.3 Hypothesis record

The record MUST list only hypotheses having an admissible constitutional basis.
Recording a hypothesis is not proof. Market Intelligence MUST be tested first,
as required by frozen OQ-3, but that order gives it no presumption, priority, or
precedence.

An unsupported candidate MUST be rejected; it MUST NOT be retained merely to
make the candidate set appear exhaustive.

### 8.4 Ownership proof

Each supported hypothesis MUST be evaluated against §7. The record MUST expose
the complete reasoning chain and exact citations. It MUST NOT use corpus
availability, a desired downstream outcome, or implementation convenience to
break an ownership tie.

The only permitted exit from this stage is:

- one owner proved under every requirement of §7; or
- ownership not proved, followed immediately by the stop in §10.1.

### 8.5 Owner-corpus boundary

This stage MUST NOT begin unless §8.4 proves one owner.

The determination record MUST then define the exact frozen corpus controlled
by that owner. The boundary MUST be reproducible and MUST distinguish:

- owner-authored governed contracts;
- artifacts merely consumed, referenced, mirrored, or implemented by the
  owner;
- superseded or non-frozen material;
- examples and fixtures; and
- repository surfaces not governed by that owner.

If the exact frozen corpus cannot be established and exhaustively inspected,
the process stops under §10.2.

### 8.6 Existing-contract assessment

Only the proved owner's bounded frozen corpus may be searched for an exact
existing governed contract kind.

The assessment MUST keep these requirements separate:

1. Frozen M43-WP2 §8.1 declaration fields:
   - Dependency key;
   - Owning domain;
   - Dependency contract kind;
   - Dependency identifier; and
   - Dependency version.
2. Frozen M43-WP2 §8.2 transitive closure, including §8.2(6): "two independent
   traversals produce the same set of exact dependency tuples."
3. Frozen M43-WP4 §6.7 owner-published information:
   - exact owner;
   - existing governed contract kind;
   - identifier;
   - immutable version; and
   - canonical value bytes.
4. Caller-override rejection. An apparent existing owner-published governed
   contract kind that permits a caller, at any layer, to supply, substitute,
   or override the annualization basis does not satisfy this assessment and
   MUST be rejected as non-conforming. Caller-override rejection is tested here
   on the candidate existing contract; that test is distinct from, and does not
   substitute for, the §7 ownership-proof proposition of the same name.
5. Version non-substitutability. Every version MUST be immutable and exact. A
   range, alias, "latest" selector, mutable reference, or compatible-version
   fallback is not an exact version and MUST be rejected.

Items 2 through 5 are the four tests frozen WP5.4 assigns, and they are
conjunctive: failure of any one means no conforming exact existing kind is
present. Item 1 states the separate frozen M43-WP2 §8.1 declaration fields. No
field may be inferred from another list. No missing field may be supplied by
M44. No substitution is permitted.

### 8.7 Proposed constitutional outcome

After a proved owner and complete corpus assessment, the later determination
record may propose exactly one of the two frozen `G-4` terminal states:

- `CLOSED` only when an exact existing owner-published governed contract kind
  satisfies every requirement in §8.6 unchanged; or
- `OPEN` only when the exhaustive search proves that no conforming exact
  existing kind is present and the record names the exact missing element and
  the proved exact owner.

A proposed `OPEN` record MUST state exactly what a future owner-domain
governance instrument would have to supply. The authority that fixes that
content, and its whole extent, is frozen M44 Architecture §8.4 C4 and §11
M44-WP5, with frozen M44-WP1 §4.4 evidence item (4). Accordingly the record
MUST enumerate the exact owner, contract kind, identifier, immutable version,
and canonical value bytes, and MUST state the named missing element and the
consequences for `D-2b` and `D-7`. No item may be inferred, omitted, or treated
as an existing instrument.

Frozen M43-WP4 §6.7 states a separate and different thing, in a different
modality, to a different addressee: "The future normative specification may
state the semantic information that a separately governed dependency would have
to make exact—source calendar identity/version, finite decimal or
reduced-rational representation, canonical bytes, compatibility, and Method
Version change effects—but may not define the missing contract or treat that
checklist as one." Its addressee is the future normative specification, which
frozen M44 Architecture §13.1 allocates to M44-WP6 at
`docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`.
Therefore:

- this specification MUST NOT restate that permission as an M44-WP5 obligation
  and MUST NOT attribute a `MUST` to frozen §6.7;
- a determination record MAY reproduce the checklist only as a quoted frozen
  §6.7 permission addressed to that future specification, marked as neither an
  M44-WP5 requirement nor a contract, consistent with frozen §6.7's own bar on
  treating the checklist as a contract; and
- reproducing it MUST NOT define annualization arithmetic, a numeric
  representation, or a Method Version effect, none of which lies within the
  M44-WP5 allocation under frozen §11 M44-WP5 or under §14 of this
  specification.

The `OPEN` record MUST also state that D-2b remains behind D-1, the confirmed
WP5 determination, D-7 when the owner-domain instrument is absent, and every
other separately governed prerequisite. WP5 and D-7 are necessary in the open
case and never sufficient by themselves. D-3 consumes the WP5 outcome only
where an attribution method requires annualization.

The statement is a requirement statement only. It MUST NOT author, register,
extend, version, serialize, or impersonate the missing instrument.

No proposed state is effective until §13 is complete.

## 9. Required repository evidence

A determination record MUST contain every item below that is applicable to the
branch it reaches. Applicability is fixed by the branch, not by whether review
occurs; §10.1, §10.2, and §13 forbid review on the stopping branches:

1. A clean pre-analysis repository status and the exact examined commit.
2. Blob identities for every controlling frozen artifact.
3. A path-level diff proving no frozen artifact was modified.
4. The complete admissibility manifest required by §8.2.
5. The four-proof matrix required by §7, with exact citations and no missing
   proposition.
6. The supported-hypothesis assessment, including the required
   Market Intelligence first test without presumption.
7. If ownership is proved, the exact owner-corpus boundary and exhaustive
   search inventory.
8. If `CLOSED` is proposed, exact owner-published citation, identifier,
   immutable version, canonical value bytes, the five M43-WP2 §8.1 declaration
   fields, and the complete §8.2 closure proof.
9. If `OPEN` is proposed, the proved owner, exact missing element, complete
   absence evidence, the enumerated future-instrument requirement statement
   required by §8.7, and the complete D-1, D-2b, conditional D-3, and D-7
   consequence statement from §8.7.
10. Documentary positive, boundary, and negative vectors, all three categories
    being required by frozen M44-WP5 plan §4.1, carrying every category
    required by frozen M44 Architecture §11 M44-WP5:
    - **If §8.6 is lawfully reached,** at least one positive vector showing the
      shape a conforming owner-published governed contract kind would have to
      take to satisfy §8.6 unchanged. Because the frozen corpus supplies no such
      kind, every positive vector is illustrative and MUST carry the marking
      below; a positive vector admits nothing and closes no gate. On the §10.1
      branch no owner is proved and §§8.5–8.7 MUST NOT begin, so no positive
      vector is produced; producing one there would state an instrument shape
      without a proved owner. On the §10.2 branch the positive vector is
      produced if and only if §8.6 was lawfully entered before the stop, on the
      terms stated below;
    - dependency-closure vectors under frozen M43-WP2 §8.2, including
      unconditional transitive-closure rejection independent of any proposed
      terminal state;
    - version non-substitutability rejection, including ranges, aliases, and
      “latest”;
    - caller-override rejection;
    - rejection of ambient or unversioned `252`, `365`, and `365.25`;
    - the governed-versus-ambient `252` boundary required in item 11; and
    - rejection of an M44-authored contract kind or a requirement statement
      presented as a contract kind.
    Wrong-owner and provider-derived claims MUST also be rejected. The negative
    and rejection vectors in this item are required on every branch, including
    the §10.1 and §10.2 stopping branches; only the positive vector is
    branch-conditioned.

    **Early and within-§8.6 §10.2 stops are distinguished, and the distinction
    is stated exhaustively.** A §10.2 stop is *early* when it occurs before
    lawful entry into §8.6, and is *within §8.6* when it occurs after that
    entry. Both labels are descriptive readings of the single §10.2 branch. They
    are not governed status tokens, terminal states, process-local terms of the
    kind §3 enumerates, or a second stopping branch, and they MUST NOT be
    emitted as any of those. Which case obtains is fixed by the stage the
    record's own evidence establishes was reached, never by the order of the
    triggers listed in §10.2 and never by the fact that ownership was proved: a
    proved owner is not by itself entry into §8.6, because §8.5 stands between
    them. The §10.2 triggers are not uniform in this respect — the
    corpus-boundary, searchability, artifact-identity, and
    absence-versus-unsearched-surface triggers can arise at §8.5, before §8.6 is
    entered, while the mutable-, ranged-, aliased-, provider-, or ambient-value
    trigger, the caller-override trigger, and the owner-published-fields and
    canonical-bytes trigger arise within §8.6.

    On an **early §10.2 stop**, all of the following hold and none is
    discretionary:

    - rejection of ambient or unversioned `252`, `365`, and `365.25` remains
      required;
    - every other negative and rejection vector in this item — dependency
      closure, version non-substitutability, caller override, wrong-owner and
      provider-derived claims, and rejection of an M44-authored contract kind
      or of a requirement statement presented as a contract kind — remains
      required;
    - the item 12 coverage-ledger obligations remain required in full, on the
      stopping-branch terms item 12 states;
    - no positive vector is produced or evaluated;
    - no owner-published evidence is evaluated; and
    - no owner-side conclusion is produced.

    An early §10.2 stop is therefore treated for this item exactly as the §10.1
    branch is treated, notwithstanding that ownership was proved. On a §10.2
    stop **within §8.6**, the positive vector is produced, §8.6 having been
    lawfully entered; the negative, rejection, and coverage-ledger obligations
    above are unchanged and remain required.
11. A boundary example distinguishing an already owner-published,
    version-bound derived session count equal to `252` from ambient `252`,
    without admitting either by example. **If §8.6 is lawfully reached,** the
    example carries both sides. On the §10.1 branch, where no owner is proved,
    the item is discharged by the ambient-`252` rejection alone; the
    owner-published side MUST NOT be supplied, because no proved owner exists
    to attribute a publication to.

    This item in its two-sided form applies only after lawful entry into §8.6.
    On the §10.2 branch it follows that entry and not the proof of ownership.
    On an **early §10.2 stop**, occurring before lawful entry into §8.6, the
    item is discharged by the ambient-`252` rejection alone and the
    owner-published side MUST NOT be supplied — no owner-published evidence
    having been evaluated and no owner-side conclusion having been produced —
    exactly as on the §10.1 branch, and notwithstanding that an owner was
    proved. A proved owner is not a proved publication, and the owner-published
    side MUST NOT be supplied on the strength of ownership alone. On a §10.2
    stop **within §8.6**, the example carries both sides.
12. A coverage ledger mapping every rule in this specification, every frozen
    M44-WP1 §4.4 evidence item, and every frozen M44 Architecture §11 M44-WP5
    Required-tests category to at least one cited record section and
    documentary vector. The ledger is required on every branch. On a stopping
    branch it maps each item that the branch makes inapplicable to the section
    of this specification that withholds it, and records the branch reached; it
    MUST NOT record an item as covered by a vector the branch forbids.

Any illustrative example not backed by an exact existing owner-published
contract MUST be marked `ARTIFICIAL` and `NON-EFFECTIVE`, and MUST carry the
frozen M43-WP4 §6.7 plain-language marking that it is “incapable of passing the
future gate.” The quoted words are a documentary marking, not a governed
status token or new vocabulary. Such an example cannot establish conformance
and cannot satisfy M43-WP2 §8.2.

## 10. Stopping conditions

### 10.1 Ownership not proved

The process MUST stop immediately when:

- no candidate satisfies every requirement of §7;
- more than one candidate remains constitutionally supportable;
- controlling evidence conflicts or is ambiguous;
- proving a candidate would require inference, precedence, amendment, or
  transfer of authority;
- the proposed owner can be stated only as a placeholder, composite,
  unresolved field value, or implicit assignment; or
- source calendar meaning would be transferred out of Market Intelligence.

On this branch:

- the failed propositions and exact evidence defect MUST be recorded;
- no owner is assigned;
- no owner-domain corpus is selected or searched;
- §§8.5 through 8.7, corresponding to frozen WP5.3 through WP5.5, MUST NOT
  begin;
- §13, corresponding to frozen WP5.6, MUST NOT begin;
- no `G-4` terminal state is proposed;
- M44-WP5 does not complete, confirm, or freeze;
- the §12.1.1 checkpoint is neither evaluated nor dispositioned by M44-WP5 or
  by this record, under either frozen reading recorded below;
- no Component G binding is formable; and
- WP6 and WP7 remain unauthorized.

The record MUST classify which defect it has established, and the two classes
MUST NOT be conflated. A defect in the attempted determination is a
work-package defect. It is corrected within M44-WP5 by correcting the
determination record and re-attempting the determination from §8.1 under this
same specification, on the evidence and proof standard already stated in §§6
and 7. That correction is an authoring act within M44-WP5; it is not a review,
confirmation, or freeze stage, it does not enter or invoke §10.3 or §13, and it
does not begin WP5.6. A re-attempt that again fails §7 stops again under this
subsection. The record enters review, confirmation, or freeze only if and when
§8.4 proves one owner and the stages through WP5.5 lawfully complete.

Where the evidence establishes that the frozen ownership ambiguity preserved in
§4 is what prevents the determination, the frozen planning baseline supplies a
mandatory onward route, and the record MUST document it. Frozen M44-WP5 plan §3
states that WP5 "stops under §12.1.1's third outcome pending the M44
Architecture Freeze Record's required new independently confirmed architecture
revision that names the defect." The frozen §5 `WP5.2` exit condition requires
WP5 to "stop under §12.1.1's third outcome and route the frozen ambiguity
through the M44 Architecture Freeze Record's process for a new independently
confirmed architecture revision that names the defect." Frozen §5.1 states that
"a new independently confirmed architecture revision that names the defect must
first correct the ambiguity, after which WP5 and then the checkpoint may be
re-evaluated." The process itself is fixed by frozen M44 Architecture Freeze
Record §9 — "[a] defect in it is corrected only by a new independently confirmed
architecture revision that names the defect (constitution G5), never by editing
it in place" — and by frozen M44 Architecture §1.6 rule 3.

Documenting that required route is not exercising it, and the distinction is
constitutive. Documenting it means citing the frozen text that supplies the
route and recording that M44-WP5 cannot proceed until that route completes.
Exercising it would mean initiating, requesting, authorizing, drafting,
prescribing, naming the defect on the architecture's behalf, or supplying any
part of the revision. This deliverable MUST do only the former. It MUST NOT
resolve the §4 ambiguity, MUST NOT amend or reinterpret any frozen artifact, and
MUST NOT treat the route's existence as a prediction that it will be taken, as
authority already granted, or as a stage of M44-WP5.

Until such a separately authorized and independently confirmed architecture
revision exists, M44-WP5 remains incomplete, no `G-4` terminal state is
formable, the §12.1.1 checkpoint is not evaluated or dispositioned by M44-WP5
or by this record, and M44-WP6 and M44-WP7 remain unauthorized.

The two frozen readings of how §12.1.1 relates to this branch, preserved in §4,
MUST both be cited here and neither ranked. Frozen M44-WP5 plan §3, §5 `WP5.2`,
and §5.1 characterize the stop as occurring "under §12.1.1's third outcome,"
whose frozen row reads "[e]ither gate's state not established | **Stop.** An
unestablished gate state is a review defect in the producing work package and is
corrected before the checkpoint is re-evaluated." Frozen M44 Architecture
§12.1.1 opens "After M44-WP4 and M44-WP5 are confirmed and before M44-WP6
begins," which on its own terms is not reached by an unconfirmed M44-WP5. The
record MUST NOT resolve that difference.

Under the third-outcome reading, the checkpoint's evaluation is a separate
governance act performed by the independent confirmation required at frozen M44
Architecture §12.5 point 5, not by M44-WP5: frozen §12.1.1 states that "[n]o
work package may declare the checkpoint satisfied on its own authority." On
that reading the third row returns **Stop**, dispositions no gate, and treats
the unestablished state as "a review defect in the producing work package"
corrected before the checkpoint is re-evaluated. Under the unreached reading
the checkpoint is not arrived at at all. What holds unqualified under both
readings, and what the consequence bullet above states, is that M44-WP5 and
this record neither evaluate nor disposition the checkpoint. Under either
reading the outcome for this branch is the same: the process stops, no gate or
checkpoint is dispositioned by M44-WP5, and the route above is the only stated
means of correcting the frozen ambiguity.

### 10.2 Repository proof incomplete

After ownership is proved, the process MUST stop without proposing a `G-4`
terminal state when:

- the proved owner's frozen corpus boundary cannot be established;
- the corpus is inaccessible or cannot be searched exhaustively;
- artifact identity or frozen status cannot be verified;
- search results cannot distinguish absence from an unsearched surface;
- an apparent match depends on a mutable, ranged, aliased, provider, or ambient
  value;
- an apparent match permits a caller, at any layer, to supply, substitute, or
  override the annualization basis; or
- required owner-published fields or canonical bytes cannot be verified and
  corpus completeness is also unproved.

On this branch:

- no `G-4` terminal state is established or proposed;
- the ownership conclusion remains proposed documentary reasoning with no
  constitutional effect under §13, while its reasoning is preserved in the
  record;
- M44-WP5 does not complete, confirm, or freeze;
- the §12.1.1 checkpoint is neither evaluated nor dispositioned by M44-WP5 or
  by this record, under either frozen reading recorded in §10.1;
- no Component G binding is formable;
- the §9 evidence applicable to the branch remains required, including the
  item 12 coverage ledger and the item 10 negative and rejection vectors, on
  the early and within-§8.6 terms §9 items 10 and 11 state; and
- WP6 and WP7 remain unauthorized.

The two frozen readings of how §12.1.1 relates to an unestablished gate state,
preserved in §4 and set out in §10.1, apply to this branch on the same terms
and are neither ranked nor resolved here.

Sections §8.7 and §13 — the frozen WP5.4 terminal-state proposal, frozen WP5.5,
and frozen WP5.6 — MUST NOT begin. The four frozen WP5.4 tests reached inside
§8.6 — M43-WP2 §8.2 closure, the distinct M43-WP4 §6.7 information,
caller-override rejection, and version non-substitutability — yield no terminal
state on this branch.

The record MUST classify which defect it has established, and the classes MUST
NOT be conflated. A defect in the repository evidence supporting the attempted
determination is a work-package defect, of the same class §10.1 addresses and
differing only in the evidence it concerns. It is distinct from a defect or
ambiguity in frozen architecture, for which this subsection creates no remedy,
no route, and no amendment authority. A repository-evidence defect is corrected
within M44-WP5 by correcting the determination record and re-attempting the
determination from §8.1 under this same specification, on the evidence,
ordering, and proof standard already stated in §§6 through 8, which this
subsection leaves unchanged and does not relax, waive, or partially apply. That
correction is an authoring act within M44-WP5, performed within this same
deliverable; it is not a review, confirmation, or freeze stage, it does not
enter or invoke §10.3, it does not enter or invoke §13, and it does not begin
WP5.6. Re-attempt begins at §8.1 and at no later stage: the boundary lock,
evidence manifest, hypothesis record, and ownership proof are re-established in
full, and a proof established in the stopped attempt is not carried forward as
established, though its reasoning remains preserved in the record. A re-attempt
whose repository evidence is again incomplete stops again under this subsection.
The record enters review, confirmation, or freeze only if and when §8.6
completes on verified evidence, §8.7 lawfully yields one of the two frozen
terminal states, and the stages through WP5.5 lawfully complete.

This mechanism creates no fallback and no default. It does not permit the
determination to proceed on unverified evidence, to treat an unproved corpus
boundary as proved, to treat an unsearched surface as absence, or to admit any
value, version, contract kind, or caller override that §6, §8, or this
subsection excludes. It implies no eventual success: nothing in it states,
predicts, or reserves that a re-attempt will succeed, no number of re-attempts
is guaranteed to yield a terminal state, and a determination may stop under this
subsection without limit. It creates no lifecycle, no lifecycle state, no
governed status token, no stage, no recursion into §13, and no review-stage
routing of any kind; correction under this subsection is an authoring act and
nothing else. §10.3 is unchanged by this subsection and remains inapplicable to
this branch.

### 10.3 Constitutional review stop

This subsection applies only after WP5.5 has completed and a candidate has
lawfully entered WP5.6. It is inapplicable to the §10.1 and §10.2 branches,
which never enter review, confirmation, or freeze.

The process MUST stop when review identifies any unresolved blocking finding,
authority expansion, frozen-artifact modification, new governed vocabulary,
implicit owner, invented precedence, invalid terminal state, or downstream
authorization.

Correction MUST remain within this specification and the separately authorized
determination scope. A correction requiring amended frozen authority is outside
M44-WP5 and MUST NOT be improvised.

## 11. Failure conditions

A proposed determination fails constitutional review if any of the following
is true:

- it names an owner without the complete §7 proof;
- it uses inadmissible evidence as affirmative support;
- it searches a presumptive owner's corpus before ownership is proved;
- it conflates the M43-WP2 §8.1 fields with the M43-WP4 §6.7 information;
- it treats a contract candidate as existing without exact frozen
  owner-domain publication;
- it treats corpus silence as exhaustive absence without a proved boundary;
- it admits an ambient constant, caller override, provider behavior, version
  substitution, or implementation practice;
- it authors or implies a missing contract kind, identifier, version, or
  canonical bytes;
- it treats a requirement statement or illustrative example as a governed
  instrument;
- it introduces a terminal state or `OPEN` variant outside frozen §16.2;
- it claims `G-4 CLOSED` on the strength of a blockage or requirement;
- it claims `G-4 OPEN` without both the exact missing element and a proved exact
  owner;
- it modifies or reinterprets a frozen artifact;
- it dispositions G-3 or §12.1.1;
- it authorizes WP6, WP7, implementation, runtime, providers, serialization,
  or another work package; or
- it proceeds with unresolved blocking review findings.

A failed determination has no ownership, gate, contract, implementation, or
downstream effect.

## 12. Required constitutional outputs

Application of this specification MUST be incorporated into the single frozen
§11 and §13.1 architectural deliverable at:

`docs/implementation/M44_WP5_ANNUALIZATION_BASIS_OWNERSHIP_DETERMINATION_AND_REQUIREMENT_SPECIFICATION.md`

No other WP5 architectural determination, requirement specification, or
constitutional-process artifact may be produced. The one bounded record is not
an implementation artifact, operating procedure, submission package, or
owner-domain decision record. Within that record, the following sections are
required when applicable to the branch reached:

1. **Authority declaration** — all authority ceilings in this specification.
2. **Frozen-baseline identity** — exact commit, blobs, paths, sections, and
   immutability verification.
3. **Evidence manifest** — admissible and rejected evidence under §6.
4. **Hypothesis assessment** — supported hypotheses and their disposition,
   preserving hypothesis status until proof.
5. **Four-proof matrix** — every proposition in §7 and its exact evidence.
6. **Ownership conclusion** — either one constitutionally proved owner or a
   fail-closed statement that ownership was not proved. The method supplies
   neither conclusion in advance; the applied record in §12.1 supplies the
   candidate conclusion only after completing the required proof.
7. **Corpus assessment** — required only if an owner is proved; exact boundary,
   inventory, search, and completeness evidence.
8. **Existing-contract assessment** — required only if §8.6 is reached.
9. **Proposed G-4 record** — required only when §8.7 lawfully yields `CLOSED`
   or `OPEN`; absent on every stopping branch.
10. **Documentary evidence and coverage ledger** — all applicable items in §9.
11. **Downstream boundary statement** — no G-3 or checkpoint disposition and no
    WP6, WP7, implementation, runtime, provider, or serialization authority.
12. **Independent governance evidence** — required only after WP5.5 completes
    and the record lawfully enters WP5.6; expressly inapplicable on the §10.1
    and §10.2 stopping branches.

These are required sections of the bounded determination record. This
specification does not authorize creation of additional packages, procedures,
contracts, registries, APIs, schemas, fixtures, source files, or decision
records.

### 12.1 RC6.3 applied determination record — WP5.1 through WP5.5

This subsection applies §§6–8 to repository evidence through frozen WP5.5. It
is the determination record incorporated into this sole deliverable. It does
not perform WP5.6, does not supply its own review or confirmation evidence, and
does not make its proposed ownership conclusion or `G-4` state effective.

#### Boundary lock and frozen-baseline identity

The repository evidence baseline examined by this determination is commit
`052358fb7b93985b34a4c9a156d5fc92b4293e60`. The pre-correction working tree
was clean. At that commit this specification was blob
`39a55733a2f114cc9a77bd26d79b18637446705b`. RC6.3 changes only this unfrozen
WP5 deliverable; it changes no frozen artifact.

The controlling frozen artifacts and their exact blobs at the examined commit
are below. Every bare filename in this applied record denotes the exact
repository path `docs/implementation/<filename>`; paths outside that directory
are written in full.

| Controlling artifact | Exact blob | Controlling scope |
| --- | --- | --- |
| `docs/architecture/platform_architecture.md` | `e9164fe75e306035321858c58039922b8ec9584c` | §§6.2 and 6.5 domain ownership |
| `M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md` | `d673c5bf3099716bd2043fef6856e20133a2309b` | §4 ownership; §§6.2, 6.6, and 8 dependency identity, caller rejection, and closure |
| `M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md` | `d6bcc609faa3e1a5a61c2f2175669e21939657a5` | §§5.2 and 6.7 |
| `M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | `088a28dbf9655f234ef8c0e6ef2c1391e2ef2116` | §§5–6, 8.4, 11, 12, 16.2, and OQ-3 |
| `M44_ARCHITECTURE_FREEZE_RECORD.md` | `bd2644753db270e1a4cc45805ef8f2bf86428fc1` | frozen M44 authority and amendment boundary |
| `M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md` | `3e952e014007ec0f9237760b6038e5d2ae528f96` | §4.4 `G-4` evidence requirements and repository evidence |
| `M44_WP1_FREEZE_RECORD.md` | `038d844801aadb423b7ec5a6aac3fe2a5a65ed34` | WP1 confirmed and frozen status |
| `M44_WP5_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | `c8cb5cbe7d0f5c0e118e5bdebc7e819fda78ffb9` | frozen non-normative WP5 planning constraints |
| `M44_WP5_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md` | `42575fde02b12d930c5669194e1543d789de6fd1` | confirmation of the planning basis only |
| `M44_WP5_PLANNING_FREEZE_RECORD.md` | `8f9e6c5a52d39c546880f4ae60a1f87ef2a0024e` | exact frozen planning corpus and authority ceiling |
| `M44_WP5_PLANNING_CLOSEOUT.md` | `cc74458f294174a7ef2c3fb779876f4cea6c8205` | planning closeout and downstream boundary |
| `M44_WP4_FREEZE_RECORD.md` | `8623bbdabbb4fd35318e125173cd99c48ffd9c2e` | frozen `G-3 OPEN — PARTIAL` state |

Every authority ceiling in the header remains in force. Before this
determination, Annualization Basis ownership and `G-4` were `NOT DETERMINED`;
`G-3` was and remains `OPEN — PARTIAL`; and the frozen §12.1.1 checkpoint was
and remains `NOT DISPOSITIONED`. The exclusions in §14 remain unchanged. This
boundary lock establishes no implementation, runtime, provider, contract,
checkpoint, WP6, or WP7 authority.

#### Evidence manifest and admissibility

| Evidence | Commit and blob identity | Status and constitutional owner | Proposition assessed | Admissibility |
| --- | --- | --- | --- | --- |
| Platform Architecture §§6.2 and 6.5 | examined commit; blob `e9164fe75e306035321858c58039922b8ec9584c` | frozen; Platform Architecture constitutional governance | Market Intelligence owns canonical calendars and market context; Portfolio Intelligence owns derived-measure meaning and consumes Market Intelligence inputs | `ADMISSIBLE — OWNERSHIP` |
| M43-WP2 §4 and §§8.1–8.3 | examined commit; blob `d673c5bf3099716bd2043fef6856e20133a2309b` | frozen; Portfolio Intelligence | Calendars remain Market Intelligence-owned; a calculation dependency requires exact owner, existing kind, identifier, and immutable version; governed evidence is not a dependency declaration | `ADMISSIBLE — OWNERSHIP AND AVAILABILITY` |
| M43-WP4 §§5.2 and 6.7 | examined commit; blob `d6bcc609faa3e1a5a61c2f2175669e21939657a5` | frozen; Portfolio Intelligence planning authority | Four-proof requirement; no artificial dependency kind; frozen-corpus absence statement; exact information required before admission | `ADMISSIBLE — PROOF AND AVAILABILITY` |
| M44 Architecture §§5.1, 8.4, 11, 16.2, and OQ-3 | examined commit; blob `088a28dbf9655f234ef8c0e6ef2c1391e2ef2116` | frozen; M44 constitutional governance | WP5 determination allocation, Market Intelligence first hypothesis, two `G-4` outcomes, completion and downstream consequences | `ADMISSIBLE — AUTHORITY AND PROOF` |
| M44-WP1 §4.4 | examined commit; blob `3e952e014007ec0f9237760b6038e5d2ae528f96` | confirmed and frozen; M44-WP1 | Required disposition evidence and repository-wide absence of an Annualization Basis governance instrument | `ADMISSIBLE — AVAILABILITY` |
| `M40_WP2_Canonical_Market_Measure_Vocabulary_Admission_Review.md` §§1, 2.2–2.3, 6, and 7 | examined commit; blob `262aab1ffd1f41617a9850706a315d988f3977dc` | complete and frozen by M40 closeout; seven admitted concepts are Market Intelligence-owned and Mechanical Boundary Rules is Repository Architecture Governance-owned | Whether its binary canonical-vocabulary admissions, rejections, owner mappings, or versioned-semantic composition publish, admit, or establish an Annualization Basis governing contract | `ADMISSIBLE — CORPUS AVAILABILITY; NOT USED TO SELECT OWNER` |
| `M40_WP3_CANONICAL_GLOSSARY_SYNCHRONIZATION.md` §§1, 3, and 6–8 | examined commit; blob `f4a43b444196764ace04ebf381ca183cd5d9b040` | complete, independently approved, and frozen by M40 closeout; synchronized canonical vocabulary with seven Market Intelligence-owned concepts and one Repository Architecture Governance-owned concept | Whether its synchronization of admitted meanings into canonical vocabulary establishes an Annualization Basis governing contract | `ADMISSIBLE — CORPUS AVAILABILITY; NOT USED TO SELECT OWNER` |
| `M41_WP1_CANDIDATE_VOCABULARY_AND_OWNERSHIP_REGISTER.md` §§3, 6.0, 6.2, and 6.5 | examined commit; blob `d0d5ffa15ab99037ffacf0963c8b2e3648d15327` | confirmed and frozen by M41-WP1 closeout; Market Intelligence owner-governed register | Whether its candidate ownership, Method Version dependency, or Measurement Window surfaces publish or establish an Annualization Basis governing contract | `ADMISSIBLE — CORPUS AVAILABILITY; NOT USED TO SELECT OWNER` |
| `M41_WP2_STAGE_A_CANDIDATE_VOCABULARY_REGISTER.md` §§1 and 3 | examined commit; blob `4cb27ce95f13e08ac15d86d1c7ec809b05bbc1d0` | confirmed and treated as frozen by the M41-WP2 confirmation chain; owner-governed Stage A register | Whether its Subject, ordering, or Manifest Entry ownership dispositions publish or establish an Annualization Basis governing contract | `ADMISSIBLE — CORPUS AVAILABILITY; NOT USED TO SELECT OWNER` |
| `M41_WP3_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md` §§2.2–2.3, 4 Component C/H, and 7.5 | examined commit; blob `ec1c420d099bc7828e716607bb6ac37a5100761a` | approved and immutable within frozen M41-WP3; Market Intelligence owner-governed Stage A register | Whether its session/count-basis, calendar, and dependency surfaces publish or establish an Annualization Basis governing contract | `ADMISSIBLE — CORPUS AVAILABILITY; NOT USED TO SELECT OWNER` |
| `M41_WP4_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md` §§0, 4, and 4.1 | examined commit; blob `867ed1c91977152686614507f85f4544e0f264d9` | confirmed and frozen by the M41-WP4 Stage A confirmation and closeout; Market Intelligence owner-governed Stage A register | Whether its Result, provenance, or dependency-surface dispositions publish or establish an Annualization Basis governing contract | `ADMISSIBLE — CORPUS AVAILABILITY; NOT USED TO SELECT OWNER` |
| Remaining frozen M39–M41 Market Intelligence corpus bounded below | examined commit; exact per-artifact blobs below | frozen; Market Intelligence | Whether an exact existing Annualization Basis governed contract kind is already owner-published | `ADMISSIBLE — AVAILABILITY ONLY AFTER OWNERSHIP PROOF` |
| WP5 planning §§3, 5, and 7 | examined commit; blob `c8cb5cbe7d0f5c0e118e5bdebc7e819fda78ffb9` | frozen non-normative; M44-WP5 planning governance | Ordered workflow, evidence sequence, and review-entry condition | `ADMISSIBLE — PROCESS CONSTRAINT; NOT OWNERSHIP EVIDENCE` |
| Source code, provider behavior, libraries, configuration, current implementations, examples, fixtures, and repository material outside the bounded owner corpus | examined repository state | non-constitutional or not controlled by the proved owner | Possible convenient or conventional values and mechanisms | `INADMISSIBLE — §6.2; NO AFFIRMATIVE RELIANCE` |

No planning statement, corpus absence, implementation fact, provider datum,
example, or desired downstream outcome participates in the ownership proof.
The six required M40–M41 admission, synchronization, Stage A, and register
artifacts above were inspected only after the ownership proof and cannot be
used circularly to select the corpus owner.

#### Hypothesis record

Market Intelligence is tested first because frozen OQ-3 requires that order.
The tested hypotheses and materially plausible alternatives are:

| Hypothesis or alternative | Admissible basis for testing | Determination |
| --- | --- | --- |
| Market Intelligence | Platform Architecture §6.2 expressly allocates market calendars, rates, histories, and market context to Market Intelligence; M43-WP2 §4 preserves that allocation; frozen OQ-3 directs this hypothesis to be tested first | `PROVED` by the conjunctive matrix below |
| Portfolio Intelligence | Platform Architecture §6.5 allocates derived measures and their semantics to Portfolio Intelligence | `REJECTED` as owner of the dependency: consumption and measure semantics do not transfer source-calendar meaning, and M43-WP4 §6.7 requires placement without expansion of Portfolio Intelligence authority |
| Ledger & Accounting | Platform Architecture §6.3 owns financial truth and canonical formula inputs | `REJECTED`: it owns recorded financial truth and ledger-derived inputs, not calendars, market context, or a calendar-derived Annualization Basis |
| Asset Foundation | Platform Architecture allocates asset identity, classification, and currency dimension to Asset Foundation | `REJECTED`: no frozen allocation gives it calendar meaning or Annualization Basis dependency ownership |
| Caller, provider, library, registry, or shared ownership | none | `REJECTED AS INADMISSIBLE`: each would violate §§6–7, M43-WP2, or singular ownership |

No additional supported owner hypothesis appears in the frozen allocations.
The absence of an owner-domain contract is not used to select the owner.

#### Four-proof ownership matrix

| Required proposition | Exact constitutional reasoning | Result |
| --- | --- | --- |
| `VERSIONED_CALCULATION_DEPENDENCY` is correct | An Annualization Basis is an output-affecting calculation control that a Portfolio Method Version must bind by exact owner, contract kind, identifier, and immutable version under M43-WP2 §8.1. M43-WP4 §§5.2 and 6.7 expressly place a representable Annualization Basis in the calculation-dependency path and prohibit an ambient or artificial substitute. Its value must therefore be exact and version-bound rather than invocation evidence. | `PROVED` |
| `GOVERNED_EVIDENCE` is incorrect | M43-WP2 §8.3 separates invocation evidence—observations, Market Measure Results, Ledger evidence, and references—from an exact governed calculation dependency. Calendar observations may be evidence owned by Market Intelligence, but the Annualization Basis is the versioned rule/dependency consumed by the calculation; treating it as evidence would evade the exact dependency declaration and closure required by §8. | `PROVED` |
| Caller override is rejected | M43-WP2 §6.6 denies permission to select an Annualization Basis at invocation time; §7.6 forbids a caller-supplied governed value; and §12 item 7 declares a request-supplied Annualization Basis constitutionally invalid. M43-WP4 §6.7 independently requires caller-override rejection and prohibits ambient constants. | `PROVED` |
| Owner and placement expand no Portfolio Intelligence authority and transfer no calendar meaning | Platform Architecture §6.2 assigns canonical calendars and market context exclusively to Market Intelligence, and frozen M44 OQ-3 states that the Annualization Basis is derived from session-calendar facts already allocated there. Determining Market Intelligence as owner preserves that allocation; Portfolio Intelligence remains only the consumer of an exact dependency. This determination grants Market Intelligence no new instrument-authoring authority: D-7 would require a future, separately authorized owner-domain governance act. Source calendar identity and version remain Market Intelligence-owned and distinct from the separately versioned dependency record. | `PROVED` |

The proof does not rely on contract availability. Market Intelligence is the
only hypothesis satisfying all four propositions. Portfolio Intelligence would
acquire source-owned calendar meaning; Ledger & Accounting and Asset Foundation
lack the relevant frozen allocation; and shared, provider, caller, or inferred
ownership is prohibited. Two readers applying the same explicit domain
allocations and the same M43-WP2/M43-WP4 distinctions therefore reach the same
owner without a tie-break, fallback, or new precedence rule.

**Proposed ownership conclusion:** `MARKET INTELLIGENCE`.

This conclusion is not effective until §13 completes.

#### Proved-owner frozen-corpus boundary and inventory

The boundary universe is every repository artifact at the examined commit
whose filename begins `M39_`, `M40_`, or `M41_` under
`docs/implementation/`: 79 artifacts in total. The searched owner corpus is
the 17-artifact subset of frozen, Market Intelligence-governed M39–M41
specifications, admission/synchronization records, and constitutional
registers that can publish or establish owner-governed contract meaning. A
corpus member need not itself be an exact dependency contract kind:
candidate-vocabulary and semantic-surface registers are included because they
can establish governed meaning, ownership, placement, or dependency
constraints that bear on whether such a kind exists.

The remaining 62 artifacts are accounted for individually below. They are
outside the candidate-contract corpus only where frozen authority establishes
their constitutional role as planning or architecture proposal, lifecycle
evidence, closeout, governance reconciliation, or non-frozen empty-scope
proposal/review. They are not excluded because their names or contents appear
unlikely to mention Annualization Basis. Boundary-role inspection establishes
whether an artifact has owner-domain publication authority; it is not used as
a substitute for including and searching every artifact that has that
authority. Examples, fixtures, source code, implementations, and artifacts
owned by other domains remain outside the candidate-contract boundary.

The complete owner-authored specification inventory assessed for an exact
existing Annualization Basis governed contract kind is:

| Owner-corpus artifact | Exact blob | Assessment |
| --- | --- | --- |
| `M39_WP1_Canonical_Boundary_Specification.md` | `50dda30ed8b471cba964627438e6a543d7b32aff` | Market Observation boundary; no Annualization Basis contract kind |
| `M39_WP2_market_observation_source_boundary_specification.md` | `5a8958fcf647e15e0fd9920daf0acd1e56086b9c` | Observation-source semantics; no Annualization Basis contract kind |
| `M39_WP3_market_observation_classification_specification.md` | `3d3a0e5cb063821448260efd80c9534ffec51ab6` | Observation classification; no Annualization Basis contract kind |
| `M39_WP4_market_observation_payload_specification.md` | `de8632c5ac7fa9bff9f50b1ca5217a5e131160eb` | Observation payload; no Annualization Basis contract kind |
| `M39_WP5_market_observation_relationship_specification.md` | `0db1d69d13a3050281c0ed76b7cd84ff5bbd8c55` | Observation relationships; no Annualization Basis contract kind |
| `M39_WP6_market_observation_identity_specification.md` | `a20d0ea55a3703cb5131a7b721019e9c7222eb30` | Observation identity; no Annualization Basis contract kind |
| `M40_WP1_Canonical_Market_Measure_Vocabulary_and_Ownership_Specification.md` | `d610c32fc2a4eadfdd136a86533708cd29090f25` | Market Measure vocabulary and ownership; no Annualization Basis contract kind |
| [`M40_WP2_Canonical_Market_Measure_Vocabulary_Admission_Review.md`](M40_WP2_Canonical_Market_Measure_Vocabulary_Admission_Review.md) | `262aab1ffd1f41617a9850706a315d988f3977dc` | §§1, 2.2–2.3, 6, and 7 apply binary canonical-vocabulary admission, preserve sole owner mappings, and admit semantic composition containing explicit semantic and dependency versions. The artifact admits seven Market Intelligence-owned concepts and one Repository Architecture Governance-owned concept, but at issuance does not itself register effective Glossary vocabulary. It publishes or establishes no exact Annualization Basis governed contract kind, identifier, immutable version, or canonical value bytes |
| [`M40_WP3_CANONICAL_GLOSSARY_SYNCHRONIZATION.md`](M40_WP3_CANONICAL_GLOSSARY_SYNCHRONIZATION.md) | `f4a43b444196764ace04ebf381ca183cd5d9b040` | §§1, 3, and 6–8 synchronize the eight admitted meanings and sole-owner mappings into the Canonical Glossary; M40 closeout records the synchronization as independently approved, making the terms shared canonical meaning. Its authority is semantic vocabulary only, and it establishes no exact Annualization Basis governed contract kind, identifier, immutable version, or canonical value bytes |
| [`M41_WP1_CANDIDATE_VOCABULARY_AND_OWNERSHIP_REGISTER.md`](M41_WP1_CANDIDATE_VOCABULARY_AND_OWNERSHIP_REGISTER.md) | `d0d5ffa15ab99037ffacf0963c8b2e3648d15327` | §§3, 6.0, 6.2, and 6.5 govern candidate ownership, Method Version dependencies, and Measurement Window calendar references, while §3 defers the contract text itself. No exact Annualization Basis governed contract kind, identifier, immutable version, or canonical value bytes are published or established |
| `M41_WP1_DEFINITION_METHOD_VERSION_APPLICABILITY_CONTRACT_SPECIFICATION.md` | `6e19d41934e6679f2d3ef846a8b0b33c0ddd073f` | Market Measure Definition/Method Version; no Annualization Basis contract kind |
| [`M41_WP2_STAGE_A_CANDIDATE_VOCABULARY_REGISTER.md`](M41_WP2_STAGE_A_CANDIDATE_VOCABULARY_REGISTER.md) | `4cb27ce95f13e08ac15d86d1c7ec809b05bbc1d0` | §§1 and 3 govern Subject Reference, Subject Ordering Key, and Manifest Entry vocabulary and ownership. No Annualization Basis contract kind, field set, identifier, immutable version, or canonical value bytes are published or established |
| `M41_WP2_STAGE_B_SUBJECT_AND_MANIFEST_CONTRACT_SPECIFICATION.md` | `f3a7168a3b684426e6770341caf034bbf3427e7b` | Market Measure subject and manifest; no Annualization Basis contract kind |
| [`M41_WP3_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md`](M41_WP3_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md) | `ec1c420d099bc7828e716607bb6ac37a5100761a` | §4 Component C classifies elapsed/civil/session/count basis and exact calendar rules as Method Version semantics with exact dependencies; Component H preserves the sole version-bound dependency list; §7.5 expressly rejects a default calendar and a `252`-session assumption. These constraints publish or establish no exact Annualization Basis governed contract kind, identifier, immutable version, or canonical value bytes |
| `M41_WP3_STAGE_B_TEMPORAL_UNIT_ADJUSTMENT_ARITHMETIC_CONTRACT_SPECIFICATION.md` | `5afb26e3b3e34fb825a56277ed56bbce96c5ad29` | Temporal/calendar consumption semantics. Its §5.1 `session count` is a method-declared duration amount using an exact named calendar dependency; it supplies no Annualization Basis kind, identifier, immutable version, or canonical value bytes |
| [`M41_WP4_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md`](M41_WP4_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md) | `867ed1c91977152686614507f85f4544e0f264d9` | §§0 and 4 govern Result, provenance, identity, and handoff surfaces; §4.1 finds no new governed dependency and preserves the Method Version dependency list as sole inventory. No Annualization Basis contract kind, identifier, immutable version, or canonical value bytes are published or established |
| `M41_WP4_STAGE_B_RESULT_STATE_AND_PROVENANCE_CONTRACT_SPECIFICATION.md` | `0a05b925b77b86d7a57de0d47c6d3743e15b95d8` | Market Measure result/state/provenance; no Annualization Basis contract kind |

The complete boundary accounting is:

| Boundary disposition | Count | Record |
| --- | ---: | --- |
| `INCLUDED — SEARCHED OWNER CORPUS` | 17 | the exact inventory above |
| `EXCLUDED — CONSTITUTIONALLY ACCOUNTED` | 62 | the exact exclusion ledger below |
| **Total M39–M41 prefixed artifacts** | **79** | no unclassified artifact |

The exclusion-authority keys used below are exact and role-specific:

- **`X-LIFECYCLE`** — frozen
  [M44-WP5 plan](M44_WP5_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §6, blob
  `c8cb5cbe7d0f5c0e118e5bdebc7e819fda78ffb9`, states that separately
  named review, response, confirmation, freeze, and closeout records are
  governance evidence only and authorize no owner-domain contract artifact.
  Frozen M44 Architecture §§12.4 and 13.1, blob
  `088a28dbf9655f234ef8c0e6ef2c1391e2ef2116`, separately allocates those
  lifecycle roles.
- **`X-M39-CLOSEOUT`** — frozen
  [M39 closeout](M39_EPIC_CLOSEOUT.md) §§1 and 3, blob
  `d766779d2884d1504a38f43d3ddf7250f3d1877a`, identifies WP1–WP6 as
  the six canonical frozen corpus paths and states that the closeout only
  reconciles the repository and creates no new architecture or semantic
  concept.
- **`X-M40-PLAN`** — frozen
  [M40 closeout](M40_EPIC_CLOSEOUT.md) §§1–3, blob
  `f94503d38fc03248897aa91fcaae309af8ecaf2f`, separates the M40 plan and
  architecture review cycle from the completed WP1–WP4 outputs and states
  that closeout does not convert the planning document into implementation
  authority or approve a formula or production method. The final
  candidate-publication outputs are the included M40-WP1 through M40-WP3
  artifacts.
- **`X-M40-CHAIN`** — M40 closeout §3, same blob, identifies every M40
  review, response, and confirmation as a lifecycle companion to a separately
  named substantive output; `X-LIFECYCLE` fixes the constitutional effect of
  that role.
- **`X-M40-CLOSEOUT`** — M40 closeout §§1 and 6, same blob, classifies itself
  as governance closeout and grants no production method, formula, model,
  implementation, runtime, provider, persistence, or API authority.
- **`X-M40-RECONCILIATION`** — frozen
  [M40-WP4 Decision Log Reconciliation](M40_WP4_DECISION_LOG_RECONCILIATION.md)
  §§1 and 3–4, blob `11aadb89b8c43bf5d3ff50e5372aa79e3b3cc16b`, states that it
  summarizes already-completed M40-WP1 through M40-WP3 decisions without
  reopening, redesigning, or reproducing their specifications and creates no
  formula, method, model, or contract authority.
- **`X-M41-ARCHITECTURE`** — frozen
  [M41-WP1 closeout](M41_WP1_CLOSEOUT.md) **Scope Completed** and
  **Canonical Deliverables**, blob
  `c16baaff939977c14f14bba9ab6ab09f71b611bf`, classifies the confirmed,
  frozen M41 architecture as the architecture dependency and separately names
  the Stage 1 register and Stage 2 specification as the canonical substantive
  outputs. The proposal and its review chain therefore allocate and validate
  work; they do not replace those owner-domain publications.
- **`X-M41-WP1`** — M41-WP1 closeout **Canonical Deliverables**,
  **Authority after Closeout**, and **Non-Reopening Statement**, same blob,
  identifies the included Stage 1 register and Stage 2 specification as the
  normative authority and every review, response, confirmation, and the
  closeout as historical lifecycle/status evidence.
- **`X-M41-WP2`** — confirmed
  [M41-WP2 Architecture Proposal](M41_WP2_ARCHITECTURE_PROPOSAL.md) §11,
  blob `6c77d8786035c9d5f4b121fc3c08b3987dc3c670`, separately allocates the
  Stage A register, the Stage B actual contract text, and their review
  artifacts. [Final Architecture Confirmation](M41_WP2_FINAL_ARCHITECTURE_CONFIRMATION.md),
  blob `96391f36aa5adbfa8dc5f590714c70a673efe508`, confirms that allocation.
  The included Stage A and Stage B artifacts are the candidate-publication
  outputs; the architecture proposal and lifecycle companions are not.
- **`X-M41-WP2-STAGE-C`** — the confirmed M41-WP2 architecture §11 and its
  final confirmation, the two `X-M41-WP2` blobs above, allocate only Stage A
  and Stage B substantive outputs. The Stage C proposal records an empty
  semantic scope and its review returns `APPROVED`, but neither artifact has an
  independent confirmation or freeze record. They are non-frozen and cannot
  enlarge the confirmed two-stage allocation.
- **`X-M41-WP3`** — frozen
  [M41-WP3 closeout](M41_WP3_CLOSEOUT.md) **Final Document Chain** and
  **Final Authority Status**, blob
  `e715dbe5a6a5b3142d23bb8a2b5fe113fc88e10a`, distinguishes the approved
  architecture and lifecycle records from the approved Stage A register and
  confirmed, frozen Stage B specification. The latter two are included; the
  former records only allocate, review, correct, confirm, or close them.
- **`X-M41-WP4`** — frozen
  [M41-WP4 closeout](M41_WP4_CLOSEOUT.md) **Reconciled Governance Chain** and
  **Final Authority Status**, blob
  `727d352c61ba3db0e4a340437b829ae94d5b230f`, distinguishes the confirmed
  architecture and lifecycle records from the confirmed, frozen Stage A
  register and Stage B contract specification. The latter two are included;
  the former records only allocate, review, correct, confirm, or close them.

Every excluded artifact is classified below. `OUTSIDE` means outside the
candidate owner-domain contract-publication corpus, not absent from the
repository and not ignored.

| Excluded artifact | Exact blob | Constitutional role and disposition | Exact exclusion authority |
| --- | --- | --- | --- |
| `M39_EPIC_CLOSEOUT.md` | `d766779d2884d1504a38f43d3ddf7250f3d1877a` | `LIFECYCLE CLOSEOUT — OUTSIDE` | `X-M39-CLOSEOUT` |
| `M40_Canonical_Asset_Market_Measure_Foundation_Plan.md` | `6dc356c9f3c0aa22736657f32eed720ed62dfb7c` | `PLANNING/PROPOSAL — OUTSIDE` | `X-M40-PLAN` |
| `M40_EPIC_CLOSEOUT.md` | `f94503d38fc03248897aa91fcaae309af8ecaf2f` | `LIFECYCLE CLOSEOUT — OUTSIDE` | `X-M40-CLOSEOUT` |
| `M40_EPIC_CLOSEOUT_INDEPENDENT_REVIEW.md` | `a3f24ea8a5b1a07c6004e454627029b56c407f16` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_INDEPENDENT_CONFIRMATION.md` | `07efecc48f8a3575d73dd78e3379693d3dc3af6f` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_INDEPENDENT_CONSTITUTIONAL_ARCHITECTURE_REVIEW.md` | `9efbd6c5c3df7f638e27a4424d9e01be449adba3` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_REVIEW_RESPONSE.md` | `2ff12489fdd7168fb1ab02238496b4bd178cb2aa` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_WP1_INDEPENDENT_CONFIRMATION.md` | `7730ca45c398c6e9557225be41accac906692c1a` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_WP1_INDEPENDENT_REVIEW.md` | `12e2c9342f3aa5222a5c4207ba30623d8b932f07` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_WP1_REVIEW_RESPONSE.md` | `2274d353a0218d4d26d45a939f6fa7bd2f473555` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_WP2_INDEPENDENT_CONFIRMATION.md` | `d297c711354f642cb98b9f66c9da476de1b0d5c3` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_WP2_INDEPENDENT_CONSTITUTIONAL_REVIEW.md` | `30f3539f12589bf19d6bfc6d0a1a4239dd09ffcf` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_WP2_REVIEW_RESPONSE.md` | `c619f86476d3816f63b62082bd10f8aad300cb9b` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_WP3_INDEPENDENT_CONSTITUTIONAL_REVIEW.md` | `d1009ebd97954f038e7de85579a9424f25eab82f` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_WP4_DECISION_LOG_RECONCILIATION.md` | `11aadb89b8c43bf5d3ff50e5372aa79e3b3cc16b` | `GOVERNANCE RECONCILIATION — OUTSIDE` | `X-M40-RECONCILIATION` |
| `M40_WP5_INDEPENDENT_CONFIRMATION.md` | `3f6ef073cee8357a7622e92626bee94340b96869` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M40_WP5_REVIEW_RESPONSE.md` | `be87fa535daec45ff31dc9d77a3b3f9c7d75f00c` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M40-CHAIN` |
| `M41_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` | `8c09beefdf2e1236e4f82d8c1801d38340aee1d9` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-ARCHITECTURE` |
| `M41_ARCHITECTURE_INDEPENDENT_REVIEW.md` | `d6b252fdfdb5578d3fa97dde07d05c8c5a6bafed` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-ARCHITECTURE` |
| `M41_ARCHITECTURE_PROPOSAL.md` | `7996ea640534aadebcccb1864055a503ed87844b` | `FROZEN ARCHITECTURE PROPOSAL — OUTSIDE` | `X-M41-ARCHITECTURE` |
| `M41_ARCHITECTURE_PROPOSAL_REVIEW_RESPONSE.md` | `5b8e453825c5af9666d7cd863ada28dc40c48588` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-ARCHITECTURE` |
| `M41_ARCHITECTURE_REQUIRED_CORRECTIONS_RESPONSE.md` | `1765c1cc0ca9888a22b6b8dcc69d285ce8b859d5` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-ARCHITECTURE` |
| `M41_WP1_CLOSEOUT.md` | `c16baaff939977c14f14bba9ab6ab09f71b611bf` | `LIFECYCLE CLOSEOUT — OUTSIDE` | `X-M41-WP1` |
| `M41_WP1_INDEPENDENT_CONFIRMATION.md` | `53a35b448d2e16b9425455cf3f3bcb0ca11108a2` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP1_INDEPENDENT_REVIEW.md` | `6b455b3e61e7b9f116257e189ad4b4a86389cc30` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP1_REQUIRED_CORRECTIONS_RESPONSE.md` | `e7f83602059748003fd4dff1f25b84e89a2ea98f` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP1_STAGE2_FINAL_INDEPENDENT_CONFIRMATION.md` | `949f3d089f84d8d4a86d403b8ad5e840c015b1e7` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP1_STAGE2_FINAL_REQUIRED_CORRECTIONS_RESPONSE.md` | `36e541c920bdb6c0d98cc12abf0175581b316023` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP1_STAGE2_FINAL2_INDEPENDENT_CONFIRMATION.md` | `b09d2d87133cef79fe624279bb31ac56766ce106` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP1_STAGE2_FINAL2_REQUIRED_CORRECTIONS_RESPONSE.md` | `2c1cd3f7657855710b5baea1427e5f6112d5dfdc` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP1_STAGE2_INDEPENDENT_CONFIRMATION.md` | `2f06c7c672f0e8e8efe6be518d209349dcd030f4` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP1_STAGE2_INDEPENDENT_REVIEW.md` | `6308e68c7222f205b9b6d5bda755abe32a716517` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP1_STAGE2_REQUIRED_CORRECTIONS_RESPONSE.md` | `9865c85dc5c8b487c256b88e5c11176dd50ad4fe` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP1` |
| `M41_WP2_ARCHITECTURE_CONFIRMATION.md` | `9869d46a9bc8b1b2b38a02fda5236076eb26cd33` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_ARCHITECTURE_CONFIRMATION_CORRECTIONS_RESPONSE.md` | `8f1decebb38c7d2d986eecd472dba505d66227e1` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_ARCHITECTURE_INDEPENDENT_REVIEW.md` | `f0cc6112b5197557906df56f1a861ba2fc75a21d` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_ARCHITECTURE_PROPOSAL.md` | `6c77d8786035c9d5f4b121fc3c08b3987dc3c670` | `FROZEN ARCHITECTURE PROPOSAL — OUTSIDE` | `X-M41-WP2` |
| `M41_WP2_FINAL_ARCHITECTURE_CONFIRMATION.md` | `96391f36aa5adbfa8dc5f590714c70a673efe508` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_REQUIRED_CORRECTIONS_RESPONSE.md` | `d6bd743d7ecea5d283abdaf252c0a4848b8afac5` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_STAGE_A_INDEPENDENT_CONFIRMATION.md` | `a9a1a334e6b4e263204c9e88a158300456f7a8b1` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_STAGE_A_INDEPENDENT_REVIEW.md` | `044be2e57236c88dcb53d8fb42ade84ba07f91f9` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_STAGE_A_REQUIRED_CORRECTIONS_RESPONSE.md` | `97fa8df21e5733d5a78c825d9505e447a500f331` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_STAGE_B_INDEPENDENT_CONFIRMATION.md` | `3132d8bc6dfa8c826f5753ee45ce260f629fe05d` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_STAGE_B_INDEPENDENT_REVIEW.md` | `10f4601889d583dec349c5e5247e1584401f2637` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_STAGE_B_REQUIRED_CORRECTIONS_RESPONSE.md` | `f6e03b3965369a94420d193e49ef91abe8e1c4e1` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP2` |
| `M41_WP2_STAGE_C_ARCHITECTURE_PROPOSAL.md` | `2e8aa653b182ad8f5ec8454416711a7b926010a1` | `NON-FROZEN PROPOSAL; EMPTY SEMANTIC SCOPE — OUTSIDE` | `X-M41-WP2-STAGE-C` |
| `M41_WP2_STAGE_C_INDEPENDENT_ARCHITECTURE_REVIEW.md` | `01c37c600d09b1ea4d4f076c95c8a913263c2e71` | `NON-FROZEN LIFECYCLE EVIDENCE — OUTSIDE` | `X-M41-WP2-STAGE-C` |
| `M41_WP3_ARCHITECTURE_PROPOSAL.md` | `ecc651df2465c7a350d7fc71d3c63b6befde5532` | `APPROVED IMMUTABLE ARCHITECTURE PROPOSAL — OUTSIDE` | `X-M41-WP3` |
| `M41_WP3_CLOSEOUT.md` | `e715dbe5a6a5b3142d23bb8a2b5fe113fc88e10a` | `LIFECYCLE CLOSEOUT — OUTSIDE` | `X-M41-WP3` |
| `M41_WP3_INDEPENDENT_ARCHITECTURE_REVIEW.md` | `90a99aae63ebc5f51fb33412332cc100da6d3565` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP3` |
| `M41_WP3_STAGE_A_INDEPENDENT_REVIEW.md` | `cc474e1362a3ac9564bb3d7be3a0a3f9403bf26f` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP3` |
| `M41_WP3_STAGE_B_INDEPENDENT_CONFIRMATION.md` | `73fc7b94f7cf21d31ce8355b2905bdab49615ae8` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP3` |
| `M41_WP3_STAGE_B_INDEPENDENT_REVIEW.md` | `8c547fea4d3d726e4607b7e0820f65d9567eda7e` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP3` |
| `M41_WP3_STAGE_B_REQUIRED_CORRECTIONS_RESPONSE.md` | `d2b9ccf8b89b47ac17620ea3f55e0ea15b6a58a6` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP3` |
| `M41_WP4_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` | `8c7fcc48da39d63b759ac5017bc086c7d7826d50` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP4` |
| `M41_WP4_ARCHITECTURE_INDEPENDENT_REVIEW.md` | `12ccc9d6e1165615d290ec7917cc865f8a7b5fd9` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP4` |
| `M41_WP4_ARCHITECTURE_PROPOSAL.md` | `9e804c3cf05e6f81c52d24702a7df18ec12128a3` | `FROZEN ARCHITECTURE PROPOSAL — OUTSIDE` | `X-M41-WP4` |
| `M41_WP4_ARCHITECTURE_REQUIRED_CORRECTIONS_RESPONSE.md` | `b2622f3c1261d0cb4536202f308d709cb707afa6` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP4` |
| `M41_WP4_CLOSEOUT.md` | `727d352c61ba3db0e4a340437b829ae94d5b230f` | `LIFECYCLE CLOSEOUT — OUTSIDE` | `X-M41-WP4` |
| `M41_WP4_STAGE_A_INDEPENDENT_CONFIRMATION.md` | `4c5d436a8f78079954e80dbeb36f615698ad9524` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP4` |
| `M41_WP4_STAGE_A_INDEPENDENT_REVIEW.md` | `1f3a30be2c42e86047a37fa5b202caa6417164fe` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP4` |
| `M41_WP4_STAGE_B_INDEPENDENT_REVIEW.md` | `5fd5d9c2ca280e53ef1f1be501459cc5016c6bd8` | `LIFECYCLE EVIDENCE — OUTSIDE` | `X-LIFECYCLE`; `X-M41-WP4` |

Frozen status is established by `M39_EPIC_CLOSEOUT.md` blob
`d766779d2884d1504a38f43d3ddf7250f3d1877a`, `M40_EPIC_CLOSEOUT.md` blob
`f94503d38fc03248897aa91fcaae309af8ecaf2f`,
`M41_WP1_CLOSEOUT.md` blob
`c16baaff939977c14f14bba9ab6ab09f71b611bf`,
`M41_WP2_STAGE_A_INDEPENDENT_CONFIRMATION.md` blob
`a9a1a334e6b4e263204c9e88a158300456f7a8b1`,
`M41_WP2_STAGE_B_INDEPENDENT_CONFIRMATION.md` blob
`3132d8bc6dfa8c826f5753ee45ce260f629fe05d`,
`M41_WP3_CLOSEOUT.md` blob
`e715dbe5a6a5b3142d23bb8a2b5fe113fc88e10a`,
`M41_WP4_STAGE_A_INDEPENDENT_CONFIRMATION.md` blob
`4c5d436a8f78079954e80dbeb36f615698ad9524`, and
`M41_WP4_CLOSEOUT.md` blob
`727d352c61ba3db0e4a340437b829ae94d5b230f`.
The M41-WP3 closeout records Stage A as `APPROVED`, preserves it as immutable,
and freezes M41-WP3 as a complete corpus; it is not restated here as having an
artifact-specific confirmation that its lifecycle did not use.

The M40 closeout records M40-WP2 as complete with `8_ADMIT_2_REJECT` frozen,
M40-WP3 as complete and independently approved, and the earlier
stage-specific effectiveness text as historical after the later approval and
closeout satisfied those gates.

The evidence-completion disposition of each required member added across RC6.1
and RC6.2 is:

| Required owner-corpus member | Annualization Basis governing contract | Effect on proposed ownership | Effect on corpus determination | Effect on proposed `G-4` |
| --- | --- | --- | --- | --- |
| `M40_WP2_Canonical_Market_Measure_Vocabulary_Admission_Review.md` | `ABSENT` — it admits and governs canonical semantic meanings and sole-owner mappings, but no Annualization Basis contract tuple | `UNCHANGED` — seven admitted Market Intelligence concepts are consistent with the proof; the one governance-owned predicate neither competes for nor transfers Annualization Basis ownership | `CHANGED — REQUIRED MEMBER NOW INSPECTED AND RECORDED` | `UNCHANGED — OPEN` |
| `M40_WP3_CANONICAL_GLOSSARY_SYNCHRONIZATION.md` | `ABSENT` — it synchronizes admitted meanings into effective shared canonical vocabulary, but no Annualization Basis contract tuple | `UNCHANGED` — it preserves the frozen owner mappings and establishes no competing Annualization Basis owner | `CHANGED — REQUIRED MEMBER NOW INSPECTED AND RECORDED` | `UNCHANGED — OPEN` |
| `M41_WP1_CANDIDATE_VOCABULARY_AND_OWNERSHIP_REGISTER.md` | `ABSENT` — it establishes owner-governed vocabulary and dependency/window constraints, but no Annualization Basis contract tuple | `UNCHANGED` — consistent with Market Intelligence ownership; not used to derive ownership from absence | `PRESERVED — REQUIRED MEMBER INSPECTED AND RECORDED IN RC6.1` | `UNCHANGED — OPEN` |
| `M41_WP2_STAGE_A_CANDIDATE_VOCABULARY_REGISTER.md` | `ABSENT` — its Subject/Manifest vocabulary and ownership dispositions establish no Annualization Basis contract tuple | `UNCHANGED` — no competing owner or ownership transfer relevant to Annualization Basis | `PRESERVED — REQUIRED MEMBER INSPECTED AND RECORDED IN RC6.1` | `UNCHANGED — OPEN` |
| `M41_WP3_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md` | `ABSENT` — it establishes exact-rule and dependency constraints and rejects ambient/default `252`, but publishes no Annualization Basis contract tuple | `UNCHANGED` — its Market Intelligence calculation-rule allocation is consistent with, but does not replace, the four-proof determination | `PRESERVED — REQUIRED MEMBER INSPECTED AND RECORDED IN RC6.1` | `UNCHANGED — OPEN` |
| `M41_WP4_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md` | `ABSENT` — its Result/provenance/dependency surfaces establish no Annualization Basis contract tuple | `UNCHANGED` — no competing owner or ownership transfer relevant to Annualization Basis | `PRESERVED — REQUIRED MEMBER INSPECTED AND RECORDED IN RC6.1` | `UNCHANGED — OPEN` |

The search evaluated every candidate artifact by role and by the complete §8.6
field set, not by filename or keyword alone. A case-insensitive whole-corpus
scan for `annualization`, `annualisation`, `annualized`, `annualised`,
`per annum`, year-basis and day-count variants, `365`, `365.25`, `252`, and
session-count variants found no Annualization Basis declaration. M40-WP2's
role-and-field inspection found binary admissions and rejections, semantic and
dependency-version composition, and sole-owner mappings, but no Annualization
Basis tuple. M40-WP3's role-and-field inspection found synchronization of those
meanings into canonical vocabulary, but no Annualization Basis tuple. The
material temporal/basis surfaces are M41-WP3 Stage A §4 Component C and §7.5,
and M41-WP3 Stage B §5.1. Stage A classifies exact method/calendar rules and
rejects the ambient `252` assumption; Stage B's `session count` is a
method-declared duration amount using an exact named calendar dependency. None
of these surfaces supplies a governed Annualization Basis contract kind,
identifier, immutable version, or canonical value bytes. This agrees with
frozen M43-WP4 §6.7 and frozen M44-WP1 §4.4, each of which records that no such
instrument exists. No owner-corpus surface was left unsearched. No excluded
artifact is used as substantive absence evidence: each exclusion rests only on
the constitutional role and exact authority recorded in the boundary ledger,
and all 79 artifacts are classified.

#### Existing-contract assessment

No owner-corpus artifact supplies a candidate tuple to which dependency closure
could lawfully be applied:

| §8.6 requirement | Owner-corpus result |
| --- | --- |
| M43-WP2 §8.1 Dependency key | `ABSENT` |
| Exact owning domain | `MARKET INTELLIGENCE — PROVED`, but no published dependency declaration |
| Exact existing governed dependency contract kind | `ABSENT` |
| Exact dependency identifier | `ABSENT` |
| Exact immutable dependency version | `ABSENT` |
| Canonical value bytes required by M43-WP4 §6.7 | `ABSENT` |
| Complete M43-WP2 §8.2 transitive closure | `NOT FORMABLE — NO CANDIDATE TUPLE` |
| Caller-override rejection on an existing candidate | `NOT FORMABLE — NO CANDIDATE` |
| Version non-substitutability on an existing candidate | `NOT FORMABLE — NO CANDIDATE` |

The canonical vocabulary admission and synchronization in M40-WP2 and
M40-WP3, and the ordinary calendar references and session-count semantics in
M41-WP3, do not supply the missing Annualization Basis dependency and are
rejected as substitutes. No field is inferred, and no M44-authored requirement
is treated as an existing owner-domain publication.

#### Proposed `G-4` record and requirement statement

The exhaustive result satisfies the `OPEN` branch of §8.7.

**Proposed terminal state:** `G-4 OPEN`.

**Proved exact owner:** `Market Intelligence`.

**Exact missing element:** an exact existing Market Intelligence-governed
Annualization Basis calculation-dependency contract kind, together with the
exact dependency identifier, immutable version, and canonical value bytes that
the owner publishes.

Before any Annualization Basis can be declared or consumed, a future,
separately authorized Market Intelligence governance instrument must supply:

1. the exact owner, `Market Intelligence`;
2. an exact governed dependency contract kind published in that owner's
   corpus;
3. an exact stable identifier under that contract kind;
4. an exact immutable version; and
5. exact canonical value bytes.

This requirement statement is not that instrument, does not name or create its
contract kind, and does not define annualization arithmetic. The optional
semantic-information checklist quoted in §8.7 remains addressed only to the
future normative specification identified there and is not added to this
requirement.

`D-2b` remains behind `D-1`, the confirmed and frozen WP5 determination, `D-7`,
and every other separately governed prerequisite. `D-7` remains the absent
owner-domain instrument and could be discharged only if Market Intelligence
later acts under separately granted authority. WP5 and D-7 are necessary in
the open case and never sufficient by themselves. `D-3` consumes this outcome
only if an attribution method requires annualization. `G-3` remains
`OPEN — PARTIAL`; the §12.1.1 checkpoint remains `NOT DISPOSITIONED`; and WP6
and WP7 remain unauthorized.

The proposed ownership conclusion and `G-4 OPEN` state have no constitutional
effect until §13 completes.

#### Documentary vectors

Every vector below is documentary only. `V-POS-1` and the governed side of
`V-BND-1` are `ARTIFICIAL`, `NON-EFFECTIVE`, and **incapable of passing the
future gate**, because the owner corpus presently supplies no conforming kind.

| Vector | Documentary input | Required result |
| --- | --- | --- |
| `V-POS-1` | Shape containing `<stable dependency key>`, `owner=Market Intelligence`, `<exact owner-published contract kind>`, `<exact identifier>`, `<exact immutable version>`, `<exact canonical value bytes>`, complete deterministic transitive closure, caller-override rejection, and no version substitution | Illustrates the complete §8.6 shape only; admits nothing and closes no gate |
| `V-BND-1` | Side A: an artificial, owner-published, exact-version dependency whose governed derived session-count value is `252`; Side B: ambient literal `252` | Side A remains non-effective pending a real owner publication and closure; Side B is rejected unconditionally |
| `V-NEG-1` | Ambient or unversioned `252`, `365`, or `365.25` | Reject; no default or inference |
| `V-NEG-2` | Caller supplies or overrides the Annualization Basis | Reject under M43-WP2 and M43-WP4 |
| `V-NEG-3` | Dependency version is a range, alias, `latest`, compatible selector, or mutable reference | Reject as non-exact and substitutable |
| `V-NEG-4` | Provider field, library frequency, configuration value, or live calendar service is presented as the dependency | Reject; origin or implementation does not establish a governed kind |
| `V-NEG-5` | Portfolio Intelligence, Ledger & Accounting, Asset Foundation, a caller, or a shared owner is substituted for Market Intelligence | Reject as wrong-owner or inferred ownership |
| `V-NEG-6` | This requirement statement, an M44 label, or an illustrative example is presented as the owner-domain contract kind | Reject; M44 authors no kind |
| `V-DC-1` | Direct dependency reference does not resolve to one immutable governed version | Reject closure |
| `V-DC-2` | Owner or contract kind differs from controlling frozen authority | Reject closure |
| `V-DC-3` | A transitive dependency declaration is not itself closed | Reject closure |
| `V-DC-4` | Closure contains a cycle or repeated node | Reject closure |
| `V-DC-5` | Closure contains a range, alias, `latest`, provider identifier, or ambient resolution | Reject closure |
| `V-DC-6` | Two independent traversals produce different exact dependency tuples | Reject closure |

#### Coverage ledger and failure scan

| Requirement surface | Applied-record coverage |
| --- | --- |
| §§1–5 authority, identity, extension basis, ambiguity, and invariants | boundary lock; evidence manifest; hypothesis record; four-proof matrix; proposed record non-effect statement |
| §6 admissible and inadmissible evidence | evidence manifest and explicit non-reliance statement |
| §7 ownership proof | hypothesis record and four-proof ownership matrix |
| §§8.1–8.4 / WP5.1–WP5.2 | boundary lock, manifest, hypotheses, and proved ownership conclusion |
| §§8.5–8.6 / WP5.3–WP5.4 | 79-artifact M39–M41 boundary derivation; exact 17-member owner-corpus inventory; exact 62-member exclusion ledger with per-artifact blobs, roles, and frozen-authority keys; exhaustive role-and-field search of every included member; per-artifact disposition; candidate rejection; and five-part assessment |
| §8.7 / WP5.4–WP5.5 | proposed `G-4 OPEN` record, exact missing element, requirement statement, and consequences |
| §9 items 1–6 | baseline commit, blobs, frozen diff scope, manifest, proof matrix, and hypothesis assessment |
| §9 items 7–9 | owner-corpus boundary, exhaustive assessment, and complete `OPEN` evidence |
| §9 items 10–11 | `V-POS-1`, `V-BND-1`, `V-NEG-1`–`V-NEG-6`, and `V-DC-1`–`V-DC-6` |
| §9 item 12 | this coverage ledger |
| §10.1 | not reached: one owner is proved; subsection remains unchanged |
| §10.2 | not reached: the exact frozen corpus is established and exhaustively inspected; subsection remains unchanged |
| §10.3 and §13 / WP5.6 | not yet applicable; independent review, any required correction, renewed review, confirmation, and freeze remain pending |
| §11 failure conditions | no implicit owner, inadmissible affirmative evidence, presumptive corpus, field conflation, ambient value, caller override, version substitution, authored kind, false closure, checkpoint disposition, or downstream authority is used; effectiveness remains withheld pending review |
| §12 required outputs | all branch-applicable items 1–11 are contained above; item 12 accrues only through §13 |
| §§14–15 exclusions and conformance | all authority exclusions remain unchanged; the candidate result is documentary and non-effective |
| Frozen M44-WP1 §4.4 items 1–7 | four proofs; corpus search; `OPEN` evidence; ambient and `252` boundary vectors; M44-kind rejection; independent confirmation pending under §13 |
| Frozen M44 Architecture §11 required-test categories | dependency closure `V-DC-1`–`V-DC-6`; version rejection `V-NEG-3`; caller rejection `V-NEG-2`; ambient constants `V-NEG-1`; governed/ambient `252` boundary `V-BND-1`; M44-kind rejection `V-NEG-6` |

The applied record therefore completes frozen WP5.1 through WP5.5 and is
eligible to enter WP5.6. Eligibility is not approval, confirmation, freeze, or
effectiveness.

## 13. Independent constitutional lifecycle

A determination that stops under §10.1 or §10.2 MUST NOT enter this lifecycle.
On either branch, WP5.6 does not begin and no independent review,
confirmation, or freeze of a candidate terminal determination occurs.

Only after WP5.5 completes may a proposed determination enter WP5.6. A proposed
ownership conclusion or `G-4` terminal state then has no constitutional effect
until:

1. the complete record satisfies every pre-lifecycle requirement in §§7–12;
   §12 item 12 accrues only through steps 2–6 below and is not a prerequisite
   for reviewability;
2. an author-independent constitutional review evaluates the whole record
   against the frozen corpus and this specification;
3. every blocking finding is corrected;
4. each correction receives renewed author-independent review;
5. independent confirmation records unresolved blocking findings `NONE`; and
6. the separately authorized M44-WP5 freeze records the effective result.

Review and confirmation MUST NOT substitute for missing ownership proof,
incomplete corpus evidence, or an unformable terminal state. A reviewer may
confirm only what the evidence proves.

Only after a conforming M44-WP5 result is independently confirmed and frozen
may the separately governed §12.1.1 checkpoint be reached. This specification
does not evaluate or disposition that checkpoint. Under the already frozen
`G-3 OPEN — PARTIAL` state, the frozen checkpoint rule remains “Stop, or
formally re-scope”; WP6 and WP7 remain unauthorized.

## 14. Explicit exclusions and non-authorization

This specification does not:

- make Annualization Basis ownership effective by self-declaration; the proved
  candidate conclusion in §12.1 remains a proposal unless and until §13
  completes;
- create shared ownership or transfer source calendar meaning;
- disposition `G-3`, `G-4`, `G-5`, or §12.1.1. A proposed `G-4` terminal state
  that a pre-confirmation candidate of this deliverable carries under §8.7 is
  a proposal only, and has no dispositional effect unless and until §13 is
  complete. Once confirmed, this deliverable is frozen on confirmation under
  frozen M44 Architecture §11 M44-WP5 and is not edited in place;
- define annualization arithmetic or select an annualization basis, factor,
  market, calendar, session count, default, or fallback;
- author, name, register, extend, version, or serialize an owner-domain
  governance instrument or dependency contract;
- create canonical value bytes;
- create or authorize a calculation-dependency declaration, Method Version,
  applicability rule, manifest entry, result contract, or Component G binding;
- authorize implementation, source code, runtime behavior, persistence,
  schemas, migrations, APIs, transport, UI, provider access, production
  methods, or executable validation;
- authorize M44-WP6, M44-WP7, M43-WP6, M43-WP7, M43-WP8, D-2b, D-3, or D-7;
- modify, supersede, reinterpret, or thaw a frozen artifact; or
- close M44-WP5 or the M44 milestone.

## 15. Conformance and final normative statement

A determination conforms to this specification only if:

- every planning constraint is preserved;
- the authority ceiling in this specification is unchanged;
- all frozen artifacts remain byte-identical;
- terminology and terminal states remain constitutionally consistent;
- every ownership proposition is supported exclusively by admissible evidence;
- all stopping and failure conditions are applied without default, inference,
  repair, or fallback;
- all required repository evidence and constitutional outputs are present;
- when and only when WP5.6 is lawfully reached, independent review and
  confirmation complete with unresolved blocking findings `NONE`; and
- no implementation or downstream authority is introduced.

This corrected RC6.3 candidate preserves the constitutional method and
incorporates its application through frozen WP5.5 into the sole WP5
deliverable. It proposes Market Intelligence as the proved owner and proposes
`G-4 OPEN` on the complete owner-corpus absence record in §12.1. Neither
proposal is effective before §13 completes. It grants no implementation
authority.
