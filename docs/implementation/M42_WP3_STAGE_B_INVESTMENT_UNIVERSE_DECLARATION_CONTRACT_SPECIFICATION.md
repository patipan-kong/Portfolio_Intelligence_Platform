# M42-WP3 Stage B — Investment Universe Declaration Contract Specification

**Stage:** M42-WP3 Stage B

**Date:** 2026-07-27

**Artifact type:** Documentation-only, implementation-neutral semantic contract

**Canonical governed noun:** **Investment Universe**

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

Normative terms such as **MUST**, **MUST NOT**, **REQUIRED**, and **MAY** govern
the meaning of this documentation-only contract. They do not authorize an
implementation, executable validator, runtime behavior, or enforcement
mechanism.

---

## 1. Executive Summary

This specification defines the canonical implementation-neutral contract for
one Investment Universe declaration. It closes only the semantic choices
authorized by the confirmed M42-WP3 Stage A surface.

An Investment Universe is a named, immutable-until-explicitly-revised,
portfolio-scoped declaration of intended holdings scope. Each declaration:

- binds to exactly one cited Portfolio Identity and that identity's
  corresponding cited Accounting Scope;
- has an explicit declared name;
- states scope through one or more distinct criteria categories selected only
  from Asset Classification, Capability, Market, and Currency;
- expresses each criterion as inert closed-set or closed-range declaration
  data made solely from exact Asset Foundation-owned references; and
- remains unchanged in meaning until an explicit revision boundary is
  declared.

Investment Universe is the sole governed noun. The subject coordinates remain
owned by Ledger & Accounting. The criterion categories and their values remain
owned by Asset Foundation. Portfolio Base Currency remains a separate Ledger
& Accounting coordinate and is never a Currency criterion, source, default,
or substitute.

The declaration produces no answer about an instrument. Investment Universe
Membership remains `REJECT`, including every renamed evaluation, matching,
eligibility, validation, refusal, or verdict equivalent. The contract defines
no implementation, persistence, runtime object, API, serialization,
executable validation, provider mapping, UI, policy, limits, execution,
enforcement, or portfolio-level declaration cardinality.

---

## 2. Contract Scope

### 2.1 Governing authority and precedence

This specification is subordinate to, and MUST be read consistently with:

1. frozen Platform Architecture and domain constitutions;
2. frozen M34 ownership decisions, especially `M34-D-0002`,
   `M34-D-0004`, and `M34-D-0007`;
3. the frozen [M42 Architecture Proposal](M42_ARCHITECTURE_PROPOSAL.md);
4. the confirmed
   [M42-WP1 Portfolio Canonical Vocabulary and Ownership Register](M42_WP1_PORTFOLIO_CANONICAL_VOCABULARY_AND_OWNERSHIP_REGISTER.md);
5. the confirmed
   [M42-WP2 Portfolio Identity, Accounting Scope, Membership and Base Currency Contract](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md);
6. the confirmed
   [M42-WP3 Architecture](M42_WP3_ARCHITECTURE_PROPOSAL.md);
7. the confirmed
   [M42-WP3 Stage A Vocabulary and Semantic Surface Register](M42_WP3_STAGE_A_VOCABULARY_AND_SEMANTIC_SURFACE_REGISTER.md);
   and
8. frozen Asset Foundation authority for Asset Classification, Capability,
   Market, Currency, and their values.

On conflict, the earlier or source-owning authority controls. This
specification cites that authority without amending, copying, or transferring
it.

### 2.2 Included surface

The complete Stage B surface is:

1. the implementation-neutral subject binding;
2. the implementation-neutral declaration structure;
3. the explicit declared-name coordinate;
4. the exact structural form of inert criteria over the four closed
   categories;
5. the immutable-until-explicitly-revised semantic boundary;
6. coordinate-by-coordinate ownership gates;
7. documentation-only positive and negative golden vectors; and
8. the exact handoff of the complete declaration to M42-WP7.

The words “subject binding,” “declared name,” “criteria,” “criterion
category,” “criterion extent,” “criterion reference,” “closed set,” “closed
range,” and “revision boundary” are ordinary contract language describing
facets of Investment Universe. They are not additional governed nouns,
independently owned objects, runtime types, or vocabulary admissions.

### 2.3 Excluded surface

This contract does not define or authorize:

- implementation, persistence, database schema, runtime objects, services,
  APIs, serialization, field order, canonical bytes, schema versions, UI, or
  provider mapping;
- executable validation, conformance code, a test runner, resolution, lookup,
  repair, enrichment, caching, or transport;
- an instrument list, instrument input, instrument-to-universe evaluation,
  matching, predicates, operators, selection, filtering, membership,
  eligibility, validation, compliance, refusal, or any verdict;
- Portfolio Policy, Decision Policy, Portfolio Limits, Sector Limits,
  optimizer constraints, allocation rules, transaction rules, execution, or
  enforcement;
- derived measures, valuation, performance, return, risk, exposure,
  concentration, attribution, recommendation, ranking, or forecasting;
- Asset Foundation taxonomies, values, aliases, mappings, identifier formats,
  ordering semantics, or range semantics;
- Portfolio Base Currency ownership, mutation, defaulting, conversion, or use
  as an Investment Universe criterion;
- revision commands, events, workflows, permissions, effective-time rules,
  storage history, or mutation behavior;
- Portfolio Composition or portfolio-wide serialization; or
- whether one Portfolio Identity has zero, one, or multiple Investment
  Universe declarations.

The last exclusion is absolute under this authority. The rule that each
declaration has exactly one subject does not imply a declaration count for
that subject.

---

## 3. Subject Binding Contract

### 3.1 Binding structure

Each Investment Universe declaration MUST contain one explicit subject
binding with exactly these two semantic coordinates:

| Coordinate | Contract |
|---|---|
| Portfolio Identity citation | Exactly one citation of the Ledger & Accounting-owned Portfolio Identity to which the declaration belongs |
| Accounting Scope citation | Exactly one citation of the corresponding Ledger & Accounting-owned Accounting Scope established for that same Portfolio Identity |

“Exactly one” applies to the coordinates within one declaration. It does not
state how many declarations a portfolio may have.

### 3.2 Binding invariants

The subject binding:

1. MUST cite the Portfolio Identity and Accounting Scope at their
   WP2-confirmed meanings;
2. MUST preserve the WP2 correspondence between the cited Portfolio Identity
   and cited Accounting Scope;
3. MUST be explicit and MUST NOT depend on current UI selection, workspace,
   user session, provider account, storage location, ambient context,
   inheritance, or default;
4. MUST NOT bind one declaration to multiple Portfolio Identities or multiple
   Accounting Scopes;
5. MUST NOT create, merge, divide, rename, or reinterpret either cited
   coordinate;
6. MUST NOT make intended holdings scope an accounting boundary;
7. MUST NOT make Portfolio Membership or any concrete holding a declaration
   input; and
8. MUST NOT be transferred from one portfolio to another by relabeling the
   declaration.

The subject binding is constitutive of the declaration. A declaration stated
for a different Portfolio Identity or Accounting Scope is a declaration for a
different subject; this contract does not define a move, copy, sharing, or
cross-portfolio mechanism.

### 3.3 Citation-without-transfer

Ledger & Accounting owns both cited subject coordinates and their
correspondence. Portfolio Intelligence owns only the fact that its Investment
Universe declaration is bound to those citations. Citation, carriage, and
later composition do not create a copied identity, alternate accounting
scope, or shared ownership.

---

## 4. Declaration Contract

### 4.1 Complete semantic structure

One Investment Universe declaration consists of exactly these semantic
facets:

| Facet | Presence | Meaning |
|---|---:|---|
| Subject binding | Required, one | The two-coordinate binding defined in §3 |
| Declared name | Required, one | The explicit name asserted for this declaration |
| Scope criteria | Required, one declaration facet | One or more distinct criterion-category coordinates under §5 |
| Revision boundary | Required semantic condition | The declaration's meaning is immutable until explicitly revised |

This table is an implementation-neutral semantic structure. “Presence” does
not prescribe fields, keys, nesting, storage, encoding, or runtime types.
No additional facet is admitted by this contract.

### 4.2 Declared name

The declared name:

1. MUST be explicitly supplied as part of the declaration;
2. MUST carry the exact human-declared naming meaning asserted for that
   declaration;
3. MUST NOT be inferred from criteria, Portfolio Identity, Accounting Scope,
   Portfolio Base Currency, a provider, a UI label, or another declaration;
4. MUST NOT be treated as an Asset Foundation classification or a canonical
   universe-name catalogue;
