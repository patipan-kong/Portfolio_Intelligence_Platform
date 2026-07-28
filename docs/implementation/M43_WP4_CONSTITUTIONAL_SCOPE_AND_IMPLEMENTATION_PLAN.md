# M43-WP4 — Constitutional Scope and Implementation Plan

**Milestone:** M43 — Portfolio Analytics Contract Foundation  
**Work package:** M43-WP4 — Temporal, Currency, Calendar, Benchmark, and Arithmetic Semantics  
**Artifact class:** Constitutional scope, architecture, and implementation plan  
**Status:** `RC1 CORRECTED — REQUIRES INDEPENDENT CONFIRMATION`  
**Independent architectural review:** `APPROVED WITH REQUIRED CORRECTIONS — RC1 APPLIED`  
**M43 Architecture:** `COMPLETE AND FROZEN` — cited, never modified  
**M43-WP1:** `COMPLETE AND FROZEN` — cited, never modified  
**M43-WP2:** `COMPLETE AND FROZEN` — cited, never modified  
**M43-WP3:** `COMPLETE AND FROZEN` — cited, never modified  
**Runtime authority:** `NONE`  
**Source-code authority:** `NONE`  
**Persistence/API/UI authority:** `NONE`  
**Implementation authority:** `NONE`  
**Provider authority:** `NONE`  
**Production-method authority:** `NONE`  
**Executable-validation authority:** `NONE`

---

## 0. Executive determination

M43-WP4 is the numerical-convention closure work package reserved by the
frozen [M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md).
It does not redesign M43, WP1, WP2, or WP3. It consumes their exact frozen
contracts and specifies only the temporal, currency, calendar, benchmark,
missing-data, precision, rounding, partial-window, and dependency-arithmetic
semantics that they deliberately deferred.

WP4 shall produce a single normative semantics specification and a
documentary numerical fixture corpus. Together they must make every
output-affecting convention:

1. explicit;
2. singularly owned;
3. immutably bound to one exact Portfolio Method Version and its exact
   specification;
4. represented by exact source-owned evidence or an exact versioned
   calculation dependency;
5. reproducible without a clock, provider, database, cache, Workspace,
   Current Selection, process locale, or host configuration; and
6. unavailable for caller override.

WP4 must discharge the following two authority-class proof obligations
required by frozen M43 Architecture §§7, 9, 16, and 20. The rows are
propositions to prove, not predetermined conclusions:

| Concern | Authority-class proposition requiring constitutional proof | Ownership proposition to verify | Binding proposition to verify | Caller-override proposition to verify |
| --- | --- | --- | --- | --- |
| Risk-free input value or series | Prove why `GOVERNED_EVIDENCE` is constitutionally correct and why `VERSIONED_CALCULATION_DEPENDENCY` is rejected | Prove that the observed market fact retains Market Intelligence ownership | Prove that exact `MARKET_EVIDENCE` roles and matching WP3 entries are the only valid placement | Prove why caller override is rejected |
| Annualization basis | Prove why `VERSIONED_CALCULATION_DEPENDENCY` is constitutionally correct and why `GOVERNED_EVIDENCE` is rejected | Prove the exact constitutional owner without expanding Portfolio Intelligence authority; source calendar meaning remains Market Intelligence-owned | Prove that WP2/WP3 dependency placement is required, then apply the fail-closed representability gate below | Prove why caller override is rejected |

Even if the first proposition is proved, it does not allow WP4 to declare an instrument economically
“risk free,” originate a rate, select a provider, or create Market evidence.
A later non-production WP7 method specification must identify the exact
governed Market evidence it consumes and its deterministic transformation.
If the required evidence contract does not exist, the method remains blocked.

Even if the second proposition is proved, WP4 cannot invent the exact existing
governed contract kind required by frozen WP2 §8.1. No such contract kind is
identified by the present frozen corpus. This is a representability gap:
until a separately authorized governance instrument supplies an exact
constitutional owner, existing governed contract kind, immutable identifier,
version, and canonical value bytes, no annualization basis can be admitted as
a WP2 dependency or supplied by a WP3 `CALCULATION_DEPENDENCY` entry. Concrete
annualized methods remain blocked and WP4 fixtures remain explicitly
artificial and documentary. WP4 does not author or imply the missing
contract.

The annualization proposition does not authorize an unstated, ambient,
implicit, or hidden `252`, `365`, or library constant. Any calendar evidence
used by a future separately governed dependency remains owned by Market
Intelligence and must itself be exact and version-bound.

No concrete performance, risk, benchmark-relative, or attribution formula is
admitted here. WP6–WP8 remain the sole work packages authorized to propose
those non-production method specifications.

---

## 1. Controlling authority and precedence

WP4 is governed in this order:

1. the Platform Constitution and Architecture Laws;
2. frozen M34 ownership decisions;
3. frozen M39 Observation contracts;
4. frozen M40–M41 Market Measure contracts;
5. frozen M42 Portfolio contracts, especially Base Currency, Portfolio
   Benchmark Declaration, Portfolio Composition, and Provenance;
6. frozen M43 Architecture;
7. frozen M43-WP1 vocabulary and ownership dispositions;
8. frozen M43-WP2 Definition, Method Version, applicability, and calculation-
   dependency contracts;
9. frozen M43-WP3 Portfolio Measure Subject and Portfolio Analytics Input
   Manifest contracts; and
10. this WP4 plan, and later the independently confirmed WP4 normative
    specification.

On conflict, the earlier or source-owning authority controls. WP4 must fail
closed rather than repair an upstream omission or reinterpret a frozen term.

The M41 temporal/unit/arithmetic corpus may be used only as a mechanical and
validation-pattern precedent. Its Market Intelligence nouns, Method Version,
Measurement Window, Input Manifest, Result types, and ownership do not become
Portfolio Intelligence contracts and must not be copied by relabeling.

### 1.1 External governance dependency

The repository-local effectivity evidence required by frozen WP1 and WP2
governance remains outstanding:

1. the WP1 §9.2/§9.4 Glossary synchronization has not been applied;
2. no repository-local WP1 independent-confirmation artifact has been
   recorded;
3. no repository-local WP2 independent-confirmation artifact has been
   recorded; and
4. activation of the standing
   `M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6` item required
   by WP1 §7.4 has not been recorded.

Those actions remain governed by their own separately authorized workflows.
WP4 neither performs nor cures them, and no frozen artifact or
`docs/GLOSSARY.md` may be modified to do so. They are an external,
fail-closed governance dependency: they must be completed under their own
authority before WP4 confirmation is recorded.

WP4 confirmation does not release WP6. The WP1 §7.4 WP6 governance block
remains independently governed and in force until its own authorized
workflow records otherwise.

---

## 2. Exact constitutional allocation

### 2.1 In scope

Only the following concerns are allocated to WP4:

1. the complete Portfolio Measurement Window contract:
   - exact boundary coordinates;
   - start/end presence and cardinality;
   - inclusivity and exclusivity;
   - time basis;
   - timezone or fixed-offset treatment;
   - calendar reference where applicable;
   - identity, immutability, ordering, and canonical bytes;
