# BANPU-WP5 — Fresh Independent Implementation Re-Review

**Artifact class:** Additive fresh independent implementation re-review record
**Review date:** 2026-08-17
**Review boundary:** `FRESH INDEPENDENT IMPLEMENTATION RE-REVIEW ONLY`
**Historical predecessor:** the first Independent Implementation Review failed
**Disposition:** `FAIL — IMPLEMENTATION CORRECTION REQUIRED`
**Implementation confirmation/freeze/closeout performed:** `NO`
**Production snapshot correction authorized:** `NO`

## 1. Review method and entry state

This review independently read the live repository, the frozen planning corpus,
the implementation authority chain, the prior failed review, current source and
tests, and reproduced tests. The correction agent's completion statement and
reported test count were not used as proof. Production code, tests, planning,
governance, lifecycle records, release/deployment state, and the Git index were
not modified. This record is the only additive artifact created by this act.

Entry verification:

| Requirement | Determination |
|---|---|
| Prior review | [`BANPU_WP5_INDEPENDENT_IMPLEMENTATION_REVIEW.md`](BANPU_WP5_INDEPENDENT_IMPLEMENTATION_REVIEW.md) remains byte-identical and records exactly `FAIL — IMPLEMENTATION CORRECTION REQUIRED` |
| Planning | Original WPP and Mechanical Continuity amendment remain byte-identical to Planning Freeze |
| Authority | Allocation, original Authorization, D7 amendment/reapprovals/Binding Freeze, Planning Confirmation, and Planning Freeze remain present and unchanged; no later WP5 planning or authority amendment exists |
| Lifecycle | No WP5 Implementation Confirmation, Implementation Freeze, closeout, or WP6 allocation exists |
| Git/index | Corrected implementation is unstaged; the index was empty at entry |
| Production/release | No production-data act, reconstruction, repair execution, release, deployment, or deployment-hook change is present |

The entry state is consistent, so the re-review proceeds.

## 2. Frozen planning identity

The frozen normative planning corpus remains exactly:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `docs/implementation/BANPU_WP5_WORK_PACKAGE_PLAN.md` | 42,903 | `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523` |
| `docs/implementation/BANPU_WP5_WORK_PACKAGE_PLAN_AMENDMENT_MECHANICAL_CONTINUITY.md` | 31,939 | `3ADAE8390462B8B93BCF19A3D8BF6182FB08D19D5860D97D4F8FE360851DFC4F` |

Using Planning Freeze §4's ordered UTF-8 manifest format
`path<TAB>SHA256<TAB>bytes<LF>`, the independently reproduced aggregate is:

`0C5EBFBBE6B6C8A3B823C0AC96BDB1F8C1492B5F36AE0A923D429CB20D9B791C`

This exactly matches [`BANPU_WP5_PLANNING_FREEZE_RECORD.md`](BANPU_WP5_PLANNING_FREEZE_RECORD.md), whose live identity is 21,455 bytes, SHA-256
`85400A5C0141BBB98ED96924218E0B28C16EE553D2B3A9C9358A41D01E87EC29`.

## 3. Prior failed-review identity

The historical failed review is 25,601 bytes, SHA-256
`66461622B5BA97173E4FF75EF2065716347C869907088C5FF114A11E124F50CC`.
It remains unchanged and its disposition is exactly:

`BANPU-WP5 INDEPENDENT IMPLEMENTATION REVIEW — FAILED — IMPLEMENTATION CORRECTION REQUIRED`

This re-review does not overwrite or reinterpret that historical failure.

## 4. Exact corrected implementation corpus

The current WP5 implementation corpus contains exactly nine modified paths.
All are named by the Authorization Record's production/test allowlists.
The aggregate uses ordered UTF-8 rows
`path<TAB>status<TAB>SHA256<TAB>bytes<LF>`.

