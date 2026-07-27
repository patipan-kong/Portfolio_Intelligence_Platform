# M42-WP3 Stage A — Investment Universe Vocabulary & Semantic Surface Register

**Stage:** M42-WP3 Stage A

**Date:** 2026-07-27

**Artifact type:** Documentation-only semantic registration

**Canonical governed noun:** **Investment Universe**

**Vocabulary disposition:** `REUSE` — no new governed vocabulary admitted

**Owner:** Portfolio Intelligence, as a specialization of Portfolio Strategy
Metadata

**Implementation authority:** `NONE`

**Persistence authority:** `NONE`

**Runtime authority:** `NONE`

**API authority:** `NONE`

**Serialization authority:** `NONE`

**Executable-validation authority:** `NONE`

**Evaluation authority:** `NONE`

**Enforcement authority:** `NONE`

**Stage status:** `COMPLETE AND CONFIRMED`

---

## 1. Executive Summary

This register establishes the complete governed semantic surface for the
M42-WP3 Investment Universe Declaration before any Stage B contract is
drafted.

**Investment Universe remains the sole governed noun.** It is reused exactly
as confirmed by M42-WP1: a named, immutable-until-explicitly-revised,
portfolio-scoped declaration of intended holdings scope, composed exclusively
from Asset Foundation-owned descriptive vocabulary. Portfolio Intelligence
owns Investment Universe as a specialization of the already-frozen Portfolio
Strategy Metadata allocation.

Stage A admits no new governed noun and does not alter any existing definition
or ownership allocation. The declaration cites:

- Portfolio Identity and Accounting Scope from the confirmed M42-WP2
  contract;
- Asset Classification, Capability, Market, and Currency from Asset
  Foundation authority; and
- Portfolio Base Currency only as a Ledger & Accounting-owned adjacent
  coordinate when necessary to prevent confusion with an Investment Universe
  Currency criterion.

Citation, reference, carriage, and later composition do not transfer, share,
or dilute ownership.

**Investment Universe Membership remains `REJECT`.** No admitted surface in
this register determines whether an instrument belongs to an Investment
Universe. No evaluation, matching, membership, policy, limits, execution,
validation, refusal, verdict, or enforcement semantics exist in the admitted
Investment Universe surface.

This document registers meaning only. It defines no field model, record shape,
cardinality of criteria, identifier format, persistence model, runtime object,
API, serialization, executable validator, evaluation procedure, or enforcement
mechanism. Those matters are either reserved for Stage B under the handoff in
§7 or remain entirely outside M42-WP3.

---

## 2. Vocabulary Register

### 2.1 Upstream authority and precedence

This register consumes the following authority without reopening it:

| Precedence | Authority | Exact Stage A use | Non-reopening rule |
|---|---|---|---|
| 1 | Frozen Platform Architecture, domain constitutions, and M34 ownership decisions, especially `M34-D-0002`, `M34-D-0004`, and `M34-D-0007` | Constitutional domain boundaries and the separation of identity, knowledge, judgment, and enforcement | No domain, layer, gate, law, or frozen ownership allocation is amended |
| 2 | [M42 Architecture Proposal](M42_ARCHITECTURE_PROPOSAL.md), especially §§3–5 and its negative corpus | Component C purpose, five-part ownership gate, Portfolio Intelligence declaration boundary, Asset Foundation citation boundary, and prohibition on a belonging predicate | The milestone architecture is `COMPLETE AND FROZEN`; candidate-era wording is read through the later confirmed WP1 dispositions |
| 3 | [M42-WP1 Portfolio Canonical Vocabulary and Ownership Register](M42_WP1_PORTFOLIO_CANONICAL_VOCABULARY_AND_OWNERSHIP_REGISTER.md), especially §§6.1, 6.6, and 8 | Confirmed admission, definition, owner, inputs, constraints, and negative boundary of Investment Universe; confirmed rejection of Investment Universe Membership | No disposition, definition, owner, or gate result is re-litigated |
| 4 | [M42-WP2 Portfolio Identity, Accounting Scope, Membership & Base Currency Contract Specification](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md), especially §§4–6 | Portfolio Identity and Accounting Scope citation; separation from Portfolio Membership; Ledger & Accounting ownership of Portfolio Base Currency; citation-without-transfer discipline | No identity, accounting boundary, membership, currency-reference, event, or replay rule is added |
| 5 | [M42-WP3 Architecture Proposal](M42_WP3_ARCHITECTURE_PROPOSAL.md), especially §§2–7, §9, and §10 | Confirmed WP3 semantic allocation, admitted/rejected surfaces, Stage A obligation, Stage B boundary, and WP7 handoff | No implementation-neutral shape is drafted during Stage A; the architecture's unresolved portfolio-level declaration cardinality remains unresolved |
| 6 | [M42-WP3 Architecture Closeout](M42_WP3_CLOSEOUT.md) | Canonical confirmation that M42-WP3 Architecture is `COMPLETE AND CONFIRMED`, with all ownership and non-authority states unchanged | This Stage A artifact does not modify architecture status or begin implementation |
| 7 | [Asset Foundation](../architecture/asset_foundation.md), together with its frozen canonical vocabulary | Ownership of Asset Classification, Capability, market classification, currency of denomination, and their values | WP3 does not create taxonomies, values, aliases, or identifier formats |