2. economic-time versus record-time selection and alignment;
3. expression of every Portfolio-derived value in the exact Portfolio Base
   Currency applicable to the evidence period;
4. exact FX-evidence requirements and conversion placement within an
   analytics calculation;
5. exact calendar authority, identity, version, session, closure, holiday,
   early-close, leap-day, timezone, DST, and alignment rules;
6. exact alignment of the Portfolio series and the declared Benchmark series;
7. the risk-free-input authority class, evidence identity requirements,
   temporal alignment, transformation placement, and binding rules;
8. the annualization-basis authority class, dependency identity, version,
   exact value representation, and binding rules;
9. missing, duplicate, sparse, asynchronous, and gapped numerical-input
   treatment;
10. full-window and partial-window determination and the allowed generic
    handling modes;
11. exact decimal/rational representation, precision, scale, rounding mode,
    tie behavior, negative zero, exceptional values, operation order, and
    serialization;
12. arithmetic involving exact calculation-dependency values;
13. canonical serialization of every WP4-owned semantic record and ordinary
    rule value;
14. an explicit no-default matrix;
15. positive, negative, boundary, permutation, and cross-platform documentary
    numerical vectors; and
16. the exact handoff of deterministic semantic predicates to WP5–WP8.

### 2.2 Out of scope

WP4 must not specify, amend, or authorize:

- a new Portfolio subject, Composition, Identity, Accounting Scope,
  Membership, Base Currency, Benchmark Declaration, lifecycle state, or
  Provenance meaning;
- accounting arithmetic, NAV, ledger replay, cost basis, cash-flow treatment,
  or `compute_period_metrics()`;
- resolution of the open questions in
  [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md);
- a Portfolio Measure Definition, Portfolio Method Version identity,
  applicability operator, manifest category, manifest field, manifest-entry
  identity, dependency-declaration shape, or input role field;
- a concrete cumulative-return, annualized-return, rolling-return, drawdown,
  volatility, deviation, Sharpe, Sortino, beta, correlation, alpha, tracking-
  error, information-ratio, contribution, or attribution formula;
- a method-specific minimum-history threshold or policy choice; WP4 defines
  how such a choice must be owned and bound, while WP6–WP8 choose it in exact
  non-production method specifications;
- Portfolio Input Sufficiency values, Portfolio Computation Outcome values,
  reason codes, Degraded State mapping, value presence, result identity,
  result lineage, Provenance carriage in a result, or result serialization;
- benchmark construction, Composite weights, Category matching, provider
  mapping, observation retrieval, or replacement of Explicitly None;
- designation of a financial instrument or series as economically risk free;
- Market observations, FX rates, calendars, benchmark observations, currency
  identifiers, asset identifiers, unit semantics, or taxonomy;
- evidence acquisition, source preference, correction, enrichment,
  interpolation presented as source truth, or provider access;
- a cross-portfolio calculation, Wealth result, recommendation, optimization,
  evaluation, causal claim, ranking, forecast, or execution instruction;
- production-method admission, executable fixtures, a test runner, a
  conformance harness, source code, registry, kernel, adapter, API, UI,
  schema, migration, cache, persistence, scheduler, or deployment behavior;
  or
- modification of any frozen M1–M43-WP3 artifact.

### 2.3 The essential boundary

WP4 specifies deterministic calculation-side interpretation of exact,
already-bound evidence. It does not obtain evidence and it does not classify
the final result.

```text
Frozen WP2 Method Version and immutable specification
  - declared roles
  - declared dependencies
  - applicability requirements
                    |
                    v
Frozen WP3 Subject and complete exact Manifest
  - source-owned canonical values
  - exact dependency values
                    |
                    v
WP4 deterministic semantic interpretation
  - window and time selection
  - currency/FX placement
  - calendar and series alignment
  - missing/partial handling
  - exact arithmetic and serialization
                    |
                    v
WP5 result/sufficiency/outcome/degradation contract
                    |
                    v
WP6-WP8 exact non-production method specifications
```

The diagram expresses dependency order, not runtime components.

---

## 3. Vocabulary gate

Portfolio Measurement Window is already admitted and Portfolio Intelligence-
owned by frozen M43-WP1 `PA-V06`. WP4 must define it at the exact meaning
frozen there: the explicit Portfolio-calculation input-selection boundary
over which a Portfolio Measure is derived.

WP4 must not:

- reuse M41 Market Intelligence `Measurement Window` as the Portfolio type;
- replace the M34-D-0005 Canonical Temporal Claim;
- add a second Portfolio window noun;
- turn a field, enum token, binding key, rule mode, basis form, dependency
  contract tag, or fixture label into business vocabulary; or
- reopen any WP1 disposition.

Before the normative specification relies on any genuinely new governed noun,
WP4 must run the frozen downstream five-part gate:

1. distinct meaning;
2. exact boundary;
3. subject;
4. exactly one owner; and
5. dependency relation.

The disposition must be `ADMIT`, `REUSE`, `RENAME`, or `REJECT`, independently
reviewed and confirmed. Any confirmed admission or rename must be synchronized
to `docs/GLOSSARY.md` in the same change. The expected plan outcome is **no
new constitutional noun**: annualization-basis forms, time bases, alignment
modes, rounding modes, and dependency tags should remain ordinary closed
contract syntax beneath the already admitted Portfolio Method Version,
Portfolio Analytics Input Manifest, and Portfolio Measurement Window.

---

## 4. Ownership and non-owner boundaries

| Concern | Sole owner | WP4 authority | WP4 prohibition |
| --- | --- | --- | --- |
| Portfolio Measurement Window and Portfolio calculation semantics | Portfolio Intelligence | Define exact immutable semantics and bytes | No Market Measurement Window reuse or runtime admission |
| Portfolio Identity, Accounting Scope, Membership, Base Currency, ledger facts | Ledger & Accounting | Cite exact coordinates and consume exact evidence | No inference, mutation, accounting recomputation, or currency taxonomy |
| Portfolio Composition and Portfolio Benchmark Declaration | Portfolio Intelligence under frozen M42 | Cite and interpret only under WP4 analytics authority | No altered declaration, default benchmark, benchmark construction, or new Composition identity |
| FX, calendars, benchmark observations, market reference measures, observed risk-free values | Market Intelligence | Require and consume exact governed evidence | No origination, fetching, correction, provider mapping, or Market ownership |
| Asset identity, currency dimension, Unit Semantics, classification, taxonomy | Asset Foundation | Cite exact governed references | No local currency code list, alias, unit, or classification |
| Portfolio Method Version and calculation semantics | Portfolio Intelligence under frozen M43-WP2 | Define WP4 semantic grammar consumed by immutable specifications | No new Method Version field or default/preferred method |
| Portfolio Analytics Input Manifest | Portfolio Intelligence under frozen M43-WP3 | Consume exact roles, entries, identities, values, and canonical bytes | No new category, entry shape, optional role, retrieval, or repair |
| Provenance meaning and capture | Connectivity & Ingestion | Preserve source association; hand off unchanged | No recapture or reconstruction |
| Result, sufficiency, outcome, reason, state, result lineage | Portfolio Intelligence under frozen WP1 and future WP5; producing domain for Degraded State | Hand off exact semantic predicates only | No early result envelope or classification |
| Rendering | Experience Platform | None | Experience computes nothing |
| Recommendations and optimization | Decision Intelligence | None | No action or judgment meaning |
| Evaluation | Trust & Evaluation | None | No correctness, quality, causal, or reliability verdict |
| Cross-portfolio meaning | Wealth Intelligence | None | Exactly one Portfolio only |

