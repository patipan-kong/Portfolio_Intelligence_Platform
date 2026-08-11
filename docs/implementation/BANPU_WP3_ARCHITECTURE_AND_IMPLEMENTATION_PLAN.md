# BANPU-WP3 — Architecture and Implementation Plan

**Artifact class:** Planning artifact only
**Work package:** `BANPU-WP3 — Quote identity and epoch protection`
**Status:** `PLANNING DECISIONS RATIFIED — PLANNING CONFIRMATION NOT PERFORMED — IMPLEMENTATION NOT AUTHORIZED`
**Constitutional predecessor:** `BANPU-WP2 — EPIC CLOSED; IMPLEMENTATION FROZEN`
**Gate S2:** `SATISFIED` by the Architecture Owner ratification of 2026-08-10 (§6.0)
**Authority:** Frozen `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`, `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`, `BANPU_IMPLEMENTATION_SEQUENCE.md`, `BANPU_WP1_FREEZE_RECORD.md`, `BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md`, `BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md`, and `BANPU_WP2_EPIC_CLOSEOUT.md`
**Amendment:** Bounded Planning Amendment `BPA-1` (2026-08-11) adds §5.3.1 and the closing paragraph of §5.4, and changes no other text in this artifact. See [BANPU-WP3 Bounded Planning Amendment Record](BANPU_WP3_BOUNDED_PLANNING_AMENDMENT_RECORD.md).

This plan defines the scope, architecture, boundaries, dependencies, risks, and
acceptance criteria for BANPU-WP3. It does not authorize implementation, does
not allocate implementation authority, and cannot change the canonical design.
Sub-package decomposition and gate sequencing are carried in
[BANPU-WP3 Work Package Decomposition and Roadmap](BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md).

## 1. Milestone determination

The successor milestone is fixed by canonical authority and is not open to
selection. `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md` §2 and §5 and
`BANPU_IMPLEMENTATION_SEQUENCE.md` Step 3 both name:

**BANPU-WP3 — Quote identity and epoch protection.**

Entry conditions are satisfied by repository state. WP1 is `FROZEN WITH
RECORDED RESIDUALS`. WP2 is `IMPLEMENTATION FROZEN` and `EPIC CLOSED`, merged
into the canonical baseline. Both WP2 closure records state explicitly that
they do not allocate BANPU-WP3, so allocation remains an open constitutional
act ahead of this plan.

The defect surface WP3 exists to remove is present and unmitigated in the
current baseline:

- `backend/services/market_data/yahoo_chart.py` `get_quote()` performs no
  comparison of the requested symbol against provider `meta.symbol`.
- Current price is read from provider metadata while previous close is read
  positionally from the close series, so the two values may originate from
  different evidence with no timestamp association.
- `backend/services/data_fetcher.py` keys all cache reads and writes on
  `(symbol, cache_type)`, so a reused or redirected identifier inherits its
  predecessor's cached values, including through the stale-fallback path.

## 2. Objectives

| # | Objective | Canonical source |
|---|---|---|
| O1 | A converted identity can never consume predecessor-epoch market data | Design §2 goal 6; Sequence Step 3 exit |
| O2 | Provider responses are treated as evidence to be verified, not trusted by position | Design §10 |
| O3 | Quote and history cache entries for converted assets are asset- and epoch-bound | Design §10 |
| O4 | Failure is closed: quarantine yields no usable price and no predecessor stale fallback | Design principle 8 |
| O5 | Unconverted assets retain existing behavior, cache keys, and response shape | Design principle 10 |
| O6 | Protection is independently deployable before any conversion row exists | Design §14 step 3 |

O6 is load-bearing. The canonical deployment strategy places the quote guard in
production ahead of the migration and ahead of ledger activation. WP3 must
therefore be correct and inert in a repository containing zero conversion rows.

## 3. Scope

### 3.1 In scope

- **Provider evidence extraction and verification.** Normalized
  requested-symbol comparison against the symbol the provider served;
  timestamp-associated close series; current and previous close derived from a
  single response.
- **Conversion quote binding.** The value
  `asset_id + provider + provider_symbol + quote_epoch_start_date + valuation_transition_date`,
  constructed from the WP1-frozen `PositionConversionQuoteBinding` and
  `PositionConversionDates` contracts.
- **Cache namespacing.** `cache_type` values of the form
  `quote:asset=<asset_id>:epoch=<date>` and
  `history:5y:1d:asset=<asset_id>:epoch=<date>`, using the existing
  `MarketDataCache` schema unchanged.
- **Quarantine contract.** Enumerated structured reasons covering the
  conditions in design §10, a fail-closed result, deterministic logging, and
  blast radius limited to the affected converted identity.
- **Provider evidence qualification.** The WP3 Provider Evidence Contract
  (§6.3) and its enforcement at the binding-consumption layer.
- **Reference-price admissibility.** The WP3 half of WP1 residual `MINOR-2`.
- **Focused regression coverage** for unaffected quote and history consumers.

### 3.2 Out of scope