Where a lower-precedence document summarizes a higher-precedence authority,
the higher-precedence authority controls. This register narrows nothing,
widens nothing, and resolves no upstream question that the confirmed
architecture left open.

### 2.2 Canonical and reused vocabulary

| Term | Stage A classification | Canonical meaning used here | Owner | Stage A use |
|---|---|---|---|---|
| **Investment Universe** | `REUSE`; sole governed noun | A named, immutable-until-explicitly-revised, portfolio-scoped declaration of the intended scope of holdings for one Portfolio Identity, composed only from Asset Foundation-owned Asset Classification, Capability, Market, and Currency vocabulary; inert descriptive strategy data, never an executable predicate or verdict | Portfolio Intelligence, as a specialization of Portfolio Strategy Metadata | Governed subject of this register |
| **Portfolio Strategy Metadata** | `CITE` / `REUSE` | The frozen Portfolio Intelligence-owned umbrella specialized by Investment Universe | Portfolio Intelligence | Establishes the existing owned home; it is not a second WP3 noun |
| **Portfolio Identity** | `CITE` / `REUSE FROM WP2` | The stable identifier of one portfolio container; establishes accounting identity only | Ledger & Accounting | Identifies the one portfolio to which a declaration is bound |
| **Accounting Scope** | `CITE` / `REUSE FROM WP2` | The accounting boundary to which one portfolio's holdings, transactions, cash, and balances belong | Ledger & Accounting | Establishes the corresponding accounting boundary that the declaration presupposes and may not redefine |
| **Portfolio Membership** | `DISTINGUISH BY CITATION ONLY` | The Ledger fact that a holding or instrument belongs to one or more Portfolio Accounting Scopes | Ledger & Accounting | Used only to prove that accounting membership is not Investment Universe meaning |
| **Asset Classification** | `CITE` / `REUSE` | Asset Foundation-owned descriptive classification, including the asset-classification dimension | Asset Foundation | One of the four closed criterion categories whose values an Investment Universe may reference |
| **Capability** | `CITE` / `REUSE` | Asset Foundation-owned descriptive capability fact | Asset Foundation | One of the four closed criterion categories whose values an Investment Universe may reference |
| **Market** | `CITE` / `REUSE` | Asset Foundation-owned market classification and its values | Asset Foundation | One of the four closed criterion categories whose values an Investment Universe may reference |
| **Currency** | `CITE` / `REUSE` | Asset Foundation-owned currency-of-denomination classification and its values | Asset Foundation | One of the four closed criterion categories whose values an Investment Universe may reference |
| **Portfolio Base Currency** | `DISTINGUISH BY CITATION ONLY` | The single explicit currency reference in which one Portfolio Identity's NAV, returns, and benchmark comparisons are expressed | Ledger & Accounting | Used only to distinguish an accounting/reporting coordinate from an asset Currency scope criterion |
| **Portfolio Composition** | `DOWNSTREAM CITATION ONLY` | The terminal portfolio-level composition confirmed by WP1 and assigned to M42-WP7 | Portfolio Intelligence | Receives the complete confirmed Investment Universe declaration after Stage B; not defined here |

The words “declaration,” “declared name,” “subject binding,” “scope criteria,”
“criterion category,” “criterion reference,” and “explicit revision” are
ordinary contract language describing facets of Investment Universe. They are
not capitalized governed nouns, independent objects, candidate vocabulary, or
new ownership allocations.

### 2.3 Vocabulary sufficiency determination

The confirmed vocabulary is sufficient for the entire Stage A surface:

1. Investment Universe names the governed declaration.
2. Portfolio Strategy Metadata supplies its already-owned Portfolio
   Intelligence home.
3. Portfolio Identity and Accounting Scope supply the declaration's
   Ledger-owned subject boundary.
4. Asset Classification, Capability, Market, and Currency supply the complete
   closed category vocabulary for inert criteria.
