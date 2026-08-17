# BANPU-WP5 — Work Package Plan

**Artifact class:** Implementation planning only
**Status:** `WORK PACKAGE PLAN MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN`
**Plan date:** 2026-08-14
**Issuing role:** BANPU-WP5 Work Package Planning Authority
**Work package:** `BANPU-WP5 — Accounting readers and bounded reconstruction`
**Authority:** [BANPU-WP5 Implementation Authorization Record](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md), 19,039 bytes, 341 lines, SHA-256 `DBCBC2BFCDB9F3A7D3E7912C6148445C68C39F5872A4DE2DEF58DF5B2BDE7F1E`, disposition `BANPU-WP5 IMPLEMENTATION AUTHORIZED`, over the scope bound by [BANPU-WP5 Allocation Record](BANPU_WP5_ALLOCATION_RECORD.md)
**`MINOR-2` (WP5 half) disposition in this plan:** `PARTIALLY PLANNABLE — TOLERANCE ADMISSIBILITY READY; RECONCILIATION FORMULA BLOCKED AT A PLANNING BOUNDARY` (§10)
**`POSITION_CONVERSION_REBUILD_BOUNDARY` disposition in this plan:** `READY — FULLY DECOMPOSED` (§8)
**Successor authority created:** `NONE`
**Release/deployment/production-mutation authority created:** `NONE`

This plan decomposes already-authorized implementation authority. It performs no
implementation. It creates no authority, no new gate, no new acceptance
criterion, no new capability, and no file surface beyond the surface the
Implementation Authorization Record already bound. Where this plan and the
frozen canonical corpus differ, the frozen corpus governs and this plan is in
error.

## 1. Purpose and constitutional position

### 1.1 Objective

Give the WP5-authorized scope — accounting-reader classification of
`POSITION_CONVERSION`, the `from_date` bounded-reconstruction boundary, and
boundary-aware snapshot verification — a precise, reviewable implementation
contract, grounded in the live repository state rather than in the roadmap's
"expected files" forecast alone.

### 1.2 Constitutional position

This plan sits between BANPU-WP5's Implementation Authorization and its
future Implementation Review. It is subordinate to the Implementation
Authorization Record, the Allocation Record, and the frozen design, roadmap,
and sequence. It authorizes nothing; it decomposes what is already
authorized. A future Planning Confirmation and Planning Freeze remain
separate, later acts (§19).

## 2. Verified entry state and prerequisites

Independently re-verified, not accepted from prompt text, immediately before
drafting this plan:

| Item | Verification | Result |
|---|---|---|
| `BANPU_WP5_ALLOCATION_RECORD.md` | present, disposition `BANPU-WP5 ALLOCATED`, 15,590 bytes / 280 lines / SHA-256 `D00D0AE886E6150F84663AA331338F764E193700EBCE944C88CB0D175CA8D687` | `EXACT` |
| `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | present, disposition `BANPU-WP5 IMPLEMENTATION AUTHORIZED`, 19,039 bytes / 341 lines / SHA-256 `DBCBC2BFCDB9F3A7D3E7912C6148445C68C39F5872A4DE2DEF58DF5B2BDE7F1E` | `EXACT` |
| No prior BANPU-WP5 Work Package Plan | `docs/implementation/` search: only `BANPU_WP5_ALLOCATION_RECORD.md` and `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md` existed under the `BANPU_WP5_*` naming; the `M39_WP5_*`/`M40_WP5_*`/`M42_WP5_*`/`M44_WP5_*` files belong to an unrelated milestone series and are not BANPU-WP5 artifacts | `CONFIRMED ABSENT` |
| Roadmap §7 (BANPU-WP5) text | re-read live from `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md` | matches the Allocation/Authorization Records' restatement exactly |
| Sequence §7 (Step 5) text | re-read live from `BANPU_IMPLEMENTATION_SEQUENCE.md` | matches exactly |
| Design doc §5, §8.4, §9, §10, §12, §16, and the WP1 residual register (§16 subsection) | re-read live from `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` | authoritative source for §8–§13 below |
| BANPU-WP4 Work Package Plan | read in full as structural and lifecycle precedent | used for §-numbering, task-table, and blocked-task conventions |
| Live repository implementation surfaces | `backend/services/portfolio_metrics.py`, `portfolio_snapshots.py`, `snapshot_return_recovery.py`, `portfolio_rebuilder.py`, `manage.py` (`verify_snapshots`), `services/transaction_canonicalizer.py`, `services/market_data/position_conversion_quote_contract.py` inspected directly (§6) | grounds §7–§13 in actual code, not hypothetical architecture |
| `git status` overlap check | only WP4-authorized files modified/untracked; no WP5 production/test file touched | `NO OVERLAPPING CHANGE` |

All authorization-entry-equivalent prerequisites for planning are satisfied.
Planning proceeds; §10 records the one genuine ambiguity found during
live-code inspection.

## 3. Authoritative scope

Restated exactly from Roadmap §7 and bound to capability IDs used throughout
this plan:

| ID | Authorized capability |
|---|---|
| WP5-C1 | Classify `POSITION_CONVERSION` as zero external/import/manual flow in accounting readers |
| WP5-C2 | Include admitted cash-in-lieu fees and realized P/L exactly once |
| WP5-C3 | Add the hard `from_date` conversion boundary to portfolio rebuilding (`POSITION_CONVERSION_REBUILD_BOUNDARY`) |
| WP5-C4 | Preserve stored pre-boundary prices and values exactly |
| WP5-C5 | Recognize evidence-annotated suspension-gap return as genuine investment return |
| WP5-C6 | Emit successor asset identity in post-boundary holdings JSON |
| WP5-C7 | `MINOR-2` WP5 half: mechanical NAV continuity tolerance admissibility, before consumption |

Nothing in this plan adds an eighth capability or widens any of the seven
above.

## 4. Explicit exclusions

This plan does not decompose, and WP5 implementation may not perform:

- any change to `backend/main.py`, any public endpoint, or any frontend
  authoring path;
- any schema, model, or migration change;
- any change to `backend/services/portfolio_transactions.py`,
  `asset_registry.py`, or `transaction_canonicalizer.py` (WP4's frozen and
  closed write/canonicalization surface);
- any change to `backend/services/market_data/position_conversion_quote_contract.py`
  or any other WP3 quote-protection module (WP3's closed surface — see §5);
- any actual production snapshot rebuild, repair, repricing, cache purge, or
  shadow rewrite;
- any WP6 (shadow/time-series continuity), WP7 (operator CLI/rehearsal), or
  WP8 (integrated regression/release) act;
- production deployment or deployment authorization;
- M46 work; and
- unrelated recommendation/optimizer/evaluation work.

## 5. Frozen predecessor dependencies and invariants

WP5 implementation must consume, and must not duplicate or reinterpret:

- **WP1** — the frozen `PositionConversion` typed value and its
  `PositionConversionBoundaryEvidence` member (`predecessor_reference_price`,
  `successor_reference_price`, `mechanical_nav_tolerance_pct`,
  `suspension_gap_annotation`), produced solely by
  `services/transaction_canonicalizer.py`'s `parse_position_conversion_payload()`.
  WP5 reads these typed values; it does not re-parse the JSON payload.
- **WP2** — `_preflight_position_conversions()`, `_resolve_conversion_successors()`,
  and the existing `from_date` filtering already present in
  `rebuild_portfolio()` (Stage 2–3 snapshot-date selection). WP5 adds a
  refusal gate ahead of this existing filtering; it does not replace it
  (§8).
- **WP3** — `services/market_data/position_conversion_quote_contract.py`
  (`assess_reference_price_admissibility`, `ReferencePriceAdmissibility`,
  `QuarantineReason`, `evaluate_candidate_quarantine`) is WP3's closed
  implementation surface. Its own docstring (module header, and the
  `QuarantineReason` class docstring) explicitly places "WP5's mechanical
  NAV continuity tolerance", "mechanical continuity failure", and
  "unannotated boundary discontinuity" **out of its scope by design** and
  names them as WP5's half of `MINOR-2`. WP5 must not edit this file, must
  not add a member to `QuarantineReason`, and must not import from it beyond
  read-only consumption of the already-validated
  `predecessor_reference_price` / `successor_reference_price` values it
  exposes. WP5 provides its own, separate admissibility function for
  `mechanical_nav_tolerance_pct` (§10) rather than extending WP3's.
- **WP4** — `execute_position_conversion()`'s live materialization,
  registry preparation, and the `MERGED_INTO` relationship it establishes,
  are frozen and closed. WP5 reads successor identity through the registry
  state WP4 already produced; it does not re-derive or duplicate registry
  logic.
- **Existing generic NAV-continuity audit** (`manage.py`
  `_audit_nav_continuity`, the `--nav-threshold` CLI flag, `AuditCheck.NAV_CONTINUITY`)
  is a pre-existing, conversion-independent snapshot-to-snapshot audit
  unrelated to the payload's `mechanical_nav_tolerance_pct`. WP5 must not
  conflate the two, must not change `_audit_nav_continuity`'s behavior or
  threshold semantics, and must not route the payload tolerance through the
  `--nav-threshold` mechanism.

## 6. Live-code analysis and proposed edit surface

Every file below was read directly (not inferred from the roadmap forecast)
before being proposed.

| File | Current POSITION_CONVERSION handling found | WP5 requirement it maps to | Proposed edit |
|---|---|---|---|
| `backend/services/portfolio_metrics.py` (`compute_period_metrics`, lines ~137–191) | **None.** The function classifies `INITIAL_POSITION` → `imported_asset_value`, `QUANTITY_CORRECTION` → `manual_adjustment_value`, `SELL` → `period_realized_pnl`, `BUY`/`SELL` → `period_fees_paid`, `DIVIDEND` → `period_dividend_income`. A `POSITION_CONVERSION` row matches none of these branches today and silently contributes to none of them | WP5-C1, WP5-C2 | Add one `elif ctx.transaction_type == "POSITION_CONVERSION":` branch that adds only the admitted `cash_in_lieu.realized_pnl`/fees when `ctx.position_conversion.cash_in_lieu` is not `None`, and adds nothing when it is `None`. No existing branch is modified |
| `backend/services/snapshot_return_recovery.py` (`_compute_return_fields`, lines ~130–191) | **None found.** No `POSITION_CONVERSION` reference in this file | WP5-C1, WP5-C2, WP5-C5 | Mirror the same classification used in `portfolio_metrics.py` so recovered/recomputed return fields agree with the live snapshot path; preserve any `suspension_gap_annotation`-covered return unmodified |
| `backend/services/portfolio_snapshots.py` (`generate_daily_snapshot`, holdings list built at lines ~381–398, serialized at line 651) | Holdings entries are built per `PortfolioItem` with no conversion-specific identity field; no `POSITION_CONVERSION` reference in this file | WP5-C6 | Extend each holdings entry with the successor's registry-resolved asset identity when the item is a post-boundary conversion successor; predecessor rows before the boundary keep their existing (predecessor) identity unchanged |
| `backend/services/portfolio_rebuilder.py` (`rebuild_portfolio`, lines 2064–2280+) | `from_date` is already threaded through Stage 2–3's snapshot-date selection (`rebuild_dates`, `prev_db_snap`) and already correctly *excludes* pre-`from_date` dates from reconstruction **when `from_date` is given**. `conversion_successors = _resolve_conversion_successors(db, portfolio_id, all_txs)` already runs and already identifies whether the ledger contains a conversion. **No `POSITION_CONVERSION_REBUILD_BOUNDARY` refusal exists anywhere in this file** — when `from_date` is `None`, `rebuild_dates` is currently built from *every* existing snapshot date, including pre-transition ones, with no refusal | WP5-C3, WP5-C4 | Insert one fail-closed guard immediately after `conversion_successors` is resolved and before Stage 2–3's `rebuild_dates` computation (§8) |
| `backend/manage.py` (`_cmd_verify_snapshots` / `_audit_portfolio`, lines 1123–1310) | Only the generic, conversion-independent `_audit_nav_continuity` exists (§5) | WP5-C7 (admissibility only — §10) | Add one new, additive audit check function invoked from `_audit_portfolio` only for portfolios whose ledger contains a `POSITION_CONVERSION`; it reports (never blocks — `verify_snapshots` is read-only) a finding when `mechanical_nav_tolerance_pct` itself is inadmissible. It does **not** perform the reconciliation comparison (§10 blocker) |

No file outside this table is proposed. `backend/services/asset_repository.py`,
`asset_registry.py`, `portfolio_transactions.py`, and
`transaction_canonicalizer.py` are not touched — WP5 has no capability that
requires them.

### 6.1 Proposed test surface

| File | Role |
|---|---|
| `backend/tests/test_portfolio_metrics.py` | WP5-C1/C2 classification cases (§11) |
| `backend/tests/test_portfolio_metrics_parity.py` | Parity between live snapshot metrics and recovered metrics for a conversion-bearing portfolio |
| `backend/tests/test_snapshot_return_recovery.py` | WP5-C1/C2/C5 cases in the recovery path |
| `backend/tests/test_portfolio_rebuilder.py` | WP5-C3/C4 — `POSITION_CONVERSION_REBUILD_BOUNDARY` refusal and bounded-rebuild preservation (§8, §14) |
| `backend/tests/test_verify_snapshots.py` | WP5-C7 tolerance-admissibility reporting only (§10) |

## 7. Detailed implementation design — overview

WP5 implementation is four independent, separately testable changes sharing
no runtime call path with each other:

1. accounting-reader classification (§11) — `portfolio_metrics.py`,
   `snapshot_return_recovery.py`;
2. rebuild-boundary refusal and bounded reconstruction (§8, §9) —
   `portfolio_rebuilder.py`;
3. successor identity in holdings JSON (§13) — `portfolio_snapshots.py`;
4. tolerance-admissibility audit reporting (§10) — `manage.py`.

None of the four depends on another's implementation order. §18 records a
recommended sequence for evidence-quality reasons, not a technical
dependency.

## 8. `POSITION_CONVERSION_REBUILD_BOUNDARY` contract

Grounded directly in design §8.4 ("If a portfolio contains a conversion,
snapshot rebuilding MUST fail with `POSITION_CONVERSION_REBUILD_BOUNDARY`
when `from_date` is absent or predates the earliest transition. Pre-transition
snapshots MUST be priced from their stored values and MUST NOT be re-fetched
under a reused ticker") and the live code read in §6:

| Question | Determination | Basis |
|---|---|---|
| Affected entry point | `rebuild_portfolio()` in `portfolio_rebuilder.py` only. `rebuild_all_portfolios()` calls `rebuild_portfolio()` per portfolio and inherits the guard automatically; it needs no separate change | live code read, §6 |
| Where `from_date` enters | The existing `from_date: str \| None = None` parameter, already present and already partially honored by the Stage 2–3 date filter | live code read |
| Where the earliest transition boundary is established | The minimum `transaction_date` over every `ctx` in `all_txs` (the effective, already-repair-overlaid and conversion-reinstated list — see `_reinstate_excluded_conversions`, §7.1 of the design) where `ctx.transaction_type == "POSITION_CONVERSION"`. Using `all_txs` rather than `raw_txs` is required because WP2's §7.1 rule already makes an excluded conversion authoritative regardless of any repair, and the boundary must reflect that same authoritative view | design §7.1 (referenced by the existing `_reinstate_excluded_conversions` code comment), §8.4 |
| Refusal condition | Conversions exist in `all_txs` **and** `not skip_snapshots` **and** (`from_date is None` **or** `from_date < earliest_transition_date`) | design §8.4 verbatim |
| Point of refusal | Immediately after `conversion_successors = _resolve_conversion_successors(...)` and strictly before `rebuild_dates` is computed (i.e., before any Stage 2–3 work) — earlier than any snapshot read, provider fetch, or write | design §8.4 ("MUST fail... before writes or unsafe provider fetches", Roadmap §7 acceptance criteria) |
| What must not occur before refusal | No `PortfolioSnapshot` query beyond what Stage 1 already performed for replay, no provider price fetch, no snapshot row write, no commit | design §4.8 (fail closed), Roadmap §7 |
| Failure mechanism | Raise a new, narrowly-scoped exception (e.g. `PositionConversionRebuildBoundaryError`, mirroring the existing `PositionConversionReplayError` pattern already used for `POSITION_CONVERSION_PAYLOAD_INVALID` etc. in the same module) carrying the check ID `POSITION_CONVERSION_REBUILD_BOUNDARY`, caught at the same level `rebuild_portfolio()` already catches replay errors, surfaced as `result.error` with `result.success = False`, no partial commit | mirrors the module's existing `PositionConversionReplayError` handling pattern (WP2) |
| Bounded reconstruction when `from_date` is admissible | Unchanged — the existing `if from_date: rebuild_dates = [... >= from_date]` / `prev_db_snap = ...` logic (lines ~2272–2280) already implements this correctly and needs no modification | live code read |
| How stored values before the boundary remain untouched | Structural: `rebuild_dates` never includes a pre-`from_date` date once the new guard forces `from_date` to be present and admissible, so Stage 2–3's write loop never iterates a pre-boundary date. WP5 adds no separate "preservation" code path — the existing exclusion, now made mandatory rather than optional, is the preservation mechanism | derived from live code, not invented |
| How this is proven | New `test_portfolio_rebuilder.py` cases: (a) conversion present, `from_date=None` → raises with `POSITION_CONVERSION_REBUILD_BOUNDARY`, no snapshot row written; (b) conversion present, `from_date` before the transition date → same refusal; (c) conversion present, `from_date` on/after the transition date → no refusal, existing behavior proceeds; (d) no conversion present, `from_date=None` → unaffected (regression); (e) byte/field-level comparison of every pre-boundary `PortfolioSnapshot` row before and after a bounded rebuild — all fields identical | Roadmap §7 verification, design §16 ("Refusal of full or pre-boundary snapshot rebuild", "Byte-for-byte preservation of pre-boundary snapshot values") |

### 8.1 Distinction preserved

This plan authorizes only (1) implementing the refusal-and-bounded-reconstruction
*mechanism* inside `rebuild_portfolio()`, exercised exclusively against the
test database in developer/CI test runs. It does not authorize, and no test
in §8 may be read as authorizing, (2) invoking that mechanism against a
production database or executing an actual historical snapshot correction.
Design §14 places (2) inside the separately controlled production deployment
sequence gated on WP8 acceptance (already recorded by the WP5 Allocation
Record §9).

## 9. Pre-boundary preservation contract

- **Covered records/fields:** every column of every `PortfolioSnapshot` row
  whose `snapshot_date` is earlier than the admissible `from_date` used in a
  bounded rebuild, for a portfolio that contains a `POSITION_CONVERSION`.
- **Byte-exact, not approximate:** design §16 requires "byte-for-byte
  preservation of pre-boundary snapshot values" and design principle 9
  requires pre-transition accounting and derived values to "remain
  unchanged"; this plan does not weaken that into numeric-tolerance
  equality. The only WP1-authorized exception is design §12's
  "metadata-only enrichment... permitted only when hashes or field
  comparisons prove all numeric values unchanged" — WP5's §13 successor-
  identity change touches only post-boundary rows and therefore does not
  invoke this exception for pre-boundary rows at all.
- **Before-state capture:** the test harness reads and serializes every
  pre-boundary `PortfolioSnapshot` row (all columns, including
  `holdings_json`) before invoking `rebuild_portfolio(..., from_date=<admissible>)`.
- **After-state comparison:** the same rows are re-read after the bounded
  rebuild and compared field-by-field (numeric fields by exact equality,
  `holdings_json` by parsed structural equality) against the captured
  before-state.
- **Test evidence:** the row (e) case in §8's table; this is the same
  evidence class the design's own test-strategy section requires.

## 10. `MINOR-2` WP5-half treatment

### 10.1 Obligation carried unchanged

The WP1 residual register (design §16) splits `MINOR-2` between WP3
(reference-price admissibility, already discharged under WP3's closed
authority) and WP5 (mechanical continuity **tolerance** admissibility),
with the canonical verification point "focused WP5 tests reject negative or
otherwise inadmissible continuity tolerances **before comparison**."

### 10.2 What live code independently confirms

`services/market_data/position_conversion_quote_contract.py` — a frozen WP3
module — states explicitly in its own docstrings (module header and the
`QuarantineReason` class docstring) that "mechanical continuity failure" and
"unannotated boundary discontinuity" are "design §10's WP5-owned half" and
are "deliberately absent" from WP3's `QuarantineReason` enumeration. This is
strong, independent, code-level corroboration — not merely a planning
inference — that WP5 owns both (a) validating `mechanical_nav_tolerance_pct`
itself, and (b) the resulting continuity-failure/discontinuity
determination that consumes it together with WP3's already-validated
`predecessor_reference_price` / `successor_reference_price`.

### 10.3 Part (a) — tolerance admissibility — `READY`

This part is well-evidenced by direct structural precedent: WP3's
`assess_reference_price_admissibility()` (lines 291–343 of the quote
contract module) already establishes the exact pattern for the sibling
field class (`ABSENT` / `NON_DECIMAL_EXACT` / `NON_FINITE` / `NON_POSITIVE`
/ `ADMISSIBLE`), reading only from the frozen, already-parsed
`PositionConversionBoundaryEvidence` object.

**Planning determination PD-WP5-1:** WP5's `mechanical_nav_tolerance_pct`
admissibility function mirrors that exact pattern — `ABSENT` /
`NON_DECIMAL_EXACT` / `NON_FINITE` / `NEGATIVE` / `ADMISSIBLE` — with no
upper-bound rejection. Basis: (i) the residual register's own wording is
"reject negative **or otherwise inadmissible**", and `NON_FINITE`/
`NON_DECIMAL_EXACT` already satisfy "otherwise inadmissible" by direct
analogy to WP3's frozen pattern; (ii) no canonical artifact states an
upper-bound percentage, and inventing one (e.g. "reject > 100") would add
an acceptance criterion the design does not state. If a reviewer wants an
upper bound, that is a plan amendment, not an inference this plan makes.
Unlike price (`<= 0` rejected), zero is treated as `ADMISSIBLE` for a
tolerance — a zero-percent tolerance is a stricter, not an invalid,
requirement, and design §5's equations never treat zero as a sentinel for
"absent" the way price naturally would.

This part is fully plannable and is included in §6's `manage.py` edit and
§15's acceptance matrix.

### 10.4 Part (b) — the reconciliation/comparison itself — `PLANNING BLOCKER`

Design §10 states only that "mechanical boundary value MUST reconcile
within the payload tolerance using evidence-bound reference prices" — unlike
§5's accounting model, which gives exact equations for every quantity, §10
gives no equation for this reconciliation. Concretely unresolved by any
canonical artifact:

- **Formula:** is the comparison
  `abs(successor_reference_price - predecessor_reference_price) / predecessor_reference_price × 100 <= mechanical_nav_tolerance_pct`,
  or relative to the successor price, or relative to their average, or an
  absolute-percentage-point comparison of two independently computed
  returns? All are plausible readings of "reconcile within tolerance"; none
  is stated.
- **Boundary inclusivity:** is exact equality to the tolerance admissible
  (`<=`) or not (`<`)?
- **Rounding/precision:** at what `Decimal` precision is the comparison
  performed, and is the payload's exact-`Decimal` tolerance percentage
  itself rounded before use?
- **Annotation interaction:** does a present-but-empty-string
  `suspension_gap_annotation` count as "annotated" (accepted) or as absent
  (failure)? The payload contract (design §6.2) requires the field as a
  non-optional string but does not state a non-empty constraint.

Per the invoking instruction's own framing ("if repository evidence is
insufficient to determine any of these safely, mark the issue as a planning
blocker rather than inventing semantics"), this plan does **not** invent an
equation. **This is recorded as an open planning blocker, not resolved by
this plan.**

**Consequence for this plan**, mirroring the WP4 Work Package Plan's
treatment of `MINOR-1` at its conditional boundary:

- the `manage.py` audit addition in §6 implements only §10.3 (tolerance
  admissibility reporting); it does not implement the reconciliation
  comparison, does not emit a "mechanical continuity failure" or
  "unannotated boundary discontinuity" finding, and does not read
  `predecessor_reference_price/successor_reference_price` for comparison
  purposes;
- no `MECHANICAL_CONTINUITY_FAILURE` or `UNANNOTATED_BOUNDARY_DISCONTINUITY`
  check ID is implemented by this plan;
- WP5-C7 is therefore only **partially** decomposed by this plan (§10.3
  only); full satisfaction of WP5's `MINOR-2` half requires either a
  separate planning decision fixing the reconciliation formula, or a
  reviewer determination that the formula is out of WP5's authorized scope
  entirely and belongs to a distinct, not-yet-identified act; and
- WP5 may not be confirmed, frozen, or closed while §10.4 remains
  undetermined and unimplemented, exactly as `MINOR-1` blocked WP4 closure
  until its conditional boundary was resolved.

This blocker does not affect WP5-C1 through WP5-C6, all of which are fully
plannable independent of it.

## 11. Accounting-reader design (WP5-C1, WP5-C2)

Both `portfolio_metrics.py::compute_period_metrics()` and
`snapshot_return_recovery.py::_compute_return_fields()` gain one additional
branch, structurally identical in shape to the existing `SELL`/`DIVIDEND`
branches already in each function (no competing interpretation is
introduced):

```text
elif ctx.transaction_type == "POSITION_CONVERSION":
    cil = ctx.position_conversion.cash_in_lieu if ctx.position_conversion else None
    if cil is not None:
        period_realized_pnl += float(cil.realized_pnl)
        period_fees_paid    += float(cil.fees) + float(cil.taxes)
    # no cash_in_lieu: contributes nothing (design §5 — Cn, RP, F, T are all zero)
