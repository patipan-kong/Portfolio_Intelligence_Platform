import { beforeEach, describe, expect, test, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import OpportunityCostPage from "@/app/ai-analytics/(hub)/opportunity-cost/page";
import type { OpportunityCostLedger } from "@/lib/api";

const { getOpportunityCost, isUnresolvedPortfolioError } = vi.hoisted(() => ({
  getOpportunityCost: vi.fn(),
  isUnresolvedPortfolioError: vi.fn(() => false),
}));
const reportUnresolvedPortfolio = vi.fn();

vi.mock("@/lib/api", () => ({ getOpportunityCost, isUnresolvedPortfolioError }));

let mockSearchParams = new URLSearchParams();
const push = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
  useSearchParams: () => mockSearchParams,
}));

vi.mock("@/lib/PortfolioContext", () => ({
  usePortfolio: () => ({ currentSelection: 1, reportUnresolvedPortfolio }),
}));

function ledger(overrides: Partial<OpportunityCostLedger> = {}): OpportunityCostLedger {
  return {
    portfolio_id: 1,
    period_days: 90,
    as_of: "2026-09-07T00:00:00Z",
    status: "ok",
    net_opportunity_cost_pct: 1.25,
    graded_count: 1,
    maturing_count: 0,
    rows: [{
      decision_id: 42,
      snapshot_id: 99,
      date: "2026-08-20T00:00:00Z",
      divergence_type: "REJECTED",
      override_type: null,
      original_symbol: null,
      replacement_symbol: null,
      status: "graded",
      grade_kind: "30d",
      counterfactual_recommendation_return_pct: 2,
      actual_return_pct: 3.25,
      counterfactual_delta_pct: 1.25,
      note: "Decision-level approximation.",
    }],
    system_deferrals: [],
    ...overrides,
  };
}

beforeEach(() => {
  mockSearchParams = new URLSearchParams();
  getOpportunityCost.mockReset();
  isUnresolvedPortfolioError.mockReset().mockReturnValue(false);
  push.mockReset();
  reportUnresolvedPortfolio.mockReset();
  window.HTMLElement.prototype.scrollIntoView = vi.fn();
});

describe("RAE-01: opportunity-cost decision target", () => {
  test("without decisionId, preserves the existing 90-day page behavior", async () => {
    getOpportunityCost.mockResolvedValue(ledger());

    render(<OpportunityCostPage />);

    await screen.findByText("Waterfall");
    expect(getOpportunityCost).toHaveBeenCalledWith(1, 90);
    expect(document.activeElement).toBe(document.body);
  });

  test("a matching graded decisionId uses the 365-day window and focuses only its exact decision_id row", async () => {
    mockSearchParams = new URLSearchParams("decisionId=42");
    getOpportunityCost.mockResolvedValue(ledger({
      period_days: 365,
      rows: [
        ledger().rows[0],
        { ...ledger().rows[0], decision_id: 99, divergence_type: "MANUAL_OVERRIDE", note: "Other decision." },
      ],
    }));

    render(<OpportunityCostPage />);

    const target = await screen.findByLabelText("Targeted opportunity-cost evaluation: Ignored · Rec #99");
    expect(getOpportunityCost).toHaveBeenCalledWith(1, 365);
    expect(target).toHaveAttribute("aria-current", "true");
    expect(document.activeElement).toBe(target);
    expect(screen.getByText("Other decision.").closest("[role=button]")).not.toHaveAttribute("aria-current");
  });

  test("a matching maturing decision remains explicit and is focusable without a fabricated value", async () => {
    mockSearchParams = new URLSearchParams("decisionId=55");
    getOpportunityCost.mockResolvedValue(ledger({
      period_days: 365,
      net_opportunity_cost_pct: null,
      graded_count: 0,
      maturing_count: 1,
      rows: [{
        ...ledger().rows[0],
        decision_id: 55,
        status: "maturing",
        grade_kind: null,
        counterfactual_recommendation_return_pct: null,
        actual_return_pct: null,
        counterfactual_delta_pct: null,
        note: "Recommendation shadow has not matured at any horizon within this window yet.",
      }],
    }));

    render(<OpportunityCostPage />);

    const target = await screen.findByLabelText("Targeted opportunity-cost evaluation, still maturing");
    expect(target).toHaveTextContent(/has not matured/);
    expect(target).not.toHaveTextContent(/0\.0%/);
    expect(document.activeElement).toBe(target);
  });

  test("a malformed decisionId leaves the normal page usable", async () => {
    mockSearchParams = new URLSearchParams("decisionId=42x");
    getOpportunityCost.mockResolvedValue(ledger());

    render(<OpportunityCostPage />);

    await screen.findByText("Waterfall");
    expect(getOpportunityCost).toHaveBeenCalledWith(1, 90);
    expect(screen.queryByText(/not present in the current/i)).not.toBeInTheDocument();
  });

  test("a valid unavailable target reports only the bounded evaluation-window limitation", async () => {
    mockSearchParams = new URLSearchParams("decisionId=777");
    getOpportunityCost.mockResolvedValue(ledger({ period_days: 365 }));

    render(<OpportunityCostPage />);

    expect(await screen.findByText("This decision is not present in the current 365-day opportunity-cost evaluation window.")).toBeInTheDocument();
    expect(screen.queryByText(/no opportunity cost exists|no impact|not applicable/i)).not.toBeInTheDocument();
  });
});
