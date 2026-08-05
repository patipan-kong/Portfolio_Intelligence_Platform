# Governance Handbook

> Status: `DRAFT`

This handbook is explanatory repository documentation. It describes the
governance model evidenced by the completed Asset Foundation milestone and
provides a map for reading the canonical records. It is not itself a
constitutional artifact, governance record, allocation, authorization,
implementation specification, repository decision, or runtime permission.

## 1. Purpose

The purpose of this handbook is to explain how repository governance creates,
limits, records, and closes bounded acts. It is intended to help a new AI or
human contributor understand why a planning record, an evidence record, a
frozen artifact, and an implementation document have different roles.

This handbook creates no authority. It does not amend or interpret the
constitutional corpus, allocate a work package, authorize implementation,
release software, reopen a frozen milestone, or replace a canonical source.
The [AI Rules](AI_RULES.md) is the operational handbook for AI work; this
document explains the governance concepts that those operating rules require an
AI to keep separate.

The following labels are used deliberately throughout the handbook:

- **Constitutional requirement** means a requirement stated by the applicable
  constitutional or frozen governing source.
- **Governance evidence** means a record of an act, determination, identity, or
  limitation. Evidence does not enlarge the authority of the act it records.
- **Repository convention** means an established way of organizing or
  performing repository work. A convention is not constitutional authority
  merely because it is useful or repeated.
- **Recommended practice** means explanatory guidance in this handbook. It is
  not a new requirement unless a canonical source separately makes it one.

## 2. Governance philosophy

The repository governance model is designed to make authority visible,
bounded, and reversible in its reasoning even when an artifact itself is
frozen. Its central ideas are related:

| Principle | Why it matters | Resulting boundary |
| --- | --- | --- |
| **Bounded authority** | An act should answer what is permitted, for which subject, and within which limits. | Authority does not spill from one package, owner, artifact, or lifecycle stage into another. |
| **Explicit authority** | A plan or intention can describe a future act without granting permission to perform it. | Authority must be stated by a competent applicable source; silence and convenience are not permission. |
| **Additive governance** | Later records should make the history more complete rather than make an earlier history look cleaner. | A correction, re-review, or later pass supplements an earlier finding; it does not silently erase a `FAIL` or a blocker. |
| **Evidence continuity** | A conclusion is trustworthy only when a reader can follow its prerequisite acts and stated limits. | Review, correction, confirmation, identity, freeze, release, and closeout evidence remain traceable as a chain. |
| **Fail-closed reasoning** | An absent prerequisite is safer when treated as unresolved than when filled by an assumption. | The next act is blocked or reported as not performed until the applicable source and evidence permit it. |
| **Exact identity preservation** | A frozen claim applies to a defined identity boundary, not to an artifact that merely looks semantically similar. | The source boundary and identity method must be preserved; a digest from one boundary is not silently treated as a digest from another. |

These principles explain why governance is more than a sequence of labels. A
record that says `CONFIRMED` can establish a bounded confirmation
determination, but it does not become a freeze record merely because freeze is
the next item in a roadmap. A record that says `FROZEN` can preserve an exact
corpus, but it does not become a runtime release. Each act carries its own
scope, competence, evidence, and non-effects.

## 3. Constitutional sources

Not every repository document is a constitutional source. The categories below
describe the question a document answers; they are not a universal ranking and
do not allow a handbook to promote one category into another. The applicable
source, corpus, scope, and express limitations control.

| Source category | Primary purpose | Authority boundary |
| --- | --- | --- |
| **Frozen planning** | Defines a bounded planned shape, dependency structure, sequence, exclusions, and milestone scope. | Planning can be ratified or frozen while still granting no implementation, runtime, allocation, or authorization authority when the source says so. |
| **Implementation artifacts** | State a technical, documentary, or normative candidate within the assigned scope. | A candidate may be reviewed, identity-validated, frozen, and later released or closed; candidate status alone does not authorize runtime or downstream use. |
| **Governance evidence** | Records allocation, authorization, review, correction, confirmation, identity, freeze, release, closeout, or another bounded act. | The record is evidence of the act and its limits. It does not create authority beyond the source-stated act. |
| **Repository conventions** | Explain how contributors navigate, edit, verify, preserve, and hand off repository work. | Conventions guide execution and safety. They do not silently become constitutional requirements. |
| **Engineering documents** | Provide architecture, design principles, decisions, domain boundaries, and implementation context. | They are technical sources for technical questions. They do not independently grant governance or runtime authority merely by describing a desired design. |
| **Handbook documentation** | Explains how to read the other categories and collaborate around them. | Handbooks are guidance and navigation. They create no authority and cannot replace a canonical artifact. |

