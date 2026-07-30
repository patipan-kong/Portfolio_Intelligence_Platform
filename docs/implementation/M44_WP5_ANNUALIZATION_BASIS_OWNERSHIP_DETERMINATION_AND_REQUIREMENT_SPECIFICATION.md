# M44-WP5 — Annualization Basis Ownership Determination and Requirement Specification

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics

**Work package:** M44-WP5 only

**Candidate:** `RC4` — corrected after the independent constitutional reviews
recorded in §2.2

**Artifact class:** Architectural deliverable, in the sense frozen M44
Architecture §11 M44-WP5 uses under **Architectural deliverables**

**Artifact identity:** The single M44-WP5 determination and requirement
specification allocated by frozen M44 Architecture §11 and §13.1

**Ownership-determination and requirement-specification authority:** `LIMITED
TO THE FROZEN M44 ARCHITECTURE §8.4 AND §11 ALLOCATION`

**Ownership determined by this RC4 candidate:** No

**G-3 disposition authority:** `NONE`

**G-4 disposition authority exercised by this RC4 candidate:** `NONE`

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

This corrected RC4 candidate does not yet apply that process to select, name,
assign, infer, or imply an owner. It does not decide any ownership hypothesis.
It does not search any presumptive owner's corpus as though ownership had
already been proved. It does not establish a terminal state for `G-4`. Any
later applied determination and any resulting requirement statement MUST be
incorporated into this same file; no separate WP5 determination,
requirement-specification, or constitutional-process artifact is permitted.

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
requirement specification within the frozen allocation. This RC4 candidate
does not perform or confirm the determination. The allocation is not authority
to author an owner-domain governance instrument, disposition a gate or
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
- the `RC3` candidate of this deliverable was independently reviewed and
  returned `NOT APPROVED`, and this `RC4` candidate is the correction of that
  review's findings; and
- the `RC3` independent constitutional review is not itself filed at a
  repository path. Until it is filed, the review chain for this deliverable
  MUST NOT be treated as complete, and this candidate MUST NOT be treated as
  reviewed to conclusion, independently confirmed, or frozen.

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

No owner name is supplied by this specification. Market Intelligence MUST be
treated only as the first hypothesis required by frozen OQ-3; it MUST be proved
or rejected under the same standard as any other materially supported
hypothesis.

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
      without a proved owner;
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
11. A boundary example distinguishing an already owner-published,
    version-bound derived session count equal to `252` from ambient `252`,
    without admitting either by example. **If §8.6 is lawfully reached,** the
    example carries both sides. On the §10.1 branch, where no owner is proved,
    the item is discharged by the ambient-`252` rejection alone; the
    owner-published side MUST NOT be supplied, because no proved owner exists
    to attribute a publication to.
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
- no Component G binding is formable; and
- WP6 and WP7 remain unauthorized.

The two frozen readings of how §12.1.1 relates to an unestablished gate state,
preserved in §4 and set out in §10.1, apply to this branch on the same terms
and are neither ranked nor resolved here.

Sections §8.7 and §13 — the frozen WP5.4 terminal-state proposal, frozen WP5.5,
and frozen WP5.6 — MUST NOT begin. The four frozen WP5.4 tests reached inside
§8.6 — M43-WP2 §8.2 closure, the distinct M43-WP4 §6.7 information,
caller-override rejection, and version non-substitutability — yield no terminal
state on this branch.

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
   fail-closed statement that ownership was not proved. This specification
   supplies neither conclusion.
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

- determine, assign, presume, or imply ownership of the Annualization Basis;
- create shared ownership or transfer source calendar meaning;
- disposition `G-3`, `G-4`, `G-5`, or §12.1.1. A proposed `G-4` terminal state
  that a later candidate of this deliverable, before confirmation and freeze,
  may carry under §8.7 is a proposal only, and has no dispositional effect
  unless and until §13 is complete. Once confirmed, this deliverable is frozen
  on confirmation under frozen M44 Architecture §11 M44-WP5 and is not edited
  in place; "later candidate" means a pre-confirmation candidate only;
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

This corrected RC4 candidate establishes the constitutional method for
determining Annualization Basis ownership within the sole frozen WP5
deliverable. It deliberately leaves ownership and `G-4` unresolved. It grants
no implementation authority.
