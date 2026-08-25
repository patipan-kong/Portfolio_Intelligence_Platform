# BANPU-WP6 — Independent Implementation Review

**Artifact class:** Independent implementation review
**Review date:** 2026-08-18
**Reviewing role:** BANPU-WP6 Independent Implementation Reviewer, distinct from Allocation, Implementation Authorization, WPP authorship/amendment, Planning Confirmation, Planning Freeze, and implementation
**Disposition:** `FAIL — IMPLEMENTATION CORRECTION REQUIRED`
**Release/deployment/production-mutation authority created:** `NONE`
**WP7+ authority created:** `NONE`

## 1. Review result

The exact current BANPU-WP6 implementation candidate is **not ready for
Implementation Confirmation**. The succession helper and horizon translation
are substantially aligned with the frozen plan, and both claimed focused test
counts reproduce, but the shadow implementation does not meet the frozen
persistence-boundary and regenerated-holdings requirements. Its conversion
ratio lookup also does not bind the selected ledger evidence to the resolved
predecessor/successor transition and date, and one pre-existing regression
assertion was removed without authorization.

Canonical disposition:

**`BANPU-WP6 INDEPENDENT IMPLEMENTATION REVIEW — FAILED — IMPLEMENTATION CORRECTION REQUIRED`**

This act changes no implementation, test, planning, governance, Decision Log,
INDEX, staging, release, deployment, or production state. This additive review
artifact is required even on failure by the WP5 Independent Implementation
Review precedent.

## 2. Entry-state verification

| Entry condition | Independent result |
|---|---|
| WP6 Allocation | `PASS` — `BANPU-WP6 ALLOCATED`; 16,307 bytes; SHA-256 `208C2B236D669141BC947A96D82C5C249535E95EB54483C25496C1B6908D9D58` |
| WP6 Implementation Authorization | `PASS` — `BANPU-WP6 IMPLEMENTATION AUTHORIZED`; 18,660 bytes; SHA-256 `442426729C8D7582961CB0BA3B7706356995A39333662042C5BEA260B95BFD0F` |
| Planning Confirmation | `PASS` — `BANPU-WP6 PLANNING CONFIRMED`; 22,056 bytes; SHA-256 `53AC63D13EE81FDC99B443DCFA8478F3F58DE72F7F67FDE9EFE38E3789E7C2FE` |
| Planning Freeze | `PASS` — Freeze Record disposition is `PLANNING FROZEN` and its closing statement says BANPU-WP6 Planning is `PLANNING FROZEN`; 21,785 bytes; SHA-256 `1DE5747F78FD42110506E81A8E620BE2367DA000F6FF6CFB1AB66AA02956FEB9` |
| Frozen WPP identity | `PASS` — live WPP is 53,844 bytes, 725 physical lines, SHA-256 `1CC7F17C916639DAD08507AEF5875EA72A60D028D0573E7CEAFA1B57D766601A`, exactly the Freeze Record identity |
| Implementation candidate state | `PASS WITH DOCUMENTARY NOTE` — the stable seven-path implementation/test diff exists and is unreviewed/unconfirmed/unfrozen at entry. No separate repository implementation-report artifact carrying the exact text `COMPLETE — CANDIDATE FOR REVIEW` was found; the candidate bytes themselves are stable and reviewable |
| Release/deployment/production mutation | `PASS` — no repository evidence of such an act; none was performed by this review |
| WP7+ | `PASS` — no BANPU-WP7 Allocation or Authorization artifact found; no later-package authority exists |
| Staging | `PASS` — `git diff --cached --name-only` empty |
| Candidate stability | `PASS` — seven exact implementation/test paths identified and byte-bound below |

No frozen-planning drift or failed constitutional prerequisite required the
review to stop before source inspection.

## 3. Exact implementation review corpus

The actual current diff independently yields the same seven-path production
and test surface suggested by the submission; no changed implementation/test
path exists outside it.

