import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, act, fireEvent } from "@testing-library/react";
import { PortfolioProvider, usePortfolio } from "@/lib/PortfolioContext";
import CsvImportPage from "@/app/import/page";
import type { Portfolio, TransactionResult } from "@/lib/api";

const { listPortfolios, buyTransaction, sellTransaction, dividendTransaction, depositTransaction, withdrawTransaction } =
  vi.hoisted(() => ({
    listPortfolios: vi.fn(),
    buyTransaction: vi.fn(),
    sellTransaction: vi.fn(),
    dividendTransaction: vi.fn(),
    depositTransaction: vi.fn(),
    withdrawTransaction: vi.fn(),
  }));

vi.mock("@/lib/api", () => ({
  listPortfolios,
  buyTransaction,
  sellTransaction,
  dividendTransaction,
  depositTransaction,
  withdrawTransaction,
}));

// PortfolioTabs (rendered by this page) reads the current route via
// usePathname(), which next/navigation returns as null outside of an actual
// App Router — this test isn't exercising routing, so a fixed path is enough.
vi.mock("next/navigation", () => ({
  usePathname: () => "/import",
}));

function makePortfolio(id: number, name = `P${id}`): Portfolio {
  return { id, name, cash_balance: 0, created_at: "2026-01-01T00:00:00Z" };
}

function txResult(overrides: Partial<TransactionResult> = {}): TransactionResult {
  return {
    transaction_id: 1,
    type: "BUY",
    symbol: "PTT.BK",
    total_amount: 3500,
    transaction_date: "2026-08-10T00:00:00Z",
    notes: null,
    holding: null,
    ...overrides,
  };
}

function SwitcherProbe() {
  const { selectPortfolio } = usePortfolio();
  return (
    <>
      <button onClick={() => selectPortfolio(1)}>select-A</button>
      <button onClick={() => selectPortfolio(2)}>select-B</button>
    </>
  );
}

function csvFile(text: string, name = "transactions.csv"): File {
  return new File([text], name, { type: "text/csv" });
}

async function selectPortfolioAndGetInput() {
  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <CsvImportPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());
  await waitFor(() => expect(screen.getByLabelText("Upload CSV file")).toBeInTheDocument());
  return screen.getByLabelText("Upload CSV file") as HTMLInputElement;
}

const HEADER = "date,type,symbol,shares,price,amount,notes";

beforeEach(() => {
  localStorage.clear();
  listPortfolios.mockReset();
  listPortfolios.mockResolvedValue([makePortfolio(1)]);
  buyTransaction.mockReset();
  sellTransaction.mockReset();
  dividendTransaction.mockReset();
  depositTransaction.mockReset();
  withdrawTransaction.mockReset();
});

