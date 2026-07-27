M42-WP6 Proposed Architectural Specification
1. Executive Summary
Recommendation: ADMIT
M42-WP6 is admissible as one narrow constitutional work package, but only under this construction:
The sole normative subject is Portfolio Lifecycle State. Provenance is a reused, citation-only carriage requirement attached to that subject and to the portfolio coordinates handed forward to WP7.

The ownership allocation is:
Surface	Meaning	Semantic owner
Portfolio Lifecycle State	Recorded active, archived, or closed state of one permanent Portfolio Identity	Ledger & Accounting
Capture-time Provenance	Where an entering fact came from	Connectivity & Ingestion
WP6 provenance carriage rule	Preservation and citation of existing provenance without recapture or reinterpretation	Ledger & Accounting as WP6 owner
Portfolio Composition carriage	Terminal composition of lifecycle and lineage into the Portfolio read surface	Portfolio Intelligence in WP7

Lifecycle State and Provenance are therefore not one concept and do not have the same source owner. They may nevertheless remain in one WP because WP6 does not acquire Provenance ownership. This follows the already-approved M41 pattern: a result owner may govern provenance carriage while Connectivity & Ingestion retains capture-time ownership.
No new noun such as Portfolio Provenance, Lifecycle Provenance, Lifecycle Event, or Lifecycle Transition should be admitted.
The frozen M42 architecture already classifies WP6 as reuse-only and assigns it to Ledger & Accounting ([M42 Architecture, Component F (line 336)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/implementation/M42_ARCHITECTURE_PROPOSAL.md:336)).
2. Constitutional Question
The constitutional question is not:
“Who owns both Lifecycle State and Provenance?”

They have different existing owners.
The admissible question is:
“May Ledger & Accounting specify how the already-owned Portfolio Lifecycle State is cited and how already-owned provenance is preserved when that state and other portfolio coordinates are handed to Portfolio Composition?”

The answer is yes, provided that:
Portfolio Lifecycle State remains the only governed subject of WP6.
Provenance retains its existing generic meaning: where a fact came from.
WP6 specifies carriage and preservation only.
Carriage creates no capture, adjudication, source-selection, or audit authority.
Every carried coordinate retains its own source owner.
WP7 remains the owner of terminal Portfolio Composition.
No lifecycle-transition or action-eligibility meaning is inferred.
This preserves “one term, one meaning, one owner” by keeping the two existing terms distinct:
Portfolio Lifecycle State → Ledger & Accounting
Provenance at capture → Connectivity & Ingestion
The WP has one primary constitutional owner—Ledger & Accounting—without claiming exclusive authority over its cited dependency.
3. Ownership Investigation Plan
The WP6 governance sequence should be:
Phase 1 — Authority freeze
Establish the binding authority hierarchy and a non-reopening statement. No interpretation may widen M34, M36, M42-WP1, or the Glossary.
Phase 2 — Vocabulary sufficiency
Test whether the surface can be expressed entirely through:
Portfolio Identity — REUSE
Accounting Scope — REUSE
Portfolio Lifecycle State — REUSE
Provenance — REUSE
provenance carriage / lineage completeness — ordinary contract language
Expected result: no candidate vocabulary and no Glossary addition.
Phase 3 — Surface ownership matrix
For every proposed semantic statement, record:
governed term;
exact meaning;
semantic owner;
authoritative source;
WP6’s permitted operation;
prohibited reinterpretations;
downstream handoff.
Phase 4 — Overlap investigation
Run explicit non-duplication tests against Ledger & Accounting, Connectivity & Ingestion, Portfolio Intelligence, Decision Intelligence, Asset Foundation, Market Intelligence, Wealth Intelligence, and Experience Platform.
Phase 5 — Dependency and consumer proof
Prove that WP6 depends on the frozen WP2 accounting subject and supplies only lifecycle-plus-lineage semantics to WP7.
Phase 6 — Governed artifact sequence
Follow the frozen sequence:
WP6 Architecture Proposal
Independent Architecture Review and Confirmation
Stage A Vocabulary and Semantic Surface Register
Independent Stage A Review and Confirmation
Stage B Contract Specification
Independent Stage B Review and Confirmation
WP6 Closeout
This is documentation and semantic governance work only. It authorizes no implementation.
4. Candidate Semantic Surface
A. Portfolio Lifecycle State
The existing definition remains exact:
The recorded active, archived, or closed lifecycle state of one Portfolio Identity. It qualifies what the portfolio may do next and never rewrites Portfolio Identity, Accounting Scope, ledger history, or evaluation history.

