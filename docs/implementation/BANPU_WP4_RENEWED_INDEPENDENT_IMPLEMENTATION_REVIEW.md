# BANPU-WP4 — Renewed Independent Implementation Review

**Artifact class:** Additive renewed independent implementation review record
**Review date:** 2026-08-13
**Review authority:** Renewed Independent Implementation Reviewer
**Review disposition:** `BANPU-WP4 CORRECTED IMPLEMENTATION CANDIDATE — NOT CONFIRMED`
**Implementation Confirmation performed:** `NO`
**Freeze, closeout, release, deployment, or production execution performed:** `NO`
**WP5+ or M46 authority exercised:** `NONE`

---

## 1. Authority and candidate identity

The live governance identity gate was independently recomputed from repository
bytes and passed:

| Artifact | Raw SHA-256 | Result |
|---|---|---|
| Original Work Package Plan | `F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE` | `EXACT` |
| Retry-order Plan amendment | `52254EB873CB57A5B3C30E62897878CAC20A23DCEDC2AAF2E5EB969D5C1C4168` | `EXACT` |
| Plan-amendment independent reapproval | `2258C1C3F40714FD371121645C3DECB2CA72946E825D816B789B586C2A5BFBF1` | `EXACT` |
| Retry-order governance decision | `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB` | `EXACT` |
| Amendment binding/freeze record | `5E312392767737C8F0445F51182B32A87B2EDF42B4C886BFB0296164EE389669` | `EXACT` |
| Implementation Authorization | `D8E89048BDC3B939731523937C8122A25E9659EDD5CE5B28F48DEAD022A6BCFA` | `EXACT` |
| Original Independent Implementation Review | `D1033DC13E8BF6D0F7AEA39AFFC4EE660FC962AE24A9B6D96521B1FA0CB91450` | `EXACT` |

The operative Plan is the original Plan plus the exact independently
reapproved additive amendment for §§3.2, 6, and 9. The independent reapproval
expressly permits implementation reliance on authoritative `E8-R` under the
existing bounded WP4 Implementation Authorization.

The corrected implementation/test candidate reviewed from live bytes is:

| Candidate file | Raw SHA-256 |
|---|---|
| `backend/services/asset_registry.py` | `16A5CECA8C0E0DA94A002C3D5C7F18D2DD7FEF89113C2D1AE837112212097B70` |
| `backend/services/portfolio_transactions.py` | `BBACA7BE62D8D468E53FED77D02C86B2A9D776DBDE66DDA8FC1A5BF884ACA031` |
| `backend/services/transaction_canonicalizer.py` | `0EA60A06C4224A303DB4B7EEFAA4A5A7D5596E4BA971F468D62B2BA278C60DFD` |
| `backend/tests/test_asset_registry.py` | `48267B7D3ECFE0375B7113E7239DA4B572EA424E67B3885C4DD2376D2BF07E16` |
| `backend/tests/test_transaction_canonicalizer.py` | `EDF2CF8C691DF7DA5AA265CD61F8137EC9E885D41E66A49186D568ECD07F0627` |
| `backend/tests/test_position_conversion_live.py` | `2B2224B597A3BA4973653C1749D4DC044978F65A0BEA9507F90F8F936850FC61` |

No implementation report was accepted as proof. The complete live diff, code,
tests, database behavior, transaction events, and adversarial cases were
reviewed independently.

## 2. Original blocker determinations

