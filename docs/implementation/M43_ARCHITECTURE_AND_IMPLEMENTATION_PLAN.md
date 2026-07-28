M43 Architecture and Implementation Plan
Milestone: M43 — Portfolio Analytics Contract Foundation
Proposed status: READY FOR INDEPENDENT ARCHITECTURE CONFIRMATION
Milestone class: Specification, canonical-method, validation-fixture, and implementation-design milestone
Runtime authority: NONE
Source-code authority: NONE
Persistence/API/UI authority: NONE
Implementation authority: NONE
Provider authority: NONE
Production-method authority: NONE
Executable-validation authority: NONE
This plan does not itself amend or activate repository authority. It becomes canonical only after the normal independent architecture review, correction, and confirmation sequence.
1. Roadmap position
M43 is the next Phase 3 Portfolio Intelligence milestone.
M39                 M40–M41                 M42                    M43
Market Observation → Market Measure rules → Portfolio Composition → Portfolio Analytics contracts
what was observed    how market facts are    what a Portfolio is    what can be derived
                     deterministically       as a governed object   about one Portfolio
                     measured
This placement follows the frozen [M42 Architecture Proposal](M42_ARCHITECTURE_PROPOSAL.md) §10, which anticipates “M43+ — Portfolio Analytics Foundation” as the first consumer of Portfolio Composition.
M43 advances the following Phase 3 roadmap capabilities without yet deploying them:
Rolling Analytics.
Advanced Risk Metrics.
Position Attribution.
Sector Attribution Timeline.
M43 precedes:
executable Portfolio Analytics registry and kernel work;
public analytics API cutover;
Experience-layer adoption;
Wealth Intelligence aggregation;
Decision Intelligence consumption;
Trust & Evaluation consumption.
2. Architectural conclusion
M43 should be specification-only.
Combining new vocabulary, ownership decisions, formula governance, first executable code, persistence, and public cutover into one milestone would repeat the scope compression that [M41](M41_ARCHITECTURE_PROPOSAL.md) explicitly rejected.
M43 therefore defines everything a later implementation milestone must implement, but does not itself implement the runtime.
M43 admits no production method. Every method definition, method version, formula specification, worked example, and validation fixture produced by M43 remains non-production until separately authorized by a later milestone.
This boundary preserves incremental review:
M43 establishes the Portfolio Analytics language and contracts.
It freezes canonical method definitions and validation vectors.
It produces the implementation and cutover design.
A separately authorized successor implements the registry, pure kernel, adapters, and adoption sequence.
3. Architectural objective
Establish the canonical, implementation-neutral contract for deterministic Portfolio Analytics:
Given one exact M42 Portfolio Composition, exact Ledger & Accounting-derived evidence, exact Market Intelligence evidence, explicit invocation parameters, and explicitly versioned calculation dependencies, produce an immutable, reproducible, provenance-preserving Portfolio measure result under one canonical method version, with no ambient defaults, no provider knowledge, no judgment semantics, and no cross-portfolio leakage.

