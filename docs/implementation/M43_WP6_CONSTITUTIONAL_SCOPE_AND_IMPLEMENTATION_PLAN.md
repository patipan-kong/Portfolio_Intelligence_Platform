# M43-WP6 — Constitutional Scope and Implementation Plan

Milestone: M43 — Portfolio Analytics Contract Foundation
Work package: M43-WP6 — Core Performance and Rolling Method Specifications
Artifact class: Documentary constitutional scope and implementation plan
Revision: RC1 — independent-review corrections applied
Proposed status: READY FOR INDEPENDENT CONSTITUTIONAL REVIEW
WP6 method-work status: BLOCKED PENDING SEPARATELY GOVERNED CORRECTIONS
Runtime authority: NONE
Source-code authority: NONE
Persistence authority: NONE
API authority: NONE
UI authority: NONE
Provider authority: NONE
Implementation authority: NONE
Production-method authority: NONE
Executable-validation authority: NONE

This artifact plans a future documentary WP6 corpus. It does not define a
formula, activate a method, satisfy a method gate, or release any standing
governance block. It becomes frozen only through the normal independent review,
correction, and confirmation sequence.

---

## 0. Executive determination

Frozen M43 Architecture section 9 allocates exactly one method family to WP6:
core performance and rolling methods. The allocation consists of:

1. “chaining the Ledger-owned canonical period return”;
2. cumulative time-weighted return;
3. annualized return;
4. rolling return;
5. normalized performance series; and
6. valid-history and partial-window requirements.

Item 1 reproduces the frozen architecture's wording verbatim. Its
“Ledger-owned” qualifier is precisely what the pending M43 governance
correction must reconcile with frozen WP1 section 7.3, which separates
Portfolio-performance measure meaning from Ledger & Accounting-owned
accounting semantics. WP6 adopts no corrected reading in advance and may not
define a second period-return rule.

WP6 must eventually express those concerns through non-production Portfolio
Measure Definition and Portfolio Method Version specifications, a dependency
map to canonical period returns, formula and applicability matrices,
documentary golden vectors, and a legacy-behavior disposition.

That eventual work is not presently authorized to begin. Frozen WP1 section
7.4 records:

> `M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6`

The block follows from WP1's confirmed decomposition of the phrase “canonical
period-return rule” into two singular concerns:

- Portfolio Intelligence owns Portfolio-performance measure meaning; and
- Ledger & Accounting retains the accounting semantics that determine what
  enters the period return.

Frozen M43 made WP6 conditional on WP1's disposition and requires correction
when that disposition differs from the architecture's tested candidate.
Neither this plan nor WP6 may perform, presume, or bypass that correction.

Frozen WP4 section 6.7 also records an unresolved representability gap for the
annualization-basis dependency whose authority class remains a frozen WP4
section 6.7 proof obligation. Until separate authority supplies every
coordinate required by frozen WP2 and WP3, annualized-return method work must
remain fail-closed. Artificial documentary examples cannot establish
dependency conformance or activate an annualized method.

Frozen WP3 Portfolio Measure Subject Contract Specification section 7.1 and
frozen WP3 Portfolio Analytics Input Manifest Contract Specification sections
6.3 and 10.3 also record that
M42-WP7 section 5 supplies no exact Portfolio Composition byte representation.
No valid concrete Portfolio Measure Subject or Portfolio Analytics Input
Manifest byte sequence can be emitted until that gap is separately closed.

Accordingly, this plan completes the constitutional allocation of WP6 while
preserving every external gate. It plans later documentary method work
conditionally and grants no runtime, source, production, or executable
authority.

---

## 1. Constitutional objective

The constitutional objective of WP6 is to make every core Portfolio
performance and rolling output deterministically specifiable under exactly one
non-production Portfolio Method Version, using:

- one exact frozen WP2 Definition and Method Version contract;
- one exact frozen WP3 Portfolio Measure Subject and closed Input Manifest,
  only after the frozen WP3 Portfolio Measure Subject Contract Specification
  section 7.1 and frozen WP3 Portfolio Analytics Input Manifest Contract
  Specification sections 6.3 and 10.3 Portfolio Composition canonical-byte
  representability gap is separately closed;
- the exact numerical and boundary semantics from the independently confirmed
  WP4 normative specification required by frozen WP4;
- one exact result, sufficiency, outcome, degradation, lineage,
  Provenance-carriage, identity, and serialization contract from the
  independently confirmed WP5 normative specification required by frozen WP5;
  and
- the exact period-return dependency permitted by the corrected M43
  governance disposition.

The eventual documentary corpus must enable two independent readers to identify
the same method, required inputs, applicability, operation order, result
meaning, and expected documentary outcome without choosing a runtime component,
provider, storage surface, library, or ambient default.

This objective does not deploy Rolling Analytics, change accounting, or admit a
production method.

---

## 2. Governing authority

### 2.1 Authority order

WP6 is governed, in descending order, by:

1. Platform Architecture Laws 1–15;
2. the frozen M43 Architecture and Implementation Plan;
3. frozen M43-WP1 through M43-WP5 and their independent confirmations;
4. the frozen Portfolio Calculation Rules and ADR-001 through ADR-004;
5. the exact upstream M34 and M39–M42 authorities cited by frozen M43 and
   frozen WP1–WP5; and
6. this plan, only after independent confirmation and only within its
   documentary planning authority.

If authorities cannot be reconciled without changing a frozen artifact, WP6
fails closed and records the conflict for the owning governance process. WP6
does not resolve the conflict by interpretation, default, local vocabulary, or
formula invention.

### 2.2 Authority declarations

| Authority class | WP6 declaration |
| --- | --- |
| Constitutional allocation | Frozen M43 section 9 only |
| Documentary planning | Authorized by this work item |
| Later documentary method specification | Conditional on all applicable external gates |
| Formula specification | Conditional, non-production, and limited to the exact WP6 allocation |
| Runtime behavior | `NONE` |
| Source code | `NONE` |
| Persistence/schema/migration | `NONE` |
| API/transport | `NONE` |
| UI/presentation | `NONE` |
| Provider integration or selection | `NONE` |
| Production method | `NONE` |
| Executable fixture/test/harness | `NONE` |
| Governance correction | `NONE` |
| Frozen-artifact amendment | `NONE` |
| Future-WP design | `NONE` |

No statement in this plan may be read as indirect authority for a class marked
`NONE`.

---

## 3. Dependency model

### 3.1 Hard dependencies

