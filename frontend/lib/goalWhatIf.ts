// Goal What-If — a transient, deterministic projection under explicit user
// assumptions. Not a forecast, not a probability of success, not advice.
//
// The user supplies a monthly contribution and an annual return assumption;
// this module answers, deterministically, "when would designated funding
// reach the target under these assumptions?" and, if the goal has a saved
// target date, "what would designated funding be by that date?"
//
// Starting value is ALWAYS the caller-supplied designated funding
// (see goalFunding.ts's computeGoalFunding().designatedFunding) — never a
// source's current capacity. Funding Health (a source's current-value
// comparison) is a separate fact this module does not read or alter.
//
// Nothing here is persisted, fetched, or mutated: pure functions only.

const HORIZON_MONTHS = 600; // 50 years
/** Every supported contribution is represented as an exact integer number of satang. */
const MAX_SAFE_SATANG = Number.MAX_SAFE_INTEGER;

const DATE_PATTERN = /^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;

const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

export interface GoalWhatIfInput {
  targetAmount: number;
  /** computeGoalFunding(...).designatedFunding — never a source's current capacity. */
  startingValue: number;
  monthlyContribution: number;
  annualReturnPct: number;
  /** "YYYY-MM-DD" */
  asOfDate: string;
  /** WealthGoal.target_date verbatim — null/undefined when the goal has none. */
  targetDate?: string | null;
}

export interface GoalWhatIfAssumptions {
  monthlyContribution: number;
  annualReturnPct: number;
  asOfDate: string;
}

export interface GoalWhatIfValid {
  valid: true;
  assumptions: GoalWhatIfAssumptions;
  targetAmount: number;
  startingValue: number;
  alreadyReached: boolean;
  reachable: boolean;
  /** null unless reachable. */
  monthsToTarget: number | null;
  /** "YYYY-MM"; null unless reachable. */
  reachDate: string | null;
  /** Echoed input target date, or null when the goal has none. */
  targetDate: string | null;
  /** True when a target date exists but is before asOfDate — the reach-date result above is still valid. */
  targetDateInPast: boolean;
  /** null when there is no (usable) target date. */
  projectedValueAtTargetDate: number | null;
  /** Set only when the target-date projection falls short of the target. */
  shortfallAtTargetDate: number | null;
  /** Set only when the target-date projection exceeds the target. */
  surplusAtTargetDate: number | null;
}

export interface GoalWhatIfInvalid {
  valid: false;
  error: string;
}

export type GoalWhatIfResult = GoalWhatIfValid | GoalWhatIfInvalid;

export interface RequiredMonthlyContributionInput {
  targetAmount: number;
  /** computeGoalFunding(...).designatedFunding — never a source's current capacity. */
  startingValue: number;
  annualReturnPct: number;
  /** "YYYY-MM-DD" */
  asOfDate: string;
  /** WealthGoal.target_date — required for this inverse calculation. */
  targetDate?: string | null;
}

export interface RequiredMonthlyContributionAssumptions {
  annualReturnPct: number;
  asOfDate: string;
  targetDate: string;
}

export interface RequiredMonthlyContributionValid {
  valid: true;
  assumptions: RequiredMonthlyContributionAssumptions;
  targetAmount: number;
  startingValue: number;
  alreadyReached: boolean;
  monthsAvailable: number;
  /** Rounded up to the smallest supported THB precision (satang). */
  requiredMonthlyContribution: number;
  /** Forward projection using the rounded-up contribution. */
  projectedValueAtTargetDate: number;
}

export interface RequiredMonthlyContributionInvalid {
  valid: false;
  error: string;
}

export type RequiredMonthlyContributionResult =
  | RequiredMonthlyContributionValid
  | RequiredMonthlyContributionInvalid;

interface CalendarDate {
  year: number;
  month: number;
  day: number;
}

function daysInMonth(year: number, month: number): number {
  if (month === 2) {
    return year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0) ? 29 : 28;
  }
  return [4, 6, 9, 11].includes(month) ? 30 : 31;
}

function parseDate(value: string): CalendarDate | null {
  const match = DATE_PATTERN.exec(value);
  if (!match) return null;
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  return day <= daysInMonth(year, month) ? { year, month, day } : null;
}

function formatDate({ year, month, day }: CalendarDate): string {
  return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}

