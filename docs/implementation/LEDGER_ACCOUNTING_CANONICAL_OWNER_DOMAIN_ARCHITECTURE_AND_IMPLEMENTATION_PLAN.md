# Ledger & Accounting — Canonical Owner-Domain Architecture and Implementation Plan

**Artifact class:** Owner-domain planning candidate  
**Status:** `PLANNING CANDIDATE — NOT RATIFIED`  
**Revision:** `RC1` — additive successor candidate correcting `LA-IR-001` only  
**Correction basis:** [Ledger & Accounting Planning Corpus — Independent Architecture Review](LEDGER_ACCOUNTING_ARCHITECTURE_INDEPENDENT_REVIEW.md), finding `LA-IR-001`  
**Purpose:** Establish a standalone Ledger & Accounting governance path for canonical-form artifacts.  
**Authority granted by this document:** `NONE`

This is not an M45 artifact, does not amend the frozen M45 planning corpus, and
does not allocate or authorize M45-WP2. M45 is named only as a possible future
external consumer of artifacts completed under this milestone's own lifecycle.

## 1. Constitutional scope

Ledger & Accounting is the owner of financial truth: the immutable event
record, accounting boundaries, deterministic replay, and accounting semantics.
The governing platform boundary is [Platform Architecture §6.3](../architecture/platform_architecture.md#63-ledger--accounting): events refer to
frozen Asset Foundation identities at record time, and replay does not consult
live external authority. The following invariants are non-negotiable:

1. Recorded truth is append-only; a correction is a new auditable event, not
   an overwrite.
2. Every portfolio-scoped fact resolves to exactly one Accounting Scope; replay
   never crosses that boundary.
3. Portfolio Membership records Ledger fact, not investment interpretation or
   exposure meaning.
4. Portfolio Base Currency is one explicit Ledger-owned coordinate per
   Portfolio Identity; its denomination identifier is an Asset Foundation
   dimension. A change is recorded and non-retroactive.
5. Canonical representation is a semantic and byte-determinacy concern. It is
   not a schema, API, provider, UI, migration, or runtime authorization.

The milestone may author canonical *forms* and source-owner evidence for the
four Ledger-owned coordinates below only after its governance gates are met.
It does not reopen their already-canonical meanings, introduce accounting
arithmetic, define FX conversion, or redefine another domain's vocabulary.

## 2. Ownership boundaries

| Subject | Sole semantic owner | This milestone may do | This milestone must not do |
| --- | --- | --- | --- |
| Portfolio Identity | Ledger & Accounting | Define its canonical reference form and proof of written-form determinacy | Add identity semantics, strategy, goal, policy, or UI meaning |
| Accounting Scope | Ledger & Accounting | Define its canonical reference form and boundary evidence | Create a second scope or cross-boundary replay rule |
| Portfolio Membership | Ledger & Accounting | Define its canonical representation and cardinality evidence | Turn membership into an investment-universe, exposure, or recommendation predicate |
| Portfolio Base Currency coordinate | Ledger & Accounting | Define the coordinate's canonical reference form and event-history representation | Define the denomination identifier, a rate, conversion, NAV, or benchmark arithmetic |
| Denomination identifier dimension | Asset Foundation | Cite the frozen Asset Foundation form and jointly verify compatibility | Author, normalize, substitute, or version its form |
| Provenance capture form | Connectivity & Ingestion | Cite it only where lineage is needed | Author capture content, sequence, or completeness basis |
| Portfolio Intelligence nested forms | Portfolio Intelligence | No action | Define, repair, infer, or select Investment Universe or Benchmark forms |

The single Base Currency element is jointly evidenced but not jointly owned:
Ledger & Accounting owns the coordinate that cites an Asset Foundation-owned
denomination identifier. Neither side can claim the element complete alone.

## 3. Canonical artifact inventory

All artifacts below are prospective until independently governed and frozen.
They refine representation, not meaning, of the established terms in
[M42-WP2](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md)
and the [Canonical Glossary](../GLOSSARY.md).

| ID | Canonical artifact | Required content | Owner | Downstream status |
| --- | --- | --- | --- | --- |
| LA-1 | Portfolio Identity Canonical Reference Form | Exact grammar; field set; ordering; encoding; affirmative absence; identity examples and negative vectors in its package-local vector annex | Ledger & Accounting | One Ledger contribution to G-3 |
| LA-2 | Accounting Scope Canonical Reference Form | Exact grammar; scope binding; encoding; ordering; boundary and negative vectors in its package-local vector annex | Ledger & Accounting | One Ledger contribution to G-3 |
| LA-3 | Portfolio Membership Canonical Representation | Subject/reference form; one-or-more scope representation; ordering; duplicate and boundary handling; vectors in its package-local vector annex | Ledger & Accounting | One Ledger contribution to G-3 |
| LA-4 | Portfolio Base Currency Coordinate Canonical Reference Form | Portfolio Identity binding; one Asset Foundation denomination reference; temporal/event-history representation; no rate/value; vectors in its package-local vector annex | Ledger & Accounting | Ledger half of the single joint Base Currency G-3 element |
| LA-5 | Ledger Base Currency Compatibility Attestation | Exact LA-4 identity; exact Asset Foundation denomination-form identity; compatibility matrix proving the Ledger coordinate can cite that dimension as one interoperable element | Ledger & Accounting | Ledger-side evidence only; never ownership transfer or a substitute for Asset Foundation evidence |
| LA-6 | Ledger Owner Evidence Manifest | Mapping from LA-1 through LA-5 to owner, authority, lifecycle records, immutable identities, coverage, and supersession policy | Ledger & Accounting | Intake-ready evidence package |
| LA-7 | Ledger Canonical-Form Conformance Vector Corpus | Immutable aggregation, exact citation, index, and completeness verification of the already-frozen package-local vector annexes of LA-1 through LA-4; contains no independently authored vector content | Ledger & Accounting | Review evidence; not runtime fixtures or implementation authority |
| LA-8 | Ledger Release Attestation | Independent verification that LA-1–LA-7 meet the release profile in §7 | Ledger & Accounting governance | Permits external consumers to assess, never mandates their allocation |

LA-5 may cite an Asset Foundation artifact but cannot create, confirm, or
attest for it. A future consumer must evaluate the two independently frozen
owner evidence streams together. LA-6 and LA-8 are evidence records, not
substitutions for LA-1 through LA-4.

### 3.1 Vector annex lifecycle and the LA-7 production boundary

Conformance vectors are authored and governed with the canonical form they
evidence, never after it. LA-7 is an aggregation artifact, not a vector author.

1. Each of LA-1 through LA-4 carries exactly one package-local vector annex.
   That annex is authored, independently reviewed, independently confirmed,
   content-identified, and frozen inside the same work package and the same
   lifecycle as its parent form. It is never deferred to a later package.
2. The frozen bytes of that annex are the only lawful vector supply for that
   form. Every vector therefore has the same authority source, reviewer,
   confirmer, and freeze identity as the form it evidences.
3. LA-7 is produced solely by immutable aggregation: exact citation of each
   frozen annex identity, indexing, and verification that every required form
   has a complete annex. LA-7 introduces no vector content of its own.
4. The LA-7 producer must never author, normalize, repair, expand, replace,
   reorder, or modify a vector, and must never supply a substitute for a
   missing, defective, or unfrozen annex.
5. A necessary new or changed vector is a change to the affected canonical
   artifact, not to LA-7. It requires reopening that artifact's successor
   lifecycle and freezing a successor annex; only then may LA-7 cite it and
   attest completeness.
6. If a required annex is absent, defective, or unfrozen, LA-7 fails closed and
   records the exact gap. Incomplete vector coverage is never presented as
   complete supply.

This boundary preserves the separation between LA-7 as representation-proof
evidence and LA-8 as aggregate release governance. It changes no ownership, no
dependency ordering, and no other artifact's scope.

## 4. Authority model

No actor obtains authority from authorship, review, confirmation, a document
label, downstream need, or silence. Competent roles must be named by the
allocation or ratification record before acting.

| Role | May | Must not |
| --- | --- | --- |
| Allocating authority | Commission this owner-domain milestone and name its scope | Author the canonical artifacts by implication |
| Planning ratifier / freezer | Ratify and freeze this plan and its roadmap as an identified corpus | Authorize substantive work by implication |
| Work-package author | Draft only the package's authorized artifact set | Self-review, self-confirm, or freeze |
| Independent reviewer | Test constitutional scope, ownership, semantic non-amendment, and serialization completeness | Edit the candidate or declare authority |
| Independent confirmer | Verify resolved findings and exact reviewed content | Ratify or release a downstream consumer |
| Freeze authority | Freeze exact confirmed bytes and record identities | Change content while freezing |
| Release attestor | Verify the release profile and publish LA-8 | Declare G-3 closed, allocate M45-WP2, or certify non-Ledger artifacts |

Ratification is not work-package authorization. Confirmation is not freeze.
Freeze is not runtime or downstream-work authorization.

## 5. Governance lifecycle

Each substantive Ledger artifact (LA-1 through LA-8 where applicable) follows
this fail-closed sequence:

`ALLOCATED` → `AUTHORIZED` → `DRAFT` → `INDEPENDENT REVIEW` →
`CORRECTIONS / FOCUSED RE-REVIEW` (if needed) → `INDEPENDENT CONFIRMATION` →
`CONTENT-IDENTITY VALIDATION` → `FROZEN` → `RELEASE ATTESTATION`.

Required controls:

- Corrections create an additive successor candidate; frozen bytes are never
  edited in place.
- Every freeze records a content hash, repository identity, authority source,
  predecessor identities, and supersession relationship.
- A review finding concerning ownership, an unstated default, live lookup,
  ambiguous ordering, unrepresentable absence, or a cross-domain form is a
  blocking finding.
- A blocked, rejected, or unconfirmed package is a valid terminal result; it
  cannot be represented as supply.
- Material changes to LA-1 through LA-4 require a successor lifecycle and a
  new LA-6 / LA-8 assessment. Consumers must cite exact frozen revisions.

## 6. Dependency graph

```text
Platform Architecture + frozen Glossary + M42-WP2 semantic contract
                              |
                              v
                   Ledger owner-domain planning corpus
                              |
          allocation + ratification/freeze + WP authorization
                              |
               +--------------+--------------+
               |              |              |
               v              v              v
             LA-1           LA-2           LA-3
               \              |              /
                \             v             /
                 +-------- LA-4 -----------+
                              |
      frozen Asset Foundation denomination identifier form
                              |
                              v
                 LA-5 Ledger compatibility attestation
                              |
                              v
                  LA-6 manifest + LA-7 vectors
                              |
                              v
                     LA-8 release attestation
                              |
                              v
         External consumer intake (including, later, M45-WP2)
```

The Asset Foundation input is a hard external dependency for LA-5, not a
Ledger work package. Connectivity & Ingestion Provenance and Portfolio
Intelligence nested forms are outside this graph; their absence does not block
Ledger artifact completion, but it does prevent any consumer from treating the
complete eight-element external evidence set as available.

## 7. Exit criteria for lawful downstream consumption by M45-WP2

M45-WP2 remains unallocated unless and until its own frozen release condition
is met. These are conditions for the Ledger evidence to be *eligible for its
future intake*, not an allocation request or authorization.

Ledger supply is lawful for that intake only when all are true:

1. LA-1, LA-2, LA-3, and LA-4 are exact, immutable, owner-supplied canonical
   forms with complete field and facet determinacy.
2. Each has completed a source-owner lifecycle: expressly allocated and
   authorized work; independent review; independent confirmation;
   content-identity validation; and freeze.
3. LA-4 cites one exact frozen Asset Foundation denomination identifier form,
   and LA-5 proves Ledger-side compatibility without recreating, attesting for,
   or splitting the Asset Foundation form. The consumer must still independently
   verify Asset Foundation's own frozen supply for the one Base Currency element.
4. LA-6 maps every Ledger contribution to its authoritative source, owner,
   lifecycle evidence, immutable identity, coverage, and any successor.
5. LA-7 demonstrates deterministic written form, including ordering,
   encoding, affirmative absence, invalid boundaries, and Base Currency change
   history without a rate, value, default, or retroactive reinterpretation.
6. LA-8 is independently produced and content-identified; it states only
   that Ledger supply meets this profile. It does not close G-3 or determine
   M45 eligibility.
7. The cited bytes and links remain resolvable at intake. A consumer receives
   them opaquely and does not parse, repair, normalize, infer, or substitute
   any owner form.

Even after all seven conditions, M45-WP2 also requires the independently
completed Asset Foundation, Connectivity & Ingestion, and lawfully authorized
Portfolio Intelligence evidence required by its frozen corpus. M45 alone
determines no condition here and has no authority over this lifecycle.

## 8. Explicit exclusions

This milestone does not create Portfolio Intelligence, Asset Foundation, or
Connectivity & Ingestion artifacts; modify any M45 record; determine G-3;
authorize M45-WP2; implement code; change schemas; create APIs; select
providers; produce migrations; or activate accounting behavior.
