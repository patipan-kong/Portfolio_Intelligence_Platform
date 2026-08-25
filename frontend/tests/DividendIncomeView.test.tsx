import { describe, test, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import DividendIncomeView from "@/components/DividendIncomeView";
import type { TransactionRecord } from "@/lib/api";

// The monthly chart is a recharts component behind next/dynamic — its own
// rendering isn't this suite's concern (recharts tests itself); what matters
// here is that DividendIncomeView computes and passes it the right series.
vi.mock("@/components/DividendMonthlyChart", () => ({
  default: ({ data, currency }: { data: Array<{ month: string; amount: number }>; currency: string }) => (
    <div data-testid="monthly-chart">
      {currency}:{data.map((d) => `${d.month}=${d.amount}`).join(",")}
    </div>
  ),
}));

function tx(overrides: Partial<TransactionRecord> & { type: TransactionRecord["type"] }): TransactionRecord {
  return {
    id: 0,
    portfolio_id: 1,
    symbol: null,
    shares: null,
    price_per_share: null,
    total_amount: 0,
    fees: 0,
    taxes: 0,
    currency: "THB",
    exchange_rate: 1,
    transaction_date: "2026-01-15T00:00:00Z",
    notes: null,
    sector: null,
    created_at: null,
    ...overrides,
  };
}

function dividend(overrides: Partial<TransactionRecord> = {}): TransactionRecord {
  return tx({ type: "DIVIDEND", ...overrides });
}

describe("DividendIncomeView", () => {
  test("loading state renders a skeleton, not any income figures", () => {
    render(<DividendIncomeView transactions={[]} loading />);
    expect(screen.queryByText(/Total Dividend Income/)).not.toBeInTheDocument();
  });

  test("no dividend transactions shows an explicit empty state", () => {
    render(
      <DividendIncomeView
        transactions={[tx({ id: 1, type: "BUY", symbol: "AAA", total_amount: 1000 })]}
        loading={false}
      />
    );
    expect(screen.getByText(/No dividend income recorded/)).toBeInTheDocument();
  });

  test("shows the total dividend income summed across all dividend rows", () => {
    const transactions = [
      dividend({ id: 1, symbol: "AAA", total_amount: 100 }),
      dividend({ id: 2, symbol: "BBB", total_amount: 50 }),
      tx({ id: 3, type: "BUY", symbol: "AAA", total_amount: 99999 }),
    ];
    render(<DividendIncomeView transactions={transactions} loading={false} />);
    expect(screen.getByText("THB 150.00")).toBeInTheDocument();
  });

  test("aggregates income by asset, keeping different symbols distinct", () => {
    const transactions = [
      dividend({ id: 1, symbol: "AAA", total_amount: 100 }),
      dividend({ id: 2, symbol: "AAA", total_amount: 50 }),
      dividend({ id: 3, symbol: "BBB", total_amount: 30 }),
    ];
    render(<DividendIncomeView transactions={transactions} loading={false} />);
    // AAA/BBB also appear in the Recent Dividends table (mobile + desktop views).
    expect(screen.getAllByText("AAA").length).toBeGreaterThan(0);
    expect(screen.getAllByText("BBB").length).toBeGreaterThan(0);
    expect(screen.getByText("THB 150.00")).toBeInTheDocument(); // AAA's by-asset total
    expect(screen.getByText("THB 30.00")).toBeInTheDocument(); // BBB's by-asset total
    expect(screen.getByText("THB 180.00")).toBeInTheDocument(); // combined total card
  });

  test("a dividend with no symbol is shown honestly, not dropped or mislabeled", () => {
    const transactions = [
      dividend({ id: 1, symbol: null, total_amount: 40 }),
      dividend({ id: 2, symbol: "AAA", total_amount: 100 }),
    ];
    render(<DividendIncomeView transactions={transactions} loading={false} />);
    expect(screen.getByText("No symbol recorded")).toBeInTheDocument();
    expect(screen.getByText("THB 40.00")).toBeInTheDocument();
  });

  test("feeds the monthly chart a grouped, currency-scoped series", () => {
    const transactions = [
      dividend({ id: 1, total_amount: 100, transaction_date: "2026-01-05T00:00:00Z" }),
      dividend({ id: 2, total_amount: 50, transaction_date: "2026-01-20T00:00:00Z" }),
      dividend({ id: 3, total_amount: 75, transaction_date: "2026-02-01T00:00:00Z" }),
    ];
    render(<DividendIncomeView transactions={transactions} loading={false} />);
    expect(screen.getByTestId("monthly-chart")).toHaveTextContent("THB:2026-01=150,2026-02=75");
  });

  test("recent dividends list renders using the existing transaction table", () => {
    const transactions = [dividend({ id: 1, symbol: "AAA", total_amount: 100, notes: "Q1 payout" })];
    render(<DividendIncomeView transactions={transactions} loading={false} />);
    expect(screen.getByText("Recent Dividends")).toBeInTheDocument();
    // TransactionHistoryTable renders a mobile card view and a desktop table
    // view simultaneously (CSS-hidden, not DOM-absent), so notes appear twice.
    expect(screen.getAllByText("Q1 payout").length).toBeGreaterThan(0);
  });

  test("mixed currencies are shown as separate totals, never summed together", () => {
    const transactions = [
      dividend({ id: 1, symbol: "AAA", total_amount: 100, currency: "THB" }),
      dividend({ id: 2, symbol: "AAPL", total_amount: 5, currency: "USD" }),
    ];
    render(<DividendIncomeView transactions={transactions} loading={false} />);
    // Each currency's own total card and its single by-asset row both read
    // the same (unsummed) amount — 2 occurrences each is expected, not a bug.
    expect(screen.getAllByText("THB 100.00").length).toBe(2);
    expect(screen.getAllByText("USD 5.00").length).toBe(2);
    expect(screen.queryByText("THB 105.00")).not.toBeInTheDocument();
    expect(screen.queryByText("USD 105.00")).not.toBeInTheDocument();
  });
});