M43 must establish:
candidate vocabulary and single ownership;
measure definition and method-version contracts;
subject and input-manifest contracts;
temporal, currency, unit, calendar, benchmark-alignment, and arithmetic rules;
input-sufficiency and degraded-state behavior;
immutable result identity, serialization, lineage, and Provenance carriage;
canonical specifications for core performance, risk, benchmark-relative, and attribution method families;
the implementation, compatibility, shadow-validation, and cutover design for a later milestone.
4. Capability gap addressed
The platform already computes many analytics, but it lacks a canonical Portfolio Analytics contract.
Current implementation evidence includes:
ORM-shaped inputs rather than a governed input manifest;
request-supplied or hard-coded benchmark symbols;
a hard-coded risk-free rate;
implicit 252-day annualization assumptions;
fallback from cash-flow-adjusted return to raw NAV percentage change;
private in-process analytics caching;
multiple implementations of drawdown, volatility, and attribution-related calculations;
no method-version identity;
no immutable result identity or canonical serialization;
incomplete lineage and degraded-state semantics;
no runtime consumption of M42 Portfolio Composition.
These are current-state findings, not precedent. Constitution G6 says code records reality but does not define intended architecture.
M43 closes the gap between:
M42’s governed definition of a Portfolio; and
a future production analytics engine capable of deriving defensible measures from it.
5. Non-goals and explicit exclusions
M43 does not:
implement executable contracts, registries, kernels, adapters, APIs, UI, schemas, migrations, schedulers, caches, or persistence;
commit executable validation artifacts, executable fixtures, test runners, or conformance harnesses;
admit or activate any production method, provider integration, or executable calculation;
implement M42 Portfolio Composition persistence or lifecycle commands;
originate or change Portfolio Identity, Accounting Scope, Portfolio Membership, Portfolio Base Currency, Investment Universe, Benchmark Declaration, Lifecycle State, or Provenance;
modify accounting arithmetic or compute_period_metrics();
resolve the open accounting questions in PORTFOLIO_CALCULATION_RULES.md;
infer missing Portfolio Base Currency, lifecycle state, Investment Universe, Benchmark Declaration, or Provenance;
admit Portfolio Policy or any renamed equivalent;
implement Investment Universe membership or eligibility;
compute cross-portfolio exposure, net worth, or Wealth analytics;
produce recommendations, rankings, suitability, constraint decisions, optimization, forecasts, or execution instructions;
grade recommendations or produce Trust & Evaluation verdicts;
specify Sector BHB decomposition or benchmark-relative attribution;
treat request-selected benchmarks as the portfolio’s declared benchmark;
use provider symbols or provider calls as canonical calculation inputs;
reinterpret M41 Market Measure contracts to accept Portfolio subjects;
bless existing legacy analytics behavior merely because it is deployed;
remove or modify legacy endpoints;
backfill historical analytic results;
update frozen M1–M42 artifacts.
Recommendation attribution, human-vs-AI attribution, regime attribution, and causal explanations remain Trust & Evaluation or Decision Intelligence concerns. M43 attribution is limited to deterministic decomposition of portfolio return.
6. Dependencies
Hard dependencies
Platform Architecture Laws 1–15, especially deterministic derivation, loud degradation, one implementation per rule, and Experience computing nothing.
M34 ownership allocations.
M36 Portfolio Identity and workspace-referenceability contracts.
M39 Market Observation contracts.
M40–M41 Market Measure vocabulary and contracts.
M42 Portfolio Identity, Accounting Scope, Base Currency, Benchmark Declaration, Lifecycle State, Provenance, and Portfolio Composition contracts.
[Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md).
ADR-001 through ADR-005.
Dependency interpretation
M43 may reuse M41’s mechanical patterns:
immutable definitions;
method versions;
explicit applicability;
input manifests;
canonical serialization;
input sufficiency;
degraded states;
result identity;
golden vectors.
It may not reuse Market Intelligence-owned contract types as if they accepted Portfolio subjects. M43 requires independently governed Portfolio Intelligence vocabulary.
7. Architectural boundaries
Permitted subject
Exactly one M42 Portfolio Composition representing one Portfolio Identity and its corresponding Accounting Scope.
No ambient Current Selection, Workspace default, cross-portfolio aggregate, person, household, or Wealth subject is permitted.
Permitted inputs
Only:
one exact M42 Portfolio Composition;
Ledger & Accounting-owned, ledger-derived portfolio evidence;
exact M39 observations or M41 Market Measure Results;
Asset Foundation-owned identity, classification, currency, or taxonomy references;
explicit invocation parameters;
explicit governed Portfolio-measure calculation dependencies;
already-captured Provenance associated with those inputs.
Explicit invocation parameters may select only choices that a confirmed method contract classifies as invocation-bound. They may not supply or override the Portfolio Benchmark Declaration, risk-free input, annualization basis, calendar authority, or any other governed evidence or calculation dependency.
Prohibited inputs
live provider answers;
provider identifiers used as canonical identity;
wall-clock time;
Current Selection;
inferred Portfolio Base Currency;
request-default benchmarks;
hidden risk-free rates;
hidden calendars or annualization factors;
unversioned sector classifications;
cross-portfolio state;
model output;
recommendation, optimizer, or evaluation results used as measurement truth.
Output meaning
An immutable Portfolio-derived knowledge result.
The output may describe performance, risk, benchmark-relative behavior, or deterministic contribution. It may not decide what should be done or whether a recommendation was good.
Required flow
M42 Portfolio Composition
Ledger-derived portfolio evidence
M39/M41 market evidence
Asset Foundation references
Explicit parameters and dependencies
              │
              ▼
Portfolio Analytics Input Manifest
              │
              ▼
Versioned pure Portfolio method
              │
              ▼
Immutable Portfolio measure result
              │
       ┌──────┼────────┐
       ▼      ▼        ▼
 Experience Decision  Trust & Evaluation
 renders    consumes  independently observes
