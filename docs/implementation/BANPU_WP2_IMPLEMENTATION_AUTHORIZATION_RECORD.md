# BANPU-WP2 — Implementation Authorization Record

**Artifact class:** Additive constitutional authorization record
**Authorization date:** 2026-08-06
**Disposition:** `AUTHORIZED`
**Authorized work package:** `BANPU-WP2 — Replay and independent validator`
**Implementation authority created:** `LIMITED — see §10`
**WP3+ authority created:** `NONE`

## 1. Constitutional authority

Acting solely as the BANPU-WP2 Constitutional Authorization Authority, this
act authorizes implementation of the frozen and allocated BANPU-WP2 planning
corpus. Authority derives from the completed
[BANPU-WP2 Allocation Record](BANPU_WP2_ALLOCATION_RECORD.md) (`ALLOCATED`),
which itself derives from the
[BANPU-WP2 Planning Freeze Record](BANPU_WP2_PLANNING_FREEZE_RECORD.md)
(`PLANNING FROZEN WITH RECORDED OBSERVATIONS`), the
[BANPU-WP2 Planning Confirmation](BANPU_WP2_PLANNING_CONFIRMATION.md)
(`CONFIRMED WITH RECORDED OBSERVATIONS`), and the
[BANPU-WP2 Planning Freeze Readiness Assessment](BANPU_WP2_PLANNING_FREEZE_READINESS_ASSESSMENT.md)
(`READY FOR PLANNING FREEZE`).

This authority is limited to identity binding, corpus-boundary verification,
and creation of this authorization record. It grants no authority to
implement code itself (implementation remains a separate later act, §16), to
amend any frozen or allocated artifact, or to allocate or authorize WP3 or
any later package.

## 2. Authorization purpose

This record authorizes BANPU-WP2 implementation to begin, so that:

- the allocated planning target has an explicit, scoped, and bounded grant of
  implementation authority distinct from allocation itself;
- implementation work can proceed under a fixed set of preconditions, review
  gates, and carried-forward observations, with no ambiguity about what is
  and is not in scope; and
- no implementation of WP3, M46, or any file outside the frozen corpus can be
  inferred from this authorization.

## 3. Authorized work package

`BANPU-WP2 — Replay and independent validator`, exactly as defined in the
frozen planning corpus (Implementation Specification, Work Package Plan,
Implementation Sequence). This authorization does not change, narrow, or
widen that definition.

## 4. Authoritative allocated corpus

The authorized corpus is the exact 3-file candidate frozen and allocated,
unchanged since freeze and allocation:

| # | Frozen artifact | Bytes | Physical lines | SHA-256 |
|---|---|---:|---:|---|
| 1 | `docs/implementation/BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md` | 42,172 | 429 | `565EE81622AE01E452943801516BDC47400EC535FAF950C6601EEB50E01A53FA` |
| 2 | `docs/implementation/BANPU_WP2_WORK_PACKAGE_PLAN.md` | 18,300 | 222 | `9B11B25F87BC09A8A15D598492C32518F328DDFC770E519F86A2E960F61D06F0` |
| 3 | `docs/implementation/BANPU_WP2_IMPLEMENTATION_SEQUENCE.md` | 17,572 | 228 | `DED46B4CC06FE7EC2D9AF1E8992A8F96E4D8B410F4727DE77320B414010A6152` |

Aggregate corpus manifest identity (unchanged from Freeze Record §3 and
Allocation Record §4): `91F9295BBF71BC9FA50D8246893DA693189C8855D4B6F0E146822E36F76DFB5E`.

Corpus cardinality: `3`. No file in this table has been modified since
freeze or allocation.

## 5. Planning confirmation reference

[BANPU-WP2 Planning Confirmation](BANPU_WP2_PLANNING_CONFIRMATION.md) — 144
physical lines, 14,994 bytes, SHA-256
`8F3932A9C08B516A8D27567F089D41C7C1F1251C6EFF25F1142223B00161BFAA`.
Disposition: `CONFIRMED WITH RECORDED OBSERVATIONS`.

## 6. Planning freeze reference

[BANPU-WP2 Planning Freeze Record](BANPU_WP2_PLANNING_FREEZE_RECORD.md) —
disposition `PLANNING FROZEN WITH RECORDED OBSERVATIONS`; frozen corpus
identity and aggregate manifest hash reconfirmed unchanged in §4 above.

