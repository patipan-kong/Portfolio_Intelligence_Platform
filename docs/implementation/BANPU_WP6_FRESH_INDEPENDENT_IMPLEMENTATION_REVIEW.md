# BANPU-WP6 — Fresh Independent Implementation Re-Review

**Artifact class:** Additive fresh independent implementation re-review record  
**Review date:** 2026-08-18  
**Review boundary:** `FRESH INDEPENDENT IMPLEMENTATION RE-REVIEW ONLY`  
**Historical predecessor:** [`BANPU_WP6_INDEPENDENT_IMPLEMENTATION_REVIEW.md`](BANPU_WP6_INDEPENDENT_IMPLEMENTATION_REVIEW.md), SHA-256 `6B10B314C5CA8D0AA315B00CD7AA082AADF39EC68EC83266EA5F3518A7A30D32`  
**Disposition:** `BANPU-WP6 INDEPENDENT IMPLEMENTATION RE-REVIEW FAILED`  
**Implementation confirmation/freeze/closeout performed:** `NO`  
**Release/deployment/production mutation performed or authorized:** `NO`

## 1. Independent method and constitutional entry state

This act independently queried the repository knowledge graph, read the live
authority/planning/review bytes and current implementation/tests, inspected the
complete diff, ran the focused and neighboring suites, compared normalized
broad-suite failure identities against an immutable `git archive HEAD`
baseline, and reproduced the decisive defect against an in-memory SQLite
database. The correction report and its claimed outcomes were not treated as
proof. No implementation, test, planning, governance, Decision Log, INDEX,
staging, release/deployment, or production-data state was modified. This file
is the only additive repository artifact created by the re-review.

| Entry premise | Independent result |
|---|---|
| Allocation | `PASS` — `BANPU-WP6 ALLOCATED`; 16,307 bytes; `208C2B236D669141BC947A96D82C5C249535E95EB54483C25496C1B6908D9D58` |
| Implementation Authorization | `PASS` — `BANPU-WP6 IMPLEMENTATION AUTHORIZED`; 18,660 bytes; `442426729C8D7582961CB0BA3B7706356995A39333662042C5BEA260B95BFD0F` |
| Frozen WPP | `PASS` — 53,844 bytes; 725 lines; `1CC7F17C916639DAD08507AEF5875EA72A60D028D0573E7CEAFA1B57D766601A`, exact Freeze identity |
| Planning Confirmation | `PASS` — `BANPU-WP6 PLANNING CONFIRMED`; 22,056 bytes; `53AC63D13EE81FDC99B443DCFA8478F3F58DE72F7F67FDE9EFE38E3789E7C2FE` |
| Planning Freeze | `PASS` — `PLANNING FROZEN`; 21,785 bytes; `1DE5747F78FD42110506E81A8E620BE2367DA000F6FF6CFB1AB66AA02956FEB9` |
| Failed Independent Review | `PASS` — unchanged live bytes; 22,726 bytes; `6B10B314C5CA8D0AA315B00CD7AA082AADF39EC68EC83266EA5F3518A7A30D32`; canonical failed disposition remains present |
| Corrected candidate | `PASS` — seven-member candidate exists and had no later independent re-review artifact at entry |
| Confirmation / Freeze / closeout | `PASS` — no BANPU-WP6 Implementation Confirmation, Implementation Freeze, closeout, release, or deployment artifact exists |
| WP7+ | `PASS` — no BANPU-WP7 Allocation or Authorization artifact exists |
| Git index | `PASS` — nothing staged |

No entry premise failed. The re-review therefore proceeded.

## 2. Corrected candidate identity

The implementation/test diff independently yields exactly seven members. The
aggregate uses the established UTF-8 manifest rows
`path<TAB>lowercase-SHA256<TAB>bytes<LF>` in the order below.

| Path | Status | Bytes | SHA-256 | Authorization basis |
|---|---:|---:|---|---|
| `backend/services/decision_memory/shadow_tracker.py` | modified | 95,108 | `EC1E55F3C53F004E5C57D10514CB1462A4A6539869830B2CB61B06A1E7313087` | Authorization §4.1; WP6-C2/C3/C4/C6 |
| `backend/services/evaluation/horizon_grader.py` | modified | 14,638 | `3C09473A9D4FE2359A1B56E539BDDF3D2AF600CD0C2DE7393FC10C9882ADCC7E` | Authorization §4.1; WP6-C1/C5 |
| `backend/services/position_conversion.py` | new | 7,413 | `BFE1BE7A6620FCAD12C87D42DF3101051185E76B6C97FE637225B3DD8536BA94` | Authorization §4.1 narrow helper; WPP §7.1 |
| `backend/tests/test_horizon_grader.py` | modified | 24,340 | `902DFF05D05FA35ED72341A504478B382DC246F66A978295D631C036DB3E57FE` | Authorization §4.2; A10/A12/A15 |
| `backend/tests/test_ideal_series.py` | modified | 24,270 | `440EF04D0CBCA49729A4639E91B942E52FA81196FF6797C079C05FEF5BEF8BDA` | Authorization §4.2; A11 |
| `backend/tests/test_position_conversion.py` | new | 5,734 | `621EA7D91F6416DFE013495D7366F8CF880F9A0B988A6B3734A582471B3986C2` | Authorization §4.2; A1/A2 |
| `backend/tests/test_shadow_regeneration.py` | modified | 53,848 | `DB78241A40641CA7A89C38D7C7FAD230A0F7A87FEC8C2C41FF7A8454C3A995C7` | Authorization §4.2; A3-A8/A13-A15 |