| Dependency | Sole authority consumed | Exact WP6 reliance | WP6 prohibition |
| --- | --- | --- | --- |
| WP1 vocabulary and ownership | Frozen WP1 | Confirmed Portfolio nouns, Portfolio Intelligence performance meaning, split period-return ownership, legacy inventory, and active WP6 block | No noun reopening, ownership merger, or block release |
| WP2 Definition, Method Version, applicability, and dependencies | Frozen WP2 | Exact immutable method identity and declared dependency closure | No alternate identity, registry, dependency kind, or applicability operator |
| WP3 Subject and Input Manifest | Frozen WP3 | One exact Portfolio Composition subject and complete closed evidence/dependency set only after every required canonical byte representation exists | No live lookup, side input, manifest repair, new entry category, or premature concrete binding |
| WP3 Portfolio Composition canonical-byte representability | Frozen WP3 Portfolio Measure Subject Contract Specification section 7.1 and frozen WP3 Portfolio Analytics Input Manifest Contract Specification sections 6.3 and 10.3; M42-WP7 section 5 | Open representability gap: a concrete Subject and Manifest cannot presently be formed or emitted | No invented nested encoding, effective Subject/Manifest binding, or canonical-byte vector |
| WP4 numerical semantics | `docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`, after it exists and is independently confirmed as required by frozen WP4 | Window, time, currency, FX, calendar, alignment, missing-data, partial-window, numeric, precision, rounding, and dependency-arithmetic grammar | No binding to the WP4 plan as if it contained the required normative rows; no alternate convention or ambient numerical choice |
| WP4 annualization disposition | Frozen WP4 section 6.7 | Open representability gap and fail-closed consequence | No literal `252`/`365`, caller override, invented dependency contract, or effective annualized method |
| WP5 result contract | `docs/implementation/M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md`, after it exists and is independently confirmed as required by frozen WP5 | Exact result classification, value presence, lineage, temporal claim, Provenance carriage, identity, canonical bytes, and reasons | No binding to the WP5 plan as if it contained the required normative rows; no parallel result envelope, outcome, degradation, or serialization |
| Period-return accounting semantics | Ledger & Accounting under Portfolio Calculation Rules sections 1–9 | Exact accounting-owned meaning of inputs to period return | No NAV, cash-flow, capital-event, cost-basis, replay, or snapshot arithmetic |
| Period-return consumption rule | Portfolio Calculation Rules section 10, subject to corrected M43 governance | Semantic dependency on the one canonical period-return source | No second period-return formula or source call-site selection |
| ADR-001 through ADR-004 | Frozen ADRs | Source-of-truth and single-rule constraints | No custody-to-ownership inference |

M41 method and result contracts may be consulted only as mechanical precedent.
Market Intelligence-owned vocabulary, field choices, formulas, identities,
outcomes, and methods do not become Portfolio Intelligence contracts.

### 3.2 Entry gates

No normative WP6 method specification, formula matrix, applicability matrix, or
effective golden vector may be created until:

1. the WP1 section 7.4 standing block has been closed by the separately
   authorized, independently reviewed M43 governance-correction workflow;
2. the correction records the exact singular ownership and semantic boundary
   upon which WP6 may rely;
3. the correction leaves one, and only one, canonical period-return rule and
   explicitly preserves Ledger & Accounting-owned accounting semantics;
4. the WP4 normative semantics specification exists, is independently
   confirmed, and is cited by its exact repository path before any WP6
   normative row binds a WP4 numerical convention;
5. the WP5 normative result contract specification exists, is independently
   confirmed, and is cited by its exact repository path before any WP6
   normative row binds a WP5 result classification;
6. all frozen WP2–WP5 prerequisites remain effective and unchanged; and
7. the proposed WP6 corpus passes the downstream vocabulary gate before
   relying on any WP6-local noun.

The two required binding sources named by frozen WP4 and frozen WP5 are:

- `docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`;
  and
- `docs/implementation/M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md`.

Neither specification is present in the current repository corpus. If either
is independently confirmed under a different path, WP6 must cite that exact
path instead. A plan artifact, expected filename, or unchanged prerequisite is
not a substitute for an existing independently confirmed specification.

Effective Subject/Manifest binding and every canonical-byte vector have the
additional gate that the frozen WP3 Portfolio Measure Subject Contract
Specification section 7.1 and frozen WP3 Portfolio Analytics Input Manifest
Contract Specification sections 6.3 and 10.3 Portfolio Composition
canonical-byte representability gap must be closed under separate authority.
Closure must supply the exact M42-WP7
Portfolio Composition canonical bytes required by the frozen WP3 contracts.
This gate blocks concrete Subject/Manifest formation, emission, binding, and
canonical-byte conformance claims. It does not block this planning artifact,
vocabulary review, ownership/dependency analysis, or expressly artificial,
non-effective documentary framing. WP6 cannot invent the missing nested
encoding.

Annualized-return specification has the additional gate that the WP4 section
6.7 representability gap must be closed under separate authority. Closure must
provide the exact existing governed contract kind, identity, version, value
representation, WP2 declaration and closure, and matching WP3 entry required by
the frozen contracts. WP6 cannot manufacture any missing coordinate.

Gate failure blocks only the affected work. It never creates permission to
weaken a dependency, use a default, or absorb another owner's concern.

### 3.3 Dependency flow

```text
separate M43 governance correction
                 |
                 v
WP1 vocabulary and singular ownership boundary
                 +
WP2 Definition / Method Version / applicability / dependency closure
                 +
WP3 exact Subject / closed Input Manifest
after the M42-WP7 Composition-byte gap closes
                 +
independently confirmed WP4 normative semantics specification
and its open-gate dispositions
                 +
independently confirmed WP5 normative result contract
                 |
                 v
WP6 non-production core-performance and rolling specifications
                 |
                 v
WP7 and WP8 consume only the frozen WP6 handoff;
WP9 alone may later design source-level realization
```

No arrow transfers ownership.

---

## 4. Constitutional scope

### 4.1 In scope after the applicable gates close

WP6 owns the documentary specification of:

1. the exact Portfolio-performance meaning of each allocated output;
2. one non-production Portfolio Measure Definition and at least one exact
   non-production Portfolio Method Version for each allocated method;
3. method applicability under the frozen WP2 operator;
4. exact declared dependencies under frozen WP2 and their matching frozen WP3
   placement;
5. semantic chaining of exact canonical period returns without defining the
   period-return accounting rule;
6. cumulative time-weighted-return method semantics;
7. annualized-return method semantics, only after the annualization dependency
   is representable;
8. rolling-return method semantics;
9. normalized-performance-series method semantics;
10. valid-history requirements for every allocated method;
11. exact allowed or prohibited partial-window behavior selected from frozen
    WP4 semantics only after the required WP4 normative specification is
    independently confirmed;
12. exact method-specific choices from the closed numerical grammar in that
    independently confirmed WP4 normative specification;
13. formula and operation-order specifications only where frozen M43 assigns
    them to WP6;
14. deterministic mappings into the result classifications and value-presence
    rules in the independently confirmed WP5 normative specification;
15. documentary positive, negative, boundary, permutation, and reconciliation
    vectors;
16. legacy behavior disposition for the core-performance and rolling family;
    and
17. an exact documentary handoff to WP7, WP8, and WP9 without choosing a
    runtime call site or admitting production behavior.

The plan itself specifies none of the formulas in items 5–9. It allocates those
later documentary decisions to their one normative home.

### 4.2 Explicit exclusions

WP6 excludes:

- releasing or performing the WP1 section 7.4 governance correction;
- amending frozen M43 or WP1–WP5;
- redefining or merging the split period-return ownership boundary;
- defining a second period-return formula;
- changing accounting arithmetic, NAV, cash-flow treatment, capital-event
  stripping, imported-asset treatment, quantity correction, cost basis,
  replay, snapshots, or open accounting questions;
