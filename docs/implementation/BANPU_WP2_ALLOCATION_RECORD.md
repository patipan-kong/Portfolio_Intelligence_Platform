# BANPU-WP2 — Allocation Record

**Artifact class:** Additive constitutional allocation record
**Allocation date:** 2026-08-06
**Disposition:** `ALLOCATED`
**Allocated work package:** `BANPU-WP2 — Replay and independent validator (planning only)`
**Implementation authority created:** `NONE`
**WP3+ authority created:** `NONE`

## 1. Constitutional authority

Acting solely as the BANPU-WP2 Constitutional Allocation Authority, this act
allocates the frozen BANPU-WP2 planning corpus identified in
[BANPU-WP2 Planning Freeze Record §3](BANPU_WP2_PLANNING_FREEZE_RECORD.md#3-frozen-planning-corpus)
(`PLANNING FROZEN WITH RECORDED OBSERVATIONS`), which itself derives from the
completed
[BANPU-WP2 Planning Confirmation](BANPU_WP2_PLANNING_CONFIRMATION.md)
(`CONFIRMED WITH RECORDED OBSERVATIONS`) and the completed
[BANPU-WP2 Planning Freeze Readiness Assessment](BANPU_WP2_PLANNING_FREEZE_READINESS_ASSESSMENT.md)
(`READY FOR PLANNING FREEZE`).

This authority is limited to identity binding, corpus-boundary verification,
and creation of this allocation record. It grants no authority to implement,
authorize implementation, or allocate WP3 or any later package.

## 2. Allocation purpose

This record allocates the frozen BANPU-WP2 planning corpus to the
implementation lifecycle stage, so that:

- the fixed, byte-identified planning target frozen in the Planning Freeze
  Record has a recorded allocation event distinct from, and prior to, any
  future WP2 implementation authorization;
- a separately governed **BANPU-WP2 Implementation Authorization** act (the
  next constitutional act, §12) has an explicit allocation record to act
  against, per Work Package Plan Gate 1; and
- no implementation, authorization, or successor-package act can be inferred
  from this allocation alone.

## 3. Allocated work package

`BANPU-WP2 — Replay and independent validator (planning only)`, scoped to
`backend/services/portfolio_rebuilder.py` and
`backend/services/ledger_validator.py`, with `backend/services/replay_key.py`
conditionally in scope, exactly as defined in the frozen planning corpus.
Allocation does not change, narrow, or widen this scope.

## 4. Authoritative planning corpus

The allocated corpus is the exact 3-file candidate frozen by the Planning
Freeze Record, unchanged since freeze:

| # | Frozen artifact | Bytes | Physical lines | SHA-256 |
|---|---|---:|---:|---|
| 1 | `docs/implementation/BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md` | 42,172 | 429 | `565EE81622AE01E452943801516BDC47400EC535FAF950C6601EEB50E01A53FA` |
| 2 | `docs/implementation/BANPU_WP2_WORK_PACKAGE_PLAN.md` | 18,300 | 222 | `9B11B25F87BC09A8A15D598492C32518F328DDFC770E519F86A2E960F61D06F0` |
| 3 | `docs/implementation/BANPU_WP2_IMPLEMENTATION_SEQUENCE.md` | 17,572 | 228 | `DED46B4CC06FE7EC2D9AF1E8992A8F96E4D8B410F4727DE77320B414010A6152` |

Aggregate corpus manifest identity (unchanged from Freeze Record §3):
`91F9295BBF71BC9FA50D8246893DA693189C8855D4B6F0E146822E36F76DFB5E`.

Corpus cardinality: `3`. No file in this table has been modified, and no
fourth file has been added to the allocated corpus.

## 5. Planning confirmation reference

[BANPU-WP2 Planning Confirmation](BANPU_WP2_PLANNING_CONFIRMATION.md) — 144
physical lines, 14,994 bytes, SHA-256
`8F3932A9C08B516A8D27567F089D41C7C1F1251C6EFF25F1142223B00161BFAA`.
Disposition: `CONFIRMED WITH RECORDED OBSERVATIONS`.

## 6. Planning freeze reference

[BANPU-WP2 Planning Freeze Record](BANPU_WP2_PLANNING_FREEZE_RECORD.md) —
disposition `PLANNING FROZEN WITH RECORDED OBSERVATIONS`; frozen corpus
identity and aggregate manifest hash both reconfirmed unchanged in §4 above.
[BANPU-WP2 Planning Freeze Readiness Assessment](BANPU_WP2_PLANNING_FREEZE_READINESS_ASSESSMENT.md) —
disposition `READY FOR PLANNING FREEZE`, cited as pre-freeze evidence only.

## 7. Scope allocated

This act allocates only:

- the frozen 3-file planning corpus identified in §4, as the fixed target for
  a future, separately governed WP2 implementation authorization act; and
- the six recorded non-blocking observations and `MINOR-3`, carried forward
  unresolved from the Planning Freeze Record §9, as mandatory
  implementation-time gates attached to that future authorization.

## 8. Excluded scope

This act does not:

- authorize BANPU-WP2 implementation, or begin, plan, or authorize BANPU-WP3
  or any later package;
- implement, modify, or scaffold any replay, validator, rebuilder, migration,
  schema, production, or test code;
- resolve, close, or waive any of the six recorded observations or `MINOR-3`;
- amend, reopen, or reinterpret the frozen BANPU-WP2 planning corpus or the
  frozen BANPU-WP1 corpus;
- change, reopen, or synchronize M46, which remains constitutionally
  independent and suspended;
- commit, push, deploy, migrate, or mutate production data.

## 9. Implementation prohibition

BANPU-WP2 implementation is **not authorized** by this allocation. Allocating
the frozen planning corpus identifies it as the target for a future
authorization act; it does not itself grant that authorization. No
production, schema, migration, or test file may be changed under color of
this record. `backend/services/portfolio_rebuilder.py` and
`backend/services/ledger_validator.py` remain unmodified and unauthorized for
modification.

## 10. Successor authority

This allocation creates:

- `NO` BANPU-WP2 implementation authority;
- `NO` BANPU-WP3 or later-package authority;
- `NO` authority to reopen or amend frozen BANPU-WP1 or the frozen BANPU-WP2
  planning corpus;
- `NO` authority over M46, which remains constitutionally independent and
  suspended.

The only effect of this record is to mark the frozen corpus in §4 as
allocated and to identify it as the fixed target for a separately governed
BANPU-WP2 Implementation Authorization act.

## 11. Allocation disposition

**BANPU-WP2 is `ALLOCATED`** at the frozen corpus identity in §4.

Implementation is **NOT** authorized. Authorization must occur separately, as
a distinct constitutional act performed by a distinct authorization
authority, consistent with Work Package Plan Gate 1. BANPU-WP1 remains frozen
and unmodified. WP3 and later packages remain unauthorized. M46 remains
constitutionally independent and suspended.

## 12. Exact next constitutional act

The exact next authorized constitutional act is **BANPU-WP2 Implementation
Authorization**, performed by a distinct authorization authority, over the
exact allocated candidate identified in §4. That act, if granted, would be the
first act permitted to authorize changes to
`backend/services/portfolio_rebuilder.py` and
`backend/services/ledger_validator.py` (and conditionally
`backend/services/replay_key.py`) — no such change may occur before it.
Implementation itself remains a separate, later act even after authorization.
WP3 and later packages remain unauthorized until their own independently
governed sequence completes.

## 13. Repository verification

| Verification | Result |
|---|---|
| Planning Freeze Record exists | `SATISFIED` — `BANPU_WP2_PLANNING_FREEZE_RECORD.md` present, disposition `PLANNING FROZEN WITH RECORDED OBSERVATIONS` |
| Planning Confirmation exists | `SATISFIED` — `BANPU_WP2_PLANNING_CONFIRMATION.md` present, disposition `CONFIRMED WITH RECORDED OBSERVATIONS` |
| Planning Freeze Readiness exists | `SATISFIED` — `BANPU_WP2_PLANNING_FREEZE_READINESS_ASSESSMENT.md` present, disposition `READY FOR PLANNING FREEZE` |
| Frozen planning corpus internally consistent | `SATISFIED` — §4 hashes identical to Freeze Record §3, Confirmation §2, and Freeze Readiness §3; no drift |
| WP1 remains frozen | `SATISFIED` — no diff against any of the 12 frozen WP1 corpus files; all remain staged exactly as at WP1 freeze |
| No implementation has begun | `SATISFIED` — `backend/services/portfolio_rebuilder.py` and `backend/services/ledger_validator.py` show no diff in `git status --short` |
| No production code changed | `SATISFIED` — no untracked or modified production file beyond the pre-existing staged WP1 corpus |
| No schema, migration, or test changes | `SATISFIED` — `backend/models/database.py`, the WP1 migration, and both WP1 test files remain in their pre-existing staged state; no WP2 test or migration file exists |
| No successor work package has begun | `SATISFIED` — no `docs/implementation/BANPU_WP3*` or later-package file exists; no M46 file appears in `git status` |
| `git diff --check` | `PASS` — exit 0 |
| `git status --short` | Only the pre-existing staged WP1 corpus and the WP2 planning/confirmation/readiness/freeze/allocation docs are present; no other file differs |
| Graph synchronized | `graphify update .` run; code-graph rebuilt (documentation-only diff, no topology-affecting code change) |
| No commit created | `SATISFIED` — this act stages no commit |