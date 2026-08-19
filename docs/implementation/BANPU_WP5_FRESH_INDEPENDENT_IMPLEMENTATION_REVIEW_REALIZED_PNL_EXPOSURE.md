# BANPU-WP5 — Fresh Independent Implementation Review: RebuildResult Realized P&L Exposure

**Artifact class:** Additive fresh independent implementation review record for a bounded amendment
**Review date:** 2026-08-19
**Instrument under review:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_REALIZED_PNL_EXPOSURE.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_REALIZED_PNL_EXPOSURE.md), 18,182 bytes, SHA-256 `DFFFF800D9636AB5266846FD750FCE3CD3DF6AFA40EAB3EB43219F280D7D8336`
**Reviewed implementation corpus:** `backend/services/portfolio_rebuilder.py` (129,464 B, SHA-256 `409FBC22313A98B24D9A23FFE3754CBA2584A702473C36CB2D51A36EDC19F429`), `backend/tests/test_portfolio_rebuilder.py` (108,142 B, SHA-256 `F42FFF2084A568CE165D0F58B0C3EA0109881E38736BB9CE299E330F49808B25`)
**Disposition:** `BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION REVIEW PASSED`
**Implementation Confirmation/Freeze performed by this act:** `NO`
**Production/release/deployment authority created:** `NONE`

---

## 1. Review entry-state verification

Independently established, not inherited from the implementation report:

| Premise | Live evidence | Result |
|---|---|---|
| HEAD | `ae223a42df688563748c0e6e6cb898e66bcb3da0` | confirmed |
| Working tree | `git status --porcelain=v2` shows exactly the same 3 modified tracked files (`backend/manage.py`, `backend/services/portfolio_rebuilder.py`, `backend/tests/test_portfolio_rebuilder.py`) and the same untracked WP7/governance artifacts as the Amendment Authorization's own entry-state table | matches |
| Staging area | `git diff --cached --stat` empty both before and after this review | confirmed empty |
| Amendment Authorization identity | 18,182 B, SHA-256 `DFFFF800D9636AB5266846FD750FCE3CD3DF6AFA40EAB3EB43219F280D7D8336` | read in full |
| Pre-amendment frozen `portfolio_rebuilder.py` identity | HEAD blob, CRLF-normalized: 129,334 B, SHA-256 `D94E686DB2EFF8F95B1047FA470A2DD94B663F0847233260FDEC9B4626422765` — exact match to WP5 Freeze §E/§H and to the Amendment Authorization's own citation | independently reproduced, not assumed |
| Amended `portfolio_rebuilder.py` identity | 129,464 B, SHA-256 `409FBC22313A98B24D9A23FFE3754CBA2584A702473C36CB2D51A36EDC19F429` | recorded |
| Amended `test_portfolio_rebuilder.py` identity | 108,142 B, SHA-256 `F42FFF2084A568CE165D0F58B0C3EA0109881E38736BB9CE299E330F49808B25` | recorded |
| WP7 frozen WPP/Confirmation/Freeze/Review identity | Recomputed raw SHA-256 of `BANPU_WP7_WORK_PACKAGE_PLAN.md`, `BANPU_WP7_PLANNING_CONFIRMATION.md`, `BANPU_WP7_PLANNING_FREEZE_RECORD.md`, `BANPU_WP7_INDEPENDENT_IMPLEMENTATION_REVIEW.md` exactly match `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897`, `7A44203B6E39BF5100B133DA39B96BD5A5B1059634B279B8C4706F1742A0E82D`, `E31AEC306C4CFDF0820A83BA1335DE22E0E9BE6A2ABC94AB153E85A6AB708B84`, `59D39B92DDDB8BFAACE785C49D4453EC3F423C85C2D8FC15B8E025DF601DDF74` respectively | byte-identical, unchanged |
| `backend/manage.py` WP7-candidate diff predates this amendment | File mtime `2026-08-19 11:26:25` precedes both the Amendment Authorization's own write time (`11:50:45`) and the amended `portfolio_rebuilder.py`/`test_portfolio_rebuilder.py` mtimes (`11:56:01`–`11:56:02`); the `manage.py` diff contains zero references to `reconstructed_realized_pnl` or `RebuildResult` field additions | pre-existing, not attributable to this act |
| WP5 Confirmation/Freeze lineage over `portfolio_rebuilder.py` | `BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md` §E/§O lists it as frozen corpus member 3/9; no WP5 amendment Confirmation or Freeze exists yet for this amendment | consistent with a still-open review step |
| No amendment Confirmation/Freeze exists | `Glob` for `BANPU_WP5*REALIZED_PNL*CONFIRMATION*` / `*FREEZE*` returns nothing beyond the Authorization itself and this review | confirmed absent |
| No production/release/deployment act | No staged change; no migration, route, or deployment artifact touched | confirmed |

