# BANPU-WP1 — Constitutional Freeze Record

**Artifact class:** Additive constitutional freeze record
**Freeze date:** 2026-08-06
**Disposition:** `FROZEN WITH RECORDED RESIDUALS`
**Frozen work package:** `BANPU-WP1 — Persistence and canonical contract`
**WP2 authority created:** `NONE`

## 1. Freeze authority

Acting solely as the BANPU-WP1 Freeze Authority, this act freezes the exact
confirmed implementation candidate identified in §4. Authority derives from
the completed BANPU-WP1 confirmation, the completed freeze-readiness
assessment, and the Architecture Owner's instruction to perform the
constitutional freeze after the authoritative Renewed Independent Review
returned `APPROVED WITH RECORDED RESIDUALS`.

This authority is limited to identity binding, corpus-boundary verification,
residual carry-forward, and creation of this record. It grants no authority to
implement, allocate, authorize, or begin BANPU-WP2 or any later package.

## 2. Freeze basis

The freeze rests on the following lifecycle evidence:

- [BANPU-WP1 Confirmation](BANPU_WP1_CONFIRMATION.md), disposition
  `CONFIRMED WITH RECORDED RESIDUALS`;
- [BANPU-WP1 Freeze Readiness Assessment](BANPU_WP1_FREEZE_READINESS_ASSESSMENT.md),
  disposition `READY FOR CONSTITUTIONAL FREEZE`;
- the authoritative Renewed Independent Review of RC3, disposition
  `APPROVED WITH RECORDED RESIDUALS`; and
- the synchronized canonical design, roadmap, and mandatory sequence listed
  in §4.

The renewed review was supplied as authoritative external governance evidence;
no separate renewed-review file exists in the repository. Its verdict, RC1–RC3
history, governance findings, and residual dispositions are recorded in the
confirmation artifact. This freeze does not invent a repository identity for
an external artifact.

## 3. Implementation candidate

The frozen candidate is WP1 Repair Candidate 3 plus its approved governance
closure. It contains only:

- additive transaction persistence for `conversion_payload`;
- the named conversion-specific identity/date constraint and retained partial
  unique index;
- PostgreSQL/Alembic, ORM, and legacy SQLite compatibility behavior;
- the immutable typed version-1 payload parser, deterministic errors, exact
  Decimal values, and canonical typed-value fingerprinting;
- focused canonicalizer and migration tests;
- authoritative transaction-vocabulary corrections; and
- the synchronized canonical design, roadmap, sequence, confirmation, and
  readiness artifacts.

No conversion replay, validator, live write path, registry materialization,
market-data protection, snapshot behavior, CLI, frontend, production-data
mutation, or M46 change is included.

## 4. Frozen corpus identity

The frozen implementation corpus contains exactly 12 files. Each SHA-256 is
computed from the binary working-tree bytes on 2026-08-06 before this lifecycle
record was added.

| # | Frozen artifact | Bytes | Physical lines | SHA-256 |
|---|---|---:|---:|---|
| 1 | `backend/models/database.py` | 72,515 | 1,222 | `377D008E68B973F5DA2F56CE12EF890719746AB2BEFBB9B44926BA467839F6C3` |
| 2 | `backend/services/transaction_canonicalizer.py` | 31,416 | 728 | `59339DCBAF1BF7838BE0E472F562C9BCCACE0990598A564301F5F0BD3BE4560E` |
| 3 | `backend/migrations/versions/b7d9f1a3c5e7_add_position_conversion_payload.py` | 4,214 | 121 | `0983345189FA567E527D7336D2D2DF6C51ACF5A1EE13FF4F301B55B832DED66E` |
| 4 | `backend/tests/test_transaction_canonicalizer.py` | 25,881 | 734 | `FB91E7B7632ACC58B3A0CA1511997726F2F748FBEFFC81ACA01E9BDAA65F8942` |
| 5 | `backend/tests/test_position_conversion_migration.py` | 15,126 | 427 | `7B2ED020E9BEDAC814B655426D1641A58810737788C35169FECC48686EF8D636` |
| 6 | `docs/architecture/ARCHITECTURE.md` | 25,328 | 525 | `DFFE081EDF166CAE9DA3B585725A22B40BABCD3E5F5D15003B7EE1627F8FEA2F` |
| 7 | `docs/investment/PORTFOLIO_CALCULATION_RULES.md` | 45,125 | 392 | `9BF323803F618CB210E1CE97E104B13CBB329F29672D1984570939E701E3718D` |
| 8 | `docs/implementation/BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` | 28,179 | 474 | `7EE5300D1251A845FB9FD626076ED03FC77307117F7CFB7731B152D68500DE60` |
| 9 | `docs/implementation/BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md` | 22,264 | 588 | `00DCE62C85FC39673584CB05F75CF14E6A0F3C40AFE6D034E81814C4C223EE6B` |
| 10 | `docs/implementation/BANPU_IMPLEMENTATION_SEQUENCE.md` | 13,568 | 356 | `43207FE0EFB12872583711B8320A29A64CC72A58ED3E07473C5A19C482C068BA` |
| 11 | `docs/implementation/BANPU_WP1_CONFIRMATION.md` | 5,129 | 95 | `A52C9C2F805FE52FB53A5C3927C5A589B9D882FF4A1421155F5000910FD658D1` |
| 12 | `docs/implementation/BANPU_WP1_FREEZE_READINESS_ASSESSMENT.md` | 3,577 | 66 | `76B7CA036C7E8457C40CEAB2ACEB4053177A11BD756F95BB3EAD0EF5854E8425` |

