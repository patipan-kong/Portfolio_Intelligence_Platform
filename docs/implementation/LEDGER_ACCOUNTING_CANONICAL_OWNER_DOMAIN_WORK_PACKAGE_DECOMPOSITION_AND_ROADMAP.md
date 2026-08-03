# Ledger & Accounting — Canonical Owner-Domain Work-Package Decomposition and Roadmap

**Artifact class:** Owner-domain roadmap planning candidate  
**Status:** `PLANNING CANDIDATE — NOT RATIFIED`  
**Revision:** `RC1` — additive successor candidate correcting `LA-IR-001` only  
**Correction basis:** [Ledger & Accounting Planning Corpus — Independent Architecture Review](LEDGER_ACCOUNTING_ARCHITECTURE_INDEPENDENT_REVIEW.md), finding `LA-IR-001`  
**Paired plan:** [Ledger & Accounting Architecture and Implementation Plan](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)  
**Authority granted by this document:** `NONE`

This roadmap is independent of M45. It creates no M45 work package, does not
allocate M45-WP2, and gives M45 no authority over Ledger work.

## 1. Delivery model

The objective is a lifecycle-complete, immutable Ledger-owned evidence package
that a future external consumer can evaluate without interpreting or repairing
it. Documentary implementation below means canonical governance artifacts,
never source code, runtime behavior, schemas, persistence, APIs, or production
methods.

| WP | Purpose and bounded deliverable | Dependencies | Completion / fail-closed boundary |
| --- | --- | --- | --- |
| LA-WP1 | Authority, baseline, and semantic non-amendment register. Locks Platform Architecture, Glossary, M42-WP2, and M44 G-3 criteria by exact identity. | Owner-domain allocation; planning corpus frozen; explicit WP authorization | `FROZEN BASELINE` or `BLOCKED`; no artifact form is authored here |
| LA-WP2 | Portfolio Identity and Accounting Scope canonical reference forms (LA-1, LA-2), each with its own package-local vector annex. | Frozen LA-WP1 | Both forms and their annexes independently frozen together, or a frozen blocked determination |
| LA-WP3 | Portfolio Membership canonical representation (LA-3) with its package-local cardinality and boundary vector annex. | Frozen LA-WP1; LA-WP2 identities cited for coherent portfolio references | Form and annex independently frozen together, or a frozen blocked determination |
| LA-WP4 | Portfolio Base Currency coordinate reference form (LA-4) with its package-local temporal change-history and negative vector annex. | Frozen LA-WP1; exact Asset Foundation denominator-form identity available for citation | Form and annex independently frozen together, or a frozen blocked determination; never supplies an Asset form |
| LA-WP5 | Ledger Base Currency compatibility attestation (LA-5). | Frozen LA-WP4; lifecycle-complete Asset Foundation denomination identifier form | Independently frozen Ledger-side evidence, or a frozen external-dependency block |
| LA-WP6 | Ledger evidence manifest (LA-6) and aggregated conformance vector corpus (LA-7), assembled only by immutable citation, indexing, and completeness verification of the already-frozen LA-1 through LA-4 vector annexes. | Frozen LA-WP2 through LA-WP5 | Independently frozen manifest and aggregated corpus, or a frozen incomplete-supply determination; no vector is authored, altered, or substituted here |
| LA-WP7 | Release attestation and owner-domain closeout (LA-8). | Frozen LA-WP6; revalidated cited identities | `RELEASE ATTESTED` or `NOT RELEASE ATTESTED`, plus truthful closeout |

Each WP requires its own allocation and authorization after the planning
corpus is ratified and frozen. No downstream WP starts from a draft,
unconfirmed, or merely reviewed predecessor.

## 2. Work-package rules

### LA-WP1 — baseline control

- Enumerates controlling facts and exact identities; it does not reinterpret
  M42-WP2 or M45.
- Must explicitly distinguish established semantics from missing canonical
  representation.
- Its exit condition is a reviewed, confirmed, content-identified freeze.

### LA-WP2 through LA-WP4 — owner-form authoring

- Each artifact fixes grammar, required and forbidden fields, encoding,
  ordering, cardinality, affirmative absence, error/invalid-state treatment,
  and positive/boundary/negative vectors.
- Those vectors constitute the artifact's package-local vector annex. The annex
  is authored, independently reviewed, independently confirmed,
  content-identified, and frozen inside this work package together with its
  parent form. Vector authoring is never deferred to LA-WP6.
- The frozen annex bytes are the sole lawful vector supply for that form. A
  later new or changed vector is a change to the form's own artifact and
  requires reopening that artifact's successor lifecycle here, not in LA-WP6.
