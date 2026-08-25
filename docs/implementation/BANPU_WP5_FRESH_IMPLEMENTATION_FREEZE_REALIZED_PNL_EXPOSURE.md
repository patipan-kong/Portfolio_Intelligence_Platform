# BANPU-WP5 — Fresh Implementation Freeze: RebuildResult Realized P&L Exposure

**Artifact class:** Additive Fresh Implementation Freeze record for a bounded amendment to a historically frozen/closed WP5 corpus
**Freeze date:** 2026-08-19
**Issuing role:** Independent BANPU-WP5 Fresh Implementation Freeze Authority
**Amendment Authorization:** [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_REALIZED_PNL_EXPOSURE.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_AMENDMENT_REBUILDRESULT_REALIZED_PNL_EXPOSURE.md), 18,182 bytes, SHA-256 `DFFFF800D9636AB5266846FD750FCE3CD3DF6AFA40EAB3EB43219F280D7D8336`
**Fresh independent review:** [`BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_REALIZED_PNL_EXPOSURE.md`](BANPU_WP5_FRESH_INDEPENDENT_IMPLEMENTATION_REVIEW_REALIZED_PNL_EXPOSURE.md), 21,189 bytes, SHA-256 `3B3E836377269CAB1E352CC653F4C79E133525761C7ACC097B5A8C3CF8085925`
**Fresh Implementation Confirmation:** [`BANPU_WP5_FRESH_IMPLEMENTATION_CONFIRMATION_REALIZED_PNL_EXPOSURE.md`](BANPU_WP5_FRESH_IMPLEMENTATION_CONFIRMATION_REALIZED_PNL_EXPOSURE.md), 16,548 bytes, SHA-256 `92CB87DDB7263712EF8CCF640C3A91CDDC36B98CAAAA97B94C4072D739F4E7E4`
**Disposition:** `BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION FROZEN`
**WP7 correction resumed by this act:** `NO`
**Production/release/deployment authority created:** `NONE`

---

## 1. Freeze authority and boundary

This act performs only the Fresh Implementation Freeze required by the original WP5 Implementation Freeze Record §P for a material change to a historically frozen implementation member. It binds the exact bounded amendment corpus in §5, at the confirmed identities in §6, as competent frozen predecessor functionality.

It does not modify implementation or tests, re-perform the independent review or Confirmation, reopen the historical WP5 corpus, resume or implement WP7, modify LM13, synchronize the Decision Log or Implementation INDEX, perform production execution, release, deployment, cache/schema/database mutation, staging, commit, or push.

## 2. Freeze entry-state verification

All mandatory fail-closed premises were independently rechecked from live bytes before this record was created:

| Premise | Result |
|---|---|
| HEAD baseline | `ae223a42df688563748c0e6e6cb898e66bcb3da0` — exact |
| Staging area | empty |
| Amendment Authorization | present and exact at `DFFFF800…8336`; disposition `BANPU-WP5 REALIZED-PNL RESULT-SURFACE AMENDMENT AUTHORIZED` |
| Amended production member | exact at `409FBC22…F429` |
| Amended test member | exact at `F42FFF20…8B25` |
| Fresh independent review | present and exact at `3B3E8363…5925`; disposition `BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION REVIEW PASSED` |
| Fresh Implementation Confirmation | present and exact at `92CB87DD…E7E4`; disposition `BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION CONFIRMED` |
| Post-Confirmation implementation/test mutation | none; current two-file hashes exactly equal the reviewed and confirmed identities |
| Prior Fresh Freeze for this amendment | absent before this act |
| Historical WP5 Freeze / Closeout | unchanged at `8FE512A2…0E54` / `46AC7C4B…3E4A` |
| WP7 frozen planning corpus | unchanged: WPP `9A5F4F79…2897`, Planning Confirmation `7A44203B…E82D`, Planning Freeze `E31AEC30…8B84`, failed review `59D39B92…DF74` |
| WP7 consumption / correction state | `backend/manage.py` has zero `reconstructed_realized_pnl` references; its correction remains paused |
| LM13 | `backend/tests/test_position_conversion_live.py` unchanged, SHA-256 `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8` |
| Decision Log / Implementation INDEX | unchanged |
| Production/release/deployment activity | none found or performed |

No drift or contradictory lifecycle state was found. Freeze proceeds.

## 3. Freeze precedent and binding model