Amendment provenance was separated cleanly: the two-file WP5 diff (`portfolio_rebuilder.py`, `test_portfolio_rebuilder.py`) is distinguishable from the pre-existing, pre-dated WP7 `manage.py`/fixture/test diff by both content (no cross-reference) and timestamp ordering. Graph metadata is addressed separately in §17.

## 2. Amendment authority verification

The Authorization (§8) authorizes exactly:

1. one additive, trailing, defaulted `RebuildResult` field, `reconstructed_realized_pnl: float | None = None`;
2. population at the existing Stage-1 result-construction point via `_f(final_state.cumulative_realized_pnl)`;
3. focused test additions confined to `backend/tests/test_portfolio_rebuilder.py`.

It explicitly excludes (§10) accounting changes, replay changes, provider/snapshot changes, refactoring, debug-print cleanup, API/frontend changes, WP7 changes, and LM13 changes.

The reviewed diff matches this authorized surface exactly — see §3.

## 3. Actual diff review

`git diff -- backend/services/portfolio_rebuilder.py` shows exactly two hunks:

- one added dataclass line: `reconstructed_realized_pnl: float | None = None`, trailing all other `RebuildResult` fields;
- one added assignment line: `result.reconstructed_realized_pnl = _f(final_state.cumulative_realized_pnl)`, immediately following the existing `result.reconstructed_cash = _f(final_state.cash_balance)` assignment.

No other line in the file changed. No refactor, no reordering, no formatting change, no touched debug `print()` statement, no changed default, no changed control flow, no provider/replay/snapshot code touched.

`git diff -- backend/tests/test_portfolio_rebuilder.py` shows exactly four additions: one assertion appended to the existing `test_rebuild_result_new_fields_default_to_zero`, and three new focused test functions (zero/fetch-free, ordinary SELL, conversion cash-in-lieu). No existing test body was altered.

No unauthorized material change was found in either file.

## 4. Canonical realized-P&L provenance

Independently inspected live source, not test output:

- `_PortfolioState(Decimal("0"), {}, Decimal("0"))` at line 2257 initializes `cumulative_realized_pnl` — pre-existing.
- `_apply_transaction()` line 797: `state.cumulative_realized_pnl += _d(pnl)` on `SELL`, where `pnl = ctx.realized_pnl if ctx.realized_pnl is not None else 0.0` — pre-existing, unchanged by the diff.
- `_apply_transaction()` line 944: `state.cumulative_realized_pnl += realized_pnl` in the `POSITION_CONVERSION` branch, where `realized_pnl = payload.cash_in_lieu.realized_pnl if payload.cash_in_lieu else Decimal("0")` — pre-existing, unchanged by the diff.
- Lines 2271–2273 populate `result.reconstructed_holdings_count`, `result.reconstructed_cash`, and (new) `result.reconstructed_realized_pnl` from the same `final_state` immediately after the Stage-1 replay loop, before `_resolve_conversion_successors` (line 2286) and before any Stage 2/3 snapshot or provider work.

No new accumulation path, no changed formula, no changed transaction semantics. The new field is a pure read of pre-existing final state.

## 5. Stage-boundary finding

`reconstructed_realized_pnl` is set at line 2273, inside the same statement block as `reconstructed_cash`/`reconstructed_holdings_count`, unconditionally after a successful Stage-1 replay loop and before any `skip_snapshots`-gated code. `_build_price_matrix` (the sole provider-dependent call in this function) occurs at line 2359, nested under `if not skip_snapshots:` → `else` of `if not rebuild_dates:` — structurally unreachable before line 2273 and entirely skipped when `skip_snapshots=True`. Failed/pre-Stage-1 paths (e.g., the "portfolio not found" early return at line 2159, and the pre-Stage-1 default-constructed `result` at line 2166) never reach line 2273, so `reconstructed_realized_pnl` retains its dataclass default of `None` on those paths. A successful Stage 1 with no realized event yields `Decimal("0")` → `_f(Decimal("0"))` = `0.0`, not `None`.

