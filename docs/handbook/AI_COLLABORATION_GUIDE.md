# AI Collaboration Guide

> Status: `DRAFT`

This handbook explains how humans and AI systems can collaborate clearly,
safely, and continuously within this repository. It is explanatory repository
documentation. It creates no authority, performs no governance act, approves no
implementation, produces no review evidence, and does not redefine
constitutional behavior.

The applicable source, user instruction, repository convention, and operating
lane determine what may actually be done. This guide helps collaborators keep
those boundaries visible; it does not replace the source that establishes them.

## Contents

1. [Purpose](#1-purpose)
2. [Collaboration philosophy](#2-collaboration-philosophy)
3. [Roles](#3-roles)
4. [Session continuity](#4-session-continuity)
5. [Multi-AI collaboration](#5-multi-ai-collaboration)
6. [Communication practices](#6-communication-practices)
7. [Working with repository artifacts](#7-working-with-repository-artifacts)
8. [Collaboration boundaries](#8-collaboration-boundaries)
9. [Common collaboration mistakes](#9-common-collaboration-mistakes)
10. [Human–AI interaction](#10-humanai-interaction)
11. [Relationship to other handbooks](#11-relationship-to-other-handbooks)
12. [Related repository sources](#12-related-repository-sources)

## 1. Purpose

AI collaboration is most useful when the human and the AI share an accurate
understanding of the task, the repository state, the applicable sources, and the
limits of the current session. This guide explains practices for task framing,
role clarity, context transfer, multi-AI collaboration, uncertainty, findings,
and handoffs.

It creates no authority. Reading it does not authorize an edit, make an AI a
reviewer, establish a governance role, approve a design, or turn a suggestion
into a repository requirement. The [AI Rules](AI_RULES.md) remain the operating
source for AI work. The [Governance Handbook](GOVERNANCE_HANDBOOK.md) explains
authority and evidence boundaries. The [Review Handbook](REVIEW_HANDBOOK.md)
explains review methodology. The
[Architecture Handbook](ARCHITECTURE_HANDBOOK.md) explains architectural
reasoning and the boundary between architecture and implementation.

### Four collaboration labels

The following labels keep a conversation from giving guidance more force than
it has:

| Label | Meaning | How to handle it |
| --- | --- | --- |
| **Repository requirement** | A requirement established by an applicable source, repository instruction, explicit user scope, or other authority that actually applies to the task. | Follow it within its stated scope. Cite the source when it matters. |
| **Repository convention** | A recurring way the repository organizes, verifies, preserves, or communicates work. | Follow it as applicable practice; do not present it as constitutional authority unless a canonical source says so. |
| **Recommended collaboration practice** | Guidance that tends to make human–AI work clearer, safer, or more reproducible. | Use judgment. Departure is not automatically a violation. |
| **Optional workflow** | One possible sequence or format for reaching a result. | Use it when helpful; choose another bounded workflow when the task calls for it. |

When a requirement and a recommendation appear to conflict, the applicable
requirement controls. When the source or scope is unclear, preserve the
uncertainty and consult [AI_RULES.md](AI_RULES.md) before acting.

## 2. Collaboration philosophy

### AI as collaborator, not decision-maker

An AI can search, explain, compare, draft, calculate when the task permits it,
and identify consequences. It does not become the owner of a repository
decision merely by producing a persuasive answer. A human or applicable source
retains responsibility for decisions that require human judgment, explicit
authority, or a defined governance act.

This does not make the AI passive. A good collaborator notices scope conflicts,
missing evidence, hidden assumptions, contradictory sources, and unsafe next
steps, then makes those conditions visible before continuing.

### Explicit reasoning

Collaboration improves when the path from source to conclusion is inspectable.
State which facts were observed, which interpretation follows, which
assumptions were added, and which recommendation is optional. The goal is not
to expose every internal thought; it is to provide enough reasoning and
evidence for a human or another AI to verify the claim.

### Bounded assistance

Help should match the task's exact scope. An AI can offer an adjacent idea as a
clearly labelled observation or future option, but it should not silently turn
that idea into work. Bounded assistance protects the user's intent, unrelated
working-tree changes, frozen artifacts, owner domains, and later reviewers.

### Transparency

A collaborator should make important limitations visible: files not inspected,
sources not found, commands not run, assumptions not verified, and actions not
performed. A concise limitation is more useful than a confident statement that
leaves a later reader to discover the gap.

### Reproducibility

Another competent person should be able to repeat the relevant part of the
work. Use exact paths, source sections, commands or methods, identity
boundaries, and actual verification results when they affect the conclusion.
Reproducibility is especially important when an AI session will hand work to a
different human or AI system.

### Continuity across sessions

A session is temporary; the repository and its records persist. Important
context should therefore be transferred explicitly rather than left in an
unrecorded conversation. A useful handoff preserves the task boundary, source
status, repository state, unresolved questions, and exact next step without
pretending that a later session has observed what it has not inspected.

## 3. Roles

Roles describe the work being performed, not the identity or capability of the
system performing it. A role must come from an explicit user instruction or an
applicable source. An AI must not infer a governance role, review independence,
authorization, confirmation, freeze authority, or closeout authority from a
nearby task, a tool call, or the fact that it was asked to continue.

The roles below are useful collaboration descriptions. They are not a universal
repository taxonomy and do not grant authority by being named here.

| Collaboration role | Typical contribution | Boundary |
| --- | --- | --- |
| **Architecture advisor** | Explains architectural sources, compares design consequences, identifies boundaries, and records assumptions. | Does not approve architecture, amend a frozen source, or authorize implementation. |
| **Implementation assistant** | Searches existing code, proposes or makes bounded changes, and runs appropriate verification. | Acts only within the explicit scope and applicable authorization; implementation is not review or approval. |
| **Reviewer** | Evaluates a defined subject against applicable sources and records findings. | Review is not correction, confirmation, authorization, freeze, release, or closeout. See [REVIEW_HANDBOOK.md](REVIEW_HANDBOOK.md). |
| **Documentation author** | Creates or updates explanatory, navigational, or repository-convention documentation. | Documentation does not create authority or silently rewrite canonical artifacts. |
| **Research assistant** | Locates sources, gathers evidence, compares alternatives, and identifies unanswered questions. | Research findings remain evidence or recommendations until an authorized actor or source adopts them. |
| **Coordinator** | Frames tasks, preserves handoff context, tracks dependencies, and makes ownership visible. | Coordination does not allocate, authorize, approve, or close work unless a separate source explicitly establishes that act. |

One session may perform more than one ordinary-work contribution when the user
scope permits it, but the report should distinguish the contributions. A session
that authors output must not independently review, confirm, or otherwise
evaluate the correctness of that same output. This independence constraint
applies in both the ordinary-work and governed-work lanes. Disclosure of
combined contributions does not replace reviewer independence. Where an
applicable governing corpus explicitly authorizes a bounded combination of
lifecycle acts, that authorization concerns the lifecycle structure rather than
self-evaluation. In governed work, role separation and any permitted combination
come from the applicable corpus and records. [AI_RULES.md §7](AI_RULES.md#7-review-role-boundaries)
contains the operational role boundaries. See [REVIEW_HANDBOOK.md §4 (operating lane)](REVIEW_HANDBOOK.md#determining-the-operating-lane),
[REVIEW_HANDBOOK.md §9 (confirmation)](REVIEW_HANDBOOK.md#9-confirmation), and
[AI_RULES.md §7 (review-role boundaries)](AI_RULES.md#7-review-role-boundaries).

## 4. Session continuity

Continuity is the discipline of making the next session's starting point
explicit. It is not a claim that the next AI remembers the prior conversation.

### Preserve context that changes the task

A handoff should preserve information that affects scope, authority, identity,
or the next decision:

- the objective and exact files or artifacts in scope;
- whether the task is ordinary repository work or governed-lifecycle work;
- applicable sources, instructions, allocations, and authorizations when they
  apply;
- frozen or protected paths and the identity boundary that matters;
- repository status, including unrelated changes and untracked files;
- work completed and verification actually performed;
- assumptions, uncertainties, blockers, and questions left open; and
- the exact next permitted or requested step.

Do not transfer a conclusion without transferring the condition that made it
true. For example, “the file matches” is incomplete when the relevant question
is whether on-disk bytes, Git-normalized content, staged content, or committed
`HEAD` content was compared.

### Restarting a session

When a new session begins, re-establish the current state instead of assuming
the previous state survived. Read the handoff, inspect the relevant files and
sources, and check the repository status before acting. A short handoff is a
map, not a substitute for verification.

### A useful handoff shape

The following is an optional workflow, not a required report format:

```text
Task and exact scope:
Operating lane:
Sources consulted:
Files created or changed:
Frozen/protected paths:
Repository state:
Verification performed:
Known facts:
Assumptions and uncertainties:
Actions not performed:
Requested or source-backed next step:
```

The [AI Rules reporting guidance](AI_RULES.md#11-reporting-requirements) and
the current request may require a different shape. Use the more specific
applicable requirement.

### Frozen-state awareness

A later session must not assume that a file is editable because an earlier
session edited a similarly named file. Determine frozen status from the
applicable freeze record and exact corpus inventory. Preserve the recorded
identity boundary and do not edit a frozen artifact to make a comparison pass.
The procedure is defined in [AI_RULES.md §4](AI_RULES.md#4-frozen-artifact-rules)
and its identity guidance.

### Avoid hidden assumptions

If a handoff says “continue,” identify what continuation means: inspect, draft,
correct, review, verify, or report. If the answer changes the authority or
scope of the work, ask for or locate the missing instruction rather than
choosing the most convenient interpretation.

## 5. Multi-AI collaboration

Different AI systems can contribute useful perspectives when their roles,
inputs, and boundaries are explicit. They should be treated as collaborators
with evidence, not as a chain in which each system automatically validates the
previous system.

### Possible contributors

| Contributor | Useful perspective | Independence risk |
| --- | --- | --- |
| **Architecture AI** | Maps source documents, boundaries, ownership, dependencies, and design alternatives. | Repeats an existing implementation assumption as if it were architecture. |
| **Implementation AI** | Examines code and tests, proposes bounded changes, and reports actual behavior. | Treats working code as permission or silently redesigns the architecture. |
| **Reviewer AI** | Evaluates a defined subject against applicable sources and records findings. | Reviews a summary instead of the source, self-reviews work authored by the same session, or becomes the correction author. |
| **Research AI** | Locates evidence, compares sources, and identifies open questions. | Treats search results, indexes, or another AI's summary as canonical authority. |
| **Coordinator AI** | Preserves scope, handoffs, dependencies, and unresolved decisions. | Infers ownership, approval, or the next authorized act from the schedule. |

These labels do not require particular vendors, models, tools, or deployment
arrangements. The same system may perform several ordinary collaboration roles
when the task permits it, subject to the independence constraint above, but it
must not claim a governed role merely because it performed related work.

### Independent reasoning

Independence requires more than different session names. When a second AI is
asked for an independent view, provide the defined subject and applicable
sources, not only the first AI's conclusion. Record whether the second AI read
the canonical source, relied on a summary, or checked the same command output.

### Comparing conclusions

Compare conclusions at the level of evidence:

1. identify the exact claim on which the systems differ;
2. separate factual disagreement from interpretation, scope, or preference;
3. return to the source that owns the question;
4. compare the relevant paths, identities, commands, or results; and
5. preserve the disagreement if the source does not resolve it.

Agreement between two AI systems is not a substitute for a source, test, human
decision, or governance record.

### Avoiding circular validation

Circular validation occurs when one AI produces a claim, another repeats it as
evidence, and a third treats the repetition as independent confirmation. Break
the circle by tracing each conclusion to an independently inspected source or
reproducible observation. Confirmation is a separate act only when the
applicable source establishes that act and its boundary; collaboration language
does not create it.

### Handling disagreement

Do not force a consensus merely to keep the workflow moving. A disagreement may
indicate a missing source, ambiguous scope, different identity boundaries, a
real source conflict, or a legitimate design trade-off. State which kind it is,
what evidence would resolve it, and whether work must stop under
[AI_RULES.md](AI_RULES.md).

## 6. Communication practices

Good collaboration communication lets a reader distinguish what happened from
what the collaborator thinks should happen.

### Label the kind of claim

| Claim type | Useful wording | Do not imply |
| --- | --- | --- |
| **Fact** | “The file contains…”, “The command returned…”, “The source states…” | That the fact proves a larger conclusion than it supports. |
| **Inference** | “This suggests…”, followed by the evidence and limits. | That an interpretation is itself a source requirement. |
| **Recommendation** | “I recommend… because…” | That a recommendation is approval or authority. |
| **Uncertainty** | “I could not establish…”, “The source is silent about…” | That silence is permission. |
| **Blocker** | “The requested act was not performed because…” | That an invented substitute resolved the blocker. |
| **Optional workflow** | “One way to proceed is…” | That the proposed sequence is mandatory. |

### State assumptions

Assumptions are acceptable when they are visible and low-risk for the current
scope. Name the assumption, why it was made, whether it was verified, and what
would change if it is false. If an assumption could change authority, frozen
status, ownership, identity, or material behavior, stop and resolve it before
acting.

### Report uncertainty and limitations

Be precise about the boundary of a conclusion. Say which files, sources,
commands, tests, or identity boundaries were not examined. Use the disposition
established by the applicable source; do not invent status tokens to make a
report look complete.

### Communicate findings usefully

A useful finding identifies the exact subject location, the applicable source,
the requirement or criterion, the observed departure, and the consequence. It
separates findings from observations, preferences, and optional suggestions.
The [Review Handbook](REVIEW_HANDBOOK.md) contains the detailed methodology and
severity guidance.

### Ask for clarification when it matters

Ask when a missing answer would materially change the scope, operating lane,
authority, protected paths, artifact class, identity boundary, or required
result. When clarification would only affect a reversible presentation choice,
make a reasonable assumption, label it, and continue if the task permits.

## 7. Working with repository artifacts

Different artifacts carry different kinds of information. Collaboration is safe
when the AI preserves those distinctions instead of treating every document as
an instruction or every current file as authority.

| Artifact class | How an AI may use it | Boundary to preserve |
| --- | --- | --- |
| **Frozen artifacts** | Read, cite, compare at the recorded identity boundary, and use as a constraint. | Do not edit, normalize, reformat, reorder, replace, or repair without the applicable competent authority. |
| **Implementation artifacts** | Inspect current behavior, draft or modify bounded candidates, and verify the permitted realization. | A candidate or current implementation is not automatically approved, frozen, released, or authoritative. |
| **Governance evidence** | Trace acts, scope, identity, dispositions, prerequisites, and non-effects. | Evidence is additive and does not enlarge the authority of the act it records. Do not rewrite history to make it cleaner. |
| **Handbook and documentation** | Use guidance, navigation, explanations, and repository conventions according to their stated status. | A handbook or README creates no authority and cannot replace a canonical artifact. |
| **Engineering documents** | Use architecture, principles, decisions, domain rules, and implementation context for the technical question they own. | Technical context does not silently become constitutional, governance, or runtime authority. |

Before changing any artifact, follow the source tracing, lane selection, frozen
path discovery, Git identity, scope, and stop procedures in
[AI_RULES.md](AI_RULES.md). Do not infer artifact class from a basename or
directory alone.

## 8. Collaboration boundaries

The following are operating boundaries drawn from applicable repository rules,
not new authority created by this guide. An AI must not:

- invent a person, committee, actor, authority, evidence item, status, review
  result, confirmation, or lifecycle event;
- present a plan, recommendation, schedule, commit, or positive review as
  authorization for a later act;
- fabricate repository state, command output, test results, file contents,
  source consultation, or identity values;
- edit a frozen artifact or alter it merely to force an identity comparison to
  match;
- silently redesign architecture, reopen a frozen decision, or replace a
  canonical source with a semantically similar document;
- silently widen the user-requested scope, take over another owner domain, or
  preserve unrelated changes unsafely;
- merge separate lifecycle acts, roles, or records unless the applicable source
  explicitly permits the bounded combination;
- hide an uncertainty, failed check, blocked state, unresolved finding, or
  action that was not performed; or
- continue because the next step seems convenient when the applicable source,
  evidence, lane, or scope does not permit it.

When a boundary is reached, report the exact blocker, the act not performed, the
evidence consulted, and the next source-backed step if one exists. A user can
change an ordinary-work request, but a chat instruction cannot amend a frozen
artifact or perform an unestablished constitutional act.

## 9. Common collaboration mistakes

| Mistake | Why it harms collaboration | Better practice |
| --- | --- | --- |
| **Assuming context** | The AI acts on stale scope, an unverified status, or a prior session's interpretation. | Re-establish the task, source, lane, and repository state before acting. |
| **Overwriting history** | A correction or later pass makes an earlier failure or decision impossible to audit. | Add a bounded response and preserve prior records and dispositions. |
| **Merging separate lifecycle acts** | Review, confirmation, validation, freeze, release, or closeout becomes ambiguous and appears to grant unintended authority. | Keep acts distinct unless the applicable source explicitly permits a bounded combination. |
| **Treating conventions as authority** | A useful workflow preference becomes an unsupported requirement. | Label requirements, conventions, recommendations, and optional workflows separately. |
| **Solving the wrong problem** | The AI optimizes a nearby issue while missing the user's exact objective or source boundary. | Restate the objective and exclusions, then verify the proposed work answers that objective. |
| **Ignoring repository state** | Unrelated changes, untracked files, staged content, or frozen paths are overwritten or misreported. | Inspect status, preserve unrelated work, and report the exact identity boundary and changes. |
| **Circular validation** | Repeated AI summaries create the appearance of independent evidence. | Trace each conclusion to independently inspected sources or reproducible observations. |
| **Filling uncertainty with confidence** | A plausible assumption becomes a false fact that later collaborators rely on. | State the uncertainty, its impact, and what would resolve it. |

## 10. Human–AI interaction

### User authority and source boundaries

A user instruction defines the task the AI has been asked to help with. For
ordinary repository work, it may authorize bounded edits within its explicit
scope. It does not by itself amend frozen content, create constitutional
interpretation, perform an unestablished governance act, or grant authority
that a canonical source withholds.

The AI should identify that boundary rather than treating “please continue” as
permission for every adjacent action. If the requested work changes from
ordinary documentation to a governed act, stop and identify the source-backed
requirement.

### AI recommendations

An AI recommendation is an input to a human decision, not the decision itself.
The recommendation should state its evidence, assumptions, alternatives,
uncertainty, and limits. The human can accept, reject, revise, or request more
evidence within the applicable scope.

Acceptance of an AI suggestion does not retroactively make an unsupported claim
true or turn a recommendation into a canonical record. If a decision needs an
architectural, governance, or review artifact, create or update that artifact
through the applicable process rather than treating the conversation as a
substitute.

### Review before acceptance

Human review is proportionate to consequence. A small reversible documentation
change may need a concise inspection; a change touching a frozen path,
identity, accounting boundary, security property, or governance record needs
the applicable source and verification. “The AI wrote it” is not evidence that
the result is correct.

### Iterative refinement

Iteration is useful when each pass preserves the current scope and makes the
change or decision clearer. A later pass should state what it is refining,
what evidence changed, and what remains untouched. Iteration must not silently
rewrite a historical record or expand a bounded task into a new project.

### Responsibility boundaries

The human maintainer supervises the intended outcome, scope, and acceptance of
ordinary work and decides when a matter needs an explicit source-backed act.
The AI is responsible for truthful communication about what it inspected,
changed, verified, assumed, and did not perform. Neither collaboration partner
should assign authority to the other by implication; the applicable repository
source controls governed roles and acts.

## 11. Relationship to other handbooks

This guide explains collaboration around repository work. It does not repeat
the operational, governance, review, or architecture rules owned elsewhere.

| Document | Relationship to this guide |
| --- | --- |
| [AI_RULES.md](AI_RULES.md) | The operating source for source hierarchy, authority before action, ordinary and governed lanes, frozen artifacts, evidence, Git safety, stop conditions, and reporting. |
| [GOVERNANCE_HANDBOOK.md](GOVERNANCE_HANDBOOK.md) | Explains governance acts, authority boundaries, evidence continuity, and corpus-bound interpretation. |
| [REVIEW_HANDBOOK.md](REVIEW_HANDBOOK.md) | Explains review boundaries, findings, focused re-review, and confirmation. Collaboration around findings should follow its methodology. |
| [ARCHITECTURE_HANDBOOK.md](ARCHITECTURE_HANDBOOK.md) | Explains architectural reasoning, source roles, boundaries, evolution, and the distinction between architecture and implementation. |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | Contains contributor-facing repository conventions. It guides participation but does not replace canonical sources. |
| [Handbook entry point](README.md) | Describes the handbook system, inventory, audiences, reading order, and overall documentation boundaries. |

When a collaboration question is actually an authority, architecture, review,
or repository-convention question, follow the handbook or canonical source that
owns that question.

## 12. Related repository sources

These are source pointers, not additional authority. Each linked artifact keeps
its own scope, status, identity, and limitations. Read the applicable source
rather than relying on a summary in this guide.

- [AI Rules](AI_RULES.md) — operational source for AI work and safe repository
  actions.
- [Repository instructions](../../AGENTS.md) — project-specific instructions,
  including graphify behavior and repository navigation.
- [Handbook entry point](README.md) — documentation-system overview and
  boundaries.
- [Governance Handbook](GOVERNANCE_HANDBOOK.md) — governance authority and
  evidence model.
- [Review Handbook](REVIEW_HANDBOOK.md) — review methodology and findings.
- [Architecture Handbook](ARCHITECTURE_HANDBOOK.md) — architectural practice
  and source navigation.
- [CONTRIBUTING.md](../../CONTRIBUTING.md) — contributor conventions.
- [Repository Glossary](../GLOSSARY.md) — shared repository vocabulary.

The presence of a source in this list does not make it applicable to every
task. Applicability, scope, and authority must still be traced to the source
and current instruction that govern the work.

## Status

`DRAFT`
