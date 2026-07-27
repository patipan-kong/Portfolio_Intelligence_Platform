1. Executive Summary
M42-WP3 should establish the canonical Investment Universe Declaration Contract.
Its sole architectural purpose is to define how one portfolio records its intended investment scope as inert, descriptive data. It does not determine whether an instrument belongs, validate a transaction, refuse an action, enforce a limit, or implement an engine.
The governing boundary is:
WP1-confirmed Investment Universe vocabulary
        +
WP2-confirmed Portfolio Identity / Accounting Scope
        +
Asset Foundation-owned descriptive vocabulary
        ↓
M42-WP3 Investment Universe Declaration
        ↓
M42-WP7 Portfolio Composition
WP3 is owned by Portfolio Intelligence, as a specialization of the already-frozen Portfolio Strategy Metadata allocation. Referenced Asset Foundation and Ledger & Accounting coordinates retain their existing owners.
This plan grants no implementation, runtime, persistence, API, provider, production, or executable-validation authority.
Authority was inspected read-only at origin/feature/m42-architecture, commit ccb712e.
2. Scope
WP3 governs exactly one semantic surface: the confirmed Investment Universe declaration.
The contract must define:
Its binding to exactly one Portfolio Identity and its corresponding Accounting Scope.
Its explicit declared name.
Its inert scope criteria.
The closed set of permitted criteria categories already authorized by WP1:Asset Classification, including the asset-classification dimension.
Capability.
Market.
Currency.

How criteria cite the corresponding Asset Foundation-owned values without copying, renaming, extending, or reclassifying them.
The declaration’s immutable-until-explicitly-revised semantic condition.
The exact downstream handoff to M42-WP7.
A negative corpus proving that the declaration cannot evaluate a specific instrument or produce a verdict.
The contract may define an implementation-neutral record shape in Stage B. It may not define a database, API model, runtime object, validation function, or storage mechanism.
WP3 must not assume an ambient universe, an implicit default, or a concrete instrument list. Each declaration is explicitly portfolio-scoped.
3. Responsibilities
WP3 responsibilities
Portfolio Intelligence is responsible for:
Defining Investment Universe solely as descriptive strategy data.
Closing the permitted criteria-category surface.
Defining a deterministic, inert representation suitable for later composition.
Ensuring every criterion is an exact reference to Asset Foundation-owned vocabulary.
Preserving the distinction between strategy scope and accounting scope.
Preserving the distinction between declaration and enforcement.
Supplying documentation-only examples, negative cases, and golden vectors.
Producing an unambiguous handoff for WP7 without defining WP7’s Portfolio Composition.
Responsibilities retained elsewhere
Ledger & Accounting: Portfolio Identity, Accounting Scope, Portfolio Membership, and Portfolio Base Currency.
Asset Foundation: Asset Classification, Capability, market classification, currency of denomination, and their values.
Decision Intelligence: Any future instrument-level evaluation, constraint enforcement, refusal, or verdict.
M42-WP7 / Portfolio Intelligence: Terminal Portfolio Composition, canonical portfolio-level serialization, and composition determinism.
Experience Platform: Presentation of a later composed surface.
Connectivity & Ingestion: Provider-facing acquisition and provenance mechanisms.
No ownership transfers occur through citation or composition.
4. Architecture
4.1 Contract structure
The WP3 Stage B contract should contain five logical sections:
Subject binding
The declaration identifies one Portfolio Identity.
It presupposes the same Accounting Scope established by WP2.
It cannot be ambient, shared implicitly, or used to create an alternate accounting boundary.

Declared identity
An explicit declared name.
No standardized catalogue of universe names is created.
Examples such as “Thai Equity” remain illustrative, not canonical enumerations.

Scope criteria
Criteria are inert data expressed only through the four WP1-approved categories.
Values are references to Asset Foundation authority.
No provider values, UI labels, cached copies, or private taxonomies become canonical.

Revision boundary
The declaration is immutable until explicitly revised.
WP3 defines this semantic condition but not an event schema, command, workflow, persistence strategy, or runtime update mechanism.
Revision must never silently rewrite historical meaning.

WP7 handoff
WP7 receives the confirmed Investment Universe declaration as a complete Portfolio Intelligence-owned coordinate.
WP7 may carry it but may not evaluate, repair, enrich, or reinterpret it.
Portfolio-wide canonical serialization remains WP7’s responsibility.

