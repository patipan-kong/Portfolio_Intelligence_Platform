# M43-WP7 — Constitutional Scope and Implementation Plan

**Milestone:** M43 — Portfolio Analytics Contract Foundation  
**Work package:** M43-WP7 — Risk and Benchmark-Relative Method Specifications  
**Artifact class:** Documentary constitutional scope and implementation plan  
**Revision:** RC2  
**Status:** COMPLETE AND FROZEN  
**Final Independent Constitutional Confirmation:** CONFIRMED  
**Unresolved findings:** NONE  
**Normative method-work status:** BLOCKED PENDING INHERITED GATE CLOSURE  
**Runtime authority:** `NONE`  
**Source-code authority:** `NONE`  
**Persistence authority:** `NONE`  
**Database/schema authority:** `NONE`  
**API authority:** `NONE`  
**UI authority:** `NONE`  
**Provider authority:** `NONE`  
**Implementation authority:** `NONE`  
**Executable-validation authority:** `NONE`  
**Production-method authority:** `NONE`

This artifact plans documentary work only. It defines no formula, algorithm,
executable fixture, runtime behavior, production method, or operational
authority.

---

## 0. Executive determination

The requested label “M43-WP7 — Core Performance and Rolling Method
Specification” cannot be adopted.

Frozen M43 Architecture section 9 assigns:

- **M43-WP6 — Core Performance and Rolling Method Specifications**; and
- **M43-WP7 — Risk and Benchmark-Relative Method Specifications**.

M43-WP6 is complete, confirmed, and frozen as a constitutional planning work
package. Reallocating its subject matter to WP7 would violate constitutional
allocation, ownership and placement singularity, the frozen implementation
sequence, and the prohibition against redesigning completed work packages.

This plan therefore preserves the frozen allocation and defines M43-WP7
exclusively as the documentary work package for:

- drawdown;
- volatility;
- downside deviation;
- Sharpe ratio;
- Sortino ratio;
- beta;
- correlation;
- alpha;
- tracking error;
- information ratio;
- declared-benchmark applicability;
- required risk-free, calendar, and annualization dependencies; and
- sufficiency, degraded-state, and numerical-validation obligations for those
  methods.

Core performance, cumulative return, annualized return, rolling return,
normalized performance series, valid-history rules for those outputs, and
their period-return chaining remain solely within frozen M43-WP6.

Frozen M43-WP1 section 7.4 records the separate standing block:

> `M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6`

That block concerns future WP6 normative method work, not the confirmed status
of the frozen WP6 planning artifact. It is inherited transitively by WP7.
WP7 planning may proceed, but normative WP7 method work must fail closed until
the M43 governance correction and every other applicable inherited gate are
demonstrably closed.

---

## 1. Constitutional objective

M43-WP7 shall plan a future, non-production documentary corpus through which
two independent readers can identify the same:

- Portfolio Measure Definition;
- Portfolio Method Version;
- applicable Portfolio Measure Subject;
- Portfolio Analytics Input Manifest requirements;
- Portfolio Measurement Window;
- required Portfolio and benchmark return dependencies;
- risk-free evidence dependency, where applicable;
- annualization-basis dependency, where applicable;
- calendar and alignment requirements;
- applicability determination;
- Portfolio Input Sufficiency determination;
- Portfolio Computation Outcome;
- Degraded State relationship;
- Portfolio Measure Result meaning;
- lineage and Provenance carriage;
- numerical operation order; and
- expected documentary outcome.

The future corpus must do so without consulting:

- live providers;
- ambient configuration;
- request-selected benchmark symbols;
- wall-clock time;
- implicit calendars;
- hidden annualization factors;
- hidden risk-free rates;
- library defaults;
- deployment-specific behavior; or
- cross-portfolio state.

This objective does not deploy Advanced Risk Metrics, activate
benchmark-relative analytics, or admit any production method.

---

## 2. Governing authority

### 2.1 Authority order

WP7 shall consume the following authorities in order:

1. Platform Architecture Laws 1–15;
2. ADR-001 through ADR-005;
3. frozen M34 ownership allocations;
4. [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md);
5. frozen M39 Market Observation contracts;
6. frozen M40–M41 Market Measure vocabulary and contracts;
7. frozen M42 Portfolio Intelligence contracts, especially M42-WP5 and
   M42-WP7;
8. frozen M43 Architecture and Implementation Plan;
9. frozen M43-WP1 through M43-WP6 artifacts;
10. independently confirmed normative specifications required by those frozen
    plans; and
11. future WP7 documentary specifications, only within the scope allocated
    here.

A lower authority cannot amend, weaken, reinterpret, or bypass a higher
authority.

Legacy source code, deployed formulas, third-party libraries, provider
behavior, API contracts, and UI behavior are evidence of current state only.
They possess no constitutional or method authority.

### 2.2 Authority declarations

| Authority class | WP7 planning authority |
| --- | --- |
| Constitutional allocation | Exact frozen consumption only |
| Vocabulary | Reuse confirmed vocabulary; conditional local gate for unavoidable new nouns |
| Ownership | Exact frozen consumption only |
| Documentary planning | Authorized |
| Governance correction | `NONE` |
| Frozen-artifact amendment | `NONE` |
| Future-WP design | `NONE` |
| Future documentary WP7 method specification | Conditional on all applicable inherited gates |
| Static documentary vectors | Conditional on confirmed normative rows |
| Executable specification or fixture | `NONE` |
| Runtime calculation | `NONE` |
| Production method | `NONE` |
| Registry activation | `NONE` |
| Persistence or serialization implementation | `NONE` |
| API or UI adoption | `NONE` |
| Provider selection or retrieval | `NONE` |
| Capability-completion declaration | `NONE` |

---

## 3. Dependency model and inherited gates

### 3.1 Hard dependencies

