# BANPU-WP4 — Independent Implementation Review

**Artifact class:** Independent implementation review record
**Review date:** 2026-08-13
**Review authority:** Independent Implementation Reviewer
**Candidate claim reviewed:** `BANPU-WP4 IMPLEMENTATION CANDIDATE — READY FOR INDEPENDENT REVIEW`
**Review disposition:** `NOT CONFIRMED — BLOCKING FINDINGS`
**Implementation confirmation performed:** `NO`
**Freeze or closeout performed:** `NO`
**Release, deployment, production execution, or production-data authority:** `NONE`
**BANPU-WP5+ authority:** `NONE`
**M46 authority:** `NONE`

---

## 1. Review boundary and authority

This record independently reviews the BANPU-WP4 implementation candidate. It
does not act as implementer, planning authority, allocation authority,
authorization authority, implementation-confirmation authority, freeze
authority, or closeout authority.

The review applied, without amendment:

- [the canonical implementation design](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md);
- [the remediation work-package roadmap](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md);
- [the mandatory implementation sequence](BANPU_IMPLEMENTATION_SEQUENCE.md);
- the applicable frozen WP1, WP2, and WP3 records and implementation corpora;
- [the BANPU-WP4 Allocation Record](BANPU_WP4_ALLOCATION_RECORD.md);
- [the BANPU-WP4 Implementation Authorization Record](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md);
- [the BANPU-WP4 Work Package Plan](BANPU_WP4_WORK_PACKAGE_PLAN.md); and
- [the roadmap Section 1 reviewer confirmation](BANPU_WP4_ROADMAP_SECTION_1_REVIEWER_CONFIRMATION.md).

The implementation report was not accepted as proof. The live diff, production
code, test assertions, database behavior, precision behavior, regression
suites, and frozen identities were inspected or reproduced independently.

## 2. Candidate surface and scope result

The complete tracked implementation diff contains:

| Candidate file | Classification | Authority result |
|---|---|---|
| `backend/services/asset_registry.py` | WP4 production | Authorized file |
| `backend/services/portfolio_transactions.py` | WP4 production | Authorized file |
| `backend/services/transaction_canonicalizer.py` | Conditional MINOR-1 production | Admitted by roadmap Section 1 confirmation |
| `backend/tests/test_asset_registry.py` | WP4 focused tests | Authorized file |
| `backend/tests/test_transaction_canonicalizer.py` | Conditional MINOR-1 tests | Admitted by roadmap Section 1 confirmation |
| `backend/tests/test_position_conversion_live.py` | New focused WP4 live tests | Authorized file |
| `frontend/app/page.tsx` | Unrelated frontend work | Not BANPU-WP4; excluded from candidate assessment |
| `frontend/tests/Dashboard.test.tsx` | Unrelated frontend test appearing after the initial review snapshot | Not BANPU-WP4; excluded from candidate assessment |

No candidate change exists in a schema, model, migration, `backend/manage.py`,
public endpoint, `LedgerRepair`, snapshot service, cache service, WP5+ module,
or M46 file. Repository-wide reference search found no call or authoring surface
for `execute_position_conversion()` in `backend/main.py`, `backend/manage.py`,
backend routers, or frontend code. No frozen governance artifact was modified.

Scope-file containment therefore passes, but behavioral conformance does not:
the candidate implements unauthorized caller-controlled symbol behavior and
does not satisfy several mandatory authorized capabilities. The candidate is
not conforming merely because its changed filenames are allowlisted.

## 3. Blocking finding register

### `WP4-IIR-B1` — E8 executes before E5/E6 contrary to canonical runtime order

**Severity:** `BLOCKING — GOVERNANCE RESOLUTION REQUIRED`

The candidate parses and validates registry state, then evaluates fingerprint
idempotency and returns or conflicts before predecessor lookup and optimistic
quantity/basis validation. Its actual order is:

- first application: portfolio lock; payload parse; relevant-item locks;
  registry validation; date derivation; MINOR-1 gate; duplicate lookup; then
  predecessor lookup and optimistic checks; insert; predecessor removal;
  successor create/merge; CIL; final checks; commit;
- matching retry: portfolio lock; payload parse; relevant-item locks; registry
  validation; date derivation; MINOR-1 gate; duplicate lookup; immediate
  `already_applied` return; no E5 or E6;
- conflicting retry: the same path through duplicate lookup, followed by a hard
  failure and rollback; no E5 or E6; and
- stale-state attempt with no duplicate: the first-application order through
  E5/E6, where stale quantity or basis fails before a write.

The reorder preserves E7 before E8 and preserves E3/E6 before every write on a
first-application path. A retry does not bypass portfolio identity, payload
parsing, registry validation, date identity, or conflict detection. The
duplicate key is sufficiently scoped by portfolio, predecessor asset ID, and
transition date, and the full canonical fingerprint distinguishes payload
semantics.

Those properties do not make the reorder authorized. Canonical Design Section
9 orders predecessor location and optimistic verification before duplicate
evaluation. Work Package Plan Section 3.2 records E5 and E6 before E7/E8,
requires implementation through that runtime order, and Section 9 requires the
Section 3.2 runtime order to hold. The candidate's assertion that only four
cross-step rules are mandatory narrows the plan without authority.

LM-14 creates a real design tension because a successful first application
removes the predecessor holding. That tension does not authorize the
implementer or reviewer to rewrite the frozen order. A bounded decision by the
authority governing the canonical design and plan must explicitly resolve the
retry order, followed by any required planning amendment/reapproval. Existing
WP4 implementation authority alone cannot amend this ordering requirement.

### `WP4-IIR-B2` — caller-controlled symbols are trusted and persisted

**Severity:** `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY`

The canonical design and Work Package Plan require symbols and provider
identifiers to be registry-resolved rather than trusted from arbitrary input.
The candidate accepts a caller-assembled payload and uses
`payload.predecessor.symbol` and `payload.successor.symbol` to locate holdings,
write the transaction symbol, overwrite an existing successor symbol, or create
a successor holding.

A non-committed SQLite probe supplied otherwise valid asset IDs and registry
state but used payload symbols `CALLER-PREDECESSOR` and `CALLER-SUCCESSOR`. The
service returned `applied`, stored the transaction symbol as
`CALLER-PREDECESSOR`, and stored the successor holding symbol as
`CALLER-SUCCESSOR`.

The registry provider-symbol check does not resolve or validate these listing
symbols. This violates the frozen input/identity boundary and can bind arbitrary
caller text to canonical asset IDs. The service must resolve the authoritative
symbols and provider identifiers from registry state and construct/validate the
canonical payload accordingly, within the already authorized C-2/C-3/C-7/C-9
surface.

### `WP4-IIR-B3` — registry preparation can create a knowingly invalid double relationship

**Severity:** `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY`

`retire_identifier()` correctly reuses
`asset_repository.mark_identifier_not_current()`. The ordinary successful
preparation path is repeatable, establishes the successor provider identifier,
retires the predecessor identifier, transitions the predecessor to `MERGED`,
and reuses the existing status/relationship primitives. Validation is read-only
and fail-closed, and `execute_position_conversion()` validates rather than
prepares registry state.

However, preparation does not fail closed when the predecessor already carries
an outgoing `MERGED_INTO` edge to another asset. It calls the existing
pair-specific idempotent `link_relationship()`, which adds the requested edge
alongside the conflicting edge. A non-committed probe observed two outgoing
`MERGED_INTO` targets after preparation; the preparation call returned
successfully, while immediate validation failed because exactly one required
edge did not exist.

Preparation therefore does not always establish the state it promises and can
add mutation before exposing the conflict. It must reject a conflicting
relationship without creating a second edge. Focused registry tests must cover
that path. This correction belongs within existing C-1/C-2 authority and must
not change existing generic relationship semantics.