## 6. Numeric-semantics finding

`_f(v) = float(v.quantize(_QUANT, rounding=ROUND_HALF_UP))` (line 125–126) is the same conversion already applied to `reconstructed_cash` on the immediately preceding line. No new rounding rule, no new quantization constant, no WP7-specific conversion was introduced. `None` is preserved as the pre-Stage-1 default; `0.0` is the exact, intentional successful-zero value — the two are structurally distinguishable (default value vs. assigned value) and both are exercised by tests (§9).

## 7. Ordinary SELL evidence

`test_rebuild_exposes_canonical_sell_realized_pnl` supplies canonicalized `INITIAL_POSITION` (100 sh @ 75.0) then `SELL` (100 sh, total_amount 8,000.0, `realized_pnl=500.0`) contexts, patches only `canonicalize_transactions` and `validate_portfolio_ledger`, and asserts `r.reconstructed_realized_pnl == pytest.approx(500.0)`. The `500.0` value is supplied on the `SELL` context's `realized_pnl` field and consumed exactly by the pre-existing line-797 accumulation (`ctx.realized_pnl` is not `None`, so `pnl = 500.0`) — the test exercises the real accumulation path, not a mocked or directly assigned `cumulative_realized_pnl`. Independently reproduced: **PASS**.

## 8. Cash-in-lieu evidence

`test_rebuild_exposes_conversion_cash_in_lieu_realized_pnl` builds a `_conversion_payload` with `cash_in_lieu=_cil(..., pnl="1.5")` and a matching `INITIAL_POSITION` predecessor holding, patches only `canonicalize_transactions` and `validate_portfolio_ledger`, and asserts `r.reconstructed_realized_pnl == pytest.approx(1.5)`. The `1.5` flows through the pre-existing line-944 accumulation (`payload.cash_in_lieu.realized_pnl`) inside the unmodified `POSITION_CONVERSION` branch. No WP7 conversion behavior was imported; no accounting path was touched to make this pass. Independently reproduced: **PASS**.

## 9. Default/zero evidence

- **Default:** `test_rebuild_result_new_fields_default_to_zero` gained one appended assertion, `assert r.reconstructed_realized_pnl is None`, on a `RebuildResult(...)` constructed without the new keyword — reproduced: **PASS**.
- **Successful zero:** `test_rebuild_exposes_zero_realized_pnl_without_snapshot_provider_fetch` runs a `DEPOSIT`-only replay (`skip_snapshots=True`) and asserts `r.reconstructed_realized_pnl == 0.0` — reproduced: **PASS**.

The `None`-vs-`0.0` distinction is intentional and compatible with §5's finding (unset dataclass default vs. an assigned Stage-1 output).

## 10. Fetch-free evidence

`test_rebuild_exposes_zero_realized_pnl_without_snapshot_provider_fetch` patches `_build_price_matrix` with an `AsyncMock` and asserts `mock_fetch.assert_not_called()` after `skip_snapshots=True`. Independent trace of the call path (§5) confirms `_build_price_matrix` is structurally unreachable under `skip_snapshots=True` — the mock assertion is not over-credited; the tested code path genuinely bypasses all provider-dependent stages. Reproduced: **PASS**.

## 11. Compatibility finding

All in-repository `RebuildResult(` construction sites were independently located and inspected: `services/portfolio_rebuilder.py` (2 sites, both keyword-only, both predate the new field and correctly receive its default), `tests/test_apply_position_conversion_cli.py` (3 sites, keyword-only), `tests/test_registry_replay_parity.py` (1 site, keyword-only). No positional construction, no `RebuildResult ==` equality comparison, no `asdict()`/`__dict__` use, and no JSON/API serialization of `RebuildResult` exist anywhere in the repository (site-packages noise excluded). `manage.py` prints/consumes only named existing fields; its live diff contains no reference to `reconstructed_realized_pnl`. The trailing, defaulted field is genuinely backward-compatible; no consumer receives it unexpectedly through any generic serialization path because none exists.

