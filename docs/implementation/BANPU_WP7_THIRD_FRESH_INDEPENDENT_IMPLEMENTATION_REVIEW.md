# BANPU-WP7 — Third Fresh Independent Implementation Re-Review After Error-Bearing Result Correction

**Artifact class:** Additive fresh independent implementation re-review record  
**Review date:** 2026-08-19  
**Review boundary:** Read-only implementation re-review; no code/test correction, Implementation Confirmation, Implementation Freeze, closeout, rehearsal, LM13 synchronization, staging, commit, release, deployment, or production act  
**Disposition:** `BANPU-WP7 IMPLEMENTATION RE-REVIEW PASSED`

## 1. Re-review entry-state verification

HEAD is `ae223a42df688563748c0e6e6cb898e66bcb3da0`; cached name/status and cached diff were empty. The frozen WP7 WPP is unchanged at 53,998 bytes / SHA-256 `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897`; Planning Confirmation is unchanged at 39,845 bytes / `7A44203B6E39BF5100B133DA39B96BD5A5B1059634B279B8C4706F1742A0E82D`; Planning Freeze is unchanged at 31,901 bytes / `E31AEC306C4CFDF0820A83BA1335DE22E0E9BE6A2ABC94AB153E85A6AB708B84`.

All three failed reviews are unchanged: initial review 10,558 bytes / `59D39B92DDDB8BFAACE785C49D4453EC3F423C85C2D8FC15B8E025DF601DDF74`; first fresh re-review 18,810 bytes / `C79564232FE269488AB3D9EDB4AE38B3B265238F2447AB6C038BEDF28D2BA6BD`; second fresh re-review 17,793 bytes / `F631DE4459BDC0B02392629C955881741A25388726FACC4BD30C3CB3E898878D`.

Current WP7 candidate identities at entry:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `backend/manage.py` | 262,795 | `710B5E2CBF22FD6D774554C601201CD848BF663F89492F025C10CBD1E5E412F7` |
| `backend/tests/test_apply_position_conversion_cli.py` | 55,466 | `CEE866EABAAA24C5B2268B5CDDEE77710BA6FB591CB74080A80D2422A976B60A` |
| `backend/tests/fixtures/banpu_wp7_position_conversion_manifest.json` | 1,247 | `2B843A3ECFBB85AA9E1A6882CAD7DE6AA3690A94627BD7DBF4F317ED802A9E03` |

The active WP5 Freeze record is unchanged at `33B7898DCACF71CDDEF352AD6D4898F69C500A01E42B20D0371B7A7C52360176`; it still binds `portfolio_rebuilder.py` `64026DDA722B949205F4FB3E875396BBBCC11C7EA6B4E10CC6AF87BB5AFF7947` and its test `ABC8C406AA91DE405E4C1B1A9253E3BB99134EB5B072DAC41ACD136927F1B5D0`. Raw aggregate `E1F8B3E559AC9BD6683F9C1B69FD685C6B9A39934703B6E76AD3FE4720DEDC08` and canonical-LF aggregate `89AA23712BE8177F8D363587343B520CB7DCC2C950BB6AE8B08E27A6D519C6F0` were independently recomputed. Both `reconstructed_realized_pnl` and `reconstructed_holding_basis` remain present.

LM13 is unchanged at `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8`; Decision Log and INDEX are unchanged at `3BE8084DDE1813BF3B4ED7FF0C655C553EC3022B8554162E5585A44B8282EC50` and `5A1DB032AB4D35B0216A3346E7C07CE120E2067783461182872A75F1F1C466FC`. No WP7 Implementation Confirmation, Implementation Freeze, closeout, production, release, or deployment act exists.

## 2. Full lineage verification

The complete chain is continuous: frozen planning → initial implementation → failed review → bounded replay/reporting correction → realized-P&L predecessor blocker → WP5 realized-P&L Authorization `DFFFF800…8336` → implementation → Review `3B3E8363…5925` → Confirmation `92CB87DD…E7E4` → Freeze `D9757181…0ED8` → resumed WP7 correction → first fresh failure `C7956423…6BD` → ordinary-basis predecessor blocker → source determination `D32DEED1…0411` → WP5 basis Authorization `9A8107A5…BED2` → implementation → Review `B3E1CB85…3F82` → Confirmation `C655877C…530D` → Freeze `33B7898D…0176` → resumed WP7 correction → second fresh failure `F631DE44…878D` → bounded error-bearing-result correction → current candidate.

The current size/hash delta from the second review is explained exactly by the reported bounded correction: the canonical error gate in `manage.py` and six focused cases (legacy, native, `None`/empty, whitespace, and real post-commit behavior). Every predecessor surface was frozen before WP7 consumed it. No pause, independent review, Confirmation, Freeze, or authorized resumption boundary was skipped.