| Path | Status | Bytes | SHA-256 | Authorization basis |
|---|---:|---:|---|---|
| `backend/services/decision_memory/shadow_tracker.py` | modified | 87,348 | `089342543C7B0C2F7353CAE51F4BE9B685AF33EE2686FC42879072FD22CB8E87` | Authorization §4.1; WP6-C2/C3/C4/C6 |
| `backend/services/evaluation/horizon_grader.py` | modified | 14,638 | `3C09473A9D4FE2359A1B56E539BDDF3D2AF600CD0C2DE7393FC10C9882ADCC7E` | Authorization §4.1; WP6-C1/C5 |
| `backend/services/position_conversion.py` | new | 4,625 | `F9A6F6F2A5E3B89EDB0D393FEA7F3B84A6FED5F0BFDCC6C495435BB7CFA82EF0` | Authorization §4.1 narrow pure helper option; WPP §7.1 |
| `backend/tests/test_horizon_grader.py` | modified | 24,340 | `902DFF05D05FA35ED72341A504478B382DC246F66A978295D631C036DB3E57FE` | Authorization §4.2; WP6-A10/A12/A15 |
| `backend/tests/test_ideal_series.py` | modified | 24,270 | `440EF04D0CBCA49729A4639E91B942E52FA81196FF6797C079C05FEF5BEF8BDA` | Authorization §4.2; WP6-A11 |
| `backend/tests/test_position_conversion.py` | new | 5,734 | `621EA7D91F6416DFE013495D7366F8CF880F9A0B988A6B3734A582471B3986C2` | Authorization §4.2; WP6-A1/A2 |
| `backend/tests/test_shadow_regeneration.py` | modified | 35,787 | `5CEAC14E9FA8934BD94CA48850C97C0EDCAAB8F3963919910A0C007569CDDA7D` | Authorization §4.2; WP6-A3-A8/A13-A15 |

Following the established WP5 method, the deterministic aggregate hashes the
ordered UTF-8 rows `path<TAB>SHA256<TAB>bytes<LF>`:

`66612230CE88D363B335DD718D06CB6E5E1F9B03D7C8687656663ED408B79B14`

These are the exact bytes reviewed. The five additive WP6 lifecycle documents
are authority/evidence, not implementation-candidate members.

## 4. Authorization and diff-scope review

All seven changed paths are within the authorized file surface. The new helper
is narrow and justified by repeated consumers. The production changes are
directed at authorized capabilities rather than a generalized framework.

One hunk is neither necessary support nor authorized evidence: the existing
`test_compute_ideal_series_replay_is_deterministic` assertion
`result["result"]["status"] == "ok"` was deleted from
`test_ideal_series.py`. The replacement WP6 test is additive, but deleting an
unrelated existing assertion weakens the pre-WP6 regression and is an
unauthorized test-evidence change. It must be restored unless a separately
reviewable, in-scope reason proves a different assertion is required.

No schema, migration, public endpoint, CLI, frontend, transaction write path,
WP3/WP4/WP5 closed production surface, M46 surface, Decision Log, or INDEX
file changed.

## 5. WP6-C1 — succession lookup

**Result: `PASS`.** `resolve_identity`:

- resolves only outgoing `MERGED_INTO` rows;
- follows only one hop;
- uses `AssetRelationship.effective_date`, not `created_at`;
- keeps the predecessor before the boundary and resolves the successor on the
  boundary (`>=`) and afterward;
- ignores an edge with `effective_date IS NULL`;
- treats no applicable relationship as a normal predecessor result;
- raises only for an unresolved caller identity;
- performs no write and introduces no generalized corporate-action vocabulary.

The focused tests cover before, exactly at, and after the boundary, symbol and
asset-ID inputs, no relationship, null effective date, unknown identities, and
single-hop behavior. The registry's existing single-outgoing-edge invariant
makes iteration order immaterial for currently valid state.

## 6. WP6-C2/C3/C4/C6 — shadow mechanics

**Result: `FAIL — IMPLEMENTATION CORRECTION REQUIRED`.** Correct portions:

- `_carry_succession_identity` evaluates each entry for the supplied row date;
- it adds a registry-resolved asset ID for registered holdings;
- the valid-fixture path uses Decimal ratio arithmetic, preserves fractional
  shares, divides inception price by the ratio, and introduces no cash-in-lieu;
- callers begin from raw/replayed holdings rather than recursively multiplying
  a converted output in the main tested paths;
- active-model persistence uses date-keyed upsert behavior.

Blocking defects:

1. `_rebuild_shadow_snapshots` computes `priced_holdings` but discards the
   enriched result. New rows are written with `holdings_json=None`, and existing
   rows do not have `holdings_json` updated. Static regeneration therefore does
   not persist the required predecessor/successor asset identity, converted
   shares, inception price, price, or market value per row. This directly fails
   WP6-C2/C3 and A3/A4/A11 for the principal static-regeneration path.
