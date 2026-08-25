# BANPU-WP5 — Second Fresh Independent Implementation Re-Review

**Artifact class:** Additive fresh Independent Implementation Re-Review record
**Review date:** 2026-08-17
**Review authority:** Fresh Independent BANPU-WP5 Implementation Re-Review Authority
**Review scope:** A10-only bounded correction plus non-regression verification of the previously reviewed candidate
**Independent disposition:** `BANPU-WP5 FRESH INDEPENDENT IMPLEMENTATION RE-REVIEW — PASSED`
**Implementation Confirmation performed:** `NO`
**Implementation Freeze, closeout, production correction, release, or deployment performed:** `NO`

## 1. Boundary and method

This is a review-only act. It does not trust a correction report as evidence and
does not modify production code, tests, planning, governance, authority, or any
lifecycle record. It independently reads the frozen planning, both historical
failed reviews, the live implementation/test bytes, the A10 fixture, the
production conversion and snapshot paths, test results, and BANPU lifecycle
precedent.

The only repository mutation made by this act is this additive review artifact.
Nothing is staged, committed, pushed, released, deployed, or executed against
production data.

## 2. Entry-state verification

All entry premises are satisfied:

- BANPU-WP5 planning remains `COMPLETE, CONFIRMED, AND FROZEN`.
- The frozen planning aggregate independently reproduces exactly as
  `0C5EBFBBE6B6C8A3B823C0AC96BDB1F8C1492B5F36AE0A923D429CB20D9B791C`.
- The [original Independent Implementation Review](BANPU_WP5_INDEPENDENT_IMPLEMENTATION_REVIEW.md)
  is unchanged and retains `FAIL — IMPLEMENTATION CORRECTION REQUIRED`.
- The [previous Fresh Independent Implementation Re-Review](BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW.md)
  is unchanged and retains `FAIL — IMPLEMENTATION CORRECTION REQUIRED`.
- The previous fresh re-review records A10 as the sole `INSUFFICIENT EVIDENCE`
  acceptance row; A1–A9 and A11–A32 passed.
- No later planning or authority amendment exists.
- No BANPU-WP5 Implementation Confirmation, Implementation Freeze, or Epic
  Closeout exists.
- The index and Decision Log contain no later WP5 production, release, or
  deployment act.
- The Git index is empty. Nothing is staged.

## 3. Frozen planning identity

The canonical manifest is UTF-8 without BOM, with each ordered row encoded as
`path<TAB>SHA256<TAB>bytes<LF>`:

| Frozen member | SHA-256 | Bytes |
|---|---|---:|
| `docs/implementation/BANPU_WP5_WORK_PACKAGE_PLAN.md` | `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523` | 42,903 |
| `docs/implementation/BANPU_WP5_WORK_PACKAGE_PLAN_AMENDMENT_MECHANICAL_CONTINUITY.md` | `3ADAE8390462B8B93BCF19A3D8BF6182FB08D19D5860D97D4F8FE360851DFC4F` | 31,939 |

**Frozen planning aggregate:**
`0C5EBFBBE6B6C8A3B823C0AC96BDB1F8C1492B5F36AE0A923D429CB20D9B791C`.

The [Planning Freeze Record](BANPU_WP5_PLANNING_FREEZE_RECORD.md) is unchanged:
21,455 bytes, SHA-256
`85400A5C0141BBB98ED96924218E0B28C16EE553D2B3A9C9358A41D01E87EC29`.

## 4. Historical review identities and findings

| Review | Bytes | SHA-256 | Preserved disposition |
|---|---:|---|---|
| Original Independent Implementation Review | 25,601 | `66461622B5BA97173E4FF75EF2065716347C869907088C5FF114A11E124F50CC` | `FAIL — IMPLEMENTATION CORRECTION REQUIRED` |
| Previous Fresh Independent Implementation Re-Review | 23,652 | `08400A5F5DE384D7793F1C64FF20B3FA341522BBEFC811A16BA38A397A298250` | `FAIL — IMPLEMENTATION CORRECTION REQUIRED` |

The previous fresh re-review's historical A10 finding is preserved: its test
manually inserted a successor-shaped `PortfolioItem(asset_id=5002)`. It began
after the registry/conversion provenance fact A10 was meant to prove, then only
showed that snapshot serialization copied the already supplied value. It did
not connect registry identity, conversion materialization, and snapshot output.