- choosing a source module, function, package, adapter, registry, cache,
  database, call site, or implementation language;
- executable contracts, methods, fixtures, tests, harnesses, or calculations;
- runtime, persistence, migration, API, transport, UI, or provider behavior;
- provider identifiers, live provider answers, wall-clock time, Current
  Selection, or workspace defaults;
- benchmark-relative, risk, drawdown, volatility, ratio, alpha, beta,
  correlation, tracking-error, or information-ratio methods allocated to WP7;
- position contribution, sector contribution, attribution timeline,
  classification/grouping, or residual methods allocated to WP8;
- runtime realization, compatibility design, shadow execution, cutover,
  rollout, rollback, observability, or deprecation design allocated to WP9;
- BHB or benchmark-relative attribution;
- recommendation, optimization, ranking, suitability, evaluation, causal,
  regime, or human-versus-AI semantics;
- production-method admission;
- a claim that any roadmap capability is complete; and
- any new constitutional noun without the downstream vocabulary workflow.

### 4.3 Essential boundary

WP6 owns method-family meaning. It does not own upstream evidence meaning,
accounting semantics, shared contracts, or downstream realization.

```text
Ledger & Accounting:
what enters the canonical period return
                    |
                    v
Portfolio Intelligence / WP6:
how exact period returns become one allocated performance or rolling measure
                    |
                    v
WP5 result contract:
how the method result is classified, identified, serialized, and carried
                    |
                    v
WP9:
where a later authorized implementation would live and how it would cut over
```

Custody, citation, carriage, or consumption never transfers semantic ownership.

---

## 5. Vocabulary gate

### 5.1 Closed inherited vocabulary

WP6 must use the frozen WP1 dispositions unchanged:

| Term | Disposition | Owner / grammar authority | WP6 use |
| --- | --- | --- | --- |
| Portfolio Measure | `ADMIT` | Portfolio Intelligence | Exact inherited meaning |
| Portfolio Measure Definition | `ADMIT` | Portfolio Intelligence | Exact WP2 contract |
| Portfolio Method Version | `ADMIT` | Portfolio Intelligence | Exact WP2 contract |
| Portfolio Measure Subject | `ADMIT` | Portfolio Intelligence | Exact WP3 contract |
| Portfolio Analytics Input Manifest | `ADMIT` | Portfolio Intelligence | Exact WP3 contract |
| Portfolio Measurement Window | `ADMIT` | Portfolio Intelligence | Exact semantics only from the independently confirmed WP4 normative specification |
| Portfolio Input Sufficiency | `ADMIT` | Portfolio Intelligence | Exact contract only from the independently confirmed WP5 normative specification |
| Portfolio Measure Result | `ADMIT` | Portfolio Intelligence | Exact contract only from the independently confirmed WP5 normative specification |
| Portfolio Computation Outcome | `ADMIT` | Portfolio Intelligence | Exact contract only from the independently confirmed WP5 normative specification |
| Portfolio Deterministic Calculation | `ADMIT` | Portfolio Intelligence | Exact contract only from the independently confirmed WP5 normative specification |
| Portfolio Degraded State | `REUSE` | M34-D-0005 producing-domain grammar | Use `Degraded State`; never admit the prefixed noun |

`UNAVAILABLE` remains a Degraded State and never becomes a Portfolio
Computation Outcome.

### 5.2 WP6-local vocabulary rule

The architecture's phrases “cumulative time-weighted return,” “annualized
return,” “rolling return,” “normalized performance series,” “valid history,”
and “partial window” are allocation labels. This plan does not promote them
into new constitutional nouns or contract types.

Before a normative WP6 corpus relies on any new noun, the owning WP6 workflow
must:

1. prove that inherited vocabulary and ordinary structural language are
   insufficient;
2. record exactly one `ADMIT`, `REUSE`, `RENAME`, or `REJECT` disposition;
3. identify one semantic owner and one normative home;
4. perform collision and overlap analysis across the repository;
5. receive independent vocabulary review and confirmation; and
6. synchronize any confirmed admission or rename with `docs/GLOSSARY.md` in
   the same authorized change.

No later vocabulary decision may reopen WP1 or another frozen package. A
candidate term cannot appear in a Definition, Method Version, fixture schema,
or acceptance criterion before confirmation.

Current planning conclusion: no new constitutional noun is required by this
planning artifact, and no Glossary change is authorized.

---

## 6. Ownership model

| Semantic concern | Sole semantic owner | Normative authority/home | Exact WP6 authority | Non-owner boundary |
| --- | --- | --- | --- | --- |
| Portfolio-performance measure meaning | Portfolio Intelligence | Frozen architecture, WP1, and later WP6 method specification | Specify allocated method meaning | Ledger evidence custody does not transfer this meaning |
| Accounting semantics determining period return | Ledger & Accounting | Portfolio Calculation Rules sections 1–9 | Consume exactly | WP6 may not reinterpret or restate them normatively |
| Canonical period-return dependency boundary | As fixed by the required M43 correction while preserving the WP1 split | Separate correction record plus frozen authorities | Bind after correction only | WP6 cannot author the correction |
| Definition, Method Version, applicability, dependency grammar | Portfolio Intelligence | Frozen WP2 | Instantiate exact contracts | WP6 cannot alter the grammar |
| Subject and Manifest identity/evidence closure | Portfolio Intelligence | Frozen WP3 | Bind exact instances only after the WP3/M42-WP7 canonical-byte gap closes | WP6 cannot add coordinates, entries, or nested encoding |
| Portfolio Composition canonical-byte representation | Portfolio Intelligence under frozen M42-WP7 | Separate governance outside WP6, then exact consumption through frozen WP3 | Consume only after complete closure | WP6 cannot supply the missing representation |
| Window, time, currency, FX, calendar, alignment, missing-data, partial-window, numeric, precision, and rounding semantics | Portfolio Intelligence, with cited source authorities retained | Independently confirmed WP4 normative semantics specification required by frozen WP4 | Select exact retained modes for each method only after that specification exists | WP6 cannot bind to planning propositions or add a new mode |
| Annualization dependency representation | Owner and placement required by frozen WP4/WP2/WP3; presently unresolved | Separate governance outside WP6 | Consume only after complete closure | WP6 cannot use a literal or invent a dependency |
| Result classification, lineage, identity, serialization, temporal claim, and Provenance carriage | Portfolio Intelligence for result relations; cited source owners retain source meanings | Independently confirmed WP5 normative result contract specification required by frozen WP5 | Produce exact documentary mappings only after that specification exists | WP6 cannot bind to planning propositions or create a parallel envelope |
| Cumulative time-weighted-return method | Portfolio Intelligence | Future WP6 normative method specification | Sole documentary method authority | No runtime authority |
| Annualized-return method | Portfolio Intelligence | Future WP6 normative method specification after dependency closure | Sole documentary method authority | Blocked while the dependency gap is open |
| Rolling-return method | Portfolio Intelligence | Future WP6 normative method specification | Sole documentary method authority | No WP7 statistical semantics |
| Normalized-performance-series method | Portfolio Intelligence | Future WP6 normative method specification | Sole documentary method authority | No Experience calculation |
| Valid-history method requirements | Portfolio Intelligence | Future WP6 normative method specification under WP4 | Fix exact method requirements | No config, caller, or library default |
| Legacy runtime behavior | Existing subsystem custody only; not semantic precedent | WP1 inventory; future WP9 disposition | Characterize documentary differences | WP6 does not preserve or deprecate runtime |
| Future source placement and call sites | Future WP9 design authority | Frozen M43 WP9 allocation | None; provide documentary handoff only | No module selection in WP6 |