## 3. Historical-defect closure matrix

| Finding | Source review | Current evidence | Fresh status |
|---|---|---|---|
| replay `success=False` ignored | initial review | both modes return sanitized `REPLAY_FAILED` | `CLOSED` |
| canonical replay error ignored | second fresh review | truthy `result.error` rejected before parity; legacy/native/post-commit probes pass | `CLOSED` |
| replay exception ignored/leaked | initial/first fresh reviews | sanitized `REPLAY_EXCEPTION`; sentinel absent | `CLOSED` |
| holdings-count-only comparison | initial review | stable-symbol fields plus exact basis maps compared | `CLOSED` |
| ordinary basis omitted/locally synthesized | first fresh review | direct frozen exact-Decimal predecessor map; local formula absent | `SUPERSEDED BY FROZEN PREDECESSOR AUTHORITY` |
| realized P&L omitted | initial review | direct frozen result field compared exactly | `CLOSED` |
| cash completeness | first fresh review | either `None` fails; zero remains valid | `CLOSED` |
| P&L precision | first fresh review | sub-cent and adjacent float differences fail | `CLOSED` |
| incomplete pre/post comparison | prior reviews | success, error, completeness, and full parity gate both locations | `CLOSED` |
| raw error leakage | first fresh review | exception/result/outer sentinels suppressed; stable categories remain | `CLOSED` |
| deterministic reporting | initial/first fresh reviews | exact complete output equality for six representative states | `CLOSED` |
| mechanical-continuity evidence | initial review | pure helper and truthful `NOT_EVALUABLE` evidence | `CLOSED` |
| post-commit mismatch coverage | initial/first fresh reviews | basis, cash, P&L, and error-bearing anomalies halt instructions | `CLOSED` |

No WP7 implementation finding remains `PARTIALLY CLOSED` or `STILL OPEN`.

## 4. Implementation diff review

The complete candidate remains limited to `backend/manage.py`, the focused WP7 CLI test, and the sanitized fixture. The separate two-file WP5 delta matches the active frozen overlay and is not a WP7 mutation. No unrelated refactor, new accounting logic, provider fetch, manifest change, API/frontend exposure, schema/persistence change, replay overlay, WP5 mutation, PD-3 absorption, WP8/M46 expansion, production execution behavior, release, or deployment act was found.

## 5. Canonical result validation ordering

`_run_one_replay_mode()` executes the replay under contained stdout, catches raised exceptions as `REPLAY_EXCEPTION`, rejects `success=False` as `REPLAY_FAILED`, then rejects populated `result.error` as `REPLAY_FAILED`. Only the resulting error-free object reaches `_preflight_replay_mode_sanity()` evidence-completeness and parity checks. An error-bearing result cannot reach semantic comparison.

## 6. Canonical error semantics

`RebuildResult.error` is `str | None` with default `None`. The predecessor writes non-empty diagnostic strings on failure and existing consumers use truthiness. Fresh probes establish: `None` and `""` are unpopulated/no-error values; a non-empty string is canonical failure evidence; whitespace-only text is populated and fails. This matches the predecessor convention rather than importing the correction report.

## 7. Legacy error-bearing counterexample

Injected `success=True`, `error="TOKEN_SENTINEL"`, otherwise complete/equal legacy evidence. Result: preflight FAIL; commit path not reached; detail contains `legacy-mode replay REPLAY_FAILED`; sentinel absent; original replay toggle restored; rollback called exactly once.

## 8. Native error-bearing counterexample

The equivalent native injection produced preflight FAIL with `native-mode replay REPLAY_FAILED`; commit was not reached; sentinel was absent; toggle restored; rollback called exactly once.

## 9. Post-commit error-bearing counterexample

The exact prior real command-path falsification was rerun: conversion applied, fourth replay returned `success=True` with a populated canonical error, and all other evidence remained genuine and complete. Result: four replay calls; exit 1; persisted conversion present; truthful `Status: applied`; sanitized `REPLAY_FAILED` and `CRITICAL`; sentinel absent; no cache/rebuild instructions; no rollback claim. The prior blocker is closed.

## 10. Exception/success=False preservation

Raised replay exceptions remain `REPLAY_EXCEPTION`; `success=False` remains `REPLAY_FAILED` in either mode. Both are sanitized, block commit/parity, restore the toggle, and roll back replay-session mutation. The new canonical-error gate does not regress either branch.

## 11. Replay evidence completeness

An error-free successful result must still supply reconstructed holdings, exact ordinary basis, cash, realized P&L, and applicable conversion-basis evidence. Missing count/fields, basis, cash, or P&L fails closed. Empty holdings with an empty exact basis map remains the valid empty-portfolio case.