| Dependency | Sole authority consumed | Exact WP7 reliance | WP7 prohibition |
| --- | --- | --- | --- |
| M43-WP1 sections 7.3–7.4 | Confirmed vocabulary, ownership split, negative corpus, legacy inventory, and standing M43 governance block | Reuse exact dispositions and preserve the split between Portfolio-performance meaning and accounting-input semantics | No reopening, silent admission, ownership merger, or local release of the block |
| M43-WP2 | Definition, Method Version, applicability, and dependency contracts | Exact identity and dependency closure | No alternative identity or dependency grammar |
| M43-WP3 Subject section 7.1 and Manifest sections 6.3 and 10.3 | Subject and Input Manifest contracts plus inherited Portfolio Composition byte gap | One exact Portfolio Composition and closed evidence set only after representability closure | No side input, live lookup, manifest repair, invented nested bytes, or premature binding |
| M43-WP4 sections 6.6–6.7 and required normative specification | Temporal, currency, calendar, benchmark, risk-free, annualization, alignment, and arithmetic semantics | Exact independently confirmed normative rows | No use of planning propositions as operative semantics |
| M43-WP5 and required normative specification | Result, sufficiency, outcome, degraded-state relation, lineage, Provenance, and serialization | Exact independently confirmed result contract | No parallel result envelope |
| M43-WP6 sections 0, 3.1, 3.2, and 12 | Core performance and rolling method allocation, inherited gates, and future dependency corpus | Exact independently confirmed Portfolio-return dependencies required by WP7 | No duplicate return calculation and no reliance on an unauthorized WP6 method |
| M42-WP5 | Portfolio Benchmark Declaration | Sole portfolio benchmark-selection authority | No request or provider-symbol substitution |
| M42-WP7 section 5 | Portfolio Composition and its recorded canonical-byte representability boundary | Exact governed subject after separate representability closure | No alternative portfolio snapshot or invented canonical bytes |
| M39–M41 | Market observations and measures | Exact benchmark, risk-free, FX, calendar, and other market evidence | No provider knowledge or live market lookup |
| Asset Foundation | Asset identity, currency, classification, and taxonomy references | Exact versioned references where required | No Portfolio Intelligence redefinition |
| Period-return accounting semantics | Ledger & Accounting under Portfolio Calculation Rules sections 1–9 | Authoritative accounting-derived evidence | No accounting recomputation |
| Period-return consumption rule | Portfolio Calculation Rules section 10, subject to the pending M43 governance correction | Exact corrected dependency semantics consumed through WP6 | No second period-return rule |
| ADR-001 through ADR-005 | Source-of-truth, replay, timeline, single-rule, and correctness-baseline constraints | Preserve upstream rule singularity and evidentiary authority | No second implementation or custody-to-ownership inference |

The two required binding-source paths established by the frozen plans are:

- `docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`;
  and
- `docs/implementation/M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md`.

If either specification is independently confirmed under a different path,
WP7 must cite that exact confirmed path instead. A plan, expected filename, or
unchanged prerequisite is not a substitute for an existing independently
confirmed normative specification.

M41 contracts may be used as mechanical precedent only. Market
Intelligence-owned contract types, identities, methods, or outcomes do not
become Portfolio Intelligence contracts by analogy.

### 3.2 Inherited external gates

The following gates are outside WP7 ownership and cannot be closed locally:

1. **WP7 identity gate — frozen M43 Architecture section 9.**  
   The work package must retain the frozen title and allocation “Risk and
   Benchmark-Relative Method Specifications.” Core performance and rolling
   semantics remain in WP6.

2. **M43 governance-correction gate — frozen WP1 sections 7.3–7.4.**  
   Frozen WP1 section 7.3 assigns Portfolio-performance measure meaning to
   Portfolio Intelligence while Ledger & Accounting retains the accounting
   semantics determining what enters the return. Frozen WP1 section 7.4
   records:

   > `M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6`

   Closure belongs to the M43 governance sequence, not WP6 or WP7. No WP7
   dependency row may bind a WP6 Portfolio-return method until the correction
   is independently confirmed and the resulting WP6 normative method
   specification is independently confirmed.

3. **WP6 normative completion gate — frozen M43 Architecture section 9 and
   frozen WP6 sections 0, 3.2, 12, and 15.2.**  
   Frozen M43 orders WP7 after WP6. The confirmed WP6 planning artifact is not
   a substitute for the required independently confirmed
   `M43_WP6_CORE_PERFORMANCE_AND_ROLLING_METHOD_SPECIFICATION.md`, or its exact
   independently confirmed alternate path, method identities, dependency
   results, and documentary validation corpus. WP7 may not invent or recompute
   Portfolio returns while that dependency is unavailable.

4. **WP3/M42-WP7 representability gate — frozen WP3 Subject section 7.1,
   frozen WP3 Manifest sections 6.3 and 10.3, and M42-WP7 section 5.**  
   No effective Portfolio Measure Subject, Input Manifest, result identity,
   hash, or canonical-byte vector may be claimed until the Portfolio
   Composition canonical-byte representability gap is separately closed.

5. **WP4 normative-specification gate — frozen WP4 plan and frozen WP6
   sections 3.1–3.2.**  
   WP7 may bind no calendar, alignment, missing-data, precision, rounding,
   risk-free, annualization, or arithmetic convention until the required
   independently confirmed WP4 normative specification exists and is cited by
   its exact repository path.

6. **WP5 normative-result gate — frozen WP5 plan and frozen WP6 sections
   3.1–3.2.**  
   WP7 may bind no result classification, value-presence rule, sufficiency
   outcome, degraded-state relationship, lineage, Provenance, temporal claim,
   identity, or canonical serialization until the required independently
   confirmed WP5 normative specification exists.

7. **Risk-free-evidence gate — frozen WP4 section 6.6.**  
   Sharpe, Sortino, alpha, or any other method requiring a risk-free input
   remains blocked until WP4 has confirmed the input's authority class and
   exact binding rules. The planned disposition requires exact manifest-bound
   Market Intelligence evidence, but WP7 cannot treat the planning
   proposition as a confirmed normative rule.

8. **Annualization-dependency gate — frozen WP4 section 6.7.**  
   Annualized volatility, tracking error, downside deviation, Sharpe, Sortino,
   information ratio, alpha, or any other annualized method remains blocked
   until a separately governed instrument supplies the exact owner, governed
   contract kind, identifier, immutable version, canonical value
   representation, WP2 declaration, and WP3 manifest entry required by frozen
   WP4.

9. **Benchmark-form evidence gate — frozen M42-WP5, frozen WP4 section 6.5,
   and frozen M43 Architecture section 9.**  
   `Single` benchmark declarations may be used only when exact conforming
   evidence exists. `Composite` and `Category` forms remain unavailable
   wherever exact construction, weighting, membership, or matching evidence
   is not governed and representable.