The original [`BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP5_IMPLEMENTATION_FREEZE_RECORD.md) supplies the applicable Implementation Freeze semantics: freeze independently verifies Confirmation, identity continuity, corpus boundary, review evidence, residual carry-forward, change control, exclusions, and the exact next act. Its §P requires a fresh authorization, fresh independent review, fresh Confirmation, and fresh Freeze for any material change to a frozen member.

The completed D7 amendment lineage supplies the amendment-specific form: its Binding Freeze record is additive, binds exact reviewed predecessor identities, preserves the earlier frozen records, and does not silently rebind unrelated implementation corpus members. D7's planning and mechanical-continuity substance does not transfer.

Accordingly, this is **an additive two-member overlay**, not a re-freeze of all nine historical WP5 members. The original nine-member WP5 corpus remains historically frozen at its original record and identity. This Freeze binds only the two amended members that passed the new Authorization → Review → Confirmation chain. No hybrid or substituted nine-member identity is created.

## 4. Confirmation sufficiency verification

The Fresh Implementation Confirmation was read in full and independently found sufficient to bind:

- the exact Amendment Authorization and two-file implementation identities;
- the exact passing independent-review identity;
- predecessor provenance for ordinary SELL and conversion cash-in-lieu realized P&L;
- successful Stage-1 assignment, successful-zero `0.0`, pre-Stage-1 default `None`, `skip_snapshots=True`, and fetch-free behavior;
- trailing/defaulted-field compatibility across constructors, consumers, equality, serialization, API/frontend, and persistence/schema surfaces;
- accounting, replay, provider, snapshot, registry, cache, and persistence non-interference;
- governing regression evidence, the historical count discrepancy, and the environmental/graph classifications;
- WP7 and LM13 non-interference; and
- explicit authority exclusions.

The Confirmation is thus an adequate Freeze input; this Freeze does not rely on its disposition alone.

## 5. Frozen amended-corpus membership and identity model

The fresh frozen overlay has cardinality **2**:

1. `backend/services/portfolio_rebuilder.py`
2. `backend/tests/test_portfolio_rebuilder.py`

These are the complete and only members of the Amendment Authorization's production and focused-test surface. They are frozen as an additive overlay to, not a replacement for, the original WP5 nine-member frozen corpus.

The raw continuity aggregate uses the original WP5 Freeze §E convention and order: UTF-8 manifest rows of `path<TAB>status<TAB>SHA256<TAB>bytes<LF>`, with status `M` for both working-tree amendment members. The canonical identity of record uses the original WP5 Freeze §H convention and order: normalized-LF `path<TAB>SHA256<TAB>canonical-bytes<LF>` rows. The two files carry CRLF in this checkout, so raw and canonical identities intentionally differ.

## 6. Cryptographic identity verification

| Artifact | Raw bytes | Raw SHA-256 | Canonical LF bytes | Canonical LF SHA-256 |
|---|---:|---|---:|---|
| `backend/services/portfolio_rebuilder.py` | 129,464 | `409FBC22313A98B24D9A23FFE3754CBA2584A702473C36CB2D51A36EDC19F429` | 126,793 | `37BE4B62606E381D8FC227B26E61D14422E17BBA1F572908318932F63A648976` |
| `backend/tests/test_portfolio_rebuilder.py` | 108,142 | `F42FFF2084A568CE165D0F58B0C3EA0109881E38736BB9CE299E330F49808B25` | 105,928 | `2D082FC0B4B36D20B23D0AE798F8EBB479A4882084E2DA5AA3935DCF5387DCA9` |

The following predecessor identities were also recomputed and are exact:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Amendment Authorization | 18,182 | `DFFFF800D9636AB5266846FD750FCE3CD3DF6AFA40EAB3EB43219F280D7D8336` |
| Fresh independent review | 21,189 | `3B3E836377269CAB1E352CC653F4C79E133525761C7ACC097B5A8C3CF8085925` |
| Fresh Implementation Confirmation | 16,548 | `92CB87DDB7263712EF8CCF640C3A91CDDC36B98CAAAA97B94C4072D739F4E7E4` |

```text
Amended overlay aggregate (raw continuity)    = 42A11FF7198AF237F766D0E3A52D2C3A3BE56BF61C70140FCDB67130B589DBA4
Amended overlay aggregate (canonical LF record) = 6C898E13B32293F3C57225511DDAD23EDDC5C3324C197BBE28343F753596EA28
```

The canonical-LF aggregate is the identity of record for this two-member frozen overlay. The raw aggregate preserves continuity with the review/Confirmation checkout bytes.

## 7. Exact frozen semantic delta

This Freeze binds only the following observation-only semantic delta:

```python
reconstructed_realized_pnl: float | None = None
```

as the trailing/defaulted `RebuildResult` field, populated on successful Stage 1 by:

```python
_f(final_state.cumulative_realized_pnl)
```

It exposes an already-computed canonical cumulative realized-P&L value. It does not create, alter, or reinterpret an accounting formula, replay transition, or provider operation.

## 8. Accounting, replay, and provider preservation

The historical WP5 semantics remain frozen unchanged. This amendment made no change to realized-P&L equations, basis allocation, transaction canonicalization, BUY/SELL behavior, conversion or cash-in-lieu behavior, replay ordering, reconciliation, provider fetching, snapshots, registry, cache, persistence, schema, or database state. The new result field is an observation of existing Stage-1 state only.

## 9. Regression evidence bound

The Confirmation independently reproduced the original WP5 Freeze §O governing four-file corpus:

```text
207 passed, 0 failed
```

That result remains live-supported by the unchanged Confirmation and review evidence and is bound to this Freeze. The earlier `188 passed` is preserved as a non-blocking historical reporting discrepancy from a different command; neither count is rewritten to describe the other.

## 10. Environmental and graph metadata observations

- **Temporary-directory incident:** `ENVIRONMENTAL / NON-BLOCKING`. It occurred in pytest setup before test bodies, and a workspace-local temporary base reproduced the governing green result without changing code or test semantics.
- **Graph metadata:** `TOOL/DERIVED METADATA — NON-REPOSITORY / NON-BLOCKING`. `.gitignore` excludes `graphify-out/`; it is not present in Git status or the frozen implementation overlay.

Neither observation is a frozen corpus member or implementation finding.

## 11. WP7 successor boundary

WP7's Authorization authorizes its CLI-only `backend/manage.py` correction and focused manifest/test surfaces; its WPP freezes both-mode replay comparison of holdings, basis, cash, and realized P&L; and its Planning Freeze expressly determines that no additional implementation-entry governance act is required after its existing Authorization and frozen plan.

This completed WP5 Freeze makes `reconstructed_realized_pnl` competent frozen predecessor functionality. A later, separately performed resumption of the already-authorized bounded WP7 Implementation Correction may consume this field to complete the four-component comparison. WP7 still may not edit `portfolio_rebuilder.py`, and this record does not itself resume, implement, review, or confirm WP7.

## 12. LM13 boundary and residual preservation

LM13 remains outside this WP5 amendment and is neither modified nor synchronized. Its known WP7 successor-boundary issue remains a separate later act.

No residual is discharged or altered: `MINOR-5`, `NEW-MINOR-A`, `PD-3`, WP7 rehearsal-dependent acceptance rows, WP8 release evidence, and M46 remain as previously assigned.

## 13. Change-control boundary

The two amended overlay identities are now immutable under the applicable WP5 change-control mechanism. Any future material change to either freshly frozen member requires a new competent amendment/correction lifecycle: scoped authority, fresh independent review, fresh Confirmation, and fresh Freeze. No silent edit may preserve this frozen identity.

## 14. Authority explicitly not granted

This Freeze grants no authority for further WP5 implementation or `portfolio_rebuilder.py` modification; WP7 implementation within this act; LM13 synchronization; production execution; release; deployment; schema/database/cache mutation; WP8/M46 work; staging; commit; push; or merge. It completes only this WP5 amendment lifecycle and records the successor boundary for the later WP7 act.

## 15. Artifact created and repository verification

This single additive artifact is the only file created by this Freeze act:

`docs/implementation/BANPU_WP5_FRESH_IMPLEMENTATION_FREEZE_REALIZED_PNL_EXPOSURE.md`

After creation, the production/test members, Amendment Authorization, Review, Confirmation, historical WP5 Freeze/Closeout, WP7 frozen planning artifacts, LM13, Decision Log, and Implementation INDEX were re-verified unchanged. The pre-existing WP7 candidate/governance changes and already-reviewed WP5 two-file implementation diff remain separately attributable; this act adds only this record.

## 16. Resulting constitutional state and exact next act

- Historical WP5 remains complete, frozen, and closed at its historical nine-member corpus identity.
- The two-member realized-P&L result-surface overlay is now independently authorized, implemented, reviewed, confirmed, and freshly frozen at the identities in §6.
- WP7 remains planning-confirmed/planning-frozen; its correction has not been resumed by this act, but may now be resumed separately within its existing bounded authority to consume the frozen predecessor result.
- No production/release/deployment authority, residual discharge, or WP8/M46 authority exists.

The exact next constitutional act is:

**Resume the bounded BANPU-WP7 Implementation Correction**, consuming the now-frozen canonical `reconstructed_realized_pnl` result to complete the required both-mode comparison of holdings, basis, cash, and realized P&L.

This Freeze performs no part of that WP7 correction.

## 17. Fresh Implementation Freeze disposition

**`BANPU-WP5 REALIZED-PNL RESULT-SURFACE IMPLEMENTATION FROZEN`**
