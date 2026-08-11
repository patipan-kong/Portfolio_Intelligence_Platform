# BANPU-WP3 — Work Package Plan

**Artifact class:** Implementation planning only
**Status:** `WORK PACKAGE PLAN MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN`
**Work package:** `BANPU-WP3 — Quote identity and epoch protection`
**Authorized planning corpus identity (as originally approved, 2026-08-10):** `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
**Governing planning corpus identity (current, after BPA-1 amendment, 2026-08-11):** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Authority:** [BANPU-WP3 Implementation Authorization Record](BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md), disposition `BANPU-WP3 IMPLEMENTATION AUTHORIZED`, as synchronized by [BANPU-WP3 Amended Implementation Authorization Record](BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
**Successor authority created:** `NONE` beyond what the cited authorization records already grant
**BPA-1 amendment applied:** `YES` — see §0

This plan operationalizes already-authorized implementation authority. It
creates no implementation authority, no new architecture, no new planning
decision, no new gate beyond the single BPA-1 focused-review gate in §0.4, no
new acceptance criterion, and no file surface beyond the single bounded BPA-1
addition in §0.2. Where it and the frozen planning corpus differ, the frozen
corpus governs and this plan is in error.

## 0. BPA-1 Amendment (additive, 2026-08-11)

**Amendment identifier:** `BPA-1`
**Amendment date:** 2026-08-11
**Superseded governing corpus identity:** `C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`
**Current governing corpus identity:** `3A04B06A9AF5A405EC6EA6C08A2C98519FA3B2FC963AFC5EA584655294D8F43D`
**Amendment authority:** BANPU-WP3 Work Package Planning and Approval Authority,
acting on
[BANPU-WP3 Amended Implementation Authorization Record](BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
(`BANPU-WP3 BPA-1 IMPLEMENTATION AUTHORIZATION SYNCHRONIZED TO AMENDED PLANNING CORPUS`),
[BANPU-WP3 Amended Allocation Record](BANPU_WP3_AMENDED_ALLOCATION_RECORD.md), and
[BANPU-WP3 Amended Planning Freeze Record](BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md).

### 0.1 Nature of this amendment

This section and the three marked edits at §2, §3.4 Step 4.2, and the
Checkpoint C4 entry in §5 are the entire BPA-1 delta to this plan. Every other
step, checkpoint, criterion, decision, risk, and file-surface entry is
unchanged and continues to govern exactly as originally approved on
2026-08-10. Where this amendment and the frozen BPA-1 corpus differ, the
frozen corpus governs and this amendment is in error.

### 0.2 Exact operational delta

BPA-1 admits exactly one additional bounded production surface into WP3.4:

| Item | Value |
|---|---|
| File | `backend/services/data_fetcher.py` |
| Symbol | `resolve_successor_bindings(symbols)` |
| Sub-package | WP3.4 |
| Sole authorized caller | the holdings-price call path in `backend/main.py` (§3.4 Step 4.2) |
| Purpose | read-only propagation of requested, non-ambiguous canonical `SuccessorQuoteBinding` values from the accepted WP3.3 guard projection to that sole call path |
| Class | Production, read-only |

All thirteen BPA-1 constraints bind exactly as frozen, allocated, and
authorized:

1. creates no persistent state;
2. performs no memoization and holds no cache;
3. changes no guard-membership semantics;
4. changes no quarantine policy and adds, removes, or reinterprets no
   quarantine reason;
5. changes no `fetch_price_info` or `fetch_history` semantics, signature
   contract, or return shape;
6. performs no provider lookup;
7. performs no registry lookup;
8. reads no environment value and no configuration value;
9. exposes no boundary evidence;
10. constructs no binding outside the accepted WP3.2 and WP3.3 machinery;
11. leaves ambiguous and unavailable projection states fail-closed;
12. authorizes no caller other than the single WP3.4 holdings-price call path
    in `backend/main.py`;
13. confers on WP3.4 no authority over any other
    `backend/services/data_fetcher.py` behavior.

### 0.3 Consequential edits to this plan

Marked inline at their exact locations, each tagged `[BPA-1]`:

- **§2 Authorized change surface `A`** — one row added, admitting
  `resolve_successor_bindings(symbols)` in `backend/services/data_fetcher.py`,
  bounded to WP3.4, read-only.
- **§3.4 Step 4.2** — "Files expected to change" and "Files prohibited"
  updated to reflect that the binding is obtained via the accessor rather than
  constructed inline at the call site.
- **§5 Checkpoint C4** — "Expected repository state" updated to lawfully
  include the bounded `data_fetcher.py` accessor delta.

No other step, checkpoint, criterion, decision, risk, or file-surface entry in
this plan is changed by BPA-1.

### 0.4 Required gate — Focused C3 Accessor-Delta Review

Inserted between accepted Checkpoint C3 and the resumption of WP3.4 (Step 4.2
onward). **WP3.4 propagation (Step 4.2) may not resume until this gate
passes.**

**Scope.** Independent review of exactly `resolve_successor_bindings(symbols)`
in `backend/services/data_fetcher.py` against the thirteen constraints in
§0.2. This focused review does **not** reopen accepted pre-accessor WP3.3
behavior (Checkpoint C3, already accepted) and does not re-review G1–G4, cache
namespacing, stale-fallback suppression, or PD-4 enforcement, all of which
remain accepted from Checkpoint C3.

**Required outcome before WP3.4 may resume:**
`BANPU-WP3 BPA-1 ACCESSOR DELTA — FOCUSED C3 ACCEPTED`, or equivalent
unambiguous independent acceptance, recorded as a discrete artifact.

**Status at this amendment: outstanding.** This amendment does not perform,
begin, or imply that review.

### 0.5 Preserved checkpoint and evidence state

Explicit and unchanged by this amendment:

- **C1 accepted** (WP3.1) — unreopened.
- **C2 accepted** (WP3.2) — unreopened.
- **C3 accepted for the pre-accessor WP3.3 state only** — the accessor delta
  is the separate focused review in §0.4, not yet independently accepted.
- **C4 incomplete** — requires both §0.4 acceptance and the Step 4.1 evidence
  below.
- **Step 4.1 (unbound call-site register, all eleven `fetch_price_info`
  sites) remains outstanding**, exhaustive and unperformed by this amendment.
  Of those eleven sites — eight in `backend/main.py`, one each in
  `portfolio_snapshots.py`, `idea_review.py`, and `analytics/factor_engine.py`
  — only the single holdings-price call path in `backend/main.py` (Step 4.2)
  is authorized to receive propagated binding; the remaining ten must remain
  deliberately unbound unless separately authorized, and C4 evidence must
  exhaustively register and prove the required behavior for all eleven.

This amendment creates no implementation authority beyond what
[`BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP3_AMENDED_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
already granted, performs no focused C3 delta review, performs no Step 4.1
evidence work, performs no C4 review, and modifies no production or test
file.

