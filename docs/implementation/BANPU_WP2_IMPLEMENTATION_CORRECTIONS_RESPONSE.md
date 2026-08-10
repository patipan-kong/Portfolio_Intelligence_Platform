# BANPU-WP2 — Implementation Corrections Response

**Artifact class:** Implementation corrections response (BANPU-WP2 governance
corpus)
**Date:** 2026-08-07
**Issuing role:** WP2 Implementation Owner
**Review consumed:** BANPU-WP2 — Step 9 Independent Implementation Review
(2026-08-07), baseline `feature/m46-banpu-remediation @ 451ab85` + working
tree, disposition **BLOCKED — IMPLEMENTATION CONFIRMATION CANNOT PROCEED
(3 CRITICAL, 3 MAJOR)**
**This response's disposition:** 6 ACCEPTED, 5 GOVERNANCE REFERRAL,
1 DEFERRED, 0 REJECTED

---

## 1. Scope and authority

This response is issued under WP2 Implementation Owner authority only.

- The Independent Implementation Review is treated as authoritative in
  full. No execution evidence in the review is challenged, re-tested, or
  re-derived here.
- The review's text is not restated in full and is not rewritten; each
  finding below is answered, not reproduced.
- Accepted findings are corrected **within the existing frozen
  specification only** — no redesign, no scope widening, no new work.
- Governance findings are **referred, not decided** — no disposition is
  chosen on this owner's authority for any finding requiring a
  specification interpretation, wording amendment, or acceptance-criterion
  decision.
- This response modifies no production code, creates no implementation,
  and creates no tests. It is not committed.

## 2. Findings register

| Finding ID | Disposition |
|---|---|
| CRITICAL-1 | ACCEPTED |
| CRITICAL-2 | ACCEPTED |
| CRITICAL-3 | ACCEPTED |
| MAJOR-1 | ACCEPTED |
| MAJOR-2 | ACCEPTED |
| MAJOR-3 | GOVERNANCE REFERRAL |
| MINOR-1 | ACCEPTED |
| MINOR-2 | GOVERNANCE REFERRAL |
| MINOR-3 | GOVERNANCE REFERRAL |
| MINOR-4 | GOVERNANCE REFERRAL |
| MINOR-5 | DEFERRED |
| MINOR-6 | GOVERNANCE REFERRAL |

The review's un-IDed OBSERVATIONS are noted as read; they carry no
required disposition in the review and none is assigned here.

## 3. Per-finding disposition

### CRITICAL-1 — Same-day conversion chain ordering dependency

- **Disposition:** ACCEPTED
- **Technical reasoning:** `_SAME_DAY_CONFLICT_TYPES`
  (`portfolio_rebuilder.py:402`) and `_CONVERSION_SAME_DAY_TYPES`
  (`ledger_validator.py:676`) both exclude `POSITION_CONVERSION`, on the
  false premise that a same-day chain is separately caught as
  `POSITION_CONVERSION_DUPLICATE`. The duplicate key is
  `(predecessor_asset_id, transition_date)`, so a chain X→Y then Y→Z on one
  date has two distinct keys and is not caught. The executed probe shows
  the accepted/rejected outcome is determined purely by transaction-ID
  order for identical economic facts.
- **Constitutional reasoning:** Direct violation of §4.1(1) and its
  governing principle that transaction-ID order cannot resolve an
  otherwise ambiguous affected-asset sequence, and of §9.2's
  `SAME_DAY_CONFLICT` predicate and AC10.
- **Planned implementation scope:** Add `POSITION_CONVERSION` to the
  same-day conflict predicate in both engines, excluding the row itself
  and preserving `DUPLICATE` precedence for the identical key, exactly as
  the review's Required disposition states. Add positive fixtures for both
  orderings on the same transition date. The implementation will be
  corrected within the existing frozen specification; no redesign, no
  scope widening, no new work beyond this correction.
- **Planning artifacts requiring amendment:** None. §4.1 and §9.2 already
  state the required rule; this is a conformance fix.

### CRITICAL-2 — Top-level compatibility projections never validated

- **Disposition:** ACCEPTED
- **Technical reasoning:** `_preflight_position_conversions`
  (`portfolio_rebuilder.py:405`) performs no projection check; the
  validator checks `total_amount`/`fees`/`taxes` only when
  `payload.cash_in_lieu` is not `None`. Top-level `shares` and
  `price_per_share`, and the null-cash-leg case, are checked nowhere. The
  executed probe shows a row with fabricated `shares`, `price_per_share`,
  `total_amount`, `fees`, and `taxes` replays clean with zero findings.