5. MUST NOT create a provider alias, standardized enumeration, or independent
   declaration identifier; and
6. MUST NOT determine, imply, or evaluate scope by itself.

Examples such as “Thai Equity” and “Retirement” are illustrative names only.
This contract defines no lexical encoding, length limit, normalization,
uniqueness rule, localization rule, or serialization for declared names.

### 4.3 Revision boundary

The subject binding, declared name, and criteria together constitute the
declaration's meaning. That meaning MUST NOT change silently.

An alteration to any meaning-bearing facet is an explicit revision boundary;
it MUST NOT be represented as the unchanged declaration meaning. Prior
meaning MUST NOT be retrospectively reinterpreted by later vocabulary,
provider data, UI state, holdings, clocks, models, or later composition.

This is a semantic immutability condition only. It defines no revision
identifier, version number, command, event, actor, permission, workflow,
effective time, persistence history, replacement rule, or runtime mutation
mechanism.

### 4.4 Declaration invariants

An Investment Universe:

- states intended holdings scope and no other output;
- is descriptive Portfolio Strategy Metadata, not accounting truth, judgment,
  policy, a limit, or enforcement;
- contains no concrete instrument list or Portfolio Membership fact;
- has no ambient, inherited, inferred, repaired, or provider-supplied default;
- has no live provider, wall-clock, current-holdings, model-output, or
  cross-portfolio dependency; and
- does not answer whether any specific instrument belongs, matches, qualifies,
  is eligible, is valid, is allowed, or may be transacted.

Investment Universe Membership remains `REJECT`. It is not deferred and
cannot be restored through a synonym, helper facet, vector, handoff, or later
WP3 interpretation.

---

## 5. Criteria Contract

### 5.1 Closed category structure

The scope-criteria facet MUST contain one or more and no more than four
distinct criterion-category coordinates. Each present category MUST be
exactly one of:

1. Asset Classification;
2. Capability;
3. Market; or
4. Currency.

A category may occur at most once within one declaration. A declaration may
use one category or multiple distinct categories. No fifth category,
extension category, generic “other” category, provider category, or
privately-defined category is admitted.

These rules govern criteria inside one declaration. They do not determine
the number of Investment Universe declarations associated with a portfolio.

### 5.2 Criterion structure

Each present criterion-category coordinate has exactly two semantic parts:

| Part | Contract |
|---|---|
| Category citation | The exact Asset Foundation-owned category named in §5.1 |
| Declared extent | Exactly one inert closed set or one inert closed range composed only of exact references belonging to that same Asset Foundation-owned category |

A closed set contains one or more distinct exact Asset Foundation references.
It states the declared values collectively and carries no ordering, priority,
weight, score, negation, wildcard, fallback, or operator.

A closed range states a bounded descriptive span solely through the exact
Asset Foundation references needed by the source authority's own range
meaning. WP3 does not create ordering, comparison, adjacency, inclusivity,
units, interpolation, or range semantics. A range is available here only
where the cited Asset Foundation authority already supplies all semantics
necessary to understand that range without a WP3-owned rule. Otherwise the
criterion MUST use a closed set of exact references or remain unstated.

The phrases “closed set” and “closed range” describe inert declared extent.
They do not authorize membership tests, set algebra, comparisons, interval
evaluation, queries, selectors, or predicates.

### 5.3 Exact-reference contract

Every criterion reference:

1. MUST cite an existing Asset Foundation-owned value at its authoritative
   meaning;
2. MUST belong to the category coordinate in which it appears;
3. MUST remain a reference, not a WP3-owned copy or redefinition;
4. MUST NOT be replaced by a provider code, broker label, UI label, cached
   value, local alias, private taxonomy, inferred value, or invented
   identifier;
5. MUST NOT be repaired, enriched, normalized, mapped, reclassified, or
   defaulted by WP3 or WP7;
6. MUST NOT carry a weight, threshold, ranking, preference, permission,
   prohibition, limit, action, or expected result; and
7. MUST NOT consume or identify a specific instrument.

This contract deliberately defines no identifier syntax. Exactness means
semantic identity with the source-owned reference, not a WP3-defined string,
code, URI, key, or byte representation.

### 5.4 Category meanings and non-collisions

