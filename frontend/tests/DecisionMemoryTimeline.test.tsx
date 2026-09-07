import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import DecisionMemoryTimeline from "@/components/DecisionMemoryTimeline";
import type { DecisionMemoryEntry, AIvsHumanTimelineEntry } from "@/lib/api";

// Slice 4 (Decision History / Audit UX), Behavior 2: DecisionMemoryTimeline
// already fetched decision_id and recommendation_snapshot.id but exposed no
// row-level navigation. This proves the added drill-down uses exactly those
// already-present IDs — no new data is fetched.

const { getDecisionMemoryTimeline, getAIvsHumanTimeline } = vi.hoisted(() => ({
  getDecisionMemoryTimeline: vi.fn(),
  getAIvsHumanTimeline: vi.fn(),
}));

vi.mock("@/lib/api", () => ({ getDecisionMemoryTimeline, getAIvsHumanTimeline }));

const push = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
}));

function entry(overrides: Partial<DecisionMemoryEntry> = {}): DecisionMemoryEntry {
  return {
    decision_id: 456,
    decision: "APPROVED",
    portfolio_id: 1,
    override_notes: null,
    override_type: null,
    original_symbol: null,
    replacement_symbol: null,
    reason_category: null,
    executed_at: "2026-08-20T00:00:00Z",
    recommendation_snapshot: {
      id: 123,
      persona: null,
      total_portfolio_value: null,
      created_at: "2026-08-19T00:00:00Z",
      consensus: null,
      regime: null,
    },
    shadows: [],
    ...overrides,
  };
}

const aiEmpty: AIvsHumanTimelineEntry[] = [];

beforeEach(() => {
  getDecisionMemoryTimeline.mockReset();
  getAIvsHumanTimeline.mockReset().mockResolvedValue({ timeline: aiEmpty });
  push.mockReset();
});

describe("DecisionMemoryTimeline — historical navigation (Slice 4)", () => {
  test("row navigates to the Recommendation Report Card using recommendation_snapshot.id", async () => {
    getDecisionMemoryTimeline.mockResolvedValue([entry({ decision_id: 456, recommendation_snapshot: { ...entry().recommendation_snapshot!, id: 123 } })]);

    render(<DecisionMemoryTimeline portfolioId={1} />);

    const row = await screen.findByText("Approve Recommendation");
    row.closest("tr")!.click();
    expect(push).toHaveBeenCalledWith("/ai-analytics/recommendations/123");
  });

  test("secondary link navigates to Execution Detail using decision_id and does not trigger row navigation", async () => {
    getDecisionMemoryTimeline.mockResolvedValue([entry({ decision_id: 456 })]);

    render(<DecisionMemoryTimeline portfolioId={1} />);

    const link = await screen.findByText("Execution →");
    expect(link.closest("a")).toHaveAttribute("href", "/ai-analytics/execution/456");

    link.click();
    expect(push).not.toHaveBeenCalled();
  });

  test("REJECTED entries remain navigable to both surfaces", async () => {
    getDecisionMemoryTimeline.mockResolvedValue([
      entry({ decision_id: 789, decision: "REJECTED", recommendation_snapshot: { ...entry().recommendation_snapshot!, id: 321 } }),
    ]);

    render(<DecisionMemoryTimeline portfolioId={1} />);

    expect(await screen.findByText("Reject Recommendation")).toBeInTheDocument();
    const execLink = await screen.findByText("Execution →");
    expect(execLink.closest("a")).toHaveAttribute("href", "/ai-analytics/execution/789");

    const row = screen.getByText("Reject Recommendation").closest("tr")!;
    row.click();
    expect(push).toHaveBeenCalledWith("/ai-analytics/recommendations/321");
  });

  test("EXPIRED entries render a distinct label rather than mislabeling as Partial Execution, and remain navigable", async () => {
    getDecisionMemoryTimeline.mockResolvedValue([
      entry({
        decision_id: 999,
        decision: "EXPIRED" as DecisionMemoryEntry["decision"],
        recommendation_snapshot: { ...entry().recommendation_snapshot!, id: 654 },
      }),
    ]);

    render(<DecisionMemoryTimeline portfolioId={1} />);

    expect(await screen.findByText("Expired")).toBeInTheDocument();
    expect(screen.queryByText("Partial Execution")).not.toBeInTheDocument();
    const execLink = await screen.findByText("Execution →");
    expect(execLink.closest("a")).toHaveAttribute("href", "/ai-analytics/execution/999");
  });

  test("a row with no recommendation_snapshot has no primary navigation but keeps the secondary Execution link", async () => {
    getDecisionMemoryTimeline.mockResolvedValue([entry({ decision_id: 111, recommendation_snapshot: null })]);

    render(<DecisionMemoryTimeline portfolioId={1} />);

    const row = (await screen.findByText("Approve Recommendation")).closest("tr")!;
    expect(row).not.toHaveAttribute("tabindex");
    row.click();
    expect(push).not.toHaveBeenCalled();

    const execLink = await screen.findByText("Execution →");
    expect(execLink.closest("a")).toHaveAttribute("href", "/ai-analytics/execution/111");
  });
});