| Path | Status | Bytes | SHA-256 |
|---|---:|---:|---|
| `backend/manage.py` | M | 230,045 | `2422491A5E520BB92533C296A6D0E8580256F158D17EB209749D1ED1B3AA751A` |
| `backend/services/portfolio_metrics.py` | M | 10,642 | `514E9FF605E97A7C555D4C28E4F4F8C271BB3EED3B538AD1EC32A5976EF6D2AC` |
| `backend/services/portfolio_rebuilder.py` | M | 129,334 | `D94E686DB2EFF8F95B1047FA470A2DD94B663F0847233260FDEC9B4626422765` |
| `backend/services/portfolio_snapshots.py` | M | 33,472 | `20C08265DCE777346716F6F9A436B949720C1741011127BA6F74D5E1F80E35C5` |
| `backend/services/snapshot_return_recovery.py` | M | 13,097 | `18D89455C8D9DD2CE6A02C44235CAA83E71C8DDC94E32773343809FED9A9F560` |
| `backend/tests/test_portfolio_metrics.py` | M | 16,944 | `3BCD688F6ABD8E073062FD091C546343F0C80BDE73F7837D98AC44772CD8FE91` |
| `backend/tests/test_snapshot_return_recovery.py` | M | 42,610 | `DC64DC7431B4C64E69EB527E7B3E4B85C8FC679AF4713737E514E626594191F1` |
| `backend/tests/test_portfolio_rebuilder.py` | M | 104,275 | `F5D62A8A012316FF632B6862FA5497B293D719950C7DC7BFE9F4353A784F3160` |
| `backend/tests/test_verify_snapshots.py` | M | 44,522 | `0EF3E1BA1111071AC3F5537248E3E81DB9BB1AD5367156583CE12BAE0A70262D` |

Corrected implementation-corpus aggregate:
`7E2F02776A1928A0ADF8DF0FAE392EB55F5A44641B11E308EE5F089C1BD4D9DF`.

The exact Authorization Record §4.2 test allowlist is
`test_portfolio_metrics.py`, `test_portfolio_metrics_parity.py`,
`test_snapshot_return_recovery.py`, `test_portfolio_rebuilder.py`, and
`test_verify_snapshots.py`. `test_position_conversion_replay.py` has zero live
Git diff; `test_portfolio_snapshots_wp5.py` is absent; no replacement
unauthorized test path exists.

## 5. Correction-diff reconstruction

Comparison with the prior review's exact ten-path corpus establishes:

- byte-identical retained production behavior in `portfolio_metrics.py`,
  `portfolio_rebuilder.py`, `portfolio_snapshots.py`, and
  `snapshot_return_recovery.py`;
- byte-identical retained evidence in `test_portfolio_metrics.py`;
- required correction in `manage.py`: standalone §10.3 assessment/audit,
  alongside §10.4 invocation, and exact `Decimal` anomaly evidence;
- required/acceptable relocation into `test_portfolio_rebuilder.py` and
  `test_snapshot_return_recovery.py`, with removal of all WP5 changes from
  `test_position_conversion_replay.py` and deletion of the unauthorized new
  test file;
- required test expansion in `test_verify_snapshots.py` for consumer outcomes,
  severity/status, all `NOT_EVALUABLE` classes, persisted-state preservation,
  and independence;
- no unrelated source change and no authority expansion.

The attempted A10 correction is incomplete (§9): relocation cured file-scope
authority but did not cure the prior review's registry-provenance evidence gap.
This is not unexplained drift; it is an incomplete required correction.

## 6. §10.3 and §10.4 separation

**PASS.** `_assess_tolerance_admissibility()` exposes the exact independent
`ABSENT` / `NON_DECIMAL_EXACT` / `NON_FINITE` / `NEGATIVE` / `ADMISSIBLE`
taxonomy. `_audit_tolerance_admissibility()` reports that result independently.
`_evaluate_mechanical_continuity()` and `_audit_mechanical_continuity()` retain
their separate D2–D6 reconciliation responsibility. `_audit_portfolio()` calls
the two audit consumers on separate consecutive invocations for the same
canonical conversion context; neither consumes or suppresses the other's
result. Diagnostics distinguish tolerance admissibility through
`details["obligation"] == "tolerance_admissibility"` and its reason, while
reconciliation diagnostics carry metric/tolerance or invalid-field evidence
and distinct descriptions. No economic or numerical policy was added.

