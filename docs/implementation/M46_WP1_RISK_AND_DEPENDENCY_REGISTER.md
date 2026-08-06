# M46-WP1 — Risk and Open-Dependency Register

**Artifact class:** Authorized WP1 documentary implementation deliverable 6 of 6

**Authoring role:** M46-WP1 Implementation Author

**Authorization:** [M46-WP1 Authorization Record](M46_WP1_AUTHORIZATION_RECORD.md)

**Disposition:** `AUTHORED — BLOCKERS OPEN`

**Successor-package authority:** `NONE`

---

## 1. Purpose

This register consolidates the exact blockers, owner-supplied dependencies,
risks, and fail-closed controls carried by the other five WP1 deliverables. It
does not solicit, manufacture, repair, or approve external supply.

## 2. Blocking conditions

| Blocker ID | Condition | Evidence | Required competent resolution | Effect while open |
| --- | --- | --- | --- | --- |
| `BLK-01` | Six AF-WP1–AF-WP4 frozen outputs fail raw binary working-tree identity checks | [Baseline Register](M46_WP1_BASELINE_REGISTER.md) §5 | Authority competent to restore the recorded bytes or govern an additive successor lifecycle | WP1 intended-path output blocked; frozen artifacts untouched |
| `BLK-02` | Asset Foundation Domain Constitution is still marked draft pending ratification | [Alignment Disposition](M46_WP1_ALIGNMENT_RESIDUAL_DISPOSITION.md) §3 | Competent constitutional ratification | M46-G1 open; WP2–WP4 blocked |
| `BLK-03` | Corporate Action level-4 design retains superseded bridge-domain wording | Alignment Disposition §3 | Competent textual conformance or another frozen-plan-permitted closure route | M46-G1 open; WP2–WP4 blocked |
| `BLK-04` | No Asset Foundation successor-authoring authority exists after AF-WP4 closeout | [AF-WP4 Closeout](../governance/ASSET_FOUNDATION_AF_WP4_CLOSEOUT_RECORD.md) | New competent Asset Foundation governance act | WP2/WP3 blocked; WP4/WP6 transitively blocked |
| `BLK-05` | No Ledger successor-authoring authority exists | [Ledger Owner-Domain Final State](../governance/LEDGER_ACCOUNTING_OWNER_DOMAIN_FINAL_STATE.md) | New competent Ledger governance act | WP4 blocked; WP5 transitively blocked |
| `BLK-06` | No M46 candidate label has owner admission | [Vocabulary Register](M46_WP1_VOCABULARY_REGISTER.md) | Each semantic owner admits/rejects under future authority | No private dialect or runtime representation |
| `BLK-07` | Approved generic and BANPU fixtures are absent | [Acceptance-Vector Contract](M46_WP1_ACCEPTANCE_VECTOR_CONTRACT.md) §§3–6 | Exact owner-approved evidence and adjudication fixtures under later authority | Vector instances cannot execute; no terms inferred |
| `BLK-08` | Structural-event performance composition is absent | Frozen architecture §20.16 and current calculation rules | Ledger & Accounting plus Portfolio Intelligence governed contract | Affected authoritative performance `UNCOMPUTABLE` |
| `BLK-09` | Multi-denomination cash/FX expansion is ungoverned | Frozen architecture §20.12 | Separate Ledger/Portfolio governance and exact conversion evidence | Any vector needing it fails closed |
| `BLK-10` | Historical quote-basis policy and full binding contract are absent | Frozen architecture §20.11 | Market Intelligence/Portfolio Intelligence supply and future WP6 authority | Quote-dependent acceptance remains blocked |

No blocker releases a narrower unrecorded path. A blocked WP1 corpus is not
successor supply.

## 3. Dependency register

