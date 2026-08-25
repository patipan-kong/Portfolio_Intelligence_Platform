# BANPU-WP5 — Fresh Implementation Confirmation: RebuildResult Realized P&L Exposure

**Artifact class:** Additive fresh Implementation Confirmation record for a bounded amendment  
**Confirmation date:** 2026-08-19  
**Issuing role:** Independent BANPU-WP5 Implementation Confirmation Authority  
**Amendment Authorization:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_REALIZED_PNL_EXPOSURE.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_REALIZED_PNL_EXPOSURE.md), 18,182 bytes, SHA-256 `DFFFF800D9636AB5266846FD750FCE3CD3DF6AFA40EAB3EB43219F280D7D8336`  
**Fresh independent review:** [`BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_REALIZED_PNL_EXPOSURE.md`](BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_REALIZED_PNL_EXPOSURE.md), 21,189 bytes, SHA-256 `3B3E836377269CAB1E352CC653F4C79E133525761C7ACC097B5A8C3CF8085925`  
**Independent-review disposition:** `BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION REVIEW PASSED`  
**Disposition:** `BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION CONFIRMED`  
**Fresh Implementation Freeze performed by this act:** `NO`  
**WP7 correction resumed by this act:** `NO`  
**Production/release/deployment authority created:** `NONE`

---

## 1. Purpose and confirmation boundary

This record performs only the fresh Implementation Confirmation required for the successor-triggered, bounded `RebuildResult` realized-P&L exposure amendment. It confirms the exact two-file amended implementation identities in §6 under the exact Authorization and fresh independent-review identities named above.

This record does not modify or re-review implementation or tests, perform the fresh Implementation Freeze, reopen unrelated portions of historical WP5, resume the WP7 correction, alter LM13, synchronize the Decision Log or Implementation INDEX, or authorize production execution, release, deployment, staging, commit, or push. Confirmation applies only to the exact bytes bound here. Any later change to either implementation member requires a new competent lifecycle determination.

## 2. Confirmation entry-state verification

The following premises were independently re-established from live repository state before this record was created:

| Premise | Live result |
|---|---|
| HEAD baseline | `ae223a42df688563748c0e6e6cb898e66bcb3da0` — exact expected baseline |
| Staging area | empty |
| Amendment Authorization | present, byte-identical at `DFFFF800…8336`; disposition re-read as `BANPU-WP5 REALIZED-PNL RESULT-SURFACE AMENDMENT AUTHORIZED` |
| Amended corpus membership | exactly `backend/services/portfolio_rebuilder.py` and `backend/tests/test_portfolio_rebuilder.py` |
| Reviewed implementation identities | exact matches to the fresh independent review: `409FBC22…F429` and `F42FFF20…8B25` |
| Fresh independent-review record | present, byte-identical at `3B3E8363…5925`; disposition re-read as `BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION REVIEW PASSED` |
| Post-review implementation mutation | none; both current hashes equal the reviewed hashes and the live diff remains the reviewed two-file diff |
| Prior amendment Confirmation or Freeze | none found before this act |
| Original WP5 Freeze and Closeout | unchanged at `8FE512A2…0E54` and `46AC7C4B…3E4A` respectively |
| WP7 WPP / Planning Confirmation / Planning Freeze / failed review | unchanged at `9A5F4F79…2897`, `7A44203B…E82D`, `E31AEC30…8B84`, and `59D39B92…DF74` |
| WP7 consumption of the new field | absent; `backend/manage.py` contains no `reconstructed_realized_pnl` reference |
| LM13 | governing `backend/tests/test_position_conversion_live.py` unchanged; SHA-256 `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8` |
| Decision Log / Implementation INDEX | unchanged; neither is modified in the working tree |
| Production/release/deployment act | none found or performed; no staging, migration, deployment artifact, or production mutation exists in this act |

No identity drift, missing authority, post-review mutation, or contradictory lifecycle state was found. The fail-closed entry gate passes.

## 3. Confirmation precedent

