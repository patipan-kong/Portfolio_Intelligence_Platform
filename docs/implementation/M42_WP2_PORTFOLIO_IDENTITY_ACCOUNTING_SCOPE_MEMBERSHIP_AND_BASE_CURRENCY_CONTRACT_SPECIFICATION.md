# M42-WP2 — Portfolio Identity, Accounting Scope, Membership & Base Currency Contract Specification

**Document role:** Architecture and Governance authorship (normative contract
specification, consolidated Stage A + Stage B for a reuse-only work package)

**Milestone:** M42 — Portfolio Intelligence Foundation (Canonical Portfolio Domain)

**Work package:** M42-WP2 — Portfolio Identity, Accounting Scope & Membership
Contract (Component B), carrying Portfolio Base Currency per the confirmed
WP1 disposition

**Component:** B

**Sole/primary owner:** Ledger & Accounting

**Stage:** Consolidated Stage A (reuse-only vocabulary register) + Stage B
(contract specification), per the Architecture Proposal's own classification
of this component as *"reuse-only vocabulary"* (§6) — no genuinely new
candidate noun is proposed here; the one new field this document specifies,
Portfolio Base Currency, was already admitted at M42-WP1's Stage A gate, not
proposed for the first time by this document.

**Stage status:** `READY_FOR_INDEPENDENT_CONFIRMATION`

**Prior review:** [M42-WP2 Independent Governance
Review](M42_WP2_INDEPENDENT_REVIEW.md) — `APPROVED WITH REQUIRED CORRECTIONS`,
six required corrections (IR-1 through IR-6), three observations (IR-7
through IR-9). A first corrections pass applied all six; a subsequent
Independent Confirmation pass identified two residual defects — RC-1 (an
unregistered normative term, "holding-record," introduced by the IR-1 fix)
and RC-4 (residual wording implying `PORTFOLIO_CALCULATION_RULES.md` is
parameterized by, implicitly requires, or already consumes Portfolio Base
Currency) — both now applied in this revision.

**M42 Architecture:** asserted `READY FOR INDEPENDENT ARCHITECTURE REVIEW` per
its own Final Status line; treated as frozen per this document's operating
instruction (see §1.4).

**M42-WP1 Stage A register:** asserted `COMPLETE AND CONFIRMED`, all
dispositions frozen, per this document's operating instruction (see §1.4).
The register's own on-disk status line still reads
`READY_FOR_INDEPENDENT_CONFIRMATION`; see §1.4 for how this document treats
that gap, which mirrors the identical gap the WP1 register itself flagged at
its own §7 against the Architecture Proposal.

**Implementation authority:** `NONE`

**Runtime authority:** `NONE`

**Provider authority:** `NONE`

**Persistence authority:** `NONE`

**API authority:** `NONE`

**Production-method authority:** `NONE`

**Executable-validation authority:** `NONE`

**Canonical vocabulary admission (by this document):** `NONE`. This document
admits no candidate. It specifies contract text for coordinates already
frozen (`M34-D-0002`, `M34-D-0003`) or already confirmed `ADMIT` at M42-WP1's
Stage A gate (Portfolio Base Currency). Glossary synchronization for
Portfolio Base Currency is WP1's own confirmation condition (register §6.4),
to be performed in the same change as WP1's own Independent Confirmation. As
of this revision, `docs/GLOSSARY.md` does not yet contain a "Portfolio Base
Currency" entry; this document does not perform that synchronization (outside
its own authority — see §11) and does not represent it as already done. See
§11 for the corrected repository-state statement.

---

## 0. Executive Determination

This specification closes the complete normative M42-WP2 allocation. A
conforming M42-WP2 contract:

1. reuses Portfolio Identity, Accounting Scope, and Portfolio Membership
   exactly as `M34-D-0002` and `M34-D-0003` and their `GLOSSARY.md` entries
   state them today, authoring no new definition, field, or exception for any
   of the three;
2. states, as a contract rather than a re-derivation, the **boundary
   integrity invariant** — every portfolio-scoped fact resolves to exactly
   one Accounting Scope — and the **replay-never-crosses-a-boundary
   invariant**, both already implied by `M34-D-0002/0003` and
   `PORTFOLIO_DOMAIN_MODEL.md` §§1–2, never newly authored by this document;
3. carries Portfolio Base Currency as a **confirmed** coordinate admitted at
   M42-WP1's Stage A gate to Ledger & Accounting — not a fresh proposal, not
   a Portfolio Intelligence coordinate, and not an assertion that
   `M34-D-0002` silently contained it before WP1's admission;
4. supplies Portfolio Base Currency's currency-reference coordinate (bounded
   truthfully to what Asset Foundation's frozen Classification dimension
   actually publishes today), its event-sourced-change mechanism, and a
   worked example distinguishing it from FX Observation without authoring
   new computation behavior — the three items WP1 §6.4 named as this work
   package's own future contract-review obligation;