| Excluded | Owner or reason |
|---|---|
| Any change to `portfolio_rebuilder.py`, `ledger_validator.py`, `portfolio_transactions.py` | WP2 frozen corpus; roadmap §5 "NOT to change" |
| Validator emission of `POSITION_CONVERSION_QUOTE_QUARANTINED` | Unowned; referred for separate constitutional determination (§6.4) |
| Snapshot blocking behavior on quarantine | WP5 |
| Mechanical NAV continuity tolerance admissibility | WP5 (the other half of `MINOR-2`) |
| Optimizer and evaluation refresh blocking | WP6 |
| Registry mutation, identifier retirement, `MERGED_INTO` authoring | WP4 |
| Succession-aware lookups in shadow, attribution, and evaluation | WP6 |
| CLI, operator manifest, cache purge execution, rehearsal | WP7 |
| Transaction or portfolio schema; `MarketDataCache` schema | Design §7, §10 |
| Frontend and public API authoring surface | Design §3 |
| Generalized corporate-action or event framework | Design §3, §17 |
| M46 in any respect | Roadmap §1 |

### 3.3 Design §10 obligations not discharged by WP3

Recorded explicitly so that no clause of design §10 is left without an owner:

| Clause | Owner |
|---|---|
| "blocks affected snapshots" | WP5 |
| "blocks downstream optimizer/evaluation refresh" | WP6 |
| "mechanical boundary value MUST reconcile within the payload tolerance" | WP5 |
| `POSITION_CONVERSION_QUOTE_QUARANTINED` emission (design §11) | Unowned by any package; referred for separate constitutional determination (§6.4) |

## 4. Boundary verification

### 4.1 Against completed work packages

Every WP3 scope item was checked against delivered WP1 and WP2 responsibility.
No overlap exists.

| WP3 item | WP1 (frozen) | WP2 (frozen) | Verdict |
|---|---|---|---|
| Quote-binding payload fields | Defines the typed contract | Consumes for replay | WP3 reads only; no redefinition |
| Reference-price admissibility | Parses decimals; consumer validation deferred as `MINOR-2` | Not addressed | WP3 owns by named assignment |
| Quarantine predicate | Absent | Finding ID catalogued only; predicate deferred | WP3 owns; no overlap |
| Provider symbol and timestamp verification | Absent | Absent | Greenfield in WP3 |
| Cache namespacing | Absent | Absent | Greenfield in WP3 |
| Conversion replay and validation | — | Owns | WP3 must not touch |

WP2's own specification defers quote identity, epochs, cache namespacing, and
quarantine evidence to WP3, so the boundary is asserted from both sides.

### 4.2 Against future work packages

| Package | Creep vector | Status |
|---|---|---|
| WP4 | Registry read, `MERGED_INTO` authoring, identifier retirement | Clear — the binding is built from the payload only; no registry access in any sub-package |
| WP5 | Snapshot blocking; mechanical tolerance reconciliation | Clear — excluded by §3.2 and by the wording of A9 and A10 |
| WP6 | Succession-aware time series, shadow valuation | Clear — WP3 is stateless with respect to succession chains |
| WP7 | Cache purge, CLI, manifest, rehearsal | Clear — WP3 owes enumerability only, per A11 |
| WP8 | Integrated regression and release evidence | Clear — WP3 assigns WP8 no work. The emitter-locus item is referred out of the package inventory entirely (§6.4), not deferred to WP8 |

## 5. Architectural analysis

### 5.1 Reuse-first assessment

WP3 requires no new architectural layer. Four existing structures carry it.

1. **`MarketDataCache.cache_type` is already a compound namespace field.** Its
   uniqueness constraint is `(symbol, cache_type)` and its documented purpose
   is to encode both the data kind and the fetch parameters. Epoch namespacing
   is a string-convention change inside an existing field: no schema work, no
   migration, and existing rows remain valid.
2. **The WP1 payload contract already carries every binding input.**
   `PositionConversionQuoteBinding` supplies provider and provider symbols;
   `PositionConversionDates` supplies `successor_quote_epoch_start_date` and
   `valuation_transition_date`. No registry access is required, which keeps WP3
   cleanly outside WP4's territory.
3. **`backend/services/market_data/` already houses pure evidence modules.**
   `execution_quote.py` and `session_evidence.py` establish the discipline WP3
   should follow: immutable frozen dataclasses built by pure adapters that do
   not resolve registry identity, access a cache or database, fetch the
   network, or read a clock.
4. **Provider metadata extraction already exists.**
   `adapt_yahoo_chart_execution_quote()` already records the provider symbol
   and session metadata without comparing or rejecting on mismatch. WP3's
   verification is a predicate over evidence that is already extracted, not new
   extraction machinery.

Explicitly rejected as unnecessary abstraction: a general market-data policy
engine; a provider-agnostic corporate-action price adapter; a new cache table
or cache-key entity; and a shared position-conversion service module, which
the roadmap assigns to WP6 if it is needed at all.

### 5.2 Provider neutrality

The architecture is provider-parameterized by construction, and WP3 implements
the first qualifying adapter rather than coupling the design to one provider.

| Evidence | Location |
|---|---|
| Abstract provider contract with `get_quote` and `get_history` as interface methods | `backend/services/market_data/base.py` |
| Runtime provider selection rather than compile-time binding | `backend/services/market_data/provider.py` |
| The WP1-frozen binding carries `provider` as a first-class field | `backend/services/transaction_canonicalizer.py` |

Design §10 states the obligation over "provider adaptation" generically. The
roadmap's phrase "validate requested symbol against Yahoo chart metadata" names
the first implementation, not the principle.