```

Acceptance coverage (§15):

- a `POSITION_CONVERSION` with no cash-in-lieu contributes zero to
  `net_external_cash_flow`, `imported_asset_value`,
  `manual_adjustment_value`, `period_realized_pnl`, and `period_fees_paid`
  (WP5-C1);
- a `POSITION_CONVERSION` with cash-in-lieu contributes its admitted
  `realized_pnl` and `fees + taxes` exactly once, and nothing else changes
  (WP5-C2);
- an existing `SELL`/`DIVIDEND`/`BUY` transaction in the same period is
  unaffected (regression — proves no competing interpretation was
  introduced); and
- `portfolio_metrics.py` and `snapshot_return_recovery.py` produce identical
  classification for the same fixture (parity, per §6.1).

## 12. Suspension-gap return behavior (WP5-C5)

Design principle 9 and Roadmap §7's acceptance criterion ("Genuine annotated
suspension-period return remains investment return") require a
**passive**, not corrective, behavior: the snapshot/return calculation path
must compute the conversion-period return normally from the stored
predecessor/successor prices and must not detect, clamp, smooth, or
"repair away" an unusual return magnitude across the transition date. No
existing code in `portfolio_metrics.py` or `snapshot_return_recovery.py`
performs such clamping today (confirmed by the live-code read in §6), so
this capability is satisfied by **not introducing** any magnitude-based
filter alongside the WP5-C1/C2 branch above, and is proven by a regression
test asserting that a large but genuine price move across a conversion
boundary produces an unclamped `investment_return_pct` equal to the
arithmetic result. `suspension_gap_annotation` itself is carried as
existing payload metadata (already parsed and typed by WP1); WP5 does not
need to add a new field to persist it — it is a boundary-evidence property
of the transaction, not a snapshot property, and its consumption for
reporting purposes belongs to §10.3/§10.4's audit path, not to the
per-snapshot return computation.

## 13. Successor-identity design (WP5-C6)

Design §12: "Derived BANPU holdings JSON MUST carry a non-null predecessor
asset ID before the boundary and successor asset ID after it." The live
holdings-entry construction in `portfolio_snapshots.py` (§6) builds one
dict per current `PortfolioItem` row; because WP4's `execute_position_conversion()`
already removes/transforms the predecessor `PortfolioItem` and creates the
successor row at conversion time (design §9, step 7–8), a snapshot
generated **after** the boundary already iterates only the successor's
`PortfolioItem` — the successor's `asset_id` is therefore already the one
naturally present in `items` by construction, sourced from the same
registry state WP4 established (§5). The required WP5 change is narrower
than "derive an identity": it is to ensure the existing holdings-entry
`asset_id` field is populated from `PortfolioItem.asset_id` (the
registry-bound column) rather than from any caller-controlled or
display-only value, for every entry, and add a **regression test**, not new
derivation logic, proving:

- a post-boundary holdings entry's `asset_id` equals the successor's
  registry `asset_id`, never the predecessor's;
- a pre-boundary snapshot's holdings entry (generated before any
  conversion existed) is unaffected; and
- no holdings entry ever carries the predecessor's identifier once that
  predecessor has been retired by WP4's registry preparation.

If live inspection of the `items`-building query during implementation
finds any path where a stale or cached `asset_id` could leak through
(e.g., a display-symbol join), that is exactly the narrow defect this
capability closes; if none is found, the capability is satisfied by the
regression test alone with no source change, and implementation must
record that finding rather than inventing an edit.

## 14. Failure/fail-closed behavior

| Condition | Behavior |
|---|---|
| `from_date` absent or predates earliest transition, conversion present, snapshots not skipped | `rebuild_portfolio()` returns `result.success = False`, `result.error` naming `POSITION_CONVERSION_REBUILD_BOUNDARY`; no snapshot row is read for reconstruction, no provider fetch occurs, no commit occurs (§8) |
| `ctx.position_conversion` is `None` for a row typed `POSITION_CONVERSION` | Cannot occur past WP2's `_preflight_position_conversions()`, which already raises `POSITION_CONVERSION_PAYLOAD_INVALID` earlier in the same pipeline; WP5 code does not need a defensive branch for this, and must not add one that could mask the WP2 gate |
| `mechanical_nav_tolerance_pct` inadmissible (§10.3) | `verify_snapshots` reports a finding (non-blocking — the command is read-only by design) rather than raising; it never affects `rebuild_portfolio()` |
| Reconciliation comparison (§10.4) | Not implemented by this plan; no failure path exists for it yet |

## 15. Test and acceptance matrix

| ID | Obligation | Governing requirement/source | Implementation surface | Required test/evidence | Expected result | Failure condition |
|---|---|---|---|---|---|---|
| WP5-A1 | Zero external/import/manual classification, no CIL | Roadmap §7; design §5 | `portfolio_metrics.py` | `test_portfolio_metrics.py` fixture, no `cash_in_lieu` | all four flow fields unaffected | any field changes |
| WP5-A2 | Zero external/import/manual classification, with CIL | Roadmap §7; design §5 | `portfolio_metrics.py` | same, with `cash_in_lieu` | flow fields still unaffected; `period_realized_pnl`/`period_fees_paid` reflect CIL exactly once | double-count or flow-field leakage |
| WP5-A3 | Recovery-path parity | Roadmap §7 | `snapshot_return_recovery.py` | `test_snapshot_return_recovery.py` | matches WP5-A1/A2 | divergence from live path |
| WP5-A4 | Rebuild refusal, `from_date=None` | design §8.4 | `portfolio_rebuilder.py` | `test_portfolio_rebuilder.py` | `POSITION_CONVERSION_REBUILD_BOUNDARY`, no write | rebuild proceeds |
| WP5-A5 | Rebuild refusal, `from_date` before transition | design §8.4 | `portfolio_rebuilder.py` | same | same refusal | rebuild proceeds |
| WP5-A6 | Bounded rebuild proceeds when admissible | design §8.4 | `portfolio_rebuilder.py` | same | normal Stage 2–3 behavior, unchanged | unexpected refusal |
| WP5-A7 | No-conversion regression | design §2 goal 8 | `portfolio_rebuilder.py` | same | unaffected by the new guard | new guard fires without a conversion |
| WP5-A8 | Byte-exact pre-boundary preservation | design §16 | `portfolio_rebuilder.py` | field/hash comparison (§9) | zero diffs | any pre-boundary field changes |
| WP5-A9 | Unclamped suspension-gap return | Roadmap §7; design principle 9 | `portfolio_metrics.py`/`snapshot_return_recovery.py` | large genuine move fixture | arithmetic result, unmodified | any clamping/smoothing |
| WP5-A10 | Successor identity post-boundary | design §12 | `portfolio_snapshots.py` | holdings-json assertion | successor `asset_id` only | predecessor id leaks through |
| WP5-A11 | Predecessor identity pre-boundary unaffected | design §12 | `portfolio_snapshots.py` | same | predecessor `asset_id` unchanged | identity altered before boundary |
| WP5-A12 | Tolerance admissibility — negative rejected | design §16 residual register; PD-WP5-1 | `manage.py` | `test_verify_snapshots.py` | `NEGATIVE` reported | accepted |
| WP5-A13 | Tolerance admissibility — non-finite/non-decimal rejected | PD-WP5-1 | `manage.py` | same | rejected, mirroring WP3 pattern | accepted |
| WP5-A14 | Tolerance admissibility — admissible value passes | PD-WP5-1 | `manage.py` | same | `ADMISSIBLE`, no finding | false-positive report |
| WP5-BLOCKED | Reconciliation formula (mechanical continuity failure / unannotated discontinuity) | §10.4 | none — not implemented | none | — | **not implementable until the formula is fixed by a separate planning decision** |

Every row except `WP5-BLOCKED` covers both a positive and a negative/
fail-closed case; `WP5-BLOCKED` is carried in the matrix precisely so a
later independent reviewer can see it was identified, not overlooked.

## 16. Regression requirements

WP5 implementation must keep green, unmodified in expectation:

- `backend/tests/test_portfolio_metrics.py` (pre-existing cases)
- `backend/tests/test_portfolio_metrics_parity.py` (pre-existing cases)
- `backend/tests/test_snapshot_return_recovery.py` (pre-existing cases)
- `backend/tests/test_portfolio_rebuilder.py` (pre-existing cases — includes
  WP2's `_preflight_position_conversions` and replay-branch coverage)
- `backend/tests/test_verify_snapshots.py` (pre-existing cases, including
  the unrelated `_audit_nav_continuity` behavior — §5)
- `backend/tests/test_position_conversion_live.py`,
  `test_asset_registry.py`, `test_transaction_canonicalizer.py` (WP4's
  frozen surface — must remain untouched and green as a non-regression
  check, even though WP5 does not edit these files)
- `backend/tests/test_position_conversion_quote_contract.py` (WP3's frozen
  surface — proves WP5 did not edit the quote-contract module)

## 17. Residual handling

Carried unchanged, without definition, resolution, waiver, or
reinterpretation:

| Item | Carried state |
|---|---|
| `MINOR-1`, `NEW-MINOR-A` | WP4-owned, closed; untouched by WP5 |
| `MINOR-5` | WP7 rehearsal / WP8 release evidence; untouched by WP5 |
| WP2 `MINOR-A`, `MINOR-B`, `OBSERVATION-A`…`OBSERVATION-E` | inherited unchanged, no obligation text invented |
| WP3 `R6`, WP3-scoped `R7` waiver, WP3 closeout observations | carried unchanged, gate nothing for WP5 |
| WP3 `PD-3` emitter-locus referral | belongs to the authority governing the canonical corpus; no WP5 criterion depends on it |
| `MINOR-2` WP3 half (reference-price admissibility) | already discharged under WP3's closed authority; WP5 reads its result, does not redo it |
| `MINOR-2` WP5 half — tolerance admissibility | `READY`, decomposed at §10.3 |
| `MINOR-2` WP5 half — reconciliation formula | `BLOCKED`, recorded at §10.4, not resolved by this plan |
| `POSITION_CONVERSION_REBUILD_BOUNDARY` | `READY`, fully decomposed at §8 |

WP5-owned open items after this plan remain exactly: the §10.4
reconciliation-formula blocker, and — until implementation actually
occurs — every capability in §3.

## 18. Implementation sequencing

| Task | Work | Depends on | Deliverable / evidence |
|---|---|---|---|
| WP5-T1 | Record entry baseline: repository state, frozen WP1–WP4 identities, test commands, pre-existing failures, §6 file allowlist | Authorization | Reproducible entry-gate record |
| WP5-T2 | Author failing tests WP5-A1…A3 (accounting-reader classification) | T1 | Obligations expressed before code |
| WP5-T3 | Implement the `portfolio_metrics.py`/`snapshot_return_recovery.py` branch (§11) | T2 | WP5-C1, WP5-C2 |
| WP5-T4 | Author failing tests WP5-A4…A8 (rebuild boundary) | T1 | Obligations expressed before code |
| WP5-T5 | Implement the `POSITION_CONVERSION_REBUILD_BOUNDARY` guard (§8) | T4 | WP5-C3, WP5-C4 |
| WP5-T6 | Author failing test WP5-A9 (unclamped suspension-gap return) | T1 | Obligation expressed before code |
| WP5-T7 | Confirm WP5-A9 passes with no source change, or make the minimal change if T6 fails (§12) | T3, T5, T6 | WP5-C5 |
| WP5-T8 | Author failing tests WP5-A10…A11 (successor identity) | T1 | Obligations expressed before code |
| WP5-T9 | Confirm/implement the holdings-entry identity source (§13) | T8 | WP5-C6 |
| WP5-T10 | Author failing tests WP5-A12…A14 (tolerance admissibility) | T1 | Obligations expressed before code |
| WP5-T11 | Implement the `manage.py` tolerance-admissibility audit addition (§10.3) | T10 | WP5-C7 (partial — §10.3 only) |
| WP5-T12 | **Conditional / blocked.** Submit the §10.4 reconciliation-formula question for a separate planning decision | — | Not part of this plan's exit criteria |
| WP5-T13 | Run the full §15 matrix (excluding `WP5-BLOCKED`) and the §16 regression suites; `graphify update .` | T3, T5, T7, T9, T11 | Complete WP5 evidence set |
| WP5-T14 | Prepare the independent implementation-review submission | T13 | Review-ready candidate; no confirmation, freeze, or closeout performed |

T12 does not block T1–T11 or T13–T14: every other capability is independent
of the reconciliation formula (§10.4's consequence list). WP5 cannot reach
full `MINOR-2` satisfaction while T12 is open, mirroring exactly how WP4
could not reach its exit criteria while `MINOR-1`'s T7/T8 were open.

## 19. Completion evidence required before implementation review

WP5 may enter independent implementation review only when:

1. every capability WP5-C1…C6 and WP5-C7 (§10.3 only) is implemented within
   the §6 file allowlist and nothing outside it is modified;
2. the full §15 matrix is green except `WP5-BLOCKED`, which remains
   explicitly open and recorded, not silently dropped;
3. every §16 regression suite is green;
4. §9's byte-exact pre-boundary preservation evidence is produced for at
   least one conversion-bearing fixture;
5. §8.1's distinction is respected — no test in §15 executes against a
   production database or performs an actual production snapshot
   correction;
6. the diff is allowlisted to §6, frozen WP1–WP4 artifacts and identities
   are unchanged, and `graphify update .` has been run; and
7. all §17 residuals are carried unchanged and no §4 exclusion was
   breached.

A failed criterion returns work to WP5; no later package may compensate for
it. This plan authorizes no confirmation, freeze, closeout, release,
deployment, or production execution. Satisfying these criteria makes WP5
review-ready and nothing more — the §10.4 blocker must still be separately
resolved before WP5's `MINOR-2` obligation as a whole can be called
complete, even if reviewers determine the rest of WP5 may proceed to review
first.

## 20. Prohibited acts / downstream boundaries

WP5 implementation may **not**:

- mutate production data or execute a production snapshot correction;
- edit `backend/services/portfolio_transactions.py`, `asset_registry.py`,
  `transaction_canonicalizer.py`, or
  `services/market_data/position_conversion_quote_contract.py`;
- add a member to WP3's `QuarantineReason` enum or otherwise extend WP3's
  closed module;
- change `_audit_nav_continuity`'s existing generic behavior or the
  `--nav-threshold` CLI semantics;
- invent a reconciliation formula for §10.4 and implement it as if it were
  settled;
- add a schema, model, or migration change;
- add a public endpoint, frontend authoring path, or CLI command beyond the
  additive `verify_snapshots` audit check in §6;
- perform any WP6, WP7, or WP8 act, or M46 work;
- modify any frozen governance artifact; or
- stage, commit, push, merge, or publish repository changes under color of
  this plan.

## 21. Repository verification of this planning act

| Verification | Result |
|---|---|
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP5_WORK_PACKAGE_PLAN.md` |
| Allocation Record or Implementation Authorization Record modified | `NONE` |
| Frozen BANPU artifacts modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX files modified | `NONE` — all live-code reads in §6 were read-only inspection |
| Trailing-whitespace verification | see final report |
| Markdown relative-link target verification | see final report |
| Markdown fragment-heading verification | see final report |
| `git diff --check` | see final report |
| `git diff --cached --check` | see final report |
| `graphify update .` | see final report |
| Final `git status --short --untracked-files=all` | see final report |
| Commit created | `NO` |

## 22. Exact next constitutional act

Two independent next acts follow from this plan, at different scopes:

1. For the plannable majority of WP5 (§3's WP5-C1…C6 and WP5-C7 at §10.3):
   the exact next constitutional act is **BANPU-WP5 Planning Confirmation**
   (or the repository's equivalently named confirmation act, per the
   precedent this plan otherwise follows), performed by a reviewer distinct
   from this planning authority.
2. For §10.4: the exact next act is a **separate planning decision fixing
   the mechanical-continuity reconciliation formula**, which must occur
   before WP5's `MINOR-2` obligation can be called planned, let alone
   implemented or closed.

This plan performs neither act.
