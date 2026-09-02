import { describe, test, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, act, fireEvent } from "@testing-library/react";
import { PortfolioProvider, usePortfolio } from "@/lib/PortfolioContext";
import TransactionHistoryPage from "@/app/history/page";
import type { Portfolio, TransactionRecord } from "@/lib/api";

const { listPortfolios, createPortfolio, deletePortfolio, getTransactionHistory, isUnresolvedPortfolioError } =
  vi.hoisted(() => ({
    listPortfolios: vi.fn(),
    createPortfolio: vi.fn(),
    deletePortfolio: vi.fn(),
    getTransactionHistory: vi.fn(),
    isUnresolvedPortfolioError: vi.fn(() => false),
  }));

vi.mock("@/lib/api", () => ({
  listPortfolios,
  createPortfolio,
  deletePortfolio,
  getTransactionHistory,
  isUnresolvedPortfolioError,
}));

// PortfolioTabs (rendered by this page) reads the current route via
// usePathname(), which next/navigation returns as null outside of an actual
// App Router — this test isn't exercising routing, so a fixed path is enough.
vi.mock("next/navigation", () => ({
  usePathname: () => "/history",
}));

function makePortfolio(id: number, name = `P${id}`): Portfolio {
  return { id, name, cash_balance: 0, created_at: "2026-01-01T00:00:00Z" };
}

function tx(overrides: Partial<TransactionRecord> = {}): TransactionRecord {
  return {
    id: 1,
    portfolio_id: 1,
    symbol: "PTT.BK",
    type: "BUY",
    shares: 100,
    price_per_share: 35,
    total_amount: 3500,
    fees: 5.5,
    taxes: 0,
    currency: "THB",
    exchange_rate: 1,
    transaction_date: "2026-08-10T03:00:00Z",
    notes: null,
    sector: "Energy",
    execution_decision_id: null,
    created_at: "2026-08-10T03:00:01Z",
    ...overrides,
  };
}

function SwitcherProbe() {
  const { selectPortfolio, clearSelection } = usePortfolio();
  return (
    <div>
      <button onClick={() => selectPortfolio(1)}>select-A</button>
      <button onClick={() => clearSelection()}>clear</button>
    </div>
  );
}

beforeEach(() => {
  localStorage.clear();
  listPortfolios.mockReset();
  getTransactionHistory.mockReset();
});

test("no portfolio selected: shows the empty/selection state and issues no request", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  expect(getTransactionHistory).not.toHaveBeenCalled();
});

test("selecting a portfolio requests that portfolio's transaction history and renders it", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([tx()]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());

  await act(async () => screen.getByText("select-A").click());

  expect(getTransactionHistory).toHaveBeenCalledWith(1, undefined, 500);
  await waitFor(() => expect(screen.getAllByText("Buy").length).toBeGreaterThan(0));
  expect(screen.getAllByText("PTT").length).toBeGreaterThan(0);
});

test("a portfolio with no transactions shows a clear empty state, not an error", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());

  await waitFor(() => expect(screen.getByText(/No transactions recorded/)).toBeInTheDocument());
});

test("searching by symbol filters the list without issuing another request", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([
    tx({ id: 1, symbol: "BANPU.BK" }),
    tx({ id: 2, symbol: "PTT.BK" }),
  ]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(screen.getAllByText("BANPU").length).toBeGreaterThan(0));

  await act(async () => {
    fireEvent.change(screen.getByPlaceholderText("Search symbol or notes"), { target: { value: "banpu" } });
  });

  expect(screen.getAllByText("BANPU").length).toBeGreaterThan(0);
  expect(screen.queryByText("PTT")).not.toBeInTheDocument();
  expect(screen.getByText("1 of 2 transactions")).toBeInTheDocument();
  expect(getTransactionHistory).toHaveBeenCalledTimes(1);
});

test("the type filter narrows the list to a single transaction type", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([
    tx({ id: 1, type: "BUY", symbol: "PTT.BK" }),
    tx({ id: 2, type: "DIVIDEND", symbol: "ADVANC.BK" }),
  ]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(screen.getAllByText("PTT").length).toBeGreaterThan(0));

  await act(async () => {
    fireEvent.change(screen.getByLabelText("Transaction type"), { target: { value: "DIVIDEND" } });
  });

  // "Buy"/"Dividend" text also appears in the <select>'s own <option>
  // elements, so assert on the row's symbol (unambiguous) rather than the
  // type-badge label.
  expect(screen.queryByText("PTT")).not.toBeInTheDocument();
  expect(screen.getAllByText("ADVANC").length).toBeGreaterThan(0);
  expect(getTransactionHistory).toHaveBeenCalledTimes(1);
});