The boundary is made structural rather than documentary: provider-specific
extraction is confined to the adapter sub-package, and the verification
predicate operates on a provider-neutral evidence structure and contains no
provider-specific import. A future provider qualifies by producing that
structure, with no change to the predicate, the binding, the cache namespace,
or the quarantine contract.

### 5.3 Binding propagation

`fetch_price_info(symbol)` is symbol-only and has eleven call sites across four
modules: eight in `backend/main.py`, one each in
`backend/services/portfolio_snapshots.py`,
`backend/services/idea_review.py`, and
`backend/services/analytics/factor_engine.py`. Three propagation strategies
were considered.

| Option | Mechanism | Coverage | Cost |
|---|---|---|---|
| A. Explicit binding only | Optional binding parameter supplied by callers | Only bound call sites protected; the remainder silently bypass | Minimal |
| B. Default-deny by lookup | Conversion state resolved per fetch | Complete | Database read on every quote; couples the cache layer to the ledger |
| C. Hybrid guard set | Explicit binding is the only way to obtain a converted-identity price; a set of converted provider symbols is consulted solely to refuse unbound requests | Complete and fail-closed | One bounded lookup; no effect while no conversion row exists |

**Adopted: Option C, unconditionally.** It satisfies fail-closed behavior
without violating "no unaffected drift", because the guard set is empty until a
conversion row exists, which by the canonical deployment order is after WP3
ships. It also converts the roadmap's single-call-site forecast from a
correctness gap into a provable boundary: an unbound consumer of a converted
identity receives a refusal, never an incorrect number.

**Guard-set lifecycle.** Option C makes correctness depend on the guard set's
contents, and the set transitions from empty to non-empty in production only
after WP4 materializes a conversion, which is after WP3 is deployed. A set that
is loaded lazily and memoized without a defined refresh condition would remain
empty across that transition and fail **open**. The freshness invariant that
forecloses that failure — authoritative source, staleness bound,
undetermined-membership behavior, and required transition evidence — is fixed
by the ratified PD-5 (§6.5) as G1 through G4. Option C's adoption is no longer
conditional, and A10 is verifiable against that invariant.

### 5.3.1 Propagation surface — the WP3.4 binding accessor

**Bounded Planning Amendment `BPA-1`, 2026-08-11. Additive.** This subsection
adds one bounded cross-package surface element. It amends no other section,
alters no planning decision, acceptance criterion, gate, or risk, and reopens no
accepted sub-package semantics.

**The deficiency.** §5.3 fixes that an explicit binding is the only route to a
converted-identity price, and §5.4 places binding propagation at the
`backend/main.py` holdings and price call path. Neither states where that call
path *obtains* the binding. The omission is one of surface allocation, not of
architecture, but under the unamended surface it leaves the WP3.4 propagation
outcome unreachable by any lawful edit.

**Why the original WP3.4 surface was insufficient.** WP3.4's authorized
production surface is the holdings and price call site in `backend/main.py`, and
nothing else. A binding is the five-field value of §3.1, every element of which
is drawn from a `POSITION_CONVERSION` payload canonicalized by the frozen WP1
contract. `backend/main.py` owns portfolio holding identity — the holdings and
their symbols — and holds no canonical conversion field. Under the unamended
surface the call path can therefore neither be handed a binding nor obtain one,
and every holdings price request for a converted identity would reach the fetch
layer unbound and be refused. That outcome is fail-closed, and it is not the
WP3.4 propagation outcome: it leaves the outcome undeliverable rather than
delivered.

**Why a `main.py`-only implementation is inadmissible.** To construct the
binding itself, `backend/main.py` would have to read `POSITION_CONVERSION`
ledger rows, canonicalize them through the frozen WP1 contract, build the
binding, and decide the ambiguous and undetermined-membership cases. Those are
precisely WP3.3's guard-projection obligations under the ratified PD-5 G1
through G4, together with WP3.2's construction and quarantine obligations. A
second implementation of them in an API module would establish a second
membership authority, which G1 forbids, and a second quarantine policy, which A7
and PD-3 obligation B1 forbid. The remaining alternative — importing WP3.3's
private projection internals into `backend/main.py` — would cross the accepted
WP3.3 module boundary and place enforcement logic in an API module, contrary to
§5.4.

**What is authorized.** Exactly one bounded accessor in
`backend/services/data_fetcher.py`, whose sole purpose is to expose requested,
non-ambiguous canonical successor binding values already present in the accepted
WP3.3 conversion guard projection, so that the single authorized WP3.4 holdings
and price call path in `backend/main.py` can propagate them. Its exact identity
and its binding constraints are fixed by
[Decomposition](BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) §4.4.1.

**Why the accessor is cross-package plumbing, not new architecture.** It
introduces no layer, no abstraction, no policy, and no state. It decides
nothing: membership, binding construction, ambiguity, and undetermined-source
refusal are each already decided by the accepted WP3.2 contract and the accepted
WP3.3 projection, and the accessor reads their result. It adds no admissibility
element, no quarantine reason, and no evidence obligation. Dependency direction
is unchanged and still points strictly upward — WP3.4 consumes WP3.3, exactly as
§5.4 states. Removing the accessor would remove a read, not a rule.

