# M46-WP1 — Candidate Vocabulary Ownership and Disposition Register

**Artifact class:** Authorized WP1 documentary implementation deliverable 4 of 6

**Authoring role:** M46-WP1 Implementation Author

**Authorization:** [M46-WP1 Authorization Record](M46_WP1_AUTHORIZATION_RECORD.md)

**Disposition:** `AUTHORED — NO VOCABULARY ADMITTED`

**Glossary authority:** `NONE`

---

## 1. Vocabulary rule

Frozen architecture §0 makes every term introduced by M46 a candidate planning
term. This register assigns each candidate label to its semantic owner and
records a disposition. It does not define canonical semantics, amend the
[Glossary](../GLOSSARY.md), or create a private M46 dialect.

Disposition values are:

- `REUSED — OWNER MEANING UNCHANGED`: an existing governed term is referenced
  without amendment;
- `DESCRIPTIVE ONLY — NOT ADMITTED`: usable only as a label inside the frozen
  M46 planning and WP1 evidence corpus;
- `DEFERRED TO OWNER — NOT ADMITTED`: only the named competent owner may admit,
  reject, rename, or replace it in a future authorized contract; and
- `FAIL-CLOSED LABEL — NOT ADMITTED`: documentary failure state only.

## 2. Existing governed terms reused without amendment