Every row has one owner or an explicit unresolved external gate. An unresolved
gate is not an invitation for WP6 ownership.

---

## 7. Placement model

| Concern | One normative home | Permitted WP6 artifact placement | Prohibited duplicate placement |
| --- | --- | --- | --- |
| WP6 constitutional allocation | This plan after confirmation | `docs/implementation/M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md` | Method files, fixtures, code, or Glossary |
| Required governance correction | Separately authorized M43 governance artifact | Citation only | This plan or a WP6 method specification |
| Shared contract semantics | Exact frozen WP2/WP3 specifications and independently confirmed WP4/WP5 normative specifications | Citation and exact binding only | WP6 restatement as new norms or binding to a planning proposition |
| Allocated performance-method semantics | One future WP6 normative method-specification artifact | `docs/implementation/M43_WP6_CORE_PERFORMANCE_AND_ROLLING_METHOD_SPECIFICATION.md` | Fixtures, runtime code, API, UI, or WP7–WP9 |
| Positive/boundary documentary vectors | One future WP6 positive-vector artifact | `docs/implementation/m43/fixtures/` | Method specification as an untraceable example corpus |
| Negative documentary vectors | One future WP6 negative-vector artifact | `docs/implementation/m43/fixtures/` | Runtime tests or executable fixtures |
| Legacy-behavior disposition | One section in the future WP6 normative method specification | `docs/implementation/M43_WP6_CORE_PERFORMANCE_AND_ROLLING_METHOD_SPECIFICATION.md`; an optional companion matrix is subordinate evidence only | A companion matrix cannot become a second normative home; source edits and WP9 call-site design remain prohibited |
| New confirmed vocabulary, if unavoidable | WP6 vocabulary decision plus same-change Glossary synchronization | Owning documentary artifact and `docs/GLOSSARY.md` | Fixture-only or code-only definition |
| Future runtime realization | WP9 design, then separately authorized implementation milestone | Handoff citation only | Any WP6 artifact |

The fixture corpus demonstrates specifications; it never becomes the normative
home of a semantic rule. If an optional legacy companion matrix is used, it is
selected only as subordinate evidence at execution and cannot duplicate or
replace the single normative disposition section.

---

## 8. Boundary analysis

### 8.1 Period-return boundary

The future WP6 specification must:

- cite the corrected M43 governance disposition exactly;
- consume the one canonical period-return dependency;
- preserve Ledger & Accounting-owned input accounting semantics;
- prohibit NAV-delta reconstruction and any other parallel period-return rule;
- distinguish dependency consumption from cumulative chaining; and
- leave source-level call-site selection to WP9.

This plan does not decide the corrected governance text or a chaining formula.

### 8.2 Cumulative time-weighted-return boundary

The future normative home must close, without defaults:

- exact Definition and Method Version identity;
- applicability and required period-return history;
- window-boundary treatment under the independently confirmed WP4 normative
  specification;
- exact order and arithmetic semantics;
- missing, conflicting, duplicate, and non-success input treatment;
- output value shape, unit, precision, and rounding under frozen rules; and
- result classification and value-presence mapping from the independently
  confirmed WP5 normative specification.

It may not change what a period return means.

### 8.3 Annualized-return boundary

Annualized-return work remains blocked until the WP4 section 6.7 dependency is
fully representable under WP2 and WP3. After closure, the future normative home
must bind the exact dependency, history requirement, partial-window rule,
operation order, output semantics, and the independently confirmed WP5
classification.

No ambient `252`, `365`, elapsed-period convention, library frequency, calendar
inference, caller override, or artificial fixture value may substitute for the
governed dependency.

### 8.4 Rolling-return boundary

The future normative home must close:

- exact rolling-window identity and boundary semantics;
- observation and valid-history requirements;
- permitted or prohibited partial windows;
- output-series ordering and point identity;
- missing and non-success window treatment;
- exact numerical semantics inherited from the independently confirmed WP4
  normative specification; and
- exact result-series carriage under the independently confirmed WP5 normative
  specification.

It may not import volatility, risk, benchmark-relative, or provider-calendar
semantics from WP7 or runtime libraries.

### 8.5 Normalized-performance-series boundary

The future normative home must define the performance-series transformation
and its output meaning without:

- treating a display index as Ledger NAV;
- allowing Experience to compute the series;
- falling back from a governed period return to raw NAV change;
- substituting zero for missing history;
- using input order as canonical order; or
- admitting a provider or presentation scale as semantic authority.

The exact transformation remains for the gated documentary method
specification, not this plan.

### 8.6 Valid-history and partial-window boundary

Every future method must state:

- the exact required history;
- whether partial windows are allowed or prohibited;
- the exact retained partial-window mode from the independently confirmed WP4
  normative specification;
- the sufficiency and non-success consequence of short, sparse, conflicting,
  or gapped history; and
- whether a value is present under the independently confirmed WP5 normative
  matrix.

“Use available history,” a library minimum, a UI/config threshold, or silent
window shortening is prohibited.

### 8.7 Upstream and downstream boundary

WP6 consumes WP2–WP5; it does not amend them. WP7 and WP8 may later consume only
the confirmed WP6 method results and dependencies expressly required by their
own frozen allocations. WP6 may not predefine WP7 risk or WP8 attribution.

WP9 alone owns future module placement, registry design, adapters, compatibility,
shadow comparison, API versioning, persistence options, observability, rollout,
rollback, and deprecation. WP6's legacy matrix characterizes semantic
conformance only and makes no future call-site decision.

---

## 9. No-default philosophy

Absence, ambiguity, conflict, or unrepresentability produces an exact
inapplicable, insufficient, non-success, unavailable, or degraded documentary
result as governed by frozen WP2 and the independently confirmed WP4 and WP5
normative specifications. It never permits invention.