The [Constitutional Precedent Index](../governance/CONSTITUTIONAL_PRECEDENT_INDEX.md)
is a useful navigation layer, but its own status is non-authoritative. A
reader must follow its links to the source opinion or adoption record for any
interpretive content and preserve the source's corpus and limitations.

## 4. Governance lifecycle

The current repository model treats governance as a set of distinct acts. A
typical bounded path is:

```text
Planning -> Allocation -> Authorization -> Implementation
    -> Independent Review
    -> Correction -> Focused Re-review (when findings require it)
    -> Independent Confirmation
    -> Content-Identity Validation
    -> Freeze
    -> Release Attestation or Closeout
    -> Repository Synchronization -> Commit
```

The arrows describe relationships, not permission to perform the next act.
The applicable corpus can require a different sequence, omit an act, or define
additional acts. The following table explains the current repository model.

| Act | What it does | What it does not establish by itself |
| --- | --- | --- |
| **Planning** | Defines a proposed or frozen shape, scope, dependency, or sequence. | Allocation, authorization, implementation, release, runtime, or downstream permission. |
| **Ratification** | Records adoption of a defined planning corpus when the governing corpus provides for ratification. | Any authority outside the ratified planning scope, including implementation or runtime authority. |
| **Allocation** | Assigns a bounded work package and responsibility to a competent role. | Authorization to perform the work, or completion of the work. |
| **Authorization** | Permits a specified act within an explicit scope and subject to stated constraints. | Proof that the act was performed, reviewed, confirmed, frozen, released, or closed. |
| **Implementation** | Creates or changes the permitted candidate or normative artifact. | Independent review, correction acceptance, confirmation, identity validation, freeze, release, or runtime activation. |
| **Independent Review** | Evaluates the defined subject and records findings within the review boundary. | Confirmation, validation, freeze, release, closeout, or authority to implement. |
| **Correction** | Responds to a recorded finding within the permitted scope. | A passing review, confirmation, or permission to broaden the correction. |
| **Focused Re-review** | Re-examines a specified correction or limited issue. | A broader review, independent confirmation, freeze, release, or closeout. |
| **Independent Confirmation** | Records an independent determination within its stated boundary. | Content-identity validation, exact-byte freeze, release, closeout, or successor authority. |
| **Content-Identity Validation** | Validates the reproducible identity of exact content at a named boundary. | Exact-byte freeze, canonical supply, release, closeout, or implementation authority. |
| **Freeze** | Establishes the immutability boundary for the validated corpus and preserves its identity. | Release attestation, runtime release, downstream intake, or closeout. |
| **Release Attestation** | Records a package-specific release disposition after its stated predicates are satisfied. | Runtime release, production activation, downstream authorization, or authority over another owner domain. |
| **Closeout** | Concludes the specified lifecycle and records its final bounded state. | Successor allocation, successor authorization, runtime release, or new authority. |
| **Repository Synchronization** | Aligns repository files and handoff state with an intended record or completed act. | A constitutional act, identity validation, freeze, release, or closeout. |
| **Commit** | Records a repository snapshot in Git history. | Governance approval, allocation, authorization, freeze, release, or proof that an earlier working-tree claim was valid. |

The completed Asset Foundation records provide the repository precedents for
this model. The planning pair records planning-specific review, confirmation,
ratification, identity validation, freeze, and closeout without creating
implementation authority. The AF-WP3 record demonstrates that allocation and
authorization may be documented in one record when each remains a separate,
bounded decision. The AF-WP4 records demonstrate the later package path from
bounded documentary implementation through review, identity and freeze
evidence, and a package-specific release or closeout disposition.

Those precedents are corpus-bound. Repositories may define corpus-specific
variants, additional acts, or a permitted combined record. This handbook
explains the current repository model; it does not make every listed act
universal or authorize a next step.

## 5. Governance concepts

These concepts are used to read governance records consistently. They are
short explanations, not a replacement for the canonical records or the
repository [Glossary](../GLOSSARY.md).