5. Portfolio Base Currency supplies the adjacent Ledger-owned currency
   coordinate needed to state a non-collision.
6. Portfolio Composition supplies the named downstream destination.

No residual semantic surface requires a new noun, owner, lifecycle, or
independent identity. Therefore:

- no candidate vocabulary is opened;
- no rename is required;
- no glossary synchronization is authorized by Stage A; and
- any future discovery that a new governed noun is necessary must stop Stage B
  and return through the frozen vocabulary-governance path before that noun is
  used.

---

## 3. Ownership Register

### 3.1 Coordinate-by-coordinate ownership

Every admitted semantic coordinate has exactly one owner:

| Semantic coordinate | Exact owner | What the owner owns | Explicit non-owners |
|---|---|---|---|
| Investment Universe as a declaration | Portfolio Intelligence | The descriptive strategy meaning of one named, portfolio-scoped declaration of intended holdings scope | Asset Foundation; Ledger & Accounting; Decision Intelligence; Wealth Intelligence; Market Intelligence; Experience Platform; Connectivity & Ingestion; providers; storage; runtime |
| Specialization within Portfolio Strategy Metadata | Portfolio Intelligence | The placement of Investment Universe inside the existing strategy-metadata allocation | No new “Portfolio” owner; no cross-domain shared ownership |
| Declared name, as a semantic facet of Investment Universe | Portfolio Intelligence | The fact that the declaration has an explicit human-declared name | UI labels, provider labels, and catalogues are non-authoritative; the name does not create a standardized universe-name vocabulary |
| Binding to one Portfolio Identity | Ledger & Accounting owns Portfolio Identity; Portfolio Intelligence owns only the fact that its declaration cites that identity | Ledger & Accounting retains accounting identity; Portfolio Intelligence owns no identity semantics | WP3, Asset Foundation, UI selection, provider account identifiers, storage keys |
| Preservation of the corresponding Accounting Scope | Ledger & Accounting | The accounting boundary and its integrity | WP3 may neither create an alternate scope nor interpret intended scope as accounting scope |
| Investment Universe criteria as descriptive declaration facets | Portfolio Intelligence | The choice to cite descriptive criteria as part of intended strategy scope | It does not own the referenced categories or values |
| Asset Classification criterion reference | Asset Foundation owns the category and value; Portfolio Intelligence owns only its citation in the declaration | Classification meaning, taxonomy, and value authority remain Asset Foundation-owned | WP3 private classifications, copied taxonomies, provider labels, UI labels |
| Capability criterion reference | Asset Foundation owns the category and value; Portfolio Intelligence owns only its citation in the declaration | Capability meaning and value authority remain Asset Foundation-owned | WP3 capability invention, capability testing, instrument evaluation |
| Market criterion reference | Asset Foundation owns the category and value; Portfolio Intelligence owns only its citation in the declaration | Market-classification meaning and value authority remain Asset Foundation-owned | WP3 market lists, exchange/provider mappings, execution venues, market eligibility |
| Currency criterion reference | Asset Foundation owns the category and value; Portfolio Intelligence owns only its citation in the declaration | Currency-of-denomination meaning and value authority remain Asset Foundation-owned | WP3 currency codes, FX semantics, conversion rules, Portfolio Base Currency |
| Immutable-until-explicitly-revised semantic condition | Portfolio Intelligence | The declaration's descriptive condition that its meaning does not change silently | No event, command, workflow, version schema, persistence, mutation API, or runtime update mechanism is owned or implied |
| Portfolio Base Currency | Ledger & Accounting | The portfolio accounting/reporting currency coordinate confirmed in WP2 | Portfolio Intelligence and WP3 do not own, default, infer, copy, or mutate it |
| Future instrument-level universe evaluation, if separately chartered | Decision Intelligence territory under separate future authority; not admitted here | Nothing in M42-WP3 | Portfolio Intelligence, Investment Universe, and Asset Foundation do not own a belonging verdict |
| WP7 Portfolio Composition | Portfolio Intelligence under M42-WP7 | The terminal composed surface and any later-authorized portfolio-wide canonical serialization | WP3 does not own composition, field order, schema version, canonical bytes, or serialization |

### 3.2 Explicit non-ownership declarations

This register confirms all of the following:

- Portfolio Intelligence does not own Portfolio Identity, Accounting Scope,
  Portfolio Membership, or Portfolio Base Currency.
- Ledger & Accounting does not own Investment Universe or its descriptive
  strategy meaning.
- Asset Foundation does not own Investment Universe and WP3 does not own
  Asset Classification, Capability, Market, Currency, their taxonomies, their
  values, or their identifier formats.
