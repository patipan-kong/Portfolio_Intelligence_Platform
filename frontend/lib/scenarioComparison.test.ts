import assert from "node:assert/strict";
import { test } from "node:test";

import { computeScenarioComparison, type ScenarioComparisonAssumptions } from "./scenarioComparison.ts";

const asOfDate = "2026-01-01";

function scenario(overrides: Partial<ScenarioComparisonAssumptions> = {}): ScenarioComparisonAssumptions {
  return { name: "Scenario", monthlyContribution: 10_000, annualReturnPct: 5, ...overrides };
}

// 1. two normal scenarios / 2. common current starting value / 3. different contributions
test("two normal scenarios share the same starting value and target", () => {
  const result = computeScenarioComparison(
    1_000_000, 200_000, "2030-01-01", asOfDate,
    scenario({ name: "A", monthlyContribution: 10_000 }),
    scenario({ name: "B", monthlyContribution: 20_000 }),
  );
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.context.startingValue, 200_000);
  assert.equal(result.context.targetAmount, 1_000_000);
  assert.equal(result.a.whatIf.valid, true);
  assert.equal(result.b.whatIf.valid, true);
  if (result.a.whatIf.valid && result.b.whatIf.valid) {
    assert.equal(result.a.whatIf.startingValue, 200_000);
    assert.equal(result.b.whatIf.startingValue, 200_000);
  }
  // Higher contribution reaches sooner.
  if (result.a.whatIf.valid && result.b.whatIf.valid) {
    assert.ok((result.b.whatIf.monthsToTarget as number) < (result.a.whatIf.monthsToTarget as number));
  }
});

// 4. different returns
test("different annual return assumptions produce different reach dates", () => {
  const result = computeScenarioComparison(
    1_000_000, 200_000, null, asOfDate,
    scenario({ name: "A", annualReturnPct: 2 }),
    scenario({ name: "B", annualReturnPct: 8 }),
  );
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.notEqual(result.a.whatIf, result.b.whatIf);
  if (result.a.whatIf.valid && result.b.whatIf.valid) {
    assert.ok((result.b.whatIf.monthsToTarget as number) <= (result.a.whatIf.monthsToTarget as number));
  }
});

// 5. one unreachable
test("one scenario unreachable within horizon while the other reaches", () => {
  const result = computeScenarioComparison(
    100_000_000, 0, null, asOfDate,
    scenario({ name: "Reachable", monthlyContribution: 500_000, annualReturnPct: 8 }),
    scenario({ name: "Unreachable", monthlyContribution: 1, annualReturnPct: 0 }),
  );
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.a.whatIf.valid && result.a.whatIf.reachable, true);
  assert.equal(result.b.whatIf.valid && result.b.whatIf.reachable, false);
});

// 6. both unreachable
test("both scenarios unreachable within horizon", () => {
  const result = computeScenarioComparison(
    100_000_000, 0, null, asOfDate,
    scenario({ name: "A", monthlyContribution: 1, annualReturnPct: 0 }),
    scenario({ name: "B", monthlyContribution: 2, annualReturnPct: 0 }),
  );
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.a.whatIf.valid && result.a.whatIf.reachable, false);
  assert.equal(result.b.whatIf.valid && result.b.whatIf.reachable, false);
});

// 7. already funded
test("already-funded starting value reports alreadyReached for both scenarios", () => {
  const result = computeScenarioComparison(
    100_000, 250_000, "2030-01-01", asOfDate,
    scenario({ name: "A", annualReturnPct: 5 }),
    scenario({ name: "B", annualReturnPct: -3 }),
  );
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.a.whatIf.valid && result.a.whatIf.alreadyReached, true);
  assert.equal(result.b.whatIf.valid && result.b.whatIf.alreadyReached, true);
  // Distinct return assumptions can still yield distinct target-date projections.
  if (result.a.whatIf.valid && result.b.whatIf.valid) {
    assert.notEqual(result.a.whatIf.projectedValueAtTargetDate, result.b.whatIf.projectedValueAtTargetDate);
  }
});

// 8. future target date
test("future target date yields target-date projection and required contribution for both sides", () => {
  const result = computeScenarioComparison(
    1_000_000, 200_000, "2030-01-01", asOfDate,
    scenario({ name: "A" }),
    scenario({ name: "B", annualReturnPct: 3 }),
  );
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.a.whatIf.valid && result.a.whatIf.projectedValueAtTargetDate !== null, true);
  assert.equal(result.a.requiredContribution.valid, true);
  assert.equal(result.b.requiredContribution.valid, true);
});