## 1. Executive summary

This plan operationalizes the frozen BANPU-WP3 planning corpus into an
executable implementation sequence. It expands WP3.1–WP3.4 into 23
implementation steps across five stages, plus the non-implementation Gate S8
entry Step 2.0, fixes checkpoint placement, defines the Gate S5 baseline
capture, states per-step verification and completion criteria, and sets
rollback boundaries.

It adds no architecture, no planning decision, no file beyond the frozen
surface, and no authority. Every architectural position it relies on is a
citation to the frozen corpus, not a restatement with variation. Where the
corpus deliberately left a mechanism to implementation authority — guard-set
mechanism under PD-5, module and symbol names, quarantine reason members,
fixture layout, log formats (Plan §11) — this plan schedules the decision and
names its constraints without pre-empting it.

One implementation observation (IO-1, §3.1) requires reviewer determination at
the entry checkpoint before the first production edit. It is a placement
question inside the already-authorized surface, not a scope question. It is
raised rather than decided, because deciding it here would be a planning act.

A second implementation observation (IO-2, §3.2, Step 2.2) concerns the exact
WP1 field mapping for the successor quote binding. Unlike IO-1, IO-2 is not
left open: the frozen WP1 parser already enforces the mapping as a parse-time
invariant, so this plan records it as a mechanical determination rather than
electing a resolution. IO-2 does not bear on Gate S8, which continues to
govern only the new WP3.2 module's necessity under roadmap rule 7.

Gates honoured: **S3** — this plan is drafted after Allocation and after
Implementation Authorization. **S4** — strictly serial; no sub-package begins
before its predecessor is accepted at its checkpoint. **S5** — Stage 0 baseline
capture completes before the first production edit and is unrecoverable
afterwards. **S8** — WP3.2 cannot begin until rule 7 reviewer confirmation is
obtained.

## 2. Overall implementation strategy

**Strategy.** Evidence first, contract second, enforcement third, propagation
last — the layering fixed by Plan §5.4. Dependencies point strictly upward.
WP3.1 and WP3.2 are fixture-testable with no I/O. Only WP3.3 touches I/O. Only
WP3.4 touches an API module.

**Five governing disciplines**, each traceable to the frozen corpus:

1. **Baseline before edit.** Gate S5. The PD-1 characterization values are
   unrecoverable once `yahoo_chart.py` is edited, so Stage 0 is mandatory and
   blocking.
2. **Test before production, within each sub-package.** Each sub-package opens
   with a failing focused test expressing its obligation, then implements. This
   is how the frozen A-criteria become executable rather than asserted.
3. **Dual path, never a global correction.** PD-1 NARROW. Every derivation
   change is conditioned on the converted/bound path. The unbound path must be
   provably numerically identical to Stage 0 baseline, including sparse-bar.
4. **Fail closed at one layer.** Option C, adopted unconditionally. Refusal
   lives in `data_fetcher.py`; consumers are protected by refusal, not by
   editing them. `portfolio_snapshots.py`, `idea_review.py`, and
   `factor_engine.py` are deliberately untouched (Decomposition §4.4).
5. **Inert at zero conversions.** Objective O6 and criterion A6. Every stage
   must demonstrate that with an empty guard set and no conversion row, behavior
   is indistinguishable from baseline.

**Concurrency.** None. Gate S4 forbids it. Sub-packages are implemented,
reviewed, and accepted one at a time.

**Prohibited-file set `P`** — referenced by every step below, exhaustive, and
never expanded informally:

- Frozen WP1 corpus (12 files, recorded aggregate
  `DF0AF823EFEACA38171F4DACAC0B19975BAE07EE1BA09A040B549B06ACD443E1`), including
  `backend/models/database.py`, `backend/services/transaction_canonicalizer.py`,
  and the conversion migration.
- Frozen WP2 implementation corpus (aggregate
  `6E50F5B5E2AAA008EA1C3DA25D1FC34C41F9CBAE81A293A463FB3F6BF5DA4159`):
  `portfolio_rebuilder.py`, `ledger_validator.py`, `test_portfolio_rebuilder.py`,
  `test_ledger_validator.py`, `test_position_conversion_replay.py`,
  `test_repair_validate_consistency.py`.
- The frozen WP3 planning corpus itself, and the WP3 Planning Freeze,
  Allocation, and Implementation Authorization Records.
- `backend/services/portfolio_transactions.py`,
  `backend/services/portfolio_snapshots.py`,
  `backend/services/idea_review.py`,
  `backend/services/analytics/factor_engine.py`.
- `backend/services/market_data/base.py`,
  `backend/services/market_data/provider.py`, and any provider adapter other
  than `yahoo_chart.py`. In the current repository that additionally names
  `backend/services/market_data/yahoo.py`; that path is a derived instantiation
  of Decomposition §4.1 "Any other provider adapter", not a separately
  enumerated canonical entry.
- Transaction, portfolio, and `MarketDataCache` schema; all migrations; admin
  cache endpoints.
- All frontend files; all `M46*` documentation and implementation files.
- `docs/engineering/DECISION_LOG.md`, `docs/architecture/ARCHITECTURE.md`,
  `docs/investment/PORTFOLIO_CALCULATION_RULES.md`, the canonical design,
  roadmap, and implementation sequence.