- Decision Intelligence does not own the declaration, while Portfolio
  Intelligence receives no evaluation, judgment, policy, limit, refusal, or
  enforcement authority from owning it.
- Market Intelligence does not own the declaration and supplies no market
  observation, live price, FX rate, or provider answer to its Stage A meaning.
- Experience Platform presentation, labels, filters, and current selection do
  not define the declaration.
- Connectivity & Ingestion, registries, providers, brokers, storage systems,
  APIs, serializers, and runtime services have custody or implementation roles
  only if separately authorized; they acquire no semantic ownership here.
- M42-WP3 does not own M42-WP7 Portfolio Composition or portfolio-wide
  canonical serialization.

### 3.3 Citation-without-transfer rule

For every cited coordinate:

> The source authority owns the coordinate and its meaning. Investment
> Universe owns only the declaration's exact reference to that coordinate.

Accordingly, citation does not:

- copy or fork the cited coordinate;
- make ownership joint or shared;
- authorize WP3 to rename, normalize, enrich, repair, classify, or version the
  cited value;
- authorize a private identifier, cached authoritative copy, provider-shaped
  alias, or UI label to replace the cited authority;
- make the cited coordinate part of Portfolio Intelligence's owned
  vocabulary; or
- allow a downstream composition to dilute the source owner's authority.

No ownership transfer occurs through citation, reference, carriage, semantic
binding, or later composition.

---

## 4. Semantic Surface Register

### 4.1 Admitted semantic surface

The following table is the complete Stage A admission. Anything not listed is
not admitted by M42-WP3 Stage A.

| Surface | Admitted semantic meaning | Governing vocabulary | Owner boundary | Stage B may later close | Stage A expressly does not define |
|---|---|---|---|---|---|
| Governed subject | One Investment Universe declaration | Investment Universe | Portfolio Intelligence owns the declaration | An implementation-neutral record shape | Runtime class, entity, table, aggregate, API resource |
| Portfolio binding | The declaration belongs to exactly one Portfolio Identity and preserves that identity's corresponding Accounting Scope | Portfolio Identity; Accounting Scope | Ledger & Accounting owns both cited coordinates; Portfolio Intelligence owns only the declaration-to-subject association | Exact subject-reference field and structural requirements | Identity format, storage key, lookup, resolution, cross-portfolio mechanism |
| Explicit declared name | The declaration has an explicit name; examples are illustrative only | Investment Universe plus ordinary “declared name” language | Portfolio Intelligence | Exact field, presence rule, and deterministic representation | Standard catalogue, canonical enumeration of names, UI label, provider name |
| Inert scope criteria | The declaration may state intended holdings scope only through inert descriptive criteria | Investment Universe | Portfolio Intelligence owns the declared choice; referenced meanings remain externally owned | Exact inert data shape and structural closure | Executable expressions, functions, predicates, query languages, matching algorithms |
| Asset Classification category | Criteria may cite Asset Foundation-owned Asset Classification values, including the asset-classification dimension | Asset Classification | Asset Foundation owns category and values; Portfolio Intelligence owns only citation | Exact reference placement and allowed structural form | New classification, reclassification, taxonomy, alias, code list |
| Capability category | Criteria may cite Asset Foundation-owned Capability values | Capability | Asset Foundation owns category and values; Portfolio Intelligence owns only citation | Exact reference placement and allowed structural form | New capabilities, tests, discovery calls, evaluation of an instrument's capabilities |
| Market category | Criteria may cite Asset Foundation-owned Market classification values | Market | Asset Foundation owns category and values; Portfolio Intelligence owns only citation | Exact reference placement and allowed structural form | Market eligibility, allowed venues, execution routing, provider/exchange mappings |
| Currency category | Criteria may cite Asset Foundation-owned Currency-of-denomination values | Currency | Asset Foundation owns category and values; Portfolio Intelligence owns only citation | Exact reference placement and allowed structural form, without inventing an identifier format | Portfolio Base Currency default, FX, conversion, currency policy, invented code format |
| Revision condition | The declaration's meaning is immutable until explicitly revised; no silent reinterpretation is permitted | Investment Universe plus ordinary revision language | Portfolio Intelligence owns the semantic condition only | A representation that preserves the condition without exceeding Stage B authority | Command, event, workflow, authorization, mutation API, persistence, temporal evaluation |
| Downstream handoff | The complete confirmed declaration may be cited and carried by M42-WP7 Portfolio Composition without evaluation, enrichment, repair, or reinterpretation | Investment Universe; Portfolio Composition | WP3 owns the declaration contract; WP7 owns the later terminal composition | Exact contract boundary supplied to WP7 | WP7 record, canonical ordering, schema version, bytes, serialization |

