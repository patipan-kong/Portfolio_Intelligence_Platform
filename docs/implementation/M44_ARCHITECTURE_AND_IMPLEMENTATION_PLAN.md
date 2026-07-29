# M44 Architecture and Implementation Plan

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics Foundation

**Artifact class:** Constitutional architecture and implementation plan

**Proposed status:** `RC2 — CORRECTED AFTER INDEPENDENT CONSTITUTIONAL REVIEW AND ADJUDICATION; REQUIRES INDEPENDENT CONSTITUTIONAL CONFIRMATION`

**Revision:** RC2. Supersedes RC1 under the adjudicated dispositions recorded in
§1.7 and Appendix A. RC1 is superseded in full; no RC1 text remains effective
where Appendix B records a change.

**Predecessor milestone:** M43 — Portfolio Intelligence Method Specifications (`COMPLETE AND FROZEN`)

**Governing authority:** [Platform Architecture](../architecture/platform_architecture.md) Laws 1–15, §§6–8, §§11–12

**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/schema/migration authority:** `NONE`
**API/transport authority:** `NONE`
**UI/presentation authority:** `NONE`
**Implementation authority:** `NONE`
**Provider authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`
**Capability-completion authority:** `NONE`
**Frozen-artifact-amendment authority:** `NONE`

This plan does not itself amend or activate repository authority. It becomes
canonical only after the normal independent architecture review, correction,
and confirmation sequence recorded in §12, and only when that confirmation is
represented by a repository-local artifact.

---

## 1. Status and authority

### 1.1 Document status

`RC2 — REQUIRES INDEPENDENT CONSTITUTIONAL CONFIRMATION`. This candidate has
received an Independent Constitutional Architecture Review, a Formal
Constitutional Response, and a Constitutional Adjudication (§1.7). It applies
every mandatory adjudicated correction. No work package described here is
authorized to begin until an Independent Architecture Confirmation of RC2 is
recorded as a repository-local artifact at
`docs/implementation/M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md`.

The repository-local confirmation artifact is mandatory rather than optional.
Its absence for M43 is itself one of the defects M44 must close (§3.1, G-1);
M44 must not reproduce it.

### 1.2 Governing authority

Authority order, highest first:

1. [Platform Architecture](../architecture/platform_architecture.md) Laws 1–15,
   §6 domain allocations, §7 relationships and gates, §8 cross-cutting
   principles, §11 governance precedence (G1–G6), §12 canonical vocabulary
   (V1–V4);
2. Domain Constitutions —
   [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md)
   and [Optimizer Philosophy](../investment/OPTIMIZER_PHILOSOPHY.md);
3. [ADR-001](../decisions/ADR-001_TRANSACTION_LEDGER_SINGLE_SOURCE_OF_TRUTH.md)
   through
   [ADR-005](../decisions/ADR-005_REPLAY_CORRECTNESS_BASELINE.md), and the
   [Decision Log](../engineering/DECISION_LOG.md);
4. frozen M34 ownership allocations, especially `M34-D-0001`, `M34-D-0004`,
   `M34-D-0005`, and `M34-D-0010`;
5. frozen M36, M39, M40–M41, and M42 contracts;
6. the frozen [M43 Architecture and Implementation Plan](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
   and frozen M43-WP1 through M43-WP8 artifacts;
7. this plan, after confirmation, within the authority classes declared above.

A lower authority cannot amend, weaken, reinterpret, or bypass a higher one.
Legacy source code, deployed formulas, libraries, provider behavior, API
contracts, and UI behavior are evidence of current state only and carry no
constitutional authority (constitution G6).

### 1.3 Predecessor milestone

M43 is `COMPLETE AND FROZEN` per [M43_EPIC_CLOSEOUT.md](M43_EPIC_CLOSEOUT.md)
and the [M43 epic decision](../engineering/DECISION_LOG.md#m43--portfolio-intelligence-method-specifications-epic-closeout).
M43 is the canonical baseline; M44 consumes it through its frozen normative
contracts only.

M43's closeout states explicitly that it *does not close an inherited gate and
grants no additional authority*, and that normative work packages whose
inherited gates remain open continue to report
`BLOCKED PENDING INHERITED GATE CLOSURE`. M44 exists because those gates are
still open and M43 can no longer close them.

### 1.4 Canonical dependencies

| Canonical artifact | Consumed as |
| --- | --- |
| [Platform Architecture](../architecture/platform_architecture.md) | Laws, domains, layer order, gates, governance precedence |
| [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md) | Accounting semantics §§1–9; consumption rule §10; invariants §11; open questions §12 |
| [M42-WP2](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md) | Portfolio Identity, Accounting Scope, Membership, Portfolio Base Currency |
| [M42-WP3 Stage B](M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md) | Investment Universe Declaration |
| [M42-WP5](M42_WP5_PORTFOLIO_BENCHMARK_DECLARATION_CONTRACT_SPECIFICATION.md) | Portfolio Benchmark Declaration, including `Explicitly None` |
| [M42-WP6](M42_WP6_PORTFOLIO_LIFECYCLE_STATE_REUSE_AND_PROVENANCE_CONTRACT_SPECIFICATION.md) | Portfolio Lifecycle State; Provenance carriage |
| [M42-WP7](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md) §5, §8, §9 | Portfolio Composition schema tag, canonical semantic field order, conditional canonical-byte representation permission, preserved canonical-byte obligation, negative vectors PC-NGV-11 through PC-NGV-14, conformance checklist items 10–12 |
| [M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§7–9, 16 | Boundaries, ownership rows, WP allocation |
| [M43-WP1 Register](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §1, §7, §8, §9 | Confirmation-record obligation, ownership finding, governance block, duplication controls, Glossary package |
| [M43-WP1 Reconciliation](M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md) | Legacy inventory, disposition matrix, negative corpus |
| [M43-WP2](M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md) §8 | Definition, Method Version, applicability, dependency declaration and closure |
| [M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md) §7 | `PMS1` framing and the representability failure |
| [M43-WP3 Manifest](M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md) §§6, 10 | `PAIM1` framing, ordering, identity, and the representability failure |
| [M43-WP4 Plan](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §§6.1–6.11, 7–9, 12 | Required normative semantic components A–K and their acceptance criteria |
| [M43-WP5 Plan](M43_WP5_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §§0, 3, 5–10, 13 | Required result-contract closures and acceptance criteria |
| [M43-WP6 Plan](M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §§3.1–3.2 | Binding-source paths and inherited gates |
| [M43-WP7 Plan](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §3.2 | The canonical enumeration of inherited external gates 1–10 |
| [M43-WP8 Plan](M43_WP8_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | Attribution-side inherited gates and blocked status |

### 1.5 Implementation authority granted and withheld

**Granted by this plan, after confirmation:** authority to author the
documentary governance, contract, and normative-specification artifacts
enumerated in §11, in `docs/` only.

**Withheld:** all runtime, source-code, persistence, schema, migration, API,
transport, UI, provider, scheduler, cache, observability, executable-test,
executable-fixture, production-method, and capability-completion authority.
M44 admits no production method. M44 declares no `ROADMAP.md` capability
complete.

### 1.6 Amendment rules

1. This plan may be corrected only through the review sequence in §12, and
   every correction must be independently confirmed.
2. Once confirmed, this plan is frozen. Later M44 work packages consume it by
   exact citation and may not redesign it.
3. M44 may not amend, edit, reinterpret, or restate any frozen M1–M43
   artifact. Where a frozen artifact is defective, M44 produces an additive
   superseding record that names the defect and its resolution, following the
   constitution's G5 rule that a wrong ruling is superseded by a new ruling
   that names it, never edited in place.
4. A conflict between this plan and a higher authority is a defect resolved
   upward (constitution G4), never by recency.

### 1.7 Revision provenance

RC1 was submitted for independent constitutional architecture review. The
review returned six findings and an approval recommendation of `REJECTED`. A
Formal Constitutional Response evaluated each finding against repository
evidence, and a Constitutional Adjudication then fixed the binding disposition
of every disputed finding. RC2 implements exactly those dispositions.

| Finding | Subject | Adjudicated disposition |
| --- | --- | --- |
| 1 | M44-WP4 Composition byte-encoding authority versus frozen M42-WP7 | Partially upheld — WP4 retained; the "declared silence" rationale removed and the authority re-grounded; explicit PC-NGV-11 through PC-NGV-14 conformance required |
| 2 | M44-WP5 creating or registering an owner-domain annualization contract | Upheld — every implication of contract creation or registration removed; ownership determination retained; G-4 remains `OPEN` absent the owner-domain instrument |
| 3 | Partial nested-coordinate routing treated as G-3 closure | Upheld — partial routing never counts as closure; G-3 may terminate `OPEN — PARTIAL`; WP6/WP7 cannot proceed without formable Composition bytes; a stop-or-re-scope checkpoint is added |
| 4 | G-2 closure versus the frozen correction path's recording vehicle | Not upheld as a defect — the frozen release condition is steps 1–3; RC2 separates block release from final recording and claims no final recording before an authorized vehicle exists |
| 5 | Provider-boundary failure wording | Partially upheld — "provider-sourced value" replaced with governance-based admissibility terminology distinguishing raw provider semantics from governed M39/M41 evidence |
| 6 | Indicative M45/M46/M47 milestone numbering | Upheld — milestone numbering removed and replaced with successor obligations |

The review, response, and adjudication artifacts are part of this plan's formal
review history. Until they are filed in `docs/implementation/`, they are cited
here by name and disposition rather than by repository path; filing them is a
governance-record obligation carried in §12.6 and §16.9.

RC2 introduces no constitutional decision that the adjudication did not
require, adds no scope, and removes no scope other than the authority the
adjudication withdrew.

---

## 2. Executive summary

### 2.1 What M44 introduces

M44 addresses the five inherited constitutional gates that currently block
every normative Portfolio Analytics method specification, and — where those
gates close — produces the two method-family-independent normative
specifications that all blocked method families depend on.

M44 does not guarantee closure of all five gates. G-3 and G-4 each depend on
instruments that other domains must supply and that M44 has no authority to
author. Where the required instrument is absent, the constitutionally correct
M44 outcome is a recorded, named, open gate — never a declared closure and
never a blockage recharacterized as closure (§16.2).

Concretely, M44 produces:

1. the missing repository-local M43 Architecture confirmation record required
   by frozen [M43-WP1 Register](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §1;
2. the governance correction of the M43 §8 canonical period-return ownership
   row required by frozen [M43-WP1 Register](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §7.4;
3. the Portfolio Composition canonical byte representation contract that
   frozen [M42-WP7](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md) §5
   expressly conditioned but did not supply, whose absence makes every `PMS1`
   subject and `PAIM1` manifest unformable, and which frozen
   [M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md)
   §7.1 identifies as the work of "a separately authorized contract";
4. the annualization-basis dependency **ownership determination**, and the
   exact specification of what an owner-domain governance instrument must
   supply before any annualization dependency can be declared — M44 authors no
   such instrument and registers no contract kind in any domain's corpus;
5. the normative Portfolio Analytics semantics specification discharging
   frozen M43-WP4 Components A–K; and
6. the normative Portfolio Measure Result contract specification discharging
   frozen M43-WP5.

### 2.2 Why it is needed now

M43 froze a complete plan and then closed without executing the
gate-conditional normative work it planned. Every method family — core
performance (M43-WP6), risk and benchmark-relative (M43-WP7), and attribution
(M43-WP8) — currently reports `BLOCKED PENDING INHERITED GATE CLOSURE`. The
blocking gates are owned by the M43 governance sequence and by upstream
contracts, not by any surviving M43 work package. M43's own closeout confirms
it closed none of them. Without a successor milestone that closes them, the
Portfolio Analytics corpus is permanently stalled and the Phase 3 Portfolio
Intelligence roadmap capabilities cannot advance.

### 2.3 What becomes possible after M44

- If, and only if, every nested coordinate reference required by frozen
  M42-WP7 §5 is supplied by its owner, a concrete Portfolio Measure Subject and
  Portfolio Analytics Input Manifest become formable, so identity, ordering,
  and hash-stability claims stop being artificial. If any required reference is
  unsupplied, G-3 terminates `OPEN — PARTIAL` and the downstream normative work
  does not proceed (§12.1 checkpoint).
- Every temporal, currency, calendar, benchmark-alignment, missing-data,
  precision, rounding, and arithmetic convention becomes explicit, owned, and
  non-overridable.
- Every Portfolio Measure Result acquires one immutable envelope with
  sufficiency, outcome, degraded-state, lineage, Provenance carriage, and
  canonical bytes.
- The period-return ownership row is reconciled and the standing M43-WP6 block
  is released on the frozen release condition, so a successor milestone may
  begin M43-WP6 normative core-performance method work.
- The annualization basis acquires a proved owner and an exact statement of the
  owner-domain instrument still required. Annualized methods remain blocked
  until that owner supplies it; they never acquire an implicit `252`.

### 2.4 What remains intentionally unavailable

No method formula, no method version admission, no executable artifact, no
registry, kernel, adapter, endpoint, schema, migration, cache, scheduler, or
UI change, and no roadmap capability completion. Core performance, risk,
benchmark-relative, and attribution method specifications remain allocated to
their frozen M43 work packages and to later milestones. Runtime realization,
compatibility, shadow validation, and cutover remain allocated to the frozen
M43-WP9 allocation, which M44 does not absorb (§4.5, §17 OQ-4).

---

## 3. Architectural motivation

### 3.1 The gap remaining after M43

M43 produced a nine-work-package plan and closed with eight. Of the eight,
WP1 produced the vocabulary and ownership register and the current-state
reconciliation; WP2 and WP3 produced normative contract specifications; WP4
through WP8 produced constitutional scope and implementation plans whose
normative specifications were never authorized to begin. The frozen corpus
therefore contains a complete description of work that cannot start.

Five specific, repository-confirmed unclosed obligations remain. Each is
labelled here as a gate and carried forward through the rest of this document.

**G-1 — M43 Architecture confirmation record absent.**
[M43-WP1 Register](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
§1 records that the commissioning authority holds the M43 Architecture as
`COMPLETE AND FROZEN` after Independent Constitutional Confirmation `APPROVED`,
that "the repository-local M43 plan header has not yet been synchronized to
that confirmed state," and that "a separately authorized governance change
must synchronize the plan's status line or provide its repository-local
confirmation artifact; WP1 cannot self-authorize that external edit."
[M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
line 3 still reads `Proposed status: READY FOR INDEPENDENT ARCHITECTURE
CONFIRMATION`, and no `M43_ARCHITECTURE_INDEPENDENT_*` artifact exists in
`docs/implementation/`. The obligation is unsatisfied and was not satisfied by
the epic closeout.

**G-2 — M43 period-return ownership governance correction outstanding.**
[M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §8 lists
"Canonical period-return rule — Candidate: Ledger & Accounting — OWNER TO
PROVE AT WP1." Frozen
[M43-WP1 Register](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
§7.3 rejected that composite claim and split it: the Portfolio-performance
*meaning* of the period return is Portfolio Intelligence's under Platform
Architecture §6.5 and M40-WP1 §8.3; the *accounting semantics determining what
enters the return* remain Ledger & Accounting's under Portfolio Calculation
Rules §§1–9. §7.4 therefore activates the standing block
`M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6` and specifies a
four-step correction path. Neither step 3 — an independently reviewed
constitutional correction of the governing M43 ownership row — nor step 4 —
its recorded final resolution — was performed. The M43 epic closeout expressly
closed no inherited gate.

G-2 has two constitutionally distinct components, and M44 keeps them separate:

- **Block release.** Frozen M43-WP1 §7.4 states the release condition exactly:
  *"Until steps 1–3 are complete, WP6 may not begin."* Step 3 is the
  independently reviewed constitutional correction of the M43 ownership row.
  M44-WP3 is that correction, and its independent confirmation discharges the
  release condition. Step 4 is not part of the release condition.
- **Final recording.** Step 4 requires that "the final resolution is recorded
  in the consolidated Decision Log entry authorized at M43 epic closeout by
  frozen M43 §§13 and 17." That named vehicle has passed. M44 does **not**
  claim step 4 discharged and does not assert final G-2 recording until a
  separately authorized recording vehicle exists. Until then G-2 is reported as
  `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`, which is an accurate
  status, not a closure claim (§17, OQ-5).

**G-3 — Portfolio Composition canonical-byte obligation undischarged.**
G-3 is an *unfulfilled delegated obligation*, not an encoding gap and not a
withheld authority.
[M42-WP7](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md) §5 fixes the
schema-version tag `M42-WP7-PORTFOLIO-COMPOSITION-1` and the ten-element
canonical semantic field order, and then does three separable things:

1. it **expressly conditions** a canonical-byte representation rather than
   forbidding one — "A representation may claim canonical bytes **only if** it
   preserves this tag, this order, exact citations, owner attributions,
   Provenance associations, and the explicit-absence distinction";
2. it **declines to supply** the representation itself — "This
   documentation-only contract defines no byte or character encoding,
   delimiter, escaping, container syntax, transport, serialization library, or
   persistence form. Those implementation details are outside scope"; and
3. it **preserves the obligation** for whoever does supply it — "Their
   exclusion does not remove or defer the frozen canonical-byte obligation."

Frozen
[M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md)
§7.1 then names the remedy: "until **a separately authorized contract supplies
the exact Composition canonical bytes**, no concrete Portfolio Measure
Subject — and consequently no concrete Portfolio Analytics Input Manifest — can
be formed," and the
[Manifest specification](M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md)
§6.3 and §10.3 repeat it. Every subject, manifest, result identity, hash, and
canonical byte claim in the entire Portfolio Analytics corpus is therefore
artificial until the obligation is discharged.

Two limits are constitutive of G-3 and are carried into every M44 artifact that
touches it:

- **The obligation is container-level only.** Frozen M42-WP7 §5 also states
  that its framing "does not define nested field order inside any source-owned
  coordinate or alter an upstream coordinate." Discharging G-3 means defining
  the Composition's own container framing over coordinate canonical
  *references*; it never means inventing the encoding of a source-owned nested
  coordinate. That prohibition is PC-NGV-14 and §9 checklist item 11, and it is
  a boundary on conforming canonical-byte language, not a bar against it.
- **The obligation is discharged whole or not at all.** Frozen M43-WP3 §7.1 is
  categorical: "If an owning contract cannot supply one exact immutable
  canonical reference or canonical representation required here, a conforming
  subject cannot be formed." Routing an unsupplied coordinate to its owner
  records the obligation; it does not discharge it. G-3 therefore admits
  exactly two terminal states — `CLOSED`, when every required coordinate
  reference is supplied and the container framing is confirmed, or
  `OPEN — PARTIAL`, when any is not. There is no third state, and
  `OPEN — PARTIAL` is not a closure (§11 M44-WP4, §12.1, §17 OQ-1).

**G-4 — Annualization-basis governed dependency absent.**
[M43-WP4 Plan](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §6.7
records that frozen M43-WP2 §8.1 requires an exact *existing* governed contract
kind for every declared calculation dependency, that "the frozen corpus
presently supplies no such annualization contract kind," and that WP4 "MUST
NOT author, name, imply, or serialize a new governed dependency contract."
Consequently every annualized method — annualized return, annualized
volatility, downside deviation, Sharpe, Sortino, tracking error, information
ratio, alpha — remains blocked "until a separately authorized governance
instrument supplies an exact owner, existing governed contract kind,
identifier, immutable version, and canonical value bytes."

M44 cannot be that instrument, on two independent frozen grounds:

- **The "existing" predicate.** Frozen
  [M43-WP2](M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md)
  §8.1 requires an "exact **existing** governed contract type," and §8.2(2)
  requires that "every owner and contract kind match the controlling frozen
  authority." A contract kind registered for the purpose cannot satisfy
  "existing" at the moment of declaration, and frozen M43-WP4 §5.2 expressly
  prohibits any "artificial contract kind, or WP4-authored dependency kind."
- **The owner-domain predicate.** Frozen M43-WP4 requires the owner to be
  proved "without expanding Portfolio Intelligence authority," with "source
  calendar meaning remain[ing] Market Intelligence-owned." M44 §5.1 records the
  annualization owner as presumptively **not** Portfolio Intelligence. An M44
  work package therefore has no authority to author, register, extend, or
  otherwise create a contract kind inside that owner's corpus.

G-4 accordingly admits exactly two terminal states in M44: `CLOSED`, only if an
owner-domain governance instrument satisfying frozen M43-WP2 §8.1 already
exists and is identified, or `OPEN`, with the exact missing element and the
exact owner it must come from recorded by name. M44 produces the ownership
determination and the specification of what that instrument must contain; it
does not produce the instrument.

**G-5 — The two universal normative specifications do not exist.**
[M43-WP7 Plan](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §3.1
names the two required binding-source paths,
`docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`
and
`docs/implementation/M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md`,
and states that "a plan, expected filename, or unchanged prerequisite is not a
substitute for an existing independently confirmed normative specification."
Frozen [M43-WP8 Plan](M43_WP8_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md)
§4 records the same finding as a validation outcome: "The required WP4 and WP5
normative specifications and WP6 normative method specification are not
currently present. Consequently, future WP8 normative method work remains
blocked." Neither file exists in the repository.

### 3.2 Why M44 belongs immediately after M43

Each of G-1 through G-5 is a direct, cited obligation of a frozen M43 or M42
artifact. None can be discharged inside M43, which is closed and unamendable.
None is a new capability, and none can be deferred without leaving all three
remaining Portfolio Analytics method families permanently blocked. M44 is
therefore the narrowest defensible successor: it adds no new architectural
ambition, it only completes obligations the frozen corpus already imposed.

### 3.3 Roadmap position

```text
M39                M40–M41            M42                  M43                  M44
Market          → Market Measure  → Portfolio          → Portfolio Analytics → Gate closure and
Observation       rules              Composition          contracts             universal normative
                                                          (planned, blocked)    semantics
