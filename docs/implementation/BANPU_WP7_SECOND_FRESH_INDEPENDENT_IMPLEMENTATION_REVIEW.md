# BANPU-WP7 — Second Fresh Independent Implementation Re-Review After Exact Basis Integration

**Artifact class:** Additive fresh independent implementation re-review record  
**Review date:** 2026-08-19  
**Review boundary:** Read-only implementation re-review; no implementation/test correction, Confirmation, Freeze, closeout, rehearsal, LM13 synchronization, staging, commit, release, deployment, or production act  
**Frozen WPP:** `BANPU_WP7_WORK_PACKAGE_PLAN.md`, 53,998 bytes, SHA-256 `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897`  
**Historical failed review:** `BANPU_WP7_INDEPENDENT_IMPLEMENTATION_REVIEW.md`, 10,558 bytes, SHA-256 `59D39B92DDDB8BFAACE785C49D4453EC3F423C85C2D8FC15B8E025DF601DDF74`  
**First fresh failed re-review:** `BANPU_WP7_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW.md`, 18,810 bytes, SHA-256 `C79564232FE269488AB3D9EDB4AE38B3B265238F2447AB6C038BEDF28D2BA6BD`  
**Active WP5 canonical-LF overlay:** `89AA23712BE8177F8D363587343B520CB7DCC2C950BB6AE8B08E27A6D519C6F0`  
**Disposition:** `BANPU-WP7 IMPLEMENTATION RE-REVIEW FAILED — IMPLEMENTATION CORRECTION REQUIRED`

## 1. Re-review entry-state verification

HEAD is `ae223a42df688563748c0e6e6cb898e66bcb3da0`; cached name/status and cached diff were empty. Frozen WP7 identities reproduced exactly: Planning Confirmation `7A44203B6E39BF5100B133DA39B96BD5A5B1059634B279B8C4706F1742A0E82D`, Planning Freeze `E31AEC306C4CFDF0820A83BA1335DE22E0E9BE6A2ABC94AB153E85A6AB708B84`, historical failed review `59D39B92…DF74`, and first fresh failed re-review `C7956423…6BD`.

Current WP7 candidate identities at entry:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `backend/manage.py` | 262,427 | `D2F3DC9A5E0913A6E80888E30B09ABC136CEE49715CCE808325B3A9848EF32A6` |
| `backend/tests/test_apply_position_conversion_cli.py` | 51,964 | `8FD41A6C0EC977E549A7B6FB257A773AC53E74C3FFA8048FBB759E1B4CBDEE4E` |
| `backend/tests/fixtures/banpu_wp7_position_conversion_manifest.json` | 1,247 | `2B843A3ECFBB85AA9E1A6882CAD7DE6AA3690A94627BD7DBF4F317ED802A9E03` |

The newest WP5 Fresh Freeze exists at `33B7898DCACF71CDDEF352AD6D4898F69C500A01E42B20D0371B7A7C52360176` and binds production `64026DDA…7947` and test `ABC8C406…F1B5D0`. Independent canonical-LF aggregation reproduced `89AA2371…C6F0`. Both frozen predecessor fields exist. LM13 remains `FF7CE1F4…918D8`; Decision Log/INDEX remain `3BE8084D…EC50` / `5A1DB032…66FC`. No WP7 Implementation Confirmation, Implementation Freeze, closeout, or repository evidence of a production/release/deployment act exists. Nothing was staged.

## 2. Full lineage verification

The chain is continuous: frozen WP7 planning → initial three-member implementation → failed review → bounded replay/reporting correction → realized-P&L predecessor blocker → WP5 realized-P&L Authorization `DFFFF800…8336` → implementation → fresh Review `3B3E8363…5925` → Confirmation `92CB87DD…E7E4` → Freeze `D9757181…0ED8` → authorized WP7 resumption → first fresh WP7 re-review failure `C7956423…6BD` → ordinary-basis predecessor blocker → source determination `D32DEED1…0411` → WP5 basis Authorization `9A8107A5…BED2` → implementation → fresh Review `B3E1CB85…3F82` → Confirmation `C655877C…530D` → Freeze `33B7898D…0176` → explicitly authorized WP7 resumption → current candidate.

Each WP5 freeze expressly establishes the successor boundary before WP7 consumption. Mtime order and immutable records corroborate every pause/resumption. No WP7 implementation leap crossed an unfrozen predecessor boundary.

## 3. Historical-defect closure matrix