**Why `data_fetcher.py` remains WP3.3-owned.** Enforcement ownership follows the
obligation, not the file. Every enforcement obligation in
`backend/services/data_fetcher.py` — the guard projection and its PD-5 G1–G4
invariant, binding-aware fetch, cache namespacing, stale-fallback suppression,
PD-4 enforcement at the binding-consumption layer, and quarantine logging —
remains WP3.3's, unamended and unreopened. This amendment admits one read-only
accessor into that file for WP3.4 propagation support and confers on WP3.4 no
authority over any other behavior in it. The file is not reallocated.

### 5.4 Layering

```text
WP3.1  yahoo_chart.py        provider evidence extraction (conversion-unaware)
           ↓  provider-neutral evidence structure
WP3.2  new market-data module binding value, epoch classification,
                              admissibility, evidence contract, quarantine
                              reasons (pure; no I/O, no clock, no database)
           ↓  consumed by
WP3.3  data_fetcher.py       binding-aware fetch, namespaced cache,
                              guard set, stale-fallback suppression
           ↓  consumed by
WP3.4  main.py holdings path binding propagation and regression evidence
```

Dependencies point strictly upward. WP3.1 and WP3.2 are testable with fixtures
alone. Only WP3.3 touches I/O; only WP3.4 touches an API module.

**Amended by `BPA-1` (§5.3.1).** The `↓ consumed by` edge from WP3.3 to WP3.4 is
realized by one bounded read-only accessor residing in the WP3.3-owned module,
because `backend/main.py` holds no canonical conversion field from which the
binding could otherwise be obtained. The layering, the ownership of
`backend/services/data_fetcher.py`, and the strictly upward dependency direction
are unchanged.

### 5.5 Backward compatibility

Preserved without exception, including numerically in the sparse-bar case,
which is fixed by the ratified PD-1 (§6.1).

- `get_quote()` returns the same three-key dictionary; `fetch_price_info()`
  returns the same shape.
- Unconverted `cache_type` strings retain their present values, so no cache
  invalidation event occurs and existing rows remain valid.
- No public API request or response contract changes.
- No migration is introduced by WP3.

## 6. Planning decisions

Planning decisions bind implementation. They are recorded here in final form.

### 6.0 Architecture Owner ratification record

On 2026-08-10 the Architecture Owner ratified the five items that gated
BANPU-WP3 Planning Confirmation under gate S2. The decisions are recorded here
as taken; this plan does not restate reasoning that belongs to the ratifying
authority and does not reopen any of them.

| Item | Architecture Owner decision |
|---|---|
| PD-1 | **NARROW.** The corrected close derivation applies only where required to prevent epoch mixing for converted identities. Unconverted and unbound derivation remains numerically unchanged. Design §2 goal 8, design principle 10, roadmap §5, and canonical acceptance criterion A4 remain unamended. Pre-change characterization evidence remains required before the first production edit |
| PD-2 | **RATIFIED AS SPECIFIED.** Epoch classification uses exchange-local calendar dates derived from the provider-reported exchange timezone. UTC-date comparison is rejected |
| PD-4 | **RATIFIED AS SPECIFIED.** The conditional dependency on PD-2 is satisfied by the same ratification. The E1–E5 Provider Evidence Contract is binding |
| PD-5 | **RATIFIED.** G1 through G4 are ratified exactly as stated in §6.5. No implementation mechanism is prescribed; implementation authority remains free to choose the mechanism provided the ratified invariant is satisfied |
| R7 | **PATH B — FORMAL WAIVER**, scoped exactly to "No BANPU-WP3 obligation is inherited." The waiver does not define, reinterpret, weaken, or resolve any residual. It binds BANPU-WP3 only; WP4–WP8 inherit the residuals unchanged |

PD-3 was already resolved as to WP3 scope by restatement of canonical text
(§6.4) and was not part of the gate S2 register.

This record is a record of decisions taken. It performs no Planning
Confirmation, no Planning Freeze, and no allocation of implementation
authority.

### 6.1 PD-1 — Unconverted previous-close semantics

**Status:** RATIFIED — **NARROW**.

**The question.** Does the corrected close derivation apply to all symbols, or
only where required to protect a converted identity?

**The ratified answer.** The corrected derivation applies **only where required
to prevent epoch mixing for a converted identity**. Derivation for unconverted
and unbound requests is numerically unchanged, including in the sparse-bar
case. Design §2 goal 8, design principle 10, roadmap §5, and canonical
acceptance criterion A4 remain unamended. The implementation cost accepted by
this election is a dual derivation path confined to the adapter sub-package.

**The canonical tension the ratification resolves.** Two canonical statements
bore on the question and were not reconciled by any existing artifact:

- Design §10 states, unconditionally over provider adaptation, that closes MUST
  be associated with their timestamps and that current and previous close MUST
  derive from one result. Read plainly, this applies to every symbol.
- Design §2 goal 8 requires preserving **all existing behavior** for portfolios
  without `POSITION_CONVERSION`; design principle 10 requires that portfolios
  without conversions remain unchanged; and roadmap §5 requires preserving
  existing quote behavior for unconverted assets. Read plainly, these forbid a
  numeric change to unconverted output.

The two readings diverge only in the sparse-bar case, where the most recent bar
is absent and positional derivation currently selects a different close than
timestamp association would. NARROW resolves the divergence by confining the
corrected derivation to the converted path, leaving the canonical
no-unaffected-drift boundary intact as written.