Sharing `AuditCheck.MECHANICAL_CONTINUITY` is faithful. The frozen amendment
authorizes exactly that one new audit enum member and requires §10.3 and §10.4
to be separately invoked/reportable; it does not require or authorize a second
enum identity. Separate functions, invocation results, descriptions, and
details satisfy the distinction. Adding a symmetric reconciliation
`details["obligation"]` value could improve presentation but is not required.

## 7. Exact Decimal evidence

**PASS.** The classifier performs only `Decimal` multiplication, subtraction,
absolute value, division, and multiplication by integer `100`. There is no
`float()`, rounding, quantization, or alternate rounding context in the D7
path. `MechanicalContinuityResult.metric_pct` and `.tolerance_pct` remain
`Decimal`; `_audit_mechanical_continuity()` places those same objects in
`AuditAnomaly.details`; `_print_audit_anomaly()` does not enter its int/float
formatting branch for `Decimal` and prints exact `str(Decimal)` output. No
lossy intermediate serializer exists before governed evidence storage.
Annotation affects only the above-tolerance state. A20 asserts `Decimal`
identity/value in consumer details; A28 supplies repeating-decimal evidence
that would expose quantization. Together with full-path inspection, the exact
evidence obligation is satisfied.

## 8. Test-surface authorization

**PASS.** Every current WP5 test diff is in an authorized path. Moving rebuild
tests to `test_portfolio_rebuilder.py` cures their prior scope defect. Moving
successor/predecessor identity tests to `test_snapshot_return_recovery.py`
cures file authorization only; it does not by itself cure A10's substantive
evidence defect (§9).

## 9. WP5-A11 and successor-identity evidence

**A11: PASS — DIRECT EVIDENCE.** The corrected test creates a predecessor
`PortfolioItem` with predecessor `asset_id`, creates a canonical
`POSITION_CONVERSION` whose effective date is after the requested snapshot
date, generates that pre-boundary snapshot, and proves the predecessor identity
remains while the successor identity does not leak early. This is the exact
temporal/identity scenario; it is no longer an ordinary unrelated holding.

**A10: INSUFFICIENT EVIDENCE.** The relocated A10 test directly inserts a
successor-shaped `PortfolioItem(asset_id=5002)` and then proves snapshot
serialization copies `PortfolioItem.asset_id`. It does not create the successor
registry record, execute/materialize the conversion, or trace the asserted ID
from that registry successor through the converted `PortfolioItem` into the
snapshot. Existing WP4 tests separately prove conversion materialization and
the production source separately proves snapshot copying, but the failed
review explicitly required replacement with registry-bound successor
provenance. The corrected A10 is materially the same disconnected fixture and
therefore does not close that blocker.

## 10. A12–A25 consumer audit

| Rows | Determination |
|---|---|
| A12–A14 | Direct standalone §10.3 assessment and audit-consumer evidence: rejected categories report independently; admissible zero/non-negative values emit no false finding |
| A15–A16 | Classifier arithmetic plus audit-consumer no-anomaly and portfolio `PASS` evidence, including exact-tolerance inclusivity |
| A17–A19 | Null, empty, and whitespace-only annotations remain unannotated failures; each emits one `CRITICAL` anomaly and portfolio `FAIL` (exit-2 contribution) |
| A20 | Non-empty annotation yields warning-only status, exact `Decimal` details, no metric alteration, and read-only evidence shared with A30 |
| A21 | Every missing required operand produces `NOT_EVALUABLE`, `CRITICAL`, and portfolio `FAIL` |
| A22 | Malformed non-Decimal evidence produces the same consumer-level fail-closed result without numeric comparison |
| A23 | `NaN`, positive infinity, and negative infinity produce the same consumer-level fail-closed result |
| A24 | Zero and negative predecessor reference price produce the same consumer-level fail-closed result |
| A25 | Zero, negative, malformed, and absent conversion ratios produce the same consumer-level fail-closed result |

No row is passed solely from a classifier enum/string. A12–A25 are sufficient.

## 11. WP5-A30 read-only evidence

**PASS — SHARED DIRECT EVIDENCE.** The test persists a real
`PortfolioSnapshot`, captures every ORM column, invokes both D7 audit consumers
for `PASS`, `ANNOTATED_BOUNDARY_DISCONTINUITY`,
`MECHANICAL_CONTINUITY_FAILURE`, and `NOT_EVALUABLE`, expires/requeries, and
compares every column. This covers holdings JSON, NAV, return fields, and all
other persisted snapshot columns rather than a selected-column proxy. Source
inspection confirms both consumers are object readers with no session/write
operation. No D7 mutation was found.

