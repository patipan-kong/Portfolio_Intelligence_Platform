// Goal Affordability Bridge — a read-only, derived comparison between a
// single Goal's required monthly contribution and recorded Personal Cash
// Flow. This composes two already-existing pure engines and adds no new
// math of its own:
//   - computeRequiredMonthlyContribution (goalWhatIf.ts) for the required side
//   - aggregateMonthlyCashFlow (cashFlow.ts) for the observed side
// Nothing here is fetched, persisted, or mutated — pure functions only. It
// grants no new Goal behavioral authority: the result is presentational
// only and must never be wired into optimizer, recommendation, or execution
// inputs.
//
// Three distinctions are load-bearing and must not be collapsed:
//   1. ONE calendar anchor. goalAffordabilityCalendar() is the only clock
//      reader in this feature. The months it names are the months the caller
//      fetches AND the months this helper evaluates, and the as-of date used
//      for the required side comes from the same instant on the same (local)
//      calendar. No consumer may derive months from a second clock.
//   2. A technical retrieval failure is NOT evidence sparsity. A month that
//      failed to load fails the whole assessment closed; it never shrinks the
//      sample into a smaller-but-confident AFFORDABLE/SHORTFALL claim.
//   3. Absence of a recording population is NOT a measured zero — neither for
//      a whole workspace that tracks no cash accounts, nor for a single month
//      that predates when tracking began. A successful month only enters the
//      sample as a measured zero once a recording population is proven for
//      it: either real historical Cash Flow activity in that month, or the
//      month falling on/after the earliest active Cash Account baseline. A
//      month before tracking began with no historical activity is omitted
//      exactly like a month with no fetch entry at all — never fabricated as
//      ฿0.

import type { CashAccount } from "./api.ts";
import { aggregateMonthlyCashFlow, currentMonthKey, shiftMonth, type CashFlowSummary } from "./cashFlow.ts";
import { computeRequiredMonthlyContribution } from "./goalWhatIf.ts";
import type { CashAccountsFetchStatus, MonthlyFetchResult } from "./emergencyFund.ts";

export type GoalAffordabilityState =
  | "NO_CONTRIBUTION_REQUIRED"
  | "INSUFFICIENT_DATA"
  | "AFFORDABLE"
  | "SHORTFALL";

/**
 * Why an INSUFFICIENT_DATA result was reached. The public state model stays
 * at four states; this is an internal diagnosis so a technical failure is
 * never reported to the reader as an absence of historical activity.
 */
export type GoalAffordabilityReasonCode =
  | "REQUIRED_SIDE_INVALID"
  | "CASH_FLOW_UNAVAILABLE"
  | "CASH_ACCOUNTS_UNAVAILABLE"
  | "NO_RECORDED_MONTH"
  | "NO_TRACKED_CASH_FLOW";

const CASH_FLOW_UNAVAILABLE_REASON = "Cash Flow data could not be fully loaded. Try again.";
const CASH_ACCOUNTS_UNAVAILABLE_REASON = "Cash account data could not be fully loaded. Try again.";
const NO_RECORDED_MONTH_REASON = "No completed month of recorded cash flow is available yet.";
const NO_TRACKED_CASH_FLOW_REASON = "Not enough recorded cash flow to assess affordability yet.";

export interface GoalAffordabilityCalendar {
  /** "YYYY-MM-DD" on the viewer's local calendar. */
  asOfDate: string;
  /** The 3 completed calendar months immediately before asOfDate's month, oldest first. */
  trailingCompletedMonths: string[];
}

/**
 * The single calendar anchor for the whole feature, derived from one instant
 * on one calendar. `currentMonthKey` (cashFlow.ts) is the repository's local
 * month convention and is also what Recorded Expense Coverage anchors on, so
 * a month is "completed" exactly when it is completed on the calendar the
 * user's own transaction dates are written in.
 *
 * Deliberately NOT derived through toISOString(): at 2026-09-01T00:30+07:00
 * the UTC date is still 2026-08-31, which would evaluate June/July/August as
 * May/June/July and silently corrupt the window for the first 7 hours of
 * every month in Thailand.
 */
export function goalAffordabilityCalendar(now: Date): GoalAffordabilityCalendar {
  const anchorMonth = currentMonthKey(now);
  return {
    asOfDate: `${anchorMonth}-${String(now.getDate()).padStart(2, "0")}`,
    trailingCompletedMonths: [shiftMonth(anchorMonth, -3), shiftMonth(anchorMonth, -2), shiftMonth(anchorMonth, -1)],
  };
}

