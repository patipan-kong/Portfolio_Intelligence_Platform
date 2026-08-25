"use client";

import { Fragment, useState } from "react";
import Link from "next/link";
import type { PositionConversionDetail, TransactionRecord, TransactionType } from "@/lib/api";

const TZ = "Asia/Bangkok";

function formatDate(iso: string): string {
  const d = new Date(iso);
  return (
    d.toLocaleDateString("th-TH", { day: "2-digit", month: "short", year: "2-digit", timeZone: TZ }) +
    " " +
    d.toLocaleTimeString("th-TH", { hour: "2-digit", minute: "2-digit", timeZone: TZ })
  );
}

// Conversion detail dates are plain "YYYY-MM-DD" calendar dates, not
// timestamps — formatted in UTC so no local/Bangkok timezone shift can move
// the displayed day relative to the stored date.
function formatPlainDate(d: string): string {
  return new Date(d + "T00:00:00Z").toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  });
}

function fmt(n: number | null | undefined, decimals = 2): string {
  if (n == null) return "—";
  return n.toLocaleString(undefined, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

function stripBk(symbol: string): string {
  return symbol.replace(".BK", "");
}

// Reuses the exact colors already assigned to these transaction types
// elsewhere in the app (transaction action buttons on /portfolio, and the
// non-performance disclosure banner on /performance) so a given type reads
// the same way everywhere.
export const TYPE_STYLE: Record<TransactionType, { label: string; color: string; bg: string }> = {
  BUY:                  { label: "Buy",                color: "#27500A", bg: "#27500A18" },
  SELL:                 { label: "Sell",               color: "#854F0B", bg: "#854F0B18" },
  DEPOSIT:              { label: "Deposit",             color: "#0C447C", bg: "#0C447C18" },
  WITHDRAW:             { label: "Withdraw",            color: "#791F1F", bg: "#791F1F18" },
  DIVIDEND:             { label: "Dividend",            color: "#0F6E56", bg: "#0F6E5618" },
  INITIAL_POSITION:     { label: "Imported Position",   color: "#7C3AED", bg: "#7C3AED18" },
  INITIAL_CASH:         { label: "Starting Cash",       color: "#0C447C", bg: "#0C447C18" },
  QUANTITY_CORRECTION:  { label: "Quantity Correction", color: "#C2660B", bg: "#C2660B18" },
  POSITION_CONVERSION:  { label: "Position Conversion", color: "#4338CA", bg: "#4338CA18" },
};

function TypeBadge({ type }: { type: TransactionType }) {
  const style = TYPE_STYLE[type] ?? { label: type, color: "#4B5563", bg: "#4B556318" };
  return (
    <span
      className="inline-block text-xs font-semibold px-1.5 py-0.5 rounded whitespace-nowrap"
      style={{ color: style.color, backgroundColor: style.bg }}
    >
      {style.label}
    </span>
  );
}

// QUANTITY_CORRECTION's total_amount is abs(shares_delta) * price — a
// notional valuation only; the service never touches cash_balance for it.
// POSITION_CONVERSION's total_amount is the cost basis carried to the
// successor holding, not a cash flow either — UNLESS the conversion has a
// cash-in-lieu leg (a fractional share settled in cash), which IS real cash
// into the account. Both would otherwise look identical to a real cash
// movement (BUY/SELL/DEPOSIT/WITHDRAW/DIVIDEND) in this same column, so
// they're labeled explicitly rather than left implicit.
const ALWAYS_NO_CASH_IMPACT_TYPES: ReadonlySet<TransactionType> = new Set(["QUANTITY_CORRECTION"]);

function AmountCell({ tx }: { tx: TransactionRecord }) {
  const cashInLieu = tx.type === "POSITION_CONVERSION" ? tx.conversion_detail?.cash_in_lieu : null;
  const noCashImpact = ALWAYS_NO_CASH_IMPACT_TYPES.has(tx.type) || (tx.type === "POSITION_CONVERSION" && !cashInLieu);
  return (
    <>
      {fmt(tx.total_amount)} <span className="text-xs text-gray-400 font-normal">{tx.currency}</span>
      {noCashImpact && (
        <span className="block text-xs text-gray-400 font-normal">(no cash impact)</span>
      )}
      {cashInLieu && (
        <span className="block text-xs text-gray-400 font-normal">
          (cash in lieu: {fmt(cashInLieu.net_cash)} {tx.currency})
        </span>
      )}
    </>
  );
}

function SymbolCell({ symbol }: { symbol: string | null }) {
  if (!symbol) return <span className="text-gray-400 text-sm">Cash</span>;
  return (
    <Link href={`/stock/${encodeURIComponent(symbol)}`} className="text-sm font-medium text-blue-700 hover:underline">
      {symbol.replace(".BK", "")}
      {symbol.endsWith(".BK") && <span className="ml-1 text-xs text-gray-400">.BK</span>}
    </Link>
  );
}

function DetailField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-gray-400">{label}</dt>
      <dd className="text-gray-700 font-medium">{value}</dd>
    </div>
  );
}

