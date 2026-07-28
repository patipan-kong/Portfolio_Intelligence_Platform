# M43-WP1 — Portfolio Analytics Vocabulary and Ownership Register

**Milestone:** M43 — Portfolio Analytics Contract Foundation
**Work package:** M43-WP1 only
**Artifact class:** Constitutional vocabulary and ownership specification
**Status:** `CORRECTED AFTER INDEPENDENT REVIEW — REQUIRES INDEPENDENT CONFIRMATION`
**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/API/UI authority:** `NONE`
**Implementation authority:** `NONE`
**Provider authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`

## 1. Purpose and normative boundary

This register establishes only the cross-work-package Portfolio Analytics
vocabulary, single-owner allocations, admission boundaries, glossary
synchronization package, validation rules, and completion criteria required by
the frozen
[M43 Architecture and Implementation Plan](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§9, WP1.

It does not specify any WP2 contract field, identifier syntax, schema,
serialization format, formula, applicability rule, method catalog, result
shape, state enumeration, fixture, runtime component, or production method.
Those subjects remain outside WP1.

All proposed `ADMIT` dispositions are non-effective until this register
receives independent constitutional confirmation. Until then their ownership
status is exactly `Candidate — Owner to Prove`, downstream reliance is
prohibited, and `docs/GLOSSARY.md` must not be changed.

The commissioning authority records the governing M43 Architecture as
`COMPLETE AND FROZEN` after Independent Constitutional Confirmation
`APPROVED`. That confirmation is the prerequisite under frozen M43 §11 for
starting WP1. The repository-local M43 plan header has not yet been
synchronized to that confirmed state. Because the present correction is
authorized to modify WP1 artifacts only, this register records the governing
confirmation but does not alter the frozen M43 artifact. Before WP1
confirmation is recorded, a separately authorized governance change must
synchronize the plan’s status line or provide its repository-local
confirmation artifact; WP1 cannot self-authorize that external edit.

## 2. Constitutional admission procedure

Every candidate receives exactly one of:

| Disposition | Meaning in WP1 |
| --- | --- |
| `ADMIT` | A distinct Portfolio Intelligence noun is constitutionally necessary and has passed WP1’s candidate-level ownership gate, subject to independent confirmation |
| `REUSE` | An existing frozen term is sufficient at its existing meaning and owner; no new noun or ownership is created |
| `RENAME` | The candidate meaning is admissible only under the stated collision-free canonical name |
| `REJECT` | The candidate must not enter the canonical vocabulary; any permitted meaning is routed to an existing term or excluded |

Each `ADMIT` candidate must pass all five boundary questions:

1. **Permitted subject:** exactly one M42 Portfolio Composition representing
   one Portfolio Identity and its corresponding Accounting Scope.
2. **Permitted inputs:** only exact Ledger-derived evidence, M39/M41 market
   evidence, Asset Foundation references, explicit invocation parameters,
   explicit governed calculation dependencies, and already-captured
   Provenance. Explicit invocation parameters may select only choices that a
   confirmed method contract classifies as invocation-bound. They may not
   supply or override the Portfolio Benchmark Declaration, risk-free input,
   annualization basis, calendar authority, or any other governed evidence or
   calculation dependency.
3. **Output meaning:** immutable Portfolio-derived descriptive knowledge,
   never truth, judgment, evaluation, authorization, or action.
4. **Owner:** exactly one constitutional domain.
5. **Prohibited semantics:** no cross-portfolio, Wealth, recommendation,
   ranking, optimization, forecast, causal/evaluator, provider, runtime,
   persistence, API, UI, or production-method meaning.

Shared ownership is not a valid result. Custody, invocation, storage,
transport, rendering, execution, and evaluation do not create semantic
ownership.

## 3. Candidate vocabulary register

This is the complete cross-WP noun set frozen into M43-WP1. WP1 introduces no
additional canonical Portfolio Analytics noun.

| ID | Candidate term | Disposition | Proposed or existing owner | Ownership classification now | Constitutional result |
| --- | --- | --- | --- | --- | --- |
| `PA-V01` | Portfolio Measure | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Distinct Portfolio-derived measure umbrella reserved to Portfolio Intelligence by M40-WP1 §8.3 and Platform Architecture §6.5 |
| `PA-V02` | Portfolio Measure Definition | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Portfolio-scoped semantic definition; cannot reuse Market Intelligence’s Market Measure Definition |
| `PA-V03` | Portfolio Method Version | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Portfolio-scoped immutable non-production method identity; avoids collision with M41 Method Version |
| `PA-V04` | Portfolio Measure Subject | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Binds exactly one M42 Portfolio Composition as the subject of one Portfolio measure |
| `PA-V05` | Portfolio Analytics Input Manifest | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Closed Portfolio evidence binding; cannot reuse Observation Input Manifest |
| `PA-V06` | Portfolio Measurement Window | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Portfolio calculation input-selection boundary; cannot reuse Market Intelligence’s Measurement Window |
| `PA-V07` | Portfolio Input Sufficiency | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Portfolio calculation prerequisite classification; cannot reuse Market Intelligence’s Input Sufficiency |
| `PA-V08` | Portfolio Measure Result | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Immutable Portfolio-derived result; cannot reuse Market Measure Result |
| `PA-V09` | Portfolio Computation Outcome | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Portfolio calculation completion axis; cannot reuse Market Intelligence’s Computation Outcome |
| `PA-V10` | Portfolio Deterministic Calculation | `ADMIT` | Portfolio Intelligence | Candidate — Owner to Prove | Portfolio-result reproducibility property; cannot reuse Market Intelligence’s Deterministic Calculation |
| `PA-V11` | Portfolio Degraded State | `REUSE` | Producing domain for the exact claim | Frozen (with governing authority) | Use the existing M34-D-0005 `Degraded State`; the Portfolio-prefixed spelling is not admitted |

No `RENAME` disposition is required by this candidate set. The absence of a
rename is a result, not an omitted classification.

“Portfolio Analytics” is the architecture’s scope label for this milestone,
not a separately admitted business object. “Portfolio Analytics contract,”
“ownership gate,” “glossary synchronization package,” “validation rule,” and
similar document-control phrases are ordinary specification language, not
additional canonical nouns.

## 4. Exact candidate meanings and constitutional justifications

### 4.1 `PA-V01` — Portfolio Measure — `ADMIT`

**Exact candidate meaning:** A Portfolio Measure is an immutable descriptive
knowledge claim derived about exactly one M42 Portfolio Composition under one
explicit Portfolio Method Version from a closed Portfolio Analytics Input
Manifest.

**Owner:** Portfolio Intelligence.

**Justification:** Platform Architecture §6.5 assigns canonical Portfolio
derived measures and the meaning of performance to Portfolio Intelligence.
M40-WP1 §8.3 expressly reserves `portfolio measure`, portfolio performance,
attribution, exposure, and portfolio risk to Portfolio Intelligence. Market
Measure cannot be reused because it excludes Portfolio subjects.

**Exclusions:** No accounting truth, recommendation, comparison choice,
evaluator verdict, cross-portfolio result, method formula, runtime, or
production availability is implied.

**Five-part gate:** `PASS` at candidate level.

### 4.2 `PA-V02` — Portfolio Measure Definition — `ADMIT`

**Exact candidate meaning:** A Portfolio Measure Definition is the immutable
semantic identity and revision of one kind of Portfolio Measure, stating what
the measure means independently of any particular calculation method,
invocation, or result.

**Owner:** Portfolio Intelligence.

**Justification:** The M41 Market Measure Definition pattern is useful but its
subject and owner are Market Intelligence. Reusing that type would reinterpret
a Market Intelligence contract to accept a Portfolio, which frozen M43 §6
forbids. Asset Definition and Definition Version concern Asset Foundation
identity and capability, not Portfolio-derived knowledge.

**Exclusions:** WP1 admits no identifier format, definition fields,
applicability vocabulary, output coordinates, formula, concrete definition,
or production catalog entry.

**Five-part gate:** `PASS` at candidate level.

### 4.3 `PA-V03` — Portfolio Method Version — `ADMIT`

**Exact candidate meaning:** A Portfolio Method Version is one immutable,
version-identified, non-production calculation specification bound to exactly
one Portfolio Measure Definition and to explicit calculation dependencies.

**Owner:** Portfolio Intelligence.

**Justification:** M41 Method Version is governed inside the Market
Intelligence Market Measure contract family. A Portfolio-prefixed noun is
required to prevent cross-domain type reuse and to make the Portfolio owner
explicit. “Portfolio Method Version” is also distinct from Asset Definition
Version and from an implementation/library version.

**Exclusions:** No formula, version syntax, dependency schema, registry,
executable method, implementation, or production admission is created.

**Five-part gate:** `PASS` at candidate level.

### 4.4 `PA-V04` — Portfolio Measure Subject — `ADMIT`

**Exact candidate meaning:** A Portfolio Measure Subject is the exact,
identity-bound reference to one M42 Portfolio Composition about which one
Portfolio Measure is derived.

**Owner:** Portfolio Intelligence.

**Justification:** The subject is a Portfolio Intelligence calculation
coordinate, while every component cited by the Composition retains its frozen
owner. M41 Measure Subject excludes Portfolio subjects and cannot be reused.

**Exclusions:** No Current Selection, Workspace default, person, household,
cross-portfolio aggregate, raw ORM Portfolio, inferred coordinate, or
composition mutation is permitted.

**Five-part gate:** `PASS` at candidate level.

### 4.5 `PA-V05` — Portfolio Analytics Input Manifest — `ADMIT`

**Exact candidate meaning:** A Portfolio Analytics Input Manifest is the
immutable, complete, closed, and deterministically orderable binding of every
exact governed input supplied to one Portfolio calculation.

**Owner:** Portfolio Intelligence.

**Justification:** Observation Input Manifest is Market Intelligence-owned and
binds frozen M39 Observations for a Market calculation. M43’s manifest must
also bind the exact Portfolio subject, Ledger-derived evidence, Market
evidence, Asset Foundation references, explicit invocation parameters,
governed calculation dependencies, and already-captured Provenance without
re-owning any of them. Its different subject and input closure require a
separate Portfolio noun.

**Exclusions:** No live lookup, provider request, dynamic `latest`, ORM query,
Current Selection, retrieval permission, inferred input, or manifest schema is
admitted.

**Five-part gate:** `PASS` at candidate level.

### 4.6 `PA-V06` — Portfolio Measurement Window — `ADMIT`

**Exact candidate meaning:** A Portfolio Measurement Window is the explicit
Portfolio-calculation input-selection boundary over which a Portfolio Measure
is derived.

**Owner:** Portfolio Intelligence.

**Justification:** M41 Measurement Window is owned inside Market
Intelligence’s contract family. Portfolio measurement has a different subject
and must remain independently governed. The noun does not replace the
M34-D-0005 Canonical Temporal Claim; a selection boundary and an authoritative
event timestamp answer different questions.

**Exclusions:** No boundary inclusivity, timezone, calendar, as-of rule,
partial-window behavior, current date, or serialization is decided by WP1.

**Five-part gate:** `PASS` at candidate level.

### 4.7 `PA-V07` — Portfolio Input Sufficiency — `ADMIT`

**Exact candidate meaning:** Portfolio Input Sufficiency is the deterministic
classification of whether the exact supplied canonical inputs satisfy every
declared prerequisite of the specified Portfolio calculation.

**Owner:** Portfolio Intelligence.

**Justification:** M40 Input Sufficiency is explicitly Market
Intelligence-owned and defined for a Market calculation. The Portfolio
prerequisite surface includes a Portfolio Composition and Ledger-derived
evidence that the Market term excludes. The Portfolio noun is also distinct
from M39 Semantic Sufficiency.

**Exclusions:** It does not assess truth, quality, freshness, trust,
suitability, success, lifecycle authority, or production availability. WP1
does not admit its values or reason taxonomy.

**Five-part gate:** `PASS` at candidate level.

### 4.8 `PA-V08` — Portfolio Measure Result — `ADMIT`

**Exact candidate meaning:** A Portfolio Measure Result is one immutable,
owner-explicit semantic result of applying one exact Portfolio Method Version
to one exact Portfolio Measure Subject and one exact Portfolio Analytics Input
Manifest.

**Owner:** Portfolio Intelligence.

**Justification:** Market Measure Result is Market Intelligence-owned and
excludes Portfolio subjects. PortfolioSnapshot is Ledger-derived disposable
evidence and lacks the M43 identities and closed lineage required of this
result. A distinct Portfolio result noun is therefore necessary.

**Exclusions:** WP1 specifies no fields, ordering, bytes, hash, value shape,
outcome values, temporal binding, persistence, endpoint, or concrete result.
It implies neither correctness nor production availability.

**Five-part gate:** `PASS` at candidate level.

### 4.9 `PA-V09` — Portfolio Computation Outcome — `ADMIT`

**Exact candidate meaning:** Portfolio Computation Outcome is the
Portfolio Intelligence-owned axis stating whether the specified Portfolio
calculation completed with the required Portfolio Measure output.

**Owner:** Portfolio Intelligence.

**Justification:** M40 Computation Outcome is explicitly Market
Intelligence-owned and belongs to the Market Measure contract family.
Reusing it for a Portfolio calculation would leak subject and owner. A
Portfolio-scoped noun is required, while the mechanical separation between
outcome, sufficiency, Degraded State, and Evaluation is reused as a pattern.

**Mandatory reservation:** `UNAVAILABLE` remains a Degraded State under
M34-D-0005 and M40-WP1 §8.3. It must not become a Portfolio Computation
Outcome. A successful outcome must not imply correctness, trust, currentness,
suitability, recommendation, runtime availability, or production admission.

**Exclusions:** WP1 does not admit an outcome enumeration, mapping, reason
taxonomy, result-value rule, or exception contract. WP5 owns that later
contract subject after WP1 confirmation.

**Five-part gate:** `PASS` at candidate level.

### 4.10 `PA-V10` — Portfolio Deterministic Calculation — `ADMIT`

**Exact candidate meaning:** A Portfolio Deterministic Calculation is the
Portfolio Intelligence-owned semantic reproducibility property under which
identical canonical Portfolio inputs, explicit parameters, Portfolio Method
Version, and governed dependency versions produce an identical canonical
Portfolio Measure Result.

**Owner:** Portfolio Intelligence.

**Justification:** M40 Deterministic Calculation is expressly defined to
produce a Market Measure Result and is Market Intelligence-owned. Ledger
Derivation describes replayable accounting truth. Neither term can be
reinterpreted to describe a Portfolio-derived result, so a Portfolio-scoped
noun is necessary.

**Exclusions:** Determinism is not correctness, trust, implementation, a
formula, a kernel, execution, or production availability. WP1 does not decide
canonical bytes or identity inputs.

**Five-part gate:** `PASS` at candidate level.

### 4.11 `PA-V11` — Portfolio Degraded State — `REUSE`

**Disposition:** `REUSE` the existing `Degraded State`.

**Reason:** M34-D-0005 already supplies one complete Canonical Temporal Claim
grammar with Event Type, Producing Domain, authoritative timestamp, and
Degraded State. The Producing Domain owns the event, timestamp meaning, and
Degraded State for the exact claim. A Portfolio Intelligence-produced result
therefore uses the existing `Degraded State` term with Producing Domain
`Portfolio Intelligence`; it does not need a parallel Portfolio-prefixed
state axis.

The candidate phrase `Portfolio Degraded State` is not a new canonical
spelling. Its one disposition is `REUSE`, which routes every permitted use to
`Degraded State` at its frozen meaning and ownership rule.

**Mandatory reservation:** the only approved states remain `UNKNOWN`,
`UNAVAILABLE`, `DELAYED`, `STALE`, `PARTIAL`, and `CONFLICTING` unless a
future constitutional amendment changes M34-D-0005. No M43 document may add a
seventh value. `UNAVAILABLE` must not be used as a Portfolio Computation
Outcome.

**Glossary consequence:** no `Portfolio Degraded State` entry may be added.

## 5. Admission / Reuse / Rename / Reject matrix

| Candidate | Collision tested | Why reuse is or is not sufficient | Final disposition request | Glossary action after independent confirmation |
| --- | --- | --- | --- | --- |
| Portfolio Measure | Market Measure; Calculated Market Measure; Portfolio Composition | Market terms exclude Portfolio subjects; Composition carries no derived measure | `ADMIT` | Add |
| Portfolio Measure Definition | Market Measure Definition; Asset Definition; Definition Version | Each collision has a different subject and owner | `ADMIT` | Add |
| Portfolio Method Version | M41 Method Version; Definition Version | Market method identity and Asset definition identity are not Portfolio method identity | `ADMIT` | Add |
| Portfolio Measure Subject | M41 Measure Subject; Portfolio Identity; Portfolio Composition | M41 subject excludes Portfolio; Identity/Composition are inputs, not calculation-subject binding | `ADMIT` | Add |
| Portfolio Analytics Input Manifest | Observation Input Manifest; Provenance | Observation manifest has a narrower Market input closure; Provenance is lineage, not the complete binding | `ADMIT` | Add |
| Portfolio Measurement Window | M41 Measurement Window; Canonical Temporal Claim | Market window has the wrong contract family; temporal claim is not an input-selection window | `ADMIT` | Add |
| Portfolio Input Sufficiency | Input Sufficiency; Semantic Sufficiency | Both existing terms answer differently scoped questions | `ADMIT` | Add |
| Portfolio Measure Result | Market Measure Result; PortfolioSnapshot; Portfolio Composition | Existing results/snapshots have different subject, owner, or authority | `ADMIT` | Add |
| Portfolio Computation Outcome | Computation Outcome; Degraded State; Evaluation | Market outcome has wrong owner; State and Evaluation are orthogonal | `ADMIT` | Add |
| Portfolio Deterministic Calculation | Deterministic Calculation; Ledger Derivation | Existing terms produce Market knowledge or accounting truth, not Portfolio knowledge | `ADMIT` | Add |
| Portfolio Degraded State | Degraded State | Existing producing-domain grammar is exactly sufficient; the prefixed spelling is not admitted | `REUSE` | None; cite existing entry |

`RENAME` count: zero.
`ADMIT` count: ten.
`REUSE` count: one.
`REJECT` count: zero.

The existing `Degraded State`, `Portfolio Composition`, `Provenance`, Asset
Foundation vocabulary, Ledger vocabulary, M39 observations, and M41 Market
Measure Results are consumed by exact `REUSE` citation where applicable; they
are not candidates for re-admission.

## 6. Ownership and Authority Matrix

### 6.1 Frozen ownership preserved

| Concern | Sole owner | Ownership classification | Governing authority | WP1 boundary |
| --- | --- | --- | --- | --- |
| Portfolio Identity, Accounting Scope, Membership, Base Currency | Ledger & Accounting | Frozen (with governing authority) | M42-WP2 and M42-WP7 | Exact citation only |
| Portfolio Lifecycle State | Ledger & Accounting | Frozen (with governing authority) | M42-WP6; M34-D-0002 | Exact citation only |
| Ledger events, replay, holdings, cash, cost basis, snapshots | Ledger & Accounting | Frozen (with governing authority) | Platform Laws 1–3; ADR-001 through ADR-004 | Authoritative evidence; never redefined |
| Portfolio Composition | Portfolio Intelligence | Frozen (with governing authority) | M42-WP7 | Only permitted Portfolio subject |
| Portfolio-derived measures and performance semantics | Portfolio Intelligence | Frozen (with governing authority) | Platform Architecture §6.5; M40-WP1 §8.3; M42 Architecture §8 | Owning domain of admitted WP1 nouns |
| Portfolio Benchmark Declaration | Portfolio Intelligence | Frozen (with governing authority) | M42-WP5 | Comparison declaration only; never benchmark data |
| Market observations, FX, calendars, benchmark observations, market reference measures | Market Intelligence | Frozen (with governing authority) | Platform Architecture §6.2; M39–M41 | Exact evidence only |
| Asset identity, currency dimension, Unit Semantics, Asset Classification, taxonomy | Asset Foundation | Frozen (with governing authority) | Platform Architecture §6.1; M34-D-0004 | Exact versioned references |
| Analytical Grouping | Portfolio Intelligence | Frozen (with governing authority) | M34-D-0001 and M34-D-0004 | Distinct from Asset Classification; WP8-local use still requires its own gate |
| Canonical Temporal Claim and Degraded State grammar | Producing domain for the exact claim | Frozen (with governing authority) | M34-D-0005 | Reuse exactly; no Portfolio-prefixed state |
| Provenance meaning and capture | Connectivity & Ingestion | Frozen (with governing authority) | Platform Architecture §6.4; M42-WP6 | Carry already-captured lineage; never reconstruct |
| Recommendations, constraints, optimization, execution plans | Decision Intelligence | Frozen (with governing authority) | Platform Architecture §6.6 | Excluded |
| Grades, causal evaluation, human-vs-AI evaluation | Trust & Evaluation | Frozen (with governing authority) | Platform Architecture §6.7 | Excluded |
| Rendering and interaction | Experience Platform | Frozen (with governing authority) | Platform Architecture §§6.9 and 7.3 | Renders; computes nothing |
| Cross-portfolio exposure and net worth | Wealth Intelligence | Frozen (with governing authority) | Platform Architecture §6.8; M34-D-0003 | Excluded |

### 6.2 Candidate ownership created by this register

All ten `ADMIT` nouns in §3 have:

- **proposed sole owner:** Portfolio Intelligence;
- **current classification:** `Candidate — Owner to Prove`;
- **transition condition:** independent constitutional confirmation of this
  register; and
- **failed-proof behavior:** `Rejected`, with downstream reliance blocked.

No candidate is frozen merely because this authoring artifact proposes
`ADMIT`. Confirmation, not authorship, changes the status.

### 6.3 Rejected ownership claims

| Ownership claim | Classification | Reason |
| --- | --- | --- |
| Market Intelligence owns Portfolio Measure contract nouns | Rejected | Market Measure contracts exclude Portfolio subjects |
| Ledger & Accounting owns Portfolio-derived measure semantics merely because it supplies ledger evidence | Rejected | Evidence ownership does not transfer Portfolio knowledge ownership |
| Portfolio Intelligence owns Ledger events, replay, snapshots, Base Currency, or Accounting Scope | Rejected | Frozen Ledger ownership |
| Portfolio Intelligence owns benchmark observations, FX, or calendars | Rejected | Frozen Market Intelligence ownership |
| Portfolio Intelligence owns Asset Classification or taxonomy | Rejected | Frozen Asset Foundation ownership |
| Portfolio Intelligence recaptures or reconstructs Provenance | Rejected | Frozen Connectivity & Ingestion ownership |
| Experience owns a measure because it renders or recomputes it | Rejected | Experience computes nothing |
| Runtime, storage, endpoint, provider, or caller owns a term through custody | Rejected | Custody is not semantic ownership |
| Portfolio Degraded State is an independently owned Portfolio vocabulary axis | Rejected | M34-D-0005 already provides the complete producing-domain grammar |

## 7. Canonical period-return ownership proof

### 7.1 Candidate tested

Frozen M43 §8 presents:

> Canonical period-return rule — Candidate: Ledger & Accounting — Owner to
> Prove at WP1.

The candidate owner is not an instruction to pre-approve the allocation. M43
§8 expressly states that M43 pre-owns and pre-admits nothing and that a failed
proof blocks the dependency.

### 7.2 Governing evidence

| Authority | Finding |
| --- | --- |
| Platform Architecture §6.3 | Ledger & Accounting owns financial truth, transaction vocabulary, accounting semantics, and the canonical return and metric formulas’ **inputs** |
| Platform Architecture §6.5 | Portfolio Intelligence owns canonical derived measures and their semantics, performance measurement under canonical formulas, and the meaning of performance |
| M40-WP1 §8.3 | `portfolio measure` and portfolio performance remain Portfolio Intelligence meaning |
| M42 Architecture §8 deferred-capability matrix | “Portfolio performance / return computation” is allocated to Portfolio Intelligence and consumes frozen accounting rules |
| M42-WP1 §3 | Accounting arithmetic, NAV/return formulas, and cost-basis rules remain frozen in the Portfolio Calculation Rules, while future derived performance remains Portfolio Intelligence |
| Portfolio Calculation Rules §§1–9 | This level-2 Domain Constitution owns the accounting semantics that determine what enters the return, including capital-event stripping, external cash flow, imported assets, quantity corrections, and NAV |
| Portfolio Calculation Rules §10 | Analytics must consume `PortfolioSnapshot.investment_return_pct` and must not independently recompute return |
| ADR-001 | Ledger is the source of truth for the evidence from which the result is derived |
| ADR-004 | The rule must have one implementation; it does not transfer semantic ownership to the module holding that implementation |

### 7.3 Finding

The phrase “canonical period-return rule” combines two constitutionally
distinct allocations and therefore cannot be assigned as one indivisible
ownership claim:

1. **Measure meaning:** Portfolio Intelligence owns the meaning of the period
   return as Portfolio performance under Platform Architecture §6.5 and
   M40-WP1 §8.3.
2. **Accounting semantics:** Ledger & Accounting retains, unamended, the
   frozen rules that determine what enters that return under the Portfolio
   Calculation Rules §§1–9. Capital-event stripping, external cash flow,
   imported assets, quantity corrections, NAV, cost basis, and the associated
   accounting arithmetic are accounting rule, not merely evidence.

The proposed claim that Ledger & Accounting owns the entire composite
period-return rule therefore fails the owner portion of the five-part gate
only as to the Portfolio performance meaning. Conversely, Portfolio
Intelligence does not acquire or redefine the accounting semantics merely
because it owns the derived measure meaning.

Therefore:

| Item | Result |
| --- | --- |
| “Ledger & Accounting owns the canonical period-return rule” | `Rejected` |
| Period-return Portfolio performance meaning | `Frozen — Portfolio Intelligence` |
| Accounting semantics determining what enters the return | `Frozen — Ledger & Accounting`; Portfolio Calculation Rules §§1–9 remain controlling |
| Ledger & Accounting evidence relationship | Supplies exact ledger-derived inputs and replay/snapshot evidence under its frozen ownership |
| Existing `compute_period_metrics()` relationship | Current sole implementation under ADR-004; source placement does not decide constitutional owner |
| Duplicate Portfolio return formula | Prohibited |
| Accounting open questions | Remain outside M43; no indirect settlement |

This finding amends neither the level-2 Portfolio Calculation Rules Domain
Constitution nor ADR-001 or ADR-004. It creates no formula authority and
settles no accounting question.

### 7.4 Downstream consequence

Frozen M43 §9 WP6 says that if WP1 confirms a disposition different from
Ledger & Accounting ownership, WP6 is blocked pending correction. Upon
independent confirmation of this corrected WP1 corpus, this finding therefore
blocks WP6:

> `M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6`

This is not an amendment to M43 and does not design WP6. It is the exact
fail-closed consequence the frozen architecture requires. WP2 may not use this
finding to specify a formula, method, or production behavior.

The correction path is documentary and governed:

1. the WP1 independent confirmation records whether §7.3 is confirmed and,
   only if confirmed, activates the block;
2. the confirmed block is carried as a standing M43 governance item owned by
   the M43 governance sequence, not by WP6;
3. the governing M43 ownership row must be reconciled by an independently
   reviewed constitutional correction before WP6 begins; and
4. the final resolution is recorded in the consolidated Decision Log entry
   authorized at M43 epic closeout by frozen M43 §§13 and 17.

Until steps 1–3 are complete, WP6 may not begin. This routing names a
governance instrument and closure record without specifying any WP6 contract,
formula, or implementation.

## 8. Cross-domain semantic duplication controls

| Seam | Required rule |
| --- | --- |
| Market Measure vs Portfolio Measure | Different governed subjects and owners; no subtype, alias, or relabeling |
| Observation Input Manifest vs Portfolio Analytics Input Manifest | The former binds M39 observation evidence for Market calculations; the latter binds the complete Portfolio calculation evidence set |
| Input Sufficiency vs Portfolio Input Sufficiency | No shared type or owner assumption; values and reasons are not inherited automatically |
| Computation Outcome vs Portfolio Computation Outcome | Mechanical separation pattern may be cited; Market-owned enumeration is not silently inherited |
| Deterministic Calculation vs Portfolio Deterministic Calculation | Same constitutional determinism principle, different result family and owner |
| Market Measure Result vs Portfolio Measure Result | Neither may accept the other’s subject or imply a shared registry |
| Measurement Window vs Portfolio Measurement Window | Different calculation family; neither replaces Canonical Temporal Claim |
| Portfolio Composition vs Portfolio Measure Result | Composition is the subject and carries no derived measure; Result is derived knowledge |
| Asset Classification vs Analytical Grouping | Labels may coincide; authority and version must never be inferred across the seam |
| Portfolio Computation Outcome vs Degraded State | Outcome answers completion; State qualifies temporal availability; `UNAVAILABLE` remains only a State |
| Portfolio measure vs Trust & Evaluation | A deterministic result is not a correctness, reliability, causal, or recommendation-quality verdict |
| Portfolio measure vs Wealth Intelligence | Exactly one Portfolio only; no household or cross-portfolio meaning |

## 9. Glossary Synchronization Package

### 9.1 Synchronization status

`NOT APPLIED`.

This register is not independently confirmed in the present change.
Requirement 9 and frozen M43 §13 permit `docs/GLOSSARY.md` changes only for
independently confirmed admissions or renames. Applying the following package
now would falsely make candidates effective.

### 9.2 Post-confirmation additions

After independent constitutional confirmation, the confirmation change must
add exactly these ten headings to `docs/GLOSSARY.md`:

1. `Portfolio Measure`
2. `Portfolio Measure Definition`
3. `Portfolio Method Version`
4. `Portfolio Measure Subject`
5. `Portfolio Analytics Input Manifest`
6. `Portfolio Measurement Window`
7. `Portfolio Input Sufficiency`
8. `Portfolio Measure Result`
9. `Portfolio Computation Outcome`
10. `Portfolio Deterministic Calculation`

Each entry must:

- use the exact candidate meaning from §4;
- name Portfolio Intelligence as owner;
- state that it creates no implementation, runtime, provider, persistence,
  API, UI, or production-method authority;
- link this register and its independent confirmation;
- mark “Effective now: Yes” only in the confirmation change; and
- preserve all cross-domain exclusions in §8.

### 9.3 No-add and no-change list

The synchronization change must not:

- add `Portfolio Degraded State`;
- change the six M34-D-0005 Degraded State values;
- change `UNAVAILABLE` into an outcome;
- edit or broaden Market Measure, Market Measure Result, Input Sufficiency,
  Computation Outcome, Deterministic Calculation, Observation Input Manifest,
  or M41 contract vocabulary;
- edit any M42 Portfolio entry;
- add a concrete Portfolio Measure Definition, Portfolio Method Version,
  formula, method, registry, result instance, or production-method claim; or
- modify M1–M42 governance artifacts.

The existing `Degraded State` entry is reused without edit unless the
independent reviewer requires a purely cross-referential link; any such link
must not alter meaning or ownership.

No equivalent allowance is necessary for the existing `Computation Outcome`,
`Input Sufficiency`, or `Deterministic Calculation` entries. Glossary V1
already distinguishes those domain-generic definitions through their frozen
Market Intelligence ownership, while the ten new Portfolio-prefixed entries
will state Portfolio Intelligence ownership and link their collision
boundaries back to this register. A link from each new Portfolio entry to its
frozen Market counterpart supplies the useful cross-reference without editing
an existing term. The stricter no-change rule therefore remains necessary to
prevent an M43 synchronization change from appearing to reopen M40–M41.

### 9.4 Synchronization verification

After confirmation, verify:

1. ten and only ten new M43-WP1 glossary headings exist;
2. zero rename entries exist;
3. no `Portfolio Degraded State` heading exists;
4. every new entry links the independent confirmation;
5. all ten owners are Portfolio Intelligence;
6. every entry remains non-implementing and non-production;
7. existing Market, Ledger, Asset, Provenance, temporal, Decision, Evaluation,
   Experience, and Wealth entries are unchanged in meaning; and
8. repository-relative links resolve.

## 10. Validation Rules

### 10.1 Vocabulary collision

For every admitted candidate, validation must check exact-name, stem,
synonym, subject, input, output, event, owner, and prohibited-semantics
collisions against `docs/GLOSSARY.md`, M39–M42, and the M34 decision register.
A name-only search is insufficient.

Pass condition: every candidate has one disposition and no existing term can
carry the candidate meaning without owner or subject reinterpretation.

**Recorded evidence:** the independent constitutional review performed a
repository-wide search and found zero pre-existing occurrences outside the
M43 corpus for all ten admitted candidate names. It also checked every cited
counterpart at subject, input, output, and owner level: Market Measure, Market
Measure Definition, Method Version, Measure Subject, Observation Input
Manifest, Measurement Window, Input Sufficiency, Market Measure Result,
Computation Outcome, Deterministic Calculation, Portfolio Composition,
Canonical Temporal Claim, and Degraded State. No collision or reusable
same-owner/same-subject meaning was found. The M41 counterparts are governed
by the confirmed M41 corpus even though four of those terms have not yet been
synchronized into `docs/GLOSSARY.md`; that pre-existing M41 synchronization
gap is not widened or repaired by WP1.

### 10.2 Ownership leakage

For every noun and ownership row:

- input ownership remains with the supplying domain;
- Portfolio Intelligence owns only the derived Portfolio knowledge;
- custody and rendering create no ownership;
- no row has shared ownership; and
- every non-frozen owner remains `Candidate — Owner to Prove` until
  confirmation.

Pass condition: exactly one semantic owner or an explicit Rejected result.

### 10.3 Cross-domain semantic duplication

Validation must apply every seam in §8 and reject aliases, subtypes, wrapper
types, or shared enumerations that silently widen an existing owner’s term.

Pass condition: Market, Portfolio, Ledger, Asset, Decision, Evaluation,
Experience, and Wealth meanings remain mechanically separable.

### 10.4 Constitutional conflict

Validation must prove preservation of:

- Platform Laws 1–15;
- M34-D-0004 classification/grouping separation;
- M34-D-0005 temporal/degraded-state grammar;
- Platform Architecture §6.4 and M42-WP6 Provenance ownership and capture;
- M39 Observation meaning;
- M40–M41 Market Measure ownership;
- M42 Portfolio coordinate ownership and no-derived-measure invariant; and
- ADR-001/ADR-004 source-of-truth and one-rule constraints.

Pass condition: no frozen decision is amended, weakened, or reinterpreted.

### 10.5 Implementation leakage

The corpus must contain no normative module, class, function, storage schema,
endpoint, cache, scheduler, adapter, registry, kernel, library, migration,
call-site, serialization encoding, identifier syntax, or rollout decision.

Pass condition: current code appears only as evidence in the reconciliation
artifact.

### 10.6 Runtime authority

No noun or example may imply that a method can be invoked, registered,
discovered, persisted, served, cached, scheduled, or rendered as a canonical
M43 result.

Pass condition: runtime, source, persistence/API/UI, provider, and executable
validation authority remain `NONE`.

### 10.7 Production-method admission

No formula, worked example, fixture, Definition instance, Method Version
instance, outcome enumeration, or legacy behavior may be described as an
admitted production method.

Pass condition: production-method authority remains `NONE`, and any later
method remains non-production until separately authorized.

### 10.8 Documentary validation commands

The independent review should perform repository-wide, read-only searches for:

- every candidate name and plausible unprefixed collision;
- `UNAVAILABLE` near outcome language;
- Portfolio subjects inside M40–M41 contract types;
- request/default benchmark, risk-free, annualization, calendar, provider,
  cache, `Current Selection`, cross-portfolio, Wealth, recommendation,
  evaluation, and Experience-computation language;
- production, runtime, implementation, schema, API, persistence, provider,
  registry, and kernel authority claims; and
- modifications outside the two WP1 deliverables and the conditionally
  authorized post-confirmation glossary change.

These are documentary searches, not executable M43 validation artifacts.

## 11. Completion Criteria

M43-WP1 is complete only when:

1. the roadmap and current-state reconciliation is independently approved;
2. all eleven candidate terms have exactly one confirmed disposition;
3. all ten proposed admissions have one independently confirmed owner;
4. `Portfolio Degraded State` is confirmed `REUSE`, the prefixed spelling is
   not admitted, and the existing Degraded State grammar is reused unchanged;
5. `UNAVAILABLE` remains a Degraded State and is not any computation outcome;
6. the canonical period-return ownership proof is independently confirmed,
   including the recorded WP6 block required by the different disposition;
7. no vocabulary collision, ownership leakage, cross-domain duplication, or
   constitutional conflict remains;
8. the negative corpus passes;
9. the legacy inventory and duplicate-rule map are complete and are not
   treated as precedent;
10. glossary synchronization is applied only in the independent-confirmation
    change and passes §9.4;
11. no downstream WP has relied on an unconfirmed noun;
12. no WP2 or later contract, field, formula, method, fixture, or
    implementation design has been specified;
13. no M1–M42 artifact has been modified;
14. no backend, frontend, model, migration, API, operational, or deployment
    file has been modified;
15. runtime, implementation, provider, persistence/API/UI,
    production-method, and executable-validation authority remain `NONE`; and
16. unresolved WP1 findings are `NONE`.

Until independent confirmation and glossary synchronization are both
complete, WP1 remains non-effective in
`CORRECTED AFTER INDEPENDENT REVIEW — REQUIRES INDEPENDENT CONFIRMATION`
status, every `ADMIT` owner remains `Candidate — Owner to Prove`, and
downstream reliance remains prohibited.

## 12. Required-Corrections Change Summary

This correction revision preserves the eleven-term candidate register and all
eleven dispositions: ten `ADMIT`, one `REUSE`, zero `RENAME`, and zero
`REJECT`. It introduces no noun, capability, contract, formula, runtime,
implementation, or production-method authority.

The revision:

- decomposes canonical period-return ownership into Portfolio performance
  meaning and frozen Ledger & Accounting rule semantics;
- routes the conditional WP6 block through confirmation, a standing M43
  governance item, an independently reviewed M43 correction, and the
  authorized epic-closeout Decision Log record;
- completes the current-state duplicate map for
  `attribution_engine.py::_compute_twr()`,
  `attribution_engine.py::compute_actual_indexed_series()`, and
  `shadow_tracker.py::_benchmark_return_pct()` without selecting a future
  implementation;
- restores the frozen caller-parameter restriction;
- corrects Provenance authority citations;
- aligns the reconciliation authority block with all seven `NONE`
  declarations;
- adds the three omitted frozen exclusions to the negative corpus;
- makes the WP6 block expressly effective only upon WP1 confirmation;
- records the independent collision-search evidence;
- records the governing architecture confirmation and the external
  repository-status synchronization prerequisite; and
- retains the glossary no-change rule for the three Market Intelligence twins
  after determining that links from the new Portfolio-prefixed entries are
  sufficient.

## 13. Required-Corrections Response Matrix

| Finding | Response | Constitutional justification and implemented result |
| --- | --- | --- |
| `M-1` | `ACCEPTED` | §7.3 now separates Portfolio Intelligence ownership of period-return performance meaning from Ledger & Accounting ownership of the accounting semantics in the Portfolio Calculation Rules §§1–9. It expressly amends neither that Domain Constitution nor ADR-001/004. |
| `M-2` | `ACCEPTED` | §7.4 now names the instruments, sequence, and closure record: WP1 independent confirmation, a standing M43 governance item, an independently reviewed M43 correction before WP6, and the consolidated Decision Log entry authorized by M43 §§13 and 17. No WP6 design is introduced. |
| `M-3` | `ACCEPTED` | The reconciliation §§3.2–3.3 now inventory both omitted `attribution_engine.py` return paths and `shadow_tracker.py::_benchmark_return_pct()`. Their treatment remains only `CHARACTERIZE` or `REJECT AS PRECEDENT`; no call site or method is admitted. |
| `m-1` | `ACCEPTED` | §2 restores verbatim the frozen prohibition against caller override of Benchmark Declaration, risk-free input, annualization basis, calendar authority, or any governed dependency. |
| `m-2` | `ACCEPTED` | §§6.1 and 10.4 now cite Platform Architecture §6.4 plus M42-WP6 for Provenance ownership and capture. M34-D-0010 is no longer presented as the allocation authority. |
| `m-3` | `ACCEPTED` | The reconciliation header now declares Source-code, Persistence/API/UI, and Provider authority `NONE`, completing the same seven-part authority boundary as this register. |
| `m-4` | `ACCEPTED` | Negative-corpus items 21–23 now reject Portfolio Policy or renamed equivalents, Investment Universe membership/eligibility, and inference of missing Base Currency, Lifecycle State, or Provenance. |
| `m-5` | `ACCEPTED` | §7.4 now states that the governance finding blocks WP6 only upon independent confirmation; candidate effectivity remains uniform and fail-closed. |
| `m-6` | `ACCEPTED` | §10.1 records the review’s repository-wide zero-collision result and the subject/input/output/owner checks for every cited counterpart, while noting the pre-existing M41 glossary synchronization gap. |
| `m-7` | `PARTIALLY ACCEPTED` | §1 records the commissioning authority’s architecture confirmation and the WP1 status lines now show this corrected post-review state. The repository-local M43 plan status line cannot be edited because the correction authority expressly permits only WP1 artifacts; §1 therefore records that synchronization as a separately authorized prerequisite before WP1 confirmation. |
| `m-8` | `PARTIALLY ACCEPTED` | The requested evaluation was accepted, but the proposed allowance was not. §9.3 explains that ownership plus Portfolio-prefixed new entries already satisfies Glossary V1 and permits useful links from new entries without reopening existing M40–M41 terms. The existing no-change wording is retained. |
| `o-1` | `ACCEPTED` | The naming asymmetry is acknowledged as deliberate and remains governed by frozen M43; no rename or candidate-set change is authorized. |
| `o-2` | `ACCEPTED` | The observation is valid: snapshot records may be immutable historical records while remaining Ledger-derived, replayable evidence rather than M43 results. No requested correction or semantic change follows. |
| `o-3` | `ACCEPTED` | §10.1 records the M41 glossary synchronization gap and makes clear that the collision proof relies on the confirmed M41 corpus. WP1 neither repairs nor widens that external gap. |
| `o-4` | `ACCEPTED` | Repository-scope validation remains required: only the WP1 artifacts are changed by this correction pass; no glossary, M1–M42, source, runtime, model, migration, or operational artifact is authorized. |