Citation, embedding, canonical framing, arithmetic use, and transport custody do
not transfer ownership.

---

## 5. Contract-placement architecture

WP4 must fit entirely into the frozen WP2/WP3 placement model.

### 5.1 Immutable method specification

The immutable non-production specification referenced by a Portfolio Method
Version is the home for:

- the exact WP4 semantic choices used by that method;
- every stable WP3 input-role declaration required to supply those choices;
- exact generic handling modes selected from the WP4 contract;
- method-specific fixed literals and thresholds;
- operation order and output numeric form;
- identification of every exact governed dependency; and
- the prohibition of every alternative or fallback.

WP4 adds no Method Version field. Changing any output-affecting WP4 semantic
choice changes the immutable specification and therefore requires a new
Portfolio Method Version under frozen WP2 compatibility rules.

### 5.2 WP2 calculation-dependency declaration

Frozen WP2 permits a calculation dependency only when the dependency already
has both:

1. an exact constitutional owner; and
2. an exact existing governed contract kind.

Only such a dependency may appear in the WP2 declaration and closure, with
its exact identifier and immutable version. Directly consumed governed
Portfolio-measure results may qualify when their controlling contract
supplies all of those coordinates.

External facilities such as calendar engines, timezone databases, and
external currency-path, normalization, interpolation, or other algorithm
implementations do not become WP2 dependencies merely because they affect an
output. When a facility lacks either an exact constitutional owner or an
exact existing governed contract kind, it cannot be declared as a WP2
dependency. If a method requires it and its behavior cannot be completely
fixed as immutable specification semantics using already governed inputs,
the method remains blocked until a separately authorized governance
instrument supplies both prerequisites.

No “latest,” compatible range, unversioned library, system facility,
transitive-only reference, artificial contract kind, or WP4-authored
dependency kind is permitted.

### 5.3 WP3 manifest roles and entries

Every concrete invocation supplies:

- exact Ledger evidence as `LEDGER_DERIVED_EVIDENCE`;
- exact FX, calendar, and benchmark observations or Market Measure Results as
  `MARKET_EVIDENCE`, plus risk-free observations/results in that category
  only if the §6.6 constitutional proof succeeds;
- exact currency/unit references as `ASSET_FOUNDATION_REFERENCE`;
- only genuinely caller-selectable values as `INVOCATION_PARAMETER`; and
- exact values for annualization or another calculation dependency as
  `CALCULATION_DEPENDENCY` only after frozen WP2 representability is proved,
  including an exact pre-existing owner and governed contract kind.

WP4 must not add a manifest field, category, sidecar, policy record, hidden
context, or post-manifest lookup. A value absent from the exact manifest is
absent from the calculation.

### 5.4 WP5 handoff

WP4 emits deterministic documentary semantic facts and predicates, not
result classifications. Those predicates are not reason codes, Portfolio
Computation Outcomes, or Degraded States. The normative specification must
make the following determinate:

- window validity;
- temporal selection/alignment success;
- currency compatibility/conversion-path closure;
- calendar resolution;
- benchmark alignability;
- risk-free evidence closure;
- annualization authority proof and representability status;
- density/gap/full-window/partial-window status; and
- arithmetic success or named arithmetic failure condition.

WP5 retains exclusive authority to map those facts to Portfolio Input
Sufficiency, Portfolio Computation Outcome, Degraded State, reason codes,
value presence, and result serialization. WP4 must not name, encode, or
pre-assign that mapping.

### 5.5 WP6-WP8 handoff

WP4 defines the closed grammar and deterministic mechanics. WP6–WP8 choose
exact values within that grammar for each non-production method:

- exact required history and threshold;
- allowed or prohibited partial-window mode;
- exact calendar and alignment mode;
- exact annualization dependency only after the §6.7 external
  representability gap is separately closed;
- exact risk-free evidence role where used, only after the §6.6 proof;
- exact benchmark alignment rule where used;
- exact arithmetic expression and operation order; and
- exact output scale and rounding.

WP4 therefore eliminates ambient choices without admitting a formula early.

### 5.6 Complete authority-and-binding matrix

Every WP4 concern must resolve through exactly one permitted placement:

| Concern | Authority class and owner | Required binding |
| --- | --- | --- |
| Concrete Portfolio Measurement Window | Portfolio Intelligence-owned explicit caller choice only where the exact method specification declares it invocation-bound | One exact `INVOCATION_PARAMETER` role and WP3 entry carrying complete WP4-canonical window bytes; absence never means “current” or a default |
| Window interpretation, boundary kinds, and alignment mode | Portfolio Intelligence immutable specification semantics | Exact semantic choices in the non-production specification bound by the Portfolio Method Version |
| Portfolio Base Currency | Ledger & Accounting-owned declaration using an Asset Foundation-owned currency reference | Exact subject/Composition coordinate plus exact Ledger/Asset evidence roles where calculation requires their values |
| FX value | Market Intelligence-governed evidence | Exact `MARKET_EVIDENCE` role and manifest entry |
| FX path and conversion order | Portfolio Intelligence immutable specification semantics; an external path algorithm is dependency-eligible only if it already has an exact constitutional owner and exact governed contract kind | Exact specification rule; WP2 declaration plus WP3 dependency entry only after frozen WP2 representability is proved, otherwise the method is blocked |
| Calendar content | Market Intelligence-governed evidence | Exact `MARKET_EVIDENCE` role and entry under a frozen representable contract |
| Calendar/timezone algorithm or database | Not a WP2 dependency unless an exact constitutional owner and exact existing governed contract kind are already supplied outside WP4 | Use an entirely specified calendar-free/fixed-offset rule with governed evidence, or remain blocked pending separate governance; WP4 cannot promote a facility into a dependency |
| Portfolio Benchmark Declaration | Portfolio Intelligence under frozen M42 | Exact declaration already carried by the subject/Composition; never an invocation parameter |
| Benchmark observations/results | Market Intelligence-governed evidence | Exact `MARKET_EVIDENCE` roles and entries matching the declaration |
| Risk-free value/series | Authority class is a proof obligation; the observed market fact retains Market Intelligence ownership | Use an exact `MARKET_EVIDENCE` role and entry only if §6.6 proves that placement and rejects dependency/caller placement |
| Annualization basis | Authority class is a proof obligation; if `VERSIONED_CALCULATION_DEPENDENCY` is proved correct, the present corpus still lacks the existing governed contract kind required by WP2 | Fail closed until separate authority supplies the missing representability; only then may an exact WP2 declaration/closure and WP3 entry be used |
| Method-specific density, history, or partial-window threshold | Portfolio Intelligence immutable specification literal; an externally computed value is dependency-eligible only with a pre-existing exact owner and governed contract kind | Exact finite canonical literal in the specification, or exact WP2/WP3 binding after representability proof; otherwise blocked and never caller supplied |
| Missing-data treatment, interpolation mode, precision, rounding, and operation order | Portfolio Intelligence immutable specification semantics | Exact retained WP4 mode and all required numeric coordinates in the bound specification |
| Direct Portfolio-measure dependency value | Exact constitutional owner already supplied by its governed contract | Exact existing governed contract kind, identifier, and version in WP2 declaration/closure and one matching WP3 `CALCULATION_DEPENDENCY` entry |