| Concept | Meaning in this handbook |
| --- | --- |
| **Authority** | An explicit, bounded permission supplied by an applicable competent source or record. It can remain `NONE` after a governance act. |
| **Competence** | The role, scope, and independence basis that make an actor eligible to perform a defined act. Competence is not inferred from merely doing adjacent work. |
| **Scope** | The exact subject, files, package, corpus, act, and exclusions to which a record applies. |
| **Lifecycle** | The ordered or source-defined set of bounded acts and dispositions for a corpus or work package. |
| **Frozen artifact** | An artifact whose exact identity and immutability boundary have been established by the applicable freeze record. |
| **Normative artifact** | An artifact intended to state the governing, planning, architectural, or implementation content assigned to it. Its class does not by itself grant runtime authority. |
| **Governance evidence** | Additive documentation that records what act or determination occurred, its identity, and its limits. It is not automatically the authority it describes. |
| **Implementation candidate** | A proposed artifact under a bounded implementation scope and before any later review, identity, freeze, release, or closeout act. |
| **Repository convention** | A recurring repository practice for safe organization or workflow that remains distinct from a constitutional requirement. |
| **Constitutional interpretation** | A source-grounded, corpus-bound account of what an identified constitutional text requires, permits, leaves open, or excludes. |
| **Precedent** | An adopted interpretation with the applicable corpus, holdings, and limitations preserved. It does not automatically carry to a successor corpus. |
| **Release attestation** | A bounded governance disposition about a package's release profile after the relevant predicates are evaluated. |
| **Runtime release** | Operational activation, deployment, or production availability. It is a separate concern from a governance release attestation unless an applicable source expressly connects them. |

## 6. Evidence model

Authority answers what is permitted. Evidence answers what was recorded,
performed, evaluated, or identified. A complete governance history needs both,
but evidence does not enlarge the authority of the act it supports.

### Additive records and visible history

Governance records are additive. A later record should append a correction,
focused re-review, confirmation, identity result, freeze, release, or closeout
without silently rewriting the earlier record. A historical `FAIL`, blocker,
or unresolved finding remains part of the history even when a later bounded act
records a pass or resolves the finding.

### Review and correction chains

A review record explains the subject evaluated and the findings made. A
correction response explains how a permitted correction addressed a finding. A
focused re-review evaluates the correction or specified issue. These records
form a chain:

```text
review finding -> correction response -> focused re-review -> later determination
```

The chain makes the transition visible. It does not allow a later pass to be
backdated into the earlier review, and it does not allow a correction response
to claim that review, confirmation, or freeze already occurred.

### Confirmation, identity, and freeze evidence

- **Confirmation evidence** records an independent determination within a
  stated boundary. The absence of a finding is not confirmation unless the
  applicable record says that it is.
- **Identity evidence** identifies the exact path or corpus, the identity
  boundary used, the reproducible command or method, and the resulting digest,
  byte count, line count, or other recorded predicate. Working-tree bytes,
  Git-normalized content, staged content, and committed content are distinct
  possible boundaries; the source record controls which one matters.
- **Freeze evidence** names the exact frozen corpus and preserves the identity
  that was validated before the freeze act. Supporting governance records,
  indexes, and later explanatory handbooks are not silently added to the
  frozen corpus.

Historical evidence remains visible because it lets a future reader determine
what was known at each stage, which prerequisite was missing, and why a later
act was or was not permitted. Removing a failed record would make an apparent
pass impossible to audit and would undermine fail-closed reasoning.

## 7. Authority model

Authority is not a feeling that a next step is expected. It is a bounded
relationship from an applicable source and competent act to a defined subject.
The relationship can be narrow, conditional, or explicitly `NONE`; it does not
expand because a later task would be convenient.

| Distinction | Why the distinction matters |
| --- | --- |
| **Planning is not Authorization** | Planning explains what may be needed or intended. Authorization is the separate permission to perform a specified act. A frozen or ratified plan can still leave implementation and runtime authority at `NONE`. |
| **Allocation is not Authorization** | Allocation supplies competent scope and responsibility. Authorization supplies permission. Keeping them separate prevents a work-package description from becoming an unintended command to implement. |
| **Freeze is not Release** | Freeze protects the identity and immutability of a corpus. Release attestation evaluates a separate package-specific release profile. A frozen artifact can remain unreleased or blocked. |
| **Release Attestation is not Runtime Release** | A release attestation records a bounded governance disposition. Runtime release requires operational authority and execution conditions that a governance attestation does not supply by implication. |
| **Closeout is not Successor Authority** | Closeout records that the defined lifecycle ended. It does not allocate the next package, authorize a successor, or create a new owner-domain permission. |

The same reasoning applies to neighboring acts. Review does not become
confirmation, confirmation does not become identity validation, and a Git
commit does not become governance approval. Each authority claim must be
traced to the record that actually states it.

