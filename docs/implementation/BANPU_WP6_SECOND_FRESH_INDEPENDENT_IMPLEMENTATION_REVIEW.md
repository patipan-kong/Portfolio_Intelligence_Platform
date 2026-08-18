# BANPU-WP6 — Second Fresh Independent Implementation Re-Review

**Artifact class:** Additive second fresh independent implementation re-review record  
**Review date:** 2026-08-18  
**Review boundary:** `READ-ONLY INDEPENDENT IMPLEMENTATION RE-REVIEW ONLY`  
**Current candidate aggregate:** `0CB01B5849062C141F9BCEA477A4E633AFA6BB220691251B3DC624EE9B72F9B7`  
**Historical failed candidate aggregates:** `66612230CE88D363B335DD718D06CB6E5E1F9B03D7C8687656663ED408B79B14`, `32714BFCC9EB1F6820BF3E2757AE75F6A864494C148B06FD514D819F796372FD`  
**Disposition:** `BANPU-WP6 INDEPENDENT IMPLEMENTATION RE-REVIEW PASSED`  
**Implementation Confirmation/Freeze/closeout performed:** `NO`  
**Release/deployment/production mutation performed or authorized:** `NO`

## 1. Independent method and constitutional entry state

This act independently queried the repository knowledge graph before source
inspection, read the complete frozen authority/planning and both failed review
artifacts, re-derived the live implementation/test corpus from Git state,
recomputed every identity, reconstructed the exact second correction against
the prior failed aggregate, inspected the complete implementation/test diff,
executed focused and neighboring tests, reproduced the active persistence
boundary in a separate in-memory database, exercised six boundary-derivation
scenarios, and compared normalized broad-suite failure identities against an
immutable `git archive HEAD` baseline. Correction statements were history, not
proof.

No implementation, test, planning, governance, prior review, Decision Log,
INDEX, staging, commit, release/deployment, or production-data state was
modified. This file is the only additive repository artifact created by this
re-review.

| Entry premise | Independent result |
|---|---|
| Allocation | `PASS` — `BANPU-WP6 ALLOCATED`; 16,307 bytes; `208C2B236D669141BC947A96D82C5C249535E95EB54483C25496C1B6908D9D58` |
| Implementation Authorization | `PASS` — `BANPU-WP6 IMPLEMENTATION AUTHORIZED`; 18,660 bytes; `442426729C8D7582961CB0BA3B7706356995A39333662042C5BEA260B95BFD0F` |
| Frozen WPP | `PASS` — 53,844 bytes; `1CC7F17C916639DAD08507AEF5875EA72A60D028D0573E7CEAFA1B57D766601A`, exact Freeze identity |
| Planning Confirmation | `PASS` — `BANPU-WP6 PLANNING CONFIRMED`; 22,056 bytes; `53AC63D13EE81FDC99B443DCFA8478F3F58DE72F7F67FDE9EFE38E3789E7C2FE` |
| Planning Freeze | `PASS` — `PLANNING FROZEN`; 21,785 bytes; `1DE5747F78FD42110506E81A8E620BE2367DA000F6FF6CFB1AB66AA02956FEB9` |
| Original failed Independent Review | `PASS` — unchanged; 22,726 bytes; `6B10B314C5CA8D0AA315B00CD7AA082AADF39EC68EC83266EA5F3518A7A30D32`; `FAIL — IMPLEMENTATION CORRECTION REQUIRED` remains recorded |
| Prior Fresh Independent Re-Review | `PASS` — unchanged; 17,416 bytes; `75670FCD08C482DCFAB94D5006BD43684268330A72D89E48B7EB0FEA8FFE1900`; `BANPU-WP6 INDEPENDENT IMPLEMENTATION RE-REVIEW FAILED` remains recorded |
| Prior remaining blocker | `PASS` — the prior re-review identifies exactly one remaining blocker, `WP6-RR-B1` |
| Confirmation / Freeze / closeout | `PASS` — no BANPU-WP6 Implementation Confirmation, Implementation Freeze, closeout, release, or deployment artifact exists |
| WP7+ | `PASS` — no BANPU-WP7 Allocation or Authorization artifact exists |
| Git index | `PASS` — nothing staged |

No prerequisite failed, so substantive review proceeded.

## 2. Current candidate identity

The repository-derived implementation/test diff yields exactly seven candidate
members. The aggregate is SHA-256 over the ordered UTF-8 rows
`path<TAB>lowercase-SHA256<TAB>bytes<LF>` below.