The four criterion categories are closed:

1. Asset Classification;
2. Capability;
3. Market; and
4. Currency.

“Closed” means Stage B may not add a fifth category under this authority. It
does not mean Stage A defines an enumeration of values, a field cardinality, a
set algebra, a range syntax, a comparison operator, or a matching procedure.

### 4.2 Semantic invariants

The admitted surface carries these invariants:

1. **Declaration only.** Investment Universe states intended holdings scope
   and produces no answer about any instrument.
2. **One governed noun.** No facet or referenced coordinate becomes a second
   WP3-governed noun.
3. **One declaration, one subject boundary.** Each declaration binds to
   exactly one Portfolio Identity and its corresponding Accounting Scope.
4. **No portfolio-level declaration-cardinality rule.** This register does
   not determine whether a portfolio has zero, one, or multiple Investment
   Universe declarations.
5. **One-way reference.** Criteria cite Asset Foundation facts; they do not
   own, copy, change, or supersede them.
6. **Strategy scope is not accounting scope.** Investment Universe describes
   intended holdings scope; Accounting Scope establishes the ledger boundary.
7. **Declaration is not membership.** Investment Universe does not store a
   concrete instrument list or a belonging fact.
8. **No ambient default.** Missing declaration meaning cannot be filled from
   another portfolio, provider, UI state, convention, or inferred default.
9. **No verdict.** No belongs/does-not-belong, met/unmet, valid/invalid,
   eligible/ineligible, accepted/rejected, or allowed/prohibited result exists.
10. **No enforcement.** Criteria are not Portfolio Policy, Decision Policy,
    Portfolio Limits, Sector Limits, optimizer constraints, transaction
    validation, or execution eligibility.
11. **No derived measure.** No valuation, performance, return, risk, exposure,
    concentration, attribution, allocation, or recommendation result exists.
12. **No live dependency.** Meaning does not depend on a provider response,
    wall clock, model output, market observation, portfolio holdings, or
    cross-portfolio state.
13. **No implicit base currency.** An asset Currency criterion is not
    Portfolio Base Currency and cannot infer, default, or mutate it.
14. **No silent revision.** Revision is an explicit semantic boundary, but
    Stage A authorizes no revision mechanism.
15. **No ownership transfer.** Citation and downstream carriage preserve each
    source coordinate's owner.

### 4.3 Rejected semantic surface

| Rejected surface | Rejection reason | Authority retained elsewhere |
|---|---|---|
| Instrument-to-universe evaluation | Produces an answer about a specific instrument and converts inert criteria into executable semantics | Not admitted; if ever separately chartered, verdict territory requires Decision Intelligence authority |
| Matching or satisfaction procedure | Introduces comparison, operator, expression, or truth-valued behavior absent from a declaration | Not admitted anywhere in M42-WP3 |
| Investment Universe Membership | Explicitly rejected by confirmed M42-WP1 because its met/unmet verdict fails the output-meaning gate | `REJECT`; no owner under M42 |
| Stored concrete instrument membership list | Replaces declared scope with enumerated membership facts and invites runtime maintenance/evaluation | Portfolio Membership remains a separate Ledger fact, but it is not a substitute |
| Portfolio Policy or Decision Policy | Changes descriptive scope into an allowed/prohibited operating rule | Decision Intelligence retains frozen policy territory |
| Portfolio Limits or Sector Limits | Changes descriptive scope into an enforced constraint or threshold | Decision Intelligence |
| Transaction validation or refusal | Produces validity/refusal behavior rather than descriptive strategy data | Outside WP3; no authority granted |
| Execution eligibility or routing | Converts Market/Capability criteria into actionability, venue, broker, or order semantics | Execution/Decision domains under separate authority |
| Concrete taxonomy or identifier format | Duplicates Asset Foundation ownership and fills gaps without authority | Asset Foundation |
| Portfolio Base Currency as a criterion default | Confuses asset denomination with the portfolio's unit of account | Ledger & Accounting owns Portfolio Base Currency |
| Portfolio Composition or serialization | Assumes the terminal WP7 surface and its deterministic encoding authority | M42-WP7 / Portfolio Intelligence |
| Revision command, event, workflow, or mutation behavior | Expands a semantic condition into lifecycle, persistence, or runtime authority | Not admitted by Stage A or WP3 Architecture |

### 4.4 Forbidden semantic leakage

The following transformations are forbidden even if they are presented as
fields, labels, examples, helper text, pseudocode, schemas, acceptance tests,
or “non-normative” convenience:

| From admitted surface | Forbidden leakage | Why it changes the concept |
|---|---|---|
| Asset Classification criterion | “allowed asset classes,” classification whitelist, or `asset.classification IN universe` | Adds policy or executable matching |
| Capability criterion | capability probe, capability requirement evaluation, or pass/fail result | Adds instrument evaluation |
| Market criterion | allowed market, tradable venue, routing venue, or market-access check | Adds policy, execution, or enforcement |
| Currency criterion | allowed currency, automatic conversion, FX lookup, or Portfolio Base Currency fallback | Adds policy, market data, accounting, or runtime behavior |
| Portfolio binding | shared, ambient, inherited, workspace-selected, or cross-portfolio universe | Breaks the one-portfolio boundary |
| Declared name | canonical universe-name catalogue or provider-supplied authoritative label | Creates a new taxonomy or provider authority |
| Inert criteria | expression language, query, selector, predicate, callback, rule engine, or comparison operators | Creates evaluation/matching capability |
| Revision condition | update command, effective-time behavior, event schema, approval workflow, or silent mutation | Creates lifecycle/runtime/persistence semantics |
| WP7 handoff | enrichment, repair, defaulting, evaluation, field order, canonical bytes, or serializer | Assumes WP7 or implementation authority |

Terminology cannot evade this boundary. A “filter,” “screen,” “resolver,”
“qualifier,” “compatibility check,” “scope check,” “candidate selection,”
“admission rule,” or renamed equivalent is rejected whenever it consumes a
specific instrument or produces a truth-valued, policy, validation, refusal,
execution, or enforcement result.

---

## 5. Rejected Vocabulary

### 5.1 Canonically rejected term

| Term | Disposition | Reason | Consequence for Stage A and Stage B |
|---|---|---|---|
| **Investment Universe Membership** | `REJECT` | It is a predicate that evaluates one instrument against an Investment Universe and produces a met/unmet verdict and possible refusal. Confirmed M42-WP1 found that output meaning inadmissible to the descriptive Portfolio Intelligence surface. | It may not appear as a field, object, method, result, status, relation, rule, vector output, acceptance criterion, or renamed equivalent in the WP3 contract |

This rejection is complete within M42. It is not a deferred WP3 feature and
cannot be revived in Stage B.

### 5.2 Other prohibited or non-admitted labels

The following labels are not governed WP3 vocabulary and must not be used to
smuggle rejected semantics into the declaration:

- Universe Member, Universe Membership, Universe Eligibility;
- Universe Match, Universe Matcher, Universe Matching Result;
- Universe Validation, Universe Validity, Universe Compliance;
- Universe Admission, Universe Permission, Universe Allowlist;
- Eligible Instrument, Ineligible Instrument, Allowed Instrument;
- Scope Predicate, Scope Resolver, Scope Filter, Scope Check;
- Universe Policy, Universe Limit, Universe Constraint;
- Universe Enforcement, Universe Refusal, Universe Violation; and
- any synonymous term whose meaning evaluates, matches, validates, permits,
  rejects, executes, or enforces.

The ordinary phrase “criterion reference” is permitted only for inert citation
of an Asset Foundation-owned value. It must not be upgraded into a governed
“Criterion,” “Rule,” “Expression,” or executable matcher.

---

## 6. Negative Corpus

Each item below is outside the admitted semantic surface. Quoted examples are
negative specimens only and create no vocabulary or contract shape.