## 5. Current implementation corpus

The canonical implementation manifest uses ordered
`path<TAB>status<TAB>SHA256<TAB>bytes<LF>` rows:

| Path | Status | SHA-256 | Bytes |
|---|---|---|---:|
| `backend/manage.py` | `M` | `2422491A5E520BB92533C296A6D0E8580256F158D17EB209749D1ED1B3AA751A` | 230,045 |
| `backend/services/portfolio_metrics.py` | `M` | `514E9FF605E97A7C555D4C28E4F4F8C271BB3EED3B538AD1EC32A5976EF6D2AC` | 10,642 |
| `backend/services/portfolio_rebuilder.py` | `M` | `D94E686DB2EFF8F95B1047FA470A2DD94B663F0847233260FDEC9B4626422765` | 129,334 |
| `backend/services/portfolio_snapshots.py` | `M` | `20C08265DCE777346716F6F9A436B949720C1741011127BA6F74D5E1F80E35C5` | 33,472 |
| `backend/services/snapshot_return_recovery.py` | `M` | `18D89455C8D9DD2CE6A02C44235CAA83E71C8DDC94E32773343809FED9A9F560` | 13,097 |
| `backend/tests/test_portfolio_metrics.py` | `M` | `3BCD688F6ABD8E073062FD091C546343F0C80BDE73F7837D98AC44772CD8FE91` | 16,944 |
| `backend/tests/test_snapshot_return_recovery.py` | `M` | `5283299E9D10B46E65D93C6875C898040180F482D67B07EA45A6CE3A223FF9F1` | 48,797 |
| `backend/tests/test_portfolio_rebuilder.py` | `M` | `F5D62A8A012316FF632B6862FA5497B293D719950C7DC7BFE9F4353A784F3160` | 104,275 |
| `backend/tests/test_verify_snapshots.py` | `M` | `0EF3E1BA1111071AC3F5537248E3E81DB9BB1AD5367156583CE12BAE0A70262D` | 44,522 |

**Current implementation corpus aggregate:**
`A4C26406A3D8CEB1F85210040FAA145FBB6FD8CD2CF14AAF12812F013168F08F`.

## 6. A10 correction reconstruction

Comparison with the exact corpus bound by the previous fresh re-review shows
one changed member only:

| Path | Previous identity/bytes | Current identity/bytes | Determination |
|---|---|---|---|
| `backend/tests/test_snapshot_return_recovery.py` | `DC64DC7431B4C64E69EB527E7B3E4B85C8FC679AF4713737E514E626594191F1` / 42,610 | `5283299E9D10B46E65D93C6875C898040180F482D67B07EA45A6CE3A223FF9F1` / 48,797 | authorized A10-only test correction |

All other eight corpus members are byte-identical to the prior review. The
test correction adds the registry/domain and real conversion-service imports,
adds `_mint_and_prepare_registry()` and `_a10_conversion_payload()`, and
replaces the disconnected successor-shaped A10 fixture with one connected
registry → conversion → materialization → snapshot fixture. No production byte,
governance byte, or other WP5 test byte drifted.

## 7. Exact frozen A10 requirement

The frozen WPP §15 row states:

- ID: `WP5-A10`;
- obligation: successor identity post-boundary;
- governing source: design §12;
- implementation surface: `portfolio_snapshots.py`;
- required evidence: holdings-JSON assertion;
- expected result: successor `asset_id` only;
- failure condition: predecessor ID leaks through.

Read together with the frozen design consumption in WPP §13, the identity
property is that a post-boundary holdings entry carries the registry-bound
successor identity from the materialized successor `PortfolioItem`; it must not
carry the predecessor ID or substitute ticker/display/provider identity.

## 8. Registry provenance review

**PASS — DIRECT EVIDENCE.** `_mint_and_prepare_registry()` uses the production
`registry.mint()` mechanism to persist two distinct assets. Their database IDs
are assigned by that path and are never hard-coded as the expected answer. It
then calls production `prepare_position_conversion_registry()`, which attaches
the successor provider identifier, retires the predecessor identifier,
transitions the predecessor to `MERGED`, and creates the `MERGED_INTO`
relationship.