10. **Vocabulary gate — frozen WP1 downstream vocabulary rule.**  
    No WP7-local noun may be relied upon until it receives an independently
    reviewed `ADMIT`, `REUSE`, `RENAME`, or `REJECT` disposition with one owner
    and one normative home.

Failure of one gate blocks the affected method or claim. It never authorizes a
fallback, weakened dependency, alternate formula, or ownership transfer.

### 3.3 Dependency flow

```text
Independently confirmed M43 governance correction
        +
Exact M42 Portfolio Composition
        +
Independently confirmed WP6 Portfolio-return dependencies
        +
M42 Portfolio Benchmark Declaration
        +
Exact M39/M41 benchmark and risk-free evidence
        +
Explicit WP4-governed calendar, alignment,
annualization, arithmetic, and missing-data semantics
        +
Exact WP2/WP3 method and manifest bindings
        |
        v
Future non-production WP7 method specification
        |
        v
WP5-conforming documentary Portfolio Measure Result
```

No arrow represents executable flow or production behavior.

---

## 4. Constitutional scope

### 4.1 In scope after applicable gates close

WP7 shall plan future documentary specifications for:

1. drawdown;
2. volatility;
3. downside deviation;
4. Sharpe ratio;
5. Sortino ratio;
6. beta;
7. correlation;
8. alpha;
9. tracking error;
10. information ratio;
11. exact method applicability by Portfolio Benchmark Declaration form;
12. exact input and calculation-dependency declarations;
13. exact sample and valid-history requirements;
14. exact calendar and observation-alignment requirements;
15. exact missing, sparse, duplicate, and asynchronous observation treatment;
16. exact numerical representation, operation ordering, precision,
    quantization, and rounding;
17. exact sufficiency and fail-closed result mappings;
18. documentary positive, boundary, and negative vectors;
19. legacy-behavior characterization; and
20. constrained handoff to M43-WP9.

Each retained method must eventually have one non-production Portfolio Measure
Definition and one exact Portfolio Method Version for each non-substitutable
method specification.

### 4.2 Explicit exclusions

WP7 does not:

- specify core performance or rolling-return methods;
- define or recompute canonical period return;
- define cumulative, annualized, rolling, or normalized performance;
- change Ledger & Accounting arithmetic;
- redefine Portfolio Composition;
- redefine Portfolio Benchmark Declaration;
- choose a benchmark for a Portfolio;
- permit request-selected benchmark symbols;
- construct Composite benchmarks;
- match Category benchmarks;
- define provider lookup or symbol resolution;
- define Market Observation or Market Measure semantics;
- create a risk-free observation or market series;
- create the missing annualization dependency contract;
- define benchmark-relative attribution or BHB decomposition;
- define position or sector attribution;
- define recommendation, optimization, suitability, constraint, or execution
  semantics;
- grade performance or establish causal explanations;
- define cross-portfolio or Wealth Intelligence analytics;
- select runtime modules, libraries, databases, caches, endpoints, or call
  sites;
- deprecate legacy behavior;
- create executable fixtures or tests;
- admit production methods; or
- modify any frozen M43-WP1 through WP6 artifact.

### 4.3 Essential boundary

WP7 owns the documentary meaning of Portfolio-derived risk and
declared-benchmark-relative measures.

It does not own:

- accounting evidence;
- market evidence;
- benchmark declaration;
- calendar meaning;
- source risk-free observations;
- Portfolio-return methods;
- Provenance meaning;
- runtime placement; or
- downstream evaluation.

---

## 5. Vocabulary gate

### 5.1 Closed inherited vocabulary

| Term | Disposition | Owner / grammar authority | WP7 permitted use |
| --- | --- | --- | --- |
| Portfolio Measure | `ADMIT` | Portfolio Intelligence | Exact inherited meaning |
| Portfolio Measure Definition | `ADMIT` | Portfolio Intelligence under frozen WP2 | Exact frozen WP2 contract |
| Portfolio Method Version | `ADMIT` | Portfolio Intelligence under frozen WP2 | Exact frozen WP2 contract |
| Portfolio Measure Subject | `ADMIT` | Portfolio Intelligence under frozen WP3 | Exact frozen WP3 contract after representability closure |
| Portfolio Analytics Input Manifest | `ADMIT` | Portfolio Intelligence under frozen WP3 | Exact frozen WP3 contract after representability closure |
| Portfolio Measurement Window | `ADMIT` | Portfolio Intelligence | Exact semantics only from the independently confirmed WP4 normative specification |
| Portfolio Input Sufficiency | `ADMIT` | Portfolio Intelligence | Exact semantics only from the independently confirmed WP5 normative specification |
| Portfolio Measure Result | `ADMIT` | Portfolio Intelligence | Exact frozen result contract only after WP5 confirmation |
| Portfolio Computation Outcome | `ADMIT` | Portfolio Intelligence | Exact frozen result classification only after WP5 confirmation |
| Portfolio Deterministic Calculation | `ADMIT` | Portfolio Intelligence | Exact inherited calculation relation only after WP5 confirmation |
| Portfolio Degraded State | `REUSE` | M34-D-0005 producing-domain grammar | Use `Degraded State`; never admit the prefixed noun |
| Degraded State | `REUSE` | M34-D-0005 producing-domain grammar | Exact inherited meaning |
| Portfolio Benchmark Declaration | `ADMIT` | Portfolio Intelligence under frozen M42-WP5 | Exact declaration; never a request-selected replacement |
| Portfolio Composition | `ADMIT` | Portfolio Intelligence under frozen M42-WP7 | Exact subject after inherited representability closure |
| Canonical Temporal Claim | `REUSE` | M34-D-0005 grammar authority | Exact WP5-confirmed compatibility mapping |
| Provenance | `REUSE` | Connectivity & Ingestion | Carry exact already-captured Provenance; never recapture |

`UNAVAILABLE` remains a Degraded State and must not become a Portfolio
Computation Outcome.

The method-family labels listed in frozen M43 Architecture section 9 are
allocation labels. Ordinary descriptive quantity phrases used by this plan,
including “active return” and “excess return,” are not admitted constitutional
nouns, contract kinds, identities, or fixture-schema fields. Any future WP7
corpus that requires either phrase as a governed semantic term must route it
through section 5.2 before reliance.

### 5.2 WP7-local vocabulary procedure

Before relying on any new noun, WP7 must:

1. prove inherited vocabulary is insufficient;
2. record exactly one disposition of `ADMIT`, `REUSE`, `RENAME`, or `REJECT`;
3. identify one semantic owner;
4. identify one normative home;
5. perform repository-wide collision and overlap analysis;
6. obtain independent vocabulary review and confirmation; and
7. synchronize any confirmed admission or rename with `docs/GLOSSARY.md` in
   the same authorized change.

No fixture field, method identity, or acceptance criterion may implicitly
admit a noun.

**Current planning conclusion:** no new constitutional noun is required by
this plan.

---

## 6. Ownership model

| Concern | Sole owner | WP7 relationship | Prohibited WP7 action |
| --- | --- | --- | --- |
| Portfolio-performance measure meaning | Portfolio Intelligence under frozen WP1 section 7.3 | Consume exact WP6 Portfolio-return method results after all gates close | No transfer to Ledger & Accounting and no recomputation |
| Accounting semantics determining what enters period return | Ledger & Accounting under frozen WP1 section 7.3 and Portfolio Calculation Rules | Consume only through the corrected and confirmed WP6 dependency boundary | No Portfolio Intelligence restatement |
| Portfolio-derived risk meaning | Portfolio Intelligence | Specify future non-production methods | No production activation |
| Declared-benchmark-relative measure meaning | Portfolio Intelligence | Specify future non-production methods | No benchmark selection |
| Portfolio Benchmark Declaration | Portfolio Intelligence under frozen M42-WP5 | Consume exact declaration | No replacement or default |
| Portfolio-return methods | Portfolio Intelligence under frozen M43-WP6 | Consume independently confirmed results and dependencies after the M43 governance correction | No recomputation or premature binding |
| Portfolio Composition | Portfolio Intelligence under frozen M42-WP7 | Consume exact subject | No alternative snapshot |
| Ledger and accounting evidence | Ledger & Accounting | Consume authoritative evidence | No restatement |
| Benchmark observations and measures | Market Intelligence | Consume exact manifest-bound evidence | No construction or provider lookup |
| Risk-free observations and measures | Market Intelligence | Consume exact evidence after WP4 section 6.6 confirmation | No literal or caller override |
| Calendar and market-reference meaning | Market Intelligence | Consume exact versioned reference | No ambient calendar |
| Annualization-basis dependency | Separately governed owner required by frozen WP4 section 6.7 | Consume only after full closure | No local contract invention |
| Asset identity and classification | Asset Foundation | Consume exact references | No taxonomy redefinition |
| Provenance meaning and capture | Connectivity & Ingestion | Carry captured Provenance | No recapture or fabrication |
| Result relations and Portfolio measure lineage | Portfolio Intelligence under WP5 | Populate exact confirmed contract | No parallel result model |
| Attribution | Portfolio Intelligence under WP8 allocation | None | No WP8 anticipation |
| Runtime placement and cutover | Future M43-WP9 | Documentary handoff only | No module or call-site choice |
| Rendering | Experience Platform | Downstream consumer | Experience computes nothing |
| Evaluation and causal judgment | Trust & Evaluation | Independent downstream observer | No grading |
| Recommendations and actions | Decision Intelligence | Downstream consumer | No prescriptive semantics |
| Cross-portfolio aggregation | Wealth Intelligence | Excluded | No cross-portfolio state |

Every concern has one owner. An unresolved owner or dependency is a blocking
condition, not permission for WP7 to assume ownership.

---

## 7. Placement model

| Documentary concern | Singular normative home |
| --- | --- |
| Definition identity, Method Version, applicability grammar | Frozen WP2 specification |
| Subject and Input Manifest grammar | Frozen WP3 specifications |
| Calendar, benchmark alignment, risk-free, annualization, missing-data, numeric, precision, and rounding semantics | Independently confirmed WP4 normative specification |
| Result classification, sufficiency, lineage, Provenance, temporal claim, identity, and serialization | Independently confirmed WP5 normative specification |
| Core Portfolio-return dependencies | Independently confirmed WP6 normative method specification after M43 governance-correction closure |
| WP7 method meanings, operation order, method-specific applicability, and history requirements | Future WP7 risk and benchmark-relative method specification |
| Positive, boundary, and negative examples | Future WP7 documentary fixture corpus |
| Runtime location, compatibility, shadow validation, and cutover | Future WP9 implementation design |
| Confirmed new vocabulary, if any | Owning WP7 vocabulary gate plus synchronized Glossary entry |
| This constitutional planning allocation | `docs/implementation/M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md` |

No semantic rule may have two normative homes.

---

## 8. Method-family boundaries

### 8.1 Drawdown

The future specification must bind one exact Portfolio-return or
normalized-performance dependency from WP6 and close:

- peak and trough eligibility;
- measurement-window treatment;
- ordering and tie rules;
- recovery-state treatment;
- missing and non-success input handling;
- numeric model and rounding;
- valid-history requirements; and
- WP5 result classification.

WP7 must not recreate the underlying return or normalized series.

### 8.2 Volatility and downside deviation

The future specification must close:

- exact return dependency;
- sample eligibility;
- minimum observation count;
- dispersion convention;
- downside threshold authority;
- observation frequency;
- annualization dependency, where used;
- missing and duplicate observation treatment;
- precision and rounding; and
- sufficiency/result mapping.

No library statistical default may determine these choices.

### 8.3 Sharpe and Sortino

The future specification must bind:

- exact Portfolio-return dependency;
- exact governed risk-free evidence;
- exact alignment and transformation rules;
- exact volatility or downside-deviation dependency;
- exact annualization dependency, where required;
- zero-denominator behavior;
- minimum history; and
- fail-closed outcome rules.

A literal `0`, `2.5%`, environment value, caller value, or “current risk-free
rate” is prohibited.

### 8.4 Beta and correlation

The future specification must require:

- a non-`Explicitly None` Portfolio Benchmark Declaration;
- exact benchmark evidence corresponding to the declaration;
- exact Portfolio and benchmark return dependencies;
- explicit calendar and observation alignment;
- exact sample-pair eligibility;
- minimum paired observations;
- zero-variance handling;
- missing or asynchronous observation treatment; and
- exact numeric and result rules.

Request-selected or provider-selected benchmark symbols are invalid.

### 8.5 Alpha

The future specification must bind exact confirmed dependencies for:

- Portfolio return;
- benchmark return;
- beta;
- risk-free evidence;
- annualization basis, where applicable;
- aligned measurement window;
- exact operation order; and
- result classification.

Alpha remains blocked while any required risk-free or annualization coordinate
is unrepresentable.

### 8.6 Tracking error and information ratio

The future specification must bind:

- exact Portfolio and declared-benchmark return dependencies;
- exact aligned Portfolio-minus-benchmark return observations;
- minimum valid history;
- annualization dependency, where applicable;
- zero-tracking-error behavior;
- missing, sparse, and asynchronous observation behavior;
- precision and rounding; and
- exact WP5 outcome mapping.

Information ratio must fail closed when its denominator is zero or
insufficient under the confirmed method contract.

### 8.7 Benchmark-form applicability

| Benchmark Declaration form | WP7 planning disposition |
| --- | --- |
| `Explicitly None` | Benchmark-relative methods are not applicable; no fallback |
| `Single` | Potentially applicable only with exact matching governed evidence and complete alignment |
| `Composite` | Blocked unless exact governed construction, weights, identities, versions, and evidence are representable |
| `Category` | Blocked unless exact governed category-matching authority and evidence are representable |

WP7 cannot collapse `Composite` or `Category` into an arbitrary `Single`
benchmark.

### 8.8 Missing-benchmark boundary

The future specification must distinguish:

- an absent Portfolio Benchmark Declaration coordinate;
- `Explicitly None`, which is an affirmative declared choice;
- a `Single` declaration whose exact governed benchmark evidence is absent
  from the manifest;
- a `Single` declaration whose evidence is present but non-conforming; and
- unsupported `Composite` or `Category` evidence.

An absent declaration coordinate or absent/non-conforming required evidence
must fail closed under the independently confirmed WP5 result contract. WP7
must not infer a declaration, substitute a benchmark, consult a provider, or
reinterpret absence as `Explicitly None`.

---

## 9. No-default matrix

| Concern | Prohibited default | Only permitted closure |
| --- | --- | --- |
| Portfolio | Current Selection or workspace default | Exact M42 Portfolio Composition |
| Benchmark declaration coordinate | Inference from holdings, asset class, request, provider, or history | Exact M42 Portfolio Benchmark Declaration; absence fails closed |
| Benchmark evidence | Substitute index, alternate provider, nearest series, or omission | Exact governed evidence matching the declaration; absence/non-conformance fails closed |
| `Explicitly None` | Global or asset-class fallback | Not applicable |
| Risk-free input | `0`, `2.5%`, config, request, live provider answer | Exact WP4-confirmed manifest-bound Market evidence |
| Annualization | Hidden `252`, `365`, `365.25`, library frequency | Exact versioned dependency after separate closure |
| Calendar | Weekdays, exchange-name guess, dataframe calendar | Exact WP4-governed calendar binding |
| Observation alignment | Positional zip, automatic inner join, library default | Exact method-selected WP4 mode |
| Missing observation | Zero, forward-fill, backfill, alternate provider | Exact confirmed missing-data rule |
| Minimum sample | Library minimum, UI setting, arbitrary constant | Exact method-version requirement |
| Statistical convention | Library default | Exact immutable documentary method choice |
| Zero denominator | Infinity, zero, omission, exception convention | Exact WP5-conforming fail-closed rule |
| Currency | User preference or majority holding currency | Exact historical Portfolio Base Currency and governed FX evidence |
| Precision and rounding | Language or database default | Exact WP4 numeric rules |
| Input order | Database, provider, or request order | Canonical semantic order and tie-break |
| Dependency version | Latest, compatible range, silent upgrade | Exact immutable identity and version |

---

## 10. Documentary deliverables

After applicable gates close, WP7 shall produce:

1. `docs/implementation/M43_WP7_RISK_AND_BENCHMARK_RELATIVE_METHOD_SPECIFICATION.md`;
2. `docs/implementation/m43/fixtures/M43_WP7_POSITIVE_DOCUMENTARY_VECTORS.md`;
3. `docs/implementation/m43/fixtures/M43_WP7_NEGATIVE_DOCUMENTARY_VECTORS.md`;
4. a complete method/dependency/applicability matrix;
5. a benchmark-form applicability matrix;
6. a risk-free, calendar, and annualization dependency register;
7. a sufficiency, outcome, and degraded-state mapping;
8. a legacy-behavior disposition matrix;
9. a normative-row-to-vector coverage ledger;
10. `docs/implementation/M43_WP7_INDEPENDENT_CONSTITUTIONAL_AND_NUMERICAL_REVIEW.md`;
11. `docs/implementation/M43_WP7_REQUIRED_CORRECTIONS_RESPONSE.md`, if
    required; and
12. `docs/implementation/M43_WP7_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md`.

Every artifact must state that it is documentary, non-executable, and
non-production.

---

## 11. Documentary vector strategy

### 11.1 Positive and boundary coverage

The future corpus must cover at least:

- drawdown with multiple peaks and recoveries;
- equal-value peak ties;
- monotonic positive and negative histories;
- minimum valid volatility sample;
- below-minimum sample;
- zero variance;
- downside observations at and around the threshold;
- aligned Portfolio, benchmark, and risk-free histories;
- negative excess-quantity observations, using that phrase descriptively
  unless separately admitted;
- zero beta denominator;
- zero tracking error;
- short history;
- boundary and interior gaps;
- asynchronous Portfolio and benchmark calendars;
- negative Portfolio and benchmark returns;
- `Single` benchmark evidence with exact identity;
- absent Portfolio Benchmark Declaration coordinate, with a fail-closed
  result and no inference;
- `Single` declaration with absent governed benchmark evidence, with a
  fail-closed result and no substitution;
- `Single` declaration with non-conforming governed benchmark evidence, with
  a fail-closed result and no substitution;
- `Explicitly None`;
- unimplemented `Composite`;
- unimplemented `Category`;
- precision and rounding boundaries;
- exact dependency-version distinction; and
- deterministic input-order permutations.

### 11.2 Required negative coverage

The future corpus must directly reject:

- inference of a missing Portfolio Benchmark Declaration;
- reinterpretation of an absent declaration as `Explicitly None`;
- substitution or fallback when required benchmark evidence is absent or
  non-conforming;
