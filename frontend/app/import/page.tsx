"use client";

import { useEffect, useRef, useState } from "react";
import { usePortfolio } from "@/lib/PortfolioContext";
import PortfolioTabs from "@/components/PortfolioTabs";
import { TYPE_STYLE } from "@/components/TransactionHistoryTable";
import {
  parseCsv,
  validateRows,
  buildImportPayload,
  type ParsedImportRow,
} from "@/lib/csvImport";
import {
  buyTransaction,
  sellTransaction,
  dividendTransaction,
  depositTransaction,
  withdrawTransaction,
} from "@/lib/api";

type Phase = "upload" | "preview" | "importing" | "summary";

interface ImportOutcome {
  row: ParsedImportRow;
  ok: boolean;
  message: string;
}

async function executeRow(portfolioId: number, row: ParsedImportRow): Promise<ImportOutcome> {
  try {
    const built = buildImportPayload(row);
    switch (built.type) {
      case "BUY":
        await buyTransaction(portfolioId, built.payload);
        break;
      case "SELL":
        await sellTransaction(portfolioId, built.payload);
        break;
      case "DIVIDEND":
        await dividendTransaction(portfolioId, built.payload);
        break;
      case "DEPOSIT":
        await depositTransaction(portfolioId, built.payload);
        break;
      case "WITHDRAW":
        await withdrawTransaction(portfolioId, built.payload);
        break;
    }
    return { row, ok: true, message: "Imported" };
  } catch (e) {
    return { row, ok: false, message: e instanceof Error ? e.message : "Import failed" };
  }
}