| Category | Permitted declarative meaning | Mandatory non-collision |
|---|---|---|
| Asset Classification | Intended scope stated through cited Asset Foundation classification values | Does not classify an instrument, create a taxonomy, or mean an allowed/prohibited class |
| Capability | Intended scope stated through cited Asset Foundation capability values | Does not probe capability, require a runtime result, or determine eligibility |
| Market | Intended scope stated through cited Asset Foundation market-classification values | Does not mean broker venue, execution route, market access, or allowed market |
| Currency | Intended scope stated through cited Asset Foundation currency-of-denomination values | Does not mean Portfolio Base Currency, FX, conversion, reporting currency, or allowed currency |

Portfolio Base Currency is never part of the criteria facet. It MUST NOT fill,
default, constrain, convert, or reinterpret a Currency criterion. If cited
adjacently to distinguish the two concepts, it remains solely Ledger &
Accounting-owned and adds no Investment Universe meaning.

### 5.5 No composition logic

The presence of multiple criterion categories states multiple facets of the
same intended scope. This contract defines no `AND`, `OR`, `NOT`, precedence,
grouping, intersection, union, exclusion, comparison, satisfaction, or
short-circuit meaning between or within categories.

Consequently, the declaration is complete as descriptive data but is not
capable of being applied to an instrument. Any rule that turns one or more
criteria into a truth-valued or action-guiding result is not part of
Investment Universe and is not authorized by M42-WP3.

---

## 6. Ownership Gate

### 6.1 Five-part gate

Each semantic facet passes the frozen five-part ownership-boundary gate
independently:

| Semantic facet | Permitted subject | Permitted inputs | Output meaning | Prohibited inputs absent | Prohibited semantics absent | Result |
|---|---|---|---|---|---|---|
| Investment Universe declaration | One portfolio-scoped intended-holdings declaration | Subject binding, declared name, inert criteria | Named descriptive strategy declaration | No live, ambient, provider, model, holdings, or cross-portfolio input | No judgment, measure, membership, policy, or enforcement | `PASS` |
| Portfolio Identity citation | The one portfolio to which the declaration belongs | Exact WP2-confirmed citation only | Subject coordinate cited without redefinition | No UI selection, provider account, storage key, or inferred identity | No identity creation, merge, transfer, or strategy meaning | `PASS` |
| Accounting Scope citation | The corresponding accounting boundary | Exact WP2-confirmed citation only | Boundary coordinate cited without redefinition | No alternate, derived, shared, or inferred scope | No accounting mutation or intended-scope substitution | `PASS` |
| Declared name | The same Investment Universe declaration | Explicit human-declared name | Descriptive name only | No provider label, inferred name, catalogue, or ambient default | No classification, identity, evaluation, or policy meaning | `PASS` |
| Asset Classification criterion | The declaration's intended scope | Exact Asset Foundation category and value references | Inert classification extent | No provider mapping, private taxonomy, instrument, or live classification | No reclassification, matching, permission, or verdict | `PASS` |
| Capability criterion | The declaration's intended scope | Exact Asset Foundation category and value references | Inert capability extent | No probe, runtime result, provider answer, or instrument | No capability testing, matching, eligibility, or verdict | `PASS` |
| Market criterion | The declaration's intended scope | Exact Asset Foundation category and value references | Inert market-classification extent | No broker, venue adapter, provider map, market observation, or instrument | No routing, access, matching, policy, or execution | `PASS` |
| Currency criterion | The declaration's intended scope | Exact Asset Foundation currency-of-denomination references | Inert currency extent | No Portfolio Base Currency, FX, provider code, live rate, or instrument | No conversion, matching, permission, policy, or verdict | `PASS` |
| Revision boundary | The declaration's fixed semantic meaning | Explicit recognition that meaning changed | No-silent-reinterpretation condition | No clock, workflow, actor, command, event, or storage input | No lifecycle, mutation, authorization, or runtime behavior | `PASS` |
| WP7 handoff | The complete confirmed declaration | Exact declaration facets defined here | Citation and carriage of one coordinate | No repair, enrichment, default, provider, or ambient input | No evaluation, reinterpretation, serialization, or ownership transfer | `PASS` |

### 6.2 Ownership determination

The gate confirms:

- Portfolio Intelligence solely owns Investment Universe and its declarative
  strategy meaning.
- Ledger & Accounting solely owns Portfolio Identity, Accounting Scope,
  their correspondence, Portfolio Membership, and Portfolio Base Currency.