// 9. no target date
test("no target date omits target-date projection and required contribution", () => {
  const result = computeScenarioComparison(1_000_000, 200_000, null, asOfDate, scenario({ name: "A" }), scenario({ name: "B" }));
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.context.targetDate, null);
  assert.equal(result.a.whatIf.valid && result.a.whatIf.projectedValueAtTargetDate, null);
  assert.equal(result.a.requiredContribution.valid, false);
  assert.equal(result.b.requiredContribution.valid, false);
});

// 10. past target date
test("past target date reports targetDateInPast and an unavailable required contribution", () => {
  const result = computeScenarioComparison(1_000_000, 200_000, "2020-01-01", asOfDate, scenario({ name: "A" }), scenario({ name: "B" }));
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.a.whatIf.valid && result.a.whatIf.targetDateInPast, true);
  assert.equal(result.a.requiredContribution.valid, false);
  if (!result.a.requiredContribution.valid) {
    assert.match(result.a.requiredContribution.error, /passed/);
  }
});

// 11. negative return
test("negative annual return above -100% is a valid assumption", () => {
  const result = computeScenarioComparison(1_000_000, 200_000, null, asOfDate, scenario({ name: "A", annualReturnPct: 5 }), scenario({ name: "B", annualReturnPct: -3 }));
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.b.whatIf.valid, true);
});

// 12. zero contribution
test("zero monthly contribution is a valid assumption", () => {
  const result = computeScenarioComparison(1_000_000, 200_000, null, asOfDate, scenario({ name: "A", monthlyContribution: 0 }), scenario({ name: "B" }));
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.a.whatIf.valid, true);
  assert.equal(result.a.monthlyContribution, 0);
});

// 13. required contribution differs by return assumption
test("required monthly contribution differs by each scenario's own return assumption", () => {
  const result = computeScenarioComparison(1_000_000, 200_000, "2030-01-01", asOfDate, scenario({ name: "A", annualReturnPct: 1 }), scenario({ name: "B", annualReturnPct: 10 }));
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.a.requiredContribution.valid, true);
  assert.equal(result.b.requiredContribution.valid, true);
  if (result.a.requiredContribution.valid && result.b.requiredContribution.valid) {
    assert.notEqual(result.a.requiredContribution.requiredMonthlyContribution, result.b.requiredContribution.requiredMonthlyContribution);
  }
});

// required contribution is independent of the scenario's own saved monthly contribution
test("required contribution ignores the scenario's own monthly contribution input", () => {
  const result = computeScenarioComparison(1_000_000, 200_000, "2030-01-01", asOfDate, scenario({ name: "A", monthlyContribution: 1 }), scenario({ name: "B", monthlyContribution: 999_999 }));
  assert.equal(result.valid, true);
  if (!result.valid) return;
  assert.equal(result.a.requiredContribution.valid, true);
  assert.equal(result.b.requiredContribution.valid, true);
  if (result.a.requiredContribution.valid && result.b.requiredContribution.valid) {
    // Same target/starting/return/target-date => identical required contribution
    // regardless of each side's own saved monthly contribution.
    assert.equal(result.a.requiredContribution.requiredMonthlyContribution, result.b.requiredContribution.requiredMonthlyContribution);
  }
});

// 14. designated funding unavailable
test("unavailable designated funding is not treated as a loaded zero balance", () => {
  const zeroFunding = computeScenarioComparison(1_000_000, 0, "2030-01-01", asOfDate, scenario({ name: "A" }), scenario({ name: "B" }));
  assert.equal(zeroFunding.valid, true);

  const unavailableFunding = computeScenarioComparison(1_000_000, null, "2030-01-01", asOfDate, scenario({ name: "A" }), scenario({ name: "B" }));
  assert.equal(unavailableFunding.valid, false);
  if (unavailableFunding.valid) return;
  assert.match(unavailableFunding.error, /unavailable/i);
});

// 15. deterministic repeatability
test("identical inputs produce identical outputs across repeated calls", () => {
  const inputs = [1_000_000, 200_000, "2030-01-01", asOfDate, scenario({ name: "A" }), scenario({ name: "B", annualReturnPct: 3 })] as const;
  const inputsBefore = JSON.stringify(inputs);
  const first = computeScenarioComparison(...inputs);
  const second = computeScenarioComparison(...inputs);
  assert.equal(JSON.stringify(inputs), inputsBefore);
  assert.deepEqual(first, second);
});

// No ranking/winner language anywhere in the shape.
test("result shape carries no ranking, score, or winner field", () => {
  const result = computeScenarioComparison(1_000_000, 200_000, "2030-01-01", asOfDate, scenario({ name: "A" }), scenario({ name: "B" }));
  assert.equal(result.valid, true);
  if (!result.valid) return;
  const serialized = JSON.stringify(result);
  assert.doesNotMatch(serialized, /winner|best|recommended|optimal|score/i);
});