| Concern | Prohibited default or inference | Required constitutional treatment |
| --- | --- | --- |
| Period return | Raw NAV delta, `daily_return_pct` fallback, local recomputation | Exact canonical dependency after governance correction, otherwise blocked |
| Missing return | `0`, previous value, omission | Exact non-success treatment from the independently confirmed WP4 and WP5 normative specifications |
| Window | Current date, UI selection, input extent | Exact Portfolio Measurement Window and method declaration |
| History threshold | Library minimum, config, caller preference | Exact finite method-specification choice under the independently confirmed WP4 normative specification |
| Partial window | “Use what is available” | Exact allowed/prohibited method declaration |
| Calendar | Weekdays, library calendar, provider calendar | Exact mode/evidence from the independently confirmed WP4 normative specification |
| Annualization | `252`, `365`, inferred frequency, caller value | Exact governed dependency after representability closure |
| Ordering | Input order, database order, map iteration | Exact frozen WP3 ordering and exact ordering semantics from the independently confirmed WP4 normative specification |
| Missing point | Forward fill, backfill, interpolation, zero | Exact retained rule from the independently confirmed WP4 normative specification or non-success |
| Numeric type | Binary float/library default | Exact numeric representation from the independently confirmed WP4 normative specification |
| Precision/rounding | Language, database, or display default | Exact scale, point, mode, and tie rule from the independently confirmed WP4 normative specification |
| Result status | Local `status`, null, exception text | Exact sufficiency/outcome/degradation/reason mapping from the independently confirmed WP5 normative specification |
| Timestamp | Wall clock | Complete frozen Canonical Temporal Claim |
| Provenance | Reconstruction from labels or provider | Exact already-captured records and associations |
| Provider | Live answer, symbol, preferred vendor | No provider input; exact manifest evidence only |
| Production status | Existing deployment or passing example | Remains non-production until separately authorized |

The closed-set rule is fail-closed: if a needed choice is not already admitted
by the frozen contracts and allocated to WP6, the method remains blocked.

---

## 10. Documentary vectors

### 10.1 Status and purpose

Future WP6 vectors are static documentary records. They may contain exact
inputs, expected classifications, and expected values after the relevant
method specification is authorized. They may not contain executable code,
test-runner instructions, production identifiers, live lookups, or claims of
runtime conformance.

No effective formula vector may be authored while the WP1 section 7.4 block is
open. Annualization examples remain explicitly artificial and
non-conformance-establishing until the WP4 section 6.7 gap is closed. No
effective Subject/Manifest binding or canonical-byte vector may be authored
until the frozen WP3 Portfolio Measure Subject Contract Specification section
7.1, frozen WP3 Portfolio Analytics Input Manifest Contract Specification
sections 6.3 and 10.3, and M42-WP7 section 5 Portfolio Composition
canonical-byte representability gap is separately closed. No
vector may bind a WP4 numerical row or WP5 result row until the respective
normative specification exists and is independently confirmed.

### 10.2 Required positive and boundary coverage

After gate closure, the corpus must cover at least:

1. a minimal valid canonical-period-return dependency;
2. multiple valid periods in canonical order;
3. a paired measure-side cash-flow-neutrality case demonstrating that differing
   external cash flows do not become gain or loss in the chained result,
   while consuming the Ledger & Accounting-owned canonical period-return
   semantics unchanged;
4. exact governed missing-period handling for both an interior missing period
   and a measurement-window boundary period, including the applicable
   sufficiency, outcome, degradation, and value-presence result;
5. cumulative identity and compounding boundaries;
6. zero period return;
7. a return at the exact negative boundary permitted by the numeric contract;
8. alternating positive and negative periods;
9. an exact full measurement window;
10. a valid rolling window at minimum history;
11. multiple rolling-window outputs with exact canonical order;
12. allowed partial-window behavior, if any method permits it;
13. prohibited partial-window behavior;
14. normalized-series initial-point and subsequent-point boundaries;
15. exact precision and rounding boundaries;
16. byte-identical results for equivalent canonical inputs, only after the
    frozen WP3 Portfolio Measure Subject Contract Specification section 7.1,
    frozen WP3 Portfolio Analytics Input Manifest Contract Specification
    sections 6.3 and 10.3, and M42-WP7 section 5 Portfolio Composition
    canonical-byte representability gap is separately closed;
17. permutation stability where WP3 declares entries equivalent;
18. exact success/value-present mapping from the independently confirmed WP5
    normative specification;
19. exact insufficient-input and non-success mappings from the independently
    confirmed WP5 normative specification;
20. complete temporal-claim and Provenance carriage; and
21. parity against corrected accounting baselines without treating legacy
    output as authority.

Annualized-return positive vectors are added only after dependency
representability closure and must bind the exact dependency identity, version,
and value.

### 10.3 Required negative coverage

The negative corpus must reject at least:

1. work attempted while the WP6 governance block is open;
2. a second or locally recomputed period-return formula;
3. raw NAV-delta fallback;
4. treating an external cash deposit as gain, an external withdrawal as loss,
   or recomputing Ledger & Accounting-owned cash-flow semantics inside WP6;
5. `daily_return_pct` or zero fallback;
6. missing, duplicate, conflicting, or misordered period-return evidence;
7. cross-portfolio evidence;
8. wrong Accounting Scope or Portfolio Composition;
9. ambient Current Selection or workspace selection;
10. wall-clock-derived windows;
11. silent window shortening;
12. caller or config history thresholds;
13. an implicit or caller-supplied annualization basis;
14. hidden `252` or `365`;
15. a fabricated annualization dependency kind or identity;
16. forward fill, backfill, interpolation, or zero fill not expressly retained
    by the independently confirmed WP4 normative specification;
17. binary-float, precision, or rounding defaults;
18. provider symbol or live provider answer;
19. local result status, null-on-failure, or incomplete Degraded State;
20. `UNAVAILABLE` used as a Portfolio Computation Outcome;
21. incomplete Canonical Temporal Claim;
22. reconstructed Provenance;
23. Experience-side normalized-series calculation;
24. WP7 risk or benchmark-relative semantics in a WP6 method;
25. WP8 attribution semantics in a WP6 method;
26. source call-site or runtime-module selection;
27. an executable fixture or harness; and
28. any production-method claim.

### 10.4 Vector record shape

Each future vector must record:

- stable documentary vector identifier;
- positive, boundary, negative, permutation, or parity classification;
- exact governing requirement identifiers;
- exact non-production Definition and Method Version identities;
- exact Subject and Manifest identities only after closure of the frozen WP3
  Portfolio Measure Subject Contract Specification section 7.1, frozen WP3
  Portfolio Analytics Input Manifest Contract Specification sections 6.3 and
  10.3, and M42-WP7 section 5 Portfolio Composition canonical-byte
  representability gap, or visibly artificial placeholders
  while that gap remains open;
- exact measurement window;
- exact dependency identities and versions;
- exact input values and canonical ordering;
- expected applicability, sufficiency, outcome, Degraded State, and reason;
- expected value presence or absence;
- expected value and canonical bytes only when constitutionally representable;
- complete Canonical Temporal Claim and Provenance-carriage expectation;
- explicit production authority `NONE`;
- expected accept/reject determination; and
- a short explanation that introduces no new rule.

Fixture explanation is subordinate to the normative specification.

---

## 11. Fixture strategy

### 11.1 Planned corpus

After the entry gates close, the smallest complete corpus is:

- `docs/implementation/m43/fixtures/M43_WP6_POSITIVE_DOCUMENTARY_VECTORS.md`;
  and
- `docs/implementation/m43/fixtures/M43_WP6_NEGATIVE_DOCUMENTARY_VECTORS.md`.

A separate file may be added only if corpus size makes independent review
materially clearer. File count does not create a new normative home.

### 11.2 Derivation rules

Fixtures must:

1. be derived from confirmed normative rows, never the reverse;
2. cite every governing rule directly;
3. use exact canonical representations available from frozen WP2/WP3 and the
   independently confirmed WP4/WP5 normative specifications;
