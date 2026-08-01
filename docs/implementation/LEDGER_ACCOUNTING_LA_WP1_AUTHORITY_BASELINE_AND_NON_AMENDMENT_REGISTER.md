# Ledger & Accounting — LA-WP1 Authority, Baseline, and Non-Amendment Register

**Artifact class:** LA-WP1 documentary implementation candidate
**Candidate date:** 2026-08-01
**Status:** `IMPLEMENTATION CANDIDATE — NOT REVIEWED, CONFIRMED, OR FROZEN`
**Revision:** `RC4`
**Correction basis:**

- [LA-WP1 Final Focused Independent Re-review (RC3)](LEDGER_ACCOUNTING_LA_WP1_FINAL_FOCUSED_REREVIEW_RC3.md)
- **Finding:** `LA-WP1-FFR3-001`

**Implementation authority:** LA-WP1 only
**Authority source:** [LA-WP1 Authorization Record](LEDGER_ACCOUNTING_LA_WP1_AUTHORIZATION_RECORD.md)
**Downstream authority granted by this candidate:** `NONE`

## 1. Candidate purpose and boundary

This candidate implements only the documentary baseline assigned to LA-WP1 by
the frozen [Ledger & Accounting Work-Package Decomposition and Roadmap](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md).
It records authority, the frozen planning baseline, inherited semantics,
owner-domain boundaries, implementation prohibitions, and the documentary
entry conditions for a possible future LA-WP2.

This candidate does not author a canonical Ledger form. It does not complete
independent review, confirmation, content-identity validation, freeze, or
closeout. Its creation therefore does not establish the LA-WP1 terminal state
`FROZEN BASELINE` and does not permit LA-WP2 to begin.

Under the frozen roadmap, the only lawful LA-WP1 terminal states are `FROZEN
BASELINE` and `BLOCKED`. `BLOCKED` is a truthful fail-closed terminal state
under the frozen plan §5 and does not permit LA-WP2 entry.

## 2. Authority verification register

### 2.1 Planning corpus identity

The canonical planning corpus is the following inseparable, jointly ratified
and jointly frozen pair. The identities observed for this implementation match
the identities recorded by the [Planning Freeze](LEDGER_ACCOUNTING_PLANNING_FREEZE.md)
exactly.

