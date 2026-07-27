# M42-WP4 — Portfolio Policy Ownership Investigation

**Document role:** Architecture Review ownership and admissibility investigation

**Milestone:** M42 — Portfolio Intelligence Foundation

**Work package:** M42-WP4

**Investigation date:** 2026-07-27

**Document status:** `COMPLETE — REJECT`

**Authority posture:** M42 Architecture, M42-WP1, M42-WP2, and M42-WP3 are
accepted as complete, confirmed, and frozen under the session mandate. This
document cites that authority and does not reopen it.

**Implementation authority:** `NONE`

**Contract-design authority:** `NONE`

**Admission outcomes permitted:** `ADMIT under proven owner`, `REJECT`, or
`REMAIN BLOCKED`

**Scope fence:** This document investigates only whether the proposed
**Portfolio Policy** noun is admissible and whether one constitutional domain
owns it. It defines no policy structure, syntax, rule, allocation, limit,
execution behavior, optimizer behavior, enforcement behavior, persistence,
API, or implementation.

---

## 1. Executive Assessment

**Assessment: `REJECT`.**

Portfolio Policy is not admissible as one canonical platform noun under
Portfolio Intelligence or any other constitutional domain.

The investigation establishes three facts:

1. The noun does not already exist as a canonical term in
   [GLOSSARY.md](../GLOSSARY.md).
2. Its constraint-shaped meaning is not new. Frozen `M34-D-0007` already
   assigns policy envelopes, decision constraints, execution preferences, and
   portfolio-composition constraints to **Decision Policy** and **Portfolio
   Limits**, owned by **Decision Intelligence**.
3. The remaining meaning grouped beneath the proposed noun has no proven
   single owner. M42-WP1 deliberately leaves that residue unresolved rather
   than assigning it by silence.

The first fact prevents canonical reuse of the exact noun. The second prevents
admission to Portfolio Intelligence or reassignment of the whole to another
domain without duplicating frozen authority. The third prevents admission of
the whole under Decision Intelligence, Ledger & Accounting, Asset Foundation,
or a speculative future owner.

This is no longer merely an absence of proof that warrants `REMAIN BLOCKED`.
Confirmed M42-WP1 supplied the required ownership investigation and reached
the frozen disposition `REJECT`. The blocked branch in the M42 Architecture
therefore resolves to non-progression, not to contract design.

---

## 2. Existing Authority Survey

### 2.1 Governing authority

