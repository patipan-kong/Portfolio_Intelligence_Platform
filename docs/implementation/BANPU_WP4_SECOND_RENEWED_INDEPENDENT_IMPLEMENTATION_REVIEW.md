# BANPU-WP4 — Second Renewed Independent Implementation Review

**Artifact class:** Additive second-renewed independent implementation review record
**Review date:** 2026-08-13
**Review authority:** Second Renewed Independent Implementation Reviewer
**Prior renewed review:** [`BANPU_WP4_RENEWED_INDEPENDENT_IMPLEMENTATION_REVIEW.md`](BANPU_WP4_RENEWED_INDEPENDENT_IMPLEMENTATION_REVIEW.md)
**Prior renewed-review identity:** raw SHA-256 `AD6017FFCFA4CC0D23BBFDA51B0F387C8E4CA0351BECE47CF96FC216F42845F3`
**Review disposition:** `BANPU-WP4 CORRECTED IMPLEMENTATION CANDIDATE — NOT CONFIRMED`
**Implementation Confirmation performed:** `NO`
**Implementation or test correction performed:** `NO`
**Freeze, closeout, release, deployment, production execution, WP5+, or M46 authority exercised:** `NONE`

---

## 1. Authority and identity continuity

The live authority chain was recomputed from repository bytes. The operative
Plan remains the exact original Plan plus the independently reapproved additive
amendment for Plan §§3.2, 6, and 9. The reapproval permits implementation
reliance on authoritative `E8-R` under the existing bounded WP4 Implementation
Authorization.

| Artifact | Raw SHA-256 | Result |
|---|---|---|
| [Original Work Package Plan](BANPU_WP4_WORK_PACKAGE_PLAN.md) | `F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE` | `EXACT` |
| [Retry-order Plan amendment](BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT.md) | `52254EB873CB57A5B3C30E62897878CAC20A23DCEDC2AAF2E5EB969D5C1C4168` | `EXACT` |
| [Plan-amendment independent reapproval](BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT_INDEPENDENT_REAPPROVAL.md) | `2258C1C3F40714FD371121645C3DECB2CA72946E825D816B789B586C2A5BFBF1` | `EXACT` |
| [Retry-order governance decision](BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md) | `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB` | `EXACT` |
| [Amendment binding/freeze record](BANPU_WP4_RETRY_ORDER_AMENDMENT_BINDING_FREEZE_RECORD.md) | `5E312392767737C8F0445F51182B32A87B2EDF42B4C886BFB0296164EE389669` | `EXACT` |
| [Allocation Record](BANPU_WP4_ALLOCATION_RECORD.md) | `CEE6F01C4113697BE6485AE56BB80FE0E9E99CB8555C08BC5D3E3CD67B94BAA9` | `EXACT` |
| [Implementation Authorization](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md) | `D8E89048BDC3B939731523937C8122A25E9659EDD5CE5B28F48DEAD022A6BCFA` | `EXACT` |
| [Original Independent Implementation Review](BANPU_WP4_INDEPENDENT_IMPLEMENTATION_REVIEW.md) | `D1033DC13E8BF6D0F7AEA39AFFC4EE660FC962AE24A9B6D96521B1FA0CB91450` | `EXACT` |
| Prior Renewed Independent Implementation Review | `AD6017FFCFA4CC0D23BBFDA51B0F387C8E4CA0351BECE47CF96FC216F42845F3` | `EXACT` |

No correction report was accepted as proof.

## 2. Candidate identity and scope

The live candidate reviewed is:

| Candidate file | Raw SHA-256 |
|---|---|
| `backend/services/asset_registry.py` | `16A5CECA8C0E0DA94A002C3D5C7F18D2DD7FEF89113C2D1AE837112212097B70` |
| `backend/services/portfolio_transactions.py` | `19B30C06445881393F0BA0169A7CD1AFF1B7DB9F9C4257CCD63DD9CB7CB6A080` |
| `backend/services/transaction_canonicalizer.py` | `0EA60A06C4224A303DB4B7EEFAA4A5A7D5596E4BA971F468D62B2BA278C60DFD` |
| `backend/tests/test_asset_registry.py` | `48267B7D3ECFE0375B7113E7239DA4B572EA424E67B3885C4DD2376D2BF07E16` |
| `backend/tests/test_transaction_canonicalizer.py` | `EDF2CF8C691DF7DA5AA265CD61F8137EC9E885D41E66A49186D568ECD07F0627` |
| `backend/tests/test_position_conversion_live.py` | `2B037AF820C6B3D037D4C2CAA23351BA0654AF4DCB2A4F48F259479FBE79F724` |

The production/test diff remains inside the authorized WP4 surface, including
the separately admitted MINOR-1 pair. No schema, model, migration, endpoint,
frontend, CLI, snapshot, `LedgerRepair`, replay/repair-framework, WP5+, M46, or
frozen-governance implementation change is present.

## 3. Prior-blocker determinations

| Finding | Second-renewed determination | Reason |
|---|---|---|
| `WP4-IIR-B1` | `PARTIALLY RESOLVED — BLOCKING` | The idle-Session transaction lifecycle is corrected and ordinary row projections are checked. Full canonical existing-row validity is still not established: registry-unresolved provider identifiers can establish retry authority, while a numerically valid legacy projection within the Design's `0.000001` storage tolerance is rejected because the implementation compares floats exactly. |
| `WP4-IIR-B2` | `PARTIALLY RESOLVED — BLOCKING` | Caller predecessor/successor listing symbols are replaced with registry symbols. Caller-controlled provider identity remains in the authoritative payload and fingerprint. |
| `WP4-IIR-B3` | `RESOLVED — PRESERVED` | Conflicting outgoing `MERGED_INTO` state is rejected without adding a second edge or mutating registry state; exact repeated preparation remains idempotent. |
| `WP4-IIR-B4` | `RESOLVED` | An already-active caller Session is rejected before conversion database access and is neither committed nor rolled back. Success uses one begin/one commit and returns closed; retry, conflict, invalid, stale, and forced-failure exits clean up. |
| `WP4-IIR-B5` | `PARTIALLY RESOLVED — BLOCKING` | E13 now enforces the tested top-level identity/numeric fields and registry state, but it validates the original parsed object rather than the transaction row's actual persisted `conversion_payload`. A post-flush payload corruption committed successfully. |
| `WP4-IIR-B6` | `PARTIALLY RESOLVED — BLOCKING` | LM-3, LM-4, and LM-11 now prove their named outcomes. EQ-1 still derives the live realized-P/L leg from `live_result["basis_carried"]`, which is populated directly from the input payload, rather than from the live materialized successor basis. The asserted result is numerically correct but is not the required independently derived live accounting outcome. |

Any remaining blocking partial/open finding prevents approval.

## 4. Transaction isolation and service ownership

The service checks `Session.in_transaction()` before its first database access.
With an unrelated pending `Workspace`, it raises the controlled idle-Session
error; the object remains pending in `Session.new`, the caller transaction
remains active, and no conversion query or mutation is performed. The caller
can subsequently commit its own work.

Connection events on a normal conversion are exactly:

```text
begin
commit
```

There is no post-commit refresh or ORM access. `Session.in_transaction()` is
false when the service returns. Matching retry explicitly finishes its
read-only transaction before returning. Conflict, invalid stored row, stale
quantity/basis, forced commit failure, and E13 failures roll back and return or
raise with no open transaction.

Repository-wide call-site search found no current production, endpoint, CLI,
or other authorized caller of `execute_position_conversion()`. Current calls
are confined to the focused test module. The idle-Session requirement therefore
does not silently break an existing caller contract.

**B4 determination:** `RESOLVED`.

## 5. Registry-authoritative payload evidence

