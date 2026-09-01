import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, act, fireEvent } from "@testing-library/react";
import { PortfolioProvider, usePortfolio } from "@/lib/PortfolioContext";
import PortfolioPage from "@/app/portfolio/page";
import type { Portfolio, ExecutionDecisionDetail, TransactionResult } from "@/lib/api";

// Decision -> Transaction Linkage Completion: /portfolio reads ?decision=<id>,
// fetches the decision, switches Current Selection to its portfolio if
// needed, and threads execution_decision_id invisibly into Buy/Sell payloads
// while the banner is active. These tests exercise that wiring end to end
// against a mocked @/lib/api, following the existing TransactionHistoryPage/
// ImportPage test convention (PortfolioProvider + mocked module + a probe
// component for portfolio selection).

const {
  listPortfolios, getHoldings, getPortfolioPrices, getSectorBreakdown,
  removeHolding, analyzeSymbol, updateSwapPermission,
  buyTransaction, sellTransaction, depositTransaction, withdrawTransaction,
  initialPositionTransaction, dividendTransaction, isUnresolvedPortfolioError,
  getExecutionDecision,
  listPortfolioInvestmentMandates, listWealthGoals,
  deletePortfolioInvestmentMandate, putPortfolioInvestmentMandate,
} = vi.hoisted(() => ({
  listPortfolios: vi.fn(),
  getHoldings: vi.fn(),
  getPortfolioPrices: vi.fn(),
  getSectorBreakdown: vi.fn(),
  removeHolding: vi.fn(),
  analyzeSymbol: vi.fn(),
  updateSwapPermission: vi.fn(),
  buyTransaction: vi.fn(),
  sellTransaction: vi.fn(),
  depositTransaction: vi.fn(),
  withdrawTransaction: vi.fn(),
  initialPositionTransaction: vi.fn(),
  dividendTransaction: vi.fn(),
  isUnresolvedPortfolioError: vi.fn(() => false),
  getExecutionDecision: vi.fn(),
  listPortfolioInvestmentMandates: vi.fn(),
  listWealthGoals: vi.fn(),
  deletePortfolioInvestmentMandate: vi.fn(),
  putPortfolioInvestmentMandate: vi.fn(),
}));

vi.mock("@/lib/api", () => ({
  listPortfolios, getHoldings, getPortfolioPrices, getSectorBreakdown,
  removeHolding, analyzeSymbol, updateSwapPermission,
  buyTransaction, sellTransaction, depositTransaction, withdrawTransaction,
  initialPositionTransaction, dividendTransaction, isUnresolvedPortfolioError,
  getExecutionDecision,
  listPortfolioInvestmentMandates, listWealthGoals,
  deletePortfolioInvestmentMandate, putPortfolioInvestmentMandate,
}));

let mockSearchParams = new URLSearchParams();
const routerReplace = vi.fn();

vi.mock("next/navigation", () => ({
  usePathname: () => "/portfolio",
  useSearchParams: () => mockSearchParams,
  useRouter: () => ({ replace: routerReplace, push: vi.fn() }),
}));

function makePortfolio(id: number, name = `P${id}`): Portfolio {
  return { id, name, cash_balance: 100_000, created_at: "2026-01-01T00:00:00Z" };
}

function decisionDetail(overrides: Partial<ExecutionDecisionDetail> = {}): ExecutionDecisionDetail {
  return {
    id: 42,
    portfolio_id: 1,
    recommendation_snapshot_id: 7,
    optimizer_history_id: null,
    decision: "APPROVED",
    override_notes: null,
    override_type: null,
    original_symbol: null,
    replacement_symbol: null,
    reason_category: null,
    is_system_generated: false,
    executed_at: "2026-08-20T00:00:00Z",
    created_at: "2026-08-20T00:00:00Z",
    approved_allocations: null,
    rejected_symbols: null,
    recommendation_snapshot: null,
    ...overrides,
  };
}

function txResult(overrides: Partial<TransactionResult> = {}): TransactionResult {
  return {
    transaction_id: 1,
    type: "BUY",
    symbol: "PTT.BK",
    total_amount: 3500,
    transaction_date: "2026-08-20T00:00:00Z",
    notes: null,
    holding: null,
    cash_balance: 96_500,
    ...overrides,
  };
}

function SwitcherProbe() {
  const { selectPortfolio, loading } = usePortfolio();
  return (
    <div>
      {!loading && <span>ready</span>}
      <button onClick={() => selectPortfolio(1)}>select-1</button>
      <button onClick={() => selectPortfolio(2)}>select-2</button>
    </div>
  );
}

