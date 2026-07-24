# M42-WP1 — Portfolio Canonical Vocabulary and Ownership Register

**Date:** 2026-07-24

**Milestone:** M42 — Portfolio Intelligence Foundation (Canonical Portfolio Domain)

**Document class:** Constitutional candidate-vocabulary and ownership register

**Workflow stage:** Stage 1 of the governed per-artifact sequence (Architecture
→ **Stage A Candidate Vocabulary Register** → Stage B Contract Specification →
Closeout), each independently reviewed, corrected where required, and
independently confirmed before the next stage begins — the same sequence
M40-WP1/WP2 and M41-WP1..WP4 ran. This document is the Stage A register. It
precedes, and is a precondition for, any M42-WP2..WP7 contract text, none of
which begins until this register is independently reviewed, corrected if
required, and independently confirmed. This revision resolves the seven
required corrections (RC-1 through RC-7) returned by Independent Review —
`APPROVED WITH REQUIRED CORRECTIONS` — per §0.1, plus two remaining
consistency corrections Independent Confirmation review identified (stale
`REUSE` references to Portfolio Base Currency in downstream planning
documents; residual "scope predicate" wording in the Investment Universe
five-part gate table), and is submitted for Independent Confirmation. No
disposition in this register is confirmed, canonical, or reliable until a
separate Independent Confirmation record states that this stage has passed.

**Status:** `READY_FOR_INDEPENDENT_CONFIRMATION`

**Canonical vocabulary admission:** `NONE`

**Implementation authority:** `NONE`

**Runtime authority:** `NONE`

**Production method authority:** `NONE`

**Provider authority:** `NONE`

**Persistence authority:** `NONE`

**API and public-exposure authority:** `NONE`

**Decision Log status:** `NOT_SUBMITTED`

**Supersedes:** `NONE`

**Closeout:** `NONE`

**Architecture phase:** Produced under the
[M42 Architecture Proposal](M42_ARCHITECTURE_PROPOSAL.md), whose own Final
Status line records `READY FOR INDEPENDENT ARCHITECTURE REVIEW`. This register
is authored on the instruction that a separate architecture-review session has
since independently reviewed, required-corrected, and independently confirmed
that proposal, freezing it. **That review, correction, and confirmation are
not yet recorded as committed artifacts in this repository** — no
`M42_ARCHITECTURE_INDEPENDENT_REVIEW.md` or
`M42_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` exists alongside the proposal,
unlike the paired record M41's architecture phase left behind
([M41_ARCHITECTURE_INDEPENDENT_REVIEW.md](M41_ARCHITECTURE_INDEPENDENT_REVIEW.md),
[M41_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md](M41_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md)).
Per this repository's own governance discipline (G5 — "each level amends by
its own mechanism," [platform_architecture.md §11](../architecture/platform_architecture.md#11-architecture-governance)),
a confirmation that exists only as an assertion in a chat session and not as a
committed record is not yet a citable authority. **This register is written to
be consistent with the proposal exactly as committed** (§0–§11 as read from
`M42_ARCHITECTURE_PROPOSAL.md` on disk) and does not rely on any correction the
absent review might have required. Closing that gap — committing the
Independent Review and Independent Confirmation artifacts for the M42
Architecture Proposal — is a repository-hygiene precondition this register
flags but does not itself satisfy; see §7.

**Document role:** The complete candidate-vocabulary and ownership register
required by the M42 architecture proposal's Component A (§5) and M42-WP1's own
charter (§6, §11 step 2): *"M42-WP1 — Portfolio Canonical Vocabulary &
Ownership Register... Inventories every Portfolio coordinate, cites frozen
owners, and determines — it does not presuppose — the disposition of each §4.2
candidate (`ADMIT` / `REUSE` / `RENAME` / `REJECT`)... In particular WP1 must
prove the owner of Portfolio Policy... and Portfolio Base Currency... before
either may be admitted, and must determine whether any belonging/evaluation
predicate is admissible at all."* This document is that register. It creates
no contract text for any of Components B–G and does not begin M42-WP2's,
WP3's, WP4's, WP5's, WP6's, or WP7's own specification, all of which are
conditional on this register's independent confirmation.

**Normative language:** `MUST`, `MUST NOT`, `SHALL`, `SHALL NOT`, `MAY`, and
`SHOULD` are normative within this register. They constrain what the
independent reviewer may consider for disposition; they do not themselves
admit vocabulary, synchronize `GLOSSARY.md`, or authorize implementation,
runtime use, persistence, provider integration, an API, or a production
method.

---

## 0.1 Corrections Applied (Independent Review Response)

Independent Review returned `APPROVED WITH REQUIRED CORRECTIONS` with seven
findings, RC-1 through RC-7. This revision resolves each with the smallest
change that logically follows from the finding. No disposition changes except
where a finding forced it (Benchmark, Portfolio Base Currency); every other
disposition — Investment Universe `ADMIT`, Portfolio Policy `REJECT`,
Portfolio Composition `ADMIT`, Investment Universe Membership `REJECT` — is
preserved.

| Finding | Disposition changed? | Resolution |
| --- | --- | --- |
| RC-1 — Benchmark V1 collision with Market Intelligence's frozen "Benchmark" observation type (`MARKET_DATA_PLATFORM.md` §7, `PROVIDER_INTERFACE.md`) | Yes — `ADMIT` → `RENAME` | Candidate renamed to **Portfolio Benchmark Declaration**, never abbreviated to bare "Benchmark," with an explicit non-collision note against Market Intelligence's canonical Benchmark observation type. See §6.3. |
| RC-2 — Policy-derived form's "target-allocation weights" input not proven owned by Portfolio Strategy Metadata | Yes — one of five forms narrowed | The Policy-derived form is withheld from this admission pending a future, separately proven ownership of target-allocation weights; the candidate is confirmed for its four remaining forms (Single, Composite, Category, None) only. See §6.3. |
| RC-3 — Portfolio Base Currency REUSE asserted rather than proved | Yes — `REUSE` → `ADMIT` (Ledger & Accounting) | The candidate is now admitted as a new field-level coordinate on its own five-part-gate proof, rather than claimed as silently already included in `M34-D-0002`. Owner and consequence (Ledger & Accounting; not a Portfolio Intelligence coordinate) are unchanged. See §6.4. |
| RC-4 — Incomplete candidate records (Portfolio Policy, Portfolio Base Currency, Investment Universe Membership missing required fields) | No | Missing Non-owner / Permitted inputs / Forbidden inputs / Proposed exact definition / Constitutional constraints fields added to all three entries. See §6.2, §6.4, §6.6. |
| RC-5 — Five-part gate misapplied to both `REJECT` candidates | No | Gate tables corrected: Portfolio Policy's REJECT is restated as resting on the V1 single-owner failure and frozen-ownership overlap, not a misstated permitted-subject failure; Investment Universe Membership's REJECT is restated as resting solely on the output-meaning verdict prohibition, with the suitability analogy removed. See §6.2, §6.6. |
| RC-6 — Portfolio Policy's settlement/fractional/tax field-level ownership overclaimed | No | Settlement discipline's owner is restated as unresolved among Ledger & Accounting, Asset Foundation's frozen Settlement Semantics, and Decision Intelligence — immaterial to the REJECT either way. Fractional-trading permission and tax/wrapper context ownership is restated as unresolved and undecided by this register, not assigned to Portfolio Strategy Metadata by silence. See §6.2. |
| RC-7 — Investment Universe declaration/verdict boundary internally ambiguous | No | Purpose and Proposed exact definition reworded to remove predicate/evaluation language; "scope predicates" renamed "scope criteria," defined as inert declarative data, never an executable or truth-valued function; an explicit constitutional constraint added forbidding any evaluation capability. See §6.1. |

---

## 1. Purpose

This register assembles, in one place and before any M42 contract
specification text is written, every noun the M42 Architecture Proposal names
across §4.1 (reused, frozen) and §4.2 (candidate, new): its single owning
domain (proven, not assumed), an overlap analysis against every plausibly
adjacent `GLOSSARY.md` entry, a canonical-reuse analysis, a negative-corpus
analysis against the frozen M34/M36/M39–M41 negative corpus so far as it
touches Portfolio-adjacent territory, a V1–V3 constitutional-compatibility
analysis, and an explicit disposition request (`ADMIT`, `REUSE`, `RENAME`, or
`REJECT`).

This satisfies the M42 Architecture Proposal's own precondition — restated at
§6: *"WP1 gates everything. No interior WP admits, specifies, or relies on a
candidate noun before WP1's Stage A register is independently confirmed and
the Glossary synchronized at that gate"* — and Component A (§5): *"The
whole-domain admission/reuse/reject register: every Portfolio coordinate
mapped to exactly one owner, frozen terms cited and new candidates
dispositioned per §4."* No candidate in this register is canonical, admitted,
or reusable by any downstream artifact until it independently completes
review and confirmation.

## 2. Governing Authority

This register is subordinate to repository authority. Where this document
conflicts with an approved or frozen authority, that authority governs and the
conflicting M42 candidate is inadmissible.

The governing corpus is:

- [Platform Architecture](../architecture/platform_architecture.md), especially
  §6 (Platform Domains), §7 (Domain Relationships), §11 (Architecture
  Governance), and §12 (Canonical Vocabulary: V1 one term/one meaning/one home,
  V2 same-change synchronization, V3 constitutional terms are reserved);