| Path | Status | Bytes | SHA-256 | Authorization basis |
|---|---:|---:|---|---|
| `backend/services/decision_memory/shadow_tracker.py` | modified | 99,858 | `342481763FE73C2A08BE443A7255F4C5D6E5753F5B2F1812D74883DEEEE82F08` | Authorization §4.1; C2/C3/C4/C6 |
| `backend/services/evaluation/horizon_grader.py` | modified | 14,638 | `3C09473A9D4FE2359A1B56E539BDDF3D2AF600CD0C2DE7393FC10C9882ADCC7E` | Authorization §4.1; C1/C5 |
| `backend/services/position_conversion.py` | new | 7,413 | `BFE1BE7A6620FCAD12C87D42DF3101051185E76B6C97FE637225B3DD8536BA94` | Authorization §4.1 narrow helper; WPP §7.1 |
| `backend/tests/test_horizon_grader.py` | modified | 24,340 | `902DFF05D05FA35ED72341A504478B382DC246F66A978295D631C036DB3E57FE` | Authorization §4.2; A10/A12/A15 |
| `backend/tests/test_ideal_series.py` | modified | 24,270 | `440EF04D0CBCA49729A4639E91B942E52FA81196FF6797C079C05FEF5BEF8BDA` | Authorization §4.2; A11 |
| `backend/tests/test_position_conversion.py` | new | 5,734 | `621EA7D91F6416DFE013495D7366F8CF880F9A0B988A6B3734A582471B3986C2` | Authorization §4.2 focused helper tests; A1/A2 |
| `backend/tests/test_shadow_regeneration.py` | modified | 63,693 | `BA9E488FD37625F882C7D83446CFD099DC6BF877FFA3C33E972E6C3B3C0150C1` | Authorization §4.2; A3-A8/A13-A15 |

**Aggregate:**
`0CB01B5849062C141F9BCEA477A4E633AFA6BB220691251B3DC624EE9B72F9B7`.

It equals the required current identity exactly. The two earlier aggregates are
historical failed identities only.

## 3. Exact second-correction diff

Comparison against the seven identities recorded for aggregate
`32714BFCC9EB1F6820BF3E2757AE75F6A864494C148B06FD514D819F796372FD`
proves that five members are byte-identical and exactly two changed:

| Path | Prior identity / bytes | Current identity / bytes | Exact correction |
|---|---|---|---|
| `shadow_tracker.py` | `EC1E55F3C53F004E5C57D10514CB1462A4A6539869830B2CB61B06A1E7313087` / 95,108 | `342481763FE73C2A08BE443A7255F4C5D6E5753F5B2F1812D74883DEEEE82F08` / 99,858 | active-replay write-boundary derivation over seed plus rebalance allocations; return of that boundary; active persistence guard; prior-row daily-return seed; directly associated documentation |
| `test_shadow_regeneration.py` | `DB78241A40641CA7A89C38D7C7FAD230A0F7A87FEC8C2C41FF7A8454C3A995C7` / 53,848 | `BA9E488FD37625F882C7D83446CFD099DC6BF877FFA3C33E972E6C3B3C0150C1` / 63,693 | appended active pre-boundary sentinel and active full persisted-state Contract-B rerun tests |

The test change is exactly a 9,845-byte append: the current file's first
53,848 bytes reproduce the prior hash exactly. Reversing only the active
boundary documentation, seed/rebalance union, returned boundary, persistence
guard, and return-continuity seed reconstructs the prior production file at
95,108 bytes and its exact prior hash. No other candidate member changed. No
previously passed production logic was rewritten, and every new hunk is
directly necessary for `WP6-RR-B1`, A13, A14, or its mechanical documentation.

## 4. Prior blocker authority

The complete prior Fresh Independent Implementation Re-Review has exactly one
remaining blocker: `WP6-RR-B1`. It inseparably requires:

1. active-model regeneration to continue any necessary pre-boundary in-memory
   replay while persisting no mutation to protected pre-boundary rows; and
2. active Contract-B evidence to prove full persisted-business-state
   convergence, non-compounded conversion, and duplicate/orphan protection.

No other blocking or correction-required finding remained open. The prior B5
active NAV finding was resolved; B3/B4 provenance was resolved; B1 holdings
persistence and B6 regression evidence were resolved. B7 remained only as the
active Contract-B evidence half incorporated into `WP6-RR-B1`.