It is explicitly distinct from Portfolio Status, Current Selection, availability, permission, authority, action eligibility, and transition legitimacy ([Glossary (line 594)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/GLOSSARY.md:594)).
No additional state—including draft, pending, suspended, deleted, imported, merging, or pre-activation—may be introduced.
B. Reuse
“Reuse” means:
exact citation of an already-governed term;
unchanged meaning;
unchanged owner;
unchanged vocabulary;
no new cardinality or transition rule;
no implementation inference.
It does not mean code reuse, object reuse, runtime-state reuse, cached-state reuse, cloning, copying, or restoring persisted state.
C. Provenance
Provenance retains the frozen generic meaning: where a fact came from ([Glossary (line 257)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/GLOSSARY.md:257)).
For WP6, provenance means only:
retain existing source-owned lineage;
cite it without recapture;
prevent a lifecycle or composition projection from obscuring or laundering its origin;
preserve ownership attribution across the handoff to WP7.
WP6 must not define new provenance fields, evidence classes, trust grades, audit structures, provider rules, or lineage storage.
D. Relationship between State and Provenance
Provenance is not Portfolio Lifecycle State and does not determine its value.
Provenance is evidence of the state fact’s origin, not proof that:
the state is correct;
a transition was legitimate;
an actor was authorized;
an operation is permitted;
the portfolio is available;
the state is current at runtime.
Conversely, a lifecycle-state value does not manufacture, replace, or validate provenance.
E. Portfolio-surface carriage
The M42 phrase “provenance/lineage every portfolio-scoped fact carries” should be interpreted narrowly:
Every coordinate carried into Portfolio Composition retains whatever provenance and owner attribution its governing source supplies.

It must not mean that Ledger & Accounting becomes the provenance owner for Investment Universe, Benchmark declarations, Market observations, Asset references, or other domains’ facts.
5. Governing Authorities
In descending order:
Platform Architecture
Ledger & Accounting owns recorded financial truth and replayable state ([§6.3 (line 203)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/architecture/platform_architecture.md:203)).
Connectivity & Ingestion owns provenance at capture and provides proposed events with lineage ([§6.4 (line 217)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/architecture/platform_architecture.md:217)).

M34-D-0002
Decomposes the Portfolio container across existing constitutional domains and rejects a hidden single Portfolio owner ([decision (line 153)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/implementation/m34/audit/registers/decision_register.md:153)).

M36 Multiple-Portfolio Foundation
M36-WP1-A01: lifecycle is distinct from Current Selection.
M36-WP1-A09: identity and history survive transitions; transition legitimacy remains separate ([decision register (line 583)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/implementation/M36_WP1_Multiple_Portfolio_Foundation.md:583)).
Exact state vocabulary is active, archived, closed ([invariants (line 607)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/implementation/M36_WP1_Multiple_Portfolio_Foundation.md:607)).

Frozen M42 Architecture
Assigns WP6 to Ledger & Accounting as reuse-only.
Prohibits transition vocabulary and cites Connectivity & Ingestion as provenance owner ([WP6 allocation (line 440)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/implementation/M42_ARCHITECTURE_PROPOSAL.md:440)).

M42-WP1
Records Portfolio Lifecycle State as an already-frozen reused coordinate.
Allows Portfolio Composition to cite lifecycle and provenance without ownership transfer.

Canonical Glossary
Supplies the exact Portfolio Lifecycle State and Provenance meanings.

Portfolio Domain Model
Descriptive design-of-record only.
Its transition descriptions cannot override M36’s explicit deferrals.

A useful precedent is M41-WP4: Connectivity & Ingestion retains capture-time Provenance while another domain owns result carriage/composition ([M41 Stage A surface F (line 302)](/D:/Works/TA/work/Portfolio_Intelligence_Platform/docs/implementation/M41_WP4_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md:302)).
6. Dependency Graph
Platform Architecture
  ├─ Ledger & Accounting authority
  └─ Connectivity & Ingestion provenance authority
                 │
                 ▼
             M34-D-0002
                 │
                 ▼
     M36-WP1-A01 / M36-WP1-A09
                 │
                 ▼
       M42 Architecture + M42-WP1
                 │
                 ▼
 M42-WP2 Identity / Accounting Scope contract
                 │
                 ▼
 M42-WP6 Lifecycle reuse + provenance carriage
                 │
                 ▼
 M42-WP7 Portfolio Composition and Projection
                 │
                 ▼
           M42 Epic Closeout