| Original finding | Renewed determination | Reason |
|---|---|---|
| `WP4-IIR-B1` | `PARTIALLY RESOLVED — BLOCKING` | The authorized E8-R order is present for ordinary valid invocation classes, but the common boundary does not own an isolated transaction lifecycle and invalid-but-well-formed existing rows can establish retry authority. |
| `WP4-IIR-B2` | `PARTIALLY RESOLVED — BLOCKING` | Registry symbols now control holding lookup, top-level transaction symbol, and successor holding label. False caller symbols nevertheless remain in the persisted authoritative `conversion_payload` and therefore affect its canonical fingerprint and retry disposition. |
| `WP4-IIR-B3` | `RESOLVED` | Conflicting outgoing `MERGED_INTO` is detected before preparation mutation; no second edge is inserted; state remains unchanged; exact repeated preparation remains idempotent. |
| `WP4-IIR-B4` | `PARTIALLY RESOLVED — BLOCKING` | Matching, conflict, malformed payload, registry, stale-state, and forced-write failures now roll back. A successful call performs a commit, then ORM refreshes begin a second transaction and the function returns with it open. The service also joins and commits a caller's already-active transaction. |
| `WP4-IIR-B5` | `PARTIALLY RESOLVED — BLOCKING` | The successor-basis assertion is corrected and the original corruption probe rolls back atomically. E13 still does not assert canonical transaction-row identity; an adversarial mutation of top-level `asset_id` and `symbol` committed successfully. |
| `WP4-IIR-B6` | `OPEN — BLOCKING` | The numerical test run passes except for the carried baseline failure, but LM-3, LM-4, LM-11, EQ-1, RTO-1, RTO-7/8, RTO-9, and RTO-12 do not collectively prove their mandatory descriptions. |

Any blocking partial or open finding prevents confirmation.

## 3. B1 and E8-R review

For an ordinary invocation, `execute_position_conversion()` performs portfolio
ownership and lock, payload parse, registry asset resolution, relevant-item
locks, complete E3 validation, transition-date construction, MINOR-1/fingerprint
gate, and identity lookup before E8-R. No-prior-row execution retains E5/E6;
stale quantity and basis fail before write; E9 is the first conversion write;
E9 precedes E10–E12; E13 precedes the sole business commit.

For one ordinary existing row, the implementation reads
`conversion_payload`, reparses it with
`parse_position_conversion_payload()`, obtains the regenerated fingerprint
from that sole canonicalizer, and compares it exactly with the incoming
fingerprint. Repository search found no detached digest column, caller-provided
fingerprint authority, partial comparison, alternate hash, or WP4-local hash.

The valid-row invocation classes behave as follows:

- no prior row: E5/E6 are mandatory; stale state fails before mutation;
- matching retry: only E5/E6 are bypassed, no business mutation occurs,
  cleanup rolls back, and `already_applied` is returned;
- conflicting retry: only E5/E6 are bypassed, no repair occurs, controlled
  conflict raises, and cleanup rolls back; and
- successor materialized state is not consulted as the retry predicate.

Two mandatory common-boundary/invalid-state properties fail:

1. The function does not establish an isolated service-owned transaction.
   With an unrelated caller-authored `Workspace` pending in the supplied
   Session, the conversion's commit also committed that unrelated row. On an
   ordinary successful application, SQLAlchemy connection events observed two
   transaction begins and one commit; trailing `db.refresh(tx)` and
   `db.refresh(portfolio)` opened the second transaction, and
   `Session.in_transaction()` was `True` when the function returned.
2. A structurally possible row with a fully parseable matching payload but
   corrupted top-level `workspace_id`, `symbol`, `shares`, `price_per_share`,
   `total_amount`, `fees`, and `taxes` was accepted as `already_applied`.
   E8-R validates the payload internally but never validates the existing row
   against its payload projections and canonical row identity. Such an
   inconsistent row must establish neither match nor conflict authority.

Therefore B1 is only partially resolved.

## 4. Registry determinations

### 4.1 Conflicting `MERGED_INTO` preparation

`prepare_position_conversion_registry()` queries all outgoing relationships
and rejects a `MERGED_INTO` target other than the requested successor before
identifier attachment, retirement, status transition, or relationship
creation. The focused adversarial cases pass: the original edge remains the
sole edge, successor/predecessor registry state remains unchanged by the
rejected call, and identical repeated preparation is idempotent.

**Determination:** `WP4-IIR-B3 RESOLVED`.

