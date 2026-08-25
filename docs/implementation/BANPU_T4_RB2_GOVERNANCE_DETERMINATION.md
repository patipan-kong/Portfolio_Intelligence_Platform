# BANPU-T4-RB2 Governance Determination

**Act:** BANPU T4-RB2 Governance Determination Authority
**Scope:** Determination-only. No correction implemented, authorized, or
performed in this act. No test, fixture, configuration, or production file
mutated. WP8-T4 not rerun. WP8-T5 not started.

---

## 1. Entry state

- Branch: `feature/banpu-remediation`
- HEAD: `f052e2bfb11f2c8a0ec13f523da4599d690927ea` — confirmed via
  `git rev-parse HEAD`.
- Staging: confirmed empty (`git diff --cached --stat` — no output).
- Frozen RB-1 Correction Freeze Record
  (`docs/implementation/BANPU_T4_RB1_CORRECTION_FREEZE_RECORD.md`):
  SHA-256 `6f10267cc621487d5b0db71edc66bf5c91fdd4cefc02ddf40787c6a64fe8349a`,
  230 lines, 10,993 bytes — all three independently re-derived from live
  bytes and matched exactly. Disposition line confirmed present:
  `BANPU-T4-RB1 CORRECTION FROZEN`.
- Frozen RB-1 implementation corpus, independently re-hashed:
  - `backend/tests/test_ledger_validator_effective.py` →
    `2ecce008e3e0818dae99bed5ea43edb33b4123b2dafb13e9c71bb3b247155bb2` — match.
  - `backend/tests/test_fee_accounting.py` →
    `abeaba223fe5f5bb418d066823e52c4406c1df9d913438944fab905ad0360f10` — match.
  - `backend/tests/test_snapshot_coverage.py` →
    `bed1922d702566e19da13de7b5446923c397ce2b0ce256b5d67eb0338f0bc5e7` — match.
  - RB-1 implementation authority confirmed `EXHAUSTED / CLOSED`; none of
    the three files touched in this act.
- Original WP8-T4 evidence
  (`docs/implementation/BANPU_WP8_REGRESSION_RESULTS.md`): SHA-256
  `1539b0875682cbc0f2f795d3d030f2b6bda0a57346012e84edf4681192b26885` — match,
  unchanged, still records `BANPU-WP8 T4 BLOCKED —
  REGRESSION BLOCKER OPEN-IDENTIFIED`.
- Frozen WP8 corpus (Allocation, Implementation Authorization, WPP, Planning
  Confirmation, Planning Freeze, T1/T2 survey, T3 test) — all seven
  independently re-hashed and matched the values already on record from the
  RB-1 act: `75b293f5…`, `f2b000a8…`, `a43f2601…`, `21816abe…`, `20c332c9…`,
  `0a3cd0e2…`, `215c150b…` respectively. No drift.
- No prior RB-2 allocation, authorization, correction, or governance
  determination exists anywhere in `docs/implementation/` — confirmed by
  directory listing; this determination establishes the first RB-2 record.
- Complete dirty/untracked surface (`git status --porcelain`), classified:
  - Modified, RB-1-authorized: `backend/tests/test_fee_accounting.py`,
    `backend/tests/test_ledger_validator_effective.py`,
    `backend/tests/test_snapshot_coverage.py`.
  - Modified, pre-existing and outside every BANPU act to date:
    `backend/tests/test_position_conversion_live.py`,
    `docs/engineering/DECISION_LOG.md`, `docs/implementation/INDEX.md`.
  - Untracked: the full pre-existing BANPU governance corpus (WP4/WP7/WP8/RB-1
    records) plus `backend/tests/test_banpu_wp8_integrated_regression.py`.
  - No RB-2 test surface mutation, no production mutation, no new generated
    file beyond this determination artifact itself.
- No unexplained drift found anywhere in the entry-state sweep.

---

## 2. Reconstructed RB-2 failure

Test: `backend/tests/test_portfolio_transactions_capability_shadow.py::test_execute_buy_unaffected_by_capability_mismatch`

The test mints a CASH-typed symbol (`SHADOW_CASH`), seeds a portfolio, calls
`execute_buy(db, ws.id, p.id, "SHADOW_CASH", shares=10.0, price_per_share=2.0)`
inside `caplog.at_level("WARNING", logger="services.portfolio_transactions")`,
then asserts:

1. `result["shares"] == 10.0` — business result.
2. `result["holding"]["shares"] == 10.0` — persisted holding.
3. `any("RUNTIME_TRANSACTION_QUANTITY_VALUATION" in r.message for r in caplog.records)`
   — a WARNING-level shadow-consultation finding was logged.

