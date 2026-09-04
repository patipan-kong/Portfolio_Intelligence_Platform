import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { PlanHistorySection, PLAN_HISTORY_DISCLOSURE } from "@/components/goals/PlanHistorySection";
import type { GoalPlanAmendmentHistory } from "@/lib/api";

const base: GoalPlanAmendmentHistory = {
  id: 1,
  workspace_id: 1,
  wealth_goal_id: 1,
  previous_target_amount: 1_000_000,
  resulting_target_amount: 1_200_000,
  previous_target_date: "2030-01-01",
  resulting_target_date: "2031-01-01",
  previous_priority: "HIGH",
  resulting_priority: "MEDIUM",
  recorded_at: "2026-09-04T12:00:00",
};

describe("PlanHistorySection", () => {
  it("renders only the plan fields that changed", () => {
    render(<PlanHistorySection state={[base]} />);
    expect(screen.getByText("Target amount changed from ฿1,000,000.00 to ฿1,200,000.00.")).toBeInTheDocument();
    expect(screen.getByText("Target date changed from 2030-01-01 to 2031-01-01.")).toBeInTheDocument();
    expect(screen.getByText("Priority changed from High priority to Medium priority.")).toBeInTheDocument();
  });

  it("renders a cleared target date as a plan amendment", () => {
    render(<PlanHistorySection state={[{ ...base, previous_target_amount: 1_000_000, resulting_target_amount: 1_000_000, resulting_target_date: null }]} />);
    expect(screen.getByText("Target date changed from 2030-01-01 to No target date.")).toBeInTheDocument();
    expect(screen.queryByText(/Target amount changed/)).not.toBeInTheDocument();
  });

  it("has isolated loading, empty, and failure states with safe wording", () => {
    const { rerender } = render(<PlanHistorySection state={undefined} />);
    expect(screen.getByText("Loading plan history…")).toBeInTheDocument();
    rerender(<PlanHistorySection state={[]} />);
    expect(screen.getByText("No plan amendments recorded yet.")).toBeInTheDocument();
    rerender(<PlanHistorySection state={{ error: "history offline" }} />);
    expect(screen.getByRole("alert")).toHaveTextContent("history offline");
    expect(screen.getByText(PLAN_HISTORY_DISCLOSURE)).toBeInTheDocument();
    expect(screen.queryByText(/contribution occurred|funding changed|optimizer caused/i)).not.toBeInTheDocument();
  });
});
