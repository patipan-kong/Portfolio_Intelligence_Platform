import { beforeEach, describe, expect, test, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ExecutionFollowUpCard from "@/components/evaluation/ExecutionFollowUpCard";
import type { ExecutionReview } from "@/lib/api";

const { getExecutionFollowUp, putExecutionFollowUp } = vi.hoisted(() => ({
  getExecutionFollowUp: vi.fn(),
  putExecutionFollowUp: vi.fn(),
}));

vi.mock("@/lib/api", () => ({ getExecutionFollowUp, putExecutionFollowUp }));

const review: ExecutionReview = {
  id: 1,
  execution_decision_id: 42,
  reviewed_at: "2026-09-07T10:00:00Z",
  outcome: "MIXED",
  summary: "Mixed result",
  changed_context: null,
  created_at: "2026-09-07T10:00:00Z",
  updated_at: "2026-09-07T11:00:00Z",
};

beforeEach(() => {
  getExecutionFollowUp.mockReset().mockResolvedValue({ acknowledged_at: null });
  putExecutionFollowUp.mockReset();
});

describe("ExecutionFollowUpCard", () => {
  test("eligible unacknowledged state offers acknowledgment with the displayed review timestamp", async () => {
    const user = userEvent.setup();
    putExecutionFollowUp.mockResolvedValue({ acknowledged_at: "2026-09-08T03:00:00Z" });

    render(<ExecutionFollowUpCard portfolioId={1} decisionId={42} reviewable review={review} />);

    expect(await screen.findByText("Follow-up attention")).toBeInTheDocument();
    expect(screen.getByText("Acknowledge follow-up")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Acknowledge follow-up" }));

    await waitFor(() => expect(putExecutionFollowUp).toHaveBeenCalledWith(1, 42, {
      acknowledged: true,
      expected_review_updated_at: review.updated_at,
    }));
    expect(await screen.findByText("Follow-up acknowledged on Sep 8, 2026.")).toBeInTheDocument();
    expect(screen.getByText("Return to Needs follow-up")).toBeInTheDocument();
  });

  test("acknowledged state supports an idempotent undo action", async () => {
    const user = userEvent.setup();
    getExecutionFollowUp.mockResolvedValue({ acknowledged_at: "2026-09-08T03:00:00Z" });
    putExecutionFollowUp.mockResolvedValue({ acknowledged_at: null });

    render(<ExecutionFollowUpCard portfolioId={1} decisionId={42} reviewable review={review} />);

    await user.click(await screen.findByRole("button", { name: "Return to Needs follow-up" }));
    await waitFor(() => expect(putExecutionFollowUp).toHaveBeenCalledWith(1, 42, { acknowledged: false }));
    expect(await screen.findByText("Acknowledge follow-up")).toBeInTheDocument();
  });

  test("does not render workflow UI for ineligible review states", async () => {
    const { rerender } = render(
      <ExecutionFollowUpCard portfolioId={1} decisionId={42} reviewable={false} review={review} />,
    );
    expect(screen.queryByText("Follow-up attention")).not.toBeInTheDocument();

    rerender(<ExecutionFollowUpCard portfolioId={1} decisionId={42} reviewable review={{ ...review, outcome: "ON_TRACK" }} />);
    expect(screen.queryByText("Acknowledge follow-up")).not.toBeInTheDocument();
    expect(getExecutionFollowUp).not.toHaveBeenCalled();
  });

  test("surfaces stale-review conflict and asks the parent to refresh", async () => {
    const user = userEvent.setup();
    const onConflict = vi.fn();
    putExecutionFollowUp.mockRejectedValue(new Error("API 409: stale review"));

    render(
      <ExecutionFollowUpCard
        portfolioId={1}
        decisionId={42}
        reviewable
        review={review}
        onConflict={onConflict}
      />,
    );

    await user.click(await screen.findByRole("button", { name: "Acknowledge follow-up" }));
    expect(await screen.findByText("This review changed while you were viewing it. The current review is being refreshed.")).toBeInTheDocument();
    expect(onConflict).toHaveBeenCalled();
  });

  test("does not restore a stale conflict message after a fast canonical-review refresh", async () => {
    const user = userEvent.setup();
    let resolveReload: ((value: { acknowledged_at: null }) => void) | undefined;
    getExecutionFollowUp
      .mockResolvedValueOnce({ acknowledged_at: null })
      .mockImplementationOnce(() => new Promise((resolve) => { resolveReload = resolve; }));
    putExecutionFollowUp.mockRejectedValue(new Error("API 409: stale review"));

    let rerenderCard: ReturnType<typeof render>["rerender"];
    const rendered = render(
      <ExecutionFollowUpCard
        portfolioId={1}
        decisionId={42}
        reviewable
        review={review}
        onConflict={() => rerenderCard(
          <ExecutionFollowUpCard
            portfolioId={1}
            decisionId={42}
            reviewable
            review={{ ...review, updated_at: "2026-09-07T12:00:00Z" }}
          />,
        )}
      />,
    );
    rerenderCard = rendered.rerender;

    await user.click(await screen.findByRole("button", { name: "Acknowledge follow-up" }));
    await waitFor(() => expect(resolveReload).toBeDefined());
    resolveReload?.({ acknowledged_at: null });

    await waitFor(() => expect(screen.queryByRole("alert")).not.toBeInTheDocument());
  });

  test("renders a load error without offering a false acknowledgment", async () => {
    getExecutionFollowUp.mockRejectedValue(new Error("API 500: unavailable"));

    render(<ExecutionFollowUpCard portfolioId={1} decisionId={42} reviewable review={review} />);

    expect(await screen.findByRole("alert")).toHaveTextContent("API 500: unavailable");
    expect(screen.queryByRole("button", { name: "Acknowledge follow-up" })).not.toBeInTheDocument();
  });
});
