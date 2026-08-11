# BANPU-WP3 — Work Package Plan Amended Approval `BPA-1`

**Artifact class:** Additive constitutional reapproval record
**Reapproval date:** 2026-08-11
**Amendment identifier:** `BPA-1`
**Issuing role:** BANPU-WP3 Work Package Planning and Approval Authority
**Approved amended artifact:** [`docs/implementation/BANPU_WP3_WORK_PACKAGE_PLAN.md`](BANPU_WP3_WORK_PACKAGE_PLAN.md)
**Approved amended artifact identity:** SHA-256 `84E1EC24ACF436AFCC26BFABB4E982692BDB80AAF24B02828356D0F69B23045D`, 49,541 bytes
**Superseded historical plan identity:** SHA-256 `02F805452B0686DCBF7C74AD2711B6104368331F1F6F6DF51BB7C14345FD8033`, 42,342 bytes
**Superseded historical approval identity:** SHA-256 `B4D287AD9AFE971B99C130C35F17029E8C25038DE82F36E9A17BF5F65F446ED3`, 7,441 bytes
**Governing planning corpus identity:** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Disposition:** `BANPU-WP3 BPA-1 WORK PACKAGE PLAN AMENDED AND REAPPROVED`
**New implementation authority created by this record:** `NONE`

---

## 1. Constitutional authority and basis

Acting solely as the BANPU-WP3 Work Package Planning and Approval Authority,
this record independently reapproves the Work Package Plan as amended for
`BPA-1`. Authority derives from the fully synchronized BPA-1 lifecycle:

| # | Predecessor act | Disposition | Binds corpus identity |
|---|---|---|---|
| 1 | Independent Bounded Planning Amendment Review | `BANPU-WP3 BPA-1 INDEPENDENTLY APPROVED` | `3A04B06A…D8F43D` |
| 2 | Planning Amendment Confirmation | `BANPU-WP3 BPA-1 PLANNING AMENDMENT CONFIRMED` | `3A04B06A…D8F43D` |
| 3 | Amended Planning Freeze | `BANPU-WP3 BPA-1 AMENDED PLANNING CORPUS FROZEN` | `3A04B06A…D8F43D` |
| 4 | Amended Allocation | `BANPU-WP3 BPA-1 ALLOCATION SYNCHRONIZED TO AMENDED PLANNING CORPUS` | `3A04B06A…D8F43D` |
| 5 | Amended Implementation Authorization | `BANPU-WP3 BPA-1 IMPLEMENTATION AUTHORIZATION SYNCHRONIZED TO AMENDED PLANNING CORPUS` | `3A04B06A…D8F43D` |
| 6 | **This act** — Work Package Plan Amendment and Reapproval | `BANPU-WP3 BPA-1 WORK PACKAGE PLAN AMENDED AND REAPPROVED` | `3A04B06A…D8F43D` |

No predecessor act is absent, inconsistent, or bound to a different corpus.
This authority is limited to plan-amendment review, identity binding, and
creation of this record. It grants no authority to perform the focused C3
accessor-delta review, perform C4 review, or resume WP3.4 implementation.

## 2. Verification of the governing frozen and allocated corpus

Independently rehashed from working-tree bytes:

| # | Frozen artifact | Bytes | SHA-256 |
|---|---|---:|---|
| 1 | `docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | 45,667 | `DF4630CFC00A32402B45489D1779F3BBAAD39A86630301256C541BC806481DD7` |
| 2 | `docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | 21,949 | `48BE744AD91367293FF790772A96FA49D60058CF0221080F538AE6FBEB3BAB01` |

Recomputed aggregate manifest identity, exact match:

```text
3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D
```

## 3. Independent review of the amended plan

The amended [`BANPU_WP3_WORK_PACKAGE_PLAN.md`](BANPU_WP3_WORK_PACKAGE_PLAN.md)
was independently reviewed against the frozen BPA-1 planning corpus (§2), the
[Amended Allocation Record](BANPU_WP3_AMENDED_ALLOCATION_RECORD.md), the
[Amended Implementation Authorization Record](BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md),
all thirteen BPA-1 accessor constraints, and the preserved checkpoint state.

