import assert from "node:assert/strict";
import { test } from "node:test";

import {
  computeGoalWhatIf,
  computeRequiredMonthlyContribution,
  formatMonthLabel,
  type GoalWhatIfInput,
  type GoalWhatIfValid,
  type RequiredMonthlyContributionInput,
  type RequiredMonthlyContributionValid,
} from "./goalWhatIf.ts";

function input(overrides: Partial<GoalWhatIfInput> = {}): GoalWhatIfInput {
  return {
    targetAmount: 1_000_000,
    startingValue: 0,
    monthlyContribution: 10_000,
    annualReturnPct: 0,
    asOfDate: "2026-08-01",
    targetDate: null,
    ...overrides,
  };
}

function assertValid(result: ReturnType<typeof computeGoalWhatIf>): asserts result is GoalWhatIfValid {
  assert.equal(result.valid, true, (result as { error?: string }).error);
}

function inverseInput(overrides: Partial<RequiredMonthlyContributionInput> = {}): RequiredMonthlyContributionInput {
  return {
    targetAmount: 1_000_000,
    startingValue: 0,
    annualReturnPct: 0,
    asOfDate: "2026-01-15",
    targetDate: "2027-01-15",
    ...overrides,
  };
}

function assertInverseValid(
  result: ReturnType<typeof computeRequiredMonthlyContribution>,
): asserts result is RequiredMonthlyContributionValid {
  assert.equal(result.valid, true, (result as { error?: string }).error);
}

function assertInverseIsForwardMinimal(inverse: RequiredMonthlyContributionInput): RequiredMonthlyContributionValid {
  const result = computeRequiredMonthlyContribution(inverse);
  assertInverseValid(result);
  const forward = computeGoalWhatIf({
    ...inverse,
    monthlyContribution: result.requiredMonthlyContribution,
  });
  assertValid(forward);
  assert.equal(forward.projectedValueAtTargetDate, result.projectedValueAtTargetDate);
  assert.ok(result.projectedValueAtTargetDate >= result.targetAmount);

  if (result.requiredMonthlyContribution > 0) {
    const previousSatang = Math.round(result.requiredMonthlyContribution * 100) - 1;
    const previous = computeGoalWhatIf({
      ...inverse,
      monthlyContribution: previousSatang / 100,
    });
    assertValid(previous);
    assert.ok((previous.projectedValueAtTargetDate as number) < result.targetAmount);
  }
  return result;
}

// ─── already reached / over-funded ──────────────────────────────────────────

test("already fully funded: alreadyReached, reachable, 0 months, reachDate = asOfDate month", () => {
  const result = computeGoalWhatIf(input({ startingValue: 1_000_000, targetAmount: 1_000_000 }));
  assertValid(result);
  assert.equal(result.alreadyReached, true);
  assert.equal(result.reachable, true);
  assert.equal(result.monthsToTarget, 0);
  assert.equal(result.reachDate, "2026-08");
});

test(">100% funded (starting value exceeds target) is also already reached", () => {
  const result = computeGoalWhatIf(input({ startingValue: 1_200_000, targetAmount: 1_000_000 }));
  assertValid(result);
  assert.equal(result.alreadyReached, true);
  assert.equal(result.monthsToTarget, 0);
});

// ─── zero / positive contribution ───────────────────────────────────────────

test("zero starting, zero contribution, zero return: never reachable", () => {
  const result = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 0, annualReturnPct: 0 }));
  assertValid(result);
  assert.equal(result.alreadyReached, false);
  assert.equal(result.reachable, false);
  assert.equal(result.monthsToTarget, null);
  assert.equal(result.reachDate, null);
});

test("zero starting, positive contribution: reaches target eventually", () => {
  const result = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 50_000, annualReturnPct: 0, targetAmount: 600_000 }));
  assertValid(result);
  assert.equal(result.reachable, true);
  assert.equal(result.monthsToTarget, 12);
  assert.equal(result.reachDate, "2027-08");
});

// ─── 0% return: exact linear math ───────────────────────────────────────────

test("0% return is exactly linear: contribution * months", () => {
  const result = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 1_000, annualReturnPct: 0, targetAmount: 12_000 }));
  assertValid(result);
  assert.equal(result.monthsToTarget, 12);
});