Corpus cardinality: `12`. Missing artifacts: `0`. Unauthorized included
artifacts: `0`.

The deterministic corpus manifest is the listed repository-relative paths in
table order, each encoded as `path<TAB>SHA256<TAB>bytes<LF>` in UTF-8. Its
aggregate identity is:

```text
56478CB0A4312314724DD81D90A9FAE852434C2156BD47B5FED141296E0578A9
```

This freeze record is a lifecycle artifact and is not a member of the frozen
12-file implementation corpus it identifies.

## 5. Confirmation-to-candidate verification

| Verification | Result |
|---|---|
| Confirmation describes the frozen candidate | `SATISFIED` — every implementation capability listed in Confirmation §2 maps to the model, canonicalizer, migration, or focused tests in §4 |
| Confirmation exclusions match the candidate | `SATISFIED` — no replay, validator, live write path, market-data, snapshot, CLI, frontend, production-data, or M46 diff exists |
| Architecture Owner decision is preserved | `SATISFIED` — the corpus retains the named conversion constraint, naive-midnight business date, mandatory predecessor asset ID, and unchanged partial unique index |
| Independent review disposition is preserved | `SATISFIED` — the confirmation and canonical residual register both record `APPROVED WITH RECORDED RESIDUALS` |
| No open implementation finding remains | `SATISFIED` — MAJOR-1 is closed by RC3 and no renewed-review finding requires further WP1 implementation |

## 6. Canonical synchronization verification

| Canonical artifact | Frozen state | Result |
|---|---|---|
| Implementation design | WP1 complete, independently approved and confirmed with residuals; freeze pending at the instant before this act | `SYNCHRONIZED` |
| Work-package roadmap | WP1 complete and confirmed; WP2 blocked until freeze | `SYNCHRONIZED` |
| Mandatory sequence | RC3 and the renewed-review result recorded; Step 2 not started and freeze-gated | `SYNCHRONIZED` |

The pre-freeze wording is preserved as part of the confirmed identity. This
freeze record is the constitutional state transition; changing the already
confirmed canonical bytes merely to replace “freeze pending” would invalidate
the confirmed corpus and is neither required nor authorized by this act.

## 7. Recorded residuals

The following remain frozen as explicit future-package verification gates, not
open WP1 findings:

| Finding | Frozen disposition | Responsible future package | Required verification |
|---|---|---|---|
| `MINOR-1` | Deferred precision improvement | WP4, before fingerprint-based idempotency is active | Distinct payload fingerprints beyond 28 significant digits plus retry/conflict tests |
| `MINOR-2` | Deferred consumer-domain validation | WP3 for reference prices; WP5 for mechanical tolerance | Focused rejection tests before either value is consumed |
| `MINOR-5` | Accepted PostgreSQL execution-verification residual | WP7 rehearsal; WP8 release evidence | Real PostgreSQL upgrade, repeated upgrade, constraint/index probes, and guarded downgrade |
| `NEW-MINOR-A` | Accepted PostgreSQL typed-storage/coercion residual | WP4 authoring; WP7 production-dialect rehearsal | Naive-midnight authoring and payload/date equality tests, followed by real PostgreSQL coercion/stored-invariant probes |

`NEW-MINOR-B` and Renewed Review Observation 1 are resolved governance
findings and are not residuals.

## 8. Freeze scope

This freeze makes the identities and WP1 decisions in §4 immutable unless a
separately authorized constitutional amendment explicitly reopens WP1. It
freezes:

- the version-1 persistence and canonical payload contract;
- the approved Alternative 3 database invariant;
- PostgreSQL/SQLite compatibility behavior in the candidate;
- WP1 acceptance and focused verification evidence;
- the four recorded residual dispositions and their future verification gates;
- the WP1/WP2 boundary and the prohibition on implicit successor authority.

## 9. Freeze exclusions

This act does not:

- authorize, allocate, or begin WP2;
- implement replay, validator, live materialization, registry, quote, snapshot,
  shadow, CLI, frontend, deployment, or production behavior;
- resolve or waive any recorded residual;
- commit, push, deploy, migrate, or mutate production data;
- alter M46 or create general corporate-action machinery; or
- perform any post-freeze work.

## 10. Exact repository state

The freeze was prepared on branch `feature/m46-banpu-remediation` at baseline
HEAD `451ab8529567076eb8836e20e6c632956b2de675`.

At the final freeze check, the 12 frozen corpus files and this freeze record are
the complete staged BANPU-WP1 candidate. There are no unstaged or untracked
WP1 candidate files. Graph output is synchronized by `graphify update .` and
remains repository-ignored. No commit is created by this act.

## 11. Freeze verification

| Required verification | Result |
|---|---|
| Confirmation matches frozen candidate | `SATISFIED` |
| Canonical documents synchronized | `SATISFIED` |
| Implementation corpus internally consistent | `SATISFIED` |
| No WP2 implementation exists | `SATISFIED` |
| Residuals remain recorded | `SATISFIED` |
| Graph synchronized | `SATISFIED` — final command evidence recorded after creation of this artifact |
| Repository ready to freeze | `SATISFIED` — final diff and status evidence recorded after staging |

## 12. Freeze disposition

**BANPU-WP1 is `FROZEN WITH RECORDED RESIDUALS` at the corpus identity in §4.**

BANPU-WP2 remains constitutionally blocked. This freeze supplies no WP2
allocation, authorization, or implementation authority. No post-freeze work is
performed under this act.