- **Constitutional reasoning:** Violates §4's absolute-tolerance
  comparison requirement, §7.1 preflight requirement 4, and the §9.2
  `SHARE_MISMATCH`, `BASIS_MISMATCH`, and `CIL_INVALID` predicates; AC11
  requires cash-in-lieu-invalid cases be unable to commit.
- **Planned implementation scope:** Implement the §4 projection comparison
  for all five top-level fields in both engines, including the
  null-cash-leg consistency rule, mapped to the §9.2 predicates as
  specified — exactly the review's Required disposition. No additional
  scope.
- **Planning artifacts requiring amendment:** None. §4, §7.1, and §9.2
  already specify this; the gap is implementation-only.

### CRITICAL-3 — Native-mode null-asset fallback splits the successor holding

- **Disposition:** ACCEPTED
- **Technical reasoning:** The successor is keyed by
  `payload.successor.asset_id` only when `predecessor_key` is `int`. Under
  the §5.3 historical null-asset fallback, the predecessor resolves via
  the symbol tier, so the successor is symbol-keyed — but `replay_key()`
  returns `asset_id` for a later native-mode trade on that successor. The
  executed probe shows this splits one economic holding into two
  same-symbol keys, which `_reconcile_portfolio_items` re-keys by
  `report_symbol` and silently drops one of, and which `_commit_rebuild`
  would stage as two rows violating `uq_portfolio_symbol`.
- **Constitutional reasoning:** Violates §7.4 (legacy and native modes must
  produce identical reported economic state) and AC7/AC8. This is
  precisely the transaction-83 scenario §5.3 exists to serve.
- **Planned implementation scope:** Key the created successor by
  `payload.successor.asset_id` whenever the run resolves asset IDs at all,
  independent of which tier resolved the predecessor. Add a native-mode
  fallback plus subsequent-successor-trade fixture. Exactly the review's
  Required disposition; no additional design.
- **Planning artifacts requiring amendment:** None. §7.4 and §5.3 already
  specify the required parity; the gap is implementation-only.

### MAJOR-1 — Reconciliation ignores asset-ID-precedence pairing

- **Disposition:** ACCEPTED
- **Technical reasoning:** `_resolve_conversion_successors`
  (`portfolio_rebuilder.py:548`) correctly implements §8's
  asset-first/symbol-fallback pairing, but `_reconcile_portfolio_items`
  discards that paired item and re-pairs by symbol only, producing
  MISSING/EXTRA rows against the wrong comparand instead of the five
  required field-level `DIFFERENT` rows.
- **Constitutional reasoning:** Violates §8 pairing rules 1 and 4 and the
  requirement that "every actual field delta is visible" before commit,
  and AC14.
- **Planned implementation scope:** Pair reconciliation on the
  already-computed paired item from `_resolve_conversion_successors`;
  emit the five required rows against it. Add the differing-symbol
  fixture named in the review. Exactly the review's Required disposition.
- **Planning artifacts requiring amendment:** None. §8 already specifies
  the required pairing and row behavior; this is a conformance fix.

### MAJOR-2 — Validator-side five-field conversion comparison absent

- **Disposition:** ACCEPTED
- **Technical reasoning:** `_check_holdings_consistency`
  (`ledger_validator.py:1303`) remains symbol-keyed and shares-only.
  `state.basis`/`state.identity` are tracked but consumed nowhere outside
  conversion candidate resolution.
- **Constitutional reasoning:** §6.2's required change is unimplemented
  with no recorded residual, weakening §5.2's independence gate — the
  validator cannot corroborate the rebuilder's Stage 4 conclusion.
- **Planned implementation scope:** Extend the validator's holdings
  consistency check for conversion portfolios to compare by asset ID,
  symbol, shares, average cost, and basis, per §6.2's literal text. The
  review names this as one of two available options (the other being a
  recorded governance residual); this response elects the implementation
  option, consistent with the review's own "Return to implementation"
  recommendation for MAJOR-2. No additional design beyond §6.2's stated
  requirement.
- **Planning artifacts requiring amendment:** None. §6.2 already specifies
  the requirement; the gap is implementation-only.

### MAJOR-3 — SAME_DAY_CONFLICT Stage 5 gate unreachable; §10 disposition not produced

- **Disposition:** GOVERNANCE REFERRAL
- **Technical reasoning:** `_has_conversion_blocking_error`
  (`portfolio_rebuilder.py:615`) fires only on a validator-reported
  `SAME_DAY_CONFLICT` at Stage 5, but rebuilder preflight raises first, so
  the gate is never reached through the real pipeline; the only test
  exercising it patches in a synthetic validator report. The code comment
  at line 610 is also stale.
