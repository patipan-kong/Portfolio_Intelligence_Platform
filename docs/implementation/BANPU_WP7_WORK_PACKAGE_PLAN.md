# BANPU-WP7 — Work Package Plan

**Artifact class:** Implementation planning only
**Status:** `WORK PACKAGE PLAN REVISED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN — READY FOR INDEPENDENT PLANNING CONFIRMATION`
**Plan date:** 2026-08-18
**Revision date:** 2026-08-18
**Issuing role:** BANPU-WP7 Work Package Planning Authority
**Work package:** `BANPU-WP7 — Operator command and migration rehearsal`
**Authority:** [BANPU-WP7 Implementation Authorization Record](BANPU_WP7_IMPLEMENTATION_AUTHORIZATION_RECORD.md), 20,963 bytes, 361 lines, SHA-256 `e7a6b235c84abbfff9159c7e91e2477e746b314128e1c1b1ee0b46d6e5faeb6c`, disposition `BANPU-WP7 IMPLEMENTATION AUTHORIZED`, over the scope bound by [BANPU-WP7 Allocation Record](BANPU_WP7_ALLOCATION_RECORD.md), 19,609 bytes, 329 lines, SHA-256 `1aa24cd242c95039b81df1a43f061b04140ea0ed5e0a2e7405ae18945900f4f1`, disposition `BANPU-WP7 ALLOCATED`
**`MINOR-5` (WP7 rehearsal portion / WP8 release-evidence portion) disposition in this plan:** `WP7 REHEARSAL PORTION PLANNED — NOT DISCHARGED` (§9)
**`NEW-MINOR-A` (WP7 production-dialect-rehearsal portion) disposition in this plan:** `WP7 PORTION PLANNED — NOT DISCHARGED, EVIDENCE REQUIREMENTS STRENGTHENED THIS REVISION` (§9)
**`PD-3` disposition in this plan:** `NOT WP7-OWNED — CARRIED FORWARD UNCHANGED, NOT PLANNED, NOT DISCHARGED` (§9)
**Successor authority created:** `NONE`
**Release/deployment/production-mutation authority created:** `NONE`

This plan decomposes already-authorized implementation authority. It performs
no implementation. It creates no authority, no new gate, no new acceptance
criterion, no new capability, and no file surface beyond the surface the
Implementation Authorization Record already bound. Where this plan and the
frozen canonical corpus differ, the frozen corpus governs and this plan is in
error.

## 0. Revision record

**Revision authority:** this bounded revision, performed under the
implementation authority already granted by the Implementation Authorization
Record (no re-allocation or re-authorization). No Planning Confirmation or
Planning Freeze is performed or claimed by this revision.

**Occasion:** an independent BANPU-WP7 Work Package Plan review returned
`BANPU-WP7 WPP INDEPENDENT REVIEW FAILED — PLAN REVISION REQUIRED`. This
revision corrects the identified defects and incorporates
[BANPU-WP7 Identity Ingress Design Clarification](BANPU_WP7_IDENTITY_INGRESS_DESIGN_CLARIFICATION.md),
17,489 bytes, 360 lines, SHA-256 `9cd583342cef65ecc3f771a93d37aba85327662f3d10920229552b794ca34c5d`,
disposition `BANPU-WP7 IDENTITY INGRESS CLARIFIED — CLI PORTFOLIO INPUT;
WORKSPACE DERIVED`.

**Original materialized identity (superseded by this revision):** 35,827
bytes, 496 lines, SHA-256 `2bdb77dd5ce9ce4da1649be276820b71aa48689ba2f45852c5265e6f55964eef`,
status `WORK PACKAGE PLAN MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT
PERFORMED — NOT CONFIRMED — NOT FROZEN`.

**Defects corrected (independent review findings):**

1. Open Item #1 (portfolio/workspace identity ingress) — closed via the
   identity clarification record (§7.1).
2. Registry-state preflight incorrectly validated a post-preparation
   invariant before preparation had run (§7.2).
3. Quote-gate integration was not callable from manifest fields alone (§7.2).
4. Mechanical-continuity integration path was unspecified (§7.2).
5. Broker-fact validation was named but not concretely integrated (§7.2).
6. Dual-replay preflight assumed a non-persistent simulation that does not
   exist as a callable capability (§7.2).
7. `NEW-MINOR-A` evidence requirements were underspecified (§9).
8. Rehearsal-environment provisioning was misclassified as a Planning
   Confirmation blocker (§7.5, §8, §12).

**Sections changed:** §3 (closing sentence only), §5.1 (dependency list
precision only), §6 (overview items 2-3, for consistency with §7.2/§7.3),
§7.1, §7.2, §7.3, §8, §9 (`NEW-MINOR-A` row only), §10 (rows WP7-A1–A3,
A7–A9, A11, A15, plus new rows WP7-A17–A19), §12 (one bullet), §13, §14,
§15, and this new §0. §1, §2, §4, §11, and the unmodified portions of §3,
§5, §6, §9, and §12 are preserved unchanged from the materialized plan
below.

## 1. Purpose and constitutional position

### 1.1 Objective

Give the WP7-authorized scope — the `apply_position_conversion` CLI with
dry-run default and explicit `--commit`, manifest/registry/broker/quote-epoch/
continuity/rebuild-boundary/replay-mode validation, deterministic before/
after reporting, cache-purge/bounded-rebuild instructions, and an isolated
production-shaped rehearsal — a precise, reviewable implementation contract,
grounded in the live repository's existing services rather than in the
roadmap's "expected files" forecast alone.

### 1.2 Constitutional position

This plan sits between BANPU-WP7's Implementation Authorization and its
future Implementation Review. It is subordinate to the Implementation
Authorization Record, the Allocation Record, and the frozen design, roadmap,
and sequence. It authorizes nothing; it decomposes what is already
authorized. A future Planning Confirmation and Planning Freeze remain
separate, later acts (§15), following the same lifecycle the WP6 Work
Package Plan used (`BANPU_WP6_PLANNING_CONFIRMATION.md`,
`BANPU_WP6_PLANNING_FREEZE_RECORD.md`), itself following the WP5 precedent —
i.e. Allocation and Authorization precede this Work Package Plan, consistent
with `BANPU_WP6_PLANNING_FREEZE_RECORD.md` §11's finding that the earlier
WP2/WP3 "Work Package Plan Gate 1" ordering does not transfer to the current
lifecycle.

## 2. Controlling authority

In descending order of scope, this plan is strictly subordinate to and does
not amend, reinterpret, or supersede:

1. the frozen canonical
   [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   especially §6 (payload/manifest contract), §9 (live materialization and
   the operator CLI), §10 (market-data protection), §11 (validator finding
   catalogue), §13-14 (migration and deployment strategy), and §15
   (rollback strategy);
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md)
   §9 (BANPU-WP7 purpose, scope, expected files, explicit no-change surface,
   dependencies, deliverables, acceptance criteria, verification, size
   estimate);
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md) §9
   (Step 7 preconditions, repository state, expected code changes,
   verification, exit criteria);
4. [`BANPU_WP7_ALLOCATION_RECORD.md`](BANPU_WP7_ALLOCATION_RECORD.md),
   disposition `BANPU-WP7 ALLOCATED`; and
5. [`BANPU_WP7_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP7_IMPLEMENTATION_AUTHORIZATION_RECORD.md),
   disposition `BANPU-WP7 IMPLEMENTATION AUTHORIZED`, whose §3-§4 bind the
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
| `BANPU_WP7_ALLOCATION_RECORD.md` | present, disposition `BANPU-WP7 ALLOCATED`, 19,609 bytes / 329 lines / SHA-256 `1aa24cd242c95039b81df1a43f061b04140ea0ed5e0a2e7405ae18945900f4f1` | `EXACT` |
| `BANPU_WP7_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | present, disposition `BANPU-WP7 IMPLEMENTATION AUTHORIZED`, 20,963 bytes / 361 lines / SHA-256 `e7a6b235c84abbfff9159c7e91e2477e746b314128e1c1b1ee0b46d6e5faeb6c` | `EXACT` |
| Authorization bounded to exact allocated scope | Authorization Record §3 restates the Allocation Record §3 scope verbatim; no capability added | `CONFIRMED` |
| BANPU-WP7 implementation authorized but not started | Authorization Record §11: implementation `AUTHORIZED / NOT STARTED`; repository search found no WP7 production/test file from §4.1/§4.2 | `CONFIRMED` |
| No prior BANPU-WP7 Work Package Plan | `docs/implementation/` search: only `BANPU_WP7_ALLOCATION_RECORD.md` and `BANPU_WP7_IMPLEMENTATION_AUTHORIZATION_RECORD.md` exist under the `BANPU_WP7_*` naming | `CONFIRMED ABSENT` |
| No BANPU-WP7 implementation artifact or diff | `git status --porcelain` shows only the two untracked BANPU-WP7 governance files; `backend/manage.py` unmodified; no `apply_position_conversion` subcommand exists; no fixture or CLI test file exists | `CONFIRMED ABSENT` |
| No release/deployment/production-mutation authority | Authorization Record header and §10: `NONE` | `CONFIRMED` |
| BANPU-WP8+ not allocated/not authorized | Authorization Record §11: `NOT ALLOCATED / NOT AUTHORIZED` | `CONFIRMED` |
| Allocation Record and Authorization Record are the only current additive WP7 artifacts | Same repository search as above | `CONFIRMED` |
| Nothing staged | `git diff --cached --name-only` empty; `git status --porcelain` shows only the two untracked files, both `??` | `CONFIRMED` |
| Roadmap §9 and Sequence §9 text | re-read live from both files | matches the Allocation/Authorization Records' restatement exactly |
| Design §6, §9-11, §13-15 text | re-read live from `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` | authoritative source for §6-§7 below |
| BANPU-WP6 Work Package Plan | read in full (724 lines) as structural and lifecycle precedent | used for §-numbering, task-table, and maturity-status conventions |
| Live repository implementation surfaces | `backend/services/portfolio_transactions.py::execute_position_conversion` (E1-E13 order), `backend/services/asset_registry.py::prepare_position_conversion_registry`, `::validate_position_conversion_registry_state`, `::resolve_predecessor_provider_symbol`, `backend/services/market_data/position_conversion_quote_contract.py::evaluate_candidate_quarantine`, `backend/manage.py` subcommands `apply_repair` (dry-run/`--commit`/`--yes`/`--force`/exit-code convention), `regenerate_paper_portfolios` (dry-run-default `--commit`/`--backup`/`--yes` convention), and `rebuild_portfolio` (`--backup`/`--commit`/`--plan`/`--plan-json` staged pipeline) inspected directly (§6-§7) | grounds §6-§7 in actual code and actual CLI precedent, not hypothetical architecture |
| `git status` overlap check | only the two BANPU-WP7 governance files untracked; no `backend/manage.py` or test/fixture file touched | `NO OVERLAPPING CHANGE` |

All premises match. No fail-closed condition exists. Planning proceeded. Two
implementation-critical design questions were found not to be settled by any
canonical artifact read for this original act; §8 recorded them as open
items rather than resolving them by invention. Both are resolved by the
revision recorded in §0 — see the current §8 for their determinations.

## 4. Exact bounded scope

Restated exactly from Authorization Record §3, bound to capability IDs used
throughout this plan:

| ID | Authorized capability |
|---|---|
| WP7-C1 | Add the `apply_position_conversion` CLI with dry-run default and explicit `--commit` |
| WP7-C2 | Validate manifest schema, registry state, broker facts, quote epoch, continuity evidence, rebuild boundary, and both replay modes |
| WP7-C3 | Produce a deterministic before/after report without exposing credentials or raw provider payloads |
| WP7-C4 | Add cache-purge and bounded-rebuild instructions; do not execute production changes in the package |

Nothing in this plan adds a fifth capability or widens any of the four
above. `MINOR-5`'s WP8 portion, `NEW-MINOR-A`'s WP4 portion, and `PD-3` are
not WP7 capabilities (§9).

## 5. Authorized file surface

Restated exactly from Authorization Record §4. No file outside this table is
proposed by this plan.

### 5.1 Production/operational surface

| File | Authorization basis |
|---|---|
| `backend/manage.py` | Authorization §4.1 — CLI command addition only, bounded to §4 |
| operational documentation, only if strictly required by the canonical design, and not M46 documentation | Authorization §4.1 |

No other new production file is authorized. `backend/services/portfolio_transactions.py::execute_position_conversion`,
`backend/services/asset_registry.py::prepare_position_conversion_registry`
and `::validate_position_conversion_registry_state`,
`backend/services/market_data/position_conversion_quote_contract.py::build_successor_quote_binding`,
`::evaluate_request_identity`, `::check_cache_namespace_mismatch`,
`::check_reference_price_inadmissible`, `::quote_cache_type`,
`::history_cache_type` (individually, per §7.2's corrected quote-gate
integration — `evaluate_candidate_quarantine` itself remains WP3-owned and
is not called directly by WP7), `backend/services/portfolio_rebuilder.py::rebuild_portfolio`,
and `backend/manage.py`'s own private `_evaluate_mechanical_continuity()`
(a same-file call, §7.2 step 3) (WP3/WP4/WP5's frozen and closed surfaces)
are read-only dependencies the CLI calls into — they are not edit targets
under this plan.

### 5.2 Test surface

| File | Role |
|---|---|
| a new sanitized test manifest under `backend/tests/fixtures/` | Section 6.2's payload contract shape, sanitized (no real credentials, no real broker reference), used by the new CLI test file |
| a new focused CLI test file (e.g. `backend/tests/test_apply_position_conversion_cli.py`) | §10 acceptance matrix — parser, preflight, dry-run, commit, idempotency, conflict, reporting cases |

No file outside this table is authorized. Authorization §4.2 permits "other
corresponding focused tests strictly bounded to the capabilities in §3, for
the files listed in §4.1" only if implementation identifies a genuine need;
this plan proposes none beyond the single CLI test file because
`backend/manage.py` is the sole production file in scope.

## 6. Implementation decomposition — overview

Live-code inspection (§7-§8) establishes that BANPU-WP7 is not new business
logic — every accounting, registry, and quote-protection mechanism it needs
already exists, authored and frozen by WP3/WP4. WP7's entire authorized
capability set is a **new orchestration layer**: one CLI subcommand that
parses and validates a manifest, then calls existing services in a specific,
fail-closed order. In dependency order:

1. **manifest loading and schema validation** (§7.1) — parse the reviewed
   production manifest against the Design §6.2 payload contract; no other
   step may run against an unparsed or invalid manifest.
2. **preflight validation chain** (§7.2) — pre-preparation registry
   preconditions, manifest-only quote-gate components, mechanical
   continuity, broker-fact discharge via schema parse, rebuild boundary,
   and existing-ledger both-replay-mode sanity, each reusing an existing
   WP3/WP4/WP5 function or a same-file `manage.py` helper; no preflight may
   be weakened or skipped.
3. **dry-run / explicit-commit branching** (§7.3) — dry-run computes and
   reports without persisting; `--commit` requires every preflight to have
   passed, then calls `prepare_position_conversion_registry()`, then
   `validate_position_conversion_registry_state()` as an explicit
   post-preparation checkpoint, then `execute_position_conversion()`, then
   runs the mandatory post-commit both-replay-mode verification.
4. **deterministic reporting** (§7.4) — a structured before/after report,
   built from the same data the preflight chain already computed, with
   credentials and raw provider payloads excluded by construction.
5. **cache-purge / bounded-rebuild instructions and the isolated
   production-shaped rehearsal** (§7.5) — orchestration-only reuse of the
   existing `rebuild_portfolio` and `regenerate_paper_portfolios`
   subcommands against an isolated production-shaped copy; WP7 does not
   reimplement rebuild or shadow-regeneration logic.

None of items 2-5 can begin before item 1 exists. Item 3 cannot begin before
item 2 passes. Item 5's rehearsal cannot begin before items 1-4 exist and
pass their own tests.

## 7. Detailed mechanics

### 7.1 Manifest loading and schema validation (WP7-C1, WP7-C2) — `backend/manage.py`

The manifest is a JSON file matching Design §6.2's `conversion_payload`
contract exactly (`schema_version: 1`; `predecessor`/`successor`/
`conversion_ratio`/`basis`/`cash_in_lieu`/`dates`/`quote_binding`/
`boundary_evidence`/`evidence`) — WP7 introduces no second manifest format.
Loading MUST:

- read the file at `--manifest FILE`;
- parse it as JSON, failing closed on malformed JSON with a structured
  error, not a raw traceback;
- pass the parsed object through the existing canonical parser
  (`parse_position_conversion_payload`, already used by
  `execute_position_conversion` and by WP2's replay) rather than
  reimplementing field-level validation — this is the same "one canonical
  implementation per rule" (ADR-004) reasoning the WP6 Work Package Plan
  applied to its own shared succession-lookup mechanism; and
- fail closed with `POSITION_CONVERSION_PAYLOAD_INVALID`-class reporting
  (Design §11) on any parse error, before any preflight in §7.2 runs.

**Identity ingress (resolved — closes former §8 Open Item #1):** per
[BANPU-WP7 Identity Ingress Design Clarification](BANPU_WP7_IDENTITY_INGRESS_DESIGN_CLARIFICATION.md) §10,
`apply_position_conversion` requires a `--portfolio`/`-p` flag (matching the
`apply_repair`/`rebuild_portfolio` precedent exactly). Loading MUST also:

- read `args.portfolio` as `portfolio_id` (explicit, operator-supplied, no
  default — omission is a usage error, not a silent fallback);
- resolve the `Portfolio` row for `portfolio_id` and read its persisted,
  non-nullable `workspace_id` column (`backend/models/database.py:87`) to
  derive `ws_id` — never a second operator-supplied flag, never
  `db.query(Workspace).first()`;
- fail closed with a non-zero exit and no write if `--portfolio` does not
  resolve to an existing `Portfolio` row, before any preflight in §7.2 runs.

This adds no field to the Design §6.2 manifest contract, which remains
exactly as frozen. Design §9's example invocation is illustrative, not an
exhaustive argparse specification (identity clarification §8); the flag
narrows it without amending frozen architecture.

### 7.2 Preflight validation chain (WP7-C2) — `backend/manage.py`

**Corrected ordering.** Live inspection
(`asset_registry.py:458`, `validate_position_conversion_registry_state`)
establishes that this function requires the predecessor already `MERGED`
and the successor already carrying a current `PROVIDER_SYMBOL` identifier —
i.e. it validates the *post-preparation* state that only
`prepare_position_conversion_registry()` (`asset_registry.py:351`)
establishes. The original plan's step 1 called this function as a
pre-preparation check, which cannot pass against an unprepared pair. The
corrected order is:

1. **Pre-preparation, non-mutating registry preconditions** — replicate,
   read-only, the exact preconditions `prepare_position_conversion_registry()`
   itself checks before its first mutating call: predecessor and successor
   asset IDs are distinct and both resolve to an existing `Asset`; no
   existing outgoing `MERGED_INTO` relationship links the predecessor to a
   *different* successor. These are ordinary read queries, not a new
   mechanism — the same checks `prepare_position_conversion_registry()`
   already performs internally, evaluated here only to fail closed before
   the CLI reaches the preparation boundary.
2. **Quote-gate — manifest-only, provider-independent components.**
   WP3's frozen `position_conversion_quote_contract.py` exposes the
   composite decision (`evaluate_candidate_quarantine`) but also its
   individual checks. Two are provider-independent and manifest-only, and a
   third is purpose-built for exactly this pre-fetch situation:
   - `build_successor_quote_binding(successor, quote_binding, dates)` —
     constructs the `SuccessorQuoteBinding` mechanically from the already-
     parsed manifest (§7.1); no new construction path.
   - `evaluate_request_identity(binding, requested_symbol, request_provider)`
     — documented as consuming "only authoritative request-side values...
     does not require provider evidence" (`position_conversion_quote_contract.py:381-392`),
     the canonical pre-fetch identity check.
   - `check_cache_namespace_mismatch(quote_cache_type(binding), binding, kind="quote")`
     (and the `history` variant) — mechanical, binding-only.
   - `check_reference_price_inadmissible(boundary_evidence, field, binding)`
     — its own docstring: `boundary_evidence` "is a
     `PositionConversionBoundaryEvidence` instance from the frozen WP1
     parsed payload — never provider evidence" (`position_conversion_quote_contract.py:548-558`),
     i.e. this check is manifest-only by design.

   The remaining `evaluate_candidate_quarantine` checks
   (`EVIDENCE_CONTRACT_NOT_SATISFIED`, `PROVIDER_SYMBOL_MISMATCH`,
   `CROSS_EPOCH_TIMESTAMP`) require a live provider quote observation as
   `evidence`. WP7 does not fetch one: WP3's already-frozen fetch-layer gate
   (`data_fetcher.py`, importing this same module) evaluates those checks
   automatically the first time any code requests a quote or history row
   for the converted asset after commit. WP7 does not duplicate that
   continuous protection with a synthetic preflight fetch (which would
   invent new provider-fetch mechanics with no canonical requirement for
   one); it relies on the already-active WP3 gate for the live-evidence
   dimension.
3. **Mechanical continuity** — the pure classifier `_evaluate_mechanical_continuity()`
   (`backend/manage.py:1240`) is already a private, module-scope helper
   inside `manage.py` itself, consuming only literal Decimal fields
   (`predecessor_reference_price`, `successor_reference_price`,
   `mechanical_nav_tolerance_pct`, `conversion_ratio`,
   `suspension_gap_annotation`) already present in the manifest's
   `boundary_evidence` and top-level `conversion_ratio`. Because WP7's new
   subcommand lives in the same file, this is an ordinary same-module
   private-function call — not a cross-module reach into a frozen service
   surface, and not a new orchestration architecture. `_audit_mechanical_continuity()`
   (the wrapper that expects a persisted `PortfolioSnapshot`/`CanonicalTransaction`)
   is a *post-commit* audit consumer (used by `verify_snapshots`) and is not
   called here.
4. **Broker facts** — live inspection found no separate broker-fact
   service, validator, or external integration anywhere in the repository.
   "Broker facts" are the manifest's own broker-confirmed carried values
   (`successor.shares_received`, `cash_in_lieu`, `basis`, and
   `evidence.reference`/`source`/`captured_at`, Design §6.2) — the operator
   is trusted to have populated them from the real broker confirmation
   before submitting the manifest, exactly as Design §9 states
   ("broker-confirmed received quantity, optional cash-in-lieu facts").
   Their validation is discharged entirely by the canonical schema parse
   already performed in §7.1 (`parse_position_conversion_payload`) plus the
   reference-price-admissibility check already run in step 2 above — no
   separate broker-fact callable interface exists to integrate, and none is
   invented here.
5. **Rebuild boundary** — unchanged from the materialized plan: confirm the
   manifest's `valuation_transition_date` is consistent with
   `POSITION_CONVERSION_REBUILD_BOUNDARY` semantics (Design §8.4) without
   invoking a rebuild; read-only consistency check, not an invocation of
   WP5's bounded-rebuild guard itself (WP5-owned; §9).
6. **Both replay modes — split by what existing services can prove.**
   `Portfolio.replay_asset_id_native` (a persisted boolean) selects
   `prefer_asset_id` for `canonicalize_transactions()`
   (`portfolio_rebuilder.py:2193`); `rebuild_portfolio(..., dry_run=True)`
   is the existing no-write, full-replay entry point, but it operates only
   on already-persisted `Transaction` rows — there is no existing overlay
   mechanism (unlike `apply_repair`'s `LedgerRepair` exclusion overlay,
   which excludes rows, not adds hypothetical ones) that lets a not-yet-
   inserted candidate conversion be replayed without first materializing
   it. Promising an atomic pre-commit both-mode replay of the *candidate*
   conversion would be an impossible non-persistent simulation. The
   requirement is therefore split, using only existing capability:
   - **Pre-commit (achievable, this preflight):** toggle
     `portfolio.replay_asset_id_native` and run
     `rebuild_portfolio(..., dry_run=True)` under both values against the
     *existing, pre-conversion* ledger, comparing holdings/basis/cash/
     realized P/L; revert the flag; nothing is committed. This proves the
     portfolio is not already in legacy/asset-native disagreement before
     WP7 touches it — a genuine, valuable, achievable precondition.
   - **Full candidate-conversion parity (rehearsal-owned, not this
     preflight):** verifying both replay modes agree on the *post-
     conversion* state, where mutation-and-discard is safe, is exactly what
     the isolated production-shaped rehearsal (§7.5) already exercises
     against a disposable database copy. This is not a capability gap in
     production; it is a difference in which environment can safely
     materialize a candidate to replay it.
   - **Post-commit (achievable, mandatory, this same CLI invocation):**
     immediately after `execute_position_conversion()` returns
     `applied`, the CLI re-runs the same both-mode dry-run comparison
     against the now-persisted conversion. A mismatch is reported as a
     `CRITICAL` post-commit anomaly; the CLI does not attempt automated
     rollback (Design §15 already assigns post-commit recovery to the
     scoped backup/restore path, an operator-governed process this plan
     does not reinvent) and does not proceed to cache purge or rebuild
     (§7.5) on this outcome.

Any preflight failure in steps 1-5 stops the command before any write, with
a structured, deterministic failure report (Design §11 finding codes) and a
non-zero exit code (§7.4). No preflight may be reordered ahead of manifest
parsing (§7.1), and none may be skipped by any flag. Step 6's post-commit
half is the one designed exception to "no write before validation," bounded
and disclosed exactly as above — not a silent gap.

### 7.3 Dry-run / explicit-commit branching (WP7-C1) — `backend/manage.py`

Following the `apply_repair`/`regenerate_paper_portfolios` precedent
(dry-run-default, explicit opt-in mutation, `--yes` confirmation skip for
automation):

- **No flags**: run manifest load (§7.1) and preflight steps 1-5 (§7.2);
  report results (§7.4); perform no write. This is the default — identical
  in effect to `--dry-run`. The report explicitly distinguishes what is
  proven (pre-preparation registry preconditions, manifest-only quote-gate
  components, continuity, rebuild boundary, and existing-ledger both-mode
  replay parity) from what cannot be proven without a write (post-
  preparation registry state, live-provider quote evidence, and both-mode
  parity of the *candidate* conversion specifically — the last two remain
  the domain of WP3's continuous fetch-time gate and the isolated
  rehearsal, §7.2 step 6, respectively). No dry-run report claims a
  post-mutation invariant that no read-only mechanism can prove.
- **`--dry-run`** (explicit): identical behavior to no flags; accepted for
  symmetry with the design's documented invocation
  (`apply_position_conversion --manifest FILE --dry-run`).
- **`--commit`**: run manifest load and preflight steps 1-5 (§7.2); if and
  only if every one passes, proceed through the corrected commit sequence:
  1. call `asset_registry.prepare_position_conversion_registry()`
     (idempotent registry preparation — PD-WP4-1 establishes this is a
     separate service act, never invoked by `execute_position_conversion`
     itself, so WP7's CLI is the first and only caller that must invoke
     it);
  2. call `asset_registry.validate_position_conversion_registry_state()` as
     an explicit post-preparation confirmation checkpoint, giving the CLI
     its own dedicated, reported registry-state result distinct from
     `execute_position_conversion()`'s internal E3 (which still runs — this
     is a deliberate, cheap, redundant safety net, not a correctness
     dependency);
  3. call `execute_position_conversion()` (its own internal E1-E13 order,
     including the canonical retry preflight E8-R);
  4. on `applied`, run preflight step 6's post-commit both-replay-mode
     verification (§7.2) before reporting success.
  A failed preflight (steps 1-5) blocks `--commit` unconditionally; there is
  no override flag for a preflight failure (contrast with `apply_repair
  --force`, which WP7 does not adopt, because Design §11 treats every
  WP7-relevant finding as `CRITICAL`, not an overridable warning). A failed
  post-commit verification (step 6, item 4 above) does not block the write
  that already happened — it is reported as a `CRITICAL` post-commit
  anomaly and the CLI does not proceed to §7.5's cache-purge/rebuild
  instructions on that outcome.
- **Idempotency**: because `execute_position_conversion()` already
  implements E8-R (matching-fingerprint retry → `already_applied` no-op;
  conflicting-fingerprint retry → hard failure), the CLI reports whichever
  of the three outcomes (`applied` / `already_applied` / `conflict`) the
  service returns, without re-deriving idempotency logic of its own.

### 7.4 Deterministic reporting (WP7-C3) — `backend/manage.py`

Before/after report fields are drawn only from data already computed by
§7.1-§7.3 (parsed manifest, preflight results, and — on `--commit` — the
service's returned `{"status": ..., "transaction_id": ..., "type": ...}`
dict). The report MUST NOT include: database credentials, provider API
keys/tokens, or raw provider HTTP payloads. It MAY include: predecessor/
successor asset IDs and symbols, share/basis/cash figures already present
in the manifest, preflight pass/fail per check ID, and the service status.
Report output is deterministic for a given manifest and repository state
(no wall-clock-dependent or non-canonical ordering in the output).

### 7.5 Cache-purge / bounded-rebuild instructions and rehearsal orchestration (WP7-C4) — `backend/manage.py`, isolated environment only

WP7 does not reimplement cache purging, portfolio rebuild, or shadow
regeneration — Design §13 step 6 assigns bounded rebuild to the existing
rebuild machinery, and WP6 already owns bounded shadow regeneration. WP7's
authorized surface is **instructions and orchestration**, reusing the
existing subcommands as external steps, not new code:

- **cache purge**: document the affected cache-namespace keys (Design §10:
  `quote:asset=<asset_id>:epoch=<date>`,
  `history:5y:1d:asset=<asset_id>:epoch=<date>`) that an operator or a
  thin wrapper must purge after `--commit`, before snapshot refresh;
- **bounded rebuild**: instruct invocation of the existing
  `rebuild_portfolio` subcommand with a `from_date` at or after the
  transition date (Design §8.4, §13 step 6) — WP7 does not add rebuild
  logic, it documents the correct invocation and confirms
  `POSITION_CONVERSION_REBUILD_BOUNDARY` is honored (WP5-owned; §9);
- **shadow regeneration**: instruct invocation of the existing
  `regenerate_paper_portfolios` subcommand, bounded to the transition date
  onward — WP6-owned mechanism, reused not reimplemented; and
- **isolated production-shaped rehearsal** (Sequence §9): a rehearsal
  script/procedure that, against an isolated production-shaped database
  copy only, exercises the full sequence — migration (already applied at
  WP1), registry preparation (§7.3), `--commit` conversion (§7.3), cache
  purge (above), `rebuild_portfolio` (above), `regenerate_paper_portfolios`
  (above), and a transaction-rollback verification — and asserts the
  resulting accounting matches the expected result with zero production
  contact. This rehearsal is the vehicle for the `MINOR-5` and
  `NEW-MINOR-A` WP7-bound portions (§9).

**Rehearsal-environment dependency (reclassified — no longer a Planning
Confirmation blocker; formerly §8 Open Item #2).** No canonical artifact
assigns a named human or team owner for provisioning the isolated
production-shaped rehearsal environment, and none is required for
deterministic CLI implementation: the environment's *contract* is already
fully fixed — isolated, production-shaped, real PostgreSQL, repeatable,
rollback-capable, no production access (Sequence §9). This plan does not
invent a provisioning mechanism or assign an owner. Availability of such an
environment is an **acceptance/rehearsal-execution dependency**: WP7-T11
(§13) and acceptance rows WP7-A11/A12/A14/A15 (§10) cannot complete until
the environment exists, but this dependency does not block Planning
Confirmation itself, which evaluates the plan's design completeness, not
whether every execution-time resource has already been provisioned.

## 8. Design determination and open items

| # | Question | Determination |
|---|---|---|
| 1 | How does the CLI receive `portfolio_id`/`ws_id`? | `RESOLVED — CLOSED THIS REVISION`. [BANPU-WP7 Identity Ingress Design Clarification](BANPU_WP7_IDENTITY_INGRESS_DESIGN_CLARIFICATION.md) §10: required `--portfolio`/`-p` flag supplies `portfolio_id`; `ws_id` derived from `Portfolio.workspace_id`; fail closed on non-resolution; manifest contract unchanged (§7.1) |
| 2 | Who provisions the isolated production-shaped rehearsal database? | `RESOLVED — RECLASSIFIED, NOT A PLANNING BLOCKER`. No canonical artifact assigns provisioning ownership and none is required for deterministic CLI implementation; the environment contract is already fixed by Sequence §9; availability is an acceptance/rehearsal-execution dependency (§7.5), not a design gap |
| 3 | Preflight call order among registry/quote/continuity/boundary/replay checks | `RESOLVED, CORRECTED THIS REVISION`. Live inspection of `validate_position_conversion_registry_state()` (`asset_registry.py:458`) proved it requires post-preparation state (predecessor `MERGED`, successor identifier attached), so the materialized plan's step 1 was defective — it validated an invariant that could exist only after preparation, before allowing preparation to occur. §7.2 now splits pre-preparation (read-only precondition replication), the preparation boundary, and post-preparation validation as distinct, correctly ordered steps |
| 4 | Whether `--commit` needs an override/force flag analogous to `apply_repair --force` | `RESOLVED — NO` (unchanged from materialized plan). Design §11 classifies every WP7-relevant validator finding as `CRITICAL`; Roadmap §9 acceptance criteria require "`--commit` is explicit and refuses any failed preflight" with no stated exception |
| 5 | How is quote-gate protection integrated given `evaluate_candidate_quarantine` needs live provider evidence the CLI does not fetch? | `RESOLVED THIS REVISION`. §7.2 step 2: the manifest-only, provider-independent components (`build_successor_quote_binding`, `evaluate_request_identity`, `check_cache_namespace_mismatch`, `check_reference_price_inadmissible`) are evaluated as preflight; the live-evidence components are correctly left to WP3's already-active, continuous fetch-time gate in `data_fetcher.py`, which requires no new WP7 orchestration |
| 6 | How is mechanical-continuity evidence obtained given the only existing evaluator (`_evaluate_mechanical_continuity`/`_audit_mechanical_continuity`) is private to `manage.py`? | `RESOLVED THIS REVISION`. WP7's new subcommand is added to the same file (`manage.py`), so calling `_evaluate_mechanical_continuity()` directly (the pure, manifest-sourced classifier — not `_audit_mechanical_continuity()`, which needs a persisted snapshot) is an ordinary same-module call, not a cross-module architecture change (§7.2 step 3) |
| 7 | How is "broker-fact" validation integrated given no broker-fact service exists in the repository? | `RESOLVED THIS REVISION`. Repository-wide search found no broker-fact service, API, or validator of any kind. "Broker facts" are manifest-carried, broker-confirmed values (Design §6.2/§9); their validation is discharged entirely by the canonical schema parse (§7.1) and the reference-price-admissibility check already run for the quote gate (§7.2 step 2/4). No separate integration point exists to build |
| 8 | How is "both replay modes" validated before commit given existing replay services operate only on persisted ledger data? | `RESOLVED THIS REVISION`. §7.2 step 6 splits the requirement: an achievable pre-commit sanity check of the *existing* ledger under both `Portfolio.replay_asset_id_native` values; full parity of the *candidate* conversion is rehearsal-owned (§7.5, where mutate-and-discard is safe); an achievable, mandatory post-commit verification of the *materialized* conversion, with `CRITICAL`-anomaly reporting and no invented automated rollback (Design §15's existing backup/restore path governs recovery) |

Fresh latent-ambiguity search performed against this revision (Design §6-9,
§13-15; Roadmap §9; Sequence §9; live code cited throughout §7 above; all
four WP7 lifecycle artifacts): no further implementation-critical design
question was found.

`NO OPEN IMPLEMENTATION-CRITICAL DESIGN DECISIONS`

## 9. Residual treatment

Preserved exactly, without definition, resolution, waiver, or
reinterpretation:

| Item | Carried state |
|---|---|
| `MINOR-5` — WP7 rehearsal portion | Planned in §7.5 (real PostgreSQL upgrade rehearsal, repeated-upgrade rehearsal, constraint/index probes, guarded-downgrade rehearsal, all inside the isolated production-shaped rehearsal). This plan schedules the rehearsal task (§13); it does not execute it and does not discharge the residual |
| `MINOR-5` — WP8 release-evidence portion | Not a WP7 capability. `BANPU_WP1_FREEZE_RECORD.md` §7 names WP8 as sole owner of this portion; this plan does not claim, plan, or discharge it. WP7's rehearsal evidence may later be consumed by WP8 without transferring ownership (Authorization Record §6) |
| `NEW-MINOR-A` — WP7 production-dialect-rehearsal portion | Planned in §7.5, folded into the same isolated production-shaped rehearsal as `MINOR-5`'s portion (both require real-PostgreSQL execution). Evidence requirements strengthened this revision (§10, WP7-A15): the rehearsal must produce (1) documented PostgreSQL coercion behavior for the canonical stored-value rule, (2) proof that persisted rows satisfy the canonical naive-midnight stored-value invariant, (3) proof that service-authored rows satisfy the same invariant, (4) all of the above against real PostgreSQL in the isolated rehearsal, not SQLite. Not discharged by this plan; WP4's authoring-portion ownership remains closed and is not reopened |
| `NEW-MINOR-A` — WP4 authoring portion | WP4-owned, closed. `BANPU_WP1_FREEZE_RECORD.md` §7; untouched by this plan |
| `PD-3` | Unassigned, open, referred out per `BANPU_WP3_ALLOCATION_RECORD.md` and confirmed unassigned by every WP4/WP5/WP6 Allocation Record and `BANPU_WP6_EPIC_CLOSEOUT.md` §15. This plan does not claim or assign it to WP7, does not treat it as a WP7 task, deliverable, acceptance criterion, or implicit prerequisite. §7 identifies no genuine WP7 dependency on `PD-3`; if implementation later discovers one not already established by canonical authority, implementation must stop and escalate constitutionally rather than absorb it (§12) |
| `MINOR-1` | WP4-owned, closed; untouched by WP7 |
| `MINOR-2` (WP3/WP5-owned) and `POSITION_CONVERSION_REBUILD_BOUNDARY` (WP5-owned) | Not WP7 capabilities. §7.2/§7.5 above consult, but do not own or discharge, the boundary predicate they reference |
| WP2 `MINOR-A`, `MINOR-B`, `OBSERVATION-A` | Carried unchanged, no obligation text invented |
| WP3 `OBSERVATION-IC-1`, `OBSERVATION-IC-2`, `OBSERVATION-SR-1`, `OBSERVATION-SR-2` | Carried unchanged, non-blocking |
| WP4's baseline missing-log assertion, temporary-path permission condition, `B1`-`B6`, `RTO-1`-`RTO-13`, `PIA-1`-`PIA-4` | Carried forward at BANPU-WP4 Epic Closeout unchanged |

This plan creates no residual-discharge authority. WP7-owned open items
after this plan are — until implementation actually occurs — every
capability in §4, the two rehearsal-bound residual portions above, and
nothing else.

## 10. Acceptance matrix

| ID | Canonical criterion | Revised task | Verification method | Required evidence | Planning coverage |
|---|---|---|---|---|---|
| WP7-A1 | No flags performs no write | T6 | new CLI test file, DB-diff assertion | zero-diff proof across manifest load + preflight steps 1-5 | `COMPLETE` |
| WP7-A2 | `--dry-run` performs no write | T6 | new CLI test file, DB-diff assertion | identical to WP7-A1 | `COMPLETE` |
| WP7-A3 | `--commit` is explicit and refuses any failed preflight | T5, T6 | new CLI test file, one negative fixture per preflight step 1-5 | non-zero exit, no write, on each induced failure | `COMPLETE` |
| WP7-A4 | Re-running the same manifest is an `already_applied` no-op | T6 | new CLI test file | `execute_position_conversion` E8-R matching-fingerprint outcome surfaced verbatim | `COMPLETE` |
| WP7-A5 | A conflicting manifest fails | T6 | new CLI test file | `execute_position_conversion` E8-R conflicting-fingerprint outcome surfaced verbatim | `COMPLETE` |
| WP7-A6 | The command never broadens scope to generic corporate actions | T12 | diff review against §5.1 at implementation review | diff limited to §5.1 file surface | `COMPLETE` |
| WP7-A7 | CLI parser and transaction-boundary tests pass | T3, T4 | new CLI test file | `--portfolio`/`-p` parsing and fail-closed lookup (§7.1) covered | `COMPLETE` |
| WP7-A8 | No-flag/dry-run database diff equals zero | T6 | new CLI test file, DB-diff assertion | same evidence as WP7-A1/A2 | `COMPLETE` |
| WP7-A9 | Manifest schema, registry (pre- and post-preparation), quote-gate (manifest-only components), continuity, rebuild boundary, and existing-ledger both-replay-mode checks each fail closed independently | T4, T5 | new CLI test file, one negative fixture per §7.2 step 1-5 and one for the pre-commit half of step 6 | independent fail-closed proof per check, per corrected §7.2 ordering | `COMPLETE` |
| WP7-A10 | Deterministic before/after report; no credential or raw provider payload exposure | T7 | new CLI test file, report-content assertion | field allowlist from §7.4 enforced | `COMPLETE` |
| WP7-A11 | Isolated production-shaped rehearsal covers migration, registry preparation, quote gate, continuity, conversion, post-commit both-replay-mode verification, bounded rebuild, shadow regeneration, and transaction rollback | T11 | rehearsal procedure evidence | full-sequence rehearsal log against real PostgreSQL | `BLOCKED — CAPABILITY GAP` (environment-execution dependency, §7.5; not a design gap — see §8 #2) |
| WP7-A12 | Rehearsal touches no production system | T11 | rehearsal procedure evidence, environment-isolation proof | connection-string/target isolation proof | `BLOCKED — CAPABILITY GAP` (same dependency as WP7-A11) |
| WP7-A13 | No public conversion endpoint exists | T12 | diff review — no `backend/main.py` or route change | diff review | `COMPLETE` |
| WP7-A14 | `MINOR-5` WP7 rehearsal portion demonstrated (real PostgreSQL upgrade, repeated upgrade, constraint/index probes, guarded downgrade) | T11 | rehearsal procedure evidence | `BANPU_WP1_FREEZE_RECORD.md` §7 evidence list | `BLOCKED — CAPABILITY GAP` (same dependency as WP7-A11) |
| WP7-A15 | `NEW-MINOR-A` WP7 production-dialect-rehearsal portion demonstrated, strengthened evidence (§9) | T11 | rehearsal procedure evidence | 4-point evidence list, §9 `NEW-MINOR-A` row | `BLOCKED — CAPABILITY GAP` (same dependency as WP7-A11) |
| WP7-A16 | No forbidden surface change (public API routes, frontend, core accounting equations, production DB/cache, M46) | T12 | diff review; regression suites for those modules stay green and untouched | §11 regression suite results | `COMPLETE` |
| WP7-A17 | Post-commit both-replay-mode verification runs after every successful `--commit` and blocks cache-purge/rebuild on mismatch | T6 | new CLI test file | induced post-commit mismatch fixture halts before §7.5 steps | `COMPLETE` |
| WP7-A18 | Registry pre-preparation checks (§7.2 step 1) never call a mutating registry function | T5 | new CLI test file / code review at implementation review | no `attach_identifier`/`retire_identifier`/`transition_status`/`link_relationship` call before the preparation boundary | `COMPLETE` |
| WP7-A19 | Mechanical-continuity preflight calls only the pure `_evaluate_mechanical_continuity()`, never `_audit_mechanical_continuity()`, before commit | T5 | code review at implementation review | call-site inspection | `COMPLETE` |

All canonical criteria have `COMPLETE` planning coverage except WP7-A11,
A12, A14, and A15, which are `BLOCKED — CAPABILITY GAP` solely on the
rehearsal-environment execution dependency reclassified in §7.5/§8 #2 — not
on any unresolved design or implementation-critical question. No criterion
above is marked `PASS` by this plan — planning materializes the matrix; it
does not execute it.

## 11. Verification strategy

Implementation must keep green, unmodified in expectation:

- `backend/tests/test_asset_registry.py`, `test_position_conversion_live.py`,
  `test_transaction_canonicalizer.py` (WP4's frozen surface — proves WP7
  did not edit the registry write path or `execute_position_conversion`);
- `backend/tests/test_position_conversion_quote_contract.py` (WP3's frozen
  surface — proves WP7 did not edit quote-epoch/quarantine logic);
- `backend/tests/test_shadow_regeneration.py`, `test_horizon_grader.py`,
  `test_ideal_series.py` (WP6's frozen surface);
- `backend/tests/test_portfolio_metrics.py`, `test_portfolio_rebuilder.py`,
  `test_verify_snapshots.py` (WP5's frozen surface — proves WP7 did not
  reach into WP5's closed files or reinterpret the rebuild boundary).

New/added coverage must satisfy §10's acceptance matrix in full.
`graphify update .` must be run before implementation review, per the
top-level CLAUDE.md rule (this plan is documentation-only and does not
itself trigger that rule — see §14 verification table).

## 12. Explicit exclusions

This plan does not decompose, and WP7 implementation may not perform:

- any public API endpoint, route, or frontend authoring path (Sequence §9
  exit criteria: "No public conversion endpoint exists");
- any schema, model, or migration change of any kind;
- any change to `RecommendationSnapshot`, `OptimizerHistory`,
  `UserExecutionDecision`, or `RecommendationGrade` schema, or any
  mutation/rewrite of a historical recommendation or decision payload;
- any change to `backend/services/portfolio_transactions.py`,
  `asset_registry.py`, `position_conversion_quote_contract.py`,
  `portfolio_rebuilder.py`, `shadow_tracker.py`, or any other WP3/WP4/WP5/
  WP6 frozen and closed surface — WP7 calls these modules, it does not
  edit them;
- any actual production execution, cache mutation, or production-data
  mutation of any kind — the CLI's `--commit` path targets only whatever
  database the operator points it at, and no production invocation is
  authorized by this plan or its authority chain;
- reopening, reinterpreting, or silently deviating from any §8 determination
  at implementation time; §8 now records `NO OPEN IMPLEMENTATION-CRITICAL
  DESIGN DECISIONS` and implementation must follow its determinations
  exactly, not invent an alternative;
- resolving, narrowing, discharging, or waiving `MINOR-5`'s WP8 portion,
  `NEW-MINOR-A`'s WP4 portion, `MINOR-2`, `POSITION_CONVERSION_REBUILD_BOUNDARY`,
  `PD-3`, or any other residual (§9);
- introducing a general corporate-action dispatcher or event vocabulary, or
  expanding the general asset-definition vocabulary;
- remapping any unrelated symbol;
- any BANPU-WP8 or M46 act;
- production deployment or deployment authorization; and
- staging, committing, pushing, merging, or publishing repository changes
  under color of this plan.

## 13. Implementation sequencing

| Task | Work | Depends on | Deliverable / evidence |
|---|---|---|---|
| WP7-T1 | Record entry baseline: repository state, frozen WP1-WP6 identities, test commands, pre-existing failures, §5 file allowlist | Authorization | Reproducible entry-gate record |
| WP7-T2 | Fix the CLI argument surface: `--portfolio`/`-p` (required), FK-derived `ws_id`, fail-closed lookup (§7.1) — mechanical implementation of the already-resolved identity-ingress determination, not a design act | T1 | Fixed CLI signature; unblocks T3-T7 |
| WP7-T3 | Author failing tests WP7-A1-A3, WP7-A7-A9, WP7-A18, WP7-A19 (parser, preflight steps 1-5, dry-run/commit safety, pre-preparation-only registry calls, pure-classifier-only continuity calls) | T2 | Obligations expressed before code |
| WP7-T4 | Implement manifest loading and schema validation (§7.1) | T2, T3 | WP7-C1 (parsing half), WP7-C2 (schema half) |
| WP7-T5 | Implement preflight steps 1-5 (§7.2): pre-preparation registry preconditions, manifest-only quote-gate components, pure mechanical-continuity classifier, broker-fact discharge via schema parse, rebuild-boundary consistency | T4 | WP7-C2 (registry/quote/continuity/broker/boundary halves) |
| WP7-T6 | Implement the corrected commit sequence (§7.3): registry preparation boundary → post-preparation registry validation → `execute_position_conversion()` → post-commit both-replay-mode verification (§7.2 step 6); implement dry-run/no-flags branching and idempotency reporting | T5 | WP7-C1 (commit-gate half); WP7-A4, WP7-A5, WP7-A17 |
| WP7-T7 | Implement deterministic reporting (§7.4), including the dry-run proven-vs-not-provable distinction (§7.3) | T6 | WP7-C3 |
| WP7-T8 | Author failing tests WP7-A4-A6, WP7-A10, WP7-A13, WP7-A16, WP7-A17 (idempotency, conflict, scope-containment, reporting, negative diff checks, post-commit-mismatch halt) | T6, T7 | Obligations expressed before rehearsal work |
| WP7-T9 | Document cache-purge / bounded-rebuild instructions (§7.5) | T7 | WP7-C4 (documentation half) |
| WP7-T10 | Obtain the isolated production-shaped rehearsal environment (execution dependency, §7.5/§8 #2 — infrastructure availability, not a design or implementation task) | T1 | Unblocks T11 |
| WP7-T11 | Execute the isolated production-shaped rehearsal (§7.5), including full candidate-conversion both-replay-mode parity (§7.2 step 6); produce `MINOR-5`/strengthened `NEW-MINOR-A` WP7-portion evidence (§9) | T9, T10 | WP7-C4 (rehearsal half); WP7-A11, WP7-A12, WP7-A14, WP7-A15 evidence |
| WP7-T12 | Run the full §10 matrix and the §11 regression suites; `graphify update .` | T3, T4, T5, T6, T7, T8, T11 | Complete WP7 evidence set |
| WP7-T13 | Prepare the independent implementation-review submission | T12 | Review-ready candidate; no confirmation, freeze, or closeout performed |

T10 is an execution-dependency task (infrastructure availability), not a
design-resolution task — it may proceed in parallel with T2-T9 and only
gates T11. No task in this table is conditional beyond its stated
dependency.

## 14. WPP maturity/status

`WORK PACKAGE PLAN REVISED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED —
NOT CONFIRMED — NOT FROZEN — READY FOR INDEPENDENT PLANNING CONFIRMATION`,
using the exact maturity terminology `BANPU_WP6_WORK_PACKAGE_PLAN.md`
established as valid current BANPU precedent (its own header, line 4), with
the revision qualifier this plan's own §0 records. This plan does not claim
confirmation, approval, freeze, or implementation-readiness merely because
it has been revised. Per §8, `NO OPEN IMPLEMENTATION-CRITICAL DESIGN
DECISIONS` remain; the sole remaining gaps (WP7-A11/A12/A14/A15,
`BLOCKED — CAPABILITY GAP`) are execution-time dependencies on an
infrastructure resource (§7.5), not unresolved design questions. Any
required confirmation, binding, or freeze remains a separate, later act.

### 14.1 Repository verification of this revision act

| Verification | Result |
|---|---|
| Only path modified by this act | `SATISFIED` — `docs/implementation/BANPU_WP7_WORK_PACKAGE_PLAN.md` (§0 above records the superseded before-identity; the final report accompanying this revision records the after-identity) |
| Allocation Record, Implementation Authorization Record, or Identity Ingress Design Clarification modified | `NONE` |
| Frozen BANPU artifacts modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX files modified | `NONE` — all live-code reads in this revision were read-only inspection |
| `graphify update .` | not run — documentation-only revision act, no code changed, mirroring the WP6 Work Package Plan §14.1 waiver logic |
| Commit created | `NO` |

## 15. Exact next constitutional act

A single next constitutional act follows from this revision: **BANPU-WP7
Planning Confirmation** (the repository's established equivalent — see
`BANPU_WP6_PLANNING_CONFIRMATION.md` — performed by a reviewer distinct from
this planning authority), covering the full §10 acceptance matrix against
this revised plan. This plan does not perform that confirmation, and does
not claim it has occurred.