- Asset Foundation solely owns Asset Classification, Capability, Market,
  Currency, their values, and any source-defined taxonomy or relation needed
  to understand them.
- Portfolio Intelligence owns the choice to cite criteria but does not own
  any cited category or value.
- WP7 may later own Portfolio Composition while acquiring no ownership of the
  coordinates it carries.
- No owner is assigned under M42 to Investment Universe Membership because
  the concept remains `REJECT`.

For every cited coordinate, the source authority owns its meaning.
Investment Universe owns only its exact citation. Citation, reference,
carriage, revision, and composition do not transfer, share, or dilute
ownership.

---

## 7. Positive Golden Vectors

These vectors are normative documentation examples, not serialized records,
executable tests, validation responses, or instrument evaluations. Abstract
labels such as `PI-TH-01` and `AF-CURRENCY-THB` stand for exact citations
whose real identifier form remains owned elsewhere.

| ID | Documentary declaration | Why it conforms |
|---|---|---|
| PGV-01 | Subject: Portfolio Identity `PI-TH-01`; corresponding Accounting Scope `AS-TH-01`. Name: “Thai Equity”. Criteria: Asset Classification closed set containing exact reference `AF-CLASS-EQUITY`. | Explicit one-subject binding, explicit name, and one admitted inert category |
| PGV-02 | Subject: `PI-RET-01` / corresponding `AS-RET-01`. Name: “Retirement”. Criteria: Asset Classification closed set `{AF-CLASS-EQUITY, AF-CLASS-FIXED-INCOME}`; Capability closed set `{AF-CAP-INCOME}`. | Multiple distinct categories and multiple exact references remain inert descriptive data |
| PGV-03 | Subject: `PI-GLOBAL-01` / corresponding `AS-GLOBAL-01`. Name: “Global Multi-Market”. Criteria: Market closed set `{AF-MARKET-TH, AF-MARKET-US}`; Currency closed set `{AF-CURRENCY-THB, AF-CURRENCY-USD}`. | Market and asset denomination are cited without venue, FX, base-currency, policy, or matching meaning |
| PGV-04 | Subject: `PI-SCOPE-01` / corresponding `AS-SCOPE-01`. Name: “Foundation Range Example”. Criteria: one Asset Classification closed range expressed entirely by exact references and range meaning already owned by Asset Foundation. | A range is declarative only because all of its meaning is supplied by source authority; WP3 adds no ordering or comparison |
| PGV-05 | A later explicit revision changes the declared name or criterion extent and identifies that the meaning boundary changed; the earlier declaration meaning is not reinterpreted. | Preserves immutable-until-explicitly-revised semantics without specifying a revision mechanism |
| PGV-06 | WP7 cites and carries the complete PGV-03 declaration, preserving its subject, name, criteria, revision meaning, and all source ownership unchanged. | Exact downstream carriage with no evaluation, enrichment, repair, reinterpretation, or serialization rule |
| PGV-07 | A Portfolio Base Currency citation appears in an adjacent WP7-owned composition coordinate, while the Investment Universe Currency criterion remains the exact set declared in PGV-03. | Demonstrates ownership separation: adjacency does not default, copy, or alter the Currency criterion |

None of these vectors asks about, consumes, or produces a result for a
specific instrument. They make no assertion about the number of Investment
Universe declarations a Portfolio Identity may have. Only future explicit
frozen authority may decide portfolio-level declaration cardinality.

---

## 8. Negative Golden Vectors

These vectors are prohibited documentary shapes. Their classification
expresses contract analysis only; it does not define executable validation,
runtime rejection, transaction refusal, or enforcement behavior.

