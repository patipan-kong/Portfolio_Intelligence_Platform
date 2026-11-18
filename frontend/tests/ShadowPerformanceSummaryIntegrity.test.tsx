import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import type { PortfolioAttributionResult } from "@/lib/api";
import { fmtPct, windowedDivergence } from "@/lib/shadowSummary";
import ShadowPortfolioPanel from "@/components/ShadowPortfolioPanel";
import { DecisionActionPanel } from "@/components/optimizer/DecisionActionPanel";

// Phase 4.23 — Shadow Performance summary integrity (frontend).

const {
  getShadowPerformanceSummary, getAttributionSummary,
  listExecutionDecisions, getExecutionDecision, getExecutionDetail, recordDecisionBySnapshot,
} = vi.hoisted(() => ({
  getShadowPerformanceSummary: vi.fn(), getAttributionSummary: vi.fn(),
  listExecutionDecisions: vi.fn(), getExecutionDecision: vi.fn(),
  getExecutionDetail: vi.fn(), recordDecisionBySnapshot: vi.fn(),
}));
vi.mock("@/lib/api", () => ({
  getShadowPerformanceSummary, getAttributionSummary,
  listExecutionDecisions, getExecutionDecision, getExecutionDetail, recordDecisionBySnapshot,
}));

const item = (o: Record<string, unknown> = {}) => ({
  shadow_id: 1, shadow_type: "STATIC_FROZEN", name: "s", inception_date: "2026-10-01",
  inception_value: 100, current_value: 100, inception_return_pct: 2.5, last_valued_at: null,
  latest_alpha: 0.4, latest_benchmark_return_pct: null, snapshot_count: 10, ...o,
});

function attr(o: Partial<PortfolioAttributionResult> = {}): PortfolioAttributionResult {
  return {
    portfolio_id: 1, evaluation_window_days: 30, period_start: "2026-10-17", period_end: "2026-11-16",
    status: "ok", data_points_available: 20, required_days_remaining: 0, has_sufficient_history: true,
    actual: { return_pct: 1.0, max_drawdown_pct: 2, annualized_volatility: null, snapshot_count: 20 },
    static_shadow: { shadow_id: 9, return_pct: 4.0, max_drawdown_pct: 6.5, annualized_volatility: null },
    static_shadow_selection: {
      status: "selected", shadow_id: 9, inception_date: "2026-09-01",
      first_valuation: "2026-10-17", last_valuation: "2026-11-16",
    },
    ai_model_shadow: { shadow_id: 5, return_pct: 2.0, max_drawdown_pct: 1, annualized_volatility: null },
    ai_model_shadow_coverage: { window_covered: true, first_valuation: "2026-10-17", last_valuation: "2026-11-16" },
    avoided_drawdown_pct: 1, regret_score: 1, ai_outperformed: true, interpretation: "", computed_at: "",
    ...o,
  } as PortfolioAttributionResult;
}

const NO_SELECTION = {
  status: "no_eligible_shadow" as const,
  shadow_id: null, inception_date: null, first_valuation: null, last_valuation: null,
};

beforeEach(() => {
  [getShadowPerformanceSummary, getAttributionSummary, listExecutionDecisions,
    getExecutionDecision, getExecutionDetail, recordDecisionBySnapshot].forEach((m) => m.mockReset());
});

describe("windowedDivergence / fmtPct", () => {
  test("matching verified window gives static minus actual", () => {
    expect(windowedDivergence(attr(), "static")).toBeCloseTo(3.0);
  });
  test("static comparison without a verified selection is null", () => {
    expect(windowedDivergence(attr({ static_shadow_selection: NO_SELECTION }), "static")).toBeNull();
    expect(windowedDivergence(attr({ static_shadow_selection: undefined }), "static")).toBeNull();
  });
  test("AI shadow incepted after the window start is null; before it is AI minus actual", () => {
    expect(windowedDivergence(attr(), "ai", "2026-11-01")).toBeNull();
    expect(windowedDivergence(attr(), "ai", "2026-10-01")).toBeCloseTo(1.0);
    expect(windowedDivergence(attr(), "ai", null)).toBeNull();
  });
  test("AI shadow not proven to cover the window is null despite early inception", () => {
    const cov = (window_covered: boolean | undefined) =>
      attr({ ai_model_shadow_coverage: window_covered === undefined ? undefined : { window_covered, first_valuation: null, last_valuation: null } });
    expect(windowedDivergence(cov(false), "ai", "2026-10-01")).toBeNull();
    expect(windowedDivergence(cov(undefined), "ai", "2026-10-01")).toBeNull();
  });
  test("missing actual return is null", () => {
    expect(windowedDivergence(attr({ actual: { return_pct: null } as never }), "static")).toBeNull();
  });
  test("zero is formatted, missing is a dash", () => {
    expect(fmtPct(0)).toBe("0.00%");
    expect(fmtPct(null)).toBe("-");
    expect(fmtPct(undefined)).toBe("-");
  });
});