| ID | Term | Governing owner/source | WP1 disposition |
| --- | --- | --- | --- |
| `VOC-001` | Asset / `asset_id` | Asset Foundation; [Asset Foundation](../architecture/asset_foundation.md), frozen AF-1 form | `REUSED — OWNER MEANING UNCHANGED` |
| `VOC-002` | Transaction | Ledger & Accounting; [Transaction Domain Model](../architecture/TRANSACTION_DOMAIN_MODEL.md) | `REUSED — OWNER MEANING UNCHANGED` |
| `VOC-003` | Accounting Scope | Ledger & Accounting / Portfolio boundary; [Glossary](../GLOSSARY.md#accounting-scope) | `REUSED — OWNER MEANING UNCHANGED` |
| `VOC-004` | Portfolio Base Currency | Portfolio and Ledger owners; frozen portfolio/accounting contracts | `REUSED — OWNER MEANING UNCHANGED` |
| `VOC-005` | Observation / Observation Identity | Market Intelligence; frozen M39/M41 contracts cited by M46 | `REUSED — OWNER MEANING UNCHANGED` |
| `VOC-006` | total cost basis | Ledger & Accounting; frozen calculation/accounting rules | `REUSED — OWNER MEANING UNCHANGED` |
| `VOC-007` | average cost | Ledger & Accounting read derivation; frozen calculation rules | `REUSED — OWNER MEANING UNCHANGED`; never independent mutable M46 state |
| `VOC-008` | economic time / knowledge time | Ledger & Accounting; ADR-003 and Transaction Domain Model | `REUSED — OWNER MEANING UNCHANGED` |
| `VOC-009` | provenance | Connectivity & Ingestion / evidence-owner contracts | `REUSED — OWNER MEANING UNCHANGED` |
| `VOC-010` | standing policy / human confirmation | Connectivity & Ingestion and human sovereignty boundary | `REUSED DESCRIPTIVELY`; no policy is created here |

## 3. Candidate aggregate and boundary labels

| ID | Candidate label | Semantic owner named by frozen architecture | Disposition |
| --- | --- | --- | --- |
| `VOC-101` | Corporate Action Case | Asset Foundation | `DEFERRED TO OWNER — NOT ADMITTED`; future WP2 only under new successor authority |
| `VOC-102` | Asset Identity Consequence Set | Asset Foundation | `DEFERRED TO OWNER — NOT ADMITTED`; future WP3 |
| `VOC-103` | Portfolio Accounting Effect Bundle | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED`; future WP4 |
| `VOC-104` | Portfolio Accounting Projection | Ledger & Accounting / Portfolio Intelligence handoff | `DESCRIPTIVE ONLY — NOT ADMITTED`; contract deferred to WP4/WP5 owners |
| `VOC-105` | Valuation Binding | Market Intelligence / Portfolio Intelligence | `DEFERRED TO OWNER — NOT ADMITTED`; future WP6 |
| `VOC-106` | Effective Identifier Binding | Asset Foundation | `DEFERRED TO OWNER — NOT ADMITTED`; exact interval form belongs to WP3 |
| `VOC-107` | consequence proposal manifest | Asset Foundation with Connectivity & Ingestion admission boundary | `DEFERRED TO OWNER — NOT ADMITTED`; future WP2 |
| `VOC-108` | atomic both-or-neither release | Asset Foundation guarantee with owner-domain consequences | `DESCRIPTIVE ONLY — NOT ADMITTED`; mechanism remains open |
| `VOC-109` | Valuation Request | Portfolio Intelligence / Market Intelligence boundary | `DEFERRED TO OWNER — NOT ADMITTED`; future WP6 |
| `VOC-110` | Valuation Result | Portfolio Intelligence | `DEFERRED TO OWNER — NOT ADMITTED`; future WP6 |

## 4. Candidate accounting-effect labels

Frozen architecture §7.2 explicitly calls these planning labels rather than
admitted Transaction types. All remain outside replay and production.

| ID | Candidate label | Semantic owner | Disposition |
| --- | --- | --- | --- |
| `VOC-201` | Quantity delta | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED` |
| `VOC-202` | Quantity rescale | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED` |
| `VOC-203` | Position conversion | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED` |
| `VOC-204` | Cash movement | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED` |
| `VOC-205` | Cost-basis transfer | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED` |
| `VOC-206` | Cost-basis adjustment | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED` |
| `VOC-207` | Entitlement grant | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED` |
| `VOC-208` | Entitlement disposition | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED` |
| `VOC-209` | Reversal / compensation | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED`; append-only correction invariant retained |
| `VOC-210` | basis instruction | Ledger & Accounting | `DEFERRED TO OWNER — NOT ADMITTED`; exact amounts/weights may never be inferred by WP1 |
| `VOC-211` | structural-event performance classification | Ledger & Accounting / Portfolio Intelligence | `DEFERRED TO OWNERS — NOT ADMITTED`; affected performance fails closed meanwhile |

## 5. Candidate evidence, lifecycle, and projection labels

| ID | Candidate label | Semantic owner | Disposition |
| --- | --- | --- | --- |
| `VOC-301` | Evidence event | Connectivity & Ingestion or Market Intelligence witness boundary | `DESCRIPTIVE ONLY — NOT ADMITTED` |
| `VOC-302` | Adjudication revision | Asset Foundation | `DEFERRED TO OWNER — NOT ADMITTED`; future WP2 |
| `VOC-303` | Identity fact | Asset Foundation | `REUSED DESCRIPTIVELY`; no fact admitted here |
| `VOC-304` | Accounting consequence | Ledger & Accounting | `REUSED DESCRIPTIVELY`; no fact admitted here |
| `VOC-305` | admission decision | Connectivity & Ingestion / human confirmation boundary | `DEFERRED TO OWNER — NOT ADMITTED`; future WP2 |
| `VOC-306` | idempotency identity | Ledger & Accounting / admission owner | `DEFERRED TO OWNER — NOT ADMITTED`; future WP2/WP4 |
| `VOC-307` | canonical order tuple | Ledger & Accounting | `DESCRIPTIVE ONLY — NOT ADMITTED`; exact form deferred to WP4 |
| `VOC-308` | projection contract version / method version | Respective owner of projection or measure | `DESCRIPTIVE ONLY — NOT ADMITTED` |

## 6. Candidate failure and migration labels

| ID | Candidate label | Owner of final contract | Disposition |
| --- | --- | --- | --- |
| `VOC-401` | identity unresolved | Asset Foundation | `FAIL-CLOSED LABEL — NOT ADMITTED` |
| `VOC-402` | basis unresolved | Ledger & Accounting | `FAIL-CLOSED LABEL — NOT ADMITTED` |
| `VOC-403` | performance `UNCOMPUTABLE` | Portfolio Intelligence with Ledger handoff | `FAIL-CLOSED LABEL — NOT ADMITTED`; required documentary outcome meanwhile |
| `VOC-404` | unvalued / degraded valuation | Portfolio Intelligence | `FAIL-CLOSED LABEL — NOT ADMITTED`; scoped product semantics remain open |
| `VOC-405` | unaffected portfolio / cohort | Migration authority | `DESCRIPTIVE ONLY — NOT ADMITTED`; future WP7 |
| `VOC-406` | affected portfolio / explained difference | Migration authority | `DESCRIPTIVE ONLY — NOT ADMITTED`; future WP7 |
| `VOC-407` | unresolved portfolio / quarantine | Applicable fact owner and migration authority | `DESCRIPTIVE ONLY — NOT ADMITTED`; future WP7 |
| `VOC-408` | shadow lineage | Migration and downstream owners | `DESCRIPTIVE ONLY — NOT ADMITTED`; future WP7/WP8 |
| `VOC-409` | stale downstream artifact | Portfolio Intelligence / Trust & Evaluation owner | `DESCRIPTIVE ONLY — NOT ADMITTED`; future WP8 |

## 7. Action-family naming boundary

The generic action stories in the acceptance contract—splits, reverse splits,
symbol/name changes, bonus shares, stock dividends, dividends, return of
capital, rights, mergers, amalgamations, spin-offs, fund mergers, and class
conversions—are evidence classifications only. Existing declarative
`EventFamily` values in the repository do not authorize new canonical action,
Transaction, replay, or glossary vocabulary. Exact family admission belongs to
Asset Foundation under future WP2 authority.

BANPU is an incident fixture label, not a term, family, alias, exception, or
type. No BANPU vocabulary is admitted.

## 8. Completeness and unresolved dispositions

This register covers the named candidate aggregates in architecture §5.2, the
identifier label in §6.2, the complete effect algebra in §7.2, the event-layer
labels in §8.1, the basis label in §10.1, valuation labels in §11, failure
labels in §12, and migration labels in §14.

No candidate term has received a competent owner admission. That is a visible
dependency, not authority for M46 to choose a substitute. The six raw-byte AF
predecessor mismatches and the open alignment residual independently prevent
this register from serving as intended-path successor supply.

## 9. Vocabulary disposition

**Every candidate label has an owner and explicit disposition.**

**Vocabulary admitted by WP1: `NONE`.**

**Terminal disposition: `AUTHORED — NO VOCABULARY ADMITTED; WP1 BLOCKED`.**

This register does not authorize glossary changes, owner contracts, code,
schema, runtime behavior, migration, action adjudication, successor packages,
release, or closeout.