| # | Condition | Result |
|---|---|---|
| 1 | Amended plan's §0 governing corpus identity matches §2 above | `SATISFIED` |
| 2 | Amended plan admits exactly the BPA-1 accessor and no wider surface (§0.2, §2 table, Step 4.2) | `SATISFIED` — file/symbol/caller match the Amended Allocation Record §6 and Amended Implementation Authorization Record §6 exactly |
| 3 | All thirteen BPA-1 constraints reproduced verbatim (§0.2) | `SATISFIED` |
| 4 | Sole authorized consumer preserved as the `backend/main.py` holdings-price call path (§0.2, Step 4.2) | `SATISFIED` |
| 5 | Step 4.2 and Checkpoint C4 updated consistently with §0.2–§0.3, with no other step, checkpoint, criterion, decision, or risk altered | `SATISFIED` — diff confined to §0 (new), §2 (one row), Step 4.2, and Checkpoint C4 |
| 6 | Focused C3 Accessor-Delta Review gate inserted before WP3.4/Step 4.2 resumption, and does not reopen accepted pre-accessor C3 (§0.4) | `SATISFIED` |
| 7 | C1/C2 accepted, C3 accepted only for pre-accessor WP3.3 state, C4 incomplete, all stated explicitly (§0.5) | `SATISFIED` |
| 8 | Step 4.1 eleven-site register requirement preserved and unweakened (§0.5, original §3.4 Step 4.1 unmodified) | `SATISFIED` |
| 9 | PD-1 through PD-5, A1–A14, quarantine taxonomy, provider-evidence semantics, cache-key semantics, WP1/WP2 boundaries, WP5 ownership unchanged | `SATISFIED` — no edit touches §1, §3.0–§3.3, §4, §6, or §7 |
| 10 | No new implementation authority created beyond the already-synchronized bounded accessor surface | `SATISFIED` — §0 explicitly disclaims it |
| 11 | No unsupported planning or implementation rule appears | `SATISFIED` — no finding requiring `CHANGES REQUIRED` |

No `BLOCKING`, `MAJOR`, or unresolved `MINOR` finding exists. The amendment is
fully supported by the frozen BPA-1 corpus and the synchronized allocation and
authorization.

## 4. Relationship to the historical plan and approval

Neither
[`BANPU_WP3_WORK_PACKAGE_PLAN_APPROVAL.md`](BANPU_WP3_WORK_PACKAGE_PLAN_APPROVAL.md)
(historical approval, `B4D287AD…F446ED3`, 7,441 bytes, disposition
`BANPU-WP3 WORK PACKAGE PLAN APPROVED`, approved 2026-08-10 against the
pre-amendment plan text `02F805452B…FD8033`, 42,342 bytes) nor its approved
plan text at that identity is modified, rewritten, or deleted by this act.
Both remain historical evidence of the pre-amendment approval. This record is
additive and supersedes them as the current plan-approval state; from this
act forward, the approved plan is the amended text at `84E1EC24…23045D`,
49,541 bytes, governed by the corpus identity in §2.

## 5. Effect

- The amended [`BANPU_WP3_WORK_PACKAGE_PLAN.md`](BANPU_WP3_WORK_PACKAGE_PLAN.md)
  is `BANPU-WP3 BPA-1 WORK PACKAGE PLAN AMENDED AND REAPPROVED`.
- This creates no new implementation authority beyond the bounded accessor
  surface already synchronized by the Amended Implementation Authorization
  Record.
- It does **not** perform the Focused C3 Accessor-Delta Review required by
  plan §0.4 before WP3.4 (Step 4.2) may resume.
- It does **not** perform Step 4.1 eleven-site evidence work.
- It does **not** perform C4 review, WP3 confirmation, or WP3 freeze.
- It authorizes no commit, push, deployment, or release.

## 6. Preserved checkpoint state

