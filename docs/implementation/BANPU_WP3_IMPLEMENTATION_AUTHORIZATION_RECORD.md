# BANPU-WP3 — Implementation Authorization Record

**Artifact class:** Additive constitutional authorization record
**Record class:** Transcription of an authorization act already performed
**Authorization date:** 2026-08-10
**Record date:** 2026-08-10
**Disposition:** `BANPU-WP3 IMPLEMENTATION AUTHORIZED`
**Authorized work package:** `BANPU-WP3 — Quote identity and epoch protection`
**Authorized planning corpus identity:** `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
**New authority created by this record:** `NONE`
**WP4+ authority:** `NONE`

## 1. Nature of this record

This artifact **records an authorization act already performed** and **grants no
new authority**.

The BANPU-WP3 Implementation Authorization was performed on 2026-08-10 by the
BANPU-WP3 Implementation Authorization Authority, acting over the allocated
planning corpus identified in §4. That act completed with the disposition
`BANPU-WP3 IMPLEMENTATION AUTHORIZED`. It was performed under an instruction
prohibiting repository modification, so it created no durable artifact at the
time. This record supplies that artifact.

Accordingly, this record:

- does **not** re-authorize implementation;
- does **not** re-decide, re-verify, or reinterpret the authorization;
- does **not** widen, narrow, or restate the authorized scope in any way that
  differs from the act;
- does **not** amend any frozen artifact; and
- performs **no** new constitutional determination beyond the identity checks in
  §17 that are necessary to confirm this transcription names the correct act and
  the correct corpus.

If any statement in this record were to diverge from the act it transcribes, the
act governs and this record is in error.

## 2. Constitutional authority

Authority for the transcribed act derives from the completed
[BANPU-WP3 Allocation Record](BANPU_WP3_ALLOCATION_RECORD.md)
(`BANPU-WP3 ALLOCATED`), which itself derives from the
[BANPU-WP3 Planning Freeze Record](BANPU_WP3_PLANNING_FREEZE_RECORD.md)
(`BANPU-WP3 PLANNING COMPLETE, CONFIRMED, AND FROZEN`), which in turn derives
from the BANPU-WP3 Planning Confirmation
(`PLANNING CONFIRMED WITH MINOR OBSERVATIONS`, transcribed in Planning Freeze
Record §3) and from the Architecture Owner ratification of 2026-08-10 that
closed gate S2.

Authority for **this record** is limited to transcription: identity binding,
corpus-boundary confirmation, and creation of this artifact. It grants no
authority to implement, to authorize, to allocate, to amend any frozen or
allocated artifact, or to reach WP4 or any later package.

## 3. Authorized work package

`BANPU-WP3 — Quote identity and epoch protection`, exactly as defined by the
frozen planning corpus in §4. The transcribed act did not change, narrow, or
widen that definition, and neither does this record.

## 4. Authorized planning corpus

The authorized corpus is the exact 2-file candidate frozen and allocated,
unchanged since freeze, allocation, and authorization:

| # | Frozen artifact | Bytes | Physical lines | SHA-256 |
|---|---|---:|---:|---|
| 1 | `docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | 40,882 | 688 | `1F4E21FBC275FF5AA6CC061E2A7AD7972B41008926D8E8E4648C1C07A9C2F096` |
| 2 | `docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | 17,909 | 430 | `A6A4AB0AC4DE1E7B1813EEFFB01E2F48A662DA9B937F1BF1A45982B065294462` |

Aggregate corpus manifest identity, unchanged from Planning Freeze Record §4 and
Allocation Record §3.1:
`C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`.

Corpus cardinality: `2`. Neither file has been modified since freeze,
allocation, or authorization. Both files contain zero `CR` bytes, so their raw
and LF-normalized identities coincide and the identity is invariant under the
convention established by `BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md` §4
and §9.

## 5. Planning Freeze dependency

[BANPU-WP3 Planning Freeze Record](BANPU_WP3_PLANNING_FREEZE_RECORD.md) —
20,789 bytes, 390 physical lines, SHA-256
`85FBDF9DB5B8EAC71A9DA7C82445E5A465E61548FD235A93D1E2A96E22924D90`.
Disposition: `BANPU-WP3 PLANNING COMPLETE, CONFIRMED, AND FROZEN`.

The freeze bound the corpus at the aggregate identity in §4 and recorded
implementation authority as `NONE`. It is unchanged since the freeze act and is
not amended by this record.

## 6. Allocation dependency

[BANPU-WP3 Allocation Record](BANPU_WP3_ALLOCATION_RECORD.md) — 15,730 bytes,
287 physical lines, SHA-256
`05F248B5B5965314AA1DF060155FE5B40BA87C13DA054DF19D13F7917152E2CB`.
Disposition: `BANPU-WP3 ALLOCATED`.

The allocation bound the same aggregate identity, recorded implementation
authority created as `NONE` and Work Package Plan authorized as `NO`, and named
BANPU-WP3 Implementation Authorization as the next constitutional act. The
transcribed act acted on that allocation; it did not re-perform or amend it, and
neither does this record.

## 7. Authorized implementation scope

The transcribed act authorized implementation for `BANPU-WP3 — Quote identity
and epoch protection`, exactly and only as the frozen corpus defines it, and
explicitly authorized implementation of all four sub-packages subject to that
corpus:

| Sub-package | Name | Depends on | Additional entry gate |
|---|---|---|---|
| BANPU-WP3.1 | Provider evidence extraction — first provider adapter | WP1 | — |
| BANPU-WP3.2 | Conversion quote binding, epoch, and quarantine contract | WP3.1 | Gate S8 |
| BANPU-WP3.3 | Cache namespacing and fail-closed fetch integration | WP3.2 | — |
| BANPU-WP3.4 | Call-path propagation and regression evidence | WP3.3 | — |

Implementation must remain within:

- the authorized production file surface (§8.1);
- the authorized test surface (§8.2);
- the frozen acceptance criteria (§9.1);
- the frozen architectural decisions (§9.2); and
- the frozen dependency model (§9.3).

## 8. Authorized file surface

Reproduced from the frozen Work Package Decomposition and Roadmap §2, §4.1,
§4.2, §4.3, and §4.4. The union of all sub-package file lists may not exceed
this surface.

### 8.1 Authorized production surface

- `backend/services/market_data/yahoo_chart.py` — WP3.1
- One new module under `backend/services/market_data/` — WP3.2, subject to the
  rule 7 confirmation required by gate S8 (§10)
- `backend/services/data_fetcher.py` — WP3.3
- The narrow holdings and price call site in `backend/main.py`, if required to
  pass the binding — WP3.4

### 8.2 Authorized test surface

- `backend/tests/test_yahoo_chart_provider.py` — WP3.1
- One new focused test module for the WP3.2 contract
- One new focused quote-epoch isolation test module — WP3.3
- `backend/tests/test_fetch_history.py` — WP3.4
- Focused regression test modules for unaffected quote and history consumers —
  WP3.4

### 8.3 Explicitly not to change

- Transaction or portfolio database schema, and the `MarketDataCache` schema
- `backend/services/portfolio_rebuilder.py`
- `backend/services/ledger_validator.py`
- `backend/services/portfolio_transactions.py`
- `backend/services/portfolio_snapshots.py`,
  `backend/services/idea_review.py`, and
  `backend/services/analytics/factor_engine.py` — price consumers deliberately
  left unmodified; their protection is delivered by refusal at the fetch layer
- `backend/services/market_data/base.py`,
  `backend/services/market_data/provider.py`, and any provider adapter other
  than `yahoo_chart.py`
- Admin cache endpoints
- Frontend transaction authoring, and all frontend files
- All M46 files

## 9. Frozen decisions and boundaries binding implementation

### 9.1 Frozen acceptance criteria

Canonical criteria A1–A5 govern. Derived criteria A6–A14 are subordinate
verification aids and cannot override them.

| # | Criterion | Class |
|---|---|---|
| A1 | Cross-symbol or cross-epoch results never produce a usable quote | Canonical |
| A2 | First successor-epoch quote may return a null previous close but never a predecessor close | Canonical |
| A3 | Converted cache entries are asset- and epoch-bound | Canonical |
| A4 | Unconverted quote dictionaries and cache keys retain current behavior | Canonical |
| A5 | Quarantine blocks only the affected converted identity | Canonical |
| A6 | With zero conversion rows, quote and history behavior is provably indistinguishable from baseline | Derived |
| A7 | Every quarantine emits exactly one enumerated reason; no rejection is free-text only | Derived |
| A8 | A quarantined identity receives no stale-cache fallback through any cache read path | Derived |
| A9 | Reference prices rejected when absent, non-positive, non-finite, or not decimal-exact and evidence-bound, at the point of consumption, without amending the frozen WP1 parser | Derived |
| A10 | No caller can obtain a price for a converted identity without a valid binding served by a contract-qualifying provider; refusal is observable and structured; verified against PD-5 including the G4 transition test | Derived |
| A11 | Namespaced `cache_type` values deterministically derivable from the binding and enumerable, with no admin endpoint change | Derived |
| A12 | No migration, no `MarketDataCache` schema change, no public API contract change | Derived |
| A13 | Change surface confined to the authorized file lists; M46 unchanged; WP1 and WP2 frozen corpora unchanged | Derived |
| A14 | `graphify update .` runs and the change surface matches the declared boundary | Derived |

### 9.2 Frozen architectural decisions

| Item | Frozen disposition |
|---|---|
| PD-1 | **RATIFIED — NARROW.** The corrected close derivation applies only where required to prevent epoch mixing for a converted identity. Unconverted and unbound derivation is numerically unchanged, including in the sparse-bar case. Pre-change characterization evidence is required before the first production edit |
| PD-2 | **RATIFIED AS SPECIFIED.** Epoch classification uses exchange-local calendar dates derived from the provider-reported exchange timezone. UTC-date comparison is rejected. Boundary fixtures cover both edges of the exchange-local day for a UTC+7 market |
| PD-3 | **RESOLVED as to WP3 scope.** WP3 owns the quarantine predicate and reason contract (obligation B1) and leaves the frozen WP2 deferral guard test unmodified and green (obligation B3). The emitter-locus item is referred out of WP3 and is not a WP3 obligation, decision, or residual |
| PD-4 | **RATIFIED AS SPECIFIED.** The WP3 Provider Evidence Contract E1–E5 is binding. Non-satisfaction is a first-class quarantine condition. Qualification is affirmative; an adapter silent about its evidence does not qualify. The rule is stated over capability, not identity |
| PD-5 | **RATIFIED.** Guard-set invariant G1–G4 is binding: canonical ledger evidence is the sole authority for membership; no unbounded memoization and a declared finite testable staleness bound; undetermined membership is refused and never resolves to "not converted"; acceptance requires the in-process transition test. The satisfying mechanism remains an implementation decision |
| R7 | **PATH B — FORMAL WAIVER**, scoped exactly to "No BANPU-WP3 obligation is inherited." It defines, reinterprets, weakens, and resolves nothing; it binds BANPU-WP3 only; WP4–WP8 inherit the residuals unchanged |
| Option C | Hybrid guard set adopted **unconditionally**. Explicit binding is the only route to a converted-identity price; unbound requests for a converted identity are refused |
| Provider neutrality | The verification predicate operates on a provider-neutral evidence structure and contains no provider-specific import. WP3 implements the first qualifying adapter, not a provider-coupled design |
| Backward compatibility | `get_quote()` and `fetch_price_info()` response shapes preserved; unconverted `cache_type` strings unchanged; no public API contract change; no migration |

### 9.3 Frozen dependency model

```text
BANPU-WP1 [FROZEN] → BANPU-WP2 [FROZEN, EPIC CLOSED] →
BANPU-WP3: WP3.1 → WP3.2 → WP3.3 → WP3.4 → BANPU-WP4
```

Sub-packages execute strictly serially. A sub-package does not begin until its
predecessor is independently reviewed and accepted (gate S4).

### 9.4 Carried-forward residuals

Unchanged and unresolved by the transcribed act and by this record: R6 (the
roadmap's naming of `backend/tests/test_fetch_history.py` as regression
evidence, recorded for separately approved documentation correction); the R7
formal waiver and the seven undefined WP2 residuals it declines to inherit; and
WP1's `backend/models/database.py` identity residual together with the WP2 Step
8 gate language. The emitter-locus item referred out by PD-3 is not a WP3
residual and creates no WP3 obligation.

## 10. Gate state

| # | Gate | State at authorization |
|---|---|---|
| S1 | WP2 accepted before WP3 begins | Satisfied |
| S2 | PD-1, PD-2, PD-4, PD-5 ratified and R7 closed — all five — before Planning Confirmation | Satisfied — Architecture Owner ratification of 2026-08-10; the §6.6 register is closed on all five items and no planning decision is open |
| S3 | Planning Confirmation precedes Planning Freeze; Planning Freeze precedes Allocation; the Work Package Plan is drafted only after Allocation | Satisfied as to sequencing (§16) |
| S4 | Sub-packages implemented serially, each independently reviewed and accepted before its successor begins | Pending — implementation-time |
| S5 | Baseline behavioral evidence captured before the first production edit; unrecoverable afterwards | Pending — implementation-time, and one-way |
| S6 | WP3 closes through review, corrections, confirmation, implementation freeze, epic closeout, Decision Log synchronization | Pending |
| S7 | WP4 does not begin until WP3 is confirmed and frozen; approved but unfrozen does not satisfy the gate | Pending |
| S8 | Rule 7 reviewer confirmation obtained for the WP3.2 module before WP3.2 begins | **Open** |

**Gate S8 remains open.** It is an implementation-entry gate scoped to the
single new WP3.2 production module in `backend/services/market_data/` and to
nothing else. The transcribed act did not satisfy it, and this record does not
satisfy it. WP3.2 may not begin until a reviewer confirms the module's strict
necessity under roadmap §1 rule 7. Observation O-1 of the Planning Confirmation
is preserved exactly: S8 was never a gate S2 item and is not a planning defect,
finding, open decision, or residual.

## 11. Explicit implementation boundaries

Implementation must **not**:

- modify BANPU-WP1;
- modify BANPU-WP2;
- modify M46;
- expand scope; or
- reinterpret planning.

Equally binding, from the frozen corpus: no schema change; no migration; no
public API contract change; no admin endpoint change; no general
corporate-action framework; no conversion logic placed in market-data policy
abstractions; no amendment of the canonical design, roadmap, or implementation
sequence; no resolution of any carried-forward residual or of the emitter-locus
item referred out by PD-3; and no release, deployment, or production data
mutation.

Gate S5 is one-way: baseline behavioral evidence lost after the first production
edit is unrecoverable.

## 12. Authorization verification transcribed

The eleven verifications required of, and completed by, the transcribed act.
These are reproduced as performed; this record does not re-perform them.

| # | Verification | Result |
|---|---|---|
| 1 | Planning was confirmed | `SATISFIED` |
| 2 | Planning was frozen | `SATISFIED` |
| 3 | Allocation was completed | `SATISFIED` |
| 4 | Allocated planning corpus identity matches the authorization target | `SATISFIED` |
| 5 | No planning amendment occurred after Allocation | `SATISFIED` |
| 6 | Authorization scope exactly equals the allocated planning scope | `SATISFIED` |
| 7 | All Architecture Owner decisions remain unchanged | `SATISFIED` |
| 8 | Gate S2 remains satisfied | `SATISFIED` |
| 9 | Gate S8 remains an implementation-entry gate for WP3.2 only | `SATISFIED` |
| 10 | No implementation authority already exists | `SATISFIED` |
| 11 | No conflicting constitutional authority exists | `SATISFIED` |

## 13. Successor authority

The transcribed act created exactly the following, and nothing beyond it:

- **Work Package Plan preparation is now authorized.**
- **Production implementation is now authorized.**
- **Implementation confirmation has NOT occurred.**
- **Implementation freeze has NOT occurred.**

## 14. Excluded authority

Neither the transcribed act nor this record creates:

- `NO` BANPU-WP4 or later-package authority;
- `NO` release, deployment, or production data mutation authority;
- `NO` authority over M46, which remains constitutionally independent and
  suspended;
- `NO` authority to reopen, amend, or reinterpret frozen BANPU-WP1, frozen
  BANPU-WP2, or the frozen BANPU-WP3 planning corpus;
- `NO` authority to amend the Planning Freeze Record or the Allocation Record;
- `NO` authority to satisfy gate S8;
- `NO` authority to resolve, weaken, or close any carried-forward residual, or
  the emitter-locus item referred out by PD-3;
- `NO` authority to perform implementation confirmation, implementation freeze,
  epic closeout, or Decision Log synchronization; and
- `NO` authority to skip, waive, or shortcut any gate in §10.

## 15. Authorization disposition

**BANPU-WP3 implementation is `AUTHORIZED`** at planning corpus identity
`C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`, scoped
exactly as set out in §7 through §11.

Work Package Plan preparation is authorized. Production implementation is
authorized. Implementation confirmation has not occurred. Implementation freeze
has not occurred. BANPU-WP1, BANPU-WP2, and the frozen BANPU-WP3 planning corpus
remain unmodified. WP4 and later packages remain unauthorized. M46 remains
constitutionally independent and suspended.

## 16. Sequencing note

Recorded because a subsequent independent review raised, and a Constitutional
Interpretation Authority resolved, a question about the placement of this act.
This section records that determination; it does not make one.

Gate S3 states that "the Work Package Plan is drafted only after Allocation."
That is a precedence constraint fixing a lower bound, not a successor
designation and not a claim of adjacency. The determination was
**DETERMINATION C — no sequencing contradiction exists**: the lawful sequence is

```text
Allocation → Implementation Authorization → Work Package Plan
```

and it satisfies gate S3 in full. No frozen artifact required amendment, and no
clarification record was required. The frozen planning corpus remains valid,
unchanged, and bound at the identity in §4.

Gate-state columns in the frozen artifacts are as-of-freeze snapshots, not live
status fields. The frozen decomposition shows S3 as `Pending`; S3 is now
satisfied. That is a change in the world, not a falsification of frozen text.

## 17. Repository verification

Performed at record creation, limited to what is necessary to confirm this
transcription names the correct act and the correct corpus.

| Verification | Result |
|---|---|
| Planning corpus per-file identities unchanged | `SATISFIED` — both files recomputed and identical to §4 |
| Planning corpus aggregate identity unchanged | `SATISFIED` — recomputed `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A` |
| Corpus cardinality | `SATISFIED` — `2`, unchanged |
| Corpus files contain zero `CR` bytes | `SATISFIED` — raw and LF-normalized identities coincide |
| `BANPU_WP3_PLANNING_FREEZE_RECORD.md` unchanged | `SATISFIED` — 20,789 bytes, 390 lines, SHA-256 matches §5 |
| `BANPU_WP3_ALLOCATION_RECORD.md` unchanged | `SATISFIED` — 15,730 bytes, 287 lines, SHA-256 matches §6 |
| Frozen WP1 corpus content unchanged | `SATISFIED AS TO CONTENT` — all 12 files clean against `HEAD`; each matches its recorded identity in the representation in which that identity was recorded. See the identity-representation observation below |
| Frozen WP2 implementation corpus unchanged | `SATISFIED` — 6-file LF aggregate recomputed from disk as `6E50F5B5E2AAA008EA1C3DA25D1FC34C41F9CBAE81A293A463FB3F6BF5DA4159` |
| Frozen WP2 planning corpus unchanged | `SATISFIED` — 3-file LF aggregate recomputed from disk as `91F9295BBF71BC9FA50D8246893DA693189C8855D4B6F0E146822E36F76DFB5E` |
| No production file changed | `SATISFIED` — no production, schema, migration, or M46 file appears in `git status --porcelain` |
| No test file changed | `SATISFIED` |
| No frozen artifact modified | `SATISFIED` |
| No Work Package Plan created | `SATISFIED` — this act creates no such artifact |
| `git diff --check` | `PASS` — exit 0 under intent-to-add |
| `git diff --cached --check` | `PASS` — exit 0 |
| Graph synchronization | Not applicable — documentation-only addition; no code changed, so `graphify update .` is not required by this act |
| No commit created | `SATISFIED` — this act stages no commit |

**Identity-representation observation, recorded and not resolved.** Verification
at record creation established that the WP1 frozen corpus is unchanged in
content, but that its recorded 12-file aggregate
`DF0AF823EFEACA38171F4DACAC0B19975BAE07EE1BA09A040B549B06ACD443E1` is
**representation-mixed**: ten of the twelve recorded per-file identities are
LF-normalized values, while `backend/services/transaction_canonicalizer.py`
(31,416 bytes) and `backend/tests/test_transaction_canonicalizer.py`
(25,881 bytes) are recorded at their raw CRLF working-tree identities and match
only in that representation. The recorded aggregate is therefore not
reproducible from repository files under the single LF convention made binding
by `BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md` §4 and §9, which corrected
three files and did not reach these two.

This is a **pre-existing identity-convention condition, not content drift**, and
it is adjacent in kind to the WP1 `backend/models/database.py` identity residual
already carried forward by the frozen WP3 corpus §12. It is recorded here
because it was observed here. It is **not** resolved, reinterpreted, or closed
by this record; it creates no BANPU-WP3 obligation; it does not affect the
BANPU-WP3 planning corpus identity in §4, which is convention-invariant because
both corpus files contain zero `CR` bytes; and it is not an implementation
blocker. Any disposition belongs to the authority that governs the WP1 freeze
identity, not to this act.

## 18. Exact next constitutional act

The exact next constitutional act is **BANPU-WP3 Work Package Plan**.

This record performs no part of that act, creates no Work Package Plan, performs
no implementation, performs no implementation review, performs no implementation
confirmation, and performs no implementation freeze.

**Final disposition: `BANPU-WP3 IMPLEMENTATION AUTHORIZATION RECORDED`.**