- Forms may cite existing canonical vocabulary only at its frozen meaning.
- LA-WP4 may carry an opaque reference to an Asset Foundation denomination
  identifier; it must not define its lexical syntax or enumerate values.

### LA-WP5 — Ledger-side compatibility without co-ownership

- Has no power to alter either owner artifact.
- Verifies only that LA-4 can reference the cited Asset Foundation form exactly
  and that the Ledger coordinate participates in one Base Currency element.
- Does not attest that the Asset Foundation form is semantically sufficient;
  that determination remains with Asset Foundation and a future consumer's
  lawful intake assessment.
- An absent, incompatible, unreviewed, or unfrozen Asset form terminates in a
  frozen external-dependency block; Ledger may not manufacture a substitute.

### LA-WP6 — packaging and determinacy

- Produces a manifest mapping each Ledger form to lifecycle records and exact
  immutable identities.
- Assembles LA-7 solely by immutable aggregation: it cites each frozen LA-1
  through LA-4 vector annex by exact identity, indexes it, and verifies that
  coverage is complete. It creates no vector content.
- Must never author, normalize, repair, expand, replace, reorder, or modify a
  vector, and must never supply a substitute for a missing, defective, or
  unfrozen annex. The aggregated vectors remain documentary evidence, not a
  runtime test suite or implementation grant.
- If a new or changed vector is required, LA-WP6 stops. The vector must be
  introduced through the successor lifecycle of the affected canonical
  artifact and frozen there before LA-WP6 may cite it or attest completeness.
- Fails closed if any required form, lifecycle record, identity, or frozen
  vector annex is absent.

### LA-WP7 — release and closeout

- Revalidates that all cited frozen bytes still resolve and that no successor
  has invalidated the manifest.
- May issue `RELEASE ATTESTED` only when every condition in the paired plan
  §7 passes. Otherwise it issues `NOT RELEASE ATTESTED` with exact blockers.
- Does not close G-3, decide a downstream consumer's allocation, or convert
  the external consumer's needs into Ledger authority.

## 3. Governance gates and roadmap

```text
G0  Competent owner-domain allocation
 |   (if absent: milestone remains uncommissioned)
 v
G1  Independent plan review -> confirmation -> ratification -> joint freeze
 |   (if any fails: planning remains non-normative)
 v
G2  Separate authorization of LA-WP1
 v
LA-WP1 frozen baseline
 |\
 | +--> LA-WP2 frozen --+
 | +--> LA-WP3 frozen --+--> LA-WP6 frozen --> LA-WP7 release attestation
 | +--> LA-WP4 frozen --+              ^
                         \             |
                          +-> LA-WP5 ---+
                               ^
                               |
                 external frozen Asset Foundation form
```

Recommended sequencing is LA-WP1, then LA-WP2 and LA-WP3, then LA-WP4,
LA-WP5, LA-WP6, and LA-WP7. LA-WP2 and LA-WP3 may be independently scheduled
only if their authorization records expressly permit parallel work and both
still cite the same frozen LA-WP1 baseline. Calendar dates are intentionally
absent: authority and evidence, not schedule, release each stage.

## 4. Review protocol

Every substantive candidate is checked independently for:

1. competent authorization and exact scope;
2. non-amendment of established Ledger, Asset Foundation, and Portfolio
   Intelligence semantics;
3. complete canonical-form determinacy, including no ambient defaults;
4. identity, scope, membership, and Base Currency boundary invariants;
5. opacity and non-substitution of cross-domain inputs;
6. compatibility with the one Base Currency evidence-matrix entry; and
7. absence of implementation, runtime, or M45 authority claims.

Findings are corrected only through an additive candidate revision and a
focused independent re-review. A confirmation and content-identity validation
are required before any freeze.

## 5. Terminal states and handoff

| Terminal state | Meaning | Permitted handoff |
| --- | --- | --- |
| `RELEASE ATTESTED` | All Ledger forms and Ledger-side Base Currency evidence have lifecycle-complete, immutable supply | An external consumer may independently verify and cite the exact evidence |
| `NOT RELEASE ATTESTED` | One or more Ledger release conditions failed | Exact blocker only; no substitute artifact |
| `BLOCKED — EXTERNAL ASSET FORM` | Asset Foundation form is absent, defective, or not lifecycle-complete | No Base Currency joint-evidence claim |
| `BLOCKED — GOVERNANCE` | Allocation, authorization, review, confirmation, or freeze is absent | No canonical supply claim |
| `SUPERSEDED` | A later frozen Ledger form replaces a cited revision | Consumers must re-verify the current applicable revision |

A `RELEASE ATTESTED` handoff is deliberately narrow. It establishes Ledger
evidence availability, not G-3 closure, M45-WP2 allocation, M45-WP2
authorization, or the adequacy of the other owner domains' artifacts.
