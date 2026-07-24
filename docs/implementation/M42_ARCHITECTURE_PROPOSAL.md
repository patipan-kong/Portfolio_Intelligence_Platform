# M42 — Architecture Proposal

**Document role:** Architecture Review Board (fresh session)

**Document status:** `READY FOR INDEPENDENT ARCHITECTURE REVIEW`

**Proposal date:** 2026-07-24

**Milestone:** M42 — Portfolio Intelligence Foundation (Canonical Portfolio Domain)

**Advisory role:** Architecture and Implementation advisor

**M29–M41 corpus authority:** `COMPLETE`, `CONFIRMED`, `FROZEN` (cited, not
modified)

**Implementation authority:** `NONE`

**Runtime authority:** `NONE`

**Provider authority:** `NONE`

**Persistence authority:** `NONE`

**API authority:** `NONE`

**Production-method authority:** `NONE`

**Executable-validation authority:** `NONE`

**Normative status:** This document is a non-canonical architecture proposal.
Its use of `MUST`, `MUST NOT`, `SHALL`, `SHALL NOT`, `MAY`, and `SHOULD`
describes requirements proposed for review. Those terms acquire no repository
authority unless and until this proposal is independently reviewed and
explicitly approved, work package by work package, under the same per-artifact
governance sequence M40 and M41 established: a separately-governed **Architecture
Proposal**, **Stage A Candidate Vocabulary Register**, and **Stage B Contract
Specification**, each independently reviewed, corrected where required, and
independently confirmed before the next gate opens.

---

## 0. Authority, Precedence, and Non-Reopening Rule

This proposal determines the architectural scope, semantic boundaries, work
package decomposition, and implementation-neutral roadmap for **M42** exactly
within the space the frozen constitution leaves open. It is subordinate, in
order, to:

1. the frozen [Platform Architecture](../architecture/platform_architecture.md)
   constitution (v1.1) — its nine domains, six layers, three gates, fifteen
   laws, governance precedence (§11), and canonical-vocabulary rules (§12);
2. the frozen domain constitutions —
   [OPTIMIZER_PHILOSOPHY.md](../investment/OPTIMIZER_PHILOSOPHY.md) and
   [PORTFOLIO_CALCULATION_RULES.md](../investment/PORTFOLIO_CALCULATION_RULES.md);
3. the frozen Architecture Decision Records, in particular `M34-D-0002`,
   `M34-D-0003`, `M34-D-0007`, and `ADR-004`;
4. the frozen M29–M41 milestone corpus — M29 runtime adoption, M30–M31
   capability safety, M32 cost-aware execution, M33 identity/authority, M34
   semantic governance, M35 product workspace, M36 multiple-portfolio
   foundation, M37 universal asset search, M38 product workspace foundation,
   M39 canonical market observation, and M40–M41 canonical market measure
   semantics; and
5. the [Portfolio Domain Model](../architecture/PORTFOLIO_DOMAIN_MODEL.md), a
   Level-4 design-of-record that M42 **canonicalizes** but does not author
   anew.

If this proposal conflicts with any higher authority, the higher authority
governs and the conflicting clause is invalid.

**Non-reopening.** M42 does not reopen, reinterpret, extend, correct, or
replace any decision of M29–M41 or of `M34-D-0002/0003/0007`. In particular it
accepts as **fixed and consumes by exact reference**:

- **Portfolio Identity**, **Accounting Scope**, **Portfolio Membership**,
  **Cross-Portfolio Aggregation** — owned by Ledger & Accounting, frozen under
  `M34-D-0002` / `M34-D-0003`;
- **Portfolio Lifecycle State** — owned by Ledger & Accounting, frozen under
  `M34-D-0002`, `M36-WP1-A01`, `M36-WP1-A09`;
- **Portfolio Strategy Metadata** — owned by Portfolio Intelligence, frozen
  under `M34-D-0002` / `M34-D-0007`;
- **Portfolio Limits** and **Sector Limits** — owned by Decision Intelligence,
  frozen under `M34-D-0007`;
- **Goal Target** and **Cross-Portfolio Exposure** — owned by Wealth
  Intelligence, frozen under `M34-D-0002/0003/0007`;
- **Current Selection** — owned by Experience Platform, frozen under
  `M34-D-0002`;
- the frozen **M39** Market Observation corpus and the frozen **M40–M41**
  Market Measure corpus, consumed by citation only; and
- the frozen **M37** universal asset search and **M36/M38** workspace
  foundations, preserved unchanged.

M42 introduces **no new constitutional domain**. The constitution's Section 6
enumerates nine domains and no "Portfolio" domain among them; the canonical
name for the Knowledge-layer domain that owns portfolio meaning is **Portfolio
Intelligence** (§6.5). Creating a tenth domain would be a Section-6 amendment
under constitutional process (§10) and is explicitly out of scope. "Canonical
Portfolio domain," throughout this proposal, denotes the **canonical semantic
surface of the Portfolio object** whose coordinates are already owned, per M34,
across five existing domains — never a new box on the domain diagram.

---

## 1. Milestone Objective (Deliverable 1)

The complete architectural allocation of M42 is:

> Establish the **canonical Portfolio semantic foundation**: the frozen,
> implementation-neutral contract for what a **Portfolio** *is* as a composed
> object — its identity and accounting boundary, its declarative strategy
> surface (Investment Universe, Portfolio Policy, Benchmark, Base Currency),
> its lifecycle and provenance, and the single deterministic **Portfolio
> Composition** projection through which every downstream domain reads it —
> such that the coordinates already owned across Ledger & Accounting, Portfolio
> Intelligence, Decision Intelligence, Wealth Intelligence, and Experience
> Platform compose into exactly one coherent, canonically serializable,
> boundary-clean Portfolio surface, with no derived measure, no ambient
> default, and no ownership migration — thereby founding the semantic bedrock
> on which all future Portfolio functionality (analytics, optimization,
> wealth aggregation, advice) will later rest.