**Not elected.** The alternative resolution — amending design §2 goal 8, design
principle 10, and roadmap §5 so that correcting a defective derivation is not
drift — was not elected. No amendment to those artifacts is sought, required,
or implied by WP3.

**Binding effect on WP3.** WP3.1 carries a dual derivation path: corrected
single-source, timestamp-associated derivation on the converted path, and the
existing derivation, numerically unchanged, on every other path. No WP3
artifact may reinterpret a canonical design principle, and none does.

**Standing condition.** Pre-change values are captured as characterization
evidence before the first production edit.

### 6.2 PD-2 — Epoch timezone convention

**Status:** RATIFIED AS SPECIFIED.

Epoch classification maps provider observation timestamps to exchange-local
calendar dates, using the exchange timezone reported by the provider, and
compares them against the timezone-free calendar dates carried in the frozen
WP1 payload. UTC-date comparison is explicitly rejected.

**Condition:** boundary fixtures cover both edges of the exchange-local day for
a UTC+7 market.

### 6.3 PD-4 — Provider evidence qualification

**Status:** RATIFIED AS SPECIFIED. The conditional dependency on PD-2, which
defines E5, is satisfied by the same ratification. The E1–E5 contract below is
binding.

A converted identity may be served market data only by a provider adapter that
satisfies the WP3 Provider Evidence Contract. A provider that does not satisfy
the contract yields a structured quarantine for that identity; it does not
yield an unvalidated price.

The rule is stated over capability, not identity. No provider name, module
path, environment variable, or configuration value forms part of it.

**WP3 Provider Evidence Contract.** To serve a converted identity, a provider
adapter must supply all of:

| # | Required evidence | Purpose |
|---|---|---|
| E1 | The provider identity it acts as, comparable to the binding's provider | Binds the response to the frozen WP1 payload discriminator |
| E2 | The symbol the provider actually served, comparable post-normalization to the symbol requested | Cross-symbol detection |
| E3 | Per-observation timestamps for the close series | Epoch classification without positional inference |
| E4 | Current and previous close derivable from a single response | Prevents mixed-origin evidence |
| E5 | A deterministic basis for mapping observation timestamps to exchange-local calendar dates | Epoch boundary correctness, per PD-2 |

Non-satisfaction is a first-class quarantine condition enumerated alongside the
conditions in design §10, not an error or an exception. Qualification is
affirmative: an adapter that is silent about its evidence does not qualify.

Enforcement lives at the binding-consumption layer in the fetch path. The
platform's provider-selection mechanism is untouched, and unconverted assets
are unaffected regardless of which provider is selected.

### 6.4 PD-3 — Quarantine predicate ownership

**Status:** RESOLVED as to WP3 scope, by restatement of canonical text rather
than by election.

**Predicate ownership is already canonical and is not a WP3 decision.**
`BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md` §5.4 states that WP3 supplies
quote, epoch, and quarantine behavior, and that WP2 preserves only the finding
ID and severity in the conversion finding catalog without fabricating or
querying quote evidence. Its finding-catalog table records the disposition
directly: `Catalogued in WP2; predicate remains WP3-owned`. The same section
states that catalog presence is not authorization to implement another
package's evidence producer, and that a deferred predicate becomes active only
in its constitutionally assigned package.

WP3 therefore owns the quarantine predicate and the reason contract, and
produces them in the market-data domain as scoped in §3.1.

**Obligations on WP3.**

| # | Obligation |
|---|---|
| B1 | Expose quarantine state as a consultable, deterministic artifact carrying enumerated reason and affected identity |
| B3 | Leave the frozen WP2 deferral guard test unmodified and green throughout WP3 |

Obligation numbering is preserved; B2 and B4 were withdrawn with the deferral
described below.

**Referred item — emitter locus.** Design §11 lists
`POSITION_CONVERSION_QUOTE_QUARANTINED` among the validator's required
findings, but no canonical artifact assigns the validator call site to any
package. The item is referred out of WP3 and is **not** a WP3 planning
decision, a WP3 residual, or a WP3 obligation. It is recorded here solely so it
is not lost:

- Neither `POSITION_CONVERSION_QUOTE_QUARANTINED` nor
  `POSITION_CONVERSION_REBUILD_BOUNDARY` appears anywhere in production source.
  Both appear only in the frozen WP2 deferral guard test. "Catalogued in WP2"
  is a documentary catalog disposition, not a code-level emitter awaiting
  wiring.
- The condition is not specific to WP3. `POSITION_CONVERSION_REBUILD_BOUNDARY`
  is WP5-owned by the same §5.4 mechanism, and roadmap §7's WP5 file list also
  excludes `backend/services/ledger_validator.py`. The emitter locus is
  therefore an unresolved question shared by both deferred findings.
- No package's canonical scope currently admits the work.
  `backend/services/ledger_validator.py` is listed under WP3's files not to
  change; WP2's implementation authority is recorded as exhausted and closed
  and the epic closeout states that no further implementation work belongs to
  WP2; and roadmap §10 confines WP8 to proving deployability without adding new
  production behavior, permitting production source changes only as fixes
  strictly required to close a failed acceptance criterion in an owning prior
  package.

