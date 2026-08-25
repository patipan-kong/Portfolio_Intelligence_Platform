# BANPU-WP3 — Amended Implementation Authorization Record `BPA-1`

**Artifact class:** Additive constitutional implementation-authorization synchronization record
**Synchronization/authorization date:** 2026-08-11
**Amendment identifier:** `BPA-1`
**Issuing role:** BANPU-WP3 Implementation Authorization Authority
**Superseded authorization corpus identity:** `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
**Current frozen and allocated corpus identity:** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Disposition:** `BANPU-WP3 BPA-1 IMPLEMENTATION AUTHORIZATION SYNCHRONIZED TO AMENDED PLANNING CORPUS`
**Implementation authority created by this act:** `YES — bounded exactly to the BPA-1 accessor surface in §6`
**Work Package Plan amended or reapproved by this act:** `NO`

---

## 1. Constitutional authority and basis

Acting solely as the BANPU-WP3 Implementation Authorization Authority, this
act synchronizes BANPU-WP3 implementation authorization to the planning
corpus frozen by
[BANPU-WP3 Amended Planning Freeze Record](BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md)
(`BANPU-WP3 BPA-1 AMENDED PLANNING CORPUS FROZEN`) and allocated by
[BANPU-WP3 Amended Allocation Record](BANPU_WP3_AMENDED_ALLOCATION_RECORD.md)
(`BANPU-WP3 BPA-1 ALLOCATION SYNCHRONIZED TO AMENDED PLANNING CORPUS`), which
in turn derive from
[BANPU-WP3 Planning Amendment Confirmation](BANPU_WP3_PLANNING_AMENDMENT_CONFIRMATION.md)
(`BANPU-WP3 BPA-1 PLANNING AMENDMENT CONFIRMED`) and the concluded
Independent Bounded Planning Amendment Review
(`BANPU-WP3 BPA-1 INDEPENDENTLY APPROVED`).

Required lifecycle chain, independently verified as present, consistent, and
binding the same amended corpus:

| # | Predecessor act | Disposition | Binds corpus identity |
|---|---|---|---|
| 1 | Independent Bounded Planning Amendment Review | `BANPU-WP3 BPA-1 INDEPENDENTLY APPROVED` | `3A04B06A…D8F43D` (candidate) |
| 2 | Planning Amendment Confirmation | `BANPU-WP3 BPA-1 PLANNING AMENDMENT CONFIRMED` | `3A04B06A…D8F43D` |
| 3 | Amended Planning Freeze | `BANPU-WP3 BPA-1 AMENDED PLANNING CORPUS FROZEN` | `3A04B06A…D8F43D` |
| 4 | Amended Allocation | `BANPU-WP3 BPA-1 ALLOCATION SYNCHRONIZED TO AMENDED PLANNING CORPUS` | `3A04B06A…D8F43D` |
| 5 | **This act** — Implementation Authorization Synchronization | `BANPU-WP3 BPA-1 IMPLEMENTATION AUTHORIZATION SYNCHRONIZED TO AMENDED PLANNING CORPUS` | `3A04B06A…D8F43D` |

No predecessor act is absent, inconsistent, or bound to a different corpus.
The chain does not fail closed.

This authority is limited to identity binding, corpus-boundary verification,
the exact bounded authorization delta in §6, and creation of this record. It
grants no authority to amend or reapprove the Work Package Plan, perform the
focused C3 accessor-delta review, perform C4 review, or resume any
implementation, correction, production, or test activity beyond what §6
admits.

## 2. Verification of the current frozen and allocated corpus

Independently rehashed from working-tree bytes before this act:

| # | Frozen artifact | Bytes | SHA-256 |
|---|---|---:|---|
| 1 | `docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | 45,667 | `DF4630CFC00A32402B45489D1779F3BBAAD39A86630301256C541BC806481DD7` |
| 2 | `docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | 21,949 | `48BE744AD91367293FF790772A96FA49D60058CF0221080F538AE6FBEB3BAB01` |

Recomputed aggregate manifest identity, exact match:

```text
3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D
```

This is exactly the identity frozen by the Amended Planning Freeze Record and
bound by the Amended Allocation Record (§2 of that record). Both artifacts
contain zero `CR` bytes, so raw and LF-normalized identities coincide.

## 3. Why authorization synchronization is required

The historical
[BANPU-WP3 Implementation Authorization Record](BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
binds `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
throughout (header `Authorized planning corpus identity`, §4, §15, §17) — the
pre-amendment corpus, now superseded. Its §4 records the pre-amendment
per-file identities (`1F4E21FB…`, 40,882 bytes; `A6A4AB0A…`, 17,909 bytes),
which differ from the current amended per-file identities in §2 above. It
does not authorize implementation reliance on BPA-1 and is **not
reinterpreted by this act to do so automatically**. Because the planning
corpus identity changed at Amended Planning Freeze and the allocation was
separately synchronized, implementation authorization must be independently
re-performed against the new identity before the BPA-1 accessor may be
lawfully relied upon.