- [Canonical Glossary](../GLOSSARY.md) in its complete current state, in
  particular the frozen Portfolio-adjacent entries: Portfolio Identity,
  Accounting Scope, Portfolio Lifecycle State, Portfolio Strategy Metadata,
  Goal Target, Current Selection, Portfolio Membership, Cross-Portfolio
  Aggregation, Cross-Portfolio Exposure, Decision Policy, Portfolio Limits,
  Sector Limits, and Portfolio Status;
- the frozen M34 Decision Register entries `M34-D-0002`, `M34-D-0003`, and
  `M34-D-0007`, and `ADR-004`;
- the frozen M36 corpus (`M36-WP1-A01`, `M36-WP1-A09`) governing Portfolio
  Lifecycle State;
- the domain constitutions
  [OPTIMIZER_PHILOSOPHY.md](../investment/OPTIMIZER_PHILOSOPHY.md) (Decision
  Intelligence) and
  [PORTFOLIO_CALCULATION_RULES.md](../investment/PORTFOLIO_CALCULATION_RULES.md)
  (frozen accounting semantics);
- the [Portfolio Domain Model](../architecture/PORTFOLIO_DOMAIN_MODEL.md), a
  Level-4 design-of-record this register admits vocabulary *from* but which is
  not itself frozen or canonical; and
- the [M42 Architecture Proposal](M42_ARCHITECTURE_PROPOSAL.md), asserted
  independently confirmed per this document's front matter, with the
  outstanding artifact-commit gap noted there and at §7.

### 2.1 Authority order

The following order resolves any apparent conflict:

1. repository constitution, approved Decision Register decisions, and the
   Canonical Glossary;
2. frozen milestone specifications and closeouts (M29–M41);
3. the M42 architecture (as asserted confirmed; see front matter caveat);
4. this WP1 register; and
5. any future M42 work-package contract text.

No lower item may reinterpret, weaken, or silently narrow a higher item.

### 2.2 Admission boundary

This register is complete as a Stage A deliverable, but no entry in it is
canonical. Every candidate MUST pass independent review, any required
correction, and independent confirmation before Glossary synchronization and
downstream reliance. Until a candidate's disposition is independently
confirmed:

- no candidate term SHALL be added to `GLOSSARY.md`;
- no downstream artifact — including M42-WP2..WP7's own contract text — SHALL
  claim a candidate term is canonical or rely on it;
- no schema, module, service, registry, adapter, endpoint, persistence model,
  or production method SHALL be justified by this register; and
- examples, names, and constraints in this register SHALL NOT be treated as
  runtime behavior.

## 3. Scope

This register governs candidate semantic meaning, ownership, overlap analysis,
negative-corpus analysis, constitutional compatibility, and disposition
requests for every noun the M42 architecture's §4.1 and §4.2 name. It does not
govern:

- the Identity/Accounting-Boundary, Investment-Universe, Policy, Benchmark/
  Base-Currency, Lifecycle/Provenance, or Composition/Projection contract text
  itself (deferred to M42-WP2..WP7, and only for candidates this register
  confirms `ADMIT`);