The concrete window is the only WP4-governed choice expected to be caller
selectable, and only when the bound immutable specification declares its
exact `INVOCATION_PARAMETER` role and canonical value domain. Selecting a
window does not select its timezone authority, calendar authority, alignment
mode, partial-window fallback, or any other governed semantic choice.

---

## 6. Required normative semantic components

The primary WP4 specification must contain all components below. None may be
left to “standard practice,” a library default, a provider, or a future
implementer.

### 6.1 Component A — Portfolio Measurement Window

The contract must close:

- one exact schema/version tag;
- required and optional coordinates with exact cardinality;
- start and end/cutoff semantics;
- permitted open/closed boundary combinations;
- instantaneous, elapsed-duration, civil-period, and session-bound forms, if
  retained;
- the exact meaning of absent start, if retained;
- timezone, fixed-offset, or timezone-free declaration;
- calendar reference or explicit calendar-free rule;
- alignment origin and interval membership;
- validation, canonical field order, identity, immutability, and rejection;
- no wall-clock-relative form such as “today,” “latest,” or “last N days”
  without an exact immutable cutoff; and
- no replacement of the Canonical Temporal Claim.

### 6.2 Component B — Economic time, record time, and stable ordering

For every evidence role, the immutable specification must state which
source-owned temporal coordinate controls:

- economic inclusion;
- record/replay cutoff;
- observation availability;
- reference period;
- interval overlap;
- multi-series alignment; and
- stable tie-breaking.

WP4 must preserve both economic and record time where ADR-003 or the owning
contract requires them. It must never rewrite one as the other. An absent,
ambiguous, approximate, incompatible, or insufficiently precise controlling
time fails its exact predicate.

### 6.3 Component C — Portfolio Base Currency and FX

The exact Portfolio Base Currency applicable to each historical fact remains
Ledger & Accounting-owned. Its currency reference remains Asset Foundation-
owned. WP4 must define:

- how a calculation proves that every numeric operand is already expressed in
  the applicable Base Currency or requires conversion;
- the exact Market-owned FX evidence roles;
- direction, numerator/denominator orientation, inversion permission,
  multiplication/division placement, and conversion time;
- whether a direct pair is mandatory or an explicitly declared cross-rate
  path is permitted;
- the exact ordering of conversion relative to alignment, aggregation,
  compounding, dependency use, and rounding;
- behavior across a recorded Base Currency change without retroactive
  reinterpretation; and
- fail-closed treatment of absent, stale, temporally misaligned, ambiguous,
  provider-shaped, or incompatible FX evidence.

WP4 analytics-side conversion must not be described as Ledger NAV or
accounting conversion and must not amend Portfolio Calculation Rules.

### 6.4 Component D — Calendar and observation alignment

The specification must require either:

1. an explicit calendar-free rule whose complete behavior is fixed; or
2. one exact Market Intelligence-owned calendar identity and version, with
   every required external facility independently representable under frozen
   WP2.

A calendar engine, timezone database, or external algorithm implementation
that lacks either an exact constitutional owner or an exact existing governed
contract kind cannot become a WP2 dependency. If the required behavior cannot
be fully specified without such a facility, the affected method remains
blocked until separate governance supplies those prerequisites.

It must close timezone, offset, session boundary, holiday, early close,
irregular session, leap day, DST gap/fold, week/month/year boundary, expected
position, observation selection, asynchronous-series join, and stable-order
rules. Weekday arithmetic, host locale, exchange-name convention, an
unstated, ambient, implicit, or hidden `252`, and “business day” without exact
authority are prohibited. An explicitly governed, version-bound session count
derived under an admissible contract is not prohibited merely because its
value is 252.

### 6.5 Component E — Benchmark alignment

Benchmark-relative semantics must:

- consume the exact Portfolio Benchmark Declaration carried by the frozen
  Composition;
- treat Explicitly None as an affirmative declaration for which a relative
  method is not applicable, never as missing evidence or permission to choose
  a substitute;
- bind every Single, Composite, or Category observation role to exact Market-
  owned series citations from the declaration;
- prohibit request symbols, provider symbols, “market benchmark,” category
  search, or alternate series;
- require identical or explicitly specified compatible windows, time bases,
  currencies, calendars, return intervals, observation timing, and density;
- specify inner/outer/exact joins, gap treatment, and alignment ordering;
- leave Composite weighting/construction and Category matching unavailable
  unless a later exact governed contract supplies them; and
- hand an exact alignability predicate to WP5/WP7 without defining their
  result outcome.

### 6.6 Component F — Risk-free evidence

The normative contract must prove, before applying any disposition:

1. why `GOVERNED_EVIDENCE` is constitutionally correct;
2. why `VERSIONED_CALCULATION_DEPENDENCY` is constitutionally incorrect for
   the observed risk-free input value or series; and
3. why caller override is constitutionally rejected.

If and only if that proof succeeds, the `GOVERNED_EVIDENCE` placement must
require:

- the value must be an exact M39 Observation or M41 Market Measure Result;
- Market Intelligence remains owner;
- the later method specification must declare the exact role, contract kind,
  identity constraints, required term/tenor/basis qualifications, time
  coordinate, currency/unit, compounding basis, and transformation;
- the manifest must carry the complete exact evidence value and reference;
- selection, resampling, conversion, and transformation order must be fixed;
- the evidence must align to the Portfolio/Benchmark window under explicit
  rules;
- a bare percentage, `0`, `2.5%`, request value, environment variable, config
  value, provider answer, or “current risk-free rate” is invalid; and
- absence or inability to represent the evidence under frozen Market
  contracts blocks the concrete ratio method rather than permitting a
  default.

### 6.7 Component G — Annualization-basis dependency

The normative contract must prove:

1. why `VERSIONED_CALCULATION_DEPENDENCY` is constitutionally correct;
2. why `GOVERNED_EVIDENCE` is constitutionally incorrect for the
   annualization basis;