If implementation appears to require any file in `P`, work stops and returns to
governance. No reviewer may widen the surface informally (Decomposition §1).

**Authorized change surface `A`** — the complete union, and the union may not
exceed it:

| Path | Sub-package | Class |
|---|---|---|
| `backend/services/market_data/yahoo_chart.py` | WP3.1 | Production |
| One new module under `backend/services/market_data/` | WP3.2 | Production, S8-gated |
| `backend/services/data_fetcher.py` | WP3.3 | Production |
| `backend/main.py` — holdings and price call site only | WP3.4 | Production |
| `backend/services/data_fetcher.py` — `resolve_successor_bindings(symbols)` only `[BPA-1]` | WP3.4 | Production, read-only, bounded per §0.2 |
| `backend/tests/test_yahoo_chart_provider.py` | WP3.1 | Test |
| One new focused test module for the WP3.2 contract | WP3.2 | Test |
| One new focused quote-epoch isolation test module | WP3.3 | Test |
| `backend/tests/test_fetch_history.py` | WP3.4 | Test |
| Focused regression test module(s) for unaffected consumers | WP3.4 | Test |

## 3. Detailed implementation sequence

### 3.0 Stage 0 — Baseline capture (Gate S5)

Not a sub-package. A blocking precondition. **No production file may be edited
until Stage 0 is complete and recorded.**

**Entry conditions.** Implementation Authorization in force; working tree clean
apart from the WP3 governance artifacts; branch `feature/banpu-remediation`.
**Exit conditions.** All four steps recorded, reproducible, and reviewed at
Checkpoint C0.
**Review checkpoint.** C0.
**Risks.** Gate S5 is one-way: baseline lost after the first edit is
unrecoverable and WP3 would have no admissible PD-1 evidence.

---

**Step 0.1 — Record repository entry state.**
*Purpose:* fix the constitutional and physical baseline WP3 starts from.
*Files expected to change:* none.
*Files prohibited:* all of `P`; in this step, every file.
*Verification evidence:* branch name; `git rev-parse HEAD`;
`git status --porcelain`; recomputed aggregates for the WP1 12-file corpus, the
WP2 implementation blob, the WP2 planning corpus, and the WP3 planning corpus,
each compared to its recorded value.
*Completion criteria:* all four aggregates match their recorded values; working
tree contains no modification to any file in `A` or `P`.

**Identity-convention condition on this step.** WP1 identity verification must
apply the per-row convention recorded in Planning Freeze Record §11.3, not a
single uniform convention. Ten of the twelve recorded WP1 rows reproduce under
the canonical LF convention; `backend/services/transaction_canonicalizer.py`
(31,416 bytes) and `backend/tests/test_transaction_canonicalizer.py` (25,881
bytes) reproduce only under the raw working-tree convention while the checkout
is CRLF. A uniform recomputation will fail for those two rows and must **not**
be read as WP1 content drift. Content continuity for both is established by
comparing LF-normalized content against the committed Git blob at `HEAD`. This
condition records an existing observation; it resolves nothing and is not
BANPU-WP3's to dispose of.

**Step 0.2 — Record baseline test state.**
*Purpose:* distinguish pre-existing failures from WP3-introduced ones.
*Files expected to change:* none.
*Files prohibited:* all of `P`.
*Verification evidence:* full pass/fail output of
`backend/tests/test_yahoo_chart_provider.py` and every suite named in §4.5,
recorded verbatim, including any pre-existing failure and its cause.
*Completion criteria:* a written baseline register exists; every pre-existing
failure is named and attributed; no failure is left unexplained.

**Step 0.3 — Capture PD-1 characterization evidence.** *(Unrecoverable after the
first edit to `yahoo_chart.py`.)*
*Purpose:* freeze the exact pre-change numeric output of the unconverted
derivation path, so PD-1 NARROW is provable rather than asserted.
*Files expected to change:* none.
*Files prohibited:* all of `P`, and
`backend/services/market_data/yahoo_chart.py` — Stage 0 is read-only.
*Verification evidence:* for each fixture in the matrix below, the exact
`get_quote()` three-key dictionary and the exact `fetch_price_info()` return,
recorded to full precision:

| Fixture | Condition |
|---|---|
| F1 | Dense close series, latest bar present, matching `meta.symbol` |
| F2 | **Sparse series, latest bar absent** — the case where positional and timestamp-associated derivation diverge |
| F3 | `meta.symbol` differs from the requested symbol |
| F4 | `meta` absent or incomplete |
| F5 | Close series containing null entries |
| F6 | Exchange-local day boundary, UTC+7 market, both edges |
| F7 | DR symbol requiring normalization (risk R5) |

*Completion criteria:* every fixture captured with exact values; F2 in
particular captured; the capture is reproducible from recorded fixture inputs
alone.

**Step 0.4 — Capture baseline cache behavior.**
*Purpose:* baseline for A4, A6, and A8.
*Files expected to change:* none.
*Files prohibited:* all of `P`.
*Verification evidence:* observed `cache_type` strings actually written for
quote and history (`quote`, `history:{period}:{interval}`); cache-hit,
cache-miss, and stale-fallback behavior on each read path — `_get_cached`,
`_get_stale`, and `prefetch_history_batch`; recorded TTLs.
*Completion criteria:* every cache read path in `data_fetcher.py` is enumerated
with its baseline behavior; the enumeration is exhaustive, not sampled.

**Baseline evidence recording format.** Stage 0 evidence is written to a
non-repository working location and transcribed into the WP3 implementation
record. Where a captured value becomes an assertion, it is embedded as an
explicit constant in an authorized test file — never recomputed from production
code at assert time, which would make the characterization vacuous.

---

### 3.1 WP3.1 — Provider evidence extraction

**Entry conditions.** Stage 0 complete; Checkpoint C0 passed; WP1 accepted
(satisfied); PD-1 and PD-2 ratified (satisfied); IO-1 determined.
**Exit conditions.** Evidence structure emitted; dual derivation path in place;
unbound values provably identical to Step 0.3; fixture matrix green; Checkpoint
C1 passed.
**Review checkpoint.** C1.
**Implementation risks.** R3 — timestamp association leaking into the unbound
path and changing sparse-bar values, which A4 forbids. R5 — DR normalization
causing false symbol mismatch.

