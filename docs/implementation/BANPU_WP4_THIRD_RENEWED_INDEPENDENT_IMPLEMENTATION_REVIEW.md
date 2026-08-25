# BANPU-WP4 — Third Renewed Independent Implementation Review

**Artifact class:** Additive renewed Independent Implementation Review record
**Review date:** 2026-08-13
**Review authority:** Renewed Independent BANPU-WP4 Implementation Review Authority
**Entry claim:** `BANPU-WP4 CORRECTED IMPLEMENTATION CANDIDATE — READY FOR ANOTHER RENEWED INDEPENDENT REVIEW`
**Independent disposition:** `BANPU-WP4 IMPLEMENTATION CANDIDATE — INDEPENDENTLY APPROVED`
**Implementation Confirmation performed:** `NO`
**Freeze, closeout, release, deployment, production execution, WP5+, or M46 authority:** `NONE`

---

## 1. Boundary and method

This authority is independent from the implementation, correction, and
provider-identity governance authorities. The entry disposition was treated as
a claim. No implementation or test code was modified, no defect was corrected,
no earlier record was amended, and nothing was staged, committed, pushed,
merged, deployed, or executed against production data.

The review independently read and hashed the governance chain and six-file
candidate; applied the complete operative authority including PIA-1 through
PIA-4; inspected implementation behavior; ran direct in-memory SQLite probes;
ran focused and full regression matrices; audited scope and continuity; and
inspected Graphify without disabling its shrink guard.

## 2. Independent entry identities

Every identity was recomputed from live repository bytes before evaluation.

| Artifact | SHA-256 | Bytes | Lines |
|---|---|---:|---:|
| [Original Plan](BANPU_WP4_WORK_PACKAGE_PLAN.md) | `F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE` | 30,266 | 475 |
| [Retry-order amendment](BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT.md) | `52254EB873CB57A5B3C30E62897878CAC20A23DCEDC2AAF2E5EB969D5C1C4168` | 18,701 | 300 |
| [Independent reapproval](BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT_INDEPENDENT_REAPPROVAL.md) | `2258C1C3F40714FD371121645C3DECB2CA72946E825D816B789B586C2A5BFBF1` | 17,620 | 307 |
| [Retry-order governance decision](BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md) | `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB` | 20,350 | 420 |
| [Retry-order independent review](BANPU_WP4_RETRY_ORDER_AMENDMENT_INDEPENDENT_REVIEW.md) | `54C3CAC4DD263CEABA1ED70211529C56839A3C27D4A054A964DD3C68135463B4` | 22,686 | 417 |
| [Retry-order confirmation](BANPU_WP4_RETRY_ORDER_AMENDMENT_CONFIRMATION.md) | `41E1A23C5C09D095686E5675A37CF5DC191802060DC9BB104A99D2EEC2574BC8` | 17,832 | 363 |
| [Binding/freeze record](BANPU_WP4_RETRY_ORDER_AMENDMENT_BINDING_FREEZE_RECORD.md) | `5E312392767737C8F0445F51182B32A87B2EDF42B4C886BFB0296164EE389669` | 17,306 | 348 |
| [Allocation Record](BANPU_WP4_ALLOCATION_RECORD.md) | `CEE6F01C4113697BE6485AE56BB80FE0E9E99CB8555C08BC5D3E3CD67B94BAA9` | 11,180 | 214 |
| [Implementation Authorization](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md) | `D8E89048BDC3B939731523937C8122A25E9659EDD5CE5B28F48DEAD022A6BCFA` | 17,221 | 321 |
| [Roadmap §1 confirmation](BANPU_WP4_ROADMAP_SECTION_1_REVIEWER_CONFIRMATION.md) | `361492715FCB70E4B7AFD8F2905BA83A37795AFFDA666828F7767890FB6885EB` | 14,303 | 305 |
| [Original IIR](BANPU_WP4_INDEPENDENT_IMPLEMENTATION_REVIEW.md) | `D1033DC13E8BF6D0F7AEA39AFFC4EE660FC962AE24A9B6D96521B1FA0CB91450` | 21,397 | 421 |
| [Prior renewed IIR](BANPU_WP4_RENEWED_INDEPENDENT_IMPLEMENTATION_REVIEW.md) | `AD6017FFCFA4CC0D23BBFDA51B0F387C8E4CA0351BECE47CF96FC216F42845F3` | 19,890 | 335 |
| [Second-renewed IIR](BANPU_WP4_SECOND_RENEWED_INDEPENDENT_IMPLEMENTATION_REVIEW.md) | `994512F5E0C859C1E7406753C4B91A2DC92150D3745309B305A9E2791387DC3A` | 19,188 | 337 |
| [Provider-identity decision](BANPU_WP4_PROVIDER_IDENTITY_GOVERNANCE_DECISION.md) | `3B5C081A8CE9BBD08B6DD2BF1985A6DB9556DE1B0572D316D34EDA41967CDFE9` | 35,319 | 643 |
| [Historical Design](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md) | `2D2ECE4391961C85DE4076091662C66DA4586C553C6CDD57094970168BF1CE76` | 28,653 | 474 |