The helper prepares legitimate inputs only. It never creates a successor
`PortfolioItem`, edits one, or supplies a snapshot holdings object.

## 9. Conversion materialization review

**PASS — DIRECT EVIDENCE.** The test calls the real
`execute_position_conversion()` service without monkeypatching its identity
path. That service:

- parses and cross-checks the payload asset IDs;
- loads both real registry assets;
- validates the prepared provider-identifier, lifecycle, and `MERGED_INTO`
  relationship state;
- finds and removes the predecessor holding;
- creates the successor `PortfolioItem` with the validated successor asset ID;
- refreshes the row and enforces its post-write identity invariant; and
- revalidates persisted canonical payload and registry state before commit.

The payload necessarily names the registry-minted IDs because that is the real
production API contract. This is not tautological: mismatched IDs, missing
assets, an unprepared relationship, or a wrong materialized identity fail the
production validation/invariant path.

## 10. Successor `PortfolioItem` provenance

**PASS — DIRECT EVIDENCE.** Before conversion, test code creates only the
predecessor holding. No successor holding exists. After the service reports
`applied`, the test queries the successor row produced by the service and also
proves the predecessor symbol is absent.

Test code never inserts, overwrites, or reshapes that successor row. If the
service did not materialize it, the `.one()` query would fail. If it bound a
different identity, that query or the service's own post-write invariant would
fail.

## 11. Post-boundary snapshot and final identity

**PASS — DIRECT EVIDENCE.** The conversion boundary and snapshot date are both
2026-03-02, so the snapshot is at the effective post-transition state after the
conversion has been applied. `generate_daily_snapshot()` reads the materialized
portfolio state. `price_override` is keyed by the materialized row's symbol and
supplies only price; it neither contains nor controls `asset_id`.

Production snapshot code constructs each holdings record with
`"asset_id": item.asset_id`. It performs no registry/provider/ticker identity
lookup. The final assertions prove the exact registry-minted `successor.id` is
in the successor holdings entry and that `predecessor.id` is absent from all
holdings.

## 12. Adversarial A10 sufficiency

The connected fixture meaningfully fails under the governed broken states:

- wrong registry successor binding fails registry validation and/or the exact
  successor-row assertion;
- no successor materialization fails the `.one()` query before snapshotting;
- a successor row carrying a wrong asset ID fails the service invariant or
  exact holdings assertion;
- predecessor leakage fails the explicit all-holdings exclusion assertion;
- replacing `PortfolioItem.asset_id` with a ticker/display/provider value fails
  the numeric exact-ID assertion.

Source inspection complements the black-box assertions by proving the live
snapshot path performs no symbol-to-identity derivation at all. A hypothetical
re-resolution that happened to return the same database ID would be output-
equivalent, but it is not present in the reviewed bytes; any future byte change
would leave this reviewed corpus and require review again.

**A10 final result: `PASS — DIRECT EVIDENCE`.**

## 13. Helper and session-fixture review

`_mint_and_prepare_registry()` is legitimate production-backed setup.
`_a10_conversion_payload()` supplies a canonically valid conversion request;
it does not reproduce conversion materialization or snapshot identity logic.
Its IDs come from the two just-minted database rows.

The isolated session uses `expire_on_commit=False` solely to avoid SQLAlchemy's
implicit autobegin when committed ORM IDs are read before the conversion
service's idle-session guard. This mirrors the production-service test pattern
and changes test-session mechanics only. It does not alter governed production
behavior or mask a dependency failure.

No blocking or non-blocking helper concern remains.

## 14. Authorized-surface and minimality result

**PASS.** The A10 correction changed one authorized WP5 test path only:
`backend/tests/test_snapshot_return_recovery.py`.

- `backend/tests/test_position_conversion_replay.py` has zero diff.
- `backend/tests/test_portfolio_snapshots_wp5.py` remains absent.
- No replacement unauthorized test path exists.
- No production path changed after the prior review.
- The complete WP5 corpus still contains exactly the authorized nine paths.

No unrelated refactor, debug code, provider-derived identity, Decimal/rounding
regression, or D7/rebuild coupling was introduced. The correction is minimal.

## 15. A11 non-regression