3. why caller override is constitutionally rejected; and
4. why the proposed owner and placement do not expand Portfolio Intelligence
   authority or transfer ownership of source calendar meaning.

That proof does not create the dependency it justifies. Frozen WP2 §8.1
requires an exact existing governed contract kind, in addition to an exact
constitutional owner, identifier, and immutable version. The frozen corpus
presently supplies no such annualization contract kind. WP4 therefore records
the same fail-closed representability pattern used by WP3 for missing
M42-WP7 Portfolio Composition canonical bytes:

- WP4 MUST NOT author, name, imply, or serialize a new governed dependency
  contract;
- no artificial label in a fixture can satisfy WP2 closure;
- no concrete WP2 annualization dependency declaration or WP3
  `CALCULATION_DEPENDENCY` entry can be formed;
- concrete annualized-return, volatility, or ratio methods remain blocked
  until a separately authorized governance instrument supplies an exact
  owner, existing governed contract kind, identifier, immutable version, and
  canonical value bytes; and
- documentary examples may illustrate elapsed-time, civil-calendar,
  fixed-period, or exact session-calendar arithmetic only when marked
  artificial, non-effective, and incapable of passing the future gate.

The future normative specification may state the semantic information that a
separately governed dependency would have to make exact—source calendar
identity/version, finite decimal or reduced-rational representation,
canonical bytes, compatibility, and Method Version change effects—but may
not define the missing contract or treat that checklist as one.

No unstated, ambient, implicit, or hidden `252`, `365`, `365.25`, or other
constant is permitted. An explicitly governed, version-bound, derived
session-count value—including a value of 252—is not prohibited once an
admissible contract exists.

### 6.8 Component H — Missing data, density, and partial windows

The specification must distinguish:

- structurally absent manifest input;
- present source evidence carrying an authoritative absence;
- boundary gap;
- interior gap;
- duplicate timestamp;
- conflicting value;
- sparse but valid series;
- asynchronous series;
- full requested window;
- exact shorter available window; and
- prohibited fallback window.

It must define the allowed generic modes—such as reject, exact intersection,
omit under an exact denominator rule, or deterministic interpolation—only if
each retained mode has complete semantics. Any interpolation must create
calculation-side working material, never an M39 Observation, and must fix
endpoints, maximum gap, formula, ordering, precision, and rounding.

There is no automatic start-date shift, “use all available,” forward fill,
backfill, zero fill, prior-close fill, benchmark drop, or shorter-window
fallback. WP6–WP8 must state whether a method permits a partial window and its
exact minimum-history predicate. WP5 owns the resulting sufficiency/outcome
classification.

### 6.9 Component I — Numeric model and arithmetic

The contract must fix:

- permitted integer, finite decimal, and reduced-rational forms;
- prohibition or exact treatment of binary floating-point input;
- canonical lexical and byte form;
- input scale, working precision, intermediate precision, output scale, and
  quantization points;
- one closed rounding mode and exact tie behavior per operation requiring
  rounding;
- operation order and prohibition of algebraic reassociation where it changes
  exact results;
- signed zero normalization;
- negative values, values below `-1`, zero denominators, overflow, underflow,
  division by zero, invalid root/log domain, NaN, and infinity;
- comparison/equality semantics; and
- exact failure predicates handed to WP5.

No library, CPU, database numeric type, locale, or serializer may supply an
unstated rule.

Every arithmetic predicate remains a deterministic semantic fact only. It is
not a reason code, Portfolio Computation Outcome, or Degraded State; WP5
retains exclusive classification authority.

### 6.10 Component J — Dependency arithmetic

For every constitutionally admissible calculation dependency the method
consumes, the exact specification must state:

- expected contract kind, identifier, and version;
- exact value/result shape and canonical bytes;
- unit, currency, scale, time basis, window, and subject compatibility;
- whether and where the dependency value enters the operation sequence;
- exact conversion, normalization, and rounding before and after use;
- prohibition of compatible-version substitution;
- treatment of missing, mismatched, unresolved, cyclic, surplus, or
  differently scoped dependencies; and
- deterministic closure over direct and transitive dependencies under frozen
  WP2.

An external facility without an exact constitutional owner and exact existing
governed contract kind is not a calculation dependency for this section and
cannot be made one by listing it. A method requiring such a facility remains
blocked pending separate governance.

WP4 does not define the formula or result identity of a dependency owned by a
later work package.

### 6.11 Component K — Canonical serialization

The normative specification must define exact canonical bytes for:

- Portfolio Measurement Window;
- every WP4-owned closed rule value;
- the annualization-basis dependency identity, version, and value only after
  the §6.7 representability gap is closed outside WP4; artificial documentary
  placeholders must be visibly non-canonical and non-effective;
- finite decimal and reduced-rational values;
- absent/present alternatives where absence is permitted;
- ordered lists and closed maps, if retained; and
- each documentary expected numerical output used in fixtures.

The encoding must be tagged, injective, round-trippable, length-delimited,
order-stable, locale-independent, and reject unknown fields, alternate forms,
trailing bytes, duplicate keys, non-canonical numbers, and Unicode ambiguity.
WP4 must embed or cite WP2/WP3 canonical bytes without changing them.

---

## 7. Explicit no-default matrix

The normative artifact must contain at least the following matrix, expanded
with exact binding and rejection rules:

| Concern | Prohibited ambient/default source | Only permitted closure |
| --- | --- | --- |
| Window cutoff | Wall clock, current date, request receipt time | Exact immutable Portfolio Measurement Window |
| Controlling time coordinate | Input order, most recent field, provider convention, record time substituted for economic time | Exact specification-selected coordinate with source authority, cutoff, interval, and tie rules |
| Timezone | Host, user profile, browser, provider, locale | Exact fixed offset/timezone-free rule, or an external zone facility only after its owner and existing governed contract kind satisfy frozen WP2; otherwise blocked |
| Calendar | Weekdays, exchange-name convention, library default | Explicit calendar-free rule or exact Market calendar identity/version; any required external engine must independently satisfy frozen WP2 or the method remains blocked |
| Base Currency | Workspace, user preference, majority holding currency | Exact historical Ledger-owned Portfolio Base Currency |
| FX | Provider lookup, cache, spot “now,” inferred pair | Exact manifest-bound Market evidence and fixed conversion path |
| Benchmark | Request symbol, hard-coded index, peer lookup | Exact M42 Portfolio Benchmark Declaration and matching Market evidence |
| Benchmark join mode | Library dataframe join, input-order zip, automatic intersection/union | Exact specification-selected exact/inner/outer or other retained mode with ordering and gap semantics |
| Risk-free input | `0`, `2.5%`, config, request, “current rate” | Exact manifest-bound governed Market evidence only after the §6.6 proof succeeds; otherwise fail closed |
| Annualization | Unstated, ambient, implicit, or hidden `252`/`365`; library frequency inference | Exact versioned calculation dependency only after §6.7 representability is separately governed; until then fail closed. Explicitly governed, version-bound derived session counts are permitted |
| Missing observation | Forward/backfill, zero, previous close, alternate provider | Exact retained WP4 mode selected by the immutable specification |
| Partial window | “Use available history” | Exact later method declaration under WP4 mechanics |
| Minimum history | `_MIN_DAYS_FOR_ANNUALIZATION`, UI/config value | Exact later method-specification literal, or a dependency only when a pre-existing owner and governed contract kind satisfy frozen WP2; otherwise blocked |
| Numeric input representation | Binary-float parsing, locale numeric syntax, database coercion, display rounding | Exact canonical integer, finite-decimal, or reduced-rational representation; any binary-float treatment must be explicitly retained and complete |
| Precision | Language/database numeric default | Exact WP4 numeric model selected in the immutable specification |
| Rounding | Language/library default | Exact declared scale, point, mode, and tie rule |
| Arithmetic operation order | Compiler/library reassociation, algebraic equivalence, parallel reduction order | Exact immutable operation sequence and quantization points |
| Dependency version | Latest/compatible/range | Exact WP2 identity/version and WP3 value |
| Evidence ordering | Input order, database order | Exact semantic ordering and tie-break rules |