Resolution requires a separate constitutional determination by the authority
that governs the canonical design, roadmap, and package inventory. **WP3
planning neither performs that determination nor assigns the work to any
package**, and no WP3 acceptance criterion depends on its outcome.

### 6.5 PD-5 — Guard-set authority and freshness

**Status:** RATIFIED.

**The question.** What is the guard set's authoritative source, under what
condition is it refreshed, and what evidence proves the refresh is sufficient?

**Why it is load-bearing.** Under Option C (§5.3), no unbound caller may obtain
a price for a converted identity, and A10 asserts exactly that. The guarantee
holds only while the guard set reflects the set of converted identities that
actually exist. WP3 is deployed before any conversion row is authored, and
roadmap §2 places live materialization in WP4, after WP3. The set therefore
transitions from empty to non-empty in production while WP3 code is already
running. A set loaded once and memoized without a refresh condition would still
be empty at that moment, and every unbound caller would receive a predecessor
price rather than a refusal. The failure is silent and fail-open, which
principle 8 forbids.

**Ratified invariant.** G1 through G4 are binding on implementation.

| # | Ratified element |
|---|---|
| G1 | **Authoritative source.** The canonical `POSITION_CONVERSION` ledger evidence, as canonicalized by the frozen WP1 contract, is the sole authority for converted-identity membership. Any in-process structure is a **projection** of it and is never itself authoritative. No configuration value, constant, or environment setting may define membership |
| G2 | **Refresh condition and staleness bound.** A projection may never be relied upon beyond a declared, finite, and testable staleness bound. Unbounded memoization is inadmissible. The bound must be small relative to the interval between a conversion becoming authoritative and the next quote serve, such that no serve can occur against a projection formed before a conversion that is already authoritative |
| G3 | **Undetermined membership.** If membership cannot be determined — source unavailable, projection expired and unrefreshable, or any error — the request is refused with an enumerated quarantine reason. Undetermined never resolves to "not converted" |
| G4 | **Acceptance evidence.** Acceptance requires a transition test: an identity that becomes converted *after* the guard projection was first populated is refused for an unbound caller, in the same running process, without restart. A test exercising only an empty set and a pre-populated set does not discharge G4 |

**Mechanism remains an implementation decision.** The ratification fixes the
invariant, not the mechanism. No cache lifetime, event hook, or query strategy
is prescribed; implementation authority is free to choose any mechanism that
satisfies G1 through G4. This preserves the classification in §11, which places
guard-set caching mechanics and invalidation with allocated implementation
authority.

### 6.6 Gate S2 register — closed

| Item | Required act | State |
|---|---|---|
| PD-1 | Architecture Owner ratification selecting an admissible resolution | Closed — NARROW elected (§6.1) |
| PD-2 | Architecture Owner ratification | Closed — ratified as specified (§6.2) |
| PD-4 | Architecture Owner ratification; depended on PD-2, which defines E5 | Closed — ratified as specified; dependency satisfied by the same act (§6.3) |
| PD-5 | Architecture Owner ratification fixing G1 through G4 | Closed — ratified (§6.5) |
| R7 | Definition or formal waiver of the WP2 residuals `MINOR-A`, `MINOR-B`, and `OBSERVATION-A` through `OBSERVATION-E` | Closed — formal waiver adopted (§6.7) |

All five items in the gate S2 register are closed. PD-3 is resolved as to WP3
scope; its referred item is not a WP3 planning decision and does not gate this
corpus.

No planning decision is open.

### 6.7 R7 — Formal waiver of the undefined WP2 residuals

**Disposition:** PATH B — FORMAL WAIVER, adopted by the Architecture Owner on
2026-08-10.

The residuals `MINOR-A`, `MINOR-B`, and `OBSERVATION-A` through
`OBSERVATION-E` are carried forward by
`BANPU_WP2_IMPLEMENTATION_CONFIRMATION.md` §2,
`BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md` §4, and
`BANPU_WP2_EPIC_CLOSEOUT.md` §5 as identifiers without accompanying text. No
committed repository artifact defines them; the Step 9 Focused Independent
Implementation Re-Review in which they originate is recorded by its disposition
only and was never committed as a repository artifact.

**Waiver, in its exact scope:**

> No BANPU-WP3 obligation is inherited.

**The waiver does not** define, reinterpret, weaken, or resolve any residual.
All seven remain carried forward exactly as accepted, and the WP2 records that
carry them are neither amended nor reinterpreted by this artifact.

**The waiver binds BANPU-WP3 only.** WP4 through WP8 inherit the residuals
unchanged, and this waiver creates no precedent, disposition, or relief for any
of them.

The waiver itself is carried as a WP3 planning-freeze residual under §12.

## 7. Dependency analysis

### 7.1 Upstream

Roadmap §2 records WP3's dependency as WP1 only. Roadmap §11 places WP2 before
WP3 in the strict sequence, and roadmap §1 rule 2 makes acceptance of the
predecessor a start condition. The two relations are distinct and both are
satisfied.

| Relation | Value | State |
|---|---|---|
| Technical dependency | WP1 — the binding consumes the frozen canonical payload contract | Satisfied |
| Sequencing predecessor | WP2 — procedural only, not a technical coupling | Satisfied |
| Clean baseline | Working tree clean on the working branch | Satisfied |
| WP3 planning freeze and allocation | This plan is input to those acts | Not started |