- validation rules, constraint-resolution mechanics, or optimizer behavior
  (Decision Intelligence's own territory, unowned by M42);
- accounting arithmetic, NAV/return formulas, or cost-basis rules (frozen in
  `PORTFOLIO_CALCULATION_RULES.md`);
- software design, implementation, runtime, persistence, provider, or API
  behavior; and
- Decision Log reconciliation or Graphify refresh, both reserved to Epic
  Closeout.

Naming a noun in this register specifies candidate meaning only. It authorizes
no work-package contract text, schema, or executable process.

## 4. Frozen Ownership Baseline

This register inherits, without amendment, the frozen ownership baseline the
M42 Architecture Proposal itself states at §4.1 and §3, sourced from
`M34-D-0002`, `M34-D-0003`, `M36-WP1-A01/A09`, and the current `GLOSSARY.md`.

| Coordinate | Sole owner | Governing authority | Register preservation rule |
| --- | --- | --- | --- |
| Portfolio Identity | Ledger & Accounting | `M34-D-0002` | Cited by reference; establishes accounting identity only — never strategy, goals, decision policy, analytics, or UI selection |
| Accounting Scope | Ledger & Accounting | `M34-D-0002` | Cited by reference; every semantic projection of one portfolio refers to the same scope |
| Portfolio Membership | Ledger & Accounting | `M34-D-0003` | Cited by reference; a Ledger fact, not an investment interpretation |
| Cross-Portfolio Aggregation | Ledger & Accounting | `M34-D-0003` | Cited by reference; adds no investment meaning |
| Portfolio Lifecycle State | Ledger & Accounting | `M34-D-0002`, `M36-WP1-A01`, `M36-WP1-A09` | Cited by reference; qualifies what a portfolio may do next, never rewrites Identity, Accounting Scope, ledger history, or evaluation history; carries no transition-command vocabulary (RC-2, §6.6 below) |
| Portfolio Strategy Metadata | Portfolio Intelligence | `M34-D-0002`, `M34-D-0007` | Cited by reference; excludes Goal Target, Decision Policy, and accounting truth |
| Decision Policy | Decision Intelligence | `M34-D-0007` | Cited by reference; policy envelopes, optimization rules, decision constraints, execution preferences, and optimizer behavior — may reference Goal Target and Portfolio Strategy Metadata but owns neither |
| Portfolio Limits / Sector Limits | Decision Intelligence | `M34-D-0004`, `M34-D-0007` | Cited by reference; constraints on portfolio composition and optimization, not Portfolio Identity or Accounting Scope |
| Goal Target / Cross-Portfolio Exposure | Wealth Intelligence | `M34-D-0002/0003/0007` | Cited by reference; strategy and policy may reference Goal Target but do not own it |
| Current Selection | Experience Platform | `M34-D-0002` | Cited by reference; has no business meaning and never establishes Portfolio Identity or Accounting Scope |
| Portfolio Status | Portfolio Intelligence | `M34-D-0009` | Cited by reference; a source-domain status, not aggregate Operations truth |

Every semantic concept in this register SHALL have exactly one owner.
Custody, reference, transport, display, storage, execution, or evaluation
SHALL NOT create shared ownership. No row in this table is reopened,
reinterpreted, or extended by this register: each is cited exactly as
`GLOSSARY.md` and its governing ADR state it today.

## 5. Register Record Fields

Each candidate entry in §6 uses the following fields, mirroring the fields
M40-WP1 and M41-WP1 established for this exact purpose:

| Field | Required interpretation |
| --- | --- |
| Purpose | The constitutional reason the candidate concept exists |
| Owner | The single proposed semantic owner — proven, not merely proposed |
| Non-owner | Domains or mechanisms that may reference or carry the concept but cannot define or reinterpret it |
| Permitted inputs | Categories that may contribute to the concept's semantic claim |
| Forbidden inputs | Categories whose presence makes the candidate inadmissible |
| Proposed exact definition | The exact semantic claim the term would make if admitted |
| Constitutional constraints | Mechanically reviewable invariants the disposition must preserve |
| Overlap analysis | Comparison against every existing `GLOSSARY.md` entry with a plausible naming or meaning collision |
| Canonical reuse analysis | Whether an existing canonical term already covers this meaning, in whole or in part |
| Negative corpus analysis | Comparison against the frozen negative corpus this register's territory touches — Decision Intelligence's judgment/enforcement vocabulary (forecast, recommendation, signal, verdict, constraint), Wealth Intelligence's aggregation-as-interpretation, and any re-authored accounting arithmetic |
| V1–V3 disposition | Whether the candidate satisfies Platform Architecture §12 V1 (one term, one meaning, one home), V2 (same-change synchronization, deferred to confirmation), and V3 (constitutional-term reservation) |
| M34/M36 compatibility | Explicit compatibility check against `M34-D-0002/0003/0007`, `M36-WP1-A01/A09` |
| Five-part ownership-boundary gate (current) | The candidate-level pass/fail result, recorded now, against the M42 architecture's own five-part gate (§4.3 of the proposal: permitted subject; permitted inputs; output meaning; prohibited live/ambient inputs; prohibited judgment semantics) — decided from the candidate's own Purpose, Owner, Permitted/Forbidden inputs, and Proposed exact definition fields, not from unwritten future contract text |
| Disposition request | Exactly one of `ADMIT`, `REUSE`, `RENAME`, `REJECT` |
| Glossary synchronization requirement | What `GLOSSARY.md` change, if any, this disposition would require — performed only after independent confirmation |
| Future contract acceptance evidence | What a future WP2–WP7 contract specification, once this candidate is independently confirmed, must additionally supply. This is a downstream work-package obligation, not a precondition for this candidate's present disposition |

"Permitted" means constitutionally eligible for future candidacy. It does not
mean available, implemented, supported, or authorized for runtime use.

## 6. Candidate Vocabulary and Ownership Register

### 6.0 Complete Noun Inventory

The M42 architecture proposal §4.2 names six candidates. This section
inventories all six and classifies each as `ADMIT`, `REUSE`, `REJECT`, or
ordinary non-canonical contract language, before the full disposition record
for each follows at §6.1–§6.6.

| Noun | Source | Classification | Reasoning |
| --- | --- | --- | --- |
| Investment Universe (declarative definition only) | Proposal §4.2, §6 (WP3) | `ADMIT` candidate | Registered at §6.1 — a named specialization within the already-frozen Portfolio Strategy Metadata umbrella (Portfolio Intelligence, `M34-D-0002`/`M34-D-0007`), not a sibling new umbrella |
| Portfolio Policy | Proposal §4.2, §6 (WP4) | `REJECT` | Registered at §6.2 — not distinctly ownable by Portfolio Intelligence as a single noun; three fields (allowed markets/classes/currencies, leverage, cash requirement) are proven Decision Policy / Portfolio Limits territory (`M34-D-0007`); the remaining fields' ownership is unresolved and left undecided (RC-6), which V1 forbids assembling under one new owner regardless |
| Benchmark | Proposal §4.2, §6 (WP5) | `RENAME` candidate | Registered at §6.3 as **Portfolio Benchmark Declaration** (RC-1 — bare "Benchmark" collides with Market Intelligence's frozen canonical observation type, `MARKET_DATA_PLATFORM.md` §7); Policy-derived form withheld (RC-2) |
| Portfolio Base Currency | Proposal §4.2, §6 (WP5) | `ADMIT` candidate | Registered at §6.4 — a new coordinate proven owned by Ledger & Accounting on this register's own five-part-gate proof (RC-3 — not silently already included in `M34-D-0002`); not a Portfolio Intelligence coordinate |
| Portfolio Composition | Proposal §4.2, §6 (WP7) | `ADMIT` candidate | Registered at §6.5 — registered now per Component A's whole-domain scope; its field-level contract remains WP7's terminal obligation |
| Investment Universe Membership (belonging predicate) | Proposal §4.2, §6 (WP3 exclusion) | `REJECT` | Registered at §6.6 — verdict/enforcement semantics, not a descriptive coordinate; inadmissible to Portfolio Intelligence under this milestone at all |

This inventory accounts for every noun the confirmed §4.2 candidate table
names. No additional vocabulary is proposed beyond what §4.2 already lists;
this register neither narrows nor widens the proposal's own candidate set.

---

### 6.1 Investment Universe (declarative definition only)

**Purpose:** Name, as a first-class portfolio-level object, the declared
scope of what a portfolio's strategy intends to hold — composed from existing
Asset Foundation classification, capability, market, and currency vocabulary
— stated once as inert, declarative data rather than re-legislated as a type
whitelist per portfolio or per asset class (Portfolio Domain Model §4). The
declaration states scope; it evaluates nothing and asks no question of any
instrument (RC-7 — see Constitutional constraints below for the resulting
boundary against Investment Universe Membership, §6.6).

**Owner:** Portfolio Intelligence, as a **named specialization within the
already-frozen Portfolio Strategy Metadata allocation** (`GLOSSARY.md`:
"Metadata describing a portfolio as an investment-strategy container... Owned
by Portfolio Intelligence... excludes Goal Target, Decision Policy, and
accounting truth," governed by `M34-D-0002` and `M34-D-0007`). Portfolio
Strategy Metadata's frozen definition excludes only Goal Target, Decision
Policy, and accounting truth — it does not exclude a declared universe, and
nothing in its frozen text forecloses naming one of its own coordinates
precisely. Investment Universe is therefore not a sibling umbrella beside
Portfolio Strategy Metadata; it is the first named, precisely defined
coordinate *within* it, exactly as Market Measure Definition (M41-WP1 §6.1)
was admitted as a named coordinate within the already-admitted Market Measure
umbrella rather than a new umbrella of its own.

**Non-owner:** Asset Foundation (owns the classification, capability, market,
and currency vocabulary Investment Universe is *composed from*, never
re-owned or reclassified here); Ledger & Accounting; Decision Intelligence;
Wealth Intelligence; Experience Platform; providers, storage, and runtime
mechanisms.

**Permitted inputs:**

- an explicit declared name (e.g. "Thai Equity," "Retirement," "Custom");
- explicit declared scope **criteria** — inert, non-executable data values
  composed only from already-owned Asset Foundation vocabulary: asset
  type/classification, capability, market, and currency (Portfolio Domain
  Model §4); and
- a reference to the Portfolio Identity / Accounting Scope the universe
  declaration belongs to (§4 baseline; cited, not redefined).

**Forbidden inputs:**

- any evaluation function, refusal, "not here" determination, validation
  routine, or belonging-verdict predicate applied against an instrument —
  that capability, whatever it would be called, is Investment Universe
  Membership (§6.6), explicitly excluded from this candidate and, under this
  register, inadmissible in its own right;
- Ledger, Decision, or Wealth meaning (accounting truth, decision constraint,
  or goal target);
- a concrete instrument list maintained independently of the declared scope
  criteria (the universe declares *scope*, never enumerates *membership* as
  a stored fact); and
- an ambient or ungoverned default scope.

**Proposed exact definition (corrected, RC-7):** An Investment Universe is a
named, immutable-until-explicitly-revised, portfolio-scoped **declaration**
of the intended scope of holdings for one Portfolio Identity, composed
exclusively from already-owned Asset Foundation classification, capability,
market, and currency vocabulary. Its scope criteria are inert data — closed
sets and ranges over already-owned vocabulary — never an executable
function, a truth-valued predicate, or anything capable of being *evaluated*
against a specific instrument. It is a descriptive strategy fact, not an
accounting fact, and not an enforcement constraint. It answers no question
about, and produces no result for, any instrument; whether a specific
instrument satisfies the declared scope criteria is a distinct, separately
named capability — Investment Universe Membership (§6.6) — which this
register finds inadmissible in its own right, so no such evaluation exists
anywhere under confirmation of this candidate.

**Constitutional constraints (RC-7 boundary, corrected):**

- It MUST reference only already-owned Asset Foundation vocabulary; it MUST
  NOT hardcode a taxonomy that a future asset class would require re-
  legislating (Portfolio Domain Model §4; constitution §2.3).
- It MUST be expressed only as inert declarative data (named criteria, closed
  sets, ranges); it MUST NOT be specified, described, or implemented as an
  executable function, a truth-valued predicate, or any construct capable of
  producing a verdict about a specific instrument. A future contract that
  gives Investment Universe an evaluation capability of any kind is not this
  candidate — it is Investment Universe Membership, separately inadmissible
  under §6.6.
- It MUST be scoped to exactly one Portfolio Identity / Accounting Scope; it
  MUST NOT be shared or ambient across portfolios.
- It MUST NOT be confused with, or offered as a substitute for, the broader
  Portfolio Strategy Metadata coordinate it specializes; the register (WP1)
  states the specialization explicitly so a future reader does not treat
  Investment Universe as a second, competing strategy-metadata concept.

**Five-part ownership-boundary gate (current):**

| Part | Result | Reasoning |
| --- | --- | --- |
| Permitted subject | Pass | Subject is one Portfolio Identity's declared scope of intended holdings; no cross-portfolio or ambient subject |
| Permitted inputs | Pass | Inputs are limited to a declared name and declarative scope criteria composed from already-owned Asset Foundation vocabulary, plus a Portfolio Identity reference |
| Output meaning | Pass | Output meaning is limited to a named, immutable-until-revised scope declaration — no verdict, no computed measure |
| Prohibited inputs | Pass | No live provider answer, wall-clock, cross-portfolio state, or model output appears in the proposed exact definition |
| Prohibited semantics | Pass | Forbidden-inputs field expressly excludes any belonging/evaluation/refusal/validation predicate, and no performance, risk, or recommendation meaning appears |

**Overlap analysis:** `GLOSSARY.md` contains **Portfolio Strategy Metadata**
("Metadata describing a portfolio as an investment-strategy container...
excludes Goal Target, Decision Policy, and accounting truth," Portfolio
Intelligence, `M34-D-0002`/`M34-D-0007`). Investment Universe is not a
collision with this entry; it is the entry's first named specialization — a
precise, closed-vocabulary declaration where the frozen entry is deliberately
generic. No other `GLOSSARY.md` entry uses "Universe," "Scope of holdings," or
an equivalent name. **Accounting Scope** (`GLOSSARY.md`, Ledger & Accounting)
is structurally adjacent — both bound "what belongs" — but Accounting Scope
answers *which ledger a fact belongs to*, an accounting-boundary fact owned by
Ledger & Accounting, while Investment Universe answers *what the strategy
intends to hold*, a descriptive strategy fact owned by Portfolio Intelligence.
The two compose (a universe declaration presupposes exactly one Accounting
Scope, §4 baseline) but neither redefines the other. No collision.

**Canonical reuse analysis:** No existing canonical term names a portfolio-
level declared scope of intended holdings. Portfolio Strategy Metadata names
the umbrella category without naming this specific coordinate; this candidate
closes that naming gap without creating a second umbrella.

**Negative corpus analysis:** Does not carry a belonging/evaluation/refusal
predicate (that territory is explicitly excluded to §6.6, dispositioned
`REJECT`). Does not reintroduce a generic Analysis domain, a portfolio-
measurement owner, or an Investment Judgment/recommendation/strategy-
authoring layer — it declares scope, it recommends nothing. No overlap with
the frozen negative corpus.

**V1–V3 disposition:** V1 satisfied — one term, one meaning, one home
(Portfolio Intelligence), explicitly registered as a specialization of
Portfolio Strategy Metadata rather than a competing umbrella. V2 (same-change
synchronization) is deferred to confirmation and not performed by this
register. V3 satisfied — the name is not currently reserved and does not
collide with a reserved term (the nine domains, six layers, three gates, or
load-bearing law vocabulary).

**M34/M36 compatibility:** Compatible with `M34-D-0002` (Portfolio Identity /
Accounting Scope untouched, referenced only) and `M34-D-0007` (Portfolio
Strategy Metadata's frozen exclusions — Goal Target, Decision Policy,
accounting truth — are preserved; Investment Universe adds none of them).

**Disposition request:** `ADMIT`.

**Glossary synchronization requirement:** If confirmed `ADMIT`, add a
`GLOSSARY.md` entry titled "Investment Universe," cross-linking Portfolio
Strategy Metadata (as the umbrella it specializes) and Accounting Scope (as
the boundary it presupposes but never redefines), with an explicit note that
Investment Universe Membership (the belonging predicate) is a distinct,
currently-inadmissible concept, in the same change the confirmation is
recorded.

**Future contract acceptance evidence:** Once independently confirmed,
M42-WP3's contract text must supply the exact closed vocabulary of permitted
scope-criteria categories (asset type, capability, market, currency), the
exact inert data shape those criteria take (never an executable form), and a
worked example distinguishing a declared universe from a belonging verdict.
This is WP3's own future contract-review obligation, not a precondition for
this candidate's present disposition.

---

### 6.2 Portfolio Policy

**Purpose (as proposed):** Name a declared, portfolio-level rulebook — allowed
markets/classes/currencies, cash requirement, leverage prohibition, fractional
permission, settlement discipline, tax/wrapper context — stated as
forward-binding data rather than enforcement code (Portfolio Domain Model
§5).

**Owner (as proposed):** Portfolio Intelligence. **This register does not
confirm that proposal.** The analysis below proves the concept is not
distinctly ownable by Portfolio Intelligence as a single noun.

**Non-owner:** Not applicable in the ordinary sense — this disposition's
finding is that no single non-owner set is coherent, because the proposed
noun is a composite that fractures across owners already fixed by frozen
authority. See Overlap analysis.

**Permitted inputs (as proposed):** an explicit declared allowed-markets/
classes/currencies set; an explicit declared cash-requirement value; an
explicit declared leverage prohibition; an explicit declared fractional-
trading permission; an explicit declared tax/wrapper context; an explicit
declared settlement discipline.

**Forbidden inputs (as proposed):** a computed verdict, an enforcement
algorithm, or a constraint-resolution outcome (those are Decision
Intelligence's frozen territory, per the proposal's own R1 risk).

**Proposed exact definition (as proposed, RC-4):** A Portfolio Policy would be
a named, portfolio-scoped, forward-binding declaration of the operating rules
a strategy imposes on itself — allowed markets, asset classes, and
currencies; a cash-requirement floor; a leverage/margin prohibition; a
fractional-trading permission; a declared tax/wrapper context; and a declared
settlement discipline — stated as data the optimizer's constraint resolver
and transaction validation consume, never as an enforcement algorithm or
computed verdict in its own right.

**Constitutional constraints (as proposed, RC-4):**

- It would bind forward only, never re-judging recorded history (Portfolio
  Domain Model §5).
- It would be data, never code: each field a declared value, never an `if`
  branch inside an engine.
- It would carry no verdict of its own; the deterministic verdict on any one
  transaction remains Decision Intelligence's constraint-resolution act,
  never this candidate's.

**Overlap analysis (the load-bearing section):** `GLOSSARY.md` already
contains **Decision Policy** — *"Policy envelopes, optimization rules,
decision constraints, execution preferences, and optimizer behavior. Owned by
Decision Intelligence. It may reference Goal Target and Portfolio Strategy
Metadata but owns neither. Governed by `M34-D-0007`."* — and **Portfolio
Limits** / **Sector Limits** — *"Constraints on portfolio composition and
optimization... They govern decision behavior, not Portfolio Identity or
Accounting Scope. Governed by `M34-D-0007`."* Testing the proposed Portfolio
Policy field list against these frozen entries, field by field:

| Proposed Portfolio Policy field | Frozen owner it already falls under | Reasoning |
| --- | --- | --- |
| Allowed Markets / Allowed Asset Classes / Allowed Currencies | Decision Policy (Decision Intelligence, `M34-D-0007`) | "Policy envelopes" is Decision Policy's own frozen phrase for exactly this: the declared boundary of what may be held. `OPTIMIZER_PHILOSOPHY.md` names this territory directly — "Risk / Policy Constraints — the envelope: position limits, sector caps, cash floors, regime-driven restrictions" (§2 there) — as material the optimizer enforces deterministically. A second, Portfolio-Intelligence-owned copy of this same envelope is a second implementation of one rule, forbidden by Law 9. |
| Margin / Leverage prohibition | Portfolio Limits (Decision Intelligence, `M34-D-0007`) | "Constraints on portfolio composition and optimization" is precisely a leverage/margin prohibition. `OPTIMIZER_PHILOSOPHY.md` §2 states the objective hierarchy treats "Risk & Policy Compliance" as Priority 2, enforced deterministically — the same discipline a Portfolio-owned leverage flag would duplicate. |
| Cash Requirement | Portfolio Limits (Decision Intelligence, `M34-D-0007`) | The Portfolio Domain Model's own text concedes this directly: cash requirement is "already a live concept in the optimizer's cash-floor enforcement, promoted here to its proper home as portfolio policy" (§5). The Domain Model is proposing to *move* an already-owned Decision Intelligence coordinate, not describe a new one — exactly the "ownership migration" the M42 proposal's §0 non-reopening rule forbids and its own Final Architectural Boundary disclaims ("no ownership migration"). |
| Fractional Trading permission | Ownership unresolved (RC-6, corrected) | The Portfolio Domain Model frames this as "an asset capability and a portfolio permission... two-sided" (§5). The asset-side capability is Asset Foundation's (frozen). The portfolio-side permission's owner is **not settled by this register**: Portfolio Strategy Metadata's frozen text neither includes nor excludes it, and silence in an existing definition does not prove inclusion. This register makes no ownership claim on this field, positive or negative, beyond confirming it is not admitted as part of "Portfolio Policy" here. |
| Settlement Rules | Ownership unresolved (RC-6, corrected) | Frozen authority distinguishes at least three adjacent, differently-owned concepts: Asset Foundation's frozen **Settlement Semantics** (`GLOSSARY.md` — the asset-class mechanism, instant/cycle-based/negotiated), Ledger & Accounting's ledger-recorded settlement *facts* (what the Accounting Scope's cash balance already reflects), and Decision Intelligence's execution-timing preferences. A portfolio-declared settlement *discipline* does not resolve which of these three it would extend, and this register does not decide that question — it is immaterial to this candidate's disposition either way, since none of the three is Portfolio Intelligence. |
| Tax Rules / wrapper context | Ownership unresolved (RC-6, corrected) | "The policy doesn't compute taxes; it declares which regime's constraints... must respect" (Domain Model §5) is descriptive, but its owner is contested among at least Asset Foundation (wrapper is a fact about the asset's own definition), Wealth Intelligence (tax/protection posture, `GLOSSARY.md` §6.8), Ledger & Accounting (recorded holding-period facts), and Decision Policy (constraints the optimizer must respect). This register does not resolve that contest and assigns this field to none of them by silence. |

Three of seven proposed fields have a proven, frozen owner: allowed
markets/classes/currencies, leverage, and cash requirement are Decision
Intelligence's Decision Policy / Portfolio Limits by their own frozen
definitions and by `OPTIMIZER_PHILOSOPHY.md`'s explicit framing of the same
territory as an enforced envelope. The remaining four (settlement,
fractional permission, tax/wrapper context, and — see below — the
overlap-free residue) do not have a single proven owner among Portfolio
Intelligence, Ledger & Accounting, Asset Foundation, Wealth Intelligence, and
Decision Intelligence; this register leaves each **unresolved** rather than
silently assigning it, per RC-6. **That is sufficient on its own: Platform
Architecture §12's V1 rule — "every platform noun is defined once... two
documents needing different meanings for one word is a naming defect" —
requires a single proven home before a term is admitted. A composite noun
three of whose fields are proven to belong to a different, already-frozen
owner (Decision Intelligence) and the remainder of whose fields have no
proven owner at all cannot be admitted to Portfolio Intelligence under any
reading.** The REJECT disposition below rests on the three proven-overlap
fields alone; it does not require, and does not make, any ownership finding
about the remaining four.

**Canonical reuse analysis:** The three constraint-shaped fields are already
Decision Policy / Portfolio Limits (`M34-D-0007`). The remaining four fields
(settlement, fractional permission, tax/wrapper context) are not proven to be
covered by any single existing canonical term (RC-6); this register does not
resolve their ownership and does not admit them under this or any other name.

**Negative corpus analysis:** Portfolio Policy as proposed risks exactly the
R1 hazard the M42 architecture proposal itself names at §9: *"If M42 lets
Policy carry a verdict or an enforcement algorithm, it forks an owned rule
(Law 9) and reopens `M34-D-0007`."* This register's finding sharpens that risk
from hypothetical to actual: the proposed *declarative* fields, not merely a
future enforcement misstep, already restate frozen Decision Policy / Portfolio
Limits territory by their own definitions, before any contract text is
written. Admitting "Portfolio Policy" to Portfolio Intelligence would not
draw a declaration/enforcement boundary against Decision Intelligence — it
would create a second declared source for the same envelope Decision Policy
already declares, which Decision Intelligence's optimizer would then have to
reconcile against its own frozen constraint-resolution machinery. That is the
architecture's own negative-corpus item (a "portfolio-measurement owner" or
competing judgment-adjacent layer, generalized to a competing *policy-adjacent*
layer) under a new name.

**V1–V3 disposition:** V1 **fails** — the proposed noun does not have one
home. Three of its seven fields have a proven, different, frozen owner
(Decision Intelligence); the remaining four have no proven owner at all. A
term whose fields are proven to belong partly to another domain and are
otherwise unresolved cannot satisfy "one term, one meaning, one home" under
any assignment. V2 is not reached — a term that fails V1 is not a candidate
for synchronization. V3 is not implicated either way.

**M34/M36 compatibility:** **Incompatible as proposed.** Admitting Portfolio
Policy to Portfolio Intelligence, with the field list the Portfolio Domain
Model proposes, would reopen `M34-D-0007`'s Decision Policy / Portfolio Limits
allocation and `M34-D-0002`'s Accounting Scope allocation by relocating
already-owned fields to a new owner — precisely the "ownership migration" the
M42 proposal's §0 forbids ("M42 does not reopen, reinterpret, extend, correct,
or replace any decision of M29–M41... in particular it accepts as fixed and
consumes by exact reference... Portfolio Limits and Sector Limits — owned by
Decision Intelligence, frozen under `M34-D-0007`").

**Five-part ownership-boundary gate (current, corrected — RC-5):** The
five-part gate tests whether one coordinate, *as proposed*, is subject-scoped
to one Portfolio Identity/Accounting Scope, draws only permitted inputs, and
carries permitted rather than prohibited output meaning and semantics. It
does not itself test single ownership across fields — that is V1 (Platform
Architecture §12), a separate constitutional requirement applied above, not
one of the five parts. Portfolio Policy, taken as proposed, is portfolio-
scoped and does not fail the gate on that ground:

| Part | Result | Reasoning |
| --- | --- | --- |
| Permitted subject | Pass | As proposed, the subject is one portfolio's declared operating rules — portfolio-scoped, not cross-portfolio or ambient |
| Permitted inputs | Pass | As proposed, inputs are explicit declared values within the closed field list; no live provider answer or model output |
| Output meaning | Pass | As proposed, output meaning is a declaration, not a computed verdict |
| Prohibited inputs | Pass | As proposed, no wall-clock, cross-portfolio state, or model output |
| Prohibited semantics | Pass | As proposed, no forecast, recommendation, or trust-score meaning |

**The five-part gate passing does not admit this candidate.** Disposition
rests entirely on the separate, independent V1 finding above: the proposed
noun's fields do not have one home — three are proven Decision Intelligence
territory, the rest are unresolved — which V1 forbids regardless of the
gate's outcome on the composite taken at face value.

**Disposition request:** `REJECT` (as a single composite noun owned by
Portfolio Intelligence). **This is not a rejection of the underlying
strategy-fact content** — cash floors, leverage prohibition, allowed markets,
and settlement discipline remain exactly as real and as necessary as the
Portfolio Domain Model describes. The rejection rests on the proven overlap
of three fields (allowed markets/classes/currencies, leverage, cash
requirement) with the frozen Decision Policy / Portfolio Limits allocation —
sufficient on its own to fail V1. The remaining four fields' ownership
(settlement, fractional permission, tax/wrapper context, and any residual
field) is **left unresolved by this register**, not assigned to Portfolio
Strategy Metadata or any other domain; a future, separately chartered
admission MAY propose an owner for any of them, subject to its own five-part
gate and overlap analysis at that time.

**Glossary synchronization requirement:** None. No new `GLOSSARY.md` entry.
No existing entry is amended — Decision Policy, Portfolio Limits, Sector
Limits, Accounting Scope, and Portfolio Strategy Metadata all retain their
frozen text unchanged.

**Consequence for M42-WP4:** Per the M42 architecture proposal's own §11 step
4 ("If WP1 proves the concept is not distinctly ownable by Portfolio
Intelligence, this WP does not proceed"), **M42-WP4 (Portfolio Policy
Declaration Contract) does not proceed** as scoped. Any future work proposing
an owner for the settlement, fractional-permission, tax/wrapper-context, or
other unresolved fields is a separate, later-chartered admission with its own
five-part gate and overlap analysis — not a continuation of M42-WP4, and not
decided in either direction by this register.

**Future contract acceptance evidence:** Not applicable — this candidate does
not survive to a future contract.

---

### 6.3 Portfolio Benchmark Declaration (registered at proposal §4.2 as "Benchmark"; renamed — RC-1)

**Naming correction (RC-1):** `GLOSSARY.md` line 54 already uses the bare word
"Benchmark" in a "Used by" list, and — more materially — the frozen
[Market Data Platform](../architecture/MARKET_DATA_PLATFORM.md) §7 and
[Provider Interface](../architecture/PROVIDER_INTERFACE.md) already define
**Benchmark** as a canonical Market Intelligence-owned observation type: "one
index observation, normalized identically to asset prices so the Benchmark
Engine and AI Evaluation never handle vendor-shaped series" (Market Data
Platform §7), reported by providers via a `Get Benchmarks` capability
(Provider Interface §5) and cached permanently as canonical history (Market
Data Platform §12). Platform Architecture V1 ("one term, one meaning, one
home") applies across documents, not only within `GLOSSARY.md`'s own admitted
entries, and an unqualified "Benchmark" admitted here would collide with that
already-established meaning and owner. This candidate is therefore
**registered under the full compound name Portfolio Benchmark Declaration,
never abbreviated to bare "Benchmark,"** exactly as M41-WP1 §6.1 registered
"Market Measure Definition" under its full compound name to avoid an
analogous collision with "Definition Version." The concept the M42 proposal's
§4.2/§6/Component E describe is unaffected: this is a rename of the *term*,
not a change to the *concept*, its owner, or its scope.

**Purpose:** Name, as a first-class portfolio-level declaration, the
operational definition of "doing well" for one portfolio's strategy — a
choice, never a computation — so that every downstream evaluation layer
(alpha, attribution, human-vs-AI, the Trust Report) compares against a
strategy-appropriate reference rather than a platform-wide default (Portfolio
Domain Model §6). It references the Market Intelligence-owned canonical
**Benchmark** observation series (Market Data Platform §7) by citation only;
it never redefines, re-derives, or shares that term's name.

**Owner:** Portfolio Intelligence.

**Non-owner:** Market Intelligence (owns the referenced observation series
themselves — prices, indices, rates — cited, never re-owned, by a Benchmark
declaration); Ledger & Accounting; Decision Intelligence; Wealth Intelligence;
Experience Platform; providers, storage, and runtime mechanisms.

**Permitted inputs (narrowed — RC-2):**

- an explicit declared form, limited for this confirmation to **Single,
  Composite, Category, or explicitly None** (Portfolio Domain Model §6);
- for Single/Composite/Category forms, an explicit reference to one or more
  Market Intelligence canonical Benchmark observation series (Market Data
  Platform §7), by citation only; and
- a reference to the Portfolio Identity / Accounting Scope the declaration
  belongs to.

**Policy-derived form withheld (RC-2):** The Portfolio Domain Model's fifth
form — the composite "derived from the portfolio's own declared target
allocation" (§6) — is **not admitted by this confirmation**. Its permitted
input, "the portfolio's declared target-allocation weights," is not proven
owned by Portfolio Strategy Metadata: neither `M34-D-0002` nor `M34-D-0007`
nor `GLOSSARY.md` assigns target-allocation weights to that coordinate, and
the Portfolio Domain Model's own §6 cross-references target weights to "the
same question the Ideal/Shadow portfolio infrastructure already asks from the
recommendation side" — Decision Intelligence's territory (Ideal Portfolio,
recommendation machinery), not a settled Portfolio Intelligence fact. Because
this register separately `REJECT`s Portfolio Policy (§6.2) as the nominal
source of a declared target allocation, the Policy-derived form currently has
no proven-owned input to reference at all. This form is therefore withheld
pending a future, separately proven admission of target-allocation-weights
ownership; it is not decided, in either direction, by this register, and
neither M42-WP5 nor M42-WP7 may rely on it before such a future admission.

**Forbidden inputs:**

- a computed alpha, attribution, or performance-comparison value (those are
  Portfolio Intelligence's *future*, explicitly-deferred derived-measure
  territory — M42 §8 — never part of the declaration itself);
- an ambient default substituted when none is declared (Portfolio Domain
  Model §6: "declaring 'this portfolio is not benchmarked' is truthful;
  defaulting it to an equity index would manufacture noise");
- any input the Market Intelligence Benchmark observation series itself does
  not already canonically carry (no private re-derivation of a series); and
- the withheld Policy-derived form's target-allocation-weights input, until
  a future admission proves its ownership (RC-2).

**Proposed exact definition (renamed and narrowed — RC-1, RC-2):** A
Portfolio Benchmark Declaration is a named, portfolio-scoped declaration of
one of **four** closed forms — Single, Composite, Category, or explicitly
None — stating which Market Intelligence canonical Benchmark observation
series (Market Data Platform §7), if any, this portfolio's performance is
judged against. It references the chosen series by citation only; it
computes no alpha, attribution, or comparison value; it carries no ambient
default; and it is never abbreviated to bare "Benchmark," which remains
Market Intelligence's reserved name for the underlying observation type. The
fifth form the Portfolio Domain Model describes — Policy-derived — is
withheld from this confirmation (see Permitted inputs above).

**Constitutional constraints:**

- It MUST instantiate exactly one of the four confirmed closed forms; a
  hybrid, open-ended, or Policy-derived form is outside this candidate's
  present closure.
- It MUST reference Market Intelligence Benchmark series by exact citation;
  it MUST NOT re-derive, re-price, or maintain a private copy of a series.
- It MUST NOT compute or carry any comparison value (alpha, attribution) —
  that is explicitly deferred to a future milestone (M42 §8).
- "No Benchmark" MUST be a distinct, explicit, valid declaration state, never
  collapsed to or confused with an unset/missing value.
- It MUST NOT be named or abbreviated as bare "Benchmark" in any future
  contract, schema, or Glossary text (RC-1).

**Five-part ownership-boundary gate (current, corrected — RC-2):**

| Part | Result | Reasoning |
| --- | --- | --- |
| Permitted subject | Pass | Subject is one portfolio's declared comparison choice; no cross-portfolio or ambient subject |
| Permitted inputs | Pass | Inputs are limited, for the four confirmed forms, to a declared form and a Market Intelligence Benchmark series citation, plus a Portfolio Identity reference; the Policy-derived form's unproven input is excluded from this gate evaluation, not passed conditionally |
| Output meaning | Pass | Output meaning is limited to a named declaration of comparison intent — no computed alpha, attribution, or comparison value |
| Prohibited inputs | Pass | No live provider answer, wall-clock, cross-portfolio state, or model output; Benchmark series are cited as already-canonical, not freshly fetched |
| Prohibited semantics | Pass | No performance, risk, recommendation, or trust meaning appears in the proposed exact definition; alpha/attribution are explicitly excluded and deferred |

**Overlap analysis (corrected — RC-1):** `GLOSSARY.md` line 54 already lists
"Benchmark" as a consumer of Portfolio Snapshot data, and — the material
collision — [Market Data Platform](../architecture/MARKET_DATA_PLATFORM.md)
§7 and [Provider Interface](../architecture/PROVIDER_INTERFACE.md) already
define **Benchmark** as a frozen Market Intelligence-owned canonical
observation type ("one index observation, normalized identically to asset
prices," reported via a `Get Benchmarks` provider capability, cached
permanently as Benchmark Cache). This register's candidate is a different
concept with a different owner — a per-portfolio *declaration of which
series to compare against*, not the series itself — and V1 forbids the same
bare name for both. Registering this candidate under the full compound name
**Portfolio Benchmark Declaration**, never abbreviated, resolves the
collision exactly as M41-WP1 §6.1 resolved "Market Measure Definition"
against "Definition Version": two structurally adjacent, differently-owned
concepts, disambiguated by a compound name rather than by contesting the
bare word. Portfolio Strategy Metadata remains the umbrella this candidate
sits beside as a sibling declared coordinate (as Investment Universe does at
§6.1); no collision there.

**Canonical reuse analysis:** No existing canonical term names a per-
portfolio declared comparison reference (as distinct from the observation
series itself, which Market Intelligence already owns and this candidate
cites without redefining). This is a genuinely new descriptive coordinate
under its corrected, disambiguated name.

**Negative corpus analysis:** Does not compute alpha, attribution, or any
derived performance measure (all explicitly deferred by the M42 proposal
§8). Does not reintroduce a portfolio-measurement owner beside Portfolio
Intelligence, an Investment Judgment/recommendation layer, or a Trust &
Evaluation verdict. Does not reuse Market Intelligence's reserved "Benchmark"
name unqualified (RC-1). No overlap with the frozen negative corpus.

**V1–V3 disposition:** V1 satisfied **only under the corrected compound
name** — one term, one meaning, one home (Portfolio Intelligence),
disambiguated from Market Intelligence's frozen Benchmark observation type
and from Portfolio Strategy Metadata's broader umbrella; V1 would have
**failed** under the bare name "Benchmark," which is why RC-1 forces the
rename rather than a bare `ADMIT`. V2 deferred to confirmation. V3
satisfied — no reserved-term collision.

**M34/M36 compatibility:** Compatible with `M34-D-0002`/`M34-D-0007`
(Portfolio Strategy Metadata's frozen exclusions are preserved; this
candidate adds a sibling declared coordinate, not a redefinition). Preserves
the frozen M39 Market Observation, M40–M41 Market Measure corpus, and Market
Data Platform's Benchmark observation type by citation only, under a
disambiguated name.

**Disposition request:** `RENAME` — admitted under the compound name
**Portfolio Benchmark Declaration**, with the Policy-derived form withheld
per RC-2. Not a bare `ADMIT`.

**Glossary synchronization requirement:** If confirmed, add a `GLOSSARY.md`
entry titled "Portfolio Benchmark Declaration" (never abbreviated),
cross-linking Portfolio Strategy Metadata, the frozen Market Intelligence
Benchmark observation type (with an explicit non-collision note), and stating
that only Single/Composite/Category/None forms are admitted, with
Policy-derived explicitly recorded as withheld pending future admission, in
the same change the confirmation is recorded.

**Future contract acceptance evidence:** Once independently confirmed,
M42-WP5's contract text must supply the exact closed vocabulary for each of
the four confirmed forms, the exact citation format for referenced Benchmark
series, a worked example of the "No Benchmark" declaration state, and MUST
NOT specify a Policy-derived form unless a future, separately confirmed
admission has first proven target-allocation-weights ownership. This is
WP5's own future contract-review obligation, not a precondition for this
candidate's present disposition.

---

### 6.4 Portfolio Base Currency

**Purpose:** Name the unit of account in which one portfolio's NAV, returns,
and benchmark comparisons are expressed (Portfolio Domain Model §3).

**Owner (corrected — RC-3):** Ledger & Accounting. **This is a fresh
admission on this register's own five-part-gate proof, not a claim that
`M34-D-0002` already silently included this field.** `M34-D-0002` assigns
Portfolio Identity and Accounting Scope to Ledger & Accounting as coordinates,
but neither `M34-D-0002` nor the canonical Portfolio Identity / Accounting
Scope entries in `GLOSSARY.md` enumerate a unit-of-account field: Portfolio
Identity is "the stable identifier of one portfolio container... it
establishes accounting identity," and Accounting Scope is "the accounting
boundary to which a portfolio's holdings, transactions, cash, and balances
belong" — neither text mentions currency or a reporting unit. A Level-4
design placement (Portfolio Domain Model §3 locates Base Currency under a
section titled "Portfolio Identity") is evidence for where the field
*belongs*, never proof that a frozen canonical coordinate already *contains*
it. This register does not treat that placement as dispositive; it treats it
as the starting hypothesis the five-part gate below independently tests.

**Non-owner:** Portfolio Intelligence (does not own accounting-semantic unit-
of-account facts consumed directly by `PORTFOLIO_CALCULATION_RULES.md`'s NAV
and `investment_return_pct` arithmetic); Asset Foundation (owns the
underlying currency/Unit Semantics vocabulary this coordinate references,
never the portfolio-level choice of which currency applies); Decision
Intelligence, Wealth Intelligence, Experience Platform; providers, storage,
and runtime mechanisms.

**Permitted inputs:**

- an explicit currency reference drawn from Asset Foundation's frozen
  currency/Unit Semantics vocabulary, cited without redefinition; and
- a reference to the Portfolio Identity the currency choice belongs to.

**Forbidden inputs:**

- a live FX rate or any computed conversion value (Market Intelligence's FX
  observations are consumed downstream by accounting arithmetic; this
  coordinate states only *which* currency, never a rate or a converted
  amount);
- an ambient or inferred default currency; and
- any strategy, policy, or benchmark meaning (this is an accounting-identity
  fact, not a declarative strategy coordinate).

**Proposed exact definition:** Portfolio Base Currency is the single,
explicit currency reference, drawn from Asset Foundation's frozen currency
vocabulary, in which one Portfolio Identity's NAV, returns, and benchmark
comparisons are expressed. It is set at portfolio creation and changed only
as an explicit, recorded event — never a silent reinterpretation of the
meaning of a historical number (Portfolio Domain Model §3) — consistent with
the same immutability-of-accounting-fact discipline Ledger & Accounting
already applies to every other coordinate it owns (Law 2, Law 4).

**Constitutional constraints:**

- It MUST reference only Asset Foundation's already-owned currency
  vocabulary; it MUST NOT define a new currency taxonomy.
- It MUST be scoped to exactly one Portfolio Identity; it MUST NOT be
  ambient or shared across portfolios.
- A change MUST be an explicit, recorded event, never an in-place edit of
  historical meaning (Law 2).
- It MUST carry no computed conversion, rate, or NAV value of its own — it
  names the unit; `PORTFOLIO_CALCULATION_RULES.md` states the arithmetic
  that consumes it.

**Five-part ownership-boundary gate (current):**

| Part | Result | Reasoning |
| --- | --- | --- |
| Permitted subject | Pass | Subject is the unit-of-account field of one Portfolio Identity — an accounting-identity fact within Ledger & Accounting's constitutional purview (Platform Architecture §6.3) |
| Permitted inputs | Pass | Inputs are limited to a currency reference and Asset Foundation's frozen Unit Semantics/currency vocabulary, cited without redefinition, and a Portfolio Identity reference |
| Output meaning | Pass | Output meaning is limited to an identity-adjacent accounting fact — no strategy declaration, no computed measure |
| Prohibited inputs | Pass | No live provider answer, wall-clock, live FX rate, or model output |
| Prohibited semantics | Pass | No performance, risk, or recommendation meaning |

**Overlap analysis:** No `GLOSSARY.md` entry currently names this coordinate
explicitly. The two adjacent frozen entries — Portfolio Identity and
Accounting Scope — are consulted and found not to already state it (see
Owner above); admitting it as a named field of the same owning domain avoids
creating a second, competing accounting-identity coordinate while not
overclaiming that the frozen text already covered it. No collision with
Investment Universe (§6.1) or Portfolio Benchmark Declaration (§6.3), which
are strategy-level, not accounting-level, coordinates.

**Canonical reuse analysis:** No existing canonical term fully names this
coordinate. It is closely adjacent to, and composed from, Asset Foundation's
frozen currency/Unit Semantics vocabulary (reused by reference) and sits
within Ledger & Accounting's already-frozen accounting-identity purview
(extended, not reopened, by this admission).

**Negative corpus analysis:** Treating Base Currency as a Portfolio-
Intelligence-owned strategy declaration, or as a silently mutable display
setting, would risk exactly the R6 hazard the M42 proposal names (§9):
"Treating Base Currency as a mutable display setting would silently rewrite
the meaning of every historical number." Fixing its owner as Ledger &
Accounting — the domain that already owns immutability discipline over every
accounting fact — closes that hazard structurally.

**V1–V3 disposition:** V1 satisfied — one term, one meaning, one home
(Ledger & Accounting), proven fresh by this register rather than assumed.
V2 deferred to confirmation. V3 satisfied — Portfolio Identity's and
Accounting Scope's reserved meanings are not altered; this is an additional,
distinctly named coordinate within the same owning domain, not a
redefinition of either.

**M34/M36 compatibility:** Compatible with `M34-D-0002` as an admission
*within* the accounting-identity purview `M34-D-0002` already assigns to
Ledger & Accounting, not as a reinterpretation of what `M34-D-0002` itself
enumerates. No ownership migrates *to* Portfolio Intelligence, satisfying the
M42 proposal's own §0 non-reopening rule and Final Architectural Boundary
("no ownership migration").

**Disposition request:** `ADMIT` (corrected from `REUSE` — RC-3). Portfolio
Base Currency is a new, named coordinate, admitted to Ledger & Accounting on
this register's own five-part-gate proof — not asserted to have been already
silently present in `M34-D-0002`.

**Glossary synchronization requirement (corrected — RC-3):** If confirmed
`ADMIT`, add a `GLOSSARY.md` entry titled "Portfolio Base Currency," owned by
Ledger & Accounting, cross-linking Portfolio Identity, Accounting Scope, and
Asset Foundation's currency/Unit Semantics vocabulary, with the explicit
event-sourced-change invariant, in the same change the confirmation is
recorded.

**Consequence for M42-WP5:** Unchanged in outcome: the Base-Currency leg of
M42-WP5 does not proceed as a Portfolio-Intelligence admission — it was never
proven ownable there. Under the corrected disposition, M42-WP2 (Ledger &
Accounting, Component B) carries this coordinate as a confirmed `ADMIT`
citation, not as an assumed-reuse field it may optionally choose to name.

**Future contract acceptance evidence:** Once independently confirmed,
M42-WP2's contract text must supply the exact currency-reference format, the
exact "change is a recorded event, never a silent reinterpretation"
mechanism, and a worked example distinguishing Portfolio Base Currency from
a live FX conversion. This is WP2's own future contract-review obligation,
not a precondition for this candidate's present disposition.

---

### 6.5 Portfolio Composition

**Purpose:** Name the single, terminal, deterministic projection that binds
every frozen and WP1-confirmed Portfolio coordinate — identity, boundary,
declarations, lifecycle, lineage — into one immutable, canonically
serializable read-surface, carrying no derived measure (M42 architecture
Component G, the Portfolio-domain analog of M41-WP4's Result model).

**Owner:** Portfolio Intelligence.

**Non-owner:** Ledger & Accounting (contributes Identity/Boundary/Lifecycle
coordinates by citation, never re-owned); Decision Intelligence, Wealth
Intelligence, Experience Platform (consumers, never contributors of meaning);
providers, storage, and runtime mechanisms.

**Permitted inputs:**

- the frozen Portfolio Identity, Accounting Scope, Portfolio Membership, and
  Portfolio Lifecycle State coordinates (§4 baseline), cited without
  mutation;
- any candidate this register confirms `ADMIT`/`RENAME` (Investment Universe,
  Portfolio Base Currency, Portfolio Benchmark Declaration — the latter
  limited to its four confirmed forms, Policy-derived excluded per RC-2),
  cited at their confirmed meaning only; and
- lineage/provenance fields citing Connectivity & Ingestion as provenance
  owner (frozen, unmodified).

**Forbidden inputs:**

- any candidate this register confirms `REJECT` or leaves unproven (Portfolio
  Policy, Investment Universe Membership) — the composition carries no field
  those dispositions did not admit;
- any performance, risk, attribution, or exposure value (the no-derived-
  measure invariant, M42 §4.3 part 5); and
- an ambient default for any composed field.

**Proposed exact definition:** A Portfolio Composition is the single,
deterministic, canonically serializable projection binding one Portfolio
Identity's frozen and confirmed-admitted coordinates — accounting boundary,
lifecycle state, confirmed declarative strategy fields, and provenance —
into one immutable read-surface. Two independent readers, given the same
frozen and confirmed coordinates, MUST derive the identical composition. It
carries no derived measure, no ambient default, and no field this register or
a future confirmed WP1 disposition did not admit.

**Constitutional constraints:**

- It MUST compose only frozen or WP1-confirmed coordinates; it MUST NOT
  introduce a field this register rejected or left unconfirmed (Portfolio
  Policy, Investment Universe Membership).
- It MUST carry no derived measure — a NAV, a weight, a return, or any
  performance/risk/attribution number breaks the truth/judgment wall the
  whole milestone exists to protect (M42 §9, R3).
- Composition determinism MUST hold: identical inputs produce an identical
  composition, with no wall-clock, provider, or model dependence.
- It MUST NOT become a shadow Portfolio Identity — the terminal projection
  is a read-surface, never a second source of the Ledger & Accounting facts
  it composes (Law 1, Law 3).

**Five-part ownership-boundary gate (current):**

| Part | Result | Reasoning |
| --- | --- | --- |
| Permitted subject | Pass | Subject is the terminal composition of one Portfolio Identity's already-owned coordinates; no new subject beyond what §4 baseline and confirmed §6.1/§6.3 candidates supply |
| Permitted inputs | Pass | Inputs are limited to frozen coordinates and confirmed-admitted candidates, cited without mutation |
| Output meaning | Pass | Output meaning is limited to an immutable, deterministic composition — explicitly no derived measure |
| Prohibited inputs | Pass | No live provider answer, wall-clock, cross-portfolio state, or model output |
| Prohibited semantics | Pass | No performance, risk, attribution, exposure, optimization, ranking, forecast, recommendation, trust score, or suitability appears in the proposed exact definition |

**Overlap analysis:** No `GLOSSARY.md` entry with this name exists. The
closest structural analog is M41's Market Measure Result (a terminal,
composed, immutable record) — a different subject (a calculation's outcome,
not a portfolio's composed identity) with a different owner (Market
Intelligence) — cited here only as a pattern precedent, not a term overlap.
No collision.

**Canonical reuse analysis:** No existing canonical term names a terminal,
whole-Portfolio composed projection. This is a genuinely new concept the
milestone's own stated objective (M42 §1) requires: "the single deterministic
Portfolio Composition projection through which every downstream domain reads
it."

**Negative corpus analysis:** Explicitly carries no derived measure (the
architecture's own R3 mitigation, restated here as a constitutional
constraint). Does not become a new umbrella beside the nine domains — it is
owned by the existing Portfolio Intelligence domain (M42 §9, R2 mitigation).
No overlap with the frozen negative corpus.

**V1–V3 disposition:** V1 satisfied — one term, one meaning, one home
(Portfolio Intelligence). V2 deferred to confirmation. V3 satisfied — no
reserved-term collision.

**M34/M36 compatibility:** Compatible with `M34-D-0002/0003` — composes,
never redefines, Portfolio Identity, Accounting Scope, Portfolio Membership,
and Portfolio Lifecycle State. Compatible with `M36-WP1-A01/A09` — Lifecycle
State is composed by citation, with no new transition vocabulary introduced.

**Disposition request:** `ADMIT`.

**Glossary synchronization requirement:** If confirmed `ADMIT`, add a
`GLOSSARY.md` entry titled "Portfolio Composition," cross-linking Portfolio
Identity, Accounting Scope, Portfolio Lifecycle State, and (if independently
confirmed by their own admission path) Investment Universe, Portfolio Base
Currency, and Portfolio Benchmark Declaration, with an explicit
no-derived-measure note, in the same change the confirmation is recorded.
Note: this Glossary entry names the *concept*; it does not specify the
composition's exact field order, schema-version tag, or serialization rule,
which remain M42-WP7's terminal contract obligation.

**Future contract acceptance evidence:** Once independently confirmed,
M42-WP7's contract text must supply the exact canonical field order, a
schema-version tag, composition-determinism golden vectors, and the
integrated no-derived-measure proof the M42 proposal's §11 step 5 requires.
This is WP7's own future contract-review obligation, not a precondition for
this candidate's present disposition.

---

### 6.6 Investment Universe Membership (belonging predicate)

**Purpose (as proposed):** A predicate that decides whether a specific
instrument belongs within a portfolio's declared Investment Universe, and the
refusal that follows when it does not (Portfolio Domain Model §9, "Universe
allowed").

**Owner (as proposed):** Unproven — the M42 architecture proposal itself
flags this candidate as requiring "an ownership and five-part-gate proof
consistent with `M34-D-0007`" before any admission (§4.2). **This register
finds no such proof is available within Portfolio Intelligence, and that the
predicate is inadmissible to M42 at all.**

**Non-owner:** Portfolio Intelligence, for the reason stated below. Asset
Foundation (owns the classification/capability facts the predicate would
read, never the verdict it would produce).

**Permitted inputs (as proposed, RC-4):** a reference to one portfolio's
declared Investment Universe (§6.1); a reference to one Asset Foundation
classification/capability record for the instrument under evaluation.

**Forbidden inputs (as proposed, RC-4):** none additionally forbidden beyond
the closed permitted-input set above — the candidate's defect is in its
*output*, not its inputs (see Five-part gate below).

**Proposed exact definition (as proposed, RC-4):** Investment Universe
Membership would be a deterministic predicate, evaluated against one
portfolio's declared Investment Universe and one instrument's Asset
Foundation classification/capability record, producing a met/unmet verdict
and, on "unmet," a refusal.

**Constitutional constraints (as proposed, RC-4):**

- It would be deterministic and replay-stable, reading only already-owned
  Investment Universe and Asset Foundation facts.
- Its refusal would state which declared criterion was violated, in strategy
  language (Portfolio Domain Model §9).

**Overlap analysis (the load-bearing section):** Deciding "does this
instrument belong here?" and producing a refusal from that decision is, by
its own nature, a **verdict** — a computed determination applied against a
declared boundary, exactly the shape `GLOSSARY.md`'s frozen **Portfolio
Limits** / **Sector Limits** entries already own: *"Constraints on portfolio
composition and optimization... They govern decision behavior."* A predicate
that evaluates an instrument against a declared universe and refuses entry on
failure is functionally identical in kind to a predicate that evaluates a
proposed trade against a declared limit and refuses it on breach — both are
"declared boundary, in; runtime evaluation, out; failure is a refusal." The
Portfolio Domain Model's own §9 places "Universe allowed" in a numbered list
alongside "Policy compatible" (the very territory §6.2 above found already
belongs to Decision Policy / Portfolio Limits) as one more entry the same
validation machinery evaluates — it does not describe a differently-shaped
concept, it describes the same evaluation discipline applied to one more
declared boundary. `OPTIMIZER_PHILOSOPHY.md` states the general principle this
predicate would violate if admitted to Portfolio Intelligence: "Constraints
are enforced deterministically — a belief cannot negotiate with a constraint"
(§2) — constraint evaluation and refusal is Decision Intelligence's owned
discipline, not a descriptive Portfolio Intelligence fact.

**Canonical reuse analysis:** No existing canonical term names this exact
predicate, but its *shape* — declared boundary, runtime evaluation, refusal on
failure — is already Decision Intelligence's Portfolio Limits / Sector Limits
shape, applied here to one more declared surface (the Universe) rather than to
a numeric limit. It is not a new concept; it is the frozen enforcement pattern
applied to one more input.

**Negative corpus analysis:** Admitting a belonging/evaluation/refusal
predicate to Portfolio Intelligence as descriptive vocabulary would violate
the M42 architecture's own explicit non-goal (RC-3, restated at §4.2 and the
Explicit Non-Goals list): *"author any belonging/evaluation/refusal/
validation/enforcement predicate that decides whether an instrument
belongs — that is a verdict, not a descriptive coordinate."* This register
confirms that finding rather than reopening it.

**V1–V3 disposition:** V1 is not reached — a verdict-producing predicate is
not a descriptive coordinate Portfolio Intelligence may own under the M42
architecture's own truth/judgment separation (§0, §2.3 there). V2, V3 not
applicable.

**M34/M36 compatibility:** Admitting this predicate to Portfolio Intelligence
would conflict with `M34-D-0007`'s frozen allocation of constraint/verdict
territory to Decision Intelligence. Leaving it unadmitted preserves
`M34-D-0007` untouched.

**Five-part ownership-boundary gate (current, corrected — RC-5):** The
subject of this candidate is one portfolio and one instrument — a
permitted, portfolio-scoped subject, exactly as Investment Universe
Membership's proponent would frame it. The gate does not fail here; it fails
squarely and solely at output meaning, which is sufficient on its own (a
single failed part blocks approval):

| Part | Result | Reasoning |
| --- | --- | --- |
| Permitted subject | Pass | Subject is one portfolio and one instrument — portfolio-scoped, not ambient or cross-portfolio |
| Permitted inputs | Pass | Inputs are limited to the declared Investment Universe and the instrument's Asset Foundation classification/capability record — the closed permitted-input set above |
| Output meaning | **Fail** | Output meaning is a met/unmet verdict and an associated refusal — the M42 architecture's five-part gate part 3 requires "only an immutable, deterministic descriptive coordinate... never a verdict." This is the sole and sufficient failure. |
| Prohibited inputs | Pass | No live provider answer, wall-clock, cross-portfolio state, or model output |
| Prohibited semantics | Pass (corrected — RC-5) | A belonging refusal is not itself "recommendation" or "suitability" language, and the suitability analogy is withdrawn as overreach; this part does not independently fail, and does not need to — the output-meaning failure above is sufficient by itself |

The single output-meaning failure blocks approval; no further part need also
fail, and this register no longer claims that they do.

**Disposition request:** `REJECT`, for admission as Portfolio Intelligence
descriptive vocabulary, under this milestone, in full. **This is not a
statement that instrument-belonging evaluation is undesirable** — Portfolio
Domain Model §9 correctly identifies it as a real and valuable check. It is a
finding that the check is verdict/enforcement in kind, and that its only
constitutionally available home, if it is ever separately chartered, is
Decision Intelligence, under its own ownership and five-part-gate proof
consistent with `M34-D-0007` — a future, separately-governed admission, wholly
outside M42's scope, never a continuation of M42-WP3.

**Glossary synchronization requirement:** None. No `GLOSSARY.md` change.

**Consequence for M42-WP3:** M42-WP3 (Investment Universe Declaration
Contract) proceeds, per its own architecture-stated scope, on the confirmed
`ADMIT` of Investment Universe (§6.1) alone, and MUST NOT specify a belonging
predicate, refusal, or validation verdict as part of its declaration contract
— exactly as the M42 architecture's own Component C and RC-3 already require,
now confirmed rather than merely proposed by this register's independent
analysis.

**Future contract acceptance evidence:** Not applicable — this candidate does
not survive to a future contract under M42.

---

## 7. Repository-Hygiene Note (non-normative)

This register's front matter records that the M42 Architecture Proposal's own
Independent Review and Independent Confirmation are asserted, in this
session, to have occurred, but no corresponding artifact
(`M42_ARCHITECTURE_INDEPENDENT_REVIEW.md`,
`M42_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md`) exists in
`docs/implementation/` alongside `M42_ARCHITECTURE_PROPOSAL.md`, unlike every
prior milestone's architecture phase (M39, M40, M41 each left this pair
committed). This section is not a disposition, a finding, or a governance
predicate — it does not gate this register's own review — but it is recorded
so that the eventual Independent Review of this document has the same
complete paper trail every prior WP1 register enjoyed. Committing the missing
pair (or correcting `M42_ARCHITECTURE_PROPOSAL.md`'s own Final Status line,
still reading `READY FOR INDEPENDENT ARCHITECTURE REVIEW`, to reflect its
actual confirmed state) is recommended before this register's own Independent
Review begins, so that reviewers are not asked to trust an unrecorded
assertion at the one level of authority (architecture) this register is
directly subordinate to.

---

## 8. Summary Disposition Table

| Candidate | Disposition | Owner (confirmed by this register) | Consequence |
| --- | --- | --- | --- |
| Investment Universe (declaration only, inert scope criteria only — RC-7) | `ADMIT` | Portfolio Intelligence (specialization of Portfolio Strategy Metadata) | M42-WP3 proceeds, declaration-only, no belonging predicate, no evaluation capability |
| Portfolio Policy | `REJECT` | N/A — three fields proven Decision Intelligence territory (Decision Policy / Portfolio Limits, `M34-D-0007`); remaining fields' ownership left unresolved (RC-6) | M42-WP4 does not proceed as scoped |
| Portfolio Benchmark Declaration (renamed from "Benchmark" — RC-1; four forms only, Policy-derived withheld — RC-2) | `RENAME` | Portfolio Intelligence | M42-WP5's declaration leg proceeds under the corrected name, for Single/Composite/Category/None only |
| Portfolio Base Currency | `ADMIT` (corrected from `REUSE` — RC-3) | Ledger & Accounting (new coordinate, proven by this register's own five-part gate) | M42-WP5's Base-Currency leg does not proceed as a Portfolio Intelligence admission; M42-WP2 carries the confirmed coordinate |
| Portfolio Composition | `ADMIT` | Portfolio Intelligence | M42-WP7 proceeds, terminal contract, composing only frozen + confirmed-admitted coordinates |
| Investment Universe Membership (belonging predicate) | `REJECT` | N/A — verdict/enforcement shape (output-meaning gate failure alone is sufficient — RC-5), Decision Intelligence's territory if ever separately chartered | Excluded from M42-WP3 and from M42 in its entirety |

No disposition in this table is canonical, admitted, or reliable until a
separate Independent Review, any required correction, and a separate
Independent Confirmation document record that this register has passed.

---

## Status

**`READY_FOR_INDEPENDENT_CONFIRMATION`**

This revision resolves Independent Review findings RC-1 through RC-7 (§0.1),
plus the two remaining consistency corrections Independent Confirmation
review identified (Base Currency `REUSE` → `ADMIT` residue in downstream
planning text; residual "scope predicate" wording), and is submitted for
Independent Confirmation. It creates no implementation,
runtime, provider, persistence, API, or production-method authority. It
modifies no frozen artifact, no domain constitution, `GLOSSARY.md`, the
Decision Log, the Implementation Index, or source code. It does not begin
M42-WP2 through WP7. Glossary synchronization for the `ADMIT`/`RENAME`
dispositions above occurs only in the same change as this register's own
Independent Confirmation, per the same corpus convention M40-WP1 and M41-WP1
established.