| Finding | Prior status | Current evidence | Fresh classification |
|---|---|---|---|
| Replay `success=False` ignored | blocking | both modes map it to `REPLAY_FAILED` | `CLOSED` |
| Replay canonical error ignored | blocking/insufficient | `success=True, error=TOKEN_SENTINEL` passes as parity | `STILL OPEN` |
| Replay exception ignored/leaked | blocking | maps to sanitized `REPLAY_EXCEPTION` | `CLOSED` |
| Holdings-count-only comparison | blocking | symbol/share/average-cost, exact ordinary basis, and conversion basis all compared | `CLOSED` |
| Ordinary basis omitted/locally synthesized | blocking | frozen WP5 exact map directly consumed; local formula removed | `SUPERSEDED BY FROZEN PREDECESSOR AUTHORITY` |
| Realized P&L omitted | blocking | frozen field consumed directly and exactly compared as predecessor floats | `CLOSED` |
| Cash `None` accepted as zero | blocking | either `None` fails; zero remains valid | `CLOSED` |
| Sub-cent P&L differences hidden | blocking | `1.001 != 1.002` and adjacent representable floats fail | `CLOSED` |
| Incomplete pre/post comparison | blocking | full evidence set is compared, but an error-bearing successful result is accepted in both locations | `PARTIALLY CLOSED` |
| Raw exception/result-error leakage | blocking | raw content is replaced by stable categories; outer exception is sanitized | `CLOSED` |
| Deterministic-reporting evidence | insufficient | full stdout/stderr equality now covered for all six representative outcomes | `CLOSED` |
| Mechanical-continuity test semantics | inaccurate | truthful `NOT_EVALUABLE` test and pure evaluator call remain | `CLOSED` |
| Missing post-commit mismatch evidence | insufficient | exact-basis, cash-incomplete, and P&L mismatches halt after truthful `applied` | `CLOSED` |

One WP7 defect remains `STILL OPEN`; technical PASS is unavailable.

## 4. Implementation diff review

The complete `backend/manage.py` delta, full focused test, and fixture were inspected. The WP7 candidate remains within its three authorized paths. No unrelated refactor, provider fetch, manifest schema, API/frontend, schema/persistence, accounting equation, replay overlay, WP5 mutation, PD-3, WP8, M46, release, deployment, or production execution path was added. The separate WP5 two-file diff exactly matches its fresh freeze.

## 5. Frozen predecessor-surface consumption

WP7 directly reads `RebuildResult.reconstructed_realized_pnl` and `RebuildResult.reconstructed_holding_basis`. The WP7 block contains no realized-P&L calculation, ordinary `shares * avg_cost`, reconciliation-float basis reconstruction, snapshot/provider derivation, `_PortfolioState` access, or fallback proxy. Unrelated pre-existing formulas elsewhere in `manage.py` are outside the WP7 delta.

## 6. Holdings/basis completeness verification

The semantic identity is the reconciliation report's stable `report_symbol`. The final holding symbol set is required to match the basis-map key set exactly. Missing, extra, non-dict, non-Decimal, non-finite, empty-key, and count/holding-shape defects fail. Empty holdings plus empty basis passes; non-empty holdings plus empty basis fails. Direct counterexamples reproduced those outcomes.

## 7. Exact Decimal basis verification

Exact equal `Decimal("100.00004040000016")` maps pass. `100.00004040000016` versus `100.00004040000017`, same projected shares/average cost with distinct maps, and one-sided symbols fail. The comparator applies no float conversion, rounding, quantization, tolerance, or projection. Diagnostics are sorted and preserve the exact Decimal text.

## 8. Conversion-specific basis preservation

Conversion reconciliation still evaluates the existing `B0`/`Bs`-derived successor basis independently with the frozen `0.01` tolerance. The exact ordinary map neither replaces nor changes that path; exact ordinary comparison and conversion-specific tolerant comparison remain distinct.

## 9. Cash completeness verification

Direct results: `None/0.0` FAIL; `None/None` FAIL; `0.0/0.0` PASS; equal non-zero PASS; unequal and sub-cent differences FAIL. No `value or 0` behavior remains.

## 10. Realized-P&L precision verification

`None` fails closed; zero/zero and equal non-zero pass; `1.001/1.002` fails; `1.0/1.0000000000000002` fails. No two-decimal normalization remains. WP7 consumes the frozen predecessor float surface directly.

## 11. Replay failure/error handling

Legacy and native `success=False` fail; raised exceptions fail; incomplete cash/holdings/basis/P&L fail. However `_run_one_replay_mode()` checks only `result.success`, not `result.error`. A controlled `RebuildResult(success=True, error="TOKEN_SENTINEL", complete-equal default evidence)` returned PASS. This is the blocking fail-closed defect.

