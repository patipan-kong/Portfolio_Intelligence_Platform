// Shared display formatting for the Cross-Portfolio Exposure Snapshot
// sections — kept tiny and local to this feature rather than a new
// general-purpose formatter module.

export const formatThb = (value: number) =>
  value.toLocaleString("th-TH", { style: "currency", currency: "THB", minimumFractionDigits: 2 });

export const formatPct = (value: number) => `${value.toFixed(1)}%`;