| Frozen planning artifact | Recorded and observed Git blob ID | Recorded and observed SHA-256 | Verification |
| --- | --- | --- | --- |
| [Canonical Owner-Domain Architecture and Implementation Plan](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | `6e68ab3e3f152d105e72bef4f84cd7c4afae9e1a` | `c6ac324a786953dec79d89363a712df07fcb190f7bdd93a635a97bcdb2fd595f` | `MATCH` |
| [Canonical Owner-Domain Work-Package Decomposition and Roadmap](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) | `b812e31cb0473c16c324419e1efb6103af1e274a` | `eca5abc8e1a7fbfff7ca9f6c4e7e09479f93df3d73748cad936874574bb3ccfa` | `MATCH` |

Neither artifact is independently canonical or frozen outside this pair.
LA-WP1 does not amend, reinterpret, or supersede either artifact.

### 2.2 Planning freeze verification

| Required planning fact | Controlling evidence | Verified state |
| --- | --- | --- |
| Planning governance complete | [Planning Closeout](LEDGER_ACCOUNTING_PLANNING_CLOSEOUT.md), disposition `COMPLETE` | `VERIFIED` |
| Planning baseline canonical | [Planning Ratification](LEDGER_ACCOUNTING_PLANNING_RATIFICATION.md), disposition `RATIFIED` | `VERIFIED` |
| Planning baseline frozen | [Planning Freeze](LEDGER_ACCOUNTING_PLANNING_FREEZE.md), disposition `FROZEN` | `VERIFIED` |
| Planning epic closed | [Planning Epic Closeout](LEDGER_ACCOUNTING_PLANNING_EPIC_CLOSEOUT.md), disposition `COMPLETE`; status `CANONICAL`, `FROZEN`, `CLOSED` | `VERIFIED` |
| Frozen bytes unchanged | Both planning artifacts match the freeze-recorded identities in §2.1 | `VERIFIED` |

The freeze grants no implementation authority. It is a prerequisite to, not a
substitute for, work-package allocation and authorization.

### 2.3 Allocation verification

| Item | Verification |
| --- | --- |
| Record | [LA-WP1 Allocation Record](LEDGER_ACCOUNTING_LA_WP1_ALLOCATION_RECORD.md) |
| Disposition | `ALLOCATED` |
| Scope | LA-WP1 allocation only |
| Observed Git blob identity | `0711b9e3526d44dfae85b2c478f02965c4e40039` |
| Observed SHA-256 | `62d04056c3c2e8b14fb2b53a1c634f4181fb117edcf455040378c24675d6ae8f` |
| Result | `VERIFIED` |

The observed identities identify the authority evidence read by this
candidate. They do not independently freeze or enlarge that record. Allocation
alone granted no implementation authority.

### 2.4 Authorization verification

| Item | Verification |
| --- | --- |
| Record | [LA-WP1 Authorization Record](LEDGER_ACCOUNTING_LA_WP1_AUTHORIZATION_RECORD.md) |
| Disposition | `AUTHORIZED` |
| Scope | LA-WP1 only |
| Observed Git blob identity | `85ce59909c538c441fd96854e2520aa514ac4af3` |
| Observed SHA-256 | `4d65d34e3886e48e237eac166658b6d255a44e72957aa292f530b77d29c7d35b` |
| Result | `VERIFIED` |

The observed identities identify the authority evidence read by this
candidate. They do not independently freeze or enlarge that record.

### 2.5 Implementation authority boundary

The verified authority permits the LA-WP1 implementation author to draft only
this documentary implementation candidate. It grants no authority to review,
confirm, content-identify, freeze, or close this candidate; to implement any
later Ledger work package; or to act for another owner domain or M45.

No authority exists under LA-WP1 for LA-WP2 through LA-WP7. No downstream need,
document label, authorship act, or silence expands this boundary.

## 3. Frozen baseline register

The exact frozen planning baseline governing LA-WP1 and every successor Ledger
work package is the pair in §2.1. Its immutable identities are repeated below
as the inheritance lock for clarity.

| Baseline member | Git blob ID | SHA-256 | Inherited control |
| --- | --- | --- | --- |
| [Architecture and Implementation Plan](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | `6e68ab3e3f152d105e72bef4f84cd7c4afae9e1a` | `c6ac324a786953dec79d89363a712df07fcb190f7bdd93a635a97bcdb2fd595f` | Constitutional scope, ownership, artifacts, authority, lifecycle, dependencies, release boundary, and exclusions |
| [Work-Package Decomposition and Roadmap](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) | `b812e31cb0473c16c324419e1efb6103af1e274a` | `eca5abc8e1a7fbfff7ca9f6c4e7e09479f93df3d73748cad936874574bb3ccfa` | LA-WP1 through LA-WP7 scope, dependencies, package rules, gates, terminal states, and handoff boundaries |

The planning corrections response, reviews, confirmation, content-identity
validation, ratification, freeze, and closeout records remain governance
evidence. Consistent with the Planning Freeze, they are not additional frozen
planning specifications.

No later Ledger work package may replace either baseline member by inference,
current repository preference, or downstream convenience. A different
planning baseline requires a governed successor planning lifecycle.

## 4. Semantic non-amendment register

### 4.1 Direct inherited sources locked by LA-WP1

These are the exact direct sources the frozen roadmap requires LA-WP1 to lock.
Their identities fix the source bytes inherited by this candidate; recording
an identity does not grant LA-WP1 authority to amend or re-freeze its source.

| Inherited source | Git blob ID | SHA-256 | Authority inherited without amendment |
| --- | --- | --- | --- |
| [Platform Architecture](../architecture/platform_architecture.md), especially §6.3 | `e9164fe75e306035321858c58039922b8ec9584c` | `c8c843ac4abcee862c900b8247a777611dd6adfee336db936c4eecc361a0bf3c` | Constitutional Ledger & Accounting ownership of financial truth, accounting boundaries, deterministic replay, and accounting semantics; domain boundaries and dependency law |
| [Canonical Glossary](../GLOSSARY.md) | `a43010dbaf40b15e2dbb7c9c8ba59bda3d7d6990` | `0f82f22fb3c7394ae4dda73c3d9ca0800ab9d1a4254f6a3adc8aeccebf897dbb` | Canonical meanings and owner mappings for Portfolio Identity, Accounting Scope, Portfolio Membership, and Portfolio Base Currency |
| [M42-WP2 Portfolio Identity, Accounting Scope, Membership & Base Currency Contract Specification](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md) | `f9b06f6ca3eb20bf2bc2a8678eda3fbceac45db0` | `4b3cc23368aac24aedd1c16b4687765045ebdcba2315a4c7cc9d8bf0f5692d39` | Confirmed semantic contract, boundary invariants, ownership preservation, Base Currency coordinate, and event-sourced non-retroactive change |
| [M44 G-3 Closure and WP6-Entry Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) | `e29e09efd4a1fa4a8aaeb47e04df35c6fc66f044` | `d82796c38c8f56abb1116cf80c3e89bd67e1fd5bee32a3109b9c7d617ed863f9` | Frozen G-3 evidence criteria, owner routing, source-owner lifecycle, exactness and written-form determinacy requirements, and the unchanged `G-3 OPEN — PARTIAL` state |

The M44 roadmap Git blob matches the identity recorded by its
[Freeze Record](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP_FREEZE_RECORD.md).
The M42 semantic contract belongs to the approved M42 corpus recorded as
canonical and frozen by the [M42 Epic Closeout](M42_EPIC_CLOSEOUT.md).

### 4.2 Inherited semantic authority lineage

| Semantic subject | Inherited authorities | LA-WP1 non-amendment determination |
| --- | --- | --- |
| Portfolio Identity | Platform Architecture §6.3; Canonical Glossary; [M34 Decision Register](m34/audit/registers/decision_register.md) `M34-D-0002`; M42-WP2 §§5.1 and 5.6 | Meaning and Ledger ownership are inherited exactly; no field, exception, strategy, goal, policy, analytics, UI, or alternate identity meaning is added |
| Accounting Scope | Platform Architecture §6.3; Canonical Glossary; M34 Decision Register `M34-D-0002`; M42-WP2 §§5.2 and 5.4–5.6 | The single accounting boundary and no-cross-boundary replay rule are inherited exactly; no second scope or exception is created |
| Portfolio Membership | Platform Architecture §6.3; Canonical Glossary; M34 Decision Register `M34-D-0003`; M42-WP2 §§5.3–5.6 | The Ledger fact and one-or-more-scope cardinality are inherited exactly; no investment-universe, exposure, or recommendation meaning is added |
| Portfolio Base Currency | Platform Architecture §6.3; Canonical Glossary; [M42-WP1 Vocabulary and Ownership Register](M42_WP1_PORTFOLIO_CANONICAL_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §6.4; M42-WP2 §6 | The single explicit Ledger-owned coordinate, Asset Foundation-owned denomination dimension, and prospective-only event history are inherited exactly; no identifier form, rate, conversion, NAV, benchmark, default, or retroactive meaning is added |

The inherited M34 Decision Register bytes are identified by Git blob
`80b87b7bd4dc8567834be3f2c5efa4dbffcacfd4` and SHA-256
`1b067a83d429f0175bcf1aae7c180bf39399ac967a55cb157038a6566336aa53`.
The inherited M42-WP1 register bytes are identified by Git blob
`8808ead827f9ac703e358b9ed7643eb0d5afd616` and SHA-256
`31de9ab92d9495ca841ec8b388f3ced7aa7299839d40ff451673c1e4f2e0f22d`.

### 4.3 Explicit semantic non-amendment declaration

LA-WP1 does not redefine Portfolio Identity, Accounting Scope, Portfolio
Membership, or Portfolio Base Currency. LA-WP1 distinguishes those established
semantics from the canonical written forms that the M44 G-3 criteria record as
missing. Recording that representation gap neither fills it nor changes the
underlying meanings.

## 5. Owner-boundary register

| Domain | Preserved ownership | LA-WP1 boundary |
| --- | --- | --- |
| Ledger & Accounting | Financial truth; the immutable event record; accounting boundaries; deterministic replay; accounting semantics; Portfolio Identity; Accounting Scope; Portfolio Membership; the Portfolio Base Currency coordinate | LA-WP1 records this ownership only. It creates none of LA-1 through LA-8 and exercises no runtime authority. |
| Asset Foundation | The denomination identifier dimension referenced by the Portfolio Base Currency coordinate, including its canonical form | LA-WP1 does not author, normalize, substitute, version, confirm, freeze, or attest an Asset Foundation form. |
| Connectivity & Ingestion | Provenance capture content, representation, supplied sequence, and completeness basis | LA-WP1 creates no Provenance form and no Connectivity & Ingestion authority. |
| Portfolio Intelligence | Its nested canonical forms, including Investment Universe and Benchmark forms, and its derived-measure meanings | LA-WP1 does not define, repair, infer, select, or authorize Portfolio Intelligence content. |

Portfolio Base Currency remains one jointly evidenced but not jointly owned
element: Ledger & Accounting owns its coordinate, while Asset Foundation owns
the denomination identifier dimension. LA-WP1 creates no co-ownership,
ownership transfer, cross-domain artifact, cross-domain authorization, or
cross-domain implementation authority.

## 6. Implementation prohibition register

LA-WP1 expressly does not:

- author LA-1, LA-2, LA-3, LA-4, LA-5, LA-6, LA-7, or LA-8;
- define any canonical Ledger grammar, field set, encoding, ordering,
  cardinality, absence representation, or conformance vector;
- implement or activate runtime behavior;
- create or modify source code, schemas, APIs, persistence, providers,
  migrations, production methods, executable fixtures, or UI behavior;
- modify the canonical frozen planning baseline or any inherited semantic
  authority;
- modify M45 or any M45 artifact, allocate or authorize M45-WP2, or grant M45
  authority over Ledger work;
- determine, reopen, close, or change G-3;
- create an Asset Foundation, Connectivity & Ingestion, or Portfolio
  Intelligence artifact;
- allocate, authorize, begin, review, confirm, content-identify, freeze, or
  close LA-WP2 through LA-WP7; or
- treat this implementation candidate as reviewed, confirmed, frozen,
  released, or sufficient downstream supply.

## 7. Successor implementation entry register

LA-WP2 may begin only after every documentary prerequisite below exists and is
truthfully satisfied. The prerequisites are conjunctive; no item substitutes
for another.

This implementation candidate records only implementation content. Current
lifecycle progression for LA-WP1 is established exclusively by the applicable
additive LA-WP1 governance records. This register
therefore preserves the implementation prerequisites and identifies their
authoritative evidence sources without attempting to mirror current governance
progress.

| # | Required documentary prerequisite before LA-WP2 begins | Required evidence or state | Authoritative evidence source; not current lifecycle status |
| --- | --- | --- | --- |
| 1 | LA-WP1 candidate completed within its authorized scope | This implementation candidate organizes the required roadmap obligations using six registers and authors no canonical form | This implementation candidate |
| 2 | Independent LA-WP1 review completed | A separate independent review of authority, scope, exact identities, semantic non-amendment, owner boundaries, prohibitions, successor gates, links, and repository hygiene; no blocking finding unresolved | Applicable additive LA-WP1 independent-review record |
| 3 | LA-WP1 corrections and focused re-review completed if required | Additive correction candidate and separate focused re-review for every review finding | Applicable additive LA-WP1 corrections-response and focused-re-review records |
| 4 | Independent LA-WP1 confirmation completed | Separate confirmation of the exact reviewed candidate and resolution of every required finding | Applicable additive LA-WP1 independent-confirmation record |
| 5 | LA-WP1 content identity validated | Exact Git blob and SHA-256 identities for the confirmed LA-WP1 bytes, with repository-relative links and hygiene results recorded | Applicable additive LA-WP1 content-identity-validation record |
| 6 | LA-WP1 frozen | Separate freeze record, as required by the frozen plan §5, records the content hash, repository identity, authority source, predecessor identities, supersession relationship, and terminal state `FROZEN BASELINE` | Applicable additive LA-WP1 freeze record |
| 7 | LA-WP2 independently allocated | A competent allocation record names LA-WP2 and LA-WP2 only | Applicable additive LA-WP2 allocation record |
| 8 | LA-WP2 separately authorized | A competent authorization record, distinct from allocation, authorizes LA-WP2 and LA-WP2 only | Applicable additive LA-WP2 authorization record |
| 9 | LA-WP2 entry cites the inherited baseline exactly | LA-WP2 cites the frozen LA-WP1 identity and the unchanged planning and semantic-source identities locked by it | Applicable additive LA-WP2 entry record and its cited frozen identities |

No draft, merely reviewed, unconfirmed, content-unidentified, or unfrozen
LA-WP1 artifact satisfies the dependency. LA-WP2 may not derive allocation or
authorization from this register, the planning baseline, downstream demand,
or the completion of any unrelated owner-domain artifact.

## 8. Candidate implementation validation

The implementation author must validate this candidate's repository-relative
Markdown links, repository working-tree and index hygiene, and own bytes.
`git diff --check` and `git diff --cached --check` describe only repository
working-tree and index hygiene, respectively, for the repository state observed
at each validation event. Their coverage of any particular file depends on the
repository state at that event and is not an immutable property of this
candidate. The dedicated candidate trailing-whitespace scan verifies the
candidate's own bytes independently of repository state. These are
implementation checks only; they are not independent review, confirmation,
content-identity validation, freeze, or closeout.

| Check | Candidate result |
| --- | --- |
| Repository-relative links in this candidate | `PASS` — 22 links checked; 0 broken |
| `git diff --check` | `PASS` — exit `0`; no output; repository working-tree hygiene at the recorded validation event |
| `git diff --cached --check` | `PASS` — exit `0`; no output; repository index hygiene at the recorded validation event |
| Candidate trailing-whitespace scan | `PASS` — 0 lines reported; this dedicated scan verifies the candidate's own bytes |
| Files created by LA-WP1 implementation | This candidate only |
| Canonical Ledger forms created | `NONE` |
| LA-WP2 through LA-WP7 artifacts created | `NONE` |

## 9. Implementation stop

LA-WP1 implementation stops at this candidate. No governance lifecycle act and
no successor work package is performed by this artifact.