## 12. Holdings/basis verification

Stable `report_symbol` is the holding identity. Basis-map keys must equal the reconstructed holding-symbol set exactly. Missing, extra, non-dict, non-Decimal, non-finite, or invalid-key evidence fails. Equal high-precision Decimals pass; a one-unit final-digit difference fails. No WP7-local ordinary `shares * avg_cost` reconstruction exists. Conversion-specific `basis` remains a distinct reconciliation field with its established `0.01` tolerance.

## 13. Cash verification

`None/0`, `None/None`, unequal, and sub-cent-different cash values fail; `0/0` and exactly equal non-zero values pass. There is no fallback-to-zero behavior.

## 14. Realized-P&L verification

WP7 reads the frozen `reconstructed_realized_pnl` field directly. Either `None` fails; equal values pass; `1.001/1.002` and adjacent representable float differences fail. No two-decimal normalization or WP7-local P&L derivation exists.

## 15. Sanitization verification

Sentinels injected through a raised replay exception, populated `result.error`, and an outer unexpected exception do not appear in stdout/stderr; neither raw payload nor object-address text escapes. Stable `REPLAY_EXCEPTION`, `REPLAY_FAILED`, and `APPLY_POSITION_CONVERSION_UNEXPECTED_FAILURE` categories remain visible.

## 16. Deterministic-reporting verification

Full stdout/stderr equality is covered and reproduced for dry-run, failed preflight, successful commit, `already_applied`, conflict, and post-commit anomaly. Fixed ordering and contained rebuilder stdout prevent wall-clock, raw payload, and object-identity variation. The result-error correction adds only a stable category.

## 17. Pre-commit verification

Both replay modes execute against the persisted ledger with `dry_run=True`. Success, unpopulated error, complete evidence, and full parity gate commit. `success=False`, populated error, exception, incomplete evidence, or any mismatch blocks. Toggle restoration and rollback occur in `finally`; no lasting mutation remains.

## 18. Post-commit verification

After `applied`, the same complete gate runs. Failure, canonical error, exception, incomplete evidence, or mismatch yields a non-zero critical outcome while `Status: applied` remains truthful. Cache/rebuild instructions are withheld and no automated rollback is claimed.

## 19. Replay-toggle restoration

The focused suite and direct probes cover success; legacy/native reported failure; legacy/native error-bearing success; raised exception; holdings, basis, cash, and P&L mismatch; and incomplete evidence. All paths restore the original toggle and roll back replay-session state.

## 20. Registry/quote/broker/mechanical-continuity

Registry preconditions remain read-only before the separately committed preparation boundary. Quote checks remain the manifest-only/provider-independent split; no provider fetch exists. Broker facts remain schema/reference-price evidence. Mechanical continuity calls only the pure `_evaluate_mechanical_continuity()` helper; `NOT_EVALUABLE` coverage is truthful. No generic corporate-action expansion exists.

## 21. CLI/public boundary

`--portfolio/-p` is required and workspace identity derives from persisted `Portfolio.workspace_id`. Exposure is CLI-only. Searches found no route, `backend/main.py` public endpoint, router action, or frontend conversion action.

## 22. Focused WP7 test result

From the established `backend` working directory, with a verified writable external pytest base:

```text
71 passed, 0 failed, 536 warnings in 4.65s
```

The targeted error-contract set separately returned `6 passed, 22 warnings in 1.82s`. An earlier targeted attempt used the inaccessible default Windows pytest temp root: five non-temp cases passed and the real-path case failed in setup with `PermissionError`; it is an environment/invocation observation and is not counted as candidate evidence.

## 23. Governing regression result

Exact WPP corpus: `test_asset_registry.py`, `test_position_conversion_live.py`, `test_transaction_canonicalizer.py`, `test_position_conversion_quote_contract.py`, `test_shadow_regeneration.py`, `test_horizon_grader.py`, `test_ideal_series.py`, `test_portfolio_metrics.py`, `test_portfolio_rebuilder.py`, and `test_verify_snapshots.py`.

```text
581 passed, 1 failed, 1935 warnings in 10.76s
```

Sole failure: `test_position_conversion_live.py::test_lm13_no_public_endpoint_or_cli_references_execute_position_conversion`. Focused plus governing execution is `652 passed, 1 failed`. The repository is not fully green.

## 24. LM13 classification

`STALE PREDECESSOR TEST — WP7 AUTHORITY SUPERSEDES CLI PORTION`. WP4's controlling protection is no public endpoint/frontend authoring path, while its Roadmap/Sequence authority expressly deferred CLI wiring to WP7. That protection remains intact. LM13 is separate repository synchronization debt, blocks a repository-green claim, and is not current WP7 implementation nonconformance.