4. bind any artificial Subject/Manifest placeholder directly to the frozen WP3
   Portfolio Measure Subject Contract Specification section 7.1, frozen WP3
   Portfolio Analytics Input Manifest Contract Specification sections 6.3 and
   10.3, and M42-WP7 section 5 Portfolio Composition canonical-byte
   representability gate, and mark it non-canonical,
   non-effective, and incapable of proving conformance;
5. keep source-domain meanings and ownership intact;
6. avoid provider, runtime, API, database, UI, or library artifacts;
7. pair every admitted boundary with acceptance and rejection coverage;
8. include exact expected classifications even when no value is present; and
9. remain static and non-executable.

### 11.3 Coverage closure

A traceability ledger in the future corpus must map every:

- method;
- applicability branch;
- dependency;
- retained choice from the independently confirmed WP4 normative
  specification;
- classification branch from the independently confirmed WP5 normative
  specification;
- valid-history boundary;
- partial-window branch;
- formula identity;
- serialization obligation; and
- prohibited interpretation

to at least one documentary vector. Unmapped rows block confirmation.

---

## 12. Traceability

| Frozen M43 WP6 requirement | Planned normative home | Required evidence | Gate |
| --- | --- | --- | --- |
| “Chaining the Ledger-owned canonical period return” | WP6 method specification dependency section | Exact corrected governance citation, dependency map, and no-second-formula negatives | M43 correction closed; no advance reading of “Ledger-owned” |
| Cumulative time-weighted return | WP6 method specification | Definition, Method Version, formula/applicability rows, and vectors bound to the exact upstream specifications | M43 correction and all applicable upstream binding gates closed |
| Annualized return | WP6 method specification | Exact dependency binding, formula/applicability rows, and vectors bound to the exact upstream specifications | M43 correction, WP3 concrete-binding gate, WP4/WP5 specification gates, and WP4 section 6.7 gap closed |
| Rolling return | WP6 method specification | Definition, Method Version, window/history rows, and vectors bound to the exact upstream specifications | M43 correction and all applicable upstream binding gates closed |
| Normalized performance series | WP6 method specification | Definition, Method Version, series/ordering rows, and vectors bound to the exact upstream specifications | M43 correction and all applicable upstream binding gates closed |
| Valid history | Per-method requirement matrix in the WP6 method specification | Exact thresholds and boundary vectors under the confirmed WP4 and WP5 specifications | M43 correction and WP4/WP5 specification gates closed |
| Partial window | Per-method applicability matrix in the WP6 method specification | Exact allow/reject rows and vectors under the confirmed WP4 and WP5 specifications | M43 correction and WP4/WP5 specification gates closed |
| WP3 concrete Subject/Manifest binding | Frozen WP3 specifications; exact binding only in the WP6 method specification | Exact Portfolio Composition canonical bytes and conforming concrete Subject/Manifest identities | Frozen WP3 Portfolio Measure Subject Contract Specification section 7.1, frozen WP3 Portfolio Analytics Input Manifest Contract Specification sections 6.3 and 10.3, and M42-WP7 section 5 representability gap closed |
| WP4 numerical and boundary binding | `docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`, or its exact independently confirmed path | Exact cited normative rows for every WP6 numerical choice | Specification exists and is independently confirmed |
| WP5 result binding | `docs/implementation/M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md`, or its exact independently confirmed path | Exact cited normative rows for every WP6 result classification and representation | Specification exists and is independently confirmed |
| Non-production definitions and versions | WP6 method specification | Exact WP2-conforming identities and status declarations | Vocabulary and applicable entry gates passed |
| Dependency map | WP6 method specification | Complete WP2/WP3 bindings to existing exact contract kinds and identities | All dependencies representable |
| Formula/applicability matrices | WP6 method specification | Closed rows with no ambient choices and exact WP4/WP5 citations | Applicable gates passed |
| Golden vectors | WP6 fixture corpus | Positive, boundary, negative, permutation, parity, and coverage ledger | Normative rows confirmed first; WP3 gap closed for canonical-byte vectors |
| Legacy disposition | Legacy-disposition section of the WP6 method specification | Every in-scope behavior classified without call-site design; any companion matrix is subordinate evidence | WP1 inventory cited |
| Cash-flow neutrality validation | WP6 method specification validation obligations | Paired positive/boundary case proving measure-side neutrality while consuming Ledger & Accounting-owned canonical period-return semantics unchanged, plus rejection of treating external cash flow as gain or loss | M43 correction and all applicable upstream binding gates closed |
| Missing-period handling validation | WP6 method specification validation obligations | Positive/boundary interior and boundary missing-period cases plus direct rejection of zero, omission, fill, and undeclared fallback | M43 correction and WP4/WP5 specification gates closed; WP3 gap closed for effective vectors |
| Compounding identities validation | WP6 method specification validation obligations | Cumulative identity and compounding boundary vectors | M43 correction and all applicable upstream binding gates closed |
| Short-history behavior validation | WP6 method specification validation obligations | Minimum-history, below-minimum, valid partial-window, and prohibited partial-window vectors | M43 correction and WP4/WP5 specification gates closed |
| Negative-return boundaries validation | WP6 method specification validation obligations | Exact negative boundary, alternating-return, and rejection vectors under confirmed numeric semantics | M43 correction and WP4/WP5 specification gates closed |
| Parity against corrected accounting baselines validation | WP6 method specification validation obligations | Documentary parity cases citing corrected Ledger & Accounting baselines without treating legacy output as authority | M43 correction and all applicable upstream binding gates closed |
| Documentary handoff to WP7, WP8, and WP9 | Handoff section of the WP6 method specification; derived from frozen M43 section 9 WP7/WP8 dependencies on WP2–WP6 and WP9 dependency on all earlier M43 packages | Exact confirmed WP6 identities, dependencies, result boundary, and unresolved-item state; no downstream formula or call-site design | WP6 corpus otherwise complete and independently confirmed |
| No production method | Every WP6 artifact | Explicit authority `NONE` and negative coverage | Always |
| WP6-local vocabulary rule | Vocabulary section or separate gate record | Disposition, owner, home, collision search, confirmation | Before reliance |

This table is exhaustive for the frozen M43 WP6 allocation. Anything not mapped
is outside WP6 unless a separately authorized amendment changes the frozen
architecture.

---

## 13. Dependency-safe implementation sequence

“Implementation” in this section means production of documentary
specifications and static documentary fixtures only.

1. **Freeze this plan.** Obtain independent confirmation that scope,
   ownership, placement, exclusions, and gates match frozen M43.
2. **Preserve the block.** Make no method, formula, applicability, or effective
   fixture change while WP1 section 7.4 remains open.
3. **Receive the external M43 correction.** Cite, but do not author, the
   independently confirmed correction resolving the architecture/WP1
   disposition mismatch.
4. **Preserve the WP3 representability gate.** Make no concrete
   Subject/Manifest binding, emission, or canonical-byte vector until separate
   authority closes the frozen WP3 Portfolio Measure Subject Contract
   Specification section 7.1, frozen WP3 Portfolio Analytics Input Manifest
   Contract Specification sections 6.3 and 10.3, and M42-WP7 section 5
   Portfolio Composition canonical-byte gap.