WP6 depends on WP2 because lifecycle qualifies one exact Portfolio Identity and its corresponding Accounting Scope. WP6 must not manufacture an alternative portfolio subject.
7. Included Scope
WP6 may include:
exact reuse of active, archived, and closed;
confirmation that the state qualifies one permanent Portfolio Identity;
preservation of identity, Accounting Scope, ledger history, and evaluation history;
future-only semantic effect without defining how change occurs;
disambiguation from Portfolio Status, Current Selection, availability, authority, permission, degradation, and action eligibility;
citation-only preservation of existing provenance;
owner and lineage preservation across the WP7 handoff;
a semantic dependency and downstream-consumer matrix;
documentary examples or golden vectors that contain no executable mechanism;
explicit NONE declarations for every implementation authority.
8. Explicitly Excluded Scope
WP6 must exclude:
lifecycle state machines and transition graphs;
lifecycle commands or workflows;
create, activate, archive, close, clone, merge, import, or export behavior;
transition legitimacy or approval;
rules determining which state permits which read or write;
authorization, permission, access control, or actor identity;
Current Selection and workspace navigation;
Portfolio Status or other analytical status;
persistence, schemas, migrations, backfills, defaults, or deletion;
events, event sourcing, audit logs, or audit-log retention;
APIs, serialization, synchronization, caching, or orchestration;
provider adapters and import/export integrations;
source adjudication, reconciliation, deduplication, or confidence scoring;
provenance capture or a new Portfolio-specific provenance taxonomy;
validation engines, executable tests, runtime enforcement, or production adoption;
investment-universe evaluation;
benchmark selection or computation;
market-observation provenance reinterpretation;
asset lifecycle or Asset Foundation lifecycle vocabulary;
performance, valuation, risk, exposure, recommendation, or other derived measures.
Implementation, runtime, provider, persistence, API, production, and executable-validation authority must all remain NONE.
9. Candidate Acceptance Criteria
WP6 should be acceptable only if Independent Review confirms:
Portfolio Lifecycle State is reused exactly as active, archived, or closed.
Ledger & Accounting remains its sole semantic and constitutional owner.
Provenance retains its existing meaning and capture-time ownership.
WP6 owns only provenance carriage for its semantic surface, not provenance capture.
No Portfolio-specific provenance noun is introduced.
No lifecycle transition, command, workflow, legitimacy, eligibility, or authorization meaning is authored.
Every lifecycle-state citation resolves to one exact Portfolio Identity and its WP2 Accounting Scope without redefining either.
Identity and recorded history cannot be rewritten, re-keyed, merged, or deleted by lifecycle qualification.
Provenance is not treated as proof of state correctness, transition legitimacy, authority, or action eligibility.
Lifecycle state is not treated as provenance, availability, Current Selection, Portfolio Status, permission, or degradation.
Every carried external coordinate retains its original semantic owner and exact meaning.
Asset Foundation lifecycle, Market Intelligence observation provenance, Portfolio Intelligence declarations, and Decision Intelligence judgment remain outside WP6 ownership.
WP7 receives only confirmed lifecycle and lineage citations—no derived value or operational coordinate.
The complete negative corpus is explicit.
All implementation authorities remain NONE.
No frozen M34, M36, M42-WP1–WP5, Glossary, or domain-contract statement is redesigned.
10. Recommendation
ADMIT — with a mandatory narrow-scope condition.
WP6 should remain a single work package because its admissible semantic surface is:
Portfolio Lifecycle State reuse, with provenance preservation as a subordinate carriage rule.

It should not be split merely because the carried evidence has an upstream owner. Citation across domain boundaries is normal and already constitutionally proven.
A split becomes mandatory only if future drafting attempts to:
define provenance independently;
introduce Portfolio Provenance or Lifecycle Provenance;
regulate capture, adapters, reconciliation, providers, evidence stores, or audit mechanisms; or
govern provenance for all portfolio-related facts independently of their producing domains.
Those concerns belong to Connectivity & Ingestion or the relevant producing domain and would require a separately chartered work package.
Lifecycle transitions would likewise require a separate non-reuse admission. They must not be rescued by broadening WP6.