5. authors **no new accounting arithmetic**: the NAV, return, and
   cash-flow-adjustment formulas remain exactly as `PORTFOLIO_CALCULATION_RULES.md`
   states them, unedited and unamended; this contract defines the Portfolio
   Base Currency coordinate itself and takes no position on whether or how
   those formulas consume it;
6. authors **no lifecycle-transition vocabulary** (that is M42-WP6's
   citation-only territory, not this one); and
7. carries no derived measure, no ambient default, and no candidate this
   register did not already confirm `ADMIT`.

No ambient default remains on the accounting-boundary leg of the Portfolio
surface. No new governed vocabulary, owner, or accounting rule is introduced.

---

## 1. Authority, Precedence, and Non-Reopening

### 1.1 Authority order

This specification is subordinate, in order, to:

1. the frozen [Platform Architecture](../architecture/platform_architecture.md)
   constitution (v1.1) — its domains, layers, gates, laws, governance
   precedence (§11), and canonical-vocabulary rules (§12);
2. the frozen domain constitutions —
   [OPTIMIZER_PHILOSOPHY.md](../investment/OPTIMIZER_PHILOSOPHY.md) and
   [PORTFOLIO_CALCULATION_RULES.md](../investment/PORTFOLIO_CALCULATION_RULES.md);
3. the frozen Architecture Decision Records, in particular `M34-D-0002`,
   `M34-D-0003`, and `ADR-004`;
4. the frozen M29–M41 milestone corpus, in particular `M36-WP1-A01` and
   `M36-WP1-A09` governing Portfolio Lifecycle State;
5. the [Portfolio Domain Model](../architecture/PORTFOLIO_DOMAIN_MODEL.md),
   consulted for descriptive context and cited by name where it supplies the
   working vocabulary this contract formalizes, but not itself a frozen or
   canonical authority;
6. the [M42 Architecture Proposal](M42_ARCHITECTURE_PROPOSAL.md) (§0, §3,
   §4.1, Component B, §6 M42-WP2 charter, §7 dependency graph), asserted
   confirmed per this document's operating instruction (§1.4); and
7. the [M42-WP1 Candidate Vocabulary and Ownership
   Register](M42_WP1_PORTFOLIO_CANONICAL_VOCABULARY_AND_OWNERSHIP_REGISTER.md)
   §4 (frozen baseline) and §6.4 (Portfolio Base Currency), and the
   [M42-WP1 Roadmap Reconciliation](M42_WP1_ROADMAP_RECONCILIATION.md) §2.2,
   asserted confirmed per this document's operating instruction (§1.4).

If this specification conflicts with a higher authority, the higher authority
governs and the conflicting clause here is invalid. This specification cites
upstream authority; it does not summarize it into replacement authority.

### 1.2 Normative language

`MUST`, `MUST NOT`, `SHALL`, `SHALL NOT`, `MAY`, and `SHOULD` are normative
within this specification and constrain what Independent Review may accept.
They acquire no repository authority beyond this work package's own governed
confirmation.

### 1.3 Non-reopening

This specification does not reopen, reinterpret, extend, correct, or replace
any decision of `M34-D-0002`, `M34-D-0003`, `M36-WP1-A01/A09`, or M42-WP1.
Portfolio Identity, Accounting Scope, and Portfolio Membership are cited
exactly as `GLOSSARY.md` states them; Portfolio Base Currency's owner,
five-part-gate proof, and disposition are cited exactly as M42-WP1 §6.4
confirmed them. Where this document appears to add words to any of the four,
those words are contract-specification elaboration of an already-fixed
meaning, never a new meaning.

### 1.4 Operating instruction on the WP1-confirmation gap

M42-WP1's own front matter recorded that the M42 Architecture Proposal's
Independent Review and Independent Confirmation were asserted, in a chat
session, to have occurred, without a committed
`M42_ARCHITECTURE_INDEPENDENT_REVIEW.md` /
`M42_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` pair on disk — and it
proceeded on the basis that the register itself is "written to be consistent
with the proposal exactly as committed" and does not rely on any correction
the absent review might have required (WP1 front matter; WP1 §7). This
document is instructed, by the same operating pattern, that M42-WP1 is
`COMPLETE AND CONFIRMED` and that all six candidate dispositions in its §8
Summary Disposition Table are frozen. Consistent with WP1's own discipline,
this document:

- proceeds on that instruction without re-litigating any WP1 disposition;
- does not itself fabricate a committed
  `M42_WP1_INDEPENDENT_CONFIRMATION.md` record, since this document has no
  authority to create one;
- notes, as WP1 §7 noted for the layer above it, that the missing
  confirmation artifact for WP1 is a repository-hygiene item this document
  flags but does not resolve; and
- writes every citation to WP1 in this document exactly as WP1's committed
  text reads today, so that closing the hygiene gap later requires no
  correction to this document's citations.

---