## 7. Allocation reference

[BANPU-WP2 Allocation Record](BANPU_WP2_ALLOCATION_RECORD.md) — disposition
`ALLOCATED`; allocated corpus identity reconfirmed unchanged in §4 above.
This authorization acts on that allocation; it does not re-perform or amend
it.

## 8. Implementation scope

This authorization grants implementation authority for, and only for:

- `backend/services/portfolio_rebuilder.py`
- `backend/services/ledger_validator.py`
- `backend/services/replay_key.py` — **only if** implementation evidence
  proves a pure conversion-key helper cannot remain package-local without
  changing existing `replay_key()` semantics (Work Package Plan §3.2).
  Default decision: do not modify. Any use of this conditional file requires
  an architecture review gate before the change, and its public signature and
  existing three-tier behavior must remain unchanged.

Corresponding test files identified by the frozen corpus
(`backend/tests/test_portfolio_rebuilder.py`,
`backend/tests/test_ledger_validator.py`,
`backend/tests/test_position_conversion_replay.py`,
`backend/tests/test_repair_validate_consistency.py`, and, only if
`replay_key.py` changes, `backend/tests/test_replay_key.py`) are authorized
as part of the same implementation act, since a code change without its
corresponding test coverage would violate the mandatory verification suites
in §14.

## 9. Prohibited scope

This authorization explicitly does **not** extend to:

- `BANPU-WP3` or any later package — no planning, allocation, or
  implementation of any kind;
- any planning amendment — the frozen Specification, Work Package Plan, or
  Implementation Sequence may not be edited under color of this record;
- production deployment of any kind;
- `M46` — which remains constitutionally independent and suspended;
- schema redesign — `backend/models/database.py` is frozen WP1 territory and
  is not reopened by this authorization;
- corporate-action expansion, or any feature beyond `POSITION_CONVERSION`
  replay/validation as scoped by the frozen corpus;
- any production file not named in §8.

## 10. Implementation authority granted

**Authorized:**

- implementation of BANPU-WP2 only;
- only within the frozen planning corpus identified in §4;
- only within the file scope in §8;
- only subject to all recorded observations (§15) and deferred findings
  (`MINOR-3`), none of which are waived by this act.

**Not authorized:**

- WP3 or later;
- planning amendments;
- production deployment;
- M46;
- schema redesign;
- corporate-action expansion.

This is a scoped grant, not a blanket implementation authority. Any work
outside §8 requires a separate, independently governed authorization act.

## 11. Successor authority

This authorization creates:

- `NO` BANPU-WP3 or later-package authority;
- `NO` authority to reopen or amend frozen BANPU-WP1, the frozen BANPU-WP2
  planning corpus, the Planning Confirmation, the Planning Freeze Record, or
  the Allocation Record;
- `NO` authority over M46, which remains constitutionally independent and
  suspended;
- `NO` authority to skip, waive, or shortcut the mandatory review gates in
  §14–§15.

## 12. Authorization disposition

**BANPU-WP2 implementation is `AUTHORIZED`**, scoped exactly as set out in
§8–§10. This authorization does not itself constitute implementation;
implementation remains a separate, later act (§16) subject to the
preconditions in §14. BANPU-WP1 remains frozen and unmodified. WP3 and later
packages remain unauthorized. M46 remains constitutionally independent and
suspended.

## 13. Implementation preconditions

Before any implementation act proceeds, the following preconditions apply,
in order:

1. Implementation must remain strictly inside the frozen scope in §8; any
   file not listed there requires a separate authorization.
2. Every mandatory verification suite defined by the planning corpus (Work
   Package Plan §6, reproduced in §14 below) must pass before implementation
   is considered complete.
3. Independent architecture review of the implementation must occur before
   confirmation.
4. Confirmation of the implementation must occur before any freeze.
5. Freeze of the implementation must occur before any successor allocation
   (i.e., before WP3 planning or allocation may begin).

## 14. Mandatory review gates

Per Work Package Plan §6, the following verification suites are mandatory
before implementation confirmation:

```text
pytest backend/tests/test_position_conversion_replay.py
pytest backend/tests/test_portfolio_rebuilder.py
pytest backend/tests/test_ledger_validator.py
pytest backend/tests/test_replay_key.py
pytest backend/tests/test_repair_validate_consistency.py
pytest backend/tests/test_ledger_validator_effective.py
pytest backend/tests/test_portfolio_rebuilder_capability_shadow.py
```

In addition, an independent architecture review of the implementation is
required before confirmation, and confirmation is required before freeze, per
§13 above.

## 15. Recorded observations carried forward

All six non-blocking observations and `MINOR-3`, carried forward unresolved
from the Planning Freeze Record §9, remain mandatory implementation-time
gates attached to this authorization. None is waived, resolved, or closed by
this act:

| ID | Disposition | Owner / gate |
|---|---|---|
| `OBSERVATION-1` | Non-blocking implementation-time fixture | WP2 validator implementation and independent review |
| `OBSERVATION-2` | Non-blocking implementation clarification | WP2 rebuilder implementation / materialization review |
| `OBSERVATION-3` | Non-blocking entry-gate clarification | WP2 Step 1 baseline record |
| `OBSERVATION-4` | Non-blocking interpretation note | WP2 validator implementation review |
| `OBSERVATION-5` | Non-blocking test-construction condition | WP2 rebuilder fixture implementation |
| `OBSERVATION-6` | Non-blocking governance interpretation | WP2 confirmation and future WP4/WP5 authorization review |

`MINOR-3` (deferred documentation synchronization) remains carried forward to
the separately approved WP8 documentation-correction gate and is not a WP2
authorization or implementation blocker.

## 16. Exact next constitutional act

The exact next authorized constitutional act is **BANPU-WP2 Implementation**,
performed strictly within the scope authorized in §8, subject to every
precondition in §13 and every review gate in §14, with all observations in
§15 carried forward unresolved. Implementation is itself a separate act from
this authorization and has not been performed by this record. Following
implementation, the standard lifecycle sequence (independent review →
confirmation → freeze) applies before any successor allocation, including
BANPU-WP3, may begin.

## 17. Repository verification

| Verification | Result |
|---|---|
| `BANPU_WP2_ALLOCATION_RECORD.md` exists | `SATISFIED` — present, disposition `ALLOCATED` |
| `BANPU_WP2_PLANNING_FREEZE_RECORD.md` exists | `SATISFIED` — present, disposition `PLANNING FROZEN WITH RECORDED OBSERVATIONS` |
| `BANPU_WP2_PLANNING_CONFIRMATION.md` exists | `SATISFIED` — present, disposition `CONFIRMED WITH RECORDED OBSERVATIONS` |
| `BANPU_WP2_PLANNING_FREEZE_READINESS_ASSESSMENT.md` exists | `SATISFIED` — present, disposition `READY FOR PLANNING FREEZE` |
| Allocated planning corpus unchanged | `SATISFIED` — §4 hashes identical to Freeze Record §3 and Allocation Record §4; no drift |
| Allocation references the same frozen corpus | `SATISFIED` — Allocation Record §4 corpus and manifest hash identical to Freeze Record §3 |
| All frozen WP1 hashes still match | `SATISFIED` — 12/12 recomputed and compared against `BANPU_WP1_FREEZE_RECORD.md` §4, exact match |
| No production implementation has begun | `SATISFIED` — `backend/services/portfolio_rebuilder.py`, `backend/services/ledger_validator.py`, `backend/services/replay_key.py` show no diff in `git status --short` |
| No production, schema, migration, test, or M46 file changed | `SATISFIED` — no untracked or modified file beyond the pre-existing staged WP1 corpus and the WP2 planning/confirmation/readiness/freeze/allocation/authorization docs |
| No WP3 artifact exists | `SATISFIED` — no `docs/implementation/BANPU_WP3*` file exists; unrelated `M38`–`M44_WP3_*` files belong to a separate, distinct program and are not BANPU-WP3 |
| `git diff --check` | `PASS` — exit 0 |
| `git diff --cached --check` | `PASS` — exit 0 |
| `git status --short` | Only the pre-existing staged WP1 corpus and the WP2 planning/confirmation/readiness/freeze/allocation/authorization docs are present; no other file differs |
| Graph synchronized | `graphify update .` run; code-graph rebuilt (documentation-only diff, no topology-affecting code change) |
| No commit created | `SATISFIED` — this act stages no commit |
