# BANPU-WP3 — Allocation Record

**Artifact class:** Additive constitutional allocation record
**Allocation date:** 2026-08-10
**Issuing role:** BANPU-WP3 Allocation Authority
**Allocated work package:** `BANPU-WP3 — Quote identity and epoch protection (planning ownership only)`
**Disposition:** `BANPU-WP3 ALLOCATED`
**Implementation authority created:** `NONE`
**Work Package Plan authorized:** `NO`
**WP4+ authority created:** `NONE`

## 1. Executive summary

The frozen BANPU-WP3 planning corpus is allocated at corpus identity
`C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`, unchanged
since Planning Freeze.

This act allocates **planning ownership only**. It marks the frozen, byte-
identified planning corpus as the fixed target of a separately governed
BANPU-WP3 Implementation Authorization act. It authorizes no implementation, no
production or test change, and no Work Package Plan. Every frozen planning
decision, observation, residual, and gate is carried forward exactly as frozen
and is reinterpreted in no respect.

Independent verification was performed before allocation: the Planning Freeze
Record was verified as present and dispositive; both corpus artifacts were
re-hashed from working-tree bytes; the aggregate manifest identity was
recomputed and matched exactly; and no planning amendment was found after
Planning Freeze.

## 2. Constitutional authority

Acting solely as the BANPU-WP3 Allocation Authority, this act allocates the
planning corpus frozen by
[BANPU-WP3 Planning Freeze Record](BANPU_WP3_PLANNING_FREEZE_RECORD.md) §4,
disposition `BANPU-WP3 PLANNING COMPLETE, CONFIRMED, AND FROZEN`, which itself
derives from the concluded BANPU-WP3 Planning Confirmation
(`PLANNING CONFIRMED WITH MINOR OBSERVATIONS`), the concluded Focused Planning
Re-review (`APPROVED`), and the Architecture Owner ratification of 2026-08-10
that satisfied gate S2.

This authority is limited to identity binding, corpus-boundary verification, and
creation of this allocation record. It grants no authority to implement, to
authorize implementation, to draft a Work Package Plan, or to allocate WP4 or
any later package. It reinterprets no planning decision.

## 3. Allocation scope

### 3.1 What is allocated

`BANPU-WP3 — Quote identity and epoch protection`, exactly and only as defined
by the frozen planning corpus. Allocation does not change, narrow, or widen this
scope.

The allocated corpus is the exact two-file candidate frozen by the Planning
Freeze Record, unchanged since freeze:

| # | Allocated frozen artifact | Bytes | Physical lines | SHA-256 |
|---|---|---:|---:|---|
| 1 | `docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | 40,882 | 688 | `1F4E21FBC275FF5AA6CC061E2A7AD7972B41008926D8E8E4648C1C07A9C2F096` |
| 2 | `docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | 17,909 | 430 | `A6A4AB0AC4DE1E7B1813EEFFB01E2F48A662DA9B937F1BF1A45982B065294462` |

Aggregate corpus manifest identity, unchanged from Planning Freeze Record §4:

```text
C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A
```

Corpus cardinality: `2`. No file in this table has been modified, and no third
file has been added to the allocated corpus.

### 3.2 Allocated substantive scope, as frozen

Allocated exactly as written in the frozen corpus, without restatement that
could operate as reinterpretation:

- the in-scope and out-of-scope boundaries in Plan §3, including the design §10
  obligations expressly not discharged by WP3;
- the boundary verification against WP1, WP2, and WP4 through WP8 in Plan §4;
- the architectural positions in Plan §5, including unconditional Option C,
  provider neutrality, the four-layer decomposition, and backward compatibility;
- the canonical acceptance criteria A1 through A5 and the derived criteria A6
  through A14 in Plan §9;
- the planning gates S1 through S7 in Plan §10 and S1 through S8 in
  Decomposition §6; and
- the sub-package decomposition WP3.1 through WP3.4, its strict serial order,
  and the authorized file surfaces in Decomposition §2 and §4.

### 3.3 Frozen planning decisions preserved exactly

Carried into allocation exactly as frozen. This record restates them for
identification only and does not reinterpret, extend, weaken, or condition any
of them.

| Item | Frozen decision | Recorded at |
|---|---|---|
| PD-1 | `NARROW` — the corrected close derivation applies only where required to prevent epoch mixing for a converted identity; unconverted and unbound derivation is numerically unchanged; design §2 goal 8, principle 10, roadmap §5, and criterion A4 remain unamended; pre-change characterization evidence remains required before the first production edit | Plan §6.1 |
| PD-2 | `RATIFIED AS SPECIFIED` — exchange-local calendar dates from the provider-reported exchange timezone; UTC-date comparison rejected | Plan §6.2 |
| PD-3 | `RESOLVED` as to WP3 scope by restatement of canonical text; the emitter-locus item is referred out and is not a WP3 decision, residual, or obligation | Plan §6.4 |
| PD-4 | `RATIFIED AS SPECIFIED` — the E1 through E5 Provider Evidence Contract is binding; non-satisfaction is a first-class quarantine condition | Plan §6.3 |
| PD-5 | `RATIFIED` — invariant G1 through G4; no implementation mechanism is prescribed, and mechanism selection remains with a future implementation authority | Plan §6.5 |
| R7 | `PATH B — FORMAL WAIVER`, scoped exactly to "No BANPU-WP3 obligation is inherited" | Plan §6.7 |