## 2. Explicit Non-Authority

This specification defines a documentary contract only. It does not define or
authorize:

- source code, a schema implementation, a migration, a service, an adapter,
  or a reference implementation;
- runtime construction, persistence, an API, an SDK, or a UI;
- provider selection, provider behavior, or a currency-conversion or FX-rate
  computation of any kind;
- a formula, a production catalog entry, or a computation kernel — every NAV,
  return, and cash-flow formula remains exactly as
  `PORTFOLIO_CALCULATION_RULES.md` states it;
- lifecycle-transition commands, workflows, or transition-legitimacy
  semantics (`create`, `activate`, `clone`, `merge`, `import`, `export`) —
  those are M42-WP6's citation-only territory and, beyond citation, M36's
  deferred territory; and
- production adoption or executable validation of any kind.

---

## 3. Scope

This work package governs, and only governs:

- the reuse-only citation contract for Portfolio Identity, Accounting Scope,
  and Portfolio Membership (§5);
- the boundary-integrity and replay-never-crosses-a-boundary invariants
  stated as contract text over those three frozen coordinates (§5.4–5.5);
  and
- the field-level contract for Portfolio Base Currency, the one coordinate
  M42-WP1 confirmed `ADMIT` to Ledger & Accounting and assigned to this work
  package to carry (§6).

It does not govern:

- Investment Universe, Portfolio Benchmark Declaration, or Portfolio
  Composition (M42-WP3, WP5, WP7 — different components, different owners,
  and, per the WP1 Roadmap Reconciliation, WP2 precedes them but does not
  specify their content);
- Portfolio Lifecycle State's transition vocabulary (M42-WP6, reuse-only for
  the *state* itself, not authored here either);
- accounting arithmetic, NAV/return formulas, or cost-basis rules (frozen in
  `PORTFOLIO_CALCULATION_RULES.md`); or
- any candidate M42-WP1 dispositioned `REJECT` (Portfolio Policy, Investment
  Universe Membership) or left unresolved — no such field appears anywhere in
  this contract.

---

## 4. Exact Upstream Consumption

This specification consumes, without re-derivation:

| Frozen/confirmed authority | Exact coordinate consumed | WP2 prohibition |
|---|---|---|
| `M34-D-0002`; `GLOSSARY.md` "Portfolio Identity" | The stable identifier of one portfolio container; establishes accounting identity only | No new identity field, no strategy/goal/policy/analytics/UI meaning added to Identity |
| `M34-D-0002`; `GLOSSARY.md` "Accounting Scope" | The accounting boundary to which holdings, transactions, cash, and balances belong; every semantic projection of one portfolio refers to the same scope | No redefinition; no downstream domain, including this one, may define a second scope for one portfolio |
| `M34-D-0003`; `GLOSSARY.md` "Portfolio Membership" | The Ledger fact that a holding or instrument belongs to one or more Portfolio Accounting Scopes | No investment interpretation or cross-portfolio exposure meaning attached |
| `M34-D-0003`; `GLOSSARY.md` "Cross-Portfolio Aggregation" | Cited for boundary completeness only; a mathematical aggregation across scopes, adding no investment meaning | Not specified further here — Wealth Intelligence's own territory (Cross-Portfolio Exposure) is untouched |
| `M36-WP1-A01`, `M36-WP1-A09`; `GLOSSARY.md` "Portfolio Lifecycle State" | Cited for boundary completeness only; qualifies what a portfolio may do next, never rewrites Identity or Accounting Scope | No transition vocabulary is authored here; full reuse contract is M42-WP6's, not this document's |
| [`PORTFOLIO_DOMAIN_MODEL.md`](../architecture/PORTFOLIO_DOMAIN_MODEL.md) line 48, line 262 | "Replay never reaches across a portfolio boundary"; "One ledger per portfolio, every event in exactly one ledger, all state derived by replay, nothing crossing the boundary unclassified" | Restated as a contract invariant (§5.5), not re-derived or altered |
| M42-WP1 register §6.4 | Portfolio Base Currency's confirmed `ADMIT` disposition, owner (Ledger & Accounting), Purpose, Owner, Non-owner, Permitted/Forbidden inputs, Proposed exact definition, Constitutional constraints, and passed five-part gate | No re-litigation of the disposition; no field beyond what §6.4 already admitted |
| M42-WP1 Roadmap Reconciliation §2.2 | The instruction that Base Currency is "confirmed, owned work for M42-WP2... not an optional citation" | Fulfilled at §6 below |

---

## 5. Component B — Portfolio Identity, Accounting Scope & Membership Contract (reuse-only)

### 5.1 Portfolio Identity — citation

Portfolio Identity is the stable identifier of one portfolio container. It
establishes accounting identity. It does not own strategy, goals, decision
policy, analytics, or UI selection. Owned by Ledger & Accounting. Governed by
`M34-D-0002`. This contract adds no field, exception, or alternate meaning.

