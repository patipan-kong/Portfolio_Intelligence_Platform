# BANPU-WP7 — Fresh Independent Implementation Re-Review

**Artifact class:** Additive fresh independent implementation re-review record  
**Review date:** 2026-08-19  
**Review boundary:** Read-only implementation re-review; no implementation correction, Confirmation, Freeze, closeout, rehearsal, LM13 synchronization, staging, commit, release, deployment, or production act  
**Frozen WPP:** `BANPU_WP7_WORK_PACKAGE_PLAN.md`, 53,998 bytes, SHA-256 `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897`  
**Historical failed review:** `BANPU_WP7_INDEPENDENT_IMPLEMENTATION_REVIEW.md`, 10,558 bytes, SHA-256 `59D39B92DDDB8BFAACE785C49D4453EC3F423C85C2D8FC15B8E025DF601DDF74`  
**Disposition:** `BANPU-WP7 IMPLEMENTATION RE-REVIEW FAILED — IMPLEMENTATION CORRECTION REQUIRED`

## 1. Re-review entry-state verification

HEAD is `ae223a42df688563748c0e6e6cb898e66bcb3da0`. The index is empty. The frozen WP7 identities reproduce exactly: WPP `9A5F4F79…2897`, Planning Confirmation `7A44203B…E82D`, Planning Freeze `E31AEC30…8B84`, and historical failed review `59D39B92…DF74`. Their dispositions remain Planning Confirmed, Planning Frozen, and failed implementation review respectively.

The current WP7 candidate identities at review entry were:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `backend/manage.py` | 259,701 | `762A9F780C37058E7092B1AAA18B2CD89F9A0CFC34E810F47C80735F725A7B41` |
| `backend/tests/test_apply_position_conversion_cli.py` | 40,146 | `5FB4A157E24C6F854FFF6A9D0D5D5CAB2E84797BAC87A597C0EEB595AB51ADF8` |
| `backend/tests/fixtures/banpu_wp7_position_conversion_manifest.json` | 1,247 | `2B843A3ECFBB85AA9E1A6882CAD7DE6AA3690A94627BD7DBF4F317ED802A9E03` |

No WP7 Implementation Confirmation, Implementation Freeze, closeout, release, or deployment artifact exists. LM13, the Decision Log, and Implementation INDEX reproduced their prior identities. Nothing was staged and no production/release/deployment evidence was found or created.

## 2. Implementation/review lineage verification

The complete authority lineage was re-established:

frozen WP7 WPP → initial three-member WP7 candidate → failed independent implementation review → bounded replay/reporting correction → realized-P&L authority blocker → additive WP5 Amendment Authorization → bounded two-line WP5 implementation plus focused tests → fresh WP5 review PASS → fresh WP5 Confirmation → fresh WP5 Freeze → resumed WP7 consumption correction → current candidate.

No authority step was skipped. The first correction is reproducible semantically from the current helper/test additions that close replay failure handling, semantic holdings/basis/cash comparison, post-commit mismatch, and T8 evidence. The resumed correction is separately identifiable as direct `reconstructed_realized_pnl` consumption and its focused tests. The historical initial candidate identities remain recorded by the failed review (`manage.py` `2D18CC59…9BB4`, fixture `2B843A3E…A9E03`, focused test `8E8148AE…8540`). No immutable intermediate first-correction aggregate was recorded; this is a documentary observation, not an authority leap, because the pause, WP5 amendment chain, and permitted resumption are all identity-bound by the additive WP5 records.

## 3. Historical failed-finding closure matrix