| ID | Prohibited specimen | Contract breach |
|---|---|---|
| NGV-01 | “Use the currently selected portfolio.” | Ambient subject; Portfolio Identity is not explicit |
| NGV-02 | One declaration cites `PI-A` and `PI-B`. | Cross-portfolio subject; one declaration may bind to exactly one Portfolio Identity |
| NGV-03 | Portfolio Identity `PI-A` is paired with an Accounting Scope that is not its WP2-corresponding scope. | Breaks the cited Ledger & Accounting correspondence |
| NGV-04 | “Every portfolio must have exactly one Investment Universe.” | Invents the unresolved portfolio-level declaration cardinality |
| NGV-05 | Name omitted or inferred from the first classification. | Violates the explicit-name coordinate and creates inference |
| NGV-06 | Criteria contain concrete instrument identifiers `ABC` and `XYZ`. | Replaces intended scope with a membership list |
| NGV-07 | Category `Sector`, `Theme`, `Region`, `ProviderAssetType`, or `Other`. | Adds a fifth/private category outside the closed surface |
| NGV-08 | Asset Classification value is provider code `EQ`, mapped locally to “Equity.” | Adds provider mapping and a competing reference |
| NGV-09 | Currency uses a WP3-invented ISO-code format. | Invents an identifier format owned nowhere by WP3 |
| NGV-10 | Missing Currency criteria default to Portfolio Base Currency. | Confuses Asset Foundation denomination with Ledger & Accounting reporting currency and creates a default |
| NGV-11 | “Convert declared currencies to Portfolio Base Currency using the latest FX rate.” | Adds conversion, market data, clock, runtime, and accounting behavior |
| NGV-12 | `classification IN {Equity, Bond}` or `market == TH`. | Converts inert extent into executable matching operators |
| NGV-13 | Criteria use `AND`, `OR`, `NOT`, precedence, or nested expression groups. | Creates composition logic and a predicate language |
| NGV-14 | “Instrument X satisfies the universe.” | Produces an instrument-specific matching verdict |
| NGV-15 | `belongs(instrument, universe) -> boolean`. | Reintroduces rejected Investment Universe Membership |
| NGV-16 | “Instrument X is eligible / ineligible.” | Reintroduces an evaluation-equivalent verdict |
| NGV-17 | “Reject an order for an instrument outside the universe.” | Adds transaction refusal and enforcement |
| NGV-18 | “Only these markets, currencies, or classes are allowed.” | Converts descriptive scope into policy |
| NGV-19 | “Maximum allocation to this classification is 25%.” | Adds Portfolio Limits and allocation semantics |
| NGV-20 | Capability value is included only after a runtime capability probe succeeds. | Replaces cited descriptive authority with live evaluation |
| NGV-21 | Missing criteria are inferred from current holdings or a provider taxonomy. | Adds live inputs, repair, enrichment, and silent defaulting |
| NGV-22 | A closed range supplies WP3-defined ordering, comparison, inclusive edges, units, or interpolation. | Creates range semantics not owned by WP3 and enables matching |
| NGV-23 | A later taxonomy update silently changes what an earlier declaration meant. | Violates immutable-until-explicitly-revised meaning |
| NGV-24 | “Revision is effective after approval at 09:00,” with a command or event shape. | Adds workflow, time, lifecycle, runtime, or persistence semantics |
| NGV-25 | WP7 resolves, repairs, enriches, normalizes, or reclassifies a criterion reference. | Violates exact handoff and source ownership |
| NGV-26 | WP7 serializes category fields in an order prescribed by this contract. | Assumes WP7 serialization authority that Stage B does not possess |
| NGV-27 | Portfolio Membership is used as proof that an instrument is inside an Investment Universe. | Collapses a Ledger fact into rejected universe evaluation |
| NGV-28 | “Universe match,” “scope filter,” “compatibility check,” “candidate selection,” or another renamed helper returns a result for an instrument. | Terminology attempts to evade the complete rejection of evaluation-equivalent concepts |

No negative vector authorizes the behavior it illustrates. In particular,
“prohibited” is a documentary boundary term, not an operational refusal or
enforcement result.

---

## 9. Stage-WP7 Handoff

### 9.1 Exact handoff coordinate

After this Stage B contract is independently confirmed, M42-WP7 receives one
complete Investment Universe declaration coordinate consisting of:

1. the exact Portfolio Identity citation;
2. the exact corresponding Accounting Scope citation;
3. the explicit declared name;
4. every present criterion-category coordinate;
5. each criterion's set-or-range extent and exact Asset Foundation
   references; and
6. the immutable-until-explicitly-revised semantic condition.

Completeness means no facet defined by §§3–5 is omitted, inferred, replaced,
or supplemented in handoff. It does not prescribe a serialized envelope,
field order, schema, identifier, bytes, transport, or runtime object.

### 9.2 WP7 permissions

M42-WP7 MAY:

- cite and carry the complete declaration as a Portfolio
  Intelligence-owned coordinate;
- compose it alongside other independently owned coordinates at their
  confirmed meanings; and