| ID | Negative specimen | Rejected because |
|---|---|---|
| NC-01 | “Does instrument X belong to this Investment Universe?” | Asks the rejected membership question |
| NC-02 | “Instrument X matches all universe criteria.” | Produces a matching verdict |
| NC-03 | `belongs(instrument, universe) -> boolean` | Defines an executable truth-valued predicate |
| NC-04 | `classification in allowed_classifications` | Defines an operator and policy/matching semantics |
| NC-05 | “Reject the order because the asset is outside the universe.” | Adds transaction refusal and enforcement |
| NC-06 | “Only eligible instruments may be purchased.” | Adds eligibility policy and execution control |
| NC-07 | “The universe contains instrument identifiers A, B, and C.” | Stores concrete membership rather than declared scope |
| NC-08 | “If no universe is declared, use the platform default.” | Creates an ambient default |
| NC-09 | “Use the current workspace portfolio's universe.” | Makes UI selection authoritative and breaks explicit subject binding |
| NC-10 | “This universe is shared by portfolios P1 and P2.” | Violates exactly-one-Portfolio-Identity binding |
| NC-11 | “A portfolio must have exactly one universe.” | Invents the unresolved portfolio-level declaration cardinality |
| NC-12 | “The Asset Classification values are Equity, Bond, and Cash.” | Creates a WP3-owned enumeration and duplicates Asset Foundation |
| NC-13 | “Map provider asset type `EQ` to the canonical universe class.” | Introduces provider mapping and classification behavior |
| NC-14 | “Market means the broker execution venue.” | Reinterprets Asset Foundation market classification as execution semantics |
| NC-15 | “Capability means the capability successfully tested at runtime.” | Replaces cited descriptive authority with runtime evaluation |
| NC-16 | “Currency uses ISO 4217 codes.” | Invents an identifier-format rule not frozen by the cited authority |
| NC-17 | “If Currency is absent, use Portfolio Base Currency.” | Creates an implicit default and confuses two owners and meanings |
| NC-18 | “Convert all universe currencies to Portfolio Base Currency.” | Adds FX, accounting, and runtime behavior |
| NC-19 | “Allowed markets / allowed currencies / prohibited classes.” | Introduces Portfolio Policy or Decision Policy semantics |
| NC-20 | “Maximum allocation by classification is 25%.” | Introduces Portfolio Limits and allocation semantics |
| NC-21 | “Rank candidate assets by universe fit.” | Adds ranking and evaluation |
| NC-22 | “Infer missing criteria from current holdings.” | Adds evaluation, live state, and silent defaulting |
| NC-23 | “Enrich criteria from the latest provider taxonomy.” | Adds mutable provider dependency and copies authority |
| NC-24 | “The universe is valid only while all references resolve.” | Adds runtime/executable validation and temporal state |
| NC-25 | “Revision becomes effective at runtime after approval.” | Defines workflow, time, and runtime behavior beyond the semantic condition |
| NC-26 | “Persist the declaration as table `investment_universe`.” | Defines implementation and persistence |
| NC-27 | “Expose `POST /universes` and `GET /universes/{id}`.” | Defines an API |
| NC-28 | “Serialize category fields in Asset/Capability/Market/Currency order.” | Assumes Stage B/WP7 serialization and canonical-order authority |
| NC-29 | “WP7 may repair unresolved references before composing.” | Violates exact handoff and citation ownership |
| NC-30 | “Investment Universe Membership is deferred to a later WP3 stage.” | Reopens a confirmed rejection |

The negative corpus also excludes, whether named or implicit:

- evaluation, matching, membership, validation, compliance, eligibility,
  permission, refusal, and verdict semantics;
- policy, limits, constraints, allocation caps, and enforcement;
- optimization, ranking, recommendation, suitability, rebalancing, execution,
  order planning, and routing;
- performance, return, benchmark comparison, valuation, risk, exposure,
  concentration, attribution, and forecasting;
- provider, broker, exchange-adapter, transport, registry-resolution, cache,
  live-state, wall-clock, and model-output dependencies;
- database schemas, migrations, runtime services, endpoints, UI components,
  serialization formats, canonical bytes, and executable validators.

---

## 7. Stage B Handoff

### 7.1 Exact handoff

Following unconditional Independent Architecture Review approval and the
canonical Stage A closeout, M42-WP3 Stage B may be separately initiated to
draft an implementation-neutral Investment Universe Declaration Contract
using only the semantic surface admitted in §4.

Stage B receives:

1. exactly one governed noun: Investment Universe;
2. Portfolio Intelligence ownership of the declaration as a specialization of
   Portfolio Strategy Metadata;
3. binding of each declaration to exactly one cited Portfolio Identity and its
   corresponding cited Accounting Scope from WP2;
4. an explicit declared name;
5. inert scope criteria limited to the four closed categories Asset
   Classification, Capability, Market, and Currency;
6. exact-reference and non-owner discipline for every Asset Foundation-owned
   category and value;
7. the immutable-until-explicitly-revised semantic condition;
8. the distinction between Currency criteria and Ledger & Accounting-owned
   Portfolio Base Currency;
9. the complete rejection of Investment Universe Membership and every
   evaluation/matching/verdict equivalent;
10. the negative corpus in §6; and
11. the downstream requirement to hand the complete confirmed declaration to
    M42-WP7 without evaluation, enrichment, repair, reinterpretation, or
    ownership transfer.

### 7.2 Stage B drafting obligations

Stage B must:

- define the implementation-neutral subject binding;
- define the inert declaration shape;
- define the explicit-name coordinate;
- close the exact structural representation of the four and only four
  permitted criteria categories;
- make every criterion value an exact citation of Asset Foundation authority;
- define the semantic revision boundary without specifying a revision
  mechanism;