## 25. Graph metadata classification

Graph metadata was refreshed at the latest correction time. `.gitignore` line 67 ignores `graphify-out/`; `git ls-files graphify-out` is empty. Classification: `TOOL/DERIVED METADATA — NON-REPOSITORY / NON-BLOCKING`.

## 26. Rehearsal-dependent acceptance

WP7-A11, A12, A14, and A15 remain `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED`. The WP7 portions of `MINOR-5` and `NEW-MINOR-A` remain pending. No isolated real-PostgreSQL rehearsal exists or was performed.

## 27. Fresh acceptance matrix

| ID | Evidence | Fresh finding | Status |
|---|---|---|---|
| A1 | default dry-run DB test | no lasting write | `PASS` |
| A2 | explicit dry-run DB test | no lasting write | `PASS` |
| A3 | independent negative/error-bearing preflights | every failed preflight blocks commit | `PASS` |
| A4 | E8-R retry test | matching retry is a no-op | `PASS` |
| A5 | conflict test | conflict fails closed | `PASS` |
| A6 | complete diff | no generic framework | `PASS` |
| A7 | parser/lookup tests | explicit portfolio, derived workspace | `PASS` |
| A8 | dry-run DB assertions | zero lasting write | `PASS` |
| A9 | all semantic replay counterexamples | each check fails closed independently | `PASS` |
| A10 | exact-output and sentinel tests | deterministic and sanitized | `PASS` |
| A11 | no real-PostgreSQL rehearsal | environment required | `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED` |
| A12 | no isolation proof | environment required | `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED` |
| A13 | route/API/frontend search | CLI-only | `PASS` |
| A14 | no rehearsal | environment required | `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED` |
| A15 | no rehearsal | environment required | `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED` |
| A16 | complete diff/source searches | no forbidden WP7 surface or equation | `PASS` |
| A17 | real post-commit error/mismatch probes | critical non-zero halt before instructions | `PASS` |
| A18 | call-site review/tests | no pre-preparation mutation | `PASS` |
| A19 | call-site review/tests | pure evaluator only | `PASS` |

## 28. Counterexample-search findings

Legacy/native `success=True + populated error`, the real post-commit equivalent, `success=False`, replay exception, incomplete holdings, missing/extra/invalid/high-precision-different basis, cash `None`, adjacent/sub-cent P&L difference, secret sentinels, toggle restoration, public endpoint search, and local ordinary-basis-formula search were attempted. Every invalid case failed closed with stable sanitized evidence; every valid exact case passed. No successful falsification remains.

## 29. Remaining defects/observations

| Category | Finding |
|---|---|
| WP7 implementation defect | none |
| LM13 predecessor-test debt | literal CLI prohibition remains red and requires later successor-boundary synchronization |
| rehearsal pending | A11/A12/A14/A15 and WP7 portions of `MINOR-5`/`NEW-MINOR-A` |
| environment/tooling observation | default Windows pytest temp root is inaccessible; verified external base works |
| documentation-only observation | focused-test module header still omits A10 from its acceptance list although A10 tests exist |

## 30. Review artifact created

This additive record is the sole repository artifact created by this review. The three prior failed-review records and successful WP5 fresh-review precedent establish that the independent result is preserved additively rather than replacing history.

## 31. Repository/diff verification

Post-artifact verification re-hashes all protected implementation, test, fixture, planning, prior-review, WP5 overlay, LM13, Decision Log, and INDEX members; verifies this record is the only review-attributable file; runs working and cached diff checks; confirms an empty index; and creates no commit. Those final mechanical results accompany this record's final report.

## 32. Resulting WP7 constitutional state

WP7 Planning remains `CONFIRMED / FROZEN`. The current implementation has now passed fresh independent implementation re-review, but has not been Implementation Confirmed or Frozen. LM13 remains separate predecessor-test synchronization debt; rehearsal-dependent acceptance remains pending. No closeout, rehearsal, release, deployment, production, staging, or commit act occurred.

## 33. Fresh independent re-review disposition

**`BANPU-WP7 IMPLEMENTATION RE-REVIEW PASSED`**

## 34. Exact next constitutional act

The exact next act is **BANPU-WP7 Implementation Confirmation**, not LM13 synchronization. The controlling lifecycle precedent is the established implementation chain: authorized implementation → passing independent implementation review → Implementation Confirmation → Implementation Freeze. Both passing WP5 fresh reviews name Confirmation immediately, while preserving LM13 as separate debt; the Confirmation records likewise deny LM13 synchronization. Successor-boundary/repository synchronization does not interpose between a passing implementation review and Confirmation. This review performs neither act.