beforeEach(() => {
  localStorage.clear();
  mockSearchParams = new URLSearchParams();
  routerReplace.mockReset();
  listPortfolios.mockReset();
  listPortfolios.mockResolvedValue([makePortfolio(1), makePortfolio(2)]);
  getHoldings.mockReset();
  getHoldings.mockResolvedValue([]);
  getPortfolioPrices.mockReset();
  getPortfolioPrices.mockResolvedValue([]);
  getSectorBreakdown.mockReset();
  getSectorBreakdown.mockResolvedValue(null);
  listPortfolioInvestmentMandates.mockReset();
  listPortfolioInvestmentMandates.mockResolvedValue([]);
  listWealthGoals.mockReset();
  listWealthGoals.mockResolvedValue([]);
  buyTransaction.mockReset();
  buyTransaction.mockResolvedValue(txResult());
  sellTransaction.mockReset();
  sellTransaction.mockResolvedValue(txResult({ type: "SELL" }));
  getExecutionDecision.mockReset();
});

test("no ?decision= param: no banner, ordinary Buy sends no execution_decision_id", async () => {
  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <PortfolioPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText("ready")).toBeInTheDocument());
  await act(async () => screen.getByText("select-1").click());
  await waitFor(() => expect(getHoldings).toHaveBeenCalledWith(1));

  expect(screen.queryByText(/Recording execution for Decision/)).not.toBeInTheDocument();
  expect(getExecutionDecision).not.toHaveBeenCalled();

  await act(async () => screen.getByText("Buy").click());
  await waitFor(() => expect(screen.getByPlaceholderText("AAPL or SCB.BK")).toBeInTheDocument());
});