- request-supplied benchmark substitution;
- provider-symbol identity;
- fallback from `Explicitly None`;
- arbitrary `Single` substitution for `Composite` or `Category`;
- hidden `2.5%`, zero, or caller-supplied risk-free values;
- hidden `252`, `365`, or library annualization;
- live provider retrieval;
- wall-clock window selection;
- automatic dataframe alignment;
- silent row dropping;
- forward-fill, backfill, or zero-fill;
- insufficient samples treated as success;
- zero denominator treated as a numeric value without authority;
- cross-portfolio inputs;
- mismatched Portfolio and benchmark windows;
- unversioned dependencies;
- recomputation of WP6 returns;
- reliance on a WP6 return before M43 governance-correction closure;
- artificial bytes presented as canonical;
- executable fixtures;
- production-method claims; and
- WP8 or WP9 concerns embedded in WP7.

### 11.3 Vector authority

Documentary vectors illustrate and test traceability to previously confirmed
normative rows. They do not create semantics.

While an inherited gate remains open, any illustrative material touching that
gate must be marked:

- `ARTIFICIAL`;
- `NON-EFFECTIVE`; and
- `NON-CONFORMANCE-ESTABLISHING`.

No expected value may be used to reverse-author a missing rule.

---

## 12. Traceability matrix

### 12.1 Method and deliverable allocation

| Frozen WP7 allocation | Planned normative home | Required evidence | Entry gate |
| --- | --- | --- | --- |
| Drawdown | WP7 method specification | Definition, Method Version, dependency, history, operation-order, result, and vectors | M43 correction and WP4–WP6 binding sources confirmed |
| Volatility | WP7 method specification | Sample, dispersion, annualization, numeric, sufficiency, and vectors | Annualization closure if annualized |
| Downside deviation | WP7 method specification | Threshold, sample, annualization, result, and vectors | WP4 and annualization gates |
| Sharpe | WP7 method specification | Return, risk-free, dispersion, annualization, applicability, and vectors | Risk-free and annualization gates |
| Sortino | WP7 method specification | Return, risk-free, downside, annualization, applicability, and vectors | Risk-free and annualization gates |
| Beta | WP7 method specification | Declared benchmark, paired observations, variance boundary, and vectors | Benchmark evidence and WP6 gates |
| Correlation | WP7 method specification | Declared benchmark, paired sample, zero variance, and vectors | Benchmark evidence and WP6 gates |
| Alpha | WP7 method specification | Return, benchmark, beta, risk-free, annualization, and vectors | All risk-free and annualization gates |
| Tracking error | WP7 method specification | Aligned Portfolio-minus-benchmark return dependency, sample, annualization, zero boundary, and vectors | Benchmark, WP6, and annualization gates |
| Information ratio | WP7 method specification | Portfolio-minus-benchmark return quantity, tracking error, zero denominator, and vectors | Benchmark, WP6, and annualization gates |
| Benchmark applicability | WP7 applicability matrix | `Single`, `Explicitly None`, `Composite`, `Category`, and missing-coordinate cases | M42-WP5 exact consumption |
| Sufficiency/degraded behavior | WP5 contract plus WP7 mappings | Positive, boundary, and negative mappings | WP5 normative specification confirmed |
| Numerical vectors | WP7 fixture corpus | Expected documentary outcomes and coverage ledger | Normative rows confirmed first |
| WP7-local vocabulary | Vocabulary gate | Disposition, owner, home, collision review, confirmation | Before first reliance |
| WP9 handoff | WP7 specification handoff section | Exact confirmed method identities and dependencies | WP7 corpus otherwise complete |

### 12.2 Frozen validation allocation

| Frozen M43 section 9 WP7 validation criterion | Planned normative home | Required evidence | Entry gate |
| --- | --- | --- | --- |
| Zero variance | Applicable volatility, beta, correlation, Sharpe, Sortino, or ratio rows in the WP7 method specification | Boundary vectors proving exact denominator/variance classification and no library fallback | WP4, WP5, WP6, and applicable annualization/risk-free gates closed |
| Insufficient sample | Per-method history and sufficiency matrix | Minimum, below-minimum, sparse, and non-success vectors | WP4 and WP5 normative specifications confirmed |
| Missing benchmark | Benchmark applicability and missing-benchmark sections of the WP7 method specification | Absent declaration coordinate; `Single` with absent evidence; `Single` with non-conforming evidence; direct no-inference/no-substitution negatives | M42-WP5, WP3, WP4, and WP5 gates closed |
| `Explicitly None` | Benchmark-form applicability matrix | Non-applicability vector distinct from missing-coordinate behavior and direct no-fallback negative | M42-WP5 exact consumption and WP5 result contract confirmed |
| Unimplemented `Composite`/`Category` evidence | Benchmark-form applicability matrix | Separate blocked/unavailable cases and rejection of arbitrary `Single` substitution | M42-WP5 and benchmark-form evidence gate |
| Asynchronous calendars | WP7 alignment requirements under WP4 | Paired-observation boundary cases, ordering evidence, and rejection of positional or automatic joins | WP4 normative specification confirmed |
| Zero tracking error | Tracking-error and information-ratio rows | Exact zero-denominator boundary, classification, and no infinity/zero/default vector | WP4, WP5, WP6, and annualization gates closed as applicable |
| Negative-return vectors | Each applicable WP7 method and fixture corpus | Portfolio-only, benchmark-only, both-negative, negative difference, and boundary cases under exact numeric semantics | WP4–WP6 binding sources confirmed |

### 12.3 Gate and ownership traceability

| Inherited constraint | Planned evidence |
| --- | --- |
| Frozen WP1 section 7.4 M43 governance correction | Exact independently confirmed correction citation before any WP6 dependency binding |
| Frozen WP1 section 7.3 ownership split | Ownership rows preserving Portfolio Intelligence performance meaning and Ledger & Accounting input semantics |
| WP3/M42-WP7 canonical-byte gap | Exact closure citation before any effective Subject, Manifest, result-byte, or hash claim |
| WP4 risk-free gate | Exact independently confirmed WP4 section 6.6 normative disposition and evidence binding |
| WP4 annualization gate | Exact separately governed dependency contract and WP2/WP3 closure |
| WP5 result gate | Exact independently confirmed result-contract path and cited rows |
| WP6 completion gate | Exact independently confirmed WP6 method-specification path, identities, and dependency results |

---

## 13. Dependency-safe documentary implementation sequence

