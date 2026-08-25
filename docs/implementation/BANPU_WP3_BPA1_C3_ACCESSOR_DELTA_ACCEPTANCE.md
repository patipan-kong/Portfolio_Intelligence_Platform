# BANPU-WP3 — BPA-1 Accessor Delta Acceptance (Focused C3 Accessor-Delta Review)

**Artifact class:** Additive constitutional acceptance record
**Recorded date:** 2026-08-11
**Recorder role:** Independent C3 Accessor-Delta Review Recorder
**BPA-1 identifier:** `BPA-1`
**Governing planning corpus identity:** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Amended Work Package Plan identity:** `84E1EC24ACF436AFCC26BFABB4E982692BDB80AAF24B02828356D0F69B23045D`
**Reviewed accessor:** `backend/services/data_fetcher.py` — `resolve_successor_bindings(symbols)` (lines 256–280)
**Disposition:** `BANPU-WP3 BPA-1 ACCESSOR DELTA INDEPENDENTLY ACCEPTED`

## 1. Nature of this record

This artifact materializes, as a durable repository record, a determination
already reached over the current repository bytes: that
`resolve_successor_bindings(symbols)` in `backend/services/data_fetcher.py`
satisfies the Focused C3 Accessor-Delta Review gate required by
[`BANPU_WP3_WORK_PACKAGE_PLAN.md`](BANPU_WP3_WORK_PACKAGE_PLAN.md) §0.4 before
WP3.4 propagation (Step 4.2) may resume. It does not perform a new
implementation review from a blank slate; it independently re-verifies that
current repository state still supports the prior determination, and records
that verification.

