# BANPU-WP6 — Work Package Plan

**Artifact class:** Implementation planning only
**Status:** `WORK PACKAGE PLAN MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN`
**Plan date:** 2026-08-17
**Issuing role:** BANPU-WP6 Work Package Planning Authority
**Work package:** `BANPU-WP6 — Shadow and succession-aware time-series continuity`
**Authority:** [BANPU-WP6 Implementation Authorization Record](BANPU_WP6_IMPLEMENTATION_AUTHORIZATION_RECORD.md), 18,660 bytes, 323 lines, SHA-256 `442426729C8D7582961CB0BA3B7706356995A39333662042C5BEA260B95BFD0F`, disposition `BANPU-WP6 IMPLEMENTATION AUTHORIZED`, over the scope bound by [BANPU-WP6 Allocation Record](BANPU_WP6_ALLOCATION_RECORD.md), 16,307 bytes, 282 lines, SHA-256 `208C2B236D669141BC947A96D82C5C249535E95EB54483C25496C1B6908D9D58`, disposition `BANPU-WP6 ALLOCATED`
**`MINOR-2` (WP3/WP5-owned) disposition in this plan:** `NOT WP6-OWNED — CARRIED FORWARD UNCHANGED, NOT PLANNED, NOT DISCHARGED` (§9)
**`POSITION_CONVERSION_REBUILD_BOUNDARY` disposition in this plan:** `NOT WP6-OWNED — CARRIED FORWARD UNCHANGED, NOT PLANNED, NOT DISCHARGED` (§9)
**Successor authority created:** `NONE`
**Release/deployment/production-mutation authority created:** `NONE`

This plan decomposes already-authorized implementation authority. It performs
no implementation. It creates no authority, no new gate, no new acceptance
criterion, no new capability, and no file surface beyond the surface the
Implementation Authorization Record already bound. Where this plan and the
frozen canonical corpus differ, the frozen corpus governs and this plan is in
error.

## 1. Purpose and constitutional position

### 1.1 Objective

Give the WP6-authorized scope — the narrow effective-dated `MERGED_INTO`
succession lookup, non-null asset IDs in affected holdings JSON, replay-time
shadow-holdings conversion at the boundary, paper fractional-share
preservation without broker cash-in-lieu, post-boundary valuation-subject
normalization preserving immutable source evidence, and boundary-bounded
persisted regeneration — a precise, reviewable implementation contract,
grounded in the live repository state rather than in the roadmap's "expected
files" forecast alone.

### 1.2 Constitutional position

This plan sits between BANPU-WP6's Implementation Authorization and its
future Implementation Review. It is subordinate to the Implementation
Authorization Record, the Allocation Record, and the frozen design, roadmap,
and sequence. It authorizes nothing; it decomposes what is already
authorized. A future Planning Confirmation and Planning Freeze remain
separate, later acts (§15), following the same lifecycle the WP5 Work
Package Plan used (`BANPU_WP5_PLANNING_CONFIRMATION.md`,
`BANPU_WP5_PLANNING_FREEZE_RECORD.md`).

## 2. Controlling authority

In descending order of scope, this plan is strictly subordinate to and does
not amend, reinterpret, or supersede:

1. the frozen canonical
   [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   especially §12 ("Derived accounting and identity continuity");
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md)
   §8 (BANPU-WP6 purpose, scope, expected files, explicit no-change surface,
   dependencies, deliverables, acceptance criteria, verification, size
   estimate);
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md) §8
   (Step 6 preconditions, repository state, expected code changes,
   verification, exit criteria);
4. [`BANPU_WP6_ALLOCATION_RECORD.md`](BANPU_WP6_ALLOCATION_RECORD.md),
   disposition `BANPU-WP6 ALLOCATED`; and