/**
 * The nth projection occurs on the calendar-month anniversary of asOfDate.
 * If that day does not exist in a month, it occurs on that month's final day
 * (for example, Jan 31 -> Feb 28/29). This is a scheduling rule only; the
 * economic recurrence remains one growth step followed by one contribution.
 */
function projectionDateAfterMonths(fromDate: CalendarDate, months: number): CalendarDate {
  const total = fromDate.year * 12 + (fromDate.month - 1) + months;
  const resultYear = Math.floor(total / 12);
  const resultMonth = (total % 12) + 1;
  return {
    year: resultYear,
    month: resultMonth,
    day: Math.min(fromDate.day, daysInMonth(resultYear, resultMonth)),
  };
}

function projectionMonthAfterMonths(fromDate: CalendarDate, months: number): string {
  const date = projectionDateAfterMonths(fromDate, months);
  return `${date.year}-${String(date.month).padStart(2, "0")}`;
}

/**
 * Number of completed monthly projection boundaries at targetDate. A target
 * date on a boundary includes that month's growth and month-end contribution;
 * a date before it does not. The result is never negative for a non-past date.
 */
function completedProjectionMonths(asOfDate: CalendarDate, targetDate: CalendarDate): number {
  let months = (targetDate.year - asOfDate.year) * 12 + (targetDate.month - asOfDate.month);
  if (formatDate(projectionDateAfterMonths(asOfDate, months)) > formatDate(targetDate)) months--;
  return Math.max(months, 0);
}

/** "2028-03" -> "March 2028". Pure formatting for reachDate / target-month display. */
export function formatMonthLabel(monthStr: string): string {
  const [year, month] = monthStr.split("-").map(Number);
  return `${MONTH_NAMES[month - 1]} ${year}`;
}

/**
 * Closed-form value after `months` of monthly compounding with an end-of-month
 * contribution — mathematically identical to repeatedly applying
 * `balance = balance * (1 + monthlyRate) + monthlyContribution`, without
 * accumulating iterative floating-point drift over a long horizon.
 */
function monthlyRateFromAnnualReturn(annualReturnPct: number): number {
  // log1p/expm1 retain very small nonzero return assumptions that the
  // equivalent pow(...)-1 expression can round down to zero.
  return Math.expm1(Math.log1p(annualReturnPct / 100) / 12);
}

function growthAndAnnuityFactor(monthlyRate: number, months: number): { growth: number; annuityFactor: number } {
  if (months <= 0) return { growth: 1, annuityFactor: 0 };
  if (monthlyRate === 0) return { growth: 1, annuityFactor: months };
  const logGrowth = months * Math.log1p(monthlyRate);
  return {
    growth: Math.exp(logGrowth),
    annuityFactor: Math.expm1(logGrowth) / monthlyRate,
  };
}

function valueAfterMonths(startingValue: number, monthlyContribution: number, monthlyRate: number, months: number): number {
  if (months <= 0) return startingValue;
  const { growth, annuityFactor } = growthAndAnnuityFactor(monthlyRate, months);
  return startingValue * growth + monthlyContribution * annuityFactor;
}

function ceilToSafeSatang(value: number): number | null {
  const satang = Math.ceil(value * 100);
  return Number.isSafeInteger(satang) && satang >= 0 ? satang : null;
}

interface ReachSearch {
  alreadyReached: boolean;
  reachable: boolean;
  monthsToTarget: number | null;
  reachDate: string | null;
}

/**
 * Bounded month-by-month search (never unbounded) for the first month at
 * which balance >= targetAmount, applying growth then the contribution each
 * month (contribution occurs at month-end, matching the frozen math contract).
 */
function findReachDate(startingValue: number, monthlyContribution: number, monthlyRate: number, targetAmount: number, asOfDate: CalendarDate): ReachSearch {
  if (startingValue >= targetAmount) {
    return { alreadyReached: true, reachable: true, monthsToTarget: 0, reachDate: projectionMonthAfterMonths(asOfDate, 0) };
  }
  let balance = startingValue;
  for (let month = 1; month <= HORIZON_MONTHS; month++) {
    balance = balance * (1 + monthlyRate) + monthlyContribution;
    if (balance >= targetAmount) {
      return { alreadyReached: false, reachable: true, monthsToTarget: month, reachDate: projectionMonthAfterMonths(asOfDate, month) };
    }
  }
  return { alreadyReached: false, reachable: false, monthsToTarget: null, reachDate: null };
}

