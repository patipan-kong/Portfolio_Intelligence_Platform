# M46 — Corporate Action Adjudication and Portfolio Accounting Correctness Planning Allocation / Commissioning Record

**Artifact class:** Additive planning allocation / commissioning record
**Lifecycle stage:** Allocation / commissioning
**Assigned initiative identifier:** `M46`
**Disposition:** `ALLOCATED`
**Implementation authority:** `NONE`

---

## 1. Act and decision boundary

Acting solely as the competent allocation / commissioning authority, this
record decides whether to allocate a new additive cross-domain planning
initiative for **Corporate Action Adjudication and Portfolio Accounting
Correctness**.

This record performs allocation only. It does not author, review, correct,
confirm, ratify, or freeze an architecture or implementation-plan candidate.
It does not authorize a work package, implementation, schema change, migration,
runtime change, production correction, cutover, or release.

The allocation decision is:

**`ALLOCATED`**

## 2. Identifier determination

The identifier is resolved, not presumed.

1. [M45's current status](../implementation/M45_MILESTONE_STATUS_RECORD.md#L1-L5)
   establishes `M45` as an assigned milestone identifier.
2. The repository contains no milestone or work-package artifact using `M46`
   or a higher integer identifier at this allocation boundary.
3. The repository's latest milestone-allocation precedent identifies
   allocation / commissioning as the act that assigns a milestone label and
   planning mandate
   ([M45 Architecture and Implementation Plan, lines 204–219](../implementation/M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md#L204-L219)).
4. No existing record assigns the next identifier to another initiative.

The next unoccupied sequential identifier is therefore assigned by this act:

**`M46`**

This assignment creates no dependency on M45 and changes no M45 status.

## 3. Why the initiative is required

The governing architecture already requires:

- immutable recorded history, derived holdings, deterministic replay,
  permanent asset identity, decisive identity resolution, loud failure, and
  correctness over convenience
  ([Platform Architecture, lines 69–111](../architecture/platform_architecture.md#L69-L111));
- Asset Foundation adjudication of symbols, listings, renames, and corporate
  restructurings into identity facts
  ([Platform Architecture, lines 175–185](../architecture/platform_architecture.md#L175-L185));
- append-only accounting events and deterministic derivation of holdings, cash,
  cost basis, and valuation-in-time
  ([Platform Architecture, lines 203–213](../architecture/platform_architecture.md#L203-L213));
- corporate-action evidence to enter through provenance-bearing proposals
  ([Platform Architecture, lines 217–227](../architecture/platform_architecture.md#L217-L227)); and
- derived valuation, performance, attribution, risk, and exposure to remain
  Portfolio Intelligence responsibilities
  ([Platform Architecture, lines 231–241](../architecture/platform_architecture.md#L231-L241)).

The Phase 3 roadmap expressly schedules Corporate Actions
([Roadmap, lines 136–160](../architecture/ROADMAP.md#L136-L160)). The Asset
Registry implementation plan records that the stable identity prerequisite is
available and that Corporate Action processing belongs to a separate epic
([Asset Registry Implementation Plan, lines 499–507](../implementation/ASSET_REGISTRY_IMPLEMENTATION_PLAN.md#L499-L507)).

The existing Corporate Action architecture requires evidence to be adjudicated
before replay, identity and ledger consequences to land consistently, and
history to be corrected additively rather than rewritten
([Corporate Action Domain, lines 15–21](../architecture/CORPORATE_ACTION_DOMAIN.md#L15-L21),
[lines 112–144](../architecture/CORPORATE_ACTION_DOMAIN.md#L112-L144), and
[lines 179–187](../architecture/CORPORATE_ACTION_DOMAIN.md#L179-L187)).

A production-facing incident involving BANPU is admitted only as an acceptance
incident demonstrating the need for this planning initiative. It supplies no
corporate-action terms, identity verdict, ratio, accounting instruction, or
production-correction authority. The initiative is generic and multi-asset.

## 4. Governing and frozen predecessor corpus

### 4.1 Governing architecture

The M46 planning candidates must conform to, and may not amend through silence:

1. [Portfolio Intelligence Platform Architecture](../architecture/platform_architecture.md),
   especially Laws 1–15 and the domain boundaries at lines 175–241.
2. [Portfolio Intelligence Roadmap](../architecture/ROADMAP.md), especially the
   Phase 3 Corporate Actions entry at lines 136–160.
3. [Corporate Action Domain](../architecture/CORPORATE_ACTION_DOMAIN.md), as the
   existing technical architecture for claims, adjudication, dual-authority
   consequences, replay, uncertainty, and correction.
4. [Asset Registry Implementation Plan](../implementation/ASSET_REGISTRY_IMPLEMENTATION_PLAN.md),
   as implementation history and prerequisite evidence, not authority to
   redesign frozen identity work.

### 4.2 Frozen and terminal predecessor state

The M46 planning candidates must cite and preserve:

1. The frozen M45 planning corpus identified by the
   [M45 Architecture Freeze Record, lines 56–95](../implementation/M45_ARCHITECTURE_FREEZE_RECORD.md#L56-L95).
2. M45's current `ACTIVE — WAITING FOR EXTERNAL SUPPLY` state and its prohibition
   on manufacturing external owner-domain supply
   ([M45 Milestone Status Record, lines 20–49](../implementation/M45_MILESTONE_STATUS_RECORD.md#L20-L49)).
3. The frozen Asset Foundation planning corpus and its `NONE` implementation,
   runtime, allocation, authorization, and downstream-execution authority
   ([Asset Foundation Planning Freeze Record, lines 32–42](ASSET_FOUNDATION_PLANNING_FREEZE_RECORD.md#L32-L42)).
4. The frozen Ledger & Accounting planning corpus, modifiable only through a
   governed successor lifecycle, with no work package allocated by its freeze
   ([Ledger & Accounting Planning Freeze, lines 58–68](../implementation/LEDGER_ACCOUNTING_PLANNING_FREEZE.md#L58-L68)).
5. The Ledger & Accounting final state: LA-WP2 is terminally governance-blocked,
   LA-WP3–LA-WP7 are unauthorized, executable authority is absent, and future
   work may transition without reopening that lifecycle
   ([Ledger & Accounting Owner-Domain Final State, lines 8–25](LEDGER_ACCOUNTING_OWNER_DOMAIN_FINAL_STATE.md#L8-L25)).

The Decision Log is context rather than independent constitutional authority
([AI Rules, lines 72–76](../handbook/AI_RULES.md#L72-L76)). The Implementation
Index is non-normative navigation and creates no authority
([Implementation Index, lines 1–13](../implementation/INDEX.md#L1-L13)). Neither
is modified by this allocation.

## 5. Allocation prerequisites

| Prerequisite | Evidence | Result |
| --- | --- | --- |
| Competent allocation role is explicit | The commissioning instruction for this act assigns only the competent allocation / commissioning role; this record exercises no later lifecycle role | `SATISFIED` |
| Initiative is additive | A new record and prospective candidate corpus can be created without editing any frozen artifact | `SATISFIED` |
| Existing architecture admits the subject | Phase 3 schedules Corporate Actions; existing domain boundaries already own identity, evidence, accounting, market worth, and derived intelligence | `SATISFIED` |
| No constitutional-domain change is required | M46 coordinates existing domains and transfers no ownership | `SATISFIED` |
| Stable identity prerequisite exists | Asset Registry planning records Corporate Actions as a separately ready successor epic | `SATISFIED` |
| Existing milestone cannot supply the authority | M45 remains bounded and Ledger & Accounting's earlier lifecycle has no executable or successor authority | `SATISFIED` |
| Identifier is available | `M45` is assigned; no `M46` or higher milestone artifact exists at this boundary | `SATISFIED` |
| Planning can remain separate from implementation | Allocation and authorization are distinct acts under [AI Rules, lines 224–250](../handbook/AI_RULES.md#L224-L250) | `SATISFIED` |

No prerequisite requires a constitutional amendment, reopening a frozen
artifact, or granting implementation authority.

## 6. Cross-domain planning boundary

M46 is a coordinating planning initiative, not a constitutional domain. It
plans the complete path:

`evidence → adjudication → asset identity consequences → accounting effects → deterministic replay → quote-basis resolution → valuation → downstream regeneration`

Ownership remains unchanged:

| Domain | Planning boundary retained by M46 |
| --- | --- |
| Asset Foundation | Permanent asset identity; effective-dated identifiers; continuity, successor, predecessor, listing, and lifecycle identity consequences; adjudication of structural identity facts |
| Connectivity & Ingestion | Announcement and broker evidence intake; provenance; deduplication; conflict handling; proposal and reconciliation boundaries |
| Ledger & Accounting | Immutable portfolio-scoped accounting effects; entitlement and settlement consequences; quantity, cash, and total-cost-basis state; deterministic replay; append-only correction semantics |
| Market Intelligence | Identity-, listing-, unit-, currency-, time-, provider-, and adjustment-basis-aware observations and quote resolution |
| Portfolio Intelligence | Derived holdings valuation, performance, attribution, exposure, risk, optimization inputs, signals, and AI-evaluation regeneration from admitted truth and worth |

No M46 coordinator or artifact may overrule an owner domain or record identity
facts, ledger truth, market observations, or derived measures on that domain's
behalf.

## 7. Authority allocated

This record allocates planning responsibility only for:

1. architecture candidate authoring;
2. documentary implementation-plan candidate authoring;
3. work-package decomposition and dependency sequencing;
4. generic multi-asset acceptance-vector definition, including BANPU solely as
   a real incident vector without encoded market-, issuer-, or ratio-specific
   logic;
5. preparation of an independently reviewable candidate corpus and review
   handoff; and
6. read-only repository discovery required to ground those candidates.

The intended planning candidate pair is:

- `docs/implementation/M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md`
- `docs/implementation/M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md`

Those paths are prospective outputs, not artifacts created or approved by this
record.

## 8. Competent lifecycle roles

This allocation constitutes the following role types for the M46 planning
lifecycle. A future actor must be explicitly assigned to the applicable role
and may act only after that stage's prerequisites exist.

| Lifecycle act | Competent role | Independence and authority boundary |
| --- | --- | --- |
| Candidate authoring | **M46 Architecture and Planning Candidate Author** | May create the candidate pair within Section 7; may not review, confirm, ratify, freeze, or implement it |
| Independent review | **M46 Independent Architecture Reviewer** | Must be independent of candidate and correction authorship; may issue findings and disposition only |
| Correction | **M46 Planning Candidate Correction Author** | Normally the candidate author or an explicitly appointed successor author; may answer review findings additively but may not declare them resolved |
| Independent confirmation | **M46 Independent Planning Confirmer** | Must be distinct from candidate authorship, correction authorship, and independent review; may confirm or refuse confirmation only |
| Ratification | **M46 Planning Ratifying Authority** | Must be distinct from authorship, correction, review, and confirmation; may adopt or refuse the confirmed candidate corpus only |
| Freeze | **M46 Planning Freeze Authority** | Must act independently after ratification; may content-identify and freeze or refuse freeze only |

Naming these role types does not perform their later acts and does not appoint
the current allocation authority to any of them. Review, correction,
confirmation, ratification, and freeze remain future, separate lifecycle acts.

## 9. Authority explicitly withheld

Authority is `NONE` for all of the following:

- production code or test implementation;
- database schema or persistence changes;
- data migrations or backfills;
- runtime or API changes;
- quote-provider, provider-routing, or market-data changes;
- ledger correction or transaction admission;
- BANPU correction or any issuer-specific correction;
- portfolio or holding mutation;
- portfolio rebuilding or replay execution against production data;
- snapshot, analysis, signal, optimization, attribution, or AI-evaluation
  regeneration;
- shadow migration, cutover, rollback execution, or production release;
- amendment or reopening of frozen artifacts;
- creation of a constitutional domain;
- allocation or authorization of any M46 work package; and
- M45, Ledger & Accounting, Asset Foundation, or other owner-domain authority.

No later work package is allocated or authorized by this record. Ratification
or freeze of future planning candidates will not imply implementation or
work-package authority. Each substantive work package must receive its own
explicit allocation and authorization after the planning corpus is ratified
and frozen.

## 10. Planning invariants and non-goals

The M46 planning candidates must preserve these boundaries:

1. BANPU is an acceptance incident, never a special type, conditional, hard
   ratio, or source of inferred terms.
2. Historical transactions and announcements are not rewritten. Corrections
   are append-only.
3. Corporate actions are facts learned from evidence, not calculations inferred
   from quantity, price, valuation, or profit-and-loss symptoms.
4. Symbol substitution is not identity adjudication.
5. Identity consequences and accounting consequences must be planned as one
   consistent admission decision, both or neither.
6. Replay consumes admitted consequences and does not interpret announcements
   or consult mutable provider authority.
7. Ambiguous identity, action terms, entitlement, cost-basis allocation, quote
   basis, unit basis, or effective date must produce a fail-closed or quarantine
   state.
8. Incident containment, planning, authorization, implementation, migration,
   production correction, cutover, and release remain separate acts.

## 11. Allocation disposition

All prerequisites for the bounded planning initiative are satisfied.

**Disposition: `ALLOCATED`**

**Assigned initiative: `M46 — Corporate Action Adjudication and Portfolio Accounting Correctness`**

**Authority granted: planning candidate production within Section 7 only.**

**Implementation, work-package, runtime, migration, production-correction,
cutover, and release authority: `NONE`.**

## 12. Exact next constitutional act

A fresh session explicitly assigned as the **M46 Architecture and Planning
Candidate Author** may create the two planning candidates named in Section 7.

That authoring act must:

1. cite this allocation record as its sole M46 planning mandate;
2. ground the candidate pair in the corpus identified in Section 4;
3. resolve domain model, identity, event, accounting-effect, cost-basis,
   temporal, quote-basis, replay, migration, quarantine, downstream, and
   acceptance-vector questions at planning level;
4. define independently allocatable and authorizable work packages;
5. mark both artifacts `REVIEW CANDIDATE` and authority `NONE` beyond this
   planning allocation; and
6. stop before independent review, confirmation, ratification, freeze,
   implementation, migration, or production action.

## 13. Validation

| Validation | Result |
| --- | --- |
| Assigned-identifier collision scan | `PASS` — no pre-existing `M46` or higher milestone artifact |
| Required source and frozen-predecessor links | `PASS` — 24 repository-local targets checked, 0 broken |
| Scope-to-authority audit | `PASS` — all required planning permissions, lifecycle roles, and explicit withholding clauses present |
| Markdown structure and local-link validation | `PASS` |
| `git diff --check` | `PASS` — no tracked-tree whitespace errors; untracked-record no-index check reported no whitespace error |
| `git diff --cached --check` | `PASS` |
| Production-code and frozen-artifact change audit | `PASS` — only this additive governance record is present in Git status |