### 4.2 Registry-resolved symbols

Asset IDs now drive registry lookup. Registry `display_symbol` (falling back to
`canonical_symbol`) drives holding lookup, top-level `Transaction.symbol`, and
successor `PortfolioItem.symbol`. False caller symbols cannot redirect those
three surfaces.

However, the service inserts `conversion_payload=conversion_payload`, the raw
caller object. An adversarial call with `CALLER-PREDECESSOR` and
`CALLER-SUCCESSOR` committed those exact strings inside the authoritative
stored payload. That payload is also the fingerprint input, so caller strings
remain persisted identity/fingerprint authority. Plan E4 instead requires
registry resolution before the assembled payload is parsed and persisted.

**Determination:** `WP4-IIR-B2 PARTIALLY RESOLVED — BLOCKING`.

## 5. Transaction lifecycle (B4)

Code inspection and probes produced:

| Exit | Transaction state on return/raise | Determination |
|---|---|---|
| Matching retry | closed after explicit rollback; transaction ID captured before rollback | correct cleanup |
| Conflicting retry | closed by outer rollback | correct cleanup |
| Malformed stored payload | closed by outer rollback | correct cleanup |
| Registry validation failure | closed by outer rollback | correct cleanup |
| Invalid payload after portfolio query/lock | closed by outer rollback | correct cleanup |
| Stale quantity | closed by outer rollback; no write | correct cleanup |
| Stale basis | closed by outer rollback; no write | correct cleanup |
| Forced failure after writes / basis corruption | closed; row, holdings, and cash roll back | correct cleanup |
| Successful first application | one commit, then a second transaction opened by refresh; returned open | nonconforming |

Rollback terminates lock-bearing failure/no-op transactions, so their locks are
released. The successful path does not use exactly one transaction from entry
through return, and a caller's pre-existing transaction is neither rejected
nor isolated. A direct probe proved an unrelated pending caller write was
committed by the conversion service.

**Determination:** `WP4-IIR-B4 PARTIALLY RESOLVED — BLOCKING`.

## 6. E13 final-state enforcement (B5)

The original successor-basis adversarial probe was independently reproduced by
changing refreshed successor `avg_cost` to `999.0` immediately before E13.
E13 raised `post-write successor basis invariant failed`; no conversion row
committed; the predecessor remained; no successor remained; cash stayed
`500.0`; and the Session transaction was closed. The corrected basis assertion
therefore works and rollback is atomic.

E13 asserts predecessor removal, successor shares, successor basis, successor
asset ID, and cash. It does not assert the new transaction row's canonical
identity or its top-level/payload projection agreement, and it does not
revalidate required registry state at the final boundary. An adversarial
post-flush mutation changed the pending conversion row's top-level `asset_id`
from predecessor to successor and its symbol to `CORRUPTED`; the service
returned `applied` and committed the inconsistent row while the payload still
named the predecessor asset ID.

**Determination:** `WP4-IIR-B5 PARTIALLY RESOLVED — BLOCKING`.

## 7. Mandatory evidence matrix (B6)

The focused live matrix reports `29 passed`. The count is genuine, but complete
mandatory evidence is not:

| Evidence | Determination |
|---|---|
| LM-1, LM-2 | satisfied |
| LM-3 | not fully proved: it inspects an unrelated prior SELL in isolation and absence of a conversion note/result field, rather than comparing cumulative realized-P/L outcome before and after the no-CIL conversion |
| LM-4 | not fully proved: it asserts the input/stored payload's `realized_pnl` and equation, not that the realized-P/L outcome is applied exactly once |
| LM-5 through LM-10 | satisfied |
| LM-11 | still weaker than described: it proves only successful row/state co-presence; LM-10 supplies rollback evidence, but the named bidirectional matrix assertion itself remains absent |
| LM-12 | satisfied |
| LM-13 | satisfied; backend entry points and frontend source are scanned and independent repository search found no authoring surface |
| LM-14, LM-15 | ordinary matching/conflict behavior satisfied; broader E8-R validity defects remain |
| NMA-1 through NMA-4 | satisfied |
| M1-1 through M1-4 | satisfied |
| EQ-1 materialized shares/basis/cash/identity | satisfied |
| EQ-1 realized P/L | not proved: both paths are seeded with the same payload and the test compares the same input field re-read from each stored row, not independently computed live and replay realized-P/L outcomes |
| EQ-1 event-loop isolation | satisfied; a fresh current loop is restored and the combined process no longer produces fee-accounting loop failures |