“Implementation” below means production of documentary specifications and
static documentary vectors only.

1. **Freeze and confirm this plan.** Final Independent Constitutional
   Confirmation is `CONFIRMED` at RC2.
2. **Preserve the frozen allocation.** Reject the requested WP7
   core-performance relabeling and make no change to WP6.
3. **Verify frozen prerequisites.** Confirm WP1–WP6 artifacts remain
   unchanged.
4. **Preserve the M43 governance-correction gate.** Require the independently
   confirmed correction demanded by frozen WP1 section 7.4 before any WP6
   method dependency is treated as authorized.
5. **Preserve the WP3/M42-WP7 representability gate.** Make no effective
   Subject, Manifest, result-byte, or hash claim before separate closure.
6. **Require the WP4 normative specification.** Bind no numerical convention
   to a planning proposition.
7. **Require the WP5 normative result specification.** Bind no result
   classification or representation to a planning proposition.
8. **Require the confirmed WP6 normative corpus.** Bind no Portfolio-return
   dependency before the M43 correction and WP6 method-specification reviews
   are independently confirmed.
9. **Inventory all closure evidence.** Record exact section and repository
   path citations for every inherited gate.
10. **Run the WP7 vocabulary-sufficiency gate.**
11. **Build ownership, placement, dependency, method, and applicability
    matrices.**
12. **Partition methods by gate.** One blocked method must not weaken another
    method's requirements.
13. **Specify drawdown** after its exact WP6 dependency is available.
14. **Specify non-annualized statistical meanings** only where every required
    dependency is representable.
15. **Specify benchmark-form applicability,** including missing declaration,
    missing evidence, `Explicitly None`, `Single`, `Composite`, and `Category`.
16. **Specify beta and correlation** only after exact paired Portfolio and
    benchmark evidence is representable.
17. **Specify annualized methods** only after annualization-dependency closure.
18. **Specify Sharpe, Sortino, and alpha** only after exact risk-free evidence
    and annualization bindings are confirmed.
19. **Specify information ratio** only after its prerequisite dependencies are
    confirmed.
20. **Complete method-specific sufficiency and WP5 result mappings.**
21. **Characterize legacy behavior** without granting precedent or choosing
    runtime action.
22. **Derive positive and boundary documentary vectors** from confirmed
    normative rows.
23. **Derive negative vectors** for every prohibited default, missing
    benchmark path, and ownership violation.
24. **Complete traceability** for every frozen method, validation criterion,
    deliverable, gate, and rejection.
25. **Perform independent constitutional, numerical, dependency, fixture, and
    boundary reviews.**
26. **Correct only WP7 artifacts.** Route upstream defects to their owners.
27. **Confirm and freeze WP7** only when every allocated method is complete,
    every applicable gate is closed, unresolved findings are `NONE`, and all
    authority remains documentary and non-production.

WP7 cannot be declared complete by omitting a frozen allocated method or
validation criterion. If an external dependency remains unresolved, WP7
remains incomplete and blocked.

---

## 14. Independent review strategy

### 14.1 Constitutional review

An independent reviewer must verify:

- WP7 retains the frozen risk and benchmark-relative allocation;
- no WP6 concern is duplicated or relocated;
- the frozen WP1 sections 7.3–7.4 ownership split and governance block are
  preserved;
- all inherited gates are preserved with exact citations;
- every concern has one owner;
- every semantic rule has one normative home;
- no WP8 or WP9 concern is anticipated;
- no new noun bypasses the vocabulary gate;
- all authority declarations are complete; and
- no executable, runtime, provider, persistence, API, UI, or production
  authority appears.

### 14.2 Numerical review

An independent numerical reviewer must verify:

- every statistical convention is explicit;
- no library behavior supplies semantics;
- each method uses exact authorized WP6 return dependencies;
- every applicable risk-free input is exact governed evidence;
- every annualization dependency is exact and version-bound;
- zero variance and zero denominator behavior is closed;
- minimum-history and sample rules are complete;
- asynchronous calendars and missing observations fail or align only as
  specified;
- operation order, precision, and rounding are deterministic; and
- expected documentary values are reproducible without executable
  assumptions.

### 14.3 Benchmark and dependency review

An independent reviewer must verify:

- every benchmark-relative method consumes the exact M42 declaration;
- a missing declaration is distinct from `Explicitly None`;
- missing or non-conforming benchmark evidence fails closed;
- `Explicitly None` causes non-applicability without fallback;
- `Single` uses matching governed evidence;
- `Composite` and `Category` remain unavailable without exact governed
  support;
- provider and request symbols never become canonical identity;
- dependency closure conforms to WP2 and WP3;
- no WP6 dependency is used before M43 governance-correction closure; and
- no missing dependency is manufactured inside WP7.

### 14.4 Fixture and boundary review

An independent reviewer must verify:

- vectors derive from normative rows;
- every normative row has positive or boundary coverage;
- all eight frozen M43 section 9 validation criteria have direct coverage;
- every prohibited interpretation has direct negative coverage;
- artificial material is visibly non-effective;
- no fixture is executable;
- no legacy behavior becomes precedent;
- no runtime disposition is selected; and
- Experience computes nothing.

### 14.5 Independence

Authors of normative method rows must not be the sole reviewers of their
numerical expectations. Corrections require renewed review. Confirmation
requires unresolved findings `NONE`.

---

## 15. Acceptance criteria

This planning artifact is acceptable only if:

1. it corrects the requested WP7/WP6 allocation conflict without modifying
   either frozen allocation;
2. it assigns all and only frozen WP7 concerns;
3. it preserves the frozen WP1 section 7.3 ownership split;
4. it preserves the frozen WP1 section 7.4 M43 governance-correction block;
5. it preserves exact ownership boundaries;
6. it assigns one normative home per concern;
7. it occupies its declared repository path;
8. it declares every authority class;
9. it remains documentary only;
10. it defines no formula, algorithm, or executable semantic;
11. it grants no production authority;
12. it preserves every WP2–WP6 dependency;
13. it identifies every inherited representability and
    specification-existence gate with exact citations;
