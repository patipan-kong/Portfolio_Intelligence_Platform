"use client";

import { useEffect, useRef, useState } from "react";
import {
  listPositionIntents,
  putPositionIntent,
  type IntentSoftPreference,
  type PositionIntentInput,
  type PositionIntentRow,
  type PositionIntentView,
} from "@/lib/api";

const PREFERENCE_LABELS: Record<IntentSoftPreference, string> = {
  NONE: "No preference",
  PREFER_KEEP: "Prefer to keep",
  PREFER_EXIT: "Prefer to exit",
};

type Draft = Omit<PositionIntentInput, "expected_revision">;

function draftFor(row: PositionIntentRow): Draft {
  return row.intent
    ? {
        increase_prohibited: row.intent.increase_prohibited,
        decrease_prohibited: row.intent.decrease_prohibited,
        soft_preference: row.intent.soft_preference,
      }
    // A new intent starts unrestricted, but nothing is saved until the owner confirms.
    : { increase_prohibited: false, decrease_prohibited: false, soft_preference: "NONE" };
}

// In-flight saves are keyed by portfolio AND symbol, so a pending save in one
// portfolio never disables the same symbol in another.
function savingKey(portfolioId: number, symbol: string): string {
  return `${portfolioId}:${symbol}`;
}

function isRevisionConflict(err: unknown): boolean {
  return err instanceof Error && err.message.startsWith("API 409:");
}

function describeSaved(row: PositionIntentRow): string {
  if (!row.intent) return "No confirmed intent";
  const { increase_prohibited: inc, decrease_prohibited: dec, soft_preference: pref } = row.intent;
  return `Saved now (revision ${row.intent.revision}): Do not increase ${inc ? "on" : "off"} · `
    + `Do not decrease ${dec ? "on" : "off"} · ${PREFERENCE_LABELS[pref]}`;
}