2. `_rebuild_shadow_snapshots` iterates and assigns fields on every existing
   row from inception. It has no boundary predicate that skips persistence for
   dates before the conversion. Equal recomputed numeric values are not the
   frozen requirement: WPP §7.2 and §8 #8 require writes only on/after the
   boundary and pre-boundary persisted rows unchanged. This fails WP6-C6/A13.
3. The A13 test merely compares pre-boundary `total_value` after two runs. It
   does not seed a sentinel persisted row and prove its complete fields and
   write boundary remain untouched. It therefore passes the defective code.
4. The A14 test compares only date keys and `total_value`; it does not compare
   the required persisted business fields (shares, prices, asset ID, symbol,
   market value), nor does it independently prove absence of orphan rows.
5. In the live active-model rebalance path, `create_active_model_shadow`
   calculates `running_nav` from `old_holdings` before applying succession
   translation for the current date. A boundary-crossing holding can therefore
   be valued under the stale predecessor identity immediately before the
   rebalance. The subsequent translation of only `new_holdings` does not repair
   that NAV basis.

## 7. Conversion-ratio provenance

**Result: `FAIL — UNDER-BOUNDED CANONICAL-EVIDENCE SELECTION`.** Reading the
ratio from the portfolio's append-only `POSITION_CONVERSION`
`Transaction.conversion_payload` is mechanically consistent with the frozen
design's canonical typed payload and WPP §7.2. The source class itself is
authorized and preferable to re-deriving a ratio.

The production selector is not sufficient. `_conversion_ratio` filters only by
`portfolio_id`, predecessor `Transaction.symbol`, and transaction type, orders
ascending, and takes the first row. It does not bind the row to:

- the predecessor asset ID resolved by the relationship;
- the resolved successor asset ID;
- the relationship effective date or the row's valuation-transition date;
- the particular conversion applicable to the requested `as_of_date`.

Thus multiple same-symbol conversions, historical reuse, or an unrelated or
malformed first row can select the wrong evidence. More seriously, absent or
malformed payload returns `None` after identity has already switched to the
successor; shares and inception price are silently left unconverted. That is
not the required exact conversion and can break NAV continuity. No test covers
wrong successor, wrong date, multiple candidate rows, absent payload, malformed
payload, or a mismatch between relationship and payload identities.

The smallest compliant correction is to select and validate the canonical row
against the resolved predecessor ID, successor ID, and applicable transition
date, and to fail closed for a relationship that requires quantity conversion
but lacks one unambiguous valid payload. Ordinary assets with no applicable
relationship must continue to fail open to unchanged behavior.

## 8. WP6-C5 — evaluation continuity

**Result: `PASS`.** The pre-WP6 defect exists: inception holdings are keyed by
the immutable predecessor symbol while a post-boundary horizon snapshot is
keyed by the successor, causing an exact-string lookup miss and silent
exclusion. The optional `symbol_translation` map changes only the lookup key.
The historical holding remains unchanged, unrelated symbols retain the old
path, and callers omitting the parameter remain backward compatible. Resolving
the translation at the DB-owning caller preserves `score_directional_calls` as
a pure function and is the smallest compliant implementation.

## 9. Confirm-or-implement consumers

| Consumer | Result | Exact evidence |
|---|---|---|
| `attribution.py` | `CONFIRMED — NO CHANGE REQUIRED` | `compute_attribution` derives portfolio return from aggregate shadow snapshot `total_value`; `_portfolio_sector_return` is a stub and no operative symbol-keyed join exists |
| `quant_engine.py` | `CONFIRMED — NO CHANGE REQUIRED` | `calculate_buy_win_rate` and `calculate_sell_accuracy` classify aggregate snapshot-value changes; `sig.symbol` is display-only in details |
| `ideal_series.py` | `IMPLEMENTATION GAP` | its join correctly consumes the per-row shadow symbol and portfolio-snapshot price history, but the claimed common transition schedule is not enforced: shadow transition uses `AssetRelationship.effective_date`, while the real portfolio conversion and snapshots transition from payload `valuation_transition_date`/`Transaction.transaction_date`. Registry preparation accepts an independently supplied effective date, and the live conversion validator does not prove those dates equal. The new test manually switches both fixtures on the same day and does not exercise or prove the production invariant |

## 10. WPP factual-citation finding

**Classification: `NON-BLOCKING DOCUMENTARY INACCURACY`.** The frozen WPP
states that `regenerate_static_shadow` performs a bulk `.delete()`. Against the
source identity planning reviewed, the bulk delete is actually in
`reset_active_model_inception`. `regenerate_static_shadow` calls
`_rebuild_shadow_snapshots`, which uses date-keyed upsert behavior and does not
bulk-delete rows.