test("no portfolio selected shows the selection prompt and no upload control", async () => {
  render(
    <PortfolioProvider>
      <CsvImportPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  expect(screen.queryByLabelText("Upload CSV file")).not.toBeInTheDocument();
});

test("uploading a CSV with valid and invalid rows shows a preview with both counted and highlighted", async () => {
  const input = await selectPortfolioAndGetInput();
  const text = [
    HEADER,
    "2026-08-10,BUY,PTT.BK,100,35,,first buy",
    "2026-08-11,BUY,,100,35,,missing symbol",
  ].join("\n");

  await act(async () => {
    fireEvent.change(input, { target: { files: [csvFile(text)] } });
  });

  await waitFor(() => expect(screen.getByText(/1 valid, 1 invalid/)).toBeInTheDocument());
  expect(screen.getByText("Valid")).toBeInTheDocument();
  expect(screen.getByText("Invalid")).toBeInTheDocument();
  expect(screen.getByText("Symbol is required")).toBeInTheDocument();
});

test("a structurally broken CSV shows a parsing error, not a preview table", async () => {
  const input = await selectPortfolioAndGetInput();
  const text = "date,type,symbol,shares,price,notes\n2026-08-10,BUY,PTT.BK,100,35,note";

  await act(async () => {
    fireEvent.change(input, { target: { files: [csvFile(text)] } });
  });

  await waitFor(() => expect(screen.getByText(/Missing required column/)).toBeInTheDocument());
  expect(screen.queryByText(/valid,.*invalid/)).not.toBeInTheDocument();
});

test("import calls the correct API for each transaction type and reports success counts", async () => {
  buyTransaction.mockResolvedValue(txResult({ type: "BUY" }));
  sellTransaction.mockResolvedValue(txResult({ type: "SELL" }));
  dividendTransaction.mockResolvedValue(txResult({ type: "DIVIDEND" }));
  depositTransaction.mockResolvedValue(txResult({ type: "DEPOSIT", symbol: null }));
  withdrawTransaction.mockResolvedValue(txResult({ type: "WITHDRAW", symbol: null }));

  const input = await selectPortfolioAndGetInput();
  const text = [
    HEADER,
    "2026-08-10,BUY,PTT.BK,100,35,,",
    "2026-08-10,SELL,PTT.BK,50,36,,",
    "2026-08-10,DIVIDEND,PTT.BK,,,250,",
    "2026-08-10,DEPOSIT,,,,10000,",
    "2026-08-10,WITHDRAW,,,,5000,",
  ].join("\n");

  await act(async () => {
    fireEvent.change(input, { target: { files: [csvFile(text)] } });
  });
  await waitFor(() => expect(screen.getByText(/valid,.*invalid/)).toBeInTheDocument());

  await act(async () => screen.getByText(/Import \d+ valid transaction/).click());

  await waitFor(() => expect(screen.getByText(/Imported \d+ of \d+ transaction/)).toBeInTheDocument());

  expect(buyTransaction).toHaveBeenCalledWith(1, expect.objectContaining({ symbol: "PTT.BK", shares: 100, price_per_share: 35 }));
  expect(sellTransaction).toHaveBeenCalledWith(1, expect.objectContaining({ symbol: "PTT.BK", shares: 50, price_per_share: 36 }));
  expect(dividendTransaction).toHaveBeenCalledWith(1, expect.objectContaining({ symbol: "PTT.BK", amount: 250 }));
  expect(depositTransaction).toHaveBeenCalledWith(1, expect.objectContaining({ amount: 10000 }));
  expect(withdrawTransaction).toHaveBeenCalledWith(1, expect.objectContaining({ amount: 5000 }));
});

test("a failed row does not stop later rows from being imported, and the summary reflects the partial result", async () => {
  buyTransaction
    .mockRejectedValueOnce(new Error("API 422: shares must be positive"))
    .mockResolvedValueOnce(txResult({ symbol: "SCB.BK" }));

  const input = await selectPortfolioAndGetInput();
  const text = [HEADER, "2026-08-10,BUY,PTT.BK,100,35,,", "2026-08-11,BUY,SCB.BK,10,120,,"].join("\n");

  await act(async () => {
    fireEvent.change(input, { target: { files: [csvFile(text)] } });
  });
  await waitFor(() => expect(screen.getByText(/valid,.*invalid/)).toBeInTheDocument());

  await act(async () => screen.getByText(/Import \d+ valid transaction/).click());

  await waitFor(() => expect(screen.getByText(/Imported 1 of 2 transaction/)).toBeInTheDocument());
  expect(buyTransaction).toHaveBeenCalledTimes(2);
  expect(screen.getByText(/API 422: shares must be positive/)).toBeInTheDocument();
});

test("a portfolio switch that happens while an import is still running does not let the stale result overwrite the new portfolio's reset state", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1), makePortfolio(2)]);

  let resolveBuy!: (v: TransactionResult) => void;
  buyTransaction.mockReturnValue(new Promise<TransactionResult>((resolve) => { resolveBuy = resolve; }));

  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <CsvImportPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());
  const input = await screen.findByLabelText("Upload CSV file");

  const text = [HEADER, "2026-08-10,BUY,PTT.BK,100,35,,"].join("\n");
  await act(async () => {
    fireEvent.change(input, { target: { files: [csvFile(text)] } });
  });
  await waitFor(() => expect(screen.getByText(/valid,.*invalid/)).toBeInTheDocument());

  await act(async () => {
    screen.getByText(/Import \d+ valid transaction/).click();
  });
  await waitFor(() => expect(screen.getByText(/Importing/)).toBeInTheDocument());

  // Switch away from portfolio 1 while its import is still in flight.
  await act(async () => screen.getByText("select-B").click());
  await waitFor(() => expect(screen.getByLabelText("Upload CSV file")).toBeInTheDocument());

  // Now let the slow API call for portfolio 1's row resolve.
  await act(async () => {
    resolveBuy(txResult());
  });

  expect(buyTransaction).toHaveBeenCalledWith(1, expect.objectContaining({ symbol: "PTT.BK" }));
  // The now-finished import for the abandoned portfolio must not jump the
  // UI (currently on portfolio 2) to a summary screen.
  expect(screen.getByLabelText("Upload CSV file")).toBeInTheDocument();
  expect(screen.queryByText(/Imported \d+ of \d+ transaction/)).not.toBeInTheDocument();
});

test("switching portfolios resets the import flow", async () => {
  listPortfolios.mockResolvedValue([makePortfolio(1), makePortfolio(2)]);
  render(
    <PortfolioProvider>
      <SwitcherProbe />
      <CsvImportPage />
    </PortfolioProvider>
  );
  await waitFor(() => expect(screen.getByText(/Select a portfolio/)).toBeInTheDocument());
  await act(async () => screen.getByText("select-A").click());
  const input = await screen.findByLabelText("Upload CSV file");

  const text = [HEADER, "2026-08-10,BUY,PTT.BK,100,35,,"].join("\n");
  await act(async () => {
    fireEvent.change(input, { target: { files: [csvFile(text)] } });
  });
  await waitFor(() => expect(screen.getByText(/valid,.*invalid/)).toBeInTheDocument());

  // Switching to a different portfolio must not let the in-progress preview
  // built for portfolio 1 survive onto portfolio 2.
  await act(async () => screen.getByText("select-B").click());
  await waitFor(() => expect(screen.getByLabelText("Upload CSV file")).toBeInTheDocument());
  expect(screen.queryByText(/valid,.*invalid/)).not.toBeInTheDocument();
});
