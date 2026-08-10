# BANPU-WP2 — Planning Confirmation

**Artifact class:** WP2 planning confirmation record
**Confirmation date:** 2026-08-06
**Disposition:** `CONFIRMED WITH RECORDED OBSERVATIONS`
**Freeze performed:** `NO`
**Implementation authority:** `NONE`
**WP3+ authority:** `NONE`

## 1. Confirmation boundary

This record confirms the reviewed BANPU-WP2 planning candidate (RC2) only. It
does not freeze the candidate, authorize BANPU-WP2 implementation, authorize
WP3 or any later package, amend frozen BANPU-WP1, or change production,
schema, migration, or test code.

## 2. Planning corpus

The confirmed planning candidate consists of exactly three files:

| # | Artifact | Lines | Bytes | SHA-256 |
|---|---|---:|---:|---|
| 1 | `docs/implementation/BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md` | 429 | 42,172 | `565EE81622AE01E452943801516BDC47400EC535FAF950C6601EEB50E01A53FA` |
| 2 | `docs/implementation/BANPU_WP2_WORK_PACKAGE_PLAN.md` | 222 | 18,300 | `9B11B25F87BC09A8A15D598492C32518F328DDFC770E519F86A2E960F61D06F0` |
| 3 | `docs/implementation/BANPU_WP2_IMPLEMENTATION_SEQUENCE.md` | 228 | 17,572 | `DED46B4CC06FE7EC2D9AF1E8992A8F96E4D8B410F4727DE77320B414010A6152` |

Corpus cardinality: `3`. Verified against `git status --short`: these are the
only untracked BANPU-WP2 files in the repository, and no other WP2 planning or
production artifact exists. All three files carry
`Status: PLANNING RC2 — IMPLEMENTATION NOT AUTHORIZED` and cite the frozen
`BANPU_WP1_FREEZE_RECORD.md` as their constitutional predecessor.

## 3. Review chain — RC1 and RC2 history

| Candidate | Review outcome | Resulting action |
|---|---|---|
| RC1 | Original Independent Architecture Review returned `NOT APPROVED`: one CRITICAL finding (validator identity keyspace) and five MAJOR findings (dual replay-site modeling, WP4→WP5 persistence window, successor `asset_id` binding, five-field reconciliation constructibility, incomplete verification suite set), plus four MINOR findings | Architecture Owner Design Decision Gate convened for MAJOR-2, MAJOR-3, and MAJOR-4; corrections required before re-review |
| RC2 | Implemented the corrections described in §5–§6 below | Renewed Independent Review returned `APPROVED WITH MINOR OBSERVATIONS` |

RC1 candidate bytes are not separately preserved in the repository — WP2
planning files are untracked working-tree documents, corrected in place rather
than versioned as discrete RC1/RC2 commits. This record does not invent a
repository identity for the pre-correction RC1 bytes; the RC1 finding content
below is recorded as externally attested (see §8), not independently
re-derived from RC1 bytes that no longer exist on disk.

## 4. Original independent review disposition — findings

The Original Independent Architecture Review issued the following findings
against RC1. All eleven were closed, resolved, or deferred by RC2; see §6.

| ID | Severity | Issue | Required correction |
|---|---|---|---|
| `CRITICAL-1` | CRITICAL | Validator conversion identity resolution assumed the rebuilder's `replay_key()` keyspace, but the validator's authoritative replay state is keyed by `raw_symbol` | Define engine-specific identity handling; validator must mutate its existing raw-keyed state, not a parallel conversion state |
| `MAJOR-1` | MAJOR | Rebuilder has two replay application sites (Stage 1 final-state, Stage 2 per-date); planning modeled only one, with no defined preflight ownership, duplicate-key scoping, `_PortfolioState.copy()` field coverage, or Stage 1/Stage 2 equality requirement | Explicitly model both sites, shared immutable preflight, fresh per-run duplicate tracking, complete state copying, and terminal-state equality |
| `MAJOR-2` | MAJOR | No explicit rule prevents a conversion-bearing portfolio from being rebuilt across pre-transition history before WP5 installs the hard reconstruction boundary | Architecture Owner decision: preserve WP5 ownership; do not add an interim WP2 runtime boundary |
| `MAJOR-3` | MAJOR | Rebuild commit deletes and reinserts all `PortfolioItem` rows; the existing path did not preserve `asset_id` across that operation | Architecture Owner decision: preserve every existing `PortfolioItem.asset_id`; authoritatively bind only the conversion successor |
| `MAJOR-4` | MAJOR | Existing reconciliation joins by symbol and compares only shares/average cost; asset_id and independent symbol comparison had no defined comparand under conversion | Architecture Owner decision: add conversion-scoped identity-aware five-field pairing; keep ordinary reconciliation unchanged |
| `MAJOR-5` | MAJOR | Verification command set omitted four suites owning affected behavior: `test_ledger_validator_effective.py`, `test_portfolio_rebuilder_capability_shadow.py`, `test_registry_replay_parity.py`, `test_replay_cutover.py` | Add all four suites consistently across specification, plan, sequence, verification matrix, command set, and review gates |
| `MINOR-1` | MINOR | Ambiguous whether `POSITION_CONVERSION` joins `_EQUITY_TYPES` | Explicitly exclude it; validate only through conversion-specific predicates |
| `MINOR-2` | MINOR | Repair-overlay enforcement boundary unspecified given `ledger_repair.py` is prohibited from modification | Enforce only at `portfolio_rebuilder.py`/`ledger_validator.py` consumer boundaries |
| `MINOR-3` | MINOR | No authorized path to synchronize frozen documentation and `DECISION_LOG.md` once WP2 activates replay behavior | Defer synchronization to a separately approved WP8 documentation-correction owner; prohibit `DECISION_LOG.md` edits during WP2 |
| `MINOR-4` | MINOR | Rebuilder failure disposition (`success`/`aborted`/`committed`) was ambiguous across failure modes | Define exact field values for preflight/replay failure, Stage-5 blocking, commit-exception rollback, and dry-run success |