8. Subsystem ownership
Subsystem or concern	Owner	Ownership status and authority	M43 relationship
Portfolio Identity, Accounting Scope, Membership, Base Currency	Ledger & Accounting	FROZEN — M42-WP2 and M42-WP7	Exact citation only
Ledger events, replay, and snapshots	Ledger & Accounting	FROZEN — Platform Laws 1–3; ADR-001 through ADR-004	Authoritative evidence; never redefined
Canonical period-return rule	Candidate: Ledger & Accounting	OWNER TO PROVE AT WP1 — Constitution §§6.3/6.5, ADR-001/004, and PORTFOLIO_CALCULATION_RULES.md §10	WP6 is blocked until disposition; no second rule is permitted
Portfolio Composition	Portfolio Intelligence	FROZEN — M42-WP7	Exact governed subject
Portfolio-derived measures	Portfolio Intelligence	FROZEN — Constitution §6.5 and M40-WP1 §8.3	M43’s owning-domain scope
Portfolio Benchmark Declaration	Portfolio Intelligence	FROZEN — M42-WP5	Declared comparison choice; not benchmark data
Benchmark observations, FX, calendars, market reference measures	Market Intelligence	FROZEN — Constitution §6.2 and M39–M41	Exact governed evidence supplied to M43
Asset identity, currency dimension, Asset Classification, sector/classification taxonomy	Asset Foundation	FROZEN — Constitution §6.1 and M34-D-0004	Exact versioned references
Analytical Grouping	Portfolio Intelligence	FROZEN — M34-D-0004	Distinct from Asset Classification; WP8 must disposition its attribution-grouping use explicitly
Provenance meaning and capture	Connectivity & Ingestion	FROZEN — M34-D-0010 and M42-WP6	Preserved and carried, never reconstructed
Recommendations, constraints, optimization, actions	Decision Intelligence	FROZEN — Constitution §6.6	Downstream consumer; excluded from calculation
Grades, causal evaluation, human-vs-AI	Trust & Evaluation	FROZEN — Constitution §6.7	Independent downstream observer
Rendering and interaction	Experience Platform	FROZEN — Constitution §6.9 and §7.3	Renders results; computes nothing
Cross-portfolio exposure and net worth	Wealth Intelligence	FROZEN — Constitution §6.8 and M34-D-0003	Explicitly excluded

M43 pre-owns and pre-admits nothing. WP1 must prove every candidate allocation before a downstream contract relies on it; a failed or unresolved proof blocks that dependency rather than creating an implicit owner.

9. Work-package decomposition
M43-WP1 — Roadmap, Current-State, Vocabulary, and Ownership Register
Purpose: Establish the complete M43 vocabulary and prevent legacy code from silently defining the architecture.
Scope:
roadmap reconciliation;
inventory of existing formulas, endpoints, defaults, fallbacks, caches, persistence, and consumers;
candidate vocabulary register;
ownership and overlap analysis;
legacy-to-canonical disposition matrix.
Deliverables:
M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md;
M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md;
candidate dispositions of ADMIT, REUSE, RENAME, or REJECT;
negative corpus;
source inventory and duplicate-rule map.
Candidate terms include, without pre-admission:
Portfolio Measure;
Portfolio Measure Definition;
Portfolio Method Version;
Portfolio Measure Subject;
Portfolio Analytics Input Manifest;
Portfolio Measurement Window;
Portfolio Input Sufficiency;
Portfolio Measure Result;
Portfolio Computation Outcome;
Portfolio Deterministic Calculation;
Portfolio Degraded State.
The last three rows must determine whether a Portfolio-prefixed noun is required or whether M43 explicitly REUSES an existing owned term. WP1 must cite M40-WP1 §8.3, including its frozen rule that UNAVAILABLE remains a Degraded State and must not become a Computation Outcome. M40-WP1 §8.3 also supplies the existing reservation of portfolio measure, portfolio performance, attribution, exposure, and portfolio risk to Portfolio Intelligence.
Repository areas: docs/implementation/; confirmed admissions only in docs/GLOSSARY.md.
Order: First, after M43 Architecture confirmation.
Dependencies: M34, M39–M42, Glossary V1–V3, existing source inventory.
Validation: ownership gate, overlap search, negative-corpus review, legacy formula inventory, no downstream reliance before confirmation.
Completion: every cross-WP noun required to begin WP2–WP9 has a confirmed disposition and single owner. WP1 need not pre-decide vocabulary local to an undrafted downstream contract.

