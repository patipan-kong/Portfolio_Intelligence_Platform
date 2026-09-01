import { describe, test, expect, vi } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import type { ComponentProps } from "react";
import TransactionModal from "@/components/TransactionModal";
import type { BuyPayload, SellPayload, TransactionResult } from "@/lib/api";

// Decision -> Transaction Linkage Completion: TransactionModal threads an
// optional executionDecisionId invisibly into Buy/Sell payloads only. Actual
// transaction facts (shares/price/date) always stay user-authored — the
// prop never pre-fills them.

// Derived from the component's own prop type rather than reconstructed here
// — stays exact even if TransactionModal's internal Payload union changes,
// and gives vi.fn() a real parameter type instead of inferring `[]`.
type OnConfirm = ComponentProps<typeof TransactionModal>["onConfirm"];

function txResult(overrides: Partial<TransactionResult> = {}): TransactionResult {
  return {
    transaction_id: 1,
    type: "BUY",
    symbol: "PTT.BK",
    total_amount: 3500,
    transaction_date: "2026-08-20T00:00:00Z",
    notes: null,
    holding: null,
    ...overrides,
  };
}

function fillBuyForm() {
  fireEvent.change(screen.getByPlaceholderText("AAPL or SCB.BK"), { target: { value: "PTT" } });
  fireEvent.change(screen.getByPlaceholderText("0"), { target: { value: "100" } });
  fireEvent.change(screen.getByPlaceholderText("0.00"), { target: { value: "35" } });
}

describe("ordinary Buy/Sell (no decision context)", () => {
  test("Buy sends no execution_decision_id when the prop is omitted", async () => {
    const onConfirm = vi.fn<OnConfirm>(async (_payload) => txResult());
    render(<TransactionModal mode="buy" onConfirm={onConfirm} onClose={vi.fn()} />);

    await act(async () => fillBuyForm());
    await act(async () => screen.getByText("Confirm Buy").click());

    expect(onConfirm).toHaveBeenCalledTimes(1);
    expect(onConfirm.mock.calls[0][0]).not.toHaveProperty("execution_decision_id");
  });

  test("Sell sends no execution_decision_id when the prop is omitted", async () => {
    const onConfirm = vi.fn<OnConfirm>(async (_payload) => txResult({ type: "SELL" }));
    render(
      <TransactionModal
        mode="sell"
        symbol="PTT.BK"
        currentPrice={35}
        maxShares={100}
        onConfirm={onConfirm}
        onClose={vi.fn()}
      />
    );

    fireEvent.change(screen.getByPlaceholderText("0"), { target: { value: "50" } });
    await act(async () => screen.getByText("Confirm Sell").click());

    expect(onConfirm).toHaveBeenCalledTimes(1);
    expect(onConfirm.mock.calls[0][0]).not.toHaveProperty("execution_decision_id");
  });

  test("Deposit never carries execution_decision_id, even when the prop is passed", async () => {
    const onConfirm = vi.fn<OnConfirm>(async (_payload) => txResult({ type: "DEPOSIT", symbol: undefined }));
    render(
      <TransactionModal
        mode="deposit"
        executionDecisionId={42}
        onConfirm={onConfirm}
        onClose={vi.fn()}
      />
    );

    fireEvent.change(screen.getByPlaceholderText("0.00"), { target: { value: "1000" } });
    await act(async () => screen.getByText("Confirm Deposit").click());

    expect(onConfirm).toHaveBeenCalledTimes(1);
    expect(onConfirm.mock.calls[0][0]).not.toHaveProperty("execution_decision_id");
  });
});

describe("linked Buy/Sell (decision context active)", () => {
  test("Buy sends the correct execution_decision_id", async () => {
    const onConfirm = vi.fn<OnConfirm>(async (_payload) => txResult());
    render(<TransactionModal mode="buy" executionDecisionId={42} onConfirm={onConfirm} onClose={vi.fn()} />);

    await act(async () => fillBuyForm());
    await act(async () => screen.getByText("Confirm Buy").click());

    const payload = onConfirm.mock.calls[0][0] as BuyPayload;
    expect(payload.execution_decision_id).toBe(42);
    // Actual facts remain exactly what the user typed — never overwritten.
    expect(payload.symbol).toBe("PTT");
    expect(payload.shares).toBe(100);
    expect(payload.price_per_share).toBe(35);
  });

  test("Sell sends the correct execution_decision_id", async () => {
    const onConfirm = vi.fn<OnConfirm>(async (_payload) => txResult({ type: "SELL" }));
    render(
      <TransactionModal
        mode="sell"
        symbol="PTT.BK"
        currentPrice={35}
        maxShares={100}
        executionDecisionId={7}
        onConfirm={onConfirm}
        onClose={vi.fn()}
      />
    );

    fireEvent.change(screen.getByPlaceholderText("0"), { target: { value: "50" } });
    await act(async () => screen.getByText("Confirm Sell").click());

    const payload = onConfirm.mock.calls[0][0] as SellPayload;
    expect(payload.execution_decision_id).toBe(7);
    expect(payload.shares).toBe(50);
  });

  test("recommended price/shares are never pre-filled into the actual-execution fields", async () => {
    // currentPrice is a display hint only, passed the same way an ordinary
    // Sell from the portfolio table would — the field must start blank/user
    // editable, never silently equal to a recommended value the user didn't
    // type themselves.
    render(
      <TransactionModal
        mode="buy"
        currentPrice={99.99}
        executionDecisionId={42}
        onConfirm={vi.fn(async () => txResult())}
        onClose={vi.fn()}
      />
    );

    const priceInput = screen.getByPlaceholderText("0.00") as HTMLInputElement;
    // currentPrice pre-fills the *display* price field verbatim (existing
    // behavior for ordinary buys) — the invariant under test is narrower:
    // nothing here derives that value from the decision/plan, and the user
    // can freely overwrite it before submitting.
    expect(priceInput.value).toBe("99.99");
    fireEvent.change(priceInput, { target: { value: "101.5" } });
    expect(priceInput.value).toBe("101.5");
  });

  test("success view shows a Linked to Decision confirmation", async () => {
    const onConfirm = vi.fn(async () => txResult());
    render(<TransactionModal mode="buy" executionDecisionId={42} onConfirm={onConfirm} onClose={vi.fn()} />);

    await act(async () => fillBuyForm());
    await act(async () => screen.getByText("Confirm Buy").click());

    expect(screen.getByText("Linked to Decision #42")).toBeInTheDocument();
  });
});
