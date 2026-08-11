# BANPU-WP3 — Planning Amendment Confirmation `BPA-1`

**Artifact class:** Planning amendment confirmation record
**Confirmation date:** 2026-08-11
**Amendment identifier:** `BPA-1`
**Confirmation authority:** Independent Planning Amendment Confirmation Authority
**Pre-amendment corpus identity:** `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
**Confirmed amended corpus identity:** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Confirmation determination:** `BANPU-WP3 BPA-1 PLANNING AMENDMENT CONFIRMED`
**Implementation authority created by this act:** `NONE`

---

## 1. Independent-review verification

The completed independent bounded planning amendment review was independently
verified against the candidate corpus, its bounded amendment record, the
pre-amendment allocation boundary, and the live repository surface. Its
disposition is confirmed as:

```text
BOUNDED PLANNING AMENDMENT — APPROVED
BANPU-WP3 BPA-1 INDEPENDENTLY APPROVED
```

No `BLOCKING`, `MAJOR`, or unresolved `MINOR` finding remains that prevents
this confirmation. The preceding review did not authorize implementation,
freeze the candidate corpus, or accept the accessor delta.

## 2. Confirmed planning corpus

The amended planning corpus consists of exactly these two artifacts. This
confirmation record is not a member of that corpus.

| # | Artifact | Bytes | SHA-256 |
|---|---|---:|---|
| 1 | `docs/implementation/BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | 45,667 | `DF4630CFC00A32402B45489D1779F3BBAAD39A86630301256C541BC806481DD7` |
| 2 | `docs/implementation/BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | 21,949 | `48BE744AD91367293FF790772A96FA49D60058CF0221080F538AE6FBEB3BAB01` |

The canonical manifest is the two rows above, in the listed order, serialized
as `path<TAB>SHA-256<TAB>bytes<LF>` and SHA-256 hashed as UTF-8. Its aggregate
identity is:

```text
3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D
```

The recomputed values exactly match BPA-1's reviewed candidate identity. Both
planning artifacts have LF-only bytes; raw and canonical-LF identities are the
same.

## 3. Confirmed bounded amendment

BPA-1 changes only the WP3.4 allocation needed for the sole authorized
holdings-price call path in `backend/main.py` to consume
`resolve_successor_bindings(symbols)` from `backend/services/data_fetcher.py`.

The admitted surface is exactly one read-only accessor. It may expose requested,
non-ambiguous, already-constructed canonical `SuccessorQuoteBinding` values
from the accepted WP3.3 guard projection, solely to that holdings-price call
path. It creates no state, cache, policy, provider or registry lookup,
configuration read, evidence surface, binding construction, or additional
caller authority. Ambiguous and unavailable projection states remain absent and
therefore enter the existing fail-closed unbound refusal path.

The amendment does not alter PD-1 through PD-5, any existing risk disposition,
A1 through A14, WP3.1 or WP3.2 semantics, accepted pre-accessor WP3.3
semantics, WP1 or WP2, WP5 tolerance or reconciliation ownership, quarantine
taxonomy, general `data_fetcher.py` authority, or any consumer other than the
single authorized WP3.4 holdings-price path.

## 4. Amendment-record verification

[`BANPU_WP3_BOUNDED_PLANNING_AMENDMENT_RECORD.md`](BANPU_WP3_BOUNDED_PLANNING_AMENDMENT_RECORD.md)
accurately records BPA-1 as a candidate prepared for independent review. It
does not claim to perform confirmation, amended planning freeze, allocation
synchronization, implementation-authorization synchronization, Work Package
Plan reapproval, focused C3 delta acceptance, or C4 acceptance.

## 5. Acceptance and authority effect

- **C1 remains accepted.**
- **C2 remains accepted.**
- **C3 remains accepted for the pre-accessor WP3.3 state.** The accessor is a
  separately reviewable focused C3 delta after the successor governance chain
  authorizes it; no full C3 re-review is implied.
- **C4 remains incomplete.** It still requires focused C3 delta acceptance and
  exhaustive Step 4.1 eleven-site evidence before C4 re-review.

This confirmation creates **no implementation authority**. Existing allocation
and Implementation Authorization records bind the superseded pre-amendment
corpus and do not by themselves authorize reliance on BPA-1.

This act does **not** perform Amended Planning Freeze. Allocation and
Implementation Authorization synchronization remain outstanding. Work Package
Plan amendment and reapproval remain outstanding. Focused C3 accessor-delta
review remains outstanding.

## 6. Lifecycle boundary

The following successor acts remain separate and unperformed:

1. BANPU-WP3 Amended Planning Freeze.
2. Allocation synchronization.
3. Implementation Authorization synchronization.
4. Work Package Plan amendment and reapproval.
5. Focused C3 accessor-delta review.
6. Complete Step 4.1 evidence and return to C4.

No production or test file is modified by this confirmation. No commit, push,
deployment, release, allocation, authorization, Work Package Plan approval,
focused C3 review, or C4 review is performed here.

## 7. Exact next act

**BANPU-WP3 Amended Planning Freeze.**

This confirmation performs no part of that next act.
