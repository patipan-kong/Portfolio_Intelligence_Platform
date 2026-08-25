import { describe, expect, test } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import TransactionHistoryTable from "@/components/TransactionHistoryTable";
import type { PositionConversionDetail, TransactionRecord } from "@/lib/api";

function tx(overrides: Partial<TransactionRecord> = {}): TransactionRecord {
  return {
    id: 1,
    portfolio_id: 4,
    symbol: "KBANK.BK",
    type: "BUY",
    shares: 10,
    price_per_share: 150,
    total_amount: 1500,
    fees: 2.35,
    taxes: 0,
    currency: "THB",
    exchange_rate: 1,
    transaction_date: "2026-08-01T04:00:00Z",
    notes: null,
    sector: "Financials",
    created_at: "2026-08-01T04:00:01Z",
    ...overrides,
  };
}

function conversionDetail(overrides: Partial<PositionConversionDetail> = {}): PositionConversionDetail {
  return {
    predecessor_symbol: "BANPU.BK",
    successor_symbol: "BANPUU.BK",
    conversion_ratio: 0.38242,
    shares_surrendered: 6700,
    shares_entitled: 2562.214,
    shares_received: 2562.214,
    legal_effective_date: "2026-03-02",
    valuation_transition_date: "2026-03-02",
    cost_basis_before: 48709,
    cost_basis_carried: 48709,
    cash_in_lieu: null,
    ...overrides,
  };
}

describe("TransactionHistoryTable", () => {
  test("shows a clear empty state when there are no transactions", () => {
    render(<TransactionHistoryTable transactions={[]} />);
    expect(screen.getByText(/No transactions recorded/)).toBeInTheDocument();
  });

  test("renders a BUY row with symbol, shares, price and amount", () => {
    render(<TransactionHistoryTable transactions={[tx()]} />);
    expect(screen.getAllByText("Buy").length).toBeGreaterThan(0);
    expect(screen.getAllByText("KBANK").length).toBeGreaterThan(0);
    expect(screen.getAllByText("10.0000").length).toBeGreaterThan(0);
    expect(screen.getAllByText("150.00").length).toBeGreaterThan(0);
    expect(screen.getAllByText(/1,500\.00/).length).toBeGreaterThan(0);
  });

  test("renders a cash-only transaction (no symbol) as 'Cash', not a broken link", () => {
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 2,
            type: "DEPOSIT",
            symbol: null,
            shares: null,
            price_per_share: null,
            total_amount: 5000,
            sector: null,
          }),
        ]}
      />
    );
    expect(screen.getAllByText("Deposit").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Cash").length).toBeGreaterThan(0);
  });

  test("renders QUANTITY_CORRECTION with its notes (the only place the correction's sign is available) and marks the amount as not a cash flow", () => {
    // backend/services/portfolio_transactions.py::execute_quantity_correction
    // always populates shares (abs(delta)), price_per_share, and total_amount
    // (abs(delta) * price) — total_amount is a valuation, and the function's
    // own docstring is explicit that it "does NOT affect cash_balance."
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 3,
            type: "QUANTITY_CORRECTION",
            shares: 5,
            price_per_share: 150,
            total_amount: 750,
            notes: "Quantity correction: +5 shares",
          }),
        ]}
      />
    );
    expect(screen.getAllByText("Quantity Correction").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Quantity correction: +5 shares").length).toBeGreaterThan(0);
    expect(screen.getAllByText("(no cash impact)").length).toBeGreaterThan(0);
  });

  test("renders POSITION_CONVERSION with its real (non-null) fields and marks the amount as not a cash flow", () => {
    // backend/services/portfolio_transactions.py::execute_position_conversion
    // (E9) always populates symbol (the predecessor symbol), shares (the
    // successor shares received), price_per_share (carried basis / shares
    // received), and total_amount (the carried cost basis) — none of these
    // are null, and total_amount is a cost-basis figure, never a cash flow.
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 4,
            type: "POSITION_CONVERSION",
            symbol: "BANPU.BK",
            shares: 2562.214,
            price_per_share: 19.010512,
            total_amount: 48709,
            notes: "BANPU.BK -> BANPUU.BK",
          }),
        ]}
      />
    );
    expect(screen.getAllByText("Position Conversion").length).toBeGreaterThan(0);
    expect(screen.getAllByText("BANPU").length).toBeGreaterThan(0);
    expect(screen.getAllByText(/48,709\.00/).length).toBeGreaterThan(0);
    expect(screen.getAllByText("(no cash impact)").length).toBeGreaterThan(0);
  });

  test("renders a DIVIDEND on a specific symbol honestly: symbol is linked, shares/price stay null rather than fabricated", () => {
    // backend/services/portfolio_transactions.py::execute_dividend always
    // sets shares=None and price_per_share=None, even when a symbol is
    // given — a dividend is a cash amount, not a share transaction.
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 5,
            type: "DIVIDEND",
            symbol: "ADVANC.BK",
            shares: null,
            price_per_share: null,
            total_amount: 320,
            notes: null,
          }),
        ]}
      />
    );
    expect(screen.getAllByText("Dividend").length).toBeGreaterThan(0);
    expect(screen.getAllByText("ADVANC").length).toBeGreaterThan(0);
    expect(screen.getAllByText("—").length).toBeGreaterThan(0); // shares/price cells, honestly blank
    expect(screen.queryByText("(no cash impact)")).not.toBeInTheDocument(); // a dividend IS a cash flow
  });

  test("renders multiple rows sorted as given (API returns most-recent-first)", () => {
    render(
      <TransactionHistoryTable
        transactions={[
          tx({ id: 10, type: "SELL", transaction_date: "2026-08-05T00:00:00Z" }),
          tx({ id: 11, type: "BUY", transaction_date: "2026-08-01T00:00:00Z" }),
        ]}
      />
    );
    expect(screen.getAllByText("Sell").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Buy").length).toBeGreaterThan(0);
  });
});