/**
 * Compute a deterministic What-If projection. Invalid/non-finite inputs are
 * rejected honestly (`valid: false`) rather than silently coerced — this
 * mirrors goalFunding.ts's "fail honestly, never fabricate" convention.
 */
export function computeGoalWhatIf(input: GoalWhatIfInput): GoalWhatIfResult {
  const { targetAmount, startingValue, monthlyContribution, annualReturnPct, asOfDate, targetDate } = input;

  if (!Number.isFinite(targetAmount) || targetAmount <= 0) {
    return { valid: false, error: "Target amount must be a positive number." };
  }
  if (!Number.isFinite(startingValue) || startingValue < 0) {
    return { valid: false, error: "Starting value must be zero or a positive number." };
  }
  if (!Number.isFinite(monthlyContribution) || monthlyContribution < 0) {
    return { valid: false, error: "Monthly contribution must be zero or a positive number." };
  }
  if (!Number.isFinite(annualReturnPct) || annualReturnPct <= -100) {
    return { valid: false, error: "Annual return assumption must be greater than -100%." };
  }
  const parsedAsOfDate = parseDate(asOfDate);
  if (parsedAsOfDate === null) {
    return { valid: false, error: "As-of date is invalid." };
  }
  const parsedTargetDate = targetDate == null ? null : parseDate(targetDate);
  if (targetDate != null && parsedTargetDate === null) {
    return { valid: false, error: "Target date is invalid." };
  }

  const monthlyRate = monthlyRateFromAnnualReturn(annualReturnPct);
  const search = findReachDate(startingValue, monthlyContribution, monthlyRate, targetAmount, parsedAsOfDate);

  let targetDateInPast = false;
  let projectedValueAtTargetDate: number | null = null;
  let shortfallAtTargetDate: number | null = null;
  let surplusAtTargetDate: number | null = null;

  if (targetDate != null && parsedTargetDate !== null) {
    if (targetDate < asOfDate) {
      targetDateInPast = true;
    } else {
      const monthsAhead = completedProjectionMonths(parsedAsOfDate, parsedTargetDate);
      const value = valueAfterMonths(startingValue, monthlyContribution, monthlyRate, monthsAhead);
      projectedValueAtTargetDate = value;
      if (value < targetAmount) shortfallAtTargetDate = targetAmount - value;
      else if (value > targetAmount) surplusAtTargetDate = value - targetAmount;
    }
  }

  return {
    valid: true,
    assumptions: { monthlyContribution, annualReturnPct, asOfDate },
    targetAmount,
    startingValue,
    alreadyReached: search.alreadyReached,
    reachable: search.reachable,
    monthsToTarget: search.monthsToTarget,
    reachDate: search.reachDate,
    targetDate: targetDate ?? null,
    targetDateInPast,
    projectedValueAtTargetDate,
    shortfallAtTargetDate,
    surplusAtTargetDate,
  };
}

/**
 * Solve the inverse month-end contribution question for a saved target date.
 * This deliberately shares date and forward-projection helpers with the
 * forward What-If path, and returns the rounded-up contribution's projection
 * so the displayed amount is independently verified to reach the target.
 */