```

M44 advances, without deploying, the same four Phase 3 Portfolio Intelligence
roadmap capabilities that M43 advanced: Rolling Analytics, Advanced Risk
Metrics, Position Attribution, and Sector Attribution Timeline. Consistent
with frozen [M43-WP1 Reconciliation](M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
§2, `docs/architecture/ROADMAP.md` receives no capability-completion mark and
is not modified by M44.

### 3.4 Milestone class

M44 is a **governance-correction, contract-completion, and normative
specification milestone**. It is not an implementation milestone, not an
integration milestone, and not a mixed milestone: it authorizes no source,
runtime, persistence, API, or UI change of any kind.

---

## 4. Scope partition

Every capability named anywhere in this document belongs to exactly one
partition below.

### 4.1 INCLUDED

| # | Included capability | Closes |
| --- | --- | --- |
| I-1 | Inherited-gate inventory, closure register, and roadmap/current-state reconciliation for M44 | prerequisite to all |
| I-2 | Repository-local M43 Architecture confirmation record and status reconciliation | G-1 |
| I-3 | Constitutional correction of the M43 §8 canonical period-return ownership row, superseding it without editing it | G-2 |
| I-4 | Portfolio Composition container-level canonical byte representation contract, subordinate to the frozen M42-WP7 tag and field order | G-3, only if I-5 closes completely |
| I-5 | Nested coordinate canonical-reference obligation inventory and per-coordinate closure or fail-closed routing; any routed coordinate leaves G-3 `OPEN — PARTIAL` | G-3, or determines that G-3 cannot close |
| I-6 | Annualization-basis ownership determination and the exact specification of the owner-domain governance instrument still required | G-4 only if that instrument already exists; otherwise G-4 remains `OPEN` |
| I-7 | Normative Portfolio Analytics semantics specification discharging frozen M43-WP4 Components A–K, including the risk-free-evidence authority-class proof | G-5 |
| I-8 | Normative Portfolio Measure Result contract specification discharging frozen M43-WP5 | G-5 |
| I-9 | Documentary positive, boundary, and negative vectors for I-7 and I-8, and for I-4 once bytes are formable | supporting |
| I-10 | Independent review, correction, and confirmation chains for every M44 artifact | governance |
| I-11 | M44 Epic Closeout, Decision Log entry, and Implementation INDEX synchronization performed at closeout under separate authorization | governance |

### 4.2 EXCLUDED

Explicitly outside M44 and not deferred to a later M44 stage:

- any executable artifact — source module, test, harness, runnable fixture,
  serializer, or validator;
- any schema, migration, persistence design, cache, scheduler, endpoint,
  transport, or UI change;
- any provider integration, symbol resolution, or live lookup;
- admission or activation of any production method;
- modification, restatement, or reinterpretation of any frozen M1–M43
  artifact, including the frozen M43 Architecture header;
- modification of `docs/architecture/ROADMAP.md` capability status;
- settlement of the three open accounting questions in
  [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md)
  §12 (`daily_return_pct` deprecation, fallback pricing for stripped
  non-performance transactions, ledger-validity precondition);
- redefinition of Portfolio Identity, Accounting Scope, Portfolio Membership,
  Portfolio Base Currency, Investment Universe, Benchmark Declaration,
  Lifecycle State, or Provenance meaning;
- Portfolio Policy or any renamed equivalent;
- cross-portfolio, household, net-worth, or Wealth Intelligence semantics;
- recommendation, optimization, suitability, constraint, execution, grading,
  causal, regime, or human-versus-AI semantics;
- BHB decomposition and benchmark-relative attribution.

### 4.3 DEFERRED

Named, real, and intentionally postponed to a later separately authorized
milestone:

| # | Deferred capability | Blocked on |
| --- | --- | --- |
| D-1 | M43-WP6 normative core performance and rolling method specification | M44-WP3 (G-2) and M44-WP6/WP7 |
| D-2a | M43-WP7 normative risk methods that do **not** depend on the annualization basis | D-1 |
| D-2b | M43-WP7 normative risk and benchmark-relative methods that depend on the annualization basis | D-1, plus an owner-domain annualization governance instrument that M44 does not author (G-4) |
| D-3 | M43-WP8 normative position and sector attribution method specification | D-1 |
| D-4 | M43-WP9 runtime realization, compatibility, and cutover design | D-1 through D-3 |
| D-5 | Executable Portfolio Analytics implementation, registry, kernel, adapters, shadow parity, and API cutover | D-4 |
| D-6 | Benchmark `Composite` and `Category` evidence construction and matching | separate governed Market Intelligence evidence |
| D-7 | The owner-domain annualization-basis governance instrument itself | the determined owner domain, acting under its own authority; M44 supplies only the requirement specification (§11 M44-WP5) |

Where this document refers to `D-2` without a suffix, it means D-2a and D-2b
together. D-2b is separately blocked by G-4 and by D-7.

### 4.4 NON-GOALS

- Making current analytics behavior canonical, or preserving it as precedent.
  Frozen [M43-WP1 Reconciliation](M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
  §4 dispositions remain controlling.
- Producing user-visible capability, performance improvement, or any change a
  user could observe.
- Reducing the number of remaining M43 work packages by absorbing their method
  scope into M44.
- Achieving completeness of the annualization contract by inventing an owner,
  by authoring the contract, or by registering a contract kind in another
  domain's corpus. If ownership cannot be proved, or if the owner-domain
  instrument does not already exist, the correct M44 outcome is a recorded,
  named, open gate stating the exact missing element and its exact owner.
- Declaring a gate closed on the strength of a recorded blockage. A blockage is
  an honest terminal state for a work package; it is never a gate closure
  (§16.2).

### 4.5 SUCCESSOR OBLIGATIONS

M44 has no future-milestone allocation authority. It assigns no milestone
number to any successor and creates no obligation on any milestone after itself
beyond recording what remains open. Consistent with the frozen
[M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md), which defers
work by obligation and prerequisite and never by forward milestone number, the
remaining work is recorded as follows:

| Successor obligation | Discharges | May begin when |
| --- | --- | --- |
| Normative core performance and rolling method specification | D-1 | M44-WP3 confirmed; M44-WP6 and M44-WP7 confirmed and frozen |
| Normative risk and benchmark-relative method specification | D-2a, and D-2b only in its non-annualized part until G-4 closes | D-1 frozen |
| Normative position and sector attribution method specification | D-3 | D-1 frozen |
| Runtime realization, compatibility, and cutover design, discharging the live frozen M43-WP9 allocation | D-4 | D-1 through D-3 frozen |
| Executable Portfolio Analytics implementation and cutover | D-5 | D-4 frozen, under a separately authorized implementation milestone |
| Owner-domain annualization-basis governance instrument | D-7 | the determined owner domain acts; no M44 successor obligation attaches |

Each row states an obligation and its prerequisite. No row allocates a
milestone, assigns a number, or binds a future author to a work-package
decomposition.

---

## 5. Constitutional boundaries

### 5.1 What M44 owns

| Owned surface | Owning domain | Basis |
| --- | --- | --- |
| The documentary resolution of the M43 §8 period-return ownership row, and the release of the standing M43-WP6 block | M43 governance sequence, exercised by M44 | frozen M43-WP1 §7.4 step 3 and the release condition at "Until steps 1–3 are complete, WP6 may not begin" |
| The exact **container-level** canonical byte representation of Portfolio Composition, subordinate to the frozen tag and field order | Portfolio Intelligence, as sole owner of the Portfolio Composition noun | Platform Architecture §6.5; M42-WP7 §5 conditional representation permission ("may claim canonical bytes only if…") and preserved canonical-byte obligation; M42-WP7 §9 checklist item 1; frozen M43-WP3 §7.1 "a separately authorized contract" |
| The normative temporal, currency, calendar, benchmark-alignment, missing-data, numeric, precision, rounding, dependency-arithmetic, and canonical-serialization semantics of Portfolio measures | Portfolio Intelligence | frozen M43-WP4 §§4, 6 |
| The normative Portfolio Measure Result envelope, sufficiency, outcome, lineage, Provenance carriage, and result serialization | Portfolio Intelligence | frozen M43-WP5 §§0, 5 |
| The determination of the annualization-basis owner, and the requirement specification for the owner-domain governance instrument | determination exercised by M44-WP5; the annualization basis itself is owned by a domain presumptively **not** Portfolio Intelligence | frozen M43-WP4 §6.7 |

M44 owns no surface in another domain's corpus. In particular it does not own,
author, register, extend, or version the annualization-basis dependency
contract; that contract is owned exclusively by the domain M44-WP5 proves, and
is produced under that domain's own authority (D-7).

### 5.2 What M44 consumes but does not own

Ledger events, replay, snapshots, accounting semantics, and the period-return
inputs (Ledger & Accounting). Market Observations, Market Measures, benchmark
series, FX, risk-free observations, calendars, and market-reference meaning
(Market Intelligence). Asset identity, currency dimension, Asset
Classification, and taxonomy (Asset Foundation). Provenance meaning and capture
(Connectivity & Ingestion). Portfolio Identity, Accounting Scope, Membership,
Base Currency, Investment Universe, Benchmark Declaration, Lifecycle State, and
Portfolio Composition semantics (frozen M42). Analytical Grouping
(Portfolio Intelligence, frozen under `M34-D-0001` and `M34-D-0004`).
Recommendations and actions (Decision Intelligence). Grades and causal
evaluation (Trust & Evaluation). Rendering (Experience Platform).

### 5.3 What M44 may extend

M44 may extend a frozen contract only on one of three exact bases, and every
M44 artifact must name which basis it relies on and quote the frozen sentence
that supplies it.

**E-1 — Express conditional permission preserved by the frozen contract.** The
frozen contract states the conditions under which the extension is conforming
and states that its own silence on the mechanism does not extinguish the
obligation. This is the basis for the Portfolio Composition container-level
byte representation: frozen M42-WP7 §5 states that "a representation may claim
canonical bytes **only if** it preserves this tag, this order, exact citations,
owner attributions, Provenance associations, and the explicit-absence
distinction," and that "their exclusion does not remove or defer the frozen
canonical-byte obligation." A contract that forbade the representation would
not state the conditions under which it conforms.

**E-2 — A remedy the frozen corpus names but does not supply.** A frozen,
independently confirmed artifact identifies the instrument required to
discharge an obligation and declines to produce it. Frozen M43-WP3 §7.1 does
exactly this: "until **a separately authorized contract** supplies the exact
Composition canonical bytes, no concrete Portfolio Measure Subject … can be
formed." M44-WP4 is that separately authorized contract.

**E-3 — Addition into declared silence, under constitution G3.** Residual and
subordinate to E-1 and E-2. It supports supplying a repository-local record
where a frozen governance chain required one and none was written (G-1), and
supplying a superseding ruling that names a defective frozen row (G-2). It is
**not** the basis for the Composition byte contract; that authority rests on
E-1 and E-2, which are stronger and more exact, because M42-WP7 §5 is not
silent on canonical bytes — it speaks, conditions, and preserves.

M44 may not extend by reinterpretation, relaxation, generalization, or by
adding a coordinate, field, form, or state to a frozen contract. No M44
extension reaches upstream: M44 defines no nested source-owned encoding,
field, schema, or identifier, and creates no contract kind in another domain's
corpus.

### 5.4 What M44 must not reinterpret

- The frozen M42-WP7 schema-version tag, ten-element canonical semantic field
  order, explicit-absence distinction, owner attributions, and Provenance
  associations.
- The frozen M42-WP7 §8 non-conforming-shape vectors PC-NGV-01 through
  PC-NGV-14 and the §9 conformance checklist. M44-WP4 must prove
  non-triggering against them; it may not read any of them as narrowed,
  inapplicable, or superseded.
- The frozen M43-WP1 §7.3 ownership split. M44-WP3 reconciles the *M43 §8
  row* to that split; it does not revisit, widen, narrow, or re-argue the
  split itself.
- The frozen M43-WP2 identity, applicability, dependency-declaration, and
  closure grammar, including the requirement that a dependency contract kind
  be an exact *existing* governed contract type.
- The frozen M43-WP3 `PMS1` and `PAIM1` framings, ordering, and identity
  rules.
- `UNAVAILABLE` remains a Degraded State under `M34-D-0005` and M40-WP1 §8.3
  and never becomes a Portfolio Computation Outcome.
- Portfolio Calculation Rules §§1–9 accounting semantics and §10 consumption
  rule.
- The vocabulary dispositions closed by frozen M43-WP1 and restated in frozen
  [M43-WP7 Plan](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §5.1.

### 5.5 Which previous artifacts remain authoritative

All of them. Every M1–M43 frozen artifact remains authoritative in its own
scope and unchanged in the repository. M44 artifacts are subordinate to them
and cite them exactly.

### 5.6 Layers M44 is prohibited from bypassing

- **Identity → Observation → Truth → Knowledge.** M44 specifies Knowledge-layer
  semantics only. It may not create Truth, originate an Observation, mint
  identity, or consult a live authority.
- **The three gates.** M44 touches none of the ingestion, decision, or
  configuration gates.
- **Trust as observer plane.** No M44 artifact produces or consumes a grade,
  calibration, counterfactual, or evaluator verdict.
- **Experience computes nothing.** No M44 artifact assigns a calculation to a
  presentation surface.
- **One implementation per rule (Law 9).** M44 creates no second period-return
  rule, no second serialization of an owned contract, and no second result
  envelope.

---

## 6. Architectural invariants

Every M44 implementation and artifact must preserve the following. Each is
stated so that a reviewer can falsify it against repository evidence.

**Authority**

- INV-A1 — Every M44 artifact declares runtime, source-code, persistence,
  schema, API, UI, provider, implementation, production-method, and
  executable-validation authority as `NONE`.
- INV-A2 — No M44 artifact grants authority that its predecessor plan withheld;
  a reviewer can trace every asserted authority to an exact citation in this
  plan.
- INV-A3 — No M44 artifact closes a gate it does not own; gate closures occur
  only in the work package this plan assigns them to.

**Ownership**

- INV-O1 — Every semantic concern named by an M44 artifact has exactly one
  owner, and that owner matches the frozen allocation or an M44 determination
  that was independently confirmed.
- INV-O2 — No M44 artifact transfers ownership of accounting semantics,
  calendar meaning, market evidence, Provenance meaning, or asset
  classification to Portfolio Intelligence.
- INV-O3 — An unresolved owner is a blocking condition, never an implicit
  assignment.

**Determinism**

- INV-D1 — No M44 semantic rule depends on wall-clock time, host locale,
  process, library default, provider state, cache state, database state,
  Workspace, or Current Selection.
- INV-D2 — Two independent readers applying an M44 normative rule to the same
  inputs reach the same result, including the same rounding, ordering, and
  tie-break outcome.
- INV-D3 — Every retained numerical convention has an explicit owner and
  binding rule; no convention is ambient, inferred, or caller-supplied.

**Persistence**

- INV-P1 — M44 defines no persistence form. Any statement about storage is
  descriptive of a future separately authorized milestone and carries no
  authority.
- INV-P2 — No M44 contract requires or implies a database entity, column,
  index, or migration.

**Identity**

- INV-I1 — Identity is canonical bytes. No M44 contract introduces a second
  identity axis, mutable key, digest-as-identity, registry address, or
  revision counter.
- INV-I2 — A canonical byte sequence is injective and round-trippable: one
  valid logical value has exactly one byte sequence, and one valid byte
  sequence reconstructs exactly one logical value.
- INV-I3 — Any change to any canonical byte produces a different identity.

**Ordering**

- INV-R1 — Every list, map, or set in an M44 contract has an explicit total
  order and tie-break rule, independent of input, storage, or presentation
  order.
- INV-R2 — Permuting the presentation order of inputs never changes an
  identity or a result.

**Isolation**

- INV-S1 — Exactly one Portfolio Composition representing one Portfolio
  Identity and its corresponding Accounting Scope is the permitted subject.
- INV-S2 — No M44 artifact admits cross-portfolio, household, person, or
  Wealth subject state.

**Compatibility**

- INV-C1 — No frozen M1–M43 artifact is modified, and `git diff` for M44
  contains no frozen-artifact path.
- INV-C2 — Every M44 addition rests on exactly one of the extension bases E-1,
  E-2, or E-3 in §5.3, names which one, and quotes the exact frozen sentence
  that supplies it. No addition is justified by unstated silence.
- INV-C4 — No M44 artifact reaches upstream. It defines no nested source-owned
  encoding, field order, schema, or identifier, and creates, registers, or
  extends no contract kind in a domain M44 does not own. A reviewer can falsify
  this against frozen M42-WP7 PC-NGV-14 and frozen M43-WP4 §5.2.
- INV-C3 — A change to a confirmed M44 rule creates a new version of the
  affected contract, never an edit to a frozen one.

**Observability**

- INV-B1 — Every non-success outcome carries a named, enumerated,
  deterministic reason; no outcome is silent, empty, or generic.
- INV-B2 — Every open gate is named, cited by exact path and section, and
  reported in every artifact that inherits it.

**Failure behavior**

- INV-F1 — Every M44 boundary fails closed. Missing, ambiguous, conflicting,
  or unrepresentable input produces a named non-success outcome, never a
  default, substitution, inference, repair, or fallback.
- INV-F2 — No absence is reinterpreted as an affirmative state; in particular
  a missing Portfolio Benchmark Declaration coordinate never becomes
  `Explicitly None`.
- INV-F3 — Failure of one gate blocks only the affected claim; it never
  weakens another rule and never authorizes an alternate path.

**Replay and idempotency**

- INV-Y1 — Applying an M44 normative rule twice to identical inputs yields
  byte-identical output.
- INV-Y2 — No M44 rule reads or is affected by prior application of itself.

**Provider independence**

- INV-V1 — No M44 artifact names a provider, provider symbol, raw provider
  payload, provider answer, vendor field, or vendor default as canonical
  identity, evidence, or calculation input. These are collectively *raw
  provider semantics*.
- INV-V2 — Market evidence enters only as exact manifest-bound M39 Observations
  or M41 Market Measure Results. These are *governed evidence*.
- INV-V3 — Admissibility is decided by governance, not by origin. A datum is
  admissible if and only if a governed owning contract supplies it and a
  manifest binds it exactly. That an underlying fact originated outside the
  platform never makes governed evidence inadmissible, and Provenance carriage
  alone never makes raw provider semantics admissible.

**API stability**

- INV-X1 — M44 defines no API. No M44 rule constrains, promises, or deprecates
  a current endpoint, and current endpoints remain untouched legacy reality.

**Data migration**

- INV-M1 — M44 requires no data migration and authorizes no backfill, repair,
  or recomputation of any stored record.
- INV-M2 — Existing `PortfolioSnapshot`, `BenchmarkPrice`, `AttributionMetric`,
  and `ShadowPortfolioSnapshot` rows remain Ledger-derived or legacy evidence
  and are never retroactively declared Portfolio Measure Results.

---

## 7. Dependency model

### 7.1 Upstream dependencies

| Dependency | Kind | Mandatory | Why it exists | Governing artifact |
| --- | --- | --- | --- | --- |
| Platform Architecture Laws 1–15, §§6–8, 11–12 | Governance | Mandatory | Supplies the layer order, domain ownership, gates, precedence, and vocabulary rules every M44 determination must satisfy | [platform_architecture.md](../architecture/platform_architecture.md) |
| Portfolio Calculation Rules §§1–9 | Governance + data | Mandatory | Owns the accounting semantics determining what enters the period return; M44-WP3 reconciles ownership without touching them | [PORTFOLIO_CALCULATION_RULES.md](../investment/PORTFOLIO_CALCULATION_RULES.md) |
| Portfolio Calculation Rules §10 | Governance | Mandatory | The consumption rule prohibiting independent recomputation of return; controlling for M44-WP3's correction statement | same |
| ADR-001 – ADR-005 | Governance | Mandatory | Ledger source-of-truth, no-compensation, two-timeline, one-implementation, and replay-correctness constraints | [docs/decisions/](../decisions/) |
| `M34-D-0001`, `M34-D-0004` | Governance | Mandatory | Analytical Grouping and classification allocations that M44 must not blur | m34 audit corpus |
| `M34-D-0005` | Contract | Mandatory | Canonical Temporal Claim and Degraded State producing-domain grammar reused by the result contract | m34 audit corpus |
| `M34-D-0010` | Governance | Mandatory | Provenance meaning and capture ownership; the result contract carries, never recaptures | m34 audit corpus |
| M39 Market Observation contracts | Contract + data | Mandatory | The only admissible form of market evidence, including risk-free evidence | [M39 corpus](M39_WP1_Canonical_Boundary_Specification.md) |
| M40–M41 Market Measure contracts | Contract | Mandatory | Mechanical precedent for definitions, method versions, manifests, results, and golden vectors; never subject reuse | [M41-WP1](M41_WP1_DEFINITION_METHOD_VERSION_APPLICABILITY_CONTRACT_SPECIFICATION.md), [M41-WP3](M41_WP3_STAGE_B_TEMPORAL_UNIT_ADJUSTMENT_ARITHMETIC_CONTRACT_SPECIFICATION.md) |
| M40-WP1 §8.3 | Governance | Mandatory | Reserves portfolio measure, performance, attribution, exposure, and risk to Portfolio Intelligence; freezes `UNAVAILABLE` as Degraded State | [M40-WP1](M40_WP1_Canonical_Market_Measure_Vocabulary_and_Ownership_Specification.md) |
| M42-WP2/WP3/WP5/WP6/WP7 | Contract | Mandatory | The Portfolio coordinates whose canonical references M44-WP4 must encode | M42 corpus |
| M42-WP7 §5, §8, §9 | Contract | Mandatory | Fixes the tag and field order the byte contract must preserve exactly; supplies the conditional representation permission and preserved canonical-byte obligation that authorize M44-WP4; supplies PC-NGV-11 through PC-NGV-14 and checklist items 10–12, against which M44-WP4 must prove non-triggering | [M42-WP7](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md) |
| M43 Architecture §§7–9, 16 | Governance | Mandatory | Boundaries, ownership rows, WP allocation, risk responses | [M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) |
| M43-WP1 register and reconciliation | Governance + contract | Mandatory | Vocabulary, ownership split, standing block, negative corpus, legacy dispositions | M43-WP1 corpus |
| M43-WP2 | Contract | Mandatory | Definition, Method Version, applicability, dependency declaration and closure | [M43-WP2](M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md) |
| M43-WP3 Subject and Manifest | Contract | Mandatory | The `PMS1`/`PAIM1` framings M44-WP4 makes formable | M43-WP3 corpus |
| M43-WP4 plan §§6–9, 12 | Sequencing | Mandatory | The exact component list and acceptance criteria M44-WP6 must discharge | [M43-WP4 Plan](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) |
| M43-WP5 plan §§3, 5–10, 13 | Sequencing | Mandatory | The exact closure list and acceptance criteria M44-WP7 must discharge | [M43-WP5 Plan](M43_WP5_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) |
| M43-WP6/WP7/WP8 plans | Sequencing | Mandatory | Canonical enumeration of the inherited gates M44 must close and must not weaken | M43 corpus |
| `docs/GLOSSARY.md` | Governance | Mandatory | V1–V2 registration target if any M44 noun is admitted or renamed | [GLOSSARY.md](../GLOSSARY.md) |

### 7.2 Downstream consumers

| Consumer | Kind | Consumes |
| --- | --- | --- |
| D-1 M43-WP6 normative core performance specification | Sequencing + contract | M44-WP3 correction; M44-WP6 semantics; M44-WP7 result contract; M44-WP4 bytes |
| D-2a M43-WP7 non-annualized risk specification | Sequencing + contract | all of the above; not the annualization basis |
| D-2b M43-WP7 annualized risk and benchmark-relative specification | Sequencing + contract | all of the above, plus M44-WP5's ownership determination **and** the owner-domain instrument of D-7, which M44 does not produce |
| D-3 M43-WP8 normative attribution specification | Sequencing + contract | all of D-1's inputs; not M44-WP5 unless an attribution method requires annualization |
| D-4 M43-WP9 runtime realization design | Sequencing | the complete confirmed corpus |
| Decision Intelligence, Trust & Evaluation, Experience Platform | Governance | nothing operationally; they remain downstream observers with no M44 dependency |

### 7.3 Runtime dependencies

`NONE`. M44 introduces no runtime component and depends on no running system.
Existing backend and frontend behavior is unaffected and unmodified.

### 7.4 Storage dependencies

`NONE` mandatory. Existing tables are cited as current-state evidence under
constitution G6 only, never as contract inputs.

### 7.5 Service dependencies

`NONE`. No M44 artifact requires a service to exist, run, or respond.

### 7.6 Contract dependencies

Mandatory: M34-D-0005, M34-D-0010, M39, M40–M41, M42-WP2/WP3/WP5/WP6/WP7,
M43-WP1/WP2/WP3. Each is consumed by exact citation, at its frozen meaning,
with no subject substitution across the Market/Portfolio seam.

### 7.7 Provider dependencies

`NONE`, and prohibited. Raw provider semantics — provider symbols, raw provider
payloads, provider answers, and vendor defaults — are inadmissible as identity,
evidence, or calculation input (INV-V1). Governed M39 Observations and M41
Market Measure Results are admissible and mandatory (INV-V2), and remain so
irrespective of the external origin of the underlying fact (INV-V3). M44
depends on no provider; it depends on the governed contracts that own the
evidence.

### 7.8 Optional dependencies

| Optional dependency | Kind | Effect if absent |
| --- | --- | --- |
| An existing governed contract kind suitable for the annualization basis, already present in the determined owner's corpus | Contract | G-4 remains `OPEN`. M44-WP5 records the exact missing element and its exact owner, and specifies what the owner-domain instrument must supply. M44 does not author, register, or extend the kind under any circumstances. Annualized methods remain deferred under D-2b and D-7 |
| Graphify knowledge graph refresh | Tooling | Skipped; M44 changes no source and creates no graph obligation |

### 7.9 Prohibited dependencies

Live provider answers; wall-clock time; Current Selection or Workspace
defaults; inferred Portfolio Base Currency; request-default benchmarks; hidden
risk-free rates; hidden calendars or annualization factors; unversioned
classifications; cross-portfolio state; model output; recommendation,
optimizer, or evaluation results as measurement truth; process or library
defaults; database ordering; cache state. This list restates frozen M43
Architecture §7 and is not widened by M44.

---

## 8. Proposed component model

M44 produces documentary components only. "Component" below means a normative
artifact with an owner and a bounded responsibility, never a software module.
No component is speculative: each discharges exactly one gate from §3.1.

### 8.1 C1 — M43 Governance Reconciliation Record

- **Responsibility.** Record, as a repository-local artifact, the independent
  confirmation status of the frozen M43 Architecture, and reconcile the
  divergence between its in-file `Proposed status` line and its confirmed
  `COMPLETE AND FROZEN` state.
- **Authority.** Documentary governance record only. It states status; it
  grants nothing.
- **Inputs.** Frozen M43 Architecture; frozen M43-WP1 Register §1; M43 Epic
  Closeout; Implementation INDEX current-status statement; Decision Log M43
  entries.
- **Outputs.** One confirmation record stating the confirmed status, the exact
  divergence, and the reconciliation basis.
- **Dependencies.** None beyond its inputs.
- **Prohibited responsibilities.** Editing the frozen M43 header; restating
  M43 substance; granting authority; closing G-2 through G-5.
- **Expected location.** `docs/implementation/`.

### 8.2 C2 — Period-Return Ownership Correction Record

- **Responsibility.** Supersede the M43 Architecture §8 row "Canonical
  period-return rule — Candidate: Ledger & Accounting" with the confirmed
  frozen M43-WP1 §7.3 two-part allocation, and record the disposition of the
  standing block `M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6`.
- **Authority.** Constitutional correction of one named M43 ownership row,
  exercised by the M43 governance sequence under frozen M43-WP1 §7.4 **step 3**.
  Step 3 plus its independent confirmation discharges the frozen release
  condition "Until steps 1–3 are complete, WP6 may not begin." C2 carries no
  authority to discharge step 4, and asserts none. No other row, artifact, or
  allocation is in scope.
- **Inputs.** Platform Architecture §§6.3, 6.5; Portfolio Calculation Rules
  §§1–9 and §10; M40-WP1 §8.3; M42 Architecture §8; M42-WP1 §3; ADR-001;
  ADR-004; frozen M43 §8; frozen M43-WP1 §7.
- **Outputs.** One correction record; a superseded-row statement; an explicit
  release statement discharging the frozen steps 1–3 condition; a separate,
  explicitly undischarged statement of the step 4 recording obligation naming
  the lapsed vehicle; the exact conditions under which D-1 may begin.
- **Dependencies.** C1 for the confirmed status of the artifact whose row is
  corrected.
- **Prohibited responsibilities.** Re-arguing the §7.3 split; amending
  Portfolio Calculation Rules or any ADR; defining any formula; designing
  M43-WP6; settling any §12 open accounting question; claiming that step 4 is
  discharged, or that G-2 is finally recorded, before a separately authorized
  recording vehicle exists.
- **Expected location.** `docs/implementation/`; the ratified decision is
  recorded in [DECISION_LOG.md](../engineering/DECISION_LOG.md) at closeout
  under separate authorization.

### 8.3 C3 — Portfolio Composition Canonical Byte Representation Contract

- **Responsibility.** Supply the exact **container-level** canonical byte
  representation of a Portfolio Composition — the framing that carries the
  frozen `M42-WP7-PORTFOLIO-COMPOSITION-1` tag and the frozen ten-element
  canonical semantic field order over owner-supplied coordinate canonical
  references — so that a concrete `PMS1` subject and `PAIM1` manifest become
  formable.
- **Authority.** Portfolio Intelligence, as the sole owner of the Portfolio
  Composition noun under frozen M42-WP7 §9 checklist item 1, exercising
  extension bases **E-1** and **E-2** of §5.3:
  - E-1 — frozen M42-WP7 §5 expressly conditions the representation ("a
    representation may claim canonical bytes **only if** it preserves this tag,
    this order, exact citations, owner attributions, Provenance associations,
    and the explicit-absence distinction") and preserves the obligation ("their
    exclusion does not remove or defer the frozen canonical-byte obligation");
  - E-2 — frozen M43-WP3 §7.1 names "a separately authorized contract" as the
    instrument that supplies the exact Composition canonical bytes, and C3 is
    that contract.

  C3 does **not** rest on declared silence. It supplies representation only; it
  supplies no meaning; and it acts as owner of the Composition, not as a
  downstream consumer under frozen M42-WP7 §6, which withholds authority over
  *coordinates* and expressly permits reliance on the serialization boundary.
- **Required conformance proofs.** C3 is not conforming unless it proves, vector
  by vector, that it does not instantiate any frozen M42-WP7 §8 non-conforming
  shape, with these four addressed individually and by name:
  - **PC-NGV-11** — "A database, JSON, API, service, runtime object, byte
    encoding, or storage form is prescribed." Non-triggering basis: PC-NGV-11
    governs the shape of a conforming Portfolio Composition *specimen*, which
    must remain representation-free. C3 prescribes nothing inside a specimen
    and defines no database, JSON, API, service, runtime object, or storage
    form. That a downstream contract may define canonical byte framing is
    established by frozen M43-WP3 §7.2, which defines `PMS1` framing with
    `ASCII`, `u32`, and `lp(x)` and embeds
    `lp(portfolio_composition_canonical_bytes)`.
  - **PC-NGV-12 and PC-NGV-13** — proved non-triggering on their own terms by
    exact citation, with one negative vector each.
  - **PC-NGV-14** — "Canonical-byte language defines **upstream** encoding,
    fields, schema, or identifiers." Non-triggering basis: C3 defines only the
    Composition's own container framing and treats every coordinate as an
    opaque owner-supplied canonical reference. It defines no upstream encoding,
    field, schema, or identifier (INV-C4).
  - **§9 checklist items 10, 11, and 12** — item 11 ("no source-owned nested
    coordinate is reordered, normalized, encoded, or reinterpreted") and item 12
    ("canonical-byte obligations are preserved without invented encoding or
    removal, deferral, or weakening") are each answered with a direct
    conformance statement and at least one negative vector.
- **Inputs.** M42-WP7 §5, §8 vectors, §9 checklist; the coordinate contracts
  M42-WP2, M42-WP3 Stage B, M42-WP5, M42-WP6; `M34-D-0010` Provenance
  association rules; M43-WP3 Subject §7.1–§7.2 and Manifest §6.3, §10 framing
  conventions (`u32`, `lp(x)`, tagged, length-delimited, injective).
- **Outputs.** One container-level byte-representation contract; the
  nested-coordinate canonical-reference obligation inventory; per-coordinate
  closure or fail-closed routing; the PC-NGV conformance proof; positive,
  boundary, and negative documentary vectors.
- **Dependencies.** None among M44 components; strictly upstream.
- **Prohibited responsibilities.** Adding, removing, renaming, or reordering a
  coordinate; changing the tag; defining nested source-owned *meaning*;
  defining nested source-owned *encoding*, field order, schema, or identifiers;
  defining a persistence form, transport, or serializer implementation;
  inventing an encoding for a nested coordinate whose owner has not supplied
  one — that case fails closed, is routed to the owner, and leaves G-3
  `OPEN — PARTIAL`.
- **Expected location.** `docs/implementation/`; vectors under
  `docs/implementation/m44/fixtures/`.

### 8.4 C4 — Annualization Basis Ownership Determination and Requirement Specification

- **Responsibility.** Prove the constitutional owner of the annualization
  basis; prove the authority class (`VERSIONED_CALCULATION_DEPENDENCY` versus
  `GOVERNED_EVIDENCE`); prove that caller override is rejected; prove that the
  owner and placement expand no domain's authority; then determine, by search
  of the determined owner's frozen corpus, whether an exact **existing**
  governed contract kind is already present. If one is, C4 identifies it by
  exact citation. If none is, C4 records G-4 `OPEN` and specifies exactly what
  an owner-domain governance instrument must supply.
- **Authority.** Determination and requirement-specification authority only.
  C4 holds **no** contract-authoring authority, **no** contract-kind
  registration authority, and **no** authority in any domain's corpus other
  than Portfolio Intelligence's. Frozen M43-WP2 §8.1 requires an "exact
  *existing* governed contract type" and §8.2(2) requires that "every owner and
  contract kind match the controlling frozen authority"; frozen M43-WP4 §5.2
  prohibits any "artificial contract kind, or WP4-authored dependency kind."
  A kind registered for the purpose satisfies none of these.
- **Inputs.** Frozen M43-WP4 §§0, 5.2, 6.7, 7; frozen M43-WP2 §8.1–8.2;
  Platform Architecture §§6.2, 6.5; M39/M41 calendar and market-reference
  contracts.
- **Outputs.** One ownership determination with its four proofs; one corpus
  search result identifying an existing governed contract kind by exact
  citation, or recording that none exists; where none exists, one requirement
  specification stating the exact owner, contract kind, identifier, immutable
  version, and canonical value bytes that the owner-domain instrument must
  supply, and one recorded `OPEN` gate naming that missing element and owner.
- **Dependencies.** None among M44 components.
- **Prohibited responsibilities.** Expanding Portfolio Intelligence authority;
  transferring source calendar meaning out of Market Intelligence; naming a
  literal `252`, `365`, or `365.25` as an ambient value; authoring, drafting,
  registering, extending, versioning, or serializing a governed dependency
  contract in any domain's corpus; creating a contract kind that does not
  already exist in the owning domain's governed vocabulary; treating a
  requirement specification as an instrument; treating a recorded blockage as
  a gate closure; admitting a method that consumes the dependency.
- **Expected location.** `docs/implementation/`.

### 8.5 C5 — Portfolio Analytics Normative Semantics Specification

- **Responsibility.** Discharge frozen M43-WP4 Components A–K as one normative
  specification: Portfolio Measurement Window; economic versus record time and
  stable ordering; Portfolio Base Currency and FX; calendar and observation
  alignment; benchmark alignment; risk-free evidence authority class and
  binding; annualization-basis binding or recorded blockage; missing data,
  density, and partial windows; numeric model and arithmetic; dependency
  arithmetic; canonical serialization.
- **Authority.** Portfolio Intelligence normative semantics, non-production.
- **Inputs.** Frozen M43-WP4 plan; frozen M43-WP1/WP2/WP3; M42 coordinates;
  M39/M41 evidence contracts; C3 bytes; C4 outcome.
- **Outputs.** One normative specification; the explicit no-default matrix;
  the risk-free authority-class proof; the annualization binding or blockage
  statement; documentary numerical vectors; a normative-row-to-vector coverage
  ledger.
- **Dependencies.** C3 (for the WP3 bytes Component K must embed or cite), C4
  (for the annualization binding).
- **Prohibited responsibilities.** Defining any method formula; admitting any
  Portfolio Measure Definition or Method Version; defining result
  classification (that is C6); creating market evidence; selecting a provider,
  module, or call site.
- **Expected location.** `docs/implementation/`; vectors under
  `docs/implementation/m44/fixtures/`.

### 8.6 C6 — Portfolio Measure Result Normative Contract Specification

- **Responsibility.** Discharge frozen M43-WP5: result identity; value
  presence and absence; Portfolio Input Sufficiency; Portfolio Computation
  Outcome; Portfolio Deterministic Calculation; reuse of Degraded State under
  the `M34-D-0005` producing-domain grammar; reason-code grammar; method and
  manifest lineage; Provenance carriage without recapture; Canonical Temporal
  Claim compatibility; canonical result serialization; canonical-byte and hash
  stability.
- **Authority.** Portfolio Intelligence normative result contract,
  non-production.
- **Inputs.** Frozen M43-WP5 plan; frozen M43-WP1 §8 duplication controls;
  M40-WP1 §8.3; `M34-D-0005`; `M34-D-0010`; C3 bytes; C5 numeric, precision,
  and serialization semantics.
- **Outputs.** One normative result contract; the outcome/sufficiency/
  degradation matrix; the reason-code grammar; the Canonical Temporal Claim
  compatibility mapping; round-trip and hash-stability vectors.
- **Dependencies.** C3 and C5, both strict.
- **Prohibited responsibilities.** Admitting a method; defining a method-family
  value semantic; defining a runtime response, transport payload, cache value,
  database entity, or UI model; recapturing Provenance; promoting `UNAVAILABLE`
  to an outcome.
- **Expected location.** `docs/implementation/`; vectors under
  `docs/implementation/m44/fixtures/`.

### 8.7 C0 — Inherited Gate Closure Register

- **Responsibility.** Enumerate every inherited gate with exact path and
  section citations, map each to exactly one M44 work package or to an
  explicitly deferred milestone, reconcile the roadmap and current state for
  M44, and confirm whether any new noun is required.
- **Authority.** Evidence and navigation only. It closes nothing.
- **Inputs.** Frozen M43-WP7 §3.2 gate enumeration; frozen M43-WP8 §§2, 4;
  frozen M43-WP6 §§3.1–3.2; frozen M43-WP1 §§1, 7.4; M42-WP7 §5; M43-WP3 §7.1;
  M43-WP4 §§6.6–6.7.
- **Outputs.** The closure register; the M44 roadmap reconciliation; the
  vocabulary-sufficiency finding; the M44 negative corpus.
- **Dependencies.** None. It is first.
- **Prohibited responsibilities.** Closing a gate; admitting a noun; selecting
  an implementation; choosing an owner.
- **Expected location.** `docs/implementation/`.

---

## 9. Data and contract model

### 9.1 Reuse without modification

| Item | Owner | Basis |
| --- | --- | --- |
| Portfolio Identity, Accounting Scope, Portfolio Membership, Portfolio Base Currency | Ledger & Accounting / Portfolio Intelligence per M42-WP2 | frozen M42-WP2 |
| Investment Universe Declaration | Portfolio Intelligence | frozen M42-WP3 Stage B |
| Portfolio Benchmark Declaration, including `Explicitly None`, `Single`, `Composite`, `Category` | Portfolio Intelligence | frozen M42-WP5 |
| Portfolio Lifecycle State; Provenance association | Portfolio Intelligence / Connectivity & Ingestion | frozen M42-WP6; `M34-D-0010` |
| Portfolio Composition semantic definition, tag, field order | Portfolio Intelligence | frozen M42-WP7 §5 |
| Portfolio Measure Definition, Portfolio Method Version, applicability, dependency declaration and closure | Portfolio Intelligence | frozen M43-WP2 |
| Portfolio Measure Subject (`PMS1`), Portfolio Analytics Input Manifest (`PAIM1`) | Portfolio Intelligence | frozen M43-WP3 |
| Degraded State, Canonical Temporal Claim | producing-domain grammar under `M34-D-0005` | frozen M34 |
| Market Observation, Market Measure Result | Market Intelligence | frozen M39, M40–M41 |
| Asset Classification, Analytical Grouping | Asset Foundation / Portfolio Intelligence | `M34-D-0001`, `M34-D-0004` |

### 9.2 New contracts

| New contract | Kind | Owner | Produced by | Justification |
| --- | --- | --- | --- | --- |
| Portfolio Composition container-level canonical byte representation | Persistence-neutral serialization contract | Portfolio Intelligence | M44-WP4 | M42-WP7 §5 conditionally permits the representation and preserves the obligation; frozen M43-WP3 §7.1 names a separately authorized contract as the remedy; without it no subject, manifest, result identity, or hash is formable |
| Portfolio Analytics normative semantics contract | Semantic contract | Portfolio Intelligence | M44-WP6 | Frozen M43-WP4 allocation; no normative specification exists |
| Portfolio Measure Result contract | Semantic contract | Portfolio Intelligence | M44-WP7 | Frozen M43-WP5 allocation; no normative specification exists |

**Not produced by M44:** the annualization-basis governed dependency contract.
Frozen M43-WP2 §8.1 requires an exact *existing* governed contract kind and
frozen M43-WP4 §5.2 prohibits an authored one; the annualization basis is owned
by a domain presumptively other than Portfolio Intelligence. M44-WP5 produces
the ownership determination and the requirement specification only. The
instrument itself is D-7, produced by the determined owner under its own
authority. Every new contract in the table above is owned by Portfolio
Intelligence and registered in Portfolio Intelligence's corpus; M44 registers
nothing anywhere else (INV-C4).

### 9.3 Extensions of existing contracts

| Extended contract | Nature of the extension | Constraint |
| --- | --- | --- |
| M42-WP7 Portfolio Composition | Container-level representation supplied under the §5 conditional permission and preserved obligation (extension basis E-1/E-2, §5.3) | Tag, field order, explicit-absence distinction, owner attributions, and Provenance associations preserved byte-for-byte in meaning; no coordinate added, removed, renamed, or reordered; no nested source-owned encoding defined; non-triggering proved against PC-NGV-11 through PC-NGV-14 and §9 checklist items 10–12 |
| M43-WP3 `PMS1` / `PAIM1` | Made formable, not redefined — and only if every required coordinate reference is supplied | Framing, ordering, and identity rules unchanged; only the previously missing container-level Composition bytes are supplied; if any coordinate reference is unsupplied, the subject and manifest remain unformable and G-3 is `OPEN — PARTIAL` |
| M43-WP2 dependency declaration | **No extension.** M44 supplies no contract kind and makes no new dependency declarable | The declaration grammar and closure rules are unchanged and untouched. Whether an annualization dependency becomes declarable is determined by the owner-domain instrument (D-7), not by M44 |

### 9.4 Identifiers, records, and state models

M44 introduces no new identifier scheme. Identity remains canonical bytes
(INV-I1). M44 introduces no new state axis: Portfolio Computation Outcome and
Degraded State remain exactly as allocated by frozen M43-WP1 §8 and M40-WP1
§8.3.

### 9.5 DTOs, service contracts, persistence contracts, API contracts

`NONE`. M44 defines no DTO, service contract, persistence contract, or API
contract. Any future such artifact belongs to D-4 and D-5.

### 9.6 Event and observation contracts

`NONE` new. M44 consumes M39 Observations and M41 Market Measure Results by
exact citation and originates neither.

### 9.7 Vocabulary policy

M44 expects to require no new constitutional noun. Every term it uses is
already disposed by frozen M43-WP1 and restated in frozen M43-WP7 §5.1. If an
M44 work package proves an unavoidable new noun, it must run the frozen M43-WP1
downstream vocabulary rule — prove insufficiency, record exactly one
disposition, identify one owner and one normative home, perform repository-wide
collision analysis, obtain independent confirmation, and synchronize
[GLOSSARY.md](../GLOSSARY.md) in the same authorized change — before any
reliance.

---

## 10. Failure and boundary behavior

All M44 boundaries are **fail-closed**. There is no fail-open case anywhere in
this milestone, because every M44 artifact is a semantic contract whose only
safe response to an unrepresentable condition is a named non-success outcome.

| Condition | Architecture-level behavior |
| --- | --- |
| **Invalid input** | Reject with a named reason. No normalization, coercion, trimming, rounding-to-fit, or repair. A rejected input never produces a partial value. |
| **Unavailable dependency** | The affected claim is blocked and reported with the exact missing dependency's owner, contract kind, identifier, and version. No substitution, latest-version resolution, or compatible-range fallback. |
| **Partial data** | Explicitly classified: structurally absent input, authoritative absence carried by present evidence, boundary gap, interior gap, sparse-but-valid, or short-but-exact window. Each classification has one outcome; none defaults to "use what is available." |
| **Unsupported capability** | Named as unsupported and blocked. `Composite` and `Category` benchmark forms remain unavailable rather than collapsing to `Single`. An unsupported annualization dependency blocks the annualized claim rather than admitting a constant. |
| **Provider failure** | Not applicable by construction: no M44 artifact consults a provider. Admissibility at an M44 boundary is decided by governance, never by origin (INV-V3). **Raw provider semantics** — a provider symbol, raw provider payload, provider answer, or vendor default — are inadmissible as identity, evidence, or calculation input and are rejected with a named reason (INV-V1). **Governed evidence** — an exact manifest-bound M39 Observation or M41 Market Measure Result — is admissible and mandatory, and remains admissible irrespective of the external origin of the underlying fact (INV-V2). Provenance carriage alone never converts raw provider semantics into governed evidence. |
| **Persistence failure** | Not applicable by construction: M44 defines no persistence. A persistence-derived value is legacy evidence under G6 and is never a contract input. |
| **Authorization failure** | An artifact asserting authority this plan withheld is a constitutional defect; the artifact fails review and is corrected, never granted an exception. |
| **Inconsistent state** | Conflicting evidence for the same coordinate is a named conflict outcome. No precedence-by-recency, no source-priority heuristic, no averaging, no silent last-write-wins. |
| **Duplicate request** | Idempotent by construction (INV-Y1). A duplicate manifest entry for the same coordinate is a named duplicate-entry rejection, not a deduplication. |
| **Stale data** | There is no freshness concept in M44. Evidence is exact and manifest-bound or it is absent. "Recent," "current," and "latest" are prohibited selectors. |
| **Compatibility mismatch** | A method version, contract version, or schema tag mismatch is a hard rejection. No forward-compat reading, no unknown-field tolerance, no alternate-form acceptance, no trailing-byte tolerance. |
| **Unrepresentable nested coordinate** | The specific coordinate fails closed and is routed to its owning domain. M44 does not invent an encoding for another domain's coordinate, and one unrepresentable coordinate does not authorize a degraded whole-Composition encoding. Because frozen M43-WP3 §7.1 admits no partial subject, a single routed coordinate leaves G-3 `OPEN — PARTIAL`; routing records the obligation and never discharges it. |
| **Ownership proof failure** | The affected determination fails and no contract is authored — by M44 or on any domain's behalf. A failed ownership proof produces a recorded named blockage with the exact missing element and the exact owner it must come from, never an implicit owner (INV-O3). |
| **Required governance instrument absent** | The gate remains `OPEN`. M44 records what the instrument must supply and which domain owns it, and stops. M44 never substitutes a requirement specification for the instrument, and never recharacterizes a recorded blockage as a closure (§16.2). |

---

## 11. Work-package decomposition

Seven work packages. Each is independently reviewable, has one authority class,
and is responsible for a bounded set of gates. A work package completes by
recording the correct terminal state for each gate it owns, which may be a
non-closure state (§16.2). No work package promises a closure it may lack the
authority or the upstream inputs to reach.

### M44-WP1 — Inherited Gate Inventory, Roadmap Reconciliation, and Closure Register

- **Purpose.** Establish the authoritative, cited enumeration of every
  inherited gate and its M44 disposition before any closure is attempted.
- **Included scope.** Gate inventory with exact path and section citations;
  gate-to-work-package mapping; roadmap and current-state reconciliation for
  M44; vocabulary-sufficiency finding; M44 negative corpus; nested-coordinate
  encoding-obligation pre-inventory feeding WP4.
- **Excluded scope.** Closing any gate; admitting any noun; determining any
  owner; selecting any encoding.
- **Architectural deliverables.** `M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md`;
  `M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md`.
- **Implementation deliverables.** `NONE`.
- **Dependencies.** Frozen M42 and M43 corpora.
- **Predecessor requirements.** Confirmed M44 Architecture.
- **Expected repository impact.** Two new files in `docs/implementation/`.
- **Required tests.** Documentary only: citation-existence check for every gate
  (every cited path and section must resolve); completeness check against the
  frozen M43-WP7 §3.2 enumeration; collision and overlap scan; negative-corpus
  review.
- **Completion criteria.** Every gate named in any frozen M43 artifact appears
  exactly once with an exact citation and exactly one disposition of
  `CLOSED BY M44-WPn` or `DEFERRED TO D-n`; no gate is unassigned; no new noun
  is required, or each required noun has entered the vocabulary gate.
- **Freeze boundary.** Frozen on independent confirmation; later M44 work
  packages cite it and may not re-derive the inventory.
- **Downstream consumers.** M44-WP2 through WP7; D-1 through D-4.

### M44-WP2 — M43 Architecture Confirmation Record and Status Reconciliation

- **Purpose.** Close G-1 by supplying the repository-local confirmation
  artifact that frozen M43-WP1 §1 requires and that M43 never produced.
- **Included scope.** The confirmation record; the exact statement of the
  divergence between the frozen M43 header line and the confirmed status; the
  reconciliation basis drawn from the M43 Epic Closeout, Decision Log, and
  Implementation INDEX.
- **Excluded scope.** Editing the frozen M43 header; restating M43 substance;
  granting authority; any other gate.
- **Architectural deliverables.** `M44_WP2_M43_ARCHITECTURE_CONFIRMATION_RECORD.md`.
- **Implementation deliverables.** `NONE`.
- **Dependencies.** M44-WP1.
- **Predecessor requirements.** M44-WP1 confirmed.
- **Expected repository impact.** One new file; no frozen file touched.
- **Required tests.** Documentary: the record's claimed status matches the M43
  Epic Closeout and Decision Log verbatim in substance; `git diff` shows no
  frozen M43 path; the record asserts no authority.
- **Completion criteria.** G-1 recorded `CLOSED`; frozen M43 artifacts
  unchanged; independent confirmation with unresolved findings `NONE`.
- **Freeze boundary.** Frozen on confirmation.
- **Downstream consumers.** M44-WP3; every artifact citing M43 Architecture
  status.

### M44-WP3 — Period-Return Ownership Governance Correction

- **Purpose.** Perform step 3 of the correction path in frozen M43-WP1 §7.4,
  thereby discharging the frozen release condition for the standing M43-WP6
  block, and separately record the step 4 obligation as outstanding.
- **The two components of G-2, kept separate.** Frozen M43-WP1 §7.4 states the
  release condition exactly: *"Until steps 1–3 are complete, WP6 may not
  begin."* Step 3 is the independently reviewed constitutional correction of
  the M43 ownership row. M44-WP3, once independently confirmed, is that
  correction and discharges the release condition. Step 4 — recording the final
  resolution in the consolidated Decision Log entry authorized at M43 epic
  closeout — is a **recording** obligation, not a release condition, and its
  named vehicle has passed. M44-WP3 asserts no discharge of step 4.
- **Included scope.** Constitutional proof restating the confirmed §7.3 split
  against Platform Architecture §§6.3 and 6.5, Portfolio Calculation Rules
  §§1–9 and §10, M40-WP1 §8.3, ADR-001, and ADR-004; the superseding record
  for the M43 §8 row; an explicit **release statement** discharging the frozen
  steps 1–3 condition and disposing of the standing `M43-WP6 BLOCKED` item; an
  explicit **outstanding-recording statement** naming step 4, its lapsed
  vehicle, and the fact that final G-2 recording is not claimed; the exact
  preconditions under which D-1 may begin.
- **Excluded scope.** Re-arguing the split; amending Portfolio Calculation
  Rules or any ADR; defining any formula, method, or method version; designing
  M43-WP6; settling any Portfolio Calculation Rules §12 open question;
  selecting a call site; claiming step 4 discharged; claiming G-2 finally
  recorded before a separately authorized recording vehicle exists;
  authorizing or creating such a vehicle.
- **Architectural deliverables.** `M44_WP3_PERIOD_RETURN_OWNERSHIP_GOVERNANCE_CORRECTION.md`.
- **Implementation deliverables.** `NONE`.
- **Dependencies.** M44-WP1, M44-WP2.
- **Predecessor requirements.** M44-WP2 confirmed, so the corrected artifact's
  status is itself settled.
- **Expected repository impact.** One new file; a Decision Log entry at
  closeout under separate authorization.
- **Required tests.** Documentary: the correction cites every governing
  authority in frozen M43-WP1 §7.2; it states exactly one allocation per
  concern; it introduces no formula; a negative-corpus check confirms it does
  not create a second period-return rule (Law 9) and does not amend Portfolio
  Calculation Rules.
- **Completion criteria.** The M43 §8 row is superseded by name; the ownership
  split is restated verbatim in substance; step 3 is performed and
  independently confirmed, so the frozen steps 1–3 release condition is
  discharged and the standing block is dispositioned with explicit D-1
  preconditions; the step 4 recording obligation is recorded as outstanding
  with its lapsed vehicle named; G-2 is reported `RELEASED — FINAL RECORDING
  PENDING AUTHORIZED VEHICLE`, never `CLOSED`; unresolved findings `NONE`.
- **Freeze boundary.** Frozen on confirmation; D-1 cites it as its entry gate.
- **Downstream consumers.** D-1, D-2, D-3.

### M44-WP4 — Portfolio Composition Canonical Byte Representation Contract

- **Purpose.** Discharge the frozen M42-WP7 §5 canonical-byte obligation at
  container level, so that a concrete `PMS1` subject and `PAIM1` manifest
  become formable — or, if any required coordinate reference is unsupplied,
  establish and report that G-3 is `OPEN — PARTIAL`.
- **Authority basis.** Extension bases E-1 and E-2 of §5.3, exercised as sole
  owner of the Portfolio Composition noun (frozen M42-WP7 §9 checklist item 1).
  Not declared silence.
- **Included scope.** Nested-coordinate canonical-reference obligation
  inventory across all ten frozen M42-WP7 fields; the exact tagged,
  length-delimited, injective, round-trippable, order-stable,
  locale-independent **container-level** byte representation preserving the
  frozen tag and field order over opaque owner-supplied coordinate canonical
  references; explicit-absence representation for coordinates whose owner
  defines an affirmative absence; owner-attribution and Provenance-association
  representation; rejection rules for unknown fields, alternate forms,
  duplicate keys, non-canonical numbers, trailing bytes, and Unicode ambiguity;
  per-coordinate closure or fail-closed routing to the owning domain; the
  PC-NGV conformance proof required by §8.3; positive, boundary, and negative
  documentary vectors.
- **Excluded scope.** Nested source-owned *meaning*; nested source-owned
  *encoding*, field order, schema, or identifiers; adding, removing, renaming,
  or reordering any coordinate; changing the schema tag; persistence form,
  transport, or serializer implementation; the `PMS1`/`PAIM1` framings
  themselves, which remain frozen; declaring G-3 closed while any required
  coordinate reference is unsupplied.
- **Architectural deliverables.**
  `M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md`;
  `m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md`;
  `m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md`.
- **Implementation deliverables.** `NONE`.
- **Dependencies.** M44-WP1; frozen M42-WP2/WP3/WP5/WP6/WP7; frozen M43-WP3.
- **Predecessor requirements.** M44-WP1 confirmed.
- **Expected repository impact.** One new contract file; a new
  `docs/implementation/m44/fixtures/` directory with two vector files.
- **Required tests.** Documentary: injectivity and round-trip vectors;
  order-stability vectors under presentation permutation; explicit-absence
  versus missing-coordinate separation vectors; rejection vectors for each
  prohibited form; a coverage ledger mapping each of the ten frozen fields to
  at least one positive and one negative vector; a preservation check proving
  the tag and field order are byte-order-identical to frozen M42-WP7 §5; and a
  **non-triggering conformance proof** addressing PC-NGV-11, PC-NGV-12,
  PC-NGV-13, and PC-NGV-14 individually and by name, plus frozen M42-WP7 §9
  checklist items 10, 11, and 12, each with a direct conformance statement and
  at least one negative vector (§8.3).
- **Completion criteria.** The work package is complete in exactly one of two
  terminal states, and never in a blend of them:
  - **G-3 `CLOSED`** — every one of the ten frozen M42-WP7 coordinates has an
    owner-supplied exact immutable canonical reference; the container framing
    is confirmed; two independent readers derive byte-identical Composition
    bytes for the same logical Composition; the PC-NGV conformance proof
    passes; no frozen M42 artifact is modified; unresolved findings `NONE`.
  - **G-3 `OPEN — PARTIAL`** — at least one required coordinate reference is
    unsupplied. The container framing and the per-coordinate inventory are still
    delivered and confirmed, every unsupplied coordinate is named and routed to
    its owner with the exact missing element, and the work package terminates
    reporting `G-3 OPEN — PARTIAL`. No Composition bytes are claimed formable,
    no subject or manifest is claimed formable, and the milestone enters the
    stop-or-re-scope checkpoint in §12.1 before M44-WP6 or M44-WP7 begins.

  Byte-identical derivation by two independent readers is required for closure
  and is unattainable while any coordinate is routed; the two criteria are
  therefore never asserted together. Routing an obligation records it and never
  discharges it (frozen M43-WP3 §7.1: "a conforming subject cannot be formed").
- **Freeze boundary.** Frozen on confirmation. Any later change is a new
  contract version, never an edit (INV-C3).
- **Downstream consumers.** M44-WP6 and M44-WP7, but only in the `CLOSED`
  terminal state; D-1 through D-4.

### M44-WP5 — Annualization Basis Ownership Determination and Requirement Specification

- **Purpose.** Prove the constitutional owner of the annualization basis, and
  determine whether an exact *existing* governed contract kind is already
  present in that owner's frozen corpus. Close G-4 only if one is; otherwise
  record G-4 `OPEN` with the exact missing element and its exact owner.
- **Authority ceiling.** M44-WP5 holds determination and
  requirement-specification authority only. It has **no** authority to author,
  draft, register, extend, version, or serialize a governed dependency contract
  in any domain's corpus, including Portfolio Intelligence's. Frozen M43-WP2
  §8.1 requires an "exact *existing* governed contract type," §8.2(2) requires
  that "every owner and contract kind match the controlling frozen authority,"
  and frozen M43-WP4 §5.2 prohibits any "artificial contract kind, or
  WP4-authored dependency kind." A kind registered by this work package could
  satisfy none of them. Frozen M43-WP4 additionally requires the owner to be
  proved "without expanding Portfolio Intelligence authority," and the owner is
  presumptively not Portfolio Intelligence.
- **Included scope.** The four proofs required by frozen M43-WP4 §6.7 —
  authority class correct, alternative class incorrect, caller override
  rejected, and owner/placement not expanding Portfolio Intelligence authority
  or transferring calendar meaning; an exhaustive, cited search of the
  determined owner's frozen corpus for an exact *existing* governed contract
  kind; where one exists, its identification by exact citation together with
  identifier, immutable version, and canonical value bytes as the owner already
  publishes them; where none exists, a **requirement specification** stating
  precisely what an owner-domain governance instrument must supply, a recorded
  `OPEN` G-4 naming the exact missing element and exact owner, and the
  consequences for D-2b and D-7.
- **Excluded scope.** Authoring, drafting, registering, extending, versioning,
  or serializing any governed dependency contract or contract kind, in any
  domain's corpus, under any condition; admitting any method that consumes the
  dependency; defining annualization arithmetic; originating a calendar;
  selecting a session-count value as a default; expanding any domain's
  authority; treating the requirement specification as an instrument; treating
  a recorded blockage as a closure.
- **Architectural deliverables.**
  `M44_WP5_ANNUALIZATION_BASIS_OWNERSHIP_DETERMINATION_AND_REQUIREMENT_SPECIFICATION.md`.
- **Implementation deliverables.** `NONE`.
- **Dependencies.** M44-WP1; frozen M43-WP2 §8; frozen M43-WP4 §5.2 and §6.7;
  M39/M41 calendar contracts.
- **Predecessor requirements.** M44-WP1 confirmed.
- **Expected repository impact.** One new file in `docs/implementation/`. **No**
  contract-kind registration, in any domain's corpus, under any outcome. No
  file is created outside Portfolio Intelligence's own milestone namespace.
- **Required tests.** Documentary: dependency-closure vectors under frozen
  M43-WP2 §8.2; version non-substitutability vectors; caller-override rejection
  vectors; a negative vector rejecting an unversioned or ambient `252`, `365`,
  or `365.25`; an explicit vector distinguishing a governed version-bound
  derived session count of `252` (permitted once admissible) from an ambient
  `252` (prohibited); and a negative vector rejecting a contract kind, or a
  requirement specification presented as a contract kind, authored by M44.
- **Completion criteria.** The ownership determination is proved with all four
  frozen M43-WP4 §6.7 proofs, and G-4 terminates in exactly one of two states:
  - **G-4 `CLOSED`** — an exact *existing* governed contract kind is identified
    by citation in the determined owner's frozen corpus, with all five required
    fields already published by that owner, and it passes frozen M43-WP2 §8.2
    closure unchanged.
  - **G-4 `OPEN`** — no such existing kind is identified. The requirement
    specification is delivered, the exact missing element and exact owner are
    named, and the gate is reported `OPEN`. This is a valid and honest terminal
    state for the work package, and it is **not** a gate closure (§16.2).

  Ownership is never implicit; no contract kind is authored or registered under
  either outcome; unresolved findings `NONE`.
- **Freeze boundary.** Frozen on confirmation.
- **Downstream consumers.** M44-WP6, which binds the outcome in either state;
  D-2b; D-7; D-3 where an attribution method would require annualization.

### M44-WP6 — Portfolio Analytics Normative Semantics Specification

- **Purpose.** Close G-5's first half by discharging frozen M43-WP4 Components
  A–K as an independently confirmed normative specification.
- **Included scope.** Components A–K exactly as allocated by frozen M43-WP4 §6;
  the explicit no-default matrix of frozen M43-WP4 §7 expanded with exact
  binding and rejection rules; the risk-free-evidence authority-class proof of
  §6.6; the annualization binding taken from M44-WP5's outcome; the canonical
  serialization of Component K embedding or citing M43-WP2/WP3 bytes made
  formable by M44-WP4; documentary numerical vectors; a
  normative-row-to-vector coverage ledger.
- **Component G binding rule.** Where M44-WP5 terminates G-4 `OPEN`, Component G
  binds exactly one value: *annualization unavailable — named missing element
  and named owner*. No annualization-dependent normative row may then claim
  closure, supply a factor, or admit a placeholder, and every such row is
  reported blocked with the same named missing element. Frozen M43-WP4 §6.7
  requires precisely this form of binding.
- **Excluded scope.** Any method formula; any Definition or Method Version
  admission; result classification, sufficiency, outcome, degradation,
  lineage, Provenance carriage, or result serialization, all of which are
  M44-WP7's; module, call-site, library, or provider selection; legacy
  deprecation.
- **Architectural deliverables.**
  `M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`
  at the exact path named by frozen M43-WP6 §3.1 and frozen M43-WP7 §3.1;
  `m44/fixtures/M44_WP6_POSITIVE_DOCUMENTARY_VECTORS.md`;
  `m44/fixtures/M44_WP6_NEGATIVE_DOCUMENTARY_VECTORS.md`.
- **Implementation deliverables.** `NONE`.
- **Dependencies.** M44-WP1, M44-WP4, M44-WP5, all strict.
- **Predecessor requirements.** M44-WP4 and M44-WP5 confirmed and frozen, **and
  G-3 terminated `CLOSED`**. Component K cannot specify a canonical
  serialization that embeds or cites Composition bytes which are not formable.
  If G-3 terminated `OPEN — PARTIAL`, M44-WP6 does not begin; the milestone
  enters the §12.1 stop-or-re-scope checkpoint instead. G-4 terminating `OPEN`
  does **not** block M44-WP6, because a named unavailability is a bindable
  outcome under the Component G binding rule above.
- **Expected repository impact.** One new specification at the M43-named path,
  authored under M44 authority and clearly identifying its authorizing
  milestone; two vector files.
- **Required tests.** Documentary: every one of Components A–K has at least one
  normative row and at least one positive and one negative vector; every row of
  the frozen M43-WP4 §7 no-default matrix has a direct negative vector;
  timezone, market-closure, sparse-history, FX-gap, benchmark-gap, zero
  denominator, negative value, leap-year, rounding-boundary, and
  caller-override rejection vectors; determinism vectors proving identical
  inputs yield identical outputs; a coverage ledger with no uncovered row.
- **Completion criteria.** No method can choose a calendar, currency,
  benchmark, annualization factor, risk-free input, missing-data mode,
  precision, rounding, or operation order implicitly; the risk-free input has
  one confirmed authority class and binding rule; the annualization basis is
  bound to M44-WP5's outcome, including a named-unavailability binding where
  G-4 is `OPEN`; Component K's canonical serialization rests on confirmed
  formable Composition bytes; unresolved findings `NONE`.
- **Freeze boundary.** Frozen on confirmation; D-1 through D-3 bind to it by
  exact path and cited rows.
- **Downstream consumers.** M44-WP7; D-1, D-2, D-3, D-4.

### M44-WP7 — Portfolio Measure Result Normative Contract Specification

- **Purpose.** Close G-5's second half by discharging frozen M43-WP5 as an
  independently confirmed normative result contract.
- **Included scope.** The twelve closures enumerated in frozen M43-WP5 §0:
  result identity; value presence and absence; Portfolio Input Sufficiency;
  Portfolio Computation Outcome; Portfolio Deterministic Calculation; exact
  reuse of Degraded State under the `M34-D-0005` producing-domain grammar;
  deterministic reason-code representation; method and manifest lineage;
  Provenance carriage without recapture; complete Canonical Temporal Claim
  compatibility; canonical result serialization; canonical-byte and hash
  stability.
- **Excluded scope.** Any method-family value semantic; any method admission;
  any runtime response, transport payload, cache value, database entity, or UI
  model; any Provenance recapture; any promotion of `UNAVAILABLE` to an
  outcome.
- **Architectural deliverables.**
  `M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md` at the exact
  path named by frozen M43-WP6 §3.1 and frozen M43-WP7 §3.1;
  `m44/fixtures/M44_WP7_POSITIVE_DOCUMENTARY_VECTORS.md`;
  `m44/fixtures/M44_WP7_NEGATIVE_DOCUMENTARY_VECTORS.md`.
- **Implementation deliverables.** `NONE`.
- **Dependencies.** M44-WP1, M44-WP4, M44-WP6, all strict.
- **Predecessor requirements.** M44-WP4 and M44-WP6 confirmed and frozen, **and
  G-3 terminated `CLOSED`**. Result identity, canonical result serialization,
  and hash stability all resolve through subject and manifest identity, which
  frozen M43-WP3 §7.1 and Manifest §6.3 hold unformable while any Composition
  coordinate reference is unsupplied. If G-3 terminated `OPEN — PARTIAL`,
  M44-WP7 does not begin.
- **Expected repository impact.** One new specification at the M43-named path;
  two vector files.
- **Required tests.** Documentary: no-value-on-failure vectors;
  `UNAVAILABLE`-versus-outcome separation vectors; complete Canonical Temporal
  Claim vectors including Event Type, Producing Domain, authoritative
  timestamp, and Degraded State; explicit partial-result vectors; round-trip
  reconstruction vectors; hash-stability vectors; provenance non-recapture
  vectors; deterministic identity vectors under input permutation; a coverage
  ledger mapping each of the twelve closures to at least one positive and one
  negative vector.
- **Completion criteria.** Identical inputs and Portfolio Method Version yield
  byte-identical Portfolio Measure Results; every unavailable or degraded
  result explains why with a named reason; temporal authority is complete;
  unresolved findings `NONE`.
- **Freeze boundary.** Frozen on confirmation; D-1 through D-3 bind to it by
  exact path and cited rows.
- **Downstream consumers.** D-1, D-2, D-3, D-4.

### 11.1 Dependency graph

```text
M44-WP1
   ├──► M44-WP2 ──► M44-WP3
   ├──► M44-WP4 ──┐
   └──► M44-WP5 ──┤
                  ▼
        §12.1.1 GATE-STATE CHECKPOINT
        (G-3 CLOSED? → proceed; OPEN — PARTIAL → stop or re-scope)
                  │
                  ├──────────┐
                  ▼          │
              M44-WP6        │
                  │          │
                  ▼          │
              M44-WP7 ◄──────┘