| Historical finding | Current evidence | Fresh classification |
|---|---|---|
| WP7-IIR-B1 — replay `success=False`, canonical errors, and exceptions ignored | `_run_one_replay_mode()` now returns an error and the common helper fails closed | `CLOSED` for pass/fail control; fresh sanitization defect recorded in §12 |
| WP7-IIR-B1 — only cash and holding count compared | symbols, shares, average cost, explicit successor basis, cash, and realized P&L are now examined | `PARTIALLY CLOSED` — cash `None` is accepted as zero; ordinary basis is synthesized in WP7; asset identity is collected but not compared |
| WP7-IIR-B1 — basis omitted | explicit conversion-successor basis differences fail | `PARTIALLY CLOSED` — ordinary basis is newly calculated as shares × average cost instead of consumed as canonical predecessor evidence |
| WP7-IIR-B1 — realized P&L omitted | frozen `RebuildResult.reconstructed_realized_pnl` is consumed directly; `None`, zero, equal, unequal, and zero/non-zero tests exist | `PARTIALLY CLOSED` — two-decimal rounding accepts distinct six-decimal canonical results |
| WP7-IIR-B1 — same defect affected pre- and post-commit | both call the common corrected helper | `PARTIALLY CLOSED` — both also inherit the fresh incomplete-evidence and precision defects |
| A10 deterministic/sanitized evidence gap | representative T8 tests and stdout containment were added | `PARTIALLY CLOSED` — exception/result error strings remain unsanitized and several “stable fields” tests do not prove repeatable full output |
| Missing replay-failure tests | legacy, native, exception, and failed-default tests added | `CLOSED` |
| Missing full-comparison tests | symbol/share/average-cost/basis/cash/P&L tests added | `PARTIALLY CLOSED` for the semantic defects above |
| Missing post-commit mismatch test | realized-P&L-only persisted-conversion mismatch test added | `PARTIALLY CLOSED` because sub-cent divergence still passes |
| Missing deterministic/sanitized reporting tests | dry-run/preflight repeatability and representative status/sentinel tests added | `PARTIALLY CLOSED` |
| Mechanical-continuity test misstatement | test is accurately named `test_mechanical_continuity_not_evaluable_blocks_commit`; no direct unannotated-failure claim remains | `CLOSED` |

## 4. Implementation diff review

The WP7 candidate remains limited to `backend/manage.py`, the focused CLI test, and the authorized sanitized fixture. The separate modified `portfolio_rebuilder.py` and `test_portfolio_rebuilder.py` are the freshly frozen WP5 overlay, not WP7 scope. No unrelated service, manifest-contract, provider fetch, overlay replay, API, frontend, schema, migration, production behavior, PD-3, WP8, or M46 change was found.

One WP7-local accounting derivation is nevertheless present: `_extract_reconstructed_holdings()` creates `basis = round(shares * avg_cost, 2)` when the predecessor reconciliation report omits basis. This is an implementation defect/authority-boundary violation even though it is located in an authorized file.

## 5. WP5 predecessor-field consumption

`manage.py` directly reads `legacy.reconstructed_realized_pnl` and `native.reconstructed_realized_pnl`. It contains no transaction summation, snapshot/provider fallback, direct `_PortfolioState` access, or duplicate realized-P&L formula. The result is consumed only after the WP5 overlay was freshly frozen. This portion conforms.

## 6. Replay failure-handling verification

For both modes, `success=False`, a populated canonical `error`, and raised exceptions all produce a failed check. A failed mode cannot compare equal through default numeric values. However, incomplete successful-result evidence is not uniformly rejected: `reconstructed_cash=None` is converted to `0.0` by `float(value or 0)`. An independently injected `None` versus `0.0` pair returned PASS. Therefore the required failure handling is not complete.

## 7. Full replay comparison verification

- Holdings: symbol-keyed shares/average-cost comparison is semantic rather than count-only, and one-sided symbols fail. `reconstructed_holdings_count` is also checked. The extracted `asset_id`/`symbol` fields are not part of `_diff_reconstructed_holdings()`'s comparison set.
- Basis: explicit conversion-successor basis is compared, but ordinary basis is re-derived in `manage.py`; this is not direct canonical predecessor evidence.
- Cash: two-decimal normalization is inherited from the initial WP7 candidate, but `None` is incorrectly treated as zero.
- Realized P&L: the frozen predecessor field is consumed directly; `None` fails, `0.0` is valid, and ordinary unequal/zero cases fail. `round(float(value), 2)` was established for the candidate's cash comparison, not for the newly exposed six-decimal P&L result. An injected `1.001` versus `1.002` pair returned PASS, materially weakening the canonical result.

## 8. Pre-commit replay verification

Pre-commit executes legacy then native replay against existing persisted ledger state with `dry_run=True`, no candidate overlay, restores the toggle in `finally`, and rolls back session changes. Either replay failure and ordinary full-set mismatches fail. It nevertheless accepts the cash-incomplete and sub-cent P&L counterexamples in §6/§7, so WP7-A3/A9 are not satisfied.

## 9. Post-commit replay verification

Post-commit runs only for service status `applied`, after the conversion has persisted. It reuses the same comparison helper, reports `Status: applied` truthfully before any anomaly, reports `CRITICAL`, exits 1, prints no cache/rebuild instructions on mismatch, and invents no rollback. The focused realized-P&L-only `+999.0` mismatch test passes. Because the same helper accepts incomplete cash and sub-cent P&L divergence, WP7-A17 remains unsatisfied.