## 12. WP5-A31 independence

**PASS — SHARED DIRECT EVIDENCE.** In the D7 direction, the behavioral test
executes every D7 outcome while a patched real `portfolio_rebuilder` module
entry asserts reconstruction is never invoked. In the converse direction, a
bounded rebuild proceeds using canonical conversion evidence that would fail
D7 (50% metric against 1% tolerance), proving the guard does not depend on the
D7 verdict. Direct source/import inspection confirms no shared predicate,
result identity, or call path. `co_names` remains supplementary only. The
combined evidence would fail under either practical coupling direction.

## 13. Rebuild zero-provider-call and preservation evidence

**PASS — SHARED DIRECT EVIDENCE.** A4/A5 patch
`services.portfolio_rebuilder._build_price_matrix`, the actual Stage 2
historical-price fetch orchestration point, and assert it is never called for
both refusal cases. They also assert unsuccessful boundary result and zero
`db.add`; source ordering independently proves the guard occurs before snapshot
read-for-reconstruction, provider fetch, snapshot construction/write, backup,
execution-plan application, and commit. A6 proves an exact-boundary rebuild
reaches the real fetch boundary once. A8 compares every ORM column and excludes
the pre-boundary date from writes. The evidence is sufficient.

## 14. C1/C2 regression check

**PASS.** These production files are byte-identical to the first review's
accepted versions. `POSITION_CONVERSION` remains a mutually exclusive metrics
branch with zero external/import/manual flow; absent CIL contributes nothing;
present canonical CIL realized P&L, fees, and taxes are admitted exactly once;
unrelated transaction branches are unchanged. Live and recovery transaction
whitelists still include only the necessary added `POSITION_CONVERSION` type
and both delegate arithmetic to `compute_period_metrics()`. No provider or
current-price substitute was introduced.

## 15. C3/C4/C5/C6 regression check

- **C3:** pass; earliest transition from effective canonical transactions,
  exact `from_date` predicate, `skip_snapshots` bypass, and pre-fetch/pre-write
  refusal remain byte-identical.
- **C4:** pass; admissible bounded reconstruction structurally excludes and
  preserves every pre-boundary ORM column/content byte represented by the row.
- **C5:** pass; the genuine +150% suspension-gap return remains ordinary,
  unclamped, unsmoothed, and unreclassified in live/recovery arithmetic.
- **C6 production behavior:** correct and unchanged; holdings JSON sources
  `asset_id` directly from `PortfolioItem.asset_id`. A11 is cured, but A10's
  required registry-provenance acceptance evidence remains insufficient.

## 16. Full operative acceptance matrix

Historical `WP5-BLOCKED` is non-operative.