## 5. WP6-RR-B1 — active persistence boundary

**Result: `WP6-RR-B1 RESOLVED`.**

`_replay_active_model_series` still computes every replay date from inception.
It derives `write_boundary` from raw base identities in the seed allocations
plus every parsed historical rebalance allocation and returns the ISO date to
the writer. The persistence loop loads existing rows, optionally seeds return
continuity from the last untouched pre-boundary row, and executes `continue`
before holdings serialization, existing-row lookup, field assignment, or new
row insertion whenever `date < write_boundary`. At/on and after the boundary,
the existing upsert-by-date path proceeds normally. No delete path exists in
active regeneration.

This separates replay state from persistence state as frozen WPP §7.2 requires.
Later rows still use the fully replayed preceding holdings, cash, prices, and
rebalance NAV; only the database write is bounded.

## 6. Active boundary derivation

**Result: `PASS`.** The independently executed scenarios returned:

| Scenario | Observed result |
|---|---|
| seed holding converts | its effective date |
| rebalance-introduced holding converts | its effective date is found through the seed/rebalance union |
| only one of multiple holdings converts | converting holding's date |
| multiple holdings convert on different dates | earliest effective date |
| no holding converts | `None`, leaving persistence unrestricted |
| holding appears after another holding's earlier boundary | earlier boundary remains row-write boundary; later holding remains date-resolved independently |

At the early date in the two-conversion reproduction, the early holding was
successor-shaped at 50 fractional shares while the later holding remained the
predecessor at 80 shares. At the later date, the latter became its successor at
20 fractional shares. Thus earliest-boundary row eligibility does not cause a
later-converting holding to transition early, and it does not suppress an
earlier-converting holding until a later/global boundary.

## 7. Independent active sentinel reproduction

A separate in-memory SQLite fixture used boundary `2026-08-17`, an existing
sentinel row at `2026-08-16`, and deliberately distinguishable values:
`total_value=987654.25`, `return_pct_since_inception=321.25`,
`daily_return_pct=-12.5`, sentinel holdings JSON, and sentinel benchmark.

Run 1 returned `regenerated`, wrote exactly the two eligible rows, and left all
five sentinel fields unchanged after database reload. Run 2 returned the same
status/write count and again left all five fields unchanged. Persisted dates
were exactly `2026-08-16`, `2026-08-17`, and `2026-08-18`; the two non-sentinel
dates were on/after the boundary.

**`WP6-RR-B1 RESOLVED`.**

## 8. A13 and A14

**A13: `PASS`.** Both governed regeneration families now have direct evidence.
Static and active fixtures prove existing pre-boundary rows survive unchanged
through two runs. Because the initial databases contain no other pre-boundary
rows and the resulting row sets contain only the sentinel plus on/after-boundary
rows, the absent-row/insert path is also proven protected. Source inspection
shows both update and insert operations occur after their guards; neither path
deletes protected rows.

**A14: `PASS`.** The strengthened active test runs regeneration twice against
unchanged canonical inputs and reloads persistence after each run. Eligible
row/date sets, row counts, return fields, total values, and complete holdings
objects converge. The persisted holdings objects include the same entry count,
successor asset ID and symbol, 50,000 fractional shares, inception/current
price fields, market value, and price source. Equality of the complete objects
proves those fields remain identical on run 2; the explicit share assertion
proves the 0.5 ratio did not compound. Database row count equals unique date
count, no additional/orphan date appears, and the protected sentinel remains
unchanged. Contract C (zero-write/timestamp identity) is neither required nor
claimed.

## 9. Preservation register

| Finding/capability | Result | Independent evidence |
|---|---|---|
| B1 holdings JSON | `PASS — PRESERVED` | enriched holdings still feed static and active insert/update persistence paths |
| B3 exact ratio evidence | `PASS — PRESERVED` | portfolio/type/predecessor/successor selectors; malformed/zero/duplicate/mismatched cases fail closed |
| B4 schedule binding | `PASS — PRESERVED` | payload `valuation_transition_date` must equal relationship effective date; mismatch test green |
| B5 active NAV succession | `PASS — PRESERVED` | old holdings are translated at current date before price/NAV; successor-only quote fixture still returns `running_nav=2000.0` |
| B6 deterministic assertion | `PASS — PRESERVED` | exact pre-existing `assert result["result"]["status"] == "ok"` remains at test line 528; no assertion was weakened/deleted |
| C1 | `PASS — PRESERVED` | `position_conversion.py` and its ten tests retain prior identities and remain green |
| C5 | `PASS — PRESERVED` | `horizon_grader.py` and its test retain prior identities; directional converted-holding test remains green |