| Dependency ID | Required supply | Owner / competent act | Current state | Consumed by | Status |
| --- | --- | --- | --- | --- | --- |
| `DEP-01` | Exact frozen M46 planning pair | M46 Planning Freeze | Present and SHA-256 exact | All WP1 deliverables | `SATISFIED` |
| `DEP-02` | WP1 allocation | M46 Work-Package Allocation Authority | `ALLOCATED` | WP1 authorization/authorship | `SATISFIED` |
| `DEP-03` | WP1 documentary authorization | M46-WP1 Authorization Authority | `AUTHORIZED` | Six exact paths | `SATISFIED` |
| `DEP-04` | Exact AF-WP1 form and annex | Frozen AF-WP1 lifecycle | Present; raw bytes mismatch recorded identity | Baseline, inventory, later WP3 | `BLOCKED` |
| `DEP-05` | Exact AF-WP2 form and annex | Frozen AF-WP2 lifecycle | Present; raw bytes mismatch recorded identity | Baseline, inventory, currency boundary | `BLOCKED` |
| `DEP-06` | Exact AF-WP3 manifest/index | Frozen AF-WP3 lifecycle | Present; raw bytes mismatch recorded identity | Owner evidence inventory | `BLOCKED` |
| `DEP-07` | Exact AF-WP4 release profile | Frozen AF-WP4 lifecycle | Present; raw bytes mismatch recorded identity | Non-authority and release boundary | `BLOCKED` |
| `DEP-08` | Ratified Asset Foundation alignment and/or conformed level-4 text | Competent architecture governance | No qualifying supply found | M46-G1, WP2–WP4 | `OPEN` |
| `DEP-09` | Candidate vocabulary disposition | Each semantic owner | Owners identified; no admission acts found | WP2–WP6 contracts | `OPEN` |
| `DEP-10` | New Asset Foundation successor path | Competent owner-domain governance | `NONE` | WP2/WP3; WP4/WP6 transitively | `OPEN` |
| `DEP-11` | New Ledger successor path | Competent owner-domain governance | `NONE` | WP4; WP5 transitively | `OPEN` |
| `DEP-12` | Connectivity & Ingestion adjudication/admission/confirmation contract | Future WP2 under owner authority | WP2 unallocated/unauthorized | WP3/WP4 | `NOT AVAILABLE` |
| `DEP-13` | Asset identity consequences and effective identifiers | Future WP3 under owner authority | WP3 unallocated/unauthorized | WP4/WP6 | `NOT AVAILABLE` |
| `DEP-14` | Ledger structural Transaction and total-basis contract | Future WP4 under owner authority | WP4 unallocated/unauthorized | WP5/performance | `NOT AVAILABLE` |
| `DEP-15` | Governed performance-continuity composition | Ledger & Portfolio Intelligence | Absent | Performance vectors and downstream | `OPEN` |
| `DEP-16` | Quote identity/adjustment-basis contract | Market/Portfolio owners; future WP6 | WP6 unallocated/unauthorized | Valuation vectors/WP7 | `NOT AVAILABLE` |
| `DEP-17` | Migration/shadow authority and evidence | Future WP7 acts | WP7 unallocated/unauthorized | Migration vectors/WP8 | `NOT AVAILABLE` |
| `DEP-18` | Downstream regeneration and closeout authority | Future WP8 and closeout acts | WP8 unallocated/unauthorized | Downstream vectors/M46 closeout | `NOT AVAILABLE` |

## 4. Risk register