| Authority | Existing ruling relevant to WP4 | Effect on this investigation |
| --- | --- | --- |
| [Platform Architecture](../architecture/platform_architecture.md) §6.1 | Asset Foundation owns asset identity, classification, and asset-behavior vocabulary. | Asset facts and capabilities do not make Asset Foundation the owner of portfolio operating judgment. |
| Platform Architecture §6.3 | Ledger & Accounting owns financial truth, the accounting boundary, and deterministic recorded state. | Accounting facts do not create ownership of a forward-looking policy envelope. |
| Platform Architecture §6.5 | Portfolio Intelligence owns derived portfolio meaning and measures. | It does not receive policy-envelope ownership; its later-frozen Portfolio Strategy Metadata expressly excludes Decision Policy. |
| Platform Architecture §6.6 | Decision Intelligence owns policy and constraint governance and the policy envelope. | This is the constitutional home of the already-governed policy/constraint meaning. |
| Platform Architecture §12, V1 | Every platform noun has one meaning and one home. | A composite spanning frozen and unresolved ownership cannot be admitted. |
| `M34-D-0007` | Portfolio Strategy Metadata belongs to Portfolio Intelligence; Decision Policy, Portfolio Limits, and Sector Limits belong to Decision Intelligence. Grouping or presentation does not create a semantic owner. | The proposed noun cannot acquire ownership merely because its values are presented as portfolio declarations. |
| [Glossary](../GLOSSARY.md), **Portfolio Strategy Metadata** | Owned by Portfolio Intelligence and expressly excludes Decision Policy. | Portfolio Policy cannot be absorbed into Portfolio Strategy Metadata without contradicting frozen text. |
| Glossary, **Decision Policy** | Policy envelopes, optimization rules, decision constraints, execution preferences, and optimizer behavior; owned by Decision Intelligence. | The proposed noun's central operating-envelope meaning is already governed. |
| Glossary, **Portfolio Limits** | Constraints on portfolio composition and optimization; owned by Decision Intelligence. | A second portfolio-owned constraint surface would duplicate existing authority. |
| [Optimizer Philosophy](../investment/OPTIMIZER_PHILOSOPHY.md) §§2–3 | Risk and policy constraints form a deterministic envelope, including portfolio constraint concerns. | Confirms that declaration wording does not separate the proposed meaning from Decision Intelligence's frozen territory. |
| [Portfolio Domain Model](../architecture/PORTFOLIO_DOMAIN_MODEL.md) §5 | Proposes Portfolio Policy as one portfolio-level operating rulebook consumed by validation, constraint resolution, and execution planning. | This Level-4 proposal supplies the candidate, but cannot override higher frozen ownership. |
| [M42 Architecture Proposal](M42_ARCHITECTURE_PROPOSAL.md) §§0, 4.2, 5, 6, 11 | Marks Portfolio Policy admission-blocked, forbids ownership migration, and states WP4 does not proceed if WP1 cannot prove distinct Portfolio Intelligence ownership. | WP4 has no authority to design a contract before a positive ownership result. |
| [M42-WP1 Ownership Register](M42_WP1_PORTFOLIO_CANONICAL_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §6.2 and §8 | Dispositions Portfolio Policy `REJECT`; proves overlap with Decision Policy / Portfolio Limits and leaves the remainder unresolved. It states M42-WP4 does not proceed as scoped. | This is the controlling candidate-specific result. |

### 2.2 Does Portfolio Policy already exist?

**As an exact canonical noun: no.** There is no Portfolio Policy entry in the
canonical Glossary.

**As governed meaning: materially yes, but not as one intact object.** The
constraint and operating-envelope meaning already exists as Decision Policy
and Portfolio Limits under Decision Intelligence. Other concerns collected by
the Level-4 Portfolio Domain Model touch boundaries owned by Asset Foundation,
Ledger & Accounting, Wealth Intelligence, and Decision Intelligence, or remain
unresolved under confirmed M42-WP1.

Portfolio Policy is therefore neither a clean synonym that can be canonically
reused nor a new, ownership-coherent noun that can be admitted.

### 2.3 Authority discrepancy that must not change the result

The non-normative
[M42-WP1 Roadmap Reconciliation](M42_WP1_ROADMAP_RECONCILIATION.md) describes
some residual concerns more conclusively than the corrected WP1 register.
The reconciliation identifies itself as provisional and states that it makes
no architectural decision. The corrected WP1 register is the
candidate-specific authority and expressly leaves the residual ownership
unresolved. This investigation follows the register and makes no new
field-level ownership ruling.

---

## 3. Ownership Analysis

### 3.1 Portfolio Intelligence

**Not owner.**

Portfolio Intelligence owns Portfolio Strategy Metadata, but the frozen
Glossary expressly excludes Decision Policy from that concept. The proposed
Portfolio Policy would place an operating and constraint envelope beside the
Decision Policy and Portfolio Limits already owned by Decision Intelligence.
Calling that envelope declarative data does not create a different semantic
owner: `M34-D-0007` expressly rejects ownership inferred from grouping,
storage, or presentation.

Admission here would reopen frozen M34 ownership and violate M42's
non-reopening rule.

### 3.2 Ledger & Accounting

**Not owner.**

Ledger & Accounting owns recorded financial truth, Accounting Scope,
Portfolio Identity, and deterministic accounting state. A forward-binding
operating envelope is not ledger truth. Some proposed concerns may consume or
refer to accounting facts, but reference does not transfer semantic ownership.
Confirmed WP1 did not assign the unresolved residue to Ledger & Accounting.

Admission here would mix prospective judgment with recorded truth and would
still duplicate Decision Intelligence's frozen policy territory.

### 3.3 Asset Foundation

**Not owner.**

Asset Foundation owns asset identity, classification, and asset capabilities.
It can describe what an asset or asset class is capable of doing. Whether one
portfolio permits or constrains an operation is not an asset-definition fact.
Sector Limits already demonstrate the boundary: Decision Intelligence may
reference Asset Foundation classification without redefining or transferring
ownership of classification.

Admission here would turn asset facts into portfolio judgment and would not
resolve the proposed noun's accounting- and decision-adjacent concerns.

### 3.4 Decision Intelligence

**Owner of the already-governed policy-envelope meaning, but not a proven
owner of the proposed composite noun.**

Platform Architecture §6.6, `M34-D-0007`, the Glossary, and Optimizer
Philosophy align: Decision Intelligence owns Decision Policy, Portfolio
Limits, Sector Limits, and the deterministic policy envelope.

That evidence supports canonical reuse of those existing terms by future
authorized consumers. It does **not** support admitting Portfolio Policy as an
additional umbrella term. Doing so would duplicate existing canonical meaning
and would silently pull unresolved residue into Decision Intelligence. V1
forbids both outcomes.

### 3.5 Wealth Intelligence or another existing domain

**Not owner.**

Wealth Intelligence owns Goal Target and cross-portfolio wealth meaning, not
the single-portfolio policy envelope. Market Intelligence owns observations,
not portfolio operating judgment. Experience Platform presents and mediates
human interaction; it does not own referenced business rules. Trust &
Evaluation evaluates decisions after the fact; it does not own the rules
being evaluated. Connectivity & Ingestion governs entry of external facts, not
policy meaning.

No remaining constitutional domain provides a coherent single home for the
composite.

### 3.6 Another future domain

**Not an admissible WP4 owner.**

M42 introduces no new constitutional domain. A speculative future domain
cannot satisfy the present proof burden, and frozen authority cannot be
assigned by forecast. Any future constitutional amendment or separately
chartered admission would be new authority, not continuation or completion of
M42-WP4.

### 3.7 Permanent exclusion

The **Portfolio Policy composite noun** must remain excluded from M42's
canonical vocabulary and contract roadmap under the frozen constitution.
This exclusion does not erase the underlying concerns and does not prohibit
future work from:

- reusing Decision Policy and Portfolio Limits under their frozen owner; or
- separately investigating an unresolved concern under a new charter and its
  own ownership gate.

Such work must not revive Portfolio Policy as an umbrella, treat WP4 as
blocked-but-pending, or infer ownership from the rejected grouping.

---

## 4. Admission Analysis

| Admission test | Finding | Result |
| --- | --- | --- |
| Exact canonical concept already exists | Portfolio Policy does not exist in the Glossary. | No direct `REUSE` path. |
| One meaning | The proposed noun groups already-governed policy-envelope meaning with unresolved residue. | Fail. |
| One constitutional home | Decision Intelligence owns the envelope; no single owner is proven for the whole. | Fail. |
| Non-duplication | Admission would duplicate Decision Policy and Portfolio Limits even if no enforcement implementation were designed. | Fail. |
| Frozen-boundary compatibility | Admission to Portfolio Intelligence or another domain would reopen `M34-D-0007`; admission to Decision Intelligence would absorb unresolved meaning without proof. | Fail. |
| Portfolio Intelligence specialization | Portfolio Strategy Metadata expressly excludes Decision Policy. | Fail. |
| New-domain necessity and authority | No future domain is proven, and M42 cannot create one. | Fail. |
| Contract eligibility | The M42 Architecture permits WP4 contract work only after positive owner proof; confirmed WP1 instead returned `REJECT`. | Fail. |

The candidate fails the constitutional V1 requirement independently of the
five-part descriptive-coordinate gate recorded by WP1. A declaration can be
portfolio-scoped, explicit, deterministic, and non-executable yet still be
inadmissible because its meaning has no single owner. Consequently:

- `ADMIT under proven owner` is unavailable;
- `REMAIN BLOCKED` is no longer accurate because the required investigation
  has produced a conclusive negative result; and
- `REJECT` is the only outcome consistent with the frozen record.

---

## 5. Recommendation

1. Close M42-WP4 as an ownership investigation with disposition `REJECT`.
2. Do not author a Portfolio Policy contract, vocabulary register, schema,
   rule surface, enforcement boundary, or implementation artifact.
3. Do not add Portfolio Policy to the canonical Glossary or treat it as a
   specialization of Portfolio Strategy Metadata.
4. Preserve Decision Policy, Portfolio Limits, and Sector Limits under
   Decision Intelligence without amendment or aliasing.
5. Leave every residual ownership question exactly as M42-WP1 left it:
   unresolved and outside WP4. Any later inquiry requires a separately
   chartered admission and cannot reuse this rejected composite as its assumed
   container.
6. Treat references in lower-level design documents that speak of Portfolio
   Policy as historical or non-canonical candidate language. They confer no
   ownership and authorize no contract or implementation.

---

## 6. Final Verdict

**Verdict: `REJECT`.**

**Portfolio Policy is not admissible as a canonical composite noun under any
proven constitutional owner.**

Decision Intelligence already owns the candidate's policy-envelope and
portfolio-constraint meaning through Decision Policy and Portfolio Limits.
The remaining grouped meaning has no proven common owner. Portfolio
Intelligence, Ledger & Accounting, Asset Foundation, every other existing
domain, and any speculative future domain therefore fail the single-owner
test for the whole.

M42-WP4 must not proceed to contract design. Its blocked state is resolved by
rejection, and this investigation creates no authority beyond that verdict.

**Final status:** `COMPLETE — REJECT`

The rejection occurred at the ownership/admission gate and is permanent for
M42-WP4. It authorizes no contract-design stage.