The B3/B4 fail-closed tests cover unrelated conversions, date mismatch,
ambiguous duplicates, missing/malformed evidence, repeated historical
conversions, unbound ratio, and the positive uniquely bound case. The second
correction does not touch their code or tests.

## 10. Integrated capabilities C2/C3/C4/C6

| Capability | Result | Evidence |
|---|---|---|
| C2 identity continuity | `PASS` | predecessor before each holding's date; successor at/on and after; persisted JSON carries coherent symbol/asset ID |
| C3 quantity continuity | `PASS` | exact relationship-bound ledger ratio; Decimal-based fractional conversion; no rerun compounding |
| C4 valuation continuity | `PASS` | successor pricing and transformed inception price/market value align with successor identity and NAV |
| C6 persistence boundary | `PASS` | full in-memory replay plus static/active write guards; direct two-run sentinel reproduction |

The complete flow — canonical evidence → single-hop succession resolution →
exact conversion record → fractional quantity → identity normalization →
date-specific price → in-memory replay → enriched serialization → bounded
upsert → repeated convergence — has no observed partial state. Identity never
transitions without quantity, quantity never transitions without identity,
successor holdings do not use predecessor pricing, later holdings do not
transition early, protected rows are not persisted, and conversion does not
compound.

## 11. Confirm-or-implement consumers

| Consumer | Result | Basis |
|---|---|---|
| `backend/services/analytics/quant_engine.py` | `CONFIRMED — NO SOURCE CHANGE REQUIRED` | operative return/risk paths consume snapshot totals; holdings symbols are presentation/diagnostic inputs and no changed premise requires source work |
| `backend/services/evaluation/ideal_series.py` | `CONFIRMED — NO SOURCE CHANGE REQUIRED` | shadow holdings are revalued per row by their persisted date-specific symbols; exact transition binding and corrected bounded persistence preserve its premise |
| `backend/services/decision_memory/attribution.py` | `CONFIRMED — NO SOURCE CHANGE REQUIRED` | operative attribution consumes ordered aggregate shadow totals; no identity-keyed join is introduced by this correction |

All three files are byte-unchanged. The second correction changes only when
active snapshot rows may be persisted and does not invalidate the prior
no-source-change conclusions.

## 12. Acceptance matrix WP6-A1 through WP6-A18

| ID | Controlling requirement | Evidence inspected / executed | Result |
|---|---|---|---|
| A1 | predecessor before, successor at/after boundary | helper source; 10 focused helper tests | `PASS` |
| A2 | null effective date never resolves successor | narrow lookup source; null-date test | `PASS` |
| A3 | holdings JSON identity continuity | static/active persisted/reloaded JSON, independent date-specific two-holding run | `PASS` |
| A4 | non-null asset ID on affected entries | persisted boundary/post-boundary holdings assertions | `PASS` |
| A5 | same transition schedule as real portfolio | exact relationship/payload date binding and mismatch rejection | `PASS` |
| A6 | exact fractional quantity, no whole-share rounding | Decimal ratio path; 0.5/0.25 reproduction; rerun share equality | `PASS` |
| A7 | no broker cash-in-lieu for paper holdings | source/diff inspection; exact fractional tests | `PASS` |
| A8 | inception/NAV continuity | inception-price transform, NAV invariant, preserved active NAV test | `PASS` |
| A9 | attribution continuity | aggregate consumer source inspection and neighboring tests | `PASS` |
| A10 | converted directional call remains evaluable | focused horizon end-to-end test | `PASS` |
| A11 | post-boundary valuation-subject normalization | persisted successor holdings; ideal-series conversion test | `PASS` |
| A12 | immutable recommendation/decision evidence | source/diff audit and focused regression assertions | `PASS` |
| A13 | no pre-boundary persisted write | static/active update and absent-row insert evidence; two-run independent sentinel | `PASS` |
| A14 | Contract-B rerun convergence | full reloaded business fields, date/row sets, no compound/duplicate/orphan, sentinel unchanged | `PASS` |
| A15 | unrelated symbol unchanged | no-relationship path and focused unrelated-symbol test | `PASS` |
| A16 | no generalized corporate-action framework | narrow helper and complete diff | `PASS` |
| A17 | no forbidden schema/write-path change | full status/diff audit; closed neighboring suites green | `PASS` |
| A18 | no M46 modification | full status/diff audit | `PASS` |