- define Portfolio Composition and portfolio-wide serialization only under
  WP7's own separately confirmed authority.

### 9.3 WP7 prohibitions

This handoff grants WP7 no authority to:

- evaluate a specific instrument against the declaration;
- create Investment Universe Membership or an equivalent result;
- match, filter, select, validate, qualify, rank, permit, reject, or enforce;
- omit, repair, enrich, normalize, map, default, infer, reclassify, or
  reinterpret a declaration facet or cited reference;
- turn descriptive criteria into Portfolio Policy, Decision Policy,
  Portfolio Limits, transaction rules, or execution eligibility;
- treat Currency criteria as Portfolio Base Currency or vice versa;
- transfer or share ownership through composition;
- derive a portfolio-level zero/one/many declaration rule from the handoff;
  or
- attribute WP7's composition, serialization, schema, ordering, or canonical
  bytes to this WP3 contract.

The handoff is therefore:

> exact citation and carriage of the complete confirmed Investment Universe
> declaration, with meaning and ownership preserved and with no evaluation,
> enrichment, repair, reinterpretation, or authority transfer.

---

## 10. Acceptance Criteria

This specification is acceptable only if Independent Review confirms all of
the following:

1. Investment Universe is the sole governed noun and remains owned by
   Portfolio Intelligence as a specialization of Portfolio Strategy
   Metadata.
2. Every declaration binds explicitly to exactly one Portfolio Identity and
   its corresponding Accounting Scope, both cited from Ledger & Accounting
   without redefinition or ownership transfer.
3. The one-subject-per-declaration rule is not misread as a zero/one/many
   declarations-per-portfolio rule; portfolio-level declaration cardinality
   remains wholly unresolved.
4. The complete declaration structure contains only subject binding,
   explicit declared name, inert scope criteria, and the semantic revision
   boundary.
5. Criteria contain one or more distinct categories selected only from Asset
   Classification, Capability, Market, and Currency, with no fifth,
   provider-owned, or private category.
6. Each criterion uses only an inert closed set or source-authorized closed
   range of exact Asset Foundation references and adds no WP3-owned taxonomy,
   value, alias, mapping, identifier format, ordering, comparison, or range
   semantics.
7. No category combination, set, range, example, or handoff defines an
   operator, expression, predicate, query, match, or instrument-specific
   result.
8. Asset Classification, Capability, Market, Currency, and their values
   remain solely Asset Foundation-owned; Portfolio Intelligence owns only
   their citation in its declaration.
9. Portfolio Base Currency remains solely Ledger & Accounting-owned and is
   never a criterion, default, conversion input, or substitute for a Currency
   criterion.
10. Portfolio Membership remains a distinct Ledger & Accounting fact and is
    never treated as Investment Universe meaning or evidence.
11. Investment Universe Membership remains `REJECT` and no evaluation,
    matching, eligibility, validation, compatibility, selection, refusal,
    verdict, or renamed equivalent reintroduces it.
12. No Portfolio Policy, Decision Policy, Portfolio Limits, Sector Limits,
    allocation rule, transaction rule, optimizer constraint, execution
    eligibility, refusal, or enforcement semantics exist.
13. The immutable-until-explicitly-revised boundary prevents silent
    reinterpretation while defining no command, event, workflow, permission,
    effective time, persistence, history, or runtime mechanism.
14. The positive vectors demonstrate valid single-category, multi-category,
    revision-boundary, base-currency-separation, and exact-WP7-carriage
    shapes without evaluating an instrument.
15. The negative vectors cover ambient or cross-portfolio subjects, concrete
    instrument lists, private/provider vocabulary, identifier invention,
    base-currency confusion, evaluation equivalents, policy, limits,
    execution, enforcement, silent revision, and WP7 authority leakage.
16. The WP7 handoff transfers the complete declaration without omission,
    evaluation, enrichment, repair, reinterpretation, defaulting, or ownership
    transfer, while leaving Portfolio Composition and portfolio-wide
    serialization entirely to WP7.
17. Citation-without-transfer discipline is explicit for every Ledger &
    Accounting and Asset Foundation coordinate.
18. Implementation, persistence, runtime, API, serialization, provider, UI,
    executable-validation, evaluation, production, and enforcement authority
    remain `NONE`.
19. No repository artifact outside this Stage B specification is modified by
    creation of this contract.