export function computeRequiredMonthlyContribution(
  input: RequiredMonthlyContributionInput,
): RequiredMonthlyContributionResult {
  const { targetAmount, startingValue, annualReturnPct, asOfDate, targetDate } = input;

  if (!Number.isFinite(targetAmount) || targetAmount <= 0) {
    return { valid: false, error: "Target amount must be a positive number." };
  }
  if (!Number.isFinite(startingValue) || startingValue < 0) {
    return { valid: false, error: "Starting value must be zero or a positive number." };
  }
  if (!Number.isFinite(annualReturnPct) || annualReturnPct <= -100) {
    return { valid: false, error: "Annual return assumption must be greater than -100%." };
  }

  const parsedAsOfDate = parseDate(asOfDate);
  if (parsedAsOfDate === null) {
    return { valid: false, error: "As-of date is invalid." };
  }
  if (targetDate == null) {
    return { valid: false, error: "A saved target date is required for this calculation." };
  }
  const parsedTargetDate = parseDate(targetDate);
  if (parsedTargetDate === null) {
    return { valid: false, error: "Target date is invalid." };
  }
  if (targetDate < asOfDate) {
    return { valid: false, error: "The saved target date has passed." };
  }

  const monthsAvailable = completedProjectionMonths(parsedAsOfDate, parsedTargetDate);
  const monthlyRate = monthlyRateFromAnnualReturn(annualReturnPct);
  if (!Number.isFinite(monthlyRate)) {
    return { valid: false, error: "Annual return assumption cannot produce a finite monthly rate." };
  }
  const verifyForward = (monthlyContribution: number): GoalWhatIfResult => computeGoalWhatIf({
    targetAmount,
    startingValue,
    monthlyContribution,
    annualReturnPct,
    asOfDate,
    targetDate,
  });

  if (startingValue >= targetAmount) {
    const forward = verifyForward(0);
    if (!forward.valid || forward.projectedValueAtTargetDate === null || !Number.isFinite(forward.projectedValueAtTargetDate)) {
      return { valid: false, error: "Required contribution could not be verified to reach the target." };
    }
    return {
      valid: true,
      assumptions: { annualReturnPct, asOfDate, targetDate },
      targetAmount,
      startingValue,
      alreadyReached: true,
      monthsAvailable,
      requiredMonthlyContribution: 0,
      projectedValueAtTargetDate: forward.projectedValueAtTargetDate,
    };
  }
  if (monthsAvailable <= 0) {
    return { valid: false, error: "No completed monthly contribution periods are available before the saved target date." };
  }

  const { growth, annuityFactor } = growthAndAnnuityFactor(monthlyRate, monthsAvailable);
  const numerator = targetAmount - startingValue * growth;
  const rawContribution = numerator / annuityFactor;
  if (!Number.isFinite(growth) || !Number.isFinite(annuityFactor) || !Number.isFinite(rawContribution)) {
    return { valid: false, error: "Required contribution could not be calculated finitely." };
  }

  const initialSatang = ceilToSafeSatang(Math.max(rawContribution, 0));
  if (initialSatang === null) {
    return { valid: false, error: "Required contribution could not be calculated finitely." };
  }
  let upperSatang: number = initialSatang;

  const forwardValueAtSatang = (satang: number): number | null => {
    const forward = verifyForward(satang / 100);
    return forward.valid && forward.projectedValueAtTargetDate !== null && Number.isFinite(forward.projectedValueAtTargetDate)
      ? forward.projectedValueAtTargetDate
      : null;
  };
  const reachesTarget = (satang: number): boolean => {
    const projectedValue = forwardValueAtSatang(satang);
    return projectedValue !== null && projectedValue >= targetAmount;
  };

  // The closed form gives an efficient upper bound. Verify it through the
  // forward engine, then expand only if floating-point operation ordering
  // leaves it short. The binary search establishes the smallest safe integer
  // satang that satisfies the forward engine's own semantics.
  if (!reachesTarget(upperSatang)) {
    upperSatang = Math.max(upperSatang, 1);
    while (!reachesTarget(upperSatang)) {
      if (upperSatang === MAX_SAFE_SATANG) {
        return { valid: false, error: "Required contribution could not be verified to reach the target." };
      }
      upperSatang = Math.min(upperSatang * 2, MAX_SAFE_SATANG);
    }
  }

  let lowerSatang = 0;
  while (lowerSatang < upperSatang) {
    const middleSatang = lowerSatang + Math.floor((upperSatang - lowerSatang) / 2);
    if (reachesTarget(middleSatang)) upperSatang = middleSatang;
    else lowerSatang = middleSatang + 1;
  }

  const projectedValueAtTargetDate = forwardValueAtSatang(upperSatang);
  if (projectedValueAtTargetDate === null || projectedValueAtTargetDate < targetAmount) {
    return { valid: false, error: "Required contribution could not be verified to reach the target." };
  }

  return {
    valid: true,
    assumptions: { annualReturnPct, asOfDate, targetDate },
    targetAmount,
    startingValue,
    alreadyReached: false,
    monthsAvailable,
    requiredMonthlyContribution: upperSatang / 100,
    projectedValueAtTargetDate,
  };
}