**Determination:** `WP4-IIR-B6 OPEN — BLOCKING`.

## 8. RTO-1 through RTO-13

| Row | Determination | Independent reason |
|---|---|---|
| RTO-1 | `PARTIAL — BLOCKING` | Ordering of the database/common elements and E7 before E8-R is visible, but the transaction lifecycle is not isolated/service-owned and the test exercises only E3 ordering rather than the complete boundary. |
| RTO-2 | `SATISFIED` | No-row path executes E5/E6 before E9; stale quantity/basis produce no write. |
| RTO-3 | `SATISFIED FOR A VALID ROW` | Equal regenerated fingerprint bypasses only E5/E6, mutates nothing, returns `already_applied`, and ignores successor state. |
| RTO-4 | `SATISFIED FOR A VALID ROW` | Unequal regenerated fingerprint bypasses only E5/E6, mutates nothing, and raises controlled conflict. |
| RTO-5 | `SATISFIED FOR PAYLOAD VALIDATION` | Stored payload is reparsed through the complete version-1 typed parser. Existing-row projection consistency is the separate RTO-9 failure. |
| RTO-6 | `SATISFIED` | Both fingerprints come from the sole canonical parser/algorithm; caller fingerprint fields are rejected; no alternate digest exists. |
| RTO-7 | `PARTIAL — BLOCKING` | Equality classifies an ordinary valid row correctly, but is incorrectly treated as sufficient when the existing row is inconsistent with its payload. |
| RTO-8 | `PARTIAL — BLOCKING` | Inequality classifies an ordinary valid row correctly, but row validity is not first established, so an inconsistent row can be misclassified as conflict rather than invalid. |
| RTO-9 | `OPEN — BLOCKING` | Malformed payload fails closed, but a parseable payload on an inconsistent existing row is accepted as a match. |
| RTO-10 | `SATISFIED` | Matching return rolls back, captures ID before expiration, leaves no open transaction, and performs no mutation. |
| RTO-11 | `SATISFIED` | Ordinary controlled conflict rolls back and leaves no open transaction or mutation. |
| RTO-12 | `PARTIAL — BLOCKING` | Malformed stored payload cleans up, but other supported invalid state is not recognized as invalid and therefore does not produce the required fail-closed invalid-state disposition. |
| RTO-13 | `SATISFIED` | Later successor share/basis perturbation does not affect retry classification or get overwritten. |

### 8.1 RTO-9 multiple-row limitation

The WP1 partial unique index is genuinely unique over
`(portfolio_id, asset_id, transaction_date)` where
`transaction_type = 'POSITION_CONVERSION'`, and the conversion-specific check
requires non-null asset/date with naive midnight. Multiple rows at one
canonical identity are structurally impossible in the authorized persistence
model. Not fabricating that impossible state is acceptable and is not treated
as equivalent to PD-WP4-4.

That limitation does not satisfy RTO-9 as a whole. Inconsistent top-level row
projections, row workspace identity, and payload/row agreement are supported
states not prohibited by that unique index. The adversarial valid-payload,
invalid-row probe demonstrates an actual missing RTO-9 case.

## 9. MINOR-1 and NEW-MINOR-A

Independent precision probes at Decimal precisions 10, 28, and 50 reproduced
the same values on every run:

```text
fixture  09e4e2d3b9f3d5789dc14f2adea727f448cdca51f74e4b15b2e63d1f070374d0
A        03d66877530d70b1e2a3bb8a21ef4df4432504d0e82e0789f8b6774b7cc0d8ca
B        bfaa6a0586aa830914ff015d2993187c5a209d504e1fd157b8aa374c382d9a87
```

A and B remain distinct, each is stable across contexts, and the established
fixture is unchanged. Repository search found exactly one canonical payload
fingerprint implementation.

**MINOR-1:** `SATISFIED`.

The service accepts no separate transaction datetime, derives the row datetime
only from the parsed payload calendar date, constructs naive midnight, and
rejects offset/time-bearing transition-date input before business write. Direct
payload-date equality is retained.

**NEW-MINOR-A / NMA-1 through NMA-4:** `SATISFIED`.

## 10. Regression result

The canonical §6.3 suites were run in separate processes. Aggregate result,
after directing pytest's temporary fixture directory to a writable review
location, was:

```text
746 passed
1 failed
```

The sole failure was:

```text
test_portfolio_transactions_capability_shadow.py::
test_execute_buy_unaffected_by_capability_mismatch
```

The same complete suite list in one combined process produced `746 passed,
1 failed`; no event-loop/order contamination remained. The focused
`test_position_conversion_live.py` result was `29 passed`.

The remaining failure is the same logging assertion recorded by the original
independent review and reproduces in isolation. The test file is unchanged by
WP4. The live diff adds imports and appends the conversion service after the
pre-existing executors; the `execute_buy()` body and its logging behavior have
no WP4 diff. This is a carried pre-existing unrelated failure, not a new WP4
regression. No new regression failure was observed.

## 11. Scope and continuity audit

The candidate production/test diff is confined to the six files identified in
§1. There is no candidate change to schema/migrations, `backend/main.py`,
frontend, CLI, snapshots, `LedgerRepair`, replay/repair framework, WP5+, M46,
or frozen governance bytes. Registry preparation remains a separate E0 act;
the live service does not prepare, replay, repair, reconcile, rebuild
snapshots, or expose a public endpoint.

The original Plan, additive amendment, reapproval, governance decision,
binding/freeze, Allocation, Authorization, and original review identities
remain exact. WP2's six-file corpus and WP3's nine-file frozen surface have no
WP4 working-tree changes. WP1 changes remain limited to the two independently
admitted MINOR-1 files; the other ten frozen members are outside the candidate
diff. This review changed no implementation or test byte.

## 12. Remaining limitations and findings

- SQLite proves query issuance, cleanup, and state behavior, not production
  row-lock semantics; PD-WP4-4 remains carried without expansion.
- The single capability-shadow logging failure remains carried from the WP4
  entry baseline.
- Blocking findings remain B1, B2, B4, B5, and B6 as described above.
- RTO-1, RTO-7, RTO-8, RTO-9, and RTO-12 are not fully satisfied.

## 13. Renewed independent disposition

**`BANPU-WP4 CORRECTED IMPLEMENTATION CANDIDATE — NOT CONFIRMED`**

This is an Independent Implementation Review disposition only. It performs no
Implementation Confirmation and does not call WP4 complete, frozen, closed,
release-ready, deployed, or authorized for production conversion.

## 14. Exact next constitutional act

The exact next act is **bounded BANPU-WP4 implementation and evidence
correction under the existing Implementation Authorization**, limited to:

1. making the service transaction lifecycle isolated/service-owned and closed
   on every return without committing or rolling back unrelated caller work;
2. resolving and persisting canonical payload symbols from registry authority;
3. validating every existing transaction row against its stored payload and
   canonical row/projection invariants before equality/inequality may classify
   it;
4. enforcing canonical transaction identity at E13; and
5. replacing the remaining LM/EQ/RTO evidence gaps with outcome-based proofs.

After those corrections and the complete matrix, another renewed Independent
Implementation Review is required. Implementation Confirmation remains a
separate later act.