// ─── positive / negative return compounding ─────────────────────────────────

test("positive return compounds: fewer months needed than the 0% case", () => {
  const zeroReturn = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 10_000, annualReturnPct: 0, targetAmount: 500_000 }));
  const positiveReturn = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 10_000, annualReturnPct: 8, targetAmount: 500_000 }));
  assertValid(zeroReturn);
  assertValid(positiveReturn);
  assert.ok((positiveReturn.monthsToTarget as number) < (zeroReturn.monthsToTarget as number));
});

test("negative return: allowed, and requires more months than the 0% case", () => {
  const zeroReturn = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 10_000, annualReturnPct: 0, targetAmount: 500_000 }));
  const negativeReturn = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 10_000, annualReturnPct: -5, targetAmount: 500_000 }));
  assertValid(zeroReturn);
  assertValid(negativeReturn);
  assert.equal(negativeReturn.valid, true);
  assert.ok((negativeReturn.monthsToTarget as number) > (zeroReturn.monthsToTarget as number));
});

test("annual return of exactly -100% (or lower) is rejected, not silently clamped", () => {
  const result = computeGoalWhatIf(input({ annualReturnPct: -100 }));
  assert.equal(result.valid, false);
  const result2 = computeGoalWhatIf(input({ annualReturnPct: -150 }));
  assert.equal(result2.valid, false);
});

// ─── reach-date precision ────────────────────────────────────────────────────

test("target reached on the exact month, not one month early or late", () => {
  const result = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 100_000, annualReturnPct: 0, targetAmount: 500_000 }));
  assertValid(result);
  assert.equal(result.monthsToTarget, 5);
  // one month less would fall short (400,000 < 500,000); confirms no off-by-one.
});

test("target not reachable within 600 months returns unreachable, not an unbounded search", () => {
  const result = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 0, annualReturnPct: -50, targetAmount: 1_000_000 }));
  assertValid(result);
  assert.equal(result.reachable, false);
  assert.equal(result.reachDate, null);
});

test("the 600-month horizon is inclusive", () => {
  const result = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 1, annualReturnPct: 0, targetAmount: 600,
  }));
  assertValid(result);
  assert.equal(result.reachable, true);
  assert.equal(result.monthsToTarget, 600);
});

test("contribution is applied at month-end: first month's growth applies to the starting balance only", () => {
  // starting 1,000,000; 12% annual -> ~0.9489% monthly; after month 1 with
  // zero contribution, balance should be startingValue * (1+monthlyRate),
  // strictly greater than startingValue and unaffected by any contribution.
  const noContribution = computeGoalWhatIf(input({ startingValue: 1_000_000, monthlyContribution: 0, annualReturnPct: 12, targetAmount: 1_000_001 }));
  assertValid(noContribution);
  assert.equal(noContribution.reachable, true);
  assert.equal(noContribution.monthsToTarget, 1);
});

test("a first-month contribution is not itself grown before the month-end boundary", () => {
  const result = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 100, annualReturnPct: 12, targetAmount: 1_000,
    asOfDate: "2026-01-15", targetDate: "2026-02-15",
  }));
  assertValid(result);
  assert.equal(result.projectedValueAtTargetDate, 100);
});

// ─── target-date comparison ──────────────────────────────────────────────────

test("target date in the future: projected value, no shortfall/surplus set when reached exactly", () => {
  const result = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 100_000, annualReturnPct: 0, targetAmount: 1_200_000,
    asOfDate: "2026-01-01", targetDate: "2027-01-01",
  }));
  assertValid(result);
  assert.equal(result.targetDateInPast, false);
  assert.equal(result.projectedValueAtTargetDate, 1_200_000);
  assert.equal(result.shortfallAtTargetDate, null);
  assert.equal(result.surplusAtTargetDate, null);
});