## 12. Accounting non-interference

Line-by-line comparison of the frozen HEAD blob against the amended file confirms the only two changes are the field declaration and its Stage-1 assignment (§3). The realized-P&L formula (lines 797, 944), basis allocation, transaction canonicalization, BUY/SELL/conversion processing, cash-in-lieu calculation, portfolio-state transitions, replay ordering, and reconciliation equations are byte-identical to the frozen corpus outside the two authorized lines.

## 13. Provider/snapshot non-interference

No line touching `_build_price_matrix`, snapshot generation, quote handling, or cache behavior appears in the diff. Confirmed by direct diff inspection (§3) and by the stage-boundary trace (§5).

## 14. Focused-test result (independently reproduced)

```
pytest tests/test_portfolio_rebuilder.py -k "reconstructed_realized_pnl or rebuild_exposes_zero_realized_pnl or rebuild_exposes_canonical_sell_realized_pnl or rebuild_exposes_conversion_cash_in_lieu_realized_pnl or test_rebuild_result_new_fields_default_to_zero"
→ 4 passed, 94 deselected
```

## 15. WP5 governing regression result (independently reproduced)

```
pytest tests/test_portfolio_rebuilder.py
→ 98 passed
```

The WP5 Freeze Record §O defines the frozen implementation corpus's test membership as four files: `test_portfolio_rebuilder.py`, `test_portfolio_metrics.py`, `test_snapshot_return_recovery.py`, `test_verify_snapshots.py`. Run together:

```
pytest tests/test_portfolio_rebuilder.py tests/test_portfolio_metrics.py tests/test_snapshot_return_recovery.py tests/test_verify_snapshots.py
→ 207 passed, 0 failed
```

