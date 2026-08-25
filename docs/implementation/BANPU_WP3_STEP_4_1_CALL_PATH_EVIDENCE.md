# BANPU-WP3.4 — Step 4.1 Call-Path Evidence Record

**Artifact class:** Additive constitutional evidence record
**Recorded date:** 2026-08-11
**Recorder role:** BANPU-WP3.4 Step 4.1 Evidence Recorder
**Governing planning corpus identity:** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Amended Work Package Plan identity:** `84E1EC24ACF436AFCC26BFABB4E982692BDB80AAF24B02828356D0F69B23045D`
**Disposition:** `BANPU-WP3.4 STEP 4.1 CALL-PATH EVIDENCE RECORDED`

## 1. Nature of this record

This artifact materializes, as a durable repository record, the Step 4.1
exhaustive `fetch_price_info(...)` call-path evidence already established over
current repository bytes. It does not perform new implementation, does not
perform C4 acceptance, and does not perform Implementation Confirmation. It
creates no implementation authority beyond
[`BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md).
No production or test file was modified to produce this record.

## 2. Relationship to the focused C3 accessor-delta acceptance record

[`BANPU_WP3_BPA1_C3_ACCESSOR_DELTA_ACCEPTANCE.md`](BANPU_WP3_BPA1_C3_ACCESSOR_DELTA_ACCEPTANCE.md)
records independent acceptance of the BPA-1 accessor
(`resolve_successor_bindings(symbols)`) against its thirteen constraints and
confirms it is lawfully resumable. That record was independently re-verified
unchanged before this one was created: current bytes hash to
`D35B2AE7363CE8FC1A78D8C4213B45050ECD52563C925F1703B0D4E4DCED0167`
(7,975 bytes), matching the file as written. This record depends on that
acceptance (WP3.4 propagation, Step 4.2, presupposes it) but performs a
distinct verification: exhaustive coverage of every `fetch_price_info` call
site, not just the accessor itself.

## 3. Fresh enumeration method and result

`grep -rn "fetch_price_info" backend --include="*.py"`, filtered to exclude
the definition (`data_fetcher.py:948`), its internal helpers
(`_fetch_price_info_bound`, `_fetch_price_info_legacy`), imports, comments,
docstrings, and all `backend/tests/*.py` files. The pattern was checked
against both direct-call and callable-passing forms (`asyncio.to_thread(
fetch_price_info, ...)`), since a naive `fetch_price_info\(` search misses
the latter.

**Result: exactly 11 production call sites.** This matches the previously
accepted Step 4.1 conceptual register exactly — no site added, removed, or
reclassified.

## 4. Exhaustive eleven-site register

| # | File:Line | Function | Endpoint/purpose | Owns identity? | Bound? |
|---|---|---|---|---|---|
| 1 | `main.py:736` | `get_portfolio_prices` | `GET /portfolios/{id}/prices` — holdings price | **Yes** | **Bound** |
| 2 | `main.py:759` | `get_portfolio_prices` | DR-parent price for upside_pct | No | Unbound |
| 3 | `main.py:883` | `add_holding` | `POST /portfolios/{id}/holdings` | No | Unbound |
| 4 | `main.py:1047` | `list_watchlist` | `GET /watchlist` — primary price | No | Unbound |
| 5 | `main.py:1052` | `list_watchlist` | DR-parent price | No | Unbound |
| 6 | `main.py:2038` | `analyze_optimizer` (`_get_scores` closure) | `POST /analyze/optimizer` — candidate price | No | Unbound |
| 7 | `main.py:2045` | `analyze_optimizer` (`_get_scores` closure) | DR-parent price | No | Unbound |
| 8 | `main.py:4712` | `admin_validate_portfolio` | `GET /admin/validate-portfolio/{id}` | No | Unbound |
| 9 | `portfolio_snapshots.py:333` | `generate_daily_snapshot` | Scheduler/admin snapshot engine | No | Unbound |
| 10 | `idea_review.py:396` | `review_ideas` | AI Committee Review market-value loop | No | Unbound |
| 11 | `factor_engine.py:797` | `compute_portfolio_factor_exposure` | Portfolio DNA factor exposure | No | Unbound |

Function boundaries independently confirmed via `grep "^(async )?def "` over
`main.py`: `get_portfolio_prices` spans lines 712–781, `add_holding` 873–922,
`list_watchlist` 1022–1089, `analyze_optimizer` 1970–2618,
`admin_validate_portfolio` 4690–4826 — each call site's line number falls
inside its stated owning function. Line numbers are read fresh from current
bytes, not carried over from the Plan's own (self-declared stale) citations.

## 5. Per-site ownership and bound/unbound classification

Only site 1 (`main.py:736`, inside `get_portfolio_prices`) supplies a binding
argument to `fetch_price_info`, sourced exclusively from
`resolve_successor_bindings(symbols)` (line 732) — the accessor accepted in
§0.4/BPA-1. `get_portfolio_prices` is the sole call site that owns portfolio
holding identity per Plan §3.4 Step 4.2 and Plan §0.2's "sole authorized
caller" clause.

All ten remaining sites call `fetch_price_info(symbol)` with no second
argument, so `binding` defaults to `None` and the call falls into the
`_unbound_guard_result(symbol)` branch (`data_fetcher.py:961-964`) —
confirmed by direct re-read of `fetch_price_info`'s current body, unchanged
from the accepted Checkpoint C3 state.

## 6. Per-site behavioral evidence / test mapping

| # | Site | Test(s) | Assertion proves |
|---|---|---|---|
| 1 | `main.py:736` (bound) | `test_owning_call_site_propagates_binding_and_serves_converted_successor_quote`, `test_owning_call_site_without_propagation_fails_closed`, `test_owning_call_site_preserves_legacy_behavior_for_unconverted_holding`, `test_owning_call_site_handles_mixed_converted_and_unconverted_holdings_independently` | Converted successor served via bound path; counterfactual without propagation fails closed; unconverted holding legacy-quotes unchanged; mixed converted/unconverted handled independently in one call |
| 2 | `main.py:759` (DR-parent) | `test_owning_call_site_dr_parent_price_remains_unbound` | Parent-ticker lookup receives no binding even at the owning endpoint; `upside_pct is None` for a guard-bound parent, zero evidence calls, one legacy quote call |
| 3 | `main.py:883` | `test_non_owning_call_site_add_holding_refuses_converted_symbol` | Direct `add_holding` call refuses a converted symbol (`current_price is None`), zero provider calls |
| 4 | `main.py:1047` | `test_non_owning_call_site_watchlist_refuses_converted_symbol` | Watchlist primary price refuses a converted symbol, zero provider calls |
| 5 | `main.py:1052` | `test_non_owning_call_site_watchlist_dr_parent_remains_unbound` | Watchlist DR-parent price unbound, refused, zero evidence calls |
| 6, 7 | `main.py:2038`, `2045` | `test_non_owning_call_site_optimizer_scoring_refuses_converted_symbol` | Spy on the module-level `fetch_price_info` binding proves both the candidate's own price (2038) and its DR-parent price (2045) are called with `binding is None` and refused; `run_layered_optimizer` stubbed to prevent live AI calls |
| 8 | `main.py:4712` | `test_non_owning_call_site_admin_validate_portfolio_refuses_converted_symbol` | Diagnostic endpoint refuses converted symbol, `nav_reconciliation.status == "no_snapshot"`, zero provider calls |
| 9 | `portfolio_snapshots.py:333` | `test_non_owning_call_site_snapshot_generation_refuses_converted_symbol` | `SnapshotCoverageError` raised (0% live-price coverage from the single refused holding), zero provider calls |
| 10 | `idea_review.py:396` | `test_non_owning_call_site_idea_review_refuses_converted_symbol` | `review_ideas` completes with the converted portfolio holding refused, zero provider calls |
| 11 | `factor_engine.py:797` | `test_non_owning_call_site_factor_engine_refuses_converted_symbol` | Factor exposure computed with the converted holding refused, `per_stock_scores[0].symbol == "SUCC.BK"`, zero provider calls |

All 13 tests inspected in `backend/tests/test_wp34_call_path_propagation.py`
were confirmed present and unmodified from the previously reported evidence;
no new test was added by this act.

## 7. Sole-consumer verification for `resolve_successor_bindings`

`grep -rn "resolve_successor_bindings" backend --include="*.py"` returns
exactly: the definition (`data_fetcher.py:256`), one import
(`main.py:42`), one production call (`main.py:732`, inside
`get_portfolio_prices`), and test-only references (a monkeypatch target and
comments in `test_wp34_call_path_propagation.py`). No other production module
calls the accessor — `get_portfolio_prices` remains the sole consumer.

## 8. Provider-call suppression evidence for unbound converted identities

For every one of the ten unbound sites, the corresponding test asserts the
fake provider's `evidence_calls == 0` (or, where applicable, an equivalent
zero-network-call condition — e.g. `SnapshotCoverageError` raised before any
snapshot is persisted). Refusal is produced entirely by the WP3.3 guard
(`_unbound_guard_result` → `_guard_result_from_projection`) before
`_fetch_price_info_legacy` — and therefore the provider, any stale-cache
fallback, or any alternate-provider retry — is ever reached. This was
re-confirmed by direct re-read of `fetch_price_info`
(`data_fetcher.py:948-964`): the `guard_result is not None` branch returns
`_quote_quarantine_response(...)` and returns before `_fetch_price_info_legacy`
is called.

## 9. Optimizer live-AI isolation statement

`test_non_owning_call_site_optimizer_scoring_refuses_converted_symbol`
(covering sites 6 and 7) contains
`monkeypatch.setattr(main, "run_layered_optimizer", lambda *a, **k: {})`,
confirmed present at line 501 of the current test file. This stub prevents
`agents.optimizer.run_layered_optimizer` — a real network call to a live LLM
provider — from ever executing inside this test, regardless of what
downstream exception handling would otherwise contain. The full focused
Step 4.1 suite was re-run and produced no live-model output (no
`stop_reason`/`claude-sonnet` debug output), consistent with the stub holding.

## 10. Focused regression results

```
tests/test_wp34_call_path_propagation.py -v
13 passed, 90 warnings in 3.94s

tests/test_position_conversion_quote_contract.py
tests/test_quote_epoch_isolation.py
tests/test_wp34_call_path_propagation.py
214 passed, 98 warnings in 3.39s
```

No failures. Step 4.1 evidence rests on unchanged WP3.2 (conversion contract)
and WP3.3 (quote epoch isolation / guard) behavior, re-confirmed green
alongside this evidence in the same run.

## 11. Explicit completeness statement

**Step 4.1 is complete.** All eleven production `fetch_price_info` call
sites are freshly enumerated, individually classified, and individually
proven — the sole bound holdings-price path (site 1) and all ten deliberately
unbound sites (2–11) each have durable, per-site behavioral test evidence,
not a single representative example.

## 12. Explicit non-performance statement

**Checkpoint C4 is NOT performed by this act.** This record materializes
Step 4.1 evidence only. It does not perform the Step 4.4 boundary audits
(WP1/WP2 aggregate re-verification, M46-unchanged check, WP2 deferral guard
green check, diff ⊆ authorized surface `A`), does not perform C4 review, and
does not perform Implementation Confirmation.

## 13. Governance identity

| Identity | Recomputation | Result |
|---|---|---|
| Governing planning corpus (aggregate manifest) | `DF4630CFC00A32402B45489D1779F3BBAAD39A86630301256C541BC806481DD7` (Architecture & Implementation Plan) + `48BE744AD91367293FF790772A96FA49D60058CF0221080F538AE6FBEB3BAB01` (Decomposition & Roadmap) | Aggregate `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D` — exact match |
| Amended Work Package Plan | Direct SHA-256, 49,541 bytes | `84E1EC24ACF436AFCC26BFABB4E982692BDB80AAF24B02828356D0F69B23045D` — exact match |
| C3 accessor-delta acceptance record | Direct SHA-256, 7,975 bytes | `D35B2AE7363CE8FC1A78D8C4213B45050ECD52563C925F1703B0D4E4DCED0167` — unchanged since creation |

## 14. Repository hygiene

- `git diff --check`: exit `0` (only pre-existing benign LF→CRLF advisory warnings, unrelated to this record).
- `git diff --cached --check`: exit `0`, no output.
- `git status --porcelain`: unchanged pre-existing dirty/untracked state; this record and the prior C3 acceptance record are the only new paths; no production or test file altered.

## 15. Disposition

**`BANPU-WP3.4 STEP 4.1 CALL-PATH EVIDENCE RECORDED`**

## 16. Exact next act

Independent Checkpoint C4 Re-review. This record does not perform that act.