- preserve the unresolved portfolio-level declaration cardinality unless
  separately frozen authority resolves it;
- include a field-by-field five-part ownership gate;
- include documentation-only positive and negative golden vectors;
- prove that no field, operator, example, or vector can evaluate a specific
  instrument or produce a verdict; and
- state the exact WP7 handoff while leaving Portfolio Composition and
  portfolio-wide serialization to WP7.

### 7.3 Authority not handed to Stage B

Stage B receives no authority to define:

- implementation, database, persistence, runtime object, service, endpoint,
  API, provider integration, UI, or serialization;
- executable validation or a committed test runner;
- criterion evaluation, set/range matching operators, expression languages,
  filters, predicates, or membership results;
- policy, limits, transaction validation, refusal, execution eligibility, or
  enforcement;
- a concrete instrument list;
- Asset Foundation taxonomies, values, aliases, mappings, or identifier
  formats;
- Portfolio Base Currency ownership, defaulting, conversion, or mutation;
- a revision command, event, workflow, or runtime lifecycle;
- Portfolio Composition, its field order, schema version, canonical bytes, or
  serialization; or
- a zero/one/many Investment Universe declarations-per-portfolio rule.

Stage A closeout does not itself start Stage B. Stage B remains a separately
governed stage and receives only the bounded handoff recorded here.

---

## 8. Acceptance Criteria

This Stage A register is acceptable only if independent review confirms every
row below:

| Criterion | Evidence | Result |
|---|---|---|
| Investment Universe is the sole governed noun | §§1, 2.2, 2.3, 4.1, 7.1 | **PASS** |
| No new governed vocabulary is admitted | §§2.2–2.3 | **PASS** |
| Investment Universe retains its confirmed definition and Portfolio Intelligence ownership as a specialization of Portfolio Strategy Metadata | §§1, 2.2, 3.1 | **PASS** |
| Investment Universe Membership remains rejected and cannot be revived under a synonym | §§4.3–4.4, 5, 6 | **PASS** |
| Portfolio Identity and Accounting Scope are cited from WP2 and not redefined | §§2.1–2.2, 3.1, 4.1 | **PASS** |
| Each declaration binds to exactly one Portfolio Identity and its corresponding Accounting Scope | §§4.1–4.2 | **PASS** |
| Stage A does not invent a portfolio-level zero/one/many declarations cardinality | §§4.2, 6 `NC-11`, 7.2–7.3 | **PASS** |
| Asset Classification, Capability, Market, and Currency remain Asset Foundation-owned | §§2.2, 3.1, 4.1 | **PASS** |
| The four criterion categories are closed without defining values, operators, matching, or representation | §4.1 | **PASS** |
| Portfolio Base Currency remains Ledger & Accounting-owned and distinct from a Currency criterion | §§2.2, 3.1–3.2, 4.2, 6 | **PASS** |
| Citation, reference, carriage, and composition cause no ownership transfer | §3.3 and §7.1 | **PASS** |
| Every admitted semantic coordinate has an explicit owner and explicit non-owner boundary | §3 | **PASS** |
| The admitted and rejected semantic surfaces are complete and mutually distinct | §§4.1–4.4 | **PASS** |
| No evaluation, matching, membership, policy, limits, execution, validation, refusal, verdict, or enforcement semantics exist | §§1, 4.2–4.4, 5, 6 | **PASS** |
| No concrete instrument list or ambient default exists | §§4.2–4.3, 6 | **PASS** |
| Revision is a semantic condition only, with no mechanism | §§3.1, 4.1–4.2, 7 | **PASS** |
| The negative corpus covers all material semantic leakage risks | §6 | **PASS** |
| The Stage B handoff is exact, bounded, and leaves WP7 authority intact | §7 | **PASS** |
| No implementation, persistence, runtime, API, serialization, executable-validation, evaluation, or enforcement authority is created | Header, §§1, 6, 7.3 | **PASS** |
| No frozen upstream authority is modified or reinterpreted | §§2.1, 2.3, 3.3 | **PASS** |

### Final determination

The confirmed upstream vocabulary is sufficient for M42-WP3. Investment
Universe is the one and only governed noun required for the Investment
Universe Declaration Contract. Every supporting coordinate is cited at its
existing owner; every non-owner boundary is explicit; every evaluation,
matching, membership, policy, limits, execution, validation, refusal, verdict,
and enforcement surface is excluded.

No vocabulary admission, ownership transfer, implementation authority, or
operational authority is created.

**M42-WP3 STAGE A - COMPLETE AND CONFIRMED**