test("valid ?decision=<id> fetches the decision, switches portfolio, and shows the banner", async () => {
  mockSearchParams = new URLSearchParams("decision=42");
  // Resolve the decision only after the portfolio list has loaded — in the
  // real app, PortfolioProvider is mounted app-wide and portfolios are
  // already loaded long before a user follows a "Record execution" deep
  // link; a bare mockResolvedValue here would race the two independent
  // mocked fetches and isn't representative.
  let resolveDecision!: (v: ExecutionDecisionDetail) => void;
  getExecutionDecision.mockImplementation(
    () => new Promise((r) => (resolveDecision = r))
  );

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <PortfolioPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText("ready")).toBeInTheDocument());
  await act(async () => resolveDecision(decisionDetail({ id: 42, portfolio_id: 2, decision: "APPROVED" })));

  await waitFor(() => expect(screen.getByText(/Recording execution for Decision #42/)).toBeInTheDocument());
  // The decision belongs to portfolio 2 — Current Selection must follow it.
  await waitFor(() => expect(getHoldings).toHaveBeenCalledWith(2));
});

test("a decision resolving before the portfolio list loads does not wipe the persisted selection, and activates once portfolios arrive", async () => {
  mockSearchParams = new URLSearchParams("decision=42");
  localStorage.setItem("workspace_current_selection", "1");

  let resolvePortfolios!: (v: Portfolio[]) => void;
  listPortfolios.mockReset();
  listPortfolios.mockImplementation(() => new Promise((r) => (resolvePortfolios = r)));
  getExecutionDecision.mockResolvedValue(decisionDetail({ id: 42, portfolio_id: 2 }));

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <PortfolioPage />
    </PortfolioProvider>
  );

  // The decision resolves immediately — well before the portfolio list does
  // (a fresh direct load / pasted deep link / new tab). It must be deferred,
  // not acted on: no banner yet, and critically the persisted selection must
  // survive rather than being wiped to NONE by a selectPortfolio() call
  // against an empty, not-yet-loaded portfolio list.
  await waitFor(() => expect(getExecutionDecision).toHaveBeenCalledWith(42));
  expect(screen.queryByText(/Recording execution for Decision/)).not.toBeInTheDocument();
  expect(localStorage.getItem("workspace_current_selection")).toBe("1");

  // Portfolio list now arrives — the deferred activation runs against a
  // real, resolvable list.
  await act(async () => resolvePortfolios([makePortfolio(1), makePortfolio(2)]));

  await waitFor(() => expect(screen.getByText(/Recording execution for Decision #42/)).toBeInTheDocument());
  await waitFor(() => expect(getHoldings).toHaveBeenCalledWith(2));
  expect(localStorage.getItem("workspace_current_selection")).toBe("2");
});

test("Clear removes the banner and strips the query param", async () => {
  mockSearchParams = new URLSearchParams("decision=42");
  getExecutionDecision.mockResolvedValue(decisionDetail({ id: 42, portfolio_id: 1 }));

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <PortfolioPage />
    </PortfolioProvider>
  );
  await act(async () => screen.getByText("select-1").click());
  await waitFor(() => expect(screen.getByText(/Recording execution for Decision #42/)).toBeInTheDocument());

  await act(async () => screen.getByText("Clear").click());

  expect(screen.queryByText(/Recording execution for Decision/)).not.toBeInTheDocument();
  expect(routerReplace).toHaveBeenCalledWith("/portfolio");
});

test("manually switching to a different portfolio clears the active decision context", async () => {
  mockSearchParams = new URLSearchParams("decision=42");
  getExecutionDecision.mockResolvedValue(decisionDetail({ id: 42, portfolio_id: 1 }));

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <PortfolioPage />
    </PortfolioProvider>
  );
  await act(async () => screen.getByText("select-1").click());
  await waitFor(() => expect(screen.getByText(/Recording execution for Decision #42/)).toBeInTheDocument());

  // User manually navigates to a different portfolio than the decision's own.
  await act(async () => screen.getByText("select-2").click());

  await waitFor(() => expect(screen.queryByText(/Recording execution for Decision/)).not.toBeInTheDocument());
});

test("Buy while a decision context is active links the transaction; Buy after Clear does not", async () => {
  mockSearchParams = new URLSearchParams("decision=42");
  getExecutionDecision.mockResolvedValue(decisionDetail({ id: 42, portfolio_id: 1 }));

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <PortfolioPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText("ready")).toBeInTheDocument());
  await act(async () => screen.getByText("select-1").click());
  await waitFor(() => expect(screen.getByText(/Recording execution for Decision #42/)).toBeInTheDocument());

  await act(async () => screen.getByText("Buy").click());
  await waitFor(() => expect(screen.getByPlaceholderText("AAPL or SCB.BK")).toBeInTheDocument());
  await act(async () => {
    fireEvent.change(screen.getByPlaceholderText("AAPL or SCB.BK"), { target: { value: "PTT" } });
    fireEvent.change(screen.getByPlaceholderText("0"), { target: { value: "100" } });
    fireEvent.change(screen.getByPlaceholderText("0.00"), { target: { value: "35" } });
  });

  await act(async () => screen.getByText("Confirm Buy").click());

  await waitFor(() => expect(buyTransaction).toHaveBeenCalledTimes(1));
  expect(buyTransaction.mock.calls[0][1]).toMatchObject({ execution_decision_id: 42 });

  // Banner persists across the trade (multi-trade decisions) until Clear.
  expect(screen.getByText(/Recording execution for Decision #42/)).toBeInTheDocument();
  await act(async () => screen.getByText("Done").click());
  await act(async () => screen.getByText("Clear").click());

  buyTransaction.mockClear();
  await act(async () => screen.getByText("Buy").click());
  await waitFor(() => expect(screen.getByPlaceholderText("AAPL or SCB.BK")).toBeInTheDocument());
  await act(async () => {
    fireEvent.change(screen.getByPlaceholderText("AAPL or SCB.BK"), { target: { value: "PTT" } });
    fireEvent.change(screen.getByPlaceholderText("0"), { target: { value: "50" } });
    fireEvent.change(screen.getByPlaceholderText("0.00"), { target: { value: "35" } });
  });
  await act(async () => screen.getByText("Confirm Buy").click());

  await waitFor(() => expect(buyTransaction).toHaveBeenCalledTimes(1));
  expect(buyTransaction.mock.calls[0][1]).not.toHaveProperty("execution_decision_id");
});

test("a stale decision response cannot attach to a later portfolio selection", async () => {
  mockSearchParams = new URLSearchParams("decision=1");
  let resolveFirst!: (v: ExecutionDecisionDetail) => void;
  const firstPending = new Promise<ExecutionDecisionDetail>((r) => (resolveFirst = r));
  getExecutionDecision.mockImplementation((id: number) =>
    id === 1 ? firstPending : Promise.resolve(decisionDetail({ id: 2, portfolio_id: 2 }))
  );

  const { rerender } = render(
    <PortfolioProvider>
      <SwitcherProbe />
      <PortfolioPage />
    </PortfolioProvider>
  );
  await act(async () => screen.getByText("select-1").click());
  await waitFor(() => expect(getExecutionDecision).toHaveBeenCalledWith(1));

  // URL moves on to a second decision before the first request resolves.
  mockSearchParams = new URLSearchParams("decision=2");
  await act(async () => {
    rerender(
      <PortfolioProvider>
        <SwitcherProbe />
        <PortfolioPage />
      </PortfolioProvider>
    );
  });
  await waitFor(() => expect(screen.getByText(/Recording execution for Decision #2/)).toBeInTheDocument());

  // The stale first response now resolves — it must be discarded, not
  // override the already-established decision #2 context.
  await act(async () => resolveFirst(decisionDetail({ id: 1, portfolio_id: 1 })));

  expect(screen.getByText(/Recording execution for Decision #2/)).toBeInTheDocument();
  expect(screen.queryByText(/Recording execution for Decision #1\b/)).not.toBeInTheDocument();
});