All required A1-A18 rows pass. No `FAIL`, `INSUFFICIENT EVIDENCE`, or required
`NOT APPLICABLE` row remains.

## 13. Focused and neighboring tests

Focused execution from `backend`:

| File | Collected/executed | Passed |
|---|---:|---:|
| `test_position_conversion.py` | 10 | 10 |
| `test_shadow_regeneration.py` | 30 | 30 |
| `test_horizon_grader.py` | 20 | 20 |
| `test_ideal_series.py` | 18 | 18 |
| **Total** | **78** | **78** |

Result: **78 passed**, 0 failed/errors/skipped; 723 warnings; 5.70 s.

The exact seven neighboring WP3/WP4/WP5 suites in frozen WPP §11 returned
**505 passed**, 0 failed/errors/skipped; 1,242 warnings; 6.68 s. Running the
entire §11 list including the three focused shadow/horizon/ideal files returned
573 passed. No WP6-attributable neighboring regression exists.

## 14. Broad immutable-baseline comparison

Both corpora used the identical command and exclusions:
`tests/investigate`, `test_pandas.py`, `test_dr.py`, `test_yf.py`, and
`test_snapshot_repair.py`. The baseline was extracted from immutable
`git archive HEAD`; the same external virtual environment was used.

| Corpus | Passed | Failed | Skipped | Errors | Normalized bad IDs |
|---|---:|---:|---:|---:|---:|
| Current candidate | 2,914 | 53 | 32 | 3 | 56 |
| Immutable `HEAD` baseline | 2,884 | 53 | 32 | 3 | 56 |

Normalized candidate-only bad IDs: `0`. Baseline-only bad IDs: `0`. The
candidate therefore adds 30 passes and zero new bad identities. The submitted
62-failed/0-error headline was not reproducible in this environment/order; the
identity comparison, not the varying headline, controls the regression result.

## 15. Documentary observation and authorization audit

The frozen WPP's statement that `regenerate_static_shadow` performs a bulk
`.delete()` remains factually inaccurate. Live source still contains no such
delete in that function. This remains **`NON-BLOCKING DOCUMENTARY
INACCURACY`** and does not reopen frozen planning.

Every implementation/test path is authorized. The complete diff contains no
unrelated refactor, weakened/deleted assertion, schema/model/migration change,
transaction write-path change, endpoint/CLI/frontend change, M46 change,
WP3/WP4/WP5 frozen production-surface change, Decision Log change, or INDEX
change. The second correction does not perform a production regeneration.

## 16. Findings, disposition, and constitutional state

**Blocking findings:** none.

**Non-blocking observations:**

- the frozen WPP `.delete()` attribution remains a documentary inaccuracy;
- broad headline counts are order/environment-sensitive here, but normalized
  current/baseline bad identities are exactly equal.

Canonical disposition:

**`BANPU-WP6 INDEPENDENT IMPLEMENTATION RE-REVIEW PASSED`**

Resulting state:

- BANPU-WP6 remains `ALLOCATED` and bounded `IMPLEMENTATION AUTHORIZED`;
- planning remains `BANPU-WP6 PLANNING CONFIRMED` and `PLANNING FROZEN` at the
  exact WPP identity;
- the seven-member candidate at aggregate
  `0CB01B5849062C141F9BCEA477A4E633AFA6BB220691251B3DC624EE9B72F9B7`
  has passed independent implementation re-review;
- Implementation Confirmation, Implementation Freeze, closeout,
  release/deployment, production mutation, residual discharge, and WP7+
  allocation/authorization remain unperformed and unauthorized.

## 17. Exact next constitutional act

Under live BANPU/WP5 precedent, the exact next act is a **separate BANPU-WP6
Implementation Confirmation** binding the exact seven-member candidate and
aggregate in §2 to this additive passing re-review artifact. Only after that
separate confirmation may the distinct Implementation Freeze act be
considered.

This review performs neither next act.

## 18. Final verification requirement

After this artifact is created, finalization independently rechecks the seven
candidate identities and aggregate, all seven constitutional/history
identities, `git diff --check`, `git diff --cached --check`, the empty index,
and final Git status. No stage, commit, push, release, deployment, or production
act is permitted by this record.