Downstream vocabulary rule: any WP2–WP9 work package that introduces a new noun must run its own independently reviewed and confirmed vocabulary gate before relying on that noun. The owning WP must record ADMIT, REUSE, RENAME, or REJECT and synchronize every confirmed Glossary admission or rename in the same change. No later vocabulary decision may reopen WP1 or another frozen work package.
M43-WP2 — Definition, Method Version, and Applicability Contracts
Purpose: Specify what a Portfolio measure means and how an exact calculation method is identified.
Scope:
Portfolio Measure Definition identity and revision;
immutable Portfolio Method Version identity;
applicability requirements of a Portfolio Measure Definition;
dependency declaration;
future registry invariants;
future non-production method-specification gate.
Deliverables:
normative contract specification;
canonical identity rules;
prohibited interpretation rules;
compatibility rules for method revisions;
positive and negative documentary vectors.
Repository areas: docs/implementation/; docs/implementation/m43/fixtures/.
Order: After WP1 confirmation.
Dependencies: WP1 vocabulary dispositions; M41 mechanical patterns by citation, not ownership reuse.
Validation: field-level ownership gate, identity collision vectors, version non-substitutability, dependency closure.
Completion: two independent readers identify the same Portfolio Measure Definition, Portfolio Method Version, applicability result, and dependency set; any WP2-local noun has passed the downstream vocabulary rule.
M43-WP3 — Portfolio Subject and Analytics Input Manifest Contract
Purpose: Bind every calculation to one exact Portfolio Composition and a complete, closed evidence set.
Scope:
subject identity;
exact M42 Composition citation;
ledger-derived evidence entries;
M39/M41 market-evidence entries;
Asset Foundation references;
explicit invocation parameters;
dependency-result references;
Portfolio Analytics Input Manifest entry ordering, equivalence, conflict, and identity.
Deliverables:
subject contract;
manifest and entry schema specification;
canonical ordering and serialization rules;
sufficiency-precondition inputs;
conflict and duplicate rules.
Repository areas: docs/implementation/; M43 fixtures.
Order: After WP2.
Dependencies: WP1–WP2; M42-WP7; M39–M41; ADR-001/003/004.
Validation: wrong-scope, cross-portfolio, missing-coordinate, duplicate-entry, conflicting-evidence, provider-symbol, and ambient-selection vectors.
Completion: every calculation input is exact, closed, attributable, and reconstructable without consulting live state; any WP3-local noun has passed the downstream vocabulary rule.
M43-WP4 — Temporal, Currency, Calendar, Benchmark, and Arithmetic Semantics
Purpose: Eliminate every ambient numerical convention before formulas are admitted.
Scope:
Portfolio Measurement Window boundaries;
economic versus record-time handling;
portfolio base-currency expression;
FX evidence and conversion placement;
calendar and observation alignment;
authority class, identity, versioning, and binding rules for the risk-free input;
authority class, identity, versioning, and binding rules for the annualization basis;
benchmark alignment;
missing-data rules;
decimal precision and rounding;
partial-window handling;
dependency arithmetic.
Deliverables:
normative semantics specification;
explicit no-default matrix;
authority-class matrix proving whether each risk-free input and annualization basis is governed evidence or a versioned calculation dependency and proving neither is a free caller override;
canonical serialization rules;
golden vectors for every semantic choice.
Repository areas: docs/implementation/; M43 numerical fixtures.
Order: After WP3.
Dependencies: WP2–WP3; M42 Base Currency and Benchmark Declaration; M39/M41 temporal and market contracts; ADR-003.
Validation: timezone, market-closure, sparse-history, FX-gap, benchmark-gap, caller-supplied risk-free and annualization override rejection, zero denominator, negative-value, leap-year, and rounding-boundary vectors.
Completion: no method can choose a calendar, currency, benchmark, annualization factor, risk-free input, or fallback implicitly; the risk-free input and annualization basis each have one confirmed authority class and binding rule; any WP4-local noun has passed the downstream vocabulary rule.
M43-WP5 — Result, Sufficiency, Degraded State, Provenance, and Serialization
Purpose: Define an immutable and auditable output envelope shared by every method family.
Scope:
result identity;
value presence and absence;
Portfolio Input Sufficiency;
Portfolio Computation Outcome, if admitted, or an explicit REUSE citation of the owning domain’s Computation Outcome;
Portfolio Deterministic Calculation, if admitted, or an explicit REUSE citation of the owning domain’s Deterministic Calculation;
Degraded State under the existing M34-D-0005 producing-domain grammar, or the confirmed WP1 disposition if a Portfolio-prefixed noun is required;
reason codes;
method and manifest lineage;
Provenance carriage;
compatibility with Canonical Temporal Claim, including Event Type, Producing Domain, authoritative timestamp, and Degraded State;
canonical bytes and hash stability.
Deliverables:
result contract;
outcome/sufficiency/degradation matrix;
reason-code grammar;
Canonical Temporal Claim compatibility mapping;
canonical serialization;
round-trip and hash-stability vectors.
Repository areas: docs/implementation/; M43 result fixtures.
Order: After WP4.
Dependencies: WP1–WP4; M34-D-0005 Canonical Temporal Claim and Degraded State; M40-WP1 §8.3, including UNAVAILABLE as Degraded State and never Computation Outcome; generic Provenance meaning; M41 result-pattern precedent.
Validation: no-value-on-failure, UNAVAILABLE-versus-outcome separation, complete Canonical Temporal Claim, explicit partial-result rules, deterministic identity, round-trip reconstruction, provenance non-recapture.
Completion: identical inputs and Portfolio Method Version yield byte-identical Portfolio Measure Results; every unavailable or degraded result explains why; temporal authority is complete; any WP5-local noun has passed the downstream vocabulary rule.
M43-WP6 — Core Performance and Rolling Method Specifications
Purpose: Canonicalize the first Portfolio Analytics method family.
Scope:
chaining the Ledger-owned canonical period return;
cumulative time-weighted return;
annualized return;
rolling return;
normalized performance series;
valid-history and partial-window requirements.
WP6 must bind to the canonical period-return rule and its owner exactly as confirmed by WP1. If WP1 confirms Ledger & Accounting ownership, WP6 reuses that rule semantically under PORTFOLIO_CALCULATION_RULES.md §10 and must not define a second period-return formula. If ownership remains unresolved or receives a different disposition, WP6 is blocked pending correction. Source-level call-site selection is deferred to WP9.
Deliverables:
non-production Portfolio Measure Definition and Portfolio Method Version specifications;
dependency map to canonical period returns;
formula and applicability matrices;
golden vectors;
legacy behavior disposition.
Repository areas: docs/implementation/; M43 performance fixtures.
Order: After WP5.
Dependencies: WP2–WP5; PORTFOLIO_CALCULATION_RULES.md; ADR-001–ADR-004.
Validation: cash-flow neutrality, missing-period handling, compounding identities, short-history behavior, negative-return boundaries, parity against corrected accounting baselines.
Completion: every core performance output has one exact non-production method specification, version, input contract, result contract, and validation corpus; no production method is admitted; any WP6-local noun has passed the downstream vocabulary rule.
M43-WP7 — Risk and Benchmark-Relative Method Specifications
Purpose: Canonicalize advanced risk and declared-benchmark comparison.
Scope:
drawdown;
volatility;
downside deviation;
Sharpe and Sortino;
beta and correlation;
alpha;
tracking error;
information ratio.
Benchmark-relative methods must consume the M42 Portfolio Benchmark Declaration. Request-supplied benchmark symbols may not substitute for it. Explicitly None makes relative methods not applicable, not silently defaulted.
No Sharpe, Sortino, alpha, information-ratio, or other ratio method specification may pass its gate until WP4 has confirmed the authority class and binding rules of every required risk-free input and annualization basis.
Deliverables:
non-production method specifications and versions;
explicit risk-free, calendar, and annualization dependencies;
benchmark-form applicability matrix;
sufficiency and degraded-state rules;
numerical vectors.
Repository areas: docs/implementation/; M43 risk and benchmark fixtures.
Order: After WP6. Review can be prepared in parallel with WP8 once WP6 is frozen.
Dependencies: WP2–WP6; confirmed WP4 risk-free-input and annualization-basis authority dispositions; M42-WP5; M39–M41 market evidence.
Validation: zero variance, insufficient sample, missing benchmark, Explicitly None, unimplemented Composite/Category evidence, asynchronous calendars, zero tracking error, and negative-return vectors.
Completion: no metric depends on a hidden 2.5%, 252, provider symbol, benchmark fallback, caller-overridden governed dependency, or undocumented statistical convention; no production method is admitted; any WP7-local noun has passed the downstream vocabulary rule.
M43-WP8 — Position and Sector Attribution Method Specifications
Purpose: Define deterministic contribution and attribution without crossing into evaluation or causal judgment.
Scope:
position contribution;
sector contribution;
sector attribution timeline;
explicit attribution-grouping disposition: REUSE the frozen Portfolio Intelligence-owned Analytical Grouping for attribution, or bind only to exact Asset Classification with a documented constitutional justification;
strict distinction between Analytical Grouping and Asset Classification even where labels coincide;
classification/grouping version binding;
reconciliation residual;
BHB decomposition and benchmark-relative attribution are excluded from M43.
Deliverables:
non-production attribution method specifications;
exact decomposition identities;
taxonomy and point-in-time classification requirements;
residual treatment;
explicit distinction from recommendation, regime, and human-vs-AI attribution.
Repository areas: docs/implementation/; M43 attribution fixtures.
Order: After WP6; independent of WP7.
Dependencies: WP2–WP6; M34-D-0004; Asset Foundation classifications; Portfolio Intelligence Analytical Grouping where the confirmed disposition requires it; Ledger holdings evidence.
Validation: contribution-sum reconciliation, missing classifications, classification changes, corporate-action continuity, cash treatment, incomplete sector benchmark data, and explicit residual vectors.
Completion: every reported contribution reconciles deterministically to its parent return or returns a named non-success outcome; every sector-related value identifies Asset Classification or Analytical Grouping and its exact authority; no causal or evaluator claim or production-method admission is produced; any WP8-local noun has passed the downstream vocabulary rule.
M43-WP9 — Runtime Realization, Compatibility, and Cutover Design
Purpose: Convert the frozen M43 contracts into an implementation-ready plan without writing code.
Scope:
future package/module ownership;
registry and pure-kernel design;
M42 Composition adapter boundary;
manifest assembly;
legacy analytics adapters;
shadow comparison;
API versioning;
persistence options;
observability;
rollout, rollback, and deprecation.
Deliverables:
detailed technical design;
legacy-to-canonical call-site map;
future repository diff map;
compatibility matrix;
testing plan;
migration and rollout runbook;
go/no-go gates.
Repository areas described but not modified:
backend/services/portfolio_metrics.py;
backend/services/analytics/quant_engine.py;
backend/services/analytics/attribution_engine.py;
future Portfolio Analytics contracts, registry, manifest, result, and kernel modules;
backend/main.py or a future dedicated analytics router;
backend/models/database.py and migrations only if later persistence is authorized;
backend analytics tests;
frontend/lib/api.ts;
analytics pages and components.
Order: Terminal WP, after WP6–WP8.
Dependencies: All earlier M43 work packages.
Validation: every future module maps to one owner; every legacy behavior receives PRESERVE, ADAPT, DEPRECATE, or REJECT; no big-bang cutover exists.
Completion: a later milestone can implement the system without making a new semantic, ownership, formula, migration, or compatibility decision; any WP9-local noun has passed the downstream vocabulary rule.
10. Implementation strategy
The successor implementation should proceed additively:
Implement immutable contracts and canonical serializers.
Implement the M42 Portfolio Composition value object and validator without persistence or inference.
Implement the input-manifest builder.
Implement the frozen definition/method registry.
Implement the pure computation kernel.
Implement WP6 methods.
Implement WP7 methods.
Implement WP8 methods.
Add legacy read adapters and shadow computation.
Compare legacy and canonical results, classifying every difference.
Add a versioned, read-only canonical API.
Migrate Experience consumers only after API and parity review.
Deprecate legacy calculations only after all consumers are proven migrated.
Remove duplicate implementations and private caches only in a separately reviewed cleanup step.
The pure kernel must have no ORM, database, network, clock, provider, logging, cache, or workspace-selection dependency.
11. Review sequence
M43 Architecture Independent Review.
Required Corrections Response, if needed.
Independent Architecture Confirmation; freeze Architecture.
WP1 vocabulary/ownership review and confirmation.
WP2 vocabulary gate if needed, then contract review and confirmation.
WP3 vocabulary gate if needed, then subject/manifest review and confirmation.
WP4 vocabulary gate if needed, then architectural and independent numerical review and confirmation.
WP5 vocabulary gate if needed, then identity/serialization/provenance review and confirmation.
WP6 vocabulary gate if needed, then performance-method review and confirmation.
WP7 vocabulary gate if needed, then independent statistical and constitutional review and confirmation.
WP8 vocabulary gate if needed, then independent attribution and ownership review and confirmation.
WP9 vocabulary gate if needed, then implementation-design, compatibility, and operability review and confirmation.
Epic Closeout review.
Independent confirmation of any closeout corrections.
No downstream WP may rely on a candidate noun or unresolved semantic choice.
12. Testing and validation sequence
M43 validation remains non-executable, documentary, and fixture-based. M43 may commit data fixtures and expected outcomes, but no executable validation artifact, test runner, harness, or production method:
Corpus and authority-reference validation.
Vocabulary collision and ownership validation.
Field-level five-part boundary gates.
Positive and negative contract vectors.
Independent formula recomputation.
Canonical serialization round trips.
Hash-stability checks.
Cross-method mathematical identities.
Attribution reconciliation identities.
Legacy characterization matrix.
Backward-compatibility matrix.
Whole-corpus negative-corpus scan.
WP9 must require the later executable milestone to provide:
pure unit tests;
property-based arithmetic tests;
fixture conformance tests;
mutation tests for numerical rules;
deterministic replay tests;
serialization/hash tests;
legacy shadow-parity tests;
database adapter integration tests;
API contract tests;
workspace-isolation tests;
degraded-mode and observability tests;
frontend tests proving presentation performs no calculation.
13. Repository impact
M43 itself should add:
docs/implementation/M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md;
one primary artifact per WP;
independent review, correction, and confirmation artifacts;
docs/implementation/m43/fixtures/;
M43_EPIC_CLOSEOUT.md.
Conditional changes:
docs/GLOSSARY.md only for independently confirmed admissions or renames;
docs/engineering/DECISION_LOG.md at epic closeout;
docs/implementation/INDEX.md at epic closeout;
docs/engineering/PROJECT_STATUS.md only if repository convention elects to name the next epic.
ROADMAP.md receives no M43 capability-completion mark because M43 deploys none of the four roadmap capabilities.
M43 modifies no backend, frontend, database migration, deployment, or operational file.
14. Backward compatibility
Because M43 is specification-only, existing runtime behavior remains unchanged.
Important compatibility rules for the successor:
legacy endpoints remain available during shadow adoption;
current outputs are not retroactively declared canonical;
canonical APIs are additive and versioned;
no field is silently reinterpreted;
request-selected benchmark comparison remains a legacy exploratory feature, distinct from declared-benchmark analytics;
missing M42 coordinates produce explicit unavailability, not inferred values;
existing snapshots remain Ledger-derived evidence, not immutable canonical analytics results;
historical results are never overwritten;
method corrections create new method versions and new results;
consumer migration precedes legacy removal.
15. Migration requirements
M43 requires no data migration.
The future implementation design must require:
additive schemas, if result persistence is authorized;
immutable definition, method-version, manifest, and result identities;
no automatic inference of Portfolio Base Currency, Benchmark Declaration, Investment Universe, Lifecycle State, or Provenance;
explicit human-confirmed or source-authorized creation of missing M42 coordinates;
historical recomputation as newly created, versioned result records;
no overwrite of old snapshots or analytics records;
dual-read/shadow operation before cutover;
resumable and portfolio-scoped backfill;
input-manifest hashes and method versions on every backfilled result;
rollback by disabling canonical reads, never deleting history.
The three unresolved accounting questions in PORTFOLIO_CALCULATION_RULES.md remain outside M43. Where they affect analytics, M43 must specify insufficiency or degradation rather than settle accounting policy indirectly.
16. Risks and tradeoffs
Risk	Required response
Reusing M41 contracts by relabeling Market Measure types	Reuse patterns only; govern separate Portfolio Intelligence vocabulary
M43 grows into runtime implementation	Keep source/runtime authority explicitly NONE
Existing code becomes accidental precedent	WP1 produces a disposition matrix; G6 remains controlling
Missing M42 runtime coordinates	Return unavailable; never infer or default
Legacy benchmark defaults conflict with M42 declarations	Preserve only as legacy exploratory behavior; exclude from canonical methods
Formula duplication violates Law 9	WP1 proves the canonical period-return owner; WP6 reuses the confirmed canonical rule semantically; WP9 assigns one future implementation per method
Statistical defaults remain ambient	WP4 assigns every calendar, annualization basis, threshold, and risk-free input a confirmed authority class and binding rule
Sparse or misaligned data produces plausible nonsense	WP5 requires named insufficiency and degraded states
Sector history uses current classifications	Bind exact taxonomy/version/as-of evidence or return non-success
Attribution crosses into evaluation	Limit M43 to deterministic contribution and reconciliation
Specification-to-code drift	Freeze fixtures and require future conformance testing
Review load encourages merged WPs	Keep WP6–WP8 separately reviewable; split further rather than compress

