# BANPU-WP7 — Implementation Freeze Record

**Artifact class:** Additive implementation freeze record
**Freeze date:** 2026-08-19
**Issuing role:** Independent BANPU-WP7 Implementation Freeze Authority
**Frozen work package:** `BANPU-WP7`
**Disposition:** `BANPU-WP7 IMPLEMENTATION FROZEN`
**Implementation authority:** `EXHAUSTED / CLOSED`
**Implementation Confirmation identity:** `B0C5B7D4282F8317D4136B1F5589236C6164B3AA55BBFB0C7A9CE212AAF5736C`
**Passing independent review identity:** `B96B08CCAED2B0980D205A8ED2D85AD04984A2022D687984182019CF80A27550`
**Frozen implementation corpus cardinality:** `3`
**Frozen implementation corpus aggregate identity (raw working-tree bytes, continuity value):** `1D1B101E9B8874D1B8EAD3CA2EEE5678A1A37FB6C7E3FB3A0AF76FC7743B5B5C`
**Frozen implementation corpus aggregate identity (canonical LF manifest, identity of record):** `B0C7C52B1C21A4F5D1E61FA1B5CE783B1005D629D2CCCC1722A13210A1467F06`
**Active WP5 predecessor overlay identity (canonical LF, unchanged):** `89AA23712BE8177F8D363587343B520CB7DCC2C950BB6AE8B08E27A6D519C6F0`
**Successor work package allocated:** `NO`
**Release authority created:** `NO`

---

## A. Freeze authority and constitutional basis

Acting solely as the independent BANPU-WP7 Implementation Freeze Authority,
this act freezes the exact implementation candidate recorded as
`BANPU-WP7 IMPLEMENTATION CONFIRMED` by
[`BANPU_WP7_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP7_IMPLEMENTATION_CONFIRMATION.md),
which names Implementation Freeze as its exact next act (§28).

This authority is limited to identity binding, corpus-boundary verification,
predecessor-overlay continuity re-verification, residual carry-forward, and
creation of this record. It does not re-review the passing Third Fresh
Independent Implementation Re-Review, reinterpret any finding in any of the
three historical review records, re-perform Confirmation, modify
`backend/manage.py` or its tests/fixture, modify any WP5 predecessor source
or test file, admit new implementation, amend any existing artifact, perform
rehearsal, satisfy A11/A12/A14/A15, synchronize LM13, perform Epic Closeout,
synchronize the Decision Log or Implementation INDEX, or authorize release,
deployment, staging, or production execution.

Every prerequisite below was verified by direct inspection and independent
recomputation over current repository bytes, not accepted from prompt text or
prior conversation history.

## B. Freeze standard derived from live precedent

The closest lifecycle match, read in full for this act, is
[`BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md).
It establishes, and this record applies without inventing a stronger or
weaker standard, that Implementation Freeze requires:

- a successful, live-verified Implementation Confirmation naming Freeze as
  its next act (§C, §D there; §C, §D here);
- the exact confirmed implementation corpus identity, independently
  re-recomputed rather than transcribed (§D, §E there; §D, §E here);
- confirmation-to-freeze byte continuity for every corpus member (§E, §I
  there; §E, §I here);
- authority-chain continuity across every operative governance artifact,
  independently re-hashed (§G there; §G here);
- carry-forward, not resolution, of any residual finding (§M there; §M here);
- explicit change-control semantics binding future modification to a fresh
  lifecycle sequence (§O there; §Q here);
- explicit lifecycle exclusions (no closeout, no synchronization, no
  release, no successor allocation, no production authority) (§P there; §R
  here); and
- an exact single next constitutional act, derived from live authority text,
  not assumed (§R there; §T here).

Two necessary adaptations, extending the WP6 pattern:

1. **Three-review chain.** WP7's lineage includes three historical failed
   review records (one original, two fresh re-reviews) before the passing
   Third Fresh Re-Review, one wider than WP6's two-failure chain. This is
   addressed identically to WP6's own treatment: byte-identity,
   no-reinterpretation preservation of every historical record (§G, §K).
