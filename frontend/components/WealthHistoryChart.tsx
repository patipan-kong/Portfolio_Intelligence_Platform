"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { WealthHistoryPoint } from "@/lib/wealthHistory";

function fmtTHB(n: number): string {
  return n.toLocaleString("th-TH", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fullDate(d: string): string {
  return new Date(d + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

function CustomTooltip({
  active,
  payload,
}: {
  active?: boolean;
  payload?: Array<{ value: number; payload: { date: string } }>;
}) {
  if (!active || !payload?.length) return null;
  const pt = payload[0];
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-2.5 shadow-lg text-xs min-w-[140px] space-y-1">
      <p className="font-semibold text-gray-700">{fullDate(pt.payload.date)}</p>
      <p className="text-gray-800 font-medium">฿{fmtTHB(pt.value)}</p>
    </div>
  );
}

// Complete-coverage points only — the caller filters out partial-coverage
// dates before passing them here, so this chart never has to reason about
// coverage itself; it only draws what it's given.
export default function WealthHistoryChart({ points }: { points: WealthHistoryPoint[] }) {
  return (
    <div className="h-40">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={points} margin={{ top: 4, right: 8, left: 8, bottom: 0 }}>
          <defs>
            <linearGradient id="gradWealthHistory" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.25} />
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="date" tick={{ fontSize: 10, fill: "#9ca3af" }} tickLine={false} axisLine={false} minTickGap={40} />
          <YAxis hide domain={["auto", "auto"]} />
          <Tooltip content={<CustomTooltip />} />
          <Area type="monotone" dataKey="totalValue" stroke="#3b82f6" strokeWidth={2} fill="url(#gradWealthHistory)" dot={false} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
