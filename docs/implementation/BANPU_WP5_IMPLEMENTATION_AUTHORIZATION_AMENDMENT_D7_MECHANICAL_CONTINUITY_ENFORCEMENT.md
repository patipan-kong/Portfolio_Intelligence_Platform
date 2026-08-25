# BANPU-WP5 — Implementation Authorization Amendment: D7 Mechanical-Continuity Enforcement Locus

**Artifact class:** Additive constitutional Implementation Authorization amendment (prepared, not yet binding)

**Amendment date:** 2026-08-14

**Issuing authority:** BANPU-WP5 Implementation Authorization Amendment Authority (this act names no broader standing role for itself; scope is strictly the D7 locus question below)

**Original Implementation Authorization Record:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md), raw SHA-256 `DBCBC2BFCDB9F3A7D3E7912C6148445C68C39F5872A4DE2DEF58DF5B2BDE7F1E`, 19,039 bytes, 341 lines, disposition `BANPU-WP5 IMPLEMENTATION AUTHORIZED`

**Authoritative design clarification (binding input, not reopened):** [`BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md`](BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md), raw SHA-256 `8DD43B1202714213E9EF88A65582E59A492680B747412BDAC9F176D3C43A2223`, 16,491 bytes, 158 lines, outcome `DESIGN CLARIFICATION COMPLETE — HUMAN-AUTHORIZED NORMATIVE SEMANTICS ESTABLISHED — D7 NOT AUTHORIZED`

**Work Package Plan referenced (not amended):** [`BANPU_WP5_WORK_PACKAGE_PLAN.md`](BANPU_WP5_WORK_PACKAGE_PLAN.md), raw SHA-256 `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523`, 42,903 bytes, 604 lines, §10.4 `PLANNING BLOCKER`

**Disposition:** `D7 IMPLEMENTATION AUTHORIZATION AMENDMENT PREPARED — NOT YET BINDING`

**Implementation reliance:** `PROHIBITED — IMPLEMENTATION MUST NOT YET RELY ON THIS AMENDMENT (see §15)`

**Implementation performed:** `NO`

**WPP amended:** `NO` (§17 records what a future WPP amendment must incorporate)

**Independent reapproval or binding freeze performed:** `NO`

**Release/deployment/production-mutation authority created:** `NONE`

---

## 1. Nature and boundary of this act