---

## 8. Documentary golden-vector and fixture architecture

WP4 validation remains non-executable. Fixtures may contain documentary data
and expected results but no executable method, validator, harness, test
runner, or production code. These fixtures are the WP4 golden vectors required
by frozen M43 Architecture; “golden” denotes independently reviewed expected
semantics and bytes, not executable or production authority.

### 8.1 Retained/rejected semantic register

The normative specification must contain one explicit register covering every
optional semantic considered by WP4, including calendar-free/fixed-offset
handling, boundary inclusion, benchmark joins, missing-data modes,
interpolation, partial-window treatment, binary-float treatment, numeric
forms, and annualization rule forms used in artificial documentary examples.
Each row must record:

| Required field | Meaning |
| --- | --- |
| Optional semantic | Exact ordinary rule or mode under review |
| Disposition | Exactly `RETAINED` or `REJECTED` |
| Rationale | Constitutional and deterministic reason for the disposition |
| Owner and binding | Exact owner and immutable-specification placement, without creating a noun |
| Positive/boundary fixtures | Required for every `RETAINED` row |
| Negative fixture | Required for every `RETAINED` and `REJECTED` row |

No optional semantic is available merely because this plan mentions it.
Unregistered, undecided, or incompletely specified modes fail closed. Fixture
coverage must trace by row to this register: every retained mode has positive,
boundary, and rejection coverage, while every rejected mode has direct
rejection coverage. Artificial annualization examples must additionally cite
the §6.7 representability gap and cannot establish dependency conformance.
“Retained/rejected semantic register” and “representability gap” are ordinary
documentary labels, not constitutional nouns or governed contract types.

### 8.2 Required positive and boundary vectors

At minimum, the positive corpus must independently demonstrate:

1. window start inclusion and exclusion;
2. end/cutoff inclusion and exclusion;
3. elapsed-duration versus civil-period distinction;
4. host-timezone independence;
5. fixed-offset behavior;
6. named-zone version binding;
7. DST gap;
8. DST fold;
9. holiday and early close;
10. market closure producing no eligible observation;
11. leap day and year boundary;
12. economic-time versus record-time selection;
13. stable ordering under input permutation;
14. exact Base Currency match;
15. direct FX conversion;
16. permitted explicit cross-rate conversion, if retained;
17. Base Currency change without retroactive reinterpretation;
18. aligned Portfolio and Benchmark series;
19. asynchronous-calendar alignment;
20. Explicitly None applicability predicate;
21. exact governed risk-free evidence after the §6.6 proof succeeds;
22. risk-free term/time alignment;
23. artificial elapsed annualization arithmetic under the §6.7 gap;
24. artificial calendar annualization arithmetic under the §6.7 gap;
25. artificial exact session-count annualization arithmetic, expressly
    incapable of satisfying WP2;
26. boundary gap;
27. interior gap;
28. sparse-history density;
29. exact partial-window classification predicate;
30. permitted deterministic interpolation, if retained;
31. decimal tie and rounding boundary;
32. intermediate-rounding sensitivity;
33. negative zero normalization;
34. negative value;
35. zero denominator;
36. dependency arithmetic order;
37. dependency version identity;
38. canonical numeric round trip;
39. Portfolio Measurement Window round trip; and
40. byte-identical output across presentation order, locale, timezone, and
    platform assumptions.

### 8.3 Required negative vectors

At minimum, the negative corpus must reject:

- wall-clock/current-date windows;
- host timezone or locale;
- weekday calendar, “standard calendar,” and unstated, ambient, implicit, or
  hidden `252`;
- a required calendar/zone facility lacking an exact owner or governed
  contract kind, or a constitutionally admissible dependency that is missing
  or version-ranged;
- inferred Base Currency or currency code;
- provider-selected, stale, missing, ambiguous, or temporally misaligned FX;
- implicit FX inversion or cross rate;
- request/hard-coded/default benchmark;
- a declared Benchmark whose exact evidence has a boundary or interior gap;
- substituted Benchmark for Explicitly None;
- unsupported Composite or Category construction/matching;
- request/config/default risk-free value;
- provider designation as canonical risk-free identity;
- missing, ranged, compatible, or caller-overridden annualization dependency;
- forward fill, backfill, zero fill, previous-close fill, and silent window
  shortening;
- undeclared interpolation or normalization;
- duplicate/conflicting time point;
- binary-float drift where exact decimal/rational input is required;
- unspecified precision, rounding, tie rule, or operation order;
- NaN, infinity, overflow, invalid domain, and division by zero;
- cross-Portfolio evidence or dependency;
- source-owner mismatch;
- mutable reference, live lookup, cache, or “latest” resolution;
- new manifest fields/categories or new Method Version fields;
- early WP5 result/outcome/degradation semantics;
- early WP6–WP8 formula admission; and
- any production, runtime, provider, persistence, API, UI, or executable-
  validation claim.

### 8.4 Vector format

Every vector must state:

- vector identifier;
- semantic component;
- exact frozen prerequisites;
- exact documentary input records and canonical representations;
- immutable method-specification choices;
- exact dependency identities and versions;
- exact operation sequence;
- expected semantic predicate or exact numerical/canonical-byte result;
- rejection reason for negative vectors;
- owner-preservation proof; and
- the architectural completion criterion exercised.

Independent numerical review must recompute expected values without using an
implementation under review.

---

## 9. Deliverables

### 9.1 Primary constitutional artifact

Create:

`docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`

It must include:

1. authority and precedence;
2. exact scope and exclusions;
3. vocabulary sufficiency/gate result;
4. field-level ownership matrix;
5. Components A–K from §6;
6. the risk-free and annualization constitutional proof record, including
   accepted/rejected authority classes, caller-override rejection, and the
   annualization representability gap;