5. **Receive the WP4 and WP5 normative specifications.** Require each exact
   binding source to exist, be independently confirmed, and be cited by exact
   repository path before a WP6 row binds its numerical or result semantics.
6. **Revalidate prerequisites.** Confirm frozen WP1–WP5 remain unchanged and
   effective, every required normative specification exists, and the M43
   correction creates no duplicate rule.
7. **Run the WP6 vocabulary gate.** Admit no new noun unless the downstream
   rule is completely satisfied.
8. **Build the dependency map.** Bind exact inherited contracts and identify
   any remaining unrepresentable dependency before formula work.
9. **Partition method work by gate.** Keep annualized return blocked while
   WP4 section 6.7 remains open; do not let that gap weaken another method.
10. **Specify cumulative performance.** Produce the non-production Definition,
   Method Version, applicability, dependency, numerical, and result mappings.
11. **Specify rolling return.** Close window, history, partial-window, ordering,
   numerical, and result mappings.
12. **Specify normalized performance series.** Close transformation, ordering,
    history, numerical, and result mappings without presentation semantics.
13. **Specify annualized return only after closure.** Bind the exact
    represented annualization dependency and then close the allocated method.
14. **Complete legacy disposition.** Characterize each in-scope legacy
    behavior as conforming, conflicting, incomplete, or non-precedential,
    without selecting future code action.
15. **Derive positive and boundary vectors.** Create static vectors from
    confirmed normative rows.
16. **Derive negative vectors.** Prove rejection of defaults, ownership leaks,
    cross-WP absorption, executable behavior, and production claims.
17. **Close frozen validation allocation.** Require cash-flow neutrality,
    missing-period handling, compounding identities, short-history behavior,
    negative-return boundaries, and parity against corrected accounting
    baselines to map to normative rows and vectors.
18. **Close traceability.** Require every scope, deliverable, validation,
    handoff, normative row, and rejection to map to evidence.
19. **Perform independent performance-method review.** Require constitutional
    and numerical reviewers to reach the same interpretation independently.
20. **Correct only WP6 artifacts.** Route any frozen-authority defect to its
    owner; never repair it inside WP6.
21. **Confirm and freeze WP6.** Confirmation requires every allocated method
    complete, every applicable gate closed, unresolved findings `NONE`, and
    production authority still `NONE`.

WP6 cannot be declared complete by omitting annualized return. If its external
dependency remains unresolved, WP6 remains incomplete and blocked.

---

## 14. Independent review strategy

### 14.1 Constitutional review

An independent constitutional reviewer must verify:

- the allocation is exactly frozen M43 section 9;
- the WP1 period-return ownership split is preserved;
- the standing governance block is neither ignored nor cured locally;
- the frozen WP3 Portfolio Measure Subject Contract Specification section 7.1,
  frozen WP3 Portfolio Analytics Input Manifest Contract Specification
  sections 6.3 and 10.3, and M42-WP7 section 5 Portfolio Composition
  canonical-byte representability gate is inherited and not cured locally;
- the WP4 and WP5 plan artifacts are not treated as substitutes for their
  required independently confirmed normative specifications;
- every concern has one owner and one normative home;
- no WP1–WP5 responsibility is absorbed;
- no WP7–WP9 concern is anticipated;
- vocabulary is closed or independently gated;
- all authority declarations are complete; and
- no production, runtime, executable, provider, persistence, API, or UI
  authority appears.

### 14.2 Independent numerical review

After method work is permitted, a reviewer independent from the specification
author must verify:

- the period-return dependency is consumed without recomputation;
- formulas cover exactly the allocated meanings;
- operation order is complete and deterministic;
- every numerical choice cites the exact independently confirmed WP4 normative
  specification and no default remains;
- valid-history and partial-window behavior is closed per method;
- cash-flow neutrality, missing-period handling, negative-return, compounding,
  sparse-history, and rounding boundaries are complete;
- annualization is absent while its dependency is unrepresentable; and
- expected documentary values are reproducible without runtime or library
  assumptions.

### 14.3 Contract and fixture review

An independent reviewer must verify:

- every method conforms to frozen WP2 identities and applicability;
- every concrete input conforms to frozen WP3 only after the Portfolio
  Composition canonical-byte representability gate closes;
- every output cites and conforms to the independently confirmed WP5 normative
  specification's classification and serialization;
- fixture rows derive from, and do not define, normative semantics;
- every normative row has positive/boundary coverage;
- every prohibited interpretation has direct negative coverage; and
- artificial material cannot be mistaken for canonical or effective material.

### 14.4 Legacy and boundary review

An independent reviewer must verify that:

- deployed behavior is evidence, not precedent;
- raw-NAV, zero, daily-return, benchmark, calendar, and history defaults are
  rejected where inconsistent;
- no runtime disposition or call site is selected;
- Experience computes nothing; and
- WP7, WP8, and WP9 boundaries remain intact.

### 14.5 Independence and confirmation

Review must be performed by readers who did not author the relevant normative
rows or fixture expectations. Review findings must be recorded explicitly.
Corrections must be reviewed again. WP6 freezes only when all required reviews
confirm the corpus and unresolved findings are `NONE`.

---

## 15. Acceptance criteria

This planning artifact is acceptable only if:

1. it allocates all and only the frozen M43 WP6 concerns;
2. it preserves the WP1 section 7.4 standing block;
3. it preserves the frozen WP3 Portfolio Measure Subject Contract
   Specification section 7.1, frozen WP3 Portfolio Analytics Input Manifest
   Contract Specification sections 6.3 and 10.3, and M42-WP7 section 5
   Portfolio Composition canonical-byte representability gap;
4. it preserves the WP4 section 6.7 annualization representability gap;
5. it requires the independently confirmed WP4 and WP5 normative
   specifications to exist before WP6 binds their rows;
6. it defines no method formula or executable semantic;
7. every semantic concern has one owner or an explicit external unresolved
   owner gate;
8. every concern has one normative home;
9. inherited vocabulary is closed and no new noun is admitted;
10. authority declarations are complete and every production/runtime class is
   `NONE`;
11. no frozen artifact is changed;
12. no prior-WP responsibility is absorbed;
13. no future-WP responsibility is anticipated;
14. all six frozen M43 WP6 validation criteria are allocated and traceable;
15. repository changes are documentary only; and
16. the plan contains scope, exclusions, dependencies, ownership, placement,
    authority, vocabulary, no-default rules, boundaries, vectors, fixtures,
    traceability, review, repository modifications, and completion reporting.

### 15.1 Planning validation matrix

