# M44-WP5 — Annualization Basis Ownership Determination Specification

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics

**Work package:** M44-WP5 only

**Artifact class:** Normative constitutional-process specification

**Normative scope:** Ownership-determination process only

**Ownership determined by this specification:** No

**G-3 disposition authority:** `NONE`

**G-4 disposition authority exercised by this specification:** `NONE`

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

This specification defines the constitutional process by which a later
M44-WP5 determination must attempt to prove the owner of the Annualization
Basis. It defines:

- the evidence that may and may not participate in the determination;
- the required order of analysis;
- the proof standard;
- the conditions that stop the determination;
- the conditions that make a proposed determination fail;
- the repository evidence that must support a proposed determination; and
- the constitutional outputs required before any proposed determination may
  become effective.

This specification does not apply that process to select, name, assign, infer,
or imply an owner. It does not decide any ownership hypothesis. It does not
search any presumptive owner's corpus as though ownership had already been
proved. It does not establish a terminal state for `G-4`.

The governing posture is determination-only and fail-closed. Consumption of an
Annualization Basis by Portfolio Analytics does not transfer ownership to
Portfolio Intelligence. Similarity to a calendar, market session count,
provider field, configuration value, library facility, or current repository
implementation does not prove ownership.

## 2. Authority and constitutional basis

This specification is bounded by, and must be read with:

- the frozen [M44 Architecture and Implementation
  Plan](../implementation/M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md),
  especially §§3.1, 4.4, 5–6, 8.4, 10, 11 M44-WP5, 12.1.1, 12.3, 12.5,
  13.1, 16.2, and 17 OQ-3;
- the frozen [M44 Architecture Freeze
  Record](../implementation/M44_ARCHITECTURE_FREEZE_RECORD.md);