The distinction matters in implementation: WP3 must not import, extend, or
assume any WP2 artifact, and no WP3 test may depend on rebuilder or validator
behavior.

**Frozen-boundary verification is not a dependency.** Confirming that the
frozen WP2 deferral guard test remains green is a boundary-preservation check
on WP3's own change surface, of the same class as the M46 and frozen-corpus
audits. It asserts that WP3 changed nothing in WP2's territory. It is not a
behavioral dependency, does not couple WP3 to validator semantics, and is not
satisfied by any WP3 test asserting validator behavior.

### 7.2 Downstream consumers

| Consumer | What it requires from WP3 |
|---|---|
| WP4 | Nothing structurally; the identity it materializes must match the binding WP3 validates |
| WP5 | Quarantine state consultable so snapshots can be blocked; reference prices already admissibility-checked |
| WP6 | Epoch-safe prices for post-boundary shadow valuation |
| WP7 | Deterministically enumerable namespaced cache keys as purge targets |
| WP8 | Quote-path golden evidence |

### 7.3 Inherited residuals landing in WP3

| Residual | Source | WP3 obligation |
|---|---|---|
| `MINOR-2`, partial | WP1 renewed review | Reject inadmissible provider and reference prices at the point of consumption, with focused tests, without amending the frozen WP1 parser. Mechanical continuity tolerance admissibility remains WP5's |

WP1's `MINOR-1`, `MINOR-5`, and `NEW-MINOR-A` are assigned to WP4, WP7, and WP8
and are not WP3 work.

### 7.4 Unresolved governance state noted, not reopened

The WP1 residual identity record classifies `backend/models/database.py` as
`IDENTITY NOT RECONSTRUCTABLE` and states that the WP2 Step 8 gate remains
blocked pending an Architecture Owner determination. Later WP2 records proceed
past it. WP1 and WP2 artifacts are treated as canonical and closed and are not
reinterpreted here. This plan records only that WP3 enters with an unclosed WP1
residual whose terminal condition names a decision that no repository artifact
shows as taken.

## 8. Risks

| ID | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | Design §11 lists the quarantine finding among validator requirements, but no canonical artifact assigns the validator call site to any package | Medium | Referred out of WP3 by PD-3 (§6.4). No WP3 acceptance criterion depends on it; WP3 owns and delivers the predicate under B1 |
| R2 | Ten of eleven `fetch_price_info` call sites lie outside WP3's authorized file list, so explicit-binding-only propagation would leave unprotected paths | High | Option C guard set (§5.3), adopted unconditionally under the ratified PD-5; every unbound site enumerated in the Work Package Plan |
| R3 | Timestamp-associating previous close changes values for unconverted symbols when the latest bar is absent, against design goal 8 and principle 10 | High | Foreclosed by the ratified PD-1 (§6.1): NARROW confines the corrected derivation to the converted path, leaving unconverted values numerically unchanged; characterization evidence still captured before the first production edit |
| R11 | A guard set loaded once and memoized without a refresh condition would remain empty after WP4 materializes a conversion, silently failing open | High | Ratified PD-5 (§6.5) G1–G4; G2 forbids unbounded memoization, G3 refuses on undetermined membership, and G4's transition test is mandatory acceptance evidence |
| R4 | Provider bar timestamps are UTC while epoch dates are timezone-free calendar dates, producing off-by-one classification at UTC+7 | High | Ratified PD-2; boundary fixtures at both edges of the exchange-local day |
| R5 | Requested symbols pass through DR normalization on some paths and not others, so naive equality could quarantine DR holdings | Medium | Compare against the symbol as sent to the provider; explicit DR fixtures |
| R6 | `backend/tests/test_fetch_history.py` is a live print script with no test functions, yet the roadmap names it as WP3 regression evidence | Medium | Create a real focused suite; record the roadmap inaccuracy for separately approved documentation correction rather than amending the roadmap from WP3 |
| R7 | WP2 residuals `MINOR-A`, `MINOR-B`, `OBSERVATION-A`–`OBSERVATION-E` exist as labels only, so WP3 cannot verify it inherits no obligation | Medium | Closed by the formal waiver in §6.7: no BANPU-WP3 obligation is inherited. The residuals remain unresolved and bind WP4–WP8 unchanged; the waiver is carried as a planning-freeze residual (§12) |
| R8 | Cache namespace change strands existing rows | Low | Converted namespaces are new keys; legacy rows expire naturally; purge is WP7 |
| R9 | Scope creep toward a general market-data policy layer | Low | Design §17 authority boundary; exhaustive per-sub-package file lists |
| R10 | A provider adapter that does not satisfy the WP3 Provider Evidence Contract could serve an unvalidated price for a converted identity | High | Ratified PD-4; enforcement at the binding-consumption layer, with contract non-satisfaction as an enumerated quarantine reason |

## 9. Acceptance criteria

### 9.1 Canonical criteria

Reproduced from roadmap §5 and authoritative. Where any derived criterion
conflicts with these, these govern.

| # | Criterion |
|---|---|
| A1 | Cross-symbol or cross-epoch results never produce a usable quote |
| A2 | First successor-epoch quote may return a null previous close but never a predecessor close |
| A3 | Converted cache entries are asset- and epoch-bound |
| A4 | Unconverted quote dictionaries and cache keys retain current behavior |
| A5 | Quarantine blocks only the affected converted identity |