The directly applicable form is the additive standalone record in [`BANPU_WP5_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP5_IMPLEMENTATION_CONFIRMATION.md): independently re-hash the exact candidate and passing review, confirm authority-chain continuity and review sufficiency, preserve historical records, state the narrow disposition, deny Freeze/release/production effects, and name the exact next constitutional act.

The completed D7 amendment lineage supplies the relevant amendment-specific discipline: an amendment is additive; each successor act binds exact predecessor identities; earlier frozen/closed records remain historically intact; and the act grants no consequences belonging to a later binding/freeze step. D7's mechanical-continuity substance and its planning-stage reapproval complications are not imported. Here, the operative post-freeze rule is WP5 Implementation Freeze §P, which requires fresh authorization, independent review, Confirmation, and fresh Freeze for a material change to a frozen member.

## 4. Authority-chain verification

The complete operative chain is present and uncontradicted:

1. original WP5 implementation authority, Confirmation, Freeze, and Closeout established the historical frozen/closed corpus;
2. frozen WP7 requires both replay modes to compare holdings, basis, cash, and realized P&L, while prohibiting WP7 ownership of `portfolio_rebuilder.py`;
3. the WP7 failed implementation review exposed the missing result-surface observation;
4. the Realized-P&L Result-Surface Amendment Authorization created exactly one bounded WP5 correction path;
5. the bounded implementation changed exactly two authorized files;
6. the fresh independent implementation review examined those exact bytes and passed; and
7. this record confirms those exact reviewed bytes.

No constitutional act is missing before Confirmation. The remaining required act is the fresh Implementation Freeze in §20; it is not performed here.

## 5. Exact confirmed amendment scope

The production change remains exactly two additive lines in `backend/services/portfolio_rebuilder.py`:

```python
reconstructed_realized_pnl: float | None = None
```

declared as the final, defaulted `RebuildResult` field, and:

```python
result.reconstructed_realized_pnl = _f(final_state.cumulative_realized_pnl)
```

assigned at the existing successful Stage-1 result boundary immediately after reconstructed cash and holdings count.

Test changes remain confined to `backend/tests/test_portfolio_rebuilder.py`: one default assertion and focused successful-zero/fetch-free, ordinary-SELL, and conversion-cash-in-lieu cases. No other production or test surface is confirmed by this record.

## 6. Cryptographic identities bound

| Bound artifact | Bytes | SHA-256 |
|---|---:|---|
| Amendment Authorization | 18,182 | `DFFFF800D9636AB5266846FD750FCE3CD3DF6AFA40EAB3EB43219F280D7D8336` |
| `backend/services/portfolio_rebuilder.py` | 129,464 | `409FBC22313A98B24D9A23FFE3754CBA2584A702473C36CB2D51A36EDC19F429` |
| `backend/tests/test_portfolio_rebuilder.py` | 108,142 | `F42FFF2084A568CE165D0F58B0C3EA0109881E38736BB9CE299E330F49808B25` |
| Fresh independent implementation review | 21,189 | `3B3E836377269CAB1E352CC653F4C79E133525761C7ACC097B5A8C3CF8085925` |

The two implementation identities are exactly those reviewed as PASS. There was no implementation or test byte change between that review and this Confirmation.

## 7. Canonical provenance confirmation

Independent live-source inspection re-established that `cumulative_realized_pnl` is predecessor functionality, introduced in commit `3a0bbe726dd4f2de67a8e6d3dbe227b4b5b27f44` on 2026-08-10, before this amendment and the 2026-08-19 WP7 planning corpus.

The pre-existing `_PortfolioState` initializes the value as `Decimal("0")`. The pre-existing `SELL` branch adds canonical `ctx.realized_pnl` (or zero), and the pre-existing `POSITION_CONVERSION` branch adds `payload.cash_in_lieu.realized_pnl` (or zero). The amendment changes neither accumulation site nor any formula. It only reads the final canonical replay state into a result field.

## 8. Stage and numeric semantics confirmation

- A successful Stage 1 assigns the field before snapshot/provider stages.
- A successful replay without realized events assigns `0.0`.
- A failure or return before successful Stage-1 completion retains the trailing field's `None` default.
- `skip_snapshots=True` does not bypass the Stage-1 assignment and therefore still exposes the result.
- Provider-dependent `_build_price_matrix` remains later and snapshot-gated; no provider fetch is required for this result.
- `_f()` remains the existing `Decimal` quantization and `ROUND_HALF_UP` conversion convention already used by adjacent reconstructed cash.
- No new rounding, tolerance, or WP7-specific numeric rule was introduced.

## 9. Compatibility confirmation

All repository `RebuildResult` construction sites were re-enumerated. Production has two keyword constructions; the existing WP7 focused test has keyword constructions; registry parity and rebuilder tests use keyword construction. No positional construction was found. Existing callers omit the new trailing/defaulted field safely.

No whole-`RebuildResult` equality assumption, exact dataclass-field-set assertion, `asdict()`/`__dict__` use, generic JSON serialization, API/router exposure, frontend contract, persistence model, schema, or migration consumes this dataclass. Existing named consumers continue to read their existing fields. The additive field therefore creates no repository compatibility work.

## 10. Accounting, replay, and provider non-interference

Direct diff inspection confirms that the production file contains only the field declaration and result assignment in §5. The amendment does not alter realized-P&L calculation, cost basis, BUY/SELL/conversion semantics, cash-in-lieu accounting, replay ordering, canonicalization, reconciliation, provider fetching, snapshots, registry behavior, cache behavior, persistence, or database state. It is result-surface exposure only.

## 11. Independent-review sufficiency

The fresh independent-review record was read in full and independently checked against live source, diff, repository consumers, and tests. It adequately establishes:

- the exact authorized two-file diff;
- predecessor provenance for ordinary SELL and conversion cash-in-lieu accumulation;
- the successful Stage-1 boundary and `None`/`0.0` numeric distinction;
- ordinary SELL, cash-in-lieu, default, successful-zero, `skip_snapshots=True`, and fetch-free evidence;
- constructor, equality, serialization, API/frontend, schema/persistence, and named-consumer compatibility;
- accounting, replay, provider, and snapshot non-interference;
- focused tests and the Freeze-defined governing WP5 regression corpus;
- the temporary-directory incident as environmental/non-blocking;
- graph output as ignored derived metadata, not a repository mutation;
- WP7 and LM13 non-interference; and
- a counterexample search covering successful zero, both realized-event types, failed/pre-Stage-1 behavior, skipped snapshots, existing callers, and absent generic serialization.

The PASS is sufficient for Confirmation and is not inherited without verification.

## 12. Regression-evidence determination

WP5 Implementation Freeze §O defines the governing test membership as:

- `backend/tests/test_portfolio_rebuilder.py`;
- `backend/tests/test_portfolio_metrics.py`;
- `backend/tests/test_snapshot_return_recovery.py`; and
- `backend/tests/test_verify_snapshots.py`.

This Confirmation independently ran that exact four-file corpus and obtained:

```text
207 passed, 0 failed
```

The prior implementer's `188 passed` remains a non-blocking historical reporting discrepancy. It came from a different command/file set and is not represented as the same governing invocation. This record neither erases that historical result nor claims the two counts describe one command.

## 13. Temporary-directory incident treatment

The earlier permission failure occurred during pytest temporary-directory setup before affected test bodies ran. The same implementation bytes later passed with a workspace-local temporary base, and this Confirmation independently reproduced the governing `207 passed` result using a workspace-local temporary base. The temporary location changes fixture storage only, not application or test semantics.

**Classification: `ENVIRONMENTAL / NON-BLOCKING`.**

The temporary test directory used by this Confirmation was removed after the run and is not part of repository state.

## 14. Graph metadata treatment

`.gitignore` line 67 excludes `graphify-out/`; `git check-ignore` confirms `graphify-out/graph.json` is ignored, and Git status contains no repository mutation under that path. The graph is local derived knowledge metadata and is not a WP5/WP7 source, test, or governance member.

**Classification: `TOOL/DERIVED METADATA — NON-REPOSITORY / NON-BLOCKING`.**

## 15. WP7 relationship

WP7's frozen four-component replay comparison triggered the need for this WP5 amendment. WP7 neither owns nor modified the WP5 service. Its WPP, Planning Confirmation, Planning Freeze, and failed independent implementation review remain byte-identical. Its candidate remains paused and `backend/manage.py` still does not consume `reconstructed_realized_pnl`.

This Confirmation grants no authority to resume WP7. WP7 may resume its separately bounded correction only after the fresh WP5 Implementation Freeze binds the amended identities and this Confirmation record.

## 16. Residual and non-interference boundary

This amendment and Confirmation discharge no WP5 or WP7 residual. They do not alter `MINOR-5`, `NEW-MINOR-A`, or `PD-3`; do not alter LM13 or WP7 acceptance results; do not reopen historical WP5 implementation outside the two confirmed lines and focused evidence; and create no WP8/M46 authority.

## 17. Confirmation determination

The Authorization is exact; the amended two-file corpus is exact and unchanged since review; the review is exact, independently sufficient, and passing; the governing regression corpus is green; compatibility and non-interference hold; and no lifecycle contradiction exists.

**`BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION CONFIRMED`**

This confirms only the bounded amendment identities in §6. It does not replace the historical WP5 Confirmation, reopen unrelated historical implementation, or freeze the amended bytes.

## 18. Authority explicitly not granted

This Confirmation grants no authority for additional WP5 implementation, implementation correction, WP7 correction, LM13 synchronization, production execution, release, deployment, schema/data/cache mutation, WP8/M46 work, staging, commit, push, or merge. It performs no Decision Log or INDEX synchronization and no production or operator action.

## 19. Artifact created and repository boundary

This single additive record is the only artifact created by the Confirmation act:

`docs/implementation/BANPU_WP5_FRESH_IMPLEMENTATION_CONFIRMATION_REALIZED_PNL_EXPOSURE.md`

The Amendment Authorization, fresh independent-review record, implementation/test bytes, prior WP5 frozen artifacts, WP7 state, LM13, Decision Log, and Implementation INDEX are not modified by this act. Pre-existing unstaged WP7 candidate/governance changes and the already-reviewed two-file WP5 implementation amendment remain separately attributable and are not created by this Confirmation.

## 20. Resulting constitutional state and exact next act

- Historical WP5 remains complete, implementation-frozen, and closed at its prior corpus identity, with this confirmed amendment not yet freshly frozen.
- The bounded realized-P&L result-surface amendment is authorized, implemented, freshly independently reviewed as PASS, and now confirmed.
- WP7 remains planning-confirmed/planning-frozen with its failed implementation review and paused correction still of record; it does not yet consume the field.
- No release, deployment, production mutation, residual discharge, or WP8/M46 authority exists.

The exact next constitutional act is:

**BANPU-WP5 Fresh Implementation Freeze — RebuildResult Realized P&L Exposure**

over the exact confirmed amended implementation identities in §6 and this Confirmation record. This act performs no part of that Freeze.