test("target-date closed form has the same economic result as the iterative month-end recurrence", () => {
  const startingValue = 500_000;
  const monthlyContribution = 15_000;
  const annualReturnPct = 6;
  const months = 24;
  const monthlyRate = Math.pow(1 + annualReturnPct / 100, 1 / 12) - 1;
  let iterative = startingValue;
  for (let month = 0; month < months; month++) iterative = iterative * (1 + monthlyRate) + monthlyContribution;

  const result = computeGoalWhatIf(input({
    startingValue, monthlyContribution, annualReturnPct, targetAmount: 2_000_000,
    asOfDate: "2026-01-15", targetDate: "2028-01-15",
  }));
  assertValid(result);
  // The closed form is algebraically identical to the recurrence. IEEE-754
  // operation ordering can differ only by sub-cent floating-point noise.
  assert.ok(Math.abs((result.projectedValueAtTargetDate as number) - iterative) < 0.000001);
});

test("target date before the first same-month projection boundary gets no contribution", () => {
  const result = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 100, annualReturnPct: 0, targetAmount: 1_000,
    asOfDate: "2026-01-15", targetDate: "2026-01-31",
  }));
  assertValid(result);
  assert.equal(result.targetDateInPast, false);
  assert.equal(result.projectedValueAtTargetDate, 0);
});

test("target date earlier in the same calendar month is past, not a zero-month future projection", () => {
  const result = computeGoalWhatIf(input({ asOfDate: "2026-01-15", targetDate: "2026-01-14" }));
  assertValid(result);
  assert.equal(result.targetDateInPast, true);
  assert.equal(result.projectedValueAtTargetDate, null);
});

test("exact one-month anniversary includes exactly one month-end contribution", () => {
  const result = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 100, annualReturnPct: 0, targetAmount: 1_000,
    asOfDate: "2026-01-15", targetDate: "2026-02-15",
  }));
  assertValid(result);
  assert.equal(result.projectedValueAtTargetDate, 100);
});

test("month-end anniversaries clamp Jan 31 to February's final day, including leap years", () => {
  const commonYear = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 100, annualReturnPct: 0, targetAmount: 1_000,
    asOfDate: "2027-01-31", targetDate: "2027-02-27",
  }));
  const commonYearBoundary = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 100, annualReturnPct: 0, targetAmount: 1_000,
    asOfDate: "2027-01-31", targetDate: "2027-02-28",
  }));
  const leapYearBoundary = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 100, annualReturnPct: 0, targetAmount: 1_000,
    asOfDate: "2028-01-31", targetDate: "2028-02-29",
  }));
  assertValid(commonYear);
  assertValid(commonYearBoundary);
  assertValid(leapYearBoundary);
  assert.equal(commonYear.projectedValueAtTargetDate, 0);
  assert.equal(commonYearBoundary.projectedValueAtTargetDate, 100);
  assert.equal(leapYearBoundary.projectedValueAtTargetDate, 100);
});

test("a February clamp does not shift later 30-day/31-day projection boundaries", () => {
  const beforeMarchBoundary = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 100, annualReturnPct: 0, targetAmount: 1_000,
    asOfDate: "2027-01-31", targetDate: "2027-03-30",
  }));
  const marchBoundary = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 100, annualReturnPct: 0, targetAmount: 1_000,
    asOfDate: "2027-01-31", targetDate: "2027-03-31",
  }));
  assertValid(beforeMarchBoundary);
  assertValid(marchBoundary);
  assert.equal(beforeMarchBoundary.projectedValueAtTargetDate, 100);
  assert.equal(marchBoundary.projectedValueAtTargetDate, 200);
});

test("target-date shortfall is reported when the projection falls short", () => {
  const result = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 50_000, annualReturnPct: 0, targetAmount: 1_200_000,
    asOfDate: "2026-01-01", targetDate: "2027-01-01",
  }));
  assertValid(result);
  assert.equal(result.projectedValueAtTargetDate, 600_000);
  assert.equal(result.shortfallAtTargetDate, 600_000);
  assert.equal(result.surplusAtTargetDate, null);
});

test("target-date surplus is reported when the projection exceeds the target", () => {
  const result = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 150_000, annualReturnPct: 0, targetAmount: 1_200_000,
    asOfDate: "2026-01-01", targetDate: "2027-01-01",
  }));
  assertValid(result);
  assert.equal(result.projectedValueAtTargetDate, 1_800_000);
  assert.equal(result.surplusAtTargetDate, 600_000);
  assert.equal(result.shortfallAtTargetDate, null);
});