The correction reads asset IDs first, resolves both assets, replaces
`predecessor.symbol` and `successor.symbol` in a deep-copied payload, then
parses, fingerprints, and persists that assembled payload. Adversarial
`CALLER-PREDECESSOR` and `CALLER-SUCCESSOR` labels do not survive in the
persisted payload, top-level transaction symbol, or successor holding, and two
such label variants retain matching retry identity.

The correction is incomplete for provider identity. A non-committed in-memory
probe supplied:

```text
quote_binding.provider = CALLER-PROVIDER-A
quote_binding.predecessor_provider_symbol = CALLER-PROVIDER-PRE-A
```

Both values persisted verbatim. Changing only those two values to a second set
caused the otherwise identical retry to be classified as a conflict. The
canonicalizer only requires
`quote_binding.successor_provider_symbol == successor.provider_symbol`, and E3
only validates that successor provider symbol against current registry state.
Neither layer registry-resolves the quote provider nor the predecessor provider
symbol. This violates the Authorization and Plan rule that symbols and provider
identifiers are registry-resolved rather than trusted from arbitrary input.

**B2 determination:** `PARTIALLY RESOLVED — BLOCKING`.

## 6. Existing-row validity before retry classification

The corrected helper checks workspace, portfolio, type, predecessor asset ID,
top-level predecessor symbol, transaction date, shares, price, amount, fees,
taxes, payload asset IDs, payload listing symbols, and transition date. Existing
payloads are reparsed and registry state is revalidated before fingerprint
comparison. The focused matrix proves malformed payloads and large individual
corruptions of supported top-level and payload fields fail as invalid state for
both equal- and unequal-incoming-fingerprint cases, with no mutation and closed
transactions.

Two adversarial gaps remain:

1. a stored payload carrying arbitrary `quote_binding.provider` and
   `quote_binding.predecessor_provider_symbol` is treated as valid and can
   establish matching or conflict authority; and
2. the frozen Design permits absolute top-level numeric storage deviation up
   to `0.000001`, but `_validate_conversion_transaction_projection()` uses
   exact float equality. A stored `shares` value of `2562.2140005`, within the
   authorized tolerance of the payload projection `2562.214`, was classified
   as invalid rather than a valid equal-fingerprint match.

Thus the implementation both accepts a canonically unauthorized provider
identity and rejects a canonically valid legacy numeric projection. Full valid
row status is not established before equality/inequality classification.

**B1 determination:** `PARTIALLY RESOLVED — BLOCKING`.

## 7. E13 final-invariant review

Independent post-flush probes mutated top-level transaction fields before E13:

| Mutation | Detection | Atomic rollback |
|---|---|---|
| predecessor `asset_id` and symbol | `PASS` | row absent; predecessor restored; successor absent; cash unchanged; transaction closed |
| numeric `price_per_share` | `PASS` | same |
| ownership `workspace_id` | `PASS` | same |
| `transaction_date` | `PASS` | same |

The original successor-basis corruption probe also passes, and final registry
revalidation is present.

However, E13 passes the pre-write typed `payload` object into
`_validate_conversion_transaction_projection()` and never parses or compares
`tx.conversion_payload` itself. A direct post-flush probe replaced the pending
row's payload predecessor symbol with `POST-FLUSH-CORRUPTION`. The service
returned `applied` and committed that corrupted authoritative payload together
with the successor state. The Plan-required canonical persisted payload and
row/payload agreement therefore remain fail-open at the sole commit boundary.

**B5 determination:** `PARTIALLY RESOLVED — BLOCKING`.

## 8. Accounting and parity evidence