The R7 waiver is allocated in its exact frozen scope. It defines, reinterprets,
weakens, and resolves nothing. The seven WP2 residuals `MINOR-A`, `MINOR-B`, and
`OBSERVATION-A` through `OBSERVATION-E` remain carried forward exactly as
accepted; BANPU-WP4 through BANPU-WP8 inherit them unchanged.

### 3.4 Observation O-1 preserved exactly

Gate S8 — rule 7 reviewer confirmation for the WP3.2 module — remains an
implementation-entry gate for BANPU-WP3.2 only. It is not part of gate S2, it
did not affect Planning Confirmation or Planning Freeze, and it does not affect
this allocation. It is **not** a planning defect, a planning finding, an open
planning decision, or a residual.

Gate S8 is allocated in that exact state. It stands `Open` in Decomposition §6,
which is its correct pre-WP3.2 condition, and it remains an additional gate that
must be satisfied before WP3.2 begins — after, and separately from, any future
implementation authorization.

### 3.5 Residuals allocated unresolved

Carried forward unresolved and unreinterpreted, exactly as recorded in Plan §12
and Planning Freeze Record §8:

| Residual | State at allocation |
|---|---|
| R6 — the canonical roadmap names `backend/tests/test_fetch_history.py` as WP3 regression evidence although it is a live print script | Recorded for separately approved documentation correction; the roadmap is not amended |
| The R7 formal waiver | Carried as a planning-freeze residual; binds WP3 alone |
| WP1's `backend/models/database.py` identity residual and the WP2 Step 8 gate language | Carried forward unchanged and not reinterpreted |

Allocation resolves, closes, weakens, and waives none of them.

## 4. Allocation boundaries

### 4.1 What this allocation is

Allocation of **planning ownership only** over the frozen corpus in §3.1. Its
sole effect is to mark that corpus as allocated and to identify it as the fixed
target against which a separately governed BANPU-WP3 Implementation
Authorization act may operate.

### 4.2 What this allocation is not

This act does **not**:

- authorize BANPU-WP3 implementation;
- create, draft, commission, or authorize a BANPU-WP3 Work Package Plan;
- authorize any production change, including to
  `backend/services/market_data/yahoo_chart.py`,
  `backend/services/data_fetcher.py`, or `backend/main.py`;
- authorize any test change, including to
  `backend/tests/test_yahoo_chart_provider.py` or
  `backend/tests/test_fetch_history.py`;
- authorize the new WP3.2 production module, which additionally requires the
  gate S8 rule 7 confirmation;
- begin, plan, or authorize BANPU-WP4 or any later package;
- reinterpret, amend, narrow, widen, or condition any frozen planning decision,
  gate, acceptance criterion, or file surface;
- resolve, close, or waive any carried-forward residual, or reopen any ratified
  decision;
- resolve the emitter-locus item referred out by PD-3;
- amend or reinterpret the canonical design, roadmap, or implementation
  sequence;
- modify any frozen planning artifact, or amend, reopen, or reinterpret
  BANPU-WP1 or BANPU-WP2 or any of their lifecycle records;
- change, reopen, or synchronize M46, which remains constitutionally independent
  and suspended; or
- commit, push, deploy, migrate, or mutate production data.

### 4.3 Implementation prohibition

BANPU-WP3 implementation is **not authorized** by this allocation. Allocating
the frozen planning corpus identifies it as the target for a future
authorization act; it does not itself grant that authorization. No production,
schema, migration, or test file may be changed under color of this record.

Baseline gate S5 remains in force: pre-change characterization evidence must be
captured before the first production edit, and it is unrecoverable afterwards.
Nothing in this record permits that first edit.

## 5. Allocation verification

Performed independently before allocation. All identity values were recomputed
from current repository bytes, not transcribed from the Planning Freeze Record.