4.2 Semantic invariants
WP3 should freeze these invariants:
Declaration only: It states intended scope; it produces no answer about an instrument.
One-way reference: It references Asset Foundation facts; it never owns or changes them.
Boundary consistency: It belongs to one Portfolio Identity and never redefines Accounting Scope.
No enumeration of holdings: It does not maintain a concrete instrument list.
No default: Missing scope cannot be repaired with an ambient or inferred declaration.
No verdict: There is no met/unmet, belongs/does-not-belong, valid/invalid, or refusal output.
No enforcement: Criteria are not Portfolio Limits, Decision Policy, optimizer constraints, or execution eligibility.
No derived measure: It contains no performance, risk, exposure, allocation, or valuation result.
No provider dependency: Meaning is independent of live providers, wall-clock state, and model output.
4.3 Important cardinality boundary
Each Investment Universe declaration binds to exactly one Portfolio Identity and its corresponding Accounting Scope.
WP3 does not determine whether a portfolio has zero, one, or multiple declarations. Any portfolio-side cardinality rule requires future explicit frozen authority.
5. Interfaces
Interface	Exact WP3 use	Prohibited WP3 behavior
M42 Architecture	Component C purpose, owner, gates, negative corpus	Redesigning the milestone or adding enforcement
M42-WP1	Reuse confirmed Investment Universe admission and ownership	New nouns, renamed criteria, or revival of rejected Investment Universe Membership
M42-WP2	Cite Portfolio Identity and Accounting Scope as subject boundary	Redefining identity/scope or introducing another boundary
Portfolio Base Currency	Citation only if needed to distinguish reporting currency from universe currency criteria	Using it as a default criterion or copying its value into a competing coordinate
Asset Classification	Reference canonical descriptive classifications	Private classifications or hard-coded WP3 taxonomy
Capability	Reference existing queryable behavior facts	Inventing new capabilities or evaluating an asset
Market/currency classification	Reference Asset Foundation-owned coordinates	Minting identifier formats or parallel enumerations
M42-WP7	Hand off the exact confirmed declaration	Defining Portfolio Composition or portfolio-wide serialization
Future Decision Intelligence	May eventually consume the declaration under separate authority	WP3 defining membership checks, refusals, or enforcement

WP5 and WP6 are parallel siblings, not upstream dependencies or WP3 consumers.
6. Dependencies
Mandatory upstream authority
Frozen Platform Architecture and domain constitutions.
Frozen M34 ownership decisions, especially M34-D-0002, M34-D-0004, and M34-D-0007.
Frozen M42 Architecture Proposal.
Confirmed M42-WP1 register:Investment Universe is ADMIT.
Owner is Portfolio Intelligence.
It specializes Portfolio Strategy Metadata.
Investment Universe Membership is REJECT.

Confirmed M42-WP2:Portfolio Identity.
Accounting Scope.
Boundary-integrity invariant.
Replay-never-crosses-a-boundary invariant.
Portfolio Base Currency ownership and citation discipline.

Frozen Asset Foundation authority for Asset Classification, Capability, market, and currency-of-denomination facts.
Downstream consumers
Direct normative consumer: M42-WP7 Portfolio Composition.
Indirect future consumers through the composed surface: portfolio analytics, Experience rendering, Decision Intelligence, Wealth Intelligence, and evaluation surfaces.
These future consumers receive no authority from WP3 to evaluate membership or enforce the declaration.
7. Out-of-Scope
WP3 explicitly excludes:
Investment Universe Membership.
Any belonging predicate or instrument-specific question.
Evaluation, validation, refusal, or enforcement.
Portfolio Policy, Decision Policy, Portfolio Limits, and Sector Limits.
Concrete instrument lists or stored membership facts.
Portfolio Membership, which remains a Ledger fact with different meaning.
Creation of new Asset Classification, Capability, market, or currency vocabulary.
Provider, broker, symbol, exchange-adapter, or transport knowledge.
Portfolio Base Currency ownership or mutation.
Accounting calculations and ledger behavior.
Performance, return, benchmark comparison, risk, attribution, exposure, or allocation.
Optimization, recommendation, suitability, ranking, or forecasting.
Lifecycle commands or revision workflows.
Portfolio Composition and portfolio-wide canonical serialization.
Database schemas, migrations, endpoints, runtime services, UI components, or production code.
Executable validators or committed test runners.
Decision Log, Implementation Index, Glossary, or Graphify changes before the appropriate approved closeout stage.
8. Risks
Evaluation leakage — critical.
Sets, ranges, operators, or examples may accidentally become a truth-valued matching language. Stage B must define representation without defining instrument evaluation.