| Required validation | Planning result | Evidence in this artifact |
| --- | --- | --- |
| Constitutional allocation complete | `PASS` | Sections 0, 4, and 12 map all six frozen WP6 concerns and all frozen deliverables |
| Ownership singular | `PASS` | Section 6 assigns one owner per concern and treats unresolved external authority as a block, never as WP6 ownership |
| Placement singular | `PASS` | Section 7 assigns one normative home per concern |
| Vocabulary closed | `PASS` | Section 5 reuses frozen vocabulary and admits no new noun |
| Fail-closed inheritance complete | `PASS` | Sections 0, 1, 3, 6, 10, 11, 13, and 15 preserve the WP1 block, WP3 canonical-byte gate, WP4/WP5 specification-existence gates, and WP4 annualization gate |
| Traceability complete | `PASS` | Sections 10 and 12 allocate every frozen scope item, deliverable, validation criterion, and constrained downstream handoff |
| Authority declarations complete | `PASS` | Section 2.2 declares every applicable authority class |
| No capability expansion | `PASS` | Sections 4.2, 15, and 16 prohibit deployment and capability-completion claims |
| No executable semantics | `PASS` | This artifact defines allocation and gates but no formula, algorithm, executable fixture, or runtime behavior |
| No production authority | `PASS` | Authority block and sections 2.2, 15, and 18 declare production-method authority `NONE` |
| No redesign of frozen artifacts | `PASS` | Sections 2, 3, 4.2, 16, and 18 require exact frozen consumption and prohibit amendment |
| Documentary-only scope preserved | `PASS` | Sections 0, 13, and 16 authorize only documentary artifacts |

### 15.2 Future WP6 corpus acceptance

The future WP6 documentary corpus is complete only when:

1. the separate M43 governance correction is independently confirmed;
2. the frozen WP3/M42-WP7 Portfolio Composition canonical-byte
   representability gap is separately closed before any concrete
   Subject/Manifest or canonical-byte claim;
3. the WP4 and WP5 normative specifications exist, are independently
   confirmed, and are cited by exact repository path;
4. every allocated core-performance output has one exact non-production
   Portfolio Measure Definition;
5. every allocated method has one exact non-production Portfolio Method
   Version for each retained specification;
6. every method has an exact input, dependency, applicability, valid-history,
   partial-window, numerical, and result contract;
7. no second period-return formula exists;
8. Ledger & Accounting-owned accounting semantics remain unchanged;
9. annualized return is specified only after complete dependency
   representability closure;
10. all formulas and operation orders are deterministic and confined to the
   allocated method family;
11. all WP4 choices from the independently confirmed normative specification
    are explicit and no default remains;
12. all WP5 classifications, temporal claims, lineage, Provenance, and
    canonical bytes from the independently confirmed normative specification
    are complete, and Subject/Manifest bytes are claimed only after the WP3
    representability gate closes;
13. documentary vectors cover every normative, validation, and rejection row;
14. cash-flow neutrality, missing-period handling, compounding identities,
    short-history behavior, negative-return boundaries, and parity against
    corrected accounting baselines are each independently validated;
15. legacy behavior is fully characterized without becoming precedent;
16. two independent readers obtain the same method meaning and expected
    documentary outcomes;
17. constitutional, numerical, contract, fixture, and boundary reviews are
    confirmed;
18. unresolved findings are `NONE`;
19. no executable artifact exists;
20. no production method is admitted; and
21. no capability-completion claim is made.

---

## 16. Repository modifications

### 16.1 Corrective modification authorized now

This corrective work item authorizes modification only of:

- `docs/implementation/M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md`.

No frozen file, Glossary entry, fixture, source file, test, schema, migration,
API, UI, provider integration, or production-status artifact is authorized for
change.

### 16.2 Planning review-sequence artifacts authorized now

Review, correction, and confirmation of this planning artifact are not gated
on future method-work entry conditions. Their exact placements are:

- `docs/implementation/M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN_INDEPENDENT_REVIEW.md`;
- `docs/implementation/M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN_REQUIRED_CORRECTIONS_RESPONSE.md`;
  and
- `docs/implementation/M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN_INDEPENDENT_CONFIRMATION.md`.

These artifacts may review, record corrections to, and confirm this plan only.
They cannot close an external governance gate or authorize method work.

### 16.3 Planned gate-conditional WP6 execution artifacts

Only after the applicable gates close, a separately reviewed WP6 execution may
add:

- `docs/implementation/M43_WP6_CORE_PERFORMANCE_AND_ROLLING_METHOD_SPECIFICATION.md`;
- `docs/implementation/m43/fixtures/M43_WP6_POSITIVE_DOCUMENTARY_VECTORS.md`;
- `docs/implementation/m43/fixtures/M43_WP6_NEGATIVE_DOCUMENTARY_VECTORS.md`;
- `docs/implementation/M43_WP6_INDEPENDENT_CONSTITUTIONAL_AND_NUMERICAL_REVIEW.md`;
- `docs/implementation/M43_WP6_REQUIRED_CORRECTIONS_RESPONSE.md`, if required;
  and
- `docs/implementation/M43_WP6_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md`.

`docs/GLOSSARY.md` may change only if a WP6-local noun is independently
confirmed for admission or rename, and only in the same separately authorized
change. This plan identifies no such noun.

### 16.4 Prohibited repository effect

WP6 planning and later documentary execution must not modify:

- frozen M43 Architecture or WP1–WP5 artifacts;
- M1–M42 artifacts;
- production source or configuration;
- backend or frontend tests;
- database models or migrations;
- API or UI surfaces;
- providers, schedulers, caches, or observability;
- ROADMAP capability-completion state; or
- future WP7–WP9 artifacts.

---

## 17. Completion report

The eventual WP6 completion report must contain:

1. **Implementation summary** — documentary artifacts produced, allocated
   methods closed, and explicit non-production status;
2. **Files created** — exact repository-relative documentary paths;
3. **Validation performed** — vocabulary, ownership, placement, dependency,
   formula, numerical, fixture, traceability, no-default, no-executable, and
   no-production reviews;
4. **Gate evidence** — exact independently confirmed M43 correction, exact
   closure of the frozen WP3/M42-WP7 Portfolio Composition canonical-byte
   representability gap, exact independently confirmed WP4 and WP5 normative
   specification paths, and exact annualization representability closure;
5. **Method coverage** — one-to-one mapping from every frozen M43 WP6 output to
   its Definition, Method Version, contract rows, and vectors;
6. **Unresolved findings** — must be `NONE`;
7. **Frozen-artifact confirmation** — exact statement that M43 Architecture
   and WP1–WP5 remain unchanged;
8. **Allocation confirmation** — exact statement that WP6 follows frozen M43
   and absorbs no earlier or future package;
9. **Authority confirmation** — exact statement that no constitutional,
   runtime, implementation, executable, provider, persistence, API, UI, or
   production-method authority expanded; and
10. **Capability statement** — exact statement that no roadmap capability was
    declared deployed or complete.

If any required external governance gate, representability gate, or
specification-existence gate remains open, the report must say `WP6 INCOMPLETE
— BLOCKED`, identify the exact gate, and make no completion or confirmation
claim.

---

## 18. Final constitutional boundary

M43-WP6 is a future non-production method-specification package for cumulative
time-weighted return, annualized return, rolling return, normalized performance
series, and their valid-history and partial-window rules. It consumes the one
canonical period-return dependency, but it neither owns nor redefines the
Ledger & Accounting semantics that determine what enters that return.

This plan completes the deterministic allocation of that package. It does not
begin the blocked method work, close any external governance or
representability gate, substitute a plan for a required normative
specification, define a formula, create an executable artifact, choose a
runtime location, admit a production method, or change a frozen noun, owner,
placement, or artifact.