**PASS — PREVIOUSLY PASSED, UNCHANGED.** The A11 bytes are within the same test
file but its test remains semantically unchanged: it creates predecessor state,
records a future-effective conversion, snapshots before that boundary, and
proves predecessor identity remains while successor identity does not leak
early.

A10 and A11 remain distinct: A10 proves post-boundary registry-bound successor
identity; A11 proves pre-boundary predecessor behavior.

## 16. Previously passed implementation bytes

The prior re-review's production findings remain valid because every relevant
production byte is identical:

- §10.3 tolerance admissibility and §10.4 continuity evaluation remain separate;
- exact `Decimal` construction, arithmetic, storage, and reporting remain intact;
- C1–C7/D7 behavior is unchanged;
- the rebuild refusal still precedes snapshot reads, provider fetches, writes,
  and commit, with exact-boundary behavior separate;
- A1–A9 and A11–A32 retain their passed production/evidence basis;
- A30 read-only and A31 D7/rebuild independence evidence are unchanged.

No architecture is re-litigated where the bound bytes did not change.

## 17. Final acceptance matrix

| Row | Final disposition | Basis |
|---|---|---|
| WP5-A1 | PASS — unchanged direct evidence | zero-flow classification, no CIL |
| WP5-A2 | PASS — unchanged direct evidence | CIL exact-once accounting |
| WP5-A3 | PASS — unchanged direct evidence | recovery parity |
| WP5-A4 | PASS — unchanged shared direct evidence | absent-bound refusal; no provider/write |
| WP5-A5 | PASS — unchanged shared direct evidence | pre-transition refusal; no provider/write |
| WP5-A6 | PASS — unchanged direct evidence | exact-boundary rebuild proceeds |
| WP5-A7 | PASS — unchanged direct evidence | no-conversion regression |
| WP5-A8 | PASS — unchanged shared direct evidence | every pre-boundary ORM field preserved |
| WP5-A9 | PASS — unchanged shared direct evidence | unclamped genuine suspension-gap return |
| WP5-A10 | PASS — fresh direct evidence | connected registry → conversion → materialized row → snapshot identity chain |
| WP5-A11 | PASS — unchanged direct evidence | pre-boundary predecessor identity |
| WP5-A12 | PASS — unchanged direct evidence | negative tolerance report |
| WP5-A13 | PASS — unchanged direct evidence | non-finite/non-decimal/absent reports |
| WP5-A14 | PASS — unchanged direct evidence | admissible tolerance, no finding |
| WP5-A15 | PASS — unchanged direct evidence | below-tolerance consumer pass |
| WP5-A16 | PASS — unchanged direct evidence | exact-tolerance inclusivity |
| WP5-A17 | PASS — unchanged direct evidence | null annotation critical failure |
| WP5-A18 | PASS — unchanged direct evidence | empty annotation critical failure |
| WP5-A19 | PASS — unchanged direct evidence | whitespace annotation critical failure |
| WP5-A20 | PASS — unchanged shared direct evidence | warning-only annotated discontinuity; exact Decimal |
| WP5-A21 | PASS — unchanged direct evidence | all missing operands fail closed |
| WP5-A22 | PASS — unchanged direct evidence | malformed numeric evidence fails closed |
| WP5-A23 | PASS — unchanged direct evidence | all non-finite classes fail closed |
| WP5-A24 | PASS — unchanged direct evidence | non-positive predecessor price fails closed |
| WP5-A25 | PASS — unchanged direct evidence | invalid ratio classes fail closed |
| WP5-A26 | PASS — unchanged direct evidence | not-evaluable state remains distinct |
| WP5-A27 | PASS — unchanged shared direct evidence | Decimal-only path |
| WP5-A28 | PASS — unchanged direct evidence | unquantized repeating Decimal |
| WP5-A29 | PASS — unchanged direct evidence | distinct authorized audit identity |
| WP5-A30 | PASS — unchanged shared direct evidence | persisted row, every column, all states, read-only |
| WP5-A31 | PASS — unchanged shared direct evidence | D7/rebuild independence both directions |
| WP5-A32 | PASS — unchanged shared direct evidence | canonical typed inputs; no provider derivation |

All A1–A32 pass. No `FAIL` or `INSUFFICIENT EVIDENCE` row remains.

## 18. Residual evidence dispositions