| Row | Result | Evidence |
|---|---|---|
| WP5-A1 | PASS — DIRECT EVIDENCE | no-CIL accounting fixture |
| WP5-A2 | PASS — DIRECT EVIDENCE | CIL exactly-once and mixed-window fixtures |
| WP5-A3 | PASS — DIRECT EVIDENCE | real recovery-path parity |
| WP5-A4 | PASS — SHARED DIRECT EVIDENCE | refusal, zero actual fetch-boundary call, zero write plus source order |
| WP5-A5 | PASS — SHARED DIRECT EVIDENCE | pre-transition refusal with the same direct observables |
| WP5-A6 | PASS — DIRECT EVIDENCE | exact-boundary rebuild proceeds and fetches once |
| WP5-A7 | PASS — DIRECT EVIDENCE | no-conversion guard regression |
| WP5-A8 | PASS — SHARED DIRECT EVIDENCE | every ORM column/content preserved and no pre-boundary write |
| WP5-A9 | PASS — SHARED DIRECT EVIDENCE | +150% result plus no-clamp source inspection |
| WP5-A10 | INSUFFICIENT EVIDENCE | disconnected successor-shaped item; no registry→conversion→snapshot provenance chain |
| WP5-A11 | PASS — DIRECT EVIDENCE | future conversion plus pre-boundary predecessor identity |
| WP5-A12 | PASS — DIRECT EVIDENCE | independent NEGATIVE report |
| WP5-A13 | PASS — DIRECT EVIDENCE | independent NON_FINITE/NON_DECIMAL_EXACT/ABSENT reports |
| WP5-A14 | PASS — DIRECT EVIDENCE | ADMISSIBLE and no finding |
| WP5-A15 | PASS — DIRECT EVIDENCE | below-tolerance consumer no-anomaly/PASS |
| WP5-A16 | PASS — DIRECT EVIDENCE | equality consumer no-anomaly/PASS |
| WP5-A17 | PASS — DIRECT EVIDENCE | CRITICAL and FAIL/exit-2 contribution |
| WP5-A18 | PASS — DIRECT EVIDENCE | empty annotation CRITICAL and FAIL |
| WP5-A19 | PASS — DIRECT EVIDENCE | whitespace annotation CRITICAL and FAIL |
| WP5-A20 | PASS — SHARED DIRECT EVIDENCE | WARNING, warning-only status, exact Decimal details, A30 immutability |
| WP5-A21 | PASS — DIRECT EVIDENCE | all missing operands, CRITICAL, FAIL |
| WP5-A22 | PASS — DIRECT EVIDENCE | malformed numeric evidence, CRITICAL, FAIL |
| WP5-A23 | PASS — DIRECT EVIDENCE | all non-finite classes, CRITICAL, FAIL |
| WP5-A24 | PASS — DIRECT EVIDENCE | zero/negative predecessor, CRITICAL, FAIL |
| WP5-A25 | PASS — DIRECT EVIDENCE | invalid ratio classes, CRITICAL, FAIL |
| WP5-A26 | PASS — DIRECT EVIDENCE | distinct state, description, details, never silent |
| WP5-A27 | PASS — SHARED DIRECT EVIDENCE | Decimal result/type and full-path no-float inspection |
| WP5-A28 | PASS — DIRECT EVIDENCE | repeating Decimal equals unquantized formula |
| WP5-A29 | PASS — DIRECT EVIDENCE | distinct authorized AuditCheck identity |
| WP5-A30 | PASS — SHARED DIRECT EVIDENCE | all states, real persisted row, every column, source inspection |
| WP5-A31 | PASS — SHARED DIRECT EVIDENCE | behavioral independence in both directions plus source inspection |
| WP5-A32 | PASS — SHARED DIRECT EVIDENCE | canonical typed inputs and no provider/network/ticker derivation |

Because A10 remains `INSUFFICIENT EVIDENCE`, the overall re-review cannot pass.

## 17. Residual evidence dispositions

**MINOR-2 WP5 half:**
`IMPLEMENTED — ACCEPTANCE EVIDENCE SUFFICIENT FOR REVIEW`. Both distinct
obligations—§10.3 tolerance admissibility and §10.4 mechanical-continuity
reconciliation—are implemented and sufficiently evidenced. This review does
not formally close the residual.

**POSITION_CONVERSION_REBUILD_BOUNDARY:** implementation and acceptance
evidence are sufficient. The refusal predicate, earliest transition boundary,
`from_date=None`, pre-boundary and exact-boundary cases, `skip_snapshots`, zero
provider fetch/write before refusal, and bounded preservation are established.
This review does not formally close the residual.

## 18. Focused test reproduction

Command from `backend/`:

```text
.\venv-test\Scripts\python.exe -m pytest -q \
  tests/test_portfolio_metrics.py tests/test_portfolio_metrics_parity.py \
  tests/test_snapshot_return_recovery.py tests/test_portfolio_rebuilder.py \
  tests/test_verify_snapshots.py tests/test_position_conversion_live.py \
  tests/test_asset_registry.py tests/test_transaction_canonicalizer.py \
  tests/test_position_conversion_quote_contract.py
```

An independent `--collect-only -q` run collected **533 tests**. Execution
result: **533 passed, 0 failed, 0 skipped, 0 errors; 1,446 warnings; 7.29s**.
The set uses all current authorized WP5 test surfaces plus the frozen
conversion/registry/parser/quote-contract regressions. The two formerly
unauthorized paths are intentionally absent.