| Risk ID | Risk | Consequence | WP1 control | Blocking gate |
| --- | --- | --- | --- | --- |
| `RSK-01` | Symbol treated as identity | Wrong security, quantity, quote, P/L | Identity-negative vector; no current-symbol fallback | M46-G3 |
| `RSK-02` | Partial action lands | Registry/Ledger split brain | Both-or-neither vector and manifest completeness slot | M46-G2/G3 |
| `RSK-03` | Privileged action write path | Machine-created truth bypasses admission/human sovereignty | Confirmation vectors require exact policy/human evidence | M46-G2 |
| `RSK-04` | Alignment treated as absent or closed without evidence | Invalid owner contract and premature WP2–WP4 | Explicit `BLK-02`/`BLK-03`; no fresh owner decision | M46-G1 |
| `RSK-05` | Frozen predecessor byte mismatch ignored | Wrong corpus consumed as exact supply | `BLK-01`; raw and normalized identities kept distinct | WP1 exit |
| `RSK-06` | Closed Asset Foundation lifecycle reused | Unauthorized WP2/WP3 semantics | `BLK-04`; new successor act required | WP2/WP3 entry |
| `RSK-07` | Terminated Ledger lifecycle reused | Unauthorized accounting contract | `BLK-05`; new successor act required | WP4 entry |
| `RSK-08` | Average cost treated as primary state | Basis corruption through structural events | Vector contract requires total basis and derived average | M46-G4 |
| `RSK-09` | Double adjustment | Structural event applied in quantity and price | Raw/adjusted mismatch and exact-basis vectors | M46-G4 |
| `RSK-10` | Basis or residue guessed | Persistent accounting/P&L error | Exact instruction/closure fields; missing evidence blocks | M46-G3/G4 |
| `RSK-11` | Same-time order guessed | Wrong entitlement/conversion | Exact time-role and canonical-order slots | M46-G3/G4 |
| `RSK-12` | Provider taxonomy enters replay | Provider/action-specific branches | One-stream and future-story negative vectors | M46-G4 |
| `RSK-13` | Second corporate-action stream | Replay divergence | One canonical Transaction-stream invariant | M46-G4 |
| `RSK-14` | Structural event creates return | Phantom performance | Zero-return/`UNCOMPUTABLE` vectors and `BLK-08` | M46-G4 |
| `RSK-15` | Tax view becomes Ledger truth | Jurisdictional interpretation frozen universally | Basis instruction distinguishes platform book basis; owner evidence required | M46-G3 |
| `RSK-16` | Fractional residue disappears | Basis/value conservation drift | Exact fraction, quantization, and residue fields | M46-G3/G4 |
| `RSK-17` | Backfill rewrites history | Audit/replay invalidation | Immutability and additive-correction vector obligations | M46-G5 |
| `RSK-18` | Legacy parity preserves known defect | Wrong output becomes baseline | Predeclared affected differences and ADR-005 boundary | M46-G5 |
| `RSK-19` | Shadow output contaminates production | Unreviewed truth path | No-write, isolated-lineage, cohort, and rollback vectors | M46-G5/G6 |
| `RSK-20` | Stale downstream output appears current | Decisions consume obsolete state | Stale detection and exact-lineage regeneration vector | M46-G7 |
| `RSK-21` | Candidate vocabulary becomes private dialect | Conflicting canonical semantics | Every candidate term owner-mapped; admissions `NONE` | M46-G1 onward |
| `RSK-22` | Float arithmetic determines financial truth | Nondeterministic basis/residue | Exact-rational vector fields; current float gap recorded | M46-G3/G4 |
| `RSK-23` | Replay pressure promotes checkpoints to truth | Disposable state becomes authority | Full immutable stream remains authority in contract | M46-G4/G5 |
| `RSK-24` | BANPU facts inferred from symptoms | Issuer-specific correction/logic | All BANPU slots unfilled; no ratio, alias, term, or exception | Every gate |
| `RSK-25` | Calendar pressure bypasses evidence | Premature allocation/cutover | Evidence-released milestones only | Every gate |

## 5. Open architecture determinations preserved

| Open item | Named future owner/package | WP1 treatment |
| --- | --- | --- |
| Action identity/co-reference, timeline, and confirmation | WP2 / Asset Foundation and Connectivity & Ingestion | Deferred; only vector slots recorded |
| Identifier interval convention and runtime AF-1 interoperability | WP3 / Asset Foundation | Deferred; no representation chosen |
| Atomicity mechanism | Later technical design after WP2–WP4 contracts | Semantic requirement preserved; no mechanism selected |
| Canonical structural Transaction vocabulary | WP4 / Ledger & Accounting | Candidate labels not admitted |
| Book-basis method classes, entitlements, fractions, same-session order | WP4 and named owners | Exact evidence required; otherwise blocked |
| Historical quote basis and provider-series inventory | WP6 / Market Intelligence | Mismatch vectors locked; policy not invented |
| Multi-currency cash/FX | Separate Ledger/Portfolio governance | Fails closed |
| Scoped degraded valuation | Portfolio Intelligence | Failure slot preserved; product behavior not chosen |
| Structural-event performance composition | Ledger and Portfolio Intelligence | `UNCOMPUTABLE` until governed |
| BANPU containment or correction | Separate operational authority | Excluded from WP1 |

## 6. WP1 terminal state and handoff

The six authorized deliverables exist, are internally linked, and record the
full baseline, inventory, residual, vocabulary, vector, risk, and dependency
scope. WP1 nevertheless cannot claim intended-path completion because
`BLK-01`, `BLK-02`, and `BLK-03` are open. The result is truthful blocked
evidence and cannot release a successor package.

The next constitutional act after authorship is independent review of the
exact six-document WP1 corpus. Review may assess this blocked disposition; it
does not cure it by implication.

## 7. Non-authority statement

This register does not authorize or perform predecessor repair, vocabulary
admission, owner-domain supply, implementation code, tests, schemas, runtime
changes, migration, replay, accounting, quote selection, production
correction, allocation/authorization of WP2–WP8, release, freeze, or closeout.

**Terminal disposition: `AUTHORED — BLOCKERS OPEN; NOT SUCCESSOR SUPPLY`.**
