import { describe, expect, test } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import RecommendationComparisonCard from "@/components/evaluation/RecommendationComparisonCard";
import type { RecommendationComparison } from "@/lib/api";

const comparison: RecommendationComparison = {
  current: { snapshot_id: 145, created_at: "2026-09-01T03:00:00Z" },
  previous: { snapshot_id: 138, created_at: "2026-08-25T03:00:00Z" },
  status: "ok",
  as_of: "2026-09-08T10:00:00Z",
  sections: [
    {
      key: "regime",
      label: "Market regime",
      status: "ok",
      changed: true,
      fields: [{ key: "confidence_pct", label: "Confidence", previous: 61.2, current: 74.5, delta: 13.3 }],
    },
    {
      key: "allocations",
      label: "Target allocation",
      status: "ok",
      changed: true,
      fields: [],
      entries: [
        { symbol: "PTT", status: "changed", previous_target_weight: 5, current_target_weight: 8, delta: 3, previous_action: "HOLD", current_action: "BUY" },
        { symbol: "AOT", status: "added", current_target_weight: 4, current_action: "BUY" },
        { symbol: "CPALL", status: "removed", previous_target_weight: 6, previous_action: "HOLD" },
      ],
    },
  ],
};

describe("RecommendationComparisonCard", () => {
  test("is collapsed by default and expands with dates, neutral fields, and navigation", async () => {
    const user = userEvent.setup();
    render(<RecommendationComparisonCard comparison={comparison} portfolioId={7} />);

    expect(screen.getByText("4 · Compared to Previous Recommendation")).toBeInTheDocument();
    expect(screen.queryByText("Previous recommendation")).not.toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /Compared to Previous Recommendation/i }));
    expect(screen.getByText("Previous recommendation")).toBeInTheDocument();
    expect(screen.getByText("Aug 25, 2026")).toBeInTheDocument();
    expect(screen.getByText("Sep 1, 2026")).toBeInTheDocument();
    expect(screen.getByText("Confidence")).toBeInTheDocument();
    expect(screen.getByText("Previous: 61.2")).toBeInTheDocument();
    expect(screen.getByText("Current: 74.5")).toBeInTheDocument();
    expect(screen.getByText("Delta: +13.3")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "View previous recommendation" })).toHaveAttribute(
      "href",
      "/ai-analytics/recommendations/138?portfolio_id=7",
    );
  });

  test("renders allocation additions, removals, and changes without interpretive wording", async () => {
    const user = userEvent.setup();
    render(<RecommendationComparisonCard comparison={comparison} portfolioId={7} />);
    await user.click(screen.getByRole("button", { name: /Compared to Previous Recommendation/i }));

    expect(screen.getByText("PTT")).toBeInTheDocument();
    expect(screen.getByText("AOT")).toBeInTheDocument();
    expect(screen.getByText("CPALL")).toBeInTheDocument();
    expect(screen.getByText("Added")).toBeInTheDocument();
    expect(screen.getByText("Removed")).toBeInTheDocument();
    expect(screen.getByText("Changed")).toBeInTheDocument();
    expect(document.body.textContent).not.toMatch(/improved|worsened|better|worse|material|significant/i);
  });

  test("shows the frozen no-predecessor and no-tracked-change states", () => {
    const { rerender } = render(
      <RecommendationComparisonCard
        comparison={{ ...comparison, previous: null, status: "no_previous", sections: [] }}
        portfolioId={7}
      />,
    );
    expect(screen.getByText("No previous recommendation is available for comparison.")).toBeInTheDocument();

    rerender(<RecommendationComparisonCard comparison={{ ...comparison, sections: [] }} portfolioId={7} />);
    expect(screen.getByText("No tracked recommendation inputs changed from the previous snapshot.")).toBeInTheDocument();
  });

  test("renders unavailable source state explicitly and remains wrapping-safe", async () => {
    const user = userEvent.setup();
    const unavailable: RecommendationComparison = {
      ...comparison,
      sections: [{ key: "constraint_envelope", label: "Constraint envelope", status: "unavailable", changed: false, fields: [], reason: "missing_or_unparseable_source" }],
    };
    const { container } = render(<RecommendationComparisonCard comparison={unavailable} portfolioId={7} />);
    await user.click(screen.getByRole("button", { name: /Compared to Previous Recommendation/i }));
    expect(screen.getByText("Not available for this recommendation.")).toBeInTheDocument();
    expect(container.querySelector(".flex.flex-wrap")).toBeInTheDocument();
  });
});