## 19. Broader regression reproduction

Identical current and baseline command (from each isolated `backend/`):

```text
<venv-test-python> -m pytest tests -q --tb=no \
  --ignore=tests/investigate --ignore=tests/test_pandas.py \
  --ignore=tests/test_snapshot_repair.py --ignore=tests/test_dr.py \
  --ignore=tests/test_yf.py
```

| State | Passed | Failed | Skipped | Errors | Warnings |
|---|---:|---:|---:|---:|---:|
| Corrected live state | 2,875 | 62 | 32 | 3 | 5,185 |
| Isolated pre-WP5 baseline (`HEAD` plus the pre-existing WP4 dirty production/test surface) | 2,839 | 62 | 32 | 3 | 5,138 |

JUnit node-identity comparison found **65 bad-node identities in each state,
zero only-current identities, and zero only-baseline identities**. Thus WP5
adds 36 passing tests and no new failure/error identity. The broad failures and
setup errors are pre-existing. Native crash-prone scratch/investigation files
remain excluded exactly as in the prior review. Temporary baseline and JUnit
artifacts were removed.

## 20. Diff, scope, and minimality audit

No schema/model/migration change, public endpoint, provider-derived substitute,
provider-semantics change, WP3/WP4 rewrite, D7/rebuild coupling, debug fallback,
production mutation authority, repair execution, release/deployment hook, or
unrelated refactor was found in the WP5 corpus. The two transaction-whitelist
widenings remain necessary and bounded. New tolerance helpers are required by
§10.3 separation. The shared audit identity is the exact frozen identity.
`details["obligation"]` makes §10.3 separately observable. The retained
`models.asset` import is still necessary for isolated SQLite FK metadata.
Supplementary `co_names` assertions are non-primary and non-blocking.

The current production diff is minimal. The relocated A10 fixture is authorized
and harmless but insufficient as governed proof; strengthening it within an
already-authorized test path is the minimal remaining correction.

## 21. Blocking defect

Exactly one blocking acceptance-evidence defect remains:

1. **WP5-A10 registry-bound successor provenance is not directly proven.**
   Replace or extend the authorized A10 evidence so one connected fixture
   creates the actual predecessor/successor registry identities, executes or
   faithfully materializes the governed conversion transition, generates a
   post-boundary snapshot, and asserts its holdings entry contains the actual
   successor registry `asset_id` and never the predecessor ID. This can be
   corrected wholly within the existing authorized test surface; no production
   change and no authority/planning amendment is needed.

## 22. Non-blocking findings

- A symmetric `details["obligation"] = "mechanical_continuity_reconciliation"`
  could make machine presentation more uniform, but existing function,
  invocation, description, and evidence distinctions already satisfy frozen
  planning.
- The broader suite's pre-existing failures, setup errors, deprecations, and
  cache warning remain repository test-environment debt, not WP5 regressions.

## 23. Repository verification and final disposition

After writing this artifact, final verification must and did confirm: the
implementation aggregate remains
`7E2F02776A1928A0ADF8DF0FAE392EB55F5A44641B11E308EE5F089C1BD4D9DF`;
the planning aggregate remains
`0C5EBFBBE6B6C8A3B823C0AC96BDB1F8C1492B5F36AE0A923D429CB20D9B791C`;
Planning Freeze and the prior failed review remain byte-identical; all nine
implementation paths remain authorized; relative artifact links resolve;
source/test bytes are unchanged by this review; and nothing is staged,
committed, or pushed. Graphify was queried before code inspection; `graphify
update .` is not required because no code was modified.

**`BANPU-WP5 FRESH INDEPENDENT IMPLEMENTATION RE-REVIEW — FAILED — IMPLEMENTATION CORRECTION REQUIRED`**

Production snapshot correction is authorized: **NO**.

The exact next constitutional act is a bounded **BANPU-WP5 implementation
correction** limited to the A10 acceptance evidence above, followed by another
fresh independent implementation re-review. It is not Implementation
Confirmation, Implementation Freeze, closeout, synchronization, WP6 allocation,
production reconstruction, release, or deployment. This review performs none
of those acts.