**Implementation observation IO-1 — evidence-structure placement.**
Decomposition §4.1 authorizes only `yahoo_chart.py` as WP3.1's production file,
so the provider-neutral evidence structure must be declared there. Plan §5.2
requires the WP3.2 verification predicate to contain no provider-specific
import, so the predicate may not import `yahoo_chart.py`. Both constraints are
satisfiable — WP3.2 defines its acceptance structurally and imports nothing from
the adapter — but the determination belongs to a reviewer, not to this plan.
**If a reviewer determines instead that the structure must be declared in the
new WP3.2 module, that module is introduced in WP3.1, and Gate S8 must therefore
be satisfied before WP3.1 begins.** Raised at Checkpoint C0 and unresolved until
determined there.

**Step 1.1 — Lock the baseline as characterization tests.**
*Purpose:* make PD-1 NARROW mechanically enforced from the first edit onward.
*Files expected to change:* `backend/tests/test_yahoo_chart_provider.py`.
*Files prohibited:* all of `P`; all production files.
*Verification evidence:* new tests asserting Step 0.3 values as literal
constants for F1–F7; all green against unmodified production code.
*Completion criteria:* F2 is covered; every assertion uses a captured literal,
not a computed value.

**Step 1.2 — Extract provider evidence (E1, E2, E3, E5).**
*Purpose:* supply provider identity, the symbol actually served, per-observation
timestamps, and the exchange timezone basis, as a provider-neutral immutable
structure.
*Files expected to change:* `backend/services/market_data/yahoo_chart.py`,
`backend/tests/test_yahoo_chart_provider.py`.
*Files prohibited:* all of `P`; `execution_quote.py`; `session_evidence.py`;
every other provider adapter.
*Verification evidence:* extraction tests for matching, mismatched, and missing
metadata; the structure is immutable and carries no comparison, no binding, and
no quarantine decision; Step 1.1 characterization tests still green.
*Completion criteria:* E1, E2, E3, E5 all present and affirmative — silence does
not qualify; the module remains conversion-unaware.

**Step 1.3 — Dual derivation path (E4), converted path only.**
*Purpose:* derive current and previous close from a single response where a
binding is present, leaving every other path numerically unchanged. The
existing `get_execution_quote_envelope()` method (`yahoo_chart.py`) already
shows, as precedent rather than a mandated mechanism, that this shape of
problem is solved by a method held separate from `get_quote()` rather than a
branch inside it; module and symbol design remain implementation authority's
choice per Plan §11.
*Files expected to change:* `backend/services/market_data/yahoo_chart.py`,
`backend/tests/test_yahoo_chart_provider.py`.
*Files prohibited:* all of `P`.
*Verification evidence:* F2 sparse-bar values unchanged on the unbound path;
single-source derivation demonstrated on the bound path; both paths tested
independently.
*Completion criteria:* zero numeric drift on the unbound path across all of
F1–F7; the corrected derivation is unreachable without a binding.

**Step 1.4 — Complete the fixture matrix.**
*Purpose:* discharge WP3.1's acceptance contribution to A1, A2, A6, A4, A12, and
E1–E5.
*Files expected to change:* `backend/tests/test_yahoo_chart_provider.py`.
*Files prohibited:* all of `P`; all production files.
*Verification evidence:* fixtures for matching, mismatched, and missing
metadata; sparse closes; epoch boundaries at both edges of the UTC+7
exchange-local day; DR normalization.
*Completion criteria:* every row of the F1–F7 matrix has at least one positive
and one non-triggering case; the full suite is green; `get_quote()` still
returns the same three-key dictionary.

---

### 3.2 WP3.2 — Binding, epoch, and quarantine contract

**Entry conditions.** WP3.1 accepted at C1. **Gate S8 satisfied** — rule 7
reviewer confirmation that the new module is strictly necessary, on the recorded
ground that the binding, epoch, admissibility, and quarantine predicate must
contain no provider-specific import and no I/O and therefore cannot live in
`yahoo_chart.py` or `data_fetcher.py` without violating market-data purity. PD-2
and PD-4 ratified (satisfied). IO-2 (successor quote-binding field mapping,
Step 2.2) resolved by mechanical determination — not a Gate S8 matter.
**Exit conditions.** Pure contract module complete; fixture-only tests green; no
I/O, no clock, no database, no registry, no provider-specific import; Checkpoint
C2 passed.
**Review checkpoint.** C2.
**Implementation risks.** R4 — UTC-versus-exchange-local off-by-one at UTC+7.
R10 — a non-qualifying adapter serving an unvalidated price. R9 — drift toward a
general market-data policy layer.

**Step 2.0 — Gate S8 confirmation.** *Not an implementation step.* No file
changes. WP3.2 does not begin until the reviewer records the confirmation. If it
is refused, WP3 stops and returns to governance; no alternative placement is
authorized by this plan.

**Step 2.1 — Focused test module first.**
*Purpose:* express the contract as failing fixture-only tests before it exists.
*Files expected to change:* one new test module under `backend/tests/`.
*Files prohibited:* all of `P`; `yahoo_chart.py`; `data_fetcher.py`; `main.py`.
*Verification evidence:* tests reference no database, no network, no clock; they
fail for absence, not for error.
*Completion criteria:* the module runs standalone with no fixture requiring I/O.