Aggregate identity:

`32714BFCC9EB1F6820BF3E2757AE75F6A864494C148B06FD514D819F796372FD`

This exactly matches the submitted corrected identity. The prior failed
aggregate `66612230CE88D363B335DD718D06CB6E5E1F9B03D7C8687656663ED408B79B14`
remains historical evidence only.

## 3. Failed-review finding register and correction verification

The complete predecessor review contains exactly B1-B7 and O1-O3; no omitted
correction-required finding was found.

| ID | Original failed-review evidence | Corrected location/evidence | Independent result |
|---|---|---|---|
| B1 | `_rebuild_shadow_snapshots` discarded enriched holdings; inserts wrote null and updates left stale JSON | `shadow_tracker.py:1440-1485`; persisted insert/update and rerun tests | `RESOLVED` |
| B2 | no pre-boundary persistence guard | static guard at `shadow_tracker.py:1404-1438`; active writer at `2030-2067` still has none; direct sentinel reproduction below | `NOT RESOLVED` |
| B3 | ratio evidence was not predecessor/successor/transition bound; malformed/absent evidence could mix successor identity with predecessor quantity | `_conversion_ratio`, `shadow_tracker.py:514-575`; mismatch/zero/duplicate/malformed/history tests | `RESOLVED` |
| B4 | relationship effective date and payload transition date were not proven equal | exact `valuation_transition_date == effective_date` match at `shadow_tracker.py:566-570`; mismatch test | `RESOLVED` |
| B5 | active rebalance valued old holdings before succession translation | `create_active_model_shadow`, `shadow_tracker.py:1087-1101`; focused persisted fixture | `RESOLVED` |
| B6 | pre-existing deterministic ideal-series status assertion was deleted | restored exactly at `test_shadow_regeneration.py:528`, in its original test and semantic position | `RESOLVED — REGRESSION EVIDENCE RESTORED` |
| B7 | A14 compared only dates/total value and did not prove business-state convergence/orphans | strengthened static test at `test_shadow_regeneration.py:813-888`; active rerun test at `399-421` remains value/date-only and does not prove full active persisted state | `NOT FULLY RESOLVED — INSUFFICIENT ACTIVE-MODEL EVIDENCE` |
| O1 | WPP misattributes a bulk `.delete()` to `regenerate_static_shadow` | source fact remains unchanged | `NON-BLOCKING DOCUMENTARY INACCURACY — CARRIED FORWARD` |
| O2 | broad-suite failures/errors pre-exist WP6 | normalized candidate/baseline bad sets are identical (65/65) | `PRE-EXISTING — ZERO WP6 BAD-IDENTITY DELTA` |
| O3 | reported “53 failures” was not reproducible | current candidate and baseline each have 62 failures + 3 errors | `NON-BLOCKING REPORTING OBSERVATION — CARRIED FORWARD` |

## 4. B1 — persisted holdings JSON

**Result: `RESOLVED`.** `_rebuild_shadow_snapshots` serializes the enriched,
date-specific holdings and assigns it on both existing-row update and new-row
insert. The static persisted-row tests independently reload boundary and
post-boundary rows and prove successor asset ID/symbol, exact fractional
shares, inception/current prices, and market value. The sentinel test proves
the static pre-boundary update path does not execute. Active-model update and
insert paths also serialize the replay row's enriched holdings.

## 5. B2 — persistence boundary

**Result: `NOT RESOLVED` — BLOCKER.** The static `_rebuild_shadow_snapshots`
path correctly derives the earliest relevant relationship boundary, continues
LOCF price replay in memory, and skips every insert/update before that date.
No relationship yields no restriction. For a multi-holding snapshot, earliest
is the coherent row-write boundary: the first converting holding makes that
atomic snapshot row eligible for regeneration, while every other holding is
still resolved independently for the row date and stays predecessor-bound
until its own later boundary. A later/global boundary would incorrectly
suppress the first holding's required rows.