## 10. Replay-toggle restoration verification

Independent injected runs covered success, legacy failure, native failure, holdings mismatch, explicit basis mismatch, cash mismatch, and realized-P&L mismatch. Every run restored the original toggle and called rollback exactly once. This requirement passes.

## 11. Deterministic reporting verification

Dry-run and failed-preflight tests compare complete repeated stdout. Successful commit, `already_applied`, conflict, and post-commit mismatch tests verify stable semantic fields but do not compare complete repeated output. Source ordering is fixed, but returned error text is uncontrolled. Evidence is improved but insufficient for the full deterministic-reporting claim.

## 12. Sanitized reporting verification

Redirecting the frozen rebuilder's stdout is a valid boundary-containment mechanism: it prevents full manifest evidence and object-address debug output from escaping while leaving WP7's own pass/fail result available. It does not suppress required semantic failure evidence.

The containment is incomplete. `_run_one_replay_mode()` appends `str(exc)` or `result.error` verbatim to the WP7 report. An injected exception containing `TOKEN_SENTINEL raw_payload at 0xDEADBEEF` was reproduced verbatim in the check detail. The outer command also prints unexpected exception text verbatim. Thus A10 fails sanitized-reporting semantics despite the passing manifest-sentinel happy-path test.

## 13. Mechanical-continuity evidence verification

Production logic still calls only the accepted pure `_evaluate_mechanical_continuity()` helper. `PASS` and annotated discontinuity proceed; `NOT_EVALUABLE` and the schema-unreachable unannotated `MECHANICAL_CONTINUITY_FAILURE` block. Current test naming accurately proves `NOT_EVALUABLE` fail-closed behavior and does not claim direct coverage of the unreachable branch. Coverage is sufficient under the frozen WPP.

## 14. Registry/quote/broker conformance

Registry preconditions remain read-only before the separate preparation commit; post-preparation validation is followed by the required idle-session rollback. Quote checks remain manifest-only; no provider fetch was added. Broker facts remain schema/reference-price evidence, not a fabricated service. Registry order, provider boundary, generic-action exclusion, and accounting-service reuse remain intact.

## 15. Focused WP7 test result

Using the repository `backend/venv-test` environment and a workspace-external writable pytest base:

```text
46 passed, 0 failed
```

The first default-temp launch produced permission errors before affected test bodies; it is an environmental setup incident and was not counted as test evidence.

## 16. Governing WP7 regression result

The exact ten-file WPP §11 regression set returned:

```text
575 passed, 1 failed
```

Exact failure:

```text
backend/tests/test_position_conversion_live.py::
test_lm13_no_public_endpoint_or_cli_references_execute_position_conversion
```

Together with the current 46-test focused suite, the full current WP7 implementation-review execution is `621 passed, 1 failed`. The historical review's `588 passed, 1 failed` combined count reflected a 16-test focused file and the pre-amendment regression membership/count. The sole failing assertion is unchanged; the repository is not fully green.

## 17. LM13 classification

Classification remains `STALE PREDECESSOR TEST — WP7 AUTHORITY SUPERSEDES CLI PORTION`. WP4 WPP LM-13 names no public endpoint/frontend authoring path; Roadmap §6 explicitly defers CLI wiring to WP7; Sequence §6 says direct-internal invocation only pending WP7. The literal `manage.py` scan is the stale portion. Searches found no conversion exposure in `backend/main.py`, routers, or frontend. WP7 has no authority to edit LM13. LM13 remains separate successor-boundary debt and still blocks any repository-green statement, but it is not the reason for this implementation-review failure.

## 18. Public/API/frontend boundary

No new route, main-app wiring, public API, or frontend authoring reference to position conversion was found. WP7 remains CLI-only. PASS.

## 19. Rehearsal-dependent acceptance

WP7-A11, A12, A14, and A15 remain `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED`. The WP7 portions of `MINOR-5` and `NEW-MINOR-A` remain pending. No compliant real-PostgreSQL rehearsal evidence exists, and none was performed. These rows do not independently downgrade implementation review.

## 20. Fresh acceptance-matrix result