7. the no-default matrix;
8. exact canonical serialization;
9. compatibility and non-substitutability;
10. WP2/WP3 binding examples;
11. WP5–WP8 handoffs;
12. prohibited interpretation corpus;
13. the retained/rejected semantic register;
14. fixture register and coverage traceability; and
15. completion and independent-review gate.

### 9.2 Documentary numerical fixtures

Create:

- `docs/implementation/m43/fixtures/M43_WP4_POSITIVE_NUMERICAL_VECTORS.md`
- `docs/implementation/m43/fixtures/M43_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md`

The positive file may contain exact numerical expected values and canonical
bytes. Neither file may contain executable code.

### 9.3 Review artifacts

After the primary artifact and fixtures are complete:

- an independent architectural and constitutional review;
- an independent numerical review;
- a required-corrections response if either review identifies findings; and
- an independent confirmation after all accepted corrections.

Review and confirmation artifacts must remain separate from the authoring
artifact. WP4 becomes complete and frozen only after both review dimensions
are approved and all findings are closed.

### 9.4 Conditional vocabulary synchronization

WP4 requires no Glossary change and does not perform the outstanding WP1
§9.2/§9.4 synchronization. If a future vocabulary gate identifies an
unavoidable admission or rename, WP4 remains blocked until a separately
authorized workflow completes the required Glossary governance. Tokens,
fields, rule modes, dependency tags, and fixture labels must not be added to
the Glossary.

---

## 10. Dependency-safe implementation sequence

“Implementation” in this section means documentary specification work only.

1. **Freeze the authority baseline.** Record M43 Architecture and WP1–WP3 as
   immutable prerequisites. Make no edits to them.
2. **Run the WP4 vocabulary test.** Prove Portfolio Measurement Window is the
   only WP4 governed noun required, or gate any unavoidable candidate before
   reliance.
3. **Build the semantic-surface register.** For every Component A–K, record
   owner, non-owner, placement, upstream contract, dependency exposure,
   downstream handoff, prohibited defaults, and required vectors.
4. **Prove the authority-class dispositions.** For risk-free input, prove
   `GOVERNED_EVIDENCE`, reject `VERSIONED_CALCULATION_DEPENDENCY`, and reject
   caller override. For annualization, prove
   `VERSIONED_CALCULATION_DEPENDENCY`, reject `GOVERNED_EVIDENCE`, reject
   caller override, and prove no Portfolio Intelligence authority expansion.
   Do not ratify either proposition without its constitutional proof.
5. **Classify dependency placement.** Separate dependencies that already have
   an exact constitutional owner and existing governed contract kind from
   external facilities that lack either coordinate. The latter cannot become
   WP2 dependencies and remain blocked pending separate governance.
6. **Specify the Portfolio Measurement Window.** Complete its shape,
   invariants, canonical bytes, identity, and rejection rules first because
   all later temporal semantics depend on it.
7. **Specify temporal selection.** Close economic/record time, cutoff,
   interval, timezone, calendar, session, DST, ordering, and alignment.
8. **Specify currency and FX.** Preserve historical Base Currency, source
   ownership, conversion path, placement, ordering, and fail-closed gaps.
9. **Specify benchmark alignment.** Bind the M42 declaration and exact Market
   evidence; close Explicitly None and unsupported-form behavior.
10. **Specify risk-free evidence after proof.** If the §6.6 proof succeeds,
    close exact Market-evidence roles and prohibit every caller/default path.
11. **Record the annualization representability gap after proof.** If the
    §6.7 authority-class proof succeeds, record that no exact existing
    governed contract kind is presently available, prohibit invented
    contract kinds and concrete WP2/WP3 binding, mark examples artificial,
    and keep annualized methods blocked pending separate governance.
12. **Specify missing/partial semantics.** Close gaps, density, duplicates,
   intersection, interpolation if retained, and the WP5 handoff.
13. **Specify arithmetic.** Close numeric types, precision, scale, rounding,
   exceptional values, operation order, and dependency arithmetic.
14. **Specify canonical serialization.** Prove injectivity, round trip,
   canonical rejection, and composition with frozen WP2/WP3 bytes.
15. **Complete the retained/rejected register and fixtures.** Record every
    optional semantic as retained or rejected with rationale. Bind positive,
    boundary, and negative fixture coverage to every retained row and direct
    rejection coverage to every rejected row.
16. **Perform whole-corpus conflict scans.** Search for caller overrides,
    unstated, ambient, implicit, or hidden `252`, hard-coded risk-free values,
    request benchmarks, clock/
    provider/locale dependencies, early WP5 semantics, and early formulas.
17. **Perform independent architectural review.** Verify scope, ownership,
    placement, vocabulary, frozen-contract preservation, and no authority
    leakage.
18. **Perform independent numerical review.** Recompute all values and bytes;
    test boundary, ordering, rounding, dependency, and cross-platform cases.
19. **Correct only WP4 artifacts.** Never cure a finding by editing M43
    Architecture or WP1–WP3.
20. **Close the external governance dependency.** Before WP4 confirmation,
    require the §1.1 workflows to complete under their own authority without
    modifying a frozen artifact in WP4.
21. **Obtain independent confirmation.** Freeze WP4 only after architectural
    and numerical approval, completed §1.1 dependency, and unresolved
    findings `NONE`.
22. **Preserve downstream gates.** WP4 confirmation does not release WP6; the
    WP1 §7.4 governance block remains independently governed. WP7 annualized
    or ratio specifications remain blocked while the §6.7 representability
    gap is open.

---

## 11. Review plan

### 11.1 Architectural and constitutional review

The reviewer must verify:

- exact match to frozen M43-WP4 scope;
- no M43/WP1–WP3 redesign or reinterpretation;
- singular ownership for every field and rule;
- no new WP2 or WP3 field/category;
- no result, formula, runtime, provider, or production authority;
- complete vocabulary disposition;
- complete constitutional proof for the risk-free and annualization
  authority-class dispositions, including rejection of each alternative and
  caller override;
- fail-closed annualization representability with no WP4-authored contract
  kind;
- exact evidence/dependency placement;
- rejection of external facilities as WP2 dependencies when they lack an
  exact constitutional owner or exact existing governed contract kind;
- complete retained/rejected register with rationale and fixture
  traceability;
- arithmetic predicates remain semantic facts and never become reason codes,
  Portfolio Computation Outcomes, or Degraded States;
- completion of the §1.1 dependency under its own authority before
  confirmation, without releasing the independently governed WP6 block;
- no caller override or ambient default;
- explicit WP5–WP8 handoffs; and
- no frozen artifact changes.

### 11.2 Independent numerical review

The numerical reviewer must verify:

- every formula-like generic transform is fully specified;
- exact decimal/rational arithmetic;
- all precision and rounding points;
- operation-order sensitivity;
- boundary and leap/DST behavior;
- FX direction and placement;
- benchmark and risk-free alignment;
- artificial annualization values only as documentary arithmetic, with no
  claim of dependency conformance while the representability gap remains;
- missing/partial-window treatment;
- exceptional-value closure;
- canonical-byte round trips; and
- independent recomputation of every positive expected value.