test("target date in the past does not invalidate the reach-date calculation", () => {
  const result = computeGoalWhatIf(input({
    startingValue: 0, monthlyContribution: 50_000, annualReturnPct: 0, targetAmount: 600_000,
    asOfDate: "2026-08-01", targetDate: "2020-01-01",
  }));
  assertValid(result);
  assert.equal(result.reachable, true);
  assert.equal(result.monthsToTarget, 12);
  assert.equal(result.targetDateInPast, true);
  assert.equal(result.projectedValueAtTargetDate, null);
  assert.equal(result.shortfallAtTargetDate, null);
  assert.equal(result.surplusAtTargetDate, null);
});

test("no target date: target-date fields are all null/false, reach-date still computed", () => {
  const result = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 50_000, annualReturnPct: 0, targetAmount: 600_000, targetDate: null }));
  assertValid(result);
  assert.equal(result.targetDate, null);
  assert.equal(result.targetDateInPast, false);
  assert.equal(result.projectedValueAtTargetDate, null);
  assert.equal(result.reachable, true);
});

// ─── invalid input rejection ─────────────────────────────────────────────────

test("non-finite target amount is rejected", () => {
  assert.equal(computeGoalWhatIf(input({ targetAmount: NaN })).valid, false);
  assert.equal(computeGoalWhatIf(input({ targetAmount: Infinity })).valid, false);
  assert.equal(computeGoalWhatIf(input({ targetAmount: 0 })).valid, false);
  assert.equal(computeGoalWhatIf(input({ targetAmount: -1 })).valid, false);
});

test("non-finite or negative starting value is rejected", () => {
  assert.equal(computeGoalWhatIf(input({ startingValue: NaN })).valid, false);
  assert.equal(computeGoalWhatIf(input({ startingValue: -1 })).valid, false);
});

test("non-finite or negative monthly contribution is rejected", () => {
  assert.equal(computeGoalWhatIf(input({ monthlyContribution: NaN })).valid, false);
  assert.equal(computeGoalWhatIf(input({ monthlyContribution: -100 })).valid, false);
});

test("invalid asOfDate / targetDate strings are rejected", () => {
  assert.equal(computeGoalWhatIf(input({ asOfDate: "not-a-date" })).valid, false);
  assert.equal(computeGoalWhatIf(input({ targetDate: "2026-13-40" })).valid, false);
  assert.equal(computeGoalWhatIf(input({ targetDate: "2026-02-30" })).valid, false);
});

// ─── zero designated funding is a legitimate starting point ────────────────

test("zero designated funding (startingValue = 0) is legitimate, not an error", () => {
  const result = computeGoalWhatIf(input({ startingValue: 0, monthlyContribution: 10_000 }));
  assertValid(result);
  assert.equal(result.startingValue, 0);
});

// ─── precision / repeatability ───────────────────────────────────────────────

test("no intermediate rounding drift: matches the closed-form compounding value exactly", () => {
  const startingValue = 500_000;
  const monthlyContribution = 15_000;
  const annualReturnPct = 6;
  const months = 24;
  const monthlyRate = Math.pow(1 + annualReturnPct / 100, 1 / 12) - 1;
  let expected = startingValue;
  for (let i = 0; i < months; i++) expected = expected * (1 + monthlyRate) + monthlyContribution;

  const result = computeGoalWhatIf(input({
    startingValue, monthlyContribution, annualReturnPct, targetAmount: expected, asOfDate: "2026-01-01",
  }));
  assertValid(result);
  assert.equal(result.monthsToTarget, months);
});

test("deterministic repeatability: identical input produces identical output", () => {
  const same = input({ startingValue: 250_000, monthlyContribution: 12_500, annualReturnPct: 4.5, targetAmount: 900_000, targetDate: "2029-06-01" });
  const first = computeGoalWhatIf(same);
  const second = computeGoalWhatIf(same);
  assert.deepEqual(first, second);
});

// ─── formatMonthLabel ─────────────────────────────────────────────────────────

test("formatMonthLabel renders a human month/year label", () => {
  assert.equal(formatMonthLabel("2028-03"), "March 2028");
  assert.equal(formatMonthLabel("2026-01"), "January 2026");
  assert.equal(formatMonthLabel("2026-12"), "December 2026");
});

// ─── required monthly contribution inverse ──────────────────────────────────