This act performs exactly one thing: it determines and (subject to §15's non-binding qualification) prepares the grant of a D7 mechanical-continuity enforcement/classification locus for the predicate whose formula, inclusivity, rounding, and annotation semantics were fixed by the human-authorized design clarification. It does not implement code, does not amend the WP5 Work Package Plan, does not perform independent reapproval, does not perform binding freeze, does not perform Planning Confirmation or Freeze, does not execute reconstruction, does not mutate production data, and does not reopen D2/D4/D5/D6.

## 2. Independent verification

Independently re-verified from live repository state immediately before drafting this amendment (not accepted from prompt text):

| Item | Verification | Result |
|---|---|---|
| `BANPU_WP5_ALLOCATION_RECORD.md` | present, `BANPU-WP5 ALLOCATED`, 15,590 bytes / 280 lines / SHA-256 `D00D0AE886E6150F84663AA331338F764E193700EBCE944C88CB0D175CA8D687` | `EXACT` |
| `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | present, `BANPU-WP5 IMPLEMENTATION AUTHORIZED`, identity above | `EXACT` |
| `BANPU_WP5_WORK_PACKAGE_PLAN.md` | present, `MATERIALIZED — NOT CONFIRMED/FROZEN`, §10.4 `PLANNING BLOCKER` (formula unresolved at plan time) | `EXACT` |
| `BANPU_MECHANICAL_CONTINUITY_DESIGN_CLARIFICATION.md` | present, `DESIGN CLARIFICATION COMPLETE`, §14 explicitly reserves D7 to "a subsequent, separate WP5 Implementation Authorization amendment" | `EXACT` — this act is that named successor |
| Design §10 (re-read live) | "Before activation, mechanical boundary value MUST reconcile within the payload tolerance..."; "quarantined for... mechanical continuity failure, or an unannotated boundary discontinuity" | unchanged since the clarification act |
| `position_conversion_quote_contract.py` `QuarantineReason` (re-read live) | class docstring: "Mechanical continuity failure and unannotated boundary discontinuity are design §10's WP5-owned half... deliberately absent from this enumeration" | unchanged; WP3 module frozen |
| Prior WP5 mechanical-continuity governance chain | `..._RECONCILIATION_GOVERNANCE_DECISION.md` (`PARTIAL`), `..._COMPETENT_AUTHORITY_DETERMINATION.md` (`OUTCOME C`), `..._DESIGN_CLARIFICATION_COMPETENT_AUTHORITY_DETERMINATION.md` (`BLOCKED`), `BANPU_DESIGN_AMENDMENT_AUTHORITY_DETERMINATION.md` (`BLOCKED`) | all present, unchanged, superseded only for D2/D4/D5/D6 by the design clarification — none purported to grant D7 | `CONFIRMED — NO INTERVENING D7 GRANT` |
| WP4 Retry-Order amendment chain (four files, re-read) | Governance Decision → Plan Amendment ("not yet independently reapproved," implementation reliance "PROHIBITED") → Independent Reapproval ("PERMITTED under existing bounded authorization") → Binding Freeze Record | present, unchanged; used as structural precedent (§16) |
| Roadmap §7 / Sequence §7 | re-read live; unchanged since the Authorization Record's own citation | `EXACT` |
| Package/file inventory governing WP5 | Authorization Record §4.1/§4.2, re-read live | `EXACT` — see §12 below |
| `git status` overlap check | only pre-existing WP4-authorized files and the additive BANPU-WP4/WP5/M-corpus governance files; no WP5 production/test file touched; no new implementation file present | `NO OVERLAPPING CHANGE` |

Confirmed premises: (1) the design clarification exists and is unsuperseded; (2) D7 remains unauthorized prior to this act; (3) no implementation has occurred; (4) no intervening act has expanded WP5's authorized capability or file surface. All four hold; this act proceeds.

## 3. D7 authorization/amendment precedent

The only in-repository precedent for adding capability to an already-authorized BANPU work package is the **BANPU-WP4 Retry-Order chain**: `Governance Decision` (selects semantics, disposition `PREPARED — INDEPENDENT APPROVAL AND PLAN REAPPROVAL REQUIRED`, implementation reliance `NONE UNTIL SUCCESSOR GOVERNANCE ACTS COMPLETE`) → `Work Package Plan Amendment` (operationalizes the decision into the Plan, disposition `PREPARED — NOT YET INDEPENDENTLY REAPPROVED`, implementation reliance explicitly `PROHIBITED`) → `Independent Reapproval` (disposition `INDEPENDENTLY REAPPROVED`, implementation reliance now `PERMITTED UNDER EXISTING BOUNDED... AUTHORIZATION`) → `Binding Freeze Record`.

This act sits at the **first** position in that chain's shape — it is the act that determines and records the selected D7 semantics, analogous to the Retry-Order Governance Decision, not to the Plan Amendment itself (WP5's WPP is not amended here; §17). Per that precedent, an act at this position is **not implementation-reliable** until it passes through the remaining chain positions. §15 applies this precedent explicitly.

## 4. Live architecture inspected

Read directly from the working tree (not inferred from roadmap forecasts):

- **`backend/manage.py`** lines 789–1311: the `verify_snapshots` audit subsystem — `AuditSeverity` (`WARNING`/`CRITICAL`), `AuditCheck` enum (`NAV_CONTINUITY`, `PNL_CONTINUITY`, `HOLDINGS_INTEGRITY`, `PRICE_INTEGRITY`, `RETURN_SANITY`), `AuditAnomaly`/`PortfolioAuditResult` dataclasses, five `_audit_*` check functions each returning `list[AuditAnomaly]`, `_audit_portfolio()` (the per-portfolio dispatcher), and `_cmd_verify_snapshots()` — confirmed read-only ("Read-only snapshot integrity audit. Never modifies the database.") with exit codes `0` (clean) / `1` (warnings only) / `2` (any critical).
- **`backend/services/portfolio_rebuilder.py`** lines 2259–2280 and the `_resolve_conversion_successors()` call site: confirmed this is the exact point WP5's WPP §8 already identified for the (distinct) `POSITION_CONVERSION_REBUILD_BOUNDARY` refusal guard — immediately after `conversion_successors = _resolve_conversion_successors(...)`, before `rebuild_dates` is computed, before any write or provider fetch.
- **`backend/services/transaction_canonicalizer.py`** lines 145–187 and 326: the frozen, WP1-owned typed model — `PositionConversionBoundaryEvidence(predecessor_reference_price, successor_reference_price, mechanical_nav_tolerance_pct, suspension_gap_annotation)`, `PositionConversion(conversion_ratio, boundary_evidence, ...)`, and the public, side-effect-free `parse_position_conversion_payload(payload) -> PositionConversionParseResult` (exposing `.value`/`.is_valid`). This is the canonical, already-parsed source for every D2 operand; no WP5 code re-parses the raw JSON.
- **`backend/services/market_data/position_conversion_quote_contract.py`** lines 41–353: WP3's frozen quote-protection/quarantine module. Its `QuarantineReason` enum is confirmed, by its own class docstring, to be "exhaustive over design §10's WP3-scoped quarantine conditions," with "mechanical continuity failure" and "unannotated boundary discontinuity" **deliberately absent** and named as "design §10's WP5-owned half." This module is frozen; WP5's Authorization Record §4.1/§11 already forbids editing it or adding a `QuarantineReason` member.
- **`backend/services/portfolio_metrics.py`**, **`snapshot_return_recovery.py`**, **`portfolio_snapshots.py`**: re-confirmed (per WPP §6, re-read live) to contain no `POSITION_CONVERSION`-specific reconciliation logic and no natural per-conversion (as opposed to per-snapshot) iteration point.
- **`backend/services/data_fetcher.py`**: found to reference `boundary_evidence`-adjacent fields but confirmed to belong to WP3's live provider-adaptation path (a distinct value class per the quote-contract module's own docstring: "never a provider `current_close`/`previous_close`"), not WP5's authorized surface.

Actual call/data flow determined:

1. **Reading boundary evidence:** only through `transaction_canonicalizer.parse_position_conversion_payload()`, invoked against a `Transaction` row's raw payload; `portfolio_rebuilder.py` already does this via `ctx.position_conversion` for its own (different) purposes.
2. **Rebuilding snapshots:** `rebuild_portfolio()` — a separate CLI/service entry point (`apply_position_conversion` / rebuild tooling), never invoked by `verify_snapshots`.
3. **Verifying snapshots:** `manage.py verify_snapshots` — a wholly separate, read-only CLI command with no call-path overlap with `rebuild_portfolio()`.
4. **Classifying/accounting conversion:** `portfolio_metrics.py`/`snapshot_return_recovery.py` (WP5-C1/C2, already authorized, unrelated to D7).
5. **Reporting continuity anomalies:** no existing mechanism; `verify_snapshots`'s `AuditAnomaly` structure is the only existing read-only, non-mutating result/reporting structure in WP5's authorized surface capable of hosting a new finding without crossing into WP3's frozen `QuarantineReason` enum or WP4's frozen materialization surface.

No code was modified during this inspection.

## 5. D7 option analysis

**Option A — WP5 read-only classifier/helper (standalone).** Provides the cleanest *conceptual* boundary (pure function, D2–D6 in, four-state result out) but, evaluated alone, does not specify a consumer or a code location, leaving the actual capability inert. Necessary as a *shape*, insufficient as a *complete* locus determination.

**Option B — Existing WP5 verification path (`manage.py` `verify_snapshots`).** This exact path already has: (i) explicit prior authorization — the original Authorization Record §4.1 already permits `backend/manage.py`, "strictly bounded to conversion-boundary classification inside `verify_snapshots`, and only if that classification is required to satisfy this scope"; (ii) an already-planned, structurally identical precedent — WPP §6/§10.3 already scoped "one new, additive audit check function invoked from `_audit_portfolio` only for portfolios whose ledger contains a `POSITION_CONVERSION`" for the *tolerance-admissibility* half of the same predicate family, deferring only the *reconciliation* half (§10.4) because the formula was then unfixed; (iii) the exact `AuditCheck`/`AuditSeverity`/`AuditAnomaly` data shape already in production use for four structurally analogous checks; and (iv) a confirmed read-only, non-mutating, CLI-only invocation with no call-path overlap with reconstruction. Sufficient canonical inputs are available (§11). No inappropriate CLI ownership of *domain semantics* is created, because the domain semantics (D2–D6) were already fixed by the design clarification, not invented by `manage.py` — `manage.py` only hosts the classification's read-only reporting, exactly as it already does for `NAV_CONTINUITY`, `HOLDINGS_INTEGRITY`, etc.

**Option C — Reconstruction guard (coupled to `portfolio_rebuilder.py`).** Rejected as the primary locus. Design §10's "before activation" language concerns whether a converted holding's *price* may be used at all (a market-data/quote-protection concern, §10's own paragraph structure places it adjacent to WP3's quarantine mechanism, not to reconstruction-boundary refusal). Coupling D7 to `POSITION_CONVERSION_REBUILD_BOUNDARY` would improperly merge two predicates the design clarification (§3, preserved) and the WPP (§8 vs. §10) already treat as structurally distinct: one guards *which dates may be reconstructed*, the other classifies *whether a specific conversion's boundary prices are mechanically coherent*. A portfolio can fail mechanical continuity and still have every date fully reconstructible, and vice versa. **Rejected**; see §8 below for the binding separation statement.

**Option D — Combination (pure classifier + multiple authorized consumers).** Rejected as unnecessary. Nothing in the design, Roadmap §7, or the WPP identifies a second genuine consumer beyond `verify_snapshots`; the literal "quarantine... blocks affected snapshots and downstream optimizer/evaluation refresh" reading of design §10 belongs to WP3's frozen provider-adaptation/quote-protection pipeline (§6 below), which is outside WP5's authorized file surface entirely and is not extended by this act. Inventing a second consumer here would exceed "the minimum WP5 code/package surface needed."

**Option E — New WP5-owned module.** Rejected as unnecessary. `manage.py` already provides a complete, already-authorized, structurally-precedented hosting location (Option B) requiring no new file and no new dataclass shape. A new module would add authorized surface beyond what §4.1 of the original Authorization Record already grants, contrary to the "minimum surface" instruction.

## 6. Selected classifier ownership/locus

**Option B, refined**, combining a pure computation with a single existing authorized consumer:

- A new, WP5-owned, **pure, read-only function** (module-private to `manage.py`, e.g. `_evaluate_mechanical_continuity(boundary_evidence, conversion_ratio) -> MechanicalContinuityResult`) implements exactly the D2/D4/D5/D6 predicate fixed by the design clarification and returns one of the four semantic outcomes (§12 below). It performs no I/O, no DB access, and no side effect.
- A new, WP5-owned **check function** (`_audit_mechanical_continuity(db, portfolio) -> list[AuditAnomaly]`), following the existing `_audit_*` pattern exactly, queries the portfolio's `Transaction` rows for `transaction_type == "POSITION_CONVERSION"` (read-only), parses each via the frozen `parse_position_conversion_payload()`, and — for each structurally valid payload — calls the pure function above and translates its result into zero or one `AuditAnomaly` (§7).
- This check function is invoked from the existing `_audit_portfolio()` dispatcher (manage.py:1123–1151), exactly once per conversion-bearing portfolio, alongside the four existing per-snapshot checks but structured as a per-conversion check (it does not iterate `PortfolioSnapshot` rows).

This is the literal completion of what the WPP already began at §10.3 and explicitly deferred at §10.4 pending the formula. No new file, no new top-level module, and no change to `AuditSeverity`, `AuditAnomaly`, or `PortfolioAuditResult`'s existing shape is required — only one new `AuditCheck` enum member and two new functions, all inside the file already authorized for exactly this purpose.

## 7. Authorized consumer(s)

**Exactly one:** `manage.py`'s `verify_snapshots` CLI command, via `_audit_portfolio()`. No other consumer (not `rebuild_portfolio()`, not `portfolio_metrics.py`, not any public endpoint — none exists — and not WP3's quote-contract module) is authorized to invoke or consume this classification by this act.

## 8. Outcome handling

| Result | Treatment |
|---|---|
| `PASS` | No `AuditAnomaly` emitted. Verification proceeds normally; contributes nothing to `warnings`/`criticals` counts or exit code. |
| `ANNOTATED_BOUNDARY_DISCONTINUITY` | One `AuditAnomaly` emitted at `AuditSeverity.WARNING`, `check = AuditCheck.MECHANICAL_CONTINUITY`, description naming the evidenced/annotated discontinuity, `details` carrying the preserved `metric_pct`, `mechanical_nav_tolerance_pct`, and the (trimmed) `suspension_gap_annotation` text. This is visible in `verify_snapshots` output and contributes to exit code `1` (warnings) if no other CRITICAL exists — never to `2`. It does **not** erase the return, modify NAV, rewrite any snapshot value, or become external cash flow; `verify_snapshots` is, and remains, read-only. It does **not** automatically fail merely because `metric_pct > tolerance` — that is precisely the case this classification exists to distinguish from an unexplained defect. |
| `MECHANICAL_CONTINUITY_FAILURE` | One `AuditAnomaly` emitted at `AuditSeverity.CRITICAL`, `check = AuditCheck.MECHANICAL_CONTINUITY`, `details` carrying `metric_pct` and `mechanical_nav_tolerance_pct`. **Fail-closed for verification acceptance only** — it contributes to `verify_snapshots`'s exit code `2`, exactly as `HOLDINGS_INTEGRITY`'s invalid-JSON case already does for a structural defect. It creates **no** production-mutation authority, **no** reconstruction-refusal behavior, and **no** authority to block, quarantine, or filter live price usage (that would require WP3's frozen surface — out of scope; §5 Option D). This is the strongest behavior actually justified within WP5's current authorized surface. |
| `NOT_EVALUABLE` | One `AuditAnomaly` emitted at `AuditSeverity.CRITICAL`, `check = AuditCheck.MECHANICAL_CONTINUITY`, with a description distinct from `MECHANICAL_CONTINUITY_FAILURE`'s (e.g. "mechanical continuity not evaluable — malformed or degenerate boundary evidence") so operators can distinguish "reconciliation failed" from "reconciliation could not be attempted." Treated as CRITICAL, not diagnostic-only and never silently `PASS`, because a structurally-valid `POSITION_CONVERSION` payload whose `boundary_evidence` prices are non-finite or non-positive is itself a data-integrity defect that `verify_snapshots` exists to surface; the design clarification's own §6 confirms this case is distinct from, and does not re-derive, WP3's separate "missing/non-positive prices" quarantine reason (a different value class — live provider quotes, not the payload's stored `boundary_evidence`). |

A structural payload-parse failure (`parse_position_conversion_payload(...).is_valid is False`) is **out of scope** for this predicate — it is a more fundamental integrity defect than D2/D4/D5/D6 addresses and is not newly authorized, reported, or addressed by this amendment, to avoid inventing a capability beyond the design clarification's scope.

## 9. Relationship and ordering with `POSITION_CONVERSION_REBUILD_BOUNDARY`

Binding separation, per §5 Option C's rejection and the design clarification's preserved §3:

- **They execute independently.** `POSITION_CONVERSION_REBUILD_BOUNDARY` executes only inside `rebuild_portfolio()` (`portfolio_rebuilder.py`); the D7 mechanical-continuity classifier executes only inside `verify_snapshots` (`manage.py`). These are two separate CLI/service entry points with no shared call path under this amendment.
- **No ordering exists between them** because neither is ever invoked from within the other's execution.
- **Neither's failure implies anything about the other.** A portfolio may fail `POSITION_CONVERSION_REBUILD_BOUNDARY` (an attempted rebuild with an inadmissible `from_date`) while its stored conversion's mechanical continuity is perfectly sound, and vice versa — a fully rebuildable portfolio may still carry a `MECHANICAL_CONTINUITY_FAILURE` finding in `verify_snapshots` if its boundary evidence itself is defective.
- **Either may run without the other.** `verify_snapshots` may be run against a portfolio that is never rebuilt; `rebuild_portfolio()` may be invoked against a portfolio that has never been through `verify_snapshots`. This act creates no new dependency in either direction.

They remain two distinct WP5-owned predicates, as the design clarification and WPP already established; this amendment does not collapse them.

## 10. Read-only vs. fail-closed determination

Resolved per the invocation's own preferred separation of concerns:

- The classifier itself (§6, `_evaluate_mechanical_continuity`) is a **pure semantic classification** — no I/O, no fail-closed behavior of its own; it only returns one of four values.
- **Failure policy belongs to the consumer**, not the classifier: `_audit_mechanical_continuity`/`verify_snapshots` (the sole authorized consumer, §7) applies `AuditSeverity` and exit-code policy exactly as it already does for the four existing checks. This is a **read-only classifier whose result is consumed by a fail-closed-for-verification-acceptance-only policy** — the third option the invocation itself offered, and the one already structurally present in `manage.py`.
- No component authorized by this act is fail-closed for *reconstruction* or for *any write path*. `verify_snapshots` remains, and this amendment keeps it, entirely non-mutating.

## 11. Invocation point and ordering (verification path)

D7's classification belongs immediately alongside the existing per-portfolio checks in `_audit_portfolio()` (manage.py:1123–1151), invoked once per portfolio whose ledger contains at least one `POSITION_CONVERSION` transaction, logically after the portfolio's snapshot rows are loaded (order within `_audit_portfolio()` is immaterial since the new check does not depend on `PortfolioSnapshot` state — it depends only on the `Transaction` ledger). It is not placed relative to `NAV_CONTINUITY`/`PNL_CONTINUITY`/etc. in any load-bearing way; those are per-snapshot, this is per-conversion. `manage.py` is not made "owner of domain semantics" by this placement — the semantics were already fixed by the design clarification; `manage.py` only hosts their read-only reporting, identically to how it already hosts `NAV_CONTINUITY`'s semantics (defined by design/roadmap, not invented by the CLI).

Reconstruction-path ordering (§7 of the invocation's instructions) is **not applicable** — no reconstruction consumer is authorized by this act (§7 above).

## 12. Canonical inputs

Exclusively, and only from already-canonical, already-frozen sources:

- `conversion_payload.boundary_evidence.predecessor_reference_price`, `.successor_reference_price`, `.mechanical_nav_tolerance_pct`, `.suspension_gap_annotation` — via `PositionConversionBoundaryEvidence`, produced solely by `transaction_canonicalizer.parse_position_conversion_payload()`.
- `conversion_payload.conversion_ratio` — via `PositionConversion.conversion_ratio`, same source.

No provider identity, predecessor/successor identity, conversion ratio, or reference-price field is re-derived from caller-controlled or display text; all four operands are read exclusively from the typed, already-validated `PositionConversion` value returned by the frozen WP1 parser — the same pattern `portfolio_rebuilder.py` already uses for its own (unrelated) purposes.

## 13. Authorized code/file surface

| File | Necessity | Capability | Already in §4.1? | Newly added by this amendment? |
|---|---|---|---|---|
| `backend/manage.py` | Sole hosting location for the classifier and its consumer (§6) | One new `AuditCheck` enum member (`MECHANICAL_CONTINUITY`); one new pure function (`_evaluate_mechanical_continuity`); one new check function (`_audit_mechanical_continuity`); one new call site inside `_audit_portfolio()` | **Yes** — §4.1 already authorizes `manage.py` "strictly bounded to conversion-boundary classification inside `verify_snapshots`" | **No new file authority created.** This amendment clarifies that the already-granted `manage.py` capability extends to the now-fixed §10.4 reconciliation classification, not only §10.3's tolerance-admissibility reporting the WPP had already scoped inside the same authorization |
| `backend/tests/test_verify_snapshots.py` | Required test coverage for the four outcomes and their severity/exit-code mapping | New test cases only; no existing case altered | **Yes** — already in §4.2 | **No** |

No other file is authorized by this act. In particular, `backend/services/market_data/position_conversion_quote_contract.py` (WP3, frozen), `backend/services/portfolio_rebuilder.py` beyond its already-authorized, unrelated §4.1 bound, and any new top-level module remain **unauthorized** for this capability.

## 14. Failure/result identity

A stable domain identity is required, consistent with the repository's existing `check`/`AuditCheck` convention:

- **New `AuditCheck` member:** `MECHANICAL_CONTINUITY = "mechanical_continuity"` — a distinct identity, not a reuse of `POSITION_CONVERSION_REBUILD_BOUNDARY` (which remains the identity for the unrelated rebuild-refusal predicate; §9) and not a reuse of any `AuditCheck` member above.
- **Two distinguishable description strings** under the same `AuditCheck` value, one for `MECHANICAL_CONTINUITY_FAILURE` and one for `NOT_EVALUABLE` (§8), so operators can tell the two apart in `verify_snapshots` output without needing a fifth `AuditCheck` member (the existing `AuditAnomaly.description`/`details` fields already carry this distinction for other checks, e.g. `HOLDINGS_INTEGRITY`'s several distinct description strings).
- This identity is reserved by this amendment, not implemented; no enum member is added to the live file by this act (§1).

## 15. Relationship to production execution — explicit exclusions

This amendment grants **implementation authority only, and only conditionally** (§16). It explicitly grants no authority for: historical snapshot correction; production rebuild execution; production-data mutation; release; deployment; operator execution against production; WP7 CLI execution; WP8 acceptance; or production deployment authorization. Because the sole authorized consumer (`verify_snapshots`) is already, and remains, read-only, even the strongest authorized outcome (`MECHANICAL_CONTINUITY_FAILURE` → exit code `2`) does not authorize reconstruction, repair, or any database write — it authorizes only a non-zero process exit code and printed diagnostic output.

## 16. Amendment binding status

Per the WP4 Retry-Order precedent (§3), an act at this position in the amendment chain is **not implementation-reliable** on its own. This amendment is:

- `PREPARED`, not `BOUND` or `FROZEN`;
- subject to the same two-step completion the Retry-Order chain required: an **Independent Reapproval** (a distinct reviewing authority reproducing this amendment's identity and reasoning from live repository bytes, not accepting this act's own report as proof) and, if reapproved, a **Binding Freeze Record**;
- **not** to be relied upon by any WP5 implementation task until both of those acts complete. Implementation must not consume `AuditCheck.MECHANICAL_CONTINUITY` under color of this amendment alone.

This act performs neither the independent reapproval nor the binding freeze.

## 17. Effect on existing WP5 authorization

This amendment adds exactly one clarified capability to the existing grant and widens nothing else:

```text
Original WP5 Implementation Authorization (§3–§4 of the Authorization Record)
  +
D7 mechanical-continuity classification/reporting capability, confined to
manage.py's already-authorized verify_snapshots surface (§6, §13 above)
```

Every other capability, boundary, gate, exclusion, and residual in the original Authorization Record (§§1–13) is inherited unchanged and is not restated with altered semantics here. In particular: `MINOR-2`'s WP5 half moves from `DESIGN SEMANTICS RESOLVED — IMPLEMENTATION OBLIGATION OPEN` (the design clarification's own framing) to `DESIGN SEMANTICS RESOLVED — ENFORCEMENT LOCUS DETERMINED (NOT YET BINDING) — IMPLEMENTATION OBLIGATION OPEN`; `POSITION_CONVERSION_REBUILD_BOUNDARY` is untouched (§9); no WP6+, release, deployment, or production-mutation authority is created or implied (§15).

## 18. Effect on WPP — required follow-up (not performed here)

The WPP is **not amended by this act**. A subsequent WPP amendment (structured, per §3's precedent, as its own additive `Work Package Plan Amendment` + `Independent Reapproval`) must incorporate, once this amendment itself is independently reapproved and bound:

- the fixed D2/D4/D5/D6 semantics (already recorded in the design clarification, §6 of that artifact);
- the D7 locus determined here (§6/§13): the `manage.py` classifier and check function, and the new `AuditCheck.MECHANICAL_CONTINUITY` identity (§14);
- the consumer policy (§7/§8/§10): sole consumer `verify_snapshots`, fail-closed for verification acceptance only, never for reconstruction;
- the code surface (§13), added to WPP §6's file table and §15's acceptance matrix as new rows (e.g. `WP5-A15`…`WP5-A18` covering `PASS`/`ANNOTATED_BOUNDARY_DISCONTINUITY`/`MECHANICAL_CONTINUITY_FAILURE`/`NOT_EVALUABLE`);
- acceptance tests for all four outcomes and their severity/exit-code mapping, added to `test_verify_snapshots.py`'s scope in WPP §6.1/§15; and
- the completion evidence required to move `MINOR-2`'s WP5 half from "reconciliation formula `BLOCKED`" (WPP §10.4) to fully planned and, eventually, implemented.

Until that WPP amendment (and this amendment's own reapproval/freeze) complete, WP5-C7 remains only partially decomposed exactly as WPP §10.4 already recorded.

## 19. Explicit exclusions

This act does not: implement D7; modify application code; modify test code; amend WP5's WPP; perform independent reapproval; perform binding freeze; perform Planning Confirmation; perform Planning Freeze; execute snapshot reconstruction; mutate production data; perform WP6/WP7/WP8 work; deploy; stage, commit, or push; reopen D2/D4/D5/D6; or alter the human-authorized design clarification.

## 20. Repository verification

| Verification | Result |
|---|---|
| Added/modified paths this act | `docs/implementation/BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md` only (additive) |
| Original WP5 Implementation Authorization Record modified | `NONE` — identity unchanged (§2 table) |
| Human-authorized design clarification modified | `NONE` — identity unchanged (§2 table) |
| WP5 WPP modified | `NONE` |
| Production/test code modified | `NONE` — all code inspection in §4 was read-only |
| `git diff --check` | see final report |
| `git diff --cached --check` | see final report |
| Trailing whitespace | see final report |
| Relative link / fragment anchor verification | see final report |
| `graphify update .` | see final report |
| Nothing staged or committed | see final report |
| Final `git status --short --untracked-files=all` | see final report |

## 21. Final disposition

`D7 IMPLEMENTATION AUTHORIZATION AMENDMENT PREPARED — NOT YET BINDING`

## 22. Exact next constitutional act

Following the WP4 Retry-Order chain's precedent shape (§3, §16): the exact next constitutional act is an **Independent Reapproval of this D7 Implementation Authorization Amendment**, performed by a reviewing authority distinct from this amending act, independently reproducing this amendment's cited identities and reasoning from live repository bytes. Only if reapproved does a subsequent **Binding Freeze Record** become available, after which (and only after which) the WPP follow-up in §18 may proceed and WP5 implementation may rely on this amendment.

This act performs neither the independent reapproval nor any act after it.