M42 is to the **Portfolio** object what M39 was to the **Market Observation**
and M40–M41 were to the **Market Measure**: the governed canonicalization of a
domain's foundational vocabulary and composition contract, *before* any engine
computes over it. It closes the gap between the Level-4
[Portfolio Domain Model](../architecture/PORTFOLIO_DOMAIN_MODEL.md) (rich,
descriptive, unfrozen) and the Level-1/2 constitution by admitting the domain
model's remaining vocabulary to the Glossary through the governed workflow and
freezing the composition contract that binds it.

M42's terminal exit condition inherits the corpus determinism condition — **no
ambient semantic default remains** across the Portfolio surface — and adds four
Portfolio-specific completion tests: **boundary integrity** (every
portfolio-scoped fact resolves to exactly one Accounting Scope), **declaration/
enforcement separation** (every declarative rule states intent without
computing a verdict), **composition determinism** (the same coordinates project
to the same canonical Portfolio Composition), and **no derived measure** (the
projection carries no performance, risk, attribution, or exposure number).

---

## 2. Architectural Motivation (Deliverable 2)

Four forces make this milestone necessary now, and necessary in this form.

**2.1 The Portfolio noun is real, load-bearing, and still ungoverned as a
whole.** Every engine the platform has built either operates *inside* a
portfolio boundary or *compares across* boundaries (Portfolio Domain Model
§1). Yet the canonical vocabulary defines the Portfolio only in *fragments* —
Identity, Accounting Scope, Membership, Lifecycle State, Strategy Metadata,
Limits — each admitted by a different milestone to a different owner, with no
frozen contract stating how the fragments compose into one object. The
descriptive whole lives only in an unfrozen Level-4 design. A platform heading
toward wealth management cannot leave its central noun half-canonical: the same
scar Law 9 names for calculations — many consumers, no single owned contract —
is forming around the Portfolio itself.