### 9.2 Derived criteria

Subordinate verification aids. They add no scope beyond §3.1 and cannot
override A1–A5.

| # | Criterion | Anchor |
|---|---|---|
| A6 | With zero conversion rows, quote and history behavior is provably indistinguishable from baseline | A4; design §14 step 3 |
| A7 | Every quarantine emits exactly one enumerated reason; no rejection is free-text only | Roadmap §5 deliverable |
| A8 | A quarantined identity receives no stale-cache fallback through any cache read path | Roadmap §5 scope; principle 8 |
| A9 | Reference prices are rejected when absent, non-positive, non-finite, or not decimal-exact and evidence-bound, at the point of consumption, without amending the frozen WP1 parser | `MINOR-2`, WP3 half only |
| A10 | No caller can obtain a price for a converted identity without a valid binding served by a contract-qualifying provider; refusal is observable and structured. Verified against the ratified PD-5 invariant, including the G4 transition test | A1, A5; principle 8; PD-4; PD-5 |
| A11 | Namespaced `cache_type` values are deterministically derivable from the binding and enumerable, verified with no change to any admin endpoint | A3 |
| A12 | No migration, no `MarketDataCache` schema change, and no public API contract change | Design §3, §7, §10 |
| A13 | The change surface is confined to the authorized file lists; M46 unchanged; WP1 and WP2 frozen corpora unchanged | Roadmap §1, §5 |
| A14 | `graphify update .` runs and the change surface matches the declared boundary | Project instructions |

A9 deliberately excludes mechanical continuity tolerance reconciliation, which
is WP5's. A10 deliberately stops at "no incorrect price is served" and does not
define downstream snapshot, optimizer, or evaluation behavior, which are WP5's
and WP6's. A11 deliberately owes enumerability only; purge execution is WP7's.

## 10. Planning gates

Planning fixes what must be true and in what dependency order. Step ordering,
review checkpoint placement, and verification mechanics belong to the
BANPU-WP3 Work Package Plan.

| # | Gate |
|---|---|
| S1 | WP3 does not begin until WP2 is accepted — satisfied |
| S2 | PD-1, PD-2, PD-4, and PD-5 are ratified and R7 is closed — all five — before BANPU-WP3 Planning Confirmation — **satisfied** by the Architecture Owner ratification of 2026-08-10 (§6.0, §6.6) |
| S3 | Planning Confirmation precedes Planning Freeze; Planning Freeze precedes Allocation; the Work Package Plan is drafted only after Allocation |
| S4 | Sub-packages are implemented serially in the order fixed by the decomposition artifact |
| S5 | Baseline behavioral evidence is captured before the first production edit; it is unrecoverable afterwards |
| S6 | WP3 closes through the standard lifecycle: review, corrections, confirmation, implementation freeze, epic closeout, Decision Log synchronization |
| S7 | WP4 may not begin until WP3 is confirmed and frozen; approved but unfrozen does not satisfy the gate |

## 11. Classification of statements

**Planning decisions, binding on implementation:** the scope boundary in §3;
the boundary verification in §4; the architectural positions in §5, including
Option C and provider neutrality; PD-1 through PD-5; the derived acceptance
criteria in §9.2; the gates in §10; and the sub-package decomposition carried
in the companion artifact.

**Implementation decisions, deferred to allocated implementation authority:**
module and symbol names; the concrete quarantine reason enumeration members;
function signatures for binding-aware fetch; guard-set caching mechanics and
invalidation; test file names and fixture layout; and log message formats.

**Future candidate ideas, explicitly not WP3 scope and recorded only so they
are not mistaken for it:** generalizing epoch protection to splits or
spin-offs; a provider-agnostic corporate-action price adapter; a persisted
quarantine state table; extending epoch namespacing to other cache families;
and replacing the current close source with a direct exchange feed. Each would
require separate approval under design §17.

## 12. Residuals carried into the WP3 planning freeze

These are recorded, not blocking:

- R6, the roadmap's naming of `backend/tests/test_fetch_history.py` as
  regression evidence, recorded for separately approved documentation
  correction. The roadmap is not amended by WP3.
- The R7 formal waiver (§6.7). The seven WP2 residuals remain undefined and
  unresolved; the waiver records only that no BANPU-WP3 obligation is inherited
  and binds WP3 alone.
- WP1's `backend/models/database.py` identity residual and the WP2 Step 8 gate
  language, carried forward unchanged and not reinterpreted.

The emitter-locus item referred out by PD-3 (§6.4) is **not** carried as a WP3
residual and creates no WP3 obligation. It is referred to the authority
governing the canonical design, roadmap, and package inventory.

## 13. Excluded effects

This plan does **not**:

- authorize implementation;
- allocate implementation authority;
- authorize release;
- modify any implementation file;
- amend the canonical design, roadmap, or implementation sequence;
- amend, reopen, or reinterpret WP1 or WP2, or any frozen artifact;
- resolve, weaken, or close any carried-forward residual;
- assign scope, work, or obligation to any package other than BANPU-WP3; or
- modify M46.

## 14. Exact next constitutional act

Gate S2 is satisfied. The exact next constitutional act is **BANPU-WP3 Planning
Confirmation**, followed by **Planning Freeze**, then **Allocation**.

This plan performs no part of any of those acts and creates no implementation
authority.