| Evidence | Determination |
|---|---|
| LM-3 | `SATISFIED` — cumulative frozen-replay realized P/L is `250.0` before and after the no-CIL conversion; cash is unchanged. |
| LM-4 | `SATISFIED` — cumulative realized P/L increases exactly `0.28`; a matching retry adds no row and does not apply it again. |
| LM-11 | `SATISFIED` — the same named test proves successful row/state co-presence and forced-failure row/state co-rollback. |
| EQ-1 shares | `SATISFIED` |
| EQ-1 basis/average cost | `SATISFIED NUMERIC PARITY` |
| EQ-1 cash | `SATISFIED` |
| EQ-1 successor identity | `SATISFIED` |
| EQ-1 realized P/L | `INSUFFICIENT — BLOCKING` — live P/L uses a service return field copied from input payload basis rather than deriving basis from the live successor materialization; replay P/L is produced by the frozen replay engine. The equality `0.28` is correct but the two accounting outcomes are not independently derived as required. |
| Event-loop isolation | `SATISFIED` — the complete combined process has no event-loop contamination. |

**B6 determination:** `PARTIALLY RESOLVED — BLOCKING`.

## 9. RTO-1 through RTO-13

| Row | Determination | Reason |
|---|---|---|
| RTO-1 | `PARTIAL — BLOCKING` | One owned transaction lifecycle is proved, and ordering is otherwise visible. The complete common boundary is not satisfied while caller provider identifiers can enter canonical identity. |
| RTO-2 | `SATISFIED` | No-row execution retains E5/E6 before E9; stale quantity/basis writes nothing. |
| RTO-3 | `SATISFIED FOR A FULLY VALID ROW` | Equal regenerated fingerprint bypasses only E5/E6, mutates nothing, returns `already_applied`, and excludes successor state. |
| RTO-4 | `SATISFIED FOR A FULLY VALID ROW` | Unequal regenerated fingerprint bypasses only E5/E6, mutates nothing, and raises controlled conflict. |
| RTO-5 | `PARTIAL — BLOCKING` | The version-1 parser is used, but registry-unresolved provider identity remains parser-valid and can establish disposition. |
| RTO-6 | `SATISFIED` | Stored and incoming fingerprints use the sole canonical implementation; no detached or alternate digest exists. |
| RTO-7 | `PARTIAL — BLOCKING` | Ordinary exact rows classify correctly, but a fully valid within-tolerance projection is rejected and arbitrary provider identity may classify. |
| RTO-8 | `PARTIAL — BLOCKING` | Ordinary inequality conflicts correctly, but full canonical validity is not established first for the same reasons as RTO-7. |
| RTO-9 | `PARTIAL — BLOCKING` | Malformed and tested row inconsistencies fail closed; unsupported registry-unresolved provider states are accepted, and within-tolerance valid numeric state is rejected. |
| RTO-10 | `SATISFIED` | Matching no-op performs no mutation and returns with no open transaction. |
| RTO-11 | `SATISFIED` | Conflict performs no mutation and raises with no open transaction. |
| RTO-12 | `PARTIAL — BLOCKING` | Detected invalid states clean up deterministically, but not every supported invalid class is recognized before disposition. |
| RTO-13 | `SATISFIED` | Legitimate later successor-state changes do not affect retry classification or get repaired. |

The WP1 partial unique index remains unique over
`(portfolio_id, asset_id, transaction_date)` for
`transaction_type = 'POSITION_CONVERSION'`. Multiple rows at one canonical
identity remain structurally impossible and were not fabricated. This is not
treated as PD-WP4-4.

## 10. Previously satisfied findings

- **B3:** preserved; the conflicting-edge, no-second-edge, unchanged-state,
  normal preparation, and repeated-idempotency cases pass.
- **Valid matching/conflicting retry:** preserved for a fully valid exact row.
- **Successor-state exclusion:** preserved.
- **Basis-corruption rollback:** preserved.
- **Event-loop isolation:** preserved.
- **No endpoint/frontend/CLI authoring surface:** preserved by source scan and
  call-site search.
- **NEW-MINOR-A:** NMA-1 through NMA-4 pass; date derives solely from the
  payload calendar date as naive midnight and offset/time-bearing authoring
  input fails before insertion.

## 11. MINOR-1

