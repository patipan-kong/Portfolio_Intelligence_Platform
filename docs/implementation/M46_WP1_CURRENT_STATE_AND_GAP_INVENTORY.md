# M46-WP1 — Current-State and Gap Inventory

**Artifact class:** Authorized WP1 documentary implementation deliverable 2 of 6

**Authoring role:** M46-WP1 Implementation Author

**Authorization:** [M46-WP1 Authorization Record](M46_WP1_AUTHORIZATION_RECORD.md)

**Disposition:** `AUTHORED — FAIL-CLOSED BLOCKED`

**Production mutation authority:** `NONE`

---

## 1. Inventory method and cutoff

This is a read-only inventory of repository state observed on 2026-08-05. It
uses the frozen [architecture](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md),
[roadmap](M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md), exact Asset Foundation
freeze/closeout evidence, and current source files. Absence is recorded as a
gap; it is never filled by inference.

The inventory does not declare runtime conformance, adjudicate an action,
create an owner contract, or authorize a repository change.

## 2. Complete AF-WP1–AF-WP4 frozen-output inventory

### 2.1 AF-WP1 — AF-1 permanent-reference form

| Frozen output | Lifecycle evidence | Intended supply | Non-authority boundary | Identity state |
| --- | --- | --- | --- | --- |
| [AF-1 Canonical Lexical Form](ASSET_FOUNDATION_AF_WP1_AF_1_CANONICAL_LEXICAL_FORM.md) | [AF-WP1 Freeze](../governance/ASSET_FOUNDATION_AF_WP1_FREEZE_RECORD.md), [Closeout](../governance/ASSET_FOUNDATION_AF_WP1_CLOSEOUT_RECORD.md) | Exact documentary permanent asset-reference form | No runtime representation, G-3 closure, downstream intake, or successor authority | `RAW WORKING-TREE MISMATCH` — baseline register §5 |
| [AF-WP1 Vector Annex](ASSET_FOUNDATION_AF_WP1_VECTOR_ANNEX.md) | Same frozen pair | Package-local AF-1 positive/boundary/negative evidence | No M46 vector execution or consumer authority | `RAW WORKING-TREE MISMATCH` |

### 2.2 AF-WP2 — AF-2 denomination-identifier dimension

| Frozen output | Lifecycle evidence | Intended supply | Non-authority boundary | Identity state |
| --- | --- | --- | --- | --- |
| [AF-2 Denomination-Identifier Canonical Form](ASSET_FOUNDATION_AF_WP2_AF_2_DENOMINATION_IDENTIFIER_DIMENSION_CANONICAL_FORM.md) | [AF-WP2 Freeze](../governance/ASSET_FOUNDATION_AF_WP2_FREEZE_RECORD.md), [Closeout](../governance/ASSET_FOUNDATION_AF_WP2_CLOSEOUT_RECORD.md) | Asset Foundation half of the denomination-identifier dimension | Does not supply the Ledger-owned coordinate, FX, Base Currency closure, runtime, or downstream authority | `RAW WORKING-TREE MISMATCH` |
| [AF-WP2 Vector Annex](ASSET_FOUNDATION_AF_WP2_VECTOR_ANNEX.md) | Same frozen pair | Package-local AF-2 conformance evidence | No Ledger or M46 contract admission | `RAW WORKING-TREE MISMATCH` |

### 2.3 AF-WP3 — owner evidence manifest and annex index

| Frozen output | Lifecycle evidence | Intended supply | Non-authority boundary | Identity state |
| --- | --- | --- | --- | --- |
| [AF-3 Owner Evidence Manifest and Conformance-Annex Index](ASSET_FOUNDATION_AF_WP3_OWNER_EVIDENCE_MANIFEST_AND_CONFORMANCE_ANNEX_INDEX.md) | [AF-WP3 Freeze](../governance/ASSET_FOUNDATION_AF_WP3_FREEZE_RECORD.md), [Closeout](../governance/ASSET_FOUNDATION_AF_WP3_CLOSEOUT_RECORD.md) | Exact manifest/index for AF-1 and AF-2 owner evidence | No downstream supply acceptance, intake, runtime, G-3 closure, or successor authority | `RAW WORKING-TREE MISMATCH` |

### 2.4 AF-WP4 — release profile