- **Constitutional reasoning:** §9.1 marks `SAME_DAY_CONFLICT` as
  Stage-5-blocking, but no real input reaches it. §10 prescribes two
  mutually exclusive dispositions; the implementation has chosen bullet 1
  (preflight precedence) without a recorded deviation, and AC18 is
  asserted against the wrong bucket. Choosing between "accept preflight
  precedence and amend §10/§9.1 wording" versus "move the same-day
  predicate into the Stage 5 gate" is a specification decision, not an
  implementation correction — this owner does not decide it.
- **Planned implementation scope:** None pending governance decision. The
  stale code comment at line 610 will be corrected regardless of which
  option governance selects, since the review states this correction
  applies "either way" and requires no design choice. Note for governance:
  this finding is coupled to CRITICAL-1 — once `POSITION_CONVERSION` is
  added to the same-day predicate under CRITICAL-1's correction, the same
  preflight-vs-Stage-5 precedence question will apply to the corrected
  predicate as well, so resolution of MAJOR-3 is best sequenced after
  CRITICAL-1 lands.
- **Planning artifacts requiring amendment:** Yes, pending governance
  choice — either §10/§9.1 wording is amended to reflect preflight
  precedence, or the same-day predicate is relocated to the Stage 5 gate.
  Referred to governance for decision; not decided here.

### MINOR-1 — Rebuilder/validator divergence on NULL top-level asset_id

- **Disposition:** ACCEPTED
- **Technical reasoning:** The rebuilder fails closed on
  `raw.asset_id != payload.predecessor.asset_id` (`portfolio_rebuilder.py:435`).
  The validator's equivalent guard (`raw_asset_id is not None and ...`,
  `ledger_validator.py:771`) skips the check entirely for a genuine `NULL`
  value, not only for the test-shim case its docstring describes — the
  validator fails open where the rebuilder fails closed.
- **Constitutional reasoning:** This divergence undermines §5.2's
  independent-corroboration goal: the two independently implemented
  engines should reach the same accept/reject conclusion for the same
  input.
- **Planned implementation scope:** Align the validator's NULL top-level
  `asset_id` guard to fail closed, consistent with the rebuilder's
  existing check. No new predicate is introduced and no scope is widened —
  this brings the validator's behavior into line with a check the
  rebuilder already implements.
- **Planning artifacts requiring amendment:** None. No specification value
  changes; this is a cross-engine consistency fix.

### MINOR-2 — Basis conservation not exact under non-terminating decimal division

- **Disposition:** GOVERNANCE REFERRAL
- **Technical reasoning:** `_HoldingState` derives basis as
  `shares × avg_cost` rather than retaining it as an independent field. The
  executed probe (existing successor 3 shares @ 100/3) shows a ~1e-27
  relative residual against §7.3's stated invariant
  (`combined_shares × combined_avg_cost = combined_basis`), which the
  review characterizes as economically inert and far inside the existing
  THB 0.01 tolerance used elsewhere in the specification.
- **Constitutional reasoning:** §7.3 states the invariant as exact
  equality. Whether the frozen specification intends literal exact
  equality (which is not achievable for non-terminating Decimal division
  without a structural change) or is to be read under the tolerance
  conventions already established elsewhere in the spec (e.g., §4's
  absolute tolerance) is a specification-interpretation question, not an
  implementation defect. This owner does not decide it.
- **Planned implementation scope:** None pending governance decision.
- **Planning artifacts requiring amendment:** Possibly — §7.3 may need
  explicit tolerance wording, or governance may affirm the invariant is
  non-blocking as measured. Referred to governance; not decided here.

### MINOR-3 — Freeze-identity convention not reproducible as stated

- **Disposition:** GOVERNANCE REFERRAL
- **Technical reasoning:** The measured claim in
  `BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md` — that LF-normalized
  SHA-256 is "the only single, uniform rule" reproducing the Freeze
  Record's values "with zero exceptions" — does not hold:
  `transaction_canonicalizer.py` and `test_transaction_canonicalizer.py`
  carry CRLF on every line and match the Freeze Record under raw CRLF
  bytes, not LF bytes. The rule holds for 10 of 12 files, not 12 of 12.
  All 12 files remain intact under their applicable convention, and WP2
  changed none of them.
- **Constitutional reasoning:** This is a WP1 freeze-identity governance
  matter, not a WP2 implementation matter; the review itself states this
  explicitly and states it does not block WP2. For governance's context:
  `BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md` was never approved: the
  currently-authoritative WP1 disposition for the identity residual is
  `BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md` (approved) together with the
  Architecture Owner Determination exercising its §8 Path B — neither of
  which asserts a "zero exceptions" universal normalization rule. This
  owner does not decide how governance should treat the unapproved
  correction record; the observation is provided for routing only.