Policy collision — high.
Market, classification, and currency criteria can resemble the rejected Portfolio Policy fields. WP3 must consistently describe intended scope and avoid words or behavior such as “allowed,” “prohibited,” “eligible,” or “enforced.”

Asset Foundation duplication — high.
WP3 could accidentally create its own enumerations or identifier formats. Every value must remain an exact Asset Foundation reference.

Membership confusion — high.
Investment Universe, rejected Investment Universe Membership, and Ledger-owned Portfolio Membership are three distinct meanings. Reviews must verify they are never collapsed.

Base-currency confusion — medium.
An asset currency criterion is not Portfolio Base Currency. WP3 must not use the latter as an implicit criterion or define conversion behavior.

Revision-authority expansion — medium.
“Explicitly revised” could grow into commands, events, schemas, or lifecycle rules. WP3 may state the semantic condition only.

WP7 overlap — medium.
Defining portfolio-wide serialization or composition in WP3 would duplicate terminal WP7 authority.

Identifier-format gap — medium.
WP2 confirms that Asset Foundation has not frozen an exact currency identifier format. WP3 must cite the owned coordinate and must not fill this gap by inventing a format.

9. Recommended Implementation Sequence
“Implementation” here means the governed documentation sequence only.
WP3 Architecture Proposal
Freeze purpose, owner, interfaces, semantic invariants, negative corpus, and downstream handoff.
Independent architecture review, correction response if required, and unconditional confirmation.

Stage A Vocabulary and Semantic Surface Register
Reuse confirmed Investment Universe.
Register Portfolio Strategy Metadata, Portfolio Identity, Accounting Scope, Asset Classification, and Capability as cited/reused authority.
Record Investment Universe Membership as excluded because WP1 rejected it.
Admit no new vocabulary.
Independent review and confirmation.

Stage B Contract Specification
Define subject binding.
Define the inert declaration shape.
Close the four permitted criteria categories.
Define exact reference and non-owner rules.
Define the revision semantic boundary.
Define the WP7 handoff.
Include a field-by-field five-part ownership gate.

Documentation-only golden vectors
Valid single- and multi-category declarations.
Invalid ambient default.
Invalid concrete instrument list.
Invalid provider-owned value.
Invalid executable expression.
Invalid belonging verdict or refusal.
Invalid Portfolio Policy or Portfolio Limit field.
Invalid competing classification or currency enumeration.
Invalid cross-portfolio subject.
Valid WP7 citation with no evaluation or enrichment.

Independent Stage B review and confirmation
Require zero unresolved ownership, semantic, or negative-corpus findings.

WP3 Closeout
Record WP3 as complete and frozen.
Synchronize only the governance artifacts authorized by the approved closeout procedure.
Grant no code or operational authority.

10. Acceptance Criteria
WP3 is acceptable only if independent review confirms all of the following:
Its sole governed noun is the already-confirmed Investment Universe.
Ownership remains Portfolio Intelligence, as a specialization of Portfolio Strategy Metadata.
Each declaration is bound to one Portfolio Identity and preserves WP2’s Accounting Scope.
The permitted declaration inputs are limited to an explicit name, the portfolio reference, and inert criteria in the four WP1-authorized categories.
Every criterion value cites Asset Foundation authority without duplicating its taxonomy or identifier formats.
No concrete instrument list is stored as the universe.
No executable function, matching expression, truth-valued predicate, evaluation result, or refusal exists.
Rejected Investment Universe Membership is not reintroduced under another name.
Ledger-owned Portfolio Membership remains semantically distinct.
Portfolio Policy, Decision Policy, Portfolio Limits, and enforcement behavior are absent.
Portfolio Base Currency remains Ledger & Accounting-owned and is not treated as an implicit universe criterion.
The declaration has no ambient default and no provider, clock, model, or live-state dependency.
Revision is bounded semantically without defining commands, events, persistence, or runtime mechanics.
WP7 receives a complete, unambiguous declaration coordinate without WP3 assuming WP7’s composition or serialization authority.
Golden vectors demonstrate both valid declaration shapes and all material prohibited shapes.
M42 Architecture, WP1, WP2, M34, and Asset Foundation authority are cited without amendment or reinterpretation.
Implementation, runtime, provider, persistence, API, production, executable-validation, and enforcement authority remain NONE.