| Frozen output | Lifecycle evidence | Intended supply | Non-authority boundary | Identity state |
| --- | --- | --- | --- | --- |
| [AF-WP4 Release-Attestation Candidate](ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md) | [AF-WP4 Freeze](../governance/ASSET_FOUNDATION_AF_WP4_FREEZE_RECORD.md), [Release Attestation](../governance/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md), [Closeout](../governance/ASSET_FOUNDATION_AF_WP4_CLOSEOUT_RECORD.md) | Documentary release profile for the exact AF-WP1–AF-WP3 evidence | Release attestation is not runtime release; no downstream, Ledger, G-3, M45, M46, or successor authority | `RAW WORKING-TREE MISMATCH` |

The six artifacts above are the complete frozen implementation-output set named
by the AF package freeze records. Governance records and navigation artifacts
are evidence about the set, not additional frozen implementation outputs.

## 3. Recorded constitutional alignment state

| Evidence | Repository observation | Gap disposition |
| --- | --- | --- |
| [Platform Architecture](../architecture/platform_architecture.md) §§5, 6.1, 11 G2/G4 | Nine-domain constitution; Asset Foundation owns identity/restructuring adjudication; lower conflicts resolve upward | Governing and unchanged |
| [Asset Foundation](../architecture/asset_foundation.md) §§3, 4.4, 9 | Records structural-event interpretation and both-or-neither guarantee in Asset Foundation and supersedes the level-4 bridge address | Ownership reconciliation exists, but the file header remains `draft, pending ratification` |
| [Corporate Action Domain](../architecture/CORPORATE_ACTION_DOMAIN.md) opening and §2 | Still describes a standalone bridge/adjudication domain and says that domain owns the process | Textual conformance has not occurred |
| [Asset Foundation Planning Ratification](../governance/ASSET_FOUNDATION_PLANNING_RATIFICATION.md) | Ratifies the separate implementation planning pair identified there | Does not ratify `docs/architecture/asset_foundation.md` as a Domain Constitution and does not conform the level-4 text |

The ownership question is not reopened. The narrower ratification/textual-
conformance residual remains open and is dispositioned in deliverable 3.

## 4. Current runtime and repository implementation inventory

| Area | Current evidence | Alignment already present | Exact gap relative to frozen M46 plan | WP ownership |
| --- | --- | --- | --- | --- |
| Asset identity model | [Asset model](../../backend/models/asset.py) defines permanent integer `Asset.id`, identifier rows, and relationship rows | Permanent identity and related-but-distinct structures exist | Runtime/AF-1 interoperability and effective interval contract remain unresolved; WP1 does not modify them | Future WP3 under new Asset Foundation successor authority |
| Transaction persistence | [Database model](../../backend/models/database.py) `Transaction` supports `BUY`, `SELL`, `DEPOSIT`, `WITHDRAW`, `INITIAL_POSITION`, `INITIAL_CASH`, and `QUANTITY_CORRECTION`; `asset_id` is nullable; monetary/share fields are floats | Immutable transaction-shaped source and optional identity attachment exist | No canonical structural Transaction family, atomic effect grouping, entitlement, exact rational allocation, total-basis instruction, or correction reference | Future WP4 under new Ledger successor authority |
| Canonical transaction preparation | [Transaction canonicalizer](../../backend/services/transaction_canonicalizer.py) preserves raw symbol, maps a canonical symbol, optionally exposes `asset_id`, and orders by `(transaction_date, id)` | One canonicalization boundary and deterministic legacy order exist | Default path remains symbol-oriented; M46 time roles, order tuple, effect identity, atomic group, exact units/bases, and knowledge cutoff are absent | WP4 contract, then WP5 implementation |
| Holding replay | [Portfolio rebuilder](../../backend/services/portfolio_rebuilder.py) replays transactions into mutable cash, shares, and `avg_cost`; keying may fall back from `asset_id` to canonical/raw symbol; prices are fetched per symbol | A replay/reconciliation facility exists | Total cost basis is not the sole replay state; average cost is mutable; corporate-action consequences are not ordinary canonical Transactions; live/historical price acquisition remains coupled to the workflow | WP5 after frozen WP3/WP4 |
| Ledger validation | [Ledger validator](../../backend/services/ledger_validator.py) expressly states that no ledger transaction type corresponds to split/merger/spin-off/rename/suspension/delisting and declines to invent a legacy comparison | Gap is explicitly acknowledged | No structural-event Ledger semantics exist | WP4, not WP1 |
| Asset-definition vocabulary | [Asset-definition vocabulary](../../backend/services/asset_definitions/vocabulary.py) declares `SPLIT`, `MERGER`, `SPIN_OFF`, `RENAME`, `SUSPENSION`, and `DELISTING` as an event-family axis | Declarative family capability exists | The ledger validator does not consult that axis; it supplies no adjudication, admission, transaction, replay, or accounting behavior | Future owner contracts; no WP1 admission |
| Provider action evidence | [Yahoo chart adapter](../../backend/services/market_data/yahoo_chart.py) exposes provider dividends and stock-split columns/events | Provider testimony can be observed | Provider events are not adjudicated truth and cannot supply identity, ratios, Ledger effects, or replay input | WP2 evidence/adjudication contract, later packages |
| Market evidence | [Execution price observation](../../backend/services/execution_price_observation.py) and [market-price evidence](../../backend/services/market_price_evidence.py) carry some `asset_id`, symbol, currency, provider, observation-time, and provenance fields | Partial identity/provenance/freshness evidence exists | No complete M46 asset/listing/unit/time/kind/adjustment-basis binding or double-adjustment contract is established | Future WP6 |
| Performance continuity | [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md) define existing return strips but no corporate-action continuity term | Existing governed return method remains intact | Structural-event performance must be `UNCOMPUTABLE` until Ledger and Portfolio Intelligence supply a governed composition | Future owner act/WP4 handoff; not WP1 |
| Migration and shadow adoption | Current repository includes migration/rebuild utilities but no authorized M46 migration corpus or cutover evidence | Existing tools are not treated as M46 authority | M46 no-write rehearsal, additive action backfill, shadow parity, cohort, rollback, and downstream lineage are absent | WP7/WP8; both unallocated |