### `WP4-IIR-B4` — transaction scope is left open on matching retry and pre-handler parse failure

**Severity:** `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY`

The portfolio `SELECT ... FOR UPDATE` and payload parse occur before the
function's rollback-protected `try` block. An invalid payload therefore exits
after opening a database transaction but without rollback. The matching-retry
branch returns from inside the transaction after lock-bearing reads without
commit or rollback.

Starting each probe from `Session.in_transaction() == False` produced:

```text
matching retry result                  already_applied
transaction open after matching retry True
transaction open after invalid payload True
```

This violates the Work Package Plan's single owned E1–E13 transaction and its
rule that any failure from E1 rolls the complete unit back. It also makes the
required no-op disposition retain transaction/lock state in the caller's
session. The whole lock/parse/validation/idempotency path must be inside a
well-defined transaction cleanup boundary, including no-op and pre-write error
exits.

### `WP4-IIR-B5` — E13 omits the mandatory final basis assertion

**Severity:** `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY`

The candidate's E13 block asserts successor shares, successor asset ID, and
cash. It never recomputes or asserts final successor basis, even though C-11,
Canonical Design Section 9, and Work Package Plan E13 require final shares,
basis, cash, and identity assertions.

A non-committed probe altered the refreshed successor `avg_cost` to `999.0`
immediately before final assertions. The service returned `applied` and
committed `999.0`, proving the final block does not detect basis corruption.
The correction must assert the final successor basis using the applicable
canonical tolerance before the sole successful commit.

### `WP4-IIR-B6` — mandatory verification rows are not fully proved

**Severity:** `BLOCKING — TEST/EVIDENCE CORRECTION UNDER EXISTING WP4 AUTHORITY`

The test names do not equal the required evidence:

- LM-3 is named for cash and realized P/L but asserts only cash.
- LM-4 asserts net cash plus top-level fees/taxes, but does not assert that the
  admitted realized P/L is carried/applied exactly once.
- EQ-1 compares shares, average cost/basis proxy, cash, and successor identity,
  but explicitly omits realized P/L and assigns it to WP5. Work Package Plan
  EQ-1 expressly requires realized P/L comparison; the candidate cannot invent
  later-package ownership for that row.
- LM-13 scans backend entry surfaces but not frontend code. Independent review
  found no frontend authoring path, but the matrix test itself does not prove
  its full named surface.
- LM-11 proves successful row/state co-presence. Together with LM-10 and code
  inspection it supports transaction atomicity, but it does not directly
  exercise both named partial-state directions.
- the MINOR-1 parametrized test proves the baseline fingerprint is invariant
  and A/B remain distinct at each precision, but does not bind each A and B
  fingerprint to the same value across all tested precisions. Independent probe
  supplies that evidence; the eventual committed vector should state it
  directly.

These gaps prevent the Section 6 matrix and Section 9 exit criteria from being
declared complete. They can be corrected within the existing authorized test
surface; they do not authorize WP5 behavior.

## 4. Registry review disposition

Registry review is `PARTIALLY SATISFIED / BLOCKED BY WP4-IIR-B3`.

The existing repository retirement primitive is reused correctly. Successful
preparation is idempotent. Successor provider identity, predecessor retirement,
`MERGED` status, and the normal required relationship are established.
Validation is read-only and fail-closed. The live service performs validation
and never silently prepares. Existing generic primitives retain their previous
code and semantics. The conflicting-edge preparation case remains a blocking
defect.

## 5. Transaction, accounting, and atomicity review

First-application writes occur only after registry validation, predecessor
lookup, and optimistic quantity/basis checks. Portfolio and relevant existing
items receive `with_for_update()`. Quantity is exact and basis uses the
canonical THB `0.01` tolerance. E9 precedes predecessor removal, successor
create/merge, and CIL cash application. Transaction insertion and materialized
state share the same commit, and the forced-commit failure test demonstrates
rollback of the row, holdings, and cash.