The principal tradeoff is deliberate: M43 delays visible runtime capability in exchange for freezing the semantic and numerical contract before another analytics implementation becomes entrenched.
17. Closeout sequence
Confirm WP1–WP9 complete with no unresolved findings.
Verify every admitted noun is synchronized in the Glossary.
Verify every downstream-WP vocabulary gate was independently confirmed and synchronized in the same change as admission or rename.
Verify all method specifications have canonical vectors.
Verify the negative corpus across the complete M43 corpus.
Verify no M1–M42 artifact was modified or reinterpreted.
Verify backend, frontend, schema, API, and operational authority remained unused.
Draft M43_EPIC_CLOSEOUT.md.
Perform independent closeout review.
Resolve and independently confirm any required correction.
Add the consolidated Decision Log entry.
Update the Implementation Index.
Do not mark any ROADMAP capability complete; update status navigation only as authorized.
Refresh Graphify only if a graph corpus and command are available; do not create one solely for closeout.
Validate repository-relative links and orphan references.
Confirm a clean repository state.
Record the separately governed next-milestone readiness for executable Portfolio Analytics implementation.
18. Final milestone completion criteria
M43 is complete only when:
Architecture and every WP are independently approved;
all required corrections are independently confirmed;
every required noun has a final disposition and single owner;
every WP-local noun was confirmed before contractual reliance and synchronized in the same change where required;
no ambient semantic or numerical default remains;
core performance, risk, benchmark-relative, and attribution methods have exact versioned specifications;
every result is deterministic, serializable, attributable, and loudly degraded;
the successor implementation requires no new semantic decision;
no frozen M1–M42 decision has changed;
no runtime or operational change has occurred;
no production method or executable validation artifact has been admitted;
repository governance records are synchronized;
unresolved findings are NONE.