- **C1 accepted** — unchanged, unreopened.
- **C2 accepted** — unchanged, unreopened.
- **C3 accepted for the pre-accessor WP3.3 state only** — the accessor delta
  remains a separately reviewable focused C3 delta, not yet independently
  accepted.
- **C4 incomplete** — requires both focused C3 delta acceptance (plan §0.4)
  and Step 4.1 eleven-site evidence (plan §3.4 Step 4.1, unmodified).

This reapproval performs no independent implementation acceptance of any
kind. The accessor implementation already present in the worktree is not
accepted, ratified, or relied upon by this record.

## 7. Post-write verification

After creating this record, the frozen planning corpus, the amended plan, and
all BPA-1 lifecycle governance records were independently rehashed:

| Check | Result |
|---|---|
| `BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` — 45,667 bytes, `DF4630CF…81DD7` | `EXACT` |
| `BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` — 21,949 bytes, `48BE744A…3BAB01` | `EXACT` |
| Recomputed aggregate manifest identity | `EXACT` — `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D` |
| Amended `BANPU_WP3_WORK_PACKAGE_PLAN.md` — 49,541 bytes, `84E1EC24…23045D` | `EXACT` |
| `BANPU_WP3_BOUNDED_PLANNING_AMENDMENT_RECORD.md` unmodified | `SATISFIED` |
| `BANPU_WP3_PLANNING_AMENDMENT_CONFIRMATION.md` unmodified | `SATISFIED` |
| `BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md` unmodified | `SATISFIED` |
| `BANPU_WP3_AMENDED_ALLOCATION_RECORD.md` unmodified | `SATISFIED` |
| `BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md` unmodified | `SATISFIED` |
| Historical `BANPU_WP3_ALLOCATION_RECORD.md` unmodified | `SATISFIED` |
| Historical `BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md` unmodified | `SATISFIED` |
| Historical `BANPU_WP3_WORK_PACKAGE_PLAN_APPROVAL.md` unmodified — 7,441 bytes, `B4D287AD…F446ED3` | `SATISFIED` |
| All production files unmodified by this act | `SATISFIED` — pre-existing dirty state only, listed in §8 |
| All test files unmodified by this act | `SATISFIED` — pre-existing dirty state only, listed in §8 |

## 8. Repository hygiene

| Check | Result |
|---|---|
| `git diff --check` | `PASS` — exit 0 (only pre-existing benign LF→CRLF conversion warnings) |
| `git diff --cached --check` | `PASS` — exit 0 |
| Paths changed by this act | `docs/implementation/BANPU_WP3_WORK_PACKAGE_PLAN.md` (amended in place) and one new path, `docs/implementation/BANPU_WP3_WORK_PACKAGE_PLAN_AMENDED_APPROVAL.md` |
| Pre-existing staging state | Unaltered by this act |

**Pre-existing dirty state, disclosed and not caused by this act.**
`backend/main.py`, `backend/services/data_fetcher.py`,
`backend/services/market_data/yahoo_chart.py`,
`backend/tests/test_fetch_history.py`,
`backend/tests/test_yahoo_chart_provider.py`, the staged BANPU-WP3 governance
artifacts, and the untracked WP3 accessor/test files and prior BPA-1
governance records all predate this act and are unmodified by it.

## 9. Excluded effects

This record does **not**:

- perform the Focused C3 Accessor-Delta Review or accept the accessor
  implementation;
- perform Step 4.1 eleven-site evidence work;
- resume or modify WP3.4 implementation;
- complete or re-review C4;
- reopen C1, C2, or accepted pre-accessor C3 (WP3.3) semantics;
- modify the frozen planning artifacts, any BPA-1 governance record, the
  historical Allocation Record, the historical Implementation Authorization
  Record, or the historical Work Package Plan Approval record;
- modify any production or test file;
- commit, push, deploy, or release.

## 10. Final disposition

**BANPU-WP3 BPA-1 WORK PACKAGE PLAN AMENDED AND REAPPROVED** at governing
corpus identity `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`.

## 11. Exact next act

**Focused Independent C3 Accessor-Delta Review.**

This record performs no part of that review.
