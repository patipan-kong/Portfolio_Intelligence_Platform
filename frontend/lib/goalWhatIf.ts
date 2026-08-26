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
function valueAfterMonths(startingValue: number, monthlyContribution: number, monthlyRate: number, months: number): number {
  if (months <= 0) return startingValue;
  if (monthlyRate === 0) return startingValue + monthlyContribution * months;
  const growth = Math.pow(1 + monthlyRate, months);
  return startingValue * growth + monthlyContribution * ((growth - 1) / monthlyRate);
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

  const monthlyRate = Math.pow(1 + annualReturnPct / 100, 1 / 12) - 1;
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
