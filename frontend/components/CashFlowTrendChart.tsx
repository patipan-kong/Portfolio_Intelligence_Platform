"use client";

import {
  Bar,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatMonthLabel } from "@/lib/cashFlow";
import type { CashFlowTrendPoint } from "@/lib/cashFlowTrend";

function fmtThb(value: number): string {
  return value.toLocaleString("th-TH", { style: "currency", currency: "THB", minimumFractionDigits: 2 });
}

const MONTH_ABBREV = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function shortMonthLabel(month: string): string {
  const [year, monthNumber] = month.split("-").map(Number);
  return `${MONTH_ABBREV[monthNumber - 1]} '${String(year).slice(2)}`;
}

interface ChartDatum {
  month: string;
  status: CashFlowTrendPoint["status"];
  income: number | null;
  expenses: number | null;
  netCashFlow: number | null;
}

function CustomTooltip({ active, payload }: { active?: boolean; payload?: Array<{ payload: ChartDatum }> }) {
  if (!active || !payload?.length) return null;
  const datum = payload[0].payload;
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-2.5 shadow-lg text-xs min-w-[160px] space-y-1">
      <p className="font-semibold text-gray-700">{formatMonthLabel(datum.month)}</p>
      {datum.status === "AVAILABLE" ? (
        <>
          <p className="text-green-700">Income: {fmtThb(datum.income!)}</p>
          <p className="text-red-700">Expenses: {fmtThb(datum.expenses!)}</p>
          <p className="text-gray-800 font-medium">Net Cash Flow: {fmtThb(datum.netCashFlow!)}</p>
        </>
      ) : (
        <p className="text-gray-500">{datum.status === "PRE_TRACKING" ? "Before tracking began" : "Could not load"}</p>
      )}
    </div>
  );
}

/**
 * Renders only what it is given — PRE_TRACKING/UNAVAILABLE points must arrive
 * with null income/expenses/netCashFlow so Recharts skips drawing bars and
 * breaks the Net Cash Flow line rather than bridging or zeroing the gap.
 */
export default function CashFlowTrendChart({ points }: { points: CashFlowTrendPoint[] }) {
  const data: ChartDatum[] = points.map((point) => ({
    month: point.month,
    status: point.status,
    income: point.income,
    expenses: point.expenses,
    netCashFlow: point.netCashFlow,
  }));
  const gapMonths = points.filter((point) => point.status !== "AVAILABLE");
  const preTrackingMonths = gapMonths.filter((point) => point.status === "PRE_TRACKING");
  const unavailableMonths = gapMonths.filter((point) => point.status === "UNAVAILABLE");

  return (
    <div>
      <div className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 4, right: 8, left: 8, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="month" tickFormatter={shortMonthLabel} tick={{ fontSize: 10, fill: "#9ca3af" }} tickLine={false} axisLine={false} minTickGap={20} />
            <YAxis hide domain={["auto", "auto"]} />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ fontSize: 11 }} />
            <ReferenceLine y={0} stroke="#d1d5db" />
            <Bar dataKey="income" name="Income" fill="#22c55e" radius={[2, 2, 0, 0]} />
            <Bar dataKey="expenses" name="Expenses" fill="#ef4444" radius={[2, 2, 0, 0]} />
            <Line type="monotone" dataKey="netCashFlow" name="Net Cash Flow" stroke="#2563eb" strokeWidth={2} dot={{ r: 3 }} connectNulls={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      {gapMonths.length > 0 && (
        <p className="text-xs text-gray-500 mt-2">
          {preTrackingMonths.length > 0 && `${preTrackingMonths.length} month${preTrackingMonths.length === 1 ? "" : "s"} before tracking began`}
          {preTrackingMonths.length > 0 && unavailableMonths.length > 0 && "; "}
          {unavailableMonths.length > 0 && `${unavailableMonths.length} month${unavailableMonths.length === 1 ? "" : "s"} could not load`}
          {" are shown as gaps, not ฿0."}
        </p>
      )}
    </div>
  );
}