19. Change Summary

This corrected version applies the governing Independent Constitutional Architecture Review without changing M43’s architectural intent, roadmap position, scope, milestone boundary, or nine-work-package decomposition. RC-1 through RC-8 are each valid and are accepted in full.

Localized corrections:

- completed the no-authority declaration and explicitly denied production-method and executable-validation admission;
- converted all repository links to repository-relative form;
- narrowed WP1 to cross-WP vocabulary and added independently confirmed vocabulary gates for WP-local nouns;
- classified every ownership row as frozen-with-citation or candidate-owner-to-prove;
- restored the frozen Analytical Grouping versus Asset Classification boundary in WP8;
- added Portfolio-scoped outcome and determinism candidates and made Degraded State reuse/disposition explicit;
- bound WP5 to M40-WP1 §8.3 and the M34-D-0005 Canonical Temporal Claim;
- made all M43 method specifications explicitly non-production;
- required WP4 to fix risk-free-input and annualization-basis authority before WP7 ratio specifications;
- excluded BHB and benchmark-relative attribution, fixing WP8 as independent of WP7;
- prohibited a false ROADMAP capability-completion mark; and
- restated WP6 at the canonical-rule level, conditional on WP1 ownership proof, with source call sites deferred to WP9.

No capability, runtime behavior, repository subsystem, migration, or frozen M1–M42 decision is added or changed.