Assertions 1 and 2 pass. Assertion 3 fails: no matching log record exists.
The test asserts nothing else after the logging assertion.

The warning is not incidental/diagnostic-only text — it is the log-only
reporting shape of a named Stage R1 shadow consultation contract
(`RUNTIME_TRANSACTION_QUANTITY_VALUATION`, mirroring the equivalent checks in
`ledger_validator.py` (M11), `asset_registry.py` (M12), and
`portfolio_snapshots.py` (M30.2)) — see §7.

---

## 3. Focused diagnostic reproduction

Interpreter: `backend/venv-test/Scripts/python.exe` (Python 3.13.3,
pytest-9.1.1), external basetemp under the session scratchpad.

**Isolated run** (single test):

```
pytest tests/test_portfolio_transactions_capability_shadow.py::test_execute_buy_unaffected_by_capability_mismatch -v
→ 1 failed, 11 warnings in 1.01s
AssertionError at line 205: assert False = any(...)
```

**Containing-module run** (unchanged, all 10 tests):

```
pytest tests/test_portfolio_transactions_capability_shadow.py -v
→ 1 failed, 9 passed, 46 warnings in 1.08s
FAILED: test_execute_buy_unaffected_by_capability_mismatch
```

Both runs are diagnostic only — neither constitutes T4, and no full 37-path
corpus rerun was performed.

Failure text, business-behavior result, and record count are identical
between isolated and full-module execution: exactly one failure, in the same
test, for the same reason, both times.

---

## 4. Production call/logging path

`backend/services/portfolio_transactions.py`:

- `_log = logging.getLogger(__name__)` → logger name `services.portfolio_transactions`
  (line 75) — matches the test's `caplog.at_level(..., logger=...)` exactly.
- `_QUANTITY_VALUATION_CHECK = "RUNTIME_TRANSACTION_QUANTITY_VALUATION"` (line 77).
- `_consult_runtime_for_transaction(db, symbol, tx_id, kind)` (line 113) —
  resolves the symbol's capability view and returns a
  `RuntimeConsultationLog` of findings; never raises.
- `_log_runtime_consultation(db, symbol, tx_id, kind, fn_name)` (line 166) —
  calls the above, and for each finding emits
  `_log.warning("runtime consultation finding on %s: check_id=%s ...", ...)`
  — this is the only code path capable of producing the record the test
  expects.
- Call-site grep across the entire file
  (`grep -n "_log_runtime_consultation" services/portfolio_transactions.py`)
  returns exactly **one** call site in the live file:

  ```
  685:    _log_runtime_consultation(db, symbol, tx.id, "dividend_flow", "execute_dividend")
  ```

- `execute_buy()` (line 250) commits the transaction, builds the result
  dict, calls `_observe_transaction_execution_eligibility()` (an unrelated,
  already-passing Stage-R1-adjacent shadow consult for execution
  eligibility), and returns — **it never calls `_log_runtime_consultation`
  for `"quantity_valuation"` at all.**
- `execute_sell()` (line 385) and `execute_initial_position()` (line 702)
  are in the same state — neither calls `_log_runtime_consultation` for
  `"quantity_valuation"` either. Confirmed by the same single-call-site grep
  result above.

---

## 5. Business-behavior result

