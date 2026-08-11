# BANPU-WP3 — Amended Allocation Record `BPA-1`

**Artifact class:** Additive constitutional allocation synchronization record
**Synchronization date:** 2026-08-11
**Amendment identifier:** `BPA-1`
**Issuing role:** BANPU-WP3 Allocation Authority
**Superseded allocation corpus identity:** `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
**Current frozen amended corpus identity:** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Disposition:** `BANPU-WP3 BPA-1 ALLOCATION SYNCHRONIZED TO AMENDED PLANNING CORPUS`
**Implementation authority created by this act:** `NONE`
**Implementation Authorization synchronized by this act:** `NO`

---

## 1. Constitutional authority and basis

Acting solely as the BANPU-WP3 Allocation Authority, this act synchronizes
BANPU-WP3 allocation to the planning corpus frozen by
[BANPU-WP3 Amended Planning Freeze Record](BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md)
(`BANPU-WP3 BPA-1 AMENDED PLANNING CORPUS FROZEN`), which in turn derives from
[BANPU-WP3 Planning Amendment Confirmation](BANPU_WP3_PLANNING_AMENDMENT_CONFIRMATION.md)
(`BANPU-WP3 BPA-1 PLANNING AMENDMENT CONFIRMED`).

This authority is limited to identity binding, corpus-boundary verification,
and creation of this record. It grants no authority to authorize
implementation, synchronize Implementation Authorization, amend or reapprove
the Work Package Plan, or perform the focused C3 delta review.

## 2. Verification of the current frozen corpus

Independently rehashed from working-tree bytes before this act:

| # | Frozen artifact | Bytes | SHA-256 |
|---|---|---:|---|
| 1 | `docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | 45,667 | `DF4630CFC00A32402B45489D1779F3BBAAD39A86630301256C541BC806481DD7` |
| 2 | `docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | 21,949 | `48BE744AD91367293FF790772A96FA49D60058CF0221080F538AE6FBEB3BAB01` |

Recomputed aggregate manifest identity, exact match:

```text
3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D
```

This is exactly the identity bound by the Amended Planning Freeze Record and
the Planning Amendment Confirmation.

## 3. Why synchronization is required

The existing [BANPU-WP3 Allocation Record](BANPU_WP3_ALLOCATION_RECORD.md)
binds `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
throughout (header, §3.1, §5 V3, §9) — the pre-amendment corpus, now
superseded. It does not allocate against the current frozen BPA-1 corpus and
is not reinterpreted by this act to do so automatically. Because the planning
corpus identity changed at Amended Planning Freeze, allocation must be
independently re-performed against the new identity before any successor
Implementation Authorization synchronization may rely on BPA-1.

## 4. Relationship to the historical Allocation Record

[`BANPU_WP3_ALLOCATION_RECORD.md`](BANPU_WP3_ALLOCATION_RECORD.md) is **not
modified, rewritten, or deleted** by this act. It remains historical evidence
that BANPU-WP3 planning ownership was allocated at the pre-amendment corpus
identity on 2026-08-10, with disposition `BANPU-WP3 ALLOCATED`. This record is
additive and supersedes it as the current allocation state; from this act
forward, the allocation target is the identity in §2 above, not the identity
the historical record binds.

## 5. Preserved allocation, unchanged by this act

Every element of the historical allocation is carried forward unchanged
**except** the bounded WP3.4 delta in §6:

- Allocated work package: `BANPU-WP3 — Quote identity and epoch protection`,
  unchanged in scope.
- Boundaries against WP1, WP2, and WP4–WP8 (historical §4) — unchanged.
- Architectural positions, unconditional Option C, provider neutrality, the
  four-layer decomposition, backward compatibility (historical §3.2) —
  unchanged.
- Canonical acceptance criteria A1–A5 and derived criteria A6–A14 (historical
  §3.2) — unchanged, preserved verbatim.
- Planning gates S1–S7 (Plan) and S1–S8 (Decomposition) — unchanged.
- Sub-package decomposition WP3.1 through WP3.4, strict serial order —
  unchanged, except for the single bounded surface-allocation correction in
  §6.
- Frozen decisions PD-1, PD-2, PD-4, PD-5, and the R7 Path B waiver
  (historical §3.3) — unchanged, unreinterpreted.
- Observation O-1 and gate S8's `Open` state (historical §3.4) — unchanged.
- All carried-forward residuals R6, the R7 waiver, and the WP1
  `database.py` identity residual (historical §3.5) — unchanged, unresolved.

No other work-package allocation changes.

## 6. Exact bounded WP3.4 allocation delta

The synchronized allocation admits exactly one additional surface, matching
BPA-1 exactly as frozen:

| Item | Value |
|---|---|
| File | `backend/services/data_fetcher.py` |
| Accessor | `resolve_successor_bindings(symbols)` |
| Sub-package | WP3.4 |
| Sole authorized caller | The authorized holdings-price call path in `backend/main.py` |
| Class | Production, read-only |

Preserved exactly, as bounded by BPA-1 and the Amended Planning Freeze Record:

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

This allocation admits the surface. It does **not** itself accept, review, or
authorize reliance on the existing accessor implementation — see §8.

## 7. Preserved checkpoint state

- **C1 accepted** — unchanged, unreopened.
- **C2 accepted** — unchanged, unreopened.
- **C3 accepted for the pre-accessor WP3.3 state only** — the accessor delta
  remains a separately reviewable focused C3 delta, **not yet independently
  accepted**.
- **C4 incomplete** — unchanged by this act; requires both focused C3 delta
  acceptance and Step 4.1 eleven-site evidence.

This allocation synchronization does **not** imply that the existing accessor
implementation in `backend/services/data_fetcher.py` is accepted, does not
authorize it by virtue of this act alone, and does not retrospectively accept
it. Acceptance requires the outstanding focused C3 delta review.

## 8. Authority boundary

**Does allocation synchronization itself permit implementation to resume?
NO.**

Allocation and implementation authorization are separate constitutional acts.
This record creates allocation authority only — the recorded synchronization
of the frozen BPA-1 corpus as the fixed target for a future, separately
governed Implementation Authorization synchronization act. It does **not**:

- synchronize or create Implementation Authorization — the existing
  [Implementation Authorization Record](BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
  remains bound to the superseded identity `C7B6CEEF…0670638A` until
  separately synchronized;
- amend or reapprove the Work Package Plan;
- perform the focused C3 accessor-delta review;
- authorize resumption of WP3.4 or any production or test change under color
  of this record.

No implementation code was modified, relied upon, or newly authorized during
this act.

## 9. Post-write corpus verification

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
| Historical `BANPU_WP3_ALLOCATION_RECORD.md` unmodified | `SATISFIED` |
| `BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md` unmodified | `SATISFIED` — still binds superseded identity, as expected |
| `BANPU_WP3_WORK_PACKAGE_PLAN.md` unmodified | `SATISFIED` |
| `BANPU_WP3_WORK_PACKAGE_PLAN_APPROVAL.md` unmodified | `SATISFIED` |

## 10. Repository hygiene

| Check | Result |
|---|---|
| `git diff --check` | `PASS` — exit 0 |
| `git diff --cached --check` | `PASS` — exit 0 |
| Path created by this act | Exactly one: `docs/implementation/BANPU_WP3_AMENDED_ALLOCATION_RECORD.md` |
| Pre-existing staging state | Unaltered by this act |

**Pre-existing dirty state, disclosed and not caused by this act.**
`backend/main.py`, `backend/services/data_fetcher.py`,
`backend/services/market_data/yahoo_chart.py`,
`backend/tests/test_fetch_history.py`,
`backend/tests/test_yahoo_chart_provider.py`, the staged BANPU-WP3 governance
artifacts, and the untracked WP3 accessor/test files and prior BPA-1
governance records all predate this act and are unmodified by it. The
recursive `Permission denied` warnings `git status` emits for
`backend/.pytest-m32-3e3r2*` directories are pre-existing environmental noise
and affect no verification above.

## 11. Excluded effects

This record does **not**:

- authorize, allocate, or begin implementation of any kind beyond the
  surface-allocation delta in §6;
- synchronize or create Implementation Authorization;
- amend or reapprove the Work Package Plan;
- perform the focused C3 accessor-delta review or accept the accessor
  implementation;
- complete or re-review C4;
- reopen C1, C2, or accepted pre-accessor C3 (WP3.3) semantics;
- modify the frozen planning artifacts, the Bounded Planning Amendment
  Record, the Planning Amendment Confirmation, the Amended Planning Freeze
  Record, the historical Allocation Record, the Implementation Authorization
  Record, the Work Package Plan, or its approval record;
- modify any production or test file;
- commit, push, deploy, or release.

## 12. Final disposition

**BANPU-WP3 BPA-1 ALLOCATION SYNCHRONIZED TO AMENDED PLANNING CORPUS** at
corpus identity `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`.

Implementation authority remains `NONE`. Implementation Authorization remains
unsynchronized, still bound to the superseded identity. The Work Package Plan
remains unamended. Focused C3 accessor-delta review remains outstanding. C4
remains incomplete.

## 13. Exact next act

**BANPU-WP3 Implementation Authorization Synchronization to Amended Planning
Corpus.**

This record performs no part of that act.