All were exact. The two identities supplied to this review matched exactly.

### 2.1 Exact candidate reviewed

| Candidate file | SHA-256 | Bytes | Lines |
|---|---|---:|---:|
| `backend/services/asset_registry.py` | `A603E193E883184FAEB19B9C08BA711DD9A3364AF7E6FC94D0EAF3F60EED705A` | 26,163 | 583 |
| `backend/services/portfolio_transactions.py` | `10C504D8D27AA310B5DA6DF595FCED5CBBB8776B4D1BA98CA390FE12E03D5379` | 69,925 | 1,625 |
| `backend/services/transaction_canonicalizer.py` | `0EA60A06C4224A303DB4B7EEFAA4A5A7D5596E4BA971F468D62B2BA278C60DFD` | 32,177 | 745 |
| `backend/tests/test_asset_registry.py` | `785BBE04596867274689554E8FB790CBBFFA080880FB2188F430ECA004D7EDDE` | 29,301 | 699 |
| `backend/tests/test_transaction_canonicalizer.py` | `EDF2CF8C691DF7DA5AA265CD61F8137EC9E885D41E66A49186D568ECD07F0627` | 30,002 | 818 |
| `backend/tests/test_position_conversion_live.py` | `FF7CE1F40B7D62B1D692698054559C8BD5EC86EA2898B2E6914A25D7236918D8` | 85,502 | 1,804 |

The live and focused counts are 65 and 179; the PIA vectors are present; and
the full matrix totals 787 passed plus the one carried baseline failure. No
material entry mismatch required a stop.

## 3. PIA-1 through PIA-4

| Rule | Independent determination |
|---|---|
| PIA-1 | `SATISFIED`. Registry authority governs exactly `predecessor.symbol`, `successor.symbol`, `successor.provider_symbol`, `quote_binding.successor_provider_symbol`, and `quote_binding.predecessor_provider_symbol`. |
| PIA-2 | `SATISFIED`. `quote_binding.provider` is not registry-resolved and is not derived from `AssetIdentifier.source`, `PRICE_PROVIDER`, or runtime provider configuration. |
| PIA-3 | `SATISFIED`. Provider remains required, string-typed, non-empty after stripping, persisted as authored evidence, and fully fingerprinted. |
| PIA-4 | `SATISFIED`. A valid provider-only change at the same conversion identity regenerates a different fingerprint and yields controlled conflict without mutation. |

A first-application probe supplied false listing labels and a false predecessor
provider symbol. The persisted five PIA-1 values were respectively `BANPU.BK`,
`BANPUU.BK`, `BANPUU.BK`, `BANPUU.BK`, and `BANPU.BK`; the authored provider
persisted unchanged. A false, internally consistent successor provider-symbol
pair failed before business writes. Existing parseable rows with corrupted
predecessor or successor provider-symbol authority establish neither match nor
conflict and fail closed.

## 4. B1 through B6

### 4.1 B1 — `RESOLVED`

Ownership, transaction type, assets, symbols, and calendar identity remain
exact. Absolute `Decimal("0.000001")` tolerance applies only to shares, price
per share, total amount, fees, and taxes. The boundary is inclusive.

Independent deltas against `2562.214` produced:

| Delta | Valid |
|---:|---|
| `0`, `+0.0000009`, `+0.0000010` | yes |
| `+0.0000011` | no |
| `-0.0000009`, `-0.0000010` | yes |
| `-0.0000011` | no |

The validator is shared by E8-R and E13; retry and final validity remain strict.

### 4.2 B2 — `RESOLVED` under PIA-1 through PIA-4

Listing symbols are overwritten from Asset state. The predecessor provider
symbol comes from its retained historical `PROVIDER_SYMBOL` after E0 retirement.
The successor provider-symbol pair must satisfy the frozen parser and current
registry state at E3, E8-R, and E13. `quote_binding.provider` is correctly left
under PIA-2/PIA-3 and is not misclassified as registry identity.