**Step 2.2 — Binding value and epoch cache-key derivation.**
*Purpose:* the immutable five-field **successor** binding, per **IO-2** below —
`asset_id + provider + provider_symbol + quote_epoch_start_date + valuation_transition_date`,
each element drawn from one named WP1 field, never a generic label — built
from the frozen WP1 `PositionConversionQuoteBinding`,
`PositionConversionSuccessor`, and `PositionConversionDates` contracts, plus
deterministic derivation of `quote:asset=<asset_id>:epoch=<date>` and
`history:5y:1d:asset=<asset_id>:epoch=<date>`.
*Files expected to change:* the new WP3.2 module; its test module.
*Files prohibited:* all of `P`, `transaction_canonicalizer.py` emphatically — it
is consumed, never amended.
*Fields prohibited:* `PositionConversionQuoteBinding.predecessor_provider_symbol`
must never be read when constructing this binding — see IO-2.
*Verification evidence:* derivation is deterministic and enumerable; identical
inputs yield identical keys; no registry lookup; no schema reference; a fixture
in which the predecessor and successor provider symbols differ, proving the
constructed binding carries the successor value and never the predecessor
value.
*Completion criteria:* A11's derivability and enumerability obligations are met
with no admin endpoint change; the differing-symbol fixture passes.

