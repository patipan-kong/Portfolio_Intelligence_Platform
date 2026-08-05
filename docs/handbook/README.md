# Repository Documentation Handbook

## Handbook overview

This directory is the entry point for repository documentation guidance. It maps the handbooks that help AI agents and human contributors navigate repository rules, collaboration, governance, review, and architecture.

The initial handbook suite is complete in its current DRAFT form. Each handbook provides explanatory guidance for its subject and links to canonical repository sources. The handbooks remain distinct from authority, evidence, and implementation permission; their DRAFT status makes their current documentation state explicit.

## Design philosophy

The handbook system follows these principles:

- Give each concept one canonical home and link to it from elsewhere.
- Avoid duplicating constitutional text; reference canonical documents instead.
- Distinguish constitutional requirements from repository conventions.
- Distinguish governance from workflow.
- Distinguish authority from guidance.
- Keep documentation guidance separate from implementation authorization and work allocation.
- Make scope and status explicit so that guidance is not mistaken for an adopted requirement.

## Handbook inventory

| Handbook | Focus | Status |
| --- | --- | --- |
| [AI Rules](AI_RULES.md) | AI operating boundaries, source tracing, repository safety, evidence, and reporting | DRAFT |
| [AI Collaboration Guide](AI_COLLABORATION_GUIDE.md) | Human-AI collaboration, continuity, roles, communication, and handoffs | DRAFT |
| [Governance Handbook](GOVERNANCE_HANDBOOK.md) | Governance concepts, authority boundaries, evidence, and lifecycle records | DRAFT |
| [Review Handbook](REVIEW_HANDBOOK.md) | Review scope, findings, independent review, focused re-review, and confirmation | DRAFT |
| [Architecture Handbook](ARCHITECTURE_HANDBOOK.md) | Architectural reasoning and navigation of architecture sources | DRAFT |

## Intended audiences

- AI agents working in or documenting the repository.
- Human maintainers and contributors planning, reviewing, or implementing changes.
- Reviewers who need to separate evidence, guidance, governance, and authority.
- Future collaborators who need a concise map before reading detailed repository records.

## Recommended reading order

1. This README for the documentation map and boundaries.
2. [AI Rules](AI_RULES.md) for AI operating boundaries and repository safety.
3. [AI Collaboration Guide](AI_COLLABORATION_GUIDE.md) for collaboration, continuity, and handoffs.
4. [Governance Handbook](GOVERNANCE_HANDBOOK.md) for governance concepts and authority navigation.
5. [Review Handbook](REVIEW_HANDBOOK.md) for review scope, findings, and confirmation.
6. [Architecture Handbook](ARCHITECTURE_HANDBOOK.md) for architectural reasoning and source navigation.
7. The canonical documents linked by those handbooks, selected for the task at hand.

## Relationship to constitutional artifacts

The handbook system is documentation guidance only. It creates no constitutional authority, does not interpret or amend constitutional text, and does not replace the canonical governance records. The [Constitutional Precedent Index](../governance/CONSTITUTIONAL_PRECEDENT_INDEX.md) is a non-authoritative navigation document; its linked records remain the sources of their own stated content and limits.

Handbook language must not be treated as a holding, adoption, allocation, authorization, freeze, closeout, or other constitutional disposition. When constitutional meaning matters, consult the applicable canonical artifact directly.

## Relationship to implementation

Handbooks help readers find and use repository documentation. They do not authorize implementation, allocate work packages, define implementation requirements, or modify frozen artifacts. Implementation questions should be answered from the relevant [implementation index](../implementation/INDEX.md), architecture records, code, and tests, according to the scope of the task.

## Relationship to repository conventions

Repository conventions describe how work is organized and performed. They are distinct from constitutional requirements and should be maintained in their canonical locations. Relevant starting points include the [repository instructions](../../AGENTS.md), [CONTRIBUTING.md](../../CONTRIBUTING.md), [engineering principles](../engineering/ENGINEERING_PRINCIPLES.md), [decision records](../decisions/README.md), and [repository glossary](../GLOSSARY.md).

The handbooks link to those conventions and explain their relationship; they should not silently promote a convention into authority.

## Related documents

- [Repository README](../../README.md)
- [Documentation README](../README.md)
- [Constitutional Precedent Index](../governance/CONSTITUTIONAL_PRECEDENT_INDEX.md)
- [Architecture documentation](../architecture/README.md)
- [Implementation index](../implementation/INDEX.md)
- [Engineering principles](../engineering/ENGINEERING_PRINCIPLES.md)
- [Decision records](../decisions/README.md)
- [Repository glossary](../GLOSSARY.md)