| # | Required verification | Result |
|---|---|---|
| V1 | Planning Freeze Record exists and is dispositive | `SATISFIED` — `BANPU_WP3_PLANNING_FREEZE_RECORD.md` present, disposition `BANPU-WP3 PLANNING COMPLETE, CONFIRMED, AND FROZEN`; 20,789 bytes, 390 physical lines, SHA-256 `85FBDF9DB5B8EAC71A9DA7C82445E5A465E61548FD235A93D1E2A96E22924D90` |
| V2 | Frozen corpus identity matches the allocation target, per file | `SATISFIED` — both per-file SHA-256 and byte counts recomputed and identical to Planning Freeze Record §4 |
| V3 | Aggregate manifest identity matches | `SATISFIED` — recomputed `C7B6CEEF…0670638A`, exact match; manifest method re-applied as defined in Planning Freeze Record §4 |
| V4 | No planning amendment after Planning Freeze | `SATISFIED` — corpus bytes unchanged; both artifacts remain untracked and unmodified since freeze; no edit event exists between the freeze act and this act |
| V5 | Corpus cardinality unchanged | `SATISFIED` — exactly two planning artifacts; no third WP3 planning artifact exists |
| V6 | Identity convention preserved | `SATISFIED` — both artifacts still contain zero `CR` bytes, so raw and LF-normalized identities remain byte-identical, exactly as recorded in Planning Freeze Record §4.1 |
| V7 | Allocation scope equals frozen planning scope | `SATISFIED` — §3 allocates the frozen corpus and its frozen scope with no addition, removal, narrowing, or widening |
| V8 | PD-1, PD-2, PD-4, PD-5, and R7 Path B preserved exactly | `SATISFIED` — §3.3, transcribed from Plan §6.0 through §6.7 without alteration |
| V9 | Observation O-1 preserved exactly | `SATISFIED` — §3.4, carried at its recorded altitude and not elevated |
| V10 | Gate S8 preserved as an implementation-entry gate | `SATISFIED` — §3.4; state `Open` in Decomposition §6 is unchanged by this act |
| V11 | No planning decision open | `SATISFIED` — Plan §6.6 register closed on all five items |
| V12 | No successor authority beyond allocation created | `SATISFIED` — §6 and §7 |

## 6. Successor authority created

This allocation creates exactly one thing: the recorded allocation of the frozen
planning corpus in §3.1, as the fixed target for a separately governed
BANPU-WP3 Implementation Authorization act.

Stated explicitly, as required:

- **Implementation authority remains `NONE`.**
- **The Work Package Plan has not been authorized.**
- **Allocation creates no implementation authority.**
- **Allocation creates no WP4 authority.**

Gate S3 places the drafting of the BANPU-WP3 Work Package Plan after Allocation
in the frozen sequence. That sequencing fact is unchanged and is recorded here
for accuracy only; this act neither drafts, commissions, nor authorizes such a
plan, and no Work Package Plan may be created under color of this record.

## 7. Excluded authority

This allocation creates:

- `NO` BANPU-WP3 implementation authority;
- `NO` authority to draft or authorize a BANPU-WP3 Work Package Plan;
- `NO` authority to change any production file;
- `NO` authority to change any test file;
- `NO` authority to add the WP3.2 production module, which remains additionally
  gated by S8;
- `NO` BANPU-WP4 or later-package authority;
- `NO` authority to reopen, amend, or reinterpret the frozen BANPU-WP3 planning
  corpus;
- `NO` authority to reopen or amend frozen BANPU-WP1 or BANPU-WP2;
- `NO` authority to resolve any carried-forward residual or the referred
  emitter-locus item;
- `NO` release authority; and
- `NO` authority over M46, which remains constitutionally independent and
  suspended.

## 8. Repository verification

| Verification | Result |
|---|---|
| Only `docs/implementation/BANPU_WP3_ALLOCATION_RECORD.md` created by this act | `SATISFIED` |
| No implementation file changed | `SATISFIED` — no production, service, model, migration, or test file appears in `git status` |
| No frozen planning artifact changed | `SATISFIED` — both WP3 corpus artifacts byte-identical to their frozen identities |
| No WP1 or WP2 artifact changed | `SATISFIED` |
| No canonical design, roadmap, or implementation-sequence file changed | `SATISFIED` |
| No M46 file changed | `SATISFIED` |
| No frontend or schema change | `SATISFIED` |
| `git status --porcelain` before this act | Three entries, all untracked: the two frozen planning artifacts and the Planning Freeze Record; nothing else differs |
| `git diff --check` | `PASS` — exit 0 |
| `git diff --cached --check` | `PASS` — exit 0; nothing staged |
| Repository state boundary | Branch `feature/banpu-remediation`, HEAD `3a0bbe726dd4f2de67a8e6d3dbe227b4b5b27f44` |
| No staging or commit | `SATISFIED` — this act stages no commit |
| `graphify update .` | Not run; no source file changed by this act, so no code-graph node is affected |

The recursive `Permission denied` warnings emitted by `git status` for
`backend/.pytest-m32-3e3r2*` directories are pre-existing environmental noise,
unrelated to this act, and affect no verification above.

## 9. Final disposition

**BANPU-WP3 ALLOCATED** at the frozen corpus identity
`C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`.

Implementation authority remains `NONE`. The Work Package Plan has not been
authorized. This allocation creates no implementation authority and no WP4
authority. BANPU-WP1 and BANPU-WP2 remain frozen and unmodified. The frozen
BANPU-WP3 planning corpus remains frozen and unmodified. M46 remains
constitutionally independent and suspended.

## 10. Exact next constitutional act

The exact next authorized constitutional act is **BANPU-WP3 Implementation
Authorization**, performed by a distinct authorization authority, over the exact
allocated candidate identified in §3.1.

That act, if granted, would be the first act permitted to authorize changes to
the WP3 file surface. Implementation itself remains a separate, later act even
after authorization, gate S5 baseline capture precedes the first production
edit, and gate S8 remains an additional entry gate before WP3.2 begins. WP4 and
later packages remain unauthorized until their own independently governed
sequence completes.

This record performs no part of that act.
