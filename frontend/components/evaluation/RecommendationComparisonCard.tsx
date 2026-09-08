"use client";

import { useState } from "react";
import Link from "next/link";
import type {
  RecommendationComparison,
  RecommendationComparisonAllocationEntry,
  RecommendationComparisonField,
  RecommendationComparisonSection,
  RecommendationComparisonSectorEntry,
  RecommendationComparisonSubsection,
  RecommendationComparisonValue,
} from "@/lib/api";

function formatDate(value: string | null): string {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value.slice(0, 10);
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function formatValue(value: RecommendationComparisonValue): string {
  if (value == null) return "—";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") return value.toLocaleString("en-US", { maximumFractionDigits: 8 });
  return value;
}

function formatDelta(value: number | undefined): string | null {
  if (value == null) return null;
  const rendered = value.toLocaleString("en-US", { maximumFractionDigits: 8 });
  return `Delta: ${value >= 0 ? "+" : ""}${rendered}`;
}

function StatusLabel({ status }: { status: "added" | "removed" | "changed" }) {
  return <span className="text-[10px] font-semibold uppercase tracking-wide text-gray-500">{status.charAt(0).toUpperCase() + status.slice(1)}</span>;
}

function ScalarFields({ fields }: { fields: RecommendationComparisonField[] }) {
  if (fields.length === 0) return null;
  return (
    <div className="space-y-2">
      {fields.map((field) => (
        <div key={field.key} className="text-xs text-gray-600">
          <p className="font-medium text-gray-700">{field.label}</p>
          <div className="flex flex-wrap gap-x-3 gap-y-1">
            <span>Previous: {formatValue(field.previous)}</span>
            <span>Current: {formatValue(field.current)}</span>
            {formatDelta(field.delta) && <span>{formatDelta(field.delta)}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}

function SectorEntries({ entries }: { entries: RecommendationComparisonSectorEntry[] }) {
  if (entries.length === 0) return null;
  return (
    <div className="space-y-2">
      <p className="text-xs font-medium text-gray-500">Resolved sector limits</p>
      {entries.map((entry) => (
        <div key={entry.sector} className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-gray-600">
          <span className="font-medium text-gray-700 break-words">{entry.sector}</span>
          <StatusLabel status={entry.status} />
          {entry.previous != null && <span>Previous: {formatValue(entry.previous)}</span>}
          {entry.current != null && <span>Current: {formatValue(entry.current)}</span>}
          {formatDelta(entry.delta) && <span>{formatDelta(entry.delta)}</span>}
        </div>
      ))}
    </div>
  );
}

function AllocationEntries({ entries }: { entries: RecommendationComparisonAllocationEntry[] }) {
  if (entries.length === 0) return null;
  return (
    <div className="space-y-2">
      {entries.map((entry) => (
        <div key={entry.symbol} className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-gray-600">
          <span className="font-semibold font-mono text-gray-800 break-all">{entry.symbol}</span>
          <StatusLabel status={entry.status} />
          {entry.previous_target_weight != null && <span>Previous: {formatValue(entry.previous_target_weight)}%</span>}
          {entry.current_target_weight != null && <span>Current: {formatValue(entry.current_target_weight)}%</span>}
          {formatDelta(entry.delta) && <span>{formatDelta(entry.delta)}%</span>}
          {entry.previous_action != null && <span>Previous action: {entry.previous_action}</span>}
          {entry.current_action != null && <span>Current action: {entry.current_action}</span>}
        </div>
      ))}
    </div>
  );
}

function Subsection({ title, value }: { title: string; value: RecommendationComparisonSubsection }) {
  return (
    <div className="space-y-2">
      <p className="text-xs font-medium text-gray-500">{title}</p>
      {value.status === "unavailable" && <p className="text-xs text-gray-400 italic">Not available for this recommendation.</p>}
      <ScalarFields fields={value.fields} />
    </div>
  );
}

function ChangedSection({ section }: { section: RecommendationComparisonSection }) {
  const hasUnavailableSectors = section.sectors_status === "unavailable";
  const hasUnavailableBody =
    section.status === "unavailable" &&
    section.fields.length === 0 &&
    (!section.sectors || section.sectors.length === 0) &&
    !section.dna &&
    !section.style &&
    !section.entries;
  return (
    <div className="border-t border-gray-100 pt-3 first:border-t-0 first:pt-0 space-y-2">
      <h3 className="text-sm font-semibold text-gray-800">{section.label}</h3>
      {hasUnavailableBody && <p className="text-xs text-gray-400 italic">Not available for this recommendation.</p>}
      <ScalarFields fields={section.fields} />
      {section.sectors && <SectorEntries entries={section.sectors} />}
      {hasUnavailableSectors && <p className="text-xs text-gray-400 italic">Resolved sector limits are not available for this recommendation.</p>}
      {section.entries && <AllocationEntries entries={section.entries} />}
      {section.dna && <Subsection title="Portfolio DNA" value={section.dna} />}
      {section.style && <Subsection title="Style drift" value={section.style} />}
    </div>
  );
}

export default function RecommendationComparisonCard({
  comparison,
  portfolioId,
  loading = false,
  error = null,
}: {
  comparison: RecommendationComparison | null;
  portfolioId: number;
  loading?: boolean;
  error?: string | null;
}) {
  const [open, setOpen] = useState(false);
  const hasChanges = comparison?.status === "ok" && comparison.sections.length > 0;

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-4 py-2.5 border-b border-gray-100 bg-gray-50/60">
        {hasChanges ? (
          <button
            type="button"
            className="w-full flex items-center justify-between gap-3 text-left"
            aria-expanded={open}
            aria-controls="recommendation-comparison-details"
            onClick={() => setOpen((value) => !value)}
          >
            <span className="text-xs font-bold text-gray-600 uppercase tracking-wide">4 · Compared to Previous Recommendation</span>
            <span className="text-xs text-blue-600" aria-hidden="true">{open ? "▴" : "▾"}</span>
          </button>
        ) : (
          <h2 className="text-xs font-bold text-gray-600 uppercase tracking-wide">4 · Compared to Previous Recommendation</h2>
        )}
      </div>

      {loading && <div className="p-4 text-sm text-gray-400 italic">Loading comparison…</div>}
      {!loading && error && <div className="p-4 text-sm text-gray-400 italic">Comparison unavailable — {error}</div>}
      {!loading && !error && !comparison && <div className="p-4 text-sm text-gray-400 italic">Comparison unavailable.</div>}
      {!loading && !error && comparison?.status === "no_previous" && (
        <div className="p-4 text-sm text-gray-400 italic">No previous recommendation is available for comparison.</div>
      )}
      {!loading && !error && comparison?.status === "ok" && comparison.sections.length === 0 && (
        <div className="p-4 text-sm text-gray-400 italic">No tracked recommendation inputs changed from the previous snapshot.</div>
      )}
      {!loading && !error && hasChanges && open && comparison && comparison.previous && (
        <div id="recommendation-comparison-details" className="p-4 space-y-4">
          <div className="flex flex-wrap items-center gap-3 text-xs text-gray-500">
            <div>
              <p className="font-semibold text-gray-700">Previous recommendation</p>
              <p>{formatDate(comparison.previous.created_at)}</p>
            </div>
            <span className="text-gray-400" aria-hidden="true">→</span>
            <div>
              <p className="font-semibold text-gray-700">This recommendation</p>
              <p>{formatDate(comparison.current.created_at)}</p>
            </div>
            <Link
              href={`/ai-analytics/recommendations/${comparison.previous.snapshot_id}?portfolio_id=${portfolioId}`}
              className="text-blue-600 hover:underline sm:ml-auto"
            >
              View previous recommendation
            </Link>
          </div>
          <div className="space-y-3">
            {comparison.sections.map((section) => <ChangedSection key={section.key} section={section} />)}
          </div>
        </div>
      )}
    </div>
  );
}
