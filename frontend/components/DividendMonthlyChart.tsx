"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function formatMonth(m: string): string {
  const [y, mo] = m.split("-");
  return new Date(Number(y), Number(mo) - 1, 1).toLocaleDateString("en-US", { month: "short", year: "2-digit" });
}

function CustomTooltip({ active, payload, label, currency }: {
  active?: boolean;
  payload?: Array<{ value: number | null }>;
  label?: string;
  currency: string;
}) {
  if (!active || !payload?.length) return null;
  const v = payload[0]?.value;
  return (
    <div className="bg-white border border-gray-200 rounded-lg px-3 py-2 shadow-md text-xs">
      <p className="text-gray-500 mb-1">{label ? formatMonth(label) : ""}</p>
      <p className="font-semibold text-emerald-700 tabular-nums">
        {v != null ? `${currency} ${v.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : "—"}
      </p>
    </div>
  );
}

export default function DividendMonthlyChart({
  data,
  currency,
}: {
  data: Array<{ month: string; amount: number }>;
  currency: string;
}) {
  if (!data.length) {
    return (
      <div className="h-40 flex items-center justify-center text-sm text-gray-400">
        No dividend income recorded yet.
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={160}>
      <BarChart data={data} margin={{ top: 4, right: 20, left: 4, bottom: 4 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
        <XAxis
          dataKey="month"
          tickFormatter={formatMonth}
          tick={{ fontSize: 11, fill: "#9ca3af" }}
          tickLine={false}
          axisLine={false}
          minTickGap={20}
        />
        <YAxis
          tickFormatter={(v: number) => v.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          tick={{ fontSize: 11, fill: "#9ca3af" }}
          tickLine={false}
          axisLine={false}
          width={48}
        />
        <Tooltip content={<CustomTooltip currency={currency} />} cursor={{ fill: "#f3f4f6" }} />
        <Bar dataKey="amount" name="Dividend income" fill="#10b981" radius={[3, 3, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