This is a strict superset of, and fully consistent with, the reported "188 passed" — but the exact count of 188 could not be independently reproduced under the corpus definition recorded in WP5 Freeze §O (98+21+25+63 = 207, not 188; no subset or superset combination of these four files' individual counts — 98, 21, 25, 63 — sums to 188). This is recorded as a non-blocking reporting discrepancy in §22: the reproduced regression evidence is unambiguously green and at least as broad as what was reported, so it does not undermine the disposition, but the "188" figure itself should not be treated as a verified count.

## 16. Temporary-directory incident classification

`%TEMP%\pytest-of-patip\` contains numbered run directories (`pytest-33` through `pytest-58`) consistent with pytest's default rolling retention/garbage-collection of prior `basetemp` runs. This collection is pytest's own session-setup housekeeping (pruning older numbered dirs), which executes before test bodies run — a `PermissionError` there (e.g., from a lingering Windows file handle or AV scan on an old run directory) occurs in test infrastructure, not application code, and necessarily precedes any test body executing. No code or test modification occurred between the reported failed attempt and the reported successful rerun (confirmed: the working tree's only diff is the two-file amendment already reviewed in §3, and it existed before either run). Using a workspace-local `--basetemp` is semantically neutral — it only changes where pytest's `tmp_path` fixtures write ephemeral files, not test logic or application behavior; this review independently ran the full corpus both against the OS default temp directory and against a workspace-local `--basetemp`, obtaining identical, fully green results (98/98, and 207/207 for the four-file corpus) in both configurations.

**Classification: `ENVIRONMENTAL / NON-BLOCKING`.**

## 17. Graph metadata classification

`graphify-out/` (including `graph.json`, modified 2026-08-19 11:58:31, two minutes after the amended `portfolio_rebuilder.py`/`test_portfolio_rebuilder.py` mtimes) is excluded from Git entirely — `.gitignore:67` lists `graphify-out/`, and `git status`/`git diff` show no trace of it under any path. It is local, tool-generated derivative metadata (the project's `graphify` knowledge-graph cache), produced by a `graphify update .`-style command referenced in project tooling conventions, not a repository-governed source, test, or governance artifact. It creates no third-file mutation of anything Git tracks or that WP5/WP7 governance defines as corpus membership.

**Classification: `TOOL/DERIVED METADATA — NON-REPOSITORY / NON-BLOCKING`.**

## 18. WP7 non-interference

`backend/manage.py`, the WP7 CLI test, the WP7 fixture, and all WP7 governance records (WPP, Planning Confirmation, Planning Freeze, Independent Implementation Review) are unchanged by this amendment: the `manage.py` diff pre-dates the amendment (§1), and independently recomputed SHA-256 values for the four WP7 governance documents exactly match the citations already recorded in the Amendment Authorization (§1). `grep` for `reconstructed_realized_pnl` across `backend/manage.py` returns zero matches — WP7 does not yet consume the new field; its diff's own docstring (lines 367–371) explicitly documents realized P&L as still uncompared, consistent with the frozen WP7 review's open finding.

## 19. LM13 non-interference

LM13 is not present in either file touched by this amendment (`portfolio_rebuilder.py`, `test_portfolio_rebuilder.py`); the complete diff of both files was reviewed line-by-line in §3 and contains no reference to LM13 or its governing test file. LM13's known WP7-era failure is therefore structurally unaffected by this act and is not attributable to it.

## 20. Test-adequacy determination

| Evidence area | Status |
|---|---|
| Default compatibility | present, reproduced PASS (§9) |
| Zero P&L | present, reproduced PASS (§9) |
| Ordinary SELL P&L | present, reproduced PASS (§7) |
| Cash-in-lieu P&L | present, reproduced PASS (§8) |
| `skip_snapshots=True` | present, reproduced PASS (§9–10) |
| No provider fetch | present, reproduced PASS (§10) |
| Existing consumer compatibility | established by inspection, no test required — no consumer exists that could be broken (§11) |
| Existing WP5 regressions | present, reproduced green, superset of frozen corpus (§15) |

No missing evidence is blocking. No coverage beyond the exact Amendment Authorization was demanded or found lacking.

## 21. Counterexample-search result

Attempted against: a successful zero-P&L Stage 1, ordinary SELL, conversion cash-in-lieu, a failed/pre-Stage-1 result path, `skip_snapshots=True`, an existing caller omitting the new field, every positional/keyword constructor found in the repository, and generic result serialization (none exists). No counterexample falsifying the amendment was found.

## 22. Additional defects/observations (non-blocking)

- The implementation report's reproduced regression count ("188 passed") does not match the actual size of the WP5 Freeze §O-defined governing corpus (207 passed) under any subset/superset combination checked. The independently reproduced evidence is fully green and broader in scope, so this is a reporting-accuracy note, not a blocking defect.
- Pre-existing debug `print()` statements at and around the Stage-1 replay loop (lines 2258–2270) remain untouched, as authorized (§9 of the Amendment Authorization); their cleanup remains explicitly out of scope for this act.
- Stale, permission-denied `.pytest-m32-*` directories exist at `backend/.pytest-m32-3e3r2*` (dated 2026-07-15, over a month before this amendment). These are unrelated leftover artifacts from an unrelated prior phase (M32), not connected to this review's temporary-directory incident (§16), and are noted only for completeness — no action taken.

## 23. Review artifact created

This record — `docs/implementation/BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_REALIZED_PNL_EXPOSURE.md` — is the sole additive artifact created by this act, per the precedent established by [`BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW.md`](BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW.md) and [`BANPU_WP5_SECOND_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW.md`](BANPU_WP5_SECOND_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW.md), both of which record a fresh independent implementation review as its own standalone artifact distinct from any later Confirmation record.

## 24. Repository/diff verification

- No code or test file was modified by this review; the only file this act created is this record.
- `backend/services/portfolio_rebuilder.py` and `backend/tests/test_portfolio_rebuilder.py` remain exactly as reviewed (409FBC22…, F42FFF20… respectively).
- The Amendment Authorization is unchanged (DFFFF800…).
- Prior WP5 frozen artifacts, WP7 state, and LM13 are unchanged (§1, §18, §19).
- Decision Log and Implementation INDEX untouched by this act.
- `git diff --check` and `git diff --cached --check`: clean (exit 0, no whitespace errors).
- `git diff --cached --stat`: empty — nothing staged.
- No commit was made.

## 25. Fresh independent-review disposition

**`BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION REVIEW PASSED`**

## 26. Exact next constitutional act

**BANPU-WP5 Fresh Implementation Confirmation — RebuildResult Realized P&L Exposure**, against the authorized amendment, the reviewed two-file implementation diff, and this fresh independent-review evidence. Not performed in this session.