Confirmed unaffected. `execute_buy()`'s transaction, holding, and cash
mutation are untouched by this gap — the consultation, when wired, is a
pure post-commit, log-only observation (module comment, lines 89–112, and
DECISION_LOG M30.3/M30.2: "structurally incapable of affecting the
transaction already recorded"). The missing call site cannot itself be a
correctness regression in the transaction ledger; it is an observability
gap only.

---

## 6. Expected logging contract in the test

Exactly as coded: WARNING-level record on logger `services.portfolio_transactions`
whose message contains the literal string `RUNTIME_TRANSACTION_QUANTITY_VALUATION`,
captured via `caplog.at_level("WARNING", logger="services.portfolio_transactions")`
around the `execute_buy()` call. No other record content, count, or ordering
is asserted.

---

## 7. Historical test origin

`git log --follow` on the test file shows exactly one commit:

```
679e2ae 2026-07-14 feat(runtime): complete portfolio capability safety rollout
```

The test was introduced complete, alongside the production wiring, and has
never been modified since.

---

## 8. Historical production/logging origin

`git show 679e2ae -- backend/services/portfolio_transactions.py` shows the
commit added `_consult_runtime_for_transaction`, `_log_runtime_consultation`,
and **four** call sites:

```
161:+    _log_runtime_consultation(db, symbol, tx.id, "quantity_valuation", "execute_buy")
170:+    _log_runtime_consultation(db, symbol, tx.id, "quantity_valuation", "execute_sell")
179:+    _log_runtime_consultation(db, symbol, tx.id, "dividend_flow", "execute_dividend")
188:+    _log_runtime_consultation(db, symbol, tx.id, "quantity_valuation", "execute_initial_position")
```

DECISION_LOG.md's own **M30.3 — Capability Safety Adoption, Portfolio
Fan-out** entry (2026-07-14, same day) independently documents this as
built and verified: *"called once per write path — `execute_buy()`,
`execute_sell()`, `execute_initial_position()`, `execute_dividend()` —
immediately after `db.commit()`"*, and its **Impact** section reports the
full backend suite at milestone completion as `59 failed / 1666 passed / 32
skipped`, with all 59 failures independently accounted for by two named,
unrelated causes (50 pre-existing baseline crash-file failures, 9
pre-existing `test_quant_engine.py` failures) — leaving zero failures
attributable to `test_portfolio_transactions_capability_shadow.py`. All ten
of that file's tests, including
`test_execute_buy_unaffected_by_capability_mismatch`, were green at M30.3
completion.

`git log --graph` on `backend/services/portfolio_transactions.py` shows
what happened next:

```
*   c50b2cf a2049a8 679e2ae 2026-07-14 Merge branch 'feature/runtime-adoption'
|\
| * 679e2ae ff50c70 2026-07-14 feat(runtime): complete portfolio capability safety rollout
* | a2049a8 ff50c70 2026-07-14 feat(execution): implement M31.3 shadow eligibility and M31.5 registry remediation foundations
|/
```

`679e2ae` (capability-safety fan-out, above) and `a2049a8` (M31.3/M31.5,
same day, same parent `ff50c70`) independently modified
`execute_buy()`/`execute_sell()`/`execute_initial_position()` on divergent
branches. The merge commit `c50b2cf` ("Merge branch
'feature/runtime-adoption'") reconciled both — and its resolution of
`portfolio_transactions.py` kept the M31.3/M31.5 (`a2049a8`) bodies of
`execute_buy()`, `execute_sell()`, and `execute_initial_position()`, which
did not carry the three `_log_runtime_consultation("quantity_valuation", …)`
calls, while the shared helper functions, constants, and the fourth call
site (`execute_dividend()`, untouched by the `a2049a8` branch) survived
intact. `git log -S'"quantity_valuation", "execute_buy"'` on the file
returns only the introducing commit `679e2ae` — consistent with a merge
resolution silently dropping the line rather than any later commit
explicitly deleting it via a normal diff.

No commit after `c50b2cf` (`c76ff53` 2026-07-14, `af07dc4` 2026-07-21,
`1e55f0e` 2026-08-17) reintroduces or further touches any
`_log_runtime_consultation` call site in this file. DECISION_LOG's `c76ff53`
entry ("M31/fee quotes") records fixing an unrelated `NameError:
RuntimeConsultationLog` import-collection failure in `test_fee_accounting.py`
— evidence that Stage R1 transaction-consultation code was touched again
after the merge, but only for an import, not for re-verifying the dropped
wiring, and not in this test file.

---

## 9. Relevant BANPU/predecessor ownership history

No BANPU work package (WP1–WP8) or RB-1 previously modified, owned, tested,
or discussed `test_portfolio_transactions_capability_shadow.py`,
`portfolio_transactions.py`'s Stage R1 wiring, capability-shadow logging, or
this failure. WP8-T4 is the first point at which this failure was observed
by any BANPU act (as one of the original 36 T4 failures, subsequently split:
35 RB-1, 1 provisional RB-2). RB-1's implementation authority is exhausted
and scoped to a single unrelated test-stub field
(`replay_asset_id_native`) in three named files that do not include this
one. No predecessor authority remains live over this defect.

---

## 10. Hypothesis results

**A — stale canonical test expectation: REJECTED.** No canonical source
(DECISION_LOG, module docstring, code comment) indicates the
quantity-valuation warning was ever intentionally removed from
`execute_buy()`'s contract. On the contrary, M30.3's decision text and
impact accounting affirmatively describe it as built, wired, and green.

**B — production observability regression: CONFIRMED.** §8 establishes a
concrete mechanism (a divergent-branch merge, `c50b2cf`, dropping three of
four call sites while preserving the fourth) and a concrete before/after
(green at M30.3 completion per DECISION_LOG's own accounting; the call site
absent in the current file per direct grep). This is the operative finding.
A correction would require production mutation (§13/§9 of the request —
re-adding the dropped call site); no such mutation is made or authorized by
this act.

**C — logger/caplog capture-contract mismatch: REJECTED.** The identical
capture pattern (`caplog.at_level("WARNING", logger="services.portfolio_transactions")`)
is used one test later in the same module, against the same logger, for
`execute_dividend()`, and passes (`test_execute_dividend_unaffected_by_capability_mismatch`
— confirmed passing in the full-module run, §3). The harness, logger name,
and level are proven correct by a working sibling test in the same file.

**D — changed control-flow/semantic behavior: REJECTED.** The absence is
unconditional (the call site is simply not present in the function body),
not a branch that is no longer reached. `capability_lookup_service.resolve_capability_view()`
and `permits_quantity_valuation()` are unchanged and independently proven
correct by the passing unit-level test `test_quantity_valuation_mismatches_for_cash`,
which calls `_consult_runtime_for_transaction` directly and observes the
expected mismatch finding for a CASH-typed symbol.

**E — environment/order artifact: REJECTED, independently verified.**
Isolated single-test execution and full-10-test-module execution produced
byte-identical outcomes (§3) — same one failure, same message, same
business-result pass/fail split. This directly confirms the prior T4
report's isolation claim rather than merely trusting it.

**F — invalid/insufficient original T4 evidence: DOES NOT BLOCK
CLASSIFICATION.** See §12.

---

## 11. Canonical contract determination

The expected `RUNTIME_TRANSACTION_QUANTITY_VALUATION` warning is category
**(1) a required behavioral/observability invariant** — established
directly by DECISION_LOG M30.3 as an intentional, verified-green deliverable
of the platform's Stage R1 shadow-consultation program (the fourth of four
consumers: `ledger_validator.py`/M11, `asset_registry.py`/M12,
`portfolio_snapshots.py`/M30.2, `portfolio_transactions.py`/M30.3), not an
incidental diagnostic. It is not obsolete, not emitted under a changed
mechanism, and not merely unclassifiable — the evidence is unambiguous.

---

## 12. T4-evidence limitation and whether live evidence overcomes it

The original T4 artifact (`BANPU_WP8_REGRESSION_RESULTS.md`) does not
preserve the complete raw failure output required by frozen WPP §§9/16 —
that limitation is real and remains open (§14 below), but it does **not**
block this ownership classification. §§2–3 above reproduce the exact
failure directly from live test bytes (assertion text, line number, pass/
fail split, isolation vs. full-module identity), and §§7–8 establish origin
and root cause from live git history and the (unmodified, pre-existing)
DECISION_LOG — none of which depends on the T4 artifact's own completeness.
The T4 artifact was needed only to point at *which* test to investigate; the
classification itself rests on independently reproduced, primary evidence.

---

## 13. Technical defect classification

**Production observability regression**, introduced at merge commit
`c50b2cf` (2026-07-14, "Merge branch 'feature/runtime-adoption'"), which
silently dropped the `_log_runtime_consultation(db, symbol, tx.id,
"quantity_valuation", "execute_buy")` call (and its `execute_sell()` /
`execute_initial_position()` siblings) that commit `679e2ae` had added and
DECISION_LOG M30.3 had verified green, while the sibling
`execute_dividend()` call site — on a code path the conflicting branch did
not touch — survived. The test's expectation is canonical and correct; no
test-side change is indicated.

---

## 14. Ownership classification

**Classification B — new cross-package blocker package: `BANPU-T4-RB2`.**

- **Classification A (predecessor-owned) rejected:** no live predecessor
  authority owns this surface (§9). M30.3's own authority is not a standing
  BANPU package and is not live; RB-1's authority is exhausted/closed and
  textually scoped to an unrelated file/field.
- **Classification C (WP8-owned) rejected:** frozen WP8 authority
  (Allocation/Authorization/WPP) governs running and reporting T4, not
  authoring production corrections; using it here would be an expansion by
  interpretation, which this act is required to refuse.
- **Classification D (governance clarification/amendment required)
  rejected:** the technical picture is unambiguous and fully evidenced from
  live, primary sources (git history + DECISION_LOG, independently
  cross-checked); no frozen authority needs amending and no higher-order
  clarification is needed to know what happened or who should own fixing
  it. Classification D is reserved for genuine ambiguity, which is absent
  here.

RB-2 is therefore constituted as its own package, parallel to and
independent of RB-1, with RB-1 remaining untouched and exhausted (§15).

---

## 15. Rejected ownership alternatives

See §14. Summarized: A (no live predecessor), C (WP8 authority does not
stretch to production correction by interpretation), D (no unresolved
ambiguity exists to clarify).

---

## 16. Future mutation ceiling

Exactly one production call-site addition, in
**`backend/services/portfolio_transactions.py`, inside `execute_buy()`**,
placed immediately after `db.commit()`/`db.refresh()` and before
`_observe_transaction_execution_eligibility()` (mirroring the surviving
`execute_dividend()` placement at line 685):

```python
_log_runtime_consultation(db, symbol, tx.id, "quantity_valuation", "execute_buy")
```

No other line in `execute_buy()`, no test file, no fixture, and no other
production function may be mutated by an RB-2 correction under this
ceiling. No test-side change is authorized or anticipated — the existing
assertion is canonical (§11); it is expected to turn green once the
production call site is restored.

**Explicitly out of RB-2's ceiling, flagged only for future awareness:**
`execute_sell()` and `execute_initial_position()` carry the identical gap
(§4) but are not covered by any currently failing test (the module's own
"Coverage" docstring, §2, documents end-to-end coverage for only
`execute_buy()`/`execute_dividend()`) and are not part of the WP8-T4-observed
36 failures. Correcting them is not authorized, prohibited, or required by
this determination — it is a distinct, presently-untested gap a future
allocation may choose to address separately.

---

## 17. Future acceptance contract

A future RB-2 Allocation/Authorization/correction must prove, at minimum:

- `execute_buy()`'s transaction, holding, and cash-balance behavior is
  byte-identical before/after (no assertion in the existing test weakened
  or removed to obtain green);
- the restored call reproduces the exact `RUNTIME_TRANSACTION_QUANTITY_VALUATION`
  warning contract, captured deterministically by the existing
  `caplog.at_level(...)` pattern, with no skip/xfail/deselection anywhere;
- `test_portfolio_transactions_capability_shadow.py` is fully green in
  isolation and unchanged in the containing module (10/10);
- no unrelated production line changes (verified by `git diff --stat`
  scoped to the one authorized function);
- protected WP8/RB-1/WP7/M46 identities remain exact, matching this
  determination's §1 baseline;
- independent implementation review of the correction;
- Correction Confirmation;
- Correction Freeze;
- only after RB-2 is frozen, and only together with satisfying the
  separately open T4 evidence-completeness recovery prerequisite (§18), a
  fresh, unchanged, full 37-path WP8-T4 rerun.

None of these obligations are satisfied by this act; they are prospective
requirements for whatever act comes next.

---

## 18. Relationship to frozen RB-1

RB-1's seven governance/confirmation/freeze records and its exact three-file
implementation corpus are re-verified unchanged in §1 and remain exhausted/
closed. RB-2 shares no file, function, or test with RB-1's corpus
(`test_ledger_validator_effective.py`, `test_fee_accounting.py`,
`test_snapshot_coverage.py`) and requires no RB-1 mutation of any kind. No
technical dependency between RB-1 and RB-2 was found. RB-1 is not reopened
by this act.

---

## 19. T4 evidence-completeness state

Unchanged and separately open:

**`T4 EVIDENCE COMPLETENESS RECOVERY — OPEN`**

The original T4 artifact was not edited, replaced, or otherwise mutated by
this act. §12 records that this open limitation does not block the RB-2
ownership classification, but it remains an independent prerequisite that
must be satisfied (alongside RB-1 and RB-2 both being frozen) before any
future full WP8-T4 rerun.

---

## 20. Authority created by this act

This act creates a governance **determination** only: the existence,
ownership (`BANPU-T4-RB2`), technical classification, and future mutation
ceiling of the second WP8-T4 regression blocker. It creates **no
implementation authority** — no repository precedent inspected during this
act establishes implementation authority as automatically inseparable from
a determination of this class (contrast RB-1, where the Correction
Allocation and Implementation Authorization were separate, later, explicit
records). A distinct BANPU-T4-RB2 Correction Allocation, followed by its
own Implementation Authorization, is required before §16's ceiling may be
exercised.

---

## 21. Exact next lifecycle act

**BANPU-T4-RB2 Correction Allocation** — the next constitutionally valid
act is allocating correction ownership/scope for RB-2 (formally, on top of
this determination), followed in a later, separate act by its own
Implementation Authorization. Not: implementation, WP8-T4 rerun, WP8-T5, or
any RB-1 act.