## 4. Relationship to the historical Implementation Authorization Record

[`BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
is **not modified, rewritten, or deleted** by this act. It remains historical
evidence that BANPU-WP3 implementation was authorized at the pre-amendment
corpus identity on 2026-08-10, with disposition
`BANPU-WP3 IMPLEMENTATION AUTHORIZED`, scoped to the four sub-packages
WP3.1–WP3.4 and the file surfaces in its §8. This record is additive and
supersedes it as the current implementation-authorization state; from this
act forward, the authorized corpus target is the identity in §2 above, and
authorization additionally includes the exact bounded delta in §6.

## 5. Preserved implementation authorization, unchanged by this act

Every element of the historical authorization is carried forward unchanged
**except** the bounded WP3.4 delta in §6:

- Authorized work package: `BANPU-WP3 — Quote identity and epoch protection`,
  unchanged in scope.
- Authorized sub-packages WP3.1–WP3.4 and their strict serial dependency
  model (historical §7, §9.3) — unchanged.
- Authorized production surface (historical §8.1) — unchanged, except the
  bounded addition in §6.
- Authorized test surface (historical §8.2) — unchanged.
- Explicitly-not-to-change list (historical §8.3) — unchanged.
- Frozen acceptance criteria A1–A5 (canonical) and A6–A14 (derived,
  historical §9.1) — unchanged, preserved verbatim.
- Frozen architectural decisions PD-1 through PD-5, R7 Path B waiver, Option
  C, provider neutrality, backward compatibility (historical §9.2) —
  unchanged, unreinterpreted.
- Gate state table (historical §10), including gate S8 `Open` and gates
  S4–S7 `Pending` — unchanged.
- Explicit implementation boundaries (historical §11) — unchanged.
- Carried-forward residuals R6, the R7 waiver and its seven undefined WP2
  residuals, the WP1 `database.py` identity residual, and the
  identity-representation observation (historical §9.4, §17) — unchanged,
  unresolved.
- Excluded authority (historical §14) — unchanged: no WP4+ authority, no
  release/deployment authority, no authority over M46, no authority to
  reopen frozen WP1/WP2, no authority to satisfy gate S8, no authority to
  perform implementation confirmation, implementation freeze, epic closeout,
  or Decision Log synchronization.

No other work-package authorization changes.

## 6. Exact bounded implementation-authorization delta

The synchronized authorization admits exactly one additional production
surface, matching BPA-1 exactly as frozen and allocated:

| Item | Value |
|---|---|
| File | `backend/services/data_fetcher.py` |
| Symbol | `resolve_successor_bindings(symbols)` |
| Sub-package | WP3.4 |
| Sole authorized consumer | The holdings-price call path in `backend/main.py` |
| Purpose | Read-only propagation of requested, non-ambiguous canonical `SuccessorQuoteBinding` values from the existing accepted WP3.3 guard projection to that sole WP3.4 call path |
| Class | Production, read-only |

Preserved exactly, as bounded by BPA-1, the Amended Planning Freeze Record,
and the Amended Allocation Record:

1. creates no persistent state;
2. performs no memoization and holds no cache;
3. changes no guard-membership semantics;
4. changes no quarantine policy and adds, removes, or reinterprets no
   quarantine reason;
5. changes no `fetch_price_info` or `fetch_history` semantics, signature
   contract, or return shape;
6. performs no provider lookup;
7. performs no registry lookup;
8. reads no environment value and no configuration value;
9. exposes no boundary evidence;
10. constructs no binding outside the accepted WP3.2 and WP3.3 machinery;
11. leaves ambiguous and unavailable projection states fail-closed;
12. authorizes no caller other than the single WP3.4 holdings-price call path
    in `backend/main.py`;
13. confers on WP3.4 no authority over any other
    `backend/services/data_fetcher.py` behavior.

No other implementation surface is added or widened. This authorization does
**not** itself accept, review, or independently ratify the existing accessor
implementation already present in the worktree — see §7 and §9.

## 7. Preserved checkpoint state

- **C1 accepted** — unchanged, unreopened.
- **C2 accepted** — unchanged, unreopened.
- **C3 accepted for the pre-accessor WP3.3 state only** — the accessor delta
  remains a separately reviewable focused C3 delta, **not yet independently
  accepted**.
- **C4 incomplete** — unchanged by this act; requires both focused C3 delta
  acceptance and Step 4.1 eleven-site evidence.

Authorization of the bounded implementation surface in §6 is **not**
independent acceptance of the implementation already present in the
worktree, and does not retrospectively declare the accessor C3-accepted.
Focused C3 accessor-delta review remains outstanding and is not performed,
begun, or implied by this act.

## 8. Effect on implementation

**Does this synchronization create implementation authority for the bounded
BPA-1 accessor surface?**
**YES** — but only within the exact amended and allocated BPA-1 surface
identified in §6: the single accessor `resolve_successor_bindings(symbols)`
in `backend/services/data_fetcher.py`, for the sole `backend/main.py`
holdings-price call path, subject to all thirteen preserved constraints.

**Does it independently accept the accessor implementation currently in the
worktree?**
**NO.** Acceptance requires the outstanding focused C3 delta review (§7).

**Does it allow focused C3 delta review immediately?**
**NO.** The Work Package Plan (§9 below) remains bound to the superseded
planning state and must first be amended and independently reapproved.

**Does it authorize arbitrary further WP3.4 implementation?**
**NO.** The only newly authorized production delta is the exact BPA-1
accessor and its sole authorized propagation relationship in §6. No other
file, symbol, caller, or behavior is authorized by this act.

## 9. Work Package Plan boundary

[`BANPU_WP3_WORK_PACKAGE_PLAN.md`](BANPU_WP3_WORK_PACKAGE_PLAN.md) and
[`BANPU_WP3_WORK_PACKAGE_PLAN_APPROVAL.md`](BANPU_WP3_WORK_PACKAGE_PLAN_APPROVAL.md)
were prepared and approved against the pre-amendment corpus identity
`C7B6CEEF…0670638A`. They remain historical, currently-superseded operational
governance for any purpose touched by BPA-1, and **must be amended and
independently reapproved** before the focused C3 delta review or C4
continuation may proceed. Neither file is modified, amended, or reapproved by
this act. This act does not treat the prior Work Package Plan approval as
approval of the BPA-1 operational sequence, and creates no authority to begin
or resume any Work Package Plan step under color of this record.

## 10. Post-write corpus verification

After creating this record, both frozen planning artifacts and the aggregate
manifest were independently rehashed:

| Check | Result |
|---|---|
| `BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` — 45,667 bytes, `DF4630CF…81DD7` | `EXACT` |
| `BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` — 21,949 bytes, `48BE744A…3BAB01` | `EXACT` |
| Recomputed aggregate manifest identity | `EXACT` — `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D` |
| `BANPU_WP3_BOUNDED_PLANNING_AMENDMENT_RECORD.md` unmodified | `SATISFIED` |
| `BANPU_WP3_PLANNING_AMENDMENT_CONFIRMATION.md` unmodified | `SATISFIED` |
| `BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md` unmodified | `SATISFIED` |
| `BANPU_WP3_AMENDED_ALLOCATION_RECORD.md` unmodified | `SATISFIED` |
| Historical `BANPU_WP3_ALLOCATION_RECORD.md` unmodified | `SATISFIED` |
| Historical `BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md` unmodified | `SATISFIED` — still binds superseded identity, as expected |
| `BANPU_WP3_WORK_PACKAGE_PLAN.md` unmodified | `SATISFIED` |
| `BANPU_WP3_WORK_PACKAGE_PLAN_APPROVAL.md` unmodified | `SATISFIED` |
| All production files unmodified by this act | `SATISFIED` — no production file appears in the diff introduced by this act |
| All test files unmodified by this act | `SATISFIED` — no test file appears in the diff introduced by this act |

## 11. Repository hygiene

| Check | Result |
|---|---|
| `git diff --check` | `PASS` — exit 0 (only pre-existing benign LF→CRLF conversion warnings) |
| `git diff --cached --check` | `PASS` — exit 0 |
| Path created by this act | Exactly one: `docs/implementation/BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md` |
| Pre-existing staging state | Unaltered by this act |

**Pre-existing dirty state, disclosed and not caused by this act.**
`backend/main.py`, `backend/services/data_fetcher.py`,
`backend/services/market_data/yahoo_chart.py`,
`backend/tests/test_fetch_history.py`,
`backend/tests/test_yahoo_chart_provider.py`, the staged BANPU-WP3 governance
artifacts, and the untracked WP3 accessor/test files and prior BPA-1
governance records all predate this act and are unmodified by it.

## 12. Excluded effects

This record does **not**:

- authorize, allocate, or begin implementation of any kind beyond the exact
  bounded surface in §6;
- amend or reapprove the Work Package Plan or its approval record;
- perform the focused C3 accessor-delta review or accept the accessor
  implementation;
- complete or re-review C4;
- reopen C1, C2, or accepted pre-accessor C3 (WP3.3) semantics;
- modify the frozen planning artifacts, the Bounded Planning Amendment
  Record, the Planning Amendment Confirmation, the Amended Planning Freeze
  Record, the Amended Allocation Record, the historical Allocation Record,
  the historical Implementation Authorization Record, the Work Package Plan,
  or its approval record;
- modify any production or test file;
- commit, push, deploy, or release.

## 13. Final disposition

**BANPU-WP3 BPA-1 IMPLEMENTATION AUTHORIZATION SYNCHRONIZED TO AMENDED
PLANNING CORPUS** at corpus identity
`3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`.

Implementation authority is created, bounded exactly to the accessor surface
in §6. The existing accessor implementation is not independently accepted.
The Work Package Plan remains unamended and unreapproved. Focused C3
accessor-delta review remains outstanding. C4 remains incomplete.

## 14. Exact next act

**BANPU-WP3 Work Package Plan Amendment and Reapproval.**

This record performs no part of that act.