**Implementation observation IO-2 — successor quote-binding field mapping.**
Resolved by mechanical determination, not elected — the frozen WP1 corpus
already fixes this mapping. `PositionConversionQuoteBinding`
(`transaction_canonicalizer.py`) carries two distinct symbol fields,
`predecessor_provider_symbol` and `successor_provider_symbol`;
`PositionConversionSuccessor` separately carries its own `asset_id` and
`provider_symbol`. The frozen WP1 parser enforces, as a parse-time
`INVARIANT_VIOLATION` at `$.quote_binding.successor_provider_symbol` ("must
match successor.provider_symbol"), that
`quote_binding.successor_provider_symbol == successor.provider_symbol` for
every `PositionConversion` payload admitted to the ledger. No equivalent
invariant ties `predecessor_provider_symbol` to any successor field.

| Binding element | WP1 source field |
|---|---|
| `asset_id` | `PositionConversionSuccessor.asset_id` |
| `provider` | `PositionConversionQuoteBinding.provider` |
| `provider_symbol` | `PositionConversionQuoteBinding.successor_provider_symbol` (parser-invariant-equal to `PositionConversionSuccessor.provider_symbol`) |
| `quote_epoch_start_date` | `PositionConversionDates.successor_quote_epoch_start_date` |
| `valuation_transition_date` | `PositionConversionDates.valuation_transition_date` |

`predecessor_provider_symbol` is excluded by construction: it is scoped to the
predecessor identity's own quote lookup, is not parser-invariant-checked
against the successor, and WP3 protects the successor identity going forward,
not the predecessor. This determination requires no Architecture Owner
ratification, creates no new planning decision, and does not bear on Gate S8,
which continues to govern only the new WP3.2 module's necessity under roadmap
rule 7 and remains unchanged.

**Step 2.3 — Epoch classification (PD-2).**
*Purpose:* map provider observation timestamps to exchange-local calendar dates
using the provider-reported exchange timezone, and compare against the payload's
timezone-free calendar dates.
*Files expected to change:* the new WP3.2 module; its test module.
*Files prohibited:* all of `P`.
*Verification evidence:* boundary fixtures at **both** edges of the
exchange-local day for a UTC+7 market; UTC-date comparison demonstrably not
used.
*Completion criteria:* no classification path reads a clock or a system
timezone; both boundary cases pass.

**Step 2.4 — Evidence contract E1–E5 and reference-price admissibility.**
*Purpose:* the PD-4 predicate over capability, plus the WP3 half of WP1 residual
`MINOR-2`.
*Files expected to change:* the new WP3.2 module; its test module.
*Files prohibited:* all of `P`; the frozen WP1 parser is consulted, never
amended.
*Verification evidence:* qualifying and non-qualifying evidence fixtures; an
adapter silent about its evidence does not qualify; reference prices rejected
when absent, non-positive, non-finite, or not decimal-exact and evidence-bound;
**no** mechanical continuity tolerance logic, which is WP5's.
*Completion criteria:* the predicate names no provider, module path, environment
variable, or configuration value; A9 satisfied without touching the WP1 parser.

**Step 2.5 — Quarantine reasons and consultable result.**
*Purpose:* enumerated reasons covering design §10 plus evidence-contract
non-satisfaction, and a deterministic consultable result carrying reason and
affected identity (PD-3 obligation B1).
*Files expected to change:* the new WP3.2 module; its test module.
*Files prohibited:* all of `P`; `ledger_validator.py` absolutely — WP3 emits no
validator finding, and the emitter locus is referred out.
*Verification evidence:* every quarantine path yields exactly one enumerated
reason; no rejection is free-text only; the result identifies exactly one
affected identity.
*Completion criteria:* A7 satisfied; the enumeration members are
implementation-chosen, as Plan §11 permits, and are exhaustive over design §10
plus E1–E5 non-satisfaction.

---

### 3.3 WP3.3 — Cache namespacing and fail-closed fetch integration

**Entry conditions.** WP3.2 accepted at C2. PD-5 ratified (satisfied).
**Exit conditions.** Binding-aware fetch; converted namespaces live; stale
fallback suppressed; guard set satisfying G1–G4 including the G4 transition
test; unbound path proven unchanged from Step 0.4 baseline; Checkpoint C3
passed.
**Review checkpoint.** C3 — the heaviest review in WP3.
**Implementation risks.** R11 — memoized guard set failing open after WP4
materializes a conversion. R2 — unbound call sites. R8 — stranded legacy cache
rows. R10 — non-qualifying provider.

**Step 3.1 — Regression tests for the unbound path first.**
*Purpose:* lock A4, A6, and A8 before touching the fetch layer.
*Files expected to change:* one new focused quote-epoch isolation test module.
*Files prohibited:* all of `P`; `data_fetcher.py` at this step.
*Verification evidence:* Step 0.4 cache behavior asserted as literals across
every read path; guard set empty.
*Completion criteria:* green against unmodified `data_fetcher.py`.

**Step 3.2 — Guard set satisfying PD-5 G1–G4.**
*Purpose:* Option C's refusal mechanism, with the ratified freshness invariant.
*Files expected to change:* `backend/services/data_fetcher.py`; the WP3.3 test
module.
*Files prohibited:* all of `P`; no configuration value, constant, or environment
setting may define membership (G1).
*Verification evidence:* membership sourced solely from canonical
`POSITION_CONVERSION` ledger evidence as canonicalized by the frozen WP1
contract; a declared, finite, testable staleness bound with unbounded
memoization demonstrably absent (G2); undetermined membership refused with an
enumerated reason and never resolved to "not converted" (G3); **the G4
transition test — an identity that becomes converted after the projection was
first populated is refused for an unbound caller, in the same running process,
without restart.**
*Completion criteria:* all four of G1–G4 have dedicated evidence; a test
exercising only an empty set and a pre-populated set does **not** satisfy this
step; the set is empty and inert while no conversion row exists.

**Step 3.3 — Binding-aware quote and history fetch.**
*Purpose:* explicit binding as the only route to a converted-identity price;
structured refusal otherwise.
*Files expected to change:* `backend/services/data_fetcher.py`; the WP3.3 test
module.
*Files prohibited:* all of `P`; `fetch_price_info()` and `fetch_history()`
return shapes are preserved.
*Verification evidence:* bound converted request served; unbound converted
request refused, structured and observable; unconverted request identical to
baseline.
*Completion criteria:* A10 demonstrated end to end at the fetch layer; A5 blast
radius confined to the affected identity.

**Step 3.4 — Epoch-namespaced cache types.**
*Purpose:* asset- and epoch-bound cache entries for converted identities.
*Files expected to change:* `backend/services/data_fetcher.py`; the WP3.3 test
module.
*Files prohibited:* all of `P`; `backend/models/database.py` — the existing
`(symbol, cache_type)` uniqueness constraint is sufficient; admin cache
endpoints.
*Verification evidence:* namespaced writes and reads via `_get_cached` and
`_set_cached`; **`prefetch_history_batch` covered**, since it is an independent
cache read path; unconverted keys byte-identical to Step 0.4.
*Completion criteria:* A3, A11, A12 satisfied; no migration; no schema change;
legacy rows remain valid and are not purged, per R8.

**Step 3.5 — Stale-fallback suppression.**
*Purpose:* a quarantined or converted identity receives no predecessor value
through any cache read path.
*Files expected to change:* `backend/services/data_fetcher.py`; the WP3.3 test
module.
*Files prohibited:* all of `P`.
*Verification evidence:* every `_get_stale` call site enumerated and covered —
the quote path and the history path at minimum; suppression proven per path;
unconverted stale fallback unchanged from baseline.
*Completion criteria:* A8 satisfied by exhaustive path enumeration, not by
sampling.

**Step 3.6 — PD-4 enforcement and quarantine logging.**
*Purpose:* enforce the evidence contract at the binding-consumption layer; emit
structured quarantine logs.
*Files expected to change:* `backend/services/data_fetcher.py`; the WP3.3 test
module.
*Files prohibited:* all of `P`; `provider.py` — provider selection is untouched.
*Verification evidence:* a non-qualifying adapter yields quarantine, never an
unvalidated price, for a converted identity; unconverted assets unaffected
regardless of selected provider; logs carry the enumerated reason and affected
identity.
*Completion criteria:* A7 holds at the enforcement layer; log format is
implementation-chosen per Plan §11 but deterministic.

---

### 3.4 WP3.4 — Call-path propagation and regression evidence

**Entry conditions.** WP3.3 accepted at C3.
**Exit conditions.** Binding propagated at the owning call site; unbound
register complete with refusal evidence; real regression suite in place;
boundary audits green; Checkpoint C4 passed.
**Review checkpoint.** C4.
**Implementation risks.** R2 — an unbound site silently bypassing protection.
R6 — reliance on `test_fetch_history.py`, which is a 325-byte live print script
with no test functions.

**Step 4.1 — Unbound call-site register.**
*Purpose:* enumerate every price call site that supplies no binding and
demonstrate each receives a structured refusal, not an incorrect value.
*Files expected to change:* none — this is review evidence.
*Files prohibited:* all of `P`; the three consumer modules are deliberately not
edited.
*Verification evidence:* the register must account for all eleven
`fetch_price_info` call sites — eight in `backend/main.py` (at the time of
writing, lines 726, 747, 871, 1035, 1040, 2026, 2033, 4700), and one each in
`portfolio_snapshots.py`, `idea_review.py`, and `analytics/factor_engine.py` —
with per-site refusal demonstration for a converted identity.
*Completion criteria:* the register is exhaustive against a fresh repository
search, not against this plan's line numbers; each site's protection is
attributed to WP3.3 refusal, never to a consumer edit.

**Step 4.2 — Binding propagation at the owning call site.** *`[BPA-1]`
Requires the Focused C3 Accessor-Delta Review gate (§0.4) passed before this
step may resume.*
*Purpose:* supply the binding at the one holdings and price call site that owns
portfolio identity, obtained via the bounded BPA-1 accessor
`resolve_successor_bindings(symbols)` (§0.2) rather than constructed inline at
the call site.
*Files expected to change:* `backend/main.py`, that call site only; and
`backend/services/data_fetcher.py`, bounded exactly to
`resolve_successor_bindings(symbols)` per §0.2 `[BPA-1]`.
*Files prohibited:* all of `P`; every other `main.py` region; every endpoint
definition; every `data_fetcher.py` symbol or behavior other than
`resolve_successor_bindings(symbols)`.
*Verification evidence:* no endpoint added; no response shape changed; the
`main.py` diff confined to the identified call site; the `data_fetcher.py`
diff confined to the bounded accessor and satisfies all thirteen constraints
in §0.2; all other sites remain in the Step 4.1 register.
*Completion criteria:* the selected site is the one that owns portfolio
identity, identified from repository evidence and recorded with its
justification at C4; the accessor carries no authority beyond §0.2.

**Step 4.3 — Real regression suite for unaffected consumers.**
*Purpose:* replace reliance on a print script with executable regression
evidence.
*Files expected to change:* `backend/tests/test_fetch_history.py`; focused
regression test module(s).
*Files prohibited:* all of `P`; **the roadmap is not amended** — R6 remains a
recorded residual for separately approved documentation correction.
*Verification evidence:* real test functions with assertions; quote and history
behavior for unaffected consumers proven unchanged from Stage 0 baseline.
*Completion criteria:* the suite executes under `pytest` and fails when
regressed; R6 remains recorded, not resolved.

**Step 4.4 — Boundary audits and graph currency.**
*Purpose:* prove the change surface and the frozen corpora.
*Files expected to change:* none.
*Files prohibited:* all of `P`.
*Verification evidence:* recomputed WP1 and WP2 aggregates matching Step 0.1,
under the per-row convention condition stated there; M46 files unchanged; the
frozen WP2 deferral guard test green — a **frozen-boundary preservation check**
discharging PD-3 obligation B3, not a behavioral dependency, and no WP3 test
asserts validator semantics; `git diff --name-only` ⊆ surface `A`;
`graphify update .` run.
*Completion criteria:* A13 and A14 satisfied; zero paths outside `A`.

## 4. Per-step verification

### 4.1 Verification command set

```text
pytest backend/tests/test_yahoo_chart_provider.py
pytest backend/tests/<wp3.2 contract test module>
pytest backend/tests/<wp3.3 quote-epoch isolation module>
pytest backend/tests/test_fetch_history.py
pytest backend/tests/<wp3.4 regression module(s)>
pytest backend/tests/test_position_conversion_replay.py
pytest backend/tests/test_transaction_canonicalizer.py
pytest backend/tests/test_position_conversion_migration.py
git status --porcelain
git diff --check
git diff --name-only
graphify update .
```

**`git diff --check` on untracked files is vacuous.** New test modules are
untracked until added. The verified pattern: `git add -N <new paths>` →
`git diff --check` → `git diff --cached --check` → `git reset -q` if the staging
was only for the check. Reporting a clean `git diff --check` over untracked
files without intent-to-add is not admissible evidence.

### 4.2 Criterion-to-step traceability

| Criterion | Proven at |
|---|---|
| A1 | 1.2, 1.3, 3.3, 4.1 |
| A2 | 1.3, 3.3 |
| A3 | 2.2, 3.4 |
| A4 | 0.3, 1.1, 1.3, 3.1, 3.4, 4.3 |
| A5 | 2.5, 3.3, 3.6 |
| A6 | 0.3, 0.4, 3.1, 3.2, 4.3 |
| A7 | 2.5, 3.6 |
| A8 | 0.4, 3.5 |
| A9 | 2.4 |
| A10 | 3.2 (G4), 3.3, 3.6, 4.1 |
| A11 | 2.2, 3.4 |
| A12 | 1.4, 3.4 |
| A13 | 4.4 |
| A14 | 4.4 |

### 4.3 Ratified-decision traceability

PD-1 NARROW → 0.3, 1.1, 1.3. PD-2 → 1.2, 2.3. PD-3 B1 → 2.5; B3 → 4.4. PD-4
E1–E5 → 1.2, 1.3, 2.4, 3.6. PD-5 G1–G4 → 3.2. R7 waiver → no step; it creates no
WP3 obligation.

### 4.4 Risk-to-step traceability

R2 → 3.2, 3.3, 4.1. R3 → 0.3, 1.1, 1.3. R4 → 1.4, 2.3. R5 → 1.4. R6 → 4.3,
recorded not resolved. R8 → 3.4. R9 → C2 review. R10 → 2.4, 3.6. R11 → 3.2 G4.

### 4.5 Mandatory unchanged regression owners

Run, not edited, because they own behavior on or adjacent to the surface:
`test_position_conversion_replay.py` (frozen WP2 deferral guard),
`test_transaction_canonicalizer.py`, `test_position_conversion_migration.py`,
and every suite that monkeypatches `fetch_price_info` —
`test_workspace_referenceability_m36_1_wp4c.py`, `test_watchlist_registry.py`,
`test_fee_accounting.py`, `test_factor_engine_asset_id.py`,
`test_position_import_accounting.py`,
`test_portfolio_snapshot_capability_shadow.py`, `test_snapshot_coverage.py`. A
signature change to `fetch_price_info` that breaks these monkeypatches is a
scope signal, not a test-fixing task, and is raised at C3.

## 5. Independent review checkpoints

Each checkpoint is an independent review. A sub-package is not accepted until
its checkpoint passes, and its successor does not begin until acceptance —
Gate S4.

**Checkpoint C0 — Entry.** Implementation Authorization in force; Stage 0
complete with F2 captured; all four frozen aggregates match under their recorded
conventions; baseline failures attributed; file surface `A` and prohibition set
`P` acknowledged; **IO-1 determined**, with the consequence recorded if the
determination moves the module into WP3.1. *Expected repository state:*
unchanged apart from the WP3 governance artifacts. Zero production edits.

**Checkpoint C1 — WP3.1.** Evidence structure immutable and conversion-unaware;
E1, E2, E3, E5 affirmative; dual derivation confined to the bound path; **F2
sparse-bar value numerically unchanged**; `get_quote()` shape unchanged; DR
fixtures present. *Expected repository state:* `yahoo_chart.py` and
`test_yahoo_chart_provider.py` modified. Nothing else.

**Checkpoint C2 — WP3.2, incorporating the S8 record.** Rule 7 confirmation
recorded before any WP3.2 edit; the module performs no I/O, reads no clock,
touches no database, resolves no registry identity, and imports nothing
provider-specific; binding built from the frozen WP1 contract without amending
it, using exactly the IO-2 field mapping —
`PositionConversionSuccessor.asset_id`, `PositionConversionQuoteBinding.provider`,
`PositionConversionQuoteBinding.successor_provider_symbol` (never
`predecessor_provider_symbol`),
`PositionConversionDates.successor_quote_epoch_start_date`,
`PositionConversionDates.valuation_transition_date` — proven by the
differing-symbol fixture; both UTC+7 boundary edges pass; E1–E5 affirmative;
reference-price admissibility present and **mechanical continuity tolerance
absent**; exactly one enumerated quarantine reason per path; no validator
emission. *Expected
repository state:* C1 state plus one new production module under
`backend/services/market_data/` and one new test module.

**Checkpoint C3 — WP3.3.** The heaviest review. G1–G4 each independently
evidenced, **G4 by the in-process transition test**; every cache read path
namespaced, including `prefetch_history_batch`; every `_get_stale` path
suppressed for converted and quarantined identities; unbound path proven
identical to Step 0.4 with an empty guard set; PD-4 enforced at binding
consumption; no schema change, no migration, no admin endpoint change; provider
selection untouched. *Expected repository state:* C2 state plus
`data_fetcher.py` and one new test module.

**Checkpoint C4 — WP3.4 and package acceptance.** Unbound register exhaustive
against a fresh search covering all eleven sites; propagation confined to the
one owning call site; no endpoint or response-shape change; real regression
suite replacing the print script; WP1 and WP2 aggregates unchanged; M46
unchanged; WP2 deferral guard green as a boundary check; diff ⊆ `A`;
Focused C3 Accessor-Delta Review (§0.4) independently accepted `[BPA-1]`;
`graphify update .` run. *Expected repository state:* C3 state plus `main.py`
(one call site), `backend/services/data_fetcher.py` bounded exactly to
`resolve_successor_bindings(symbols)` per §0.2 `[BPA-1]`, `test_fetch_history.py`,
and the regression module(s). Nothing outside `A`.

**Reviewer standing instructions.** A reviewer may accept, or return with
findings. A reviewer may **not** widen surface `A`, admit a file from `P`,
reinterpret a ratified decision, resolve a residual, satisfy Gate S8 implicitly,
or accept a sub-package on partial evidence. Acceptance at C4 is package
acceptance only; it performs no confirmation and no freeze.

## 6. Completion conditions

BANPU-WP3 implementation is complete when all four sub-packages are accepted at
C1–C4; canonical criteria A1–A5 and derived criteria A6–A14 are satisfied; and
the frozen WP1 and WP2 corpora are unchanged, evidenced by aggregate identity.

Completion satisfies the WP4 entry gate, as Decomposition §8 states. Gate S7
additionally requires that WP3 be **confirmed and frozen** before WP4 begins;
approved but unfrozen does not satisfy that gate.

Completion does not authorize release, does not authorize production data
mutation, does not close R6, the R7 waiver, or the WP1 `database.py` identity
residual, and does not resolve the emitter-locus item referred out by PD-3.

### 6.1 Rollback boundaries

The rollback unit is the sub-package, which is why serial execution is required.
There is no migration, no schema change, and no data mutation in WP3, so
rollback is confined to source revert.

| Boundary | Rollback action |
|---|---|
| Within a sub-package, before its checkpoint | Revert that sub-package's files to the prior accepted checkpoint state |
| After C1 | Revert `yahoo_chart.py`, `test_yahoo_chart_provider.py` |
| After C2 | Delete the WP3.2 module and its test; then C1 boundary if needed |
| After C3 | Revert `data_fetcher.py`, delete the WP3.3 test module; then C2 boundary if needed |
| After C4 | Revert `main.py`, `test_fetch_history.py`, regression modules; then C3 boundary if needed |
| Cache rows | None required. Converted namespaces are new keys; legacy rows are untouched and remain valid (R8). Purge is WP7 |
| Database | None. No migration, no schema change (A12) |

**Rollback triggers:** frozen-corpus aggregate mismatch; any numeric drift on
the unbound path, sparse-bar especially; a guard set that fails open under the
G4 transition test; a quarantine that escapes its affected identity; a stale
fallback reaching a quarantined identity; a change to `get_quote()` or
`fetch_price_info()` response shape; any diff path outside `A`; any edit to a
file in `P`; any WP3 test asserting validator behavior; Gate S8 bypassed.

No manual ledger edit, row deletion, migration downgrade, cache purge,
production restore, or conversion-row authoring is authorized by this plan.

## 7. Repository hygiene requirements

- **Branch.** Work continues on `feature/banpu-remediation`. HEAD at plan issue:
  `3a0bbe726dd4f2de67a8e6d3dbe227b4b5b27f44`.
- **Entry state.** Any `git status --porcelain` entry at Stage 0 beyond the WP3
  governance artifacts is investigated and attributed before the first edit.
- **Untracked-file checking.** `git diff --check` is vacuous over untracked
  files. Use `git add -N` before checking, then `git diff --cached --check`,
  then `git reset -q`.
- **Whitespace and line endings.** `git diff --check` must exit 0 at every
  checkpoint. `core.autocrlf=true` with no `.gitattributes`: committed blobs are
  LF, checkouts CRLF. "LF will be replaced by CRLF" is informational and
  expected.
- **Identity convention.** Corpus identity is SHA-256 over Git-canonical LF
  content (CRLF→LF normalized), binding per
  `BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md` §4 and §9, with the two-row
  raw-convention exception recorded at Planning Freeze Record §11.3. Aggregate
  manifest: one row per file as `path<TAB>SHA256<TAB>bytes<LF>`, uppercase hex,
  plain decimal bytes, forward-slash repo-relative paths, table order, trailing
  LF, UTF-8, hashed as a single UTF-8 string.
- **Graph currency.** `graphify update .` after production changes, at Step 4.4
  at minimum, and at any checkpoint where production source changed.
- **Diff discipline.** At every checkpoint, `git diff --name-only` must be a
  subset of surface `A`. A single path outside it halts the checkpoint.
- **Commits.** This plan authorizes no commit, no push, no branch operation, no
  deployment, and no release. Commit policy is governance's, not
  implementation's.
- **Python invocation.** Use `./.venv/Scripts/python.exe`; the bare
  `python`/`python3` on this machine resolves to the Store stub.
- **Evidence storage.** Stage 0 and checkpoint evidence lives outside the
  repository until transcribed into an implementation record; no evidence file
  is written into `docs/` under this plan.

## 8. Exact next constitutional act

This plan performs no implementation, produces no code, and performs no review,
confirmation, or freeze. It creates no authority beyond what the Implementation
Authorization already granted.

The exact next constitutional act is **Independent Work Package Plan Review**.
Implementation begins at Stage 0 only after this plan is approved, and Stage 0
must complete before the first production edit under Gate S5.