| ID | Current evidence | Fresh finding | Status |
|---|---|---|---|
| A1 | default dry-run real DB test/source | no lasting write | PASS |
| A2 | explicit dry-run real DB test/source | no lasting write | PASS |
| A3 | all preflights gate commit | incomplete cash evidence can pass | FAIL |
| A4 | retry test/E8-R | matching retry no-op | PASS |
| A5 | conflict test/E8-R | conflict fails closed | PASS |
| A6 | three-member WP7 surface | no generic action framework | PASS |
| A7 | parser/lookup tests | portfolio required; workspace derived | PASS |
| A8 | dry-run DB assertions and rollback | no lasting write | PASS |
| A9 | independent negative preflights | replay comparison remains incomplete/over-normalized | FAIL |
| A10 | reporting tests/stdout wrapper | raw exception/result error leakage; incomplete determinism proof | FAIL |
| A11 | no real-PostgreSQL rehearsal | environment required | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A12 | no isolation rehearsal | environment required | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A13 | route/API/frontend search | CLI-only | PASS |
| A14 | no rehearsal | environment required | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A15 | no rehearsal | environment required | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A16 | diff/boundary search | no forbidden file change, but WP7 adds an ordinary-basis equation | FAIL |
| A17 | post-commit mismatch test/common helper | large mismatch fails; incomplete/sub-cent mismatch can pass | FAIL |
| A18 | registry call-site inspection | no mutation before preparation | PASS |
| A19 | continuity call-site inspection | pure helper only | PASS |

## 21. Counterexample-search result

Failed-replay defaults, different holding symbols/quantities, explicit basis-only, cash-only, ordinary realized-P&L-only, `None` P&L, zero/non-zero P&L, toggle restoration, persisted post-commit mismatch, sentinel output, provider fetch, and API exposure were exercised or source-traced. Three falsifying counterexamples were reproduced: cash `None` versus zero passes; distinct `1.001`/`1.002` P&L passes; raw exception sentinel text leaks. Source inspection additionally found ordinary basis synthesis and non-comparison of extracted asset identity.

## 22. Remaining defects/observations

| Category | Finding |
|---|---|
| WP7 implementation defect | incomplete cash evidence is accepted as zero |
| WP7 implementation defect | ordinary basis is re-derived in `manage.py` rather than consumed from canonical predecessor evidence |
| WP7 implementation defect | two-decimal P&L normalization hides distinct frozen six-decimal results |
| WP7 implementation defect | exception/result error detail is emitted without sanitization |
| WP7 implementation observation | extracted asset identity is not included in semantic holding comparison |
| Test-evidence gap | full deterministic output is not proved for every representative terminal state |
| Stale predecessor-test debt | LM13 literal CLI prohibition remains red and out of WP7 correction scope |
| Rehearsal evidence pending | A11/A12/A14/A15, `MINOR-5`, and `NEW-MINOR-A` WP7 portions |
| Infrastructure/environment | default pytest temp root is inaccessible; external writable base works |

## 23. Review artifact created

This additive record is the only repository file created by the review. Failed fresh-review precedent (`BANPU_WP6_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW.md`) and the historical WP7 failed-review precedent require preserving the review result rather than reporting it ephemerally.

## 24. Repository/diff verification

At review completion, the WP5 fresh-frozen production/test bytes, WP7 implementation/test/fixture bytes, WPP, Planning Confirmation, Planning Freeze, historical failed review, LM13, Decision Log, and INDEX were re-hashed. Only this record is attributable to the review. `git diff --check` and cached diff check pass; the index remains empty. No code or test file was modified by this review.

## 25. Resulting WP7 constitutional state

WP7 Planning remains `CONFIRMED / FROZEN`. The historical failed implementation review remains intact. The two correction rounds and completed WP5 predecessor amendment remain visible, but the current WP7 candidate has fresh implementation defects. Rehearsal acceptance remains pending. Implementation Confirmation, Implementation Freeze, closeout, LM13 synchronization, release, deployment, staging, and commit remain unperformed.

## 26. Fresh independent re-review disposition

**`BANPU-WP7 IMPLEMENTATION RE-REVIEW FAILED — IMPLEMENTATION CORRECTION REQUIRED`**

## 27. Exact next constitutional act

A bounded **BANPU-WP7 Implementation Correction** limited to the fresh findings in §§6, 7, 11, 12, 17, 21, and 22, followed by another fresh independent implementation re-review. The correction must obtain canonical predecessor evidence/authority where WP7 cannot lawfully supply it itself; it must not silently add another accounting formula. LM13 synchronization, Implementation Confirmation, and Implementation Freeze are not performed and are not the immediate next act while implementation defects remain.
