# BANPU-WP5 — Implementation Authorization Amendment: RebuildResult Realized P&L Exposure

**Artifact class:** Additive constitutional Implementation Authorization amendment for a frozen-corpus correction path  
**Amendment date:** 2026-08-19  
**Issuing authority:** BANPU-WP5 Implementation Authorization Amendment Authority, acting only for the bounded result-surface exposure specified below  
**Frozen implementation record:** [`BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md), SHA-256 `8FE512A22BD0979B274C211BA48E4EB10B7CD5E82F42950C617DBE856A570E54`, disposition `BANPU-WP5 IMPLEMENTATION FROZEN`  
**Closed lifecycle record:** [`BANPU_WP5_EPIC_CLOSEOUT.md`](BANPU_WP5_EPIC_CLOSEOUT.md), SHA-256 `46AC7C4B5517F5DCE3978CE292ABDD4B8D6783D6C86A20DE8191291C55103E4A`, disposition `BANPU-WP5 EPIC CLOSEOUT COMPLETE`  
**Disposition:** `BANPU-WP5 REALIZED-PNL RESULT-SURFACE AMENDMENT AUTHORIZED`  
**Implementation performed by this act:** `NO`  
**Release/deployment/production-mutation authority created:** `NONE`

---

## 1. Nature and boundary of this act

This is a successor-triggered, additive authorization amendment only.  It creates a fresh, narrowly bounded path to expose through `RebuildResult` a cumulative realized-P&L value that Stage 1 replay already computes.  It does not implement that field, alter a realized-P&L equation, amend the frozen WP5 or WP7 plans, perform independent review, confirmation, or freeze, reopen WP5 accounting design, or authorize release, deployment, reconstruction, or production mutation.

The active WP5 frozen identity remains the one named above until a future implementation amendment completes the fresh review, confirmation, and freeze sequence in §15.  This amendment is not an assertion that any future field already exists.

## 2. Amendment entry-state verification

Each entry premise was independently checked from current repository bytes immediately before this record was written.

| Premise | Live evidence | Result |
|---|---|---|
| HEAD and staging state | HEAD `ae223a42df688563748c0e6e6cb898e66bcb3da0`; `git diff --cached --name-only` is empty | `SATISFIED` |
| WP5 lifecycle remains complete, frozen, and closed | Freeze and Closeout records above retain their exact recorded identities and dispositions | `SATISFIED` |
| `portfolio_rebuilder.py` is a frozen WP5 member | Freeze §E row 3 / §O list it in the nine-member corpus | `SATISFIED` |
| Frozen WP5 change-control rule is unchanged | Freeze §P still requires fresh authorization scoped to the change, fresh independent review, Confirmation, and Freeze | `SATISFIED` |
| Exact change has no prior authorization | Repository-wide search found no `RebuildResult` realized-P&L authorization/amendment or `reconstructed_realized_pnl` field | `SATISFIED` |
| WP7 planning remains confirmed and frozen | WPP `9A5F4F797AD800E8A6E2CAA475E428BAA6BB5693686401F47CE131E829952897`; Confirmation `7A44203B6E39BF5100B133DA39B96BD5A5B1059634B279B8C4706F1742A0E82D`; Freeze `E31AEC306C4CFDF0820A83BA1335DE22E0E9BE6A2ABC94AB153E85A6AB708B84` | `SATISFIED` |
| WP7 review is still failed on replay comparison | [`BANPU_WP7_INDEPENDENT_IMPLEMENTATION_REVIEW.md`](BANPU_WP7_INDEPENDENT_IMPLEMENTATION_REVIEW.md), SHA-256 `59D39B92DDDB8BFAACE785C49D4453EC3F423C85C2D8FC15B8E025DF601DDF74`, retains `FAIL — IMPLEMENTATION CORRECTION REQUIRED` | `SATISFIED` |
| Corrected WP7 candidate still lacks only realized-P&L comparison | `manage.py` lines 4548–4603 fail closed on replay failure and compare cash/holdings/basis, while expressly recording realized P&L as unavailable from `RebuildResult` | `SATISFIED` |
| Frozen rebuilder has not drifted | `backend/services/portfolio_rebuilder.py`: 129,334 B, SHA-256 `D94E686DB2EFF8F95B1047FA470A2DD94B663F0847233260FDEC9B4626422765`, exact match to Freeze §E | `SATISFIED` |
| No staged, production, release, or deployment act | Empty index; working tree contains only the pre-existing WP7 candidate/governance artifacts and no production/release/deployment artifact or act | `SATISFIED` |

The entry state contains pre-existing, unstaged WP7 candidate changes in `backend/manage.py`, its focused test/fixture, and WP7 governance records.  They neither modify `portfolio_rebuilder.py` nor constitute implementation under this amendment.

## 3. Applicable WP5 amendment precedent

The closest implementation-authorization-amendment lineage is the complete D7 chain:

1. [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_D7_MECHANICAL_CONTINUITY_ENFORCEMENT.md) — an additive, bounded authorization determination;
2. its independent reapproval record and fresh independent reapproval record;
3. [`BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_BINDING_FREEZE_RECORD.md`](BANPU_WP5_D7_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_BINDING_FREEZE_RECORD.md); and
4. the resulting WP5 amendment/implementation lifecycle preserved in the later Freeze and Closeout records.

Its governing semantics are applied here: an authorization amendment is additive; it identifies one competent, minimum capability; it leaves the prior authorization and frozen corpus historically intact; it explicitly states both permitted and prohibited effects; and it does not claim implementation or a new frozen corpus.  D7's mechanical-continuity substance, its two earlier reapproval complications, and its WPP-amendment requirements do not transfer: they addressed an unresolved design predicate in an unclosed planning lifecycle.  The present trigger is an already-frozen WP7 requirement and an already-computed WP5 value.  The directly applicable post-freeze control is WP5 Freeze §P, whose required future sequence is recorded in §15.

## 4. Successor trigger and WP5 ownership

WP7 WPP §7.3 requires both replay modes to be checked after a successful conversion, and §7.2 fixes the replay comparison set as holdings, basis, cash, and realized P&L.  Its Planning Confirmation independently confirmed the dual-replay mechanism, and its Planning Freeze binds that WPP without permitting silent reinterpretation.  WP7 WPP §12 simultaneously prohibits WP7 from editing `backend/services/portfolio_rebuilder.py`.

The current WP7 implementation therefore correctly calls the existing WP5 rebuilder but cannot lawfully invent another realized-P&L calculation or modify the rebuilder.  The failed independent review identified exactly that missing observation in WP7-IIR-B1.  The current bounded WP7 correction cures mode failure handling plus cash/holdings/basis comparison, but its live code explicitly leaves the realized-P&L leg open because the result does not expose it.  This is the narrow successor trigger for WP5 action; it transfers no ownership of the file or accounting semantics to WP7.

## 5. Canonical realized-P&L provenance

Live Stage 1 code proves the requested value is canonical predecessor logic, not a WP7 calculation:

| Fact | Live locus | Finding |
|---|---|---|
| Initialization | `portfolio_rebuilder.py` line 2256 initializes `final_state = _PortfolioState(Decimal("0"), {}, Decimal("0"))` | cumulative realized P&L begins as a Stage 1 state value |
| Ordinary realized-P&L accumulation | `_apply_transaction()` lines 789–806 adds canonical `ctx.realized_pnl` on `SELL` (or zero where absent) | ordinary realized P&L is accumulated by the established replay path |
| Conversion/cash-in-lieu accumulation | `_apply_transaction()` lines 849–943 adds the already-parsed `payload.cash_in_lieu.realized_pnl`, or `Decimal("0")` where there is no cash in lieu | conversion realized P&L is accumulated exactly once by existing canonical logic |
| Final-state availability | lines 2264–2271 finish Stage 1, then populate existing reconstructed result fields | the value exists before Stage 2/3 snapshot/provider work and when result fields are populated |
| Predecessor timing | `git log -S'cumulative_realized_pnl'` reports commit `3a0bbe726dd4f2de67a8e6d3dbe227b4b5b27f44`, dated 2026-08-10 | it predates the 2026-08-19 WP7 planning corpus |

The intended change is therefore an observation of `final_state.cumulative_realized_pnl` at the existing Stage 1 result-construction point.  It neither specifies nor changes the underlying sell or cash-in-lieu accounting equation, transaction canonicalization, replay order, state transition, snapshot calculation, provider behavior, or database state.

## 6. Current result-surface gap and numeric representation

`RebuildResult` currently exposes `reconstructed_holdings_count: int = 0` and `reconstructed_cash: float | None = None` as Stage 1 outputs, but no cumulative realized-P&L output.  The current population site at lines 2270–2271 uses `_f(final_state.cash_balance)`.  `_f()` is the module's established `Decimal`-to-`float` convention: it quantizes to the existing `_QUANT` with `ROUND_HALF_UP` before conversion.

The amendment therefore authorizes the semantic value `reconstructed_realized_pnl` with the same `float | None` representation and the same `_f(final_state.cumulative_realized_pnl)` conversion already used by the adjacent reconstructed cash result.  This does not introduce a WP7-specific accounting or rounding rule; it applies the module's existing result-surface convention mechanically.  `None` remains the default for result paths that do not successfully reach Stage 1, while a successful Stage 1 exposes its canonical value, including `0.0`.

## 7. Compatibility determination

All in-repository constructors and consumers of `RebuildResult` were inspected.

| Compatibility question | Finding | Result |
|---|---|---|
| Positional construction | The three required constructor parameters are first; all current in-repository constructions use keyword arguments.  The new field must be declared last and defaulted. | `BACKWARD-COMPATIBLE` |
| Keyword construction | Every existing constructor omits the proposed field and will receive its default. | `BACKWARD-COMPATIBLE` |
| Dataclass equality | A dataclass field participates in generated equality, but repository search found no equality comparison of whole `RebuildResult` values. | `NO CURRENT CONSUMER IMPACT` |
| Exact field-set / `asdict()` / `__dict__` use | No `RebuildResult` consumer uses these forms or asserts an exact dataclass field set. | `NO CURRENT CONTRACT IMPACT` |
| JSON or API serialization | No router, endpoint, serializer, persisted model, or JSON response serializes `RebuildResult`; `manage.py` prints selected fields only. | `NO API OR PERSISTED-CONTRACT EXPANSION` |
| Downstream consumers | `manage.py`, `registry_replay_parity.py`, `replay_cutover.py`, and tests consume named existing fields or the reconciliation report.  None requires modification to tolerate a trailing defaulted field. | `BACKWARD-COMPATIBLE` |
| Snapshot/golden output | Golden-baseline content uses holdings/snapshots/validator findings/cash; the proposed field neither changes that extraction nor requires a golden-output edit. | `NO COLLATERAL CHANGE REQUIRED` |

The authorization is sufficient only because no unrelated caller, public contract, schema, or serializer must be changed.  It authorizes no such change.

## 8. Exact authorized surface

### 8.1 Production file and code surface

The sole authorized production file is:

`backend/services/portfolio_rebuilder.py`

Within that file, the future amendment may do exactly and only the following:

1. append one trailing, defaulted `RebuildResult` field named `reconstructed_realized_pnl`, semantically representing replay-computed cumulative realized P&L; and
2. after Stage 1 replay succeeds, at the same canonical result-population point as reconstructed cash and holding count, assign `result.reconstructed_realized_pnl = _f(final_state.cumulative_realized_pnl)`.

The field must remain trailing and defaulted.  No other production behavior is authorized.

### 8.2 Focused future test/evidence surface

The future implementation amendment may modify only the existing frozen WP5-owned test file:

`backend/tests/test_portfolio_rebuilder.py`

It may add narrowly focused cases proving: (a) default compatibility; (b) Stage 1 ordinary sell realized P&L surfaces correctly; (c) canonical cash-in-lieu realized P&L surfaces correctly where applicable; (d) `skip_snapshots=True` still exposes the field; (e) no provider fetch is required; and (f) existing callers and the existing WP5 regression scope remain compatible.  No new test file is authorized by this amendment.

## 9. Accounting and provider non-interference

This amendment authorizes output exposure only.  It does not authorize a realized-P&L formula change, transaction canonicalization change, basis-allocation change, replay-order change, portfolio-state transition change, snapshot behavior change, provider or historical-price fetch, registry behavior, conversion behavior, cache/rebuild semantic change, schema/database migration, or any persistence.

The direct source is the in-memory `final_state` already constructed before Stages 2–3.  `skip_snapshots=True` therefore remains sufficient, and the new observation requires no provider data.  The current debug `print()` statements in `portfolio_rebuilder.py` remain outside this amendment.

## 10. Explicit exclusions

This amendment does not authorize:

- any file other than the production and focused-test surfaces in §8;
- refactoring, formatting, unrelated typing cleanup, debug-print cleanup, or other maintenance in `portfolio_rebuilder.py`;
- API, frontend, serializer, route, database, migration, cache, registry, transaction, quote-contract, or shadow changes;
- implementation, review, Confirmation, Freeze, closeout, Decision Log, or INDEX work in this act;
- any modification to the WP7 WPP, the WP7 candidate, or the stale WP4 LM13 test; or
- release, deployment, production conversion, production reconstruction, staging, commit, push, or merge.

LM13 is explicitly excluded.  Its separate successor-boundary synchronization remains unrelated to this WP5 amendment.

## 11. WP5 non-interference and WP7 relationship

The amendment does not reopen WP5 accounting design, invalidate WP5's historical completion, transfer `portfolio_rebuilder.py` ownership to WP7, or weaken any prior WP5 acceptance result.  It creates one newly authorized correction path to the frozen corpus under Freeze §P.

It exists solely to make a pre-existing canonical WP5 replay value observable to WP7 after the WP5 amendment lifecycle closes.  WP7's frozen requirement is unchanged: both replay modes must compare holdings, basis, cash, and realized P&L.  This record grants WP7 no scope other than later consuming the exposed field through its own separately authorized, bounded correction; it does not amend the WP7 WPP or implement that consumption.

`MINOR-5`, `NEW-MINOR-A`, `PD-3`, WP7 rehearsal evidence, and WP8 release-evidence ownership are unchanged.  No residual is discharged by this authorization.

## 12. Authority granted

This amendment authorizes a future **BANPU-WP5 Bounded Implementation Amendment** limited to §8's additive `RebuildResult` realized-P&L exposure and focused evidence.  It is a fresh authorization scoped to the material change required by WP5 Freeze §P.

It does not claim the code change has occurred, does not re-freeze WP5, and does not authorize any wider implementation.  The pre-amendment WP5 frozen corpus remains the active frozen identity until the exact future lifecycle in §15 is complete.

## 13. Authority not granted

No authority is granted to alter the canonical calculation, to expose any result through an API, to add a generic result framework, to consume the field in WP7 now, to alter LM13, or to perform production/release/deployment work.  Any need beyond the single field assignment and its focused proof is a new scope question and must fail closed.

## 14. Resulting constitutional state

- WP5 remains `COMPLETE / IMPLEMENTATION FROZEN / EPIC CLOSED` at its existing frozen corpus identity.
- Its prior implementation authority remains exhausted for the closed candidate; this amendment supplies only the separately bounded correction path in §12.
- The `RebuildResult` realized-P&L field is `NOT IMPLEMENTED`.
- WP7 remains `PLANNING CONFIRMED / PLANNING FROZEN`; its failed implementation review remains of record.
- The corrected WP7 candidate remains incomplete on the realized-P&L comparison leg and may not consume a new field before WP5's amendment lifecycle completes.
- No release, deployment, production mutation, residual discharge, or WP8 authority exists.

## 15. Required downstream amendment lifecycle

WP5 Freeze §P fixes the post-freeze sequence for a material frozen-corpus change.  The required successor chain is:

1. this Implementation Authorization Amendment;
2. **BANPU-WP5 Bounded Implementation Amendment** within §8 only;
3. fresh independent WP5 implementation review of the amended corpus;
4. fresh WP5 Implementation Confirmation; and
5. fresh WP5 Implementation Freeze binding the updated corpus.

Only then may WP7 resume its separately bounded correction to consume the field and complete the frozen four-component replay comparison.  No direct jump from this authorization to WP7 implementation is permitted.

## 16. Artifact created

This additive record only:

`docs/implementation/BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_REALIZED_PNL_EXPOSURE.md`

No prior governance artifact, source file, test file, frozen corpus member, Decision Log, or INDEX entry is modified by this act.

## 17. Disposition

**`BANPU-WP5 REALIZED-PNL RESULT-SURFACE AMENDMENT AUTHORIZED`**

The authorization is narrow, compatible, and sufficient.  It authorizes a future implementation amendment; it does not implement, confirm, freeze, or close that amendment.

## 18. Exact next constitutional act

**BANPU-WP5 Bounded Implementation Amendment — expose the already-computed canonical replay realized P&L through `RebuildResult`**

That act must be performed strictly under this Amendment Authorization and remain within §8.  It is not performed in this session.