## 5. Architecture Owner decisions

Three findings required an explicit Architecture Owner decision rather than a
mechanical correction:

- **MAJOR-2:** Preserve WP5 ownership of the hard historical reconstruction
  boundary. WP2 adds no interim runtime gate; the pre-WP5 persistence risk is
  carried as a named procedural governance prohibition instead (no persistent
  conversion row in any environment before WP5 acceptance; transient,
  rollback-isolated fixtures only; dry-run/`skip_snapshots=True` evidence
  only).
- **MAJOR-3:** Preserve every existing `PortfolioItem.asset_id` through the
  delete-and-reinsert commit via a deterministic preservation map; the
  surrendered predecessor is never reinserted and its ID is never transferred;
  only the conversion successor is authoritatively bound, and a conflicting
  non-null successor ID fails closed with no registry lookup or backfill.
- **MAJOR-4:** Add a conversion-scoped, identity-aware five-field
  reconciliation path (asset ID, symbol, shares, average cost, basis) that
  applies only to the conversion successor; ordinary symbol-keyed two-field
  reconciliation is explicitly left unchanged for every other item.

## 6. Finding closure register

| ID | Severity | Disposition after renewed review | Cross-check against current planning corpus |
|---|---|---|---|
| `CRITICAL-1` | CRITICAL | `CLOSED` | Consistent with Specification §5.2 and §9 (single augmented raw-keyed `_ReplayState`; legacy/native candidate construction; ambiguity fails closed) |
| `MAJOR-1` | MAJOR | `CLOSED` | Consistent with Specification §7.1 and §7.4 and Plan T3/T4 (shared preflight, fresh per-run duplicate sets, `_PortfolioState.copy()` coverage, terminal-state equality) |
| `MAJOR-2` | MAJOR | `CLOSED` | Consistent with Specification §5.4 and Plan §1 (transient-fixture-only rule; WP5 ownership unchanged) |
| `MAJOR-3` | MAJOR | `CLOSED` | Consistent with Specification §8 and Plan T5 (preservation map; predecessor never reinserted; conflict fails closed) |
| `MAJOR-4` | MAJOR | `CLOSED` | Consistent with Specification §8 and Plan T5 (asset-ID precedence, canonical-symbol fallback, five independent comparison fields) |
| `MAJOR-5` | MAJOR | `CLOSED` | Consistent with Specification §6.3/§12.3 and Plan §3.4/§6 (all four suites present in command set and verification matrix) |
| `MINOR-1` | MINOR | `RESOLVED` | Consistent with Specification §6.2 (`_EQUITY_TYPES` explicitly unchanged) |
| `MINOR-2` | MINOR | `RESOLVED` | Consistent with Specification §7.1 and §9.3 (`ledger_repair.py` unchanged; enforcement at consumer boundaries; `EXCLUDE`/`SUPPRESS_FINDING` ineffective on conversions) |
| `MINOR-3` | MINOR | `APPROPRIATELY DEFERRED` — owner: WP8 documentation-correction gate | Consistent with Plan §4.2 (`DECISION_LOG.md` explicitly prohibited during WP2; deferral does not authorize WP8) |
| `MINOR-4` | MINOR | `RESOLVED` | Consistent with Specification §10 (exact `success`/`aborted`/`committed` values per failure mode) |

No open WP2 planning finding remains. `MINOR-3` is a carried-forward future
gate, not an open finding.

## 7. Recorded non-blocking observations