- **Planned implementation scope:** None. No WP2 file is affected by this
  finding.
- **Planning artifacts requiring amendment:** Referred to WP1
  freeze-identity governance to determine the disposition of
  `BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md`'s unapproved claim; not
  decided here.

### MINOR-4 — Deferred catalog IDs absent

- **Disposition:** GOVERNANCE REFERRAL
- **Technical reasoning:** `POSITION_CONVERSION_REBUILD_BOUNDARY` and
  `POSITION_CONVERSION_QUOTE_QUARANTINED` appear nowhere in `backend/`.
  `ledger_validator.py` has no catalogue data structure to add them to.
- **Constitutional reasoning:** §9.1/§5.4 require catalogue presence with
  dormant predicates, and WP2-T2 requires them "asserted as catalogued."
  Adding a catalogue data structure where none currently exists is new
  structural work, which this owner's authority explicitly excludes ("do
  not introduce new work"); whether that work is authorized, and under
  what scope, is a governance decision.
- **Planned implementation scope:** None pending governance decision.
- **Planning artifacts requiring amendment:** Possibly — §9.1/§5.4/WP2-T2
  wording, or a recorded carried-forward residual, depending on
  governance's decision. Referred to governance; not decided here.

### MINOR-5 — Successor-symbol keying collision

- **Disposition:** DEFERRED
- **Technical reasoning:** `_resolve_conversion_successors` is keyed by
  successor symbol; two conversions sharing one successor symbol would
  silently overwrite one another. The review states this is "unreachable
  today," with CRITICAL-1's same-day chain case as its nearest neighbour.
- **Constitutional reasoning:** No currently reachable code path exercises
  this condition. The review issues no Required disposition for this
  finding, consistent with it being non-blocking and not presently
  actionable.
- **Planned implementation scope:** Deferred. No implementation action is
  taken now. Once CRITICAL-1's correction (adding `POSITION_CONVERSION` to
  the same-day conflict predicate) lands, reachability of a
  same-successor-symbol collision must be reassessed; if it remains
  reachable, it is to be re-raised as a new finding for disposition at
  that time.
- **Planning artifacts requiring amendment:** None at this time.

### MINOR-6 — Mandatory regression owners give no WP2 signal

- **Disposition:** GOVERNANCE REFERRAL
- **Technical reasoning:** `test_ledger_validator_effective.py` (22
  failures) and `test_replay_cutover.py` (9 failures) are red at baseline,
  verified byte-identical against a clean HEAD worktree — pre-existing,
  not WP2-introduced.
- **Constitutional reasoning:** AC19 requires zero regressions from these
  owners but is not literally satisfiable while they are red at baseline.
  WP2 introduces zero regressions (demonstrated), but no WP2 change can
  make AC19's literal text satisfiable, since the pre-existing failures
  are outside WP2's frozen specification and allowlist. Whether AC19's
  wording is amended (e.g., to "zero WP2-introduced regressions," matching
  demonstrated evidence) or the condition is accepted as a carried-forward
  residual is a governance decision.
- **Planned implementation scope:** None. No WP2 file change can address
  pre-existing baseline failures outside the WP2 allowlist.
- **Planning artifacts requiring amendment:** Referred to governance to
  determine how AC19 is satisfied given pre-existing baseline failures;
  not decided here.

## 4. Summary disposition

- **ACCEPTED (6):** CRITICAL-1, CRITICAL-2, CRITICAL-3, MAJOR-1, MAJOR-2,
  MINOR-1. Each will be corrected within the existing frozen
  specification, exactly as the review's own Required disposition states
  for each, with no redesign, no scope widening, and no new work.
- **GOVERNANCE REFERRAL (5):** MAJOR-3, MINOR-2, MINOR-3, MINOR-4,
  MINOR-6. None of these is decided by this response; each is referred to
  governance for disposition.
- **DEFERRED (1):** MINOR-5, pending reassessment after CRITICAL-1's
  correction lands.
- **REJECTED (0):** No finding is rejected; the review's execution
  evidence is not challenged.

## 5. Exact next constitutional act

Implementation correction of the six ACCEPTED findings, within the
existing frozen specification and the two already-allowlisted production
files, followed by re-entry into BANPU-WP2 Step 9 (Independent
Implementation Review) on the corrected candidate. The five
GOVERNANCE REFERRAL findings and the one DEFERRED finding remain open in
parallel and do not block the correction-and-resubmission cycle for the
ACCEPTED findings.