export interface GoalAffordabilityInput {
  targetAmount: number;
  /** Server-supplied Goal Context designated total — never a source's current capacity. */
  startingValue: number;
  /** "YYYY-MM-DD", from goalAffordabilityCalendar — the same instant that named the months below. */
  asOfDate: string;
  /** WealthGoal.target_date. */
  targetDate?: string | null;
  /**
   * The completed months to evaluate, from goalAffordabilityCalendar. This
   * helper never recomputes them: the caller's fetched months and the
   * evaluated months are the same list by construction.
   */
  trailingCompletedMonths: string[];
  /**
   * Fetch outcomes for those months. Each entry means exactly one thing:
   *   status "success" — the month loaded; its events are the whole month.
   *   status "error"   — the month failed to load technically. The entire
   *                      assessment fails closed; it is never a zero month
   *                      and never silently narrows the sample.
   * A window month with NO entry is genuinely-unrecorded history: excluded
   * from the denominator, never fabricated as zero. A "success" month that
   * predates the earliest active Cash Account baseline and holds no
   * historical activity is excluded the same way (see isEligibleEvidenceMonth
   * below) — pre-tracking history is not a recorded zero either. Entries
   * outside trailingCompletedMonths are ignored (a month -4 report can never
   * be pulled in to fill the sample back up to three).
   */
  monthlyCashFlowResults: MonthlyFetchResult[];
  /** Whether the cash-account list itself loaded. "error" fails closed. */
  cashAccountsStatus: CashAccountsFetchStatus;
  /** The workspace's cash accounts, used only as a presence gate — no balance is read. */
  cashAccounts: CashAccount[];
}

export interface GoalAffordabilityResult {
  state: GoalAffordabilityState;
  /** Rounded up to the nearest satang. Null only when the required side is invalid. */
  requiredMonthlyContribution: number | null;
  /** Mean of the available completed months' netCashFlow. Null when no evidence contributed. */
  observedMonthlySurplus: number | null;
  /** observedMonthlySurplus - requiredMonthlyContribution. Null unless both sides are defined. */
  affordabilityGap: number | null;
  /**
   * 0-3. Count of trailing months that both loaded successfully and passed
   * the pre-tracking presence gate (isEligibleEvidenceMonth). Only meaningful
   * as an evidence claim when state is AFFORDABLE or SHORTFALL — on a
   * fail-closed result it is a diagnosis, not a sample size.
   */
  evidenceMonthCount: number;
  /** The subset of the trailing window that had a successful fetch AND passed the pre-tracking presence gate, oldest first. */
  evidenceMonths: string[];
  /** Set only for INSUFFICIENT_DATA. */
  reason: string | null;
  /** Set only for INSUFFICIENT_DATA. */
  reasonCode: GoalAffordabilityReasonCode | null;
}

function roundCurrency(value: number): number {
  return Number(value.toFixed(2));
}

/**
 * Earliest baseline date among active tracked Cash Accounts, or null if none
 * are tracked. Reuses Recorded Expense Coverage's population marker exactly
 * (`!is_archived && baseline != null`, emergencyFund.ts computeCoveragePopulation)
 * — the same accounts, the same field — so the two features never disagree
 * about which accounts are "tracked".
 */
function earliestActiveBaselineDate(cashAccounts: CashAccount[]): string | null {
  const trackedActiveAccounts = cashAccounts.filter(
    (account) => !account.is_archived && account.baseline != null,
  );
  if (trackedActiveAccounts.length === 0) return null;
  return trackedActiveAccounts
    .map((account) => account.baseline!.effective_on)
    .reduce((earliest, effectiveOn) => (effectiveOn < earliest ? effectiveOn : earliest));
}

/**
 * Presence gate for a single successfully-retrieved month, deciding whether
 * it may enter the affordability sample. This reuses Recorded Expense
 * Coverage's fail-closed gating PATTERN only — never its numeric coverage
 * result, whose semantics remain separate. Two independent factual proofs
 * are accepted, and nothing is inferred from either:
 *
 *   - the month itself actually contains ledger activity, which proves a
 *     recording population exists for it even when the caller's active
 *     account list cannot show it — the Goal page lists active accounts
 *     only, while /cash-flow keeps archived-account history; or
 *   - the month falls on/after the earliest active Cash Account baseline,
 *     using the same whole-month boundary Recorded Expense Coverage uses
 *     (`${month}-01 >= earliestBaseline`): a baseline effective mid-month
 *     starts counting the FOLLOWING month, not a partial one.
 *
 * With neither, a successful empty month predates tracking and is an absence
 * of evidence, not a measured ฿0 — it is omitted exactly like a month with no
 * fetch entry at all. With either, the month is a legitimate zero-flow month
 * under canonical Cash Flow semantics if it holds no economic events —
 * including a month whose only rows are ADJUSTMENT or TRANSFER, which are
 * correctly non-economic rather than absent. Unrecorded real-world spending
 * is never inferred in either case.
 */
function isEligibleEvidenceMonth(
  month: string,
  summary: CashFlowSummary | undefined,
  earliestActiveBaseline: string | null,
): boolean {
  if (!summary) return false;
  if (summary.eventCount > 0) return true;
  return earliestActiveBaseline !== null && `${month}-01` >= earliestActiveBaseline;
}