Predecessor removal, successor creation, existing-successor combination,
combined shares/basis, average-cost calculation, sector carry, net CIL cash,
and top-level fee/tax projections are otherwise consistent with the authorized
accounting model. Historical transaction rows, including fixture transaction
83, are never updated by the service.

Transaction/atomicity disposition is nevertheless `BLOCKED` by
WP4-IIR-B2, B4, B5, and the realized-P/L evidence portion of B6.

## 6. MINOR-1 disposition

The admitted production change is confined to nonzero Decimal fingerprint
serialization. It uses exact `format(value, "f")` output and removes only
fractional trailing zeroes and a trailing decimal point. It performs no
context-applying Decimal arithmetic and changes no parser, schema, validation,
JSON encoding, hashing, timestamp, date, mapping, sequence, or zero branch.

Independent probes at precisions 10, 28, and 50 observed, identically at every
precision:

```text
A serialization   1.12345678901234567890123456781
B serialization   1.12345678901234567890123456782
A fingerprint     03d66877530d70b1e2a3bb8a21ef4df4432504d0e82e0789f8b6774b7cc0d8ca
B fingerprint     bfaa6a0586aa830914ff015d2993187c5a209d504e1fd157b8aa374c382d9a87
```

A and B parsed exactly and remained distinct. `0`, `-0`, `0.000`, and
`-0.000` all canonicalized to `0`. `1`, `1.0`, and `1.000` all canonicalized
to `1`; `1000` and `1000.000` both canonicalized to `1000`. The established
full-payload fingerprint remained:

```text
09e4e2d3b9f3d5789dc14f2adea727f448cdca51f74e4b15b2e63d1f070374d0
```

`MINOR-1` is technically satisfied at the WP4 pre-use point. That result does
not cure or authorize the E8/E5 runtime reorder and does not confirm WP4.

## 7. Idempotency disposition

The candidate uses one canonical fingerprint produced by the canonicalizer; no
WP4-local competing hash exists. Duplicate lookup uses portfolio ID,
predecessor asset ID, conversion type, and transition date, matching the
canonical database identity, then compares the full canonical fingerprint.
Matching retry performs no database write and returns `already_applied`;
conflicting retry fails hard. Precision-distinct payloads cannot collapse under
the corrected Decimal serializer.

The identity itself is sufficiently scoped. Idempotency disposition remains
`BLOCKED` because the activation point violates the unresolved canonical order
and the matching no-op leaves an open transaction.

## 8. NEW-MINOR-A disposition

`transaction_date` is not accepted as a separate caller argument. It derives
only from the parsed payload `valuation_transition_date` using
`datetime.combine(date, time.min)`. The stored value is naive midnight with no
host, session, UTC, or offset conversion. Offset-bearing and time-bearing date
strings fail the canonical date parser before insertion.

NMA-1 through NMA-4 pass and the authoring semantics satisfy `NEW-MINOR-A` at
the WP4 point. The invalid-payload transaction-cleanup defect is separately
recorded as WP4-IIR-B4. WP7 PostgreSQL coercion and WP8 release evidence are not
required by this review.

## 9. Verification-matrix and regression result

Focused suites run independently:

| Suite | Result |
|---|---:|
| `test_position_conversion_live.py` | `20 passed` |
| `test_asset_registry.py` | `32 passed` |
| `test_transaction_canonicalizer.py` | `72 passed` |

Every Work Package Plan Section 6.3 suite was then run in its own process, as
the plan's suggested command set specifies. Aggregate result:

```text
732 passed
1 failed
```

The sole separate-process failure is:

```text
test_portfolio_transactions_capability_shadow.py::
test_execute_buy_unaffected_by_capability_mismatch
```