2. **Predecessor overlay dependency and first-computed aggregate.** WP7's
   corpus is not self-contained: two of its three evidentiary fields
   (`reconstructed_realized_pnl`, `reconstructed_holding_basis`) are supplied
   by a frozen WP5 predecessor overlay consumed by direct reference. Unlike
   WP6 — whose Second Fresh Review and Confirmation had already computed a
   raw seven-file aggregate that this Freeze only needed to canonicalize —
   the WP7 Implementation Confirmation computed **no aggregate at all** for
   the three-file WP7 corpus, by deliberate choice (its own §7: *"this record
   does not invent an aggregate the review itself did not use"*). This Freeze
   is therefore the first point at which any WP7-corpus aggregate (raw or
   canonical) is computed, under the same existing convention (§H), not a
   new one. Corpus continuity since the passing review and since Confirmation
   is proven by **per-file** identity match (§E, §I), exactly as Confirmation
   itself proved it — the newly computed aggregates are additive, not the
   basis of the continuity proof. Separately, this Freeze independently
   re-verifies the frozen WP5 predecessor overlay identity itself is
   unchanged (§O), which WP6 had no analogous predecessor dependency to
   verify.

## C. Verification of Implementation Confirmation

`docs/implementation/BANPU_WP7_IMPLEMENTATION_CONFIRMATION.md`, independently
hashed at entry: 28,795 bytes, SHA-256

```text
B0C5B7D4282F8317D4136B1F5589236C6164B3AA55BBFB0C7A9CE212AAF5736C
```

Read in full (not disposition-only) for this act. Its live disposition is
exactly `BANPU-WP7 IMPLEMENTATION CONFIRMED` (§23, §27). It independently
re-verified all seventeen entry premises (§2), bound the exact three-file
candidate with per-file identities and explicitly declined to invent an
aggregate (§7), bound the Third Fresh Independent Implementation Re-Review by
identity (§5), preserved the three-record historical review chain without
reopening any of them (§6), preserved the frozen planning identity by
continuity (§2 rows 3–5), bound the active WP5 predecessor overlay identity
unchanged (§2 row 12, §7), independently re-executed both test suites rather
than trusting the review's reported figures (§18), recorded LM13 and
rehearsal-pending treatment without falsely claiming resolution (§19–§21),
explicitly recorded `Implementation Freeze performed: NO` (header, §24), and
identified Implementation Freeze as the exact next constitutional act (§28).
All entry conditions are `SATISFIED`. This Confirmation is sufficient Freeze
input.

## D. Entry-state verification (independently re-checked)

| # | Premise | Result |
|---|---|---|
| 1 | HEAD | `SATISFIED` — `ae223a42df688563748c0e6e6cb898e66bcb3da0` |
| 2 | Staging area empty | `SATISFIED` — `git diff --cached --stat` empty |
| 3 | WP7 Allocation Record unchanged | `SATISFIED` — 19,609 bytes, `1AA24CD242C95039B81DF1A43F061B04140EA0ED5E0A2E7405AE18945900F4F1` |
| 4 | WP7 Implementation Authorization Record unchanged | `SATISFIED` — 20,963 bytes, `E7A6B235C84ABBFFF9159C7E91E2477E746B314128E1C1B1EE0B46D6E5FAEB6C` |
| 5 | Identity Ingress Design Clarification unchanged | `SATISFIED` — 17,489 bytes, `9CD583342CEF65ECC3F771A93D37ABA85327662F3D10920229552B794CA34C5D` |
| 6 | Frozen WPP unchanged | `SATISFIED` — 53,998 bytes, `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897` |
| 7 | Planning Confirmation unchanged | `SATISFIED` — 39,845 bytes, `7A44203B6E39BF5100B133DA39B96BD5A5B1059634B279B8C4706F1742A0E82D` |
| 8 | Planning Freeze unchanged | `SATISFIED` — 31,901 bytes, `E31AEC306C4CFDF0820A83BA1335DE22E0E9BE6A2ABC94AB153E85A6AB708B84` |
| 9 | Initial failed review unchanged, `FAIL` disposition intact | `SATISFIED` — 10,558 bytes, `59D39B92DDDB8BFAACE785C49D4453EC3F423C85C2D8FC15B8E025DF601DDF74` |
| 10 | First fresh re-review unchanged, `FAILED` disposition intact | `SATISFIED` — 18,810 bytes, `C79564232FE269488AB3D9EDB4AE38B3B265238F2447AB6C038BEDF28D2BA6BD` |
| 11 | Second fresh re-review unchanged, `FAILED` disposition intact | `SATISFIED` — 17,793 bytes, `F631DE4459BDC0B02392629C955881741A25388726FACC4BD30C3CB3E898878D` |
| 12 | Third Fresh Independent Re-Review unchanged, `PASSED` disposition intact | `SATISFIED` — 18,998 bytes, `B96B08CCAED2B0980D205A8ED2D85AD04984A2022D687984182019CF80A27550` |
| 13 | Implementation Confirmation exists at exact disposition `BANPU-WP7 IMPLEMENTATION CONFIRMED` | `SATISFIED` — §C above |
| 14 | Confirmation binds the exact three-member corpus (per-file, no aggregate) | `SATISFIED` — Confirmation §7 |
| 15 | No implementation/test byte changed after Confirmation | `SATISFIED` — all three corpus files reproduce the exact per-file identities recorded by the Confirmation (§E below) |
| 16 | Active WP5 predecessor overlay unchanged | `SATISFIED` — canonical-LF `89AA23712BE8177F8D363587343B520CB7DCC2C950BB6AE8B08E27A6D519C6F0`, independently re-derived from live bytes, §O |
| 17 | LM13 unchanged | `SATISFIED` — `backend/tests/test_position_conversion_live.py`, 85,502 bytes, `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8` |
| 18 | Decision Log unchanged | `SATISFIED` — 436,520 bytes, `3BE8084DDE1813BF3B4ED7FF0C655C553EC3022B8554162E5585A44B8282EC50`; every `WP7` occurrence independently confirmed to be an unrelated M38/M42/M43/M44 milestone-numbered label, not `BANPU-WP7` |
| 19 | Implementation INDEX unchanged | `SATISFIED` — 55,779 bytes, `5A1DB032AB4D35B0216A3346E7C07CE120E2067783461182872A75F1F1C466FC`; lines 289–291 remain stale pre-allocation text (*"WP7 remains `NOT ALLOCATED` and `NOT AUTHORIZED`"*), confirming no `BANPU-WP7` synchronization has occurred, not a contradiction |
| 20 | No prior WP7 Implementation Freeze artifact exists | `SATISFIED` — no `BANPU_WP7_IMPLEMENTATION_FREEZE_RECORD.md` existed before this act (directory search) |
| 21 | No WP7 Epic Closeout artifact exists | `SATISFIED` — no `BANPU_WP7_EPIC_CLOSEOUT.md` |
| 22 | No BANPU-WP8/M46 allocation or authorization exists | `SATISFIED` — no `BANPU_WP8_*` artifact exists anywhere; the `M46_*` files are a distinct milestone-numbered lineage, unrelated to BANPU work-package numbering |
| 23 | No release/deployment/production mutation occurred | `SATISFIED` — `git status` shows no snapshot, migration, or deployment artifact touched |
| 24 | Nothing is staged | `SATISFIED` — `git diff --cached --name-only` returns empty |

All twenty-four entry premises are satisfied. Freeze proceeds.

## E. Verification of the confirmed implementation corpus (raw bytes)

Each of the three candidate files was independently re-hashed from live
working-tree bytes and compared against the Confirmation's §7 table. This is
the same raw-byte convention the Third Fresh Review and the Confirmation
already used to bind this candidate — reproduced here to prove continuity.

| # | Frozen artifact | Status | Raw bytes | Confirmed SHA-256 (raw) | Result |
|---|---|---|---:|---|---|
| 1 | `backend/manage.py` | modified | 262,795 | `710B5E2CBF22FD6D774554C601201CD848BF663F89492F025C10CBD1E5E412F7` | `EXACT` |
| 2 | `backend/tests/test_apply_position_conversion_cli.py` | new | 55,466 | `CEE866EABAAA24C5B2268B5CDDEE77710BA6FB591CB74080A80D2422A976B60A` | `EXACT` |
| 3 | `backend/tests/fixtures/banpu_wp7_position_conversion_manifest.json` | new | 1,247 | `2B843A3ECFBB85AA9E1A6882CAD7DE6AA3690A94627BD7DBF4F317ED802A9E03` | `EXACT` |

Recomputed raw aggregate (`path<TAB>SHA256<TAB>bytes<LF>` manifest, UTF-8,
trailing `\n`, this table's order): `1D1B101E9B8874D1B8EAD3CA2EEE5678A1A37FB6C7E3FB3A0AF76FC7743B5B5C`
— computed for the first time by this Freeze (§B.2). All three: `EXACT`.
Zero mismatches. Corpus cardinality: `3`. Missing artifacts: `0`. Unauthorized
included artifacts: `0`.

## F. Frozen planning identity (continuity re-check)

| Frozen member | SHA-256 (recomputed) | Bytes |
|---|---|---:|
| `docs/implementation/BANPU_WP7_WORK_PACKAGE_PLAN.md` | `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897` | 53,998 |

Exact match against the Planning Freeze Record's own recorded identity and
against the Confirmation §2 row 3. This freeze does not alter or re-bind the
planning corpus; it exists under a separate, already-frozen convention and is
reverified here only for continuity.

## G. Authority-chain continuity

Every operative WP7 governance artifact between Allocation and this Freeze
was independently re-hashed from live bytes.

| Operative artifact | Bytes | SHA-256 | Result |
|---|---:|---|---|
| Allocation Record | 19,609 | `1AA24CD242C95039B81DF1A43F061B04140EA0ED5E0A2E7405AE18945900F4F1` | `EXACT` |
| Implementation Authorization Record | 20,963 | `E7A6B235C84ABBFFF9159C7E91E2477E746B314128E1C1B1EE0B46D6E5FAEB6C` | `EXACT` |
| Identity Ingress Design Clarification | 17,489 | `9CD583342CEF65ECC3F771A93D37ABA85327662F3D10920229552B794CA34C5D` | `EXACT` |
| Work Package Plan (frozen) | 53,998 | `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897` | `EXACT` |
| Planning Confirmation | 39,845 | `7A44203B6E39BF5100B133DA39B96BD5A5B1059634B279B8C4706F1742A0E82D` | `EXACT` |
| Planning Freeze Record | 31,901 | `E31AEC306C4CFDF0820A83BA1335DE22E0E9BE6A2ABC94AB153E85A6AB708B84` | `EXACT` |
| Initial Independent Implementation Review | 10,558 | `59D39B92DDDB8BFAACE785C49D4453EC3F423C85C2D8FC15B8E025DF601DDF74` | `EXACT` |
| First Fresh Independent Implementation Re-Review | 18,810 | `C79564232FE269488AB3D9EDB4AE38B3B265238F2447AB6C038BEDF28D2BA6BD` | `EXACT` |
| Second Fresh Independent Implementation Re-Review | 17,793 | `F631DE4459BDC0B02392629C955881741A25388726FACC4BD30C3CB3E898878D` | `EXACT` |
| Third Fresh Independent Implementation Re-Review | 18,998 | `B96B08CCAED2B0980D205A8ED2D85AD04984A2022D687984182019CF80A27550` | `EXACT` |
| Implementation Confirmation | 28,795 | `B0C5B7D4282F8317D4136B1F5589236C6164B3AA55BBFB0C7A9CE212AAF5736C` | `EXACT` |

All eleven: `EXACT`. The chain is complete and uncontradicted. The
acceptance matrix (A1–A19) is not reinterpreted by this act; it remains
exactly as the Third Fresh Review and the Confirmation recorded it. The two
historical failed reviews and the original failed review are not reopened,
rewritten, or reinterpreted.

## H. Frozen corpus manifest — canonical identity and convention

### H.1 Convention (existing, not invented)

Individual candidate identity (§E) is the raw working-tree byte hash,
matching the identity the Third Fresh Review and the Confirmation already
bound. For the **aggregate** corpus identity this record applies the
Git-canonical LF convention established by
[`BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md`](BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md)
§4, continued by every subsequent WP freeze record through
[`BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md)
§H — SHA-256 over file bytes with every line's trailing `\r` stripped.
Independently confirmed: `core.autocrlf=true` on this branch. Byte-level
inspection (not line-count heuristics) of all three corpus files found:
`backend/manage.py` carries 5,838 CRLF pairs in the working tree;
`backend/tests/test_apply_position_conversion_cli.py` and
`backend/tests/fixtures/banpu_wp7_position_conversion_manifest.json` are
already pure LF (zero `\r` bytes each) because both were written directly
rather than checked out through Git's `core.autocrlf` conversion. Canonical
LF normalization is applied uniformly to all three regardless.

Manifest: for each corpus row, in the §E table order, the line
`<repo-relative-path><TAB><SHA-256 uppercase hex><TAB><canonical byte count>`,
lines joined by `\n` with one trailing `\n`, encoded UTF-8, then SHA-256 —
the identical algorithm used by `BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md`
§H.1.

### H.2 Canonical (LF) per-file identities

| # | Frozen artifact | CRLF in working tree | Canonical bytes (LF) | Canonical SHA-256 (LF) |
|---|---|---|---:|---|
| 1 | `backend/manage.py` | yes (5,838 pairs) | 256,957 | `E07B8EB3C837A613F2E1B29880682FDB73C6C7B1E301D696F03F10C1AC6926AB` |
| 2 | `backend/tests/test_apply_position_conversion_cli.py` | no (already LF) | 55,466 | `CEE866EABAAA24C5B2268B5CDDEE77710BA6FB591CB74080A80D2422A976B60A` |
| 3 | `backend/tests/fixtures/banpu_wp7_position_conversion_manifest.json` | no (already LF) | 1,247 | `2B843A3ECFBB85AA9E1A6882CAD7DE6AA3690A94627BD7DBF4F317ED802A9E03` |

Files 2 and 3 legitimately show identical raw and canonical identities
because they contain no CRLF to normalize — the expected effect for
LF-native files under the same normalization rule, not an inconsistency,
exactly as WP6 §H.2 recorded for its own two LF-native new files. Every file
ends with a newline, so LF normalization is unambiguous for all three.

### H.3 Aggregate identity

```text
B0C7C52B1C21A4F5D1E61FA1B5CE783B1005D629D2CCCC1722A13210A1467F06
```

Independently computed from the three canonical rows in §H.2, in that exact
order. This is the frozen aggregate corpus identity of record; a different
enumeration order of the same three members would yield a different
aggregate. Per §B.2, this is the **first** time any WP7-corpus aggregate
(raw or canonical) has been computed in the BANPU-WP7 lifecycle — the
Third Fresh Review and the Confirmation both bound only per-file identities.
Corpus continuity (§I) rests on the per-file match, not on aggregate
recomputation, exactly as Confirmation itself established.

## I. Review-to-Confirmation-to-Freeze continuity

```text
Implementation corpus reviewed as PASS (per-file)  = {710B5E2C…412F7, CEE866EA…A60A, 2B843A3E…9E03}
Implementation corpus confirmed (per-file)          = {710B5E2C…412F7, CEE866EA…A60A, 2B843A3E…9E03}
Current implementation corpus (per-file)            = {710B5E2C…412F7, CEE866EA…A60A, 2B843A3E…9E03}
Implementation corpus proposed for Freeze (raw aggregate, first computed)       = 1D1B101E9B8874D1B8EAD3CA2EEE5678A1A37FB6C7E3FB3A0AF76FC7743B5B5C
Implementation corpus proposed for Freeze (canonical LF, identity of record)   = B0C7C52B1C21A4F5D1E61FA1B5CE783B1005D629D2CCCC1722A13210A1467F06
```

All three per-file sets identical, proven by independently recomputed
per-file SHA-256 (§E), not inferred from filenames or `git status` alone. No
implementation or test byte changed after the passing review or after
Confirmation. The two new aggregate values are additive identities
established by this Freeze act under existing binding precedent (§H) — they
do not replace or contradict the per-file continuity chain; they fix the
frozen corpus against future checkout-state drift. The Third Fresh
Independent Implementation Re-Review and the Implementation Confirmation
also both remain byte-identical (§G) to what each successor artifact
consumed. Continuity is proven.

## J. Acceptance-evidence continuity

This freeze does not re-run the acceptance matrix. Because §E and §I prove
zero implementation-byte drift since the passing review and since
Confirmation, the acceptance evidence the Third Fresh Review established and
the Confirmation summarized transfers unmodified to the frozen candidate:

- `PASS`: A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A13, A16, A17, A18, A19
  (15 rows) — none reopened;
- `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED`: A11, A12, A14, A15
  (4 rows) — not converted to `PASS` by this act;
- `FAIL`: none;
- `INSUFFICIENT EVIDENCE`: none;
- focused WP7 suite, as independently re-executed by the Confirmation:
  71 passed, 0 failed, 536 warnings;
- governing regression corpus, as independently re-executed by the
  Confirmation: 581 passed, 1 failed (LM13, sole failure), 1935 warnings;
- combined: 652 passed, 1 failed — the repository is **not** claimed fully
  green by this Freeze, exactly as the Confirmation did not claim it.

This Freeze does not independently re-execute either suite; §E/§I already
prove the corpus is byte-identical to what the Confirmation tested, so the
Confirmation's independently re-executed results transfer without needing a
third execution.

## K. LM13 and non-blocking observation treatment

Carried forward unchanged, not re-adjudicated by this act:

`STALE PREDECESSOR TEST — WP7 AUTHORITY SUPERSEDES CLI PORTION`

- Not current WP7 implementation nonconformance — the focused suite and
  governing corpus otherwise pass completely (§J).
- The public/API/frontend prohibition the test partially still protects
  remains intact; §L below independently reconfirms no route, `main.py`
  endpoint, router, or frontend conversion action exists.
- It remains separate repository-synchronization debt, tracked but not
  discharged.
- This Freeze does not modify, waive, or discharge LM13, and does not
  falsely claim the repository is fully green (§J).

## L. WP5 predecessor-surface preservation

Independently re-verified against live bytes, not accepted from the
Confirmation's report alone:

- **Overlay identity unchanged.** `backend/services/portfolio_rebuilder.py`
  (raw 129,960 bytes, `64026DDA722B949205F4FB3E875396BBBCC11C7EA6B4E10CC6AF87BB5AFF7947`)
  and `backend/tests/test_portfolio_rebuilder.py` (raw 117,056 bytes,
  `ABC8C406AA91DE405E4C1B1A9253E3BB99134EB5B072DAC41ACD136927F1B5D0`) both
  reproduce exactly the raw identities recorded by
  [`BANPU_WP5_FRESH_IMPLEMENTATION_FREEZE_ORDINARY_HOLDING_BASIS_EXPOSURE.md`](BANPU_WP5_FRESH_IMPLEMENTATION_FREEZE_ORDINARY_HOLDING_BASIS_EXPOSURE.md)
  (17,390 bytes, `33B7898DCACF71CDDEF352AD6D4898F69C500A01E42B20D0371B7A7C52360176`).
- **Canonical-LF overlay aggregate independently reproduced.** Applying the
  same convention (§H.1) to the two predecessor files' canonical-LF
  identities (`2F035255181354E24CBA5FEF59BF23C85E2C9FE761E488778AFE2EBD81C936E1`,
  127,289 bytes; `13D8AB7991D4C7DA2538D95B869C9B7E5F3DC5A7DC902EE1F1ACD39CDC292E23`,
  114,848 bytes, in that order) independently reproduces
  `89AA23712BE8177F8D363587343B520CB7DCC2C950BB6AE8B08E27A6D519C6F0` exactly
  — not transcribed from the Confirmation, recomputed from first principles
  in this act.
- **Both frozen predecessor fields remain consumed by direct reference.**
  `reconstructed_realized_pnl` and `reconstructed_holding_basis` remain
  present and populated in the live, byte-verified `portfolio_rebuilder.py`
  (`RebuildResult` fields), and remain read directly by `backend/manage.py`
  (§E, §H — the frozen WP7 `manage.py` identity itself proves no
  WP7-local replacement formula was substituted, since that would have
  changed the frozen byte identity).
- **No unauthorized WP7-local replacement of predecessor accounting
  evidence exists.** Exact ordinary-basis `Decimal` semantics (direct
  frozen-map comparison, no `shares × avg_cost` reconstruction, no float
  conversion or tolerance) and direct realized-P&L comparison (no WP7-local
  formula, no tolerance) are properties of the frozen `manage.py` bytes
  themselves (§E) and were independently confirmed present by both the
  Third Fresh Review (§12, §14) and the Confirmation (§11, §12); this Freeze
  adds no new technical determination, it fixes the byte identity that
  carries those properties.
- This Freeze does not modify, re-derive, or reinterpret any WP5 source,
  test, or governance artifact. WP5 remains frozen exactly as its own
  Freeze record states.

## M. Replay fail-closed/parity properties frozen

The following properties, established by the Third Fresh Review and
restated by the Confirmation (§9–§17 there), are properties of the exact
frozen `backend/manage.py` byte identity (§E, §H) and are therefore fixed by
this act, not re-verified from scratch:

- `success=False` fails closed to sanitized `REPLAY_FAILED`.
- A populated (non-empty, non-whitespace-only) canonical `RebuildResult.error`
  also fails closed to `REPLAY_FAILED`, evaluated after the `success=False`
  check.
- A raised exception during replay fails closed to sanitized
  `REPLAY_EXCEPTION`.
- Holdings/full identity evidence is compared by stable `report_symbol`,
  exact set equality.
- Exact ordinary basis is compared as raw frozen `Decimal`, exact key-set
  and value equality, no tolerance.
- Reconstructed cash completeness/parity: `None` on either side fails
  closed; `0`/`0` is valid; no fallback-to-zero path; unequal or sub-cent
  differences fail.
- Realized P&L completeness/parity: direct `reconstructed_realized_pnl`
  comparison, exact float equality, no tolerance; a missing value fails.
- Conversion-specific basis evidence (`B0`/`Bs`) remains separately
  preserved with its own `0.01` tolerance, kept distinct from
  ordinary-basis exactness.
- Pre-commit mismatch prevents commit.
- Post-commit anomaly (failure, canonical error, exception, incomplete
  evidence, or mismatch) truthfully retains `Status: applied`, emits a
  non-zero `CRITICAL` outcome, withholds cache/rebuild instructions, and
  does not claim automatic rollback.
- Replay toggle/session state is restored on every path, including
  injected-failure counterexamples.
- Reporting remains sanitized (no raw exception/result-error text or
  provider payload reaches stdout/stderr) and deterministic across dry-run,
  failed-preflight, successful-commit, `already_applied`, conflict, and
  post-commit-anomaly states.

Because §E proves the frozen `manage.py` bytes are unchanged since the
passing review, all of the above properties transfer to the frozen candidate
without re-execution. This Freeze does not weaken, strengthen, or
reinterpret any of them.

## N. CLI/public/API/frontend boundary

Independently reconfirmed against the frozen `backend/manage.py` bytes and a
live repository search: `--portfolio`/`-p` remains required with no default;
the target portfolio resolves from persisted state, not caller-supplied
identity; `ws_id` derives from the resolved `Portfolio.workspace_id`; no
route, `main.py` endpoint, router, or frontend conversion action exists for
position conversion. This boundary is unchanged from the Third Fresh Review's
§21 and the Confirmation's §8, and is fixed — not re-created — by this
Freeze.

## O. Scope and authority continuity

Independently re-checked against the Implementation Authorization Record and
the Confirmation's §22–§24, unchanged since Confirmation:

| Check | Result |
|---|---|
| All production files authorized | `SATISFIED` — `backend/manage.py` within the authorized surface |
| All test/fixture files authorized | `SATISFIED` — both within the authorized surface |
| Unauthorized file | `NONE` |
| Schema/model/migration change | `NONE` |
| New CLI/operator authority | `NONE` created |
| Production-data mutation authority | `NONE` created |
| Release/deployment authority | `NONE` created |
| BANPU-WP8/M46 authority | `NONE` — no `BANPU_WP8_*` artifact exists; `M46_*` is an unrelated milestone lineage |
| Widening between Confirmation and Freeze | `NONE` — corpus membership (§E) and scope (this table) are identical to the Confirmation's |

Scope and authority remain entirely within the frozen implementation
authorization; no widening occurred between Confirmation and Freeze.

## P. Residual preservation

This freeze carries forward, and does not discharge, reassign, or
reinterpret, any pre-existing residual:

- Rehearsal-dependent acceptance (**A11**, **A12**, **A14**, **A15**) and the
  WP7 portions of **MINOR-5** and **NEW-MINOR-A** remain
  `NOT EVALUATED — REHEARSAL ENVIRONMENT REQUIRED` / pending, exactly as the
  Third Fresh Review and the Confirmation left them; no rehearsal was
  performed by this act.
- **LM13** remains separate predecessor-test synchronization debt (§K),
  untouched.
- `MINOR-2`, `POSITION_CONVERSION_REBUILD_BOUNDARY`, `PD-3`, and any other
  WP1–WP6 carried residual or observation are outside this corpus and
  untouched by this act.
- WP7 carries forward **zero** WP7-native residuals beyond the four
  rehearsal-pending acceptance rows and the two named pending items above:
  no new residual was created by the Confirmation (its §26) and none is
  created by this act.

## Q. Frozen implementation corpus (definition)

The exact frozen BANPU-WP7 implementation corpus, immutable by content
identity:

**Production (1):**
- `backend/manage.py`

**Tests/fixtures (2):**
- `backend/tests/test_apply_position_conversion_cli.py`
- `backend/tests/fixtures/banpu_wp7_position_conversion_manifest.json`

Per-file identities: §E (raw, continuity) and §H.2 (canonical LF, identity of
record). Manifest convention: §H.1. Aggregate identity of record:
`B0C7C52B1C21A4F5D1E61FA1B5CE783B1005D629D2CCCC1722A13210A1467F06` (§H.3),
bound only because independently reproduced.

**Frozen predecessor dependency (not a WP7 corpus member, bound separately):**
- `backend/services/portfolio_rebuilder.py` and
  `backend/tests/test_portfolio_rebuilder.py`, under the frozen WP5
  canonical-LF overlay identity `89AA23712BE8177F8D363587343B520CB7DCC2C950BB6AE8B08E27A6D519C6F0`
  (§L). WP7 consumes this overlay by direct reference; it does not own or
  refreeze it.

Governance and review artifacts (Allocation, Authorization, Identity Ingress
Clarification, WPP, Planning Confirmation, Planning Freeze, all three
historical reviews, the passing review, and the Implementation Confirmation)
are cited as evidence in §D, §F, and §G but are **not** members of the
frozen implementation corpus; live WP6 precedent (§N there) treats only
implementation/test/fixture source files as freeze members, and this record
applies that same boundary without extension.

## R. Change-control rule

Derived from precedent (`BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md` §9,
continued by every subsequent WP freeze record through WP6): no future
process may modify a frozen implementation member merely to make an identity
match a particular checkout's line-ending state, and no silent modification
can preserve the frozen identity. Any future material change to any of the
three frozen WP7 members, or any future material change to the frozen WP5
predecessor overlay that WP7 depends on, requires, in order: a new
authorized correction/amendment path under fresh implementation
authorization scoped to that change; a fresh independent implementation
review; a fresh Implementation Confirmation; and a fresh Implementation
Freeze. This record does not itself create that authorization — it only
states the rule that would govern if such a change were ever proposed.

## S. Excluded effects

This freeze creates **no** epic closeout, **no** Decision Log
synchronization, **no** Implementation INDEX synchronization, **no** release
authority, **no** deployment authority, **no** production execution
authority, **no** BANPU-WP8 or M46 allocation/authorization/planning
authority, and **no** rehearsal-satisfaction authority.

It additionally does **not**:

- reopen, modify, or reinterpret implementation or test code;
- amend planning, allocation, authorization, identity ingress, review,
  Confirmation, or any other governance artifact;
- modify any of the three historical failed reviews or the passing
  re-review artifact;
- resolve, weaken, or expand LM13, `MINOR-2`,
  `POSITION_CONVERSION_REBUILD_BOUNDARY`, `PD-3`, or any WP1–WP6 residual
  (§P);
- modify WP1 through WP6, WP5's predecessor overlay, or any of their frozen
  corpora;
- perform rehearsal or convert A11/A12/A14/A15 to `PASS`;
- commit, push, merge, or stage any change.

Implementation authority for BANPU-WP7 is **exhausted and closed**. No
additional implementation work may enter this candidate.

**Production execution is not authorized by this act: `NO`.** The
Implementation Authorization Record's excluded-surface scope and the
Confirmation's §22 lifecycle boundary already establish that production
execution, if any, is gated by separate, later, rehearsal-dependent
production-deployment authority; this Freeze does not create, imply, or
advance that authority.

## T. Repository verification

| # | Verification | Result |
|---|---|---|
| 1 | All three frozen candidate raw hashes remain exact (§E) | `SATISFIED` |
| 2 | Canonical LF per-file identities and aggregate independently computed (§H) | `SATISFIED` — `B0C7C52B1C21A4F5D1E61FA1B5CE783B1005D629D2CCCC1722A13210A1467F06` |
| 3 | Third Fresh Independent Implementation Re-Review remains exactly `B96B08CC…7550` (§G) | `SATISFIED` |
| 4 | Implementation Confirmation remains byte-identical to its pre-freeze identity (§C) | `SATISFIED` |
| 5 | All eleven authority-chain artifacts remain byte-identical (§G) | `SATISFIED` |
| 6 | All three historical failed/re-review records remain byte-identical, unedited (§G) | `SATISFIED` |
| 7 | Frozen planning identity unchanged (§F) | `SATISFIED` |
| 8 | Active WP5 predecessor overlay identity independently reproduced (§L) | `SATISFIED` — `89AA2371…6C6F0` |
| 9 | No implementation or test file changed by this act | `SATISFIED` — only this record was created |
| 10 | No new implementation path appeared in the corpus | `SATISFIED` — cardinality remains 3 |
| 11 | No frozen WP1–WP6 or WP5-overlay artifact changed | `SATISFIED` — untouched by this act |
| 12 | Decision Log and Implementation INDEX untouched | `SATISFIED` — not intrinsic to freeze per §S |
| 13 | Relative links resolve | `SATISFIED` — verified against live file paths |
| 14 | `git diff --check` | `PASS` — exit `0` |
| 15 | `git diff --cached --check` | `PASS` — exit `0` |
| 16 | Nothing staged | `SATISFIED` — `git diff --cached --name-only` empty |
| 17 | No commit created | `SATISFIED` |
| 18 | Trailing whitespace in this record | `NONE` |

## T2. Resulting WP7 constitutional state

- WP7 Planning remains `CONFIRMED / FROZEN`.
- WP7 Implementation is now `BANPU-WP7 IMPLEMENTATION FROZEN`.
- Implementation authority for WP7 is `EXHAUSTED / CLOSED`.
- WP7 is **not** thereby closed out.
- LM13 remains separate predecessor-test synchronization debt, untouched.
- Rehearsal-dependent acceptance (A11/A12/A14/A15, WP7 portions of
  MINOR-5/NEW-MINOR-A) remains pending, untouched.
- The frozen WP5 predecessor overlay remains unchanged and is not refrozen
  or re-owned by this act.
- No release, deployment, production, WP8, or M46 authority exists.
- No implementation, test, or fixture file was modified by this act.
- No staging, commit, push, or merge was performed by this act.

## U. Exact next constitutional act

Determined from the governing WP7 authority corpus and live WP5/WP6 lineage
precedent, not assumed. The Third Fresh Review's own §34 named "BANPU-WP7
Implementation Confirmation" as its successor (performed by
`BANPU_WP7_IMPLEMENTATION_CONFIRMATION.md`). The Confirmation's own §28
named "BANPU-WP7 Implementation Freeze" as its successor (now performed by
this record).
[`BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP6_IMPLEMENTATION_FREEZE_RECORD.md)
§R — the closest live freeze precedent — names Epic Closeout as its own
exact next act, applying the same BANPU-WP1 through WP6 sequence of
independent review → Implementation Confirmation → Implementation Freeze →
Epic Closeout → Decision Log synchronization → Implementation INDEX
synchronization.

**Exact next constitutional act: `BANPU-WP7 Epic Closeout`.**

This record performs no part of that act.

## Final disposition

**`BANPU-WP7 IMPLEMENTATION FROZEN`**

at Implementation Confirmation identity
`B0C5B7D4282F8317D4136B1F5589236C6164B3AA55BBFB0C7A9CE212AAF5736C`,
passing independent review identity
`B96B08CCAED2B0980D205A8ED2D85AD04984A2022D687984182019CF80A27550`,
and frozen implementation corpus identity
`1D1B101E9B8874D1B8EAD3CA2EEE5678A1A37FB6C7E3FB3A0AF76FC7743B5B5C` (raw,
continuity) /
`B0C7C52B1C21A4F5D1E61FA1B5CE783B1005D629D2CCCC1722A13210A1467F06`
(canonical LF, identity of record) over three files, consuming the frozen
WP5 predecessor overlay identity
`89AA23712BE8177F8D363587343B520CB7DCC2C950BB6AE8B08E27A6D519C6F0` by
direct reference.

The implementation candidate is constitutionally fixed. LM13, `MINOR-2`,
`POSITION_CONVERSION_REBUILD_BOUNDARY`, `PD-3`, rehearsal-dependent
acceptance (A11/A12/A14/A15), and the WP7 portions of MINOR-5/NEW-MINOR-A
remain exactly as previously recorded — none is discharged, reassigned, or
reinterpreted by this act. No release, deployment, production execution,
WP8, or M46 authority is created or implied by this act.
