# AI Rules

## 1. Purpose and status

**Status:** `DRAFT`

This handbook is the operational entry point for AI systems working in this
repository. It summarizes and links established repository authority,
conventions, and safe working practices so that an AI can determine what it
may do before it changes anything.

This document is guidance. It is not a constitutional artifact, governance
record, allocation, authorization, implementation specification, or source of
new repository authority. It does not amend, reopen, reinterpret, replace, or
override a frozen artifact or a valid governance record. It does not turn a
repository convention into a constitutional requirement.

The primary audience is any AI system operating in the repository, including
coding agents, architecture advisors, documentation authors, reviewers,
confirmers, validators, and governance evidence recorders. Human maintainers
are the secondary audience and supervise the scope and truthfulness of AI
work.

For constitutional questions, consult the applicable frozen corpus and the
valid governance records that act within that corpus. The
[Constitutional Precedent Index](../governance/CONSTITUTIONAL_PRECEDENT_INDEX.md)
is explicitly non-authoritative navigation; its linked records remain the
sources of their own content and limits. For repository navigation, consult
the [Implementation Index](../implementation/INDEX.md), the
[Decision Log](../engineering/DECISION_LOG.md), the
[Engineering Principles](../engineering/ENGINEERING_PRINCIPLES.md), and the
[repository instructions](../../AGENTS.md) according to their stated scope.

## Contents

