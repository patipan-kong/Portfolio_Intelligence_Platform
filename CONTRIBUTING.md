# Contributing

This guide is the starting point for anyone contributing to the repository. It
is written for new contributors, maintainers, external collaborators, and
AI-assisted contributors who need to understand where to begin and which
source owns a particular question.

It is repository onboarding guidance, not a constitutional artifact,
governance record, implementation specification, or engineering policy. It
creates no authority and does not replace the source that governs a specific
artifact, decision, lifecycle act, or technical question.

## 1. Purpose

Contribute correctly by identifying the work before changing files. Start with
the objective, determine what kind of contribution it is, read the relevant
source, make the smallest scoped change, and leave a clear record of what was
done and verified.

This document provides the map. The handbooks and canonical repository sources
provide the detailed guidance.

## 2. Repository philosophy

The repository is easier to maintain when each question has a clear source and
each contribution has a visible boundary. The practical principles are:

- keep one canonical home for a requirement, decision, or technical contract;
- distinguish explanatory guidance from authority and evidence;
- preserve the history and identity of existing artifacts;
- keep ordinary documentation, implementation, architecture, governance,
  review, and engineering work distinguishable;
- make assumptions, limitations, and verification visible; and
- treat human and AI collaborators as contributors working within an explicit
  scope, not as substitutes for the source or role that owns a decision.

These principles guide repository participation. The applicable handbook,
canonical artifact, repository convention, or user instruction controls the
specific task.

## 3. Before making changes

Begin with a short task definition:

1. State the objective and the exact files or artifact in scope.
2. Check the repository instructions in [`AGENTS.md`](AGENTS.md) and inspect
   the current repository state before touching files.
3. Determine whether the work is ordinary documentation, implementation,
   governance, architecture, review, or engineering work.
4. Read the handbook and canonical source that own that kind of question.
5. Identify exclusions, protected or frozen paths, and unrelated working-tree
   changes that must be preserved.

The classification matters because different artifact classes have different
owners and boundaries. When the classification or permitted action is unclear,
pause and consult the relevant handbook rather than inferring permission from a
nearby document or an earlier contribution.

## 4. Repository map

The repository is organized into documentation areas with different purposes:

| Area | What to expect | Starting point |
| --- | --- | --- |
| `docs/handbook/` | Explanatory guidance for AI work, collaboration, governance navigation, review, and architecture navigation. | [`docs/handbook/README.md`](docs/handbook/README.md) |
| `docs/governance/` | Governance records, constitutional navigation, lifecycle evidence, and bounded dispositions. | [`GOVERNANCE_HANDBOOK.md`](docs/handbook/GOVERNANCE_HANDBOOK.md) |
| `docs/implementation/` | Implementation plans, implementation artifacts, package records, and implementation navigation. | [`implementation/INDEX.md`](docs/implementation/INDEX.md) |
| `docs/architecture/` | The architecture corpus, architectural records, and its source navigation. | [`Architecture Handbook`](docs/architecture/README.md) |
| `docs/engineering/` | Engineering principles, technical decisions, project status, and related engineering context. | [`ENGINEERING_PRINCIPLES.md`](docs/engineering/ENGINEERING_PRINCIPLES.md) |
| `docs/decisions/` | Architecture and engineering decision records. | [`decisions/README.md`](docs/decisions/README.md) |

The directory named `docs/architecture/` has its own README titled
“Architecture Handbook.” It is part of the architecture corpus. The
`docs/handbook/ARCHITECTURE_HANDBOOK.md` file is a separate explanatory
handbook that helps readers navigate architecture; the two artifacts should not
be treated as interchangeable.

## 5. Which handbook should I read?

Use the question you are trying to answer to choose the first handbook:

| If you are asking… | Start with… | Then consult… |
| --- | --- | --- |
| “I am implementing code.” | [`AI_RULES.md`](docs/handbook/AI_RULES.md) for scope, source, and operating-lane expectations. | [`ARCHITECTURE_HANDBOOK.md`](docs/handbook/ARCHITECTURE_HANDBOOK.md), the [implementation index](docs/implementation/INDEX.md), and applicable engineering sources. |
| “I am reviewing.” | [`REVIEW_HANDBOOK.md`](docs/handbook/REVIEW_HANDBOOK.md) for review boundaries, evidence, findings, and confirmation distinctions. | The source and artifact under review, plus `AI_RULES.md` when AI work or repository safety is involved. |
| “I am changing architecture.” | [`ARCHITECTURE_HANDBOOK.md`](docs/handbook/ARCHITECTURE_HANDBOOK.md) for architectural source navigation and architecture-versus-implementation boundaries. | The [architecture corpus](docs/architecture/README.md) and the applicable architecture record. |
| “I am working with AI.” | [`AI_RULES.md`](docs/handbook/AI_RULES.md) and [`AI_COLLABORATION_GUIDE.md`](docs/handbook/AI_COLLABORATION_GUIDE.md). | The handbook that owns the underlying task: governance, review, architecture, implementation, or engineering. |
| “I am interpreting governance.” | [`GOVERNANCE_HANDBOOK.md`](docs/handbook/GOVERNANCE_HANDBOOK.md) for governance concepts and authority boundaries. | The applicable governance record and, where relevant, the [Constitutional Precedent Index](docs/governance/CONSTITUTIONAL_PRECEDENT_INDEX.md). |
| “I am writing repository documentation.” | [`docs/handbook/README.md`](docs/handbook/README.md) for the documentation map and boundaries. | The handbook or repository convention that owns the subject. |