However, frozen WPP §7.2 lines 376-387 expressly names
`regenerate_active_model_shadow` as a regeneration writer that must gain the
same pre-boundary guard. Its live loop writes every replay row, including
pre-boundary rows. An independent in-memory reproduction created an active
shadow with a boundary on 2026-08-17 and a deliberately wrong sentinel row on
2026-08-16. Regeneration returned `status=regenerated`, wrote three rows, and
changed the protected sentinel's `total_value` from `999999.0` to `1000000.0`
and its `holdings_json` from `SENTINEL_UNTOUCHED` to reconstructed predecessor
holdings. `sentinel_preserved=false`.

This is a direct WPP §7.2 / WP6-C6 / A13 violation.

## 6. B3/B4 — conversion-ratio provenance

**Result: `RESOLVED`.** The selector is limited to the relevant portfolio and
`POSITION_CONVERSION`, parses canonical typed payloads, and accepts exactly one
row whose predecessor asset ID, successor asset ID, and
`valuation_transition_date` equal the resolved relationship triple. Zero,
duplicate, malformed, predecessor/successor mismatch, unrelated conversion,
date mismatch, and repeated-history cases fail closed. `_carry_succession_identity`
keeps the predecessor symbol/asset ID and unconverted quantity when the ratio
cannot be uniquely bound, preventing mixed identity/quantity state.

## 7. B5 — active-model NAV

**Result: `RESOLVED`.** `create_active_model_shadow` now translates
`old_holdings` for the current date before fetching prices and computing
`running_nav`. Pre-boundary resolution remains predecessor-bound; on/after the
boundary it uses successor identity and exact fractional conversion. The test
with only a successor quote reproduces a `2000.0` running NAV. Source evidence
is read only and the change stays inside the authorized shadow path.

## 8. B6 and B7/A14

B6 is **`RESOLVED — REGRESSION EVIDENCE RESTORED`**. Git `HEAD` and the live
test both contain `assert result["result"]["status"] == "ok"` in
`test_compute_ideal_series_replay_is_deterministic`; no other pre-existing
test assertion was deleted or weakened.

B7 is **`NOT FULLY RESOLVED — INSUFFICIENT ACTIVE-MODEL EVIDENCE`**. The new
static test proves full holdings business fields, stable identity/symbol,
non-compounded shares, stable market values, stable row count/date set, no
duplicates/orphans, and (with the separate twice-run sentinel test) protected
pre-boundary rows. The active-model idempotency test still compares only
`total_value`, date keys, and write count. It does not compare active persisted
holdings fields or independently prove no orphan rows, and its path currently
violates the pre-boundary rule.

## 9. C1-C6 and consumers

| Capability | Result | Evidence |
|---|---|---|
| C1 | `PASS — PRESERVED` | narrow outgoing `MERGED_INTO`; single hop; effective date; inclusive boundary; null-date/unrelated behavior; no generalized framework |
| C2/C3/C4 | `PASS` | integrated identity, ratio, quantity, pricing, serialization, and persisted static/active rows are coherent on/after boundary |
| C5 | `PASS — PRESERVED` | `horizon_grader.py` and its test are byte-identical to the failed candidate; the previously passing translation semantics remain green |
| C6 | `FAIL` | active-model regeneration mutates protected pre-boundary rows |

The integrated canonical-position → relationship → exact ledger evidence →
ratio → fractional quantity → identity → valuation → serialization → upsert
chain is coherent where writes are authorized. It is not complete as a frozen
WP6 whole because the active writer lacks C6 protection and active Contract-B
evidence remains incomplete.

Confirm-or-implement consumers:

| Consumer | Result | Evidence |
|---|---|---|
| `quant_engine.py` | `CONFIRMED — NO SOURCE CHANGE REQUIRED` | operative decisions use aggregate snapshot values; symbol is display-only |
| `ideal_series.py` | `CONFIRMED — NO SOURCE CHANGE REQUIRED` | per-row shadow symbol joins canonical portfolio price history; corrected B4 binding now proves the common transition date |
| `attribution.py` | `CONFIRMED — NO SOURCE CHANGE REQUIRED` | operative attribution consumes aggregate shadow total value; no symbol-keyed join |

## 10. Acceptance matrix WP6-A1 through WP6-A18