1. [Purpose and status](#1-purpose-and-status)
2. [Source-of-truth hierarchy](#2-source-of-truth-hierarchy)
3. [Authority before action](#3-authority-before-action)
4. [Frozen artifact rules](#4-frozen-artifact-rules)
5. [Lifecycle separation](#5-lifecycle-separation)
6. [Evidence discipline](#6-evidence-discipline)
7. [Review-role boundaries](#7-review-role-boundaries)
8. [Repository and Git safety](#8-repository-and-git-safety)
9. [Change-scope discipline](#9-change-scope-discipline)
10. [Stop conditions](#10-stop-conditions)
11. [Reporting requirements](#11-reporting-requirements)
12. [Common prohibited behaviors](#12-common-prohibited-behaviors)
13. [Quick preflight checklist](#13-quick-preflight-checklist)
14. [Related documents](#14-related-documents)

## 2. Source-of-truth hierarchy

The following table is primarily an operating order for authority and
governance questions. It is not a universal ranking of every engineering
source in the repository and it is not a new constitutional hierarchy. Each
source governs only the question and scope it actually owns, and a lower-level
source cannot override a higher-level source.

For technical questions, consult the relevant technical source directly:
architecture records and domain rules for intended structure and ownership;
source code for current implementation behavior; tests for executable
verification and observed contracts; and implementation documents for
milestones, sequencing, current state, and implementation scope. This is
question-dependent source selection, not a universal rank among those sources.

Rows marked `Instruction context` or `Technical source` below are reference
categories, not additional positions in the governance order.

| Order or role | Source | What it answers | Boundary |
| --- | --- | --- | --- |
| 1 | Frozen constitutional artifacts | Constitutional requirements, fixed boundaries, and the exact corpus to which they apply. | They are authoritative only within their stated corpus and limits. A later competent act is required for an amendment or successor authority. |
| 2 | Valid allocation and authorization records | What bounded work is allocated and what bounded act is authorized. | Allocation is not authorization. Authorization is limited to its stated scope and does not prove that implementation or later lifecycle acts occurred. |
| 3 | Frozen implementation artifacts | The exact implementation content that was permitted and frozen. | Frozen content is not permission to change itself or to perform a later lifecycle act. |
| 4 | Governance evidence | The facts, findings, identities, dispositions, and lifecycle events recorded by review, correction, confirmation, validation, freeze, release attestation, or closeout records. | Evidence does not silently create authority. A record's express disposition and role boundary control; silence is not permission. |
| 5 | Decision Log | Repository decisions and the reasoning useful for revisiting constraints or architecture. | The Decision Log is not independent constitutional authority and cannot replace a governing artifact when one is required. |
| 6 | INDEX and navigation documents | Where to find the relevant record and how documents relate. | The linked document governs. The Implementation Index and Constitutional Precedent Index introduce no authority of their own. |
| 7 | Handbook guidance | Practical operating rules for AI and human collaboration. | This handbook creates no constitutional, governance, implementation, runtime, or operational authority. |
| 8 | Chat instructions and agent assumptions | The requested task scope, context, and working assumptions. | A user request may authorize ordinary repository edits within its explicit scope, but it does not amend frozen content or perform an unestablished constitutional act. Agent assumptions are never authority. |
| Instruction context | `AGENTS.md` | In this repository, graphify query/path/explain/update handling and related navigation instructions. | It does not contain a broader constitutional hierarchy. Follow it for graphify behavior; cite the underlying artifact for authority. |
| Instruction context | `CLAUDE.md` | Required project-document reading before tasks: `ENGINEERING_PRINCIPLES.md`, `ARCHITECTURE.md`, `OPTIMIZER_PHILOSOPHY.md`, `PORTFOLIO_CALCULATION_RULES.md`, and `DECISION_LOG.md`, plus relevant additional documents. | It says `docs/` is the authoritative source of project knowledge and that project rules should not be duplicated in `CLAUDE.md`; it is an instruction file, not constitutional authority. |
| Technical source | Architecture records, domain rules, source code, tests, and implementation documents | Intended design, current behavior, verification, milestones, sequencing, and technical scope, according to the source type. | Choose the source that answers the technical question. None is promoted to constitutional authority by this table. |

When sources appear to conflict, preserve the higher source's boundary, identify
the conflict, and stop if the permitted action cannot be determined. Do not
resolve the conflict by preference, convenience, a graph result, or an
unstated assumption.

## 3. Authority before action

Before modifying repository content, an AI must determine and record in its
working notes:

- the requested objective and exact scope;
- whether the work is ordinary repository work or part of a governed lifecycle;
- the canonical source for the rule, requirement, or artifact involved;
- the applicable allocation, if a work package or bounded package is involved;
- the applicable authorization, if the requested act requires one;
- the current lifecycle stage and the exact act permitted at that stage;
- the files and artifact class that may be touched;
- the prohibited acts, required evidence, and required verification; and
- the current Git status, including unrelated work that must be preserved.

Use this separation as a hard operating rule:

> Description or sequencing is not allocation. Allocation is not authorization.
> Authorization is not implementation.

The repository's AF-WP4 records demonstrate this separation: the
[Allocation Record](../governance/ASSET_FOUNDATION_AF_WP4_ALLOCATION_RECORD.md)
allocates bounded work but states that authorization was not performed, while
the [Authorization Record](../governance/ASSET_FOUNDATION_AF_WP4_AUTHORIZATION_RECORD.md)
authorizes only bounded documentary implementation and states that
authorization is not implementation.

Choose the operating lane before applying the checklist:

- **Ordinary-work lane:** Routine coding or documentation work outside a
  governed lifecycle does not require work-package allocation or lifecycle
  authorization unless a repository source specifically requires them. The AI
  must still verify the user-requested scope, repository instructions,
  frozen/protected paths, unrelated working-tree changes, the technical source
  of truth, appropriate verification, and commit/push permission.
- **Governed-lifecycle lane:** Work governed by a frozen corpus must verify the
  applicable allocation, authorization, lifecycle stage, permitted artifact
  class, prohibited acts, and required evidence before acting.

Ordinary-work permission is still bounded permission. It does not authorize
changes to constitutional, governance-evidence, frozen implementation,
runtime, or downstream artifacts unless a repository source specifically puts
those paths in scope.

## 4. Frozen artifact rules

Treat every artifact identified as frozen, or included in a frozen corpus, as
immutable unless a later competent governance act explicitly authorizes an
amendment or a separately bounded successor act.

Do not infer artifact class from a basename. The repository contains two
different AF-WP4 release-attestation paths:

- frozen normative implementation artifact:
  `docs/implementation/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md`;
- governance release-attestation record:
  `docs/governance/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md`.

To determine whether a path is frozen, use this discovery procedure:

1. Locate the applicable freeze record.
2. Read its exact corpus inventory.
3. Identify each full repository-relative path in that inventory.
4. Verify the identity boundary recorded for those paths.
5. Treat only the enumerated corpus as frozen under that record.

If a same-basename file is outside the enumerated corpus, do not call it
frozen under that record; if its status is unclear, stop and resolve the
status from the applicable source.

An AI must not, without that authority:

- edit or rewrite a frozen artifact;
- normalize line endings, whitespace, encoding, or formatting;
- repair, reformat, reorder, or regenerate it;
- substitute semantically equivalent text;
- copy its content into a replacement and present the replacement as the same
  artifact; or
- change it and then preserve the old identity claim.

The [Asset Foundation Planning Freeze Record](../governance/ASSET_FOUNDATION_PLANNING_FREEZE_RECORD.md)
identifies the exact two-artifact planning corpus and records Git blob IDs,
SHA-256 values, and line counts. It also states that freeze grants no
implementation, runtime, allocation, authorization, or downstream execution
authority. A freeze record therefore protects identity and boundary; it does
not grant permission to change the frozen bytes.

Exact-byte identity means identity of the actual bytes at the relevant
boundary, not merely semantic equivalence. Whitespace, line endings, ordering,
encoding, and other byte-level changes can produce a different Git blob or
digest while leaving the apparent prose meaning similar. If a record fixes a
Git blob, SHA-256, line count, byte size, or another identity predicate, all
applicable predicates must be checked against the exact current bytes.

An identity comparison must name its byte source and computation boundary:

1. **On-disk working-tree bytes:** the file contents currently present on disk.
2. **Git-normalized blob content derived from the working tree:** the content
   Git would store after applicable filters and attributes.
3. **Staged index content:** the bytes represented by the Git index for the
   staged path.
4. **Committed `HEAD` content:** the blob stored in the named committed
   revision.

Depending on `.gitattributes` and relevant Git configuration such as
`core.autocrlf`, on-disk bytes may differ from Git-stored blob bytes because of
line-ending normalization. Before comparing identities, inspect
`.gitattributes`, inspect relevant Git configuration, and identify the exact
identity boundary recorded by the governing validation or freeze record.

When the recorded boundary is committed or Git-normalized content, use a
reproducible Git content source such as `git cat-file -p <rev>:<path>` or
`git show <rev>:<path>`. When the recorded boundary is the staged index, read
the staged path from the index, for example with `git cat-file -p :<path>` or
`git show :<path>`. Report the byte source, command or method, attributes and
configuration considered, and the resulting identity values.

A SHA-256 or byte-size difference caused solely by verified line-ending
normalization is a computation-boundary condition, not proof that frozen
content changed. Report it and resolve it by using the correct comparison
boundary. Never edit a file merely to force its digest to match. A recorded
tracking or staging state is a point-in-time fact; it may legitimately change
after a later commit without invalidating the historical record that reported
the earlier state.

Never hash a file, edit it afterward, and continue to claim the earlier
identity. The [AF-WP4 Content-Identity Validation](../governance/ASSET_FOUNDATION_AF_WP4_CONTENT_IDENTITY_VALIDATION.md)
states that any byte change after validation requires a new identity-validation
act, and the [AF-WP4 Exact-Byte Freeze Record](../governance/ASSET_FOUNDATION_AF_WP4_FREEZE_RECORD.md)
preserves the validated bytes as the frozen corpus. If identity does not
match, first verify the applicable identity boundary and normalization method.
Only if the comparison remains unresolved should the AI stop and report an
identity mismatch; do not repair the artifact opportunistically.

## 5. Lifecycle separation

Lifecycle acts are separate acts. Completion of one does not imply completion,
authority, or permission for another. The table below is a non-exhaustive
inventory of distinct acts, not a mandatory universal sequence.

These are operational summaries derived from repository precedents, including
the Asset Foundation records. Lifecycle definitions are corpus-bound. Another
frozen corpus may define a different or additional act or role, so the AI must
consult the frozen corpus governing the work at hand rather than treat Asset
Foundation semantics as universal constitutional law.

| Act | Meaning | Does not imply |
| --- | --- | --- |
| Planning | Describes a proposed shape, scope, dependency, or sequence. | Allocation, authorization, implementation, or runtime permission. |
| Ratification | Records ratification of a defined planning or constitutional corpus when the governing corpus provides for that act. | Allocation, authorization, implementation, or authority beyond the ratified corpus and record. |
| Adopted constitutional interpretation or ARB adoption | Records a bounded interpretation or adoption disposition for an identified corpus. | Authority over a different or successor corpus, or operational and implementation authority. |
| Allocation | Assigns a bounded responsibility and scope to a work package. | Authorization, implementation, review, or release. |
| Authorization | Permits a specified act within a bounded scope. | That the act was performed, reviewed, confirmed, frozen, released, or closed. |
| Implementation | Creates or changes the permitted artifact. | Independent review, correction acceptance, confirmation, identity validation, or freeze. |
| Independent review | Evaluates the artifact or act against its stated scope and records findings. | Confirmation, freeze, release, closeout, or implementation authority. |
| Correction | Responds to a review finding within the permitted scope. | A passing review, focused re-review, or confirmation. |
| Focused re-review | Re-examines a specified correction or limited issue. | Independent confirmation or a broader approval than its scope states. |
| Independent confirmation | Records an independent confirmation determination within its stated boundary. | Content-identity validation, freeze, release, closeout, or successor authority. |
| Content-identity validation | Validates the identity of exact bytes at a defined boundary. | Exact-byte freeze, canonical supply, release, closeout, or implementation authority. |
| Exact-byte freeze | Fixes the identity and immutability boundary of the validated corpus. | Release attestation, runtime release, downstream authority, or closeout. |
| Release attestation | Records a bounded release-attestation disposition. | Runtime release, production activation, downstream intake, or closeout. The governance record at `docs/governance/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md` states these non-effects for the frozen normative implementation artifact at `docs/implementation/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md`. |
| Epic closeout | Concludes the specified epic lifecycle when the governing corpus defines an epic-level closeout. | Successor allocation, successor authorization, runtime release, or new authority. |
| Closeout | Concludes the specified lifecycle. | Successor allocation, successor authorization, runtime release, or new authority. |
| Repository synchronization | Aligns repository state with the intended record or handoff. | A constitutional act, freeze, release, or closeout. |
| Commit | Records a snapshot in Git history. | Governance approval, allocation, authorization, freeze, or proof that a working-tree claim was valid. |

Do not collapse these acts into one session merely because they are adjacent in
a plan. Multiple lifecycle acts may share one record or session only when the
governing source explicitly authorizes that combination and each act remains
separately bounded and evidenced. The repository's
[AF-WP3 combined allocation-and-authorization precedent](../governance/ASSET_FOUNDATION_AF_WP3_ALLOCATION_AND_AUTHORIZATION_RECORD.md)
is an example of a source-specific combination; it does not create a universal
exception. Otherwise, perform only the act authorized for the current stage
and preserve separate records and identities when the governing corpus
requires them.

## 6. Evidence discipline

AI work must preserve an additive and reproducible history.

- Add new evidence or a correction response without silently rewriting prior
  findings, failed reviews, or historical dispositions.
- Preserve failed reviews, blocked states, corrections, and re-review results.
  A later pass does not erase an earlier fail.
- Keep normative artifacts, governance evidence, frozen supporting evidence,
  and navigation documents separate. The AF-WP4 validation record explicitly
  excludes allocation, authorization, review, confirmation, validation, and
  index records from the normative implementation candidate bytes.
- Cite the exact repository-relative path and, where relevant, section,
  record date, role, lifecycle disposition, Git identity, digest, line count,
  byte size, or commit identity.
- State which identity boundary was used: on-disk working-tree bytes,
  Git-normalized blob content derived from working-tree bytes, staged index
  content, or committed `HEAD` content. State the command or method that
  produced the identity and whether Git normalization affected the comparison.
  See [Repository and Git safety](#8-repository-and-git-safety); never collapse
  Git-normalized blob content into the generic working-tree label or describe
  one boundary as another.
- Do not invent a person, committee, actor, authority, evidence item, hash,
  status, review result, confirmation, or lifecycle event.
- Do not infer a positive result from missing evidence. Report `NONE`,
  `NOT PERFORMED`, blocked, or another disposition only when the source
  establishes that wording; otherwise use plain language and identify the gap.
- Treat evidence as evidence. It supports a determination but does not enlarge
  the scope or authority of the act that produced it.

## 7. Review-role boundaries

The roles below are a non-exhaustive operational summary derived from
repository precedents and are corpus-bound. Another frozen corpus may define
different or additional roles. Consult the corpus governing the work at hand.
The roles are distinct unless a governing source explicitly and competently
combines them for a defined act. The [Review Handbook](REVIEW_HANDBOOK.md) is
the detailed source for review
workflow; this section states only the boundary needed for safe AI work.

| Role | Boundary |
| --- | --- |
| Author | Produces the permitted artifact or response. The author must not present authorship as independent review, confirmation, freeze, release, or closeout. |
| Reviewer | Evaluates the defined scope and records findings. Review is not confirmation, authorization, freeze, release, or closeout. |
| Confirmer | Makes an independent confirmation determination within its scope. Confirmation is not identity validation, freeze, release, or closeout. |
| Content-identity validator | Validates exact bytes and identity predicates. Validation does not freeze, canonicalize, release, or close out the artifact. |
| Freeze authority | Performs the exact-byte freeze act within its scope. Freeze does not grant runtime, downstream, release, or closeout authority. |
| Release-attestation authority | Records the bounded release-attestation disposition. Release attestation is not runtime release or production activation. |
| Closeout authority | Concludes the specified lifecycle. Closeout does not create successor authority or authorize later work. |

An AI must not claim a role merely because it performed a neighboring task or
because a later act appears obvious.

## 8. Repository and Git safety

These are repository conventions and safe operating rules. They do not create
constitutional authority, but an AI must follow them when performing repository
work unless a more specific authorized instruction establishes a different
safe procedure.

- Inspect `git status --short` before work and again before reporting results.
- Identify the exact intended paths and preserve unrelated working-tree
  changes, including untracked files that are not part of the current task.
- Avoid broad staging commands when exact scope matters. If staging is
  explicitly authorized, stage only the intended paths.
- Run appropriate diff, whitespace, Markdown, test, and local-link checks for
  the change; report what was actually run and its result.
- Never claim a clean tree without checking it.
- Never claim committed identity for untracked or uncommitted content.
- Do not commit or push unless the current request explicitly authorizes that
  action. A documentation request does not implicitly authorize either.
- Do not use a commit, branch name, or current checkout as a substitute for a
  governance record or exact identity calculation.

Git identity has four separate practical boundaries:

1. **On-disk working-tree bytes** are the file contents currently present on
   disk.
2. **Git-normalized blob content** is the content derived from the working tree
   after applicable attributes and filters.
3. **Staged index content** is the version represented by the Git index for the
   staged path.
4. **Committed `HEAD` content** is the blob stored in the named committed
   revision.

Inspect `.gitattributes` and relevant configuration such as `core.autocrlf`
before comparing these boundaries. A hash or byte-size difference caused only
by verified line-ending normalization is a computation-boundary condition, not
proof that frozen content changed. Report the condition and compare the source
record's actual boundary; never edit a file merely to force a digest to match.

For committed or Git-normalized comparisons, use a reproducible Git content
source such as `git cat-file -p <rev>:<path>` or `git show <rev>:<path>`. For a
staged boundary, use the staged index path such as `git cat-file -p :<path>` or
`git show :<path>`. Report the byte source, command or method, relevant
attributes/configuration, tracking state, staging state, and resulting
identity. A working-tree or staged identity is not a committed `HEAD`
identity, and a later commit may legitimately change tracking or staging state
without invalidating a historical record of the earlier state.

## 9. Change-scope discipline

Changes must be minimal and bounded by the current request and authority.

- Do not redesign completed milestones or reopen frozen decisions because a
  different design seems preferable.
- Do not touch unrelated files.
- Do not perform opportunistic refactoring, formatting, or ``cleanup`` outside
  the named scope.
- Do not update the Decision Log or an INDEX merely because a change occurred;
  update them only when the current act explicitly authorizes that update.
- Do not modify frozen constitutional artifacts, governance evidence, or frozen
  implementation artifacts during documentation work unless the current scope
  explicitly and validly authorizes it.
- Do not use a handbook to create a successor plan, allocate work, authorize
  implementation, or record a governance disposition.
- `graphify` output is tooling output for navigation and relationships. It is
  not constitutional authority, evidence of authorization, or a replacement
  for the source document. Follow the repository's graphify instructions when
  using it, but cite the underlying repository artifact for any authority claim.

When a change would broaden scope, stop and ask for an explicitly bounded
instruction or report that the broader action was not performed.

## 10. Stop conditions

First determine the operating lane. In the governed-lifecycle lane, stop when
a required lifecycle prerequisite is missing. In the ordinary-work lane,
routine coding or documentation work does not stop merely because there is no
work-package allocation, lifecycle authorization, or lifecycle stage; those
are conditional requirements unless a repository source specifically makes
them applicable. Ordinary work must still verify user scope, repository
instructions, frozen/protected paths, unrelated working-tree changes, the
technical source of truth, appropriate verification, and commit/push
permission.

When an identity difference may be caused solely by verified line-ending
normalization, do not treat that difference as proof that frozen content
changed. Report the computation boundary, inspect the relevant attributes and
configuration, and resolve the comparison against the identity boundary
recorded by the governing source. Do not edit the file to force a match.

For either lane, stop before modifying content when any of the following
applies:

- a governed work package requires allocation and that allocation is missing or
  its scope is unclear;
- a governed act requires authorization and the authorization is missing or
  does not cover the requested act;
- the applicable authority or technical source is ambiguous, conflicting, or
  cannot be traced to a source;
- a governed request belongs to a later lifecycle stage;
- a frozen/protected artifact or frozen corpus has changed unexpectedly;
- an identity comparison is required, its boundary is not identified, or the
  identity does not match the recorded predicate after the relevant Git
  normalization boundary has been checked;
- required governed review, confirmation, validation, freeze, release, or
  closeout evidence is missing;
- the working tree contains unexpected scope or unrelated changes that cannot
  be safely preserved;
- the request would modify a prohibited file or perform a prohibited act; or
- the user asks for a next step that is not authorized by the applicable
  record, instruction, or ordinary-work scope.

On stop, do not invent a bridge record, substitute a semantic equivalent, or
continue because the next action appears operationally convenient. Report the
exact blocker, the act that was **not performed**, the evidence consulted, and
the next source-backed step if one exists. If the repository has not
established a formal disposition token, use plain language instead of inventing
a universal constitutional token.

## 11. Reporting requirements

Every completion report must be truthful, reproducible, and explicit about
limits. Include the following fields when they apply to the work:

- the authority, instruction, or convention relied upon;
- the exact scope;
- the lifecycle stage and current lifecycle state for governed work;
- files created;
- files modified;
- files intentionally left unchanged;
- verification performed and the actual results;
- limitations, blockers, and unresolved questions;
- the exact next permitted step, if a governing source establishes one; and
- whether anything was staged, committed, or pushed.

Use a report shape such as:

```text
Authority relied upon:
Scope:
Lifecycle stage/current lifecycle state: (governed work only)
Files created:
Files modified:
Files intentionally unchanged:
Verification:
Current state: (when meaningful)
Limitations or blockers:
Next permitted step:
Commit/push status:
```

For an ordinary read-only task, a compact report is sufficient unless the
request or repository source requires more detail:

```text
Read-only scope:
Sources consulted:
Files changed: none
Verification performed:
Findings or limitations:
Commit/push: none
```

If no action is authorized, say so plainly and do not imply that an action was
completed. If a conclusion is uncertain, state what is known, what is not
known, and what evidence would be required to resolve it.

## 12. Common prohibited behaviors

The following are prohibited AI operating patterns:

- inferring authorization from planning, description, sequencing, or a
  roadmap;
- treating allocation as authorization or authorization as implementation;
- treating review as confirmation;
- hashing a file and then editing it while retaining the earlier identity
  claim;
- claiming freeze before exact identity validation and the required freeze act;
- treating `RELEASE ATTESTED` as runtime release, production activation, or
  downstream authorization;
- treating an INDEX or the Decision Log as independent constitutional
  authority;
- creating successor authority from a closeout record;
- inventing a person, committee, board, actor, authority, evidence item, or
  status to make a lifecycle appear complete;
- erasing a historical `FAIL`, blocker, correction, or unresolved finding;
- editing a frozen artifact to fix formatting, encoding, line endings, or
  semantic presentation;
- performing multiple distinct lifecycle acts in one session without explicit
  authorization for each act;
- broadening a documentation task into implementation, governance, or cleanup;
  and
- continuing merely because the user asks for ``the next prompt`` when the
  current authority, evidence, or lifecycle stage does not permit it.

## 13. Quick preflight checklist

Before any repository action, confirm:

- [ ] I read the current Git status and identified unrelated work.
- [ ] I can name the exact files and artifact class in scope.
- [ ] I found the canonical source and read its authority boundary.
- [ ] I chose the ordinary-work lane or governed-lifecycle lane.
- [ ] For governed work, I verified allocation and authorization separately
      when they are required.
- [ ] For governed work, I identified the current lifecycle stage and the one
      act permitted now.
- [ ] For ordinary work, I verified repository instructions, the technical
      source of truth, appropriate checks, and commit/push permission.
- [ ] If a protected or potentially frozen path is involved, I located the
      applicable freeze record, read its exact corpus inventory, identified the
      full repository-relative path, and verified the identity boundary.
- [ ] I confirmed that no enumerated frozen bytes will be changed.
- [ ] I know what evidence and identity predicates must be preserved.
- [ ] I will make the smallest bounded change and preserve unrelated work.
- [ ] I know which verification checks I will run.
- [ ] I will report files, state, limitations, and Git identity truthfully.
- [ ] I will stop rather than infer permission if any prerequisite is missing
      or ambiguous.

## 14. Related documents

### Handbook and repository guidance

- [Handbook entry point](README.md)
- [AI Collaboration Guide](AI_COLLABORATION_GUIDE.md)
- [Governance Handbook](GOVERNANCE_HANDBOOK.md)
- [Review Handbook](REVIEW_HANDBOOK.md)
- [Architecture Handbook](ARCHITECTURE_HANDBOOK.md)
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [Repository instructions](../../AGENTS.md)
- [CLAUDE.md](../../CLAUDE.md)
- [Repository Glossary](../GLOSSARY.md)
- [Decision Records](../decisions/README.md)

### Canonical and navigation sources

- [Constitutional Precedent Index](../governance/CONSTITUTIONAL_PRECEDENT_INDEX.md)
- [Asset Foundation Planning Freeze Record](../governance/ASSET_FOUNDATION_PLANNING_FREEZE_RECORD.md)
- [AF-WP4 Allocation Record](../governance/ASSET_FOUNDATION_AF_WP4_ALLOCATION_RECORD.md)
- [AF-WP4 Authorization Record](../governance/ASSET_FOUNDATION_AF_WP4_AUTHORIZATION_RECORD.md)
- [AF-WP4 Content-Identity Validation](../governance/ASSET_FOUNDATION_AF_WP4_CONTENT_IDENTITY_VALIDATION.md)
- [AF-WP4 Exact-Byte Freeze Record](../governance/ASSET_FOUNDATION_AF_WP4_FREEZE_RECORD.md)
- Frozen normative implementation artifact: [`docs/implementation/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md`](../implementation/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md)
- Governance release-attestation record: [`docs/governance/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md`](../governance/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md)
- [AF-WP4 Closeout Record](../governance/ASSET_FOUNDATION_AF_WP4_CLOSEOUT_RECORD.md)
- [AF-WP3 combined allocation-and-authorization precedent](../governance/ASSET_FOUNDATION_AF_WP3_ALLOCATION_AND_AUTHORIZATION_RECORD.md)
- [Implementation Index](../implementation/INDEX.md)
- [Decision Log](../engineering/DECISION_LOG.md)
- [Engineering Principles](../engineering/ENGINEERING_PRINCIPLES.md)