## 8. Constitutional interpretation

Constitutional interpretation is source-bound reasoning about an identified
corpus. This section describes a safe way to read such records; it is not a
new holding, adoption resolution, or interpretation of any particular
historical review.

### Source-first reasoning

Start with the applicable canonical source, its exact repository path or
identity, the relevant section, the corpus to which it applies, and its
express limitations. Read the source before relying on a summary, index,
workflow expectation, or downstream need. A navigation document can point to a
source but cannot extend it.

### Evidence-first reasoning

Separate four questions:

1. What does the governing source require, permit, or leave open?
2. What act or determination does the evidence record establish?
3. What exact scope and identity does that record cover?
4. What non-effects or prerequisites does the record state?

The answer should not treat a proposed act, a future deliverable, a missing
record, or an adjacent status as proof that the act occurred.

### No invention

Do not invent an actor, board, authority, status, evidence item, identity,
exception, or lifecycle event to make the sequence appear complete. Silence is
not permission. If the source does not establish the required predicate, the
truthful result is unresolved, not performed, blocked, or another source-stated
disposition.

### Corpus-bound interpretation

An interpretation or adopted precedent applies only to the corpus, text, and
limitations identified by its source. A different or successor corpus may need
a new competent interpretive act. Similar wording, repository proximity, or a
shared work-package name does not transfer precedent automatically.

### Convention versus constitutional requirement

Repository instructions, contribution guidance, engineering principles, and
handbook recommendations can make work safer and more consistent. They remain
repository conventions or guidance unless an applicable constitutional source
expressly gives them a different status. Conversely, a constitutional
requirement is not weakened because a local workflow has not yet implemented a
convenient way to observe it.

When interpretation cannot be resolved from the applicable source and evidence,
preserve the uncertainty and identify the missing source or act. Do not convert
a recommendation into authority, or authority into a recommendation, merely to
continue.

## 9. Common misconceptions

| Misconception | Correct distinction |
| --- | --- |
| **Planning ≠ Authorization** | A plan defines intended scope or sequence; authorization is a separate permission for a bounded act. |
| **Allocation ≠ Authorization** | Allocation assigns responsibility and scope; authorization permits the work. |
| **Review ≠ Confirmation** | Review records an evaluation and findings; confirmation records an independent determination within its own boundary. |
| **Confirmation ≠ Validation** | Confirmation concerns the stated determination; content-identity validation concerns reproducible identity at a defined boundary. |
| **Validation ≠ Freeze** | Validation checks identity; freeze establishes the immutability boundary for the validated corpus. |
| **Freeze ≠ Closeout** | Freeze protects exact content; closeout concludes the specified lifecycle. |
| **Release Attestation ≠ Runtime Release** | Release attestation is a package-specific governance disposition; runtime release is operational activation or deployment. |
| **Decision Log ≠ Authority** | A decision log provides engineering history and context; it does not independently create constitutional or runtime authority. |
| **INDEX ≠ Authority** | An index helps readers navigate records; the linked source records retain their own meaning and limits. |
| **Repository Convention ≠ Constitutional Requirement** | A recurring workflow or instruction guides repository work; it is not constitutional authority unless a canonical source says so. |

## 10. Governance boundaries

Governance intentionally does not perform every action that may follow from a
governed decision. Its boundary protects both the authority source and the
owner responsible for the downstream work.

- **It does not implement software.** Governance may define a bounded
  implementation scope or record authorization, but code, schemas, APIs,
  persistence, provider integrations, and tests remain implementation work
  unless separately performed under the applicable scope.
- **It does not redesign frozen milestones.** A handbook or later convenience
  cannot reopen, rewrite, normalize, or replace frozen planning or artifact
  bytes. A different design requires a separately competent source and scope.
- **It does not infer authority.** A roadmap, allocation, positive review,
  confirmation, freeze, closeout, or commit does not supply an authority that
  its record does not state.
- **It does not repair missing evidence by invention.** A missing act or
  ambiguous identity must be reported and resolved by an additive, competent
  record when one is permitted; it must not be silently reconstructed.
- **It does not replace owner domains.** A governance record can preserve
  ownership boundaries and exclusions, but it cannot take over another
  domain's technical or operational authority.
- **It does not authorize runtime.** A frozen artifact or release attestation
  is not production activation, deployment permission, or downstream intake
  unless a separate applicable source expressly establishes that effect.
- **It does not erase history.** Later corrections and passes supplement the
  record and preserve earlier failures, blockers, and limitations.