- the frozen [M44-WP1 Inherited Gate Inventory and Closure
  Register](../implementation/M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
  §4.4;
- frozen [M43-WP2 Portfolio Measure Definition, Method Version, and
  Applicability Contract
  Specification](../implementation/M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md)
  §§8.1–8.2;
- frozen [M43-WP4 Constitutional Scope and Implementation
  Plan](../implementation/M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md)
  §§5.2 and 6.7; and
- the complete and frozen M44-WP5 planning-governance corpus:
  [RC3 plan](../implementation/M44_WP5_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md),
  [RC1 review](../implementation/M44_WP5_RC1_CONSTITUTIONAL_ARCHITECTURE_REVIEW.md),
  [RC2 review](../implementation/M44_WP5_RC2_CONSTITUTIONAL_ARCHITECTURE_REVIEW.md),
  [RC3 review](../implementation/M44_WP5_RC3_CONSTITUTIONAL_ARCHITECTURE_REVIEW.md),
  [independent
  confirmation](../implementation/M44_WP5_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md),
  [planning freeze
  record](../implementation/M44_WP5_PLANNING_FREEZE_RECORD.md), and
  [planning
  closeout](../implementation/M44_WP5_PLANNING_CLOSEOUT.md).

The planning-governance corpus supplies architectural intent and constraints.
It remains non-normative and immutable. This specification does not convert
any planning statement into an ownership result and does not amend or
reinterpret any frozen statement.

The authority exercised here is limited to specifying a determination
process. It is not authority to perform or confirm the determination, author an
owner-domain governance instrument, disposition a gate or checkpoint, or
authorize downstream work.

## 3. Normative language and process-local terms

`MUST`, `MUST NOT`, `REQUIRED`, `SHALL`, and `SHALL NOT` are normative within
the process scope of this specification.

The following terms are process-local descriptions only. They do not create
governed business vocabulary, terminal states, contract kinds, identifiers, or
repository artifact classes:

- **determination record:** the later constitutional record that applies this
  specification;
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

The active §12.1.1 checkpoint is not reached on that branch because M44-WP5
has not completed, confirmed, or frozen. The frozen checkpoint's
unestablished-state row remains a governing constraint on any future
checkpoint evaluation; it is not a checkpoint disposition performed by this
specification.

A defect in the attempted M44-WP5 determination and an ambiguity in frozen
architecture are distinct constitutional matters. A determination record MUST
identify each precisely and MUST NOT silently convert one into the other. This
specification creates no remedy or amendment authority for either.

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
10. Every missing, ambiguous, conflicting, inaccessible, stale, or
    unbounded evidentiary condition fails closed.
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
7. **Constitutional review evidence.** Filed author-independent review,
   corrections where required, renewed review, and independent confirmation
   with unresolved blocking findings `NONE`.

An evidence item MUST be assessed at its frozen meaning. Citation does not make
an artifact relevant; the cited text must state the proposition for which it
is offered.

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
  frozen evidence would reach the same ownership conclusion.

The proof is conjunctive. A missing, circular, ambiguous, conflicting, or
inference-dependent proposition means that ownership is not proved. Strength
in one proposition cannot compensate for failure in another.

No owner name is supplied by this specification. Market Intelligence MUST be
treated only as the first hypothesis required by frozen OQ-3; it MUST be proved
or rejected under the same standard as any other materially supported
hypothesis.

## 8. Ordered determination workflow

The workflow is strictly sequential.

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
2. Frozen M43-WP2 §8.2 transitive closure.
3. Frozen M43-WP4 §6.7 owner-published information:
   - exact owner;
   - existing governed contract kind;
   - identifier;
   - immutable version; and
   - canonical value bytes.

No field may be inferred from another list. No missing field may be supplied by
M44. Every version MUST be immutable and exact; no substitution is permitted.

### 8.7 Proposed constitutional outcome

After a proved owner and complete corpus assessment, the later determination
record may propose exactly one of the two frozen `G-4` terminal states:

- `CLOSED` only when an exact existing owner-published governed contract kind
  satisfies every requirement in §8.6 unchanged; or
- `OPEN` only when the exhaustive search proves that no conforming exact
  existing kind is present and the record names the exact missing element and
  the proved exact owner.

A proposed `OPEN` record MUST state exactly what a future owner-domain
governance instrument would have to supply and the consequences for D-2b and
D-7. That statement is a requirement statement only. It MUST NOT name,
author, register, extend, version, serialize, or impersonate the missing
instrument.

No proposed state is effective until §13 is complete.

## 9. Required repository evidence

A determination record is constitutionally reviewable only when it contains
all applicable evidence below:

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
   absence evidence, bounded future-instrument requirements, and consequences
   for D-2b and D-7.
10. Documentary negative evidence rejecting:
    - ambient or unversioned `252`, `365`, and `365.25`;
    - caller override;
    - version substitution, ranges, aliases, and “latest”;
    - wrong-owner and provider-derived claims;
    - an M44-authored contract kind; and
    - a requirement statement presented as a contract kind.
11. A boundary example distinguishing an already owner-published,
    version-bound derived session count equal to `252` from ambient `252`,
    without admitting either by example.
12. A coverage ledger mapping every rule in this specification and every
    frozen M44-WP1 §4.4 evidence item to at least one cited record section.
13. Filed author-independent constitutional review, all required corrections,
    renewed review where applicable, and independent confirmation with
    unresolved blocking findings `NONE`.

Any illustrative example not backed by an exact existing owner-published
contract MUST be marked `ARTIFICIAL` and `NON-EFFECTIVE`, and MUST state in
plain language that it cannot establish conformance or pass dependency
closure. Those documentary markings are non-governed and cannot satisfy
M43-WP2 §8.2.

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
- §§8.5 through 8.7 MUST NOT begin;
- no `G-4` terminal state is proposed;
- M44-WP5 does not complete, confirm, or freeze;
- the §12.1.1 checkpoint is not reached;
- no Component G binding is formable; and
- WP6 and WP7 remain unauthorized.

The record may identify a frozen-architecture ambiguity, but it MUST NOT
resolve it or prescribe an amendment. Any constitutional correction requires
separate authority under the frozen governance process.

### 10.2 Repository proof incomplete

After ownership is proved, the process MUST stop without proposing a `G-4`
terminal state when:

- the proved owner's frozen corpus boundary cannot be established;
- the corpus is inaccessible or cannot be searched exhaustively;
- artifact identity or frozen status cannot be verified;
- search results cannot distinguish absence from an unsearched surface;
- an apparent match depends on a mutable, ranged, aliased, provider, or ambient
  value; or
- required owner-published fields or canonical bytes cannot be verified and
  corpus completeness is also unproved.

This stop does not undo a constitutionally proved ownership conclusion, but it
prevents completion of the M44-WP5 terminal-state determination.

### 10.3 Constitutional review stop

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

Application of this specification MUST produce one bounded determination
record, not an implementation artifact, operating procedure, submission
package, or owner-domain decision record. Within that record, the following
sections are required:

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
12. **Independent governance evidence** — filed review and confirmation
    required by §13.

These are required sections of the bounded determination record. This
specification does not authorize creation of additional packages, procedures,
contracts, registries, APIs, schemas, fixtures, source files, or decision
records.

## 13. Independent constitutional lifecycle

A proposed ownership conclusion or `G-4` terminal state has no constitutional
effect until:

1. the complete record satisfies §§7–12;
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
- disposition `G-3`, `G-4`, `G-5`, or §12.1.1;
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
- independent review and confirmation complete with unresolved blocking
  findings `NONE`; and
- no implementation or downstream authority is introduced.

This specification establishes the constitutional method for determining
Annualization Basis ownership. It deliberately leaves ownership unresolved.
It grants no implementation authority.