export default function PositionInvestorIntent({ portfolioId }: { portfolioId: number }) {
  const [view, setView] = useState<PositionIntentView | null>(null);
  const [drafts, setDrafts] = useState<Record<string, Draft>>({});
  const [loading, setLoading] = useState(true);
  const [savingKeys, setSavingKeys] = useState<Record<string, true>>({});
  // Symbols whose save was rejected because the saved intent changed meanwhile.
  const [conflicts, setConflicts] = useState<Record<string, true>>({});
  const [error, setError] = useState<string | null>(null);
  const currentPortfolioIdRef = useRef(portfolioId);

  useEffect(() => {
    currentPortfolioIdRef.current = portfolioId;
    let active = true;
    setLoading(true);
    setError(null);
    setView(null);
    setDrafts({});
    setConflicts({});
    listPositionIntents(portfolioId)
      .then((next) => { if (active) setView(next); })
      .catch((err: unknown) => {
        if (active) setError(err instanceof Error ? err.message : "Unable to load investor intent");
      })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [portfolioId]);

  function draft(row: PositionIntentRow): Draft {
    return drafts[row.position_symbol] ?? draftFor(row);
  }

  function update(row: PositionIntentRow, patch: Partial<Draft>) {
    setDrafts((current) => ({ ...current, [row.position_symbol]: { ...draft(row), ...patch } }));
  }

  function clearConflict(symbol: string) {
    setConflicts((current) => {
      const next = { ...current };
      delete next[symbol];
      return next;
    });
  }

  // A stale expected_revision: reload the saved state so the next save uses the
  // current revision, keep the owner's attempted values as an unsaved draft,
  // and show what is saved now so the owner can review before saving again.
  async function recoverFromRevisionConflict(requestPortfolioId: number, symbol: string, attempted: Draft) {
    try {
      const next = await listPositionIntents(requestPortfolioId);
      if (currentPortfolioIdRef.current !== requestPortfolioId) return;
      setView(next);
      setDrafts((current) => ({ ...current, [symbol]: attempted }));
      setConflicts((current) => ({ ...current, [symbol]: true }));
      setError(`The saved intent for ${symbol} changed since this page loaded. Your edits are kept but not saved; `
        + "review them against what is saved now, then save again.");
    } catch {
      if (currentPortfolioIdRef.current !== requestPortfolioId) return;
      setError(`The saved intent for ${symbol} changed since this page loaded, and the latest version `
        + "could not be loaded. Reload the page before saving again.");
    }
  }

  async function save(row: PositionIntentRow) {
    const requestPortfolioId = portfolioId;
    const symbol = row.position_symbol;
    const key = savingKey(requestPortfolioId, symbol);
    // The row's controls are disabled while this request is in flight, so the
    // draft sent here is exactly what the owner sees until it settles.
    const attempted = draft(row);
    setSavingKeys((current) => ({ ...current, [key]: true }));
    setError(null);
    try {
      const result = await putPositionIntent(requestPortfolioId, symbol, {
        ...attempted,
        expected_revision: row.intent?.revision ?? null,
      });
      if (currentPortfolioIdRef.current !== requestPortfolioId) return;
      setView((current) => current && {
        ...current,
        positions: current.positions.map((item) => item.position_symbol === symbol
          ? { ...item, intent: result.intent, intent_status: "CONFIRMED" }
          : item),
      });
      setDrafts((current) => {
        const next = { ...current };
        delete next[symbol];
        return next;
      });
      clearConflict(symbol);
    } catch (err) {
      if (currentPortfolioIdRef.current !== requestPortfolioId) return;
      if (isRevisionConflict(err)) {
        await recoverFromRevisionConflict(requestPortfolioId, symbol, attempted);
      } else {
        setError(err instanceof Error ? err.message : "Unable to save investor intent");
      }
    } finally {
      setSavingKeys((current) => {
        const next = { ...current };
        delete next[key];
        return next;
      });
    }
  }

  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm" aria-labelledby="investor-intent-heading">
      <h2 id="investor-intent-heading" className="text-sm font-semibold text-gray-700">
        Investor Intent (V1)
      </h2>
      <p className="text-xs text-gray-500 mt-1">Your own restrictions and preferences for each position.</p>
      <p role="note" className="text-xs text-amber-800 bg-amber-50 border border-amber-200 rounded px-2 py-1 mt-2">
        {view?.disclosure
          ?? "Investor Intent V1 is saved for your records only. It is not yet read or enforced by the portfolio optimizer."}
      </p>

      {loading ? <p className="text-sm text-gray-400 mt-3">Loading…</p> : view && (
        view.positions.length === 0 ? (
          <p className="text-sm text-gray-500 mt-3">No positions in this portfolio.</p>
        ) : (
          <ul className="mt-3 space-y-2">
            {view.positions.map((row) => {
              const value = draft(row);
              const dirty = row.position_symbol in drafts;
              const confirmed = row.intent !== null && row.intent_status === "CONFIRMED";
              const needsReconfirmation = row.intent !== null && row.intent_status === "RECONFIRMATION_REQUIRED";
              // A confirmed intent saves only after a change; a missing or
              // earlier-holding intent always needs an explicit confirmation.
              const canSave = confirmed ? dirty : true;
              const rowSaving = savingKey(portfolioId, row.position_symbol) in savingKeys;
              return (
                <li key={row.position_symbol} className="border rounded-lg px-3 py-2 space-y-2"
                    aria-label={`Intent for ${row.position_symbol}`}>
                  <div className="flex flex-wrap items-center gap-2 text-sm">
                    <span className="font-medium text-gray-800">{row.position_symbol}</span>
                    <span className={`text-xs ${confirmed ? "text-green-700" : needsReconfirmation ? "text-amber-700" : "text-gray-500"}`}
                          title={needsReconfirmation
                            ? "You sold this position fully and bought it again. The earlier intent is kept as history and does not apply until you re-confirm it."
                            : undefined}>
                      {confirmed && row.intent ? `Confirmed · revision ${row.intent.revision}`
                        : needsReconfirmation && row.intent
                          ? `Re-confirmation needed · revision ${row.intent.revision} was for an earlier holding`
                          : "No confirmed intent"}
                    </span>
                    {!row.currently_held && <span className="text-xs text-gray-500">Not currently held</span>}
                    {row.legacy_lock_status && (
                      <span className="text-xs text-amber-700"
                            title="This older lock is kept exactly as it works today. It is not converted into Investor Intent.">
                        Legacy lock (meaning unconfirmed)
                      </span>
                    )}
                  </div>
                  {conflicts[row.position_symbol] && (
                    <p className="text-xs text-amber-800">{describeSaved(row)}</p>
                  )}
                  <div className="flex flex-wrap items-center gap-4 text-xs text-gray-700">
                    <label className="flex items-center gap-1">
                      <input type="checkbox" checked={value.increase_prohibited} disabled={rowSaving}
                             onChange={(e) => update(row, { increase_prohibited: e.target.checked })} />
                      Do not increase
                    </label>
                    <label className="flex items-center gap-1">
                      <input type="checkbox" checked={value.decrease_prohibited} disabled={rowSaving}
                             onChange={(e) => update(row, { decrease_prohibited: e.target.checked })} />
                      Do not decrease
                    </label>
                    <label className="flex items-center gap-1">
                      Preference
                      <select value={value.soft_preference} className="border rounded px-1 py-0.5" disabled={rowSaving}
                              onChange={(e) => update(row, { soft_preference: e.target.value as IntentSoftPreference })}>
                        {(Object.keys(PREFERENCE_LABELS) as IntentSoftPreference[]).map((key) => (
                          <option key={key} value={key}>{PREFERENCE_LABELS[key]}</option>
                        ))}
                      </select>
                    </label>
                    <button type="button" onClick={() => save(row)}
                            disabled={!canSave || rowSaving}
                            className="text-xs text-blue-600 border border-blue-200 rounded px-2.5 py-1 hover:bg-blue-50 disabled:opacity-40">
                      {confirmed ? "Save changes" : needsReconfirmation ? "Re-confirm intent" : "Confirm intent"}
                    </button>
                  </div>
                </li>
              );
            })}
          </ul>
        )
      )}
      {error && <p className="text-xs text-red-600 mt-2">{error}</p>}
    </section>
  );
}