// Human-readable presentation of the canonical POSITION_CONVERSION contract
// — never raw JSON. Every field comes from the parsed, validated payload
// (backend main.py::_conversion_detail); nothing here is symbol-specific.
function ConversionDetailPanel({ detail }: { detail: PositionConversionDetail }) {
  const showValuationDate = detail.valuation_transition_date !== detail.legal_effective_date;
  return (
    <dl className="grid grid-cols-2 sm:grid-cols-3 gap-x-4 gap-y-2 text-xs py-1">
      <DetailField label="From" value={stripBk(detail.predecessor_symbol)} />
      <DetailField label="To" value={stripBk(detail.successor_symbol)} />
      <DetailField label="Ratio" value={detail.conversion_ratio.toLocaleString(undefined, { maximumFractionDigits: 6 })} />
      <DetailField label="Shares surrendered" value={fmt(detail.shares_surrendered, 4)} />
      <DetailField label="Shares received" value={fmt(detail.shares_received, 4)} />
      <DetailField label="Effective date" value={formatPlainDate(detail.legal_effective_date)} />
      {showValuationDate && (
        <DetailField label="Valuation transition date" value={formatPlainDate(detail.valuation_transition_date)} />
      )}
      <DetailField label="Cost basis before" value={fmt(detail.cost_basis_before)} />
      <DetailField label="Cost basis carried" value={fmt(detail.cost_basis_carried)} />
      {detail.cash_in_lieu ? (
        <>
          <DetailField label="Cash in lieu" value={fmt(detail.cash_in_lieu.net_cash)} />
          <DetailField label="Realized P/L" value={fmt(detail.cash_in_lieu.realized_pnl)} />
        </>
      ) : (
        <DetailField label="Cash in lieu" value="None" />
      )}
    </dl>
  );
}

function DetailsToggle({ expanded, onToggle }: { expanded: boolean; onToggle: () => void }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      className="text-xs text-blue-600 hover:text-blue-800 font-medium whitespace-nowrap"
      aria-expanded={expanded}
    >
      {expanded ? "Hide details ▴" : "Details ▾"}
    </button>
  );
}