| ID | Observation | Disposition | Owner / gate | Required verification | Blocks freeze |
|---|---|---|---|---|---|
| `OBSERVATION-1` | Post-conversion successor trading under a raw symbol differing from canonical may form a separate raw-key entry under existing ordinary BUY/SELL behavior, producing a visible `HOLDINGS_MISMATCH` | Non-blocking implementation-time fixture | WP2 validator implementation and independent review | Add a post-conversion successor-trade fixture documenting the expected existing behavior; do not redesign ordinary validator keying | `NO` |
| `OBSERVATION-2` | Asset-ID preservation scope is stated generally in the specification but phrased as conversion-portfolio-specific in one acceptance criterion | Non-blocking implementation clarification | WP2 rebuilder implementation / materialization review | State explicitly in implementation evidence whether preservation applies to all rebuilds or only conversion-portfolio rebuilds; prove no existing identity is lost and no registry backfill occurs | `NO` |
| `OBSERVATION-3` | Entry-baseline precondition names six suite categories; final verification runs eleven suites, including the four MAJOR-5 additions | Non-blocking entry-gate clarification | WP2 Step 1 baseline record | Record baseline results, including pre-existing failures, for all mandatory owner suites, explicitly naming the four MAJOR-5 suites | `NO` |
| `OBSERVATION-4` | Frozen design language calls `POSITION_CONVERSION` a symbol-bearing equity type; RC2 correctly excludes it from the `_EQUITY_TYPES` implementation constant, which controls only generic `NULL_SYMBOL`/`ZERO_SHARES` checks | Non-blocking interpretation note | WP2 validator implementation review | Record that the semantic classification and the implementation-constant exclusion are not in conflict; verify conversion-specific findings remain complete | `NO` |
| `OBSERVATION-5` | Stage 1 final-state/terminal Stage 2 state equality is valid only when the terminal snapshot date is on or after the final transaction date | Non-blocking test-construction condition | WP2 rebuilder fixture implementation | Construct the terminal Stage 2 fixture with a snapshot date on or after the last transaction date | `NO` |
| `OBSERVATION-6` | The statement that WP4 acceptance does not authorize persistent conversion rows should be read as restating the frozen roadmap/release sequence, not as WP2 asserting authority over WP4 | Non-blocking governance interpretation | WP2 confirmation and future WP4/WP5 authorization review | Record that WP2 creates no successor authority and does not modify WP4's constitutional scope | `NO` |

The Renewed Independent Architecture Review expressly disposed as
`APPROVED WITH MINOR OBSERVATIONS`; none of the six independently constitutes
a confirmation or freeze blocker, and none is silently waived — each carries a
named owner, gate, and required verification for WP2 implementation time.

## 8. Content-identity and repository-state evidence

- The three planning-corpus files were hashed directly from working-tree bytes
  (§2); all three exist only as untracked files and match `git status --short`
  exactly.
- All 12 frozen BANPU-WP1 corpus files were independently rehashed during this
  confirmation and match `BANPU_WP1_FREEZE_RECORD.md` §4 exactly — hash and
  byte count, all 12/12 — confirming WP1 is unmodified.
- `git status --short` shows only the pre-existing staged WP1 corpus and this
  untracked 3-file WP2 planning corpus; no production, schema, migration,
  test, M46, or future-package file differs.
- `git diff --check` exits clean (no whitespace errors).
- `backend/stocks.db` and `stocks.db` are both `.gitignore`d and untracked;
  no tracked-repository evidence of a database mutation or persistent
  conversion row exists.
- `graphify update .` was run; no code-graph topology change (expected — this
  diff is documentation-only).

## 9. Independent-evidence disclosure

The Original Independent Architecture Review, the Architecture Owner
decisions, the Renewed Independent Architecture Review, all eleven findings
(`CRITICAL-1`, `MAJOR-1`–`MAJOR-5`, `MINOR-1`–`MINOR-4`), and the six
non-blocking observations were supplied as authoritative external governance
evidence in this confirmation's commissioning instruction. No separate
reviewer artifact for either review exists in the repository, and this
confirmation does not invent a repository identity for either external review
act — consistent with the disclosure precedent set by
[BANPU-WP1 Freeze Record §2](BANPU_WP1_FREEZE_RECORD.md).

This confirmation did independently cross-check the substance of every
finding and observation against the current three-file planning corpus (§6–§7
"cross-check" columns) and found each closure claim consistent with corpus
content at the cited sections. It did not re-run the Original Independent
Architecture Review itself, and RC1's pre-correction bytes are not
reconstructable from the repository (§3).

## 10. Confirmation decision

BANPU-WP2 Planning RC2 is **`CONFIRMED WITH RECORDED OBSERVATIONS`**. The
review chain is complete (`NOT APPROVED` → corrections →
`APPROVED WITH MINOR OBSERVATIONS`), all eleven findings are closed, resolved,
or appropriately deferred with a named owner, the six non-blocking
observations are recorded without being treated as resolved, the frozen WP1
corpus is verified unmodified, and no unauthorized file exists in the working
tree.

BANPU-WP2 Planning is not frozen by this record. BANPU-WP2 implementation
remains unauthorized until a separate constitutional freeze act completes and
a separate implementation authorization is granted.

## 11. Exact next constitutional act

The exact next authorized constitutional act is **BANPU-WP2 Planning Freeze**
over the confirmed three-file candidate identified in §2. That act must verify
content identity, record the frozen planning corpus, and grant no implicit
WP2 implementation authority or WP3+ authority.