describe("ShadowPortfolioPanel", () => {
  test("labels since-inception and 30D groups separately; divergence uses the 30D pair", async () => {
    getShadowPerformanceSummary.mockResolvedValue({
      has_shadows: true, shadows: [], summary: {
        static_frozen: item(),
        active_model: item({ shadow_type: "ACTIVE_MODEL", shadow_id: 2, inception_date: "2026-01-01", inception_return_pct: 50 }),
        tracking_since: null,
      },
    });
    getAttributionSummary.mockResolvedValue({ current: attr() });
    render(<ShadowPortfolioPanel portfolioId={1} />);
    expect(await screen.findByText(/Latest Frozen Decision — since inception/)).toBeInTheDocument();
    expect(screen.getByText(/Historical Attribution — 30D window/)).toBeInTheDocument();
    expect(screen.getByText("+2.50%")).toBeInTheDocument(); // since-inception return
    expect(screen.getByText("+3.00%")).toBeInTheDocument(); // 30D: 4.0 - 1.0
    expect(screen.queryByText("+1.50%")).not.toBeInTheDocument(); // never 2.5 - 1.0
  });

  test("mismatched windows make divergence a dash, not a subtraction", async () => {
    getShadowPerformanceSummary.mockResolvedValue({
      has_shadows: true, shadows: [], summary: {
        static_frozen: item(),
        active_model: item({ shadow_type: "ACTIVE_MODEL", shadow_id: 2, inception_date: "2026-11-10", inception_return_pct: 9 }),
        tracking_since: null,
      },
    });
    getAttributionSummary.mockResolvedValue({ current: attr({ static_shadow_selection: undefined }) });
    render(<ShadowPortfolioPanel portfolioId={1} />);
    await screen.findByText(/Historical Attribution/);
    expect(screen.queryByText("+1.50%")).not.toBeInTheDocument();
    expect(screen.queryByText("+8.00%")).not.toBeInTheDocument();
    expect(screen.queryByText("+3.00%")).not.toBeInTheDocument();
  });

  test("no frozen decision shows an explicit message instead of numbers", async () => {
    getShadowPerformanceSummary.mockResolvedValue({
      has_shadows: true, shadows: [], summary: { static_frozen: null, active_model: null, tracking_since: null },
    });
    getAttributionSummary.mockResolvedValue({ current: attr() });
    render(<ShadowPortfolioPanel portfolioId={1} />);
    expect(await screen.findByText(/No execution decision has been frozen yet/)).toBeInTheDocument();
  });
});

describe("DecisionActionPanel shadow chips", () => {
  const mountApproved = async (summary: unknown) => {
    listExecutionDecisions.mockResolvedValue([{
      id: 7, portfolio_id: 1, recommendation_snapshot_id: 5,
      optimizer_history_id: null, decision: "APPROVED", override_notes: null, override_type: null,
      original_symbol: null, replacement_symbol: null, reason_category: null, expiry_reason: null,
      is_system_generated: false, executed_at: "2026-08-20T00:00:00Z", created_at: "2026-08-20T00:00:00Z",
    }]);
    getExecutionDecision.mockResolvedValue({ approved_allocations: null, rejected_symbols: null, recommendation_snapshot: null });
    getShadowPerformanceSummary.mockResolvedValue(summary);
    getExecutionDetail.mockResolvedValue(null);
    render(<DecisionActionPanel snapshotId={5} portfolioId={1} />);
    await screen.findByText(/Shadow Tracking Active/);
  };

  test("genuine 0.0% return is shown, not treated as missing", async () => {
    await mountApproved({
      has_shadows: true, shadows: [item()],
      summary: { static_frozen: item({ inception_return_pct: 0, latest_alpha: null }), active_model: null, tracking_since: null },
    });
    expect(screen.getByText("+0.00%")).toBeInTheDocument();
    expect(screen.queryByText(/Performance data available after first daily valuation/)).not.toBeInTheDocument();
  });

  test("missing alpha renders nothing, not +0.00% vs benchmark", async () => {
    await mountApproved({
      has_shadows: true, shadows: [item()],
      summary: { static_frozen: item({ latest_alpha: null }), active_model: null, tracking_since: null },
    });
    expect(screen.queryByText(/vs benchmark/)).not.toBeInTheDocument();
  });

  test("real alpha, including 0, is labelled per shadow", async () => {
    await mountApproved({
      has_shadows: true, shadows: [item()],
      summary: {
        static_frozen: item({ latest_alpha: 0 }),
        active_model: item({ shadow_type: "ACTIVE_MODEL", latest_alpha: 1.25 }),
        tracking_since: null,
      },
    });
    expect(screen.getByText(/Frozen α\s*\+0\.00% vs benchmark/)).toBeInTheDocument();
    expect(screen.getByText(/AI α\s*\+1\.25% vs benchmark/)).toBeInTheDocument();
  });
});
