# M44-WP1 — Roadmap and Current-State Reconciliation

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics Foundation

**Work package:** M44-WP1 only

**Artifact class:** Constitutional current-state evidence and reconciliation

**Status:** `RC1 — REQUIRES INDEPENDENT CONSTITUTIONAL REVIEW AND CONFIRMATION`

**Reconciliation date:** 2026-07-29

**Companion artifact:** [M44-WP1 Inherited Gate Inventory and Closure Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)

**Governing frozen authority:** [M44 Architecture and Implementation Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
(RC2), `COMPLETE AND FROZEN` per [M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md) §9

**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/schema/migration authority:** `NONE`
**API/transport authority:** `NONE`
**UI/presentation authority:** `NONE`
**Implementation authority:** `NONE`
**Provider authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`
**Capability-completion authority:** `NONE`
**Frozen-artifact-amendment authority:** `NONE`
**Gate-disposition authority:** `NONE`
**Ownership-determination authority:** `NONE`
**Vocabulary-admission authority:** `NONE`
**Encoding-selection authority:** `NONE`

---

## 0. Executive determination

This artifact is the second of the two architectural deliverables that frozen
[M44 RC2](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §11 allocates to
M44-WP1, filed at the exact path frozen RC2 §11 and §13.1 declare. It carries
four things and nothing else:

1. the **roadmap reconciliation** — M44 marks no capability complete (§2);
2. the **current-state inventory** of the governance corpus M44 inherits, as
   verified in the repository at the reconciliation date (§3, §4);
3. the **M44 negative corpus** — the statements that are invalid in every M44
   artifact and in every downstream reliance on M44-WP1 (§5); and
4. the **nested-coordinate encoding-obligation pre-inventory** feeding
   M44-WP4, which frozen RC2 §17 `OQ-1` names as "the deciding evidence"
   (§6).

**It dispositions nothing.** It closes no gate, determines no owner, selects
no encoding, admits no noun, and grants no work package permission to begin.
Where the evidence it records bears on a determination, the determination is
named and referred to the frozen authority that holds it, and the referral is
recorded as a referral rather than performed as a decision.

This artifact carries forward the authorization precondition recorded at
companion register §3, with one component's state changed by verified
repository evidence:

- **`P-1` — filing remediation** required by frozen
  [Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md) §2.1. **Satisfied.**
  Verified at §3.1 on 2026-07-29: all four review-chain artifacts now resolve
  at the `M44_ARCHITECTURE_*` paths frozen RC2 §1.1, §13.1, and §16.1 declare.
  The register recorded this as unperformed at its own authoring; the change is
  recorded as a supersession at §7.2, not as an edit to the register.
- **`P-2` — independent confirmation of M44-WP1.** Not recorded. Outstanding
  (§7.3).

Until `P-2` holds, this artifact and its companion remain `NON-EFFECTIVE` on
exactly the terms the register states. Nothing here is a re-decision of that
precondition; §3.1 records only what the repository now contains.

---

## 1. Controlling authority and scope

### 1.1 What this artifact implements

Frozen RC2 §11, M44-WP1, **Included scope**, in its own words: "Gate inventory
with exact path and section citations; gate-to-work-package mapping; roadmap
and current-state reconciliation for M44; vocabulary-sufficiency finding; M44
negative corpus; nested-coordinate encoding-obligation pre-inventory feeding
WP4."

The first two items are discharged by the companion register (§4–§7 there).
The vocabulary-sufficiency finding for the work package is recorded at register
§11 and extended to this artifact at §7.4 below. The remaining three items —
roadmap and current-state reconciliation, the M44 negative corpus, and the
nested-coordinate pre-inventory — are discharged here.

The two artifacts are one work package and are read together. Neither is
complete without the other, and neither may be cited as if it stood alone.

### 1.2 Governing baseline

In the precedence order recorded at companion register §2:

1. the Platform Architecture Laws and governance rules G1–G6, and the domain
   allocations of `platform_architecture.md` §§6.2–6.9;
2. the Domain Constitutions and
   [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md);
3. `ADR-001` through `ADR-005`;
4. frozen M34 decisions, frozen M36, frozen M39, frozen M40–M41, and the
   frozen M42 corpus;
5. the frozen M43 corpus, including the M43 Epic Closeout;
6. frozen [M44 RC2](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) and the
   [M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md); and
7. this work package's own two artifacts, which are subordinate to every level
   above and add nothing to any of them.

### 1.3 Explicit non-authority

This artifact does not, and may not be read to:

- close, release, defer, re-scope, or otherwise disposition any inherited gate;
- determine or imply the owner of any semantic concern, including the
  annualization basis and the period-return rule;
- select, prescribe, name, or constrain any byte encoding, character encoding,
  delimiter, container syntax, field order, identifier format, or schema, for
  the Portfolio Composition or for any coordinate inside it;
- author, name, imply, register, extend, version, or serialize a governed
  contract kind, in Portfolio Intelligence's corpus or in any other domain's;
- admit, rename, retire, or re-scope any constitutional noun;
- amend, correct, restate, supersede, or re-file any frozen artifact;
- mark any roadmap capability complete, partially complete, or in progress;
- authorize any work package, including M44-WP1's own review chain, to begin;
  or
- assert that any legacy behavior it inventories is preserved, adapted,
  deprecated, blessed, or condemned.

Under constitution G6, every statement of current runtime reality below is
evidence of what *is*. None is precedent, admission, compatibility promise, or
permission.

---

## 2. Roadmap reconciliation

### 2.1 The frozen instruction

Frozen RC2 §13.3 states the roadmap effect of the whole milestone in one line:
"`docs/architecture/ROADMAP.md`: `NONE` — no capability-completion mark."

M44 is a documentary governance milestone. Its entire authority is documentary
(frozen RC2 §5, §13.3). It deploys nothing, computes nothing, and exposes
nothing. No capability moves.

### 2.2 Position of M44

M44 is the gate-closure and normative-semantics bridge between the frozen M43
contract corpus and any future, separately authorized executable Portfolio
Analytics milestone:

```text
M39 Market Observation
        +
M40–M41 Market Measure
        +
M42 Portfolio Composition
        ↓
M43 non-production Portfolio Analytics contracts
        ↓
M44 inherited-gate closure + the two universal normative specifications
        ↓
(a later, separately authorized milestone — no number is assigned)
```

The last row carries no milestone number by force of frozen RC2 §4.5 and §17
`OQ-4`, recorded as deferred-with-owner-unassigned at companion register §5.4.

### 2.3 Capability findings

`docs/architecture/ROADMAP.md` §"Portfolio Intelligence" lists four
capabilities. None is touched.

| Roadmap capability | M44-WP1 finding | Consequence |
| --- | --- | --- |
| Rolling Analytics — rolling return, Sharpe, volatility | M44 may supply the two universal normative specifications if the §12.1.1 checkpoint permits; a normative specification is not a method, an implementation, an endpoint, or a deployment | No capability-completion mark |
| Advanced Risk Metrics — including Sortino | Every annualized method remains blocked on `G-4`, which frozen RC2 §12.3 expressly records as a *non-blocking* `OPEN` outcome for sequencing but a blocking one for the method itself | No capability-completion mark |
| Position Attribution | Untouched by M44; contribution and attribution methods remain outside the frozen M43 and M44 surfaces | No capability-completion mark |
| Sector Attribution Timeline | Untouched by M44; no grouping choice, method, or timeline contract enters | No capability-completion mark |

Two further roadmap-adjacent findings, recorded so that no reader infers
progress that has not occurred:

| Concern | Finding |
| --- | --- |
| M42 Portfolio Composition | Remains the only permitted governed Portfolio subject. `G-3` leaves its canonical-byte obligation undischarged; a subject that cannot be formed is not a capability that has regressed, it is an obligation that has not yet been met (frozen M43-WP3 §7.1) |
| Future executable analytics | Remains a successor-milestone concern with no number, no owner, and no schedule (frozen RC2 §4.5, `D-4`) |

`docs/architecture/ROADMAP.md` is not modified by this artifact, and frozen RC2
§13.2 reserves every governance-record synchronization to a single separately
authorized act at epic closeout.

---

## 3. Current-state governance inventory

This section inventories the state of the **governance corpus** as verified in
the repository on 2026-07-29. It is the current-state evidence M44-WP1 is
allocated to produce. Absence claims are verified by directory enumeration, not
inferred; the enumeration is recorded at companion register §9.5 and is not
repeated here.

### 3.1 M44 corpus

| Path | State | Bearing |
| --- | --- | --- |
| [M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | Present; RC2; `COMPLETE AND FROZEN` | The canonical authority for this work package |
| [M44_ARCHITECTURE_FREEZE_RECORD.md](M44_ARCHITECTURE_FREEZE_RECORD.md) | Present | Records the freeze, the open milestone state, and the §2.1 filing divergence |
| [M44_ARCHITECTURE_INDEPENDENT_REVIEW.md](M44_ARCHITECTURE_INDEPENDENT_REVIEW.md) | Present at the frozen-declared path | `P-1` satisfied |
| [M44_ARCHITECTURE_FORMAL_CONSTITUTIONAL_RESPONSE.md](M44_ARCHITECTURE_FORMAL_CONSTITUTIONAL_RESPONSE.md) | Present at the frozen-declared path | `P-1` satisfied |
| [M44_ARCHITECTURE_CONSTITUTIONAL_ADJUDICATION.md](M44_ARCHITECTURE_CONSTITUTIONAL_ADJUDICATION.md) | Present at the frozen-declared path | `P-1` satisfied |
| [M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md](M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md) | Present at the frozen-declared path; Findings 1–6 `PASS`; `APPROVED FOR FREEZE`; unresolved findings `NONE` | Frozen RC2 §1.1 now resolves |
| `M44_INDEPENDENT_CONSTITUTIONAL_REVIEW.md`, `M44_FORMAL_CONSTITUTIONAL_RESPONSE.md`, `M44_CONSTITUTIONAL_ADJUDICATION.md`, `M44_INDEPENDENT_CONFIRMATION.md` | **Absent** — the four non-conforming filings no longer exist | The remediation was performed by rename, as frozen Freeze Record §2.1 requires |
| M44-WP2 through M44-WP7 deliverables | **Absent** | Not started; frozen RC2 §12.5 point 2 makes M44-WP1's confirmation the gate before any of them |
| `M44_EPIC_CLOSEOUT.md` | **Absent** | Milestone open |

**Filing remediation — verified performed.** Frozen
[Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md) §2.1 recorded a filing
divergence and stated its consequence in terms this artifact may not soften:
"**Until that rename is performed, no M44 work package is authorized to begin
under frozen RC2 §1.1.**" The remedy it prescribed — "to rename the four filings
to the paths the frozen architecture declares" — has been performed. Verified by
directory enumeration on 2026-07-29: the four `M44_ARCHITECTURE_*` paths exist
and the four superseded paths do not. Frozen RC2 §1.1 therefore resolves, and
`P-1` is satisfied.

Two review notes are recorded, neither acted on here:

1. The remediation was performed outside M44-WP1 and is not this work package's
   act. M44-WP1 neither authorized nor performed it, and claims no credit for
   it; it is recorded as current-state evidence under constitution G6.
2. Frozen Freeze Record §2 still tabulates the four superseded filing paths,
   which no longer resolve. That is the expected residue of a rename the record
   itself demanded, and correcting it — if a confirming reviewer holds it should
   be corrected — is a governance act outside M44-WP1's authority. No frozen
   artifact is edited by this work package.

### 3.2 M43 corpus

| Path or statement | Verified state | Bearing |
| --- | --- | --- |
| [M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) line 3 | Reads `Proposed status: READY FOR INDEPENDENT ARCHITECTURE CONFIRMATION` | `G-1` evidence |
| [INDEX.md](INDEX.md) §current status | States M43 Architecture and M43-WP1 through M43-WP8 are `COMPLETE`, reviews `CONFIRMED`, unresolved findings `NONE` | The divergence `G-1` names; reconciliation is M44-WP2's, not this artifact's |
| `M43_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` or any repository-local M43 architecture confirmation record | **Absent** | `G-1` remains open on absence, not on disagreement |
| [M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §8, canonical period-return rule row | Reads `OWNER TO PROVE AT WP1`; "WP6 is blocked until disposition; no second rule is permitted" | `G-2` evidence |
| [M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §7.4 | Standing block `M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6`; four-step correction path; "Until steps 1–3 are complete, WP6 may not begin." | `G-2` evidence; frozen RC2 §17 `OQ-5` concerns step 4 only |
| [M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md) §7.1 | "a conforming subject cannot be formed"; WP3 "does not cure the gap" | `G-3` evidence; the governing test in §6 below |
| [M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md](M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md) §6.3 | "this mandatory entry—and therefore a concrete manifest—cannot yet be formed" | `G-3` propagation |
| [M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §6.7 | "The frozen corpus presently supplies no such annualization contract kind"; WP4 "MUST NOT author, name, imply, or serialize a new governed dependency contract" | `G-4` evidence |
| `M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md` | **Absent** | `G-5`, first half |
| `M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md` | **Absent** | `G-5`, second half |
| [M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md](M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §3.2 | "Neither specification is present in the current repository corpus" | `G-5` evidence |
| [M43_WP8_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md](M43_WP8_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §4 | "Normative WP8 method work: BLOCKED PENDING INHERITED GATE CLOSURE" | Recorded blockage, not a closure |
| [M43_EPIC_CLOSEOUT.md](M43_EPIC_CLOSEOUT.md) §1 | "This closeout does not close an inherited gate and grants no additional authority." | The closeout is not a gate discharge |
| M43-WP9 | Allocated by frozen M43 §9; never produced | `D-4`, deferred-with-owner-unassigned (register §5.4) |

No frozen M43 artifact is modified, corrected, or re-filed by this work package.

### 3.3 M42 corpus — the coordinate-owning contracts

Every contract that owns a Portfolio Composition coordinate exists and is
frozen. What each does **not** carry is the material fact for §6.

| Owning contract | Coordinates supplied | Declared serialization authority |
| --- | --- | --- |
| [M42_WP2_...CONTRACT_SPECIFICATION.md](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md) | Portfolio Identity, Accounting Scope, Portfolio Membership, Portfolio Base Currency | No serialization surface; §6.2 expressly declines to mint a currency-identifier format |
| [M42_WP3_STAGE_B_...CONTRACT_SPECIFICATION.md](M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md) | Investment Universe declaration | `Serialization authority: NONE` (header); §5.3 "deliberately defines no identifier syntax" |
| [M42_WP5_...CONTRACT_SPECIFICATION.md](M42_WP5_PORTFOLIO_BENCHMARK_DECLARATION_CONTRACT_SPECIFICATION.md) | Portfolio Benchmark Declaration | `Serialization authority: NONE` (header); §4.4 reuses the frozen `asset_id` citation format without inventing one |
| [M42_WP6_...CONTRACT_SPECIFICATION.md](M42_WP6_PORTFOLIO_LIFECYCLE_STATE_REUSE_AND_PROVENANCE_CONTRACT_SPECIFICATION.md) | Portfolio Lifecycle State; Provenance carriage | `Serialization authority: NONE` (header); §4.2 "not a prescribed object, tuple, record, schema, payload, field list, or wire format" |
| [M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md) | The composition container | §5 fixes the tag and the ten-element order; "defines no byte or character encoding, delimiter, escaping, container syntax, transport, serialization library, or persistence form"; "Their exclusion does not remove or defer the frozen canonical-byte obligation" |

This is the frozen shape of `G-3`: the obligation is preserved and undischarged
by design, and no owning contract has since discharged it.

### 3.4 Repository governance records

| Record | Current state relative to M44 | Required treatment |
| --- | --- | --- |
| [DECISION_LOG.md](../engineering/DECISION_LOG.md) | Contains no M44 entry | One consolidated entry at epic closeout, separately authorized (frozen RC2 §13.2) |
| [INDEX.md](INDEX.md) | Names M43 as the latest completed milestone; no M44 row | M44 row and status paragraph at epic closeout, separately authorized |
| [GLOSSARY.md](../GLOSSARY.md) | Unchanged; no M44 term | Modified only if a vocabulary gate confirms an admission or rename; M44-WP1 requires none (register §11, §7.4 below) |
| [ROADMAP.md](../architecture/ROADMAP.md) | Unchanged | `NONE` under frozen RC2 §13.3 |

None of the four is modified by this work package. Recording their current state
is not a licence to synchronize them.

### 3.5 Legacy runtime current state

Frozen RC2 §13.4 names the legacy modules and consumers M44 describes but does
not modify, and routes their inventory to frozen
[M43-WP1 Reconciliation](M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
§§3.1–3.5. That inventory covers accounting-derived period evidence, duplicate
analytics rules, defaults and fallbacks, caches and persistence, and APIs and
consumers.

**M44-WP1 re-inventories none of it and changes none of its dispositions.** The
frozen M43-WP1 inventory is consumed by citation. Three consequences are
recorded because M44's specific work touches the same subject matter:

| Legacy fact (frozen M43-WP1 §3.3) | Its relevance to M44 | M44 treatment |
| --- | --- | --- |
| `quant_engine.py` uses `252` and `sqrt(252)` | These are the annualization bases `G-4` concerns | `REJECT AS PRECEDENT`, unchanged. Their existence is not the governed dependency frozen M43-WP2 §8.1 requires, and M44-WP5 may not derive an owner, a basis, or a contract kind from them |
| `calculate_sharpe_ratio(..., risk_free_rate=0.025)` | Adjacent to the Component F risk-free evidence requirement (frozen M43-WP4 §6.6) | `REJECT AS PRECEDENT`, unchanged. Outside M44's allocated gates entirely |
| `PortfolioSnapshot` persists NAV and period-return fields | Adjacent to `G-2` and to any future Portfolio Measure Result | `LEGACY EVIDENCE`, unchanged. Frozen RC2 INV-M1 and INV-M2 forbid reclassifying any stored record; no migration, backfill, or repair authority enters M44 |

No source file, endpoint, schema, migration, scheduler, cache, or frontend
component is created, modified, deprecated, renamed, or blessed by M44-WP1.

---

## 4. Legacy-to-canonical disposition

Frozen [M43-WP1 Reconciliation](M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
§4 carries the legacy-to-canonical disposition matrix. **M44 changes no row of
it, adds no row to it, and softens no row of it.** It is consumed by citation
and remains in force verbatim.

The only dispositions this artifact records are the three governance-surface
statements below, which concern M44's own artifacts rather than legacy code:

| Surface | M44-WP1 disposition | Reason |
| --- | --- | --- |
| The documentary specimens in frozen M42 and M43 vector tables — `PI-01`, `AS-01`, `MI-BENCH-02`, and every similar label | `REJECT` as an identifier format, value domain, or encoding precedent | The vector-table preambles of frozen M42-WP3 Stage B, M42-WP5, and M42-WP6 each state that the vectors are documentary examples and are not serialized records. Frozen RC2 §15 R-8 forbids fixtures becoming de facto semantics; frozen M43-WP7 §11.3 forbids reverse-authoring rules from vectors |
| The file forecast at frozen RC2 §13.1 | `REJECT` as authorization | A forecast names a path; it does not authorize the work package that would produce it. Frozen M43-WP7 §3.1: "A plan, expected filename, or unchanged prerequisite is not a substitute for an existing independently confirmed normative specification" |
| A recorded blockage — frozen M43-WP8 §4, frozen M43-WP1 §7.4, frozen M43-WP6 §3.2 | `REJECT` as a closure | Frozen RC2 §16.2 admits exactly one closure state, `CLOSED`; R-14 names blockage-as-closure as the defect the terminal-state vocabulary exists to prevent |

---

## 5. Negative corpus

### 5.1 Carried forward

The twenty-three statements at frozen
[M43-WP1 Reconciliation](M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md) §5
are invalid "in every WP1 artifact and in every downstream reliance on WP1."
M44 is downstream reliance. They are therefore in force across the whole M44
corpus, are consumed by citation, and are **not** restated, renumbered,
paraphrased, narrowed, or extended here. Frozen RC2 §14 makes the whole-corpus
scan against them a required regression check.

### 5.2 The M44 negative corpus

The following statements are additionally invalid in every M44 artifact and in
every downstream reliance on M44-WP1. Each is traceable to a frozen sentence,
named in the second column.

| # | Invalid statement | Frozen basis |
| --- | --- | --- |
| `M44-N-01` | "An entry in the M44-WP1 register closes, releases, or discharges a gate." | RC2 §8.7 C0 — "Evidence and navigation only. It closes nothing." |
| `M44-N-02` | "`OPEN — PARTIAL`, `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`, or `DEFERRED` is a closure." | RC2 §16.2 — `CLOSED` is the only closure |
| `M44-N-03` | "A recorded blockage, a routing record, a requirement specification, or a successor obligation discharges an inherited gate." | RC2 §16.2, R-14; M43 Epic Closeout §1 |
| `M44-N-04` | "M44 may author, name, imply, register, extend, version, or serialize a governed contract kind in a domain other than Portfolio Intelligence." | RC2 INV-C4, §11 M44-WP5, §13.1; M43-WP4 §5.2 |
| `M44-N-05` | "The frozen RC2 §13.1 file forecast authorizes the work package that would produce the forecast file." | RC2 §13 preamble — "Forecast only"; M43-WP7 §3.1 |
| `M44-N-06` | "A documentary vector, specimen label, or fixture establishes an identifier format, a value domain, a field order, or an encoding." | RC2 §15 R-8; M43-WP7 §11.3; the M42 vector-table preambles |
| `M44-N-07` | "M44-WP4 may encode a source-owned nested coordinate whose owner has not supplied its exact form." | M42-WP7 §9 checklist item 11 — "No source-owned nested coordinate is reordered, normalized, encoded, or reinterpreted"; PC-NGV-14 |
| `M44-N-08` | "M44 may supply, complete, default, infer, normalize, or repair a coordinate reference on an absent owner's behalf." | M42-WP7 §3 — "An unsupplied coordinate is missing, not a value or authority to complete the composition"; §4.2; PC-NGV-04 |
| `M44-N-09` | "Routing an unsupplied coordinate to its owner discharges the canonical-byte obligation." | RC2 §3.1 — "Routing an unsupplied coordinate to its owner records the obligation; it does not discharge it" |
| `M44-N-10` | "The M43 Epic Closeout, the Implementation INDEX, or the M43 Decision Log entry closed an inherited gate." | M43 Epic Closeout §1 |
| `M44-N-11` | "The M43 plan's own proposed-status line is, or substitutes for, the repository-local M43 architecture confirmation record." | M43-WP1 §1; RC2 §3.1 `G-1` |
| `M44-N-12` | "A milestone number may be assigned to a deferred successor obligation `D-1` through `D-7`." | RC2 §4.5, §17 `OQ-4` |
| `M44-N-13` | "An M44 work package may begin before the M44 architecture confirmation resolves at the path frozen RC2 §1.1 declares." | RC2 §1.1; Freeze Record §2.1 |
| `M44-N-14` | "A hard-coded `252`, `365`, `365.25`, `sqrt(252)`, or short-history threshold in existing code establishes, evidences, or constrains the governed annualization basis." | M43-WP4 §6.7; M43-WP1 §3.3; constitution G6 |
| `M44-N-15` | "An existing calendar, temporal, or market-session contract kind is, without proof, the exact *existing* governed contract kind frozen M43-WP2 §8.1 requires for annualization." | M43-WP2 §8.1; M43-WP4 §6.7 |
| `M44-N-16` | "M44 may amend, correct, restate, re-file, or supersede a frozen M42 or M43 artifact." | RC2 INV-C1, §13.3 — "All frozen M1–M43 artifacts: `NONE`" |
| `M44-N-17` | "The two universal normative specifications exist, or are partly satisfied, because frozen M43 names their filenames." | M43-WP7 §3.1 — "A plan, expected filename, or unchanged prerequisite is not a substitute for an existing independently confirmed normative specification" |
| `M44-N-18` | "M44 may mark a roadmap capability complete, partially complete, or in progress." | RC2 §13.3 |
| `M44-N-19` | "The M44-WP1 register or this reconciliation grants a downstream work package authority to begin." | RC2 §11 M44-WP1 freeze boundary — authority arrives only with independent confirmation; §12.5 |
| `M44-N-20` | "The gate-state checkpoint may be declared satisfied by the work package that produced the gate state, or by the M44-WP1 artifacts themselves." | RC2 §12.1.1 — "No work package may declare the checkpoint satisfied on its own authority" |
| `M44-N-21` | "A document-local mechanical label — `P-1`, `P-2`, `RQ-1`, `C-nn`, `M44-N-nn`, or a pre-inventory status token — is a constitutional noun, a gate, or a disposition." | RC2 §9.7; register §11 |
| `M44-N-22` | "Provenance carriage converts raw provider semantics into governed evidence." | RC2 INV-V3; M42-WP6 §5.2 |
| `M44-N-23` | "An owner may be determined for the annualization basis, or for the period-return rule, by placement convenience, adjacency, or current code location." | M43-WP4 §6.7; M43-WP1 §7.3; constitution G6; RC2 §17 `OQ-3` |
| `M44-N-24` | "M44-WP1's pre-inventory determines `G-3`'s terminal state, or decides frozen RC2 §17 `OQ-1`." | RC2 §17 `OQ-1` decision deadline — the checkpoint decides; §11 M44-WP1 excluded scope — "Closing any gate" |

---

## 6. Nested-coordinate encoding-obligation pre-inventory

### 6.1 What this pre-inventory is

Frozen RC2 §11 allocates to M44-WP1 the "nested-coordinate encoding-obligation
pre-inventory feeding WP4," and frozen RC2 §17 `OQ-1` states its evidentiary
role: "The WP1 pre-inventory is the deciding evidence for both" — for M44-WP4's
scoping question, and for the stop-or-re-scope decision at the §12.1.1
checkpoint.

It is an **inventory of obligations and of what the frozen corpus does and does
not supply**. It is not a decision, a recommendation, an encoding, a schema, a
solicitation to another domain, or a determination of `G-3`'s terminal state.
`M44-N-24` forbids reading it as any of those.

### 6.2 The governing test

Frozen
[M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md)
§7.1 states the test this pre-inventory applies, verbatim:

> "If an owning contract cannot supply one exact immutable canonical reference
> or canonical representation required here, a conforming subject cannot be
> formed."

Applied to canonical bytes, that test decomposes into three separable questions
per coordinate. Separating them is required, not stylistic: frozen RC2 §3.1
records that the prohibition on encoding nested source-owned content "is a
boundary on conforming canonical-byte language, not a bar against it," which is
only true if the container framing and the nested content are assessed apart.

| Question | What it asks | Who can answer it |
| --- | --- | --- |
| **(a) Reference exactness** | Does the owning frozen contract supply one exact, immutable, semantically unambiguous reference or representation for this coordinate? | The owning contract, already frozen |
| **(b) Written-form determinacy** | Does frozen authority fix the exact written form that reference takes — its value domain, lexical form, and, for a composite coordinate, its nested element order? | The owning domain. M44 may not invent it (`M44-N-08`) |
| **(c) M44-WP4 encodability** | May M44-WP4 supply the byte form of this coordinate's content without violating a frozen prohibition? | Frozen M42-WP7 §9 items 11–12 and PC-NGV-14 |

Question (c) has one frozen answer for every source-owned coordinate, stated
once here rather than repeated in each row. M42-WP7 §9 checklist item 11
requires that "No source-owned nested coordinate is reordered, normalized,
**encoded**, or reinterpreted," and PC-NGV-14 makes it a non-conforming shape
when "Canonical-byte language defines upstream encoding, fields, schema, or
identifiers." **M44-WP4 may therefore frame the container and carry the exact
citations; it may not author the byte form of any source-owned coordinate's
content.** Where (b) is unsatisfied, the obligation routes to the owner and,
per frozen RC2 §3.1, routing "records the obligation; it does not discharge it."

### 6.3 Per-field inventory

The ten fields are the frozen M42-WP7 §5 canonical semantic field order,
reproduced in that order and not reordered. Owners are quoted from frozen
M42-WP7 §3; none is determined here.

| # | §5 field | Owner (M42-WP7 §3) | (a) Reference exactness | (b) Written-form determinacy | Frozen evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | `schema_version` | Portfolio Intelligence (container framing, M42-WP7 §5) | `SUPPLIED — EXACT` | `SUPPLIED — EXACT LITERAL` | M42-WP7 §5: "The schema-version tag is exactly M42-WP7-PORTFOLIO-COMPOSITION-1"; §9 item 10 |
| 2 | `portfolio_identity` | Ledger & Accounting | `SUPPLIED — EXACT` — the coordinate is itself "the stable identifier of one portfolio container" | `NOT SUPPLIED` — no identifier syntax, value domain, or lexical form is frozen | `GLOSSARY.md` "Portfolio Identity"; `M34-D-0002`; M42-WP2 §5.1 "This contract adds no field, exception, or alternate meaning" |
| 3 | `accounting_scope` | Ledger & Accounting | `SUPPLIED — EXACT` — an exact corresponding-scope citation is required and owner-supplied | `NOT SUPPLIED` — no scope-reference form is frozen | `GLOSSARY.md` "Accounting Scope"; `M34-D-0002`; M42-WP2 §5.2; M42-WP7 §3 "Exact corresponding-scope citation" |
| 4 | `portfolio_membership` | Ledger & Accounting | `NOT SUPPLIED` — the coordinate is an "Exact Ledger fact"; no canonical representation of the membership set, its elements, its cardinality, or its order is frozen | `NOT SUPPLIED` | M42-WP7 §3; M42-WP2 §5.3; `M34-D-0003` |
| 5 | `portfolio_base_currency` | Ledger & Accounting (coordinate); Asset Foundation (the currency-of-denomination dimension) | `SUPPLIED — EXACT` — "a single reference to Asset Foundation's currency-of-denomination coordinate for one Portfolio Identity" | `NOT SUPPLIED — EXPRESSLY` | M42-WP2 §6.2: "this contract does not itself mint a format, because none is frozen for it to cite yet"; "Until Asset Foundation publishes that exact format..." |
| 6 | `investment_universe_declaration` | Portfolio Intelligence (declaration); Asset Foundation (criterion vocabulary) | `SUPPLIED — EXACT` — the complete six-facet declaration of M42-WP3 Stage B §9.1 | `NOT SUPPLIED` — no identifier syntax, no envelope, no nested order | M42-WP3 Stage B header `Serialization authority: NONE`; §5.3 "deliberately defines no identifier syntax... not a WP3-defined string, code, URI, key, or byte representation"; §9.1 "does not prescribe a serialized envelope, field order, schema, identifier, bytes, transport"; NGV-26 |
| 7 | `portfolio_benchmark_declaration` | Portfolio Intelligence (declaration); Market Intelligence (series); Asset Foundation (`asset_id`) | `SUPPLIED — EXACT` for all four forms, including Explicitly None | `PARTIAL` — see the facet breakdown at §6.4 | M42-WP5 §§4.2–4.5; M42-WP7 §4.4 |
| 8 | `portfolio_lifecycle_state` | Ledger & Accounting | `SUPPLIED — EXACT` | `SUPPLIED — CLOSED LITERAL VOCABULARY` — exactly `active`, `archived`, `closed`, with no fourth value admissible | M42-WP6 §4.1 item 2, §4.2, §4.3; `GLOSSARY.md` "Portfolio Lifecycle State" |
| 9 | `coordinate_owner_attributions` | Portfolio Intelligence (association only) | `SUPPLIED — EXACT` — the owner names are the frozen domain names of M42-WP7 §3 | `NOT SUPPLIED` — no attribution form is frozen; framing is available to M44-WP4 because the element is the container's own | M42-WP7 §5: "Owner attribution and Provenance association preserve association only; neither creates a new owner or Provenance meaning" |
| 10 | `coordinate_provenance_associations` | Connectivity & Ingestion (meaning and capture); Portfolio Intelligence (association only) | `NOT SUPPLIED` for the Provenance content — no capture format, evidence class, storage shape, or completeness test is frozen | `NOT SUPPLIED` — the association is framable; the carried content is not | M42-WP6 §5.1: "It does not define what must have been captured, a capture format, a confidence threshold, an evidence class, a storage shape, or a completeness test"; §5.2 forbids parsing, normalization, and summarization |

**Tally at the reconciliation date.** Of the ten frozen §5 fields, question (b)
is:

- **satisfied for two** — `schema_version` (an exact frozen literal) and
  `portfolio_lifecycle_state` (a closed literal vocabulary of exactly three
  values);
- **partially satisfied for one** — `portfolio_benchmark_declaration`, whose
  series references carry a frozen, named citation format while three of its
  other facets carry none (§6.4);
- **unsatisfied for seven** — `portfolio_identity`, `accounting_scope`,
  `portfolio_membership`, `portfolio_base_currency`,
  `investment_universe_declaration`, `coordinate_owner_attributions`, and
  `coordinate_provenance_associations`.

One of those seven, `coordinate_owner_attributions`, is the container's own
framing element, which M44-WP4 may frame without encoding source-owned content;
that leaves **six source-owned coordinates** whose written form no frozen
authority supplies. Question (a) is additionally unsatisfied for two of the six
— `portfolio_membership`, and the carried content of
`coordinate_provenance_associations`.

### 6.4 Facet breakdown for the composite coordinates

Fields 6, 7, and 10 are not atomic. Their facets are inventoried separately
because frozen M42-WP7 §5 states plainly that the container contract "does not
define nested field order inside any source-owned coordinate," so each facet
carries its own obligation.

**Field 6 — Investment Universe declaration** (facets exactly as frozen M42-WP3
Stage B §9.1 enumerates them):

| Facet | (a) | (b) | Note |
| --- | --- | --- | --- |
| Exact Portfolio Identity citation | `SUPPLIED` | `NOT SUPPLIED` | Inherits field 2 |
| Exact corresponding Accounting Scope citation | `SUPPLIED` | `NOT SUPPLIED` | Inherits field 3 |
| Explicit declared name | `SUPPLIED` | `NOT SUPPLIED` | Stage B §4.2: "This contract defines no lexical encoding, length limit, normalization, uniqueness rule, localization rule, or serialization for declared names" |
| Every present criterion-category coordinate | `SUPPLIED` | `NOT SUPPLIED` | No category order is frozen; NGV-26 records that Stage B does not supply one to a downstream serializer |
| Each criterion's set-or-range extent and exact Asset Foundation references | `SUPPLIED` | `NOT SUPPLIED` | Stage B §5.3: exactness "means semantic identity with the source-owned reference, not a WP3-defined string, code, URI, key, or byte representation" |
| The immutable-until-explicitly-revised semantic condition | `SUPPLIED` | `NOT SUPPLIED` | A semantic condition with no frozen representation |

**Field 7 — Portfolio Benchmark Declaration:**

| Facet | (a) | (b) | Note |
| --- | --- | --- | --- |
| Benchmark series references (Single, Composite, Category) | `SUPPLIED — EXACT` | `PARTIAL` | M42-WP5 §4.4 requires "the frozen `asset_id` format: the platform's own permanent, opaque identifier, owned by Asset Foundation and defined once at UNIVERSAL_ASSET_ARCHITECTURE.md §2–3." The reference form is frozen and named; the identifier is expressly **opaque**, and no lexical form is published for it |
| The explicit declared name | `SUPPLIED` | `NOT SUPPLIED` | M42-WP5 §4.2: "WP5 defines no name syntax, identifier format, uniqueness scope, localization, normalization, storage, or serialization rule" |
| The closed form discriminator | `SUPPLIED` | `CONSTRAINED — NOT SUPPLIED` | M42-WP5 §4.3: "The four form labels classify the declaration only. They do not authorize runtime discriminators, **serialized tags**, API values, database enumerations, or implementation constants." A canonical byte form must distinguish the four forms without using the labels as tags; no frozen authority supplies how |
| Explicitly None | `SUPPLIED — EXACT` | `NOT SUPPLIED` | An affirmative state distinct from missing (M42-WP7 §4.4, PC-NGV-10); no representation is frozen, and the distinction must survive encoding |
| Composite weights | Not applicable | Not applicable | M42-WP5 §4.3 places "calculation, weighting, construction, maintenance, and observation values" outside the declaration; no encoding obligation arises |

**Field 10 — Coordinate Provenance associations:**

| Facet | (a) | (b) | Note |
| --- | --- | --- | --- |
| The association between one Provenance item and its exact coordinate | `SUPPLIED` | `NOT SUPPLIED` — framable by the container | M42-WP6 §5.1 items 2 and 5; M42-WP7 §5 |
| The already-captured Provenance content itself | `NOT SUPPLIED` | `NOT SUPPLIED` | M42-WP6 §5.1; encoding it would require parsing or normalizing it, both prohibited by §5.2 |
| Separation of one coordinate's Provenance from another's | `SUPPLIED` | `NOT SUPPLIED` | M42-WP6 §5.1 item 2 and §5.2 — combination "in a way that obscures which origin belongs to which coordinate" is prohibited, which is an encoding constraint, not a form |

### 6.5 Obligation routing map

For every unsatisfied cell, the obligation routes to the frozen owner named
below. **This map is a record, not a request.** M44 holds no authority in any
domain but Portfolio Intelligence (frozen RC2 INV-C4), and frozen RC2 §17
`OQ-1` alternative (b) — soliciting per-coordinate records from owning domains
— is expressly "constitutionally unavailable to M44 in any case."

| Unsupplied element | Frozen owner it routes to | M44 authority over it |
| --- | --- | --- |
| Portfolio Identity reference form | Ledger & Accounting | `NONE` |
| Accounting Scope reference form | Ledger & Accounting | `NONE` |
| Portfolio Membership canonical representation | Ledger & Accounting | `NONE` |
| Portfolio Base Currency identifier format | Asset Foundation (the dimension), Ledger & Accounting (the coordinate) | `NONE` |
| Investment Universe declaration nested form and order | Portfolio Intelligence, under the frozen M42-WP3 Stage B contract | `NONE` without amending a frozen M42 artifact, which INV-C1 forbids — see §6.6 |
| Benchmark declared-name form; form-discriminator representation; Explicitly None representation | Portfolio Intelligence, under the frozen M42-WP5 contract | Same as above |
| `asset_id` lexical form | Asset Foundation | `NONE` |
| Provenance content representation | Connectivity & Ingestion | `NONE` |

### 6.6 The own-domain question, recorded and referred

Two of the unsupplied elements — the Investment Universe declaration's nested
form and three Benchmark Declaration facets — belong to coordinates that frozen
M42-WP7 §3 allocates to **Portfolio Intelligence**, the same domain that holds
M44. Whether M44-WP4 may therefore supply those forms is a real question with
frozen text on both sides:

- **For:** M42-WP3 Stage B §9.2 permits the downstream composer to "define
  Portfolio Composition and portfolio-wide serialization only under WP7's own
  separately confirmed authority," and frozen RC2 §3.1 records that the
  encoding prohibition "is a boundary on conforming canonical-byte language,
  not a bar against it."
- **Against:** M42-WP7 §9 checklist item 11 bars encoding a "source-owned
  nested coordinate" without qualifying the owner, and M42-WP7 §5 states the
  container contract "does not define nested field order inside any
  source-owned coordinate." Supplying a nested form that the frozen owning
  contract declines to supply may constitute a silent amendment of frozen M42,
  which frozen RC2 R-1 names as the milestone's critical risk and INV-C1
  forbids.

**This artifact does not resolve it.** Resolution is a scoping determination
frozen RC2 §17 `OQ-1` assigns to M44-WP4 — "Decision deadline. Before M44-WP4
begins for the scoping question" — under its own independent confirmation. It
is recorded here as the pre-inventory's principal referred question so that
M44-WP4 begins with it named rather than discovering it mid-authorship.

### 6.7 Finding

Frozen RC2 §17 `OQ-1` is conditional on a fact about the repository: "If the
WP1 pre-inventory establishes that every required coordinate reference is
available, G-3 closes and the milestone proceeds on its planned path. If any is
unavailable, (c) is mandatory and (a) is unavailable."

**The pre-inventory records the fact, not the consequence.** As verified on
2026-07-29, the frozen corpus does **not** supply an exact written form for
every required Portfolio Composition coordinate reference. Six source-owned
coordinates lack it outright, one further field lacks it in part, and for two of
the six the underlying canonical representation is itself unsupplied (§6.3
tally). Every unsupplied
element is owned by a domain in which M44 holds no authority, save the two
own-domain cases referred at §6.6.

That is the antecedent of `OQ-1`'s second branch, observed. The consequent —
whether `G-3` terminates `CLOSED` or `OPEN — PARTIAL`, and whether the
milestone stops or is formally re-scoped — is a determination frozen RC2
reserves to M44-WP4 and to the §12.1.1 checkpoint confirmation. This artifact
draws it neither by statement nor by implication, and companion register §4.3
continues to record `G-3`'s terminal state as `NOT YET DISPOSITIONED`.

Two consequences follow for how this evidence must be used, both stated as
frozen requirements rather than as this artifact's advice:

1. M44-WP4 consumes this pre-inventory; it does not re-derive it (frozen RC2
   §11 M44-WP1 freeze boundary — "later M44 work packages cite it and may not
   re-derive the inventory").
2. The §12.1.1 checkpoint may not treat an unsupplied element as supplied, and
   may not treat this pre-inventory as the checkpoint's own confirmation
   (`M44-N-20`).

---

## 7. Re-evaluation of M44-WP1 against frozen RC2 §11

### 7.1 Allocation checklist

Every element frozen RC2 §11 allocates to M44-WP1, checked against the
repository at the reconciliation date.

| Frozen RC2 §11 allocation | Where discharged | State |
| --- | --- | --- |
| **Architectural deliverable 1** — `M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md` | [the register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md), at the frozen path | `EXISTS` |
| **Architectural deliverable 2** — `M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md` | this artifact, at the frozen path | `EXISTS` |
| **Implementation deliverables** — `NONE` | — | `SATISFIED` — no non-`docs/` path is written |
| Included scope: gate inventory with exact path and section citations | register §4, §5, §9 | `PRESENT` |
| Included scope: gate-to-work-package mapping | register §6, §7 | `PRESENT` |
| Included scope: roadmap and current-state reconciliation for M44 | §2, §3, §4 here | `PRESENT` |
| Included scope: vocabulary-sufficiency finding | register §11; extended to this artifact at §7.4 | `PRESENT` |
| Included scope: M44 negative corpus | §5.2 here, twenty-four statements, plus the twenty-three carried forward at §5.1 | `PRESENT` |
| Included scope: nested-coordinate encoding-obligation pre-inventory feeding WP4 | §6 here | `PRESENT` |
| Excluded scope: closing any gate; admitting any noun; determining any owner; selecting any encoding | register §1.2, §13; §1.3 and §5.2 here | `OBSERVED` — none occurs |
| Required test: citation-existence check for every gate | register §9, §13 | `PERFORMED` — re-verification is a review obligation |
| Required test: completeness check against the frozen M43-WP7 §3.2 enumeration | register §5.1, 10 of 10 | `PERFORMED` |
| Required test: collision and overlap scan | register §13; §7.4 here | `PERFORMED` |
| Required test: negative-corpus review | §5 here | `AUTHORED` — the review itself is the independent reviewer's act |
| Completion criterion: every gate appears exactly once, with an exact citation and exactly one disposition | register §4.0, §5, §10.2 `C-04`–`C-06` | `SATISFIED` |
| Completion criterion: no gate is unassigned | register §6.1 | `SATISFIED` |
| Completion criterion: no new noun is required, or each has entered the vocabulary gate | register §11; §7.4 here | `SATISFIED` — none is required |
| Expected repository impact: "Two new files in `docs/implementation/`" | the register and this artifact | `MATCHES EXACTLY` — two files, no third |
| Freeze boundary: frozen on independent confirmation | — | `NOT REACHED` |

**Every artifact frozen RC2 §11 allocates to M44-WP1 now exists at the path
frozen RC2 §11 and §13.1 declare.** The repository impact is exactly the two
files forecast — no third file was created, and no frozen artifact was
modified.

### 7.2 Supersession record for companion register §10.1

Companion register §10.1 records, in a column headed "State at register date,"
that criteria `C-02` and `C-03` are `NOT MET`, and §10.5 names both as
explicitly outstanding. That snapshot was taken at the point of the register's
authoring, before this artifact existed.

Under this artifact, both are now met:

| Criterion | Register's recorded state | State on this evidence | Where |
| --- | --- | --- | --- |
| `C-02` — the reconciliation exists at the frozen path | `NOT MET` | `MET` | this artifact |
| `C-03` — the nested-coordinate pre-inventory exists, is cited, and is the deciding evidence for frozen RC2 §17 `OQ-1` | `NOT MET` | `MET` | §6 here, cited by §7.1 |
| `C-25` / `P-1` — the frozen Freeze Record §2.1 filing remediation is performed, so the M44 confirmation resolves at the path frozen RC2 §1.1 declares | `NOT MET`; register §3.1 records the rename as not performed and §3.2 declares the register `NON-EFFECTIVE` in part on that ground | `MET` | §3.1 here, verified by directory enumeration on 2026-07-29 |

The `C-25` change is not this work package's doing: the rename was performed
outside M44-WP1, between the register's authoring and this artifact's. The
register's §3 statement was accurate when written and is superseded by verified
repository evidence, not corrected as an error. Companion register §3.2's
`NON-EFFECTIVE` declaration still stands on its remaining ground, `P-2`, which
is unsatisfied (§7.3).

This is recorded as a supersession, not performed as an edit. The register's
text is not modified by this artifact, which holds no authority over a
companion artifact's content. Constitution G5 leaves level-4 artifacts free to
be revised and owes the reader currency; a confirming reviewer may therefore
require the register's §10.1 column and §10.5 to be refreshed as part of the
confirmation act. Recording the divergence here, rather than silently editing
the register, keeps the package's internal state visible to that reviewer.

### 7.3 What remains outstanding for M44-WP1 completion

Delivering both artifacts does not complete the work package. The following
criteria remain unmet, and no reading of this artifact may treat M44-WP1 as
complete, confirmed, or authorized:

| Criterion | State | Basis |
| --- | --- | --- |
| `C-26` — independent constitutional review by a reviewer who did not author | `NOT MET` | Frozen RC2 §12.4, §16.4 |
| `C-27` — every finding answered by a corrections response, and every correction re-reviewed | `NOT MET` | Frozen RC2 §12.5 |
| `C-28` — independent confirmation recorded with unresolved findings `NONE` (`P-2`) | `NOT MET` | Frozen RC2 §12.5 point 2 |

`M44-WP1` is therefore `RC1 — STRUCTURALLY COMPLETE, NOT CONFIRMED`. Frozen RC2
§12.5 point 2 makes M44-WP1's confirmation the gate "before any gate closure,"
and §11 makes its freeze boundary independent confirmation. No downstream M44
work package is released by this artifact.

### 7.4 Vocabulary-sufficiency finding for this artifact

Companion register §11 records the work package's finding: no new
constitutional noun is required. This artifact does not disturb it.

Every term used here is already disposed by a frozen artifact: the M42
coordinate nouns and the ten §5 field names, consumed verbatim from frozen
M42-WP7 §5; the gate, deferred-obligation, component, extension-basis, and
terminal-state identifiers, consumed from frozen RC2; the roadmap capability
names, consumed from `docs/architecture/ROADMAP.md`; and the legacy surface
names, consumed from frozen M43-WP1 §§3.1–3.5.

The identifiers `M44-N-01` through `M44-N-24`, and the pre-inventory's status
tokens `SUPPLIED — EXACT`, `NOT SUPPLIED`, `PARTIAL`, and `CONSTRAINED — NOT
SUPPLIED`, are **document-local mechanical labels**: they name no semantic
concern, allocate no ownership, carry no authority, and are scoped to this
artifact and its companion. `M44-N-21` forbids reading them as constitutional
nouns. Collision scan against the frozen corpus: no collision found — no frozen
artifact uses the `M44-N-` prefix, and the status tokens are not gate states
and are textually distinct from the five terminal states of frozen RC2 §16.2.
`docs/GLOSSARY.md` is not modified.

### 7.5 Package integrity note — citations invalidated by the `P-1` remediation

The rename recorded at §3.1 invalidated four citations in the companion
register, which cited the review-chain artifacts at the paths they occupied
when it was written:

| Register location | Citation as written | State |
| --- | --- | --- |
| §3.1, the filing-divergence verification table | The four superseded paths, recorded as present | Now inaccurate; the remediation the table tracked has been performed |
| §9.1, four evidence rows | `M44_INDEPENDENT_CONFIRMATION.md`, `M44_CONSTITUTIONAL_ADJUDICATION.md`, `M44_FORMAL_CONSTITUTIONAL_RESPONSE.md`, `M44_INDEPENDENT_CONSTITUTIONAL_REVIEW.md` | Do not resolve; each artifact exists at its `M44_ARCHITECTURE_*` path |

The **substance** of all four citations is unaffected: the same artifacts, with
the same content and the same `APPROVED FOR FREEZE` result, exist at the
conforming paths, as verified at §3.1. What is affected is the register's
citation-existence test, `C-08`, which requires that "Every cited path and
section resolves."

This artifact records the divergence and does not repair it: the register's
text is a companion artifact's, and repairing it was outside the scope this
work package was given. **A confirming reviewer should treat the four citations
as requiring path correction before confirmation**, which is a mechanical
re-pointing that changes no finding, no disposition, and no authority.

---

## 8. Reconciliation result

The repository state confirms the exact condition M44 was frozen to address,
and confirms it has not yet changed:

1. Five inherited gates are open, and every one of them is open on **absence**
   — an absent confirmation record, an absent ownership correction, an absent
   canonical-byte contract, an absent governed dependency, two absent
   normative specifications — not on disagreement about substance.
2. The frozen M42 coordinate-owning contracts uniformly declare no
   serialization authority, exactly as their own freeze boundaries intended.
   That is the mechanism by which `G-3` survives intact into M44.
3. Six source-owned Portfolio Composition coordinates lack an owner-supplied
   written form, and every unsupplied element outside two own-domain cases
   belongs to a domain in which M44 holds no authority.
4. Legacy runtime behavior is unchanged, unblessed, and unusable as precedent
   under constitution G6; the annualization constants in current code neither
   evidence nor constrain the governed dependency `G-4` names.
5. No roadmap capability has moved, and no governance record has been
   synchronized.

These findings justify the work package's register and pre-inventory. They
authorize no fix, no closure, and no work package. Repository code, runtime
behavior, APIs, persistence, consumers, and every frozen artifact remain
unchanged.

---

## 9. Completion gate for this artifact

This reconciliation is ready for independent constitutional review when, and
only when, all of the following hold. Each is falsifiable against repository
evidence.

1. The roadmap section contains no M44 capability-completion claim, and
   `docs/architecture/ROADMAP.md` is unmodified.
2. The current-state inventory covers the M44, M43, and M42 corpora, the four
   repository governance records, and the legacy runtime surface, and every
   absence claim is verified by enumeration rather than inferred.
3. The legacy inventory of frozen M43-WP1 §§3.1–3.5 is consumed by citation,
   not re-derived, and no disposition in frozen M43-WP1 §4 is changed, added
   to, or softened.
4. The negative corpus carries forward the frozen twenty-three by citation and
   states the M44-specific statements with a frozen basis for each.
5. The nested-coordinate pre-inventory covers all ten frozen M42-WP7 §5 fields
   in their frozen order, breaks out every composite coordinate's facets,
   cites frozen text for every status, and states its finding as an observed
   antecedent rather than as a gate disposition.
6. No gate is dispositioned, no owner is determined, no encoding is selected,
   no noun is admitted, and no work package is authorized.
7. No frozen artifact is modified; the work package's total repository impact
   is exactly the two files frozen RC2 §11 and §13.1 forecast.
8. Every cited path and section resolves and says what the citation claims.

Independent confirmation of this artifact **and** its companion register is
required before any downstream M44 work package relies on either. The
authorization precondition `P-1` recorded at companion register §3 is satisfied
as of 2026-07-29 (§3.1, §7.2); `P-2`, that confirmation itself, is not.

---

## 10. Final constitutional boundary

This artifact reconciles a roadmap that does not move, inventories a repository
state that has not changed, and records an encoding obligation that its
milestone cannot discharge alone. It closes nothing. It releases nothing. It
determines no owner, selects no encoding, and admits no noun.

Its one substantive contribution is evidentiary: it establishes, by frozen
citation and verified absence, what the Portfolio Composition canonical-byte
obligation would require and who alone can supply each part of it. Frozen RC2
§17 `OQ-1` designates that evidence as deciding. Deciding on it is somebody
else's act — M44-WP4's, and the §12.1.1 checkpoint's, each under its own
independent confirmation.

M44-WP1 is structurally complete and is not confirmed. This artifact says so
rather than claiming otherwise.