### 11.3 Mandatory review independence

The author of the normative specification must not self-confirm it.
Architectural and numerical conclusions may be produced in one coordinated
review only if the artifact identifies the independent competence and
separate conclusion for each dimension.

---

## 12. Acceptance and completion criteria

WP4 is complete only when all statements below are true:

1. the normative specification covers every frozen WP4 scope item;
2. Portfolio Measurement Window has one exact immutable contract and
   canonical representation;
3. every time coordinate has one role, authority, selection rule, and stable
   ordering rule;
4. Portfolio Base Currency is exact, historical, and never inferred;
5. every permitted FX conversion has exact evidence, direction, time,
   placement, operation order, precision, and rounding;
6. every calendar/timezone rule is explicit and version-bound where output-
   affecting;
7. benchmark alignment consumes only the exact M42 declaration and matching
   Market evidence;
8. Explicitly None never triggers substitution;
9. the normative specification constitutionally proves why risk-free input is
   governed Market evidence, why versioned calculation dependency placement
   is rejected, and why caller override is rejected;
10. the normative specification constitutionally proves why annualization
    basis requires versioned calculation dependency placement, why governed
    evidence and caller override are rejected, and why this disposition does
    not expand Portfolio Intelligence authority; it also records the open
    §6.7 representability gap and admits no concrete dependency while that gap
    remains;
11. no hidden `2.5%`, unstated, ambient, implicit, or hidden `252`, current
    date, provider symbol, request benchmark, weekday calendar, locale, or
    library convention remains; an explicitly governed, version-bound,
    derived session-count value is not prohibited;
12. missing, sparse, duplicate, conflicting, asynchronous, and partial-window
    cases either retain one fully specified deterministic semantic mode or
    fail closed, consistently with §6.8;
13. numeric type, scale, precision, rounding, tie, exceptional-value, and
    operation-order semantics are complete;
14. dependency arithmetic is exact, closed, non-substitutable, and acyclic
    under WP2;
15. all WP4 canonical encodings are injective and round-trippable;
16. every optional semantic is recorded `RETAINED` or `REJECTED` with
    rationale, every retained semantic has positive, boundary, and negative
    documentary vectors, and every rejected semantic has a direct rejection
    vector;
17. two independent readers derive the same selection, alignment, arithmetic
    predicates, exact values, and canonical bytes;
18. WP5 receives facts but no pre-decided result classification;
19. WP6–WP8 receive mechanics but no pre-admitted method or formula;
20. every WP4-local noun has a confirmed disposition; WP4 requires no
    Glossary change and does not perform the outstanding WP1 synchronization;
21. runtime, source-code, implementation, persistence, API, UI, provider,
    production-method, and executable-validation authority remain `NONE`;
22. no M1–M43-WP3 artifact is modified;
23. dependencies admitted under WP2 already have an exact constitutional
    owner and exact existing governed contract kind; external facilities
    lacking either coordinate remain blocked and are not treated as
    dependencies;
24. the external governance dependency in §1.1 is completed under its own
    authority before WP4 confirmation is recorded, without WP4 modifying a
    frozen artifact or `docs/GLOSSARY.md`;
25. WP4 confirmation does not release WP6, and the WP1 §7.4 governance block
    remains independently governed;
26. independent architectural review is approved;
27. independent numerical review is approved; and
28. unresolved findings are `NONE`.

---

## 13. Risks and mandatory responses

| Risk | Mandatory response |
| --- | --- |
| M41 Market contracts are copied and relabeled | Reuse patterns only; define independently owned Portfolio semantics |
| WP4 becomes a formula package | Keep method formulas and method-specific choices in WP6–WP8 |
| WP4 changes accounting | Limit currency conversion to analytics-side exact input interpretation; never amend Ledger arithmetic |
| Portfolio Base Currency format is invented | Cite the exact Asset Foundation-owned reference available; fail closed if canonical bytes are unavailable |
| Risk-free status becomes a Portfolio assertion | Consume exact Market evidence only; later WP7 names the role and transformation |
| Annualization remains a literal hidden in a formula | Prove the authority class, preserve the §6.7 representability gap, and block concrete dependency use until separate governance supplies every frozen-WP2 coordinate |
| Calendar or timezone library changes output | Use a complete calendar-free/fixed-offset rule, or require a pre-existing exact owner and governed contract kind; otherwise remain blocked |
| Request parameters smuggle governed choices | Reject benchmark, risk-free, annualization, calendar, Base Currency, and governed-dependency overrides |
| Partial history silently changes the question | Exact window remains fixed; later method explicitly permits or rejects a partial mode |
| Missing data becomes fabricated evidence | Derived working values never become M39 Observations; no fill unless fully specified and explicitly selected |
| FX helper invents a path | Require exact evidence and a declared direct/cross path; otherwise fail closed |
| Composite/Category benchmark is guessed | Remain unavailable until an exact governed construction/matching contract exists |
| Floating-point implementation defines semantics | Normative decimal/rational model and canonical bytes control |
| Equivalent algebra changes rounding | Fix operation order and quantization points; include non-commutative vectors |
| WP4 predefines WP5 outcomes | Hand off predicates only |
| Documentary fixtures become executable authority | Markdown/data-only fixtures; no runner or harness |
| Missing M42 Composition bytes are bypassed | Preserve WP3 fail-closed rule; use explicitly artificial documentary nesting only where WP3 permits |

---

## 14. Repository effect

WP4 may add only:

- this planning artifact;
- the primary normative WP4 specification;
- WP4 documentary fixture files;
- WP4 independent review, correction-response, and confirmation artifacts;
  and
- no Glossary change; any future vocabulary admission/rename workflow remains
  separately authorized and outside WP4.

WP4 must not modify backend, frontend, database, migration, API, operational,
provider, deployment, or executable-test files. It must not update ROADMAP
capability completion. Implementation Index and consolidated Decision Log
updates remain governed by M43 epic closeout unless separately authorized.

---

## 15. Final constitutional boundary

M43-WP4 is complete numerical semantics, not a calculation product.

It receives one exact Portfolio subject, one exact Portfolio Method Version,
one complete exact Portfolio Analytics Input Manifest, and only dependency
values already representable under frozen WP2/WP3. It defines how later
Portfolio methods must select,
align, express, and combine those values without ambient convention. It
returns only deterministic semantic facts to the later contracts.

It never chooses another Portfolio, another benchmark, a current time, a
provider, a risk-free default, an annualization constant, a calendar default,
a missing-data fallback, or an implementation. It never changes accounting,
source evidence, Provenance, or another owner's vocabulary. It admits no
formula and no production method.

It cannot convert an external facility into a WP2 dependency and cannot cure
the missing annualization contract kind. While that representability gap is
open, annualized methods remain blocked and documentary examples remain
artificial. WP4 confirmation also does not release the independently governed
WP1 §7.4 WP6 block.

That is the complete scope reserved to WP4 by the frozen M43 Architecture.