test("From/To date filters use inclusive boundaries", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([
    tx({ id: 1, symbol: "EARLY.BK", transaction_date: "2026-08-01T03:00:00Z" }),
    tx({ id: 2, symbol: "MID.BK", transaction_date: "2026-08-10T03:00:00Z" }),
    tx({ id: 3, symbol: "LATE.BK", transaction_date: "2026-08-20T03:00:00Z" }),
  ]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(screen.getAllByText("MID").length).toBeGreaterThan(0));

  await act(async () => {
    fireEvent.change(screen.getByLabelText("From"), { target: { value: "2026-08-10" } });
    fireEvent.change(screen.getByLabelText("To"), { target: { value: "2026-08-10" } });
  });

  expect(screen.queryByText("EARLY")).not.toBeInTheDocument();
  expect(screen.getAllByText("MID").length).toBeGreaterThan(0);
  expect(screen.queryByText("LATE")).not.toBeInTheDocument();
  expect(screen.getByText("1 of 3 transactions")).toBeInTheDocument();
});

test("Clear filters restores the complete list", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([
    tx({ id: 1, symbol: "BANPU.BK" }),
    tx({ id: 2, symbol: "PTT.BK" }),
  ]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(screen.getAllByText("BANPU").length).toBeGreaterThan(0));

  await act(async () => {
    fireEvent.change(screen.getByPlaceholderText("Search symbol or notes"), { target: { value: "banpu" } });
  });
  expect(screen.queryByText("PTT")).not.toBeInTheDocument();

  await act(async () => screen.getByText("Clear filters").click());

  expect(screen.getAllByText("BANPU").length).toBeGreaterThan(0);
  expect(screen.getAllByText("PTT").length).toBeGreaterThan(0);
  expect(screen.queryByText("Clear filters")).not.toBeInTheDocument();
});

test("active filters matching nothing show a filter-specific empty state, distinct from a genuinely empty portfolio", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  getTransactionHistory.mockResolvedValue([tx({ id: 1, symbol: "BANPU.BK" })]);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(screen.getAllByText("BANPU").length).toBeGreaterThan(0));

  await act(async () => {
    fireEvent.change(screen.getByPlaceholderText("Search symbol or notes"), { target: { value: "nonexistent" } });
  });

  expect(screen.getByText("No transactions match these filters.")).toBeInTheDocument();
  expect(screen.queryByText(/No transactions recorded/)).not.toBeInTheDocument();
});

test("switching portfolios resets active filters instead of carrying them over", async () => {
  const portfolios = [makePortfolio(1, "A"), makePortfolio(2, "B")];
  listPortfolios.mockResolvedValue(portfolios);
  getTransactionHistory.mockImplementation((portfolioId: number) =>
    Promise.resolve([tx({ id: portfolioId, symbol: portfolioId === 1 ? "AAA.BK" : "BBB.BK" })])
  );

  function TwoPortfolioSwitcher() {
    const { selectPortfolio } = usePortfolio();
    return (
      <div>
        <button onClick={() => selectPortfolio(1)}>select-1</button>
        <button onClick={() => selectPortfolio(2)}>select-2</button>
      </div>
    );
  }

  render(
    <PortfolioProvider>
      <TwoPortfolioSwitcher />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());

  await act(async () => screen.getByText("select-1").click());
  await waitFor(() => expect(screen.getAllByText("AAA").length).toBeGreaterThan(0));

  await act(async () => {
    fireEvent.change(screen.getByPlaceholderText("Search symbol or notes"), { target: { value: "AAA" } });
  });
  expect(screen.getByDisplayValue("AAA")).toBeInTheDocument();

  await act(async () => screen.getByText("select-2").click());
  await waitFor(() => expect(screen.getAllByText("BBB").length).toBeGreaterThan(0));

  // The search box is cleared for the new portfolio, and its one
  // transaction is not hidden by a stale filter from the previous one.
  expect(screen.getByPlaceholderText("Search symbol or notes")).toHaveValue("");
  expect(screen.queryByText("No transactions match these filters.")).not.toBeInTheDocument();
});

test("a late response for an abandoned portfolio does not repopulate the page after clearing selection", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  let resolve!: (v: TransactionRecord[]) => void;
  const pending = new Promise<TransactionRecord[]>((r) => (resolve = r));
  getTransactionHistory.mockReturnValue(pending);

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <TransactionHistoryPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());

  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(getTransactionHistory).toHaveBeenCalledWith(1, undefined, 500));

  await act(async () => screen.getByText("clear").click());
  expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument();

  await act(async () => resolve([tx()]));
  expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument();
});