test("required contribution at 0% return uses the simple linear inverse", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ targetAmount: 1_200_000 }));
  assertInverseValid(result);
  assert.equal(result.monthsAvailable, 12);
  assert.equal(result.requiredMonthlyContribution, 100_000);
  assert.equal(result.projectedValueAtTargetDate, 1_200_000);
});

test("positive return lowers the required contribution and still reaches the target", () => {
  const zeroReturn = computeRequiredMonthlyContribution(inverseInput({ targetAmount: 1_200_000, annualReturnPct: 0 }));
  const positiveReturn = computeRequiredMonthlyContribution(inverseInput({ targetAmount: 1_200_000, annualReturnPct: 8 }));
  assertInverseValid(zeroReturn);
  assertInverseValid(positiveReturn);
  assert.ok(positiveReturn.requiredMonthlyContribution > 0);
  assert.ok(positiveReturn.requiredMonthlyContribution < zeroReturn.requiredMonthlyContribution);
  assert.ok(positiveReturn.projectedValueAtTargetDate >= positiveReturn.targetAmount);
});

test("negative return is allowed and requires more contribution", () => {
  const zeroReturn = computeRequiredMonthlyContribution(inverseInput({ targetAmount: 1_200_000, annualReturnPct: 0 }));
  const negativeReturn = computeRequiredMonthlyContribution(inverseInput({ targetAmount: 1_200_000, annualReturnPct: -5 }));
  assertInverseValid(zeroReturn);
  assertInverseValid(negativeReturn);
  assert.ok(negativeReturn.requiredMonthlyContribution > zeroReturn.requiredMonthlyContribution);
  assert.ok(negativeReturn.projectedValueAtTargetDate >= negativeReturn.targetAmount);
});

test("already funded goals require zero additional monthly contribution", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ startingValue: 1_200_000, targetAmount: 1_000_000 }));
  assertInverseValid(result);
  assert.equal(result.alreadyReached, true);
  assert.equal(result.requiredMonthlyContribution, 0);
});

test("an exact N-month target produces a forward-verifiable contribution", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ targetAmount: 600_000 }));
  assertInverseValid(result);
  assert.equal(result.monthsAvailable, 12);
  assert.equal(result.requiredMonthlyContribution, 50_000);
  assert.ok(result.projectedValueAtTargetDate >= result.targetAmount);
});

test("required contribution rounds up to satang and avoids underfunding", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ targetAmount: 1_000 }));
  assertInverseValid(result);
  assert.equal(result.requiredMonthlyContribution, 83.34);
  assert.ok(result.projectedValueAtTargetDate >= 1_000);
  const roundedDown = computeGoalWhatIf({
    targetAmount: 1_000,
    startingValue: 0,
    monthlyContribution: 83.33,
    annualReturnPct: 0,
    asOfDate: "2026-01-15",
    targetDate: "2027-01-15",
  });
  assertValid(roundedDown);
  assert.equal(roundedDown.projectedValueAtTargetDate, 999.96);
});

test("inverse result is the forward-minimal satang across returns, horizons, and month-end boundaries", () => {
  for (const scenario of [
    inverseInput({ targetAmount: 1_000 }),
    inverseInput({ targetAmount: 1_200_000, annualReturnPct: 8 }),
    inverseInput({ targetAmount: 1_200_000, annualReturnPct: -5 }),
    inverseInput({ targetAmount: 100, annualReturnPct: 8, targetDate: "2026-02-15" }),
    inverseInput({ targetAmount: 2_000_000, startingValue: 500_000, annualReturnPct: 4.5, targetDate: "2076-01-15" }),
    inverseInput({ targetAmount: 100, annualReturnPct: -5, asOfDate: "2027-01-31", targetDate: "2027-02-28" }),
  ]) {
    assertInverseIsForwardMinimal(scenario);
  }
});

test("very small nonzero annual returns retain stable inverse math", () => {
  const result = assertInverseIsForwardMinimal(inverseInput({
    startingValue: 1_000_000_000_000,
    targetAmount: 1_000_000_000_600.04,
    annualReturnPct: 1e-13,
    targetDate: "2076-01-15",
  }));
  assert.equal(result.requiredMonthlyContribution, 1);
});