export default function TransactionHistoryTable({ transactions }: { transactions: TransactionRecord[] }) {
  const [expandedIds, setExpandedIds] = useState<Set<number>>(new Set());

  function toggle(id: number) {
    setExpandedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  if (transactions.length === 0) {
    return (
      <p className="text-gray-500 text-sm py-8 text-center">
        No transactions recorded for this portfolio yet.
      </p>
    );
  }

  return (
    <>
      {/* ── Mobile card view (< md) ── */}
      <div className="md:hidden space-y-3">
        {transactions.map((tx) => {
          const detail = tx.type === "POSITION_CONVERSION" ? tx.conversion_detail : null;
          const expanded = expandedIds.has(tx.id);
          return (
            <div key={tx.id} className="bg-white border rounded-xl p-4 shadow-sm space-y-2">
              <div className="flex items-center justify-between">
                <TypeBadge type={tx.type} />
                <span className="text-xs text-gray-400">{formatDate(tx.transaction_date)}</span>
              </div>
              <div className="flex items-center justify-between">
                <SymbolCell symbol={tx.symbol} />
                <span className="text-sm font-semibold text-gray-800 text-right">
                  <AmountCell tx={tx} />
                </span>
              </div>
              {(tx.shares != null || tx.price_per_share != null) && (
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  {tx.shares != null && <span>Shares: <span className="text-gray-700">{fmt(tx.shares, 4)}</span></span>}
                  {tx.price_per_share != null && <span>Price: <span className="text-gray-700">{fmt(tx.price_per_share)}</span></span>}
                  {tx.fees > 0 && <span>Fees: <span className="text-gray-700">{fmt(tx.fees)}</span></span>}
                </div>
              )}
              {tx.notes && <p className="text-xs text-gray-400 border-t border-gray-100 pt-2">{tx.notes}</p>}
              {detail && (
                <div className="border-t border-gray-100 pt-2">
                  <DetailsToggle expanded={expanded} onToggle={() => toggle(tx.id)} />
                  {expanded && <ConversionDetailPanel detail={detail} />}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* ── Desktop table (≥ md) ── */}
      <div className="hidden md:block overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b text-left text-gray-500">
              <th className="py-2 pr-4 font-medium whitespace-nowrap">Date</th>
              <th className="py-2 pr-4 font-medium whitespace-nowrap">Type</th>
              <th className="py-2 pr-4 font-medium whitespace-nowrap">Symbol</th>
              <th className="py-2 pr-4 font-medium text-right whitespace-nowrap">Shares</th>
              <th className="py-2 pr-4 font-medium text-right whitespace-nowrap">Price</th>
              <th className="py-2 pr-4 font-medium text-right whitespace-nowrap">Amount</th>
              <th className="py-2 pr-4 font-medium text-right whitespace-nowrap">Fees</th>
              <th className="py-2 pr-4 font-medium">Notes</th>
              <th className="py-2 font-medium"></th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => {
              const detail = tx.type === "POSITION_CONVERSION" ? tx.conversion_detail : null;
              const expanded = expandedIds.has(tx.id);
              return (
                <Fragment key={tx.id}>
                  <tr className="border-b last:border-0 hover:bg-gray-50">
                    <td className="py-2 pr-4 text-gray-500 whitespace-nowrap">{formatDate(tx.transaction_date)}</td>
                    <td className="py-2 pr-4"><TypeBadge type={tx.type} /></td>
                    <td className="py-2 pr-4"><SymbolCell symbol={tx.symbol} /></td>
                    <td className="py-2 pr-4 text-right text-gray-700">{fmt(tx.shares, 4)}</td>
                    <td className="py-2 pr-4 text-right text-gray-700">{fmt(tx.price_per_share)}</td>
                    <td className="py-2 pr-4 text-right font-medium text-gray-800">
                      <AmountCell tx={tx} />
                    </td>
                    <td className="py-2 pr-4 text-right text-gray-500">{tx.fees > 0 ? fmt(tx.fees) : "—"}</td>
                    <td className="py-2 pr-4 text-gray-500 text-xs max-w-xs truncate" title={tx.notes ?? undefined}>
                      {tx.notes ?? "—"}
                    </td>
                    <td className="py-2 text-right">
                      {detail && <DetailsToggle expanded={expanded} onToggle={() => toggle(tx.id)} />}
                    </td>
                  </tr>
                  {detail && expanded && (
                    <tr className="border-b last:border-0 bg-gray-50">
                      <td colSpan={9} className="px-4 py-3">
                        <ConversionDetailPanel detail={detail} />
                      </td>
                    </tr>
                  )}
                </Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