### 5.2 Accounting Scope — citation

Accounting Scope is the accounting boundary to which a portfolio's holdings,
transactions, cash, and balances belong. Every semantic projection of one
portfolio refers to the same Accounting Scope; no downstream domain,
including Portfolio Intelligence's future Composition (M42-WP7), may
redefine it. Owned by Ledger & Accounting. Governed by `M34-D-0002`. This
contract adds no field, exception, or alternate meaning.

### 5.3 Portfolio Membership — citation

Portfolio Membership is the Ledger fact that a holding or instrument belongs
to one or more Portfolio Accounting Scopes. It is not an investment
interpretation or a cross-portfolio exposure measure — that interpretation is
Wealth Intelligence's frozen Cross-Portfolio Exposure, untouched by this
document. Owned by Ledger & Accounting. Governed by `M34-D-0003`. This
contract adds no field, exception, or alternate meaning.

### 5.4 Boundary integrity invariant

**Cardinality distinction (required by IR-1; RC-1 removes the unregistered
term "holding-record" and restates the distinction using only already-frozen
vocabulary).** `M34-D-0002`'s Accounting Scope entry and `M34-D-0003`'s
Portfolio Membership entry each use the word "holding," in two different
senses, without conflict:

- **Accounting Scope's sense:** Accounting Scope is "the accounting boundary
  to which a portfolio's holdings, transactions, cash, and balances belong"
  (`GLOSSARY.md`, `M34-D-0002`). In this sense, a holding is a portfolio-
  scoped fact — one instance of what belongs to one portfolio's ledger,
  exactly as one transaction, one cash movement, or one balance does. Each
  such portfolio-scoped fact belongs to exactly one Accounting Scope.
