# BANPU-WP3 — Checkpoint C4 Acceptance Record (WP3.4 and Package Acceptance)

**Artifact class:** Additive constitutional acceptance record
**Review/acceptance date:** 2026-08-11
**Reviewer role:** Independent Checkpoint C4 Reviewer and Acceptance Recorder
**Governing planning corpus identity:** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Amended Work Package Plan identity:** `84E1EC24ACF436AFCC26BFABB4E982692BDB80AAF24B02828356D0F69B23045D`
**Disposition:** `CHECKPOINT C4 — PASSED` / `BANPU-WP3.4 INDEPENDENTLY ACCEPTED`

## 1. Nature of this record

This artifact records an independent re-review of Checkpoint C4 ("WP3.4 and
package acceptance") against current repository state, per
[`BANPU_WP3_WORK_PACKAGE_PLAN.md`](BANPU_WP3_WORK_PACKAGE_PLAN.md) §5. It
creates no implementation authority beyond
[`BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md).
It does not perform WP3 Implementation Confirmation, does not perform
Implementation Freeze, and modifies no existing governance, production, or
test artifact.

## 2. Durable dependencies verified

| Dependency | Claim inspected | Verification |
|---|---|---|
| [`BANPU_WP3_BPA1_C3_ACCESSOR_DELTA_ACCEPTANCE.md`](BANPU_WP3_BPA1_C3_ACCESSOR_DELTA_ACCEPTANCE.md) | BPA-1 accessor delta independently accepted; does not itself claim C4 | Re-hashed: 7,975 bytes, `D35B2AE7363CE8FC1A78D8C4213B45050ECD52563C925F1703B0D4E4DCED0167` — unchanged since creation; §10 explicitly states "Checkpoint C4 remains incomplete" |
| [`BANPU_WP3_STEP_4_1_CALL_PATH_EVIDENCE.md`](BANPU_WP3_STEP_4_1_CALL_PATH_EVIDENCE.md) | Step 4.1 evidence complete and current; does not itself claim C4 | Re-hashed: 12,262 bytes, `256E53459CFC7AEF5EF56D1F970127C5165E0973AE3B2A6245EEEB91837E25FB` — unchanged since creation; §12 explicitly states "Checkpoint C4 is NOT performed by this act" |

Both records bind the current governing corpus (`3A04B06A9...`) and amended
Work Package Plan (`84E1EC24A...`) identities, confirmed identical to those
re-verified in §7 below.

## 3. Step 4.1 re-verified against live code

Fresh enumeration repeated (`grep -rn "fetch_price_info" backend --include="*.py"`,
excluding definition/imports/comments/tests, covering both direct-call and
`asyncio.to_thread(fetch_price_info, ...)` forms): **exactly 11 production
call sites**, identical topology to the durable Step 4.1 register — no site
added, removed, or reclassified.

- **Exactly one bound caller:** `main.py:736`, inside `get_portfolio_prices`
  (`GET /portfolios/{id}/prices`), supplied via `resolve_successor_bindings(
  symbols)` at `main.py:732` — the sole production consumer of that accessor
  (re-confirmed by grep: definition, one import, one call, test-only
  references).
- **Exactly ten deliberately unbound callers**, matching the durable
  register exactly: `main.py:759/883/1047/1052/2038/2045/4712`,
  `portfolio_snapshots.py:333`, `idea_review.py:396`, `factor_engine.py:797`.

Re-ran `backend/tests/test_wp34_call_path_propagation.py` (13 tests) —
all 13 confirmed present and passing, corresponding to all 11 conceptual
sites (§6 of the Step 4.1 evidence record). No topology drift; nothing fails
closed here.

## 4. Step 4.4 boundary audit (per current amended Work Package Plan §3.4)

**A. WP1 frozen 12-file aggregate.** Recomputed under the per-row convention
recorded in Planning Freeze Record §11.3 (LF-normalized SHA-256 for ten
rows; raw working-tree SHA-256 for `transaction_canonicalizer.py` and
`test_transaction_canonicalizer.py`, whose current raw bytes and SHA-256
were independently confirmed byte-identical to the original Freeze Record
values). Recomputed aggregate: `DF0AF823EFEACA38171F4DACAC0B19975BAE07EE1BA09A040B549B06ACD443E1` — **exact match**.

**B. WP2 implementation 6-file aggregate.** Current raw working-tree bytes
for all six files were found larger than previously recorded (by exactly
each file's prior "lone-LF" line count, per the pre-existing
`BANPU_WP2_COMMITTED_IDENTITY_CONTINUITY_RECORD.md` §8 table) — a benign
`core.autocrlf=true` checkout re-normalization converting previously bare-LF
lines to CRLF, not a content change. LF-normalizing current bytes and
applying the Plan's own committed-blob-analogy manifest reproduces
`6E50F5B5E2AAA008EA1C3DA25D1FC34C41F9CBAE81A293A463FB3F6BF5DA4159` exactly —
**exact match**, confirming zero content drift.

**C. WP2 planning 3-file aggregate.** LF-normalized manifest recomputed:
`91F9295BBF71BC9FA50D8246893DA693189C8855D4B6F0E146822E36F76DFB5E` —
**exact match** (matched on direct recomputation, no convention ambiguity).

**D. BPA-1 / frozen WP3 planning corpus.** Recomputed aggregate manifest
over `BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md`
(`DF4630CFC00A32402B45489D1779F3BBAAD39A86630301256C541BC806481DD7`) and
`BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md`
(`48BE744AD91367293FF790772A96FA49D60058CF0221080F538AE6FBEB3BAB01`):
`3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D` — **exact
match**.

**E. Amended Work Package Plan.** Direct SHA-256, 49,541 bytes:
`84E1EC24ACF436AFCC26BFABB4E982692BDB80AAF24B02828356D0F69B23045D` — **exact
match**.

**F. M46 unchanged.** `git status --porcelain -- '*M46*'` returns nothing —
no `M46*` file tracked as modified or untracked. **Confirmed unchanged.**

**G. WP2 deferral guard green.** `test_position_conversion_replay.py` run
as part of the combined regression (§5) — passing, as a frozen-boundary
preservation check (PD-3 obligation B3), not a behavioral dependency.
**Green.**

**H. Complete implementation/test diff ⊆ authorized surface `A` + BPA-1
exception.** `git diff --name-only` (unstaged production/test paths):
`backend/main.py`, `backend/services/data_fetcher.py`,
`backend/services/market_data/yahoo_chart.py`,
`backend/tests/test_fetch_history.py`,
`backend/tests/test_yahoo_chart_provider.py`. New untracked production/test
paths: `backend/services/market_data/position_conversion_quote_contract.py`,
`backend/tests/test_position_conversion_quote_contract.py`,
`backend/tests/test_quote_epoch_isolation.py`,
`backend/tests/test_wp34_call_path_propagation.py`. Every one of these nine
paths is an exact row of surface `A` (Plan §2), including the `[BPA-1]` row
bounded to `resolve_successor_bindings(symbols)` in `data_fetcher.py`.
**Zero paths outside `A`.**

**I. Prohibited surface `P` untouched.** None of the modified/untracked
production or test paths above intersects `P`. The WP1/WP2 frozen corpora
and the four `P`-listed consumer modules
(`portfolio_transactions.py`, `portfolio_snapshots.py`, `idea_review.py`,
`analytics/factor_engine.py`) show zero content drift, confirmed by the
aggregate reverification in A/B above and by direct absence from the diff
in H. **Confirmed untouched.**

**J. WP3.1–WP3.3 accepted semantics intact.** `fetch_price_info`'s signature
and branching (`data_fetcher.py:948-964`), `_guard_result_from_projection`
semantics (`data_fetcher.py:217-238`), and `_quote_quarantine_response`
shape (`data_fetcher.py:455-468`) were re-read and found unchanged from the
Checkpoint C3-accepted state. Not reopened; only re-confirmed unchanged.

**K. Reference-price/WP5 boundary intact.**
[`BANPU_WP3_REFERENCE_PRICE_ADMISSIBILITY_CLARIFICATION_RECORD.md`](BANPU_WP3_REFERENCE_PRICE_ADMISSIBILITY_CLARIFICATION_RECORD.md)
remains present and unmodified by this act; A9's WP5 exclusion (mechanical
continuity tolerance reconciliation) was not reopened or touched by any
WP3.4 evidence produced this session.

**L. No WP4 implementation or authority.** No file outside the WP3
authorized surface was touched; no WP4-scoped module exists in the diff or
untracked set.

**M. Graphify state current.** `graphify update .` run: 21,152 nodes, 40,889
edges, 1,731 communities rebuilt; `graphify-out/` is fully `.gitignore`d
(`git check-ignore -v graphify-out/graph.json` confirms), so this produces
no git-visible change.

**N. Repository hygiene clean.** See §8.

## 5. Regression evidence

C4-required set — WP3.4 focused suite, WP3.3, WP3.2, WP3.1, WP1 owners,
WP2 deferral guard, and affected unchanged consumers, run together:

```
tests/test_yahoo_chart_provider.py            (WP3.1)
tests/test_position_conversion_quote_contract.py  (WP3.2)
tests/test_quote_epoch_isolation.py           (WP3.3)
tests/test_fetch_history.py                   (WP3.4)
tests/test_wp34_call_path_propagation.py      (WP3.4)
tests/test_position_conversion_replay.py      (WP2 deferral guard)
tests/test_transaction_canonicalizer.py       (WP1 owner)
tests/test_position_conversion_migration.py   (WP1 owner)
tests/test_workspace_referenceability_m36_1_wp4c.py  (consumer)
tests/test_watchlist_registry.py              (consumer)
tests/test_factor_engine_asset_id.py          (consumer)
tests/test_portfolio_snapshot_capability_shadow.py   (consumer)

444 passed, 32 skipped (live-network-gated), 490 warnings, 0 failed
```

No regression. The previously reported Python 3.13 asyncio
`get_event_loop()`-ordering fragility (5 known files, none included in this
run's file list) was not re-triggered here and is not reproduced by this
act; it remains a separately reported, pre-existing artifact per the Step
4.1 evidence record, not repaired.

## 6. Full authorized-surface audit

| Path | Class | Surface |
|---|---|---|
| `backend/services/market_data/yahoo_chart.py` | Production | `A` — WP3.1 |
| `backend/tests/test_yahoo_chart_provider.py` | Test | `A` — WP3.1 |
| `backend/services/market_data/position_conversion_quote_contract.py` | Production | `A` — WP3.2 |
| `backend/tests/test_position_conversion_quote_contract.py` | Test | `A` — WP3.2 |
| `backend/services/data_fetcher.py` | Production | `A` — WP3.3, plus `[BPA-1]` `resolve_successor_bindings(symbols)` |
| `backend/tests/test_quote_epoch_isolation.py` | Test | `A` — WP3.3 |
| `backend/main.py` | Production | `A` — WP3.4, holdings/price call site only |
| `backend/tests/test_fetch_history.py` | Test | `A` — WP3.4 |
| `backend/tests/test_wp34_call_path_propagation.py` | Test | `A` — WP3.4 regression module |

No schema, migration, frontend, `M46*`, WP4, or unrelated production file
appears modified or newly created anywhere in `git status --porcelain`
beyond this authorized list and the additive WP3 governance/lifecycle
records (which are procedural evidence artifacts, not part of `A` or `P` in
the production-code sense, consistent with every prior act in this
lifecycle chain).

## 7. Identity verification (independently recomputed, not inferred from diff)

| Identity | Value | Result |
|---|---|---|
| Frozen amended planning corpus | `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D` | Exact match |
| Amended Work Package Plan | `84E1EC24ACF436AFCC26BFABB4E982692BDB80AAF24B02828356D0F69B23045D` | Exact match |
| WP1 frozen 12-file aggregate (per-row convention) | `DF0AF823EFEACA38171F4DACAC0B19975BAE07EE1BA09A040B549B06ACD443E1` | Exact match |
| WP2 implementation 6-file aggregate (LF-normalized vs. blob) | `6E50F5B5E2AAA008EA1C3DA25D1FC34C41F9CBAE81A293A463FB3F6BF5DA4159` | Exact match |
| WP2 planning 3-file aggregate | `91F9295BBF71BC9FA50D8246893DA693189C8855D4B6F0E146822E36F76DFB5E` | Exact match |

## 8. A1–A14 acceptance criteria matrix

| # | Criterion (abridged) | Discharged by |
|---|---|---|
| A1 | Cross-symbol/cross-epoch results never produce a usable quote | WP3.2/WP3.3 accepted evidence (C2, C3) |
| A2 | First successor-epoch quote: null previous close, never predecessor close | WP3.3 accepted evidence (C3) |
| A3 | Converted cache entries asset- and epoch-bound | WP3.3 cache namespacing (C3) |
| A4 | Unconverted quote/cache behavior unchanged | WP3.1 baseline (C1); WP3.3 empty-guard-set identity (C3); WP3.4 `test_owning_call_site_preserves_legacy_behavior_for_unconverted_holding` |
| A5 | Quarantine blocks only the affected converted identity | WP3.3 G1–G4 (C3) |
| A6 | Zero conversions ⇒ behavior indistinguishable from baseline | WP3.1/WP3.3 inert-at-zero-conversions evidence (C1, C3) |
| A7 | Exactly one enumerated quarantine reason per rejection | WP3.3 quarantine reason enum (C3) |
| A8 | No stale-cache fallback for a quarantined identity | WP3.3 `_get_stale` suppression (C3); re-confirmed by Step 4.1 §8 |
| A9 | Reference-price admissibility at consumption, WP5 boundary preserved | WP3.2 (C2); reference-price/WP5 clarification record, §4.K above |
| A10 | No caller obtains a converted-identity price without a valid binding; refusal observable/structured | Step 4.1 exhaustive 11-site register (1 bound, 10 refused) + WP3.3 G4 transition test |
| A11 | Namespaced `cache_type` deterministic/enumerable; no admin endpoint change | WP3.3 (C3); confirmed no admin endpoint in diff (§4.H) |
| A12 | No migration, no `MarketDataCache` schema change, no public API contract change | Surface audit §6; Step 4.1 "no endpoint or response-shape change" |
| A13 | Change surface confined to authorized lists; M46 unchanged; WP1/WP2 unchanged | This record §4.A/B/C/F/H/I |
| A14 | `graphify update .` run; surface matches declared boundary | This record §4.M |

A1–A12 rest on already-accepted WP3.1–WP3.3 evidence plus the WP3.4 Step 4.1
evidence record, not reopened here. A13 and A14 are discharged directly by
this record's own Step 4.4 audit.

## 9. C4 determination

| Question | Answer |
|---|---|
| Step 4.1 complete? | Yes |
| All 11 sites accounted for? | Yes — fresh re-enumeration matches the durable register exactly |
| Bound caller correct? | Yes — sole bound site, sole `resolve_successor_bindings` consumer |
| Ten unbound callers fail closed? | Yes — per-site evidence intact, zero provider calls on refusal |
| Step 4.4 complete? | Yes — all fourteen items (§4.A–N) verified |
| Full surface authorized? | Yes — zero paths outside `A` |
| WP1/WP2 identities preserved? | Yes — all three aggregates exact match |
| M46 unchanged? | Yes |
| WP2 deferral guard green? | Yes |
| A1–A14 satisfied? | Yes |
| Every C4 condition met? | Yes |
| WP3.4 independently accepted? | Yes |

**Findings:**

No `BLOCKING` findings. No `MAJOR` findings.

`OBSERVATION-C4-1`: current raw working-tree bytes for the WP1 pair
(`transaction_canonicalizer.py`, `test_transaction_canonicalizer.py`) and
the entire WP2 six-file implementation corpus carry more CRLF pairs today
than at their respective freeze/continuity-record capture times — a
`core.autocrlf=true` checkout re-normalization of previously bare-LF lines,
not a content change. Confirmed via exact byte-count deltas matching the
WP2 Continuity Record's own "lone-LF" counts, and via unchanged raw SHA-256
for the two WP1 rows. Recorded so a future uniform (non-per-row) identity
check does not misreport drift that is not present. No action required.

`OBSERVATION-C4-2`: `BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md`,
`BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md`, and
`BANPU_WP3_WORK_PACKAGE_PLAN.md` show as staged-and-further-modified (`AM`)
in `git status --porcelain`, a pre-existing index/working-tree split
predating this act. Content hashes were independently reconfirmed exact
against their recorded identities in §4.D/E; this is a staging-state
artifact only, already noted in every prior act of this lifecycle chain.

## 10. Regression / hygiene disposition

No `BLOCKING` or `MAJOR` finding remains. C4 acceptance is materialized.

## 11. Disposition

**`CHECKPOINT C4 — PASSED`**
**`BANPU-WP3.4 INDEPENDENTLY ACCEPTED`**

Per Plan §5's standing instruction, acceptance at C4 is package acceptance
only. **WP3 Implementation Confirmation is NOT performed by this record.**
Implementation Freeze is NOT performed by this record. No commit, push,
deploy, or release occurred.

## 12. Exact next act

BANPU-WP3 Implementation Confirmation. This record does not perform that
act.