/**
 * Bridges a Goal's required monthly contribution (goalWhatIf.ts) against
 * observed Personal Cash Flow (cashFlow.ts) for exactly one Goal. Always
 * uses a 0% return assumption for the required side, independent of any
 * saved Goal Scenario, so the result never depends on transient
 * scenario-selection state.
 */
export function computeGoalAffordability(input: GoalAffordabilityInput): GoalAffordabilityResult {
  const {
    targetAmount,
    startingValue,
    asOfDate,
    targetDate,
    trailingCompletedMonths,
    monthlyCashFlowResults,
    cashAccountsStatus,
    cashAccounts,
  } = input;

  const resultByMonth = new Map(monthlyCashFlowResults.map((result) => [result.month, result]));
  const windowResults = trailingCompletedMonths.map((month) => resultByMonth.get(month));
  const anyRetrievalFailed = windowResults.some((result) => result?.status === "error");

  // Successfully retrieved months, before the pre-tracking presence gate —
  // used only to tell "nothing loaded at all" (NO_RECORDED_MONTH) apart from
  // "loaded, but none of it is eligible evidence" (NO_TRACKED_CASH_FLOW).
  const successMonths = trailingCompletedMonths.filter((month) => resultByMonth.get(month)?.status === "success");
  const summaryByMonth = new Map(
    successMonths.map((month) => [month, aggregateMonthlyCashFlow(resultByMonth.get(month)!.events, month)] as const),
  );
  const earliestActiveBaseline = earliestActiveBaselineDate(cashAccounts);
  const evidenceMonths = successMonths.filter((month) =>
    isEligibleEvidenceMonth(month, summaryByMonth.get(month), earliestActiveBaseline),
  );

  const insufficient = (reasonCode: GoalAffordabilityReasonCode, reason: string): GoalAffordabilityResult => ({
    state: "INSUFFICIENT_DATA",
    requiredMonthlyContribution: null,
    observedMonthlySurplus: null,
    affordabilityGap: null,
    evidenceMonthCount: evidenceMonths.length,
    evidenceMonths,
    reason,
    reasonCode,
  });

  const required = computeRequiredMonthlyContribution({
    targetAmount,
    startingValue,
    annualReturnPct: 0,
    asOfDate,
    targetDate,
  });

  if (!required.valid) {
    return insufficient("REQUIRED_SIDE_INVALID", required.error);
  }

  // Already-reached keeps precedence over every evidence question: no monthly
  // contribution is required whatever the Cash Flow side did or failed to do.
  if (required.alreadyReached) {
    return {
      state: "NO_CONTRIBUTION_REQUIRED",
      requiredMonthlyContribution: 0,
      observedMonthlySurplus: null,
      affordabilityGap: null,
      evidenceMonthCount: evidenceMonths.length,
      evidenceMonths,
      reason: null,
      reasonCode: null,
    };
  }

  // Fail closed on technical failure. A transient network or server error is
  // not thin history: computing over the months that happened to succeed
  // would publish a confident verdict from a silently degraded sample.
  if (anyRetrievalFailed) {
    return insufficient("CASH_FLOW_UNAVAILABLE", CASH_FLOW_UNAVAILABLE_REASON);
  }
  if (cashAccountsStatus === "error") {
    return insufficient("CASH_ACCOUNTS_UNAVAILABLE", CASH_ACCOUNTS_UNAVAILABLE_REASON);
  }

  // Nothing loaded at all (never fetched, or fetched outside the window) —
  // distinct from "loaded, but every month predates tracking" below.
  if (successMonths.length === 0) {
    return insufficient("NO_RECORDED_MONTH", NO_RECORDED_MONTH_REASON);
  }

  // Every successfully-loaded month failed the pre-tracking presence gate:
  // no recording population is proven anywhere in the window. Three
  // successful empty months from a workspace that tracks no cash accounts,
  // or from before any account began tracking, must not become a measured
  // ฿0 surplus.
  if (evidenceMonths.length === 0) {
    return insufficient("NO_TRACKED_CASH_FLOW", NO_TRACKED_CASH_FLOW_REASON);
  }

  const summaries = evidenceMonths.map((month) => summaryByMonth.get(month)!);
  const netFlows = summaries.map((summary) => summary.netCashFlow);
  const observedMonthlySurplus = roundCurrency(netFlows.reduce((sum, value) => sum + value, 0) / netFlows.length);
  const affordabilityGap = roundCurrency(observedMonthlySurplus - required.requiredMonthlyContribution);
  const state: GoalAffordabilityState =
    observedMonthlySurplus >= required.requiredMonthlyContribution ? "AFFORDABLE" : "SHORTFALL";

  return {
    state,
    requiredMonthlyContribution: required.requiredMonthlyContribution,
    observedMonthlySurplus,
    affordabilityGap,
    evidenceMonthCount: evidenceMonths.length,
    evidenceMonths,
    reason: null,
    reasonCode: null,
  };
}