## 5. Current-state gap register

| Gap ID | Gap | Evidence status | Required disposition | Blocks |
| --- | --- | --- | --- | --- |
| `M46-WP1-GAP-01` | Six AF frozen outputs fail binary working-tree identity comparison | Exact mismatch recorded in baseline §5 | Competent predecessor identity/restoration or successor lifecycle; WP1 may not repair | WP1 intended-path supply |
| `M46-WP1-GAP-02` | Asset Foundation Domain Constitution remains draft | Direct header evidence | Competent constitutional ratification evidence | WP2–WP4 |
| `M46-WP1-GAP-03` | Corporate Action level-4 design retains bridge-domain wording | Direct opening/ownership evidence | Competent textual conformance, or other frozen-plan-permitted ratification route | WP2–WP4 |
| `M46-WP1-GAP-04` | No competent Asset Foundation successor-authoring authority | AF-WP4 closeout records successor authority `NONE` | New competent governance act | WP2, WP3; transitively WP4/WP6 |
| `M46-WP1-GAP-05` | No competent Ledger successor-authoring authority | Ledger owner-domain final state | New competent governance act | WP4; transitively WP5 |
| `M46-WP1-GAP-06` | Candidate vocabulary has not been admitted by semantic owners | Frozen M46 plan and vocabulary register | Owner-specific disposition; no M46 private dialect | Owner contracts and later implementation |
| `M46-WP1-GAP-07` | Acceptance fixtures lack approved facts and owner contracts | No approved M46 action fixtures identified | Preserve slots and fail closed | Vector execution and all later packages |
| `M46-WP1-GAP-08` | Performance continuity composition absent | Frozen plan and current calculation rules | Ledger/Portfolio Intelligence governed contract | Authoritative affected performance |
| `M46-WP1-GAP-09` | Full M46 quote-basis binding absent | Current source inventory | Market/Portfolio owner contract and later WP6 authority | Structural-event valuation acceptance |

## 6. Inventory disposition

The repository contains useful identity, event-family, transaction, replay,
and market-evidence foundations, but none constitutes an M46 corporate-action
implementation or authority. The AF source set is complete by name and
lifecycle evidence but is not byte-identical in the working tree. The
alignment residual is also open.

**Terminal disposition: `AUTHORED — FAIL-CLOSED BLOCKED`.**

This inventory authorizes no code, schema, runtime, migration, replay,
accounting, quote, production correction, successor package, release, or
closeout act.