## 11. Relationship to other handbooks

The handbooks are complementary. They should link to one another rather than
repeat canonical constitutional text or turn a workflow explanation into a
governance disposition.

| Document | Relationship to this handbook |
| --- | --- |
| [AI_RULES.md](AI_RULES.md) | Operational expectations for AI work, including source tracing, scope control, evidence discipline, identity boundaries, stop conditions, and reporting. |
| [REVIEW_HANDBOOK.md](REVIEW_HANDBOOK.md) | Review preparation, review boundaries, findings, correction handling, and verification guidance. It does not replace the actual review records. |
| [ARCHITECTURE_HANDBOOK.md](ARCHITECTURE_HANDBOOK.md) | Navigation of architecture sources, ownership boundaries, and technical design records. Architecture guidance does not itself create governance authority. |
| [AI_COLLABORATION_GUIDE.md](AI_COLLABORATION_GUIDE.md) | Human-AI collaboration, handoffs, communication, and expectation-setting around repository work. |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | Repository contributor conventions and participation guidance. It is not a substitute for a constitutional or governance record. |

The [handbook entry point](README.md) describes the documentation system and
its overall boundaries. For a specific task, read the relevant handbook and
then follow its links to the canonical artifact that actually answers the
question.

## 12. Related constitutional artifacts

The following are source pointers for the governance model described here. The
links do not give this handbook authority; each canonical artifact remains the
source of its own content, scope, identity, and limitations.

### Planning corpus and closeout

- [Asset Foundation Canonical Owner-Domain Architecture and Implementation Plan](../implementation/ASSET_FOUNDATION_CANONICAL_OWNER_DOMAIN_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
- [Asset Foundation Work-Package Decomposition and Roadmap](../implementation/ASSET_FOUNDATION_CANONICAL_OWNER_DOMAIN_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md)
- [Asset Foundation Planning Ratification](../governance/ASSET_FOUNDATION_PLANNING_RATIFICATION.md)
- [Asset Foundation Planning Freeze Record](../governance/ASSET_FOUNDATION_PLANNING_FREEZE_RECORD.md)
- [Asset Foundation Planning Closeout Record](../governance/ASSET_FOUNDATION_PLANNING_CLOSEOUT_RECORD.md)

### Work-package lifecycle precedents

- [AF-WP3 Allocation and Authorization Record](../governance/ASSET_FOUNDATION_AF_WP3_ALLOCATION_AND_AUTHORIZATION_RECORD.md)
- [AF-WP3 Closeout Record](../governance/ASSET_FOUNDATION_AF_WP3_CLOSEOUT_RECORD.md)
- [AF-WP4 Allocation Record](../governance/ASSET_FOUNDATION_AF_WP4_ALLOCATION_RECORD.md)
- [AF-WP4 Authorization Record](../governance/ASSET_FOUNDATION_AF_WP4_AUTHORIZATION_RECORD.md)
- [AF-WP4 Independent Review](../governance/ASSET_FOUNDATION_AF_WP4_INDEPENDENT_REVIEW.md)
- [AF-WP4 Content-Identity Validation](../governance/ASSET_FOUNDATION_AF_WP4_CONTENT_IDENTITY_VALIDATION.md)
- [AF-WP4 Exact-Byte Freeze Record](../governance/ASSET_FOUNDATION_AF_WP4_FREEZE_RECORD.md)
- [AF-WP4 Release Attestation Record](../governance/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md)
- [AF-WP4 Closeout Record](../governance/ASSET_FOUNDATION_AF_WP4_CLOSEOUT_RECORD.md)

The [AF-WP4 frozen implementation artifact](../implementation/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md)
and the [AF-WP4 governance release-attestation record](../governance/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md)
are intentionally separate artifacts. The first is the normative documentary
implementation artifact; the second is governance evidence. Their shared
subject does not make them the same authority source or the same freeze
corpus.

### Constitutional interpretation and navigation

- [Constitutional Precedent Index](../governance/CONSTITUTIONAL_PRECEDENT_INDEX.md)
- [Constitutional Opinion on the CIV Framework](../governance/CONSTITUTIONAL_OPINION_LA_WP2.md)
- [ARB Adoption Resolution for the Constitutional Opinion](../governance/ARB_RESOLUTION_ADOPTION_OF_CONSTITUTIONAL_OPINION.md)

Read the opinion and adoption resolution for their exact applicable corpus,
holding, adoption status, and limitations. The index remains a non-authoritative
navigation document.

## Status

`DRAFT`
