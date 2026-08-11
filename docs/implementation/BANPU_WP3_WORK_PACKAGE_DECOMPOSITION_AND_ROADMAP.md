# BANPU-WP3 — Work Package Decomposition and Roadmap

**Artifact class:** Planning artifact only
**Work package:** `BANPU-WP3 — Quote identity and epoch protection`
**Status:** `PLANNING DECISIONS RATIFIED — PLANNING CONFIRMATION NOT PERFORMED — IMPLEMENTATION NOT AUTHORIZED`
**Constitutional predecessor:** `BANPU-WP2 — EPIC CLOSED; IMPLEMENTATION FROZEN`
**Gate S2:** `SATISFIED` by the Architecture Owner ratification of 2026-08-10, recorded in [Architecture and Implementation Plan](BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §6.0
**Authority:** Frozen `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`, `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`, and `BANPU_IMPLEMENTATION_SEQUENCE.md`, together with [BANPU-WP3 Architecture and Implementation Plan](BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
**Amendment:** Bounded Planning Amendment `BPA-1` (2026-08-11) adds one line to §4.4 "Files expected to change" and adds §4.4.1, and changes no other text in this artifact. See [BANPU-WP3 Bounded Planning Amendment Record](BANPU_WP3_BOUNDED_PLANNING_AMENDMENT_RECORD.md).

This artifact decomposes BANPU-WP3 into independently reviewable sub-packages.
It does not authorize implementation by itself, cannot change the canonical
design, and cannot alter the package inventory in
`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`. WP3 remains one package in that
inventory; the sub-packages below exist to give review granularity inside it.

## 1. Universal sub-package rules

- Sub-packages execute in the order defined in §3 and §8. A sub-package does
  not begin until its predecessor is accepted.
- Every sub-package includes focused tests for its own behavior.
- The union of all sub-package file lists may not exceed BANPU-WP3's
  authorized file surface in `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md` §5,
  except where roadmap §1 rule 7 has been satisfied.
- "Files expected to change" is a bounded forecast. Adding another production
  file requires reviewer confirmation that it is strictly necessary under the
  canonical design.
- Existing quote and history behavior for unconverted assets must remain
  compatible, and under the ratified PD-1 (NARROW) that compatibility is
  numeric, including in the sparse-bar case. The corrected close derivation
  applies only where required to prevent epoch mixing for a converted identity.
- No sub-package may modify M46, the WP1 frozen corpus, the WP2 frozen corpus,
  the canonical design, the roadmap, or the implementation sequence.
- No sub-package may create a general corporate-action framework or place
  conversion logic in market-data policy abstractions.

## 2. Authorized file surface

The canonical WP3 file surface, reproduced from
`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md` §5.

**Expected to change**

- `backend/services/market_data/yahoo_chart.py`
- `backend/services/data_fetcher.py`
- The narrow holdings and price call site in `backend/main.py` if required to
  pass the binding
- `backend/tests/test_yahoo_chart_provider.py`
- `backend/tests/test_fetch_history.py`
- New focused quote-epoch test file if useful

**Explicitly not to change**

- Transaction or portfolio database schema
- `backend/services/portfolio_rebuilder.py`
- `backend/services/ledger_validator.py`
- `backend/services/portfolio_transactions.py`
- Frontend transaction authoring
- All M46 files

**Rule 7 item.** WP3.2 introduces one new production module in
`backend/services/market_data/`. It is an additional production file beyond the
forecast above and therefore requires reviewer confirmation of strict necessity
under roadmap §1 rule 7 before WP3.2 begins. The necessity argument is
recorded in §4.2 and rests on the canonical purity discipline of the
market-data domain: the binding, epoch, admissibility, and quarantine predicate
must contain no provider-specific import and no I/O, and therefore cannot live
in either `yahoo_chart.py` or `data_fetcher.py` without violating that
discipline.

## 3. Sub-package inventory

| Sub-package | Name | Depends on | Implementation size | Review size |
|---|---|---|---:|---:|
| BANPU-WP3.1 | Provider evidence extraction — first provider adapter | WP1 | S | S |
| BANPU-WP3.2 | Conversion quote binding, epoch, and quarantine contract | WP3.1 | S–M | M |
| BANPU-WP3.3 | Cache namespacing and fail-closed fetch integration | WP3.2 | M | M |
| BANPU-WP3.4 | Call-path propagation and regression evidence | WP3.3 | S | S |

Size guide matches the canonical roadmap: S is a localized change with focused
tests; M is several cooperating concerns.

## 4. Sub-packages

### 4.1 BANPU-WP3.1 — Provider evidence extraction

#### Purpose

Extract the evidence required to judge quote identity and epoch membership, and
correct the evidence defects present in the current adapter, for the first
provider adapter brought into compliance.

#### Scope

- Extract the symbol actually served by the provider alongside the symbol
  requested.
- Associate each close observation with its timestamp.
- Derive current and previous close from a single response rather than from two
  independent sources, on the path that serves a converted identity. Under the
  ratified PD-1 (NARROW), values returned for unconverted and unbound requests
  are numerically unchanged, including in the sparse-bar case.
- Expose the exchange timezone basis required for epoch classification, under
  the ratified PD-2 convention.
- Emit the above as a provider-neutral evidence structure.

This sub-package is conversion-unaware. It contains no binding, no epoch
comparison, and no quarantine decision. It is named as the first provider
implementation of a provider-agnostic obligation, not as a provider-coupled
design.

#### Files expected to change

- `backend/services/market_data/yahoo_chart.py`
- `backend/tests/test_yahoo_chart_provider.py`

#### Explicit files not to change

- `backend/services/market_data/base.py`
- `backend/services/market_data/provider.py`
- Any other provider adapter
- Everything in §2 "explicitly not to change"

#### Dependencies

BANPU-WP1 accepted — satisfied. PD-1 ratified, because this sub-package carries
the change whose blast radius PD-1 scopes — satisfied; NARROW is elected, and
this sub-package carries the resulting dual derivation path. PD-2 ratified,
because the timezone basis is part of the extracted evidence — satisfied.

#### Deliverables

- Provider-neutral evidence structure carrying provider identity, served
  symbol, timestamped closes, and exchange timezone basis.
- Corrected single-source derivation of current and previous close.
- Fixture tests for matching metadata, mismatched metadata, missing metadata,
  sparse closes, and epoch boundaries.

#### Acceptance contribution

Supplies the evidence on which A1, A2, A6, and E1 through E5 depend. Preserves
A4 and A12 in its own right.

#### Verification

Provider fixture tests; the existing Yahoo chart suite; characterization
evidence captured under gate S5 before the first edit.

### 4.2 BANPU-WP3.2 — Conversion quote binding, epoch, and quarantine contract

#### Purpose

Express, as a pure and independently testable contract, what makes a quote
admissible for a converted identity and what happens when it is not.

#### Scope

- Immutable binding value constructed from the frozen WP1 payload contract:
  `asset_id + provider + provider_symbol + quote_epoch_start_date + valuation_transition_date`.
- Deterministic derivation of epoch-namespaced cache-key components.
- Epoch classification of timestamped observations against the payload's
  calendar dates, under the convention ratified in PD-2.
- The WP3 Provider Evidence Contract predicate E1 through E5, under PD-4.
- Reference-price admissibility: present, positive, finite, decimal-exact, and
  evidence-bound. Mechanical continuity tolerance is excluded and belongs
  to WP5.
- Enumerated quarantine reasons covering the conditions in design §10 together
  with evidence-contract non-satisfaction.
- A consultable, deterministic quarantine result carrying reason and affected
  identity, satisfying PD-3 obligation B1.

The module performs no I/O, reads no clock, accesses no database, resolves no
registry identity, and contains no provider-specific import. This mirrors the
purity discipline already established by `execution_quote.py` and
`session_evidence.py`.

#### Files expected to change

- One new module under `backend/services/market_data/`, subject to the rule 7
  confirmation in §2
- One new focused test module under `backend/tests/`

#### Explicit files not to change

- `backend/services/transaction_canonicalizer.py`, which is frozen WP1; the
  binding consumes it and never amends it
- Everything in §2 "explicitly not to change"

#### Dependencies

BANPU-WP3.1 accepted. PD-2 and PD-4 ratified — satisfied. Rule 7 confirmation
obtained — open, per gate S8.

#### Deliverables

- Binding value object and epoch cache-key derivation.
- Evidence-contract predicate.
- Reference-price admissibility predicate.
- Quarantine reason enumeration and consultable result.

#### Acceptance contribution

A7, A9, and A10, and the derivation on which A3 and A11 depend. Discharges the
WP3 half of `MINOR-2`.

#### Verification

Fixture-only unit tests across matching, mismatched, missing, sparse, and
boundary evidence; both edges of the exchange-local day for a UTC+7 market;
qualifying and non-qualifying provider evidence; admissible and inadmissible
reference prices.

### 4.3 BANPU-WP3.3 — Cache namespacing and fail-closed fetch integration

#### Purpose

Apply the contract at the only layer that performs market-data I/O, and make
failure closed.

#### Scope

- Binding-aware quote and history fetch.
- Epoch-namespaced `cache_type` values for converted identities, of the form
  `quote:asset=<asset_id>:epoch=<date>` and
  `history:5y:1d:asset=<asset_id>:epoch=<date>`.
- Suppression of predecessor stale-cache fallback for converted and
  quarantined identities across every cache read path.
- The Option C guard set: a set of converted provider symbols consulted solely
  to refuse unbound requests, empty while no conversion row exists. Its
  authoritative source, staleness bound, undetermined-membership behavior, and
  acceptance evidence are fixed by the ratified PD-5 invariant G1 through G4.
  The mechanism satisfying that invariant remains an implementation decision
  and is not settled by this artifact.
- Enforcement of PD-4 at the binding-consumption layer.
- Structured quarantine logging.

Unconverted identifiers retain their existing symbol-based keys and existing
read, write, and fallback behavior.

#### Files expected to change

- `backend/services/data_fetcher.py`
- New focused quote-epoch isolation test module

#### Explicit files not to change

- `backend/models/database.py`; the existing `MarketDataCache` uniqueness
  constraint on symbol and cache type is sufficient and no schema change is
  required
- Admin cache endpoints
- Everything in §2 "explicitly not to change"

#### Dependencies

BANPU-WP3.2 accepted. PD-5 ratified, because the guard set's lifecycle and
A10's verifiability both depend on it — satisfied.

#### Deliverables

- Binding-aware fetch path.
- Converted-asset cache namespace.
- Stale-fallback suppression.
- Guard set and refusal behavior, including the G4 transition test required by
  the ratified PD-5: an identity that becomes converted after the guard
  projection was first populated is refused for an unbound caller, in the same
  running process, without restart.
- Quarantine logging contract.

#### Acceptance contribution

A3, A5, A8, A10, A11, and A12. Carries the primary burden of A4 and A6.

#### Verification

Cache hit, cache miss, stale fallback, and namespace tests; proof that the
unbound path is unchanged from baseline while the guard set is empty; the
existing data-fetcher suite.

This is the highest-regression sub-package in WP3 and is expected to carry the
largest share of review attention.

### 4.4 BANPU-WP3.4 — Call-path propagation and regression evidence

#### Purpose

Supply the binding at the one call site that owns portfolio identity, and prove
that unaffected consumers are unaffected.

#### Scope

- Binding propagation at the narrow holdings and price call site.
- Enumeration, as review evidence, of every price call site that does not
  supply a binding, together with the demonstration that each receives a
  structured refusal rather than an incorrect value for a converted identity.
- A focused regression suite for unaffected quote and history consumers,
  replacing reliance on `backend/tests/test_fetch_history.py`, which is a live
  print script rather than a regression suite.

No endpoint is added, no response shape changes, and no consumer module outside
the authorized surface is modified.

#### Files expected to change

- `backend/main.py`, holdings and price call site only
- `backend/services/data_fetcher.py`, **one bounded propagation accessor only**,
  admitted by amendment `BPA-1` and constrained exactly by §4.4.1 and Plan §5.3.1
- `backend/tests/test_fetch_history.py`
- Focused regression test modules

#### Explicit files not to change

- `backend/services/portfolio_snapshots.py`
- `backend/services/idea_review.py`
- `backend/services/analytics/factor_engine.py`
- Everything in §2 "explicitly not to change"

The three service modules above are price consumers and are deliberately left
unmodified. Their protection is delivered by refusal at the fetch layer in
WP3.3, not by editing them. How each responds to a refusal is WP5 and WP6
scope.

#### Dependencies

BANPU-WP3.3 accepted.

#### Deliverables

- Binding propagation at the owning call site.
- Unbound call-site register with refusal evidence.
- Regression suite for unaffected consumers.

#### Acceptance contribution

A1, A2, A4, A5, A6, A13, and A14, and closure of the roadmap deliverable
"regression tests for unaffected quote callers".

#### Verification

Focused regression suite; existing Yahoo chart and data-fetcher suites; file
boundary audit.

Confirmation that the frozen WP2 deferral guard test remains green is a
**frozen-boundary preservation check**, of the same class as the M46 and
frozen-corpus audits, discharging PD-3 obligation B3. It asserts that WP3
changed nothing in WP2's territory. It is **not** a WP3 dependency on validator
behavior, and no WP3 test asserts validator semantics.

#### 4.4.1 Bounded propagation accessor

**Bounded Planning Amendment `BPA-1`, 2026-08-11. Additive.** This subsection
admits one bounded cross-package surface element into WP3.4 and changes nothing
else in this artifact. Its architectural justification — why the original WP3.4
surface was insufficient, why a `main.py`-only implementation would force
forbidden policy duplication, why the accessor is plumbing rather than new
architecture, and why `backend/services/data_fetcher.py` remains WP3.3-owned for
enforcement — is recorded at Plan §5.3.1 and is not restated here.

**Authorized element.** Exactly one accessor, and nothing else:

| Item | Value |
|---|---|
| File | `backend/services/data_fetcher.py` |
| Accessor | `resolve_successor_bindings(symbols)` |
| Sub-package | WP3.4 |
| Class | Production, read-only |
| Purpose | Expose requested, non-ambiguous canonical `SuccessorQuoteBinding` values from the already-accepted WP3.3 conversion guard projection, solely so the authorized WP3.4 holdings and price call path in `backend/main.py` can propagate bindings |

The accessor is named exactly because the amendment's boundedness is defined by
its exact identity. Plan §11's reservation of module and symbol naming to
allocated implementation authority is otherwise unchanged, and this naming
extends to no other symbol.

**Constraints.** Binding on implementation. The accessor:

| # | Constraint |
|---|---|
| 1 | creates no persistent state |
| 2 | performs no memoization and holds no cache |
| 3 | changes no guard-membership semantics |
| 4 | changes no quarantine policy and adds, removes, or reinterprets no quarantine reason |
| 5 | changes no `fetch_price_info` or `fetch_history` semantics, signature contract, or return shape |
| 6 | performs no provider lookup |
| 7 | performs no registry lookup |
| 8 | reads no environment value and no configuration value |
| 9 | exposes no boundary evidence |
| 10 | constructs no binding outside the accepted WP3.2 and WP3.3 machinery; it reads already-constructed values |
| 11 | leaves ambiguous and unavailable projection states fail-closed — such a symbol is simply absent from the result, and its request proceeds unbound into WP3.3's existing refusal |
| 12 | authorizes no caller other than the single WP3.4 holdings and price call path in `backend/main.py` |
| 13 | confers on WP3.4 no authority over any other `backend/services/data_fetcher.py` behavior |

**Ownership.** `backend/services/data_fetcher.py` remains WP3.3-owned for all
enforcement. This subsection admits one read-only accessor for WP3.4
propagation support; it does not reallocate the file, and §4.3 is unamended.

**Review lifecycle.**

- **Prior Checkpoint C3 acceptance remains valid for the pre-accessor WP3.3
  state.** This amendment reopens no accepted WP3.1, WP3.2, or WP3.3 semantics.
  No WP3.1 re-review, no WP3.2 re-review, and no full WP3.3 re-review is
  required or implied.
- **The accessor itself requires a focused C3 delta review**, scoped to the
  accessor and to constraints 1 through 13 above, and performed after the
  amended planning corpus is reconfirmed, re-frozen, and synchronized into
  Allocation and Implementation Authorization.
- **Checkpoint C4 remains incomplete** until both the accessor delta receives
  focused C3 acceptance and the Step 4.1 exhaustive eleven-site unbound
  call-site evidence is completed.

This subsection creates no new gate. The §6 gate table is unamended, and the
focused C3 delta review is an amendment-borne review obligation inside the
existing gate S4 discipline, not a ninth gate.

## 5. Dependency graph

```text
BANPU-WP1  Persistence and canonical contract   [FROZEN]
    ↓
BANPU-WP2  Replay and independent validator     [FROZEN, EPIC CLOSED]
    ↓
BANPU-WP3  Quote identity and epoch protection
    ├── WP3.1  Provider evidence extraction
    │       ↓
    ├── WP3.2  Binding, epoch, and quarantine contract
    │       ↓
    ├── WP3.3  Cache namespacing and fail-closed fetch
    │       ↓
    └── WP3.4  Call-path propagation and regression evidence
    ↓
BANPU-WP4  Registry and live materialization
```

The strict internal sequence favours review certainty over parallel
implementation, consistent with roadmap §11. Deployment still places the WP3
quote guard into production before any conversion row is authored.

## 6. Gate sequence

Gates are constitutional. They fix what must be true and in what order; they do
not enumerate implementation steps.

| # | Gate | State |
|---|---|---|
| S1 | WP2 accepted before WP3 begins | Satisfied |
| S2 | PD-1, PD-2, PD-4, and PD-5 ratified and R7 closed — all five — before BANPU-WP3 Planning Confirmation | Satisfied — Architecture Owner ratification of 2026-08-10 |
| S3 | Planning Confirmation precedes Planning Freeze; Planning Freeze precedes Allocation; the Work Package Plan is drafted only after Allocation | Pending |
| S4 | Sub-packages implemented serially per §5, each independently reviewed and accepted before its successor begins | Pending |
| S5 | Baseline behavioral evidence captured before the first production edit | Pending |
| S6 | WP3 closes through review, corrections, confirmation, implementation freeze, epic closeout, and Decision Log synchronization | Pending |
| S7 | WP4 does not begin until WP3 is confirmed and frozen; approved but unfrozen does not satisfy the gate | Pending |
| S8 | Rule 7 reviewer confirmation obtained for the WP3.2 module before WP3.2 begins | Open |

## 7. Delegated to the BANPU-WP3 Work Package Plan

The following are deliberately absent from this artifact and belong to the
Work Package Plan issued after allocation:

- Step enumeration and ordering within each sub-package.
- Review checkpoint placement and reviewer instructions.
- Baseline capture method, fixture inventory, and characterization-test
  construction.
- Verification command invocation points, including `git diff --check` and
  `graphify update .`.
- Test module names, module and symbol names, and suite composition.
- Per-step expected results and evidence recording format.

## 8. Completion condition

BANPU-WP3 is complete when all four sub-packages are accepted, the canonical
acceptance criteria A1 through A5 and the derived criteria A6 through A14 are
satisfied, and the frozen WP1 and WP2 corpora are unchanged.

Completion satisfies the WP4 entry gate. It does not authorize release, does
not authorize production data mutation, does not close any carried-forward
residual, and does not resolve the emitter-locus item referred out by PD-3,
which is not WP3's to close.

## 9. Excluded effects

This artifact does **not**:

- authorize implementation;
- allocate implementation authority;
- authorize release;
- modify any implementation file;
- amend the canonical design, roadmap, or implementation sequence;
- alter the BANPU package inventory or the package-level dependency graph;
- amend, reopen, or reinterpret WP1 or WP2, or any frozen artifact;
- resolve, weaken, or close any carried-forward residual;
- assign scope, work, or obligation to any package other than BANPU-WP3; or
- modify M46.

## 10. Exact next constitutional act

Gate S2 is satisfied. The exact next constitutional act is **BANPU-WP3 Planning
Confirmation**, followed by **Planning Freeze**, then **Allocation**. The
BANPU-WP3 Work Package Plan is drafted only after Allocation, per gate S3.

This artifact performs no part of any of those acts and creates no
implementation authority.