The mistaken citation does not alter the normative Contract-B requirement,
the on/after-boundary write restriction, or the acceptance matrix. The
candidate did not implement a delete/recreate strategy based on the mistaken
premise. Planning Confirmation and Freeze remain materially valid. Record this
documentary inaccuracy at later governance/closeout without reopening or
amending the frozen WPP during this review.

## 11. Test-fixture imports

The added `import models.asset` statements in the authorized SQLite test
fixtures are **necessary fixture/table-registration support**. They register
the asset tables on shared `Base.metadata` before `create_all`. They neither
manipulate production behavior nor weaken assertions. The separate deletion of
the ideal-series status assertion is not part of this fixture support and is
classified independently in §4.

## 12. Independent WP6-A1 through WP6-A18 matrix

| ID | Requirement | Evidence inspected | Reviewer result |
|---|---|---|---|
| A1 | predecessor before, successor at/after boundary | helper source and boundary tests | `PASS` |
| A2 | null effective date never resolves successor | helper source and null-date test | `PASS` |
| A3 | identity continuity in holdings JSON | value-today/active paths; static rebuild discards enriched holdings | `FAIL` |
| A4 | non-null asset ID on affected entries | direct valuation passes; static regenerated rows remain null/stale | `FAIL` |
| A5 | same schedule as real portfolio | relationship date and transaction/payload date are independently supplied and not equality-validated | `FAIL` |
| A6 | exact fractional ratio, no whole-share rounding | valid path works; ambiguous/missing ratio silently leaves quantities unchanged | `FAIL` |
| A7 | no broker cash-in-lieu in shadows | no CIL field is read or applied | `PASS` |
| A8 | inception/NAV continuity | valid fixture passes; missing/wrong ratio and stale active rebalance NAV can violate it | `FAIL` |
| A9 | attribution continuity | operative attribution uses aggregate snapshot values; no symbol join | `PASS` |
| A10 | converted directional call remains evaluable | source defect reproduced and end-to-end translation test passes | `PASS` |
| A11 | post-boundary valuation-subject normalization | static persistence missing; common schedule unproven | `FAIL` |
| A12 | immutable historical recommendation/decision evidence | source rows are read only; test verifies frozen inception symbol | `PASS` |
| A13 | no pre-boundary persisted write | no write guard; test checks value equality only | `FAIL` |
| A14 | Contract-B rerun convergence | source supports date upsert, but required full business-field/orphan evidence is absent | `INSUFFICIENT EVIDENCE` |
| A15 | unrelated symbol unchanged | fail-open source path and regression tests | `PASS` |
| A16 | no generalized framework | narrow helper and bounded call sites only | `PASS` |
| A17 | no forbidden schema/write-path surface | repository diff inspection | `PASS` |
| A18 | no M46 modification | repository diff inspection | `PASS` |

Required criteria A3, A4, A5, A6, A8, A11, and A13 fail; A14 lacks the
required evidence. Each is a review blocker.

## 13. Executed tests

### 13.1 WP6-focused

Command:

```text
python -m pytest -q tests/test_position_conversion.py tests/test_shadow_regeneration.py tests/test_horizon_grader.py tests/test_ideal_series.py
```

Result: **66 passed, 0 failed, 0 skipped, 0 errors** (579 warnings; 8.51 s).
The claimed 66/66 count reproduces exactly.

### 13.2 Frozen-WPP neighboring regression suites

Command:

```text
python -m pytest -q tests/test_portfolio_metrics.py tests/test_portfolio_rebuilder.py tests/test_verify_snapshots.py tests/test_asset_registry.py tests/test_position_conversion_live.py tests/test_transaction_canonicalizer.py tests/test_position_conversion_quote_contract.py
```

Result: **505 passed, 0 failed, 0 skipped, 0 errors** (1,242 warnings; 7.53 s).
The claimed 505/505 count reproduces exactly.

Passing fixtures do not override the source-level acceptance failures above.

## 14. Broad-suite baseline comparison

A raw broad collection reproduced a Windows access violation while importing
`tests/test_pandas.py`. Source inspection confirms `test_pandas.py`,
`test_dr.py`, and `test_yf.py` are import-time debug scripts rather than test
suites; the latter two also execute/patch yfinance at import. Separately,
`test_snapshot_repair.py` reproducibly reaches 19 passing tests and then
crashes in pandas datetime normalization. It is therefore a fourth crash-prone
file, but not one of the three debug scripts.