### 4.3 B3 — `RESOLVED — PRESERVED`

The conflicting outgoing `MERGED_INTO` check precedes every preparation
mutation. Focused execution proved that conflict preserves the original edge
and complete registry state. Repeated identical preparation is idempotent.

### 4.4 B4 — `RESOLVED — PRESERVED`

Caller-owned pending work is rejected before conversion database activity; it
is neither committed nor rolled back. Successful service ownership emits one
begin and one commit. Matching, conflict, invalid, stale, and forced-failure
exits close the transaction. Result construction precedes commit and there is
no post-commit ORM refresh or second transaction.

### 4.5 B5 — `RESOLVED`

E13 reads the pending row's current `tx.conversion_payload`, reparses it through
the sole parser, regenerates its fingerprint, compares it to the intended E7
fingerprint, validates row projection from that reparsed payload, and revalidates
registry state immediately before the sole commit.

Independent post-flush mutations of `predecessor.symbol`,
`quote_binding.predecessor_provider_symbol`, and numeric canonical content were
all detected. Each rolled back the row, restored the predecessor, removed the
successor, preserved cash, and left the Session closed.

### 4.6 B6 — `RESOLVED`

LM-3 proves cumulative replay realized P/L is unchanged by no-CIL. LM-4 proves
the admitted CIL cash and `0.28` realized P/L apply once. LM-11 proves row/state
co-presence and complete co-rollback.

EQ-1 derives live realized P/L solely from pre-conversion materialized
predecessor shares × average cost, pre/post materialized cash, and
post-conversion successor shares × average cost. It does not use
`live_result["basis_carried"]`, payload basis, or the replay input. Replay P/L
comes independently from frozen replay cumulative state. The comparison covers
successor shares, basis/average cost, cash, realized P/L, and successor identity.

Reconstructing basis from `_f()`-quantized float columns produces about
`0.0008 THB` drift. The existing E6/E13 `0.01 THB` absolute accounting tolerance
is justified and cannot conceal the substantive `0.28 THB` outcome.

## 5. RTO-1 through RTO-13

| Row | Result | Independent basis |
|---|---|---|
| RTO-1 | `SATISFIED` | Full common boundary and E7 precede E8-R; success has one transaction and commit. |
| RTO-2 | `SATISFIED` | No row proceeds through E5/E6 before E9 or mutation. |
| RTO-3 | `SATISFIED` | One valid row with regenerated equal fingerprint returns `already_applied`. |
| RTO-4 | `SATISFIED` | One valid row with unequal fingerprint yields controlled conflict. |
| RTO-5 | `SATISFIED` | Stored payload, projection, and all five PIA-1 facts are revalidated first. |
| RTO-6 | `SATISFIED` | Sole canonical regeneration; payload schema rejects caller fingerprints. |
| RTO-7 | `SATISFIED` | Match bypasses only E5/E6 and performs no mutation or repair. |
| RTO-8 | `SATISFIED` | Conflict bypasses only E5/E6 and performs no mutation or repair. |
| RTO-9 | `SATISFIED` | Malformed, inconsistent, out-of-tolerance, or registry-corrupt rows establish no disposition. |
| RTO-10 | `SATISFIED` | Matching return leaves no open transaction or retained lock. |
| RTO-11 | `SATISFIED` | Conflict rolls back and leaves no open transaction or retained lock. |
| RTO-12 | `SATISFIED` | Every supported invalid-state exit is clean and mutation-free. |
| RTO-13 | `SATISFIED` | Later legitimate successor state is neither predicate nor repair target. |

The WP1 partial unique index was independently verified: it is unique over
`(portfolio_id, asset_id, transaction_date)` with a
`transaction_type = 'POSITION_CONVERSION'` predicate for SQLite and PostgreSQL.
Multiple rows at one canonical identity are structurally prevented; no
schema-invalid state was fabricated.

## 6. MINOR-1 and NEW-MINOR-A

MINOR-1 is `SATISFIED — PRESERVED`. There is exactly one position-conversion
fingerprint implementation, `transaction_canonicalizer._payload_fingerprint()`.
Live, retry, E13, and replay consume parser-produced fingerprints.

Independent results were identical at Decimal precisions 10, 28, and 50:

| Vector | SHA-256 |
|---|---|
| Fixture | `09e4e2d3b9f3d5789dc14f2adea727f448cdca51f74e4b15b2e63d1f070374d0` |
| A | `03d66877530d70b1e2a3bb8a21ef4df4432504d0e82e0789f8b6774b7cc0d8ca` |
| B | `bfaa6a0586aa830914ff015d2993187c5a209d504e1fd157b8aa374c382d9a87` |

