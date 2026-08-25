# BANPU-WP3 — Amended Planning Freeze Record `BPA-1`

**Artifact class:** Additive constitutional freeze record
**Freeze date:** 2026-08-11
**Amendment identifier:** `BPA-1`
**Issuing role:** Independent Amended Planning Freeze Authority
**Pre-amendment frozen corpus identity:** `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
**Frozen amended corpus identity:** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Disposition:** `BANPU-WP3 BPA-1 AMENDED PLANNING CORPUS FROZEN`
**Implementation authority created by this act:** `NONE`

---

## 1. Constitutional authority and basis

Acting solely as the BANPU-WP3 Independent Amended Planning Freeze Authority,
this act freezes the exact confirmed amended planning candidate identified in
§3. Authority derives from
[BANPU-WP3 Planning Amendment Confirmation `BPA-1`](BANPU_WP3_PLANNING_AMENDMENT_CONFIRMATION.md),
disposition `BANPU-WP3 BPA-1 PLANNING AMENDMENT CONFIRMED`, which itself rests
on the concluded Independent Bounded Planning Amendment Review, disposition
`BANPU-WP3 BPA-1 INDEPENDENTLY APPROVED`.

Independently verified before this act:

| Check | Result |
|---|---|
| BPA-1 independently reviewed and approved | `SATISFIED` — Confirmation §1 records disposition `BOUNDED PLANNING AMENDMENT — APPROVED` / `BANPU-WP3 BPA-1 INDEPENDENTLY APPROVED`, with no unresolved `BLOCKING`, `MAJOR`, or `MINOR` finding |
| BPA-1 subsequently confirmed | `SATISFIED` — Confirmation record disposition `BANPU-WP3 BPA-1 PLANNING AMENDMENT CONFIRMED` |
| Confirmation binds exactly the candidate aggregate identity `3A04B06A…D8F43D` | `SATISFIED` — Confirmation §2 states this identity as the confirmed amended corpus identity, and independently recomputed in §3 below |
| Confirmation created no implementation authority | `SATISFIED` — Confirmation header and §5 state `NONE` explicitly |
| No successor freeze has already occurred | `SATISFIED` — `docs/implementation/BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md` did not exist prior to this act |

**Disclosure — external review evidence.** Consistent with the disclosure
precedent of the original
[BANPU-WP3 Planning Freeze Record](BANPU_WP3_PLANNING_FREEZE_RECORD.md) §3, no
separate repository artifact for the Independent Bounded Planning Amendment
Review exists; this freeze relies on its recording in the Confirmation record
and re-adjudicates no finding.

This authority is limited to identity binding, corpus-boundary verification,
and creation of this record. It grants no authority to allocate, authorize
implementation, reapprove the Work Package Plan, or perform the focused C3
delta review.

## 2. Freeze purpose

This record makes the confirmed amended BANPU-WP3 planning corpus immutable at
its confirmed content identity, superseding the pre-amendment frozen corpus as
the current planning target, while preserving the pre-amendment freeze record
as historical evidence of the superseded state.

## 3. Frozen amended planning corpus identity

The frozen amended planning corpus contains exactly two files, independently
rehashed from working-tree bytes immediately before this record was added.

| # | Frozen artifact | Bytes | SHA-256 |
|---|---|---:|---|
| 1 | `docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | 45,667 | `DF4630CFC00A32402B45489D1779F3BBAAD39A86630301256C541BC806481DD7` |
| 2 | `docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | 21,949 | `48BE744AD91367293FF790772A96FA49D60058CF0221080F538AE6FBEB3BAB01` |

Corpus cardinality: `2`. This freeze record is a lifecycle artifact and is not
a member of the frozen corpus it identifies.

The manifest convention is the two listed repository-relative paths in table
order, each encoded as `path<TAB>SHA-256<TAB>bytes<LF>` in UTF-8, with
uppercase hexadecimal digests and plain decimal byte counts. Its independently
recomputed aggregate identity is:

```text
3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D
```

This exactly matches the candidate identity reviewed by the Independent
Bounded Planning Amendment Review and bound by the Planning Amendment
Confirmation. Both artifacts contain zero `CR` bytes, so raw and
LF-normalized identities coincide.

## 4. Supersession relationship

This freeze supersedes the pre-amendment frozen corpus identified by the
original [Planning Freeze Record](BANPU_WP3_PLANNING_FREEZE_RECORD.md) §4:

```text
C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A
```

That identity, and the record that froze it, remain **historical evidence**
of the pre-amendment planning state. Neither is rewritten, deleted, or
reinterpreted by this act. From this freeze forward, the identity in §3 above
is the current planning corpus identity; the superseded identity must not be
represented as current.

## 5. What this freeze does not do

This act creates **no implementation authority** and performs none of the
following, all of which remain **outstanding**:

- **Allocation synchronization** — `BANPU_WP3_ALLOCATION_RECORD.md` still
  binds the superseded pre-amendment identity and is not synchronized by this
  act.
- **Implementation Authorization synchronization** —
  `BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md` still binds the
  superseded pre-amendment identity and is not synchronized by this act.
- **Work Package Plan amendment/reapproval** —
  `BANPU_WP3_WORK_PACKAGE_PLAN.md` and its approval record are not amended,
  reissued, or reapproved by this act.
- **Focused C3 accessor-delta review** — not performed by this act; the
  accessor added under BPA-1 remains unreviewed at the C3 level.
- **C4 re-review** — `C4` remains incomplete; it requires both the focused C3
  delta acceptance above and completion of Step 4.1 eleven-site evidence.
- Acceptance of the accessor implementation itself.
- Any commit, push, deployment, or release.

## 6. Preserved constitutional state

Preserved exactly, and unaltered by this act:

- **C1 accepted** — WP3.1 acceptance stands, unreopened.
- **C2 accepted** — WP3.2 acceptance stands, unreopened.
- **C3 accepted for the pre-accessor WP3.3 state** — the accessor delta
  remains a separately reviewable focused C3 delta, not yet independently
  accepted.
- **C4 incomplete** — unchanged by this act.
- **WP3.1 and WP3.2 semantics** — unchanged.
- **Accepted pre-accessor WP3.3 semantics** — unchanged.
- **WP1 and WP2** — unchanged.
- **WP5 boundary** — unchanged; this act exposes no boundary evidence and
  performs no tolerance or reconciliation evaluation.
- **A1 through A14** — unchanged, preserved verbatim.
- **PD-1 through PD-5** — unchanged, unreinterpreted, unconditioned.

## 7. Post-write identity verification

After creating this record, both planning artifacts and the aggregate
manifest were independently rehashed:

| Check | Result |
|---|---|
| `BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` — 45,667 bytes, `DF4630CF…81DD7` | `EXACT` |
| `BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` — 21,949 bytes, `48BE744A…3BAB01` | `EXACT` |
| Recomputed aggregate manifest identity | `EXACT` — `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D` |
| Planning Amendment Confirmation record unmodified by this act | `SATISFIED` |
| Bounded Planning Amendment Record (`BPA-1`) unmodified by this act | `SATISFIED` |
| Original Planning Freeze Record unmodified by this act | `SATISFIED` |
| This freeze record is not a member of the two-file planning corpus | `SATISFIED` |

## 8. Repository hygiene

| Check | Result |
|---|---|
| `git diff --check` | `PASS` — exit 0 |
| `git diff --cached --check` | `PASS` — exit 0 |
| Path created by this act | Exactly one: `docs/implementation/BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md` |
| Pre-existing staging state | Unaltered by this act |

**Pre-existing dirty state, disclosed and not caused by this act.**
`backend/main.py`, `backend/services/data_fetcher.py`,
`backend/services/market_data/yahoo_chart.py`,
`backend/tests/test_fetch_history.py`, `backend/tests/test_yahoo_chart_provider.py`,
the staged BANPU-WP3 governance artifacts (`BANPU_WP3_ALLOCATION_RECORD.md`,
`BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md`,
`BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md`,
`BANPU_WP3_PLANNING_FREEZE_RECORD.md`,
`BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md`,
`BANPU_WP3_WORK_PACKAGE_PLAN.md`, `BANPU_WP3_WORK_PACKAGE_PLAN_APPROVAL.md`),
and the untracked WP3 accessor/test files and prior BPA-1 governance records
all predate this act and are unmodified by it. The recursive
`Permission denied` warnings `git status` emits for
`backend/.pytest-m32-3e3r2*` directories are pre-existing environmental noise
and affect no verification above.

## 9. Excluded effects

This record does **not**:

- authorize, allocate, or begin implementation of any kind;
- synchronize the Allocation Record or the Implementation Authorization
  Record;
- amend or reapprove the Work Package Plan;
- perform the focused C3 accessor-delta review or accept the accessor
  implementation;
- complete or re-review C4;
- reopen C1, C2, or accepted pre-accessor C3 (WP3.3) semantics;
- modify the two amended planning artifacts, the Planning Amendment
  Confirmation record, the Bounded Planning Amendment Record, or the original
  Planning Freeze Record;
- modify any production or test file;
- commit, push, deploy, or release.

## 10. Freeze disposition

**BANPU-WP3 BPA-1 AMENDED PLANNING CORPUS FROZEN** at the corpus identity in
§3.

## 11. Exact next act

**BANPU-WP3 Allocation Synchronization to Amended Planning Corpus.**

This record performs no part of that act.
