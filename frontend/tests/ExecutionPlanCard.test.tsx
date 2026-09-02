import { describe, test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import ExecutionPlanCard from "@/components/optimizer/ExecutionPlanCard";
import type {
  OptimizerResult, ActionSummary, ActionSummaryEntry, TargetAllocation,
  OptimizedTrade, ExecutionOptimizationResult,
} from "@/lib/api";

// Decision Explainability Polish — Slice 2 (A): ExecutionPlanCard already
// receives the structured Reason/Execution Role classification computed by
// execution_optimizer.py (via result.execution_optimization) but never
// rendered it — only `necessity` drove the existing badge. These tests
// exercise the additive Reason/Funding-Source rendering: it must use the
// canonical enum values directly (never recompute or infer them), degrade
// silently when unavailable, and never leak raw enum text as product copy.

function actionSummaryEntry(overrides: Partial<ActionSummaryEntry> = {}): ActionSummaryEntry {
  return { symbol: "KBANK", allocation_change_percent: -5, timing_score: null, ...overrides };
}

function actionSummary(overrides: Partial<ActionSummary> = {}): ActionSummary {
  return { sell: [], reduce: [], accumulate: [], new_position: [], hold: [], ...overrides };
}

function allocation(overrides: Partial<TargetAllocation> = {}): TargetAllocation {
  return {
    symbol: "KBANK",
    current_weight: 10,
    target_weight: 5,
    action: "SELL",
    allocation_change_percent: -5,
    estimated_amount: -50_000,
    reason: "Overweight vs target allocation",
    ...overrides,
  };
}

function optimizedTrade(overrides: Partial<OptimizedTrade> = {}): OptimizedTrade {
  return {
    symbol: "KBANK",
    action: "SELL",
    sector: "Banking",
    reason: "MANDATORY_RISK_REDUCTION",
    necessity: "NECESSARY",
    execution_role: "STANDALONE",
    execution_state: "FULL",
    full_recommended_amount: 50_000,
    executed_amount: 50_000,
    note: "",
    ...overrides,
  };
}

function executionOptimization(trades: OptimizedTrade[]): ExecutionOptimizationResult {
  return { cash_available: 10_000, total_buy_deployment: 0, funding_gap: 0, trades, idle_cash_after: 0 };
}

function baseResult(overrides: Partial<OptimizerResult> = {}): OptimizerResult {
  return {
    portfolio_name: "Core", portfolio_assessment: "Assessment", optimization_notes: "Notes",
    swap_suggestions: [], watchlist_ranking: [], analyzed_at: "2026-09-02T00:00:00Z",
    portfolio_count: 1, max_reached: false,
    ...overrides,
  };
}

function resultWithSellTrade(tradeOverrides: Partial<OptimizedTrade> = {}): OptimizerResult {
  return baseResult({
    action_summary: actionSummary({ sell: [actionSummaryEntry()] }),
    target_allocations: [allocation()],
    execution_optimization: executionOptimization([optimizedTrade(tradeOverrides)]),
  });
}

describe("ExecutionPlanCard structured trade reason", () => {
  test("MANDATORY_RISK_REDUCTION renders its user-facing reason", () => {
    render(<ExecutionPlanCard result={resultWithSellTrade({ reason: "MANDATORY_RISK_REDUCTION" })} />);
    expect(screen.getByText(/Reason: Mandatory risk reduction/)).toBeInTheDocument();
  });

  test("POLICY_ENFORCEMENT renders its user-facing reason", () => {
    render(<ExecutionPlanCard result={resultWithSellTrade({ reason: "POLICY_ENFORCEMENT" })} />);
    expect(screen.getByText(/Reason: Policy enforcement/)).toBeInTheDocument();
  });

  test("PORTFOLIO_IMPROVEMENT renders its user-facing reason", () => {
    render(<ExecutionPlanCard result={resultWithSellTrade({ reason: "PORTFOLIO_IMPROVEMENT" })} />);
    expect(screen.getByText(/Reason: Portfolio improvement/)).toBeInTheDocument();
  });

  test("FUNDING_SOURCE execution role renders a Funding Source indicator", () => {
    render(<ExecutionPlanCard result={resultWithSellTrade({ execution_role: "FUNDING_SOURCE" })} />);
    expect(screen.getByText("Funding source")).toBeInTheDocument();
  });

  test("a SELL trade does not fabricate Funding Source when the structured role says STANDALONE", () => {
    render(<ExecutionPlanCard result={resultWithSellTrade({ action: "SELL", execution_role: "STANDALONE" })} />);
    expect(screen.queryByText("Funding source")).not.toBeInTheDocument();
  });

  test("NOT_NEEDED_TODAY execution role does not render a Funding Source indicator", () => {
    render(<ExecutionPlanCard result={resultWithSellTrade({ execution_role: "NOT_NEEDED_TODAY" })} />);
    expect(screen.queryByText("Funding source")).not.toBeInTheDocument();
  });

  test("missing execution_optimization degrades gracefully — no reason line, no crash", () => {
    const result = baseResult({
      action_summary: actionSummary({ sell: [actionSummaryEntry()] }),
      target_allocations: [allocation()],
      // execution_optimization intentionally omitted (old history payload)
    });
    render(<ExecutionPlanCard result={result} />);
    expect(screen.getByText("KBANK")).toBeInTheDocument();
    expect(screen.queryByText(/^Reason:/)).not.toBeInTheDocument();
    expect(screen.queryByText("Funding source")).not.toBeInTheDocument();
  });

  test("raw enum text is never dumped where product-facing copy is expected", () => {
    render(<ExecutionPlanCard result={resultWithSellTrade({ reason: "MANDATORY_RISK_REDUCTION" })} />);
    expect(screen.queryByText(/MANDATORY_RISK_REDUCTION/)).not.toBeInTheDocument();
    expect(screen.getByText(/Mandatory risk reduction/)).toBeInTheDocument();
  });
});