20. RC Response Matrix

| RC | Status | Summary of change | Affected sections |
|---|---|---|---|
| RC-1 | ACCEPTED | WP1 now closes only cross-WP vocabulary. Any WP2–WP9 noun introduced later must pass an independently reviewed and confirmed vocabulary gate, with same-change Glossary synchronization for confirmed admissions or renames. | §9 WP1–WP9; §11; §17; §18 |
| RC-2 | ACCEPTED | Every ownership row is frozen-with-citation or candidate-owner-to-prove. Canonical period-return ownership is a WP1 proof gate, and WP6 is conditional on its confirmed disposition. | §8; §9 WP1; §9 WP6; §16 |
| RC-3 | ACCEPTED | Analytical Grouping is restored as Portfolio Intelligence-owned under M34-D-0004. WP8 must distinguish and explicitly disposition Analytical Grouping against Asset Classification for every sector-related value. | §8; §9 WP8 |
| RC-4 | ACCEPTED | Portfolio Computation Outcome, Portfolio Deterministic Calculation, and Portfolio Degraded State were added as candidates without pre-admission. WP2–WP5 use Portfolio-prefixed terms or explicit reuse, and WP5 cites the frozen UNAVAILABLE rule in M40-WP1 §8.3. | §9 WP1–WP5; §18 |
| RC-5 | ACCEPTED | Production-method and Executable-validation authority are NONE; M43 admits no production method, and every method specification and fixture remains non-production until separately authorized. | Authority block; §2; §5; §9 WP2/WP6/WP7/WP8; §12; §18 |
| RC-6 | ACCEPTED | WP4 must confirm one authority class and binding rule for the risk-free input and annualization basis. Caller override is prohibited, and WP7 ratio specifications are gated on those confirmed dispositions. | §7; §9 WP4; §9 WP7 |
| RC-7 | ACCEPTED | BHB and benchmark-relative attribution are excluded, making WP8 independent of WP7. M43 may not mark any ROADMAP capability complete. | §5; §9 WP8; §13; §17 |
| RC-8 | ACCEPTED | Absolute links are repository-relative; missing authority declarations and executable-validation exclusions are present; WP5 is bound to Canonical Temporal Claim; WP6 reuses the canonical rule semantically and defers call-site design to WP9. | Authority block; §1; §2; §5; §6; §9 WP5; §9 WP6; §12 |