The handbook is a navigation aid, not a substitute for the canonical artifact
that answers the question.

## 6. Contribution workflow

For a normal contribution, use this high-level flow:

1. **Frame the change.** Record the objective, intended scope, exclusions, and
   the source or convention that explains the work.
2. **Inspect before editing.** Read the relevant files, check repository state,
   and preserve unrelated changes.
3. **Make a bounded contribution.** Change only the files needed for the
   stated objective and keep adjacent ideas as clearly labelled follow-up
   suggestions.
4. **Verify the result.** Run checks appropriate to the artifact, such as
   tests, Markdown checks, link checks, or source-specific validation.
5. **Report the handoff.** Identify files changed, checks run, relevant
   limitations, unresolved questions, and the next responsible step.

This is an onboarding summary, not a replacement for a constitutional,
governance, review, or release procedure. If the work is governed by a specific
corpus or record, follow the applicable handbook and source for that work.

## 7. Good contribution practices

Useful contributions tend to share a few habits:

- keep the change scoped to the stated objective;
- preserve unrelated working-tree changes and repository history;
- explain the reason for a non-obvious decision or trade-off;
- use links to the source that owns a rule instead of copying its full text;
- distinguish facts, observations, recommendations, and unresolved questions;
- verify local links, formatting, tests, or other checks relevant to the files;
- state what was not inspected or verified; and
- make the next contributor’s starting point easy to reconstruct.

For AI-assisted work, keep the human-visible scope, source basis, actions, and
limitations explicit. The [AI Collaboration Guide](docs/handbook/AI_COLLABORATION_GUIDE.md)
provides the collaboration practices, while [AI Rules](docs/handbook/AI_RULES.md)
provides the operating boundaries.

## 8. Things to avoid

Avoid contribution patterns that make ownership, history, or authority unclear:

- mixing unrelated work into one change;
- editing a file merely to force an identity or comparison to match;
- inventing authority, approval, evidence, status, or repository facts;
- rewriting or normalizing a frozen artifact without an applicable source and
  process;
- treating a plan, recommendation, review result, or commit as permission for a
  later act;
- bypassing a review or verification required by the applicable source;
- presenting a repository convention as a constitutional requirement; and
- silently expanding a documentation task into implementation, architecture,
  governance, or policy work.

When one of these risks appears, stop at the boundary and consult the handbook
that owns the question. Do not solve an authority or scope ambiguity by making
the broadest convenient change.

## 9. Relationship to the handbook suite

`CONTRIBUTING.md` is the contributor-facing entry point. It answers where to
begin, maps repository areas, and points to the source that owns each topic.

The handbooks contain the detailed guidance:

- [AI Rules](docs/handbook/AI_RULES.md) covers AI operating boundaries, source
  tracing, repository safety, evidence, and reporting.
- [AI Collaboration Guide](docs/handbook/AI_COLLABORATION_GUIDE.md) covers
  human-AI collaboration, continuity, roles, communication, and handoffs.
- [Governance Handbook](docs/handbook/GOVERNANCE_HANDBOOK.md) explains
  governance concepts, authority boundaries, evidence, and lifecycle records.
- [Review Handbook](docs/handbook/REVIEW_HANDBOOK.md) explains review scope,
  findings, independent review, focused re-review, and confirmation.
- [Architecture Handbook](docs/handbook/ARCHITECTURE_HANDBOOK.md) explains
  architectural reasoning and navigation of architecture sources.

Read only the guidance relevant to the task, then follow the links to the
canonical repository artifact. None of these handbooks replaces the source
that establishes a requirement, decision, authority, or technical contract.

## 10. Related documents

- [Repository README](README.md) — product overview and repository orientation.
- [Handbook entry point](docs/handbook/README.md) — handbook inventory,
  audiences, reading order, and documentation boundaries.
- [AI Rules](docs/handbook/AI_RULES.md) — operating guidance for AI work.
- [Governance Handbook](docs/handbook/GOVERNANCE_HANDBOOK.md) — governance
  navigation and authority boundaries.
- [Review Handbook](docs/handbook/REVIEW_HANDBOOK.md) — review methodology and
  findings guidance.
- [Architecture Handbook](docs/handbook/ARCHITECTURE_HANDBOOK.md) — architecture
  navigation and reasoning guidance.
- [AI Collaboration Guide](docs/handbook/AI_COLLABORATION_GUIDE.md) — human-AI
  collaboration and handoff guidance.
- [Repository instructions](AGENTS.md) — repository-specific agent and graph
  navigation instructions.
- [Engineering principles](docs/engineering/ENGINEERING_PRINCIPLES.md) —
  engineering guidance and technical conventions.
- [Decision records](docs/decisions/README.md) — repository decision navigation.

When in doubt, state the question and scope, start with this guide, and follow
the link to the handbook or canonical source that owns the answer.

See the [Repository Documentation Handbook](docs/handbook/README.md) for the current documentation map.