## 12. Sanitized reporting verification

Controlled exception, result-error, and outer-command sentinels (`TOKEN_SENTINEL`, `RAW_PAYLOAD_SENTINEL`, `0xDEADBEEF`) do not appear in output. Stable mode and category remain visible (`legacy/native`, `REPLAY_FAILED`, `REPLAY_EXCEPTION`, `APPLY_POSITION_CONVERSION_UNEXPECTED_FAILURE`). The open defect is error presence being ignored, not leakage.

## 13. Deterministic reporting verification

The frozen criterion is exact output determinism for a given manifest/repository state, not merely selected-field equality. Current tests compare complete stdout/stderr for dry-run, failed preflight, successful commit, `already_applied`, conflict, and post-commit anomaly; all pass. Source ordering is fixed and raw replay output is contained.

## 14. Pre-commit replay verification

Both modes execute with `dry_run=True`, no candidate overlay, then restore the toggle and roll back. Holdings, exact basis, cash, realized P&L, and applicable conversion evidence gate commit. The error-bearing-success counterexample nevertheless returns a passing preflight and can permit commit, so A3/A9 fail.

## 15. Post-commit replay verification

After `applied`, the same full check runs. Basis-only high-precision mismatch, cash-only/incomplete mismatch, and P&L-only mismatch retain truthful `Status: applied`, emit sanitized `CRITICAL`, return non-zero, omit cache/rebuild instructions, and invent no rollback. But a real-path injected fourth replay with `success=True` and populated `error` exited `0` and emitted post-commit operator instructions. A17 fails.

## 16. Replay-toggle restoration

Independent probes covered full success, legacy failure, native failure, holdings mismatch, basis mismatch, cash mismatch, P&L mismatch, incomplete evidence, and raised exception. Every case restored the original value and called rollback exactly once.

## 17. Mechanical-continuity verification

Production calls only `_evaluate_mechanical_continuity()`. `PASS` and `ANNOTATED_BOUNDARY_DISCONTINUITY` proceed; `NOT_EVALUABLE` and failure states block. Test naming truthfully covers the schema-reachable fail-closed state and does not claim unreachable-branch coverage.

## 18. Registry/quote/broker/identity conformance

`--portfolio/-p` is explicit and required; `ws_id` derives from the persisted Portfolio. Read-only pre-preparation checks precede preparation, which precedes post-validation. Quote checks remain manifest/provider split with no new fetch. Broker facts remain manifest-carried trusted facts. No generic corporate-action expansion or public endpoint exists.

## 19. Focused WP7 test result

From the established `backend` working directory:

```text
65 passed, 516 warnings in 3.87s
```

An initial repository-root invocation produced fixture-relative `FileNotFoundError` setup failures; it was an invocation/cwd incident and was not counted as candidate evidence.

## 20. Governing regression result

Exact WPP §11 files: `test_asset_registry.py`, `test_position_conversion_live.py`, `test_transaction_canonicalizer.py`, `test_position_conversion_quote_contract.py`, `test_shadow_regeneration.py`, `test_horizon_grader.py`, `test_ideal_series.py`, `test_portfolio_metrics.py`, `test_portfolio_rebuilder.py`, and `test_verify_snapshots.py`.

```text
581 passed, 1 failed, 1935 warnings in 10.20s
```

Sole failure: `test_position_conversion_live.py::test_lm13_no_public_endpoint_or_cli_references_execute_position_conversion`. Combined current execution is `646 passed, 1 failed`; the repository is not fully green.

## 21. LM13 classification

`STALE PREDECESSOR TEST — WP7 AUTHORITY SUPERSEDES CLI PORTION`. WP4 LM-13's primary criterion is no public endpoint/frontend authoring path; WP4 Allocation and Authorization defer CLI wiring to WP7; Roadmap line 253 does the same; Sequence line 195 limits access pending WP7. The CLI assertion is stale, while the public/frontend invariant remains controlling. LM13 blocks a repository-green claim but is not current WP7 implementation nonconformance.

## 22. Public/API/frontend boundary

Searches found no conversion route, public endpoint, `backend/main.py` exposure, frontend action, or new public service surface. Current exposure remains the authorized CLI calling the pre-existing internal service.

## 23. Graph metadata classification