5. [`BANPU_WP6_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP6_IMPLEMENTATION_AUTHORIZATION_RECORD.md),
   disposition `BANPU-WP6 IMPLEMENTATION AUTHORIZED`, whose §3-§4 bind the
   exact scope and file surface this plan decomposes and whose §5-§8 bind
   the gates and residual treatment this plan must not relitigate.

This plan operationalizes already-authorized implementation detail. It does
not enlarge scope, create new architecture, reinterpret frozen design,
authorize additional files, create release/deployment authority, discharge
residuals, or alter predecessor governance.

## 3. Entry-state evidence

Independently re-verified against live repository bytes immediately before
drafting this plan, not accepted from prompt text:

| Item | Verification | Result |
|---|---|---|
| `BANPU_WP6_ALLOCATION_RECORD.md` | present, disposition `BANPU-WP6 ALLOCATED`, 16,307 bytes / 282 lines / SHA-256 `208C2B236D669141BC947A96D82C5C249535E95EB54483C25496C1B6908D9D58` | `EXACT` |
| `BANPU_WP6_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | present, disposition `BANPU-WP6 IMPLEMENTATION AUTHORIZED`, 18,660 bytes / 323 lines / SHA-256 `442426729C8D7582961CB0BA3B7706356995A39333662042C5BEA260B95BFD0F` | `EXACT` |
| Authorization bounded to exact allocated scope | Authorization Record §3 restates the Allocation Record §3 scope verbatim; no capability added | `CONFIRMED` |
| BANPU-WP6 implementation authorized but not started | Authorization Record §11: implementation `AUTHORIZED / NOT STARTED`; repository search found no WP6 production/test file from §4.1/§4.2 | `CONFIRMED` |
| No prior BANPU-WP6 Work Package Plan | `docs/implementation/` search: only `BANPU_WP6_ALLOCATION_RECORD.md` and `BANPU_WP6_IMPLEMENTATION_AUTHORIZATION_RECORD.md` exist under the `BANPU_WP6_*` naming; the `M39_WP6_*`/`M42_WP6_*`/`M43_WP6_*`/`M44_WP6_*`/`M44_G3_..._WP6_...` files belong to an unrelated milestone series and are not BANPU-WP6 artifacts | `CONFIRMED ABSENT` |
| No BANPU-WP6 implementation artifact or diff | `git status --porcelain=v1` shows only the two untracked BANPU-WP6 governance files; no file in Authorization Record §4.1/§4.2 exists | `CONFIRMED ABSENT` |
| No release/deployment/production-mutation authority | Authorization Record header and §10: `NONE` | `CONFIRMED` |
| BANPU-WP7+ not allocated/not authorized | Authorization Record §11: `NOT ALLOCATED / NOT AUTHORIZED` | `CONFIRMED` |
| Allocation Record and Authorization Record are the only current additive WP6 artifacts | Same repository search as above | `CONFIRMED` |
| Nothing staged | `git diff --cached --name-only` empty; `git status --porcelain=v1` shows only the two untracked files, both `??` | `CONFIRMED` |
| Roadmap §8 and Sequence §8 text | re-read live from both files | matches the Allocation/Authorization Records' restatement exactly |
| Design §12-14 text | re-read live from `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` | authoritative source for §7-§8 below |
| BANPU-WP5 Work Package Plan | read in full (605 lines) as structural and lifecycle precedent | used for §-numbering, task-table, blocked-task, and maturity-status conventions |
| Live repository implementation surfaces | `backend/services/decision_memory/shadow_tracker.py`, `attribution.py`, `backend/services/analytics/quant_engine.py`, `backend/services/evaluation/horizon_grader.py`, `ideal_series.py`, `backend/services/asset_registry.py`, `backend/services/asset_repository.py`, `backend/models/asset.py`, `backend/models/database.py` inspected directly (§6-§7) | grounds §7-§8 in actual code, not hypothetical architecture |
| `git status` overlap check | only the two BANPU-WP6 governance files untracked; no §4.1/§4.2 production or test file touched | `NO OVERLAPPING CHANGE` |

All premises match. No fail-closed condition exists. Planning proceeds; §8
records the mechanical-continuity determinations found during live-code
inspection. One item (§8 #14) was originally classified
`UNRESOLVED — REQUIRES SEPARATE CLARIFICATION` at materialization and was
later resolved to `MECHANICALLY DERIVABLE` by a separate, focused
independent interpretation act; §14.2 records that amendment.

## 4. Exact bounded scope

Restated exactly from Authorization Record §3, bound to capability IDs used
throughout this plan:

| ID | Authorized capability |
|---|---|
| WP6-C1 | Add a narrow, single-hop, effective-dated succession lookup using the existing `MERGED_INTO` relationship |
| WP6-C2 | Carry non-null asset IDs in affected holdings JSON (shadow, not just the WP5-closed real-portfolio surface) |
| WP6-C3 | Apply conversion to replay-time shadow holdings at the boundary |
| WP6-C4 | Keep paper fractional shares; do not apply broker cash-in-lieu treatment to hypothetical portfolios |
| WP6-C5 | Normalize post-boundary valuation subjects while preserving immutable source evidence |
| WP6-C6 | Restrict persisted regeneration to on/after the boundary |

Nothing in this plan adds a seventh capability or widens any of the six
above. `MINOR-2` and `POSITION_CONVERSION_REBUILD_BOUNDARY` are not WP6
capabilities (§9).

## 5. Authorized file surface

Restated exactly from Authorization Record §4. No file outside this table is
proposed by this plan.

### 5.1 Production surface

| File | Authorization basis |
|---|---|
| `backend/services/position_conversion.py` (new, narrow) | Authorization §4.1 permits this "only if strictly needed for pure succession/conversion helpers." §7.1 below establishes the need: five independent consumers require the identical effective-dated lookup, and duplicating it five times would violate ENGINEERING_PRINCIPLES.md "Reuse Before Create" — the same reasoning basis the WP5 Work Package Plan itself relied on |
| `backend/services/decision_memory/shadow_tracker.py` | Authorization §4.1 |
| `backend/services/decision_memory/attribution.py` | Authorization §4.1 |
| `backend/services/analytics/quant_engine.py` | Authorization §4.1 |
| `backend/services/evaluation/horizon_grader.py` | Authorization §4.1 |
| `backend/services/evaluation/ideal_series.py` | Authorization §4.1 |

No other new production file is authorized. `backend/services/asset_registry.py`,
`asset_repository.py`, `portfolio_transactions.py`, `portfolio_snapshots.py`
(WP4/WP5's frozen and closed surfaces) and `backend/services/analytics/attribution_engine.py`
(read-only reused by `horizon_grader.py` for `compute_max_drawdown` per that
file's own header) are read-only dependencies, not edit targets.

### 5.2 Test surface

| File | Role |
|---|---|
| `backend/tests/test_position_conversion.py` (new, if `position_conversion.py` is created) | Pure succession-lookup unit tests (§10) |
| `backend/tests/test_shadow_regeneration.py` | WP6-C2/C3/C4/C6 cases |
| `backend/tests/test_horizon_grader.py` | WP6-C1/C5 cases (directional-call continuity across a conversion) |
| `backend/tests/test_ideal_series.py` | WP6-C2/C5 cases |
| other focused tests strictly bounded to §5.1 files (e.g. an attribution- or quant-engine-scoped test module, only if §8's confirm-or-implement review finds a defect requiring one) | Authorization §4.2 "other corresponding focused tests strictly bounded to the capabilities in §3, for the files listed in §4.1" |

## 6. Implementation decomposition — overview

Live-code inspection (§7-§8) establishes that WP6 is not six independent,
equally-sized edits — it is one shared mechanism (a succession-lookup
helper) consumed by a small number of concrete call sites, most of which
either need a direct edit or can be shown at implementation time to already
inherit correctness once the shared mechanism exists. In dependency order:

1. **the shared succession-lookup mechanism** (§7.1) — new
   `position_conversion.py`. Every other item depends on this.
2. **shadow holdings-JSON identity carrying** (§7.2) — `shadow_tracker.py`.
   This is the capability-dense center of WP6: WP6-C2, WP6-C3, WP6-C4, and
   WP6-C6 are all decomposed here.
3. **horizon-grading cross-identity translation** (§7.3) —
   `horizon_grader.py`. A concrete, already-identified defect site for
   WP6-C1/WP6-C5.
4. **confirm-or-implement review of downstream consumers** (§7.4) —
   `attribution.py`, `quant_engine.py`, `ideal_series.py`. Each is either
   shown to already inherit correctness from item 2, or the narrow defect
   found is fixed — mirroring the WP5 Work Package Plan §13 pattern exactly
   ("if none is found, the capability is satisfied by the regression test
   alone with no source change, and implementation must record that finding
   rather than inventing an edit").

None of items 2-4 can begin before item 1 exists. Items 3 and 4 do not
depend on each other's implementation order.

## 7. Detailed mechanics

### 7.1 The succession-lookup mechanism (WP6-C1) — `position_conversion.py`

**Why in scope:** design §12 states "succession-aware lookups in quant,
attribution, shadow, horizon grading, and ideal-series consumers use the
effective-dated `MERGED_INTO` edge" — a single sentence naming five
consumers of one mechanism. Building it once and importing it five times is
the only reading consistent with "narrow" (Allocation/Authorization
Records' own repeated word) and with ENGINEERING_PRINCIPLES.md's
reuse-before-create rule.

**Exact responsibility:** given a starting identity (an `asset_id`, or a
symbol string for callers that do not yet carry `asset_id` — §7.2) and an
as-of date, return the identity that should be used for valuation/evaluation
purposes on that date: the predecessor's identity if no admissible
succession applies as of that date, or the successor's identity if one does.

**Inputs:** `db: Session`; either `asset_id: int` or `symbol: str`; `as_of_date: str` (naive calendar date, matching the `transaction_date`/`valuation_transition_date` convention `BANPU_WP5_WORK_PACKAGE_PLAN.md` §8 and design §6.3 already establish).

**Outputs:** the resolved `asset_id`, the resolved canonical symbol, and a
boolean `converted` flag (mirroring the shape WP4's
`prepare_position_conversion_registry` and WP5's admissibility functions
already use for caller ergonomics).

**Identity semantics:** built entirely from already-existing,
already-frozen registry primitives — `asset_repository.get_asset_by_canonical_symbol()`
(symbol → `Asset`, for callers that only carry a symbol),
`asset_registry.get_relationships()` / `asset_repository.get_relationships()`
(existing relationship read, already used by WP4's own
`execute_position_conversion()` and by its `RelationshipType.MERGED_INTO`
guard). WP6 adds no new registry primitive and no schema change — only a
read-only composition of what WP1/WP4 already built.

**Effective-date/boundary semantics:** the `AssetRelationship.effective_date`
column (`backend/models/asset.py` line 122, nullable `DateTime`) is the
field design §12 means by "effective-dated." A relationship whose
`effective_date` is `None` is not yet effective-dated and must not resolve
a successor (fail toward the predecessor, not toward an unproven
succession). Boundary inclusivity is `>=`: `as_of_date >= effective_date`
resolves to the successor; `as_of_date < effective_date` resolves to the
predecessor. This mirrors, rather than invents, the exact inclusivity
convention `BANPU_WP5_WORK_PACKAGE_PLAN.md` §8 and design §8.4 already use
for the identical boundary date family (`from_date >= earliest_transition_date`
admits; earlier refuses), and matches the Allocation/Authorization Records'
own phrase "on/after the boundary" for regeneration (§4).

**Interaction with predecessor/successor asset IDs:** single-hop only. The
lookup follows at most one outgoing `MERGED_INTO` edge from the starting
asset and does not walk a chain of successive conversions. This is a
deliberate scope boundary, not an oversight: (a) the Allocation and
Authorization Records both use the word "narrow" for this capability; (b)
`asset_registry.execute_position_conversion()`'s own `WP4-IIR-B3` guard
(lines 384-402) fail-closes on a predecessor asset acquiring a *second*
outgoing `MERGED_INTO` edge, which is the existing registry invariant that
makes single-hop resolution well-defined today; and (c) no canonical BANPU
artifact (design, Roadmap, Sequence, Allocation Record, Authorization
Record) discusses or requires chain-walking. A second, later conversion of
the same successor asset is out of this plan's scope; if it is ever needed,
that is a distinct future capability, not an inference this plan makes.

**Fractional precision:** the lookup itself returns identity only, not
quantity — it performs no share-count arithmetic. Quantity conversion is
entirely `shadow_tracker.py`'s responsibility (§7.2).

**Failure behavior:** never raises for an absent relationship — absence
means "no succession as of this date," which is the common case for every
non-converted asset and must be a normal, fast, silent path, not an
exception. Raises only if the caller-supplied `asset_id`/`symbol` does not
resolve to any `Asset` at all (mirrors `asset_registry.py`'s existing
`AssetRegistryError` pattern for an unknown asset).

**Idempotency/replay:** the function is a pure read with no side effect;
calling it any number of times with the same inputs against the same
registry state returns the same result. It performs no write, so it needs
no idempotency guard of its own — idempotency is instead a property of its
callers (§7.2, §8).

**Persistence boundaries:** reads only; writes nothing; opens no
transaction of its own.

**Explicit non-responsibilities:** does not create, modify, or retire any
`AssetRelationship`, `AssetIdentifier`, or asset lifecycle status (that
remains WP4's frozen `prepare_position_conversion_registry`/
`execute_position_conversion` surface); does not decide the boundary date
for a given conversion (that is read from the existing relationship's
`effective_date`, established upstream by WP4's registry preparation);
does not compute the conversion ratio or share quantities (§7.2); does not
touch `RecommendationSnapshot`, `OptimizerHistory`, `UserExecutionDecision`,
or `RecommendationGrade` (the Roadmap §8 / Authorization §10 no-change
surface).

### 7.2 Shadow holdings-JSON identity carrying (WP6-C2, WP6-C3, WP6-C4, WP6-C6) — `shadow_tracker.py`

**Why in scope:** live inspection found `ShadowPortfolio.inception_holdings_json`
and `ShadowPortfolioSnapshot.holdings_json` (`backend/models/database.py`
lines 521, 546) are both plain JSON text columns shaped
`[{symbol, shares, market_value, ...}]` with **no `asset_id` key at all**
today, and every read site found in `shadow_tracker.py` (e.g.
`item_symbols = [i.symbol for i in portfolio_items]` at line 776,
`_fetch_cached_prices(db, symbols)` at line 182, `_price_near_date`,
`_benchmark_return_pct`) is symbol-string-keyed. This is the file the
Roadmap names first, and live inspection confirms why: this is the only
module that actually constructs the shadow's own holdings JSON, so it is
the only place the "carry non-null asset ID" and "convert replay-time
holdings at the boundary" requirements can be satisfied structurally,
rather than papered over downstream.

**Exact responsibility:** when a holdings entry is built for
`inception_holdings_json` or a `ShadowPortfolioSnapshot.holdings_json` row,
resolve the holding's identity as of that row's date through §7.1's lookup,
and populate a new `asset_id` key (successor's `asset_id` on/after the
boundary, predecessor's `asset_id` before it) alongside the existing
`symbol` key (successor's symbol on/after the boundary). This is a JSON
*shape* enrichment inside an unchanged `Text` column — the same technique
`BANPU_WP5_WORK_PACKAGE_PLAN.md` §13 already used for
`PortfolioSnapshot.holdings_json` — not a schema, model, or migration
change.

**Inputs:** the real `PortfolioItem` row(s) a shadow is seeded or
replay-priced from (`PortfolioItem.asset_id`, nullable but populated for
BANPU-converted holdings by WP4's frozen write path — the same column
`BANPU_WP5_WORK_PACKAGE_PLAN.md` §13 already relies on for the real
portfolio's own holdings JSON), or, where replay works from a symbol alone
(most of `shadow_tracker.py`'s time-series replay functions), the symbol
resolved through §7.1's `get_asset_by_canonical_symbol` path; the row's own
valuation date.

**Outputs:** each holdings-JSON entry carries a non-null `asset_id` and the
identity-correct `symbol` for its own date.

**Identity semantics:** identical source of truth to WP5's — the
registry-bound `asset_id`, never a caller-controlled or display-only value.

**Effective-date/boundary semantics:** every date-bearing holdings entry
(inception and each daily snapshot) is resolved independently and
individually against §7.1 using its own `snapshot_date` (or
`created_at`/inception date for `inception_holdings_json`) — there is no
single portfolio-wide "before/after" flag; the boundary is evaluated
per-row, exactly mirroring how `portfolio_rebuilder.py`'s existing
`rebuild_dates` filtering already treats `from_date` per snapshot date
(`BANPU_WP5_WORK_PACKAGE_PLAN.md` §8) rather than as a portfolio-level
switch.

**Interaction with predecessor/successor asset IDs:** a pre-boundary
holdings entry keeps the predecessor's `asset_id`/`symbol` unchanged (this
plan adds a key; it does not touch pre-boundary numeric values, mirroring
design §12's "metadata-only enrichment... permitted only when hashes or
field comparisons prove all numeric values unchanged"). A post-boundary
entry carries the successor's `asset_id`/`symbol`.

**Treatment of fractional quantities (WP6-C4):** design §12 verbatim:
"Paper shares use the exact ratio and remain fractional; broker-specific
cash-in-lieu is not applied to hypothetical holdings. Shadow
`inception_price` is divided by the ratio to preserve inception value."
This is `FIXED BY CONTROLLING AUTHORITY` (§8) — the conversion ratio is
read from the same `PositionConversion.conversion_ratio` typed `Decimal`
value WP1/WP4 already parse and store (design §6.2's payload contract);
shadow-side share count becomes `predecessor_shares * conversion_ratio`
(exact `Decimal` arithmetic, no rounding to whole shares), and
`inception_price` becomes `predecessor_inception_price / conversion_ratio`.
No cash-in-lieu leg is read or applied for any shadow/hypothetical holding,
regardless of whether the real portfolio's conversion admitted one.

**Immutable evidence requirements:** identical to WP5's byte-exact
preservation obligation, applied to the shadow's own persisted rows —
every `ShadowPortfolioSnapshot` row whose date is before a holding's
resolved boundary must remain unchanged by this capability; only rows
on/after the boundary may carry the enriched, successor-resolved entry.

**Failure behavior:** if §7.1 cannot resolve a symbol to any `Asset` at
all (a genuinely unregistered symbol), the existing pre-WP6 behavior is
preserved unchanged (symbol-only entry, no `asset_id` key) rather than
raising — WP6 must not turn an unrelated, non-BANPU shadow holding's normal
valuation into a hard failure. This is the fail-open counterpart to §7.1's
fail-closed non-resolution: absence of a *conversion* is silent (§7.1);
absence of an *asset row* for an unrelated symbol is likewise silent here,
and only an internal invariant violation (a resolved successor `Asset`
itself missing) would be a defect.

**Idempotency/replay expectations:** `MECHANICALLY DERIVABLE — CONTRACT B
REQUIRED` (§8 #14, amended). Shadow regeneration must be safe to repeat:
rerunning a boundary-bounded regeneration against unchanged canonical
inputs (the same `AssetRelationship`/`effective_date` state and the same
underlying transaction ledger) must converge persisted business fields
(shares, prices, `asset_id`, symbol, market value) to the same result the
first successful run produced. Repeated execution must not compound the
conversion ratio a second time, and must not create duplicate or orphan
`ShadowPortfolioSnapshot` rows. This does not relax the pre-boundary
protection this section already establishes — a rerun remains bound by the
same pre-boundary-row-unchanged rule as a first run. An upsert-by-date
strategy (or an equivalent persistence approach that reaches the same
converged state) satisfies this requirement; a literal no-write/byte-
identical rerun (unchanged timestamps, no row touched at all) is **not**
required and is not to be implemented as if it were. See §8 #14 for the
controlling basis.

**Persistence boundaries (WP6-C6):** `_rebuild_shadow_snapshots`,
`regenerate_static_shadow`, and `regenerate_active_model_shadow` (lines
1148, 1463, 1707) are the only functions in this file that write
`ShadowPortfolioSnapshot` rows during regeneration. Each must gain the same
class of guard `BANPU_WP5_WORK_PACKAGE_PLAN.md` §8 designed for
`portfolio_rebuilder.py`: replay may read/compute from inception in memory
(design §12: "Regeneration may replay from inception in memory"), but no
write to a pre-boundary row's persisted fields may occur, and the write
loop must skip persisting any recomputed value for a date earlier than the
resolved boundary for a shadow holding a converted asset. Design §12's own
sentence — "writes only rows on or after the boundary and proves
pre-boundary rows unchanged" — is the acceptance target (§10).

Per the amended §8 #14 determination, all three functions must also satisfy
Contract B on rerun. `_rebuild_shadow_snapshots` and
`regenerate_active_model_shadow` already document an upsert-by-date pattern,
which is compatible with Contract B on its face. `regenerate_static_shadow`,
by contrast, was found at live-code inspection to perform a bulk `.delete()`
of existing `ShadowPortfolioSnapshot` rows before regenerating (line 1407)
— a delete-then-recreate pattern rather than an upsert. This is recorded
here as a specific **implementation-time compliance point to inspect**
(does the delete/recreate sequence, combined with the boundary guard above,
still converge to the same persisted state on rerun without a window in
which rows are transiently missing or without recreating a pre-boundary row
outside the guard) — not as a planning blocker, and not as authority to
redesign `regenerate_static_shadow`'s behavior beyond what WP6-C6 already
requires.

**Explicit non-responsibilities:** does not decide *whether* a conversion
happened (§7.1's job); does not touch `PortfolioItem`, `PortfolioSnapshot`,
or `portfolio_rebuilder.py` (WP4/WP5's closed surfaces); does not perform
any production shadow regeneration (§11); does not implement the
tolerance-admissibility or reconciliation logic of `MINOR-2` (WP3/WP5-owned,
§9).

### 7.3 Horizon-grading cross-identity translation (WP6-C1, WP6-C5) — `horizon_grader.py`

**Why in scope:** live inspection of `score_directional_calls` (lines
63-126) found a concrete defect site, not a hypothetical one.
`inception_holdings` is keyed by the symbol frozen at recommendation time
(line 98, `sym = h.get("symbol")` — the immutable predecessor symbol per
design §12's "source recommendations... retain their original symbols and
are never rewritten"). `horizon_holdings_json` is read from a later
`ShadowPortfolioSnapshot` row (line 88-90,
`horizon_holdings = {h["symbol"]: h for h in json.loads(horizon_holdings_json)...}`).
Once §7.2 makes a post-boundary shadow snapshot carry the successor's
symbol, an exact-string match at line 103
(`horizon = horizon_holdings.get(sym)`) silently returns `None` for any
recommendation whose holding converted before its horizon date — the call
falls into the existing `if not entry_price or not horizon_price...:
continue` branch (lines 105-106) and is silently excluded from the
directional-call count, not reported as an error. This is exactly the
"recommendations retain original evidence while post-boundary evaluation
follows the successor" requirement (Authorization Record §7) failing
silently without this fix.

**Exact responsibility:** before matching, translate each inception
holding's frozen symbol forward through §7.1's lookup, using the horizon
snapshot's own date as the as-of date, and match against
`horizon_holdings_json` using the translated (possibly successor) symbol.
The frozen `inception_holdings` entry itself — its stored symbol, action,
and `inception_price` — is never rewritten (design §12, Authorization §7);
only the *lookup key* used to find the matching horizon entry changes.

**Inputs/outputs:** unchanged function signature
(`score_directional_calls(inception_holdings, horizon_holdings_json)`) plus
the horizon date already available to its caller
(`grade_due_recommendations`, via the graded horizon's target date) and a
`db: Session` the pure-function docstring (line 69, "Pure function — no DB
access") currently promises it does not need — this is the one place §7.1's
introduction changes an existing contract, and is recorded here explicitly
rather than silently: `score_directional_calls` becomes DB-touching (a
single read through §7.1) or its caller pre-resolves the translated symbol
map before calling it, preserving purity. Either is a legitimate
implementation choice within this plan's scope; §14 leaves the choice to
implementation, not to invented planning specificity.

**Identity/boundary semantics:** identical to §7.1/§7.2, applied per
recommendation rather than per shadow.

**Failure behavior:** if translation finds no admissible succession (the
overwhelmingly common case — most recommendations never involve a
conversion), behavior is byte-identical to today's code — no behavior
change for the non-converted path is an explicit regression requirement
(§11).

**Explicit non-responsibilities:** does not change `RecommendationGrade`
schema or `grade_due_recommendations`'s append-only, at-most-once grading
contract (module docstring lines 13-17); does not change
`_sps_at_or_before`'s existing on/before nearest-snapshot semantics.

### 7.4 Confirm-or-implement review of downstream consumers (WP6-C1, WP6-C5) — `attribution.py`, `quant_engine.py`, `ideal_series.py`

Live inspection found these three files' relevant functions consume
already-materialized shadow/portfolio snapshot data rather than performing
independent symbol-to-identity resolution of their own, so each is either
already correct once §7.2 lands, or needs a narrow, specific fix — not a
speculative rewrite. This plan records what live inspection found for each
and defers the final determination to implementation-time confirmation,
exactly as `BANPU_WP5_WORK_PACKAGE_PLAN.md` §13 did for its own successor-
identity capability ("if none is found, the capability is satisfied by the
regression test alone with no source change, and implementation must record
that finding rather than inventing an edit").

- **`quant_engine.py::calculate_buy_win_rate` / `calculate_sell_accuracy`**
  (lines 640-739): use `sig.symbol` only as a display label in the returned
  `details` list; the win/loss determination itself compares aggregate
  portfolio-level snapshot values (`_snap_value_map`, `_value_at_or_after`),
  not per-holding prices keyed by symbol. Preliminary finding: **no source
  change required** — implementation must confirm this by live re-reading
  immediately before starting §12's T-tasks, and if confirmed, the
  capability is satisfied for this file by a regression test proving an
  unchanged win/loss classification across a synthetic conversion fixture,
  per the same file-allowlist discipline WP5 used.
- **`ideal_series.py::_revalue_ai_portfolio_with_canonical_prices`** (lines
  345-423): reads holdings symbols from `ShadowPortfolioSnapshot.holdings_json`
  (§7.2's output) and looks up canonical prices from `history`
  (`_snapshot_price_history`, sourced from `PortfolioSnapshot.holdings_json`,
  already successor-symbol-correct per WP5's closed scope) using the same
  symbol as the join key. Preliminary finding: **likely inherits
  correctness once §7.2 lands**, because both sides of the join transition
  to the successor symbol at the identical boundary date once shadow's own
  holdings JSON is fixed. Implementation must confirm the two boundary
  dates are in fact identical (both ultimately trace to the same
  `transaction_date`/`valuation_transition_date`) rather than assume it;
  if a live gap is found, that gap — not a general rewrite — is the narrow
  defect this capability closes.
- **`attribution.py::compute_attribution` / `_portfolio_sector_return`**:
  consumes shadow-snapshot-derived series and `sector` fields, not symbols,
  for its return comparison. Preliminary finding: **likely inherits
  correctness once §7.2 lands**, on the same reasoning as `ideal_series.py`.
  Implementation must confirm no symbol-keyed join exists inside this file
  that §7.2 does not already cover.

No test file is authorized for these three files beyond Authorization §4.2's
"other corresponding focused tests strictly bounded to the capabilities in
§3" — if confirm-or-implement finds no defect, no new test file for that
specific module is required beyond the regression coverage in §11.

## 8. Mechanical-continuity / ambiguity determination

| # | Implementation-critical behavior | Classification | Basis |
|---|---|---|---|
| 1 | Effective-dated succession lookup uses `AssetRelationship.effective_date`, not `created_at` or any other field | `FIXED BY CONTROLLING AUTHORITY` | Design §12 verbatim ("effective-dated `MERGED_INTO` edge") |
| 2 | Boundary date inclusivity is `>=` (boundary day itself resolves to successor) | `MECHANICALLY DERIVABLE` | Direct structural analogy to design §8.4 / `BANPU_WP5_WORK_PACKAGE_PLAN.md` §8's already-accepted `from_date >= earliest_transition_date` convention for the identical date family, and the Allocation/Authorization Records' own "on/after the boundary" phrase |
| 3 | Succession lookup is single-hop only (no chain-walking through a successor that later converts again) | `FIXED BY CONTROLLING AUTHORITY` (bounded) | Allocation/Authorization Records' repeated word "narrow"; `asset_registry.py`'s `WP4-IIR-B3` guard against a second outgoing `MERGED_INTO` edge; no canonical artifact discusses or requires chain-walking |
| 4 | An `AssetRelationship` with `effective_date IS NULL` does not resolve a successor | `MECHANICALLY DERIVABLE` | Fail-closed design principle (design §4.8, applied by the WP5 precedent's own fail-closed reasoning); an un-dated relationship is not yet "effective-dated" per design §12's own qualifier |
| 5 | Fractional share/inception-price conversion arithmetic for shadow holdings | `FIXED BY CONTROLLING AUTHORITY` | Design §12 verbatim (§7.2 above) |
| 6 | No broker cash-in-lieu applied to hypothetical/shadow holdings | `FIXED BY CONTROLLING AUTHORITY` | Design §12 verbatim |
| 7 | Immutable source evidence: original recommendation/decision symbols never rewritten | `FIXED BY CONTROLLING AUTHORITY` | Design §12 verbatim; Authorization §7 |
| 8 | Persisted shadow regeneration writes only rows on/after the boundary; pre-boundary rows unchanged | `FIXED BY CONTROLLING AUTHORITY` | Design §12 verbatim; Authorization §7 |
| 9 | Per-row (not portfolio-wide) boundary evaluation for holdings-JSON identity | `MECHANICALLY DERIVABLE` | Direct structural analogy to `portfolio_rebuilder.py`'s existing per-date `rebuild_dates` filtering (`BANPU_WP5_WORK_PACKAGE_PLAN.md` §8) |
| 10 | Symbol-to-`asset_id` resolution reuses `asset_repository.get_asset_by_canonical_symbol()` rather than a new resolver | `MECHANICALLY DERIVABLE` | Function already exists and is the only canonical-symbol resolver found in the registry surface; no second resolver is evidenced or needed |
| 11 | `horizon_grader.py`'s cross-identity translation site and failure-mode (silent exclusion) | `FIXED BY CONTROLLING AUTHORITY` (defect identified) | Direct live-code read of `score_directional_calls` lines 88-106 (§7.3) |
| 12 | `quant_engine.py` / `ideal_series.py` / `attribution.py` exact final disposition (source change vs. regression-test-only) | `MECHANICALLY DERIVABLE, PENDING IMPLEMENTATION-TIME CONFIRMATION` | Preliminary live-code finding recorded in §7.4; final determination deferred to implementation per the WP5 §13 precedent, not a planning blocker — non-determination here does not block any other WP6-C item |
| 13 | Reading `PortfolioItem.asset_id` (a column its own `backend/models/database.py` line 127-131 comment marks "nothing reads this column yet (Stage 5 native cutover)" in the general, non-BANPU runtime) directly, without routing through the M29/M30 capability-safety consultation path | `MECHANICALLY DERIVABLE` (not gated) | `BANPU_WP5_WORK_PACKAGE_PLAN.md` §13 already read this exact column directly, for the closed and accepted WP5 scope, with no M29/M30 gate invoked or required; no BANPU governance artifact (design, Roadmap, Sequence, Allocation Record, Authorization Record) references the M29/M30 capability-safety track at all. This plan follows the same accepted precedent rather than inventing a new cross-track dependency BANPU governance never established |
| 14 | Idempotent rerun of WP6's persisted regeneration (does a second run of the boundary-bounded shadow regeneration converge to the same persisted business state as the first run) | `MECHANICALLY DERIVABLE` — `CONTRACT B REQUIRED`; `CONTRACT C NOT REQUIRED` | Design §13 step 6 defines "rebuild" for this corpus as covering "portfolio **and shadow** rows"; design §13's closing sentence requires the enumerated rebuild commands to be "safe to repeat"; the identical clause's sibling half (portfolio rebuild) is realized in WP5's accepted, frozen `portfolio_rebuilder.py` as persistence-state idempotency via an upsert pattern ("running twice = same state," module docstring Stage 9) — not as a byte-identical/zero-write rerun. No controlling authority (design, Roadmap §8, Sequence Step 6, Allocation Record, Authorization Record) states or implies a byte-identical/zero-mutation requirement (Contract C); the corpus's only realized precedent for this exact clause achieves Contract B, not C. See §7.2 for the resulting requirement statement |

Per item 12, implementation may proceed on every WP6-C item without waiting
for item 12's confirmation step, because item 12's possible outcomes (no
source change, or a narrow specific fix) are both already bounded by §5.1's
file surface and do not affect §7.1/§7.2/§7.3's design. Per item 14 as
amended, implementation of WP6-C3/C6's regeneration guard proceeds under a
single, already-derived contract — Contract B — for both the first run and
any subsequent rerun; the acceptance-matrix row this determination was
blocking is un-blocked in §10 below. No implementation-critical ambiguity
remains open in this table.

## 9. Residual treatment

Preserved exactly, without definition, resolution, waiver, or
reinterpretation:

| Item | Carried state |
|---|---|
| `MINOR-2` (WP3/WP5-owned) | Not a WP6 capability. `BANPU_WP1_FREEZE_RECORD.md` §7 names WP3/WP5 as sole owners; `BANPU_WP5_EPIC_CLOSEOUT.md` §13 classification (`TECHNICALLY SATISFIED — CARRIED FORWARD; NOT DISCHARGED`) is unchanged by this plan. WP6 implementation does not touch it merely because WP6 also implements boundary-sensitive behavior — WP6's boundary is the shadow/derived-series boundary (§7.2), a distinct mechanism from WP5's mechanical-NAV-continuity-tolerance boundary |
| `POSITION_CONVERSION_REBUILD_BOUNDARY` (WP5-owned) | Not a WP6 capability. `BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md` finding catalogue names WP5 as sole owner; `BANPU_WP5_EPIC_CLOSEOUT.md` §14 classification unchanged. WP6's own, separate "regeneration bounded to on/after the boundary" (WP6-C6, §7.2) is a distinct capability using the same date family but is not this residual and does not discharge it |
| `PD-3` | Unassigned, open, referred out per `BANPU_WP5_EPIC_CLOSEOUT.md` §15. This plan does not claim or assign it to WP6 |
| `MINOR-1`, `NEW-MINOR-A` | WP4-owned, closed; untouched by WP6 |
| `MINOR-5` | WP7 rehearsal / WP8 release evidence; untouched by WP6 |
| WP2 `MINOR-A`, `MINOR-B`, `OBSERVATION-A` | Carried unchanged, no obligation text invented |
| WP3 `OBSERVATION-IC-1`, `OBSERVATION-IC-2`, `OBSERVATION-SR-1`, `OBSERVATION-SR-2` | Carried unchanged, non-blocking |
| WP4's baseline missing-log assertion, temporary-path permission condition, `B1`-`B6`, `RTO-1`-`RTO-13`, `PIA-1`-`PIA-4` | Carried forward at BANPU-WP4 Epic Closeout unchanged |

This plan creates no residual-discharge authority. Ambiguity #14 (§8) was
resolved by a separate, focused independent interpretation act and is no
longer a WP6-owned open planning item as of this amendment; it is not a
residual and was never carried as one — it is removed from this table
because it no longer exists as an open item, not because any residual
disposition changed. WP6-owned open items after this amendment are —
until implementation actually occurs — every capability in §4, and nothing
else.

## 10. Acceptance matrix

| ID | Criterion | Governing source | Expected test/evidence surface | Status during planning |
|---|---|---|---|---|
| WP6-A1 | Succession lookup correctness (predecessor before boundary, successor at/after) | Design §12; §7.1, §8 #1-#4 | `test_position_conversion.py` (new) | Not evaluated — implementation-time |
| WP6-A2 | Effective-date correctness (unset `effective_date` never resolves a successor) | §8 #4 | `test_position_conversion.py` | Not evaluated |
| WP6-A3 | Predecessor/successor identity continuity across the boundary in holdings JSON | Design §12; §7.2 | `test_shadow_regeneration.py` | Not evaluated |
| WP6-A4 | Holdings-JSON asset-ID completeness (non-null `asset_id` on every affected entry) | Roadmap §8; §7.2 | `test_shadow_regeneration.py` | Not evaluated |
| WP6-A5 | Shadow replay conversion applies the same schedule as the real portfolio | Design §12; §7.2 | `test_shadow_regeneration.py` | Not evaluated |
| WP6-A6 | Paper fractional-share preservation (exact ratio, no rounding to whole shares) | Design §12; §7.2 | `test_shadow_regeneration.py` | Not evaluated |
| WP6-A7 | No broker cash-in-lieu semantics applied to hypothetical/shadow holdings | Design §12; §7.2 | `test_shadow_regeneration.py` | Not evaluated |
| WP6-A8 | Shadow inception/NAV value conserved (inception_price / ratio) | Design §12; §7.2 | `test_shadow_regeneration.py`, reusing `assert_nav_conserved` | Not evaluated |
| WP6-A9 | Attribution continuity | Roadmap §8; §7.4 | confirm-or-implement result — `attribution.py`-scoped test only if a defect is found | Not evaluated |
| WP6-A10 | Horizon/evaluation continuity (converted holding's directional call remains evaluable) | Authorization §7; §7.3 | `test_horizon_grader.py` | Not evaluated |
| WP6-A11 | Valuation-subject normalization post-boundary | Design §12; §7.2, §7.4 | `test_shadow_regeneration.py`, `test_ideal_series.py` | Not evaluated |
| WP6-A12 | Immutable source-evidence preservation (recommendation/decision symbols never rewritten) | Design §12; Authorization §7 | regression assertion across `test_horizon_grader.py` and existing `RecommendationSnapshot`/`UserExecutionDecision` fixtures (read-only check, no write) | Not evaluated |
| WP6-A13 | Regeneration boundary enforcement (no pre-boundary row write) | Design §12; §7.2 | `test_shadow_regeneration.py`, byte/field comparison per WP5's §9 precedent | Not evaluated |
| WP6-A14 | Regeneration rerun convergence: a repeated boundary-bounded shadow regeneration against unchanged canonical inputs converges persisted business fields to the same first-run result, does not compound the conversion ratio, creates no duplicate/orphan `ShadowPortfolioSnapshot` rows, and preserves WP6-A13's pre-boundary protection | Design §13 (step 6, closing sentence); §7.2; §8 #14 | `test_shadow_regeneration.py`, focused rerun-comparison fixture (run regeneration twice, compare persisted business fields) | Not evaluated |
| WP6-A15 | Unrelated-symbol non-remapping | Roadmap §8; §7.2, §7.3 | regression fixture with a non-converted symbol, unaffected | Not evaluated |
| WP6-A16 | Absence of a generalized corporate-action framework or event vocabulary | Roadmap §8; §5.1 file surface itself | diff review against §5.1 at implementation review | Not evaluated |
| WP6-A17 | No forbidden schema/write-path change (`RecommendationSnapshot`, `OptimizerHistory`, `UserExecutionDecision`, `RecommendationGrade`, transaction schema/write path) | Roadmap §8; Authorization §10 | diff review; regression suite for those modules stays green and untouched | Not evaluated |
| WP6-A18 | No M46 modification | Authorization §10 | diff review | Not evaluated |

Every row is plannable; none is blocked. `WP6-A14` was un-blocked from a
prior `WP6-BLOCKED` placeholder by the amended §8 #14 determination
(`MECHANICALLY DERIVABLE`, Contract B required). No criterion above is
marked `PASS` by this plan — planning materializes the matrix; it does not
execute it.

## 11. Verification strategy

Implementation must keep green, unmodified in expectation:

- `backend/tests/test_shadow_regeneration.py`, `test_horizon_grader.py`,
  `test_ideal_series.py` (pre-existing cases)
- `backend/tests/test_portfolio_metrics.py`, `test_portfolio_rebuilder.py`,
  `test_verify_snapshots.py` (WP5's frozen surface — proves WP6 did not
  reach into WP5's closed files)
- `backend/tests/test_asset_registry.py`, `test_position_conversion_live.py`,
  `test_transaction_canonicalizer.py` (WP4's frozen surface — proves WP6
  did not edit the registry write path)
- `backend/tests/test_position_conversion_quote_contract.py` (WP3's frozen
  surface)

New/added coverage must satisfy §10's acceptance matrix in full.
`graphify update .` must be run before implementation review,
per the top-level CLAUDE.md rule (this plan is documentation-only and does
not itself trigger that rule — see §14 verification table).

## 12. Explicit exclusions

This plan does not decompose, and WP6 implementation may not perform:

- any change to `backend/main.py`, any public endpoint, operator CLI, or
  frontend authoring path (Roadmap §8; CLI wiring is BANPU-WP7 work per
  `portfolio_transactions.py` line 950's own comment);
- any schema, model, or migration change, including no new column on
  `ShadowPortfolio`, `ShadowPortfolioSnapshot`, `PortfolioItem`, or any
  asset table — §7.2's JSON-shape enrichment is explicitly not a schema
  change and must not become one;
- any change to `RecommendationSnapshot`, `OptimizerHistory`,
  `UserExecutionDecision`, or `RecommendationGrade` schema, or any
  mutation/rewrite of a historical recommendation or decision payload;
- any change to `backend/services/asset_registry.py`, `asset_repository.py`,
  `portfolio_transactions.py`, `asset_registry.py`'s `execute_position_conversion`,
  `transaction_canonicalizer.py`, `portfolio_rebuilder.py`, or
  `portfolio_snapshots.py` (WP3/WP4/WP5's frozen and closed surfaces);
- any actual production shadow regeneration, snapshot rebuild, repair,
  repricing, or cache purge;
- inventing an implementation-time resolution to any *future* planning
  ambiguity this plan has not itself resolved through a governed
  interpretation act, and implementing as if it were settled;
- resolving, narrowing, discharging, or waiving `MINOR-2`,
  `POSITION_CONVERSION_REBUILD_BOUNDARY`, `PD-3`, or any other residual
  (§9);
- introducing a general corporate-action dispatcher or event vocabulary, or
  expanding the general asset-definition vocabulary;
- remapping any unrelated symbol;
- any BANPU-WP7, WP8, or M46 act;
- production deployment or deployment authorization; and
- staging, committing, pushing, merging, or publishing repository changes
  under color of this plan.

## 13. Implementation sequencing

| Task | Work | Depends on | Deliverable / evidence |
|---|---|---|---|
| WP6-T1 | Record entry baseline: repository state, frozen WP1-WP5 identities, test commands, pre-existing failures, §5 file allowlist | Authorization | Reproducible entry-gate record |
| WP6-T2 | Author failing tests WP6-A1, WP6-A2 (succession lookup) | T1 | Obligations expressed before code |
| WP6-T3 | Implement `position_conversion.py` (§7.1) | T2 | WP6-C1 mechanism |
| WP6-T4 | Author failing tests WP6-A3-A8, WP6-A13, WP6-A14, WP6-A15 (shadow holdings identity, fractional shares, boundary enforcement, regeneration rerun convergence) | T1 | Obligations expressed before code |
| WP6-T5 | Implement `shadow_tracker.py` holdings-JSON identity carrying, regeneration boundary guard, and rerun-convergence (Contract B) compliance across `_rebuild_shadow_snapshots`, `regenerate_static_shadow`, and `regenerate_active_model_shadow` (§7.2) | T3, T4 | WP6-C2, WP6-C3, WP6-C4, WP6-C6; WP6-A14 satisfied |
| WP6-T6 | Author failing test WP6-A10 (horizon directional-call continuity) | T1 | Obligation expressed before code |
| WP6-T7 | Implement the `horizon_grader.py` cross-identity translation (§7.3) | T3, T6 | WP6-C1 applied, WP6-C5 (horizon leg) |
| WP6-T8 | Live-code confirm-or-implement pass on `quant_engine.py`, `ideal_series.py`, `attribution.py` (§7.4) | T5 | WP6-C5 (remaining legs); record finding whether source change was needed |
| WP6-T9 | Author WP6-A9, WP6-A11 tests reflecting T8's finding | T8 | Obligation expressed before any T8 source change |
| WP6-T10 | Author WP6-A12, WP6-A16, WP6-A17, WP6-A18 regression/negative tests | T1 | Obligations expressed before code |
| WP6-T11 | Run the full §10 matrix and the §11 regression suites; `graphify update .` | T3, T5, T7, T8, T9, T10 | Complete WP6 evidence set |
| WP6-T12 | Prepare the independent implementation-review submission | T11 | Review-ready candidate; no confirmation, freeze, or closeout performed |

No task in this table is conditional or blocked. The prior `WP6-T11`
(submitting ambiguity #14 for a separate clarification act) is removed by
this amendment: §8 #14 was resolved by a governed interpretation act before
this amendment was made, so no clarification task remains to schedule.
Rerun-idempotency test authoring is folded into `WP6-T4`; rerun-idempotency
implementation compliance is folded into `WP6-T5`, the corresponding
shadow-regeneration implementation task.

## 14. WPP maturity/status

`WORK PACKAGE PLAN MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT
PERFORMED — NOT CONFIRMED — NOT FROZEN`, using the exact maturity
terminology `BANPU_WP5_WORK_PACKAGE_PLAN.md` established as valid BANPU
precedent (its own header, line 4). This plan does not claim confirmation
or freeze merely because it has been materialized, and it does not claim
confirmation, approval, freeze, or implementation-readiness merely because
§14.2's amendment corrected one planning interpretation. Any required
confirmation, binding, or freeze remains a separate, later act.

### 14.1 Repository verification of this planning act

| Verification | Result |
|---|---|
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP6_WORK_PACKAGE_PLAN.md` |
| Allocation Record or Implementation Authorization Record modified | `NONE` |
| Frozen BANPU artifacts modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX files modified | `NONE` — all live-code reads in §6-§8 were read-only inspection |
| Trailing-whitespace verification | see final report |
| `git diff --check` | see final report |
| `git diff --cached --check` | see final report |
| `graphify update .` | not run — documentation-only additive act, no code changed, mirroring the WP5 Epic Closeout §21 waiver logic |
| Final `git status --porcelain=v1` | see final report |
| Commit created | `NO` |

### 14.2 Amendment record

| Item | Value |
|---|---|
| Amendment date | 2026-08-18 |
| Controlling interpretation | Separate, focused, independent, read-only constitutional interpretation of ambiguity #14, resolving it to `WP6-IDEMPOTENCY MECHANICALLY DERIVABLE FROM CONTROLLING AUTHORITY` (Contract B required; Contract C not required) |
| Sections amended | §7.2 (idempotency/replay expectations; persistence-boundaries compliance note), §8 (item #14 reclassification and closing note), §9 (removal of ambiguity #14 as an open item), §10 (WP6-BLOCKED replaced by WP6-A14; WP6-A14–A17 renumbered to WP6-A15–A18), §13 (WP6-T4/T5/T10 updated; blocked WP6-T11 removed; matrix/review tasks renumbered WP6-T11/T12), §14 (stale forward-reference removed), §15 (two-track successor collapsed to one), §3 (closing sentence updated to reflect this amendment) |
| Sections NOT amended | §1, §2, §4, §5, §6, §7.1, §7.3, §7.4 (substance unchanged — only acceptance-ID cross-references adjusted where renumbering required it), §11 (only the `WP6-BLOCKED` exception phrase removed), §12 (only the stale ambiguity-#14 bullet reworded) |
| Effect on the six authorized WP6 capabilities, authorized file surface, implementation decomposition, horizon-grader finding, confirm-or-implement treatment, residual ownership, release/deployment boundaries, and WP7+ state | `NONE — UNCHANGED` |
| Effect on WPP maturity | `NONE` — remains `MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN`; this amendment is not a confirmation, approval, freeze, or implementation-readiness determination |

## 15. Exact next constitutional act

A single next constitutional act follows from this plan as amended:
**BANPU-WP6 Planning Confirmation** (the repository's established
equivalent — see `BANPU_WP5_PLANNING_CONFIRMATION.md` — performed by a
reviewer distinct from this planning authority), covering the full §10
acceptance matrix, including the now-unblocked `WP6-A14`. The prior
two-track successor structure (a separate clarification act for ambiguity
#14) no longer applies, because §8 #14 was resolved before this amendment
was made.

This plan performs neither Planning Confirmation nor Planning Freeze.