**2.2 The declarative strategy surface has no canonical home.** The Portfolio
Domain Model's most important design decision — *validation is driven by
Investment Universe, not Asset Type* (§4) — depends on three nouns the Glossary
does not yet carry: **Investment Universe** (a descriptive scope *declaration*),
**Portfolio Policy** (proposed as a governed declaration whose owner must be
proven distinct from Decision Intelligence's enforcement **Portfolio Limits**),
and **Benchmark**. Until these are dispositioned to their correct owners through
the governed workflow, universe-declared scope, policy-as-data, and
benchmark-per-strategy remain private dialects (§V2) — and private dialects are
where boundary leaks begin (Law 4 of §2.4). Whether an instrument *belongs* is a
downstream evaluation, not part of this descriptive surface (RC-3).

**2.3 Truth/judgment separation must be drawn *before* analytics arrive, not
after.** The explicit non-goals of M42 — performance, risk, attribution,
exposure, optimization — are precisely the machinery that, if built over an
ungoverned Portfolio, would each grow their own idea of what a portfolio is.
The platform's deepest commitment (§2.1) is that truth and judgment never
blend. A Portfolio Composition projection that carries **only** identity,
boundary, declaration, and lineage — and **no measure** — is the structural
guarantee that when analytics do arrive, they consume a clean surface rather
than inventing one. Founding the surface first is the cheap correction; retro-
fitting a boundary around live analytics is the expensive one.

**2.4 The multiplication opportunity.** The constitution's evolution thesis
(§9) is that each era adds *description*, not *surgery*. A frozen Portfolio
Composition contract is the surface that lets Retirement, Emergency Fund,
Property, and every future strategy arrive as a *declaration* — a universe, a
policy, a benchmark choice — over an invariant projection (Portfolio Domain
Model §11). M42 builds that invariant once so that Phase 5 (Wealth) and Phase 6
(AI Advisor) are acts of description.

M42 is therefore the keystone of the transition from *Multiple Portfolios exist*
(M36) to *the Portfolio is a fully-governed, composable semantic object* — the
Portfolio-domain analog of the observation and measure foundations already laid.

---

## 3. Domain Boundaries (Deliverable 3)

M42 spans the semantic surface of one object across five *existing* domains and
touches a sixth by consumption. It creates no new domain and moves no boundary.

| Constitutional domain | M42 relationship |
|---|---|
| **Ledger & Accounting** (Truth, §6.3) | **Owner** of the accounting-boundary leg: Portfolio Identity, Accounting Scope, Portfolio Membership, boundary-crossing classification, Lifecycle State. M42 canonicalizes their composition; it authors no new accounting rule (that is `PORTFOLIO_CALCULATION_RULES.md`, frozen). |
| **Portfolio Intelligence** (Knowledge, §6.5) | **Owner** of the frozen Portfolio Strategy Metadata, and the **proposed** (not yet admitted) home of the declarative strategy legs that are *not* accounting truth and *not* decision enforcement — Investment Universe (declarative definition) and Benchmark. Ownership of **Portfolio Policy** and **Portfolio Base Currency** is *unproven* and admission-blocked pending WP1 overlap analysis against Decision Intelligence (`M34-D-0007`) and Ledger & Accounting respectively (§4.2, RC-4). M42 founds this domain's vocabulary **without** admitting any of its derived measures. |
| **Decision Intelligence** (Judgment, §6.6) | **Consumer / boundary partner.** Owns Portfolio Limits and Sector Limits (frozen). M42 must draw the exact line between a portfolio-owned **policy declaration** (M42) and a decision-owned **enforcement limit / constraint envelope** (frozen `M34-D-0007`, `OPTIMIZER_PHILOSOPHY.md`). M42 declares; the optimizer enforces. |
| **Wealth Intelligence** (Knowledge widening, §6.8) | **Consumer / boundary partner.** Owns Goal Target and Cross-Portfolio Exposure (frozen). M42 stops at the single-portfolio boundary; wealth-level aggregation-as-interpretation is deferred (§8). |
| **Market Intelligence** (Observation, §6.2) | **Cited authority.** Benchmark series are canonical observations (M39/M40); a Base Currency's FX path is canonical observation. M42 *references* these; it never re-owns valuation. |
| **Experience Platform** (Experience, §6.9) | **Consumer.** Owns Current Selection (frozen). M42 defines the composition Experience renders; Experience computes nothing. |
| **Asset Foundation** (Identity, §6.1) | **Cited authority.** Universe and Policy are *composed from* asset classification, capability, market, and currency vocabulary (frozen). M42 references; it never re-classifies. |

The three constitutional gates (§7.2) are untouched: M42 opens no ingestion,
decision, or configuration gate. It specifies a **read/composition surface**,
not a write path. The dependency law (§7.1) is preserved — every M42 coordinate
depends only downward or sideways-by-citation, never upward.

---

## 4. Semantic Ownership (Deliverable 4)

The organizing principle: **M42 reuses every already-owned Portfolio coordinate
at its frozen owner, and admits each genuinely new coordinate to the domain the
constitution already assigns it — never to a new "Portfolio" owner.**

### 4.1 Reused (frozen — cited, never redefined)

| Coordinate | Frozen owner | Governing authority |
|---|---|---|
| Portfolio Identity | Ledger & Accounting | `M34-D-0002` |
| Accounting Scope | Ledger & Accounting | `M34-D-0002` |
| Portfolio Membership | Ledger & Accounting | `M34-D-0003` |
| Cross-Portfolio Aggregation | Ledger & Accounting | `M34-D-0003` |
| Portfolio Lifecycle State | Ledger & Accounting | `M34-D-0002`, `M36-WP1-A01/A09` |
| Portfolio Strategy Metadata | Portfolio Intelligence | `M34-D-0002`, `M34-D-0007` |
| Portfolio Limits / Sector Limits | Decision Intelligence | `M34-D-0007` |
| Goal Target / Cross-Portfolio Exposure | Wealth Intelligence | `M34-D-0002/0003/0007` |
| Current Selection | Experience Platform | `M34-D-0002` |

### 4.2 Candidate admissions (new governed nouns — proposed dispositions)

Each row below is a **candidate only**. It records the owner and disposition a
work package will *argue for* through the governed per-artifact sequence
(Architecture → Stage A Candidate Vocabulary Register → Stage B Contract), and
carries no force until WP1's **Stage A register is independently confirmed**. No
disposition in this table is operative in advance: this proposal **pre-owns,
pre-admits, and pre-synchronizes nothing**. Until the confirmed WP1 Stage A gate,
every downstream work package (§6) is **conditional on** the confirmed
disposition of the candidates it would specify, and no candidate may be assumed
admitted, owned, or Glossary-synchronized. The *proposed owner* column states a
**target hypothesis to be proven**, not a settled allocation; where a candidate
materially overlaps a frozen allocation, its row is marked **admission-blocked**
until WP1's overlap analysis establishes a single owner and exact permitted
fields.

| Candidate noun | Proposed owner (to prove) | Proposed disposition (candidate) | Rationale / gating condition |
|---|---|---|---|
| **Investment Universe** *(declarative definition only)* | Portfolio Intelligence | candidate `ADMIT` — pending WP1 | The named, portfolio-level *declaration* of the intended scope of holdings (Domain Model §4). A descriptive strategy fact — **not** an accounting fact, **not** an enforcement constraint, and **not** an evaluation/refusal/validation predicate (see the carve-out below and RC-3). |
| **Portfolio Policy** | **unproven — overlap analysis required (WP1)** | **admission-blocked** — pending WP1 owner proof | The declared rulebook of *how the portfolio may operate* (Domain Model §5). It overlaps Decision Intelligence's frozen policy/limit territory (`M34-D-0007`); calling it a "declaration" does not by itself establish a distinct owned concept. Blocked until WP1 proves a single owner, exact permitted fields, and non-duplication of Decision Intelligence semantics. |
| **Benchmark** | Portfolio Intelligence | candidate `ADMIT` — pending WP1 | The declared operational definition of "doing well" per strategy (Domain Model §6). References Market Intelligence series; would own the *choice*, never the series. |
| **Portfolio Base Currency** | **unproven — overlap analysis required (WP1)** | **admission-blocked** — pending WP1 owner proof | The unit of account in which a portfolio's meaning is stated (Domain Model §3). The Domain Model locates Base Currency within **Portfolio Identity** and uses it as the unit of account for NAV/returns — an accounting-semantic relationship with Ledger & Accounting's frozen identity boundary. Blocked until WP1 reconciles that relationship and proves a single owner and exact permitted fields. |
| **Portfolio Composition** | Portfolio Intelligence | candidate `ADMIT` — pending WP1 | The single deterministic projection binding all frozen + confirmed-admitted coordinates into one canonical Portfolio read-surface, carrying **no derived measure**. |
| **Investment Universe Membership** *(belonging predicate)* | **unproven — evaluation semantics; ownership/gate proof required** | **admission-blocked** — not a descriptive coordinate until proven | A predicate that *decides whether an instrument belongs* and a refusal that follows from it are **verdict/enforcement** semantics, not descriptive coordinates (RC-3). It cannot be admitted as Portfolio Intelligence descriptive vocabulary without an ownership and five-part-gate proof consistent with `M34-D-0007`. WP1/WP3 must either prove that proof or route it to a separately-governed non-descriptive admission. |

### 4.3 Ownership guardrails (the five-part gate, adapted from M41 §5.2)

Every M42 concrete coordinate and rule MUST pass, before any review approves it:

1. **Permitted subject:** exactly one Portfolio Identity / Accounting Scope
   already valid under frozen `M34-D-0002`.
2. **Permitted inputs:** only frozen Portfolio coordinates, Asset Foundation
   references, Market Intelligence observation/measure citations, and explicit
   declaration parameters — the same closed input categories the corpus uses.
3. **Output meaning:** only an immutable, deterministic *descriptive*
   coordinate — an identity, a boundary fact, a declaration, a lineage, or the
   composition of these — never a computed measure and never a verdict.
4. **Prohibited inputs:** no live provider answer, no wall-clock, no
   cross-portfolio state read as authority, no model output.
5. **Prohibited semantics:** no performance, return, risk, drawdown,
   attribution, exposure, optimization, ranking, forecast, recommendation,
   trust score, or suitability — the M42 negative corpus (§Non-Goals).

A single failure blocks approval. Stage-B specifications carry a field-by-field
gate table, exactly as M41 required.

---

## 5. Major Architectural Components (Deliverable 5)

M42's normative surface is seven components, A–G. Each is a work-package
obligation; none is *designed* here — this proposal fixes each component's
purpose, owner, and boundary, and defers its contract to the WP's Stage B.

**Component A — Portfolio Canonical Vocabulary & Ownership Register.** The
whole-domain admission/reuse/reject register: every Portfolio coordinate mapped
to exactly one owner, frozen terms cited and new candidates dispositioned per
§4. Owner-of-record: cross-domain, governed by the M40/M41 vocabulary workflow.

**Component B — Portfolio Identity & Accounting Boundary Contract.** The
canonical statement that a Portfolio *is* an accounting boundary: one Accounting
Scope per Portfolio Identity, every portfolio-scoped fact resolving to exactly
one scope, Membership and boundary-crossing classification, and the invariant
that replay never crosses a boundary. Owner: Ledger & Accounting (citation of
`M34-D-0002/0003` and `PORTFOLIO_CALCULATION_RULES.md`, authoring no new rule).

**Component C — Investment Universe Declaration Contract.** The headline
declarative surface: Universe as a first-class named object composed from asset
classification/capability/market/currency vocabulary — a *descriptive
declaration of intended scope*. It **excludes** any evaluation, refusal,
validation, or enforcement predicate: a rule that *decides whether an instrument
belongs* and a refusal that follows from it are verdict/enforcement semantics
(RC-3), which cannot be admitted as descriptive Portfolio Intelligence
vocabulary without a separate ownership and five-part-gate proof consistent with
`M34-D-0007`. Owner (proposed): Portfolio Intelligence for the declaration only;
the belonging predicate is admission-blocked (§4.2) and, if pursued, routed
through its own governed admission rather than authored here.

**Component D — Portfolio Policy Declaration Contract *(admission-blocked)*.**
The declared rulebook — allowed markets/classes/currencies, cash requirement,
leverage prohibition, fractional permission, settlement discipline, tax/wrapper
context — as *data-not-code* declarations that bind forward, never backward
(Domain Model §5). These fields overlap Decision Intelligence's frozen
policy/limit territory (`M34-D-0007`) materially; **owner is unproven** and this
contract MUST NOT be specified until WP1 establishes a single owner, the exact
permitted fields, and non-duplication of Decision Intelligence semantics (RC-4).
Only once owned may its spine — the **declaration/enforcement boundary**, where
M42 declares intent and the frozen Portfolio Limits enforce it — be drawn.

**Component E — Benchmark & Base-Currency Contract.** Benchmark forms (single,
composite, policy-derived, category, explicitly none) as a *strategy
declaration* that references Market Intelligence series but computes nothing;
owner (proposed): Portfolio Intelligence; cited authority: Market Intelligence.
**Portfolio Base Currency** — the unit of account for NAV/returns, which the
Domain Model locates within Portfolio Identity — is an accounting-semantic
coordinate whose **owner is unproven**; its contract is admission-blocked until
WP1 reconciles it against Ledger & Accounting's frozen identity boundary and
proves a single owner and exact permitted fields (RC-4). Once owned, it is fixed
as a changed-only-as-recorded-event unit of account (Domain Model §3, §6).

**Component F — Portfolio Lifecycle State Reuse & Provenance Contract.**
**Reuse-only.** It reuses the frozen Portfolio Lifecycle State (the `active`,
`archived`, `closed` states) and its established invariants — permanent
identity, preservation of history, future-only change — by citation of
`M34-D-0002`, `M36-WP1-A01/A09`. It authors **no** lifecycle-transition
vocabulary: M36 expressly deferred lifecycle *commands*, workflows, runtime
eligibility, and transition legitimacy, so transitions such as create, activate,
clone, merge, import, and export are **out of scope for reuse** and, if pursued,
MUST be routed through a separately-governed non-reuse admission (RC-2), not
authored in this component. It fixes the lineage/provenance every
portfolio-scoped fact carries (Domain Model §8), citing Connectivity & Ingestion
as provenance owner, never re-captured. Owner: Ledger & Accounting.

**Component G — Portfolio Composition & Projection Contract *(terminal)*.** The
single canonical projection that binds Components B–F into one immutable,
serializable Portfolio Composition — identity + boundary + declarations +
lifecycle + lineage — with canonical field order, a schema-version tag,
composition determinism, and the **no-derived-measure** invariant. This is the
Portfolio-domain analog of M41-WP4's Result model: the terminal composition on
which Epic Closeout depends. Owner: Portfolio Intelligence.

---

## 6. Work Package Decomposition (Deliverable 6)

M42 decomposes into **seven work packages**, mirroring the proven corpus shape
(a vocabulary-foundation WP first, a terminal-composition WP last, each interior
WP a single reviewable semantic surface). Each WP runs the full per-artifact
governed sequence exactly as M41-WP1..WP4 did: a separately-governed
**Architecture Proposal**, then a **Stage A Candidate Vocabulary Register**, then
a **Stage B Contract Specification** — each independently reviewed, corrected
where required, and independently confirmed before the next artifact begins, and
Closeout only after Stage B is confirmed. **Confirmation of Architecture gates
Stage A; confirmation of Stage A gates Stage B; confirmation of Stage B gates
Closeout.** Candidate synchronization and any downstream reliance occur **only at
the confirmed Stage A vocabulary gate**, never earlier. **No WP grants
implementation, runtime, provider, persistence, API, production, or
executable-validation authority.**

Every "would specify" entry below is **conditional on the confirmed WP1 Stage A
disposition** of the candidate named; no admission is operative in advance
(RC-1).

| WP | Title | Component | Sole/primary owner | Candidate it would specify (conditional on WP1) |
|---|---|---|---|---|
| **M42-WP1** | Portfolio Canonical Vocabulary & Ownership Register | A | Cross-domain (governed) | the register + all §4.2 dispositions; no contract |
| **M42-WP2** | Portfolio Identity, Accounting Scope & Membership Contract | B | Ledger & Accounting | reuse-only |
| **M42-WP3** | Investment Universe Declaration Contract | C | Portfolio Intelligence | Investment Universe *(declaration only; belonging predicate excluded — RC-3)* |
| **M42-WP4** | Portfolio Policy Declaration Contract *(blocked)* | D | **unproven — WP1 must prove** | Portfolio Policy *(admission-blocked until owner proven — RC-4)* |
| **M42-WP5** | Benchmark & Base-Currency Contract | E | Portfolio Intelligence (Benchmark); **Base Currency owner unproven** | Benchmark; Portfolio Base Currency *(base-currency admission-blocked — RC-4)* |
| **M42-WP6** | Portfolio Lifecycle State Reuse & Provenance Contract | F | Ledger & Accounting | reuse-only *(no transition vocabulary — RC-2)* |
| **M42-WP7** | Portfolio Composition & Projection Contract *(terminal)* | G | Portfolio Intelligence | Portfolio Composition |

**M42-WP1 — Portfolio Canonical Vocabulary & Ownership Register.** The
foundation. Inventories every Portfolio coordinate, cites frozen owners, and
determines — it does not presuppose — the disposition of each §4.2 candidate
(`ADMIT` / `REUSE` / `RENAME` / `REJECT`). Each disposition is justified with
full Glossary/negative-corpus overlap analysis, V1–V3 analysis, single-owner
justification, and the candidate-level five-part gate. In particular WP1 must
**prove the owner** of Portfolio Policy (against Decision Intelligence's frozen
`M34-D-0007` territory) and Portfolio Base Currency (against Ledger &
Accounting's frozen identity boundary) before either may be admitted, and must
determine whether any belonging/evaluation predicate is admissible at all
(RC-3, RC-4). Admission and Glossary synchronization occur only at WP1's
confirmed Stage A gate; no later WP relies on a candidate before then.
Deliverable: candidate register + review chain + closeout.

**M42-WP2 — Portfolio Identity, Accounting Scope & Membership Contract.**
Canonicalizes the accounting-boundary leg by citation of frozen `M34-D-0002/
0003`. Freezes the boundary-integrity invariant (one scope per fact) and the
replay-never-crosses-a-boundary rule as a *stated contract*, authoring no new
accounting arithmetic (deferred to the frozen calculation rules). Reuse-only
vocabulary.

**M42-WP3 — Investment Universe Declaration Contract.** Contingent on WP1
confirming Investment Universe's `ADMIT` disposition, specifies the Universe as a
*descriptive declaration* of intended scope, composed from frozen
classification/capability/market/currency vocabulary. It **excludes** any
belonging predicate, evaluation, "not here" refusal, validation, or enforcement
semantics: those are verdict/enforcement, not descriptive coordinates (RC-3), and
may not be authored here. Any such predicate is admissible only through a
separate governed admission with an ownership and five-part-gate proof consistent
with `M34-D-0007`. Declaration semantics only; no enforcement engine.

**M42-WP4 — Portfolio Policy Declaration Contract *(admission-blocked)*.** MUST
NOT specify a Policy contract until WP1 has proven a single owner, the exact
permitted fields, and non-duplication of frozen Decision-Intelligence
policy/limit semantics (`M34-D-0007`, `OPTIMIZER_PHILOSOPHY.md`) (RC-4). Only on
that confirmed disposition does it specify the declared policy surface as
forward-binding data, drawing — as its load-bearing obligation — the
field-by-field boundary between M42 **declaration** and frozen
Decision-Intelligence **enforcement**, so no rule is owned twice (Law 9). If WP1
proves the concept is not distinctly ownable by Portfolio Intelligence, this WP
does not proceed.

**M42-WP5 — Benchmark & Base-Currency Contract.** Contingent on WP1 confirming
Benchmark's `ADMIT` disposition, specifies benchmark forms as declarations that
cite Market Intelligence series and never compute alpha/attribution (deferred).
**Portfolio Base Currency is admission-blocked**: this WP may specify it only if
WP1 first reconciles it against Ledger & Accounting's frozen identity/accounting
boundary and confirms a single owner and exact permitted fields (RC-4); once
owned, it is fixed as the unit of account whose change is an explicit recorded
event, never a silent reinterpretation of historical meaning.

**M42-WP6 — Portfolio Lifecycle State Reuse & Provenance Contract.**
**Reuse-only.** Reuses the frozen Portfolio Lifecycle State (`active`,
`archived`, `closed`) and its invariants — permanent identity, preservation of
history, future-only change — by citation of `M34-D-0002`, `M36-WP1-A01/A09`. It
authors **no** lifecycle-transition vocabulary or semantics; M36 deferred
lifecycle commands, workflows, runtime eligibility, and transition legitimacy,
so create/activate/clone/merge/import/export are out of scope here and, if ever
pursued, are routed through a separately-governed non-reuse admission (RC-2). It
fixes the provenance/lineage every portfolio-scoped fact carries, citing
Connectivity & Ingestion as provenance owner.

**M42-WP7 — Portfolio Composition & Projection Contract *(terminal)*.** Admits
Portfolio Composition; binds WP2–WP6 coordinates into one canonical, immutable,
serializable projection with composition determinism, canonical serialization,
identity independence from operational coordinates, and the no-derived-measure
invariant. Its confirmation is the precondition for M42 Epic Closeout.

---

## 7. Dependency Graph (Deliverable 7)

```text
                       M42-WP1
        Portfolio Canonical Vocabulary & Ownership Register
                     (foundation)
                          │  admits / disposition every coordinate
        ┌─────────────────┼───────────────────────────────┐
        ▼                 ▼                                ▼
   M42-WP2           M42-WP3, WP4, WP5                 M42-WP6
  Identity /        Universe · Policy ·              Lifecycle /
  Accounting        Benchmark · Base Ccy             Provenance
  Boundary          (declarative surface,            (events on
  (Ledger)           Portfolio Intelligence)          permanent id)
        │                 │                                │
        └────────┬────────┴────────────────┬──────────────┘
                 ▼                          ▼
                       M42-WP7  (terminal)
             Portfolio Composition & Projection
              binds all coordinates → one surface
                          │
                          ▼
                  M42 EPIC CLOSEOUT
        (whole-corpus reconciliation; Decision Log;
         Glossary sync verification; Graphify refresh)
```

**Ordering rules.**

- **WP1 gates everything.** No interior WP admits, specifies, or relies on a
  candidate noun before WP1's **Stage A register is independently confirmed** and
  the Glossary synchronized at that gate. Candidates marked admission-blocked
  (Portfolio Policy, Portfolio Base Currency, the belonging predicate) do not
  reach any WP contract until WP1 proves their owner and disposition; if a
  disposition resolves to `REJECT` or "not distinctly ownable," the dependent WP
  does not proceed.
- **WP2 precedes WP3–WP6.** The accounting boundary is the subject every other
  coordinate qualifies; belonging, policy, benchmark, and lifecycle all presume
  "this Accounting Scope."
- **WP3, WP4, WP5, WP6 are mutually independent** and may proceed in parallel
  after WP2, but each depends on WP1. WP4's declaration/enforcement boundary and
  WP5's benchmark-series citation are the two interior WPs with the highest
  external-boundary review load and should be scheduled with that in mind.
- **WP7 is terminal.** It composes only confirmed WP2–WP6 coordinates and adds
  no coordinate not traceable to a frozen or WP-confirmed authority.
- **Epic Closeout** follows WP7 confirmation and performs documentation-only
  reconciliation (Decision Log entry, Glossary-sync verification, Implementation
  Index update, Graphify refresh) — never new semantics.

No stage begins before its predecessor gate is confirmed. Epic Closeout cannot
infer or repair a WP ambiguity; an unresolved Portfolio-surface default blocks
the terminal WP's closeout.

---

## 8. Deferred Capabilities (Deliverable 8)

M42 founds the surface and stops. The following are explicitly **deferred to
future, separately-chartered milestones**, and M42 authorizes none of them:

| Deferred capability | Future home (constitutional domain) | Why deferred |
|---|---|---|
| Portfolio performance / return computation | Portfolio Intelligence | A derived measure; requires the frozen accounting rules over a composed surface — M42 provides the surface only. |
| Risk / drawdown / volatility / concentration analytics | Portfolio Intelligence | Derived measures; judged against declared policy tolerances M42 merely *declares*. |
| Attribution, recommendation grading, human-vs-AI | Portfolio Intelligence · Trust & Evaluation | Evaluation-plane machinery (Law 8); consumes the surface, never part of it. |
| Cross-Portfolio Exposure computation, net worth | Wealth Intelligence | Aggregation-as-interpretation above the single-portfolio boundary (frozen `M34-D-0003`). M42 stops at one boundary. |
| Optimization, rebalancing, position sizing, execution planning | Decision Intelligence | Judgment-layer action; M42 declares the envelope, the optimizer acts within it. |
| Order execution, trading | Decision Intelligence / Connectivity | Write-path action through the decision gate; M42 opens no gate. |
| Forecasting, AI recommendations | Decision Intelligence | Judgment substance (Law 7); M42 is truth-adjacent description only. |
| Tax computation | Wealth Intelligence | M42 declares wrapper/tax *context*; it computes no tax (Domain Model §5). |
| Provider-specific portfolio import logic | Connectivity & Ingestion | Edge logic (Law 10); M42's import/export are lifecycle *semantics*, not adapters. |
| Runtime, persistence schema, API/SDK/UI | Experience / infrastructure | M42 is specification-only, like every M39–M41 WP. |
| Merge/clone execution mechanics | Ledger & Accounting | M42 fixes the *semantics* (forward-only, mirrored events, no re-keying); the mechanics are a later runtime charter. |

Each deferral is a **description-not-surgery** promise: when the capability
arrives it consumes the frozen Portfolio Composition surface, adding vocabulary
and consumers at a domain edge, never editing the composition contract.

---

## 9. Risks and Architectural Considerations (Deliverable 9)

**R1 — Declaration/enforcement collision (highest risk).** Portfolio Policy
(M42, Portfolio Intelligence) and Portfolio Limits (frozen, Decision
Intelligence, `M34-D-0007`) both describe "constraints on a portfolio." If M42
lets Policy carry a *verdict* or an *enforcement algorithm*, it forks an owned
rule (Law 9) and reopens `M34-D-0007`. *Mitigation:* WP4's contract spine is a
field-by-field declaration-vs-enforcement gate; Policy states intent, the
optimizer's frozen constraint resolver enforces it; Independent Review rejects
any Policy field that computes a verdict.

**R2 — Accidental domain creation.** Calling M42 "the Portfolio domain" tempts a
tenth domain or a migration of frozen coordinates to a new "Portfolio" owner —
either of which is a Section-6 constitutional amendment done by drift (forbidden
by §10, G2, G4). *Mitigation:* §0 and §3 fix that M42 creates no domain and
moves no boundary; every coordinate keeps its frozen owner; the terminal
Composition is *owned by Portfolio Intelligence*, an existing domain.

**R3 — Measure leakage into the composition.** A Portfolio Composition that
carries even one convenience number (a NAV, a weight, a return) breaks the
truth/judgment wall the milestone exists to protect. *Mitigation:* the
no-derived-measure invariant is a WP7 acceptance criterion and a negative-corpus
row; Independent Review confirms the projection carries only identity, boundary,
declaration, lifecycle, and lineage.

**R4 — Reopening frozen M34/M36 vocabulary.** M42 touches nine frozen terms; a
careless re-definition of Accounting Scope or Lifecycle State would violate
non-reopening. *Mitigation:* WP2/WP6 are *reuse-only*; every frozen term is
cited, never re-authored; the register (WP1) marks each as `REUSE` with its
governing ADR.

**R5 — Universe/classification coupling.** Investment Universe is composed from
Asset Foundation classification; if its scope declaration hardcodes today's
taxonomy, it inherits exactly the type-branching failure the platform rejected
(Domain Model §4, constitution §2.3). *Mitigation:* WP3 intentionally excludes
belonging, evaluation, refusal, validation, and enforcement semantics, and
specifies the Universe *declaration* as *described* over capability/
classification vocabulary, so a new asset class fits existing universe
declarations without redesign.

**R6 — Base-currency reinterpretation hazard.** Treating Base Currency as a
mutable display setting would silently rewrite the meaning of every historical
number. *Mitigation:* WP5 fixes Base Currency as an explicit recorded event,
not a preference, consistent with immutability (Law 2).

**R7 — Wealth-boundary bleed.** Aggregation-as-interpretation (net worth,
exposure) is Wealth Intelligence's frozen territory; M42 must stop at one
boundary or it reopens `M34-D-0003`. *Mitigation:* §8 defers all cross-boundary
interpretation; the Composition projects exactly one Accounting Scope.

**R8 — Corpus fatigue / scope compression.** Seven governed WPs is a large
review load; the temptation is to merge WPs or skip stages. *Mitigation:* WP3/
WP4/WP5/WP6 are parallelizable after WP2; the roadmap (§11) sequences the
external-boundary-heavy WPs deliberately; no stage may be skipped, as with every
prior milestone.

---

## 10. Future Milestone Alignment (Deliverable 10)

M42 is positioned as the Portfolio-domain foundation immediately after the
Market-measure foundation (M40–M41) and immediately before the analytics and
wealth eras (constitution §9 / ROADMAP Phases 3–6):

- **M39 → M40/M41 → M42** completes the *Knowledge-layer foundations trilogy*:
  canonical Observation (what the world reports), canonical Measure (what we
  compute about it), canonical Portfolio (what it is *for*). Each is vocabulary
  and composition frozen before the engines that consume it.
- **M43+ (anticipated) — Portfolio Analytics Foundation.** The first consumer of
  M42's Composition: performance/risk/attribution as Portfolio Intelligence
  derived measures over the frozen surface — pure *description* of the deferred
  §8 analytics, added without editing the composition contract.
- **Phase 5 — Wealth.** Wealth Intelligence's Cross-Portfolio Exposure and net
  worth aggregate *many* M42 Compositions; Goal Target binds to a portfolio's
  declared strategy. M42's single-boundary discipline is exactly what makes the
  aggregation honest.
- **Phase 6 — AI Wealth Advisor.** Decision Intelligence consumes the declared
  Universe/Policy/Benchmark as the envelope every recommendation must fit; Trust
  & Evaluation grades per-portfolio against the declared Benchmark. Both read
  M42; neither edits it.

The alignment test the constitution demands (§9) holds: every downstream era
adds vocabulary and consumers at a domain edge over M42's invariant surface —
description, not surgery.

---

## 11. Recommended Implementation Roadmap (Deliverable 11)

Implementation-neutral throughout: "implementation" here means the governed
*specification* sequence, not code. Each step is gated by the previous step's
unconditional confirmation.

1. **Independent review of this Architecture Proposal.** Resolve every required
   architecture correction individually; obtain unconditional Independent
   Architecture Confirmation; **freeze the M42 Architecture.**
2. **M42-WP1 — Vocabulary & Ownership Register.** Run WP1's own per-artifact
   sequence: Architecture → confirm; **Stage A Candidate Vocabulary Register** →
   Independent Review → corrections → unconditional Confirmation. Each candidate
   is dispositioned on its merits — `ADMIT` / `REUSE` / `RENAME` / `REJECT` —
   with the owner of Portfolio Policy and Portfolio Base Currency, and the
   admissibility of any belonging predicate, **proven** before any `ADMIT`.
   **Glossary synchronization applies only to candidates confirmed `ADMIT`**, in
   the same change as the Stage A confirmation; reuse rows record their frozen
   ADRs; blocked or rejected candidates are synchronized nothing. **Gate: no
   interior WP begins until WP1's Stage A is confirmed and synchronized.**
3. **M42-WP2 — Identity/Accounting Boundary Contract.** Reuse-only; freeze the
   boundary-integrity contract by citation. Confirm.
4. **M42-WP3, WP4, WP5, WP6 — the declarative + lifecycle surface (parallelizable
   after WP2).** Each WP proceeds **only for candidates WP1 confirmed** and runs
   the full per-artifact sequence: Architecture → confirm → Stage A register
   (reuse or confirmed-WP1 admission only) → confirm → Stage B contract with
   field-level five-part gate → confirm → closeout, with independent review and
   correction handling at each gate. **WP3** specifies the Investment Universe
   *declaration only* — no belonging/refusal predicate (RC-3). **WP6** is
   reuse-only — the frozen Lifecycle State and its invariants, no transition
   vocabulary (RC-2). **WP4 (Policy)** and the **Base-Currency leg of WP5** do
   **not** begin until WP1 has proven their owner; if unproven they are
   withheld (RC-4). Recommended sequencing given review load: **WP3** and **WP6**
   first (lower external-boundary risk), then **WP5 (Benchmark)** and, if
   unblocked, **WP4** with dedicated declaration/enforcement review.
5. **M42-WP7 — Portfolio Composition & Projection (terminal).** Draft in
   dependency order: Composition binding → serialization/identity → composition
   determinism → no-derived-measure proof → lineage completeness → integrated
   golden-vector matrix, gate table, and compatibility proof against §0
   authorities. Independent architectural + serialization/identity review;
   resolve to zero open findings; **freeze.**
6. **M42 Epic Closeout.** Whole-corpus reconciliation across WP1–WP7: verify the
   five-part gate held, that no derived measure entered any composition, that no
   frozen M34/M36/M39/M41 term was re-authored, and that no negative-corpus item
   reappeared. Record the consolidated Decision Log entry, update the
   Implementation Index, and refresh Graphify **only after** the Epic Closeout is
   itself independently reviewed and any correction confirmed.

**Validation evidence is specification-only** at every step — golden-vector
data fixtures and documented derivations, no committed test runner, reference
implementation, or Composition-building code (corpus convention, M41 §8).

---

## Explicit Non-Goals (negative corpus)

M42 does **not**, in any WP:

- compute performance, return, alpha, drawdown, volatility, risk, concentration,
  attribution, exposure, or net worth;
- perform optimization, rebalancing, position sizing, or execution/order
  planning;
- forecast, recommend, rank, score trust, or judge suitability;
- author any belonging/evaluation/refusal/validation/enforcement predicate that
  *decides whether an instrument belongs* — that is a verdict, not a descriptive
  coordinate (RC-3);
- author any lifecycle-transition vocabulary, command, workflow, or transition-
  legitimacy semantics (create/activate/clone/merge/import/export), which M36
  deferred (RC-2);
- treat any §4.2 candidate as admitted, owned, or Glossary-synchronized before
  its confirmed WP1 Stage A disposition, or admit an admission-blocked candidate
  (Portfolio Policy, Portfolio Base Currency, belonging predicate) before its
  owner is proven (RC-1, RC-4);
- compute tax, or apply wrapper qualification arithmetic;
- contain provider, broker, or format knowledge, or any import adapter;
- author accounting arithmetic (frozen in `PORTFOLIO_CALCULATION_RULES.md`) or
  reopen `M34-D-0002/0003/0007`, M36, M39, or M40–M41;
- create a tenth constitutional domain or migrate any frozen coordinate to a new
  owner;
- carry any derived measure on the Portfolio Composition;
- implement a module, schema, endpoint, runtime, or persistence;
- author any committed executable validation artifact; or
- update the Decision Log or refresh Graphify before Epic Closeout.

Independent Review must confirm the negative corpus holds across every WP.

---

## Acceptance Criteria

This proposal is architecturally acceptable only if Independent Review confirms:

1. Scope founds the canonical Portfolio semantic surface and reopens no part of
   M34, M36, M39, M40, or M41.
2. No new constitutional domain is created; every frozen coordinate keeps its
   frozen owner; the terminal Composition is owned by the existing Portfolio
   Intelligence domain.
3. No candidate noun (§4.2) is treated as admitted, owned, or synchronized in
   advance; each is dispositioned only through the governed per-artifact sequence
   (Architecture → Stage A → Stage B, each independently confirmed before the
   next), with owner proven before `ADMIT`, and no WP relies on a candidate
   before its confirmed WP1 Stage A disposition.
4. The owner of Portfolio Policy (vs. frozen Decision-Intelligence `M34-D-0007`)
   and of Portfolio Base Currency (vs. Ledger & Accounting's frozen identity
   boundary) is proven by WP1 before either is admitted; where Policy is owned,
   its declaration/enforcement boundary against Portfolio Limits is explicit and
   forks no owned rule (Law 9).
5. The Portfolio Composition carries no derived measure and no ambient default.
6. Boundary integrity (one Accounting Scope per fact) and replay-never-crosses-
   a-boundary are stated as contracts, authoring no new accounting arithmetic.
7. The seven-WP decomposition and dependency graph are sufficient for
   independent review and incremental, gated implementation.
8. Every deferred capability (§8) has a named future home and a description-not-
   surgery path.
9. Implementation, runtime, provider, persistence, API, production, and
   executable-validation authority remain `NONE`.

---

## Repository and Governance Effects

This proposal creates only:

- `docs/implementation/M42_ARCHITECTURE_PROPOSAL.md` (this document).

It modifies no frozen artifact, no domain constitution, `docs/GLOSSARY.md`, the
Decision Log, the Implementation Index, Graphify output, or source code. Per the
frozen corpus convention, Glossary synchronization is WP1 work (on confirmation)
and Decision Log reconciliation plus Graphify refresh are Epic Closeout work.
Creating this proposal is authority to perform none of those.

---

## Final Architectural Boundary

M42 begins with the frozen, multi-domain-owned Portfolio coordinates that M34
and M36 established and the descriptive Portfolio Domain Model that has never
been frozen. It ends with a fully-governed **canonical Portfolio semantic
foundation** — identity and accounting boundary, declared Investment Universe,
Portfolio Policy, Benchmark, and Base Currency, lifecycle and provenance, and
one deterministic Portfolio Composition projection binding them all — carrying
no derived measure, no ambient default, and no ownership migration.

It changes no upstream contract and creates no downstream authority. Its
decisive completion test is that two independent readers, given the same frozen
coordinates and the M42 contracts, derive the same Portfolio Composition, the
same boundary resolution, and the same declaration semantics — without
consulting a clock, a provider, a live authority, an analytics engine, or an
unstated convention.

---

## Final Status

**READY FOR INDEPENDENT ARCHITECTURE REVIEW**