describe("POSITION_CONVERSION detail affordance", () => {
  test("a conversion row with structured detail gets a Details toggle; ordinary rows do not", () => {
    render(
      <TransactionHistoryTable
        transactions={[
          tx({ id: 20, type: "BUY" }),
          tx({ id: 21, type: "POSITION_CONVERSION", symbol: "BANPU.BK", conversion_detail: conversionDetail() }),
        ]}
      />
    );
    expect(screen.getAllByText("Details ▾").length).toBeGreaterThan(0);
  });

  test("expanding shows predecessor -> successor identity, ratio and share quantities", () => {
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 22,
            type: "POSITION_CONVERSION",
            symbol: "BANPU.BK",
            conversion_detail: conversionDetail(),
          }),
        ]}
      />
    );
    fireEvent.click(screen.getAllByText("Details ▾")[0]);

    expect(screen.getAllByText("From").length).toBeGreaterThan(0);
    expect(screen.getAllByText("To").length).toBeGreaterThan(0);
    expect(screen.getAllByText("BANPU").length).toBeGreaterThan(0);
    expect(screen.getAllByText("BANPUU").length).toBeGreaterThan(0);
    expect(screen.getAllByText("0.38242").length).toBeGreaterThan(0);
    expect(screen.getAllByText("6,700.0000").length).toBeGreaterThan(0);
    expect(screen.getAllByText("2,562.2140").length).toBeGreaterThan(0);
  });

  test("effective date and cost-basis fields render when available", () => {
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 23,
            type: "POSITION_CONVERSION",
            symbol: "BANPU.BK",
            conversion_detail: conversionDetail({
              legal_effective_date: "2026-03-02",
              valuation_transition_date: "2026-03-02",
              cost_basis_before: 48709,
              cost_basis_carried: 48709,
            }),
          }),
        ]}
      />
    );
    fireEvent.click(screen.getAllByText("Details ▾")[0]);

    expect(screen.getAllByText("Effective date").length).toBeGreaterThan(0);
    expect(screen.getAllByText("02 Mar 2026").length).toBeGreaterThan(0);
    // legal_effective_date === valuation_transition_date here, so the
    // distinct "Valuation transition date" field is correctly omitted.
    expect(screen.queryByText("Valuation transition date")).not.toBeInTheDocument();
    expect(screen.getAllByText("Cost basis before").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Cost basis carried").length).toBeGreaterThan(0);
    expect(screen.getAllByText("48,709.00").length).toBeGreaterThan(0);
  });

  test("no cash-in-lieu leg is represented as an honest 'no cash impact', not silently omitted", () => {
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 24,
            type: "POSITION_CONVERSION",
            symbol: "BANPU.BK",
            total_amount: 48709,
            conversion_detail: conversionDetail({ cash_in_lieu: null }),
          }),
        ]}
      />
    );
    expect(screen.getAllByText("(no cash impact)").length).toBeGreaterThan(0);
    fireEvent.click(screen.getAllByText("Details ▾")[0]);
    expect(screen.getAllByText("Cash in lieu").length).toBeGreaterThan(0);
    expect(screen.getAllByText("None").length).toBeGreaterThan(0);
    expect(screen.queryByText("Realized P/L")).not.toBeInTheDocument();
  });

  test("a real cash-in-lieu leg is surfaced honestly — not labeled 'no cash impact'", () => {
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 25,
            type: "POSITION_CONVERSION",
            symbol: "BANPU.BK",
            total_amount: 48704.93,
            conversion_detail: conversionDetail({
              shares_received: 2562,
              cost_basis_carried: 48704.93,
              cash_in_lieu: { fractional_entitlement_shares: 0.214, net_cash: 4.35, realized_pnl: 0.28 },
            }),
          }),
        ]}
      />
    );
    expect(screen.queryByText("(no cash impact)")).not.toBeInTheDocument();
    expect(screen.getAllByText(/cash in lieu: 4\.35/).length).toBeGreaterThan(0);

    fireEvent.click(screen.getAllByText("Details ▾")[0]);
    expect(screen.getAllByText("Realized P/L").length).toBeGreaterThan(0);
    expect(screen.getAllByText("0.28").length).toBeGreaterThan(0);
  });

  test("a legacy/malformed conversion payload (conversion_detail null) degrades gracefully — row renders, no details toggle", () => {
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 26,
            type: "POSITION_CONVERSION",
            symbol: "BANPU.BK",
            notes: "BANPU.BK -> BANPUU.BK",
            conversion_detail: null,
          }),
        ]}
      />
    );
    expect(screen.getAllByText("Position Conversion").length).toBeGreaterThan(0);
    expect(screen.queryByText("Details ▾")).not.toBeInTheDocument();
    expect(screen.getAllByText("(no cash impact)").length).toBeGreaterThan(0);
  });

  test("expanded detail never renders raw JSON", () => {
    render(
      <TransactionHistoryTable
        transactions={[
          tx({
            id: 27,
            type: "POSITION_CONVERSION",
            symbol: "BANPU.BK",
            conversion_detail: conversionDetail({
              cash_in_lieu: { fractional_entitlement_shares: 0.214, net_cash: 4.35, realized_pnl: 0.28 },
            }),
          }),
        ]}
      />
    );
    fireEvent.click(screen.getAllByText("Details ▾")[0]);
    expect(document.body.textContent).not.toMatch(/[{}[\]]/);
    expect(document.body.textContent).not.toContain('"schema_version"');
  });
});