export default function CsvImportPage() {
  const { currentSelection: portfolioId } = usePortfolio();

  const [phase, setPhase] = useState<Phase>("upload");
  const [fileName, setFileName] = useState<string | null>(null);
  const [parseError, setParseError] = useState<string | null>(null);
  const [rows, setRows] = useState<ParsedImportRow[]>([]);
  const [progress, setProgress] = useState({ done: 0, total: 0 });
  const [outcomes, setOutcomes] = useState<ImportOutcome[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Switching portfolios mid-flow could otherwise let a preview/import that
  // was built for the old portfolio carry over to the new one.
  useEffect(() => {
    setPhase("upload");
    setFileName(null);
    setParseError(null);
    setRows([]);
    setOutcomes([]);
  }, [portfolioId]);

  // Tracks the *current* portfolio selection so an in-flight import (which
  // closes over the portfolio id it started with) can tell, after each
  // await, whether the user has since switched away — without that check,
  // a slow import finishing after a switch would stomp the freshly-reset
  // "upload" phase with a summary that belongs to the abandoned portfolio.
  const portfolioIdRef = useRef(portfolioId);
  useEffect(() => {
    portfolioIdRef.current = portfolioId;
  }, [portfolioId]);

  async function handleFile(file: File) {
    setParseError(null);
    const text = await file.text();
    const parsed = parseCsv(text);
    if (!parsed.ok) {
      setParseError(parsed.error);
      setRows([]);
      setFileName(null);
      setPhase("upload");
      return;
    }
    setFileName(file.name);
    setRows(validateRows(parsed.rows));
    setPhase("preview");
  }

  function reset() {
    setPhase("upload");
    setFileName(null);
    setParseError(null);
    setRows([]);
    setOutcomes([]);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  async function handleImport() {
    if (portfolioId == null) return;
    // Captured once: rows must always go to the portfolio the import was
    // started for, even if the user switches the active portfolio mid-run.
    const importPortfolioId = portfolioId;
    const validRows = rows.filter((r) => r.status === "VALID");
    if (validRows.length === 0) return;
    setPhase("importing");
    setProgress({ done: 0, total: validRows.length });

    const results: ImportOutcome[] = [];
    for (const row of validRows) {
      const outcome = await executeRow(importPortfolioId, row);
      results.push(outcome);
      if (portfolioIdRef.current !== importPortfolioId) continue;
      setProgress((p) => ({ ...p, done: p.done + 1 }));
    }
    if (portfolioIdRef.current !== importPortfolioId) return;
    setOutcomes(results);
    setPhase("summary");
  }

  const validCount = rows.filter((r) => r.status === "VALID").length;
  const invalidCount = rows.length - validCount;
  const successCount = outcomes.filter((o) => o.ok).length;
  const failureCount = outcomes.length - successCount;

  return (
    <main className="max-w-5xl mx-auto px-4 py-6 space-y-6">
      <PortfolioTabs />

      <div>
        <h1 className="text-xl font-bold text-gray-900">Import Transactions</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          Bring an existing portfolio&apos;s transaction history in from a CSV file.
        </p>
      </div>

      {portfolioId == null ? (
        <p className="text-center text-gray-400 text-sm py-8">
          Select a portfolio from the navbar to import transactions.
        </p>
      ) : (
        <>
          {phase === "upload" && (
            <div className="space-y-4">
              <div className="border border-dashed border-gray-300 rounded-xl p-6 text-center space-y-3">
                <p className="text-sm text-gray-500">
                  Upload a UTF-8 CSV with columns: <code className="text-xs bg-gray-100 px-1 py-0.5 rounded">date,type,symbol,shares,price,amount,notes</code>
                </p>
                <p className="text-xs text-gray-400">
                  Supported types: BUY, SELL, DIVIDEND, DEPOSIT, WITHDRAW. Dates use YYYY-MM-DD.
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".csv,text/csv"
                  aria-label="Upload CSV file"
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file) handleFile(file);
                  }}
                  className="text-sm mx-auto"
                />
              </div>
              {parseError && (
                <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">
                  {parseError}
                </div>
              )}
            </div>
          )}

          {phase === "preview" && (
            <div className="space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <p className="text-sm font-medium text-gray-700">{fileName}</p>
                  <p className="text-xs text-gray-500">
                    {validCount} valid, {invalidCount} invalid of {rows.length} row{rows.length !== 1 ? "s" : ""}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={reset}
                    className="text-xs text-gray-500 underline hover:no-underline whitespace-nowrap"
                  >
                    Choose different file
                  </button>
                  <button
                    onClick={handleImport}
                    disabled={validCount === 0}
                    className="text-sm font-semibold text-white bg-blue-700 px-4 py-1.5 rounded-lg disabled:opacity-40 hover:opacity-90 transition-opacity"
                  >
                    Import {validCount} valid transaction{validCount !== 1 ? "s" : ""}
                  </button>
                </div>
              </div>

              <div className="overflow-x-auto border rounded-xl">
                <table className="min-w-full text-sm">
                  <thead>
                    <tr className="border-b text-left text-gray-500 bg-gray-50">
                      <th className="py-2 px-3 font-medium whitespace-nowrap">Row</th>
                      <th className="py-2 px-3 font-medium whitespace-nowrap">Status</th>
                      <th className="py-2 px-3 font-medium whitespace-nowrap">Date</th>
                      <th className="py-2 px-3 font-medium whitespace-nowrap">Type</th>
                      <th className="py-2 px-3 font-medium whitespace-nowrap">Symbol</th>
                      <th className="py-2 px-3 font-medium text-right whitespace-nowrap">Shares</th>
                      <th className="py-2 px-3 font-medium text-right whitespace-nowrap">Price</th>
                      <th className="py-2 px-3 font-medium text-right whitespace-nowrap">Amount</th>
                      <th className="py-2 px-3 font-medium">Notes / Errors</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rows.map((r) => {
                      const style = TYPE_STYLE[r.normalizedType as keyof typeof TYPE_STYLE];
                      return (
                        <tr key={r.rowNumber} className={`border-b last:border-0 ${r.status === "INVALID" ? "bg-red-50" : ""}`}>
                          <td className="py-2 px-3 text-gray-400">{r.rowNumber}</td>
                          <td className="py-2 px-3">
                            {r.status === "VALID" ? (
                              <span className="text-xs font-semibold text-green-700">Valid</span>
                            ) : (
                              <span className="text-xs font-semibold text-red-700">Invalid</span>
                            )}
                          </td>
                          <td className="py-2 px-3 text-gray-500 whitespace-nowrap">{r.date}</td>
                          <td className="py-2 px-3 whitespace-nowrap">
                            {style ? (
                              <span
                                className="inline-block text-xs font-semibold px-1.5 py-0.5 rounded whitespace-nowrap"
                                style={{ color: style.color, backgroundColor: style.bg }}
                              >
                                {style.label}
                              </span>
                            ) : (
                              <span className="text-xs text-gray-500">{r.type || "—"}</span>
                            )}
                          </td>
                          <td className="py-2 px-3 text-gray-700">{r.symbol || "—"}</td>
                          <td className="py-2 px-3 text-right text-gray-700">{r.shares || "—"}</td>
                          <td className="py-2 px-3 text-right text-gray-700">{r.price || "—"}</td>
                          <td className="py-2 px-3 text-right text-gray-700">{r.amount || "—"}</td>
                          <td className="py-2 px-3 text-xs">
                            {r.status === "INVALID" ? (
                              <span className="text-red-600">{r.errors.join("; ")}</span>
                            ) : (
                              <span className="text-gray-400">{r.notes || "—"}</span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {phase === "importing" && (
            <div className="space-y-3 py-8 text-center">
              <p className="text-sm text-gray-600">
                Importing {progress.done} of {progress.total}…
              </p>
              <div className="max-w-sm mx-auto h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-700 transition-all"
                  style={{ width: `${progress.total > 0 ? (progress.done / progress.total) * 100 : 0}%` }}
                />
              </div>
            </div>
          )}

          {phase === "summary" && (
            <div className="space-y-4">
              <div className="p-4 bg-gray-50 border rounded-xl text-sm">
                <p className="font-medium text-gray-800">
                  Imported {successCount} of {outcomes.length} transaction{outcomes.length !== 1 ? "s" : ""}
                  {failureCount > 0 && <span className="text-red-600"> ({failureCount} failed)</span>}
                </p>
                {invalidCount > 0 && (
                  <p className="text-xs text-gray-500 mt-1">
                    {invalidCount} row{invalidCount !== 1 ? "s" : ""} skipped for failing validation.
                  </p>
                )}
              </div>

              {failureCount > 0 && (
                <div className="overflow-x-auto border rounded-xl">
                  <table className="min-w-full text-sm">
                    <thead>
                      <tr className="border-b text-left text-gray-500 bg-gray-50">
                        <th className="py-2 px-3 font-medium whitespace-nowrap">Row</th>
                        <th className="py-2 px-3 font-medium whitespace-nowrap">Symbol</th>
                        <th className="py-2 px-3 font-medium">Error</th>
                      </tr>
                    </thead>
                    <tbody>
                      {outcomes
                        .filter((o) => !o.ok)
                        .map((o) => (
                          <tr key={o.row.rowNumber} className="border-b last:border-0 bg-red-50">
                            <td className="py-2 px-3 text-gray-400">{o.row.rowNumber}</td>
                            <td className="py-2 px-3 text-gray-700">{o.row.symbol || "—"}</td>
                            <td className="py-2 px-3 text-red-600 text-xs">{o.message}</td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              )}

              <button
                onClick={reset}
                className="text-sm font-semibold text-white bg-blue-700 px-4 py-1.5 rounded-lg hover:opacity-90 transition-opacity"
              >
                Import another file
              </button>
            </div>
          )}
        </>
      )}
    </main>
  );
}