It fails on the pre-existing logging assertion while transaction, holding, and
cash assertions pass. The test file and the existing `execute_buy()` body are
unchanged by WP4. The failure reproduces deterministically in isolation and is
consistent with the reported pre-implementation baseline; it is unrelated to
the added conversion path.

A single combined-process run produced `730 passed, 3 failed`: the same known
failure plus two fee-accounting event-loop failures. Both fee tests pass in
isolation. The new EQ-1 test calls `asyncio.run()`, which closes the process's
current loop before the later legacy fee tests call `get_event_loop()`. The
canonical command set uses separate processes, so this is not classified as a
new production regression, but it is a test-isolation observation that should
be corrected with the B6 evidence work.

Passing tests do not waive the blocking semantic and evidence findings above.

## 10. Locking limitation

The implementation issues row-lock requests over the portfolio and relevant
existing `PortfolioItem` rows and combines them with fail-closed optimistic
checks. SQLite tests demonstrate query issuance and stale-state refusal, not
production-dialect row-lock semantics.

Work Package Plan PD-WP4-4 explicitly records this as an accepted WP4 evidence
limitation, not an implementation-confirmation blocker, and assigns it to no
later package. This review preserves that exact treatment and invents no future
owner.

## 11. Repository and frozen-identity verification

- The candidate backend diff is confined to the six reported authorized files.
- `frontend/app/page.tsx` and `frontend/tests/Dashboard.test.tsx` are unrelated
  price-display work and are not absorbed into BANPU-WP4. The test path appeared
  after the initial review snapshot; this review did not create or modify it.
- No staged change exists.
- No schema/model/migration, CLI, endpoint, LedgerRepair, snapshot, cache, WP5+,
  M46, Decision Log, or Implementation INDEX change exists.
- WP1 canonical-LF identity: 10 unchanged members reproduce their frozen or
  corrected identities exactly; only the two explicitly admitted MINOR-1 files
  differ.
- WP2 canonical-LF continuity: all six members reproduce their committed blob
  identities and aggregate
  `6E50F5B5E2AAA008EA1C3DA25D1FC34C41F9CBAE81A293A463FB3F6BF5DA4159`.
- WP3 canonical-LF identity: all nine members and aggregate
  `E2C44B920D533D386FE3C470C48A8701806D14BA4C1866A7F9058C700FB0E7B8`
  reproduce exactly.
- WP4 Allocation, Authorization, Work Package Plan, and roadmap Section 1
  confirmation artifacts were not modified by this review.

Final hygiene results are recorded in the handoff after this additive record is
verified and the knowledge graph is refreshed. Nothing is staged or committed.

## 12. Independent review disposition

**`BANPU-WP4 IMPLEMENTATION CANDIDATE — NOT CONFIRMED`**

The candidate has six blocking findings. MINOR-1 and NEW-MINOR-A are satisfied,
the normal-path accounting is substantially implemented, the authorized
separate-process regression count is reproduced, and the locking limitation is
accepted as PD-WP4-4 records. Those positive results do not satisfy the Work
Package Plan exit criteria while the blocking findings remain.

This disposition performs no implementation confirmation, freeze, closeout,
release, deployment, production execution, production-data mutation, snapshot
rebuild, WP5+ allocation/authorization, or M46 act.

## 13. Exact next constitutional act

The immediate next constitutional act is a **bounded canonical governance
decision on WP4-IIR-B1** by the authority governing the frozen live-service
order. It must decide and record how matching retry can precede or conditionally
bypass predecessor lookup/optimistic checks without silently rewriting
Canonical Design Section 9 or Work Package Plan Sections 3.2 and 9. If the
order is changed, the required canonical design/planning amendment,
independent approval, and plan reapproval must occur before implementation
relies on it.

After that governance act, the implementation candidate returns to WP4 under
the existing bounded implementation authority for corrections B2 through B6
and for whatever implementation order the governance act authorizes. A renewed
independent implementation review is required after all corrections and the
complete verification matrix pass. Implementation confirmation remains a
separate later act.