```

No cycle exists. M44-WP3 has no downstream M44 consumer; it gates D-1 only.
M44-WP6 and M44-WP7 both consume M44-WP4's Composition bytes, and neither is
reachable except through the checkpoint.

---

## 12. Implementation roadmap

### 12.1 Recommended order

1. M44 Architecture independent review, corrections, confirmation, freeze.
2. M44-WP1.
3. M44-WP2, M44-WP4, and M44-WP5 in parallel.
4. M44-WP3 (after WP2).
5. **Gate-state checkpoint (mandatory).** See §12.1.1.
6. M44-WP6 (after WP4 and WP5, and only if the checkpoint permits).
7. M44-WP7 (after WP4 and WP6).
8. M44 Epic Closeout.

#### 12.1.1 Gate-state checkpoint — stop or re-scope

After M44-WP4 and M44-WP5 are confirmed and before M44-WP6 begins, the
milestone halts and evaluates the terminal state of G-3 and G-4. The checkpoint
has exactly three outcomes and no default.

| Observed state | Outcome | Basis |
| --- | --- | --- |
| G-3 `CLOSED` | **Proceed.** M44-WP6 begins, binding M44-WP5's annualization outcome in whichever state it terminated. G-4 `OPEN` does not stop the milestone, because a named unavailability is a bindable outcome under frozen M43-WP4 §6.7. | frozen M43-WP3 §7.1 satisfied |
| G-3 `OPEN — PARTIAL` | **Stop, or formally re-scope.** M44-WP6 and M44-WP7 do not begin. Either M44 terminates with a documented blockage naming every unsupplied coordinate and its owner, or M44 is re-scoped to a G-3-only milestone through a new architecture revision that is independently reviewed and confirmed before any further work package begins. Re-scoping is never implicit and never performed by a work package. | frozen M43-WP3 §7.1: "a conforming subject cannot be formed"; Manifest §6.3 |
| Either gate's state not established | **Stop.** An unestablished gate state is a review defect in the producing work package and is corrected before the checkpoint is re-evaluated. | INV-B2, INV-F1 |

The checkpoint is a mandatory confirmation point (§12.5). Its outcome is
recorded in the M44-WP1 closure register and carried into the epic closeout. No
work package may declare the checkpoint satisfied on its own authority.

### 12.2 Parallelism

- M44-WP2, M44-WP4, and M44-WP5 may proceed concurrently: different subject
  matter, different owners, no shared normative rows.
- M44-WP3 may proceed concurrently with M44-WP4 and M44-WP5 once M44-WP2 is
  confirmed.
- Review of M44-WP7 may be prepared while M44-WP6 corrections are in flight,
  but M44-WP7 may not be confirmed before M44-WP6 is frozen.

### 12.3 Strict prerequisites

| Work package | Strict prerequisites | Reason |
| --- | --- | --- |
| M44-WP2 | WP1 | Gate disposition must exist before closure |
| M44-WP3 | WP1, WP2 | The corrected artifact's own status must be settled first |
| M44-WP4 | WP1 | Obligation inventory precedes encoding |
| M44-WP5 | WP1 | Gate disposition precedes ownership proof |
| M44-WP6 | WP1, WP4, WP5, **G-3 `CLOSED`**, and the §12.1.1 checkpoint passed | Component K embeds WP3 bytes, which frozen M43-WP3 §7.1 holds unformable while any coordinate reference is unsupplied; §6.7 binding requires the annualization outcome, which may validly be a named unavailability |
| M44-WP7 | WP1, WP4, WP6, **G-3 `CLOSED`** | Result identity, canonical result serialization, and hash stability require formable Composition bytes and WP6 numeric/serialization semantics |

G-4 `OPEN` is not a prerequisite failure for M44-WP6 or M44-WP7; it constrains
their content through the Component G binding rule. G-3 `OPEN — PARTIAL` is a
prerequisite failure for both, without exception.

### 12.4 Review checkpoints

Each work package follows the M43 review pattern: independent constitutional
review → required-corrections response if findings exist → independent
confirmation → freeze. M44-WP4, M44-WP6, and M44-WP7 additionally require an
independent serialization/numerical review distinct from the constitutional
reviewer. Authors of normative rows may not be sole reviewers of their own
expectations; corrections require renewed review; confirmation requires
unresolved findings `NONE`.

### 12.5 Constitutional confirmation points

1. M44 Architecture confirmation (before any work package begins).
2. M44-WP1 confirmation (before any gate closure).
3. M44-WP2 confirmation (before M44-WP3).
4. M44-WP4 and M44-WP5 confirmations (before the checkpoint).
5. **Gate-state checkpoint confirmation** (§12.1.1) — an independent
   confirmation that G-3's and G-4's terminal states are established, that the
   checkpoint outcome follows from them, and that no partial closure is being
   reported as closure. Required before M44-WP6.
6. M44-WP6 confirmation (before M44-WP7).
7. M44-WP7 confirmation (before epic closeout).
8. M44 Epic Closeout confirmation.

Where the checkpoint outcome is *stop* or *re-scope*, points 6 and 7 do not
occur, and the epic closeout records the milestone's terminal gate states
directly.

### 12.6 Repository synchronization points

Repository governance records are synchronized once, at epic closeout, under
separate authorization: the M44 Epic Closeout artifact, one consolidated
Decision Log entry, and the Implementation INDEX milestone row and
current-status paragraph. No work package synchronizes them individually.
`docs/GLOSSARY.md` is synchronized only in the same change as a confirmed
vocabulary admission or rename, if any occurs.

Two recording obligations are carried explicitly and are **not** presumed
discharged by this synchronization:

- **The frozen M43-WP1 §7.4 step 4 recording.** Its named vehicle — the
  consolidated Decision Log entry authorized at M43 epic closeout — has passed.
  Whether an M44 Decision Log entry is an authorized substitute vehicle is a
  governance question that M44 does not decide for itself (§17, OQ-5). Until an
  authorized vehicle is established, M44 records step 4 as outstanding and does
  not claim final G-2 recording. The M43-WP6 block is nonetheless released,
  because the frozen release condition is steps 1–3 (§11 M44-WP3).
- **The filing of this plan's review history.** The independent review, the
  formal constitutional response, and the constitutional adjudication (§1.7)
  are filed in `docs/implementation/` as part of the closeout governance
  records, so that RC2's provenance resolves by repository path.

### 12.7 Final integration sequence

1. Verify every work package that ran is confirmed with unresolved findings
   `NONE`, and that any work package that did not run was withheld by a
   recorded §12.1.1 checkpoint outcome.
2. Verify every gate in the WP1 register carries exactly one terminal state —
   `CLOSED`, `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`, `OPEN`,
   `OPEN — PARTIAL`, or `DEFERRED` with a named successor obligation — and that
   no `OPEN`, `OPEN — PARTIAL`, or blocked state is reported anywhere as a
   closure.
3. Verify every normative row has vector coverage.
4. Verify no frozen M1–M43 artifact changed.
5. Verify no backend, frontend, schema, migration, configuration, or
   operational file changed.
6. Draft the M44 Epic Closeout; obtain independent closeout review and
   confirmation of any corrections.
7. Add the consolidated Decision Log entry and update the Implementation INDEX.
8. Validate repository-relative links and orphan references.
9. Record which gates remain open and which milestone inherits each.

---

## 13. Repository impact map

Forecast only. No change outside this architecture document is made by this
session.

### 13.1 New files

| Path | Produced by |
| --- | --- |
| `docs/implementation/M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | this session |
| `docs/implementation/M44_ARCHITECTURE_INDEPENDENT_REVIEW.md` | review |
| `docs/implementation/M44_ARCHITECTURE_FORMAL_CONSTITUTIONAL_RESPONSE.md` | response to review |
| `docs/implementation/M44_ARCHITECTURE_CONSTITUTIONAL_ADJUDICATION.md` | adjudication |
| `docs/implementation/M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` | confirmation of RC2 |
| `docs/implementation/M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md` | WP1 |
| `docs/implementation/M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md` | WP1 |
| `docs/implementation/M44_WP2_M43_ARCHITECTURE_CONFIRMATION_RECORD.md` | WP2 |
| `docs/implementation/M44_WP3_PERIOD_RETURN_OWNERSHIP_GOVERNANCE_CORRECTION.md` | WP3 |
| `docs/implementation/M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md` | WP4 |
| `docs/implementation/M44_WP5_ANNUALIZATION_BASIS_OWNERSHIP_DETERMINATION_AND_REQUIREMENT_SPECIFICATION.md` | WP5 |
| `docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md` | WP6 |
| `docs/implementation/M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md` | WP7 |
| `docs/implementation/m44/fixtures/` (six vector files, two per WP4/WP6/WP7) | WP4, WP6, WP7 |
| Per-work-package independent review, corrections-response, and confirmation artifacts | review chain |
| `docs/implementation/M44_EPIC_CLOSEOUT.md` | closeout |