Independent probes at Decimal precisions 10, 28, and 50 reproduced identical
values at every precision:

```text
fixture  09e4e2d3b9f3d5789dc14f2adea727f448cdca51f74e4b15b2e63d1f070374d0
A        03d66877530d70b1e2a3bb8a21ef4df4432504d0e82e0789f8b6774b7cc0d8ca
B        bfaa6a0586aa830914ff015d2993187c5a209d504e1fd157b8aa374c382d9a87
```

A and B remain distinct and each is stable across contexts. Repository search
found one payload-fingerprint implementation,
`transaction_canonicalizer._payload_fingerprint()`, and no WP4-local or
alternate fingerprint.

**MINOR-1 determination:** `SATISFIED — PRESERVED`.

## 12. Regression results

The claimed focused results reproduce:

```text
test_asset_registry.py + test_transaction_canonicalizer.py
+ test_position_conversion_live.py: 157 passed

test_position_conversion_live.py: 48 passed
```

Every operative Plan §6.3 suite was run in its own process:

```text
765 passed
1 failed
0 errors
```

The same complete list in one combined process produced:

```text
765 passed
1 failed
```

The sole failure in both modes is:

```text
backend/tests/test_portfolio_transactions_capability_shadow.py::
test_execute_buy_unaffected_by_capability_mismatch
```

It is the carried baseline logging assertion. The test file has no WP4 diff;
the `execute_buy()` body has no WP4 diff; transaction, holding, and cash
assertions pass; and the failure reproduces in isolation. It remains unrelated
and is not a new WP4 regression.

## 13. Scope and continuity audit

The current production/test changes remain the six authorized candidate files.
There is no unauthorized schema/migration, `backend/main.py`, endpoint,
frontend, CLI, snapshot, `LedgerRepair`, replay/repair framework, WP5+, M46, or
governance-byte change attributable to the candidate or this review.

WP1 continuity is preserved except for the two separately admitted MINOR-1
files. The protected WP1 members, WP2 six-file frozen corpus, and WP3 nine-file
frozen surface have no WP4 working-tree diff. The frozen governance identities
in §1 remain exact. Registry preparation remains separate E0 work; no
production conversion or snapshot/replay operation was executed.

This review changed no implementation or test byte. It created only this
additive review record. Nothing was staged, committed, pushed, merged,
released, or deployed.

## 14. Carried limitations and findings

- SQLite proves query issuance, transaction events, cleanup, rollback, and
  state behavior, not production-dialect row-lock semantics. PD-WP4-4 remains
  carried without expansion.
- The unrelated capability-shadow logging failure remains baseline-carried.
- Blocking findings remain B1, B2, B5, and B6 as stated above.
- RTO-1, RTO-5, RTO-7, RTO-8, RTO-9, and RTO-12 are not fully satisfied.

## 15. Second-renewed independent disposition

**`BANPU-WP4 CORRECTED IMPLEMENTATION CANDIDATE — NOT CONFIRMED`**

This is a second Renewed Independent Implementation Review disposition only.
It performs no Implementation Confirmation and does not call WP4 complete,
frozen, closed, release-ready, deployed, or production-authorized.

## 16. Exact next constitutional act

The exact next act is **bounded BANPU-WP4 implementation and evidence
correction under the existing Implementation Authorization**, limited to:

1. assembling every authoritative provider identifier from registry state so
   arbitrary caller provider text cannot persist or alter fingerprint/retry
   identity;
2. applying the Design's `0.000001` absolute storage tolerance when validating
   legacy top-level numeric projections before retry classification;
3. validating the actual pending transaction row's persisted
   `conversion_payload` and exact canonical payload identity at E13; and
4. deriving EQ-1 live realized P/L from live materialized cash and successor
   basis outcomes rather than from payload-derived service return fields.

After those bounded corrections and a complete evidence matrix, another
renewed Independent Implementation Review is required. Implementation
Confirmation remains a separate later act.