This record performs no C4 acceptance, no Implementation Confirmation, no
production or test edit, and no commit, push, deploy, or release. It creates
no implementation authority beyond
[`BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md).

## 2. Scope

Exactly `resolve_successor_bindings(symbols)` in
`backend/services/data_fetcher.py`, against the thirteen constraints frozen in
Plan §0.2. Per Plan §0.4, this review does not reopen accepted pre-accessor
WP3.3 behavior (Checkpoint C3) and does not re-review G1–G4, cache
namespacing, stale-fallback suppression, or PD-4 enforcement — all remain
accepted from Checkpoint C3 and were not re-examined here.

## 3. Thirteen-constraint verification (independently re-checked against current bytes)

| # | Constraint | Verification method | Result |
|---|---|---|---|
| 1 | Creates no persistent state | Full read of the function body: no writes, no DB session use, no module-level mutable state introduced | Confirmed |
| 2 | Performs no memoization and holds no cache | Calls `_read_conversion_guard_projection()` directly on every invocation; no `@cache`/`@lru_cache`, no stored result | Confirmed |
| 3 | Changes no guard-membership semantics | Consumes the same `_read_conversion_guard_projection()` output already used by `_unbound_guard_result`; no independent membership logic | Confirmed |
| 4 | Changes no quarantine policy; adds/removes/reinterprets no quarantine reason | Function constructs no `QuarantineResult`; returns only `dict[str, SuccessorQuoteBinding]` | Confirmed |
| 5 | Changes no `fetch_price_info`/`fetch_history` signature, contract, or return shape | `fetch_price_info(symbol, binding=None)` re-read at lines 948–964: signature and branching (`binding is not None` → bound path; else guarded legacy path) unchanged from the accepted C3 state | Confirmed |
| 6 | Performs no provider lookup | No reference to `_provider` or any network/provider call in the function body | Confirmed |
| 7 | Performs no registry lookup | No registry/lookup-table access; only the guard projection | Confirmed |
| 8 | Reads no environment value and no configuration value | No `os.environ`/config access in the function body | Confirmed |
| 9 | Exposes no boundary evidence | Return value is `{symbol: SuccessorQuoteBinding}` only — no raw provider/network evidence surfaced | Confirmed |
| 10 | Constructs no binding outside accepted WP3.2/WP3.3 machinery | Bindings are taken verbatim from `projection.bindings_by_symbol`, the same WP3.2-canonicalized, WP3.3-guarded projection; no new binding is constructed | Confirmed |
| 11 | Leaves ambiguous and unavailable projection states fail-closed | `if not projection.available: return {}` (unavailable → empty, caller's existing fail-closed unbound path applies); `symbol not in projection.ambiguous_symbols` explicitly excludes ambiguous symbols from the returned bindings | Confirmed |
| 12 | Authorizes no caller other than the single WP3.4 holdings-price call path in `backend/main.py` | Repository-wide grep for `resolve_successor_bindings`: exactly one production call site, `backend/main.py:732` (`get_portfolio_prices`); all other occurrences are the accessor's own definition or test-file references/monkeypatches | Confirmed |
| 13 | Confers on WP3.4 no authority over any other `data_fetcher.py` behavior | Accessor is purely additive (lines 256–280); no other function in the module was altered by its presence | Confirmed |

## 4. Sole-consumer verification

`grep -rn "resolve_successor_bindings" backend --include="*.py"` returns:

- `backend/services/data_fetcher.py:256` — the accessor's own definition.
- `backend/main.py:42` — import.
- `backend/main.py:732` — the sole production call, inside `get_portfolio_prices` (`GET /portfolios/{id}/prices`), the owning holdings-price call path per Plan §3.4 Step 4.2.
- `backend/tests/test_wp34_call_path_propagation.py` — test-only references (a monkeypatch target in one negative-control test, and comments).

No other production module calls the accessor. Constraint 12 and the Plan §0.2
"sole authorized caller" clause are both independently satisfied.

## 5. Regression evidence

Focused suite covering the accessor, the WP3.3 guard it reads, and WP3.4 call-path
behavior, re-run against current working-tree bytes:

```
tests/test_position_conversion_quote_contract.py
tests/test_quote_epoch_isolation.py
tests/test_wp34_call_path_propagation.py

214 passed, 150 warnings in 4.69s
```

No failures. No skips outside the suite's own live-network gates (none present
in this focused set).

## 6. Pre-accessor Checkpoint C3 status

Explicit statement, per Plan §0.4 and §0.5: pre-accessor WP3.3 behavior
(Checkpoint C3) **remains accepted and was not reopened, re-examined, or
re-litigated by this record.** This record's scope is strictly the accessor
delta (§0.2), not the guard machinery it reads.

## 7. Governance identity verification

| Identity | Recomputation method | Result |
|---|---|---|
| Governing planning corpus | Manifest convention (`path\tSHA-256\tbytes\n`, UTF-8) over `BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` (45,667 bytes, `DF4630CFC00A32402B45489D1779F3BBAAD39A86630301256C541BC806481DD7`) and `BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` (21,949 bytes, `48BE744AD91367293FF790772A96FA49D60058CF0221080F538AE6FBEB3BAB01`) | Aggregate `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D` — exact match |
| Amended Work Package Plan | Direct SHA-256 of `BANPU_WP3_WORK_PACKAGE_PLAN.md` (49,541 bytes) | `84E1EC24ACF436AFCC26BFABB4E982692BDB80AAF24B02828356D0F69B23045D` — exact match |

## 8. Repository hygiene

- `git diff --check`: exit `0` (only pre-existing benign LF→CRLF advisory warnings on files unrelated to this record).
- `git diff --cached --check`: exit `0`, no output.
- `git status --porcelain`: unchanged pre-existing dirty/untracked state; no production or test file altered by this record; this record itself is the only new path introduced.

## 9. Disposition

**`BANPU-WP3 BPA-1 ACCESSOR DELTA INDEPENDENTLY ACCEPTED`**

WP3.4 propagation (Step 4.2 onward) remains lawfully resumable under this
acceptance, consistent with the Plan §0.4 gate.

## 10. Outstanding state

**Checkpoint C4 remains incomplete.** This record satisfies only the Plan
§0.4 gate (the focused accessor-delta review). It does not itself constitute
Step 4.1 evidence, does not perform the Step 4.4 boundary audits, and does not
perform C4 review. Do not treat this record as C4 acceptance.

**Exact next act:** materialize Step 4.1 eleven-site evidence.
