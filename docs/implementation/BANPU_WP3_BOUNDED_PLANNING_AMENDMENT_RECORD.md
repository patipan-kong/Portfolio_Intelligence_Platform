# BANPU-WP3 — Bounded Planning Amendment Record `BPA-1`

**Artifact class:** Constitutional planning amendment record
**Amendment identifier:** `BPA-1`
**Date:** 2026-08-11
**Issuing authority:** BANPU-WP3 Bounded Planning Amendment Authority
**Occasion:** Independent Checkpoint C4 Review — `CHECKPOINT C4 — CHANGES REQUIRED`; independent authority determination `C — PLANNING AMENDMENT REQUIRED`
**Subject:** The single WP3.4 propagation-surface deficiency
**Disposition:** `BANPU-WP3 BOUNDED PLANNING AMENDMENT PREPARED — READY FOR INDEPENDENT REVIEW`
**Prior authorized planning corpus identity:** `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
**Amended planning corpus identity (candidate, not yet frozen):** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Implementation performed by this act:** `NONE`
**New implementation authority created:** `NONE`

---

## 1. Nature of this act

This record prepares a **bounded amendment** to the frozen BANPU-WP3 planning
corpus, confined to the single surface-allocation deficiency identified by
Independent Checkpoint C4 Review.

It is:

- **Amending**, unlike the
  [Reference-Price Admissibility Clarification Record](BANPU_WP3_REFERENCE_PRICE_ADMISSIBILITY_CLARIFICATION_RECORD.md),
  which was interpretive only. Frozen planning bytes are changed, and the
  planning corpus identity therefore changes.
- **Bounded.** It authorizes exactly one accessor in exactly one file for
  exactly one consumer.
- **Non-authorizing beyond that.** It creates no implementation authority beyond
  the surface it admits, opens no work package, and satisfies no gate.
- **Non-performing.** It performs no implementation, no confirmation, no freeze,
  no allocation, no authorization, and no review.

This act does **not** redesign WP3, does not reopen accepted WP3.1–WP3.3
semantics, and does not broaden `backend/services/data_fetcher.py` generally.

## 2. Established deficiency

Independent Checkpoint C4 Review concluded `CHECKPOINT C4 — CHANGES REQUIRED`,
and independent authority determination concluded
`C — PLANNING AMENDMENT REQUIRED`, on the following facts, each independently
verified against the live repository before this act (§9):

| # | Fact | Verification |
|---|---|---|
| 1 | WP3.4 requires the portfolio-holdings price call path in `backend/main.py` to propagate the successor binding | Decomposition §4.4; Plan §5.4 |
| 2 | Under the frozen corpus, `backend/main.py` cannot lawfully derive that binding itself — it holds no canonical conversion field | `backend/main.py` imports no canonicalizer and references no `POSITION_CONVERSION` payload field; the endpoint holds portfolio holdings and symbols only |
| 3 | Re-querying or re-canonicalizing `POSITION_CONVERSION` data, or constructing bindings, in `backend/main.py` would duplicate WP3.3 and WP3.2 ownership | Plan §6.5 G1; Plan §9.2 A7; Plan §6.4 obligation B1 |
| 4 | Importing private WP3.3 guard-projection internals into `backend/main.py` would cross the accepted WP3.3 boundary | The projection type and reader are module-private in `backend/services/data_fetcher.py` |
| 5 | Leaving the request unbound fails the WP3.4 propagation outcome | Decomposition §4.4 deliverables |
| 6 | A technically narrow implementation already exists and satisfies every constraint below | `backend/services/data_fetcher.py` `resolve_successor_bindings(symbols)` |
| 7 | The defect is authority and surface allocation, not runtime correctness | This record |

**The defect, stated exactly.** The frozen corpus fixes *that* the holdings and
price call path must propagate a binding, and fixes *where* the binding is
constructed, but allocates no surface by which the one may reach the other.

## 3. Exact bounded amendment

### 3.1 Planning artifacts amended

Exactly two — the entire frozen planning corpus:

| # | Artifact | Amendment |
|---|---|---|
| 1 | `docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | Header `Amendment:` line; new §5.3.1; closing paragraph appended to §5.4 |
| 2 | `docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | Header `Amendment:` line; one line added to §4.4 "Files expected to change"; new §4.4.1 |

No other line of either artifact was altered. Every edit is additive; no
existing sentence, table row, criterion, gate, decision, or risk was removed,
reworded, or renumbered.

### 3.2 What is authorized

| Item | Value |
|---|---|
| File | `backend/services/data_fetcher.py` |
| Accessor | `resolve_successor_bindings(symbols)` |
| Sub-package | WP3.4 |
| Class | Production, read-only |
| Purpose | Expose requested, non-ambiguous canonical `SuccessorQuoteBinding` values from the already-accepted WP3.3 conversion guard projection, solely so the authorized WP3.4 holdings and price call path in `backend/main.py` can propagate bindings |

### 3.3 Constraints, binding on implementation

Reproduced from Decomposition §4.4.1, which governs. The accessor:

1. creates no persistent state;
2. performs no memoization and holds no cache;
3. changes no guard-membership semantics;
4. changes no quarantine policy and adds, removes, or reinterprets no quarantine
   reason;
5. changes no `fetch_price_info` or `fetch_history` semantics, signature
   contract, or return shape;
6. performs no provider lookup;
7. performs no registry lookup;
8. reads no environment value and no configuration value;
9. exposes no boundary evidence;
10. constructs no binding outside the accepted WP3.2 and WP3.3 machinery;
11. leaves ambiguous and unavailable projection states fail-closed;
12. authorizes no caller other than the single WP3.4 holdings and price call path
    in `backend/main.py`;
13. confers on WP3.4 no authority over any other
    `backend/services/data_fetcher.py` behavior.

## 4. The seven required statements

Recorded here in one place; each is also stated in the amended corpus at the
section cited.

| # | Statement | Recorded at |
|---|---|---|
| 1 | **Why the original WP3.4 surface was insufficient.** WP3.4's authorized production surface is the `backend/main.py` holdings and price call site alone. A binding's five elements are all drawn from a WP1-canonicalized `POSITION_CONVERSION` payload; that call path holds none of them. The propagation outcome was unreachable by any lawful edit | Plan §5.3.1 |
| 2 | **Why a `main.py`-only implementation would force forbidden policy duplication.** Deriving the binding there requires ledger reading, WP1 canonicalization, binding construction, and ambiguity/undetermined-membership decisions — a second membership authority (forbidden by PD-5 G1) and a second quarantine policy (forbidden by A7 and PD-3 B1) | Plan §5.3.1 |
| 3 | **Why the accessor is cross-package plumbing, not new architecture.** It introduces no layer, abstraction, policy, or state, and decides nothing; every decision it surfaces was already made by the accepted WP3.2 contract and WP3.3 projection. Dependency direction is unchanged and still strictly upward | Plan §5.3.1, §5.4 |
| 4 | **Why `data_fetcher.py` remains WP3.3-owned for enforcement.** Ownership follows the obligation, not the file. Guard projection, PD-5 G1–G4, binding-aware fetch, cache namespacing, stale-fallback suppression, PD-4 enforcement, and quarantine logging all remain WP3.3's, unamended. One read-only accessor is admitted; the file is not reallocated | Plan §5.3.1; Decomposition §4.4.1 |
| 5 | **Prior C3 acceptance remains valid for the pre-accessor WP3.3 state.** No accepted WP3.1, WP3.2, or WP3.3 semantics are reopened | Decomposition §4.4.1 |
| 6 | **The accessor itself requires a focused C3 delta review**, scoped to the accessor and constraints 1–13, after reconfirmation, re-freeze, and Allocation/Authorization synchronization | Decomposition §4.4.1 |
| 7 | **C4 remains incomplete** until the accessor delta receives focused C3 acceptance *and* Step 4.1 exhaustive eleven-site evidence is completed | Decomposition §4.4.1 |

## 5. Why no broader planning change is required

Fail-closed test applied: had the amendment required any element below, this act
would have halted and returned to governance rather than proceeding. None was
required.

| Candidate broader change | Required? | Why not |
|---|---|---|
| New architectural layer or abstraction | No | The accessor reads an existing projection; it introduces no structure |
| New or amended planning decision (PD-1…PD-5) | No | Membership authority, epoch convention, evidence contract, and guard freshness are untouched; the accessor consults the same projection those decisions govern |
| New or amended acceptance criterion (A1–A14) | No | A13 confines the change surface to the **authorized file lists**, and `backend/services/data_fetcher.py` was already inside WP3's package-level surface (Decomposition §2). Only the *sub-package* allocation was deficient. A1–A14 are preserved verbatim |
| New gate | No | The focused C3 delta review is an amendment-borne obligation inside the existing gate S4 discipline; the §6 gate table is unamended |
| New quarantine reason or admissibility element | No | Constraint 4 and constraint 10 forbid both |
| Change to the R7 waiver | No | Untouched; it binds WP3 alone, exactly as frozen |
| Change to the WP5 reference-price / tolerance boundary | No | The accessor exposes no boundary evidence (constraint 9) and performs no tolerance, reconciliation, or continuity evaluation |
| Change to WP3's package-level file surface | No | Decomposition §2 already lists `backend/services/data_fetcher.py` under "Expected to change" |
| Reopening WP3.1, WP3.2, or WP3.3 | No | §4 statement 5 |
| Widening `data_fetcher.py` for WP3.4 generally | No | Constraint 13 forecloses it explicitly |
| Any WP1 or WP2 change | No | §9 verifies both frozen corpora unchanged |

## 6. Preservation

Preserved exactly, and unaltered by this act:

- **WP3.1 evidence ownership** — provider evidence extraction and the E1–E5
  evidence structure remain WP3.1's.
- **WP3.2 pure contract ownership** — binding construction, epoch
  classification, admissibility, and the quarantine reason contract remain
  WP3.2's, and the module remains pure.
- **WP3.3 enforcement ownership** — every enforcement obligation in
  `backend/services/data_fetcher.py` remains WP3.3's (§4 statement 4).
- **C1, C2, and C3 accepted semantics** — unchanged and unreopened.
- **PD-1 through PD-5** — unchanged, unreinterpreted, unconditioned.
- **The R7 formal waiver** — unchanged in scope and effect.
- **A1 through A14** — preserved verbatim. The amendment required no criterion
  change; the surface clarification lands in Plan §5.3.1 and Decomposition
  §4.4.1, not in §9.2 (§5).
- **The WP5 reference-price and mechanical-tolerance boundary** — unchanged, and
  reinforced by constraint 9.
- **PD-3's referred emitter-locus item** — still referred out; not a WP3
  decision, residual, or obligation.
- **Gate S8 and Observation O-1** — unchanged at their recorded state.
- **Residuals R6, the R7 waiver, and the WP1 `database.py` identity residual** —
  carried forward unresolved and unreinterpreted.
- **All WP1 and WP2 frozen state** — unchanged (§9).

## 7. Effect on prior acceptance and on C4

### 7.1 C1 and C2

**No effect.** WP3.1 and WP3.2 acceptance stands. No WP3.1 re-review and no
WP3.2 re-review is required or implied. Neither is reopened.

### 7.2 C3

**Prior C3 acceptance remains valid for the pre-accessor WP3.3 state.** No full
WP3.3 re-review is required. The accessor is a delta on top of that accepted
state and requires a **focused C3 delta review**, scoped to the accessor and to
the thirteen constraints of §3.3, performed after the successor governance acts
of §8 complete.

### 7.3 C4

**C4 remains incomplete.** It closes only when both of the following hold:

1. the accessor delta receives focused C3 acceptance; and
2. Step 4.1 exhaustive eleven-site unbound call-site evidence is completed.

This record performs neither, accepts neither, and does not re-review C4.

## 8. Lifecycle consequences

### 8.1 Required successor acts, in order

Because frozen planning bytes changed, the full planning lifecycle re-runs over
the amended candidate:

1. **Independent Bounded Planning Amendment Review** — of this amendment and the
   amended corpus.
2. **BANPU-WP3 Planning Amendment Confirmation.**
3. **BANPU-WP3 Amended Planning Freeze** — binding the amended corpus identity
   `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`.
4. **Allocation and Implementation Authorization synchronization** — both
   records bind the superseded identity `C7B6CEEF…0670638A` in their headers and
   bodies and must be synchronized to the amended identity.
5. **BANPU-WP3 Work Package Plan amendment and reapproval** — see §8.3.
6. **Focused C3 delta review** of the accessor.
7. **Completion of Step 4.1 eleven-site evidence**, then **C4 re-review**.

### 8.2 Not required

- WP3.1 re-review.
- WP3.2 re-review.
- Full WP3.3 re-review.
- Reopening C1 or C2.
- Planning redesign outside this bounded surface.

### 8.3 Work Package Plan — amendment required

**Yes.** `docs/implementation/BANPU_WP3_WORK_PACKAGE_PLAN.md` requires
amendment, and its approval record requires reissue, because:

- **§2 surface `A`** lists `backend/services/data_fetcher.py` against sub-package
  `WP3.3` only;
- **Step 4.2** names `backend/main.py`, that call site only, as WP3.4's expected
  change;
- **Checkpoint C4's** expected repository state is "C3 state plus `main.py` (one
  call site), `test_fetch_history.py`, and the regression module(s)", which the
  accessor edit contradicts;
- **§5** defines no focused C3 delta review; and
- **§1, §6, and §7** bind the superseded planning corpus identity.

That amendment is **not performed by this act**. The Work Package Plan
operationalizes the frozen corpus and must be re-derived from the amended
corpus only after §8.1 steps 2 through 4 complete; drafting it now would
operationalize an unconfirmed, unfrozen candidate.

## 9. Verification performed

All values recomputed from live repository bytes, not transcribed.

### 9.1 Pre-amendment state

| Check | Result |
|---|---|
| Prior corpus per-file identity matched the frozen record | `SATISFIED` — `1F4E21FB…` / 40,882 bytes / 688 lines and `A6A4AB0A…` / 17,909 bytes / 430 lines |
| Prior aggregate identity reproduced | `SATISFIED` — `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A` |
| Manifest algorithm independently validated | `SATISFIED` — the recorded algorithm reproduces the recorded pre-amendment aggregate exactly |
| Cited surface facts 1–7 of §2 verified from live repository | `SATISFIED` |

### 9.2 Post-amendment state

| # | Amended artifact | Bytes (LF) | Lines | SHA-256 (LF) |
|---|---|---:|---:|---|
| 1 | `docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | 45,667 | 761 | `DF4630CFC00A32402B45489D1779F3BBAAD39A86630301256C541BC806481DD7` |
| 2 | `docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | 21,949 | 498 | `48BE744AD91367293FF790772A96FA49D60058CF0221080F538AE6FBEB3BAB01` |

Amended aggregate, under the canonical Git-canonical-LF convention and the
recorded manifest algorithm:

```text
3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D
```

Corpus cardinality: `2`, unchanged. Both artifacts contain zero `CR` bytes, so
raw and LF-normalized identities coincide, exactly as at the original freeze.

**This identity is a candidate, not a frozen identity.** It becomes binding only
at the Amended Planning Freeze of §8.1 step 3.

### 9.3 Boundary verification

| Check | Result |
|---|---|
| Exactly two planning artifacts amended | `SATISFIED` |
| Only additive edits; no existing text removed or reworded | `SATISFIED` |
| A1–A14 unchanged | `SATISFIED` |
| PD-1…PD-5, R7, Option C, provider neutrality unchanged | `SATISFIED` |
| Gate tables (Plan §10; Decomposition §6) unchanged | `SATISFIED` |
| Risk register R1–R11 unchanged | `SATISFIED` |
| Frozen WP1 canonicalizer byte-identical | `SATISFIED` — `59339DCBAF1BF7838BE0E472F562C9BCCACE0990598A564301F5F0BD3BE4560E`, 31,416 bytes, per-row raw convention of Planning Freeze Record §11.3 |
| No WP1 artifact changed by this act | `SATISFIED` |
| No WP2 artifact changed by this act | `SATISFIED` |
| No canonical design, roadmap, or implementation-sequence file changed | `SATISFIED` |
| No M46 file changed | `SATISFIED` |
| No production file changed **by this act** | `SATISFIED` |
| No test file changed **by this act** | `SATISFIED` |
| `git diff --check` | `PASS` — exit 0 |
| `git diff --cached --check` | `PASS` — exit 0 |
| No commit, stage, or push performed | `SATISFIED` |
| `graphify update .` | Not applicable — no source file changed by this act |

**Pre-existing working-tree state, disclosed and not caused by this act.**
`backend/main.py`, `backend/services/data_fetcher.py`,
`backend/services/market_data/yahoo_chart.py`,
`backend/tests/test_fetch_history.py`,
`backend/tests/test_yahoo_chart_provider.py`, and four untracked WP3 test and
module files carry the WP3.1–WP3.4 implementation performed under the existing
Implementation Authorization before this act. This act modified none of them.
The recursive `Permission denied` warnings `git status` emits for
`backend/.pytest-m32-3e3r2*` directories are pre-existing environmental noise
and affect no verification above.

## 10. Excluded effects

This record does **not**:

- perform implementation, or modify any implementation file;
- perform Planning Amendment Confirmation, Amended Planning Freeze, Allocation
  synchronization, Implementation Authorization synchronization, or Work Package
  Plan amendment or reapproval;
- perform any review, including the focused C3 delta review and C4 re-review;
- accept, reject, or dispose of any Checkpoint C4 finding other than by
  authorizing the surface the propagation-surface finding requires;
- reopen C1, C2, or accepted WP3.1, WP3.2, or WP3.3 semantics;
- create, amend, or satisfy any gate, including S8;
- create, amend, or discharge any acceptance criterion;
- resolve, weaken, or close any carried-forward residual, or the emitter-locus
  item referred out by PD-3;
- amend WP1, WP2, the canonical design, the roadmap, or the implementation
  sequence;
- alter WP4, WP5, WP6, WP7, or WP8 scope;
- create WP4 or later-package authority; or
- authorize any commit, push, deployment, or release.

## 11. Disposition

`BANPU-WP3 BOUNDED PLANNING AMENDMENT PREPARED — READY FOR INDEPENDENT REVIEW`

## 12. Exact next act

**Independent Bounded Planning Amendment Review** of amendment `BPA-1` and of
the amended planning corpus at candidate identity
`3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`.

This record performs no part of that act.