The two specification files bearing `M43_WP4_` and `M43_WP5_` prefixes are
authored at the exact paths that frozen M43-WP6 §3.1 and frozen M43-WP7 §3.1
name as their binding sources. Each must state in its header that it is
authorized by M44 and discharges a frozen M43 allocation. Frozen M43-WP7 §3.1
permits an alternate confirmed path; if the reviewer prefers `M44_`-prefixed
filenames, the alternate path must be recorded so downstream citations resolve
(§17, OQ-2).

The WP6 and WP7 files are produced only if the §12.1.1 checkpoint permits those
work packages to begin. If it does not, they are not authored, and the closeout
records G-5 as open with the checkpoint outcome as its cause.

No M44 work package creates a file representing a contract, contract kind, or
registration in a domain other than Portfolio Intelligence. In particular, no
annualization-basis contract file is produced at any path under any outcome
(INV-C4, §11 M44-WP5).

### 13.2 Modified files

| Path | Modification | When |
| --- | --- | --- |
| `docs/engineering/DECISION_LOG.md` | One consolidated M44 entry appended | Epic closeout, separately authorized |
| `docs/implementation/INDEX.md` | M44 milestone row and current-status paragraph | Epic closeout, separately authorized |
| `docs/GLOSSARY.md` | Only if a vocabulary gate confirms an admission or rename | Same change as the confirmation |