test("same-month underfunded target has zero available periods and is unavailable", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ targetDate: "2026-01-31" }));
  assert.equal(result.valid, false);
  assert.match(result.error, /No completed monthly contribution periods/);
});

test("same-month target on the as-of date remains zero-period and honest", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ targetDate: "2026-01-15" }));
  assert.equal(result.valid, false);
  assert.match(result.error, /No completed monthly contribution periods/);
});

test("exactly one completed month includes one month-end contribution period", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ targetAmount: 100, targetDate: "2026-02-15" }));
  assertInverseValid(result);
  assert.equal(result.monthsAvailable, 1);
  assert.equal(result.requiredMonthlyContribution, 100);
});

test("Jan 31 clamps to Feb 28 and later 31-day boundaries remain anchored", () => {
  const febBoundary = computeRequiredMonthlyContribution(inverseInput({
    targetAmount: 100, asOfDate: "2027-01-31", targetDate: "2027-02-28",
  }));
  const beforeMarchBoundary = computeRequiredMonthlyContribution(inverseInput({
    targetAmount: 200, asOfDate: "2027-01-31", targetDate: "2027-03-30",
  }));
  const marchBoundary = computeRequiredMonthlyContribution(inverseInput({
    targetAmount: 200, asOfDate: "2027-01-31", targetDate: "2027-03-31",
  }));
  assertInverseValid(febBoundary);
  assert.equal(febBoundary.monthsAvailable, 1);
  assert.equal(febBoundary.requiredMonthlyContribution, 100);
  assertInverseValid(beforeMarchBoundary);
  assert.equal(beforeMarchBoundary.monthsAvailable, 1);
  assert.equal(beforeMarchBoundary.requiredMonthlyContribution, 200);
  assertInverseValid(marchBoundary);
  assert.equal(marchBoundary.monthsAvailable, 2);
  assert.equal(marchBoundary.requiredMonthlyContribution, 100);
});

test("leap-year Jan 31 clamps to Feb 29", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({
    targetAmount: 100, asOfDate: "2028-01-31", targetDate: "2028-02-29",
  }));
  assertInverseValid(result);
  assert.equal(result.monthsAvailable, 1);
  assert.equal(result.requiredMonthlyContribution, 100);
});

test("past target date is unavailable", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ targetDate: "2020-01-15" }));
  assert.equal(result.valid, false);
  assert.equal(result.error, "The saved target date has passed.");
});

test("missing target date is unavailable", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ targetDate: null }));
  assert.equal(result.valid, false);
  assert.equal(result.error, "A saved target date is required for this calculation.");
});

test("annual return at or below -100% is rejected", () => {
  assert.equal(computeRequiredMonthlyContribution(inverseInput({ annualReturnPct: -100 })).valid, false);
  assert.equal(computeRequiredMonthlyContribution(inverseInput({ annualReturnPct: -150 })).valid, false);
});

test("non-finite inverse inputs are rejected honestly", () => {
  assert.equal(computeRequiredMonthlyContribution(inverseInput({ targetAmount: NaN })).valid, false);
  assert.equal(computeRequiredMonthlyContribution(inverseInput({ startingValue: Infinity })).valid, false);
  assert.equal(computeRequiredMonthlyContribution(inverseInput({ annualReturnPct: NaN })).valid, false);
  assert.equal(computeRequiredMonthlyContribution(inverseInput({ asOfDate: "2026-02-30" })).valid, false);
});

test("zero starting value is legitimate for the inverse", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({ startingValue: 0, targetAmount: 1_200 }));
  assertInverseValid(result);
  assert.equal(result.startingValue, 0);
  assert.equal(result.requiredMonthlyContribution, 100);
});

test("the 600-month boundary is supported", () => {
  const result = computeRequiredMonthlyContribution(inverseInput({
    targetAmount: 600, asOfDate: "2026-01-15", targetDate: "2076-01-15",
  }));
  assertInverseValid(result);
  assert.equal(result.monthsAvailable, 600);
  assert.equal(result.requiredMonthlyContribution, 1);
});

test("inverse output is deterministic for identical inputs", () => {
  const same = inverseInput({ targetAmount: 900_000, annualReturnPct: 4.5, targetDate: "2029-06-15" });
  assert.deepEqual(computeRequiredMonthlyContribution(same), computeRequiredMonthlyContribution(same));
});