- **Portfolio Membership's sense:** Portfolio Membership is "the Ledger fact
  that a holding or instrument belongs to one or more Portfolio Accounting
  Scopes" (`GLOSSARY.md`, `M34-D-0003`). In this sense, "a holding or
  instrument" is considered across the platform, not inside one portfolio's
  ledger alone — the same instrument (for example, one company's stock) may
  be held within many different portfolios at once, each such portfolio
  relationship recorded by Portfolio Membership.

Neither frozen entry redefines the other's sense of the word, and this
contract does not merge them into one term or coin a new one. The invariant
below states only the first, Accounting-Scope sense; it says nothing about,
and does not narrow, the second, Portfolio-Membership sense.

**Statement:** Every portfolio-scoped fact — every holding, transaction, cash
movement, and balance that `M34-D-0002`'s Accounting Scope entry enumerates
as belonging to a portfolio — resolves to exactly one Accounting Scope. No
such fact is ownerless, and no such fact resolves to more than one scope.
This statement is silent on, and does not constrain, how many Accounting
Scopes the same instrument may be a member of across the platform through
Portfolio Membership — that is `M34-D-0003`'s own one-or-more rule, stated
above and left exactly as it already reads.

This invariant is not newly authored here; it restates, as an explicit
contract clause, what `M34-D-0002`'s Accounting Scope definition and
`PORTFOLIO_DOMAIN_MODEL.md` §2 ("The Portfolio is an accounting boundary; the
boundary is sacred... every event in exactly one ledger") already require. Its
purpose in this document is to give the M42 Composition (M42-WP7) and every
other consumer a citable, one-sentence statement of the property they may
assume without re-deriving it from the frozen prose each time.

**Constitutional constraints:**

- A portfolio-scoped fact that would resolve to zero or to more than one
  Accounting Scope is not valid under this contract; resolving that
  condition is an accounting-engine concern outside this specification's
  documentary authority.
- This invariant MUST NOT be read as limiting an instrument to membership in
  a single Accounting Scope; Portfolio Membership's frozen one-or-more
  cardinality (`M34-D-0003`) governs that question exclusively and is not
  narrowed by this section.
- Cross-Portfolio Aggregation (`M34-D-0003`) does not violate this invariant:
  it aggregates facts that each individually still resolve to exactly one
  scope, and it "retains every contributing scope" (`GLOSSARY.md`,
  Cross-Portfolio Aggregation) rather than merging them into one.

### 5.5 Replay-never-crosses-a-boundary invariant

**Statement:** A portfolio's state, deterministically reconstructed by
replaying its own ledger, never reads, requires, or reaches across another
portfolio's Accounting Scope to produce its result.

This invariant restates, verbatim in substance, `PORTFOLIO_DOMAIN_MODEL.md`
line 48 ("Replay never reaches across a portfolio boundary; that isolation is
what makes it tractable and trustworthy") and line 262 ("all state derived by
replay, nothing crossing the boundary unclassified"). It authors no new
replay mechanism, algorithm, or exception; it fixes, as a contract this work
package is accountable for, that the property those lines describe is a
requirement M42's Composition and every future consumer may rely on.

**Scope correction (required by IR-2).** `PORTFOLIO_DOMAIN_MODEL.md` §1's
description of a mirrored, two-sided ledger event for inter-portfolio money
movement is Level-4 descriptive context, not frozen or canonical authority
(§1.1 above), and is not a coordinate `M34-D-0002/0003` defines. This
contract does not adopt it as a WP2 rule. WP2 authors no mirrored-transfer
protocol, no two-sided-completeness rule, and no cross-portfolio transfer
mechanism of any kind; whatever mechanism eventually governs money moving
between two portfolios is entirely outside this work package's authority and
is not fixed, constrained, or implied by this contract in either direction.

**Constitutional constraints:**

- No coordinate this contract specifies (Identity, Accounting Scope,
  Membership, or Base Currency) may be defined in a way that requires reading
  a second Accounting Scope to resolve the first — this is the sole
  constraint the replay-isolation invariant imposes.
- This contract takes no position on, and does not require, any particular
  mechanism, protocol, or completeness rule for how a transfer between two
  portfolios' boundaries is recorded; that is outside WP2's scope and is not
  decided here in either direction.

### 5.6 Five-part gate — reaffirmation, not re-derivation

Portfolio Identity, Accounting Scope, and Portfolio Membership are frozen,
pre-existing coordinates admitted under `M34-D-0002/0003`, outside the M42
architecture's own five-part gate (which governs *candidate* admission, not
reuse). This contract does not re-run the gate against them; it cites them.
The boundary-integrity and replay-never-crosses-a-boundary invariants (§5.4,
§5.5) are restatements of already-frozen properties, not new candidates,
and are likewise not independently gated.

---

## 6. Portfolio Base Currency Contract

### 6.1 Disposition and owner — citation, not re-litigation

Portfolio Base Currency was confirmed `ADMIT` at M42-WP1's Stage A gate
(register §6.4), owner **Ledger & Accounting**, as a new, named coordinate
proven on the register's own five-part-gate proof — not asserted to have
been already silently present, unnamed, inside `M34-D-0002`'s frozen text.
This document does not reopen that finding. Per the WP1 Roadmap
Reconciliation §2.2, this coordinate is "confirmed, owned work for M42-WP2...
not an optional citation," and this section discharges that obligation.

**Proposed exact definition (cited verbatim in substance from WP1 §6.4):**
Portfolio Base Currency is the single, explicit currency reference, drawn
from Asset Foundation's frozen currency-classification vocabulary, in which
one Portfolio Identity's NAV, returns, and benchmark comparisons are
expressed. It is set at portfolio creation and changed only as an explicit,
recorded event — never a silent reinterpretation of the meaning of a
historical number — consistent with the immutability-of-accounting-fact
discipline Ledger & Accounting already applies to every other coordinate it
owns.

### 6.2 Currency-reference coordinate (corrected — IR-3)

**Correction of an overstated claim.** Asset Foundation's frozen charter
(`asset_foundation.md` §2, item 3, "Classification") names "currency of
denomination" as one dimension of its descriptive taxonomy, alongside asset
class, sector, region, and wrapper qualification. That frozen text states
that this dimension exists and that Asset Foundation owns it; it does not
itself publish a closed enumeration, code list, or exact identifier format
(for example, it does not state or require an ISO 4217 code) for currency
values. Neither does `GLOSSARY.md`'s "Asset Classification" or "Unit
Semantics" entries — Unit Semantics governs how a *kind* is counted (discrete
or continuous, sign, conservation), a different question from which currency
denominates an asset or a portfolio. The prior revision of this section
conflated these three sources into an assertion of an "exact... format" and a
"closed currency vocabulary" that the frozen corpus does not, at present,
itself define. This section corrects that overstatement without inventing a
new taxonomy, a new ISO requirement, or a new Asset Foundation concept.

**What this contract can truthfully specify:** Portfolio Base Currency's
value **MUST** be a single reference to the same currency-of-denomination
coordinate Asset Foundation's frozen Classification dimension already names
for an asset — the identical dimension, cited by exact name and owner,
without redefinition, duplication, or a parallel enumeration. Concretely:

- the reference **MUST** identify exactly one currency, expressed using
  whatever identifier form Asset Foundation's own frozen currency-of-
  denomination Classification values already take — this contract does not
  itself mint a format, because none is frozen for it to cite yet;
- the reference **MUST NOT** introduce a second, Portfolio-Intelligence- or
  Ledger-owned currency taxonomy, code list, or enumeration parallel to Asset
  Foundation's Classification dimension — one term, one meaning, one home
  (Platform Architecture §12, V1) — regardless of whether that dimension's
  own exact format is yet published;
- the reference **MUST** be scoped to exactly one Portfolio Identity; it
  **MUST NOT** be ambient, defaulted, or shared across portfolios (a
  multi-portfolio person may declare a different Base Currency per
  portfolio; each declaration is independent); and
- the reference carries **no rate, no conversion factor, and no computed
  value** — it names the unit, nothing else.

**Dependency, not a WP2 obligation to resolve:** publishing the exact
currency-identifier format (an enumeration, a code standard, or otherwise) is
Asset Foundation's own governed concern under its Classification charter, not
a question this work package answers or defers improperly. Until Asset
Foundation publishes that exact format, Portfolio Base Currency's contract is
complete at "a single reference to Asset Foundation's currency-of-
denomination coordinate for one Portfolio Identity" — the same closure the
five-part gate at WP1 §6.4 already tested and passed (§6.5 below) — and does
not require this document to invent a format Asset Foundation has not yet
frozen.

### 6.3 Event-sourced-change mechanism

Portfolio Base Currency is set once, at portfolio creation, and thereafter
changes only through an explicit, recorded event — never an in-place
overwrite of the stored value:

- a change **MUST** be represented as a distinct recorded event on the
  portfolio's own ledger history, carrying an effective point after which the
  new currency reference applies;
- a change event **MUST NOT** retroactively alter the currency in which any
  historical NAV, return, or benchmark-comparison figure was expressed — the
  historical figures remain expressed in whatever currency was in effect when
  they were recorded, exactly as Law 2 (immutability) and Law 4 (no silent
  reinterpretation) already require of every other Ledger & Accounting fact;
  and
- this document specifies only that such an event **MUST** exist as a
  concept and **MUST** carry this non-retroactivity property; it does not
  specify the event's storage shape, schema, or runtime mechanics — those are
  explicitly outside this document's persistence and implementation
  authority (§2).

This mirrors, rather than duplicates, the discipline `GLOSSARY.md`'s
Definition Version entry already states for a structurally similar problem
("Recorded facts replay under the version that admitted them. Definitions
bind forward, never backward") — cited here as a pattern precedent, not as a
shared coordinate.

### 6.4 Worked example — Portfolio Base Currency vs. FX Observation (corrected — IR-4)

**Correction of authored computation behavior.** The prior revision of this
section stated that a foreign-currency holding "converts... only inside the
frozen NAV computation, using a canonical FX observation looked up at
computation time." No such conversion step, FX operand, or lookup timing
exists in `PORTFOLIO_CALCULATION_RULES.md`'s frozen NAV formula (§9 there:
NAV is `cash_balance + equity_value`, with `equity_value` defined as shares
times current price). That sentence authored new calculation behavior this
work package has no authority to create (§2). It is removed. The corrected
example draws only the semantic distinction between the two coordinates,
without describing how, whether, or when any conversion occurs:

- **Portfolio Base Currency** is a declaration: "this portfolio's NAV,
  return, and benchmark comparisons are expressed in THB." That sentence is
  the coordinate's entire content — a currency reference, nothing more, and
  nothing about how any figure is computed.
- **FX Observation** is a different, differently-owned coordinate entirely:
  a canonical Market Intelligence observation of an exchange rate
  (`MARKET_DATA_PLATFORM.md`), owned, produced, and consumed under Market
  Intelligence's own frozen rules — never part of, never redefined by, and
  never authored by this contract.
- **The distinction this contract draws, and no more:** Portfolio Base
  Currency never carries a rate, a converted figure, or any computed value —
  those would be FX Observation content or NAV-formula output, neither of
  which this coordinate is. This contract takes no position on whether, when,
  or how a foreign-currency-denominated holding's value is expressed in a
  portfolio's Base Currency; whatever `PORTFOLIO_CALCULATION_RULES.md` states
  or comes to state on that question is entirely its own, unchanged and
  unamended by this document. Multi-currency *holdings* under one Base
  Currency are permitted by the Portfolio Domain Model's descriptive text
  (§3 there), a fact this contract notes without prescribing, or asserting
  the existence of, any computation mechanism for it.
- **Illustration of the forbidden shape:** a schema or contract in which
  "Base Currency" itself carries a rate value, or in which changing Base
  Currency silently recomputes or reinterprets a historical figure, is not
  this coordinate — it is the R6 hazard the M42 Architecture Proposal names
  at §9 ("Treating Base Currency as a mutable display setting would silently
  rewrite the meaning of every historical number"), and is inadmissible under
  §6.3's non-retroactivity requirement.

### 6.5 Five-part gate — reaffirmation, not re-derivation

Portfolio Base Currency's five-part ownership-boundary gate was run and
passed in full at M42-WP1 register §6.4 (permitted subject: pass; permitted
inputs: pass; output meaning: pass; prohibited inputs: pass; prohibited
semantics: pass). This document does not re-run that gate; §6.2–6.4 above
supply the field-level detail the gate's passing result presupposed but did
not itself spell out, discharging WP1's own stated "Future contract
acceptance evidence" obligation for this coordinate (register §6.4): the
currency-reference coordinate, truthfully bounded to what Asset Foundation's
frozen Classification dimension actually publishes today (§6.2, corrected),
the exact "change is a recorded event, never a silent reinterpretation"
mechanism (§6.3), and a worked example distinguishing Portfolio Base Currency
from FX Observation without authoring new computation behavior (§6.4,
corrected).

### 6.6 Non-owner discipline (corrected — IR-5)

Consistent with WP1 §6.4's Non-owner finding, this contract confirms that
Portfolio Intelligence does not, and may not, **own** or **redefine**
Portfolio Base Currency. Ownership remains, exclusively, Ledger & Accounting's.

This is distinct from **citation and carriage**, both of which Portfolio
Intelligence retains and requires. WP1's confirmed Portfolio Composition
record (register §6.5) permits Portfolio Base Currency as a cited input to
the Composition, and §9 below confirms that M42-WP7's Portfolio Composition
— owned by Portfolio Intelligence — cites this coordinate. The prior revision
of this section stated Portfolio Intelligence "does not carry" Base
Currency; that overstated non-ownership into a no-carriage rule, which would
have contradicted the Composition's own confirmed input and this document's
own §9 handoff. It is corrected:

- Portfolio Intelligence **does NOT own** Portfolio Base Currency;
- Portfolio Intelligence **MAY cite** Portfolio Base Currency;
- Portfolio Intelligence **MAY compose** using this Ledger & Accounting
  coordinate (as M42-WP7's Portfolio Composition does, per §9); and
- Portfolio Intelligence **MUST NOT redefine** Portfolio Base Currency — any
  Portfolio Intelligence artifact (Investment Universe, Portfolio Benchmark
  Declaration, Portfolio Composition) that needs the currency a portfolio
  reports in **MUST** cite this Ledger & Accounting coordinate at its
  confirmed meaning, never declare, mutate, or maintain a competing copy of
  its own.

---

## 7. Negative Corpus — Explicit Non-Goals for M42-WP2

This work package does **not**, in this or any future revision:

- redefine Portfolio Identity, Accounting Scope, or Portfolio Membership, or
  add a field, exception, or alternate meaning to any of the three beyond
  what `M34-D-0002/0003` already state;
- compute an FX rate, a currency conversion, or any converted value;
- author lifecycle-transition vocabulary, a lifecycle command, or a
  transition-legitimacy rule (M42-WP6's territory, and beyond citation, M36's
  deferred territory);
- carry, cite as owned, or rely upon any candidate M42-WP1 dispositioned
  `REJECT` (Portfolio Policy, Investment Universe Membership) or otherwise
  left unresolved;
- author any accounting arithmetic — NAV, return, or cost-basis formulas
  remain exactly as `PORTFOLIO_CALCULATION_RULES.md` states them;
- introduce a second currency taxonomy parallel to Asset Foundation's
  classification vocabulary;
- migrate any coordinate's ownership to Portfolio Intelligence or any other
  domain; Base Currency's owner remains Ledger & Accounting, exactly as WP1
  confirmed; or
- implement a module, schema, endpoint, runtime, or persistence mechanism, or
  author any committed executable validation artifact.

---

## 8. Compatibility Matrix

| Frozen/confirmed authority | Compatibility |
|---|---|
| `M34-D-0002` | Compatible. Portfolio Identity and Accounting Scope are cited, not redefined; Base Currency is admitted as an additional named coordinate within Ledger & Accounting's already-frozen accounting-identity purview, not a reinterpretation of what `M34-D-0002` itself enumerates. |
| `M34-D-0003` | Compatible. Portfolio Membership and Cross-Portfolio Aggregation are cited, not redefined; no investment or exposure meaning is added. |
| `M36-WP1-A01`, `M36-WP1-A09` | Compatible. Portfolio Lifecycle State is cited for boundary completeness only (§4); its full reuse contract and provenance discipline remain M42-WP6's own obligation, not duplicated here. |
| `PORTFOLIO_CALCULATION_RULES.md` | Compatible. No NAV, return, or cash-flow formula is added, altered, or parameterized differently by this document. This document defines the Portfolio Base Currency coordinate; it does not assert that the formula text currently references, requires, or consumes that coordinate, and takes no position on whether or how it might in the future. |
| M42-WP1 register §6.4 | Compatible. Owner, disposition, and five-part-gate result are cited exactly as confirmed; §6.2–6.4 of this document discharge, without altering, WP1's own stated future-contract obligation. |
| M42 Architecture Proposal, Component B (§5) | Compatible. This document specifies exactly Component B's stated purpose — "the canonical statement that a Portfolio *is* an accounting boundary... by citation of `M34-D-0002/0003`... authoring no new rule" — plus the Base Currency carry-forward the Roadmap Reconciliation assigned to it. |

---

## 9. Consequence for M42-WP7

Once this contract is independently confirmed, M42-WP7's Portfolio
Composition — owned by Portfolio Intelligence — **MAY cite and compose
using**, as permitted inputs at their confirmed meaning only:

- Portfolio Identity, Accounting Scope, and Portfolio Membership (§5, cited
  from `M34-D-0002/0003`, unchanged); and
- Portfolio Base Currency (§6, cited from this contract's field-level
  detail, itself citing WP1's confirmed admission).

Citing and composing using these coordinates in the Composition does not
transfer, share, or dilute their ownership: Ledger & Accounting remains the
sole owner of all four, exactly as §5 and §6.6 state; Portfolio Intelligence
owns only the terminal Composition that cites them (consistent with §6.6's
corrected citation/carriage discipline). M42-WP7 **MUST NOT** treat this
contract as licensing any field beyond what §5 and §6 specify, and **MUST
NOT** derive a measure (a converted NAV value, a rate, a comparison) from
Base Currency — the coordinate composes as a named unit reference only,
consistent with the M42 architecture's no-derived-measure invariant (§4.3
part 3 of the Architecture Proposal).

---

## 10. Acceptance Criteria

This specification is acceptable only if Independent Review confirms:

1. No field, exception, or alternate meaning is added to Portfolio Identity,
   Accounting Scope, or Portfolio Membership beyond `M34-D-0002/0003` as
   currently frozen, and the boundary-integrity invariant's cardinality
   distinction (§5.4) does not narrow, restate, or reinterpret Portfolio
   Membership's frozen one-or-more cardinality.
2. The boundary-integrity and replay-never-crosses-a-boundary invariants
   (§5.4–5.5) are restatements of already-established properties, introducing
   no new mechanism, exception, accounting rule, or cross-portfolio transfer
   protocol.
3. Portfolio Base Currency's owner, disposition, and five-part-gate result are
   cited from M42-WP1 §6.4 exactly, without re-litigation.
4. Portfolio Base Currency's currency-reference coordinate, event-sourced-
   change mechanism, and worked example (§6.2–6.4) are internally consistent
   with WP1's Purpose, Owner, Permitted/Forbidden-inputs, and Proposed-exact-
   definition fields, add no capability WP1 did not already admit, and do not
   overstate Asset Foundation's currently published currency vocabulary.
5. No accounting arithmetic, FX computation, FX lookup, or NAV/return formula
   is authored, altered, or parameterized differently than
   `PORTFOLIO_CALCULATION_RULES.md` already states.
6. No candidate M42-WP1 dispositioned `REJECT` or left unresolved (Portfolio
   Policy, Investment Universe Membership, or the unresolved Portfolio
   Policy residue fields) is reintroduced as a field, input, rule, or owned
   concept anywhere in this contract; exclusionary mention of those names is
   permitted.
7. No lifecycle-transition vocabulary is authored; Portfolio Lifecycle
   State's reuse contract remains fully deferred to M42-WP6.
8. Implementation, runtime, provider, persistence, API, production, and
   executable-validation authority remain `NONE`, and no computation-time,
   lookup, or runtime behavior is stated in any worked example.
9. Portfolio Intelligence's citation and carriage of Portfolio Base Currency
   (via M42-WP7's Composition) are stated as permitted and are not confused
   with, or restricted by, its non-ownership of the coordinate (§6.6, §9).
10. This document's statement of `docs/GLOSSARY.md`'s current state (§11)
    matches the repository as it actually stands, neither claiming a
    synchronization that has not occurred nor reopening WP1's own
    confirmation condition for performing it.

---

## 11. Repository and Governance Effects

This specification creates only:

- `docs/implementation/M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md`
  (this document).

It modifies no frozen artifact, no domain constitution, `docs/GLOSSARY.md`,
the Decision Log, the Implementation Index, Graphify output, or source code.

**Corrected repository-state statement (IR-6).** `GLOSSARY.md` synchronization
for Portfolio Base Currency is WP1's own confirmation condition (register
§6.4: "add a `GLOSSARY.md` entry titled 'Portfolio Base Currency'... in the
same change the confirmation is recorded"). As of this revision,
`docs/GLOSSARY.md` contains no "Portfolio Base Currency" entry. This document
does not perform that synchronization — it is outside this document's own
authority and belongs to WP1's own confirmation change — and does not assert
that it has already occurred. Closing that gap is a precondition of WP1's
own Independent Confirmation being complete in the repository, not a task
this document undertakes or a reason to reopen WP1's disposition. Decision
Log reconciliation and Graphify refresh remain reserved to M42 Epic Closeout,
after M42-WP7. Creating this specification is authority to perform none of
those.

---

## Final Status

**`READY_FOR_INDEPENDENT_CONFIRMATION`**

All six required corrections from the [Independent Governance
Review](M42_WP2_INDEPENDENT_REVIEW.md) (IR-1 through IR-6), and both residual
corrections identified at the subsequent Independent Confirmation pass (RC-1,
RC-4), are applied. This document does not perform its own Independent
Confirmation; that determination belongs to a subsequent, separate review
pass.
