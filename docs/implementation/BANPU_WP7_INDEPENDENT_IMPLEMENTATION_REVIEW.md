# BANPU-WP7 — Independent Implementation Review and Predecessor-Test Conflict Classification

**Artifact class:** Additive independent implementation review record  
**Review date:** 2026-08-19  
**Review boundary:** Read-only independent review; no implementation confirmation, freeze, rehearsal, staging, commit, or production act  
**Disposition:** `FAIL — IMPLEMENTATION CORRECTION REQUIRED`

## 1. Review entry-state verification

HEAD is `ae223a42df688563748c0e6e6cb898e66bcb3da0`; the index is empty. The implementation candidate consists only of the modified `backend/manage.py` plus new `backend/tests/fixtures/banpu_wp7_position_conversion_manifest.json` and `backend/tests/test_apply_position_conversion_cli.py`. No production/release/deployment act and no prior WP7 Implementation Confirmation, Implementation Freeze, or closeout artifact exists.

## 2. Frozen implementation authority

The frozen WPP (`53,998` bytes, `701` lines, SHA-256 `9a5f4f797ad800e8a6e2caa475e428baa6bb5693686401f47ce131e829952897`) and Authorization §3/§4 expressly authorize `apply_position_conversion`, its `backend/manage.py` implementation, and CLI orchestration of the existing `execute_position_conversion()` service. WP7-C1 is not permissive inference; it is a direct frozen requirement.

## 3. Predecessor-test origin and intent

`test_position_conversion_live.py::test_lm13_no_public_endpoint_or_cli_references_execute_position_conversion` is a WP4 LM-13 surface test. The WP4 WPP defines LM-13 as no public endpoint or frontend authoring path and says the service remains direct-internal invocation pending WP7. Its implementation scans `main.py`, routes, and `manage.py`, so its literal CLI prohibition is broader than its named public-surface purpose.

## 4. Conflict classification

**Classification A — `STALE PREDECESSOR TEST — WP7 AUTHORITY SUPERSEDES CLI PORTION`.** Roadmap §6 explicitly says WP4 keeps operator access service-only and defers CLI wiring to WP7; Sequence §6 says the service is unreachable except by direct internal invocation pending WP7. The public/API and frontend portions remain controlling. WP7 has no authority to edit the predecessor test, so the still-red repository result cannot be ignored.

## 5. Public-endpoint boundary

Repository search found no conversion reference in `backend/main.py`, `backend/routers`, or `frontend`. The candidate is CLI-only and preserves the no-public-endpoint/no-frontend-authoring boundary.

## 6. Implementation diff review

The candidate does not alter a frozen WP3-WP6 production surface, the manifest contract, provider-fetch code, API routes, frontend, PD-3, or WP8-owned behavior. It derives `ws_id` from the resolved portfolio and makes no hidden provider fetch. However, its replay implementation does not meet frozen WP7 replay semantics; that is a blocking defect, not scope expansion.

## 7. Idle-session integration finding

The post-preparation validation performs reads after the separately committed registry-preparation act. The following `db.rollback()` releases only that read/autobegin transaction; it cannot undo the already committed preparation and is required because `execute_position_conversion()` rejects a non-idle session. This is a correct mechanical session boundary, not a planning deviation.

## 8. Quote-gate review

The implementation uses the frozen manifest-only checks and correctly leaves live provider evidence to WP3's continuous fetch-time gate. Passing `conversion.successor.provider_symbol` as `requested_symbol` is mechanically prescribed by WPP §7.2, not a new design choice. Some live-evidence failure branches are necessarily unreachable in this CLI because it intentionally does not fetch provider evidence; the report accurately distinguishes them and does not credit them as CLI proof.

## 9. Mechanical-continuity review

Only `_evaluate_mechanical_continuity()` is called, and `PASS`/`ANNOTATED_BOUNDARY_DISCONTINUITY` proceed while `NOT_EVALUABLE` and `MECHANICAL_CONTINUITY_FAILURE` block. Canonical parsing requires a non-empty annotation, making an unannotated above-tolerance `MECHANICAL_CONTINUITY_FAILURE` unreachable for a schema-valid manifest. The negative-tolerance test proves only the different `NOT_EVALUABLE` branch; it is not evidence of the intended above-tolerance fail-closed branch.

## 10. Replay/session review

**Blocking finding WP7-IIR-B1.** `_preflight_replay_mode_sanity()` does exercise both flag values and restores/rolls back the toggle, but it ignores `legacy.success`, `native.success`, errors, basis, and realized P/L. It compares only rounded reconstructed cash and holding count. Frozen WPP §7.2 requires comparison of holdings, basis, cash, and realized P/L; a failed rebuild can therefore appear as a passing replay preflight. The same insufficient comparison is used for the mandatory post-commit verification, leaving Planning Freeze Observation A only mechanically, not semantically, resolved.

## 11. Dry-run/no-write review