A and B remain distinct and the fixture is stable at every precision.

NEW-MINOR-A is `SATISFIED — PRESERVED`. NMA-1 through NMA-4 pass: valid input
stores naive midnight equal to its calendar date; offset-bearing and
time-bearing input fail before insertion; host time, timezone, UTC conversion,
and session timezone do not participate.

## 7. Mandatory evidence and regression matrix

LM-1 through LM-15, M1-1 through M1-4, NMA-1 through NMA-4, EQ-1, and event-loop
isolation are all `SATISFIED`.

| Run | Result |
|---|---|
| Live module | `65 passed` |
| Focused three-file matrix | `179 passed` |
| Complete Plan §6.3, separate processes | `787 passed, 1 failed, 0 errors` |
| Complete Plan §6.3, combined process | `787 passed, 1 failed` |

The first separate run encountered two `tmp_path` setup errors because the
sandbox could not write the default Windows temporary directory. The unchanged
suite rerun with pytest's base temporary path in an authorized location produced
`28 passed`. These were environment permission errors, not candidate errors.

The sole real failure remains
`test_portfolio_transactions_capability_shadow.py::test_execute_buy_unaffected_by_capability_mismatch`.
It is the established missing-log assertion; holding, transaction, and cash
assertions pass. WP4 adds its service after existing transaction functions and
does not modify `execute_buy()`. The failure is unchanged and unrelated. There
are zero new unexplained regressions or event-loop contamination.

## 8. Scope and continuity

The only implementation/test changes are the six candidate files in §2.1. No
WP4 diff exists in schema/migrations, models, endpoints or `backend/main.py`,
frontend, CLI/manage code, snapshots, LedgerRepair, replay/repair framework,
WP5+, M46, or protected WP1/WP2/WP3 surfaces except the expressly admitted
conditional canonicalizer file and test.

The working tree also contains the pre-existing untracked WP4 governance and
review chain; this review did not create those records. Its only addition is
this artifact. Decision Log and Implementation INDEX contain no BANPU-WP4 entry
and have no diff, consistent with a review that performs no confirmation or
closeout.

WP1/WP2/WP3 continuity is `PRESERVED`: the valid comparison is absence of a WP4
diff on protected surfaces, not raw equality to the oldest freeze where later
accepted tracked revisions exist.

## 9. Graphify determination

The reported shrink-guard refusal was inspected without bypassing the guard.
The graph was already queryable and resolved corrected live symbols. A normal
`graphify update .` then completed successfully with 21,697 nodes, 42,074 edges,
and 1,743 communities. No shrink guard fired. Ignored graph outputs do not enter
the WP4 diff.

The earlier approximately 432-document incremental condition was a legitimate
protective no-write state when reported, but is not current, has no WP4
evidentiary consequence, needs no bypass, and reveals no synchronization drift.

## 10. Repository verification

| Check | Result |
|---|---|
| Authority and candidate identities | `PASS` — §2 |
| Governance artifacts unchanged during review | `PASS` |
| Implementation/test bytes unchanged during review | `PASS` |
| WP1/WP2/WP3 continuity | `PASS` |
| Decision Log / INDEX | `UNCHANGED`; no BANPU-WP4 entry |
| Relative links | `PASS`; all sibling targets exist |
| Fragment anchors | `NOT USED` |
| Trailing whitespace | `PASS` |
| `git diff --check` | `PASS` |
| `git diff --cached --check` | `PASS` |
| Staging | `EMPTY` |
| Commit, push, merge | `NONE` |
| Production execution or persistent data mutation | `NONE` |

## 11. Independent disposition

B1 through B6 are resolved. RTO-1 through RTO-13, MINOR-1, NEW-MINOR-A, and
the complete mandatory evidence and regression matrices satisfy the operative
Plan, independently reapproved amendment, Implementation Authorization, and
PIA-1 through PIA-4.

**`BANPU-WP4 IMPLEMENTATION CANDIDATE — INDEPENDENTLY APPROVED`**

This is Independent Implementation Review approval only. It does not itself
perform or authorize Implementation Confirmation, freeze, closeout, release,
deployment, production execution, WP5+, or M46 work.

## 12. Exact next constitutional act

**Separate BANPU-WP4 Implementation Confirmation against the exact six reviewed
candidate identities in §2.1 and this additive review record.**

This review does not perform that act.