| ID | Controlling requirement | Evidence / execution | Result |
|---|---|---|---|
| A1 | predecessor before; successor at/after boundary | C1 source + 10 helper tests | `PASS` |
| A2 | null effective date never resolves successor | source + null-date test | `PASS` |
| A3 | holdings JSON identity continuity | static/active persisted JSON source and tests | `PASS` |
| A4 | non-null asset ID on affected entries | persisted boundary rows | `PASS` |
| A5 | same schedule as real portfolio | exact payload/relationship transition binding | `PASS` |
| A6 | exact fractional ratio; no whole-share rounding | Decimal path + success/fail-closed tests | `PASS` |
| A7 | no broker cash-in-lieu | source review | `PASS` |
| A8 | inception/NAV continuity | exact ratio/inception-price transform + active NAV test | `PASS` |
| A9 | attribution continuity | aggregate consumer review | `PASS` |
| A10 | converted directional call remains evaluable | preserved horizon end-to-end test | `PASS` |
| A11 | post-boundary valuation-subject normalization | persisted static/active holdings and ideal-series schedule | `PASS` |
| A12 | immutable historical recommendation/decision evidence | source + preserved test | `PASS` |
| A13 | no pre-boundary persisted write | static sentinel passes; active sentinel reproduction fails | `FAIL` |
| A14 | Contract-B persisted convergence | static full-state evidence; active evidence remains aggregate-only and path violates boundary | `INSUFFICIENT EVIDENCE` |
| A15 | unrelated symbol unchanged | helper/shadow tests + no-boundary source path | `PASS` |
| A16 | no generalized framework | narrow helper/diff | `PASS` |
| A17 | no forbidden schema/write-path surface | complete diff/status audit | `PASS` |
| A18 | no M46 modification | complete diff/status audit | `PASS` |

## 11. Executed tests and broad-suite comparison

Focused command collected and passed exactly:

- `test_position_conversion.py`: 10;
- `test_shadow_regeneration.py`: 28;
- `test_horizon_grader.py`: 20;
- `test_ideal_series.py`: 18;
- total: **76 passed**, 0 failed/errors/skipped (687 warnings; 6.20 s).

Frozen neighboring suites: **505 passed**, 0 failed/errors/skipped (1,242
warnings; 6.20 s).

Broad comparison excluded the same crash-prone/debug corpus identified by the
failed review: `tests/investigate`, `test_pandas.py`, `test_dr.py`,
`test_yf.py`, and `test_snapshot_repair.py`.

| Corpus | Passed | Failed | Skipped | Errors | Normalized bad IDs |
|---|---:|---:|---:|---:|---:|
| Corrected candidate | 2,931 | 62 | 32 | 3 | 65 |
| Immutable `git archive HEAD` baseline | 2,903 | 62 | 32 | 3 | 65 |

Normalized comparison: candidate-only bad IDs `0`; baseline-only bad IDs `0`.
The corrected candidate adds 28 passing tests and zero broad-suite bad
identities. The claimed 53 failing IDs is not reproducible in this environment;
the stable comparison is 65 identical bad identities (62 failures + 3 setup
errors) in both corpora.

## 12. Diff/authorization and documentary audit

Every live production/test path is authorized. The new helper remains narrow.
No schema/model/migration/endpoint/CLI/frontend, transaction write path,
WP3/WP4/WP5 frozen production surface, M46, Decision Log, or INDEX path is
changed. No unrelated refactor or weakened assertion was found. The WPP
statement that `regenerate_static_shadow` contains a bulk `.delete()` remains
factually wrong but non-normative: **`NON-BLOCKING DOCUMENTARY INACCURACY`**,
carried forward without reopening frozen planning.

## 13. Blocker, disposition, and constitutional state

**Blocker WP6-RR-B1:** `regenerate_active_model_shadow` does not apply the
frozen pre-boundary persistence guard and demonstrably rewrites protected
active-model rows. The smallest bounded corrective act is to apply the same
relationship-derived write-boundary protection to its persistence loop while
continuing full in-memory replay, and add direct active-model sentinel plus
full persisted-business-state rerun evidence (including duplicates/orphans).
No planning amendment or authority expansion is required.

Canonical disposition:

**`BANPU-WP6 INDEPENDENT IMPLEMENTATION RE-REVIEW FAILED`**

Resulting state:

- BANPU-WP6 remains `ALLOCATED` and bounded `IMPLEMENTATION AUTHORIZED`;
- Planning remains `PLANNING CONFIRMED` and `PLANNING FROZEN` at the exact WPP identity;
- the corrected candidate at aggregate `32714BFCC9EB1F6820BF3E2757AE75F6A864494C148B06FD514D819F796372FD` has failed independent re-review;
- Implementation Confirmation, Implementation Freeze, closeout, release/deployment, production mutation, residual discharge, and WP7+ remain unperformed/unauthorized.

The exact next constitutional act is a bounded **BANPU-WP6 implementation
correction** limited to WP6-RR-B1 and the associated active-model A14 evidence,
followed by another fresh independent implementation re-review. This act
performs neither next act.