**MINOR-2 WP5 half:**
`IMPLEMENTED — ACCEPTANCE EVIDENCE SUFFICIENT FOR REVIEW`. The separately
implemented §10.3 and §10.4 obligations and their acceptance evidence remain
sufficient. This review does not formally close the residual.

**`POSITION_CONVERSION_REBUILD_BOUNDARY`:** implementation and acceptance
evidence remain sufficient. Refusal and exact-boundary behavior, zero-provider-
call observables, no-write behavior, and pre-boundary preservation are unchanged.
This review does not formally close the residual.

## 19. Focused test reproduction

Executed independently from `backend`:

```text
.\venv-test\Scripts\python.exe -m pytest -q tests/test_portfolio_metrics.py tests/test_portfolio_metrics_parity.py tests/test_snapshot_return_recovery.py tests/test_portfolio_rebuilder.py tests/test_verify_snapshots.py tests/test_position_conversion_live.py tests/test_asset_registry.py tests/test_transaction_canonicalizer.py tests/test_position_conversion_quote_contract.py
```

Result: **533 passed, 0 failed, 0 skipped, 0 errors; 1,457 warnings; 7.83s**.

## 20. Broader regression reproduction

Executed independently from `backend`:

```text
.\venv-test\Scripts\python.exe -m pytest tests -q --tb=no --ignore=tests/investigate --ignore=tests/test_pandas.py --ignore=tests/test_snapshot_repair.py --ignore=tests/test_dr.py --ignore=tests/test_yf.py
```

Current result: **2,875 passed, 62 failed, 32 skipped, 3 errors; 5,196
warnings; 44.80s**.

An isolated pre-WP5 baseline was reconstructed from `HEAD` plus only the six
pre-existing WP4 dirty members (`asset_registry.py`,
`portfolio_transactions.py`, `transaction_canonicalizer.py`, their two named
tests, and `test_position_conversion_live.py`). The identical command returned
**2,839 passed, 62 failed, 32 skipped, 3 errors; 5,138 warnings; 39.41s**.

JUnit identity comparison found 65 failure/error node IDs in each run, with
**zero current-only and zero baseline-only identities**. WP5 therefore adds 36
passes and no regression. The reported current count of `2,878 passed` is not
reproducible; the independently reproduced count remains 2,875. That report
error is not relied upon and does not affect the identity-based regression
finding.

## 21. Blocking and non-blocking findings

**Blocking defects:** none.

**Non-blocking findings:** none. The incorrect external `2,878 passed` report
is superseded by this review's direct reproduction and is not a candidate-code
or acceptance-evidence defect.

## 22. Repository verification

After creating this record, the following must remain true and is independently
rechecked in the finalization pass:

- all nine implementation members retain the identities in §5;
- frozen planning aggregate remains `0C5EBFBB...9B791C`;
- Planning Freeze and both historical failed reviews retain §§3–4 identities;
- `git diff --check` and `git diff --cached --check` pass;
- no trailing whitespace exists in this record;
- all relative artifact links resolve;
- nothing is staged;
- the working tree remains dirty only with the pre-existing WP4/WP5 corpus and
  governance history plus this additive record;
- no stage, commit, push, release, deployment, or production act occurs.

`graphify query` was used before code inspection. `graphify update .` is not
required because this review changes documentation only, not code.

## 23. Exact next constitutional act

Live BANPU-WP2/WP3/WP4 precedent fixes the post-approval sequence as independent
implementation review → Implementation Confirmation → Implementation Freeze →
closeout and later synchronization. In particular, the successful WP4 Third
Renewed Independent Implementation Review names a separate Implementation
Confirmation against the exact reviewed corpus, and the WP4 confirmation binds
those identities before freeze.

Therefore the exact next constitutional act is:

**Separate BANPU-WP5 Implementation Confirmation against the exact nine-member
implementation corpus in §5 and this additive passing review record.**

This review does not perform that act.

## 24. Final disposition

**`BANPU-WP5 FRESH INDEPENDENT IMPLEMENTATION RE-REVIEW — PASSED`**

Production snapshot correction is authorized: **NO**.

No Implementation Confirmation, Implementation Freeze, closeout,
synchronization, WP6 allocation, production reconstruction, release,
deployment, staging, commit, or push is performed or authorized by this review.