Default and explicit dry-run route through no mutation-capable registry call. The replay toggle can autoflush, but its `finally` rollback reverts it; real in-memory SQLite tests pass for both modes. The focused tests assert selected row state rather than a complete database diff, so they are weaker than the WPP's stated zero-diff evidence but source inspection finds no surviving write path in dry-run.

## 12. Idempotency/conflict review

The first commit, matching retry, and conflicting retry use the existing E8-R service behavior. Focused real-database tests show one conversion row after retry, no duplicate materialized effect, and failure without added rows on conflict. Registry preparation is separately committed and idempotently revalidated.

## 13. New-test adequacy

All 16 focused tests pass. They meaningfully cover identity lookup, parser failure, default/explicit dry-run, several preflights, registry preparation, idempotency, and conflict. They omit the frozen T8 evidence for deterministic/sanitized report content and induced post-commit replay mismatch/cache-rebuild halt. They also do not cause either replay mode to fail or prove basis/realized-P&L comparison. The negative-tolerance continuity test is the false-positive/unreachable-path limitation described in §9.

## 14. Regression-suite classification

The exact LM13 failure reproduces. The frozen §11 governing set currently returns `588 passed, 1 failed`; its one failure is LM13, with no additional failure in that corpus. The submitted `572 passed, 1 failed` count is not reproducible as a current count, but its asserted sole failure is. LM13 is authorized test-maintenance debt: the implementation is conforming on the CLI/public-boundary conflict itself, yet the repository cannot be called green.

## 15. Rehearsal-dependent acceptance

WP7-A11, A12, A14, and A15 remain `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED`. Neither the WP7 portion of `MINOR-5` nor the WP7 portion of `NEW-MINOR-A` is discharged. No compliant real-PostgreSQL rehearsal evidence exists.

## 16. Acceptance-matrix independent result

| ID | Implementation evidence | Independent finding | Status |
|---|---|---|---|
| A1 | Default branch and real SQLite test | No lasting write found | PASS |
| A2 | `--dry-run` branch and real SQLite test | No lasting write found | PASS |
| A3 | Preflight gate present | Replay failure can be accepted | FAIL |
| A4 | E8-R plus retry test | Matching retry is a no-op | PASS |
| A5 | E8-R plus conflict test | Conflict fails closed | PASS |
| A6 | Three-path candidate diff | No generic action framework | PASS |
| A7 | Required portfolio parser/lookup tests | Workspace derives from portfolio | PASS |
| A8 | Dry-run source/session rollback and tests | No lasting write found | PASS |
| A9 | Preflight implementation | Replay comparison/error handling incomplete | FAIL |
| A10 | Source report only | Required deterministic/sanitization test absent | INSUFFICIENT EVIDENCE |
| A11 | No real PostgreSQL rehearsal | Environment evidence absent | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A12 | No isolation proof | Environment evidence absent | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A13 | Route/API/frontend search | No public conversion endpoint | PASS |
| A14 | No rehearsal | Evidence absent | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A15 | No rehearsal | Evidence absent | NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED |
| A16 | Diff and route/frontend search | Forbidden surfaces untouched | PASS |
| A17 | Post-commit invokes same replay helper | Required comparison/failure semantics incomplete | FAIL |
| A18 | Read-only precondition helper | No mutation before preparation boundary | PASS |
| A19 | Direct pure-helper call | Persisted audit helper not used | PASS |

## 17. Additional defects or ambiguities

WP7-IIR-B1 and the missing T8 tests are implementation-correction items. The predecessor test is a separate successor-boundary synchronization item, not a reason to retain a prohibited literal CLI ban. No canonical contradiction or new planning ambiguity was found.

## 18. Artifact created, if precedent requires

Created this additive record only. The current WP5/WP6 failed-independent-review precedent requires a failed review to be materialized without changing implementation or predecessor tests.

## 19. Repository/diff verification

Candidate identities: `backend/manage.py` SHA-256 `2d18cc59e7bdd7e40be5e5a3a47bb61cd646da3c2a6d86dbb0b29d8d7f8b9bb4`; fixture `2b843a3ecfbb85aa9e1a6882cad7de6aa3690a94627bd7dbf4f317ed802a9e03`; focused test `8e8148aea3fcf1cbe456d9c37517f86b25d6c289400cce67dc27208d5e448540`. Allocation, Authorization, Identity Clarification, WPP, Planning Confirmation, and Planning Freeze retain their recorded identities. `git diff --check` and cached diff check pass; nothing is staged.

## 20. Independent-review disposition

**`BANPU-WP7 IMPLEMENTATION REVIEW FAILED — IMPLEMENTATION CORRECTION REQUIRED`**

## 21. Exact next constitutional act

A bounded **BANPU-WP7 implementation correction**: make both replay-mode checks fail closed on either failed replay and compare the frozen holdings/basis/cash/realized-P&L result set; add the missing T8 tests, including induced post-commit mismatch halt and deterministic/sanitized reporting; then request a fresh independent implementation re-review. The separate, later predecessor-test amendment/successor-boundary synchronization must preserve the no-public-endpoint invariant. This review performs neither act.
