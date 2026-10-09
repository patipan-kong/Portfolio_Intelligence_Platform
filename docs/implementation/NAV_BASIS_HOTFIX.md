# Optimizer NAV-Basis Correctness Hotfix

**Date:** 2026-10-09 · **Trigger:** optimizer history 219 / snapshot 175 · **Status:** implemented, not committed
**Decision record:** `docs/engineering/DECISION_LOG.md` → "Optimizer NAV-Basis Correctness Hotfix"

## Invariants

1. **One weight source.** `services/optimizer/nav_basis.compute_nav_basis()`; `agents.optimizer._compute_portfolio_weights(items, cash_balance)` wraps it. No second formula.
2. **NAV = Σ(shares × price) + cash**; price = live quote, else average cost (unchanged rule). Position weight = value / NAV × 100.
3. **Full precision in calculations.** `weight_pct`, breach comparisons and evidence use unrounded floats. Rounding only at established output contracts: allocation rows (`current_weight`/`target_weight` 2 dp), L1 prompt `w` (1 dp), prompt `weight_pct` (2 dp), valuation persisted at 2 dp.
4. Allocation delta and amount: `target − current_weight` (both NAV) and `delta% × total_value` (NAV). Flag-independent. With the advisory flag on, the frozen-quote canonical weights still override the row/prompt weights (they agree with the shared weights to display precision).
5. Unchanged: thresholds; hard-policy and DR execution caps clamp BUY/ACCUMULATE targets only (no automatic liquidation); DR basket 40% is advisory; Investor Intent never blocks or overrides.

## Evidence contract (`active_policy.violation_evidence`)

Additive list; its **presence (even `[]`) marks an evidence-aware run**. Entry:

```
{evidence_version: "wealth.policy-evidence.v1", type: "CONCENTRATION_BREACH", scope: "SINGLE_POSITION",
 rule: "hard_constraints.max_single_position_pct", symbol, basis: "NAV",
 position_value, nav, cash, observed_pct, limit_pct}
```

`POLICY_ENFORCEMENT` for a single position requires: matching symbol/type/scope/rule; `basis == "NAV"`; entry `nav`/`cash` equal the payload's `total_value`/`cash_balance` (±0.011); `position_value / nav × 100` equals `observed_pct` and is strictly greater than the payload's limit; and the allocation row's `current_weight` within 0.05pp. Any failure → `PORTFOLIO_IMPROVEMENT` / `DISCRETIONARY` with `evidence_status: UNVERIFIED` and a reason code in `evidence_detail`. Violation strings, model claims and labels are never inputs.

`OptimizedTrade.evidence_status`: `NOT_APPLICABLE | VERIFIED_NAV | UNVERIFIED | LEGACY_RECORDED_UNVERIFIED | SECTOR_EQUITY_BASIS`.

## Historical behavior

Stored runs (217/218/219) are never rewritten. `execution_optimization` is not stored; history reads derive it. A payload **without** `violation_evidence` is reproduced under its original string rule and marked `LEGACY_RECORDED_UNVERIFIED` ("Required (as recorded)" + qualifier in the UI). No current policy evidence or current Intent is attached. Runs without Intent review evidence show "Intent review not captured".

## Known limitation

Sector current/projected weights and sector limits remain equity-only (`policy_engine._detect_violations` sector block, `compute_concentration_breach_severity`, `calculate_current_sector_weights`) while L2 targets are NAV based. Sector-driven Required trades are qualified `SECTOR_EQUITY_BASIS`. A follow-up decision is needed before converting sectors.

## Tests

Backend `tests/test_nav_basis_hotfix.py` (history 219 fixture `tests/fixtures/history_219_nav_basis.json`; AI stubbed). Frontend `tests/decisionLookup.test.ts`, `DecisionActionPanel.test.tsx`, `AdvisoryIntentReviewCard.test.tsx`, `ExecutionPlanCard.test.tsx`.

## Report Card provenance (follow-up)

- `read_snapshot_plan_inputs` adds an additive `policy_provenance` (stored `violation_evidence` or `None`, the limit, run `total_value`/`cash_balance`). `compute_plan_grade` does not read it.
- `derive_full_plan(..., policy_provenance=…)` delegates to `optimize_execution_for_payload` **only when the caller passes it**. Only `recommendation_ledger.get_report_card` does, so the Report Card, the optimizer page and history reads use one classifier.
- For every stored run (none carries `violation_evidence`) the delegation reproduces the legacy derivation exactly (test: trades and buy trades identical for 217/218/219), so funding order, amounts and states do not change.
- Shared wording lives in `frontend/lib/tradeProvenance.ts`: `Required`, `Required (as recorded)`, `Required (equity-basis)`, plus the UNVERIFIED qualifier.

**Remaining grader limitation (explicit, unchanged):** the plan grade, funding-order analytics, opportunity cost, execution ledger, human-vs-AI and plan-vs-actual analyzer still call `derive_full_plan` without provenance, i.e. the legacy string rule. For a future evidence-aware run whose concentration claim fails NAV verification they would still treat the trade as Required while the optimizer page and Report Card do not. Persisted PLAN grades are reproducible from their stored arguments and were deliberately not re-based. Converting them needs an evaluation-semantics decision.