`graphify-out/graph.json`, report, labels, cache, and manifest were regenerated at the latest correction time. `.gitignore` line 67 ignores all `graphify-out/`; `git ls-files graphify-out` is empty and no tracked repository file changed. Classification: `TOOL/DERIVED METADATA — NON-REPOSITORY / NON-BLOCKING`.

## 24. Rehearsal-dependent acceptance

A11, A12, A14, and A15 remain `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED`. `MINOR-5` and `NEW-MINOR-A` WP7 portions remain pending. No rehearsal was performed; these are distinct from the implementation defect.

## 25. Fresh acceptance-matrix result

| ID | Evidence | Fresh finding | Status |
|---|---|---|---|
| A1 | default dry-run DB test | no lasting write | PASS |
| A2 | explicit dry-run DB test | no lasting write | PASS |
| A3 | preflight/commit path plus error-bearing result probe | canonical replay error can pass | FAIL |
| A4 | E8-R retry test | matching retry no-op | PASS |
| A5 | E8-R conflict test | conflict fails closed | PASS |
| A6 | complete diff | no generic framework | PASS |
| A7 | parser/lookup tests | explicit portfolio; derived workspace | PASS |
| A8 | dry-run DB assertions | no lasting write | PASS |
| A9 | independent preflight probes | canonical result error does not fail closed | FAIL |
| A10 | exact-output and sentinel tests | deterministic and sanitized | PASS |
| A11 | no real-PostgreSQL rehearsal | environment required | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A12 | no isolation proof | environment required | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A13 | route/API/frontend search | CLI-only | PASS |
| A14 | no rehearsal | environment required | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A15 | no rehearsal | environment required | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A16 | diff/source searches | no forbidden surface or WP7 equation | PASS |
| A17 | real post-commit error-bearing replay probe | exits 0 and emits instructions | FAIL |
| A18 | call-site inspection/tests | no mutation before preparation | PASS |
| A19 | call-site inspection/tests | pure evaluator only | PASS |

## 26. Counterexample-search findings

Cash `None`/zero, both-`None`, missing/extra/invalid basis, high-precision basis-only difference, sub-cent/adjacent-float P&L, one-sided holdings, replay failure, exception sentinel, all toggle exits, and post-commit basis/cash/P&L mismatches were rejected correctly. Empty holdings/empty map and exact equal values passed correctly. Public exposure and local ordinary-basis formula searches found none. One falsification succeeded: an error-bearing successful replay passed both preflight and post-commit; the post-commit probe emitted instructions.

## 27. Remaining defects/observations

| Category | Finding |
|---|---|
| WP7 implementation defect | `_run_one_replay_mode()` ignores non-`None` `RebuildResult.error` when `success=True`; affects pre- and post-commit |
| Predecessor-test debt | LM13's literal CLI prohibition remains red |
| Rehearsal evidence pending | A11/A12/A14/A15 plus WP7 portions of `MINOR-5` and `NEW-MINOR-A` |
| Environment/tooling observation | test file requires the established `backend` cwd; graph output is ignored derived metadata |
| Documentation-only observation | focused-test module header's acceptance list omits A10 although the file now contains A10 evidence |

## 28. Review artifact created

This second fresh re-review record is the sole repository artifact created by the review. Both prior failed-review precedents preserve each review result additively; neither prior record was modified.

## 29. Repository/diff verification

Post-artifact verification must re-hash all protected implementation/test/planning/review/predecessor/LM13/index files, confirm only this record is attributable to the review, run working and cached diff checks, confirm nothing staged, and create no commit. The accompanying final report records those results.

## 30. Resulting WP7 constitutional state

WP7 Planning remains `CONFIRMED / FROZEN`; both prior failed reviews remain immutable; both WP5 predecessor surfaces are freshly frozen and correctly consumed; the current WP7 implementation still has one fail-closed defect. Rehearsal rows and LM13 remain separate. Confirmation, Freeze, closeout, rehearsal, LM13 synchronization, staging, commit, release, deployment, and production acts remain unperformed.

## 31. Fresh independent re-review disposition

**`BANPU-WP7 IMPLEMENTATION RE-REVIEW FAILED — IMPLEMENTATION CORRECTION REQUIRED`**

## 32. Exact next constitutional act

A bounded **BANPU-WP7 Implementation Correction**: treat any populated `RebuildResult.error` as sanitized replay failure in both modes, add focused pre-commit and post-commit error-bearing-result evidence, then request another fresh independent implementation re-review. LM13 synchronization, Implementation Confirmation, and Implementation Freeze are not the immediate act while this implementation defect remains. This review performs no part of that correction.