describe("CSV export", () => {
  let capturedBlobs: Blob[];
  let anchorClicks: { href: string; download: string }[];
  let originalCreateObjectURL: typeof URL.createObjectURL | undefined;
  let originalRevokeObjectURL: typeof URL.revokeObjectURL | undefined;
  let clickSpy: ReturnType<typeof vi.spyOn>;

  beforeEach(() => {
    capturedBlobs = [];
    anchorClicks = [];
    originalCreateObjectURL = URL.createObjectURL;
    originalRevokeObjectURL = URL.revokeObjectURL;
    URL.createObjectURL = vi.fn((blob: Blob) => {
      capturedBlobs.push(blob);
      return `blob:mock-${capturedBlobs.length}`;
    });
    URL.revokeObjectURL = vi.fn();
    // Real anchor.click() triggers jsdom navigation (which isn't
    // implemented and only logs a warning) — intercepting it here keeps
    // the test hermetic and avoids depending on an actual file download.
    clickSpy = vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(function (this: HTMLAnchorElement) {
      anchorClicks.push({ href: this.href, download: this.download });
    });
  });

  afterEach(() => {
    URL.createObjectURL = originalCreateObjectURL as typeof URL.createObjectURL;
    URL.revokeObjectURL = originalRevokeObjectURL as typeof URL.revokeObjectURL;
    clickSpy.mockRestore();
  });

  test("no records: Export CSV control is absent, not merely disabled", async () => {
    listPortfolios.mockResolvedValue([makePortfolio(1)]);
    getTransactionHistory.mockResolvedValue([]);

    render(
      <PortfolioProvider>
        <SwitcherProbe />
        <TransactionHistoryPage />
      </PortfolioProvider>
    );
    await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
    await act(async () => screen.getByText("select-A").click());

    await waitFor(() => expect(screen.getByText(/No transactions recorded/)).toBeInTheDocument());
    expect(screen.queryByText("Export CSV")).not.toBeInTheDocument();
  });

  test("records loaded: Export CSV control appears alongside honest bounded-export wording", async () => {
    listPortfolios.mockResolvedValue([makePortfolio(1)]);
    getTransactionHistory.mockResolvedValue([tx()]);

    render(
      <PortfolioProvider>
        <SwitcherProbe />
        <TransactionHistoryPage />
      </PortfolioProvider>
    );
    await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
    await act(async () => screen.getByText("select-A").click());

    await waitFor(() => expect(screen.getByText("Export CSV")).toBeInTheDocument());
    expect(screen.getByText(/Exports up to the most recent 500 transactions\./)).toBeInTheDocument();
  });

  test("clicking Export CSV downloads a CSV of the loaded records, unaffected by active filters", async () => {
    listPortfolios.mockResolvedValue([makePortfolio(1, "Retirement Fund")]);
    getTransactionHistory.mockResolvedValue([
      tx({ id: 1, symbol: "BANPU.BK" }),
      tx({ id: 2, symbol: "PTT.BK" }),
    ]);

    render(
      <PortfolioProvider>
        <SwitcherProbe />
        <TransactionHistoryPage />
      </PortfolioProvider>
    );
    await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
    await act(async () => screen.getByText("select-A").click());
    await waitFor(() => expect(screen.getAllByText("BANPU").length).toBeGreaterThan(0));

    // Narrow the visible table with a search filter — export must still
    // reflect the full loaded history (Option A), not this filtered view.
    await act(async () => {
      fireEvent.change(screen.getByPlaceholderText("Search symbol or notes"), { target: { value: "banpu" } });
    });
    expect(screen.queryByText("PTT")).not.toBeInTheDocument();

    await act(async () => screen.getByText("Export CSV").click());

    expect(anchorClicks.length).toBe(1);
    expect(anchorClicks[0].download).toMatch(/^wealth-os-transactions-Retirement-Fund-\d{4}-\d{2}-\d{2}\.csv$/);
    expect(capturedBlobs.length).toBe(1);
    const text = await capturedBlobs[0].text();
    expect(text).toContain("BANPU.BK");
    expect(text).toContain("PTT.BK"); // filtered out on screen, still present in the export
    expect(text).not.toMatch(/[{}[\]]/); // no raw JSON leaking into the export

    // The UTF-8 BOM bytes are present in the Blob (for Excel/Thai-text
    // compatibility) even though Blob.text()'s decoder transparently strips
    // them back out of the decoded string above — check the raw bytes instead.
    const bytes = new Uint8Array(await capturedBlobs[0].arrayBuffer()).slice(0, 3);
    expect(Array.from(bytes)).toEqual([0xef, 0xbb, 0xbf]);
  });

  test("switching portfolios exports the newly selected portfolio's records, never the previous one's", async () => {
    const portfolios = [makePortfolio(1, "A"), makePortfolio(2, "B")];
    listPortfolios.mockResolvedValue(portfolios);
    getTransactionHistory.mockImplementation((portfolioId: number) =>
      Promise.resolve([tx({ id: portfolioId, symbol: portfolioId === 1 ? "AAA.BK" : "BBB.BK" })])
    );

    function TwoPortfolioSwitcher() {
      const { selectPortfolio } = usePortfolio();
      return (
        <div>
          <button onClick={() => selectPortfolio(1)}>select-1</button>
          <button onClick={() => selectPortfolio(2)}>select-2</button>
        </div>
      );
    }

    render(
      <PortfolioProvider>
        <TwoPortfolioSwitcher />
        <TransactionHistoryPage />
      </PortfolioProvider>
    );
    await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());

    await act(async () => screen.getByText("select-1").click());
    await waitFor(() => expect(screen.getAllByText("AAA").length).toBeGreaterThan(0));

    await act(async () => screen.getByText("select-2").click());
    await waitFor(() => expect(screen.getAllByText("BBB").length).toBeGreaterThan(0));

    await act(async () => screen.getByText("Export CSV").click());

    const text = await capturedBlobs[0].text();
    expect(text).toContain("BBB.BK");
    expect(text).not.toContain("AAA.BK");
    expect(anchorClicks[0].download).toContain("-B-");
  });
});