14. it preserves exact M42 Benchmark Declaration authority;
15. it distinguishes a missing benchmark from `Explicitly None`;
16. it rejects benchmark fallback and request/provider-symbol substitution;
17. it rejects hidden risk-free and annualization defaults;
18. it defines documentary deliverables and placements;
19. it allocates all eight frozen validation criteria;
20. it defines positive, boundary, and negative validation obligations;
21. it provides complete traceability;
22. it provides a dependency-safe sequence;
23. it defines independent review obligations;
24. it prohibits redesign of frozen work packages; and
25. it makes no capability-completion claim.

### 15.1 Planning validation matrix

| Required verification | Result | Evidence |
| --- | --- | --- |
| Constitutional allocation | `PASS` | Sections 0, 4, and 12 retain frozen WP7 and reject WP6 reassignment |
| Ownership singularity | `PASS` | Section 6 assigns one owner per concern and preserves the WP1 section 7.3 split |
| Placement singularity | `PASS` | Section 7 assigns one normative home, including this artifact's exact path |
| Authority declarations | `PASS` | Header and section 2.2 include governance-correction and frozen-amendment authority `NONE` |
| Dependency integrity | `PASS` | Section 3 preserves WP2–WP6, M39–M42, Portfolio Calculation Rules, and ADR-001 through ADR-005 |
| External gates complete | `PASS` | Section 3.2 records the M43 governance correction and every inherited specification, representability, risk-free, annualization, benchmark-form, and vocabulary gate |
| Documentary-only scope | `PASS` | Header and sections 4, 10, 13, and 17 |
| No executable semantics | `PASS` | No formula, algorithm, test, executable vector, or runtime flow is defined |
| No production authority | `PASS` | All production and implementation authorities are `NONE` |
| No redesign of frozen work packages | `PASS` | Sections 0, 3, 4.2, and 18 |
| Traceability | `PASS` | Section 12 maps every frozen method, all eight frozen validation criteria, every inherited gate, and the WP9 handoff |
| Validation strategy | `PASS` | Sections 11, 12.2, and 14 include distinct missing-benchmark coverage |
| Implementation sequence | `PASS` | Section 13 preserves the M43 correction before WP6 and WP7 dependency binding |
| Vocabulary closure | `PASS` | Section 5 records disposition, owner, and permitted use and prevents descriptive quantity phrases from implicit admission |
| Markdown and citation integrity | `PASS` | ATX headings, pipe-delimited tables, and exact gate anchors are present |

### 15.2 Future WP7 corpus completion criteria

The future WP7 corpus is complete only when:

1. the M43 governance correction required by frozen WP1 section 7.4 is
   independently confirmed;
2. every other inherited gate applicable to an allocated method is closed;
3. the WP4 and WP5 normative specifications exist and are independently
   confirmed;
4. the WP6 normative core-performance dependency corpus exists, was
   authorized after the M43 correction, and is independently confirmed;
5. the WP3/M42-WP7 representability gap is closed before canonical-byte
   claims;
6. every frozen WP7 method has one exact Definition and Method Version;
7. every method has exact inputs, dependencies, applicability, valid-history,
   numerical, and result rules;
8. every benchmark-relative method consumes the exact M42 declaration;
9. missing declaration, missing evidence, `Explicitly None`, `Single`,
   `Composite`, and `Category` behavior is explicit and non-substitutable;
10. every required risk-free input is exact governed evidence;
11. every required annualization basis is an exact versioned dependency;
12. no hidden convention or caller override remains;
13. all eight frozen validation criteria have documentary coverage;
14. all normative rows are traceable to vectors;
15. independent reviews are confirmed;
16. unresolved findings are `NONE`;
17. no executable artifact exists;
18. no production method is admitted; and
19. no roadmap capability is declared deployed or complete.

---

## 16. Repository effect

### 16.1 Planning artifact authorized now

This work item authorizes only the documentary planning artifact:

- `docs/implementation/M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md`.

Its review chain may add:

- `docs/implementation/M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN_INDEPENDENT_REVIEW.md`;
- `docs/implementation/M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN_REQUIRED_CORRECTIONS_RESPONSE.md`,
  if required; and
- `docs/implementation/M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN_INDEPENDENT_CONFIRMATION.md`.

### 16.2 Gate-conditional future artifacts

Only after applicable gates close may a separately authorized documentary
execution add the artifacts listed in section 10.

### 16.3 Prohibited repository effect

WP7 must not modify:

- frozen M43 Architecture;
- frozen M43-WP1 through WP6 artifacts;
- any M1–M42 frozen artifact;
- production source or configuration;
- executable tests or fixtures;
- schemas or migrations;
- APIs or UI;
- providers, schedulers, caches, or observability;
- roadmap capability status; or
- WP8 or WP9 artifacts.

`docs/GLOSSARY.md` may change only through a confirmed WP7-local vocabulary
admission or rename.

---

## 17. Completion report requirements

The eventual WP7 completion report must state:

1. exact documentary artifacts produced;
2. exact method coverage;
3. exact M43 governance-correction evidence;
4. exact dependency and other gate-closure evidence;
5. exact vocabulary disposition;
6. validation and review performed;
7. coverage of all eight frozen validation criteria;
8. benchmark-form and missing-benchmark coverage;
9. risk-free and annualization dependency closure;
10. unresolved findings, which must be `NONE`;
11. confirmation that frozen M43 Architecture and WP1–WP6 remain unchanged;
12. confirmation that no WP6, WP8, or WP9 concern was absorbed;
13. confirmation that no constitutional, governance-correction, frozen-
    amendment, runtime, executable, persistence, API, UI, provider, or
    production authority expanded; and
14. confirmation that no capability was declared deployed or complete.

If any required gate remains open, the report must state:

> `M43-WP7 INCOMPLETE — BLOCKED`

It must identify the exact gate and make no completion claim.

---

## 18. Final constitutional boundary

M43-WP7 is the future non-production documentary method-specification package
for drawdown, volatility, downside deviation, Sharpe, Sortino, beta,
correlation, alpha, tracking error, information ratio, and their
declared-benchmark applicability, dependency, sufficiency, degraded-state, and
numerical-validation obligations.

Core Performance and Rolling Method Specifications remain solely and
permanently allocated to frozen M43-WP6.

This plan establishes WP7's documentary scope, ownership, placement,
dependencies, inherited gates, deliverables, validation, traceability,
sequence, and acceptance criteria. It does not define a formula, begin
normative method work, close an external gate, perform the M43 governance
correction, create executable semantics, choose runtime placement, admit a
production method, amend a frozen artifact, or redesign any frozen work
package.