For a deterministic comparison, both candidate and an immutable `git archive
HEAD` baseline were run with `tests/investigate` and those four crash-prone
files excluded:

| Corpus | Passed | Failed | Skipped | Errors |
|---|---:|---:|---:|---:|
| Current WP6 candidate | 2,893 | 62 | 32 | 3 |
| Pre-WP6 `HEAD` archive | 2,875 | 62 | 32 | 3 |

JUnit testcase identity comparison found 65 bad identities in each corpus,
zero candidate-only bad identities, and zero baseline-only bad identities.
Therefore WP6 introduces **zero new broad-suite failures/errors** and adds 18
passing tests in this collection. The submitted claim of **53 failures** is not
reproducible against the exact current repository and is a reporting/count
error, not a new WP6 regression.

The baseline was created by `git archive` in a temporary directory; the live
candidate was never stashed, checked out, or overwritten.

## 15. Findings and severity

| ID | Severity | Finding | Required disposition |
|---|---|---|---|
| WP6-IIR-B1 | Blocking defect | Static regeneration discards enriched per-row holdings and does not persist conversion identity/quantity evidence | Correct `_rebuild_shadow_snapshots` within the existing authorized surface and add direct persisted-JSON tests |
| WP6-IIR-B2 | Blocking defect | Pre-boundary rows are still assigned/upserted; no on/after-boundary write guard exists | Add the frozen per-boundary persistence guard and prove complete pre-boundary rows untouched |
| WP6-IIR-B3 | Blocking defect | Ratio row selection is not transition-bound and absence/malformed evidence silently produces successor identity with predecessor quantity | Bind lookup to predecessor, successor, transition date, and applicable row; fail closed for an applicable but unprovable conversion |
| WP6-IIR-B4 | Blocking defect | Relationship effective date and canonical transaction transition date are not proven equal, so real/shadow schedules can diverge | Reuse or validate one canonical transition schedule and test mismatch rejection/handling |
| WP6-IIR-B5 | Blocking defect | Active-model rebalance values old holdings before current-date succession conversion | Translate the pre-rebalance valuation subject before calculating running NAV |
| WP6-IIR-B6 | Implementation correction required | A pre-existing ideal-series deterministic-replay status assertion was removed | Restore it or replace it only with demonstrably equivalent/stronger in-scope evidence |
| WP6-IIR-B7 | Implementation correction required | A14 test compares only dates and total value, not all required business fields/orphans | Add full Contract-B persisted-state comparison |
| WP6-IIR-O1 | Non-blocking documentary issue | WPP attributes bulk delete to the wrong function | Carry to later governance/closeout; do not reopen planning now |
| WP6-IIR-O2 | Pre-existing unrelated failures | Broad suite has identical 62 failures + 3 errors on candidate and HEAD baseline | No WP6 correction; retain as baseline evidence |
| WP6-IIR-O3 | Non-blocking reporting issue | “53 failures” is not reproducible | Correct future implementation/re-review reporting to actual counts |

All blocking corrections fit the already-authorized WP6 production/test file
surface. No planning amendment or authority expansion is required if the
correction remains bounded as stated.

## 16. Post-review verification

At review completion:

- the seven implementation/test member hashes and aggregate remain exactly as
  recorded in §3;
- Allocation, Authorization, WPP, Planning Confirmation, and Planning Freeze
  identities remain exactly as recorded in §2;
- no implementation or test file was modified by this review;
- the only review-created repository path is this additive artifact;
- `git diff --check` and `git diff --cached --check` are required to remain
  clean in the final verification;
- the staged path count is required to remain zero;
- no release, deployment, production mutation, confirmation, freeze, closeout,
  residual discharge, or WP7+ act occurred.

## 17. Resulting constitutional state and next act

Resulting state:

- BANPU-WP6 remains `ALLOCATED`;
- BANPU-WP6 remains `IMPLEMENTATION AUTHORIZED` within its bounded surface;
- BANPU-WP6 Planning remains `PLANNING CONFIRMED` and `PLANNING FROZEN` at the
  exact WPP identity above;
- the current implementation candidate has been independently reviewed and
  **failed**;
- BANPU-WP6 Implementation Confirmation, Implementation Freeze, closeout,
  release/deployment, and WP7+ remain unperformed/unauthorized.

The exact next constitutional act is a bounded **BANPU-WP6 implementation
correction** addressing WP6-IIR-B1 through B7 within the existing frozen WPP
and Authorization, followed by a fresh independent implementation re-review.
This review performs neither act.