### 13.3 Areas with no anticipated change

Packages, modules, services, interfaces, schemas, and migrations: `NONE`.
`backend/`, `frontend/`, `scripts/`, `.github/`, and all configuration:
`NONE`. Executable tests: `NONE`. `docs/architecture/ROADMAP.md`: `NONE` —
no capability-completion mark. `docs/decisions/`: `NONE` — M44 supersedes no
ADR. All frozen M1–M43 artifacts: `NONE`.

### 13.4 Documents described but not modified

`backend/services/portfolio_metrics.py`,
`backend/services/analytics/quant_engine.py`,
`backend/services/analytics/attribution_engine.py`,
`backend/services/timing_performance.py`,
`backend/models/database.py`, and the analytics endpoints and frontend
consumers inventoried by frozen
[M43-WP1 Reconciliation](M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
§§3.1–3.5. They are current-state evidence under constitution G6 and are
neither preserved, adapted, deprecated, nor blessed by M44.

---

## 14. Testing strategy

M44 validation is documentary, non-executable, and fixture-based, consistent
with frozen M43 §12. Every category below is tied to a specific invariant or
risk.

| Category | Form in M44 | Connected risk or invariant |
| --- | --- | --- |
| **Unit** | Per-rule documentary vectors: one normative row, one expected outcome | INV-D2; risk of an unstated rule |
| **Contract** | Five-part boundary gates on every field: subject, inputs, owner, output meaning, prohibited use | INV-O1; risk of ownership leakage |
| **Integration** | Cross-artifact citation resolution: every cited path and section exists and says what the citation claims | INV-B2; risk of a phantom binding source (the exact defect frozen M43-WP7 §3.1 warns about) |
| **Architecture** | Layer and gate conformance review: no Truth creation, no Observation origination, no Experience calculation, no Trust coupling | §5.6; risk of layer bypass |
| **Compatibility** | Tag, field-order, and version-mismatch rejection vectors; frozen-artifact diff check; the PC-NGV-11 through PC-NGV-14 non-triggering proof and the M42-WP7 §9 checklist items 10–12 conformance statements, each with at least one negative vector; an extension-basis check confirming every M44 addition names E-1, E-2, or E-3 and quotes its frozen sentence | INV-C1, INV-C2, INV-C4; risk of silent amendment of M42-WP7; risk of an unstated or misstated authority basis |
| **Migration** | Explicit no-migration assertion plus vectors proving no stored record is reclassified | INV-M1, INV-M2; risk of retroactively canonizing `PortfolioSnapshot` |
| **Negative-path** | One direct negative vector per prohibited default, inference, substitution, and fallback in the frozen no-default matrices | INV-F1, INV-F2; risk that a prohibition is stated but untested |
| **Determinism** | Identical-input/identical-output vectors; permutation-invariance vectors; locale- and clock-independence assertions | INV-D1, INV-D2, INV-Y1; risk of ambient nondeterminism |
| **Concurrency** | Not applicable to documentary contracts; replaced by order-independence vectors proving no rule depends on evaluation sequence | INV-R1, INV-R2 |
| **Provider-boundary** | Paired vectors on both sides of the governance line: rejection vectors for raw provider semantics (provider symbols, raw payloads, provider answers, vendor defaults) as identity, evidence, or input; **admission** vectors proving that exact manifest-bound M39 Observations and M41 Market Measure Results are accepted despite the external origin of the underlying fact; and a laundering-rejection vector proving that Provenance carriage alone never converts raw provider semantics into governed evidence | INV-V1, INV-V2, INV-V3; risk of the historical symbology leak; risk of a rejection rule that would exclude mandatory governed evidence |
| **Regression** | Whole-corpus negative-corpus scan against the twenty-three prohibited statements in frozen [M43-WP1 Reconciliation](M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md) §5, plus the M44 negative corpus | risk that a later artifact reintroduces a rejected claim |
| **Serialization** | Injectivity, round-trip, order-stability, and hash-stability vectors for WP4, WP6 Component K, and WP7 | INV-I1, INV-I2, INV-I3; risk of two byte forms for one value |

No executable test, runner, harness, or runnable fixture is produced. The
future executable milestone's testing obligations remain as enumerated by
frozen M43 §12 and are inherited unchanged by D-4 and D-5.

---

## 15. Risk register

| ID | Risk | Cause | Consequence | Likelihood | Impact | Mitigation | Owning WP | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-1 | The Composition byte contract silently amends M42-WP7 | Encoding decisions imply meaning; a coordinate is reordered or reshaped for convenience | Frozen M42 is broken; every downstream identity is invalid | Medium | Critical | Byte contract preserves tag and field order verbatim; preservation check is a required test; independent serialization reviewer distinct from author | WP4 | Low |
| R-2 | A nested coordinate has no owner-supplied canonical reference, so the Composition cannot be encoded at all | M42 coordinate contracts define meaning, not representation; frozen M42-WP7 §3 assigns six of the ten coordinate classes to Ledger & Accounting and Connectivity & Ingestion, whose cooperation M44 cannot compel | G-3 terminates `OPEN — PARTIAL`; M44-WP6 and WP7 do not begin; the milestone stops or is re-scoped | High | Critical | WP1 produces the obligation pre-inventory before WP4 begins, and it is the deciding evidence for OQ-1; per-coordinate fail-closed routing; the §12.1.1 checkpoint converts partial closure into an explicit stop-or-re-scope decision rather than a silent continuation; partial closure is reported, never faked | WP1, WP4, checkpoint | **High — accepted.** This is the most likely single cause of M44 terminating short of G-5, and the mitigation controls the consequence, not the likelihood |
| R-3 | No exact *existing* governed contract kind for the annualization basis is present in the determined owner's corpus | Frozen M43-WP4 §6.7 already records that "the frozen corpus presently supplies no such annualization contract kind" | G-4 terminates `OPEN`; every annualized method stays blocked; D-2b is deferred behind D-7 | **High** | High | WP5's completion criteria admit `OPEN` as a valid terminal state; the requirement specification tells the owner domain exactly what to supply; D-2 is pre-partitioned into D-2a and D-2b so non-annualized risk work is not held hostage; Component G binds a named unavailability so M44-WP6 still completes | WP5, WP6 | **High — accepted.** The frozen corpus already reports the kind absent, so `OPEN` is the expected outcome, not the exceptional one |
| R-4 | The period-return correction is read as amending Portfolio Calculation Rules | The correction touches accounting-adjacent language | A level-2 Domain Constitution is weakened by a level-4 artifact, violating G2 | Medium | Critical | WP3 restates the confirmed §7.3 split verbatim in substance, asserts no formula authority, and carries an explicit non-amendment clause tested by negative corpus | WP3 | Low |
| R-5 | M44 grows into runtime implementation | Pressure to show visible capability after two consecutive documentary milestones | Constitutional authority expands without review; the exact failure M43 §16 anticipated | Medium | Critical | All runtime authority declared `NONE` in every artifact; §13.3 forbids any non-`docs/` path; closeout verifies `git diff` contains no source path | all | Low |
| R-6 | The two normative specifications are authored under M43 filenames and later read as M43-authorized | Frozen M43-WP6/WP7 name those exact paths as binding sources | Authority provenance becomes ambiguous; a reader infers M43 granted authority it withheld | High | Medium | Each file states its authorizing milestone in its header and cites this plan; alternate-path option recorded per frozen M43-WP7 §3.1 | WP6, WP7 | Low — see OQ-2 |
| R-7 | The M43-WP9 allocation is orphaned | M43 closed with eight of nine allocated work packages | Runtime realization has no owning milestone; D-4 never begins | High | High | Recorded as D-4 in §4.5 as a successor obligation with a stated prerequisite and no milestone number, following the frozen M43 convention; WP1 register names it deferred-with-owner-unassigned | WP1 | Medium — see OQ-4 |
| R-8 | Vector corpora reverse-author missing rules | Expected values are easier to write than normative rows | Fixtures become de facto semantics, exactly as frozen M43-WP7 §11.3 forbids | Medium | High | Vectors derive from confirmed rows only; artificial material marked `ARTIFICIAL`, `NON-EFFECTIVE`, `NON-CONFORMANCE-ESTABLISHING`; coverage ledger runs row→vector, never vector→row | WP4, WP6, WP7 | Low |
| R-9 | Review load encourages merging WP6 and WP7 | Both are large and adjacent | A single oversized artifact mixing semantics and result authority; loss of independent reviewability | Medium | Medium | Separate freeze boundaries and separate confirmation points; §12.3 makes WP7 strictly downstream of WP6 | WP6, WP7 | Low |
| R-10 | Terminology drift between M44 and frozen M43 vocabulary | New authors restate rather than cite | V1 violation; a private dialect forms | Medium | High | §9.7 vocabulary policy; WP1 vocabulary-sufficiency finding; collision scan is a required WP1 test | WP1, all | Low |
| R-11 | The correction record is treated as authorization to begin D-1 immediately | Closing G-2 is visible progress | M43-WP6 normative work starts before WP6/WP7 specifications exist, violating frozen M43-WP6 §3.2 | Medium | High | WP3 states D-1's full precondition set, which includes the confirmed M44-WP6 and M44-WP7 specifications | WP3 | Low |
| R-12 | Sequencing deadlock between WP5 and WP6 | WP6 needs the annualization binding; WP5 will often terminate G-4 `OPEN` | WP6 cannot complete | Low | High | WP5's `OPEN` outcome is a valid, bindable input: under the Component G binding rule WP6 binds "annualization unavailable — named missing element and named owner," exactly as frozen M43-WP4 §6.7 requires | WP5, WP6 | Low |
| R-13 | Decision Log or INDEX is synchronized per work package rather than at closeout | Habit from smaller changes | Repository governance records diverge from confirmed state mid-milestone | Low | Medium | §12.6 makes synchronization a single closeout act under separate authorization | closeout | Low |
| R-14 | A recorded blockage or an `OPEN` gate is reported as a closure | Closure reads as progress; a milestone that "closes five gates" is a more satisfying record than one that closes two and documents three | The milestone's own gate register contradicts its summary; a successor inherits an obligation it believes discharged — the precise defect G-1 embodies | Medium | Critical | §16.2 forbids blockage-as-closure; §2.1, §12.7 step 2, and §19 state the terminal-state vocabulary explicitly; the §12.1.1 checkpoint is independently confirmed; the closeout enumerates terminal states per gate | all, checkpoint, closeout | Low |
| R-15 | The M44-WP4 authority basis is restated as "declared silence" by a later author | The G3 framing is shorter and was used in RC1 | The Finding 1 defect returns; the byte contract's basis is weaker and less accurate than the frozen text supports, inviting a well-founded challenge | Medium | High | §5.3 fixes three named extension bases and requires each artifact to name the one it uses and quote the frozen sentence; INV-C2 makes this falsifiable; the §14 compatibility check tests it | WP4, all | Low |

---

## 16. Completion criteria

### 16.1 M44 Architecture complete

Independent constitutional architecture review performed; all required
corrections applied and independently confirmed; a repository-local
`M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` exists; unresolved findings
`NONE`; the in-file status line matches the confirmed state.

### 16.2 Each work package complete

Every deliverable in §11 exists at its declared path; every normative row has
vector coverage; the independent review chain is complete; unresolved findings
`NONE`; all authority declarations remain as this plan granted; no frozen
artifact changed.

Each allocated gate carries exactly one terminal state, drawn from this closed
vocabulary and from no other:

| Terminal state | Meaning | Counts as closure |
| --- | --- | --- |
| `CLOSED` | The obligation is fully discharged; every element the frozen authority requires is present | Yes |
| `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE` | The frozen release condition is discharged; a separate recording obligation remains outstanding with its vehicle named | No |
| `OPEN` | The obligation is not discharged; the exact missing element and its exact owner are named | No |
| `OPEN — PARTIAL` | Some constituents are discharged and at least one is not; the frozen authority admits no partial form | No |
| `DEFERRED` | Allocated to a named successor obligation with a stated prerequisite | No |

A work package **completes** when it delivers its artifacts and records the
correct terminal state, including a non-closure state. A recorded blockage,
an `OPEN` gate, or an `OPEN — PARTIAL` gate is an honest and valid completion
of a work package and is **never** a gate closure. No artifact may report a
gate as closed on the strength of a recorded blockage, a routing, a
requirement specification, or a successor obligation.

### 16.3 Implementation complete

Not applicable. M44 authorizes no implementation. The correct terminal
statement for M44 is: *no implementation was performed, and none was
authorized.*

### 16.4 Independent review approved

Every M44 artifact has an independent review by a reviewer who did not author
the rows under review; WP4, WP6, and WP7 additionally have an independent
serialization/numerical review; every correction cycle is re-reviewed.

### 16.5 Constitutional confirmation approved

Each applicable confirmation point in §12.5 is recorded `CONFIRMED` with
unresolved findings `NONE`, including the §12.1.1 gate-state checkpoint. Where
the checkpoint outcome withheld M44-WP6 and M44-WP7, their confirmation points
are recorded `NOT REACHED — WITHHELD BY CHECKPOINT`, with the checkpoint
outcome cited.

### 16.6 Decision Log synchronized

One consolidated M44 entry recording the milestone decision, the terminal state
of each gate in the §16.2 vocabulary, the period-return ownership correction as
a ratified architectural decision together with the outstanding step 4
recording obligation, the annualization ownership determination outcome and the
requirement specification it produced, and the explicit statement that no
runtime, implementation, or production authority was granted and that no
contract kind was registered in any domain's corpus.

### 16.7 Implementation INDEX synchronized

The M44 milestone row, the current-milestone-status paragraph, and the closeout
navigation entry are added; classification codes are assigned; no other row is
altered.

### 16.8 Repository documentation synchronized

`docs/GLOSSARY.md` reflects any confirmed admission or rename, or is
unchanged if none occurred. `docs/architecture/ROADMAP.md` is unchanged.
All repository-relative links resolve; no orphan reference exists.

### 16.9 M44 Epic Closeout complete

The closeout artifact records: exact artifacts produced; the terminal state of
every gate in the §16.2 vocabulary, with `OPEN`, `OPEN — PARTIAL`, and
`RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE` states reported as
such and never as closures; the §12.1.1 checkpoint outcome; exact remaining
open obligations and the successor obligation that inherits each, without
assigning a milestone number; the filing of this plan's review, response, and
adjudication artifacts (§12.6); the confirmation that frozen M1–M43 artifacts
are unchanged; the confirmation that runtime, implementation, executable, and
production authority remain `NONE`; the confirmation that no contract kind was
registered in any domain's corpus; and the confirmation that no `ROADMAP.md`
capability was declared complete.

### 16.10 Main branch clean

`git diff --check` clean; the working tree contains no unintended change; no
file outside `docs/` is modified; the branch merges to `main` with the full
M44 corpus and no partial work package.

---

## 17. Open questions and decisions

Only items that cannot be resolved from canonical repository evidence appear
here.

### OQ-1 — Can every nested Portfolio Composition coordinate be canonically referenced?

- **Why it matters.** M44-WP4 can only encode the Composition if each of the
  ten frozen M42-WP7 fields has an owner-supplied exact immutable canonical
  reference. Frozen
  [M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md)
  §7.1 states that where an owning contract cannot supply one, "a conforming
  subject cannot be formed" and WP3 "does not cure the gap." Frozen M42-WP7 §3
  allocates six of the ten coordinate classes outside Portfolio Intelligence —
  Portfolio Identity, Accounting Scope, Portfolio Membership, and Portfolio
  Base Currency to Ledger & Accounting, and Provenance meaning and capture to
  Connectivity & Ingestion — so the answer is substantially not M44's to
  determine. If any coordinate lacks a reference, G-3 terminates
  `OPEN — PARTIAL` and M44-WP6 and WP7 do not begin.
- **Alternatives.** (a) WP4 encodes only the coordinates whose owners supply
  references, fails closed on the rest, and the milestone continues.
  (b) WP4 is expanded to solicit canonical references from each owning domain
  as additive per-coordinate records — which would require authority in those
  domains that M44 does not hold (INV-C4). (c) WP4 delivers the container
  framing and the per-coordinate inventory, reports `OPEN — PARTIAL`, and the
  milestone stops or is formally re-scoped at the §12.1.1 checkpoint.
- **Recommended answer.** **(c), conditionally.** If the WP1 pre-inventory
  establishes that every required coordinate reference is available, G-3 closes
  and the milestone proceeds on its planned path. If any is unavailable, (c) is
  mandatory and (a) is unavailable: frozen M43-WP3 §7.1 admits no partial
  subject, so continuing past a partial G-3 would build WP6's Component K and
  WP7's result identity on bytes that cannot be formed. (b) is
  constitutionally unavailable to M44 in any case. Partial closure is reported
  honestly, is never cured by invention, and is never continued past.
- **Decision deadline.** Before M44-WP4 begins for the scoping question; at the
  §12.1.1 checkpoint for the stop-or-re-scope decision. The WP1 pre-inventory
  is the deciding evidence for both.
- **Affected work packages.** WP1, WP4, the checkpoint, WP6, WP7.

### OQ-2 — Should the two normative specifications use the M43-named paths or M44-prefixed paths?

- **Why it matters.** Frozen M43-WP6 §3.1 and M43-WP7 §3.1 name the exact
  `M43_WP4_...` and `M43_WP5_...` paths as their binding sources, and permit an
  alternate path only if the specification "is independently confirmed under a
  different path," in which case downstream work "must cite that exact
  confirmed path." Choosing wrongly either creates authority ambiguity
  (M43-named files authored under M44 authority) or forces every downstream
  citation to be rewritten.
- **Alternatives.** (a) Use the M43-named paths, with an explicit
  authorizing-milestone header. (b) Use `M44_WP6_...` / `M44_WP7_...` and
  record the alternate confirmed paths in the WP1 register and the closeout.
- **Recommended answer.** (a). It satisfies the frozen binding sources without
  requiring any downstream artifact to resolve an alternate path, and the
  authority-provenance risk is fully mitigated by a mandatory header
  declaration (R-6).
- **Decision deadline.** M44 Architecture confirmation.
- **Affected work packages.** WP6, WP7.

### OQ-3 — Who owns the annualization basis?

- **Why it matters.** Frozen M43-WP4 §6.7 requires proof of an owner whose
  placement does not expand Portfolio Intelligence authority and does not
  transfer source calendar meaning out of Market Intelligence, plus an exact
  *existing* governed contract kind. Whether such a kind exists is not
  resolvable from the frozen corpus, which states only that none is presently
  supplied.
- **Alternatives.** (a) Market Intelligence, if and only if an exact *existing*
  governed contract kind is already present in its frozen corpus. (b) Market
  Intelligence as the proved owner, with **no** existing kind present — the
  owner is determined, G-4 remains `OPEN`, and the instrument is D-7. (c) No
  admissible owner; G-4 `OPEN` with the ownership question itself unresolved.
- **Recommended answer.** Test Market Intelligence ownership first — the
  annualization basis is derived from session-calendar facts that Platform
  Architecture §6.2 already allocates to Market Intelligence — and expect
  **(b)**, because frozen M43-WP4 §6.7 already records that "the frozen corpus
  presently supplies no such annualization contract kind." Ownership is an M44
  determination; the instrument is not. Whichever alternative holds, M44
  authors no contract and registers no kind: under (a) it cites what already
  exists; under (b) and (c) it records `OPEN` and specifies what is required.
  This is an architectural deduction, not a repository-confirmed fact, and
  M44-WP5 must prove or reject it.
- **Decision deadline.** M44-WP5 confirmation, before M44-WP6 binds Component
  G.
- **Affected work packages.** WP5, WP6; downstream D-2b and D-7.

### OQ-4 — Which successor obligation inherits the frozen M43-WP9 allocation?

- **Why it matters.** Frozen [M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
  §9 allocates nine work packages, the last being "M43-WP9 — Runtime
  Realization, Compatibility, and Cutover Design," and frozen M43-WP6, WP7, and
  WP8 all defer runtime placement to it. No WP9 artifact exists, and the M43
  Epic Closeout declares M43 complete with WP1–WP8. The allocation is live in
  frozen text but has no owning milestone.
- **Alternatives.** (a) Record it as the D-4 successor obligation with a stated
  prerequisite and no milestone number. (b) Absorb it into M44.
  (c) Declare the allocation discharged by M43's closeout.
- **Recommended answer.** (a), as recorded in §4.5. (b) would mix
  implementation-design authority into a governance and semantics milestone and
  violate §4.4. (c) has no repository support: the closeout closed no gate and
  discharged no allocation, and frozen WP6–WP8 still cite WP9 as a live future
  authority. Assigning a milestone number to (a) is separately unavailable:
  M44 holds no future-milestone allocation authority, and the frozen M43
  Architecture defers work by obligation and prerequisite — "a **later
  milestone** can implement the system" — and never by forward milestone
  number.
- **Decision deadline.** M44-WP1 confirmation, so the register records the
  allocation as deferred-with-owner-unassigned rather than silently dropped.
- **Affected work packages.** WP1; downstream D-4.

### OQ-5 — Which vehicle validly discharges the frozen step 4 recording obligation?

- **What is settled, and not in question.** Release of the standing M43-WP6
  block is **not** at issue. Frozen M43-WP1 §7.4 states the release condition
  exactly — *"Until steps 1–3 are complete, WP6 may not begin"* — and step 4
  is not part of it. M44-WP3, once independently confirmed, performs step 3 and
  discharges the release condition regardless of how this question is answered.
  This question concerns the recording obligation alone.
- **Why it matters.** Frozen M43-WP1 §7.4 step 4 says "the final resolution is
  recorded in the consolidated Decision Log entry authorized at M43 epic
  closeout by frozen M43 §§13 and 17." That closeout has occurred and did not
  record it. Whether an M44 Decision Log entry is an authorized substitute for
  a lapsed named vehicle is a governance judgement, not a repository fact, and
  M44 does not decide it for itself.
- **Alternatives.** (a) The M44 consolidated Decision Log entry is accepted as
  the substitute vehicle, since the step's substance is "recorded in the
  Decision Log" and its named vehicle is no longer available. (b) A separately
  authorized governance instrument establishes the substitute vehicle before
  any recording is claimed. (c) A standalone ADR in `docs/decisions/`
  supersedes the M43 §8 row.
- **Recommended answer.** (a) as the substantively correct reading, but M44
  does not self-authorize it. Until the vehicle question is settled by the
  authority that can settle it, G-2 is reported
  `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE` (§16.2), M44-WP3
  claims no step 4 discharge, and the closeout carries the obligation forward
  by name. (c) adds an immutable level-3 ruling for what is a level-4
  allocation correction, which over-escalates. No alternative blocks D-1: the
  release condition is already discharged.
- **Decision deadline.** M44 epic closeout, for the recording. Not a
  precondition of M44-WP3 confirmation or of D-1's entry.
- **Affected work packages.** WP3; closeout.

---

## 18. Validation performed on this plan

Re-run in full on RC2. Rows whose evidence changed under the adjudication are
marked **(RC2)**.

| Check | Result | Evidence |
| --- | --- | --- |
| Contradiction with canonical decisions | `NONE FOUND` | Every ownership row traces to Platform Architecture §6, frozen M34/M42/M43 allocations, or an explicitly labelled M44 determination to be proved |
| Duplicated authority | `NONE FOUND` | §5.1 and §8 assign exactly one owner and one responsibility per component; §11 assigns each gate to exactly one work package |
| Authority asserted without a frozen basis **(RC2)** | `NONE FOUND` | §5.3 fixes three named extension bases; every extension names the one it uses and quotes the frozen sentence (INV-C2); M44-WP4 rests on E-1/E-2, not on declared silence |
| Cross-domain authority expansion **(RC2)** | `NONE FOUND` | INV-C4; §5.1 closing statement; §8.4 and §11 M44-WP5 withdraw all contract-authoring and registration authority; §9.2 records the annualization contract as not produced by M44; §13.1 forbids any file representing a registration in another domain |
| Closure claimed without discharge **(RC2)** | `NONE FOUND` | §16.2 fixes a closed terminal-state vocabulary in which blockage, `OPEN`, `OPEN — PARTIAL`, and `DEFERRED` are non-closures; §11 M44-WP4 and M44-WP5 each state two mutually exclusive terminal states; §12.1.1 makes the partial case a mandatory stop-or-re-scope decision |
| Jointly unsatisfiable completion criteria **(RC2)** | `NONE FOUND` | M44-WP4's byte-identical-derivation criterion and its routing criterion are assigned to different terminal states and are never asserted together |
| Upstream reach by a canonical-byte contract **(RC2)** | `NONE FOUND` | §8.3 requires a named non-triggering proof against PC-NGV-11 through PC-NGV-14 and §9 checklist items 10–12; INV-C4; §14 compatibility row tests it |
| Governed evidence excluded by a boundary rule **(RC2)** | `NONE FOUND` | §10's provider row and INV-V1–V3 separate raw provider semantics from governed evidence and decide admissibility by governance, not origin; §14 requires paired rejection and admission vectors |
| Future-milestone allocation without authority **(RC2)** | `NONE FOUND` | §4.5 records successor obligations and prerequisites only; no milestone number appears anywhere in this plan for any successor, matching the frozen M43 convention |
| Terminology drift | `NONE FOUND` | Canonical repository terms preserved throughout: Portfolio Measure Subject, Portfolio Analytics Input Manifest, Portfolio Measure Result, Portfolio Input Sufficiency, Portfolio Computation Outcome, Degraded State, Canonical Temporal Claim, Portfolio Benchmark Declaration, Analytical Grouping, Constitutional Scope and Implementation Plan |
| Layer bypass | `NONE FOUND` | §5.6 enumerates the layers and gates M44 may not bypass; no component writes Truth, originates an Observation, or assigns calculation to Experience |
| Circular dependencies | `NONE FOUND` | §11.1 graph is acyclic; §12.3 lists strict prerequisites consistent with it |
| Hidden implementation assumptions | `NONE FOUND` | §7.3–7.5 declare runtime, storage, and service dependencies `NONE`; §13.3 forbids non-`docs/` paths |
| Scope leakage | `NONE FOUND` | §4 partitions every named capability exactly once; the deferred set names its blocking prerequisite |
| Missing failure behavior | `NONE FOUND` | §10 covers all twelve required conditions plus three M44-specific ones, all fail-closed |
| Missing closeout obligations | `NONE FOUND` | §16 covers architecture, per-work-package, review, confirmation, Decision Log, INDEX, documentation, epic closeout, and branch cleanliness |
| Work-package ordering defects | `NONE FOUND` | Every strict prerequisite in §12.3 is justified by a cited frozen dependency |
| Incompatibility with repository structure | `NONE FOUND` | Naming and placement follow the M43 convention: milestone artifacts in `docs/implementation/`, fixtures in `docs/implementation/m44/fixtures/` |
| Frozen-artifact modification | `NONE` | No M44 work package writes to any M1–M43 path; §1.6 rule 3 forbids it |
| Roadmap capability claim | `NONE` | §3.3 and §4.2 forbid it, consistent with frozen M43-WP1 Reconciliation §2 |

---

## 19. Final constitutional boundary

M44 is the gate-closure and universal-semantics milestone for Portfolio
Analytics. It addresses the five inherited obligations that frozen M42 and M43
artifacts imposed and that M43's closeout expressly left open, and — where
those obligations are dischargeable by an authority M44 holds — it produces the
two method-family-independent normative specifications on which every blocked
method family depends.

M44 does not promise five closures. It promises five accurate terminal states.
G-3 depends on coordinate canonical references that six of ten coordinate
classes' owners must supply; G-4 depends on an owner-domain governance
instrument that M44 has no authority to author; G-2's release is discharged by
M44 while its final recording awaits an authorized vehicle. Where an obligation
is discharged, M44 records `CLOSED`. Where it is not, M44 records `OPEN`,
`OPEN — PARTIAL`, or `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`,
names the exact missing element and its exact owner, and stops. A recorded
blockage is never reported as a closure (§16.2), and a partial discharge is
never continued past (§12.1.1).

It defines no formula, admits no method, creates no executable artifact,
changes no runtime behavior, modifies no frozen artifact, registers no contract
kind in any domain's corpus, allocates no milestone number to any successor,
and declares no roadmap capability complete. Core performance, risk,
benchmark-relative, and attribution method specifications remain allocated to
their frozen M43 work packages; runtime realization remains allocated to the
frozen M43-WP9 allocation and is deferred as a successor obligation, not
absorbed.

---

## Appendix A — RC2 constitutional change summary

RC2 changes what M44 *claims authority to do* in four places and what M44
*claims to achieve* in three. Nothing else about the milestone's purpose,
decomposition, or scope changed.

**Authority narrowed.**

1. **M44-WP5 loses all contract-authoring and contract-kind registration
   authority** (Finding 2). RC1 held conditional authority to author the
   annualization dependency contract and anticipated "potentially one new
   governed contract-kind registration in the owning domain's corpus." Frozen
   M43-WP2 §8.1 requires an "exact *existing* governed contract type," §8.2(2)
   requires owner and kind to match the controlling frozen authority, and
   frozen M43-WP4 §5.2 prohibits an "artificial contract kind, or WP4-authored
   dependency kind." A registered-for-the-purpose kind satisfies none of them,
   and the owner is presumptively not Portfolio Intelligence. RC1 also
   contradicted itself: §8.4 already prohibited creating a kind that does not
   exist in the owning domain's vocabulary. WP5 now produces an ownership
   determination and a requirement specification; the instrument is D-7, owned
   by the determined domain.
2. **No M44 artifact may reach upstream or into another domain's corpus**
   (Findings 1 and 2), fixed as the new invariant INV-C4.
3. **M44-WP3 loses any claim to discharge frozen M43-WP1 §7.4 step 4**
   (Finding 4). It performs step 3, which discharges the frozen release
   condition; the recording obligation is carried forward outstanding.
4. **The extension power is bounded by three named bases** (Finding 1). §5.3
   replaces the single "addition into declared silence" rationale with E-1
   (express conditional permission), E-2 (a remedy the frozen corpus names but
   does not supply), and E-3 (declared silence, residual). INV-C2 now requires
   every M44 addition to name its basis and quote the frozen sentence.

**Authority re-grounded, not removed.**

5. **M44-WP4 is retained** (Finding 1). Its basis moves from constitution G3
   "declared silence" — which mischaracterized frozen M42-WP7 §5, a section
   that speaks, conditions, and preserves rather than falling silent — to E-1
   plus E-2: the §5 conditional permission ("a representation may claim
   canonical bytes **only if**…"), the preserved obligation ("their exclusion
   does not remove or defer the frozen canonical-byte obligation"), and frozen
   M43-WP3 §7.1's naming of "a separately authorized contract" as the remedy.
   WP4 acts as owner of the Composition noun under frozen M42-WP7 §9 checklist
   item 1, and must now prove non-triggering against PC-NGV-11 through
   PC-NGV-14 and checklist items 10–12, vector by vector.

**Claims corrected.**

6. **Blockage is never closure** (Findings 2 and 3). §16.2 replaces "`CLOSED`
   or explicitly and permanently `BLOCKED`" with a closed five-state terminal
   vocabulary in which only `CLOSED` counts as closure. §2.1, §12.7, and §19
   are conformed.
7. **Partial discharge is never continued past** (Finding 3). G-3 admits
   `CLOSED` or `OPEN — PARTIAL` and nothing between. M44-WP4's two RC1
   completion criteria — byte-identical derivation by two readers, and every
   coordinate "closed **or** explicitly routed" — were jointly unsatisfiable in
   the partial case; they are now assigned to different terminal states. A
   mandatory, independently confirmed stop-or-re-scope checkpoint (§12.1.1)
   sits between M44-WP4/WP5 and M44-WP6.
8. **Admissibility is decided by governance, not origin** (Finding 5). §10's
   "a provider-sourced value reaching an M44 boundary is an invalid input" —
   which on its face would have rejected the M39 and M41 evidence §5.2 and
   INV-V2 make mandatory — is replaced by an explicit split between *raw
   provider semantics* (rejected) and *governed evidence* (admitted), with a
   new INV-V3 closing the Provenance-laundering path.
9. **No successor is allocated a milestone number** (Finding 6). §4.5's
   indicative M45/M46/M47 table, which contradicted its own disclaimer,
   becomes a successor-obligation table with prerequisites, matching the frozen
   M43 Architecture's convention of deferring by obligation and never by
   forward number.

**No new constitutional decision is introduced.** Every change above is either
a withdrawal of authority the adjudication found unavailable, a re-grounding of
authority in frozen text that already supplied it, or a correction of a claim
to match a terminal state the frozen corpus already determines.

---

## Appendix B — Section-by-section revision summary

| Section | Change | Driving finding | Why |
| --- | --- | --- | --- |
| Header, §1.1 | Status to `RC2 — …REQUIRES INDEPENDENT CONSTITUTIONAL CONFIRMATION`; revision line added | all | RC1 is superseded; the artifact must not present as unreviewed |
| §1.4 | M42-WP7 row extended to §5, §8, §9 with the conditional permission and the negative vectors | 1 | The dependency actually consumed is wider than RC1 declared |
| §1.7 (new) | Revision provenance and the six adjudicated dispositions | all | A confirmer must see what was decided and by whom |
| §2.1 | Opening claim conditioned; items 3 and 4 restated | 1, 2, 3 | RC1 promised five closures M44 cannot guarantee, and promised a contract M44 may not author |
| §2.3 | Formability and annualization bullets conditioned | 2, 3 | Both outcomes depend on instruments others must supply |
| §3.1 G-2 | Split into block release (steps 1–3) and final recording (step 4) | 4 | Frozen M43-WP1 §7.4 gates release on steps 1–3; step 4 is a recording obligation |
| §3.1 G-3 | Restated as an unfulfilled *delegated* obligation, with the three frozen operations of M42-WP7 §5 quoted; container-level limit and two-terminal-state rule added | 1, 3 | The RC1 "encoding gap / declared silence" framing misread a section that expressly conditions and preserves |
| §3.1 G-4 | Both frozen grounds that bar M44 from authoring the instrument added; two terminal states fixed | 2 | RC1 stated the gap without stating why M44 cannot fill it |
| §4.1 I-4, I-5, I-6 | Closure columns made conditional | 2, 3 | An included capability cannot promise a closure it may not reach |
| §4.3 | D-2 split into D-2a/D-2b; D-7 added | 2 | Non-annualized risk work must not be blocked by an instrument M44 does not own |
| §4.4 | Non-goals extended to contract authoring, kind registration, and blockage-as-closure | 2 | The prohibition belongs where the milestone states what it will not do |
| §4.5 | Retitled `SUCCESSOR OBLIGATIONS`; M45/M46/M47 removed; obligation-and-prerequisite table substituted | 6 | RC1 allocated and disclaimed allocation in one subsection; frozen M43 never numbers forward |
| §5.1 | Period-return row rebased on step 3 and the frozen release condition; Composition row rebased on the §5 conditional permission and §9 item 1; annualization row reduced to determination and requirement specification; closing statement added | 1, 2, 4 | Owned surfaces must match the authority actually held |
| §5.3 | Rewritten as three named extension bases E-1/E-2/E-3, with WP4 on E-1 and E-2 and declared silence expressly excluded | 1 | The mandated re-grounding |
| §5.4 | PC-NGV-01 through PC-NGV-14 and the §9 checklist added to the non-reinterpretable list | 1 | Non-triggering must be proved, not assumed |
| §6 | INV-C2 rewritten; INV-C4 added; INV-V1/V2 sharpened and INV-V3 added | 1, 2, 5 | Each corrected rule needs a falsifiable invariant |
| §7.1 | M42-WP7 row extended | 1 | Matches §1.4 |
| §7.2 | D-2 split | 2 | Matches §4.3 |
| §7.7 | Restated in governance-based terms | 5 | Aligns the dependency statement with §10 and INV-V1–V3 |
| §7.8 | Annualization row: outcome is `OPEN`, never authorship | 2 | RC1's row still implied a WP5-authored contract was the alternative |
| §8.2 C2 | Authority limited to step 3; step 4 claim prohibited; outputs split | 4 | Release and recording are constitutionally distinct |
| §8.3 C3 | Authority rewritten on E-1/E-2 and §9 item 1; a required PC-NGV-11 through PC-NGV-14 and checklist 10–12 conformance-proof block added; nested encoding added to prohibitions; routing tied to `OPEN — PARTIAL` | 1, 3 | The core of the mandated re-grounding |
| §8.4 C4 | Retitled; contract-authoring and registration authority removed; requirement specification substituted; prohibitions extended | 2 | The core of the Finding 2 correction |
| §9.2 | Annualization contract row removed; replaced by an explicit not-produced-by-M44 statement | 2 | A new-contracts table must not list a contract M44 may not author |
| §9.3 | M42-WP7 row rebased on E-1/E-2 with PC-NGV conformance; `PMS1`/`PAIM1` row conditioned on complete closure; M43-WP2 row changed to **no extension** | 1, 2, 3 | RC1 claimed M44 supplies "an owning contract kind" — precisely the authority withdrawn |
| §10 | Provider row rewritten on the raw-semantics / governed-evidence split; nested-coordinate row tied to `OPEN — PARTIAL`; ownership-proof row restated; a required-instrument-absent row added | 2, 3, 5 | Boundary behavior must match the governing rules in §6 and §7.7 |
| §11 M44-WP3 | Purpose, a two-component explanation, scope, and completion criteria separated into release and recording | 4 | RC1 read as performing "steps 3–4" and closing G-2 outright |
| §11 M44-WP4 | Purpose, authority basis, scope, tests, and completion criteria rewritten; two mutually exclusive terminal states | 1, 3 | Removes the jointly unsatisfiable criteria and adds the conformance proof |
| §11 M44-WP5 | Retitled; authority ceiling added; scope reduced to determination plus requirement specification; deliverable renamed; repository impact states no registration; two terminal states | 2 | The Finding 2 correction at work-package level |
| §11 M44-WP6 | Component G binding rule added; predecessor requirements now demand G-3 `CLOSED`; completion criteria conformed | 2, 3 | Component K cannot serialize bytes that are not formable |
| §11 M44-WP7 | Predecessor requirements demand G-3 `CLOSED` | 3 | Result identity resolves through subject and manifest identity |
| §12.1, §12.1.1 (new) | Mandatory gate-state checkpoint with three outcomes and no default | 3 | The mandated stop-or-re-scope checkpoint |
| §12.3 | WP6 and WP7 prerequisites now include G-3 `CLOSED` and the checkpoint; G-4 `OPEN` distinguished as non-blocking | 2, 3 | Prerequisites must reflect what is actually required |
| §12.5 | Checkpoint added as a confirmation point; withheld points defined | 3 | The checkpoint must be independently confirmed, not self-declared |
| §12.6 | Step 4 recording and review-history filing carried as explicit outstanding obligations | 4 | Prevents silent presumption of discharge |
| §12.7 | Steps 1–2 rewritten around the terminal-state vocabulary | 2, 3 | Integration must verify honest states, not just closures |
| §13.1 | Review-history artifacts added; WP5 deliverable renamed; WP6/WP7 files made conditional; no-foreign-registration statement added | 2, 3 | The file forecast must match the corrected authority |
| §14 | Compatibility row extended with the PC-NGV proof and extension-basis check; provider-boundary row extended with admission and laundering-rejection vectors | 1, 5 | Every corrected rule acquires a test |
| §15 | R-2 and R-3 recalibrated to `High — accepted`; R-7 and R-12 conformed; R-14 and R-15 added | 1, 2, 3, 6 | RC1 understated the likelihood of the outcomes the adjudication makes explicit |
| §16.2 | Five-state terminal vocabulary replacing blockage-as-closure | 2, 3 | The mandated correction |
| §16.5, §16.6, §16.9 | Conformed to the checkpoint and the terminal-state vocabulary | 2, 3, 4 | Closeout records must not overstate |
| §17 OQ-1 | Recommended answer moved from (a) to conditional (c); frozen M42-WP7 §3 owner allocation added | 3 | RC1 recommended continuing past a partial G-3 |
| §17 OQ-3 | Alternatives restated so no branch produces an M44-authored contract; expected outcome stated | 2 | RC1's alternatives all implied M44 authorship |
| §17 OQ-4 | Retitled to successor obligation; numbering expressly unavailable | 6 | Matches §4.5 |
| §17 OQ-5 | Narrowed to the recording vehicle; release expressly settled and removed from the question | 4 | RC1 framed step 4 as potentially gating, which invited the finding |
| §18 | Re-run; eight RC2 checks added; failure-condition count corrected | all | A confirmer needs the validation re-performed against RC2 |
| §19 | Terminal-state promise replaces the five-closure claim | 2, 3 | The final boundary must match §16.2 |

**Unchanged sections.** §1.2, §1.3, §1.5, §1.6, §2.2, §2.4, §3.2, §3.3, §3.4,
§4.2, §5.2, §5.5, §5.6, §7.3–§7.6, §7.9, §8.1, §8.5, §8.6, §8.7, §9.1,
§9.4–§9.7, §11 M44-WP1, §11 M44-WP2, §11.1, §12.2, §12.4, §13.2–§13.4, §16.1,
§16.3, §16.4, §16.7, §16.8, §16.10, §17 OQ-2. No finding reached them, and
minimizing textual change was a revision constraint.
